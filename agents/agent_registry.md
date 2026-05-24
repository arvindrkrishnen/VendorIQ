# Agent Registry

## Execution Principle

The orchestrator owns the final output. Sub-agents produce section-ready Markdown content with evidence URLs. Sub-agents must not create separate persistent artifacts.

During drafting, agents may include raw source URLs. The orchestrator converts raw URLs into numbered references such as `[1]`, `[2]`, and `[3]`, and renders the corresponding source URLs in the final `Reference Links` section.

## Required Agents

| Agent | Responsibility | Primary Output |
|---|---|---|
| `orchestrator_agent` | Coordinates the full run, delegates sections, enforces guardrails, normalizes references, and assembles report | One final Markdown report |
| `identity_sec_resolution_agent` | Resolves legal entity, ticker, website, CIK, latest annual report, latest quarterly report, investor presentation, proxy statement, and official filing sources | Identity and filing section |
| `market_position_agent` | Company overview, history, mission, market position, geography, source-basis table, and annual-report-backed business description | Market position section |
| `business_model_agent` | Revenue model, segment model, GTM, operating drivers, recurring vs. transactional revenue, and annual-report-backed business model | Business model section |
| `financial_metrics_agent` | EPS, P/E, PEG, FCF, cash, debt, debt as % of cash, revenue growth, margin signals, valuation narrative, and liquidity narrative for public companies | Financial metrics and valuation narrative |
| `leadership_credentials_agent` | Leadership extraction from annual report/proxy/company site and credential enrichment from official bios, LinkedIn, or other public sources | Leadership credentials subsection |
| `product_services_agent` | Exhaustive products/services catalog and capability map | Product section |
| `customer_supplier_agent` | Named customers, customer segments, suppliers, cloud providers, partners | Commercial ecosystem section |
| `government_contracts_agent` | Direct awards, agency contracts, FedRAMP, marketplaces, public-sector signals | Government/public-sector section |
| `sec_filings_agent` | 10-K/10-Q/8-K/S-1/proxy scan, risk factors, strategy, customers/suppliers, future actions, leadership, liquidity, and financial metrics | SEC filing scan bullets |
| `future_actions_agent` | Disclosed plans, roadmap, capital allocation, hiring/geography/product expansion | Future actions section |
| `architecture_agent` | Technology, application, information, security, standards, resiliency | Architecture section |
| `ai_ml_genai_agent` | AI/ML/automation/GenAI capabilities and benefits | AI capability section |
| `competitive_pugh_matrix_agent` | Competitors and Pugh Matrix table | Competitive section and table |
| `reference_normalization_agent` | Deduplicates source URLs, assigns numeric references, replaces raw URLs with `[n]`, and renders `Reference Links` | Numbered reference map |
| `quality_evaluation_agent` | Evidence authenticity, numbered-reference completeness, annual-report source coverage, financial-metric completeness, and output compliance | Quality Document JSON |

## Universal Agent Output Contract

Each agent must return:

1. Markdown section content.
2. Raw evidence URLs embedded in the content while drafting, or numbered references if the host environment already supports reference normalization.
3. Any unknowns labeled `Not found in public sources reviewed`.
4. No separate files.

## Public-Company Source Contract

When the target company is public, agents must prioritize:

1. Annual report / 10-K / 20-F / 40-F.
2. Latest 10-Q or quarterly report.
3. Investor presentation / investor day material.
4. Proxy statement / DEF 14A for leadership and compensation context.
5. Official website and investor relations pages.
6. Bloomberg, FactSet, Yahoo Finance, Investing.com, and reputable analyst/financial sources.

## Financial Metrics Contract

For public companies, the financial metrics agent must attempt to include:

- EPS
- P/E
- PEG
- Free cash flow
- Cash and cash equivalents
- Total debt
- Debt as % of cash
- Revenue growth
- Gross margin / operating margin
- Narrative on liquidity, valuation, growth expectations, and financial flexibility

If unavailable, state `Not found in public sources reviewed`.
