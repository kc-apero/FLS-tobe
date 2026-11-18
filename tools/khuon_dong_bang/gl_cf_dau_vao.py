"""Khuôn đóng băng `gl_cf_dau_vao` — ĐẦU VÀO của SO.CFA1 Daily *(H5)*: dòng sổ GL CỦA BẢN SAO CF report.

    python tools/dong_bang_sheet.py gl_cf_dau_vao <bản_thô.json> --mong 12385
        ⇒ tests/fixture/dap_an/gl_cf_dau_vao.json

⭐ **Vì sao có khuôn này** *(ISP 3.1.2 · Step 16 · H5 — errata ㉓; WO-164)*. Orchestrator đọc
CÔNG THỨC `'Report I CFA1 Daily'` của bản sao CF report *(khoá SA chỉ-đọc, 18/11)*:
  · ô lá khối **GROUP** = `SUMIFS(GL!$BR, GL!$A, ngày, GL!$V, $F<hàng>) − SUMIFS(GL!$BS, …)` —
    Σ MỌI dòng GL *(⛔ lọc LE)* theo (ngày cột `A`, nhãn HD cột `V`);
  · khối LE *(SGO2 · SGO1 · HGO6 · BGO2)*: cùng công thức + `GL!$P = <mã LE>` ⇒ **LE = cột `P`**;
  · hàng cha `=sum(con)` theo cây.
`GL` ở đây là sheet `Report I General Ledger` **TRONG CHÍNH bản sao CF report** *(⛔ bản sao 406
của H4: 12.385 dòng ≠ 7.883, có thêm cột P/V)*. Trước bước này repo ⛔ có ảnh nào mang LE + ngày +
HD Final + tiền theo dòng *(quét 17 ảnh `tests/fixture/` 18/11: chỉ 2 ảnh có LE — đều là đáp án)*.

Hợp đồng bản thô *(phiên H5 đọc bằng `sa_lay.py`, 5 lượt `A10:A` · `D10:F` · `P10:P` · `R10:R` ·
`V10:V` tới hàng 19238 = rowCount; ⛔ commit bản thô — chỉ /tmp)* — LƯỚI
`{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values}`:
  · `cot` = `("dong_sheet", "A", "D", "E", "F", "P", "R", "V")`. ⛔⛔ `B` Số CT · `C` Diễn giải ·
    `G` Tài khoản — vùng đọc ⛔ phủ.
  · `values` = hàng dữ liệu theo thứ tự sheet *(10…12394, LIÊN TỤC — đo 18/11: 12.385 hàng, cả 5
    lượt cùng 12.385; dưới đó rỗng)*.

⭐ **Sáu quyết định** *(mỗi cái một số đo 18/11 — Đ4/Đ5)*:
  ① Khoá `dong_sheet`, giữ thứ tự sheet.
  ② `ngay` = serial cột `A` *(SỐ; đo: 12.385/12.385 ô int, 45586…46337 = 2024-10-21…2026-11-11)*.
  ③ `le` = cột `P` NHƯNG chỉ khi ∈ `LE_CFA1` *(4 mã khối LE của CFA1)*; giá trị khác ⇒ `None` và
    CHỈ ĐẾM ở bảng phụ `le_lop`. Lý do: cột `P` có **24** giá trị khác nhau, trong đó có TÊN NGƯỜI
    viết tắt *(PII)* và `#N/A` *(109)*; GROUP ⛔ lọc `P` nên H5 ⛔ cần mã nào ngoài 4 mã kia.
  ④ `hd_final` = cột `V` *(khối Final của `Budget Code (HDCode)` — hàng 8 = "Final")* GIỮ NGUYÊN
    CHỮ *(SUMIFS so NHÃN đủ `"MÃ | Tên"`, ⛔ so mã)*; đo: 12.376 nhãn có `" | "`, 8 thiếu mã, 1 rỗng.
  ⑤ `itl_id` = cột `R` *(⛔ khớp `^ITL#\\d+$` ở 109 hàng `#N/A` — giữ y nguyên, H5 ⛔ nối qua nó)*.
  ⑥ `D` ∈ 5 tiền tệ hoặc rỗng *(đo: 12 rỗng)*; `E`/`F` số hoặc rỗng *(đo: 0 chuỗi khác rỗng)*.
"""
from __future__ import annotations

import datetime
from typing import Any

BANG = "CF.GL.DauVao"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("ngay", "itl_id", "le", "hd_final", "D", "E", "F")
KIEU_COT = {"itl_id": "chu", "le": "chu?", "hd_final": "chu?", "D": "chu?", "E": "so?", "F": "so?"}
RA = "tests/fixture/dap_an/gl_cf_dau_vao.json"

