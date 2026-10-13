"""Collect stock headlines from free RSS feeds and keep a dated archive.

Sources (no API keys):
  * Yahoo Finance's per-ticker headline feed
  * Google News search for "<company name>" stock

RSS feeds only show the latest few dozen items, so every new headline is saved
to data/news/YYYY-MM-DD.jsonl along with its sentiment scores. Signals are
computed from that archive, and over time it becomes a news history that
strategies can be re-tested against.
"""

import hashlib
import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests

log = logging.getLogger(__name__)

YAHOO_RSS = "https://feeds.finance.yahoo.com/rss/2.0/headline"
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


@dataclass
class Headline:
    id: str
    ticker: str
    title: str
    published: str  # ISO 8601 UTC
    source: str = ""
    url: str = ""
    feed: str = ""
    scores: dict = field(default_factory=dict)  # scorer name -> score in [-1, 1]
    reasons: dict = field(default_factory=dict)  # scorer name -> short explanation
    kind: str = "news"  # "news" or "opinion" (see classify)

    @property
    def published_dt(self):
        return datetime.fromisoformat(self.published)


# Institutional-holdings filler ("XYZ Wealth Management LLC Buys 1,234 Shares of ...").
_HOLDINGS = re.compile(
    r"\b(?:LLC|L\.?P\.?|Advisors|Advisers|Wealth|Asset Management|Capital Management|"
    r"Investment Management|Investments|Partners|Holdings Inc|Trust Co|Financial Group)\b.*"
    r"\b(?:Shares|Stake|Position|Holdings)\b"
    r"|\b(?:Shares|Stake|Position|Holdings) (?:Bought|Sold|Acquired|Increased|Decreased|Raised|"
    r"Lowered|Trimmed|Cut|Boosted|Lifted|Reduced) by\b"
    r"|\b(?:Buys|Sells|Acquires|Purchases|Trims|Boosts|Raises|Lowers|Cuts|Reduces|Increases|Decreases)"
    r" (?:[\d,]+ )?(?:Shares|Stake|Position|Holdings)\b"
    r"|\bInvests? \$[\d.,]+ ?(?:[MBK]|Million|Billion|Thousand)? in\b",
    re.I,
)
# Multi-company market wraps: never about one stock.
_WRAP = re.compile(
    r"\b(?:stock market today|market (?:midday|update|wrap|recap)|company news for|"
    r"stocks to watch|movers? (?:today|premarket|after hours)|biggest (?:stock )?movers|"
    r"morning brief|evening brief|what to watch|stocks? that explain|and more stocks|"
    r"stocks? making (?:the )?biggest moves|price today|live price|stock quote|sector update)\b",
    re.I,
)
# Opinion, comparisons and listicles: weak evidence about tomorrow.
_OPINION = re.compile(
    r"\?\s*$|\b(?:vs\.?|versus)\b|\b(?:should you|is it time|time to buy|buy now|"
    r"what to know|things to know|need to know|here'?s why|here is why|reasons? (?:why|to)|"
    r"better buy|top \d+|\d+ (?:stocks|reasons|things)|could make you|millionaire|"
    r"bull case|bear case|prediction:|my top|i'?m buying|i'?d buy|forever|no-brainer|"
    r"motley fool|zacks rank)\b",
    re.I,
)


def name_patterns(ticker, names):
    """Regexes that mean a title is about this company: any of its names, or its ticker."""
    pats = [re.compile(r"(?<![\w])" + re.escape(n) + r"(?![\w])", re.I) for n in names if n]
    if len(ticker) >= 2:
        # Tickers are matched in capitals only, so "COST" doesn't match "cost".
        pats.append(re.compile(r"(?<![\w])\$?" + re.escape(ticker) + r"(?![\w])"))
    else:
        pats.append(re.compile(r"(?:\$|\(|:)" + re.escape(ticker) + r"\b"))
    return pats


def classify(title, ticker, patterns):
    """"news", "opinion", "offtopic" (doesn't name the company) or "junk" (filings, wraps)."""
    if not any(p.search(title) for p in patterns):
        return "offtopic"
    if _HOLDINGS.search(title) or _WRAP.search(title):
        return "junk"
    if _OPINION.search(title):
        return "opinion"
    return "news"


