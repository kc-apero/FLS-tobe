# -*- coding: utf-8 -*-
"""Adapter `F04` — **60 sheet `R |` → khuôn `Bank Transactions`**.

⭐⭐ **Đây là thứ thay CÚ ĐẨY** *(`QĐ-ITL-100`)*. Hôm nay chuỗi chạy thế này:

    P100 ▸ R | (60 sheet, kế toán dán sao kê)
        │  `Run` thủ công  (OP-09)
    P100 ▸ Bank Transactions
        │  ⛔ CÚ ĐẨY tay/script  ← **đang trễ 19 ngày / 377 dòng**
    A-CCR ▸ Bank Transactions → 1.2 Ledger 112 → ITL RAW → ITL Ledge

FLS thay **đúng hai mũi tên trên**: đọc `R |`, dựng `Bank Transactions`. ⛔ Không
đụng `P100`, ⛔ không đụng một công thức hạ nguồn nào.

⭐⭐⭐ **Và nó ⛔ KHÔNG phát minh phép chuẩn hoá.** Kế toán **đã tự chuẩn hoá**:
   **dòng 1 của mỗi sheet `R |` là một BẢN KHAI ÁNH XẠ** *(`1`=Date · `2`=
   Description · `3`=Currency · `4`=Debit · `5`=Credit · `6`=Reference number)*,
   do người **duy trì bằng tay**, đo được **68/68 sheet khai đủ**. Adapter này
   **ĐỌC LẤY** bản khai — ⛔ **không** đoán theo vị trí cột. Đo trên kho
   08/09: **68 dòng chảy** mang **19 bố cục cột** khác nhau *(**16** nếu chỉ
   đếm **5 trường FLS thực đọc**)* ⇒ đoán là **sai tiền**.

⛔ **Cũng ⛔ không phát minh phép chống trùng.** Cột `Num` của AS-IS là **thứ tự
   lần xuất hiện của mã**, đo được khớp **8.331/8.331 = 100,0%**. Ta **giữ**
   đúng luật ấy *(`QĐ-ITL-97`)*.

── Ba đường, và tổng phải khớp *(luật của `adapters/bank.py`)* ─────────────
   `ra` · `rong` *(dòng không có ngày — đệm của trang tính)* · `loi`.
   `ThongKe.tong()` **phải bằng** số dòng vào; ⛔ không dòng nào rơi im lặng.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from fls.canon.o_loi import la_o_loi

# ⭐ **MỘT** bản khai cho cả hệ. `fls/kiem/nguon_song.py` và `tools/*` đều
#    phải import từ đây — ⛔ không ai được gõ lại danh sách này.
SAU_TRUONG: tuple[str, ...] = ("Date", "Description", "Currency",
                               "Debit", "Credit", "Reference number")

# Số ở dòng 1 ↔ tên trường. Đây là **quy ước của kế toán**, ⛔ không phải của ta.
SO_TRUONG: dict[str, str] = {"1": "Date", "2": "Description", "3": "Currency",
                             "4": "Debit", "5": "Credit",
                             "6": "Reference number",
                             # ⭐ Lằn QUỸ đánh số tiếp tới `15` (`QĐ-ITL-108`).
                             #    Ta nhận đúng **hai** số có giá trị nghiệp vụ;
                             #    `7` `9`…`14` ⛔ KHÔNG nhận — `9`…`14` là khối
                             #    nhân sự bị cấm (`QĐ-ITL-107`), `7` là `Note`.
                             "8": "Legal Entity", "15": "CDT"}

# Khuôn ra = **đúng 10 cột của `Bank Transactions`**, đúng thứ tự.
KHUON_RA: tuple[str, ...] = (
    "Transaction date", "Description", "Currency", "Debit", "Credit",
    "Reference number", "Source", "Num", "Check trùng", ",")

# Trường nào của bản khai đổ vào cột nào của khuôn ra.
_DO_VAO = {"Transaction date": "Date", "Description": "Description",
           "Currency": "Currency", "Debit": "Debit", "Credit": "Credit",
           "Reference number": "Reference number"}

# ⭐⭐⭐ **`QĐ-ITL-128` (2026-09-17) — MỞ LẠI `QĐ-ITL-92`: đọc CẢ 6/6 trường.**
#
# ⛔ `QĐ-ITL-92` cấm `Description` trên **hai chân**, và chỉ **một** còn đứng:
#
#   ⓐ *"trường duy nhất có thể mang thông tin cá nhân"* — ⭐ **VẪN ĐÚNG**,
#      và nay **đo được** *(58/60 sheet `R |`, 7.712 ô có chữ)*:
#          tên NGƯỜI (có thể)  367 = **4,8%**   ⚠ SÀN DƯỚI
#          tên doanh nghiệp    401 = 5,2%
#          số điện thoại       180 = 2,3%
#          dạng số giấy tờ     735 = 9,5%       ⚠ TRẦN TRÊN — số tài khoản
#                                                cũng 9/12 chữ số
#          email                 4 = 0,1%
#   ⓑ *"⛔ không phép đo nào của `F04` cần nó"* — ⛔ **ĐÃ ĐỔI**: `F04` (màn
#      NẠP) vẫn ⛔ không cần, ⛔ nhưng **màn GHÉP cần**, và `US-KT-037` cần.
#      Đo được: **1.776 = 23,0%** ô mang mã `PI…`/`PE…`/`PM…` — tín hiệu
#      ghép **gấp ~4,8 lần** tỉ lệ tên người.
#
# ⛔⛔ **Owner chọn hình RỘNG NHẤT: nạp cả chuỗi, ⛔ không siết thêm** (17/09),
#    sau khi được nêu rõ rằng nó **đi ngược tiền lệ `QĐ-ITL-107`** — chỗ ấy
#    owner đã chọn **rộng hơn phép đo** khi dính dữ liệu người. Ghi ra ở đây
#    để người sau đọc được **cả quyết định lẫn cái đã được cân nhắc**.
#
# ⚠ **Hệ quả phải biết:** `sao_luu/` từ nay chứa tên người ⇒ dòng `gitignore`
#    của nó trở nên **quan trọng hơn trước**, ⛔ đừng gỡ.
#
# ⇒ Khai ở **đây**, cạnh `SAU_TRUONG`, để mọi công cụ **import** chứ ⛔ không
#   gõ lại — bài `test_CHI_MOT_BAN_KHAI_ANH_XA_trong_ca_he` đã bắt được **ba**
#   bản sao của đúng danh sách này trong một phiên.
TRUONG_DOC_DUOC: tuple[str, ...] = SAU_TRUONG

# ⭐ Tên trường NGÀY — khai **MỘT** lần ở đây *(`QĐ-ITL-113`)*.
#
# ⛔ Trước đó chuỗi `"Date"` bị gõ tay ở **ba** chỗ *(`repo.khai_cot`,
#   `repo.chup`, và đây)*. Ba bản là ba chỗ để chúng trôi khỏi nhau, và cái
#   trôi ở đây ⛔ không nổ — nó chỉ làm phép đo bằng chứng **đếm 0 dòng** rồi
#   báo *"⛔ không cần khai"* cho một nguồn có 905 dòng mơ hồ.
#
# ⛔ Suy từ `SAU_TRUONG` chứ ⛔ không viết lại: đổi tên trường ở một chỗ thì
#   hằng này **NỔ ngay lúc nạp module**, ⛔ không lặng lẽ trỏ vào hư không.
TRUONG_NGAY: str = SAU_TRUONG[0]
assert TRUONG_NGAY == "Date", TRUONG_NGAY

# ⛔⛔ **MẪU TRƯỜNG CẤM ĐỌC — mở rộng `QĐ-ITL-92` sau phép đo 2026-09-08.**
#    `QĐ-ITL-92` chỉ loại `Description`, vì lúc viết nó ⛔ **chưa ai đo lằn
#    QUỸ**. Đo sống cả 68 sheet ngày 08/09: **3/8** sheet quỹ mang cột **dữ
#    liệu cá nhân**, và bản khai của kế toán bên ấy đánh số tới **15** trường
#    *(`R | VND_HotBonus` khai `1`…`15`)* — trong đó:
#
#        10 = `ID Employee I ID Name`   11 = `Họ và tên (*)`
#        12 = `Số CMND/CCCD/Passport (*)`
#
#    ⇒ Ai mở `SAU_TRUONG` từ 6 lên 15 **một cách máy móc** sẽ kéo số căn cước
#      vào kho. Hôm nay `_soi_khai` chặn được vì nó là **danh sách TRẮNG** —
#      nhưng danh sách trắng chỉ bảo vệ được **chừng nào ⛔ chưa ai nới nó**,
#      và nới nó là việc **hoàn toàn hợp lý** sẽ có người làm: trường `8` =
#      `Legal Entity` và `15` = `CDT` là hai thứ **thật sự đáng lấy** *(lằn
#      bank phải chờ ghép PM mới có, tỷ lệ ghép gần kịch trần 33,8%)*.
#
#    ⇒ Nên phép canh đặt ở **TỪ VỰNG**, ⛔ không ở dữ liệu: bài
#      `test_tu_vung_doc_duoc_KHONG_duoc_chua_truong_CAM` đỏ **ngay giây** ai
#      thêm một tên chạm mẫu này vào `SAU_TRUONG` — ⛔ không đợi tới lúc đã
#      có dữ liệu cá nhân nằm trong kho, vì lúc ấy thì đã muộn.
#    ⭐⭐ **Owner chốt 2026-09-08 (`QĐ-ITL-107`): cấm CẢ KHỐI NHÂN SỰ `9`…`14`**,
#    ⛔ không chỉ ba cột đã đo. Lý do owner chọn rộng hơn phép đo — và nó đúng:
#    hai trường **thật sự đáng lấy** là `8` `Legal Entity` và `15` `CDT`, mà
#    chúng nằm **NGOÀI** khối ấy *(đo 08/09: `LE` ở cột `H`, khối nhân sự
#    `I`…`N`, `CDT` ở `O` — **liền mạch**)*. ⇒ Cấm cả khối **⛔ không mất gì**,
#    và bỏ được mọi lần phải phân vân từng cột khi có sheet mới.
RE_TRUONG_CAM = re.compile(
    # giấy tờ tuỳ thân
    r"CMND|CCCD|Passport|C[ăa]n\s*c[ưu][ơo]c"
    # họ tên + mã/tên nhân viên  (trường 10 · 11)
    r"|H[oọ]\s+v[àa]\s+t[êe]n|ID\s*Employee|ID\s*Name"
    # chức danh · ngạch  (trường 13 · 14)
    r"|Ch[ứu]c\s*danh|EmpTrack|Ng[ạa]ch",
    re.I)


def truong_cam_doc(ten: str) -> bool:
    """⛔ Tên trường này có mang **dữ liệu cá nhân** ⛔ không?"""
    return bool(RE_TRUONG_CAM.search(str(ten)))


# ⭐⭐ **Hai trường THÊM của lằn QUỸ — owner chốt 08/09 (`QĐ-ITL-108`).**
#    Kế toán quỹ **gõ sẵn** pháp nhân và chủ dự toán **ngay tại sheet nguồn**;
#    lằn bank phải **chờ ghép PM** mới có, mà tỷ lệ ghép gần kịch trần
#    **33,8%**. ⇒ Bỏ chúng đi là **vứt một phân loại đã có sẵn**.
#
# ⛔ **TUỲ CHỌN, ⛔ không bắt buộc** — và đó ⛔ không phải sự dễ dãi: đo 08/09
#    thì **chỉ 3/8** sheet quỹ **có** hai cột này, và **0/60** bên bank. Bắt
#    buộc chúng là làm 65 nguồn ⛔ không nạp được.
TRUONG_THEM_QUY: tuple[str, ...] = ("Legal Entity", "CDT")

# ⛔ **Từ vựng ĐẦY ĐỦ** = 6 bắt buộc + 2 tuỳ chọn. `SAU_TRUONG` giữ nguyên
#    nghĩa *"đủ mới cho đi tiếp"*; ⛔ đừng gộp hai khái niệm vào một hằng.
TRUONG_HOP_LE: tuple[str, ...] = SAU_TRUONG + TRUONG_THEM_QUY

# ⭐⭐⭐ **CÁCH ĐỌC MỘT DÒNG ẢNH CHỤP** *(`QĐ-ITL-110`, `CR#11` task `9`)*.
#
# Ảnh chụp giữ ô theo **TÊN TRƯỜNG** *(`{"Date": 45586, …}`)*, còn `chuyen()`
# đọc theo **VỊ TRÍ**. ⇒ Cần một bản khai để đi từ tên sang vị trí — và nó
# phải nằm **ở đây**, cạnh `SAU_TRUONG`/`TRUONG_DOC_DUOC`, ⛔ không ở
# `fls/repo/chup.py`.
#
# ⛔⛔ **Vì sao chỗ ở quan trọng hơn nó trông.** Bài
#    `test_CHI_MOT_BAN_KHAI_ANH_XA_trong_ca_he` đã bắt được **ba** bản sao của
#    đúng danh sách này trong **một phiên**. Một bản khai thứ hai đặt ở tầng
#    kho là một chỗ để nó **lệch trong im lặng** với bản ở đây — và cái lệch
#    ấy là **lệch CỘT**, tức **sai tiền**.
#
# ⭐ Đây ⛔ **KHÔNG** phải bản khai thứ hai của một *nguồn*. Bản khai của nguồn
#   đã được **áp xong** lúc chụp *(`fls_chup_nguon.khai_version` ghim lại)*;
#   cái dưới đây chỉ tả **bố cục của chính ảnh chụp**, và nó **cố định**.
#
# ⚠ `Description` có mặt trong bản khai này **với một ô LUÔN RỖNG**, ⛔ không
#   bị bỏ ra. Lý do: `kiem_ban_khai` đòi **đủ 6 trường** *(và luật ấy đúng —
#   thiếu một trường là mất cột trong im lặng)*, mà `QĐ-ITL-92` thì cấm **ĐỌC**
#   nó. Hai luật ⛔ không xung đột: trường **được khai**, giá trị **⛔ không bao
#   giờ được lấy**. Đó cũng đúng cái đường nạp thật đang làm hôm nay.
# ⭐ Tu `QĐ-ITL-128`, `TRUONG_DOC_DUOC == SAU_TRUONG` nen ban khai nay chi
#   con MOT nguon — ⛔ khong con o `Description` dat rieng o cuoi.
KHAI_ANH_CHUP: dict[str, int] = {t: i for i, t in enumerate(TRUONG_DOC_DUOC)}


def hang_tu_o(o: Mapping[str, Any]) -> list[Any]:
    """Một ô-theo-tên của ảnh chụp → **một dòng theo VỊ TRÍ** cho `chuyen()`.

    ⛔ **Trường lạ thì NỔ, ⛔ không bỏ qua** — cùng lý do `_soi_khai`: bỏ qua
      một tên lạ là biến **một lỗi gõ** thành **một trường thiếu**, và người ta
      sẽ đi sửa **nhầm chỗ**.

    ⛔ Ô của `Description` **luôn rỗng** *(`QĐ-ITL-92`)*. Nếu ảnh chụp lại
      **có** khoá ấy thì đó là một ảnh chụp đã đọc thứ ⛔ không được đọc ⇒ **NỔ**,
      ⛔ không lặng lẽ ném đi: ném đi thì dữ liệu cá nhân **đã vào kho rồi** và
      ⛔ không ai biết.
    """
    la = sorted(set(o) - set(TRUONG_DOC_DUOC))
    if la:
        raise BanKhaiHong(
            "⛔ ô ảnh chụp có trường ⛔ KHÔNG được phép: %s. Cho phép: %s"
            " · `Description` bị cấm bởi `QĐ-ITL-92`"
            % (la, list(TRUONG_DOC_DUOC)))
    hang: list[Any] = [""] * len(TRUONG_DOC_DUOC)
    for t, i in KHAI_ANH_CHUP.items():
        hang[i] = o.get(t, "")
    return hang


# Chỉ số cột trong `KHUON_RA` — khai **MỘT** lần ở đây, ⛔ không tra lại
# bằng chuỗi ở nơi khác.
I_NGAY, I_MOTA, I_TE, I_NO, I_CO, I_MA, I_XUAT_XU, I_NUM = (
    KHUON_RA.index(c) for c in (
        "Transaction date", "Description", "Currency", "Debit", "Credit",
        "Reference number", "Source", "Num"))


class BanKhaiHong(RuntimeError):
    """⛔ Sheet ⛔ không khai đủ 6 trường thì **NỔ TO**.

    ⛔ Không được đoán theo vị trí cột. Đo trên kho 08/09: **68 dòng chảy**
    mang **19 bố cục cột** khác nhau — **16** nếu chỉ đếm **5 trường FLS
    thực đọc**. ⇒ Đoán ⛔ không phải là *"kém chính xác"* — nó là **sai
    tiền**.

    ⚠ Bản trước ghi *"**9** bố trí"*. Con số `9` **đúng**, nhưng nó chỉ
    nhìn **3/6 trường** *(`Date`·`Debit`·`Credit` — `tools/do_hinh_dang.py`)*
    trong khi câu chữ nói *"bố trí **cột**"*. Một **con số đúng nằm trong
    một câu sai** đi lọt qua **66 phép so**, vì cổng canh **CON SỐ** chứ
    ⛔ không canh **NGHĨA**. Nay ba con số ấy **ở trong cổng**.
    """


@dataclass(frozen=True)
class ThongKe:
    vao: int
    ra: int
    rong: int
    loi: int

    def tong(self) -> int:
        return self.ra + self.rong + self.loi


def doc_ban_khai(dong1: Sequence[Any]) -> dict[str, int]:
    """Dòng 1 → `{tên trường: chỉ số cột}`. ⛔ Rỗng nếu sheet ⛔ không khai."""
    ra: dict[str, int] = {}
    for i, o in enumerate(dong1):
        s = str(o).strip()
        # `5.00` cũng là `5` — một sheet OCBC ghi kiểu số thực
        if s.endswith(".00"):
            s = s[:-3]
        if s in SO_TRUONG:
            ra[SO_TRUONG[s]] = i
    return ra


def kiem_ban_khai(ten_sheet: str, khai: dict[str, int],
                  *, cho: str = "dòng 1") -> None:
    """⛔ Thiếu một trong 6 trường thì **NỔ TO**, ⛔ không nạp một phần.

    ⭐ `cho` = **bản khai ấy nằm ở đâu**. Từ `CR#11` bản khai có **hai chỗ ở**
      *(dòng 1 của sheet, và bảng `fls_khai_cot`)*, mà phép kiểm thì phải chỉ
      có **MỘT** — nên chỗ ở là **tham số**, ⛔ không phải lý do để viết một
      bản kiểm thứ hai. ⛔ Câu *"thiếu ở dòng 1"* nói với người đang đọc từ
      **kho** sẽ chỉ họ đi sửa **nhầm chỗ**.
    """
    thieu = sorted(set(SAU_TRUONG) - set(khai))
    if thieu:
        raise BanKhaiHong(
            "%s: bản khai (%s) thiếu %s. ⛔ Không đoán theo vị trí cột — "
            "đo trên kho 08/09: 68 dòng chảy · 19 bố cục cột."
            % (ten_sheet, cho, thieu))


def chuyen(ten_sheet: str, khai: Mapping[str, int],
           cac_dong: Iterable[Sequence[Any]],
           dem_ma: Counter | None = None) -> tuple[list[list], ThongKe]:
    """Một sheet `R |` → các dòng theo `KHUON_RA`.

    ⭐⭐ **`khai` là BẢN KHAI ĐƯA VÀO, ⛔ không phải dòng 1** *(`CR#11` task
      `3`, 08/09)*. Trước đó hàm này tự gọi `doc_ban_khai(dong1)` — tức nó
      **tự quyết định bản khai đến từ đâu**, và chỗ ấy là **sheet**.

      ⛔ Nay bản khai có **hai chỗ ở** *(dòng 1 · bảng `fls_khai_cot`)*, và
      `QĐ-ITL-105` bỏ Google Sheets khỏi đường nạp ⇒ nếu hàm này còn tự đọc
      dòng 1 thì **⛔ không có đường nào cắt được dây sang Sheets**. Mà tầng
      `adapters` thì ⛔ **không được biết tầng kho** *(`lint-imports` hợp đồng
      1: cấm `psycopg`)* — nên nó ⛔ **không thể** tự đọc kho.

      ⇒ Lời giải đúng ⛔ không phải *"đọc chỗ khác"* mà là **THÔI QUYẾT ĐỊNH**:
        hàm **nhận** bản khai, người gọi chọn nguồn. Adapter ⛔ không còn biết
        — và ⛔ không cần biết — bản khai đến từ sheet hay từ kho.

    `dem_ma` đi **xuyên nhiều sheet** để `Num` đếm đúng *(mã có thể lặp giữa
    các tài khoản)*. Người gọi truyền **cùng một** `Counter` cho cả 60 sheet.

    ⛔ Adapter này **⛔ KHÔNG làm sạch giá trị** — cùng lý do với
    `adapters/bank.py`: mọi phép làm sạch ở đây là một chỗ đối soát có thể đỏ
    vì **lỗi của ta**, ⛔ không phải lỗi của sổ.
    """
    # ⛔ VẪN kiểm, dù người gọi có thể đã kiểm. Một hàm tin vào người gọi của
    #    nó là một hàm ⛔ không có hàng rào — và cái thiếu có thể là cột TIỀN.
    khai = dict(khai)
    kiem_ban_khai(ten_sheet, khai, cho="bản khai đưa vào")
    dem = Counter() if dem_ma is None else dem_ma

    ra: list[list] = []
    vao = rong = loi = 0
    for hang in cac_dong:
        vao += 1

        def o(truong: str, hang=hang) -> Any:
            i = khai[truong]
            return hang[i] if i < len(hang) else ""

        ngay = o("Date")
        if str(ngay).strip() == "":
            rong += 1                       # đệm của trang tính, ⛔ không phải dòng
            continue
        if la_o_loi(ngay) or la_o_loi(o("Reference number")):
            loi += 1                        # `#REF!`/`#N/A` — ⛔ không nuốt
            continue

        ma = str(o("Reference number")).strip()
        dem[ma] += 1
        dong = [o(_DO_VAO[c]) if c in _DO_VAO else "" for c in KHUON_RA]
        dong[KHUON_RA.index("Source")] = ten_sheet
        dong[KHUON_RA.index("Num")] = dem[ma]   # ⭐ luật `Num` của AS-IS
        ra.append(dong)

    return ra, ThongKe(vao=vao, ra=len(ra), rong=rong, loi=loi)
