"""Command line: python -m papertrader {run,report,status,backtest}."""

import argparse
import logging
import sys

from . import report
from .backtest import PRICE_ONLY, run_backtest
from .config import load_config
from .engine import run_daily
from .market import fetch_all, make_session
from .news import fetch_all_news


def cmd_run(args, cfg):
    session = make_session()
    summary = run_daily(
        cfg,
        args.data_dir,
        fetch_prices=lambda symbols: fetch_all(symbols, session),
        fetch_news=lambda aliases: fetch_all_news(session, aliases),
        use_claude=False if args.no_claude else None,
    )
    report.write_reports(cfg, args.data_dir)
    kinds = summary.get("headline_kinds", {})
    print(
        f"Session {summary['asof']}: {summary['trades']} trades filled, {summary['graded']} predictions "
        f"graded, {summary['new_headlines']} new headlines "
        f"(fetched: {', '.join(f'{v} {k}' for k, v in sorted(kinds.items()))}), "
        + ("new orders placed." if summary["decided"] else "no new orders (market already open).")
    )
    if summary["price_failures"]:
        print("No price data for: " + ", ".join(summary["price_failures"]), file=sys.stderr)
    cmd_status(args, cfg)


def cmd_report(args, cfg):
    report.write_reports(cfg, args.data_dir)
    print("Wrote REPORT.md and docs/index.html")


def cmd_status(args, cfg):
    data = report.build(cfg, args.data_dir)
    if not data["asof"]:
        print("No runs yet.")
        return
    print(f"\nThrough the close on {data['asof']}")
    print(f"{'strategy':<11}{'equity':>12}{'return':>9}{'vs SPY':>9}{'hit rate':>10}{'calls':>7}")
    for r in data["rows"]:
        s = r["stats"]
        hit = f"{s['hit_rate'] * 100:.1f}%" if s.get("calls") else "-"
        vs = f"{r['vs_benchmark'] * 100:+.2f}%" if r["vs_benchmark"] is not None else "-"
        print(f"{r['name']:<11}{r['equity']:>12,.0f}{r['return'] * 100:>+8.2f}%{vs:>9}{hit:>10}{s.get('calls', 0):>7}")


def cmd_backtest(args, cfg):
    histories, failed = fetch_all(list(cfg["universe"]) + [cfg["benchmark"]], make_session(), years=args.years)
    if failed:
        print("No price data for: " + ", ".join(failed), file=sys.stderr)
    results = run_backtest(cfg, histories, PRICE_ONLY)
    first = next(iter(results.values()))
    print(f"\nBacktest {first['start']} to {first['end']} (price-only strategies; news can't be backtested)")
    print(f"{'strategy':<11}{'equity':>12}{'return':>9}{'max DD':>9}{'trades':>8}{'hit rate':>10}{'IC':>8}")
    for name, r in results.items():
        s = r["stats"]
        hit = f"{s['hit_rate'] * 100:.1f}%" if s.get("calls") else "-"
        ic = f"{s['ic']:+.3f}" if "ic" in s else "-"
        print(f"{name:<11}{r['equity']:>12,.0f}{r['return'] * 100:>+8.1f}%{r['max_drawdown'] * 100:>8.1f}%"
              f"{r['trades']:>8}{hit:>10}{ic:>8}")


def cmd_research(args, cfg):
    from pathlib import Path

    from .research import render, run_research

    histories, failed = fetch_all(list(cfg["universe"]) + [cfg["benchmark"]], make_session(), years=args.years)
    if failed:
        print("No price data for: " + ", ".join(failed), file=sys.stderr)
    text = render(run_research(cfg, histories))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


def cmd_backfill_news(args, cfg):
    from .history import backfill

    res = backfill(cfg, args.history_dir, days=args.days, max_minutes=args.max_minutes)
    counts = res["counts"]
    print(f"Saved {sum(counts.values()):,} relevant headlines: "
          + ", ".join(f"{t} {n}" for t, n in counts.items()))
    if not res["complete"]:
        print("Backfill not finished (time limit or failed windows); run it again to continue.")


def cmd_news_research(args, cfg):
    from pathlib import Path

    from .history import HistoryStore, evaluate_news, render_news

    from .history import add_missing_finbert

    store = HistoryStore(args.history_dir)
    added = add_missing_finbert(store, cfg["universe"])
    if added:
        print(f"Scored {added:,} saved headlines with FinBERT")
    headlines = {t: store.load(t) for t in cfg["universe"]}
    histories, failed = fetch_all(list(cfg["universe"]) + [cfg["benchmark"]], make_session(), years=1)
    if failed:
        print("No price data for: " + ", ".join(failed), file=sys.stderr)
    text = render_news(evaluate_news(cfg, histories, headlines))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


