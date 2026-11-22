"""Khuôn đóng băng `sign_off_dau_vao` — ĐẦU VÀO của luỹ kế FS1 *(PD 608)* = tab `[MID][FS1][PLA5]5. Daily Report 3 (Sign off)`
của sổ `[COPY] Report I General Ledger | P&L Report` *(id `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g`)*
*(ISP 3.1.2 · DT13 · `WO-319` · `BG-312` §"FS1 luỹ kế DỪNG")*.

    python tools/dong_bang_sheet.py sign_off_dau_vao <bản_thô.json> --mong 94
        ⇒ tests/fixture/dau_vao/sign_off_dau_vao.json

⭐ **Vì sao.** `[FS1]5. Daily Report 3` `CM Cumulative` *(đo 22/11 `FORMULA`)*: khối CDT 233/1.209 ô và `GROUP` 197/1.300 ô là
`='[MID][FS1][PLA5]5. Daily Report 3 (Sign off)'!<ô> / sumifs('9.2.Exchange Rate'!$B:$B,'9.2.Exchange Rate'!$A:$A,<tháng>) / 10^6`;
các ô còn lại là `='[FS2]5. Daily Report 3'!…` *(ảnh 607)* · `ATL` · `Allocation Table | By NOEM & By GI` *(ảnh `alloc_noem_gi`)*.
Tab Sign off **dán GIÁ TRỊ — 0 công thức** *(đo 22/11: 0/18.536… ô; không có thượng nguồn trong sổ ⇒ nguồn (b))*, và đã đóng băng
làm ĐÁP ÁN 605 *(`dap_an/daily_report_3.json`, DT11)*. Engine cấm đọc đáp án *(bài `test_AC4_engine_khong_doc_dap_an`)* ⇒ cần bản
**ĐẦU VÀO** riêng *(cùng lưới, cùng giá trị — đo ở `test_dau_vao_dt13`: trùng từng ô với ảnh đáp án ở ngày đóng băng)*.
Tái dùng NGUYÊN thân `daily_report_3.chuan_bi/thieu_lac` *(⛔ chép)*; chỉ đổi `BANG` · `RA`.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

_P = pathlib.Path(__file__).resolve().parent / "daily_report_3.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang_daily_report_3", _P)
_d3 = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _d3
    _spec.loader.exec_module(_d3)

BANG = "DAU_VAO.SIGN_OFF"
KHOA = _d3.KHOA
KIEU_KHOA = _d3.KIEU_KHOA
RA = "tests/fixture/dau_vao/sign_off_dau_vao.json"
COT = _d3.COT
KIEU_COT = _d3.KIEU_COT
LOI_MONG = _d3.LOI_MONG
PHU_MONG = _d3.PHU_MONG
chuan_bi = _d3.chuan_bi
thieu_lac = _d3.thieu_lac
