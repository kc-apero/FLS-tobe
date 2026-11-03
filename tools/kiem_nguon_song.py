# -*- coding: utf-8 -*-
"""Cong chung #17 — BAY LUAT ve nguon AS-IS, do tren **nguon SONG**.

⚠ So `17` ⛔ khong tu chon: bang cong o `06_ORCHESTRATOR_DASHBOARD` da dung
   toi **#16**. Ban dau toi danh so no la `#14` — trung voi cong *"ban khai
   bang tuyen phai khop SQL that"*. Hai cong cung so la hai cong ⛔ khong
   goi ten duoc.

    PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/kiem_nguon_song.py

⭐⭐ **Vi sao co cong nay.** Nam phep do `Đ2`–`Đ5-b` da lat **ba trong bon bao
   dong lon nhat** cua bo AS-IS, va tim ra **bon thu AS-IS lam dung roi**.
   Nhung ca nam deu **chay bang tay** ⇒ ⛔ **khong mot dong nao cua so doi
   chieu len duoc `K4`**, vi `K4` doi *"da thay do"*. **Mot phep do ⛔ khong tu
   do thi no chua canh gi ca.** Day la cho bien nam phep do thanh **bay cau
   khang dinh se DO** khi so that trot khoi cho.

⛔ **Cong nay ⛔ khong o trong `pytest`, va do la co y.** No doc Google Sheets
   **song** *(~2–4 phut, can `gcloud` + mang)*. Bo test phai chay duoc offline
   va trong vai giay. ⇒ **Luat** nam o `fls/kiem/nguon_song.py` *(thuan)*,
   **bang chung do duoc** o `tests/kiem/test_nguon_song.py` *(offline, moi
   luat co mot ca DO that)*, con day chi la **cai vo I/O**.

⛔⛔ **Luat chung: do duoc 0 thu thi ⛔ KHONG DAT.** Tien le that trong nha:
   hai cong `RUN_ATOMIC` xanh suot hai thang tren 28 vi pham, vi chung loc
   `IS NOT NULL` tren chinh cot chung canh. Xanh tren tap rong la **chua do**.

⛔ Pham vi doc: `QĐ-ITL-92` + `QĐ-ITL-95`. ⛔ Khong doc `Diễn giải` (PII),
   ⛔ khong in noi dung o nao — chi in **so dem**.
"""
from __future__ import annotations

import sys

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from fls.kiem import nguon_song as ns                      # noqa: E402
from tools import do_khoa_ghep as dkg                       # noqa: E402
from tools.do_bat_bien_ngam import BANK, QUY, cot           # noqa: E402
from tools.do_chenh_lech import GOP, GOP_NGAY, GOP_NGUON, GOP_REF  # noqa: E402
from tools.do_chenh_lech import doc_cot                     # noqa: E402
from tools.do_hinh_dang import doc_ban_khai, dong_dau, meta, token  # noqa: E402

CAU = "Bank Transactions_Filter"


def _o(a, i):
    return a[i] if i < len(a) else ""


