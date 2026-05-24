# ChatGPT Online Execution Prompt

Use this GitHub repository as the VendorIQ skill package:

https://github.com/arvindrkrishnen/VendorIQ

Execute the Universal Vendor Analysis Skill for:

Vendor: <VENDOR NAME>  
Ticker: <OPTIONAL TICKER>  
Website: <OPTIONAL WEBSITE>  
Depth: exhaustive

## Instructions for ChatGPT

1. Do not run code unless the user explicitly asks for local execution.
2. Treat the GitHub repository as an instruction package.
3. Read `SKILL.md` first.
4. Then read:
   - `README.md`
   - `skills.md`
   - `agents/agent_registry.md`
   - `guardrails/`
   - `playbooks/`
   - `templates/exhaustive_final_report_template.md`
5. Use web browsing/search for current public evidence.
6. Prefer SEC filings, annual reports, investor relations, official product pages, official press releases, government procurement sources, and reputable financial/news sources.
7. Every factual claim must include a URL.
8. If evidence is unavailable, write `Not found in public sources reviewed`.
9. Produce one final Markdown artifact named `exhaustive_final_report.md`.
10. Embed the Pugh Matrix as a Markdown table.
11. Make the final section `Quality Document JSON`.
12. Do not create separate intermediate files.
