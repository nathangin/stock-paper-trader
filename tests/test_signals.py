from datetime import datetime, timedelta, timezone

import pytest

from papertrader.news import Headline
from papertrader.signals import momentum_score, news_score, target_weights
from tests.conftest import make_history, weekdays

NOW = datetime(2026, 10, 9, 22, tzinfo=timezone.utc)


def test_momentum_sign_follows_trend():
    days = weekdays("2026-01-01", 120)
    up = [b.close for b in make_history("U", days, drift=0.004, vol=0.01, seed=1).bars]
    down = [b.close for b in make_history("D", days, drift=-0.004, vol=0.01, seed=1).bars]
    assert momentum_score(up) > 0.3
    assert momentum_score(down) < -0.3


def test_momentum_needs_history():
    assert momentum_score([100.0] * 60) == 0.0
    assert momentum_score([100.0] * 61) == 0.0  # zero volatility


def _h(score, hours_ago, scorer="lexicon"):
    return Headline("id", "AAA", "t", (NOW - timedelta(hours=hours_ago)).isoformat(), scores={scorer: score})


def test_news_score_shrinks_single_story():
    one = news_score([_h(1.0, 0)], "lexicon", NOW, 24, 72)
    many = news_score([_h(1.0, 0)] * 5, "lexicon", NOW, 24, 72)
    assert one == pytest.approx(0.5)
    assert 0.8 < many < 1.0


def test_news_score_decays_and_ignores_other_scorers():
    fresh = news_score([_h(1.0, 0)], "lexicon", NOW, 24, 72)
    old = news_score([_h(1.0, 48)], "lexicon", NOW, 24, 72)
    assert old < fresh
    assert news_score([_h(1.0, 100)], "lexicon", NOW, 24, 72) == 0.0  # outside lookback
    assert news_score([_h(1.0, 0, scorer="claude")], "lexicon", NOW, 24, 72) == 0.0


def test_target_weights_entry_exit_hysteresis():
    scores = {"A": 0.10, "B": 0.30, "C": 0.20, "D": -0.5}
    # Nothing held: only scores >= entry qualify, best first, capped at max_positions.
    assert target_weights(scores, {}, entry=0.15, exit_=0.0, max_positions=5) == {"B": 0.2, "C": 0.2}
    # A is held and still above exit, so it stays even though it's below entry.
    held = target_weights(scores, {"A": 10}, entry=0.15, exit_=0.0, max_positions=2)
    assert set(held) == {"A", "B"}
    # D is held but below exit, so it's sold.
    assert "D" not in target_weights(scores, {"D": 5}, entry=0.15, exit_=0.0, max_positions=5)


def test_opinion_counts_less():
    news = _h(1.0, 0)
    opinion = _h(-1.0, 0)
    opinion.kind = "opinion"
    # One news item at +1 and one opinion at -1: the news item dominates.
    s = news_score([news, opinion], "lexicon", NOW, 24, 72, opinion_weight=0.25)
    assert s == pytest.approx((1.0 - 0.25) / (1.25 + 1.0))
