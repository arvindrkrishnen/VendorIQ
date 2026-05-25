from __future__ import annotations

import html
import json
import re
from typing import Any, Dict, List


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def _esc(text: Any) -> str:
    return html.escape("" if text is None else str(text))


def _inline(text: str) -> str:
    escaped = _esc(text)
    escaped = re.sub(r"\[(\d+)\]", r'<a class="citation" href="#ref-\1">[\1]</a>', escaped)
    escaped = re.sub(r"(https?://[^\s<]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', escaped)
    return escaped


def _render_table(lines: List[str]) -> str:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.match(r"^:?-{3,}:?$", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    thead = "".join(f"<th>{_inline(cell)}</th>" for cell in header)
    tbody = "".join("<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in row) + "</tr>" for row in body)
    return f'<div class="table-wrap"><table class="sortable"><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>'


def _render_chart(chart: Dict[str, Any]) -> str:
    title = chart.get("title", "VendorIQ chart")
    series = chart.get("series", []) or []
    points = []
    for s in series:
        for p in s.get("points", []) or []:
            y = p.get("y")
            if isinstance(y, (int, float)):
                points.append(float(y))
    if not points:
        return f'<figure class="chart"><figcaption>{_esc(title)}</figcaption><p>Chart data was not found in public sources reviewed.</p></figure>'
    min_y = min(points)
    max_y = max(points)
    if min_y == max_y:
        min_y -= 1
        max_y += 1
    width, height = 860, 320
    left, right, top, bottom = 70, 30, 34, 58
    plot_w = width - left - right
    plot_h = height - top - bottom
    palette = ["#2563eb", "#059669", "#dc2626", "#7c3aed", "#ea580c"]

    svg_parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{_esc(title)}">']
    svg_parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" rx="14" fill="#ffffff"></rect>')
    svg_parts.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#9ca3af"></line>')
    svg_parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#9ca3af"></line>')
    svg_parts.append(f'<text x="{left}" y="22" font-size="14" font-weight="700">{_esc(title)}</text>')
    svg_parts.append(f'<text x="12" y="{top}" font-size="11">{_esc(max_y)}</text>')
    svg_parts.append(f'<text x="12" y="{top + plot_h}" font-size="11">{_esc(min_y)}</text>')

    for idx, s in enumerate(series):
        valid = [p for p in (s.get("points", []) or []) if isinstance(p.get("y"), (int, float))]
        if not valid:
            continue
        step = plot_w / max(1, len(valid) - 1)
        poly = []
        for i, p in enumerate(valid):
            x = left + i * step
            y = top + plot_h - ((float(p["y"]) - min_y) / (max_y - min_y) * plot_h)
            poly.append(f"{x:.2f},{y:.2f}")
            if i in (0, len(valid) - 1):
                svg_parts.append(f'<text x="{x:.2f}" y="{top + plot_h + 18}" font-size="10" text-anchor="middle">{_esc(p.get("x", ""))}</text>')
        color = palette[idx % len(palette)]
        svg_parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{" ".join(poly)}"></polyline>')
        svg_parts.append(f'<text x="{left + 12}" y="{top + 22 + idx * 18}" font-size="12" fill="{color}">■ {_esc(s.get("name", "Series"))}</text>')
    svg_parts.append("</svg>")
    return f'<figure class="chart"><div class="chart-svg">{"".join(svg_parts)}</div></figure>'


def convert_markdown_report_to_self_contained_html(markdown: str, title: str = "VendorIQ Exhaustive Vendor Analysis") -> str:
    blocks: List[str] = []
    lines = markdown.splitlines()
    toc: List[str] = []
    i = 0
    section_open = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("```vendoriq_chart"):
            json_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                json_lines.append(lines[i])
                i += 1
            try:
                blocks.append(_render_chart(json.loads("\n".join(json_lines))))
            except Exception as exc:
                blocks.append(f'<pre class="code">Invalid chart block: {_esc(exc)}</pre>')
        elif line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append(f'<pre class="code">{_esc("\n".join(code_lines))}</pre>')
        elif line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            i -= 1
            blocks.append(_render_table(table_lines))
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            slug = _slug(text)
            if level <= 2:
                if section_open:
                    blocks.append("</div></section>")
                blocks.append(f'<section class="report-section" id="{slug}"><button class="section-toggle" aria-expanded="true">Collapse</button><h{min(level,6)}>{_esc(text)}</h{min(level,6)}><div class="section-body">')
                section_open = True
                toc.append(f'<li><a href="#{slug}">{_esc(text)}</a></li>')
            else:
                blocks.append(f'<h{min(level,6)}>{_esc(text)}</h{min(level,6)}>')
                toc.append(f'<li class="toc-sub"><a href="#{slug}">{_esc(text)}</a></li>')
        elif line.strip().startswith("-"):
            items = []
            while i < len(lines) and lines[i].strip().startswith("-"):
                items.append(lines[i].strip()[1:].strip())
                i += 1
            i -= 1
            blocks.append("<ul>" + "".join(f"<li>{_inline(item)}</li>" for item in items) + "</ul>")
        elif line.strip():
            blocks.append(f"<p>{_inline(line.strip())}</p>")
        i += 1
    if section_open:
        blocks.append("</div></section>")

    css = """
:root{--bg:#f7f8fb;--ink:#111827;--muted:#6b7280;--card:#fff;--line:#d1d5db;--brand:#102a43;--accent:#2563eb}
*{box-sizing:border-box}body{font-family:Arial,Helvetica,sans-serif;margin:0;background:var(--bg);color:var(--ink);line-height:1.55}header{position:sticky;top:0;z-index:20;background:var(--brand);color:#fff;padding:16px 20px;box-shadow:0 4px 18px rgba(0,0,0,.18)}header h1{margin:0 0 12px;font-size:22px}.toolbar{display:flex;gap:8px;flex-wrap:wrap}input,button{border-radius:10px;border:1px solid var(--line);padding:9px 11px;font-size:14px}button{cursor:pointer;background:#fff}#q{min-width:280px;flex:1}.layout{display:grid;grid-template-columns:320px 1fr;gap:20px;padding:20px}nav,main{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:0 10px 28px rgba(17,24,39,.06)}nav{position:sticky;top:104px;align-self:start;max-height:calc(100vh - 130px);overflow:auto}nav ol{padding-left:22px}nav a{color:var(--brand);text-decoration:none}.toc-sub{font-size:13px;color:var(--muted)}.report-section{border:1px solid var(--line);border-radius:16px;margin:0 0 18px;padding:16px;background:#fff;position:relative}.section-toggle{position:absolute;right:14px;top:14px}.report-section h1,.report-section h2{padding-right:100px}.collapsed .section-body{display:none}.collapsed .section-toggle::after{content:""}.table-wrap{overflow:auto;margin:14px 0}table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid var(--line);padding:8px;vertical-align:top}th{background:#eef2ff;text-align:left;cursor:pointer}tr:nth-child(even) td{background:#fafafa}.citation{font-weight:700;color:var(--accent)}.chart{border:1px solid var(--line);border-radius:16px;padding:12px;background:#fff;margin:16px 0}.chart-svg{width:100%;overflow:auto}.code,pre{white-space:pre-wrap;background:#f3f4f6;border-radius:12px;padding:12px;overflow:auto}a{color:var(--accent)}@media(max-width:950px){.layout{grid-template-columns:1fr}nav{position:relative;top:0;max-height:none}}@media print{header,nav,.section-toggle,.toolbar{display:none}.layout{display:block;padding:0}main{border:0;box-shadow:none}.report-section{break-inside:avoid}}
"""
    js = """
const q=document.getElementById('q');
q.addEventListener('input',()=>{const v=q.value.toLowerCase();document.querySelectorAll('.report-section').forEach(s=>{s.style.display=s.innerText.toLowerCase().includes(v)?'':'none';});});
document.getElementById('expandAll').onclick=()=>document.querySelectorAll('.report-section').forEach(s=>{s.classList.remove('collapsed');s.querySelector('.section-toggle').textContent='Collapse';});
document.getElementById('collapseAll').onclick=()=>document.querySelectorAll('.report-section').forEach(s=>{s.classList.add('collapsed');s.querySelector('.section-toggle').textContent='Expand';});
document.querySelectorAll('.section-toggle').forEach(b=>b.onclick=()=>{const s=b.closest('.report-section');s.classList.toggle('collapsed');b.textContent=s.classList.contains('collapsed')?'Expand':'Collapse';});
document.querySelectorAll('table.sortable th').forEach((th,idx)=>th.addEventListener('click',()=>{const table=th.closest('table');const rows=[...table.querySelectorAll('tbody tr')];const asc=th.dataset.asc!=='true';rows.sort((a,b)=>{const av=a.children[idx]?.innerText.trim()||'';const bv=b.children[idx]?.innerText.trim()||'';const an=parseFloat(av.replace(/[$,%B,M,]/g,''));const bn=parseFloat(bv.replace(/[$,%B,M,]/g,''));if(!Number.isNaN(an)&&!Number.isNaN(bn))return asc?an-bn:bn-an;return asc?av.localeCompare(bv):bv.localeCompare(av);});th.dataset.asc=asc;rows.forEach(r=>table.querySelector('tbody').appendChild(r));}));
"""
    return f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>{_esc(title)}</title><style>{css}</style></head><body><header><h1>{_esc(title)}</h1><div class=\"toolbar\"><input id=\"q\" placeholder=\"Search sections\" aria-label=\"Search sections\"><button id=\"expandAll\">Expand all</button><button id=\"collapseAll\">Collapse all</button><button onclick=\"window.print()\">Print</button></div></header><div class=\"layout\"><nav aria-label=\"Table of contents\"><h2>Contents</h2><ol>{''.join(toc)}</ol></nav><main id=\"report\">{''.join(blocks)}</main></div><script>{js}</script></body></html>"
