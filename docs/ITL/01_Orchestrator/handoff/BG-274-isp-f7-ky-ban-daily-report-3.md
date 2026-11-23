# BG-274 — Bàn giao WO-273 · ISP Step 40 · F7 · SCR-F08 ký bản Daily Report 3

| | |
|---|---|
| Phát bởi | fls-dev #FE (phiên cloud Sonnet 5.5) · 2026-11-22 · nhánh `isp/F7` (nền `bb9ea2f`) |
| Gửi | fls-test (R1 → `KQ-275` · R2 cuối → `KQ-276`) |

## Đã làm
- `fls/web/tep/man_f08.js`: vùng thứ hai `#ban-f08` *(dựng một lần bằng `createElement`, ⛔ phụ thuộc bảng `IX.FX` — kho test thiếu `IX.FX` ⇒ `GET /config/fx` `409` mà vùng vẫn sống)*: ô kỳ `#ban-ky` + `Xem bản` ⇒ `GET /report/snapshot/{ky}`; bảng phiên bản *(bản · checksum 12 ký tự, đủ 64 ở `title` · đã/chưa ký · người ký · ngày)*; `Ký bản` ký bản **mới nhất** qua hộp `HT.mo` của F5 *(⛔ hộp mới)* ⇒ `POST …/{ky}/sign` thân `{}` *(⛔ `actor`)*. Bốn trạng thái qua `TT.chay`; lượt xem mới nhất thắng.
- Tiêu điểm: đóng hộp mà ⛔ ký ⇒ về nút `Ký bản` *(hộp không tự trả — `_tra_tieu_diem`, theo dõi lớp `on` của `#scrim`, một lần)*; ký xong ⇒ vẽ lại, giữ `scrollY`.
- `tests/web/test_isp_f08_ky_ban_pg.py` (7 bài) · `tests/web/test_isp_f08_fx.py` *(đếm `button.nut-ky` thay mọi `button` — màn có thêm nút; 4 bài F4 đã đỏ vì vỏ DOM giả + đếm sai vật, sửa cả hai)*.
- Thuyết minh: `13_THUYET_MINH_MAN_HINH.md §6b` + `Ban-ve-TOBE-Man-Ghep-PM.html` thêm `Ký bản` · `Xem bản` *(`kiem_thuyet_minh` 35/35)*. ⛔ sửa `BA-06 §9` *(spec field-level của F7 là việc `fls-ba`; nợ ghi dưới)*.
- Dữ liệu thử: `chc.dua_ban_ky` + `chc.ky_ban` *(hàm mức repo — ⛔ tuyến ghi mới)*; mỗi bài một kỳ `yyyymm` chưa có bản *(2000…2099; nền kiểm `[]`/2 bản trước khi chạy — Đ3)*.

## C13-R1-04 — đóng
Chọn **chữ phía màn theo ngữ cảnh tuyến** *(`CAU_BAN` trong `man_f08.js`)*: `FLS-CAUHINH-DA-KY` ở `POST /report/snapshot/…/sign` hiện *"Bản báo cáo mới nhất của kỳ này đã được ký rồi"* + `chi_tiet` của cửa *("phiên bản N của kỳ K ĐÃ ký bởi X")*. ⛔ đổi mã lỗi, ⛔ chạm `bao.py`/`goi_cua.js` *(F5 `409` tỷ giá giữ câu cũ — bài F5 xanh)*. Đột biến *(bỏ ghi đè)* ⇒ bài `test_AC4_C13_R1_04_…` **ĐỎ** *(`assert 'tỷ giá' not in …`)*; trả nguyên ⇒ xanh.

