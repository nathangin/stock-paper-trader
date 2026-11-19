# Paper trading report

_Through the close on **2026-11-18**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $96,740 | -3.26% | +2.56% | +2.19% | -8.23% | 38 | 53.6% ± 4.8 (416) | Too early to tell (26/60 days) |
| Hybrid (news + momentum) | $97,734 | -2.27% | +3.55% | +3.18% | -4.65% | 22 | 50.8% ± 4.7 (429) | Too early to tell (26/60 days) |
| News (word-list sentiment) | $102,899 | +2.90% | +8.72% | +8.35% | -5.49% | 25 | 52.0% ± 5.7 (298) | Too early to tell (26/60 days) |
| Momentum (prices only) | $97,463 | -2.54% | +3.28% | +2.91% | -4.62% | 21 | 48.6% ± 4.5 (477) | Too early to tell (26/60 days) |
| Equal weight, whole list | $94,552 | -5.45% | +0.37% | – | -6.34% | 25 | – |  |
| Buy & hold SPY | $94,182 | -5.82% | – | – | -5.82% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 416 | 53.6% | 53.6% | +24.3 bp | +0.067 (26) |
| Hybrid (news + momentum) | 429 | 50.8% | 53.1% | +20.9 bp | +0.042 (26) |
| News (word-list sentiment) | 298 | 52.0% | 53.4% | +32.2 bp | +0.070 (26) |
| Momentum (prices only) | 477 | 48.6% | 51.2% | +5.4 bp | +0.032 (26) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh), XOM (117.83 sh); cash $650
  - next open: DIS 20%, LLY 20%, V 20%, WMT 20%, XOM 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $59
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: COST (18.46 sh), DIS (172.58 sh), WMT (168.69 sh); cash $40,048
  - next open: COST 20%, DIS 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $23
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **UNH** (UnitedHealth) news score -0.24
  - UnitedHealth Group stock slips to EUR 319.00, down 3.04% _(ad-hoc-news.de; words -0.29)_
  - UnitedHealth stock falls 10.21% on Medicare audit fears _(finchannel; words -0.64)_
  - Nasdaq, Dow, S&P 500 Futures Climb Ahead Of Anthropic’s Record Debut: SLS, GLD, TTWO, UNH In Focus _(unknown; words +0.64)_
- **INTC** (Intel) news score -0.24
  - NVDA, INTC Stocks Ease Post 5-Day Rout: After Meeting Xi Jinping, Trump Says Nvidia Blackwell Chips Could Reach China Within 2-3 Years _(unknown; words +0.00)_
  - Intel Stock And The Chipmaking Picks Investors May Be Missing _(Yahoo Finance Singapore; words +0.00)_
  - Intel's Foundry Business Scores Double Win: First External Customer Signs for 18A-P, Microsoft Adopts EMIB Packaging _(BigGo Finance; words +0.29)_
- **DIS** (Disney) news score +0.21
  - Why Did DIS, TGT, ASO Stocks Surge To 52-Week Highs Today? _(unknown; words +0.64)_
  - Why is Disney stock up 4.2% today? _(Traders Union; words +0.00)_
  - Disney Stock Rises 3.2% Intraday to $122.28 _(24/7 Wall St.; words +0.34)_
- **NFLX** (Netflix) news score -0.11
  - Netflix trades near 16 times earnings after a 50% slide from its peak _(Startup Fortune; words -0.57)_
  - Josh Brown Says Netflix Trades at 16 Times Next Year’s Earnings After a 50% Drop. Is It a Buy? _(unknown; words -0.34)_
  - Rep. Byron Donalds Sells Netflix Stock for Loss: Here’s What He’s Buying Instead _(TradingView; words -0.29)_
- **META** (Meta) news score -0.10
  - Meta Platforms, Inc. $META Stock Sold by AlTi Global Inc. _(MarketBeat; words +0.00)_
  - Meta Platforms Halts Class C Stock Plan Amid Shareholder Lawsuit _(GuruFocus; words -0.76)_
  - Meta: Buy The AI Payoff Before The Capex Fear Fades _(Seeking Alpha; words +0.00)_
- **AMD** (AMD) news score +0.09
  - Key facts: AMD Buys World Labs; Upgrades; 80% Data Center Mix in 2027 _(TradingView; words +0.64)_
  - ‘Unprecedented Results’: AMD Packs a Year of Chip Progress Into 5 Months Using OpenAI, Greg Brockman Says _(unknown; words +0.00)_
  - Is AMD's (NASDAQ:AMD) Chart Drawing Attention? _(Kalkine Media; words +0.00)_

See `docs/index.html` for the chart and full tables.
