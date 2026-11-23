# -*- coding: utf-8 -*-
"""`B1` — BA LUAT DOC cua man GAN LENH CHI, va ca ba deu **CHUA TUNG duoc viet**.

⭐⭐⭐ `QĐ-ITL-148` · `2026-09-21`. Chang `B1` cua `Plan-Test-Dev-Man-Ghep.md`:
**bai thu DO truoc, ma sau**. Ba luat duoi day nam trong `BA-07 §4h ⓶ ⓷ ⓸`.

⛔⛔ **Vi sao ca ba deu nguy hiem hon ve ngoai cua chung:**

    ⓐ TACH NGUON — *moi tai lieu cua du an dang trich SAI gia tri that*.
       Kho co tien to **`R | `** o **`8.387/8.387`** dong; `BA-06`, hop dong
       thiet ke va brief deu trich **thieu** no. ⇒ Mot phep tach chep theo
       tai lieu **hong ngay ky tu dau**.

    ⓑ CHIEU No/Co — du an **da doc nham cot nay mot lan** *(lay dau tu
       `pay_type` thay vi cot No/Co)*. `3.691/8.387` dong mang **ca hai** o,
       nen mot phep doc ngay tho se gap ca nhap nhang o **44%** cuon so —
       ⭐ nhung **`0`** dong co ca hai khac `0`, nen luat that la mot dong.

    ⓒ SE-RI → NGAY — chon sai goc lech **4 nam 1 ngay**, va ⛔ khong o nao
       tren man noi cho biet da chon goc nao. Goc duoc **DO**, ⛔ khong chon:

           goc 1900 ⇒ 2025-03-10 … 2026-08-29 · lech trung vi **3** ngay
           goc 1904 ⇒ 2029-03-11 … 2030-08-30 · lech trung vi **1.462** ngay

       ⭐ Phep kiem dung mot nguon **DOC LAP** — ngay cua dong tien **da noi**
         (`fls_itl.doc_date`) — ⛔ khong phai mot dai ngay *"trong hop ly"*.
         Dai ngay mot minh ⛔ khong du: mot goc sai voi do lech nho hon thi
         mat ⛔ khong bat duoc.
"""
from __future__ import annotations

import datetime as dt

import pytest

from fls.repo import man_ghep


# ── ⓐ tach `source_sheet` ────────────────────────────────────────────────

def test_tach_nguon_BOC_tien_to_R():
    """⛔ Gia tri THAT mang `R | ` — do `8.387/8.387` dong ngay `21/09`."""
    r = man_ghep.tach_nguon("R | PO2_OCBC USD_SGO2")
    assert r == {"tk": "PO2", "bank": "OCBC", "curr": "USD", "le": "SGO2"}, (
        "⛔ tien to `R | ` (ten tang sheet nguon) chua duoc boc ⇒ so tai khoan "
        "se ra `R | PO2`. Moi tai lieu cua du an dang trich gia tri NAY THIEU "
        "tien to, nen mot phep tach chep theo tai lieu hong ngay ky tu dau.")


def test_tach_nguon_ca_so_tai_khoan_dai():
    r = man_ghep.tach_nguon("R | 358468128_VPB VND_VGOH")
    assert r == {"tk": "358468128", "bank": "VPB", "curr": "VND", "le": "VGOH"}


def test_tach_nguon_KHONG_dung_khuon_thi_NO_chu_KHONG_doan():
    """⛔ `INV-I16` — may ⛔ khong duoc bia mot cau tra loi cho chuoi la."""
    with pytest.raises(ValueError):
        man_ghep.tach_nguon("R | mot_chuoi khong dung khuon")


# ── ⓐ' che so tai khoan ──────────────────────────────────────────────────

def test_che_tai_khoan_toan_chu_so_thi_rut_4_so_cuoi():
    assert man_ghep.che_tai_khoan("358468128") == "••8128"


def test_che_tai_khoan_KHONG_phai_so_thi_GIU_NGUYEN():
    """⭐ `6` tai khoan THE ⛔ khong phai so: PO1·PO2·PO3·PO5·PO6·PO9.

    ⛔ Luat *"4 so cuoi"* ap mu quang cho ra `••PO2` — vua **vo nghia** vua
       **⛔ khong che duoc gi** (no in nguyen ca ma).
    """
    for ma in ("PO1", "PO2", "PO3", "PO5", "PO6", "PO9"):
        assert man_ghep.che_tai_khoan(ma) == ma, (
            f"⛔ `{ma}` la tai khoan THE, ⛔ khong phai so tai khoan ⇒ ⛔ khong "
            "duoc cat 4 ky tu cuoi")


