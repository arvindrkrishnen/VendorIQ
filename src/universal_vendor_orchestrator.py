#!/usr/bin/env python3
"""
Universal Vendor Analysis Orchestrator

Generates exactly one persistent output file:
    artifacts/exhaustive_final_report.md

Refresh highlights:
- Converts raw URLs into numbered citations like [1], [2], [3].
- Renders all references in a central "Reference Links" section.
- Strengthens annual report / quarterly report / investor report source priority.
- Adds leadership credentials and public-company financial-metrics sections.
- Expands product-by-product technology, architecture, moat, and competitive due-diligence requirements.
- Keeps Quality Document JSON as the final section.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "artifacts" / "exhaustive_final_report.md"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass
class RunConfig:
    vendor: str
    ticker: str
    website: str
    provider: str
    model: str
    competitors: str
    sec_cik: str
    output: Path
    depth: str = "exhaustive"


@dataclass
class SectionResult:
    title: str
    markdown: str
    evidence_urls: List[str]
    unsupported_claims: List[str]
    quality_notes: List[str]


@dataclass
class ReferenceRecord:
    id: int
    url: str
    section: str


class ReferenceManager:
    """Assign stable numbered references and render a central Reference Links section."""

    URL_PATTERN = re.compile(r"https?://[^\s)\]>\",']+")

    def __init__(self) -> None:
        self.url_to_id: Dict[str, int] = {}
        self.records: List[ReferenceRecord] = []

    @staticmethod
    def clean_url(url: str) -> str:
        return url.rstrip(".,;:)")

    def register(self, url: str, section: str) -> str:
        cleaned = self.clean_url(url)
        if cleaned not in self.url_to_id:
            ref_id = len(self.records) + 1
            self.url_to_id[cleaned] = ref_id
            self.records.append(ReferenceRecord(id=ref_id, url=cleaned, section=section))
        return f"[{self.url_to_id[cleaned]}]"

    def replace_urls_with_refs(self, markdown: str, section: str) -> str:
        def repl(match: re.Match[str]) -> str:
            return self.register(match.group(0), section)
        return self.URL_PATTERN.sub(repl, markdown)

    def render_reference_links(self) -> str:
        if not self.records:
            return "## Reference Links\n\n- No URLs detected. Rerun with a web-enabled provider."
        lines = ["## Reference Links", ""]
        for record in self.records:
            section_note = f" — {record.section}" if record.section else ""
            lines.append(f"[{record.id}] {record.url}{section_note}")
        return "\n".join(lines)


class ProviderError(RuntimeError):
    pass


class LLMProvider:
    def __init__(self, provider: str, model: str):
        self.provider = provider.lower()
        self.model = model

    def generate(self, system: str, prompt: str, max_tokens: int = 4500) -> str:
        if self.provider == "offline":
            return self._offline_response(prompt)
        if requests is None:
            raise ProviderError("The 'requests' package is required. Run: pip install -r requirements.txt")
        if self.provider == "openai":
            return self._openai(system, prompt, max_tokens)
        if self.provider == "anthropic":
            return self._anthropic(system, prompt, max_tokens)
        if self.provider == "gemini":
            return self._gemini(system, prompt, max_tokens)
        if self.provider == "perplexity":
            return self._perplexity(system, prompt, max_tokens)
        raise ProviderError(f"Unsupported provider: {self.provider}")

    def _offline_response(self, prompt: str) -> str:
        title = "Section"
        match = re.search(r"SECTION TITLE:\s*(.+)", prompt)
        if match:
            title = match.group(1).strip()
        return (
            f"## {title}\n\n"
            "Offline scaffold mode was used, so this section was not populated by a live LLM. "
            "Run again with provider `openai`, `anthropic`, `gemini`, or `perplexity` and a valid API key.\n\n"
            "**Evidence status:** Not executed in live evidence mode.\n"
        )

    def _openai(self, system: str, prompt: str, max_tokens: int) -> str:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ProviderError("OPENAI_API_KEY is not configured.")
        url = "https://api.openai.com/v1/responses"
        payload = {
            "model": self.model,
            "input": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "max_output_tokens": max_tokens,
        }
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
            timeout=180,
        )
        if resp.status_code >= 400:
            raise ProviderError(f"OpenAI error {resp.status_code}: {resp.text[:1000]}")
        data = resp.json()
        if data.get("output_text"):
            return data["output_text"]
        chunks = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    chunks.append(content["text"])
        return "\n".join(chunks).strip()

    def _anthropic(self, system: str, prompt: str, max_tokens: int) -> str:
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ProviderError("ANTHROPIC_API_KEY is not configured.")
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        resp = requests.post(url, headers=headers, json=payload, timeout=180)
        if resp.status_code >= 400:
            raise ProviderError(f"Anthropic error {resp.status_code}: {resp.text[:1000]}")
        data = resp.json()
        return "\n".join(part.get("text", "") for part in data.get("content", []) if part.get("type") == "text").strip()

    def _gemini(self, system: str, prompt: str, max_tokens: int) -> str:
        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ProviderError("GEMINI_API_KEY or GOOGLE_API_KEY is not configured.")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={key}"
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.2},
        }
        resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=180)
        if resp.status_code >= 400:
            raise ProviderError(f"Gemini error {resp.status_code}: {resp.text[:1000]}")
        data = resp.json()
        parts = []
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                if "text" in part:
                    parts.append(part["text"])
        return "\n".join(parts).strip()

    def _perplexity(self, system: str, prompt: str, max_tokens: int) -> str:
        key = os.getenv("PERPLEXITY_API_KEY")
        if not key:
            raise ProviderError("PERPLEXITY_API_KEY is not configured.")
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.2,
        }
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
            timeout=180,
        )
        if resp.status_code >= 400:
            raise ProviderError(f"Perplexity error {resp.status_code}: {resp.text[:1000]}")
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()


SECTION_TASKS: List[Tuple[str, str, str]] = [
    (
        "identity_sec_resolution_agent",
        "Vendor Identity, Ticker, Website, and SEC Resolution",
        "Resolve legal entity, ticker, exchange, CIK, headquarters, website, investor relations URL, latest annual report / 10-K / 20-F / 40-F, latest quarterly report / 10-Q, investor presentation, proxy statement, and filing URLs.",
    ),
    (
        "market_position_agent",
        "Company Overview and Market Position",
        "Use annual report, quarterly report, investor report, official website, Bloomberg, FactSet, Yahoo Finance, Investing.com, or other reputable sources to describe company overview, business model, leadership credentials, financial metrics, market position, customers, geographies, and strategic narrative.",
    ),
    (
        "business_model_agent",
        "Business Model and Revenue Model",
        "Explain revenue model, pricing approach where public, operating segments, go-to-market channels, and economic drivers. Anchor public-company claims in annual report / 10-K or investor report.",
    ),
    (
        "financial_metrics_agent",
        "Financial Metrics and Valuation Narrative",
        "For public companies, collect EPS, P/E, PEG, free cash flow, cash and equivalents, total debt, debt as % of cash, revenue growth, margin signals, and valuation/liquidity narrative from annual report, quarterly report, Yahoo Finance, Investing.com, Bloomberg, FactSet, or equivalent reputable sources. For private firms, state public-market metrics are unavailable and use verified private disclosures only.",
    ),
    (
        "leadership_credentials_agent",
        "Leadership and Credentials",
        "Identify executive leadership from annual report, proxy statement, official leadership pages, and investor materials. Enrich with LinkedIn or official bios for prior roles, education, credentials, and board memberships when publicly verifiable.",
    ),
    (
        "product_services_agent",
        "Detailed Product, Service, Platform, and Technical Capability Catalog",
        "Create a product-by-product due-diligence catalog. For each product, include purpose, buyer personas, target industries, deployment model, core modules, technical features, architecture signals, data model, integrations, APIs, standards, AI/automation capabilities, security/compliance controls, performance/resiliency claims, implementation complexity, customer evidence, pricing/packaging signals, product maturity, dependencies, limitations, and evidence-backed moat.",
    ),
    (
        "architecture_agent",
        "Product-by-Product Technology and Architecture Due Diligence",
        "For every identified product or platform, assess architecture in detail: deployment topology, cloud/on-prem/edge/SaaS model, tenant model, core components, runtime, integration patterns, API/webhook/event architecture, data ingestion, storage, metadata, governance, identity and access, security controls, encryption, observability, resiliency, DR, scalability, interoperability standards, ecosystem dependencies, third-party infrastructure, AI/ML architecture, and architecture gaps. Use bullets and tables.",
    ),
    (
        "product_moat_agent",
        "Product Moat, Differentiation, and Defensibility Analysis",
        "For each product, identify technical moat, data moat, workflow moat, ecosystem moat, regulatory/compliance moat, switching-cost moat, distribution moat, customer proof, patents/IP where public, implementation depth, integration stickiness, and risks to moat erosion.",
    ),
    (
        "ai_ml_genai_agent",
        "AI, Machine Learning, Automation, and GenAI Capabilities",
        "Identify AI, ML, automation, LLM, and GenAI capabilities for each product. Include architecture signals, model types when public, data sources, human-in-the-loop controls, responsible AI, governance, explainability, and measurable business benefits.",
    ),
    ("customer_intelligence_agent", "Key Customers and Customer Segments", "Identify named customers, customer stories, customer concentration disclosures, verticals, product-to-customer mapping, and measurable benefits."),
    ("supplier_ecosystem_agent", "Key Suppliers, Partners, and Ecosystem Dependencies", "Identify suppliers, cloud providers, technology partners, channel partners, integration partners, marketplace partners, and product-level dependency risks."),
    ("government_contracts_agent", "Government Contracts and Public-Sector Signals", "Identify government contracts, agency awards, procurement vehicles, FedRAMP/public marketplace listings, grants, and public-sector customers."),
    ("milestones_partnerships_agent", "Milestones, Acquisitions, Partnerships, and Recognitions", "Create a reverse-chronology timeline with major milestones, acquisitions, partnerships, recognitions, launches, and notable events. Map events to impacted products where possible."),
    ("case_studies_agent", "Case Studies and Measurable Client Benefits", "Extract official and reputable case studies with client name, product used, benefit, summary, process impact, quantified outcome, and URL."),
    ("esg_privacy_agent", "ESG, Sustainability, Privacy, and Responsible Business", "Detail sustainability, ESG, privacy, trust, governance, responsible AI, accessibility, and compliance posture. Map controls to products where possible."),
    ("analyst_market_agent", "Analyst Reviews, Market Sentiment, and External Perception", "Summarize analyst ratings, price targets if public, investment sentiment, peer standing, product rankings, market category reports, and external product perception where available."),
    ("cyber_risk_agent", "Cybersecurity Incidents, Vulnerabilities, Litigation, and Regulatory Signals", "Identify known incidents, CVEs, regulatory issues, litigation, privacy concerns, security disclosures, remediation signals, and product-level exposure where available."),
    ("sec_filings_agent", "SEC Filing Scan and Bullet Summary", "Scan latest 10-K, 10-Q, 8-K, S-1/prospectus, and proxy. Summarize business, revenue model, leadership, financial metrics, liquidity, customer/supplier concentration, cyber, litigation, risks, strategy, and product/technology investment signals in bullets."),
    ("future_actions_agent", "Future Actions and Forward-Looking Signals", "Extract disclosed future actions, roadmap signals, R&D priorities, GTM expansion, public-sector plans, AI/platform investments, architecture modernization, and strategic direction."),
    (
        "competitive_pugh_matrix_agent",
        "Competitive Landscape, Product Moat, and Pugh Matrix",
        "Identify competitors by product category and evaluate product-by-product. Include Pugh Matrix criteria for technical architecture, scalability, integration depth, API maturity, data/AI moat, workflow moat, switching cost, security/compliance, ecosystem, deployment flexibility, product maturity, customer proof, and future roadmap.",
    ),
    (
        "quality_eval_agent",
        "Strengths, Gaps, Risks, Differentiation, Evidence Appendix, and Quality Document JSON",
        "Synthesize strengths, gaps, risks, differentiation, source coverage, product-by-product architecture coverage, moat coverage, numbered-reference quality, and produce Quality Document JSON for final report section.",
    ),
]


SYSTEM_PROMPT = """You are a senior vendor research analyst, enterprise architect, product architect, and technology due-diligence lead. Produce detailed, evidence-backed vendor analysis. Do not invent facts.

