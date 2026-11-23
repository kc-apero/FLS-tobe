"""Khuôn đóng băng `gl_hr_407` — ĐÁP ÁN PD 407 · `Report I H1000 Ledge (HR Allocate HD) Y2025` *(sổ CF, tab gom bốn tab H1000 bằng `QUERY`)* *(ISP 3.1.2 · Step 23 · DT6)*.

    python tools/dong_bang_sheet.py gl_hr_407 <bản_thô.json> --mong 9421
        ⇒ tests/fixture/dap_an/gl_hr_407.json

⭐ **Nguồn** `[COPY] Report I General Ledger | CF report` · id `12S00TnFMd9Uz0g-NLvOA7kdmPPhY1V_SVOQJkDi1ZiU`
sheet `Report I H1000 Ledge (HR Allocate HD) Y2025` *(19238 × 67)*. Công thức `A10` = `sort(QUERY({Y2025 NIS/INT/COM;
Y2025 PIT; Y2024 NIS/INT/COM; Y2024 PIT}…))` — hai tab Y2024 đi bằng IMPORTRANGE ⇒ `#REF!` ⇒ **thiếu Y2024**.

Phần chung *(soát tiêu đề · che số tài khoản · tập đóng · cổng)* ở `_gl_hr.py`; tệp này chỉ
KHAI `mong` của riêng 407 *(Đ5 — khác ⇒ ĐỎ cả hai chiều)*. Số đo 18/11 *(khoá SA chỉ-đọc; mỗi số
đếm MỘT vật, Đ4)*: 9421 hàng cột A có ngày · 13 kỳ có dòng · kỳ NGOÀI 2025: {202601: 269} (⇒ kỳ ⊄ 2025).
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

_P = pathlib.Path(__file__).resolve().parent / "_gl_hr.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__gl_hr", _P)
_gl = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _gl
_spec.loader.exec_module(_gl)

PD = "407"
BANG = "PD.407"
KHOA = _gl.KHOA
KIEU_KHOA = "dong_sheet"
COT = _gl.COT
KIEU_COT = dict(_gl.KIEU_COT)
RA = "tests/fixture/dap_an/gl_hr_407.json"
#: Đ5 — số dòng bảng phụ *(đoạn A-rỗng · hai tab Y2024 thiếu)*.
PHU_MONG = {"doan_trong": 1, "thieu_nguon": 2}

#: Đ5 — số dòng MỖI KỲ *(đo 18/11)*. Kỳ ngoài 2025 *(nếu có)* ⇒ `lac` CÓ TÊN, cổng IN rõ.
KY_MONG = {202501: 225, 202502: 667, 202503: 629, 202504: 1041, 202505: 365, 202506: 916, 202507: 1685, 202508: 767, 202509: 912, 202510: 868, 202511: 478, 202512: 599, 202601: 269}
#: Đ5 — ô LỖI Sheets theo cột chữ: NGUYÊN chuỗi, ĐẾM *(luật `DT5-R1-04`)*.
LOI_CHU_MONG = {'P': {'#N/A': 11}}
#: Đ5 — đoạn A-rỗng `(hàng_sheet_đầu, số_hàng, số_hàng_còn_ô_khác, vị_trí)`.
DOAN_MONG = [(9431, 9808, 9808, 'duoi')]


def chuan_bi(tho):
    return _gl.chuan_bi(tho, PD)


def thieu_lac(dong):
    return _gl.thieu_lac(dong, pd=PD, ky_mong=KY_MONG, loi_mong=LOI_CHU_MONG, doan_mong=DOAN_MONG)
