# Paper trading report

_Through the close on **2026-11-19**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $94,919 | -5.08% | +2.59% | +2.46% | -8.23% | 40 | 53.3% ± 4.7 (430) | Too early to tell (27/60 days) |
| Hybrid (news + momentum) | $96,117 | -3.88% | +3.78% | +3.65% | -4.65% | 22 | 50.7% ± 4.6 (446) | Too early to tell (27/60 days) |
| News (word-list sentiment) | $102,261 | +2.26% | +9.93% | +9.80% | -5.49% | 25 | 51.5% ± 5.6 (307) | Too early to tell (27/60 days) |
| Momentum (prices only) | $95,850 | -4.15% | +3.52% | +3.39% | -4.62% | 21 | 48.6% ± 4.4 (496) | Too early to tell (27/60 days) |
| Equal weight, whole list | $92,462 | -7.54% | +0.13% | – | -7.59% | 25 | – |  |
| Buy & hold SPY | $92,334 | -7.67% | – | – | -7.67% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 430 | 53.3% | 54.9% | +21.9 bp | +0.060 (27) |
| Hybrid (news + momentum) | 446 | 50.7% | 54.7% | +19.8 bp | +0.048 (27) |
| News (word-list sentiment) | 307 | 51.5% | 54.4% | +30.0 bp | +0.068 (27) |
| Momentum (prices only) | 496 | 48.6% | 52.8% | +6.0 bp | +0.041 (27) |

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
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **UNH** (UnitedHealth) news score -0.29
  - Can UnitedHealth Group Stock Rally 50% After This Dip? _(Trefis; words +0.24)_
  - UnitedHealth (UNH) Stock: $330.48, Down 5.55% Nov 19 _(JournalArta; words +0.00)_
  - TD Cowen upgrades UnitedHealth stock rating on earnings outlook _(Investing.com; words +0.64)_
- **DIS** (Disney) news score +0.19
  - Disney Is Near Its High. Morgan Stanley Still Sees 14% Upside _(TIKR.com; words +0.24)_
  - Disney Just Raised Its Dividend 33% and Guided to Double-Digit EPS Growth. Here’s What Its Results Mean for Investors. _(unknown; words +0.46)_
  - Disney Just Boosted Its Dividend by 33%. That Gives DIS Stock Investors a Real Reason to Stick Around. _(Barchart.com; words +0.00)_
- **AMD** (AMD) news score -0.18
  - When Nvidia Falls 30%, How Far Does AMD Fall? _(Trefis; words -0.60)_
  - AMD Shares Fall 7.7% After Short Seller Targets Its China Ties _(www.trendingtopics.eu; words -0.69)_
  - Key facts: AMD Revenue +45%; Anthropic Helios Deal; $800M MI308 Charge _(TradingView; words +0.00)_
- **WMT** (Walmart) news score +0.11
  - Walmart (WMT) Ad Revenue Jumped 25% As AI And TV Deals Gain Traction _(unknown; words +0.69)_
  - WMT Stock Ticks Higher Overnight: Analyst Says Walmart Deserves Rich Valuation, CEO Stands By ‘Low Price’ Game _(unknown; words +0.00)_
  - Walmart Stock (WMT) Falls 1.0% After Q3 Earnings (Nov 19) _(Gotrade; words -0.34)_
- **INTC** (Intel) news score +0.11
  - INTC Stock Rebound Is Underway as Intel Signs First External Customer for Advanced 18A Chips _(FXLeaders; words +0.38)_
  - Intel (NASDAQ:INTC) Shares Climb 1.9% - Still a Buy? _(MarketBeat; words +0.34)_
  - Nvidia vs. Intel: One AI Stock Is Worth the Drama, the Other Isn’t Worth the Wait, Says Investor _(unknown; words +0.00)_
- **COST** (Costco) news score +0.10
  - 229,666 Shares in Costco Wholesale Corporation $COST Acquired by Advisors Asset Management Inc. _(MarketBeat; words +0.00)_
  - Costco Wholesale (NASDAQ:COST) Stock Sale Reported by Rep. Michael A. Rulli _(MarketBeat; words +0.00)_
  - Costco (COST) Saw Emergency Supply Sales Surge After Tech Outages _(Simply Wall St; words +0.64)_

See `docs/index.html` for the chart and full tables.