COT_THO = ("dong_sheet", "A", "D", "E", "F", "P", "R", "V")
DONG_DAU_SHEET = 10
TIEN_TE = ("USD", "SGD", "COP", "VND", "HKD")
#: ③ 4 khối LE của CFA1 *(khối thứ 5 `GROUP` = Σ mọi dòng, ⛔ là mã cột P)*.
LE_CFA1 = ("SGO2", "SGO1", "HGO6", "BGO2")
#: Lớp đếm của cột P: 4 mã LE · `loi_sheets` *(chuỗi `#…`)* · `khac` *(mã/tên khác — ⛔ in)*.
LOP = (*LE_CFA1, "loi_sheets", "khac")
#: Đ5 — số dòng mỗi lớp *(đo 18/11)*. Khác ⇒ bài ghim ĐỎ *(⛔ cổng công cụ: bảng phụ chỉ đếm hàng)*.
MONG_LE_LOP = {"SGO2": 3871, "SGO1": 715, "HGO6": 94, "BGO2": 118, "loi_sheets": 109, "khac": 7478}
PHU_MONG = {"le_lop": len(LOP)}
EPOCH = datetime.date(1899, 12, 30)


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v == "")


def _lop(p: Any) -> str:
    if isinstance(p, str) and p in LE_CFA1:
        return p
    if isinstance(p, str) and p.startswith("#"):
        return "loi_sheets"
    return "khac"


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI → bảng `{dong_sheet, ngay, itl_id, le, hd_final, D, E, F}` + bảng phụ `le_lop`.
    `ValueError` ⇒ TỪ CHỐI; ⛔ lời lỗi mang giá trị ô *(cột P có tên người)*."""
    if tho.get("cot") != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(⛔ phủ B:C·G)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng dữ liệu ⛔ rỗng")
    dong: list[list[Any]] = []
    dem = {k: 0 for k in LOP}
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô")
        ds, a, d_tt, e, f, p, r, v = h
        if ds != DONG_DAU_SHEET + i:
            raise ValueError(f"hàng {i + 1}: dong_sheet ⛔ liên tục *(mong {DONG_DAU_SHEET + i})*")
        if not isinstance(a, int) or isinstance(a, bool) or a < 1:
            raise ValueError(f"hàng {i + 1}: cột A *(ngày)* phải serial số nguyên ≥ 1")
        d_tt = None if _rong(d_tt) else d_tt
        if d_tt is not None and d_tt not in TIEN_TE:
            raise ValueError(f"hàng {i + 1}: cột D ⛔ thuộc tập đóng tiền tệ {list(TIEN_TE)}")
        lop = _lop(p)
        dem[lop] += 1
        dong.append([ds, a, None if _rong(r) else r, lop if lop in LE_CFA1 else None,
                     None if _rong(v) else v, d_tt,
                     None if _rong(e) else e, None if _rong(f) else f])
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"le_lop": [{"lop": k, "so_dong": dem[k]} for k in LOP]},
        "ghi_chu": (
            f"ĐẦU VÀO SO.CFA1 Daily = {len(dong)} dòng `Report I General Ledger` CỦA BẢN SAO CF report "
            f"*(sheet mà SUMIFS của `Report I CFA1 Daily` đọc)*, khoá dong_sheet {DONG_DAU_SHEET}…"
            f"{DONG_DAU_SHEET + len(dong) - 1} liên tục. Cột: ngay = A *(serial)* · itl_id = R · "
            f"le = P CHỈ khi ∈ {list(LE_CFA1)} *(mã khác ⇒ null, chỉ ĐẾM ở `le_lop` — cột P có tên "
            f"người)* · hd_final = V *(nhãn 'MÃ | Tên' nguyên chữ)* · D · E/F nguyên tệ. ⛔ B (Số CT) · "
            f"C (Diễn giải) · G (Tài khoản). ⛔ BR/BS của sheet *(H5 tính lại bằng tinh_gl — ⛔ vòng tròn)*."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """`thieu` = ngày ngoài [2024-10-20, 2026-11-18] *(trục 409)*; `lac` ⛔ có *(Đ5: mong rỗng)*."""
    dau, cuoi = 45585, 46344
    ngoai = [d["dong_sheet"] for d in dong if not dau <= int(d["ngay"]) <= cuoi]
    return {"thieu": [f"ngay_ngoai_truc@{x}" for x in ngoai], "lac": [],
            "dai": f"{len(dong)} dòng · ngày ngoài trục 409: {len(ngoai)}"}
