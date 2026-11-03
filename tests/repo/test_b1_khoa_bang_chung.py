# -*- coding: utf-8 -*-
"""`B1` — ⭐⭐ Khoa BANG CHUNG: to cai gi trong dien giai sao ke.

⭐ Dien giai la **bang chung duy nhat** cua `4.145/8.387` = **49%** cuon so
  *(nhanh nuoc ngoai, `DT-I13 ⓑ`)*. Hop dong `§6` doi to **ba** thu: so
  chung tu **chi khi trung dung**, so tien **khi khop tuyet doi**, va ten
  ben nhan — sau khi loc **tu rac** de ⛔ khong to nhieu.

⛔⛔ **Bo tu rac la mot LUAT NGHIEP VU, ⛔ khong phai meo hien thi.** De no o
   JS thi ⛔ khong mot bai thu Python nao cham toi, va no se lech voi moi
   phep doi chieu khac cua he.
"""
from __future__ import annotations

from fls.repo import man_ghep as mg

#: ⚠ Ten ben nhan CO Y giu nguyen dang phap nhan *(`INC.`)* vi day chinh la
#: thu bai thu do — **⛔ khong** phai mot ho so nhan su.
LENH = {"ma_lenh": "PM1-1", "so_tien": "1000.00", "curr": "USD",
        "so_chung_tu": "1026946429", "nguoi_nhan": "SENSORTOWER, INC."}
UV = {"itl_id": 42, "doc_no": "1026946429", "amount": "1000.00",
      "curr": "USD", "dien_giai": "SENSORTOWER INC 1026946429 1000.00"}


def _k(**doi):
    return mg.khoa_bang_chung(dict(LENH), dict(UV, **doi))


# ── ⓐ ⭐ SO CHUNG TU — chi to khi TRUNG DUNG ────────────────────────────

def test_so_chung_tu_CHI_to_khi_TRUNG_DUNG():
    """⛔⛔ To mot so chung tu **⛔ khong** trung la noi doi bang mau: mau nen
    o day nghia la *"day dung la khoan cua ban"*."""
    assert "1026946429" in _k()
    assert "1026946429" not in _k(doc_no="9999999999")
    assert "1026946429" not in _k(doc_no=None)


# ── ⓑ ⭐ SO TIEN — chi to khi khop TUYET DOI ───────────────────────────

def test_so_tien_CHI_to_khi_khop_TUYET_DOI():
    assert "1000.00" in _k()
    assert "1000.00" not in _k(amount="987.60"), "⛔ lech tien ma van to"
    assert "1000.00" not in _k(curr="VND"), (
        "⛔⛔ **Cung con so, KHAC don vi tien** — to len la noi rang chung "
        "khop, va do la cach nhanh nhat de mot ke toan gan nham ca tien te")


# ── ⓒ ⭐⭐ TU RAC ───────────────────────────────────────────────────────

def test_TU_RAC_bi_loai_khoi_ten_ben_nhan():
    """⛔⛔ ⛔ Khong loc thi `INC` to **moi** dong co chu `inc` — va luc ay
    mau danh dau **thoi mang nghia**."""
    k = _k()
    assert "SENSORTOWER" in k
    for rac in ("INC", "inc", "COMPANY", "TNHH"):
        assert rac not in k, f"⛔ `{rac}` la tu rac ma van lot vao khoa"


def test_TU_RAC_loc_KHONG_phan_biet_hoa_thuong():
    """⚠ CO Y cat ca so CT lan so tien *(`doc_no=None`, `amount` lech)* de bai
    nay do **dung mot thu**: phep loc tu rac. Mot bai do ba thu cung luc thi
    khi no do, ⛔ khong ai biet thu nao hong."""
    l = dict(LENH, nguoi_nhan="Cong Ty TNHH ABCDEF")
    k = mg.khoa_bang_chung(l, dict(UV, doc_no=None, amount="1.00"))
    assert k == ["ABCDEF"], k


def test_tu_NGAN_hon_BA_ky_tu_bi_loai():
    """⭐ Mot chuoi `2` ky tu se to **rai rac khap** moi dien giai."""
    l = dict(LENH, nguoi_nhan="AB CD SENSORTOWER")
    k = mg.khoa_bang_chung(l, dict(UV))
    assert all(len(x) >= 3 for x in k), k


# ── ⓓ ⭐⭐⭐ THU TU: DAI TRUOC — de `<mark>` ⛔ khong LONG nhau ──────────

def test_khoa_xep_DAI_TRUOC():
    """⛔⛔ To `1026946429` roi to tiep `102` nam **ben trong** no se ra
    `<mark>` **long nhau** va HTML vo. ⇒ Quet **mot luot** bang mot regex
    hop nhat, va thu tu dai-truoc bao dam **mieng dai thang**."""
    k = _k()
    assert k == sorted(k, key=len, reverse=True), k


def test_KHONG_khoa_TRUNG_nhau():
    l = dict(LENH, nguoi_nhan="SENSORTOWER sensortower SENSORTOWER")
    k = mg.khoa_bang_chung(l, dict(UV))
    assert len(k) == len(set(x.lower() for x in k)), k


# ── ⓔ ⭐ Ca RONG ───────────────────────────────────────────────────────

def test_lenh_KHONG_co_gi_de_to_thi_tra_DANH_SACH_RONG():
    l = {"ma_lenh": "PM1-1", "so_tien": None, "curr": None,
         "so_chung_tu": None, "nguoi_nhan": None}
    assert mg.khoa_bang_chung(l, dict(UV)) == []


def test_so_tien_HONG_khong_lam_NO():
    """⛔ `curr` tung co gia tri `20` *(mot o bi lech cot)* — mot phep doi so
    that bai o day ⛔ khong duoc lam sap ca man."""
    assert mg.khoa_bang_chung(dict(LENH, so_tien="hai muc"), dict(UV)) is not None
    assert mg.khoa_bang_chung(dict(LENH), dict(UV, amount=None)) is not None
