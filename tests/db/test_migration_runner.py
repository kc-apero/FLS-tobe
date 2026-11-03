"""Cong: moi thay doi schema phai co duong di tru, va duong do phai TOI DUNG cho.

Boi canh: pg_migrate ban dau chi biet CREATE TABLE IF NOT EXISTS. Bang da co
thi lenh bo qua trong im lang => them FK/cot moi khong bao gio duoc ap, ma
runner van in "thanh cong". Da gap that 26/08 (GAP-DB-P0-02).
"""

from fls.db.migration_runner import MIGRATIONS, checksum_of, discover


def test_co_it_nhat_migration_baseline():
    assert MIGRATIONS, "phai co it nhat 0001_baseline"
    assert MIGRATIONS[0].version == 1
    assert "baseline" in MIGRATIONS[0].name


def test_so_thu_tu_tang_don_khong_trung_khong_ho():
    ver = [m.version for m in MIGRATIONS]
    assert ver == sorted(ver), "phai xep theo so thu tu"
    assert len(set(ver)) == len(ver), "trung so thu tu"
    assert ver == list(range(1, len(ver) + 1)), f"ho so thu tu: {ver}"


def test_checksum_on_dinh():
    """Cung noi dung => cung checksum. Day la co so cua cong bat-sua-lich-su."""
    a = checksum_of(MIGRATIONS[0].sql)
    b = checksum_of(MIGRATIONS[0].sql)
    assert a == b and len(a) == 64


def test_checksum_doi_khi_noi_dung_doi():
    assert checksum_of("a") != checksum_of("a ")


def test_discover_doc_dung_thu_muc_migrations():
    assert [m.version for m in discover()] == [m.version for m in MIGRATIONS]


def test_baseline_co_du_cot_thyt_va_canon():
    """QD-ITL-35: 5 cot *_thyt + canon PHAI co trong migration DAU TIEN."""
    sql = MIGRATIONS[0].sql
    for c in ("hd_thyt", "pay_type_thyt", "cdt1_thyt",
              "svc_start_thyt", "svc_end_thyt", "canon"):
        assert c in sql, f"{c} khong co trong migration dau tien"
