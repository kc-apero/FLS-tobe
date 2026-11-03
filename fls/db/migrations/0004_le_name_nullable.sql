-- 0004_le_name_nullable
--
-- `fls_le.le_name` khai NOT NULL. Nhung nguon KHONG CO ten phap nhan:
--
--   tab 'Mapping Master' > "Mapping LE I Legal Entity" chi co HAI cot:
--       A 'Bank Sheet'  ->  B 'LE'          (ma, khong ten, khong co/khong nhan)
--   canon L 'Phap nhan thanh toan' co ten cho DUNG 5 ma ('VGOH - APERO HQ'…),
--   24 ma con lai khong o dau co ten.
--
-- NOT NULL o day chi con hai duong: hoac lay MA lam ten (bia, va ve sau khong
-- ai phan biet duoc "chua biet ten" voi "ten dung la the"), hoac khong nap duoc
-- dong nao. Ca hai deu te hon mot cot NULL trung thuc (INV-I16 / P-ITL-05).
--
-- GAP-LE-01: danh muc phap nhan chua co nguon co ten + co nhan is_entity.
-- Ung vien khong-phai-phap-nhan da do duoc: 'Cash Treasury' (716 dong),
-- 'HIEPNV' (16), 'SONNH' (5), 'HOATT' (3) — nhung NGUON KHONG NOI, nen
-- ⛔ khong tu gan is_entity=false.

ALTER TABLE fls_le ALTER COLUMN le_name DROP NOT NULL;

COMMENT ON COLUMN fls_le.le_name IS
  'ten phap nhan — NULL khi nguon khong noi (GAP-LE-01), KHONG lay ma lam ten';
