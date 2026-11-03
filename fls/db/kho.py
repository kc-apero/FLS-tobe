"""MOT cho khai duy nhat: co HAI kho, va bo test ⛔ khong cham kho THAT.

⛔⛔ **Vi sao co file nay.** Nam file test PG lay MAC DINH dung dia chi kho
that (`os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")`).
Bien moi truong co the tro di noi khac, nhung **khong gi bat buoc** — nen mot
lenh `pytest` tron ghi thang vao so. Do duoc 2026-08-27:

    fls_itl   : 9.973 dong THAT + **1.204 dong dau test**  (11.177 tong)
    fls_reject:    19 dong THAT + **  106 dong dau test**
    fls_run   :     1 lan nap THAT + **227 lan chay test** (229 tong)
    hang cho  : 7.625 dong THAT + **  194 dong dau test**

★ Con so trong moi tai lieu **van dung**, vi chung duoc tinh CO LOC theo lan
nap. Cho hong la **khong gi bat buoc phai loc**. Va chang ke tiep (`P4` cua
doc, `P6` man hinh `F01`) doc dung bang nay ⇒ **man hinh dau tien ke toan
nhin thay se co 194 dong bia trong danh sach viec phai lam**.

⛔ Tien bia trong kho: **1.285.475.949** nam canh 1.214 ty tien that.

**Ba muc thiet ke:**

1. `dsn_test()` **NO** neu ket qua tro vao ten kho THAT. Test khong the cham
   kho that **du co ai dat sai bien moi truong** — day la chan cung, khong
   phai loi khuyen.
2. Test nao that su can doc kho THAT (`test_pg_verify` soi kho khop ban khai)
   thi mo bang `noi_chi_doc()`: PostgreSQL **tu tu choi** moi phep ghi
   (`default_transaction_read_only`). ⇒ ⛔ Khong dua vao ky luat cua nguoi viet
   test, dua vao tang duoi.
3. Ten kho khai **o day va chi o day**. Doi ten kho phai sua mot cho.

⚠ ⛔ File nay ⛔ KHONG duoc xoa dong nao khoi `fls_itl` — `INV-I08` append-only.
Don dau test la viec cua **dung lai kho** (DDL: drop/create database), ⛔ khong
phai cua mot cau `DELETE` len so.
"""
from __future__ import annotations

import os
import urllib.parse
from typing import Any

TEN_THAT = "fls"
TEN_TEST = "fls_test"

_MAC_DINH_THAT = "postgresql://fls:fls@localhost:5433/fls"

BIEN_THAT = "PG_DSN"
BIEN_TEST = "PG_DSN_TEST"


def ten_kho(dsn: str) -> str:
    """Ten kho (database) trong mot DSN. Rong neu DSN khong noi."""
    return urllib.parse.urlparse(dsn).path.lstrip("/")


def doi_ten_kho(dsn: str, ten: str) -> str:
    p = urllib.parse.urlparse(dsn)
    return urllib.parse.urlunparse(p._replace(path="/" + ten))


def dsn_that() -> str:
    """Kho THAT — noi so that nam. ⛔ Chi cong cu nap that va cong duoc dung."""
    return os.environ.get(BIEN_THAT) or _MAC_DINH_THAT


def dsn_test() -> str:
    """Kho TEST. ⛔ NO neu no tro vao kho THAT.

    Chan cung: khong test nao cham duoc kho that qua duong nay, ke ca khi
    `PG_DSN_TEST` bi dat sai hay bi dat bang `PG_DSN`.
    """
    dsn = os.environ.get(BIEN_TEST) or doi_ten_kho(dsn_that(), TEN_TEST)
    ten = ten_kho(dsn)
    if ten == TEN_THAT:
        raise RuntimeError(
            f"⛔ {BIEN_TEST} tro vao KHO THAT ({ten!r}). Bo test ⛔ khong duoc "
            f"ghi vao so that — do la cach 1.204 dong dau test da lan vao "
            f"fls_itl ngay 27/08. Dat {BIEN_TEST} tro vao kho khac, "
            f"hay bo trong de dung mac dinh {TEN_TEST!r}."
        )
    if not ten:
        raise RuntimeError(f"⛔ {BIEN_TEST}={dsn!r} khong noi ten kho")
    return dsn


