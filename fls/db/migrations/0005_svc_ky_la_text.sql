-- 0005_svc_ky_la_text
--
-- `svc_start`/`svc_end` (+ ban `_thyt`) khai la `date`. SAI, va lan nap THAT
-- dau tien do ngay tai day:
--
--     DatetimeFieldOverflow: date/time field value out of range: "202412"
--
-- Do tren 9.967 dong cua so (`itl_ledge_adjustment.json`):
--   svc_start · 39 gia tri khac nhau · 30 dang YYYYMM · 9 dang KHAC
--   svc_end   · 57 gia tri khac nhau · 47 dang YYYYMM · 10 dang KHAC
--   dang KHAC that su co trong so: 'thang 5' · 'Thang 4' · 'TPCI' · '2025.07'
--                                  '20509' · '252512' · '2027' · '45962'
--
-- ⇒ Hai cot nay la o NGUOI GO, don vi la KY (thang), khong phai ngay. Kieu
--   `date` sai HAI lan:
--     ① no buoc phai bia mot NGAY trong thang ma nguon khong he co (INV-I16);
--     ② no lam NO tren 9-10 loai gia tri ma ke toan THAT SU da go — tuc bat
--        chinh chu so phai "sua lai cho dung kieu", va cai sua do khong con
--        duong quay ve.
--
-- Chep nguyen van (kieu `text`) roi phan loai o mot lop sau la duong duy nhat
-- giu duoc ca hai: parity 100% tung o VA mot cho tuong minh de noi "o nay go la".

ALTER TABLE fls_itl ALTER COLUMN svc_start      TYPE text USING svc_start::text;
ALTER TABLE fls_itl ALTER COLUMN svc_end        TYPE text USING svc_end::text;
ALTER TABLE fls_itl ALTER COLUMN svc_start_thyt TYPE text USING svc_start_thyt::text;
ALTER TABLE fls_itl ALTER COLUMN svc_end_thyt   TYPE text USING svc_end_thyt::text;

COMMENT ON COLUMN fls_itl.svc_start IS
  'AH(33) Final khoi 4 — KY do nguoi go, kieu text. ⛔ KHONG phai date: nguon '
  'co ''thang 5'', ''2025.07'', ''TPCI''… va khong he co ngay trong thang';
COMMENT ON COLUMN fls_itl.svc_end IS
  'AL(37) Final khoi 5 — KY do nguoi go, kieu text (xem svc_start)';
