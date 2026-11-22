"""Thân chung của hai khuôn `ccr_so_du_ccr` · `ccr_so_du_cash` *(ISP 3.1.2 · DT13 · `WO-319` · ĐẦU VÀO của PD 615)*
— ⛔ KHÔNG phải khuôn *(tên bắt đầu `_` ⇒ `danh_sach_khuon` bỏ qua; mỗi khuôn là một tệp riêng nạp `tao(...)`)*.

⭐ **Vì sao.** Khối `CB I Cash Balance by LE I Legal Entity by Currency` của `5. Daily Report` *(A-CCR, PD 615)* là
**47 hàng công thức** `=SUMIFS('2. CCR Cash'!$K<h>:<h>,'2. CCR Cash'!$K$5:$5,F$5)/10^6 + SUMIFS('2. CCR'!$K<h>:<h>,…)/10^6`
*(đo 22/11 bằng `FORMULA`, CHỈ ĐỌC)* — mỗi ô = số dư tiền của MỘT hàng ở `2. CCR` / `2. CCR Cash` *(hàng = thực thể × ngân hàng
× tiền tệ)* tại MỘT ngày *(tra theo hàng 5 = serial ngày)*. Ảnh này đóng băng đúng các hàng đó × 31 ngày **31/10→30/11/2026**
*(`F5` = 46326 … `AJ5` = 46356 của 615)*; ⛔ ngày khác.

⛔⛔ **PII** *(`CLAUDE.md` Riêng tư — bản đồ cột bằng tiêu đề TRƯỚC)*: chỉ đọc 4 cột nhãn + các cột ngày:
  · `A` Entity · `B` Bank · `C` Currency · `F` Account type — nhãn TỔ CHỨC *(đo: 0 nhãn có ≥ 8 chữ số ở A·B·C·F)*;
  · ⛔ `E` *(Accounts — số tài khoản, 181 ô ≥ 8 chữ số ở `2. CCR`)* · `G` Link · `H` ID · `I` Pass *(⛔⛔ `2. CCR Cash` có
    cột `ID`/`Pass` — KHÔNG BAO GIỜ đọc)* · `D` · `J`.
  · nhãn `B` dạng `R | <tên>` mà `<tên>` ⛔ thuộc tập nhãn tổ chức đã đo ⇒ che `TK_CA_NHAN_<n>` *(cùng mã ⇒ cùng số thứ tự)*.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from decimal import Decimal
from typing import Any, Callable

NGAY_DAU, NGAY_CUOI = 46326, 46356            # serial 31/10/2026 … 30/11/2026 (31 cột — F…AK của 615)
COT_NHAN = ("thuc_the", "ngan_hang", "tien_te", "loai_tk")
_J_NHAN = (0, 1, 2, 5)                          # A · B · C · F — ⛔ D E G H I J
J_NGAY_DAU = 10                                 # cột K — hàng 5 là serial ngày
HANG_NGAY = 4                                   # hàng sheet 5 (0-based)
DONG_DAU = 6                                    # hàng ≥ 6: FX (6–9) + số dư

#: nhãn `B` dạng `R | …` là TỔ CHỨC *(đo 22/11 ở `2. CCR Cash`: 7 nhãn)*; nhãn `R | …` khác ⇒ tên người ⇒ che.
NHAN_R_TO_CHUC = frozenset({"R | CNC", "R | PO", "R | PO BGO1 _HKD", "R | PO BGO1 _USD", "R | Pingpong",
                            "R | VND_CNC", "R | VND_HotBonus"})
_R_RE = re.compile(r"R \|\s+\S.*")


def cot_ngay(serial: int) -> str:
    d = date(1899, 12, 30) + timedelta(days=serial)
    return "d" + d.strftime("%Y%m%d")


COT_NGAY = tuple(cot_ngay(s) for s in range(NGAY_DAU, NGAY_CUOI + 1))
COT = (*COT_NHAN, *COT_NGAY)
KIEU_COT = {**{c: "chu?" for c in COT_NHAN}, **{c: "so?" for c in COT_NGAY}}


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _la_so(v: Any) -> bool:
    return isinstance(v, (int, float, Decimal)) and not isinstance(v, bool)


def che_nhan(v: Any, ma: dict[str, int]) -> Any:
    """Nhãn `R | <tên>` ngoài tập tổ chức ⇒ `TK_CA_NHAN_<n>`; nhãn khác giữ nguyên."""
    if not isinstance(v, str):
        return v
    s = " ".join(v.split())
    if _R_RE.fullmatch(s) and s not in NHAN_R_TO_CHUC:
        return f"TK_CA_NHAN_{ma.setdefault(s, len(ma) + 1)}"
    return v


def _cs(n: int) -> str:
    s, n = "", n + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def chuan_bi(tho: dict[str, Any], tab: str, n_hang: int, n_cot: int) -> dict[str, Any]:
    """Bản thô `{nguon, doc_luc, cach_doc, values}` *(lưới `A1:ABM240` của MỘT tab)* → bảng ảnh."""
    V = tho.get("values")
    if not isinstance(V, list) or len(V) != n_hang or any(not isinstance(h, list) for h in V):
        raise ValueError(f"`values` phải {n_hang} hàng *(tab {tab}, A1:ABM240 — API cắt hàng cuối rỗng)*")
    V = [list(h) + [""] * (n_cot - len(h)) for h in V]
    if any(len(h) != n_cot for h in V):
        raise ValueError(f"`values` rộng quá {n_cot} cột")
    hn = V[HANG_NGAY]
    j_ngay = {int(x): j for j, x in enumerate(hn) if j >= J_NGAY_DAU and _la_so(x) and NGAY_DAU <= x <= NGAY_CUOI}
    if sorted(j_ngay) != list(range(NGAY_DAU, NGAY_CUOI + 1)):
        raise ValueError("hàng 5 phải có ĐỦ 31 serial ngày 46326…46356 *(mỗi ngày đúng MỘT cột)*")
    js = sorted(j_ngay.values())
    if js != list(range(js[0], js[0] + 31)):
        raise ValueError("31 cột ngày phải LIỀN nhau")
    ma: dict[str, int] = {}
    dong: list[list[Any]] = []
    chi_nhan: list[dict[str, Any]] = []
    n_trong = 0
    for i in range(DONG_DAU - 1, len(V)):
        h = V[i]
        ds = i + 1
        cells = [None if _rong(h[j_ngay[s]]) else h[j_ngay[s]] for s in range(NGAY_DAU, NGAY_CUOI + 1)]
        if any(x is not None and not _la_so(x) for x in cells):
            # hàng CHỮ ở cột ngày *(vd hàng `Auto`/`Nhập` — cờ cách nhập)*: ⛔ vào ảnh số; có tên ở phụ, ⛔ in giá trị.
            chi_nhan.append({"dong_sheet": ds, "nhan": "hang_chu_o_cot_ngay"})
            continue
        lab = [None if _rong(h[j]) else che_nhan(" ".join(str(h[j]).split()), ma) for j in _J_NHAN]
        if all(x is None for x in cells):
            if any(lab):
                chi_nhan.append({"dong_sheet": ds, "nhan": " > ".join(str(x) for x in lab if x)})
            else:
                n_trong += 1
            continue
        dong.append([ds, *lab, *cells])
    if not dong:
        raise ValueError("0 hàng có số — mẫu số 0 (Đ3)")
    ngay_cot = [{"cot": cot_ngay(s), "serial": s, "cot_sheet": _cs(j_ngay[s])}
                for s in range(NGAY_DAU, NGAY_CUOI + 1)]
    return {
        "cot": ["dong_sheet", *COT],
        "dong": dong,
        "phu": {"ngay_cot": ngay_cot, "dong_chi_nhan": chi_nhan},
        "ghi_chu": (
            f"Số dư tiền theo (thực thể × ngân hàng × tiền tệ) × 31 ngày 31/10→30/11/2026 — tab `{tab}` của A-CCR_V2_Working "
            f"(đầu vào khối CB của PD 615). {len(dong)} hàng sheet có số (hàng sheet ≥ {DONG_DAU}: tỷ giá 6–9 + số dư); "
            f"{len(chi_nhan)} hàng chỉ có nhãn ở `dong_chi_nhan`; {n_trong} hàng rỗng hẳn ⛔ mang. Cột = `d<yyyymmdd>` "
            "(serial hàng 5 ở phụ `ngay_cot`). ⛔ cột E (số TK) · G · H · I · J; nhãn `R | <tên người>` che `TK_CA_NHAN_n` "
            f"({len(ma)} nhãn che)."),
    }


def do(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Số đo của ảnh *(mỗi số nói nó đếm gì — Đ4)*."""
    def u(v: Any) -> Any:
        return v["chu"] if isinstance(v, dict) else v
    theo_ngay = [sum(1 for d in dong if d[c] is not None) for c in COT_NGAY]
    che = sorted({u(d["ngan_hang"]) for d in dong if isinstance(u(d["ngan_hang"]), str)
                  and u(d["ngan_hang"]).startswith("TK_CA_NHAN_")})
    return {"hang": len(dong), "o_so": sum(theo_ngay), "theo_ngay": tuple(theo_ngay),
            "ngay_0_o": tuple(c for c, n in zip(COT_NGAY, theo_ngay) if n == 0), "nhan_che": tuple(che)}


def thieu_lac(dong: list[dict[str, Any]], mong: dict[str, Any], ten: str) -> dict[str, Any]:
    """Cổng *(Đ5 hai chiều)*: đo ↔ `mong`. Tập rỗng ⇒ `ValueError` *(Đ3)*; `mong` ⛔ khai ⇒ ĐỎ."""
    if not dong:
        raise ValueError("0 hàng — mẫu số 0, ⛔ nền xanh (Đ3)")
    if not mong:
        raise ValueError(f"MONG ⛔ khai — cổng `{ten}` ⛔ đo được")
    d = do(dong)
    thieu = [f"{k}: đo {d[k]} ≠ mong {m}" for k, m in mong.items() if d[k] != m]
    return {"thieu": thieu, "lac": [],
            "dai": (f"{d['hang']} hàng sheet có số × 31 ngày 2026-10-31…2026-11-30 · ô số {d['o_so']} "
                    f"(mong {mong['o_so']}) · ngày 0 ô: {len(d['ngay_0_o'])} · nhãn che {len(d['nhan_che'])}")}
