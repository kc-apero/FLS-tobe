"""Tang truy cap DB cho fls_itl. Chỗ DUY NHAT chạm bảng này.

INV-I08: ghi la THEM. ⛔ Khong ham nao o day phat UPDATE hay DELETE len fls_itl —
sua chi bang but toan moi trong fls_adjustment. Co test quet ma nguon.

SQL viet nguyen van, tham so hoa qua psycopg. ⛔ Khong noi chuoi SQL.
"""

from __future__ import annotations

import json
from typing import Any, Sequence

# Thu tu cot dung CHUNG cho INSERT — khai mot lan de cau lenh va gia tri
# khong the lech nhau.
_COT: tuple[str, ...] = (
    "content_key", "source_system", "source_sheet", "source_row",
    "run_id", "contract_version", "canon_version", "mapping_version",
    "doc_date", "doc_no", "memo", "curr", "ps_no", "ps_co", "acct",
    "le", "le_payer",
    "hd", "pay_type", "cdt1", "svc_start", "svc_end",
    "hd_thyt", "pay_type_thyt", "cdt1_thyt", "svc_start_thyt", "svc_end_thyt",
    "work_status", "canon",
)

_SQL = (
    "INSERT INTO fls_itl (" + ", ".join(_COT) + ") VALUES ("
    + ", ".join("%s" for _ in _COT) + ") RETURNING itl_id"
)


def _gia_tri(p: dict[str, Any]) -> tuple[Any, ...]:
    thieu = [c for c in _COT if c not in p]
    if thieu:
        raise ValueError(f"payload thieu cot: {thieu}")
    return tuple(json.dumps(p[c], default=str) if c == "canon" else p[c]
                 for c in _COT)


def chen_mot(conn, payload: dict[str, Any]) -> int:
    """Chen mot dong, tra itl_id do SEQUENCE cua DB cap."""
    with conn.cursor() as cur:
        cur.execute(_SQL, _gia_tri(payload))
        return cur.fetchone()[0]


def chen(conn, payloads: Sequence[dict[str, Any]]) -> list[int]:
    """Chen mot lo. Lo rong thi khong cham DB."""
    if not payloads:
        return []
    with conn.cursor() as cur:
        return [
            (cur.execute(_SQL, _gia_tri(p)), cur.fetchone()[0])[1]
            for p in payloads
        ]
