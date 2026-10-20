# Paper trading report

_Through the close on **2026-10-19**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,113 | +0.11% | +1.25% | +0.64% | -0.83% | 9 | 55.7% ± 12.5 (61) | Too early to tell (4/60 days) |
| Hybrid (news + momentum) | $97,458 | -2.54% | -1.40% | -2.02% | -2.54% | 7 | 49.3% ± 12.0 (67) | Too early to tell (4/60 days) |
| News (word-list sentiment) | $100,247 | +0.25% | +1.39% | +0.77% | -1.13% | 7 | 56.5% ± 14.3 (46) | Too early to tell (4/60 days) |
| Momentum (prices only) | $97,669 | -2.33% | -1.19% | -1.81% | -3.27% | 7 | 43.1% ± 11.4 (72) | Too early to tell (4/60 days) |
| Equal weight, whole list | $99,474 | -0.53% | +0.61% | – | -1.26% | 20 | – |  |
| Buy & hold SPY | $98,861 | -1.14% | – | – | -1.56% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 61 | 55.7% | 50.8% | +45.9 bp | +0.206 (4) |
| Hybrid (news + momentum) | 67 | 49.3% | 52.2% | +14.1 bp | -0.002 (4) |
| News (word-list sentiment) | 46 | 56.5% | 54.3% | +37.0 bp | +0.161 (4) |
| Momentum (prices only) | 72 | 43.1% | 51.4% | -20.3 bp | -0.083 (4) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (20.77 sh), LLY (16.07 sh), META (26.28 sh), V (50.49 sh), XOM (111.96 sh); cash $669
  - next open: COST 20%, LLY 20%, META 20%, V 20%, XOM 20%
- **Hybrid (news + momentum)**: META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: META 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $0
  - next open: MSFT 20%, UNH 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score +0.31
  - JPMorgan withdraws negative call on Intel, upgrades to neutral from underweight _(디지털투데이; words +0.34)_
  - 129,502 Shares of Intel Corporation $INTC Bought by Teamwork Financial Advisors LLC _(MarketBeat; words +0.00)_
  - Did Foundry Win Just Shift Intel (INTC) Investment Narrative? _(unknown; words +0.29)_
- **BA** (Boeing) news score -0.21
  - Boeing 737 Max Fraud Lawsuit Tossed for Good After Investor Never Bought Stock _(Law Commentary; words -0.91)_
  - Boeing Price Target Slashed To $235 By RBC – Firm Says Lingering Defense Budget Uncertainty Will Remain A Headwind _(Stocktwits; words -0.66)_
  - US set to announce certification of Boeing 737 MAX 10 Tuesday, sources say By Reuters _(Investing.com; words +0.00)_
- **AMZN** (Amazon) news score +0.20
  - Amazon Stock to Top $300 in October? Prediction Market Punters Trade the Odds as Morgan Stanley Raises Near-Term Target _(unknown; words +0.00)_
  - Amazon Stock to Top $300 in October? Prediction Market Punters Trade the Odds as Morgan Stanley Raises Ne _(Benzinga; words +0.00)_
  - Dow, S&P 500, Nasdaq Edge Higher Amid Tech Rebound As Q3 Earnings Season Forges Ahead: DJT, AMZN, CBRS, CRWV Stocks In Focus _(unknown; words +0.38)_
- **XOM** (ExxonMobil) news score +0.19
  - ExxonMobil (NYSE:XOM) Hits New 52-Week High After Analyst Upgrade _(MarketBeat; words +0.85)_
  - Chevron’s Performance Better than Exxon Mobil Despite High Valuation _(SSBCrack; words +0.00)_
  - Why Did XOM, CVX, MPC Stocks Surge To 52-Week Highs Today? _(unknown; words +0.64)_
- **COST** (Costco) news score +0.15
  - Costco is One of the Best Retailers on the Planet _(The Motley Fool; words +0.00)_
  - APR launches Medicube in 400 Costco stores: 647.9 billion won adds context for APR stock _(ad-hoc-news.de; words +0.20)_
  - COST Stock: Why Truist Remains on the Sidelines on Costco Despite Sales Momentum _(TipRanks; words +0.20)_
- **MSFT** (Microsoft) news score +0.12
  - Microsoft vs. Oracle: Which Tech Stock Is a Better Buy in 2026? _(unknown; words +0.00)_
  - Azure Energy, Thompson, and Tangen Report Significant Ownership Stake in Algorhythm Holdings via 13G Filing _(Kalkine Media; words +0.00)_
  - Why Citi Thinks Microsoft Beats Neoclouds in the AI Debt Squeeze _(unknown; words +0.46)_

See `docs/index.html` for the chart and full tables.
