# Universal Vendor Analysis Skill

**Name:** `universal-vendor-analysis`  
**Product name:** VendorIQ  
**Author:** Arvind Radhakrishnen  
**LinkedIn:** https://www.linkedin.com/in/arvindradhakrishnen/

VendorIQ is a reusable AI skill that generates evidence-backed vendor strategy intelligence for any target company. It can research and organize a vendor’s identity, business model, product portfolio, AI/GenAI capabilities, customer segments, partner ecosystem, public-sector signals, security and ESG posture, risks, competitors, strengths, gaps, and a weighted Pugh Matrix.

The value of VendorIQ is not only the depth of research, but also the ease of use. Users can run the skill in two ways:

1. **Online chat execution** — use ChatGPT, Google Gemini AI Studio, or Claude by uploading the skill package or pointing the model to the GitHub repository.
2. **Local / VS Code execution** — run the Python orchestrator locally from VS Code or another coding environment using a supported LLM provider.


<img width="1247" height="647" alt="image" src="https://github.com/user-attachments/assets/88201d39-4540-4b40-8ae3-56fb65f0c814" />

Both execution paths produce the same final deliverable:

```text
artifacts/exhaustive_final_report.md
```

In online chat execution, the model should return the same Markdown report content as the final answer or as a downloadable Markdown artifact named:

```text
exhaustive_final_report.md
```

## What the Skill Does

VendorIQ follows a multi-agent orchestration pattern. An orchestrator decomposes the vendor-analysis assignment into section-level work, delegates each section to a specialized sub-agent, validates evidence and completeness through guardrails, and assembles one final report.

The skill intentionally produces only one persistent user-facing output:

```text
artifacts/exhaustive_final_report.md
```

## Two Ways to Use VendorIQ

### Option 1 — Online Chat Execution

Use this option when you want ChatGPT, Gemini AI Studio, or Claude to execute the skill directly.

Users can run the online mode in either of these ways:

- **Upload the skill package zip** to ChatGPT, Gemini AI Studio, or Claude.
- **Point the model to the GitHub repository** and ask it to read the repository instructions.

Online execution does not require users to run Python locally. The quality of the output depends on the model’s available tools, especially file upload, long-context handling, and web browsing or grounding.

#### Online Prompt — Upload Zip

```text
You are executing the uploaded Universal Vendor Analysis Skill package.
Read README.md first, then skills.md, guardrails/README.md, agents/agent_registry.md, and the playbooks/ folder.
Execute the skill for the vendor: <VENDOR NAME>
Optional ticker: <TICKER>
Optional website: <WEBSITE>

Follow the package rules:
- Use the agents and playbooks as the execution plan.
- Use web browsing/search if available.
- Every factual claim must include a source URL.
- Do not invent customers, suppliers, government contracts, certifications, SEC details, or analyst commentary.
- Produce only one final Markdown artifact named exhaustive_final_report.md.
- Embed the Pugh Matrix as a Markdown table.
- Make the last section Quality Document JSON.
```

Example:

```text
Execute the uploaded Universal Vendor Analysis Skill for Rubrik, Inc. Ticker: RBRK. Website: https://www.rubrik.com. Produce only exhaustive_final_report.md.
```

#### Online Prompt — GitHub Repository

```text
Use this GitHub repository as a skill package: <GITHUB_REPO_URL>
Read README.md, skills.md, guardrails/, agents/, and playbooks/.
Execute the Universal Vendor Analysis Skill for vendor: <VENDOR NAME>.
Optional ticker: <TICKER>
Optional website: <WEBSITE>
Return one final Markdown file named exhaustive_final_report.md.
```

Example:

```text
Use this GitHub repository as a skill package: https://github.com/arvindrkrishnen/VendorIQ
Read README.md, skills.md, guardrails/, agents/, and playbooks/.
Execute the Universal Vendor Analysis Skill for Microsoft.
Return one final Markdown file named exhaustive_final_report.md.
```

#### ChatGPT Online Notes

- Use ChatGPT with file upload enabled.
- Upload the package zip or provide the GitHub repository URL.
- Ask ChatGPT to browse the web when available.
- Ask for the final deliverable as a downloadable Markdown file.
- Recommended prompt file: `prompts/online/chatgpt_execute_skill.md`.

#### Google Gemini AI Studio Online Notes

- Upload the zip or paste the key files into the prompt context.
- Enable grounding/search tools if available in your AI Studio setup.
- Recommended prompt file: `prompts/online/gemini_ai_studio_execute_skill.md`.

#### Claude Online Notes

- Upload the zip or connect the GitHub repository if your Claude environment supports repository context.
- Claude is well suited for long-context synthesis, but you must explicitly require evidence URLs.
- Recommended prompt file: `prompts/online/claude_execute_skill.md`.

