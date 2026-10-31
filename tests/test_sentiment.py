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


# Real headlines from Oct 24-31 2026 (earnings week) that the word list scored the wrong way round.
@pytest.mark.parametrize("text, sign", [
    ("Google Erases a Record $500 Billion as AI Eats Into Sales", -1),
    ("Gemini 4 Carbon arrives as Alphabet stock suffers record fall", -1),
    ("Bank of America Clients Are Dumping Meta and Google Stocks at a Record Pace", -1),
    ("Amazon Shares Slide 7% After Hours as Cash Burn Surges Despite 39% AWS Growth", -1),
    ("Alphabet Cloud Revenue Jumps 82%, but Stock Lags as Investors Focus on AI Investment Payback Pace", -1),
    ("Tesla shares pull back as rally pauses", -1),
    ("Google expands AI Search ads globally as core ad growth slows", -1),
    ("Meta erases its 2026 gain as investors punish Big Tech’s biggest spenders", -1),
    ("Stocktwits AI Roundup: Intel, Amazon, Alphabet Results Trigger Meltdown As Big Tech’s Record Spending "
     "Returns To Focus", -1),
    ("Google, Amazon, Intel shares dive on disappointing earnings, AI jitters", -1),
])
def test_earnings_week_headlines(text, sign):
    assert score_text(text) * sign > 0


def test_mixed_results_with_a_disappointment_are_not_good_news():
    assert score_text("Boeing Third-Quarter Loss Narrows Less Than Expected as Commercial Airplane Revenue "
                      "Disappoints") <= 0
    assert score_text("Netflix doesn't disappoint as subscribers jump") > 0
