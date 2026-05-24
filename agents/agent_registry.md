# Agent Registry

## Execution Principle
The orchestrator owns the final output. Sub-agents produce section-ready Markdown content with evidence URLs. Sub-agents must not create separate persistent artifacts.

## Required Agents

| Agent | Responsibility | Primary Output |
|---|---|---|
| `orchestrator_agent` | Coordinates the full run, delegates sections, enforces guardrails, assembles report | One final Markdown report |
| `identity_sec_resolution_agent` | Resolves legal entity, ticker, website, CIK, latest SEC filings | Identity and filing section |
| `market_position_agent` | Company overview, history, mission, market position, geography | Market position section |
| `business_model_agent` | Revenue model, segment model, GTM, operating drivers | Business model section |
| `product_services_agent` | Exhaustive products/services catalog and capability map | Product section |
| `customer_supplier_agent` | Named customers, customer segments, suppliers, cloud providers, partners | Commercial ecosystem section |
| `government_contracts_agent` | Direct awards, agency contracts, FedRAMP, marketplaces, public-sector signals | Government/public-sector section |
| `sec_filings_agent` | 10-K/10-Q/8-K scan, risk factors, strategy, customers/suppliers, future actions | SEC filing scan bullets |
| `future_actions_agent` | Disclosed plans, roadmap, capital allocation, hiring/geography/product expansion | Future actions section |
| `architecture_agent` | Technology, application, information, security, standards, resiliency | Architecture section |
| `ai_ml_genai_agent` | AI/ML/automation/GenAI capabilities and benefits | AI capability section |
| `competitive_pugh_matrix_agent` | Competitors and Pugh Matrix table | Competitive section and table |
| `quality_evaluation_agent` | Evidence authenticity, completeness, output compliance | Quality Document JSON |
| `financial_metrics_agent` | Extracts EPS, P/E, PEG, FCF, cash, debt, debt/cash ratio, market cap, revenue growth, margin signals, and valuation/liquidity narrative for public companies | Financial metrics and valuation narrative |
| `leadership_credentials_agent` | Extracts leadership from annual report/proxy/company site and enriches credentials from official bios and LinkedIn/public profiles | Leadership credentials subsection |
| `reference_normalization_agent` | Deduplicates source URLs, assigns numeric references, replaces raw URLs with `[n]`, and renders `Reference Links` | Numbered reference map |

## Universal Agent Output Contract
Each agent must return:

1. Markdown section content.
2. Evidence URLs embedded in the content.
3. Any unknowns labeled `Not found in public sources reviewed`.
4. No separate files.
