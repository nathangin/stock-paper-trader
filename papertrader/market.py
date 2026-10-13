"""Daily price history from Yahoo Finance's chart API, with Stooq as a fallback.

Neither source needs an API key. Yahoo prices are split-adjusted (not dividend-
adjusted), and the response also carries split and dividend events, which the
portfolio code uses to keep share counts and cash right when a held stock splits
or pays a dividend. Stooq has no event data, so it is only a fallback.
"""

import csv
import io
import logging
import time
from dataclasses import dataclass, field
from datetime import date, datetime, time as dtime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger(__name__)

NY = ZoneInfo("America/New_York")
MARKET_OPEN = dtime(9, 30)
# A daily bar is treated as final this long after the 4pm close.
BAR_FINAL_AFTER = dtime(16, 15)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
)


@dataclass
class Bar:
    date: str  # YYYY-MM-DD, exchange-local trading day
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass
class History:
    symbol: str
    bars: list = field(default_factory=list)  # list[Bar], oldest first
    splits: list = field(default_factory=list)  # [{"date", "ratio"}], ratio = new/old shares
    dividends: list = field(default_factory=list)  # [{"date", "amount"}] per (adjusted) share
    source: str = ""

    def bar_on(self, day):
        for bar in self.bars:
            if bar.date == day:
                return bar
        return None

    def first_bar_after(self, day):
        for bar in self.bars:
            if bar.date > day:
                return bar
        return None

    def bars_until(self, day):
        return [b for b in self.bars if b.date <= day]


def make_session():
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(total=3, backoff_factor=1.5, status_forcelist=(429, 500, 502, 503, 504))
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def parse_yahoo_chart(symbol, payload):
    result = (payload.get("chart") or {}).get("result") or []
    if not result:
        err = (payload.get("chart") or {}).get("error")
        raise ValueError(f"Yahoo returned no data for {symbol}: {err}")
    r = result[0]
    tz = ZoneInfo(r.get("meta", {}).get("exchangeTimezoneName") or "America/New_York")
    stamps = r.get("timestamp") or []
    quote = (r.get("indicators", {}).get("quote") or [{}])[0]
    bars = []
    for i, ts in enumerate(stamps):
        o, h, lo, c = (quote.get(k, [None] * len(stamps))[i] for k in ("open", "high", "low", "close"))
        if None in (o, h, lo, c) or c <= 0:
            continue
        v = (quote.get("volume") or [0] * len(stamps))[i] or 0
        day = datetime.fromtimestamp(ts, tz).date().isoformat()
        if bars and bars[-1].date == day:
            bars[-1] = Bar(day, o, h, lo, c, v)  # keep the latest print for a day
        else:
            bars.append(Bar(day, o, h, lo, c, v))

    events = r.get("events") or {}
    splits = []
    for s in (events.get("splits") or {}).values():
        num, den = s.get("numerator"), s.get("denominator")
        if num and den:
            day = datetime.fromtimestamp(s["date"], tz).date().isoformat()
            splits.append({"date": day, "ratio": num / den})
    dividends = []
    for d in (events.get("dividends") or {}).values():
        if d.get("amount"):
            day = datetime.fromtimestamp(d["date"], tz).date().isoformat()
            dividends.append({"date": day, "amount": float(d["amount"])})
    splits.sort(key=lambda s: s["date"])
    dividends.sort(key=lambda d: d["date"])
    return History(symbol, bars, splits, dividends, source="yahoo")


def parse_stooq_csv(symbol, text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows or "Close" not in rows[0]:
        raise ValueError(f"Stooq returned no data for {symbol}: {text[:80]!r}")
    bars = [
        Bar(r["Date"], float(r["Open"]), float(r["High"]), float(r["Low"]), float(r["Close"]),
            float(r.get("Volume") or 0))
        for r in rows
        if r.get("Close") not in (None, "", "0")
    ]
    return History(symbol, bars, source="stooq")


def fetch_yahoo(symbol, session, years=2):
    now = int(time.time())
    params = {
        "period1": now - int(years * 365.25 * 86400), "period2": now,
        "interval": "1d", "events": "div,split", "includePrePost": "false",
    }
    last_error = None
    for host in ("query1", "query2"):
        url = f"https://{host}.finance.yahoo.com/v8/finance/chart/{symbol}"
        try:
            resp = session.get(url, params=params, timeout=20)
            resp.raise_for_status()
            return parse_yahoo_chart(symbol, resp.json())
        except (requests.RequestException, ValueError) as e:
            last_error = e
            log.warning("Yahoo %s failed for %s: %s", host, symbol, e)
    raise RuntimeError(f"Yahoo failed for {symbol}: {last_error}")


def fetch_stooq(symbol, session, years=2):
    start = (date.today() - timedelta(days=365 * years + 10)).strftime("%Y%m%d")
    stooq_symbol = symbol.lower().replace(".", "-") + ".us"
    resp = session.get(
        "https://stooq.com/q/d/l/", params={"s": stooq_symbol, "i": "d", "d1": start}, timeout=20
    )
    resp.raise_for_status()
    return parse_stooq_csv(symbol, resp.text)


def fetch_history(symbol, session=None, years=2):
    """Daily bars for one symbol: Yahoo first, Stooq if Yahoo fails."""
    session = session or make_session()
    try:
        return fetch_yahoo(symbol, session, years)
    except RuntimeError as yahoo_error:
        try:
            hist = fetch_stooq(symbol, session, years)
            log.warning("Using Stooq for %s (no split/dividend data)", symbol)
            return hist
        except (requests.RequestException, ValueError) as stooq_error:
            raise RuntimeError(f"No price data for {symbol}: {yahoo_error}; stooq: {stooq_error}")


def fetch_all(symbols, session=None, years=2, pause=0.25):
    session = session or make_session()
    out, failed = {}, []
    for sym in symbols:
        try:
            out[sym] = fetch_history(sym, session, years)
        except RuntimeError as e:
            log.error("%s", e)
            failed.append(sym)
        time.sleep(pause)
    return out, failed


def drop_unfinished_bar(history, now):
    """Remove today's bar if the session hasn't closed yet (it would be a partial bar)."""
    now_ny = now.astimezone(NY)
    if history.bars and history.bars[-1].date == now_ny.date().isoformat():
        if now_ny.time() < BAR_FINAL_AFTER:
            history.bars = history.bars[:-1]
    return history


def next_session_open(day):
    """9:30am New York on the first weekday after `day` (holidays are not modelled)."""
    d = date.fromisoformat(day) + timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return datetime.combine(d, MARKET_OPEN, NY)


def can_decide(asof, now):
    """True while it is still before the next session's open after `asof`.

    Orders are filled at that open, so a decision made after it would be using
    information the fill price couldn't have reflected (look-ahead bias).
    """
    return now.astimezone(timezone.utc) < next_session_open(asof).astimezone(timezone.utc)
