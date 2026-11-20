# BG-250 — bàn giao WO-249 · ISP 3.1.2 · DT6c: ảnh ĐẦU VÀO HR 2025 + công thức CFA3 cho H7

| | |
|---|---|
| **Phiếu** | trả `WO-249` *(DT6c, làn DATA)* |
| **Bởi** | phiên cloud `fls-dev #DATA` · cụm PG **5436** · nhánh `isp/DT6C` · 2026-11-19 |
| **Nền** | `b8afd74` · commit ① mã+bài+ảnh `19252c0` |
| **Dải phiếu** | `KQ-251` (R1) · `KQ-252` (R2) |

## 0. Kết luận
AC-1…AC-5 đạt. **Y2025 đọc ĐƯỢC từ file gốc** ⇒ ảnh đầu vào `tests/fixture/dau_vao/hr_ledger_2025.json` (**10.105** hàng; `checksum_noi_dung` `c27a12e49b7aa875`). Khuôn `hr_ledger_2025` **gọi** `chuan_bi_chung`/`thieu_lac_chung` của `hr_ledger_2024` *(⛔ chép)*; ảnh 2024 và mọi ảnh khác đúng từng byte. ⚠ **Hai phát hiện cho H7** ở §2–§3: kỳ **2026-01 ⛔ có đầu vào** ở file nguồn; và **2.302 hàng `ky_suy` ⛔ phải là hàng có ngày ở nguồn** — nguồn gán ngày KHÁC kỳ "hàng trên".

## 1. Nguồn *(AC-1)* — file gốc `1YEyGxBY…ZAoD4`, đọc CHỈ-ĐỌC
Bản đồ cột bằng hàng tiêu đề 3 TRƯỚC *(4 tab 2025/2026 đều khớp 9 tiêu đề)*; chỉ đọc `A·D·E·F·G·H·S·T·AG`. Cột `A` là serial ngày ở **10.105/10.105** hàng; 0 hàng rỗng; 0 hàng có nội dung mà thiếu ngày.
| Tab | Vùng đọc | Hàng | Theo kỳ |
|---|---|---|---|
| `1.3 Ledger NIS/INT/COM 2025` | hàng 4…7588 | **7.585** | 01=225 · 02=668 · 03=629 · 04=579 · 05=365 · 06=916 · 07=850 · 08=767 · 09=912 · 10=868 · 11=478 · 12=328 *(2025)* |
| `1.3 Ledger PIT 2025` | hàng 4…2523 | **2.520** | 04=462 · 07=835 · 10=1.223 |
| `… 2026` NIS · PIT | — | **⛔ không lấy** | NIS: 588 hàng ở kỳ **2026-10 = 452 · 2026-11 = 136** *(0 hàng 2026-01)*; PIT: 293 hàng mà `A` ⛔ số ngày |
Σ PS Có theo kỳ *(hai tab, VND)*: 01 = 321.317.500 · 02 = 5.745.812.541 · 03 = 5.971.078.533 · 04 = 7.967.090.891 · 05 = 6.623.088.442 · 06 = 7.642.967.845,363 · 07 = 9.712.306.163,707232147 · 08 = 7.862.221.681 · 09 = 8.241.418.295 · 10 = 11.751.792.973 · 11 = 7.356.669.375 · 12 = 7.332.731.464.
Khác Y2024 *(khuôn nới có chủ đích, mỗi nới có `mong` đếm riêng — Đ5)*: **9** ô `F` NIS là số LẺ ⇒ `cho_so_le`, Σ `Decimal`; **1** ô `LE = #N/A` *(hàng sheet NIS 7430)* ⇒ tập đóng LE thêm `#N/A`, `MONG_LE_NA = 1`; **9** ô `H` mang số tài khoản ⇒ che về `R`, `MONG_H_R = 9`. Khoá `dong_sheet`: PIT = `100000 + hàng sheet`. Ảnh 3,57 MB.

## 2. Đối chiếu với `gl_hr_408` *(AC-2)* — 408 chỉ để ĐO
Mẫu số > 0 *(Đ3)*: 408 có 9.410 hàng CÓ NGÀY. Khớp **cả số hàng lẫn Σ PS Có** ở 6/12 kỳ *(01 · 03 · 04 · 05 · 07 · 11)*; lệch CÓ TÊN *(nguồn − 408)*:
| Kỳ | Hàng | Σ PS Có | Ghi |
|---|---|---|---|
| 2025-02 | +3 | +1.760.000 | nguồn hơn 408 |
| 2025-06 · 08 · 09 | +1 mỗi kỳ | 0 | hàng PS Có rỗng/0 ở nguồn |
| 2025-10 | **+1.227** | **+3.369.480.447** | = đúng PIT 2025-10 *(1.223 hàng, ΣF 3.369.480.447)* + 4 hàng NIS: 408 ⛔ có PIT kỳ 10 *(PIT 04·07 thì có)* |
| 2025-12 | **−269** | **−413.535.000** | 408 hơn nguồn 269 hàng |
| **2026-01** | *(408 = 269 hàng, ΣF 7.216.357.058)* | | **⛔ đầu vào** — số 269 trùng đúng số hàng thừa ở 2025-12 |
Đo trực tiếp ⛔ giải thích hết nguyên nhân ở 2025-12/2026-01 *(chưa tra từng hàng)* — câu cho BA/H7.

