-- 0001_baseline.sql
-- DONG BANG 2026-08-26. ⛔ TUYET DOI KHONG SUA FILE NAY.
-- Sinh mot lan tu fls/db/schema.py + triggers.py o trang thai 26/08 (commit 01898b9).
-- Sua file da ap = doi lich su => cong kiem_lich_su NO tren moi DB da ap no.
-- Doi schema tu day tro di: THEM file 0002_*.sql voi cau ALTER.
-- Cau lenh tach nhau bang mot dong phan cach rieng (xem migration_runner.SEP),
-- KHONG tach bang dau ';' vi than ham plpgsql co ';' ben trong.

CREATE SEQUENCE IF NOT EXISTS seq_itl_id START 1;
-- >>>
CREATE TABLE IF NOT EXISTS fls_le (
  le_code text NOT NULL PRIMARY KEY,
  le_name text NOT NULL,
  is_entity boolean NOT NULL DEFAULT true
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_run (
  run_id text NOT NULL PRIMARY KEY,
  contract_version text NOT NULL,
  canon_version text NOT NULL,
  mapping_version text NOT NULL,
  started_at timestamptz NOT NULL DEFAULT now(),
  row_count int,
  state text NOT NULL DEFAULT 'queued'
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_itl (
  itl_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  content_key text NOT NULL UNIQUE,
  source_system text NOT NULL,
  source_sheet text NOT NULL,
  source_row int NOT NULL,
  run_id text NOT NULL REFERENCES fls_run(run_id),
  contract_version text NOT NULL,
  canon_version text NOT NULL,
  mapping_version text NOT NULL,
  raw_frozen boolean NOT NULL DEFAULT false,
  is_flash boolean NOT NULL DEFAULT true,
  period_state text NOT NULL DEFAULT 'open',
  created_at timestamptz NOT NULL DEFAULT now(),
  doc_date date,
  doc_no text,
  memo text,
  curr text,
  ps_no numeric(20,2),
  ps_co numeric(20,2),
  acct text,
  le text REFERENCES fls_le(le_code),
  hd text,
  pay_type text,
  cdt1 text,
  svc_start date,
  svc_end date,
  hd_thyt text,
  pay_type_thyt text,
  cdt1_thyt text,
  svc_start_thyt date,
  svc_end_thyt date,
  work_status text NOT NULL DEFAULT 'ok',
  id_payee text,
  invoice text,
  cdt1_cfa1 text,
  cdt1_cfa2 text,
  alloc_method text,
  cdt1_cfa2_classify text,
  alloc_method_classify text,
  le_payer text REFERENCES fls_le(le_code),
  is_intercompany boolean GENERATED ALWAYS AS (le IS NOT NULL AND le_payer IS NOT NULL AND le <> le_payer) STORED,
  pic text,
  audit_status text,
  canon jsonb NOT NULL
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_adjustment (
  adj_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  field text NOT NULL,
  value_after text,
  state text NOT NULL DEFAULT 'posted',
  reversal_of bigint REFERENCES fls_adjustment(adj_id),
  actor text NOT NULL,
  at timestamptz NOT NULL DEFAULT now()
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_journal (
  jrn_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  field text NOT NULL,
  value_before text,
  value_after text,
  actor text NOT NULL,
  at timestamptz NOT NULL DEFAULT now(),
  value_source text NOT NULL,
  reason text
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_reject (
  rej_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  run_id text NOT NULL REFERENCES fls_run(run_id),
  source_system text NOT NULL,
  source_sheet text NOT NULL,
  source_row int NOT NULL,
  reason text NOT NULL
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_mapping_master (
  hd_code text NOT NULL PRIMARY KEY,
  need_cfa2 text,
  method_cfa2 text,
  code_hr text,
  coa1 text,
  coa2 text
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_source (
  source_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  source_key text NOT NULL UNIQUE,
  src_type text NOT NULL,
  last_seen_at timestamptz,
  lag_days int,
  cutoff_date date,
  txn_count int
);
-- >>>
CREATE TABLE IF NOT EXISTS fls_queue_event (
  evt_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  evt_type text NOT NULL,
  reason text,
  defer_until date,
  actor text NOT NULL,
  at timestamptz NOT NULL DEFAULT now()
);
-- >>>
CREATE OR REPLACE VIEW fls_queue_state AS SELECT itl_id,
       (ARRAY_AGG(reason ORDER BY at DESC)
          FILTER (WHERE evt_type = 'reason'))[1]            AS reason,
       MAX(defer_until) FILTER (WHERE evt_type = 'defer')   AS defer_until,
       COUNT(*) FILTER (WHERE evt_type = 'defer')::int      AS defer_count
FROM fls_queue_event
GROUP BY itl_id;
-- >>>
CREATE OR REPLACE VIEW fls_queue_reason_weekly AS SELECT DATE_TRUNC('week', at)::date AS tuan,
       COUNT(*)::int                AS so_lan
FROM fls_queue_event
WHERE evt_type = 'reason'
GROUP BY 1
ORDER BY 1 DESC;
-- >>>
CREATE OR REPLACE FUNCTION fls_chan_sua_dong_dong_bang() RETURNS trigger AS $$
BEGIN
  IF OLD.raw_frozen THEN
    RAISE EXCEPTION 'INV-I03: itl_id % da raw_frozen, sua chi bang but toan moi', OLD.itl_id;
  END IF;
  IF TG_OP = 'DELETE' THEN
    RETURN OLD;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
-- >>>
DROP TRIGGER IF EXISTS trg_fls_itl_inv_i03 ON fls_itl;
-- >>>
CREATE TRIGGER trg_fls_itl_inv_i03 BEFORE UPDATE OR DELETE ON fls_itl
FOR EACH ROW EXECUTE FUNCTION fls_chan_sua_dong_dong_bang();
-- >>>
CREATE OR REPLACE FUNCTION fls_chan_doi_itl_id() RETURNS trigger AS $$
BEGIN
  IF NEW.itl_id <> OLD.itl_id THEN
    RAISE EXCEPTION 'INV-I04a: itl_id dong bang, khong duoc doi (% -> %)',
      OLD.itl_id, NEW.itl_id;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
-- >>>
DROP TRIGGER IF EXISTS trg_fls_itl_inv_i04a ON fls_itl;
-- >>>
CREATE TRIGGER trg_fls_itl_inv_i04a BEFORE UPDATE ON fls_itl
FOR EACH ROW EXECUTE FUNCTION fls_chan_doi_itl_id();
