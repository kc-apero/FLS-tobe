"""Khuôn đóng băng `ccr_daily_report_2_song` — ĐẦU VÀO của PD 615 *(tab `5. Daily Report 2` của `A-CCR_V2_Working`)* chụp LẠI từ
NGUỒN SỐNG, CÙNG lượt với đáp án 615 + 2 tab số dư *(ISP 3.1.2 · `WO-353` C3 = ⓐ, chủ 23/11)*.

    python tools/dong_bang_sheet.py ccr_daily_report_2_song <bản_thô.json> --mong <số dòng ảnh> \\
        --ra tests/fixture/dau_vao/ccr_daily_report_2_20261123.json

⭐ Vì sao một tệp KHUÔN MỚI *(⛔ sửa `ccr_daily_report_2.py`)*: khuôn cũ là cổng của ảnh CŨ 22/11 *(biên bản — Đ2)*. Thân, rào,
`MONG_AK` · `MONG_DONG` · `LOI_MONG` · `PHU_MONG` · `CHUA_CO_DU_LIEU` = khuôn cũ *(đo 23/11 lượt 2: TRÙNG — ⛔ khai hai chỗ, đọc
thẳng)*; CHỈ `MONG_CHECK` khai lại: **WO-345 đo** cổng cũ ĐỎ `thiếu 2` *(ngày 2026-11-22 mới có số ở `ngay:GROUP` · `ngay:SGO2`
— CHECK ① NB ≠ 0)*. Số CŨ 22/11 ở chú thích từng chỗ đổi.
⛔ RÀO: cùng `DAU_VAO_CHO` / `CAM_CHO` với khuôn cũ *(ảnh này trùng đáp án 610 như ảnh cũ ⇒ CHỈ cho 615)* — `_rao_dau_vao.ANH_CO_RAO`
khai thêm tên khuôn này.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "ccr_daily_report_2.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang_ccr_daily_report_2", _P)
_c2 = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _c2
    _spec.loader.exec_module(_c2)
_d2 = _c2._d2

DAU_VAO_CHO = _c2.DAU_VAO_CHO
CAM_CHO = _c2.CAM_CHO
BANG = _c2.BANG
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
RA = "tests/fixture/dau_vao/ccr_daily_report_2_20261123.json"
COT = _c2.COT
KIEU_COT = _c2.KIEU_COT
LOI_MONG = _c2.LOI_MONG
PHU_MONG = dict(_c2.PHU_MONG)
chuan_bi = _c2.chuan_bi

#: ⭐ Đ5 — đo 23/11 lượt 2 *(WO-353)* rồi khai. Khác khuôn cũ ĐÚNG hai ô `nb_khac_0` — thêm ngày `2026-11-22`:
#:    `ngay:GROUP` 22/11: 9 ngày *(…@2026-11-18)* ⇒ 10 · `ngay:SGO2` 22/11: `('ngay:SGO2@2026-11-10',)` ⇒ 2.
MONG_CHECK: dict[str, dict[str, Any]] = {k: dict(v) for k, v in _c2.MONG_CHECK.items()}
MONG_CHECK["ngay:GROUP"]["nb_khac_0"] = (*_c2.MONG_CHECK["ngay:GROUP"]["nb_khac_0"], "ngay:GROUP@2026-11-22")
MONG_CHECK["ngay:SGO2"]["nb_khac_0"] = (*_c2.MONG_CHECK["ngay:SGO2"]["nb_khac_0"], "ngay:SGO2@2026-11-22")
MONG_AK = _c2.MONG_AK
MONG_DONG = _c2.MONG_DONG
CHUA_CO_DU_LIEU = _c2.CHUA_CO_DU_LIEU


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5)* = `ccr_daily_report_2.thieu_lac` với `MONG_CHECK` của ảnh này *(tạm thay trong lời gọi, trả nguyên sau)*."""
    goc = _c2.MONG_CHECK
    _c2.MONG_CHECK = MONG_CHECK
    try:
        return _c2.thieu_lac(dong)
    finally:
        _c2.MONG_CHECK = goc
