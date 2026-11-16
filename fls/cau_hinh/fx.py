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

── ⛔⛔ Vòng sửa sau R1 *(`KQ-077`, 16/11)* — ba lối vào từng đi qua IM LẶNG hay MÉO ──
   R1 dò thuần trên bản sao *(31 ca biên + 13 đột biến)*; mã cũ đúng ở mọi ca spec có,
   nhưng:
     · **`C1-R1-02`** — `doc_tep` đọc `_GOC_REPO / duong`: `Path / '/etc/hostname'` LÀ
       `/etc/hostname`, `..` ra ngoài repo ⇒ nay đi qua `nguon_tinh.giai` *(luật đường
       MỘT chỗ, chung với hai cổng bảng tuyến)*;
     · **`C1-R1-06`** ⓐ khoá JSON TRÙNG trong một dòng ⇒ `json.loads` giữ **bản cuối**,
       im lặng *(cùng họ "hai giá trị, giữ một" mà `trung` chặn ở mức tháng)*; ⓑ
       `Decimal` nhận số mũ *(`'1e4'` ⇒ ra JSON tuyến thành `"1E+4"`)* và chữ số
       Unicode *(`'１２３'` ⇒ `123`)*; ⓒ khuôn tháng `\\d` cũng nhận chữ số Unicode, và
       năm `0000` lọt *(`'000001'` ⇒ `lac = [1]`)*. ⇒ từ chối, **gọi tên** từng lối;
     · **`C1-R1-04`** — mỗi chốt *(`is_finite` · chặn `bool`)* nay trả một **lý do có
       tên** riêng: chốt nào bị gỡ thì câu nổ đổi, và có bài đỏ *(xem `_thang`)*.
   Lõi đọc tách thành `doc_van_ban` để bài thử khỏi phải ghi tệp vào thư mục tĩnh —
   thư mục DUY NHẤT `doc_tep` nay chịu đọc.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable, Mapping

from fls.cau_hinh import nguon_tinh

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
#   ⚠ Phải nằm NGAY dưới `nguon_tinh.THU_MUC` *(luật đường — `C1-R1-02`)*.
#   ⚠ `tools/soi_bang_tuyen.py` đòi chuỗi này hiện NGUYÊN VĂN trong một hàm của
#   đường gọi `ty_gia` *(tham số mặc định của `doc_tep` — giữ nó là hằng chuỗi trơn,
#   ⛔ ghép bằng f-string)*.
NGUON_TINH = "fls/cau_hinh/tinh/ix_fx_mau.json"

# ⭐ `C1-R1-06` ⓒ: năm **2000…2099**, tháng `01…12`, chữ số **ASCII** *(khuôn cũ
#   `^(\d{4})…$` — `\d` của `re` trên `str` nhận MỌI chữ số Unicode, nên
#   `'２０２４06'` thành `202406`; và năm `0000` lọt: `'000001'` ⇒ `lac = [1]`)*.
#   Biên năm là chốt HÌNH *(cùng loại với "tháng 01…12")*, ⛔ luật nghiệp vụ: sổ ITL
#   bắt đầu `2023` *(dòng lạc `202306`, AP §3.2.1)*, ảnh thật tới `202612` — năm ngoài
#   `20YY` chỉ có thể là gõ nhầm.
_YYYYMM = re.compile(r"20[0-9]{2}(?:0[1-9]|1[0-2])", re.ASCII)
# ⭐ `C1-R1-06` ⓑ: tỷ giá là thập phân **ASCII trơn** — ⛔ số mũ, ⛔ dấu `+`, ⛔ chữ số
#   ngoài ASCII *(`Decimal('１２３') == 123`, `Decimal('1e4')` in ra `'1E+4'`)*. Ảnh
#   thật `DT2` *(37 dòng × 5 tiền tệ, `tests/fixture/cau_hinh/ix_fx.json` nhánh DT2)*
#   đo 16/11: **185/185** ô khớp khuôn này.
_SO_THAP_PHAN = re.compile(r"[0-9]+(?:\.[0-9]+)?", re.ASCII)


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


