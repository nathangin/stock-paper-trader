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


@pytest.mark.parametrize("text,sign", [
    ("Meta's Costs Surged in the Second Quarter", -1),
    ("Rivian losses narrow as deliveries climb", 1),
    ("Uber loss widens on legal charges", -1),
])
def test_subject_flips(text, sign):
    assert score_text(text) * sign > 0


# Real headlines from Oct 17-23 2026 that the word list used to read the wrong way round.
@pytest.mark.parametrize("text, sign", [
    ("Tesla stock slips despite Q3 earnings beat, better-than-expected capex spend", -1),
    ("ETFs in Focus as META Drops 7% Despite Q3 Earnings Beat, Strong View", -1),
    ("Intel Stocks Edge Higher Despite Susquehanna's $105 Target Cut", 1),
    ("Broadcom remains a Buy despite AI lab concerns and recent stock selloff, trading at attractive valuation.", 1),
    ("Iran War Erodes Exxon, Chevron Profits Even as Oil Prices Soar", -1),
    ("META Stock Set To Record Worst Day In Nearly Three Months As Investors Fret Over Negative Cash Flows", -1),
    ("Dan Ives Calls the Selloff in NVDA Stock a Buying Opportunity as Analysts See 53% Upside", 1),
    ("Despite the earnings beat, Tesla shares tumble", -1),
])
def test_contrast_words_and_new_terms(text, sign):
    assert score_text(text) * sign > 0


def test_but_weights_the_second_half_more():
    assert score_text("Shares fall, but analysts upgrade the stock") > 0
    assert score_text("Revenue surges but the company cuts guidance") < 0


@pytest.mark.parametrize("text", [
    "Walmart stock sits 8.81 percent below its 52-week high at EUR 105.76",
    "Microsoft stock: Below its 52-week high, Microsoft stock trades 5.55 percent lower",
])
def test_distance_from_a_high_is_not_a_new_high(text):
    assert score_text(text) == 0
    assert score_text("Apple hits a new all-time high against the market trend") > 0
