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

from . import finbert_scorer, sentiment
from .market import NY
from .news import Headline, filter_relevant, headline_id
from .predictions import spearman
from .research import align, simulate, stats
from .signals import momentum_score, news_score

log = logging.getLogger(__name__)

GDELT_DOC = "https://api.gdeltproject.org/api/v2/doc/doc"
REQUEST_GAP = 6  # GDELT asks for no more than one request every 5 seconds
# GitHub's runners share IP addresses, so GDELT often rate-limits even a slow
# client; back off for longer before retrying.
RATE_LIMIT_WAIT = 20


def gdelt_query(names):
    """GDELT search for any of a company's names in stock-related English news.

    GDELT rejects quoted phrases shorter than 5 characters ("Meta", "AMD"), so
    those become "Meta stock" / "Meta shares", and it only allows parentheses
    around OR'd terms, so a single term goes without them.
    """
    terms = []
    for n in names:
        if len(n) >= 5:
            terms.append(f'"{n}"')
        else:
            terms += [f'"{n} stock"', f'"{n} shares"']
    terms = list(dict.fromkeys(terms))
    core = terms[0] if len(terms) == 1 else "(" + " OR ".join(terms) + ")"
    return f"{core} (stock OR shares) sourcelang:english"


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


class GdeltError(RuntimeError):
    pass


def fetch_window(session, ticker, names, start, end, tries=3):
    """Headlines for one ticker and time window. Returns (headlines, status).

    status is "ok", "rate_limited" (GDELT said to slow down; worth retrying
    later) or "error" (anything else).
    """
    params = {
        "query": gdelt_query(names), "mode": "ArtList", "format": "json", "maxrecords": 250,
        "sort": "HybridRel",
        "startdatetime": start.strftime("%Y%m%d%H%M%S"), "enddatetime": end.strftime("%Y%m%d%H%M%S"),
    }
    status = "error"
    for attempt in range(tries):
        t0 = time.monotonic()
        try:
            resp = session.get(GDELT_DOC, params=params, timeout=30)
            text = resp.text.strip()
            if resp.status_code == 429 or "limit requests" in text[:300].lower():
                status = "rate_limited"
                log.info("GDELT rate limit for %s %s (%.1fs); waiting", ticker, start.date(),
                         time.monotonic() - t0)
                time.sleep(RATE_LIMIT_WAIT * (attempt + 1))
                continue
            resp.raise_for_status()
            if text and not text.startswith("{"):
                # A query GDELT refuses (bad syntax) won't work on retry.
                log.warning("GDELT refused the query for %s: %r", ticker, text[:120])
                return [], "error"
            items = parse_gdelt(json.loads(text) if text else {}, ticker)
            log.info("GDELT %s %s..%s: %d articles in %.1fs", ticker, start.date(), end.date(),
                     len(items), time.monotonic() - t0)
            return items, "ok"
        except (requests.RequestException, ValueError) as e:
            status = "error"
            log.warning("GDELT %s %s failed after %.1fs: %s", ticker, start.date(), time.monotonic() - t0, e)
            time.sleep(REQUEST_GAP)
    return [], status


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


def windows(now, days, window_days):
    """Fixed calendar windows (UTC midnight to midnight) covering the last `days` days.

    Boundaries don't depend on the time of day, so a later run can tell which
    windows an earlier run already fetched. Newest first.
    """
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    today = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    # Anchor windows to multiples of window_days since 1970 so they line up across
    # runs on different days and with different `days`.
    offset = ((today - timedelta(days=days)) - epoch).days // window_days * window_days
    out = []
    start = epoch + timedelta(days=offset)
    while start < now:
        out.append((start, min(start + timedelta(days=window_days), now)))
        start += timedelta(days=window_days)
    return out[::-1]


