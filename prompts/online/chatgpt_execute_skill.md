# ChatGPT Online Execution Prompt

You are executing the Universal Vendor Analysis Skill from the uploaded zip or GitHub repository.
Read README.md, skills.md, agents/agent_registry.md, playbooks/, and guardrails/.
Execute the skill for:
Vendor: <VENDOR NAME>
Ticker: <OPTIONAL TICKER>
Website: <OPTIONAL WEBSITE>

Rules:
- Use browsing/search/grounding if available.
- Execute each major section through the sub-agent definitions.
- Every factual claim must include a source URL or `Not found in public sources reviewed`.
- Produce one final Markdown artifact named exhaustive_final_report.md.
- Embed Pugh Matrix as a Markdown table.
- Make the last section Quality Document JSON.
