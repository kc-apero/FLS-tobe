# -*- coding: utf-8 -*-
"""apgen.py — bộ sinh Architecture Pack HTML (khuôn FPA-T4 v2.0.0 / build-ap §A.1–§A.18).

Dùng:  from apgen import Doc, S ;  doc = Doc(title=..., ...); doc.add(S(...)); doc.write(path)

- Shell (CSS + script) lấy NGUYÊN VĂN từ AP FPA-T4 (không viết lại CSS).
- Mỗi heading h2–h4 nhận id, data-st, data-st-hash (băm thân), data-st-on.
- Mục con không khai st riêng → kế thừa cha (data-st-inherited).
- §0.B sinh tự động từ marker (đếm trước, rồi rows).
- TOC sinh từ cây mục, có chấm trạng thái.
"""
from __future__ import annotations
import re, hashlib, html as _h
from dataclasses import dataclass, field

FPA = r"C:\Users\0_Apero Project\FPA-T4\docs\architecturepack_FPA-T4_v2.0.0_unified_2026-09-16.html"

def body_hash(body: str) -> str:
    b = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return hashlib.sha256(re.sub(r"\s+", " ", b).strip().encode()).hexdigest()[:8]

@dataclass
class S:
    id: str            # 's1', 's1-2', 's1-2-3', 's0-B'
    title: str         # đã có tiền tố § ; có thể chứa HTML (badge)
    body: str = ""     # HTML thân
    st: str | None = None   # draft/review/approved/locked/superseded — None = kế thừa
    part: str | None = None # nếu là mục đầu của một PART: nhãn part-divider

    @property
    def level(self) -> int:
        return 2 + self.id.count("-")   # s1→h2, s1-2→h3, s1-2-3→h4

    @property
    def plain_title(self) -> str:
        t = re.sub(r"<span class=['\"]badge[^'\"]*['\"]>.*?</span>", "", self.title)  # bỏ huy hiệu khỏi TOC/§0.B
        return _h.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip())

