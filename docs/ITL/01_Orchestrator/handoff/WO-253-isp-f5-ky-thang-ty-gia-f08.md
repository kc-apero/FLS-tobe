# WO-253 — ISP 3.1.2 · Step 37 · F5: SCR-F08 ký tháng tỷ giá (D1) có hộp xác nhận

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 19/11 ~10:55 UTC |
| **Phát bởi** | orchestrator · 2026-11-19 |
| **Nhận** | `fls-dev` làn **FE** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/F5` |
| **Nền** | ngọn nhánh làm việc (đã gộp F4 — `man_f08.js` SCR-F08 xem tỷ giá; C7 — `POST /api/fls/v1/config/fx/{yyyymm}/sign`: `actor` từ thẻ, `201`/`409`/`400`, `FX_CHAN` có câu tiếng Việt trong `goi_cua.js`) |
| **Dải phiếu** | `BG-254` · `KQ-255` (R1) · `KQ-256` (R2) |

## Vì sao
- ISP **Step 37 · F5** (wave W12). Khái niệm mới: **hành động ghi từ màn cấu hình**. Mở đường F7 (Step 40). Chủ hỏi 19/11 về luồng FE cơ bản — F5 hoàn tất màn F08 (xem + ký).

## Spec phải đọc
| Tệp | Mục |
|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | **Step 37** (· Step 18 F4 · Step 33 C7) |
| `02_BA/06_SCREEN_SPEC.md` §9 `SCR-F08` · `02_BA/13_THUYET_MINH_MAN_HINH.md` (mục F08) · `02_BA/07_API_CONTRACT.md` §1 + §4i dòng `POST …/sign` | hợp đồng màn + tuyến |
| `fls/web/tep/man_f08.js` · `hop_thoai.js` · `goi_cua.js` · bài `tests/web/` của F4 | khuôn |
| `CLAUDE.md` | Đ1–Đ5 |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (F5-F1) | bấm 'Ký tháng' ở tháng chưa ký ⇒ hộp xác nhận (`hop_thoai.js`) ⇒ xác nhận ⇒ `POST …/sign` ⇒ tháng hiện 'đã ký · người ký (từ thẻ) · ngày' và nút khoá | tích hợp headless (pg) |
| AC-2 (F5-F2) | ký lại ⇒ chữ lỗi 409 tiếng Việt (⛔ mã thô) | tích hợp |
| AC-3 (F5-F3) | huỷ ở hộp xác nhận ⇒ ⛔ gọi POST (đếm request) | DOM |
| AC-4 | mã lỗi 400/401/403/409 + `FX_CHAN` có chữ — bài `test_goi_cua_phu_het_ma_loi.py` xanh | pytest web |
| AC-5 | ⛔ gửi `actor` trong thân (cửa trả 400) | DOM/tích hợp |
| AC-6 | `kiem_thuyet_minh.py` ĐẠT (cập nhật thuyết minh F08 nếu thêm nút) | công cụ |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` (+ `MONG_PYTEST_WEB`) + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ huỷ ký · ⛔ phân quyền theo vai (O11). ⛔ đổi tuyến BE. Ghi kho THẬT: `KHONG` (chỉ kho test).
