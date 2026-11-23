#!/usr/bin/env python3
"""Sinh AP Voi FLS v3.1.1 — bản VÁ CHỈ GHI NHẬN DUYỆT (patch: ⛔ đổi số mục, ⛔ thêm nội dung).

Người dùng phiên 16/11/2026: *"Duyệt AP, đồng ý với các recommendation. Tôi duyệt ISP rồi mới triển khai."*

⭐ Cách làm: đọc NGUYÊN tệp v3.1.0 đã đóng băng (⛔ sinh lại cả chuỗi v2.5 → v3.0 → v3.1 — sinh lại
có thể trôi theo dữ liệu đo mới, mà bản duyệt phải đúng là bản người dùng đã đọc), rồi:
   1. 15 nhãn `RECOMMENDED` → `DECIDED · 2026-11-16` (§2.1.1 · §2.1.2 · §3.5.3 · §5.5) — đúng phương án đề xuất.
   2. §3.5.3 · §5.5: thêm MỘT câu "đã chốt 16/11" sau "Owner chốt — tác giả ⛔ tự chốt."
   3. Mọi đơn vị → `approved` · ngày 2026-11-16 · băm lại; dựng lại chỉ mục còn nợ (→ 0).
   4. Đầu trang: Version · Status · dòng `Changes in v3.1.1`; dòng v3.1.0 gấp vào lịch sử.
   5. CHỨNG MINH chỉ những đơn vị trên đổi thân (§A.16) — khác danh sách mong ⇒ ĐỎ, cả hai chiều (Đ5).

⛔ Ngày đóng dấu cố định `NGAY` — ⛔ dùng `--stamp` của ap-status-check (nó lấy ngày đồng hồ máy).
"""
from __future__ import annotations

import glob
import importlib.util
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
TRUOC = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.0_How-Done-Acceptance_2026-11-16.html"
RA = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.1_Duyet_2026-11-16.html"
NGAY = "2026-11-16"

# Đơn vị được phép đổi THÂN — khai trước (Đ5). s1-4-1 mang bảng đếm theo trạng thái,
# s1-4-2 là chỉ mục còn nợ: cả hai do máy dựng lại từ trạng thái nên PHẢI đổi.
MONG_DOI_THAN = {"s2-1-1", "s2-1-2", "c3-5-3", "s5-5", "s1-4-1", "s1-4-2"}
MONG_SO_NHAN = 15


def _apc():
    p = glob.glob(str(Path.home() / ".claude/skills/synced/*/apr-build-ap/references/ap-status-check.py"))
    if len(p) != 1:
        raise SystemExit(f"⛔ tìm thấy {len(p)} bản ap-status-check.py (mong đúng 1)")
    s = importlib.util.spec_from_file_location("apc", p[0])
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


APC = _apc()


def thay(s: str, a: str, b: str, n: int = 1) -> str:
    k = s.count(a)
    if k != n:
        raise SystemExit(f"⛔ chuỗi gặp {k} lần (mong {n}): {a[:90]!r}")
    return s.replace(a, b)


def dong_dau(s: str, ids: set[str] | None = None) -> str:
    """Đặt approved + ngày cố định + băm sống cho các đơn vị (mặc định: tất cả)."""
    for u in sorted(APC.units(s), key=lambda x: -x["m"].start()):
        if not u["id"] or (ids is not None and u["id"] not in ids):
            continue
        a = re.sub(r'\s*data-st(-on|-hash|-inherited)?="[^"]*"', "", u["attrs"])
        a += f' data-st="approved" data-st-on="{NGAY}" data-st-hash="{u["live"]}"'
        if u["inherited"]:
            a += f' data-st-inherited="{u["inh_from"]}"'
        m = u["m"]
        s = s[:m.start()] + f'<h{u["lvl"]}{a}>{m.group(3)}</h{u["lvl"]}>' + s[m.end():]
    return s


