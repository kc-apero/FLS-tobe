# WO-216 — ISP 3.1.2 · Step 28 · H10: AL.PLT · 5 vendor đặc biệt theo cột 'cách tính' — cổng WP-C4b

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 19/11 ~01:40 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-19 |
| **Nhận** | `fls-dev` làn **BE-HC** — **phiên cloud** (Opus 5.5 · medium — bước engine khó, quyết của chủ 18/11) · cụm PG **5444** · nhánh `isp/H10` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp H9 + DT8b: `fls/bao_cao/phan_bo.py` `chia_nen_tang` · `ks_al`; cổng WP-C4a; ảnh `gi_mid1/2/3.json` · `gi_cfa1.json` · `ix_ven.json`) |
| **Dải phiếu** | `BG-217` · `KQ-218` (R1) · `KQ-219` (R2). Số trống kế tiếp: **220** |

## Vì sao
- ISP **Step 28 · H10** (wave W10). Phụ thuộc H9 (đã gộp). Khái niệm mới: **tính theo mã cấu hình**.
- ⭐ Mang theo từ H9 (`BG-201` mục "Chuyển H10", backlog `H9-R1-03…-05`): dữ liệu thật — MỌI ô ≠ 0 của MID3 thuộc vendor ĐẶC BIỆT (PE ≠ 0 trên 165/165 Vendor-tháng của 15 vendor; 44 Vendor-tháng thường toàn 0). ⇒ **H10 là nơi DUY NHẤT chứng minh RATE trên số thật.**
- Cấu trúc MID3 đo ở H9 (⛔ đầu vào): mỗi khối tháng = 22 hàng = 1 tổng tháng + 1 tổng nhóm `Max` + 12 hàng nhóm `Max` (RATE chung, khớp RATE MID2 tới `1e-9`) + 1 tổng nhóm VD341 · VD428 · VD444 + 3 hàng ấy + 4 hàng vendor thường (O = 0).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 28** (· Step 24 H9) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.2.2 IX.VEN · §3.2.4 ('VD341 · VD444 · VD428 · Max · VD62 tính riêng') · §3.4.1 PD 501–507 · §3.5.4 WP-C4 | 3.1.2 |
| `BG-201` · `KQ-202` · `KQ-203` · `BG-205` · sổ `SO_PHAT_HIEN_ISP-3.1_H9.md` | bàn giao + backlog H9 | nền |
| `CLAUDE.md` | Đ1–Đ5 | — |

## Đầu vào PE theo CDT1 — orchestrator chốt
- Nguồn AS-IS là Looker (PD 502). Thử theo thứ tự: ① cột PE theo CDT1 đã có trong ảnh `gi_mid1.json` (MID1 là tầng THƯỢNG NGUỒN của MID3 — dùng làm đầu vào ⛔ là vòng tròn NẾU MID1 ⛔ tính từ MID3; ĐO bằng `FORMULA` của sheet MID1 — công cụ SA `sa_cong_thuc.py` — và khai); ② nếu MID1 ⛔ mang đủ PE theo CDT1 ⇒ đọc công thức MID2/MID3 xem RATE lấy từ đâu và đề xuất ảnh cần thêm (tab + vùng) — **DỪNG và báo** (⛔ đoán, ⛔ đọc MID3 thay).
- Công thức riêng từng mã 'cách tính': đọc NGUYÊN VĂN bằng `FORMULA` (khoá SA chỉ-đọc: env `FLS_GSHEETS_SA_JSON_B64`/`FLS_GSHEETS_SA_JSON`; `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`; python `-I`; bản thô `/tmp`, ⛔ commit; ⛔ đọc cột PII) và chép vào chú thích.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (H10-B1) | bảng hàm theo mã 'cách tính' của IX.VEN (5 mã); mỗi mã một ca tổng hợp đúng tay tính; mã lạ ⇒ lỗi có tên | `tests/bao_cao/test_vendor_dac_biet.py` | chưa có |
| AC-2 (H10-B2) | grep tên vendor (`VD341` · `VD444` · `VD428` · `Max` · `VD62`) trong `fls/bao_cao` = **0** (Đ1: dán số đếm `fls/` + `tools/`) | kiến trúc | — |
| AC-3 (H10-B3 · WP-C4b) | cổng khớp MID3 GI đủ mọi vendor (165 Vendor-tháng đặc biệt + 44 thường); mẫu số khai TRƯỚC kèm nhãn Đ4 (ô so · ô ≠ 0 · ô ⛔ so được + lý do); lệch khai `mong` hai chiều (Đ5); vendor bỏ qua = **0** | `tools/do_hd2.py --goi WP-C4b` + pytest | — |
| AC-4 | KS.AL chạy trên 165 Vendor-tháng đặc biệt: Σ chia = O/P (lệch khai) | pytest | — |
| AC-5 | backlog H9: `-04` ("tổng tháng" tính cả vendor đặc biệt? `P < 0`?) — trả lời bằng công thức AS-IS đo được, khai trong BG; `-05` so GIÁ TRỊ (⛔ chỉ đếm) | BG + pytest | — |
| AC-6 | ⛔ vòng tròn: đột biến 1 ô đầu vào ⇒ đúng ô MID3 tương ứng ĐỎ | pytest | — |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Ràng buộc
- ⛔ `if` theo tên vendor. ⛔ vendor mới. ⛔ di trú. Ghi kho THẬT: `KHONG`. `tools/do_hd2.py`: thêm gói `WP-C4b`, giữ nguyên các gói cũ (CG2 đọc `hd2_cong.json` — gói con mới tự hiện).

## Câu còn treo
- không có.
