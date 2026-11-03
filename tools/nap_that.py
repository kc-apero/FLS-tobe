"""Nap THAT: doc `Transaction Mapping L1` LIVE -> `fls_itl` tren PostgreSQL.

Lan dau kho co du lieu that thay vi vai tram dong test. Chi doc nguon; ⛔ khong
ghi mot o nao ve file ke toan (`QD-ITL-34`), ⛔ khong cham `fps_*`/P100.

Chay:  python tools/nap_that.py [--that]
       khong co `--that` thi CHI DO, khong ghi vao DB.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fls.adapters.bank import kiem_header, nap                    # noqa: E402
from fls.canon.o_loi import la_o_loi                              # noqa: E402
from fls.adapters.pm_join import (PM_DONG_DAU, PM_DONG_TIEU_DE,   # noqa: E402
                                  PM_COT, DongPM, canon_ref,
                                  kiem_tieu_de_pm, loc_tho)
from fls.ledger.build import NgucCanh                             # noqa: E402
from fls.oracle.doc_du import NGUONG_SAN, DemCot, danh_gia        # noqa: E402
from fls.oracle.nguon import BAN_SAO_RAW                          # noqa: E402

SA = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
LO = 2500          # dong moi lat — do duoc ~2,2s/lat, ⛔ khong dat 300s timeout


def _token() -> str:
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA, "--scopes",
         "https://www.googleapis.com/auth/spreadsheets.readonly"],
        capture_output=True, text=True, shell=True)
    if not r.stdout.strip():
        raise SystemExit("khong lay duoc token: " + r.stderr.strip()[:300])
    return r.stdout.strip()


# ⭐⭐⭐ Timeout cua lan `PM` — **DO DUOC**, ⛔ khong doan (09/09).
#
# ⛔⛔ Ban truoc ghim `45` giay cho **moi** lat, va cau van giai thich no la
#    *"tab `[Importrange]` khi lanh co the vuot 45s MOT LAN roi chay binh
#    thuong"*. Do that ngay 09/09 tren dung tab ay: **60s TIMEOUT · 120s OK sau
#    78,7 giay**. ⇒ Gia thiet *"mot lan"* **SAI**: no vuot 45s **moi lan**, va
#    ba lan thu deu timeout ⇒ `doc_pm` **⛔ khong the chay** — tuc bo nap lenh
#    chi duy nhat cua he **dang hong tren sheet song**, va ⛔ khong ai biet vi
#    ⛔ khong ai chay no tu 27/08.
#
# ⇒ Lan `PM` doi mot timeout rieng. ⛔ Va lan `Bank` **giu 45**: cau van cua no
#   *("⛔ khong 300s")* co ly le rieng — mot lat bank cham la mot dau hieu, con
#   mot lat PM cham la **binh thuong** (`IMPORTRANGE` keo tu mot workbook khac).
CHO_PM = 180
CHO_MAC_DINH = 45


def _lat(tok: str, rng: str, lan: int = 3,
         cho: int = CHO_MAC_DINH) -> list[list]:
    """Mot lat. ⚠ `timeout` mac dinh 45s, ⛔ khong 300s.

    Co RETRY vi tab `[Importrange]` khi "lanh" co the vuot 45s mot lan roi chay
    binh thuong. ⛔ Nhung retry ⛔ khong duoc lam thay viec cua timeout: gap
    timeout 3 lan thi NO TO, khong tra lat rong — mot lat rong di qua im lang la
    dung cai da lam cong parity NOI DOI.

    ⚠ `cho` — xem `CHO_PM`: gia thiet *"vuot 45s mot lan"* da bi phep do lat.
    """
    url = (f"https://sheets.googleapis.com/v4/spreadsheets/"
           f"{BAN_SAO_RAW.spreadsheet_id}/values/" + urllib.parse.quote(rng)
           + "?valueRenderOption=UNFORMATTED_VALUE&majorDimension=ROWS")
    q = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    for i in range(1, lan + 1):
        t = time.time()
        try:
            v = json.load(urllib.request.urlopen(q, timeout=cho)).get("values", [])
        except Exception as e:                       # timeout · 500 · 503
            print(f"  {rng:34s} lan {i}/{lan} LOI {type(e).__name__}", flush=True)
            if i == lan:
                raise SystemExit(f"⛔ doc {rng} that bai {lan} lan: {e}")
            continue
        print(f"  {rng:34s} {len(v):6d} dong  {time.time() - t:.1f}s", flush=True)
        return v
    raise SystemExit("khong the toi day")


def doc_nguon(tok: str) -> tuple[list, list[list]]:
    s, d0 = BAN_SAO_RAW.sheet, BAN_SAO_RAW.dong_dau
    hdr = _lat(tok, f"'{s}'!A3:AL3")
    hang: list[list] = []
    lo = d0
    while True:
        v = _lat(tok, f"'{s}'!A{lo}:AL{lo + LO - 1}")
        if not v:
            break
        hang.extend(v)
        if len(v) < LO:
            break
        lo += LO
    return (hdr[0] if hdr else []), hang


# (chu cai cot canon, ten trong NGUONG_SAN, vi tri 0-based)
COT_THEN_CHOT = (
    ("S", "S · Budget Code (hd)", 18),
    ("H", "H · Payment Type", 7),
    ("T", "T · CDT1", 19),
    ("AB", "AB · svc_start", 27),
    ("AC", "AC · svc_end", 28),
    ("Y", "Y · ID Payee", 24),
)


def _cot_rieng(tok: str, chu: str, tu: int, den: int) -> int:
    """Doc MOT cot bang mot cau rieng, dem o co gia tri. ⛔ Lan doc DOC LAP."""
    rng = f"'{BAN_SAO_RAW.sheet}'!{chu}{tu}:{chu}{den}"
    url = (f"https://sheets.googleapis.com/v4/spreadsheets/"
           f"{BAN_SAO_RAW.spreadsheet_id}/values/" + urllib.parse.quote(rng)
           + "?valueRenderOption=UNFORMATTED_VALUE&majorDimension=COLUMNS")
    q = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    v = json.load(urllib.request.urlopen(q, timeout=45)).get("values", [[]])
    o = v[0] if v else []
    return sum(1 for x in o if x not in (None, "") and not la_o_loi(x))


def cong_doc_du(tok: str, hang: list[list]) -> None:
    """⛔ CHAN truoc khi ghi. Mot lat HOP LE van co the THIEU GIA TRI.

    Lan nap 27/08 ghi **257 gia tri `svc_start` it hon** chinh du lieu do, va
    khong cong nao bao gi: header dung, so dong dung, 0 loi HTTP. Cong nay doc
    lai sau cot then chot bang **cau rieng theo COT** roi so so o co gia tri.
    """
    d0 = BAN_SAO_RAW.dong_dau
    den = d0 + len(hang) - 1
    dem = []
    for chu, ten, vt in COT_THEN_CHOT:
        lat = sum(1 for r in hang
                  if vt < len(r) and r[vt] not in (None, "") and not la_o_loi(r[vt]))
        rieng = _cot_rieng(tok, chu, d0, den)
        dem.append(DemCot(ten, lat, rieng, NGUONG_SAN[ten]))
        dau = "OK " if lat == rieng and lat >= NGUONG_SAN[ten] else "⛔ "
        print(f"  {dau}{ten:24s} theo HANG {lat:6d} · theo COT {rieng:6d}"
              f" · san {NGUONG_SAN[ten]}", flush=True)
    px = danh_gia(dem, dong_doc=len(hang), dong_toi_thieu=9_000)
    print(px.bao())
    if not px.dat:
        raise SystemExit("⛔ cong doc-du KHONG DAT — ⛔ khong ghi mot dong nao")


def doc_pm(tok: str) -> list[DongPM]:
    """Doc `[Importrange]PM_Unpivot`. ⚠ Tieu de o dong 2, du lieu tu dong 3.

    ⭐⭐ **SUA 2026-09-11 — owner chot "co luu dong tho".** Truoc do ham nay
      chi dung 8 truong da phan tich va **vut 20 cot con lai ngay luc doc**,
      nen them mot truong hien thi ve sau thi ⛔ khong bu nguoc duoc cho 3.772
      dong dang co. Nay moi dong mang them `tho` = **ca hang**, khoa theo TEN.

    ⛔ Ban den rieng tu chuyen ve `pm_join.PM_COT_RIENG_TU` — **mot cho**:
      `Email Address` **CAM** *(viec ghep ⛔ khong dung den no mot lan nao)*;
      `Ten tai khoan` **GIU**, vi 535 dong ⛔ khong co so chung tu **chi tra
      duoc bang no** — owner quyet 11/09.
    """
    from decimal import Decimal
    tab = "[Importrange]PM_Unpivot"
    hdr = _lat(tok, f"'{tab}'!A{PM_DONG_TIEU_DE}:AC{PM_DONG_TIEU_DE}",
               cho=CHO_PM)
    kiem_tieu_de_pm(hdr[0] if hdr else [])
    print(f"cong hinh dang PM: XANH ({len(hdr[0])} cot)")

    hang: list[list] = []
    lo = PM_DONG_DAU
    while True:
        v = _lat(tok, f"'{tab}'!A{lo}:AC{lo + LO - 1}", cho=CHO_PM)
        if not v:
            break
        hang.extend(v)
        if len(v) < LO:
            break
        lo += LO

    def g(r, k):
        j = PM_COT[k]
        return r[j] if j < len(r) else None

    def _chu(v):
        """O -> chuoi da cat, hoac `None`. ⛔ Chuoi rong ⛔ KHONG phai '' — no
        la **KHONG BIET** (`INV-I16`), va '' se lam moi phep dem sai."""
        if v in (None, ""):
            return None
        return str(v).strip() or None

    def so(v):
        if v in (None, ""):
            return None
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        try:
            return Decimal(str(v).strip().replace(",", ""))
        except Exception:
            return None

    ra = []
    for i, r in enumerate(hang):
        ra.append(DongPM(
            dong_sheet=PM_DONG_DAU + i,
            slip=str(g(r, "slip") or "").strip(),
            line=str(g(r, "line") or "").strip(),
            tien=so(g(r, "tien")),
            cur=str(g(r, "cur") or "").strip(),
            status=str(g(r, "status") or "").strip(),
            ref=canon_ref(g(r, "ref")),
            hd=str(g(r, "hd") or "").strip() or None,
            cdt1=str(g(r, "cdt1") or "").strip() or None,
            ref_tho=(lambda x: None if x in (None, "") else str(x).strip() or None)(
                g(r, "ref")),
            # ⭐ CA HANG, khoa theo TEN COT — tru ban den rieng tu.
            tho=loc_tho(hdr[0] if hdr else [], r),
            # ⭐⭐ Bay khoa PE/PI len KIEU (2026-09-17). `pe_loai` do MA NAY
            #   sinh, ⛔ khong doc thang: nguon de no o HAI cot rieng
            #   (`Advance` / `Urgent`) va dong nao cung chi co mot.
            pe_slip=_chu(g(r, "pe_slip")),
            pe_line=_chu(g(r, "pe_line")),
            pe_loai=("Advance" if _chu(g(r, "pe_adv"))
                     else "Urgent" if _chu(g(r, "pe_urg")) else None),
            pi_slip=_chu(g(r, "pi_slip")),
            pi_line=_chu(g(r, "pi_line"))))
    co_tho = sum(1 for x in ra if x.tho)
    print(f"PM: {len(ra)} dong · {sum(1 for x in ra if x.ref)} dong co ma"
          f" · {co_tho} dong giu duoc hang tho")
    return ra


def main() -> int:
    that = "--that" in sys.argv
    tok = _token()
    print(f"doc {BAN_SAO_RAW.ma} · {BAN_SAO_RAW.sheet} (live)")
    header, hang = doc_nguon(tok)

    kiem_header(header)                       # ④ nguon doi hinh dang => NO TO
    print(f"cong hinh dang nguon: XANH ({len(header)} cot khop ITL-CANON)")

    print("\ncong DOC-DU (mot lat hop le van co the thieu gia tri):")
    cong_doc_du(tok, hang)

    ra, loai, tk = nap(hang, header=header)
    print(f"ba duong cua adapter: vao {tk.vao} = canon {tk.ra} + loai {tk.loai}"
          f" + rong {tk.rong}  ·  can={tk.can()}")
    if not tk.can():
        print("⛔ ba duong khong can — DUNG")
        return 2
    for dong, ly in loai[:5]:
        print(f"   loai dong {dong}: {' | '.join(ly)[:100]}")

    print()
    pm = doc_pm(tok)
    from fls.adapters.pm_join import GHEP_DUOC, TEN_HINH, xep_ca_lat
    from fls.repo.chay_nap import _bank_tu_canon
    from fls.ledger.build import NgucCanh as _NC
    _nc0 = _NC("do", "v1.0", "v1.0", "v1.0", BAN_SAO_RAW.ma, BAN_SAO_RAW.sheet)
    _nhom, tkg = xep_ca_lat(_bank_tu_canon(ra, _nc0), pm)
    print("\nBAC THANG GHEP PM (do that):")
    for h in sorted(tkg.dong_theo_hinh):
        d = tkg.dong_theo_hinh[h]
        dau = "GHEP  " if h in GHEP_DUOC else "NGUOI "
        print(f"  {dau} {h}  {d:6d} dong · {tkg.theo_hinh[h]:5d} ma   {TEN_HINH[h]}")
    print(f"  ---   khong co ma          {tkg.khong_co_ma:6d} dong")
    print(f"  ---   khong thay ma PM     {tkg.khong_thay_ma_PM:6d} dong")
    print(f"  bon duong can = {tkg.can()}")

    if not that:
        print("\n(CHI DO — them --that de ghi vao DB)")
        return 0

    import os

    import psycopg

    from fls.repo.chay_nap import chay
    dsn = os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")
    run_id = f"NAP-{date.today().isoformat()}-{BAN_SAO_RAW.ma}"
    nc = NgucCanh(run_id, "v1.0", "v1.0", "v1.0", BAN_SAO_RAW.ma, BAN_SAO_RAW.sheet)
    t = time.time()
    with psycopg.connect(dsn, autocommit=True) as conn:
        kq = chay(conn, hang, nc, header=header, pm=pm)
    print(f"\n{kq.bao()}    ({time.time() - t:.1f}s)")
    print(f"can() = {kq.can()}")
    for k, v in sorted(kq.ly_do_loai.items(), key=lambda x: -x[1]):
        print(f"   loai vi {k}: {v}")
    return 0 if kq.can() else 3


if __name__ == "__main__":
    raise SystemExit(main())