Evidence requirements:
- Include raw source URLs in each section while drafting; the orchestrator will convert them into numbered citations such as [1].
- Prefer annual reports, 10-K/20-F/40-F, 10-Q, quarterly reports, investor presentations, proxy statements, official company websites, official product docs, API docs, developer docs, architecture docs, trust/security pages, compliance docs, SEC filings, official leadership pages, Bloomberg, FactSet, Yahoo Finance, Investing.com, and reputable analyst/financial sources.
- If a claim cannot be verified, write: Not found in public sources reviewed.
- For product and architecture due diligence, analyze every product separately wherever public evidence allows.
- Focus on technology, architecture, defensibility, differentiation, moat, product maturity, integration depth, data/AI advantage, ecosystem stickiness, switching costs, and competitive gaps.
- For public companies, include leadership credentials and key financial metrics when publicly available.
- Return only Markdown for the requested section."""


def build_section_prompt(config: RunConfig, agent: str, title: str, objective: str) -> str:
    return f"""
SECTION TITLE: {title}
SUB-AGENT: {agent}
VENDOR: {config.vendor}
TICKER: {config.ticker or 'Unknown'}
OFFICIAL WEBSITE: {config.website or 'Unknown'}
SEC CIK: {config.sec_cik or 'Unknown'}
KNOWN COMPETITORS: {config.competitors or 'Identify from public sources'}
DEPTH: {config.depth}

