"""Fast walk-forward backtests of price-only strategy variants.

The daily bot's Account code is exact but slow (it re-walks the calendar every
day). This module simulates the same trading rules (decide after the close,
trade at the next open, pay slippage on turnover) on aligned price arrays, so
a decade of data for a dozen variants runs in seconds.

Every variant is scored on two halves of the history separately. Picking the
best variant on the first half and checking it on the second half is the
minimum defence against fooling ourselves: with enough variants, something
always looks great in hindsight.

Two benchmarks matter here:
  * SPY buy-and-hold, what the live report compares against;
  * equal weight across the universe. The universe is today's biggest
    companies, picked with hindsight, so any long-only strategy on it beats SPY
    in a backtest. A variant is only interesting if it beats this one.
"""

import math
import statistics

from .signals import momentum_score

TRADING_DAYS = 252


def align(histories, symbols, benchmark):
    """Opens and closes on the benchmark's calendar. Missing days carry None."""
    calendar = [b.date for b in histories[benchmark].bars]
    opens, closes = {}, {}
    for sym in symbols:
        if sym not in histories:
            continue
        by_date = {b.date: b for b in histories[sym].bars}
        opens[sym] = [by_date[d].open if d in by_date else None for d in calendar]
        closes[sym] = [by_date[d].close if d in by_date else None for d in calendar]
    return calendar, opens, closes


def simulate(calendar, opens, closes, decide, start, slippage_bps=5.0):
    """Run one strategy from calendar index `start`.

    `decide(t, weights)` is called after the close on day t with the current
    weights and returns new target weights (or None to keep the current ones).
    Targets are traded at the open of day t+1. Returns daily equity (starting
    at 1.0 on day `start`) and the average one-way turnover per year.
    """
    slip = slippage_bps / 10_000
    equity = [1.0]
    weights = {}
    turnover = 0.0
    pending = decide(start, {})
    for t in range(start + 1, len(calendar)):
        value = equity[-1]
        # Overnight: positions held from the previous close to today's open.
        grow = 0.0
        held = 0.0
        for s, w in weights.items():
            prev_c, o = closes[s][t - 1], opens[s][t]
            r = o / prev_c if prev_c and o else 1.0
            grow += w * r
            held += w
        value_open = value * (grow + (1 - held))
        if value_open > 0 and weights:
            weights = {s: w * value * (opens[s][t] / closes[s][t - 1] if closes[s][t - 1] and opens[s][t] else 1.0)
                       / value_open for s, w in weights.items()}
        # Trade at the open.
        if pending is not None:
            pending = {s: w for s, w in pending.items() if opens.get(s) and opens[s][t]}
            traded = sum(abs(pending.get(s, 0.0) - weights.get(s, 0.0)) for s in set(pending) | set(weights))
            value_open *= 1 - slip * traded
            turnover += traded / 2
            weights = {s: w for s, w in pending.items() if w > 0}
        # Intraday: open to close.
        grow = 0.0
        held = 0.0
        for s, w in weights.items():
            o, c = opens[s][t], closes[s][t]
            r = c / o if o and c else 1.0
            grow += w * r
            held += w
        value_close = value_open * (grow + (1 - held))
        if value_close > 0 and weights:
            weights = {s: w * value_open * (closes[s][t] / opens[s][t] if opens[s][t] and closes[s][t] else 1.0)
                       / value_close for s, w in weights.items()}
        equity.append(value_close)
        pending = decide(t, dict(weights)) if t < len(calendar) - 1 else None
    years = max((len(calendar) - start - 1) / TRADING_DAYS, 1e-9)
    return equity, turnover / years


def stats(equity):
    """CAGR, annualized volatility, Sharpe (zero risk-free rate) and max drawdown."""
    if len(equity) < 2:
        return {}
    rets = [equity[i] / equity[i - 1] - 1 for i in range(1, len(equity))]
    years = len(rets) / TRADING_DAYS
    cagr = equity[-1] ** (1 / years) - 1 if equity[-1] > 0 else -1.0
    vol = statistics.pstdev(rets) * math.sqrt(TRADING_DAYS)
    mean = statistics.fmean(rets) * TRADING_DAYS
    peak, mdd = equity[0], 0.0
    for v in equity:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    return {"cagr": cagr, "vol": vol, "sharpe": mean / vol if vol else 0.0, "max_dd": mdd,
            "total": equity[-1] / equity[0] - 1}


