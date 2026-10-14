# Stock Paper Trader

A bot that reads stock news, makes next-day predictions, and trades them with
**fake money** so you can see whether the predictions are any good. Several
strategies each run their own $100,000 paper account side by side, against two
benchmark accounts (SPY, and all 20 stocks held equally), using real prices and
real headlines. It runs once a
day on GitHub Actions and commits its results back to this repo, so the track
record builds itself.

**Latest results: [REPORT.md](REPORT.md)** (and `docs/index.html` for the chart).

This is an experiment, not investment advice. No real orders are ever placed.
**It costs nothing to run**: free data sources, a free AI model, and GitHub
Actions, which is free and unlimited for public repositories (a private repo gets
2,000 free minutes a month; the daily bot alone uses about 100). The only paid
part, the optional `claude` account, stays off unless you add an API key.

## The strategies

| Account | How it scores each stock |
|---|---|
| `finbert` | **Free AI reader.** [FinBERT](https://huggingface.co/ProsusAI/finbert), an open-source model trained on financial news, reads each headline as a whole sentence (so "Character.AI files for Chapter 11, puts Disney in the driver's seat" is good news for Disney). Runs on the GitHub Actions machine: no account, no key, no cost. |
| `claude` | Optional, **paid**: Claude reads each headline and rates its likely next-day impact. Off unless `ANTHROPIC_API_KEY` is set. |
| `news` | The same headlines scored by a finance word list (`papertrader/sentiment.py`): "beats estimates", "cuts guidance", "downgrade", with negation handling. |
| `hybrid` | 60% `news` score + 40% `momentum` score. |
| `momentum` | Prices only: 20- and 60-day returns scaled by the stock's volatility. The no-news baseline. |
| `equal_weight` | Holds all 20 stocks at 5% each. **The fair yardstick**: the list is today's biggest companies, picked with hindsight, so simply holding them has beaten SPY by a wide margin in the past. |
| `benchmark` | Buys SPY once and holds it. What you'd get by doing nothing clever. |

`news`, `finbert` (and `claude`, if on) read the same headlines and trade with
the same rules, so the gaps between them measure what a smarter reader adds. `momentum` shows whether the
news helps at all compared to price trends.

Headline scores are combined per stock as a recency-weighted average (weight
halves every 24 hours, 72-hour window), shrunk toward 0 so that one story moves
the score less than a steady stream of stories pointing the same way.

**Headline filtering.** About a third of what the per-ticker feeds return is
about other companies ("BigBear.ai Stock Soared" shows up under NVDA), and more
is filler. Before scoring, a headline must name the company or its ticker
(`aliases` in `config.json` adds names like Google or Exxon); fund-filing spam
("XYZ Wealth LLC Buys 1,234 Shares of...") and market wraps are dropped; and
questions, "X vs Y" comparisons and listicles count at a quarter weight. The
rules live in `papertrader/news.py` and are tested against real headlines.

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
4. **News**: new headlines from Yahoo Finance and Google News RSS. Off-topic
   and junk headlines are dropped (see above); the rest are scored and saved to
   `data/news/YYYY-MM-DD.jsonl`. FinBERT (and Claude) score each headline once;
   word-list scores are recomputed on every run, so word-list fixes apply
   immediately. If a model fails to load on some day, its account keeps its
   positions instead of selling everything.
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

- **Return vs equal weight and vs SPY**: did it beat simply holding the whole
  list, or the index?
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
close all year), again at 01:15 UTC as a backup in case GitHub drops a scheduled
run, and on Sunday evening (to read weekend news before Monday), then commits
`data/`, `REPORT.md` and `docs/` back to the repo. Re-runs are safe: no order
fills twice; the pending decision is simply refreshed with the newest headlines.

