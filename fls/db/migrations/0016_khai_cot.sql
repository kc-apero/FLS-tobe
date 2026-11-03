-- 0016 · CHO O CHO BAN KHAI ANH XA COT (`CR#11` · `DD-I10` · `QĐ-ITL-105`).
--
-- ⛔⛔ **Bang nay ⛔ KHONG luu du lieu — no luu CACH DOC du lieu.**
--
-- ── Vi sao phai co, va vi sao phai co BAY GIO ────────────────────────────
--
-- Ke toan **da tu giai** bai toan "60+ dinh dang sao ke", va giai rat tot:
-- **dong 1 cua moi sheet `R |` la mot BAN KHAI ANH XA** — `1`=Date · `2`=
-- Description · `3`=Currency · `4`=Debit · `5`=Credit · `6`=Reference number.
-- Ho tu duy tri bang tay, va do duoc: **68/68 sheet khai du 6 truong**, tren
-- **9 bo tri cot khac nhau**.
--
-- ⭐ Do la **thu tot nhat trong ca he AS-IS**, va no ⛔ KHONG co ban sao o dau
--   khac. `QĐ-ITL-105` bo Google Sheets khoi duong nap ⇒ neu ⛔ khong dung cho
--   o moi thi **ban khai ay bi vut theo**, va FLS se phai **doan vi tri cot** —
--   thu ma `fls/adapters/sao_ke.py` cam thang:
--
--       "⛔ khong doan theo vi tri cot: do song co 9 bo tri khac nhau, nen
--        doan ⛔ khong phai la kem chinh xac — no la **sai tien**."
--
-- ⇒ Viec cua migration nay ⛔ **khong phai cho DU LIEU di**, ma la cho **CACH
--   DOC** di. Dung dieu owner chot: *"giai doan nay tao khuon de nhan data,
--   chua can migrate du lieu tu ggsheet"*.
--
-- ── Ba luat (`DD-I10` ⓷) ────────────────────────────────────────────────
--
--   ⓐ ⛔ CHI-THEM. Sua khai = them mot `version` MOI, ⛔ khong sua khai cu.
--      Mot dong nap thang truoc phai giai thich duoc bang **ban khai hieu luc
--      LUC AY**; sua de la viet lai lich su (`INV-I08`).
--   ⓑ ⛔ Du 6 truong moi cho nap. Thieu mot truong la **NO TO**
--      (`sao_ke.BanKhaiHong`), ⛔ khong nap mot phan — nap mot phan la **mat
--      cot trong im lang**, va cot mat co the la cot TIEN.
--   ⓒ ⛔ `cot` la SO, `truong` la TEN. `ITL-CANON` co **4 cot trung ten** ⇒ ⛔
--      khong tham chieu theo ten duoc; con tep nguon thi **doi thu tu cot** ⇒
--      ⛔ khong neo theo so duoc. Hai dau **phai nguoc nhau**.
--
-- ⚠ **Luat ⓑ va mien gia tri ⛔ KHONG cuong che o day, va do la mot QUYET
--    DINH, ⛔ khong phai mot cho quen.** Ca repo nay ⛔ khong co lay mot rang
--    buoc `CHECK` nao: `work_status` (`ok|UNMAPPED|rejected`), `period_state`
--    (`open|locked`), `src_type`, `evt_type` — tat ca deu la **loi van trong
--    schema + chan o tang ghi**. Them mot `CHECK` rieng cho bang nay se la
--    **cho khai thu hai** cho `sao_ke.SAU_TRUONG`, dung benh ma ca khuon
--    `fls/db/model.py` sinh ra de chua. ⇒ Cho chan la `fls/repo/khai_cot.py`
--    (task `2`), va no phai chan luc **GHI** — chan luc DOC thi ban khai hong
--    da nam trong kho roi.
--
-- ── `fls_run.khai_id` — vi sao NULLABLE ─────────────────────────────────
--
-- Lan nap `NAP-2026-08-27-RAW` (**10.030 dong dang nam trong kho**) **co truoc**
-- bang nay. Bia mot `khai_id` cho qua khu la trai `R-A1`. ⇒ `NULL` o day doc la
-- *"lo nay co truoc khi ban khai co cho o"* — mot cau **THAT**; con mot so bia
-- ra thi doc nhu mot **cau tra loi**. Cung ly do `fls_le.le_name` de NULL cho
-- 24/29 ma (`INV-I16`: NULL trung thuc hon ma bia).
--
-- ⭐⭐ Va cot nay lam mot viec nua, ngoai le: no **noi lien `fls_source` voi so**.
--    Truoc migration nay `fls_source` la mot DAO (`ERD_ISLANDS`) — mot manifest
--    ma ⛔ khong dong so nao tro toi duoc. Nay co duong di bo duoc:
--        `fls_itl.run_id` → `fls_run.khai_id` → `fls_khai_cot.source_id` → `fls_source`
--    doc ra: *"dong so nay den tu NGUON nay, doc bang BAN KHAI nay"*.
--    ⇒ `fls_source` da duoc go khoi `ERD_ISLANDS` (3 → 2 ten).

CREATE TABLE IF NOT EXISTS fls_khai_cot (
  khai_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  version int NOT NULL,
  truong text NOT NULL,
  cot int NOT NULL,
  hieu_luc_tu timestamptz NOT NULL DEFAULT now(),
  actor text NOT NULL,
  CONSTRAINT fls_khai_cot_source_id_version_truong_uq UNIQUE (source_id, version, truong)
);

COMMENT ON TABLE fls_khai_cot IS
  'DD-I10 — ban khai anh xa cot. ⛔ KHONG luu du lieu, luu CACH DOC du lieu. Chi-THEM: sua khai = version moi';
COMMENT ON COLUMN fls_khai_cot.truong IS
  'mot trong 6 ten cua sao_ke.SAU_TRUONG — doc theo TEN, ⛔ khong theo so';
COMMENT ON COLUMN fls_khai_cot.cot IS
  'chi so cot 0-based trong tep nguon — SO, vi tep nguon doi thu tu cot';
COMMENT ON COLUMN fls_khai_cot.actor IS
  'ban khai la HANH VI CUA NGUOI, phai co ten';

-- Duong nong cua tang doc: "ban khai nao dang hieu luc cho nguon nay".
CREATE INDEX IF NOT EXISTS ix_fls_khai_cot_nguon
  ON fls_khai_cot (source_id, version);

ALTER TABLE fls_run ADD COLUMN IF NOT EXISTS khai_id bigint;
ALTER TABLE fls_run DROP CONSTRAINT IF EXISTS fls_run_khai_id_fkey;
ALTER TABLE fls_run ADD CONSTRAINT fls_run_khai_id_fkey
  FOREIGN KEY (khai_id) REFERENCES fls_khai_cot(khai_id);

COMMENT ON COLUMN fls_run.khai_id IS
  'DD-I10: lo nap nay doc bang ban khai nao. NULL = lo co TRUOC khi bang khai ton tai (⛔ khong bia — R-A1)';
