# KQ-114 — biên bản kiểm `BG-112` *(R2 · ISP 3.1.2 · Step 12 · DT4 · phạm vi = vòng sửa sau R1)*

| | |
|---|---|
| **Thuộc** | `BG-112` *(mục "Vòng sửa sau R1")* · `WO-111` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2)* · 2026-11-17 |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới** *(`DT4-R2-01` · `-02`)*. `F-1…F-4` đều **ĐÃ SỬA** *(ĐỎ trên `fdbb024`, XANH trên ngọn)*. **Dữ liệu khớp nguồn: 0 lệch / 86.713 ô bảng chính + 4/4 hàng bảng phụ** |
| **Cổng vào** | `git rev-parse isp/DT4` = `6516dcb` ✅ *(mã `a43ae0f` + BG)* · spec ISP 3.1.2 Step 12 ✅ |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT4.md` *(v0.2)* |

## Đối chiếu ĐỘC LẬP với nguồn *(lượt đọc lại thứ hai — mã của R2, ⛔ dùng khuôn tác giả)*
Bản sao `19NNTbX…hEU2g` · sheet `Report I General Ledger` · Sheets API v4 `values:batchGet` · `UNFORMATTED_VALUE` · `SERIAL_NUMBER` · **chỉ** `A` · `D` · `R` · `BM:BT` *(⛔ đọc `B` · `C`)*. Bản thô ở `/tmp/r2_dt4/` ⛔ commit.

| Phép so *(mỗi số nói nó đếm gì — Đ4)* | Mẫu số | Lệch |
|---|---|---|
| Hàng sheet có `A` là SỐ *(= hàng dữ liệu)*: **7.883**, liên tục `10…7892`; ảnh có đúng 7.883 `dong_sheet` cùng dải | 7.883 hàng | 0 |
| Ô bảng chính: `ky` *(suy từ `A` bằng epoch 1899-12-30 viết riêng)* · `itl_id` · `D` · `BM…BT` = 3 + 8 = **11 ô/hàng** × 7.883 | **86.713 ô** | **0** |
| Bảng phụ `itl_id_lech`: hàng nguồn có `R` ⛔ khớp `ITL#[0-9]+` | nguồn **4** = ảnh **4** | 0 *(đúng `6684·6836·7500·7832`, giá trị thô `#N/A ()` khớp)* |
| `cong_thuc`: hàng `BM:BT` có mà `A` rỗng | nguồn **9.843** *(7893…17735)* = ảnh 9.843 | 0 |
| Phụ: `itl_id` hợp lệ **7.879**, duy nhất **7.879** · `D ∈ {VND 4085 · USD 3634 · SGD 86 · HKD 72}` + **6** rỗng *(⛔ `COP`)* · **20** kỳ | — | khớp BG |

