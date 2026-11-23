"""Khuôn đóng băng `ccr_daily_report` — ĐÁP ÁN PD 615 = tab `5. Daily Report` của sổ `A-CCR_V2_Working` (id `1ycMOKKZg5rraLAYW-HuZDp9k3RPzr0H-iyPs_0IKL5Q`)
*(ISP 3.1.2 · Step 41 · DT11 · vòng sửa `KQ-271` `DT11-R1-02` — đáp án còn thiếu cho H14)*.

    python tools/dong_bang_sheet.py ccr_daily_report <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dap_an/ccr_daily_report.json

Vùng đọc `A1:AR12521` ⇒ API trả **2502 hàng** *(cắt hàng cuối rỗng)*. Lưới + cách ghi ô: xem `_dr_luoi.py` *(thân chung của 4
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

BANG = "DAP_AN.CCR_DAILY_REPORT"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
RA = "tests/fixture/dap_an/ccr_daily_report.json"
COT = _g.COT
KIEU_COT = _g.KIEU_COT
CH = _g.CauHinh(n_hang=2502, n_dau=10, vung="A1:AR12521")

#: ⭐ Đ5 — đo 22/11 rồi khai; khác ⇒ ĐỎ cả hai chiều. Ô lỗi Sheets ở vùng giá trị: **127** *(0 RÕ RÀNG cho cột không lỗi)*.
LOI_MONG: dict[str, Any] = {'f': {'#VALUE!': 9}, 'g': 0, 'h': {'#N/A': 1, '#REF!': 2}, 'i': {'#N/A': 1, '#REF!': 5}, 'j': {'#N/A': 2, '#REF!': 5}, 'k': 0, 'l': 0, 'm': {'#N/A': 1}, 'n': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 'o': {'#DIV/0!': 14, '#N/A': 2, '#REF!': 1}, 'p': 0, 'q': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 'r': {'#DIV/0!': 14, '#N/A': 2, '#REF!': 1}, 's': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 't': {'#DIV/0!': 14, '#N/A': 2, '#REF!': 1}, 'u': 0, 'v': 0, 'w': {'#N/A': 1}, 'x': 0, 'y': 0, 'z': {'#N/A': 1}, 'aa': 0, 'ab': 0, 'ac': 0, 'ad': 0, 'ae': 0, 'af': 0, 'ag': 0, 'ah': 0, 'ai': 0, 'aj': 0, 'ak': 0, 'al': 0}
PHU_MONG = {'tieu_de': 1792, 'dong_chi_nhan': 230, 'o_khong_so': 56}
#: số ô SỐ ≠ rỗng *(⛔ ô lỗi)* THEO CỘT `f…al` — tổng **48021**.
MONG_COT: dict[str, int] = {'f': 52, 'g': 1992, 'h': 2028, 'i': 2029, 'j': 2029, 'k': 2034, 'l': 1979, 'm': 1979, 'n': 1862, 'o': 1861, 'p': 1880, 'q': 1863, 'r': 1862, 's': 1862, 't': 1861, 'u': 1874, 'v': 1875, 'w': 1874, 'x': 1875, 'y': 1874, 'z': 986, 'aa': 975, 'ab': 873, 'ac': 975, 'ad': 976, 'ae': 819, 'af': 819, 'ag': 922, 'ah': 922, 'ai': 922, 'aj': 922, 'ak': 922, 'al': 443}
#: hàng · ô theo `phan:khoi` *(Đ4: `phan` = vết đoạn, `khoi` = mã khối — ⛔ nghĩa kế toán)*.
MONG_DONG: dict[str, tuple[int, int]] = {'-:-': (35, 1078), 'CB I Cash Balance by LE I Legal Entity by Currency:-': (47, 1497), 'Raw Data Management:Type': (3, 51), 'Raw Data Management:P100': (57, 1100), 'Unit: mUSD:-': (3, 93), 'Unit: mUSD:GROUP': (75, 2325), 'Unit: mUSD:SGO2': (80, 2480), 'Unit: mUSD:SGO1': (80, 2480), 'Unit: mUSD:HGO2': (80, 2480), 'Unit: mUSD:BGO2': (80, 2480), 'CM Cumulative:-': (1, 2), 'CM Cumulative:GROUP': (68, 2176), 'CM Cumulative:SGO2': (68, 2176), 'CM Cumulative:SGO1': (68, 2176), 'CM Cumulative:HGO2': (68, 2176), 'CM Cumulative:BGO2': (68, 2176), 'Unit: person:-': (1, 2), 'Unit: person:GROUP': (111, 3147), 'Unit: person:[FS1][PLA3] GROUP': (74, 1202), 'Unit: person:[FS2][PLA3] GROUP': (75, 1353), 'Unit: person:[FS1][PLA3] CVL': (76, 1210), 'Unit: person:[FS2][PLA3] CVL': (76, 1354), 'Unit: person:[FS1][PLA3] COR': (76, 1210), 'Unit: person:[FS2][PLA3] COR': (76, 1354), 'Unit: person:[FS1][PLA3] CSM': (76, 1210), 'Unit: person:[FS2][PLA3] CSM': (76, 1354), 'Unit: person:[FS1][PLA3] CAH': (76, 1210), 'Unit: person:[FS2][PLA3] CAH': (76, 1354), 'Unit: person:[FS1][PLA3] ASA': (76, 1210), 'Unit: person:[FS2][PLA3] ASA': (76, 1354), 'Unit: person:[FS1][PLA3] SHQ': (76, 1210), 'Unit: person:[FS2][PLA3] SHQ': (78, 1461), 'Daily Transactions:No': (1, 7)}
#: cột `f…al` có 0 ô số/lỗi ở bảng chính — có tên.
CHUA_CO_DU_LIEU: tuple[str, ...] = ()


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    return _g.chuan_bi(tho, CH, "5. Daily Report (PD 615)")


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    return _g.thieu_lac(dong, MONG_COT, MONG_DONG, CHUA_CO_DU_LIEU, "5. Daily Report (PD 615)")
