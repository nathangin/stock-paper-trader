# Paper trading report

_Through the close on **2026-11-20**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $94,828 | -5.17% | +5.86% | +5.72% | -8.23% | 42 | 53.4% ± 4.6 (444) | Too early to tell (28/60 days) |
| Hybrid (news + momentum) | $96,197 | -3.80% | +7.22% | +7.09% | -4.65% | 23 | 51.0% ± 4.6 (463) | Too early to tell (28/60 days) |
| News (word-list sentiment) | $102,345 | +2.34% | +13.37% | +13.23% | -5.49% | 25 | 51.4% ± 5.5 (315) | Too early to tell (28/60 days) |
| Momentum (prices only) | $95,351 | -4.65% | +6.38% | +6.24% | -4.65% | 23 | 48.8% ± 4.3 (514) | Too early to tell (28/60 days) |
| Equal weight, whole list | $89,112 | -10.89% | +0.14% | – | -10.94% | 25 | – |  |
| Buy & hold SPY | $88,972 | -11.03% | – | – | -11.03% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 444 | 53.4% | 55.4% | +26.6 bp | +0.063 (28) |
| Hybrid (news + momentum) | 463 | 51.0% | 55.5% | +25.1 bp | +0.058 (28) |
| News (word-list sentiment) | 315 | 51.4% | 54.3% | +27.9 bp | +0.075 (28) |
| Momentum (prices only) | 514 | 48.8% | 53.7% | +8.3 bp | +0.050 (28) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: DIS (157.02 sh), LLY (13.54 sh), WMT (152.59 sh); cash $38,540
  - next open: DIS 20%, LLY 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), WMT (157.18 sh); cash $18,498
  - next open: COST 20%, DIS 20%, LLY 20%, WMT 20%
- **News (word-list sentiment)**: COST (18.46 sh), DIS (172.58 sh), WMT (168.69 sh); cash $40,048
  - next open: COST 20%, DIS 20%, WMT 20%
- **Momentum (prices only)**: AAPL (52.40 sh), COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), WMT (147.22 sh); cash $0
  - next open: AAPL 20%, COST 20%, DIS 20%, LLY 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $9
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **AVGO** (Broadcom) news score -0.22
  - Data Center AI Chips Could Change the Winners: Broadcom and Marvell _(unknown; words +0.00)_
  - Broadcom, Intel, Nvidia, and Qualcomm stocks trade down, what you need to know _(The Globe and Mail; words +0.00)_
  - Broadcom falls 11% after analyst Ming-Chi Kuo says Google cut 2027 orders for its TPU chips _(MLQ.ai; words -0.50)_
- **NVDA** (Nvidia) news score -0.21
  - NVIDIA's Market Cap Evaporates, Equaling Amazon's, Amid Tech Selloff _(조선일보; words -0.54)_
  - Dow Jones Futures: Market Has Worst Week Since Covid Amid Nvidia, Anthropic. Does Fear Gauge Offer Hope? _(unknown; words -0.64)_
  - Here's Why Nvidia Stock Crashed on Friday _(The Globe and Mail; words +0.00)_
- **AMD** (AMD) news score -0.20
  - AMD Nov 2026 682.500 call (AMD261120C00682500) stock price, news, quote and history _(Yahoo Finance Singapore; words +0.00)_
  - Mets Owner Steve Cohen’s Fund Dumped Nearly All of Its AMD and Bet $1 Billion That Microsoft Is the Safer AI Stock. AMD Has Fallen 31% Since _(unknown; words -0.38)_
  - AMD Nov 2026 445.000 call (AMD261120C00445000) Stock Price, News, Quote & History _(Yahoo! Finance Canada; words +0.00)_
- **WMT** (Walmart) news score +0.13
  - Why did Walmart stock go up when the market fell? It rose Friday as investors left AI stocks _(Nacionale; words +0.00)_
  - Synchrony Financial Puts Lending Discipline First, Sees Walmart as Growth Opportunity _(unknown; words +0.24)_
  - Walmart has a surprising update on grocery prices _(unknown; words +0.00)_
- **COST** (Costco) news score +0.10
  - Unusual Volume Alert: Costco (NASDAQ:COST) Shares Rise in Active Trading _(kalkine.ca; words +0.34)_
  - Costco to pay $30 special dividend on Dec 4, do... _(Pluang; words +0.00)_
  - Tech Outages Drive Costco Surge: How Much Emergency Prep Should You Buy? _(MoneyLion; words +0.64)_
- **BA** (Boeing) news score -0.09
  - Boeing (NYSE:BA) Shares Down 2.9% - What's Next? _(MarketBeat; words +0.00)_
  - Boeing Stock (NYSE:BA) Slips, The Stingray is Heading to Carriers _(TipRanks; words -0.29)_
  - Boeing (BA) Faces Execution Pressure, Is The Stock Fully Valued? _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
