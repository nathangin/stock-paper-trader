# Paper trading report

_Through the close on **2026-10-13**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,000 | +0.00% | +0.00% | +0.00% | +0.00% | 0 | – | Too early to tell (0/60 days) |
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
| FinBERT reads the news (free AI) | 0 | – | – | – | – |
| Hybrid (news + momentum) | 0 | – | – | – | – |
| News (word-list sentiment) | 0 | – | – | – | – |
| Momentum (prices only) | 0 | – | – | – | – |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: all cash; cash $100,000
  - next open: AAPL 20%, COST 20%, META 20%, UNH 20%, V 20%
- **Hybrid (news + momentum)**: all cash; cash $100,000
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **News (word-list sentiment)**: all cash; cash $100,000
  - next open: META 20%, UNH 20%, V 20%
- **Momentum (prices only)**: all cash; cash $100,000
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: all cash; cash $100,000
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: all cash; cash $100,000
  - next open: SPY 100%

## Strongest news signals

- **V** (Visa) news score +0.34
  - 2 Financial Stocks to Buy That Berkshire Hathaway Kept While Selling Visa and Mastercard _(unknown; words +0.00)_
  - Visa (NYSE:V) Shares Climb 1.6% Following Analyst Upgrade _(MarketBeat; words +0.80)_
  - Visa wins China approval: Visa stock after-hours at EUR 353.58, plus 0.66 percent versus Xetra close _(ad-hoc-news.de; words +0.72)_
- **UNH** (UnitedHealth) news score +0.31
  - UNH Stock Outpaces S&P 500 In 2026, Eyes Best Year Since Pandemic — CFO Says Wall Street May Be Missing 2027 Upside _(unknown; words +0.38)_
  - UnitedHealth (UNH) Q3 2026 Earnings Call Transcript _(unknown; words +0.00)_
  - UnitedHealth vs. Johnson & Johnson: Which Stock Is the Better Buy After Q3 Earnings? _(Zacks Investment Research; words +0.00)_
- **META** (Meta) news score +0.17
  - Alphabet vs. Meta Platforms: Here's What Revenue Trends Tell Investors About These Media Giants Turned Artificial Intelligence Companies _(unknown; words +0.00)_
  - Meta Stock Jumps as New AI Models Put Its Comeback to the Test _(MEXC; words +0.46)_
  - Tech Futures Rise: Meta, AMD Lead 5 Buys; ASML, CPI Inflation Due _(Investor's Business Daily; words +0.34)_
- **MSFT** (Microsoft) news score +0.14
  - RBC Capital Sticks to Its Buy Rating for Microsoft (MSFT) _(The Globe and Mail; words +0.20)_
  - Microsoft (MSFT) Stock Hits A Record High: Here Is Why? _(TOP1markets; words +0.38)_
  - Microsoft hits first record in a year after US$1.4 trillion rally; shares soar 54% from June low _(The Business Times; words +0.93)_
- **AVGO** (Broadcom) news score -0.11
  - Broadcom CEO flags capital constraint; stock pre-market at EUR 318.93 _(ad-hoc-news.de; words +0.00)_
  - Broadcom CEO echoes Warren Buffett with warning for investors _(unknown; words -0.46)_
  - Broadcom Inc (AVGO) Shares Surge 0.7% -- What GF Score of 99 Tells Investors _(GuruFocus; words +0.64)_
- **AAPL** (Apple) news score +0.11
  - 100 Million Siri Users Paying $20 A Month Could Generate $24 Billion A Year For Apple, Analyst Says: 'Tha _(Benzinga; words +0.00)_
  - LG ELECTRONICS ANNOUNCES NEW SMART HOME ACCESSORIES, DESIGNED IN COLLABORATION WITH APPLE FOR THE APPLE HOME COLLECTION _(unknown; words +0.00)_
  - Would You Pay $20 A Month For Apple Siri? Analyst Says It Could Deliver $24B, Sees Smaller Boost From Smart Home Products _(unknown; words +0.29)_

See `docs/index.html` for the chart and full tables.
