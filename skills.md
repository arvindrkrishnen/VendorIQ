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

The skill must trigger each major section through a sub-agent. 

Required agents include identity + financial metrics, executive leadership, market position, business model, product/service catalog, architecture, information architecture, application architecture, security architecture, interoperability, resiliency/DR, AI/ML/GenAI, product moat, customers, suppliers, government contracts, milestones, case studies, ESG/privacy, analyst sentiment, cybersecurity/litigation, SEC filing scan, future actions, competitive landscape, Pugh Matrix, reference normalization, Markdown assembly, Markdown-to-HTML conversion, and quality evaluation.


## Combined Identity and Financial Metrics Requirement

Combine the former vendor identity section with the former financial metrics and valuation narrative. The combined section must be titled:

```text
Vendor Identity, Public Status, Financial Metrics and Valuation Narrative
```

For public companies with ticker data, include:

- vendor legal identity, ticker, exchange, website, headquarters, public/private status, SEC CIK, and latest filing basis;
- last four quarterly revenue, profitability / net income, and EPS where public;
- last three fiscal years revenue, profitability / net income, and EPS where public;
- monthly stock-price close for the last three years;
- visualizations for quarterly revenue/profitability, annual revenue/profitability/EPS, and monthly stock price changes;
- references from Yahoo Finance, Investing.com, Bloomberg, FactSet, Morningstar, Fidelity, SEC site, issuer filings, and investor relations where available.

If any metric is unavailable, state `Not found in public sources reviewed`.

## Executive Leadership Requirement

Include a dedicated section titled:

```text
Executive Leadership and Credentials
```

For each leader, include verified name, current role, prior roles, public credentials, strategic relevance, and source URLs. Do not infer experience from titles alone.

## Report Quality Requirements

Each section must be elaborated, not summarized. In exhaustive mode, each section should contain 500+ words of narrative analysis unless reliable public evidence is unavailable. Every factual claim must include a raw source URL while drafting. The orchestrator will normalize URLs into numbered references.

The Markdown assembly and final HTML report must include:

- annual-report-led company overview for public companies;
- business model and revenue model from annual report, investor report, or official company sources;
- executive leadership credentials;
- financial metrics and valuation narrative using Yahoo Finance, Investing.com, Bloomberg, FactSet, Morningstar, Fidelity, issuer filings, and investor relations where available;
- the required financial and stock-price visualizations;
- exhaustive product catalog;
- product-by-product technical due diligence;
- product-by-product architecture due diligence;
- product-by-product moat and defensibility analysis;
- product-to-capability map;
- key customers and customer segments mapped to products where possible;
- key suppliers, cloud providers, ecosystem dependencies, and partners mapped to products where possible;
- recent government contracts, public-sector awards, FedRAMP/public-sector marketplace status, or explicit `Not found in public sources reviewed`;
- SEC filing scan for public companies;
- future actions and forward-looking indicators;
- product-level competitive analysis;
- Pugh Matrix;
- Reference Links section with numbered links;
- Quality Document JSON as the final visible section.

## Evidence Requirements

Preferred evidence order:

1. SEC filings, official annual reports, quarterly reports, investor relations pages, investor presentations, and proxy statements.
2. Official company website, product pages, product documentation, API/developer documentation, architecture documentation, trust/security/privacy pages, leadership pages, and customer stories.
3. Yahoo Finance, Investing.com, Bloomberg, FactSet, Morningstar, Fidelity, and reputable financial/analyst sources.
4. Government procurement portals, FedRAMP marketplace, agency award notices, and marketplace listings.
5. Reputable news, standards, technology-review, and market-research sources.

Do not invent data. Use `Not found in public sources reviewed` when evidence is unavailable.

## Product and Architecture Due-Diligence Requirements

For every major product where public evidence exists, include product purpose, target buyer, workflow fit, deployment model, tenant model, core components, data architecture, integration architecture, API / SDK ecosystem, standards, AI / ML / automation architecture, security, privacy, compliance, observability, resiliency, backup, DR, failover, RPO/RTO, SLA signals, implementation complexity, ecosystem dependencies, product maturity, limitations, technical moat, data moat, workflow moat, integration moat, ecosystem moat, compliance moat, switching-cost moat, distribution moat, IP/patent signals where public, customer proof, and measurable outcomes.

## Competitive Due-Diligence Requirements

Competitive analysis must be product-specific. For each major vendor product, compare relevant competitors across product-market fit, architecture maturity, deployment flexibility, scalability, resiliency/DR, security and compliance, API maturity, integration ecosystem, data architecture, AI / ML / automation capability, workflow depth, implementation complexity, switching cost, customer proof, public-sector readiness, roadmap/R&D signal, technical moat durability, and commercial moat durability.

## Interactive HTML Conversion Requirements

The converted HTML report must be self-contained and include internal CSS, internal JavaScript, sticky header, clickable table of contents, section search/filter, collapsible sections, expand/collapse controls, sortable HTML tables, clickable citations, chart visualizations, reference backlinks, and print-friendly CSS. It must not depend on external CSS, JavaScript, CDN links, remote fonts, external images, or external assets.

## Local Provider Support

| Provider | Provider ID | API key |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic Claude | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Perplexity | `perplexity` | `PERPLEXITY_API_KEY` |
| Offline scaffold | `offline` | none |

## Completion Definition

A run is complete only when Markdown is generated, references are normalized, validation is executed, final HTML exists as `exhaustive_final_report.html`, every required section is present, financial and stock visualizations are included for public tickers where available, every factual claim is cited or marked not found, product moat and differentiation are detailed, Pugh Matrix is converted into an HTML table, and Quality Document JSON is the final visible section.
