"""O loi cua Sheets — mot ban khai, va cai gia ma no vua dap."""
from __future__ import annotations

from fls.canon.o_loi import MA_LOI, la_o_loi, ma_loi_cua


def test_MA_LOI_THAT_duoc_nhan_ra():
    for v in ("#N/A", "#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#NULL!",
              "#NUM!", "#ERROR!", " #REF! "):
        assert la_o_loi(v), v


def test_N_A_dang_DAI_van_la_o_loi():
    """Sheets tra `#N/A` kem giai thich khi doc qua API."""
    assert la_o_loi("#N/A (Did not find value '' in VLOOKUP evaluation)")
    assert ma_loi_cua("#N/A (Did not find value '')") == "#N/A"


def test_NGUOI_GO_TAY_bat_dau_bang_thang_KHONG_phai_o_loi():
    """★★ Cai gia ma luat cu tra: lan nap THAT dau tien tren nguon day du.

        dong 20 · cot goc C ('Dien giai') la o loi: ##LAI NHAP VON#

    `##LAI NHAP VON#` la ke toan go tay. Luat cu `startswith("#")` nem **7 giao
    dich that** vao `fls_reject`, kem mot ly do SAI (*"o loi"*) — khong ai di tim
    mot cong thuc khong ton tai.
    """
    for v in ("##LAI NHAP VON#", "#LAI NHAP VON", "#1", "#tag", "# ghi chu",
              "#NAP VON#", "#N/AI KHONG PHAI LOI"):
        assert not la_o_loi(v), v
        assert ma_loi_cua(v) is None


def test_khong_phai_chuoi_thi_khong_phai_o_loi():
    for v in (None, 0, 1234.5, True, [], {}):
        assert not la_o_loi(v)


def test_tat_ca_ma_deu_bat_dau_bang_thang_va_khong_trung_tien_to():
    assert all(m.startswith("#") for m in MA_LOI)
    assert len(set(MA_LOI)) == len(MA_LOI)


def test_CHI_MOT_BAN_KHAI_trong_ca_he():
    """⛔ Bon ban sao mot luat la bon co hoi de chung lech nhau — va cai lech se
    im lang: dong bi loai o tang nay, duoc giu o tang kia.
    """
    import pathlib
    goc = pathlib.Path(__file__).resolve().parents[2]
    xau = []
    for f in list((goc / "fls").rglob("*.py")) + list((goc / "tools").rglob("*.py")):
        t = f.read_text(encoding="utf-8")
        if 'startswith("#")' in t and f.name != "o_loi.py":
            xau.append(str(f.relative_to(goc)))
    assert not xau, "con ban sao cua luat o loi: " + ", ".join(xau)
