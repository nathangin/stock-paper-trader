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
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **News (word-list sentiment)**: all cash; cash $100,000
  - next open: MSFT 20%, UNH 20%, V 20%
- **Momentum (prices only)**: all cash; cash $100,000
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Buy & hold SPY**: all cash; cash $100,000
  - next open: SPY 100%

## Strongest news signals

- **UNH** (UnitedHealth) news score +0.22
  - Sector Update: Healthcare Stocks Fall Late Afternoon _(unknown; words -0.34)_
  - Q3 2026: UnitedHealth’s Profits Soar as it Covers Fewer People, Pays Less for Care _(HEALTH CARE un-covered; words +0.64)_
  - QUICK SPARK: UnitedHealth Calls 2026 the Bottom for Medicaid Margins _(Benzinga; words +0.00)_
- **V** (Visa) news score +0.19
  - Visa wins China approval: Visa stock after-hours at EUR 353.58, plus 0.66 percent versus Xetra close _(ad-hoc-news.de; words +0.72)_
  - Buffett Successor Sold Visa Stock in Q1: Why That May Have Been an $823M Mistake _(Benzinga; words +0.00)_
  - Is Visa Stock Increasing Your Market Risk? _(unknown; words -0.15)_
- **MSFT** (Microsoft) news score +0.15
  - If Palantir Stock Looks Expensive, You Need To Read This _(unknown; words +0.00)_
  - What Would It Take For Salesforce Stock To Move Higher? _(unknown; words +0.00)_
  - Is Snowflake Stock Riskier Than It Looks? _(unknown; words +0.00)_
- **JPM** (JPMorgan) news score -0.14
  - Tenable Announces Closing of New $400M Secured Revolving Credit Facility _(unknown; words +0.00)_
  - JPMorgan Earnings: Solid Results Despite Capital Markets Softening _(Morningstar; words +0.00)_
  - Stock Market Today: Nasdaq-100 Trims Losses; Cheesecake Factory Breaks Out (Live Coverage) _(unknown; words -0.34)_
- **NFLX** (Netflix) news score -0.12
  - Netflix Stock Is Trending: What's Going On? _(AOL.com; words +0.00)_
  - Can You Make Money Off Netflix Stock Now? _(unknown; words +0.00)_
  - Netflix Stock (NFLX) Is Double Downgraded by Huber Research. Here’s Why _(TipRanks; words -0.64)_
- **AMD** (AMD) news score +0.12
  - AMD Stocks Slip 1.2% Although Sweden Deployment Broadens Its AI Reach _(Yahoo Finance; words +0.00)_
  - What Is Next For Micron Stock? _(unknown; words +0.00)_
  - Fermi Stock Soars 20% on AMD Deal. Why Analysts See Hurdles Ahead. _(Barron's; words +0.64)_

See `docs/index.html` for the chart and full tables.
