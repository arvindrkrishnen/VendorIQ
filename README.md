# Universal Vendor Analysis Skill

**Name:** `universal-vendor-analysis`  
**Product name:** VendorIQ  
**Author:** Arvind Radhakrishnen  
**LinkedIn:** https://www.linkedin.com/in/arvindradhakrishnen/

VendorIQ is a reusable AI skill that generates evidence-backed vendor strategy and technology due-diligence intelligence for any target company. It researches and organizes a vendor’s identity, business model, product portfolio, product-level technology architecture, AI/GenAI capabilities, customer segments, partner ecosystem, public-sector signals, security and ESG posture, risks, competitors, strengths, gaps, financial metrics, leadership credentials, product moat, and a weighted Pugh Matrix.

Architecture is given here: https://github.com/arvindrkrishnen/VendorIQ/blob/main/vendor_IQ_Architecture.png

## Output Flow

VendorIQ follows a two-step output flow:

1. Generate the full report content as Markdown.
2. Convert the generated Markdown report into one self-contained interactive HTML file.

The final user-facing deliverable is:

```text
artifacts/exhaustive_final_report.html
```

When triggered directly from ChatGPT, Gemini AI Studio, Claude, or another online model, the model should return one downloadable self-contained HTML artifact named:

```text
exhaustive_final_report.html
```

The Markdown report is an intermediate representation used to assemble and validate the content. The final deliverable must be HTML.



## What the Skill Does

VendorIQ follows a multi-agent orchestration pattern. An orchestrator decomposes the vendor-analysis assignment into section-level work, delegates each section to a specialized sub-agent, validates evidence and completeness through guardrails, assembles a complete Markdown report, and then converts that Markdown into a final interactive HTML report.

The report supports:
- annual-report-led public-company analysis;
- business model and revenue model analysis;
- leadership credentials;
- public-company financial metrics where available;
- product-by-product technology due diligence;
- product-by-product architecture analysis;
- product moat and defensibility analysis;
- product-level competitive analysis;
- product-level Pugh Matrix;
- linked references;
- Quality Document JSON as the final visible section.

<img width="1247" height="647" alt="image" src="https://github.com/user-attachments/assets/791b8505-95cb-469d-966f-971248e66281" />

## Output Files

### Intermediate Markdown

The system may generate Markdown internally as an intermediate report representation:

```text
exhaustive_final_report.md
```

or, in local execution:

```text
artifacts/exhaustive_final_report.md
```

This Markdown file is not the final user-facing artifact unless the user explicitly requests Markdown.

### Final HTML

The final deliverable must be:

```text
exhaustive_final_report.html
```

or, in local execution:

```text
artifacts/exhaustive_final_report.html
```

The HTML report must be self-contained:
- all CSS embedded inside the HTML file;
- all JavaScript embedded inside the HTML file;
- no external CSS frameworks;
- no external JavaScript libraries;
- no remote fonts;
- no CDN links;
- no dependency on external assets.

## Interactive HTML Requirements

The converted HTML report should include:
- sticky header;
- clickable table of contents;
- section search/filter;
- expand-all and collapse-all controls;
- collapsible major sections;
- sortable HTML tables;
- due-diligence cards;
- product-level matrices;
- clickable citations;
- reference backlinks;
- print-friendly CSS.

## Two Ways to Use VendorIQ

### Option 1 — Prompt Directly using the GitHub Repository

Use this option when you want ChatGPT, Google Gemini AI Studio, Claude, or another capable AI assistant to execute VendorIQ directly from the public GitHub repository.

#### Recommended Prompt

```text
Execute the skill from here https://github.com/arvindrkrishnen/VendorIQ for Microsoft.
Generate the full report as Markdown first, then convert it into one self-contained interactive HTML file named exhaustive_final_report.html.
```

#### Expanded Prompt Template

