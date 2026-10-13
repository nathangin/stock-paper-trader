import copy
import json
from datetime import datetime, timedelta, timezone

import pytest

from papertrader.engine import run_daily
from papertrader.news import Headline, headline_id
from papertrader.store import Store
from tests.conftest import make_history, weekdays
from tests.test_claude_scorer import fake_client, response

DAYS = weekdays("2026-06-01", 90)  # ends Wed 2026-10-07; all in daylight time
TICKERS = ["AAA", "BBB", "CCC", "DDD", "EEE"]


def full_histories():
    h = {t: make_history(t, DAYS, drift=0.001 * (i - 2), seed=i) for i, t in enumerate(TICKERS)}
    h["SPY"] = make_history("SPY", DAYS, start_price=500, drift=0.0005, vol=0.008, seed=99)
    return h


def evening(day, hour=21, minute=30):
    d = datetime.fromisoformat(day)
    return d.replace(hour=hour, minute=minute, tzinfo=timezone.utc)


class Market:
    """Serves price history as it would have looked at a given time."""

    def __init__(self):
        self.full = full_histories()
        self.through = None
        self.calls = 0

    def __call__(self, symbols):
        self.calls += 1
        out = {}
        for s in symbols:
            h = copy.deepcopy(self.full[s])
            h.bars = [b for b in h.bars if b.date <= self.through]
            out[s] = h
        return out, []


def news_for(now):
    def mk(ticker, title, hours_ago):
        return Headline(headline_id(ticker, title), ticker, title, (now - timedelta(hours=hours_ago)).isoformat())

    return lambda universe: [
        mk("AAA", f"Alpha Corp beats estimates and raises guidance {now:%d}", 1),
        mk("AAA", f"Alpha Corp shares surge to record high {now:%d}", 2),
        mk("AAA", f"Analyst upgrades Alpha Corp {now:%d}", 3),
        mk("EEE", f"Epsilon plunges after it cuts guidance {now:%d}", 1),
        mk("CCC", f"Gamma Co to present at conference {now:%d}", 1),
    ]


@pytest.fixture
def market():
    return Market()


def run(cfg, tmp_path, market, through, now, **kw):
    market.through = through
    return run_daily(cfg, tmp_path, market, news_for(now), now=now, use_claude=False, **kw)


def test_two_day_cycle(cfg, tmp_path, market):
    d1, d2 = DAYS[-3], DAYS[-2]
    s1 = run(cfg, tmp_path, market, d1, evening(d1))
    assert s1["asof"] == d1 and s1["decided"] and s1["trades"] == 0
    assert s1["strategies"] == ["momentum", "news", "hybrid", "equal_weight", "benchmark"]
    store = Store(tmp_path)
    accounts = store.load_accounts()
    assert set(accounts) == {"momentum", "news", "hybrid", "equal_weight", "benchmark"}
    assert accounts["equal_weight"].pending["targets"] == {t: 0.2 for t in TICKERS}
    assert "AAA" in accounts["news"].pending["targets"]
    assert "EEE" not in accounts["news"].pending["targets"]
    assert accounts["benchmark"].pending["targets"] == {"SPY": 1.0}
    preds = store.read_rows(store.predictions_path)
    assert {r["strategy"] for r in preds} == {"momentum", "news", "hybrid"}
    assert all(r["next_date"] == "" for r in preds)

    s2 = run(cfg, tmp_path, market, d2, evening(d2))
    assert s2["trades"] > 0
    trades = store.trade_rows()
    assert {t["date"] for t in trades} == {d2}
    aaa_open = market.full["AAA"].bar_on(d2).open
    news_buy = next(t for t in trades if t["strategy"] == "news" and t["symbol"] == "AAA")
    assert float(news_buy["price"]) == pytest.approx(aaa_open * 1.0005, rel=1e-6)
    graded = [r for r in store.read_rows(store.predictions_path) if r["date"] == d1]
    assert graded and all(r["next_date"] == d2 for r in graded)
    equity = store.equity_rows()
    assert [r["date"] for r in equity if r["strategy"] == "news"] == [d1, d2]
    signals = json.loads(store.signals_path.read_text())
    assert signals["asof"] == d2 and "AAA" in signals["headlines"]


