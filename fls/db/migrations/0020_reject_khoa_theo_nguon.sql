-- 0020 · `fls_reject` khoa theo (run_id, source_sheet, source_row) — cong
--        chung #3: *"0 dong roi im lang"*.
--
-- ⛔⛔⛔ **MOT CHOT CHONG TRUNG DUNG, DAT SAI CHO, THANH MOT DUONG MAT DU LIEU.**
--
-- Khoa cu `UNIQUE (run_id, source_row)` sinh ra o `0007` vi mot loi THAT: chay
-- lai nhan ban `fls_reject` thanh **76 dong cho 19 dong loai that**. Luc ay
-- **mot lan nap = MOT nguon**, nen `source_row` la duy nhat trong mot `run_id`.
--
-- ⭐ `QĐ-ITL-111` (08/09) dung **cua nap CA LO**: *mot* `run_id` cho **59
--   nguon**. Tien de ay bien mat, va ⛔ **khong ai sua khoa**. `source_row` chi
--   la **chi so dong TRONG MOT SHEET**, nen dong 0 cua 59 sheet la 59 lan cung
--   mot gia tri ⇒ chi nguon **DEN TRUOC** duoc ghi, 58 nguon con lai bi
--   `WHERE NOT EXISTS` **nuot trong im lang** *(rowcount 0, ⛔ khong loi)*.
--
-- ── Phep do 2026-09-10, kho nhap `fls_dung`, anh THAT `chup_id 24033` ──
--
--   anh                                         : 8.406 dong
--   vao so                                      : 6.617
--   ghi duoc vao `fls_reject`                   : 1.143
--   ⛔ BI LOAI MA ⛔ KHONG CO BAN GHI NAO        : ⛔ **646 dong**
--   ⇒ trai tren                                 : ⛔ **23 nguon**, chi **11**
--                                                 nguon co ban ghi
--
--   ⭐ Dau van tay cua khoa: **1.143 ban ghi tren dung 1.143 gia tri
--     `source_row` KHAC NHAU TUYET DOI** — mot chuoi ⛔ khong the tu nhien.
--
-- ⇒ Them `source_sheet` vao khoa. `run_id` van o trong khoa nen tinh chat
--   **chay lai ⛔ khong nhan ban** *(ly do `0007` ra doi)* duoc giu nguyen.
--
-- ⚠ `fls_pm_line` mang **cung mot hinh khoa** `(run_id, source_row)`. Hom nay
--   no AN TOAN vi lan `PM` chi co **mot** nguon; nhung day la **cung mot bay
--   dang mo**, va no se sap dung ngay lan dau co nguon thu hai. Da khai:
--   `GAP-NAP-03`.

ALTER TABLE fls_reject
  DROP CONSTRAINT IF EXISTS fls_reject_run_id_source_row_uq;

ALTER TABLE fls_reject
  ADD CONSTRAINT fls_reject_run_id_source_sheet_source_row_uq
  UNIQUE (run_id, source_sheet, source_row);
