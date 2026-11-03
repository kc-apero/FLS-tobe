"""Vo boc cau tra loi: `{data, error, meta}` (`BA-07` §1) + ma loi (§5).

⛔⛔ **Tien ra JSON la CHUOI, ⛔ khong phai so.** JSON ⛔ khong noi kieu, nen may
doc (JavaScript o `P6`) bien moi so thanh `float64` **truoc khi ai kip chon**.
Tra chuoi la cach duy nhat cua doc ⛔ khong giao pho quyet dinh do cho may khac.

⚠ **Va day la hang rao dat truoc, ⛔ khong phai vet dang chay mau** — toi da
tung viet o day rang so 1.214 ty lam `float` mat mot phan xu, va **do la sai**:
`float` giu ~15-17 chu so co nghia, 1.214 ty kem hai so le moi la **15**. Cho
mat that su bat dau khoang **17** chu so, tuc con cach ~1.000 lan. Bai
`test_do_KHOANG_CACH_den_cho_float_bat_dau_mat_chu_so` ghim ca hai moc.

★ `data_status` (`INV-I14`): so chua chot **luon mang co**. Mac dinh la `flash`
— ⛔ mac dinh KHONG duoc la `reconciled`, vi mot con so chua doi soat ma khoac
nhan da doi soat la loai sai te nhat cua ca lop bao cao.
"""
from __future__ import annotations

import datetime as _dt
import json
import uuid
from dataclasses import dataclass, is_dataclass, asdict
from decimal import Decimal
from typing import Any

# `BA-07` §5 — ma loi. Them ma moi thi them o day, ⛔ khong go chuoi tai cho.
MA_LOI: dict[str, tuple[int, str]] = {
    "FLS-CONFLICT-SOURCE": (409, "gia tri go khac nguon, chua `force`"),
    "FLS-LOCKED-PERIOD": (409, "ghi vao ky da chot"),
    "FLS-CONTRACT-DRIFT": (500, "reader lech ITL-CONTRACT"),
    "FLS-DQ-FAILED": (422, "cong ACC-1…4 khong dat"),
    "FLS-UNMAPPED-HIDDEN": (422, "co ghi gia tri cung vao cho UNMAPPED"),
    "FLS-ACCR-UNREADABLE": (503, "khong doc duoc ket qua A-CCR"),
    # P4 them:
    "FLS-UNAUTHORIZED": (401, "the khong hop le hay thieu the"),
    "FLS-NOT-FOUND": (404, "khong co, hay co ma ngoai pham vi"),
    "FLS-BAD-REQUEST": (400, "tham so sai"),
    "FLS-METHOD": (405, "duong nay khong nhan phuong thuc do"),
    "FLS-TOO-LARGE": (413, "than yeu cau qua to"),
    "FLS-INTERNAL": (500, "loi trong may"),
}

TRANG_THAI = ("flash", "reconciled", "signed")


@dataclass(frozen=True)
class Meta:
    request_id: str
    pham_vi: str
    as_of: str
    data_status: str = "flash"
    contract_version: str | None = None
    run_id: str | None = None

    def __post_init__(self) -> None:
        if self.data_status not in TRANG_THAI:
            raise ValueError(f"data_status={self.data_status!r} khong biet")


def _bay_gio() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def meta(pham_vi: str, *, data_status: str = "flash",
         contract_version: str | None = None, run_id: str | None = None) -> Meta:
    return Meta(request_id=uuid.uuid4().hex, pham_vi=pham_vi, as_of=_bay_gio(),
                data_status=data_status, contract_version=contract_version,
                run_id=run_id)


def _thuong(o: Any) -> Any:
    """⛔ `Decimal` → chuoi. Ngay → ISO. Khong bao gio → `float`."""
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, (_dt.date, _dt.datetime)):
        return o.isoformat()
    if isinstance(o, (set, frozenset, tuple)):
        return list(o)
    if is_dataclass(o) and not isinstance(o, type):
        return asdict(o)
    if isinstance(o, memoryview):
        return o.tobytes().decode("utf-8", "replace")
    raise TypeError(f"⛔ khong biet dua {type(o).__name__} ra JSON — khai o "
                    f"`_thuong` chu ⛔ dung de no thanh chuoi bua")


def dong_goi(data: Any, m: Meta) -> bytes:
    return json.dumps({"data": data, "error": None, "meta": asdict(m)},
                      default=_thuong, ensure_ascii=False).encode()


# ⛔ Khoa DUOC phep xuat hien trong `error`. Ban TRANG, vi phan `them` di ra
# ngoai HTTP: mot ma loi vo tinh mang theo mot truong noi bo la mot cho ro.
# ⭐ `khac` la cho `409 FLS-CONFLICT-SOURCE` noi *"nguon dang la X"* — thieu no
# thi man hinh khong the hoi *"ghi de khong?"* mot cach tu te (`US-025`).
KHOA_THEM: frozenset[str] = frozenset({"khac", "gia_tri_go"})


def dong_goi_loi(ma: str, m: Meta, chi_tiet: str = "",
                 **them: Any) -> tuple[int, bytes]:
    """Tra (ma HTTP, than). ⛔ `ma` phai co trong `MA_LOI`.

    `them` chi nhan khoa trong `KHOA_THEM` — khoa la thi **NO**, ⛔ khong am
    tham bo qua: mot truong noi bo di ra ngoai trong im lang la mot cho ro.
    """
    if ma not in MA_LOI:
        raise KeyError(f"ma loi {ma!r} chua khai trong MA_LOI")
    la = sorted(k for k in them if k not in KHOA_THEM)
    if la:
        raise KeyError(f"khoa {la} chua khai trong KHOA_THEM — phan `them` di "
                       f"ra ngoai HTTP nen phai duoc khai tuong minh")
    http, mo_ta = MA_LOI[ma]
    than = json.dumps(
        {"data": None,
         "error": {"code": ma, "message": mo_ta,
                   **({"detail": chi_tiet} if chi_tiet else {}),
                   **{k: v for k, v in them.items() if v is not None}},
         "meta": asdict(m)}, default=_thuong, ensure_ascii=False).encode()
    return http, than
