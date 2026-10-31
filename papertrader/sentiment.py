"""Rule-based headline sentiment tuned for stock news.

General-purpose sentiment word lists misread finance headlines ("shares fall
short" vs "short interest", "beats" vs "beaten down"), so this uses a small
hand-made lexicon of market phrases and words. Phrases are matched first and
their words are not counted again. A negator ("not", "no", "fails to") in the
three words before a term flips its sign.

Contrast words decide which part of a headline carries the news. In "Tesla
slips despite earnings beat" the stock slipped, so only the main clause is
scored ("despite", "even as", "in spite of"). In "Revenue surges, but costs
weigh" the part after "but" or "however" counts three times as much as the part
before it (1.5 vs 0.5), as in VADER.

The score is tanh(sum of weights / 2), so it lies in [-1, 1]; 0 means no
sentiment terms were found.
"""

import math
import re

PHRASES = {
    # earnings and guidance
    "beats estimates": 2.0, "beat estimates": 2.0, "tops estimates": 2.0,
    "beats expectations": 2.0, "tops expectations": 2.0, "better than expected": 1.5,
    "raises guidance": 2.5, "raises outlook": 2.5, "raises forecast": 2.0,
    "boosts guidance": 2.5, "lifts guidance": 2.0, "record revenue": 2.0,
    "record profit": 2.0, "record quarter": 1.5, "strong demand": 1.5,
    "misses estimates": -2.0, "missed estimates": -2.0, "misses expectations": -2.0,
    "worse than expected": -1.5, "cuts guidance": -2.5, "lowers guidance": -2.5,
    "cuts outlook": -2.5, "lowers outlook": -2.0, "cuts forecast": -2.0,
    "weak guidance": -2.0, "weak demand": -1.5, "profit warning": -2.5,
    # analysts
    "price target raised": 1.5, "raises price target": 1.5, "lifts price target": 1.5,
    "price target cut": -1.5, "cuts price target": -1.5, "lowers price target": -1.5,
    "upgraded to buy": 2.0, "downgraded to sell": -2.0, "upgraded to outperform": 2.0,
    "downgraded to underperform": -2.0, "upgraded to overweight": 2.0, "downgraded to underweight": -2.0,
    "raises target": 1.2, "lifts target": 1.2, "boosts target": 1.2, "ups target": 1.2,
    "cuts target": -1.2, "lowers target": -1.2, "trims target": -1.0, "slashes target": -1.5,
    "target raised": 1.2, "target lowered": -1.2, "target cut": -1.2,
    "buy rating": 0.4, "sell rating": -0.8, "initiates coverage": 0.2,
    "beat-and-raise": 2.5, "beat and raise": 2.5, "blowout quarter": 2.0, "blowout report": 2.0,
    "new high": 0.8, "new low": -0.8, "win streak": 0.6, "winning streak": 0.6,
    "losing streak": -0.6, "breaks out": 0.8, "buy point": 0.5,
    # capital return and deals
    "share buyback": 1.0, "stock buyback": 1.0, "dividend increase": 1.0,
    "raises dividend": 1.0, "cuts dividend": -2.0, "suspends dividend": -2.0,
    "all time high": 1.0, "all-time high": 1.0, "52 week high": 1.0, "52-week high": 1.0,
    "52 week low": -1.0, "52-week low": -1.0, "record low": -1.5,
    # "sits 8 percent below its 52-week high" is a price report, not a new high
    "below its 52-week high": 0.0, "below its 52 week high": 0.0, "below the 52-week high": 0.0,
    "off its 52-week high": 0.0, "below its all-time high": 0.0, "below its record high": 0.0,
    "from its peak": -0.5, "off its peak": -0.5, "worst day": -1.5, "worst week": -1.5,
    "best day": 1.5, "best week": 1.5, "edges higher": 0.4, "edge higher": 0.4,
    "edges lower": -0.4, "edge lower": -0.4, "buying opportunity": 1.0, "remains a buy": 0.8,
    # direction words whose meaning flips with the subject ("costs surged" is bad news)
    "costs surged": -1.0, "costs surge": -1.0, "costs soar": -1.0, "costs rise": -0.8,
    "costs jump": -0.8, "expenses rise": -0.8, "expenses surge": -1.0, "spending surges": -0.5,
    "spending soars": -0.5, "spending jumps": -0.5, "spending rises": -0.4, "warnings rise": -1.0,
    "losses widen": -1.5, "loss widens": -1.5, "losses narrow": 1.0, "loss narrows": 1.0,
    "costs fall": 0.8, "costs drop": 0.8, "debt rises": -0.6, "short interest rises": -0.6,
    "rising costs": -0.8, "higher costs": -0.8, "cash burn surges": -1.0, "cash burn rises": -0.8,
    "cash burn jumps": -0.8, "growth slows": -1.0, "growth slowed": -1.0, "growth slowing": -1.0,
    "demand slows": -1.0, "demand slowed": -1.0, "demand slowing": -1.0,
    # "record" is good news except next to a fall ("record one-day drop") or as a speed ("record pace")
    "record drop": -1.5, "record one-day drop": -1.8, "record fall": -1.5, "record decline": -1.5,
    "record selloff": -1.5, "record sell-off": -1.5, "record pace": 0.0,
    "pull back": -0.6, "pulls back": -0.6, "pulled back": -0.6, "rally pauses": -0.6, "rally stalls": -0.8,
    "wipes out": -1.0, "wiped out": -1.0, "eats into": -0.8, "eat into": -0.8, "eating into": -0.8,
    # legal and regulatory
    "fda approval": 2.0, "wins approval": 1.5, "class action": -1.5,
    "antitrust lawsuit": -2.0, "sec investigation": -2.0, "data breach": -1.5,
    "short seller": -1.0, "chapter 11": -3.0,
}

