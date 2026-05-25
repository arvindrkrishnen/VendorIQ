# Sub-Agent Co-ordination Playbook

**Playbook name:** Parallel Sub-Agent Orchestration and Consolidated Reasoning  
**Primary skill:** VendorIQ Universal Vendor Analysis Skill  
**Invocation file:** `playbooks/sub-agent-co-ordination-playbook.md`  
**Purpose:** Enable a master agent or orchestrator to trigger multiple specialized sub-agents in parallel, collect structured outputs, validate evidence, resolve conflicts, and consolidate results into one final VendorIQ report section assembly.

> Note: The filename intentionally uses `co-ordination` to match the requested artifact name. Teams may also alias this playbook as `sub-agent-coordination-playbook.md`.

---

## 1. When to Invoke This Playbook

Invoke this playbook whenever the VendorIQ skill must execute the required sub-agent workflow, especially when:

- the report requires multiple independent due-diligence workstreams;
- the vendor has multiple products, segments, geographies, or public/private evidence sources;
- public evidence must be gathered, reconciled, normalized, and cited;
- output from one section could contradict or overlap with another section;
- the user requests `standard` or `exhaustive` analysis;
- the orchestrator needs to speed up execution by running agents in parallel;
- the final report must consolidate many section-level Markdown outputs into one validated Markdown assembly before HTML conversion.

---

## 2. Core Pattern

```text
User Request
   ↓
Master Orchestrator
   ↓
Task Decomposition and Agent Selection
   ↓
Parallel Sub-Agent Execution
   ↓
Structured Markdown Output Collection
   ↓
Evidence and Reference Normalization
   ↓
Conflict, Gap, and Quality Review
   ↓
Final Markdown Assembly
   ↓
Self-Contained HTML Conversion
```

The master orchestrator owns the final answer. Sub-agents own only their assigned sections or workstreams.

---

## 3. Master Orchestrator Responsibilities

The master orchestrator must:

1. Interpret the user request and required input fields.
2. Determine whether the run is `standard` or `exhaustive`.
3. Build a task plan mapped to the required report sections.
4. Select the sub-agents needed for the vendor, ticker, industry, geography, and competitor context.
5. Run eligible sub-agents in parallel.
6. Enforce timeouts, retries, and fallback behavior.
7. Require every sub-agent to return section-ready Markdown only.
8. Collect raw evidence URLs from sub-agent Markdown.
9. Normalize citations into numbered references.
10. Detect duplication, missing evidence, unsupported assertions, and contradictions.
11. Resolve conflicts using the evidence hierarchy from `SKILL.MD`.
12. Assemble one complete Markdown report.
13. Validate section completeness, citation coverage, table quality, and not-found markers.
14. Trigger the Markdown-to-HTML conversion agent.
15. Produce only the required final persistent artifact: `artifacts/exhaustive_final_report.html`.

---

## 4. Sub-Agent Responsibilities

Each sub-agent must:

- execute only the assigned task;
- return Markdown only;
- include raw evidence URLs while drafting;
- use required Markdown tables where useful;
- include `Not found in public sources reviewed` when reliable public evidence is unavailable;
- state assumptions, limitations, and quality concerns;
- avoid creating separate files, JSON artifacts, HTML, CSS, JavaScript, screenshots, or image assets;
- avoid answering the full user request unless explicitly assigned by the master orchestrator.

---

## 5. Required Sub-Agent Clusters

The master orchestrator may group agents into parallel clusters to reduce total runtime while preserving validation quality.

### Cluster A: Company Identity, Financials, and Leadership

Run in parallel when ticker, website, or public/private status can be determined early.

- identity and financial metrics agent;
- executive leadership agent;
- market position agent;
- SEC filing scan agent, when public ticker or SEC CIK exists.

### Cluster B: Business Model, Products, and Capabilities

Run after initial identity is known.

- business model and revenue model agent;
- product/service catalog agent;
- product-to-capability mapping agent;
- AI/ML/GenAI capabilities agent.

### Cluster C: Architecture and Technical Due Diligence

