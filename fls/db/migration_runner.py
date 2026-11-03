"""Di tru forward-only co so thu tu + so ghi trong DB.

Vi sao ton tai (GAP-DB-P0-02): ban dau pg_migrate chi phat CREATE TABLE
IF NOT EXISTS. Bang da ton tai thi lenh BO QUA trong im lang, nen cot/FK moi
khong bao gio duoc ap — ma runner van in "da ap N cau DDL". Ap THIEU, bao DU.

Hai nguon su that va cong noi chung:
  - fls/db/schema.py   = TRANG THAI MONG DOI. Sinh ERD, va la thuoc do cua pg_verify.
  - fls/db/migrations/ = DUONG DI toi trang thai do. Text DONG BANG, khong sinh ra.
  - Cong noi hai cai: dung schema TRONG -> ap het migration -> pg_verify PHAI xanh.
    (test_migration_toi_dung_schema_khai_bao). Thieu cong nay thi hai nguon se troi.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
from dataclasses import dataclass

_DIR = pathlib.Path(__file__).resolve().parent / "migrations"
_TEN = re.compile(r"^(\d{4})_([a-z0-9_]+)\.sql$")

# So ghi di tru. Runner tu tao truoc khi ap (bootstrap) — khong phai mot migration,
# vi no phai ton tai TRUOC khi migration dau tien chay.
LEDGER = "fls_migration"
LEDGER_DDL = f"""
CREATE TABLE IF NOT EXISTS {LEDGER} (
  version int NOT NULL PRIMARY KEY,
  name text NOT NULL,
  checksum text NOT NULL,
  applied_at timestamptz NOT NULL DEFAULT now()
)"""


@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    sql: str


def checksum_of(sql: str) -> str:
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()


def discover(dir_: pathlib.Path | None = None) -> tuple[Migration, ...]:
    """Doc thu muc migrations. File sai ten => NO, khong bo qua im lang."""
    d = dir_ or _DIR
    ra: list[Migration] = []
    for f in sorted(d.glob("*.sql")):
        m = _TEN.match(f.name)
        if not m:
            raise ValueError(
                f"ten file di tru sai khuon NNNN_ten_bang_chu.sql: {f.name}")
        ra.append(Migration(int(m.group(1)), m.group(2),
                            f.read_text(encoding="utf-8")))
    return tuple(ra)


MIGRATIONS: tuple[Migration, ...] = discover()


SEP = "-- " + ">" * 3   # dat noi de chinh chuoi nay KHONG xuat hien trong loi van


def _co_sql(khoi: str) -> bool:
    """Khoi chi gom dong trong va dong comment thi khong phai cau lenh."""
    return any(d.strip() and not d.strip().startswith("--")
               for d in khoi.splitlines())


def cau_lenh(sql: str) -> list[str]:
    """Tach mot file .sql thanh tung cau theo dong phan cach SEP.

    Khong tach bang dau ';' vi than ham plpgsql chua dau ';' ben trong.
    Khoi chi co comment (vi du header cua file) bi bo qua.
    """
    return [c.strip() for c in sql.split(SEP) if c.strip() and _co_sql(c)]


def da_ap(cur) -> dict[int, str]:
    """Tra {version: checksum} da ghi trong so. So chua co => rong."""
    cur.execute(
        "SELECT to_regclass(%s) IS NOT NULL", (LEDGER,))
    if not cur.fetchone()[0]:
        return {}
    cur.execute(f"SELECT version, checksum FROM {LEDGER} ORDER BY version")
    return {v: c for v, c in cur.fetchall()}


def kiem_lich_su(cu: dict[int, str], khai: tuple[Migration, ...]) -> list[str]:
    """Migration DA AP thi cam sua. Sua la lich su khac nhau tren cac moi truong."""
    theo_ver = {m.version: m for m in khai}
    ra = []
    for v, cks in sorted(cu.items()):
        m = theo_ver.get(v)
        if m is None:
            ra.append(f"migration {v:04d} da ap tren DB nhung KHONG con trong code")
        elif checksum_of(m.sql) != cks:
            ra.append(f"migration {v:04d}_{m.name} DA BI SUA sau khi ap "
                      f"(checksum DB={cks[:12]}… code={checksum_of(m.sql)[:12]}…)")
    return ra


def con_thieu(cu: dict[int, str]) -> tuple[Migration, ...]:
    return tuple(m for m in MIGRATIONS if m.version not in cu)
