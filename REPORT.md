# Paper trading report

_Through the close on **2026-11-20**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $94,828 | -5.17% | +5.86% | +5.72% | -8.23% | 42 | 53.4% ± 4.6 (444) | Too early to tell (28/60 days) |
| Hybrid (news + momentum) | $96,197 | -3.80% | +7.22% | +7.09% | -4.65% | 23 | 51.0% ± 4.6 (463) | Too early to tell (28/60 days) |
| News (word-list sentiment) | $102,345 | +2.34% | +13.37% | +13.23% | -5.49% | 25 | 51.4% ± 5.5 (315) | Too early to tell (28/60 days) |
| Momentum (prices only) | $95,351 | -4.65% | +6.38% | +6.24% | -4.65% | 23 | 48.8% ± 4.3 (514) | Too early to tell (28/60 days) |
| Equal weight, whole list | $89,112 | -10.89% | +0.14% | – | -10.94% | 25 | – |  |
| Buy & hold SPY | $88,972 | -11.03% | – | – | -11.03% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 444 | 53.4% | 55.4% | +26.6 bp | +0.063 (28) |
| Hybrid (news + momentum) | 463 | 51.0% | 55.5% | +25.1 bp | +0.058 (28) |
| News (word-list sentiment) | 315 | 51.4% | 54.3% | +27.9 bp | +0.075 (28) |
| Momentum (prices only) | 514 | 48.8% | 53.7% | +8.3 bp | +0.050 (28) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: DIS (157.02 sh), LLY (13.54 sh), WMT (152.59 sh); cash $38,540
  - next open: DIS 20%, LLY 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), WMT (157.18 sh); cash $18,498
  - next open: COST 20%, DIS 20%, LLY 20%, WMT 20%
- **News (word-list sentiment)**: COST (18.46 sh), DIS (172.58 sh), WMT (168.69 sh); cash $40,048
  - next open: COST 20%, DIS 20%, UNH 20%, WMT 20%
- **Momentum (prices only)**: AAPL (52.40 sh), COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), WMT (147.22 sh); cash $0
  - next open: AAPL 20%, COST 20%, DIS 20%, LLY 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $9
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **NVDA** (Nvidia) news score -0.21
  - Jensen Huang Has Lost $92 Billion and Nvidia’s Board Does Not Intend to Bring Him Back. Here’s What 9 Stocks Did the Year After Their Founder Handed Over _(unknown; words +0.00)_
  - Has the AI Bubble Already Burst? Nvidia, Nasdaq Plunge _(조선일보; words -0.72)_
  - Elon Musk Could Use His Nvidia Chip Orders to Push for Jensen Huang’s Return, Analyst Says _(unknown; words +0.00)_
- **UNH** (UnitedHealth) news score +0.19
  - UnitedHealth Group (UNH) Shares Plunge 16.59% Amid Healthcare Se _(GuruFocus; words -0.72)_
  - UnitedHealth Beats Q1 2026 and Raises Guidance - Is UNH Stock a Buy After Jumping 8%? _(TradingKey; words +0.98)_
  - UnitedHealth Is Suing the Government Over Medicare Advantage Star Ratings _(unknown; words +0.00)_
- **AVGO** (Broadcom) news score -0.16
  - Google Cuts Broadcom TPU Orders by a Million Units; MediaTek Seen Capturing the Shift, Goldman Sachs Trims Broadcom Price Target _(finance.biggo.com; words -0.24)_
  - Google’s 2027 chip plan is bad news for Broadcom _(unknown; words +0.00)_
  - Here's What a $1,000 Investment in Broadcom Stock Could Be Worth By 2035 _(unknown; words +0.00)_
- **AMD** (AMD) news score -0.12
  - AMD vs. Nvidia Stock After Jensen Huang’s Exit: 1 Trades at Nearly 4x the Other’s Earnings Multiple. Here’s the AI Chip Stock I’d Buy Now. _(Barchart.com; words +0.00)_
  - AMD Gained From Nvidia’s China Scandal. Now a Short Seller Says AMD Has a China Problem Too. _(unknown; words -0.15)_
  - Prediction: These Will Be AMD’s and Nvidia’s Stock Prices by 2028 _(unknown; words +0.00)_
- **LLY** (Eli Lilly) news score +0.12
  - Eli Lilly’s Next Weight-Loss Drug Shows 54.1-Pound Loss _(JournalArta; words -0.29)_
  - Eli Lilly leads obesity drug market with strong sales and promising pipeline, securing its top position. _(Pluang; words +0.34)_
  - Eli Lilly's Obesity Pipeline Is Getting Crowded. That's Great News for Investors _(unknown; words +0.00)_
- **NFLX** (Netflix) news score -0.11
  - Michael Burry's Netflix warning puts investors in a $39 dilemma _(unknown; words -0.46)_
  - Netflix (NFLX) Stock Could Be 34% Undervalued Despite Ad Guidance Cuts _(Simply Wall St; words +0.00)_
  - Netflix Stock Split Halves Price: Burry Eyes $39 Entry as Ackman Adds $1.07 Billion _(BigGo Finance; words +0.00)_

See `docs/index.html` for the chart and full tables.
