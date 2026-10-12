"""Log every prediction, grade it once the next close is known, and summarize accuracy.

A prediction is made after the close on day D: "this stock's close on the next
trading day will be above (call +1) or below (call -1) today's close". Scores
too close to 0 are logged with call 0 (no call) and don't count toward the
hit rate.
"""

import math
import statistics
from collections import defaultdict

FIELDS = ["date", "strategy", "symbol", "score", "call", "close", "next_date", "next_close", "ret", "correct"]


def make_predictions(asof, strategy, scores, histories, min_abs_score):
    rows = []
    for sym, score in sorted(scores.items()):
        bar = histories[sym].bar_on(asof) if sym in histories else None
        if bar is None:
            continue
        call = 0 if abs(score) < min_abs_score else (1 if score > 0 else -1)
        rows.append({
            "date": asof, "strategy": strategy, "symbol": sym, "score": round(score, 4),
            "call": call, "close": round(bar.close, 4),
            "next_date": "", "next_close": "", "ret": "", "correct": "",
        })
    return rows


def merge(existing, new_rows):
    """Add new rows; a re-run for the same day and strategy replaces the earlier rows."""
    replaced = {(r["date"], r["strategy"]) for r in new_rows}
    kept = [r for r in existing if (r["date"], r["strategy"]) not in replaced]
    return kept + new_rows


def grade(rows, histories):
    """Fill in the outcome for every prediction whose next close is now known."""
    graded = 0
    for r in rows:
        if r["next_date"] or r["symbol"] not in histories:
            continue
        bar = histories[r["symbol"]].first_bar_after(r["date"])
        if bar is None:
            continue
        ret = bar.close / float(r["close"]) - 1
        call = int(r["call"])
        r["next_date"], r["next_close"], r["ret"] = bar.date, round(bar.close, 4), round(ret, 6)
        r["correct"] = "" if call == 0 else int(call * ret > 0)
        graded += 1
    return graded


def _ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2
        i = j + 1
    return ranks


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    rx, ry = _ranks(xs), _ranks(ys)
    if len(set(rx)) < 2 or len(set(ry)) < 2:
        return None
    return statistics.correlation(rx, ry)


def summarize(rows, strategy):
    """Accuracy stats for one strategy over all graded predictions."""
    graded = [r for r in rows if r["strategy"] == strategy and r["next_date"]]
    calls = [r for r in graded if int(r["call"]) != 0]
    n = len(calls)
    out = {"strategy": strategy, "graded": len(graded), "calls": n}
    if n:
        hits = sum(int(r["correct"]) for r in calls)
        p = hits / n
        out["hit_rate"] = p
        out["ci95"] = 1.96 * math.sqrt(p * (1 - p) / n) if 0 < p < 1 else 1.96 * math.sqrt(0.25 / n)
        # Baseline: the hit rate of always calling whichever direction these stocks moved
        # more often on these days (in hindsight), never less than a coin flip.
        ups = sum(1 for r in calls if float(r["ret"]) > 0)
        p0 = min(max(0.5, ups / n, 1 - ups / n), 0.99)
        out["base_rate"] = p0
        # Two-sided p-value against that baseline (normal approximation). Calls made on the
        # same day move together, so this overstates significance; the report also waits
        # for enough trading days before giving a verdict.
        z = (hits - n * p0) / math.sqrt(n * p0 * (1 - p0))
        out["p_value"] = math.erfc(abs(z) / math.sqrt(2))
        out["days"] = len({r["date"] for r in calls})
        out["edge_bps"] = statistics.fmean(int(r["call"]) * float(r["ret"]) for r in calls) * 10_000
        out["longs"] = sum(1 for r in calls if int(r["call"]) > 0)
    by_day = defaultdict(list)
    for r in graded:
        by_day[r["date"]].append((float(r["score"]), float(r["ret"])))
    ics = []
    for pairs in by_day.values():
        if len(pairs) >= 5:
            ic = spearman([s for s, _ in pairs], [x for _, x in pairs])
            if ic is not None:
                ics.append(ic)
    if ics:
        out["ic"] = statistics.fmean(ics)
        out["ic_days"] = len(ics)
    return out
