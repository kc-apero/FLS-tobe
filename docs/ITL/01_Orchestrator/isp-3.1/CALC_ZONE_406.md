# CALC ZONE 406 — công thức NOW nguyên văn (đọc 2026-11-16)

> Orchestrator đọc bằng connector, **chỉ công thức** (`userEnteredValue`, ⛔ giá trị, ⛔ dữ liệu người) từ bản sao `[COPY] Report I General Ledger | P&L Report` · sheet `Report I General Ledger` · hàng tiêu đề 7–9, hàng dữ liệu 10–12. Phục vụ: R1 của H1 (`BG-071` câu Q1) và bước H4 (parity CA.GL ↔ 406). ⚠ Giá trị của bản sao hôm nay ⛔ dùng được làm đáp án (`B-DATA-1`: `9.2.Exchange Rate` = `#REF!` ⇒ mUSD `#DIV/0!`) — tệp này chỉ khai CẤU TRÚC và CÔNG THỨC.

## Bản đồ cột (hàng 7 · 8 · 9)

| Cột | Hàng 7 | Hàng 8 | Hàng 9 | Công thức hàng 10 | Hàng 11 trở đi |
|---|---|---|---|---|---|
| AX · AY · AZ | Phát sinh · · Tồn | PS Nợ · PS Có · — | USD | `AX = if($D10=AX$9,$E10,"")` · `AY = if($D10=AY$9,$F10,"")` · `AZ = AX10-AY10` | `AZ11 = AZ10+AX11-AY11` — **tồn LŨY KẾ theo thứ tự dòng, nguyên tệ** |
| BA · BB · BC | như trên | | SGD | cùng khuôn (cột D = tiền tệ, E = Nợ, F = Có) | lũy kế |
| BD · BE · BF | như trên | | COP | cùng khuôn | lũy kế |
| BG · BH · BI | như trên | | VND | cùng khuôn | lũy kế |
| BJ · BK · BL | như trên | | HKD | cùng khuôn | lũy kế |
| BM | `TỒN ALL theo cột AZ; BC; BF; BI và BL` | — | VND | `AZ*SUMIFS(9.2!B, 9.2!H, DATE(YEAR(A),MONTH(A),1)) + BC*SUMIFS(…C…) + BF*SUMIFS(…D…) + BI + BL*SUMIFS(…F…)` | cùng khuôn trên hàng của nó — **tồn từng tiền tệ × tỷ giá THÁNG CỦA DÒNG ĐANG XÉT** (đánh giá lại) |
| BN | — | — | mUSD | `(AZ + BC*SGD/USD + BF*COP/USD + BI/USD + BL*HKD/USD)/10^6` (mọi tỷ giá qua `SUMIFS` theo tháng của dòng) | cùng khuôn |
| BO · BP | `Phát sinh theo cột E và F` | PS Nợ · PS Có | bVND | `iferror(INDEX('9.2'!$A$1:$H, MATCH(DATE(YEAR(A10),MONTH(A10),1), '9.2'!$H$1:$H, 0), MATCH(D10, '9.2'!$A$1:$H$1, 0)) * E10 \| F10 / 10^9)` | cùng khuôn |
| BQ | Tồn | — | bVND | `BO10-BP10` | `BQ11 = BQ10+BO11-BP11` — lũy kế |
| BR · BS | `Phát sinh theo cột E và F` | PS Nợ · PS Có | mUSD | `iferror(BO10 \| BP10 / SUMIFS('9.2'!$B:$B, '9.2'!$H:$H, DATE(YEAR(A10),MONTH(A10),1)) * 10^3)` | cùng khuôn |
| BT | Tồn | — | mUSD | `BR10-BS10` | `BT11 = BT10+BR11-BS11` — lũy kế |
| BU | Date of Balance | MID 1 | — | `=A10` | |

