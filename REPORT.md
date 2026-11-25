# Paper trading report

_Through the close on **2026-11-24**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $96,533 | -3.47% | +3.82% | +4.05% | -8.23% | 44 | 52.4% ± 4.5 (475) | Too early to tell (30/60 days) |
| Hybrid (news + momentum) | $98,824 | -1.18% | +6.11% | +6.34% | -4.65% | 24 | 50.4% ± 4.4 (498) | Too early to tell (30/60 days) |
| News (word-list sentiment) | $104,596 | +4.60% | +11.89% | +12.12% | -5.49% | 29 | 50.3% ± 5.3 (338) | Too early to tell (30/60 days) |
| Momentum (prices only) | $98,528 | -1.47% | +5.82% | +6.05% | -4.65% | 23 | 48.6% ± 4.2 (553) | Too early to tell (30/60 days) |
| Equal weight, whole list | $92,479 | -7.52% | -0.23% | – | -10.94% | 25 | – |  |
| Buy & hold SPY | $92,709 | -7.29% | – | – | -11.03% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 475 | 52.4% | 53.7% | +7.0 bp | +0.052 (30) |
| Hybrid (news + momentum) | 498 | 50.4% | 53.6% | +11.1 bp | +0.042 (30) |
| News (word-list sentiment) | 338 | 50.3% | 53.3% | +1.8 bp | +0.042 (30) |
| Momentum (prices only) | 553 | 48.6% | 51.9% | -1.6 bp | +0.042 (30) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: DIS (157.02 sh), INTC (334.11 sh), LLY (13.54 sh), V (46.81 sh), WMT (152.59 sh); cash $232
  - next open: DIS 20%, INTC 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), TSLA (49.62 sh), WMT (157.18 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, TSLA 20%, WMT 20%
- **News (word-list sentiment)**: DIS (172.58 sh), TSLA (54.04 sh), WMT (168.69 sh); cash $40,343
  - next open: DIS 20%, TSLA 20%, WMT 20%
- **Momentum (prices only)**: AAPL (52.40 sh), COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), WMT (147.22 sh); cash $569
  - next open: AAPL 20%, COST 20%, DIS 20%, LLY 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $165
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **TSLA** (Tesla) news score +0.13
  - Tesla's $3.5 trillion merger talks have a surprising catch _(unknown; words +0.00)_
  - Jensen Huang's Return Could Make a Tesla/SpaceX Merger More Likely _(unknown; words +0.00)_
  - TSLA Stock Slips Overnight: Dell And HP See No Quick Relief From The AI-Driven Chip Crunch Behind Tesla’s 25% Memory Cut _(unknown; words -0.46)_
- **NVDA** (Nvidia) news score +0.11
  - Dow Jones Futures Fall; Trump Says 'Not Too Late' For U.S. To Take Nvidia Stake _(unknown; words -0.34)_
  - NVidia Still Faces 'Key-Man Risk' in Huang: Professor _(unknown; words -0.15)_
  - Jensen Huang Reportedly Says Succession Plan Risks ‘Unnecessary Hierarchy’ At Nvidia — Crypto Bettors Wager on Another Exit _(unknown; words +0.00)_
- **INTC** (Intel) news score +0.10
  - Why Intel Stock Fell Today _(unknown; words -0.34)_
  - Top Analyst Reports for Apple, Philip Morris & Intel _(unknown; words +0.00)_
  - Applied Materials vs. Intel: Which Technology Stock Is a Better Buy for 2027? _(unknown; words +0.00)_
- **UNH** (UnitedHealth) news score -0.09
  - How Much Could You Lose In UnitedHealth Stock? _(unknown; words +0.00)_
  - Can Genoa Help UNH Expand Its Behavioral Health Pharmacy Business? _(unknown; words +0.00)_
  - UnitedHealth Group (UNH) Stock Price Prediction: Oversold Bounce Faces Heavy Overhead Supply _(Blockchain News; words +0.00)_
- **DIS** (Disney) news score +0.08
  - Walt Disney (DIS) Stock Price Prediction: Analyst targets rise as Disney holds above short-term support _(Blockchain News; words +0.34)_
  - Walt Disney (DIS) Stock: $120.27, Up 1.94% Nov 23 _(JournalArta; words +0.00)_
  - Disney Stops Reporting Streaming Profit. Should You Worry? _(unknown; words +0.20)_
- **V** (Visa) news score +0.07
  - iwoca and Visa launch credit card to widen SME funding choice _(unknown; words +0.20)_
  - Visa, Mastercard Seen Gaining From Expansion of Tokenized Payments, UBS Says _(unknown; words +0.54)_
  - CME vs. Visa: Which Financial Stock Is a Better Buy for 2027? _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
