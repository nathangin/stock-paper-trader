"""Backfill past headlines from GDELT and test the news signal on them.

The live bot only sees headlines from the day it runs, so on its own the news
strategies need months before they can be judged. GDELT's DOC API (free, no
key) can search roughly the last three months of world news, which is enough
for a first, rough answer to "does the news score predict anything?".

Two things to keep in mind when reading the results:
  * GDELT titles come from many more outlets than the live feeds, so the
    headline mix is different. The same relevance filter and scorer are used.
  * Three months is about 60 trading days. Treat the numbers as a smoke test,
    not proof. The t-statistics in the report say how seriously to take them.
"""

import bisect
import gzip
import json
import logging
import math
import statistics
import time
from datetime import datetime, time as dtime, timedelta, timezone
from pathlib import Path

import requests

from . import sentiment
from .market import NY
from .news import Headline, filter_relevant, headline_id
from .predictions import spearman
from .research import align, simulate, stats
from .signals import momentum_score, news_score

log = logging.getLogger(__name__)

GDELT_DOC = "https://api.gdeltproject.org/api/v2/doc/doc"
REQUEST_GAP = 5.5  # GDELT asks for no more than one request every 5 seconds


def gdelt_query(names):
    words = " OR ".join(f'"{n}"' for n in names if len(n) >= 3)
    return f"({words}) (stock OR shares) sourcelang:english"


