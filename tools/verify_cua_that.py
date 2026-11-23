"""Cong chung #8 cho `P4`: **chay THAT mot lan tren KHO THAT, qua HTTP**.

    PG_DSN=... python tools/verify_cua_that.py

⛔ Mot bo test xanh ⛔ khong chung minh *"du lieu ra duoc qua HTTP"*. Cong nay
dung may that, goi bang HTTP that, doc so THAT, roi **in ra con so** — vi mot
cong khong in ra da do duoc gi thi khong ai biet no co do gi (cong chung #7).

⛔ Mac dinh KHONG DAT. Chi dat khi ca bon dieu chung minh duoc:
  ⓐ `/ledger` tra ve **>= nguong** dong that
  ⓑ `/queue` tra dung **hang + luy ke** va **luy ke tang dan trong tung tien te**
  ⓒ khong dong nao ra ngoai co `run_id` la
  ⓓ `/gates` **khong toan xanh** — bon cong ke toan phai la "chua do duoc"
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import secrets
import sys
import threading
import time
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fls.api import cua, the                                     # noqa: E402
from fls.api.bang_tuyen import TIEN_TO                           # noqa: E402
from fls.db.kho import dsn_that, noi_chi_doc                     # noqa: E402
from fls.repo.danh_muc_actor import ACTOR_VERIFY_CUA_THAT        # noqa: E402
from fls.repo.kho_sach import la_run_that                        # noqa: E402

DONG_TOI_THIEU = 1_000     # duoi nguong nay ⇒ chua do duoc gi, ⛔ khong phai "sach"


def _mo(dsn: str):
    @contextlib.contextmanager
    def mo():
        c = noi_chi_doc(dsn)
        try:
            yield c
        finally:
            c.close()
    return mo


def main() -> int:
    dsn = dsn_that()
    os.environ.setdefault(the.BIEN_KHOA, secrets.token_urlsafe(48))
    may = cua.dung_may(_mo(dsn), cong=0)
    threading.Thread(target=may.serve_forever, daemon=True).start()
    the_thu = the.dong_the(
        {"sub": ACTOR_VERIFY_CUA_THAT, "exp": int(time.time()) + 120}, the.khoa())

    def goi(duong: str) -> tuple[int, dict]:
        c = http.client.HTTPConnection(*may.server_address, timeout=30)
        try:
            c.request("GET", duong, headers={"Authorization": f"Bearer {the_thu}"})
            r = c.getresponse()
            return r.status, json.loads(r.read() or b"{}")
        finally:
            c.close()

    ly_do: list[str] = []
    da_do: list[str] = []
    try:
        print(f"kho: {dsn.rsplit('/', 1)[-1]}  ·  may: "
              f"{may.server_address[0]}:{may.server_address[1]}")

        # ⓐ so
        ma, ra = goi(f"{TIEN_TO}/ledger?limit=500")
        if ma != 200:
            ly_do.append(f"/ledger tra {ma}")
        else:
            n = ra["data"]["count"]
            da_do.append(f"/ledger trang dau {n} dong")
            print(f"  /ledger        {n} dong · pham vi = {ra['meta']['pham_vi']}"
                  f" · {ra['meta']['data_status']}")
            la = [d["run_id"] for d in ra["data"]["rows"]
                  if not la_run_that(d["run_id"])]
            if la:
                ly_do.append(f"/ledger tra {len(la)} dong cua run LA: {set(la)}")
            # ⓒ dem tong bang cach lat het trang
            tong, con = n, ra["data"]["next_cursor"]
            while con:
                ma2, r2 = goi(f"{TIEN_TO}/ledger?limit=500&cursor={con}")
                if ma2 != 200:
                    ly_do.append(f"/ledger trang tiep tra {ma2}")
                    break
                tong += r2["data"]["count"]
                con = r2["data"]["next_cursor"]
            da_do.append(f"lat het {tong} dong")
            print(f"  lat het        {tong} dong (phan trang khoa)")
            if tong < DONG_TOI_THIEU:
                ly_do.append(f"chi doc duoc {tong} dong < nguong "
                             f"{DONG_TOI_THIEU} ⇒ ⛔ chua do duoc gi")

        # ⓑ hang cho
        ma, ra = goi(f"{TIEN_TO}/queue/summary")
        if ma != 200:
            ly_do.append(f"/queue/summary tra {ma}")
        else:
            tt = ra["data"]["theo_tien_te"]
            print("  /queue/summary " + " · ".join(
                f"{x['curr']} {x['so_dong']}" for x in tt))
            da_do.append("hang cho: " + " · ".join(
                f"{x['curr']}={x['so_dong']}" for x in tt))
            if not tt:
                ly_do.append("hang cho rong ⇒ ⛔ khong do duoc phep xep")
            for x in tt:
                ma2, r2 = goi(f"{TIEN_TO}/queue?curr={x['curr']}&den_pct=90"
                              f"&limit=500")
                if ma2 != 200:
                    ly_do.append(f"/queue {x['curr']} tra {ma2}")
                    continue
                d = r2["data"]["rows"]
                pct = [Decimal(r["luy_ke_pct"]) for r in d]
                if pct != sorted(pct):
                    ly_do.append(f"/queue {x['curr']}: luy ke KHONG tang dan")
                if d and d[0]["hang"] != 1:
                    ly_do.append(f"/queue {x['curr']}: hang dau khong phai 1")
                if any(not la_run_that(r.get("run_id", "NAP-2026-01-01-X"))
                       for r in d):
                    ly_do.append(f"/queue {x['curr']}: co dong cua run LA")
                print(f"     {x['curr']:<4} phu 90% tien can {len(d)} / "
                      f"{x['so_dong']} dong")

        # ⓓ cong
        ma, ra = goi(f"{TIEN_TO}/gates")
        if ma != 200:
            ly_do.append(f"/gates tra {ma}")
        else:
            d = ra["data"]
            print(f"  /gates         dat {d['dat']} · khong dat "
                  f"{d['khong_dat']} · CHUA DO DUOC {d['chua_do_duoc']}")
            for c in d["cong"]:
                print(f"     {c['nhan']:<13} {c['ma']:<14} "
                      f"{c['da_do'] or c['ly_do']}")
            da_do.append(f"/gates {len(d['cong'])} cong")
            # ⛔⛔ Lan chay dau (27/08) cong nay in "KHONG DAT BON_DUONG" ma
            # van tra ✅ DAT, vi toi chi kiem `chua_do_duoc`. Mot cong bao mot
            # cong khac do roi tu noi minh dat la cong vo nghia.
            if d["khong_dat"]:
                ly_do.append("co " + str(d["khong_dat"]) + " cong KHONG DAT: "
                             + ", ".join(c["ma"] for c in d["cong"]
                                         if c["dat"] is False))
            if d["chua_do_duoc"] < 5:
                ly_do.append("⛔ /gates bao it hon 5 cong 'chua do duoc' — bon "
                             "cong ke toan + bon duong chua he do, khong duoc "
                             "bien mat")

        # ⓔ' ⭐ GHEP LENH — duong doc ung vien, tren dong THAT trong hang cho.
        #
        # ⛔ Phep kiem nay phai DO DUOC that: mot dong hang cho that, va it nhat
        # mot ung vien co bac `ma` (reference khop). Neu khong co ung vien nao
        # thi khai la **khong do duoc** va cong KHONG DAT — ⛔ khong im lang di
        # qua (cong chung #7). Do chinh la cai bay `verify_cua_ghi.py` da mac
        # mot lan trong ngay: chon dong bat ky roi bao ✅ ma nhanh chinh khong
        # duoc do.
        ma, _r = goi(f"{TIEN_TO}/queue?limit=50")
        d = _r.get("data") or {}
        dong_thu = None
        if ma != 200 or not d.get("rows"):
            ly_do.append(f"/queue tra {ma} — ⛔ khong lay duoc dong nao de thu ghep")
        else:
            thay_bac_ma = 0
            do_duoc = 0
            for x in d["rows"][:25]:
                ma2, _u = goi(
                    f"{TIEN_TO}/queue/{x['itl_id']}/pm-candidates?limit=5")
                u = _u.get("data") or {}
                if ma2 != 200:
                    ly_do.append(f"/pm-candidates tra {ma2} cho itl_id="
                                 f"{x['itl_id']}")
                    break
                do_duoc += 1
                if u.get("anh_chup", {}).get("so_dong", 0) == 0:
                    ly_do.append("⛔ anh chup dong lenh RONG tren kho that ⇒ "
                                 "ghep tay ⛔ khong the co ung vien")
                    break
                if any(y["bac"] == "ma" for y in u.get("ung_vien", ())):
                    thay_bac_ma += 1
                    dong_thu = dong_thu or (x["itl_id"], u)
            if do_duoc:
                da_do.append(f"/pm-candidates do tren {do_duoc} dong that")
                print(f"  /pm-candidates  do {do_duoc} dong hang cho · "
                      f"{thay_bac_ma} dong co ung vien bac `ma`")
            if dong_thu:
                i_, u_ = dong_thu
                bac = " · ".join(f"{y['bac']} {y['pm_line_id']}"
                                 for y in u_["ung_vien"][:3])
                print(f"     itl_id={i_}: {bac}")
                print(f"     anh chup {u_['anh_chup']['so_dong']} dong lenh · "
                      f"doc luc {u_['anh_chup']['doc_luc_muon_nhat']}")
                da_do.append("co dong that tra ung vien bac `ma`")
            elif do_duoc:
                # ⛔ Khai ra la chua do duoc nhanh dang gia nhat.
                ly_do.append(
                    f"⛔ trong {do_duoc} dong hang cho da thu, ⛔ KHONG dong nao "
                    f"co ung vien bac `ma` ⇒ nhanh 'reference khop' KHONG DO "
                    f"DUOC. Day la nhanh chinh cua man F01")

        # ⓔ cua ⛔ khong ghi duoc: mot phuong thuc sua phai bi tu choi
        c = http.client.HTTPConnection(*may.server_address, timeout=10)
        try:
            c.request("DELETE", f"{TIEN_TO}/ledger",
                      headers={"Authorization": f"Bearer {the_thu}"})
            r = c.getresponse()
            r.read()
            if r.status != 405:
                ly_do.append(f"DELETE /ledger tra {r.status}, phai la 405")
            else:
                da_do.append("DELETE /ledger = 405")
                print("  DELETE /ledger 405 (⛔ khong duong ghi nao)")
        finally:
            c.close()

        # ⓕ ⭐ Va tu `P5` tro di: cua nay phai chay o che do CHI DOC, nen MOI
        # duong ghi cung phai tra 405. Day la phep kiem dang gia nhat sau khi
        # nhom ghi ton tai — mot cua doc mo san duong ghi la mot cua doc khong
        # con la cua doc.
        for t_ in cua.bang_tuyen.BANG_TUYEN:
            if not t_.ghi:
                continue
            duong = (t_.duong.replace("{itl_id}", "1")
                     .replace("{adj_id}", "1").replace("{field}", "hd"))
            c = http.client.HTTPConnection(*may.server_address, timeout=10)
            try:
                c.request(t_.phuong_thuc, duong,
                          body=b'{"reason":"cong"}',
                          headers={"Authorization": f"Bearer {the_thu}",
                                   "Content-Type": "application/json"})
                r = c.getresponse()
                r.read()
                if r.status != 405:
                    ly_do.append(f"{t_.phuong_thuc} {duong} tra {r.status}, "
                                 f"phai la 405 — cua doc ⛔ khong duoc mo san "
                                 f"duong ghi")
            finally:
                c.close()
        n_ghi = sum(1 for x in cua.bang_tuyen.BANG_TUYEN if x.ghi)
        da_do.append(f"{n_ghi} duong ghi deu 405")
        print(f"  nhom ghi       {n_ghi} duong deu 405 (che do CHI DOC)")
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
    print("✅ DAT — cua doc chay that tren kho that, qua HTTP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
