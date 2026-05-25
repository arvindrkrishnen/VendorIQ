# Playbook 08: Final Markdown Assembly and HTML Conversion

Agents: reference_normalization_agent and quality_evaluation_agent. Assemble all section-level Markdown into `artifacts/exhaustive_final_report.md`. Preserve template section order, ensure every required section and table is present, normalize raw URLs into numbered references, place Reference Links immediately before Quality Document JSON, and make Quality Document JSON the final Markdown section.

Before HTML conversion, validate sections, word counts, tables, factual claims, citations, product architecture, product moat, Pugh Matrix, SEC scan, leadership credentials, and financial metrics. If a critical gate fails, do not convert to HTML. Only after Markdown passes validation, convert to `artifacts/exhaustive_final_report.html` with embedded CSS and JavaScript.

## Output Format

Return Markdown only. Do not produce HTML, CSS, JavaScript, final files, or standalone JSON.

## Minimum Depth

In exhaustive mode, this playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. If evidence is unavailable, explain what was searched, what was not found, and what due-diligence questions remain.

## Guardrails

Do not invent facts. Include raw URLs while drafting; the orchestrator will convert them to numbered references. Use `Not found in public sources reviewed` when evidence is unavailable.
