# -*- coding: utf-8 -*-
"""NHIN SO bang MAT — cua so doc cho nguoi khong go SQL.

    python tools/nhin_so.py                  # mot man hinh tong quan
    python tools/nhin_so.py --sheet OCBC     # liet ke dong cua cac sheet khop
    python tools/nhin_so.py --ra so.csv      # xuat CA SO ra CSV mo bang Excel

⛔⛔ **Vi sao tep nay ton tai.** Chu so cua mot so ke toan ⛔ khong duoc chi
   song trong dau nguoi viet ma. Owner hoi *"toi query de nhin bang mat kieu
   gi"* — va cau tra loi *"cai DBeaver len"* la mot cau tra loi **doi cho**:
   no doi nguoi doc phai biet ten 18 bang va nghia cua `ps_no`/`ps_co`.

★ **Ba dieu tep nay khai ra man hinh, va ⛔ khong cai nao la suy luan:**

  ⓐ **So co gi** — bao nhieu dong, tu ngay nao, tien vao/ra theo TUNG loai tien.
  ⓑ **⛔ So CHUA co gi** — 14 truong cua `ITL-CONTRACT` thi tang `R |` chi cho
    duoc **5**. Chin truong con lai *(`memo` · `acct` · `le` · `hd` ·
    `pay_type` · `cdt1` · `id_payee` · `invoice` · `le_payer`)* la **0/8.387**,
    va do ⛔ **khong phai loi nap**: do that 11/09 tren ca 8.406 dong chup cho
    thay nguon chi co **5 cot** *(`Date` · `Debit` · `Credit` · `Currency` ·
    `Reference number`)*. Chung duoc dien o buoc ② ghep lenh chi + ③ ITL
    adjust — **moc `B`/`C`**, ⛔ chua chay. In cot rong ra man hinh la cach
    duy nhat de con so ay ⛔ khong bi hieu nham la *"da xong"*.
  ⓒ **Anh → so con thieu o dau** — theo TUNG nguon, ⛔ khong phai mot tong so.

⛔ Tep nay mo ket noi bang `noi_chi_doc()`: PostgreSQL **tu tu choi** moi phep
  ghi. ⛔ Khong dua vao ky luat cua nguoi doc tep nay.

⚠ Cot `loai` trong bao cao cu tung la mot **bay**: `fls_reject` ghi theo LUOT,
  nen 1.772 dong bi loai o luot dau *(ngay mo ho)* van con nam do sau khi
  chung **da vao so** o luot nap bu. ⇒ Tep nay do **`anh - so`** *(cai con
  THIEU that)*, ⛔ khong do `count(fls_reject)`.
"""
from __future__ import annotations

import argparse
import csv
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fls.db.kho import dsn_that, noi_chi_doc  # noqa: E402

# 14 truong cua `ITL-CONTRACT` v1.0, khai theo TEN (⛔ khong theo vi tri —
# vi tri la chuyen cua `ITL-CANON`). Tep nay in ty le dien cua TUNG truong.
CONTRACT = ("doc_date", "doc_no", "memo", "curr", "ps_no", "ps_co", "acct",
            "le", "hd", "pay_type", "cdt1", "id_payee", "invoice", "le_payer")

# Nguon ra 0 dong ma owner xac nhan la **template de danh cho** (10/09).
# ⛔ Mot cau NHAC, ⛔ KHONG phai phep loc — xem `tools/nut_trang_thai.py`.
TEMPLATE_DE_DANH_CHO = (
    "R | 721916_ACB VND_Coretap",
    "R | 723916_ACB USD_Coretap",
)


def vn(n) -> str:
    """So kieu tai lieu: dau cham ngan nghin, dau phay thap phan."""
    if n is None:
        return "—"
    return f"{n:,.2f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def _bang(tieu_de: str, cot: tuple[str, ...], hang: list[tuple]) -> None:
    print(f"\n{tieu_de}")
    if not hang:
        print("  (⛔ khong co dong nao)")
        return
    r = [tuple(str(x) for x in h) for h in hang]
    w = [max(len(cot[i]), *(len(x[i]) for x in r)) for i in range(len(cot))]
    print("  " + "  ".join(c.ljust(w[i]) for i, c in enumerate(cot)))
    print("  " + "  ".join("─" * x for x in w))
    for x in r:
        print("  " + "  ".join(x[i].rjust(w[i]) if i else x[i].ljust(w[i])
                               for i in range(len(cot))))


