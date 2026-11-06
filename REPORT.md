# Paper trading report

_Through the close on **2026-11-05**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $92,648 | -7.35% | -1.90% | -1.07% | -8.23% | 30 | 51.8% ± 5.9 (272) | Too early to tell (17/60 days) |
| Hybrid (news + momentum) | $96,097 | -3.90% | +1.55% | +2.38% | -4.65% | 20 | 49.3% ± 5.8 (282) | Too early to tell (17/60 days) |
| News (word-list sentiment) | $97,412 | -2.59% | +2.87% | +3.70% | -5.49% | 15 | 49.5% ± 7.0 (194) | Too early to tell (17/60 days) |
| Momentum (prices only) | $96,206 | -3.79% | +1.66% | +2.49% | -4.62% | 19 | 47.8% ± 5.5 (312) | Too early to tell (17/60 days) |
| Equal weight, whole list | $93,716 | -6.28% | -0.83% | – | -6.34% | 21 | – |  |
| Buy & hold SPY | $94,543 | -5.46% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 272 | 51.8% | 54.8% | +26.9 bp | +0.051 (17) |
| Hybrid (news + momentum) | 282 | 49.3% | 53.5% | +35.1 bp | +0.038 (17) |
| News (word-list sentiment) | 194 | 49.5% | 54.1% | +25.8 bp | +0.068 (17) |
| Momentum (prices only) | 312 | 47.8% | 52.2% | +25.5 bp | +0.025 (17) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (39.30 sh), BA (108.55 sh), COST (18.85 sh), LLY (13.54 sh), V (46.08 sh); cash $0
  - next open: AMD 20%, BA 20%, COST 20%, LLY 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AMD (40.58 sh), LLY (14.58 sh), MSFT (37.54 sh), WMT (168.69 sh), XOM (117.62 sh); cash $0
  - next open: AMD 20%, COST 20%, LLY 20%, MSFT 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.34 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **TSLA** (Tesla) news score -0.25
  - SpaceX, Tesla Shares Tumble As US Midterm Results Trigger Tech Stock Sell-Off _(News Mobile; words -0.87)_
  - Tesla Shares Rise 0.58% After Hours - Tesla (NASDAQ:TSLA) _(Benzinga; words +0.34)_
  - Ross Gerber Says Tesla's 'Good Old Days' Ended When Elon Musk Started Selling Shares to Buy Twitter _(Benzinga; words +0.00)_
- **INTC** (Intel) news score -0.22
  - Intel's $600 Million Israel Setback and a Halved 2027 EPS Forecast Test the Recovery Story _(ad-hoc-news.de; words +0.00)_
  - Intel (INTC) Brings Hardware Backed Security To EdgeAI And Sharpens Xeon AI Case _(unknown; words +0.00)_
  - Intel (NASDAQ:INTC) Shares Down 10.3% - Should You Sell? _(MarketBeat; words +0.00)_
- **COST** (Costco) news score +0.17
  - Costco Stock And 2 Consumer Staples Names Facing A Margin Test _(Simply Wall St; words +0.00)_
  - JPMorgan Chase & Co. Forecasts Strong Price Appreciation for Costco Wholesale (NASDAQ:COST) Stock _(MarketBeat; words +0.34)_
  - Costco Store Inventory API “Scavio” Now Available for Resellers and Developers Tracking Warehouse Prices and Stock _(USA Today; words +0.00)_
- **NVDA** (Nvidia) news score -0.15
  - NVIDIA (NASDAQ:NVDA) Stock Sale Disclosed by Rep. Daniel Meuser _(MarketBeat; words +0.00)_
  - NVDAB Plunges As AI Regulatory Fears Drive Nvidia Stock Selloff _(MarketForces Africa; words -0.96)_
  - Nvidia, AMD, Meta, other tech stocks nosedive as Democratic sweep prompts AI slowdown fears _(The Economic Times; words -0.66)_
- **WMT** (Walmart) news score +0.15
  - Walmart Bike Racks - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.38)_
  - Walmart Danskin Women's Tops - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.72)_
  - Walmart Casas De Barbie - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.38)_
- **AVGO** (Broadcom) news score -0.12
  - Prediction: November Will Be a Huge Month for Broadcom _(unknown; words +0.00)_
  - Broadcom's AI Build-Out Meets Its Political and Financial Stress Test _(ad-hoc-news.de; words +0.00)_
  - Nvidia or Broadcom: Cathie Wood Buys $45.9M of One AI Stock, Sells $119.7M of the Other _(TipRanks; words +0.00)_

See `docs/index.html` for the chart and full tables.
