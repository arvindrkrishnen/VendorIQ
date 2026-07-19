from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List

import requests

XQUIK_SEARCH_URL = "https://xquik.com/api/v1/x/tweets/search"
XQUIK_SIGNAL_AGENTS = {
    "market_position_agent",
    "customer_segments_agent",
    "customer_supplier_agent",
    "milestones_agent",
    "case_studies_agent",
    "analyst_sentiment_agent",
    "cyber_litigation_agent",
    "future_actions_agent",
    "competitive_pugh_matrix_agent",
}


def _clean(value: Any) -> str:
    text = "" if value is None else str(value)
    return " ".join(text.replace("|", "\\|").split())


def _tweet_url(tweet: Dict[str, Any]) -> str:
    author = tweet.get("author") if isinstance(tweet.get("author"), dict) else {}
    username = _clean(author.get("username"))
    tweet_id = _clean(tweet.get("id"))
    if not username or not tweet_id:
        return ""
    return f"https://x.com/{username}/status/{tweet_id}"


def _engagement(tweet: Dict[str, Any]) -> str:
    labels = [
        ("likes", tweet.get("likeCount")),
        ("reposts", tweet.get("retweetCount")),
        ("replies", tweet.get("replyCount")),
        ("quotes", tweet.get("quoteCount")),
    ]
    return ", ".join(f"{label}: {value}" for label, value in labels if isinstance(value, int))


def _queries(vendor: str, ticker: str, website: str, competitors: str) -> list[str]:
    values = [vendor]
    if ticker:
        values.append(f"${ticker}")
    if website:
        host = website.removeprefix("https://").removeprefix("http://").split("/")[0]
        if host:
            values.append(host)
    if competitors:
        values.append(competitors)
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        query = _clean(value)
        if query and query.lower() not in seen:
            seen.add(query.lower())
            result.append(query)
    return result[:4]


def _render_rows(rows: Iterable[tuple[str, Dict[str, Any]]]) -> str:
    lines = [
        "### Optional Xquik Public X Signal Context",
        "",
        "These public X posts are anecdotal signals for market perception, customer feedback, partner activity, incidents, product announcements, and forward-looking chatter. Do not use them as primary proof for financial metrics, contracts, certifications, litigation, private customer claims, or representative sentiment.",
        "",
        'Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.',
        "",
        "| Query | Author | Date | Engagement | URL | Excerpt |",
        "|---|---|---|---|---|---|",
    ]
    row_count = 0
    seen_urls: set[str] = set()
    for query, tweet in rows:
        author = tweet.get("author") if isinstance(tweet.get("author"), dict) else {}
        author_name = _clean(author.get("username") or author.get("name"))
        excerpt = _clean(tweet.get("text"))[:280]
        url = _tweet_url(tweet)
        if not excerpt or not url or url in seen_urls:
            continue
        seen_urls.add(url)
        lines.append(
            "| "
            + " | ".join(
                [
                    _clean(query),
                    author_name or "unknown",
                    _clean(tweet.get("createdAt")),
                    _engagement(tweet) or "not provided",
                    url,
                    excerpt,
                ]
            )
            + " |"
        )
        row_count += 1
        if row_count >= 12:
            break
    if row_count == 0:
        return ""
    return "\n".join(lines) + "\n"


def collect_xquik_signal_markdown(
    vendor: str,
    ticker: str = "",
    website: str = "",
    competitors: str = "",
    days: int = 30,
    limit_per_query: int = 5,
) -> str:
    api_key = os.getenv("XQUIK_API_KEY", "").strip()
    if not api_key:
        return ""

    since_time = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat().replace("+00:00", "Z")
    rows: List[tuple[str, Dict[str, Any]]] = []
    for query in _queries(vendor, ticker, website, competitors):
        try:
            response = requests.get(
                XQUIK_SEARCH_URL,
                headers={"x-api-key": api_key},
                params={
                    "q": query,
                    "queryType": "Latest",
                    "sinceTime": since_time,
                    "limit": limit_per_query,
                },
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException:
            continue
        tweets = payload.get("tweets", []) if isinstance(payload, dict) else []
        if not isinstance(tweets, list):
            continue
        for tweet in tweets:
            if isinstance(tweet, dict):
                rows.append((query, tweet))
    return _render_rows(rows)
