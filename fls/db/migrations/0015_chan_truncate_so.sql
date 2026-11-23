-- 0015 · BIT LO CUA `INV-I03`: no chan DELETE nhung ⛔ KHONG chan TRUNCATE.
--
-- ⛔⛔ **Do that 2026-09-07 tren kho test, truoc khi va:**
--       DELETE   -> BI CHAN  ✅  "INV-I03: itl_id 1 da raw_frozen…"
--       TRUNCATE -> ⛔ KHONG bi chan — sau lenh con 0 dong
--     Tuc bat bien "so chi-THEM" (`INV-I03`) cach su that **mot cau lenh**.
--     PostgreSQL ⛔ khong ban trigger DELETE muc DONG khi chay TRUNCATE; muon
--     chan thi phai khai rieng `BEFORE TRUNCATE … FOR EACH STATEMENT`.
--
-- ★ Vi sao lo nay nguy hon no trong: `INV-I03` la thu duoc trich dan o khap
--   bo tai lieu nhu **bang chung** rang so ⛔ khong the bi sua. Mot bat bien
--   duoc tin nhieu ma chi dung MOT NUA thi te hon mot bat bien ⛔ khong ai tin,
--   vi ⛔ khong ai di kiem lai no.
--
-- ⚠ Pham vi: chi `fls_itl` — cuon SO. `fls_journal`/`fls_adjustment` la so ghi
--   THEM nhung chung ⛔ chua bao gio co trigger nao, nen them chan o day se la
--   mot quyet dinh MOI, ⛔ khong phai va mot lo. De rieng.
--
-- ⭐ Kho TEST van dung lai duoc: `fls/db/kho.py::dung_lai_kho_test` di duong
--   `DROP DATABASE` — ⛔ khong cham TRUNCATE nen ⛔ khong vuong chan nay.

CREATE OR REPLACE FUNCTION fls_chan_truncate_so() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION
    'INV-I03: `%` la so CHI-THEM — TRUNCATE bi cam. Muon dung lai kho TEST '
    'thi dung `fls.db.kho.dung_lai_kho_test()` (duong DROP DATABASE).',
    TG_TABLE_NAME;
END $$ LANGUAGE plpgsql;
-- >>>
DROP TRIGGER IF EXISTS trg_fls_itl_chan_truncate ON fls_itl;
-- >>>
CREATE TRIGGER trg_fls_itl_chan_truncate BEFORE TRUNCATE ON fls_itl
FOR EACH STATEMENT EXECUTE FUNCTION fls_chan_truncate_so();
