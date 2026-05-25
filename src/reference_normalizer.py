from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict, List
@dataclass
class ReferenceRecord:
    id:int; url:str; section:str
class ReferenceManager:
    URL_PATTERN=re.compile(r"https?://[^\s)\]>",'`]+")
    def __init__(self): self.url_to_id:Dict[str,int]={}; self.records:List[ReferenceRecord]=[]
    @staticmethod
    def clean_url(url:str)->str: return url.rstrip(".,;:)")
    def register(self,url:str,section:str)->str:
        u=self.clean_url(url)
        if u not in self.url_to_id:
            self.url_to_id[u]=len(self.records)+1; self.records.append(ReferenceRecord(self.url_to_id[u],u,section))
        return f"[{self.url_to_id[u]}]"
    def replace_urls_with_refs(self,markdown:str,section:str)->str: return self.URL_PATTERN.sub(lambda m:self.register(m.group(0),section), markdown)
    def render_reference_links(self)->str:
        if not self.records: return "## Reference Links\n\n- No URLs detected. Rerun with a web-enabled provider."
        return "## Reference Links\n\n"+"\n".join(f"[{r.id}] {r.url} — {r.section}" for r in self.records)