def _thang(v: Any) -> tuple[int | None, str]:
    """`yyyymm` hợp lệ ⇒ `(int, "")` *(vd `202407`)*; ngược lại `(None, lý do)`.

    Nhận `int` hay chuỗi 6 chữ số ASCII. ⛔ Nhận `bool`.

    ⚠ Câu cũ ở đây *("`True` … sẽ lọt thành tháng 1 nếu ⛔ chặn tường minh")* **SAI
      cơ chế** — `C1-R1-04`: hàm đọc qua `str(v)` ⇒ `'True'` vốn trượt khuôn, có chốt
      hay ⛔. R1 gỡ chốt `bool` ⇒ 22/22 bài vẫn xanh: một chốt ⛔ bài nào canh. Cái
      chốt THẬT SỰ làm được là **gọi đúng tên nguyên nhân** — một ô `bool` *(ô tick ở
      sheet)* lọt vào cột tháng — thay cho câu chung chung *"⛔ đúng khuôn"* *(luật
      `S0-R1-04`)*. Bài `test_R1_04_bool_o_cot_THANG_…` ghim đúng điều ấy.
    """
    if isinstance(v, bool):
        return None, "bool (ô tick?) ⛔ phải tháng"
    if not isinstance(v, (str, int)):
        return None, f"kiểu {type(v).__name__} ⛔ phải yyyymm (int hay chuỗi 6 chữ số)"
    s = str(v).strip()
    if not _YYYYMM.fullmatch(s):
        return None, "⛔ đúng khuôn yyyymm (năm 2000…2099 · tháng 01…12 · chữ số ASCII)"
    return int(s), ""


def _so(v: Any) -> tuple[Decimal | None, str]:
    """Tỷ giá ⇒ `(Decimal hữu hạn > 0, "")`; ngược lại `(None, lý do)`.

    ⛔ Nhận `float`: một số đã qua `float` là số đã có thể mất chữ số
      *(`fls/api/bao.py`)* — nguồn phải đưa CHUỖI, hay JSON đọc bằng
      `parse_float=Decimal` *(đúng cách `doc_van_ban` đọc)*.
    ⭐ Thứ tự chốt CỐ Ý *(`C1-R1-04`)*: đọc số → **hữu hạn** → `> 0` → **khuôn**. Đặt
      khuôn lên đầu thì `NaN`/`Infinity` ⛔ bao giờ tới `is_finite()` — chốt ấy thành
      mã chết, gỡ đi ⛔ bài nào đỏ *(đúng thứ R1 đo được: đột biến M2 SỐNG)*. Đặt
      sau ⇒ gỡ `is_finite()` thì `'NaN'` ném `InvalidOperation` ở phép `<= 0` và
      `'Infinity'` mang lý do *"khuôn"* — bài `test_R1_01c_…` đỏ.
    """
    if isinstance(v, bool):
        return None, "bool (ô tick?) ⛔ phải số"
    if not isinstance(v, (str, int, Decimal)):
        return None, (f"kiểu {type(v).__name__} ⛔ nhận (⛔ float — qua float là mất "
                      f"chữ số; ⛔ rỗng)")
    s = str(v).strip()
    try:
        d = Decimal(s)
    except InvalidOperation:
        return None, "⛔ phải số (⛔ rỗng)"
    if not d.is_finite():
        return None, "⛔ hữu hạn (NaN/Infinity)"
    if d <= 0:
        return None, "⛔ > 0"
    if not _SO_THAP_PHAN.fullmatch(s):
        return None, ("⛔ đúng khuôn thập phân ASCII [0-9]+(.[0-9]+)? (⛔ số mũ · "
                      "⛔ dấu + · ⛔ chữ số ngoài ASCII)")
    return d, ""


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
    dau, ly = _thang(thang_dau)
    if dau is None:
        ly_do.append(f"thang_dau={_mot_dong_mot_cau(thang_dau)} {ly}")

    ky: list[DongFX] = []
    cot = {"yyyymm", *TIEN_TE}
    for i, r in enumerate(dong, start=1):
        if not isinstance(r, Mapping):
            ly_do.append(f"dòng {i}: ⛔ phải một đối tượng")
            continue
        m, ly = _thang(r.get("yyyymm"))
        ten = m if m is not None else _mot_dong_mot_cau(r.get("yyyymm"))
        if m is None:
            ly_do.append(f"dòng {i} ({ten}): yyyymm {ly}")
        la = sorted(k for k in r if k not in cot)
        if la:
            ly_do.append(f"dòng {i} ({ten}): cột lạ {la}")
        ty_gia: dict[str, Decimal] = {}
        for te in TIEN_TE:
            if te not in r:
                ly_do.append(f"dòng {i} ({ten}): thiếu cột {te}")
                continue
            d, ly = _so(r[te])
            if d is None:
                ly_do.append(f"dòng {i} ({ten}): {te}={_mot_dong_mot_cau(r[te])} {ly}")
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

    dem: dict[int, int] = {}          # ⚠ khoá là `int` *(cũ ghi `str` — `C1-R1-04`)*
    for d in ky:
        dem[d.yyyymm] = dem.get(d.yyyymm, 0) + 1
    trung = tuple(sorted(m for m, n in dem.items() if n >= 2))
    lac = tuple(sorted(m for m in dem if m < dau))

    # ⚠ GIỚI HẠN đã biết *(`C1-R1-05`, ⛔ sửa ở C1)*: dải kiểm ⛔ có BIÊN CUỐI do nguồn
    #   khai — nó dừng ở tháng LỚN NHẤT có dòng, nên tháng cuối chưa nhập ⛔ bao giờ vào
    #   `thieu` và một dòng gõ nhầm SAU dải làm phình `thieu` *(R1: `+202504` ⇒ 6 tháng)*
    #   ⇒ `fx_cua()` của `C7` phải CHẶN theo **tháng được hỏi** *(∉ `ky` hay chưa ký)*,
    #   ⛔ dựa vào `thieu` — orchestrator ghi vào phiếu `C7`.
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