## AC ↔ bài
| AC | Bài *(`test_isp_f08_ky_ban_pg.py`)* | Đo |
|---|---|---|
| AC-1 | `test_AC1_F7_F1_…` | 2 bản (1 đã ký) ⇒ danh sách ⇒ hộp ⇒ **cả hai** `đã ký`, checksum 64 ký tự **khác nhau**, bản 1 giữ người ký/`ky_luc`/checksum từng byte *(so kho trước/sau)*; bản 2 = người ký từ thẻ |
| AC-2 | `test_AC2_…` | kỳ `[]` ⇒ chữ *"chưa có bản báo cáo nào"* + lớp `ban-rong`, nút ký **0/khoá**; AC-1 sau ký ⇒ nút `Ký bản` khoá |
| AC-3 | `test_AC3_AC6_…` + AC-1 | **Huỷ** *(nút)* ⇒ **0** POST; `Esc` ⇒ **0**; `dblclick` nút chính ⇒ **đúng 1** POST |
| AC-4 | `test_AC4_C13_R1_04_…` · `test_AC4_404_400_500_mang_…` · `test_AC4_GET_400_…401_…` | `409` *(người khác ký chen, `201` trước)* chữ bản báo cáo, hộp ở nguyên, danh sách tải lại ⇒ cả hai `đã ký`; `404`/`400`/`500`/mạng ⇒ chữ Việt, ⛔ `FLS-…` thô, nút hộp ⛔ treo; GET `400` *(`2025-12`)* · `401` *(thẻ rỗng)* ⇒ chữ Việt. `test_goi_cua_phu_het_ma_loi` xanh |
| AC-5 | `test_AC5_…` + `test_AC1…` | thân POST = `{}`; thân có `actor` ⇒ cửa `400` + kho không đổi; mã màn ⛔ khớp `\bactor\s*:` |
| AC-6 | `test_AC3_AC6_…` + `kiem_thuyet_minh` | `Esc`/Huỷ ⇒ tiêu điểm về nút `Ký bản`; `Enter` ngay khi hộp mở ⇒ hộp **còn mở**, 0 POST; thuyết minh **35/35** |
| AC-7 | Q8 | xem dưới |

## Đỏ trước
`pytest tests/web/test_isp_f08_ky_ban_pg.py` *(chưa có `man_f08.js` mới)* · exit **1** · **7 failed** / 0 passed *(`waitForSelector('#ban-ky')` hết giờ — THIẾU hành vi)*, 218 s. Sau mã: **7 passed** *(8,8 s)*. Phát hiện: lần đầu kho test thiếu `IX.FX` ⇒ vùng ký bản phải độc lập bảng tỷ giá *(đã làm)*.

## Hai ảnh *(1100×900, `deviceScaleFactor` 1; ⛔ commit; chụp bởi `F7_ANH_DIR`)*
- **Trước ký:** thẻ *"Bản Daily Report 3 · IX.TMP"* dưới thẻ tỷ giá; kỳ `202910`; hai dòng: `bản 1 · 335d94e082a4 · đã ký · nguoi.ky.ban1@vi-du.invalid · 2026-11-22`, `bản 2 · a32fbd10ba89 · chưa ký · — · —`; nút `Ký bản` sáng, dòng chữ *"Ký phiên bản 2 (mới nhất); bản cũ đã ký giữ nguyên."*
- **Sau ký:** cả hai `đã ký`; bản 2 người ký `ke.toan.f7@vi-du.invalid` *(từ thẻ)* · `2026-11-22`; bản 1 y nguyên; `Ký bản` mờ/khoá + *"Phiên bản 2 (mới nhất) đã ký — ⛔ ký lại."*; hộp đóng. *(Thẻ tỷ giá phía trên hiện `409 FLS-CAUHINH-CHUA-KHAI` vì kho test thiếu `IX.FX` lúc chụp — ⛔ liên quan F7.)*

## Cổng
- `--duong-nen --cong 5436` **hai lượt** *(lượt 1 ĐỎ: 4 bài `test_isp_f08_fx.py` đỏ — sửa; lượt 2 một mình)*: **tests/web** `3 failed, 685 passed` ⇒ tập đỏ **3 = 3**, chạy **688** ≥ 688, thêm 0 · bớt 0 — **ĐẠT**. **Toàn bộ** `13 failed · 4256 passed · 2 xfailed · 14 errors` ⇒ **29 vs 28**: **thêm 1** = `tests/test_kiem_thuyet_minh.py::test_MOI_nhan_doc_tu_MA_deu_co_trong_CA_HAI_ban` *(nhãn `Xem bản` thiếu ở `.html`)* — **đã sửa** *(commit `a41490d`)*; kiểm lại bằng `pytest tests/test_kiem_thuyet_minh.py` ⇒ 5 passed + `kiem_thuyet_minh` 35/35, **⛔ chạy lại `--duong-nen` lần ba** *(luật: đỏ ⇒ sửa + chạy lại MỘT lần — đã dùng)*. Chạy 4285 ≥ 4285, skipped 0, deselected 0. ⇒ **cổng toàn bộ lượt cuối ĐỎ 1 bài đã sửa, chưa đo lại bằng cổng** — orchestrator/R1 đo lại.
- `lint-imports` 11 kept/0 broken · `kiem_tai_lieu` ✅ *(416 tệp · 104 mã QĐ)* · `soi_bang_tuyen` ✅ 48 tuyến · `kiem_thuyet_minh` ✅ 35/35.
- **Sàn (Q8)** *(cùng commit mã `1f86549`)*: `MONG_PYTEST_TOAN_BO` **4278 → 4285** · `MONG_PYTEST_WEB` **681 → 688** *(thu thập thật `--collect-only`: 4285 · tests/web 688 — +7 bài)* + bài ghim `test_dung_moi_truong_isp.py:423-424` + dòng changelog `+ isp/F7 ⇒ 4285`.

