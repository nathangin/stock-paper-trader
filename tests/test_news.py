from datetime import datetime, timedelta, timezone

from papertrader.news import Headline, NewsArchive, headline_id, parse_rss, select_new

YAHOO_XML = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Yahoo</title>
<item><title>Alpha Corp beats estimates, raises guidance</title>
<link>https://example.com/a</link><pubDate>Fri, 09 Oct 2026 20:15:00 +0000</pubDate></item>
<item><title>No date on this one</title><link>https://example.com/b</link></item>
<item><title></title><pubDate>Fri, 09 Oct 2026 20:15:00 +0000</pubDate></item>
</channel></rss>"""

GOOGLE_XML = """<?xml version="1.0"?>
<rss version="2.0"><channel>
<item><title>Alpha Corp shares tumble after recall - Example News</title>
<link>https://news.example/x</link><pubDate>Fri, 09 Oct 2026 18:00:00 GMT</pubDate>
<source url="https://news.example">Example News</source></item>
</channel></rss>"""


def test_parse_yahoo_rss_skips_bad_items():
    items = parse_rss(YAHOO_XML, "AAA", "yahoo")
    assert len(items) == 1
    h = items[0]
    assert h.title == "Alpha Corp beats estimates, raises guidance"
    assert h.published == "2026-10-09T20:15:00+00:00"
    assert h.id == headline_id("AAA", h.title)


def test_parse_google_rss_strips_publisher_suffix():
    (h,) = parse_rss(GOOGLE_XML, "AAA", "google")
    assert h.title == "Alpha Corp shares tumble after recall"
    assert h.source == "Example News"


def test_parse_rss_bad_xml_returns_empty():
    assert parse_rss("<html>blocked</html", "AAA", "yahoo") == []


def _h(ticker, title, hours_ago, now):
    return Headline(headline_id(ticker, title), ticker, title, (now - timedelta(hours=hours_ago)).isoformat())


def test_select_new_dedupes_and_limits():
    now = datetime(2026, 10, 9, 22, tzinfo=timezone.utc)
    items = [
        _h("AAA", "Same story", 1, now),
        _h("AAA", "Same story!", 2, now),  # same normalized title
        _h("AAA", "Old story", 100, now),  # outside lookback
        _h("AAA", "Known story", 1, now),
        _h("AAA", "Story 2", 3, now),
        _h("AAA", "Story 3", 4, now),
        _h("BBB", "Other ticker", 1, now),
    ]
    known = {headline_id("AAA", "Known story")}
    out = select_new(items, known, now, lookback_hours=72, per_ticker_limit=2)
    titles = sorted(h.title for h in out)
    assert titles == ["Other ticker", "Same story", "Story 2"]


def test_archive_roundtrip(tmp_path):
    now = datetime(2026, 10, 9, 22, tzinfo=timezone.utc)
    archive = NewsArchive(tmp_path)
    a = _h("AAA", "Fresh", 1, now)
    a.scores["lexicon"] = 0.5
    b = _h("AAA", "Stale", 80, now)
    archive.append([a, b], "2026-10-09")
    loaded = archive.load(now - timedelta(hours=72))
    assert [h.title for h in loaded] == ["Fresh"]
    assert loaded[0].scores == {"lexicon": 0.5}
    assert archive.known_ids(now - timedelta(hours=72)) == {a.id, b.id}
