# BG-173 — Bàn giao WO-172 · ISP Step 21 · C9 IX.VEN

| | |
|---|---|
| Phát bởi | fls-dev BE-CF · 2026-11-18 · nhánh `isp/C9` (nền `ffe06b8`) |
| Gửi | fls-test (R1) |

## Đã làm
`fls/cau_hinh/vendor.py` (lõi kiểm thuần) · `nap_ix_ven`/`doc_ven` (`cau_hinh_repo.py`, khoá kho = `dong_sheet`, meta `@cdt1`) · `GET /api/fls/v1/config/ven` (`cau_hinh_ven`, bảng tuyến → 38 tuyến, soi KHỚP SQL **44** tuyến-đo). ⛔ di trú mới, ⛔ sửa `07_API_CONTRACT.md`.

## AC ↔ bài · ĐỎ trước
Lệnh đỏ: `pytest tests/cau_hinh/test_vendor.py tests/cau_hinh/test_vendor_pg.py tests/api/test_isp_config_ven.py` (PG 5434) ⇒ **exit 2**, `ImportError: cannot import name 'vendor' from 'fls.cau_hinh'` — đỏ vì THIẾU module/hành vi (chưa có), ⛔ lỗi cú pháp. Sau cài đặt: **40 passed**.

| AC | Bài | Kết |
|---|---|---|
| C9-B1 | `test_vendor_pg.py::test_C9_B1_nap_42_dong_5_ma_dac_biet_7_cdt1` (+ nạp lại · kiểm trước ghi · bản SQL hỏng) · tuyến `test_isp_config_ven.py` | xanh |
| C9-B2 | `test_vendor.py::test_C9_B2_vendor_trung_khoa_loi_CO_TEN` (+ dong_sheet trùng · thiếu/thừa nhãn · CDT1≠7 · tập rỗng · ô hỏng) | xanh |

## Số đo khác ISP (Đ4 — số nào đếm gì)
- **42** DÒNG sheet 4…45 *(ISP 36 = errata `DT8-R1-01`; 36 cũng là số bộ `(vendor,network,account)` khác nhau — bài ghim cả hai)*.
- `pct` **null ở 14/42** dòng (sheet 32…45) ⇒ `pct` cho phép null, có thì > 0.
- **5** nhãn riêng (Max 12 · VD341 12 · VD444 8 · VD428 3 · VD62 1) + `thường` 6 = 42; **7** CDT1 = `cdt1_chuan` khác nhau của `cdt_correct.json`.

## Quyết định cần orchestrator xem
1. ISP "product_id → CDT1" — ảnh `ix_ven.json` ⛔ có cột `product_id`; chỉ có `MappingBlock2.gs` nhân × 7. Làm: kho lưu **danh mục 7 CDT1** (meta `@cdt1`, lấy từ ảnh DT cdt_correct, đòi đúng 7). ⛔ ghép vendor↔CDT1 (H9/H10). Khuyến nghị: giữ.
2. Sửa **một bài cũ** `test_C5R1_05` (`test_kho_cau_hinh_pg.py:289`): dùng `IX.VEN` làm bang mẫu rỗng-kiểm; nay có kiểm riêng ⇒ đổi sang `IX.DRV`. Việc của bài giữ nguyên.

## Sàn Q8 & cổng cuối
`MONG_PYTEST_TOAN_BO` **3407 → 3447** (+40) + bài ghim cùng commit; web 675 giữ.
`--duong-nen --cong 5434` (một lần): chạy **3447**, tests/web ĐẠT; toàn bộ **ĐỎ** vì tập đỏ đo 29 vs đường nền 28 — node thêm = `test_C5R1_05…` (do mục 2, đã sửa; chạy riêng `tests/cau_hinh` + tuyến + `test_dung_moi_truong_isp` ⇒ 265 xanh; ⛔ chạy lại `--duong-nen` lần hai theo lệnh). `lint-imports` 11 kept/0 broken · `soi_bang_tuyen` KHỚP · `kiem_tai_lieu` ĐẠT.
Ghi chú: `CLAUDE.md` còn ghi "37 tuyến" — số sống nay 38 (⛔ sửa ở đây).
