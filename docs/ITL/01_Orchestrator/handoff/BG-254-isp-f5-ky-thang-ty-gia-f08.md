# BG-254 — Bàn giao WO-253 · ISP Step 37 · F5 · SCR-F08 ký tháng tỷ giá (D1)

| | |
|---|---|
| Phát bởi | fls-dev #FE (phiên cloud) · 2026-11-19 · nhánh `isp/F5` (nền `7cc8d04`) |
| Gửi | fls-test (R1 → `KQ-255`) |

## Đã làm
- `fls/web/tep/man_f08.js`: cột **Ký**; nút `Ký tháng` ở dòng **sạch** chưa ký (⛔ `TRÙNG`, ⛔ `LẠC` — không niêm phong số chính màn đang gắn cờ). Bấm ⇒ `HT.mo` (`hop_thoai.js`, ⛔ hộp mới) nêu tháng + 5 tỷ giá ⇒ xác nhận ⇒ `FLS.ghi('/config/fx/{yyyymm}/sign', {})` ⇒ vẽ lại từ `GET` ⇒ dòng *"đã ký · người ký · ngày"*, nút **khoá**. Thân POST **rỗng** (`actor` từ thẻ — AC-5). Lỗi cửa ⇒ `HT.loi_trong_hop` (chữ qua `goi_cua.js`), hộp ở nguyên. Huỷ ⇒ ⛔ POST.
- Ngày ký = 10 ký tự đầu `ky_luc` (ISO của máy) — ⛔ đổi múi giờ.
- Thuyết minh: `13_THUYET_MINH` §6b + bản vẽ HTML + `DONG_SINH` (cổng **chưa thấy** nút gán bằng `textContent` ⇒ khai tay; đã chứng minh ĐỎ rồi ĐẠT, 32→33/33). `06_SCREEN_SPEC` §9 ⓐ dòng *Hành động* cập nhật.
- Q8: `MONG_PYTEST_TOAN_BO` 4101 → **4105**, `MONG_PYTEST_WEB` 675 → **679** + bài ghim cùng commit (đo `--collect-only`: 4105 · 679).

## F5-F1…F3 ↔ bài (`tests/web/test_isp_f08_ky_pg.py`, 4 bài; Playwright/Chromium thật ↔ máy chủ thử ↔ kho TEST)
| AC | Bài | Đo |
|---|---|---|
| F5-F1 | `test_AC1_F5_F1_…` | tiền đề kho: 202510 chưa ký · hộp mở, **0** POST trước xác nhận · đúng **1** POST thân `{}` · dòng *đã ký · `ke.toan.f5@…` · ngày* · nút `disabled` · kho: `actor` = thẻ |
| F5-F2 | `test_AC2_F5_F2_…` | người khác ký 202511 (201) giữa chừng ⇒ xác nhận ⇒ hộp ở nguyên, chữ *"đã được ký rồi"*, ⛔ `FLS-CAUHINH-DA-KY` |
| F5-F3 | `test_AC3_F5_F3_…` | Huỷ ⇒ **0** request POST · hộp đóng · dòng chưa ký · kho chưa ký |
| AC-5 | `test_AC5_…` | thân có `actor` ⇒ cửa **400**, kho ⛔ ghi; `man_f08.js` ⛔ có `actor:` |
| AC-4 | `test_goi_cua_phu_het_ma_loi.py` (có sẵn) | xanh; câu có cho `FLS-UNAUTHORIZED` · `FLS-NOT-FOUND` · `FLS-BAD-REQUEST` · `FLS-CAUHINH-DA-KY` (409) · `FLS-FX-CHAN` |
Sửa bài F4 `test_isp_f08_fx.py`: `nut == 0` ⇒ `nut == số dòng sạch chưa ký (36)` đếm theo `ky[]`/`lac[]` của tuyến (mẫu ≠ rỗng).
Đã đỏ trước: 4 bài ĐỎ (không có nút) trước khi sửa `man_f08.js`.

## Đo (cổng)
- `--duong-nen --cong 5446` (lượt cuối): toàn bộ `12 failed · 4077 passed · 2 xfailed · 14 errors` — tập đỏ = nền **28 = 28**, thêm 0, bớt 0, chạy 4105 (mong ≥ 4105) · `tests/web` `3 failed · 676 passed` — **3 = 3**, chạy 679 (mong ≥ 679) · **KẾT ĐẠT**.
- `lint-imports` 11 kept 0 broken · `kiem_tai_lieu` ĐẠT · `kiem_thuyet_minh` 33/33.
- ⚠ Lượt đầu ĐỎ 1 phép: bài AC1 của chính tôi — `_da_ky()` đọc chữ ký **thô**, bài C7 (chạy trước trong bộ đầy đủ) để lại chữ ký lệch dấu vân trong kho chỉ-THÊM ⇒ tiền đề *chưa ký* sai. Sửa **bài** (đếm chữ ký còn phủ đúng dấu vân, như cửa), ⛔ sửa mã; chạy lại MỘT lần ⇒ ĐẠT.

## Bằng chứng ảnh (1100×800, scale 1) — `handoff/anh_BG-254/`
- `f5_truoc_ky.png` (135 KB): bảng 37 dòng, mỗi dòng sạch có nút **Ký tháng**; dòng `202306` chỉ nhãn LẠC, ⛔ nút.
- `f5_sau_ky.png` (139 KB): `202510` hiện *đã ký · ke.toan.f5@vi-du.invalid · ngày*, nút xám khoá; hộp đã đóng.

## ⚠ Lệch / chỗ R1 nên soi
1. Nút **⛔ ở dòng TRÙNG/LẠC** — quyết định của tôi (WO không nói). Đổi ý ⇒ một dòng `_ky_o`.
2. Dòng thiếu tháng (`CHẶN`, không có `ky`) ⛔ nút — không có số để niêm phong.
3. Sau ký, **vẽ lại cả bảng** (một `GET`) — thấy chữ ký do máy xác nhận, ⛔ tự đoán.
4. `06_SCREEN_SPEC` §9 chỉ sửa dòng *Hành động*; spec field-level ⓑ + `US` vẫn nợ `fls-ba` (⛔ tôi viết spec).
5. Ba bài web đỏ + 12 đỏ toàn bộ là nền có sẵn (`duong_nen_bai_do.txt`), ⛔ liên quan F5.
