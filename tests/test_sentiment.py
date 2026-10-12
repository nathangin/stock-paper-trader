import pytest

from papertrader.sentiment import score_text


@pytest.mark.parametrize(
    "text",
    [
        "Apple beats estimates and raises guidance",
        "Nvidia shares surge to record high on strong demand",
        "Analyst upgrades Boeing, lifts price target",
    ],
)
def test_positive(text):
    assert score_text(text) > 0.4


@pytest.mark.parametrize(
    "text",
    [
        "Tesla misses estimates, cuts guidance",
        "Intel plunges after downgrade",
        "SEC investigation into accounting fraud at Example Co",
    ],
)
def test_negative(text):
    assert score_text(text) < -0.4


def test_neutral_is_zero():
    assert score_text("Microsoft to hold annual shareholder meeting in December") == 0


def test_negation_flips_sign():
    assert score_text("Drug did not win approval") < 0
    assert score_text("Company says it does not expect layoffs") > 0


def test_phrase_counts_once():
    # "beats estimates" is a phrase; "beats" must not be counted a second time.
    assert score_text("beats estimates") == pytest.approx(score_text("tops estimates"))


def test_bounded():
    s = score_text("surge soar jump rally record strong beats upgrade " * 5)
    assert 0 < s <= 1
