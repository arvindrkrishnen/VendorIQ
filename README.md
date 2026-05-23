Name: universal-vendor-analysis
Summary: Exhaustive, evidence-linked vendor and public-company analysis using multi-agent orchestration across OpenAI, Anthropic Claude, Google Gemini, and Perplexity.
description Produces a single Markdown artifact, artifacts/exhaustive_final_report.md, containing detailed vendor analysis, SEC filing review, products and services, customers, suppliers, government contracts, competitive Pugh Matrix, evidence appendix, and final quality evaluation JSON.

Author: Arvind Radhakrishnen
LinkedIn: https://www.linkedin.com/in/arvindradhakrishnen/


# Universal Vendor Analysis Skill

This repository contains a **universal multi-LLM vendor analysis skill** designed for VS Code, local terminal execution, and agentic development workflows. It generates one exhaustive Markdown report for a vendor, public company, or private technology firm.

The skill follows a multi-agent orchestration pattern: an orchestrator decomposes the vendor-analysis assignment into section-level tasks, delegates each task to a specialized sub-agent, validates evidence and completeness, and then assembles a single final report.

The package intentionally produces only one persistent user-facing output:

```text
artifacts/exhaustive_final_report.md
```

All intermediate progress, sub-agent drafts, evidence notes, Pugh Matrix JSON, SEC findings, and quality ratings are either held in memory or temporary runtime state and then consolidated into the final Markdown report.

## When to Use This Skill

Use this skill when you need a rigorous, source-backed analysis of a company or vendor, especially when the work must include public evidence, SEC filings, product/service details, customers, suppliers, government contracts, competitive positioning, and architecture or security assessment.

Typical use cases:

- preparing a vendor due-diligence report;
- evaluating a technology supplier for enterprise architecture review;
- comparing competitors for procurement or sourcing decisions;
- scanning SEC filings for risks, strategy, business model, revenue signals, customers, suppliers, and future actions;
- researching government contracts, public-sector posture, FedRAMP status, agency customers, and procurement vehicles;
- building a board-level or executive-level vendor intelligence report;
- producing a repeatable evidence-linked market-research artifact for a repository.

## What This Skill Does

1. **Identifies the vendor**  
   Resolves company name, ticker, website, corporate headquarters, public/private status, and SEC filing availability.

2. **Runs section-level sub-agents**  
   Delegates company overview, market positioning, products, customers, suppliers, government contracts, SEC filings, future actions, architecture, AI capabilities, competitors, and quality evaluation to separate agents.

3. **Requires evidence-linked claims**  
   Every factual claim should be supported by a web reference URL. Unsupported content is marked as not found instead of being invented.

4. **Builds an exhaustive final report**  
   Produces detailed section content rather than brief summaries.

5. **Embeds competitive analysis**  
   Generates an internal Pugh Matrix JSON and renders it as a Markdown table inside the final report.

6. **Appends quality evaluation**  
   Adds the Quality Document JSON as the final section of `exhaustive_final_report.md`.

7. **Enforces single-output behavior**  
   Keeps the repository clean by producing only one persistent report file.

## Repository Layout

```text
.
├── README.md
├── CONTRIBUTIONS.md
├── skills.md
├── playbooks.md
├── agents.md
├── guardrails.md
├── requirements.txt
├── .env.example
├── .gitignore
├── .vscode/
│   └── tasks.json
├── src/
│   └── universal_vendor_orchestrator.py
└── artifacts/
    └── exhaustive_final_report.md   # generated output
```

## Architecture

```text
User / VS Code Task / CLI
        |
        v
universal_vendor_orchestrator.py
        |
        +-- Runtime Configuration
        |      +-- vendor name
        |      +-- ticker
        |      +-- website
        |      +-- provider
        |      +-- model
        |      +-- competitors
        |      +-- depth
        |
        +-- Provider Adapter
        |      +-- OpenAI
        |      +-- Anthropic Claude
        |      +-- Google Gemini
        |      +-- Perplexity
        |      +-- Offline scaffold mode
        |
        +-- Orchestrator Agent
        |      |
        |      +-- Identity and SEC Agent
        |      +-- Market Position Agent
        |      +-- Business Model Agent
        |      +-- Product and Services Agent
        |      +-- Customer Intelligence Agent
        |      +-- Supplier Ecosystem Agent
        |      +-- Government Contracts Agent
        |      +-- SEC Filing Scan Agent
        |      +-- Future Actions Agent
        |      +-- Technology Architecture Agent
        |      +-- Security and Compliance Agent
        |      +-- AI / ML / GenAI Agent
        |      +-- Competitive Landscape Agent
        |      +-- Pugh Matrix Agent
        |      +-- Quality Evaluation Agent
        |
        +-- Guardrails
        |      +-- evidence authenticity gate
        |      +-- exhaustive-section gate
        |      +-- single-output gate
        |      +-- cleanup gate
        |      +-- final-report gate
        |
        v
artifacts/exhaustive_final_report.md
```

## Execution Flow

### 1. Configure the run

