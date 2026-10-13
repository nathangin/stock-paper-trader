# Paper trading report

_Through the close on **2026-10-13**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Hybrid (news + momentum) | $100,000 | +0.00% | +0.00% | +0.00% | +0.00% | 0 | – | Too early to tell (0/60 days) |
| News (word-list sentiment) | $100,000 | +0.00% | +0.00% | +0.00% | +0.00% | 0 | – | Too early to tell (0/60 days) |
| Momentum (prices only) | $100,000 | +0.00% | +0.00% | +0.00% | +0.00% | 0 | – | Too early to tell (0/60 days) |
| Equal weight, whole list | $100,000 | +0.00% | +0.00% | – | +0.00% | 0 | – |  |
| Buy & hold SPY | $100,000 | +0.00% | – | – | +0.00% | 0 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

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
- **Equal weight, whole list**: all cash; cash $100,000
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: all cash; cash $100,000
  - next open: SPY 100%

## Strongest news signals

- **V** (Visa) news score +0.33
  - Visa wins China approval: Visa stock after-hours at EUR 353.58, plus 0.66 percent versus Xetra close _(ad-hoc-news.de; words +0.72)_
  - Buffett Successor Sold Visa Stock in Q1: Why That May Have Been an $823M Mistake _(Benzinga; words +0.00)_
  - Is Visa Stock Increasing Your Market Risk? _(unknown; words -0.15)_
- **UNH** (UnitedHealth) news score +0.30
  - Q3 2026: UnitedHealth’s Profits Soar as it Covers Fewer People, Pays Less for Care _(HEALTH CARE un-covered; words +0.64)_
  - QUICK SPARK: UnitedHealth Calls 2026 the Bottom for Medicaid Margins _(Benzinga; words +0.00)_
  - UnitedHealth Group Raises 2026 Outlook As Q3 Operating Earnings Rise To $6.6 Billion _(Pulse 2.0; words +0.34)_
- **META** (Meta) news score +0.15
  - Truist Raises Meta Platforms Stock Price Target to a Street-High of $1,000 Ahead of Q3 Earnings. Here’s Why _(TipRanks; words +0.00)_
  - Meta shares rise for a second straight day as new AI model family impresses _(CNBC; words +0.34)_
  - Cathie Wood sells Meta shares after Zuckerberg's big AI launch _(unknown; words +0.20)_
- **JPM** (JPMorgan) news score -0.12
  - CRH (NYSE:CRH) Stock Rating Reaffirmed as "Overweight" by JPMorgan Chase & Co. _(MarketBeat; words +0.38)_
  - JPMorgan Earnings: Solid Results Despite Capital Markets Softening _(Morningstar; words +0.00)_
  - Prediction: JPMorgan Chase Raises Its Dividend Again in 2027 _(unknown; words +0.00)_
- **AAPL** (Apple) news score +0.11
  - Apple: Is the Walled Garden Now Also the Walled Living Room? _(Morningstar; words +0.00)_
  - Why Apple Hospitality REIT (APLE) Is Getting Attention Today _(Simply Wall Street; words +0.00)_
  - Apple Hits Fresh All-Time High _(unknown; words +0.46)_
- **COST** (Costco) news score +0.10
  - Costco (COST) Stock Could Be 21% Above Fair Value Despite Strong September Sales _(Simply Wall Street; words +0.34)_
  - Costco Wholesale Corporation $COST Stock Purchased by Jericho Financial LLP _(MarketBeat; words +0.00)_
  - 8 New Costco Food Finds Shoppers Should Look for This October _(https://docksiderestaurant.com.au/; words +0.00)_

See `docs/index.html` for the chart and full tables.