def test_rerun_same_evening_is_idempotent(cfg, tmp_path, market):
    d1, d2 = DAYS[-3], DAYS[-2]
    run(cfg, tmp_path, market, d1, evening(d1))
    run(cfg, tmp_path, market, d2, evening(d2))
    store = Store(tmp_path)
    n_trades, n_preds = len(store.trade_rows()), len(store.read_rows(store.predictions_path))
    again = run(cfg, tmp_path, market, d2, evening(d2, 23))
    assert again["trades"] == 0 and again["new_headlines"] == 0
    assert len(store.trade_rows()) == n_trades
    assert len(store.read_rows(store.predictions_path)) == n_preds


def test_no_orders_once_market_has_opened(cfg, tmp_path, market):
    d1, d2 = DAYS[-3], DAYS[-2]
    run(cfg, tmp_path, market, d1, evening(d1))
    pending_before = Store(tmp_path).load_accounts()["news"].pending
    # Midday on d2: today's bar is partial and gets dropped, so the latest close is d1 and
    # the d2 open has already happened. Deciding now would be look-ahead.
    s = run(cfg, tmp_path, market, d2, evening(d2, 16, 0))
    assert s["asof"] == d1 and not s["decided"]
    assert Store(tmp_path).load_accounts()["news"].pending == pending_before


def test_claude_strategy_uses_claude_scores(cfg, tmp_path, market):
    d1 = DAYS[-3]

    def responder(kw):
        lines = kw["messages"][0]["content"].split("\n")[2:]
        items = [json.loads(line) for line in lines if line.strip()]
        return response({"scores": [
            {"id": i["id"], "score": 0.9 if i["ticker"] == "CCC" else 0.0, "reason": "test"} for i in items
        ]})

    client, msgs = fake_client(responder)
    market.through = d1
    s = run_daily(cfg, tmp_path, market, news_for(evening(d1)), now=evening(d1),
                  use_claude=True, claude_client=client)
    assert "claude" in s["strategies"] and len(msgs.calls) == 1
    accounts = Store(tmp_path).load_accounts()
    # Claude liked CCC (which the word list scores 0) and was neutral on AAA.
    assert set(accounts["claude"].pending["targets"]) == {"CCC"}
    assert "CCC" not in accounts["news"].pending["targets"]


def test_missing_benchmark_aborts(cfg, tmp_path):
    def no_prices(symbols):
        return {}, list(symbols)

    with pytest.raises(RuntimeError):
        run_daily(cfg, tmp_path, no_prices, lambda u: [], now=evening(DAYS[-1]), use_claude=False)


def test_account_with_missing_held_prices_is_skipped_not_crashed(cfg, tmp_path, market):
    d1, d2, d3 = DAYS[-4], DAYS[-3], DAYS[-2]
    run(cfg, tmp_path, market, d1, evening(d1))
    run(cfg, tmp_path, market, d2, evening(d2))
    store = Store(tmp_path)
    held = store.load_accounts()["news"].positions
    assert "AAA" in held
    pending = store.load_accounts()["news"].pending

    def without_aaa(symbols):
        out, failed = market([s for s in symbols if s != "AAA"])
        return out, ["AAA"]

    market.through = d3
    s = run_daily(cfg, tmp_path, without_aaa, news_for(evening(d3)), now=evening(d3), use_claude=False)
    assert "news" in s["stale_accounts"] and "momentum" not in s["stale_accounts"]
    news = store.load_accounts()["news"]
    assert news.last_processed == d2 and news.pending == pending
    # Next day the prices are back and the account catches up on both days.
    run(cfg, tmp_path, market, DAYS[-1], evening(DAYS[-1]))
    rows = [r["date"] for r in store.equity_rows() if r["strategy"] == "news"]
    assert rows == [d1, d2, d3, DAYS[-1]]
