"""Thân CHUNG của 3 khuôn bộ ba HD1 *(`itl_ledge_adjustment` · `l1_canon` · `pm_join` — ISP 3.1.2 · `WO-353` C1 = ⓐ, chủ 23/11)*.

⭐ Vì sao có tệp này. Bộ ba ảnh HD1 tháng 8 *(`tests/fixture/itl_ledge_adjustment.json` xlsx 26/08 · `classifying_vs_canon.json`
L1 live 26/08 · `pm_join.json` 27/08)* ⛔ có khuôn trong repo *(BG-346 §1: `git log --diff-filter=A` = commit nhập `66cef65`; grep
`canon_pos_`/`classifying_vs_canon` ngoài NGƯỜI ĐỌC = 0)* ⇒ ⛔ đóng băng lại được. Chủ chọn ⓐ: viết khuôn trên hàm CÓ SẴN
*(`fls.adapters.bank.nap` · `fls.repo.chay_nap._bank_tu_canon` · `fls.adapters.pm_join` — `tools/nap_that.py` `doc_nguon`/`doc_pm`
gọi đúng các hàm ấy)* rồi đo lại HD1 GIỮ NGUYÊN định nghĩa đã ký.

⭐⭐ `classifying_vs_canon` ⛔ có khuôn riêng — nó ⛔ phải ảnh của MỘT nguồn: nó là KẾT QUẢ GHÉP sổ ↔ L1
*(`ghep_bang`: "khoa = (So chung tu, PS No, PS Co, Tai khoan, Don vi tien te) + seq trung")*. Ảnh tháng 8 đóng băng KẾT QUẢ ấy
mà ⛔ có mã sinh ⇒ ⛔ tái tạo được. Ở đây phép ghép thành MÃ: hai khuôn sổ + L1 cùng ghi cột `khoa_ghep` bằng CHÍNH hàm
`khoa_ghep` dưới; bên đọc *(`tools/do_voi_so_luong.py`)* ghép theo `khoa_ghep` + thứ tự sheet *(seq trùng)*. ⇒ ảnh ⛔ mang
`Số chứng từ` của SỔ *(DT12 xếp nó vào cột CẤM — có thể mang tên người)*: chỉ mang BĂM 16 hex của 5 trường đã chuẩn hoá.

⛔⛔ Lời lỗi KHÔNG mang giá trị ô *(như `itl_ledge_ky`)*.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from decimal import Decimal, InvalidOperation
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from fls.adapters.pm_join import PM_COT_RIENG_TU, canon_ref  # noqa: E402
from fls.canon.validate import parse_so                       # noqa: E402

#: Tên 5 cột khoá ghép — hàng 7 của `ITL Ledge` *(A–G = khuôn canon A–G, BA-05 §DD-I04)* VÀ hàng 3 của L1 *(`fls.canon.spec`)*.
TEN_KHOA = {"so_ct": "Số chứng từ", "cur": "Đơn vị tiền tệ", "no": "PS Nợ", "co": "PS Có", "tk": "Tài khoản"}
#: vị trí 0-based ở CẢ HAI lưới *(sổ A–G ≡ canon A–G)*: B · D · E · F · G.
VT_KHOA = {"so_ct": 1, "cur": 3, "no": 4, "co": 5, "tk": 6}


def rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def chu_so(v: Any) -> str:
    """Số → chuỗi thập phân CHÍNH TẮC *(`202603.0` ⇒ `202603`; ⛔ float — qua `Decimal(str())`)*. = `itl_ledge_ky._chu_so`."""
    d = Decimal(str(v))
    return str(int(d)) if d == d.to_integral_value() else format(d.normalize(), "f")


def o_chu(v: Any) -> str | None:
    """Ô thô → ô ẢNH: rỗng ⇒ `None` · số ⇒ CHỮ số thập phân · chữ ⇒ GIỮ NGUYÊN *(kể cả chuỗi lỗi `#N/A (…)` — Classifying/canon
    `#N/A` là CÂU TRẢ LỜI "máy ⛔ trả lời", ảnh tháng 8 cũng giữ nguyên)*. `bool` ⇒ `ValueError` *(⛔ đo được)*."""
    if rong(v):
        return None
    if isinstance(v, bool):
        raise ValueError("ô là bool — ⛔ đo được")
    if isinstance(v, (int, float, Decimal)):
        return chu_so(v)
    if isinstance(v, str):
        return v
    raise ValueError(f"ô kiểu {type(v).__name__} — ⛔ đo được")


def _tien(v: Any) -> str:
    s = parse_so(v)
    if s is None:
        return "0"                                  # rỗng ≡ 0 ở PS Nợ/Có *(một dòng chỉ ghi MỘT phía)*
    try:
        d = Decimal(str(s))
    except InvalidOperation:
        raise ValueError("PS Nợ/Có ⛔ phải số") from None
    return "0" if d == 0 else format(d.normalize(), "f")


def _tk(v: Any) -> str:
    if rong(v):
        return ""
    if isinstance(v, (int, float, Decimal)) and not isinstance(v, bool):
        return chu_so(v)
    return " ".join(str(v).split())


def khoa_ghep(hang: list[Any]) -> str:
    """Khoá ghép sổ ↔ L1 = sha256 *(16 hex)* của `[Số CT · PS Nợ · PS Có · TK · tiền tệ]` ĐÃ CHUẨN HOÁ.
    Chuẩn hoá chặn đúng hai chỗ `ban_xuat_lam_hong` của ảnh tháng 8 đã đo *("PS No/Co ... CHUOI co dau phan cach; So chung tu dai
    ... dang khoa hoc. Khong chuan hoa hai cho nay thi ty le ghep tu 98,8% roi con 16,6%")*: Số CT qua `canon_ref` *(MỘT hàm với
    phép ghép PM — dựng lại số khoa học)*, tiền qua `parse_so` + `Decimal.normalize` *(rỗng ≡ 0)*. ⛔ dùng Ngày *(ảnh tháng 8
    cũng ⛔)* · ⛔ dùng Diễn giải *(PII)*."""
    g = [hang[i] if i < len(hang) else None for i in (VT_KHOA["so_ct"], VT_KHOA["no"], VT_KHOA["co"], VT_KHOA["tk"],
                                                      VT_KHOA["cur"])]
    phan = [canon_ref(g[0]) or "", _tien(g[1]), _tien(g[2]), _tk(g[3]), " ".join(str(g[4] or "").split()).upper()]
    return hashlib.sha256(json.dumps(phan, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()[:16]


def kiem_ten_khoa(hang_tieu_de: list[Any], noi: str) -> None:
    """5 tên cột khoá ở ĐÚNG vị trí *(ánh xạ theo TÊN — cột xê dịch thì khoá lệch IM LẶNG)*."""
    h = [" ".join(str(x or "").split()) for x in hang_tieu_de] + [""] * 8
    sai = [k for k, i in VT_KHOA.items() if h[i] != TEN_KHOA[k]]
    if sai:
        raise ValueError(f"{noi}: tên cột khoá ghép lệch ở {sorted(sai)} — ánh xạ theo TÊN nên ⛔ đóng băng")


def soat_rieng_tu(ten_cot: list[Any], noi: str) -> None:
    ban_den = {" ".join(str(x).split()) for x in PM_COT_RIENG_TU}
    cam = sorted({" ".join(str(x or "").split()) for x in ten_cot} & ban_den)
    if cam:
        raise ValueError(f"{noi}: bản thô mang cột riêng tư {cam} — ⛔ vào ảnh (bản thô phải CHIẾU bỏ cột ấy trước)")


def u(v: Any) -> Any:
    """Ô ảnh `{"chu": s}` ⇒ `s` *(bên đọc)*."""
    return v.get("chu") if isinstance(v, dict) else v