WORDS = {
    # positive
    "beat": 1.0, "beats": 1.0, "tops": 1.0, "surge": 1.5, "surges": 1.5, "surged": 1.5,
    "soar": 1.5, "soars": 1.5, "soared": 1.5, "jump": 1.0, "jumps": 1.0, "jumped": 1.0,
    "rally": 1.0, "rallies": 1.0, "rallied": 1.0, "gain": 0.7, "gains": 0.7, "gained": 0.7,
    "rise": 0.7, "rises": 0.7, "rose": 0.7, "climb": 0.7, "climbs": 0.7, "climbed": 0.7,
    "rebound": 0.8, "rebounds": 0.8, "upgrade": 1.5, "upgrades": 1.5, "upgraded": 1.5,
    "outperform": 1.0, "bullish": 1.2, "record": 0.8, "strong": 0.7, "growth": 0.5,
    "profit": 0.4, "profitable": 0.8, "approval": 1.0, "approved": 1.0, "wins": 0.8,
    "win": 0.6, "partnership": 0.6, "expands": 0.5, "expansion": 0.5, "launch": 0.4,
    "launches": 0.4, "breakthrough": 1.2, "buyback": 0.8, "boost": 0.6, "boosts": 0.6,
    "optimistic": 0.8, "accelerates": 0.6, "momentum": 0.4, "outpaces": 0.8,
    "surging": 1.5, "soaring": 1.5, "jumping": 1.0, "rallying": 1.0, "rising": 0.7,
    "gaining": 0.7, "climbing": 0.7, "rebounding": 0.8, "skyrockets": 1.8, "rockets": 1.5,
    "blowout": 1.5, "breakout": 0.8, "beating": 1.0, "overweight": 0.8, "raised": 0.5,
    "awarded": 0.6, "secures": 0.6, "inks": 0.5, "strongest": 0.8,
    # negative
    "miss": -1.0, "misses": -1.0, "missed": -1.0, "plunge": -1.8, "plunges": -1.8,
    "plunged": -1.8, "tumble": -1.5, "tumbles": -1.5, "tumbled": -1.5, "sink": -1.2,
    "sinks": -1.2, "sank": -1.2, "slump": -1.2, "slumps": -1.2, "crash": -2.0,
    "crashes": -2.0, "fall": -0.7, "falls": -0.7, "fell": -0.7, "drop": -0.7,
    "drops": -0.7, "dropped": -0.7, "decline": -0.7, "declines": -0.7, "slide": -0.8,
    "slides": -0.8, "downgrade": -1.5, "downgrades": -1.5, "downgraded": -1.5,
    "underperform": -1.0, "bearish": -1.2, "weak": -0.8, "weaker": -0.8, "loss": -0.6,
    "losses": -0.7, "lawsuit": -1.0, "sued": -1.0, "probe": -1.0, "investigation": -1.0,
    "recall": -1.2, "recalls": -1.2, "layoffs": -0.8, "cuts": -0.5, "warning": -1.0,
    "warns": -1.0, "fraud": -2.0, "antitrust": -0.8, "fined": -1.0,
    "penalty": -0.8, "penalties": -0.8, "delay": -0.8, "delays": -0.8, "delayed": -0.8, "halt": -1.0,
    "halts": -1.0, "bankruptcy": -3.0, "selloff": -1.2, "sell-off": -1.2,
    "concern": -0.5, "concerns": -0.5, "fears": -0.8, "risk": -0.3, "slowdown": -0.8,
    "outage": -1.0, "tariff": -0.5, "tariffs": -0.5, "resigns": -0.8,
    "pessimistic": -0.8, "glut": -0.8, "shortfall": -1.0,
    "falling": -0.7, "dropping": -0.7, "sliding": -0.8, "sinking": -1.2, "slumping": -1.2,
    "plunging": -1.8, "tumbling": -1.5, "declining": -0.7, "crashing": -2.0, "cratered": -1.5,
    "craters": -1.5, "tanks": -1.5, "tanked": -1.5, "tanking": -1.5, "underweight": -0.8,
    "lowered": -0.5, "slashes": -1.0, "slashed": -1.0, "layoff": -0.8, "cut": -0.4,
    "subpoena": -1.2, "downturn": -0.8, "headwinds": -0.6, "headwind": -0.6, "plummets": -1.8,
    "slip": -0.6, "slips": -0.6, "slipped": -0.6, "slipping": -0.6, "dip": -0.5, "dips": -0.5,
    "dipped": -0.5, "retreat": -0.6, "retreats": -0.6, "retreated": -0.6, "erode": -0.8,
    "erodes": -0.8, "eroded": -0.8, "fret": -0.6, "frets": -0.6, "worst": -1.0, "warnings": -1.0,
    "downside": -0.5, "disappoints": -1.0, "disappointing": -1.0, "disappointed": -0.8,
    "disappointment": -1.0, "lags": -0.6, "lagged": -0.6, "lagging": -0.6, "dumping": -0.8, "dumps": -0.8,
    "dumped": -0.8, "dump": -0.8, "erases": -1.0, "erased": -1.0, "meltdown": -1.5, "pullback": -0.5,
    # positive, kept apart from the list above so the additions are easy to see
    "upside": 0.5,
}