```text
Use this GitHub repository as the VendorIQ skill package:
https://github.com/arvindrkrishnen/VendorIQ

Read README.md, SKILL.md, skills.md, guardrails/, agents/, playbooks/, and templates/.
Execute the Universal Vendor Analysis Skill for vendor: <VENDOR NAME>.
Optional ticker: <TICKER>
Optional website: <WEBSITE>

Follow the package rules:
- Use the agents and playbooks as the execution plan.
- Use web browsing/search if available.
- Generate the full report content as Markdown first.
- Every factual claim in the Markdown report must include a numbered citation such as [1], [2], or [3].
- Every numbered citation must resolve to a source URL in the Reference Links section.
- Do not invent customers, suppliers, government contracts, certifications, SEC details, product names, APIs, architecture details, financial metrics, leadership credentials, or analyst commentary.
- After the Markdown report is complete, convert the Markdown into one self-contained interactive HTML artifact named exhaustive_final_report.html.
- Embed the Pugh Matrix and all due-diligence matrices as sortable HTML tables.
- Put Reference Links immediately before Quality Document JSON.
- Make Quality Document JSON the final visible section in the HTML report.
```

### Option 2 — Clone and Configure the GitHub Repository

Use this option when you want to clone the VendorIQ repository and run the skill from a local development environment such as VS Code, Claude Code, Cursor, GitHub Copilot Chat, or another coding assistant.

```bash
git clone https://github.com/arvindrkrishnen/VendorIQ.git
cd VendorIQ
pip install -r requirements.txt
cp .env.example .env
```

Populate the API key for the provider you want to use:

```bash
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"
GEMINI_API_KEY="your-gemini-key"
GOOGLE_API_KEY="your-google-key-if-needed"
PERPLEXITY_API_KEY="your-perplexity-key"
```

Run the orchestrator so it generates Markdown first and then converts it to HTML:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --website https://www.rubrik.com \
  --provider perplexity \
  --model sonar-pro \
  --depth exhaustive \
  --output artifacts/exhaustive_final_report.html
```

The final output is:

```text
artifacts/exhaustive_final_report.html
```

## Supported Execution Modes

| Usage path | Mode | How users run it | API keys needed by user | Final Output |
|---|---|---|---:|---|
| Prompt directly from GitHub repository | ChatGPT Online | Provide the repo URL and prompt ChatGPT to execute the skill | No local key required; depends on ChatGPT tools | `exhaustive_final_report.html` |
| Prompt directly from GitHub repository | Gemini AI Studio Online | Provide the repo URL or paste selected files | No local key required inside the repo; AI Studio access required | `exhaustive_final_report.html` |
| Prompt directly from GitHub repository | Claude Online | Provide or connect the GitHub repository | No local key required; depends on Claude tools | `exhaustive_final_report.html` |
| Clone and configure GitHub repository | VS Code / local OpenAI | Clone the repo and run Python script with `--provider openai` | `OPENAI_API_KEY` | `artifacts/exhaustive_final_report.html` |
| Clone and configure GitHub repository | VS Code / local Anthropic | Clone the repo and run Python script with `--provider anthropic` | `ANTHROPIC_API_KEY` | `artifacts/exhaustive_final_report.html` |
| Clone and configure GitHub repository | VS Code / local Gemini | Clone the repo and run Python script with `--provider gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `artifacts/exhaustive_final_report.html` |
| Clone and configure GitHub repository | VS Code / local Perplexity | Clone the repo and run Python script with `--provider perplexity` | `PERPLEXITY_API_KEY` | `artifacts/exhaustive_final_report.html` |
| Clone and configure GitHub repository | Offline scaffold | Clone the repo and run Python script with `--provider offline` | None | Scaffold HTML report |

## Multi-Agent Execution Flow

1. **Orchestrator reads the vendor request.**
2. **Identity agent resolves the exact company, ticker, website, SEC CIK, and filing sources.**
3. **Company, financial, and leadership agents build annual-report-led company context.**
4. **Product and architecture agents perform product-by-product technology due diligence.**
5. **Product moat agent evaluates defensibility for each major product.**
6. **Competitive agent creates product-level competitive analysis and Pugh Matrix.**
7. **Quality evaluation agent validates evidence authenticity, completeness, unsupported claims, reference links, and single-output compliance.**
8. **Final report assembly generates the complete Markdown report.**
9. **Markdown-to-HTML conversion creates `exhaustive_final_report.html`.**

## Required Final Report Sections

The Markdown report and final HTML report must include:

