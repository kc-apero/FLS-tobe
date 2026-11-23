"""Tra loi bang PHEP DO: ke toan sua duoc gi, va sua duoc DEN DAU.

  python tools/verify_sua_duoc_gi.py

Chay tren **kho TEST** (⛔ khong dong den kho that), dung CHINH cac cua ghi ma
man hinh se goi. Moi dong in ra la mot lan goi that, ⛔ khong phai mot cau khai.

★★ **Vi sao co script nay.** Owner hoi *"xac nhan cho toi ke toan co sua duoc
cac thong tin da duoc dien khong?"* (2026-08-28). Cau tra loi **doc tu ma nguon**
la mot cau tra loi de sai — cung cai benh da lam toi bao *"cot hoa don chi co ten
tep"* trong khi 98% dong la duong dan Drive. ⇒ Chay that roi in ket qua.
"""

from __future__ import annotations

import sys
import uuid
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import psycopg                                                    # noqa: E402

from fls.db.kho import dsn_test                                   # noqa: E402
from fls.repo import doc_bao_cao as bc                            # noqa: E402
from fls.repo import ghi_tay as gt                                # noqa: E402
from fls.repo.danh_muc_actor import (ACTOR_VERIFY_SUA,            # noqa: E402
                                     ACTOR_VERIFY_SUA_2)
from fls.repo.pham_vi import mot_lan_nap                          # noqa: E402

# ⛔ `WO-011` / `HOI-012` cau 1: truoc day cong cu nay ghi `ke-toan@apero.vn`
#   — mot ten GIONG NGUOI, trong khi no la mot CONG CU *(chay kho TEST)*, va
#   chinh chuoi ay la actor **nguoi mau** cua bai nghiem thu `KQ-002`. Mot
#   chuoi mang hai nghia la cho thuoc "nguoi that" vo lan thu tu. ⇒ Ten MAY,
#   khai o SO ACTOR.
ACTOR = ACTOR_VERIFY_SUA
OK, NO = "  DUOC", "  ⛔ BI CHAN"


def _run(c) -> str:
    r = "NAP-2000-01-01-Q" + uuid.uuid4().hex[:6].upper()
    c.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
              " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong(c, run: str, *, ky: str = "open") -> int:
    """Mot dong so co `hd`/`cdt1` DA DIEN tu nguon — dung tinh huong owner hoi."""
    return c.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state,"
        " hd, cdt1, pay_type, memo)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-Q','VND',%s,'UNMAPPED',%s,"
        " 'FNS | Facilities','SHQ2 | HQ2','Transfer','dien giai goc')"
        " RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, D("1000.00"), ky)
    ).fetchone()[0]


def _thu(nhan: str, f, *a, **k) -> None:
    try:
        r = f(*a, **k)
        print(f"{OK:12} {nhan}"
              + (f"   -> {r}" if isinstance(r, str) else ""))
    except gt.LoiGhi as e:
        print(f"{NO:12} {nhan}\n{' ' * 14}{type(e).__name__}: "
              f"{str(e)[:150]}")


