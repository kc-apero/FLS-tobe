-- 0027 · KHO CONFIG CHI-THEM CO PHIEN BAN (ISP 3.1.2 · Step 14 · `C5` · `WO-142`).
--
-- ⛔⛔ **Hai bang nay luu CONFIG da dong bang theo PHIEN BAN — ⛔ KHONG luu so.**
--    `IX.FX` (ty gia thang) · `IX.HD` (cay hop dong) · `IX.HD · IX.ORG` (Mapping
--    Master) toi nay doc tu ANH TINH di cung goi; tu `C5` doc tu KHO. Tuyen
--    `/config/fx` · `/config/hd` ⛔ doi hop dong — chi doi NGUON.
--
-- ── Vi sao CHEP khuon `fls_khai_cot` (di tru `0016`) ──────────────────────────
--
-- `fls_khai_cot` da giai dung bai nay cho *"cach doc sao ke"*: chi-THEM ·
-- `version` · moc do MAY dat · du-hoac-khong trong mot giao dich · ⛔ ban mac
-- dinh · loi "nguon la" ≠ "chua khai". Config cung la mot thu **doi theo thoi
-- gian ma phai giai thich duoc qua khu**: ngan hang doi ty gia thang, ke toan
-- doi cay HD ⇒ *"so cu doc bang config nao"* phai con cau tra loi. ⇒ Mot bang
-- MOI cho moi lan nap (`fls_cau_hinh_ban`), ⛔ sua ban cu.
--
-- ⚠ `C7` (ky thang) + cac bang config khac (C6, C8…) KHONG o day — mot buoc.
--
-- ── Ba luat (cung `DD-I10` ⓷ cua `fls_khai_cot`) ─────────────────────────────
--
--   ⓐ ⛔ CHI-THEM. Nap lai = `phien_ban` MOI, ⛔ sua ban cu. Co trigger
--      `BEFORE UPDATE OR DELETE` chan — va `BEFORE TRUNCATE` (bay `0015`:
--      `INV-I03` chan DELETE ma ⛔ TRUNCATE; day dong luon lo ay).
--   ⓑ ⛔ `UNIQUE(bang, phien_ban)` — hai ban cung phien ban la hai nguon su
--      that cho cung mot cau hoi. Va `UNIQUE(ban_id, khoa)` — mot khoa hai lan
--      trong mot ban la hai cau tra loi (cung luat `fls_khai_cot`
--      `(source_id, version, truong)`).
--   ⓒ ⛔ `luc` do MAY dat (`DEFAULT now()`), ⛔ nguoi goi truyen vao — ⛔ thi
--      `phien_ban` cao nhat va moc moi nhat co the ⛔ cung chi mot ban.
--
-- ⚠ ⛔ co `CHECK` mien gia tri (vd `bang IN (…)`) — ca repo nay ⛔ co mot `CHECK`
--    enum nao: mien gia tri la **loi van + chan o tang ghi** (`work_status`,
--    `period_state`, `src_type`). Cho chan `bang` la `fls/repo/cau_hinh_repo.py`
--    (`BangLa`), va no chan luc GHI. Giu dung tien le `fls_khai_cot`.

CREATE TABLE IF NOT EXISTS fls_cau_hinh_ban (
  ban_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  bang text NOT NULL,
  phien_ban int NOT NULL,
  nguon text NOT NULL,
  checksum text NOT NULL,
  actor text NOT NULL,
  luc timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT fls_cau_hinh_ban_bang_phien_ban_uq UNIQUE (bang, phien_ban)
);
-- >>>
COMMENT ON TABLE fls_cau_hinh_ban IS
  'C5: kho config chi-THEM. Mot DONG = mot lan nap mot bang config (IX.FX/IX.HD/IX.HD · IX.ORG). Sua config = phien_ban moi';
-- >>>
COMMENT ON COLUMN fls_cau_hinh_ban.checksum IS
  'sha256 noi dung da chuan hoa — nap lai cung anh ⇒ checksum trung ⇒ khong_doi';