def backfill(cfg, directory, days=90, window_days=14, session=None, now=None, max_minutes=None,
             clock=time.monotonic):
    """Fetch and score ~`days` of GDELT headlines for every ticker, resumably.

    Each finished window is saved at once and recorded in progress.json, so a
    run that stops (time limit, error) loses nothing and the next run carries
    on. Stops cleanly after `max_minutes`. Raises GdeltError if GDELT doesn't
    answer at all. Returns {"counts": {ticker: saved}, "complete": bool}.
    """
    session = session or requests.Session()
    session.headers.setdefault("User-Agent", "stock-paper-trader research (github.com)")
    now = now or datetime.now(timezone.utc)
    store = HistoryStore(directory)
    progress_path = Path(directory) / "progress.json"
    done = json.loads(progress_path.read_text()) if progress_path.exists() else {}
    deadline = clock() + max_minutes * 60 if max_minutes else None
    attempts = errors = 0
    complete = True
    closed = [(a, b) for a, b in windows(now, days, window_days) if b - a >= timedelta(days=window_days)]
    if all(a.date().isoformat() in done.get(t, []) for t in cfg["aliases"] for a, _ in closed):
        log.info("Backfill already complete; nothing to fetch")
        return {"counts": {t: len(store.load(t)) for t in cfg["aliases"]}, "complete": True}
    for ticker, names in cfg["aliases"].items():
        finished = set(done.get(ticker, []))
        for start, end in windows(now, days, window_days):
            key = start.date().isoformat()
            if key in finished:
                continue
            if deadline and clock() > deadline:
                complete = False
                break
            found, status = fetch_window(session, ticker, names, start, end)
            attempts += 1
            errors += status == "error"
            if attempts >= 5 and errors == attempts:
                raise GdeltError("GDELT failed the first 5 requests (not rate limits); giving up")
            time.sleep(REQUEST_GAP)
            if status != "ok":
                complete = False
                continue
            kept, _ = filter_relevant(found, {ticker: names})
            for h in kept:
                h.scores["lexicon"] = round(sentiment.score_text(h.title), 4)
            if kept and finbert_scorer.available():
                finbert_scorer.score_headlines(kept)
            store.save(ticker, store.load(ticker) + kept)
            if end - start >= timedelta(days=window_days):  # the newest window may still grow
                finished.add(key)
                done[ticker] = sorted(finished)
                progress_path.write_text(json.dumps(done, indent=1, sort_keys=True) + "\n")
        if not complete and deadline and clock() > deadline:
            break
    counts = {t: len(store.load(t)) for t in cfg["aliases"]}
    log.info("Saved headlines per ticker: %s", counts)
    return {"counts": counts, "complete": complete}


# ------------------------------------------------------------------ evaluation


def decision_time(day, hour=17, minute=30):
    """When the live bot decides: 5:30pm New York on `day`."""
    d = datetime.fromisoformat(day).date()
    return datetime.combine(d, dtime(hour, minute), NY).astimezone(timezone.utc)


def daily_scores(headlines_by_ticker, calendar, first, last, half_life, lookback, opinion_weight,
                 scorer="lexicon"):
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
            day[ticker] = news_score(window, scorer, now, half_life, lookback, opinion_weight=opinion_weight)
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


def add_missing_finbert(store, tickers):
    """Score saved history with FinBERT where it's missing (free), and save. Returns count."""
    if not finbert_scorer.available():
        return 0
    total = 0
    for t in tickers:
        items = store.load(t)
        todo = [h for h in items if finbert_scorer.SCORER not in h.scores]
        if todo:
            total += finbert_scorer.score_headlines(todo)
            store.save(t, items)
    return total


SCORERS = ("lexicon", "finbert", "claude")


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
    scorers = [sc for sc in SCORERS
               if any(sc in h.scores for items in headlines_by_ticker.values() for h in items)]
    begin = (min(stamps) + timedelta(hours=cfg["news"]["lookback_hours"])).astimezone(NY).date().isoformat()
    first = next(i for i, d in enumerate(calendar) if d >= begin)
    last = len(calendar) - 2
    news_cfg = cfg["news"]
    live = (news_cfg["half_life_hours"], news_cfg.get("opinion_weight", 0.25))

    def ics(day_scores):
        return {
            "close_to_close": ic_series(day_scores, calendar, opens, closes, tradable=False),
            "tradable": ic_series(day_scores, calendar, opens, closes, tradable=True),
        }

    grid = []
    for half_life in (6, 12, 24, 48):
        for opinion_weight in (0.0, 0.25, 1.0):
            row = {"half_life": half_life, "opinion_weight": opinion_weight}
            for sc_name in scorers:
                row[sc_name] = ics(daily_scores(headlines_by_ticker, calendar, first, last, half_life,
                                                news_cfg["lookback_hours"], opinion_weight, sc_name))
            grid.append(row)

    live_scores = {
        sc_name: daily_scores(headlines_by_ticker, calendar, first, last, live[0],
                              news_cfg["lookback_hours"], live[1], sc_name)
        for sc_name in scorers
    }

    # How should news and momentum be mixed? (The hybrid account uses news_weight.)
    mom = {}
    for t in range(first, last + 1):
        mom[t] = {}
        for s_ in tickers:
            window = [c for c in closes[s_][max(0, t - 60):t + 1] if c]
            mom[t][s_] = momentum_score(window) if len(window) == 61 else 0.0
    blends = []
    for w in (0.0, 0.25, 0.5, 0.6, 0.75, 1.0):
        row = {"news_weight": w}
        for sc_name in scorers:
            sc = live_scores[sc_name]
            row[sc_name] = ics({t: {s_: w * sc[t].get(s_, 0.0) + (1 - w) * mom[t][s_] for s_ in tickers}
                                for t in sc})
        blends.append(row)

    # Trade each reader with the live rule, next to equal weight and SPY.
    params = cfg["strategies"].get("news", {})
    n = cfg["trading"]["max_positions"]

    def news_rule(sc):
        def decide(t, weights):
            day = sc.get(t)
            if day is None:
                return None
            keep = sorted((s_ for s_ in weights if day.get(s_, 0) > params.get("exit", 0.0)),
                          key=lambda s_: -day[s_])
            new = sorted((s_ for s_, v in day.items() if v >= params.get("entry", 0.15) and s_ not in keep),
                         key=lambda s_: -day[s_])
            return {s_: 1.0 / n for s_ in (keep + new)[:n]}
        return decide

    def equal_weight(t, weights):
        return {s_: 1.0 / len(tickers) for s_ in tickers} if not weights else None

    def spy(t, weights):
        return {benchmark: 1.0} if not weights else None

    rules = [(f"News strategy, {sc_name}", news_rule(live_scores[sc_name])) for sc_name in scorers]
    rules += [("Equal weight universe (buy & hold)", equal_weight), ("SPY buy & hold", spy)]
    cal = calendar[: last + 2]
    trading = {}
    for name, rule in rules:
        eq, turnover = simulate(cal, opens, closes, rule, first, cfg["trading"]["slippage_bps"])
        trading[name] = {**stats(eq), "turnover": turnover}
    counts = {t: len(v) for t, v in headlines_by_ticker.items()}
    return {
        "period": (calendar[first], calendar[last]), "days": last - first + 1,
        "headlines": sum(counts.values()), "per_ticker": counts, "scorers": scorers,
        "grid": grid, "blends": blends, "trading": trading, "live": live,
        "hybrid_weight": cfg["strategies"].get("hybrid", {}).get("news_weight", 0.6),
    }


