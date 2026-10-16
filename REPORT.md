# Paper trading report

_Through the close on **2026-10-16**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,420 | +0.42% | +1.98% | +1.62% | -0.53% | 5 | 57.4% ± 14.1 (47) | Too early to tell (3/60 days) |
| Hybrid (news + momentum) | $97,478 | -2.52% | -0.97% | -1.32% | -2.52% | 7 | 50.0% ± 13.9 (50) | Too early to tell (3/60 days) |
| News (word-list sentiment) | $99,890 | -0.11% | +1.45% | +1.09% | -1.13% | 5 | 51.4% ± 16.6 (35) | Too early to tell (3/60 days) |
| Momentum (prices only) | $96,729 | -3.27% | -1.72% | -2.07% | -3.27% | 5 | 44.4% ± 13.3 (54) | Too early to tell (3/60 days) |
| Equal weight, whole list | $98,802 | -1.20% | +0.36% | – | -1.26% | 20 | – |  |
| Buy & hold SPY | $98,445 | -1.56% | – | – | -1.56% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 47 | 57.4% | 51.1% | +58.8 bp | +0.300 (3) |
| Hybrid (news + momentum) | 50 | 50.0% | 52.0% | +14.4 bp | +0.089 (3) |
| News (word-list sentiment) | 35 | 51.4% | 51.4% | +30.0 bp | +0.168 (3) |
| Momentum (prices only) | 54 | 44.4% | 51.9% | -30.9 bp | +0.011 (3) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AAPL (58.01 sh), COST (20.77 sh), META (26.28 sh), UNH (52.29 sh), V (50.49 sh); cash $0
  - next open: AAPL 20%, COST 20%, META 20%, V 20%, XOM 20%
- **Hybrid (news + momentum)**: META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: META 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: META (26.29 sh), MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh), WMT (168.69 sh); cash $0
  - next open: META 20%, MSFT 20%, UNH 20%, V 20%, WMT 20%
- **Momentum (prices only)**: AMD (33.90 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **WMT** (Walmart) news score +0.20
  - Walmart (NASDAQ:WMT) EVP Sells $575,000.00 in Stock _(MarketBeat; words +0.00)_
  - Walmart Insider Sold Shares Worth $349,751, According to a Recent SEC Filing _(www.marketscreener.com; words +0.00)_
  - Walmart (WMT) executive sells 1,600 and 1,300 shares under a trading plan _(Stock Titan; words +0.00)_
- **XOM** (ExxonMobil) news score +0.20
  - Exxon sees higher refining margins adding $4.5B to Q3 earnings (XOM:NYSE) _(Seeking Alpha; words +0.00)_
  - ExxonMobil (NYSE:XOM) Shares Climb 2.5% After Analyst Upgrade _(MarketBeat; words +0.80)_
  - Exxon Mobil's Q3 earnings boosted by $4.5B refi... _(Pluang; words +0.00)_
- **COST** (Costco) news score +0.15
  - Costco Wholesale (NASDAQ:COST) Stock Price Up 1.1% After Analyst Upgrade _(MarketBeat; words +0.64)_
  - Costco (COST) Rises As Market Takes a Dip: Key Facts _(unknown; words +0.34)_
  - Top Analyst Reports for Costco, Walt Disney & Marriott _(unknown; words +0.00)_
- **V** (Visa) news score +0.15
  - Visa Stock Charges To A Record High, Leads 47 New to IBD Best Stock Lists _(Investor's Business Daily; words +0.38)_
  - Coca-Cola, Visa and Mastercard Hit Records as Investors Rotate Out of Chip Stocks _(unknown; words +0.00)_
  - Visa Stock Is Up 11% in October While Earnings Estimates Stood Still. Here’s What October 27 Has to Prove _(unknown; words +0.00)_
- **NFLX** (Netflix) news score -0.14
  - Netflix Scrambles to Rewrite Its Narrative With Layoffs and a Sudden Firing _(The New York Times; words -0.38)_
  - Netflix (NASDAQ:NFLX) Stock Price Down 2.9% on Analyst Downgrade _(MarketBeat; words -0.64)_
  - Here’s How Much Traders See Netflix Stock Moving After Earnings _(unknown; words +0.00)_
- **LLY** (Eli Lilly) news score +0.13
  - Market Expectation Breaker; Apple, Eli Lilly, Cheesecake Factory In Focus _(Investor's Business Daily; words +0.00)_
  - Eli Lilly buys about $12.3M in TRex Bio (TRXB) IPO shares, adding to its holdings. _(Stock Titan; words +0.00)_
  - Forget Zepbound: 3 Newer Drugs That Could Power Eli Lilly's Next Leg Higher _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
