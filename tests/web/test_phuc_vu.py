"""Bang tep: cong hai chieu + ⛔ khong co cho cho loi vuot thu muc.

★ Cung khuon `tests/api/test_bang_tuyen.py`: bang khai mot lan thi cong quet
duoc bang, ⛔ khong phai doc ma nguon de doan.
"""
from __future__ import annotations

import pytest

from tests.web.than_sinh import than_sinh

from fls.web import phuc_vu as pv


# ── cong cua chinh bang ────────────────────────────────────────────────────
def test_bang_tep_that_khong_vi_pham():
    assert pv.kiem_bang_tep() == []


def test_moi_tep_tren_dia_deu_duoc_khai():
    """⛔ Chieu nguoc — mot tep ⛔ khong ai khai la mot tep ⛔ khong ai biet."""
    khai = {t.ten for t in pv.BANG_TEP if not t.sinh} | pv.KHONG_PHUC_VU
    import os
    tren_dia = {n for n in os.listdir(pv.THU_MUC)
                if os.path.isfile(os.path.join(pv.THU_MUC, n))}
    assert tren_dia == khai


# ── ⛔⛔ PHA CO CHU DICH: cong phai DO ─────────────────────────────────────
# `Luat so 1`: cong chua tung thay do la cong chua biet co song.

def test_cong_DO_khi_bang_khai_tep_khong_co_that():
    loi = pv.kiem_bang_tep(bang=pv.BANG_TEP + (
        pv.Tep("/ma.js", "tep_khong_ton_tai.js", mo_ta="tep ma"),))
    assert any("tep_khong_ton_tai.js" in x for x in loi)


def test_cong_DO_khi_co_tep_tren_dia_ma_khong_ai_khai(tmp_path):
    (tmp_path / "index.html").write_text("x", encoding="utf-8")
    (tmp_path / "len_lut.js").write_text("x", encoding="utf-8")
    loi = pv.kiem_bang_tep(
        bang=(pv.Tep("/", "index.html", mo_ta="vo"),), thu_muc=str(tmp_path))
    assert any("len_lut.js" in x for x in loi)


def test_cong_DO_khi_mot_tep_tinh_dam_vao_vung_cua():
    """⛔ Mot tep tinh nam duoi `/api/` se gia lam mot cau tra loi that."""
    loi = pv.kiem_bang_tep(bang=pv.BANG_TEP + (
        pv.Tep("/api/fls/v1/gates", "index.html", mo_ta="gia mao"),))
    assert any("dam vao vung cua" in x for x in loi)


def test_cong_DO_khi_trung_duong():
    loi = pv.kiem_bang_tep(bang=pv.BANG_TEP + (
        pv.Tep("/tokens.css", "tokens.css", mo_ta="ban sao"),))
    assert any("trung duong" in x for x in loi)


def test_cong_DO_khi_thieu_mo_ta():
    loi = pv.kiem_bang_tep(bang=pv.BANG_TEP + (
        pv.Tep("/x.js", "ung_dung.js"),))
    assert any("khong co mo ta" in x for x in loi)


def test_cong_DO_khi_duoi_la():
    with pytest.raises(KeyError):
        pv.Tep("/x.svg", "x.svg", mo_ta="svg chay duoc script").kieu


def test_lam_nguoi_phuc_vu_NO_khi_bang_hong(monkeypatch):
    monkeypatch.setattr(pv, "BANG_TEP", pv.BANG_TEP + (
        pv.Tep("/ma.js", "khong_co_that.js", mo_ta="tep ma"),))
    with pytest.raises(RuntimeError, match="bang tep vi pham"):
        pv.lam_nguoi_phuc_vu(than_sinh=than_sinh())


# ── ⭐⭐ loi vuot thu muc ⛔ KHONG CO CHO DE TON TAI ────────────────────────
@pytest.mark.parametrize("duong", [
    "/../pyproject.toml",
    "/../../etc/passwd",
    "/%2e%2e/pyproject.toml",
    "/..%2fpyproject.toml",
    "/./../.importlinter",
    "//etc/passwd",
    "/tep/../../fls/db/kho.py",
    "/TOKENS.CSS",          # ⚠ Windows ⛔ khong phan biet hoa thuong —
    "/tokens.css/",         #   mot phep ghep duong se mo ca hai dang nay
    "/index.html%00.txt",
    "/phien.js/../tokens.css",
])
def test_khong_duong_la_nao_ra_duoc_mot_byte(duong):
    p = pv.lam_nguoi_phuc_vu({"the": "bi-mat"}, than_sinh=than_sinh())
    assert p(duong) is None


def test_duong_that_thi_ra_duoc():
    p = pv.lam_nguoi_phuc_vu({"the": "abc"}, than_sinh=than_sinh())
    kieu, than = p("/")
    assert kieu.startswith("text/html")
    assert b"<title>FLS" in than
    kieu, than = p("/tokens.css")
    assert kieu.startswith("text/css")
    assert b"--ink" in than


def test_phien_js_sinh_trong_bo_nho_va_cho_the():
    p = pv.lam_nguoi_phuc_vu({"the": "the-cua-toi", "actor": "lan@apero.vn"}, than_sinh=than_sinh())
    kieu, than = p("/phien.js")
    assert kieu.startswith("text/javascript")
    assert b"the-cua-toi" in than
    assert b"lan@apero.vn" in than


def test_phien_js_KHONG_nam_tren_dia():
    """⛔ Mot cai the tren dia se bi commit, bi sao luu, bi gui di."""
    import os
    assert not os.path.exists(os.path.join(pv.THU_MUC, "phien.js"))


def test_ten_nguoi_co_dau_nhay_khong_lam_vo_tep_phien():
    """⛔ Mot dau nhay trong ten nguoi ⛔ khong duoc cat doi tep `phien.js`."""
    import json

    goc = {"actor": 'a"b\'c</script>', "the": "t\\n"}
    p = pv.lam_nguoi_phuc_vu(goc, than_sinh=than_sinh())
    _, than = p("/phien.js")
    chu = than.decode("utf-8")
    # ⭐ Phep kiem THAT: cat lay phan JSON roi doc NGUOC lai. Neu phep thoat
    # sai o bat cu dau, `json.loads` NO — chac chan hon la dem dau nhay.
    tho = chu.split("window.FLS_PHIEN = ", 1)[1].rsplit(";", 1)[0]
    assert json.loads(tho) == goc
