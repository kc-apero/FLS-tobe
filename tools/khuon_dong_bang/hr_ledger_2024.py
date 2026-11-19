"""Khuôn đóng băng `hr_ledger_2024` — ĐẦU VÀO Y2024 của sổ HR *(ISP 3.1.2 · DT6b · `WO-225` AC-1)*.

    python tools/dong_bang_sheet.py hr_ledger_2024 <bản_thô.json> --mong 1381
        ⇒ tests/fixture/dau_vao/hr_ledger_2024.json

⭐ **Nguồn** file GỐC `H1000 Ledger (APERO-HR Allocate HD_FS1)` id `1YEyGxBYXaa6n4dX9_rWXoFn6NgJStTP2DKJd64ZAoD4`
*(chủ share SA quyền nhận xét — dùng CHỈ-ĐỌC)* — hai tab **có giá trị thật** *(bản `[COPY]` cùng tên ra `#REF!` vì
IMPORTRANGE gãy — chính là `thieu_nguon` ở `gl_hr_408/413`)*:
  · `1.3 Ledger NIS/INT/COM 2024` — 969 hàng · `1.3 Ledger PIT 2024` — 412 hàng *(tiêu đề hàng 3, dữ liệu từ hàng 4)*.
Đo 19/11: **969 + 412 = 1.381** hàng, cột `A` là serial NGÀY ở **1.381/1.381**; kỳ: NIS 2024-11 = 165 · 2024-12 = 536 ·
2025-01 = 268 · PIT 2025-01 = 200 · 2025-04 = 212.

⛔⛔ **Riêng tư** *(sổ HR — lương, tên người)*. Bản đồ cột bằng **hàng tiêu đề TRƯỚC**; chỉ đọc 9 cột
`A·D·E·F·G·H·S·T·AG` *(⛔ `B` Số chứng từ · `C` Diễn giải · `I·J·K` nội dung PE/PI · `M…R` ID Payee/PMSlip/PESlip/…)*.
Cột `H` *(Payment Type)* có **6** ô mang số tài khoản — ⚠ KHÁC DT6: ở Y2024 ô là **dãy chữ số liền, ⛔ có
tiền tố `R |`** *(đo hình dạng 19/11: 6/6 ô = đúng 1 dãy 9 chữ số)* ⇒ CHE về `R` *(theo `WO-225`: "che như DT6")*;
dạng `R | <số>_<NH>_<ĐƠN VỊ>` *(DT6)* cũng che về `R`. ⛔ Ảnh ⛔ giữ chữ số nào. Mọi cột chữ có
TẬP ĐÓNG *(dùng chung `_gl_hr.py`)*; giá trị lạ ⇒ ĐỎ, lời lỗi ⛔ in giá trị.

⭐ **Khoá** `dong_sheet` *(⛔ trùng)*: tab NIS = hàng sheet; tab PIT = `100000 + hàng sheet` *(hai tab chung một ảnh,
`tab` nói rõ; `dong_sheet` ≥ 100000 ⇒ PIT)*. **Đ5**: số hàng MỖI `(tab, kỳ)` + Σ PS Có mỗi kỳ khai `mong`, ĐỎ cả hai chiều.
"""
from __future__ import annotations

import datetime
import importlib.util
import re
import pathlib
import sys
from collections import Counter
from decimal import Decimal
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "_gl_hr.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__gl_hr", _P)
_gl = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _gl
if not hasattr(_gl, "chuan_bi"):
    _spec.loader.exec_module(_gl)

BANG = "HR.Ledger.2024"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("tab", "ky", "D", "E", "F", "G", "H", "hd", "cdt1", "le")
KIEU_COT = {"tab": "chu", "D": "chu?", "E": "so?", "F": "so?", "G": "chu?", "H": "chu?",
            "hd": "chu?", "cdt1": "chu?", "le": "chu?"}
RA = "tests/fixture/dau_vao/hr_ledger_2024.json"
PHU_MONG = {"tong_ky": 5}

TABS = ("1.3 Ledger NIS/INT/COM 2024", "1.3 Ledger PIT 2024")
TEN_TAB = {TABS[0]: "NIS", TABS[1]: "PIT"}
#: Cột sheet đọc *(theo thứ tự)* và TIÊU ĐỀ hàng 3 mong *(ánh xạ theo TÊN, ⛔ theo vị trí)*.
COT_THO = ("A", "D", "E", "F", "G", "H", "S", "T", "AG")
TIEU_DE = ("Ngày chứng từ", "Đơn vị tiền tệ", "PS Nợ", "PS Có", "Tài khoản",
           "Loại giao dịch (Payment Type)", "Budget Code (HDCode)", "Chủ dự toán (CDT1)", "LE")
DONG_DAU_SHEET = 4
OFFSET_PIT = 100000
EPOCH = datetime.date(1899, 12, 30)
TAP_DONG = {"D": _gl.TIEN_TE, "G": _gl.TAI_KHOAN, "H": _gl.PAYMENT_TYPE, "hd": _gl.HD_CODE,
            "cdt1": _gl.CDT1, "le": _gl.LE}
