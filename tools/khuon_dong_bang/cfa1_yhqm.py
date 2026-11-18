"""Khuôn đóng băng `cfa1_yhqm` — ĐÁP ÁN 410 · `Report I CFA1 Y H Q M` *(HD × kỳ, CF THEO LE)*.

    python tools/dong_bang_sheet.py cfa1_yhqm <bản_thô.json> --mong 5655
        ⇒ tests/fixture/dap_an/cfa1_yhqm.json

⭐ **Vì sao có khuôn này** *(ISP 3.1.2 · Step 15 · DT5 · AP v3.1.2 §3.3.1 PD 410 · §3.5.1)*. Cùng
đáp án CFA1 với `cfa1_daily` nhưng trục cột là **KỲ** Y/H/Q/M *(⛔ ngày)*. H6 so Σ theo (HD, kỳ).

Hợp đồng bản thô = **LƯỚI SA** `{spreadsheet_id, nguon, doc_luc, cach_doc, values}` của sheet
`'Report I CFA1 Y H Q M'` *(458 × 502)* — CÙNG cây HD với Daily *(5 khối LE × 74 mã)*, chỉ khác
tiêu đề cột:
  · Hàng 5 = `Year`; hàng 6 = `Period` *(mỗi năm MỘT khối 19 cột: năm · `H1` · `H2` · `Q1`…`Q4` ·
    tháng `1`…`12`)*. Cột `A` = mUSD *(⛔ vào ảnh)*.

⭐ **Đo 18/11 *(mỗi số đếm MỘT vật, Đ4)*:** 190 cột kỳ *(10 năm × 19)*; giữ **57** cột ≤ năm đọc
`2026` *(2024·2025·2026)*, cắt 7 năm tương lai *(toàn 0 — kiểm ③)*. 370 hàng HD. **5.655** ô ≠ 0 ⇒
dòng chính thưa; **25** ô `"-"` ⇒ bảng phụ `o_loi` *(AC-3)*.

⭐ **Khoá kỳ** *(hàm `_khoa_ky`)*: năm `2024`; nửa `2024H1`·`2024H2`; quý `2024Q1`…`2024Q4`; tháng
`2024M01`…`2024M12`. Loại kỳ ở bảng phụ `ky_truc` *(`Y`·`H`·`Q`·`M`)*.
"""
from __future__ import annotations

import datetime
import importlib.util
import pathlib
import sys
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "_cfa1.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__cfa1", _P)
_cfa1 = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _cfa1
_spec.loader.exec_module(_cfa1)

BANG = "PD.410"
KHOA = "o_id"
KIEU_KHOA = "ma"
#: Trục KỲ là nhãn CHỮ *(`2024H1`…)* ⇒ `ky` kiểu `chu` *(⛔ `so` như `ngay` của Daily)*.
COT = ("le", "ma_hd", "ky", "gt")
KIEU_COT = {"le": "chu", "ma_hd": "chu", "ky": "chu", "gt": "so"}
RA = "tests/fixture/dap_an/cfa1_yhqm.json"
#: Đ5 *(đo 18/11)*. `ky_truc` = số cột kỳ ≤ năm đọc *(3 năm × 19 = 57)*; khác ⇒ cổng ĐỎ.
PHU_MONG = {"hd": 370, "ky_truc": 57, "o_loi": 25}
#: Đ5 — phân bố giá trị ô lỗi *(như `cfa1_daily.O_LOI_GIA`)*: tập ⛔ số = `{"-"}` ×25.
O_LOI_GIA = {"-": 25}

I_YEAR, I_PERIOD, COT_DAU = 4, 5, 6

#: Thứ tự CHUẨN 19 kỳ TRONG một năm *(AP v3.1.2 §3.2.x)*: Năm · `H1` `H2` · `Q1`…`Q4` · tháng
#: `M01`…`M12`. Nhãn kỳ ⛔ TIN mù *(bia `DT5-R1-03`)*: thứ tự khoá dựng phải đúng chuỗi này,
#: hoán nhãn tháng ⇒ TỪ CHỐI.
_KY_CHUAN = ("Y", "H1", "H2", "Q1", "Q2", "Q3", "Q4") + tuple(f"M{m:02d}" for m in range(1, 13))