Tổng ô nguồn đã so = **86.713 + 4 hàng phụ**; **0 lệch**. *(Mẫu số > 0 ở mọi phép — Đ3.)*

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_dap_an_406.py` | `32 passed` | *(nằm trong dòng dưới; đột biến chạy riêng)* | ✅ |
| `pytest tests/du_lieu` | `195 passed` | **`195 passed in 17.99s`** | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(script NHÁNH, `GOC = …/isp-dt4`, một mình)* | `KẾT: ĐẠT` · `12 failed, 2657 passed, 2 xfailed, 14 errors` · `26 = 26` · `tests/web 3 = 3` | **`KẾT: ĐẠT`** · **`12 failed, 2657 passed, 2 xfailed, 1 warning, 14 errors in 343.82s`** · **`26 = 26 node id (thêm 0 · bớt 0)`** · `tests/web 3 failed, 661 passed` = **`3 = 3`** | ✅ |
| `lint-imports` | `11 kept, 0 broken` | **`Contracts: 11 kept, 0 broken.`** | ✅ |
| `docs/ITL/_tools/kiem_tai_lieu.py` | `✅ ĐẠT` | **`✅ cổng tài liệu ĐẠT`** *(185 file · 1.918 bảng · 731 ô ngày · 104 mã QĐ)* | ✅ |
| `ix_fx.json` + 3 ảnh DT3 đúng từng byte | `git diff cau_hinh/` rỗng | `git diff --stat cf5156e isp/DT4 -- tests/fixture/cau_hinh` = **0 dòng**; `test_DT4_giu_anh_IX_FX…` xanh *(nằm trong 195)* | ✅ |
| Checksum ảnh đổi `e98f3a699e2de469 → 53a243b42101c314` **chỉ do bảng phụ mới** | khai | `git diff fdbb024 isp/DT4 -- gl_406.json`: phần đổi = 4 dòng đầu *(`cach_doc` · `khong_mang_PII` · `ghi_chu_khuon` — chữ)* + `checksum_noi_dung` + khối `phu.itl_id_lech` *(+34 dòng)*; **`dong` (7883×11) · `nguon` · `cong_thuc` không có dòng diff**; đối chiếu nguồn lại = 0 lệch ⇒ điều khai **ĐÚNG** | ✅ |

## Bảng AC *(+ mục 8 ISP)*
| AC | Mong | Đo được | Phán quyết |
|---|---|---|---|
| mục 8 · DT4-B1…B3 đúng | ba bài + cổng | B1 *(19 kỳ khớp + 4 lệch có tên; cổng `--mong 7883`)* · B2 *(lát rỗng ⇒ ĐỎ; `values=[]` ⇒ exit 2)* · B3 *(0 khoá Diễn giải/Số CT; nay quét cả GIÁ TRỊ `itl_id`/`D`: mẫu số **2·7883**, 0 khớp)* — đều xanh trong 195; đột biến phần mới **11/12 ĐỎ** | **ĐẠT** |
| mục 8 · "3 vòng review xong" | R1 · R2 · R3 | R1 `KQ-113` xong; **R2 = phiếu này**; R3 chưa | *(chờ R3)* |
| mục 8 · điều kiện PUSH | đủ R1·R2·R3, chặn = 0 | chặn = **0** *(R1 0 · R2 0)* | *(chờ R3)* |
| AC-1 / DT4-B1 | Σ kỳ khớp `phan_bo_ky`, lệch có tên | 19 kỳ khớp · 4 lệch có tên *(`202605…08`)* · Σ 7.883 — giữ nguyên sau vòng sửa *(bảng chính 0 lệch nguồn)* | **ĐẠT** |
| AC-2 / DT4-B2 | lát rỗng ⇒ ĐỎ | bài `…ky_RONG_thi_DO` + `…values_RONG_thi_TU_CHOI` xanh; chính bài là ca phá | **ĐẠT** |
| AC-3 / DT4-B3 | 0 cột Diễn giải/Số CT | vùng đọc ⛔ `B`/`C`; quét tên + GIÁ TRỊ; ca phá cắn *(`DT4-R1-03` đã vá)* | **ĐẠT** |
| AC-4 | công cụ chung: ảnh cũ từng byte | `cau_hinh/` 0 diff từ `cf5156e`; mọi bài DT2/DT3 xanh *(trong `tests/du_lieu` 195)* | **ĐẠT** |
| AC-5 | 9.843 hàng công thức ĐẾM, ⛔ bảng chính | nguồn 9.843 = bảng phụ; hàng dữ liệu 0 ô lỗi *(86.713/86.713 số hoặc rỗng đúng 12 ô)* | **ĐẠT** |
| AC-6 | số bài | `--collect-only` ghi trong `BG`; sàn do orchestrator *(`DT4-R1-05/06`)* | **ĐẠT** *(orchestrator giữ sàn +33 — xem câu hỏi)* |

## Xét `F-1…F-7` *(tái hiện ĐỎ trên `fdbb024` = nền R1, XANH trên ngọn)*
Cách làm: `git archive fdbb024` + chép **tệp bài và ảnh của ngọn** vào ⇒ chạy: **6 failed, 26 passed** *(ĐỎ: `…TAI_TAO_dung_tung_byte…` · `…khuon_gl_406_la_tep_rieng…` · `…khoa_dong_sheet_hop_le` · `…itl_id_lech_khac_4[them_NA_thu_5]` · `…[bo_1_NA]` · `…D_ngoai_tap_tien_te_thi_DO`)*. Trên ngọn: `32 passed`.

| F | Kết luận R2 | Bằng chứng |
|---|---|---|
| `F-1` *(NÊN SỬA)* | **ĐÃ SỬA** | `itl_id_lech` = 4 hàng đúng nguồn; thêm hàng `#N/A` thứ 5 ⇒ `5 ≠ 4` ĐỎ exit 1 · bỏ 1 ⇒ `3 ≠ 4` ĐỎ; ĐỎ trên `fdbb024`; đột biến `ITL_ID_RE=.*` · `PHU_MONG 4→5` · `LECH_ITL_ID` đổi · ảnh bỏ/đổi hàng phụ ⇒ đều ĐỎ. ⚠ còn lỗ `\d` Unicode → `DT4-R2-01` |
| `F-2` | **ĐÃ SỬA** | 4 serial viết tay *(`45688→202501` · `45689→202502` · `45657→202412` · `45717→202503`)* — R2 tự tra epoch 1899-12-30 ra đúng 2025-01-31 · 2025-02-01 · 2024-12-31 · 2025-03-01; đột biến `EPOCH+1` *(sống ở R1)* nay ĐỎ `…ky_tu_serial_ghim_ranh_gioi_thang` |
| `F-3` | **ĐÃ SỬA** | `D = "Diễn giải lạc cột D"` ⇒ `D_la@10` ĐỎ exit 1, ⛔ in giá trị; bỏ nhánh `D_la` ⇒ ĐỎ; bài quét giá trị mẫu số 2·7883. Hở nhỏ → `DT4-R2-02` |
| `F-4` | **ĐÃ SỬA** | `fullmatch([0-9]+)`; ĐỎ trên `fdbb024`; đột biến về `isdigit()` ⇒ ĐỎ `…khoa_dong_sheet_hop_le` |
| `F-5` | **CHẤP NHẬN** *(orchestrator)* | ISP `:1355` còn "5 tiền tệ" — việc orchestrator, ⛔ Dev |
| `F-6` | **Đính chính chỉ-THÊM CHẤP NHẬN** | mục "Vòng sửa sau R1" nêu `162→188 (+26)` · `2652→2678`; R2 đếm `--collect-only` (đếm `::`) trên ngọn: toàn bộ **2.685** · `tests/du_lieu` **195** · `test_dap_an_406` **32** = đúng bảng BG; dòng cũ giữ nguyên *(đúng luật chỉ-THÊM, ⛔ viết lại lịch sử — Đ2)* |
| `F-7` | **CHẤP NHẬN** | hình dict/dòng là hợp đồng chung DT2·DT3 |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | Đúng spec Step 12 + WO-111 sau vòng sửa; 2 lỗ nhẹ ở cổng mới | Đột biến 12 chỗ phần mới *(bảng dưới)*: **11 ĐỎ · 1 sống** *(`DT4-R2-02`)*; thăm dò Unicode ⇒ `DT4-R2-01` |
| **Dữ liệu** *(nguồn SA, chỉ đọc)* | Ảnh = nguồn | 86.713 ô + 4 hàng phụ + 9.843 hàng công thức: **0 lệch** |
| **Màn hình** | N/A — bước dữ liệu | — |

