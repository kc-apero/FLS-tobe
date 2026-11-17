# KQ-113 — biên bản kiểm `BG-112` *(R1 · ISP 3.1.2 · Step 12 · DT4)*

| | |
|---|---|
| **Thuộc** | `BG-112` · `WO-111` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1)* · 2026-11-17 |
| **Phán quyết** | **`TRƯỢT`** *(nhẹ)* — **0 CHẶN · 1 NÊN SỬA** `F-1` · 6 GHI NHẬN. Lý do duy nhất: `F-1` *(4 hàng `itl_id = #N/A ()` lọt cổng + BG khai sai)*. **Dữ liệu khớp nguồn: 0 lệch / 157.648 phép so** |
| **Cổng vào** | `git rev-parse isp/DT4` = `bcc0cb6` ✅ *(mã `afe1c0a` + `BG-112`; nền `cf5156e`)* · spec ISP 3.1.2 ✅ |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT4.md` *(v0.1 · `DT4-R1-01…07`)* |

## Đối chiếu ĐỘC LẬP với nguồn *(lưới SA tự đọc — mã của R1, ⛔ dùng khuôn tác giả)*
Bản sao `19NNTbX…hEU2g` · sheet `Report I General Ledger` · Sheets API v4 `values:batchGet` · `UNFORMATTED_VALUE` · `SERIAL_NUMBER` · **chỉ** `A` · `D` · `R` · `BM:BT` *(⛔ đọc `B` · `C`)*. Bản thô ở `/tmp/r1_dt4/` ⛔ commit.

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Hàng dữ liệu *(cột A là số)* | `A10:A21238` | **7.883** = hàng 10…7892, liên tục, A tăng dần, A toàn `int` |
| So **từng ô** nguồn ↔ ảnh *(`dong_sheet` · `ky` · `itl_id` · `D` · 8 ô `BM…BT` · chuỗi số = repr JSON nguồn)* | **157.648** phép so | **0 lệch** *(số GIỮ y giá trị API, ⛔ làm tròn — kiểm 7.883 × 8 − 12 ô rỗng = 63.052 số)* |
| `D` so chặt *(rỗng ↔ `null`)* | 7.883 | **0 lệch** · 6 rỗng |
| Ô rỗng BO/BP *(nguồn)* | `BM10:BT7892` | **12 ô = 6 HÀNG** *(4962 · 4963 · 6073 · 6507 · 6949 · 7631)* — đúng đính chính orchestrator |
| Ô lỗi `#…` trong `BM:BT` vùng dữ liệu | 63.064 ô | **0** |
| Phân bố kỳ ↔ `phan_bo_ky` | 23 kỳ sổ · 20 kỳ 406 · Σ = 7.883 | **19** khớp CHÍNH XÁC · lệch có tên **4**: `202605` 239/537 · `202606` 0/613 · `202607` 0/686 · `202608` 0/487 · kỳ 406 ngoài sổ **0** |
| Hàng công thức thừa *(`BM7893:BT21238`)* | 13.346 hàng vùng đọc | **9.843** hàng có nội dung, đầu **7893** cuối **17735** · **9.843** ô `BM:BT`-lỗi `#…` *(1/hàng)* · cột A vùng ấy **0** không rỗng |
| Đóng băng LẠI từ lưới của R1 qua `dong_bang_sheet gl_406 … --mong 7883` | — | `[ĐẠT]` exit **0** · `checksum_noi_dung` = `e98f3a699e2de469` · `dong` · `phu` **đúng từng phần tử** ↔ ảnh commit; chỉ khác chuỗi mô tả `cach_doc` *(chuỗi R1 tự đặt)* |

