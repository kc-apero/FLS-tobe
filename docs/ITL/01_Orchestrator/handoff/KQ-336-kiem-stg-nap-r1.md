# KQ-336 — R1 `WO-334` / `BG-335` *(staging bước 05: nạp dữ liệu thật — cũ + hiện tại)*

| | |
|---|---|
| **Thuộc** | `BG-335` · `WO-334` *(gồm mục Bổ sung 05:25)* |
| **Kiểm bởi** | `fls-test` · 2026-11-23 · phiên cloud, cụm PG `5447` |
| **Phán quyết** | **`TRƯỢT`** — **1 CHẶN · 7 NÊN SỬA · 5 GHI NHẬN** *(sổ riêng `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_NAP.md`, mã `NAP-R1-01…13`)* |
| **Cây kiểm** | `origin/claude/bold-galileo-zukpaf-isp/STG-NAP` @ `b990629` *(git thật = hash trong `BG`; vào cổng ✅)* · cây gộp thử = `origin/claude/bold-galileo-zukpaf` @ `52b5763` ⊕ `b990629`, **chưa** gồm sửa STG *(R2 STG `KQ-328` còn TRƯỢT)* |
| **Kho thật** | `KHONG_CHAM` — cụm `5447`, kho scratch `fls_stg_r1_336`; ⛔ GCP · ⛔ `fls-pg-1` · ⛔ ghi sheet. Chỉ SỐ ĐẾM *(⛔ tên người · số TK · tiền dòng)*; bản thô scratchpad đã xoá |

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/staging/test_05_nap_nguon_that.py` | 18 passed | **18 passed** *(62,9 s)* | ✅ |
| `--duong-nen --cong 5447` *(cây gộp thử, MỘT lần, một mình)* | `ĐẠT` 28 = 28 · web 3 = 3 *(trên nhánh bước, 4.886 bài)* | **`KẾT: ĐỎ`** — toàn bộ: 14 failed + 14 errors + 2 xfailed = **30** node id = 28 nền + **2 THÊM** *(`test_04_nap_du_lieu::test_chuoi_sau_khi_nap_config_ra_DAT_10_goi` · `…::test_chuoi_tren_kho_TRANG_DO_nen_ten_goi_thieu_config`)*, bớt 0, chạy **5.001** ≥ sàn, skipped 0; `tests/web` **3 = 3** ✅ chạy 690. 2 bài THÊM = **`STG-R1-02`** *(ghim cứng "10 gói", `GOI_BIET` ở nhánh làm việc có 11 gói)* — **không do WO-334**; sửa đã ở `origin/…-isp/STG` @ `4042079` *(`GOI_BIET` 6 chỗ)* nhưng cây thử này theo lệnh chưa gồm STG. *(Lần chạy đầu trên cây CHƯA commit ⇒ 52 node vì `git archive HEAD` ⛔ thấy `Dockerfile`: lỗi của cây thử, không tính; commit gộp CỤC BỘ `thu/STG-NAP`, ⛔ đẩy)* | ⛔ **ĐỎ có tên, không do bước NAP** |
| `pytest --collect-only` *(cây gộp thử)* | sàn 4.886 *(nhánh bước)* | **5.001** thu thập · web **690** ⇒ sàn cây gộp = 5.001 *(xung đột `NAP-R1-08` giải bằng số thu thập)* | ✅ *(lệch có lý do)* |
| `kiem_tai_lieu` *(cây gộp thử)* | ĐẠT | `✅ cong tai lieu DAT` *(500 tệp · 3.010 bảng · 982 ô ngày · 104 mã QĐ)* | ✅ |
| `lint-imports` | 11 kept | **11 kept, 0 broken** | ✅ |
| `quet_pii_repo` | 0 | **`[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp`** | ✅ |
| `kiem_so_song` · `dong_bo_so_song` · `khop_owner --kiem` | ⛔ chạy được ở Linux | **⛔ chạy lại** *(`kiem_so_song.py:406` gọi `.venv/Scripts/lint-imports.exe`)* — chỉ ghi nhận lời Dev | ⛔ không đo được |

## Bảng AC
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** liệt kê đủ công cụ | đủ công cụ + thứ tự + đích + số mong | `grep h1000` ở `fls/`+`tools/` = **17** tệp *(trong đó **3** có `psycopg`/`INSERT`)* — **trùng BG**. Nhưng bảng thiếu `tools/nap_nguon_dai.py` *(→ `fls_nguon_dai`, **7** tệp `fls/` dùng; tuyến `bang_tuyen.py` đọc)*: nhắc tới ở BG/README/công cụ = **0·0·0** | **TRƯỢT nhẹ** — `NAP-R1-06` |
| **AC-2** công cụ 05 | Cloud Shell + proxy + `fls_ghi`; xác thực ⛔ gắn cứng; chỉ-đọc; `FLS_CHO_GHI_THAT`; chạy lại ⛔ nhân đôi | Phạm vi = `spreadsheets.readonly` + `drive.metadata.readonly` *(đột biến M1 thêm phạm vi ghi ⇒ ĐỎ)*; đường ghi sheet: grep `values:update\|batchUpdate\|:append\|valueInputOption\|method=POST/PUT/PATCH/DELETE` ở `tools/`+`fls/` = **1** tệp `tools/ghi_o_that.py` *(có từ trước, **0** `import` từ chuỗi 05/nạp)*, ở 05 + 4 công cụ nạp = **0**; token: `ya29.`/`PRIVATE KEY` trong log live = **0**; M8 *(bỏ đòi `FLS_CHO_GHI_THAT`)* ⇒ ĐỎ; `bash -n` 05 ✅; nạp lại lần 2 *(live)* Mapping **73 → 73**, mọi số đếm lần1 = lần2 *(chênh = ∅)*; `fls_itl` lần 2 ở bài `CHAY_LAI` **9.985 → 9.985** | **ĐẠT** *(có `NAP-R1-05`: chặn 5433 lọt 5/10 dạng DSN)* |
| **AC-3** BÁO CÁO khớp 100 % | `mong` khai trước · ĐỎ hai chiều · ⛔ đo = ĐỎ · mẫu số ≠ 0 | 403 ⇒ `403 (mong 200)` có tên ở mục `0b` + bước DỪNG, ⛔ `None` im lặng *(M3 *"`None` = ĐẠT"* ⇒ ĐỎ; M5 *"403 = đọc được"* ⇒ ĐỎ)*. Nhưng **4/11 đột biến sống**: M7 · M10 *(hàng Σ nguồn = Σ kho của Mapping, PM thành tautology)* · M9 *(đảo kỳ chốt/mở)* · M11 *(mẫu số Mapping = hằng)* — mẫu `Đ5` | **TRƯỢT** — `NAP-R1-02` |
| **AC-4** riêng tư | `Email Address` ⛔ vào kho; `Tên tài khoản` giữ; BÁO CÁO chỉ số đếm | BÁO CÁO live: **0** dòng ≥ 9 chữ số liền · **0** email-like. M6 *(`PM_COT_RIENG_TU = ∅`)* ⇒ ĐỎ đúng bài. **Nhưng:** stdout trước BÁO CÁO có **5/5** dòng `loai dong` chứa chuỗi ≥ 9 chữ số *(ô nguồn thô)* — `NAP-R1-04`; và ở live phép `Email Address = 0` **ĐẠT trên mẫu số PM kho = 0** — `NAP-R1-03` *(Đ3)*. `sao_luu/`·`hien_vat/` ở 3 tệp 05: **1** lần, chỉ trong chú thích; đường tải lên = **0** | **TRƯỢT nhẹ** — `NAP-R1-03` · `-04` |
| **AC-5** HD2 + `do_voi_so_luong` | khớp `voi_so_luong.json`/`hd2_cong.json` | Chỉnh phiếu của Dev đúng *(Đ1)*: `grep -c "psycopg\|PG_DSN" tools/do_voi_so_luong.py` = **0**; HD2 10/10 gói — **không chạy lại** ở R1 *(thuộc R2)*; `--duong-nen` ở cây gộp thử gồm bước `HD1 do_voi_so_luong`: `chay 9845 / co 9967` ✅ | **ĐẠT có điều kiện** *(R2 đo chuỗi HD2)* |
| **AC-6** README/UAT/sàn | README + UAT + `--duong-nen` ĐẠT + nâng sàn cùng commit | `test_uat_doc` xanh trong 18 bài; sàn nhánh bước 4.886 = ghim; **cây gộp thử** xung đột sàn, giải = 5.001 *(`NAP-R1-08`)*; `--duong-nen` cây thử ĐỎ **chỉ** vì 2 bài `STG-R1-02` *(nhánh bước ⛔ gây ra)*; nhánh bước tự báo `ĐẠT` @ `608e35f` | **ĐẠT** *(sổ-sàn/ghim)*, `--duong-nen` **chờ gộp sửa STG** |
| **AC-7** dữ liệu CŨ | phát lại ảnh ⇒ khớp 100 % số đã đo, lệch 0 | Bài `CU_phat_lai_anh…` xanh: `bank_tong` **9.992 · 105 · 6.532 · A2.272·B29·C400·D27·E199·F428** và `pm_tong` **3.703 · 3.173** = `voi_so_luong.json` từng số; kho `fls_itl` 9.985 + `fls_reject` 7 = 9.992; mất 0 · lệch 0 · mới 0 *(14 phép)*; đột biến M2 ⇒ ĐỎ. **Không** tái lập `tong.co` **9.967** · **23** kỳ · `o_parity` **69.510** *(ảnh thiếu lưới 38 cột; Dev đã khai §9.3)*; `san_0` hạ sàn ⇒ cổng đọc-đủ ⛔ được thử ở dữ liệu cũ — `NAP-R1-07` | **ĐẠT trong phạm vi đã khai** *(ghi đúng phạm vi)* |
| **AC-8** dữ liệu THẬT hiện tại | đọc live chỉ-đọc ⇒ Σ nguồn = Σ kho; kỳ chốt = số cũ; kỳ mới đếm riêng | **Tái lập được 100 %**: chạy lại `2026-11-23T07:22Z` và `07:26Z` ⇒ **mọi** số đếm = `BG-335` §3/§4 và lần 1 = lần 2 *(15 mục ĐỎ · 16 ĐẠT)*: L1 **14.265** = canon **12.601** + loại **121** + rỗng **1.543** · PM **3.909** *(có mã 3.369)* · `T·CDT1` **3.056 < 3.300** *(theo HÀNG = theo CỘT)* · bank ảnh: mất theo vị trí **12** · lệch `ref` 7.550 · `cur` 2.975 · tiền 7.545 · **37** bộ ba mất theo nội dung · mới 2.621 · PM lệch `ref` 30 · `status` 29 · `hd` 117 · `cdt1` 534 · mới 206 · **403** Bank + Quỹ · Mapping Master **73/73**. Phép *"theo nội dung"* **ĐÚNG** *(tự đo thuần trên ảnh, 6 ca)*: dịch +1 hết ⇒ vị trí lệch 9.320 ref · nội dung **0**; xáo trộn ⇒ vị trí 9.991 · nội dung **0**; sửa 1 ô tiền ⇒ **1**; xoá 1 dòng ⇒ **1**; xoá 1 trong 2 bản trùng ⇒ **1**; nguồn rỗng ⇒ 9.992 *(⛔ xanh trên rỗng)*. **Nhưng vế "kỳ chốt = số cũ" KHÔNG được giao**: `voi_so_luong.theo_ky[k].co` có sẵn *(23 kỳ, Σ 9.967)* mà BG nói *"⛔ có số CŨ"* — sai. Tự so: **13/23** kỳ bằng · **9** kỳ live thấp hơn 1–3 dòng *(Σ −19)* · **1** kỳ cao hơn *(2026-08, +237)* | **TRƯỢT** — `NAP-R1-01` *(CHẶN)* |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến `INV-I08`)* | Thứ tự phụ thuộc ①→④ đúng; 403 DỪNG có tên; cổng đọc-đủ ĐỎ ⇒ ⛔ ghi sổ nhưng vẫn đo; `fls_itl` chỉ-THÊM giữ. **Yếu:** 4/11 đột biến sống *(`NAP-R1-02`)* và vế kỳ-chốt thiếu *(`-01`)* | đột biến **11** *(M1–M11)*: chết **7** · sống **4**; `diff` bản gốc sau đột biến = **0** *(đột biến chỉ trên `git archive`)* |
| **Dữ liệu** *(đọc live chỉ-đọc, kho scratch)* | Số đếm tái lập; 3 phát hiện NGUỒN của Dev **đúng** *(403 · CDT1 3.056 · nguồn bị sửa sau ảnh)*, thêm 1 phát hiện mới của Test: **9 kỳ chốt mất 1–3 dòng** *(`-01`)* | `fls_stg_r1_336`: `fls_itl` **0** · `fls_pm_line` **0** *(cổng đọc-đủ chặn — đúng thiết kế, **mẫu số 0** là kết quả)* · `fls_mapping_master` **73** · nạp lại **73** |
| **Màn hình** | **Không áp dụng** — bước 05 không có màn; `fls/**` diff = 0 *(BG; không đo lại tuyến)* | — |

## Phát hiện *(chi tiết ở sổ riêng — một dòng/mã)*
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `NAP-R1-01` | `CHAN` | `nap_nguon_that.py:339-348` · `BG` §4 | so `theo_ky_canon` live ↔ `voi_so_luong.theo_ky[k].co`: 13/23 bằng · 9 thấp (Σ −19) · 2026-08 +237 | `DEV` |
| `NAP-R1-02` | `NANG` | `nap_nguon_that.py:268,273,316,347` | đột biến M7·M9·M10·M11 ⇒ 18/18 xanh | `DEV` |
| `NAP-R1-03` | `NANG` | `nap_nguon_that.py:392-405` | live: `Email Address` = 0 `[ĐẠT]` trên mẫu số PM kho 0 | `DEV` |
| `NAP-R1-04` | `NANG` | `tools/nap_that.py:273` | stdout live: 5/5 dòng `loai dong` có ≥ 9 chữ số | `DEV` |
| `NAP-R1-05` | `NANG` | `nap_nguon_that.py:409-413` | `kiem_dsn` lọt 5/10 dạng DSN cổng 5433 | `DEV` |
| `NAP-R1-06` | `NANG` | `BG-335` §1 · `tools/nap_nguon_dai.py` | AC-1 thiếu `fls_nguon_dai` (7 tệp `fls/` dùng; nhắc 0·0·0) | `DEV`/`BA` |
| `NAP-R1-07…11` | `NHE` ×5 | sổ riêng | phạm vi AC-7 · xung đột sàn 5.001 · `None`/`shell=True`/test chuỗi · 37≟37 · nợ môi trường | `DEV`/`BA` |

## Bài thử mới *(`tests/nghiem_thu/`)*
Không thêm bài ở R1 *(hợp đồng R1 = tái đo + đột biến + sổ; Dev sửa ⇒ R2 thêm bài chốt)*. Mười một đột biến + năm dạng DSN lọt + sáu ca phép "theo nội dung" đã đo trên bản sao `git archive`/hàm thuần, **không** commit.

## Việc kế
`TRƯỢT` ⇒ vòng sửa `fls-dev` *(`NAP-R1-01` CHẶN + 5 NÊN SỬA)* ⇒ R2 cuối trên cây gộp thử **sau khi** gộp sửa STG *(`KQ-328`)* — sàn pytest đặt lại theo số thu thập cây gộp cuối. **Câu cho chủ:** số live đã tái lập; "kỳ đã chốt" ≠ số cũ ở 9 kỳ + 37 bộ ba bank — chủ quyết nguồn nào là chuẩn *(đã có ở BG #3, nay có thêm số theo kỳ)*.

## Phụ lục — đo lại sau khi chủ chia Viewer *(`2026-11-23T08:41Z`, SA của container, kho scratch `fls_stg_r1_336b`, cụm `5447` bật lại vì container khởi động lại)*
- **Workbook BANK: 403 → `200`** ✅ · **QUỸ: vẫn `403`** *(`HTTP … 403 (mong 200)`, ĐỎ có tên)* · RAW `200`.
- Vì ① *(68 dòng chảy = Bank + Quỹ)* cần cả hai nên **vẫn DỪNG có tên**, và ④ *(chụp 60 sheet)* phụ thuộc bản khai ① nên **vẫn DỪNG** ⇒ số `68 · 408 · 60 nguồn · 8.368 dòng` **⛔ đo được** ở lượt này. Cần chủ chia Viewer nốt `Copy of P100 | Cash Ledger` *(hoặc độ trễ lan truyền — đo lại sau)*. Ghi nhận thêm: SA của container có thể khác SA `fls-sheets-reader` mà chủ đã chia — phải chia cho **cả hai**.
- Số còn lại **y hệt** hai lượt 07:22Z/07:26Z: L1 14.265 · PM 3.909 · `T·CDT1` 3.056 < 3.300 · 37 bộ ba · PM lệch `hd` 117 · `cdt1` 534 · Mapping 73/73. `KẾT: ĐỎ — 14` mục *(trước 15: hết ĐỎ Bank)*.
- Phán quyết `TRƯỢT` **không đổi**.
