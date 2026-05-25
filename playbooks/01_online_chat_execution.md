# Playbook 01: Online Chat Execution

Execute VendorIQ in online chat. Read the full repo instruction package, run each playbook, require each sub-agent to return section-ready Markdown only, assemble exhaustive_final_report.md, validate it, append Quality Document JSON, and only then convert to exhaustive_final_report.html.

## Output Format

Return Markdown only. Do not produce HTML, CSS, JavaScript, final files, or standalone JSON.

## Minimum Depth

In exhaustive mode, this playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. If evidence is unavailable, explain what was searched, what was not found, and what due-diligence questions remain.

## Guardrails

Do not invent facts. Include raw URLs while drafting; the orchestrator will convert them to numbered references. Use `Not found in public sources reviewed` when evidence is unavailable.
