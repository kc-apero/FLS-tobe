#!/usr/bin/env python3
"""Sinh AP Voi FLS v3.1.2 — bản vá CHỈ TRỎ ("ISP correction only", apr-build-ap §A.30).

Người dùng 16/11, sau khi đọc so sánh mã ↔ ISP: *"Chọn A. Sau khi chạy xong thì agent FE sẽ nhận
job từ agents BE"*. Đó là sửa ISP, ⛔ sửa AP — nhưng §A.30 cấm ISP chạy trước AP: một lần sửa
chỉ-ISP phải kéo theo một bản vá AP chỉ đổi con trỏ, để cặp AP ↔ ISP vẫn cùng một số.

⭐ Cách làm: đọc NGUYÊN tệp v3.1.1 đã đóng băng, chỉ đổi phần ĐẦU TRANG (nằm trên mọi heading
⇒ ⛔ thuộc thân đơn vị nào). CHỨNG MINH: 0 đơn vị đổi thân, 64/64 vẫn `approved` với băm cũ
khớp (Đ5: mong = tập RỖNG; khác ⇒ ĐỎ).
"""
from __future__ import annotations

import glob
import importlib.util
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
TRUOC = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.1_Duyet_2026-11-16.html"
RA = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html"
NGAY = "2026-11-16"
MONG_DOI_THAN: set[str] = set()      # bản vá chỉ trỏ: ⛔ đơn vị nào đổi thân


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


def trang() -> str:
    s = TRUOC.read_text(encoding="utf-8")
    s = thay(s, "<!-- AP_FLS-Voi_v3.1.1_Duyet_2026-11-16.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v311.py · v3.1.0 đóng băng -->",
             "<!-- AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v312.py · v3.1.1 đóng băng -->")
    s = thay(s, '<meta name="ap:version" content="3.1.1">', '<meta name="ap:version" content="3.1.2">')
    s = thay(s, "<title>AP Voi FLS v3.1.1</title>", "<title>AP Voi FLS v3.1.2</title>")
    s = thay(s, "<h1>AP · Voi FLS v3.1.1 — ", "<h1>AP · Voi FLS v3.1.2 — ")
    s = thay(s, f"<tr><th>Version</th><td>3.1.1 · {NGAY}</td></tr>", f"<tr><th>Version</th><td>3.1.2 · {NGAY}</td></tr>")
    s = thay(s, "trước khi merge vào main (ISP 3.1.1 · quyết định O6).", "trước khi merge vào main (ISP 3.1.2 · quyết định O6).")
    cu = re.search(r"<tr><th>Changes in v3\.1\.1</th><td>(.*?)</td></tr>", s, re.S)
    if not cu:
        raise SystemExit("⛔ không thấy dòng Changes in v3.1.1")
    moi = ("<tr><th>Changes in v3.1.2</th><td>Patch · <b>ISP correction only</b> (§A.30) — ⛔ đổi mục nào, 64/64 vẫn "
           "<code>approved · 2026-11-16</code> với băm cũ. Lý do: ISP sửa theo so sánh mã ↔ ISP (người dùng chọn phương án A: "
           "cổng HD1/HD2 vào <code>GET /gates</code> + màn F03 thay màn F09; agent FE nhận bước BE khi hết bước FE sẵn sàng). "
           "Bản ISP cùng số: <code>IncrementalStepPlan-FLS-Voi_v3.1.2.md</code>.</td></tr>")
    s = thay(s, cu.group(0), moi)
    lich = re.search(r'(<details><summary><b>)9 sửa đổi trước đó(</b> — )v2 → v3\.1\.0(</summary><table style="margin-top:8px">)', s)
    if not lich:
        raise SystemExit("⛔ không thấy khối lịch sử sửa đổi")
    s = thay(s, lich.group(0), f"{lich.group(1)}10 sửa đổi trước đó{lich.group(2)}v2 → v3.1.1{lich.group(3)}"
             f'<tr><th style="white-space:nowrap;vertical-align:top">v3.1.1</th><td>{NGAY} · {cu.group(1)}</td></tr>')
    return s


def chung_minh(s: str) -> int:
    base = {u["id"]: u["live"] for u in APC.units(TRUOC.read_text(encoding="utf-8")) if u["id"]}
    cur = {u["id"]: u for u in APC.units(s) if u["id"]}
    doi = {i for i in set(cur) & set(base) if cur[i]["live"] != base[i]}
    lech_bam = sorted(i for i, u in cur.items() if u["hash"] != u["live"])
    chua = sorted(i for i, u in cur.items() if u["st"] != "approved")
    print(f"  đơn vị {len(cur)} · đổi thân {sorted(doi)} · băm lệch {lech_bam} · chưa approved {chua}")
    if doi != MONG_DOI_THAN or lech_bam or chua or set(cur) != set(base):
        print("  ⛔ ĐỎ — bản vá chỉ trỏ mà chạm thân đơn vị / trạng thái")
        return 1
    print("  ✅ 0 đơn vị đổi thân · 64/64 approved, băm khớp")
    return 0


def main() -> int:
    s = trang()
    if chung_minh(s):
        return 1
    if "--kho" in sys.argv:
        return 0
    RA.write_text(s, encoding="utf-8")
    print(f"✅ đã ghi {RA.relative_to(GOC)} · {len(s):,} byte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
