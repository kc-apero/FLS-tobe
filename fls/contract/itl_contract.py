"""ITL-CONTRACT v1.0 — DONG BANG 2026-08-24 (QD-ITL-42).

14 truong, doc THEO TEN. Cot Excel chi de doi chieu reader dang chay.
le = cot P (QD-owner-0820), KHONG phai BL.
Doi file nay la CR loai 3, kem test tuong thich (02_REPO_CONVENTIONS §4.5).
"""

from __future__ import annotations

ITL_CONTRACT_V1: tuple[tuple[str, str, str], ...] = (
    ("doc_date", "date", "A"),
    ("doc_no", "text", "B"),
    ("memo", "text", "C"),
    ("curr", "text", "D"),
    ("ps_no", "numeric", "E"),
    ("ps_co", "numeric", "F"),
    ("acct", "text", "G"),
    ("le", "text", "P"),
    ("itl_id", "bigint", "R"),
    ("hd", "text", "V"),
    ("pay_type", "text", "Z"),
    ("cdt1", "text", "AD"),
    ("svc_start", "date", "AH"),
    ("svc_end", "date", "AL"),
)