NEGATORS = {"not", "no", "never", "without", "fails", "failed", "isn't", "wasn't", "doesn't", "didn't"}

_TOKEN = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)*")
_PHRASES_LONGEST_FIRST = sorted(PHRASES, key=len, reverse=True)
_CONCESSIVE = re.compile(r"(?<![a-z0-9])(?:despite|in spite of|even as|even though|notwithstanding)(?![a-z0-9])")
_ADVERSATIVE = re.compile(r"(?<![a-z0-9])(?:but|however)(?![a-z0-9])")


def _negated(tokens, index):
    return any(t in NEGATORS for t in tokens[max(0, index - 3):index])


def score_text(text):
    """Sentiment of one headline in [-1, 1]."""
    lowered = " " + text.lower().replace("’", "'") + " "
    m = _CONCESSIVE.search(lowered)
    if m:
        main = lowered[: m.start()]
        if not _TOKEN.search(main):
            # "Despite the beat, Tesla slips": the main clause follows the comma
            _, comma, rest = lowered[m.end():].partition(",")
            main = rest if comma else ""
        return math.tanh(_weights(main) / 2)
    m = _ADVERSATIVE.search(lowered)
    if m:
        return math.tanh((0.5 * _weights(lowered[: m.start()]) + 1.5 * _weights(lowered[m.end():])) / 2)
    return math.tanh(_weights(lowered) / 2)


def _weights(lowered):
    """Sum of term weights in an already lower-cased piece of text."""
    lowered = " " + lowered + " "
    total = 0.0
    for phrase in _PHRASES_LONGEST_FIRST:
        pattern = re.compile(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])")
        for m in pattern.finditer(lowered):
            before = _TOKEN.findall(lowered[: m.start()])
            weight = PHRASES[phrase]
            total += -weight if _negated(before, len(before)) else weight
        lowered = pattern.sub(" ", lowered)
    tokens = _TOKEN.findall(lowered)
    for i, tok in enumerate(tokens):
        weight = WORDS.get(tok)
        if weight is not None:
            total += -weight if _negated(tokens, i) else weight
    return total
