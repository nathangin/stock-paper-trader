# Paper trading report

_Through the close on **2026-10-28**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $99,116 | -0.88% | -0.50% | +0.40% | -2.23% | 16 | 55.3% ± 7.5 (170) | Too early to tell (11/60 days) |
| Hybrid (news + momentum) | $95,353 | -4.65% | -4.26% | -3.36% | -4.65% | 12 | 47.5% ± 7.3 (179) | Too early to tell (11/60 days) |
| News (word-list sentiment) | $100,448 | +0.45% | +0.83% | +1.73% | -1.24% | 7 | 54.8% ± 8.7 (126) | Too early to tell (11/60 days) |
| Momentum (prices only) | $95,381 | -4.62% | -4.23% | -3.34% | -4.62% | 12 | 45.2% ± 6.9 (199) | Too early to tell (11/60 days) |
| Equal weight, whole list | $98,717 | -1.28% | -0.90% | – | -2.00% | 20 | – |  |
| Buy & hold SPY | $99,613 | -0.39% | – | – | -1.98% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 170 | 55.3% | 54.1% | +25.3 bp | +0.120 (11) |
| Hybrid (news + momentum) | 179 | 47.5% | 53.1% | +5.1 bp | -0.022 (11) |
| News (word-list sentiment) | 126 | 54.8% | 50.0% | +18.4 bp | +0.102 (11) |
| Momentum (prices only) | 199 | 45.2% | 51.8% | -8.3 bp | -0.066 (11) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (20.77 sh), INTC (194.95 sh), JPM (59.37 sh), LLY (16.07 sh), UNH (47.26 sh); cash $0
  - next open: AVGO 20%, COST 20%, INTC 20%, LLY 20%, UNH 20%
- **Hybrid (news + momentum)**: COST (16.49 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $0
  - next open: AVGO 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (149.24 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **BA** (Boeing) news score -0.25
  - Did ENPH, OPEN Stocks Hit 52-Week Lows? Enphase, Boeing Slide _(JournalArta; words -0.38)_
  - Analysts Offer Insights on Industrial Goods Companies: Boeing (BA) and Nordex (OtherNRDXF) _(The Globe and Mail; words +0.00)_
  - Why Did ENPH, OPEN, BA Stocks Slump To 52-Week Lows Today? _(unknown; words -0.54)_
- **GOOGL** (Alphabet) news score -0.21
  - Alphabet Inc. : RBC keeps its Buy rating _(marketscreener.com; words +0.20)_
  - Shares mixed after Google parent Alphabet's earnings disappoint _(unknown; words +0.00)_
  - Alphabet Stock $292 After Q3 Miss: -$9B Free Cash Flow _(FinanceFeeds; words -0.46)_
- **MSFT** (Microsoft) news score +0.21
  - Can Azure's AI boom drive Microsoft shares higher? _(The Economic Times; words +0.00)_
  - CoreWeave, neocloud stocks drop after Microsoft capex misses estimates (CRWV:NASDAQ) _(Seeking Alpha; words -0.87)_
  - Why Google stock fell while Microsoft rose after Q3 earnings _(FXStreet; words +0.00)_
- **AVGO** (Broadcom) news score +0.21
  - Broadcom Stock Is 29% Below Its Record. After Its New Anthropic Deal, I'd Consider Buying It a Little at a Time. _(The Motley Fool; words +0.38)_
  - Jim Cramer flags Broadcom as top long-term performer in latest stock picks _(Traders Union; words +0.00)_
  - Cramer's lightning round: 'Broadcom has been one of the greatest performers of all time' _(CNBC; words +0.00)_
- **V** (Visa) news score +0.18
  - Visa (NYSE:V) Stock Sold by Rep. Pete Sessions _(MarketBeat; words +0.00)_
  - Visa: 3 Key Takeaways for Long-Term Investors _(unknown; words +0.00)_
  - Visa's Stablecoin Volume Grew 10x in a Year: Which Stablecoins Benefit? _(unknown; words +0.00)_
- **TSLA** (Tesla) news score +0.18
  - Rep. Pete Sessions Sells Off Shares of Tesla, Inc. (NASDAQ:TSLA) _(MarketBeat; words +0.00)_
  - Tesla Is Flying in Europe, and We Aren't Talking About the Roadster -- 1 Big Concern Remains _(unknown; words -0.24)_
  - Elon Musk vs. Tesla? His Midterm Money Could Work Against His Own Cars _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
