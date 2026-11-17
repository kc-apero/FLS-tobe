# KQ-099 — biên bản kiểm `BG-096` *(ISP 3.1.2 · Step 5 · DT1b · vòng **R3** — xác nhận cuối trước gộp)*

| | |
|---|---|
| **Thuộc** | `BG-096` *(mục "Vòng sửa sau R2 (KQ-098)")* · `WO-095` *(⛔ có tệp — `DT1b-R1-12` còn mở)* · `KQ-098` |
| **Kiểm bởi** | `fls-test` *(R3, phiên cloud con, độc lập)* · 2026-11-17 · orchestrator giao |
| **Phạm vi** | `git diff 4a45173 isp/DT1B` = 3 tệp: `tools/phan_loai_ly_do.py` *(+28/−16)* · `tests/du_lieu/test_phan_loai_ly_do_vong_sua_r2.py` *(mới, 188 dòng, 14 bài)* · `BG-096` *(+42, chỉ THÊM)*. Mã `3bf8427` + mục BG `18b5d31` |
| **Cụm** | cổng **5435** — dựng bằng script `isp-s0` ⇒ `KẾT: ĐẠT` *(7/7)*; `isp/S0` = `c1cf29b` · `isp/DT1B` = `18b5d31` *(khớp mong)* |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA mở** *(thang gộp đạt)* · **3 GHI NHẬN mới** *(`DT1b-R3-01…03`)*. 2 NÊN SỬA của R2 *(`-01` `-02`)* đều **ĐÃ SỬA**. Lượt nhãn THẬT *(`B-DATA-2`)* **⛔ KHÔNG ĐO ĐƯỢC** ở container — khoá thật chỉ trên máy owner *(tệp nhãn thật ⛔ có; cổng mặc định exit 3)* |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1b.md` *(v0.3: đổi Trạng thái `R2-01…07` + 3 hàng; **header nâng `v0.1`→`v0.3`** — K1 ĐỎ ở `4a45173`, xanh sau commit này)* |

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu` | `106 passed` | `106 passed in 13,86 s` *(cũng trên bản sao `git archive`: `106 passed`)* | ✅ |
| `pytest tests/du_lieu/…_vong_sua_r2.py` | `14 passed` | 14 bài; trên `4a45173` + tệp bài mới: **`7 failed, 7 passed`** *(5 lá `-01` + `…dung_nguong` + `…git_khong_chay_duoc`)* | ✅ |
| tổng bài toàn bộ | `2.566` | `12 failed + 2538 passed + 2 xfailed + 14 errors` = **2.566** *(mẫu số thu từ lượt chạy thật, ⛔ `--collect-only`)* | ✅ |
| `--duong-nen` *(script **nhánh** `isp-dt1b`, log `GOC = …/isp-dt1b`, chạy MỘT MÌNH)* | `26 = 26` · `3 = 3` | **`26 = 26`** *(thêm 0 · bớt 0)* · **`3 = 3`** tests/web · `KẾT: ĐẠT` *(335 s)* | ✅ |
| `lint-imports` | `11 kept` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `kiem_tai_lieu.py` | K1 ĐỎ ở sổ DT1b | trước: K1 ĐỎ *(`v0.1` < `v0.2`)* ✅ đúng như tác giả báo · sau khi bump header: **K1–K6 ĐẠT** | ✅ |
| cổng mặc định `phan_loai_ly_do.py` | exit 3 | exit **3** `⛔ CHƯA ĐO ĐƯỢC` *(không có tệp nhãn thật)* | ✅ |
| đột biến Dev `11/11` | CHẾT | ⛔ tin — R3 tự dựng **23 đột biến** *(§Đột biến)* | — |
| `git status` worktree | — | sạch trước · sạch sau *(`hien_vat/` · CSV thăm dò xoá; bản sao `/tmp/r3_dt1b/`)* | ✅ |

