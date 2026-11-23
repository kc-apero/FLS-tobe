# BG-227 — bàn giao WO-225 · ISP 3.1.2 · DT6b: Y2024 HR từ file gốc + gán kỳ cho 2.302 hàng thiếu ngày

| | |
|---|---|
| **Phiếu** | trả `WO-225` *(DT6b, làn DATA)* |
| **Bởi** | phiên cloud `fls-dev #DATA` · cụm PG **5436** · nhánh `isp/DT6B` · 2026-11-19 |
| **Nền** | `213a40a` · commit ① mã+bài+ảnh `104f332` |
| **Dải phiếu** | `KQ-228` (R1) · `KQ-229` (R2) |

## 0. Kết luận
Cả 5 AC đạt. **Y2024 đọc ĐƯỢC từ file gốc** (1.381 hàng) ⇒ ảnh đầu vào mới `tests/fixture/dau_vao/hr_ledger_2024.json`; **2.302 hàng thiếu ngày** vào bảng chính của `gl_hr_408` · `gl_hr_413` với `ky_suy = "hang_tren"`. 407 và mọi ảnh DT2…DT10·DT8b **đúng từng byte** (`git diff` chỉ chạm 2 ảnh `dap_an` + 1 ảnh mới). `--duong-nen --cong 5436` MỘT lần: xem §6.

## 1. Y2024 *(AC-1)* — file gốc `1YEyGxBY…ZAoD4`, đọc CHỈ-ĐỌC
Bản đồ cột bằng hàng tiêu đề 3 TRƯỚC ⇒ chỉ đọc 9 cột `A·D·E·F·G·H·S·T·AG` (⛔ `B` Số CT · `C` Diễn giải · `I·J·K` nội dung PE/PI · `M…R` ID). Khuôn `tools/khuon_dong_bang/hr_ledger_2024.py`; cổng khai `mong` cả hai chiều.
| Tab | Hàng có ngày | Theo kỳ |
|---|---|---|
| `1.3 Ledger NIS/INT/COM 2024` | 969 | 2024-11 = 165 · 2024-12 = 536 · 2025-01 = 268 |
| `1.3 Ledger PIT 2024` | 412 | 2025-01 = 200 · 2025-04 = 212 |
Σ PS Có mỗi kỳ *(VND, hai tab)*: 2024-11 = 286.400.000 · 2024-12 = 5.140.567.470 · 2025-01 = 5.543.361.433 · 2025-04 = 551.671.054. Khoá `dong_sheet`: PIT = `100000 + hàng sheet`. Ảnh `481.877` B · `checksum_noi_dung` `4905b28f88819142`.

## 2. Đối chiếu với 413 *(AC-2)* — Y2024 ↔ phần 413 hơn 408 *(1.375 dòng, DT6)*
Khoá so từng hàng `(kỳ, PS Nợ, PS Có, TK, HDCode, CDT1)`. Mẫu số > 0 *(Đ3)*: 1.375 hàng ở 413.
| Kỳ | Y2024 | 413 − 408 | Khớp từng ô | Chỉ ở Y2024 | Chỉ ở 413 |
|---|---|---|---|---|---|
| 2024-11 | 165 | 165 | **165** | 0 | 0 |
| 2024-12 | 536 | 530 | **530** | **6** | 0 |
| 2025-01 | 468 | 468 | **468** | 0 | 0 |
| 2025-04 | 212 | 212 | **207** | **5** | **5** |
- **Σ PS Có bằng nhau cả 4 kỳ** (286.400.000 · 5.140.567.470 · 5.543.361.433 · 551.671.054) ⇒ lệch **chỉ ở PS Nợ**.
- **2024-12 (536 vs 530)** — 6 hàng chỉ ở Y2024: chỉ có PS Nợ, ⛔ TK/HDCode/CDT1/PS Có; **đúng 6 ô `H` mang số tài khoản** (cùng 6 hàng, hàng sheet 407–410 · 461 · 462 của tab NIS). 413 *(P&L dán giá trị)* không có 6 hàng này.
- **2025-04 (5 hàng PIT)** — Y2024 và 413 cùng `F=0` · TK `No 5/10/15/20/25` · HDCode · CDT1, **khác PS Nợ**: 413 chia lại *(có phần lẻ `…,333`/`…,667`)*; 207/212 hàng còn lại khớp từng ô.

## 3. 2.302 hàng thiếu ngày *(AC-3 · AC-4)* — gán kỳ theo hàng CÓ NGÀY liền trên
Khuôn: sửa `_gl_hr.py` **chỉ** nhánh đoạn A-rỗng GIỮA *(chế độ `suy=True`; 407 giữ `suy=False`)*; bảng chính + cột `ky_suy`; bảng phụ `gan_ky` *(tu · so_hang · ky · tong_F)*; `doan_trong` còn ĐOẠN ĐUÔI *(408: 7.517 hàng · 413: 7.142 hàng — ⛔ gán)*. Hàng rỗng hoàn toàn ở đoạn giữa ⇒ TỪ CHỐI *(đo: 0)*.
| Đoạn | Hàng sheet đầu (408 · 413) | Số hàng | Kỳ gán | Σ PS Có |
|---|---|---|---|---|
| 1 | 5221 · 6596 | 566 | 2025-06 | 1.561.809.688 |
| 2 | 6546 · 7921 | 335 | 2025-07 | 808.591.958 |
| 3 | 8163 · 9538 | 322 | 2025-08 | 999.078.801 |
| 4 | 9023 · 10398 | 538 | 2025-09 | 1.743.362.012 |
| 5 | 10113 · 11488 | 276 | 2025-10 | 826.128.265 |
| 6 | 10919 · 12294 | 265 | 2025-11 | 824.557.779 |
| **Σ** | | **2.302** | | **6.763.528.503** *(= mong; cả 408 lẫn 413; PS Nợ = 0)* |
Hàng gán kỳ **không có** `BA`·`BB` (mUSD) *(2.302/2.302 rỗng)* ⇒ hai cột nới `so?` ở 408·413, cổng đòi hàng CÓ NGÀY vẫn đủ (`mUSD_rong@`). 2.302 hàng qua đủ tập đóng *(G · H · I · J · P · V · Z · AD)*, 0 giá trị lạ.

