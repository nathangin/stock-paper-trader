"""Plain-file state in the data/ folder, so every daily run is a readable git diff."""

import csv
import json
from pathlib import Path

from .portfolio import Account

EQUITY_FIELDS = ["date", "strategy", "equity", "cash"]
TRADE_FIELDS = ["date", "strategy", "symbol", "side", "shares", "price", "value"]


class Store:
    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.accounts_path = self.dir / "accounts.json"
        self.equity_path = self.dir / "equity.csv"
        self.trades_path = self.dir / "trades.csv"
        self.predictions_path = self.dir / "predictions.csv"
        self.signals_path = self.dir / "latest_signals.json"
        self.news_dir = self.dir / "news"

    def load_accounts(self):
        if not self.accounts_path.exists():
            return {}
        with open(self.accounts_path, encoding="utf-8") as f:
            return {name: Account.from_dict(d) for name, d in json.load(f).items()}

    def save_accounts(self, accounts):
        data = {name: acct.to_dict() for name, acct in sorted(accounts.items())}
        write_json(self.accounts_path, data)

    def append_rows(self, path, fields, rows):
        if not rows:
            return
        new = not path.exists()
        with open(path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            if new:
                w.writeheader()
            w.writerows(rows)

    def read_rows(self, path):
        if not path.exists():
            return []
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def write_rows(self, path, fields, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    def equity_rows(self):
        return self.read_rows(self.equity_path)

    def trade_rows(self):
        return self.read_rows(self.trades_path)

    def load_signals(self):
        if not self.signals_path.exists():
            return {}
        with open(self.signals_path, encoding="utf-8") as f:
            return json.load(f)


def write_json(path, data):
    tmp = Path(str(path) + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    tmp.replace(path)
