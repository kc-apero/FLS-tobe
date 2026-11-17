# KQ-109 — biên bản kiểm `BG-107` *(R2 · ISP 3.1.2 · Step 10 · `DT3`)*

| | |
|---|---|
| **Thuộc** | `BG-107` *(mục "Dựng lại + vòng sửa sau R1")* · `WO-106` · tiếp `KQ-108` |
| **Kiểm bởi** | `fls-test` — R2, phiên mới độc lập · 2026-11-17 · cụm PG **5446** · worktree `.claude/worktrees/isp-dt3` |
| **Đối tượng** | `isp/DT3` @ `cf5156e` *(mã `1497535` + BG `cf5156e`)* trên nền `ae6a744`; `git diff ae6a744 HEAD` = 10 tệp, +5691 −36 |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN** · **2 NÊN SỬA** *(`DT3-R2-01` · `-02`, cả hai thuộc lớp PII — khuyến nghị sửa trước R3)* · 3 GHI NHẬN. 4 phát hiện R1 cần sửa = **ĐÃ SỬA** có bằng chứng ĐỎ-rồi-XANH; 3 còn lại **CHẤP NHẬN** *(việc orchestrator lúc gộp)* |

Sổ riêng: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT3.md` *(v0.2: 4 hàng R1 → ĐÃ SỬA · 3 → CHẤP NHẬN · +5 hàng R2)*.
⛔ Phiếu này ⛔ chứa tên người, số tài khoản, chuỗi tên sheet cá nhân hay mã băm — chỉ số đếm.

## Cổng vào
- git: `isp/S0` @ `c1cf29b` · `isp/DT3` @ `cf5156e` *(khớp sha mong)*; `git log ae6a744..HEAD` = đúng 2 commit `1497535` · `cf5156e`, tác giả/ message ⛔ mang tên người. `git merge-base --is-ancestor 2a31f76 HEAD` ⇒ `2a31f76` **⛔ có trong kho** *(`cat-file -t` ⇒ "Not a valid object name")* và `5a96cd9` cũng vậy ⇒ lịch sử MỚI sạch.
- Dựng môi trường `dung_moi_truong_isp.sh --cong 5446` ⇒ `KẾT: ĐẠT` *(26/26 di trú · pg_verify 25 bảng/view · 11 kept · kho `fls_itl` = 0)*.
- Nguồn SA: khoá ở biến môi trường *(⛔ in)*, đọc **chỉ-đọc**, bản thô ở `/tmp/r2_dt3/tho/` *(ngoài repo, ⛔ commit)*. ⚠ **Chỉ có id Mapping Master** được giao ⇒ ATL · CDT ⛔ đọc lại được *(id bảng tính của hai tab ấy ⛔ có trong lệnh; R2 ⛔ dò bảng tính khác — xem câu hỏi Q1)*.

## Cổng chạy lại
| Lệnh | `BG` nói | R2 đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_anh_cau_hinh.py tests/du_lieu/test_dong_bang_sheet.py` | 67 + 95 *(`65→67` · DT2 `+4`)* | exit 0 · `162 passed in 8.41s`; `--collect-only` = **162** *(0 skipped · 0 deselected)* | ✅ |
| `pytest --collect-only` toàn bộ | `2652` | **2652 tests collected** | ✅ |
| `bash <isp-dt3>/tools/dung_moi_truong_isp.sh --duong-nen --cong 5446` *(log in `GOC = …/isp-dt3`)* | `KẾT: ĐẠT` · 26 = 26 | `12 failed · 2624 passed · 2 xfailed · 14 errors` ⇒ `[ĐẠT] tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `KẾT: ĐẠT` | ✅ |
| `.venv/bin/lint-imports` | `11 kept` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | — | `✅ cong tai lieu DAT … (182 file, 1903 bang, 729 o ngay, 104 ma QD)` *(sau khi thêm phiếu + sổ)* | ✅ |
| Đóng băng lại MM từ lưới SA đọc lại *(`A1:P120` ⇒ **85 hàng**)* | ảnh đúng từng byte | `mapping_master_cfg --mong 73` exit 0 `[ĐẠT]`; `cmp` với ảnh commit ⇒ **trùng từng byte** *(`checksum_noi_dung a47878bf68499130`)* | ✅ |
| Tái tạo lưới từ ảnh ⇒ công cụ ⇒ so ảnh *(ATL · CDT · MM)* | đúng từng byte | 3/3 exit 0, **3/3 byte-trùng** | ✅ |

⛔ `kiem_so_song.py` · `kiem_thuyet_minh.py` · `soi_bang_tuyen.py`: ⛔ chạy — công cụ gắn đường Windows/kho `5433` *(y `KQ-108`)*; ⛔ chạm DT3.

## Quét PII độc lập *(rủi ro số 1)* — số đếm, ⛔ chuỗi
Nguồn chuỗi: lưới SA `A1:P120`, cột **A · B · O** của hàng từ dòng 4 có `B` ⛔ thuộc 21 pháp nhân khai trong khuôn.

| Phép đo | Mẫu số | Kết |
|---|---|---|
| Số hàng cá nhân tìm thấy trên lưới | **7** *(= `an_danh` của ảnh)* | khớp |
| (b) Chuỗi đầy đủ *(A · B · O)* đếm trong 10 tệp diff + message 2 commit + `git log -p ae6a744..HEAD` | **14** chuỗi × **12** nguồn | **0** khớp |
| Token ≥ 4 ký tự của 14 chuỗi, đếm không phân biệt hoa thường | **14** token × 12 nguồn *(0 token trùng với hàng pháp nhân ⇒ không phải loại bớt)* | **0** khớp |
| **Đối chứng DƯƠNG** *(Đ3)* — cùng máy quét trên lưới SA | 14 chuỗi | **28** khớp *(máy không mù)* |
| (a) `sha256_16:<16 hex>` trong `git log -p ae6a744..HEAD` · cây ngọn | — | **1** — chuỗi `0123456789abcdef` TỔNG HỢP ở ca phá của máy quét *(`test_anh_cau_hinh.py:878`)*, ⛔ mã băm thật |
| hex-16 trần ở ô `A·B` của `phu.tho` | **155** ô | **0** |
| `MUOI` · `def bam` · `hashlib` · `MA_BAM` ở `tools/dong_bang_sheet.py` + 5 khuôn | 6 tệp | **0** |
| Hàng `an_danh` có `A = B =` hằng | **7** | **7/7** |

Đối chiếu `hex16` trong ảnh MM: đúng **1** = `checksum_noi_dung` *(không phải mã băm)*. Ảnh ⛔ mang `Email Address`.

## (c) Đối chiếu ảnh ↔ lưới SA đọc lại *(độc lập, mã R2 ở nháp)*
| Ảnh | Đo trên lưới SA | Ô so | Lệch |
|---|---|---|---|
| `mapping_master_cfg.json` | **73** ô `H` khác rỗng từ dòng 7, trùng 0 · **84** dòng có ô ở `A:B·D:G` *(tập dòng khớp ảnh)* | bảng chính 73 × 6 = **438** *(`H` khoá + `I…M`)* · `phu.tho` trừ ô ẩn danh **490** | **0** · **0** |
| `atl_cay.json` *(74 · 6 · 1 trống)* | ⛔ ĐO ĐƯỢC — id bảng tính ⛔ giao | — | — |
| `cdt_correct.json` *(13)* | ⛔ ĐO ĐƯỢC — như trên | — | — |

⇒ MM: nội dung bảng chính **không đổi** so `BG` *(511 = 73 × 7 gồm `dong_sheet`; 438 ô nội dung + `dong_sheet` khớp theo chỉ số dòng)*. ATL · CDT: chỉ có phép so *"ảnh ⇒ lưới ⇒ công cụ ⇒ trùng byte"* *(tuần hoàn — bằng chứng về công cụ, ⛔ về nguồn)*; R1 đã đo hai ảnh với SA 17/11 `1430/1430`, R2 ⛔ lặp. **Không phát hiện** từ chỗ này.

## Ca phá *(bản sao lưới dựng từ ảnh; `--ra` nháp; `git status` sạch)*
| Ảnh | Xoá 1 dòng | Dòng kết | Trả nguyên |
|---|:-:|---|:-:|
| `atl_cay` | exit **1** | `[ĐỎ] --mong 74: 73 dòng ≠ mong 74 · thiếu 1` | exit 0 |
| `mapping_master_cfg` | exit **1** | `[ĐỎ] --mong 73: 72 dòng ≠ mong 73 · phụ tho 83 dòng ≠ mong 84` | exit 0 |
| `cdt_correct` | exit **1** | `[ĐỎ] --mong 13: 12 dòng ≠ mong 13` | exit 0 |

## Đột biến tự dựng *(26 chỗ, bản sao `git archive` ở `/tmp/r2_dt3/mut`, mỗi lần chạy lại 162 bài)*
**22 bị bắt** *(ĐỎ)*, **4 sống sót** — hai ở nhánh PII/cổng ⇒ phát hiện:

| # | Chỗ phá | Kết |
|---|---|---|
| M1 | `chuan_bi` MM: bỏ phép thay hằng | ĐỎ `test_R1_01` |
| M2 | chỉ thay `B`, để `A` rõ | ĐỎ `test_R1_01` |
| M3 | `DONG_DAU_LE` 4→5 | ĐỎ tái tạo byte |
| M4 | coi mọi `B` là pháp nhân | ĐỎ tái tạo byte |
| M5 / M20 | CDT biên dư `>=`→`>` / bỏ hẳn | ĐỎ `test_R1_02` |
| M6 / M21 | ATL biên dư `>=`→`>` / bỏ hẳn | ĐỎ `…[bien_du_vua_khit_du_lieu]` |
| M7 / M25 | `MONG_CAP`: bỏ phép so / đổi 37→36 | ĐỎ |
| M8 | tiêu đề nhóm ⛔ xoá ngăn cha | ĐỎ `…XOA_ngan_cha…` |
| M9 / M10 / M26 | ATL: bỏ kiểm `F` lặp / lệch cấp / dòng trống bị coi là khác | ĐỎ |
| M12 / M13 / M16 | công cụ: bảng phụ ⛔ vào checksum / ⛔ so `PHU_MONG` / lệch mong ⛔ vào lý do | ĐỎ |
| M14 | khoá `ma` ⛔ gộp khoảng trắng | ĐỎ |
| M15 / M23 | MM: bỏ kiểm tiêu đề `A:B` / bỏ đòi vùng bắt đầu `A1` | ĐỎ |
| M19 | `doc_luc`: nhận mọi dạng `fromisoformat` | ĐỎ `…[tuan_ISO]` |
| M24 | LE ⛔ `strip` | ĐỎ tái tạo byte |
| **M22** | **hàng chỉ có `A` (B rỗng) ⛔ ẩn danh** | **XANH — sống sót ⇒ `DT3-R2-01`** |
| M11 | `_NGAY_GIO` nới thành `.*T.*` | XANH ⇒ `DT3-R2-03` ⓒ |
| M17 | CDT bỏ kiểm cột `BR`·`BS` | XANH ⇒ `DT3-R2-03` ⓐ |
| M18 | ATL tiêu đề nhóm bỏ đòi ô `C` | XANH ⇒ `DT3-R2-03` ⓑ |

## Thăm dò PII trên mã ngọn *(bản thô sửa, `--ra` nháp)*
| Thăm dò | Kết |
|---|---|
| P1 hàng chỉ có `A` tổng hợp, dòng 100 | exit 1 *(thêm dòng ⇒ `tho 85 ≠ 84`)* · chuỗi trong ảnh **0** — **mã ĐÚNG** *(lỗ ở bài: M22)* |
| P4 chuỗi tổng hợp ở `E` của dòng THÊM | exit 1 *(`85 ≠ 84`)* · chuỗi vào ảnh **1** |
| **P4b** thay MỘT ô `x` sẵn có ở `D:G` bằng chuỗi tổng hợp *(số dòng ⛔ đổi)* | **exit 0 `[ĐẠT]`** · chuỗi vào ảnh **1** ⇒ `DT3-R2-02` |
| P6 `doc_luc` `…T…Z` · `YYYY-MM-DD` | exit 0 · exit 0 *(lấy NGÀY)* |
| P6 `doc_luc` có phần thập phân giây | exit 2 TỪ CHỐI *(an toàn; ⇒ `DT3-R2-05` ⓑ)* |
| P7 ô `B` là SỐ | exit 2 TỪ CHỐI, lời lỗi chỉ dòng sheet *(⛔ mang giá trị ô)* |

## Đối chiếu từng dòng mục 8 *(ISP Step 10)* + test ID mục 6
| Mục | Mong | R2 đo | Phán |
|---|---|---|---|
| 6 · `DT3-B1` | 74 · 73 · 13 *(ISP/AP ghi 18 — quyết định ⑪ `WO-106`: 18 là khoảng Ô, dữ liệu 13)* · 6 nhóm | `test_DT3_B1_*` 7 bài XANH; ba số đếm trên ảnh = 74 · 73 · 13, nhóm = 6 *(bảng phụ `nhom` mong 6)* | ĐẠT |
| 6 · `DT3-B2` | xoá 1 dòng ở bản sao ⇒ ĐỎ `N−1 ≠ N`, trả nguyên | bảng "Ca phá" ở trên + `test_DT3_B2_xoa_mot_dong_*` 3 ca XANH | ĐẠT |
| 8 · "DT3-B1, B2 xanh/đỏ đúng" | — | xanh/đỏ đúng *(trên)* | ĐẠT |
| 8 · "3 vòng review xong" | R1 · R2 · R3 | R1 `KQ-108` TRƯỢT → dựng lại; R2 = phiếu này; **R3 chưa** | CÒN R3 |
| 8 · "điều kiện PUSH: phát hiện chặn = 0" | 0 CHẶN | **0 CHẶN** sau R2; chờ R3 | ĐẠT (R2) |
| Đ1 · phủ định có số đếm | — | các câu "0" ở phiếu đều kèm mẫu số + đối chứng dương | ✅ |
| Đ3 · tập rỗng | — | `an_danh = 7`, `tho = 84`, `loai = 0` *(0 là mong, mẫu số = bảng chính 73)*; quét PII mẫu số 14 × 12 | ✅ |
| Đ4 · nhãn số | 74/73/13/6 · 81/85/13 hàng về | mỗi con số có nhãn *(dòng mã · mã hd · dòng dữ liệu · tiêu đề nhóm · hàng lưới)* | ✅ |
| Đ5 · `mong` cả hai chiều | `--mong` · `PHU_MONG` · `MONG_CAP` | thêm dòng ⇒ ĐỎ; xoá dòng ⇒ ĐỎ *(ca phá)*; đổi cấp ⇒ ĐỎ *(M7/M25)*; thăm dò P4b nêu **chỗ cổng ⛔ đỏ** ⇒ `DT3-R2-02` | ĐẠT + 1 phát hiện |
| Hành vi DT2 bị đổi *(`doc_luc` nhận ISO-8601 · bài ATL tiêu-đề-nhóm-xoá mong exit 1)* | ⛔ hồi quy | 95 bài `test_dong_bang_sheet.py` XANH; `ix_fx.json` tái tạo từng byte; M19 chứng minh ca ISO bị canh | ĐẠT |

## Xét từng phát hiện R1
| Mã | Mức | Phán R2 | Bằng chứng ĐỎ → XANH |
|---|---|---|---|
| `DT3-R1-01` | CHẶN | **ĐÃ SỬA** | quét PII ở trên *(0/14 × 12, đối chứng dương 28)*; phá lại M1 · M2 · M3 · M4 ⇒ ĐỎ; ngọn XANH. ⚠ hai chỗ yếu còn lại ở lớp này ⇒ `DT3-R2-01` · `-02` *(NÊN SỬA, ⛔ CHẶN: ảnh hiện tại sạch, mã đúng ở nhánh A-only, lỗ là đường tái đóng băng)* |
| `DT3-R1-02` | NÊN SỬA | **ĐÃ SỬA** | M5 · M20 · M6 · M21 ⇒ ĐỎ; ngọn đọc `BR11:BS32` · `A7:F90`, vùng khít ⇒ TỪ CHỐI |
| `DT3-R1-03` | GHI NHẬN | **ĐÃ SỬA** | MM đọc lại từ lưới SA ⇒ byte-trùng; ATL · CDT tái tạo lưới ⇒ byte-trùng; lệch cấp ⇒ ĐỎ *(M10)* |
| `DT3-R1-06` | GHI NHẬN | **ĐÃ SỬA** | M7 · M25 ⇒ ĐỎ; ca phá xoá 1 dòng ATL ⇒ `thiếu 1` |
| `DT3-R1-04` · `-05` · `-07` | GHI NHẬN | **CHẤP NHẬN** | việc orchestrator lúc gộp |

## Phát hiện mới *(chi tiết ở sổ)*
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `DT3-R2-01` | NÊN SỬA | nhánh "A-only" của luật ẩn danh *(`mapping_master_cfg.py`)* | M22 sống sót 162/162 XANH | `DEV` |
| `DT3-R2-02` | NÊN SỬA | cột `D:G` của `phu.tho` ⛔ có danh sách cho phép | P4b: exit 0 `[ĐẠT]`, chuỗi vào ảnh | `DEV` *(+ `BA` nếu đổi dải hợp lệ của `D:G`)* |
| `DT3-R2-03` | GHI NHẬN | kiểm cột CDT · tên nhóm ATL · `_NGAY_GIO` | M17 · M18 · M11 sống sót | `DEV` |
| `DT3-R2-04` | GHI NHẬN | `test_anh_cau_hinh.py:7` · `:9` · `:66` | docstring còn vùng cũ `A7:F88` · `BR11:BS23` | `DEV` |
| `DT3-R2-05` | GHI NHẬN | `test_R1_01` · `doc_luc` thập phân giây | bài "tấn công" luôn `[]`; TỪ CHỐI `…:29.123456+00:00` | `DEV` / orchestrator |

## Bài thử mới
⛔ `tests/nghiem_thu/` — bước dữ liệu, bài của DT3 sống ở `tests/du_lieu/`. Bộ đột biến + thăm dò ở `/tmp/r2_dt3/` *(⛔ commit)*; bài đề xuất cho `DT3-R2-01` · `-02`: xem cột "Khuyến nghị" ở sổ.

## Câu hỏi *(gửi orchestrator)*
- **Q1 · đọc lại ATL · CDT.** **A *(khuyến nghị)*** — R3 nhận id bảng tính của hai tab để tự đọc lại `A7:F90` · `BR11:BS32`, đóng phép so (c) còn thiếu. · **B** — chấp nhận `1430/1430` của R1 + tái tạo byte cho hai ảnh ấy.
- **Q2 · `DT3-R2-01` · `-02`.** **A *(khuyến nghị)*** — Dev sửa trước R3 *(cả hai nhỏ: một bài + một danh sách cho phép ở `D:G`)*; R3 kiểm lại bằng đột biến M22 và thăm dò P4b. · **B** — chuyển hai hàng sang GHI NHẬN, đẩy theo R3.
