"""Replay the price-only strategies over past data with the same account rules.

News strategies can't be backtested from scratch: free RSS feeds only return
recent headlines, and testing a news model on headlines picked today would leak
the future. They are judged by the live paper accounts instead, and the news
archive the daily run builds will make replaying them possible later.
"""

from .portfolio import Account, process_new_sessions
from .predictions import grade, make_predictions, summarize
from .report import max_drawdown
from .signals import momentum_score, target_weights

PRICE_ONLY = ("momentum", "benchmark")
WARMUP = 61


def run_backtest(cfg, histories, strategies=PRICE_ONLY):
    """Returns {strategy: result dict} for the given price-only strategies."""
    benchmark = cfg["benchmark"]
    tickers = [t for t in cfg["universe"] if t in histories]
    calendar = [b.date for b in histories[benchmark].bars]
    if len(calendar) <= WARMUP + 1:
        raise ValueError("Not enough price history to backtest")
    closes = {t: {b.date: b.close for b in histories[t].bars} for t in tickers}
    ordered = {t: [b.date for b in histories[t].bars] for t in tickers}
    index = {t: {d: i for i, d in enumerate(ordered[t])} for t in tickers}

    results = {}
    for name in strategies:
        acct = Account(name=name, cash=float(cfg["starting_cash"]))
        # Prices are already split-adjusted end to end, so splits must not rescale shares.
        acct.seen_splits = [f"{s}:{x['date']}" for s, h in histories.items() for x in h.splits]
        params = cfg["strategies"].get(name, {})
        equity, trades, preds = [], [], []
        for day in calendar[WARMUP:]:
            t, rows = process_new_sessions(acct, histories, day, cfg["trading"])
            trades += t
            equity += rows
            if day == calendar[-1]:
                break
            if name == "benchmark":
                targets = {benchmark: 1.0}
            else:
                scores = {}
                for tk in tickers:
                    i = index[tk].get(day)
                    if i is not None and i >= 60:
                        scores[tk] = momentum_score([closes[tk][d] for d in ordered[tk][i - 60:i + 1]])
                targets = target_weights(
                    scores, acct.positions, params.get("entry", 0.25), params.get("exit", 0.0),
                    cfg["trading"]["max_positions"],
                )
                preds += make_predictions(day, name, scores, histories, cfg["predictions"]["min_abs_score"])
            acct.pending = {"decided_on": day, "decided_at": day, "targets": targets}
        grade(preds, histories)
        values = [r["equity"] for r in equity]
        results[name] = {
            "start": equity[0]["date"],
            "end": equity[-1]["date"],
            "equity": values[-1],
            "return": values[-1] / float(cfg["starting_cash"]) - 1,
            "max_drawdown": max_drawdown(values),
            "trades": len(trades),
            "stats": summarize(preds, name) if preds else {},
            "curve": [(r["date"], r["equity"]) for r in equity],
        }
    return results

