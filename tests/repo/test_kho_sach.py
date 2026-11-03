"""Cong kho-sach: kho THAT chi duoc chua dong cua lan nap THAT.

Phan xu la HAM THUAN nen test duoc khong can DB — va do la co y: mot cong ma
chi kiem duoc bang cach co san mot kho ban thi khong ai kiem no.
"""
from __future__ import annotations

import pytest

from fls.repo import kho_sach
from fls.repo.kho_sach import (BANG_CO_RUN, DemBang, danh_gia,
                                la_run_that)


# ------------------------------------------------------------------ ban trang
@pytest.mark.parametrize("run", [
    "NAP-2026-08-27-RAW",
    "NAP-2024-01-01-BANK",
    "NAP-2026-12-31-P100",
])
def test_hinh_run_that_duoc_nhan(run):
    assert la_run_that(run)


@pytest.mark.parametrize("run", [
    "T-007c4ed7",                # dau test da tung lan vao so
    "r1",                        # 919 dong trong so that 27/08
    None,
    "",
    "nap-2026-08-27-raw",        # chu thuong
    "NAP-2026-8-27-RAW",         # thieu so 0
    "NAP-2026-08-27",            # thieu nguon
    "NAP-2026-08-27-RAW-THEM",   # duoi la
])
def test_moi_thu_khac_KHONG_phai_run_that(run):
    assert not la_run_that(run)


def test_ban_TRANG_khong_phai_ban_DEN():
    """⛔ Mot tien to test MOI phai bi bat ngay, khong can ai them vao danh sach.

    Neu luat la ban DEN (*loai `T-%` va `r1` ra*) thi lan sau ai dat tien to
    khac la no lot — va lot trong im lang.
    """
    assert not la_run_that("X-moi-toanh-chua-ai-biet")


# ------------------------------------------------------------------ phan xu
def _du(itl_run, reject_run=(), run_run=()):
    return [
        DemBang("fls_itl", tuple(itl_run)),
        DemBang("fls_reject", tuple(reject_run)),
        DemBang("fls_run", tuple(run_run)),
    ]


def test_kho_sach_thi_DAT():
    px = danh_gia(_du(
        [("NAP-2026-08-27-RAW", 9973)],
        [("NAP-2026-08-27-RAW", 19)],
        [("NAP-2026-08-27-RAW", 1)],
    ))
    assert px.dat, px.bao()
    assert "fls_itl=9973" in " ".join(px.da_do)


def test_dau_test_trong_so_thi_DO_va_noi_dung_so_luong():
    px = danh_gia(_du(
        [("NAP-2026-08-27-RAW", 9973), ("r1", 919), ("T-abc", 285)],
        [("NAP-2026-08-27-RAW", 19), ("T-abc", 106)],
        [("NAP-2026-08-27-RAW", 1), ("T-abc", 228)],
    ))
    assert not px.dat
    assert any("1204" in x for x in px.ly_do), px.ly_do
    assert any("106" in x for x in px.ly_do)


def test_KHONG_DO_DUOC_GI_thi_KHONG_PHAI_SACH():
    """⛔ Cong chung #7: kho rong ⇒ DO, ⛔ khong phai 'khong thay loi nen xanh'."""
    px = danh_gia(_du([], [], []))
    assert not px.dat
    assert any("khong do duoc" in x or "chua do duoc gi" in x for x in px.ly_do), px.ly_do


def test_duoi_nguong_thi_DO_du_moi_run_deu_that():
    px = danh_gia(_du([("NAP-2026-08-27-RAW", 12)], [], []))
    assert not px.dat
    assert any("nguong" in x for x in px.ly_do), px.ly_do


def test_thieu_MOT_BANG_thi_DO_khong_duoc_noi_ca_kho():
    """Thieu mot bang mang `run_id` la mot cho khong ai canh."""
    px = danh_gia([DemBang("fls_itl", (("NAP-2026-08-27-RAW", 9973),))])
    assert not px.dat
    assert any("chua soi bang" in x for x in px.ly_do), px.ly_do


def test_BANG_CO_RUN_du_ba_bang():
    """Khoa danh sach: them bang mang `run_id` ma quen khai o day = lo im lang."""
    assert BANG_CO_RUN == ("fls_itl", "fls_reject", "fls_run")


def test_bao_noi_ro_da_do_duoc_gi():
    px = danh_gia(_du([("NAP-2026-08-27-RAW", 9973)],
                      [("NAP-2026-08-27-RAW", 19)],
                      [("NAP-2026-08-27-RAW", 1)]))
    bao = px.bao()
    assert "da do:" in bao and "fls_itl=9973" in bao


# ── ⭐ ngay trong `run_id` (them 27/08 cung voi cua doc `P4`) ─────────────
def test_ngay_vo_ly_bi_BAT_du_hinh_dang_dung():
    """⛔⛔ Vi sao cong nay ra doi cung ngay voi cua doc.

    Cua doc loc pham vi bang **HINH DANG** `run_id` (mot cau SQL `~` khong goi
    duoc ham Python), nen moi bai test can thay dong cua minh qua pham vi
    *"chi lan nap that"* deu phai dat mot `run_id` HINH DANG THAT. Tu day tro
    di, **ban trang hinh dang mot minh la MU**: dau test se trong y nhu lan nap
    that, va cong `kiem_kho` mat dung kha nang no sinh ra de co.

    ⇒ Them phep kiem NGAY, chi o tang cong (Python). Bo test dung nam **2000**.
    """
    run = "NAP-2000-01-01-THU"
    assert kho_sach.la_run_that(run) is True, "hinh dang phai qua (pham vi doc)"
    assert kho_sach.ngay_hop_ly(run) is False, "ngay phai KHONG qua (cong kho)"

    px = kho_sach.danh_gia([
        kho_sach.DemBang(bang=b, theo_run=((run, 5000),))
        for b in kho_sach.BANG_CO_RUN])
    assert px.dat is False
    assert any("NGAY vo ly" in x for x in px.ly_do), px.ly_do


def test_ngay_that_thi_qua():
    for run in ("NAP-2024-10-21-RAW", "NAP-2026-08-27-RAW"):
        assert kho_sach.ngay_hop_ly(run) is True, run


def test_ngay_tuong_lai_xa_bi_BAT():
    import datetime as dt
    assert kho_sach.ngay_hop_ly("NAP-2099-01-01-RAW") is False
    mai = dt.date.today() + dt.timedelta(days=1)
    assert kho_sach.ngay_hop_ly(f"NAP-{mai.isoformat()}-RAW") is True


def test_run_khong_dung_hinh_dang_thi_ngay_cung_khong_doc_duoc():
    assert kho_sach.ngay_cua_run("T-abc12345") is None
    assert kho_sach.ngay_hop_ly("T-abc12345") is False
