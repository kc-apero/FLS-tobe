"""Adapter A — ghep tien bank <-> lenh chi PM. Bac thang, ⛔ khong doan.

★★ DO TRUOC KHI VIET, va so lieu LAT HAI TIEN DE CUA SPEC `DEV-10` v0.1.

⓵ **Spec noi `reference` song o PHIEU.** Do tren `[Importrange]PM_Unpivot`
   (3.703 dong, doc live 2026-08-27): reference song o **DONG**. Trong 1.468
   phieu co 579 phieu nhieu dong, va **526 phieu mang 2-36 reference KHAC NHAU**.
   Tien o cot *"Tong so tien thanh toan"* cung KHAC nhau tung dong (493/579).
   ⇒ Phep ghep la **bank ↔ DONG**, khong phai bank ↔ phieu. Va con so *"289 dong
   du bi bo im lang"* trong spec **khong tai lap duoc tu nguon nay**.

⓶ **Spec lo mot ma → N dong PM.** So that: chieu nguoc lai lon hon nhieu —
   mot ma → **N DONG BANK**: 8.627 ma co 1 dong, 297 ma co 2, 58 co 3 … toi 32.
   Do la tra nhieu lan + phi bank dung chung mot ma.

★★★ VA DAY LA CON SO PHAI NOI THANG: phep ghep DUNG **NHO HON** phep ghep dang
dung. AS-IS `VLOOKUP` bao ghep **33,2%** (3.312/9.992) nhung **968 dong trong so
do (29%) khong khop tien**. FLS voi cong Σ that: **26,79%** (2.677 dong) ghep
duoc **ma khong phai doan**, cong **678 dong** co ma khop nhung tien khong khop
— va 678 dong do vao hang cho **kem ly do co ten**, ⛔ khong bien mat.

⇒ ⛔ Day KHONG phai tut lui. Day la lan dau con so co nghia.

★ SAU HINH DANG, do tren du lieu that:

    A  1 bank × 1 PM  · Σ khop            2.256 ma · 2.256 dong  -> GHEP
    B  1 bank × N PM  · Σ khop               27 ma ·    27 dong  -> GHEP + chia tien
    C  N bank × 1 PM  · Σ khop               80 ma ·   394 dong  -> GHEP (tra nhieu lan)
    D  N bank × M PM  · Σ khop                5 ma ·    27 dong  -> ⛔ KHONG DOAN
    E  tien te KHAC nhau                    119 ma ·   199 dong  -> day nguoi (can ty gia)
    F  Σ lech                               325 ma ·   452 dong  -> day nguoi

⚠ Script do nhap dem `E` la 120: no coi o tien te **RONG** la *"khac nhau"*.
RONG la **khong biet**, ⛔ khong phai **khac** — nen nhom do (`20260708000001`)
roi ve `F`, va dung: tien that su lech 240 (phi bank).

⛔ `D` bi tu choi DU Σ KHOP: N×M co nhieu cach chia tien khac nhau ma **deu cong
dung**. Chon mot cach la **may quyet thay nguoi** (`INV-I16`). 27 dong.

⚠ Dung sai cong Σ = **0** (`GAP-CR1-01` chua chot). Trong `F` da nhin thay ro
hai lop se duoc cuu neu ke toan cho dung sai: **phi bank** (`15.400 VND`,
`68,53 USD` dung chung ma voi khoan chinh) va **tra thieu/thua le**. ⛔ Nhung noi
nguong la quyet dinh cua ke toan truong, ⛔ khong phai cua code.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Iterable, Sequence

from fls.canon.o_loi import la_o_loi

# ---- vi tri cot cua `[Importrange]PM_Unpivot` ------------------------------
# ⚠ Tieu de o dong **2**, du lieu tu dong **3**. Doc lech mot dong thi mat dong
# dau tien VA header thanh mot dong du lieu — toi da mac dung loi nay 27/08.
PM_DONG_TIEU_DE = 2
PM_DONG_DAU = 3
PM_COT: dict[str, int] = {
    "cur": 8, "tien": 9, "slip": 15, "line": 16,
    "hd": 21, "cdt1": 22, "status": 24, "ref": 25,
}
PM_TIEU_DE_MONG_DOI: dict[int, str] = {
    8: "Đơn vị tiền tệ (Currency)",
    9: "Tổng số tiền thanh toán (Transaction Amount)",
    15: "ID PMSlip",
    16: "ID PMLine",
    21: "Budget Code (HDCode)",
    22: "Chủ dự toán (CDT1)",
    24: "Status_Final",
    25: "Reference number",
}

_BO = re.compile(r"[\s\-_.,/\\]+")
_KHOA_HOC = re.compile(r"^\d(?:\.\d+)?E\+\d+$", re.I)


class NguonPMDoiHinhDang(RuntimeError):
    """Nguon PM doi cot thi NO TO. ⛔ Khong doan, khong am tham lech mot cot."""


def canon_ref(raw: Any) -> str | None:
    """Chuan hoa ma tham chieu. None neu khong con ky tu co nghia.

    ⚠ Ma loi **khong bao gio** thanh khoa — neu khong thi moi dong `#N/A` ben
    nay ghep voi moi dong `#N/A` ben kia.

    ⚠ Sua mot ho hong CUA DUONG DOC, khong phai cua so: Sheets API tra so chung
    tu DAI duoi dang khoa hoc (`4.36619E+15`). Khong dung lai thi hai ben cung
    mot ma ma khong ghep duoc.

    ⛔ CHUA cat tien to bank (`FT<yy><ddd>`…) — `GAP-JOIN-01`. Cat sai la **gop
    hai lenh khac nhau**, hong nang hon la khong ghep.
    """
    if raw is None or la_o_loi(raw):
        return None
    if isinstance(raw, float) and raw == int(raw):
        x = str(int(raw))
    else:
        x = str(raw).strip()
    if not x:
        return None
    if _KHOA_HOC.match(x):
        try:
            x = "%.0f" % float(x)
        except ValueError:
            pass
    x = unicodedata.normalize("NFKC", x).upper()
    return _BO.sub("", x) or None


@dataclass(frozen=True)
class DongPM:
    """Mot dong lenh chi. `line` la dinh danh muc DONG — ⛔ khong dung `slip`."""
    dong_sheet: int
    slip: str
    line: str
    tien: Decimal | None
    cur: str
    status: str
    ref: str | None
    hd: str | None = None
    cdt1: str | None = None
    # ⚠ Them 2026-08-27 cho anh chup (`fls_pm_line`). `ref` la ma DA CHUAN HOA;
    # anh chup phai giu CA ban nguyen van, ⛔ khong thi be `canon_ref` di ma cong
    # van XANH — dung cai bay da mac mot lan voi hien vat `Classifying`.
    # Mac dinh `None` de moi cho dung `DongPM` san khong phai sua.
    ref_tho: str | None = None


@dataclass(frozen=True)
class DongBank:
    dong_sheet: int
    ref: str | None
    tien: Decimal
    cur: str


# ---- dung sai Σ ------------------------------------------------------------
#
# Owner chot 2026-08-27 (`GAP-CR1-01`): **1.000 dong**.
#
# ⛔⛔ Va no la 1.000 **VND**, ⛔ KHONG phai "1.000 don vi cua tien te nao cung
# duoc". Do truoc khi code, va khoang cach giua hai cach doc rat lon:
#
#   ap 1.000 don vi cho MOI tien te : 105 ma · 171 dong  ← ⛔ NGUY
#   ap 1.000 CHI cho VND            :  20 ma ·  24 dong  ← an toan
#
# Vi sao cach doc thu nhat nguy: 1.000 USD ≈ 26 trieu VND. Cac ca no cho qua:
#
#   lech 660,04 USD tren giao dich   59,96 USD = **1.100%** cua chinh no
#   lech  40,00 USD tren giao dich   20,00 USD =    200%
#   lech 200,00 USD tren giao dich  180,00 USD =    111%
#   lech 307,59 USD tren giao dich  442,27 USD =     70%
#
# Do ⛔ khong phai phi bank hay lam tron — do la tien KHONG KHOP that. Con nhom
# VND <= 1.000 thi lech LON NHAT chi **2,00 dong**, tuc lam tron thuan.
#
# ⭐⭐ **Owner CHOT 2026-08-28 (`QĐ-ITL-62`, dong `GAP-CR1-03`): ngoai te
# ⛔ KHONG co dung sai — may ⛔ KHONG duoc tu dong mot ca lech, du chi vai xu.**
# Lech bao nhieu cung ⇒ dong nam lai HANG CHO cho nguoi xem.
#
# ⛔⛔ Day ⛔ KHONG con la "cho quyet dinh" — no LA quyet dinh. Ai thay so `0`
# nay va tuong day la viec chua lam xong thi ⛔ DUNG "sua cho xong": them mot
# khoa vao `DUNG_SAI` la **doi mot quyet dinh ke toan**, phai xin owner. Co bai
# test khoa dung viec do (`test_KHOA_bang_DUNG_SAI...`).
#
# Can cu do duoc cho quyet dinh nay (do 2026-08-28 tren so that, 2.701 dong da
# ghep — so tien bank cua dong so voi Σ tien dong lenh chi noi vao no):
#   · 2.283 dong khop TUYET DOI
#   ·   418 dong co lech, nhung **400/418 la TRA TUNG PHAN**, ⛔ khong phai sai
#         (`PM00392-4` = 967.758.000 tra bang 4 lan chuyen; tung dong lech toi
#          959 trieu, bon lan cong lai **dung bang dong**)
#   ·    18 dong lech THAT, va **toan bo nam trong 0,40 → 2,00 dong** = lam tron
#   ⇒ **KHONG ca lech ngoai te nao la lam tron**: moi ca USD/HKD deu la tra
#     tung phan. Tuc dung sai ngoai te se ⛔ khong mo them dong nao, chi mo them
#     RUI RO. Gia cua quyet dinh nay do duoc va no la ~0.
#
# ⛔ Va no ⛔ khong duoc suy ra bang ty gia: lop `E` da bi loai vi thieu ty gia;
# muon dung ty gia o day thi phai giai `E` truoc.
DUNG_SAI: dict[str, Decimal] = {
    "VND": Decimal("1000"),          # `QĐ-ITL-57` — 1.000 **VND**
}
DUNG_SAI_MAC_DINH = Decimal("0")     # `QĐ-ITL-62` — moi tien te khac: **0**

# ---- dung sai cho cua ghep TAY (`QĐ-ITL-63`, 2026-08-28) -------------------
#
# ⭐⭐ Owner chot: cua ghep **TAY** doi **CA HAI** dieu kien, lay cai NHO hon:
#       lech <= **1.000 dong**  VA  lech <= **0,5%** cua tien bank
#
# ⛔ Vi sao ⛔ khong dung mot minh con so tuyet doi. `1.000` duoc do va duyet
# tren phep ghep **TU DONG** (`QĐ-ITL-57`), noi khoang lech LON NHAT that chi
# **2,00 dong**. Nhung o cua **TAY** thi nguoi go **chon dong lenh nao cung
# duoc**, nen cung con so ay cho ghep mot dong bank **100 dong** voi mot dong
# lenh **1.099 dong** — lech **999% cua chinh giao dich** ma cong van xanh.
# Bai `test_DO_LO_...` (cu) da ghi lai do lo do bang so.
#
# ⛔ Va vi sao ⛔ khong dung mot minh ty le: 0,5% cua 3,7 ty la **18,5 trieu** —
# rong hon han khoang lam tron. ⇒ Khoan LON phai chan bang so TUYET DOI, khoan
# NHO phai chan bang TY LE. Mot minh cai nao cung ho mot dau.
#
# ⭐ `min(...)` giu nguyen `QĐ-ITL-62`: ngoai te co `DUNG_SAI_MAC_DINH = 0` nen
# `min(0, ty_le) = 0` — ⛔ khong con duong nao lam ngoai te co dung sai.
# ⛔ `tien_bank = 0` ⇒ dung sai **0** (chan mac dinh), ⛔ khong mo cua.
TY_LE_GHEP_TAY = Decimal("0.005")    # `QĐ-ITL-63` — 0,5%


def dung_sai_ghep_tay(cur: set[str], tien_bank: Decimal) -> Decimal:
    """Dung sai cua cua ghep TAY = **min**(so tuyet doi, ty le) — `QĐ-ITL-63`.

    ⛔ Chat hon `dung_sai_cua` (cua ghep TU DONG) **co y**: o day nguoi go chon
    dong lenh, nen mot con so du rong cho lam tron se du rong cho mot khoan nho
    sai hoan toan.
    """
    return min(dung_sai_cua(cur), abs(Decimal(tien_bank)) * TY_LE_GHEP_TAY)


def dung_sai_cua(cur: set[str]) -> Decimal:
    """Dung sai cho mot nhom. ⛔ Nhieu tien te / la tien te ⇒ **0**.

    ⛔ Nhieu tien te thi ⛔ khong duoc lay dung sai cua mot trong so chung: nhom
    do phai bi tu choi o buoc TIEN TE truoc do roi.
    """
    if len(cur) != 1:
        return DUNG_SAI_MAC_DINH
    return DUNG_SAI.get(next(iter(cur)), DUNG_SAI_MAC_DINH)


# ---- sau hinh dang ---------------------------------------------------------
GHEP_DUOC = ("A", "B", "C")
DAY_NGUOI = ("D", "E", "F")
TEN_HINH: dict[str, str] = {
    "A": "1 bank x 1 PM · Σ khop",
    "B": "1 bank x N PM · Σ khop (chia tien theo dong)",
    "C": "N bank x 1 PM · Σ khop (tra nhieu lan)",
    "D": "N bank x M PM · Σ khop — ⛔ KHONG DOAN: nhieu cach chia deu cong dung",
    "E": "tien te KHAC nhau — can ty gia, khong the cong",
    "F": "Σ lech qua dung sai (1.000 VND, QĐ-ITL-57)",
}
assert set(TEN_HINH) == set(GHEP_DUOC) | set(DAY_NGUOI)


@dataclass(frozen=True)
class Nhom:
    """Mot ma tham chieu, hai ben cua no, va phan xu."""
    ref: str
    bank: tuple[DongBank, ...]
    pm: tuple[DongPM, ...]
    hinh: str
    ly_do: str = ""

    @property
    def ghep_duoc(self) -> bool:
        return self.hinh in GHEP_DUOC

    def tong_bank(self) -> Decimal:
        return sum((b.tien for b in self.bank), Decimal(0))

    def tong_pm(self) -> Decimal:
        return sum((p.tien or Decimal(0) for p in self.pm), Decimal(0))


def _cur(xs: Iterable[str]) -> set[str]:
    return {x.strip().upper() for x in xs if x and x.strip()}


def xep_hinh(ref: str, bank: Sequence[DongBank], pm: Sequence[DongPM]) -> Nhom:
    """Phan loai mot ma. ⛔ Thu tu cac phep kiem la CO CHU Y.

    Tien te kiem TRUOC Σ: cong hai so khac don vi ra mot con so **trong hinh**
    nhung vo nghia, va neu no tinh co bang nhau thi ta vua ghep sai ma khong
    cong nao do. Do that: 199 dong thuoc lop nay.

    ★ Va thu tu do lai QUAN TRONG HON sau khi co dung sai: dung sai tra cuu
    THEO TIEN TE, nen nhom nhieu tien te phai bi loai o buoc truoc — neu khong
    thi ⛔ khong biet lay dung sai cua dong nao.
    """
    cb, cp = _cur(b.cur for b in bank), _cur(p.cur for p in pm)
    if cb and cp and not (cb & cp):
        return Nhom(ref, tuple(bank), tuple(pm), "E",
                    f"bank {'/'.join(sorted(cb))} vs PM {'/'.join(sorted(cp))}")
    tb = sum((b.tien for b in bank), Decimal(0))
    tp = sum((p.tien or Decimal(0) for p in pm), Decimal(0))
    ds = dung_sai_cua(cb | cp)
    if abs(tb - tp) > ds:
        return Nhom(ref, tuple(bank), tuple(pm), "F",
                    f"bank {tb} vs PM {tp} · lech {tb - tp}"
                    + (f" (dung sai {ds})" if ds else ""))
    nb, np_ = len(bank), len(pm)
    if nb == 1 and np_ == 1:
        return Nhom(ref, tuple(bank), tuple(pm), "A")
    if nb == 1:
        return Nhom(ref, tuple(bank), tuple(pm), "B")
    if np_ == 1:
        return Nhom(ref, tuple(bank), tuple(pm), "C")
    return Nhom(ref, tuple(bank), tuple(pm), "D",
                f"{nb} dong bank x {np_} dong PM — nhieu cach chia deu cong dung")


def chia_tien(tong: Decimal, phan: Sequence[Decimal]) -> list[Decimal]:
    """Chia `tong` theo ty le `phan`. ⛔ Tong cac phan chia PHAI bang `tong` KHIT.

    ⚠ Chia theo ty le roi lam tron tung phan thi **mat vai dong le**, va mat tien
    le trong mot he ke toan la loi khong the giai thich. Nen: lam tron tung phan
    roi **don du vao phan LON NHAT** — phan lon nhat de sai so tuong doi nho
    nhat, va phep chon **on dinh** (chay lai cho y het).
    """
    if not phan:
        raise ValueError("khong co phan nao de chia")
    tong_phan = sum(phan, Decimal(0))
    if tong_phan == 0:
        raise ValueError("tong ty le bang 0 — khong chia duoc, ⛔ khong chia deu")
    ra = [(tong * p / tong_phan).quantize(Decimal("0.01")) for p in phan]
    du = tong - sum(ra, Decimal(0))
    if du:
        i = max(range(len(phan)), key=lambda k: (phan[k], -k))
        ra[i] += du
    if sum(ra, Decimal(0)) != tong:
        raise AssertionError(f"chia tien lech: {sum(ra, Decimal(0))} != {tong}")
    return ra


@dataclass
class ThongKeGhep:
    """Do duoc, va ⛔ khong gop thanh MOT con so (spec §3 ⑦)."""
    dong_bank: int = 0
    khong_co_ma: int = 0
    khong_thay_ma_PM: int = 0
    theo_hinh: dict[str, int] = field(default_factory=dict)
    dong_theo_hinh: dict[str, int] = field(default_factory=dict)

    def ghep_duoc(self) -> int:
        return sum(v for k, v in self.dong_theo_hinh.items() if k in GHEP_DUOC)

    def day_nguoi(self) -> int:
        return sum(v for k, v in self.dong_theo_hinh.items() if k in DAY_NGUOI)

    def can(self) -> bool:
        return (self.ghep_duoc() + self.day_nguoi()
                + self.khong_co_ma + self.khong_thay_ma_PM) == self.dong_bank

    def bao(self) -> str:
        h = " · ".join(f"{k} {self.dong_theo_hinh[k]}"
                       for k in sorted(self.dong_theo_hinh))
        return (f"bank {self.dong_bank} = ghep {self.ghep_duoc()} + day nguoi "
                f"{self.day_nguoi()} + khong co ma {self.khong_co_ma} + khong "
                f"thay ma PM {self.khong_thay_ma_PM}   [{h}]")


def xep_ca_lat(bank: Sequence[DongBank], pm: Sequence[DongPM]
               ) -> tuple[list[Nhom], ThongKeGhep]:
    """Xep ca lat. ⛔ Bon duong khong can thi NO, khong tra ket qua mot nua."""
    pm_theo_ref: dict[str, list[DongPM]] = {}
    for p in pm:
        if p.ref:
            pm_theo_ref.setdefault(p.ref, []).append(p)

    bk_theo_ref: dict[str, list[DongBank]] = {}
    tk = ThongKeGhep(dong_bank=len(bank))
    for b in bank:
        if not b.ref:
            tk.khong_co_ma += 1
        elif b.ref not in pm_theo_ref:
            tk.khong_thay_ma_PM += 1
        else:
            bk_theo_ref.setdefault(b.ref, []).append(b)

    nhom: list[Nhom] = []
    for ref in sorted(bk_theo_ref):                 # sap xep => chay lai y het
        bs = bk_theo_ref[ref]
        n = xep_hinh(ref, bs, pm_theo_ref[ref])
        nhom.append(n)
        tk.theo_hinh[n.hinh] = tk.theo_hinh.get(n.hinh, 0) + 1
        tk.dong_theo_hinh[n.hinh] = tk.dong_theo_hinh.get(n.hinh, 0) + len(bs)
    if not tk.can():
        raise AssertionError("bon duong khong can: " + tk.bao())
    return nhom, tk


def moi_noi(n: Nhom) -> list[tuple[int, str, Decimal]]:
    """Nhom ghep duoc -> danh sach `(dong_bank, line_id, tien)`.

    ⛔ Nhom KHONG ghep duoc thi NO — de goi sai cho thi vo hinh.

    Hinh `B` (1 bank × N PM) la cho DUY NHAT phai chia tien: mot lan chuyen tra
    nhieu dong lenh. Hinh `C` (N bank × 1 PM) ⛔ khong chia gi — moi dong bank
    mang **so tien cua chinh no**, va ca N dong deu tro ve MOT `line_id`. Do la
    tra nhieu lan, khong phai chia.
    """
    if not n.ghep_duoc:
        raise ValueError(f"nhom hinh {n.hinh} khong ghep duoc: {n.ly_do}")
    if n.hinh == "B":
        b = n.bank[0]
        phan = [p.tien or Decimal(0) for p in n.pm]
        return [(b.dong_sheet, p.line, t)
                for p, t in zip(n.pm, chia_tien(b.tien, phan))]
    line = n.pm[0].line
    return [(b.dong_sheet, line, b.tien) for b in n.bank]


def kiem_tieu_de_pm(hang: Sequence[Any]) -> None:
    """④ Nguon PM doi cot thi NO TO — so tung VI TRI, ⛔ khong so long tay."""
    thay = ["" if x is None else str(x).replace("\n", " ").strip() for x in hang]
    lech = [(i, mong, thay[i] if i < len(thay) else "(thieu cot)")
            for i, mong in sorted(PM_TIEU_DE_MONG_DOI.items())
            if i >= len(thay) or thay[i] != mong]
    if lech:
        raise NguonPMDoiHinhDang(
            f"{len(lech)} cot PM lech tieu de: " + " · ".join(
                f"vi tri {i}: mong {a!r} thay {b!r}" for i, a, b in lech[:5]))
