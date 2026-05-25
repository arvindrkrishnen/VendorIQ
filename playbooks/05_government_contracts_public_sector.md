# Playbook 05: Government Contracts and Public-Sector Signals

Agent: government_contracts_agent. Search government award databases, agency pages, FedRAMP, StateRAMP, procurement vehicles, marketplaces, grants, public-sector customer stories, government cloud marketplaces, and vendor public-sector pages. Distinguish direct awards from marketplace availability, partner-led resale, and general public-sector marketing.

Required tables: Government Awards Table, Public-Sector Signal Table, Marketplace / Procurement Vehicle Table.

## Output Format

Return Markdown only. Do not produce HTML, CSS, JavaScript, final files, or standalone JSON.

## Minimum Depth

In exhaustive mode, this playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. If evidence is unavailable, explain what was searched, what was not found, and what due-diligence questions remain.

## Guardrails

Do not invent facts. Include raw URLs while drafting; the orchestrator will convert them to numbered references. Use `Not found in public sources reviewed` when evidence is unavailable.
