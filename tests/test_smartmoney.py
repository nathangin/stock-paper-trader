import json

import pytest

from papertrader import smartmoney as sm
from tests.conftest import make_history, weekdays

INFOTABLE = """<?xml version="1.0" encoding="UTF-8"?>
<informationTable xmlns="http://www.sec.gov/edgar/document/thirteenf/informationtable">
  <infoTable>
    <nameOfIssuer>APPLE INC</nameOfIssuer><titleOfClass>COM</titleOfClass><cusip>037833100</cusip>
    <value>1000</value><shrsOrPrnAmt><sshPrnamt>10</sshPrnamt><sshPrnamtType>SH</sshPrnamtType></shrsOrPrnAmt>
  </infoTable>
  <infoTable>
    <nameOfIssuer>APPLE INC</nameOfIssuer><titleOfClass>COM</titleOfClass><cusip>037833100</cusip>
    <value>500</value><shrsOrPrnAmt><sshPrnamt>5</sshPrnamt><sshPrnamtType>SH</sshPrnamtType></shrsOrPrnAmt>
  </infoTable>
  <infoTable>
    <nameOfIssuer>APPLE INC</nameOfIssuer><titleOfClass>CALL</titleOfClass><cusip>037833100</cusip>
    <value>999</value><shrsOrPrnAmt><sshPrnamt>9</sshPrnamt><sshPrnamtType>SH</sshPrnamtType></shrsOrPrnAmt>
    <putCall>Call</putCall>
  </infoTable>
  <infoTable>
    <nameOfIssuer>OCCIDENTAL PETE CORP</nameOfIssuer><titleOfClass>COM</titleOfClass><cusip>674599105</cusip>
    <value>2,000</value><shrsOrPrnAmt><sshPrnamt>40</sshPrnamt><sshPrnamtType>SH</sshPrnamtType></shrsOrPrnAmt>
  </infoTable>
</informationTable>"""


def test_parse_infotable_aggregates_and_skips_options():
    h = sm.parse_infotable(INFOTABLE)
    assert h["037833100"] == {"name": "APPLE INC", "value": 1500.0, "shares": 15.0}
    assert h["674599105"]["value"] == 2000.0


def test_list_13f_keeps_original_filings():
    sub = {"filings": {"recent": {
        "form": ["13F-HR", "13F-HR/A", "13F-HR", "4", "13F-HR"],
        "accessionNumber": ["a3", "a2x", "a2", "x", "a1"],
        "filingDate": ["2026-08-14", "2026-06-01", "2026-05-15", "2026-05-01", "2026-02-14"],
        "reportDate": ["2026-06-30", "2026-03-31", "2026-03-31", "", "2025-12-31"],
    }}}
    assert [f["accession"] for f in sm.list_13f(sub)] == ["a1", "a2", "a3"]


def test_find_infotable():
    assert sm.find_infotable(["primary_doc.xml", "0001.xml", "a-index.html"]) == "0001.xml"
    assert sm.find_infotable(["primary_doc.xml", "xyz.xml", "form13fInfoTable.xml"]) == "form13fInfoTable.xml"
    assert sm.find_infotable(["primary_doc.xml"]) is None


def test_normalize_name():
    assert sm.normalize_name("Apple Inc.") == sm.normalize_name("APPLE INC") == "APPLE"
    assert sm.normalize_name("Alphabet Inc Class A") == "ALPHABET"


class FakeFigi:
    def __init__(self):
        self.calls = 0

    def post(self, url, json, timeout):
        self.calls += 1
        table = {"037833100": "AAPL", "084670702": "BRK/B"}

        class R:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self_inner):
                out = []
                for job in json:
                    t = table.get(job["idValue"])
                    if t:
                        out.append({"data": [{"ticker": t, "securityType2": "Common Stock"}]})
                    elif job["idValue"] == "78462F103":
                        out.append({"data": [{"ticker": "SPY", "securityType2": "Mutual Fund"}]})
                    else:
                        out.append({"warning": "No identifier found."})
                return out
        return R()


def test_ticker_map_uses_openfigi_and_caches(tmp_path):
    figi = FakeFigi()
    tm = sm.TickerMap(tmp_path / "map.json", session=figi, pause=0)
    got = tm.resolve({"037833100": "APPLE INC", "084670702": "BERKSHIRE B", "78462F103": "SPDR", "000000000": "X"})
    assert got == {"037833100": "AAPL", "084670702": "BRK-B", "78462F103": None, "000000000": None}
    again = sm.TickerMap(tmp_path / "map.json", session=figi, pause=0)
    again.resolve({"037833100": "APPLE INC"})
    assert figi.calls == 1  # served from the saved map