## Giả định / nợ *(⛔ làm ở bước này)*
1. Kỳ nhập tay `yyyymm`, ⛔ mặc định *(spec §9 chưa viết field-level F7 — nợ `fls-ba`: ô chọn kỳ hay danh sách kỳ có bản?)*.
2. `C13-R1-06`: bản cũ chưa ký bị bản mới đẩy xuống — màn hiện `chưa ký` mãi, ⛔ nhãn `thay_the` *(chờ BA)*.
3. `C13-R1-05`: màn gửi `{}` *(cửa đòi thân JSON)* — đã đúng; §4i chưa ghi.
4. Thẻ `IX.FX` ở kho test rỗng ⇒ ảnh có khung đỏ `409` phía trên *(ngoài phạm vi)*.

## Vòng sửa sau R2 (`KQ-276`) — `F7-R2-01`
- **Lỗi (R2 đo):** mở hộp "Ký phiên bản 2", engine chèn bản 3, xác nhận ⇒ POST `{}` `201` ký **bản 3**, bản 2 `chua_ky`, ⛔ cảnh báo.
- **Sửa (chỉ FE `man_f08.js`; ⛔ đổi tuyến · ⛔ thêm trường thân POST):** xác nhận ⇒ `GET …/snapshot/{ky}` ngay trước POST; bản mới nhất ≠ (phiên bản · checksum) của hộp ⇒ ⛔ POST, vẽ lại danh sách + hộp nêu bản MỚI kèm *"Đã có phiên bản mới hơn — kiểm lại trước khi ký"*, đòi xác nhận lại; bản mới nhất đã `da_ky` ⇒ chỉ chữ cảnh báo trong hộp; lỗi khi tải lại ⇒ chữ lỗi, ⛔ POST.
- **Đo:** `test_F7_R2_01_ban3_chen_…` ĐỎ trước (POST ngay lần 1) → sau sửa: lần 1 **0 POST**, hộp nêu bản 3 + checksum rút gọn, lần 2 **đúng 1 POST** `{}`, kho `[da_ky, chua_ky, da_ky]` (bản 3 do thẻ ký). `test_F7_R2_01_loi_mang_…`: **0 POST** + chữ Việt. Ca thường (`AC1`: bản 2 không đổi) vẫn **1 POST**; Huỷ/Esc/Enter/bấm kép/409/404/400/500 xanh (20/20 trên `ky_ban`+`ky`+`fx`). **Đột biến** bỏ so sánh bản (`if (false)`) ⇒ bài bản-3 ĐỎ; trả nguyên ⇒ xanh.
- **Sàn (Q8, cùng commit):** thu thập thật toàn bộ **4360** (4351 + 7 F7 + 2) · web **690**; bài ghim + changelog nâng cùng commit. `--duong-nen --cong 5436` (một mình, một lần): **ĐẠT** — toàn bộ 28 = 28 (thêm 0 · bớt 0), chạy 4360; web 3 = 3, chạy 690. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT · `kiem_thuyet_minh` 35/35.
- **GHI NHẬN `F7-R1-01/03/04`** ⇒ backlog (⛔ làm ở vòng này).

### Câu hỏi cho BA
1. **Khe đua còn lại:** giữa lúc tải lại và POST (cỡ ms) engine vẫn có thể chèn bản mới ⇒ vẫn ký bản mới. Màn ⛔ chặn được hết.
2. **Phương án ràng ở tuyến:** `POST …/sign` nhận (qua query `?checksum=` hoặc thân) checksum bản người dùng đã thấy; ≠ bản mới nhất ⇒ `409` mã riêng. BA chốt §4i có đổi hợp đồng (hiện thân `{}`, cửa `400` nếu có `actor`) hay chấp nhận khe ms. ⛔ làm ở vòng này.
