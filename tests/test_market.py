from datetime import datetime, timezone

from papertrader.market import (
    History,
    can_decide,
    drop_unfinished_bar,
    next_session_open,
    parse_stooq_csv,
    parse_yahoo_chart,
)
from tests.conftest import flat_history

# 2026-10-08 and 2026-10-09 at 9:30am New York (13:30 UTC).
TS1, TS2 = 1791466200, 1791552600


def yahoo_payload():
    return {
        "chart": {
            "result": [
                {
                    "meta": {"exchangeTimezoneName": "America/New_York"},
                    "timestamp": [TS1, TS2, TS2 + 86400],
                    "indicators": {
                        "quote": [
                            {
                                "open": [10.0, 11.0, None],
                                "high": [10.5, 11.5, None],
                                "low": [9.5, 10.5, None],
                                "close": [10.2, 11.2, None],
                                "volume": [100, 200, None],
                            }
                        ]
                    },
                    "events": {
                        "splits": {str(TS2): {"date": TS2, "numerator": 4, "denominator": 1}},
                        "dividends": {str(TS1): {"date": TS1, "amount": 0.25}},
                    },
                }
            ],
            "error": None,
        }
    }


def test_parse_yahoo_chart_bars_and_events():
    hist = parse_yahoo_chart("XYZ", yahoo_payload())
    assert [b.date for b in hist.bars] == ["2026-10-08", "2026-10-09"]  # null bar dropped
    assert hist.bars[1].open == 11.0 and hist.bars[1].close == 11.2
    assert hist.splits == [{"date": "2026-10-09", "ratio": 4.0}]
    assert hist.dividends == [{"date": "2026-10-08", "amount": 0.25}]


def test_parse_yahoo_chart_error_raises():
    import pytest

    with pytest.raises(ValueError):
        parse_yahoo_chart("XYZ", {"chart": {"result": None, "error": {"code": "Not Found"}}})


def test_parse_stooq_csv():
    text = "Date,Open,High,Low,Close,Volume\n2026-10-08,10,11,9,10.5,1000\n2026-10-09,10.5,12,10,11.5,2000\n"
    hist = parse_stooq_csv("XYZ", text)
    assert [b.close for b in hist.bars] == [10.5, 11.5]
    assert hist.splits == []


def test_drop_unfinished_bar_only_before_close():
    days = ["2026-10-08", "2026-10-09"]
    during = datetime(2026, 10, 9, 18, 0, tzinfo=timezone.utc)  # 2pm New York
    after = datetime(2026, 10, 9, 21, 0, tzinfo=timezone.utc)  # 5pm New York
    assert len(drop_unfinished_bar(flat_history("X", days, [1, 1], [1, 1]), during).bars) == 1
    assert len(drop_unfinished_bar(flat_history("X", days, [1, 1], [1, 1]), after).bars) == 2
    assert drop_unfinished_bar(History("X"), during).bars == []


def test_next_session_open_skips_weekend():
    assert next_session_open("2026-10-09").isoformat() == "2026-10-12T09:30:00-04:00"  # Fri -> Mon


def test_can_decide_until_next_open():
    asof = "2026-10-09"  # a Friday
    assert can_decide(asof, datetime(2026, 10, 9, 21, 30, tzinfo=timezone.utc))
    assert can_decide(asof, datetime(2026, 10, 11, 22, 0, tzinfo=timezone.utc))  # Sunday evening
    assert not can_decide(asof, datetime(2026, 10, 12, 14, 0, tzinfo=timezone.utc))  # Monday 10am NY
