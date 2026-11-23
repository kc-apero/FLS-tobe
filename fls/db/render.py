"""Sinh DDL và ERD từ fls.db.model. Thuần hàm, không chạm DB."""

from __future__ import annotations

from fls.db.model import Column, Table


def _render_column(c: Column) -> str:
    parts = [c.name, c.type]
    if c.generated:
        parts.append(f"GENERATED ALWAYS AS {c.generated} STORED")
        return " ".join(parts)
    if not c.null:
        parts.append("NOT NULL")
    if c.default is not None:
        parts.append(f"DEFAULT {c.default}")
    if c.pk:
        parts.append("PRIMARY KEY")
    if c.unique:
        parts.append("UNIQUE")
    if c.fk:
        table, col = c.fk.split(".")
        parts.append(f"REFERENCES {table}({col})")
    return " ".join(parts)


def _render_rang_buoc(t: Table) -> list[str]:
    """Rang buoc muc BANG — khoa NHIEU COT (`GAP-DB-P0-03`, 27/08).

    Ten dat theo `<bang>_<cot>_<loai>` de `pg_verify` doi chieu duoc: mot rang
    buoc KHAI ma khong AP thi phai DO, ⛔ khong im lang — dung benh ma cong thu
    5 sinh ra de chan (`CREATE TABLE IF NOT EXISTS` bo qua trong im lang).
    """
    ra = []
    if t.pk_cols:
        ra.append(f"CONSTRAINT {t.name}_pk PRIMARY KEY ({', '.join(t.pk_cols)})")
    for k in t.unique_keys:
        ra.append(f"CONSTRAINT {t.name}_{'_'.join(k)}_uq UNIQUE ({', '.join(k)})")
    # ⭐ `CHECK` khai o muc COT nhung SINH ra o muc BANG, **co ten** — de
    #   `pg_verify` doi chieu duoc theo ten. Mot `CHECK` noi dong khuyet danh
    #   thi Postgres tu dat ten (`fls_x_check`, `fls_x_check1`, …) va cong ⛔
    #   khong con cach nao noi *"rang buoc NAY khai ma chua ap"*.
    for c in t.columns:
        if c.check:
            ra.append(f"CONSTRAINT {t.name}_{c.name}_ck CHECK ({c.check})")
    return ra


def render_ddl(t: Table) -> str:
    if t.kind == "view":
        return f"CREATE OR REPLACE VIEW {t.name} AS {t.view_sql};"
    phan = [_render_column(c) for c in t.columns] + _render_rang_buoc(t)
    body = ",\n  ".join(phan)
    return f"CREATE TABLE IF NOT EXISTS {t.name} (\n  {body}\n);"


def render_erd_json(tables: dict[str, Table]) -> dict:
    """Hien vat ERD dang may doc duoc. Sap xep on dinh de diff sach."""
    entities = []
    relations = []
    for name in sorted(tables):
        t = tables[name]
        entities.append({
            "table": t.name,
            "kind": t.kind,
            "erd_entity": t.erd_entity,
            "island_reason": t.island_reason,
            "columns": [{"name": c.name, "type": c.type, "null": c.null,
                         "pk": c.pk, "unique": c.unique, "fk": c.fk}
                        for c in t.columns],
            "pk_cols": list(t.pk_cols),
            "unique_keys": [list(k) for k in t.unique_keys],
        })
        for c in t.columns:
            if c.fk:
                relations.append({"from": t.name, "to": c.fk.split(".")[0],
                                  "via": c.name})
    relations.sort(key=lambda r: (r["from"], r["to"], r["via"]))
    return {"contract": "ERD-CONTRACT", "version": 1,
            "entities": entities, "relations": relations}


def render_erd_mermaid(tables: dict[str, Table]) -> str:
    lines = ["erDiagram"]
    for name in sorted(tables):
        t = tables[name]
        lines.append(f"    {t.name} {{")
        for c in t.columns:
            khoa = "PK" if (c.pk or c.name in t.pk_cols) else ("FK" if c.fk else "")
            lines.append(f"        {c.type.split('(')[0]} {c.name} {khoa}".rstrip())
        lines.append("    }")
    for name in sorted(tables):
        for c in tables[name].columns:
            if c.fk:
                lines.append(f'    {c.fk.split(".")[0]} ||--o{{ {name} : "{c.name}"')
    return "\n".join(lines) + "\n"