### Option 2 — Local / VS Code Execution

Use this option when you want to run the skill from a local development environment such as VS Code, Claude Code, Cursor, or another coding assistant.

Local execution uses the included Python orchestrator:

```text
src/universal_vendor_orchestrator.py
```

It supports OpenAI, Anthropic Claude, Google Gemini, Perplexity, and offline scaffold mode.

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Copy the environment template:

```bash
cp .env.example .env
```

Populate the API key for the provider you want to use:

```bash
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"
GEMINI_API_KEY="your-gemini-key"
GOOGLE_API_KEY="your-google-key-if-needed"
PERPLEXITY_API_KEY="your-perplexity-key"
```

#### Run the Orchestrator

```bash
python src/universal_vendor_orchestrator.py \
  --vendor "Rubrik, Inc." \
  --ticker RBRK \
  --website https://www.rubrik.com \
  --provider perplexity \
  --model sonar-pro \
  --depth exhaustive
```

The final output is:

```text
artifacts/exhaustive_final_report.md
```

## Supported Execution Modes

| Usage path | Mode | How users run it | API keys needed by user | Output |
|---|---|---|---:|---|
| Online chat execution | ChatGPT Online | Upload zip or point to GitHub and prompt ChatGPT to execute | No local key required; depends on ChatGPT plan/tools | `exhaustive_final_report.md` |
| Online chat execution | Gemini AI Studio Online | Upload zip, paste repo files, or point to repo and run the Gemini prompt | No local key required inside zip; AI Studio access required | `exhaustive_final_report.md` |
| Online chat execution | Claude Online | Upload zip or connect repository and run the Claude prompt | No local key required; depends on Claude plan/tools | `exhaustive_final_report.md` |
| Local / VS Code execution | VS Code / local OpenAI | Run Python script with `--provider openai` | `OPENAI_API_KEY` | `artifacts/exhaustive_final_report.md` |
| Local / VS Code execution | VS Code / local Anthropic | Run Python script with `--provider anthropic` | `ANTHROPIC_API_KEY` | `artifacts/exhaustive_final_report.md` |
| Local / VS Code execution | VS Code / local Gemini | Run Python script with `--provider gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `artifacts/exhaustive_final_report.md` |
| Local / VS Code execution | VS Code / local Perplexity | Run Python script with `--provider perplexity` | `PERPLEXITY_API_KEY` | `artifacts/exhaustive_final_report.md` |
| Local / VS Code execution | Offline scaffold | Run Python script with `--provider offline` | None | Scaffold report only |

## Repository Layout

```text
.
├── README.md
├── CONTRIBUTIONS.md
├── skills.md
├── agents.md                         # index pointing to agents/ folder
├── playbooks.md                      # index pointing to playbooks/ folder
├── requirements.txt
├── .env.example
├── .gitignore
├── .vscode/
│   ├── tasks.json
│   └── launch.json
├── agents/
│   ├── README.md
│   ├── agent_registry.md
│   ├── orchestrator_agent.md
│   ├── identity_sec_resolution_agent.md
│   ├── product_services_agent.md
│   ├── customer_supplier_agent.md
│   ├── government_contracts_agent.md
│   ├── sec_filings_agent.md
│   ├── competitive_pugh_matrix_agent.md
│   └── quality_evaluation_agent.md
├── playbooks/
│   ├── README.md
│   ├── 01_online_chat_execution.md
│   ├── 02_local_vscode_execution.md
│   ├── 03_vendor_identity_sec_resolution.md
│   ├── 04_products_services_customers_suppliers.md
│   ├── 05_government_contracts_public_sector.md
│   ├── 06_sec_filings_future_actions.md
│   ├── 07_competitive_pugh_matrix.md
│   └── 08_final_report_assembly.md
├── guardrails/
│   ├── README.md
│   ├── evidence_authenticity.md
│   ├── single_output.md
│   └── quality_eval.md
├── prompts/
│   ├── online/
│   │   ├── chatgpt_execute_skill.md
│   │   ├── gemini_ai_studio_execute_skill.md
│   │   ├── claude_execute_skill.md
│   │   └── github_repo_execute_skill.md
│   └── local/
│       └── cli_prompt_template.md
├── templates/
│   └── exhaustive_final_report_template.md
├── src/
│   └── universal_vendor_orchestrator.py
└── artifacts/
    └── .gitkeep
```

## Architecture

```text
User
  |
  +-- Option 1: Online Chat Execution
  |      +-- Upload zip or provide GitHub URL
  |      +-- Model reads README.md, skills.md, agents/, playbooks/, guardrails/
  |      +-- Model executes sub-agent playbooks in its own context
  |      +-- Model returns exhaustive_final_report.md
  |
  +-- Option 2: Local / VS Code Execution
         +-- universal_vendor_orchestrator.py
         +-- Provider adapter: OpenAI / Anthropic / Gemini / Perplexity / Offline
         +-- Section task orchestration
         +-- Guardrail validation
         +-- Final report assembly
         +-- Single output cleanup
