# Universal Vendor Analysis Skill

## Purpose
This skill produces **one exhaustive Markdown report** for a vendor or public company. The report is generated through a multi-agent orchestration pattern and is designed to run in VS Code using OpenAI, Anthropic Claude, Google Gemini, or Perplexity-compatible models.

The skill prioritizes:
- exhaustive section-level analysis rather than summaries;
- web-reference URLs for every factual claim;
- SEC filing extraction for public companies;
- key customer and supplier intelligence;
- products and services detail;
- government contracts and public-sector awards;
- future actions and forward-looking signals;
- Pugh Matrix competitive analysis rendered as a Markdown table;
- a Quality Document JSON block embedded as the final section of the report;
- only one persistent output file: `artifacts/exhaustive_final_report.md`.

## Single Output Rule
The skill must produce exactly one user-facing artifact:

```text
artifacts/exhaustive_final_report.md
```

All progress state, evidence tracking, quality-gate checks, and temporary sub-agent drafts must be maintained in memory or in a temporary runtime directory and removed before session completion. The final report embeds the quality document as the last section, eliminating separate JSON outputs.

## Supported LLM Providers
The package supports provider selection through environment variables or CLI arguments:

| Provider | Provider ID | Primary key variable | Notes |
|---|---:|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` | Uses OpenAI Responses-style prompt orchestration through a generic adapter. |
| Anthropic Claude | `anthropic` | `ANTHROPIC_API_KEY` | Uses Claude Messages-style prompt orchestration through a generic adapter. |
| Google Gemini | `gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `GOOGLE_API_KEY` may be used where Gemini libraries expect it. |
| Perplexity | `perplexity` | `PERPLEXITY_API_KEY` | Recommended for evidence discovery and current web research. |
| Offline scaffold | `offline` | none | Generates the report structure, instructions, and placeholders for environments without keys. |

## Required Inputs
Minimum input:

```bash
python src/universal_vendor_orchestrator.py --vendor "Rubrik" --ticker RBRK --provider perplexity --model sonar-pro
```

Optional input:

```bash
--website https://www.vendor.com
--output artifacts/exhaustive_final_report.md
--competitors "Competitor A,Competitor B,Competitor C"
--sec-cik 0000000000
--depth exhaustive
```

## Exhaustive Report Sections
The final report must include these sections in order:

1. Title page and evidence methodology
2. Vendor identity, ticker, website, corporate headquarters, reporting status
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
17. Government contracts, public-sector awards, FedRAMP or marketplace eligibility, grants, and procurement vehicles
18. Major milestones, acquisitions, partnerships, and recognitions
19. Case studies and measurable client benefits
20. ESG, sustainability, privacy, and responsible-business posture
21. Analyst reviews, market sentiment, and external perception
22. Cybersecurity incidents, vulnerabilities, regulatory issues, and litigation signals
23. SEC filing scan in bulleted format for all material filing signals
24. Future actions and forward-looking indicators
25. Competitive landscape and competitor identification
26. Pugh Matrix JSON rendered as a Markdown table
27. Strengths, gaps, risks, and differentiation
28. Evidence appendix with URLs grouped by section
29. Quality Document JSON as the final section

## Source and Authenticity Rules
Every factual claim must be linked to a web reference URL. Acceptable sources include:
- SEC filings and investor relations pages;
- vendor official website pages;
- customer case studies;
- government procurement databases and agency award notices;
- FedRAMP marketplace or similar public certification listings;
- security and compliance trust centers;
- recognized analyst and financial data platforms;
- reputable news and press releases.

Unsupported facts must be marked as `Not found in public sources` and must not be converted into inferred claims.

## Sub-Agent Execution Requirement
Each major section must be delegated to a specialized sub-agent. The orchestrator must:
1. create a section task;
2. provide the task with output requirements and passing criteria;
3. require claim-level evidence URLs;
4. validate section quality;
5. retry or downgrade unsupported claims;
6. merge the section into the final Markdown report.

## Completion Definition
The session is complete only when:
- `artifacts/exhaustive_final_report.md` exists;
- no other persistent output artifacts are created;
- each section has evidence-linked content;
- the Pugh Matrix JSON has been transformed into a Markdown table in the report;
- the Quality Document JSON is embedded as the final section;
- the authenticity gate passes;
- temporary runtime files have been removed.

