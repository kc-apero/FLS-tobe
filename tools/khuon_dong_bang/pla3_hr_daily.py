"""Khuôn đóng băng `pla3_hr_daily` — ĐÁP ÁN 416 · `[MID] Report I PLA3 Daily | HR Only` *(PLA3 HR only · Daily)*.

    python tools/dong_bang_sheet.py pla3_hr_daily <bản_thô.json> --mong <N>
        ⇒ tests/fixture/dap_an/pla3_hr_daily.json

⭐ ISP 3.1.2 · Step 31 · DT7 *(`WO-261`)* · AP v3.1.2 §3.3.1 PD 416. Bộ máy chung ở `_pla.py`.
Hợp đồng bản thô = LƯỚI SA *(⛔ commit)*. Số đo: `BG-262` + `tests/du_lieu/test_dap_an_pla.py`.
Sáu ảnh *(⛔ ba)*: công cụ đóng băng MỘT lưới ↔ MỘT ảnh, mà Daily và Y/H/Q/M là hai lưới khác
trục — cùng tiền lệ `cfa1_daily`/`cfa1_yhqm`.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "_pla.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__pla", _P)
_pla = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _pla
_spec.loader.exec_module(_pla)

BANG = "PD.416"
KHOA = "o_id"
KIEU_KHOA = "ma"
COT = ("le", "ma_hd", "ngay", "gt")
KIEU_COT = {"le": "chu", "ma_hd": "chu", "ngay": "so", "gt": "so"}
RA = "tests/fixture/dap_an/pla3_hr_daily.json"
#: Đ5 — mong khai SAU lần đo đầu *(20/11)*; đổi ⇒ cổng ĐỎ, buộc ghi lại.
PHU_MONG = {"hd": 888, "le": 12, "ngay_truc": 496, "o_loi": 60, "hang_khong_nhan": 0, "tuong_lai_chu": 0}
O_LOI_GIA = {"-": 60}
#: Đ5 — ô CHỮ ở cột TƯƠNG LAI bị cắt, phân bố theo giá *(xem `_pla.kiem_tuong_lai_rong`)*.
TL_CHU_GIA = {}
LE_MONG = _pla.LE12
TEN_PD = "[MID] Report I PLA3 Daily | HR Only"


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    return _pla.chuan_bi_chung(tho, kieu="ngay", le_mong=LE_MONG, ten_pd=TEN_PD,
                               o_loi_gia=O_LOI_GIA, tl_chu_gia=TL_CHU_GIA)


#: Cổng DT7 dùng chung *(`_pla.cong`)*.
thieu_lac = _pla.cong
