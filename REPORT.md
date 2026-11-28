# Paper trading report

_Through the close on **2026-11-27**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $97,486 | -2.51% | +3.55% | +3.34% | -8.23% | 46 | 51.7% ± 4.3 (507) | Too early to tell (32/60 days) |
| Hybrid (news + momentum) | $100,215 | +0.22% | +6.28% | +6.07% | -4.65% | 26 | 50.2% ± 4.2 (534) | Too early to tell (32/60 days) |
| News (word-list sentiment) | $105,900 | +5.90% | +11.96% | +11.75% | -5.49% | 30 | 49.3% ± 5.2 (355) | Too early to tell (32/60 days) |
| Momentum (prices only) | $99,604 | -0.40% | +5.66% | +5.46% | -4.65% | 23 | 48.7% ± 4.0 (591) | Too early to tell (32/60 days) |
| Equal weight, whole list | $94,148 | -5.85% | +0.21% | – | -10.94% | 26 | – |  |
| Buy & hold SPY | $93,940 | -6.06% | – | – | -11.03% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 507 | 51.7% | 52.3% | +2.2 bp | +0.042 (32) |
| Hybrid (news + momentum) | 534 | 50.2% | 52.1% | +7.2 bp | +0.035 (32) |
| News (word-list sentiment) | 355 | 49.3% | 52.4% | -4.7 bp | +0.022 (32) |
| Momentum (prices only) | 591 | 48.7% | 50.8% | -3.6 bp | +0.035 (32) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: BA (109.03 sh), DIS (157.02 sh), LLY (13.54 sh), V (46.81 sh), WMT (152.59 sh); cash $0
  - next open: BA 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), V (45.78 sh), WMT (157.18 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: DIS (172.58 sh), WMT (168.69 sh); cash $61,483
  - next open: DIS 20%, WMT 20%
- **Momentum (prices only)**: AAPL (52.40 sh), COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), WMT (147.22 sh); cash $569
  - next open: AAPL 20%, COST 20%, DIS 20%, LLY 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (54.41 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **MSFT** (Microsoft) news score -0.11
  - Microsoft (MSFT) Stock Edges Up to $492.85 in Afternoon Trading _(JournalArta; words +0.00)_
  - Microsoft Stocks Rise 0.26% as Code Red Targets One-Hour Outage Recovery _(unknown; words -0.15)_
  - Microsoft's strong quarter and steady outlook m... _(Pluang; words +0.34)_
- **GOOGL** (Alphabet) news score -0.10
  - Form 4 Alphabet Inc Class A For: 27 November By Investing.com _(Investing.com India; words +0.00)_
  - Class action lawsuit filed against Alphabet ove... _(Pluang; words -0.85)_
  - ROSEN, LEADING INVESTOR COUNSEL, Encourages Alphabet Inc. _(GlobeNewswire; words +0.00)_
- **LLY** (Eli Lilly) news score +0.09
  - Biotech Dealmaker: Sanofi’s $41B Insmed Buyout Anchors Holiday Week As Lilly Continues Buying Spree _(unknown; words +0.00)_
  - Moody's Hands Eli Lilly a Two-Notch Credit Boost as Buyouts and Label Changes Reshape the Story _(ad-hoc-news.de; words +0.29)_
  - Eli Lilly Wins Moody's Upgrade as FDA Label Change and Cancer Pipeline Reshape the Story _(ad-hoc-news.de; words +0.82)_
- **UNH** (UnitedHealth) news score +0.08
  - Brianne Gardner’s Top Picks: Amazon.com, BlackRock & UnitedHealth _(BNN Bloomberg; words +0.00)_
  - Can UnitedHealth Group (NYSE:UNH) Overcome Its Operational Challenges? _(Kalkine Media; words +0.00)_
  - Is UnitedHealth Group Stock Underperforming the S&P 500? _(unknown; words +0.00)_
- **DIS** (Disney) news score +0.07
  - Netflix Stock Down 36.64% This Year as Disney Licenses Titles _(JournalArta; words +0.00)_
  - Disney Shares the Magic of EPCOT Holiday Storytellers _(Daps Magic; words +0.00)_
  - DIS Stock Hits One-Year High as Disney Shares Rise _(JournalArta; words +0.34)_
- **AMZN** (Amazon) news score +0.07
  - Amazon takes its car store abroad for the first time in 2027 _(unknown; words +0.00)_
  - Amazon Stocks Climb 2.96% as Thanksgiving Online Spending Hits $7.1 Billion _(GuruFocus; words +0.34)_
  - Plot Twist: Nvidia’s Vera Rubin Gets 2-6.5x GB300’s Tokens per Dollar. Amazon’s Trainium Edge Was Against the Old Chip _(unknown; words +0.00)_

See `docs/index.html` for the chart and full tables.
