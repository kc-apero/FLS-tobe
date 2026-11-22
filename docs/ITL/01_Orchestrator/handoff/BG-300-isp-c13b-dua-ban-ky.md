# BG-300 — Bàn giao WO-299 · ISP C13b · `dua_ban_ky` / `ky_ban` trả ĐÚNG phiên bản

| | |
|---|---|
| Phát bởi | fls-dev #CF (phiên cloud) · 2026-11-22 · nhánh `isp/C13B` (nền `b3ab9cc`) |
| Gửi | fls-test (R1 → `KQ-301` · R2 cuối → `KQ-302`) |

## Gốc lỗi (đo, ⛔ đoán)
`fls/repo/cau_hinh_repo.py`: cả `dua_ban_ky` lẫn `ky_ban` chèn TRONG `conn.transaction()` giữ `pg_advisory_xact_lock`, nhưng **trả** `_sk_ban_ky(conn,k)[-1]` SAU khi khối kết thúc ⇒ khoá đã nhả ⇒ luồng khác chèn `n+1` kịp ⇒ hàm trả bản CỦA LUỒNG KHÁC. **`ky_ban` CÓ cùng lỗi** (ký xong, trả bản mới `chua_ky` của luồng khác).

## Đã làm
- Sửa: đọc bản vừa chèn/ký **trong** khối còn giữ khoá (`moi`/`da_ky` gán trong `with`, trả sau). ⛔ đổi khoá advisory · tuyến · hợp đồng `report/snapshot` · di trú.
- +3 bài `tests/cau_hinh/test_ban_ky_pg.py`:
  - `test_C13B_AC2_dua_ban_ky_tra_DUNG_ban…` và `test_C13B_AC1_ky_ban_tra_DUNG_ban…` — **ép đua TẤT ĐỊNH**: patch `chc._sk_ban_ky`; khi kết nối đang `IDLE` (= sau khối giữ khoá) thì một kết nối khác chèn bản `n+1`. **ĐỎ trên mã cũ** (`dua_ban_ky` trả `phien_ban=3`/checksum luồng khác; `ky_ban` trả `phien_ban=2 chua_ky` thay vì `1 da_ky`) ⇒ **xanh sau sửa**. Mẫu số: danh sách `da_chen` (mã mới ⇒ rỗng vì không còn điểm giữa; mã cũ ⇒ 1 lần chèn).
  - `test_C13B_AC1_…khong_doi_dung_ban` — trùng checksum vẫn trả đúng bản `khong_doi=True`.
- Q8: `MONG_PYTEST_TOAN_BO` 4534 → **4537** (= thu thập thật `4537 tests collected`) + bài ghim cùng commit (web giữ 690).

## AC-3 · 50 lần dưới tải
Lệnh: 4 tiến trình song song × 13 vòng `pytest tests/cau_hinh/test_ban_ky_pg.py::test_C13_R1_02_dua_ban_SONG_SONG_… -p no:cacheprovider`, mỗi tiến trình **kho test riêng** (`PG_DSN_TEST=…/fls_test_w1…w4`) ⇒ **52 lần · 52 pass · 0 đỏ** (mẫu số: 52 tệp log, 52 dòng `1 passed`).
⚠ Bẫy đo: `conftest` mỗi tiến trình `DROP/CREATE` `fls_test` ⇒ 4 tiến trình chung MỘT `fls_test` đỏ vì `database "fls_test" does not exist` (hạ tầng, ⛔ lỗi đua của hàm). Một lượt đo đầu của tôi cũng đỏ 33/52 vì tôi chồng hai đợt lên cùng kho (`wait` trong pipe không chờ) — đã loại và đo lại sạch.

## Còn lại · kết quả cổng
- `--duong-nen --cong 5436` (một mình, lần 1 bị dừng ở mốc 30' không ra kết quả; chạy lại 1 lần): **KẾT: ĐẠT** — toàn bộ `12 failed, 4509 passed, 2 xfailed, 14 errors` = **4537** bài, tập đỏ **28 = 28** đường nền (thêm 0 · bớt 0) · web `3 failed, 687 passed` = **690**, đỏ 3 = 3.
- `lint-imports` 11 kept · 0 broken · `kiem_tai_lieu.py` K1–K6 OK.
- Bài `test_ban_ky_pg.py` 14/14 xanh (gồm F7/C13 cũ).
