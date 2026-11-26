# Paper trading report

_Through the close on **2026-11-25**. Every account started with $100,000 of fake money. This file is rewritten by every run._

| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| FinBERT reads the news (free AI) | $96,507 | -3.49% | +4.07% | +4.19% | -8.23% | 46 | 52.3% ± 4.4 (491) | Too early to tell (31/60 days) |
| Hybrid (news + momentum) | $98,752 | -1.25% | +6.31% | +6.44% | -4.65% | 24 | 50.8% ± 4.3 (516) | Too early to tell (31/60 days) |
| News (word-list sentiment) | $104,821 | +4.82% | +12.38% | +12.51% | -5.49% | 29 | 50.0% ± 5.3 (348) | Too early to tell (31/60 days) |
| Momentum (prices only) | $98,784 | -1.22% | +6.34% | +6.47% | -4.65% | 23 | 49.2% ± 4.1 (573) | Too early to tell (31/60 days) |
| Equal weight, whole list | $92,312 | -7.69% | -0.13% | – | -10.94% | 26 | – |  |
| Buy & hold SPY | $92,441 | -7.56% | – | – | -11.03% | 1 | – |  |

**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, with the number of graded calls in brackets. The **baseline** is the hit rate of always guessing the more common direction, never below 50%. No verdict is given before 60 graded trading days: calls on the same day move together, so a few weeks of good calls can be one lucky market move.

**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past (see `research/RESULTS.md`). A strategy has to beat that to show skill.

## Prediction quality

| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |
|---|---:|---:|---:|---:|---:|
| FinBERT reads the news (free AI) | 491 | 52.3% | 54.0% | +7.2 bp | +0.051 (31) |
| Hybrid (news + momentum) | 516 | 50.8% | 53.9% | +12.0 bp | +0.043 (31) |
| News (word-list sentiment) | 348 | 50.0% | 53.4% | +0.0 bp | +0.034 (31) |
| Momentum (prices only) | 573 | 49.2% | 52.4% | +0.4 bp | +0.043 (31) |

*Baseline*: the hit rate of always calling whichever direction those stocks moved more often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day returns across all stocks, averaged; above about 0.03 sustained is useful.

## Holdings and next orders

- **FinBERT reads the news (free AI)**: BA (109.03 sh), DIS (157.02 sh), LLY (13.54 sh), V (46.81 sh), WMT (152.59 sh); cash $0
  - next open: BA 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **Hybrid (news + momentum)**: COST (18.52 sh), DIS (163.72 sh), LLY (13.26 sh), TSLA (49.62 sh), WMT (157.18 sh); cash $0
  - next open: COST 20%, DIS 20%, LLY 20%, V 20%, WMT 20%
- **News (word-list sentiment)**: DIS (172.58 sh), TSLA (54.04 sh), WMT (168.69 sh); cash $40,343
  - next open: DIS 20%, WMT 20%
- **Momentum (prices only)**: AAPL (52.40 sh), COST (18.95 sh), DIS (170.08 sh), LLY (13.07 sh), WMT (147.22 sh); cash $569
  - next open: AAPL 20%, COST 20%, DIS 20%, LLY 20%, WMT 20%
- **Equal weight, whole list**: AAPL (14.50 sh), AMD (8.48 sh), AMZN (19.37 sh), AVGO (14.19 sh), BA (26.93 sh), COST (5.19 sh), DIS (46.06 sh), GOOGL (14.05 sh), INTC (54.41 sh), JPM (15.27 sh), LLY (4.24 sh), META (6.57 sh), MSFT (9.17 sh), NFLX (70.47 sh), NVDA (22.15 sh), TSLA (13.46 sh), UNH (13.07 sh), V (12.62 sh), WMT (43.96 sh), XOM (28.55 sh); cash $0
  - next open: AAPL 5%, AMD 5%, AMZN 5%, AVGO 5%, BA 5%, COST 5%, DIS 5%, GOOGL 5%, INTC 5%, JPM 5%, LLY 5%, META 5%, MSFT 5%, NFLX 5%, NVDA 5%, TSLA 5%, UNH 5%, V 5%, WMT 5%, XOM 5%
- **Buy & hold SPY**: SPY (128.98 sh); cash $0
  - next open: SPY 100%

## Strongest news signals

- **INTC** (Intel) news score -0.18
  - Intel (NASDAQ:INTC) Stock Sale Disclosed by Rep. Kevin Hern _(MarketBeat; words +0.00)_
  - Dell Stock Joins Nvidia, AMD, and Intel Selloff Despite Record Demand _(BeInCrypto; words -0.54)_
  - Intel Aims for Strong Rebound as INTC Stock Buyers Defend $50 Support Convincingly after Nvidia Selloff _(FXLeaders; words +0.15)_
- **AVGO** (Broadcom) news score -0.16
  - Broadcom Shares Fall to More Than One-Year Low as Market Still Undervalues AI Growth Prospects _(NAI500; words -0.10)_
  - Broadcom: Why The Market Is Wrong To Sell (NASDAQ:AVGO) _(Seeking Alpha; words +0.00)_
  - Broadcom's Google Order Trim Takes the Shine Off a Bruising Week _(ad-hoc-news.de; words +0.00)_
- **MSFT** (Microsoft) news score -0.15
  - Microsoft (MSFT) Stock Could Be 36% Below Fair Value After Global Outage _(Simply Wall St; words -0.46)_
  - Nvidia’s Market Cap Falls Below Microsoft’s: Analyst Flags Five Overhangs For NVDA Stock _(Stocktwits; words -0.34)_
  - Satya Nadella Says “the Floor of Cyber Attacks Has Fallen.” Microsoft Just Declared Code Red After a 24-Hour Outage _(TIKR.com; words -0.46)_
- **DIS** (Disney) news score +0.13
  - DIS Stock Breaks Above $125 For First Time Since 2022: Disney Retail Bulls Are Talking About A ‘Santa Claus Rally’ _(Stocktwits; words +0.46)_
  - Atour Lifestyle, Walt Disney Among 8 New Stocks On IBD Watchlists _(Investor's Business Daily; words +0.00)_
  - Disney Tokenized Stock (Reality) (RDIS) Price Prediction for 2026 to 2031 _(Bybit; words +0.00)_
- **GOOGL** (Alphabet) news score -0.11
  - Alphabet stock drops to $273.10 as AI rout widens gap with S&P 500 _(JournalArta; words -0.34)_
  - 2 Ways Anthropic's IPO Pays Off for Alphabet Investors _(The Globe and Mail; words +0.00)_
  - Why is Alphabet stock sliding? Key factors behind the sell-off _(The Economic Times; words -0.76)_
- **AMD** (AMD) news score -0.09
  - Is The Client Unit Still Carrying AMD Stock? _(Trefis; words +0.00)_
  - Advanced Micro Devices, Inc. (AMD) Stock Price, News, Quote & History _(Yahoo! Finance Canada; words +0.00)_
  - AMD shares drop amid tariffs, inflation data, and dilution fears _(StreetInsider; words -0.76)_

See `docs/index.html` for the chart and full tables.
