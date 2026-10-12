import json
from types import SimpleNamespace

import anthropic
import httpx2

from papertrader import claude_scorer
from papertrader.news import Headline


def headlines(n=3):
    return [Headline(f"id{i}", "AAA", f"Headline {i}", "2026-10-09T20:00:00+00:00") for i in range(n)]


class FakeMessages:
    def __init__(self, responder):
        self.responder = responder
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.responder(kwargs)


def fake_client(responder):
    msgs = FakeMessages(responder)
    return SimpleNamespace(beta=SimpleNamespace(messages=msgs)), msgs


def response(payload, stop_reason="end_turn"):
    return SimpleNamespace(
        stop_reason=stop_reason,
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=json.dumps(payload))],
    )


def test_scores_are_attached_and_clamped():
    items = headlines(3)
    payload = {"scores": [
        {"id": "id0", "score": 0.6, "reason": "Beat"},
        {"id": "id1", "score": -3, "reason": "Bad"},
        {"id": "nope", "score": 1, "reason": "Not in batch"},
    ]}
    client, msgs = fake_client(lambda kw: response(payload))
    n = claude_scorer.score_headlines(items, {"AAA": "Alpha"}, "claude-opus-5-5", "low", client=client)
    assert n == 2
    assert items[0].scores["claude"] == 0.6 and items[0].reasons["claude"] == "Beat"
    assert items[1].scores["claude"] == -1.0
    assert "claude" not in items[2].scores
    req = msgs.calls[0]
    assert req["model"] == "claude-opus-5-5"
    assert req["output_config"]["effort"] == "low"
    assert req["output_config"]["format"]["type"] == "json_schema"
    assert req["fallbacks"] == "default"
    assert "Alpha" in req["messages"][0]["content"]


def test_batches_requests(monkeypatch):
    monkeypatch.setattr(claude_scorer, "BATCH_SIZE", 2)
    client, msgs = fake_client(lambda kw: response({"scores": []}))
    claude_scorer.score_headlines(headlines(5), {}, "m", client=client)
    assert len(msgs.calls) == 3


def test_refusal_leaves_batch_unscored():
    items = headlines(1)
    client, _ = fake_client(lambda kw: response({"scores": [{"id": "id0", "score": 1, "reason": ""}]}, "refusal"))
    assert claude_scorer.score_headlines(items, {}, "m", client=client) == 0
    assert items[0].scores == {}


def test_connection_error_is_survivable():
    def boom(kw):
        raise anthropic.APIConnectionError(request=httpx2.Request("POST", "https://api.anthropic.com"))

    client, _ = fake_client(boom)
    assert claude_scorer.score_headlines(headlines(2), {}, "m", client=client) == 0


def test_bad_json_is_survivable():
    client, _ = fake_client(
        lambda kw: SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text="oops")])
    )
    assert claude_scorer.score_headlines(headlines(1), {}, "m", client=client) == 0
