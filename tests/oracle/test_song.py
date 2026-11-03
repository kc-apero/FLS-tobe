"""Cong tu kiem "ban sao con SONG khong" — G-ORA-LIVE-1/2/3.

Owner chot ban sao RAW la nguon (QD-ITL-50, nguyen van "y chang ban goc, song").
Luat du an: mot cam ket phai thanh thu MAY CHAN DUOC. Ba cong duoi day la cho do.
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from fls.oracle.song import (GHEP_MAX, GHEP_MIN, NGUONG_NGAY, DoDuoc, cong_1,
                             cong_2, cong_3, kiem_song, phai_dung)

HOM_NAY = date(2026, 8, 26)


def _do(**kw) -> DoDuoc:
    """Mac dinh = so DO THAT ngay 2026-08-26 tren ban sao RAW."""
    m = dict(ky_moi_nhat=date(2026, 8, 1),
             dong_theo_tab={"PM_Unpivot": 3704, "PE_Unpivot": 2638},
             o_loi_theo_tab={"PM_Unpivot": 0, "PE_Unpivot": 0},
             ty_le_ghep=0.335)
    m.update(kw)
    return DoDuoc(**m)


def test_do_that_hom_nay_thi_ba_cong_deu_xanh():
    kq = kiem_song(_do(), HOM_NAY)
    assert len(kq) == 3
    assert not phai_dung(kq), [k.ly_do for k in kq if k.do]


def test_cong_1_do_khi_so_khong_con_duoc_cap_nhat():
    # ban sao chet: IMPORTRANGE thoi chay nhung VAN tra gia tri cu
    k = cong_1(_do(ky_moi_nhat=date(2026, 5, 1)), HOM_NAY)
    assert k.do and "ngay" in k.ly_do


def test_cong_1_do_khi_khong_co_ky_nao():
    assert cong_1(_do(ky_moi_nhat=None), HOM_NAY).do


def test_cong_1_xanh_dung_o_ranh_45_ngay():
    assert not cong_1(_do(ky_moi_nhat=HOM_NAY - timedelta(days=NGUONG_NGAY)),
                      HOM_NAY).do
    assert cong_1(_do(ky_moi_nhat=HOM_NAY - timedelta(days=NGUONG_NGAY + 1)),
                  HOM_NAY).do


def test_cong_2_do_khi_mot_tab_nguon_rong():
    k = cong_2(_do(dong_theo_tab={"PM_Unpivot": 3704, "PE_Unpivot": 0}))
    assert k.do and "PE_Unpivot" in k.ly_do


def test_cong_2_do_khi_tab_toan_o_loi():
    k = cong_2(_do(o_loi_theo_tab={"PM_Unpivot": 3704, "PE_Unpivot": 0}))
    assert k.do and "PM_Unpivot" in k.ly_do


def test_cong_2_do_khi_khong_do_tab_nao():
    assert cong_2(_do(dong_theo_tab={})).do


@pytest.mark.parametrize("ty_le", [0.0, 0.10, 0.249, 0.451, 0.99, 1.0])
def test_cong_3_do_khi_ty_le_ghep_roi_ra_ngoai(ty_le):
    assert cong_3(_do(ty_le_ghep=ty_le)).do


@pytest.mark.parametrize("ty_le", [GHEP_MIN, 0.335, 0.338, GHEP_MAX])
def test_cong_3_xanh_trong_khoang(ty_le):
    assert not cong_3(_do(ty_le_ghep=ty_le)).do


def test_cong_3_do_khi_khong_do_duoc_ty_le():
    assert cong_3(_do(ty_le_ghep=None)).do


def test_moi_cong_do_deu_phai_co_ly_do_bang_chu():
    """ACC-4: khong cai gi bi chan ma khong co ly do CO TEN."""
    xau = _do(ky_moi_nhat=None, dong_theo_tab={}, ty_le_ghep=None)
    for k in kiem_song(xau, HOM_NAY):
        assert k.do and k.ly_do.strip() and k.ma.startswith("G-ORA-LIVE-")
