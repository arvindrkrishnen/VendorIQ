# VendorIQ Universal Vendor Analysis Skill
**Product name:** VendorIQ  
**Author:** Arvind Radhakrishnen

## Purpose

VendorIQ generates one exhaustive, evidence-backed vendor-analysis report for a target company, vendor, public company, or private firm.

The skill supports detailed due diligence across company identity, public/private status, financial metrics, valuation narrative, executive leadership, business model, revenue model, product and service catalog, product-by-product technology architecture, AI/ML/GenAI capabilities, customer and supplier ecosystem, government and public-sector signals, ESG/privacy posture, analyst sentiment, cybersecurity/litigation signals, SEC filing scan, future actions, competitive landscape, product moat, differentiation, and Pugh Matrix.

## One-Shot Trigger Prompt (Recommended for Groq, ChatGPT, Gemini, Claude)
Use this GitHub repository as the VendorIQ skill package: https://github.com/arvindrkrishnen/VendorIQ
Read README.md and SKILL.MD first, then guardrails/, agents/, playbooks/, and templates/.
Execute the Universal Vendor Analysis Skill for vendor: [INSERT VENDOR NAME HERE]
Optional ticker: [INSERT TICKER IF KNOWN]
Optional website: [INSERT WEBSITE IF KNOWN]
Follow the package rules exactly:

Use the agents and playbooks as the execution plan.
Use web browsing/search if available.
Generate the full report content as Markdown first.
Every factual claim in the Markdown report must include a numbered citation such as [1], [2], or [3].
Every numbered citation must resolve to a source URL in the Reference Links section.
Do not invent customers, suppliers, government contracts, certifications, SEC details, product names, APIs, architecture details, financial metrics, leadership credentials, or analyst commentary.
After the Markdown report is complete, convert the Markdown into one self-contained interactive HTML artifact named exhaustive_final_report.html.
Embed the Pugh Matrix and all due-diligence matrices as sortable HTML tables.
Put Reference Links immediately before Quality Document JSON.
Make Quality Document JSON the final visible section in the HTML report.

Produce ONLY the final self-contained exhaustive_final_report.html file as output.

## Groq / Gemini Optimization Note
If full parallel multi-agent orchestration is not supported by the model, fall back to sequential execution of sections while still strictly following the Package Rules and producing the final self-contained HTML report.

## Required Output Flow

VendorIQ follows a two-stage output flow:

1. Generate the complete report as Markdown.
2. Convert the completed Markdown into one self-contained interactive HTML report.

The final user-facing artifact must be:

```text
exhaustive_final_report.html
```

For local execution, the final artifact must be:

```text
artifacts/exhaustive_final_report.html
```

The Markdown report is an intermediate representation used for report assembly, validation, reference normalization, table preparation, chart preparation, and HTML conversion. Do not treat Markdown as the final deliverable unless the user explicitly requests Markdown.

## Single Output Rule

Produce only one final persistent user-facing deliverable:

```text
artifacts/exhaustive_final_report.html
```

Do not produce separate persistent progress JSON, evidence JSON, Pugh Matrix JSON, quality JSON, SEC JSON, government-contract JSON, reference JSON, leadership JSON, financial JSON, product JSON, architecture JSON, moat JSON, CSS file, JavaScript file, image asset, or other standalone output file.

Intermediate Markdown may be generated during runtime, but the final deliverable must be the converted HTML file.

## Required Input

Minimum:
- Vendor name

Optional:
- Ticker
- Website
- SEC CIK
- Competitor list
- Industry focus
- Geography
- Depth: `standard` or `exhaustive`

## Execution Order for ChatGPT, Claude, Gemini, and Other Online Agents

1. Read this `SKILL.MD` file first.
2. Read `README.md`.
3. Read `agents/agent_registry.md`.
4. Read `guardrails/`.
5. Read relevant files in `playbooks/`, including `playbooks/sub-agent-co-ordination-playbook.md`.
6. Use `templates/exhaustive_final_report_template.md` as the report-section structure.
7. Ask for the vendor name only if the user did not provide it.
8. Use web browsing/search/grounding where available.
9. Execute the required sub-agent workflow using `playbooks/sub-agent-co-ordination-playbook.md` for parallel orchestration, dependency sequencing, validation, and consolidation.
10. Generate the complete report as Markdown.
11. Validate that Markdown includes all required sections, evidence markers, numbered citations, Reference Links, required tables, and Quality Document JSON.
12. Convert the validated Markdown into one self-contained interactive HTML artifact named `exhaustive_final_report.html`.

## Execution Order for Local CLI

1. Clone the repository.
2. Install dependencies.
3. Configure `.env`.
4. Run `src/universal_vendor_orchestrator.py`.
5. Use an HTML output path so the generated Markdown is converted into HTML.

