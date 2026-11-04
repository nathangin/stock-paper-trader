# Paper trading report

_Through the close on **2026-11-03**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $94,942 | -5.06% | -2.36% | -1.30% | -5.96% | 28 | 51.7% ± 6.3 (240) | Too early to tell (15/60 days) |
| Hybrid (news + momentum) | $96,683 | -3.32% | -0.61% | +0.44% | -4.65% | 18 | 48.8% ± 6.2 (248) | Too early to tell (15/60 days) |
| News (word-list sentiment) | $101,355 | +1.36% | +4.06% | +5.11% | -1.24% | 11 | 49.4% ± 7.4 (174) | Too early to tell (15/60 days) |
| Momentum (prices only) | $96,683 | -3.32% | -0.61% | +0.44% | -4.62% | 19 | 47.4% ± 5.9 (274) | Too early to tell (15/60 days) |
| Equal weight, whole list | $96,244 | -3.76% | -1.05% | – | -4.11% | 20 | – |  |
| Buy & hold SPY | $97,297 | -2.70% | – | – | -2.99% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 240 | 51.7% | 54.2% | +31.6 bp | +0.058 (15) |
| Hybrid (news + momentum) | 248 | 48.8% | 52.0% | +29.5 bp | +0.012 (15) |
| News (word-list sentiment) | 174 | 49.4% | 52.9% | +27.3 bp | +0.058 (15) |
| Momentum (prices only) | 274 | 47.4% | 51.1% | +20.5 bp | -0.007 (15) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: BA (108.55 sh), COST (18.85 sh), LLY (13.54 sh), V (46.08 sh), XOM (104.06 sh); cash $0
  - next open: BA 20%, COST 20%, LLY 20%, V 20%, XOM 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), LLY (11.85 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, LLY 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: LLY (14.58 sh), MSFT (37.54 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $480
  - next open: AMD 20%, LLY 20%, MSFT 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $8
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.21
  - AMD Has a PC Problem Just Like Intel: Chip Giant Warns of Weaker Demand as It Plans for a ‘Double-Digit’ Market Decline in 2027 _(unknown; words -0.85)_
  - AMD’s AI Boom Puts It On Track To Outsell Intel For The First Time – Analysts See More Room To Grow _(unknown; words +0.00)_
  - AMD EPS: Intel's Drag Makes No Sense _(unknown; words +0.00)_
- **AMD** (AMD) news score +0.21
  - U.S. stock futures pare losses as Dems sweep Congress; AMD rises _(Investing.com; words +0.00)_
  - AMD Stock Forecast for 2026, 2027, 2028–2030 and Beyond _(LiteFinance; words +0.00)_
  - Democrats sweep in US midterms; AMD shares surge, Brent eases, EICMA 2026 and more _(LinkedIn; words +0.64)_
- **DIS** (Disney) news score -0.16
  - Defensive stocks HAS MAT Disney _(Longbridge; words +0.00)_
  - Mckenna Grace Clarifies Headlines About Why She Won't Do 'Hyper Sexual Roles,' Says It's Not Because of Disney Princess Dream _(Just Jared; words +0.00)_
  - Form 4 Walt Disney: Brent Woodford (EVP, Control, Fin Plan & Tax) For: 2 November By Investing.com _(Investing.com India; words +0.00)_
- **AMZN** (Amazon) news score +0.12
  - Texas Goes Blue: What Gina Hinojosa's Win Means For AI Data Centers And Stocks Like MSFT, AMZN, GOOGL, CRWV _(unknown; words +0.29)_
  - AWS launches "Semarak AI Malaysia", a national program to bring AI tools to government officers, students, and local software companies _(unknown; words +0.20)_
  - Amazon's Cloud Boom Meets Its Capital Bill _(ad-hoc-news.de; words +0.00)_
- **AVGO** (Broadcom) news score +0.11
  - Broadcom ships a landmark 2nm AI chip and the market shrugs it off _(Startup Fortune; words +0.00)_
  - Marvell’s Lumentum Buy Threatens Broadcom’s AI Optics Lead, Says TrendForce _(Stocktwits; words +0.00)_
  - What Is Broadcom (AVGO) Changing In AI Security And Fraud Defense? _(unknown; words -0.76)_
- **XOM** (ExxonMobil) news score +0.07
  - ExxonMobil (NYSE:XOM) Stock Falls 1.2% - Time to Sell? _(MarketBeat; words -0.34)_
  - Here's How Much $100 Invested In ExxonMobil Holdings 5 Years Ago Would Be Worth Today _(Benzinga; words +0.00)_
  - Trump Says Iran “Wants a Settlement.” CEO Predicts Peace Sends Oil 40% Lower for Exxon, Chevron _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
