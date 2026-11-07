# Paper trading report

_Through the close on **2026-11-06**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $93,745 | -6.26% | -1.09% | -0.46% | -8.23% | 31 | 50.7% ± 5.8 (286) | Too early to tell (18/60 days) |
| Hybrid (news + momentum) | $95,629 | -4.37% | +0.79% | +1.42% | -4.65% | 22 | 47.2% ± 5.6 (301) | Too early to tell (18/60 days) |
| News (word-list sentiment) | $98,507 | -1.49% | +3.67% | +4.30% | -5.49% | 17 | 47.6% ± 6.8 (206) | Too early to tell (18/60 days) |
| Momentum (prices only) | $95,825 | -4.17% | +0.99% | +1.62% | -4.62% | 19 | 46.1% ± 5.4 (330) | Too early to tell (18/60 days) |
| Equal weight, whole list | $94,206 | -5.79% | -0.63% | – | -6.34% | 22 | – |  |
| Buy & hold SPY | $94,838 | -5.16% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 286 | 50.7% | 54.5% | +19.2 bp | +0.019 (18) |
| Hybrid (news + momentum) | 301 | 47.2% | 53.5% | +22.7 bp | -0.006 (18) |
| News (word-list sentiment) | 206 | 47.6% | 54.4% | +18.5 bp | +0.028 (18) |
| Momentum (prices only) | 330 | 46.1% | 52.1% | +14.9 bp | -0.011 (18) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (39.30 sh), BA (108.55 sh), COST (18.85 sh), LLY (13.54 sh); cash $19,089
  - next open: BA 20%, COST 20%, LLY 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AMD (40.58 sh), COST (18.46 sh), LLY (14.58 sh), MSFT (37.54 sh), WMT (168.69 sh); cash $0
  - next open: AMD 20%, COST 20%, LLY 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.34 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **COST** (Costco) news score +0.18
  - Costco (COST) Brings Real Time Health Benefit Checkout To More Than 600 Warehouses _(unknown; words +0.00)_
  - Is Costco Wholesale (COST) Fully Valued As October Comparable Sales Jumped 11%? _(Simply Wall St; words +0.46)_
  - Costco Wholesale (NASDAQ:COST) Stock Falls 1.1% - Should You Sell? _(MarketBeat; words -0.34)_
- **WMT** (Walmart) news score +0.16
  - Walmart Boost Mobile Flip Phones - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.60)_
  - Walmart Dog Hats - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.38)_
  - Walmart Dash Stroller - Walmart wins big at 2025 BrandSpark Most Trusted Awards Canadian Grocer _(auroradesio.it; words +0.38)_
- **LLY** (Eli Lilly) news score +0.12
  - Cathie Wood-Led Ark Loads Up On GOOG, AMD, NVDA And Biotech Stocks — But Sells CRWV, AVGO, LLY _(unknown; words +0.00)_
  - Jim Cramer’s Charitable Trust Plans to Trim Cardinal Health and Eli Lilly _(www.tokenpost.com; words +0.00)_
  - Eli Lilly Is Much More Than a Weight-Loss Drug Company. Here's the Evidence _(The Globe and Mail; words +0.00)_
- **INTC** (Intel) news score -0.11
  - Intel Discloses $1.9B Classiq Deal Terms, With Up to $350M More at Stake _(BigGo Finance; words +0.00)_
  - Dell Sinks 16% in a Week on Intel’s PC Warning. Its CFO Already Saw “Minus Double Digit” _(unknown; words -0.80)_
  - Intel (NASDAQ:INTC) Stock Price Up 7.7% - Still a Buy? _(MarketBeat; words +0.00)_
- **NVDA** (Nvidia) news score -0.10
  - Cathie Wood-Led Ark Loads Up On GOOG, AMD, NVDA And Biotech Stocks — But Sells CRWV, AVGO, LLY _(unknown; words +0.00)_
  - A Retiree Who Bought 1,000 Nvidia Shares at $122 Just Watched Chips Have Their Worst Day Since 2020 _(unknown; words -0.64)_
  - Nvidia-backed Groq seeks $8 billion valuation in new funding round - Bloomberg _(unknown; words +0.00)_
- **AVGO** (Broadcom) news score -0.10
  - Cathie Wood-Led Ark Loads Up On GOOG, AMD, NVDA And Biotech Stocks — But Sells CRWV, AVGO, LLY _(unknown; words +0.00)_
  - Broadcom's AI Revenue Is Exploding. Here's What Investors Should Watch Next. _(unknown; words +0.00)_
  - Broadcom stock falls 22% amid political risks d... _(Pluang; words -0.34)_

See `docs/index.html` for the chart and full tables.
