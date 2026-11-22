# WO-291 — ISP 3.1.2 · Step 42 · H12: AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS (D2) — cổng WP-C5a

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~08:55 UTC; giao theo chế độ tăng tốc ① (H8: `BG-278` + R1 `KQ-279` 0 CHẶN; R2 cuối `KQ-280` đang chạy) |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **BE-HC** — phiên cloud **Opus 5.5 · medium** (bước engine, luật A) · nhánh `isp/H12` |
| **Nền** | ngọn nhánh làm việc **+ gộp cục bộ nhánh `…-isp/H8`** (chưa gộp — tăng tốc ③) · đã gộp: H11 (AL.PLT OMC · SC · PS) · C10 (IX.DRV driver theo (driver, CDT1, tháng)) · C11 (IX.ALR luật có hiệu lực theo kỳ, cờ mặc định TẮT — D2) · DT10 (ảnh `tests/fixture/cau_hinh/ix_drv.json` + đáp án `tests/fixture/dap_an/atl.json`) |
| **Dải phiếu** | `BG-292` · `KQ-293` (R1) · `KQ-294` (R2 cuối). Số trống kế tiếp sau dải: **295** |

## Vì sao
- ISP **Step 42 · H12** (wave W14) — **đường găng** H8 → **H12** → H13 → H14 → I2. Khái niệm mới duy nhất: **phân bổ theo khoá driver có cờ**.

## Đã đo — thay chữ ISP (đọc `BG-197` (DT10) · `BG-181` (C11) · `BG-278` + `KQ-279` (H8) · `BG-235` (H11))
- **Đầu vào của AL.KEY** = đầu ra SO.PLA3 PM+HR của H8 (`fls/bao_cao/pla.py`, 12 khối × 74 mã HD, Daily + Y/H/Q/M) — ⛔ đọc ảnh đáp án PLA làm đầu vào.
- **Đáp án ATL (PD 606)** = `atl.json` từ tab `Report I PLA3 Y H Q M | PM + HR | ATL` (1110 × 196) `B5:BK1110` sổ P&L. Lưới driver IX.DRV (PD 604) **3/4 loại × 7/8 CDT1 × 11–12/12 tháng = 238 ô số**; 146 ô thiếu có tên (`NB_LE` 96 — NB khoá theo LE ⛔ CDT1 · `CMN` 36 — rơi vào phần dư SHQ2 · `GI 202501` 14 — MID3 thiếu `TOTAL 202501`). **Chỉ 2025** có driver ⇒ kỳ 2026 chỉ đối chiếu ở cờ tắt (ISP mục 3).
- **Lệch AS-IS đã biết ở đầu vào** (từ H8, `lech_co_chu_dich` WP-C3d): 72 cột 2024 của 416 (bản dán cũ) lan sang 418/419 · `GAC` 416 sót `CXA` (8 ô) — nếu lan sang ATL ⇒ khai lệch AS-IS có tên (⛔ chép lỗi vào engine).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (H12-B1) | mọi cờ IX.ALR TẮT (mặc định C11) ⇒ `phan_bo_khoa()` trả **đúng** PLA3 PM+HR từng ô (đồng nhất) — so 100 % ô, mẫu số khai trước (Đ3) | đơn vị |
| AC-2 (H12-B2) | bật cờ "by NOEM" trên **dữ liệu TỔNG HỢP** (⛔ dữ liệu thật — D2, owner ký): Σ chia = tiền (|Δ| ≤ dung sai khai), chia đúng tỉ lệ driver; driver thiếu ô có tên (146) ⇒ lỗi/lệch có tên, ⛔ hoá 0 | đơn vị |
| AC-3 (H12-B3 · WP-C5a) | cổng `WP-C5a` khớp ATL 606 (và tham chiếu 604) theo ô; mẫu số khai TRƯỚC kèm nhãn Đ4 (ô so · khớp · lệch FLS · lệch AS-IS · `khong_so_duoc`); lệch `mong` hai chiều (Đ5); khối `hd2_cong.json` theo hợp đồng CG2 (`khop` = ô khớp THẬT, `lech_co_chu_dich`), sinh bằng `do_hd2.py --ghi`; `/gates` `HD2_WP_C5A` đúng; bài CG2 + `tests/api/test_isp_gates_hd2.py` xanh | `do_hd2.py --goi WP-C5a` + pytest |
| AC-4 | ⛔ vòng tròn: đột biến 1 ô đầu vào PLA3 ⇒ đúng ô ATL tương ứng ĐỎ; đột biến 1 ô driver (khi bật cờ tổng hợp) ⇒ phân bổ đổi đúng chỗ | pytest |
| AC-5 | cờ đọc từ IX.ALR (C11, có hiệu lực theo kỳ) qua repo/kho config — ⛔ hằng trong mã; thiếu luật ⇒ lỗi có tên | pytest |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ bật cờ trên dữ liệu thật · ⛔ di trú · ⛔ sửa engine H8/H11 (dùng lại) · ⛔ sửa ảnh DT10. Ghi kho THẬT: `KHONG`.
- Engine thiếu đầu vào (vd. ATL cần cột/tab chưa đóng băng) ⇒ **DỪNG**, báo cần ảnh nào (sổ · tab · vùng · vì sao) + khuyến nghị (tiền lệ DT7b), ⛔ đọc đáp án làm đầu vào.
- AP/ISP sai dữ liệu ⇒ đo trước, khai `mong` theo dữ liệu, ghi errata v3.1.3 vào BG.
