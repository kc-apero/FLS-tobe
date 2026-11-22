"""Khuôn đóng băng `ccr_daily_report_2` — ĐẦU VÀO của PD 615 = tab `5. Daily Report 2` của sổ `A-CCR_V2_Working`
(id `1ycMOKKZg5rraLAYW-HuZDp9k3RPzr0H-iyPs_0IKL5Q`) *(ISP 3.1.2 · DT13 · `WO-319`)*.

    python tools/dong_bang_sheet.py ccr_daily_report_2 <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dau_vao/ccr_daily_report_2.json

⭐ **Vì sao.** Khối `Unit: mUSD` *(GROUP 2.400 · SGO2/SGO1/HGO2/BGO2 mỗi khối 2.560 ô công thức)* · `CM Cumulative` *(GROUP 2.176 ·
SGO2 2.104 · SGO1/HGO2 1.360 · BGO2 1.354)* · `Unit: person GROUP` *(3.552)* của `5. Daily Report` *(615)* là `='5. Daily Report 2'!…`
*(đo 22/11 `FORMULA`: MỌI công thức của các khối ấy tham chiếu CHÍNH tab này)* — và tab này của A-CCR là **dán GIÁ TRỊ: 26.459 ô số hằng ·
31 công thức chỉ ở hàng 1 `=G5=$C$1` *(đo `FORMULA`)* ⇒ nguồn **KHÁC** bản `[COPY] … CF report` đã đóng băng
`daily_report_2` *(DT11)*: BG-270 §6 đo 1.120 ô lệch ⇒ ⛔ dùng ảnh DT11 thay. Cùng lưới `A1:AR1114` ⇒ **tái dùng NGUYÊN** thân
`daily_report_2.chuan_bi` *(⛔ chép — `chuan_bi` tải bằng đường tệp, như `_dr_luoi`)*; chỉ KHAI LẠI `MONG_*` theo ảnh này.
Bản A-CCR `5. Daily Report 3` **⛔ cần ảnh mới**: 35.542/35.542 ô số khớp từng ô ảnh `daily_report_3_gop` *(đo 22/11)*.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "daily_report_2.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang_daily_report_2", _P)
_d2 = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _d2
    _spec.loader.exec_module(_d2)

BANG = "DAU_VAO.CCR_DAILY_REPORT_2"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
RA = "tests/fixture/dau_vao/ccr_daily_report_2.json"
COT = _d2.COT
KIEU_COT = _d2.KIEU_COT
LOI_MONG = _d2.LOI_MONG
PHU_MONG = {"tieu_de": 356, "dong_chi_nhan": 84}
chuan_bi = _d2.chuan_bi

#: ⭐ Đ5 — đo 22/11 trên bản A-CCR rồi khai *(KHÁC `daily_report_2.MONG_CHECK`: `ngay:GROUP` đạt ② 0=0 23 ≠ 24)*.
MONG_CHECK: dict[str, dict[str, Any]] = {
    'ngay:GROUP': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': ('ngay:GROUP@2026-11-04', 'ngay:GROUP@2026-11-05', 'ngay:GROUP@2026-11-09', 'ngay:GROUP@2026-11-10', 'ngay:GROUP@2026-11-11', 'ngay:GROUP@2026-11-13', 'ngay:GROUP@2026-11-14', 'ngay:GROUP@2026-11-16', 'ngay:GROUP@2026-11-18'), 'cb_do': 30, 'cb_dat': 23, 'cb_dat_co_so': 0, 'cb_dat_0_0': 23, 'cb_khong_dat': ('ngay:GROUP@2026-11-02', 'ngay:GROUP@2026-11-03', 'ngay:GROUP@2026-11-05', 'ngay:GROUP@2026-11-09', 'ngay:GROUP@2026-11-10', 'ngay:GROUP@2026-11-11', 'ngay:GROUP@2026-11-16'), 'cb_khong_do': 0},
    'ngay:SGO2': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': ('ngay:SGO2@2026-11-10',), 'cb_do': 30, 'cb_dat': 29, 'cb_dat_co_so': 0, 'cb_dat_0_0': 29, 'cb_khong_dat': ('ngay:SGO2@2026-11-10',), 'cb_khong_do': 0},
    'ngay:SGO1': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': ('ngay:SGO1@2026-11-04', 'ngay:SGO1@2026-11-10', 'ngay:SGO1@2026-11-13'), 'cb_do': 30, 'cb_dat': 29, 'cb_dat_co_so': 0, 'cb_dat_0_0': 29, 'cb_khong_dat': ('ngay:SGO1@2026-11-09',), 'cb_khong_do': 0},
    'ngay:HGO2': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 30, 'cb_dat': 30, 'cb_dat_co_so': 0, 'cb_dat_0_0': 30, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:BGO2': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 30, 'cb_dat': 30, 'cb_dat_co_so': 0, 'cb_dat_0_0': 30, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'luy_ke:GROUP': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:GROUP@2025-Y', 'luy_ke:GROUP@2025-H1', 'luy_ke:GROUP@2025-H2', 'luy_ke:GROUP@2025-Q1', 'luy_ke:GROUP@2025-Q2', 'luy_ke:GROUP@2025-Q3', 'luy_ke:GROUP@2025-Q4', 'luy_ke:GROUP@2025-M01', 'luy_ke:GROUP@2025-M02', 'luy_ke:GROUP@2025-M03', 'luy_ke:GROUP@2025-M04', 'luy_ke:GROUP@2025-M05', 'luy_ke:GROUP@2025-M06', 'luy_ke:GROUP@2025-M07', 'luy_ke:GROUP@2025-M08', 'luy_ke:GROUP@2025-M09', 'luy_ke:GROUP@2025-M10', 'luy_ke:GROUP@2025-M11', 'luy_ke:GROUP@2025-M12', 'luy_ke:GROUP@2026-Y', 'luy_ke:GROUP@2026-H1', 'luy_ke:GROUP@2026-H2', 'luy_ke:GROUP@2026-Q1', 'luy_ke:GROUP@2026-Q2', 'luy_ke:GROUP@2026-Q3', 'luy_ke:GROUP@2026-Q4', 'luy_ke:GROUP@2026-M01', 'luy_ke:GROUP@2026-M02', 'luy_ke:GROUP@2026-M03', 'luy_ke:GROUP@2026-M04', 'luy_ke:GROUP@2026-M05', 'luy_ke:GROUP@2026-M06'), 'cb_do': 32, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': ('luy_ke:GROUP@2025-Y', 'luy_ke:GROUP@2025-H1', 'luy_ke:GROUP@2025-H2', 'luy_ke:GROUP@2025-Q1', 'luy_ke:GROUP@2025-Q2', 'luy_ke:GROUP@2025-Q3', 'luy_ke:GROUP@2025-Q4', 'luy_ke:GROUP@2025-M01', 'luy_ke:GROUP@2025-M02', 'luy_ke:GROUP@2025-M03', 'luy_ke:GROUP@2025-M04', 'luy_ke:GROUP@2025-M05', 'luy_ke:GROUP@2025-M06', 'luy_ke:GROUP@2025-M07', 'luy_ke:GROUP@2025-M08', 'luy_ke:GROUP@2025-M09', 'luy_ke:GROUP@2025-M10', 'luy_ke:GROUP@2025-M11', 'luy_ke:GROUP@2025-M12', 'luy_ke:GROUP@2026-Y', 'luy_ke:GROUP@2026-H1', 'luy_ke:GROUP@2026-H2', 'luy_ke:GROUP@2026-Q1', 'luy_ke:GROUP@2026-Q2', 'luy_ke:GROUP@2026-Q3', 'luy_ke:GROUP@2026-Q4', 'luy_ke:GROUP@2026-M01', 'luy_ke:GROUP@2026-M02', 'luy_ke:GROUP@2026-M03', 'luy_ke:GROUP@2026-M04', 'luy_ke:GROUP@2026-M05', 'luy_ke:GROUP@2026-M06'), 'cb_khong_do': 0},
    'luy_ke:SGO2': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:SGO2@2025-Y', 'luy_ke:SGO2@2025-H1', 'luy_ke:SGO2@2025-H2', 'luy_ke:SGO2@2025-Q1', 'luy_ke:SGO2@2025-Q2', 'luy_ke:SGO2@2025-Q3', 'luy_ke:SGO2@2025-Q4', 'luy_ke:SGO2@2025-M01', 'luy_ke:SGO2@2025-M02', 'luy_ke:SGO2@2025-M04', 'luy_ke:SGO2@2025-M08', 'luy_ke:SGO2@2025-M09', 'luy_ke:SGO2@2025-M10', 'luy_ke:SGO2@2025-M11', 'luy_ke:SGO2@2025-M12', 'luy_ke:SGO2@2026-Y', 'luy_ke:SGO2@2026-H1', 'luy_ke:SGO2@2026-H2', 'luy_ke:SGO2@2026-Q1', 'luy_ke:SGO2@2026-Q2', 'luy_ke:SGO2@2026-Q3', 'luy_ke:SGO2@2026-Q4', 'luy_ke:SGO2@2026-M01', 'luy_ke:SGO2@2026-M02', 'luy_ke:SGO2@2026-M05'), 'cb_do': 32, 'cb_dat': 28, 'cb_dat_co_so': 0, 'cb_dat_0_0': 28, 'cb_khong_dat': ('luy_ke:SGO2@2026-Y', 'luy_ke:SGO2@2026-H2', 'luy_ke:SGO2@2026-Q3', 'luy_ke:SGO2@2026-Q4'), 'cb_khong_do': 0},
    'luy_ke:SGO1': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:SGO1@2025-Y', 'luy_ke:SGO1@2025-H1', 'luy_ke:SGO1@2025-H2', 'luy_ke:SGO1@2025-Q1', 'luy_ke:SGO1@2025-Q2', 'luy_ke:SGO1@2025-Q3', 'luy_ke:SGO1@2025-Q4', 'luy_ke:SGO1@2025-M01', 'luy_ke:SGO1@2025-M02', 'luy_ke:SGO1@2025-M03', 'luy_ke:SGO1@2025-M04', 'luy_ke:SGO1@2025-M05', 'luy_ke:SGO1@2025-M06', 'luy_ke:SGO1@2025-M07', 'luy_ke:SGO1@2025-M08', 'luy_ke:SGO1@2025-M09', 'luy_ke:SGO1@2025-M10', 'luy_ke:SGO1@2025-M11', 'luy_ke:SGO1@2025-M12', 'luy_ke:SGO1@2026-Y', 'luy_ke:SGO1@2026-H1', 'luy_ke:SGO1@2026-H2', 'luy_ke:SGO1@2026-Q1', 'luy_ke:SGO1@2026-Q2', 'luy_ke:SGO1@2026-Q3', 'luy_ke:SGO1@2026-Q4', 'luy_ke:SGO1@2026-M01', 'luy_ke:SGO1@2026-M02', 'luy_ke:SGO1@2026-M03', 'luy_ke:SGO1@2026-M04', 'luy_ke:SGO1@2026-M06'), 'cb_do': 32, 'cb_dat': 28, 'cb_dat_co_so': 0, 'cb_dat_0_0': 28, 'cb_khong_dat': ('luy_ke:SGO1@2026-Y', 'luy_ke:SGO1@2026-H2', 'luy_ke:SGO1@2026-Q3', 'luy_ke:SGO1@2026-Q4'), 'cb_khong_do': 0},
    'luy_ke:HGO2': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:HGO2@2025-Y', 'luy_ke:HGO2@2025-H2', 'luy_ke:HGO2@2025-Q3', 'luy_ke:HGO2@2025-M09', 'luy_ke:HGO2@2026-Y', 'luy_ke:HGO2@2026-H1', 'luy_ke:HGO2@2026-H2', 'luy_ke:HGO2@2026-Q2', 'luy_ke:HGO2@2026-Q3', 'luy_ke:HGO2@2026-Q4', 'luy_ke:HGO2@2026-M05'), 'cb_do': 32, 'cb_dat': 32, 'cb_dat_co_so': 0, 'cb_dat_0_0': 32, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'luy_ke:BGO2': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:BGO2@2025-Y', 'luy_ke:BGO2@2025-H2', 'luy_ke:BGO2@2025-Q3', 'luy_ke:BGO2@2025-Q4', 'luy_ke:BGO2@2025-M09', 'luy_ke:BGO2@2025-M12', 'luy_ke:BGO2@2026-Y', 'luy_ke:BGO2@2026-H1', 'luy_ke:BGO2@2026-H2', 'luy_ke:BGO2@2026-Q2', 'luy_ke:BGO2@2026-Q3', 'luy_ke:BGO2@2026-M05'), 'cb_do': 32, 'cb_dat': 32, 'cb_dat_co_so': 0, 'cb_dat_0_0': 32, 'cb_khong_dat': (), 'cb_khong_do': 0},
}
MONG_AK: dict[str, dict[str, Any]] = {
    'ngay:GROUP': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:SGO2': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:SGO1': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:HGO2': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:BGO2': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
}
#: số hàng · số ô KHÁC RỖNG theo (chế độ, khối) — đo: TRÙNG ảnh DT11 *(cùng lưới)*.
MONG_DONG: dict[str, tuple[int, int]] = _d2.MONG_DONG
CHUA_CO_DU_LIEU: tuple[str, ...] = ('hr@2026-H2', 'hr@2026-Q3', 'hr@2026-Q4')


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5)*: như `daily_report_2.thieu_lac` nhưng `mong` CỦA ẢNH NÀY. Tập rỗng ⇒ `ValueError` *(Đ3)*."""
    if not dong:
        raise ValueError("0 hàng — mẫu số 0, ⛔ nền xanh (Đ3)")
    if len(MONG_CHECK) != 10 or len(MONG_AK) != 5 or not MONG_DONG:
        raise ValueError("MONG_CHECK / MONG_DONG ⛔ khai — cổng ⛔ đo được")
    ck = _d2.do_check(dong)
    thieu: list[str] = []
    for k, m in MONG_CHECK.items():
        thieu += _d2._dr.so_voi_mong(k, _d2._tom(ck[k]), m)
    ak = _d2.do_check_khong_ngay(dong)
    for k, m in MONG_AK.items():
        thieu += _d2._dr.so_voi_mong(f"{k}@ak", _d2._tom(ak[k]), m)
    dd = _d2.dem_dong(dong)
    if dd != MONG_DONG:
        thieu += [f"{k}: {dd.get(k)}≠{MONG_DONG.get(k)}" for k in sorted(set(dd) | set(MONG_DONG)) if dd.get(k) != MONG_DONG.get(k)]
    chua = _d2.chua_co(dong)
    if chua != CHUA_CO_DU_LIEU:
        thieu.append(f"chua_co_du_lieu {chua}≠{CHUA_CO_DU_LIEU}")
    return {"thieu": thieu, "lac": [],
            "dai": (f"{len(dong)} hàng × 32 cột G…AL · CHECK ② đo được {sum(c['cb_do'] for c in ck.values())} kỳ-khối: "
                    f"đạt ② có số {sum(c['cb_dat_co_so'] for c in ck.values())} · đạt ② 0=0 "
                    f"{sum(c['cb_dat_0_0'] for c in ck.values())} · ⛔ đạt {sum(len(c['cb_khong_dat']) for c in ck.values())} · "
                    f"CHECK ① NB=0 ≠0 ở {sum(len(c['nb_khac_0']) for c in ck.values())} · kỳ 0 ô: {len(chua)}")}
