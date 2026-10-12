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
        fetch_news=lambda universe: fetch_all_news(session, universe),
        use_claude=False if args.no_claude else None,
    )
    report.write_reports(cfg, args.data_dir)
    print(
        f"Session {summary['asof']}: {summary['trades']} trades filled, {summary['graded']} predictions "
        f"graded, {summary['new_headlines']} new headlines, "
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
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )
    cfg = load_config(args.config)
    {"run": cmd_run, "report": cmd_report, "status": cmd_status, "backtest": cmd_backtest}[args.command](args, cfg)


if __name__ == "__main__":
    main()