Example:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Coherent Corp." \
  --ticker COHR \
  --website https://www.coherent.com \
  --provider perplexity \
  --model sonar-pro \
  --depth exhaustive \
  --html-output artifacts/exhaustive_final_report.html
```

## Parallel Sub-Agent Orchestration Playbook

**For Chat Interfaces (Groq Chat or Gemini AI Studio):**
- If full multi-agent orchestration fails or report is incomplete, use this simplified sequential prompt:
  ```
  Use the VendorIQ skill from https://github.com/arvindrkrishnen/VendorIQ.
  Follow SKILL.MD strictly but execute sections sequentially using the SECTION_TASKS list from src/universal_vendor_orchestrator.py.
  Generate one section at a time, collect all, then assemble Markdown, normalize references, and convert to self-contained HTML.
  Ensure every section is 500+ words where evidence exists, with proper citations.

Use the agents and playbooks as the execution plan.
Use web browsing/search if available.
Generate the full report content as Markdown first.
Every factual claim in the Markdown report must include a numbered citation such as [1], [2], or [3].
Every numbered citation must resolve to a source URL in the Reference Links section.
Do not invent customers, suppliers, government contracts, certifications, SEC details, product names, APIs, architecture details, financial metrics, leadership credentials, or analyst commentary.
After the Markdown report is complete, convert the Markdown into one self-contained interactive HTML artifact named exhaustive_final_report.html.
Embed the Pugh Matrix and all due-diligence matrices as sortable HTML tables.
Put Reference Links immediately before Quality Document JSON.
Make Quality Document JSON the final visible section in the HTML report.

  ```

For ChatGPT/OpenAI, VendorIQ must invoke the dedicated playbook below whenever the required sub-agent workflow is executed:

```text
playbooks/sub-agent-co-ordination-playbook.md
```

This playbook defines the master-agent orchestration pattern, parallel execution rules, dependency sequencing, sub-agent output contracts, retry behavior, evidence validation, conflict resolution, confidence scoring, reference normalization, and final consolidation logic.

The `SKILL.MD` file remains the governing skill contract. The playbook is the operational procedure used by the orchestrator to execute the skill. If the playbook and this skill conflict, this `SKILL.MD` file takes precedence.

The orchestrator must use the playbook to:
- decompose the VendorIQ report into specialized sub-agent tasks;
- run independent sub-agents in parallel where dependencies allow;
- collect section-ready Markdown only;
- normalize raw evidence URLs into numbered citations;
- detect and resolve contradictions across agents;
- preserve not-found markers where public evidence is unavailable;
- assemble the complete Markdown report;
- validate the final Markdown before HTML conversion;
- produce only the final persistent HTML artifact required by this skill.

## New: Model Compatibility Notes
- Optimized for ChatGPT/OpenAI.
- For Groq and Gemini:  In chat mode, use sequential execution if parallel orchestration in playbooks fails to produce comprehensive output. Ensure all sections from SECTION_TASKS in orchestrator are covered for full report comprehensiveness.

## Required Sub-Agent Orchestration - for OpenAI / ChatGPT 

The skill must trigger each major report section through a specialized sub-agent. The orchestrator owns the final output and must coordinate the sub-agents, normalize references, assemble the report, validate quality, and trigger HTML conversion.

Required agents include:
- identity and financial metrics agent;
- executive leadership agent;
- market position agent;
- business model and revenue model agent;
- product/service catalog agent;
- product-to-capability mapping agent;
- architecture agent;
- information architecture agent;
- application architecture agent;
- security architecture agent;
- standards and interoperability agent;
- resiliency and disaster recovery agent;
- AI/ML/GenAI capabilities agent;
- product moat and differentiation agent;
- customer segments agent;
- suppliers, cloud providers, technology partners, and ecosystem dependencies agent;
- government contracts and public-sector signals agent;
- milestones, acquisitions, partnerships, and recognitions agent;
- case studies and measurable client benefits agent;
- ESG, sustainability, privacy, and responsible-business posture agent;
- analyst reviews, market sentiment, and external perception agent;
- cybersecurity, vulnerabilities, regulatory issues, and litigation signals agent;
- SEC filing scan agent;
- future actions and forward-looking indicators agent;
- competitive landscape and Pugh Matrix agent;
- strengths, gaps, risks, and differentiation agent;
- reference normalization agent;
- quality evaluation agent;
- Markdown-to-HTML conversion agent.

## Agent Output Rule

All agents and sub-agents must return Markdown only.

Agents must not produce:
- HTML;
- CSS;
- JavaScript;
- separate JSON artifacts;
- separate files;
- standalone evidence files;
- standalone charts or image assets.

Each agent must return:
- section-ready Markdown;
- raw evidence URLs while drafting;
- required Markdown tables where useful;
- not-found markers where evidence is unavailable;
- quality notes where evidence is weak or incomplete.

## Requirements - Follow the package rules:

Use the agents and playbooks as the execution plan.
Use web browsing/search if available.
Generate the full report content as Markdown first.
Every factual claim in the Markdown report must include a numbered citation such as [1], [2], or [3].
Every numbered citation must resolve to a source URL in the Reference Links section.
Do not invent customers, suppliers, government contracts, certifications, SEC details, product names, APIs, architecture details, financial metrics, leadership credentials, or analyst commentary.
After the Markdown report is complete, convert the Markdown into one self-contained interactive HTML artifact named exhaustive_final_report.html.
Embed the Pugh Matrix and all due-diligence matrices as sortable HTML tables.
Put Reference Links immediately before Quality Document JSON.
Make Quality Document JSON the final visible section in the HTML report.

## Minimum Depth Requirements

In exhaustive mode, each major report section should contain 500+ words of narrative analysis excluding tables, unless reliable public evidence is unavailable.

If public evidence is unavailable, the section must state:

```text
Not found in public sources reviewed
```

and explain what kind of source was searched or would be required to verify the claim.

Product, architecture, moat, financial, leadership, and competitive sections should be substantially detailed when public evidence exists.

## Combined Identity and Financial Metrics Requirement

Combine the former vendor identity section with the former financial metrics and valuation narrative. The combined section must be titled:

```text
Vendor Identity, Public Status, Financial Metrics and Valuation Narrative
```

For public companies with ticker data, include:
- vendor legal identity;
- ticker;
- exchange;
- official website;
- headquarters;
- public/private status;
- SEC CIK where available;
- latest filing basis;
- last four quarterly revenue, profitability / net income, and EPS where public;
- last three fiscal years revenue, profitability / net income, and EPS where public;
- monthly stock-price close for the last three years;
- visualization for quarterly revenue and profitability;
- visualization for annual revenue, profitability, and EPS;
- visualization for monthly stock price changes over the last three years;
- references from Yahoo Finance, Investing.com, Bloomberg, FactSet, Morningstar, Fidelity, SEC, issuer filings, and investor relations where available.

If any metric is unavailable, state:

```text
Not found in public sources reviewed
```

Do not invent financial metrics. Do not estimate missing financial values unless the source explicitly provides enough information and the calculation is shown.

## Executive Leadership Requirement

Include a dedicated section titled:

```text
Executive Leadership and Credentials
```

For each leader, include:
- verified name;
- current role;
- prior roles;
- public credentials where verified;
- board memberships where verified;
- education or certifications where verified;
- strategic relevance to the company;
- source URLs.

Do not infer leadership experience from titles alone. Do not invent education, tenure, prior employers, or credentials.

## Markdown Assembly Requirements

The Markdown report must:
- include all required report sections;
- use numbered citations such as `[1]`, `[2]`, and `[3]` after reference normalization;
- include raw URLs while sub-agents are drafting so the orchestrator can normalize them;
- include `Reference Links`;
- place `Reference Links` immediately before `Quality Document JSON`;
- make `Quality Document JSON` the final Markdown section;
- render Pugh Matrix and due-diligence matrices as Markdown tables before conversion;
- include `Not found in public sources reviewed` where evidence is unavailable.

## Required Report Quality

Each section must be elaborated, not summarized. The Markdown assembly and final HTML report must include:
- annual-report-led company overview for public companies;
- business model and revenue model from annual report, investor report, or official company sources;
- executive leadership credentials;
- financial metrics and valuation narrative using Yahoo Finance, Investing.com, Bloomberg, FactSet, Morningstar, Fidelity, issuer filings, SEC filings, and investor relations where available;
- required financial and stock-price visualizations for public tickers where data is available;
- exhaustive product catalog;
- product-by-product technical due diligence;
- product-by-product architecture due diligence;
- product-by-product moat and defensibility analysis;
- product-to-capability map;
- key customers and customer segments mapped to products where possible;
- key suppliers, cloud providers, ecosystem dependencies, and partners mapped to products where possible;
- recent government contracts, public-sector awards, FedRAMP/public-sector marketplace status, or explicit not-found markers;
- SEC filing scan for public companies;
- future actions and forward-looking indicators;
- product-level competitive analysis;
- Pugh Matrix;
- Reference Links section with numbered links;
- Quality Document JSON as the final visible section.

## Evidence Rules

Every factual claim must include a raw source URL while drafting. After reference normalization, every factual claim must include a numbered citation such as `[1]`, `[2]`, or `[3]`.

Every numbered citation must resolve to a source URL in the `Reference Links` section.

Preferred evidence order:
1. SEC filings, official annual reports, quarterly reports, investor relations pages, investor presentations, and proxy statements.
2. Official company website, product pages, product documentation, API/developer documentation, architecture documentation, trust/security/privacy pages, leadership pages, and customer stories.
3. Yahoo Finance, Investing.com, Bloomberg, FactSet, Morningstar, Fidelity, and reputable financial/analyst sources.
4. Government procurement portals, FedRAMP marketplace, agency award notices, and marketplace listings.
5. Reputable news, standards, technology-review, and market-research sources.

Do not invent data. Use `Not found in public sources reviewed` when evidence is unavailable.

Do not infer:
- customers from logos unless the source clearly names them as customers;
- government contracts from vague public-sector marketing language;
- product architecture from marketing claims alone;
- certifications without a source;
- executive credentials without a source;
- financial metrics without a source;
- product names, APIs, integrations, partnerships, or suppliers without evidence.

## Product and Architecture Due-Diligence Requirements

For every major product where public evidence exists, include:
- product purpose;
- target buyer;
- target industries or segments;
- business problem solved;
- value-chain or workflow fit;
- deployment model;
- tenant model;
- core modules and features;
- core architecture components;
- data architecture;
- integration architecture;
- API / SDK / developer ecosystem;
- standards and interoperability;
- AI / ML / automation architecture;
- security, privacy, and compliance architecture;
- observability and operations;
- scalability, resiliency, backup, DR, failover, RPO/RTO, and SLA signals;
- implementation model and migration complexity;
- ecosystem dependencies;
- product maturity signals;
- known limitations and open questions;
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
Not found in public sources reviewed
```

