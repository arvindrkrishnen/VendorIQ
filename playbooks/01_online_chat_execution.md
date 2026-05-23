# Playbook 01: Online Chat Execution

## Goal
Execute the skill when the user uploads the zip to ChatGPT, Gemini AI Studio, or Claude Online, or when the user points the model to a GitHub repository.

## Steps
1. Read `README.md`, `skills.md`, `agents/agent_registry.md`, `guardrails/README.md`, and this playbook.
2. Resolve the vendor name, ticker, and website from the user prompt.
3. Use web search/browsing if available.
4. Run each section through the appropriate sub-agent definition in `agents/`.
5. Use official and primary evidence where possible.
6. Assemble a single Markdown report named `exhaustive_final_report.md`.
7. Embed the Pugh Matrix as a Markdown table.
8. Make `Quality Document JSON` the final section.
9. Do not create or ask the user to download separate JSON artifacts.

## Passing Criteria
- Final response/file is Markdown.
- All required sections are present.
- Each factual claim includes a URL or not-found marker.
- The output is one final report.
