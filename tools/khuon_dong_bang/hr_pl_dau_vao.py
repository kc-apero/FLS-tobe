"""Khuôn đóng băng `hr_pl_dau_vao` — ĐẦU VÀO PLA3-HR · tab `Report I H1000 Ledge (HR Allocate HD) Y2025 | For PL Report`.

    python tools/dong_bang_sheet.py hr_pl_dau_vao <bản_thô.json> --mong 13356
        ⇒ tests/fixture/dau_vao/hr_pl_dau_vao.json

⭐ **Vì sao có khuôn này** *(ISP 3.1.2 · DT7b · `WO-281` AC-3)*: đáp án 416 =
`SUMIFS(HR!$BA, HR!$BM, <ngày>, HR!$V, <mã HD>) − SUMIFS(HR!$BB, …)`; ảnh `hr_ledger_2025` *(DT6c)* chỉ có `ky` suy
từ cột `A` của file GỐC HR, ⛔ có `BM` của tab `For PL Report` ở sổ P&L. Khuôn này đọc CHÍNH tab ấy *(sổ P&L
`19NNTb…`)* — khác nguồn `hr_ledger_2025` *(file gốc `1YEyGx…`)* — và **MỞ RỘNG** khuôn HR: GỌI `_gl_hr` *(`LE` ·
`HD_FINAL` · `_tong` — ⛔ chép)*; ảnh `hr_ledger_2024`/`2025` giữ TỪNG BYTE.

⭐ **CÔNG THỨC `BM`** *(đọc 22/11 bằng FORMULA, chỉ-đọc — `BM10` · `BM11` · `BM2000` · `BM5000`, cùng một công thức)*:
    `=if(BK10="","" ,if(and(BL10=2024,BK10=11),DATE(BL10,BK10,1),if(and(BL10=2024,BK10=12),DATE(BL10,BK10,1),DATE(2025,BK10,1))))`
⇒ cột NGUỒN = **`BK`** *(`=ArrayFormula(AH10:AH)` — THÁNG PL start, copy của cột `AH`; 13.356/13.356 là số nguyên 1…12)* và
**`BL`** *(HẰNG dán — NĂM: `2024` ×1.375 · `2025` ×11.981; ⛔ công thức)*. Quy tắc: tháng 11–12 của `BL = 2024` giữ
năm 2024; MỌI trường hợp khác ⇒ năm **2025** *(⛔ theo `BL`)*. ⛔ `BM` ⛔ phải ngày của cột `A`: `A` còn
`2.571` hàng RỖNG mà `BM` vẫn có ngày; ở `7.578/10.785` hàng có `A`, tháng `A` ≠ tháng `BM`. Cổng tái dựng `BM` từ `BK`·`BL` cho **mọi** hàng.

⭐ **KHOÁ KHỐI CDT** *(`DT7B-R1-02`, đọc 22/11 bằng FORMULA chỉ-đọc — 416 = `[MID] Report I PLA3 Daily | HR Only`)*:
  · 6 khối CDT `CVL COR SHQ1 CSM CAH ASA` ở cột `CA…SH` *(2025-01+)*: `SUMIFS(BA, BM=ngày, V=nhãn, BP=A{mở khối}) − SUMIFS(BB, …)`;
    khối `SHQ2` = `GROUP − Σ 6 khối CDT` *(dư)*. ⛔ khoá `J` — khoá là **`BP`** *("CDT Correct")*.
  · `BP10` = `=ArrayFormula(iferror(VLOOKUP(J10:J,$BR$11:$BS$28,2,FALSE),"SHQ2 | Headquarters2"))` ⇒ nguồn `J` *(hằng dán, 114 rỗng)*
    + bảng ánh xạ `BR11:BS28` *(CÙNG tab, 13 hàng chữ — hằng `BP_ANH_XA`; `BR:BS` toàn CHỮ — 14 ô `BR` gồm tiêu đề · 13 ô `BS` · 0 số)*.
  · ⚠ Ô `G…BX` *(72 cột đầu, 2024-10-20…2024-12-30)* của 416 còn là bản dán CŨ `SUMIFS(BR…) − SUMIFS(BS…)` ở tab HR — `BR:BS`
    là bảng chữ ⇒ `0`; vì vậy `SGO2/SGO1/6 CDT` = 0 ở kỳ 2411·2412 và `SHQ2 = GROUP`; `BGO2` = ΣBA *(`BS` chữ)*.

⭐ **Hợp đồng bản thô** — LƯỚI `{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values}`:
  · `cot` = `("dong_sheet","A","P","V","BK","BL","BM","BA","BB","J","BP")` *(SA, ánh xạ cột bằng hàng tiêu đề 7–8 TRƯỚC:
    `P`=LE · `V`=Budget Code Final · `BK`/`BL`/`BM`=thời điểm bắt đầu/năm/ngày PL · `BA`/`BB`=PS Nợ/Có mUSD ·
    `J`=Chủ dự toán (CDT1) · `BP`=CDT Correct)*.
    ⛔⛔ `B` Số chứng từ · `C` Diễn giải · `G`…`O` · `H` Payment Type *(số TK)* — vùng đọc ⛔ phủ.
  · `values` = mọi hàng có `V` *(13.356, `dong_sheet` 10…13365 liên tục)*; `J` rỗng ở 114 hàng; `A`/`BA`/`BB` RỖNG đồng thời ở **2.571** hàng.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from collections import Counter
from decimal import Decimal
from typing import Any

_D = pathlib.Path(__file__).resolve().parent


def _nap(ten: str):
    spec = importlib.util.spec_from_file_location(f"khuon_dong_bang_{ten}", _D / f"{ten}.py")
    m = sys.modules.get(spec.name) or importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    if not hasattr(m, "BANG"):
        spec.loader.exec_module(m)
    return m


_gl = _nap("_gl_hr")
_pl = _nap("gl_pl_dau_vao")           # GỌI `date_sheets` · `_ky`
_k406 = _pl._k406

BANG = "PD.PL.HR.DauVao"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("A", "P", "V", "BK", "BL", "BM", "BA", "BB", "J", "BP")
KIEU_COT = {"A": "so?", "P": "chu", "V": "chu", "BK": "so", "BL": "so", "BM": "so", "BA": "so?", "BB": "so?",
            "J": "chu?", "BP": "chu"}
RA = "tests/fixture/dau_vao/hr_pl_dau_vao.json"
PHU_MONG = {"tong_ky": 14}

COT_THO = ("dong_sheet", "A", "P", "V", "BK", "BL", "BM", "BA", "BB", "J", "BP")
DONG_DAU_SHEET = 10

#: Đ5 — đo 22/11 *(mỗi số đếm MỘT vật)*.
MONG_A_RONG = 2571            # hàng mà A = BA = BB = rỗng
MONG_BM_KHOP = 13356          # hàng có BM = f(BK, BL)
MONG_BL = {2024: 1375, 2025: 11981}
#: Số hàng theo KỲ PL *(`BM`, yyyymm; tổng 13.356)* — cột "mong số hàng theo kỳ" của `WO-281` AC-3.
MONG_KY_BM_THAT: dict[int, int] = {
    202411: 726, 202412: 649, 202501: 879, 202502: 902, 202503: 792, 202504: 919, 202505: 921,
    202506: 1364, 202507: 1094, 202508: 1604, 202509: 1076, 202510: 828, 202511: 795, 202512: 807}


#: ⭐ `BR11:BS28` của tab HR *(13 hàng có chữ, đọc 22/11 — mã nhóm CDT, ⛔ tên người/TK)*: khoá `J` *(so không phân biệt hoa-thường
#: như `VLOOKUP`)* → `BP`; ⛔ có trong bảng ⇒ `SHQ2 | Headquarters2`.
BP_ANH_XA: tuple[tuple[str, str], ...] = (
    ("SHQ2 | Headquarters2", "SHQ2 | Headquarters2"), ("SHQ2_Headquarters2", "SHQ2 | Headquarters2"),
    ("SHQ1_Headquarters1", "SHQ1 | Headquarters1"), ("CMN_Management", "SHQ1 | Headquarters1"),
    ("CSM_SuperMinds", "CSM | SuperMinds"), ("ASA_Super App (IOs)", "ASA | Super App"),
    ("CVL_VisionLab", "CVL | VisionLab"), ("COR_TeraSofts", "COR | TeraSofts"),
    ("CAH_Astronex", "CAH | Astronex"), ("CSM | SuperMinds", "CSM | SuperMinds"),
    ("CVL | VisionLab", "CVL | VisionLab"), ("COR | TeraSofts", "COR | TeraSofts"),
    ("CAH | Astronex", "CAH | Astronex"))
BP_MAC_DINH = "SHQ2 | Headquarters2"
#: `J` — tập đóng 14 giá trị + rỗng *(đo 22/11, 13.356 hàng)*; `BP` — 7 giá trị. Mong phân bố `BP` *(Đ5)*.
MONG_J_RONG = 114
TAP_J = frozenset({"SHQ1_Headquarters1", "CVL_VisionLab", "SHQ2_Headquarters2", "CSM_SuperMinds", "CAH_Astronex",
                   "COR_TeraSofts", "COR_Terasofts", "ASA_Super App (IOs)", "CMN_Management", "SHQ2 | Headquarters2",
                   "COR | TeraSofts", "CSM | SuperMinds", "CVL | VisionLab", "CAH | Astronex"})
MONG_BP: dict[str, int] = {
    "SHQ1 | Headquarters1": 4689, "SHQ2 | Headquarters2": 1982, "CVL | VisionLab": 1767, "COR | TeraSofts": 1664,
    "CSM | SuperMinds": 1395, "CAH | Astronex": 1209, "ASA | Super App": 650}


def tra_bp(j: Any) -> str:
    """`BP = iferror(VLOOKUP(J, BR11:BS28, 2, FALSE), "SHQ2 | Headquarters2")` — `VLOOKUP` ⛔ phân biệt hoa-thường."""
    k = "" if j is None else str(j).casefold()
    return next((v for a, v in BP_ANH_XA if a.casefold() == k), BP_MAC_DINH)


def _ky_bm(bm: int) -> int:
    return _k406._ky_tu_serial(bm)


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    if tho.get("cot") != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(⛔ phủ B·C·G…O·H)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng dữ liệu ⛔ rỗng")
    dong: list[list[Any]] = []
    tky: dict[int, list[Any]] = {}
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô")
        if h[0] != DONG_DAU_SHEET + i:
            raise ValueError(f"hàng {i + 1}: dong_sheet {h[0]} ⛔ liên tục *(mong {DONG_DAU_SHEET + i})*")
        row = [h[0]] + [None if _pl._rong(x) else x for x in h[1:]]
        for j, nm in ((4, "BK"), (5, "BL"), (6, "BM")):
            if not isinstance(row[j], int) or isinstance(row[j], bool):
                raise ValueError(f"hàng {i + 1}: cột {nm} phải số nguyên")
        dong.append(row)
        t = tky.setdefault(_ky_bm(row[6]), [0, 0, Decimal(0), Decimal(0)])
        t[0] += 1
        t[1] += row[1] is not None
        for j, v in ((2, row[7]), (3, row[8])):
            if v is not None:
                t[j] += Decimal(str(v))
    phu = [{"ky_bm": k, "so_hang": v[0], "so_hang_co_A": v[1], "tong_BA": _gl._tong([v[2]]),
            "tong_BB": _gl._tong([v[3]])} for k, v in sorted(tky.items())]
    return {
        "cot": [KHOA, *COT], "dong": dong, "phu": {"tong_ky": phu},
        "ghi_chu": (
            f"ĐẦU VÀO PLA3-HR = {len(dong)} hàng tab `…Y2025 | For PL Report` sổ P&L, khoá dong_sheet "
            f"{DONG_DAU_SHEET}…{DONG_DAU_SHEET + len(dong) - 1} liên tục; 10 cột A·P·V·BK·BL·BM·BA·BB·J·BP "
            f"*(⛔ B Số chứng từ · C Diễn giải · H Payment Type · G…O)*. `BM` = "
            f"`=if(BK=\"\",\"\",if(and(BL=2024,BK=11),DATE(BL,BK,1),if(and(BL=2024,BK=12),DATE(BL,BK,1),DATE(2025,BK,1))))` "
            f"⇒ cột NGUỒN `BK` *(= ArrayFormula(AH10:AH), tháng)* + `BL` *(hằng năm)*; cổng tái dựng BM ở `thieu_lac`. "
            f"A/BA/BB rỗng đồng thời ở {sum(1 for r in dong if r[1] is None)} hàng. Bảng phụ `tong_ky` = số hàng "
            f"(+ số hàng có A) + ΣBA/ΣBB theo kỳ BM."),
    }


def _chu(v: Any) -> Any:
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _i(v: Any) -> int:
    return int(_chu(v))


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5; ⛔ in giá trị ô)*: ⒜ `P`/`V` ngoài tập đóng; ⒝ **`BM` ≠ f(`BK`,`BL`)** ở hàng nào / số khớp ≠ 13.356;
    ⒞ `A`·`BA`·`BB` ⛔ rỗng-cùng-lúc, số hàng rỗng ≠ 2.571; ⒟ phân bố `BL` ≠ mong; ⒠ số hàng mỗi kỳ BM ≠ mong; ⒡ **`J` ngoài tập đóng · `BP` ≠ `tra(J)` · phân bố `BP` ≠ mong**."""
    thieu: list[str] = []
    n_khop = n_rong = n_bp = 0
    j_rong = 0
    bp_dem: Counter = Counter()
    bl: Counter = Counter()
    ky: Counter = Counter()
    for d in dong:
        ds = _i(d["dong_sheet"])
        if _chu(d["P"]) not in _gl.LE:
            thieu.append(f"P_la@{ds}")
        if _chu(d["V"]) not in _gl.HD_FINAL:
            thieu.append(f"V_la@{ds}")
        j, bp = _chu(d["J"]), _chu(d["BP"])
        j_rong += j is None
        if j is not None and j not in TAP_J:
            thieu.append(f"J_la@{ds}")
        if bp not in MONG_BP:
            thieu.append(f"BP_la@{ds}")
        if bp == tra_bp(j):
            n_bp += 1
        else:
            thieu.append(f"BP_khac_tra_J@{ds}")
        bp_dem[bp] += 1
        bk, b_l, bm = _i(d["BK"]), _i(d["BL"]), _i(d["BM"])
        bl[b_l] += 1
        nam = b_l if (b_l == 2024 and bk in (11, 12)) else 2025
        if bm == _pl.date_sheets(nam, bk, 1):
            n_khop += 1
        else:
            thieu.append(f"BM_khac_f@{ds}")
        ky[_ky_bm(bm)] += 1
        trong = tuple(d[c] is None for c in ("A", "BA", "BB"))
        if len(set(trong)) != 1:
            thieu.append(f"A_BA_BB_lech@{ds}")
        elif trong[0]:
            n_rong += 1
    if n_khop != MONG_BM_KHOP:
        thieu.append(f"BM_khop@khác:{n_khop}/{MONG_BM_KHOP}")
    if n_rong != MONG_A_RONG:
        thieu.append(f"A_rong@khác:{n_rong}/{MONG_A_RONG}")
    if n_bp != MONG_BM_KHOP:
        thieu.append(f"BP_khop@khác:{n_bp}/{MONG_BM_KHOP}")
    if j_rong != MONG_J_RONG:
        thieu.append(f"J_rong@khác:{j_rong}/{MONG_J_RONG}")
    if dict(bp_dem) != MONG_BP:
        thieu.append("BP@phân_bố_khác")
    if dict(bl) != MONG_BL:
        thieu.append("BL@phân_bố_khác")
    if dict(ky) != MONG_KY_BM_THAT:
        thieu.append("ky_BM@phân_bố_khác")
    dai = (f"{len(dong)} hàng · BM=f(BK,BL) khớp {n_khop} · A/BA/BB rỗng {n_rong} · BL {dict(sorted(bl.items()))} · "
           f"{len(ky)} kỳ BM · BP=tra(J) khớp {n_bp} · J rỗng {j_rong}")
    return {"thieu": thieu, "lac": [], "dai": dai}

