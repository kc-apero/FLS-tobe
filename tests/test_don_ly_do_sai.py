# -*- coding: utf-8 -*-
"""Phep thu cho `tools/don_ly_do_sai.py` — cong cu XOA VET.

⛔⛔ **Cai dang thu o day ⛔ khong phai phep xoa — no la phep TU CHOI xoa.**

Mot cong cu xoa chay dung thi ⛔ khong ai khen; mot cong cu xoa **nham** thi
xoa mat ly do lam viec cua ke toan, va ⛔ khong ai lay lai duoc tu man hinh.
⇒ Cac bai nay ghim **dieu kien no PHAI dung tay**.
"""
from __future__ import annotations

import inspect

from tools import don_ly_do_sai as d


def _m(co_vet=8387, so_dong=8387, s3=(100, 100), s2=(100, 100), tong=108128):
    return {"tong": tong, "nguoi": 0, "khac": 0, "co_vet": co_vet,
            "so_dong": so_dong, "s3": s3, "s2": s2}


def test_DU_chung_minh_khi_ca_ba_phep_do_dat():
    assert d.in_chung_minh(_m()) is True


def test_KHONG_du_khi_ly_do_CHUA_dan_het_moi_dong():
    """⭐⭐ **Bai quan trong nhat cua tep nay.**

    Neu chi **mot phan** so dong mang ly do thi do dung la hinh dang cua mot
    ly do **THEO DONG** — tuc cai ma ban vá `_ly_do_tung_dong` sinh ra, hay
    cai mot NGUOI go vao. Luc ay cong cu ⛔ **khong** phan biet duoc tung cai,
    nen no phai **tu choi ca cum**.

    ⛔ Neu ai do noi long dieu kien nay *("gan het cung duoc")*, bai do se do.
    """
    assert d.in_chung_minh(_m(co_vet=4000, so_dong=8387)) is False


def test_KHONG_du_khi_so_RONG():
    """⛔ So rong ⇒ `0/0` ⇒ ⛔ khong duoc coi la "100% khop"."""
    assert d.in_chung_minh(_m(co_vet=0, so_dong=0, s3=(0, 0), s2=(0, 0))) is False


def test_KHONG_du_khi_S3_co_dong_THAT_su_thieu_tien():
    """⛔ Chi mot dong `S3` dung thoi la nhan ay **⛔ khong con tu mau thuan**."""
    assert d.in_chung_minh(_m(s3=(99, 100))) is False


def test_phep_XOA_chan_tay_o_ACTOR_may_chu_khong_quet_ca_bang():
    """⛔⛔ Cau `DELETE` phai mang **ca hai** dieu kien.

    Thieu `actor` ⇒ no quet luon ly do NGUOI go vao; thieu `evt_type` ⇒ no
    quet luon `defer`/`unmatch`/`done` — tuc **lich su thao tac**.
    """
    ma = inspect.getsource(d.chay)
    assert "DELETE FROM fls_queue_event" in ma
    assert "evt_type='reason'" in ma
    assert "actor=%s" in ma


def test_LUU_VET_truoc_khi_xoa_va_HOAN_TAC_neu_so_lech():
    """⛔ Chep ra `sao_luu/` phai xay ra **truoc** cau `DELETE`, va so dong
    chep phai **bang** so dong xoa — lech thi `rollback`, ⛔ khong commit."""
    ma = inspect.getsource(d.chay)
    assert ma.index("luu_vet(") < ma.index("DELETE FROM"), \
        "⛔ luu vet PHAI dung truoc cau xoa"
    assert "rollback()" in ma and ma.index("rollback()") < ma.index("commit()")


def test_VN_chi_doi_dau_cua_CON_SO_chu_khong_cua_CAU_VAN():
    """⛔ Ghim dung loi toi mac 11/09: `.replace(",", ".")` tren **ca chuoi da
    ghep** an luon dau phay cua cau van quanh so."""
    assert d.vn(108128) == "108.128"
    cau = f"(`reason`, actor=x) : {d.vn(108128)}"
    assert "`reason`, actor=" in cau, "⛔ dau phay cua CAU VAN bi an mat"


def test_KHONG_mo_duong_GHI_o_buoc_DO():
    """⛔ Buoc do phai di qua `noi_chi_doc()` — kho tu tu choi moi phep ghi."""
    assert "noi_chi_doc(" in inspect.getsource(d.chay)
