"""Bao cao MOT MAT cho `NUT-CHAY-FLS.cmd` — doc de hieu, ⛔ khong phai JSON.

⛔⛔ **Vi sao tep nay ton tai chu ⛔ khong nhoi SQL vao `.cmd`.** Dau ngoac kep
   long nhau trong `docker exec ... psql -c "..."` la cho de hong nhat tren
   Windows, va no hong theo kieu **im lang**: `psql` tra ma 0 voi mot cau
   rong. Mot nut bao *"xong"* ma ⛔ khong do gi la dung cai `A1` sinh ra de
   tranh.

★ **Ba cau nut phai tra loi**, va ⛔ khong cau nao la *"chay khong loi"*:

  ⓐ **So co bao nhieu dong, nap lan cuoi bao gio** — va ⛔ CANH BAO neu so
    dang **dong bang** *(anh moi nhat ⛔ chua bao gio duoc nap)*.
  ⓑ **Anh moi nhat moi lan** — bao nhieu nguon, bao nhieu dong, **da nap chua**.
  ⓒ **Nguon ra 0 dong** — kem cau nhac rang mot phan trong so ay la sheet
    **TEMPLATE de danh cho** *(owner tra loi 10/09)*, nen con so ay ⛔ KHONG
    tu no la mot loi.

⛔ Tep nay **CHI DOC**. ⛔ Khong mot cau ghi nao.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg  # noqa: E402

from fls.db.kho import dsn_that  # noqa: E402

# Nguon ra 0 dong ma owner da xac nhan la **template de danh cho** (10/09).
# ⛔ Danh sach nay la mot cau NHAC tren man hinh, ⛔ KHONG phai mot phep loc:
#   loc chung ra khoi bao cao la lam mot con so tu nho di, va lan sau co mot
#   sheet rong THAT thi ⛔ khong ai thay.
TEMPLATE_DE_DANH_CHO = (
    "R | 721916_ACB VND_Coretap",
    "R | 723916_ACB USD_Coretap",
)


def _so(conn) -> tuple[int, str, int]:
    """(so dong so, nap lan cuoi, so tang nguon)."""
    with conn.cursor() as c:
        c.execute("SELECT count(*), coalesce(max(created_at)::text,'—'),"
                  " count(DISTINCT source_system) FROM fls_itl")
        return c.fetchone()


def _anh_moi(conn) -> list[tuple]:
    """Anh MOI NHAT cua tung lan + no da duoc dung de nap chua."""
    with conn.cursor() as c:
        c.execute("""
            SELECT c.lan, c.chup_id,
                   to_char(c.doc_luc + interval '7 hour','DD/MM HH24:MI'),
                   c.actor,
                   (SELECT count(*) FROM fls_chup_nguon n
                     WHERE n.chup_id = c.chup_id),
                   (SELECT count(*) FROM fls_chup_dong d
                     WHERE d.chup_id = c.chup_id),
                   (SELECT count(*) FROM fls_run r
                     WHERE r.chup_id = c.chup_id)
              FROM fls_chup c
             WHERE c.doc_luc = (SELECT max(x.doc_luc) FROM fls_chup x
                                 WHERE x.lan = c.lan)
             ORDER BY c.lan""")
        return c.fetchall()


def _nguon_rong(conn, chup_id: int) -> list[str]:
    with conn.cursor() as c:
        c.execute("""
            SELECT s.source_key FROM fls_chup_nguon n
              JOIN fls_source s ON s.source_id = n.source_id
             WHERE n.chup_id = %s
               AND NOT EXISTS (SELECT 1 FROM fls_chup_dong d
                                WHERE d.chup_id = n.chup_id
                                  AND d.source_id = n.source_id)
             ORDER BY s.source_key""", (chup_id,))
        return [r[0] for r in c.fetchall()]


def _in_so(conn) -> None:
    dong, luc, tang = _so(conn)
    print(f"\n┌─ SO KE TOAN (`fls_itl`)")
    print(f"│  {dong:,} dong  ·  nap lan cuoi: {luc[:16]}  ·  {tang} tang nguon")
    if tang > 1:
        print(f"│  ⛔ CANH BAO: so co {tang} TANG NGUON — chong trung MU giua "
              f"chung (xem QD ngay 10/09)")


def _in_anh(conn) -> list[tuple]:
    ds = _anh_moi(conn)
    print("│\n├─ ANH CHUP MOI NHAT")
    for lan, cid, gio, actor, nguon, dong, da_nap in ds:
        dau = "✅ da nap" if da_nap else "⛔ CHUA NAP VAO SO"
        so = f"{dong:,} dong" if dong else "(lan nay ghi thang, ⛔ khong qua bang dong)"
        print(f"│  {lan:<5} #{cid}  {gio}  ·  {nguon} nguon  ·  {so}")
        print(f"│  {'':<5}  actor {actor}  ·  {dau}")
    return ds


def _in_rong(conn, ds: list[tuple]) -> None:
    for lan, cid, *_ in ds:
        if lan != "Bank":
            continue
        rong = _nguon_rong(conn, cid)
        if not rong:
            continue
        tpl = [x for x in rong if x in TEMPLATE_DE_DANH_CHO]
        print(f"│\n├─ NGUON RA 0 DONG: {len(rong)}/{_dem_nguon(ds)} "
              f"(lan Bank, anh #{cid})")
        print(f"│  trong do {len(tpl)} la TEMPLATE de danh cho (owner 10/09) "
              f"⇒ dung la 0 dong")
        for x in rong[:15]:
            nhan = "  ← template, de danh cho" if x in TEMPLATE_DE_DANH_CHO else ""
            print(f"│    · {x}{nhan}")
        if len(rong) > 15:
            print(f"│    … con {len(rong) - 15} nguon nua")


def _dem_nguon(ds: list[tuple]) -> int:
    for lan, _cid, _g, _a, nguon, *_ in ds:
        if lan == "Bank":
            return nguon
    return 0


def main() -> int:
    with psycopg.connect(dsn_that()) as conn:
        _in_so(conn)
        ds = _in_anh(conn)
        _in_rong(conn, ds)
    print("│\n└─ ⛔ NUT NAY **CHI CHUP**, ⛔ KHONG nap vao so.")
    print("   Ly do: khoang lech 3.413 dong giua hai tang nguon ⛔ CHUA duoc")
    print("   giai thich tung dong ⇒ cong CHAN cua quyet dinh 10/09.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