Run after major products are identified.

- architecture agent;
- information architecture agent;
- application architecture agent;
- security architecture agent;
- standards and interoperability agent;
- resiliency and disaster recovery agent.

### Cluster D: Ecosystem, Customers, Public Sector, and Proof

Run in parallel with Cluster C when product names are available.

- customer segments agent;
- suppliers, cloud providers, technology partners, and ecosystem dependencies agent;
- government contracts and public-sector signals agent;
- milestones, acquisitions, partnerships, and recognitions agent;
- case studies and measurable client benefits agent.

### Cluster E: Market Perception, Risk, Moat, and Competition

Run after product catalog and market position have enough evidence.

- ESG, sustainability, privacy, and responsible-business posture agent;
- analyst reviews, market sentiment, and external perception agent;
- cybersecurity, vulnerabilities, regulatory issues, and litigation signals agent;
- future actions and forward-looking indicators agent;
- product moat and differentiation agent;
- competitive landscape and Pugh Matrix agent;
- strengths, gaps, risks, and differentiation agent.

### Cluster F: Finalization

Run after all content agents complete or timeout.

- reference normalization agent;
- quality evaluation agent;
- Markdown-to-HTML conversion agent.

---

## 6. Parallel Execution Rules

The orchestrator should execute independent agents concurrently, but it must respect dependencies.

```text
Phase 0: Validate input and identify vendor context
Phase 1: Run Cluster A
Phase 2: Run Cluster B after basic identity is known
Phase 3: Run Clusters C and D after product catalog exists
Phase 4: Run Cluster E after products, market, and evidence base exist
Phase 5: Run Cluster F after all section Markdown is collected
```

Recommended concurrency controls:

```yaml
parallel_execution:
  enabled: true
  max_parallel_agents: 6
  timeout_seconds_per_agent: 90
  max_retries_per_agent: 2
  retry_backoff_seconds: 3
  fallback_strategy: partial_markdown_with_not_found_markers
  preserve_partial_results: true
  fail_fast: false
```

Use a lower `max_parallel_agents` when the provider has rate limits or when web/search grounding is constrained.

---

## 7. Task Assignment Object

The master orchestrator should create a normalized task assignment object for every sub-agent.

```json
{
  "trace_id": "vendoriq-{{run_id}}",
  "vendor_name": "{{vendor_name}}",
  "ticker": "{{ticker_or_null}}",
  "website": "{{website_or_null}}",
  "sec_cik": "{{sec_cik_or_null}}",
  "industry_focus": "{{industry_focus_or_null}}",
  "geography": "{{geography_or_null}}",
  "depth": "standard | exhaustive",
  "agent_name": "{{agent_name}}",
  "assigned_section": "{{report_section_name}}",
  "assigned_task": "{{specific_task}}",
  "evidence_requirements": [
    "Use raw source URLs while drafting",
    "Prefer SEC, annual reports, investor relations, official product documentation, and reputable financial sources",
    "Mark unavailable evidence as Not found in public sources reviewed"
  ],
  "output_format": "section-ready Markdown only"
}
```

---

## 8. Sub-Agent Output Contract

Every sub-agent must return one Markdown block with this structure:

```markdown
## {{Assigned Section Title}}

### Section Summary

### Evidence-Backed Analysis

### Tables and Matrices, if applicable

### Not-Found Items and Evidence Gaps

### Quality Notes

### Raw Evidence URLs
- https://example.com/source-1
- https://example.com/source-2
```

Rules:

- Do not return JSON as the main output.
- Do not return HTML.
- Do not use final numbered citations inside sub-agent output unless the orchestrator has already assigned the reference map.
- Include raw URLs so the reference normalization agent can assign `[1]`, `[2]`, and `[3]` style citations.
- Include tables in Markdown only.

---

## 9. Consolidation Algorithm

The master orchestrator should consolidate sub-agent output using this sequence:

