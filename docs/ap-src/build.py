# -*- coding: utf-8 -*-
"""Dựng AP FLS v1.0.0 → FLS/docs/architecturepack_FLS_v1.0.0_current-state_2026-09-17.html"""
import sys, re, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from apgen import Doc
import c_s0, c_s1, c_s2, c_s3, c_s4, c_s5, c_s6, c_s7, c_s8, c_s9_13

OUT = r"C:\Users\0_Apero Project\FLS\docs\architecturepack_FLS_v1.0.0_current-state_2026-09-17.html"

doc = Doc(
    title="Architecture Pack — FLS — V1.0",
    bar_sub="FLS · ITL — Input Transaction Ledger · current-state · 2026-09-17",
    h1='Architecture Pack — FLS — V1.0 <span class="badge tbd">DRAFT</span>',
    header_rows=c_s0.HEADER_ROWS,
    date="2026-09-17",
)
for m in (c_s0, c_s1, c_s2, c_s3, c_s4, c_s5, c_s6, c_s7, c_s8, c_s9_13):
    doc.add(*m.sections())

n = doc.write(OUT)
print("written", n, "bytes ->", OUT)

# --- structural gates ---
html = open(OUT, encoding="utf-8").read()
css = html[html.find("<style"):html.find("</style>")]
body = html[html.find("<main>"):]
used = {c for m in re.finditer(r'class="([^"]+)"', body) for c in m.group(1).split()}
defined = set(re.findall(r'\.([A-Za-z][\w-]*)', css))
missing = sorted(used - defined - {"mermaid"})
print("CSS classes used but undefined:", missing)
for tag in ["table", "tr", "td", "th", "div", "details", "ul", "ol", "li", "h2", "h3", "h4", "pre", "span", "code", "kbd", "p"]:
    o = len(re.findall(rf"<{tag}\b[^>]*>", body)); c = body.count(f"</{tag}>")
    if o != c:
        print(f"TAG BALANCE {tag}: {o} vs {c}")
# colgroup sums
bad = []
for m in re.finditer(r"<colgroup>(.*?)</colgroup>", body):
    s = sum(int(x) for x in re.findall(r"width:(\d+)%", m.group(1)))
    if abs(s - 100) > 1:
        bad.append(s)
print("colgroups off 100:", bad)
# headings count
print("h2/h3/h4:", body.count("<h2 "), body.count("<h3 "), body.count("<h4 "))
