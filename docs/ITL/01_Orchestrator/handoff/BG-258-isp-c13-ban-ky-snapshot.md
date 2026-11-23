# BG-258 — Bàn giao WO-257 · ISP Step 36 · C13 · IX.TMP bản báo cáo ký có phiên bản

| | |
|---|---|
| Phát bởi | fls-dev #CF (phiên cloud) · 2026-11-20 · nhánh `isp/C13` (nền `5e65ec4`) |
| Gửi | fls-test (R1 → `KQ-259`) |

## Đã làm
- `fls/cau_hinh/ban_ky.py` *(thuần)*: `kiem_ky` · `chuan_hoa` · `checksum` · `LoiBanKy`.
- `fls/repo/cau_hinh_repo.py`: `dua_ban_ky(conn, ky, noi_dung, *, actor)` *(hàm mức module — ⛔ tuyến ghi thứ ba)* · `ky_ban(conn, ky, *, actor)` · `doc_ban_ky` · `doc_noi_dung_ban_ky`.
- Tuyến (§4i, đúng 2): `GET /report/snapshot/{ky}` → `{ky, ban:[{phien_ban, checksum, trang_thai, nguoi_dua, dua_luc; da_ky thêm actor · ky_luc}]}` · `POST …/{ky}/sign` → **201** `{ky, phien_ban, checksum, trang_thai:'da_ky', actor, ky_luc}`. `actor` = thẻ.
- Kho: dùng lại `fls_cau_hinh_ban/_dong` của `0027` *(⛔ di trú mới; `bang='IX.TMP'`)*. Mỗi sự kiện = một bản config chỉ-thêm: `nguon='ban:{ky}'` *(đưa bản, dòng `so_ban` + `noi_dung`)* hoặc `nguon='ky:{ky}'` *(chữ ký, `luc` do máy, `actor` = người ký)*. Phiên bản `n` `da_ky` ⇔ có sự kiện ký mang `so_ban=n`. Cùng khoá advisory `hashtext('IX.TMP')`.
- Q8: `MONG_PYTEST_TOAN_BO` 4219 → **4226** + bài ghim cùng commit (web giữ 675).

## Checksum
sha256 hex(64) của JSON chuẩn hoá: `json.dumps(sort_keys=True, ensure_ascii=False, separators=(',',':'), allow_nan=False)` → UTF-8. Nội dung = object JSON **không rỗng**, kiểu JSON thuần (`Decimal`/`datetime`/object lạ ⇒ `LoiBanKy`, ⛔ `default=str`).

## Mã lỗi + câu
| Tình huống | HTTP · mã | Câu |
|---|---|---|
| ký, bản mới nhất đã ký | 409 `FLS-CAUHINH-DA-KY` | "⛔ phiên bản N của kỳ K ĐÃ ký bởi X lúc T" |
| ký, kỳ chưa có bản | 404 `FLS-NOT-FOUND` | "⛔ kỳ K chưa có bản báo cáo nào để ký" |
| `actor` trong thân | 400 *(cửa sẵn có, như C7)* | — |
| `{ky}` ⛔ `yyyymm` *(GET lẫn POST)* · `?run_id=` | 400 `FLS-BAD-REQUEST` | "ky=… ⛔ đúng khuôn yyyymm (năm 2000…2099 · tháng 01…12)" |
| GET kỳ chưa có bản | 200 `ban: []` | *(trạng thái thường)* |

## AC ↔ bài (`tests/cau_hinh/test_ban_ky_pg.py`, 7 bài, máy thật + kho TEST; mỗi bài chọn `{ky}` chưa có bản — mẫu số kiểm)
| AC | Bài |
|---|---|
| AC-1 | `test_C13_B1_…201_va_GET_thay_phien_ban_1_da_ky_nguoi_ky_tu_THE` |
| AC-2 | `test_C13_B2_…phien_ban_2_chua_ky_va_phien_ban_1_giu_NGUYEN` *(so `BanKy` + nội dung v1 từng byte trước/sau)* |
| AC-3 | `test_C13_AC3_…TRUNG_checksum…KHONG_sinh_phien_ban` *(+ `test_C13_checksum_TAT_DINH…`)* |
| AC-4 | `test_C13_AC4_…` *(409 · 400 actor · 400 ky hỏng ×4 · 404 · 401 · `?run_id` 400; đếm bản trước = sau)* |
| AC-5 | `test_C13_AC5_chi_them_…` *(UPDATE/DELETE cả hai bảng, mọi dòng của bản đã ký ⇒ `INV-I08`)* |
| AC-6 | `test_C13_AC6_bang_tuyen_…` + `soi_bang_tuyen` ✅ **48** *(46 → 48)*; `07_API_CONTRACT` §4i ⛔ lật |
| AC-7 | xem Cổng |

## Đỏ trước
`pytest tests/cau_hinh/test_ban_ky_pg.py -q` · exit **1** · 7 failed / 0 passed: 5× `AttributeError: module 'fls.repo.cau_hinh_repo' has no attribute 'doc_ban_ky'` · 1× `ImportError: cannot import name 'ban_ky' from 'fls.cau_hinh'` · 1× `StopIteration` *(tuyến chưa khai)* — đều vì THIẾU hành vi. Sau mã: 7 passed.

## Cổng
- `--duong-nen --cong 5434` *(một mình, 1 lần, ĐẠT ngay lần 1)*: tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4226** ≥ 4226, skipped 0, deselected 0 *(12 failed + 14 errors + 2 xfailed)*; web **3 = 3**, chạy 675.
- `lint-imports` 11 kept/0 broken · `soi_bang_tuyen` ✅ 48 · `kiem_tai_lieu` ✅ · `pg_migrate` "không có gì để áp" + `pg_verify: khớp`.

