# Paper trading report

_Through the close on **2026-11-19**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $94,919 | -5.08% | +2.59% | +2.46% | -8.23% | 40 | 53.1% ± 4.7 (429) | Too early to tell (27/60 days) |
| Hybrid (news + momentum) | $96,117 | -3.88% | +3.78% | +3.65% | -4.65% | 22 | 50.6% ± 4.6 (445) | Too early to tell (27/60 days) |
| News (word-list sentiment) | $102,261 | +2.26% | +9.93% | +9.80% | -5.49% | 25 | 51.3% ± 5.6 (306) | Too early to tell (27/60 days) |
| Momentum (prices only) | $95,850 | -4.15% | +3.52% | +3.39% | -4.62% | 21 | 48.5% ± 4.4 (495) | Too early to tell (27/60 days) |
| Equal weight, whole list | $92,462 | -7.54% | +0.13% | – | -7.59% | 25 | – |  |
| Buy & hold SPY | $92,334 | -7.67% | – | – | -7.67% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 429 | 53.1% | 54.8% | +21.2 bp | +0.058 (27) |
| Hybrid (news + momentum) | 445 | 50.6% | 54.6% | +19.1 bp | +0.047 (27) |
| News (word-list sentiment) | 306 | 51.3% | 54.2% | +29.1 bp | +0.066 (27) |
| Momentum (prices only) | 495 | 48.5% | 52.7% | +5.3 bp | +0.041 (27) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: DIS (157.02 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh), XOM (117.83 sh); cash $2,012
  - next open: DIS 20%, LLY 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $59
  - next open: COST 20%, DIS 20%, LLY 20%, WMT 20%
- **News (word-list sentiment)**: COST (18.46 sh), DIS (172.58 sh), WMT (168.69 sh); cash $40,048
  - next open: COST 20%, DIS 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $23
  - next open: AAPL 20%, COST 20%, DIS 20%, LLY 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $9
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **UNH** (UnitedHealth) news score -0.33
  - UnitedHealth Stock Continues Slide on Medicare for All Push. What Lies Ahead for Insurers. _(Barron's; words -0.38)_
  - UnitedHealth Group (UNH) Stock Price Prediction: Oversold bounce setup meets heavy trend damage after a sharp selloff _(Blockchain News; words -0.54)_
  - Bernstein’s $500 Target Says UnitedHealth’s Selloff Went Too Far _(unknown; words -0.54)_
- **DIS** (Disney) news score +0.19
  - Disney Just Raised Its Dividend 33% and Guided to Double-Digit EPS Growth. Here’s What Its Results Mean for Investors. _(unknown; words +0.46)_
  - Disney Just Boosted Its Dividend by 33%. That Gives DIS Stock Investors a Real Reason to Stick Around. _(Barchart.com; words +0.00)_
  - Walt Disney Co. stock underperforms Thursday when compared to competitors _(MarketWatch; words +0.00)_
- **AMD** (AMD) news score -0.11
  - AMD Just Plunged Almost 8%, Lost $67 Billion and Kept Falling After Hours. A Short Seller Says It Shares Nvidia’s China Risk _(unknown; words -0.96)_
  - KOSPI Breaks Below 5,000 in a Single Day... Plunges 4% on AMD Export-Control Fears _(BigGo Finance; words -0.86)_
  - Advantest: Sharp continued decline; weakness in AMD shares viewed as a negative factor for semiconductor-related stocks. _(Moomoo; words -0.34)_
- **COST** (Costco) news score +0.09
  - Jim Cramer sends strong signal to Costco investors _(TheStreet; words +0.34)_
  - Tech Outages Trigger Panic Buying of Generators and Emergency Supplies at Costco _(SSBCrack; words +0.00)_
  - Costco sees panic buying surge after tech outages, report says _(Fox Business; words +0.64)_
- **INTC** (Intel) news score +0.07
  - Intel (NASDAQ:INTC) Shares Climb 1.9% - Still a Buy? _(MarketBeat; words +0.34)_
  - Nvidia vs. Intel: One AI Stock Is Worth the Drama, the Other Isn’t Worth the Wait, Says Investor _(unknown; words +0.00)_
  - INTC Stock Rebound Is Underway as Intel Signs First External Customer for Advanced 18A Chip Technology _(FXLeaders; words +0.38)_
- **LLY** (Eli Lilly) news score +0.06
  - Judge tosses Tampa General’s 340B suit against Eli Lilly _(Modern Healthcare; words +0.00)_
  - Jefferies Has Wall Street’s Highest Target on Eli Lilly (LLY). Why? _(unknown; words +0.00)_
  - Sanofi and Regeneron’s rare disease wins; Lilly’s dealmaking dance _(unknown; words +0.38)_

See `docs/index.html` for the chart and full tables.