⚠ Hàng `6684 · 6836 · 7500 · 7832` có cột R = `#N/A ()` — xem `F-1`.

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_dap_an_406.py` | 25 passed | `--collect-only` = **25** · nằm trong 188 | ✅ |
| `pytest tests/du_lieu` | 188 passed | **188 passed in 14.89s** | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(script NHÁNH, một mình; `GOC = …/isp-dt4`)* | `KẾT: ĐẠT` · 26=26 · web 3=3 · `12 failed, 2650 passed, 2 xfailed, 14 errors` | **`KẾT: ĐẠT`** · `26 = 26` node id *(thêm 0 · bớt 0)* · `tests/web 3 = 3` · `12 failed, 2650 passed, 2 xfailed, 1 warning, 14 errors` | ✅ |
| `lint-imports` | 11 kept | **`Contracts: 11 kept, 0 broken.`** | ✅ |
| `kiem_tai_lieu.py` *(sau khi thêm sổ + KQ này)* | ĐẠT *(182 file · 1.903 bảng)* | **ĐẠT** *(184 file · 1.908 bảng · 104 mã QĐ)* | ✅ |
| `--collect-only` đếm `::` *(AC-6)* | `163 → 188` · `2653 → 2678` *(+25)* | **`162 → 188` · `2652 → 2678` *(+26)*** *(cf5156e → isp/DT4)* | ⛔ lệch 1 → `DT4-R1-06` |
| `kiem_so_song.py` · `khop_owner.py --kiem` · `soi_bang_tuyen` · `kiem_thuyet_minh` · `pg_migrate` | ⛔ chạy / đỏ pre-existing / OK | **⛔ KHÔNG chạy lại** — ngoài vùng DT4 *(⛔ chạm schema · docs owner)*; BG đã đo `kiem_so_song` + `khop_owner` đỏ **trên nền `cf5156e` cùng lỗi** | — |

## Bảng AC
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1 / DT4-B1** | 7.883 dòng; Σ/kỳ = `phan_bo_ky` ở **19** kỳ *(WO ghi 21 — lỗi đếm, đã đính chính)* + lệch có tên đúng 4 kỳ | 7.883 · 19 khớp · 4 lệch đúng bảng `202605 239/537 · 06 0/613 · 07 0/686 · 08 0/487` *(đếm TỪ NGUỒN của R1, ⛔ từ ảnh)*; cổng `--mong 7883` `[ĐẠT]`; đột biến `LECH_CO_TEN[202605]=240` ⇒ ĐỎ | **ĐẠT** |
| **AC-2 / DT4-B2** | một lát kỳ rỗng ⇒ ĐỎ; trả nguyên ⇒ xanh, ảnh đúng từng byte | Bỏ kỳ `202502` *(đánh số lại liên tục)* ⇒ `[ĐỎ]` exit 1 *(7.600 ≠ 7.883)*; xoá 1 dòng giữa ⇒ exit 2 *(`dong_sheet 3011 ⛔ liên tục`)*; xoá dòng cuối ⇒ exit 1 *(7.882, thiếu `202605`)*; `values=[]` ⇒ exit 2. Trả nguyên ⇒ ĐẠT, `dong`/`phu`/checksum đúng từng phần tử | **ĐẠT** |
| **AC-3 / DT4-B3** | 0 cột Diễn giải/Số CT/Email; vùng đọc ⛔ phủ B:C; máy quét có ca phá | Vùng đọc R1 tự dùng ⛔ có B/C; `COT_THO` của khuôn: `"B"`/`"C"` = **0** lần; lưới thô thêm cột `Email Address` ⇒ exit 2 ⛔ ghi; đột biến `COT_THO` thêm `B` ⇒ ĐỎ; ảnh 7.883 dòng: khoá `{ky,itl_id,D,BM…BT,dong_sheet,thu_tu}`, **0** khoá Diễn giải/Số CT. ⚠ chữ `Diễn`/`Số chứng`/`Email` xuất hiện **1 lần mỗi chữ** — **trong chú thích `ghi_chu_khuon`/`khong_mang_PII`**, ⛔ trong ô dữ liệu *(`dict` · `str` · `None` là mọi kiểu ô)*. Hở: bài quét chỉ canh TÊN cột → `DT4-R1-03` | **ĐẠT** *(+ ghi nhận)* |
| **AC-4** | khuôn tệp riêng; sửa công cụ chung có lý do; `ix_fx.json` + 3 ảnh DT3 đúng từng byte | `git diff --stat cf5156e isp/DT4` = **5 tệp**: BG · bài · ảnh · `tools/dong_bang_sheet.py` *(+2 kiểu `dong_sheet` · `so?`, khai lý do)* · `khuon_dong_bang/gl_406.py` *(mới)*; **0** tệp ảnh cũ chạm ⇒ byte-nguyên; bài ghim sha xanh; mọi bài DT2·DT3 trong 188 xanh | **ĐẠT** |
| **AC-5** | 9.843 hàng công thức: ĐẾM + khai, ⛔ vào bảng chính; hàng có ngày mà BM…BT lỗi ⇒ ĐỎ | R1 đếm độc lập **9.843** *(7893…17735)* = bảng phụ `cong_thuc` 1 dòng; vùng dữ liệu **0** ô lỗi; chèn `#DIV/0!` vào `BM` dòng 110 ⇒ `[ĐỎ]` exit 1; `cot_A_rong=False` ⇒ từ chối *(đột biến bỏ kiểm ⇒ ĐỎ)* | **ĐẠT** |
| **AC-6 / Q8** | nhánh ⛔ có `MONG_PYTEST_TOAN_BO` ⇒ ghi `--collect-only` trước → sau | `grep -c MONG_PYTEST tools/dung_moi_truong_isp.sh` = **0** ✅; số BG khai lệch 1 *(R1 đo `2652 → 2678`)* | **ĐẠT** *(số ghi nhận `-06`)* |
| **DT4-B1 · B2 · B3** | như ISP mục 6/8 | xem AC-1 · AC-2 · AC-3 | **ĐẠT** |
| Mục 8 · "3 vòng review xong" · "điều kiện PUSH" | R1·R2·R3 | R1 = phiếu này; R2·R3 chưa | — *(chưa tới hạn)* |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | Đúng spec Step 12 + WO-111 ⑯. Hai điểm yếu có tên: `F-1` *(cổng `chu` ⛔ mẫu hình)* · `DT4-R1-02` *(suy `ky` ⛔ ghim ranh giới tháng)* | Đột biến **15** chỗ trên bản sao `git archive HEAD` — **13 ĐỎ · 1 sống** `EPOCH+1` *(`-02`)* · 1 đột biến vô hiệu *(M16, ⛔ áp được — loại khỏi mẫu số)* |
| **Dữ liệu** *(nguồn SA, chỉ đọc)* | ảnh = nguồn: **0 lệch / 157.648** · thứ tự dòng giữ *(A tăng dần; `dong_sheet` liên tục 10…7892; đột biến hoán đổi 2 dòng ⇒ ĐỎ)* · số giữ y API *(đột biến làm tròn BM ⇒ ĐỎ)*. ⚠ 4 `itl_id` lỗi | bảng "Đối chiếu ĐỘC LẬP" |
| **Màn hình** | N/A — bước dữ liệu *(⛔ màn)* | ISP Step 12 §4 |

