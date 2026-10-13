"""Headline filtering, checked against real headlines from the first live run."""

import pytest

from papertrader.news import Headline, classify, filter_relevant, name_patterns

ALIASES = {
    "AAPL": ["Apple", "iPhone"], "BA": ["Boeing"], "COST": ["Costco"], "V": ["Visa"],
    "GOOGL": ["Alphabet", "Google", "GOOG"], "UNH": ["UnitedHealth"], "NVDA": ["Nvidia"],
    "JPM": ["JPMorgan", "JPMorgan Chase"], "META": ["Meta", "Meta Platforms"],
}


def kind(ticker, title):
    return classify(title, ticker, name_patterns(ticker, ALIASES[ticker]))


@pytest.mark.parametrize("ticker,title", [
    ("UNH", "Is Oscar Health Stock a Buy as Growth Surges but Valuation Stays Rich?"),
    ("NVDA", "Why BigBear.ai Stock Soared as Much as 11.7% Today"),
    ("JPM", "Stock Market Today: Nasdaq-100 Trims Losses; Cheesecake Factory Breaks Out"),
    ("COST", "Kroger to cut 3K corporate jobs over the next 3 years"),
    ("COST", "The cost of AI chips keeps rising"),  # "cost" is not the ticker COST
    ("V", "Stocks rally as V-shaped recovery takes hold"),
])
def test_offtopic(ticker, title):
    assert kind(ticker, title) == "offtopic"


@pytest.mark.parametrize("ticker,title", [
    ("BA", "The Boeing Company $BA Stock Position Increased by NorthCrest Asset Manangement LLC"),
    ("COST", "NorthCrest Asset Manangement LLC Purchases 3,958 Shares of Costco Wholesale Corporation $COST"),
    ("META", "Meta Platforms, Inc. $META Shares Sold by Ring Mountain Capital LLC"),
    ("COST", "1,350 Costco Wholesale Corporation $COST Shares Acquired by First County Bank CT"),
    ("JPM", "JPMorgan Chase, Goldman, Micron, J&J, UnitedHealth, and More Stocks That Explain Today's Market"),
    ("GOOGL", "Alphabet Inc. Tokenized Stock (Coinbase) price today, GOOGLc to USD live price"),
])
def test_junk(ticker, title):
    assert kind(ticker, title) == "junk"


@pytest.mark.parametrize("ticker,title", [
    ("BA", "Boeing vs. Lockheed Martin: Which Aerospace Stock Is a Better Buy in 2026?"),
    ("AAPL", "What Would Weak iPhone Demand Do To Apple Stock?"),
    ("UNH", "UnitedHealth (UNH) Stock Trades Up, Here Is Why"),
])
def test_opinion(ticker, title):
    assert kind(ticker, title) == "opinion"


@pytest.mark.parametrize("ticker,title", [
    ("V", "Visa (V) Gains Approval for China Bank Card Clearing Operation, Shares Rise Premarket"),
    ("BA", "Bernstein cuts target for Boeing stock from USD 298 to USD 278"),
    ("COST", "Costco (COST) Posts Strong Q4 Results Amid Valuation Debate"),
    ("GOOGL", "Google wins dismissal of ad-tech lawsuit"),
    ("NVDA", "INTC, AMD, NVDA: Chip Stocks Jump Premarket"),
    ("AAPL", "Apple (NASDAQ:AAPL) Stock Rises as New US$299 AI Home Device Takes Aim at Amazon"),
])
def test_news(ticker, title):
    assert kind(ticker, title) == "news"


def test_filter_relevant_sets_kind_and_counts():
    hs = [
        Headline("1", "BA", "Boeing vs. Airbus: which is the better buy?", "2026-10-13T12:00:00+00:00"),
        Headline("2", "BA", "Boeing reports 161 deliveries", "2026-10-13T12:00:00+00:00"),
        Headline("3", "BA", "GE Aerospace raises guidance", "2026-10-13T12:00:00+00:00"),
    ]
    kept, counts = filter_relevant(hs, {"BA": ["Boeing"]})
    assert [h.kind for h in kept] == ["opinion", "news"]
    assert counts == {"opinion": 1, "news": 1, "offtopic": 1}
