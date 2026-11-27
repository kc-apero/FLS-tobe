"""Khuôn đóng băng `itl_ledge_adjustment` — SỔ HD1 *(`ITL Ledge` của sổ ADJUSTED `1r4Wem…`, ⛔ bản xlsx)* · bộ ba HD1 · `WO-353` C1 = ⓐ.

    python tools/doc_bo_ba_hd1.py --ghi              # MỘT lượt đọc 3 nguồn ⇒ bản thô /tmp (chmod 600) ⇒ 3 khuôn ⇒ 3 ảnh
    python tools/dong_bang_sheet.py itl_ledge_adjustment <bản_thô.json> --mong N --ra tests/fixture/itl_ledge_adjustment_song_20261123.json

⭐ Cùng gốc với ảnh tháng 8 `tests/fixture/itl_ledge_adjustment.json` *(nguồn `[Master] ITL_Ledge_raw.xlsx > ITL Ledge` — xlsx là bản
xuất của chính sổ này; ảnh cũ ghi "21/23 kỳ khớp CHÍNH XÁC với bản ADJUSTED sạch")* ⇒ đọc THẲNG sổ sống, ⛔ qua xlsx *(bẫy
`CLAUDE.md`: xlsx offline phá ngày — ảnh cũ phải dựng lại 9.967 ngày, `ngay_dung_lai`)*.

Cột ảnh = cột ảnh tháng 8 *(`dong_sheet` · `ky` · 7 khối × Classifying · MID · Final = 21)* + `khoa_ghep` *(băm 16 hex — xem
`_bo_ba_hd1.khoa_ghep`; thay cho ảnh `classifying_vs_canon` mà ⛔ có mã sinh)*. ⛔ `Manual input` *(ảnh tháng 8 ⛔ có; DT12 có)*.
⛔⛔ KHÔNG mang `Số chứng từ` · `Diễn giải` · PS Nợ/Có · TK: bản thô có `A:B` + `D:G` *(⛔ `C`)* chỉ để dựng `ky` + `khoa_ghep`.

Bản thô *(lượt đọc của `tools/doc_bo_ba_hd1.py`)*: `{nguon, doc_luc, cach_doc, tieu_de: [hàng 7, hàng 8] (A7:AT8), dong_dau: 10,
AB: [[A, B]…], DG: [[D, E, F, G]…], RAT: [[R…AT]…]}` — ba lưới CÙNG số hàng, hàng i = hàng sheet `dong_dau + i`.
Dòng SỔ = hàng có ô `A` *(ngày)* — như DT12 *(⛔ "hàng có ≥ 1 ô": cột công thức kín lưới)*.
"""
from __future__ import annotations

import datetime
import importlib.util
import pathlib
import sys
from collections import Counter
from decimal import Decimal
from typing import Any

_KH = pathlib.Path(__file__).resolve().parent


def _nap(ten: str):
    spec = importlib.util.spec_from_file_location(f"khuon_dong_bang_{ten}", _KH / f"{ten}.py")
    m = sys.modules.get(spec.name)
    if m is None:
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
    return m


_b = _nap("_bo_ba_hd1")
_ky = _nap("itl_ledge_ky")                      # TIEU_DE 30 tên R:AT của DT12 — MỘT bản khai bố cục 7 khối

BANG = "HD1.ITL_LEDGE_ADJUSTMENT"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
KHOI = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")
PHAN = ("classifying", "mid", "final")
COT = ("ky", "khoa_ghep", *(f"{k}_{p}" for k in KHOI for p in PHAN))
KIEU_COT = {"ky": "chu", "khoa_ghep": "chu", **{c: "chu?" for c in COT[2:]}}
RA = "tests/fixture/itl_ledge_adjustment_song_20261123.json"
#: vị trí 0-based TRONG lưới `R:AT` *(R = 0)* của Classifying · MID · Final khối j: S…AT, mỗi khối 4 cột *(Cls · Manual · MID · Final)*.
_VT = {(k, p): 1 + 4 * j + {"classifying": 0, "mid": 2, "final": 3}[p] for j, k in enumerate(KHOI) for p in PHAN}
EPOCH = datetime.date(1899, 12, 30)
#: Hàng 7 cột A, B, D…G *(BA-05 §DD-I04 — ⛔ C Diễn giải)*.
TEN_A7 = "Ngày chứng từ"

#: ⭐ Đ5 — phân bố dòng sổ theo kỳ, đo lượt `WO-353` 23/11 rồi khai *(khác ⇒ ĐỎ cả hai chiều)*. Ảnh tháng 8: 23 kỳ · 9.967 dòng
#: *(`phan_bo_ky` của `tests/fixture/itl_ledge_adjustment.json`)*; DT12 23/11 sáng: 26 kỳ · Σ cột A 12.722.
#: Khác tháng 8 ở 23 kỳ chung: 2025-06 350 → 348 · 2025-07 549 → 546 · 2026-08 (ảnh 26/08 cắt giữa tháng) → 724; thêm 2026-09…11.
MONG_KY: dict[str, int] = {
    "2024-10": 6, "2024-11": 3, "2024-12": 6, "2025-01": 748, "2025-02": 283, "2025-03": 297, "2025-04": 332,
    "2025-05": 408, "2025-06": 348, "2025-07": 546, "2025-08": 537, "2025-09": 501, "2025-10": 487, "2025-11": 477,
    "2025-12": 566, "2026-01": 471, "2026-02": 439, "2026-03": 584, "2026-04": 600, "2026-05": 537, "2026-06": 613,
    "2026-07": 686, "2026-08": 724, "2026-09": 737, "2026-10": 1038, "2026-11": 748,
}                                                     # Σ 12.722 = Σ cột A manifest DT12 `itl_ledge_cac_ky_20261123.json` (Đ2)


