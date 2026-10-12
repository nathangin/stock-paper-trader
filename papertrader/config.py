"""Load config.json and fill in defaults."""

import json
import os
from pathlib import Path

DEFAULTS = {
    "starting_cash": 100_000,
    "benchmark": "SPY",
    "universe": {},
    "trading": {"slippage_bps": 5, "max_positions": 5, "min_trade_pct": 2.0},
    "news": {"lookback_hours": 72, "half_life_hours": 24, "max_new_headlines_per_ticker": 25},
    "predictions": {"min_abs_score": 0.05},
    "strategies": {},
}


def load_config(path="config.json"):
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    cfg = {}
    for key, default in DEFAULTS.items():
        value = raw.get(key, default)
        if isinstance(default, dict) and key not in ("universe", "strategies"):
            value = {**default, **value}
        cfg[key] = value
    if not cfg["universe"]:
        raise ValueError(f"{path}: 'universe' must list at least one ticker")
    if isinstance(cfg["universe"], list):
        cfg["universe"] = {t: t for t in cfg["universe"]}
    return cfg


def enabled_strategies(cfg, claude_available=None):
    """Names of the strategies that trade this run, plus the benchmark account."""
    if claude_available is None:
        claude_available = bool(os.environ.get("ANTHROPIC_API_KEY"))
    names = []
    for name, params in cfg["strategies"].items():
        enabled = params.get("enabled", True)
        if enabled == "auto":
            enabled = name != "claude" or claude_available
        if enabled:
            names.append(name)
    return names + ["benchmark"]


def data_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