def parse_gdelt(payload, ticker):
    out = []
    for a in (payload or {}).get("articles", []):
        title = (a.get("title") or "").strip()
        seen = a.get("seendate") or ""
        if not title or not seen:
            continue
        try:
            published = datetime.strptime(seen, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        out.append(Headline(
            id=headline_id(ticker, title), ticker=ticker, title=title, published=published.isoformat(),
            source=a.get("domain", ""), url=a.get("url", ""), feed="gdelt",
        ))
    return out


def fetch_window(session, ticker, names, start, end, tries=3):
    params = {
        "query": gdelt_query(names), "mode": "ArtList", "format": "json", "maxrecords": 250,
        "sort": "HybridRel",
        "startdatetime": start.strftime("%Y%m%d%H%M%S"), "enddatetime": end.strftime("%Y%m%d%H%M%S"),
    }
    for attempt in range(tries):
        try:
            resp = session.get(GDELT_DOC, params=params, timeout=60)
            if resp.status_code == 429 or "limit requests" in resp.text[:200].lower():
                time.sleep(REQUEST_GAP * (attempt + 2))
                continue
            resp.raise_for_status()
            text = resp.text.strip()
            return parse_gdelt(json.loads(text) if text.startswith("{") else {}, ticker)
        except (requests.RequestException, ValueError) as e:
            log.warning("GDELT %s %s: %s", ticker, start.date(), e)
            time.sleep(REQUEST_GAP * (attempt + 1))
    return []


class HistoryStore:
    """One gzipped JSONL file of scored historical headlines per ticker."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)

    def path(self, ticker):
        return self.dir / f"{ticker}.jsonl.gz"

    def load(self, ticker):
        p = self.path(ticker)
        if not p.exists():
            return []
        with gzip.open(p, "rt", encoding="utf-8") as f:
            return [Headline(**json.loads(line)) for line in f if line.strip()]

    def save(self, ticker, headlines):
        rows = sorted({h.id: h for h in headlines}.values(), key=lambda h: h.published)
        with gzip.open(self.path(ticker), "wt", encoding="utf-8") as f:
            for h in rows:
                f.write(json.dumps({
                    "id": h.id, "ticker": h.ticker, "title": h.title, "published": h.published,
                    "source": h.source, "feed": h.feed, "kind": h.kind, "scores": h.scores,
                }, ensure_ascii=False, sort_keys=True) + "\n")


def backfill(cfg, directory, days=90, window_days=3, session=None, now=None):
    """Fetch and score ~`days` of GDELT headlines for every ticker. Returns counts per ticker."""
    session = session or requests.Session()
    now = now or datetime.now(timezone.utc)
    store = HistoryStore(directory)
    counts = {}
    for ticker, names in cfg["aliases"].items():
        found = []
        end = now
        start_limit = now - timedelta(days=days)
        while end > start_limit:
            start = max(start_limit, end - timedelta(days=window_days))
            found += fetch_window(session, ticker, names, start, end)
            end = start
            time.sleep(REQUEST_GAP)
        kept, _ = filter_relevant(found, {ticker: names})
        for h in kept:
            h.scores["lexicon"] = round(sentiment.score_text(h.title), 4)
        store.save(ticker, kept)
        counts[ticker] = len(kept)
        log.info("%s: %d relevant of %d fetched", ticker, len(kept), len(found))
    return counts


# ------------------------------------------------------------------ evaluation


def decision_time(day, hour=17, minute=30):
    """When the live bot decides: 5:30pm New York on `day`."""
    d = datetime.fromisoformat(day).date()
    return datetime.combine(d, dtime(hour, minute), NY).astimezone(timezone.utc)


def daily_scores(headlines_by_ticker, calendar, first, last, half_life, lookback, opinion_weight):
    """{t: {ticker: score}} using only headlines published before each day's decision time."""
    ordered = {}
    for ticker, items in headlines_by_ticker.items():
        items = sorted(items, key=lambda h: h.published)
        ordered[ticker] = (items, [h.published_dt for h in items])
    out = {}
    for t in range(first, last + 1):
        now = decision_time(calendar[t])
        cutoff = now - timedelta(hours=lookback)
        day = {}
        for ticker, (items, stamps) in ordered.items():
            window = items[bisect.bisect_left(stamps, cutoff):bisect.bisect_right(stamps, now)]
            day[ticker] = news_score(window, "lexicon", now, half_life, lookback, opinion_weight=opinion_weight)
        out[t] = day
    return out


def ic_series(scores, calendar, opens, closes, tradable):
    """Daily rank IC of scores against the next day's return.

    tradable=False: close(D) -> close(D+1), which includes the overnight gap the
    bot can't trade (it buys at the open). tradable=True: open(D+1) -> open(D+2),
    what a position bought at the next open actually earns until the one after.
    """
    ics = []
    for t, day in scores.items():
        xs, ys = [], []
        for s, v in day.items():
            if tradable:
                if t + 2 >= len(calendar):
                    continue
                a, b = opens[s][t + 1], opens[s][t + 2]
            else:
                if t + 1 >= len(calendar):
                    continue
                a, b = closes[s][t], closes[s][t + 1]
            if a and b and v != 0:
                xs.append(v)
                ys.append(b / a - 1)
        if len(xs) >= 5:
            ic = spearman(xs, ys)
            if ic is not None:
                ics.append(ic)
    if len(ics) < 2:
        return {"ic": None, "t": None, "days": len(ics)}
    sd = statistics.pstdev(ics)
    mean = statistics.fmean(ics)
    return {"ic": mean, "t": mean / (sd / math.sqrt(len(ics))) if sd else 0.0, "days": len(ics)}


def evaluate_news(cfg, histories, headlines_by_ticker):
    benchmark = cfg["benchmark"]
    tickers = [t for t in cfg["universe"] if t in histories]
    calendar, opens, closes = align(histories, tickers + [benchmark], benchmark)
    for items in headlines_by_ticker.values():
        for h in items:
            h.scores["lexicon"] = sentiment.score_text(h.title)  # always the current word list
    stamps = [h.published_dt for items in headlines_by_ticker.values() for h in items]
    if not stamps:
        raise ValueError("No historical headlines; run the backfill first")
    begin = (min(stamps) + timedelta(hours=cfg["news"]["lookback_hours"])).astimezone(NY).date().isoformat()
    first = next(i for i, d in enumerate(calendar) if d >= begin)
    last = len(calendar) - 2
    news_cfg = cfg["news"]
    grid = []
    for half_life in (6, 12, 24, 48):
        for opinion_weight in (0.0, 0.25, 1.0):
            sc = daily_scores(headlines_by_ticker, calendar, first, last, half_life,
                              news_cfg["lookback_hours"], opinion_weight)
            grid.append({
                "half_life": half_life, "opinion_weight": opinion_weight,
                "close_to_close": ic_series(sc, calendar, opens, closes, tradable=False),
                "tradable": ic_series(sc, calendar, opens, closes, tradable=True),
            })

    # Trade the live configuration over the period, next to equal weight and SPY.
    sc = daily_scores(headlines_by_ticker, calendar, first, last, news_cfg["half_life_hours"],
                      news_cfg["lookback_hours"], news_cfg.get("opinion_weight", 0.25))

    # How should news and momentum be mixed? (The hybrid account uses news_weight.)
    mom = {}
    for t in sc:
        mom[t] = {}
        for s_ in tickers:
            window = [c for c in closes[s_][max(0, t - 60):t + 1] if c]
            mom[t][s_] = momentum_score(window) if len(window) == 61 else 0.0
    blends = []
    for w in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
        mixed = {t: {s_: w * sc[t].get(s_, 0.0) + (1 - w) * mom[t][s_] for s_ in tickers} for t in sc}
        blends.append({
            "news_weight": w,
            "close_to_close": ic_series(mixed, calendar, opens, closes, tradable=False),
            "tradable": ic_series(mixed, calendar, opens, closes, tradable=True),
        })
    params = cfg["strategies"].get("news", {})
    n = cfg["trading"]["max_positions"]

    def news_rule(t, weights):
        day = sc.get(t)
        if day is None:
            return None
        keep = sorted((s for s in weights if day.get(s, 0) > params.get("exit", 0.0)), key=lambda s: -day[s])
        new = sorted((s for s, v in day.items() if v >= params.get("entry", 0.15) and s not in keep),
                     key=lambda s: -day[s])
        return {s: 1.0 / n for s in (keep + new)[:n]}

    def equal_weight(t, weights):
        return {s: 1.0 / len(tickers) for s in tickers} if not weights else None

    def spy(t, weights):
        return {benchmark: 1.0} if not weights else None

    slip = cfg["trading"]["slippage_bps"]
    cal = calendar[: last + 2]
    trading = {}
    for name, rule in (("News strategy (live settings)", news_rule),
                       ("Equal weight universe (buy & hold)", equal_weight), ("SPY buy & hold", spy)):
        eq, turnover = simulate(cal, opens, closes, rule, first, slip)
        trading[name] = {**stats(eq), "turnover": turnover}
    counts = {t: len(v) for t, v in headlines_by_ticker.items()}
    return {
        "period": (calendar[first], calendar[last]), "days": last - first + 1,
        "headlines": sum(counts.values()), "per_ticker": counts, "grid": grid, "trading": trading,
        "blends": blends,
        "hybrid_weight": cfg["strategies"].get("hybrid", {}).get("news_weight", 0.6),
        "live": (news_cfg["half_life_hours"], news_cfg.get("opinion_weight", 0.25)),
    }


def render_news(res):
    def fmt(x):
        if x["ic"] is None:
            return "–", "–"
        return f"{x['ic']:+.4f}", f"{x['t']:+.1f}"

    a, b = res["period"]
    lines = [
        "# News signal research (GDELT backfill, word-list scorer)",
        "",
        f"{res['headlines']:,} relevant historical headlines from GDELT, {a} to {b} "
        f"({res['days']} trading days). Each day's score uses only headlines published before "
        "5:30pm New York, when the live bot decides. Generated by `python -m papertrader news-research`.",
        "",
        "## Does the score predict the next day?",
        "",
        "Average daily rank IC between the news score and the next day's return, with its t-statistic "
        "(|t| above about 2 is unlikely to be luck). *Close to close* includes the overnight jump the "
        "bot can't trade; *tradable* is open to next open, what a position bought at the open earns.",
        "",
        "| Half-life (h) | Opinion weight | IC close→close | t | IC tradable | t |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for g in res["grid"]:
        live = " (live)" if (g["half_life"], g["opinion_weight"]) == tuple(res["live"]) else ""
        c, ct = fmt(g["close_to_close"])
        tr, tt = fmt(g["tradable"])
        lines.append(f"| {g['half_life']}{live} | {g['opinion_weight']} | {c} | {ct} | {tr} | {tt} |")
    lines += [
        "",
        "## Mixing news with momentum",
        "",
        "Rank IC of `news_weight × news + (1 − news_weight) × momentum` across all stocks. "
        "0 is momentum alone, 1 is news alone.",
        "",
        "| News weight | IC close→close | t | IC tradable | t |",
        "|---:|---:|---:|---:|---:|",
    ]
    for b in res.get("blends", []):
        live = " (hybrid)" if b["news_weight"] == res.get("hybrid_weight") else ""
        c, ct = fmt(b["close_to_close"])
        tr, tt = fmt(b["tradable"])
        lines.append(f"| {b['news_weight']}{live} | {c} | {ct} | {tr} | {tt} |")
    lines += [
        "",
        "## Trading it",
        "",
        "| Portfolio | Return | Sharpe | Max drawdown | Turnover/yr |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, s in res["trading"].items():
        lines.append(f"| {name} | {s['total'] * 100:+.2f}% | {s['sharpe']:.2f} | {s['max_dd'] * 100:.1f}% | "
                     f"{s['turnover']:.1f}x |")
    lines += [
        "",
        "About 60 trading days is a very small sample: a Sharpe ratio over a few months is mostly "
        "noise. Use the IC t-statistics to judge the signal, and the live accounts to judge the bot.",
    ]
    return "\n".join(lines) + "\n"