1. Title Page and Evidence Methodology
2. Vendor Identity, Ticker, Website, Headquarters, Public/Private Status
3. Executive Thesis with Evidence-Linked Conclusions
4. Company Overview and Market Position
5. Business Model and Revenue Model
6. Detailed Product, Service, Platform, and Technical Capability Catalog
7. Product-to-Capability Map
8. Product-by-Product Technology and Architecture Due Diligence
9. Information Architecture Assessment
10. Application Architecture Assessment
11. Security Architecture Assessment
12. Technology Standards and Interoperability Assessment
13. Resiliency, Disaster Recovery, and Stability Assessment
14. AI, Machine Learning, Automation, and GenAI Capabilities by Product
15. Product Moat, Differentiation, and Defensibility Analysis
16. Key Customers and Customer Segments
17. Key Suppliers, Cloud Providers, Technology Partners, Channel Partners, and Ecosystem Dependencies
18. Government Contracts, Public-Sector Awards, FedRAMP Status, Marketplaces, and Procurement Vehicles
19. Major Milestones, Acquisitions, Partnerships, and Recognitions
20. Case Studies and Measurable Client Benefits
21. ESG, Sustainability, Privacy, and Responsible-Business Posture
22. Analyst Reviews, Market Sentiment, and External Perception
23. Cybersecurity Incidents, Vulnerabilities, Regulatory Issues, and Litigation Signals
24. SEC Filing Scan in Bulleted Format
25. Future Actions and Forward-Looking Indicators
26. Competitive Landscape, Product Moat, and Pugh Matrix
27. Strengths, Gaps, Risks, and Differentiation
28. Reference Links
29. Quality Document JSON

## Evidence and Authenticity Requirements

Every factual claim should include a numbered citation such as `[1]`, `[2]`, or `[3]`. Each numbered citation must resolve to a source URL in the `Reference Links` section.

Preferred source classes:
- SEC filings and official annual reports;
- investor relations pages;
- official vendor product pages;
- product documentation;
- API/developer documentation;
- architecture documentation;
- official trust, security, privacy, compliance, and sustainability pages;
- official customer stories and case studies;
- government procurement databases and agency award notices;
- FedRAMP marketplace and public-sector marketplaces;
- official press releases;
- reputable financial, analyst, and market-research references.

Rules:
- Do not invent customers, suppliers, certifications, contracts, product names, APIs, architecture details, leadership credentials, or financial metrics.
- Do not infer government contracts from vague public-sector marketing language.
- Mark unavailable information as `Not found in public sources reviewed`.
- Treat SEC filings and official company disclosures as higher-priority evidence than secondary commentary.
- Include filing date, fiscal period, and form type when citing SEC filings.

## Best Practices

1. Use web-enabled execution for current analysis.
2. Use SEC filings as the anchor source for public companies.
3. Use official product pages, product docs, developer docs, trust pages, and architecture docs for product-level due diligence.
4. Separate named customers from inferred customer segments.
5. Separate direct government awards from marketplace availability or partner-led resale.
6. Put unsupported claims in the report as `Not found in public sources reviewed` rather than guessing.
7. Generate Markdown first.
8. Convert the completed Markdown to `exhaustive_final_report.html`.
9. Keep the HTML file as the final user-facing artifact.

## Troubleshooting

### ChatGPT, Gemini, or Claude says it cannot execute code

Use the direct GitHub-repository prompt. Tell the model:

```text
Do not run code; read the GitHub repository files as instructions, generate the full Markdown report first, then convert that Markdown into one self-contained interactive HTML report using your available browsing/search capability.
```

### The report lacks current web URLs

Ask the online model to enable browsing/search, or use local Perplexity mode.

### The output creates extra files

The package rule is one final user-facing output only. Ask the model to consolidate all content into `exhaustive_final_report.html` and delete or ignore intermediate artifacts.

### Gemini AI Studio has token limits

Start with `SKILL.md`, `skills.md`, `agents/agent_registry.md`, `playbooks/01_online_chat_execution.md`, `playbooks/08_final_report_assembly.md`, `guardrails/README.md`, and the vendor name. Then add agent/playbook files section by section if needed.

### Claude produces a narrative but not a file

Ask Claude to generate the report as Markdown first, then return the converted result as a downloadable self-contained HTML artifact named `exhaustive_final_report.html`.
