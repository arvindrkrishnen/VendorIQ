# Playbook 03: Vendor Identity, SEC Resolution, Market Position, Business Model, Financials, and Leadership

Agents: identity_sec_resolution_agent, market_position_agent, business_model_agent, financial_metrics_agent, leadership_credentials_agent. Resolve legal entity, public/private status, ticker, exchange, CIK, headquarters, website, investor relations pages, latest annual report, 10-Q, proxy statement, investor presentation, business model, revenue model, leadership credentials, and public-company financial metrics.

Required tables: Authoritative Source Basis, SEC Filing Source Table, Leadership Credentials Table, Financial Metrics Table. Financial metrics must attempt EPS, P/E, PEG, free cash flow, cash, debt, debt as percentage of cash, revenue growth, and margin signals.

## Output Format

Return Markdown only. Do not produce HTML, CSS, JavaScript, final files, or standalone JSON.

## Minimum Depth

In exhaustive mode, this playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. If evidence is unavailable, explain what was searched, what was not found, and what due-diligence questions remain.

## Guardrails

Do not invent facts. Include raw URLs while drafting; the orchestrator will convert them to numbered references. Use `Not found in public sources reviewed` when evidence is unavailable.