### Đột biến *(R2 tự dựng — khác bộ R1; bản sao `git archive isp/DT4` ở `/tmp/r2_dt4/mut`; mẫu số = 12 áp được, 0 vô hiệu)*
| # | Đột biến | `pytest tests/du_lieu/test_dap_an_406.py -x` |
|---|---|---|
| N1 | `ITL_ID_RE` nhận mọi chuỗi | ĐỎ `…TAI_TAO…` |
| N2 | `PHU_MONG itl_id_lech` 4→5 | ĐỎ `…TAI_TAO…` |
| N3 | bỏ nhánh `D_la@` khỏi `thieu_lac` | ĐỎ `…D_ngoai_tap_tien_te_thi_DO` |
| N4 | `TIEN_TE` bỏ `SGD` | ĐỎ `…TAI_TAO…` |
| N5 | `_khoa_hop_le` về `isdigit()` | ĐỎ `…khoa_dong_sheet_hop_le` |
| N6 | `LECH_ITL_ID` 7832→7833 | ĐỎ `…khuon_gl_406_la_tep_rieng…` |
| N7 | `EPOCH`+1 ngày *(F-2)* | ĐỎ `…ky_tu_serial_ghim_ranh_gioi_thang` |
| N8 | ảnh: bỏ 1 hàng `itl_id_lech` | ĐỎ `…anh_406_7883_dong…` |
| N9 | ảnh: đổi chữ `itl_id_tho` hàng 6684 | ĐỎ |
| N10 | ảnh: `so_dong` phụ 4→3 | ĐỎ `…TAI_TAO…` |
| **N11** | bỏ `.strip()` ở phép `∉ TIEN_TE` | **XANH 32/32 ⇒ `DT4-R2-02`** |
| N12 | `itl_lech` đổi thứ tự sắp | ĐỎ `…TAI_TAO…` |

