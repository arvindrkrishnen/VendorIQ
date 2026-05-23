# Universal Vendor Analysis Agents

## Orchestration Pattern
The package uses an orchestrator-worker model. The orchestrator decomposes the vendor report into section tasks, dispatches those tasks to specialized sub-agents, validates output, and assembles one final Markdown report.

Sub-agents must be treated as bounded workers. They should not create final artifacts. They return structured section content to the orchestrator, which alone writes `artifacts/exhaustive_final_report.md`.

## Agent Registry

### 1. `orchestrator_agent`
**Role:** Coordinates the entire run.

**Responsibilities:**
- Select provider and model.
- Resolve runtime configuration.
- Create section task list.
- Dispatch each section to the correct sub-agent.
- Run quality and authenticity gates.
- Assemble one final Markdown file.
- Delete temporary runtime artifacts.

### 2. `identity_sec_resolution_agent`
**Role:** Resolves exact entity identity.

**Outputs:**
- legal entity;
- ticker;
- exchange;
- CIK;
- official website;
- investor relations URL;
- latest SEC filing URLs.

### 3. `market_position_agent`
**Role:** Produces overview, history, mission, target markets, geography, headquarters, and external perception.

### 4. `business_model_agent`
**Role:** Explains revenue model, segments, subscription/usage/license models, margin drivers, and go-to-market channels.

### 5. `product_services_agent`
**Role:** Details every product and service family.

**Must include:**
- feature detail;
- technical capabilities;
- integrations;
- deployment models;
- industries served;
- compliance claims;
- source URLs.

### 6. `architecture_agent`
**Role:** Assesses technology, information, application, security, standards, interoperability, resiliency, and DR architecture.

### 7. `ai_ml_genai_agent`
**Role:** Extracts AI, ML, automation, LLM, and GenAI capabilities.

### 8. `customer_intelligence_agent`
**Role:** Identifies named customers, customer segments, case studies, and customer concentration disclosures.

### 9. `supplier_ecosystem_agent`
**Role:** Identifies key suppliers, cloud providers, technology dependencies, channel partners, integrators, and marketplace relationships.

### 10. `government_contracts_agent`
**Role:** Searches for public-sector awards, government contracts, procurement vehicles, agency customers, FedRAMP listings, government marketplace eligibility, and public-sector partner channels.

### 11. `milestones_partnerships_agent`
**Role:** Builds reverse-chronology list of acquisitions, partnerships, recognitions, product launches, and major corporate milestones.

### 12. `case_studies_agent`
**Role:** Extracts case studies from official site and reputable sources with client name, benefit, summary, process impact, and URL.

### 13. `esg_privacy_agent`
**Role:** Covers ESG, sustainability, privacy, responsible AI, trust, and governance posture.

### 14. `analyst_market_agent`
**Role:** Summarizes analyst reviews, ratings, investment sentiment, peer positioning, and market perception.

### 15. `cyber_risk_agent`
**Role:** Identifies cybersecurity incidents, vulnerabilities, data breaches, regulatory issues, and litigation signals.

### 16. `sec_filings_agent`
**Role:** Scans material SEC filings and generates bullet-level extraction.

### 17. `future_actions_agent`
**Role:** Extracts disclosed future actions, roadmap signals, investment priorities, R&D focus, and strategic direction.

### 18. `competitive_pugh_matrix_agent`
**Role:** Creates internal Pugh Matrix JSON and returns a Markdown table version.

### 19. `quality_eval_agent`
**Role:** Runs evidence and quality validation and emits the Quality Document JSON object for embedding as the final report section.

## Common Sub-Agent Output Contract
Each sub-agent returns:

```json
{
  "section_title": "string",
  "markdown": "detailed markdown content with source URLs",
  "evidence_urls": ["https://..."],
  "unsupported_claims": [],
  "quality_notes": [],
  "passing_criteria_met": true
}
```

## Provider-Agnostic Prompting Requirements
Prompts must avoid provider-specific syntax. The orchestrator adapter converts a generic task into the right provider request for OpenAI, Anthropic, Gemini, or Perplexity.

Each sub-agent prompt must include:
- vendor name;
- ticker if available;
- official website if available;
- section goal;
- required output format;
- evidence URL requirement;
- instruction not to invent unsupported information.

