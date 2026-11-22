"""Khuôn đóng băng `daily_report_3` — ĐÁP ÁN Daily Report 3 = bản `[MID][FS1][PLA5]5. Daily Report 3 (Sign off)`
*(PD 605 · ISP 3.1.2 · Step 41 · DT11 · `WO-269` AC-1…AC-5)*.

    python tools/dong_bang_sheet.py daily_report_3 <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dap_an/daily_report_3.json

Nguồn *(`[COPY] Report I General Ledger | P&L Report`)*: tab Sign off **137 × 203** = **0 ô công thức**
*(dán giá trị)*. Hàng `1` = nhóm thực thể · `2` = `Y24`/`Y25` · `3` = tiêu đề cột *(`E` `HDCode` · `F` `HDNameEN` ·
`G` Logic phân bổ · `H` `Y24` · `I` `Y25` · `K…GU` = kỳ `yyyymm`)*. **8 thực thể × 24 kỳ = 192 cột kỳ**
*(Group · VisionLab · TeraSofts · SuperMinds · Astronex · IOs · Headquarters · CHECKING; `202401…202512`;
cột `FW` là khe trống giữa khối Headquarters và CHECKING)* + 2 cột năm `H` `I`. Ảnh khoá theo **hàng sheet**
`5…137` *(mỗi hàng = một dòng PL, nhãn `ma` = `HDCode`)*; cột kỳ đặt tên `<thực thể>_<yyyymm>` *(Đ4)*.

Hợp đồng bản thô *(phiên cloud DATA, khoá SA chỉ-đọc, ⛔ commit)*: `{nguon, doc_luc, cach_doc, values,
o_chinh_tay}` — `values` = lưới `A1:GU137` · `o_chinh_tay` = ô chỉnh tay đọc ở tab ATL *(AC-3)*.

Ba lưu ý đo:
  · **Ô chữ-số**: 2 ô cột kỳ là CHỮ dạng `1.234.567.890` *(dấu chấm nghìn)* ⇒ ⛔ ép số; để RỖNG ở bảng chính và
    liệt kê nguyên chuỗi ở bảng phụ `o_chu_so`.
  · **Ô ngoài vùng**: 1 ô số lạc ở hàng `4` *(`AB4`)* ⇒ bảng phụ `o_ngoai_vung`.
  · **Ô chỉnh tay (AC-3)**: ATL `AH12` = `='Report I PLA3 Y H Q M | PM + HR'!AH12-0.5` ⇒ bảng phụ `o_chinh_tay`
    có tên; ⛔ chép vào config.
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import sys
from decimal import Decimal
from typing import Any

from fls.canon.o_loi import la_o_loi  # noqa: E402  (DT8: ô lỗi = tập ĐÓNG, 1 bản khai)

_P = pathlib.Path(__file__).resolve().parent / "_daily_report.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__daily_report", _P)
_dr = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _dr
    _spec.loader.exec_module(_dr)

BANG = "DAP_AN.DAILY_REPORT_3"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
RA = "tests/fixture/dap_an/daily_report_3.json"

ENT = ("Group", "VisionLab", "TeraSofts", "SuperMinds", "Astronex", "IOs", "Headquarters", "CHECKING")
ENT_COT = tuple(e.lower() for e in ENT)
KY = tuple(f"{y}{m:02d}" for y in (2024, 2025) for m in range(1, 13))        # 24 kỳ
COT_KY = tuple(f"{e}_{k}" for e in ENT_COT for k in KY)                       # 192
COT_NAM = ("y24", "y25")
COT_NHAN = ("ma", "ten", "logic", "nguon_j")
COT = (*COT_NHAN, "cap", *COT_NAM, *COT_KY)
KIEU_COT = {**{c: "chu?" for c in COT_NHAN}, "cap": "so",
            **{c: "so!" for c in (*COT_NAM, *COT_KY)}}
LOI_MONG = {c: 0 for c in (*COT_NAM, *COT_KY)}     # đo 20/11: 0 ô lỗi Sheets ở cả 194 cột — khai 0 RÕ RÀNG
PHU_MONG = {"dong_chi_nhan": 28, "o_chu_so": 2, "o_ngoai_vung": 1, "o_chinh_tay": 1}
DONG_DAU, DONG_CUOI = 5, 137
TOL = Decimal("0.5")                               # VND: dưới nửa đồng là làm tròn, ⛔ lệch

#: ⭐ Đ5 — CHECK theo THỰC THỂ *(đo lần đầu 20/11, rồi khai)*. Khác ⇒ ĐỎ cả hai chiều.
MONG_CHECK: dict[str, dict[str, Any]] = {
    'Group': {'nb_do': 24, 'nb_trong': 0, 'nb_khac_0': ('Group@202405', 'Group@202406', 'Group@202411', 'Group@202412', 'Group@202501', 'Group@202502', 'Group@202503', 'Group@202504', 'Group@202505', 'Group@202506', 'Group@202507', 'Group@202508'), 'cb_do': 6, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': ('Group@202410', 'Group@202411', 'Group@202412', 'Group@202501', 'Group@202502', 'Group@202503'), 'cb_khong_do': 18},
    'VisionLab': {'nb_do': 24, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 0, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': (), 'cb_khong_do': 24},
    'TeraSofts': {'nb_do': 24, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 0, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': (), 'cb_khong_do': 24},
    'SuperMinds': {'nb_do': 24, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 0, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': (), 'cb_khong_do': 24},
    'Astronex': {'nb_do': 24, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 0, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': (), 'cb_khong_do': 24},
    'IOs': {'nb_do': 24, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 0, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': (), 'cb_khong_do': 24},
    'Headquarters': {'nb_do': 24, 'nb_trong': 0, 'nb_khac_0': (), 'cb_do': 23, 'cb_dat': 14, 'cb_dat_co_so': 0, 'cb_dat_0_0': 14, 'cb_khong_dat': ('Headquarters@202411', 'Headquarters@202412', 'Headquarters@202501', 'Headquarters@202502', 'Headquarters@202503', 'Headquarters@202504', 'Headquarters@202505', 'Headquarters@202506', 'Headquarters@202507'), 'cb_khong_do': 1},
    'CHECKING': {'nb_do': 0, 'nb_trong': 24, 'nb_khac_0': (), 'cb_do': 0, 'cb_dat': 0, 'cb_dat_co_so': 0, 'cb_dat_0_0': 0, 'cb_khong_dat': (), 'cb_khong_do': 24},
}
#: ⭐ số ô KHÁC RỖNG theo (thực thể, năm) + 2 cột năm.
MONG_O: dict[str, int] = {
    'y24': 82,
    'y25': 83,
    'group_2024': 891,
    'group_2025': 875,
    'visionlab_2024': 903,
    'visionlab_2025': 843,
    'terasofts_2024': 915,
    'terasofts_2025': 843,
    'superminds_2024': 912,
    'superminds_2025': 840,
    'astronex_2024': 903,
    'astronex_2025': 843,
    'ios_2024': 876,
    'ios_2025': 840,
    'headquarters_2024': 956,
    'headquarters_2025': 900,
    'checking_2024': 611,
    'checking_2025': 590,
}
#: ⭐ AC-4 — (thực thể, kỳ) có 0 ô ⇒ `chua_co_du_lieu` có tên.
CHUA_CO_DU_LIEU: tuple[str, ...] = ()

_RE_CHU_SO = re.compile(r"\d{1,3}(\.\d{3})+")


def _cs(n: int) -> str:
    s, n = "", n + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    V = tho.get("values")
    if not isinstance(V, list) or len(V) != DONG_CUOI or any(not isinstance(h, list) for h in V):
        raise ValueError(f"`values` phải {DONG_CUOI} hàng *(A1:GU{DONG_CUOI})*")
    W = 203
    V = [list(h) + [""] * (W - len(h)) for h in V]
    if any(len(h) != W for h in V):
        raise ValueError("`values` rộng quá 203 cột *(A:GU)*")
    nhan3 = [str(V[2][j]).strip() for j in (4, 5, 7, 8)]
    if nhan3 != ["HDCode", "HDNameEN", "Y24", "Y25"] or not str(V[2][6]).startswith("Logic"):
        raise ValueError("hàng 3 ⛔ đúng `E`=HDCode · `F`=HDNameEN · `G`=Logic… · `H`=Y24 · `I`=Y25")
    # cột kỳ: nhóm thực thể (hàng 1, lấp tiến) × kỳ (hàng 3)
    cot_j: dict[int, str] = {7: "y24", 8: "y25"}
    cur, thay = None, {}
    for j in range(10, W):
        if not _rong(V[0][j]):
            cur = str(V[0][j]).strip()
        ky = V[2][j]
        if _rong(ky):
            continue
        if cur not in ENT or str(ky).strip() not in KY:
            raise ValueError(f"cột {_cs(j)}: thực thể/kỳ ⛔ thuộc 8 thực thể × 24 kỳ")
        cot_j[j] = f"{cur.lower()}_{str(ky).strip()}"
        thay[cot_j[j]] = j
    if tuple(c for c in COT_KY if c in thay) != COT_KY or len(thay) != len(COT_KY):
        raise ValueError(f"cột kỳ đọc được {len(thay)} ≠ {len(COT_KY)} = 8 thực thể × 24 kỳ")
    ngoai = sorted(_cs(j) for h in V[4:] for j, x in enumerate(h) if j >= 10 and j not in cot_j and not _rong(x))
    if ngoai:
        raise ValueError(f"cột ⛔ tiêu đề kỳ mà có ô giá trị: {sorted(set(ngoai))}")

    dong, chi_nhan, chu_so = [], [], []
    for i in range(DONG_DAU - 1, DONG_CUOI):
        h, ds = V[i], i + 1
        cells: dict[str, Any] = {}
        for j, c in cot_j.items():
            x = h[j]
            if _rong(x):
                x = None
            elif isinstance(x, bool):
                raise ValueError(f"ô {_cs(j)}{ds}: bool ⛔ ở cột giá trị")
            elif isinstance(x, str):
                if x.strip() == "-":
                    x = None
                elif la_o_loi(x):
                    pass
                elif _RE_CHU_SO.fullmatch(x.strip()):
                    chu_so.append({"dong_sheet": ds, "cot": c, "o": f"{_cs(j)}{ds}", "chuoi": x})
                    x = None
                else:
                    raise ValueError(f"ô {_cs(j)}{ds}: chữ lạ ở cột giá trị")
            cells[c] = x
        lab = [None if _rong(h[j]) else h[j] for j in (4, 5, 6, 9)]
        if all(x is None for x in cells.values()):
            if any(x is not None for x in lab):
                chi_nhan.append({"dong_sheet": ds, "ma": lab[0], "ten": lab[1]})
            continue
        cap = sum(1 for j in range(4) if isinstance(h[j], str) and h[j].strip().lower() == "x")
        dong.append([ds, *lab, cap, *[cells[c] for c in COT[5:]]])
    if not dong:
        raise ValueError("0 hàng dữ liệu — mẫu số 0 (Đ3)")
    # ô số lạc ở hàng 4 (trên hàng tiêu đề kỳ, ngoài bảng): ghi nguyên
    ngoai_vung = [{"dong_sheet": 4, "o": f"{_cs(j)}4", "gia_tri": V[3][j]} for j in range(W) if not _rong(V[3][j])]
    tay = tho.get("o_chinh_tay")
    if not isinstance(tay, list) or not tay:
        raise ValueError("`o_chinh_tay` ⛔ rỗng — AC-3 đòi ô ATL AH12 có tên")
    for t in tay:
        if not re.search(r"-\s*0\.5\s*$", str(t.get("cong_thuc", ""))):
            raise ValueError("`o_chinh_tay.cong_thuc` ⛔ kết thúc `-0.5`")
    return {
        "cot": ["dong_sheet", *COT],
        "dong": dong,
        "phu": {"dong_chi_nhan": chi_nhan, "o_chu_so": chu_so, "o_ngoai_vung": ngoai_vung,
                "o_chinh_tay": tay},
        "ghi_chu": (
            f"Daily Report 3 (Sign off, PD 605) = {len(dong)} hàng sheet {DONG_DAU}…{DONG_CUOI} có giá trị × "
            "192 cột kỳ (8 thực thể × 24 kỳ 202401…202512) + 2 cột năm Y24 · Y25; tab dán giá trị "
            "(0 công thức). Hàng chỉ có nhãn ở `dong_chi_nhan`; 2 ô chữ-số `1.234…` ở `o_chu_so` (⛔ ép số); "
            "ô lạc hàng 4 ở `o_ngoai_vung`; ATL AH12 chỉnh tay ở `o_chinh_tay` (AC-3, ⛔ config). Cột A:D = "
            "dấu `x` cấp (đếm vào `cap`); `J` = nhãn nguồn. Hai CHECK IX.PL khai ở MONG_CHECK. Bản A-CCR "
            "(`5. Daily Report 3` 1940×40) khác bố cục ⇒ ⛔ so từng ô (xem BG)."),
    }


def do_check(dong: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """CHECK theo thực thể *(mỗi thực thể một khối 24 kỳ)*. Mã trùng ở ≥ 2 hàng ⇒ `ValueError`."""
    hang: dict[str, dict[str, Any]] = {}
    for d in dong:
        m = d["ma"]["chu"] if isinstance(d["ma"], dict) else d["ma"]
        if m in _dr.MA_CAN:
            if m in hang:
                raise ValueError(f"mã `{m}` ở ≥ 2 hàng — ⛔ đo được CHECK")
            hang[m] = d
    return {e: _dr.kiem_check(hang, [(f"{e}@{k}", f"{e.lower()}_{k}") for k in KY], TOL) for e in ENT}


def _tom(r: dict[str, Any]) -> dict[str, Any]:
    return {"nb_do": r["nb_do"], "nb_trong": r["nb_trong"], "nb_khac_0": tuple(r["nb_khac_0"]),
            "cb_do": r["cb_do"], "cb_dat": r["cb_dat"], "cb_dat_co_so": r["cb_dat_co_so"],
            "cb_dat_0_0": r["cb_dat_0_0"], "cb_khong_dat": tuple(r["cb_khong_dat"]),
            "cb_khong_do": r["cb_khong_do"]}


def dem_o(dong: list[dict[str, Any]]) -> dict[str, int]:
    out = {c: sum(1 for d in dong if d[c] is not None) for c in COT_NAM}
    for e in ENT_COT:
        for y in ("2024", "2025"):
            out[f"{e}_{y}"] = sum(1 for d in dong for k in KY if k[:4] == y and d[f"{e}_{k}"] is not None)
    return out


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5)*: CHECK theo thực thể ↔ `MONG_CHECK` · số ô theo (thực thể, năm) ↔ `MONG_O` · kỳ 0 ô ↔
    `CHUA_CO_DU_LIEU`. Tập rỗng ⇒ `ValueError` *(Đ3)*; mong ⛔ khai ⇒ ĐỎ *(⛔ xanh vì rỗng)*."""
    if not dong:
        raise ValueError("0 hàng — mẫu số 0, ⛔ nền xanh (Đ3)")
    if set(MONG_CHECK) != set(ENT) or not MONG_O:
        raise ValueError("MONG_CHECK / MONG_O ⛔ khai — cổng ⛔ đo được")
    thieu: list[str] = []
    ck = do_check(dong)
    for e in ENT:
        thieu += _dr.so_voi_mong(e, _tom(ck[e]), MONG_CHECK[e])
    o = dem_o(dong)
    thieu += [f"{k}: {o[k]}≠{m}" for k, m in MONG_O.items() if o.get(k) != m]
    chua = tuple(f"{e}@{k}" for e in ENT_COT for k in KY if all(d[f"{e}_{k}"] is None for d in dong))
    if chua != CHUA_CO_DU_LIEU:
        thieu.append(f"chua_co_du_lieu {chua}≠{CHUA_CO_DU_LIEU}")
    c_so = sum(c["cb_dat_co_so"] for c in ck.values())
    c_00 = sum(c["cb_dat_0_0"] for c in ck.values())
    return {"thieu": thieu, "lac": [],
            "dai": (f"{len(dong)} hàng × 192 cột kỳ (8 thực thể × 202401…202512) · CHECK ② đo được "
                    f"{sum(c['cb_do'] for c in ck.values())} kỳ-thực thể: đạt ② có số {c_so} · đạt ② 0=0 {c_00} · "
                    f"⛔ đạt {sum(len(c['cb_khong_dat']) for c in ck.values())} · CHECK ① NB=0 đo được "
                    f"{sum(c['nb_do'] for c in ck.values())} kỳ-thực thể, ≠0 ở "
                    f"{sum(len(c['nb_khac_0']) for c in ck.values())} · kỳ 0 ô: {len(chua)}")}
