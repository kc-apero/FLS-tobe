"""Khuôn đóng băng `ccr_so_du_cash` — ĐẦU VÀO của PD 615 = tab `2. CCR Cash` của sổ `A-CCR_V2_Working` (id `1ycMOKKZg5rraLAYW-HuZDp9k3RPzr0H-iyPs_0IKL5Q`)
*(ISP 3.1.2 · DT13 · `WO-319` · số dư tiền theo (thực thể × ngân hàng × tiền tệ) × ngày — khối `CB` của `5. Daily Report`)*.

    python tools/dong_bang_sheet.py ccr_so_du_cash <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dau_vao/ccr_so_du_cash.json

Vùng đọc `A1:ABM240` ⇒ API trả **175 hàng × 719 cột** *(cắt hàng cuối rỗng)*. Thân + PII + lý do: xem `_ccr_so_du.py`
*(⛔ đọc cột E số TK · G · H `ID` · I `Pass` · J)*. Hợp đồng bản thô *(phiên cloud, khoá SA chỉ-đọc, ⛔ commit)*:
`{nguon, doc_luc, cach_doc, values}`.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "_ccr_so_du.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__ccr_so_du", _P)
_g = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _g
    _spec.loader.exec_module(_g)

BANG = "DAU_VAO.CCR_SO_DU_CASH"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
RA = "tests/fixture/dau_vao/ccr_so_du_cash.json"
COT = _g.COT
KIEU_COT = _g.KIEU_COT
PHU_MONG = {"ngay_cot": 31, "dong_chi_nhan": 7}
TAB, N_HANG, N_COT = "2. CCR Cash", 175, 719

#: ⭐ Đ5 — đo 22/11 rồi khai; khác ⇒ ĐỎ cả hai chiều. `o_so` = ô SỐ ≠ rỗng *(31 ngày × `hang`)*; `theo_ngay` = ô số MỖI ngày.
MONG: dict[str, Any] = {"hang": 62, "o_so": 1922, "theo_ngay": (62,) * 31, "ngay_0_o": (),
                       "nhan_che": ('TK_CA_NHAN_1',)}


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    return _g.chuan_bi(tho, TAB, N_HANG, N_COT)


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    return _g.thieu_lac(dong, MONG, "ccr_so_du_cash")
