# Paper trading report

_Through the close on **2026-11-13**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $99,895 | -0.10% | +2.60% | +2.34% | -8.23% | 35 | 53.7% ± 5.1 (367) | Too early to tell (23/60 days) |
| Hybrid (news + momentum) | $98,759 | -1.24% | +1.46% | +1.20% | -4.65% | 22 | 50.3% ± 5.0 (382) | Too early to tell (23/60 days) |
| News (word-list sentiment) | $104,545 | +4.54% | +7.25% | +6.99% | -5.49% | 21 | 51.5% ± 6.0 (270) | Too early to tell (23/60 days) |
| Momentum (prices only) | $98,453 | -1.55% | +1.15% | +0.89% | -4.62% | 21 | 48.3% ± 4.8 (424) | Too early to tell (23/60 days) |
| Equal weight, whole list | $97,559 | -2.44% | +0.26% | – | -6.34% | 22 | – |  |
| Buy & hold SPY | $97,299 | -2.70% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 367 | 53.7% | 50.7% | +23.1 bp | +0.055 (23) |
| Hybrid (news + momentum) | 382 | 50.3% | 50.0% | +17.4 bp | +0.012 (23) |
| News (word-list sentiment) | 270 | 51.5% | 50.7% | +32.1 bp | +0.075 (23) |
| Momentum (prices only) | 424 | 48.3% | 51.4% | +2.3 bp | +0.000 (23) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (35.46 sh), COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh); cash $2,208
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $59
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AAPL (58.88 sh), AMD (40.58 sh), AVGO (57.24 sh), COST (18.46 sh), WMT (168.69 sh); cash $0
  - next open: AAPL 20%, AMD 20%, AVGO 20%, COST 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $23
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.34 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $21
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **MSFT** (Microsoft) news score -0.15
  - Microsoft says affected services fully recovered following worldwide outage _(Al Jazeera; words -0.46)_
  - DAS Technology Gives Retailers a Competitive Advantage During Microsoft Outage _(unknown; words -0.46)_
  - Whale Rock Capital takes new stake in Microsoft, exits Apple, among Q3 moves (HPE:NYSE) _(Seeking Alpha; words +0.00)_
- **LLY** (Eli Lilly) news score +0.14
  - Eli Lilly (LLY) Faces New Vision Loss Lawsuits As Pipeline Milestones Keep Coming _(Simply Wall St; words -0.29)_
  - What Eli Lilly Doubters Overlooked _(unknown; words +0.00)_
  - What Is The Market Seeing In Eli Lilly Stock? _(unknown; words +0.00)_
- **NVDA** (Nvidia) news score -0.14
  - Is Nvidia Worth This Much Less Without Jensen Huang? _(unknown; words +0.00)_
  - Nvidia Fallout Puts WPP Stock And Crisis Advisory Firms In Focus _(unknown; words +0.00)_
  - Fact Check: Trump DID 'Dump' Up To $1 Million In Nvidia Stock -- But Also Bought Up To $1.6 Million _(Yahoo; words -0.20)_
- **INTC** (Intel) news score -0.13
  - INTC Stock Week Ahead (November 16–20): What to Know _(JournalArta; words +0.00)_
  - Soros Fund's Q3 Holdings Shake-Up: Intel Stake Surges More Than 27-Fold, New SK Hynix Position, Nvidia Trimmed _(BigGo Finance; words +0.64)_
  - Lawsuit filed against Intel over alleged mislea... _(Pluang; words -0.46)_
- **COST** (Costco) news score +0.12
  - What Costco Wholesale Doubters Overlooked _(Simply Wall St; words +0.00)_
  - Costco uses AI to auto-reorder drugs, keeping p... _(Pluang; words +0.00)_
  - Costco Trusts AI to Reorder Drugs. Most Retailers Won’t _(PYMNTS.com; words +0.00)_
- **UNH** (UnitedHealth) news score +0.09
  - UnitedHealth Group (UNH) Stock Looks Like A Bargain After A 30% Rise _(Simply Wall St; words +0.34)_
  - At $402.94 each, 587 UnitedHealth (UNH) shares were delivered or withheld for exercise-price or tax payments. _(Stock Titan; words +0.00)_
  - Can UNH's Optum Rx Sustain Profit Growth as Prescription Volumes Fall? _(TradingView; words +0.10)_

See `docs/index.html` for the chart and full tables.
