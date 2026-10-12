"""Paper brokerage account: cash, fractional shares, and orders filled at the next open.

Timeline for one decision:
  1. After the close on day D the bot decides target weights. They are stored
     as a pending order, nothing trades yet.
  2. The order fills at the open of the first trading day after D, at that
     day's opening price plus slippage, sells before buys.
  3. Positions are marked to market at each close after that.

Filling at the next open (instead of the close the signal was computed on)
keeps the test honest: news that came out after the close can't be traded at
a price from before it came out.
"""

from dataclasses import asdict, dataclass, field


@dataclass
class Account:
    name: str
    cash: float
    positions: dict = field(default_factory=dict)  # symbol -> shares (fractional)
    pending: dict | None = None  # {"decided_on": "YYYY-MM-DD", "decided_at": iso, "targets": {sym: weight}}
    last_processed: str | None = None  # last trading day already filled/marked
    seen_splits: list = field(default_factory=list)  # "SYM:YYYY-MM-DD" already applied or skipped
    started_on: str | None = None

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    def equity(self, prices):
        return self.cash + sum(sh * prices[s] for s, sh in self.positions.items())


def apply_splits(account, histories):
    """Rescale share counts for splits not seen before.

    Yahoo rewrites the whole price history after a split, so share counts
    bought before it must be multiplied by the split ratio to keep value the
    same. Splits of stocks the account didn't hold are just marked as seen.
    """
    events = []
    for sym, hist in histories.items():
        for s in hist.splits:
            key = f"{sym}:{s['date']}"
            if key not in account.seen_splits:
                events.append((key, sym, s["ratio"]))
    for key, sym, ratio in events:
        if sym in account.positions:
            account.positions[sym] *= ratio
        account.seen_splits.append(key)
    return [e[0] for e in events if e[1] in account.positions]


def fill_pending(account, histories, day, slippage_bps, min_trade_pct):
    """Fill the pending order at the open on `day`. Returns the list of trades made.

    Trades smaller than `min_trade_pct` of equity are skipped (except full
    exits) to avoid paying slippage on tiny rebalances. Sells go first; if the
    buys then cost more than the cash available they are all scaled down by the
    same factor. A symbol with no bar that day (halted, bad data) is left as is.
    """
    order = account.pending
    opens = {}
    for sym in set(order["targets"]) | set(account.positions):
        bar = histories[sym].bar_on(day) if sym in histories else None
        if bar is not None:
            opens[sym] = bar.open
    tradable = set(opens)
    marks = dict(opens)
    for sym in account.positions:
        if sym not in marks:
            marks[sym] = last_close(histories, sym, day)
    equity = account.equity(marks)
    slip = slippage_bps / 10_000

    deltas = {}
    for sym in sorted(tradable):
        target = order["targets"].get(sym, 0.0) * equity / opens[sym]
        delta = target - account.positions.get(sym, 0.0)
        full_exit = target == 0 and sym in account.positions
        if full_exit or abs(delta * opens[sym]) >= equity * min_trade_pct / 100:
            deltas[sym] = delta

    trades = []
    for sym, delta in deltas.items():
        if delta < 0:
            price = opens[sym] * (1 - slip)
            account.cash += -delta * price
            remaining = account.positions[sym] + delta
            if remaining <= 1e-9:
                del account.positions[sym]
            else:
                account.positions[sym] = remaining
            trades.append(_trade(account, day, sym, "SELL", -delta, price))

    buys = {s: d for s, d in deltas.items() if d > 0}
    cost = sum(d * opens[s] * (1 + slip) for s, d in buys.items())
    scale = min(1.0, account.cash / cost) if cost > 0 else 1.0
    for sym, delta in buys.items():
        shares = delta * scale
        price = opens[sym] * (1 + slip)
        account.cash -= shares * price
        account.positions[sym] = account.positions.get(sym, 0.0) + shares
        trades.append(_trade(account, day, sym, "BUY", shares, price))

    account.cash = max(account.cash, 0.0)  # float dust after scaling
    account.pending = None
    return trades


def _trade(account, day, sym, side, shares, price):
    return {
        "date": day,
        "strategy": account.name,
        "symbol": sym,
        "side": side,
        "shares": round(shares, 6),
        "price": round(price, 4),
        "value": round(shares * price, 2),
    }


def last_close(histories, sym, day):
    bars = histories[sym].bars_until(day) if sym in histories else []
    if not bars:
        raise KeyError(f"No price for {sym} on or before {day}")
    return bars[-1].close


def trading_days(histories, after, through):
    days = {b.date for h in histories.values() for b in h.bars}
    return sorted(d for d in days if (after is None or d > after) and d <= through)


def process_new_sessions(account, histories, asof, trading_cfg):
    """Bring an account up to date through the close on `asof`.

    Walks each trading day since the account was last processed: pays
    dividends whose ex-date is that day (to the shares held at the previous
    close), fills a pending order at that day's open, and marks the account at
    that day's close. Returns (trades, equity rows).
    """
    if account.last_processed is not None and account.last_processed >= asof:
        return [], []
    apply_splits(account, histories)
    days = trading_days(histories, account.last_processed, asof)
    if account.last_processed is None:
        days = days[-1:]  # a new account starts in cash at the latest close
    trades, rows = [], []
    for day in days:
        for sym, shares in list(account.positions.items()):
            for div in histories[sym].dividends if sym in histories else []:
                if div["date"] == day:
                    account.cash += shares * div["amount"]
        if account.pending and day > account.pending["decided_on"]:
            trades += fill_pending(
                account, histories, day, trading_cfg["slippage_bps"], trading_cfg["min_trade_pct"]
            )
        prices = {s: last_close(histories, s, day) for s in account.positions}
        rows.append({
            "date": day,
            "strategy": account.name,
            "equity": round(account.equity(prices), 2),
            "cash": round(account.cash, 2),
        })
    account.last_processed = asof
    if account.started_on is None:
        account.started_on = asof
    return trades, rows
