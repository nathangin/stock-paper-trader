"""Load config.json and fill in defaults."""

import json
import os
from pathlib import Path

DEFAULTS = {
    "starting_cash": 100_000,
    "benchmark": "SPY",
    "universe": {},
    "trading": {"slippage_bps": 5, "max_positions": 5, "min_trade_pct": 2.0},
    "aliases": {},
    "news": {
        "lookback_hours": 72, "half_life_hours": 24, "max_new_headlines_per_ticker": 40,
        "opinion_weight": 0.25,
    },
    "predictions": {"min_abs_score": 0.05},
    "strategies": {},
}


def load_config(path="config.json"):
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    cfg = {}
    for key, default in DEFAULTS.items():
        value = raw.get(key, default)
        if isinstance(default, dict) and key not in ("universe", "aliases", "strategies"):
            value = {**default, **value}
        cfg[key] = value
    if not cfg["universe"]:
        raise ValueError(f"{path}: 'universe' must list at least one ticker")
    if isinstance(cfg["universe"], list):
        cfg["universe"] = {t: t for t in cfg["universe"]}
    # Every name a headline might use for each company, display name first.
    cfg["aliases"] = {
        t: list(dict.fromkeys([name, *cfg["aliases"].get(t, [])]))
        for t, name in cfg["universe"].items()
    }
    return cfg


# Accounts that don't predict anything: buy and hold SPY, and equal weight across the
# whole universe (the fair yardstick, since the universe is picked with hindsight).
BENCHMARKS = ("equal_weight", "benchmark")


def enabled_strategies(cfg, claude_available=None):
    """Names of the strategies that trade this run, plus the benchmark accounts."""
    if claude_available is None:
        claude_available = bool(os.environ.get("ANTHROPIC_API_KEY"))
    names = []
    for name, params in cfg["strategies"].items():
        enabled = params.get("enabled", True)
        if enabled == "auto":
            enabled = name != "claude" or claude_available
        if enabled:
            names.append(name)
    return names + list(BENCHMARKS)


def data_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