`9.2!H` = ngày đầu tháng của dòng tỷ giá (sheet `9.2.Exchange Rate` của sổ này là `IMPORTRANGE(<FS2 gốc>, "9.2.Exchange Rate!A1:G")`).

## Hai NGỮ NGHĨA tra tỷ giá khác nhau trong cùng một dòng — H4 phải tái hiện cả hai

| Cột | Cách tra | Tháng THIẾU | Tháng TRÙNG (hai dòng) |
|---|---|---|---|
| BO · BP | `INDEX/MATCH` (khớp đầu tiên) theo (tháng, tiền tệ của dòng) | `iferror` ⇒ ô **rỗng** | lấy dòng ĐẦU |
| BM · BN · BR · BS | `SUMIFS` theo tháng | `SUMIFS` = **0** ⇒ BR/BS `iferror(…/0)` ⇒ rỗng; **BM nhân với 0 ⇒ mất số IM LẶNG**; BN `/0` ⇒ `#DIV/0!` | **CỘNG ĐÔI** tỷ giá |

⇒ FLS (D1 DECIDED): tháng thiếu/chưa ký ⇒ **CHẶN có tên** (`ThieuTyGia` ở H1 · `FX_CHAN` ở C7). Khi so với đáp án, ô AS-IS rỗng/0/`#DIV/0!` do tháng thiếu là **lệch CÓ TÊN** (⛔ đếm là lỗi FLS, ⛔ đếm là khớp).

## Ghi chú cho từng bước
- **H1** (`BG-071` L2): cách đọc "tồn theo từng tiền tệ, nguyên tệ, lũy kế theo thứ tự dòng" — **ĐÚNG** với `AZ · BC · BF · BI · BL`. BM/BN (tồn ALL đánh giá lại theo tỷ giá tháng của dòng) chưa nằm trong phạm vi H1 nếu H1 chưa dựng — H4 sẽ lộ ra khi so BM–BN.
- **H4**: so `BM … BT` (8 cột) theo dòng × kỳ; dung sai số thực nhị phân của Sheets ↔ `Decimal` phải khai trong `mong`.

## Số dư đầu kỳ GÕ TAY ở hàng 24 (orchestrator đo 2026-11-18 — chỉ THÊM)
Đọc CÔNG THỨC (`valueRenderOption=FORMULA`, khoá SA) `'Report I General Ledger'!AX10:BT7892`, so từng ô với khuôn hàng 11 (thay số hàng): **181.263 ô so · 5 ô lệch khuôn · cả 5 ở hàng 24** (dòng sổ ds24, kỳ 2024-12):

| Ô | Công thức thật | Nghĩa |
|---|---|---|
| `AX24` | `=+1235500+7189` | PS Nợ USD **gõ cứng** (thay công thức dòng) |
| `BA24` | `=985537` | PS Nợ SGD **gõ cứng** |
| `BG24` | `=if($D24=BG$9,$E24,"")+6653796781` | PS Nợ VND của dòng **cộng thêm hằng** |
| `BQ24` | `=BQ23+BO24-BP24+56842628558/10^9` | tồn bVND **cộng hằng** |
| `BT24` | `=BT23+BR24-BS24+2.267718` | tồn mUSD **cộng hằng** |

⇒ Đây là **số dư đầu kỳ AS-IS nhập tay**; mọi cột lũy kế (AZ · BC · BI · BM · BN · BQ · BT) từ hàng 24 trở đi mang nó. FLS (H1) ⛔ có khái niệm số dư đầu kỳ ⇒ H4 gieo 5 hằng này tường minh khi so (`WO-132`); **nguồn chính thức của số dư đầu kỳ trong FLS là câu hỏi cho BA/owner** (errata ⑳). Công cụ đo: `isp-3.1/chuyen_giao/cong_cu/sa_quet_cong_thuc.py`.

## Nguồn của 5 số dư đầu kỳ hàng 24 — đo 18/11 *(orchestrator, khoá SA chỉ-đọc; trả lời errata ⑳)*

