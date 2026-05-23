# Guardrails, Quality Gates, and Validation Controls

## Single Persistent Output Guardrail
The run must leave exactly one persistent user-facing output:

```text
artifacts/exhaustive_final_report.md
```

The system must not require separate output files for progress, evidence, quality, SEC summary, Pugh Matrix, or government contracts. Those data objects may exist transiently in memory or a temporary runtime directory but must be embedded into the final Markdown or removed during cleanup.

## Authenticity Gate
Every material factual claim must be supported by a visible URL in the same paragraph, table row, or bullet group. Claims without evidence must be rewritten as:

```text
Not found in public sources reviewed.
```

### Authenticity Checks
- Source URL exists for each factual section.
- SEC-related claims cite SEC or investor-relations URLs.
- Product claims cite official product pages or documentation.
- Customer claims cite case studies, press releases, SEC filings, or customer pages.
- Supplier claims cite SEC filings, official partnership pages, marketplace listings, or integration documentation.
- Government-contract claims cite government procurement, marketplace, FedRAMP, agency, or official vendor sources.
- Analyst claims cite analyst platforms, reputable financial pages, or investment research references.

## Exhaustiveness Gate
The report fails if any required major section is missing or reduced to a short summary.

Minimum expectations:
- product/services section includes product families, capabilities, sub-capabilities, buyer personas, and deployment context;
- customer/supplier section distinguishes named entities from categories;
- government section distinguishes direct awards from channel availability;
- SEC section includes bulleted extraction from material filings;
- future actions section separates disclosed plans from inference.

## Quality Document Gate
The final report must end with:

```markdown
## Quality Document JSON
```json
{ ... }
```
```

The embedded JSON must include:
- `overall_quality_rating`;
- `authenticity_gate`;
- `single_output_compliance`;
- `unsupported_claim_count`;
- `section_scores`;
- `provider_configuration`;
- `cleanup_status`;
- `recommendations`.

## Clean-State Verification
A session is complete only if:
- final Markdown exists;
- no other generated artifact remains in the persistent output directory;
- temporary runtime directory is deleted or empty;
- quality document is embedded as the final section;
- Pugh Matrix is rendered as a table;
- evidence appendix exists inside the report;
- authenticity gate passes or explicitly records exceptions.

## Idempotent Cleanup
Cleanup must be safe to run repeatedly. It must:
- remove temporary runtime folders;
- preserve `artifacts/exhaustive_final_report.md`;
- avoid deleting package source files;
- not fail if files are already absent.

## Provider-Key Safety
- Never hardcode API keys in Python files, Markdown files, or VS Code tasks.
- Use environment variables or a local `.env` file excluded from source control.
- `.env.example` may list variable names but must not contain real secrets.

## Failure Handling
If provider execution fails:
1. record the error in the final Quality Document JSON if a report can still be assembled;
2. use fallback provider only if configured;
3. otherwise produce a structured scaffold report that clearly says model execution was not completed;
4. still preserve the single-output rule.

