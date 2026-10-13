"""The daily run: update accounts, grade yesterday's predictions, read the news, decide."""

import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from . import claude_scorer, predictions, sentiment
from .config import enabled_strategies
from .market import can_decide, drop_unfinished_bar
from .news import NewsArchive, filter_relevant, select_new
from .portfolio import Account, process_new_sessions
from .signals import strategy_scores, target_weights
from .store import TRADE_FIELDS, EQUITY_FIELDS, Store, write_json

log = logging.getLogger(__name__)


def run_daily(cfg, data_dir, fetch_prices, fetch_news, now=None, claude_client=None, use_claude=None):
    """One end-of-day cycle. Returns a summary dict.

    `fetch_prices(symbols) -> ({symbol: History}, failed)` and
    `fetch_news(universe) -> [Headline]` are injected so tests can run offline.
    """
    now = now or datetime.now(timezone.utc)
    store = Store(data_dir)
    archive = NewsArchive(store.news_dir)
    universe = cfg["universe"]
    aliases = {t: cfg.get("aliases", {}).get(t) or [name] for t, name in universe.items()}
    tickers = list(universe)
    benchmark = cfg["benchmark"]
    strategies = enabled_strategies(cfg, claude_available=use_claude)
    summary = {"now": now.isoformat(), "strategies": strategies}

    # 1. Prices.
    histories, failed = fetch_prices(tickers + [benchmark])
    for hist in histories.values():
        drop_unfinished_bar(hist, now)
    if benchmark not in histories or not histories[benchmark].bars:
        raise RuntimeError(f"No price data for the benchmark {benchmark}; aborting the run")
    asof = histories[benchmark].bars[-1].date
    summary.update(asof=asof, price_failures=failed)
    log.info("Latest completed session: %s", asof)

    # 2. Bring every account up to date (fills at the open, marks at the close).
    accounts = store.load_accounts()
    for name in strategies:
        accounts.setdefault(name, Account(name=name, cash=float(cfg["starting_cash"])))
    all_trades, all_equity, stale = [], [], set()
    for acct in accounts.values():
        missing = [s for s in acct.positions if s not in histories]
        if missing:
            # Can't value the account without these prices. Leave it (and its pending
            # order) alone; the next run walks the missed days and catches up.
            log.error("%s: no prices for held %s; skipping this account today", acct.name, missing)
            stale.add(acct.name)
            continue
        trades, rows = process_new_sessions(acct, histories, asof, cfg["trading"])
        all_trades += trades
        all_equity += rows
    summary["trades"] = len(all_trades)
    summary["stale_accounts"] = sorted(stale)

    # 3. Grade predictions whose next close is now known.
    pred_rows = store.read_rows(store.predictions_path)
    summary["graded"] = predictions.grade(pred_rows, histories)

    # 4. News: fetch, drop off-topic and junk, keep only new headlines, score them once,
    # archive them.
    news_cfg = cfg["news"]
    since = now - timedelta(hours=news_cfg["lookback_hours"])
    relevant, kinds = filter_relevant(fetch_news(aliases), aliases)
    fresh = select_new(
        relevant, archive.known_ids(since), now,
        news_cfg["lookback_hours"], news_cfg["max_new_headlines_per_ticker"],
    )
    summary["headline_kinds"] = kinds
    for h in fresh:
        h.scores["lexicon"] = round(sentiment.score_text(h.title), 4)
    if "claude" in strategies and fresh:
        params = cfg["strategies"]["claude"]
        n = claude_scorer.score_headlines(
            fresh, universe, params.get("model", "claude-opus-5-5"), params.get("effort", "low"),
            client=claude_client,
        )
        log.info("Claude scored %d of %d new headlines", n, len(fresh))
    summary["new_headlines"] = len(fresh)
    by_ticker = defaultdict(list)
    archived, _ = filter_relevant(archive.load(since), aliases)
    for h in archived + fresh:
        by_ticker[h.ticker].append(h)

    # 5. Decide, unless the next session has already opened (that would be look-ahead).
    if not can_decide(asof, now):
        log.warning("Market has opened since the %s close; not placing new orders", asof)
        summary["decided"] = False
    else:
        signals = {"asof": asof, "decided_at": now.isoformat(), "strategies": {}}
        new_preds = []
        tradable = [t for t in tickers if t in histories and histories[t].bar_on(asof)]
        for name in strategies:
            acct = accounts[name]
            if name == "benchmark":
                targets = {benchmark: 1.0}
                scores = {}
            elif name == "equal_weight":
                targets = {t: 1.0 / len(tradable) for t in tradable}
                scores = {}
            else:
                params = cfg["strategies"][name]
                scores = strategy_scores(name, params, tradable, histories, by_ticker, asof, now, news_cfg)
                targets = target_weights(
                    scores, acct.positions, params.get("entry", 0.15), params.get("exit", 0.0),
                    cfg["trading"]["max_positions"],
                )
                new_preds += predictions.make_predictions(
                    asof, name, scores, histories, cfg["predictions"]["min_abs_score"]
                )
            if name not in stale:
                acct.pending = {"decided_on": asof, "decided_at": now.isoformat(), "targets": targets}
            signals["strategies"][name] = {
                "targets": targets,
                "scores": {t: round(s, 4) for t, s in sorted(scores.items(), key=lambda kv: -kv[1])},
            }
        signals["headlines"] = _top_headlines(by_ticker, now)
        pred_rows = predictions.merge(pred_rows, new_preds)
        summary["decided"] = True

    # 6. Save. Everything is written here, at the end, so a run that fails part way
    # leaves the data folder untouched and the next run simply redoes the work.
    archive.append(fresh, now.date().isoformat())
    store.append_rows(store.trades_path, TRADE_FIELDS, all_trades)
    store.append_rows(store.equity_path, EQUITY_FIELDS, all_equity)
    store.write_rows(store.predictions_path, predictions.FIELDS, pred_rows)
    if summary["decided"]:
        write_json(store.signals_path, signals)
    store.save_accounts(accounts)
    return summary


def _top_headlines(by_ticker, now, per_ticker=5):
    """Most recent scored headlines per ticker, for the report."""
    out = {}
    for ticker, items in sorted(by_ticker.items()):
        items = sorted(items, key=lambda h: h.published, reverse=True)[:per_ticker]
        out[ticker] = [
            {
                "title": h.title, "source": h.source, "url": h.url, "published": h.published,
                "scores": h.scores, "reasons": h.reasons,
            }
            for h in items
        ]
    return out
