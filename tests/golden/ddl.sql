CREATE SEQUENCE IF NOT EXISTS seq_itl_id START 1;

CREATE TABLE IF NOT EXISTS fls_le (
  le_code text NOT NULL PRIMARY KEY,
  le_name text,
  is_entity boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS fls_run (
  run_id text NOT NULL PRIMARY KEY,
  contract_version text NOT NULL,
  canon_version text NOT NULL,
  mapping_version text NOT NULL,
  started_at timestamptz NOT NULL DEFAULT now(),
  row_count int,
  state text NOT NULL DEFAULT 'queued'
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
  hd text,
  cdt1 text,
  source_row integer NOT NULL,
  read_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT fls_pm_line_pk PRIMARY KEY (run_id, pm_line_id),
  CONSTRAINT fls_pm_line_run_id_source_row_uq UNIQUE (run_id, source_row)
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
  evt_id bigint REFERENCES fls_queue_event(evt_id)
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
  CONSTRAINT fls_reject_run_id_source_row_uq UNIQUE (run_id, source_row)
);

CREATE TABLE IF NOT EXISTS fls_mapping_master (
  hd_code text NOT NULL PRIMARY KEY,
  need_cfa2 text,
  method_cfa2 text,
  code_hr text,
  coa1 text,
  coa2 text
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
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1;

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
