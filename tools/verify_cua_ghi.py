"""Cong chung #8 cho `P5`: **chay THAT ca vong ghi, qua HTTP**.

    python tools/verify_cua_ghi.py                 # tren kho TEST (mac dinh)
    PG_DSN=... python tools/verify_cua_ghi.py --kho-that   # ⛔ tren so THAT

⛔⛔ **Vi sao mac dinh la kho TEST, va vi sao co mot co rieng de sang kho that.**
Cong nay **GHI**. Chay no tren so that se de lai **4 dong vinh vien** trong
`fls_adjustment` + `fls_journal` — va day la cho dang chu y: hai bang do ⛔
**khong co `run_id`**, nen cong `kiem_kho` *(chi soi `run_id`)* se ⛔ **khong
bao gio thay** mot dau vet thu nghiem nam trong do.

Tuc la neu cu chay bua tren so that thi ta tu tao lai dung cai benh da mat mot
ngay de dap: **dau test lan vao so that ma khong cong nao bao gi**. ⇒ Mac dinh
kho TEST; sang so that phai go `--kho-that` tuong minh, va lenh do la quyet
dinh cua chu so, ⛔ khong phai cua may.

★ Vong ghi day du duoc do:
  ⓐ hoi *"nguon dang noi gi"* → ⓑ go khac nguon ⇒ phai **409** →
  ⓒ go lai voi `force` ⇒ **200** → ⓓ nhat ky co du vet →
  ⓔ **dao** but toan ⇒ gia tri **lui ve dung cai cu** →
  ⓕ so `fls_itl` ⛔ **khong doi mot o nao** tu dau den cuoi
"""
from __future__ import annotations

import argparse
import contextlib
import http.client
import json
import os
import secrets
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fls.api import cua, the                                     # noqa: E402
from fls.api.bang_tuyen import TIEN_TO                           # noqa: E402
from fls.db.kho import dsn_test, dsn_that, noi_chi_doc           # noqa: E402
from fls.repo import ghi_tay as gt                               # noqa: E402

# Cac cot cua `fls_itl` PHAI khong doi sau ca vong ghi (`INV-I08`+`QĐ-ITL-35`).
COT_PHAI_GIU = ("hd", "hd_thyt", "pay_type", "pay_type_thyt", "cdt1",
                "cdt1_thyt", "svc_start", "svc_end", "id_payee", "invoice",
                "work_status",
                "period_state", "raw_frozen", "is_flash")


def _mo_doc(dsn: str):
    @contextlib.contextmanager
    def mo():
        c = noi_chi_doc(dsn)
        try:
            yield c
        finally:
            c.close()
    return mo


