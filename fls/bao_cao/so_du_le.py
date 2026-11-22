"""`RP.CF` · khối **`CB I Cash Balance by LE I Legal Entity by Currency`** của Daily Report A-CCR *(PD 615)* — số dư tiền
theo **LE × đơn vị tiền × ngày** dựng từ số dư `2. CCR` + `2. CCR Cash` *(ISP 3.1.2 · Step 46 · H14 · vòng sửa tích hợp sau
R2 `KQ-314`; đầu vào = ảnh DT13 `ccr_so_du_ccr` · `ccr_so_du_cash`, `BG-320` §1–§3)*.

⭐ **Khuôn = công thức AS-IS đọc được** *(`FORMULA` chỉ-đọc 22/11, DT13)*: ô 615 hàng `h`, cột ngày `D` =
   `Σ dấu × SUMIFS('<tab>'!$K<r>:<r>, '<tab>'!$K$5:$5, D$5) / 10^mũ` — mỗi hạng tử là MỘT hàng `r` của tab số dư *(hàng =
   thực thể × ngân hàng × tiền tệ)*. `mUSD`/`mSGD`/`mHKD` ⇒ mũ 6 · `bVND` ⇒ mũ 9. SUMIFS trên ô rỗng = 0 ⇒ ô vắng trong ảnh
   = 0; NGÀY ⛔ có cột ở ảnh ⇒ ⛔ in ô *(⛔ đoán)*.
⛔ **Khuôn ⛔ suy được bằng luật nhãn** *(đo 22/11, Đ1)*: nhãn LE của 615 ≠ nhãn thực thể của `2. CCR` ở 3 chỗ *(`VVON` ↔
   `VOON` · `VVOL` ↔ `VOOL` · `VVOT (TERASOFTS)` ↔ `VVOO (VGO2)`)*; `UGO2 mUSD` gồm cả hàng `Non USD`; `BGO2 mUSD` bỏ hàng
   `EUR`; 7 LE cá nhân *(`LE20…LE26`)* = 7 hàng `CNC` của `2. CCR` theo THỨ TỰ, ⛔ nhãn ⇒ khuôn là BẢNG tường minh.
⛔ **Hàng 71** *(`LE04` `mUSD`)*: công thức ĐỔI theo cột *(`G` = hàng 110 + 115 · `H` = 110 + 111 + 115 …)* = chỉnh tay
   AS-IS ⇒ `NGOAI_KHUON_CB` CÓ TÊN, ⛔ dựng *(DT13 `BG-320` §3: 46/47 hàng)*.

Khoá LE = `LE<nn>` theo SỐ THỨ TỰ nhãn `"<nn> > <tên>"` của ảnh 615 *(⛔ mang tên: 7 nhãn `LE20…LE26` là tên NGƯỜI —
`CLAUDE.md` Riêng tư)*. Bài hai nguồn: `tests/bao_cao/test_so_du_le.py` *(khuôn ⇔ `CB_MAP` DT13 đo độc lập)*.

⛔ Engine ⛔ đọc tệp, ⛔ đọc kho, ⛔ đọc đáp án: số dư đến qua tham số `so_du = {tab: {hàng sheet: {ngày ISO: số|None}}}`.
"""
from __future__ import annotations

import calendar
import datetime
from decimal import Decimal
from typing import Any, Mapping

TAB = ("2. CCR", "2. CCR Cash")
_C, _K = "2. CCR", "2. CCR Cash"


class LoiSoDu(ValueError):
    """Đầu vào số dư thiếu ⇒ khối CB DỪNG `chua_co_dau_vao` *(⛔ ngầm 0)*."""


def _h(tab: str, *hang: int, mu: int = 6) -> tuple[tuple[str, int, int, int], ...]:
    return tuple((tab, r, 1, mu) for r in hang)


