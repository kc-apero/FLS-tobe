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
    # ⭐ `WO-023` `(d)` *(`BA-07` v3.5 §5)*: ba ca tung muon ma tren nay — moi
    #   chuyen mot ma, van `409`. `CONFLICT-SOURCE` **chi** con cho `US-025`.
    "FLS-DA-GHEP": (409, "dong DA co moi noi hieu luc — ⛔ ghep chong"),
    "FLS-KHONG-CON-MOI-NOI": (409, "dong ⛔ con moi noi hieu luc de bo"),
    "FLS-CHUA-XONG": (409, "dong chua tung bam xong — ⛔ co gi de mo lai"),
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
    # ⭐ `CR#11` §4b ⓺ — nhom NAP.
    #
    # ⚠ `FLS-KHAI-KHONG-CO` la **409 ⛔ KHONG phai 404**: nguon **co ton
    #   tai**, chi la ⛔ chua ai khai cach doc no. Hai cau tra loi khac
    #   nhau dan nguoi dung di **hai duong sua khac nhau** — mot ben la
    #   "go lai `source_id`", ben kia la "khai cot cho nguon nay".
    "FLS-KHAI-KHONG-CO": (409, "nguon CO nhung ⛔ chua ai khai cach doc no"),
    "FLS-KHAI-THIEU": (422, "ban khai thieu truong trong 6 — ⛔ khong nap mot phan"),
    "FLS-SOAT-CHAN": (422, "co luat hang CHAN do ⇒ ⛔ khong ghi dong nao"),
    "FLS-NGUON-LA": (404, "source_id ⛔ khong co trong fls_source"),
    # ⭐⭐ `QĐ-ITL-110` — lan ANH CHUP. HAI ma, ⛔ KHONG mot, va cung ly do da
    #    tach `FLS-NGUON-LA` (404) khoi `FLS-KHAI-KHONG-CO` (409):
    #      · ⛔ khong co anh chup ay          → **404**, di sua `chup_id`;
    #      · anh CO nhung ⛔ khong doc nguon  → **409**, di CHUP LAI.
    #    Gop chung lai thi nguoi dung doc "khong tim thay" roi go lai dung cai
    #    `chup_id` ay lan nua — mot cua bat nguoi ta thu lai cai vua that bai.
    "FLS-CHUP-KHONG-CO": (404, "⛔ khong co anh chup `chup_id` ay"),
    "FLS-CHUP-KHONG-NGUON": (409, "anh chup CO nhung no ⛔ khong doc nguon nay"),
    # ⭐⭐ `QĐ-ITL-117` — khai thu tu CA LO. **422 ⛔ khong 409**: than yeu cau
    #    doc duoc va nguon co that; cai ⛔ khong dat la **BANG CHUNG**. Cung
    #    hang voi `FLS-SOAT-CHAN`, va cung mot hau qua: **⛔ 0 ban khai moi**.
    "FLS-THU-TU-KHONG-TU-CHUNG": (
        422, "co nguon ⛔ KHONG tu chung thu tu ngay (hay BAT DONG voi ban "
             "khai cua nguoi) ⇒ TU CHOI CA LO, ⛔ 0 ban khai moi"),
    # ⭐⭐ `QĐ-ITL-118` — ghep CA LO. Cung khuon `422` voi cu tren, va cung mot
    #    hau qua: **⛔ 0 moi noi moi**. ⚠ `ly_do` cua tung dong noi ro no vuong
    #    cong NAO cua `ghep_lenh` — mot cau chi noi *"khong tu chung"* se lam
    #    nguoi ta di sua dung sai trong khi dong ay khac TIEN TE.
    "FLS-GHEP-KHONG-TU-CHUNG": (
        422, "co dong ⛔ KHONG tu chung (khac tien te / da bi ghep / chua "
             "duyet / lech tien) ⇒ TU CHOI CA LO, ⛔ 0 moi noi moi"),
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
# ⛔⛔ `bien_ban` (08/09) — **mot lo tiem an, lo ra vi mot thay doi KHAC.**
#    `nap_cua.nap()` da nem `LoiCua("FLS-SOAT-CHAN", …, bien_ban=…)` tu luc
#    tuyen nay ra doi, va cau ay **dung**: noi *"bi chan"* ma ⛔ khong noi
#    **chan vi luat nao** la bat nguoi dung doan. Nhung `bien_ban` ⛔ chua
#    bao gio duoc khai o day ⇒ duong `422` se **NO KeyError** ngay khi co
#    mot lo that bi chan.
#
# ⭐ Vi sao no song sot: ⛔ **khong bai nao tung lam do mot luat hang
#    `CHAN`** — moi bai deu dung du lieu sach nen `S1` luon dat. Lo chi lo
#    ra khi `S10` (`GAP-KHAI-01`) them mot luat `CHAN` co the do tren kho
#    TRONG. ⇒ Bai hoc: mot nhanh loi ⛔ chua ai di qua la mot nhanh **chua
#    biet co chay**, du no da nam trong ma nhieu ngay.
KHOA_THEM: frozenset[str] = frozenset({"khac", "gia_tri_go", "bien_ban"})


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
