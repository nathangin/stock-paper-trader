import pytest

from papertrader.predictions import grade, make_predictions, merge, spearman, summarize
from tests.conftest import flat_history

DAYS = ["2026-10-05", "2026-10-06"]


def hist():
    return {
        "UP": flat_history("UP", DAYS, [10, 10], [10, 11]),
        "DN": flat_history("DN", DAYS, [10, 10], [10, 9]),
        "FL": flat_history("FL", DAYS, [10, 10], [10, 10.1]),
    }


def test_make_and_grade():
    h = hist()
    rows = make_predictions("2026-10-05", "s", {"UP": 0.5, "DN": 0.4, "FL": 0.01}, h, min_abs_score=0.05)
    calls = {r["symbol"]: r["call"] for r in rows}
    assert calls == {"UP": 1, "DN": 1, "FL": 0}
    assert grade(rows, h) == 3
    by = {r["symbol"]: r for r in rows}
    assert by["UP"]["correct"] == 1 and by["DN"]["correct"] == 0 and by["FL"]["correct"] == ""
    assert by["UP"]["ret"] == pytest.approx(0.1)
    assert grade(rows, h) == 0  # already graded


def test_merge_replaces_same_day_and_strategy():
    old = [{"date": "d1", "strategy": "s", "symbol": "A"}, {"date": "d1", "strategy": "t", "symbol": "A"}]
    new = [{"date": "d1", "strategy": "s", "symbol": "B"}]
    out = merge(old, new)
    assert [(r["strategy"], r["symbol"]) for r in out] == [("t", "A"), ("s", "B")]


def test_summarize_counts_only_calls():
    h = hist()
    rows = make_predictions("2026-10-05", "s", {"UP": 0.5, "DN": -0.4, "FL": 0.01}, h, 0.05)
    grade(rows, h)
    s = summarize([{k: str(v) for k, v in r.items()} for r in rows], "s")  # as read back from CSV
    assert s["calls"] == 2 and s["hit_rate"] == 1.0
    assert s["edge_bps"] == pytest.approx(1000)
    assert 0 < s["p_value"] <= 1


def test_spearman():
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
    assert spearman([1, 1, 1], [1, 2, 3]) is None
