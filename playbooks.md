# Universal Vendor Analysis Playbooks

## Playbook 1: Orchestrated Single-Report Execution

### Goal
Produce one exhaustive final Markdown report using section-level sub-agents and strict evidence controls.

### Steps
1. Resolve vendor identity, ticker, official website, SEC CIK if available, and public-company status.
2. Build an execution plan with one task per report section.
3. Dispatch each task to the assigned sub-agent.
4. Collect section output in memory or a temporary runtime directory.
5. Run authenticity checks on every section.
6. Assemble the final report in canonical order.
7. Convert Pugh Matrix JSON to a Markdown table.
8. Append Quality Document JSON as the final section.
9. Delete temporary runtime artifacts.
10. Verify that the only persistent output is `artifacts/exhaustive_final_report.md`.

### Passing Criteria
- Final report is exhaustive and sectioned.
- Every factual paragraph contains source URLs or explicit `Not found in public sources` markings.
- No standalone progress, evidence, Pugh Matrix, or quality JSON output files remain.

---

## Playbook 2: Vendor Identity and SEC Resolution

### Agent
`identity_sec_resolution_agent`

### Objective
Resolve the vendor’s exact legal entity, ticker, exchange, CIK, headquarters, website, fiscal year, and reporting status.

### Required Evidence
- SEC company page or filing URL for public companies.
- Investor relations URL.
- Official company website URL.

### Output Requirements
- Explain ambiguity if several companies share similar names.
- Use ticker and official domain to disambiguate.
- Include a source URL for every material entity attribute.

---

## Playbook 3: Products and Services Deep Dive

### Agent
`product_services_agent`

### Objective
Create an exhaustive product and services catalog.

### Required Detail
For each product or service:
- product name;
- product category;
- business capability enabled;
- technical capability;
- target user or buyer;
- deployment model;
- integrations or APIs;
- certifications or compliance claims;
- URLs.

### Passing Criteria
- No product family is reduced to one-line summary.
- Product capabilities are grouped by business capability and sub-capability.
- Publicly unsupported product claims are marked as not found.

---

## Playbook 4: Customer and Supplier Intelligence

### Agents
- `customer_intelligence_agent`
- `supplier_ecosystem_agent`

### Objective
Identify key customers, customer segments, suppliers, cloud providers, technology partners, channel partners, and ecosystem dependencies.

### Customer Sources
- official customer stories;
- press releases;
- SEC concentration disclosures;
- marketplace case studies;
- government award notices.

### Supplier Sources
- SEC risk-factor and supplier concentration disclosures;
- cloud marketplace listings;
- technology partner pages;
- public integration directories;
- vendor trust center and architecture pages.

### Passing Criteria
- Separates named customers from customer categories.
- Separates verified suppliers from partners and integrations.
- Does not invent supplier names from generic technology usage.

---

## Playbook 5: Government Contracts and Public-Sector Signals

### Agent
`government_contracts_agent`

### Objective
Identify public-sector contracts, procurement vehicles, marketplace listings, grants, agency customers, FedRAMP status, and government-focused certifications.

### Sources
- SAM.gov or agency award pages;
- USAspending.gov where applicable;
- FedRAMP marketplace;
- state procurement portals;
- company press releases;
- SEC public-sector risk or customer disclosures.

### Passing Criteria
- Distinguishes direct contract awards from reseller/channel availability.
- Includes date, agency, contract vehicle, value if public, and URL.
- If no recent government contracts are found, states `No recent direct government contracts found in public sources`.

---

## Playbook 6: SEC Filing Scan

### Agent
`sec_filings_agent`

### Objective
Scan the latest 10-K, 10-Q, 8-K, S-1, proxy, and material filings for business, risk, financial, customer, supplier, product, cybersecurity, litigation, and forward-looking signals.

### Required Bullet Categories
- Business description
- Revenue model and segment disclosures
- Material customers or concentration risk
- Suppliers and operational dependencies
- Product and R&D disclosures
- Competition
- Government and regulatory exposure
- Cybersecurity and data-protection disclosures
- Litigation and contingencies
- Liquidity and capital allocation
- Future actions and strategy indicators

### Passing Criteria
- Each bullet cites the filing URL.
- Bullets distinguish management statements from analyst inference.
- Filing date and period covered are stated.

---

## Playbook 7: Future Actions and Forward-Looking Signals

### Agent
`future_actions_agent`

### Objective
Extract future actions from filings, earnings releases, investor presentations, roadmap announcements, hiring trends, product launches, partnership announcements, and management commentary.

### Required Categories
- planned product expansion;
- geographic expansion;
- cloud, AI, platform, or infrastructure investments;
- sales and partner-channel expansion;
- public-sector growth plans;
- R&D priorities;
- risk-mitigation actions;
- M&A or capital allocation signals if disclosed.

### Passing Criteria
- Future actions are evidence-backed.
- Speculation is labeled clearly and separated from disclosed plans.

---

## Playbook 8: Pugh Matrix Generation

### Agent
`competitive_pugh_matrix_agent`

### Objective
Compare the target vendor with competitors and render a Markdown table in the final report.

### Criteria
- Value chain alignment
- Product breadth
- Technical architecture
- AI/automation/GenAI capabilities
- API readiness
- Cloud-native readiness
- Security and compliance posture
- Data strategy
- Customer proof points
- Supplier/partner ecosystem
- Government/public-sector readiness
- Geographic presence
- Key differentiators

### Output Format
The sub-agent may create an internal JSON object, but the final report must render it as a Markdown table with columns:

| Criterion | Target Vendor Score | Competitor Benchmarks | Evidence | Gaps |

### Passing Criteria
- Scores are supported by evidence URLs.
- No separate Pugh Matrix JSON file is persisted.

---

## Playbook 9: Authenticity and Quality Gate

### Agent
`quality_eval_agent`

### Objective
Evaluate evidence completeness, source quality, section completeness, claim authenticity, and single-output compliance.

### Required Final Section
Append a fenced JSON block under:

```markdown
## Quality Document JSON
```

The JSON must include:
- overall score;
- provider and model used;
- authenticity gate status;
- unsupported claim count;
- section-level scores;
- single-output compliance status;
- cleanup status;
- recommended next improvements.

