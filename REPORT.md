# Paper trading report

_Through the close on **2026-10-20**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,633 | +0.63% | +1.44% | +0.98% | -0.83% | 9 | 55.7% ± 11.0 (79) | Too early to tell (5/60 days) |
| Hybrid (news + momentum) | $97,107 | -2.89% | -2.09% | -2.54% | -2.89% | 7 | 51.2% ± 10.8 (82) | Too early to tell (5/60 days) |
| News (word-list sentiment) | $100,830 | +0.83% | +1.64% | +1.18% | -1.13% | 7 | 56.9% ± 12.7 (58) | Too early to tell (5/60 days) |
| Momentum (prices only) | $97,434 | -2.57% | -1.76% | -2.22% | -3.27% | 7 | 46.7% ± 10.3 (90) | Too early to tell (5/60 days) |
| Equal weight, whole list | $99,651 | -0.35% | +0.46% | – | -1.26% | 20 | – |  |
| Buy & hold SPY | $99,193 | -0.81% | – | – | -1.56% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 79 | 55.7% | 51.9% | +43.7 bp | +0.265 (5) |
| Hybrid (news + momentum) | 82 | 51.2% | 51.2% | +24.9 bp | +0.068 (5) |
| News (word-list sentiment) | 58 | 56.9% | 53.4% | +39.3 bp | +0.198 (5) |
| Momentum (prices only) | 90 | 46.7% | 51.1% | -5.4 bp | -0.001 (5) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (20.77 sh), LLY (16.07 sh), META (26.28 sh), V (50.49 sh), XOM (111.96 sh); cash $669
  - next open: COST 20%, LLY 20%, META 20%, V 20%, XOM 20%
- **Hybrid (news + momentum)**: META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: META 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $0
  - next open: MSFT 20%, UNH 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score +0.29
  - Intel Stock (NASDAQ:INTC) Notches Up as JPMorgan Changes its Mind _(TipRanks; words +0.00)_
  - Intel Stocks Rise With JPMorgan Upgrade and Margin Hurdle in Focus _(TradingView; words +0.80)_
  - Intel Stock Reverses Premarket Drop Ahead of October 29 Earnings After JPMorgan Upgrade _(FinanceFeeds; words +0.38)_
- **LLY** (Eli Lilly) news score +0.21
  - Here's What I'm Planning With My Eli Lilly Position _(The Globe and Mail; words +0.00)_
  - Eli Lilly Shares Set New Intraday Record at $1,311.21 on Oct. 20 _(www.tokenpost.com; words +0.38)_
  - Eli Lilly Clears Its Prior Peak at $1,283.66, Setting a Fresh 52-Week High _(24/7 Wall St.; words +0.46)_
- **AMZN** (Amazon) news score +0.19
  - Lobbying Update: $4,490,000 of AMAZON.COM SERVICES LLC lobbying was just disclosed _(Quiver Quantitative; words +0.00)_
  - SpaceX Can't Find Spare Nvidia, Google or Amazon Chips Despite Billions to Spend, Strategist Terms It 'Pretty Insane' _(unknown; words +0.00)_
  - Media reports: Amazon Web Services faces power shortages, leaving billions of NVIDIA chips gathering dust in warehouses _(富途牛牛; words +0.00)_
- **UNH** (UnitedHealth) news score +0.16
  - RBC Capital raises UnitedHealth stock price target to $498 on strong quarter _(Investing.com Nigeria; words +0.34)_
  - UnitedHealth Group Inc (UNH) Stock Up 3.0% and Still Undervalued -- GF Score: 84/100 _(GuruFocus; words +0.00)_
  - UnitedHealth Group rated Strong Buy with 33% up... _(Pluang; words +0.34)_
- **XOM** (ExxonMobil) news score +0.13
  - What Helmerich & Payne Stock's ExxonMobil Robotics Rollout Means For Shareholders _(Simply Wall Street; words +0.00)_
  - Which Dates Could Move Exxon Mobil Stock Most? _(unknown; words +0.00)_
  - What ExxonMobil Doubters Got Wrong _(Simply Wall Street; words +0.00)_
- **V** (Visa) news score +0.12
  - Visa stock at EUR 362.13 ahead of the Xetra open: payments network begins day _(AD HOC NEWS; words +0.00)_
  - Visa Closes at $406.57, Marking Back-to-Back 52-Week Highs _(24/7 Wall St.; words +0.00)_
  - How Is Visa (V) Turning Crypto And AI Payments Into Real World Use? _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
