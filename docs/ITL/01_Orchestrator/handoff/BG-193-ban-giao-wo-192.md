# BG-193 — bàn giao WO-192 · ISP 3.1.2 · Step 23 · DT6: ảnh đáp án GL HR (407·408·413) + CFA3

| | |
|---|---|
| **Phiếu** | trả `WO-192` *(DT6, làn DATA)* |
| **Bởi** | phiên cloud `fls-dev #DATA` · cụm PG **5436** · nhánh `isp/DT6` · 2026-11-18 |
| **Nền** | `fba4849` · commit ① mã+bài+ảnh `515cf37` |
| **Dải phiếu** | `KQ-194` (R1) · `KQ-195` (R2). Số trống kế tiếp: **196** |

## 0. Kết luận
Đóng băng **4 ảnh**: `gl_hr_407` · `gl_hr_408` · `gl_hr_413` · `cfa3` (+ PD 412 ≡ `gl_406`, ⛔ ảnh mới). Khuôn mới ở `tools/khuon_dong_bang/` (`_gl_hr.py` chung + 3 khuôn + `cfa3.py`); **⛔ sửa `dong_bang_sheet.py`** · mọi ảnh DT2…DT8 giữ nguyên. `--duong-nen --cong 5436`: **KẾT ĐẠT**, tập đỏ +0/−0 (toàn bộ 28=28 · web 3=3). lint-imports 11 kept · `kiem_tai_lieu` ĐẠT.
⚠ Lần chạy `--duong-nen` đầu ĐỎ +1 (`test_o_loi::CHI_MOT_BAN_KHAI`: khuôn chép luật `startswith("#")`) ⇒ sửa dùng `la_o_loi`, chạy lại MỘT lần ĐẠT.

## 1. Nguồn (chốt của orchestrator 18/11; AP §3.3.1 "407·408·413 như 406 cho HR")
| PD | Sổ · tab · lưới | Ảnh |
|---|---|---|
| 407 | CF `12S00TnFMd9Uz0g-NLvOA7kdmPPhY1V_SVOQJkDi1ZiU` · `Report I H1000 Ledge (HR Allocate HD) Y2025` · 19238×67 | `gl_hr_407.json` |
| 408 | CF (cùng id) · `… Y2025 \| For PL Report` · 19238×67 | `gl_hr_408.json` |
| 413 | P&L `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` · `… Y2025 \| For PL Report` · 20238×73 | `gl_hr_413.json` |
| 412 | P&L · `Report I General Ledger` | **≡ `gl_406`** — đo A·D·R·BM:BT: **7883/7883** giống từng ô, chỉ-nguồn 0, chỉ-ảnh 0 ⇒ ⛔ ảnh mới |
| CFA3 | CF · `MID I Report I CFA3 Daily` · 99×502 (đọc `A1:SH99`) | `cfa3.json` |

⚠ **Tab cùng tên `Report I General Ledger` ở sổ CF ≠ `gl_406`**: 12.385 hàng có ngày (kỳ tới 2026-11), chỉ 2.243/7.883 hàng giống ảnh, 4.502 hàng chỉ ở nguồn. AP ghi 412 ở "CF report" — nếu BA muốn đáp án 412 theo sổ CF thì cần ảnh riêng (câu hỏi cho BA).
**Errata ISP:** "CFA3 Daily thuộc PD 411 phần CFA3 (DT5 loại) — PD 412·413 trong tiêu đề Step 23 là GL, ⛔ CFA3".
**408 ≠ 413** (đo): 413 ⊃ 408 + **1.375** dòng (2024-11: 165 · 2024-12: 530 · 2025-01: 468 · 2025-04: 212). 407 hơn 408 đúng **11** dòng (LE `#N/A`).