**2.302 hàng `ky_suy` có NGÀY ở ledger nguồn không?** Đếm khoá nội dung `(PS Nợ, PS Có, TK, HDCode, CDT1)` có bội, trừ phần 408-có-ngày đã dùng:
- Nguồn dư sau khi trừ 408-có-ngày = 1.264 hàng; **1.201/2.302** hàng suy trùng nội dung với hàng dư *(ngày nguồn = 2025-10, PIT)*; **1.101/2.302** ⛔ trùng hàng nào.
- Trong 1.201: **chỉ 76** khớp luôn kỳ gán *(2025-10)*; **1.125** nguồn ghi **kỳ khác** kỳ "hàng trên" gán: 556 *(gán 06)* + 329 *(gán 07)* + 316 *(gán 08)* ⇒ nguồn nói 2025-10. Kỳ gán 09 · 10 · 11: **0** trùng *(538 · 276 · 265 hàng không tìm thấy)*.
⚠ Khoá nội dung là bằng chứng YẾU *(hàng phân bổ lặp)*; kết luận an toàn: **ledger nguồn ⛔ chứng thực kỳ `hang_tren`**; 2.302 hàng của 408 ⛔ nằm gọn trong 10.105 hàng nguồn.

## 3. Công thức *(AC-3 — chỉ đọc, nguyên văn)*
**CFA3** — sổ CF `12S00TnFMd9Uz0g-NLvOA7kdmPPhY1V_SVOQJkDi1ZiU`, tab `MID I Report I CFA3 Daily`, ô lá **`G13`** *(hàng `F13` = `MC | Maketer Cost`; `G5` = ngày; 31.338/31.782 ô vùng `A1:SH99` là công thức)*:
```
=SUMIFS('Report I H1000 Ledge (HR Allocate HD) Y2025'!$BA:$BA,'Report I H1000 Ledge (HR Allocate HD) Y2025'!$A:$A,G$5,'Report I H1000 Ledge (HR Allocate HD) Y2025'!$V:$V,$F13)-SUMIFS('Report I H1000 Ledge (HR Allocate HD) Y2025'!$BB:$BB,'Report I H1000 Ledge (HR Allocate HD) Y2025'!$A:$A,G$5,'Report I H1000 Ledge (HR Allocate HD) Y2025'!$V:$V,$F13)
```
⇒ CFA3(HD, ngày) = Σ `BA` − Σ `BB` của sheet `… Y2025` có `A` = ngày và `V` = nhóm HD *(`BA`/`BB` = mUSD Nợ/Có)*. Hàng tiêu đề: `G1 =YEAR(G5)` · `G4 =MONTH(G5)` · `G5` (ô đầu) = hằng `45585`, các ô sau `=G5+1`; hàng nhóm cha là `=sum(…)` các con.

**`Report I H1000 Ledge (HR Allocate HD) Y2025 | For PL Report`** *(sổ P&L `19NNTbXJ…shEU2g`, đọc CÔNG THỨC)* — **ba ô là HẰNG** *(giá trị dán, ⛔ công thức)*:
| Ô | Nội dung |
|---|---|
| `A10` | `45636` *(serial = 2024-12-01)* |
| `E10` | `3029839765` |
| `V10` | `NIS \| Net Income Staff` |
| `BA10` | `=iferror(AX10/SUMIFS('9.2.Exchange Rate'!$B:$B,'9.2.Exchange Rate'!$H:$H,DATE(YEAR(A10),MONTH(A10),1))*10^3)` |
⇒ `BA` = `AX` (VND) ÷ tỷ giá của THÁNG của `A` × 1.000; `A`·`E`·`V` là cột dán ⇒ **kỳ ở ngày `A`**, nên 2.302 hàng thiếu ngày ở 408 mà `A` rỗng ⇒ `BA`/`BB` rỗng *(khớp BG-227 §3)*.

## 4. PII *(AC-4)*
9 cột như DT6b; ⛔ `B`·`C`·`I·J·K`·`M…R`; 0 `@`; 0 tên cột cấm; 0 ô chữ ≥ 6 chữ số liền; 9 ô `H` che `R`. ⛔ in giá trị số TK. Máy quét `tools/quet_pii_repo.py` **chưa gộp** ở nền này *(0 tệp)* ⇒ đo bằng bài `Y25_B2` *(quét ảnh + ca phá)*. Bản thô `/tmp/dt6c/` *(chmod 600)* **đã xoá** sau BG; ⛔ commit.

## 5. Bài · đột biến
`tests/du_lieu/test_dap_an_hr_ledger_2025.py` **12 bài** *(ảnh · PII · tái tạo đúng byte · ca phá · đối chiếu 408 · ảnh 2024 đúng byte)*; `…_2024` 10 bài xanh *(ảnh 2024 đúng từng byte)*. Đột biến trên khuôn dùng chung: bỏ che số trần ⇒ ĐỎ · bỏ đếm `#N/A` ⇒ ĐỎ · bỏ so ΣF ⇒ ĐỎ · cắt phần lẻ ⇒ ĐỎ; trả nguyên ⇒ xanh.
**Q8:** sàn `MONG_PYTEST_TOAN_BO` **4084 → 4097** *(= số bài thu thập)* ở `tools/dung_moi_truong_isp.sh` + bài ghim `tests/test_dung_moi_truong_isp.py` cùng commit; web giữ 675.

## 6. Cổng
`--duong-nen --cong 5436` MỘT lần (một mình): **KẾT ĐẠT** — tập đỏ + XFAIL **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)*, chạy **4097** (mong ≥ 4097) · skipped 0 · deselected 0; `tests/web` **3 = 3**, chạy 675. `lint-imports` **11 kept / 0 broken** · `kiem_tai_lieu` ĐẠT *(380 tệp · 2719 bảng)*. Ghi kho THẬT: `KHONG`.
