"""Phep kiem THE. ⛔ Moi bai o day la mot duong tan cong CU THE, khong phai
mot bai "hanh phuc".

Tu viet phep kiem JWT la mot quyet dinh co gia. Gia phai tra la bo bai nay:
neu mot trong cac bai duoi bien thanh xanh vi ly do sai (vd co ai "noi rong cho
de dung") thi cua doc mo toang.
"""
from __future__ import annotations

import base64
import json
import time

import pytest

from fls.api import the

K = b"khoa-thu-dai-hon-ba-muoi-hai-ky-tu-cho-du"


def _the(than: dict, dau: dict | None = None, k: bytes = K) -> str:
    return the.dong_the(than, k, dau)


def _than_song(**them) -> dict:
    return {"sub": "ke.toan@apero.vn", "exp": int(time.time()) + 300, **them}


# ── duong song ────────────────────────────────────────────────────────────
def test_the_hop_le_tra_ve_actor_LAY_TU_THE():
    n = the.kiem(_the(_than_song(vai=["ke_toan"])), K)
    assert n.actor == "ke.toan@apero.vn"
    assert n.vai == ("ke_toan",)


def test_boc_the_tu_de_Bearer():
    t = _the(_than_song())
    assert the.tu_dau_de(f"Bearer {t}") == t
    assert the.tu_dau_de(f"bearer  {t}") == t


# ── ⓐ doi thuat toan ──────────────────────────────────────────────────────
def test_alg_none_bi_tu_choi():
    """⛔ Bay co dien: the tu khai "khong ky" roi khong mang chu ky."""
    dau = base64.urlsafe_b64encode(
        json.dumps({"alg": "none", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    than = base64.urlsafe_b64encode(
        json.dumps(_than_song()).encode()).rstrip(b"=").decode()
    with pytest.raises(the.TheKhongHopLe) as e:
        the.kiem(f"{dau}.{than}.", K)
    assert "alg" in e.value.chi_tiet


def test_doi_sang_thuat_toan_khac_bi_tu_choi():
    """⛔ `HS512` ky bang cung khoa van bi tu choi: ban TRANG mot phan tu."""
    with pytest.raises(the.TheKhongHopLe):
        the.kiem(_the(_than_song(), dau={"alg": "HS512", "typ": "JWT"}), K)


def test_thieu_alg_bi_tu_choi():
    with pytest.raises(the.TheKhongHopLe):
        the.kiem(_the(_than_song(), dau={"typ": "JWT"}), K)


# ── ⓑ chu ky ──────────────────────────────────────────────────────────────
def test_sua_than_lam_chu_ky_khong_khop():
    t = _the(_than_song())
    dau, than, ky = t.split(".")
    than_gia = base64.urlsafe_b64encode(
        json.dumps({**_than_song(), "sub": "giam.doc@apero.vn"}).encode()
    ).rstrip(b"=").decode()
    with pytest.raises(the.TheKhongHopLe) as e:
        the.kiem(f"{dau}.{than_gia}.{ky}", K)
    assert "chu ky" in e.value.chi_tiet


def test_khoa_khac_thi_tu_choi():
    with pytest.raises(the.TheKhongHopLe):
        the.kiem(_the(_than_song(), k=b"x" * 40), K)


# ── ⓒ han ─────────────────────────────────────────────────────────────────
def test_the_het_han_bi_tu_choi():
    with pytest.raises(the.TheKhongHopLe) as e:
        the.kiem(_the({"sub": "a@b.c", "exp": int(time.time()) - 1}), K)
    assert "het han" in e.value.chi_tiet


def test_the_KHONG_CO_HAN_bi_tu_choi():
    """⛔ Thieu `exp` ⛔ khong duoc coi la "khong han" — the ro la ro vinh vien."""
    with pytest.raises(the.TheKhongHopLe) as e:
        the.kiem(_the({"sub": "a@b.c"}), K)
    assert "exp" in e.value.chi_tiet


def test_exp_la_chuoi_bi_tu_choi():
    with pytest.raises(the.TheKhongHopLe):
        the.kiem(_the({"sub": "a@b.c", "exp": "9999999999"}), K)


def test_nbf_tuong_lai_bi_tu_choi():
    with pytest.raises(the.TheKhongHopLe):
        the.kiem(_the({**_than_song(), "nbf": int(time.time()) + 60}), K)


# ── nhat ky vo nghia neu khong biet ai ────────────────────────────────────
def test_thieu_sub_bi_tu_choi():
    with pytest.raises(the.TheKhongHopLe) as e:
        the.kiem(_the({"exp": int(time.time()) + 60}), K)
    assert "sub" in e.value.chi_tiet


def test_sub_rong_bi_tu_choi():
    with pytest.raises(the.TheKhongHopLe):
        the.kiem(_the({"sub": "   ", "exp": int(time.time()) + 60}), K)


# ── hinh dang ─────────────────────────────────────────────────────────────
@pytest.mark.parametrize("t", ["", "a", "a.b", "a.b.c.d", "..", "x" * 9000])
def test_hinh_dang_la_bi_tu_choi(t):
    with pytest.raises(the.TheKhongHopLe):
        the.kiem(t, K)


@pytest.mark.parametrize("de", [None, "", "Basic abc", "Bearer", "abc"])
def test_de_Authorization_sai_bi_tu_choi(de):
    with pytest.raises(the.TheKhongHopLe):
        the.tu_dau_de(de)


# ── ⛔ khong co chia khoa thi khong mo cua ────────────────────────────────
def test_thieu_bien_khoa_thi_NO(monkeypatch):
    monkeypatch.delenv(the.BIEN_KHOA, raising=False)
    with pytest.raises(RuntimeError, match="thieu FLS_JWT_SECRET"):
        the.khoa()


def test_khoa_ngan_thi_NO(monkeypatch):
    """⛔ Khoa ngan la khoa do duoc — tu choi luon, khong canh bao roi chay."""
    monkeypatch.setenv(the.BIEN_KHOA, "ngan")
    with pytest.raises(RuntimeError, match="32"):
        the.khoa()


def test_khoa_du_dai_thi_nhan(monkeypatch):
    monkeypatch.setenv(the.BIEN_KHOA, "k" * 32)
    assert the.khoa() == b"k" * 32


# ── ly do chi tiet ⛔ khong ra ngoai ──────────────────────────────────────
def test_thong_bao_ra_ngoai_KHONG_noi_sai_o_dau():
    """Noi cho nguoi go the biet ho sai o dau la giup ho do the.

    `str(e)` la thu di ra HTTP; `chi_tiet` la thu vao log noi bo.
    """
    with pytest.raises(the.TheKhongHopLe) as e:
        the.kiem(_the({"sub": "a@b.c", "exp": int(time.time()) - 1}), K)
    assert str(e.value) == "the khong hop le"
    assert "het han" in e.value.chi_tiet and "het han" not in str(e.value)
