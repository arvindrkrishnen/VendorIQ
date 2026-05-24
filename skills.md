# Universal Vendor Analysis Skill

## Purpose

Create one exhaustive, evidence-linked vendor-analysis report for a vendor, public company, or private firm.

The skill supports detailed technology, architecture, product, moat, financial, leadership, and competitive due diligence.

## Required Output Flow

VendorIQ follows a two-stage output flow:

1. Generate the complete report as Markdown.
2. Convert the completed Markdown into one self-contained interactive HTML report.

The final deliverable is:

```text
artifacts/exhaustive_final_report.html
```

In online chat execution, return a downloadable self-contained HTML artifact named:

```text
exhaustive_final_report.html
```

The Markdown report is an intermediate representation. It is used to structure the report, validate evidence, normalize citations, build tables, and prepare the content for HTML conversion. It is not the final user-facing artifact unless the user explicitly asks for Markdown.

## Single Output Rule

Produce only one final persistent user-facing deliverable:

```text
artifacts/exhaustive_final_report.html
```

Do not produce separate progress JSON, evidence JSON, Pugh Matrix JSON, quality JSON, SEC JSON, government-contract JSON, reference JSON, leadership JSON, financial JSON, product JSON, architecture JSON, moat JSON, CSS file, JavaScript file, or image asset.

Intermediate Markdown may be generated during runtime or reasoning, but the final deliverable must be the converted HTML file.

## Execution Entry Point for Online Models

When a user uploads this package to ChatGPT, Gemini AI Studio, Claude, or another model, the model must:

1. Read `SKILL.md`.
2. Read `README.md`.
3. Read this `skills.md` file.
4. Read `agents/agent_registry.md`.
5. Read the relevant playbooks in `playbooks/`.
6. Read guardrails in `guardrails/`.
7. Ask for the vendor name only if the user did not provide it.
8. Execute all required sub-agent sections.
9. Use browsing/search if available.
10. Generate the complete report as Markdown.
11. Validate the Markdown report.
12. Convert the Markdown report into one final self-contained interactive HTML report.

## Required Inputs

Minimum:
- vendor name

Optional:
- ticker;
- official website;
- SEC CIK;
- competitor list;
- industry focus;
- geography;
- depth: `standard` or `exhaustive`.

## Required Sub-Agent Orchestration

The skill must trigger each major report section through a sub-agent.

Required agents include:
- identity and SEC resolution;
- market position;
- business model;
- financial metrics and valuation narrative;
- leadership credentials;
- products and services;
- product-by-product architecture;
- product moat and defensibility;
- customer and supplier intelligence;
- government contracts and public-sector signals;
- SEC filing scan;
- future actions;
- architecture and technology;
- security and compliance;
- AI / ML / GenAI by product;
- competitive landscape;
- product-level Pugh Matrix;
- reference normalization;
- Markdown report assembly;
- Markdown-to-HTML conversion;
- quality evaluation.

## Report Quality Requirements

Each section must be elaborated, not summarized. The Markdown assembly and final HTML report must include:
- annual-report-led company overview for public companies;
- business model and revenue model from annual report, investor report, or official company sources;
- leadership credentials and strategic relevance;
- financial metrics and valuation narrative for public companies;
- exhaustive product catalog;
- product-by-product technical due diligence;
- product-by-product architecture due diligence;
- product-by-product moat and defensibility analysis;
- product-to-capability map;
- key customers and customer segments mapped to products where possible;
- key suppliers, cloud providers, ecosystem dependencies, and partners mapped to products where possible;
- recent government contracts, agency awards, FedRAMP/public-sector marketplace status, or explicit `Not found in public sources reviewed`;
- SEC filing scan in bulleted format for public companies;
- future actions and forward-looking indicators;
- product-level competitive analysis;
- Pugh Matrix;
- Reference Links section with numbered links;
- Quality Document JSON as the final visible section.

## Markdown Assembly Requirements

The Markdown report must:
- contain all required sections;
- use numbered references such as `[1]`, `[2]`, and `[3]`;
- include a `Reference Links` section;
- place `Reference Links` immediately before `Quality Document JSON`;
- place `Quality Document JSON` as the final Markdown section;
- render Pugh Matrix and due-diligence matrices as Markdown tables;
- include `Not found in public sources reviewed` where evidence is unavailable.

## Interactive HTML Conversion Requirements