## 2. Số dòng theo kỳ · kỳ ⊂ 2025? *(mỗi số đếm hàng sheet có cột A là ngày)*
**Kỳ ⊄ 2025 — cổng IN `kỳ ⊂ 2025: KHÔNG`, `lac` có tên:**
| Ảnh | Dòng | Kỳ ∈ 2025 | Kỳ ngoài 2025 |
|---|---|---|---|
| 407 | 9.421 | 12 kỳ = 9.152 | 2026-01 = 269 |
| 408 | 9.410 | 12 kỳ = 9.141 | 2026-01 = 269 |
| 413 | 10.785 | 12 kỳ = 9.821 | 2024-11 = 165 · 2024-12 = 530 · 2026-01 = 269 |
407 theo tháng 2025-01…12: 225·667·629·1041·365·916·1685·767·912·868·478·599 (408/413: xem `KY_MONG` trong khuôn). CFA3: **650** ô ≠ 0 trên 74 HD × **496** ngày liên tục 2024-10-20…2026-02-27 (sheet dừng 2026-02-27, cắt 0 cột tương lai); 53/74 hàng HD toàn-0.
**Đoạn A-rỗng** (bảng phụ `doan_trong`, ⛔ vào bảng chính): 407 = 1 đoạn đuôi (9.808 hàng) · 408/413 = 7 đoạn (6 giữa dữ liệu + 1 đuôi). ❓ **Câu cho BA:** 6 đoạn GIỮA ở 408/413 gồm **2.302** hàng A rỗng nhưng còn I/J/F/G/P (sổ có hàng thiếu ngày — nhiều hàng có PS Có) — chưa vào bảng chính vì không gán được kỳ.

## 3. PII
- BỎ khỏi lưới đọc: `B` Số chứng từ · `C` Diễn giải · `M` Mã đối tác (ID Payee) · `N`·`O` file đính kèm. Trong lưới còn `AP` (= bản Final của ID Payee) ⇒ **BỎ**, ⛔ băm *(mã nhân sự băm vẫn là định danh ổn định xuyên kỳ)*; `Q`·`AH`·`AU`·`AV` không cần ⇒ bỏ. **0** cột tên/email trong ảnh.
- **CHE số tài khoản ngân hàng** ở `H`·`Z` (Payment Type `R | <số>_<NH>_<ĐƠN VỊ>`): 407 = 11 ô H + 11 ô Z (cùng 11 hàng LE `#N/A`); 408/413 = 0. Ảnh giữ `R`. *(Tôi đã vô tình thấy các giá trị này khi đo tập khác biệt — không ghi vào đâu.)*
- Mọi cột chữ có **tập đóng** (G 25 · H/Z 2 · I 18 · J/AD 17 · P 5 · V 10 · D 1); giá trị lạ ⇒ ĐỎ, lời lỗi ⛔ in giá trị. Máy quét có ca phá (tên ở J · số TK ở H · tiêu đề `Email Address`).

## 4. Y2024 · ô lỗi
- **Y2024:** hai tab `H1000 Ledge NIS/INT/COM (HR Allocate HD) Y2024` (970 hàng) và `… PIT … Y2024` (413 hàng) = `IMPORTRANGE` ⇒ `#REF!` ×1 mỗi tab, còn lại rỗng ⇒ **`thiếu Y2024`** có tên (bảng phụ `thieu_nguon`, ⛔ suy, ⛔ 0). Ghi chú: sổ P&L (413) lại có 695 dòng 2024-11/12 *(giá trị dán)*.
- **Ô lỗi (NGUYÊN chuỗi, đếm theo cột):** 407 `P` `#N/A` ×11 · 413 `R` `#N/A ()` ×18 · 408 = 0 · CFA3 `"-"` ×5.

## 5. Hiện vật
| Tệp | Byte | `checksum_noi_dung` |
|---|---|---|
| `gl_hr_407.json` | 6.020.461 | `62c6b780950f167a` |
| `gl_hr_408.json` | 6.015.581 | `59e1157d077c51e8` |
| `gl_hr_413.json` | 6.887.920 | `b3b4e8485378ff57` |
| `cfa3.json` | 227.445 | `4e61473a6b526057` |
> 3 ảnh GL **> 2 MB** — nguyên nhân: ~9.4–10.8 nghìn dòng × 19 cột, mỗi ô là một đối tượng có `thu_tu`/kiểu (như `cfa1_daily` 6,8 MB); đã bỏ mọi cột không cần.

Bài: `tests/du_lieu/test_dap_an_gl_hr_cfa3.py` (**27**: tái tạo lưới từ ảnh ⇒ đúng từng byte; ca phá cổng ĐỎ hai chiều; PII; Y2024; AC-4; 412≡406; CFA3). **Sàn pytest 3557 → 3588** (+27; nền thu thập 3.561, lệch 4 so ghim cũ — ghim lại theo số thu thập, web giữ 675) — cùng commit với bài ghim.
Bản thô: chỉ `/tmp/dt6/` (chmod 600) — xoá sau BG, ⛔ commit.
