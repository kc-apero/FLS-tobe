"""⛔ CONG: `Design-F02-Panel/DATA.json` ⛔ khong duoc mang van xuoi that.

⛔⛔ **Vi sao cong nay ton tai.** Tep `DATA.json` la 6 dong THAT rut tu kho, va
no **vao git** roi **duoc dua cho mot phien Claude khac**. `Diễn giải` co the
mang TEN NGUOI — do la ly do ca `sao_luu/` lan `hien_vat/` bi gitignore.

⚠⚠ Va cho de vap la: van xuoi ⛔ **khong chi nam o `memo`**. Mang `canon` cho
lai chinh cau van ay o vi tri **2**, cong voi *Nội dung PE/PI* (**8·9·10**) va
*Ghi chú* (**31**). Scrub `memo` xong ma quen `canon` la de chu ay di ra qua
**cua sau** — dung the nay da xay ra khi dung bo asset (04/09), bat duoc vi
doc lai tep chu ⛔ khong phai vi mot phep thu nao do.

Chay:  python tools/kiem_du_lieu_thiet_ke.py
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
P = (GOC / "docs" / "ITL" / "02_BA" / "Artifacts" / "Design-F02-Panel"
     / "DATA.json")

# ⭐ Moc cua chu TONG HOP. Doi cau tong hop trong `lam_bo_asset` thi doi ca day.
MOC = "Thanh toan dich vu ky thuat"
# ⭐ Vi tri canon mang van xuoi — do bang mat tren `CANON_COLS`.
VAN_XUOI = (2, 8, 9, 10, 31)
# ⛔ Dia chi noi bo ⛔ khong duoc ra khoi cong ty.
CAM = ("drive.google.com", "docs.google.com", "sheets.google.com")


def main() -> int:
    if not P.exists():
        print(f"⛔ ⛔ khong thay tep: {P}")
        return 1
    ds = json.load(io.open(P, encoding="utf-8"))
    loi: list[str] = []

    for r in ds:
        i = r.get("itl_id")
        if not r.get("_van_la_tong_hop"):
            loi.append(f"{i}: thieu co `_van_la_tong_hop` — ⛔ khong ai biet "
                       f"chu nay la that hay tong hop")
        m = r.get("memo")
        if isinstance(m, str) and m and not m.startswith(MOC):
            loi.append(f"{i}: `memo` VAN LA CHU THAT")
        cn = r.get("canon") or []
        for k in VAN_XUOI:
            v = cn[k] if k < len(cn) else None
            if isinstance(v, str) and v and not v.startswith(MOC):
                loi.append(f"{i}: canon[{k}] VAN LA CHU THAT -> {v[:40]!r}")
        tho = json.dumps(r, ensure_ascii=False)
        for x in CAM:
            if x in tho:
                loi.append(f"{i}: con DIA CHI NOI BO ({x})")

    if loi:
        print("⛔ CONG DO — bo asset thiet ke dang mang chu that:")
        for x in loi:
            print("   ", x)
        print("\n⇒ Chay lai `lam_bo_asset.py`. ⛔ Dung sua tay `DATA.json`.")
        return 1
    print(f"⭐ CONG XANH — {len(ds)} dong · ⛔ khong con van xuoi that · "
          f"⛔ khong con dia chi noi bo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
