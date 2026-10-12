# Stock Paper Trader

A bot that reads stock news, makes next-day predictions, and trades them with
**fake money** so you can see whether the predictions are any good. Several
strategies each run their own $100,000 paper account side by side, against a
buy-and-hold SPY account, using real prices and real headlines. It runs once a
day on GitHub Actions and commits its results back to this repo, so the track
record builds itself.

**Latest results: [REPORT.md](REPORT.md)** (and `docs/index.html` for the chart).

This is an experiment, not investment advice. No real orders are ever placed.

## The strategies

| Account | How it scores each stock |
|---|---|
| `claude` | Claude reads each new headline and rates its likely next-day impact from -1 to 1. Runs only when `ANTHROPIC_API_KEY` is set. |
| `news` | The same headlines scored by a finance word list (`papertrader/sentiment.py`): "beats estimates", "cuts guidance", "downgrade", with negation handling. |
| `hybrid` | 60% `news` score + 40% `momentum` score. |
| `momentum` | Prices only: 20- and 60-day returns scaled by the stock's volatility. The no-news baseline. |
| `benchmark` | Buys SPY once and holds it. What you'd get by doing nothing clever. |

`claude` and `news` read the same headlines and trade with the same rules, so
the gap between them measures what the reader adds. `momentum` shows whether the
news helps at all compared to price trends.

Headline scores are combined per stock as a recency-weighted average (weight
halves every 24 hours, 72-hour window), shrunk toward 0 so that one story moves
the score less than a steady stream of stories pointing the same way.

## How a trading day works

```text
after the close on day D                          day D+1
────────────────────────────────────────          ─────────────────────────
prices (Yahoo) ─┐                                 orders fill at the OPEN
headlines (RSS) ┼─► score ─► predict ─► orders ─► (+5 bp slippage)
archive ────────┘                                 marked at the CLOSE, and
                                                  D's predictions are graded
```

1. **Prices**: daily bars for the 20 stocks in `config.json` plus SPY from
   Yahoo Finance's chart API (Stooq as a fallback). No API key.
2. **Fill and mark**: yesterday's orders fill at today's open, then every
   account is valued at today's close. Splits and dividends are applied.
3. **Grade**: yesterday's predictions get their outcome: did the stock close
   higher or lower than the day before, as called?
4. **News**: new headlines from Yahoo Finance and Google News RSS. Each is
   scored once and saved to `data/news/YYYY-MM-DD.jsonl`.
5. **Decide**: every strategy scores every stock. A score of at least 0.05 in
   either direction is an up/down **prediction**. The top scores above the entry
   threshold become the target portfolio: up to 5 stocks at 20% each, the rest in
   cash. Long only. A stock already held stays until its score drops to 0 or
   below, which keeps the bot from churning.

Orders fill at the **next open**, never at the close the decision was based on.
News published after the close can't be traded at a price from before it came
out. If the bot runs after the next open (a late manual run, say), it places no
new orders.

## Is it actually any good?

Making money for a few weeks proves very little: in a rising market almost any
long-only strategy makes money. The report shows several measures together:

- **Return vs SPY**: did it beat doing nothing?
- **Hit rate ± 95% margin**: the share of up/down calls that were right. It's
  compared with a **baseline**, the hit rate of always guessing the more common
  direction (never below 50%), because stocks rise on a bit over half of all days.
- **Edge**: average next-day move in the called direction, in basis points.
- **Rank IC**: each day, does the ranking of scores match the ranking of
  next-day returns? Averaged over days. A sustained IC above about 0.03 is
  useful; anything under ±0.02 is noise.
- **Verdict**: withheld until there are 60 graded trading days. Calls made on the
  same day move together (when the market drops, most "up" calls are wrong at
  once), so a few hundred calls from a few weeks are far less evidence than they
  look.

Expect the honest answer to be "not distinguishable from the baseline" for a
long time. Beating the market on daily headline sentiment is hard, and that's the
point of measuring it.

## Running it on GitHub Actions (recommended)

`.github/workflows/daily.yml` runs the bot at 21:30 UTC on weekdays (after the
close all year) and on Sunday evening (to read weekend news before Monday), then
commits `data/`, `REPORT.md` and `docs/` back to the repo.

