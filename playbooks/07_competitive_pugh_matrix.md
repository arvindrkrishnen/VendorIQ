# Playbook 07: Competitive Product Moat and Pugh Matrix

Use `competitive_pugh_matrix_agent`.

## Objective

Create a product-level competitive due-diligence view. The analysis must compare the vendor’s major products against relevant competitors and substitutes. It must evaluate technology, architecture, integration, data, AI, security, compliance, workflow, implementation, customer proof, and moat durability.

## Required Steps

1. Identify competitors by product category.
2. Separate direct competitors from adjacent substitutes.
3. For each major vendor product, identify:
   - relevant competitors;
   - where the vendor wins;
   - where the vendor is neutral;
   - where the vendor loses;
   - architecture differentiators;
   - integration differentiators;
   - data / AI moat comparison;
   - security / compliance comparison;
   - workflow depth comparison;
   - customer proof comparison;
   - switching-cost comparison;
   - pricing / packaging comparison where public;
   - key due-diligence questions.
4. Build a product-level Pugh Matrix.
5. Build a competitive moat matrix.
6. Add battlecard bullets for each major product.
7. Cite source URLs for every competitor, product, capability, score rationale, and differentiator.

## Product-Level Pugh Matrix Criteria

Use these criteria where evidence exists:

- Product-market fit.
- Architecture maturity.
- Deployment flexibility.
- Cloud / hybrid / on-prem / edge support.
- Scalability.
- Resiliency / DR.
- Security and compliance.
- API maturity.
- Integration ecosystem.
- Data architecture.
- AI / ML / automation capability.
- Workflow depth.
- Implementation complexity.
- Switching cost.
- Customer proof.
- Public-sector readiness.
- Roadmap / R&D signal.
- Technical moat durability.
- Commercial moat durability.

## Scoring

Use a 1–5 score:

- 5 = clear, evidence-backed advantage.
- 4 = likely advantage with good evidence.
- 3 = parity or insufficient difference.
- 2 = weakness vs. competitor.
- 1 = material gap.
- N/A = insufficient evidence.

## Required Tables

### Competitors by Product Category

| Product Category | Vendor Product | Direct Competitors | Adjacent Substitutes | Evidence |
|---|---|---|---|---|

### Product-Level Pugh Matrix

| Product | Criterion | Vendor Score | Competitor Benchmark | Why It Matters | Evidence |
|---|---|---:|---|---|---|

### Competitive Moat Matrix

| Vendor Product | Primary Competitor | Vendor Moat | Competitor Advantage | Moat Durability | Risk of Erosion | Evidence |
|---|---|---|---|---|---|---|

## Guardrails

- Do not invent competitors or product capabilities.
- Do not score without evidence; use `N/A`.
- Distinguish direct competitor from substitute.
- Include raw URLs while drafting; the orchestrator will convert them to numbered references.
