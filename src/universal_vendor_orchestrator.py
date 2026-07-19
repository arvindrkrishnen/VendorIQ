#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

from markdown_to_html_converter import convert_markdown_report_to_self_contained_html
from markdown_validator import validate_markdown_report
from market_data import fetch_financial_snapshot, financial_snapshot_to_markdown, snapshot_to_json
from provider_clients import ProviderConfig, ProviderError, generate_section_markdown
from reference_normalizer import ReferenceManager
from xquik_signals import XQUIK_SIGNAL_AGENTS, collect_xquik_signal_markdown

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MD = ROOT / "artifacts" / "exhaustive_final_report.md"
DEFAULT_HTML = ROOT / "artifacts" / "exhaustive_final_report.html"


@dataclass
class RunConfig:
    vendor: str
    ticker: str
    website: str
    provider: str
    model: str
    competitors: str
    sec_cik: str
    markdown_output: Path
    html_output: Path
    depth: str = "exhaustive"
    skip_html: bool = False
    allow_html_on_validation_fail: bool = False


@dataclass
class SectionResult:
    agent: str
    title: str
    markdown: str
    evidence_urls: List[str]


SECTION_TASKS = [
    ("identity_financial_agent", "Vendor Identity, Public Status, Financial Metrics and Valuation Narrative"),
    ("executive_leadership_agent", "Executive Leadership and Credentials"),
    ("market_position_agent", "Company Overview and Market Position"),
    ("business_model_agent", "Business Model and Revenue Model"),
    ("product_services_agent", "Detailed Product, Service, Platform, and Technical Capability Catalog"),
    ("architecture_agent", "Product-by-Product Technology and Architecture Due Diligence"),
    ("information_architecture_agent", "Information Architecture Assessment"),
    ("application_architecture_agent", "Application Architecture Assessment"),
    ("security_architecture_agent", "Security Architecture Assessment"),
    ("standards_interoperability_agent", "Technology Standards and Interoperability Assessment"),
    ("resiliency_dr_agent", "Resiliency, Disaster Recovery, and Stability Assessment"),
    ("ai_ml_genai_agent", "AI, Machine Learning, Automation, and GenAI Capabilities by Product"),
    ("product_moat_agent", "Product Moat, Differentiation, and Defensibility Analysis"),
    ("customer_segments_agent", "Key Customers and Customer Segments"),
    ("customer_supplier_agent", "Key Suppliers, Cloud Providers, Technology Partners, Channel Partners, and Ecosystem Dependencies"),
    ("government_contracts_agent", "Government Contracts, Public-Sector Awards, FedRAMP Status, Marketplaces, and Procurement Vehicles"),
    ("milestones_agent", "Major Milestones, Acquisitions, Partnerships, and Recognitions"),
    ("case_studies_agent", "Case Studies and Measurable Client Benefits"),
    ("esg_privacy_agent", "ESG, Sustainability, Privacy, and Responsible-Business Posture"),
    ("analyst_sentiment_agent", "Analyst Reviews, Market Sentiment, and External Perception"),
    ("cyber_litigation_agent", "Cybersecurity Incidents, Vulnerabilities, Regulatory Issues, and Litigation Signals"),
    ("sec_filings_agent", "SEC Filing Scan in Bulleted Format"),
    ("future_actions_agent", "Future Actions and Forward-Looking Indicators"),
    ("competitive_pugh_matrix_agent", "Competitive Landscape, Product Moat, and Pugh Matrix"),
    ("quality_synthesis_agent", "Strengths, Gaps, Risks, and Differentiation"),
]


def _provider_config(config: RunConfig) -> ProviderConfig:
    return ProviderConfig(
        provider=config.provider,
        model=config.model,
        vendor=config.vendor,
        ticker=config.ticker,
        website=config.website,
        competitors=config.competitors,
        sec_cik=config.sec_cik,
        depth=config.depth,
    )


def run_sections(config: RunConfig) -> tuple[list[SectionResult], dict]:
    financial_snapshot = fetch_financial_snapshot(config.ticker) if config.ticker else None
    financial_markdown = financial_snapshot_to_markdown(financial_snapshot) if financial_snapshot else ""
    financial_json = snapshot_to_json(financial_snapshot) if financial_snapshot else {}
    xquik_signal_markdown = collect_xquik_signal_markdown(
        config.vendor,
        ticker=config.ticker,
        website=config.website,
        competitors=config.competitors,
    )

    if config.provider == "offline" and config.depth == "exhaustive":
        raise RuntimeError("Offline provider cannot generate an exhaustive report. Use openai, anthropic, gemini, or perplexity.")

    provider_config = _provider_config(config)
    results: list[SectionResult] = []
    for agent, title in SECTION_TASKS:
        context_parts = []
        if agent == "identity_financial_agent" and financial_markdown:
            context_parts.append(financial_markdown)
        if agent in XQUIK_SIGNAL_AGENTS and xquik_signal_markdown:
            context_parts.append(xquik_signal_markdown)
        context_markdown = "\n\n".join(context_parts)
        try:
            md = generate_section_markdown(provider_config, agent, title, context_markdown)
        except ProviderError as exc:
            raise RuntimeError(str(exc)) from exc
        except Exception as exc:
            md = f"## {title}\n\nProvider execution failed for `{agent}`: {exc}\n\nNot found in public sources reviewed.\n"
        for context_part in context_parts:
            if context_part and context_part not in md:
                md = md.rstrip() + "\n\n" + context_part
        results.append(SectionResult(agent=agent, title=title, markdown=md, evidence_urls=[]))
    return results, financial_json