## Giả định *(chọn phương án hẹp nhất — orchestrator soát ở R1)*
1. `{ky}` = `yyyymm` *(quy ước C7)*; WO viết "2025-12" ở văn xuôi ⇒ `2025-12` bị 400. Khuyến nghị: giữ.
2. "Trùng checksum" so với bản **MỚI NHẤT** *(⛔ mọi bản)*: đổi rồi quay về số cũ = phiên bản mới. Trùng ⇒ ⛔ phiên bản, trả bản ấy `khong_doi=True` *(đã ký thì vẫn `da_ky`)*.
3. GET kỳ chưa có bản ⇒ `200` `ban: []`; POST sign kỳ chưa có bản ⇒ `404 FLS-NOT-FOUND` *(tái dùng mã C7, ⛔ mã mới)*. GET ⛔ trả `noi_dung` *(đọc qua `doc_noi_dung_ban_ky`)*.
4. Ký chỉ tác động bản **mới nhất**; bản mới nhất đã ký ⇒ `409` dù bản cũ hơn chưa ký *(không xảy ra: bản mới luôn đẩy bản cũ chưa ký xuống, ⛔ ký được nữa)*. Khuyến nghị BA: bản cũ chưa ký bị bỏ rơi là đúng ý "ký phiên bản mới nhất"?
5. Tái dùng `FLS-CAUHINH-DA-KY` *(câu ở `bao.MA_LOI` ghi "tháng IX.FX" — chỉ là mô tả mã; câu thật ở `detail`)*; ⛔ chạm `bao.py`/`goi_cua.js` *(ngoài tệp làn CF)*. Khuyến nghị: orchestrator gọn lời mô tả mã khi gộp.
6. Không có đồng thời nhiều luồng bài ghim riêng *(chỉ tuần tự)*: khoá advisory đã có, nhưng bài chạy đua như C7-R1-02 để R1 quyết.

## Vòng sửa sau R1 (KQ-259)
*(2026-11-20 · 0 CHẶN · 3 NÊN SỬA đã xử · 4 GHI NHẬN ⇒ backlog, ⛔ làm. Đột biến chạy trên bản sao `git archive HEAD` sau commit mã, 6 vòng/đột biến.)*

| Mã | Cách sửa | Đỏ trước | Xanh sau |
|---|---|---|---|
| `C13-R1-01` | Chọn cách **hẹp nhất**: `ban_ky._so_khu_hoi` đưa mọi `float` hữu hạn về đúng giá trị `jsonb numeric` trả lại *(`Decimal(repr(x))` → `-0` thành `0` → `format 'f'` → `json.loads`)* **trước** băm và lưu; kiểu khác giữ nguyên; `nan/inf` vẫn `LoiBanKy`. ⚠ `1` và `1.0` vẫn là hai checksum *(kho giữ `1.0`)*. | bài `test_C13_R1_01_…` đỏ trên mã cũ: `1e22` → đọc ra `10000000000000000000000`, checksum lệch *(R1: 2/7 lệch: `1e22`, `-0.0`)* | khứ hồi **7/7** *(`1.0` · `0.1+0.2` · `1e-7` · `10**30` · `12.50` · `1e22` · `-0.0`)*: đưa → `doc_noi_dung_ban_ky` → `checksum` = checksum lưu |
| `C13-R1-02` | Bài ký SONG SONG: 5 kỳ × 8 luồng qua HTTP thật ⇒ mỗi kỳ `[201]+[409]×7` · đúng 1 sự kiện `ky:{ky}`; thêm bài đưa-bản song song 8 luồng *(cùng nội dung ⇒ `[1]×8`; khác nội dung ⇒ phiên bản `1…8` không trùng)*. | `M7` *(bỏ khoá ở `ky_ban`)* và `M12` *(bỏ khoá ở `dua_ban_ky`)* **SỐNG 7/7** bài cũ | `M7` ĐỎ **6/6** *(bài ký song song)* · `M12` ĐỎ **6/6** *(bài đưa song song)* — tỉ lệ cắn 100% ở 6 vòng |
| `C13-R1-03` | Bài ký v1 → đưa v2 → ký ⇒ `201` phiên bản 2 · GET `[(1,da_ky),(2,da_ky)]` + checksum đúng · ký lần 3 ⇒ `409` có "phiên bản 2" và tên người ký. | `M8` *(`cu[0]` thay `cu[-1]`)* SỐNG 7/7 | `M8` ĐỎ **6/6** |

**Sàn (Q8):** `MONG_PYTEST_TOAN_BO` 4226 → **4230** *(thu thập thật cây đã gộp nhánh làm việc; +4 bài `test_ban_ky_pg.py`)* + bài ghim `test_dung_moi_truong_isp.py:423` + dòng changelog cùng commit; `tests/web` giữ 675.
**Cổng:** `--duong-nen --cong 5434` *(một mình, 1 lần, ĐẠT lần 1)*: toàn bộ `12 failed · 4202 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4230** ≥ 4230 · web `3 failed, 672 passed` ⇒ 3 = 3, chạy 675. `lint-imports` 11 kept/0 broken · `soi_bang_tuyen` ✅ 48 tuyến · `kiem_tai_lieu` ✅ (402 tệp · 104 mã QĐ).
**Backlog** *(⛔ làm ở vòng này)*: `-04` mã lỗi riêng cho F7 *(`FLS-BANKY-DA-KY` + `goi_cua.js`)* · `-05` BA ghi §4i "thân JSON, có thể `{}`" · `-06` BA quyết nhãn `thay_the` cho bản chưa ký bị thay · `-07` hợp đồng đưa bản ở I2 *(ổn định kiểu số `1` vs `1.0`)*.
