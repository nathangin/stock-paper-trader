# Paper trading report

_Through the close on **2026-11-18**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $96,740 | -3.26% | +2.56% | +2.19% | -8.23% | 38 | 53.6% ± 4.8 (416) | Too early to tell (26/60 days) |
| Hybrid (news + momentum) | $97,734 | -2.27% | +3.55% | +3.18% | -4.65% | 22 | 50.8% ± 4.7 (429) | Too early to tell (26/60 days) |
| News (word-list sentiment) | $102,899 | +2.90% | +8.72% | +8.35% | -5.49% | 25 | 52.0% ± 5.7 (298) | Too early to tell (26/60 days) |
| Momentum (prices only) | $97,463 | -2.54% | +3.28% | +2.91% | -4.62% | 21 | 48.6% ± 4.5 (477) | Too early to tell (26/60 days) |
| Equal weight, whole list | $94,552 | -5.45% | +0.37% | – | -6.34% | 25 | – |  |
| Buy & hold SPY | $94,182 | -5.82% | – | – | -5.82% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 416 | 53.6% | 53.6% | +24.3 bp | +0.067 (26) |
| Hybrid (news + momentum) | 429 | 50.8% | 53.1% | +20.9 bp | +0.042 (26) |
| News (word-list sentiment) | 298 | 52.0% | 53.4% | +32.2 bp | +0.070 (26) |
| Momentum (prices only) | 477 | 48.6% | 51.2% | +5.4 bp | +0.032 (26) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh), XOM (117.83 sh); cash $650
  - next open: COST 20%, LLY 20%, V 20%, WMT 20%, XOM 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $59
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: COST (18.46 sh), DIS (172.58 sh), WMT (168.69 sh); cash $40,048
  - next open: COST 20%, DIS 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $23
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.27
  - Intel signs first external customer for advanced 18A chips _(CNBC; words +0.00)_
  - Marvell And Intel Halved: How Long Until They Recover? _(unknown; words +0.00)_
  - QUICK SPARK: Intel Stock Eyes Worst Two-Month Drop on Record After a Triple-Digit Rally _(Benzinga; words +0.05)_
- **UNH** (UnitedHealth) news score -0.25
  - ANT, UNH, CRWD, TTWO, AMZN: 5 Trending Stocks Today - Amazon.com (NASDAQ:AMZN) _(Benzinga; words +0.00)_
  - UnitedHealth Shares Fall 10.2% Amid Medicare Audit Proposal _(JournalArta; words -0.34)_
  - UnitedHealth Group (UNH) Stock Price Prediction: Pullback tests support as trading momentum cools _(Blockchain News; words -0.05)_
- **DIS** (Disney) news score +0.20
  - Walt Disney (DIS) Beats On Earnings And Lifts Dividend, Is The Stock Fully Valued? _(Simply Wall St; words +0.46)_
  - Disney Rises 5% as 10 Analysts Raise Targets on Earnings Beat and $3 Billion Savings Plan _(TIKR.com; words +0.69)_
  - After a $382K stock sale in August, a Walt Disney (DIS) officer proposes selling more shares. _(Stock Titan; words +0.00)_
- **NFLX** (Netflix) news score -0.11
  - Netflix trades near 16 times earnings after a 50% slide from its peak _(Startup Fortune; words -0.57)_
  - Josh Brown Says Netflix Trades at 16 Times Next Year’s Earnings After a 50% Drop. Is It a Buy? _(unknown; words -0.34)_
  - Rep. Byron Donalds Sells Netflix Stock for Loss: Here’s What He’s Buying Instead _(TradingView; words -0.29)_
- **COST** (Costco) news score +0.08
  - Costco sees surge in emergency supply purchases amid tech outages _(NewsNation; words +0.64)_
  - Costco Shoppers Panic Buy Rice, Water and Generators as Tech Outages Spark Fears _(Baller Alert; words -0.38)_
  - Tech Outages Spark Panic Buying, Costco Reaps the Rewards _(Breitbart News; words +0.00)_
- **LLY** (Eli Lilly) news score +0.07
  - What Eli Lilly Buyers Were Betting On _(Simply Wall St; words +0.00)_
  - Eli Lilly & Co. stock underperforms Wednesday when compared to competitors _(MarketWatch; words +0.00)_
  - Lilly Buying Spree Surpasses $32B _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
