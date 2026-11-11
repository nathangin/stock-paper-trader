# Paper trading report

_Through the close on **2026-11-10**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $97,580 | -2.42% | +0.85% | +0.97% | -8.23% | 34 | 51.1% ± 5.5 (317) | Too early to tell (20/60 days) |
| Hybrid (news + momentum) | $97,359 | -2.64% | +0.63% | +0.75% | -4.65% | 22 | 48.4% ± 5.4 (335) | Too early to tell (20/60 days) |
| News (word-list sentiment) | $102,666 | +2.67% | +5.94% | +6.05% | -5.49% | 17 | 48.7% ± 6.5 (230) | Too early to tell (20/60 days) |
| Momentum (prices only) | $97,065 | -2.94% | +0.34% | +0.45% | -4.62% | 21 | 46.7% ± 5.1 (368) | Too early to tell (20/60 days) |
| Equal weight, whole list | $96,613 | -3.39% | -0.11% | – | -6.34% | 22 | – |  |
| Buy & hold SPY | $96,726 | -3.27% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 317 | 51.1% | 52.7% | +18.5 bp | +0.024 (20) |
| Hybrid (news + momentum) | 335 | 48.4% | 51.3% | +17.3 bp | +0.001 (20) |
| News (word-list sentiment) | 230 | 48.7% | 53.0% | +28.3 bp | +0.042 (20) |
| Momentum (prices only) | 368 | 46.7% | 50.0% | +7.6 bp | -0.005 (20) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (39.30 sh), COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh); cash $0
  - next open: AMD 20%, COST 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $36
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AMD (40.58 sh), COST (18.46 sh), LLY (14.58 sh), MSFT (37.54 sh), WMT (168.69 sh); cash $0
  - next open: AMD 20%, AVGO 20%, COST 20%, LLY 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.34 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $10
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **AMD** (AMD) news score +0.20
  - (AMD) Technical Analysis and Trading Signals (AMD:CA) _(Stock Traders Daily; words +0.00)_
  - The Zacks Analyst Blog Highlights Arista Networks, Fabrinet, Analog Devices, Advanced Micro Devices and NVIDIA _(unknown; words +0.00)_
  - Prediction: This Will Be AMD’s Stock Price After 1 Year _(unknown; words +0.00)_
- **NVDA** (Nvidia) news score -0.19
  - The Zacks Analyst Blog Highlights Arista Networks, Fabrinet, Analog Devices, Advanced Micro Devices and NVIDIA _(unknown; words +0.00)_
  - 3 Data Center Infrastructure Stocks Retail Investors Are Watching Beyond Nvidia _(unknown; words +0.00)_
  - Nvidia Bloodbath Over by November’s End? Crypto Bettors Weigh NVDA Stock’s Next Move as Jensen Huang Controversy Brews _(unknown; words +0.00)_
- **WMT** (Walmart) news score +0.18
  - Walmart Stock (WMT) Slips Despite Price Target Upgrades Ahead of Q3 Earnings Next Week _(TipRanks; words -0.29)_
  - Walmart Unlikely to Deliver 'Significant' Upside Surprise; Target Set for Quarterly Beat, RBC Says _(unknown; words +0.64)_
  - Walmart vs. Coca-Cola: 53 and 64 Straight Years of Raises. Which Dividend Grows Faster From Here? _(unknown; words +0.00)_
- **AVGO** (Broadcom) news score +0.15
  - Broadcom Shares Rise 2.20% After Hours - Broadcom (NASDAQ:AVGO), JPMorgan Chase (NYSE:JPM) _(Benzinga; words +0.34)_
  - Broadcom stock rises 4.2% after VM API project addition to CNCF Sandbox _(Traders Union; words +0.34)_
  - Jim Cramer Warns About the AI Data Center Trade. What It Means for Nvidia and Broadcom _(unknown; words -0.46)_
- **AAPL** (Apple) news score +0.11
  - Apple Inc. (NASDAQ:AAPL) Stock Has Consensus Target Price of $343.74 According to Analysts _(MarketBeat; words +0.00)_
  - Tech Peers Ramp Up AI Spending, but Apple’s Restraint Keeps Its Stock Steady _(NAI500; words +0.00)_
  - Apple Harbor Turns Macs Into Private AI Servers With No Cloud Fees _(BeInCrypto; words +0.00)_
- **BA** (Boeing) news score -0.11
  - Boeing October Jet Deliveries Decline, Trail Airbus Tally _(unknown; words -0.34)_
  - Boeing Stock (NYSE:BA) Notches Up With Huge Layoff Plans _(TipRanks; words -0.38)_
  - Read the memo Boeing sent staff announcing 2,500 job cuts in its airliner business _(Business Insider; words -0.24)_

See `docs/index.html` for the chart and full tables.
