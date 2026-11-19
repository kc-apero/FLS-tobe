"""Khuôn đóng băng `noem_com_gag` — ĐẦU VÀO của dòng PL5: COM cấp nhóm hàng `GAG` *(Apero Group)*
theo tháng 2025 *(ISP 3.1.2 · `C12` vòng sửa sau R2 · `KQ-187` · `C12-R2-01`)*.

    python tools/dong_bang_sheet.py noem_com_gag <bản_thô.json> --mong 12
        ⇒ tests/fixture/dau_vao/noem_com_gag.json

⭐ **Vì sao có khuôn này.** Ô `AG84:AR84` của sheet ATL *(tab `Report I PLA3 Y H Q M | PM + HR | ATL`,
sổ `19NNTbXJ…`, `FORMULA` đo 19/11)* là
`=sumifs('[2025][RPT] NOEM PL & COM'!F$18:F$26, …!$A$18:$A$26, "GAG") / SUMIFS('9.2.Exchange Rate'!$B:$B,
 …!$H:$H, DATE(AG$5,AG$6,1)) / 10^6 * -1 + AG83` ⇒ **PL5 = PL4 − COM_GAG(VND ÷ tỷ giá USD ÷ 10^6)**.
Chủ chốt 19/11: PL5 lấy COM **cấp nhóm `GAG`**, ⛔ `COM Total` dòng 51. Số `GAG` là ĐẦU VÀO có tên
`COM_GAG` — ⛔ hằng gõ cứng trong `DINH_NGHIA`.

Hợp đồng bản thô *(⛔ commit; phiên cloud đọc bằng khoá SA chỉ-đọc)* — ⛔ chỉ đúng HAI nhóm ô:
`{spreadsheet_id, nguon, doc_luc, cach_doc, hang_sheet, nhan, nam, thang, values}`:
  · `nhan` = hai ô `A:B` của hàng `GAG` = `["GAG", "GAG I Apero Group"]` ⇒ khuôn từ chối nếu khác
    *(khoá tìm hàng là CHỮ `GAG` của cột `A`, ⛔ số thứ tự hàng)*.
  · `nam` · `thang` = hàng tiêu đề 2–3 của `F:Q` — phải đúng `2025` × 12 và `1…12`.
  · `values` = **MỘT hàng** 12 ô `F:Q` *(COM theo tháng, VND, dấu của tab — DƯƠNG = chi phí)*.
  ⛔ mang hàng nào khác của tab *(sổ HR/ATL có lương, tên người ở các hàng con)* — chỉ hàng `GAG`.

⭐ **Hai quyết định** *(mỗi cái một con số đo 19/11 — Đ3/Đ4/Đ5)*:
  ① **12 tháng `F:Q` = 202501…202512; cột `R` *(tháng 1/2026, `#N/A`)* ⛔ mang** — ngoài dải `AG:AR`
    của ô PL5. Ô lỗi, nếu có ở `F:Q`, GIỮ NGUYÊN chuỗi *(cột `so!`)* và cổng báo.
  ② **Cổng `thieu_lac`** *(Đ5 hai chiều)*: tháng ≠ đúng 202501…202512 ⇒ `thieu`; ô lỗi/chữ ở `F:Q` ⇒
    `thieu` *(`o_loi@yyyymm`)*; **cả 12 ô = 0 ⇒ ĐỎ** *(Đ3: mẫu số ≠ 0 — một bản sao sổ mà `GAG` toàn 0
    thì ⛔ chứng minh được gì; sổ HR `[COPY]` đo 19/11 ra đúng 12/12 số 0 vì ô là `=sum(F19:F26)` của
    hàng con bị bỏ)*.
"""
from __future__ import annotations

from typing import Any

BANG = "NOEM.COM.GAG"
KHOA = "thang"
KIEU_KHOA = "yyyymm"
COT = ("com_gag_vnd",)
KIEU_COT = {"com_gag_vnd": "so!"}
LOI_MONG = {"com_gag_vnd": 0}                  # Đ5: mong 0 ô lỗi; có ô lỗi ⇒ ĐỎ
RA = "tests/fixture/dau_vao/noem_com_gag.json"

THANG_MONG = tuple(f"2025{m:02d}" for m in range(1, 13))
NHAN_MONG = ["GAG", "GAG I Apero Group"]


def _num(v: Any) -> int:
    return int(v)


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Bản thô 1 hàng × 12 ô → bảng 12 dòng `{thang, com_gag_vnd}`. ⛔ lời lỗi mang giá trị ô."""
    if tho.get("nhan") != NHAN_MONG:
        raise ValueError(f"`nhan` phải đúng {NHAN_MONG} *(hàng GAG tìm theo CHỮ ở cột A)*")
    nam, thang, vals = tho.get("nam"), tho.get("thang"), tho.get("values")
    if not (isinstance(nam, list) and isinstance(thang, list) and len(nam) == len(thang) == 12):
        raise ValueError("`nam` · `thang` phải danh sách đúng 12 ô *(F:Q)*")
    if [_num(x) for x in nam] != [2025] * 12 or [_num(x) for x in thang] != list(range(1, 13)):
        raise ValueError("hàng tiêu đề F:Q phải đúng 2025 × 12 và tháng 1…12")
    if not (isinstance(vals, list) and len(vals) == 1 and isinstance(vals[0], list)
            and len(vals[0]) == 12):
        raise ValueError("`values` phải ĐÚNG MỘT hàng 12 ô *(⛔ mang hàng nào khác)*")
    dong = [[202500 + int(m), v] for m, v in zip(range(1, 13), vals[0])]
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "ghi_chu": (
            f"COM nhóm GAG (Apero Group), VND, dấu của tab (dương = chi phí), 12 tháng 2025 từ "
            f"`[2025][RPT] NOEM PL & COM` hàng {tho.get('hang_sheet')!r} cột F:Q của SỔ ATL. "
            f"Ô PL5 sheet: PL5 = PL4 − COM_GAG/tỷ giá USD/10^6. ⛔ mang cột R (2026-01), ⛔ hàng khác."),
    }


def _u(v: Any) -> Any:
    return v.get("chu") if isinstance(v, dict) else v


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng ② *(Đ5)*. Tập rỗng ⇒ `ValueError` *(Đ3)*; cả 12 ô = 0 ⇒ `ValueError`."""
    if not dong:
        raise ValueError("0 dòng COM_GAG — mẫu số 0, ⛔ nền xanh (Đ3)")
    thieu: list[str] = []
    co = {_u(d["thang"]): d["com_gag_vnd"] for d in dong}
    thieu += [f"thang_thieu@{t}" for t in THANG_MONG if t not in co]
    thieu += [f"thang_thua@{t}" for t in sorted(co) if t not in THANG_MONG]
    khac0 = 0
    for t in THANG_MONG:
        v = co.get(t)
        if isinstance(v, dict):                        # ô chữ/lỗi: giữ nguyên chuỗi, cổng báo
            thieu.append(f"o_loi@{t}")
        elif v is not None:
            khac0 += float(v) != 0
    if not thieu and khac0 == 0:
        raise ValueError("12/12 ô COM_GAG = 0 — ⛔ chứng minh được gì (Đ3: mẫu số khác 0 mới đo)")
    return {"thieu": thieu, "lac": [],
            "dai": f"{len(dong)} tháng {THANG_MONG[0]}→{THANG_MONG[-1]} · COM_GAG ≠ 0: "
                   f"{khac0}/{len(THANG_MONG)} tháng"}
