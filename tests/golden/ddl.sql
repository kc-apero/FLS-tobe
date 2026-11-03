CREATE SEQUENCE IF NOT EXISTS seq_itl_id START 1;

CREATE TABLE IF NOT EXISTS fls_le (
  le_code text NOT NULL PRIMARY KEY,
  le_name text,
  is_entity boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS fls_source (
  source_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  source_key text NOT NULL UNIQUE,
  src_type text NOT NULL,
  last_seen_at timestamptz,
  lag_days int,
  cutoff_date date,
  txn_count int
);

CREATE TABLE IF NOT EXISTS fls_khai_cot (
  khai_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  version int NOT NULL,
  truong text NOT NULL,
  cot int NOT NULL,
  thu_tu text,
  hieu_luc_tu timestamptz NOT NULL DEFAULT now(),
  actor text NOT NULL,
  CONSTRAINT fls_khai_cot_source_id_version_truong_uq UNIQUE (source_id, version, truong),
  CONSTRAINT fls_khai_cot_thu_tu_ck CHECK (thu_tu IS NULL OR (truong = 'Date' AND thu_tu IN ('dmy', 'mdy')))
);

CREATE TABLE IF NOT EXISTS fls_nguon_dai (
  dai_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  truong text NOT NULL,
  cot int,
  dai_tho text NOT NULL,
  danh_muc text NOT NULL,
  doc_luc timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fls_chup (
  chup_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  doc_luc timestamptz NOT NULL DEFAULT now(),
  spreadsheet_id text NOT NULL,
  lan text NOT NULL,
  giay numeric(8,2),
  actor text NOT NULL
);

CREATE TABLE IF NOT EXISTS fls_chup_nguon (
  chup_id bigint NOT NULL REFERENCES fls_chup(chup_id),
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  khai_version int NOT NULL,
  CONSTRAINT fls_chup_nguon_pk PRIMARY KEY (chup_id, source_id)
);

CREATE TABLE IF NOT EXISTS fls_chup_dong (
  chup_id bigint NOT NULL REFERENCES fls_chup(chup_id),
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  dong_so int NOT NULL,
  o jsonb NOT NULL,
  CONSTRAINT fls_chup_dong_pk PRIMARY KEY (chup_id, source_id, dong_so)
);

CREATE TABLE IF NOT EXISTS fls_run (
  run_id text NOT NULL PRIMARY KEY,
  contract_version text NOT NULL,
  canon_version text NOT NULL,
  mapping_version text NOT NULL,
  started_at timestamptz NOT NULL DEFAULT now(),
  row_count int,
  state text NOT NULL DEFAULT 'queued',
  khai_id bigint REFERENCES fls_khai_cot(khai_id),
  chup_id bigint REFERENCES fls_chup(chup_id)
);

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
  svc_start text,
  svc_end text,
  hd_thyt text,
  pay_type_thyt text,
  cdt1_thyt text,
  svc_start_thyt text,
  svc_end_thyt text,
  work_status text NOT NULL DEFAULT 'ok',
  id_payee text,
  invoice text,
  id_payee_thyt text,
  invoice_thyt text,
  le_payer text REFERENCES fls_le(le_code),
  is_intercompany boolean GENERATED ALWAYS AS (le IS NOT NULL AND le_payer IS NOT NULL AND le <> le_payer) STORED,
  pic text,
  audit_status text,
  pm_hinh text,
  itl_id_sheet text,
  canon jsonb NOT NULL
);

CREATE TABLE IF NOT EXISTS fls_pm_link (
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  pm_line_id text NOT NULL,
  amount numeric(20,2) NOT NULL,
  hinh text NOT NULL,
  run_id text NOT NULL REFERENCES fls_run(run_id),
  run_pm text REFERENCES fls_run(run_id),
  created_at timestamptz NOT NULL DEFAULT now(),
  link_id bigint NOT NULL DEFAULT nextval('seq_itl_id'),
  lan smallint NOT NULL DEFAULT 1,
  CONSTRAINT fls_pm_link_pk PRIMARY KEY (link_id),
  CONSTRAINT fls_pm_link_itl_id_pm_line_id_lan_uq UNIQUE (itl_id, pm_line_id, lan)
);

CREATE TABLE IF NOT EXISTS fls_pm_line (
  run_id text NOT NULL REFERENCES fls_run(run_id),
  pm_line_id text NOT NULL,
  pm_slip_id text NOT NULL,
  ref_tho text,
  ref_canon text,
  amount numeric(20,2),
  curr text NOT NULL,
  status text,
  pe_slip text,
  pe_line text,
  pe_loai text,
  pi_slip text,
  pi_line text,
  tho json,
  hd text,
  cdt1 text,
  source_row integer NOT NULL,
  read_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT fls_pm_line_pk PRIMARY KEY (run_id, pm_line_id),
  CONSTRAINT fls_pm_line_run_id_source_row_uq UNIQUE (run_id, source_row),
  CONSTRAINT fls_pm_line_pe_loai_ck CHECK (pe_loai IS NULL OR (pe_line IS NOT NULL AND pe_loai IN ('Advance', 'Urgent')))
);

CREATE TABLE IF NOT EXISTS fls_queue_event (
  evt_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  evt_type text NOT NULL,
  reason text,
  defer_until date,
  actor text NOT NULL,
  at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fls_pm_unlink (
  unlink_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  link_id bigint NOT NULL UNIQUE REFERENCES fls_pm_link(link_id),
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  evt_id bigint NOT NULL REFERENCES fls_queue_event(evt_id),
  at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fls_adjustment (
  adj_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  field text NOT NULL,
  value_after text,
  state text NOT NULL DEFAULT 'posted',
  reversal_of bigint REFERENCES fls_adjustment(adj_id),
  actor text NOT NULL,
  at timestamptz NOT NULL DEFAULT now(),
  evt_id bigint REFERENCES fls_queue_event(evt_id),
  nguon text NOT NULL DEFAULT 'sua_tay',
  CONSTRAINT fls_adjustment_nguon_ck CHECK (nguon IN ('sua_tay', 'may_goi_y'))
);

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

CREATE TABLE IF NOT EXISTS fls_reject (
  rej_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  run_id text NOT NULL REFERENCES fls_run(run_id),
  source_system text NOT NULL,
  source_sheet text NOT NULL,
  source_row int NOT NULL,
  reason text NOT NULL,
  CONSTRAINT fls_reject_run_id_source_sheet_source_row_uq UNIQUE (run_id, source_sheet, source_row)
);

CREATE TABLE IF NOT EXISTS fls_mapping_master (
  hd_code text NOT NULL PRIMARY KEY,
  need_cfa2 text,
  method_cfa2 text,
  code_hr text,
  coa1 text,
  coa2 text
);

CREATE OR REPLACE VIEW fls_queue_state AS SELECT itl_id,
       (ARRAY_AGG(reason ORDER BY at DESC)
          FILTER (WHERE evt_type = 'reason'))[1]            AS reason,
       MAX(defer_until) FILTER (WHERE evt_type = 'defer')   AS defer_until,
       COUNT(*) FILTER (WHERE evt_type = 'defer')::int      AS defer_count
FROM fls_queue_event
GROUP BY itl_id;

CREATE OR REPLACE VIEW fls_queue_reason_weekly AS SELECT DATE_TRUNC('week', at)::date AS tuan,
       COUNT(*)::int                AS so_lan
FROM fls_queue_event
WHERE evt_type = 'reason'
GROUP BY 1
ORDER BY 1 DESC;

CREATE OR REPLACE VIEW fls_sua_tay AS SELECT z.itl_id, z.field, z.value_after, z.adj_id, z.actor, z.at
FROM (SELECT a.itl_id, a.field, a.value_after, a.adj_id, a.actor, a.at,
             row_number() OVER (PARTITION BY a.itl_id, a.field
                                ORDER BY a.adj_id DESC) AS rn
      FROM fls_adjustment a
      WHERE a.reversal_of IS NULL
        AND a.nguon = 'sua_tay'
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1;

CREATE OR REPLACE VIEW fls_may_goi_y AS SELECT z.itl_id, z.field, z.value_after, z.adj_id, z.at
FROM (SELECT a.itl_id, a.field, a.value_after, a.adj_id, a.at,
             row_number() OVER (PARTITION BY a.itl_id, a.field
                                ORDER BY a.adj_id DESC) AS rn
      FROM fls_adjustment a
      WHERE a.reversal_of IS NULL
        AND a.nguon = 'may_goi_y'
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1;

CREATE OR REPLACE VIEW fls_dien_giai AS SELECT i.itl_id,
       btrim(d.o ->> 'Description') AS dien_giai,
       d.chup_id
FROM fls_itl i
JOIN fls_source s ON s.source_key = i.source_sheet
JOIN LATERAL (
  SELECT dd.o, dd.chup_id
    FROM fls_chup_dong dd
   WHERE dd.source_id = s.source_id
     AND dd.dong_so   = i.source_row
   ORDER BY dd.chup_id DESC
   LIMIT 1
) d ON true
WHERE btrim(coalesce(d.o ->> 'Description', '')) <> '';

CREATE OR REPLACE VIEW fls_moi_noi AS SELECT l.link_id, l.itl_id, l.pm_line_id, l.amount, l.hinh, l.lan, l.run_id,
       l.created_at
FROM fls_pm_link l
WHERE NOT EXISTS (SELECT 1 FROM fls_pm_unlink u WHERE u.link_id = l.link_id);

CREATE OR REPLACE VIEW fls_da_xong AS SELECT z.itl_id, z.evt_id, z.actor, z.at, z.reason
FROM (SELECT e.itl_id, e.evt_id, e.actor, e.at, e.reason, e.evt_type,
             row_number() OVER (PARTITION BY e.itl_id
                                ORDER BY e.evt_id DESC) AS rn
      FROM fls_queue_event e
      WHERE e.evt_type IN ('done', 'reopen')) z
WHERE z.rn = 1 AND z.evt_type = 'done';