def fund(filed, holdings):
    return {"filed": filed, "holdings": {c: [c, v, 1] for c, v in holdings.items()}}


TICKERS = {"A": "AAA", "B": "BBB", "C": "CCC", "D": "DDD"}


def test_quarter_picks_and_filing_dates():
    data = {
        "Fund 1": {"2026-03-31": fund("2026-05-10", {"A": 50, "B": 50}),
                   "2026-06-30": fund("2026-08-10", {"A": 40, "B": 20, "C": 40})},
        "Fund 2": {"2026-03-31": fund("2026-05-12", {"A": 100}),
                   "2026-06-30": fund("2026-08-12", {"A": 70, "C": 30})},
        # Filed after the decision day: must not be used.
        "Late": {"2026-03-31": fund("2026-05-01", {"D": 100}),
                 "2026-06-30": fund("2026-09-01", {"D": 10, "B": 90})},
    }
    picks, used = sm.quarter_picks(data, TICKERS, "2026-06-30", "2026-03-31", "2026-08-15", top_n=5)
    assert sorted(used) == ["Fund 1", "Fund 2"]
    assert picks["new_buys"][0][0] == "CCC" and sorted(picks["new_buys"][0][2]) == ["Fund 1", "Fund 2"]
    assert picks["best_ideas"][0][0] == "AAA"  # top holding of both funds
    assert picks["biggest_adds"][0][0] == "CCC"
    assert "DDD" not in [p[0] for v in picks.values() for p in v]


def test_build_quarters_waits_for_the_deadline():
    days = weekdays("2026-03-02", 140)
    data = {"F": {"2026-03-31": fund("2026-05-01", {"A": 1}), "2026-06-30": fund("2026-08-01", {"A": 1, "B": 1})}}
    qs = sm.build_quarters(data, TICKERS, days, top_n=3)
    assert [q["period"] for q in qs] == ["2026-06-30"]
    assert qs[0]["decide_on"] >= "2026-08-14"  # 45 days after the quarter end


def test_quarter_ends():
    assert sm.quarter_ends("2025-09-30", "2026-04-01") == ["2025-09-30", "2025-12-31", "2026-03-31"]


def test_backtest_runs_and_reports(cfg):
    days = weekdays("2024-01-01", 560)
    hist = {s: make_history(s, days, drift=0.0005 * i, seed=i)
            for i, s in enumerate(["AAA", "BBB", "CCC", "SPY", "RSP"])}
    quarters = []
    for i, d in enumerate(days[100::63]):
        quarters.append({"period": f"q{i}", "decide_on": d, "funds": ["F"], "picks": {
            "new_buys": [("AAA", 1, ["F"]), ("GONE", 1, ["F"])],
            "best_ideas": [("BBB", 1, ["F"])],
            "biggest_adds": [("CCC", 1, ["F"])],
        }})
    bt = sm.backtest(quarters, hist, ["SPY", "RSP"], 5)
    assert set(bt["results"]) == {"new_buys", "best_ideas", "biggest_adds", "SPY buy & hold", "RSP buy & hold"}
    assert bt["missing_prices"] == ["GONE"]
    assert bt["excess"]["best_ideas"]["quarters"] >= 5
    latest = {"period": "2026-06-30", "funds": ["F"], "picks": quarters[-1]["picks"]}
    text = sm.render(latest, bt, ["F"], [{"name": "F"}])
    assert "| BBB | F |" in text and "Did copying them work?" in text


class FakeSec:
    def __init__(self, name):
        self.name = name

    def submissions(self, cik):
        return {"name": self.name, "filings": {"recent": {
            "form": ["13F-HR"], "accessionNumber": ["0001-26-000001"],
            "filingDate": ["2026-08-14"], "reportDate": ["2026-06-30"]}}}

    def filing_files(self, cik, acc):
        return ["primary_doc.xml", "infotable.xml"]

    def filing_file(self, cik, acc, name):
        return INFOTABLE


def test_fetch_fund_checks_the_cik_name(tmp_path):
    cache = sm.FilingCache(tmp_path)
    good = sm.fetch_fund(FakeSec("BERKSHIRE HATHAWAY INC"), cache, {"name": "B", "cik": "1067983", "match": "BERKSHIRE"}, "2026-01-01")
    assert good["2026-06-30"]["holdings"]["037833100"] == ["APPLE INC", 1500, 15]
    assert cache.get("1067983", "2026-06-30") is not None
    wrong = sm.fetch_fund(FakeSec("SOMEONE ELSE LLC"), cache, {"name": "B", "cik": "1", "match": "BERKSHIRE"}, "2026-01-01")
    assert wrong == {}