**Ảnh đổi — khai từng ảnh + lý do** *(checksum ghim cập nhật CÓ CHỦ ĐÍCH)*:
| Ảnh | Dòng | `checksum_noi_dung` | Lý do |
|---|---|---|---|
| `gl_hr_408.json` | 9.410 → **11.712** | `59e1157d077c51e8` → `c876e0fe3bffd5d7` | +2.302 hàng · +cột `ky_suy` · phụ `gan_ky` · `doan_trong` 7→1 |
| `gl_hr_413.json` | 10.785 → **13.087** | `b3b4e8485378ff57` → `dd8dc675e19dfce7` | như trên |
| `gl_hr_407.json` | 9.421 | `62c6b780950f167a` *(không đổi)* | 0 đoạn giữa ⇒ đúng từng byte |
`cfa3` · `gl_406` · mọi ảnh DT2…DT10 · DT8b: `git diff` 0 tệp. Số dòng mỗi kỳ mới ở khuôn `KY_MONG` *(408: 2025-06 = 1.481 · 07 = 2.020 · 08 = 1.088 · 09 = 1.449 · 10 = 1.140 · 11 = 743)*.
⚠ **Hệ quả cần biết:** 407 hơn 408 đúng **11** hàng *có ngày* (LE `#N/A`) — bài DT6 nay đếm hàng có ngày; **tính cả hàng gán kỳ, 408 (11.712) > 407 (9.421)**; 407 không có đoạn giữa nên 2.302 hàng này ⛔ nằm ở bảng chính 407 *(còn có nằm trong đoạn đuôi A-rỗng 9.808 hàng của 407 hay không: ⛔ đo — câu cho BA nếu cần)*.

## 4. PII
- Đọc: 9 cột Y2024 + lưới GL HR đọc lại 408/413 *(cột `Q·AH·AP·AU·AV` chỉ đo rỗng/không rỗng, ⛔ lưu giá trị — thay bằng `0`)*; ⛔ in/ghi `Số chứng từ` · `Diễn giải` · tên · email · ID Payee. Máy quét ảnh: 0 `@` · 0 tên cột cấm · 0 ô chữ ≥ 6 chữ số liền.
- **6 ô `H` Y2024 mang số tài khoản — KHÁC DT6:** là **dãy 9 chữ số trần**, ⛔ có tiền tố `R |` *(đo hình dạng)* ⇒ CHE về `R` *(như DT6)*; cổng khai `MONG_H_R = 6`. Dạng DT6 `R | <số>_…` cũng che. Ảnh 0 chữ số TK. *(Khi đo hình dạng tôi vô tình in 3 chữ số đầu của các ô này ra log phiên — ⛔ ghi vào đâu, ⛔ lặp lại ở đây.)*
- Bản thô `/tmp/dt6b/` (chmod 600) — **xoá sau BG**, ⛔ commit; ⛔ `Client secret`.

## 5. Bài · đột biến
- `tests/du_lieu/test_dap_an_gl_hr_cfa3.py` 29 → **39** *(+10: 2.302 hàng · ky_suy · ΣF · 407 giữ byte · ca phá F/lạc cột/hàng rỗng/cắt đoạn · gọi thẳng cổng)*; `tests/du_lieu/test_dap_an_hr_ledger_2024.py` **10** *(ảnh · PII · tái tạo đúng byte · ca phá · đối chiếu 413)*.
- Đột biến trên mã: GL HR `M1` bỏ so ΣF ⇒ ĐỎ · `M2` bỏ so kỳ liền trên ⇒ ĐỎ · `M3` bỏ chặn hàng rỗng ⇒ ĐỎ · `M4` ép kỳ ⇒ ĐỎ *(3 bài tái tạo)*. Y2024 `M1` bỏ so ΣF ⇒ ĐỎ · `M2` bỏ che số trần ⇒ ĐỎ · `M3` bỏ tập đóng ⇒ ĐỎ *(2 bài)* · `M4` bỏ offset PIT ⇒ ĐỎ · `M5` bỏ `H_che` ⇒ ĐỎ. Trả nguyên ⇒ xanh.
- **Q8:** sàn pytest **3772 → 3792** *(= số bài thu thập; +20)* ở `tools/dung_moi_truong_isp.sh` + bài ghim `tests/test_dung_moi_truong_isp.py` cùng commit; web giữ 675.

## 6. Cổng
`--duong-nen --cong 5436` MỘT lần (một mình): **KẾT ĐẠT** — toàn bộ tập đỏ + XFAIL **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)*, chạy **3792** (mong ≥ 3792) · skipped 0 · deselected 0; `tests/web` **3 = 3**, chạy 675. Di trú 27/27 · `pg_verify` 0 lệch · HD1 9845/9967. `lint-imports` **11 kept / 0 broken** · `kiem_tai_lieu` ĐẠT *(354 tệp · 2669 bảng)*. Ghi kho THẬT: `KHONG`.