1. Push this repo to GitHub. Actions are on by default.
2. Nothing else is needed. The workflow installs FinBERT (CPU-only PyTorch)
   and caches the model, adding about a minute to each run.
   *Optional and paid:* to add the `claude` account, add an Anthropic API key
   under **Settings → Secrets and variables → Actions → New repository secret**,
   named `ANTHROPIC_API_KEY`. Without it the other accounts run as normal.
3. To start right away instead of waiting for the evening, go to **Actions →
   Daily paper trade → Run workflow**. Run it after the 4pm New York close: a run
   during market hours updates the accounts but places no orders.

**Claude cost (only if you add a key)**: each new headline is scored once (about 150–300 a day across 20
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
# optional, for the free FinBERT account:
pip install "torch>=2.6" --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements-ml.txt

python -m papertrader run          # the daily cycle (run after the close)
python -m papertrader status       # leaderboard in the terminal
python -m papertrader report       # rebuild REPORT.md and docs/index.html
python -m papertrader backtest     # replay momentum vs SPY over the last 2 years
python -m papertrader research     # walk-forward test of price-only variants (10 years)
python -m pytest -q                # tests (offline)
```

FinBERT turns on automatically when `torch` and `transformers` are installed.
`ANTHROPIC_API_KEY` in the environment turns on the `claude` account;
`run --no-claude` skips it. If you run locally *and* on Actions, pick one place:
both write the same `data/` folder.

## Research

Two GitHub Actions workflows test ideas on past data, with results committed to
`research/`:

- **Strategy research** (`research/RESULTS.md`, monthly or on demand): a dozen
  price-only variants (momentum over different windows, reversal, low
  volatility, trend filters) over 10 years. Each is scored on the first half and
  the second half separately: pick on the first, check on the second.
- **News backfill and research** (`research/NEWS.md`, every 3 hours until done):
  pulls about 3
  months of past headlines per stock from GDELT's free news index, runs them
  through the same filter and both free scorers (word list and FinBERT), and
  measures whether the news score
  predicted the next day, both close to close and as actually tradable (open to
  next open).

What the price research found (10 years, through 2026-10): holding the whole
list equally had a Sharpe ratio of 1.12 / 1.21 in the two halves, far above
SPY's 0.69 / 0.84, which is the hindsight effect. Longer momentum (6- and
12-month) earned more return than equal weight but with more risk; no variant
beat it on a risk-adjusted basis in both halves. The live momentum rule's
next-day IC was +0.013 (t = 2.0): real but tiny.

`python -m papertrader backtest` replays `momentum` and `benchmark` through the
exact live account code, and `research`, `backfill-news` and `news-research` run
the above locally.

## Configuration (`config.json`)

| Key | Meaning |
|---|---|
| `starting_cash` | Fake money per account (default 100,000). Change only before the first run. |
| `universe` | Ticker → company name. The name is used for the Google News search. |
| `aliases` | Other names a headline may use for a company (Google, Exxon, Facebook...). |
| `trading.max_positions` | Slots per account; each gets 1/N of the account (default 5). |
| `trading.slippage_bps` | Price penalty per trade, in basis points (default 5 = 0.05%). |
| `trading.min_trade_pct` | Skip rebalances smaller than this % of the account (default 2). |
| `news.lookback_hours`, `news.half_life_hours` | Window and decay for headline scores (72 h, 24 h). |
| `news.opinion_weight` | How much questions, comparisons and listicles count vs. news (0.25). |
| `strategies.<name>.entry` / `.exit` | Score needed to buy / score at or below which a holding is sold. |
| `strategies.<name>.enabled` | `true`, `false`, or `"auto"` (finbert: on when installed; claude: on when a key is set). |

## Data files

| File | Contents |
|---|---|
| `data/accounts.json` | Cash, shares, and the pending order for each account. |
| `data/equity.csv` | Each account's value at every close. |
| `data/trades.csv` | Every simulated fill. |
| `data/predictions.csv` | Every prediction with its outcome once graded. |
| `data/news/*.jsonl` | Every headline seen, with its word-list, FinBERT and Claude scores. |
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
