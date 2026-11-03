"""Khai bao nguon la DU LIEU va co cong khoa — de khong ai doi am tham."""
from __future__ import annotations

from fls.canon.spec import CANON_COLS, pos_of
from fls.oracle import nguon as N


def test_hai_nguon_dung_dia_chi_owner_da_chot():
    assert N.BAN_SAO_RAW.spreadsheet_id == (
        "1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E")
    assert N.BAN_SAO_RAW.sheet == "Transaction Mapping L1"
    assert N.BAN_SAO_RAW.dong_dau == 5          # KHONG phai 4 — dong 4 TRONG
    assert N.SO_GOC_ADJUSTED.spreadsheet_id == (
        "1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA")
    assert N.SO_GOC_ADJUSTED.sheet == "ITL Ledge"
    assert N.SO_GOC_ADJUSTED.dong_dau == 10


def test_bon_thu_tuyet_doi_khong_mo_deu_co_ly_do_bang_chu():
    assert len(N.CAM_MO) >= 4
    for ma, ly_do in N.CAM_MO.items():
        assert ly_do.strip(), ma


def test_ban_sao_ADJUSTED_ngoai_kiem_soat_van_bi_cam():
    assert "1Pqg_G81xQKKP-tyR8IFFcnaimT2oZ22e-Tq_mewxbN0" in N.CAM_MO


def test_nguon_dang_dung_KHONG_nam_trong_danh_sach_cam():
    assert N.BAN_SAO_RAW.spreadsheet_id not in N.CAM_MO
    assert N.SO_GOC_ADJUSTED.spreadsheet_id not in N.CAM_MO


def test_R_ORA_07c_hai_cot_rong_co_y_la_Z_va_AA():
    assert N.COT_RONG_CO_Y == {pos_of("Z"), pos_of("AA")}
    for p in N.COT_RONG_CO_Y:
        assert CANON_COLS[p].name == ""      # dong bo voi khuon canon


def test_R_ORA_07d_cam_dat_nguong_tren_W_va_X():
    """W/X `#N/A` 100% la trang thai DUNG (QD-ITL-51) -> cam dat nguong o day."""
    assert N.CAM_DAT_NGUONG == {pos_of("W"), pos_of("X")}


def test_ba_tap_cot_phu_kin_38_vi_tri_va_khong_chong_nhau():
    ba = (N.COT_LOI_LA_LOI_THAT, N.COT_DUOC_PHEP_NA, N.COT_RONG_CO_Y)
    assert sum(len(x) for x in ba) == 38            # phu kin
    assert len(set().union(*ba)) == 38              # khong chong nhau


def test_cot_BASE_la_cot_o_loi_dem_loi_that():
    for c in CANON_COLS[:7]:
        assert c.pos in N.COT_LOI_LA_LOI_THAT, c.name


def test_khoa_ghep_svc_phan_biet_duong_lenh_chi_va_duong_hoa_don():
    """QD-ITL-51: W/X va AB/AC KHAC nhau o KHOA, khong o bang tra."""
    assert N.KHOA_SVC[pos_of("W")] == pos_of("P")     # ID PELine
    assert N.KHOA_SVC[pos_of("X")] == pos_of("P")
    assert N.KHOA_SVC[pos_of("AB")] == pos_of("R")    # ID PILine
    assert N.KHOA_SVC[pos_of("AC")] == pos_of("R")


def test_ca_bon_cot_svc_deu_tra_CUNG_MOT_bang():
    """Bang hoc duoc tu QD-ITL-51: khac biet la KHOA, ⛔ khong phai bang tra.

    Neu ai sua BANG_TRA_SVC thanh hai bang khac nhau thi test nay do —
    do dung la suy luan sai ma may do da mac ngay 26/08.
    """
    assert len(set(N.BANG_TRA_SVC.values())) == 1
    assert set(N.BANG_TRA_SVC) == {pos_of(c) for c in ("W", "X", "AB", "AC")}
