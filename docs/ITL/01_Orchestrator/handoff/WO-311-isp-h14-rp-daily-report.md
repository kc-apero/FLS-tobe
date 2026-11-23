# WO-311 — ISP 3.1.2 · Step 46 · H14: RP.CF · RP.PL · Daily Report 2 · 3 theo bản A-CCR (D5) — cổng WP-C5c

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~14:30 UTC; giao theo tăng tốc ① khi H13 có R1 0 CHẶN (`KQ-309`) |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **BE-HC** — phiên cloud **Opus 5.5 · medium** (bước engine, luật A) · nhánh `isp/H14` |
| **Nền** | ngọn nhánh làm việc **+ nhánh `…-isp/H13`** nếu H13 chưa gộp (tăng tốc ③) · đã gộp: **DT11** (đáp án 607 · 608 · 609 · 610 (DR2) · 605 (DR3 Sign off) · 615 (A-CCR); 616 PDF loại trừ; 614 = `ix_fx`) · **C13** + **C13b** (khi gộp) — IX.TMP bản ký có phiên bản, `dua_ban_ky` · H8 · H12 · C12 · CFA (H5/H6/H7) |
| **Dải phiếu** | `BG-312` · `KQ-313` (R1) · `KQ-314` (R2 cuối). Số trống kế tiếp sau dải: **315** |

## Vì sao
- ISP **Step 46 · H14** (wave W16) — **đường găng** H13 → **H14** → I2. Khái niệm mới duy nhất: **dựng báo cáo theo khuôn**; FS là tham số (D5 A); bản chính thức = A-CCR (D5).

## Đã đo — thay chữ ISP (đọc `BG-270` + `KQ-271/272/286` (DT11) · `BG-258` (C13) · `WO-299`/`BG-300` (C13b) · `BG-308` (H13))
- **Đáp án WP-C5c**: DR3 (605, Sign off, dán giá trị, 8 thực thể × 24 kỳ 2024–2025) · DR2 (610, sổ CF, `ngay` 30 ngày 11/2026 + `luy_ke` + `hr`; cột `AK` ⛔ ngày — `khong_ngay`) · 607 `[FS2]` · 608 `[FS1]` · 609 `5. Daily Report 3` (sổ P&L; 609 `AK` là ngày 31 thật) · 615 A-CCR `5. Daily Report` (11 nhãn TK đã che `TK_CA_NHAN_1…11`). 616 PDF loại trừ có tên.
- **CHECK IX.PL trên đáp án** (DT11): ② `dat_co_so` = **0** ở mọi kỳ (đạt chỉ là 0 = 0) · H13 trên ATL FLS: ① 0·537·147·0 · ② 0·470·214·0 (684 kỳ-khối). ⇒ báo cáo thừa kế; ⛔ gọi 0 = 0 là "đạt".
- **Ô chỉnh tay**: ATL `AH12` `−0.5` (`chinh_tay_ATL_AH12` trong ảnh DR3) · OMC 2025-02 −0,5 · SHQ2 dư −0,5 (H12 `loi_as_is` 29) ⇒ liệt kê có tên "chỉnh tay ⛔ actor", ⛔ chép vào config (ISP mục 3).
- **Lớp lệch thừa kế** từ ATL/PL: `loi_as_is` · `lech_D3` · `chua_co_dau_vao` (H12/H13) — lan sang ô báo cáo bằng truy ngược thật (bài học `H12-R1-01`).
- **Câu chủ đang mở**: CHECK đỏ có chặn đóng sổ không (H13 hỏi) — ⛔ tự quyết; cổng H14 chỉ đếm và liệt kê.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (H14-B1 · WP-C5c) | `fls/bao_cao/bao_cao.py` `daily_report(ky, fs)` dựng Daily Report 2 · 3 (+ RP.CF · RP.PL) theo khuôn; so đáp án 605 · 607–610 · 615 TỪNG Ô; **ô so > 0** (Đ3) cho từng đáp án; mẫu số khai TRƯỚC kèm nhãn Đ4; lệch `mong` hai chiều theo lớp thừa kế; ô chỉnh tay liệt kê có tên | `do_hd2.py --goi WP-C5c` + pytest |
| AC-2 (H14-B2) | FS = FS1 / FS2 / FS3 cùng một engine, khác tham số (D5 A) — bài chứng minh (đổi FS ⇒ đúng khối đổi, phần chung giữ) | đơn vị |
| AC-3 | đầu ra là **JSON ô theo hợp đồng C13** (đưa được vào `dua_ban_ky`); bài: đưa bản H14 vào kho test ⇒ phiên bản mới, checksum ổn định (chạy 2 lần cùng đầu vào ⇒ `khong_doi`) | pytest |
| AC-4 | ⛔ vòng tròn: đầu vào = đầu ra engine (ATL/PL H12–H13, CFA H5–H7, GL), ⛔ đọc đáp án 605–615; đột biến 1 ô đầu vào ⇒ đúng ô báo cáo ĐỎ | pytest |
| AC-5 | khối `WP-C5c` trong `hd2_cong.json` theo hợp đồng CG2 (`khop` = ô khớp THẬT), sinh bằng `do_hd2.py --ghi`; `/gates` `HD2_WP_C5C` + cha `HD2_WP_C5` | pytest |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ ghi CCR / PDF (HD4 — ngoài ISP) · ⛔ chép ô chỉnh tay vào config · ⛔ sửa engine H8–H13 / C13 (dùng lại). Ghi kho THẬT: `KHONG`.
- Thiếu đầu vào cho một báo cáo ⇒ DỪNG phần ấy, báo cần ảnh nào (tiền lệ DT7b), ⛔ đọc đáp án làm đầu vào.
