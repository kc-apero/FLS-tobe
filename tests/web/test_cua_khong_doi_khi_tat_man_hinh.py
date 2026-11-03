"""⛔ Bat man hinh ⛔ KHONG duoc lam yeu cua `P4`/`P5` mot chut nao.

⛔⛔ **Vi sao bai nay ton tai.** `B2` cham vao `fls/api/cua.py` — tep da qua ra
soat cua `P4` va dang cho **so tien that**. Moi lan cham vao mot tep nhu the,
cau hoi ⛔ khong phai *"cai moi co chay khong"* ma la ***"cai cu co con y het
khong"***. Bai nay ghim cau tra loi do.
"""
from __future__ import annotations

import pytest

from fls.api import cua


# ── ⓐ mac dinh la TAT ─────────────────────────────────────────────────────
def test_mac_dinh_khong_phuc_vu_tep_nao():
    import inspect

    ts = inspect.signature(cua.dung_may).parameters["phuc_vu_tep"]
    assert ts.default is None, "⛔ man hinh phai TAT mac dinh"


def test_may_tat_man_hinh_thi_thuoc_tinh_la_None():
    import inspect

    tt = inspect.signature(cua._May.__init__).parameters["phuc_vu_tep"]
    assert tt.default is None


# ── ⓑ ⭐⭐ vung cua bat kha xam pham ───────────────────────────────────────
@pytest.mark.parametrize("duong", [
    "/api/fls/v1",
    "/api/fls/v1/",
    "/api/fls/v1/gates",
    "/api/fls/v1/ledger/12",
    "/api/fls/v1/queue/9/match",
])
def test_moi_duong_cua_deu_nam_trong_vung_cam(duong):
    assert cua._trong_vung_cua(duong.rstrip("/") or duong)


@pytest.mark.parametrize("duong", [
    "/", "/index.html", "/tokens.css", "/phien.js",
    "/api", "/api/fls", "/api/fls/v2/gates", "/api/fls/v1x/gates",
])
def test_duong_ngoai_vung_cua_thi_tep_tinh_duoc_phuc_vu(duong):
    assert not cua._trong_vung_cua(duong)


def test_moi_tuyen_that_deu_duoc_vung_cam_che_kin():
    """⛔ Chieu chac chan nhat: duyet CHINH bang tuyen, ⛔ khong go tay lai."""
    for t in cua.bang_tuyen.BANG_TUYEN:
        assert cua._trong_vung_cua(t.duong), (
            f"⛔ {t.duong} nam NGOAI vung cam ⇒ mot tep tinh co the chiem cho no")


# ── ⓒ ⭐ fail-closed: ⛔ khong mo man hinh ra mang ─────────────────────────
@pytest.mark.parametrize("dia_chi", ["127.0.0.1", "::1", "localhost"])
def test_loopback_thi_cho_phuc_vu(dia_chi):
    cua.kiem_phuc_vu_tep(dia_chi)          # ⛔ khong duoc nem


@pytest.mark.parametrize("dia_chi", [
    "0.0.0.0", "", "192.168.1.10", "10.0.0.5", "::",
    "127.0.0.2",          # ⚠ van la loopback ky thuat, nhung ⛔ khong trong
                          #   ban TRANG ⇒ TU CHOI. Ban trang thi thua con hon
                          #   thieu: mot dia chi lot qua la mot the phat ra
                          #   ngoai.
])
def test_ngoai_loopback_thi_TU_CHOI(dia_chi):
    with pytest.raises(RuntimeError, match="GAP-WEB-01"):
        cua.kiem_phuc_vu_tep(dia_chi)


def test_dung_may_TU_CHOI_khi_vua_mo_man_hinh_vua_nghe_ra_mang(monkeypatch):
    monkeypatch.setenv("FLS_JWT_SECRET", "k" * 40)
    with pytest.raises(RuntimeError, match="GAP-WEB-01"):
        cua.dung_may(lambda: None, cong=0, dia_chi="0.0.0.0",
                     phuc_vu_tep=lambda d: None)


# ── ⭐⭐ ⓓ MAT NHAT KY ⛔ KHONG DUOC LAM CHET CUA ──────────────────────────
#
# ⛔⛔ **Day la mot su co THAT, ⛔ khong phai mot gia dinh.** `03/09` may dang
# chay bi mat dau ra *(phien nen ket thuc, dau kia cua ong dan dong lai)*: moi
# yeu cau vao lam `log_message` **no `BrokenPipeError`** truoc khi kip tra loi
# ⇒ cong **VAN MO** nen `netstat` bao `LISTENING` va nhin nhu dang song, ma ⛔
# khong tra loi gi. Owner bao *"toi khong mo duoc"*.
#
# ★ Do la lop hong te nhat: **im lang, va trong nhu binh thuong**. Mat nhat ky
#   la mat mot lop kiem soat; mat cau tra loi la mat ca cai cua.
class _DauRaDaDong:
    """Gia lap dau ra da bi dong — moi phep ghi deu NO."""

    def write(self, _):
        raise BrokenPipeError(32, "dau kia da dong")

    def flush(self):
        raise BrokenPipeError(32, "dau kia da dong")


class _TayTron:
    """Chi muon `log_message` — ⛔ khong dung ca may HTTP cho mot phep kiem nho."""
    log_message = cua._Tay.log_message


@pytest.mark.parametrize("loi", [
    BrokenPipeError(32, "dau kia da dong"),
    ValueError("I/O operation on closed file"),
    OSError(9, "Bad file descriptor"),
])
def test_ghi_nhat_ky_hong_thi_KHONG_nem_ra_ngoai(monkeypatch, loi):
    class _No:
        def write(self, _):
            raise loi

    monkeypatch.setattr(cua.sys, "stderr", _No())
    # ⛔ Khong duoc nem: neu nem thi cua chet truoc khi kip tra loi.
    _TayTron().log_message("%s %s", "GET", "/api/fls/v1/gates")


def test_dau_ra_dong_thi_cua_VAN_TRA_LOI(monkeypatch):
    """⭐ Phep kiem that su: sau khi dau ra chet, `log_message` van chay xong."""
    monkeypatch.setattr(cua.sys, "stderr", _DauRaDaDong())
    for _ in range(3):
        _TayTron().log_message("200 %s %s actor=%s", "GET", "/", "lan@apero.vn")


def test_cong_DO_neu_ai_do_go_lop_chua_ra(monkeypatch):
    """⛔ Cong chua tung thay do la cong chua biet co song.

    Neu `log_message` quay ve dang `sys.stderr.write(...)` tran thi bai nay bat
    duoc — no chung minh cai loi VAN nem khi ⛔ khong co lop chua.
    """
    import sys as _sys

    def _tran(self, dinh_dang, *doi_so):
        _sys.stderr.write("fls-api %s\n" % (dinh_dang % doi_so))

    monkeypatch.setattr(cua.sys, "stderr", _DauRaDaDong())
    with pytest.raises(BrokenPipeError):
        _tran(None, "%s", "x")


def test_loi_KHAC_van_phai_noi(monkeypatch):
    """⚠ ⛔ Khong nuot MOI loi — chi loi cua duong ghi nhat ky."""
    class _La:
        def write(self, _):
            raise KeyboardInterrupt

    monkeypatch.setattr(cua.sys, "stderr", _La())
    with pytest.raises(KeyboardInterrupt):
        _TayTron().log_message("%s", "x")
