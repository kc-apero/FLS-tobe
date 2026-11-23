"""Khuôn đóng băng `gl_hr_413` — ĐÁP ÁN PD 413 · `… | For PL Report` *(sổ P&L)* *(ISP 3.1.2 · Step 23 · DT6)*.

    python tools/dong_bang_sheet.py gl_hr_413 <bản_thô.json> --mong 13087
        ⇒ tests/fixture/dap_an/gl_hr_413.json

⭐ **Nguồn** sổ P&L `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` · tab `Report I H1000 Ledge (HR Allocate HD) Y2025 | For
PL Report` *(20238 × 73)* — `A10` là GIÁ TRỊ dán *(⛔ công thức)* ⇒ **≠ 408** *(đo: 413 ⊃ 408 + 1375 dòng
ở 2024-11/12 · 2025-01 · 2025-04)*.

Phần chung *(soát tiêu đề · che số tài khoản · tập đóng · cổng)* ở `_gl_hr.py`; tệp này chỉ
KHAI `mong` của riêng 413 *(Đ5 — khác ⇒ ĐỎ cả hai chiều)*. Số đo 18/11 *(khoá SA chỉ-đọc; mỗi số
đếm MỘT vật, Đ4)*: 10785 hàng cột A có ngày · 15 kỳ có dòng · kỳ NGOÀI 2025: {202411: 165, 202412: 530, 202601: 269} (⇒ kỳ ⊄ 2025).
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

PD = "413"
BANG = "PD.413"
KHOA = _gl.KHOA
KIEU_KHOA = "dong_sheet"
COT = _gl.COT_SUY
KIEU_COT = dict(_gl.KIEU_COT_SUY)
RA = "tests/fixture/dap_an/gl_hr_413.json"
#: Đ5 — số dòng bảng phụ *(đoạn A-rỗng · hai tab Y2024 thiếu)*.
PHU_MONG = {"doan_trong": 1, "thieu_nguon": 2, "gan_ky": 6}

#: Đ5 — số dòng MỖI KỲ *(đo 18/11)*. Kỳ ngoài 2025 *(nếu có)* ⇒ `lac` CÓ TÊN, cổng IN rõ.
KY_MONG = {202411: 165, 202412: 530, 202501: 693, 202502: 665, 202503: 629, 202504: 1253, 202505: 365, 202506: 1481, 202507: 2020, 202508: 1088, 202509: 1449, 202510: 1140, 202511: 743, 202512: 597, 202601: 269}
#: Đ5 — ô LỖI Sheets theo cột chữ: NGUYÊN chuỗi, ĐẾM *(luật `DT5-R1-04`)*.
LOI_CHU_MONG = {'R': {'#N/A ()': 18}}
#: Đ5 — hàng GÁN KỲ *(DT6b, `WO-225` AC-3; đo 19/11)*: 6 đoạn GIỮA = 2.302 hàng thiếu ngày; kỳ = kỳ hàng
#: có ngày liền TRÊN. Số hàng MỖI KỲ + Σ PS Có *(cột F, tiền)* — khác ⇒ ĐỎ cả hai chiều. `KY_MONG` ĐÃ gồm chúng.
SUY_MONG = {202506: 566, 202507: 335, 202508: 322, 202509: 538, 202510: 276, 202511: 265}
SUY_TONG_F = 6763528503
#: Đ5 — đoạn A-rỗng ĐUÔI `(hàng_sheet_đầu, số_hàng, số_hàng_còn_ô_khác, vị_trí)`.
DOAN_MONG = [(13097, 7142, 7142, 'duoi')]


def chuan_bi(tho):
    return _gl.chuan_bi(tho, PD, suy=True)


def thieu_lac(dong):
    return _gl.thieu_lac(dong, pd=PD, ky_mong=KY_MONG, loi_mong=LOI_CHU_MONG, doan_mong=DOAN_MONG,
                         suy_mong=SUY_MONG, suy_f_mong=SUY_TONG_F)
