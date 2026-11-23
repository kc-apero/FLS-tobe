-- 0025 · `fls_adjustment.nguon` — BANG GIA TRI PHAI TU NOI DUOC "AI NOI"
--
-- ⭐⭐⭐ Owner chot **phuong an B** (`2026-09-18`) · `QĐ-ITL-143` · chang 1.
--
-- ── LO, va no ⛔ KHONG phai mot thieu sot nho ──────────────────────────
-- Duong ghep **TAY** suy `hd`/`cdt1` tu dong lenh tu `28/08`. Duong ghep
-- **TU DONG** (`chay_nap.chen_moi_noi`) thi ⛔ khong: no chen moi noi roi thoi.
-- Do tren kho that `18/09` (`pm_line_id` PHAN BIET — ⛔ bay anh chup):
--
--     `fls_itl`          8.387 dong · `hd` 0 · `cdt1` 0 · ca hai `*_thyt` 0
--     dong lenh THAT     3.772      · co `hd` 3.767 (99,9%) · `cdt1` 3.763
--     dong so DA ghep    2.222      ⇒ suy duoc `hd` 2.219 · `cdt1` 2.217
--     ⚠ va **10** dong so co N dong lenh noi HAI `hd` KHAC NHAU
--
-- ⇒ Cau tra loi **da nam san trong kho**, chi la ⛔ khong ai bac cau.
--
-- ⛔⛔⛔ **NHUNG BAC CAU THANG THI MAY TRA LOI THAY NGUOI — va cho truot
--    nam o mot cho ⛔ KHONG AI NHIN THAY.**
--
--     `fls_adjustment`  (bang GIA TRI)   ⛔ KHONG co cot nguon
--     `fls_journal`     (so NHAT KY)     CO `value_source`
--     `fls_sua_tay`     (khung xem tra loi *"o nay dang la gi"*) doc
--                                        **bang GIA TRI**
--
--   ⇒ Mot goi y cua MAY ghi vao `fls_adjustment` se hien ra **y het** mot con
--     so NGUOI da chot. `_hieu_luc()` lay no lam `value_before` cho lan go sau,
--     va `truoc_khi_go()` in no ra nhu *"gia tri dang co"*. ⛔ Khong mot cho
--     nao trong duong DOC phan biet duoc — muon biet phai di vong sang
--     `fls_journal`, ma ⛔ khong cho nao lam the.
--
--   ⇒ Do dung la `INV-I16`: **may ⛔ khong duoc tu tra loi thay nguoi**.
--
-- ── VI SAO KHONG nhet mot cot `nguon` vao `fls_sua_tay` roi thoi ──────
-- `fls_sua_tay` dang tra loi **MOT** cau: *"NGUOI da chot gi"*. `bang_tuyen.py`
-- co **8 tuyen** doc no voi dung nghia ay. Them goi y cua may vao rong roi bat
-- moi cho tu loc la doi nghia mot khung xem **dang chay** — va cho nao quen loc
-- thi ⛔ khong bao loi, chi tra sai.
--
--   ⇒ `fls_sua_tay` **GIU NGUYEN NGHIA**, nay loc thang `nguon = 'sua_tay'`.
--   ⇒ Goi y cua may di **loi RIENG**: `fls_may_goi_y`.
--
-- ⚠ `DEFAULT 'sua_tay'` o day la **an toan**, ⛔ khong phai mot phep doan:
--   do luc chay migration, `fls_adjustment` co **0 dong** tren kho that va
--   MOI duong ghi hien co deu di qua `ghi_tay._them` — tuc deu la nguoi go.
--   ⛔ Neu bang nay da co dong thi `DEFAULT` se la mot lo **gan nhan bua**.

ALTER TABLE fls_adjustment
  ADD COLUMN IF NOT EXISTS nguon text NOT NULL DEFAULT 'sua_tay';

ALTER TABLE fls_adjustment DROP CONSTRAINT IF EXISTS fls_adjustment_nguon_ck;
ALTER TABLE fls_adjustment
  ADD CONSTRAINT fls_adjustment_nguon_ck
  CHECK (nguon IN ('sua_tay', 'may_goi_y'));

COMMENT ON COLUMN fls_adjustment.nguon IS
  'AI noi con so nay: `sua_tay` = NGUOI go/chot · `may_goi_y` = MAY suy tu '
  'dong lenh da ghep. ⛔ `fls_sua_tay` CHI lay `sua_tay` (`INV-I16`).';

-- ⛔ `fls_sua_tay` — THEM dung MOT menh de, giu nguyen moi thu khac.
CREATE OR REPLACE VIEW fls_sua_tay AS
SELECT z.itl_id, z.field, z.value_after, z.adj_id, z.actor, z.at
FROM (SELECT a.itl_id, a.field, a.value_after, a.adj_id, a.actor, a.at,
             row_number() OVER (PARTITION BY a.itl_id, a.field
                                ORDER BY a.adj_id DESC) AS rn
      FROM fls_adjustment a
      WHERE a.reversal_of IS NULL
        AND a.nguon = 'sua_tay'
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1;

-- ⭐ Loi RIENG cua may. Cung mot thuoc thang: so giu ca lich su, *"dang co"*
--   la mot PHEP TINH.
CREATE OR REPLACE VIEW fls_may_goi_y AS
SELECT z.itl_id, z.field, z.value_after, z.adj_id, z.at
FROM (SELECT a.itl_id, a.field, a.value_after, a.adj_id, a.at,
             row_number() OVER (PARTITION BY a.itl_id, a.field
                                ORDER BY a.adj_id DESC) AS rn
      FROM fls_adjustment a
      WHERE a.reversal_of IS NULL
        AND a.nguon = 'may_goi_y'
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1;

CREATE INDEX IF NOT EXISTS fls_adjustment_nguon_idx
  ON fls_adjustment (itl_id, field, nguon);
