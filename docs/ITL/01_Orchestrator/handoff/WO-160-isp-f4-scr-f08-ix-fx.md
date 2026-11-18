# WO-160 — ISP 3.1.2 · Step 18 · F4: SCR-F08 Cấu hình — bảng IX.FX chỉ đọc trên tuyến thật

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 (Sonnet · 2 vòng review) |
| **Phát bởi** | orchestrator · 2026-11-18 |
| **Nhận** | `fls-dev` làn **FE** — phiên cloud **Sonnet 5.5** medium · cụm PG **5436** · nhánh `isp/F4` |
| **Nền** | ngọn nhánh làm việc (đã gộp C5 — `/config/fx` đọc từ kho; O9 — `SCR-F08` đăng ký ở `06_SCREEN_SPEC.md` §9) |
| **Dải phiếu** | `BG-161` · `KQ-162` (R1) · `KQ-163` (R2 cuối). Số trống kế tiếp: **164** |

## Spec
ISP **Step 18** (nguồn sự thật) · `02_BA/06_SCREEN_SPEC.md` §9 `SCR-F08` · `07_API_CONTRACT.md` v3.18 dòng `GET /config/fx` · khuôn màn có sẵn `fls/web/tep/man_f03.js` + `goi_cua.js` · `trang_thai.js` · `thanh_phan.js` · `tokens.css` · bảng tệp `fls/web/phuc_vu.py` (cổng `kiem_bang_tep`) · bài `tests/web` (node headless `tests/web/khung_node.py` + `dom_gia.js`; Chromium thật khi cần đo pixel — luật FG).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 (F4-F1) | mở SCR-F08 trên kho có ảnh FX (`ix_fx.json` nạp qua C5) ⇒ **37** dòng; `202306` mang nhãn **LẠC** | `tests/web/test_isp_f08_fx.py` (headless, pg) — ĐỎ trước |
| AC-2 (F4-F2) | kho thiếu một tháng (dữ liệu test, vd `202408`) ⇒ tháng ấy nhãn **CHẶN**; tháng trùng ⇒ **TRÙNG** | cùng tệp bài |
| AC-3 | bốn trạng thái qua `trang_thai.js` (đang tải · rỗng · lỗi · có số); tuyến lỗi / kho chưa nạp ⇒ trạng thái lỗi có tên, ⛔ bảng trống im lặng | DOM |
| AC-4 (F4-F3) | `kiem_bang_tep` + token màu (`test_khong_ma_mau_go_tay.py`) + một bản mẫu + phím — `tests/web` sẵn có xanh (tập đỏ web = đường nền) | `--duong-nen` MỘT lần cuối |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + `MONG_PYTEST_WEB` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ ký (F5/F7) — vùng ký hiện "chưa xây" theo §9. ⛔ sửa tuyến `/config/fx` (C1/C5 — dùng). ⛔ màu gõ tay.
- Ghi kho THẬT: `KHONG`.