def thu_thap(tok) -> list[ns.KetQua]:
    kq: list[ns.KetQua] = []

    # ── nguon 1 · `P100 Bank`
    d = meta(BANK, tok)
    ten_r = sorted(s["properties"]["title"] for s in d["sheets"]
                   if s["properties"]["title"].startswith("R |"))
    bang = dong_dau(BANK, ten_r, tok, n=2)
    # ⛔ `doc_ban_khai` nhan **MOT DONG**, ⛔ khong nhan ca bang. Doi chu ky
    #    ma quen cho goi nay => `L1` bao ca 60 sheet **thieu du 6 truong**,
    #    va `L2` do duoc **0**. Cong #17 bat duoc ngay — dung viec cua no.
    khai = {t: doc_ban_khai((bang.get(t) or [[]])[0]) for t in ten_r}
    kq.append(ns.l1_ban_khai_du_6(khai))

    can = [(t, khai[t]["Date"]) for t in ten_r if "Date" in khai[t]]
    c_nhap = doc_cot(BANK, can, tok)
    nhap = {t: len([x for x in c_nhap[(t, i)] if x]) for t, i in can}

    g = doc_cot(BANK, [(GOP, GOP_NGAY), (GOP, GOP_NGUON)], tok)
    g_ngay, g_ng = g[(GOP, GOP_NGAY)], g[(GOP, GOP_NGUON)]
    gop: dict[str, int] = {}
    for i in range(max(len(g_ngay), len(g_ng))):
        if _o(g_ngay, i):
            gop[_o(g_ng, i)] = gop.get(_o(g_ng, i), 0) + 1
    kq.append(ns.l2_nhap_bang_gop(nhap, gop))
    kq.append(ns.l3_xuat_xu_hop_le(gop, set(ten_r)))

    # `Num` — cot H (chi so 7). ⛔ Ma phai doc THO (xem `doc_cot`).
    ma = doc_cot(BANK, [(GOP, GOP_REF)], tok,
                 render="UNFORMATTED_VALUE")[(GOP, GOP_REF)]
    # ⛔⛔ `doc_cot` EP MOI O VE CHUOI ⇒ `Num` het la so, va `l6` dem duoc
    # **0 dong**. Lan chay dau cua chinh cong nay da DO vi le do — nho luat
    # *"do duoc 0 thu ⇒ ⛔ khong dat"*. ⛔ Khong co luat ay thi no da XANH GIA.
    # ⇒ doc `Num` bang `cot()` (giu nguyen kieu).
    num = (cot(BANK, "'%s'!H3:H" % GOP, tok, "UNFORMATTED_VALUE") or [[]])[0]
    kq.append(ns.l6_num_la_thu_tu([str(x).strip() for x in ma], num))

    n_cau = len([x for x in (cot(BANK, "'%s'!A3:A" % CAU, tok,
                                 "UNFORMATTED_VALUE") or [[]])[0] if x != ""])
    kq.append(ns.l7_cau_bang_ban_goc(len([x for x in g_ngay if x]), n_cau))

    # ── nguon 2 · `ITL RAW` — khoa ghep
    k_l1 = [x for x in dkg.lay(dkg.SID, dkg.L1, dkg.L1_KHOA, dkg.L1_DONG1,
                               tok, "UNFORMATTED_VALUE") if x]
    k_pm = [x for x in dkg.lay(dkg.SID, dkg.PM, dkg.PM_KHOA, dkg.PM_DONG1,
                               tok, "UNFORMATTED_VALUE") if x]
    tap = set(k_pm)
    tap_kieu = {(x, dkg.kieu_o(x)) for x in k_pm}
    kq.append(ns.l4_khoa_khong_mat_vi_kieu(
        sum(1 for x in k_l1 if x in tap),
        sum(1 for x in k_l1 if (x, dkg.kieu_o(x)) in tap_kieu),
        len(k_l1)))

    # ── nguon 3 · DANH MUC o `P100` — trong tai TUNG TAI KHOAN, du lieu SONG
    #
    # ⚠ **Doi nguon 2026-09-07 (`QĐ-ITL-101`).** Truoc day `L5` doc dong `226`
    #    cua `2. CCR` ben `A-CCR` — mot con so TONG, tren mot **ban chup chet**
    #    ⇒ mot cong canh tep dong cung thi ⛔ **khong bao gio ban duoc**.
    #    Owner chot ⛔ khong theo duoi ban `A-CCR` song ma **tan dung du lieu
    #    hien co**. ⇒ Trong tai chuyen ve `P100`, noi ke toan **da tu dung san**:
    #      `BankAccountList` cot 9/10  = SUMIFS doc thang sheet `R |`  (SAO KE)
    #                        cot 12/13 = SUMIFS tren `Bank Transactions` (SO)
    #                        cot 14/15 = `=J3=M3` / `=K3=N3`            (CO)
    #    ⭐ Manh hon han ban cu: **N la co thay vi 1 con so**, va **SONG**.
    for ma, sid, sheet, c in (
            ("BNK", BANK, "BankAccountList",
             dict(ten=3, sk_no=9, sk_co=10, so_no=12, so_co=13,
                  co_no=14, co_co=15, tt=18)),
            ("CSH", QUY, "Cash Ledger List",
             dict(ten=1, sk_no=8, sk_co=9, so_no=11, so_co=12,
                  co_no=13, co_co=14, tt=18))):
        v = cot(sid, "'%s'!A3:V" % sheet, tok, "UNFORMATTED_VALUE")

        def C(k, v=v, c=c):
            return v[c[k]] if c[k] < len(v) else []

        ten_c, tt = C("ten"), C("tt")
        n = len([x for x in ten_c if str(x).strip()])
        r_that = {s["properties"]["title"]
                  for s in meta(sid, tok)["sheets"]
                  if s["properties"]["title"].startswith("R |")}

        lech, co, trang, bang = {}, {}, {}, {}
        for k in range(n):
            # ⛔⛔ Khoa phai mang SO DONG. Ban dau toi khoa bang TEN, ma ten
            # thi **co trung va co rong** ⇒ dict **am tham nuot dong**:
            # `L8-CSH` bao 9 tai khoan `Active` trong khi do thang ra **19**.
            # Mot phep dem tren dict khoa bang du lieu nguoi go la mot phep
            # dem ⛔ khong dang tin.
            nhan = "%s#%d %s" % (ma, k + 3, str(ten_c[k]).strip())
            trang[nhan] = str(_o(tt, k)).strip()
            a, b = _o(C("sk_no"), k), _o(C("so_no"), k)
            x, y = _o(C("sk_co"), k), _o(C("so_co"), k)
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                lech[nhan + " Nợ"] = float(a) - float(b)
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                lech[nhan + " Có"] = float(x) - float(y)
            f1, f2 = _o(C("co_no"), k), _o(C("co_co"), k)
            # ⛔ Dong `Active` ma **⛔ khong ten tai khoan** thi ⛔ khong co gi
            # de doi soat ⇒ ⛔ khong dua vao `L8`. No **van bi bat**, nhung o
            # `L9` — dung cho cua no. Moi khuyet tat thuoc **DUNG MOT** luat,
            # neu khong thi thong diep cua ca hai luat deu nhieu.
            # *(Do that o `Cash Ledger List`: dong 8–12 = 5 dong nhu vay.)*
            if str(ten_c[k]).strip():
                co[nhan] = (True if (f1 is True and f2 is True)
                            else False if (f1 is False or f2 is False)
                            else None)
            if trang[nhan].lower() == "active":
                bang[nhan] = str(ten_c[k]).strip()

        kq.append(ns.l5_lech_trong_dung_sai(lech)._replace(
            ten="L5-%s · |lech| < 1.000 VND tung tai khoan" % ma))
        kq.append(ns.l8_co_doi_soat(co, trang)._replace(
            ten="L8-%s · co doi soat cua ke toan phai TRUE" % ma))
        kq.append(ns.l9_danh_muc_khop_sheet(bang, r_that)._replace(
            ten="L9-%s · tai khoan `Active` co sheet `R |` that" % ma))

    return kq


def main() -> int:
    try:
        tok = token()
        kq = thu_thap(tok)
    except Exception as e:                                  # noqa: BLE001
        print("⛔ ⛔ khong DO duoc: %s: %s" % (type(e).__name__, e))
        print("   ⛔ Do khong duoc thi DO, ⛔ khong bo qua (cong chung #7).")
        return 1

    print("=" * 74)
    print("CONG #17 · bay luat ve nguon AS-IS, do tren nguon SONG")
    print("=" * 74)
    for k in sorted(kq, key=lambda x: x.ten):
        print("%s %-46s  %s"
              % ("OK  " if k.xanh else "⛔ ⛔", k.ten, k.thong_diep))
    xau = [k for k in kq if not k.xanh]
    print()
    if xau:
        print("⛔ CONG #17 KHONG DAT — %d/%d luat" % (len(xau), len(kq)))
        return 1
    print("✅ cong #17 DAT — %d luat, va moi luat DA DO duoc that (%s)"
          % (len(kq), " · ".join("%s=%d" % (k.ten.split(" ")[0], k.da_do)
                                 for k in sorted(kq, key=lambda x: x.ten))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