# ---------------------------------------------------------------- strategies


def _ret(closes, s, t, back):
    a, b = closes[s][t - back] if t - back >= 0 else None, closes[s][t]
    return b / a - 1 if a and b else None


def top_n(scores, n):
    best = sorted((s for s, v in scores.items() if v is not None), key=lambda s: -scores[s])[:n]
    return {s: 1.0 / n for s in best}


def every(k, start, fn):
    """Only rebalance every k trading days (counting from `start`)."""
    def decide(t, weights):
        return fn(t, weights) if (t - start) % k == 0 else None
    return decide


def make_variants(calendar, closes, tickers, benchmark, start, n=5):
    """Name -> decide(t, weights). All long only, equal weight per slot."""

    def momentum_live(entry=0.25, exit_=0.0):
        # The live bot's rule: vol-scaled 20/60-day trend, entry/exit hysteresis, daily.
        def decide(t, weights):
            scores = {}
            for s in tickers:
                window = [c for c in closes[s][max(0, t - 60):t + 1] if c]
                scores[s] = momentum_score(window) if len(window) == 61 else 0.0
            keep = sorted((s for s in weights if scores.get(s, 0) > exit_), key=lambda s: -scores[s])
            new = sorted((s for s in tickers if scores[s] >= entry and s not in keep), key=lambda s: -scores[s])
            return {s: 1.0 / n for s in (keep + new)[:n]}
        return decide

    def cross_momentum(lookback, skip):
        def decide(t, weights):
            scores = {}
            for s in tickers:
                a = closes[s][t - lookback] if t - lookback >= 0 else None
                b = closes[s][t - skip] if t - skip >= 0 else None
                scores[s] = b / a - 1 if a and b else None
            return top_n(scores, n)
        return decide

    def reversal(days):
        def decide(t, weights):
            scores = {}
            for s in tickers:
                r = _ret(closes, s, t, days)
                scores[s] = -r if r is not None else None
            return top_n(scores, n)
        return decide

    def low_vol(days):
        def decide(t, weights):
            scores = {}
            for s in tickers:
                window = [c for c in closes[s][max(0, t - days):t + 1] if c]
                if len(window) < days:
                    scores[s] = None
                    continue
                rets = [window[i] / window[i - 1] - 1 for i in range(1, len(window))]
                scores[s] = -statistics.pstdev(rets)
            return top_n(scores, n)
        return decide

    def equal_weight(t, weights):
        live = [s for s in tickers if closes[s][t]]
        return {s: 1.0 / len(live) for s in live}

    def spy_hold(t, weights):
        return {benchmark: 1.0} if not weights else None

    def spy_trend(t, weights):
        window = [c for c in closes[benchmark][max(0, t - 199):t + 1] if c]
        if len(window) < 200:
            return {}
        return {benchmark: 1.0} if window[-1] > statistics.fmean(window) else {}

    def momentum_trend(lookback, skip):
        # 12-1 momentum, but only while SPY is above its 200-day average.
        mom = cross_momentum(lookback, skip)

        def decide(t, weights):
            return mom(t, weights) if spy_trend(t, weights) else {}
        return decide

    monthly, weekly = 21, 5
    return {
        "SPY buy & hold": spy_hold,
        "Equal weight universe (monthly)": every(monthly, start, equal_weight),
        "Live momentum rule (daily)": momentum_live(),
        "Live momentum rule, weekly": every(weekly, start, momentum_live()),
        "12-1 month momentum, top 5 (monthly)": every(monthly, start, cross_momentum(252, 21)),
        "6-1 month momentum, top 5 (monthly)": every(monthly, start, cross_momentum(126, 21)),
        "3-month momentum, top 5 (monthly)": every(monthly, start, cross_momentum(63, 0)),
        "12-1 momentum + SPY trend filter (monthly)": every(monthly, start, momentum_trend(252, 21)),
        "1-week reversal, top 5 (weekly)": every(weekly, start, reversal(5)),
        "1-month reversal, top 5 (monthly)": every(monthly, start, reversal(21)),
        "Low volatility, top 5 (monthly)": every(monthly, start, low_vol(60)),
        "SPY with 200-day trend filter (daily)": spy_trend,
    }