1. Push this repo to GitHub. Actions are on by default.
2. Optional, for the `claude` account: add an Anthropic API key under
   **Settings → Secrets and variables → Actions → New repository secret**, named
   `ANTHROPIC_API_KEY`. Without it the other accounts run as normal.
3. To start right away instead of waiting for the evening, go to **Actions →
   Daily paper trade → Run workflow**. Run it after the 4pm New York close: a run
   during market hours updates the accounts but places no orders.

**Claude cost**: each new headline is scored once (about 150–300 a day across 20
stocks), with `claude-opus-5-5` at `"effort": "low"`. That should come to roughly
$5–10 a month, but this is an estimate: check your usage page after the first few
runs. The model and effort are set in `config.json` under `strategies.claude`;
requests opt into Anthropic's server-side fallback, so a declined batch is
retried on another model instead of coming back empty.

## Running it locally

Requires **Python 3.11+**.

```bash
git clone https://github.com/<you>/stock-paper-trader.git
cd stock-paper-trader
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

python -m papertrader run          # the daily cycle (run after the close)
python -m papertrader status       # leaderboard in the terminal
python -m papertrader report       # rebuild REPORT.md and docs/index.html
python -m papertrader backtest     # replay momentum vs SPY over the last 2 years
python -m pytest -q                # tests (offline)
```

`ANTHROPIC_API_KEY` in the environment turns on the `claude` account;
`run --no-claude` skips it. If you run locally *and* on Actions, pick one place:
both write the same `data/` folder.

## Backtesting

`backtest` replays `momentum` and `benchmark` over past prices with the same
fill rules. The news strategies can't be backtested from scratch: free RSS feeds
only show recent headlines, and testing on headlines collected today would leak
the future into the past. They're judged by the live accounts instead. The news
archive the bot builds day by day is what will make replaying them possible later.

## Configuration (`config.json`)

| Key | Meaning |
|---|---|
| `starting_cash` | Fake money per account (default 100,000). Change only before the first run. |
| `universe` | Ticker → company name. The name is used for the Google News search. |
| `trading.max_positions` | Slots per account; each gets 1/N of the account (default 5). |
| `trading.slippage_bps` | Price penalty per trade, in basis points (default 5 = 0.05%). |
| `trading.min_trade_pct` | Skip rebalances smaller than this % of the account (default 2). |
| `news.lookback_hours`, `news.half_life_hours` | Window and decay for headline scores (72 h, 24 h). |
| `strategies.<name>.entry` / `.exit` | Score needed to buy / score at or below which a holding is sold. |
| `strategies.<name>.enabled` | `true`, `false`, or `"auto"` (claude: on when a key is set). |

## Data files

| File | Contents |
|---|---|
| `data/accounts.json` | Cash, shares, and the pending order for each account. |
| `data/equity.csv` | Each account's value at every close. |
| `data/trades.csv` | Every simulated fill. |
| `data/predictions.csv` | Every prediction with its outcome once graded. |
| `data/news/*.jsonl` | Every headline seen, with its word-list and Claude scores. |
| `data/latest_signals.json` | Today's scores, targets, and the headlines behind them. |

All plain text, so each daily commit is a readable diff of what the bot did.

## Limitations

- **Free data.** Yahoo's endpoints are unofficial and occasionally rate-limit or
  change. The bot falls back to Stooq, which has no split data, and a ticker with
  no data on a given day is skipped. RSS feeds miss some news, and Google News
  matches by company name, so some headlines are only loosely related.
- **Fills are idealized.** Trades fill at the official open plus a fixed 5 bp.
  No partial fills, no spreads that vary with volatility, no market impact (fine
  for these very liquid stocks at this size). Fractional shares are allowed.
- **Long only.** "Down" calls are graded but not traded (no shorting).
- **Holidays aren't modeled.** A run on a market holiday sees no new session and
  doesn't trade, which is correct; the only effect is a skipped decision.
- **Survivorship.** The universe is 20 of today's largest companies, picked in
  hindsight.