def _khoa_ky(nam: int, p: Any) -> tuple[str, str]:
    """(`year`, ô Period) → (khoá kỳ, loại). Năm ⇒ `"2024"`/`Y`; nửa `H1`/`H2` ⇒ `"2024H1"`/`H`;
    quý `Q1`…`Q4` ⇒ `"2024Q1"`/`Q`; tháng SỐ 1…12 ⇒ `"2024M01"`/`M`.

    ⛔ TIN số Period mù *(bia `DT5-R1-03`)*: phải NGUYÊN, và nếu ≠ năm thì phải là tháng 1…12 —
    `Period = 2023` ở cột `Year = 2024` từng cho khoá rác `2024M2023`."""
    if _cfa1._la_so(p):
        if int(p) != p:
            raise ValueError("Period số ⛔ nguyên *(ô Period lẻ ⇒ khoá kỳ rác)*")
        ip = int(p)
        if ip == nam:
            return f"{nam}", "Y"
        if not (1 <= ip <= 12):
            raise ValueError(f"Period số {ip} ⛔ là tháng 1…12 *(và ≠ năm {nam})* ⇒ khoá kỳ rác")
        return f"{nam}M{ip:02d}", "M"
    s = str(p).strip()
    loai = "H" if s in ("H1", "H2") else "Q" if s in ("Q1", "Q2", "Q3", "Q4") else "?"
    return f"{nam}{s}", loai


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI 410 → bảng thưa `{o_id, le, ma_hd, ky, gt}` + bảng phụ `hd`·`ky_truc`·`o_loi`.
    `ValueError` ⇒ TỪ CHỐI."""
    values = tho.get("values")
    if not isinstance(values, list) or len(values) <= COT_DAU:
        raise ValueError("`values` phải lưới đủ 6 hàng tiêu đề + dữ liệu")
    _cfa1.soat_pii_luoi(values)                                # ⛔ PII trước mọi thứ (AC-4)
    read_year = datetime.date.fromisoformat(tho["doc_luc"]).year

    yr, per = values[I_YEAR], values[I_PERIOD]
    cols: list[tuple[int, int, str, str]] = []            # (j, nam, khoa_ky, loai)
    for j in range(COT_DAU, len(per)):
        if per[j] is None or (isinstance(per[j], str) and not per[j].strip()):
            continue
        if not _cfa1._la_so(yr[j] if j < len(yr) else None):
            raise ValueError(f"cột kỳ {j} có Period nhưng Year *(hàng 5)* ⛔ phải số")
        nam = int(yr[j])
        khoa, loai = _khoa_ky(nam, per[j])
        if loai == "?":
            # ⛔ `{per[j]!r}` — ô Period có thể mang PII *(bia `DT5-R1-02`)*.
            raise ValueError(f"cột kỳ {j}: Period {_cfa1._an_toan(per[j])} ⛔ thuộc năm·H·Q·tháng")
        cols.append((j, nam, khoa, loai))
    if not cols:
        raise ValueError("hàng Period *(hàng 6)* ⛔ có cột kỳ nào từ cột G")

    giu = [c for c in cols if c[1] <= read_year]
    tuong_lai = [c[0] for c in cols if c[1] > read_year]
    # ② đủ Y/H/Q/M mỗi năm giữ *(19 cột/năm)* — hụt ⇒ lát kỳ hỏng ⇒ TỪ CHỐI
    from collections import OrderedDict
    seq: OrderedDict[int, list[str]] = OrderedDict()
    for j, nam, khoa, loai in giu:                         # thứ tự CỘT (khoá dựng, ⛔ ô bản thô)
        tok = "Y" if khoa == str(nam) else khoa[len(str(nam)):]
        seq.setdefault(nam, []).append(tok)
    for nam, toks in seq.items():
        if len(toks) != 19:
            raise ValueError(f"năm {nam} giữ {len(toks)} cột ≠ 19 Y/H/Q/M — lát kỳ hỏng")
        if tuple(toks) != _KY_CHUAN:                      # ⚠ hoán nhãn tháng ⇒ thứ tự lệch
            i = next(k for k in range(19) if toks[k] != _KY_CHUAN[k])
            raise ValueError(f"năm {nam}: thứ tự kỳ ⛔ chuẩn Y/H/Q/M ở vị trí {i} "
                             f"*(mong {_KY_CHUAN[i]})* — nhãn kỳ bị hoán/sai")

    hd = _cfa1.dung_cay(values)                            # ① ④
    _cfa1.kiem_tuong_lai_rong(values, hd, tuong_lai)      # ③

    cot_giu = [(j, khoa, khoa) for j, nam, khoa, loai in giu]
    dong, o_loi = _cfa1.boc_o(values, hd, cot_giu, "ky")
    _cfa1.ghi_ngu_canh(hd, o_loi, O_LOI_GIA)              # cổng `thieu_lac` đọc cây đầy đủ + o_loi
    ky_truc = [{"ky": khoa, "nam": nam, "loai": loai} for j, nam, khoa, loai in giu]
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"hd": hd, "ky_truc": ky_truc, "o_loi": o_loi},
        "ghi_chu": (
            f"CFA1 Y/H/Q/M *(lưới SA)*: 5 khối LE {list(_cfa1.LE)} × 74 mã HD = {len(hd)} hàng; "
            f"trục KỲ {len(giu)} cột *(năm ≤ {read_year}, {len(set(c[1] for c in giu))} năm × 19 "
            f"Y/H/Q/M)*, cắt {len(tuong_lai)} cột năm tương lai (toàn 0). {len(dong)} ô ≠ 0 ⇒ dòng "
            f"chính thưa; {len(o_loi)} ô ⛔ số ⇒ bảng phụ `o_loi` (giữ chuỗi, ĐẾM, ⛔ hoá 0 — AC-3). "
            "Cột A (mUSD) ⛔ vào ảnh."),
    }


#: Cổng DT5-B1 dùng chung với `cfa1_daily` *(`_cfa1.cong_hd`)*.
thieu_lac = _cfa1.cong_hd