def tong_quan(conn) -> None:
    with conn.cursor() as c:
        c.execute("SELECT count(*), min(doc_date), max(doc_date),"
                  " count(DISTINCT source_sheet), count(DISTINCT source_system)"
                  " FROM fls_itl")
        n, d1, d2, sheet, tang = c.fetchone()
        c.execute("SELECT count(*) FROM fls_moi_noi")
        noi, = c.fetchone()
    print("═" * 72)
    print(f"  SO FLS  ·  {n:,} dong  ·  {d1} → {d2}".replace(",", "."))
    print(f"  {sheet} tai khoan ngan hang  ·  {tang} tang nguon  ·  "
          f"{noi:,} moi noi lenh chi".replace(",", "."))
    print("═" * 72)


def theo_tien(conn) -> None:
    with conn.cursor() as c:
        c.execute("""SELECT curr, count(*), sum(ps_no), sum(ps_co)
                       FROM fls_itl GROUP BY curr ORDER BY count(*) DESC""")
        h = [(t, f"{n:,}".replace(",", "."), vn(no), vn(co))
             for t, n, no, co in c.fetchall()]
    _bang("── TIEN VAO / RA theo loai tien ────────── (Debit = vao · Credit = ra)",
          ("tien", "dong", "VAO (Debit)", "RA (Credit)"), h)


def theo_thang(conn) -> None:
    with conn.cursor() as c:
        c.execute("""SELECT to_char(doc_date,'YYYY-MM'), count(*),
                            count(DISTINCT source_sheet)
                       FROM fls_itl GROUP BY 1 ORDER BY 1 DESC LIMIT 14""")
        h = [(k, f"{n:,}".replace(",", "."), s) for k, n, s in c.fetchall()]
    _bang("── DONG theo THANG (14 thang gan nhat) ─────────────────────────────",
          ("thang", "dong", "tai khoan"), h)


def do_day_truong(conn) -> None:
    """ⓑ ⛔ Truong nao con RONG — cho de hieu nham *'nap xong'* nhat."""
    sel = ", ".join(f"count({c})" for c in CONTRACT)
    with conn.cursor() as c:
        c.execute(f"SELECT count(*), {sel} FROM fls_itl")
        r = c.fetchone()
    n, dem = r[0], r[1:]
    h = [(ten, f"{d:,}".replace(",", "."),
          f"{100.0 * d / n:5.1f}%" if n else "—",
          "" if d else "⛔ buoc ②/③ moc B/C chua chay")
         for ten, d in zip(CONTRACT, dem)]
    _bang("── 14 TRUONG cua `ITL-CONTRACT` — truong nao DA co so ───────────────",
          ("truong", "co o", "ty le", "vi sao rong"), h)

    # ⚠ `count(ps_no)` dem **o co mat**, va `0` la mot o co mat ⇒ con so ay
    #   ⛔ khong tra loi duoc *"dong nay tien VAO hay RA"*. Phep dem duoi day
    #   moi tra loi, va no **tu chung minh**: hai ve phai cong dung `n`.
    with conn.cursor() as c:
        c.execute("SELECT count(*) FILTER (WHERE coalesce(ps_no,0) <> 0),"
                  "       count(*) FILTER (WHERE coalesce(ps_co,0) <> 0),"
                  "       count(*) FILTER (WHERE coalesce(ps_no,0) <> 0"
                  "                          AND coalesce(ps_co,0) <> 0)"
                  "  FROM fls_itl")
        vao, ra, ca_hai = c.fetchone()
    dau = "✓" if vao + ra == n and not ca_hai else "⛔"
    print(f"\n  {dau} moi dong dung MOT chieu: VAO {vao:,} + RA {ra:,} = "
          f"{vao + ra:,} / {n:,} dong · ca hai chieu: {ca_hai:,}"
          .replace(",", "."))


