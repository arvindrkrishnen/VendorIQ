#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,time
from dataclasses import dataclass
from pathlib import Path
from typing import List
from markdown_validator import validate_markdown_report
from markdown_to_html_converter import convert_markdown_report_to_self_contained_html
from reference_normalizer import ReferenceManager
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_MD=ROOT/"artifacts"/"exhaustive_final_report.md"
DEFAULT_HTML=ROOT/"artifacts"/"exhaustive_final_report.html"
@dataclass
class RunConfig:
    vendor:str; ticker:str; website:str; provider:str; model:str; competitors:str; sec_cik:str; markdown_output:Path; html_output:Path; depth:str="exhaustive"; skip_html:bool=False; allow_html_on_validation_fail:bool=False
@dataclass
class SectionResult:
    agent:str; title:str; markdown:str; evidence_urls:List[str]
SECTION_TASKS=[("identity_sec_resolution_agent","Vendor Identity, Ticker, Website, Headquarters, Public/Private Status"),("market_position_agent","Company Overview and Market Position"),("business_model_agent","Business Model and Revenue Model"),("financial_metrics_agent","Financial Metrics and Valuation Narrative"),("leadership_credentials_agent","Leadership and Credentials"),("product_services_agent","Detailed Product, Service, Platform, and Technical Capability Catalog"),("architecture_agent","Product-by-Product Technology and Architecture Due Diligence"),("product_moat_agent","Product Moat, Differentiation, and Defensibility Analysis"),("ai_ml_genai_agent","AI, Machine Learning, Automation, and GenAI Capabilities by Product"),("customer_supplier_agent","Key Customers, Customer Segments, Suppliers, Partners, and Ecosystem Dependencies"),("government_contracts_agent","Government Contracts, Public-Sector Awards, FedRAMP Status, Marketplaces, and Procurement Vehicles"),("sec_filings_agent","SEC Filing Scan in Bulleted Format"),("future_actions_agent","Future Actions and Forward-Looking Indicators"),("competitive_pugh_matrix_agent","Competitive Landscape, Product Moat, and Pugh Matrix"),("quality_evaluation_agent","Strengths, Gaps, Risks, and Differentiation")]
def run_sections(config):
    if config.provider=="offline" and config.depth=="exhaustive": raise RuntimeError("Offline provider cannot generate exhaustive report. Use openai, anthropic, gemini, or perplexity.")
    # Merge your existing provider implementation here. This patched orchestrator enforces Markdown-first flow.
    results=[]
    for agent,title in SECTION_TASKS:
        md=f"## {title}\n\nProvider integration should execute `{agent}` using its agent spec and relevant playbook.\n\nNot found in public sources reviewed.\n"
        results.append(SectionResult(agent,title,md,[]))
    return results
def assemble(config,results,quality=None):
    ref=ReferenceManager(); sections={}; parts=[f"# Exhaustive Vendor Analysis Final Report: {config.vendor} ({config.ticker})\n\n## Title Page and Evidence Methodology\n\nMarkdown-first VendorIQ execution. Agents and playbooks produced Markdown; HTML conversion is final rendering only.\n"]
    for r in results:
        n=ref.replace_urls_with_refs(r.markdown,r.title); parts.append(n); sections[r.title]=n
    parts.append(ref.render_reference_links())
    parts.append(quality or "## Quality Document JSON\n\n```json\n{}\n```\n")
    return "\n---\n".join(parts), len(ref.records), sections
def parse_args():
    p=argparse.ArgumentParser(); p.add_argument("--vendor",required=True); p.add_argument("--ticker",default=""); p.add_argument("--website",default=""); p.add_argument("--provider",default=os.getenv("VENDOR_ANALYSIS_PROVIDER","offline")); p.add_argument("--model",default=os.getenv("VENDOR_ANALYSIS_MODEL","offline-scaffold")); p.add_argument("--competitors",default=""); p.add_argument("--sec-cik",default=""); p.add_argument("--markdown-output",default=str(DEFAULT_MD)); p.add_argument("--html-output",default=str(DEFAULT_HTML)); p.add_argument("--depth",default="exhaustive",choices=["standard","exhaustive"]); p.add_argument("--skip-html",action="store_true"); p.add_argument("--allow-html-on-validation-fail",action="store_true"); a=p.parse_args(); return RunConfig(a.vendor,a.ticker,a.website,a.provider,a.model,a.competitors,a.sec_cik,Path(a.markdown_output).resolve(),Path(a.html_output).resolve(),a.depth,a.skip_html,a.allow_html_on_validation_fail)
def main():
    c=parse_args(); c.markdown_output.parent.mkdir(parents=True,exist_ok=True); c.html_output.parent.mkdir(parents=True,exist_ok=True); results=run_sections(c); draft,refs,sections=assemble(c,results); val=validate_markdown_report(draft,sections,c.depth=="exhaustive"); quality="## Quality Document JSON\n\n```json\n"+json.dumps({"vendor":c.vendor,"ticker":c.ticker,"markdown_first_execution":True,"html_conversion_after_quality_gate_only":True,"validation":val,"generated_at_epoch_seconds":int(time.time())},indent=2)+"\n```\n"; final,refs,sections=assemble(c,results,quality); c.markdown_output.write_text(final,encoding="utf-8"); print(f"Markdown report written to: {c.markdown_output}"); print(f"Markdown quality gate: {val['quality_gate']}")
    if c.skip_html: return 0
    if val['quality_gate']!='PASS' and not c.allow_html_on_validation_fail: print("HTML conversion blocked because Markdown validation failed."); return 2
    c.html_output.write_text(convert_markdown_report_to_self_contained_html(final,f"VendorIQ Report: {c.vendor}"),encoding="utf-8"); print(f"HTML report written to: {c.html_output}"); return 0
if __name__=="__main__": raise SystemExit(main())
