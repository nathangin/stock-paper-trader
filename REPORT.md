# Paper trading report

_Through the close on **2026-10-15**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,955 | +0.95% | +1.41% | +0.90% | +0.00% | 5 | 54.8% ± 17.5 (31) | Too early to tell (2/60 days) |
| Hybrid (news + momentum) | $98,325 | -1.68% | -1.22% | -1.73% | -1.72% | 5 | 45.5% ± 17.0 (33) | Too early to tell (2/60 days) |
| News (word-list sentiment) | $101,028 | +1.03% | +1.48% | +0.97% | -0.17% | 4 | 40.9% ± 20.5 (22) | Too early to tell (2/60 days) |
| Momentum (prices only) | $98,325 | -1.68% | -1.22% | -1.73% | -1.72% | 5 | 40.5% ± 15.8 (37) | Too early to tell (2/60 days) |
| Equal weight, whole list | $100,057 | +0.06% | +0.51% | – | -0.37% | 20 | – |  |
| Buy & hold SPY | $99,546 | -0.45% | – | – | -0.74% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 31 | 54.8% | 54.8% | +44.7 bp | +0.244 (2) |
| Hybrid (news + momentum) | 33 | 45.5% | 54.5% | -7.5 bp | -0.050 (2) |
| News (word-list sentiment) | 22 | 40.9% | 54.5% | +1.8 bp | +0.057 (2) |
| Momentum (prices only) | 37 | 40.5% | 51.4% | -49.2 bp | -0.159 (2) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AAPL (58.01 sh), COST (20.77 sh), META (26.28 sh), UNH (52.29 sh), V (50.49 sh); cash $0
  - next open: AAPL 20%, COST 20%, META 20%, UNH 20%, V 20%
- **Hybrid (news + momentum)**: AMD (33.90 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: META 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: META (26.29 sh), MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh); cash $19,940
  - next open: META 20%, MSFT 20%, UNH 20%, V 20%, WMT 20%
- **Momentum (prices only)**: AMD (33.90 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **UNH** (UnitedHealth) news score +0.27
  - Nike, UnitedHealth Share Gains Lead Dow's 529-Point Rally _(Moomoo; words +0.69)_
  - UnitedHealth Stock Moves Higher: What's Going On? _(TradingView; words +0.00)_
  - Unitedhealth Group Inc Stock (UNH) Moved Up by 3.77% on Oct 15: Drivers Behind the Movement _(TradingKey; words +0.00)_
- **V** (Visa) news score +0.27
  - Microsoft's Cyber Takedown and Visa Fight Take Center Stage as Stock Hovers Near Record _(ad-hoc-news.de; words +0.38)_
  - Visa Shares Near 52-Week High as Stablecoin Payments Expand _(Benzinga; words +0.46)_
  - Visa Stock Hits Fresh Record High – BMO Raises Price Target To $425 Ahead Of Earnings _(unknown; words +0.82)_
- **WMT** (Walmart) news score +0.24
  - Buy Walmart Stock (WMT) as the AI Trade Falters, Says Deutsche Bank _(TipRanks; words +0.00)_
  - Walmart Stock Climbs as Deutsche Bank Says It’s Time to Buy _(Investopedia; words +0.34)_
  - Why This Analyst Thinks Walmart Stock Is a Buy After Its Worst Day in 5 Years _(unknown; words +0.00)_
- **MSFT** (Microsoft) news score +0.13
  - Microsoft's Cyber Takedown and Visa Fight Take Center Stage as Stock Hovers Near Record _(ad-hoc-news.de; words +0.38)_
  - Tucuvi joins the Microsoft Pegasus Program to scale clinically governed AI Care Management across health systems _(unknown; words +0.00)_
  - Microsoft integrates OpenAI Dots agents into enterprise governance stack _(scanx.trade; words +0.00)_
- **NFLX** (Netflix) news score -0.10
  - Netflix is dealing with a generational streaming shift away from the living room _(unknown; words +0.00)_
  - Netflix (NFLX) Stock Rises Amid Heavy Options Activity Ahead of Earnings _(GuruFocus; words +0.34)_
  - Netflix Stock Is Down 40%. Can Q3 Earnings Spark a Comeback? _(Cabot Wealth Network; words +0.00)_
- **NVDA** (Nvidia) news score -0.10
  - Nvidia Stock NVDA Extends Toward $200 as ASML Warns of Chipmaking Capacity _(FXLeaders; words -0.46)_
  - Nvidia leads chip stocks lower as AI trade takes _(Yahoo Finance; words +0.00)_
  - CoreWeave Stock Snaps Back as Nvidia CEO Signals Support _(Benzinga; words +0.00)_

See `docs/index.html` for the chart and full tables.
