"""Khuôn đóng băng `daily_report_2` — ĐÁP ÁN Daily Report 2 = tab `5. Daily Report 2` của sổ `[COPY] Report I General
Ledger | CF report` *(PD 610 · ISP 3.1.2 · Step 41 · DT11 · `WO-269` AC-1…AC-5)*.

    python tools/dong_bang_sheet.py daily_report_2 <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dap_an/daily_report_2.json

Nguồn: lưới `A1:AR1114` đọc về **958 hàng × 38 cột** *(API cắt hàng cuối rỗng)*. Ba chế độ, theo cột `A`:
  · `ngay`  — hàng `11…425`: **5 khối** `GROUP · SGO2 · SGO1 · HGO2 · BGO2` *(mỗi khối 82 hàng HDO·HDH·HDAP·HDT·HDC·HDCI)*;
    cột `G…AJ` = **30 ngày 01→30/11/2026** *(hàng 9: serial 46327…46356; `From`=46327 · `To`=46356)*; cột `AK` = cột
    thứ 31 **không có ngày** *(nhãn `Sat`, vẫn có 844 ô số)*; cột `F` *(= 46326, 31/10/2026, "Month 10")* **0** ô dữ liệu.
  · `luy_ke` — từ `CM Cumulative` *(hàng 426)*: 5 khối như trên; cột `G…AL` = **32 kỳ**: `2025` Y·H1·H2·Q1…Q4·M1…M12
    *(19 cột `G…Y`)* + `2026` Y·H1·H2·Q1…Q4·M1…M6 *(13 cột `Z…AL`; ⛔ có M7…M12)*.
  · `hr` — từ `Report HR` *(hàng 843)*: số người *(đơn vị person)*, cùng 32 cột kỳ; ⛔ thuộc hai phép CHECK.
Ảnh khoá theo **hàng sheet**; cột `g…al` = đúng chữ cột Sheets `G…AL` *(nghĩa của cột = bảng phụ `tieu_de`, Đ4)*;
`che_do` · `khoi` · `ma` *(= mã trước `|` ở nhãn B:E)* là cột suy ra.

Hợp đồng bản thô *(phiên cloud DATA, khoá SA chỉ-đọc, ⛔ commit)*: `{nguon, doc_luc, cach_doc, values}` — `values` =
lưới `A1:AR1114` như đọc.

Đối chiếu bản A-CCR `5. Daily Report 2` *(cùng 1114×44, sổ `A-CCR_V2_Working`; AP D5)*: ⛔ đóng băng thành ảnh thứ ba;
số ô khớp/lệch khai ở BG-270.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

from fls.canon.o_loi import la_o_loi  # noqa: E402  (DT8: ô lỗi = tập ĐÓNG, 1 bản khai)

_P = pathlib.Path(__file__).resolve().parent / "_daily_report.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__daily_report", _P)
_dr = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _dr
    _spec.loader.exec_module(_dr)

BANG = "DAP_AN.DAILY_REPORT_2"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
RA = "tests/fixture/dap_an/daily_report_2.json"

KHOI = ("GROUP", "SGO2", "SGO1", "HGO2", "BGO2")
CHE_DO = ("ngay", "luy_ke", "hr")
COT_GT = tuple(c.lower() for c in ("G H I J K L M N O P Q R S T U V W X Y Z AA AB AC AD AE AF AG AH AI AJ AK AL".split()))
COT_NHAN = ("che_do", "khoi", "ma", "nhan_b", "nhan_c", "nhan_d", "nhan_e")
COT = (*COT_NHAN, *COT_GT)
KIEU_COT = {"che_do": "chu", **{c: "chu?" for c in COT_NHAN[1:]}, **{c: "so!" for c in COT_GT}}
LOI_MONG = {c: 0 for c in COT_GT}                  # đo 20/11: 0 ô lỗi Sheets ở cả 32 cột — khai 0 RÕ RÀNG
PHU_MONG = {"tieu_de": 356, "dong_chi_nhan": 84}
TOL = Decimal("1e-9")                              # mUSD: dưới 1e-9 là nhiễu dấu phẩy động, ⛔ lệch

#: nhãn kỳ của cột theo chế độ *(Đ4: ngày ⇒ ISO; luỹ kế ⇒ `<năm>-<Y|H1|…|M01…>`)*
_NGAY0 = 46327
#: ⭐ `DT11-R1-04`: **30** ngày THẬT *(hàng 9: serial 46327…46356 = `From`…`To`)*. Cột `AK` ⛔ phải ngày — `AK5` rỗng, hàng 6
#: `=text(AK5,"ddd")` ⇒ `"Sat"` *(serial 0)*, `SUMIFS` chạy tiêu chí rỗng ⇒ **vết kéo công thức** quá `To` = 30/11. Bản đầu gộp nó
#: vào trục ngày ("31/31 cột", 155 ngày-khối = 150 + 5 `AK`) ⇒ nay tách: trục ngày 30, trục `khong_ngay` *(cột `ak`)* RIÊNG.
KY_NGAY = tuple((str(date(1899, 12, 30) + timedelta(days=_NGAY0 + i)), COT_GT[i]) for i in range(30))
COT_KHONG_NGAY = ("ak",)
NHAN_KHONG_NGAY = "khong_ngay"
_LK = [("2025", k) for k in ("Y", "H1", "H2", "Q1", "Q2", "Q3", "Q4", *[f"M{m:02d}" for m in range(1, 13)])] \
    + [("2026", k) for k in ("Y", "H1", "H2", "Q1", "Q2", "Q3", "Q4", *[f"M{m:02d}" for m in range(1, 7)])]
KY_LUY_KE = tuple((f"{n}-{k}", COT_GT[i]) for i, (n, k) in enumerate(_LK))
assert len(KY_NGAY) == 30 and len(KY_LUY_KE) == 32 and not set(COT_KHONG_NGAY) & {c for _, c in KY_NGAY}

#: ⭐ Đ5 — theo khối, đo lần đầu 20/11 rồi khai. Khác ⇒ ĐỎ cả hai chiều.
MONG_CHECK: dict[str, dict[str, Any]] = {
    'ngay:GROUP': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': ('ngay:GROUP@2026-11-04', 'ngay:GROUP@2026-11-05', 'ngay:GROUP@2026-11-09', 'ngay:GROUP@2026-11-10', 'ngay:GROUP@2026-11-11'), 'cb_do': 30, 'cb_dat': 24, 'cb_dat_co_so': 0, 'cb_dat_0_0': 24, 'cb_khong_dat': ('ngay:GROUP@2026-11-02', 'ngay:GROUP@2026-11-03', 'ngay:GROUP@2026-11-05', 'ngay:GROUP@2026-11-09', 'ngay:GROUP@2026-11-10', 'ngay:GROUP@2026-11-11'), 'cb_khong_do': 0},
    'ngay:SGO2': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': ('ngay:SGO2@2026-11-10',), 'cb_do': 30, 'cb_dat': 29, 'cb_dat_co_so': 0, 'cb_dat_0_0': 29, 'cb_khong_dat': ('ngay:SGO2@2026-11-10',), 'cb_khong_do': 0},
    'ngay:SGO1': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': ('ngay:SGO1@2026-11-04', 'ngay:SGO1@2026-11-10'), 'cb_do': 30, 'cb_dat': 29, 'cb_dat_co_so': 0, 'cb_dat_0_0': 29, 'cb_khong_dat': ('ngay:SGO1@2026-11-09',), 'cb_khong_do': 0},
    'ngay:HGO2': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 30, 'cb_dat': 30, 'cb_dat_co_so': 0, 'cb_dat_0_0': 30, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:BGO2': {'nb_do': 30, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 30, 'cb_dat': 30, 'cb_dat_co_so': 0, 'cb_dat_0_0': 30, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'luy_ke:GROUP': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:GROUP@2025-Y', 'luy_ke:GROUP@2025-H1', 'luy_ke:GROUP@2025-H2', 'luy_ke:GROUP@2025-Q1', 'luy_ke:GROUP@2025-Q2', 'luy_ke:GROUP@2025-Q3', 'luy_ke:GROUP@2025-Q4', 'luy_ke:GROUP@2025-M01', 'luy_ke:GROUP@2025-M02', 'luy_ke:GROUP@2025-M03', 'luy_ke:GROUP@2025-M04', 'luy_ke:GROUP@2025-M05', 'luy_ke:GROUP@2025-M06', 'luy_ke:GROUP@2025-M07', 'luy_ke:GROUP@2025-M08', 'luy_ke:GROUP@2025-M09', 'luy_ke:GROUP@2025-M10', 'luy_ke:GROUP@2025-M11', 'luy_ke:GROUP@2025-M12', 'luy_ke:GROUP@2026-Y', 'luy_ke:GROUP@2026-H1', 'luy_ke:GROUP@2026-H2', 'luy_ke:GROUP@2026-Q1', 'luy_ke:GROUP@2026-Q2', 'luy_ke:GROUP@2026-Q3', 'luy_ke:GROUP@2026-Q4', 'luy_ke:GROUP@2026-M01', 'luy_ke:GROUP@2026-M02', 'luy_ke:GROUP@2026-M03', 'luy_ke:GROUP@2026-M04', 'luy_ke:GROUP@2026-M05', 'luy_ke:GROUP@2026-M06'), 'cb_do': 32, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': ('luy_ke:GROUP@2025-Y', 'luy_ke:GROUP@2025-H1', 'luy_ke:GROUP@2025-H2', 'luy_ke:GROUP@2025-Q1', 'luy_ke:GROUP@2025-Q2', 'luy_ke:GROUP@2025-Q3', 'luy_ke:GROUP@2025-Q4', 'luy_ke:GROUP@2025-M01', 'luy_ke:GROUP@2025-M02', 'luy_ke:GROUP@2025-M03', 'luy_ke:GROUP@2025-M04', 'luy_ke:GROUP@2025-M05', 'luy_ke:GROUP@2025-M06', 'luy_ke:GROUP@2025-M07', 'luy_ke:GROUP@2025-M08', 'luy_ke:GROUP@2025-M09', 'luy_ke:GROUP@2025-M10', 'luy_ke:GROUP@2025-M11', 'luy_ke:GROUP@2025-M12', 'luy_ke:GROUP@2026-Y', 'luy_ke:GROUP@2026-H1', 'luy_ke:GROUP@2026-H2', 'luy_ke:GROUP@2026-Q1', 'luy_ke:GROUP@2026-Q2', 'luy_ke:GROUP@2026-Q3', 'luy_ke:GROUP@2026-Q4', 'luy_ke:GROUP@2026-M01', 'luy_ke:GROUP@2026-M02', 'luy_ke:GROUP@2026-M03', 'luy_ke:GROUP@2026-M04', 'luy_ke:GROUP@2026-M05', 'luy_ke:GROUP@2026-M06'), 'cb_khong_do': 0},
    'luy_ke:SGO2': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:SGO2@2025-Y', 'luy_ke:SGO2@2025-H1', 'luy_ke:SGO2@2025-H2', 'luy_ke:SGO2@2025-Q1', 'luy_ke:SGO2@2025-Q2', 'luy_ke:SGO2@2025-Q3', 'luy_ke:SGO2@2025-Q4', 'luy_ke:SGO2@2025-M01', 'luy_ke:SGO2@2025-M02', 'luy_ke:SGO2@2025-M04', 'luy_ke:SGO2@2025-M08', 'luy_ke:SGO2@2025-M09', 'luy_ke:SGO2@2025-M10', 'luy_ke:SGO2@2025-M11', 'luy_ke:SGO2@2025-M12', 'luy_ke:SGO2@2026-Y', 'luy_ke:SGO2@2026-H1', 'luy_ke:SGO2@2026-H2', 'luy_ke:SGO2@2026-Q1', 'luy_ke:SGO2@2026-Q2', 'luy_ke:SGO2@2026-Q3', 'luy_ke:SGO2@2026-Q4', 'luy_ke:SGO2@2026-M01', 'luy_ke:SGO2@2026-M02', 'luy_ke:SGO2@2026-M05'), 'cb_do': 32, 'cb_dat': 28, 'cb_dat_co_so': 0, 'cb_dat_0_0': 28, 'cb_khong_dat': ('luy_ke:SGO2@2026-Y', 'luy_ke:SGO2@2026-H2', 'luy_ke:SGO2@2026-Q3', 'luy_ke:SGO2@2026-Q4'), 'cb_khong_do': 0},
    'luy_ke:SGO1': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:SGO1@2025-Y', 'luy_ke:SGO1@2025-H1', 'luy_ke:SGO1@2025-H2', 'luy_ke:SGO1@2025-Q1', 'luy_ke:SGO1@2025-Q2', 'luy_ke:SGO1@2025-Q3', 'luy_ke:SGO1@2025-Q4', 'luy_ke:SGO1@2025-M01', 'luy_ke:SGO1@2025-M02', 'luy_ke:SGO1@2025-M03', 'luy_ke:SGO1@2025-M04', 'luy_ke:SGO1@2025-M05', 'luy_ke:SGO1@2025-M06', 'luy_ke:SGO1@2025-M07', 'luy_ke:SGO1@2025-M08', 'luy_ke:SGO1@2025-M09', 'luy_ke:SGO1@2025-M10', 'luy_ke:SGO1@2025-M11', 'luy_ke:SGO1@2025-M12', 'luy_ke:SGO1@2026-Y', 'luy_ke:SGO1@2026-H1', 'luy_ke:SGO1@2026-H2', 'luy_ke:SGO1@2026-Q1', 'luy_ke:SGO1@2026-Q2', 'luy_ke:SGO1@2026-Q3', 'luy_ke:SGO1@2026-Q4', 'luy_ke:SGO1@2026-M01', 'luy_ke:SGO1@2026-M02', 'luy_ke:SGO1@2026-M03', 'luy_ke:SGO1@2026-M04', 'luy_ke:SGO1@2026-M06'), 'cb_do': 32, 'cb_dat': 28, 'cb_dat_co_so': 0, 'cb_dat_0_0': 28, 'cb_khong_dat': ('luy_ke:SGO1@2026-Y', 'luy_ke:SGO1@2026-H2', 'luy_ke:SGO1@2026-Q3', 'luy_ke:SGO1@2026-Q4'), 'cb_khong_do': 0},
    'luy_ke:HGO2': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:HGO2@2025-Y', 'luy_ke:HGO2@2025-H2', 'luy_ke:HGO2@2025-Q3', 'luy_ke:HGO2@2025-M09', 'luy_ke:HGO2@2026-Y', 'luy_ke:HGO2@2026-H1', 'luy_ke:HGO2@2026-H2', 'luy_ke:HGO2@2026-Q2', 'luy_ke:HGO2@2026-Q3', 'luy_ke:HGO2@2026-Q4', 'luy_ke:HGO2@2026-M05'), 'cb_do': 32, 'cb_dat': 32, 'cb_dat_co_so': 0, 'cb_dat_0_0': 32, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'luy_ke:BGO2': {'nb_do': 32, 'nb_trong': 0, 'nb_khac_0': ('luy_ke:BGO2@2025-Y', 'luy_ke:BGO2@2025-H2', 'luy_ke:BGO2@2025-Q3', 'luy_ke:BGO2@2025-Q4', 'luy_ke:BGO2@2025-M09', 'luy_ke:BGO2@2025-M12', 'luy_ke:BGO2@2026-Y', 'luy_ke:BGO2@2026-H1', 'luy_ke:BGO2@2026-H2', 'luy_ke:BGO2@2026-Q2', 'luy_ke:BGO2@2026-Q3', 'luy_ke:BGO2@2026-M05'), 'cb_do': 32, 'cb_dat': 32, 'cb_dat_co_so': 0, 'cb_dat_0_0': 32, 'cb_khong_dat': (), 'cb_khong_do': 0},
}
#: ⭐ `DT11-R1-04` — CHECK trên cột `AK` *(⛔ ngày; vết kéo công thức)*, khai RIÊNG khỏi `MONG_CHECK`.
MONG_AK: dict[str, dict[str, Any]] = {
    'ngay:GROUP': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:SGO2': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:SGO1': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:HGO2': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
    'ngay:BGO2': {'nb_do': 1, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 1, 'cb_dat': 1, 'cb_dat_co_so': 0, 'cb_dat_0_0': 1, 'cb_khong_dat': (), 'cb_khong_do': 0},
}
#: ⭐ số hàng · số ô KHÁC RỖNG theo (chế độ, khối).
MONG_DONG: dict[str, tuple[int, int]] = {
    'ngay:GROUP': (75, 2325),
    'ngay:SGO2': (80, 2480),
    'ngay:SGO1': (80, 2480),
    'ngay:HGO2': (80, 2480),
    'ngay:BGO2': (80, 2480),
    'luy_ke:GROUP': (68, 2176),
    'luy_ke:SGO2': (68, 2176),
    'luy_ke:SGO1': (68, 2176),
    'luy_ke:HGO2': (68, 2176),
    'luy_ke:BGO2': (68, 2176),
    'hr:GROUP': (111, 3147),
}
#: ⭐ AC-4 — kỳ (chế độ, nhãn) có 0 ô ⇒ `chua_co_du_lieu` có tên.
CHUA_CO_DU_LIEU: tuple[str, ...] = ('hr@2026-H2', 'hr@2026-Q3', 'hr@2026-Q4')


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _cs(n: int) -> str:
    s, n = "", n + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _kiem_tieu_de(V: list[list[Any]]) -> list[int]:
    """Hàng tiêu đề đúng khai báo ở docstring ⇒ trả danh sách hàng sheet là *hàng tiêu đề kỳ*."""
    if V[1][2] != _NGAY0 or V[2][2] != _NGAY0 + 29:
        raise ValueError("`From`/`To` (C2·C3) ⛔ 46327…46356")
    ngay = [_NGAY0 + i for i in range(30)]
    for r in (4, 8):                                # hàng 5 · hàng 9
        if [V[r][6 + i] for i in range(30)] != ngay:
            raise ValueError(f"hàng {r + 1}: G…AJ ⛔ 30 ngày 46327…46356")
    if V[4][5] != _NGAY0 - 1:
        raise ValueError("F5 ⛔ 46326")
    mong = ["2025", "H1", "H2", "Q1", "Q2", "Q3", "Q4", *[str(m) for m in range(1, 13)],
            "2026", "H1", "H2", "Q1", "Q2", "Q3", "Q4", *[str(m) for m in range(1, 7)]]
    hs = [i for i, h in enumerate(V) if str(h[0]).strip() in ("GROUP", "SGO2", "SGO1", "HGO2", "BGO2")
          and [str(x).strip() for x in h[6:38]] == mong]
    return hs


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    V = tho.get("values")
    if not isinstance(V, list) or len(V) != 958 or any(not isinstance(h, list) for h in V):
        raise ValueError("`values` phải 958 hàng *(A1:AR1114, API cắt hàng cuối rỗng)*")
    V = [list(h) + [""] * (38 - len(h)) for h in V]
    if any(len(h) != 38 for h in V):
        raise ValueError("`values` rộng quá 38 cột")
    hs = _kiem_tieu_de(V)
    if [V[i][0] for i in hs] != [*KHOI, "GROUP"]:    # 5 khối luỹ kế + 1 khối hr, tiêu đề kỳ y hệt
        raise ValueError(f"hàng tiêu đề kỳ luỹ kế/hr ⛔ đúng 6 *(5 khối + GROUP của hr)*: {len(hs)} hàng")
    che_do, khoi = "ngay", ""
    dong, chi_nhan, tieu_de = [], [], []
    n_trong = 0
    for i, h in enumerate(V):
        ds = i + 1
        a = str(h[0]).strip()
        gt = h[6:38]
        co_chu = any(isinstance(x, str) and x.strip() and not la_o_loi(x) and x.strip() != "-" for x in gt)
        co_bool = any(isinstance(x, bool) for x in gt)
        n_gt = sum(1 for x in gt if not _rong(x))
        if ds <= 10 or co_chu or co_bool or (a == "." and 0 < n_gt <= 2):
            for j in range(5, 38):
                if not _rong(h[j]):
                    tieu_de.append({"dong_sheet": ds, "cot": _cs(j), "gia_tri": h[j]})
            if ds > 10:                              # hàng tiêu đề của khối: đặt chế độ/khối
                if a in KHOI:
                    khoi = a
            continue
        if a.startswith("CM Cumulative"):
            che_do, khoi = "luy_ke", ""
        elif a.startswith("Report HR"):
            che_do, khoi = "hr", ""
        elif a in KHOI:
            khoi = a
        if not _rong(h[5]):
            raise ValueError(f"hàng {ds}: cột F ⛔ rỗng ở vùng dữ liệu")
        lab = [None if _rong(h[j]) else str(h[j]) for j in range(1, 5)]
        ma = next((x.split("|")[0].strip() for x in lab if x), None)
        cells = []
        for j, x in enumerate(gt):
            if _rong(x):
                x = None
            elif isinstance(x, str):
                x = None if x.strip() == "-" else x          # '#…' ghi nguyên
            cells.append(x)
        if all(x is None for x in cells):
            if a not in ("", ".") or any(lab):
                chi_nhan.append({"dong_sheet": ds, "che_do": che_do, "khoi": khoi or None,
                                 "nhan": " > ".join(x for x in [a if a not in ("", ".") else None, *lab] if x)})
            else:
                n_trong += 1
            continue
        dong.append([ds, che_do, khoi or None, ma, *lab, *cells])
    if not dong:
        raise ValueError("0 hàng dữ liệu — mẫu số 0 (Đ3)")
    return {
        "cot": ["dong_sheet", *COT],
        "dong": dong,
        "phu": {"tieu_de": tieu_de, "dong_chi_nhan": chi_nhan},
        "ghi_chu": (
            f"Daily Report 2 (PD 610) = {len(dong)} hàng sheet có giá trị × 32 cột G…AL ở 3 chế độ: `ngay` (5 khối × "
            "30 ngày 01→30/11/2026 + cột AK không ngày; cột F=31/10/2026 0 ô) · `luy_ke` (5 khối × 32 kỳ "
            "2025 Y·H·Q·M1…12 + 2026 Y·H·Q·M1…6) · `hr` (số người). Tiêu đề kỳ nguyên văn ở `tieu_de`; "
            f"{len(chi_nhan)} hàng chỉ có nhãn ở `dong_chi_nhan`; {n_trong} hàng rỗng hẳn ⛔ mang. Hai CHECK IX.PL "
            "khai ở MONG_CHECK. Đối chiếu A-CCR (D5): xem BG-270."),
    }


def _hang(dong: list[dict[str, Any]], che_do: str, khoi: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for d in dong:
        if d["che_do"]["chu"] == che_do and isinstance(d["khoi"], dict) and d["khoi"]["chu"] == khoi:
            m = d["ma"]["chu"] if isinstance(d["ma"], dict) else None
            if m in _dr.MA_CAN:
                if m in out:
                    raise ValueError(f"({che_do},{khoi}): mã `{m}` ở ≥ 2 hàng — ⛔ đo được CHECK")
                out[m] = d
    return out


def do_check_khong_ngay(dong: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """CHECK trên cột `AK` *(⛔ ngày — vết kéo công thức)*, 5 khối `ngay`: RIÊNG, ⛔ cộng vào đếm ngày."""
    return {f"ngay:{k}": _dr.kiem_check(_hang(dong, "ngay", k), [(f"ngay:{k}@{NHAN_KHONG_NGAY}", "ak")], TOL)
            for k in KHOI}


def do_check(dong: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """CHECK theo (chế độ ∈ ngay·luy_ke) × khối — 10 khối. Trục `ngay` = **30 ngày thật** *(⛔ `AK`)*."""
    out = {}
    for cd, ky in (("ngay", KY_NGAY), ("luy_ke", KY_LUY_KE)):
        for k in KHOI:
            out[f"{cd}:{k}"] = _dr.kiem_check(_hang(dong, cd, k), [(f"{cd}:{k}@{n}", c) for n, c in ky], TOL)
    return out


def _tom(r: dict[str, Any]) -> dict[str, Any]:
    return {"nb_do": r["nb_do"], "nb_trong": r["nb_trong"], "nb_khac_0": tuple(r["nb_khac_0"]),
            "cb_do": r["cb_do"], "cb_dat": r["cb_dat"], "cb_dat_co_so": r["cb_dat_co_so"],
            "cb_dat_0_0": r["cb_dat_0_0"], "cb_khong_dat": tuple(r["cb_khong_dat"]),
            "cb_khong_do": r["cb_khong_do"]}


def dem_dong(dong: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int]] = {}
    for d in dong:
        k = f"{d['che_do']['chu']}:{d['khoi']['chu'] if isinstance(d['khoi'], dict) else '-'}"
        n, o = out.get(k, (0, 0))
        out[k] = (n + 1, o + sum(1 for c in COT_GT if d[c] is not None))
    return out


def chua_co(dong: list[dict[str, Any]]) -> tuple[str, ...]:
    ra = []
    for cd, ky in (("ngay", KY_NGAY), ("luy_ke", KY_LUY_KE), ("hr", KY_LUY_KE)):
        rows = [d for d in dong if d["che_do"]["chu"] == cd]
        ra += [f"{cd}@{n}" for n, c in ky if rows and all(d[c] is None for d in rows)]
    return tuple(ra)


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5)*: CHECK theo khối ↔ `MONG_CHECK` · hàng/ô theo (chế độ, khối) ↔ `MONG_DONG` · kỳ 0 ô ↔
    `CHUA_CO_DU_LIEU`. Tập rỗng ⇒ `ValueError` *(Đ3)*; mong ⛔ khai ⇒ ĐỎ."""
    if not dong:
        raise ValueError("0 hàng — mẫu số 0, ⛔ nền xanh (Đ3)")
    if len(MONG_CHECK) != 10 or len(MONG_AK) != 5 or not MONG_DONG:
        raise ValueError("MONG_CHECK / MONG_DONG ⛔ khai — cổng ⛔ đo được")
    ck = do_check(dong)
    thieu: list[str] = []
    for k, m in MONG_CHECK.items():
        thieu += _dr.so_voi_mong(k, _tom(ck[k]), m)
    ak = do_check_khong_ngay(dong)
    for k, m in MONG_AK.items():
        thieu += _dr.so_voi_mong(f"{k}@ak", _tom(ak[k]), m)
    dd = dem_dong(dong)
    if dd != MONG_DONG:
        thieu += [f"{k}: {dd.get(k)}≠{MONG_DONG.get(k)}" for k in sorted(set(dd) | set(MONG_DONG)) if dd.get(k) != MONG_DONG.get(k)]
    chua = chua_co(dong)
    if chua != CHUA_CO_DU_LIEU:
        thieu.append(f"chua_co_du_lieu {chua}≠{CHUA_CO_DU_LIEU}")
    return {"thieu": thieu, "lac": [],
            "dai": (f"{len(dong)} hàng × 32 cột G…AL · ngày 2026-11-01…2026-11-30 (30 ngày thật; AK = khong_ngay, tách) · "
                    f"luỹ kế 2025 Y…M12 + 2026 Y…M6 · CHECK ② đo được {sum(c['cb_do'] for c in ck.values())} kỳ-khối "
                    f"(150 ngày-khối + 160 luỹ kế): đạt ② có số {sum(c['cb_dat_co_so'] for c in ck.values())} · "
                    f"đạt ② 0=0 {sum(c['cb_dat_0_0'] for c in ck.values())} · ⛔ đạt {sum(len(c['cb_khong_dat']) for c in ck.values())} · "
                    f"CHECK ① NB=0 đo được {sum(c['nb_do'] for c in ck.values())} kỳ-khối, ≠0 ở "
                    f"{sum(len(c['nb_khac_0']) for c in ck.values())} · AK(khong_ngay) ② đo được "
                    f"{sum(c['cb_do'] for c in ak.values())} · kỳ 0 ô: {len(chua)}")}