The user provides a vendor name and optional metadata such as ticker, official website, competitor list, model provider, and model name.

Example:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --website https://www.rubrik.com \
  --provider perplexity \
  --model sonar-pro \
  --depth exhaustive
```

### 2. Initialize provider adapter

The orchestrator selects the configured model provider:

- OpenAI for general reasoning and structured report generation;
- Anthropic Claude for long-context synthesis and narrative analysis;
- Google Gemini for multimodal or Google ecosystem workflows;
- Perplexity for web-grounded research and current-source discovery;
- offline mode for template validation when API keys are unavailable.

### 3. Create sub-agent tasks

The orchestrator converts the vendor-analysis objective into explicit tasks. Each task includes:

- section name;
- scope;
- required evidence types;
- expected output format;
- passing criteria;
- unsupported-claim handling rule.

### 4. Execute sub-agents

Each sub-agent produces detailed Markdown-ready content. The orchestrator may run agents sequentially or in parallel depending on the implementation and provider constraints.

### 5. Validate evidence and authenticity

The guardrails require each section to contain evidence links. If a statement cannot be verified, the statement must be removed, downgraded, or marked as `Not found in public sources`.

### 6. Assemble final Markdown

The final report contains all sections, the Pugh Matrix table, evidence appendix, and Quality Document JSON as the last section.

### 7. Clean temporary state

Temporary runtime files are removed. Only `artifacts/exhaustive_final_report.md` should remain as the persistent output.

## Supported LLM Providers

The package supports multiple providers through environment variables and CLI arguments.

| Provider | Provider ID | API key variable | Typical model examples | Recommended use |
|---|---|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-4.1`, `gpt-4.1-mini`, `gpt-5.5` | Structured synthesis, report generation, reasoning |
| Anthropic Claude | `anthropic` | `ANTHROPIC_API_KEY` | `claude-3-5-sonnet-latest`, `claude-3-7-sonnet-latest` | Long-context narrative synthesis |
| Google Gemini | `gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `gemini-2.5-pro`, `gemini-2.5-flash` | Google ecosystem, large-context workflows |
| Perplexity | `perplexity` | `PERPLEXITY_API_KEY` | `sonar-pro`, `sonar` | Current web-grounded evidence discovery |
| Offline scaffold | `offline` | none | `offline` | Local template validation without API calls |

## Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Populate the provider keys you plan to use:

```bash
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"
GEMINI_API_KEY="your-gemini-key"
GOOGLE_API_KEY="your-google-key-if-needed"
PERPLEXITY_API_KEY="your-perplexity-key"
```

Do not commit `.env` to source control.

## Provider-Specific Execution Examples

### OpenAI

```bash
export OPENAI_API_KEY="your-openai-key"
python src/universal_vendor_orchestrator.py \
  --vendor "Microsoft Corporation" \
  --ticker MSFT \
  --provider openai \
  --model gpt-4.1
```

### Anthropic Claude

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --provider anthropic \
  --model claude-3-5-sonnet-latest
```

### Google Gemini

```bash
export GEMINI_API_KEY="your-gemini-key"
python src/universal_vendor_orchestrator.py \
  --vendor "Lumentum Holdings Inc." \
  --ticker LITE \
  --provider gemini \
  --model gemini-2.5-pro
```

### Perplexity

```bash
export PERPLEXITY_API_KEY="your-perplexity-key"
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --provider perplexity \
  --model sonar-pro
```