```

## Multi-Agent Execution Flow

1. **Orchestrator reads the vendor request.**
2. **Identity agent resolves the exact company, ticker, website, SEC CIK, and filing sources.**
3. **Section agents generate detailed content for products, customers, suppliers, government contracts, SEC filings, future actions, architecture, AI, market position, ESG, risks, and competitors.**
4. **Pugh Matrix agent creates scoring logic and renders the matrix as a Markdown table.**
5. **Quality evaluation agent validates evidence authenticity, completeness, unsupported claims, and single-output compliance.**
6. **Final report assembler creates `exhaustive_final_report.md` with Quality Document JSON as the last section.**

## Required Final Report Sections

1. Title page and evidence methodology
2. Vendor identity, ticker, website, headquarters, public/private status
3. Executive thesis with evidence-linked conclusions
4. Company overview and market position
5. Business model and revenue model
6. Detailed products and services catalog
7. Product-to-capability map
8. Technology architecture and platform capabilities
9. Information architecture assessment
10. Application architecture assessment
11. Security architecture assessment
12. Technology standards and interoperability assessment
13. Resiliency, disaster recovery, and stability assessment
14. AI, machine learning, automation, and GenAI capabilities
15. Key customers and customer segments
16. Key suppliers, cloud providers, technology partners, channel partners, and ecosystem dependencies
17. Government contracts, public-sector awards, FedRAMP status, marketplaces, and procurement vehicles
18. Major milestones, acquisitions, partnerships, and recognitions
19. Case studies and measurable client benefits
20. ESG, sustainability, privacy, and responsible-business posture
21. Analyst reviews, market sentiment, and external perception
22. Cybersecurity incidents, vulnerabilities, regulatory issues, and litigation signals
23. SEC filing scan in bulleted format
24. Future actions and forward-looking indicators
25. Competitive landscape and competitor identification
26. Pugh Matrix table
27. Strengths, gaps, risks, and differentiation
28. Evidence appendix with URLs grouped by section
29. Quality Document JSON as the final section

## Evidence and Authenticity Requirements

Every factual claim should include a source URL. Preferred source classes:

- SEC filings and official annual reports;
- investor relations pages;
- official vendor product pages;
- official trust, security, privacy, compliance, and sustainability pages;
- official customer stories and case studies;
- government procurement databases and agency award notices;
- FedRAMP marketplace and public-sector marketplaces;
- official press releases;
- reputable financial, analyst, and market-research references.

Rules:

- Do not invent customers, suppliers, certifications, or contracts.
- Do not infer government contracts from vague public-sector marketing language.
- Mark unavailable information as `Not found in public sources reviewed`.
- Treat SEC filings and official company disclosures as higher-priority evidence than secondary commentary.
- Include filing date, fiscal period, and form type when citing SEC filings.

## Updating Agents and Playbooks Independently

Agents and playbooks are intentionally separated:

- Update `agents/*.md` when you want to change role boundaries, inputs, outputs, or agent behavior.
- Update `playbooks/*.md` when you want to change execution steps, evidence requirements, or passing criteria.
- Update `guardrails/*.md` when you want to tighten validation rules.
- Update `skills.md` when you want to change the top-level behavior of the skill.

This separation makes the package easier to maintain in GitHub and easier for ChatGPT, Gemini, and Claude to understand when a user points to the repository.

## Best Practices

1. Use web-enabled execution for current analysis.
2. Use SEC filings as the anchor source for public companies.
3. Use official product pages for products and capabilities.
4. Separate named customers from inferred customer segments.
5. Separate direct government awards from marketplace availability or partner-led resale.
6. Put unsupported claims in the report as `Not found in public sources reviewed` rather than guessing.
7. Keep the final report as the only persistent output.

## Troubleshooting

### ChatGPT, Gemini, or Claude says it cannot execute code

Use online chat execution. Tell the model:

```text
Do not run code; read the package files as instructions and produce the final Markdown report using your available browsing/search capability.
```

### The report lacks current web URLs

Ask the online model to enable browsing/search, or use local Perplexity mode.

### The output creates extra files

The package rule is one output only. Ask the model to consolidate all content into `exhaustive_final_report.md` and delete or ignore intermediate artifacts.

### Gemini AI Studio has token limits

Start with `skills.md`, `agents/agent_registry.md`, `playbooks/01_online_chat_execution.md`, `guardrails/README.md`, and the vendor name. Then add agent/playbook files section by section if needed.

### Claude produces a narrative but not a file

Ask Claude to return the content as a Markdown artifact named `exhaustive_final_report.md` and make the final section `Quality Document JSON`.
