"""Khuôn đóng băng `noem_com_cdt` — ĐẦU VÀO của dòng PL5 khối CDT: COM theo từng nhóm `NOEM` *(hàng `18…26` của tab
`[2025][RPT] NOEM PL & COM`)* × 12 tháng 2025 *(ISP 3.1.2 · DT13 · `WO-319` · `BG-308` §"Cần ảnh COM theo CDT1")*.

    python tools/dong_bang_sheet.py noem_com_cdt <bản_thô.json> --mong 9
        ⇒ tests/fixture/dau_vao/noem_com_cdt.json

⭐ **Vì sao.** Ô PL5 của khối CDT ở ATL *(`Report I PLA3 Y H Q M | PM + HR | ATL`, `FORMULA` đo 22/11, cột `AG`)* là
`=sumifs('[2025][RPT] NOEM PL & COM'!F$18:F$26, …!$A$18:$A$26, left(A<mở khối>,3)) / SUMIFS('9.2.Exchange Rate'!$B:$B, …!$H:$H,
 DATE(AG$5,AG$6,1)) / 10^6 * -1 + <PL4>` ⇒ **PL5 = PL4 − COM(nhóm `left(nhãn khối,3)`) ÷ USD ÷ 10⁶** — cùng phép như `GAG` của
`noem_com_gag` nhưng nhóm là `CVL · COR · SHQ · CSM · CAH · ASA` *(SHQ = HAI hàng `SHQ1` + `SHQ2` cùng mã A — `SUMIFS` cộng cả hai)*.
`noem_com_gag` *(DT C12)* chỉ giữ hàng `GAG` ⇒ **252** ô PL5 ngoài mẫu số *(BG-308)*; khuôn này đóng băng 9 hàng `18…26`.
Tái dùng hằng của `noem_com_gag` *(`THANG_MONG` · `_u`)* — ⛔ chép; ⛔ sửa `noem_com_gag.py`.

⛔ **Bản đồ cột bằng tiêu đề TRƯỚC**: hàng 2 `F:Q` = `2025` × 12 · hàng 3 `F:Q` = `1…12` *(đo 22/11)*; `A` mã nhóm · `B` nhãn tổ chức
*(`GAG I Apero Group`, `SHQ1_Headquarters1`, … — ⛔ PII: 0 tên người, 0 số TK; tab này **dán GIÁ TRỊ** — 0 công thức ở `F18:Q26`)*.
⛔ cột `R` *(2026-01, `#N/A`)* · các cột sau `Q`. Hợp đồng bản thô *(phiên cloud, khoá SA chỉ-đọc, ⛔ commit)*:
`{nguon, doc_luc, cach_doc, nam, thang, values}`; `values` = 9 hàng `[hàng_sheet, A, B, F…Q]` *(⛔ hàng nào khác của tab)*.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "noem_com_gag.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang_noem_com_gag", _P)
_g = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _g
    _spec.loader.exec_module(_g)

BANG = "NOEM.COM.CDT"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
THANG_MONG = _g.THANG_MONG
COT = ("ma", "nhan", *[f"m{m:02d}" for m in range(1, 13)])
KIEU_COT = {"ma": "chu", "nhan": "chu", **{c: "so!" for c in COT[2:]}}
LOI_MONG = {c: 0 for c in COT[2:]}             # Đ5: mong 0 ô lỗi ở 12 cột tháng
RA = "tests/fixture/dau_vao/noem_com_cdt.json"
PHU_MONG: dict[str, int] = {}

#: ⭐ Đ5 — đo 22/11 rồi khai: hàng sheet → (mã A, nhãn B). Thứ tự = thứ tự hàng; `SHQ` xuất hiện HAI lần *(SHQ1 · SHQ2)*.
NHAN_MONG = {18: ("GAG", "GAG I Apero Group"), 19: ("SHQ", "SHQ1_Headquarters1"), 20: ("SHQ", "SHQ2_Headquarters2"),
             21: ("COR", "COR_Terasofts"), 22: ("CVL", "CVL_VisionLab"), 23: ("CSM", "CSM_SuperMinds"),
             24: ("CAH", "CAH_Astronex"), 25: ("ASA", "ASA_Super App (IOs)"), 26: ("CMN", "CMN_Management")}


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    nam, thang, V = tho.get("nam"), tho.get("thang"), tho.get("values")
    if not (isinstance(nam, list) and isinstance(thang, list) and len(nam) == len(thang) == 12):
        raise ValueError("`nam` · `thang` phải danh sách đúng 12 ô *(F:Q)*")
    if [int(x) for x in nam] != [2025] * 12 or [int(x) for x in thang] != list(range(1, 13)):
        raise ValueError("hàng tiêu đề F:Q phải đúng 2025 × 12 và tháng 1…12")
    if not isinstance(V, list) or len(V) != len(NHAN_MONG) or any(not (isinstance(h, list) and len(h) == 3 + 12) for h in V):
        raise ValueError(f"`values` phải ĐÚNG {len(NHAN_MONG)} hàng `[hàng, A, B, F…Q]` *(⛔ hàng khác của tab)*")
    dong = []
    for h in V:
        hs, a, b, *so = h
        if NHAN_MONG.get(hs) != (a, b):
            raise ValueError(f"hàng {hs}: nhãn `A·B` ⛔ đúng bản đo *(giá trị ⛔ in)*")
        dong.append([hs, a, b, *so])
    return {"cot": [KHOA, *COT], "dong": dong,
            "ghi_chu": ("COM theo nhóm NOEM (VND, dấu của tab: dương = chi phí) — 9 hàng 18…26 × 12 tháng 2025 (F:Q) của "
                        "`[2025][RPT] NOEM PL & COM` sổ ATL; ô PL5 khối CDT: PL5 = PL4 − COM(left(nhãn khối,3)) / USD / 10^6. "
                        "`SHQ` ở HAI hàng (SHQ1, SHQ2) — SUMIFS cộng cả hai. ⛔ cột R (2026-01) · ⛔ hàng khác.")}


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5 hai chiều)*. Tập rỗng ⇒ `ValueError` *(Đ3)*; hàng thiếu/thừa, ô lỗi/chữ ⇒ `thieu`; **mọi 9×12 ô = 0 ⇒ ĐỎ**."""
    if not dong:
        raise ValueError("0 dòng COM — mẫu số 0, ⛔ nền xanh (Đ3)")
    thieu: list[str] = []
    co = {int(d["dong_sheet"]): d for d in dong}
    thieu += [f"hang_thieu@{h}" for h in NHAN_MONG if h not in co]
    thieu += [f"hang_thua@{h}" for h in sorted(co) if h not in NHAN_MONG]
    khac0 = tong = 0
    for h, d in co.items():
        for c in COT[2:]:
            v = d[c]
            if isinstance(v, dict) or v is None:
                thieu.append(f"o_loi_hoac_rong@{h}:{c}")
            else:
                tong += 1
                khac0 += float(v) != 0
    if not thieu and khac0 == 0:
        raise ValueError(f"{tong}/{tong} ô COM = 0 — ⛔ chứng minh được gì (Đ3: mẫu số khác 0 mới đo)")
    return {"thieu": thieu, "lac": [],
            "dai": f"{len(dong)} hàng × 12 tháng {THANG_MONG[0]}→{THANG_MONG[-1]} · ô số {tong} · ≠ 0: {khac0}"}
