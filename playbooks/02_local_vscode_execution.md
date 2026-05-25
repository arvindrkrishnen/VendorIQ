# Playbook 02: Local VS Code Execution

Run `src/universal_vendor_orchestrator.py` with provider keys. Local execution must generate `artifacts/exhaustive_final_report.md` first and `artifacts/exhaustive_final_report.html` only after Markdown validation passes.

## Output Format

Return Markdown only. Do not produce HTML, CSS, JavaScript, final files, or standalone JSON.

## Minimum Depth

In exhaustive mode, this playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. If evidence is unavailable, explain what was searched, what was not found, and what due-diligence questions remain.

## Guardrails

Do not invent facts. Include raw URLs while drafting; the orchestrator will convert them to numbered references. Use `Not found in public sources reviewed` when evidence is unavailable.
