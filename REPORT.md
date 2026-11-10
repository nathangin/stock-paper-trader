# Paper trading report

_Through the close on **2026-11-09**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $97,130 | -2.87% | +0.05% | +0.59% | -8.23% | 32 | 50.3% ± 5.7 (300) | Too early to tell (19/60 days) |
| Hybrid (news + momentum) | $97,018 | -2.98% | -0.06% | +0.48% | -4.65% | 22 | 47.5% ± 5.5 (318) | Too early to tell (19/60 days) |
| News (word-list sentiment) | $102,571 | +2.57% | +5.49% | +6.03% | -5.49% | 17 | 48.1% ± 6.7 (214) | Too early to tell (19/60 days) |
| Momentum (prices only) | $97,072 | -2.93% | -0.01% | +0.54% | -4.62% | 19 | 46.1% ± 5.2 (349) | Too early to tell (19/60 days) |
| Equal weight, whole list | $96,537 | -3.46% | -0.55% | – | -6.34% | 22 | – |  |
| Buy & hold SPY | $97,083 | -2.92% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 300 | 50.3% | 53.0% | +15.6 bp | +0.009 (19) |
| Hybrid (news + momentum) | 318 | 47.5% | 51.6% | +15.7 bp | -0.013 (19) |
| News (word-list sentiment) | 214 | 48.1% | 53.3% | +25.0 bp | +0.027 (19) |
| Momentum (prices only) | 349 | 46.1% | 50.1% | +6.3 bp | -0.019 (19) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (39.30 sh), BA (108.55 sh), COST (18.85 sh), LLY (13.54 sh), WMT (152.59 sh); cash $48
  - next open: AMD 20%, COST 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AMD (40.58 sh), COST (18.46 sh), LLY (14.58 sh), MSFT (37.54 sh), WMT (168.69 sh); cash $0
  - next open: AMD 20%, COST 20%, LLY 20%, MSFT 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.34 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **NVDA** (Nvidia) news score -0.27
  - Micron, FormFactor, Amkor, Teradyne, and Nvidia shares skyrocket, what you need to know _(unknown; words +0.00)_
  - Nvidia Faces Class Action Suit Over Huang Allegations; Senator Seeks Probe, Analyst Puts CEO Exit Odds At 15% _(unknown; words -0.85)_
  - Dow Jones Soars 1,132 Points As Amazon, Tesla Rally, But Nvidia Dives; CPI Inflation Report Next _(unknown; words +0.55)_
- **AMD** (AMD) news score +0.23
  - AMD vs Nvidia Chart: 94% Share, FSR 4.1 vs DLSS 5 [2026] _(shattered.io; words +0.00)_
  - The AI Trade Looks Like It's Falling Apart. AMD's Earnings Delivered a Reality Check. _(The Globe and Mail; words -0.34)_
  - Why did AMD stock jump 13% today? An Oppenheimer upgrade and a Google Cloud chip deal _(Nacionale; words +0.85)_
- **WMT** (Walmart) news score +0.18
  - Walmart Disney Cars Toys - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.38)_
  - UBS Re-Rates Walmart (NYSE: WMT) To 40x Forward Earnings As Alternative Revenue Streams Reshape Profit Story _(Foreign Policy Journal; words +0.20)_
  - Walmart Bicycles 16 Inch - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.38)_
- **GOOGL** (Alphabet) news score +0.17
  - If I Could Buy Just 1 Stock in November and Hold for 5 Years, It Would Be Alphabet _(unknown; words +0.00)_
  - Alphabet Almost Sets a Record No One Wants _(unknown; words +0.38)_
  - GetNinjas stock: Google Gemini adds service scheduling _(ad-hoc-news.de; words +0.00)_
- **LLY** (Eli Lilly) news score +0.16
  - Jim Cramer Says Eli Lilly “Is a $2 Trillion Stock” as It Nears Tesla’s Market Cap _(TIKR.com; words +0.00)_
  - Stocks extend recovery from Thursday's sell-off. Plus, new trial data from Lilly, J&J _(CNBC; words -0.54)_
  - Eli Lilly and Company (LLY) Stock: Surges 4.50% as Foundayo Delivers Positive Phase 3 Sleep Apnea Results _(Blockonomi; words +0.64)_
- **AAPL** (Apple) news score +0.15
  - Apple (AAPL) Stock Hits New 52-Week High _(24/7 Wall St.; words +0.46)_
  - Apple Issues $7.5 Billion in Senior Unsecured Notes _(TipRanks; words +0.00)_
  - Form 25-NSE Apple Inc. Filed by: Nasdaq Stock Market LLC _(StreetInsider; words +0.00)_

See `docs/index.html` for the chart and full tables.
