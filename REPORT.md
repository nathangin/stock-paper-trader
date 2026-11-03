# Paper trading report

_Through the close on **2026-11-02**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $96,146 | -3.85% | -0.86% | +0.20% | -5.14% | 26 | 54.3% ± 6.6 (221) | Too early to tell (14/60 days) |
| Hybrid (news + momentum) | $97,847 | -2.15% | +0.84% | +1.90% | -4.65% | 15 | 51.1% ± 6.4 (231) | Too early to tell (14/60 days) |
| News (word-list sentiment) | $101,823 | +1.82% | +4.82% | +5.88% | -1.24% | 11 | 52.5% ± 7.8 (158) | Too early to tell (14/60 days) |
| Momentum (prices only) | $97,226 | -2.77% | +0.22% | +1.28% | -4.62% | 15 | 49.8% ± 6.1 (255) | Too early to tell (14/60 days) |
| Equal weight, whole list | $95,946 | -4.05% | -1.06% | – | -4.11% | 20 | – |  |
| Buy & hold SPY | $97,007 | -2.99% | – | – | -2.99% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 221 | 54.3% | 55.2% | +40.2 bp | +0.093 (14) |
| Hybrid (news + momentum) | 231 | 51.1% | 52.4% | +40.9 bp | +0.062 (14) |
| News (word-list sentiment) | 158 | 52.5% | 53.2% | +35.4 bp | +0.091 (14) |
| Momentum (prices only) | 255 | 49.8% | 51.8% | +32.3 bp | +0.035 (14) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (18.85 sh), LLY (13.54 sh), UNH (47.26 sh), V (46.08 sh), XOM (104.06 sh); cash $204
  - next open: BA 20%, COST 20%, LLY 20%, V 20%, XOM 20%
- **Hybrid (news + momentum)**: COST (16.51 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, LLY 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: LLY (14.58 sh), MSFT (37.54 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $480
  - next open: LLY 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (149.49 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $8
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.31
  - Intel’s Outlook Spooked Chip Investors – Can AMD Reassure Wall Street? _(unknown; words +0.00)_
  - Intel: A New Setback Rightfully Leaves Investors Rightfully Disappointed _(Seeking Alpha; words -0.38)_
  - Intel Shares Plunge 45%, Foundry Business Faces Critical Test : Business/Industry : JKN _(재경일보; words -0.72)_
- **DIS** (Disney) news score -0.19
  - Walt Disney stock slips 0.32% to EUR 100.72 premarket _(ad-hoc-news.de; words -0.29)_
  - DIS Stock Ticks Higher Overnight: Disney Reportedly Weighs Thousands Of Job Cuts In Fresh Cost-Cutting Push Under Josh D’Amaro _(unknown; words -0.24)_
  - Disney Eyes Thousands of Layoffs as It Targets 20% Cost Savings _(TipRanks; words -0.38)_
- **AMZN** (Amazon) news score +0.17
  - Amazon CEO Andy Jassy Says Investors Are ‘Sleeping a Bit’ on Retail as AMZN Stock Falls 7% in 6 Months _(Yahoo Finance; words -0.34)_
  - Amazon's Report Passed Both Tests I Set for It. I'd Buy More of the Stock Now. _(unknown; words +0.00)_
  - Amazon Prime Video beats Apple TV _(unknown; words +0.46)_
- **XOM** (ExxonMobil) news score +0.13
  - Chevron & Exxon Mobil Stocks Retreat From 52-Week Highs: Buy the Dip? _(Zacks Investment Research; words -0.50)_
  - ExxonMobil Third-Quarter Net Profit Doubles to $15.4 Billion, Refining Segment the Main Driver _(BigGo Finance; words +0.20)_
  - ExxonMobil (NYSE:XOM) Stock Price Down 3.9% - What's Next? _(MarketBeat; words +0.00)_
- **LLY** (Eli Lilly) news score +0.11
  - Eli Lilly Posts Strong Quarterly Results and Hits Record High Stock Price _(NAI500; words +0.64)_
  - Unprecedented weight-loss drug craze pushing Lilly to near-record highs _(TheStreet; words +0.00)_
  - Eli Lilly Stock: Is It Still a Buy at $1,400? _(unknown; words +0.00)_
- **BA** (Boeing) news score +0.11
  - Is Defense Backlog Growth Altering The Investment Case For Boeing (BA)? _(unknown; words +0.24)_
  - Why Is Boeing (BA) Pushing Deeper Into Cargo And Airline Data Tools? _(unknown; words +0.00)_
  - Boeing (NYSE:BA) Stock Jumps 2.2% - Here's Why _(MarketBeat; words +0.46)_

See `docs/index.html` for the chart and full tables.
