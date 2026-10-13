"""Build REPORT.md and the HTML dashboard (docs/index.html) from the data folder."""

import html
import json
from collections import defaultdict
from pathlib import Path

from . import predictions
from .config import BENCHMARKS
from .store import Store

LABELS = {
    "momentum": "Momentum (prices only)",
    "news": "News (word-list sentiment)",
    "hybrid": "Hybrid (news + momentum)",
    "claude": "Claude reads the news",
    "finbert": "FinBERT reads the news (free AI)",
    "equal_weight": "Equal weight, whole list",
    "benchmark": "Buy & hold SPY",
}
ORDER = ["claude", "finbert", "hybrid", "news", "momentum", "equal_weight", "benchmark"]


def _order(names):
    return sorted(names, key=lambda n: (ORDER.index(n) if n in ORDER else len(ORDER), n))


def max_drawdown(values):
    peak, worst = None, 0.0
    for v in values:
        peak = v if peak is None else max(peak, v)
        worst = min(worst, v / peak - 1)
    return worst


MIN_VERDICT_DAYS = 60


def verdict(stats):
    days = stats.get("days", 0)
    if days < MIN_VERDICT_DAYS:
        return f"Too early to tell ({days}/{MIN_VERDICT_DAYS} days)"
    p, rate = stats["p_value"], stats["hit_rate"]
    shown = "p<0.001" if p < 0.001 else f"p={p:.3f}"
    if p < 0.05:
        return ("Beating" if rate > stats["base_rate"] else "Worse than") + f" the baseline ({shown})"
    return f"No better than the baseline yet ({shown})"


def build(cfg, data_dir):
    """Collect everything the reports show into one dict."""
    store = Store(data_dir)
    accounts = store.load_accounts()
    equity = defaultdict(list)
    for r in store.equity_rows():
        equity[r["strategy"]].append((r["date"], float(r["equity"])))
    trades = store.trade_rows()
    pred_rows = store.read_rows(store.predictions_path)
    signals = store.load_signals()
    start = float(cfg["starting_cash"])
    def total_return(name):
        curve = equity.get(name, [])
        return curve[-1][1] / start - 1 if curve else None

    bench_ret, equal_ret = total_return("benchmark"), total_return("equal_weight")

    rows = []
    for name in _order(accounts):
        acct = accounts[name]
        curve = equity.get(name, [])
        value = curve[-1][1] if curve else acct.cash
        ret = value / start - 1
        stats = predictions.summarize(pred_rows, name) if name not in BENCHMARKS else {}
        rows.append({
            "name": name,
            "label": LABELS.get(name, name),
            "equity": value,
            "return": ret,
            "vs_benchmark": None if bench_ret is None or name == "benchmark" else ret - bench_ret,
            "vs_equal": None if equal_ret is None or name in BENCHMARKS else ret - equal_ret,
            "max_drawdown": max_drawdown([v for _, v in curve]) if curve else 0.0,
            "trades": sum(1 for t in trades if t["strategy"] == name),
            "days": len(curve),
            "started_on": acct.started_on,
            "positions": acct.positions,
            "cash": acct.cash,
            "pending": acct.pending,
            "stats": stats,
            "verdict": verdict(stats) if name not in BENCHMARKS else "",
        })
    last_prices = {}
    for t in reversed(trades):
        last_prices.setdefault(t["symbol"], float(t["price"]))
    dates = sorted({d for c in equity.values() for d, _ in c})
    return {
        "asof": dates[-1] if dates else None,
        "start_cash": start,
        "rows": rows,
        "equity": {n: equity[n] for n in _order(equity)},
        "signals": signals,
        "recent_predictions": [r for r in pred_rows if r["next_date"]][-200:],
    }


def _pct(x, signed=True):
    if x is None:
        return "–"
    return f"{x * 100:+.2f}%" if signed else f"{x * 100:.2f}%"


def _money(x):
    return f"${x:,.0f}"


