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


def render_ddl(t: Table) -> str:
    if t.kind == "view":
        return f"CREATE OR REPLACE VIEW {t.name} AS {t.view_sql};"
    body = ",\n  ".join(_render_column(c) for c in t.columns)
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
            khoa = "PK" if c.pk else ("FK" if c.fk else "")
            lines.append(f"        {c.type.split('(')[0]} {c.name} {khoa}".rstrip())
        lines.append("    }")
    for name in sorted(tables):
        for c in tables[name].columns:
            if c.fk:
                lines.append(f'    {c.fk.split(".")[0]} ||--o{{ {name} : "{c.name}"')
    return "\n".join(lines) + "\n"
