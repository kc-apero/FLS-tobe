"""ANH LENH CHI DANG HIEU LUC — mot ban khai duy nhat cho ca ba noi doc no.

⛔⛔⛔ **Module nay ra doi tu mot PHEP DO, va phep do lat mot tien de cua lo
   trinh.** Moc `A3` duoc dat ra de mo duong nap lenh chi cho moi — dich la
   **6.577 dong** tien co ma chung tu ma ⛔ khong dong lenh nao mang ma ay.
   Nhung phep ghep cu loc dong lenh bang `l.run_id = <run_id CUA DONG TIEN>`.

   Do that 09/09 tren kho test *(⛔ khong doan, ⛔ khong doc ma roi ket luan)*:
   nap mot dong lenh mang **dung ma tham chieu** vao mot `run_id` **moi** ⇒
   `ung_vien_pm` tra **0 ung vien**, va `anh_chup.so_dong` = **0**. Nap **cung
   dong lenh ay** vao `run_id` **cua dong tien** ⇒ **1 ung vien, bac `ma`**.

   ⇒ Neu ⛔ khong sua cho nay thi `A3` se **chay xong, bao thanh cong, va
     ⛔ khong lam dich mot dong nao**: con so 6.577 dung yen. Dung lop
     *"xanh tren tap rong"* ma luat nen cua du an dat ra de chan.

★ **Luat moi:** phep ghep nhin **anh PM DOC GAN NHAT trong pham vi**, ⛔ khong
  nhin anh cua lan nap dong tien.

  ⚠ Va no ⛔ **KHONG** lam dut vet truy — no lam vet **RO HON**. Truoc day
  `fls_pm_link.run_id` mang `run_id` cua **dong tien**, va nguoi doc phai
  **suy** rang anh PM cung la anh ay *(dung, nhung chi vi hom nay ITL va PM
  duoc nap CUNG mot lan)*. Nay cot ay mang **chinh anh PM da dung** ⇒ cau
  *"moi noi nay dung anh nao"* co **cau tra loi ghi thang trong so**, ⛔ khong
  con la mot phep suy.

  ⚠ Va du lieu cu ⛔ **khong can va**: hom nay `run_id` cua ITL **bang** `run_id`
  cua PM *(ca hai deu `NAP-2026-08-27-RAW`)*, nen 2.745 moi noi cu **dung theo
  ca hai cach doc**.

⛔⛔ **Vi sao chi lay MOT anh — anh MOI NHAT — chu ⛔ khong lay HET.** Cung mot
   `pm_line_id` co mat trong **moi** anh chup *(anh chup la ban chep lai ca
   sheet)*, nen doc het cac anh se sinh **N ung vien y het nhau** cho mot dong
   tien, va nguoi go phai chon giua ba ban sao cua cung mot dong lenh.
   ⭐ Va anh moi nhat la **su that hien tai cua sheet**: mot dong lenh da bi
   huy thi no ⛔ khong con trong anh moi ⇒ no ⛔ khong con la ung vien. Dung.

   ⚠ Moi noi CU ⛔ khong he bi anh huong: `fls_moi_noi` noi theo `pm_line_id`,
   ⛔ khong theo `run_id` — nen mot dong da ghep tu anh cu **van la da ghep**,
   va no hien `da_ghep` khi gap lai trong anh moi.

⛔⛔ **PHAM VI la doi so BAT BUOC, va day la cho no quan trong nhat trong ca
   he.** Truoc day phep loc dong lenh **ngam** duoc bao ve: no bam theo
   `i.run_id`, ma cau doc dong tien da qua `PhamVi` roi. Nay no tu chon mot
   anh ⇒ **⛔ khong con cai bao ve ngam ay**. Mot lan nap TEST co `read_at` moi
   hon se thanh *"anh dang hieu luc"* va **dong lenh test se hien ra man hinh
   that** — dung cai 1.204 dong dau test da lam mot lan (`pham_vi.py`).
"""
from __future__ import annotations

from typing import Any, Sequence

from fls.adapters.pm_join import DongPM
from fls.repo.pham_vi import PhamVi