**Thăm dò cổng *(⛔ đột biến — hành vi ngọn)*:** lưới thô đổi một `itl_id` hợp lệ thành `ITL#٣` / `ITL#７` ⇒ `[ĐẠT]` **exit 0**, `itl_id_lech 4 = mong` *(dòng sai lọt)*; `ITL#5 ` *(đệm)* và `#N/A ()` thứ 5 ⇒ `[ĐỎ]` exit 1 *(đối chứng — cổng làm việc)*.

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-8** *(`DT4-R2-01`)* | `NHE` | `gl_406.py` `ITL_ID_RE` *(`\d`)* ↔ bài `pat = re.compile(r"ITL#\d+")` | `\d` khớp chữ số Unicode: `ITL#٣`/`ITL#７` ⇒ cổng `[ĐẠT]` exit 0. Cùng lớp `DT4-R1-04`. Nguồn thật 0 ca *(R2 đếm `[0-9]+` ⇒ cũng 4)* | `DEV` |
| F-9 *(`DT4-R2-02`)* | `NHE` | `gl_406.py` `thieu_lac` nhánh `d_la` `.strip()` | N11 sống: ⛔ bài ghim `D = "USD "` | `DEV` |

Không phát hiện mức `CHAN`/`NANG`. Hai phát hiện đều ⛔ ảnh hưởng dữ liệu đóng băng hiện tại; gộp được vào R3 hoặc chấp nhận.

## Bài thử mới *(`tests/nghiem_thu/`)*
Không thêm bài *(vai KIỂM ⛔ sửa mã; thăm dò + đột biến chạy trên bản sao)*. Bài đề xuất: `ITL_ID_RE` → `[0-9]+` + ca `ITL#٣` ⇒ `itl_id_lech 5 ≠ 4` ĐỎ; ca `D = "USD "`.

## Câu hỏi cho orchestrator
1. `DT4-R2-01` *(`\d` Unicode)* + `-02` *(`.strip()`)* — **(A)** *(khuyên)* chấp nhận, ghi sổ, ⛔ chặn R3; Dev vá khi gộp *(đổi `\d`→`[0-9]`, 2 ca bài, ≈ 5 phút)*. **(B)** vòng sửa trước R3 *(ảnh ⛔ đổi — checksum giữ nguyên)*.
2. Sàn `MONG_PYTEST_TOAN_BO` lúc gộp: **+33** so `cf5156e` *(2652 → 2685 theo BG)* — R2 đo ngọn `--collect-only` = **2.685** *(khớp BG)*; nền `cf5156e` 2.652 lấy từ R1, R2 ⛔ đo lại; orchestrator đặt sàn từ lệnh đo của mình. *(`DT4-R1-05/06` vẫn của orchestrator.)*
