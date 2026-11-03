"""Chay SAU khi kho da duoc bo va dung lai rong: ap di tru -> nap -> chung minh.

    python tools/nap_lai_sau_khi_don.py sao_luu/<tep-moc>.json

⛔ Tep nay ⛔ KHONG bo kho, ⛔ khong xoa gi. Buoc bo kho la **khong lui duoc**
nen no thuoc nguoi quyet, va no ⛔ khong nam trong bat ky cong cu nao.

Bon buoc, va **buoc 4 la buoc dang gia nhat**: no kiem mot tinh chat **chua ai
kiem** — so nay co **dung lai duoc tu nguon** hay khong. Neu co thi tu nay moi
lan kho ban, ta don duoc ma khong can mot cau `DELETE` nao.

⚠ Nguon la so SONG. Do duoc 27/08: giua hai lan nap cach nhau **20 phut**, ke
toan da dien them **58 dong** (`rong` 108 -> 50). Nen lech checksum ⛔ KHONG
mac dinh la loi — no co the la **nguon da doi**, va cong `--so-sanh` in ra
**lech o cot nao, bao nhieu dong** de phan biet duoc ba kha nang.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

GOC = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC))

from fls.db.kho import TEN_THAT, dsn_that, ten_kho                # noqa: E402


def _chay(ten: str, *lenh: str) -> int:
    print(f"\n{'=' * 62}\n{ten}\n{'=' * 62}", flush=True)
    r = subprocess.run([sys.executable, *lenh], cwd=GOC)
    return r.returncode


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print("⛔ thieu duong dan tep moc (sao_luu/so_that_*.json)")
        return 1
    moc = sys.argv[1]
    if not (GOC / moc).exists() and not pathlib.Path(moc).exists():
        print(f"⛔ khong thay tep moc: {moc}")
        return 1

    ten = ten_kho(dsn_that())
    if ten != TEN_THAT:
        print(f"⛔ PG_DSN tro vao {ten!r}, khong phai kho THAT {TEN_THAT!r}")
        return 1

    import psycopg
    with psycopg.connect(dsn_that(), autocommit=True) as c:
        co = c.execute("select count(*) from information_schema.tables "
                       "where table_schema='public'").fetchone()[0]
    if co:
        print(f"⛔ kho {ten!r} van con {co} bang — no CHUA duoc dung lai rong.")
        print("   Buoc bo kho thuoc nguoi quyet, xem `tools/sao_luu_kho.py`.")
        return 1
    print(f"kho {ten!r} rong — dung nhu mong doi. Bat dau.")

    if _chay("① ap di tru", "-m", "fls.db.pg_migrate"):
        return 1
    if _chay("② nap lai tu NGUON (doc live, co the vai phut)",
             "tools/nap_that.py", "--that"):
        print("⛔ nap that bai — kho dang RONG. Chay lai buoc ② khi nguon doc duoc.")
        return 1
    rc3 = _chay("③ CHUNG MINH so dung lai duoc (so voi moc)",
                "tools/sao_luu_kho.py", "--so-sanh", moc)
    rc4 = _chay("④ cong kho-sach: chi duoc chua dong cua lan nap THAT",
                "tools/kiem_kho.py")

    print(f"\n{'=' * 62}")
    print(f"cong kho-sach : {'DAT' if rc4 == 0 else 'KHONG DAT'}")
    print(f"so voi moc    : {'TRUNG KHIT' if rc3 == 0 else 'LECH — doc phan tren'}")
    if rc3 and not rc4:
        print("⇒ Kho SACH nhung noi dung lech moc: xem cot nao lech o buoc ③")
        print("  roi doi chieu voi DU DOAN da ghi TRUOC khi chay.")
    return rc4


if __name__ == "__main__":
    sys.exit(main())