def _ten(v: Any) -> str:
    return " ".join(str(v or "").split())


def _phang(v: Any) -> Any:
    """Decimal của bản thô *(công cụ đọc JSON bằng `parse_float=Decimal`)* ⇒ int/float như JSON API — để `parse_so` ăn y như
    `tools/nap_that.py`."""
    if isinstance(v, Decimal):
        return int(v) if v == v.to_integral_value() else float(v)
    return v


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    td, d0 = tho.get("tieu_de"), tho.get("dong_dau")
    ab, dg, rat = tho.get("AB"), tho.get("DG"), tho.get("RAT")
    if not (isinstance(td, list) and len(td) == 2 and all(isinstance(h, list) for h in td)):
        raise ValueError("`tieu_de` phải [hàng 7, hàng 8] của sổ (A7:AT8)")
    if d0 != 10:
        raise ValueError("`dong_dau` phải 10 *(hàng dữ liệu đầu của sổ — DT12 `HANG_DAU_SO`)*")
    if not all(isinstance(x, list) for x in (ab, dg, rat)) or not (len(ab) == len(dg) == len(rat) > 0):
        raise ValueError("`AB` · `DG` · `RAT` phải ba lưới CÙNG số hàng > 0")
    a7, a8 = list(td[0]) + [""] * 46, list(td[1]) + [""] * 46
    _b.soat_rieng_tu(a7 + a8, "tiêu đề sổ")
    # ⚠ tên `C7` *(Diễn giải)* có ở hàng tiêu đề A7:AT8 — chỉ TÊN; DỮ LIỆU cột C ⛔ có trong bản thô *(lưới `AB` · `DG` · `RAT`)*.
    if _ten(a7[0]) != TEN_A7:
        raise ValueError("hàng 7 cột A ≠ `Ngày chứng từ` — sổ đổi bố cục")
    _b.kiem_ten_khoa(a7[:7], "sổ hàng 7")
    vt_nhan = (21, 22, 26, 30, 34, 38, 42)              # = `tools/doc_itl_ledge_ky.VT_NHAN`
    ten_rat = [_ten(a7[17]), _ten(a7[0])] + [f"{_ten(a7[vt_nhan[j]])} · {_ten(a8[18 + 4 * j + p])}"
                                             for j in range(7) for p in range(4)]
    if tuple(ten_rat) != _ky.TIEU_DE:
        raise ValueError("tên 30 cột R:AT ≠ `itl_ledge_ky.TIEU_DE` — sổ đổi bố cục, ánh xạ theo TÊN nên ⛔ đóng băng")
    dong, khong_ngay = [], 0
    for i, (h_ab, h_dg, h_r) in enumerate(zip(ab, dg, rat)):
        ds = d0 + i
        a = _phang(h_ab[0]) if h_ab else None
        if _b.rong(a):
            khong_ngay += 1
            continue
        if isinstance(a, bool) or not isinstance(a, (int, float)) or a != int(a) or a < 1:
            raise ValueError(f"hàng sheet {ds}: cột A *(ngày)* phải serial số nguyên ≥ 1")
        ngay = EPOCH + datetime.timedelta(days=int(a))
        h7 = [_phang(x) for x in (list(h_ab) + [None] * 2)[:2]] + [None] + [_phang(x) for x in (list(h_dg) + [None] * 4)[:4]]
        r = list(h_r) + [None] * 29
        dong.append([ds, f"{ngay.year}-{ngay.month:02d}", _b.khoa_ghep(h7),
                     *(_b.o_chu(_phang(r[_VT[(k, p)]])) for k in KHOI for p in PHAN)])
    if not dong:
        raise ValueError("0 dòng sổ — mẫu số 0 (Đ3)")
    pb = Counter(h[1] for h in dong)
    return {"cot": [KHOA, *COT], "dong": dong,
            "ghi_chu": (f"ITL Ledge sống *(ADJUSTED)*: {len(dong)} dòng sổ = hàng có ô A *(ngày)* · {len(pb)} kỳ "
                        f"{min(pb)}…{max(pb)}; {khong_ngay} hàng lưới ⛔ có ngày ⛔ mang. `ky` = tháng của serial A *(⛔ "
                        "dựng lại ngày — nguồn SỐNG ⛔ hỏng ngày như xlsx)*. 21 cột = 7 khối × Classifying · MID · Final ở `S…AT` "
                        "*(⛔ Manual input — như ảnh tháng 8)*. `khoa_ghep` = sha256[:16] của (Số CT · PS Nợ · PS Có · TK · "
                        "tiền tệ) đã chuẩn hoá *(`_bo_ba_hd1.khoa_ghep`)* — ⛔⛔ BỎ `Số chứng từ` · `Diễn giải` · tiền · TK.")}


def phan_bo_ky(dong: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(str(_b.u(r["ky"])) for r in dong).items()))


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5)*: phân bố dòng theo kỳ ↔ `MONG_KY` *(khác ⇒ thiếu, cả hai chiều)*. `MONG_KY` rỗng ⇒ ⛔ đo được."""
    if not dong:
        raise ValueError("ảnh rỗng — ⛔ đo được (Đ3)")
    if not MONG_KY:
        raise ValueError("MONG_KY ⛔ khai — cổng ⛔ đo được (Đ5)")
    pb = phan_bo_ky(dong)
    thieu = [f"kỳ {k}: {pb.get(k)}≠{MONG_KY.get(k)}" for k in sorted(set(pb) | set(MONG_KY)) if pb.get(k) != MONG_KY.get(k)]
    return {"thieu": thieu, "lac": [], "dai": f"{len(dong)} dòng · {len(pb)} kỳ {min(pb)}…{max(pb)}"}
