# WO-295 — ISP 3.1.2 · Step 29 · C10: IX.DRV — driver theo (driver, CDT1, tháng) từ kho config

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~09:55 UTC |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **BE-CF** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/C10` |
| **Nền** | ngọn nhánh làm việc (đã gộp C5 — kho config chỉ-thêm có phiên bản, di trú 0027, `fls/repo/cau_hinh_repo.py` đã có `IX.DRV` trong danh sách bảng · C11 — IX.ALR (khuôn tham chiếu gần nhất) · DT10 — ảnh `tests/fixture/cau_hinh/ix_drv.json`) |
| **Dải phiếu** | `BG-296` · `KQ-297` (R1) · `KQ-298` (R2 cuối). Số trống kế tiếp sau dải: **299** |

## Vì sao — ⚠ bước BỊ RƠI khỏi sổ tiến độ
- Phiên dev H12 (`BG-292`) phát hiện: **C10 ⛔ có trong cây** — grep `IX.DRV` ở `fls/`: chỉ tên bảng ở `cau_hinh_repo.py:64` + chú thích `fls/cau_hinh/__init__.py`; `git log` "C10": 0 commit; ⛔ nhánh `…-isp/C10`; ⛔ phiếu WO/BG nào. Đối chiếu lại: `HANDOFF_ORCHESTRATOR_2026-11-19.md` ghi "34/48" nhưng bảng liệt kê của chính nó chỉ có **33** Step, và C10 vắng ở CẢ danh sách "đã gộp" lẫn "còn lại" ⇒ mọi con số "x/48" từ 19/11 lệch +1 (đính chính ở `TIEN_DO` 22/11).
- H12 hiện dựng lưới driver **thẳng từ ảnh** `ix_drv.json` (⛔ qua kho) ⇒ sau C10, H12 phải đọc qua `driver_cua` (việc của vòng sửa H12, ⛔ của C10).

## Đã đo (đọc `BG-197` (DT10) · `BG-181` (C11))
- Lưới driver thật **3/4 loại × 7/8 CDT1 × 11–12/12 tháng = 238 ô số**; 146 ô thiếu có tên ở phụ `o_thieu`: `NB_LE` 96 (NB khoá theo LE ⛔ CDT1 — ảnh giữ BALANCE ở phụ `nb_le`) · `CMN` 36 (rơi vào phần dư SHQ2) · `GI 202501` 14 (MID3 thiếu `TOTAL 202501`). **Chỉ 2025.** Σ 7 CDT1 = 100 % ± 1e-9 ở 34 tổng.
- NOEM headcount lấy ô cứng H1000 (`A4289:Q4300`) — AP §3.2.4; ⛔ trỏ ô cứng trong mã.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (C10-B1) | nạp `ix_drv.json` vào kho config (bảng `IX.DRV`, chỉ-thêm có phiên bản — dùng lại hàm C5, ⛔ chép); `driver_cua("NOEM", "SHQ1", 202503)` = giá trị ảnh; **238/238** ô số khớp ảnh sau khứ hồi kho (mẫu số trước — Đ3) | pg |
| AC-2 (C10-B2) | tháng/loại/CDT1 ⛔ có driver (202603 · `GI 202501` · `NB_LE` theo CDT1 · `CMN`) ⇒ `DRV_THIEU` CÓ TÊN (loại · CDT1 · tháng · lý do từ `o_thieu`), ⛔ 0, ⛔ trỏ ô cứng H1000; 146/146 ô thiếu ném đúng | đơn vị |
| AC-3 | `GET /api/fls/v1/config/drv` (+ lọc theo kỳ/loại nếu hợp đồng C5 có khuôn chung) theo khuôn tuyến config sẵn có (`/config/fx`, `/config/alr`…); `07_API_CONTRACT` §4i thêm dòng ⬜ (orchestrator lật ✅ khi gộp); `soi_bang_tuyen` khớp SQL thật | api + công cụ |
| AC-4 | NB theo LE (phụ `nb_le`) có đường đọc riêng (`From × To`) hoặc khai rõ là ngoài phạm vi C10 kèm lý do — ⛔ giả làm lưới CDT1 | pytest / BG |
| AC-5 | `.importlinter` khối C5 giữ (11 kept); ⛔ di trú mới (dùng 0027) | `lint-imports` |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ driver 2026 (nguồn ⛔ có) · ⛔ sửa ảnh DT10 · ⛔ sửa engine H12 (bước khác). Ghi kho THẬT: `KHONG` (chỉ kho test).
