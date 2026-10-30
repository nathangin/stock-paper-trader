# Paper trading report

_Through the close on **2026-10-29**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,735 | +0.74% | +1.50% | +2.03% | -2.23% | 18 | 53.5% ± 7.2 (185) | Too early to tell (12/60 days) |
| Hybrid (news + momentum) | $96,578 | -3.42% | -2.65% | -2.13% | -4.65% | 13 | 48.7% ± 7.0 (195) | Too early to tell (12/60 days) |
| News (word-list sentiment) | $101,971 | +1.97% | +2.74% | +3.26% | -1.24% | 9 | 52.6% ± 8.4 (135) | Too early to tell (12/60 days) |
| Momentum (prices only) | $96,528 | -3.47% | -2.70% | -2.18% | -4.62% | 13 | 47.5% ± 6.6 (217) | Too early to tell (12/60 days) |
| Equal weight, whole list | $98,709 | -1.29% | -0.52% | – | -2.00% | 20 | – |  |
| Buy & hold SPY | $99,233 | -0.77% | – | – | -1.98% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 185 | 53.5% | 53.5% | +25.8 bp | +0.082 (12) |
| Hybrid (news + momentum) | 195 | 48.7% | 51.3% | +17.9 bp | +0.005 (12) |
| News (word-list sentiment) | 135 | 52.6% | 51.1% | +19.9 bp | +0.076 (12) |
| Momentum (prices only) | 217 | 47.5% | 50.7% | +8.5 bp | -0.027 (12) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AVGO (58.58 sh), COST (20.77 sh), INTC (194.95 sh), LLY (16.07 sh), UNH (47.26 sh); cash $401
  - next open: AVGO 20%, COST 20%, DIS 20%, LLY 20%, UNH 20%
- **Hybrid (news + momentum)**: COST (16.49 sh), MSFT (36.67 sh), V (50.49 sh), WMT (157.18 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: AVGO (59.57 sh), MSFT (37.54 sh), V (50.52 sh), WMT (168.69 sh), XOM (104.08 sh); cash $1,249
  - next open: AVGO 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (149.24 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: COST 20%, DIS 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.40
  - Intel Shares Fall 23% Following Earnings Beat: What Happened? _(thebull.com.au; words +0.15)_
  - U.S. stock futures sink, Nasdaq down 2% as Amazon, Intel earnings spark tech rout _(Investing.com; words -0.54)_
  - INTC: Intel Stock Plunges 24% as Weak Outlook Overshadows Strong Earnings Growth _(TradingView; words -0.60)_
- **GOOGL** (Alphabet) news score -0.31
  - Big Tech Capex Scorecard: Amazon Spends Over $77B In One Quarter — How It Stacks Up With MSFT, TSLA, GOOGL _(unknown; words +0.00)_
  - Transcript: Alphabet’s brutal day on the stock market _(Financial Times; words +0.00)_
  - Is AI Killing Google's Golden Goose? _(The Motley Fool; words +0.00)_
- **LLY** (Eli Lilly) news score +0.27
  - ServiceNow and Fortinet Sink 24% as Eli Lilly Leads Early Gainers _(24/7 Wall St.; words -0.54)_
  - Eli Lilly Lifts Revenue Outlook as Volume Surge Outpaces Price Erosion _(ad-hoc-news.de; words +0.82)_
  - Lilly's obesity drug strength fuels record rally, Wall Street optimism _(marketscreener.com; words +0.72)_
- **V** (Visa) news score +0.22
  - Visa (NYSE:V) Stock Jumps 2.4% Following Analyst Upgrade _(MarketBeat; words +0.85)_
  - Visa (V) Stock Could Be A Bargain On Record Revenue Growth _(Simply Wall St; words +0.85)_
  - Why Are Credit Card Stocks Mastercard (MA), Visa (V), and American Express (AXP) Up Today? _(TipRanks; words +0.00)_
- **BA** (Boeing) news score -0.22
  - Freedom Broker cuts Boeing stock price target on production concerns _(Investing.com; words -0.46)_
  - Boeing’s comeback hits another frustrating roadblock _(TheStreet; words +0.00)_
  - Boeing (BA) Sees Air Cargo Traffic Doubling By 2045 In New Forecast _(unknown; words +0.00)_
- **AMZN** (Amazon) news score -0.19
  - U.S. stock futures sink, Nasdaq down 2% as Amazon, Intel earnings spark tech rout _(Investing.com; words -0.54)_
  - Amazon shares sink 7% as AI spending fuels cash-burn concerns, overshadow cloud growth _(The Times of India; words -0.54)_
  - Amazon's After-Hours Drop Leaves It Below Wall Street's Lowest Price Target _(unknown; words -0.34)_

See `docs/index.html` for the chart and full tables.
