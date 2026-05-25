# Playbook 06: SEC Filings and Future Actions

Agents: sec_filings_agent and future_actions_agent. Scan latest 10-K, 10-Q, 8-K, DEF 14A, earnings releases, investor presentations, and official roadmap/product launch pages. Extract business model, revenue model, risks, financial metrics, liquidity, customer/supplier concentration, cybersecurity, litigation, R&D, product investments, capital allocation, management priorities, and forward-looking indicators.

Required tables: SEC Filing Scan Table, Risk Factor Matrix, Future Actions Table.

## Output Format

Return Markdown only. Do not produce HTML, CSS, JavaScript, final files, or standalone JSON.

## Minimum Depth

In exhaustive mode, this playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. If evidence is unavailable, explain what was searched, what was not found, and what due-diligence questions remain.

## Guardrails

Do not invent facts. Include raw URLs while drafting; the orchestrator will convert them to numbered references. Use `Not found in public sources reviewed` when evidence is unavailable.