Người dùng 18/11 chỉ nguồn: bảng tính `1ycMOKKZg5rraLAYW-HuZDp9k3RPzr0H-iyPs_0IKL5Q`, tab **`2. CCR Cash`** *(232 × 719)*. Đo thêm tab cạnh nó **`2. CCR`** *(239 × 741)* — hai tab cùng khuôn: hàng 5/22 = ngày (serial), cột `K` = **45657 = 31/12/2024**; hàng 10–14 *"Original Currency"* USD·SGD·COP·HKD·VND; hàng 15–19 *"TOTAL"* quy đổi.

| Ô 406 hàng 24 | Hằng gõ tay | Đo ở nguồn, cột `K` (31/12/2024) | Khớp |
|---|---|---|---|
| `AX24` USD | `1235500 + 7189` | `2. CCR`!K10 = **1.235.500,01** + `2. CCR Cash`!K10 = **7.188,78** | ✅ (làm tròn đơn vị) |
| `BA24` SGD | `985537` | `2. CCR`!K11 = **985.537,37** | ✅ (làm tròn) |
| `BG24` VND | `+6653796781` | `2. CCR`!K14 = **6.837.981.082** · `2. CCR Cash`!K14 = 0 | ⚠ lệch **184.184.301** — xấp xỉ một dòng VND của pháp nhân `VVOO (VGO2)` ở `2. CCR` hàng 40 *(184.184.303; còn 2 đơn vị)* ⇒ nhiều khả năng hằng = tổng trừ pháp nhân ngoài phạm vi ITL — **chưa chứng minh** |
| `BQ24` bVND tồn | `+56842628558/10^9` | `2. CCR`!K19 TOTAL VND = 56.846.965.721,77 | ⚠ lệch 4.337.164 VND |
| `BT24` mUSD tồn | `+2.267718` | `2. CCR`!K15 TOTAL USD = 2.267.891,40 | ⚠ lệch 173,4 USD |

- ⚠ Hàng 24 của 406 thuộc kỳ **2024-10** *(`gl_406.json` `ky = 202410`)* nhưng số dư nguồn là ngày **31/12/2024** — cột đầu của cả hai tab; hai tab ⛔ có cột trước 31/12/2024.
- ⛔ đọc cột `D:J` của hai tab: có cột `Link` · `ID` · `Pass` *(thông tin đăng nhập ngân hàng)* và số tài khoản; một nhãn ngân hàng ở `2. CCR Cash` mang tên người ⇒ ⛔ chép vào repo. Bản thô đã xoá khỏi scratchpad.
- ⇒ **Kết luận cho H4:** giữ 5 hằng như sheet 406 gõ (parity với AS-IS); nguồn chính thức cho TO-BE = `2. CCR` + `2. CCR Cash` ngày 31/12/2024 — câu hỏi còn mở cho BA/owner: (1) VND loại pháp nhân nào; (2) số dư 31/12/2024 vì sao đặt ở hàng kỳ 2024-10.

### Đính chính + soát logic từng ô hàng 24 — 18/11 *(orchestrator, khoá SA; chỉ THÊM — câu trên GIỮ làm biên bản)*

**Người dùng 18/11:** (1) số dư VND **CÓ loại** pháp nhân `VVOO (VGO2)`; (2) "có thể nhầm — soát công thức từng ô, có thể trùng số hoặc đặt nhầm".

- ⛔ **Lỗi của orchestrator ở mục trên:** câu *"Hàng 24 thuộc kỳ 2024-10"* SAI — tôi đọc `ky` của 3 dòng ĐẦU ảnh (`thu_tu` 1…3) rồi gán cho hàng 24. Đo lại cột `A`: **hàng 24 = 2024-12-31** *(D = VND)*; hàng 22–23 = 2024-12-29 (USD); hàng 25 = 2025-01-02. ⇒ số dư 31/12/2024 đặt ĐÚNG ngày, ⛔ đặt nhầm.
- **Soát công thức `AX24:BT24`** (đọc `FORMULA` + `UNFORMATTED_VALUE` hàng 10…26; tỷ giá `9.2.Exchange Rate` kỳ 202410…202412 = USD 25.066 · SGD 19.319):

