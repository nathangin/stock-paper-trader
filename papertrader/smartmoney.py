"""Follow what well-known funds buy, from their quarterly SEC 13F filings.

Investment managers with over $100M in US stocks must file a 13F every quarter
listing their holdings. The filings are public and free on SEC EDGAR (back to
the 2000s), so "copy the smart money" can be tested honestly: a quarter's picks
only count once the filings were public, which is up to 45 days after the
quarter ends.

Three ways to turn the filings into picks, all tested side by side:
  * new_buys:   stocks the most tracked funds opened a new position in
  * best_ideas: stocks that are in the most funds' top 3 holdings by weight
  * biggest_adds: stocks whose portfolio weight rose the most, summed across funds

Data sources (no keys): SEC EDGAR for filings, OpenFIGI to turn the CUSIP codes
in filings into tickers (with SEC's ticker list as a fallback), Yahoo for prices.
"""

import json
import logging
import os
import re
import statistics
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import requests

from .research import align, simulate, stats

log = logging.getLogger(__name__)

VARIANTS = ("new_buys", "best_ideas", "biggest_adds")
VARIANT_LABELS = {
    "new_buys": "Most new positions",
    "best_ideas": "Most top-3 holdings (best ideas)",
    "biggest_adds": "Biggest weight increases",
}
FILING_DEADLINE_DAYS = 45
# SEC asks automated clients to identify themselves and stay under 10 requests/second.
DEFAULT_USER_AGENT = "stock-paper-trader research bot (github.com/nathangin/stock-paper-trader)"


# ------------------------------------------------------------------ SEC EDGAR


