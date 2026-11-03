"""Khai bao 10 bang + 2 view cua FLS. Chi khai bao, khong ham.

Nguon: 03_Dev/04_DB_IMPLEMENTATION v1.0 §2-§6b.
LECH CO CHU DICH: bo fls_id_counter, dung SEQUENCE (xem plan P0 Task 3).
"""

from __future__ import annotations

from fls.db.model import Column as C
from fls.db.model import Table

SEQUENCES: dict[str, str] = {
    "seq_itl_id": "CREATE SEQUENCE IF NOT EXISTS seq_itl_id START 1",
}

_FLS_LE = Table(
    name="fls_le", erd_entity="LEGAL_ENTITY",
    island_reason="danh muc phap nhan — fls_itl tro TOI no, khong nguoc lai",
    columns=(
        C("le_code", "text", null=False, pk=True, comment="ma phap nhan"),
        C("le_name", "text", null=False),
        C("is_entity", "boolean", null=False, default="true",
          comment="INV-I10: nhan khong-phai-phap-nhan (USD, HotBonus) => false"),
    ))

_FLS_ITL = Table(
    name="fls_itl", erd_entity="ITL_ROW",
    columns=(
        # -- lop C · danh tinh (INV-I04a/b) --
        C("itl_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')",
          comment="cap luc staged roi DONG BANG; KHONG theo vi tri dong"),
        C("content_key", "text", null=False, unique=True,
          comment="INV-I04b: hash(source_system,source_sheet,doc_date,ps_no,ps_co,doc_no,seq_trung)"),
        # -- lop C · lineage (INV-I05) --
        C("source_system", "text", null=False, comment="P100|Cash|A-CCR|HR|Platform"),
        C("source_sheet", "text", null=False),
        C("source_row", "int", null=False),
        # -- lop C · run (INV-I12) --
        C("run_id", "text", null=False, fk="fls_run.run_id",
          comment="GAP-ERD-P0-01 (owner chot 26/08): FK de go sai run_id bi CHAN, "
                  "khong de dong so mat lineage trong im lang (INV-I05)"),
        C("contract_version", "text", null=False),
        C("canon_version", "text", null=False),
        C("mapping_version", "text", null=False),
        # -- lop C · trang thai --
        C("raw_frozen", "boolean", null=False, default="false",
          comment="INV-I03: true => trigger cam UPDATE/DELETE"),
        C("is_flash", "boolean", null=False, default="true", comment="INV-I14"),
        C("period_state", "text", null=False, default="'open'", comment="INV-I13: open|locked"),
        C("created_at", "timestamptz", null=False, default="now()"),
        # -- lop A · 14 truong ITL-CONTRACT v1.0, doc THEO TEN (QD-ITL-42) --
        C("doc_date", "date", comment="A(0) Ngay chung tu. INV-I11: date khong phai chuoi"),
        C("doc_no", "text", comment="B(1) So chung tu. AUD-12: KHONG mang nghia thoi gian"),
        C("memo", "text", comment="C(2) Dien giai"),
        C("curr", "text", comment="D(3) Don vi tien te"),
        C("ps_no", "numeric(20,2)", comment="E(4) PS No"),
        C("ps_co", "numeric(20,2)", comment="F(5) PS Co"),
        C("acct", "text", comment="G(6) Tai khoan"),
        C("le", "text", fk="fls_le.le_code", comment="P(15) SSOT phap nhan — KHONG dung BL"),
        C("hd", "text", comment="V(21) Final khoi 1 — Budget Code"),
        C("pay_type", "text", comment="Z(25) Final khoi 2 — Loai giao dich"),
        C("cdt1", "text", comment="AD(29) Final khoi 3 — Chu du toan"),
        C("svc_start", "date", comment="AH(33) Final khoi 4"),
        C("svc_end", "date", comment="AL(37) Final khoi 5"),
        # -- lop A' · cot song song (QD-ITL-35) --
        C("hd_thyt", "text", comment="NULL o cho may tu bia. KHONG vao parity"),
        C("pay_type_thyt", "text"),
        C("cdt1_thyt", "text"),
        C("svc_start_thyt", "date"),
        C("svc_end_thyt", "date"),
        C("work_status", "text", null=False, default="'ok'",
          comment="INV-I16: ok|UNMAPPED|rejected"),
        # -- lop A' · khoi 6-7 ngoai hop dong P&L (QD-owner-0824) --
        C("id_payee", "text", comment="AP Final khoi 6 — goi y doc tu canon[Y]"),
        C("invoice", "text", comment="AT Final khoi 7 — link hoa don"),
        # -- lop A' · ALLOCATE: may goi y, nguoi override thang --
        C("cdt1_cfa1", "text", comment="AU goi y = cdt1"),
        C("cdt1_cfa2", "text", comment="AV goi y = VLOOKUP Mapping Master"),
        C("alloc_method", "text", comment="AW goi y = VLOOKUP Mapping Master"),
        C("cdt1_cfa2_classify", "text", comment="SNAPSHOT goi y luc override (US-025)"),
        C("alloc_method_classify", "text"),
        # -- lop A' · phap nhan tra (QD-ITL-10) --
        C("le_payer", "text", fk="fls_le.le_code", comment="ai THUC tra; NULL neu nguon thieu"),
        C("is_intercompany", "boolean",
          generated="(le IS NOT NULL AND le_payer IS NOT NULL AND le <> le_payer)",
          comment="cam nhap tay — may suy"),
        # -- lop A' · audit/workflow --
        C("pic", "text", comment="BJ giu cot, CHUA len UI"),
        C("audit_status", "text", comment="BK khac work_status"),
        # -- lop B · canonical 36 cot --
        C("canon", "jsonb", null=False,
          comment="36 cot nguyen van theo VI TRI — 4 cot AH-AK trung ten, luu theo key la mat cot"),
    ))