### Đột biến *(R1 tự dựng, trên bản sao `git archive HEAD` ở `/tmp/r1_dt4/cp1`; mẫu số = 15 áp được)*
| # | Đột biến | `pytest tests/du_lieu/test_dap_an_406.py -x` |
|---|---|---|
| M1 | `LECH_CO_TEN[202605]` 239→240 | ĐỎ `…TAI_TAO_dung_tung_byte…` |
| M2 | `thieu_lac` luôn `thieu=[]` | ĐỎ `…cong_ky_DO_khi_lech_NGOAI_4_ky…[thieu_ky_khop]` |
| M3 | `BO/BP` `so?`→`so` | ĐỎ `…TAI_TAO…` |
| M4 | bỏ kiểm `dong_sheet` liên tục | ĐỎ `…KHONG_lien_tuc_thi_TU_CHOI` |
| M5 | bỏ đòi `cot_A_rong` | ĐỎ `…cot_A_rong_False_thi_TU_CHOI` |
| M6 | `COT_THO` thêm `B` | ĐỎ `…TAI_TAO…` |
| **M7** | **`EPOCH` lệch +1 ngày** | **XANH 25/25 ⇒ `DT4-R1-02`** |
| M8 | `_khoa_hop_le(dong_sheet)` luôn `True` | ĐỎ `…khoa_dong_sheet_hop_le` |
| M9 | ảnh: hoán đổi 2 dòng | ĐỎ |
| M10 | ảnh: `BQ` dòng 500 +1e-9 | ĐỎ |
| M11 | ảnh: xoá 1 dòng | ĐỎ |
| M12 | ảnh: bỏ cả lát kỳ `202502` | ĐỎ |
| M13 | ảnh: `BM` làm tròn 2 số lẻ | ĐỎ |
| M14 | ảnh: đổi `itl_id` 1 dòng | ĐỎ |
| M15 | ảnh: thêm khoá `Diễn giải` | ĐỎ |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-1** *(`DT4-R1-01`)* | **`NANG`** | `tools/khuon_dong_bang/gl_406.py` `KIEU_COT["itl_id"]="chu"` · ảnh `dong_sheet` 6684·6836·7500·7832 · `BG-112` "Kết quả đóng băng" | Đọc lại cột R bằng khoá SA: `itl_id == ITL#(hàng−9)` **7.879/7.883**; 4 hàng = `#N/A ()` *(3 khoá trùng giá trị)*; cổng `--mong 7883` vẫn `[ĐẠT]`; BG khai sai *"ITL#1…ITL#7883"*. H4 ⛔ nối được 4 dòng ấy | `DEV` |
| F-2 *(`-02`)* | `NHE` | `gl_406.py` `EPOCH` · bài `:51`/`:99-102` | M7: `EPOCH`+1 ⇒ 25/25 xanh; nguồn 373/7.883 hàng ở cuối tháng | `DEV` |
| F-3 *(`-03`)* | `NHE` | bài PII `:299-340` · `D = chu?` | quét chỉ TÊN cột; cột chữ tự do ⛔ ràng GIÁ TRỊ | `DEV` |
| F-4 *(`-04`)* | `NHE` | `dong_bang_sheet.py` `_khoa_hop_le` | `"²"` ⇒ `ValueError`; `"٣"` ⇒ hợp lệ | `DEV` |
| F-5 *(`-05`)* | `NHE` | ISP `:1355` · WO-111 AC-1 | ISP còn "5 tiền tệ" cho BM–BT; WO "21 kỳ"/"6 ô" ⇒ 19 kỳ · 6 hàng = 12 ô | orchestrator |
| F-6 *(`-06`)* | `NHE` | BG-112 AC-6 | `163→188 (+25)` ↔ đo `162→188`, `2652→2678 (+26)` | `DEV`/orchestrator |
| F-7 *(`-07`)* | `NHE` | ảnh 2,7 MB | dạng dict/dòng; mảng-cột 1,41 MB; hình = hợp đồng chung công cụ | chấp nhận |

