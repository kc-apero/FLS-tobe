"""Vo boc cau tra loi. Bai quan trong nhat: ⛔ **tien ⛔ khong duoc thanh
`float`**."""
from __future__ import annotations

import datetime as dt
import json
from decimal import Decimal

import pytest

from fls.api import bao


def test_tien_ra_JSON_la_CHUOI_khong_phai_so_thap_phan():
    """Tien ra ngoai la CHUOI. `Decimal` giu nguyen tung chu so."""
    v = Decimal("1214000000000.55")
    ra = json.loads(bao.dong_goi({"tien": v}, bao.meta("thu")))
    assert ra["data"]["tien"] == "1214000000000.55"
    assert isinstance(ra["data"]["tien"], str)


def test_do_KHOANG_CACH_den_cho_float_bat_dau_mat_chu_so():
    """⚠ **Bai nay do khoang cach an toan, ⛔ khong to cao mot loi dang song.**

    Toi da tung viet o day rang *"so 1.214 ty lam float mat mot phan xu"*. **Do
    la sai** — bai chinh no bat: `float(Decimal("1214000000000.55"))` ve nguyen
    ven. `float` giu ~15-17 chu so co nghia, va 1.214 ty kem hai so le moi la
    **15** chu so.

    Cho mat that su bat dau khoang **17 chu so**. Bai nay ghim ca hai moc de
    nguoi sau biet **con cach bao xa**, chu khong phai de tin rang so hien nay
    dang sai:

        1.214.000.000.000,55  (15 chu so) → float ve NGUYEN VEN
        1.214.567.890.123.456,55 (17)     → float MAT chu so cuoi

    ⇒ Ly do thuc de tra ve CHUOI van vung: JSON ⛔ khong noi kieu, nen may doc
    (JavaScript o `P6`) bien moi so thanh `float64` **truoc khi ai kip chon**.
    Tra chuoi la cach duy nhat cua doc ⛔ khong giao pho quyet dinh do cho may
    khac. ⭐ Va vi khoang cach hien la ~1.000 lan, day la **hang rao dat truoc**,
    khong phai vet vao.
    """
    an_toan = Decimal("1214000000000.55")            # ~ tong so that
    assert str(float(an_toan)) == str(an_toan), "moc an toan da doi"

    mat = Decimal("1214567890123456.55")             # 17 chu so
    assert str(float(mat)) != str(mat)
    assert json.loads(bao.dong_goi({"t": mat}, bao.meta("x")))["data"]["t"] \
        == "1214567890123456.55"


def test_ngay_ra_ISO():
    ra = json.loads(bao.dong_goi(
        {"d": dt.date(2026, 8, 27),
         "t": dt.datetime(2026, 8, 27, 10, 30, tzinfo=dt.timezone.utc)},
        bao.meta("thu")))
    assert ra["data"]["d"] == "2026-08-27"
    assert ra["data"]["t"].startswith("2026-08-27T10:30")


def test_kieu_la_thi_NO_khong_thanh_chuoi_bua():
    """⛔ `default=str` la cach mot doi tuong bien thanh `<object at 0x...>` ma
    van ra duoc JSON."""
    class La:
        pass

    with pytest.raises(TypeError, match="khong biet dua"):
        bao.dong_goi({"x": La()}, bao.meta("thu"))


def test_vo_boc_du_ba_phan():
    ra = json.loads(bao.dong_goi([1, 2], bao.meta("thu")))
    assert set(ra) == {"data", "error", "meta"}
    assert ra["error"] is None
    assert set(ra["meta"]) >= {"request_id", "pham_vi", "as_of", "data_status"}


def test_mac_dinh_la_flash_KHONG_phai_da_doi_soat():
    """`INV-I14`: so chua chot luon mang co. ⛔ Mac dinh `reconciled` la khoac
    nhan da-doi-soat cho con so chua ai doi soat."""
    assert bao.meta("thu").data_status == "flash"


def test_trang_thai_la_thi_NO():
    with pytest.raises(ValueError, match="data_status"):
        bao.meta("thu", data_status="xong_roi")


def test_ma_loi_chua_khai_thi_NO():
    with pytest.raises(KeyError, match="chua khai"):
        bao.dong_goi_loi("FLS-TU-NGHI-RA", bao.meta("thu"))


@pytest.mark.parametrize("ma,http", [
    ("FLS-UNAUTHORIZED", 401), ("FLS-NOT-FOUND", 404),
    ("FLS-BAD-REQUEST", 400), ("FLS-METHOD", 405),
    ("FLS-CONFLICT-SOURCE", 409), ("FLS-DQ-FAILED", 422),
    ("FLS-ACCR-UNREADABLE", 503), ("FLS-INTERNAL", 500),
])
def test_ma_loi_dung_ma_HTTP_theo_BA_07(ma, http):
    got, than = bao.dong_goi_loi(ma, bao.meta("thu"))
    assert got == http
    assert json.loads(than)["error"]["code"] == ma


def test_than_loi_khong_co_data():
    _h, than = bao.dong_goi_loi("FLS-NOT-FOUND", bao.meta("thu"))
    assert json.loads(than)["data"] is None