@dataclass
class Doc:
    title: str
    bar_sub: str
    h1: str
    header_rows: list[tuple[str, str]]
    date: str
    sections: list[S] = field(default_factory=list)

    def add(self, *ss: S):
        self.sections.extend(ss)

    # ---------- shell ----------
    def _shell(self):
        h = open(FPA, encoding="utf-8").read()
        head = h[: h.find('<div class="bar">')]
        head = head.replace("<title>Architecture Pack — FPA-T4 — V2.0</title>", f"<title>{_h.escape(self.title)}</title>")
        # thêm CSS phụ trợ cho AP này (không sửa CSS gốc)
        extra = """
/* ===== FLS AP bổ sung ===== */
.erd-wrap{overflow-x:auto;margin:16px 0;border:1px solid var(--line-soft);border-radius:6px;background:#fff;padding:10px}
.erd-wrap svg{display:block;min-width:900px}
table.uf td kbd{white-space:nowrap}
.badge.gate{background:#fee2e2;color:#991b1b}
.badge.machine{background:#e0f2fe;color:#075985}
.num{font-variant-numeric:tabular-nums}
td.c,th.c{text-align:center}
"""
        head = head.replace("\n</style>", extra + "\n</style>", 1)
        tail = h[h.rfind("</main></div>"):]
        return head, tail

    # ---------- state resolution ----------
    def _resolve(self):
        stack: dict[int, S] = {}
        out = []
        for s in self.sections:
            lvl = s.level
            for k in [k for k in stack if k >= lvl]:
                del stack[k]
            parent = stack.get(lvl - 1) or stack.get(lvl - 2)
            if s.st is None:
                st = parent._eff if parent else "draft"
                inh = True
            else:
                st, inh = s.st, False
            s._eff = st  # type: ignore
            s._inh = inh  # type: ignore
            stack[lvl] = s
            out.append(s)
        return out

    # ---------- §0.B ----------
    def _index_body(self, secs):
        from collections import Counter
        cnt = Counter(s._eff for s in secs)
        review = [s for s in secs if s._eff == "review" and s.id != "s0-B" and not s._inh]
        lines = [
            f'\n<p>Đếm trạng thái thoả thuận trên <b>{len(secs)}</b> đơn vị (h2–h4): '
            + " · ".join(f"<code>{k}</code> {v}" for k, v in sorted(cnt.items())) + ".</p>",
            '<p><b>Toàn bộ tài liệu là bản nháp v1.0.0 chưa có chữ ký nào.</b> Mọi đơn vị không ghi riêng đều kế thừa <code>draft</code> của mục cha (thanh mảnh, không tô nền). Bảng dưới liệt kê <b>chỉ</b> những mục đang <code>review</code> — tức mục đặt câu hỏi và chờ chủ sở hữu trả lời (§A.14/§A.15).</p>',
            '<table><thead><tr><th>Mục</th><th>Trạng thái</th></tr></thead><tbody>'
            + "".join(f'<tr><td><a href="#{s.id}">{_h.escape(s.plain_title)}</a></td><td><code>{s._eff}</code></td></tr>' for s in review)
            + '</tbody></table>\n',
            '<p class="note">Cách ký: chủ sở hữu (không phải tác giả) đổi <code>data-st</code> sang <code>approved</code> bằng <code>python docs/ap-status-check.py &lt;file&gt; --stamp s7-2=approved</code>; script ghi lại hash tại thời điểm ký. Sửa chữ dưới thanh xanh sau đó ⇒ checker báo <code>stale-approval</code>.</p>',
        ]
        return "\n".join(lines)

    # ---------- TOC ----------
    def _toc(self, secs):
        # cây: part → l1(h2) → l3(h3) → l3(h4)
        n = len(secs)
        parts = []  # [(label, [h2 nodes])]
        cur_part = None
        nodes = []
        for s in secs:
            if s.part:
                cur_part = {"label": s.part, "kids": []}
                parts.append(cur_part)
            if s.level == 2:
                node = {"s": s, "kids": []}
                cur_part["kids"].append(node)
                nodes.append(node)
            elif s.level == 3:
                node = {"s": s, "kids": []}
                nodes[-1]["kids"].append(node)
            else:
                nodes[-1]["kids"][-1]["kids"].append({"s": s, "kids": []})

        def dot(s):
            inh = " inh" if s._inh else ""
            return f'<i class="stdot st-{s._eff}{inh}" title="{s._eff}"></i>'

        def a(s):
            t = _h.escape(s.plain_title, quote=True)
            return f'<a href="#{s.id}" title="{t}">{dot(s)}<span>{_h.escape(s.plain_title)}</span></a>'

        def li(node, cls):
            s = node["s"]
            if node["kids"]:
                inner = "".join(li(k, "toc-l3") for k in node["kids"])
                return f'<li class="{cls} has-kids"><details><summary>{a(s)}</summary><ul>{inner}</ul></details></li>'
            return f'<li class="{cls}">{a(s)}</li>'

        out = ['<div class="toc-tree"><ul>']
        for p in parts:
            inner = "".join(li(k, "toc-l1") for k in p["kids"])
            out.append(f'<li class="toc-sg"><details open><summary><span class="sg-label">{_h.escape(p["label"])}</span></summary><ul>{inner}</ul></details></li>')
        out.append("</ul></div>")
        return "".join(out), n

    # ---------- render ----------
    def render(self) -> str:
        secs = self._resolve()
        # §0.B thân sinh tự động
        for s in secs:
            if s.id == "s0-B":
                s.body = self._index_body(secs)
        head, tail = self._shell()
        toc, n = self._toc(secs)
        bar = (f'<div class="bar"><b>{_h.escape(self.title)}</b><span class="m">{self.bar_sub}</span>'
               f'<span class="m">{n} mục</span><button id="tg" type="button">Ẩn/hiện mục lục</button>'
               f'<button id="exp" type="button">Mở tất cả</button><button id="col" type="button">Thu gọn</button>'
               f'<input id="q" type="search" placeholder="Lọc mục lục…" aria-label="Lọc mục lục" '
               f'style="font:inherit;background:var(--sunk);color:var(--ink);border:1px solid var(--line);border-radius:5px;padding:5px 10px;min-width:170px"></div>')
        nav = (f'<div class="shell"><nav id="toc" aria-label="Mục lục"><div class="toc-head">Mục lục'
               f'<span class="toc-count">{n} mục</span></div>{toc}</nav><main>\n\n')
        hdr = f'<h1 id="top">{self.h1}</h1>\n<table class="hdr"><tbody>\n'
        hdr += "".join(f"<tr><th>{k}</th><td>{v}</td></tr>\n" for k, v in self.header_rows)
        hdr += "</tbody></table>\n"
        SEP = "<!-- " + "═" * 72 + " -->"
        parts = []
        for s in secs:
            if s.part:
                parts.append(f'\n<h2 class="part-divider">{_h.escape(s.part)}</h2>\n')
            if s.level == 2:
                parts.append(f"\n{SEP}\n")
            attrs = f'id="{s.id}" data-st="{s._eff}"'
            if s._inh:
                attrs += ' data-st-inherited="1"'
            attrs += f' data-st-hash="{body_hash(s.body)}" data-st-on="{self.date}"'
            parts.append(f"<h{s.level} {attrs}>{s.title}</h{s.level}>\n{s.body}\n")
        return head + bar + nav + hdr + "".join(parts) + "\n" + tail

    def write(self, path: str):
        out = self.render()
        open(path, "w", encoding="utf-8").write(out)
        return len(out)

# ---------- tiện ích viết bảng ----------
def T(cols: list[tuple[str, int]], rows: list[list[str]], cls: str = "", rowcls: list[str] | None = None) -> str:
    """cols=[(tên, %)], rows=[[cell,...]]. Tự bọc colgroup + thead."""
    assert abs(sum(w for _, w in cols) - 100) <= 1, ("colgroup != 100", cols)
    cg = "".join(f'<col style="width:{w}%">' for _, w in cols)
    th = "".join(f"<th>{c}</th>" for c, _ in cols)
    body = []
    for i, r in enumerate(rows):
        assert len(r) == len(cols), (len(r), len(cols), r[0][:40])
        rc = f' class="{rowcls[i]}"' if rowcls and rowcls[i] else ""
        body.append(f"<tr{rc}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return (f'<table class="{cls}" style="table-layout:fixed"><colgroup>{cg}</colgroup>'
            f"<thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table>")

def B(kind: str, text: str | None = None) -> str:
    text = text or kind.upper()
    return f'<span class="badge {kind}">{text}</span>'

BUILT = B("built"); PARTIAL = B("partial"); PROPOSED = B("proposed"); SUPERSEDED = B("superseded")

def MER(code: str, cap: str) -> str:
    return (f'<div class="mermaid-wrap"><pre class="mermaid">{_h.escape(code)}</pre></div>\n'
            f'<p class="fig-cap">{cap}</p>')

def OL(items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def UL(items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def P(t): return f"<p>{t}</p>"
def NOTE(t, warn=False): return f'<div class="note{" warn" if warn else ""}">{t}</div>'
def C(t): return f"<code>{t}</code>"
def K(t): return f"<kbd>{t}</kbd>"
