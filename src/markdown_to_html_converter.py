from __future__ import annotations
import html,re
def convert_markdown_report_to_self_contained_html(markdown:str,title:str="VendorIQ Exhaustive Vendor Analysis")->str:
    def esc(s): return html.escape(s)
    body=[]
    for line in markdown.splitlines():
        if line.startswith("#"):
            level=len(line)-len(line.lstrip("#")); text=line[level:].strip(); slug=re.sub(r"[^a-z0-9]+","-",text.lower()).strip("-"); body.append(f'<section class="report-section" id="{slug}"><h{min(level,6)}>{esc(text)}</h{min(level,6)}>')
        elif line.startswith("|"):
            body.append(f'<pre class="md-table">{esc(line)}</pre>')
        elif line.strip():
            txt=esc(line); txt=re.sub(r"\[(\d+)\]",r'<a href="#ref-\1">[\1]</a>',txt); body.append(f"<p>{txt}</p>")
    items=[]
    for m in re.finditer(r"^#{1,3}\s+(.+)$", markdown, re.M):
        text=m.group(1); slug=re.sub(r"[^a-z0-9]+","-",text.lower()).strip("-"); items.append(f'<li><a href="#{slug}">{esc(text)}</a></li>')
    toc="".join(items)
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+esc(title)+'</title><style>body{font-family:Arial;margin:0;background:#f7f8fb;color:#111827}header{position:sticky;top:0;background:#102a43;color:white;padding:16px}.layout{display:grid;grid-template-columns:300px 1fr;gap:20px;padding:20px}nav,main{background:white;border:1px solid #ddd;border-radius:12px;padding:16px}pre{white-space:pre-wrap;background:#f3f4f6;padding:8px}@media(max-width:900px){.layout{grid-template-columns:1fr}}</style></head><body><header><h1>'+esc(title)+'</h1><input id="q" placeholder="Search"></header><div class="layout"><nav><ol>'+toc+'</ol></nav><main id="r">'+"".join(body)+'</main></div><script>q.oninput=()=>{let v=q.value.toLowerCase();document.querySelectorAll(".report-section").forEach(s=>s.style.display=s.innerText.toLowerCase().includes(v)?"":"none")}</script></body></html>'
