# Playbook 08: Final Report Assembly

Assemble all sections into `exhaustive_final_report.md`.

## Required Final Assembly Behavior

1. Collect all section Markdown returned by sub-agents.
2. Extract all raw URLs from all sections.
3. Deduplicate URLs while preserving first-seen order.
4. Assign numbered references:
   - `[1]`
   - `[2]`
   - `[3]`
5. Replace raw inline URLs in the report body with numbered references.
6. Add one centralized section:

```markdown
## Reference Links
```

7. Render each source URL as:

```markdown
[1] https://example.com
[2] https://example.com/annual-report
```

8. Add `Quality Document JSON` as the final section.
9. Do not output separate progress, evidence, reference, financial, leadership, Pugh Matrix, or JSON files.

## Required Final Section Order

The final report must end with:

```markdown
## Reference Links

[1] ...
[2] ...

---

## Quality Document JSON

```json
{}
```
```

## Quality Checks

The assembler must validate:

- Every `[n]` in the body resolves to a URL in `Reference Links`.
- No raw `http://` or `https://` URLs remain in the main report body, except inside `Reference Links`.
- `Quality Document JSON` is the final section.
- The final report remains the only persistent output file.
