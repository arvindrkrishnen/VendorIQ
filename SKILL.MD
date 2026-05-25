# VendorIQ Skill Execution Instructions

You are executing the VendorIQ Universal Vendor Analysis Skill.

Author: Arvind Radhakrishnen

## Purpose

Generate one exhaustive, evidence-backed vendor-analysis report for a target company, vendor, or public/private firm.

The required output flow is:

1. Generate the complete report as Markdown.
2. Convert the completed Markdown report into one self-contained interactive HTML file.

The final user-facing artifact must be:

```text
exhaustive_final_report.html
```

For local execution, the final artifact must be:

```text
artifacts/exhaustive_final_report.html
```

The Markdown report is an intermediate representation used for report assembly, validation, and conversion. Do not treat Markdown as the final deliverable unless the user explicitly requests Markdown.

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
7. Use `templates/exhaustive_final_report_template.md` as the report-section structure.
8. Use web browsing/search/grounding where available.
9. Execute the sub-agent workflow.
10. Generate the full report as Markdown.
11. Validate that the Markdown includes all required sections, numbered citations, Reference Links, and Quality Document JSON.
12. Convert the completed Markdown into one self-contained interactive HTML artifact named `exhaustive_final_report.html`.

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
  --output artifacts/exhaustive_final_report.html
```

## Markdown Assembly Requirements

The Markdown report must include:
- all required report sections;
- numbered citations such as `[1]`, `[2]`, and `[3]`;
- `Reference Links`;
- `Quality Document JSON` as the final Markdown section before conversion;
- Pugh Matrix and due-diligence matrices as Markdown tables before conversion.

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
- table of contents;
- search/filter box;
- expand-all and collapse-all controls;
- collapsible major sections;
- sortable tables;
- product-level due-diligence matrices;
- product architecture matrices;
- product moat matrices;
- competitive Pugh Matrix;
- clickable citations;
- Reference Links section;
- Quality Document JSON as the final visible section;
- print-friendly CSS.

## Evidence Rules

Every factual claim must include a numbered citation such as `[1]`, `[2]`, or `[3]`.

Every citation must resolve to a source URL in the `Reference Links` section.

If evidence is unavailable, write:

```text
Not found in public sources reviewed
```

## Agent Output Rule

All agents and sub-agents must return Markdown only. Agents must not produce HTML, CSS, JavaScript, separate JSON artifacts, or files. Each agent returns section-ready Markdown, raw evidence URLs while drafting, required Markdown tables, not-found markers, and quality notes where evidence is weak.

## Minimum Depth Requirements

For exhaustive mode, each playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. Product and architecture playbooks should be substantially longer.


## Final Section Order

The final visible content sections must end in this order:

1. `Reference Links`
2. `Quality Document JSON`

`Quality Document JSON` must be the final visible section in both the Markdown assembly and converted HTML report.