def dsn_quan_tri(dsn: str) -> str:
    """DSN tro vao kho `postgres` — de CREATE/DROP DATABASE."""
    return doi_ten_kho(dsn, "postgres")


def noi_chi_doc(dsn: str) -> Any:
    """Mo ket noi **CHI DOC o tang PostgreSQL**. Moi phep ghi bi kho tu choi.

    Dung cho test phai soi kho THAT. ⛔ Khong dua vao ky luat nguoi viet test.
    """
    import psycopg

    conn = psycopg.connect(dsn, autocommit=True)
    conn.execute("SET default_transaction_read_only = on")
    return conn


def tao_kho_test(dsn: str | None = None) -> tuple[str, bool]:
    """Tao kho test neu chua co roi ap het di tru. Tra (dsn, vua_tao).

    ⛔ Tu choi neu dsn tro vao kho THAT (qua `dsn_test`).
    """
    import psycopg

    dsn = dsn or dsn_test()
    ten = ten_kho(dsn)
    if ten == TEN_THAT:
        raise RuntimeError(f"⛔ tu choi tao/ap di tru len KHO THAT ({ten!r})")

    vua_tao = False
    with psycopg.connect(dsn_quan_tri(dsn), autocommit=True) as qt:
        co = qt.execute("select 1 from pg_database where datname=%s", (ten,)).fetchone()
        if not co:
            qt.execute(f'CREATE DATABASE "{ten}"')
            vua_tao = True

    from fls.db import pg_migrate

    with psycopg.connect(dsn, autocommit=True) as c:
        pg_migrate.ap(c)
    return dsn, vua_tao


def dung_lai_kho_test(dsn: str | None = None) -> str:
    """DUNG LAI kho test tu con so 0: DROP DATABASE roi tao + ap di tru.

    ⛔ **Vi sao ⛔ KHONG dung DELETE hay TRUNCATE.**
      · `DELETE` bi `INV-I03` chan (dung nhu thiet ke — so chi-THEM).
      · `TRUNCATE` tung ⛔ KHONG bi chan, nhung tu di tru `0015` thi bi chan —
        va do la CHU Y: mot duong xoa sach so ⛔ khong duoc ton tai.
      ⇒ Duong hop le duy nhat la bo ca kho roi dung lai. Co tien le: owner da
        `DROP DATABASE` + `CREATE DATABASE` kho THAT ngay 27/08, may chay tiep
        **7/7 di tru tu kho rong**, `pg_verify` khop (`GAP-KHO-01` dong).

    ⛔ Tu choi neu dsn tro vao kho THAT — cung mot chot voi `tao_kho_test`.

    ★ Vi sao can: kho test **phinh khong gioi han**. Do 2026-09-07:
      `fls_itl` **56.323** dong, trong do **43.573 (77,4%)** la rac cua chinh
      bo test (`run_id LIKE 'NAP-2000-%'`) — tang **+22.831 dong trong 4 ngay**.
      Hau qua ⛔ khong phai "ton dia": `GET /gates` cham toi **16,1s** trong khi
      client cho **10s** ⇒ **5 bai DO ma ⛔ khong phai loi code** (`GAP-KHO-02`).
      Mot bo test co 5 bai do thuong truc la mot bo test ⛔ khong con ai doc.
    """
    import psycopg

    dsn = dsn or dsn_test()
    ten = ten_kho(dsn)
    if ten == TEN_THAT:
        raise RuntimeError(f"⛔ tu choi DUNG LAI kho THAT ({ten!r})")

    with psycopg.connect(dsn_quan_tri(dsn), autocommit=True) as qt:
        # cat moi ket noi con bam vao kho — neu khong thi DROP se treo
        qt.execute(
            "select pg_terminate_backend(pid) from pg_stat_activity "
            "where datname = %s and pid <> pg_backend_pid()", (ten,))
        qt.execute(f'DROP DATABASE IF EXISTS "{ten}"')
        qt.execute(f'CREATE DATABASE "{ten}"')

    from fls.db import pg_migrate

    with psycopg.connect(dsn, autocommit=True) as c:
        pg_migrate.ap(c)
    return dsn
