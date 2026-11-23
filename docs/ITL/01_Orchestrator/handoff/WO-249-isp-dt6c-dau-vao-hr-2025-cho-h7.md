# WO-249 — ISP 3.1.2 · bổ sung DT6 (DT6c): ảnh ĐẦU VÀO HR 2025 + công thức CFA3 cho H7

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 19/11 ~09:55 UTC |
| **Phát bởi** | orchestrator · 2026-11-19 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT6C` |
| **Nền** | ngọn nhánh làm việc (đã gộp DT6 · DT6b — khuôn `hr_ledger_2024` · ảnh `dau_vao/hr_ledger_2024.json`) |
| **Dải phiếu** | `BG-250` · `KQ-251` (R1) · `KQ-252` (R2) |

## Vì sao
- H7 (`WO-245`) DỪNG đúng luật: ⛔ có ảnh đầu vào HR riêng cho 2025 — ảnh HR duy nhất `hr_ledger_2024` chỉ phủ 2024-11 · 2024-12 · 2025-01 · 2025-04; đáp án `gl_hr_408` phủ 12 kỳ 2025 + 2026-01. ⛔ đọc đáp án làm đầu vào (tiền lệ H4/H5 có ảnh `*_dau_vao` riêng).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | ảnh `tests/fixture/dau_vao/hr_ledger_2025.json` từ file GỐC `H1000 Ledger (APERO-HR Allocate HD_FS1)` `1YEyGxBYXaa6n4dX9_rWXoFn6NgJStTP2DKJd64ZAoD4` — tab `1.3 Ledger NIS/INT/COM 2025` + `1.3 Ledger PIT 2025` (+ `… 2026` cho kỳ 2026-01 nếu cần); MỞ RỘNG khuôn `hr_ledger_2024` (cùng 9 cột `A·D·E·F·G·H·S·T·AG`, cùng cách che — ⛔ chép khuôn); số hàng theo kỳ khai MONG (Đ5 hai chiều; rỗng ⇒ ĐỎ, Đ3) | cổng `--mong` + pytest |
| AC-2 | đối chiếu với `gl_hr_408` (đáp án, chỉ để ĐO — ⛔ đầu vào): số hàng theo kỳ, Σ PS Có theo kỳ khớp/lệch có tên; 2.302 hàng `ky_suy` có NGÀY ở ledger nguồn không (đếm) | BG + pytest |
| AC-3 | đọc CÔNG THỨC chỉ-đọc: một ô lá của `MID I Report I CFA3 Daily` (sổ CF report `12S00Tn…`) + `Report I H1000 Ledge (HR Allocate HD) Y2025 \| For PL Report` ô `A10` · `E10` · `V10` · `BA10` — chép nguyên văn vào BG (⛔ ảnh mới; chỉ ghi) | BG |
| AC-4 | PII như DT6b (che TK cá nhân `R`; ⛔ email/tên; máy quét `tools/quet_pii_repo.py` nếu đã gộp ĐẠT) | pytest |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- Khoá SA CHỈ-ĐỌC (⛔ ghi/nhận xét file của chủ). Bản thô `/tmp` (chmod 600), ⛔ commit. ⛔ sửa mã H7. Ghi kho THẬT: `KHONG`.
