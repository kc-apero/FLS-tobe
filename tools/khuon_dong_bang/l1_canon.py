"""Khuôn đóng băng `l1_canon` — dòng FLS DỰNG LẠI từ `Transaction Mapping L1` *(RAW `1md85t…`)* · bộ ba HD1 · `WO-353` C1 = ⓐ.

    python tools/doc_bo_ba_hd1.py --ghi
    python tools/dong_bang_sheet.py l1_canon <bản_thô.json> --mong N --ra tests/fixture/l1_canon_song_20261123.json

⭐ Thay hai nửa của bộ ba tháng 8 mà ⛔ có mã sinh: nửa `bank` của `tests/fixture/pm_join.json` *(9.992 dòng canon: `dong · ref_tho ·
cur · tien`)* và nửa `canon_pos_*` của `classifying_vs_canon.json` *(7 vị trí `Classifying` đọc — kiểm `Classifying = iferror(canon)`)*.
Dựng bằng CHÍNH đường nạp: `fls.adapters.bank.nap` *(kiểm tiêu đề `kiem_header` · ba đường vào = canon + loại + rỗng)* rồi
`fls.repo.chay_nap._bank_tu_canon` *(mã tham chiếu cột B · tiền = PS Nợ + PS Có · tiền tệ)* — ĐÚNG hai hàm `tools/nap_that.py` gọi.
⛔ chép luật.

Cột: `ref_tho` *(cột B NGUYÊN VĂN — như ảnh tháng 8 `vi_sao_ref_THO`: lưu mã đã chuẩn hoá thì bẻ `canon_ref` mà cổng vẫn XANH)* ·
`cur` · `tien` *(chữ số thập phân)* · `khoa_ghep` *(`_bo_ba_hd1.khoa_ghep` — CÙNG hàm với khuôn sổ)* · `canon_pos_<p>` ×7 *(ô THÔ
của L1 ở vị trí p — ô lỗi `#N/A (…)` GIỮ, vì `Classifying = iferror(<ô>, NTMI)` đọc chính ô lỗi; `bank.nap` thì xoá ô lỗi)*.
⛔ mang `Diễn giải` *(C)* · `Ngày` · PS Nợ/Có tách.

Bản thô: `{nguon, doc_luc, cach_doc, header: [hàng 3 A:AL], dong_dau: 5, values: [[A…AL]…]}` — hàng i = hàng sheet `5 + i`
*(`BAN_SAO_RAW.dong_dau`)*. Bản thô mang `C` *(Diễn giải)* ⇒ CHỈ ở `/tmp` chmod 600 — khuôn ⛔ chép nó.
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

BANG = "HD1.L1_CANON"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
#: = 7 vị trí `fls.ledger.classifying.VI_TRI_CLASSIFYING` *(H · S · T · Y · AB · AC · AD — chỗ `Classifying` của 7 khối đọc)*.
#: ⚠ Ảnh tháng 8 giữ 13 *(`vi_tri_giu` thêm L · U · V · W · X · AE)*; 6 vị trí thêm ⛔ khối nào đọc *(W/X là cặp CHẾT —
#: `VI_TRI_CHET`)* mà chiếm ~5,3 MB ô `#N/A (…)` ⇒ ⛔ mang *(ảnh 18,3 MB → ~10 MB; đo 23/11)*.
VI_TRI_GIU = (7, 18, 19, 24, 27, 28, 29)
COT = ("ref_tho", "cur", "tien", "khoa_ghep", *(f"canon_pos_{p}" for p in VI_TRI_GIU))
KIEU_COT = {"ref_tho": "chu?", "cur": "chu?", "tien": "chu", "khoa_ghep": "chu", **{f"canon_pos_{p}": "chu?" for p in VI_TRI_GIU}}
RA = "tests/fixture/l1_canon_song_20261123.json"

#: ⭐ Đ5 — ba đường của `bank.nap`, đo lượt `WO-353` 23/11 rồi khai *(vào = canon + loại + rỗng)*. Ảnh tháng 8: canon 9.992
#: *(L1 26/08 đọc 10.100)*; BG-346 23/11 sáng đo lại chỉ-đọc: 14.265 = 12.601 + 121 + 1.543.
MONG_BA_DUONG: dict[str, int] = {"vao": 14265, "canon": 12601, "loai": 121, "rong": 1543}
#: số đếm ba đường của LẦN `chuan_bi` cuối — `thieu_lac` so với `MONG_BA_DUONG` *(công cụ gọi `chuan_bi` rồi `thieu_lac` trong
#: MỘT lượt; ⛔ dùng ngoài lượt ấy)*.
_DEM: dict[str, int] = {}


def _phang(v: Any) -> Any:
    if isinstance(v, Decimal):
        return int(v) if v == v.to_integral_value() else float(v)
    return v


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    from fls.adapters.bank import kiem_header, nap
    from fls.ledger.build import NgucCanh
    from fls.oracle.nguon import BAN_SAO_RAW
    from fls.repo.chay_nap import _bank_tu_canon
    hdr, d0, v = tho.get("header"), tho.get("dong_dau"), tho.get("values")
    if not isinstance(hdr, list) or not isinstance(v, list) or not v or any(not isinstance(h, list) for h in v):
        raise ValueError("bản thô phải có `header` (hàng 3 A:AL) và `values` ≥ 1 hàng")
    if d0 != BAN_SAO_RAW.dong_dau:
        raise ValueError(f"`dong_dau` phải {BAN_SAO_RAW.dong_dau} *(BAN_SAO_RAW.dong_dau — `bank.nap` đánh số hàng từ đó)*")
    _b.soat_rieng_tu(hdr, "tiêu đề L1")
    try:
        kiem_header(hdr)                                         # ④ nguồn đổi cột ⇒ NỔ TO
    except Exception as e:
        raise ValueError(f"tiêu đề L1 ≠ khuôn canon: {type(e).__name__}") from None
    _b.kiem_ten_khoa(hdr[:7], "L1 hàng 3")
    phang = [[_phang(x) for x in h] for h in v]
    ra, loai, tk = nap(phang)
    if not tk.can():
        raise ValueError("ba đường ⛔ cân")
    nc = NgucCanh("wo353-dong-bang", "v1.0", "v1.0", "v1.0", BAN_SAO_RAW.ma, BAN_SAO_RAW.sheet)
    bank = {b.dong_sheet: b for b in _bank_tu_canon(ra, nc)}
    dong = []
    for ds, _row in ra:
        h = phang[ds - d0] + [None] * 38
        b = bank[ds]
        dong.append([ds, _b.o_chu(h[1]), _b.o_chu(b.cur) if b.cur else None, _b.chu_so(b.tien), _b.khoa_ghep(h[:7]),
                     *(_b.o_chu(h[p]) for p in VI_TRI_GIU)])
    _DEM.clear()
    _DEM.update({"vao": tk.vao, "canon": tk.ra, "loai": tk.loai, "rong": tk.rong})
    return {"cot": [KHOA, *COT], "dong": dong,
            "ghi_chu": (f"L1 sống qua `bank.nap`: vào {tk.vao} = canon {tk.ra} + loại {tk.loai} + rỗng {tk.rong} *(cân)*; ảnh = "
                        f"{len(dong)} dòng canon. Dòng loại *(lý do có tên ở `bank.nap`)* ⛔ vào ảnh — như ảnh tháng 8 *(9.992 = "
                        "`so_dong_canon`)*. `ref_tho` = cột B NGUYÊN VĂN · `tien` = PS Nợ + PS Có *(`_bank_tu_canon`)* · `canon_pos_p` "
                        "= ô THÔ vị trí p *(giữ ô lỗi)*. ⛔⛔ BỎ `Diễn giải` · ngày · PS Nợ/Có tách.")}


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    if not dong:
        raise ValueError("ảnh rỗng — ⛔ đo được (Đ3)")
    if not MONG_BA_DUONG or not _DEM:
        raise ValueError("MONG_BA_DUONG ⛔ khai hoặc chưa chạy `chuan_bi` trong lượt — cổng ⛔ đo được (Đ5)")
    thieu = [f"{k}: {_DEM.get(k)}≠{MONG_BA_DUONG.get(k)}" for k in ("vao", "canon", "loai", "rong")
             if _DEM.get(k) != MONG_BA_DUONG.get(k)]
    if _DEM.get("canon") != len(dong):
        thieu.append(f"canon {_DEM.get('canon')} ≠ dòng ảnh {len(dong)}")
    return {"thieu": thieu, "lac": [], "dai": "ba đường " + " · ".join(f"{k} {n}" for k, n in _DEM.items())}