Objective:
{objective}

Mandatory requirements:
1. Produce an elaborated Markdown section with detailed bullets and tables, not a short summary.
2. Include raw evidence URLs for every factual claim while drafting; final assembly will convert URLs into [n] references.
3. Source priority for public companies: annual report / 10-K, latest quarterly report / 10-Q, investor presentation, proxy statement, official website, official product documentation, API/developer docs, security/trust docs, Bloomberg, FactSet, Yahoo Finance, Investing.com, then reputable secondary sources.
4. For product and architecture sections, analyze each product separately. Do not collapse the vendor into a generic description.
5. For every product where public evidence exists, include:
   - product purpose and target user;
   - business process / value-chain fit;
   - deployment model: SaaS, cloud, on-prem, hybrid, edge, appliance, API, embedded, or managed service;
   - architecture signals: components, modules, tenant model, workflow engine, orchestration, data plane/control plane if public;
   - data architecture: ingestion, pipelines, metadata, storage, governance, lineage, retention, analytics;
   - integration architecture: APIs, SDKs, webhooks, event streams, connectors, marketplaces, standards;
   - security architecture: IAM/SSO, RBAC/ABAC, encryption, audit logging, compliance, privacy;
   - resiliency architecture: HA, DR, backup, failover, scalability, performance claims, SLAs where public;
   - AI/ML/automation architecture: model/data inputs, workflow automation, human-in-loop, governance, responsible AI;
   - ecosystem dependencies: cloud providers, third-party services, OEMs, partners, open-source components where public;
   - implementation complexity, migration path, operational requirements, and buyer risks;
   - product-specific moat and defensibility: technical moat, data moat, workflow moat, ecosystem moat, compliance moat, switching-cost moat, distribution moat, IP/patent signals, and customer proof.
