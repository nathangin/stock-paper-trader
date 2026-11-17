# Paper trading report

_Through the close on **2026-11-16**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $98,903 | -1.10% | +3.46% | +3.13% | -8.23% | 36 | 54.2% ± 5.0 (384) | Too early to tell (24/60 days) |
| Hybrid (news + momentum) | $98,779 | -1.22% | +3.34% | +3.00% | -4.65% | 22 | 50.8% ± 4.9 (398) | Too early to tell (24/60 days) |
| News (word-list sentiment) | $102,483 | +2.48% | +7.04% | +6.71% | -5.49% | 22 | 51.8% ± 5.9 (274) | Too early to tell (24/60 days) |
| Momentum (prices only) | $98,474 | -1.53% | +3.03% | +2.70% | -4.62% | 21 | 48.6% ± 4.7 (442) | Too early to tell (24/60 days) |
| Equal weight, whole list | $95,777 | -4.22% | +0.34% | – | -6.34% | 23 | – |  |
| Buy & hold SPY | $95,440 | -4.56% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 384 | 54.2% | 51.8% | +25.0 bp | +0.074 (24) |
| Hybrid (news + momentum) | 398 | 50.8% | 51.0% | +19.4 bp | +0.041 (24) |
| News (word-list sentiment) | 274 | 51.8% | 51.1% | +33.7 bp | +0.086 (24) |
| Momentum (prices only) | 442 | 48.6% | 50.2% | +3.8 bp | +0.030 (24) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (39.52 sh), COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh); cash $164
  - next open: COST 20%, LLY 20%, V 20%, WMT 20%, XOM 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $59
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AAPL (58.88 sh), AMD (40.58 sh), COST (18.46 sh), WMT (168.69 sh); cash $19,023
  - next open: AAPL 20%, COST 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $23
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.43
  - IREN Stock Rises Overnight As Intel Reveals Stake, Anthropic IPO Buzz Catches On _(unknown; words +0.34)_
  - Shareholders Sue Intel After Stock Plunges 29% _(Electronics For You BUSINESS; words -0.72)_
  - Intel Shareholders Sue CEO, CFO After 28.6 Percent Stock Crash In One Day—PC Sales Dipping? _(Tech Times; words -0.76)_
- **AVGO** (Broadcom) news score -0.15
  - Trump’s Tighter Chip Rules Sink AMD and Broadcom, Not Just Nvidia _(unknown; words -0.54)_
  - AMD, MU, SKHY, AVGO: Chip Stocks Ease Overnight After Selloff On New US Chip Restrictions Targeting China _(unknown; words -0.54)_
  - Broadcom Stock (AVGO) Falls 3.9% on Tighter US Chip Rules (Nov 16) _(Gotrade; words -0.34)_
- **MSFT** (Microsoft) news score -0.14
  - Is Cerebras Stock Still a Buy After Its Microsoft Deal? _(unknown; words +0.00)_
  - Microsoft Stock: What Caused the 12 November Outage _(FinanceFeeds; words -0.46)_
  - Microsoft stock at EUR 469.98, down 1.51% premarket _(ad-hoc-news.de; words +0.00)_
- **UNH** (UnitedHealth) news score +0.13
  - UnitedHealth (UNH) Stock: $412.02, Up 1.12% Nov 16 _(JournalArta; words +0.00)_
  - UnitedHealth Group stock gains to EUR 371.50, up 1.61% _(ad-hoc-news.de; words +0.34)_
  - UnitedHealth Group (UNH) Stock Price Prediction: Momentum is holding, but low-volume selling keeps the breakout unconfirmed _(Blockchain News; words +0.60)_
- **AMD** (AMD) news score -0.11
  - Trump’s Tighter Chip Rules Sink AMD and Broadcom, Not Just Nvidia _(TIKR.com; words -0.54)_
  - AMD Acquires Li Feifei’s Team for $8.2 Billion: Beyond Chip Sales to Challenge NVIDIA in AI Leadership _(eu.36kr.com; words +0.00)_
  - Advanced Micro Devices, Inc. $AMD Stock Sold by Banco Santander S.A. _(MarketBeat; words +0.00)_
- **NVDA** (Nvidia) news score -0.09
  - Nvidia to reveal first earnings since spy scandal _(unknown; words +0.00)_
  - Asian stocks sink as scandal-hit Nvidia's earnings loom _(unknown; words -0.54)_
  - Nvidia to halt chip sales to data centers renting over half to China - report _(unknown; words -0.46)_

See `docs/index.html` for the chart and full tables.
