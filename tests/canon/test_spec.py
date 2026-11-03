from collections import Counter

from fls.canon.spec import CANON_36, CANON_COLS, letter_of, pos_of


def test_38_vi_tri_va_36_truong():
    """Nhin thi 38 vi tri (A..AL) nhung chi 36 truong — Z, AA trong.
    Dem sai la lech mapping toan bo khuon (DD-I01 khuyet tat 3)."""
    assert len(CANON_COLS) == 38
    assert len(CANON_36) == 36
    trong = [c.letter for c in CANON_COLS if not c.name]
    assert trong == ["Z", "AA"]


def test_vi_tri_lien_tuc_tu_0():
    assert [c.pos for c in CANON_COLS] == list(range(38))


def test_chu_cai_dung_khuon_bang_tinh():
    assert letter_of(0) == "A" and letter_of(25) == "Z"
    assert letter_of(26) == "AA" and letter_of(37) == "AL"
    assert pos_of("A") == 0 and pos_of("V") == 21 and pos_of("AL") == 37


def test_bon_cot_AH_AK_trung_ten_van_phan_biet_duoc_theo_vi_tri():
    """Khuyet tat 1: 4 cot ten y het nhau => KHONG the tham chieu theo ten."""
    trung = [c for c in CANON_COLS if c.name == "MID I DoubleCheck LE"]
    assert len(trung) == 4
    assert [c.letter for c in trung] == ["AH", "AI", "AJ", "AK"]
    assert len({c.pos for c in trung}) == 4


def test_W_X_va_AB_AC_trung_ten_nhung_khac_nguon():
    """Khuyet tat 2: cung ten, khac nguon (PE vs PI). Tron nham = sai ky P&L."""
    ten = "Thời điểm bắt đầu sử dụng dịch vụ"
    same = [c for c in CANON_COLS if c.name == ten]
    assert [c.letter for c in same] == ["W", "AB"]
    assert {c.source for c in same} == {"[Importrange]PE_Unpivot",
                                        "[Importrange]PI_Unpivot"}


def test_bay_cot_BASE_dung_thu_tu():
    assert [c.name for c in CANON_COLS[:7]] == [
        "Ngày chứng từ", "Số chứng từ", "Diễn giải", "Đơn vị tiền tệ",
        "PS Nợ", "PS Có", "Tài khoản"]


def test_lineage_PM_song_sot():
    """INV-I05 + QD-ITL-20/CR#1: AS-IS vut ID PMLine o chang 8."""
    ten = {c.name for c in CANON_COLS}
    assert {"ID PMLine", "ID PMSlip", "Pháp nhân thanh toán"} <= ten


def test_nhom_dem_dung_DD_I01():
    """7 BASE + 15 (H-V) + 3 (W-Y) + 5 (AB-AF) + 6 (AG-AL) = 36."""
    c = Counter(x.group for x in CANON_36)
    assert sum(c.values()) == 36
    assert c["BASE"] == 7
