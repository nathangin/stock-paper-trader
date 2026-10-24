# Paper trading report

_Through the close on **2026-10-23**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $99,052 | -0.95% | +1.03% | +0.99% | -1.89% | 13 | 53.9% ± 8.6 (128) | Too early to tell (8/60 days) |
| Hybrid (news + momentum) | $96,136 | -3.86% | -1.89% | -1.92% | -3.86% | 9 | 50.0% ± 8.6 (130) | Too early to tell (8/60 days) |
| News (word-list sentiment) | $101,461 | +1.46% | +3.44% | +3.40% | -1.13% | 7 | 54.2% ± 10.0 (96) | Too early to tell (8/60 days) |
| Momentum (prices only) | $96,558 | -3.44% | -1.46% | -1.50% | -3.44% | 9 | 47.9% ± 8.2 (144) | Too early to tell (8/60 days) |
| Equal weight, whole list | $98,058 | -1.94% | +0.04% | – | -2.00% | 20 | – |  |
| Buy & hold SPY | $98,022 | -1.98% | – | – | -1.98% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 128 | 53.9% | 53.1% | +12.8 bp | +0.093 (8) |
| Hybrid (news + momentum) | 130 | 50.0% | 51.5% | +5.3 bp | +0.034 (8) |
| News (word-list sentiment) | 96 | 54.2% | 51.0% | +3.9 bp | +0.085 (8) |
| Momentum (prices only) | 144 | 47.9% | 51.4% | -2.9 bp | -0.010 (8) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (20.77 sh), LLY (16.07 sh), UNH (47.26 sh), V (50.49 sh); cash $17,399
  - next open: COST 20%, LLY 20%, UNH 20%, WMT 20%, XOM 20%
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

- **XOM** (ExxonMobil) news score +0.15
  - ExxonMobil (NYSE:XOM) Upgraded at Wall Street Zen _(MarketBeat; words +0.64)_
  - Exxon Mobil at $183.21: A New 52-Week High and What It Signals _(24/7 Wall St.; words +0.46)_
  - 3 Energy Stocks to Buy and Hold for the Next Decade, Starting With ExxonMobil _(unknown; words +0.00)_
- **UNH** (UnitedHealth) news score +0.15
  - UnitedHealth Group (UNH), What Is Behind The Fresh Attention Now? _(Simply Wall Street; words +0.00)_
  - UnitedHealth Soars 11% in a Week After a Beat-and-Raise Quarter: “Discipline and Execution” _(unknown; words +0.96)_
  - UnitedHealth (NYSE:UNH) Stock Rises 1.91%: P/E, EPS Decline and RSI Review _(Kalkine India; words +0.00)_
- **DIS** (Disney) news score +0.14
  - Could Skydance Be Bigger Than Disney? Skydance (NYSE:SKYD) Stock Rises _(TipRanks; words +0.34)_
  - Walt Disney (NYSE:DIS) Stock Rises 1.16%: P/E, EPS Trend and RSI Review _(Kalkine India; words +0.34)_
  - Disney shares dip 3% as company cuts hundreds in HR and tech units _(scanx.trade; words -0.24)_
- **NFLX** (Netflix) news score -0.12
  - Can Netflix Stock Hold Margin Gains as Content Spending Keeps Growing? _(Zacks Investment Research; words +0.34)_
  - Netflix Stock Slips as Q3 Earnings Hand Investors a Win Wrapped in Caution _(FinanceBuzz; words +0.29)_
  - Netflix Is Now Down 29% This Year: Is NFLX Stock Hopeless or Ready for a Rebound? _(unknown; words +0.38)_
- **WMT** (Walmart) news score +0.11
  - Affirm Lost Walmart to Klarna in 2025. Now It Has Sam’s Club. Here’s What Moves the Stock Before November 5 _(TIKR.com; words +0.00)_
  - Walmart (NASDAQ:WMT) Stock Falls 1% - Here's Why _(MarketBeat; words -0.34)_
  - Walmart (NASDAQ: WMT) Surges Toward $1 Trillion Market Cap As Best Month Since 1999 Raises Valuation Questions _(Foreign Policy Journal; words +0.64)_
- **MSFT** (Microsoft) news score +0.09
  - Dow Jones Futures: Microsoft, Google, Amazon Lead Earnings Wave; What To Do Amid Mixed Signals _(unknown; words +0.00)_
  - Microsoft Earnings Report To Focus On AI Momentum, Capex _(unknown; words +0.20)_
  - Tech Stocks Got A Late Lift From Microsoft And ServiceNow _(Finimize; words +0.00)_

See `docs/index.html` for the chart and full tables.
