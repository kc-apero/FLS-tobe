# WO-277 — ISP 3.1.2 · Step 39 · H8: SO.PLA1 (dồn ngày 1 tháng PL start — D4) + SO.PLA3 cộng theo khoá — cổng WP-C3d

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~04:00 UTC; giao sau khi gộp DT7 + DT12 qua `--duong-nen` |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **BE-HC** — phiên cloud **Opus 5.5 · medium** (bước engine, luật A) · nhánh `isp/H8` |
| **Nền** | ngọn nhánh làm việc (đã gộp H4 CA.GL · H5/H6 CFA1 Daily + Y/H/Q/M · **H7** CA.GL dòng HR + SO.CFA3 (WP-C3c) · **C6** IX.PER luật ghi nhận kỳ D4 · **DT7** 6 ảnh đáp án PLA `tests/fixture/dap_an/pla1_* · pla3_hr_* · pla3_pm_hr_*` + `tools/khuon_dong_bang/_pla.py` · CG2 hợp đồng cổng + `lech_co_chu_dich`) |
| **Dải phiếu** | `BG-278` · `KQ-279` (R1) · `KQ-280` (R2 cuối). Số trống kế tiếp sau dải: **281** |

## Vì sao
- ISP **Step 39 · H8** (wave W13) — **đường găng** H7 ✅ → **H8** → H12 → H13 → H14 → I2. Khái niệm mới duy nhất: **ghi nhận kỳ P&L** (D4 A: mọi số vào ngày 1 tháng PL start).

## Đã đo — thay chữ ISP (đọc `BG-262` · `KQ-263` · `KQ-264` · sổ `SO_PHAT_HIEN_ISP-3.1_DT7.md`)
- **Nguồn đáp án** = sổ `[COPY] Report I General Ledger | P&L Report` (chủ đồng ý 22/11; ⛔ sổ CF như ISP/danh mục ghi).
- **Hình đáp án:** 12 khối (`GROUP SGO2 SGO1 HGO6 BGO2` + 7 khối nhãn) × 74 mã HD = 888 hàng; **417 (`pla3_hr_yhqm`) chỉ có khối `GROUP`** ⇒ 46.398 ô Y/H/Q/M HR `khong_so_duoc` — cổng phải khai, ⛔ coi là khớp. Daily: 496 ngày `2024-10-20 … 2026-02-27` (mốc thật của sheet, ⛔ 21/10 như AP — `DT7-R1-07`); Y/H/Q/M: 57 kỳ (2024·2025·2026 × 19).
- **Công thức nguồn (BG-262 §4–5):** `la` (40 mã) PLA1 = `SUMIFS(GL!$BR, GL!$DE, <ngày>, GL!$V, <mã HD>) − SUMIFS(GL!$BS, …)`; PLA3 PM+HR `la` = `PLA1 + HR` **theo khoá (khối, mã HD, ngày)**; `tong` (10 mã) = tổng hàng con; **`kpi` (17 mã) là công thức CHÉO hàng, dấu HR NGƯỢC PM** (vd. 414/418 `EBITDA = G8+G9+G23`, 416/417 `G8−G9−G23`) ⇒ KPI PM+HR ⛔ = KPI PLA1 + KPI HR — engine tính KPI theo công thức của từng tab, ⛔ cộng; `trong` (7 mã) ⛔ có số.
- **Ngoại lệ cần xử lý có tên:** khối `SHQ2` có 40 hàng `la` là công thức dư `=G{GROUP} − SUMIFS(…)` (`DT7-R1-01`); `416`/`417` `TAC`·`CIT` (`GROUP`) ⛔ có công thức (`DT7-R1-04`); `NPC` chiếm 408/510 ô KPI lệch Daily (`DT7-R1-05`).
- **Lệch của AS-IS (tách khỏi lệch FLS — giới hạn ISP mục 3):** Daily **4** ô không-KPI (`GROUP#GAC#45597/45627` · `GROUP#NCFO#45597/45627`), Y/H/Q/M **0**; KPI 510 (Daily) + 206 (Y/H/Q/M) đếm RIÊNG. Khai ở `lech_co_chu_dich` + `mong_lech_co_chu_dich`.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (H8-B1) | dịch vụ PL start `2025-03-15` → end `2025-08` ⇒ **toàn bộ** số vào `2025-03-01` (D4 A, luật C6/IX.PER — dùng lại, ⛔ chép); ⛔ chia đều (D4 B) | đơn vị |
| AC-2 | **ĐẦU VÀO thượng nguồn** cho PLA1 = dòng GL đã qua CA.GL (H4) + cột ngày PL (`DE`) — xác định cột/trường thật trong engine hiện có; PLA3 HR = dòng HR (H7). ⛔ đọc đáp án 414–419 làm đầu vào. Thiếu ảnh đầu vào (vd. cột `DE` ⛔ có trong ảnh GL đầu vào) ⇒ **DỪNG**, báo cần ảnh nào (sổ · tab · vùng · vì sao) + khuyến nghị | BG + pytest |
| AC-3 (H8-B2 · WP-C3d) | `fls/bao_cao/pla.py`: PLA1 · PLA3 HR · PLA3 PM+HR Daily + Y/H/Q/M (Y/H/Q/M qua IX.PER như H6); PM+HR cộng theo **KHOÁ** (khối, mã HD, ngày hoặc kỳ), ⛔ theo vị trí ô; mẫu số khai TRƯỚC kèm nhãn (Đ4: ô so · ô ≠ 0 · `khong_so_duoc` · KPI tách); lệch FLS `mong` hai chiều (Đ5); lệch AS-IS ở `lech_co_chu_dich` | `tools/do_hd2.py --goi WP-C3d` + pytest |
| AC-4 | khối `WP-C3d` trong `hd2_cong.json` theo hợp đồng CG2 (`tong_o`/`khop` = ô khớp THẬT), sinh bằng `do_hd2.py --ghi` ⇒ `/gates` `HD2_WP_C3D` đúng; bài quét tệp thật CG2 + `tests/api/test_isp_gates_hd2.py` xanh | pytest |
| AC-5 | ⛔ vòng tròn: đột biến 1 dòng đầu vào ⇒ đúng ô đáp án tương ứng ĐỎ (PLA1 và HR, cả Daily lẫn Y/H/Q/M); đổi khoá cộng sang vị trí ⇒ ĐỎ | pytest |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ HR qua ALLOCATE (Q3). ⛔ chia đều kỳ PL (D4 B). ⛔ di trú. ⛔ sửa khuôn/ảnh DT7. Ghi kho THẬT: `KHONG`.
- Engine dùng lại H4/H5/H6/H7 (⛔ chép); CDT qua `cdt_cua` (lạ ⇒ lỗi có tên, ⛔ SHQ2 mặc định).
- AP/ISP sai dữ liệu ⇒ đo trước, khai `mong` theo dữ liệu, ghi errata v3.1.3 vào BG.
