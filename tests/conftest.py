import math
import random
from datetime import date, timedelta
from pathlib import Path

import pytest

from papertrader.market import Bar, History

ROOT = Path(__file__).resolve().parent.parent


def weekdays(start, n):
    d, out = date.fromisoformat(start), []
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += timedelta(days=1)
    return out


def make_history(symbol, days, start_price=100.0, drift=0.0, vol=0.01, seed=0, gap=0.0):
    """Synthetic daily bars: open = previous close * (1 + gap), close follows a random walk."""
    rng = random.Random(seed)
    bars, close = [], start_price
    for d in days:
        o = close * (1 + gap)
        close = o * math.exp(drift + vol * rng.gauss(0, 1))
        bars.append(Bar(d, o, max(o, close) * 1.002, min(o, close) * 0.998, close, 1e6))
    return History(symbol, bars, source="test")


def flat_history(symbol, days, opens, closes):
    return History(symbol, [Bar(d, o, max(o, c), min(o, c), c) for d, o, c in zip(days, opens, closes)])


@pytest.fixture
def cfg():
    from papertrader.config import load_config

    c = load_config(ROOT / "config.json")
    c["universe"] = {"AAA": "Alpha Corp", "BBB": "Beta Inc", "CCC": "Gamma Co", "DDD": "Delta Ltd", "EEE": "Epsilon"}
    c["trading"] = {**c["trading"], "max_positions": 2}
    return c
