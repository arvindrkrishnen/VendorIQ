# Playbook 07: Competitive Product Moat and Pugh Matrix

Agent: competitive_pugh_matrix_agent. Identify competitors by product category, separate direct competitors from substitutes, compare products across architecture maturity, deployment, scalability, resiliency, security, API maturity, ecosystem, data architecture, AI/ML, workflow depth, implementation complexity, switching cost, customer proof, public-sector readiness, roadmap, and moat durability.

Required tables: Competitors by Product Category, Product-Level Pugh Matrix, Competitive Moat Matrix. Use 1-5 scoring or N/A when evidence is insufficient.

## Output Format

Return Markdown only. Do not produce HTML, CSS, JavaScript, final files, or standalone JSON.

## Minimum Depth

In exhaustive mode, this playbook must contribute at least 500 words of narrative analysis excluding tables unless public evidence is unavailable. If evidence is unavailable, explain what was searched, what was not found, and what due-diligence questions remain.

## Guardrails

Do not invent facts. Include raw URLs while drafting; the orchestrator will convert them to numbered references. Use `Not found in public sources reviewed` when evidence is unavailable.
