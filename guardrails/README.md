# Guardrails

## Phase 1 Markdown Gates

- Markdown-generation gate: all agents and playbooks produce Markdown only.
- No-HTML-from-agents gate: agents must not produce HTML, CSS, JavaScript, or final artifacts.
- Section completeness gate: no required section from `templates/exhaustive_final_report_template.md` is missing.
- Minimum-depth gate: in exhaustive mode, each playbook must contribute at least 500 words of narrative analysis, excluding tables, unless public evidence is unavailable.
- Evidence authenticity gate: every factual claim has a URL, numbered citation, or not-found marker.
- SEC gate: public companies include SEC filing scan.
- Financial metrics gate: public companies attempt EPS, P/E, PEG, free cash flow, cash, total debt, debt as percentage of cash, revenue growth, and margin signals.
- Product architecture gate: product-by-product architecture analysis is present or marked not found.
- Pugh Matrix gate: product-level Pugh Matrix is present as a Markdown table.
- Quality gate: final Markdown section is `Quality Document JSON`.

## Phase 2 HTML Gates

- HTML conversion must happen only after Markdown quality validation passes.
- Final HTML must be self-contained.
- HTML must preserve every Markdown section, table, citation, Reference Link, and Quality Document JSON.