#: (LE, đơn vị) → ((tab, hàng sheet, dấu, mũ), …) — thứ tự hạng tử = thứ tự trong công thức AS-IS.
KHUON_CB_615: dict[tuple[str, str], tuple[tuple[str, int, int, int], ...]] = {
    ("LE01", "mUSD"): _h(_K, 10) + _h(_C, 10),          # Group — hàng `Original Currency` (tổng theo tiền tệ)
    ("LE01", "mSGD"): _h(_K, 11) + _h(_C, 11),
    ("LE01", "mHKD"): _h(_K, 12) + _h(_C, 12),
    ("LE01", "bVND"): _h(_K, 14, mu=9) + _h(_C, 14, mu=9),
    ("LE02", "mUSD"): _h(_C, 100, 101, 102),            # SGO2
    ("LE02", "mSGD"): _h(_C, 99),
    ("LE03", "mUSD"): _h(_C, 94, 95, 97),               # SGO1
    ("LE03", "mSGD"): _h(_C, 93, 96),
    ("LE04", "mHKD"): _h(_C, 111),                      # HGO1 (HGO6) — `mUSD` ở NGOAI_KHUON_CB
    ("LE05", "mUSD"): _h(_C, 104, 105),                 # BGO2 — ⛔ hàng EUR 106
    ("LE05", "mSGD"): _h(_C, 103),
    ("LE06", "mUSD"): _h(_K, 32),                       # BGO1
    ("LE06", "mHKD"): _h(_K, 33),
    ("LE07", "mUSD"): _h(_C, 48, 49),                   # VGOH
    ("LE07", "bVND"): _h(_C, 46, 47, 50, mu=9),
    ("LE08", "mUSD"): _h(_C, 54, 55),                   # VVOV
    ("LE08", "bVND"): _h(_C, 52, 53, mu=9),
    ("LE09", "mUSD"): _h(_C, 42, 43),                   # VVOT ↔ `VVOO (VGO2)` ở 2. CCR
    ("LE09", "bVND"): _h(_C, 40, 41, mu=9),
    ("LE10", "mUSD"): _h(_C, 60, 61),                   # VVOS
    ("LE10", "bVND"): _h(_C, 58, 59, mu=9),
    ("LE11", "mUSD"): _h(_C, 66, 67),                   # VVOH
    ("LE11", "bVND"): _h(_C, 64, 65, mu=9),
    ("LE12", "mUSD"): _h(_C, 107, 108, 109),            # UGO2 — gồm hàng `Non USD` 108
    ("LE13", "mUSD"): _h(_C, 112),                      # CGO1
    ("LE14", "mUSD"): _h(_C, 113, 114),                 # MGO1
    ("LE15", "bVND"): _h(_C, 75, mu=9),                 # VOOA
    ("LE15", "mUSD"): _h(_C, 76),
    ("LE16", "mUSD"): _h(_C, 116),                      # HGO2
    ("LE17", "bVND"): _h(_C, 78, mu=9),                 # VGC1
    ("LE17", "mUSD"): _h(_C, 79, mu=9),                 # ⚠ ÷10^9 dù nhãn mUSD — xem MU_LECH_DON_VI
    ("LE18", "bVND"): _h(_C, 84, mu=9),                 # VVON ↔ `VOON`
    ("LE18", "mUSD"): _h(_C, 85),
    ("LE19", "bVND"): _h(_C, 81, mu=9),                 # VVOL ↔ `VOOL`
    ("LE19", "mUSD"): _h(_C, 82, mu=9),                 # ⚠ ÷10^9 dù nhãn mUSD — xem MU_LECH_DON_VI
    ("LE20", "mUSD"): _h(_C, 117),                      # LE20…LE26: 7 hàng `CNC` theo thứ tự (⛔ mang nhãn người)
    ("LE21", "mUSD"): _h(_C, 118),
    ("LE22", "mUSD"): _h(_C, 119),
    ("LE23", "mUSD"): _h(_C, 120),
    ("LE24", "mUSD"): _h(_C, 121),
    ("LE25", "mUSD"): _h(_C, 122),
    ("LE26", "mUSD"): _h(_C, 123),
    ("LE27", "bVND"): _h(_C, 87, mu=9),                 # Coretap
    ("LE27", "mUSD"): _h(_C, 88),
    ("LE28", "bVND"): _h(_C, 90, mu=9),                 # NEXTWIST
    ("LE28", "mUSD"): _h(_C, 91),
}
#: ⚠ (LE, đơn vị) mà công thức AS-IS chia mũ ≠ nhãn đơn vị *(nhãn `mUSD` ⇒ mong ÷10^6, công thức ÷10^9)*. Bài hai nguồn
#: bắt được *(khuôn suy theo nhãn ≠ `CB_MAP` DT13 đọc `FORMULA`)*. Khuôn GIỮ công thức AS-IS *(engine tái lập sổ)*; số dư
#: hàng nguồn `2. CCR` 79 · 82 = 0 cả 31 ngày ⇒ phép so ⛔ phân biệt được hai mũ *(Đ3)* — câu "AS-IS sai mũ?" chờ chủ.
MU_LECH_DON_VI = frozenset({("LE17", "mUSD"), ("LE19", "mUSD")})
#: (LE, đơn vị) có ở khối CB mà ⛔ dựng — (tên rổ, lý do). Ô của nó NGOÀI mẫu số CÓ TÊN.
NGOAI_KHUON_CB: dict[tuple[str, str], tuple[str, str]] = {
    ("LE04", "mUSD"): ("cb_cong_thuc_doi_theo_cot",
                       "hàng 71: công thức ĐỔI theo cột (G = 2. CCR 110 + 115 · H = 110 + 111 + 115 …) — chỉnh tay AS-IS, "
                       "⛔ khuôn"),
}


def ngay_cua_thang(nam: int, thang: int) -> list[datetime.date]:
    return [datetime.date(nam, thang, d) for d in range(1, calendar.monthrange(nam, thang)[1] + 1)]


def bang_so_du_le(nam: int, thang: int, so_du: Mapping[str, Mapping[int, Mapping[str, Any]]] | None
                  ) -> dict[tuple[str, str, str], Decimal]:
    """→ {(LE, đơn vị, ngày ISO): số} cho mọi (LE, đơn vị) của khuôn × mọi ngày của tháng CÓ cột ở CẢ HAI ảnh.

    Ảnh vắng ⇒ `LoiSoDu` *(`chua_co_dau_vao`)*. Hàng khuôn ⛔ có ở ảnh *(ảnh bỏ hàng rỗng hẳn)* ⇒ hạng tử 0 *(SUMIFS)*."""
    if not so_du or any(not so_du.get(t) for t in TAB):
        thieu = [t for t in TAB if not (so_du or {}).get(t)]
        raise LoiSoDu(f"chua_co_dau_vao: thiếu ảnh số dư {thieu} (ccr_so_du_ccr · ccr_so_du_cash — DT13)")
    co_ngay = {t: set().union(*(set(h) for h in so_du[t].values())) for t in TAB}
    ra: dict[tuple[str, str, str], Decimal] = {}
    for d in ngay_cua_thang(nam, thang):
        c = d.isoformat()
        if not all(c in co_ngay[t] for t in TAB):
            continue
        for (le, dv), hang in KHUON_CB_615.items():
            s = Decimal(0)
            for tab, r, dau, mu in hang:
                v = (so_du[tab].get(r) or {}).get(c)
                if v is not None:
                    s += dau * Decimal(str(v)) / (Decimal(10) ** mu)
            ra[(le, dv, c)] = s
    return ra
