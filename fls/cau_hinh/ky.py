# -*- coding: utf-8 -*-
"""`IX.PER` — **lịch kỳ**: `ky_cua(ngày)` + ngày đầu cột + luật ghi nhận kỳ
*(AP v3.1.2 §3.2.1 IX.PER · §3.2.4 · D4 — ISP 3.1.2 · Step 17 · `C6` · `WO-152`)*.

⛔⛔ **Năm của CHÍNH dữ liệu.** Bản AS-IS *ép năm 2025* khi suy ra kỳ *(AP §3.2.4, dòng
   "ngày đầu cột… năm ép 2025")* ⇒ ngày `2026-11-05` bị xếp vào kỳ của 2025, **không báo**.
   `ky_cua` ⛔ có hằng năm nào: `2026-11-05` ⇒ `Y2026·H2·Q4·M11`, `2024-12-31` ⇒ `Y2024`.

⭐ **Ngày đầu cột + luật ghi nhận là CONFIG trong KHO** *(`fls_cau_hinh_*`, di trú `0027` —
   ⛔ di trú mới)*, ⛔ gõ cứng ở mã. Tệp này chỉ **kiểm hình** một bản đã đọc
   *(`kiem`)*; đọc/ghi kho là `fls/repo/cau_hinh_repo.py` *(hợp đồng `.importlinter` 10)*.
   Hình bản: `ngay_dau` ⇒ `{"ngay": "yyyy-mm-dd"}` · `luat` ⇒ `{"ma": "A"}`.

⛔ **Luật ghi nhận kỳ *(D4)*** — chỉ **A** chạy:
     · `A` — *dồn về ngày 1 của tháng `PL start`*;
     · `B` — *chia đều `PL start → PL end`*: **CHƯA** mở *(chờ owner ký)* ⇒ `LUAT_CHUA_KY`,
       ⛔ lặng lẽ rơi về A *(sẽ ra số khác mà ⛔ ai thấy)*.
   Mã luật lạ ⇒ `PER_HONG`, ⛔ đoán.

⚠ Hai lỗi, hai tên: `LUAT_CHUA_KY` *(luật có thật nhưng chưa mở)* ≠ `PER_HONG` *(bản/ô sai
   hình)* — dẫn người dùng đi hai đường sửa khác nhau.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping

BANG = "IX.PER"

LUAT_A = "A"
LUAT_B = "B"
# `TEN_LUAT` ⇒ tên đọc được của luật ĐÃ MỞ; `LUAT_CHUA_MO` ⇒ luật có thật mà chưa mở.
TEN_LUAT: dict[str, str] = {LUAT_A: "don ngay 1 thang PL start"}
LUAT_CHUA_MO: tuple[str, ...] = (LUAT_B,)       # B = chia đều PL start→end (D4)

LUAT_CHUA_KY = "LUAT_CHUA_KY"
PER_HONG = "PER_HONG"

KHOA_NGAY_DAU = "ngay_dau"
KHOA_LUAT = "luat"


class LoiKy(ValueError):
    """Lỗi `IX.PER` **có tên**: `ma` ∈ {`LUAT_CHUA_KY`, `PER_HONG`}."""

    def __init__(self, ma: str, thong_bao: str) -> None:
        super().__init__(f"{ma}: {thong_bao}")
        self.ma = ma


@dataclass(frozen=True)
class Ky:
    """Kỳ của một ngày — mỗi trường nói MÌNH ĐẾM GÌ: `nua` ∈ {1,2} · `quy` ∈ 1..4 ·
    `thang` ∈ 1..12 *(⛔ cộng dồn từ ngày đầu)*."""

    nam: int
    nua: int
    quy: int
    thang: int

    @property
    def nhan_nam(self) -> str:
        return f"Y{self.nam}"

    @property
    def nhan_nua(self) -> str:
        return f"H{self.nua}"

    @property
    def nhan_quy(self) -> str:
        return f"Q{self.quy}"

    @property
    def nhan_thang(self) -> str:
        return f"M{self.thang}"


def ky_cua(ngay: date) -> Ky:
    """Y/H/Q/M của `ngay` — năm là năm **của chính `ngay`** *(⛔ ép 2025)*."""
    if not isinstance(ngay, date):
        raise TypeError(f"ky_cua cần `date`, nhận {type(ngay).__name__}")
    return Ky(nam=ngay.year, nua=(ngay.month - 1) // 6 + 1,
              quy=(ngay.month - 1) // 3 + 1, thang=ngay.month)


def chon_luat(ma: Any) -> str:
    """Trả mã luật nếu **chạy được**; ⛔ lặng lẽ đổi sang luật khác."""
    if ma in LUAT_CHUA_MO:
        raise LoiKy(LUAT_CHUA_KY,
                    f"luat {ma!r} (chia deu PL start→end, D4 B) CHUA mo — cho owner ky; "
                    f"chi luat {sorted(TEN_LUAT)} chay")
    if ma not in TEN_LUAT:
        raise LoiKy(PER_HONG, f"ma luat la {ma!r} — biet {sorted(TEN_LUAT) + list(LUAT_CHUA_MO)}")
    return ma


def ngay_ghi_nhan(luat: Any, pl_start: date, pl_end: date) -> date:
    """Ngày ghi nhận kỳ của một dòng PL. Luật `A`: **ngày 1 của tháng `PL start`**
    *(`pl_end` ⛔ ảnh hưởng)*. Luật `B` ⇒ `LUAT_CHUA_KY`."""
    chon_luat(luat)
    return pl_start.replace(day=1)


@dataclass(frozen=True)
class LichKy:
    """Config `IX.PER` đã kiểm: `ngay_dau` *(ngày đầu cột — config, có nguồn)* + `luat`."""

    nguon: str
    ngay_dau: date
    luat: str


def _ngay(o: Any) -> date:
    if not isinstance(o, Mapping) or set(o) != {"ngay"}:
        raise LoiKy(PER_HONG, f"`ngay_dau` phai dung {{ngay}}, do {o!r}")
    v = o["ngay"]
    if not isinstance(v, str) or len(v) != 10:
        raise LoiKy(PER_HONG, f"`ngay_dau.ngay` phai 'yyyy-mm-dd', do {v!r}")
    try:
        return date.fromisoformat(v)
    except ValueError as e:
        raise LoiKy(PER_HONG, f"`ngay_dau.ngay` ⛔ phai ngay co that: {v!r}") from e


def kiem(dong: Mapping[str, Any], *, nguon: str) -> LichKy:
    """Kiểm một bản `IX.PER` ⇒ `LichKy`. Thiếu khoá/sai hình ⇒ `PER_HONG`; luật `B` ⇒
    `LUAT_CHUA_KY`. Một lõi cho CẢ `nap` *(kiểm trước khi ghi)* lẫn đọc."""
    if not isinstance(dong, Mapping):
        raise LoiKy(PER_HONG, f"ban phai la anh xa khoa→gia tri, do {type(dong).__name__}")
    thieu = [k for k in (KHOA_NGAY_DAU, KHOA_LUAT) if k not in dong]
    if thieu:
        raise LoiKy(PER_HONG, f"ban thieu khoa {thieu}")
    ngay = _ngay(dong[KHOA_NGAY_DAU])
    o = dong[KHOA_LUAT]
    if not isinstance(o, Mapping) or set(o) != {"ma"}:
        raise LoiKy(PER_HONG, f"`luat` phai dung {{ma}}, do {o!r}")
    return LichKy(nguon=nguon, ngay_dau=ngay, luat=chon_luat(o["ma"]))