CHU = tuple(TAP_DONG)

#: Đ5 — đo 19/11 *(mỗi số đếm MỘT vật: hàng sheet có ngày, theo tab × kỳ)*.
MONG_TAB_KY = {("NIS", 202411): 165, ("NIS", 202412): 536, ("NIS", 202501): 268,
               ("PIT", 202501): 200, ("PIT", 202504): 212}
#: Đ5 — Σ PS Có *(cột F, VND)* mỗi kỳ, gộp hai tab. Khác ⇒ ĐỎ.
MONG_F_KY = {202411: 286400000, 202412: 5140567470, 202501: 5543361433, 202504: 551671054}
#: Đ5 — số ô `H` bị CHE về `R` *(đo 19/11; mẫu số > 0 — Đ3)*.
MONG_H_R = 6


#: Y2024: ô Payment Type mang MỖI số tài khoản trần *(≥ 6 chữ số liền)* ⇒ che về `R`.
_SO_TK_TRAN = re.compile(r"\d{6,}")


def _che(v: Any) -> tuple[Any, bool]:
    if isinstance(v, str) and _SO_TK_TRAN.fullmatch(v):
        return "R", True
    return _gl.che_tai_khoan(v)


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v == "")


def chuan_bi_chung(tho: dict[str, Any], *, tabs_mong: tuple[str, str], ten_tab: dict[str, str], nam: str,
                   cho_so_le: bool = False) -> dict[str, Any]:
    """LƯỚI SA `{tabs:[{tab, dong_dau_sheet, cot_sheet, tieu_de, values}]}` → bảng + phụ `tong_ky`.

    ⭐ Phần CHUNG của Y2024 *(`WO-225`)* và Y2025 *(`WO-249` — `hr_ledger_2025` GỌI hàm này, ⛔ chép)*.
    `cho_so_le=True` ⇒ PS Nợ/Có được LẺ *(Y2025 đo 19/11: 9 ô F của tab NIS là phân bổ chia lẻ — `gl_hr_408`
    cũng giữ phần lẻ)*; Σ chính xác bằng `Decimal`. `ValueError` ⇒ TỪ CHỐI. ⛔⛔ lời lỗi KHÔNG mang giá trị ô.
    """
    tabs = tho.get("tabs")
    if not isinstance(tabs, list) or [t.get("tab") for t in tabs if isinstance(t, dict)] != list(tabs_mong):
        raise ValueError(f"`tabs` phải đúng 2 tab {list(tabs_mong)} theo thứ tự")
    dong: list[list[Any]] = []
    tong: dict[tuple[str, int], list[Any]] = {}
    for t in tabs:
        ten = ten_tab[t["tab"]]
        if t.get("cot_sheet") != list(COT_THO):
            raise ValueError(f"`cot_sheet` phải đúng {list(COT_THO)} *(⛔ phủ B·C·I·J·K·M…R)*")
        if t.get("dong_dau_sheet") != DONG_DAU_SHEET:
            raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
        if tuple(t.get("tieu_de") or ()) != TIEU_DE:
            raise ValueError(f"tab {ten}: tiêu đề hàng 3 của 9 cột ≠ bản khai — cột xê dịch hay sheet "
                             "đổi bố cục; ánh xạ theo TÊN nên ⛔ đóng băng")
        values = t.get("values")
        if not isinstance(values, list) or not values or any(
                not isinstance(h, list) or len(h) != len(COT_THO) for h in values):
            raise ValueError(f"tab {ten}: `values` phải lưới ≥ 1 hàng × {len(COT_THO)} ô")
        for i, h in enumerate(values):
            hang = DONG_DAU_SHEET + i
            a, d_, e, f, g, hh, s, tt, le = h
            if not isinstance(a, int) or isinstance(a, bool) or a < 1:
                raise ValueError(f"tab {ten} hàng sheet {hang}: cột A *(ngày)* phải serial số nguyên ≥ 1")
            ngay = EPOCH + datetime.timedelta(days=a)
            ky = ngay.year * 100 + ngay.month
            hh, che = _che(None if _rong(hh) else hh)
            khoa = hang + (OFFSET_PIT if ten == "PIT" else 0)
            dong.append([khoa, ten, ky, *(None if _rong(x) else x for x in (d_, e, f, g)), hh,
                         *(None if _rong(x) else x for x in (s, tt, le))])
            tk = tong.setdefault((ten, ky), [0, Decimal(0), Decimal(0)])
            tk[0] += 1
            for j, v in ((1, e), (2, f)):
                if not _rong(v):
                    if isinstance(v, bool) or not isinstance(v, (int, float, Decimal)) or (
                            not cho_so_le and v != int(v)):
                        raise ValueError(f"tab {ten} hàng sheet {hang}: PS Nợ/Có phải số"
                                         + ("" if cho_so_le else " nguyên VND"))
                    tk[j] += Decimal(str(v))
    phu = [{"tab": k[0], "ky": k[1], "so_hang": v[0], "tong_E": _gl._tong([v[1]]), "tong_F": _gl._tong([v[2]])}
           for k, v in sorted(tong.items())]
    return {"cot": [KHOA, *COT], "dong": dong, "phu": {"tong_ky": phu},
            "ghi_chu": (f"Y{nam} HR *(lưới SA, file gốc)*: {len(dong)} hàng = "
                        + " + ".join(f"{sum(1 for r in dong if r[1] == n)} {n}" for n in ten_tab.values())
                        + ", khoá dong_sheet = hàng sheet *(PIT +100000)*; `ky` suy từ cột A. ⛔⛔ BỎ cột B Số "
                        "chứng từ · C Diễn giải · I·J·K nội dung PE/PI · M…R ID Payee/PMSlip/PESlip/PELine/"
                        "PISlip/PILine · U·V·W… *(chỉ đọc 9 cột A·D·E·F·G·H·S·T·AG)*. CHE số tài khoản ngân "
                        "hàng ở H: `R | <số>_…` ⇒ `R`. Bảng phụ `tong_ky` = số hàng + Σ PS Nợ/Có theo (tab, kỳ).")}


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    return chuan_bi_chung(tho, tabs_mong=TABS, ten_tab=TEN_TAB, nam="2024")


