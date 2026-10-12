"""Score headlines with Claude (optional; used only when ANTHROPIC_API_KEY is set).

Each new headline is sent once, in batches, and the score is stored in the news
archive with the headline, so re-runs and later days never pay for it again.
The "claude" strategy then aggregates these scores exactly the way the "news"
strategy aggregates the word-list scores, which makes the two directly
comparable: same headlines, same trading rules, different reader.
"""

import json
import logging

log = logging.getLogger(__name__)

SCORER = "claude"
BATCH_SIZE = 50

SYSTEM_PROMPT = """You score stock-market news headlines for a paper-trading experiment.

For each headline, estimate how it is likely to move the named company's stock over the next \
trading day, relative to the overall market, on a scale from -1 (strongly negative) through 0 \
(no meaningful effect) to 1 (strongly positive).

Score 0 for opinion pieces, listicles, recaps of price moves that already happened, and items \
that are not really about the company. Reserve large magnitudes for clearly material news: \
earnings or guidance surprises, regulatory decisions, major contracts or deals, management \
changes, litigation. Keep each reason under 15 words."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "scores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "score": {"type": "number"},
                    "reason": {"type": "string"},
                },
                "required": ["id", "score", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["scores"],
    "additionalProperties": False,
}


def make_client():
    import anthropic

    return anthropic.Anthropic(max_retries=3)


def _request(client, model, effort, batch, universe):
    lines = [
        json.dumps(
            {
                "id": h.id,
                "ticker": h.ticker,
                "company": universe.get(h.ticker, h.ticker),
                "published": h.published,
                "headline": h.title,
            }
        )
        for h in batch
    ]
    return client.beta.messages.create(
        model=model,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=SYSTEM_PROMPT,
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        messages=[
            {
                "role": "user",
                "content": "Score every one of these headlines (one JSON object per line):\n\n"
                + "\n".join(lines),
            }
        ],
    )


def _parse(response, batch):
    if response.stop_reason in ("refusal", "max_tokens"):
        log.warning("Claude batch ended with stop_reason=%s; leaving it unscored", response.stop_reason)
        return {}
    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        items = json.loads(text)["scores"]
    except (ValueError, KeyError, TypeError) as e:
        log.warning("Could not parse Claude output (%s): %.200s", e, text)
        return {}
    wanted = {h.id for h in batch}
    out = {}
    for item in items:
        if item.get("id") in wanted:
            score = max(-1.0, min(1.0, float(item.get("score", 0))))
            out[item["id"]] = (score, str(item.get("reason", ""))[:200])
    return out


def score_headlines(headlines, universe, model, effort="low", client=None):
    """Add a "claude" score and reason to each headline in place.

    Returns the number scored. API failures are logged and the affected
    headlines are left unscored, so a bad day for the API never stops the run.
    """
    import anthropic

    if not headlines:
        return 0
    client = client or make_client()
    scored = 0
    for start in range(0, len(headlines), BATCH_SIZE):
        batch = headlines[start:start + BATCH_SIZE]
        try:
            response = _request(client, model, effort, batch, universe)
        except anthropic.AuthenticationError:
            log.error("ANTHROPIC_API_KEY was rejected; skipping Claude scoring")
            return scored
        except anthropic.RateLimitError as e:
            log.warning("Claude rate limit, skipping a batch: %s", e)
            continue
        except anthropic.APIStatusError as e:
            log.warning("Claude API error %s, skipping a batch: %s", e.status_code, e.message)
            continue
        except anthropic.APIConnectionError as e:
            log.warning("Could not reach the Claude API, skipping a batch: %s", e)
            continue
        results = _parse(response, batch)
        for h in batch:
            if h.id in results:
                h.scores[SCORER], h.reasons[SCORER] = results[h.id]
                scored += 1
    return scored