1. **Schema check:** Confirm each agent returned section-ready Markdown.
2. **Section check:** Confirm the assigned section title is present.
3. **Evidence check:** Extract raw URLs and claim-adjacent source references.
4. **Not-found check:** Confirm missing evidence uses `Not found in public sources reviewed`.
5. **Deduplication:** Remove repeated paragraphs, repeated URLs, repeated product descriptions, and repeated risks.
6. **Conflict detection:** Identify conflicting names, metrics, dates, product claims, customer claims, certifications, and architecture claims.
7. **Conflict resolution:** Prefer higher-order evidence from the evidence hierarchy.
8. **Gap handling:** Preserve unresolved gaps in the relevant section and in Quality Document JSON.
9. **Citation normalization:** Map raw URLs to numbered references and replace claim-level raw URLs with `[n]` citations.
10. **Final assembly:** Order all sections according to `SKILL.MD` requirements.
11. **Quality evaluation:** Produce Quality Document JSON as the final Markdown section.
12. **HTML conversion:** Convert validated Markdown into `artifacts/exhaustive_final_report.html`.

---

## 10. Conflict Resolution Rules

When agents disagree, the master orchestrator must resolve conflicts using the following order:

1. SEC filings, annual reports, quarterly reports, proxy statements, investor relations, or issuer filings.
2. Official company product, leadership, trust, documentation, API, and customer-story pages.
3. Reputable financial and analyst sources.
4. Government procurement portals, FedRAMP marketplace, agency awards, and marketplace listings.
5. Reputable news and market-research sources.
6. Lower-confidence or indirect sources.

If conflicts remain unresolved, the final report must explicitly state:

```text
Evidence conflict unresolved based on public sources reviewed
```

and explain what additional source would be required.

---

## 11. Confidence Scoring

Each section should receive an internal confidence score from the master orchestrator.

```yaml
confidence_scoring:
  high:
    criteria:
      - multiple independent high-quality sources agree
      - official or regulatory source supports the claim
      - claim is recent and directly stated
  medium:
    criteria:
      - one strong source supports the claim
      - supporting source is indirect but credible
      - evidence is partially complete
  low:
    criteria:
      - evidence is weak, dated, indirect, or incomplete
      - sources disagree
      - public evidence is limited
```

The final Quality Document JSON should summarize section-level confidence, unresolved gaps, and evidence limitations.

---

## 12. Retry and Fallback Rules

If a sub-agent fails, times out, or returns invalid content:

1. Retry the agent once with a shorter, stricter prompt.
2. If it fails again, retry with a narrower task focused only on evidence discovery and not-found markers.
3. If it still fails, insert a section-level fallback block:

```markdown
## {{Assigned Section Title}}

Not found in public sources reviewed

The assigned sub-agent failed or returned insufficient evidence. The orchestrator could not verify this section from the reviewed public sources. Additional official documentation, regulatory filings, customer references, or vendor-provided material would be required.
```

4. Continue the run unless a critical finalization agent fails.

Critical finalization failures include:

- reference normalization failure;
- Markdown assembly validation failure;
- Markdown-to-HTML conversion failure.

---

## 13. Master Agent Prompt Template

```text
You are the VendorIQ Master Orchestrator.

User request:
{{user_request}}

Vendor context:
{{vendor_context}}

Depth:
{{standard_or_exhaustive}}

Your responsibilities:
1. Decompose the request into report-section workstreams.
2. Assign each workstream to the correct specialized sub-agent.
3. Execute independent sub-agents in parallel while respecting dependencies.
4. Require Markdown-only section output with raw evidence URLs.
5. Collect and validate all sub-agent outputs.
6. Detect duplication, unsupported claims, contradictions, and gaps.
7. Resolve conflicts using the VendorIQ evidence hierarchy.
8. Normalize raw URLs into numbered citations.
9. Assemble the complete Markdown report.
10. Place Reference Links immediately before Quality Document JSON.
11. Ensure Quality Document JSON is the final visible Markdown section.
12. Trigger conversion into one self-contained HTML artifact.

Do not create any persistent artifact other than artifacts/exhaustive_final_report.html.
```

---

## 14. Sub-Agent Prompt Template

