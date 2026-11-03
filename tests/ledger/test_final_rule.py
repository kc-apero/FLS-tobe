from fls.ledger.final_rule import (
    CO_INPUT_HERE,
    KHONG_TRA_LOI,
    MAC_DINH_CUNG,
    NAM_KHOI,
    tinh_final,
)


def test_dung_nam_khoi():
    assert len(NAM_KHOI) == 5
    assert [a for a, _ in NAM_KHOI] == [
        "hd", "pay_type", "cdt1", "svc_start", "svc_end"]
    assert all(b == a + "_thyt" for a, b in NAM_KHOI)


def test_may_tra_loi_duoc_thi_dung_ket_qua_may():
    kq = tinh_final("NB | Lưu chuyển nội bộ", "")
    assert kq.parity == "NB | Lưu chuyển nội bộ"
    assert kq.thyt == "NB | Lưu chuyển nội bộ"
    assert kq.may_tu_bia is False


def test_may_khong_tra_loi_va_nguoi_da_go_thi_dung_cua_nguoi():
    kq = tinh_final(KHONG_TRA_LOI, "SHQ2 | Headquarters2")
    assert kq.parity == "SHQ2 | Headquarters2"
    assert kq.thyt == "SHQ2 | Headquarters2", "AUD-12: KHONG duoc cham gia tri nguoi go"
    assert kq.may_tu_bia is False


def test_o_van_con_co_Input_here_thi_parity_mang_mac_dinh_NHUNG_thyt_la_None():
    """★ Cho nay la ca thiet ke: vua khop so 100%, vua khong noi doi."""
    kq = tinh_final(KHONG_TRA_LOI, CO_INPUT_HERE)
    assert kq.parity == MAC_DINH_CUNG, "phai khop so cu tung o (QD-ITL-35)"
    assert kq.thyt is None, "may tu bia => KHONG vao parity that"
    assert kq.may_tu_bia is True


def test_classifying_rong_va_khong_ai_go_thi_may_tu_bia():
    kq = tinh_final("", CO_INPUT_HERE)
    assert kq.parity == MAC_DINH_CUNG and kq.thyt is None and kq.may_tu_bia


def test_ca_hai_rong_thi_khong_bia_ra_gi_ca():
    """INV-I16: khong suy duoc thi de trong TUONG MINH, khong gan mac dinh."""
    kq = tinh_final("", "")
    assert kq.parity is None and kq.thyt is None
    assert kq.may_tu_bia is False


def test_final_khong_bao_gio_khac_classifying_khi_classifying_co_gia_tri():
    """Hang dung cua cong thuc (DD-I06), khong phai phat hien thuc nghiem."""
    for s in ("A", "B | C", "202410"):
        for t in ("", "gi cung duoc", CO_INPUT_HERE):
            assert tinh_final(s, t).parity == s


def test_None_xu_nhu_rong():
    assert tinh_final(None, None).parity is None
    assert tinh_final(None, "nguoi go").parity == "nguoi go"


def test_khoang_trang_hai_ben_khong_lam_doi_nhanh():
    assert tinh_final("  " + KHONG_TRA_LOI + " ", CO_INPUT_HERE).parity == MAC_DINH_CUNG
