"""Khuôn đóng băng `pm_join` — dòng LỆNH CHI `[Importrange]PM_Unpivot` *(RAW `1md85t…`)* · bộ ba HD1 · `WO-353` C1 = ⓐ.

    python tools/doc_bo_ba_hd1.py --ghi
    python tools/dong_bang_sheet.py pm_join <bản_thô.json> --mong N --ra tests/fixture/pm_join_song_20261123.json

⭐ Thay nửa `pm` của ảnh tháng 8 `tests/fixture/pm_join.json` *(27/08, 3.703 dòng — ⛔ có mã sinh)*. Dựng bằng CHÍNH luật đọc của
`tools/nap_that.dung_pm` *(tách thuần từ `doc_pm` ở `WO-353` — ⛔ chép)*: tiêu đề hàng 2 qua `fls.adapters.pm_join.kiem_tieu_de_pm`,
vị trí `PM_COT`, tiền qua `Decimal` *(⛔ float)*, ô rỗng = KHÔNG BIẾT *(`INV-I16`)*.
Cột = cột ảnh tháng 8: `ref_tho` *(NGUYÊN VĂN — `vi_sao_ref_THO`)* · `slip` · `line` · `tien` · `cur` · `status` · `hd` · `cdt1`.

⛔⛔ Riêng tư *(ảnh tháng 8 `khong_mang_PII`: ⛔ Timestamp · Email Address · Tên tài khoản · Số tài khoản · Ghi chú · Diễn giải)*:
bản thô ĐÃ CHIẾU ở lượt đọc *(`tools/doc_bo_ba_hd1.py`)* — chỉ giữ 14 vị trí `PM_TIEU_DE_MONG_DOI`, mọi ô khác `None` và tên
cột khác `""` ⇒ `Email Address` ⛔ tới được khuôn *(khuôn vẫn soát lại: tên thuộc `PM_COT_RIENG_TU` ⇒ TỪ CHỐI; ô ngoài 14 vị trí
có giá trị ⇒ TỪ CHỐI — bản thô ⛔ chiếu)*.

Bản thô: `{nguon, doc_luc, cach_doc, tieu_de: [hàng 2 A:AC đã chiếu], dong_dau: 3, values: [[A…AC đã chiếu]…]}`.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from decimal import Decimal
from typing import Any

_KH = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_KH.parents[1]))


def _nap(ten: str):
    spec = importlib.util.spec_from_file_location(f"khuon_dong_bang_{ten}", _KH / f"{ten}.py")
    m = sys.modules.get(spec.name)
    if m is None:
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
    return m


_b = _nap("_bo_ba_hd1")

BANG = "HD1.PM_JOIN"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("ref_tho", "slip", "line", "tien", "cur", "status", "hd", "cdt1")
KIEU_COT = {c: "chu?" for c in COT}
RA = "tests/fixture/pm_join_song_20261123.json"

#: ⭐ Đ5 — đo lượt `WO-353` 23/11 rồi khai *(khác ⇒ ĐỎ cả hai chiều)*: `co_ma` = dòng có `ref` sau `canon_ref` · `co_tien` = dòng
#: có tiền. Ảnh tháng 8: 3.703 dòng · 3.173 có mã; BG-346 23/11 sáng *(chỉ-đọc)*: 3.909 · 3.369.
MONG_DEM: dict[str, int] = {"dong": 3909, "co_ma": 3369, "co_tien": 3909}
_DEM: dict[str, int] = {}


def _phang(v: Any) -> Any:
    if isinstance(v, Decimal):
        return int(v) if v == v.to_integral_value() else float(v)
    return v


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    from fls.adapters.pm_join import PM_DONG_DAU, PM_TIEU_DE_MONG_DOI, kiem_tieu_de_pm
    from tools.nap_that import dung_pm
    td, d0, v = tho.get("tieu_de"), tho.get("dong_dau"), tho.get("values")
    if not isinstance(td, list) or not isinstance(v, list) or not v or any(not isinstance(h, list) for h in v):
        raise ValueError("bản thô phải có `tieu_de` (hàng 2) và `values` ≥ 1 hàng")
    if d0 != PM_DONG_DAU:
        raise ValueError(f"`dong_dau` phải {PM_DONG_DAU} *(PM_DONG_DAU — tiêu đề hàng 2, dữ liệu từ hàng 3)*")
    _b.soat_rieng_tu(td, "tiêu đề PM")
    giu = set(PM_TIEU_DE_MONG_DOI)
    if any(str(x or "").strip() for j, x in enumerate(td) if j not in giu):
        raise ValueError("tiêu đề PM mang tên cột ngoài 14 vị trí `PM_TIEU_DE_MONG_DOI` — bản thô ⛔ chiếu")
    if any(not _b.rong(x) for h in v for j, x in enumerate(h) if j not in giu):
        raise ValueError("hàng PM mang ô ngoài 14 vị trí `PM_TIEU_DE_MONG_DOI` — bản thô ⛔ chiếu")
    try:
        kiem_tieu_de_pm(td)                                     # ④ nguồn PM đổi cột ⇒ NỔ TO
    except Exception as e:
        raise ValueError(f"tiêu đề PM ≠ `PM_TIEU_DE_MONG_DOI`: {type(e).__name__}") from None
    pm = dung_pm(list(td), [[_phang(x) for x in h] for h in v])
    dong = [[x.dong_sheet, _b.o_chu(x.ref_tho), x.slip or None, x.line or None,
             _b.chu_so(x.tien) if x.tien is not None else None, x.cur or None, x.status or None, x.hd, x.cdt1] for x in pm]
    _DEM.clear()
    _DEM.update({"dong": len(pm), "co_ma": sum(1 for x in pm if x.ref), "co_tien": sum(1 for x in pm if x.tien is not None)})
    return {"cot": [KHOA, *COT], "dong": dong,
            "ghi_chu": (f"PM_Unpivot sống qua `nap_that.dung_pm`: {len(pm)} dòng *(hàng 3…{2 + len(pm)})* · {_DEM['co_ma']} dòng có mã "
                        f"*(`canon_ref`)* · {_DEM['co_tien']} dòng có tiền. Bản thô ĐÃ CHIẾU 14 vị trí `PM_TIEU_DE_MONG_DOI` ⇒ "
                        "⛔⛔ Timestamp · Email Address · Tên tài khoản · Số tài khoản · Ghi chú ⛔ tới khuôn. Ô rỗng ghi `null` "
                        "*(⛔ chuỗi rỗng)*.")}


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    if not dong:
        raise ValueError("ảnh rỗng — ⛔ đo được (Đ3)")
    if not MONG_DEM or not _DEM:
        raise ValueError("MONG_DEM ⛔ khai hoặc chưa chạy `chuan_bi` trong lượt — cổng ⛔ đo được (Đ5)")
    thieu = [f"{k}: {_DEM.get(k)}≠{MONG_DEM.get(k)}" for k in sorted(set(_DEM) | set(MONG_DEM)) if _DEM.get(k) != MONG_DEM.get(k)]
    return {"thieu": thieu, "lac": [], "dai": " · ".join(f"{k} {n}" for k, n in _DEM.items())}