## Từng phát hiện R2
| Mã R2 | Phán | Bằng chứng R3 *(tái hiện trên `4a45173` rồi trên ngọn)* |
|---|---|---|
| `-01` NÊN SỬA · trần độ lớn 4 lá số | **ĐÃ SỬA** | **5/5 ĐỎ** *(exit 0 — Số CT 16 chữ số dạng int lọt)* trên `4a45173` → **5/5 XANH** *(exit 1, `/mau_so/…`, `str(SO_CT) ⛔ trong stderr)* trên ngọn. `…dung_nguong`: `= 10**6` ĐỎ, `10**6−1` qua. Đột biến M1 `TRAN_DEM`+1 · M5 bỏ trần `so_dong_l1` · M6 `<=` `so_dong_l1` · M8 `any` · M9 · M10 *(in giá trị)* **6/6 CHẾT**. Còn lỗ biên ở 2 lá `khoa_hong` / `dang_khoa_hoc` ⇒ `R3-02` |
| `-02` NÊN SỬA · 3 nhánh thiếu bài | **ĐÃ SỬA** | *(a)* chỉ `phan_bo_nhan` ghim ⇒ mã **4** · M16 *(bỏ `or mong_vt is None`)* **CHẾT**. *(b)* R8 đường tương đối ⇒ mã 2 *(M15 bỏ `.resolve()` ở **lệnh git** SỐNG nhưng vô hại — xem `R3-02`; M13 đảo nhánh ngoài-repo CHẾT)*. *(c)* git 128 ⇒ mã 2 · M14 `!= 0`→`== 1` **CHẾT** |
| `-03` git hỏng ⇒ R8 mã 2 | **ĐÃ SỬA** | bài ĐỎ trên `4a45173` *(mã 0)* → XANH. M11 `return True`→`False` **CHẾT**. CLI thật: `PATH=/nonexistent` + CSV trong `docs/ITL/_tools/` ⇒ **mã 2**; ngoài repo + ⛔ git ⇒ vẫn đo *(mã 4)*; `hien_vat/` + git ⇒ đo *(mã 4)*; CSV trong repo + git ⇒ mã 2 |
| `-04` | **ĐÃ SỬA một phần** | M19 *(bỏ `$`)* · M20 *(`re.I`)* · M21 *(bỏ `sorted`)* **3/3 CHẾT**; M22 `DAI_TOI_THIEU` 6→8 **SỐNG** *(Dev đã khai)*; hex16 ≡ 16 chữ số thập phân ở chế độ cổng — **orchestrator CHẤP NHẬN** |
| `-05` | **ĐÃ SỬA** | M23 `range(5)`→`range(4)` **CHẾT** |
| `-06` K14 | **GHI NHẬN — ⛔ NÊN SỬA** | Đ1 *(hai nơi, đếm)*: `grep K14 tools/ fls/ tests/du_lieu/` = **0** · `docs/ITL` = **5** *(BG-096 ×2 · `KQ-002` *(K14 nghĩa khác)* · `KQ-098` · sổ)* · ISP = **0**. ⇒ BG-096:271 ghi *"ISP đánh số"* là **sai nguồn** *(orchestrator đánh số)*. ISP `Step 5 §6` chỉ có `DT1b-B1…B4`; K14 ⛔ thuộc AC nào ⇒ ⛔ chặn gộp. MONG của K14 chỉ ghim được sau lượt thật ⇒ gộp vào `WO` ghim MONG |
| `-07` đường nền nhạy tải | **ĐÃ XÁC NHẬN** | chạy một mình: `26 = 26`, `KẾT: ĐẠT` |

## Bảng AC *(phạm vi bước — bản đọc TỔNG HỢP)*
| AC | Mong | Đo được | Phán quyết |
|---|---|---|---|
| AC-1 · B1 | Σ nhãn = 122, mỗi dòng đúng 1 nhãn | CLI trên bản đọc tổng hợp `_dung(7)`: **122** dòng đúng một nhãn, mã **4** *(MONG nhãn chưa ghim — đúng luật)*; mẫu số in trước *(122 · 9.967 · 9.845)* | ĐẠT *(tổng hợp)* |
| AC-2 · B2 | chuẩn hoá trước khi băm, tái lập | bài `…TAI_LAP…` XANH *(trong 106)* | ĐẠT |
| AC-3 · B3 | tệp ra 0 Số CT thô · 0 Diễn giải | 7 lá chuỗi chặn + **5 lá số chặn bởi trần** *(R7)*; 6 lá khác ĐỎ nhưng in lại giá trị ⇒ `R3-01` | ĐẠT có ghi chú |
| AC-4 · B4 | cổng ĐỎ khi lệch MONG | K13 + K1–K10 + R7 + R8 cắn *(23 đột biến)* | ĐẠT |
| nhãn THẬT | — | **⛔ KHÔNG ĐO ĐƯỢC** *(O10 · `B-DATA-2`)* — cổng mặc định exit 3 | ⛔ ngoài khả năng container |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | ĐẠT | Phần sửa R2 khớp spec. Đ3: mẫu số mọi phép so ≠ 0 *(122 · 9.967 · 9.845; 106 bài)*. Đ4: `TRAN_DEM` = `10**DAI_TOI_THIEU` = **1.000.000** là **trần của số đếm** *(số đếm lớn nhất đo = 9.967)*, ⛔ lẫn `DAI_TOI_THIEU = 6` *(độ dài token)*. Đ5: cổng R8 **fail-đóng** *(git hỏng ⇒ 2)* và mới được chứng ĐỎ *(M11)*; R7 trần được chứng ĐỎ *(M5)* |
| **Dữ liệu** | không áp dụng | ⛔ đọc kho thật; bản đọc **TỔNG HỢP**. Tập khác rỗng *(122 dòng thiếu)* |
| **Màn hình** | không áp dụng | công cụ CLI |

**Riêng tư:** diff 3 tệp: 0 email · 0 secret · 0 chữ số ≥ 9 ký tự ngoài `4366191234567890` *(3 lần — chuỗi **tổng hợp** của bài `…vong_sua_r2.py`, ⛔ Số CT thật)*; message 2 commit ⛔ PII.

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `DT1b-R3-01` | `NHE` | `phan_loai_ly_do.py` K4 · K5 · K7 · `so()` | Số CT int 16 chữ số cấy vào `dong_sheet` · `thieu` · `so_dong_so` · `tai_lap` · `dem_nhan` · `ky` ⇒ 6/6 exit **1** *(⛔ lọt)* nhưng giá trị **hiện ra stderr** | `DEV` *(khi có dịp)* |
| `DT1b-R3-02` | `NHE` | R7 `khoa_hong`/`dang_khoa_hoc` · R8 | 6 đột biến SỐNG vô hại: `<=` biên 2 lá · bỏ cận dưới ×2 · `isinstance` *(bool)* · `except FileNotFoundError` · bỏ `.resolve()` ở lệnh `git` | `DEV` |
| `DT1b-R3-03` | `NHE` | `_che_do_do` câu từ chối R8 | bản **không có `.git`** + `hien_vat/k.csv` ⇒ mã 2 + *"bị .gitignore … chuyển vào hien_vat/"* — sai lý do *(fail-đóng đúng)* | `DEV` |
| *(ghi nhận `-06`)* | `NHE` | K14 | chưa có mã; BG sai nguồn *"ISP đánh số"* | `BA`/orch |

**⛔ Không có `CHAN`, ⛔ không có `NANG` mở.** Hàng cũ còn mở *(không thuộc phạm vi R3, không phải mã DT1b)*: `R1-07` `R1-08` *(lý do Dev đứng, chuyển `WO`)* · `R1-09` `R1-12` *(việc DEV — `WO-095` vẫn ⛔ có tệp: `ls handoff | grep -c ^WO-095` = **0**)*.

## Đột biến *(R3 tự dựng — trên bản sao `git archive isp/DT1B`, chạy `tests/du_lieu -x`, `cmp` trả nguyên sau mỗi lượt)*
**23** đột biến BIÊN ở phần MỚI *(R7 trần · R8 fail-đóng · `phan_xu` · K4b · hex16 · `sorted` · `lech`)* ⇒ **15 CHẾT · 8 SỐNG**.
- **CHẾT:** M1 M5 M6 M8 M9 M10 *(R7)* · M11 M13 M14 *(R8)* · M16 *(phan_xu)* · M17 *(K4b)* · M19 M20 M21 M23.
- **SỐNG:** M2 M7 *(bỏ cận dưới `0 <=`)* · M3 *(`<=` biên `khoa_hong`/`dang_khoa_hoc`)* · M4 *(`isinstance` bool)* · M12 *(`FileNotFoundError`)* · M15 *(bỏ `.resolve()` ở lệnh git)* — **6 thật, ⛔ lộ PII** ⇒ `R3-02` · **M18** *(bỏ 4 lá khỏi vòng trần: tương đương — `thieu`/`so_dong_so`/`tai_lap` đã bị MONG ghim)* · **M22** *(`DAI_TOI_THIEU` 6→8: Dev đã khai `-04`)*.
- Mẫu số thật = 23 − 1 *(M18)* = 22 ⇒ bắt **15/22 = 68 %**; riêng nhóm mới có hậu quả riêng tư *(R7 trần · R8 fail-đóng · phan_xu)*: **9/9 chết**. Cổng ĐỎ-khi-lạ của bản sửa R2 được chứng minh ĐỎ *(Đ5)*.

## Kịch bản phá *(S1–S5 của `KQ-097` trên mã mới, bản đọc tổng hợp)*
| | Phá | Mong | Đo |
|---|---|---|---|
| S1 | đổi `nhan`·`lech`·`ghi_chu` hai dòng cùng kỳ | ĐỎ | ✅ *(bài `…doi_nhan_HAI_dong…` trong 106)* |
| S2 | 7 lá chuỗi + khoá lạ · 5 lá SỐ int 16 chữ số | ĐỎ × 12 | **12/12 ✅** *(5 lá số nay exit 1 — R2 ghi exit 0)* |
| S4 | `phan_loai` khoá tay 6 nhánh | thiết kế | ✅ *(trong 106)* |
| S5 | CSV khoá thô trong `docs/ITL/_tools/` | từ chối 2 | **2 ✅** *(cả khi `PATH` ⛔ git)*; `hien_vat/` ⇒ đo |
| S7 *(mới)* | Số CT int vào 6 lá còn lại | ĐỎ | 6/6 exit 1 ✅ · ⚠ in giá trị ⇒ `R3-01` |

## Bài thử mới
⛔ Không thêm bài vào `tests/nghiem_thu/` hay `tests/du_lieu/` *(vai KIỂM — sổ luật; 3 phát hiện GHI NHẬN chờ Dev)*. Tập thăm dò + bộ đột biến ở `/tmp/r3_dt1b/` *(⛔ commit)*.

## Câu hỏi cho orchestrator
- **Q1 — `R2-06` K14 có chặn gộp?** **A *(khuyến nghị)***: ⛔ chặn — GHI NHẬN; dựng K14 cùng `WO` ghim MONG lượt thật *(MONG chỉ có sau `B-DATA-2`)* và sửa BG-096:271 *"ISP đánh số"* ⇒ *"orchestrator đánh số"*. **B**: chặn gộp, Dev dựng K14 với MONG = 0 tạm *(thêm lớp tạm sẽ phải sửa lại khi ghim)*.
- **Q2 — sàn `MONG_PYTEST_TOAN_BO`.** Nhánh ⛔ có hằng này; số đo hôm nay **2.566** *(12 + 2538 + 2 + 14)*, đường nền `26 = 26`. **A *(khuyến nghị)***: đặt sàn **2.566** lúc gộp. **B**: đặt theo số của `isp/S0` + 106 bài `du_lieu`.
- **Q3 — nhãn THẬT `B-DATA-2`.** Container ⛔ đo được. **A *(khuyến nghị)***: gộp DT1b với MONG nhãn chưa ghim *(mã 4 — đúng luật)*, mở `WO` riêng cho lượt owner. **B**: giữ DT1b mở đến khi có lượt thật.