class Sec:
    def __init__(self, session=None, pause=0.15):
        self.session = session or requests.Session()
        self.session.headers["User-Agent"] = os.environ.get("SEC_USER_AGENT") or DEFAULT_USER_AGENT
        self.pause = pause

    def get(self, url):
        for attempt in range(4):
            resp = self.session.get(url, timeout=30)
            time.sleep(self.pause)
            if resp.status_code in (429, 503):
                time.sleep(5 * (attempt + 1))
                continue
            resp.raise_for_status()
            return resp
        resp.raise_for_status()
        return resp

    def submissions(self, cik):
        return self.get(f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json").json()

    def filing_files(self, cik, accession):
        folder = accession.replace("-", "")
        data = self.get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{folder}/index.json").json()
        return [item["name"] for item in data.get("directory", {}).get("item", [])]

    def filing_file(self, cik, accession, name):
        folder = accession.replace("-", "")
        return self.get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{folder}/{name}").text


def list_13f(submissions):
    """Original 13F-HR filings, one per report period (the earliest filed), oldest first."""
    recent = submissions.get("filings", {}).get("recent", {})
    rows = zip(recent.get("form", []), recent.get("accessionNumber", []),
               recent.get("filingDate", []), recent.get("reportDate", []))
    by_period = {}
    for form, acc, filed, period in rows:
        if form != "13F-HR" or not period:
            continue
        if period not in by_period or filed < by_period[period]["filed"]:
            by_period[period] = {"accession": acc, "filed": filed, "period": period}
    return [by_period[p] for p in sorted(by_period)]


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def parse_infotable(xml_text):
    """{cusip: {"name", "value", "shares"}} for plain share holdings (options skipped)."""
    root = ET.fromstring(xml_text)
    out = {}
    for row in root.iter():
        if _local(row.tag) != "infoTable":
            continue
        fields = {}
        for el in row.iter():
            key = _local(el.tag)
            if el.text and el.text.strip() and key not in fields:
                fields[key] = el.text.strip()
        if fields.get("putCall"):
            continue
        cusip = fields.get("cusip", "").upper()
        if not cusip:
            continue
        try:
            value = float(fields.get("value", "0").replace(",", ""))
            shares = float(fields.get("sshPrnamt", "0").replace(",", ""))
        except ValueError:
            continue
        entry = out.setdefault(cusip, {"name": fields.get("nameOfIssuer", ""), "value": 0.0, "shares": 0.0})
        entry["value"] += value
        entry["shares"] += shares
    return out


def find_infotable(files):
    """The information-table XML in a filing folder (its name varies by filer agent)."""
    xmls = [f for f in files if f.lower().endswith(".xml") and f.lower() != "primary_doc.xml"]
    named = [f for f in xmls if "info" in f.lower() or "table" in f.lower()]
    return (named or xmls or [None])[0]


class FilingCache:
    """Parsed holdings per fund and period, saved so each filing is fetched only once."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)

    def path(self, cik, period):
        return self.dir / f"{int(cik)}_{period}.json"

    def get(self, cik, period):
        p = self.path(cik, period)
        return json.loads(p.read_text()) if p.exists() else None

    def put(self, cik, period, filing, holdings):
        data = {"filed": filing["filed"], "accession": filing["accession"],
                "holdings": {c: [h["name"], round(h["value"]), round(h["shares"])] for c, h in holdings.items()}}
        self.path(cik, period).write_text(json.dumps(data, separators=(",", ":"), sort_keys=True))
        return data


def fetch_fund(sec, cache, fund, since):
    """{period: {"filed", "holdings": {cusip: [name, value, shares]}}} for one fund."""
    sub = sec.submissions(fund["cik"])
    name = sub.get("name", "")
    if fund.get("match") and fund["match"].upper() not in name.upper():
        log.error("CIK %s is %r, not %s; skipping it (fix the CIK in config.json)",
                  fund["cik"], name, fund["name"])
        return {}
    out = {}
    for filing in list_13f(sub):
        if filing["period"] < since:
            continue
        cached = cache.get(fund["cik"], filing["period"])
        if cached is None:
            try:
                files = sec.filing_files(fund["cik"], filing["accession"])
                table = find_infotable(files)
                if not table:
                    log.warning("%s %s: no information table found", fund["name"], filing["period"])
                    continue
                holdings = parse_infotable(sec.filing_file(fund["cik"], filing["accession"], table))
            except (requests.RequestException, ET.ParseError) as e:
                log.warning("%s %s: %s", fund["name"], filing["period"], e)
                continue
            cached = cache.put(fund["cik"], filing["period"], filing, holdings)
        out[filing["period"]] = cached
    log.info("%s (%s): %d quarterly filings", fund["name"], name, len(out))
    return out


# ---------------------------------------------------------- CUSIP -> ticker

_SUFFIXES = re.compile(r"\b(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LTD|LIMITED|PLC|HOLDINGS?|"
                       r"GROUP|CLASS [A-C]|CL [A-C]|COM|NEW|THE|SA|NV|AG|LP)\b")


def normalize_name(name):
    name = re.sub(r"[^A-Z0-9 ]", " ", name.upper())
    return " ".join(_SUFFIXES.sub(" ", name).split())


class TickerMap:
    """CUSIP -> Yahoo ticker (or None for funds, ETFs and anything unmappable), cached on disk."""

    def __init__(self, path, session=None, pause=2.6):
        self.path = Path(path)
        self.map = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.session = session or requests.Session()
        self.pause = pause  # OpenFIGI allows 25 requests a minute without a key
        self._sec_names = None

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.map, indent=0, sort_keys=True))

    def _openfigi(self, cusips):
        jobs = [{"idType": "ID_CUSIP", "idValue": c, "exchCode": "US"} for c in cusips]
        for attempt in range(3):
            resp = self.session.post("https://api.openfigi.com/v3/mapping", json=jobs, timeout=30)
            time.sleep(self.pause)
            if resp.status_code == 429:
                time.sleep(30 * (attempt + 1))
                continue
            resp.raise_for_status()
            out = {}
            for cusip, res in zip(cusips, resp.json()):
                ticker = None
                for d in res.get("data", []) or []:
                    if d.get("securityType2") in ("Common Stock", "Depositary Receipt") and d.get("ticker"):
                        ticker = d["ticker"].replace("/", "-").replace(" ", "-")
                        break
                if "data" in res or "warning" in res:
                    out[cusip] = ticker
            return out
        return {}

    def _sec_lookup(self, sec):
        if self._sec_names is None:
            data = sec.get("https://www.sec.gov/files/company_tickers.json").json()
            self._sec_names = {}
            for row in data.values():
                self._sec_names.setdefault(normalize_name(row["title"]), row["ticker"].replace(".", "-"))
        return self._sec_names

    def resolve(self, names_by_cusip, sec=None):
        todo = [c for c in names_by_cusip if c not in self.map]
        for i in range(0, len(todo), 10):
            batch = todo[i:i + 10]
            try:
                self.map.update(self._openfigi(batch))
            except requests.RequestException as e:
                log.warning("OpenFIGI failed (%s); falling back to name matching", e)
                break
        missing = [c for c in names_by_cusip if c not in self.map]
        if missing and sec is not None:
            try:
                lookup = self._sec_lookup(sec)
                for c in missing:
                    self.map[c] = lookup.get(normalize_name(names_by_cusip[c]))
            except requests.RequestException as e:
                log.warning("SEC ticker list unavailable: %s", e)
        self.save()
        return {c: self.map.get(c) for c in names_by_cusip}


# ------------------------------------------------------------------ signals


def weights(holdings, tickers):
    """Ticker -> share of the fund's reported stock portfolio (unmapped holdings still count in the total)."""
    total = sum(h[1] for h in holdings.values()) or 1.0
    out = defaultdict(float)
    for cusip, h in holdings.items():
        t = tickers.get(cusip)
        if t:
            out[t] += h[1] / total
    return dict(out)


def quarter_picks(funds_data, tickers, period, prev_period, known_by, top_n):
    """Picks for one quarter from every fund whose filings for both quarters were public by `known_by`.

    Returns {variant: [(ticker, score, [fund names])...]} best first, plus the funds used.
    """
    new_buys = defaultdict(lambda: [0, 0.0, []])
    best = defaultdict(lambda: [0, 0.0, []])
    adds = defaultdict(lambda: [0.0, []])
    used = []
    for fund, by_period in funds_data.items():
        cur, prev = by_period.get(period), by_period.get(prev_period)
        if not cur or not prev or cur["filed"] > known_by or prev["filed"] > known_by:
            continue
        used.append(fund)
        w_now, w_before = weights(cur["holdings"], tickers), weights(prev["holdings"], tickers)
        for t, w in w_now.items():
            if w_before.get(t, 0.0) == 0.0:
                e = new_buys[t]
                e[0] += 1
                e[1] += w
                e[2].append(fund)
            delta = w - w_before.get(t, 0.0)
            if delta > 0:
                adds[t][0] += delta
                adds[t][1].append(fund)
        for t, w in sorted(w_now.items(), key=lambda kv: -kv[1])[:3]:
            e = best[t]
            e[0] += 1
            e[1] += w
            e[2].append(fund)

    def rank(d, key):
        return [(t, *v) for t, v in sorted(d.items(), key=lambda kv: key(kv[1]))][:top_n]

    return {
        "new_buys": [(t, n + w, f) for t, n, w, f in rank(new_buys, lambda v: (-v[0], -v[1]))],
        "best_ideas": [(t, n + w, f) for t, n, w, f in rank(best, lambda v: (-v[0], -v[1]))],
        "biggest_adds": [(t, w, f) for t, w, f in rank(adds, lambda v: -v[0])],
    }, used


def quarter_ends(start, end):
    """Calendar quarter-end dates (YYYY-MM-DD) from start to end."""
    out = []
    y = int(start[:4])
    while True:
        for m, d in ((3, 31), (6, 30), (9, 30), (12, 31)):
            q = date(y, m, d).isoformat()
            if q > end:
                return out
            if q >= start:
                out.append(q)
        y += 1


def build_quarters(funds_data, tickers, calendar, top_n):
    """Every quarter's picks with the trading day they become usable (after the 13F deadline)."""
    periods = sorted({p for by in funds_data.values() for p in by})
    if len(periods) < 2:
        return []
    ends = quarter_ends(periods[0], periods[-1])
    out = []
    for prev, cur in zip(ends, ends[1:]):
        known = (date.fromisoformat(cur) + timedelta(days=FILING_DEADLINE_DAYS)).isoformat()
        idx = next((i for i, d in enumerate(calendar) if d >= known), None)
        if idx is None:
            continue
        picks, used = quarter_picks(funds_data, tickers, cur, prev, calendar[idx], top_n)
        if used:
            out.append({"period": cur, "decide_on": calendar[idx], "index": idx, "picks": picks, "funds": used})
    return out


# ----------------------------------------------------------------- backtest


def backtest(quarters, histories, benchmarks, slippage_bps):
    """Hold each variant's picks (equal weight) from one quarter's decision day to the next."""
    symbols = sorted({t for q in quarters for v in q["picks"].values() for t, *_ in v} | set(benchmarks))
    symbols = [s for s in symbols if s in histories]
    calendar, opens, closes = align(histories, symbols, benchmarks[0])
    index = {d: i for i, d in enumerate(calendar)}
    rebalance = {}
    for q in quarters:
        i = index.get(q["decide_on"])
        if i is not None:
            rebalance[i] = q
    if not rebalance:
        return {}
    start = min(rebalance)
    end = len(calendar) - 1
    mid = start + (end - start) // 2
    missing = set()

    def rule(variant):
        def decide(t, w):
            q = rebalance.get(t)
            if q is None:
                return None
            names = [p[0] for p in q["picks"][variant]]
            have = [n for n in names if n in closes and closes[n][t]]
            missing.update(set(names) - set(have))
            return {n: 1.0 / len(have) for n in have} if have else {}
        return decide

    def hold(sym):
        return lambda t, w: {sym: 1.0} if not w else None

    rules = {v: rule(v) for v in VARIANTS}
    rules.update({f"{b} buy & hold": hold(b) for b in benchmarks if b in closes})
    results = {}
    for name, decide in rules.items():
        halves = {}
        for half, (a, b) in (("all", (start, end)), ("first", (start, mid)), ("second", (mid, end))):
            eq, turnover = simulate(calendar[: b + 1], opens, closes, decide_from(decide, a), a, slippage_bps)
            halves[half] = {**stats(eq), "turnover": turnover}
        results[name] = halves
    # Average next-quarter return of each variant's picks minus SPY's, quarter by quarter.
    excess = {v: [] for v in VARIANTS}
    order = sorted(rebalance)
    for i, j in zip(order, order[1:] + [end]):
        if j <= i + 1:
            continue
        spy = _period_return(opens, closes, benchmarks[0], i, j)
        for v in VARIANTS:
            rets = [_period_return(opens, closes, p[0], i, j) for p in rebalance[i]["picks"][v]]
            rets = [r for r in rets if r is not None]
            if rets and spy is not None:
                excess[v].append(statistics.fmean(rets) - spy)
    return {
        "period": (calendar[start], calendar[end]), "split": calendar[mid], "results": results,
        "excess": {v: _summ(xs) for v, xs in excess.items()}, "missing_prices": sorted(missing),
    }


def decide_from(decide, start):
    """Start a rule fresh at `start` (the first call must trade even off a rebalance day)."""
    state = {"first": True}

    def wrapped(t, w):
        if state["first"]:
            state["first"] = False
            # Use the most recent rebalance at or before the start.
            for back in range(t, -1, -1):
                r = decide(back, w)
                if r is not None:
                    return r
            return {}
        return decide(t, w)
    return wrapped


def _period_return(opens, closes, sym, i, j):
    if sym not in opens or i + 1 >= len(opens[sym]):
        return None
    a, b = opens[sym][i + 1], closes[sym][j]
    return b / a - 1 if a and b else None


def _summ(xs):
    if not xs:
        return {"quarters": 0}
    mean = statistics.fmean(xs)
    sd = statistics.pstdev(xs) if len(xs) > 1 else 0.0
    return {"quarters": len(xs), "mean": mean, "beat_rate": sum(x > 0 for x in xs) / len(xs),
            "t": mean / (sd / len(xs) ** 0.5) if sd else 0.0}


# ------------------------------------------------------------------- report


def render(latest, bt, funds_ok, funds_cfg):
    lines = ["# Smart money: what top funds are buying", ""]
    if latest:
        lines += [
            f"From 13F filings for the quarter ending **{latest['period']}** "
            f"({len(latest['funds'])} of {len(funds_cfg)} tracked funds have filed: "
            f"{', '.join(latest['funds'])}). 13F filings are up to 45 days old when published and "
            "only show US stock holdings, not shorts or cash.",
            "",
        ]
        for v in VARIANTS:
            lines += [f"## {VARIANT_LABELS[v]}", "", "| Stock | Funds |", "|---|---|"]
            for t, _score, funds in latest["picks"][v]:
                lines.append(f"| {t} | {', '.join(sorted(set(funds)))} |")
            lines.append("")
    if bt:
        a, b = bt["period"]
        lines += [
            "## Did copying them work? (backtest)",
            "",
            f"Each quarter's top picks bought (equal weight) on the first trading day after the 13F "
            f"deadline, held until the next quarter's picks, {a} to {b}. Split at {bt['split']}.",
            "",
            "| Portfolio | CAGR | Sharpe | Max drawdown | CAGR 1st half | CAGR 2nd half |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for name, r in bt["results"].items():
            label = VARIANT_LABELS.get(name, name)
            lines.append(
                f"| {label} | {r['all']['cagr'] * 100:+.1f}% | {r['all']['sharpe']:.2f} | "
                f"{r['all']['max_dd'] * 100:.1f}% | {r['first']['cagr'] * 100:+.1f}% | {r['second']['cagr'] * 100:+.1f}% |"
            )
        lines += ["", "| Variant | Quarters | Avg. quarter vs SPY | Quarters beating SPY | t |",
                  "|---|---:|---:|---:|---:|"]
        for v, s in bt["excess"].items():
            if s["quarters"]:
                lines.append(f"| {VARIANT_LABELS[v]} | {s['quarters']} | {s['mean'] * 100:+.2f}% | "
                             f"{s['beat_rate'] * 100:.0f}% | {s['t']:+.1f} |")
        lines += [
            "",
            "**Caveats.** Stocks that were later delisted have no Yahoo prices and are dropped "
            f"({len(bt['missing_prices'])} picks: {', '.join(bt['missing_prices'][:15]) or 'none'}), "
            "which flatters the results a little. The fund list is picked today, and famous funds are "
            "famous partly because they did well. |t| above about 2 is unlikely to be luck.",
        ]
    return "\n".join(lines) + "\n"
