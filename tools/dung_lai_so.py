"""DUNG LAI SO tu tang `R |` — cu nap dau tien cua mot kho vua dung lai.

    FLS_CHO_GHI_THAT=1 python tools/dung_lai_so.py --that [--chup <id>]

⛔⛔⛔ **Vi sao tep nay ton tai, va vi sao no CO MOT CONG RIENG.**

`tools/nap_that.py` (27/08) nap tu tang `Transaction Mapping L1` — tang PHAI
SINH cua Google Sheets. Duong thiet ke la **60 sheet `R |`** *(tang ke toan GO
VAO)*. Hai tang dung hai `source_system`, va `content_key` chua no ⇒ chong
trung **MU giua chung**: do that 10/09 tren kho nhap, nap ca hai sinh **3.694
dong** khop ca bon khoa nghiep vu ma nam **hai lan**.

⇒ Cong cu nay nap **CHI tang `R |`**, qua **dung cua ma man `F04` di**
  *(`nap_cua.lo_nap`)* — ⛔ khong viet duong nap thu hai. Ba thu ma
  `chay_nap.chay()` giu *(chong trung `content_key` · cong bon duong · MOT giao
  dich)* vi the ⛔ khong co ban sao.

★ **Ba cong cua chinh tep nay:**

  ⓐ ⛔ **Doi `FLS_CHO_GHI_THAT=1`.** Mot cong cu ghi vao so ke toan ⛔ khong
    duoc chay chi vi ai do go dung ten tep. Thieu bien ⇒ NO, ⛔ khong ghi gi.
  ⓑ ⛔ **Doi so DANG RONG** — hay, voi `--nap-bu`, doi so co **DUNG MOT
    tang** `P100`. Muc dich cua cong nay ⛔ khong phai *"so phai rong"* ma la
    ***"⛔ dung tron hai tang nguon"***; mot cu nap lai **cung tang** la hop
    le *(vd sau khi khai `thu_tu`, cac dong tung bi loai vi ngay mo ho nay
    doc duoc)* va `content_key` **tu chong trung** cac dong da co.
  ⓒ ⭐ **Nap kem GHEP LENH CHI.** Doc anh PM **hieu luc** roi truyen xuong;
    thieu no thi so co **0 moi noi** va 2.427 moi noi MAY ghep bien thanh
    2.427 cu bam TAY *(lo im lang da do duoc 10/09)*.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg  # noqa: E402

from fls.api.xu_ly import YeuCau  # noqa: E402  (phai TRUOC `nap_cua`)
from fls.api import nap_cua  # noqa: E402
from fls.db.kho import dsn_that  # noqa: E402
from fls.repo.danh_muc_actor import ACTOR_DUNG_LAI_SO  # noqa: E402
from fls.repo.pham_vi import chi_nap_that  # noqa: E402

BIEN_CHO_GHI = "FLS_CHO_GHI_THAT"


def _cong_moi_truong() -> None:
    """ⓐ Bien moi truong la CONG, ⛔ khong phai mot lua chon tien loi."""
    if os.environ.get(BIEN_CHO_GHI) != "1":
        raise SystemExit(
            f"⛔ thieu {BIEN_CHO_GHI}=1. Cong cu nay GHI vao so ke toan THAT "
            f"— no ⛔ khong duoc chay chi vi ai do go dung ten tep.")


TANG = "P100"


def _cong_mot_tang(conn, nap_bu: bool) -> None:
    """ⓑ So phai RONG — hay, voi `--nap-bu`, **chi co DUNG MOT tang** `P100`.

    ⛔⛔ **Vi sao noi long, va noi long theo CHIEU NAO.** Muc dich cua cong nay
       ⛔ **khong** phai *"so phai rong"* — no la ***"⛔ dung tron hai tang
       nguon"***. Mot cu nap lai **cung tang** la hop le va can thiet: sau khi
       khai `thu_tu`, **1.770** dong tung bi loai vi ngay mo ho nay doc duoc,
       va `content_key` **tu chong trung** 6.617 dong da co *(cung
       `source_system` + `source_sheet`)*.

    ⇒ Cong doi dung dieu no van luon muon: `count(DISTINCT source_system) = 1`
      va tang ay la `P100`. Mot so co `RAW` trong do ⇒ **NO**, y nhu truoc.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT count(*), count(DISTINCT source_system),"
                    " coalesce(min(source_system),'') FROM fls_itl")
        n, so_tang, tang = cur.fetchone()
    if not n:
        return
    if not nap_bu:
        raise SystemExit(
            f"⛔ so da co {n:,} dong. Cong cu nay la cu nap DAU TIEN sau khi "
            f"dung lai kho. Neu ban muon nap BU cung tang *(vd sau khi khai "
            f"`thu_tu`)* thi them `--nap-bu`.")
    if so_tang != 1 or tang != TANG:
        raise SystemExit(
            f"⛔ so co {so_tang} tang nguon ({tang!r}) — `--nap-bu` chi chay "
            f"khi so co DUNG MOT tang {TANG!r}. Nap them vao mot so da tron "
            f"tang la lam nang dung cai loi HAI TANG.")
    print(f"nap BU vao so dang co {n:,} dong · 1 tang {tang!r} "
          f"(chong trung bang `content_key`)")