def main() -> int:
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        run = _run(c)
        pv = mot_lan_nap(run)

        print("═" * 78)
        print("① BAY TRUONG NAO SUA DUOC — va 31 cot con lai thi sao")
        print("═" * 78)
        print(f"  sua duoc ({len(gt.TRUONG_GHI)} truong): "
              f"{', '.join(sorted(gt.TRUONG_GHI))}")
        print(f"    · vao P&L (co cot do parity): {', '.join(gt.TRUONG_HOP_DONG)}")
        print(f"    · ngoai P&L                 : {', '.join(gt.TRUONG_NGOAI)}")
        i = _dong(c, run)
        _thu("go mot truong NGOAI danh sach (`memo` — dien giai)",
             gt.ghi_but_toan, c, pv, i, "memo", "sua dien giai",
             actor=ACTOR, reason="thu")

        print()
        print("═" * 78)
        print("② O DA CO GIA TRI TU NGUON — go de len duoc khong")
        print("═" * 78)
        t = gt.truoc_khi_go(c, pv, i, "hd")
        print(f"  gia tri dang co: {t['gia_tri']!r}  (nguon: {t['value_source']})")
        _thu("go gia tri KHAC ma ⛔ khong `force`",
             gt.ghi_but_toan, c, pv, i, "hd", "GAC | Other",
             actor=ACTOR, reason="phan loai lai")
        _thu("go gia tri KHAC, CO `force` + ly do",
             gt.ghi_but_toan, c, pv, i, "hd", "GAC | Other",
             actor=ACTOR, reason="phan loai lai", force=True)
        t = gt.truoc_khi_go(c, pv, i, "hd")
        print(f"  -> gia tri hieu luc nay: {t['gia_tri']!r}  "
              f"(nguon: {t['value_source']})")
        print(f"  -> cot NGUON van nguyen : {t['nguon']!r}   "
              f"⇐ ⛔ so goc KHONG bi ghi de")

        print()
        print("③ SUA LAN THU HAI, THU BA")
        _thu("go tiep gia tri thu ba",
             gt.ghi_but_toan, c, pv, i, "hd", "OPC | Operating Cost",
             actor=ACTOR_VERIFY_SUA_2, reason="doi lai", force=True)
        t = gt.truoc_khi_go(c, pv, i, "hd")
        print(f"  -> hieu luc: {t['gia_tri']!r}")
        n = len(bc.doc_nhat_ky(c, pv, i))
        print(f"  -> nhat ky co {n} dong (moi lan sua la MOT dong, ⛔ khong ghi de)")

        print()
        print("④ HOAN TAC (dao but toan)")
        d = bc.doc_mot_dong(c, pv, i)
        adj = [x for x in d["but_toan"] if x["field"] == "hd"
               and x["reversal_of"] is None][-1]
        _thu(f"dao but toan moi nhat (adj_id={adj['adj_id']})",
             gt.dao_but_toan, c, pv, adj["adj_id"], actor=ACTOR,
             reason="dao lai, go sai")
        t = gt.truoc_khi_go(c, pv, i, "hd")
        print(f"  -> hieu luc lui ve: {t['gia_tri']!r}  (nguon: {t['value_source']})")

        print()
        print("═" * 78)
        print("⑤ DONG DA BAM 'XONG' — con sua duoc khong")
        print("═" * 78)
        j = _dong(c, run)
        gt.danh_dau_xong(c, pv, j, actor=ACTOR)
        print("  (da bam xong, dong da roi hang cho)")
        _thu("go mot truong tren dong DA XONG",
             gt.ghi_but_toan, c, pv, j, "cdt1", "SHQ1 | HQ1",
             actor=ACTOR, reason="sua sau khi xong", force=True)
        print(f"  -> con trong hang cho? "
              f"{'CO' if any(x['itl_id'] == j for x in bc.doc_hang_cho(c, pv).dong) else 'KHONG'}")

        print()
        print("═" * 78)
        print("⑥ KY DA CHOT")
        print("═" * 78)
        k = _dong(c, run, ky="locked")
        _thu("go mot truong khi ky DA CHOT",
             gt.ghi_but_toan, c, pv, k, "hd", "GAC | Other",
             actor=ACTOR, reason="sua", force=True)
        _thu("go mot truong khi ky DA CHOT (co `force`)",
             gt.ghi_but_toan, c, pv, k, "hd", "GAC | Other",
             actor=ACTOR, reason="sua", force=True)
        _thu("bam 'xong' khi ky DA CHOT",
             gt.danh_dau_xong, c, pv, k, actor=ACTOR)

        # don sach
        for x in (i, j, k):
            c.execute("DELETE FROM fls_journal WHERE itl_id=%s", (x,))
            c.execute("DELETE FROM fls_adjustment WHERE reversal_of IS NOT NULL"
                      " AND itl_id=%s", (x,))
            c.execute("DELETE FROM fls_adjustment WHERE itl_id=%s", (x,))
            c.execute("DELETE FROM fls_queue_event WHERE itl_id=%s", (x,))
            c.execute("DELETE FROM fls_itl WHERE itl_id=%s", (x,))
        c.execute("DELETE FROM fls_run WHERE run_id=%s", (run,))
    return 0


if __name__ == "__main__":
    sys.exit(main())
