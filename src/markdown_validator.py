from __future__ import annotations
import re
REQUIRED_SECTIONS=["Reference Links","Quality Document JSON","Competitive Landscape, Product Moat, and Pugh Matrix","Product-by-Product Technology and Architecture Due Diligence","SEC Filing Scan in Bulleted Format"]
def word_count(t:str)->int: return len(re.findall(r"\b\w+\b", re.sub(r"\|.*\|"," ",t)))
def count_markdown_tables(md:str)->int: return len(re.findall(r"\n\|.+\|\n\|[-:\s|]+\|",md))
def validate_markdown_report(markdown:str, section_markdown:dict|None=None, exhaustive:bool=True)->dict:
    missing=[s for s in REQUIRED_SECTIONS if s.lower() not in markdown.lower()]
    refs=set(re.findall(r"\[(\d+)\]",markdown)); defs=set(re.findall(r"^\[(\d+)\]\s+https?://",markdown,re.M))
    checks={"required_sections":{"status":"PASS" if not missing else "FAIL","missing":missing},"reference_links":{"status":"PASS" if "Reference Links" in markdown and (not refs or defs) else "FAIL","reference_count":len(defs)},"quality_json_final":{"status":"PASS" if markdown.rfind("Quality Document JSON")>markdown.rfind("Reference Links") else "FAIL"},"markdown_table_count":{"status":"PASS" if count_markdown_tables(markdown)>=5 else "FAIL","count":count_markdown_tables(markdown)}}
    if section_markdown and exhaustive:
        low={k:word_count(v) for k,v in section_markdown.items() if word_count(v)<500 and "not found in public sources reviewed" not in v.lower()}
        checks["minimum_depth"]={"status":"PASS" if not low else "FAIL","sections_below_min_words":low}
    failures=[k for k,v in checks.items() if v.get("status")=="FAIL"]
    return {"quality_gate":"PASS" if not failures else "FAIL","critical_failures":failures,"checks":checks}