-- >>>
COMMENT ON COLUMN fls_cau_hinh_ban.actor IS
  'nap config la HANH VI CUA NGUOI, phai co ten — cung luat fls_khai_cot.actor';
-- >>>
COMMENT ON COLUMN fls_cau_hinh_ban.luc IS
  'moc do MAY dat (now()), ⛔ nguoi goi truyen vao';
-- >>>
CREATE INDEX IF NOT EXISTS ix_fls_cau_hinh_ban_bang
  ON fls_cau_hinh_ban (bang, phien_ban);
-- >>>
CREATE TABLE IF NOT EXISTS fls_cau_hinh_dong (
  dong_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  ban_id bigint NOT NULL REFERENCES fls_cau_hinh_ban(ban_id),
  khoa text NOT NULL,
  gia_tri jsonb NOT NULL,
  CONSTRAINT fls_cau_hinh_dong_ban_id_khoa_uq UNIQUE (ban_id, khoa)
);
-- >>>
COMMENT ON TABLE fls_cau_hinh_dong IS
  'C5: cac dong cua mot lan nap config. `khoa` = khoa tu nhien cua tuyen (yyyymm / ma HD); `gia_tri` jsonb';
-- >>>
CREATE INDEX IF NOT EXISTS ix_fls_cau_hinh_dong_ban
  ON fls_cau_hinh_dong (ban_id);
-- >>>
-- ── Trigger CHI-THEM (cung khuon `fls_chan_sua_dong_dong_bang` cua `0001`) ─────
CREATE OR REPLACE FUNCTION fls_chan_sua_cau_hinh() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION
    'INV-I08: `%` la kho config CHI-THEM — % bi cam. Sua config = nap mot '
    '`phien_ban` moi (fls.repo.cau_hinh_repo.nap), ⛔ sua ban cu.',
    TG_TABLE_NAME, TG_OP;
END $$ LANGUAGE plpgsql;
-- >>>
CREATE OR REPLACE FUNCTION fls_chan_truncate_cau_hinh() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION
    'INV-I08: `%` la kho config CHI-THEM — TRUNCATE bi cam. Dung lai kho TEST '
    'thi dung fls.db.kho.dung_lai_kho_test() (duong DROP DATABASE).',
    TG_TABLE_NAME;
END $$ LANGUAGE plpgsql;
-- >>>
DROP TRIGGER IF EXISTS trg_fls_cau_hinh_ban_chi_them ON fls_cau_hinh_ban;
-- >>>
CREATE TRIGGER trg_fls_cau_hinh_ban_chi_them
BEFORE UPDATE OR DELETE ON fls_cau_hinh_ban
FOR EACH ROW EXECUTE FUNCTION fls_chan_sua_cau_hinh();
-- >>>
DROP TRIGGER IF EXISTS trg_fls_cau_hinh_ban_chan_truncate ON fls_cau_hinh_ban;
-- >>>
CREATE TRIGGER trg_fls_cau_hinh_ban_chan_truncate
BEFORE TRUNCATE ON fls_cau_hinh_ban
FOR EACH STATEMENT EXECUTE FUNCTION fls_chan_truncate_cau_hinh();
-- >>>
DROP TRIGGER IF EXISTS trg_fls_cau_hinh_dong_chi_them ON fls_cau_hinh_dong;
-- >>>
CREATE TRIGGER trg_fls_cau_hinh_dong_chi_them
BEFORE UPDATE OR DELETE ON fls_cau_hinh_dong
FOR EACH ROW EXECUTE FUNCTION fls_chan_sua_cau_hinh();
-- >>>
DROP TRIGGER IF EXISTS trg_fls_cau_hinh_dong_chan_truncate ON fls_cau_hinh_dong;
-- >>>
CREATE TRIGGER trg_fls_cau_hinh_dong_chan_truncate
BEFORE TRUNCATE ON fls_cau_hinh_dong
FOR EACH STATEMENT EXECUTE FUNCTION fls_chan_truncate_cau_hinh();
