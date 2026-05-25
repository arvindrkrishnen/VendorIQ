from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
YAHOO_QUOTE_SUMMARY_URL = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
YAHOO_FINANCE_URL = "https://finance.yahoo.com/quote/{ticker}"
YAHOO_FINANCIALS_URL = "https://finance.yahoo.com/quote/{ticker}/financials"
INVESTING_URL = "https://www.investing.com/search/?q={ticker}"
MORNINGSTAR_URL = "https://www.morningstar.com/search?query={ticker}"
FIDELITY_URL = "https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol={ticker}"


@dataclass
class PeriodMetric:
    period: str
    revenue: Optional[float]
    profitability: Optional[float]
    eps: Optional[float] = None


@dataclass
class StockPoint:
    month: str
    close: Optional[float]


@dataclass
class FinancialSnapshot:
    ticker: str
    annual: List[PeriodMetric]
    quarterly: List[PeriodMetric]
    stock_monthly: List[StockPoint]
    source_urls: List[str]
    warnings: List[str]
    generated_at_epoch_seconds: int


def _safe_get_json(url: str, params: Dict[str, Any], timeout: int = 20) -> Dict[str, Any]:
    headers = {
        "User-Agent": "VendorIQ/1.0 (+https://github.com/arvindrkrishnen/VendorIQ)",
        "Accept": "application/json,text/plain,*/*",
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


def _raw_value(item: Dict[str, Any] | None) -> Optional[float]:
    if not item:
        return None
    value = item.get("raw")
    try:
        return float(value) if value is not None else None
    except Exception:
        return None


def _fmt_period_from_item(item: Dict[str, Any]) -> str:
    end_date = item.get("endDate", {}).get("fmt") or item.get("endDate", {}).get("raw")
    if isinstance(end_date, (int, float)):
        return datetime.fromtimestamp(end_date, tz=timezone.utc).strftime("%Y-%m-%d")
    return str(end_date or "Unknown period")


def _income_rows(ticker: str, quarterly: bool = False, limit: int = 4) -> List[PeriodMetric]:
    modules = "incomeStatementHistoryQuarterly" if quarterly else "incomeStatementHistory"
    data = _safe_get_json(YAHOO_QUOTE_SUMMARY_URL.format(ticker=ticker), {"modules": modules})
    result = data.get("quoteSummary", {}).get("result") or []
    if not result:
        return []
    container = result[0].get(modules, {})
    rows = container.get("incomeStatementHistory") or []
    metrics: List[PeriodMetric] = []
    for item in rows[:limit]:
        revenue = _raw_value(item.get("totalRevenue"))
        net_income = _raw_value(item.get("netIncome"))
        eps = _raw_value(item.get("dilutedEPS")) or _raw_value(item.get("basicEPS"))
        metrics.append(PeriodMetric(period=_fmt_period_from_item(item), revenue=revenue, profitability=net_income, eps=eps))
    return metrics


def _monthly_stock_points(ticker: str) -> List[StockPoint]:
    data = _safe_get_json(YAHOO_CHART_URL.format(ticker=ticker), {"range": "3y", "interval": "1mo", "events": "history"})
    result = data.get("chart", {}).get("result") or []
    if not result:
        return []
    payload = result[0]
    timestamps = payload.get("timestamp") or []
    quotes = payload.get("indicators", {}).get("quote") or []
    closes = quotes[0].get("close") if quotes else []
    points: List[StockPoint] = []
    for ts, close in zip(timestamps, closes):
        month = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m")
        try:
            close_value = float(close) if close is not None and not math.isnan(float(close)) else None
        except Exception:
            close_value = None
        points.append(StockPoint(month=month, close=close_value))
    return points


def fetch_financial_snapshot(ticker: str) -> FinancialSnapshot:
    ticker = (ticker or "").strip().upper()
    warnings: List[str] = []
    annual = _income_rows(ticker, quarterly=False, limit=3) if ticker else []
    quarterly = _income_rows(ticker, quarterly=True, limit=4) if ticker else []
    stock_monthly = _monthly_stock_points(ticker) if ticker else []

    if ticker and not annual:
        warnings.append("Yahoo Finance annual income statement data was unavailable through the public quoteSummary endpoint.")
    if ticker and not quarterly:
        warnings.append("Yahoo Finance quarterly income statement data was unavailable through the public quoteSummary endpoint.")
    if ticker and not stock_monthly:
        warnings.append("Yahoo Finance 3-year monthly stock chart data was unavailable through the public chart endpoint.")

    source_urls = []
    if ticker:
        source_urls = [
            YAHOO_FINANCE_URL.format(ticker=ticker),
            YAHOO_FINANCIALS_URL.format(ticker=ticker),
            INVESTING_URL.format(ticker=ticker),
            MORNINGSTAR_URL.format(ticker=ticker),
            FIDELITY_URL.format(ticker=ticker),
        ]
    return FinancialSnapshot(
        ticker=ticker,
        annual=annual,
        quarterly=quarterly,
        stock_monthly=stock_monthly,
        source_urls=source_urls,
        warnings=warnings,
        generated_at_epoch_seconds=int(time.time()),
    )


def _money(value: Optional[float]) -> str:
    if value is None:
        return "Not found in public sources reviewed"
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"
    if abs_value >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    return f"${value:,.0f}"


def _num(value: Optional[float]) -> str:
    return "Not found in public sources reviewed" if value is None else f"{value:,.2f}"


def _chart_block(title: str, x_label: str, y_label: str, series: List[Dict[str, Any]]) -> str:
    return "```vendoriq_chart\n" + json.dumps({"title": title, "x_label": x_label, "y_label": y_label, "series": series}, indent=2) + "\n```"


def financial_snapshot_to_markdown(snapshot: FinancialSnapshot) -> str:
    if not snapshot.ticker:
        return "\n### Public Market and Financial Metrics\n\nTicker was not provided, so market-price and financial visualizations were not generated. Not found in public sources reviewed.\n"

    lines: List[str] = [
        "### Public Market and Financial Metrics",
        "",
        "This section is generated from public market-data endpoints and should be cross-checked against the issuer's latest 10-K, 10-Q, annual report, and investor relations materials before investment or procurement decisions are made.",
        "",
        "#### Last Four Quarterly Revenue and Profitability",
        "",
        "| Quarter / Period | Revenue | Profitability / Net Income | EPS |",
        "|---|---:|---:|---:|",
    ]
    for row in snapshot.quarterly:
        lines.append(f"| {row.period} | {_money(row.revenue)} | {_money(row.profitability)} | {_num(row.eps)} |")
    if not snapshot.quarterly:
        lines.append("| Not found in public sources reviewed | Not found in public sources reviewed | Not found in public sources reviewed | Not found in public sources reviewed |")

    lines += [
        "",
        _chart_block(
            "Last Four Quarterly Revenue and Profitability",
            "Quarter",
            "USD",
            [
                {"name": "Revenue", "points": [{"x": r.period, "y": r.revenue} for r in snapshot.quarterly]},
                {"name": "Profitability / Net Income", "points": [{"x": r.period, "y": r.profitability} for r in snapshot.quarterly]},
            ],
        ),
        "",
        "#### Last Three Fiscal Years Revenue, Profitability, and EPS",
        "",
        "| Fiscal Period | Revenue | Profitability / Net Income | EPS |",
        "|---|---:|---:|---:|",
    ]
    for row in snapshot.annual:
        lines.append(f"| {row.period} | {_money(row.revenue)} | {_money(row.profitability)} | {_num(row.eps)} |")
    if not snapshot.annual:
        lines.append("| Not found in public sources reviewed | Not found in public sources reviewed | Not found in public sources reviewed | Not found in public sources reviewed |")

    lines += [
        "",
        _chart_block(
            "Last Three Fiscal Years Revenue, Profitability, and EPS",
            "Fiscal Period",
            "USD / EPS",
            [
                {"name": "Revenue", "points": [{"x": r.period, "y": r.revenue} for r in snapshot.annual]},
                {"name": "Profitability / Net Income", "points": [{"x": r.period, "y": r.profitability} for r in snapshot.annual]},
                {"name": "EPS", "points": [{"x": r.period, "y": r.eps} for r in snapshot.annual]},
            ],
        ),
        "",
        "#### Stock Price Change — Monthly Close for Last Three Years",
        "",
        "| Month | Monthly Close |",
        "|---|---:|",
    ]
    for point in snapshot.stock_monthly:
        close = "Not found in public sources reviewed" if point.close is None else f"${point.close:,.2f}"
        lines.append(f"| {point.month} | {close} |")
    if not snapshot.stock_monthly:
        lines.append("| Not found in public sources reviewed | Not found in public sources reviewed |")

    lines += [
        "",
        _chart_block(
            "Monthly Stock Price Close — Last Three Years",
            "Month",
            "Share Price",
            [{"name": "Monthly Close", "points": [{"x": p.month, "y": p.close} for p in snapshot.stock_monthly]}],
        ),
        "",
        "#### Public Financial Reference Links to Review",
        "",
    ]
    for url in snapshot.source_urls:
        lines.append(f"- {url}")
    if snapshot.warnings:
        lines += ["", "#### Market Data Collection Warnings", ""]
        lines.extend(f"- {warning}" for warning in snapshot.warnings)
    return "\n".join(lines) + "\n"


def snapshot_to_json(snapshot: FinancialSnapshot) -> Dict[str, Any]:
    return asdict(snapshot)
