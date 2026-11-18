"""`IX.PL` — **dòng PL là biểu thức trên cây HD** + 2 phép CHECK *(AP v3.1.2 §3.2.3
IX.PL · §3.2.4 "dòng PL viết trong ô ATL … hai định nghĩa" · ISP 3.1.2 Step 26 · `C12`
· `WO-184`)*.

⭐ MỘT định nghĩa cho mỗi dòng `PL2…PL8` *(`DINH_NGHIA`, bản ATL — đề xuất A của §3.2.3)*.
   Ngữ pháp TỐI THIỂU: mã HD · `+` · `-`/`−` · ngoặc *(+ dấu đơn ngôi)*. ⛔⛔ KHÔNG `eval`/
   `exec`/`compile`: chuỗi → token *(regex)* → cây → cộng/trừ; ký tự ngoài ngữ pháp là
   `PL_CU_PHAP`, ⛔ được "thử chạy".
⛔ Lỗi mang TÊN *(hằng chuỗi, `LoiPL.ten` là TẬP — bài so `X ∈ ten`)*, gom HẾT lý do.
⛔ Giá trị HD thiếu ⇒ `PL_THIEU_GIA_TRI`, ⛔ ngầm `0` *(`Đ3`: CHECK xanh trên tập rỗng)*.

⚠ **Chênh định nghĩa ATL ↔ Mapping Master** *(`CHENH_VOI_MM`)*: ghi thành DANH SÁCH cho owner,
   ⛔ tự hoà giải. Nguồn của `DINH_NGHIA` là CÔNG THỨC Ô THẬT của sheet ATL *(dòng 81…87, xem chú thích
   ở `DINH_NGHIA`; `C12-R1-01`)*, ⛔ hàng "606" mô tả; ảnh MM `mapping_master_cfg.json` chỉ giữ LỜI MÔ TẢ chữ của mỗi dòng PL.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from fls.cau_hinh import hd

BANG = "IX.PL"

PL_CU_PHAP = "PL_CU_PHAP"                 # ký tự/ngữ pháp ngoài {mã, + −, ngoặc}
PL_MA_LA = "PL_MA_LA"                     # mã ⛔ có trong cây HD (hay ⛔ trong giá trị)
PL_CHU_TRINH = "PL_CHU_TRINH"             # PL2 → PL3 → PL2
PL_THIEU_GIA_TRI = "PL_THIEU_GIA_TRI"     # cây có mã nhưng ⛔ có giá trị đưa vào

# ⭐ Bản ATL *(một định nghĩa)* = ĐÚNG công thức ô sheet ATL `[COPY] Report I General Ledger ·
#   P&L Report` › tab `Report I PLA3 Y H Q M | PM + HR | ATL`, cột G, dòng sheet 81…87, `FORMULA`
#   *(SA chỉ-đọc 17/11; giống nhau ở 46/46 cột; dịch dòng→mã bằng `atl_cay.json`)* — `C12-R1-01`.
# ⭐ QUY ƯỚC DẤU = DẤU SHEET *(`C12-R1-02`)*: sheet lưu CHI PHÍ ÂM và CỘNG *(`PL2 = GI + OMC`,
#   OMC âm 27/27 cột ≠ 0)* ⇒ giá trị HD của chi phí phải mang dấu ÂM; ⛔ nhập dương thì PL sai
#   88–107 (đo trên 46 cột). ⚠ PL6 đi qua PL4 *(⛔ qua PL5 — COM bị bỏ khỏi chuỗi, đúng ô sheet)*;
#   PL8 cộng `TAC` *(Tax Cash, dòng 57)* ⛔ `CIT` *(dòng 58)*.
# ⚠ PL5: sheet ⛔ CÓ công thức ô *(tháng N:Y rỗng, G84 = sumifs trên vùng rỗng)* ⇒ giữ lời mô tả
#   dòng sheet "PL5 = PL4 − COM" dưới dấu sheet *(COM âm ⇒ `PL4 + COM`)*; ⛔ ghim như nguồn.
DINH_NGHIA: dict[str, str] = {
    "PL2": "GI + OMC",
    "PL3": "PL2 + API + SC + LC",
    "PL4": "PL3 + PS",
    "PL5": "PL4 + COM",
    "PL6": "PL4 + MC + OTMC + DC + CSO",
    "PL7": "PL6 + GAC + CDC + ITE",
    "PL8": "PL7 + TAC",
}

# (dòng PL, mã, lý do) — ATL GIỮ mã; MM mô tả chữ ⛔ nêu nó. ⛔ tự hoà giải.
CHENH_VOI_MM: tuple[tuple[str, str, str], ...] = (
    ("PL3", "LC", "ATL trừ `LC` (License Cost) ở PL3; MM mô tả PL3 = PL2 − Tech Service "
                  "Cost (none HR: server, API.. + Tools) — ⛔ nêu License"),
)

# Hai phép CHECK *(AP §3.2.3)*: (tên, mã vế trái, mã vế phải).
CHECK: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("NB = 0", ("NB",), ()),
    ("NIS+INT+PIT+COM = CXA+GAH+DC+MC", ("NIS", "INT", "PIT", "COM"),
     ("CXA", "GAH", "DC", "MC")),
)


class LoiPL(ValueError):
    """Dòng PL ⛔ tính được. `loi` = mọi `(tên, chi tiết)`; `ten` = TẬP tên lỗi."""

    def __init__(self, loi: Iterable[tuple[str, str]]) -> None:
        self.loi = tuple(loi)
        self.ten = frozenset(t for t, _ in self.loi)
        super().__init__(f"⛔ {BANG} — {len(self.loi)} lỗi: "
                         + " · ".join(f"{t}: {c}" for t, c in self.loi))


_TOKEN = re.compile(r"\s*(?:([A-Za-z][A-Za-z0-9.]*)|([+\-−()]))")


def _tach(bt: Any) -> list[tuple[str, str]]:
    if not isinstance(bt, str):
        raise LoiPL([(PL_CU_PHAP, f"biểu thức ⛔ phải chuỗi, gặp {type(bt).__name__}")])
    ra: list[tuple[str, str]] = []
    i = 0
    s = bt.rstrip()
    while i < len(s):
        m = _TOKEN.match(s, i)
        if not m:
            raise LoiPL([(PL_CU_PHAP, f"ký tự ⛔ hợp lệ ở vị trí {i} trong {bt[:40]!r}")])
        ra.append(("ma", m.group(1)) if m.group(1) else ("op", m.group(2)))
        i = m.end()
    if not ra:
        raise LoiPL([(PL_CU_PHAP, "biểu thức rỗng")])
    return ra


def phan_tich(bt: str) -> tuple:
    """Biểu thức ⇒ cây `('ma', X) | ('dau', ±1, n) | ('hai', ±1, trái, phải)`. Sai ⇒ `LoiPL`."""
    tok = _tach(bt)
    pos = 0

    def loi(ly: str):
        return LoiPL([(PL_CU_PHAP, f"{ly} trong {bt[:40]!r}")])

    def so_hang():
        nonlocal pos
        if pos >= len(tok):
            raise loi("thiếu số hạng")
        k, v = tok[pos]
        if k == "ma":
            pos += 1
            return ("ma", v)
        if v in "+-−":
            pos += 1
            return ("dau", -1 if v in "-−" else 1, so_hang())
        if v == "(":
            pos += 1
            n = tong()
            if pos >= len(tok) or tok[pos] != ("op", ")"):
                raise loi("thiếu ngoặc đóng")
            pos += 1
            return n
        raise loi(f"ký hiệu {v!r} ⛔ đúng chỗ")

    def tong():
        nonlocal pos
        n = so_hang()
        while pos < len(tok) and tok[pos][0] == "op" and tok[pos][1] in "+-−":
            d = -1 if tok[pos][1] in "-−" else 1
            pos += 1
            n = ("hai", d, n, so_hang())
        return n

    cay = tong()
    if pos != len(tok):
        raise loi("thừa ký hiệu sau biểu thức")
    return cay


def _ma_cua(n: tuple) -> set[str]:
    if n[0] == "ma":
        return {n[1]}
    return _ma_cua(n[2]) if n[0] == "dau" else _ma_cua(n[2]) | _ma_cua(n[3])


def ma_dung(dinh_nghia: Mapping[str, str]) -> set[str]:
    """Mọi mã HD mà `dinh_nghia` nhắc *(⛔ gồm các dòng PL khai ở chính nó)*."""
    ra: set[str] = set()
    for bt in dinh_nghia.values():
        ra |= _ma_cua(phan_tich(bt))
    return ra - set(dinh_nghia)


def _tinh(n: tuple, gt: Mapping[str, Any], dn: Mapping[str, str],
          memo: dict[str, Any], dang: tuple[str, ...],
          hop_le: frozenset[str] | None = None):
    if n[0] == "ma":
        ma = n[1]
        if ma in dn:
            if ma in dang:
                raise LoiPL([(PL_CHU_TRINH, "vòng " + " → ".join(dang[dang.index(ma):] + (ma,)))])
            if ma not in memo:
                memo[ma] = _tinh(phan_tich(dn[ma]), gt, dn, memo, dang + (ma,), hop_le)
            return memo[ma]
        if hop_le is not None and ma not in hop_le:
            raise LoiPL([(PL_MA_LA, f"mã {ma!r} ⛔ có trong cây HD")])
        if ma not in gt:
            raise LoiPL([(PL_THIEU_GIA_TRI, f"mã {ma!r} ⛔ có giá trị HD")])
        return gt[ma]
    if n[0] == "dau":
        return n[1] * _tinh(n[2], gt, dn, memo, dang, hop_le)
    return (_tinh(n[2], gt, dn, memo, dang, hop_le)
            + n[1] * _tinh(n[3], gt, dn, memo, dang, hop_le))


def _hop_le(cay: hd.CayHD | None) -> frozenset[str] | None:
    return None if cay is None else frozenset(n.ma for n in cay.nut)


def tinh_bieu_thuc(bt: str, gia_tri_hd: Mapping[str, Any],
                   cay: hd.CayHD | None = None) -> Any:
    """Một biểu thức trên giá trị HD. Mã ⛔ giá trị ⇒ `PL_THIEU_GIA_TRI`; có `cay` mà mã
    ⛔ trong cây ⇒ `PL_MA_LA` *(phân biệt "mã lạ" với "quên đưa giá trị")*."""
    return _tinh(phan_tich(bt), gia_tri_hd, {}, {}, (), _hop_le(cay))


def kiem_dinh_nghia(dinh_nghia: Mapping[str, str], cay: hd.CayHD | None = None) -> None:
    """Kiểm HÌNH `dinh_nghia`: cú pháp từng dòng; (có `cay`) mọi mã ∈ cây. Gom HẾT lỗi."""
    loi: list[tuple[str, str]] = []
    theo = {n.ma for n in cay.nut} if cay is not None else None
    for pl, bt in dinh_nghia.items():
        try:
            ma = _ma_cua(phan_tich(bt))
        except LoiPL as e:
            loi += [(t, f"{pl}: {c}") for t, c in e.loi]
            continue
        if theo is not None:
            if pl not in theo:
                loi.append((PL_MA_LA, f"{pl}: dòng PL ⛔ có trong cây HD"))
            loi += [(PL_MA_LA, f"{pl}: mã {m!r} ⛔ có trong cây HD")
                    for m in sorted(ma - set(dinh_nghia)) if m not in theo]
    if loi:
        raise LoiPL(loi)


def tinh_pl(gia_tri_hd: Mapping[str, Any],
            dinh_nghia: Mapping[str, str] | None = None,
            cay: hd.CayHD | None = None) -> dict[str, Any]:
    """`PL2…PL8` từ giá trị HD. Dòng PL tham chiếu nhau *(PL3 = PL2 − …)*, chu trình ⇒ `PL_CHU_TRINH`."""
    dn = DINH_NGHIA if dinh_nghia is None else dinh_nghia
    memo: dict[str, Any] = {}
    hl = _hop_le(cay)
    return {pl: _tinh(("ma", pl), gia_tri_hd, dn, memo, (), hl) for pl in dn}


@dataclass(frozen=True)
class PhepCheck:
    ten: str
    trai: Any
    phai: Any
    chenh: Any          # trái − phải
    dat: bool


@dataclass(frozen=True)
class KetQuaCheck:
    phep: tuple[PhepCheck, ...]

    @property
    def dat(self) -> bool:
        return all(p.dat for p in self.phep)

    @property
    def lech(self) -> tuple[str, ...]:
        """Tên các phép LỆCH *(rỗng ⇒ đạt)*."""
        return tuple(p.ten for p in self.phep if not p.dat)


def check_pl(gia_tri_hd: Mapping[str, Any]) -> KetQuaCheck:
    """Hai phép: `NB = 0` · `NIS+INT+PIT+COM = CXA+GAH+DC+MC`. Thiếu giá trị ⇒ `PL_THIEU_GIA_TRI`."""
    thieu = sorted({m for _, t, p in CHECK for m in t + p if m not in gia_tri_hd})
    if thieu:
        raise LoiPL([(PL_THIEU_GIA_TRI, f"mã {m!r} ⛔ có giá trị HD") for m in thieu])
    ra = []
    for ten, t, p in CHECK:
        a = sum(gia_tri_hd[m] for m in t)
        b = sum(gia_tri_hd[m] for m in p)
        ra.append(PhepCheck(ten=ten, trai=a, phai=b, chenh=a - b, dat=a == b))
    return KetQuaCheck(phep=tuple(ra))
