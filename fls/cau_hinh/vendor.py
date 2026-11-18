"""`IX.VEN` — **vendor · network · tài khoản** *(Block 1)* + cột **`cach_tinh`** *(AP v3.1.2
§3.2.2 IX.VEN · §3.2.4 dòng "VD341 · VD444 · VD428 · 'Max' · VD62")*.

ISP 3.1.2 · Step 21 · `C9` *(`WO-172`)* — làn **BE-CF**, khuôn `fx.py`/`hd.py`: lõi kiểm THUẦN,
bản config được TRUYỀN VÀO *(⛔ biết kho — `.importlinter` hợp đồng 10)*.

⭐ **Số đo của ảnh DT8** *(`tests/fixture/cau_hinh/ix_ven.json`, Đ4 — mỗi số một nhãn)*:
  · **42** DÒNG sheet 4…45 *(ISP ghi `36` = hàng 4–39 ⇒ errata `DT8-R1-01`; `36` cũng là số
    BỘ `(vendor, network, account)` khác nhau — hai con số, hai vật)*;
  · **5** mã `cach_tinh` riêng `{Max, VD341, VD428, VD444, VD62}` + nhãn `thường`
    *(số dòng: Max 12 · VD341 12 · VD444 8 · VD428 3 · VD62 1 · thường 6 = 42)*;
  · `pct` **null ở 14/42 dòng** *(sheet 32…45 — dòng chỉ có vendor, ⛔ mang %)*; có thì > 0;
  · **7** CDT1 *(danh mục đóng — `MappingBlock2.gs` nhân Block 1 × 7)*.

⛔ **`cach_tinh` chỉ là NHÃN** — phép tính riêng của 5 vendor là việc `H10`. Ở AS-IS 5 mã ấy
   gõ cứng trong công thức CFA1/MID; ở đây engine đọc nhãn từ config. Tập 5 nhãn **ĐÓNG** *(Đ5:
   khai `mong`, NO cả hai chiều)*: thiếu một nhãn *(vendor đổi mã ⇒ lọt về `thường` im lặng)*
   hay thừa một nhãn lạ *(mã lạ hoá đặc biệt)* ⇒ `LoiVen`, ⛔ im lặng. Tập rỗng ⇒ nổ *(Đ3)*.

⛔ **Khoá**: `dong_sheet` là khoá kho *(duy nhất theo hàng)*; khoá NGHIỆP VỤ là `(vendor, No)`
   — vendor **lặp** hợp lệ *(VD341 × 12 dòng)*, nhưng cùng `(vendor, No)` hai lần là hai câu
   trả lời cho một câu hỏi ⇒ lỗi CÓ TÊN *(C9-B2)*. Mọi lý do gói trong MỘT dòng *(`S0-R1-04`)*.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Iterable, Mapping

BANG = "IX.VEN"
NHAN_RIENG: tuple[str, ...] = ("Max", "VD341", "VD428", "VD444", "VD62")   # sắp theo chữ
NHAN_THUONG = "thường"
SO_CDT1 = 7                         # danh mục CDT1 *(đếm CDT1 khác nhau, ⛔ đếm dòng)*

_COT = ("thu_tu", "dong_sheet", "No", "vendor", "network", "account", "pct",
        "cashin_month", "cashin_day", "cach_tinh")
_SO_NGUYEN = re.compile(r"[0-9]{1,2}", re.ASCII)
_THAP_PHAN = re.compile(r"[0-9]+(?:\.[0-9]+)?", re.ASCII)


class LoiVen(ValueError):
    """Bảng `IX.VEN` ⛔ đọc được. `ly_do` = **mọi** lý do, ⛔ chỉ lý do đầu."""

    def __init__(self, ly_do: Iterable[str]) -> None:
        self.ly_do = tuple(ly_do)
        super().__init__(f"⛔ {BANG} ⛔ đọc được — {len(self.ly_do)} lỗi: "
                         + " · ".join(self.ly_do))


@dataclass(frozen=True)
class DongVen:
    thu_tu: int
    dong_sheet: str
    no: str
    vendor: str
    network: str | None
    account: str | None
    pct: Decimal | None
    cashin_month: int
    cashin_day: int
    cach_tinh: str


@dataclass(frozen=True)
class BangVen:
    nguon: str
    dong: tuple[DongVen, ...]
    cdt1: tuple[str, ...]
    nhan_rieng: tuple[str, ...]


def _mot(s: Any) -> str:
    return " ".join(repr(s).split())


def _chu(v: Any, ten: str, i: int, ly: list[str], *, bat_buoc: bool) -> str | None:
    if v is None and not bat_buoc:
        return None
    if not isinstance(v, str) or not v.strip():
        ly.append(f"dòng {i}: {ten}={_mot(v)} ⛔ phải chuỗi ⛔ rỗng"
                  + ("" if bat_buoc else " (hay null)"))
        return None
    return v


def _so_nguyen(v: Any, ten: str, i: int, lo: int, hi: int, ly: list[str]) -> int | None:
    if isinstance(v, bool) or not isinstance(v, (str, int)) or \
            not _SO_NGUYEN.fullmatch(str(v).strip()) or not lo <= int(str(v).strip()) <= hi:
        ly.append(f"dòng {i}: {ten}={_mot(v)} ⛔ số nguyên ASCII {lo}…{hi}")
        return None
    return int(str(v).strip())


def kiem(dong: Iterable[Mapping[str, Any]], *, cdt1: Iterable[str],
         nguon: str) -> BangVen:
    """Kiểm **thuần** Block 1. Hỏng ⇒ `LoiVen` *(mọi lý do)*; ngược lại `BangVen`."""
    ly: list[str] = []
    cdt = list(cdt1)
    if len(cdt) != SO_CDT1 or len(set(cdt)) != SO_CDT1 or \
            any(not isinstance(c, str) or not c.strip() for c in cdt):
        ly.append(f"CDT1: đo {len(set(map(str, cdt)))} khác nhau trên {len(cdt)} mục, "
                  f"mong đúng {SO_CDT1} khác nhau ⛔ rỗng")

    ds: list[DongVen] = []
    for i, r in enumerate(dong, start=1):
        if not isinstance(r, Mapping):
            ly.append(f"dòng {i}: ⛔ phải một đối tượng")
            continue
        la = sorted(k for k in r if k not in _COT)
        if la:
            ly.append(f"dòng {i}: cột lạ {la}")
        n0 = len(ly)
        thu_tu = r.get("thu_tu", i)
        if isinstance(thu_tu, bool) or not isinstance(thu_tu, int):
            ly.append(f"dòng {i}: thu_tu={_mot(thu_tu)} ⛔ phải số nguyên")
        ds_ = _chu(r.get("dong_sheet"), "dong_sheet", i, ly, bat_buoc=True)
        no = _chu(r.get("No"), "No", i, ly, bat_buoc=True)
        ven = _chu(r.get("vendor"), "vendor", i, ly, bat_buoc=True)
        net = _chu(r.get("network"), "network", i, ly, bat_buoc=False)
        acc = _chu(r.get("account"), "account", i, ly, bat_buoc=False)
        ct = _chu(r.get("cach_tinh"), "cach_tinh", i, ly, bat_buoc=True)
        pct_v = r.get("pct")
        pct = None
        if pct_v is None:
            pass                        # ⭐ đo ảnh DT8: 14/42 dòng *(sheet 32…45)* ⛔ có %
        elif isinstance(pct_v, bool) or not isinstance(pct_v, (str, int, Decimal)) \
                or not _THAP_PHAN.fullmatch(str(pct_v).strip()) \
                or Decimal(str(pct_v).strip()) <= 0:
            ly.append(f"dòng {i}: pct={_mot(pct_v)} ⛔ null hay thập phân ASCII > 0 "
                      f"(⛔ float · ⛔ số mũ)")
        else:
            pct = Decimal(str(pct_v).strip())
        thang = _so_nguyen(r.get("cashin_month"), "cashin_month", i, 1, 12, ly)
        ngay = _so_nguyen(r.get("cashin_day"), "cashin_day", i, 1, 31, ly)
        if ct is not None and ct != NHAN_THUONG and ct not in NHAN_RIENG:
            ly.append(f"dòng {i}: cach_tinh={_mot(ct)} ⛔ thuộc {list(NHAN_RIENG)} "
                      f"hay {NHAN_THUONG!r}")
        if len(ly) == n0 and None not in (ds_, no, ven, ct, thang, ngay):
            ds.append(DongVen(thu_tu, ds_, no, ven, net, acc, pct, thang, ngay, ct))

    if not ds and not ly:
        ly.append("0 dòng ⇒ ⛔ có bảng để kiểm")
    for k, n in sorted(Counter(d.dong_sheet for d in ds).items()):
        if n >= 2:
            ly.append(f"dong_sheet={k} trùng {n} dòng")
    for (v, no), n in sorted(Counter((d.vendor, d.no) for d in ds).items()):
        if n >= 2:
            ly.append(f"vendor={v} No={no} trùng khoá {n} dòng")
    if ds and not ly:
        co = {d.cach_tinh for d in ds} - {NHAN_THUONG}
        for m in NHAN_RIENG:
            if m not in co:
                ly.append(f"thiếu nhãn riêng {m!r} (mong đủ {list(NHAN_RIENG)})")
    if ly:
        raise LoiVen(ly)
    return BangVen(nguon=nguon, dong=tuple(ds), cdt1=tuple(cdt),
                   nhan_rieng=NHAN_RIENG)
