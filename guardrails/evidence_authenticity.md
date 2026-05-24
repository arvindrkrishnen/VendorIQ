# Evidence Authenticity Gate

Every factual claim must include one of the following near the claim:

1. A numbered reference such as `[1]`, `[2]`, or `[3]` that resolves to a URL in the final `Reference Links` section; or
2. A raw visible URL while drafting, which the orchestrator must convert into a numbered reference during final assembly.

Unsupported claims must be removed or marked:

```text
Not found in public sources reviewed.
```

## Required Reference Links Section

The final report must contain a section named:

```markdown
## Reference Links
```

Each reference must follow this format:

```markdown
[1] https://example.com
[2] https://example.com/investors/annual-report
```

## Preferred Evidence Hierarchy

For public companies, use sources in this order:

1. Annual report / 10-K / 20-F / 40-F.
2. Latest quarterly report / 10-Q.
3. Investor presentation, investor day materials, proxy statement, and official investor relations pages.
4. Official company website, product pages, trust/security/privacy pages, and official customer stories.
5. Bloomberg, FactSet, Yahoo Finance, Investing.com, and reputable analyst/financial sources.
6. Reputable news, government, procurement, and market-research sources.

## Validation Rules

- Do not invent customers, suppliers, government contracts, certifications, executive credentials, or financial metrics.
- Do not infer government contracts from vague public-sector marketing.
- Do not use LinkedIn to override official annual report, proxy, or company leadership disclosures.
- For financial metrics, always include the period/date and source.
- If using calculated metrics such as Debt as % of Cash, show or explain the formula.
