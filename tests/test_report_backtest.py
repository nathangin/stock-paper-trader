from papertrader import report
from papertrader.backtest import run_backtest
from papertrader.news import Headline, headline_id
from tests.conftest import make_history, weekdays
from tests.test_engine import DAYS, Market, evening, run


def test_reports_render(cfg, tmp_path):
    market = Market()
    for d in DAYS[-4:-1]:
        run(cfg, tmp_path / "data", market, d, evening(d))
    data = report.write_reports(cfg, tmp_path / "data", root=tmp_path)
    md = (tmp_path / "REPORT.md").read_text()
    page = (tmp_path / "docs" / "index.html").read_text()
    assert data["asof"] == DAYS[-2]
    assert "| Buy & hold SPY |" in md and "Too early to tell" in md
    assert "const DATA = {" in page and "__DATA__" not in page
    names = [r["name"] for r in data["rows"]]
    assert names == ["hybrid", "news", "momentum", "benchmark"]


def test_html_escapes_script_in_headlines(cfg, tmp_path):
    market = Market()
    d = DAYS[-3]
    now = evening(d)
    title = "</script><script>alert(1)</script> beats estimates"
    market.through = d
    from papertrader.engine import run_daily

    run_daily(cfg, tmp_path / "data", market,
              lambda u: [Headline(headline_id("AAA", title), "AAA", title, now.isoformat())],
              now=now, use_claude=False)
    report.write_reports(cfg, tmp_path / "data", root=tmp_path)
    page = (tmp_path / "docs" / "index.html").read_text()
    assert "</script><script>alert" not in page


def test_reports_with_no_data(cfg, tmp_path):
    report.write_reports(cfg, tmp_path / "data", root=tmp_path)
    assert "No runs yet" in (tmp_path / "REPORT.md").read_text()


def test_backtest_momentum_and_benchmark(cfg):
    days = weekdays("2025-01-01", 200)
    h = {
        "AAA": make_history("AAA", days, drift=0.003, seed=1),
        "BBB": make_history("BBB", days, drift=-0.003, seed=2),
        "CCC": make_history("CCC", days, drift=0.0, seed=3),
        "DDD": make_history("DDD", days, drift=0.001, seed=4),
        "EEE": make_history("EEE", days, drift=-0.001, seed=5),
        "SPY": make_history("SPY", days, start_price=500, drift=0.0004, seed=6),
    }
    res = run_backtest(cfg, h)
    assert set(res) == {"momentum", "benchmark"}
    mom, bench = res["momentum"], res["benchmark"]
    assert mom["start"] == days[61] and mom["end"] == days[-1]
    assert mom["trades"] > 0 and mom["stats"]["calls"] > 0
    # Buy and hold: one buy at the first open, then it rides SPY.
    assert bench["trades"] == 1
    spy = h["SPY"]
    first_open = spy.bar_on(days[62]).open
    expected = 100_000 / (first_open * 1.0005) * spy.bars[-1].close
    assert abs(bench["equity"] - expected) < 1.0