def doc_van_ban(van_ban: str, *, nguon: str) -> BangFX:
    """Lõi đọc: VĂN BẢN JSON `{bang: 'IX.FX', thang_dau, dong: [...]}` ⇒ `kiem`.

    ⭐ `parse_float=Decimal`: một tỷ giá ghi bằng số JSON ⛔ đi qua `float`.
    ⛔ `C1-R1-06` ⓐ: khoá TRÙNG trong một đối tượng *(`{"USD": "1", "USD": "999"}`)*
      — `json.loads` mặc định giữ **bản CUỐI, im lặng**. Móc `object_pairs_hook` thấy
      MỌI cặp trước khi `dict` nuốt mất ⇒ gom hết, NỔ một lần, nói khoá nào · dòng nào.
    """
    trung: list[str] = []

    def _khong_trung(cap: list[tuple[str, Any]]) -> dict[str, Any]:
        lap = sorted(k for k, n in Counter(k for k, _ in cap).items() if n >= 2)
        if lap:
            o = next((v for k, v in cap if k == "yyyymm"), None)
            noi = (f"dòng yyyymm={_mot_dong_mot_cau(o)}" if o is not None
                   else "đối tượng ⛔ có yyyymm (vỏ tệp?)")
            trung.append(f"{noi}: khoá JSON trùng {lap} — json.loads giữ bản CUỐI "
                         f"im lặng")
        return dict(cap)

    tho = json.loads(van_ban, parse_float=Decimal, object_pairs_hook=_khong_trung)
    if trung:
        raise LoiFX([f"{nguon}: {x}" for x in trung])
    if not isinstance(tho, dict) or tho.get("bang") != BANG \
            or not isinstance(tho.get("dong"), list):
        raise LoiFX([f"{nguon}: ⛔ phải {{bang: '{BANG}', thang_dau, dong: [...]}}"])
    return kiem(tho["dong"], thang_dau=tho.get("thang_dau"), nguon=nguon)


def doc_tep(duong: str = NGUON_TINH) -> BangFX:
    """Nạp nguồn tĩnh *(tương đối gốc repo)* rồi `kiem`. `nguon` = chính `duong`.

    ⛔ `C1-R1-02`: CHỈ đọc tệp NGAY dưới `nguon_tinh.THU_MUC` *(luật đường một chỗ —
      ⛔ tuyệt đối, ⛔ `..`, ⛔ liên kết mềm ra ngoài)*. Bản cũ đọc `_GOC_REPO / duong`,
      và `Path / '/etc/hostname'` **là** `/etc/hostname`. Đường hỏng ⇒ `LoiFX` một
      dòng, ⛔ đọc gì.
    """
    try:
        p = nguon_tinh.giai(duong)
    except nguon_tinh.LoiNguonTinh as e:
        raise LoiFX([str(e)]) from None
    return doc_van_ban(p.read_text(encoding="utf-8"), nguon=duong)
