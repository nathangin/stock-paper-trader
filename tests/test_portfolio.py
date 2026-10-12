import pytest

from papertrader.portfolio import Account, apply_splits, process_new_sessions
from tests.conftest import flat_history

DAYS = ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08"]
TRADING = {"slippage_bps": 10, "min_trade_pct": 2.0}


def histories():
    return {
        "AAA": flat_history("AAA", DAYS, [100, 102, 110, 120], [101, 108, 115, 118]),
        "BBB": flat_history("BBB", DAYS, [50, 50, 50, 50], [50, 50, 50, 50]),
        "SPY": flat_history("SPY", DAYS, [400, 400, 400, 400], [400, 401, 402, 403]),
    }


def test_new_account_starts_in_cash_on_latest_close():
    acct = Account("x", 10_000)
    trades, rows = process_new_sessions(acct, histories(), "2026-10-06", TRADING)
    assert trades == []
    assert rows == [{"date": "2026-10-06", "strategy": "x", "equity": 10_000, "cash": 10_000}]
    assert acct.last_processed == "2026-10-06"


def test_order_fills_at_next_open_with_slippage():
    h = histories()
    acct = Account("x", 10_000, last_processed="2026-10-05")
    acct.pending = {"decided_on": "2026-10-05", "decided_at": "", "targets": {"AAA": 0.5}}
    trades, rows = process_new_sessions(acct, h, "2026-10-07", TRADING)
    (t,) = trades
    assert t["date"] == "2026-10-06" and t["side"] == "BUY"
    assert t["price"] == pytest.approx(102 * 1.001)  # open on the next day, plus 10 bp
    shares = 5_000 / 102
    assert acct.positions["AAA"] == pytest.approx(shares)
    assert acct.pending is None
    # Marked at each close after the fill.
    assert [r["date"] for r in rows] == ["2026-10-06", "2026-10-07"]
    cash = 10_000 - shares * 102 * 1.001
    assert rows[-1]["equity"] == pytest.approx(cash + shares * 115, abs=0.01)


def test_order_waits_when_next_bar_not_available():
    acct = Account("x", 10_000, last_processed="2026-10-07")
    acct.pending = {"decided_on": "2026-10-08", "decided_at": "", "targets": {"AAA": 0.5}}
    trades, _ = process_new_sessions(acct, histories(), "2026-10-08", TRADING)
    assert trades == [] and acct.pending is not None


def test_sells_before_buys_and_full_exit():
    h = histories()
    acct = Account("x", 0.0, positions={"AAA": 100}, last_processed="2026-10-05")
    acct.pending = {"decided_on": "2026-10-05", "decided_at": "", "targets": {"BBB": 1.0}}
    trades, _ = process_new_sessions(acct, h, "2026-10-06", TRADING)
    assert [t["side"] for t in trades] == ["SELL", "BUY"]
    assert "AAA" not in acct.positions
    proceeds = 100 * 102 * 0.999
    # Buys are scaled down to the cash the sale raised (slippage means it can't buy the full target).
    assert acct.positions["BBB"] * 50 * 1.001 == pytest.approx(proceeds)
    assert acct.cash == pytest.approx(0, abs=1e-6)


def test_small_rebalances_are_skipped():
    h = histories()
    acct = Account("x", 5_000, positions={"BBB": 99}, last_processed="2026-10-05")  # 99*50 = 4950
    acct.pending = {"decided_on": "2026-10-05", "decided_at": "", "targets": {"BBB": 0.5}}
    trades, _ = process_new_sessions(acct, h, "2026-10-06", TRADING)
    assert trades == []  # target is 4975: a 25-dollar trade is under 2% of equity


def test_split_rescales_shares_once():
    h = histories()
    h["AAA"].splits = [{"date": "2026-10-07", "ratio": 2.0}]
    acct = Account("x", 0.0, positions={"AAA": 10})
    assert apply_splits(acct, h) == ["AAA:2026-10-07"]
    assert acct.positions["AAA"] == 20
    apply_splits(acct, h)
    assert acct.positions["AAA"] == 20


def test_dividend_paid_to_holder_at_previous_close():
    h = histories()
    h["BBB"].dividends = [{"date": "2026-10-06", "amount": 1.0}]
    acct = Account("x", 0.0, positions={"BBB": 10}, last_processed="2026-10-05")
    # The stock is sold at the open on the ex-date, but it was held at the previous close.
    acct.pending = {"decided_on": "2026-10-05", "decided_at": "", "targets": {}}
    process_new_sessions(acct, h, "2026-10-06", TRADING)
    assert acct.cash == pytest.approx(10 * 50 * 0.999 + 10)
