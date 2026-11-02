# Paper trading report

_Through the close on **2026-10-30**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $95,765 | -4.23% | -1.71% | -0.61% | -5.14% | 21 | 53.7% ± 6.9 (203) | Too early to tell (13/60 days) |
| Hybrid (news + momentum) | $97,529 | -2.47% | +0.06% | +1.15% | -4.65% | 14 | 50.5% ± 6.7 (212) | Too early to tell (13/60 days) |
| News (word-list sentiment) | $101,483 | +1.48% | +4.01% | +5.10% | -1.24% | 9 | 53.1% ± 8.1 (147) | Too early to tell (13/60 days) |
| Momentum (prices only) | $97,172 | -2.83% | -0.30% | +0.79% | -4.62% | 14 | 49.4% ± 6.4 (235) | Too early to tell (13/60 days) |
| Equal weight, whole list | $96,380 | -3.62% | -1.09% | – | -3.68% | 20 | – |  |
| Buy & hold SPY | $97,474 | -2.53% | – | – | -2.53% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 203 | 53.7% | 54.7% | +33.3 bp | +0.087 (13) |
| Hybrid (news + momentum) | 212 | 50.5% | 51.9% | +36.7 bp | +0.050 (13) |
| News (word-list sentiment) | 147 | 53.1% | 52.4% | +31.4 bp | +0.087 (13) |
| Momentum (prices only) | 235 | 49.4% | 51.5% | +28.4 bp | +0.021 (13) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AVGO (58.58 sh), COST (20.77 sh), DIS (155.22 sh), LLY (13.54 sh), UNH (47.26 sh); cash $0
  - next open: COST 20%, LLY 20%, UNH 20%, V 20%, XOM 20%
- **Hybrid (news + momentum)**: COST (16.51 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: AVGO (59.57 sh), MSFT (37.54 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $1,249
  - next open: LLY 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (149.49 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $8
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.47
  - Trump Bragged About Intel Stock Gains. Now the U.S. Stake Has Lost $11 Billion _(unknown; words +0.34)_
  - ‘We thought the worst was over’: Intel Israel workers fear layoffs after 30% stock plunge _(Ynetnews; words -0.95)_
  - Intel: PC Demand Destruction Meets AI Supply Headwinds-Profit Taking Continues _(Seeking Alpha; words +0.00)_
- **LLY** (Eli Lilly) news score +0.23
  - Eli Lilly’s First Full Medicare Quarter: Is Volume Still Outrunning Price Cuts? _(MarketBeat; words -0.24)_
  - Notable healthcare headlines for the week: Eli Lilly, Merck, and AstraZeneca in focus _(TradingView; words +0.00)_
  - Novo Nordisk's November Reckoning: Lilly's Tailwind, a Courtroom Loss and a CagriSema Caveat _(ad-hoc-news.de; words -0.29)_
- **XOM** (ExxonMobil) news score +0.21
  - 1 Stock to Buy, 1 Stock to Sell This Week: ExxonMobil, Uber _(Investing.com; words +0.00)_
  - ExxonMobil Q3 Earnings: 3 Key Takeaways for Long-Term Investors _(The Globe and Mail; words +0.00)_
  - About Exxon Mobil (Stove Tokenized Stock) _(Coinbase; words +0.00)_
- **GOOGL** (Alphabet) news score -0.18
  - Reddit Stock Crashed 29%: Is Google AI Coming for More Stocks? _(unknown; words +0.00)_
  - Alphabet (GOOG) Stock Price, Chart & Analysis _(www.debelegger.nl; words +0.00)_
  - Google's ad impressions have fallen 14% as a nearly 4-year slide continues _(24/7 Wall St.; words -0.38)_
- **AMZN** (Amazon) news score -0.13
  - Amazon (AMZN) Stock May Be Underpriced Despite AI Spending Fears _(Simply Wall St; words +0.00)_
  - Amazon Stock Fell After Earnings. Jim Cramer Says Buy Right Here _(unknown; words -0.34)_
  - Walmart's $120 Walmart+ and Sam's Club Plus bundle undercuts Amazon Prime's $139 fee with gas, grocery and more perks _(unknown; words +0.00)_
- **BA** (Boeing) news score -0.11
  - Cramer thinks Boeing’s problems aren’t going away soon, says buy GE _(unknown; words +0.00)_
  - Boeing faces securities fraud probe after FAA delays 737 MAX 10 _(scanx.trade; words -0.96)_
  - Is Boeing Stock A Real Bargain? _(Trefis; words +0.00)_

See `docs/index.html` for the chart and full tables.
