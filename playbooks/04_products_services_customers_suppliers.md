# Playbook 04: Products, Services, Architecture, Customers, and Suppliers

Use:

- `product_services_agent`
- `architecture_agent`
- `product_moat_agent`
- `customer_supplier_agent`

## Objective

Build a detailed product and technology due-diligence view of the vendor. The output must help a buyer, investor, architect, or diligence team understand what each product does, how each product is architected, what makes each product defensible, and what risks or unknowns remain.

## Required Steps

1. Identify all major products, platforms, services, modules, and SKUs.
2. Build a product catalog table.
3. For each product, capture:
   - purpose;
   - target buyer;
   - target industry;
   - business workflow;
   - deployment model;
   - core modules;
   - technical features;
   - APIs/integrations;
   - data architecture;
   - security/compliance;
   - AI/automation;
   - scalability/resiliency;
   - customer proof;
   - ecosystem dependencies;
   - product maturity;
   - limitations;
   - product-specific moat.
4. Build a product technical capability matrix.
5. Build a product architecture matrix.
6. Build a product architecture risk matrix.
7. Build a product moat matrix.
8. Map customers and case studies to products where possible.
9. Map suppliers, partners, marketplaces, and cloud dependencies to products where possible.
10. Cite URLs for every named product, customer, partner, architecture detail, certification, API, or technical capability.

## Required Tables

### Product Catalog Table

| Product | Category | Buyer Persona | Deployment Model | Core Capabilities | Evidence |
|---|---|---|---|---|---|

### Product Technical Capability Matrix

| Product | Data Architecture | APIs / Integrations | AI / Automation | Security / Compliance | Resiliency / Scale | Evidence |
|---|---|---|---|---|---|---|

### Product Architecture Matrix

| Product | Deployment | Tenant Model | Core Components | Data Architecture | Integration Architecture | Security / Compliance | Resiliency | Evidence |
|---|---|---|---|---|---|---|---|---|

### Product Moat Matrix

| Product | Technical Moat | Data Moat | Workflow Moat | Ecosystem Moat | Switching-Cost Moat | Moat Durability | Evidence |
|---|---|---|---|---|---|---|---|

## Guardrails

- Do not invent product names, APIs, architecture, certifications, customers, or partners.
- If information is unavailable, state `Not found in public sources reviewed`.
- Separate verified evidence from inference.
- Include raw URLs while drafting; the orchestrator will convert them to numbered references.
