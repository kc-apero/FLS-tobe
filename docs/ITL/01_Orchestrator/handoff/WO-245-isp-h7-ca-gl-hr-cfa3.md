# WO-245 — ISP 3.1.2 · Step 32 · H7: CA.GL dòng HR + SO.CFA3 — cổng WP-C3c

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 19/11 ~09:10 UTC |
| **Phát bởi** | orchestrator · 2026-11-19 |
| **Nhận** | `fls-dev` làn **BE-HC** — phiên cloud **Opus 5.5 · medium** (bước engine) · nhánh `isp/H7` |
| **Nền** | ngọn nhánh làm việc (đã gộp H4 CA.GL · H5 CFA1 Daily · H6 Y/H/Q/M · C8 IX.ORG `cdt_cua` · DT6 + DT6b ảnh GL HR 407/408/413 + CFA3 + Y2024 · alias ITE · CG2 hợp đồng cổng có `lech_co_chu_dich`) |
| **Dải phiếu** | `BG-246` · `KQ-247` (R1) · `KQ-248` (R2) |

## Vì sao
- ISP **Step 32 · H7** (wave W11). Khái niệm mới: không (dùng lại H1/H4/H5 cho họ HR). Mở đường H8 (SO.PLA1/PLA3).

## Đã đo — thay chữ ISP (đọc `BG-193` · `BG-227` · `KQ-194/195/228/229`)
- Đáp án GL HR: `gl_hr_407` (9.421 dòng) · `gl_hr_408` (11.712 = 9.410 + 2.302 hàng `ky_suy = "hang_tren"`) · `gl_hr_413` (13.087). Kỳ ⛔ ⊂ 2025 (2026-01 có 269 dòng; 413 có 2024-11/12) — ISP "chỉ Y2025" ⇒ khai tập kỳ đo được, kỳ ngoài 2025 có tên.
- Y2024: ĐẦU VÀO `dau_vao/hr_ledger_2024.json` (1.381 hàng) — đáp án 2024 chỉ có ở 413 (dán giá trị; khớp 165/165 · 530/536 · 468/468 · 207/212, lệch có tên ở BG-227).
- CFA3: `cfa3.json` 650 ô ≠ 0, 74 HD × 496 ngày (2024-10-20 → 2026-02-27).
- 412 ≡ `gl_406` (⛔ đáp án riêng).
- 2.302 hàng thiếu ngày đã gán kỳ (`ky_suy`) — cột `BA`·`BB` (mUSD) nới `so?` cho các hàng ấy.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (H7-B1 · WP-C3c) | CA.GL chạy trên dòng họ HR (đầu vào: ⛔ đọc đáp án — xác định nguồn ĐẦU VÀO HR thượng nguồn như H5 làm với `gl_cf_dau_vao`; nếu ảnh đầu vào HR ⛔ có ⇒ DỪNG báo ảnh cần thêm) và SO.CFA3 dựng theo khuôn CFA1 (H5/H6 — một nguồn sự thật, ⛔ chép); cổng khớp đáp án GL HR (407/408/413 — chọn đáp án chính, khai) + CFA3; mẫu số khai TRƯỚC kèm nhãn Đ4; lệch `mong` hai chiều (Đ5) | `tools/do_hd2.py --goi WP-C3c` + pytest |
| AC-2 (H7-B2) | CDT lạ trong dòng HR ⇒ lỗi có tên qua `cdt_cua` (⛔ SHQ2; ⛔ CDT Correct mặc định) | đơn vị |
| AC-3 | hàng `ky_suy` (2.302) xử lý có khai (vào kỳ suy; ô `BA`/`BB` rỗng ⇒ ⛔ quy đổi được ⇒ lệch/loại có tên, ⛔ hoá 0) | pytest |
| AC-4 | khối `WP-C3c` trong `hd2_cong.json` theo hợp đồng CG2 (`tong_o`/`khop` = ô khớp THẬT; `lech_co_chu_dich` nếu có) ⇒ `/gates` `HD2_WP_C3C` đúng; bài quét tệp thật CG2 xanh | pytest |
| AC-5 | ⛔ vòng tròn: đột biến 1 ô đầu vào ⇒ đúng ô đáp án tương ứng ĐỎ | pytest |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ HR qua ALLOCATE (Q3). ⛔ di trú. Ghi kho THẬT: `KHONG`.
