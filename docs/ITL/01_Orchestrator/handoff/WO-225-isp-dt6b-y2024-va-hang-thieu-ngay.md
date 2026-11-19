# WO-225 — ISP 3.1.2 · bổ sung DT6 (DT6b): Y2024 HR từ file gốc + gán kỳ cho 2.302 hàng thiếu ngày

| | |
|---|---|
| **Trạng thái** | `MO` — giao khi có chỗ (≤ 3 phiên) |
| **Phát bởi** | orchestrator · 2026-11-19 · theo quyết của chủ 19/11 ~04:20 UTC |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT6B` |
| **Nền** | ngọn nhánh làm việc (đã gộp DT6: `gl_hr_407/408/413.json` · `cfa3.json` · khuôn `tools/khuon_dong_bang/_gl_hr.py`) |
| **Dải phiếu** | `BG-227` · `KQ-228` (R1) · `KQ-229` (R2) |

## Quyết của chủ (19/11)
1. **Y2024:** file GỐC `H1000 Ledger (APERO-HR Allocate HD_FS1)` id `1YEyGxBYXaa6n4dX9_rWXoFn6NgJStTP2DKJd64ZAoD4` — đã share SA (quyền nhận xét; dùng CHỈ-ĐỌC). Orchestrator đo: tab `1.3 Ledger NIS/INT/COM 2024` 969 hàng có ngày (2024-11: 165 · 2024-12: 536 · 2025-01: 268), `1.3 Ledger PIT 2024` 412 hàng (2025-01: 200 · 2025-04: 212). Bản `[COPY]` cùng tên chỉ ra `#REF!` (IMPORTRANGE gãy).
2. **2.302 hàng thiếu ngày** (6 đoạn ở 408/413: hàng sheet 5221 · 6546 · 8163 · 9023 · 10113 · 10919; 566 + 335 + 322 + 538 + 276 + 265): **gán kỳ theo kỳ của hàng CÓ NGÀY liền TRÊN** (chủ chọn phương án 2).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | ảnh ĐẦU VÀO Y2024 `tests/fixture/dau_vao/hr_ledger_2024.json` từ 2 tab của file gốc; số hàng theo kỳ khai MONG = số trên (Đ5 hai chiều); ⛔⛔ PII: bản đồ cột bằng hàng tiêu đề TRƯỚC — ⛔ `Số chứng từ` · `Diễn giải` · tên người · email · số TK cá nhân (che như DT6: `R`) | cổng `--mong` + pytest |
| AC-2 | đối chiếu Y2024 với 695 + 680 dòng kỳ 2024-11/12 · 2025-01/04 đang có ở `gl_hr_413` (P&L dán giá trị): khai số khớp/lệch theo kỳ (DT6 đo 413 − 408 = 1.375 = 165 · 530 · 468 · 212) — lệch có tên (vd 2024-12: 536 vs 530) | BG + pytest |
| AC-3 | 2.302 hàng: kỳ = kỳ của hàng có ngày liền trên (cùng tab); bảng chính nhận các hàng ấy với cờ `ky_suy = "hang_tren"`; ĐẾM theo kỳ + Σ PS Có (mong 6.763.528.503) khai MONG; ảnh cũ đổi ⇒ khai từng ảnh + lý do, checksum ghim cập nhật CÓ CHỦ ĐÍCH | pytest |
| AC-4 | khuôn: sửa `_gl_hr.py` chỉ phần `doan_trong` → gán kỳ; mọi ảnh khác (DT2…DT10) đúng từng byte | diff |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- Khoá SA CHỈ-ĐỌC (⛔ ghi/nhận xét lên file của chủ). Bản thô `/tmp` (chmod 600), xoá sau dùng, ⛔ commit. Ghi kho THẬT: `KHONG`.
