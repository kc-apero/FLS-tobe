"""Unit test cua luat khoi. Doi soat tren du lieu THAT o test_parity_2026_03.py."""

import pytest

from fls.ledger.final_rule import (
    BAY_KHOI,
    CO_INPUT_HERE,
    KHONG_TRA_LOI,
    MAC_DINH_THEO_KHOI,
    NAM_KHOI,
    dung_khoi,
    may_khong_tra_loi,
    tinh_final,
    tinh_mid,
)


def test_nam_khoi_hop_dong_va_bay_khoi_cua_so():
    assert [a for a, _ in NAM_KHOI] == [
        "hd", "pay_type", "cdt1", "svc_start", "svc_end"]
    assert [a for a, _ in BAY_KHOI][5:] == ["id_payee", "invoice"]
    assert all(b == a + "_thyt" for a, b in BAY_KHOI)


def test_mac_dinh_khai_du_bay_khoi():
    assert set(MAC_DINH_THEO_KHOI) == {a for a, _ in BAY_KHOI}


def test_mac_dinh_MOI_KHOI_MOT_HANG_khong_dung_chung():
    """★★ Do tren 9.219 dong. Tai lieu DD-I06 doc cong thuc khoi 1 roi suy rong
    ra ca bay khoi — sai, va cong parity that da bat (khoi 7 lech 521/584)."""
    co = {k: v for k, v in MAC_DINH_THEO_KHOI.items() if v}
    assert len(set(co.values())) == len(co)
    assert MAC_DINH_THEO_KHOI["hd"] == "OGA | GAC - Other"
    assert MAC_DINH_THEO_KHOI["pay_type"] == "Thanh toán (Regular)"
    assert MAC_DINH_THEO_KHOI["cdt1"] == "SHQ2 | Headquarters2"
    assert MAC_DINH_THEO_KHOI["id_payee"] == "VD0"
    assert MAC_DINH_THEO_KHOI["invoice"] == "Nợ hoá đơn"


def test_hai_khoi_dich_vu_CHUA_suy_duoc_mac_dinh():
    """22 dong, gia tri khac nhau (202512 x8, 202508 x4, …) => KHONG phai hang.
    De None thay vi bia mot hang — GAP-ORA-06 (INV-I16)."""
    assert MAC_DINH_THEO_KHOI["svc_start"] is None
    assert MAC_DINH_THEO_KHOI["svc_end"] is None


# ── buoc 2: Final = f(Classifying, MID) ──────────────────────────────────────

def test_final_lay_classifying_khi_may_tra_loi_duoc():
    assert tinh_final("NB | Lưu chuyển nội bộ", "gi cung duoc") == "NB | Lưu chuyển nội bộ"


def test_final_lay_MID_khi_may_khong_tra_loi():
    assert tinh_final(KHONG_TRA_LOI, "SHQ2 | Headquarters2") == "SHQ2 | Headquarters2"
    assert tinh_final("", "VD0") == "VD0"
    assert tinh_final(None, "VD0") == "VD0"


def test_final_KHONG_phu_thuoc_Manual_input():
    """⛔ Doi so thu hai la MID. Gop hai buoc la lo da bi cong parity bat."""
    assert tinh_final(KHONG_TRA_LOI, None) is None
    assert tinh_final(KHONG_TRA_LOI, "") is None


def test_hang_dung_cua_cong_thuc():
    """Final chi co the khac Classifying khi Classifying rong/that bai."""
    for s in ("A", "B | C", "202410"):
        for u in ("", "khac han", None):
            assert tinh_final(s, u) == s


def test_may_khong_tra_loi():
    assert may_khong_tra_loi("") and may_khong_tra_loi(None)
    assert may_khong_tra_loi(KHONG_TRA_LOI)
    assert not may_khong_tra_loi("co gia tri")


# ── buoc 1: MID = f(Classifying, Manual, mac dinh) ───────────────────────────

def test_mid_lay_classifying_khi_khong_ai_go():
    assert tinh_mid("NB | Noi bo", "", "MD") == "NB | Noi bo"


def test_mid_thay_bang_MAC_DINH_khi_o_van_con_co():
    assert tinh_mid(KHONG_TRA_LOI, CO_INPUT_HERE, "OGA | GAC - Other") == "OGA | GAC - Other"


def test_mid_ton_trong_gia_tri_nguoi_go():
    assert tinh_mid(KHONG_TRA_LOI, "SHQ2 | Headquarters2", "MD") == "SHQ2 | Headquarters2"


def test_mid_khoi_chua_co_mac_dinh_thi_tra_None_khong_bia():
    assert tinh_mid(KHONG_TRA_LOI, CO_INPUT_HERE, None) is None


# ── ket hop + cho noi that ───────────────────────────────────────────────────

def test_che_do_oracle_dung_MID_cua_so():
    kq = dung_khoi("invoice", KHONG_TRA_LOI, CO_INPUT_HERE, mid="Nợ hoá đơn")
    assert kq.parity == "Nợ hoá đơn"
    assert kq.thyt is None and kq.may_tu_bia is True


def test_che_do_tu_sinh_suy_MID_theo_khoi():
    kq = dung_khoi("hd", KHONG_TRA_LOI, CO_INPUT_HERE)
    assert kq.parity == MAC_DINH_THEO_KHOI["hd"]
    assert kq.thyt is None and kq.may_tu_bia is True


def test_nguoi_go_thi_KHONG_cham_gia_tri_do():
    """AUD-12: thyt chi bien gia tri MAY TU BIA thanh None."""
    kq = dung_khoi("cdt1", KHONG_TRA_LOI, "SGO1 | Saigon", mid="SGO1 | Saigon")
    assert kq.parity == "SGO1 | Saigon" and kq.thyt == "SGO1 | Saigon"
    assert kq.may_tu_bia is False


def test_ca_hai_rong_thi_khong_bia_ra_gi():
    kq = dung_khoi("hd", "", "")
    assert kq.parity is None and kq.thyt is None and kq.may_tu_bia is False


def test_ten_khoi_la_thi_NO():
    with pytest.raises(ValueError, match="khong thuoc 7 khoi"):
        dung_khoi("khong_co_that", "a", "b")
