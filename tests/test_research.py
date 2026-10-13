import pytest

from papertrader.research import align, render, run_research, simulate, stats
from tests.conftest import flat_history, make_history, weekdays


def test_simulate_buy_and_hold_matches_prices():
    days = weekdays("2025-01-01", 4)
    h = {"SPY": flat_history("SPY", days, [100, 102, 104, 108], [101, 103, 106, 110])}
    cal, opens, closes = align(h, ["SPY"], "SPY")
    eq, turnover = simulate(cal, opens, closes, lambda t, w: {"SPY": 1.0} if not w else None, 0, slippage_bps=10)
    # Bought at the open on day 1 (102, minus 10 bp), held to the last close (110).
    assert eq[-1] == pytest.approx(110 / 102 * (1 - 0.001))
    assert len(eq) == 4


def test_simulate_cash_stays_flat():
    days = weekdays("2025-01-01", 5)
    h = {"SPY": flat_history("SPY", days, [100] * 5, [105] * 5)}
    cal, opens, closes = align(h, ["SPY"], "SPY")
    eq, turnover = simulate(cal, opens, closes, lambda t, w: {}, 0)
    assert eq == [1.0] * 5 and turnover == 0


def test_stats():
    s = stats([1.0, 1.1, 0.99, 1.2])
    assert s["max_dd"] == pytest.approx(0.99 / 1.1 - 1)
    assert s["total"] == pytest.approx(0.2)


def test_run_research_end_to_end(cfg):
    days = weekdays("2020-01-01", 620)
    h = {t: make_history(t, days, drift=0.0004 * i, seed=i) for i, t in enumerate(cfg["universe"])}
    h["SPY"] = make_history("SPY", days, start_price=300, drift=0.0003, seed=42)
    res = run_research(cfg, h)
    assert "SPY buy & hold" in res["results"]
    for r in res["results"].values():
        assert set(r) == {"first", "second"}
    text = render(res)
    assert "| Equal weight universe (monthly) |" in text
    assert res["momentum_ic"]["days"] > 100


def test_run_research_needs_history(cfg):
    days = weekdays("2020-01-01", 300)
    h = {t: make_history(t, days) for t in list(cfg["universe"]) + ["SPY"]}
    with pytest.raises(ValueError):
        run_research(cfg, h)