```text
You are {{agent_name}} for the VendorIQ skill.

Assigned task:
{{assigned_task}}

Assigned section:
{{assigned_section}}

Vendor context:
{{vendor_context}}

Depth:
{{standard_or_exhaustive}}

Return section-ready Markdown only.

Your Markdown must include:
- the assigned section heading;
- evidence-backed analysis;
- Markdown tables where useful;
- raw evidence URLs while drafting;
- Not found in public sources reviewed where evidence is unavailable;
- quality notes for weak, missing, or conflicting evidence.

Rules:
- Focus only on your assigned task.
- Do not create HTML, CSS, JavaScript, JSON artifacts, or files.
- Do not invent facts, metrics, customers, architecture, certifications, or executive credentials.
- Do not infer customers from logos or product architecture from marketing language.
```

---

## 15. Python Async Orchestration Pattern

The following pattern is implementation guidance for local CLI or application code. Replace `call_llm_agent` with the actual provider implementation.

```python
import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class AgentTask:
    agent_name: str
    assigned_section: str
    assigned_task: str
    depends_on: Optional[List[str]] = None


async def run_sub_agent(task: AgentTask, context: Dict[str, Any]) -> Dict[str, Any]:
    prompt = build_sub_agent_prompt(task, context)
    markdown = await call_llm_agent(agent_name=task.agent_name, prompt=prompt)
    return {
        "agent_name": task.agent_name,
        "assigned_section": task.assigned_section,
        "markdown": markdown,
        "status": "completed"
    }


async def run_agent_cluster(
    cluster_tasks: List[AgentTask],
    context: Dict[str, Any],
    max_parallel_agents: int = 6,
    timeout_seconds: int = 90,
) -> List[Dict[str, Any]]:
    semaphore = asyncio.Semaphore(max_parallel_agents)

    async def guarded_run(task: AgentTask) -> Dict[str, Any]:
        async with semaphore:
            try:
                return await asyncio.wait_for(
                    run_sub_agent(task, context),
                    timeout=timeout_seconds,
                )
            except Exception as exc:
                return {
                    "agent_name": task.agent_name,
                    "assigned_section": task.assigned_section,
                    "markdown": build_fallback_markdown(task, exc),
                    "status": "fallback"
                }

    return await asyncio.gather(*(guarded_run(task) for task in cluster_tasks))


async def orchestrate_vendoriq_report(context: Dict[str, Any]) -> str:
    all_outputs: List[Dict[str, Any]] = []

    for cluster in build_execution_clusters(context):
        cluster_outputs = await run_agent_cluster(cluster.tasks, context)
        all_outputs.extend(cluster_outputs)
        context = update_context_from_outputs(context, cluster_outputs)

    markdown = assemble_markdown(all_outputs, context)
    markdown = normalize_references(markdown)
    validate_markdown(markdown)
    html_path = convert_markdown_to_self_contained_html(
        markdown,
        output_path="artifacts/exhaustive_final_report.html",
    )
    return html_path
```

---

## 16. Quality Gates Before HTML Conversion

Before HTML conversion, the master orchestrator must verify:

- every required report section exists;
- every factual claim is cited or marked not found;
- every raw URL is included in `Reference Links` or removed after citation normalization;
- `Reference Links` appears immediately before `Quality Document JSON`;
- `Quality Document JSON` is the final Markdown section;
- Markdown tables are valid;
- Pugh Matrix exists when competitive analysis is attempted;
- public-company financial charts are represented when data is available;
- no unsupported customer, architecture, certification, or executive-credential claims remain;
- no sub-agent output includes HTML, CSS, JavaScript, or separate artifact instructions.

---

## 17. Completion Criteria

This playbook is complete when:

- all eligible sub-agent clusters have completed, failed with fallback, or been explicitly marked not applicable;
- outputs have been consolidated into one Markdown report;
- references have been normalized;
- quality evaluation has been completed;
- final HTML has been created at `artifacts/exhaustive_final_report.html`;
- no other persistent user-facing output files are produced.
