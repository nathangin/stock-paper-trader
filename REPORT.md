# Paper trading report

_Through the close on **2026-10-21**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,678 | +0.68% | +0.96% | +0.70% | -0.83% | 9 | 55.7% ± 9.9 (97) | Too early to tell (6/60 days) |
| Hybrid (news + momentum) | $97,315 | -2.68% | -2.40% | -2.66% | -2.89% | 7 | 52.1% ± 10.0 (96) | Too early to tell (6/60 days) |
| News (word-list sentiment) | $100,832 | +0.83% | +1.12% | +0.86% | -1.13% | 7 | 57.7% ± 11.5 (71) | Too early to tell (6/60 days) |
| Momentum (prices only) | $97,720 | -2.28% | -1.99% | -2.26% | -3.27% | 7 | 47.7% ± 9.5 (107) | Too early to tell (6/60 days) |
| Equal weight, whole list | $99,977 | -0.02% | +0.26% | – | -1.26% | 20 | – |  |
| Buy & hold SPY | $99,714 | -0.29% | – | – | -1.56% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 97 | 55.7% | 50.5% | +47.5 bp | +0.166 (6) |
| Hybrid (news + momentum) | 96 | 52.1% | 52.1% | +27.7 bp | +0.021 (6) |
| News (word-list sentiment) | 71 | 57.7% | 54.9% | +48.3 bp | +0.145 (6) |
| Momentum (prices only) | 107 | 47.7% | 51.4% | -2.7 bp | -0.039 (6) |

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

- **UNH** (UnitedHealth) news score +0.25
  - UnitedHealth Group (UNH) Will Raise 2027 Medicare Costs For Seniors _(unknown; words +0.00)_
  - UnitedHealth's Earnings Jumped 60%. Is the Comeback Stock a Buy, Sell, or Hold? _(The Motley Fool; words +0.46)_
  - UnitedHealth Group stock: Piper Sandler lifts target to USD 504.00 _(AD HOC NEWS; words +0.54)_
- **NFLX** (Netflix) news score -0.18
  - Why Did NFLX, CMG, AVEX Stocks Crash To 52-Week Lows Today? _(unknown; words -0.76)_
  - Netflix Q3 2026: Underlying Profit Growth Hits 15%, but a $300 Million Ad Cut Sinks the Stock _(Techi; words -0.34)_
  - Netflix Stock: Sell-Off Creates A Buying Opportunity (NASDAQ:NFLX) _(Seeking Alpha; words -0.54)_
- **AMZN** (Amazon) news score +0.15
  - Egerton Capital boosts Amazon.com stake with 1.14M shares _(The Globe and Mail; words +0.29)_
  - Amazon vs. Target: Where Should Long-Term Investors Put Their Money? _(unknown; words +0.00)_
  - RBC Capital Remains a Buy on Amazon (AMZN) _(The Globe and Mail; words +0.00)_
- **LLY** (Eli Lilly) news score +0.15
  - RBC Capital Remains a Buy on Eli Lilly & Co (LLY) _(The Globe and Mail; words +0.00)_
  - Foghorn Therapeutics (FHTX) Stock Fair Value Moves Lower After Pipeline And Lilly Reset _(unknown; words +0.00)_
  - If You Invested $100 In Eli Lilly Stock 20 Years Ago, You Would Have This Much Today _(Benzinga; words +0.00)_
- **V** (Visa) news score +0.14
  - Is Visa Stock Riskier Than It Looks? _(unknown; words +0.00)_
  - Isbank stock: Isbank launches Visa transfers. Limits reach 5,000 USD for Isbank stock _(AD HOC NEWS; words +0.20)_
  - Here’s How Much You Would Have Made Owning Visa Stock In The Last 15 Years _(Benzinga; words +0.00)_
- **META** (Meta) news score +0.14
  - Meta’s Free Cash Flow Turned Negative. Its New Share Class Opens Another Funding Option. _(TIKR.com; words +0.00)_
  - Meta Stock Split Deal Will Keep Mark Zuckerberg In California Amid Billionaire Tax Threat _(Forbes; words +0.00)_
  - Meta Found a Way to Raise Money Without Handing Out More Votes _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
