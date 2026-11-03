"""Lop so mong: canon + ngu canh run -> payload de repo ghi vao fls_itl.

Dung "mong" theo nghia 01_TECH_DESIGN §2: 6 phep chep + 1 phep danh so
+ 5 cau if giong nhau + 1 phep join. ⛔ Khong luat phan loai nao o day —
luat phan loai thuoc adapter (thuong nguon).

Phep danh so KHONG nam trong module nay: itl_id do SEQUENCE cua DB cap
(INV-I04a). Lop so tu danh so la cach tai lap dung loi AS-IS.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from typing import Any

from fls.canon.row import CanonRow
from fls.canon.validate import parse_ngay, parse_so, validate
from fls.ledger.final_rule import NAM_KHOI, TEN_KHOI, tinh_final

# Vi tri trong khuon CANON (⛔ khong phai cua ITL Ledge — xem spec.py)
_NGAY, _SO_CT, _MEMO, _CURR, _NO, _CO, _ACCT = 0, 1, 2, 3, 4, 5, 6
_LE = 32            # AG · "LE" — ⛔ KHONG dung AH-AK (4 cot trung ten)
_LE_PAYER = 11      # L  · "Phap nhan thanh toan"
_PM_LINE = 13       # N  · "ID PMLine" — lineage phai song sot (QD-ITL-20/CR#1)


@dataclass(frozen=True)
class NgucCanh:
    run_id: str
    contract_version: str
    canon_version: str
    mapping_version: str
    source_system: str
    source_sheet: str


def content_key(source_system: str, source_sheet: str, doc_date: date | None,
                ps_no: Any, ps_co: Any, doc_no: str | None,
                seq_trung: int) -> str:
    """Khoa DOI SANH (INV-I04b). ⛔ KHONG phai danh tinh — danh tinh la itl_id.

    ⛔ KHONG chua vi tri dong: 281 dong trung noi dung + 103 dong khong co so
    chung tu, nen khoa noi dung mot minh khong du lam danh tinh; `seq_trung` la
    tham so TUONG MINH do goi truyen vao, khong phai may tu doan.
    """
    thanh_phan = "".join((
        str(source_system), str(source_sheet),
        doc_date.isoformat() if doc_date else "",
        "" if ps_no is None else repr(ps_no),
        "" if ps_co is None else repr(ps_co),
        "" if doc_no is None else str(doc_no),
        str(seq_trung),
    ))
    return hashlib.sha256(thanh_phan.encode("utf-8")).hexdigest()


def dung_dong(row: CanonRow, source_row: int, nc: NgucCanh,
              khoi: dict[str, tuple[str | None, str | None]] | None = None,
              seq_trung: int = 0) -> dict[str, Any]:
    """Dung payload mot dong fls_itl. Dong bi LOAI thi NO, khong am tham dung."""
    kq = validate(row)
    if kq.loai:
        raise ValueError("khong the dung dong, phai vao fls_reject: "
                         + " | ".join(kq.loai))

    sai = set(khoi or {}) - TEN_KHOI
    if sai:
        raise ValueError(f"khoi khong thuoc 5 khoi cua so: {sorted(sai)}")

    ngay = parse_ngay(row.at(_NGAY))
    ps_no, ps_co = parse_so(row.at(_NO)), parse_so(row.at(_CO))

    d: dict[str, Any] = {
        # 6 phep chep BASE + tai khoan
        "doc_date": ngay,
        "doc_no": row.at(_SO_CT),
        "memo": row.at(_MEMO),
        "curr": row.at(_CURR),
        "ps_no": ps_no,
        "ps_co": ps_co,
        "acct": row.at(_ACCT),
        # 1 phep join: phap nhan
        "le": row.at(_LE),
        "le_payer": row.at(_LE_PAYER),
        # lineage + run (INV-I05 / INV-I12) — khong bao gio NULL
        "source_system": nc.source_system,
        "source_sheet": nc.source_sheet,
        "source_row": source_row,
        "run_id": nc.run_id,
        "contract_version": nc.contract_version,
        "canon_version": nc.canon_version,
        "mapping_version": nc.mapping_version,
        # khoa doi sanh
        "content_key": content_key(nc.source_system, nc.source_sheet, ngay,
                                   ps_no, ps_co, row.at(_SO_CT), seq_trung),
        # 36 truong nguyen van theo VI TRI (38 o, ke ca 2 o trong)
        "canon": row.as_jsonb_list(),
    }

    # 5 cau if giong nhau
    co_bia = False
    for ten, ten_thyt in NAM_KHOI:
        cls, man = (khoi or {}).get(ten, (None, None))
        r = tinh_final(cls, man)
        d[ten], d[ten_thyt] = r.parity, r.thyt
        co_bia = co_bia or r.may_tu_bia

    d["work_status"] = "UNMAPPED" if (co_bia or kq.cho) else "ok"
    return d