| Ô | Công thức | Đo | Kết luận |
|---|---|---|---|
| `AX24` USD | `=+1235500+7189` — THAY HẲN `if($D24=AX$9,$E24,"")` | `D24 = VND` ⇒ công thức gốc ra `""` ⇒ ⛔ mất phát sinh | = `2. CCR` 1.235.500,01 + `2. CCR Cash` 7.188,78 = 1.242.688,79 làm tròn **+0,21 USD**; `AZ23 = 0` ⇒ ⛔ trùng |
| `BA24` SGD | `=985537` — thay hẳn `if` | như trên, ⛔ mất phát sinh | = 985.537,37 làm tròn **−0,37 SGD**; `BC23 = 0` ⇒ ⛔ trùng |
| `BG24` VND | `=if(…,$E24,"")+6653796781` | `E24` = 21.345 vẫn được cộng | Lũy kế VND hàng 10…23 `BI23` = **184.162.958**; + `E24` 21.345 = **184.184.303** = ĐÚNG số dư dòng `VVOO (VGO2)` TCB ở `2. CCR`. Hằng = 6.837.981.082 (tổng `2. CCR`) − 184.184.303 (VVOO) = 6.653.796.779 ⇒ gõ **6.653.796.781: thừa 2 VND**. `BI24` = 6.837.981.084 = tổng CCR + 2 ⇒ **⛔ trùng**: phần VVOO do chính các dòng sổ hàng 10…24 dựng, phần còn lại do hằng |
| `BQ24` bVND tồn | `=BQ23+BO24-BP24+56842628558/10^9` | `1.242.689×25.066 + 985.537×19.319 + 6.653.796.781 = 56.842.628.558` **khớp ĐÚNG từng đồng** | hằng = 3 hằng trên quy đổi ở tỷ giá kỳ 2024-12 (⛔ dùng TOTAL của CCR — CCR dùng SGD 19.319,35 và ⛔ gồm 7.188,78 USD tiền mặt); `BQ23` = 0,184163 (VVOO) ⇒ ⛔ trùng |
| `BT24` mUSD tồn | `=BT23+BR24-BS24+2.267718` | 56.842.628.558 / 25.066 / 10⁶ = 2,26771837 | = `BQ` hằng ÷ USD 2024-12, làm tròn 6 số lẻ (**−0,37 USD**) |
| `BD24` · `BJ24` (COP · HKD) | khuôn chuẩn | CCR 31/12 COP = HKD = 0 | đúng |

- **Kết luận:** ⛔ có trùng số, ⛔ đặt nhầm ngày. Lệch thật chỉ là **làm tròn + 2 VND gõ thừa**: USD +0,21 · SGD −0,37 · VND **+2** · bVND (kéo theo) · mUSD −0,37 USD. Cách ghép: số dư VVOO = lũy kế dòng sổ (sổ ITL có giao dịch VVOO từ 21/10/2024); số dư các pháp nhân khác = hằng ngày 31/12/2024 lấy từ `2. CCR` + `2. CCR Cash`.
- **Cho TO-BE (C-lane / H4):** số dư đầu kỳ = bản khai có chủ (owner ký), mốc **31/12/2024**, theo tiền tệ nguyên tệ (USD · SGD · VND; COP · HKD = 0), **loại VVOO** (người dùng chốt); `bVND`/`mUSD` tồn là SUY RA từ bản khai × tỷ giá kỳ 2024-12 — ⛔ khai riêng. H4 vẫn gieo đúng 5 hằng gõ tay để parity AS-IS (gồm cả 2 VND thừa).