## Product Moat and Differentiation Requirements

Product moat and differentiation must be detailed, product-specific, and evidence-backed.

Assess each major product across:
- technical moat;
- data moat;
- workflow moat;
- ecosystem moat;
- compliance moat;
- switching-cost moat;
- distribution moat;
- integration moat;
- customer proof;
- implementation depth;
- defensibility durability;
- erosion risk from competitors or substitutes.

Do not use generic statements such as “strong AI capabilities” or “robust platform” unless supported by evidence and explained in product-specific terms.

## Competitive Due-Diligence Requirements

Competitive analysis must be product-specific. For each major vendor product, compare relevant competitors and substitutes across:
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

The Pugh Matrix must be rendered as a Markdown table before HTML conversion.

## HTML Conversion Requirements

The converted HTML report must be self-contained:
- all CSS embedded in a `<style>` block;
- all JavaScript embedded in a `<script>` block;
- no external CSS framework;
- no external JavaScript library;
- no remote fonts;
- no CDN links;
- no external assets required to render the report.

The HTML report must include:
- sticky header;
- clickable table of contents;
- search/filter box;
- expand-all and collapse-all controls;
- collapsible major sections;
- sortable tables;
- product-level due-diligence matrices;
- product architecture matrices;
- product moat matrices;
- competitive Pugh Matrix;
- clickable citations;
- chart visualizations where available;
- reference backlinks;
- Reference Links section;
- Quality Document JSON as the final visible section;
- print-friendly CSS.