def next_day_ic(calendar, closes, tickers, start):
    """Average daily rank correlation between the live momentum score and the next day's return."""
    from .predictions import spearman

    ics = []
    for t in range(start, len(calendar) - 1):
        xs, ys = [], []
        for s in tickers:
            window = [c for c in closes[s][max(0, t - 60):t + 1] if c]
            nxt = _ret(closes, s, t + 1, 1)
            if len(window) == 61 and nxt is not None:
                xs.append(momentum_score(window))
                ys.append(nxt)
        if len(xs) >= 5:
            ic = spearman(xs, ys)
            if ic is not None:
                ics.append(ic)
    if not ics:
        return None
    mean = statistics.fmean(ics)
    t_stat = mean / (statistics.pstdev(ics) / math.sqrt(len(ics))) if len(ics) > 1 and statistics.pstdev(ics) else 0.0
    return {"ic": mean, "t": t_stat, "days": len(ics)}


def run_research(cfg, histories, slippage_bps=None):
    """Walk-forward comparison: every variant on the first half and the second half."""
    benchmark = cfg["benchmark"]
    tickers = [t for t in cfg["universe"] if t in histories]
    calendar, opens, closes = align(histories, tickers + [benchmark], benchmark)
    warmup = 253  # 12-1 momentum needs a year of history
    if len(calendar) < warmup + 2 * 126:
        raise ValueError("Need at least two years of history for research")
    mid = warmup + (len(calendar) - warmup) // 2
    slippage = cfg["trading"]["slippage_bps"] if slippage_bps is None else slippage_bps
    halves = {"first": (warmup, mid), "second": (mid, len(calendar) - 1)}
    results = {}
    for half, (a, b) in halves.items():
        cal = calendar[: b + 1]
        variants = make_variants(cal, closes, tickers, benchmark, a, cfg["trading"]["max_positions"])
        for name, decide in variants.items():
            eq, turnover = simulate(cal, opens, closes, decide, a, slippage)
            results.setdefault(name, {})[half] = {**stats(eq), "turnover": turnover}
    ic = next_day_ic(calendar, closes, tickers, warmup)
    return {
        "periods": {h: (calendar[a], calendar[b]) for h, (a, b) in halves.items()},
        "tickers": tickers,
        "results": results,
        "momentum_ic": ic,
        "slippage_bps": slippage,
    }


def render(res):
    p = res["periods"]
    lines = [
        "# Strategy research (price-only, walk-forward)",
        "",
        f"Universe: {len(res['tickers'])} stocks from `config.json`. Trades at the next open with "
        f"{res['slippage_bps']} bp slippage. Long only, price returns (no dividends). "
        "Generated by `python -m papertrader research`.",
        "",
        f"- **First half** (pick variants here): {p['first'][0]} to {p['first'][1]}",
        f"- **Second half** (check them here): {p['second'][0]} to {p['second'][1]}",
        "",
        "| Variant | CAGR 1st | Sharpe 1st | CAGR 2nd | Sharpe 2nd | Max DD 2nd | Turnover/yr |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    order = sorted(res["results"], key=lambda n: -res["results"][n]["first"].get("sharpe", -9))
    for name in order:
        a, b = res["results"][name]["first"], res["results"][name]["second"]
        lines.append(
            f"| {name} | {a['cagr'] * 100:+.1f}% | {a['sharpe']:.2f} | {b['cagr'] * 100:+.1f}% | "
            f"{b['sharpe']:.2f} | {b['max_dd'] * 100:.1f}% | {b['turnover']:.1f}x |"
        )
    ic = res.get("momentum_ic")
    lines += [
        "",
        "Rows are sorted by first-half Sharpe ratio, i.e. the order you'd have picked them in. "
        "What matters is whether that order survives into the second half. *Turnover/yr*: how "
        "many times a year the whole portfolio is replaced (each full turn costs about 2x slippage).",
        "",
        "**Hindsight warning:** the universe is today's largest companies, so a long-only strategy "
        "on it beats SPY in any backtest. Compare variants with the *equal weight universe* row, "
        "not with SPY.",
    ]
    if ic:
        lines += [
            "",
            f"**Does the live momentum score predict the next day?** Average daily rank IC "
            f"{ic['ic']:+.4f} over {ic['days']} days (t = {ic['t']:+.1f}). "
            + ("That is statistically indistinguishable from zero: daily calls from this score are a coin flip."
               if abs(ic["t"]) < 2 else "That is statistically different from zero."),
        ]
    return "\n".join(lines) + "\n"
