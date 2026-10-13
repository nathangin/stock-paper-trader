import json
from datetime import datetime, timedelta, timezone

import pytest
import requests

from papertrader.history import (
    GdeltError, HistoryStore, backfill, decision_time, evaluate_news, gdelt_query, parse_gdelt,
    render_news, windows,
)
from papertrader.news import Headline, headline_id
from tests.conftest import make_history, weekdays


def test_gdelt_query_and_parse():
    assert gdelt_query(["Visa", "V"]) == '("Visa") (stock OR shares) sourcelang:english'
    payload = {"articles": [
        {"title": "Visa beats estimates", "seendate": "20260713T154500Z", "domain": "ex.com", "url": "u"},
        {"title": "", "seendate": "20260713T154500Z"},
        {"title": "Bad date", "seendate": "nope"},
    ]}
    (h,) = parse_gdelt(payload, "V")
    assert h.published == "2026-07-13T15:45:00+00:00" and h.feed == "gdelt"
    assert parse_gdelt({}, "V") == []


def test_decision_time_is_evening_new_york():
    assert decision_time("2026-07-13") == datetime(2026, 7, 13, 21, 30, tzinfo=timezone.utc)  # EDT
    assert decision_time("2026-12-14") == datetime(2026, 12, 14, 22, 30, tzinfo=timezone.utc)  # EST


class FakeResp:
    def __init__(self, payload=None, text=None, status=200):
        self.text = text if text is not None else json.dumps(payload)
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


class FakeSession:
    def __init__(self, broken=False):
        self.calls = []
        self.headers = {}
        self.broken = broken

    def get(self, url, params, timeout):
        self.calls.append(params)
        if self.broken:
            return FakeResp(text="<html>Service unavailable</html>", status=503)
        end = datetime.strptime(params["enddatetime"], "%Y%m%d%H%M%S")
        stamp = (end - timedelta(hours=5)).strftime("%Y%m%dT%H%M%SZ")
        return FakeResp({"articles": [
            {"title": f"Alpha Corp shares surge {stamp}", "seendate": stamp},
            {"title": f"Unrelated company soars {stamp}", "seendate": stamp},
        ]})


NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


@pytest.fixture
def quiet(monkeypatch):
    monkeypatch.setattr("papertrader.history.time.sleep", lambda s: None)


def test_backfill_filters_scores_saves_and_resumes(cfg, tmp_path, quiet):
    cfg = {**cfg, "aliases": {"AAA": ["Alpha Corp"]}}
    session = FakeSession()
    res = backfill(cfg, tmp_path, days=9, window_days=3, session=session, now=NOW)
    assert len(session.calls) == 3 and res == {"counts": {"AAA": 3}, "complete": True}
    saved = HistoryStore(tmp_path).load("AAA")
    assert all(h.scores["lexicon"] > 0 for h in saved)
    again = FakeSession()
    backfill(cfg, tmp_path, days=9, window_days=3, session=again, now=NOW)
    assert again.calls == []  # every window already done


def test_backfill_stops_at_deadline_and_continues_later(cfg, tmp_path, quiet):
    cfg = {**cfg, "aliases": {"AAA": ["Alpha Corp"], "BBB": ["Beta Inc"]}}
    ticks = iter(range(0, 10_000, 60))  # each clock() call advances one minute
    res = backfill(cfg, tmp_path, days=9, window_days=3, session=FakeSession(), now=NOW,
                   max_minutes=2.5, clock=lambda: next(ticks))
    assert res["complete"] is False
    session = FakeSession()
    res = backfill(cfg, tmp_path, days=9, window_days=3, session=session, now=NOW)
    assert res["complete"] and 0 < len(session.calls) < 6


def test_backfill_gives_up_when_gdelt_is_down(cfg, tmp_path, quiet):
    cfg = {**cfg, "aliases": {"AAA": ["Alpha Corp"], "BBB": ["Beta Inc"]}}
    with pytest.raises(GdeltError):
        backfill(cfg, tmp_path, days=30, window_days=3, session=FakeSession(broken=True), now=NOW)


def test_windows_are_fixed_calendar_days():
    late = datetime(2026, 10, 1, 18, 30, tzinfo=timezone.utc)
    ws = windows(late, 7, 3)
    assert ws[-1][0] == datetime(2026, 9, 24, tzinfo=timezone.utc)
    assert ws[0][1] == late  # the newest window ends now and is still open


def test_evaluate_news_runs_without_lookahead(cfg):
    days = weekdays("2026-06-01", 70)
    tickers = list(cfg["universe"])
    hist = {t: make_history(t, days, seed=i) for i, t in enumerate(tickers)}
    hist["SPY"] = make_history("SPY", days, seed=99)
    heads = {}
    for i, t in enumerate(tickers):
        items = []
        for d in days[:-1]:
            # Headline published after the decision time must not affect that day's score.
            when = decision_time(d) + timedelta(hours=1)
            title = f"{cfg['universe'][t]} beats estimates {d}" if i % 2 else f"{cfg['universe'][t]} misses estimates {d}"
            h = Headline(headline_id(t, title), t, title, when.isoformat(), scores={"lexicon": 0.9 if i % 2 else -0.9})
            items.append(h)
        heads[t] = items
    for items in heads.values():
        for h in items[::2]:
            h.scores["finbert"] = 0.5
    res = evaluate_news(cfg, hist, heads)
    assert res["days"] > 50 and len(res["grid"]) == 12
    assert res["scorers"] == ["lexicon", "finbert"]
    assert {"News strategy, lexicon", "News strategy, finbert"} <= set(res["trading"])
    text = render_news(res)
    assert "(live)" in text and "(hybrid)" in text and "| finbert |" in text
    assert len(res["blends"]) == 6


def test_daily_scores_ignore_headlines_after_decision_time():
    from papertrader.history import daily_scores

    cal = ["2026-07-13", "2026-07-14"]
    after = decision_time("2026-07-13") + timedelta(minutes=1)
    h = Headline("x", "AAA", "Alpha beats", after.isoformat(), scores={"lexicon": 1.0})
    sc = daily_scores({"AAA": [h]}, cal, 0, 1, 24, 72, 0.25)
    assert sc[0]["AAA"] == 0.0  # published after the 13th's decision
    assert sc[1]["AAA"] > 0  # but counts for the 14th