def trang() -> str:
    s = TRUOC.read_text(encoding="utf-8")
    # 1 · phiên bản
    s = thay(s, "<!-- AP_FLS-Voi_v3.1.0_How-Done-Acceptance_2026-11-16.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v31.py · v3.0.0 đóng băng -->",
             "<!-- AP_FLS-Voi_v3.1.1_Duyet_2026-11-16.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v311.py · v3.1.0 đóng băng -->")
    s = thay(s, '<meta name="ap:version" content="3.1.0">', '<meta name="ap:version" content="3.1.1">')
    s = thay(s, "<title>AP Voi FLS v3.1.0</title>", "<title>AP Voi FLS v3.1.1</title>")
    s = thay(s, "<h1>AP · Voi FLS v3.1.0 — ", "<h1>AP · Voi FLS v3.1.1 — ")
    s = thay(s, "<tr><th>Version</th><td>3.1.0 · 2026-11-16</td></tr>", f"<tr><th>Version</th><td>3.1.1 · {NGAY}</td></tr>")
    s = thay(s, '<tr><th>Status</th><td><span class="badge tbd">DRAFT</span> mọi mục là <code>draft</code> hoặc <code>review</code>; chỉ owner đặt <code>approved</code> (§1.4).</td></tr>',
             f'<tr><th>Status</th><td><span class="badge built">APPROVED · {NGAY}</span> mọi mục <code>approved</code> — người dùng phiên '
             'duyệt 16/11 kèm <i>"đồng ý với các recommendation"</i>. Owner <b>ThuongCT</b> ký xác nhận trước khi merge vào main '
             '(ISP 3.1.1 · quyết định O6).</td></tr>')
    # 2 · changelog: một dòng mở + dòng cũ gấp vào lịch sử (§A.18)
    cu = re.search(r"<tr><th>Changes in v3\.1\.0</th><td>(.*?)</td></tr>", s, re.S)
    if not cu:
        raise SystemExit("⛔ không thấy dòng Changes in v3.1.0")
    moi = ("<tr><th>Changes in v3.1.1</th><td>Patch · <b>chỉ ghi nhận duyệt</b> (⛔ đổi số mục, ⛔ thêm nội dung). Mọi mục → "
           f"<code>approved · {NGAY}</code>; 15 nhãn RECOMMENDED → DECIDED đúng phương án đề xuất ở §2.1.1 · §2.1.2 · §3.5.3 (D1–D5) · §5.5 (Q1–Q6); "
           "§3.5.3 · §5.5 thêm một câu \"đã chốt\". Chỉ mục còn nợ §1.4.2 → 0. Bản ISP cùng số: "
           "<code>IncrementalStepPlan-FLS-Voi_v3.1.1.md</code>.</td></tr>")
    s = thay(s, cu.group(0), moi)
    lich = re.search(r'(<details><summary><b>)8 sửa đổi trước đó(</b> — )v2 → v3\.0\.0(</summary><table style="margin-top:8px">)', s)
    if not lich:
        raise SystemExit("⛔ không thấy khối lịch sử sửa đổi")
    s = thay(s, lich.group(0), f"{lich.group(1)}9 sửa đổi trước đó{lich.group(2)}v2 → v3.1.0{lich.group(3)}"
             f'<tr><th style="white-space:nowrap;vertical-align:top">v3.1.0</th><td>2026-11-16 · {cu.group(1)}</td></tr>')
    # 3 · RECOMMENDED → DECIDED
    nhan = '<span class="badge new">RECOMMENDED</span>'
    if s.count(nhan) != MONG_SO_NHAN:
        raise SystemExit(f"⛔ {s.count(nhan)} nhãn RECOMMENDED (mong {MONG_SO_NHAN})")
    s = thay(s, nhan + " owner chọn — đề xuất A", f'<span class="badge built">DECIDED · {NGAY}</span> A (owner theo đề xuất)')
    s = s.replace(nhan, f'<span class="badge built">DECIDED · {NGAY}</span>')
    s = thay(s, "Owner chốt — tác giả ⛔ tự chốt.",
             "Owner chốt — tác giả ⛔ tự chốt. <b>Đã chốt 16/11/2026:</b> theo phương án đề xuất ở mọi câu (v3.1.1).", n=2)
    # 4 · đóng dấu, dựng lại chỉ mục, đóng dấu lại cái chỉ mục vừa đổi — tới khi đứng yên
    s = dong_dau(s)
    for _ in range(4):
        s, _rows = APC.rebuild_index(s, APC.units(s))
        lech = {u["id"] for u in APC.units(s) if u["id"] and u["hash"] != u["live"]}
        if not lech:
            break
        s = dong_dau(s, lech)
    else:
        raise SystemExit("⛔ chỉ mục không đứng yên sau 4 lượt")
    for tag in ("table", "tr", "div", "svg", "details", "ul"):
        a, b = len(re.findall(rf"<{tag}[\s>]", s)), s.count(f"</{tag}>")
        assert a == b, (tag, a, b)
    return s


def chung_minh(s: str) -> int:
    base = {u["id"]: u["live"] for u in APC.units(TRUOC.read_text(encoding="utf-8")) if u["id"]}
    cur = {u["id"]: u for u in APC.units(s) if u["id"]}
    them, bo = sorted(set(cur) - set(base)), sorted(set(base) - set(cur))
    doi = {i for i in set(cur) & set(base) if cur[i]["live"] != base[i]}
    chua_duyet = sorted(i for i, u in cur.items() if u["st"] != "approved")
    print(f"  đơn vị: {len(cur)} · thêm {them} · bỏ {bo} · chưa approved {chua_duyet}")
    print(f"  đổi thân: {sorted(doi)}")
    sai = (them or bo or chua_duyet or doi != MONG_DOI_THAN)
    if sai:
        print(f"  ⛔ ĐỎ — mong đổi thân đúng {sorted(MONG_DOI_THAN)}; thừa {sorted(doi - MONG_DOI_THAN)} · thiếu {sorted(MONG_DOI_THAN - doi)}")
        return 1
    print("  ✅ chỉ các đơn vị đã khai đổi thân; 0 thêm · 0 bỏ · mọi đơn vị approved")
    return 0


def main() -> int:
    s = trang()
    rc = chung_minh(s)
    if rc:
        return rc
    if "--kho" in sys.argv:          # chỉ đo, ⛔ ghi
        return 0
    RA.write_text(s, encoding="utf-8")
    print(f"✅ đã ghi {RA.relative_to(GOC)} · {len(s):,} byte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
