"""SSOT của schema fls_*. Khai báo MỘT lần, sinh ra cả DDL lẫn ERD.

Vì sao không dùng dict[str, str] DDL thô như FPS: không sinh được ERD từ chuỗi SQL
mà không viết bộ phân tích SQL, và drift ERD là rủi ro số một (03_IMPLEMENTATION_PLAN §1).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Column:
    name: str
    type: str
    null: bool = True
    default: str | None = None
    fk: str | None = None          # "bang.cot"
    pk: bool = False
    unique: bool = False
    generated: str | None = None   # biểu thức của GENERATED ALWAYS AS ... STORED
    comment: str = ""


@dataclass(frozen=True)
class Table:
    name: str
    columns: tuple[Column, ...]
    kind: str = "table"            # "table" | "view"
    erd_entity: str = ""           # tên entity tương ứng trên ERD của BA
    island_reason: str = ""        # lý do KHÔNG có FK về fls_itl (G-ERD-3)
    view_sql: str = ""