# ⭐ Lan thu BA cua anh chup — `Bank` · `Cash` · **`PM`** (`QĐ-ITL-119`).
#   ⛔ Khai o day chu ⛔ khong o `chup.py`: `chup.py` la tang GHI anh chup, con
#   ten lan la mot su that ma **ca tang doc** can *(cau "anh PM nao dang hieu
#   luc" ⛔ khong duoc phep import tang ghi)*.
LAN_PM = "PM"

# ⚠ `max(read_at)` chu ⛔ khong `max(run_id)`: `run_id` mang NGAY trong ten nen
# no **trong nhu** sap xep duoc theo thu tu thoi gian, va no se sai ngay lan dau
# co hai anh trong cung mot ngay — im lang, va theo huong chon anh **cu hon**.
_SQL = """
SELECT l.run_id
  FROM fls_pm_line l
 WHERE {dk}
 GROUP BY l.run_id
 ORDER BY max(l.read_at) DESC, l.run_id DESC
 LIMIT 1
"""


def anh_pm_hieu_luc(conn, pv: PhamVi) -> str | None:
    """`run_id` cua anh PM **doc gan nhat** trong pham vi. `None` = ⛔ khong co.

    ⛔ `None` ⛔ **khong** duoc doc thanh *"0 ung vien"* mot cach im lang: no
    nghia la **⛔ chua ai nap dong lenh nao**, va man hinh phai noi ra dieu do
    *(mot man hien "⛔ khong co ung vien" tren mot kho ⛔ khong co dong lenh
    nao dang tra loi mot cau hoi KHAC)*.
    """
    dk, ts = pv.dieu_kien("l.run_id")
    with conn.cursor() as cur:
        cur.execute(_SQL.format(dk=dk), ts)
        r = cur.fetchone()
    return None if r is None else r[0]


# ---- doc dong lenh cua MOT anh -------------------------------------------
#
# ⛔⛔⛔ **Vi sao ham nay ra doi, 2026-09-10.** Cua nap CA LO (`lo_nap`,
#    `QĐ-ITL-111`) goi `chay()` **⛔ khong truyen `pm`** ⇒ mot so dung lai qua
#    cua ay co **⛔ 0 moi noi**. Trong khi do 2.745 moi noi dang co trong kho
#    that duoc sinh boi `tools/nap_that.py`, thu doc PM **SONG tu Sheets**.
#
#    ⇒ Neu ⛔ khong co ham nay thi "dung lai so" **doi 2.745 moi noi MAY ghep
#      thanh 2.745 cu bam TAY** — mot buoc lui ⛔ khong ai khai.
#
# ⭐ Va no doc **tu ANH CHUP trong kho**, ⛔ khong doc song tu Sheets:
#   `QĐ-ITL-61` da loai duong doc-song (timeout 3/3 lan), va `anh_pm_hieu_luc`
#   o tren la **mot ban khai duy nhat** cho cau *"anh PM nao dang hieu luc"*.
#   Mot duong doc thu hai la mot cho de hai duong lech nhau.
_SQL_DONG = """
SELECT l.source_row, l.pm_slip_id, l.pm_line_id, l.amount, l.curr,
       l.status, l.ref_canon, l.hd, l.cdt1, l.ref_tho
  FROM fls_pm_line l
 WHERE l.run_id = %s
 ORDER BY l.source_row
"""


def _dong(r: Sequence[Any]) -> DongPM:
    return DongPM(dong_sheet=r[0], slip=r[1] or "", line=r[2] or "",
                  tien=r[3], cur=r[4] or "", status=r[5] or "",
                  ref=r[6], hd=r[7], cdt1=r[8], ref_tho=r[9])


def doc_dong_pm(conn, run_id: str) -> list[DongPM]:
    """Dong lenh cua anh `run_id`, dung khuon `DongPM` ma phep ghep doi.

    ⛔ `ref` lay **`ref_canon`** *(da chuan hoa luc nap)*, ⛔ KHONG goi
    `canon_ref` lai o day: chuan hoa hai lan o hai cho la hai cho de lech, va
    `ref_tho` duoc cho di kem dung de con duong nao muon ban nguyen van.
    """
    with conn.cursor() as cur:
        cur.execute(_SQL_DONG, (run_id,))
        return [_dong(r) for r in cur.fetchall()]