### Offline scaffold mode

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --provider offline
```

Offline mode validates report assembly and output policy but does not perform real model-backed research.

## VS Code Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Open the Command Palette:

```text
Tasks: Run Task
```

Choose one of the configured tasks:

- `Run Vendor Analysis - OpenAI`
- `Run Vendor Analysis - Anthropic`
- `Run Vendor Analysis - Gemini`
- `Run Vendor Analysis - Perplexity`
- `Run Vendor Analysis - Offline Scaffold`

Edit `.vscode/tasks.json` to change vendor, ticker, website, provider, model, competitors, or output path.

## Required Final Report Sections

The generated Markdown report should include the following sections:

1. Title page and evidence methodology
2. Vendor identity, ticker, website, headquarters, public/private status
3. Executive thesis with evidence-linked conclusions
4. Company overview and market position
5. Business model and revenue model
6. Detailed products and services catalog
7. Product-to-capability map
8. Technology architecture and platform capabilities
9. Information architecture assessment
10. Application architecture assessment
11. Security architecture assessment
12. Technology standards and interoperability assessment
13. Resiliency, disaster recovery, and stability assessment
14. AI, machine learning, automation, and GenAI capabilities
15. Key customers and customer segments
16. Key suppliers, cloud providers, technology partners, channel partners, and ecosystem dependencies
17. Government contracts, public-sector awards, FedRAMP status, marketplaces, and procurement vehicles
18. Major milestones, acquisitions, partnerships, and recognitions
19. Case studies and measurable client benefits
20. ESG, sustainability, privacy, and responsible-business posture
21. Analyst reviews, market sentiment, and external perception
22. Cybersecurity incidents, vulnerabilities, regulatory issues, and litigation signals
23. SEC filing scan in bulleted format
24. Future actions and forward-looking indicators
25. Competitive landscape and competitor identification
26. Pugh Matrix table
27. Strengths, gaps, risks, and differentiation
28. Evidence appendix with URLs grouped by section
29. Quality Document JSON as the final section

## Evidence and Authenticity Requirements

Every factual claim should include a source URL. Preferred source classes:

- SEC filings and official annual reports;
- investor relations pages;
- official vendor product pages;
- official trust, security, privacy, compliance, and sustainability pages;
- official customer stories and case studies;
- government procurement databases and agency award notices;
- FedRAMP marketplace and public-sector marketplaces;
- official press releases;
- reputable financial, analyst, and market-research references.

Rules:

- Do not invent customers, suppliers, certifications, or contracts.
- Do not infer government contracts from vague public-sector marketing language.
- Mark unavailable information as `Not found in public sources`.
- Treat SEC filings and official company disclosures as higher-priority evidence than secondary commentary.
- Include filing date, fiscal period, and form type when citing SEC filings.

## Pugh Matrix Requirements

The Pugh Matrix may be generated internally as JSON, but the final report must render it as a Markdown table.

Required criteria:

- Value Chain Alignment
- Technical Architecture
- AI / Generative AI Capabilities
- Mobile App Integration
- Customer Support
- API Readiness
- Cloud Native Readiness
- Data Strategy
- Security Certifications
- Geographic Presence
- Key Partnerships
- Key Differentiators
- Government / Public-Sector Readiness
- Customer and Supplier Ecosystem Strength
- Future Action Readiness

## Quality Document Requirements

The last section of the final report must be a fenced JSON block titled `Quality Document JSON`.

It should score:

- evidence authenticity;
- section exhaustiveness;
- customer/supplier coverage;
- SEC filing coverage;
- government-contract coverage;
- future-actions coverage;
- Pugh Matrix completeness;
- unsupported claim count;
- single-output compliance;
- cleanup compliance.

## Guardrails

The guardrails are maintained in `guardrails.md` and cover:

- single-output policy;
- evidence authenticity gate;
- exhaustive-section gate;
- SEC filing gate;
- government contracts gate;
- customer and supplier gate;
- future-actions gate;
- Pugh Matrix gate;
- Quality Document gate;
- cleanup and clean-state gate.

## Common Tasks

### Analyze a public company

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Microsoft Corporation" \
  --ticker MSFT \
  --provider perplexity \
  --model sonar-pro
```

### Analyze a private vendor with website only

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Example Vendor" \
  --website https://www.example.com \
  --provider perplexity \
  --model sonar-pro
```

### Add explicit competitors

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --competitors "Commvault,Veeam,Cohesity,Dell Technologies" \
  --provider openai \
  --model gpt-4.1
```

## Best Practices

1. **Use Perplexity for source discovery**  
   It is usually the best provider choice when the run depends on current web references.

2. **Use SEC filings for public companies**  
   For public companies, SEC filings should anchor revenue, risk, customer concentration, supplier dependency, liquidity, segment, and forward-looking analysis.

3. **Use official sources first**  
   Prefer official product pages, investor relations, trust centers, customer stories, and filings over third-party summaries.

4. **Separate facts from interpretation**  
   Interpretations should be labeled as analysis and tied back to evidence.

5. **Do not overproduce artifacts**  
   Keep the output clean. The final report is the only persistent deliverable.

6. **Record uncertainty**  
   If a claim is not verifiable, say so directly.

7. **Tune the model to the task**  
   Use a web-grounded provider for discovery, then a strong reasoning model for final synthesis if your workflow supports chaining.

## Extension Points

Contributors can extend the package by adding:

- new sub-agent definitions in `agents.md`;
- new section playbooks in `playbooks.md`;
- stricter validation rules in `guardrails.md`;
- provider adapters in `src/universal_vendor_orchestrator.py`;
- VS Code tasks in `.vscode/tasks.json`;
- report templates in the final-report assembler.

## Troubleshooting

### The report contains placeholders

Likely cause: offline mode was used or no API key was configured. Configure a provider key and rerun.

### The report lacks current web URLs

Use `--provider perplexity` or ensure the selected model has access to a web-search tool through your runtime.

### The report generated extra files

Check cleanup logic and the single-output gate in `guardrails.md`. Only `artifacts/exhaustive_final_report.md` should remain.

### SEC section is weak

Provide the ticker and, if known, the SEC CIK:

```bash
--ticker RBRK --sec-cik 0001943896
```

### Government-contract section is weak

Add search hints in the vendor prompt or specify the vendor’s public-sector brand, reseller, or marketplace names.

## Related Use Cases

- vendor due diligence;
- market and competitor research;
- procurement analysis;
- third-party risk management;
- architecture review board preparation;
- SEC filing analysis;
- government-contract intelligence;
- investment-research support;
- partner and supplier ecosystem mapping.
