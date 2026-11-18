# Paper trading report

_Through the close on **2026-11-17**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $98,312 | -1.69% | +3.84% | +3.52% | -8.23% | 38 | 54.0% ± 4.9 (402) | Too early to tell (25/60 days) |
| Hybrid (news + momentum) | $97,627 | -2.37% | +3.16% | +2.83% | -4.65% | 22 | 50.8% ± 4.8 (415) | Too early to tell (25/60 days) |
| News (word-list sentiment) | $102,522 | +2.52% | +8.05% | +7.73% | -5.49% | 23 | 52.1% ± 5.8 (288) | Too early to tell (25/60 days) |
| Momentum (prices only) | $97,320 | -2.68% | +2.85% | +2.52% | -4.62% | 21 | 48.4% ± 4.6 (459) | Too early to tell (25/60 days) |
| Equal weight, whole list | $94,795 | -5.21% | +0.32% | – | -6.34% | 24 | – |  |
| Buy & hold SPY | $94,471 | -5.53% | – | – | -5.53% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 402 | 54.0% | 53.0% | +22.8 bp | +0.066 (25) |
| Hybrid (news + momentum) | 415 | 50.8% | 52.8% | +17.8 bp | +0.037 (25) |
| News (word-list sentiment) | 288 | 52.1% | 52.4% | +30.8 bp | +0.074 (25) |
| Momentum (prices only) | 459 | 48.4% | 50.8% | +1.9 bp | +0.024 (25) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: COST (18.85 sh), LLY (13.54 sh), V (44.19 sh), WMT (152.59 sh), XOM (117.83 sh); cash $650
  - next open: COST 20%, LLY 20%, V 20%, WMT 20%, XOM 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.71 sh), WMT (157.18 sh); cash $59
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: AAPL (58.88 sh), COST (18.46 sh), WMT (168.69 sh); cash $39,792
  - next open: COST 20%, WMT 20%
- **Momentum (prices only)**: COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), V (45.81 sh), WMT (147.22 sh); cash $23
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (51.25 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.38
  - Intel cuts more jobs as CEO Lip-Bu Tan's efficiency push continues _(Yahoo Finance UK; words -0.24)_
  - Intel Shares Fall Following Nvidia Stake Cut and Risk Breakdown Under $50 as Lawsuit Weighs _(FXLeaders; words -0.83)_
  - Intel shareholders sue CEO, CFO after stock rout _(CFO Dive; words +0.00)_
- **UNH** (UnitedHealth) news score -0.17
  - UnitedHealth Keeps Raising Guidance. Here's What a $10,000 Investment Could Be Worth if the Turnaround Sticks. _(The Motley Fool; words +0.00)_
  - UnitedHealth Group (UNH) Stock Price Prediction: Pullback tests support as Evercore keeps a $480 target in place _(Blockchain News; words -0.24)_
  - UnitedHealth (UNH) vs. Humana (HUM): Buy the Dip? _(Zacks Investment Research; words -0.24)_
- **DIS** (Disney) news score +0.12
  - Disney (DIS) Stock Slips As Q4 Earnings Meet Margin Compression _(Simply Wall St; words -0.29)_
  - Disney (DIS) Stock Slips As Q4 Earnings Contrast Margin Compression _(unknown; words -0.29)_
  - Disney: 3 Key Takeaways for Long-Term Investors _(unknown; words +0.00)_
- **COST** (Costco) news score +0.09
  - ‘The best time to do it is when you don’t need it’: Ursula urges preparedness as Costco shoppers stock up after outages _(MyNorthwest.com; words +0.00)_
  - Costco (COST) Stock Fair Value Edges Higher As AI Rollout Expands And Lawsuits Emerge _(unknown; words +0.42)_
  - Panic stockpiling at Costco gets a boost from wave of system outages; Mizuho raises price target _(BigGo Finance; words +0.78)_
- **MSFT** (Microsoft) news score -0.08
  - Microsoft Stock MSFT Drops Below $500 as New Cybersecurity Concerns Hit Tech _(FXLeaders; words -0.54)_
  - Baseten partners with Microsoft Foundry to offe... _(Pluang; words +0.00)_
  - Baseten Brings High-Performance Inference for Open Models to Microsoft Foundry _(unknown; words +0.00)_
- **LLY** (Eli Lilly) news score +0.07
  - Eli Lilly Director Jon R. Moeller Purchases 167.6364 Shares on November 16, 2026 _(Kalkine Media; words +0.00)_
  - Eli Lilly Director Jamere Jackson Purchases 167.6364 Shares on November 16, 2026 _(Kalkine Media; words +0.00)_
  - Eli Lilly Is Up 39% in a Year. Barclays Sees Another 9% _(TIKR.com; words +0.00)_

See `docs/index.html` for the chart and full tables.
