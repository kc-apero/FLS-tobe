"""Khuôn đóng băng `ccr_daily_report_song` — ĐÁP ÁN PD 615 *(tab `5. Daily Report` của `A-CCR_V2_Working`)* chụp LẠI từ NGUỒN SỐNG
*(ISP 3.1.2 · `WO-353` C3 = ⓐ, chủ 23/11)*. Thân = `_dr_luoi.py` *(chung 4 khuôn H14, ⛔ sửa)*; chỉ KHAI LẠI hình nguồn + `mong`.

    python tools/dong_bang_sheet.py ccr_daily_report_song <bản_thô.json> --mong <số dòng ảnh> \
        --ra tests/fixture/dap_an/ccr_daily_report_20261123.json

⭐ Vì sao một tệp KHUÔN MỚI *(⛔ sửa `ccr_daily_report.py`)*: khuôn cũ là cổng của ảnh CŨ 22/11 *(2.502 hàng · biên bản — Đ2)*;
bài `tests/du_lieu/test_dap_an_report_h14.py` chạy `thieu_lac` của nó lên ảnh ấy. Sửa tại chỗ thì biên bản mất cổng.
⭐ WO-345 đo: nguồn sống **2.566** hàng *(+64)* ⇒ khuôn cũ TỪ CHỐI `values phải 2502 hàng`. Ở đây `N_HANG` khai lại = số đo
lượt 2 ngày 23/11 *(cùng lượt với DR2 + 2 tab số dư — `WO-353` AC-3)*; mọi `mong` dưới là SỐ ĐO lượt ấy, số CŨ 22/11 ở chú thích.
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
RA = "tests/fixture/dap_an/ccr_daily_report_20261123.json"
COT = _g.COT
KIEU_COT = _g.KIEU_COT
#: WO-353 — 22/11: `n_hang=2502` *(khuôn `ccr_daily_report`)*; 23/11 lượt 2: **2566**.
CH = _g.CauHinh(n_hang=2566, n_dau=10, vung="A1:AR12521")

#: ⭐ Đ5 — đo 23/11 lượt 2 rồi khai *(WO-353)*; khác ⇒ ĐỎ cả hai chiều. Ô lỗi Sheets ở vùng giá trị: **120** *(22/11: 127)*.
#: 22/11 *(khuôn cũ)*: j {'#N/A': 2, '#REF!': 5} · m/w/z {'#N/A': 1} · o/r/t {'#DIV/0!': 14, '#N/A': 2, '#REF!': 1} — tổng 127.
LOI_MONG: dict[str, Any] = {'f': {'#VALUE!': 9}, 'g': 0, 'h': {'#N/A': 1, '#REF!': 2}, 'i': {'#N/A': 1, '#REF!': 5}, 'j': {'#N/A': 1, '#REF!': 5}, 'k': 0, 'l': 0, 'm': 0, 'n': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 'o': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 'p': 0, 'q': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 'r': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 's': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 't': {'#DIV/0!': 14, '#N/A': 1, '#REF!': 1}, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0, 'aa': 0, 'ab': 0, 'ac': 0, 'ad': 0, 'ae': 0, 'af': 0, 'ag': 0, 'ah': 0, 'ai': 0, 'aj': 0, 'ak': 0, 'al': 0}
#: 22/11: `tieu_de` 1792 — +585 ô tiêu đề *(hàng mới cuối lưới mang chữ ⇒ vào tiêu đề)*; 2 bảng phụ kia ⛔ đổi.
PHU_MONG = {'tieu_de': 2377, 'dong_chi_nhan': 230, 'o_khong_so': 56}
#: số ô SỐ ≠ rỗng *(⛔ ô lỗi)* THEO CỘT `f…al` — tổng **48021** *(23/11 lượt 2 = 22/11, từng cột)*.
MONG_COT: dict[str, int] = {'f': 52, 'g': 1992, 'h': 2028, 'i': 2029, 'j': 2029, 'k': 2034, 'l': 1979, 'm': 1979, 'n': 1862, 'o': 1861, 'p': 1880, 'q': 1863, 'r': 1862, 's': 1862, 't': 1861, 'u': 1874, 'v': 1875, 'w': 1874, 'x': 1875, 'y': 1874, 'z': 986, 'aa': 975, 'ab': 873, 'ac': 975, 'ad': 976, 'ae': 819, 'af': 819, 'ag': 922, 'ah': 922, 'ai': 922, 'aj': 922, 'ak': 922, 'al': 443}
#: hàng · ô theo `phan:khoi` *(Đ4: `phan` = vết đoạn, `khoi` = mã khối — ⛔ nghĩa kế toán)*.
MONG_DONG: dict[str, tuple[int, int]] = {'-:-': (35, 1078), 'CB I Cash Balance by LE I Legal Entity by Currency:-': (47, 1497), 'Raw Data Management:Type': (3, 51), 'Raw Data Management:P100': (57, 1100), 'Unit: mUSD:-': (3, 93), 'Unit: mUSD:GROUP': (75, 2325), 'Unit: mUSD:SGO2': (80, 2480), 'Unit: mUSD:SGO1': (80, 2480), 'Unit: mUSD:HGO2': (80, 2480), 'Unit: mUSD:BGO2': (80, 2480), 'CM Cumulative:-': (1, 2), 'CM Cumulative:GROUP': (68, 2176), 'CM Cumulative:SGO2': (68, 2176), 'CM Cumulative:SGO1': (68, 2176), 'CM Cumulative:HGO2': (68, 2176), 'CM Cumulative:BGO2': (68, 2176), 'Unit: person:-': (1, 2), 'Unit: person:GROUP': (111, 3147), 'Unit: person:[FS1][PLA3] GROUP': (74, 1202), 'Unit: person:[FS2][PLA3] GROUP': (75, 1353), 'Unit: person:[FS1][PLA3] CVL': (76, 1210), 'Unit: person:[FS2][PLA3] CVL': (76, 1354), 'Unit: person:[FS1][PLA3] COR': (76, 1210), 'Unit: person:[FS2][PLA3] COR': (76, 1354), 'Unit: person:[FS1][PLA3] CSM': (76, 1210), 'Unit: person:[FS2][PLA3] CSM': (76, 1354), 'Unit: person:[FS1][PLA3] CAH': (76, 1210), 'Unit: person:[FS2][PLA3] CAH': (76, 1354), 'Unit: person:[FS1][PLA3] ASA': (76, 1210), 'Unit: person:[FS2][PLA3] ASA': (76, 1354), 'Unit: person:[FS1][PLA3] SHQ': (76, 1210), 'Unit: person:[FS2][PLA3] SHQ': (78, 1461)}
#: 22/11 có thêm `'Daily Transactions:No': (1, 7)` — 23/11 hàng ấy mang chữ ở G…AL ⇒ vào `tieu_de` *(dòng bảng chính 2.057 → 2.056)*.
#: cột `f…al` có 0 ô số/lỗi ở bảng chính — có tên.
CHUA_CO_DU_LIEU: tuple[str, ...] = ()


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    return _g.chuan_bi(tho, CH, "5. Daily Report (PD 615)")


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    return _g.thieu_lac(dong, MONG_COT, MONG_DONG, CHUA_CO_DU_LIEU, "5. Daily Report (PD 615)")
