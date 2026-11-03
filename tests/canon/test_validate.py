from datetime import date

import pytest

from fls.canon.row import CanonRow
from fls.canon.validate import parse_ngay, parse_so, validate


def _row(**kw):
    v = [None] * 38
    v[0] = kw.get("ngay", date(2026, 1, 31))
    v[3] = kw.get("curr", "VND")
    v[4] = kw.get("no", 0)
    v[5] = kw.get("co", 1000)
    v[6] = kw.get("acct", "1121")
    return CanonRow.from_list(v)


def test_ngay_dang_chuoi_duoc_parse():
    """~5.369 dong nguon co ngay dang CHUOI (itl-ledge-text-dates-unmapped)."""
    assert parse_ngay("2026-01-31") == date(2026, 1, 31)
    assert parse_ngay("31/01/2026") == date(2026, 1, 31)
    assert parse_ngay(date(2026, 1, 31)) == date(2026, 1, 31)


def test_ngay_khong_doc_duoc_thi_bao_TEN_ly_do_khong_tra_None_am_tham():
    kq = validate(_row(ngay="ba muoi mot"))
    assert any("Ngày chứng từ" in x and "không đọc được" in x for x in kq.loai)


def test_thieu_ngay_la_LOAI_khong_phai_cho():
    """Khong co ngay thi khong biet ky — khong the treo o hang cho."""
    kq = validate(_row(ngay=None))
    assert kq.loai and not any("Ngày chứng từ" in c for c in kq.cho)


def test_no_va_co_cung_rong_la_LOAI():
    kq = validate(_row(no=None, co=None))
    assert any("PS Nợ" in x or "PS Có" in x for x in kq.loai)


def test_thieu_tai_khoan_la_CHO_khong_phai_loai():
    """Thieu thong tin phan loai => hang cho UNMAPPED, khong nem dong tien di."""
    kq = validate(_row(acct=None))
    assert not kq.loai and kq.cho


def test_moi_ly_do_loai_deu_co_ten_khong_duoc_rong():
    """ACC-4: ly do CO TEN."""
    for r in (_row(ngay=None), _row(no=None, co=None), _row(ngay="rac")):
        for x in validate(r).loai:
            assert x.strip() and len(x) > 8, x


def test_parse_so_chap_dinh_dang_ke_toan():
    assert parse_so("1.234.567") == 1234567
    assert parse_so("1,234,567.89") == 1234567.89
    assert parse_so("") is None and parse_so(None) is None


def test_parse_so_rac_thi_NO_khong_tra_0():
    """Tra 0 la cach lam bien mat tien trong im lang."""
    with pytest.raises(ValueError):
        parse_so("mot ty")


def test_ngay_hoan_ngay_thang_KHONG_duoc_tu_doan():
    """93% dong nguon bi hoan ngay<->thang (itl-date-daymonth-swap, ~181 ty sai ky).
    Dinh dang khong ro rang (ca hai phan <=12) PHAI khai bao thu tu, khong doan."""
    assert parse_ngay("31/01/2026") == date(2026, 1, 31)   # ro: 31 > 12
    with pytest.raises(ValueError, match="mo ho"):
        parse_ngay("03/01/2026")                           # mo ho: 3/1 hay 1/3?
    assert parse_ngay("03/01/2026", thu_tu="dmy") == date(2026, 1, 3)
    assert parse_ngay("03/01/2026", thu_tu="mdy") == date(2026, 3, 1)


def test_dong_hop_le_thi_khong_loai_khong_cho():
    kq = validate(_row())
    assert not kq.loai and not kq.cho and kq.sach()
