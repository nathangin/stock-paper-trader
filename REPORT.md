# Paper trading report

_Through the close on **2026-11-04**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $95,863 | -4.14% | -3.04% | -2.09% | -5.96% | 28 | 52.0% ± 6.1 (256) | Too early to tell (16/60 days) |
| Hybrid (news + momentum) | $97,770 | -2.23% | -1.13% | -0.18% | -4.65% | 20 | 49.6% ± 6.0 (264) | Too early to tell (16/60 days) |
| News (word-list sentiment) | $103,070 | +3.07% | +4.17% | +5.12% | -1.24% | 14 | 50.3% ± 7.2 (183) | Too early to tell (16/60 days) |
| Momentum (prices only) | $97,927 | -2.07% | -0.98% | -0.03% | -4.62% | 19 | 47.8% ± 5.7 (293) | Too early to tell (16/60 days) |
| Equal weight, whole list | $97,954 | -2.05% | -0.95% | – | -4.11% | 20 | – |  |
| Buy & hold SPY | $98,904 | -1.10% | – | – | -2.99% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 256 | 52.0% | 52.3% | +31.5 bp | +0.053 (16) |
| Hybrid (news + momentum) | 264 | 49.6% | 50.8% | +31.8 bp | +0.013 (16) |
| News (word-list sentiment) | 183 | 50.3% | 51.9% | +31.5 bp | +0.057 (16) |
| Momentum (prices only) | 293 | 47.8% | 50.5% | +19.0 bp | +0.001 (16) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: BA (108.55 sh), COST (18.85 sh), LLY (13.54 sh), V (46.08 sh), XOM (104.06 sh); cash $0
  - next open: AMD 20%, BA 20%, COST 20%, LLY 20%, V 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, LLY 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: AMD (40.58 sh), LLY (14.58 sh), MSFT (37.54 sh), WMT (168.69 sh), XOM (117.62 sh); cash $0
  - next open: AMD 20%, LLY 20%, MSFT 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $8
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **AMD** (AMD) news score +0.21
  - AMD’s AI Deals with OpenAI and Meta: Stock Options Cause Billions in Charges Despite Record Revenue _(igor´sLAB; words +0.00)_
  - AMD Stock Jumped After Its Report. I'd Wait for a Lower Price to Buy. _(unknown; words +0.46)_
  - AMD CEO issues a strong warning for the 2027 PC market _(Yahoo Finance; words -0.15)_
- **MSFT** (Microsoft) news score +0.19
  - Microsoft declines Nscale Texas expansion ahead of $35 bln IPO - report _(unknown; words -0.10)_
  - Microsoft Stock Surges 6.7% as Q1 Earnings Beat Expectations, EPS Jumps 32% _(InteractiveCrypto; words +0.94)_
  - Why Did AAPL, MSFT, AMC Stocks Surge To 52-Week Highs? _(unknown; words +0.64)_
- **INTC** (Intel) news score -0.17
  - Intel Sinks 39% in a Week on a Weak Outlook. Its CEO Bought $9.7 Million of Stock _(TIKR.com; words -0.76)_
  - Intel stock slips to EUR 50.46, down 1.75% premarket _(ad-hoc-news.de; words -0.29)_
  - Intel Obeys Gravity: INTC Weak Guidance and Extended PC Slump Drag Stock Down _(FXLeaders; words -0.92)_
- **AMZN** (Amazon) news score +0.16
  - Amazon, Tesla and SpaceX join 56 firms opposing OKXICE tokenized stock trading _(CryptoRank; words +0.00)_
  - Amazon Trades at a Fraction of Costco's Valuation. Is the Discount Deserved? _(unknown; words +0.00)_
  - Amazon CEO Douglas Herrington sells $243,470 in stock _(Investing.com; words +0.00)_
- **AAPL** (Apple) news score +0.13
  - Why Did AAPL, MSFT, AMC Stocks Surge To 52-Week Highs? _(unknown; words +0.64)_
  - Why Did AAPL, MSFT, AMC Stocks Surge To 52-Week Highs Today? _(Stocktwits; words +0.64)_
  - Dow Jones Futures Rise, Techs Fall; Apple, Microsoft, Amazon Flash Buy Signals In Postelection Rally _(unknown; words +0.46)_
- **TSLA** (Tesla) news score -0.13
  - Amazon, Tesla and SpaceX join 56 firms opposing OKXICE tokenized stock trading _(CryptoRank; words +0.00)_
  - Tesla Bulls Could Get Burned? Gary Black Sees Trouble With SpaceX All-Stock Merger: Warns 24% Premium 'Ca _(Benzinga; words -0.46)_
  - Tesla Stock: $385 After Midterm Drop, Bull $420, Bear $350 _(FinanceFeeds; words -0.34)_

See `docs/index.html` for the chart and full tables.
