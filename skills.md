# Universal Vendor Analysis Skill

## Purpose
Create one exhaustive, evidence-linked vendor-analysis Markdown report for a vendor, public company, or private firm.

The skill can be executed in:

- ChatGPT Online by uploading the zip or pointing to the GitHub repository;
- Google Gemini AI Studio Online by uploading the zip, pasting selected files, or pointing to the repository;
- Claude Online by uploading the zip or pointing to the repository;
- VS Code / terminal using the included Python orchestrator.

## Single Output Rule
Produce only one persistent deliverable:

```text
artifacts/exhaustive_final_report.md
```

In online chat execution, return a downloadable Markdown artifact named:

```text
exhaustive_final_report.md
```

Do not produce separate progress JSON, evidence JSON, Pugh Matrix JSON, quality JSON, SEC JSON, or government-contract JSON files. These can exist only as temporary reasoning or runtime state and must be embedded in the final Markdown report.

## Execution Entry Point for Online Models
When a user uploads this package to ChatGPT, Gemini AI Studio, or Claude, the model must:

1. Read `README.md`.
2. Read this `skills.md` file.
3. Read `agents/agent_registry.md`.
4. Read the relevant playbooks in `playbooks/`.
5. Read guardrails in `guardrails/`.
6. Ask for the vendor name only if the user did not provide it.
7. Execute all required sub-agent sections.
8. Use browsing/search if available.
9. Produce one final Markdown report.

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
The skill must trigger each major report section through a sub-agent. The orchestrator can run these sequentially or in parallel depending on the host model.

Required agents are defined in `agents/agent_registry.md` and include:

- identity and SEC resolution;
- market position;
- business model;
- products and services;
- customer and supplier intelligence;
- government contracts and public-sector signals;
- SEC filing scan;
- future actions;
- architecture and technology;
- security and compliance;
- AI / ML / GenAI;
- competitive landscape;
- Pugh Matrix;
- quality evaluation.

## Report Quality Requirements

Each section must be elaborated, not summarized. The final report must include:

- detailed products and services;
- key customers and customer segments;
- key suppliers, cloud providers, ecosystem dependencies, and partners;
- recent government contracts, agency awards, FedRAMP/public-sector marketplace status, or explicit `Not found in public sources reviewed`;
- SEC filing scan in bulleted format for public companies;
- future actions and forward-looking indicators;
- Pugh Matrix rendered as a Markdown table;
- Quality Document JSON as the final section.

## Evidence Requirements
Every factual claim must include a web reference URL in the same paragraph, bullet, or table row.

Preferred evidence order:

1. SEC filings, official annual reports, and investor relations pages.
2. Official company website, product pages, trust/security/privacy pages, and customer stories.
3. Government procurement portals, FedRAMP marketplace, agency award notices, and marketplace listings.
4. Reputable analyst, financial, market-research, and news sources.

Do not invent data. Use `Not found in public sources reviewed` when evidence is unavailable.

## Local Provider Support
The Python orchestrator supports:

| Provider | Provider ID | API key |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic Claude | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Perplexity | `perplexity` | `PERPLEXITY_API_KEY` |
| Offline scaffold | `offline` | none |

## Online Provider Support
For ChatGPT, Gemini AI Studio, and Claude Online, the zip or GitHub repo acts as an instruction package. The online model does not need to run the Python script. It should read the package files, use its available browsing/search tools, execute the sub-agent playbooks conceptually, and return `exhaustive_final_report.md`.

## Completion Definition
A run is complete only when:

- the final Markdown report exists;
- every required section is present;
- factual claims include URLs or explicit not-found markers;
- Pugh Matrix is rendered as a Markdown table;
- Quality Document JSON is the last section;
- no extra persistent output files are required.
