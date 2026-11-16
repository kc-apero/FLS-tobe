"""`CA.GL` thuần — dòng sổ cái → Nợ/Có tách theo 5 tiền tệ · tồn luỹ kế · 8 cột CALC ZONE BM–BT.

ISP 3.1.2 **Step 1 · H1** *(`WO-070`)* · AP v3.1.2 §3.3.1 hàng PD `406 · 412` · §3.5.4 `WP-C2`.
Vòng sửa sau R1 *(`KQ-072`, orchestrator 16/11)*: thêm BM · BN · BQ · BT *(`H1-R1-05`)*, so tiền
tệ qua `ma_tien_te` *(`H1-R1-01`)*, chặn số ⛔ hữu hạn *(`H1-R1-02`)*, lời tả AS-IS theo CÔNG
THỨC Ô *(`H1-R1-04`)*.

── Công thức NOW, chép NGUYÊN VĂN *(AP §3.3.1, cột "PD NOW · script · công thức")* ──────────

    A10 = QUERY(ITL Ledge); tách Nợ/Có theo 5 tiền tệ; tồn = tồn trên + Nợ − Có;
    BO/BP = tỷ giá × E|F / 10^9 (bVND); BR/BS = BO|BP ÷ USD × 10^3 (mUSD);
    CA = VLOOKUP(TK, Mapping Master AB→AD)

    cột conflict cùng hàng: "tồn luỹ kế theo thứ tự dòng của cả bảng, ⛔ theo TK ⇒ phụ thuộc
    sort; tỷ giá theo tháng"
    hàng PD 405: "9.2.Exchange Rate = IMPORTRANGE APERO | FS2; tra bằng SUMIFS(tháng) và
    INDEX(MATCH tháng; MATCH tiền tệ)" — conflict: "bảng đứng yên từ 07/2025; tháng thiếu ⇒
    mất số"

── Công thức Ô NOW *(`docs/ITL/01_Orchestrator/isp-3.1/CALC_ZONE_406.md` — orchestrator đọc
   16/11 bằng connector, CHỈ công thức, sheet `Report I General Ledger` hàng 10–11; tệp nằm ở
   nhánh chính @ `1768668`, ⛔ có trong `isp/H1`)* ─────────────────────────────────────────

    AX = if($D10=AX$9,$E10,"") · AY = if($D10=AY$9,$F10,"") · AZ10 = AX10-AY10
    AZ11 = AZ10+AX11-AY11                       (cùng khuôn BA:BC SGD · BD:BF COP · BG:BI VND
                                                 · BJ:BL HKD — tồn LUỸ KẾ, nguyên tệ)
    BM = AZ*SUMIFS(9.2!B,9.2!H,tháng) + BC*SUMIFS(…C…) + BF*SUMIFS(…D…) + BI + BL*SUMIFS(…F…)
    BN = (AZ + BC*SGD/USD + BF*COP/USD + BI/USD + BL*HKD/USD)/10^6     (mọi tỷ giá qua SUMIFS)
    BO|BP = iferror(INDEX('9.2'!$A$1:$H, MATCH(tháng, '9.2'!$H$1:$H, 0),
                          MATCH(D10, '9.2'!$A$1:$H$1, 0)) * E10|F10 / 10^9)
    BQ10 = BO10-BP10 · BQ11 = BQ10+BO11-BP11
    BR|BS = iferror(BO10|BP10 / SUMIFS('9.2'!$B:$B, '9.2'!$H:$H, tháng) * 10^3)
    BT10 = BR10-BS10 · BT11 = BT10+BR11-BS11

Ánh xạ 8 cột CALC ZONE → trường của `KetQuaDongGL` *(E|F = Nợ|Có nguyên tệ của dòng; AZ · BC ·
BF · BI · BL = `ton[USD|SGD|COP|VND|HKD]`)*:

    BM = Σ tồn × tỷ giá tháng dòng   → vnd_ton_all     BQ = BQ trên + BO − BP → bvnd_ton
    BN = BM ÷ USD ÷ 10^6             → musd_ton_all    BR = BO ÷ USD × 10^3   → musd_no
    BO = tỷ giá × E / 10^9           → bvnd_no         BS = BP ÷ USD × 10^3   → musd_co
    BP = tỷ giá × F / 10^9           → bvnd_co         BT = BT trên + BR − BS → musd_ton

⭐ **Đơn vị** *(Đ4 — mỗi số nói nó đếm gì)*: `tỷ giá` = số VND cho MỘT đơn vị tiền tệ của dòng
*(`IX.FX`: VND = 1)* · **BM** = **VND** *(⛔ chia 10^9 — tiêu đề hàng 9 của ô ghi "VND")* ·
**bVND** = tỷ VND *(÷ 10^9)* · **mUSD** = triệu USD *(tỷ VND ÷ VND/USD = tỷ USD; × 10^3 = triệu
USD — BN cùng đơn vị: USD ÷ 10^6)*. ⛔⛔ ISP `H1-B1` ghi mong *"mUSD 98,039…"* cho dòng VND
2.500.000.000 @ 25.500 — **sai đơn vị**: chính công thức trên cho `2,5 ÷ 25.500 × 10^3 =
0,098039…` mUSD; `98,039…` là cùng giá trị đo bằng **nghìn** USD *(orchestrator đính chính
16/11, `BG-071`)*. Mã theo CÔNG THỨC AP; bài `test_H1_B1_…` canh riêng đơn vị.

⭐ **BN = BM ÷ USD ÷ 10^6** — đại số BẰNG khuôn ô *(chia phân phối: `(AZ×USD + BC×SGD + … + BI
+ …) / USD = AZ + BC×SGD/USD + … + BI/USD + …`)*, nhưng chỉ **MỘT** lần làm tròn *(÷ USD; ÷ 10^6
chỉ dời số mũ)* thay vì bốn. BM cộng các tích ĐÚNG tuyệt đối *(tiền `numeric(20,2)` × tỷ giá ≤
7 chữ số ⇒ ≤ 27 chữ số < 28)* ⇒ BN là giá trị đúng làm tròn một lần — bài `test_R1_07_…` ghim.

── Ba hành vi AS-IS được GIỮ có chủ ý *(parity trước — D2; H4 so với đáp án 406)* ───────────

① **Tồn luỹ kế theo THỨ TỰ dòng đưa vào, ⛔ theo TK.** *"tồn = tồn trên + Nợ − Có"* cộng dồn
  từ trên xuống cả bảng ⇒ đổi thứ tự dòng là đổi tồn giữa bảng *(tồn cuối thì ⛔ đổi)*. Đó là
  conflict AP đã ghi *("phụ thuộc sort")*; đích TO-BE *"tồn theo (TK, ngày)"* là việc SAU
  parity, ⛔ của H1. `DongGL` ⛔ mang TK ⇒ hàm này **⛔ thể** gộp theo TK, bằng cấu trúc.
  Tồn tính **theo từng tiền tệ, bằng nguyên tệ** — `CALC_ZONE_406.md` xác nhận bằng công thức
  ô *(`AZ11 = AZ10+AX11-AY11`, cùng khuôn BC · BF · BI · BL — trả lời câu Q1 của `BG-071`)*.
  BQ · BT cũng luỹ kế theo thứ tự dòng, cộng **mọi** tiền tệ đã quy đổi theo tỷ giá LỊCH SỬ
  của từng dòng; BM · BN thì **đánh giá lại** toàn bộ tồn theo tỷ giá tháng của dòng đang xét
  ⇒ trong MỘT tháng `BM = BQ × 10^9`, sang tháng mới hai cột tách nhau *(bài 6 dòng, dòng 4)*.
  ⚠ Số của ô **chưa đối chiếu với đáp án thật** — H4 là phép đo quyết định.
② **Tỷ giá theo THÁNG của dòng — BA ngữ nghĩa tra trên cùng một hàng** *(⛔ một —
  `CALC_ZONE_406.md` "Hai NGỮ NGHĨA tra tỷ giá"; câu tóm tắt PD 405 gộp chúng làm một)*:
  · BO/BP: `INDEX/MATCH(tháng, tiền tệ của dòng)` *(khớp ĐẦU)* ⇒ `fx[thang][tien_te]` — dòng
    VND cũng tra cột VND của bảng;
  · BR/BS: `SUMIFS(cột USD, tháng)` ⇒ `fx[thang]["USD"]` — dòng VND cũng cần USD cùng tháng;
  · BM/BN: `SUMIFS` từng cột USD · SGD · COP · HKD theo tháng của dòng; **VND ⛔ tra** *(ô
    viết `… + BI + …` và `BI/USD`: VND là ĐƠN VỊ của BM, hệ số 1 là định nghĩa đơn vị, ⛔ một
    tỷ giá gõ cứng)*. Chỉ tiền tệ có tồn ≠ 0 mới cần tỷ giá: số hạng tồn 0 bằng 0 bất kể tỷ giá
    *(AS-IS `0 × 0 = 0` cũng ⛔ mất số)*.
③ **5 cột tiền tệ** `USD · SGD · COP · VND · HKD` — đúng thứ tự `IX.FX` *(AP §3.2.1: "tháng
  yyyymm × USD · SGD · COP · VND (=1) · HKD", 37 dòng 202401 → 202612 kể cả dòng lạc
  202306)*. `TIEN_TE_GL` là **khuôn cột của GL**, ⛔ phải luật số: ⛔ một tỷ giá nào gõ
  trong mã — kể cả VND = 1 — mọi tỷ giá đến từ tham số `fx` *(AP AC9: engine đọc config,
  ⛔ gõ lại)*.

── Bốn chỗ **⛔ giữ** lỗi AS-IS — đây là lý do engine tồn tại *(`INV-I16` · D1 CHẶN)* ────────

ⓐ **Tỷ giá thiếu ⇒ `ThieuTyGia`, ⛔ ra 0, ⛔ ô rỗng.** AS-IS trên tháng VẮNG *(bảng tỷ giá
  *"đứng yên từ 07/2025"*)*: BO · BP *(INDEX/MATCH)* và BR · BS *(÷ SUMIFS = 0)* bọc `iferror`
  ⇒ ô **RỖNG**; **BM** nhân với `SUMIFS = 0` ⇒ **mất số IM LẶNG**; BN chia 0 ⇒ `#DIV/0!`.
  Tháng có mặt mà ô tỷ giá TRỐNG ⇒ INDEX trả rỗng ⇒ BO/BP = **0** im lặng *(suy từ công thức ô,
  ⛔ đo trên giá trị)* ⇒ tỷ giá ≤ 0 cũng là THIẾU. Tháng TRÙNG ⇒ INDEX lấy dòng đầu, SUMIFS
  **cộng đôi** — `fx` là `dict` theo tháng nên ⛔ trùng tháng được *(một dòng/tháng là việc của
  C1)*; trùng KHOÁ tiền tệ sau `ma_tien_te` *(`'USD'` + `'usd'`)* ⇒ `ThieuTyGia` "mơ hồ" *(Đ5:
  khớp ≥ 2 lần là ⛔ đo được)*. Lỗi ném cho CẢ lượt *(⛔ trả nửa bảng)*: một GL có lỗ thủng mà
  vẫn in được thì ⛔ ai thấy lỗ. Khi so với đáp án *(H4)*, ô AS-IS rỗng / 0 / `#DIV/0!` do tháng
  thiếu là **lệch CÓ TÊN** — ⛔ đếm là lỗi FLS, ⛔ đếm là khớp.
ⓑ **Tiền tệ ngoài 5 cột ⇒ `TienTeNgoaiGL`.** Dòng EUR ⛔ có cột để vào: bỏ qua là mất tiền
  khỏi GL, dồn vào cột khác là bịa — cả hai đều im lặng.
ⓒ **Tiền ⛔ hữu hạn ⇒ `TienKhongHuuHan`; tỷ giá ⛔ hữu hạn ⇒ `ThieuTyGia`.** `Decimal` NaN /
  ±Infinity ⛔ là tiền: tồn LUỸ KẾ ⇒ một NaN đầu độc **mọi dòng sau** cùng tiền tệ, cả BQ/BT/BM.
  Đường vào có thật: `fls_itl.ps_no`/`ps_co` là `numeric(20,2)` ⛔ CHECK *(`0001_baseline.sql`)*,
  PG nhận `'NaN'` *(`KQ-072` F-2)*.
ⓓ **So tiền tệ qua `fls.canon.tien_te.ma_tien_te`** *(`BA-07` §4g v3.11: "**mọi** phép so tiền
  tệ trong `fls/` gọi `ma_tien_te`"; GL gom theo tiền tệ ra số in = lớp ⓑ "áp" của v3.12)*: kiểm
  5 cột · khoá tồn · tách cột · khoá tra `fx` — cả BỐN chỗ đọc CÙNG một mã chuẩn hoá. Trước vòng
  sửa, `'vnd'` · `' VND'` · `'VND'`+NBSP · BOM+`'VND'` ⇒ `TienTeNgoaiGL` *(R1 đo 4/4)* trong khi
  rổ, bậc tiền và cửa ghi coi là `VND` — **hai luật** cho một mã. ⚠ Sheets so `$D10=AX$9`
  ⛔ phân biệt hoa/thường nhưng ⛔ gỡ ký tự trắng ⇒ AS-IS đưa `'vnd'` vào cột VND còn `' VND'` thì
  rơi khỏi cả 5 cột *(suy từ công thức ô)* — FLS đưa cả hai vào VND *(sổ thật `curr` lệch khuôn
  **0 / 8.387**, `07_API_CONTRACT.md` §4g ⇒ hôm nay ⛔ ô nào đổi)*.

── Hàm THUẦN *(`.importlinter` hợp đồng 11 — cấm `psycopg` · `fls.repo` · `fls.db`)* ─────────

Dòng và tỷ giá được **TRUYỀN VÀO**; ⛔ đọc kho, ⛔ đọc biến môi trường. Cùng đầu vào ⇒ cùng
con số — kể cả khi người gọi đổi độ chính xác `Decimal` toàn cục: phép tính chạy trong ngữ
cảnh CỐ ĐỊNH `_NGU_CANH` *(28 chữ số có nghĩa, làm tròn nửa-về-chẵn = mặc định Python — bài
`test_R1_07_…` ghim cả hai bằng so đúng tuyệt đối ở chữ số 28 và ca hoà ở chữ số 29)*.
⛔ float cho tiền/tỷ giá *(`TypeError`)* — bên nạp JSON phải `parse_float=Decimal`
*(tỷ giá thật có lẻ: SGD 202507 = `20691.51` — `TIEN_DO.md` thăm dò O7)*. `fls.canon` là tầng
dưới cùng *(hợp đồng 3: ⛔ phụ thuộc gì)* ⇒ import nó ⛔ kéo kho; bài `test_R1_06_…` đo cả
đường import ĐỘNG mà `lint-imports` ⛔ thấy.

⚠ Sheets tính bằng số thực IEEE-754 *(~15–17 chữ số có nghĩa)*, mã này 28 ⇒ ô mUSD vô hạn
tuần hoàn *(vd. 2,5 ÷ 25.500)* lệch nhau ở chữ số thứ ~16 — H4 phải khai dung sai khi so
với đáp án 406, ⛔ đòi bằng tuyệt đối. BN tính một lần làm tròn *(trên)* còn ô Sheets chia
từng số hạng ⇒ thêm một lý do cho dung sai ấy.

Trước H1, grep `musd|bvnd|ty_gia` ở `fls/` + `tools/` = **2 dòng, cả hai là docstring**
`fls/bao_cao/__init__.py` ⇒ **0 dòng mã** quy đổi tỷ giá *(khớp ISP §1.3 đo 16/11)*.

⛔ Ngoài H1: dữ liệu thật + parity 406 *(H4 — so `BM … BT` theo dòng × kỳ, khai dung sai)* ·
dòng HR 407/408 *(H7)* · cột `CA` Cash/Bank qua `IX.ORG` *(C8)* · đọc `IX.FX` từ kho *(C5 — đến
đây vẫn qua tham số)*. Cả **8** cột BM–BT đã dựng ở đây *(quyết định orchestrator 16/11 sau R1,
`H1-R1-05`: cùng khái niệm "engine quy đổi GL + tồn luỹ kế" của H1)* ⇒ H4 chỉ còn SO.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from typing import Iterable, Mapping

from fls.canon.tien_te import ma_tien_te

# Khuôn cột tiền tệ của GL — đúng thứ tự `IX.FX` (AP §3.2.1). ⛔ chứa tỷ giá.
TIEN_TE_GL: tuple[str, ...] = ("USD", "SGD", "COP", "VND", "HKD")

# Đơn vị của BM (tiêu đề hàng 9 của ô: "VND"). Tồn VND cộng THẲNG vào BM (ô `… + BI + …`);
# 4 tiền tệ còn lại nhân tỷ giá tháng của dòng — ⛔ tỷ giá nào gõ ở đây.
_DON_VI_BM = "VND"
_DANH_GIA_LAI: tuple[str, ...] = tuple(t for t in TIEN_TE_GL if t != _DON_VI_BM)

_MOT_TY = Decimal(10) ** 9        # 10^9 : VND → bVND        (BO/BP "… / 10^9")
_MOT_NGHIN = Decimal(10) ** 3     # 10^3 : tỷ USD → mUSD      (BR/BS "… × 10^3")
_MOT_TRIEU = Decimal(10) ** 6     # 10^6 : USD → mUSD         (BN "(…)/10^6")
_KHONG = Decimal(0)

# Ngữ cảnh CỐ ĐỊNH ⇒ kết quả ⛔ phụ thuộc `getcontext()` của người gọi
# (bài `test_ket_qua_khong_phu_thuoc_ngu_canh_Decimal_cua_nguoi_goi`: prec = 5 ⇒ y nguyên;
#  bài `test_R1_07_…`: prec 12 · ROUND_DOWN · ROUND_HALF_UP · ROUND_HALF_DOWN đều ĐỎ).
_NGU_CANH = Context(prec=28, rounding=ROUND_HALF_EVEN)


class ThieuTyGia(LookupError):
    """Tháng/tiền tệ ⛔ có MỘT tỷ giá DƯƠNG, HỮU HẠN dùng được. ⛔ Quy đổi ra 0 — `INV-I16`.

    Năm cách thiếu: vắng tháng · vắng cột · tỷ giá ≤ 0 · ⛔ hữu hạn · **mơ hồ** *(≥ 2 khoá cùng
    chuẩn hoá về một mã)*. Mang `thang` · `tien_te` *(mã ĐÃ chuẩn hoá — tiền tệ THIẾU, có thể
    khác tiền tệ của dòng khi BM cần đánh giá lại tồn)* · `vi_tri` *(vị trí dòng trong dãy đưa
    vào, đếm từ 1 — ⛔ phải số hàng sheet)* để bên gọi gom được *"tháng nào thiếu gì"* mà ⛔ phải
    đọc chữ.
    """

    def __init__(self, thang: object, tien_te: str, vi_tri: int, ly_do: str) -> None:
        self.thang = thang
        self.tien_te = tien_te
        self.vi_tri = vi_tri
        # MỘT dòng, đọc được ngay (luật phòng tái phạm `S0-R1-04`). Câu AS-IS theo CÔNG THỨC Ô
        # (`CALC_ZONE_406.md`, `H1-R1-04`) — bản trước ghi "lỗi SUMIFS = 0" cho mọi cột, sai
        # với BO/BP (INDEX/MATCH) và với BR/BS (iferror ⇒ ô rỗng).
        super().__init__(
            f"⛔ thiếu tỷ giá {tien_te} tháng {thang!r} (dòng thứ {vi_tri}): {ly_do} — "
            f"⛔ quy đổi ra 0 hay ô rỗng (AS-IS: BO·BP·BR·BS rỗng do iferror, BM mất số do "
            f"SUMIFS = 0, BN #DIV/0! — CALC_ZONE_406)"
        )


class TienTeNgoaiGL(ValueError):
    """Dòng mang tiền tệ ⛔ thuộc 5 cột của GL ⇒ ⛔ có cột để vào. ⛔ Bỏ qua, ⛔ dồn cột khác."""


class TienKhongHuuHan(ValueError):
    """Nợ/Có là `Decimal` NaN / sNaN / ±Infinity — ⛔ là tiền *(`H1-R1-02`, hành vi ⓒ)*.

    Mang `vi_tri` *(đếm từ 1)* và `nhan` *("Nợ" | "Có")*. Tỷ giá ⛔ hữu hạn thì là `ThieuTyGia`
    *(⛔ có tỷ giá dùng được — cùng lớp với tỷ giá ≤ 0)*.
    """

    def __init__(self, nhan: str, vi_tri: int, gia_tri: Decimal) -> None:
        self.nhan = nhan
        self.vi_tri = vi_tri
        # In `gia_tri` được: nó chỉ có thể là NaN/sNaN/±Infinity — ⛔ bao giờ là một số tiền.
        super().__init__(
            f"⛔ {nhan} ở dòng thứ {vi_tri} là {gia_tri} — ⛔ hữu hạn, ⛔ phải số tiền "
            f"(lọt vào tồn LUỸ KẾ là đầu độc mọi dòng sau)"
        )


@dataclass(frozen=True)
class DongGL:
    """Một dòng sổ đưa vào GL *(phần AS-IS dùng để quy đổi: tháng · tiền tệ · E · F)*.

    `thang` là `yyyymm` *(khoá của `IX.FX` — AP §3.2.1)*; `tien_te` là mã như sổ ghi — được
    chuẩn hoá bằng `ma_tien_te` khi so *(hành vi ⓓ)*, `KetQuaDongGL.dong` giữ NGUYÊN chữ;
    `no`/`co` là **nguyên tệ** *(cột E/F)*, `Decimal` hữu hạn hoặc `int`.
    """

    thang: int
    tien_te: str
    no: Decimal
    co: Decimal


@dataclass(frozen=True)
class KetQuaDongGL:
    """Kết quả MỘT dòng, cùng thứ tự với dòng vào.

    `no`/`co`/`ton`: dict đủ 5 khoá `TIEN_TE_GL`, **nguyên tệ** — tiền nằm đúng ở cột tiền tệ
    của dòng, 4 cột kia = 0; `ton` là tồn luỹ kế SAU dòng này *(AZ · BC · BF · BI · BL)*.
    `ty_gia`/`ty_gia_usd`: tỷ giá đã dùng cho BO/BP và BR/BS *(tháng của dòng)* — để soi lại
    được từng ô. 8 cột CALC ZONE theo đúng thứ tự cột của sheet 406.
    """

    dong: DongGL
    no: dict[str, Decimal]
    co: dict[str, Decimal]
    ton: dict[str, Decimal]
    ty_gia: Decimal
    ty_gia_usd: Decimal
    vnd_ton_all: Decimal  # BM — tồn ALL, VND, đánh giá lại theo tỷ giá tháng của dòng
    musd_ton_all: Decimal  # BN — tồn ALL, mUSD
    bvnd_no: Decimal      # BO
    bvnd_co: Decimal      # BP
    bvnd_ton: Decimal     # BQ — luỹ kế BO − BP
    musd_no: Decimal      # BR
    musd_co: Decimal      # BS
    musd_ton: Decimal     # BT — luỹ kế BR − BS


def tinh_gl(
    dong: Iterable[DongGL],
    fx: Mapping[int, Mapping[str, Decimal]],
) -> list[KetQuaDongGL]:
    """Quy đổi từng dòng theo công thức ô NOW 406 *(docstring tệp)*; trả MỘT kết quả mỗi dòng.

    `fx`: tháng `yyyymm` → tiền tệ → số VND cho 1 đơn vị *(hình `IX.FX`; khoá tiền tệ cũng qua
    `ma_tien_te`)*. Thiếu tỷ giá ở BẤT KỲ dòng nào ⇒ `ThieuTyGia` cho cả lượt; tiền tệ ngoài
    5 cột ⇒ `TienTeNgoaiGL`; tiền ⛔ hữu hạn ⇒ `TienKhongHuuHan`; float ⇒ `TypeError`.
    """
    ton = {t: _KHONG for t in TIEN_TE_GL}
    bvnd_ton = _KHONG                               # BQ luỹ kế
    musd_ton = _KHONG                               # BT luỹ kế
    # tháng → (mã chuẩn hoá → [(khoá gốc, tỷ giá)]) — dựng MỘT lần mỗi tháng, chỉ trong lượt này
    bang_chuan: dict[object, dict[str, list[tuple[object, object]]]] = {}
    ra: list[KetQuaDongGL] = []
    with localcontext(_NGU_CANH):
        for vi_tri, d in enumerate(dong, start=1):
            no = _so_dung(d.no, "Nợ", vi_tri)
            co = _so_dung(d.co, "Có", vi_tri)
            ma = ma_tien_te(d.tien_te)              # ⓓ MỘT mã cho cả bốn phép so dưới đây
            if ma not in TIEN_TE_GL:
                raise TienTeNgoaiGL(
                    f"⛔ dòng thứ {vi_tri} mang tiền tệ {d.tien_te!r} (ma_tien_te ⇒ {ma!r}) — "
                    f"GL chỉ có 5 cột {' · '.join(TIEN_TE_GL)}; ⛔ bỏ qua, ⛔ dồn sang cột khác"
                )
            ty_gia = _tra_ty_gia(fx, bang_chuan, d.thang, ma, vi_tri)
            ty_gia_usd = _tra_ty_gia(fx, bang_chuan, d.thang, "USD", vi_tri)

            # ① tồn = tồn trên + Nợ − Có — cộng dồn theo THỨ TỰ đưa vào, theo tiền tệ
            #    (AZ11 = AZ10+AX11-AY11: một hàng xử CẢ HAI vế)
            ton[ma] = ton[ma] + no - co

            bvnd_no = ty_gia * no / _MOT_TY            # BO = tỷ giá × E / 10^9
            bvnd_co = ty_gia * co / _MOT_TY            # BP = tỷ giá × F / 10^9
            musd_no = bvnd_no / ty_gia_usd * _MOT_NGHIN   # BR = BO ÷ USD × 10^3
            musd_co = bvnd_co / ty_gia_usd * _MOT_NGHIN   # BS = BP ÷ USD × 10^3
            bvnd_ton = bvnd_ton + bvnd_no - bvnd_co    # BQ = BQ trên + BO − BP
            musd_ton = musd_ton + musd_no - musd_co    # BT = BT trên + BR − BS

            # BM = AZ×USD + BC×SGD + BF×COP + BI + BL×HKD — tỷ giá THÁNG CỦA DÒNG đang xét;
            # chỉ tiền tệ có tồn ≠ 0 mới cần tỷ giá (② · ⓐ). VND cộng thẳng.
            vnd_ton_all = ton[_DON_VI_BM]
            for t in _DANH_GIA_LAI:
                if ton[t]:
                    vnd_ton_all += ton[t] * _tra_ty_gia(
                        fx, bang_chuan, d.thang, t, vi_tri,
                        vi_sao=f" — BM/BN: tồn {t} ≠ 0 phải đánh giá lại theo tỷ giá tháng "
                               f"của dòng (AS-IS SUMIFS = 0 ⇒ BM mất số im lặng)",
                    )
            musd_ton_all = vnd_ton_all / ty_gia_usd / _MOT_TRIEU   # BN = BM ÷ USD ÷ 10^6

            ra.append(KetQuaDongGL(
                dong=d,
                no={t: (no if t == ma else _KHONG) for t in TIEN_TE_GL},
                co={t: (co if t == ma else _KHONG) for t in TIEN_TE_GL},
                ton=dict(ton),
                ty_gia=ty_gia,
                ty_gia_usd=ty_gia_usd,
                vnd_ton_all=vnd_ton_all,
                musd_ton_all=musd_ton_all,
                bvnd_no=bvnd_no,
                bvnd_co=bvnd_co,
                bvnd_ton=bvnd_ton,
                musd_no=musd_no,
                musd_co=musd_co,
                musd_ton=musd_ton,
            ))
    return ra


def _kieu_dung(v: object, nhan: str, vi_tri: int) -> Decimal:
    """`Decimal`/`int` → `Decimal`; ⛔ float *(bụi dấu phẩy động — ⛔ được vào tiền)*.

    ⛔ In GIÁ TRỊ vào thông điệp: chỉ kiểu — thông điệp lỗi hay đi vào log/phiếu.
    """
    if not isinstance(v, (Decimal, int)):
        raise TypeError(
            f"⛔ {nhan} ở dòng thứ {vi_tri} là {type(v).__name__} — chỉ nhận Decimal/int, "
            f"⛔ float (JSON thì đọc bằng parse_float=Decimal)"
        )
    return Decimal(v)


def _so_dung(v: object, nhan: str, vi_tri: int) -> Decimal:
    """Tiền: `_kieu_dung` + ⛔ hữu hạn ⇒ `TienKhongHuuHan` *(hành vi ⓒ)*.

    ⛔⛔ Bản trước chỉ chặn KIỂU khác *(float)* mà để giá trị ⛔ hữu hạn của CHÍNH kiểu được
    nhận đi qua: NaN ở Nợ ⇒ tồn NaN cho mọi dòng sau, ⛔ ném *(`KQ-072` F-2)*.
    """
    d = _kieu_dung(v, nhan, vi_tri)
    if not d.is_finite():                       # NaN · sNaN · Infinity · -Infinity
        raise TienKhongHuuHan(nhan, vi_tri, d)
    return d


def _tra_ty_gia(
    fx: Mapping[int, Mapping[str, Decimal]],
    bang_chuan: dict[object, dict[str, list[tuple[object, object]]]],
    thang: int,
    ma: str,
    vi_tri: int,
    vi_sao: str = "",
) -> Decimal:
    """`fx[thang][ma]` với khoá tiền tệ qua `ma_tien_te` *(ⓓ)* — vắng tháng, vắng cột, mơ hồ,
    ⛔ hữu hạn hay ≤ 0 đều là `ThieuTyGia`. `vi_sao` nối vào lý do *(BM nói vì sao cần)*.
    """
    gom = bang_chuan.get(thang)
    if gom is None:
        bang_thang = fx.get(thang)
        if bang_thang is None:
            raise ThieuTyGia(thang, ma, vi_tri, f"tháng ⛔ có trong bảng tỷ giá{vi_sao}")
        gom = {}
        for khoa, gia in bang_thang.items():
            gom.setdefault(ma_tien_te(khoa), []).append((khoa, gia))
        bang_chuan[thang] = gom
    khop = gom.get(ma, [])
    if not khop:
        raise ThieuTyGia(thang, ma, vi_tri,
                         f"tháng có trong bảng nhưng ⛔ có cột {ma}{vi_sao}")
    if len(khop) > 1:
        raise ThieuTyGia(
            thang, ma, vi_tri,
            f"tỷ giá mơ hồ — {len(khop)} khoá {[k for k, _ in khop]!r} cùng chuẩn hoá thành "
            f"{ma!r} (ma_tien_te), ⛔ chọn một{vi_sao}",
        )
    gia = _kieu_dung(khop[0][1], f"tỷ giá {ma} tháng {thang!r}", vi_tri)
    if not gia.is_finite():                     # trước phép so `<= 0`: NaN so ⇒ InvalidOperation
        raise ThieuTyGia(thang, ma, vi_tri, f"tỷ giá {gia} ⛔ hữu hạn{vi_sao}")
    if gia <= 0:
        raise ThieuTyGia(
            thang, ma, vi_tri,
            f"tỷ giá = {gia} ⛔ dương (0 là dấu vết ô tỷ giá trống — INDEX trả rỗng ⇒ "
            f"BO/BP = 0; tháng vắng ⇒ SUMIFS = 0){vi_sao}",
        )
    return gia
