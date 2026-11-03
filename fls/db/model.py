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
    # Khoá NHIỀU CỘT — thêm 2026-08-27, đóng `GAP-DB-P0-03`.
    # ⛔ Trước đó khuôn này chỉ khai được khoá MỘT cột, nên `fls_reject` không có
    # `UNIQUE(run_id, source_row)` ở tầng kho: lớp chặn trùng duy nhất là điều
    # kiện trong câu `INSERT`. Và `fls_pm_link` (một dòng sổ → N dòng lệnh) thì
    # KHÔNG THỂ khai nổi nếu không có khoá hai cột.
    pk_cols: tuple[str, ...] = ()
    unique_keys: tuple[tuple[str, ...], ...] = ()


def kiem_khai_bao(t: Table) -> list[str]:
    """Lỗi tự-mâu-thuẫn trong một bản khai. Rỗng = sạch.

    ⛔ Hai chỗ khai CÙNG một khoá là đúng cái bệnh cả khuôn này chữa — nên
    khai khoá ở cả cột lẫn bảng là LỖI, không phải "ghi cho chắc".
    """
    ra: list[str] = []
    ten = {c.name for c in t.columns}
    pk_cot = [c.name for c in t.columns if c.pk]

    if t.pk_cols and pk_cot:
        ra.append(f"{t.name}: khoá chính khai HAI CHỖ — cột {pk_cot} và bảng "
                  f"{list(t.pk_cols)}. Chọn một chỗ.")
    for c in t.pk_cols:
        if c not in ten:
            ra.append(f"{t.name}: pk_cols có {c!r} mà bảng không có cột đó")
    if len(set(t.pk_cols)) != len(t.pk_cols):
        ra.append(f"{t.name}: pk_cols có cột lặp {list(t.pk_cols)}")
    for k in t.unique_keys:
        if not k:
            ra.append(f"{t.name}: unique_keys có một khoá RỖNG")
        for c in k:
            if c not in ten:
                ra.append(f"{t.name}: unique_keys có {c!r} mà bảng không có cột đó")
        if len(k) == 1:
            ra.append(f"{t.name}: unique_keys {list(k)} chỉ MỘT cột — khai "
                      f"`unique=True` ngay ở cột đó, đừng tạo chỗ khai thứ hai")
    if t.kind == "view" and (t.pk_cols or t.unique_keys):
        ra.append(f"{t.name}: là VIEW mà khai khoá — view không có ràng buộc")
    return ra
