"""`IX.HD` — **cây hợp đồng (HD)**: nạp ảnh ATL + kiểm cha–con *(AP v3.1.2 §3.2.1
IX.HD · §3.2.5 · §3.2.4 "cây HD theo vị trí dòng" · WP-C1)*.

ISP 3.1.2 · Step 11 · `C4` *(`WO-122`)* — làn **BE-CF**. Dùng lại khuôn tuyến TĨNH
của `C1` *(`fls/cau_hinh/fx.py` + `fls/api/xu_ly.py:ty_gia` + `nguon_tinh`)*: tuyến
đọc một ẢNH đi cùng gói, ⛔ đọc kho *(kho config là `C5`)*.

⭐ **Ảnh ATL = một RỪNG, ⛔ phải một cây** *(đo DT3, 17/11)*: **74** nút mã · **6**
   nhóm `HDO · HDH · HDAP · HDT · HDC · HDCI` · **37** gốc *(mọi dòng `cap = 1`,
   `cha = null`)*. Phân cấp: `37` · `23` · `11` · `3` *(L1…L4)* — `MONG_CAP`. Mỗi
   nhóm là một khối trong lưới SA; `cha` = dòng mã gần nhất phía trên có cấp nhỏ
   hơn, TRONG nhóm *(tiêu đề nhóm xoá ngăn — ảnh đã dựng sẵn ở DT3, `ghi_chu_khuon`)*.

⛔⛔ **Vì sao kiểm cha–con là việc CỦA BƯỚC NÀY, ⛔ của engine** *(`Đ4` — mỗi số
   đếm một vật)*. `C4` kiểm **HÌNH của cây**: cha có thật, ⛔ chu trình, cấp ⛔ nhảy.
   `cha = Σ con` *(giá trị)* là việc engine **H5** *(Step 13)* — ⛔ ở đây; kho là
   `C5`; hoà giải `74 ↔ 73` *(ATL vs Mapping Master)* **⛔ bao giờ** — chỉ **liệt kê
   chênh** *(ràng buộc WO-122, `BG-107`: `ATL − MM = {NCF}`)*.

⛔ **Lỗi cây mang TÊN *(hằng chuỗi)*, ⛔ `ValueError` trơn** *(ràng buộc WO-122;
   luật `S0-R1-04`: phép kiểm đỏ in nguyên nhân đọc được trong một dòng)*. Ba tên
   bắt buộc + hai tên phòng thủ:
     · `HD_CHU_TRINH`  — A→B→A *(đi theo `cha` gặp lại một nút đã thăm)*;
     · `HD_CHA_VANG`   — `cha` trỏ một mã ⛔ có trong ảnh;
     · `HD_CAP_NHAY`   — cấp con ≠ cấp cha + 1 *(con cấp n+2 dưới cha cấp n), và gốc
                          ⛔ ở cấp 1* — cùng một bất biến: **cấp = độ sâu**;
     · `HD_MA_TRUNG`   — hai dòng cùng mã *(khoá cây ⛔ xác định — im lặng ghi đè)*;
     · `HD_HONG`       — ô hỏng *(ⓛ sai vỏ · mã rỗng · cấp ⛔ phải 1…n · thiếu cột)*.

⭐ **Vì sao gom HẾT lý do rồi NỔ một lần** *(cùng `fx.LoiFX`)*: `Đ5` đòi cổng in
   **mọi** chỗ lệch, ⛔ dừng ở lỗi đầu. Một ảnh vừa thiếu cha vừa nhảy cấp phải hiện
   **cả hai** — người sửa ảnh ⛔ phải chạy lại để thấy lỗi thứ hai.
⚠ Một nút trong CHU TRÌNH thường cũng vấp `HD_CAP_NHAY` *(chu trình ⇒ ⛔ có cấp
   nhất quán)*. Hai phép đo ĐỘC LẬP, mỗi phép một cổng — ⛔ nuốt phép này vào phép
   kia *(gỡ một cổng thì phải có một bài đổi màu)*; `ten` là **tập**, bài so *"X ∈
   ten"*, ⛔ *"ten == {X}"*.

⛔ **Ô ảnh bọc trong `{"chu": …}`** *(kiểu "chữ" lúc chụp, DT3)*: `ma · ten · cha ·
   nhom` bọc; `cap · dong_sheet` để TRẦN; `cha = null` ở gốc. `_chu` gỡ vỏ **MỘT
   chỗ** — vỏ lạ ⇒ `HD_HONG`, ⛔ đoán.

⛔ **Tầng này ⛔ biết kho** *(`.importlinter` hợp đồng 10)*: nguồn TĨNH là ẢNH ĐÓNG
   BĂNG THẬT đi cùng gói *(`NGUON_TINH` · `NGUON_MM` — chép từ ảnh DT3, checksum
   khớp, bài `tests/cau_hinh/test_hd.py` ghim)*. `C5` đổi nguồn sang kho config
   chỉ-thêm và **GỠ** hai tệp tĩnh; `kiem` giữ nguyên.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from fls.cau_hinh import nguon_tinh

BANG = "IX.HD"
# Nhóm Mapping Master mang thêm `IX.ORG` ở cùng tệp ⇒ vỏ ảnh ghi `IX.HD · IX.ORG`.
BANG_MM = "IX.HD · IX.ORG"

# ⭐ Đường ẢNH TĨNH — khai **MỘT chỗ, ở đây** *(tương đối gốc repo, POSIX)*. Phải nằm
#   NGAY dưới `nguon_tinh.THU_MUC` *(luật đường — `C1-R1-02`)*. `fls/api/bang_tuyen.py`
#   khai `nguon_tinh=(hd.NGUON_TINH, hd.NGUON_MM)` bằng CHÍNH hai hằng này, và hàm xử
#   lý gọi `doc_tep()`/`doc_mm()` với mặc định là chúng ⇒ ⛔ chuỗi đường nào gõ lại ở
#   chỗ thứ hai *(cổng `soi_bang_tuyen` ⓔ2 đòi đường khai hiện NGUYÊN VĂN trong đồ thị
#   gọi của hàm; giữ hằng chuỗi trơn, ⛔ ghép f-string)*.
NGUON_TINH = "fls/cau_hinh/tinh/ix_hd_cay.json"
NGUON_MM = "fls/cau_hinh/tinh/ix_mapping_master.json"

# ── Tên lỗi cây *(hằng chuỗi — ⛔ `ValueError` trơn)* ───────────────────────────
HD_CHU_TRINH = "HD_CHU_TRINH"      # A→B→A
HD_CHA_VANG = "HD_CHA_VANG"        # cha trỏ mã ⛔ có
HD_CAP_NHAY = "HD_CAP_NHAY"        # cấp con ≠ cấp cha + 1 (hay gốc ⛔ cấp 1)
HD_MA_TRUNG = "HD_MA_TRUNG"        # hai dòng cùng mã
HD_HONG = "HD_HONG"                # ô/vỏ hỏng

# Cột bắt buộc của một dòng ảnh ATL *(khoá `ma` + 5 cột — `atl_cay.json:cot`)*.
COT = ("ma", "ten", "cha", "cap", "nhom", "dong_sheet")


class LoiHD(ValueError):
    """Cây IX.HD ⛔ đọc được. `loi` = **mọi** `(tên, chi tiết)`, ⛔ chỉ lỗi đầu."""

    def __init__(self, loi: Iterable[tuple[str, str]]) -> None:
        self.loi = tuple(loi)
        # `ten` = TẬP tên lỗi *(bài so "X ∈ ten", ⛔ "ten == {X}")*.
        self.ten = frozenset(t for t, _ in self.loi)
        super().__init__(f"⛔ {BANG} ⛔ đọc được — {len(self.loi)} lỗi: "
                         + " · ".join(f"{t}: {c}" for t, c in self.loi))


@dataclass(frozen=True)
class NutHD:
    ma: str
    ten: str
    cha: str | None
    cap: int
    nhom: str
    dong_sheet: str
    thu_tu: int


@dataclass(frozen=True)
class CayHD:
    nguon: str
    nut: tuple[NutHD, ...]        # theo `thu_tu` của ảnh

    def _theo_ma(self) -> dict[str, NutHD]:
        return {n.ma: n for n in self.nut}

    @property
    def goc(self) -> tuple[str, ...]:
        """Mã của mọi GỐC *(`cha` None)* — theo thứ tự ảnh. ATL thật: **37**."""
        return tuple(n.ma for n in self.nut if n.cha is None)

    def con_cua(self, ma: str) -> tuple[str, ...]:
        """Mã các con TRỰC TIẾP của `ma` — theo thứ tự ảnh *(ổn định)*."""
        return tuple(n.ma for n in self.nut if n.cha == ma)

    def la(self, ma: str) -> bool:
        """`ma` là LÁ *(⛔ có con nào)*. ⛔ Có `ma` ⇒ `KeyError` *(⛔ trả True câm)*."""
        if ma not in self._theo_ma():
            raise KeyError(ma)
        return not any(n.cha == ma for n in self.nut)

    def dem_cap(self) -> dict[int, int]:
        """Số nút MỖI cấp *(`MONG_CAP` — đo trên ảnh)*. ATL thật: `{1:37,2:23,3:11,4:3}`."""
        return dict(Counter(n.cap for n in self.nut))

    @property
    def nhom(self) -> tuple[str, ...]:
        """Các nhóm có mặt, theo thứ tự xuất hiện. ATL thật: **6** nhóm."""
        ra: list[str] = []
        for n in self.nut:
            if n.nhom not in ra:
                ra.append(n.nhom)
        return tuple(ra)


def _mot_dong(s: Any) -> str:
    """Giá trị lạ đưa vào câu lỗi — ⛔ để nó phá luật *"một dòng"*."""
    return " ".join(repr(s).split())


def _chu(o: Any) -> tuple[str | None, str]:
    """Gỡ vỏ ô ảnh. `{"chu": str}` ⇒ `(str, "")`; chuỗi trần ⇒ `(str, "")`;
    `None` ⇒ `(None, "")` *(cho `cha` gốc)*; vỏ lạ ⇒ `(None, lý do)`.

    ⛔ Nhận `{"chu": …}` CÓ đúng một khoá `chu` kiểu `str`, hay `str`/`None` trần —
      vỏ khác *(nhiều khoá · `chu` ⛔ phải chuỗi · kiểu lạ)* là ẢNH HỎNG, ⛔ đoán.
    """
    if o is None:
        return None, ""
    if isinstance(o, str):
        return o, ""
    if isinstance(o, Mapping):
        if set(o) == {"chu"} and isinstance(o["chu"], str):
            return o["chu"], ""
        return None, f"vỏ ô lạ {_mot_dong(o)} (⛔ phải {{'chu': str}})"
    return None, f"kiểu ô {type(o).__name__} ⛔ nhận (⛔ phải {{'chu': str}} hay chuỗi)"


def _so(v: Any) -> tuple[int | None, str]:
    """`int` hay chuỗi chữ số **ASCII** ⇒ số nguyên; ⛔ `bool`, ⛔ chữ số ngoài ASCII.

    ⚠ `isdigit()` nhận cả `'²'` *(`int('²')` NÉM `ValueError`)* và `'١'` *(chữ số Ả
      Rập — `int('١')` lặng lẽ = 1)*; cả hai ⛔ phải chuỗi `0-9` ⇒ kèm `isascii()`
      *(`C4-R1-01`: `isdigit()` ⛔ đủ cho `int()`)*. Hỏng ⇒ `(None, lý do một dòng)`.
    """
    if isinstance(v, bool):
        return None, f"{_mot_dong(v)} là bool ⛔ phải số"
    if isinstance(v, int):
        return v, ""
    if isinstance(v, str) and (s := v.strip()).isascii() and s.isdigit():
        return int(s), ""
    return None, f"{_mot_dong(v)} ⛔ phải số nguyên"


def _cap(v: Any) -> tuple[int | None, str]:
    """`cap` ⇒ số nguyên ≥ 1 *(qua `_so` — ⛔ `bool`, ⛔ chữ số ngoài ASCII)*; ⛔ 0/âm."""
    n, _ = _so(v)
    if n is None:
        return None, f"cap={_mot_dong(v)} ⛔ phải số nguyên ≥ 1"
    if n < 1:
        return None, f"cap={n} ⛔ ≥ 1"
    return n, ""


def kiem(dong: Iterable[Mapping[str, Any]], *, nguon: str) -> CayHD:
    """Kiểm **thuần** cây IX.HD. Ô/cây hỏng ⇒ `LoiHD` *(mọi lý do)*; còn lại ⇒ `CayHD`.

    `nguon` — đi nguyên vào `CayHD.nguon` *(⛔ suy, ⛔ sửa)*.

    ⭐ Thứ tự: dọn HÌNH từng dòng *(vỏ ô, cấp)* → bắt `HD_MA_TRUNG` → dựng nút →
      `HD_CHA_VANG` → `HD_CHU_TRINH` → `HD_CAP_NHAY`. `Đ3`: tập nút KHÔNG RỖNG mới
      kết luận — 0 nút ⇒ `HD_HONG` *(⛔ "cây sạch trên tập rỗng")*.
    """
    loi: list[tuple[str, str]] = []
    nut: list[NutHD] = []
    cot = set(COT)

    for i, r in enumerate(dong, start=1):
        if not isinstance(r, Mapping):
            loi.append((HD_HONG, f"dòng {i}: ⛔ phải một đối tượng"))
            continue
        thua = sorted(k for k in r if k not in cot and k != "thu_tu")
        if thua:
            loi.append((HD_HONG, f"dòng {i}: cột lạ {thua}"))
        ma, ly = _chu(r.get("ma"))
        ten_hien = ma if ma else _mot_dong(r.get("ma"))
        if ma is None or not ma:
            loi.append((HD_HONG, f"dòng {i} ({ten_hien}): ma {ly or 'rỗng'}"))
        ten, ly = _chu(r.get("ten"))
        if ten is None:
            loi.append((HD_HONG, f"dòng {i} ({ten_hien}): ten {ly}"))
        cha, ly = _chu(r.get("cha"))        # None = gốc (hợp lệ)
        if ly:
            loi.append((HD_HONG, f"dòng {i} ({ten_hien}): cha {ly}"))
        nhom, ly = _chu(r.get("nhom"))
        if nhom is None or not nhom:
            loi.append((HD_HONG, f"dòng {i} ({ten_hien}): nhom {ly or 'rỗng'}"))
        ds, ly = _chu(r.get("dong_sheet"))
        if ds is None:
            loi.append((HD_HONG, f"dòng {i} ({ten_hien}): dong_sheet {ly}"))
        cap, ly = _cap(r.get("cap"))
        if cap is None:
            loi.append((HD_HONG, f"dòng {i} ({ten_hien}): {ly}"))
        # `thu_tu` TÙY CHỌN *(⛔ trong COT)*: vắng ⇒ vị trí dòng; có mà hỏng ⇒ `HD_HONG`
        #   *(⛔ `int(...)` trơn: `thu_tu='abc'`→`ValueError`, `None`→`TypeError` — `C4-R1-01`)*.
        tt: int | None = i
        if "thu_tu" in r:
            tt, ly = _so(r["thu_tu"])
            if tt is None:
                loi.append((HD_HONG, f"dòng {i} ({ten_hien}): thu_tu {ly}"))
        # Chỉ dựng nút khi đủ trường — một nút hỏng ⛔ được lẻn vào phép kiểm cây.
        if ma and cap is not None and tt is not None:
            nut.append(NutHD(ma=ma, ten=ten or "", cha=cha, cap=cap,
                             nhom=nhom or "", dong_sheet=ds or "", thu_tu=tt))

    # `HD_MA_TRUNG` — khoá cây ⛔ xác định *(`json`/`dict` giữ bản cuối im lặng)*.
    dem = Counter(n.ma for n in nut)
    for m, c in sorted(dem.items()):
        if c >= 2:
            loi.append((HD_MA_TRUNG, f"mã {m!r} xuất hiện {c} lần"))

    # `Đ3`: 0 nút ⇒ ⛔ có cây để kiểm *(⛔ "sạch trên tập rỗng")*.
    if not nut:
        loi.append((HD_HONG, "0 nút đọc được ⇒ ⛔ có cây để kiểm"))
        raise LoiHD(loi)

    co_ma = {n.ma for n in nut}
    theo_ma = {n.ma: n for n in nut}

    # `HD_CHA_VANG` — cha trỏ một mã ⛔ có trong ảnh.
    for n in nut:
        if n.cha is not None and n.cha not in co_ma:
            loi.append((HD_CHA_VANG,
                        f"nút {n.ma!r} trỏ cha {n.cha!r} ⛔ có trong ảnh"))

    # `HD_CHU_TRINH` — đi theo `cha` *(chỉ trong tập mã có)* gặp lại một nút đã thăm.
    #   ⛔ đếm chữ: mỗi chu trình báo MỘT lần, kèm vòng *(sắp để tất định)*.
    da_bao: set[frozenset[str]] = set()
    for n0 in nut:
        tham: list[str] = []
        cur: str | None = n0.ma
        # `len(tham) <= len(theo_ma)` = LƯỚI PHỤ *(`C4-R1-04`)*: một cây `k` nút đi theo
        #   `cha` ⛔ thể quá `k` bước mà chưa gặp lại nút. Nếu phép dò `cur in tham` lỡ
        #   hỏng, chặn này giữ vòng DỪNG thay vì phình tới khi OS `kill -9` *(OOM — ngốn
        #   bộ nhớ cả phiên pytest)*; cây đúng ⛔ bao giờ chạm chặn *(gặp lại trước)*.
        while cur is not None and cur in theo_ma and len(tham) <= len(theo_ma):
            if cur in tham:
                vong = tham[tham.index(cur):]
                khoa = frozenset(vong)
                if khoa not in da_bao:
                    da_bao.add(khoa)
                    loi.append((HD_CHU_TRINH, f"vòng {' → '.join(sorted(vong))}"))
                break
            tham.append(cur)
            cur = theo_ma[cur].cha

    # `HD_CAP_NHAY` — cấp = độ sâu: gốc phải cấp 1; con phải = cấp cha + 1.
    #   ⚠ Chỉ xét cạnh có cha TỒN TẠI *(cha vắng đã `HD_CHA_VANG`)*; nút trong chu
    #     trình cũng vào đây *(hai phép đo độc lập — xem docstring tệp)*.
    for n in nut:
        if n.cha is None:
            if n.cap != 1:
                loi.append((HD_CAP_NHAY,
                            f"gốc {n.ma!r} ở cấp {n.cap} ⛔ phải cấp 1"))
        elif n.cha in theo_ma:
            cap_cha = theo_ma[n.cha].cap
            if n.cap != cap_cha + 1:
                loi.append((HD_CAP_NHAY,
                            f"nút {n.ma!r} cấp {n.cap} dưới cha {n.cha!r} cấp "
                            f"{cap_cha} (lệch {n.cap - cap_cha}, ⛔ phải 1)"))

    if loi:
        raise LoiHD(loi)
    return CayHD(nguon=nguon, nut=tuple(sorted(nut, key=lambda n: n.thu_tu)))


def doc_van_ban(van_ban: str, *, nguon: str) -> CayHD:
    """Lõi đọc ẢNH ATL: VĂN BẢN JSON `{bang:'IX.HD', …, dong:[...]}` ⇒ `kiem`.

    JSON hỏng ⇒ `LoiHD(HD_HONG)` *(⛔ `JSONDecodeError` trơn — `C4-R1-01`)*.
    """
    try:
        tho = json.loads(van_ban)
    except json.JSONDecodeError as e:
        raise LoiHD([(HD_HONG, f"{nguon}: JSON hỏng — {_mot_dong(str(e))}")]) from None
    if not isinstance(tho, dict) or tho.get("bang") != BANG \
            or not isinstance(tho.get("dong"), list):
        raise LoiHD([(HD_HONG,
                      f"{nguon}: ⛔ phải {{bang: '{BANG}', dong: [...]}}")])
    return kiem(tho["dong"], nguon=nguon)


def doc_tep(duong: str = NGUON_TINH) -> CayHD:
    """Nạp ẢNH ATL *(tương đối gốc repo)* rồi `kiem`. `nguon` = chính `duong`.

    ⛔ `C1-R1-02`: CHỈ đọc tệp NGAY dưới `nguon_tinh.THU_MUC` *(luật đường một chỗ —
      ⛔ tuyệt đối, ⛔ `..`, ⛔ liên kết mềm ra ngoài)*. Đường hỏng ⇒ `LoiHD` một dòng.
    """
    try:
        p = nguon_tinh.giai(duong)
    except nguon_tinh.LoiNguonTinh as e:
        raise LoiHD([(HD_HONG, str(e))]) from None
    return doc_van_ban(p.read_text(encoding="utf-8"), nguon=duong)


def _ma_mm(hd_code: str) -> str:
    """Mã HD của một dòng Mapping Master: `'GI | Gross Inflow'` ⇒ `'GI'`.

    ⭐ Ảnh MM khoá bằng `hd_code` dạng `'MÃ | Tên'` *(đo DT3: 73/73 dòng có ` | `)*.
    """
    return hd_code.split("|", 1)[0].strip()


def doc_mm_van_ban(van_ban: str, *, nguon: str) -> tuple[str, ...]:
    """Lõi đọc ẢNH Mapping Master: VĂN BẢN JSON ⇒ **mã HD** *(theo thứ tự ảnh)*.

    ⭐ Song song `doc_van_ban` của ATL — tách lõi khỏi việc đọc tệp ⇒ bài thử nạp
      ảnh TỔNG HỢP cố ý hỏng *(mã trùng · 0 dòng · `hd_code` rỗng)* mà ⛔ chạm hệ tệp
      *(`C4-R1-02`: ba nhánh `raise` của `doc_mm` phải có bài ĐỎ — `Đ5`)*.
    JSON hỏng ⇒ `LoiHD(HD_HONG)` *(⛔ `JSONDecodeError` trơn — `C4-R1-01`)*. Mã
      trùng/rỗng/0 dòng ⇒ `LoiHD` *(`Đ3`: ⛔ so trên tập rỗng)*.
    """
    try:
        tho = json.loads(van_ban)
    except json.JSONDecodeError as e:
        raise LoiHD([(HD_HONG, f"{nguon}: JSON hỏng — {_mot_dong(str(e))}")]) from None
    if not isinstance(tho, dict) or tho.get("bang") != BANG_MM \
            or not isinstance(tho.get("dong"), list):
        raise LoiHD([(HD_HONG,
                      f"{nguon}: ⛔ phải {{bang: '{BANG_MM}', dong: [...]}}")])
    loi: list[tuple[str, str]] = []
    ma: list[str] = []
    for i, r in enumerate(tho["dong"], start=1):
        if not isinstance(r, Mapping):
            loi.append((HD_HONG, f"dòng {i}: ⛔ phải một đối tượng"))
            continue
        c, ly = _chu(r.get("hd_code"))
        if c is None or not c:
            loi.append((HD_HONG, f"dòng {i}: hd_code {ly or 'rỗng'}"))
            continue
        ma.append(_ma_mm(c))
    if not ma:
        loi.append((HD_HONG, f"{nguon}: 0 mã đọc được ⇒ ⛔ có gì để đối chiếu"))
    for m, n in sorted(Counter(ma).items()):
        if n >= 2:
            loi.append((HD_MA_TRUNG, f"Mapping Master: mã {m!r} xuất hiện {n} lần"))
    if loi:
        raise LoiHD(loi)
    return tuple(ma)


def doc_mm(duong: str = NGUON_MM) -> tuple[str, ...]:
    """Nạp ảnh Mapping Master *(tương đối gốc repo)*, trả **mã HD** *(⛔ COA/HR)*.

    ⭐ **Chỉ các mã, theo thứ tự ảnh** — `C4` DÙNG để LIỆT KÊ chênh với ATL, ⛔ hoà
      giải *(`74 ↔ 73`, `ATL − MM = {NCF}` — `BG-107`)*. Lõi: `doc_mm_van_ban`.
    """
    try:
        p = nguon_tinh.giai(duong)
    except nguon_tinh.LoiNguonTinh as e:
        raise LoiHD([(HD_HONG, str(e))]) from None
    return doc_mm_van_ban(p.read_text(encoding="utf-8"), nguon=duong)
