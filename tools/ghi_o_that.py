# -*- coding: utf-8 -*-
"""`D3` — BO VAN CHUYEN THAT cho co che ghi an toan, + **bien ban chay kho**.

    python tools/ghi_o_that.py viec.json                  # CHAY KHO (mac dinh)
    FLS_CHO_GHI_SHEET=1 python tools/ghi_o_that.py viec.json --duyet   # ⛔ GHI

⛔⛔ **HAI khoa, ⛔ khong mot.** Cu ghi chi chay khi co **CA HAI**: co
`--duyet` tren dong lenh **VA** bien moi truong `FLS_CHO_GHI_SHEET=1`.

⚠ Vi sao hai: mot co dong lenh la mot thu **go duoc trong ba giay**, va lich su
du an nay da co mot lan mot cong cu ghi chay tren so THAT vi mot co go quen
*(`verify_cua_ghi.py` phai dat mac dinh sang kho TEST vi dung ly do do)*. Con
day ⛔ **khong co "kho test"**: no ghi vao **trang tinh cua ke toan dang mo**.
⇒ Khoa thu hai nam ngoai dong lenh, nen mot cu dan lenh cu ⛔ khong mo duoc no.

★ Tep `viec.json`:

    {"spreadsheet_id": "1md85t…",
     "khung": [{"tab": "ITL Ledge", "dong_tieu_de": 2, "dong_dau": 3}],
     "viec": [{"tab": "ITL Ledge", "cot_khoa": "ITL ID", "khoa": "ITL-001",
               "cot": "HĐ · Final", "gia_tri_moi": "HD-2026-08"}]}

⛔ **Luat nghiep vu ⛔ khong o day.** Phep giai neo · phep so sanh · bon cong
  tu choi deu o `fls/xuat/ghi_o.py` *(ham thuan, 18 bai kiem)*. Tep nay chi
  lam ba viec: doc ban song, goi ham thuan, va **cho** phep ghi di qua khi ca
  hai khoa da mo.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fls.xuat import ghi_o as g                              # noqa: E402

SA = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
API = "https://sheets.googleapis.com/v4/spreadsheets/"
BIEN_CHO_GHI = g.BIEN_CHO_GHI

DOC = "https://www.googleapis.com/auth/spreadsheets.readonly"
GHI = "https://www.googleapis.com/auth/spreadsheets"


def _token(scope: str) -> str:
    """⚠ Xin **dung** pham vi can. Xin `spreadsheets` cho mot luot chay kho la
    mo mot the ghi duoc ma ⛔ khong ai dinh dung — va mot the nhu the la mot
    the **co the bi dung**."""
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA,
         "--scopes", scope],
        capture_output=True, text=True, shell=True)
    if not r.stdout.strip():
        raise SystemExit("⛔ khong lay duoc token: " + r.stderr.strip()[:300])
    return r.stdout.strip()


def _doc_tab(tok: str, sid: str, tab: str) -> list[list]:
    """Doc **CA tab** — ⛔ khong doc mot khoang.

    ⛔⛔ Doc ca tab la **co y**, va no la mat khac cua cung mot luat: neu ta doc
    `A1:D50` thi ta da **doan** rang dong can tim nam trong 50 dong dau — dung
    cai gia dinh ma co che neo dat ra de bo. Doc ca tab thi phep giai neo thay
    **dung nhung gi chu so dang thay**.
    """
    url = (API + urllib.parse.quote(sid) + "/values/"
           + urllib.parse.quote(tab)
           + "?valueRenderOption=UNFORMATTED_VALUE&majorDimension=ROWS")
    q = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
    return json.load(urllib.request.urlopen(q, timeout=60)).get("values", [])


def _ghi_o(tok: str, sid: str):
    """Tra ve mot ham `ghi(tab, o_a1, gia_tri)` — **mot o mot cu goi**.

    ⚠ ⛔ Khong gom lo (`batchUpdate`) o ban dau: mot cu goi mot o thi khi no
    NO giua duong, bien ban da in ra **noi dung o nao da di qua** — con mot cu
    gom 40 o that bai mot phan la mot trang thai ⛔ khong ai doc duoc.
    """
    def ghi(tab: str, o_a1: str, v: str):
        if not o_a1:
            raise SystemExit("⛔ o dich rong — ⛔ khong duoc goi den day")
        # ⭐ `RAW`, ⛔ khong `USER_ENTERED`: `USER_ENTERED` de Sheets **doan
        #   kieu** — mot ma chung tu `FT25008…` co the thanh so khoa hoc, va
        #   mot chuoi bat dau bang `=` thanh **cong thuc**. Ca hai da co that
        #   trong du an nay (xem `canon_ref`).
        url = (API + urllib.parse.quote(sid) + "/values/"
               + urllib.parse.quote(f"{tab}!{o_a1}")
               + "?valueInputOption=RAW")
        r = urllib.request.Request(
            url, method="PUT",
            data=json.dumps({"values": [[v]]}).encode(),
            headers={"Authorization": "Bearer " + tok,
                     "Content-Type": "application/json"})
        urllib.request.urlopen(r, timeout=60)
    return ghi


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("viec", help="tep JSON: spreadsheet_id · khung · viec")
    p.add_argument("--duyet", action="store_true",
                   help="⛔ KHOA THU NHAT. Con can " + BIEN_CHO_GHI + "=1")
    a = p.parse_args()

    with open(a.viec, encoding="utf-8") as f:
        d = json.load(f)
    sid = d["spreadsheet_id"]
    khung = {k["tab"]: g.KhungTab(**k) for k in d["khung"]}
    ds = [g.MotO(g.Neo(v["tab"], v["cot_khoa"], v["khoa"], v["cot"]),
                 str(v["gia_tri_moi"])) for v in d["viec"]]

    # ⛔ Xin the CHI DOC cho phan doc — ke ca khi sap ghi.
    tok_doc = _token(DOC)
    luoi = {t: _doc_tab(tok_doc, sid, t) for t in sorted(khung)}
    for t, hang in luoi.items():
        print(f"  doc {t!r}: {len(hang)} hang")

    bb = g.lap_bien_ban(luoi, khung, ds)
    print()
    print("══ BIEN BAN CHAY KHO ══")
    for dong in g.van_bien_ban(bb):
        print(" ", dong)
    print()

    # ⛔ Luat HAI KHOA lay tu `fls.xuat.ghi_o` — no co bai kiem o do.
    bien = os.environ.get(BIEN_CHO_GHI)
    co_bien = (bien or "").strip() == "1"
    if not g.hai_khoa_mo(a.duyet, bien):
        print("⛔ CHAY KHO — ⛔ 0 o duoc ghi.")
        print("   khoa 1 `--duyet`:", "MO" if a.duyet else "⛔ DONG")
        print(f"   khoa 2 `{BIEN_CHO_GHI}=1`:",
              "MO" if co_bien else "⛔ DONG")
        # ⛔ Tra `0`: mot luot chay kho la mot luot **THANH CONG**. Tra ma loi
        #   se lam moi bo chay tu dong coi bao cao nay la mot su co.
        return 0

    if bb.tu_choi:
        print(f"⛔ TU CHOI CA LO: {len(bb.tu_choi)} dong ⛔ khong giai ra o "
              f"dich chac chan ⇒ ⛔ 0 o duoc ghi.")
        return 2

    tok_ghi = _token(GHI)
    kq = g.ap_dung(bb, _ghi_o(tok_ghi, sid), duyet=True)
    print(f"✅ da ghi {kq['so_o_da_ghi']} o "
          f"· {kq['so_o_da_dung_roi']} o DA DUNG ROI (bo qua)")
    for o in kq["o"]:
        print(f"   {o['tab']}!{o['o']}  {o['truoc']!r} → {o['sau']!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