## Local Provider Support

| Provider | Provider ID | API key |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic Claude | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Perplexity | `perplexity` | `PERPLEXITY_API_KEY` |
| Offline scaffold | `offline` | none |

## Final Section Order

The final visible content sections must end in this order:

1. `Reference Links`
2. `Quality Document JSON`

`Quality Document JSON` must be the final visible section in both the Markdown assembly and converted HTML report.

## Parallel Orchestration Production Controls

When implemented in a local CLI, server-side workflow, or agent runtime, VendorIQ should apply these default controls unless the runtime or provider requires stricter limits:

```yaml
parallel_orchestration:
  playbook: playbooks/sub-agent-co-ordination-playbook.md
  enabled: true
  max_parallel_agents: 6
  timeout_seconds_per_agent: 90
  max_retries_per_agent: 2
  fallback_strategy: partial_markdown_with_not_found_markers
  preserve_partial_results: true
  fail_fast: false
  finalization_agents_must_succeed:
    - reference normalization agent
    - quality evaluation agent
    - Markdown-to-HTML conversion agent
```

The orchestrator may lower concurrency to respect model-provider, search-provider, browser, API, or system resource limits. The orchestrator must not lower evidence standards, citation requirements, quality gates, or final artifact requirements.

## Completion Definition

A run is complete only when:
- Markdown is generated;
- sub-agent sections are assembled;
- references are normalized;
- validation is executed;
- final HTML exists as `exhaustive_final_report.html`;
- every required section is present;
- financial and stock visualizations are included for public tickers where data is available;
- every factual claim is cited or marked not found;
- executive leadership is included when public evidence exists;
- product moat and differentiation are detailed;
- product-by-product architecture due diligence is attempted;
- product-level competitive analysis is attempted;
- Pugh Matrix is converted into an HTML table;
- `Reference Links` appears immediately before `Quality Document JSON`;
- `Quality Document JSON` is the final visible section;
- no extra persistent user-facing output files are required.
