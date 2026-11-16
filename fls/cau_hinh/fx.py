"""`IX.FX` — **tỷ giá tháng**: nạp + kiểm *(AP v3.1.2 §3.2.1 · §3.2.4 · §3.5.3 D1)*.

ISP 3.1.2 · Step 2 · `C1` *(`WO-075`)* — làn **BE-CF**. Khuôn bảng *(AP §3.2.1)*:
**một dòng mỗi tháng `yyyymm` × 5 tiền tệ** `USD · SGD · COP · VND · HKD`, **VND = 1**.

⛔⛔ **Vì sao tệp này nói `thieu` · `trung` · `lac` thành TRƯỜNG RIÊNG — bia của hai
   lỗi AS-IS đã đo** *(AP §3.2.4, cột DK phiên 13/11)*. Ở trang tính, bảng
   `9.2.Exchange Rate` được tra bằng `SUMIFS(tháng)`:
     · **tháng THIẾU** ⇒ `SUMIFS = 0` ⇒ mọi số quy đổi của tháng ấy thành `0` —
       **mất số mà ⛔ báo gì**;
     · **tháng nhập HAI dòng** ⇒ `SUMIFS` **cộng đôi** tỷ giá.
   Cả hai **IM LẶNG**: trang tính vẫn ra một con số, chỉ là con số sai. ⇒ Ở đây
   ⛔ có phép tra nào *"cộng các dòng của tháng"*, ⛔ có tháng nào được *"mặc định
   0"*: thiếu/trùng/lạc là **ba danh sách tháng có tên**, và mọi dòng — kể cả dòng
   trùng, dòng lạc — **hiện nguyên** trong `ky`. Engine *(H4…)* đọc tỷ giá qua
   `fx_cua()` của `C7` — chỗ **CHẶN** tháng thiếu/chưa ký *(D1)*, ⛔ ở đây.

⛔ **Một ô sai thì NỔ, ⛔ thành 0** — `LoiFX` mang **mọi** lý do, mỗi lý do nói
   **tháng nào · cột nào**, gói trong **một dòng** *(luật phòng tái phạm `S0-R1-04`:
   *"phép kiểm đỏ phải in nguyên nhân đọc được trong một dòng"*)*. Hai lớp lỗi khác
   nhau về hậu quả nên ⛔ trộn:
     · **dòng hỏng** *(thiếu tiền tệ · VND ≠ 1 · ô ⛔ phải số · tỷ giá ≤ 0 · cột lạ ·
       tháng sai khuôn)* ⇒ `LoiFX` — bảng ⛔ đọc được, ⛔ trả nửa bảng;
     · **tháng thiếu/trùng/lạc** ⇒ bảng ĐỌC ĐƯỢC, và ba danh sách nói ra chỗ lệch
       *(FE `F4` gắn nhãn CHẶN · TRÙNG · LẠC)*.

⭐ **`lac` — định nghĩa CỦA BƯỚC NÀY, ⛔ có trong spec** *(`Đ1`, grep 16/11 trước
   khi viết tệp này: `dòng lạc|tháng lạc` ở `docs/` = **8** tệp — cả 8 đều chép câu
   AP *"kể cả dòng lạc 202306"* hay hàng `C5-B1`/`F4-F1` của ISP; `fls/` + `tools/`
   = **3** tệp có chữ `lạc`/`lac` mà đều nghĩa khác *(“lạc hậu” · “lạc sang dòng
   khác” · “giá trị lạc chỗ”)* ⇒ **0** định nghĩa máy)*. Chọn: nguồn khai
   **`thang_dau`** *(tháng đầu của dải)*; tháng
   **trước** `thang_dau` là **lạc**, dải = `[thang_dau … tháng lớn nhất]`, lỗ trong
   dải là **thiếu**. Vì sao ⛔ suy dải từ dữ liệu:
     · *"chuỗi tháng liền dài nhất"* ⇒ 4 tháng `06·07·_·09·10` tách đôi, một nửa
       thành *lạc* — tức một tháng THIẾU **biến mất** khỏi `thieu`;
     · *"tháng đứng lẻ, ⛔ hàng xóm"* ⇒ `…·08·_·10` biến `10` thành lạc và `09` ⛔
       còn là thiếu — **giấu đúng tháng phải CHẶN** *(D1)*;
     · *"dòng sai thứ tự trong sheet"* ⇒ phụ thuộc thứ tự dòng, mà ảnh đóng băng
       *(`AnhChup` — checksum **độc lập thứ tự đọc**, `fls/oracle/anh_chup.py:27`)*
       ⛔ hứa giữ.
   Câu hỏi đã nêu ở `BG-076`; đổi định nghĩa chỉ đổi **một hàm** `kiem`.

⭐ **`yyyymm` là SỐ NGUYÊN** *(`202407`, ⛔ `"202407"`)* — hợp đồng liên làn do
   orchestrator chốt 16/11: engine H1 `fls/bao_cao/gl.py` nhận tỷ giá dạng
   `{int yyyymm: {tiền tệ: Decimal}}`. Nguồn ghi tháng bằng chuỗi 6 chữ số *(ô văn
   bản ở sheet)* vẫn nạp được và được **chuẩn về `int`** ở đây — một chỗ duy nhất;
   ⛔ hàm chuyển nào cho H1 ở tệp này *(nối hai bên là việc của H4)*. ⚠ ISP mục 6
   viết `trung = ['202407']` có dấu nháy — lệch kiểu với chốt này, ghi ở `BG-076`.

⛔ **Tầng này ⛔ biết kho** *(`.importlinter` hợp đồng 10)*: nguồn TĨNH của `C1`
   *(`NGUON_TINH` — 4 tháng **TỔNG HỢP**, số bịa có chủ đích)* là một tệp đi cùng
   gói, ⛔ phải kho. `C5` đổi nguồn sang kho config chỉ-thêm qua
   `fls/repo/cau_hinh_repo.py` và **GỠ** tệp tĩnh; `kiem` giữ nguyên.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping

BANG = "IX.FX"
# AP §3.2.1 — khoá · cột của `IX.FX`. Thứ tự = thứ tự cột của `9.2.Exchange Rate`.
TIEN_TE: tuple[str, ...] = ("USD", "SGD", "COP", "VND", "HKD")
# Tiền tệ GỐC: tỷ giá = 1 ở MỌI tháng *(AP §3.2.1 "VND (=1)")*.
TIEN_TE_GOC = "VND"
# D1: owner ký MỖI tháng — ký là `C7`. Nguồn tĩnh ⛔ mang chữ ký *(⛔ có người ký,
# ⛔ có token)* ⇒ mọi dòng của C1 đều `chua_ky`. Một tệp tĩnh mà tự khai `da_ky`
# là **giả chữ ký** ⇒ cột `trang_thai` trong nguồn là cột LẠ, bị từ chối.
CHUA_KY = "chua_ky"

# ⭐ Đường nguồn tĩnh — khai **MỘT chỗ, ở đây** *(tương đối gốc repo, dạng POSIX)*.
#   `fls/api/bang_tuyen.py` khai `nguon_tinh` bằng CHÍNH hằng này, và hàm xử lý
#   gọi `doc_tep()` với mặc định là nó ⇒ ⛔ chuỗi đường nào gõ lại ở chỗ thứ hai.
NGUON_TINH = "fls/cau_hinh/tinh/ix_fx_mau.json"
_GOC_REPO = Path(__file__).resolve().parents[2]

_YYYYMM = re.compile(r"^(\d{4})(0[1-9]|1[0-2])$")


class LoiFX(ValueError):
    """Bảng tỷ giá ⛔ đọc được. `ly_do` = **mọi** lý do, ⛔ chỉ lý do đầu."""

    def __init__(self, ly_do: Iterable[str]) -> None:
        self.ly_do = tuple(ly_do)
        super().__init__(f"⛔ {BANG} ⛔ đọc được — {len(self.ly_do)} lỗi: "
                         + " · ".join(self.ly_do))


@dataclass(frozen=True)
class DongFX:
    yyyymm: int
    ty_gia: Mapping[str, Decimal]
    trang_thai: str = CHUA_KY


@dataclass(frozen=True)
class BangFX:
    nguon: str
    ky: tuple[DongFX, ...]
    thieu: tuple[int, ...]
    trung: tuple[int, ...]
    lac: tuple[int, ...]


def _mot_dong_mot_cau(s: Any) -> str:
    """Giá trị lạ đưa vào câu lỗi — ⛔ để nó phá luật *"một dòng"*."""
    return " ".join(repr(s).split())


def _thang(v: Any) -> int | None:
    """`yyyymm` hợp lệ ⇒ **`int`** *(vd `202407`)*; ngược lại `None`.

    Nhận `int` hay chuỗi 6 chữ số. ⛔ Nhận `bool`: `True` là `int` trong Python và
    sẽ lọt thành *"tháng 1"* nếu ⛔ chặn tường minh.
    """
    if isinstance(v, bool) or not isinstance(v, (str, int)):
        return None
    s = str(v).strip()
    return int(s) if _YYYYMM.match(s) else None


def _so(v: Any) -> Decimal | None:
    """Tỷ giá ⇒ `Decimal` hữu hạn **> 0**; ngược lại `None`.

    ⛔ Nhận `float`: một số đã qua `float` là số đã có thể mất chữ số
      *(`fls/api/bao.py`)* — nguồn phải đưa CHUỖI, hay JSON đọc bằng
      `parse_float=Decimal` *(đúng cách `doc_tep` đọc)*.
    """
    if isinstance(v, bool) or not isinstance(v, (str, int, Decimal)):
        return None
    try:
        d = Decimal(str(v).strip())
    except InvalidOperation:
        return None
    return d if d.is_finite() and d > 0 else None


def _thang_ke(m: int) -> int:
    n, t = divmod(m, 100)
    return (n + 1) * 100 + 1 if t == 12 else m + 1


def kiem(dong: Iterable[Mapping[str, Any]], *, thang_dau: int | str,
         nguon: str) -> BangFX:
    """Kiểm **thuần** một bảng tỷ giá. Dòng hỏng ⇒ `LoiFX`; còn lại ⇒ `BangFX`.

    `thang_dau` — tháng đầu của dải *(xem docstring tệp: định nghĩa `lac`)*.
    `nguon` — đi nguyên vào `BangFX.nguon` *(⛔ suy, ⛔ sửa)*.
    """
    ly_do: list[str] = []
    dau = _thang(thang_dau)
    if dau is None:
        ly_do.append(f"thang_dau={_mot_dong_mot_cau(thang_dau)} ⛔ phải yyyymm")

    ky: list[DongFX] = []
    cot = {"yyyymm", *TIEN_TE}
    for i, r in enumerate(dong, start=1):
        if not isinstance(r, Mapping):
            ly_do.append(f"dòng {i}: ⛔ phải một đối tượng")
            continue
        m = _thang(r.get("yyyymm"))
        ten = m if m is not None else _mot_dong_mot_cau(r.get("yyyymm"))
        if m is None:
            ly_do.append(f"dòng {i} ({ten}): yyyymm ⛔ đúng khuôn yyyymm")
        la = sorted(k for k in r if k not in cot)
        if la:
            ly_do.append(f"dòng {i} ({ten}): cột lạ {la}")
        ty_gia: dict[str, Decimal] = {}
        for te in TIEN_TE:
            if te not in r:
                ly_do.append(f"dòng {i} ({ten}): thiếu cột {te}")
                continue
            d = _so(r[te])
            if d is None:
                ly_do.append(f"dòng {i} ({ten}): {te}={_mot_dong_mot_cau(r[te])}"
                             f" ⛔ phải số > 0 (⛔ float, ⛔ rỗng)")
                continue
            ty_gia[te] = d
        if TIEN_TE_GOC in ty_gia and ty_gia[TIEN_TE_GOC] != 1:
            ly_do.append(f"dòng {i} ({ten}): {TIEN_TE_GOC}={ty_gia[TIEN_TE_GOC]}"
                         f" ⛔ = 1")
        if m is not None and len(ty_gia) == len(TIEN_TE):
            ky.append(DongFX(yyyymm=m, ty_gia=ty_gia))

    if ly_do:
        raise LoiFX(ly_do)

    # ⛔ `Đ3`: thiếu = trùng = lạc = rỗng trên **0** tháng là xanh trên tập rỗng.
    trong_dai = sorted({d.yyyymm for d in ky if d.yyyymm >= dau})
    if not trong_dai:
        raise LoiFX([f"0 tháng ≥ thang_dau={dau} (đọc {len(ky)} dòng) ⇒ "
                     f"⛔ có bảng để kiểm"])

    dem: dict[str, int] = {}
    for d in ky:
        dem[d.yyyymm] = dem.get(d.yyyymm, 0) + 1
    trung = tuple(sorted(m for m, n in dem.items() if n >= 2))
    lac = tuple(sorted(m for m in dem if m < dau))

    thieu: list[int] = []
    m = dau
    co = set(trong_dai)
    while m <= trong_dai[-1]:
        if m not in co:
            thieu.append(m)
        m = _thang_ke(m)

    # ⭐ Sắp theo tháng, **ổn định** ⇒ hai dòng trùng giữ thứ tự nguồn.
    return BangFX(nguon=nguon,
                  ky=tuple(sorted(ky, key=lambda d: d.yyyymm)),
                  thieu=tuple(thieu), trung=trung, lac=lac)


def doc_tep(duong: str = NGUON_TINH) -> BangFX:
    """Nạp nguồn tĩnh *(tương đối gốc repo)* rồi `kiem`. `nguon` = chính `duong`.

    ⭐ `parse_float=Decimal`: một tỷ giá ghi bằng số JSON ⛔ đi qua `float`.
    """
    tho = json.loads((_GOC_REPO / duong).read_text(encoding="utf-8"),
                     parse_float=Decimal)
    if not isinstance(tho, dict) or tho.get("bang") != BANG \
            or not isinstance(tho.get("dong"), list):
        raise LoiFX([f"{duong}: ⛔ phải {{bang: '{BANG}', thang_dau, dong: [...]}}"])
    return kiem(tho["dong"], thang_dau=tho.get("thang_dau"), nguon=duong)
