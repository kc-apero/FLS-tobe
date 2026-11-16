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