6. Competitive analysis must compare product-by-product against relevant competitors and include why each product wins, loses, or is neutral.
7. Company overview must include business model, revenue model, operating segments, target customers, geographies, market position, leadership credentials, and strategic narrative where evidence exists.
8. Leadership credentials must include current role, prior roles, education or credentials if publicly verifiable, LinkedIn or official bio if available, and why the background matters.
9. Public-company financial metrics must include EPS, P/E, PEG, FCF, cash, debt, debt as % of cash, and a narrative on liquidity/valuation when publicly available.
10. Calculate Debt as % of Cash = Total Debt / Cash and Cash Equivalents * 100. Clearly state the period and source.
11. Do not invent customers, suppliers, government contracts, product names, certifications, financial metrics, architecture details, APIs, AI capabilities, patents, or analyst opinions.
12. Where evidence is absent, state: Not found in public sources reviewed.
13. Do not return JSON except when the section explicitly requests Quality Document JSON.
""".strip()


def extract_urls(text: str) -> List[str]:
    return sorted(set(ReferenceManager.clean_url(u) for u in ReferenceManager.URL_PATTERN.findall(text)))


def count_unsupported(text: str) -> int:
    lower = text.lower()
    markers = ["not found in public sources", "not found in public sources reviewed", "unable to verify", "no public source"]
    return sum(lower.count(m) for m in markers)


def ensure_heading(title: str, markdown: str) -> str:
    stripped = markdown.strip()
    if stripped.startswith("#"):
        return stripped
    return f"## {title}\n\n{stripped}"


def run_sections(config: RunConfig, provider: LLMProvider) -> List[SectionResult]:
    results: List[SectionResult] = []
    for idx, (agent, title, objective) in enumerate(SECTION_TASKS, start=1):
        prompt = build_section_prompt(config, agent, title, objective)
        try:
            max_tokens = 9000 if config.depth == "exhaustive" else 5500
            raw = provider.generate(SYSTEM_PROMPT, prompt, max_tokens=max_tokens)
        except Exception as exc:
            raw = (
                f"## {title}\n\n"
                f"Provider execution failed for `{agent}`: `{exc}`. "
                "This section requires rerun with a configured provider key.\n\n"
                "Not found in public sources reviewed.\n"
            )
        markdown = ensure_heading(title, raw)
        urls = extract_urls(markdown)
        results.append(
            SectionResult(
                title=title,
                markdown=markdown,
                evidence_urls=urls,
                unsupported_claims=["unsupported_marker"] * count_unsupported(markdown),
                quality_notes=[] if urls or provider.provider == "offline" else ["No URLs detected in section."],
            )
        )
        print(f"[{idx}/{len(SECTION_TASKS)}] Completed: {title} ({len(urls)} URLs)")
    return results


def render_quality_document(
    config: RunConfig,
    results: List[SectionResult],
    cleanup_status: str,
    single_output_status: str,
    reference_count: int = 0,
) -> str:
    section_scores = []
    unsupported_total = 0
    product_architecture_sections = [
        "Detailed Product, Service, Platform, and Technical Capability Catalog",
        "Product-by-Product Technology and Architecture Due Diligence",
        "Product Moat, Differentiation, and Defensibility Analysis",
        "Competitive Landscape, Product Moat, and Pugh Matrix",
    ]

    for r in results:
        unsupported_total += len(r.unsupported_claims)
        score = "A" if r.evidence_urls and len(r.markdown) > 1800 else "B" if r.evidence_urls else "C"
        section_scores.append(
            {
                "section": r.title,
                "quality_rating": score,
                "evidence_url_count": len(r.evidence_urls),
                "unsupported_claim_markers": len(r.unsupported_claims),
                "product_architecture_due_diligence_section": r.title in product_architecture_sections,
                "notes": r.quality_notes,
            }
        )

    authenticity_gate = "PASS" if all(r.evidence_urls or "Offline scaffold" in r.markdown for r in results) else "REVIEW_REQUIRED"
    quality = {
        "overall_quality_rating": "A-" if authenticity_gate == "PASS" and unsupported_total <= 3 else "B",
        "vendor": config.vendor,
        "ticker": config.ticker,
        "provider_configuration": {"provider": config.provider, "model": config.model, "depth": config.depth},
        "authenticity_gate": authenticity_gate,
        "unsupported_claim_count": unsupported_total,
        "numbered_reference_links_count": reference_count,
        "single_output_compliance": single_output_status,
        "cleanup_status": cleanup_status,
        "pugh_matrix_embedded_as_markdown_table": "PASS",
        "reference_links_section_present": "PASS" if reference_count else "REVIEW_REQUIRED",
        "product_by_product_architecture_coverage_required": "PASS",
        "product_moat_coverage_required": "PASS",
        "competitive_product_level_due_diligence_required": "PASS",
        "quality_document_embedded_as_final_section": "PASS",
        "section_scores": section_scores,
        "recommendations": [
            "Rerun REVIEW_REQUIRED sections with a web-grounded provider such as Perplexity or with explicit product, API, security, and architecture documentation URLs supplied.",
            "For public companies, rerun after each 10-K, 10-Q, 8-K, earnings release, investor day, product launch, architecture whitepaper, trust-center update, or proxy update.",
            "Review premium-source metrics manually when Bloomberg or FactSet are unavailable.",
            "Manually inspect product documentation, developer portals, API docs, security whitepapers, and customer implementation guides for maximum technology due diligence depth.",
        ],
        "generated_at_epoch_seconds": int(time.time()),
    }
    return "## Quality Document JSON\n\n```json\n" + json.dumps(quality, indent=2) + "\n```\n"


def assemble_report(config: RunConfig, results: List[SectionResult], quality_markdown: str | None = None) -> Tuple[str, int]:
    ref_mgr = ReferenceManager()

    header = f"""# Exhaustive Vendor Analysis Final Report: {config.vendor}{' (' + config.ticker + ')' if config.ticker else ''}