## Bài thử mới *(`tests/nghiem_thu/`)*
Không thêm bài — đột biến chạy trên bản sao `git archive`; `F-1` cần sửa khuôn *(⛔ phạm vi của KIỂM)* trước khi thành bài. Bài đề xuất cho vòng sửa: `itl_id` ⛔ khớp `ITL#\d+` ⇒ ĐỎ + 4 hàng khai tên · ghim `_ky_tu_serial` ngày cuối/đầu tháng.

## Câu hỏi cho orchestrator
1. **`F-1`:** **(A)** *(khuyên)* `DEV` sửa khuôn — đòi `itl_id` khớp `ITL#\d+`, khai 4 hàng `#N/A ()` thành lệch có tên *(mong = 4, khác ⇒ ĐỎ)*, sửa BG; ảnh ⛔ đổi nội dung *(chỉ `ghi_chu`/bảng phụ nếu cần ⇒ checksum đổi, cần bài tái tạo cập nhật)*. **(B)** chấp nhận: ghi vào BG 4 hàng + dặn H4 nối 4 dòng ấy bằng `dong_sheet`, nâng R1 sang `ĐẠT` *(⛔ khuyên — "ảnh nối được" là lời hứa của WO ⑯)*.
2. `-05/-06`: orchestrator vá ISP `:1355` + sàn `MONG_PYTEST_TOAN_BO` lấy **+26**.
