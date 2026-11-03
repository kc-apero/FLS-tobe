from fls.db.render import render_ddl
from fls.db.schema import CREATE_ORDER, SEQUENCES, TABLES

CONTRACT_14 = ("doc_date", "doc_no", "memo", "curr", "ps_no", "ps_co", "acct",
               "le", "itl_id", "hd", "pay_type", "cdt1", "svc_start", "svc_end")


def test_khong_con_fls_id_counter():
    """FPS da khai tu pattern counter — FLS khong duoc copy lai."""
    assert "fls_id_counter" not in TABLES
    assert "seq_itl_id" in SEQUENCES


def test_itl_id_sinh_bang_sequence_va_la_pk():
    col = {c.name: c for c in TABLES["fls_itl"].columns}["itl_id"]
    assert col.pk is True
    assert col.default == "nextval('seq_itl_id')"


def test_du_14_truong_hop_dong():
    have = {c.name for c in TABLES["fls_itl"].columns}
    assert set(CONTRACT_14) <= have


def test_5_cot_thyt_va_canon_co_trong_migration_dau():
    """QD-ITL-35: them sau la migration tren bang da day du lieu."""
    have = {c.name for c in TABLES["fls_itl"].columns}
    assert {"hd_thyt", "pay_type_thyt", "cdt1_thyt",
            "svc_start_thyt", "svc_end_thyt", "canon"} <= have


def test_lineage_va_run_deu_not_null():
    cols = {c.name: c for c in TABLES["fls_itl"].columns}
    for n in ("source_system", "source_sheet", "source_row", "run_id",
              "contract_version", "canon_version", "mapping_version"):
        assert cols[n].null is False, n


def test_content_key_unique():
    cols = {c.name: c for c in TABLES["fls_itl"].columns}
    assert cols["content_key"].unique is True
    assert cols["content_key"].null is False


def test_fls_itl_dung_dau_create_order():
    assert CREATE_ORDER[0] == "fls_le", "fls_le la cha FK, phai truoc"
    assert "fls_itl" in CREATE_ORDER


def test_render_duoc_khong_no():
    assert render_ddl(TABLES["fls_itl"]).startswith("CREATE TABLE IF NOT EXISTS fls_itl (")


import pathlib

GOLDEN = pathlib.Path(__file__).resolve().parents[1] / "golden" / "ddl.sql"


def test_golden_ddl_khop(request):
    """Anh chup DDL de doc bang mat trong diff cua PR.

    Duong dan neo theo __file__ (khong theo cwd) — chay pytest tu thu muc nao
    cung ra cung mot file, neu khong cong se do gia hoac xanh gia.
    """
    out = "\n\n".join(
        [*(s + ";" for s in SEQUENCES.values()),
         *(render_ddl(TABLES[n]) for n in CREATE_ORDER)]) + "\n"
    if request.config.getoption("--update-golden", default=False):
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8", newline="\n")
    assert GOLDEN.read_text(encoding="utf-8") == out, (
        "DDL doi ma golden chua cap nhat. Chay: pytest --update-golden")
