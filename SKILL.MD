# VendorIQ Skill Execution Instructions

You are executing the VendorIQ Universal Vendor Analysis Skill. 

Author: Arvind Radhakrishnen

## Purpose

Generate one exhaustive, evidence-backed vendor-analysis Markdown report for a target company, vendor, or public/private firm.

## Required Input

Minimum:
- Vendor name

Optional:
- Ticker
- Website
- SEC CIK
- Competitor list
- Geography
- Depth: `standard` or `exhaustive`

## Execution Order for ChatGPT, Claude, Gemini, and Other Online Agents

1. Read this file first.
2. Read `README.md`.
3. Read `skills.md`.
4. Read `agents/agent_registry.md`.
5. Read `guardrails/`.
6. Read `playbooks/`.
7. Use `templates/exhaustive_final_report_template.md`.
8. Use web browsing/search/grounding where available.
9. Produce one final Markdown artifact named `exhaustive_final_report.md`.

## Execution Order for Local CLI

1. Clone the repository.
2. Install dependencies.
3. Configure `.env`.
4. Run `src/universal_vendor_orchestrator.py`.

Example:

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Coherent Corp." \
  --ticker COHR \
  --website https://www.coherent.com \
  --provider perplexity \
  --model sonar-pro \
  --depth exhaustive