# ── ⓑ chieu No/Co ────────────────────────────────────────────────────────

@pytest.mark.parametrize("ps_no,ps_co,mong", [
    (1000, None, "no"),      # 829 dong chi co No
    (None, 1000, "co"),      # 3.867 dong chi co Co
    (0, 1000, "co"),         # 3.189 dong: o No = 0
    (1000, 0, "no"),         # 502 dong: o Co = 0
])
def test_chieu_lay_tu_o_KHAC_0(ps_no, ps_co, mong):
    """⭐ `3.691/8.387` dong mang **ca hai** o — nhung **`0`** dong ca hai khac `0`.

    ⇒ Luat: **ben nao ≠ 0 thi do la chieu**. `No` = tien VAO · `Co` = tien RA.
    """
    assert man_ghep.chieu_tien(ps_no, ps_co) == mong


def test_chieu_ca_hai_KHAC_0_thi_NO_chu_KHONG_chon_bua():
    """⛔ Do duoc `0` dong nhu vay. Neu no XAY RA thi do la du lieu HONG,
    va may ⛔ khong duoc chon giup mot ben *(`INV-I16`)*."""
    with pytest.raises(ValueError):
        man_ghep.chieu_tien(500, 700)


def test_chieu_KHONG_duoc_suy_tu_pay_type():
    """⛔⛔ Bai GHIM — du an **da doc nham cot nay mot lan**.

    ⭐⭐ **Bai nay do MA CHAY, ⛔ khong do van xuoi.** Ban dau toi quet ca
       `inspect.getsource()` va no **DO** ngay — vi chinh khoi chu thich
       *giai thich vi sao ⛔ khong dung `pay_type`* co chua chu ay. Mot phep
       do bat ca **loi canh bao ve loi** thi no ⛔ khong do cai no tuong.

    ⇒ Quet **doi tuong ma** (`co_names` + `co_consts`, de quy) — do dung thu
      se chay, va no van bat duoc ca truong hop doc `d["pay_type"]`.
    """
    import types

    def _ten(co) -> set[str]:
        ra = set(co.co_names) | {c for c in co.co_consts if isinstance(c, str)}
        for c in co.co_consts:
            if isinstance(c, types.CodeType):
                ra |= _ten(c)
        return ra

    dung = {n for n in _ten(man_ghep.chieu_tien.__code__) if "pay_type" in n}
    assert not dung, (
        f"⛔ `chieu_tien` cham toi {dung} — dung duong da dan toi loi dau tien "
        "mot lan roi. Chieu lay tu o No/Co khac 0.")


# ── ⓒ se-ri Excel → ngay ────────────────────────────────────────────────

def test_se_ri_doi_ngay_dung_GOC_1900():
    """⭐ Goc duoc **DO** bang mot nguon DOC LAP, ⛔ khong chon theo cam giac.

    `45726.759012696755` la o `Timestamp` NHO NHAT trong anh PM hieu luc.
    """
    d = man_ghep.ngay_tu_seri("45726.759012696755")
    assert d.date() == dt.date(2025, 3, 10), (
        f"⛔ ra {d.date()} — goc `1904` cho `2029-03-11` (lech 4 nam 1 ngay) "
        "va lech trung vi `1.462` ngay so voi ngay dong tien da noi; goc "
        "`1900` lech trung vi **3** ngay")


def test_se_ri_giu_ca_GIO():
    """⛔ `0,759012...` ngay = ~18:13. Cat mat gio la mat thu tu trong ngay."""
    d = man_ghep.ngay_tu_seri("45726.759012696755")
    assert (d.hour, d.minute) == (18, 12), (d.hour, d.minute)


def test_se_ri_dai_ngay_cua_KHO_nam_trong_khoang_hop_ly():
    """⭐ Hai dau cua anh PM hieu luc — `3.772` dong."""
    assert man_ghep.ngay_tu_seri("45726.6951").date() == dt.date(2025, 3, 10)
    assert man_ghep.ngay_tu_seri("46263.8918").date() == dt.date(2026, 8, 29)


def test_se_ri_KHONG_phai_so_thi_NO():
    """⛔ *"⛔ chua doc duoc"* ⛔ khong duoc bien thanh mot ngay nao do."""
    with pytest.raises(ValueError):
        man_ghep.ngay_tu_seri("18/09/2026")