def render_markdown(data, universe):
    lines = ["# Paper trading report", ""]
    if not data["asof"]:
        return "# Paper trading report\n\nNo runs yet. Run `python -m papertrader run`.\n"
    lines += [
        f"_Through the close on **{data['asof']}**. Every account started with "
        f"{_money(data['start_cash'])} of fake money. This file is rewritten by every run._",
        "",
        "| Strategy | Equity | Return | vs SPY | vs equal weight | Max drawdown | Trades | Hit rate | Verdict |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in data["rows"]:
        s = r["stats"]
        hit = f"{s['hit_rate'] * 100:.1f}% ± {s['ci95'] * 100:.1f} ({s['calls']})" if s.get("calls") else "–"
        lines.append(
            f"| {r['label']} | {_money(r['equity'])} | {_pct(r['return'])} | {_pct(r['vs_benchmark'])} | "
            f"{_pct(r['vs_equal'])} | {_pct(r['max_drawdown'])} | {r['trades']} | {hit} | {r['verdict']} |"
        )
    lines += [
        "",
        "**Hit rate** is the share of up/down calls that were right, ± its 95% margin of error, "
        "with the number of graded calls in brackets. The **baseline** is the hit rate of always "
        f"guessing the more common direction, never below 50%. No verdict is given before "
        f"{MIN_VERDICT_DAYS} graded trading days: calls on the same day move together, so a "
        "few weeks of good calls can be one lucky market move.",
        "",
        "**vs equal weight** is the fairer yardstick: the list is today's biggest companies, picked "
        "with hindsight, so simply holding all of them has beaten SPY by a wide margin in the past "
        "(see `research/RESULTS.md`). A strategy has to beat that to show skill.",
        "",
        "## Prediction quality",
        "",
        "| Strategy | Graded calls | Hit rate | Baseline | Avg. edge per call | Rank IC (days) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in data["rows"]:
        s = r["stats"]
        if r["name"] in BENCHMARKS:
            continue
        if not s.get("calls"):
            lines.append(f"| {r['label']} | 0 | – | – | – | – |")
            continue
        ic = f"{s['ic']:+.3f} ({s['ic_days']})" if "ic" in s else "–"
        lines.append(
            f"| {r['label']} | {s['calls']} | {s['hit_rate'] * 100:.1f}% | {s['base_rate'] * 100:.1f}% | "
            f"{s['edge_bps']:+.1f} bp | {ic} |"
        )
    lines += [
        "",
        "*Baseline*: the hit rate of always calling whichever direction those stocks moved more "
        "often (in hindsight, so it is a tough bar). *Edge*: average next-day return in the called "
        "direction, in basis points. *Rank IC*: daily rank correlation between scores and next-day "
        "returns across all stocks, averaged; above about 0.03 sustained is useful.",
        "",
        "## Holdings and next orders",
        "",
    ]
    for r in data["rows"]:
        held = ", ".join(f"{s} ({sh:,.2f} sh)" for s, sh in sorted(r["positions"].items())) or "all cash"
        lines.append(f"- **{r['label']}**: {held}; cash {_money(r['cash'])}")
        if r["pending"]:
            targets = ", ".join(f"{s} {w * 100:.0f}%" for s, w in r["pending"]["targets"].items()) or "all cash"
            lines.append(f"  - next open: {targets}")
    news = (data["signals"] or {}).get("strategies", {}).get("news", {}).get("scores", {})
    if news:
        movers = sorted(((t, s) for t, s in news.items() if abs(s) >= 0.01), key=lambda kv: -abs(kv[1]))[:6]
        lines += ["", "## Strongest news signals", ""] if movers else []
        heads = data["signals"].get("headlines", {})
        for t, s in movers:
            lines.append(f"- **{t}** ({universe.get(t, t)}) news score {s:+.2f}")
            for h in heads.get(t, [])[:3]:
                lex = h["scores"].get("lexicon")
                cl = h["scores"].get("claude")
                tags = f"words {lex:+.2f}" + (f", Claude {cl:+.2f}" if cl is not None else "")
                lines.append(f"  - {h['title'].replace('|', '/')} _({h['source'] or 'unknown'}; {tags})_")
    lines += ["", "See `docs/index.html` for the chart and full tables.", ""]
    return "\n".join(lines)


def render_html(data, universe):
    payload = json.dumps(
        {
            "asof": data["asof"], "start": data["start_cash"], "rows": data["rows"],
            "equity": data["equity"], "labels": LABELS, "universe": universe,
            "signals": data["signals"], "predictions": data["recent_predictions"][-60:],
        },
        default=str,
    ).replace("</", "<\\/")
    return HTML_TEMPLATE.replace("__DATA__", payload).replace("__ASOF__", html.escape(data["asof"] or "no runs yet"))


def write_reports(cfg, data_dir, root="."):
    data = build(cfg, data_dir)
    root = Path(root)
    (root / "REPORT.md").write_text(render_markdown(data, cfg["universe"]), encoding="utf-8")
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "index.html").write_text(render_html(data, cfg["universe"]), encoding="utf-8")
    return data


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paper Trading Dashboard</title>
<style>
:root {
  color-scheme: light;
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e; --muted: #898781;
  --grid: #e1e0d9; --axis: #c3c2b7; --ring: rgba(11,11,11,0.10);
  --s-claude: #2a78d6; --s-hybrid: #eb6834; --s-news: #1baf7a; --s-momentum: #eda100; --s-finbert: #e87ba4; --s-benchmark: #52514e; --s-equal_weight: #898781;
  --up: #006300; --down: #d03b3b;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --page: #0d0d0d; --surface: #1a1a19; --ink: #f0efec; --ink-2: #c3c2b7; --muted: #898781;
    --grid: #2c2c2a; --axis: #383835; --ring: rgba(255,255,255,0.10);
    --s-claude: #3987e5; --s-hybrid: #d95926; --s-news: #199e70; --s-momentum: #c98500; --s-finbert: #d55181; --s-benchmark: #c3c2b7; --s-equal_weight: #898781;
    --up: #0ca30c; --down: #e66767;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --page: #0d0d0d; --surface: #1a1a19; --ink: #f0efec; --ink-2: #c3c2b7; --muted: #898781;
  --grid: #2c2c2a; --axis: #383835; --ring: rgba(255,255,255,0.10);
  --s-claude: #3987e5; --s-hybrid: #d95926; --s-news: #199e70; --s-momentum: #c98500; --s-finbert: #d55181; --s-benchmark: #c3c2b7; --s-equal_weight: #898781;
  --up: #0ca30c; --down: #e66767;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--page); color: var(--ink);
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 1080px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 17px; margin: 32px 0 10px; }
.sub { color: var(--ink-2); margin: 0 0 20px; }
.card { background: var(--surface); border: 1px solid var(--ring); border-radius: 10px; padding: 16px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
.tile .k { color: var(--ink-2); font-size: 13px; display: flex; align-items: center; gap: 6px; }
.tile .v { font-size: 24px; font-weight: 600; margin-top: 2px; }
.tile .d { font-size: 13px; color: var(--ink-2); }
.swatch { width: 10px; height: 10px; border-radius: 3px; display: inline-block; flex: none; }
.chart-wrap { position: relative; }
svg { display: block; width: 100%; height: auto; overflow: visible; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 13px; color: var(--ink-2); margin-bottom: 8px; }
.legend span { display: inline-flex; align-items: center; gap: 6px; }
.tip { position: absolute; pointer-events: none; background: var(--surface); border: 1px solid var(--ring);
  border-radius: 8px; padding: 8px 10px; font-size: 13px; box-shadow: 0 4px 16px rgba(0,0,0,.12);
  display: none; min-width: 190px; }
.tip .row { display: flex; align-items: center; gap: 6px; justify-content: space-between; }
.tip .row b { font-weight: 600; font-variant-numeric: tabular-nums; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--grid); white-space: nowrap; }
th { color: var(--ink-2); font-weight: 500; font-size: 13px; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
td.wrap { white-space: normal; min-width: 240px; }
td.verdict { white-space: normal; min-width: 150px; }
.up { color: var(--up); } .down { color: var(--down); } .muted { color: var(--muted); }
.note { color: var(--ink-2); font-size: 13px; margin-top: 8px; }
a { color: inherit; }
</style>
</head>
<body>
<main>
  <h1>Paper trading dashboard</h1>
  <p class="sub">Fake money, real prices and headlines. Through the close on <b>__ASOF__</b>.</p>
  <div class="tiles" id="tiles"></div>

  <h2>Account value</h2>
  <div class="card">
    <div class="legend" id="legend"></div>
    <div class="chart-wrap" id="chart-wrap">
      <svg id="chart" role="img" aria-label="Account value over time for each strategy"></svg>
      <div class="tip" id="tip"></div>
    </div>
  </div>

  <h2>Leaderboard</h2>
  <div class="card scroll"><table id="board"></table>
    <p class="note">Hit rate counts up/down calls on the next day's close, ± its 95% margin of error.
    The baseline is always guessing the more common direction (never below 50%). No verdict before
    60 graded trading days.</p></div>

  <h2>Next orders (fill at the next open)</h2>
  <div class="card scroll"><table id="orders"></table></div>

  <h2>Latest headlines</h2>
  <div class="card scroll"><table id="news"></table></div>

  <h2>Recently graded predictions</h2>
  <div class="card scroll"><table id="preds"></table></div>
</main>
<script>
const DATA = __DATA__;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const color = name => css('--s-' + name) || css('--ink-2');
const pct = (x, d = 2) => x == null ? '–' : (x >= 0 ? '+' : '') + (x * 100).toFixed(d) + '%';
const money = x => '$' + Math.round(x).toLocaleString();
const el = (tag, attrs = {}, text) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (text != null) e.textContent = text;
  return e;
};
const svgEl = (tag, attrs = {}) => {
  const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  return e;
};
const label = n => DATA.labels[n] || n;
const short = n => ({benchmark: 'SPY', equal_weight: 'equal wt'})[n] || n;

function tiles() {
  const box = document.getElementById('tiles');
  for (const r of DATA.rows) {
    const t = el('div', {class: 'card tile'});
    const k = el('div', {class: 'k'});
    const sw = el('span', {class: 'swatch'}); sw.style.background = color(r.name);
    k.append(sw, document.createTextNode(label(r.name)));
    const v = el('div', {class: 'v'}, money(r.equity));
    const d = el('div', {class: 'd'});
    const ret = el('span', {class: r.return >= 0 ? 'up' : 'down'}, pct(r.return));
    d.append(ret);
    if (r.vs_equal != null) d.append(document.createTextNode(' · ' + pct(r.vs_equal) + ' vs equal wt'));
    else if (r.vs_benchmark != null) d.append(document.createTextNode(' · ' + pct(r.vs_benchmark) + ' vs SPY'));
    t.append(k, v, d);
    box.append(t);
  }
}

function legend() {
  const box = document.getElementById('legend');
  for (const n of Object.keys(DATA.equity)) {
    const s = el('span');
    const sw = el('span', {class: 'swatch'}); sw.style.background = color(n);
    s.append(sw, document.createTextNode(label(n)));
    box.append(s);
  }
}

function chart() {
  const svg = document.getElementById('chart');
  const names = Object.keys(DATA.equity);
  const narrow = document.getElementById('chart-wrap').clientWidth < 600;
  const W = Math.max(300, document.getElementById('chart-wrap').clientWidth);
  const H = narrow ? 240 : 360, L = narrow ? 44 : 64, R = narrow ? 76 : 150, T = 12, B = 30;
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.replaceChildren();
  const dates = [...new Set(names.flatMap(n => DATA.equity[n].map(p => p[0])))].sort();
  if (dates.length < 2) {
    const t = svgEl('text', {x: W / 2, y: H / 2, 'text-anchor': 'middle', fill: css('--muted')});
    t.textContent = 'The chart appears after the second trading day.';
    svg.append(t);
    return;
  }
  const vals = names.flatMap(n => DATA.equity[n].map(p => p[1])).concat([DATA.start]);
  let lo = Math.min(...vals), hi = Math.max(...vals);
  const pad = (hi - lo) * 0.08 || DATA.start * 0.01; lo -= pad; hi += pad;
  const x = d => L + (dates.indexOf(d) / (dates.length - 1)) * (W - L - R);
  const y = v => T + (1 - (v - lo) / (hi - lo)) * (H - T - B);
  const ticks = 5;
  for (let i = 0; i <= ticks; i++) {
    const v = lo + (hi - lo) * i / ticks;
    svg.append(svgEl('line', {x1: L, x2: W - R, y1: y(v), y2: y(v), stroke: css('--grid'), 'stroke-width': 1}));
    const t = svgEl('text', {x: L - 8, y: y(v) + 4, 'text-anchor': 'end', 'font-size': 12, fill: css('--muted')});
    t.textContent = '$' + Math.round(v / 1000) + 'k';
    svg.append(t);
  }
  svg.append(svgEl('line', {x1: L, x2: W - R, y1: y(DATA.start), y2: y(DATA.start), stroke: css('--axis'), 'stroke-width': 1, 'stroke-dasharray': '3 3'}));
  const step = Math.max(1, Math.ceil(dates.length / (narrow ? 3 : 6)));
  dates.forEach((d, i) => {
    if (i % step && i !== dates.length - 1) return;
    const t = svgEl('text', {x: x(d), y: H - 8, 'text-anchor': 'middle', 'font-size': 12, fill: css('--muted')});
    t.textContent = d.slice(5);
    svg.append(t);
  });
  const ends = [];
  for (const n of names) {
    const pts = DATA.equity[n];
    const path = pts.map((p, i) => (i ? 'L' : 'M') + x(p[0]).toFixed(1) + ',' + y(p[1]).toFixed(1)).join('');
    const attrs = {d: path, fill: 'none', stroke: color(n), 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round'};
    if (n === 'benchmark') attrs['stroke-dasharray'] = '6 4';
    if (n === 'equal_weight') attrs['stroke-dasharray'] = '2 4';
    svg.append(svgEl('path', attrs));
    const last = pts[pts.length - 1];
    ends.push({n, y: y(last[1]), x: x(last[0]), v: last[1]});
  }
  ends.sort((a, b) => a.y - b.y);
  for (let i = 1; i < ends.length; i++) ends[i].ly = Math.max(ends[i].y, (ends[i - 1].ly ?? ends[i - 1].y) + 16);
  ends[0].ly = ends[0].y;
  for (const e of ends) {
    svg.append(svgEl('circle', {cx: e.x, cy: e.y, r: 4, fill: color(e.n), stroke: css('--surface'), 'stroke-width': 2}));
    const t = svgEl('text', {x: W - R + 10, y: e.ly + 4, 'font-size': narrow ? 11 : 12, fill: css('--ink-2')});
    t.textContent = short(e.n) + (narrow ? '' : ' ' + pct(e.v / DATA.start - 1, 1));
    svg.append(t);
  }
  const cross = svgEl('line', {y1: T, y2: H - B, stroke: css('--axis'), 'stroke-width': 1, visibility: 'hidden'});
  svg.append(cross);
  const hit = svgEl('rect', {x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent', tabindex: 0});
  svg.append(hit);
  const tip = document.getElementById('tip');
  let focusIdx = dates.length - 1;
  function show(i) {
    const d = dates[i];
    cross.setAttribute('x1', x(d)); cross.setAttribute('x2', x(d)); cross.setAttribute('visibility', 'visible');
    tip.replaceChildren(el('div', {class: 'muted'}, d));
    const rows = names.map(n => ({n, p: DATA.equity[n].find(p => p[0] === d)})).filter(r => r.p).sort((a, b) => b.p[1] - a.p[1]);
    for (const r of rows) {
      const row = el('div', {class: 'row'});
      const left = el('span'); const sw = el('span', {class: 'swatch'}); sw.style.background = color(r.n);
      left.append(sw, document.createTextNode(' ' + short(r.n)));
      row.append(left, el('b', {}, money(r.p[1]) + '  ' + pct(r.p[1] / DATA.start - 1, 1)));
      tip.append(row);
    }
    tip.style.display = 'block';
    const box = svg.getBoundingClientRect(), scale = box.width / W;
    let left = x(d) * scale + 14;
    if (left + tip.offsetWidth > box.width) left = x(d) * scale - tip.offsetWidth - 14;
    tip.style.left = Math.max(0, left) + 'px'; tip.style.top = '16px';
  }
  function hide() { cross.setAttribute('visibility', 'hidden'); tip.style.display = 'none'; }
  hit.addEventListener('pointermove', ev => {
    const box = svg.getBoundingClientRect();
    const px = (ev.clientX - box.left) * W / box.width;
    let best = 0;
    dates.forEach((d, i) => { if (Math.abs(x(d) - px) < Math.abs(x(dates[best]) - px)) best = i; });
    focusIdx = best; show(best);
  });
  hit.addEventListener('pointerleave', hide);
  hit.addEventListener('focus', () => show(focusIdx));
  hit.addEventListener('blur', hide);
  hit.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowLeft') focusIdx = Math.max(0, focusIdx - 1);
    else if (ev.key === 'ArrowRight') focusIdx = Math.min(dates.length - 1, focusIdx + 1);
    else return;
    ev.preventDefault(); show(focusIdx);
  });
}

function table(id, head, rows) {
  const t = document.getElementById(id);
  const tr = el('tr');
  for (const [h, cls] of head) tr.append(el('th', cls ? {class: cls} : {}, h));
  const thead = el('thead'); thead.append(tr); t.append(thead);
  const tb = el('tbody');
  for (const r of rows) {
    const row = el('tr');
    r.forEach((c, i) => {
      const td = el('td', head[i][1] ? {class: head[i][1]} : {});
      if (c instanceof Node) td.append(c); else td.textContent = c;
      row.append(td);
    });
    tb.append(row);
  }
  if (!rows.length) {
    const row = el('tr'); const td = el('td', {colspan: head.length, class: 'muted'}, 'Nothing yet.');
    row.append(td); tb.append(row);
  }
  t.append(tb);
}
const signed = (x, txt) => el('span', {class: x > 0 ? 'up' : x < 0 ? 'down' : 'muted'}, txt);

function boards() {
  table('board', [['Strategy'], ['Equity', 'n'], ['Return', 'n'], ['vs SPY', 'n'], ['vs equal wt', 'n'], ['Max drawdown', 'n'],
    ['Trades', 'n'], ['Hit rate (calls)', 'n'], ['Rank IC', 'n'], ['Verdict']],
    DATA.rows.map(r => {
      const s = r.stats || {};
      return [label(r.name), money(r.equity), signed(r.return, pct(r.return)),
        r.vs_benchmark == null ? '–' : signed(r.vs_benchmark, pct(r.vs_benchmark)),
        r.vs_equal == null ? '–' : signed(r.vs_equal, pct(r.vs_equal)), pct(r.max_drawdown),
        String(r.trades),
        s.calls ? (s.hit_rate * 100).toFixed(1) + '% ± ' + (s.ci95 * 100).toFixed(1) + ' (' + s.calls + ')' : '–',
        s.ic == null ? '–' : s.ic.toFixed(3), r.verdict || ''];
    }));
  table('orders', [['Strategy'], ['Holding now'], ['Target at next open']], DATA.rows.map(r => [
    label(r.name),
    Object.keys(r.positions).sort().join(', ') || 'cash',
    r.pending ? (Object.entries(r.pending.targets).map(([s, w]) => s + ' ' + Math.round(w * 100) + '%').join(', ') || 'cash') : '–',
  ]));
  const heads = (DATA.signals && DATA.signals.headlines) || {};
  const news = [];
  for (const [t, items] of Object.entries(heads)) for (const h of items) news.push([t, h]);
  news.sort((a, b) => b[1].published.localeCompare(a[1].published));
  table('news', [['Ticker'], ['Headline'], ['Words', 'n'], ['Claude', 'n'], ['Published']],
    news.slice(0, 60).map(([t, h]) => {
      const a = h.url ? el('a', {href: h.url, rel: 'noopener', target: '_blank'}, h.title) : document.createTextNode(h.title);
      const cell = el('span'); cell.append(a);
      if (h.reasons && h.reasons.claude) cell.append(el('div', {class: 'note'}, 'Claude: ' + h.reasons.claude));
      const lex = h.scores.lexicon, cl = h.scores.claude;
      return [t, cell, lex == null ? '–' : signed(lex, lex.toFixed(2)), cl == null ? '–' : signed(cl, cl.toFixed(2)),
        h.published.slice(0, 16).replace('T', ' ')];
    }));
  document.querySelectorAll('#news td:nth-child(2)').forEach(td => td.classList.add('wrap'));
  table('preds', [['Date'], ['Strategy'], ['Ticker'], ['Score', 'n'], ['Call'], ['Next-day move', 'n'], ['Right?']],
    DATA.predictions.filter(p => p.call !== '0').slice(-25).reverse().map(p => [
      p.date, p.strategy, p.symbol, Number(p.score).toFixed(2), p.call === '1' ? 'up' : 'down',
      signed(Number(p.ret), pct(Number(p.ret))), p.correct === '1' ? 'yes' : 'no']));
}

tiles(); legend(); chart(); boards();
document.querySelectorAll('#board td:last-child').forEach(td => td.classList.add('verdict'));
let resizeTimer;
window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(chart, 150); });
</script>
</body>
</html>
"""
