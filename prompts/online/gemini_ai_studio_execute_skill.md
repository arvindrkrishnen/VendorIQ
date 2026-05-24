# Gemini AI Studio Online Execution Prompt

You are executing the Universal Vendor Analysis Skill from the uploaded zip or GitHub repository.

Execute the skill for:

Vendor: <VENDOR NAME>  
Ticker: <OPTIONAL TICKER>  
Website: <OPTIONAL WEBSITE>  
Depth: exhaustive

## Instructions for Gemini AI Studio

1. Read:
   - `README.md`
   - `SKILL.md`
   - `skills.md`
   - `agents/agent_registry.md`
   - `playbooks/`
   - `guardrails/`
   - `templates/exhaustive_final_report_template.md`
2. Use grounding/search if available.
3. Execute the full VendorIQ workflow and return one final HTML artifact.

If token limits apply, first load:
- `README.md`
- `SKILL.md`
- `skills.md`
- `agents/agent_registry.md`
- `playbooks/01_online_chat_execution.md`
- `playbooks/04_products_services_customers_suppliers.md`
- `playbooks/07_competitive_pugh_matrix.md`
- `playbooks/08_final_report_assembly.md`
- `guardrails/README.md`

Then load additional agent and playbook files section by section as needed.

## Core Evidence and Research Rules

- Use browsing/search/grounding if available.
- Execute each major section through the sub-agent definitions.
- Prefer SEC filings, annual reports, quarterly reports, investor relations, official product pages, product documentation, API/developer documentation, architecture documentation, trust/security/privacy pages, official press releases, government procurement sources, and reputable financial/news sources.
- Every factual claim must include a numbered citation such as `[1]`, `[2]`, or `[3]`.
- Every citation must resolve to a source URL in the `Reference Links` section.
- If evidence is unavailable, write `Not found in public sources reviewed`.
- Do not invent customers, suppliers, contracts, certifications, product names, APIs, architecture, financial metrics, leadership credentials, or analyst opinions.
- Embed Pugh Matrix and all due-diligence matrices as HTML tables.
- Do not create separate intermediate files.

## Final Deliverable Requirement

Produce one final interactive HTML artifact named:

```text
exhaustive_final_report.html
```

Do not produce `exhaustive_final_report.md` as the final deliverable.

The HTML file must be fully self-contained:
- All CSS must be inside a `<style>` block.
- All JavaScript must be inside a `<script>` block.
- Do not use external JavaScript libraries.
- Do not use external CSS frameworks.
- Do not use remote fonts.
- Do not use CDN links.
- Do not depend on external assets.

## Interactive HTML Requirements

Create a professional due-diligence dashboard-style HTML report with:

1. Sticky header with vendor name, ticker, generated date, and evidence methodology summary.
2. Clickable table of contents with anchor links to every major section.
3. Search box to filter visible sections by keyword.
4. Expand all and collapse all controls.
5. Collapsible major sections.
6. Sortable HTML tables using lightweight internal JavaScript.
7. Due-diligence cards for:
   - executive thesis;
   - key financial metrics;
   - leadership credentials;
   - product moat summary;
   - architecture risks;
   - major competitive findings.
8. Product-level matrices:
   - Product Catalog table;
   - Product Technical Capability Matrix;
   - Product Architecture Matrix;
   - Product Architecture Risk Matrix;
   - Product Moat Matrix;
   - Competitive Moat Matrix;
   - Product-Level Pugh Matrix.
9. Linked numbered citations:
   - every `[n]` citation in the body must link to the corresponding item in `Reference Links`;
   - every reference entry should link back to the first citation occurrence where possible;
   - external URLs must open in a new tab using `target="_blank"` and `rel="noopener noreferrer"`.
10. Status badges for:
   - Evidence-backed;
   - Not found;
   - Public company metric;
   - Product moat;
   - Architecture risk;
   - Competitive risk.
11. Accessibility:
   - semantic HTML;
   - keyboard-operable collapsible sections;
   - accessible button labels;
   - sufficient contrast;
   - do not rely on color alone.
12. Print support:
   - include `@media print`;
   - expand all sections for print;
   - hide interactive controls during print;
   - preserve tables and references.

## Required HTML Structure

The HTML must start with:

```html
<!doctype html>
<html lang="en">
```

The HTML must include:

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VendorIQ Due Diligence Report - <Vendor Name></title>
```

The HTML must include internal CSS:

```html
<style>
...
</style>
```

The HTML must include internal JavaScript:

```html
<script>
...
</script>
```

The body must use semantic structure:

```html
<header>
<nav>
<main>
<section>
<footer>
```

Do not wrap the final HTML artifact in Markdown code fences.

## Citation HTML Pattern

Use citation links like:

```html
<a class="citation" href="#ref-1" id="cite-1">[1]</a>
```

Use reference entries like:

```html
<li id="ref-1">
  <a href="https://example.com" target="_blank" rel="noopener noreferrer">https://example.com</a>
  <a class="backlink" href="#cite-1">↩</a>
</li>
```

If a factual statement has no evidence, write:

```html
<span class="badge badge-not-found">Not found in public sources reviewed</span>
```

## Required Sections Inside HTML

The HTML report must include these sections as interactive/collapsible panels:

1. Title Page and Evidence Methodology
2. Vendor Identity, Ticker, Website, Headquarters, Public/Private Status
3. Executive Thesis with Evidence-Linked Conclusions
4. Company Overview and Market Position
5. Business Model and Revenue Model
6. Detailed Product, Service, Platform, and Technical Capability Catalog
7. Product-to-Capability Map
8. Product-by-Product Technology and Architecture Due Diligence
9. Information Architecture Assessment
10. Application Architecture Assessment
11. Security Architecture Assessment
12. Technology Standards and Interoperability Assessment
13. Resiliency, Disaster Recovery, and Stability Assessment
14. AI, Machine Learning, Automation, and GenAI Capabilities by Product
15. Product Moat, Differentiation, and Defensibility Analysis
16. Key Customers and Customer Segments
17. Key Suppliers, Cloud Providers, Technology Partners, Channel Partners, and Ecosystem Dependencies
18. Government Contracts, Public-Sector Awards, FedRAMP Status, Marketplaces, and Procurement Vehicles
19. Major Milestones, Acquisitions, Partnerships, and Recognitions
20. Case Studies and Measurable Client Benefits
21. ESG, Sustainability, Privacy, and Responsible-Business Posture
22. Analyst Reviews, Market Sentiment, and External Perception
23. Cybersecurity Incidents, Vulnerabilities, Regulatory Issues, and Litigation Signals
24. SEC Filing Scan in Bulleted Format
25. Future Actions and Forward-Looking Indicators
26. Competitive Landscape, Product Moat, and Pugh Matrix
27. Strengths, Gaps, Risks, and Differentiation
28. Reference Links
29. Quality Document JSON

## Quality Document JSON

The Quality Document JSON must be the final visible content section and placed inside:

```html
<details class="quality-json" open>
  <summary>Quality Document JSON</summary>
  <pre><code>{ ... }</code></pre>
</details>
```
