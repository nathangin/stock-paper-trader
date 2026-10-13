# Paper trading report

_Through the close on **2026-10-13**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| Hybrid (news + momentum) | $100,000 | +0.00% | +0.00% | +0.00% | 0 | – | Too early to tell (0/60 days) |
| News (word-list sentiment) | $100,000 | +0.00% | +0.00% | +0.00% | 0 | – | Too early to tell (0/60 days) |
| Momentum (prices only) | $100,000 | +0.00% | +0.00% | +0.00% | 0 | – | Too early to tell (0/60 days) |
| Buy & hold SPY | $100,000 | +0.00% | – | +0.00% | 0 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| Hybrid (news + momentum) | 0 | – | – | – | – |
| News (word-list sentiment) | 0 | – | – | – | – |
| Momentum (prices only) | 0 | – | – | – | – |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **Hybrid (news + momentum)**: all cash; cash $100,000
  - next open: AMD 20%, COST 20%, META 20%, MSFT 20%, V 20%
- **News (word-list sentiment)**: all cash; cash $100,000
  - next open: META 20%, UNH 20%, V 20%
- **Momentum (prices only)**: all cash; cash $100,000
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Buy & hold SPY**: all cash; cash $100,000
  - next open: SPY 100%

## Strongest news signals

- **UNH** (UnitedHealth) news score +0.35
  - Q3 2026: UnitedHealth’s Profits Soar as it Covers Fewer People, Pays Less for Care _(HEALTH CARE un-covered; words +0.64)_
  - QUICK SPARK: UnitedHealth Calls 2026 the Bottom for Medicaid Margins _(Benzinga; words +0.00)_
  - UnitedHealth Group Raises 2026 Outlook As Q3 Operating Earnings Rise To $6.6 Billion _(Pulse 2.0; words +0.34)_
- **V** (Visa) news score +0.33
  - Visa wins China approval: Visa stock after-hours at EUR 353.58, plus 0.66 percent versus Xetra close _(ad-hoc-news.de; words +0.72)_
  - Buffett Successor Sold Visa Stock in Q1: Why That May Have Been an $823M Mistake _(Benzinga; words +0.00)_
  - Is Visa Stock Increasing Your Market Risk? _(unknown; words -0.15)_
- **META** (Meta) news score +0.18
  - Truist Raises Meta Platforms Stock Price Target to a Street-High of $1,000 Ahead of Q3 Earnings. Here’s Why _(TipRanks; words +0.00)_
  - Meta shares rise for a second straight day as new AI model family impresses _(CNBC; words +0.34)_
  - Cathie Wood sells Meta shares after Zuckerberg's big AI launch _(unknown; words +0.20)_
- **JPM** (JPMorgan) news score -0.15
  - JPMorgan Earnings: Solid Results Despite Capital Markets Softening _(Morningstar; words +0.00)_
  - Prediction: JPMorgan Chase Raises Its Dividend Again in 2027 _(unknown; words +0.00)_
  - JPMorgan vs. Citigroup: Which Big Bank Stock Is the Better Buy After Q3 Earnings? _(Zacks Investment Research; words +0.00)_
- **AVGO** (Broadcom) news score -0.12
  - Marvell stock soars 214% in 2026, far outpacing Broadcom and NVIDIA gains. _(Pluang; words +0.80)_
  - Marvell Is Up 214% in 2026 While Broadcom Is Only Up 3%: Take Profits on MRVL Stock, or Hold On for the Ride? _(unknown; words +0.00)_
  - Nvidia Stock Shakes Off Fallout From Broadcom CEO and Microsoft's New Chip -- Barrons.com _(Moomoo; words +0.00)_
- **AAPL** (Apple) news score +0.12
  - Why Apple Hospitality REIT (APLE) Is Getting Attention Today _(Simply Wall Street; words +0.00)_
  - Apple Hits Fresh All-Time High _(unknown; words +0.46)_
  - Apple: With Launch of Foldable iPhone Duo, Things Look Twice as Nice _(Morningstar; words +0.20)_

See `docs/index.html` for the chart and full tables.
