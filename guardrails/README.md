# Guardrails

Guardrails apply to online and local execution.

## Required Gates
- Single-output gate: produce only `exhaustive_final_report.md`.
- Evidence authenticity gate: every factual claim has a URL or not-found marker.
- Section completeness gate: no required section is missing.
- SEC gate: public companies include SEC filing scan.
- Customer/supplier gate: named customers and suppliers are evidence-linked or marked not found.
- Government-contract gate: direct contracts are cited, otherwise marked not found.
- Pugh Matrix gate: matrix is a Markdown table.
- Quality gate: final section is `Quality Document JSON`.
