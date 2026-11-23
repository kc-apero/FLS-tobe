# KQ-110 — biên bản kiểm `BG-107` *(R3 · Step 10 · DT3 — xác nhận cuối trước gộp)*

| | |
|---|---|
| **Thuộc** | `BG-107` *(mục "Vòng sửa sau R2")* · `WO-106` · ISP 3.1.2 Step 10 · DT3 |
| **Kiểm bởi** | `fls-test` *(R3, phiên cloud riêng)* · 2026-11-17 |
| **Nền đo** | `isp/DT3` @ `b7428de` *(phạm vi R3 = `git diff e733915 isp/DT3`: 4 tệp, +124 −3)* · cụm PG cổng 5446 |
| **Phán quyết** | **`TRƯỢT`** — **0 CHẶN · 2 NÊN SỬA · 3 GHI NHẬN** *(thang gộp: 0 CHẶN **và** 0 NÊN SỬA)* |

> Sổ riêng: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT3.md` v0.3. ⛔ chứa tên người / số TK / mã băm — chỉ số đếm.
> Cả 5 phát hiện R2 đã xử lý *(4 ĐÃ SỬA · 1 CHẤP NHẬN)*. TRƯỢT vì R3 tìm **hai lỗ bài cùng lớp với `DT3-R2-01/02`** — mã ngọn ĐÚNG, sửa chỉ là thêm bài *(vài phút)*.

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| Dựng `dung_moi_truong_isp.sh --cong 5446` *(từ S0)* | — | `KẾT: ĐẠT` · 26/26 di trú · 25 bảng/view · lint 11 kept | ✅ |
| `pytest tests/du_lieu` | 167 passed | **167 passed** *(7,7 s)* | ✅ |
| `--duong-nen` *(script CỦA NHÁNH, `GOC = …/isp-dt3`, chạy một mình)* | tập đỏ = nền 26 = 26 · web 3 = 3 | **26 = 26** *(thêm 0 · bớt 0)* · web **3 = 3** *(0 · 0)* · `12 failed · 2629 passed · 2 xfailed · 14 errors` · `KẾT: ĐẠT` | ✅ |
| `lint-imports` | 11 kept | **11 kept, 0 broken** | ✅ |
| `kiem_tai_lieu.py` | ĐẠT *(183 file · 104 mã QĐ)* | **ĐẠT** *(183 file · 1914 bảng · 104 mã QĐ)* | ✅ |
| `--collect-only` | 2657 | ⛔ chạy riêng *(đã nằm trong `--duong-nen`: 12+2629+2+14 = 2657 bài)* | ✅ |

## Đối chiếu nguồn SA — ba ảnh *(Q1 = A)*
Đọc lại bằng khoá SA *(env, ⛔ in)*, Sheets API v4 `values.get`, `UNFORMATTED_VALUE`; bản thô chỉ ở `/tmp/r3_dt3/`.
| Ảnh | Vùng đọc | Hàng thô | Đóng băng lại bằng khuôn NHÁNH | Byte so ảnh commit | So từng ô bằng MÃ CỦA R3 *(số ô · số lệch)* |
|---|---|---:|---|---|---|
| `atl_cay.json` | `A7:F90` | 83 | exit 0 `[ĐẠT] --mong 74` | **TRÙNG** *(18 202 B)* | **383 ô so · 0 lệch** *(74 dòng mã × cột B…F = 370 + 6 nhóm × 2 = 12 + 1 dòng trống; cột A số mUSD ⛔ vào ảnh nên ⛔ so — 74 + 6 + 1 ô A bỏ ra ngoài 457 ô đếm)*; hàng thô có chữ ngoài ảnh = 1 *(dòng 89 `CHECK ZONE`, ô canh khuôn khai ⛔ đếm)* |
| `cdt_correct.json` | `BR11:BS32` | 13 | exit 0 `[ĐẠT] --mong 13` | **TRÙNG** *(3 072 B)* | **26 ô · 0 lệch** *(13 hàng × 2)* |
| `mapping_master_cfg.json` | `A1:P120` | 85 | exit 0 `[ĐẠT] --mong 73` | **TRÙNG** *(39 717 B)* | **942 ô · 0 lệch** *(84 hàng `phu.tho` × `A·B·D·E·F·G` = 504 + 73 dòng × `H…M` = 438; 14 ô `A`·`B` ẩn danh so bằng hằng, không so chuỗi)* |

Đ3/Đ4: mẫu số mỗi phép là số ô thật *(⛔ 0)*; ATL: 383 ô so *(⛔ 457: số này gồm cả cột A không so)*. Đóng được phép so còn thiếu của R2: ảnh = đầu ra công cụ **và** = nguồn hiện tại.

## Bảng AC *(mục 8 ISP + `WO-106`)*
| AC | Mong | Đo được | Phán quyết |
|---|---|---|---|
| mục 8 · `DT3-B1` *(ISP §6)* | 3 nguồn ⇒ 74 · 73 · 18 dòng, 6 nhóm | 74 · 73 · **13** dòng *(18 = khoảng ô, 13 = dòng có dữ liệu — quyết định ⑪ `WO-106`, R1/R2 đã nhận)*; 6 nhóm; `test_DT3_B1_*` ×3 tái tạo đúng từng byte | ĐẠT |
| mục 8 · `DT3-B2` | xoá 1 dòng cây ⇒ ĐỎ, trả nguyên | bài `test_KHUON_atl_cay_moi_chot_CAN[…]` ĐỎ khi bỏ dòng / đổi cấp; ảnh trả nguyên *(cmp 3/3)* | ĐẠT |
| mục 8 · 3 vòng review | R1 `KQ-108` · R2 `KQ-109` · R3 `KQ-110` | R3 = phiếu này | ⛔ chưa đủ *(TRƯỢT ⇒ cần R4 nhỏ hoặc Dev sửa 2 bài + R3 xác nhận)* |
| mục 8 · phát hiện CHẶN = 0 | 0 | **0** | ĐẠT |
| thang gộp · NÊN SỬA = 0 | 0 | **2** `DT3-R3-01` `-02` | **TRƯỢT** |
| `CLAUDE.md` Riêng tư | 0 PII | xem dưới — **0 trong diff/lịch sử DT3** | ĐẠT |

## Phát hiện R2 — đối chiếu
| Mã | Mức R2 | R3 | Bằng chứng R3 |
|---|---|---|---|
| `DT3-R2-01` | NÊN SỬA | **ĐÃ SỬA** | đột biến `(A≠∅ hoặc B≠∅)`→`(B≠∅)` ⇒ ĐỎ `test_R2_01`. *(⛔ ĐỎ trên `e733915` — mã khi ấy đã đúng, lỗ ở bài: 13 bài mới đều XANH trên mã `e733915`.)* |
| `DT3-R2-02` | NÊN SỬA | **ĐÃ SỬA** | bài `test_R2_02` chép sang cây `e733915` ⇒ **FAILED** *(exit 0 thay vì 2)*; XANH trên ngọn; đột biến "nhận mọi chuỗi" ⇒ CHẾT; bỏ nhãn `HDCI` khỏi danh sách ⇒ `test_DT3_B1` ĐỎ. *(Nhưng chỉ canh cột `D` — `DT3-R3-02`.)* |
| `DT3-R2-03`ⓐⓑⓒ | GHI NHẬN | **ĐÃ SỬA** | M13 *(bỏ kiểm `BR:BS`)* · M14 *(bỏ đòi ô `C`)* · M15 *(`_NGAY_GIO`→`.*T.*`)* ⇒ cả 3 CHẾT ở đúng bài mới |
| `DT3-R2-04` | GHI NHẬN | **ĐÃ SỬA** | docstring dòng 7·9·66 = `A7:F90`·`BR11:BS32`; vùng cũ còn 7 chỗ, cả 7 là phạm vi DỮ LIỆU/thăm dò biên có chủ ý |
| `DT3-R2-05` | GHI NHẬN | **CHẤP NHẬN** | lý do Dev đứng *(hasattr·gia∉ảnh·A=B=hằng đã ĐỎ ở R2)* |

## Đột biến R3 *(bản sao `git archive isp/DT3`, mỗi lần một chỗ, `tests/du_lieu` 167 bài)*
| # | Phá | Kết |
|---|---|---|
| M1 | ẩn danh `(A≠∅ hoặc B≠∅)`→`(B≠∅)` | **CHẾT** `test_R2_01` |
| M2 | …→`(A≠∅)` *(bỏ nhánh B)* | **SỐNG** ⇒ `DT3-R3-01` |
| M3 | D:G `"DEFG"`→`"D"` | **SỐNG** ⇒ `DT3-R3-02` |
| M4 | D:G `"DEFG"`→`"DEF"` | **SỐNG** ⇒ `DT3-R3-02` |
| M5 | D:G danh sách nhận mọi chuỗi | CHẾT `test_R2_02` |
| M6 | bỏ nhãn `HDCI` khỏi danh sách | CHẾT `test_DT3_B1[mapping_master_cfg]` |
| M7 | ẩn danh `r >= DONG_DAU_LE`→`+1` | **SỐNG** *(hàng 4 thật là pháp nhân)* ⇒ `DT3-R3-03` |
| M8 | miễn pháp nhân bỏ `.strip()` | CHẾT `test_DT3_B1` |
| M9 | `MONG_CAP` cấp 1: 37→36 | CHẾT `test_DT3_B1[atl_cay]` |
| M16 | `MONG_CAP` cấp 3: 11→10 | CHẾT `test_DT3_B1[atl_cay]` |
| M10 | chốt vùng dư ATL `>=`→`>` | CHẾT `test_KHUON_atl_cay_moi_chot_CAN[bien_du_vua_khit_du_lieu]` |
| M11 | chốt vùng dư CDT `>=`→`>` | CHẾT `test_R1_02_cdt_correct_vung_doc_KHONG_du_hang_…` |
| M13–M15 | ba đột biến của `DT3-R2-03` | CHẾT ×3 |

15 phép · 11 CHẾT · 4 sống *(M2 · M3 · M4 · M7)*. *(M12 dựng sai — mẫu khớp 9 lần ⇒ coi ĐỎ theo Đ5, ⛔ tính.)* Cây gốc trả nguyên *(`git status` sạch; phá chỉ ở `/tmp/r3_dt3/mut`)*.

## Quét PII *(số đếm + mẫu số — ⛔ chuỗi)*
- **Token**: lấy từ bản thô MM ở `/tmp`: **7** hàng tài khoản cá nhân *(đúng 7 hàng `an_danh` của ảnh)* ⇒ **21** token *(tên · mã đăng nhập · số TK · cả chuỗi `A`)*. Mẫu số **7 hàng · 21 token** ⛔ 0.
- Trong `git diff e733915 isp/DT3` *(4 tệp, 160 KB nội dung · 14 KB diff)*: **0 / 21**. `git log -p e733915..isp/DT3` *(16 KB)*: **0**. Message 2 commit: **0**. Toàn bộ `git log -p isp/S0..isp/DT3` *(33 commit, 781 KB)*: **0**.
- `sha256_16:` · `MUOI` · `def bam` · `hashlib` · `MA_BAM` ở công cụ + 3 khuôn: **0 · 0 · 0 · 0 · 0**; ở 3 ảnh: **0 · 0 · 0 · 0 · 0**. Mã băm thật `sha256_16:<16 hex>` ở dòng `+` của `S0..DT3`: **1** — là chuỗi GIẢ `0123…cdef` trong một ca thử *(`test_anh_cau_hinh.py:882`, ⛔ băm của dữ liệu thật)*. Dòng `+` nêu tên pattern: nhãn ở phiếu/bài (Đ2 — khai ≠ biên bản).
- `git merge-base --is-ancestor 2a31f76 isp/DT3`: exit **128** *(đối tượng KHÔNG có trong kho)*, ⛔ exit 1 — **xanh trên tập rỗng** *(Đ3)* ⇒ `DT3-R3-05`; bằng chứng thay = các phép quét trên.
- Quét toàn cây `isp/DT3` ra **1 tệp ngoài diff** có 3 số TK cá nhân + mã người *(từ nền `aa1fe94`, ⛔ do DT3)* ⇒ `DT3-R3-04`. 10 tệp khác khớp token ngắn ≤ 7 ký tự = từ thường gặp trong tài liệu nền, ⛔ tính.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | Mã ngọn đúng spec; 2 lỗ ở bài | M2·M3·M4 sống; đọc điều kiện mã ⇒ đúng |
| **Dữ liệu** *(SA chỉ-đọc)* | ĐẠT | 3/3 byte-trùng; 383 + 26 + 942 ô · 0 lệch; kho `fls_itl` = 0 dòng |
| **Màn hình** | N/A | bước dữ liệu, không UI |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `DT3-R3-01` | **NANG** | `mapping_master_cfg.py` luật ẩn danh · bài | M2 sống: 167/167 xanh. Dữ liệu thật: `B-only` = 0/85 hàng | `DEV` |
| `DT3-R3-02` | **NANG** | `mapping_master_cfg.py` `for c in "DEFG"` · `test_R2_02` | M3·M4 sống; `E·F·G` có chữ 30·12·4 ô | `DEV` |
| `DT3-R3-03` | NHE | `DONG_DAU_LE = 4` | M7 sống | `DEV` *(tuỳ)* |
| `DT3-R3-04` | NHE | `Ket-qua-Phan-loai-4-loai-o.md:83·91·92` | 3 số TK cá nhân ở tệp nền, ⛔ thuộc DT3 | `BA`/owner |
| `DT3-R3-05` | NHE | `BG-107` lệnh `is-ancestor` | exit 128 ⇒ phép vô nghĩa | orchestrator |

## Bài thử mới *(`tests/nghiem_thu/`)*
Không thêm tệp bài *(vai KIỂM ⛔ sửa mã hệ thống / bài của Dev)*. 15 đột biến ở trên là bằng chứng; chứng minh đỏ cho `DT3-R3-01/02` = M2 · M3 · M4 *(Dev thêm bài rồi chạy lại đúng 3 đột biến ấy ⇒ phải CHẾT)*.

## Câu hỏi cho orchestrator
1. **Q1 — xử `DT3-R3-01/02` thế nào?** **A** *(khuyến nghị)*: Dev thêm 2 bài *(tham số hoá `test_R2_02` trên `D·E·F·G` + bài hàng chỉ `B`)*; R3 chỉ chạy lại M2·M3·M4 *(không cần R4 đầy đủ)*, rồi gộp. **B**: chấp nhận cả hai là GHI NHẬN vì mã đúng và `B-only`/`E:G` lạ ⛔ xảy ra trên dữ liệu thật; gộp ngay. *(A rẻ — lỗ cùng lớp PII mà R2 đã coi NÊN SỬA.)*
2. **Q2 — `DT3-R3-04`**: **A** *(khuyến nghị)* giao BA che số TK + mã người ở tệp nền *(việc ngoài DT3)*; **B** bỏ qua.
