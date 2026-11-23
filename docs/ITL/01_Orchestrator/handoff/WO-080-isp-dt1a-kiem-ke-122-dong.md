# WO-080 — ISP 3.1.2 · Step 3 · DT1a: HD1 · kiểm kê 122 dòng sổ chưa 1-1 (offline, trên ảnh đóng băng)

| | |
|---|---|
| **Trạng thái** | `MO` *(→ `DANG_LAM` khi orchestrator giao)* |
| **Phát bởi** | orchestrator (phiên điều phối ISP, thay `fls-ba` phát phiếu) · 2026-11-16 |
| **Nhận** | `fls-dev` — agent làn **DATA** · cụm PostgreSQL riêng cổng **5437** |
| **Dải phiếu** | `BG-081` (bàn giao) · `KQ-082` (R1) · `KQ-083` (R2) · `KQ-084` (R3) |
| **Phụ thuộc** | S0 — phải `done` (3 vòng review + gộp) trước khi giao |

## Vì sao
- ISP `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 3 · DT1a** — nguồn sự thật duy nhất của phiếu này (8 trường + Substep 1/2).
- Goal: Một lệnh liệt kê đúng 122 dòng sổ AS-IS chưa ghép 1-1 và 147 dòng FLS chưa có dòng sổ, kèm thuộc tính đo được (kỳ · hd Classifying/MID/Final · pay_type · cdt1), và cổng đỏ khi tổng khác 122 / 147.

## Căn cứ
- Người dùng 16/11: *"Xác nhận các recommend. Xác nhận ISP. Bắt đầu triển khai"* · *"Tự chạy theo wave"*.
- Traceability: AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10 · §2.5.3 · Figure 2.2 hàng BANK.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1.3 · §2.1 · Step 3 · DT1a | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | theo Traceability | 3.1.2 · sha256 `5cf6e576…` |
| `04_Test/review/SO_PHAT_HIEN_ISP-3.1.md` | cột **luật phòng tái phạm** | sống |
| `01_Orchestrator/isp-3.1/TIEN_DO.md` | Quy ước chạy song song | sống |
| `CLAUDE.md` | Đ1–Đ5 · Cổng · Bẫy | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| tool `tools/phan_loai_dong_thieu.py`: tập thiếu = `dong_sheet` của `itl_ledge_adjustment.json` ∖ `dong_so` của `classifying_vs_canon.json`; chiều ngược: 9.992 dòng canon − 9.845 dòng ghép = 147 dòng FLS ⛔ có dòng sổ (chỉ ĐẾM); ghi `docs/ITL/_tools/phan_loai_dong_thieu.json` theo `dong_sheet`, trường `nhan = null` (DT1b điền) | nhãn LÝ DO (cần khoá — DT1b); sửa mã ghép (H3); ký lý do (O8) |

Khái niệm mới duy nhất: kiểm kê tập lệch có cổng · mock/static: không — ảnh đóng băng thật đã có trong repo · tệp chạm: `tools/phan_loai_dong_thieu.py` · `tests/du_lieu/test_phan_loai_dong_thieu.py` · `docs/ITL/_tools/phan_loai_dong_thieu.json`.

## Tiêu chí nghiệm thu *(= test ID của ISP mục 6; exit criteria = mục 8)*
| AC | Mong *(đo được)* | Cách đo | Vì sao đỏ trước thay đổi |
|---|---|---|---|
| AC-1 (`DT1a-B1`) | 122 dòng; 147 chiều ngược; phân bố kỳ có MONG (2026-07: 23 · 2025-11: 14 · 2026-08: 13 …) | chạy tool trên 3 fixture · đơn vị + cổng | tool chưa có |
| AC-2 (`DT1a-B2`) | cổng ĐỎ (123 ≠ 122) rồi trả nguyên (Đ5) | phá nguồn: bỏ 1 dòng khỏi tập ghép (bản sao tạm) · chứng minh đỏ | — |
| AC-3 (`DT1a-B3`) | in 9.967 dòng sổ và 9.845 dòng ghép trước khi in tỷ lệ | mẫu số (Đ3) · đơn vị | — |
| AC-4 (`DT1a-B4`) | 0 khoá `dien_giai` / `so_chung_tu` / `email` | quét PII trên JSON ra · riêng tư | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG` (container ⛔ có sổ thật; `FLS_CHO_GHI_THAT` ⛔ đặt).

## Câu còn treo
- không có.

## Rủi ro
1. Giới hạn đã khai ở ISP: ⛔ gán được LÝ DO: ảnh đã bỏ Số CT · TK · tiền (riêng tư), và mã ghép đã tạo ra 9.845 ⛔ có trong repo (fixture ghi 'đọc LIVE 2026-08-26') — DT1b.
2. Chạy song song với hai làn khác — chỉ chạm tệp của làn mình (`TIEN_DO.md` §Quy ước); ⛔ sửa `08_CHANGELOG_RELEASE.md`, dashboard (orchestrator ghi lúc gộp).
