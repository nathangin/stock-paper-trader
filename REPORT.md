# Paper trading report

_Through the close on **2026-10-14**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,117 | +0.12% | +0.85% | +0.49% | +0.00% | 5 | 46.7% ± 25.2 (15) | Too early to tell (1/60 days) |
| Hybrid (news + momentum) | $98,277 | -1.72% | -0.99% | -1.35% | -1.72% | 5 | 47.1% ± 23.7 (17) | Too early to tell (1/60 days) |
| News (word-list sentiment) | $99,831 | -0.17% | +0.57% | +0.20% | -0.17% | 3 | 41.7% ± 27.9 (12) | Too early to tell (1/60 days) |
| Momentum (prices only) | $98,277 | -1.72% | -0.99% | -1.35% | -1.72% | 5 | 35.0% ± 20.9 (20) | Too early to tell (1/60 days) |
| Equal weight, whole list | $99,627 | -0.37% | +0.36% | – | -0.37% | 20 | – |  |
| Buy & hold SPY | $99,264 | -0.74% | – | – | -0.74% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 15 | 46.7% | 53.3% | +19.2 bp | +0.180 (1) |
| Hybrid (news + momentum) | 17 | 47.1% | 52.9% | -29.1 bp | -0.152 (1) |
| News (word-list sentiment) | 12 | 41.7% | 50.0% | -21.4 bp | +0.050 (1) |
| Momentum (prices only) | 20 | 35.0% | 55.0% | -104.9 bp | -0.247 (1) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AAPL (58.01 sh), COST (20.77 sh), META (26.28 sh), UNH (52.29 sh), V (50.49 sh); cash $0
  - next open: AAPL 20%, COST 20%, META 20%, UNH 20%, V 20%
- **Hybrid (news + momentum)**: AMD (33.90 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **News (word-list sentiment)**: META (26.29 sh), UNH (52.32 sh), V (50.52 sh); cash $39,970
  - next open: META 20%, MSFT 20%, UNH 20%, V 20%
- **Momentum (prices only)**: AMD (33.90 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **UNH** (UnitedHealth) news score +0.28
  - UnitedHealth Group (UNH) Shares Rise 4.8% Amid Market Selloff on October 14, 2026 _(GuruFocus; words -0.24)_
  - UnitedHealth Is Earning More From Less (NYSE:UNH) _(Seeking Alpha; words +0.00)_
  - UnitedHealth Group (UNH) Could Be 22% Undervalued After 2026 Guidance Lift _(Simply Wall Street; words +0.00)_
- **V** (Visa) news score +0.26
  - Visa (NYSE:V) Stock Falls 1.3% - Time to Sell? _(MarketBeat; words -0.34)_
  - A New Visa Survey Says 56% of Americans Are Open to the Idea of Using Stablecoins. Here's What Crypto Investors Need to Know. _(The Motley Fool; words +0.00)_
  - Visa (V) Benefits from High Margins with Minimal Credit Exposure _(unknown; words +0.00)_
- **MSFT** (Microsoft) news score +0.17
  - Microsoft Just Unveiled a Brand-New AI Chip. Could It Be the "Nvidia Killer" Everyone's Been Looking For? _(unknown; words +0.00)_
  - Microsoft's wild ride back to record highs in 1 chart — and the lessons learned _(CNBC; words +0.38)_
  - Microsoft (MSFT) Built a $100B Azure. Can It Outrun Its Own Spending? _(unknown; words +0.00)_
- **NFLX** (Netflix) news score -0.16
  - Netflix to Lay Off 1,000 Employees in Major Workforce Cuts _(LAmag; words -0.24)_
  - Netflix Stock Flatlines On Job Cuts, Subscriber Churn Data _(unknown; words -0.24)_
  - NFLX Stock Layoffs: What to Know About the Latest Netflix Job Cuts _(Barchart.com; words -0.57)_
- **XOM** (ExxonMobil) news score +0.12
  - ExxonMobil (NYSE:XOM) Stock Jumps 1.8% - Time to Buy? _(MarketBeat; words +0.46)_
  - Exxon Wants to Repeat Its Guyana Success in Trinidad. Should You Buy the Stock Now or Wait for the First Well? _(unknown; words +0.00)_
  - Exxon Mobil Holdings (XOM) Rises As Market Takes a Dip: Key Facts _(unknown; words +0.34)_
- **META** (Meta) news score +0.12
  - JPMorgan Launches Auto-Callable Market Linked Securities Featuring Dell and Meta Stocks Due October 2028 _(Kalkine Media; words +0.20)_
  - Gene Munster Flags Meta’s Muse As A Bigger Risk To Google Search Than ChatGPT _(unknown; words -0.15)_
  - Meta Platforms (NASDAQ:META) Shares Down 3.3% Following Analyst Downgrade _(MarketBeat; words -0.64)_

See `docs/index.html` for the chart and full tables.
