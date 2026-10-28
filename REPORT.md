# Paper trading report

_Through the close on **2026-10-27**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $98,806 | -1.19% | -0.47% | +0.24% | -2.23% | 16 | 55.5% ± 7.8 (155) | Too early to tell (10/60 days) |
| Hybrid (news + momentum) | $95,429 | -4.57% | -3.84% | -3.13% | -4.57% | 11 | 48.8% ± 7.7 (162) | Too early to tell (10/60 days) |
| News (word-list sentiment) | $100,569 | +0.57% | +1.30% | +2.01% | -1.13% | 7 | 53.9% ± 9.1 (115) | Too early to tell (10/60 days) |
| Momentum (prices only) | $95,571 | -4.43% | -3.70% | -2.99% | -4.43% | 11 | 47.0% ± 7.3 (181) | Too early to tell (10/60 days) |
| Equal weight, whole list | $98,562 | -1.44% | -0.71% | – | -2.00% | 20 | – |  |
| Buy & hold SPY | $99,272 | -0.73% | – | – | -1.98% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 155 | 55.5% | 53.5% | +22.8 bp | +0.093 (10) |
| Hybrid (news + momentum) | 162 | 48.8% | 51.2% | +6.5 bp | -0.015 (10) |
| News (word-list sentiment) | 115 | 53.9% | 50.4% | +12.5 bp | +0.077 (10) |
| Momentum (prices only) | 181 | 47.0% | 50.8% | -4.3 bp | -0.061 (10) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (20.77 sh), INTC (194.95 sh), JPM (59.37 sh), LLY (16.07 sh), UNH (47.26 sh); cash $0
  - next open: COST 20%, INTC 20%, JPM 20%, LLY 20%, UNH 20%
- **Hybrid (news + momentum)**: COST (16.49 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $0
  - next open: MSFT 20%, UNH 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (149.24 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **BA** (Boeing) news score -0.29
  - Jim Cramer Says Boeing’s ‘Kitchen Sink’ Quarter May Have Reset Expectations Amid Stock Sell-Off, Production Woes _(Benzinga; words -0.83)_
  - Boeing: 3 Key Takeaways for Long-Term Investors _(The Motley Fool; words +0.00)_
  - Boeing Stock Price Forecast: Plunges Nearly 11% After Q3 Earnings, Stock Risks Falling Toward $130 _(TradingKey; words -0.85)_
- **AVGO** (Broadcom) news score +0.23
  - Broadcom Stock Price Forecast: $63 Billion AI Funding Supports Anthropic's Purchase of Broadcom Chips, Shares Poised to Return to $400 _(TradingKey; words +0.00)_
  - These Dividend-Paying Stocks Offer Notable AI Exposure: AVGO VRT _(unknown; words +0.00)_
  - Nasdaq Jumps to 26,477.81 as Broadcom, AMD and New AI Deals Lift Chip Stocks _(BBN Times; words +0.46)_
- **TSLA** (Tesla) news score +0.21
  - Tesla-SpaceX Merger Needs No Premium, Investor Says — But Floats $500 To Sway Angry Holders Missing Bigger Payoff _(unknown; words +0.00)_
  - Elon Musk Says Tesla Robotaxi Expansion to Miami, Tampa Beaches Is ‘Coming Soon’ After Ron DeSantis’ Call for Expansion _(unknown; words +0.46)_
  - TSLA Stock Is October’s Mag 7 King — But 2 Motorcycle Stocks Race Past Tesla Even As Chinese EV Stocks See Red _(unknown; words +0.00)_
- **NFLX** (Netflix) news score -0.14
  - Why Did NFLX, OPEN, WHR Stocks Tumble To 52-Week Lows Today? _(unknown; words -0.64)_
  - Bill Ackman Takes Another Swing At NFLX After Colossal 2022 Loss: 'Netflix Has Effectively Won The Streaming Wars' _(Stocktwits; words -0.29)_
  - What Does Netflix (NFLX) Leadership Shakeup Mean For Its Streaming Future? _(unknown; words +0.00)_
- **V** (Visa) news score +0.13
  - Visa (V) Q4 2026 Earnings Call Transcript _(unknown; words +0.00)_
  - Visa Inc. Stock 12‑Month Price Target Raised to $434.97, Implies 8% Upside _(TradingView; words +0.76)_
  - Card services provider Visa sees profit boost in fourth quarter _(Yahoo Finance; words +0.46)_
- **AMD** (AMD) news score +0.12
  - AMD CFO Delivers Bullish Update That Investors Will Want to Hear _(The Motley Fool; words +0.54)_
  - AMD to invest US$1 billion in Meta's stock sale as Helios racks enter testing _(digitimes; words +0.00)_
  - Cathie Wood Extends Archer, Joby Buying Spree; Ark Sells More AMD, Taiwan Semiconductor Shares _(TradingView; words +0.00)_

See `docs/index.html` for the chart and full tables.
