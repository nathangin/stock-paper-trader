# Paper trading report

_Through the close on **2026-11-11**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $99,665 | -0.34% | +1.66% | +1.80% | -8.23% | 34 | 51.8% ± 5.4 (334) | Too early to tell (21/60 days) |
| Hybrid (news + momentum) | $98,030 | -1.97% | +0.03% | +0.16% | -4.65% | 22 | 48.6% ± 5.2 (350) | Too early to tell (21/60 days) |
| News (word-list sentiment) | $104,432 | +4.43% | +6.43% | +6.56% | -5.49% | 19 | 49.8% ± 6.2 (247) | Too early to tell (21/60 days) |
| Momentum (prices only) | $97,746 | -2.25% | -0.25% | -0.12% | -4.62% | 21 | 46.5% ± 5.0 (387) | Too early to tell (21/60 days) |
| Equal weight, whole list | $97,868 | -2.13% | -0.13% | – | -6.34% | 22 | – |  |
| Buy & hold SPY | $98,001 | -2.00% | – | – | -5.46% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 334 | 51.8% | 50.9% | +18.8 bp | +0.016 (21) |
| Hybrid (news + momentum) | 350 | 48.6% | 50.3% | +16.1 bp | -0.018 (21) |
| News (word-list sentiment) | 247 | 49.8% | 50.6% | +29.3 bp | +0.044 (21) |
| Momentum (prices only) | 387 | 46.5% | 51.4% | +1.5 bp | -0.028 (21) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AMD (39.30 sh), COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh); cash $0
  - next open: AMD 20%, COST 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $36
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AMD (40.58 sh), AVGO (57.24 sh), COST (18.46 sh), LLY (14.58 sh), WMT (168.69 sh); cash $0
  - next open: AAPL 20%, AMD 20%, AVGO 20%, COST 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.34 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $10
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **AMD** (AMD) news score +0.22
  - AMD Shares Climb as UBS Flags 31% Surge in Server CPU Shipments _(BigGo Finance; words +0.80)_
  - AMD Stock Surges as UBS Reports 31% Jump in Server CPU Shipments _(Coinpaper; words +0.85)_
  - Nvidia stock plunges 8.6%, but AMD and Broadcom rally. Which chip stocks are worth buying? _(investingLive; words +0.29)_
- **NVDA** (Nvidia) news score -0.20
  - Nvidia shares fall on reports board may oust CEO Jensen Huang _(unknown; words -0.34)_
  - CRWV Stock Eyes Best Week Since Nvidia’s Stake Reveal — Is Debt Scare Hiding A Bargain? Morningstar Thinks So _(unknown; words +0.64)_
  - Michael Burry Says Nvidia Earnings Will Be 'Great' — So Why Is He Telling NVDA Bulls To 'Get Out'? _(unknown; words +0.00)_
- **AAPL** (Apple) news score +0.15
  - Apple stock reaches a new high of $355.63, surpassing NVIDIA in market capitalization. _(KuCoin; words +0.38)_
  - AAPL, GOOG Stocks Gain Overnight As NVDA Slides: Are Retail Investors Rotating Into Traditional Tech Amid Leadership Turmoil? _(unknown; words -0.05)_
  - Why Did AAPL, XERS, ZETA Stocks Jump To 52-Week Highs Today? _(unknown; words +0.46)_
- **COST** (Costco) news score +0.14
  - Costco announces record $13.3 billion special dividend: is the stock a buy? _(Invezz; words +0.38)_
  - Cramer Says Tito’s Refused Costco on Price and Kirkland Made Vodka for Half _(unknown; words +0.00)_
  - Costco's $30 special dividend could cover your membership _(moneywise.com; words +0.00)_
- **WMT** (Walmart) news score +0.13
  - Walmart stock at EUR 113.95, up 1.63% before Xetra open _(ad-hoc-news.de; words +0.00)_
  - Walmart (WMT) Set to Post Quarterly Earnings on Thursday _(MarketBeat; words +0.00)_
  - Walmart Q3 earnings due Nov 19 amid hopes for r... _(Pluang; words +0.00)_
- **BA** (Boeing) news score -0.11
  - Embraer In Buy Zone After Earnings. Here's How Boeing, Airbus Compare. _(unknown; words +0.00)_
  - “Staying Close to the Work.” Boeing Stock (NYSE:BA) Ticks Down as Safety Inspectors Call for More Contact With Factory Floor _(TipRanks; words +0.00)_
  - “Staying Close to the Work.” Boeing Stock (NYSE:BA) Ticks Down as Safety Chief Calls for More Contact With Factory Floor _(TipRanks; words +0.00)_

See `docs/index.html` for the chart and full tables.
