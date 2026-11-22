"""Khuôn đóng băng `daily_report_3_fs1` — ĐÁP ÁN PD 608 = tab `[FS1]5. Daily Report 3` của sổ `[COPY] Report I General Ledger | P&L Report` (id `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g`)
*(ISP 3.1.2 · Step 41 · DT11 · vòng sửa `KQ-271` `DT11-R1-02` — đáp án còn thiếu cho H14)*.

    python tools/dong_bang_sheet.py daily_report_3_fs1 <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dap_an/daily_report_3_fs1.json

Vùng đọc `A1:AN1092` ⇒ API trả **1092 hàng** *(cắt hàng cuối rỗng)*. Lưới + cách ghi ô: xem `_dr_luoi.py` *(thân chung của 4
khuôn H14 — ⛔ sửa khuôn/ảnh DR2 · DR3 đã có)*. `N_DAU = 10`: hàng sheet ≤ 10 là tiêu đề.
Hợp đồng bản thô *(phiên cloud, khoá SA chỉ-đọc, ⛔ commit)*: `{nguon, doc_luc, cach_doc, values}`.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "_dr_luoi.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__dr_luoi", _P)
_g = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _g
    _spec.loader.exec_module(_g)

BANG = "DAP_AN.DAILY_REPORT_3_FS1"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
RA = "tests/fixture/dap_an/daily_report_3_fs1.json"
COT = _g.COT
KIEU_COT = _g.KIEU_COT
CH = _g.CauHinh(n_hang=1092, n_dau=10, vung="A1:AN1092")

#: ⭐ Đ5 — đo 22/11 rồi khai; khác ⇒ ĐỎ cả hai chiều. Ô lỗi Sheets ở vùng giá trị: **0** *(0 RÕ RÀNG cho cột không lỗi)*.
LOI_MONG: dict[str, Any] = {'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0, 'aa': 0, 'ab': 0, 'ac': 0, 'ad': 0, 'ae': 0, 'af': 0, 'ag': 0, 'ah': 0, 'ai': 0, 'aj': 0, 'ak': 0, 'al': 0}
PHU_MONG = {'tieu_de': 1930, 'dong_chi_nhan': 58, 'o_khong_so': 240}
#: số ô SỐ ≠ rỗng *(⛔ ô lỗi)* THEO CỘT `f…al` — tổng **17962**.
MONG_COT: dict[str, int] = {'f': 0, 'g': 921, 'h': 921, 'i': 921, 'j': 921, 'k': 921, 'l': 921, 'm': 921, 'n': 400, 'o': 795, 'p': 795, 'q': 795, 'r': 795, 's': 400, 't': 400, 'u': 400, 'v': 400, 'w': 400, 'x': 400, 'y': 795, 'z': 395, 'aa': 395, 'ab': 395, 'ac': 395, 'ad': 395, 'ae': 395, 'af': 395, 'ag': 395, 'ah': 395, 'ai': 395, 'aj': 395, 'ak': 395, 'al': 0}
#: hàng · ô theo `phan:khoi` *(Đ4: `phan` = vết đoạn, `khoi` = mã khối — ⛔ nghĩa kế toán)*.
MONG_DONG: dict[str, tuple[int, int]] = {'-:GROUP': (75, 1800), '-:SGO2': (80, 1920), '-:SGO1': (80, 1920), '-:HGO2': (80, 1920), '-:BGO2': (80, 1920), 'CM Cumulative:GROUP': (76, 1228), 'CM Cumulative:CVL': (75, 1209), 'CM Cumulative:COR': (75, 1209), 'CM Cumulative:CSM': (75, 1209), 'CM Cumulative:CAH': (75, 1209), 'CM Cumulative:ASA': (75, 1209), 'CM Cumulative:SHQ': (75, 1209)}
#: cột `f…al` có 0 ô số/lỗi ở bảng chính — có tên.
CHUA_CO_DU_LIEU: tuple[str, ...] = ('F', 'AL')


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    return _g.chuan_bi(tho, CH, "[FS1]5. Daily Report 3 (PD 608)")


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    return _g.thieu_lac(dong, MONG_COT, MONG_DONG, CHUA_CO_DU_LIEU, "[FS1]5. Daily Report 3 (PD 608)")
