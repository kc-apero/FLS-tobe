"""Khuôn đóng băng `cfa1_daily` — ĐÁP ÁN 409 · `Report I CFA1 Daily` *(HD × ngày, CF THEO LE)*.

    python tools/dong_bang_sheet.py cfa1_daily <bản_thô.json> --mong 33355
        ⇒ tests/fixture/dap_an/cfa1_daily.json

⭐ **Vì sao có khuôn này** *(ISP 3.1.2 · Step 15 · DT5 · AP v3.1.2 §3.3.1 PD 409 · §3.5.1)*. Bước
**H5** *(SO.CFA1 Daily)* so Σ theo (HD, ngày) trên cây IX.HD với đáp án 409 TỪNG Ô. H5 cần ẢNH
đứng yên của 409 — đọc MỘT lần, đóng băng có checksum, cổng khẳng định **mọi mã HD ∈ cây ATL 74
dòng** *(DT5-B1)* và **số cột ngày = số ngày từ 21/10/2024 tới ngày đọc**.

Hợp đồng bản thô = **LƯỚI SA** *(phiên cloud DATA đọc bằng khoá SA chỉ-đọc, ⛔ commit)* —
`{spreadsheet_id, nguon, doc_luc, cach_doc, values}`, `values` lưới THEO HÀNG của sheet
`'Report I CFA1 Daily'` *(458 × 818)*:
  · Hàng 1…6 = tiêu đề: `Year · Half · Quarter · Month · Day(serial từ G5) · (L1…L4 + Days of the
    week)`. Cột `A` = số mUSD *(⛔ vào ảnh — chỉ CẤU TRÚC, như `atl_cay`)*.
  · 5 khối LE *(GROUP · SGO2 · SGO1 · HGO6 · BGO2)* × 74 mã HD *(6 nhóm HDO…HDCI, cột L1…L4 ở
    B…E)*; ô giá trị ở cột G trở đi *(mUSD theo ngày)*.

⭐ **Đo 18/11 *(khoá SA chỉ-đọc, phiên cloud — mỗi số đếm MỘT vật, Đ4)*:**
  · **812 cột ngày** sinh sẵn tới `2027-01-09`; giữ **760** cột ≤ ngày đọc `2026-11-18`
    *(2024-10-20 … 2026-11-18, LIÊN TỤC)*; cắt **52** cột tương lai *(toàn 0 — kiểm ③)*.
  · **370 hàng HD** = 5 LE × 74 *(mọi mã ∈ cây ATL — cổng DT5-B1)*.
  · **33.355** ô số ≠ 0 ⇒ dòng chính thưa; **25** ô `"-"` ⇒ bảng phụ `o_loi` *(AC-3 — giữ chuỗi,
    ĐẾM, ⛔ hoá 0)*; ⛔ ô `#REF!`/`#N/A` *(đo: tập ⛔ số = {`-`})*.

⚠ **Mốc 2024-10-20 ≠ 21/10/2024 của spec** *(Đ1/Đ4 — khai, ⛔ giấu)*. Cột ngày ĐẦU của sheet là
serial 45585 = **2024-10-20 (CN)**, sớm MỘT ngày so với `21/10/2024 (T2)` mà ISP/AP khai. Khuôn
GIỮ cột 2024-10-20 *(nguồn có 5 ô ≠ 0 + ô `"-"` ở đó — cắt là mất số)*; neo mốc = cột đầu THẬT của
sheet. Lệch một ngày này ⇒ câu hỏi cho orchestrator *(BG)*.
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

BANG = "PD.409"
KHOA = "o_id"
KIEU_KHOA = "ma"
#: Thứ tự cột ảnh = khoá ghép + 4 cột. `ngay` = serial *(SỐ)*; `le`·`ma_hd` = CHỮ; `gt` = mUSD SỐ.
COT = ("le", "ma_hd", "ngay", "gt")
KIEU_COT = {"le": "chu", "ma_hd": "chu", "ngay": "so", "gt": "so"}
RA = "tests/fixture/dap_an/cfa1_daily.json"
#: Đ5 — số dòng mỗi bảng phụ *(đo 18/11; re-read đổi ⇒ cập nhật + đóng băng lại, như `gl_406.MONG`)*.
#: `ngay_truc` = số cột ngày ≤ ngày đọc *(= số ngày 2024-10-20 → 2026-11-18)*; khác ⇒ cổng ĐỎ.
PHU_MONG = {"hd": 370, "ngay_truc": 760, "o_loi": 25}

#: Serial cột ngày ĐẦU của sheet *(2024-10-20 — mốc THẬT; spec khai 21/10, lệch 1 ngày, xem đầu tệp)*.
SERIAL_MOC = 45585
#: Hàng tiêu đề *(0-based)*: Day = hàng 5 *(index 4)*, Days-of-week = hàng 6 *(index 5)*; dữ liệu từ
#: cột G *(index 6)*.
I_DAY, I_DOW, COT_DAU = 4, 5, 6

def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI 409 → bảng `{o_id, le, ma_hd, ngay, gt}` *(thưa, ≠ 0)* + bảng phụ `hd`·`ngay_truc`·
    `o_loi`. `ValueError` ⇒ TỪ CHỐI *(⛔ lời lỗi mang giá trị ô)*."""
    values = tho.get("values")
    if not isinstance(values, list) or len(values) <= COT_DAU:
        raise ValueError("`values` phải lưới đủ 6 hàng tiêu đề + dữ liệu")
    _cfa1.soat_pii_luoi(values)                                # ⛔ PII trước mọi thứ (AC-4)
    read_date = datetime.date.fromisoformat(tho["doc_luc"])    # công cụ đã chuẩn hoá về ngày

    # ── trục NGÀY: serial ở hàng Day, từ cột G ──
    day = values[I_DAY]
    sers = [(j, int(day[j])) for j in range(COT_DAU, len(day)) if _cfa1._la_so(day[j])]
    if not sers:
        raise ValueError("hàng Day *(hàng 5)* ⛔ có serial ngày nào từ cột G")
    if sers[0][1] != SERIAL_MOC:
        raise ValueError(f"cột ngày đầu serial {sers[0][1]} ≠ mốc {SERIAL_MOC} *(2024-10-20)*")
    giu = [(j, s) for j, s in sers if _cfa1.ngay_tu_serial(s) <= read_date]
    tuong_lai = [j for j, s in sers if _cfa1.ngay_tu_serial(s) > read_date]
    # ② LIÊN TỤC *(serial kề nhau)* — hụt một lát ⇒ TỪ CHỐI
    for k, (j, s) in enumerate(giu):
        if s != giu[0][1] + k:
            raise ValueError(f"trục ngày ⛔ liên tục ở cột {j} *(serial {s} ≠ "
                             f"{giu[0][1] + k})* — lát ngày bị hụt")

    hd = _cfa1.dung_cay(values)                                # ① ④
    _cfa1.kiem_tuong_lai_rong(values, hd, tuong_lai)           # ③

    cot_giu = [(j, str(s), s) for j, s in giu]                 # nhãn o_id = serial str; ô trục = INT
    dong, o_loi = _cfa1.boc_o(values, hd, cot_giu, "ngay")

    ngay_truc = [{"ngay": s, "ngay_iso": _cfa1.ngay_tu_serial(s).isoformat(),
                  "dow": (values[I_DOW][j] if j < len(values[I_DOW]) else None)}
                 for j, s in giu]
    d_cuoi = _cfa1.ngay_tu_serial(giu[-1][1])
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"hd": hd, "ngay_truc": ngay_truc, "o_loi": o_loi},
        "ghi_chu": (
            f"CFA1 Daily *(lưới SA)*: 5 khối LE {list(_cfa1.LE)} × 74 mã HD = {len(hd)} hàng; "
            f"trục NGÀY {len(giu)} cột LIÊN TỤC 2024-10-20 … {d_cuoi.isoformat()} *(= ngày đọc "
            f"{read_date.isoformat()})*, cắt {len(tuong_lai)} cột tương lai (toàn 0). "
            f"{len(dong)} ô số ≠ 0 ⇒ dòng chính thưa (ô 0/vắng ⇒ 0 — H5 so 'ô so > 0'); {len(o_loi)} "
            "ô ⛔ số ⇒ bảng phụ `o_loi` (giữ chuỗi, ĐẾM, ⛔ hoá 0 — AC-3). Cột A (mUSD) ⛔ vào ảnh. "
            "⚠ cột đầu 2024-10-20 (CN) sớm 1 ngày so với spec 21/10/2024 — giữ mốc THẬT của sheet."),
    }


#: Cổng DT5-B1 *(Đ5)*: mọi mã HD ∈ cây ATL 74; mọi LE ∈ 5 khối — DÙNG CHUNG với `cfa1_yhqm`
#: *(`_cfa1.cong_hd`)*. `thieu` = mã/LE LẠ ⇒ ĐỎ *(DT5-B2 chứng minh)*; ⛔ `lac`.
thieu_lac = _cfa1.cong_hd
