# Paper trading report

_Through the close on **2026-10-22**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,706 | +0.71% | +2.17% | +2.13% | -0.83% | 10 | 55.3% ± 9.1 (114) | Too early to tell (7/60 days) |
| Hybrid (news + momentum) | $96,466 | -3.53% | -2.07% | -2.11% | -3.53% | 7 | 52.7% ± 9.2 (112) | Too early to tell (7/60 days) |
| News (word-list sentiment) | $101,707 | +1.71% | +3.17% | +3.13% | -1.13% | 7 | 55.8% ± 10.5 (86) | Too early to tell (7/60 days) |
| Momentum (prices only) | $96,727 | -3.27% | -1.81% | -1.85% | -3.27% | 7 | 49.6% ± 8.8 (125) | Too early to tell (7/60 days) |
| Equal weight, whole list | $98,578 | -1.42% | +0.04% | – | -1.48% | 20 | – |  |
| Buy & hold SPY | $98,536 | -1.46% | – | – | -1.56% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 114 | 55.3% | 51.8% | +20.3 bp | +0.166 (7) |
| Hybrid (news + momentum) | 112 | 52.7% | 51.8% | +11.9 bp | +0.060 (7) |
| News (word-list sentiment) | 86 | 55.8% | 53.5% | +8.0 bp | +0.117 (7) |
| Momentum (prices only) | 125 | 49.6% | 52.0% | +0.6 bp | +0.014 (7) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (20.77 sh), LLY (16.07 sh), META (27.27 sh), V (50.49 sh), XOM (111.96 sh); cash $0
  - next open: COST 20%, LLY 20%, UNH 20%, V 20%
- **Hybrid (news + momentum)**: META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $0
  - next open: MSFT 20%, UNH 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **NFLX** (Netflix) news score -0.15
  - Cathie Wood Just Bought Netflix Stock. Should You Follow Her? _(unknown; words +0.00)_
  - Netflix Viewing Time Drops an Estimated 26%. A Bored Retiree Trades the Couch for a $40,000 Job That Could Boost His Social Security _(unknown; words -0.05)_
  - The One Chart That Explains Why Netflix Cleaned House _(The Entertainment Strategy Guy | Substack; words +0.00)_
- **LLY** (Eli Lilly) news score +0.12
  - Amgen vs. Eli Lilly: Does the GLP-1 Mania Make LLY Stock a Better Buy in 2026? _(unknown; words +0.00)_
  - What Does Eli Lilly (LLY) Mean To Signal With Its $5 Billion Richmond Build? _(unknown; words +0.00)_
  - Eli Lilly breaks ground on new Goochland facility as stock rises 3.4% _(Traders Union; words +0.34)_
- **XOM** (ExxonMobil) news score +0.11
  - ExxonMobil (XOM) Expected to Announce Earnings on Friday _(MarketBeat; words +0.00)_
  - ExxonMobil Stock And Oil Majors With The Most Riding On Crude Prices _(unknown; words +0.00)_
  - ExxonMobil (XOM) Joliet Refinery Shutdown Pushes Chicago Gasoline Prices Higher _(GuruFocus; words +0.00)_
- **V** (Visa) news score +0.09
  - Companies laying off staff this year include Meta, Amazon, and Visa — see the list _(unknown; words +0.00)_
  - Visa Partners Singapore Tourism Board to Strengthen Singapore's Global Destination Appeal _(unknown; words +0.00)_
  - Visa (NYSE:V) Stock Jumps 1.6% - Still a Buy? _(MarketBeat; words +0.46)_
- **UNH** (UnitedHealth) news score +0.08
  - Lobbying Update: $2,100,000 of UNITEDHEALTH GROUP INC lobbying was just disclosed _(Quiver Quantitative; words +0.00)_
  - UnitedHealthcare drops 30% of prior authorization requirements; more U.S. newborns are going without vitamin K; gaming addiction linked to elbow pain in medical students — Morning Medical Update _(Medical Economics; words -0.34)_
  - UnitedHealth (NYSE:UNH) Medical Cost Trends Draw Attention Across Managed Care _(Kalkine Media; words +0.00)_
- **AMZN** (Amazon) news score +0.08
  - Companies laying off staff this year include Meta, Amazon, and Visa — see the list _(unknown; words +0.00)_
  - Amazon caught hackers probing a PHP flaw 4 days before the fix _(unknown; words +0.00)_
  - Amazon employee sues, alleging company silenced her after she reported rape by senior manager _(KING5.com; words +0.00)_

See `docs/index.html` for the chart and full tables.