def assemble(config: RunConfig, results: list[SectionResult], financial_json: dict, quality: str | None = None) -> tuple[str, int, dict]:
    ref = ReferenceManager()
    sections: dict[str, str] = {}
    parts = [
        f"# Exhaustive Vendor Analysis Final Report: {config.vendor} ({config.ticker or 'Ticker not provided'})\n\n"
        "## Title Page and Evidence Methodology\n\n"
        "VendorIQ generated this report using a Markdown-first workflow. Each section is drafted by a specialized agent, raw URLs are normalized into numbered references, and the validated Markdown is converted into one self-contained interactive HTML report. "
        "Public-company sections prioritize SEC filings, annual reports, quarterly reports, investor relations materials, Yahoo Finance, Investing.com, Bloomberg, FactSet, Morningstar, Fidelity, official product documentation, trust/security pages, reputable news, and public procurement sources. "
        "Unavailable evidence is labeled as `Not found in public sources reviewed` rather than inferred.\n"
    ]
    for result in results:
        normalized = ref.replace_urls_with_refs(result.markdown, result.title)
        if not normalized.lstrip().startswith("#"):
            normalized = f"## {result.title}\n\n" + normalized
        parts.append(normalized)
        sections[result.title] = normalized
    parts.append(ref.render_reference_links())
    if quality:
        parts.append(quality)
    else:
        parts.append("## Quality Document JSON\n\n```json\n{}\n```\n")
    return "\n---\n".join(parts), len(ref.records), sections


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(description="VendorIQ Universal Vendor Analysis Orchestrator")
    parser.add_argument("--vendor", required=True)
    parser.add_argument("--ticker", default="")
    parser.add_argument("--website", default="")
    parser.add_argument("--provider", default=os.getenv("VENDOR_ANALYSIS_PROVIDER", "offline"), choices=["offline", "openai", "anthropic", "gemini", "perplexity"])
    parser.add_argument("--model", default=os.getenv("VENDOR_ANALYSIS_MODEL", "offline-scaffold"))
    parser.add_argument("--competitors", default="")
    parser.add_argument("--sec-cik", default="")
    parser.add_argument("--markdown-output", default=str(DEFAULT_MD))
    parser.add_argument("--html-output", default=str(DEFAULT_HTML))
    parser.add_argument("--depth", default="exhaustive", choices=["standard", "exhaustive"])
    parser.add_argument("--skip-html", action="store_true")
    parser.add_argument("--allow-html-on-validation-fail", action="store_true")
    args = parser.parse_args()
    return RunConfig(
        vendor=args.vendor,
        ticker=args.ticker,
        website=args.website,
        provider=args.provider,
        model=args.model,
        competitors=args.competitors,
        sec_cik=args.sec_cik,
        markdown_output=Path(args.markdown_output).resolve(),
        html_output=Path(args.html_output).resolve(),
        depth=args.depth,
        skip_html=args.skip_html,
        allow_html_on_validation_fail=args.allow_html_on_validation_fail,
    )


def main() -> int:
    config = parse_args()
    config.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    config.html_output.parent.mkdir(parents=True, exist_ok=True)

    results, financial_json = run_sections(config)
    draft, reference_count, sections = assemble(config, results, financial_json)
    validation = validate_markdown_report(draft, sections, config.depth == "exhaustive")
    quality = (
        "## Quality Document JSON\n\n```json\n"
        + json.dumps(
            {
                "vendor": config.vendor,
                "ticker": config.ticker,
                "provider": config.provider,
                "model": config.model,
                "markdown_first_execution": True,
                "html_conversion_after_quality_gate_only": True,
                "reference_count": reference_count,
                "financial_market_data_snapshot": financial_json,
                "validation": validation,
                "generated_at_epoch_seconds": int(time.time()),
            },
            indent=2,
        )
        + "\n```\n"
    )
    final_markdown, _, sections = assemble(config, results, financial_json, quality)
    final_validation = validate_markdown_report(final_markdown, sections, config.depth == "exhaustive")

    config.markdown_output.write_text(final_markdown, encoding="utf-8")
    print(f"Markdown report written to: {config.markdown_output}")
    print(f"Markdown quality gate: {final_validation['quality_gate']}")

    if config.skip_html:
        return 0
    if final_validation["quality_gate"] != "PASS" and not config.allow_html_on_validation_fail:
        print("HTML conversion blocked because Markdown validation failed. Re-run with --allow-html-on-validation-fail to inspect draft HTML.")
        return 2
    html = convert_markdown_report_to_self_contained_html(final_markdown, f"VendorIQ Report: {config.vendor}")
    config.html_output.write_text(html, encoding="utf-8")
    print(f"HTML report written to: {config.html_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
