# BG-177 — bàn giao WO-176 · ISP Step 22 · C8 (IX.ORG: CDT/TK → CDT1 + CDT lạ vào hàng chờ)

Nhánh `isp/C8` (nền `ffe06b8`) · cụm PG `5446` · 2 vòng review kế: `KQ-178` (R1) · `KQ-179` (R2).

## AC ↔ bài (ĐỎ trước)
| AC | Bài | Đỏ trước (lệnh: `pytest tests/cau_hinh/test_to_chuc.py tests/cau_hinh/test_to_chuc_pg.py`) |
|---|---|---|
| C8-B1 | `test_to_chuc.py::test_C8_B1_*` (đơn vị) + `test_to_chuc_pg.py::test_C8_B1_CDT_biet_thi_0_su_kien` | exit 2 — `ImportError: cannot import name 'to_chuc'` (module chưa có = THIẾU hành vi) |
| C8-B2 | `test_to_chuc_pg.py::test_C8_B2_CDT_la_ghi_DUNG_MOT_su_kien_va_thay_o_queue` | `2 failed, 12 passed` — `KeyError: 'cdt_la'` ở `GET /queue` (sự kiện ghi được, /queue chưa hiện) |
Xanh sau: `14 passed` (8 đơn vị + 6 pg). Hồi quy `tests/api/test_cua_lenh_cho_pg.py` xanh.

## Thay đổi
`fls/cau_hinh/to_chuc.py` (thuần) · `cau_hinh_repo.py` (`nap_ix_org` · `doc_org` · `cdt_cua_ghi`; bang `IX.ORG` đã có trong `BANG_HOP_LE`, ⛔ di trú mới) · `ghi_tay.ghi_cdt_la` (luật MỘT chỗ ghi `fls_queue_event`) · `/queue` thêm cột `cdt_la` (`doc_bao_cao._SQL_HANG_CHO` + `bang_tuyen` khai `fls_queue_event` + oracle `tools/do_trang_hang_cho.py`, công thức độc lập). Q8: `MONG_PYTEST_TOAN_BO` 3407 → **3421** + bài ghim cùng commit.

## Số đo (Đ4 — nhãn)
`13` dòng ảnh CDT Correct *(ISP ghi 18 = bề vùng sheet)* · `7` CDT1 chuẩn khác nhau *(ISP ghi 8; `CMN` chỉ là nhãn nguồn → SHQ1)* · `69` hàng TK `R |` = `59` pháp nhân (19 mã LE) + `8` `CN` + `2` `Cash Treasury` — chỉ `59` vào kho; `7` hàng `an_danh` loại.

## Cổng
`--duong-nen --cong 5446` (một lần): 1 đỏ MỚI `test_chi_mot_cho_ghi_tay` (do INSERT ngoài `ghi_tay`) → sửa bằng `ghi_cdt_la`; 28 đỏ còn lại = đường nền. ⚠ Sau sửa chạy lại **chỉ** `tests/repo` + `cau_hinh` + ghim (6 đỏ, cả 6 ∈ `duong_nen_bai_do.txt`), ⛔ chạy `--duong-nen` lần hai. `lint-imports` 11/0 · `soi_bang_tuyen` 43 tuyến khớp · `kiem_tai_lieu` ĐẠT · thu thập 3421.
Đỏ có sẵn trên nền (cùng `ffe06b8`): 6 failed + 11 errors ở tập `tests/api`+`tests/repo/wo051`, y hệt trước/sau.

## Giới hạn · quyết cho orchestrator
1. TK→CDT1 **⛔ có trong ảnh** (A:B chỉ TK→LE; AA:AD rỗng) ⇒ `cdt_cua(kho, cdt_nguon)` + `le_cua(kho, tk)` tách đôi.
2. CDT đã là CDT1 chuẩn (`SHQ1 | Headquarters1`) tính là BIẾT dù ⛔ nằm cột nguồn.
3. Sự kiện gắn `itl_id` (bảng bắt buộc FK) ⇒ chỉ dòng ITL có CDT lạ mới ghi được.

## Vòng sửa sau R1 (KQ-178)
`0 CHẶN · 3 NÊN SỬA` ⇒ sửa cả 3; `C8-R1-04…06` ⇒ backlog/orchestrator *(⛔ làm; ⛔ sửa ảnh DT3)*. Commit `c5a89ea`.
| Mã | Sửa | Đỏ trước *(đột biến trên mã gốc; nền `19 passed`)* |
|---|---|---|
| `C8-R1-01` | `test_RIENG_TU_…` ĐỌC hàng `CN`/`Cash Treasury` từ ảnh DT3 lúc chạy *(mẫu số ≥ 4 ≠ 0, Đ3)*; ⛔ chép số TK nào vào bài | M7 *(`_KHONG_PHAI_PHAP_NHAN` rỗng)* ⇒ `3 failed` |
| `C8-R1-02` | bài pg gieo 2 sự kiện `CDT_LA` *(cũ + mới)* cho 1 `itl_id`: `/queue` ra MỚI NHẤT, oracle khớp *(mẫu số 1 hàng ≠ NULL)* | M5 *(lấy CŨ nhất)* ⇒ `1 failed` |
| `C8-R1-03` | `TK_TRUNG` · `TK_RONG` có bài; `nap` từ chối 4 bản rác *(khoá/tiền tố/rỗng)* và số phiên bản ⛔ đổi; `actor` rỗng ⇒ `LoiCauHinh` + 0 sự kiện | M10 *(bỏ `TK_TRUNG`)* · M11 *(bỏ `_kiem_org`)* · M12 *(bỏ chặn `actor`)* ⇒ mỗi cái `1 failed` |
Q8: `MONG_PYTEST_TOAN_BO` **3421 → 3426** *(+5: đơn vị 2 · pg 3)* + bài ghim cùng commit. Quét PII `git diff ffe06b8..HEAD`: **0** chuỗi ≥ 8 chữ số liền trong dòng `+`.
Cổng: `--duong-nen --cong 5446` một lần ⇒ `KẾT: ĐẠT` · `12 failed · 3398 passed · 2 xfailed · 14 errors` = nền **28 = 28** *(thêm 0 · bớt 0)*, chạy 3426 · `tests/web` 3 = 3, chạy 675 · `lint-imports` 11/0.
