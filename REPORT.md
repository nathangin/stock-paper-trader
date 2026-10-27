# Paper trading report

_Through the close on **2026-10-26**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $98,705 | -1.30% | -0.01% | +0.21% | -2.23% | 15 | 55.4% ± 8.3 (139) | Too early to tell (9/60 days) |
| Hybrid (news + momentum) | $96,488 | -3.51% | -2.23% | -2.01% | -3.86% | 10 | 50.3% ± 8.1 (147) | Too early to tell (9/60 days) |
| News (word-list sentiment) | $101,394 | +1.39% | +2.68% | +2.90% | -1.13% | 7 | 53.8% ± 9.5 (106) | Too early to tell (9/60 days) |
| Momentum (prices only) | $96,535 | -3.46% | -2.18% | -1.96% | -3.46% | 10 | 48.8% ± 7.7 (162) | Too early to tell (9/60 days) |
| Equal weight, whole list | $98,496 | -1.50% | -0.22% | – | -2.00% | 20 | – |  |
| Buy & hold SPY | $98,718 | -1.28% | – | – | -1.98% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 139 | 55.4% | 54.0% | +14.1 bp | +0.081 (9) |
| Hybrid (news + momentum) | 147 | 50.3% | 50.3% | +2.6 bp | +0.005 (9) |
| News (word-list sentiment) | 106 | 53.8% | 50.0% | +2.4 bp | +0.034 (9) |
| Momentum (prices only) | 162 | 48.8% | 50.6% | -3.3 bp | -0.034 (9) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (20.77 sh), JPM (59.37 sh), LLY (16.07 sh), UNH (47.26 sh); cash $18,036
  - next open: COST 20%, INTC 20%, JPM 20%, LLY 20%, UNH 20%
- **Hybrid (news + momentum)**: COST (16.49 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $0
  - next open: MSFT 20%, UNH 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (149.24 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **TSLA** (Tesla) news score +0.19
  - SPCX Stock Up Nearly 10% Since IPO — Analyst Sees 82% Upside Without Tesla Merger, Even If Revenue Misses Lofty Goals _(unknown; words -0.24)_
  - Tesla Could Go Beyond Robotaxis Into Underground Travel And Electric Aviation — TSLA Could ‘Own’ Transportation, ARK Says _(unknown; words +0.00)_
  - Tesla Could Go Beyond Robotaxis Into Underground Travel And Electric Aviation — TSLA Could ‘Own’ Transpor _(Benzinga; words +0.00)_
- **INTC** (Intel) news score +0.14
  - Analysts Are Bullish on Intel’s Outlook, and an Acquisition Strengthens Its Position in the Quantum Race _(NAI500; words +0.54)_
  - Semtech, NXP Semiconductors, Intel, Seagate, and Western Digital shares skyrocket, what you need to know _(unknown; words +0.00)_
  - Chip Stocks Roar Back: AMD, Intel Power SOXX Toward Best Month Since June _(Stocktwits; words +0.00)_
- **NFLX** (Netflix) news score -0.14
  - Netflix Content-Tech Conflict Intensifies Amid Leadership Shakeup _(조선일보; words +0.00)_
  - I Read Every Page of the Netflix Investor Update. Here's What You Need to Know _(The Globe and Mail; words +0.00)_
  - Congressman Could Be Down 2.65x Annual Salary by Betting on Netflix Stock: Here’s the Math _(unknown; words +0.00)_
- **UNH** (UnitedHealth) news score +0.11
  - Is UnitedHealth Group (NYSE:UNH) Turning A Corner After Recent Pressure? _(Kalkine Media; words +0.00)_
  - Tennessee rate news positive for Elevance, UnitedHealth, says Evercore ISI _(TipRanks; words +0.00)_
  - Mizuho raises target for UnitedHealth Group stock to USD 500 _(ad-hoc-news.de; words +0.54)_
- **NVDA** (Nvidia) news score +0.09
  - NVIDIA and Meta to Expand Collaboration on Muse and Muse Family of Models Amid Robust Growth _(unknown; words +0.24)_
  - NVIDIA plans a $3 billion investment in Meta as both expand work on AI that does tasks for users. _(Stock Titan; words +0.00)_
  - Nvidia, Chipmakers Face Higher Costs? TSMC Reportedly Plans Up To 20% Price Hike For Advanced Chip Packaging _(unknown; words +0.00)_
- **XOM** (ExxonMobil) news score +0.09
  - ExxonMobil (NYSE:XOM) Share Price, Forecast & Analysis _(Stocks Down Under; words +0.00)_
  - How Investors Are Reacting To ExxonMobil Stock As Earnings Near _(Simply Wall Street; words +0.00)_
  - Can ExxonMobil (NYSE:XOM) Maintain Its Momentum Amid Shifting Oil Markets? _(Kalkine Media; words +0.20)_

See `docs/index.html` for the chart and full tables.
