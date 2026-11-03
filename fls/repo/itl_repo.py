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
    # LO 2026-08-26: bon cot duoi bi BO SOT — lop so tinh ra tu P1 ma tang ghi
    # khong ghi. Hai cot dau DB DA CO SAN. `_gia_tri` chi kiem khoa THIEU nen
    # khoa THUA roi ra ngoai trong im lang.
    "id_payee", "invoice", "id_payee_thyt", "invoice_thyt",
    "pm_hinh",
    "work_status", "canon",
)

_SQL = (
    "INSERT INTO fls_itl (" + ", ".join(_COT) + ") VALUES ("
    + ", ".join("%s" for _ in _COT) + ") RETURNING itl_id"
)


def _gia_tri(p: dict[str, Any]) -> tuple[Any, ...]:
    """⛔ Kiem CA HAI chieu: thieu VA thua.

    Ban dau ham nay chi kiem THIEU. Nen khi lop so tinh ra mot gia tri ma `_COT`
    chua co ten, gia tri do **roi ra ngoai khong ai biet** — dung 26/08 da mat
    `id_payee`, `invoice`, `id_payee_thyt`, `invoice_thyt` theo duong nay.
    Mot cot moi o lop so gio se lam NO TO thay vi bien mat.
    """
    thieu = [c for c in _COT if c not in p]
    if thieu:
        raise ValueError(f"payload thieu cot: {thieu}")
    thua = sorted(k for k in p if k not in _COT)
    if thua:
        raise ValueError(
            f"payload co cot tang ghi KHONG ghi: {thua} — them vao _COT "
            f"(va vao schema + migration) chu dung de roi im lang")
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


# ⚠ Bien the DUY NHAT co ON CONFLICT. Van la APPEND (INV-I08): no khong sua dong
# cu, chi KHONG chen dong moi. Dung cho lan nap LAI cung mot nguon — chay 2 lan
# phai cho cung ket qua (cong chung #4), ma content_key la UNIQUE nen lan 2 se
# no neu khong co duong nay.
_SQL_BO_QUA = _SQL.replace(") RETURNING itl_id",
                           ") ON CONFLICT (content_key) DO NOTHING RETURNING itl_id")


def chen_bo_qua_trung(conn, payloads: Sequence[dict[str, Any]]
                      ) -> list[int | None]:
    """Chen mot lo, BO QUA dong da co content_key. Tra danh sach THANG HANG voi
    `payloads`: `itl_id` neu da chen, `None` neu bo qua.

    ⛔ KHONG phai UPDATE: dong da nam trong so thi giu nguyen, khong ai ghi de.

    ⚠ Vi sao tra danh sach thang hang chu khong tra (ids, so_bo_qua): ben goi con
    phai dem `work_status` cua nhung dong THUC SU vao so. Neu chi biet "bo qua 5
    dong" ma khong biet la dong nao thi con so `UNMAPPED` se dem ca dong khong
    vao so — va cong ba duong se bao lech GIA o moi lan nap lai.
    """
    if not payloads:
        return []
    ra: list[int | None] = []
    with conn.cursor() as cur:
        for p in payloads:
            cur.execute(_SQL_BO_QUA, _gia_tri(p))
            r = cur.fetchone()
            ra.append(None if r is None else r[0])
    return ra
