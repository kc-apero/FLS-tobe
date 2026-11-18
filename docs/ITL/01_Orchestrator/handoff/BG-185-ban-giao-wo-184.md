# BG-185 — Bàn giao WO-184 · ISP 3.1.2 · Step 26 · C12 (IX.PL)

| | |
|---|---|
| **Từ → Đến** | fls-dev (làn BE-CF, Sonnet 5.5) → fls-test (R1) |
| **Nhánh** | `isp/C12` ⇒ `claude/bold-galileo-zukpaf-isp/C12` · commit ① mã+bài `11effec` |
| **Kết** | mã xong; 3 bài AC xanh; `--duong-nen` ĐẠT (tập đỏ 28 = 28) |

## Làm gì
- `fls/cau_hinh/dong_pl.py`: bộ phân tích `+ − ( )` + dấu đơn ngôi (token→cây→cộng/trừ, ⛔ `eval`/`exec`/`compile` — bài quét AST). `DINH_NGHIA` (PL2…PL8, bản ATL), `tinh_pl`, `check_pl`, `kiem_dinh_nghia`, `CHENH_VOI_MM`. Lỗi có TÊN, gom hết: `PL_CU_PHAP · PL_MA_LA · PL_CHU_TRINH · PL_THIEU_GIA_TRI` (thiếu giá trị ⇒ lỗi, ⛔ ngầm 0).
- `fls/repo/cau_hinh_repo.py`: `nap_ix_pl`/`doc_pl` + `_kiem_pl` trong `_kiem_noi_dung` (kiểm TRƯỚC khi ghi, luật `C5-R1-04`). Dùng bảng `IX.PL` đã có trong `BANG_HOP_LE`, di trú `0027` có sẵn ⇒ ⛔ di trú mới.
- Q8: `MONG_PYTEST_TOAN_BO` 3466 → **3500** (+ bài ghim, cùng commit).

## AC — đỏ trước
Lệnh đỏ: `pytest tests/cau_hinh/test_dong_pl.py tests/cau_hinh/test_dong_pl_pg.py` → exit 2, `ImportError: cannot import name 'dong_pl'` (thiếu module = thiếu hành vi, ⛔ lỗi cú pháp/setup). Sau mã: 34 xanh.

| ID | Bài | Đỏ trước | Nay |
|---|---|---|---|
| C12-B1 | `test_C12_B1_*` (7 dòng tay tính 900/840/800/750/700/640/600 · cú pháp · định nghĩa ∈ cây 74 nút · CHÊNH) | ĐỎ | xanh |
| C12-B2 | `test_C12_B2_*` (18 mẫu độc hại `__import__`… · mã lạ · chu trình · thiếu giá trị · AST) | ĐỎ | xanh |
| C12-B3 | `test_C12_B3_*` (cân ⇒ cả hai đúng · NB lệch 1 ⇒ phép NB · GAH lệch 1 ⇒ phép 2, chênh −1 · thiếu giá trị) | ĐỎ | xanh |
| kho | `test_dong_pl_pg.py` (3: nạp/đọc 7 dòng · biểu thức hỏng ⇒ không thêm phiên bản · mã lạ) | ĐỎ | xanh |

Đ5 — phá thử 3 nhánh, bài ĐỎ rồi trả nguyên: bỏ kiểm mã∈cây (1 đỏ) · `dat=True` (2 đỏ) · bỏ dò chu trình (1 đỏ). Đ3: mọi phép có mẫu số ≠ 0 (7 dòng · 2 phép · vế 125 ≠ 0).

## Cổng cuối
- `--duong-nen --cong 5446`: chạy 3500 bài (mong ≥ 3500) · 12 failed + 14 errors + 2 xfail ⇒ **tập đỏ 28 = 28 node id** (thêm 0 · bớt 0) ⇒ ĐẠT.
- `lint-imports`: 11 kept, 0 broken · `soi_bang_tuyen`: 44/44 ĐẠT · `kiem_tai_lieu`: ĐẠT (không tuyến mới ⇒ ⛔ chạm `07_API_CONTRACT.md`).

## Cho R1 / owner (giới hạn — ⛔ tự hoà giải)
1. **Nguồn `DINH_NGHIA`**: ảnh ATL chỉ giữ LỜI MÔ TẢ chữ (`ten`); công thức mã lấy từ hàng "606" của ISP/AP (PL2 = GI−OMC · PL3 = PL2−API−SC−LC · …). **Chưa đối chiếu với công thức ô ATL gốc** — cần owner/BA xác nhận.
2. **Chênh ATL ↔ MM (1 mục)**: `PL3` có `LC` ở ATL; mô tả MM ("server, API.. + Tools") ⛔ nêu License. Liệt kê ở `CHENH_VOI_MM`.
3. Chưa nối engine H13 / tuyến; `nap_ix_pl` chưa được gọi từ đâu ngoài bài (đúng phạm vi mục 7).