def render_news(res):
    def cell(x):
        if x["ic"] is None:
            return "–"
        return f"{x['ic']:+.4f} ({x['t']:+.1f})"

    scorers = res["scorers"]
    a, b = res["period"]
    lines = [
        "# News signal research (GDELT backfill)",
        "",
        f"{res['headlines']:,} relevant historical headlines from GDELT, {a} to {b} "
        f"({res['days']} trading days), scored by: {', '.join(scorers)}. Each day's score uses only "
        "headlines published before 5:30pm New York, when the live bot decides. "
        "Generated by `python -m papertrader news-research`.",
        "",
        "Each cell is the average daily **rank IC** between the news score and the next day's return, "
        "with its t-statistic in brackets (|t| above about 2 is unlikely to be luck). *Close→close* "
        "includes the overnight jump the bot can't trade; *tradable* is open to next open, what a "
        "position bought at the open actually earns.",
        "",
        "## Which reader predicts best? (live settings)",
        "",
        "| Scorer | IC close→close | IC tradable |",
        "|---|---:|---:|",
    ]
    live_row = next(g for g in res["grid"] if (g["half_life"], g["opinion_weight"]) == tuple(res["live"]))
    for sc in scorers:
        lines.append(f"| {sc} | {cell(live_row[sc]['close_to_close'])} | {cell(live_row[sc]['tradable'])} |")
    lines += [
        "",
        "## Settings: half-life and opinion weight (tradable IC)",
        "",
        "| Half-life (h) | Opinion weight | " + " | ".join(scorers) + " |",
        "|---:|---:|" + "---:|" * len(scorers),
    ]
    for g in res["grid"]:
        live = " (live)" if (g["half_life"], g["opinion_weight"]) == tuple(res["live"]) else ""
        lines.append(f"| {g['half_life']}{live} | {g['opinion_weight']} | "
                     + " | ".join(cell(g[sc]["tradable"]) for sc in scorers) + " |")
    lines += [
        "",
        "## Mixing news with momentum (tradable IC)",
        "",
        "`news_weight × news + (1 − news_weight) × momentum`; 0 is momentum alone, 1 is news alone.",
        "",
        "| News weight | " + " | ".join(scorers) + " |",
        "|---:|" + "---:|" * len(scorers),
    ]
    for r in res["blends"]:
        live = " (hybrid)" if r["news_weight"] == res.get("hybrid_weight") else ""
        lines.append(f"| {r['news_weight']}{live} | " + " | ".join(cell(r[sc]["tradable"]) for sc in scorers) + " |")
    lines += [
        "",
        "## Trading it",
        "",
        "| Portfolio | Return | Sharpe | Max drawdown | Turnover/yr |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, st in res["trading"].items():
        lines.append(f"| {name} | {st['total'] * 100:+.2f}% | {st['sharpe']:.2f} | {st['max_dd'] * 100:.1f}% | "
                     f"{st['turnover']:.1f}x |")
    lines += [
        "",
        "About 60 trading days is a small sample: a Sharpe ratio over a few months is mostly noise. "
        "Use the IC t-statistics to judge the signal, and the live accounts to judge the bot.",
    ]
    return "\n".join(lines) + "\n"
