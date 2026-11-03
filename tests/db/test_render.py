from fls.db.model import Column, Table
from fls.db.render import render_ddl


def test_render_ddl_cot_co_ban():
    t = Table(name="fls_demo", columns=(
        Column("demo_id", "bigint", null=False, pk=True),
        Column("ten", "text", null=False),
        Column("ghi_chu", "text"),
    ))
    sql = render_ddl(t)
    assert sql.startswith("CREATE TABLE IF NOT EXISTS fls_demo (")
    assert "demo_id bigint NOT NULL PRIMARY KEY" in sql
    assert "ten text NOT NULL" in sql
    assert "ghi_chu text," in sql or "ghi_chu text\n" in sql


def test_render_ddl_fk_unique_default_generated():
    t = Table(name="fls_demo", columns=(
        Column("k", "text", null=False, unique=True),
        Column("le", "text", fk="fls_le.le_code"),
        Column("mo", "boolean", null=False, default="false"),
        Column("khac", "boolean", generated="(le IS NOT NULL)"),
    ))
    sql = render_ddl(t)
    assert "k text NOT NULL UNIQUE" in sql
    assert "le text REFERENCES fls_le(le_code)" in sql
    assert "mo boolean NOT NULL DEFAULT false" in sql
    assert "khac boolean GENERATED ALWAYS AS (le IS NOT NULL) STORED" in sql


def test_render_ddl_view_dung_view_sql():
    t = Table(name="v_demo", columns=(Column("a", "text"),),
              kind="view", view_sql="SELECT 'x' AS a")
    assert render_ddl(t) == "CREATE OR REPLACE VIEW v_demo AS SELECT 'x' AS a;"