def _mo_ghi(dsn: str):
    import psycopg

    @contextlib.contextmanager
    def mo():
        c = psycopg.connect(dsn, autocommit=True)
        try:
            yield c
        finally:
            c.close()
    return mo


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kho-that", action="store_true",
                    help="⛔ chay tren SO THAT — de lai 4 dong vinh vien trong "
                         "`fls_adjustment`/`fls_journal`, va hai bang do khong "
                         "co `run_id` nen cong `kiem_kho` khong thay chung")
    ap.add_argument("--truong", default="hd",
                    help="truong de thu. Mac dinh `hd` vi so that CO gia tri o "
                         "cot nay — can the de do duoc nhanh 409 (US-025)")
    a = ap.parse_args()

    dsn = dsn_that() if a.kho_that else dsn_test()
    if a.truong not in gt.TRUONG_GHI:
        print(f"⛔ {a.truong} khong nam trong 10 truong duoc go")
        return 1

    import psycopg

    # ⛔⛔ Tim mot dong ma truong do CO GIA TRI.
    #
    # Lan chay dau (27/08) cong nay lay dong dau tien bat ky — dong do co
    # `cdt1_cfa1` RONG, nen **nhanh 409 khong duoc do** ma cong van in ✅ DAT.
    # Dung cai benh cong #7 noi: khong do gi thi tat nhien khong thay loi.
    # ⇒ Uu tien dong co gia tri; khong co thi VAN chay nhung ghi ro nhanh 409
    #   **khong do duoc**, va cong KHONG DAT.
    HINH = r"^NAP-\d{4}-\d{2}-\d{2}-[A-Z0-9]+$"
    with psycopg.connect(dsn, autocommit=True) as c:
        r = c.execute(
            f"SELECT i.itl_id FROM fls_itl i WHERE i.run_id ~ %s"
            f" AND i.period_state = 'open' AND i.{a.truong} IS NOT NULL"
            f" ORDER BY i.itl_id LIMIT 1", (HINH,)).fetchone()
        if r is None:
            r = c.execute(
                "SELECT i.itl_id FROM fls_itl i WHERE i.run_id ~ %s"
                " AND i.period_state = 'open' ORDER BY i.itl_id LIMIT 1",
                (HINH,)).fetchone()
        if r is None:
            print(f"⛔ KHONG DAT — kho {dsn.rsplit('/', 1)[-1]!r} khong co dong "
                  f"nao trong pham vi ⇒ ⛔ khong do duoc gi")
            return 1
        i = r[0]
        truoc = c.execute(
            f"SELECT {', '.join(COT_PHAI_GIU)} FROM fls_itl WHERE itl_id=%s",
            (i,)).fetchone()

    os.environ.setdefault(the.BIEN_KHOA, secrets.token_urlsafe(48))
    may = cua.dung_may(_mo_doc(dsn), cong=0, mo_ghi=_mo_ghi(dsn))
    threading.Thread(target=may.serve_forever, daemon=True).start()
    the_thu = the.dong_the(
        {"sub": "cong-ghi@apero.vn", "exp": int(time.time()) + 120}, the.khoa())

    def goi(pt, duong, than=None):
        cl = http.client.HTTPConnection(*may.server_address, timeout=30)
        de = {"Authorization": f"Bearer {the_thu}"}
        body = None
        if than is not None:
            body = json.dumps(than).encode()
            de["Content-Type"] = "application/json"
        try:
            cl.request(pt, duong, body=body, headers=de)
            r = cl.getresponse()
            return r.status, json.loads(r.read() or b"{}")
        finally:
            cl.close()

    ly_do: list[str] = []
    da_do: list[str] = []
    LD = "cong chung #8: thu vong ghi roi dao lai ngay"
    try:
        print(f"kho: {dsn.rsplit('/', 1)[-1]}"
              f"{'  ⛔ SO THAT' if a.kho_that else '  (test)'}"
              f"  ·  dong thu: itl_id={i}  ·  truong: {a.truong}")

        # ⓐ nguon dang noi gi
        ma, ra = goi("GET", f"{TIEN_TO}/ledger/{i}/fields/{a.truong}")
        if ma != 200:
            ly_do.append(f"hoi nguon tra {ma}")
            cu = None
        else:
            cu = ra["data"]["gia_tri"]
            da_do.append(f"nguon={cu!r} ({ra['data']['value_source']})")
            print(f"  ⓐ nguon dang la {cu!r} ({ra['data']['value_source']})")

        moi = "CONG-THU-" + secrets.token_hex(3).upper()

        # ⓑ go khac nguon ⇒ phai 409 (chi kiem duoc khi nguon CO gia tri)
        ma, ra = goi("POST", f"{TIEN_TO}/ledger/{i}/adjust",
                     {"field": a.truong, "value": moi, "reason": LD})
        if cu is not None:
            if ma != 409:
                ly_do.append(f"go khac nguon tra {ma}, phai la 409 (US-025)")
            else:
                da_do.append("409 khi khac nguon")
                print(f"  ⓑ go khac nguon ⇒ 409 · {ra['error'].get('khac')}")
        else:
            # ⛔ Cong chung #7: khai ra la **chua do duoc**, ⛔ khong im lang di qua.
            ly_do.append(
                f"⛔ nhanh 409 (US-025) KHONG DO DUOC: cot `{a.truong}` cua dong "
                f"{i} rong nen khong co gi de xung dot. Chay lai voi `--truong` "
                f"khac, hay tren kho co du lieu that")
            if ma != 200:
                ly_do.append(f"o trong ma go tra {ma}")

        # ⓒ go voi force
        if ma == 409:
            ma, ra = goi("POST", f"{TIEN_TO}/ledger/{i}/adjust?force=true",
                         {"field": a.truong, "value": moi, "reason": LD})
        if ma != 200:
            ly_do.append(f"ghi tra {ma}: {ra.get('error')}")
            adj = None
        else:
            adj = ra["data"]["adj_id"]
            da_do.append(f"ghi duoc adj_id={adj}")
            print(f"  ⓒ ghi duoc · adj_id={adj} · jrn_id={ra['data']['jrn_id']}")

        # ⓓ nhat ky co vet
        ma, ra = goi("GET", f"{TIEN_TO}/journal?itl_id={i}")
        vet = [x for x in ra.get("data", {}).get("rows", [])
               if x.get("reason") == LD]
        if not vet:
            ly_do.append("nhat ky ⛔ khong co vet cua phep ghi vua roi (`AUD-1`)")
        else:
            thieu = [k for k in gt.BAY_TRUONG
                     if k != "value_before" and vet[-1].get(k) in (None, "")]
            if thieu:
                ly_do.append(f"nhat ky thieu truong {thieu} (`AUD-1`)")
            da_do.append(f"nhat ky {len(vet)} vet")
            print(f"  ⓓ nhat ky co {len(vet)} vet · actor={vet[-1]['actor']}")

        # ⓔ dao lai
        if adj:
            ma, ra = goi("POST", f"{TIEN_TO}/adjustments/{adj}/reverse",
                         {"reason": LD + " — dao ngay de so ve nguyen trang"})
            if ma != 200:
                ly_do.append(f"dao tra {ma}: {ra.get('error')}")
            else:
                ma, ra = goi("GET", f"{TIEN_TO}/ledger/{i}/fields/{a.truong}")
                sau = ra["data"]["gia_tri"]
                if sau != cu:
                    ly_do.append(f"sau khi dao, gia tri la {sau!r}, phai lui ve "
                                 f"{cu!r}")
                else:
                    da_do.append("dao lui ve dung gia tri cu")
                    print(f"  ⓔ dao xong · gia tri lui ve {sau!r}")

        # ⓕ so khong doi mot o nao
        with psycopg.connect(dsn, autocommit=True) as c:
            sau_cot = c.execute(
                f"SELECT {', '.join(COT_PHAI_GIU)} FROM fls_itl WHERE itl_id=%s",
                (i,)).fetchone()
        if sau_cot != truoc:
            lech = [f"{k}: {x!r}→{y!r}" for k, x, y
                    in zip(COT_PHAI_GIU, truoc, sau_cot) if x != y]
            ly_do.append("⛔⛔ `fls_itl` BI DOI: " + " · ".join(lech))
        else:
            da_do.append(f"{len(COT_PHAI_GIU)} cot cua so khong doi")
            print(f"  ⓕ so `fls_itl`: {len(COT_PHAI_GIU)} cot ⛔ khong doi mot o")
    finally:
        may.shutdown()
        may.server_close()

    print()
    if not da_do:
        print("⛔ KHONG DAT — khong do duoc gi")
        return 1
    print("da do: " + " · ".join(da_do))
    if ly_do:
        print("⛔ KHONG DAT")
        for x in ly_do:
            print("  - " + x)
        return 1
    print("✅ DAT — vong ghi chay that qua HTTP, va so ⛔ khong doi mot o nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
