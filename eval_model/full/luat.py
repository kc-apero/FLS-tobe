"""LUAT cua bo gia lap full luong — MOT cho duy nhat, dung chung cho:
  · sinh_full.py  (tinh dap an)
  · he_thong.md   (van ban dua cho model — viet lai dung cac luat nay bang loi)

⛔ Khong import `fls.*`: dap an phai doc lap voi code dang kiem.
Can cu: AP Voi FLS v3.1.0 §4.1–§4.4 (cong thuc AS-IS doc nguyen van) + luat TO-BE
da chot (QĐ-ITL-57/62: dung sai 1.000 VND, ngoai te 0; N×M khong doan). Phan nao
AP chua chot (chuoi PL, Mapping Master gia lap) la QUY UOC CUA BO GIA LAP, ghi ro
trong he_thong.md.
"""
from __future__ import annotations

import re
import unicodedata
from decimal import ROUND_HALF_UP, Decimal

NA = "Need to manual input"
IH = "Input here"
KHOI = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")
KHOI_PNL = ("hd", "pay_type", "cdt1", "svc_start", "svc_end")
MAC_DINH = {"hd": "OGA | GAC - Other", "pay_type": "Thanh toán (Regular)",
            "cdt1": "SHQ2 | Headquarters2", "id_payee": "VD0", "invoice": "Nợ hoá đơn"}
CO_PB = "Need to Allocate to CFA2"
BAN_KHAI = ["STT", "Ngày", "Số CT", "Diễn giải", "PS Nợ", "PS Có", "Reference number",
            "Reference number_adjust"]
TY_GIA = {"VND": Decimal(1), "USD": Decimal(26300)}
NGAY = [f"2026-10-{d:02d}" for d in range(1, 8)]

# ---------------------------------------------------------------- A1
_TEN_SHEET = re.compile(r"^R \| (?P<tk>\d+)_(?P<bank>\S+) (?P<cur>[A-Z]{3})_(?P<le>\S+)$")


def doc_ten_sheet(ten: str) -> dict:
    m = _TEN_SHEET.match(ten)
    if not m:
        raise ValueError(ten)
    return m.groupdict()


def drift(khai: list[str], tieu_de: list[str]) -> list[dict]:
    t = [{"loai": "them", "cot": c} for c in tieu_de if c not in khai] + \
        [{"loai": "bo", "cot": c} for c in khai if c not in tieu_de]
    if not t and list(khai) != list(tieu_de):
        t = [{"loai": "doi_vi_tri", "cot": "*"}]
    return t


def ref_hieu_luc(dong: dict) -> str:
    a = (dong.get("Reference number_adjust") or "").strip()
    return a if a else (dong.get("Reference number") or "").strip()


# ---------------------------------------------------------------- A2
_BO = re.compile(r"[\s\-_.,/\\]+")
_KH = re.compile(r"^\d(?:\.\d+)?E\+\d+$", re.I)


def canon_ref(x) -> str | None:
    if x is None:
        return None
    x = str(x).strip()
    if not x or x.startswith("#"):
        return None
    if _KH.match(x):
        x = "%.0f" % float(x)
    x = unicodedata.normalize("NFKC", x).upper()
    return _BO.sub("", x) or None


def xep_hinh(bank: list[dict], nguon: list[dict]) -> str:
    """bank/nguon: dict co 'tien' (Decimal) va 'cur'."""
    if not bank or not nguon:
        return "KHONG_GHEP"
    cur = {d["cur"] for d in bank + nguon if d["cur"]}
    if len(cur) >= 2:
        return "E"
    ds = Decimal(1000) if all(d["cur"] == "VND" for d in bank + nguon) else Decimal(0)
    if abs(sum(d["tien"] for d in bank) - sum(d["tien"] for d in nguon)) > ds:
        return "F"
    if len(bank) == 1 and len(nguon) == 1:
        return "A"
    if len(bank) == 1:
        return "B"
    if len(nguon) == 1:
        return "C"
    return "D"


# ---------------------------------------------------------------- A3
def mid(khoi: str, t: str, ngay: str) -> str:
    """U do duoc tren so that: and() trong ArrayFormula gop ca cot => U = T, tru 'Input here'."""
    if t == IH:
        return ngay[:4] + ngay[5:7] if khoi in ("svc_start", "svc_end") else MAC_DINH[khoi]
    return t


def final(s: str, u: str) -> str:
    return u if (s == NA or s == "") else s


def allocate(cdt1_final: str, hd_final: str, mm: dict) -> tuple[str, str, str]:
    m = mm.get(hd_final)
    if m is None:
        return cdt1_final, "#N/A", "#N/A"
    av = CO_PB if m["K"] == CO_PB else cdt1_final
    aw = m["L"] if m["L"] else "No need"
    return cdt1_final, av, aw


# Quy tac dien tay — xet THEO THU TU, quy tac dau tien khop thang.
QUY_TAC_TAY = [
    ("CHUYEN NOI BO", {"hd": "NB | Lưu chuyển nội bộ", "pay_type": "Chuyển nội bộ", "cdt1": "SHQ2 | Headquarters2"}),
    ("PHI DICH VU",   {"hd": "BF | Bank Fee", "pay_type": "Phí ngân hàng", "cdt1": "SHQ2 | Headquarters2"}),
    ("LAI TIEN GUI",  {"hd": "FI | Financial Income", "pay_type": "Thu khác", "cdt1": "SHQ2 | Headquarters2"}),
    ("NOP THUE TNDN", {"hd": "CIT | Corporate Income Tax", "pay_type": "Nộp thuế", "cdt1": "SHQ2 | Headquarters2"}),
]
_VENDOR = re.compile(r"\bVDX\d{3}\b")


def dien_tay(dien_giai: str, lich_su: dict) -> tuple[dict, str | None]:
    """Tra (T theo khoi, vendor tim thay). Khong can cu => hd/pay_type/cdt1 = 'Input here'."""
    dg = (dien_giai or "").upper()
    t = {k: IH for k in KHOI}
    for tu, gt in QUY_TAC_TAY:
        if tu in dg:
            t.update(gt)
            return t, None
    m = _VENDOR.search(dg)
    if m and m.group(0) in lich_su:
        v = m.group(0)
        t.update({"hd": lich_su[v]["hd"], "pay_type": "Thanh toán (Regular)", "cdt1": lich_su[v]["cdt1"],
                  "id_payee": v})
        return t, v
    return t, None


# ---------------------------------------------------------------- CA / report
def musd(tien: Decimal, cur: str) -> Decimal:
    bvnd = TY_GIA[cur] * tien / Decimal(10**9)
    return bvnd / TY_GIA["USD"] * Decimal(1000)


SO_LE = 8   # mUSD = TRIEU USD (AP: bVND ÷ ty gia × 10^3) -> 8 chu so = 0,01 USD


def lam_tron(x: Decimal, n: int = SO_LE) -> str:
    q = x.quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)
    return format(q.copy_abs() if q == 0 else q, "f")


DONG_PL_HD = ["GI", "OMC", "API", "SC", "LC", "PS", "HR", "MC", "GAC", "FI", "BF", "CIT"]
DONG_PL_TONG = {"PL2": ["GI", "OMC"], "PL3": ["PL2", "API", "SC", "LC"], "PL4": ["PL3", "PS"],
                "PL5": ["PL4", "HR"], "PL6": ["PL5", "MC", "GAC", "FI", "BF"], "PL8": ["PL6", "CIT"]}