def _anh_bank(conn, chup_id: int | None) -> int:
    if chup_id:
        return chup_id
    with conn.cursor() as cur:
        cur.execute("SELECT chup_id FROM fls_chup WHERE lan = 'Bank'"
                    " ORDER BY doc_luc DESC LIMIT 1")
        r = cur.fetchone()
    if not r:
        raise SystemExit("⛔ ⛔ khong co anh `Bank` nao trong kho")
    return r[0]


def _nguon(conn, chup_id: int) -> list[int]:
    with conn.cursor() as cur:
        cur.execute("SELECT source_id FROM fls_chup_nguon WHERE chup_id = %s"
                    " ORDER BY source_id", (chup_id,))
        return [r[0] for r in cur.fetchall()]


def _run_id(chup_id: int) -> str:
    """`NAP-yyyy-mm-dd-RTANG<chup>` — hinh ma `HINH_RUN_THAT` doi."""
    with psycopg.connect(dsn_that()) as c, c.cursor() as cur:
        cur.execute("SELECT to_char(doc_luc + interval '7 hour','YYYY-MM-DD')"
                    " FROM fls_chup WHERE chup_id = %s", (chup_id,))
        ngay = cur.fetchone()[0]
    return f"NAP-{ngay}-RTANG{chup_id}"


def _run_id_bu(chup_id: int, n: int) -> str:
    """Luot nap BU phai co `run_id` RIENG — `fls_run` khoa theo `run_id`.

    ⛔ Dung lai `run_id` cu thi `mo_run` co `ON CONFLICT DO NOTHING` nen no di
    qua **im lang**, va bien ban cua luot nay se **cong vao** so dong cua luot
    truoc ⇒ ⛔ khong doc duoc luot nay them bao nhieu.
    """
    return f"NAP-{_ngay(chup_id)}-BU{n}"


def _ngay(chup_id: int) -> str:
    with psycopg.connect(dsn_that()) as c, c.cursor() as cur:
        cur.execute("SELECT to_char(doc_luc + interval '7 hour','YYYY-MM-DD')"
                    " FROM fls_chup WHERE chup_id = %s", (chup_id,))
        return cur.fetchone()[0]


def _in(bb: dict) -> None:
    """⛔ `_bien_ban_gop` lam `bb.update(nap)` ⇒ khoa nap nam o TANG NGOAI.

    ⚠ Ban dau tep nay doc `bb["nap"]` va in ra **tam dong `None`** — dung loai
      *"bien ban ⛔ khong noi gi"* ma ca bo tai lieu nay cam. Neu mot khoa
      thieu that thi phai in **`⛔ THIEU`**, ⛔ khong in `None`.
    """
    print("\n=== BIEN BAN ===")
    for k in ("chup_id", "doc_luc", "so_nguon", "so_nguon_vao",
              "so_nguon_chua", "so_dong_vao", "so_dong_ra"):
        print(f"  {k:16} {bb.get(k, '⛔ THIEU')}")
    print("\n=== KET QUA NAP ===")
    for k in ("run_id", "anh_pm", "vao_so", "trung", "loai", "unmapped",
              "vao_hang_cho", "ghep_pm"):
        v = bb.get(k, "⛔ THIEU")
        if k == "anh_pm" and v is None:
            v = "⛔ ⛔ khong co anh PM ⇒ 0 moi noi"
        print(f"  {k:16} {v}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--that", action="store_true",
                   help="bat buoc — xac nhan ghi vao kho THAT")
    p.add_argument("--nap-bu", action="store_true",
                   help="nap them vao so DA CO, cung tang (vd sau khai thu_tu)")
    p.add_argument("--chup", type=int, default=None,
                   help="chup_id cua anh Bank (mac dinh: anh moi nhat)")
    a = p.parse_args()
    if not a.that:
        raise SystemExit("⛔ thieu `--that`")
    _cong_moi_truong()

    with psycopg.connect(dsn_that(), autocommit=True) as conn:
        _cong_mot_tang(conn, a.nap_bu)
        cid = _anh_bank(conn, a.chup)
        sids = _nguon(conn, cid)
        if a.nap_bu:
            with conn.cursor() as cur:
                cur.execute("SELECT count(*) FROM fls_run"
                            " WHERE run_id LIKE %s", ("NAP-%-BU%",))
                rid = _run_id_bu(cid, cur.fetchone()[0] + 1)
        else:
            rid = _run_id(cid)
        print(f"kho THAT · anh Bank #{cid} · {len(sids)} nguon · run {rid}")

        yc = YeuCau(conn=conn, pv=chi_nap_that(), q={}, tham={},
                    actor=ACTOR_DUNG_LAI_SO,
                    than={"chup_id": cid, "source_ids": sids, "run_id": rid})
        bb, _ = nap_cua.lo_nap(yc)
        _in(bb)

        with conn.cursor() as cur:
            cur.execute("SELECT (SELECT count(*) FROM fls_itl),"
                        " (SELECT count(*) FROM fls_reject),"
                        " (SELECT count(*) FROM fls_moi_noi),"
                        " (SELECT count(DISTINCT source_system) FROM fls_itl)")
            so, rj, noi, tang = cur.fetchone()
    print(f"\nSO: {so:,} dong · loai {rj:,} · moi noi {noi:,} · "
          f"tang nguon {tang}")
    if tang != 1:
        print("⛔ CANH BAO: so co nhieu hon MOT tang nguon (cong `A5a`)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