The converted HTML report must:
- start with `<!doctype html>`;
- include `<html lang="en">`;
- include viewport metadata;
- include internal CSS in a `<style>` block;
- include internal JavaScript in a `<script>` block;
- include semantic `<header>`, `<nav>`, `<main>`, `<section>`, and `<footer>` elements;
- include a sticky header;
- include a clickable table of contents;
- include a section search/filter box;
- include collapsible major sections;
- include expand-all and collapse-all buttons;
- convert Markdown tables into sortable HTML tables;
- include due-diligence cards where useful;
- include linked citations and reference backlinks;
- include print CSS;
- use sufficient contrast and accessible button labels.

The HTML report must not require:
- external CSS;
- external JavaScript;
- CDN links;
- remote fonts;
- external images or assets.

## Product and Architecture Due-Diligence Requirements

For every major product where public evidence exists, include:
- product purpose and target buyer;
- business process / value-chain fit;
- deployment model;
- tenant model;
- core architecture components;
- data architecture;
- integration architecture;
- API / SDK / developer ecosystem;
- standards and interoperability;
- AI / ML / automation architecture;
- security, privacy, and compliance architecture;
- observability and operations;
- scalability, resiliency, backup, DR, failover, RPO/RTO, and SLA signals;
- implementation complexity and migration risks;
- ecosystem dependencies;
- product maturity;
- product limitations and open questions;
- technical moat;
- data moat;
- workflow moat;
- integration moat;
- ecosystem moat;
- compliance moat;
- switching-cost moat;
- distribution moat;
- IP/patent signals where public;
- customer proof and measurable outcomes.

If information is not public, state:

```text
Not found in public sources reviewed.
```

## Competitive Due-Diligence Requirements

Competitive analysis must be product-specific.

For each major vendor product, compare against relevant competitors and substitutes across:
- product-market fit;
- architecture maturity;
- deployment flexibility;
- scalability;
- resiliency / DR;
- security and compliance;
- API maturity;
- integration ecosystem;
- data architecture;
- AI / ML / automation capability;
- workflow depth;
- implementation complexity;
- switching cost;
- customer proof;
- public-sector readiness;
- roadmap / R&D signal;
- technical moat durability;
- commercial moat durability.

## Evidence Requirements

Every factual claim must include a numbered reference such as `[1]`, `[2]`, or `[3]`.

The Markdown report must include:

```markdown
## Reference Links
```

The converted HTML report must include the same references as clickable links.

Preferred evidence order:
1. SEC filings, official annual reports, quarterly reports, and investor relations pages.
2. Official company website, product pages, product documentation, developer/API documentation, architecture documentation, trust/security/privacy pages, leadership pages, and customer stories.
3. Proxy statements and official executive biographies for leadership credentials.
4. Government procurement portals, FedRAMP marketplace, agency award notices, and marketplace listings.
5. Bloomberg, FactSet, Yahoo Finance, Investing.com, and reputable financial/analyst sources.
6. Reputable market-research, standards, technology-review, and news sources.

Do not invent data. Use `Not found in public sources reviewed` when evidence is unavailable.

## Public Company Financial Metrics

For public companies, attempt to include:
- EPS;
- P/E;
- PEG;
- free cash flow;
- cash and cash equivalents;
- total debt;
- debt as % of cash;
- revenue growth;
- margin signals;
- liquidity narrative;
- valuation narrative.

Use this formula where source data is available:

```text
Debt as % of Cash = Total Debt / Cash and Cash Equivalents * 100
```

## Leadership Credentials

Use annual report, proxy statement, company leadership pages, investor reports, official biographies, and LinkedIn or public profiles where available.

For each leader, include:
- current role;
- prior roles;
- education or certifications where verified;
- board memberships where verified;
- strategic relevance to the company.

## Local Provider Support

The Python orchestrator supports:

| Provider | Provider ID | API key |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic Claude | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Perplexity | `perplexity` | `PERPLEXITY_API_KEY` |
| Offline scaffold | `offline` | none |

## Completion Definition

A run is complete only when:
- the Markdown report content has been generated or assembled;
- the Markdown report has been converted to HTML;
- the final HTML report exists;
- the final artifact is named `exhaustive_final_report.html`;
- every required section is present;
- factual claims include numbered references, raw URLs converted to numbered references, or explicit not-found markers;
- all numbered references resolve in `Reference Links`;
- `Reference Links` appears immediately before `Quality Document JSON`;
- public-company financial metrics and leadership credentials are attempted;
- product-by-product technology and architecture due diligence is attempted;
- product moat and competitive moat are attempted;
- product-level Pugh Matrix is converted into an HTML table;
- Quality Document JSON is the final visible section;
- no extra persistent user-facing output files are required.