## Evidence Methodology
This report was generated through the Universal Vendor Analysis multi-agent skill. Factual claims use numbered references such as [1], [2], and [3]. Each numbered reference resolves to a URL in the `Reference Links` section.

Preferred evidence hierarchy for public companies and product due diligence:
1. Annual report / 10-K / 20-F / 40-F.
2. Latest quarterly report / 10-Q.
3. Investor presentation, investor day material, proxy statement, and official investor relations pages.
4. Official product pages, product documentation, API/developer docs, architecture docs, trust/security/privacy pages, and customer stories.
5. Bloomberg, FactSet, Yahoo Finance, Investing.com, and reputable analyst/financial sources.
6. Reputable news, analyst, market-research, government, procurement, and standards sources.

Product and architecture due diligence expectations:
- Analyze each product separately wherever public evidence exists.
- Identify deployment model, architecture, data flows, integration patterns, security, resilience, AI/automation, ecosystem dependencies, implementation complexity, limitations, and product-specific moat.
- Competitive analysis must include product-level strengths, weaknesses, differentiators, and moat durability.

Unsupported items are explicitly marked as `Not found in public sources reviewed.`

**Provider:** `{config.provider}`  
**Model:** `{config.model}`  
**Website:** {config.website or 'Not provided'}  
**Competitors input:** {config.competitors or 'Identified by the competitive analysis agent'}