def filter_relevant(headlines, aliases):
    """Keep headlines that are about their ticker; set each one's kind. Returns (kept, counts)."""
    patterns = {}
    kept, counts = [], {}
    for h in headlines:
        if h.ticker not in patterns:
            patterns[h.ticker] = name_patterns(h.ticker, aliases.get(h.ticker, [h.ticker]))
        kind = classify(h.title, h.ticker, patterns[h.ticker])
        counts[kind] = counts.get(kind, 0) + 1
        if kind in ("news", "opinion"):
            h.kind = kind
            kept.append(h)
    return kept, counts


def normalize_title(title):
    return re.sub(r"[^a-z0-9 ]", "", title.lower()).strip()


def headline_id(ticker, title):
    return hashlib.sha1(f"{ticker}|{normalize_title(title)}".encode()).hexdigest()[:16]


def _parse_date(text):
    if not text:
        return None
    try:
        dt = parsedate_to_datetime(text.strip())
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_rss(xml_text, ticker, feed):
    """Parse an RSS 2.0 document into Headlines. Bad or undated items are skipped."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        log.warning("Bad RSS from %s for %s: %s", feed, ticker, e)
        return []
    out = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        published = _parse_date(item.findtext("pubDate"))
        if not title or published is None:
            continue
        source = (item.findtext("source") or "").strip()
        # Google News appends " - Publisher" to every title.
        if feed == "google" and source and title.endswith(f" - {source}"):
            title = title[: -len(source) - 3].strip()
        out.append(
            Headline(
                id=headline_id(ticker, title),
                ticker=ticker,
                title=title,
                published=published.isoformat(),
                source=source,
                url=(item.findtext("link") or "").strip(),
                feed=feed,
            )
        )
    return out


def fetch_feed(session, url, params, ticker, feed):
    try:
        resp = session.get(url, params=params, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        log.warning("News feed %s failed for %s: %s", feed, ticker, e)
        return []
    return parse_rss(resp.text, ticker, feed)


def fetch_ticker_news(session, ticker, names):
    items = fetch_feed(
        session, YAHOO_RSS, {"s": ticker, "region": "US", "lang": "en-US"}, ticker, "yahoo"
    )
    query = " OR ".join(f'"{n}"' for n in names[:3])
    items += fetch_feed(
        session,
        GOOGLE_NEWS_RSS,
        {"q": f"({query}) stock when:3d", "hl": "en-US", "gl": "US", "ceid": "US:en"},
        ticker,
        "google",
    )
    return items


def fetch_all_news(session, aliases, pause=0.3):
    """Headlines for every ticker ({ticker: [company names]})."""
    out = []
    for ticker, names in aliases.items():
        out.extend(fetch_ticker_news(session, ticker, names))
        time.sleep(pause)
    return out


class NewsArchive:
    """Append-only daily JSONL files of every headline the bot has seen."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _files_since(self, since):
        cutoff = (since - timedelta(days=1)).date().isoformat()
        return sorted(p for p in self.dir.glob("*.jsonl") if p.stem >= cutoff)

    def load(self, since):
        """All archived headlines published at or after `since` (a UTC datetime)."""
        out = []
        for path in self._files_since(since):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        h = Headline(**json.loads(line))
                        if h.published_dt >= since:
                            out.append(h)
        return out

    def known_ids(self, since):
        ids = set()
        for path in self._files_since(since):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        ids.add(json.loads(line)["id"])
        return ids

    def append(self, headlines, day):
        if not headlines:
            return
        path = self.dir / f"{day}.jsonl"
        with open(path, "a", encoding="utf-8") as f:
            for h in headlines:
                f.write(json.dumps(asdict(h), ensure_ascii=False, sort_keys=True) + "\n")


def select_new(headlines, known_ids, now, lookback_hours, per_ticker_limit):
    """Drop duplicates, already-archived and stale headlines; cap the count per ticker."""
    cutoff = now - timedelta(hours=lookback_hours)
    seen = set(known_ids)
    by_ticker = {}
    for h in sorted(headlines, key=lambda h: h.published, reverse=True):
        if h.id in seen or h.published_dt < cutoff or h.published_dt > now + timedelta(hours=1):
            continue
        seen.add(h.id)
        bucket = by_ticker.setdefault(h.ticker, [])
        if len(bucket) < per_ticker_limit:
            bucket.append(h)
    return [h for bucket in by_ticker.values() for h in bucket]