def cmd_smart_money(args, cfg):
    from datetime import date, timedelta
    from pathlib import Path

    import requests

    from . import smartmoney as sm
    from .store import write_json

    smc = cfg["smart_money"]
    root = Path(args.data_dir) / "smart_money"
    sec = sm.Sec()
    cache = sm.FilingCache(root / "filings")
    funds_data = {}
    for fund in smc["funds"]:
        try:
            data = sm.fetch_fund(sec, cache, fund, f"{smc['start_year']}-01-01")
        except requests.RequestException as e:
            print(f"{fund['name']}: SEC request failed: {e}", file=sys.stderr)
            continue
        if data:
            funds_data[fund["name"]] = data
    if not funds_data:
        raise SystemExit("No 13F data could be fetched; nothing to do")
    names = {c: h[0] for by in funds_data.values() for f in by.values() for c, h in f["holdings"].items()}
    tickers = sm.TickerMap(root / "cusip_tickers.json").resolve(names, sec)
    print(f"{len(funds_data)} funds, {len(names)} securities, {sum(1 for t in tickers.values() if t)} mapped to tickers")

    # Latest picks: the newest quarter whose filing deadline has passed.
    today = date.today().isoformat()
    periods = sorted({p for by in funds_data.values() for p in by})
    complete = [p for p in periods
                if (date.fromisoformat(p) + timedelta(days=sm.FILING_DEADLINE_DAYS)).isoformat() <= today]
    latest = None
    if len(complete) >= 1:
        ends = sm.quarter_ends(periods[0], complete[-1])
        if len(ends) >= 2:
            picks, used = sm.quarter_picks(funds_data, tickers, ends[-1], ends[-2], today, smc["top_n"])
            latest = {"period": ends[-1], "generated": today, "funds": used,
                      "picks": {v: [list(p) for p in ps] for v, ps in picks.items()}}
            write_json(root / "latest.json", latest)

    # Backtest every quarter since start_year.
    years = date.today().year - smc["start_year"] + 1
    bench = smc["benchmarks"]
    spy, _ = fetch_all([bench[0]], make_session(), years=years)
    calendar = [b.date for b in spy[bench[0]].bars]
    quarters = sm.build_quarters(funds_data, tickers, calendar, smc["top_n"])
    symbols = sorted({p[0] for q in quarters for v in q["picks"].values() for p in v} | set(bench))
    histories, failed = fetch_all(symbols, make_session(), years=years)
    print(f"Backtest: {len(quarters)} quarters, {len(symbols)} symbols, no prices for {len(failed)}")
    bt = sm.backtest(quarters, histories, bench, cfg["trading"]["slippage_bps"]) if quarters else None
    text = sm.render(latest, bt, list(funds_data), smc["funds"])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="papertrader", description=__doc__)
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="daily cycle: fill orders, grade predictions, read news, decide")
    run.add_argument("--no-claude", action="store_true", help="skip Claude scoring even if a key is set")
    sub.add_parser("report", help="rebuild REPORT.md and docs/index.html from data/")
    sub.add_parser("status", help="print the leaderboard")
    bt = sub.add_parser("backtest", help="replay the price-only strategies over past prices")
    bt.add_argument("--years", type=int, default=2)
    rs = sub.add_parser("research", help="walk-forward comparison of price-only strategy variants")
    rs.add_argument("--years", type=int, default=10)
    rs.add_argument("--out", default="research/RESULTS.md")
    bf = sub.add_parser("backfill-news", help="fetch ~3 months of past headlines from GDELT")
    bf.add_argument("--days", type=int, default=90)
    bf.add_argument("--history-dir", default="data/history/gdelt")
    bf.add_argument("--max-minutes", type=float, default=None, help="stop cleanly after this long")
    nr = sub.add_parser("news-research", help="test the news signal on the GDELT backfill")
    nr.add_argument("--history-dir", default="data/history/gdelt")
    nr.add_argument("--out", default="research/NEWS.md")
    smp = sub.add_parser("smart-money", help="what top funds are buying (13F filings), and a backtest")
    smp.add_argument("--out", default="research/SMART_MONEY.md")
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )
    cfg = load_config(args.config)
    commands = {
        "run": cmd_run, "report": cmd_report, "status": cmd_status,
        "backtest": cmd_backtest, "research": cmd_research,
        "backfill-news": cmd_backfill_news, "news-research": cmd_news_research,
        "smart-money": cmd_smart_money,
    }
    commands[args.command](args, cfg)


if __name__ == "__main__":
    main()