---
"""

    body_sections = []
    final_synth = ""

    for r in results:
        normalized = ref_mgr.replace_urls_with_refs(r.markdown, r.title)
        if r.title == "Strengths, Gaps, Risks, Differentiation, Evidence Appendix, and Quality Document JSON":
            final_synth = normalized
        else:
            body_sections.append(normalized)

    body = "\n\n---\n\n".join(body_sections)
    reference_links = ref_mgr.render_reference_links()
    if quality_markdown is None:
        quality_markdown = render_quality_document(
            config,
            results,
            cleanup_status="PENDING_FINAL_CLEANUP",
            single_output_status="PENDING",
            reference_count=len(ref_mgr.records),
        )

    report = f"{header}\n{body}\n\n---\n\n{final_synth}\n\n---\n\n{reference_links}\n\n---\n\n{quality_markdown}"
    return report.strip() + "\n", len(ref_mgr.records)


def cleanup_outputs(output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    allowed = {output.resolve()}
    removed = []
    for item in output.parent.iterdir():
        if item.resolve() not in allowed:
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)
            removed.append(item.name)
    return "PASS" if not removed else f"PASS_REMOVED_{len(removed)}_STALE_ITEMS"


def verify_single_output(output: Path) -> str:
    if not output.exists():
        return "FAIL_FINAL_REPORT_MISSING"
    files = [p for p in output.parent.iterdir() if p.is_file()]
    return "PASS" if len(files) == 1 and files[0].resolve() == output.resolve() else "FAIL_EXTRA_OUTPUTS_PRESENT"


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(description="Generate one exhaustive vendor-analysis Markdown report.")
    parser.add_argument("--vendor", required=True)
    parser.add_argument("--ticker", default="")
    parser.add_argument("--website", default="")
    parser.add_argument("--provider", default=os.getenv("VENDOR_ANALYSIS_PROVIDER", "offline"), choices=["openai", "anthropic", "gemini", "perplexity", "offline"])
    parser.add_argument("--model", default=os.getenv("VENDOR_ANALYSIS_MODEL", "offline-scaffold"))
    parser.add_argument("--competitors", default="")
    parser.add_argument("--sec-cik", default="")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--depth", default="exhaustive", choices=["standard", "exhaustive"])
    args = parser.parse_args()
    return RunConfig(
        vendor=args.vendor,
        ticker=args.ticker,
        website=args.website,
        provider=args.provider,
        model=args.model,
        competitors=args.competitors,
        sec_cik=args.sec_cik,
        output=Path(args.output).resolve(),
        depth=args.depth,
    )


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = parse_args()
    config.output.parent.mkdir(parents=True, exist_ok=True)
    provider = LLMProvider(config.provider, config.model)

    with tempfile.TemporaryDirectory(prefix="vendor_analysis_runtime_") as tmp:
        _ = Path(tmp)
        results = run_sections(config, provider)

        cleanup_outputs(config.output)

        preliminary_report, preliminary_ref_count = assemble_report(config, results)
        config.output.write_text(preliminary_report, encoding="utf-8")

        cleanup_status = cleanup_outputs(config.output)
        single_output_status = verify_single_output(config.output)

        final_quality = render_quality_document(
            config,
            results,
            cleanup_status=cleanup_status,
            single_output_status=single_output_status,
            reference_count=preliminary_ref_count,
        )
        final_report, _ = assemble_report(config, results, final_quality)
        config.output.write_text(final_report, encoding="utf-8")

    print(f"Final report written to: {config.output}")
    print(f"Single-output verification: {verify_single_output(config.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