def con_thieu(conn, chup_id: int | None) -> None:
    """ⓒ Anh → so: nguon nao con thieu dong. ⛔ Do `anh - so`, ⛔ khong do reject."""
    with conn.cursor() as c:
        if chup_id is None:
            c.execute("SELECT chup_id FROM fls_chup WHERE lan='Bank'"
                      " ORDER BY doc_luc DESC LIMIT 1")
            r = c.fetchone()
            if not r:
                print("\n⛔ ⛔ khong co anh `Bank` nao trong kho")
                return
            chup_id = r[0]
        c.execute("""
            SELECT s.source_key,
                   (SELECT count(*) FROM fls_chup_dong d
                     WHERE d.chup_id = n.chup_id AND d.source_id = s.source_id),
                   (SELECT count(*) FROM fls_itl i
                     WHERE i.source_sheet = s.source_key)
              FROM fls_chup_nguon n JOIN fls_source s USING (source_id)
             WHERE n.chup_id = %s ORDER BY s.source_key""", (chup_id,))
        hang = c.fetchall()
    thieu = [(k, a, s) for k, a, s in hang if a != s]
    rong = [k for k, a, s in hang if a == 0 and s == 0]
    h = [(k, f"{a:,}".replace(",", "."), f"{s:,}".replace(",", "."),
          f"{a - s:,}".replace(",", "."),
          "⛔ nguon CHAN — ⛔ chua khai `thu_tu`" if s == 0 else "")
         for k, a, s in thieu]
    _bang(f"── ANH #{chup_id} → SO: nguon con THIEU dong ──────────────────────",
          ("nguon", "anh", "so", "thieu", "ghi chu"), h)
    print(f"\n  {len(hang) - len(thieu)}/{len(hang)} nguon KHOP het.")
    if rong:
        print(f"  {len(rong)} nguon ra 0 dong (anh cung 0) — trong do "
              f"{sum(1 for k in rong if k in TEMPLATE_DE_DANH_CHO)} la "
              f"TEMPLATE de danh cho, owner xac nhan 10/09.")


def liet_ke(conn, loc: str, gioi_han: int) -> None:
    with conn.cursor() as c:
        c.execute("""SELECT itl_id, doc_date, source_sheet, curr, ps_no, ps_co,
                            doc_no
                       FROM fls_itl WHERE source_sheet ILIKE %s
                      ORDER BY doc_date DESC, itl_id DESC LIMIT %s""",
                  (f"%{loc}%", gioi_han))
        h = [(i, str(d), k[:34], t, vn(no), vn(co), (dn or "")[:20])
             for i, d, k, t, no, co, dn in c.fetchall()]
    _bang(f"── DONG khop {loc!r} (toi da {gioi_han}) ────────────────────────────",
          ("itl_id", "ngay", "tai khoan", "tien", "vao", "ra", "so chung tu"), h)


def xuat_csv(conn, ra: pathlib.Path) -> None:
    """⛔ `utf-8-sig`: Excel ban VN mo `utf-8` tran se hien tieng Viet thanh rac."""
    cot = ("itl_id", "doc_date", "source_sheet", "doc_no", "curr",
           "ps_no", "ps_co", "run_id", "created_at")
    with conn.cursor() as c:
        c.execute(f"SELECT {', '.join(cot)} FROM fls_itl"
                  f" ORDER BY doc_date, itl_id")
        hang = c.fetchall()
    ra.parent.mkdir(parents=True, exist_ok=True)
    with ra.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(("itl_id", "Ngay", "Tai khoan", "So chung tu", "Tien",
                    "VAO (Debit)", "RA (Credit)", "Luot nap", "Ghi luc"))
        w.writerows(hang)
    print(f"\n✅ {len(hang):,} dong → {ra}".replace(",", "."))
    print("   ⚠ Tep nay chua SO TIEN THAT — no ⛔ khong duoc len git "
          "(`sao_luu/` va `hien_vat/` da bi gitignore vi ly do nay).")


def main() -> int:
    p = argparse.ArgumentParser(description="Nhin so FLS bang mat — CHI DOC")
    p.add_argument("--sheet", help="liet ke dong cua tai khoan khop chuoi nay")
    p.add_argument("--so", type=int, default=40, help="so dong liet ke (40)")
    p.add_argument("--chup", type=int, default=None, help="chup_id de doi chieu")
    p.add_argument("--ra", type=pathlib.Path, help="xuat CA SO ra tep CSV")
    a = p.parse_args()

    conn = noi_chi_doc(dsn_that())          # ⛔ kho tu choi moi phep ghi
    try:
        if a.ra:
            xuat_csv(conn, a.ra)
            return 0
        if a.sheet:
            liet_ke(conn, a.sheet, a.so)
            return 0
        tong_quan(conn)
        theo_tien(conn)
        theo_thang(conn)
        do_day_truong(conn)
        con_thieu(conn, a.chup)
        print("\n  Xem mot tai khoan:  python tools/nhin_so.py --sheet OCBC")
        print("  Xuat ra Excel    :  python tools/nhin_so.py --ra so.csv")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
