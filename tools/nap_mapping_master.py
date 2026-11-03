"""Nap `Mapping Master` tu nguon RAW vao kho — dong `GAP-ALLOC-01` phan bo nap.

  python tools/nap_mapping_master.py            # chi DO, ⛔ khong ghi kho
  python tools/nap_mapping_master.py --ghi       # do roi GHI vao kho

⛔ Chi DOC Google Sheets. ⛔ Khong ghi mot o nao vao file ke toan (`QĐ-ITL-34`).
Yeu cau: gcloud da dang nhap voi service-account claude-code-access@fpa-t-494007

★ Vi sao mac dinh la *chi do*: bo nap nay **thay the toan bo** danh muc trong
kho. Mot lan chay nham vao luc nguon dang chap thi... khong sao — ham nap NO
neu danh sach rong. Nhung van de mac dinh la do, vi *"xem truoc roi hay ghi"*
la cach duy nhat de mot nguoi phat hien tab bi doi ten.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fls.adapters.mapping_master import (COT, DONG_DAU, TAB,  # noqa: E402
                                         doc_cot, tom_tat)
from fls.db.kho import dsn_that                               # noqa: E402
from fls.oracle.nguon import BAN_SAO_RAW                      # noqa: E402
from fls.repo.nap_mapping import nap_mapping_master           # noqa: E402

SA = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
HET_DONG = 4464          # so dong that cua tab, do 2026-08-28


def _token() -> str:
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA, "--scopes",
         "https://www.googleapis.com/auth/spreadsheets.readonly"],
        capture_output=True, text=True, shell=True)
    tok = r.stdout.strip()
    if not tok:
        raise SystemExit(f"khong lay duoc token: {r.stderr.strip()[:200]}")
    return tok


def _cot(tok: str, ch: str) -> list:
    """Mot cot THO, tinh tu DONG 1 — de `doc_cot` tu cat theo `DONG_DAU`."""
    url = (f"https://sheets.googleapis.com/v4/spreadsheets/"
           f"{BAN_SAO_RAW.spreadsheet_id}/values/"
           + urllib.parse.quote(f"{TAB}!{ch}1:{ch}{HET_DONG}")
           + "?valueRenderOption=UNFORMATTED_VALUE&majorDimension=COLUMNS")
    q = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    v = json.load(urllib.request.urlopen(q, timeout=300)).get("values", [[]])
    return v[0] if v else []


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true",
                   help="ghi vao kho THAT (mac dinh chi do)")
    a = p.parse_args(argv)

    print(f"doc  {BAN_SAO_RAW.spreadsheet_id[:14]}… · tab {TAB!r} · "
          f"tu dong {DONG_DAU}")
    tok = _token()
    tho = {ch: _cot(tok, ch) for ch in COT}
    dong, loai = doc_cot(tho)

    t = tom_tat(dong)
    print(f"\ndo duoc: {t['ma']} ma `hd`"
          f" · can phan bo {t['can_phan_bo']}"
          f" · co phuong phap {t['co_phuong_phap']}"
          f" · METHOD RONG {t['method_rong']} (sheet hien `0`, ⛔ khong 'No need')"
          f" · code_hr {t['co_code_hr']}"
          f" · coa1 {t['co_coa1']} · coa2 {t['co_coa2']}")
    if loai:
        print(f"\nBI LOAI {len(loai)} dong — moi cai co LY DO:")
        for x in loai[:10]:
            print(f"   dong {x.dong_sheet}: {x.hd_code!r} — {x.ly_do}")
    else:
        print("\nbi loai: 0 dong")

    if not a.ghi:
        print("\n⛔ CHUA GHI (mac dinh). Them `--ghi` de nap vao kho that.")
        return 0

    import psycopg
    with psycopg.connect(dsn_that(), autocommit=True) as c:
        kq = nap_mapping_master(c, dong, bi_loai=len(loai))
    print(f"\nDA GHI kho that: xoa {kq.da_xoa} · chen {kq.da_chen} · "
          f"loai {kq.bi_loai}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
