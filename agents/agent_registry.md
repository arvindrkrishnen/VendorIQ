# Agent Registry

## Execution Principle

The orchestrator owns the final output. Sub-agents produce section-ready Markdown content with evidence URLs. Sub-agents must not create separate persistent artifacts.

## Agent Output Contract

All agents must return Markdown only. Agents must not produce HTML, CSS, JavaScript, files, or standalone JSON artifacts. Each agent must return Markdown section content, raw evidence URLs while drafting, unknowns labeled `Not found in public sources reviewed`, and required Markdown tables.

## Required Agents

| Agent | Responsibility | Primary Output |
|---|---|---|
| `orchestrator_agent` | Coordinates the full run, delegates sections, enforces guardrails, normalizes references, assembles Markdown, validates Markdown, and triggers final HTML conversion | Complete Markdown then HTML |
| `identity_sec_resolution_agent` | Resolves legal entity, ticker, website, CIK, filings, and official sources | Identity and filing section |
| `market_position_agent` | Company overview and market position | Market position section |
| `business_model_agent` | Revenue model, segment model, GTM, operating drivers | Business model section |
| `financial_metrics_agent` | EPS, P/E, PEG, FCF, cash, debt, revenue growth, margins | Financial metrics section |
| `leadership_credentials_agent` | Leadership extraction and credential enrichment | Leadership section |
| `product_services_agent` | Product-by-product catalog and capability map | Product due-diligence section |
| `architecture_agent` | Product-by-product technology architecture | Architecture due-diligence section |
| `product_moat_agent` | Product-specific defensibility | Product moat section |
| `customer_supplier_agent` | Customers, suppliers, partners, dependencies | Commercial ecosystem section |
| `government_contracts_agent` | Government awards, FedRAMP, marketplaces, public-sector signals | Public-sector section |
| `sec_filings_agent` | SEC filing scan and risk/strategy bullets | SEC filing section |
| `future_actions_agent` | Disclosed plans and forward-looking indicators | Future actions section |
| `ai_ml_genai_agent` | AI/ML/automation/GenAI capabilities by product | AI capability section |
| `competitive_pugh_matrix_agent` | Competitors and Pugh Matrix | Competitive section |
| `reference_normalization_agent` | Deduplicates URLs and renders Reference Links | Reference map |
| `quality_evaluation_agent` | Validates completeness, evidence, word counts, required tables, and output compliance | Quality Document JSON |
