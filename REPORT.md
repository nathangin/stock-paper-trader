# Paper trading report

_Through the close on **2026-11-12**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,675 | +0.67% | +3.02% | +2.56% | -8.23% | 35 | 52.4% ± 5.2 (349) | Too early to tell (22/60 days) |
| Hybrid (news + momentum) | $97,592 | -2.41% | -0.06% | -0.52% | -4.65% | 22 | 49.3% ± 5.1 (365) | Too early to tell (22/60 days) |
| News (word-list sentiment) | $106,956 | +6.96% | +9.30% | +8.84% | -5.49% | 21 | 50.8% ± 6.1 (258) | Too early to tell (22/60 days) |
| Momentum (prices only) | $97,298 | -2.70% | -0.36% | -0.82% | -4.62% | 21 | 47.3% ± 4.9 (406) | Too early to tell (22/60 days) |
| Equal weight, whole list | $98,115 | -1.88% | +0.46% | – | -6.34% | 22 | – |  |
| Buy & hold SPY | $97,654 | -2.35% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 349 | 52.4% | 51.0% | +23.9 bp | +0.030 (22) |
| Hybrid (news + momentum) | 365 | 49.3% | 50.1% | +19.6 bp | -0.006 (22) |
| News (word-list sentiment) | 258 | 50.8% | 50.4% | +36.0 bp | +0.071 (22) |
| Momentum (prices only) | 406 | 47.3% | 51.5% | +3.7 bp | -0.020 (22) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (35.46 sh), COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh); cash $2,184
  - next open: AMD 20%, COST 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $36
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AAPL (58.88 sh), AMD (40.58 sh), AVGO (57.24 sh), COST (18.46 sh), WMT (168.69 sh); cash $0
  - next open: AAPL 20%, AMD 20%, AVGO 20%, COST 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.34 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $14
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **AMD** (AMD) news score +0.21
  - Lisa Su Named CEO of the Year as AMD Shares Surge 158% This Year, Market Cap Briefly Tops $1 Trillion _(BigGo Finance; words +0.85)_
  - AMD Stock Upgraded as Nvidia Faces Leadership Crisis _(KuCoin; words +0.64)_
  - Why Are Advanced Micro Devices (AMD) Shares Drawing Fresh AI Attention? _(unknown; words +0.00)_
- **NVDA** (Nvidia) news score -0.19
  - Nvidia CEO Jensen Huang resigns: Is the stock now a 50% bargain? _(unknown; words -0.38)_
  - Asia’s Stock Rebound Fades as Nvidia Uncertainty Lingers _(WSJ; words +0.38)_
  - US lawmakers summon Nvidia ex-CEO after affair with suspected spy _(unknown; words +0.00)_
- **LLY** (Eli Lilly) news score +0.16
  - Eli Lilly and Company stock at EUR 1,298.20, down 0.90% _(ad-hoc-news.de; words +0.00)_
  - Eli Lilly Shoots To New High, Leads 9 To Best Stock Lists _(Investor's Business Daily; words +0.38)_
  - Eli Lilly Launches $3.5B Manufacturing Facility for Weight Loss Drugs, Ticker LLY _(GuruFocus; words -0.10)_
- **AAPL** (Apple) news score +0.16
  - Apple stock slips to EUR 321.48, down 0.58 percent premarket _(ad-hoc-news.de; words -0.29)_
  - Apple (AAPL) Following Record Results Has Its Fair Value Back In Focus _(Simply Wall St; words +0.38)_
  - Why Emerging-Market Investors Buy NVIDIA Before Apple _(Business Upturn; words +0.00)_
- **COST** (Costco) news score +0.16
  - Costco executive vice president Teresa Jones sells $975,557 in shares By Investing.com _(Investing.com UK; words +0.00)_
  - Why Did AAPL, COST, JNJ Stocks Hit 52-Week Highs Today? _(unknown; words +0.00)_
  - Dear Costco Stock Fans, Mark Your Calendars for December 4 _(Barchart.com; words +0.00)_
- **INTC** (Intel) news score -0.13
  - Investor Warns Nvidia Stock May Follow Intel's Post-CEO Resignation Decline _(KuCoin; words -0.69)_
  - ‘History May Repeat Itself’: Investor Warns Nvidia Stock Could Follow Intel’s Troubling Path _(TipRanks; words -0.46)_
  - Intel: Upgrading To 'Strong Buy' After The 38% Sell-Off (NASDAQ:INTC) _(Seeking Alpha; words -0.24)_

See `docs/index.html` for the chart and full tables.
