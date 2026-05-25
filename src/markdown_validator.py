from __future__ import annotations

import re
from typing import Dict, Optional

REQUIRED_SECTIONS = [
    "Reference Links",
    "Quality Document JSON",
    "Vendor Identity, Public Status, Financial Metrics and Valuation Narrative",
    "Executive Leadership and Credentials",
    "Business Model and Revenue Model",
    "Detailed Product, Service, Platform, and Technical Capability Catalog",
    "Product-by-Product Technology and Architecture Due Diligence",
    "Product Moat, Differentiation, and Defensibility Analysis",
    "Competitive Landscape, Product Moat, and Pugh Matrix",
    "SEC Filing Scan in Bulleted Format",
]

REQUIRED_FINANCIAL_VISUALS = [
    "Last Four Quarterly Revenue and Profitability",
    "Last Three Fiscal Years Revenue, Profitability, and EPS",
    "Monthly Stock Price Close",
]


def strip_tables_and_code(markdown: str) -> str:
    markdown = re.sub(r"```.*?```", " ", markdown, flags=re.S)
    markdown = re.sub(r"^\|.*\|$", " ", markdown, flags=re.M)
    return markdown


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", strip_tables_and_code(text)))


def count_markdown_tables(markdown: str) -> int:
    return len(re.findall(r"\n\|.+\|\n\|[-:\s|]+\|", markdown))


def count_chart_blocks(markdown: str) -> int:
    return len(re.findall(r"```vendoriq_chart\s+.*?```", markdown, flags=re.S))


def validate_markdown_report(markdown: str, section_markdown: Optional[Dict[str, str]] = None, exhaustive: bool = True) -> dict:
    missing = [section for section in REQUIRED_SECTIONS if section.lower() not in markdown.lower()]
    refs = set(re.findall(r"\[(\d+)\]", markdown))
    defs = set(re.findall(r"^\[(\d+)\]\s+https?://", markdown, re.M))
    unresolved_refs = sorted(refs - defs, key=lambda x: int(x)) if refs else []
    missing_visuals = [visual for visual in REQUIRED_FINANCIAL_VISUALS if visual.lower() not in markdown.lower()]

    checks = {
        "required_sections": {"status": "PASS" if not missing else "FAIL", "missing": missing},
        "reference_links": {
            "status": "PASS" if "Reference Links" in markdown and (not refs or not unresolved_refs) else "FAIL",
            "reference_count": len(defs),
            "unresolved_reference_ids": unresolved_refs,
        },
        "quality_json_final": {"status": "PASS" if markdown.rfind("Quality Document JSON") > markdown.rfind("Reference Links") else "FAIL"},
        "markdown_table_count": {"status": "PASS" if count_markdown_tables(markdown) >= 8 else "FAIL", "count": count_markdown_tables(markdown)},
        "financial_visualizations": {"status": "PASS" if count_chart_blocks(markdown) >= 3 and not missing_visuals else "FAIL", "chart_count": count_chart_blocks(markdown), "missing_visuals": missing_visuals},
    }

    if section_markdown and exhaustive:
        below_minimum = {}
        for title, section in section_markdown.items():
            section_words = word_count(section)
            unavailable = "not found in public sources reviewed" in section.lower()
            if section_words < 500 and not unavailable:
                below_minimum[title] = section_words
        checks["minimum_depth"] = {"status": "PASS" if not below_minimum else "FAIL", "sections_below_min_words": below_minimum}

    failures = [name for name, check in checks.items() if check.get("status") == "FAIL"]
    return {"quality_gate": "PASS" if not failures else "FAIL", "critical_failures": failures, "checks": checks}
