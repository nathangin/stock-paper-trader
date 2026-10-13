"""Turn prices and headlines into per-ticker scores, and scores into target portfolios.

Every strategy produces a score in [-1, 1] for each ticker. A positive score is
a prediction that the stock goes up over the next trading day, a negative score
that it goes down. The trading rule is the same for every strategy, so the
strategies differ only in how they score.
"""

import math
import statistics
from datetime import timedelta


def momentum_score(closes):
    """Trend strength from 20- and 60-day returns, scaled by the stock's own volatility.

    Needs 61 closes. Returns 0 when there is not enough history.
    """
    if len(closes) < 61:
        return 0.0
    rets = [closes[i] / closes[i - 1] - 1 for i in range(len(closes) - 60, len(closes))]
    vol = statistics.pstdev(rets)
    if vol == 0:
        return 0.0
    r20 = closes[-1] / closes[-21] - 1
    r60 = closes[-1] / closes[-61] - 1
    z = 0.5 * r20 / (vol * math.sqrt(20)) + 0.5 * r60 / (vol * math.sqrt(60))
    return math.tanh(z / 2)


def news_score(headlines, scorer, now, half_life_hours, lookback_hours, prior_weight=1.0,
               opinion_weight=0.25):
    """Recency-weighted average of headline scores, shrunk toward 0.

    Each headline's weight halves every `half_life_hours`, and opinion pieces
    (questions, comparisons, listicles) count `opinion_weight` as much as news.
    `prior_weight` acts like one extra neutral headline, so a single story
    moves the score less than a steady stream of stories pointing the same way.
    """
    cutoff = now - timedelta(hours=lookback_hours)
    num = den = 0.0
    for h in headlines:
        s = h.scores.get(scorer)
        published = h.published_dt
        if s is None or published < cutoff:
            continue
        age_h = max(0.0, (now - published).total_seconds() / 3600)
        w = 0.5 ** (age_h / half_life_hours)
        if getattr(h, "kind", "news") == "opinion":
            w *= opinion_weight
        num += w * s
        den += w
    return num / (den + prior_weight) if den else 0.0


def strategy_scores(name, params, tickers, histories, headlines_by_ticker, asof, now, news_cfg):
    """{ticker: score} for one strategy as of the close on `asof`."""

    def mom(t):
        hist = histories.get(t)
        return momentum_score([b.close for b in hist.bars_until(asof)]) if hist else 0.0

    def news(t, scorer):
        return news_score(
            headlines_by_ticker.get(t, []), scorer, now,
            news_cfg["half_life_hours"], news_cfg["lookback_hours"],
            opinion_weight=news_cfg.get("opinion_weight", 0.25),
        )

    if name == "momentum":
        return {t: mom(t) for t in tickers}
    if name == "news":
        return {t: news(t, "lexicon") for t in tickers}
    if name in ("claude", "finbert"):
        return {t: news(t, name) for t in tickers}
    if name == "hybrid":
        w = params.get("news_weight", 0.6)
        return {t: w * news(t, "lexicon") + (1 - w) * mom(t) for t in tickers}
    raise ValueError(f"Unknown strategy {name!r}")


def target_weights(scores, held, entry, exit_, max_positions):
    """Long-only target portfolio, equal weight per slot.

    Held stocks stay while their score is above `exit_`; new stocks need at
    least `entry`. The gap between the two thresholds stops the portfolio from
    churning on small score changes. Each position gets 1/max_positions of the
    account and unused slots stay in cash.
    """
    keep = sorted((t for t in held if scores.get(t, 0.0) > exit_), key=lambda t: -scores[t])
    new = sorted(
        (t for t, s in scores.items() if s >= entry and t not in keep), key=lambda t: -scores[t]
    )
    picks = (keep + new)[:max_positions]
    return {t: 1.0 / max_positions for t in picks}
