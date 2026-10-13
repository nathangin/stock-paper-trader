from papertrader import finbert_scorer
from papertrader.news import Headline


class Fake:
    def predict(self, texts):
        return [1.5, -0.25][: len(texts)]


def test_scores_attached_and_clamped():
    hs = [Headline("1", "A", "x", "2026-10-13T00:00:00+00:00"), Headline("2", "A", "y", "2026-10-13T00:00:00+00:00")]
    assert finbert_scorer.score_headlines(hs, model=Fake()) == 2
    assert hs[0].scores["finbert"] == 1.0 and hs[1].scores["finbert"] == -0.25


def test_empty_is_noop():
    assert finbert_scorer.score_headlines([], model=None) == 0
