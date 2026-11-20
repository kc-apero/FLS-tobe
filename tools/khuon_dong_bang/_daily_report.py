"""Thân chung của hai khuôn `daily_report_2` · `daily_report_3` *(ISP 3.1.2 · Step 41 · DT11 · `WO-269`)*.

⭐ **Hai phép CHECK của IX.PL** *(AP §3.3.2 PD 605–617 · "7 dòng HDCI")* chạy trên CHÍNH đáp án:
  ① `NB = 0` *(dòng `NB` — Lưu chuyển nội bộ)*;
  ② `NIS + INT + PIT + COM = CXA + GAH + DC + MC` *(HR trả = chi phí HR đã vào PL)*.
Mỗi phép đo **theo kỳ** *(Đ4: một kỳ = một cột kỳ của MỘT khối — thực thể ở DR3, khối ngày/luỹ kế ở DR2)*.
Một kỳ rơi vào ĐÚNG một trong: *đo được & đạt* · *đo được & ⛔ đạt* · *⛔ đo được* — ô RỖNG hoặc ô
chữ/lỗi ở ≥ 1 trong 9 dòng ⇒ `⛔ đo được` **có tên kỳ** *(Đ3/Đ5: ⛔ coi là đạt)*.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Sequence

VE_TRAI = ("NIS", "INT", "PIT", "COM")
VE_PHAI = ("CXA", "GAH", "DC", "MC")
MA_CAN = ("NB", *VE_TRAI, *VE_PHAI)


def _so(c: Any) -> Decimal | None:
    """Ô ảnh → Decimal; rỗng ⇒ None; chữ/lỗi/bool ⇒ `False` *(⛔ đo được, khác rỗng)*."""
    if c is None:
        return None
    if isinstance(c, (dict, bool)):
        return False                                   # type: ignore[return-value]
    return Decimal(c)


def kiem_check(hang: Mapping[str, Mapping[str, Any]], cot_ky: Sequence[tuple[str, str]],
               tol: Decimal) -> dict[str, Any]:
    """`hang` = {mã: dòng ảnh} của MỘT khối; `cot_ky` = [(nhãn kỳ, tên cột)]. → số đo + kỳ có tên.

    Thiếu một trong 9 mã ⇒ `ValueError` *(⛔ đo được ≠ xanh — Đ5)*."""
    thieu = [m for m in MA_CAN if m not in hang]
    if thieu:
        raise ValueError(f"khối thiếu dòng {thieu} — ⛔ đo được CHECK")
    ra: dict[str, Any] = {"nb_do": 0, "nb_trong": 0, "nb_khac_0": [], "cb_do": 0, "cb_dat": 0,
                          "cb_khong_dat": [], "cb_khong_do": 0, "chenh": {}}
    for nhan, c in cot_ky:
        nb = _so(hang["NB"][c])
        if nb is None or nb is False:
            ra["nb_trong"] += 1
        else:
            ra["nb_do"] += 1
            if abs(nb) > tol:
                ra["nb_khac_0"].append(nhan)
        v = [_so(hang[m][c]) for m in (*VE_TRAI, *VE_PHAI)]
        if any(x is None or x is False for x in v):
            ra["cb_khong_do"] += 1
            continue
        ra["cb_do"] += 1
        ch = sum(v[:4]) - sum(v[4:])
        if abs(ch) > tol:
            ra["cb_khong_dat"].append(nhan)
            ra["chenh"][nhan] = ch
        else:
            ra["cb_dat"] += 1
    return ra


def so_voi_mong(ten: str, do: Mapping[str, Any], mong: Mapping[str, Any]) -> list[str]:
    """Đo ↔ mong *(Đ5, hai chiều)* — khác ⇒ một câu nói tên khối + khoá. `chenh` ⛔ so."""
    out = []
    for k, m in mong.items():
        d = tuple(do[k]) if isinstance(do[k], list) else do[k]
        if d != m:
            out.append(f"{ten}: {k} đo {d} ≠ mong {m}")
    return out
