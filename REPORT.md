# Paper trading report

_Through the close on **2026-10-15**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $100,955 | +0.95% | +1.41% | +0.90% | +0.00% | 5 | 54.8% ± 17.5 (31) | Too early to tell (2/60 days) |
| Hybrid (news + momentum) | $98,325 | -1.68% | -1.22% | -1.73% | -1.72% | 5 | 45.5% ± 17.0 (33) | Too early to tell (2/60 days) |
| News (word-list sentiment) | $101,028 | +1.03% | +1.48% | +0.97% | -0.17% | 4 | 40.9% ± 20.5 (22) | Too early to tell (2/60 days) |
| Momentum (prices only) | $98,325 | -1.68% | -1.22% | -1.73% | -1.72% | 5 | 40.5% ± 15.8 (37) | Too early to tell (2/60 days) |
| Equal weight, whole list | $100,057 | +0.06% | +0.51% | – | -0.37% | 20 | – |  |
| Buy & hold SPY | $99,546 | -0.45% | – | – | -0.74% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 31 | 54.8% | 54.8% | +44.7 bp | +0.244 (2) |
| Hybrid (news + momentum) | 33 | 45.5% | 54.5% | -7.5 bp | -0.050 (2) |
| News (word-list sentiment) | 22 | 40.9% | 54.5% | +1.8 bp | +0.057 (2) |
| Momentum (prices only) | 37 | 40.5% | 51.4% | -49.2 bp | -0.159 (2) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: AAPL (58.01 sh), COST (20.77 sh), META (26.28 sh), UNH (52.29 sh), V (50.49 sh); cash $0
  - next open: AAPL 20%, COST 20%, META 20%, UNH 20%, V 20%
- **Hybrid (news + momentum)**: AMD (33.90 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: META 20%, MSFT 20%, V 20%, WMT 20%, XOM 20%
- **News (word-list sentiment)**: META (26.29 sh), MSFT (37.54 sh), UNH (52.32 sh), V (50.52 sh); cash $19,940
  - next open: META 20%, MSFT 20%, UNH 20%, V 20%, WMT 20%
- **Momentum (prices only)**: AMD (33.90 sh), META (26.28 sh), MSFT (36.67 sh), V (50.49 sh), XOM (114.19 sh); cash $0
  - next open: AMD 20%, META 20%, MSFT 20%, V 20%, XOM 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (50.20 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **V** (Visa) news score +0.26
  - Visa (NYSE:V) Stock Jumps 2.1% - Here's Why _(MarketBeat; words +0.46)_
  - Visa (V) Outperforms Broader Market: What You Need to Know _(unknown; words +0.00)_
  - Microsoft's Cyber Takedown and Visa Fight Take Center Stage as Stock Hovers Near Record _(ad-hoc-news.de; words +0.38)_
- **UNH** (UnitedHealth) news score +0.26
  - $100 Invested In UnitedHealth Group 20 Years Ago Would Be Worth This Much Today _(Benzinga; words +0.00)_
  - Nike, UnitedHealth Share Gains Lead Dow's 529-Point Rally _(Moomoo; words +0.69)_
  - UnitedHealth Stock Moves Higher: What's Going On? _(TradingView; words +0.00)_
- **WMT** (Walmart) news score +0.24
  - What the ‘Walmart effect’ is warning about the US economy _(The Independent; words -0.46)_
  - Walmart (NASDAQ:WMT) Stock Jumps 1.5% - Time to Buy? _(MarketBeat; words +0.46)_
  - Walmart rockets higher after a Deutsche Bank buy upgrade _(Rolling Out; words +0.91)_
- **LLY** (Eli Lilly) news score +0.12
  - Pharma Giant Lilly's Shares Jump Despite Tough Market Day, As It Leads 19 To Best Stock Lists _(Investor's Business Daily; words +0.46)_
  - Eli Lilly stock rises as investors move from tech to healthcare _(Quartz; words +0.34)_
  - Eli Lilly Stock Nears $1,292 All-Time High as Technicals Point to Potential New Record _(TradingKey; words +0.72)_
- **MSFT** (Microsoft) news score +0.12
  - Microsoft (MSFT) officer Amy Coleman reports 32 shares delivered or withheld at $533.69 each. _(Stock Titan; words +0.00)_
  - Microsoft (MSFT) Gets a Buy from Jefferies _(The Globe and Mail; words +0.00)_
  - Microsoft $1,000 investment grows to $18,199 over 20 years _(scanx.trade; words +0.00)_
- **COST** (Costco) news score +0.11
  - Tigress Financial raises Costco stock price target on membership growth By Investing.com _(Investing.com South Africa; words +0.24)_
  - Tigress Financial Forecasts Strong Price Appreciation for Costco Wholesale (NASDAQ:COST) Stock _(MarketBeat; words +0.34)_
  - Move over, Trader Joe’s: Costco has mini totes that are actually in stock _(NewsNation; words +0.00)_

See `docs/index.html` for the chart and full tables.
