"""Do KHA NANG DOC cua nguon — thay `verify_parity_all.py` (doc live: bat kha thi).

★ Vi sao co file nay thay cho cong parity live. Ngay 2026-08-26 toi viet cong
parity doc LIVE tu `ADJUSTED`. No treo. Toi doan sai ba lan lien:
  ⓐ "lat 2.000 dong qua to"      -> giam con 500. Van treo.
  ⓑ "hinh dang cau hoi sai"      -> thu lat-dong / mot-cot / batchGet nhieu cot.
                                     CA BA treo y het 90s. Khong phai hinh dang.
  ⓒ "chinh minh dang tu chan"    -> kill viec chay nen. Van treo.

Do that moi ra: **doc MOT O cung treo 60s**, o **moi sheet** trong workbook, ca
`values.get` lan `spreadsheets.get?includeGridData`. Nhung `metadata` tra ve
trong **0,6s** va `valueRenderOption=FORMULA` tra ve trong **0,5s**.

⇒ Ket luan: quyen OK, mang OK, code OK. Workbook `ADJUSTED` **khong the tra gia
tri tinh ra** qua API. Cong thuc doc duoc giai thich tai sao:

    A10 = filter(IMPORTRANGE($B$1,$B$2&"!A4:F"), IMPORTRANGE($B$1,$B$2&"!A4:A")>$B$3)

Mot cong thuc mang keo ca vung tu workbook khac. Doc bat ky o nao cung bat ca
workbook tinh lai toan bo — va no khong xong trong thoi gian cho. `GAP-ORA-08`.

Va dieu nay giai thich luon mot ghi chep cu tuong la ngau nhien: *"doc thuc te
chi duoc 4/7 khoi moi buoi, co khoi truot 3/3 lan"*. Khong phai kich thuoc lat.
La may man: lan doc do co gap luc workbook con am hay khong.

Chay:  python tools/do_kha_nang_doc.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fls.oracle.nguon import BAN_SAO_RAW, SO_GOC_ADJUSTED        # noqa: E402

SA = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
CHO = 45          # giay — ⛔ khong dat 300: mot lan cho vo vong x nhieu lat = treo ca gio


def _token() -> str:
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA, "--scopes",
         "https://www.googleapis.com/auth/spreadsheets.readonly"],
        capture_output=True, text=True, shell=True)
    if not r.stdout.strip():
        raise SystemExit(f"khong lay duoc token: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def _goi(tok: str, url: str) -> tuple[bool, float, str]:
    t0 = time.time()
    try:
        d = json.load(urllib.request.urlopen(
            urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"}),
            timeout=CHO))
        return True, time.time() - t0, f"{len(json.dumps(d))} ky tu"
    except Exception as e:                       # noqa: BLE001
        return False, time.time() - t0, f"{type(e).__name__}: {str(e)[:44]}"


def do_mot_nguon(tok: str, nguon, mot_o: str) -> dict:
    sid = nguon.spreadsheet_id
    B = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}"
    r = urllib.parse.quote(f"'{nguon.sheet}'!{mot_o}")
    phep = (
        ("metadata (khong doc o nao)", f"{B}?fields=properties.title"),
        ("MOT O · FORMULA", f"{B}/values/{r}?valueRenderOption=FORMULA"),
        ("MOT O · gia tri da tinh", f"{B}/values/{r}?valueRenderOption=UNFORMATTED_VALUE"),
    )
    print(f"\n=== {nguon.ma} · {nguon.sheet} · o {mot_o} ===")
    kq = {}
    for nhan, url in phep:
        ok, giay, ghi = _goi(tok, url)
        kq[nhan] = ok
        print(f"  {'OK  ' if ok else '[X] '}{nhan:<32}{giay:6.1f}s  {ghi}")
    return kq


def main() -> int:
    tok = _token()
    raw = do_mot_nguon(tok, BAN_SAO_RAW, f"A{BAN_SAO_RAW.dong_dau}")
    adj = do_mot_nguon(tok, SO_GOC_ADJUSTED, f"A{SO_GOC_ADJUSTED.dong_dau}")

    print("\n" + "=" * 64)
    doc_duoc_gia_tri = adj.get("MOT O · gia tri da tinh", False)
    print("KET LUAN:")
    print(f"  RAW  (ban sao)  doc gia tri: "
          f"{'DUOC' if raw.get('MOT O · gia tri da tinh') else 'KHONG'}")
    print(f"  ADJUSTED (goc)  doc gia tri: "
          f"{'DUOC' if doc_duoc_gia_tri else 'KHONG'}"
          f"   (cong thuc: {'DUOC' if adj.get('MOT O · FORMULA') else 'KHONG'})")
    if not doc_duoc_gia_tri:
        print("\n  => `GAP-ORA-08` CON MO. Thuoc chuan phai chay tren HIEN VAT")
        print("     DONG BANG: tests/fixture/itl_ledge_adjustment.json")
        print("     Cach go dut diem: owner tao mot ban 'dan gia tri' cua ITL Ledge")
        print("     (copy -> paste values only) tu FILE GOC. Doc tuc thi, va dung")
        print("     la 'anh chup dong bang tu file goc' ma DoD 5.6 ① yeu cau.")
        return 1
    print("\n  => ADJUSTED da doc duoc gia tri! Xem lai GAP-ORA-08, co the doc live.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