_FLS_ADJUSTMENT = Table(
    name="fls_adjustment", erd_entity="ADJUSTMENT_ENTRY",
    columns=(
        C("adj_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("field", "text", null=False),
        C("value_after", "text"),
        C("state", "text", null=False, default="'posted'",
          comment="SM-I03: posted|reversed. KHONG co deleted"),
        C("reversal_of", "bigint", fk="fls_adjustment.adj_id",
          comment="dao chi bang but toan moi (INV-I08)"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
    ))

_FLS_JOURNAL = Table(
    name="fls_journal", erd_entity="JOURNAL",
    columns=(
        C("jrn_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("field", "text", null=False),
        C("value_before", "text"),
        C("value_after", "text"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
        C("value_source", "text", null=False, comment="nguon goi y luc go"),
        C("reason", "text"),
    ))

_FLS_RUN = Table(
    name="fls_run", erd_entity="RUN",
    columns=(
        C("run_id", "text", null=False, pk=True),
        C("contract_version", "text", null=False),
        C("canon_version", "text", null=False),
        C("mapping_version", "text", null=False),
        C("started_at", "timestamptz", null=False, default="now()"),
        C("row_count", "int"),
        C("state", "text", null=False, default="'queued'", comment="SM-I04"),
    ))

_FLS_REJECT = Table(
    name="fls_reject", erd_entity="REJECT",
    columns=(
        C("rej_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("run_id", "text", null=False, fk="fls_run.run_id"),
        C("source_system", "text", null=False),
        C("source_sheet", "text", null=False),
        C("source_row", "int", null=False),
        C("reason", "text", null=False, comment="ACC-4: ly do CO TEN, khong duoc rong"),
    ))

_FLS_MAPPING_MASTER = Table(
    name="fls_mapping_master", erd_entity="MAPPING_MASTER",
    island_reason="danh muc HD — tra theo gia tri hd, khong FK vi hd co the UNMAPPED",
    columns=(
        C("hd_code", "text", null=False, pk=True),
        C("need_cfa2", "text"),
        C("method_cfa2", "text"),
        C("code_hr", "text"),
        C("coa1", "text"),
        C("coa2", "text"),
    ))

_FLS_SOURCE = Table(
    name="fls_source", erd_entity="SOURCE",
    island_reason="manifest pipeline — pipeline ghi, F06 doc (DD-I07)",
    columns=(
        C("source_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("source_key", "text", null=False, unique=True, comment="'R | HoangACB' | 'file>sheet'"),
        C("src_type", "text", null=False, comment="Bank|Cash|CCR|Platform|Mapping"),
        C("last_seen_at", "timestamptz"),
        C("lag_days", "int"),
        C("cutoff_date", "date"),
        C("txn_count", "int"),
    ))

_FLS_QUEUE_EVENT = Table(
    name="fls_queue_event", erd_entity="QUEUE_EVENT",
    columns=(
        C("evt_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("evt_type", "text", null=False, comment="reason|defer"),
        C("reason", "text"),
        C("defer_until", "date"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
    ))

_V_QUEUE_STATE = Table(
    name="fls_queue_state", kind="view", erd_entity="QUEUE_STATE",
    columns=(C("itl_id", "bigint"), C("reason", "text"),
             C("defer_until", "date"), C("defer_count", "int")),
    view_sql="""
SELECT itl_id,
       (ARRAY_AGG(reason ORDER BY at DESC)
          FILTER (WHERE evt_type = 'reason'))[1]            AS reason,
       MAX(defer_until) FILTER (WHERE evt_type = 'defer')   AS defer_until,
       COUNT(*) FILTER (WHERE evt_type = 'defer')::int      AS defer_count
FROM fls_queue_event
GROUP BY itl_id""".strip())

_V_QUEUE_REASON_WEEKLY = Table(
    name="fls_queue_reason_weekly", kind="view", erd_entity="QUEUE_REASON_WEEKLY",
    columns=(C("tuan", "date"), C("so_lan", "int")),
    view_sql="""
SELECT DATE_TRUNC('week', at)::date AS tuan,
       COUNT(*)::int                AS so_lan
FROM fls_queue_event
WHERE evt_type = 'reason'
GROUP BY 1
ORDER BY 1 DESC""".strip())

_FLS_MIGRATION = Table(
    name="fls_migration", erd_entity="MIGRATION",
    island_reason="so ghi cac lan di tru — ha tang, khong gan dong so nao",
    columns=(
        C("version", "int", null=False, pk=True),
        C("name", "text", null=False),
        C("checksum", "text", null=False, comment="sha256 file .sql — sua sau khi ap la NO"),
        C("applied_at", "timestamptz", null=False, default="now()"),
    ))

TABLES: dict[str, Table] = {t.name: t for t in (
    _FLS_LE, _FLS_RUN, _FLS_ITL, _FLS_ADJUSTMENT, _FLS_JOURNAL, _FLS_REJECT,
    _FLS_MAPPING_MASTER, _FLS_SOURCE, _FLS_QUEUE_EVENT,
    _V_QUEUE_STATE, _V_QUEUE_REASON_WEEKLY, _FLS_MIGRATION,
)}

CREATE_ORDER: tuple[str, ...] = (
    "fls_le", "fls_run", "fls_itl", "fls_adjustment", "fls_journal",
    "fls_reject", "fls_mapping_master", "fls_source", "fls_queue_event",
    "fls_queue_state", "fls_queue_reason_weekly",
)

# Bang do RUNNER di tru tu tao truoc khi ap migration dau tien, nen CO Y khong
# nam trong CREATE_ORDER. Moi ten o day phai co ly do — giong luat ERD_ISLANDS.
BOOTSTRAP: frozenset[str] = frozenset({
    "fls_migration",   # phai ton tai TRUOC migration 0001 nen khong the la 0001
})
