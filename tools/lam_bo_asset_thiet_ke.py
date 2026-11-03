"""Rut 6 DONG THAT tu kho -> `DATA.json` cho nguoi thiet ke.

⛔⛔ `Diễn giải` co the mang TEN NGUOI. Tep nay se vao git va se duoc dua cho
mot phien Claude khac ⇒ van xuoi bi **thay bang chu tong hop** giu dung DO DAI
va HINH DANG, ⛔ khong giu noi dung.

⚠⚠ Va no ⛔ **khong chi nam o `memo`**: mang `canon` cho lai chinh cau van ay
o vi tri 2, cong voi *Nội dung PE/PI* (8·9·10) va *Ghi chú* (31). Scrub `memo`
xong ma quen `canon` la de chu ay di ra qua **cua sau**. Hai vi tri dinh kem
(29·30) mang LINK Drive noi bo — cung thay.

⭐ Chon 6 dong theo **6 tinh huong KHAC NHAU** — ⛔ khong lay 6 dong dau, vi 6
dong dau deu giong nhau va nguoi thiet ke se thiet ke cho mot truong hop.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fls.db.kho import dsn_that, noi_chi_doc  # noqa: E402
from fls.repo.doc_bao_cao import doc_mot_dong  # noqa: E402
from fls.repo.pham_vi import chi_nap_that  # noqa: E402

GOC = Path(__file__).resolve().parent.parent
RA = (GOC / "docs" / "ITL" / "02_BA" / "Artifacts" / "Design-F02-Panel"
      / "DATA.json")

# ⭐ 6 tinh huong. Moi cau tra ve MOT `itl_id` — hay ⛔ khong dong nao, va luc
# ay ta phai BIET la ⛔ khong co, chu ⛔ khong lang le bo qua.
TH: tuple[tuple[str, str], ...] = (
    ("sach nhat — da phan loai, co ghep lenh chi",
     "work_status='ok' AND hd IS NOT NULL AND cdt1 IS NOT NULL"
     " AND pm_hinh='A'"),
    ("UNMAPPED — chua ai phan loai (76,6% so la the nay)",
     "work_status='UNMAPPED' AND coalesce(hd,'')=''"),
    ("tien vao (PS No khac 0) — dau NGUOC voi da so",
     "ps_no IS NOT NULL AND ps_no <> 0"),
    ("ngoai te — o `curr` ⛔ khong phai VND",
     "curr <> 'VND' AND work_status='ok'"),
    ("dien giai DAI nhat — thu thach be rong o",
     "length(memo) > 90"),
    ("da co nguoi go tay de len (`*_thyt` khac rong)",
     "coalesce(hd_thyt,'') <> '' OR coalesce(cdt1_thyt,'') <> ''"),
)

# ⭐ Vi tri canon mang VAN XUOI — do bang mat tren `CANON_COLS`:
#    C `Diễn giải` · I/J `Nội dung PE` · K `Nội dung PI` · AF `Ghi chú`.
# ⛔ Danh sach nay phai lon len neu khuon canon lon len.
VAN_XUOI_CANON: tuple[int, ...] = (2, 8, 9, 10, 31)
# ⚠ Hai o dinh kem chua LINK Drive noi bo — thay bang mot dia chi vi du.
LINK_CANON: tuple[int, ...] = (29, 30)

VAN = ("Thanh toan dich vu ky thuat quy IV cho doi tac cung cap ha tang "
       "may chu, hop dong khung nam 2026, dot giai ngan thu hai theo bien "
       "ban nghiem thu so 214 ngay 12 thang 8")


def _thay(v: object) -> object:
    """Giu DO DAI, ⛔ khong giu noi dung."""
    if not isinstance(v, str) or not v:
        return v
    return (VAN * (len(v) // len(VAN) + 1))[:len(v)]


def main() -> None:
    conn = noi_chi_doc(dsn_that())
    pv = chi_nap_that()
    ra: list[dict] = []
    with conn.cursor() as cur:
        for ten, dk in TH:
            cur.execute(
                "SELECT itl_id FROM fls_itl WHERE run_id NOT LIKE %s"
                f" AND ({dk}) ORDER BY itl_id DESC LIMIT 1", ["NAP-2000-%"])
            r = cur.fetchone()
            if not r:
                print(f"  ⛔ KHONG co dong nao cho: {ten}")
                continue
            d = doc_mot_dong(conn, pv, r[0])
            if d is None:
                print(f"  ⛔ ngoai pham vi: {ten}")
                continue

            d["memo"] = _thay(d.get("memo"))
            cn = d.get("canon")
            if isinstance(cn, list):
                for i in VAN_XUOI_CANON:
                    if i < len(cn):
                        cn[i] = _thay(cn[i])
                for i in LINK_CANON:
                    if i < len(cn) and cn[i]:
                        cn[i] = "https://vi-du.noi-bo/tep-dinh-kem"
            if d.get("invoice"):
                d["invoice"] = "https://vi-du.noi-bo/tep-dinh-kem"

            d["_tinh_huong"] = ten
            d["_van_la_tong_hop"] = True
            ra.append(d)
            print(f"  ⭐ {r[0]:>6}  {ten}")

    RA.parent.mkdir(parents=True, exist_ok=True)
    RA.write_text(json.dumps(ra, ensure_ascii=False, indent=1, default=str),
                  encoding="utf-8")
    print(f"\n⭐ {len(ra)} dong -> {RA}")


if __name__ == "__main__":
    main()
