# Paper trading report

_Through the close on **2026-11-23**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $95,673 | -4.33% | +2.51% | +2.98% | -8.23% | 42 | 52.1% ± 4.6 (461) | Too early to tell (29/60 days) |
| Hybrid (news + momentum) | $96,981 | -3.02% | +3.82% | +4.29% | -4.65% | 23 | 50.2% ± 4.5 (480) | Too early to tell (29/60 days) |
| News (word-list sentiment) | $103,798 | +3.80% | +10.64% | +11.11% | -5.49% | 26 | 50.6% ± 5.4 (326) | Too early to tell (29/60 days) |
| Momentum (prices only) | $96,471 | -3.53% | +3.31% | +3.78% | -4.65% | 23 | 48.3% ± 4.2 (534) | Too early to tell (29/60 days) |
| Equal weight, whole list | $92,690 | -7.31% | -0.47% | – | -10.94% | 25 | – |  |
| Buy & hold SPY | $93,162 | -6.84% | – | – | -11.03% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 461 | 52.1% | 53.8% | +5.1 bp | +0.043 (29) |
| Hybrid (news + momentum) | 480 | 50.2% | 54.2% | +6.4 bp | +0.036 (29) |
| News (word-list sentiment) | 326 | 50.6% | 53.1% | +8.1 bp | +0.048 (29) |
| Momentum (prices only) | 534 | 48.3% | 52.2% | -7.9 bp | +0.033 (29) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: DIS (157.02 sh), LLY (13.54 sh), WMT (152.59 sh); cash $38,540
  - next open: DIS 20%, INTC 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), WMT (157.18 sh); cash $18,498
  - next open: COST 20%, DIS 20%, LLY 20%, TSLA 20%, WMT 20%
- **News (word-list sentiment)**: COST (18.46 sh), DIS (172.58 sh), UNH (63.24 sh), WMT (168.69 sh); cash $19,655
  - next open: DIS 20%, TSLA 20%, WMT 20%
- **Momentum (prices only)**: AAPL (52.40 sh), COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), WMT (147.22 sh); cash $0
  - next open: AAPL 20%, COST 20%, DIS 20%, LLY 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $9
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **TSLA** (Tesla) news score +0.22
  - Brad Gerstner Just Bought $680 Million of Tesla. His Range: “$420 a Share and Let’s Call It $520 or $550” _(TIKR.com; words +0.00)_
  - Tesla stock rises but still down 14% for 2026, trading at high valuations amid stalled growth. _(Pluang; words +0.50)_
  - Tesla stock rises 11% on new self-driving softw... _(Pluang; words +0.34)_
- **INTC** (Intel) news score +0.14
  - George Soros and 49 Other Big Funds Bought Intel Last Quarter, While 15 Sold. Who’s Right? _(TIKR.com; words +0.00)_
  - Intel Corporation $INTC Stock Sold by Healthcare of Ontario Pension Plan Trust Fund _(MarketBeat; words +0.00)_
  - Lawsuit Adds Insult to Injury for Struggling Intel _(Willamette Week; words -0.46)_
- **NVDA** (Nvidia) news score +0.13
  - Nvidia's historic stock surge showed Washington is getting more aggressive about backstopping markets _(Business Insider; words +0.64)_
  - Nvidia Bulls Rule on Asian Stock Markets _(unknown; words +0.00)_
  - Nvidia Turmoil: How Big Is the Risk for CoreWeave? _(unknown; words -0.15)_
- **BA** (Boeing) news score +0.12
  - Trump Teases Massive Boeing-China Deal - Boeing (NYSE:BA) _(Benzinga; words +0.00)_
  - BA, NOC, LMT, KTOS Stocks Draw Bullish Call From Mizuho: Analyst Calls The Group 'Underappreciated' Defense Plays _(Menafn; words +0.54)_
  - Boeing Stock Rises 4% on Analyst Support _(Wisevoter; words +0.34)_
- **DIS** (Disney) news score +0.09
  - Walt Disney (DIS) Stock Price Prediction: Analyst targets rise as Disney holds above short-term support _(Blockchain News; words +0.34)_
  - Walt Disney (DIS) Stock: $120.27, Up 1.94% Nov 23 _(JournalArta; words +0.00)_
  - Disney Stops Reporting Streaming Profit. Should You Worry? _(unknown; words +0.20)_
- **UNH** (UnitedHealth) news score -0.08
  - UnitedHealth Group (UNH) Stock Price Prediction: Oversold Bounce Faces Heavy Overhead Supply _(Blockchain News; words +0.00)_
  - UnitedHealth Sues Trump’s Medicare Agency Over Star Ratings. Stephanie Link Calls It “Number One on Sale” _(TIKR.com; words +0.00)_
  - UnitedHealth Sinks 18% in a Week on Washington’s Medicare Advantage Crackdown. Is It “Number One on Sale”? _(TIKR.com; words -0.54)_

See `docs/index.html` for the chart and full tables.
