-- 0024 · `fls_pm_link.run_pm` : MOI NOI NEO VAO ANH LENH CHI
--
-- ⭐⭐⭐ `CR#12` · `GAP-ERD-P0-02` · `BA-05` `DD-I13`.
--
-- ── DO TRUOC KHI KHAI (kho that `fls`, 2026-09-18) ──────────────────────
--     anh PM trong kho                            22
--     dong lenh THAT (`pm_line_id` khac nhau)  3.772
--     dong luu trong `fls_pm_line`            82.984   = 3.772 x 22,0
--     moi noi THAT                             2.262
--     moi noi khi noi bang `pm_line_id` DON   49.764   = 2.262 x 22,0
--
-- ⛔⛔ **Cai bay, va no ⛔ KHONG bao gio bao loi.** `fls_pm_line` co khoa
-- chinh **ghep doi** `(run_id, pm_line_id)` — moi cu chup giu mot ban cua
-- cung mot dong lenh. Mot cau SQL noi `fls_pm_link -> fls_pm_line` bang
-- `pm_line_id` DON van **chay trot lot**, tra ve mot con so **trong hop ly**,
-- va phong len **dung bang SO ANH PM**. So ay **tang moi gio** (nhip chup).
-- Bay nay can HAI lan trong MOT ngay 18/09: `3.486` thay vi `166`, va
-- `49.764` thay vi `2.262`.
--
-- ⛔⛔ **Vi sao ⛔ KHONG dung `run_id` san co lam ve thu hai cua khoa.**
-- No mang **HAI nghia** tuy duong ghi:
--
--     `chay_nap.chen_moi_noi`   ghi `nc.run_id`   = lan NAP
--     `ghi_tay` (ghep tay)      ghi `run_pm`      = anh LENH CHI
--
-- Do tren kho that: ca **2.262** dong deu la lan NAP (`la_anh_pm = false`,
-- `la_run_so = true`) — vi ⛔ chua ai ghep tay lan nao (`hinh='T'` = 0).
-- ⇒ Mot cot hai nghia thi moi cau hoi dat len no deu co **hai** cau tra loi
--   dung, va ⛔ khong ai biet minh dang nhan cai nao.
--
-- ── ⭐ VI SAO LO NAY XUAT HIEN — no ⛔ KHONG phai mot so suat ─────────────
-- `schema.py` khai thang: *"`pm_line_id` -> `fps_pm_line.line_id` ·
-- ⛔ KHONG FK (`QĐ-ITL-45`)"*. `QĐ-ITL-45` (24/08) chot FLS **chi DOC** tu
-- `fps_*` ⇒ ⛔ khong FK sang mot he KHAC — **hoan toan dung luc ay**.
-- ⛔⛔ Nhung `fls_pm_line` ra doi **27/08** (`QĐ-ITL-61`, migration `0011`),
-- **ba ngay sau**: tu hom ay tham chieu ⛔ khong con xuyen he nua.
-- ⇒ **Ly do khong-FK HET HIEU LUC, cau chu thich O LAI** — dung lop loi
--   *"tien de doi o cho khac, phat bieu cu o lai"* da can o `GAP-ERD-P0-01`,
--   `Q2`, va chinh migration `0020`.
--
-- ⚠ **`NULL` duoc, va no co nghia THAT:** *"moi noi sinh truoc 2026-09-18"*.
--   2.262 dong cu ⛔ khong suy nguoc **chac chan** duoc anh PM nao dang hieu
--   luc ngay 10/09 — anh PM som nhat trong kho la `09/09`, va giua no voi
--   luot ghep co nhieu cu chup. Mot `DEFAULT` o day se bien *"⛔ khong biet"*
--   thanh mot lo **doan** (`INV-I16`). ⇒ ⛔ KHONG backfill.
--
-- ── HAI rang buoc, va chung ⛔ KHONG cung suc ───────────────────────────
--
-- ⭐ **`FK -> fls_run` thi CO**, va no **mien phi**: moi dong cu deu `NULL`,
--   ma `NULL` di qua `FOREIGN KEY` ⛔ khong can gi. No ghim duoc mot dieu
--   that: *"`run_pm` phai la mot lan nap CO THAT"*.
--
-- ⛔⛔ **`FK -> fls_pm_line` thi ⛔ KHONG DAT DUOC**, va do ⛔ khong phai luoi:
--   khoa chinh ben ay la **ghep doi** `(run_id, pm_line_id)`, nen mot `FK`
--   dung nghia phai la `(run_pm, pm_line_id) -> (run_id, pm_line_id)`.
--   Dat no **bay gio** thi **2.262 dong cu** — dang mang `run_pm = NULL` va
--   `pm_line_id` co gia tri — se can mot phep **suy** anh PM nao dang hieu
--   luc ngay 10/09. Phep suy ay ⛔ **khong duoc hoa thanh rang buoc cung**
--   (`INV-I16`).
--
-- ⇒ Cho phan ay, bai `tests/db/test_moi_noi_neo_anh_pm.py` do bang mot **cau
--   dem** *(dong nao DA khai `run_pm` thi `run_pm` ay phai la mot anh PM)* —
--   no **do duoc** ma ⛔ khong chan lan nap nao. `FK` ghep doi de lan sau,
--   khi moi dong deu do duong ghi moi sinh ra.

ALTER TABLE fls_pm_link ADD COLUMN IF NOT EXISTS run_pm text;

ALTER TABLE fls_pm_link DROP CONSTRAINT IF EXISTS fls_pm_link_run_pm_fkey;
ALTER TABLE fls_pm_link
  ADD CONSTRAINT fls_pm_link_run_pm_fkey
  FOREIGN KEY (run_pm) REFERENCES fls_run(run_id);

COMMENT ON COLUMN fls_pm_link.run_pm IS
  'ANH LENH CHI da dung luc ghep (`fls_pm_line.run_id`). NULL = moi noi sinh '
  'truoc 2026-09-18. ⛔ KHONG lay `run_id` thay: cot do mang HAI nghia — '
  'chay_nap ghi lan NAP, ghi_tay ghi anh LENH CHI.';