def _chu(v: Any) -> str | None:
    return None if v is None else (v["chu"] if isinstance(v, dict) else str(v))


def thieu_lac_chung(dong: list[dict[str, Any]], *, mong_tab_ky: dict, mong_f_ky: dict, mong_h_r: int,
                    tap_dong: dict, nam: str, mong_le_na: int | None = None) -> dict[str, Any]:
    """Cổng Y2024/Y2025 *(Đ5 — `mong` khai trước, NO cả hai chiều)*: ⒜ số hàng mỗi `(tab, kỳ)` ≠ mong;
    ⒝ Σ PS Có mỗi kỳ ≠ mong *(`Decimal`)*; ⒞ ô chữ ngoài TẬP ĐÓNG *(PII lạc cột)*; ⒟ số ô `H` bị che ≠ mong;
    ⒠ khoá trùng/PIT lệch offset; ⒡ *(Y2025)* số ô `LE = #N/A` ≠ `mong_le_na` — tập đóng có `#N/A` nên
    PHẢI đếm riêng *(⛔ để nó lọt như một giá trị hợp lệ)*."""
    thieu: list[str] = []
    thuc: Counter = Counter((_chu(d["tab"]), int(d["ky"])) for d in dong)
    for k in sorted(set(thuc) | set(mong_tab_ky)):
        if thuc.get(k, 0) != mong_tab_ky.get(k, 0):
            thieu.append(f"tab_ky@{k[0]}:{k[1]}:{thuc.get(k, 0)}/{mong_tab_ky.get(k, 0)}")
    f_ky: dict[int, Decimal] = {}
    for d in dong:
        f = d["F"]
        f = f["chu"] if isinstance(f, dict) else f
        if f is not None:
            f_ky[int(d["ky"])] = f_ky.get(int(d["ky"]), Decimal(0)) + Decimal(str(f))
    for k in sorted(set(f_ky) | set(mong_f_ky)):
        if f_ky.get(k, Decimal(0)) != Decimal(str(mong_f_ky.get(k, 0))):
            thieu.append(f"F_ky@{k}:{_gl._tong([f_ky.get(k, 0)])}/{mong_f_ky.get(k, 0)}")
    n_r = n_na = 0
    for d in dong:
        ds = int(d["dong_sheet"])
        if (ds >= OFFSET_PIT) != (_chu(d["tab"]) == "PIT"):
            thieu.append(f"khoa_tab@{ds}")
        for c in CHU:
            s = _chu(d[c])
            if s is None:
                continue
            if s not in tap_dong[c]:
                thieu.append(f"{c}_la@{ds}")
        if _chu(d["H"]) == "R":
            n_r += 1
        if _chu(d["le"]) == "#N/A":
            n_na += 1
    if n_r != mong_h_r:
        thieu.append(f"H_che@khác:{n_r}/{mong_h_r}")
    if mong_le_na is not None and n_na != mong_le_na:
        thieu.append(f"le_NA@khác:{n_na}/{mong_le_na}")
    dai = (f"Y{nam} HR: {len(dong)} hàng · {len(thuc)} (tab,kỳ) · kỳ {sorted({k[1] for k in thuc})} · "
           f"Σ PS Có theo kỳ {dict(sorted((k, _gl._tong([v])) for k, v in f_ky.items()))} · {n_r} ô H che")
    return {"thieu": thieu, "lac": [], "dai": dai}


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    return thieu_lac_chung(dong, mong_tab_ky=MONG_TAB_KY, mong_f_ky=MONG_F_KY, mong_h_r=MONG_H_R,
                           tap_dong=TAP_DONG, nam="2024")
