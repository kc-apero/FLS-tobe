"""Cong SONG chay tren SO THAT — chung minh G-ORA-LIVE-1/2/3 co song.

Luat du an: cong chua tung thay do la cong chua biet co song. Script nay lam
hai viec trong mot lan chay:
  ① do thuc te tren nguon owner da chot (QD-ITL-50) roi cho ba cong xu -> mong XANH
  ② co tinh lam gia so cho tung cong -> mong DO, va DO CO LY DO BANG CHU

Chi doc. ⛔ Khong ghi mot o nao vao file ke toan (QD-ITL-34).

Chay:  python tools/verify_ora_live.py
Yeu cau: gcloud da dang nhap voi service-account claude-code-access@fpa-t-494007
"""

from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fls.canon.spec import pos_of                                  # noqa: E402
from fls.oracle.nguon import BAN_SAO_RAW, CAM_MO                   # noqa: E402
from fls.oracle.song import DoDuoc, kiem_song, phai_dung           # noqa: E402

SA = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
EPOCH = date(1899, 12, 30)
TAB_NGUON = ("[Importrange]PM_Unpivot", "[Importrange]PE_Unpivot")


def _token() -> str:
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA, "--scopes",
         "https://www.googleapis.com/auth/spreadsheets.readonly"],
        capture_output=True, text=True, shell=True)
    tok = r.stdout.strip()
    if not tok:
        raise SystemExit(f"khong lay duoc token: {r.stderr.strip()[:200]}")
    return tok


def _cot(tok: str, sid: str, rng: str) -> list:
    url = (f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/"
           + urllib.parse.quote(rng)
           + "?valueRenderOption=UNFORMATTED_VALUE&majorDimension=COLUMNS")
    q = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    v = json.load(urllib.request.urlopen(q, timeout=300)).get("values", [[]])
    return v[0] if v else []


def _la_loi(x) -> bool:      # ⛔ dung fls.canon.o_loi.la_o_loi, xem ghi chu duoi
    from fls.canon.o_loi import la_o_loi
    return la_o_loi(x)


def do_that(tok: str) -> DoDuoc:
    """Do dung ba thu ma ba cong can — khong do them cho re."""
    sid, sheet, d0 = (BAN_SAO_RAW.spreadsheet_id, BAN_SAO_RAW.sheet,
                      BAN_SAO_RAW.dong_dau)
    ngay = [x for x in _cot(tok, sid, f"'{sheet}'!A{d0}:A11000")
            if isinstance(x, (int, float))]
    ky = max((EPOCH + timedelta(days=int(x)) for x in ngay), default=None)

    # ty le ghep = so dong co Loai giao dich (cot H, tu PM) tren tong dong
    h = _cot(tok, sid, f"'{sheet}'!H{d0}:H11000")
    ghep = sum(1 for x in h[:len(ngay)] if x not in (None, "") and not _la_loi(x))

    dong, loi = {}, {}
    for tab in TAB_NGUON:
        c = _cot(tok, sid, f"'{tab}'!A3:A6000")
        dong[tab] = sum(1 for x in c if str(x).strip())
        loi[tab] = sum(1 for x in c if _la_loi(x))

    print(f"  dong co ngay        : {len(ngay)}")
    print(f"  ky moi nhat         : {ky}")
    print(f"  dong ghep (cot H)   : {ghep}")
    print(f"  ty le ghep          : {ghep / len(ngay):.1%}" if ngay else "")
    for t in TAB_NGUON:
        print(f"  {t:<26}: {dong[t]} dong, {loi[t]} o loi")
    return DoDuoc(ky_moi_nhat=ky, dong_theo_tab=dong, o_loi_theo_tab=loi,
                  ty_le_ghep=(ghep / len(ngay)) if ngay else None)


def _bao(nhan: str, kq, mong_do: bool) -> bool:
    xau = phai_dung(kq)
    ok = xau is mong_do
    print(f"\n{'PASS' if ok else 'FAIL'} · {nhan} "
          f"(mong {'DO' if mong_do else 'XANH'})")
    for k in kq:
        print(f"     {'DO  ' if k.do else 'xanh'} {k.ma}"
              + (f" — {k.ly_do}" if k.ly_do else ""))
    if mong_do:
        ok = ok and all(k.ly_do.strip() for k in kq if k.do)
    return ok


def main() -> int:
    print("nguon:", BAN_SAO_RAW.spreadsheet_id, "|", BAN_SAO_RAW.sheet,
          f"| dong dau {BAN_SAO_RAW.dong_dau}")
    assert BAN_SAO_RAW.spreadsheet_id not in CAM_MO, "nguon nam trong danh sach CAM"
    assert pos_of("W") == 22, "he toa do canon bi lech"

    print("\n=== ① DO THAT ===")
    d = do_that(_token())
    hom_nay = date.today()
    ok = [_bao("so that", kiem_song(d, hom_nay), mong_do=False)]

    print("\n=== ② CO TINH LAM DO TUNG CONG ===")
    cu = DoDuoc(hom_nay - timedelta(days=400), d.dong_theo_tab,
                d.o_loi_theo_tab, d.ty_le_ghep)
    ok.append(_bao("G-ORA-LIVE-1: so ngung cap nhat 400 ngay",
                   kiem_song(cu, hom_nay), mong_do=True))

    rong = DoDuoc(d.ky_moi_nhat, {t: 0 for t in d.dong_theo_tab},
                  d.o_loi_theo_tab, d.ty_le_ghep)
    ok.append(_bao("G-ORA-LIVE-2: tab nguon rong",
                   kiem_song(rong, hom_nay), mong_do=True))

    phong = DoDuoc(d.ky_moi_nhat, d.dong_theo_tab, d.o_loi_theo_tab, 0.99)
    ok.append(_bao("G-ORA-LIVE-3: ty le ghep phong len 99% "
                   "(dau hieu dang san xuat mac dinh)",
                   kiem_song(phong, hom_nay), mong_do=True))

    print("\n" + "=" * 62)
    print("KET LUAN:", "TAT CA PASS — ba cong da thay DO that mot lan"
          if all(ok) else "CO CHO FAIL")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
