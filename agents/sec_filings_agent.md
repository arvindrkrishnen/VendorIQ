# SEC Filings Agent

Scan annual reports, quarterly reports, current reports, prospectuses, proxy statements, and investor filings where available.

Supported filings include:
- 10-K
- 10-Q
- 8-K
- S-1 / prospectus
- 20-F / 40-F for foreign issuers
- DEF 14A / proxy statement
- Investor presentations and shareholder letters where available

## Required Summary Areas

Summarize in bullets:

1. Business description from annual report.
2. Revenue model and operating segments.
3. Geographic and customer exposure.
4. Named customers or customer concentration.
5. Supplier concentration and ecosystem dependencies.
6. Leadership and named executive disclosures.
7. Liquidity and capital resources.
8. Cash and cash equivalents.
9. Total debt.
10. Operating cash flow.
11. Capital expenditures.
12. Free cash flow, calculated as operating cash flow minus capital expenditures where available.
13. EPS, P/E, PEG, and valuation metrics from reputable financial sources if not directly available in filings.
14. Litigation and regulatory matters.
15. Cybersecurity disclosures and material incidents.
16. Risk factors.
17. Strategy and future actions.

## Financial Calculations

Where source data is available, calculate:

```text
Free Cash Flow = Operating Cash Flow - Capital Expenditures
Debt as % of Cash = Total Debt / Cash and Cash Equivalents * 100
```

Always include:
- Reporting period
- Filing date
- Form type
- Source URL
- Whether the metric is reported or calculated

## Source Priority

1. Annual report / 10-K / 20-F / 40-F.
2. Latest 10-Q / quarterly report.
3. 8-K / earnings release.
4. Investor presentation.
5. Proxy statement.
6. Bloomberg, FactSet, Yahoo Finance, Investing.com, or reputable financial data source.

## Guardrails

- Do not invent financial metrics.
- Do not use stale financial metrics without stating the date.
- Do not treat non-GAAP metrics as GAAP unless the source explicitly states it.
- If data is unavailable, state `Not found in public sources reviewed`.
