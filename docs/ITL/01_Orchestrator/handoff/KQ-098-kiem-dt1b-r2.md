# KQ-098 — biên bản kiểm `BG-096` *(ISP 3.1.2 · Step 5 · DT1b · vòng **R2** — phạm vi sau R1 `KQ-097`)*

| | |
|---|---|
| **Thuộc** | `BG-096` *(mục "Vòng sửa sau R1")* · `WO-095` *(⛔ có tệp — `DT1b-R1-12`)* · `KQ-097` |
| **Kiểm bởi** | `fls-test` *(R2, phiên cloud con, độc lập)* · 2026-11-17 · orchestrator giao |
| **Phạm vi** | `git diff 4b351d3 isp/DT1B` = 4 tệp: `tools/phan_loai_ly_do.py` *(+121/−17)* · `tests/du_lieu/test_phan_loai_ly_do.py` *(+44)* · `tests/du_lieu/test_phan_loai_ly_do_vong_sua_r1.py` *(mới, 261 dòng)* · `BG-096` *(+48)*. Mã `f90afae` + mục BG `39010d9` |
| **Cụm** | cổng **5437**, `PG_DSN`/`PG_DSN_TEST` trỏ `:5437/fls` · `/fls_test`; dựng bằng script `isp-s0` ⇒ `KẾT: ĐẠT` *(7/7 phép kiểm)*. `isp/S0` = `c1cf29b` · `isp/DT1B` = `39010d9` *(khớp mong)* |
| **Phán quyết** | **`ĐẠT`** vòng R2 — **0 CHẶN** · **2 NÊN SỬA** *(`DT1b-R2-01` · `-02`)* · **5 GHI NHẬN** *(`-03`…`-07`)*. 5 NÊN SỬA của R1 đều **ĐÃ SỬA** *(đo ĐỎ trên `4b351d3`, XANH trên ngọn)*. NÊN SỬA mới ⛔ chặn push theo sổ §1 — sửa ở vòng kế hoặc orchestrator ghi lý do chấp nhận. Lượt nhãn THẬT *(`B-DATA-2`)* **⛔ KHÔNG ĐO ĐƯỢC** ở container — ⛔ thuộc vòng này *(orchestrator đã quyết)* |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1b.md` *(v0.2: đổi Trạng thái 12 hàng R1 + thêm 7 hàng)* |

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_phan_loai_ly_do.py …_vong_sua_r1.py` | `76 passed` | `76 passed` *(cũng trên bản sao `git archive`)* | ✅ |
| `pytest tests/du_lieu` | `92 passed` | `92 passed in 14,24 s` | ✅ |
| `pytest --collect-only` toàn bộ | `2.524 → 2.552` | tổng chạy thật `12 failed + 2524 passed + 2 xfailed + 14 errors` = **2.552** · 0 skipped · 0 deselected *(mẫu số tự đo, khớp BG)* | ✅ |
| `--duong-nen` *(script **của nhánh** `isp-dt1b`, log `GOC = …/isp-dt1b`)* | `26 = 26` | **lượt 1: ĐỎ** `36 ≠ 26` *(thêm 10)* vì R2 chạy chồng đợt đột biến dùng chung `fls_test` — ⛔ tính; **lượt 2 (một mình): `26 = 26` toàn bộ · `3 = 3` tests/web · `KẾT: ĐẠT`** | ✅ *(có ghi chú — `DT1b-R2-07`)* |
| `lint-imports` | `11 kept` | `Contracts: 11 kept, 0 broken.` | ✅ |
| đột biến Dev `16/16` | CHẾT | ⛔ tin — R2 tự dựng **53 đột biến** *(§Đột biến)* | — |
| `git status` worktree | — | sạch trước kiểm · sạch sau *(tệp tạm xoá)* | ✅ |

## Bảng 5 NÊN SỬA của R1 + 3 GHI NHẬN Dev báo
| Mã R1 | Phán | Bằng chứng R2 |
|---|---|---|
| `-01` lõi ghép | **ĐÃ SỬA** | 10 đột biến R1 dựng lại **độc lập** *(D01 D02 D04 D0506 D07 D08 D11 D13 D14 D15)* trên bản sao ⇒ **10/10 CHẾT** *(D08 chạy 4 hạt `PYTHONHASHSEED` 0·1·2·3 — chết cả 4)*. Bài XANH trên mã đúng `4b351d3`+`f90afae` *(là bài giết đột biến, ⛔ đổi hành vi mã)* |
| `-02` R5/R6/R3 | **ĐÃ SỬA** | D17 D18 D19 D20 D21 D22 **6/6 CHẾT** |
| `-04` lá tự do | **ĐÃ SỬA** *(còn lỗ lá số — `R2-01`)* | `…DE_XUAT_la_chuoi_TU_DO_bi_chan` **7/7 ĐỎ** trên `4b351d3` *(mã cũ + bài mới)*, **7/7 XANH** trên ngọn. Câu lỗi: cấy câu *Số CT + tên người* vào `nguon.anh_so` ⇒ stderr chỉ `riêng tư: /nguon/anh_so ⛔ đúng đường dẫn hằng` — **⛔ in giá trị** ✅ |
| `-05` vân tay nhãn | **ĐÃ SỬA** *(còn lỗ bài — `R2-02`)* | `…doi_nhan_HAI_dong_cung_ky…` ĐỎ trên cũ → XANH ngọn *(exit 1, `vân tay danh tính nhãn (K13)`)*. R2 thêm: đổi `ghi_chu` giữa hai dòng `KHAC` cùng kỳ ⇒ exit 1 · đổi `lech` giữa hai dòng `KHOA_LECH` cùng kỳ ⇒ exit 1 · đột biến bỏ `lech` / bỏ `ghi_chu` khỏi vân tay CHẾT. Câu `BG-096:176` nay đúng *(đính chính trong BG ✅)* |
| `-06` repo ⛔ ignore | **ĐÃ SỬA** *(còn `R2-02`·`R2-03`)* | ĐỎ trên cũ → XANH ngọn. CLI thật: CSV trong `docs/ITL/_tools/` ⇒ **exit 2** với đường **tuyệt đối · tương đối từ gốc · tương đối từ `docs/`**; `hien_vat/k.csv` *(`.gitignore:17`)* ⇒ đo *(mã 4)*; ngoài repo ⇒ đo |
| `-03` | GHI NHẬN **ĐÃ SỬA** | D23 D24 D28 D30 D31 **5/5 CHẾT** *(R2 đo lại)*; D27 khai phòng thủ chồng ở docstring `_ghi` — chấp nhận |
| `-10` | **ĐÃ SỬA** *(đọc bài)* | `…B4_tep_nhan_THAT…`: tệp thật có mà chưa ghim ⇒ `pytest.fail`. ⛔ chạy được nhánh này ở container *(không có tệp thật)* |
| `-11` | **ĐÃ SỬA** | bài `…R1_11…` ĐỎ trên `4b351d3` → XANH; đột biến bỏ phép kiểm thư mục ở cổng `--tep` CHẾT |
| `-07` `-08` Dev ⛔ sửa | lý do **ĐỨNG** | `-07`: sửa bộ dựng đụng nhãn mong của 20 `TRUNG_SEQ` + 10 `KHOP` ⇒ rủi ro cả suite, cần orchestrator trả nghĩa *(ISP `:814`)*; `-08`: lõi `parse_so` ở làn BE-HC. Cả hai chuyển `WO` riêng. `-09` `-12` ⛔ việc DEV |

## Bảng AC *(phạm vi bước — bản đọc TỔNG HỢP)*
| AC | Mong | Đo được | Phán |
|---|---|---|---|
| AC-1 · B1 | Σ nhãn = 122, mỗi dòng đúng 1 nhãn | `tests/du_lieu` 92 XANH *(bài `…MOI_dong_DUNG_mot_nhan…TUNG_dong`)*; CLI trên bản đọc tổng hợp `20.153` dòng CSV *(bản sao `/tmp`)*: `122` dòng mỗi dòng đúng một nhãn, mã **4** *(MONG nhãn chưa ghim — đúng luật)* | ĐẠT *(tổng hợp)* |
| AC-2 · B2 | tái lập khoá + seq, mẫu số in trước | bài `…TAI_LAP…` XANH; đột biến `tai_lap` = `n` CHẾT | ĐẠT |
| AC-3 · B3 | tệp ra 0 Số CT thô · 0 Diễn giải | quét chữ + lá: 7/7 lá chuỗi chặn; **lá SỐ NGUYÊN 4/4 lọt** ở chế độ cổng ⇒ `R2-01` *(chế độ ĐO còn R5)* | ĐẠT có ghi chú |
| AC-4 · B4 | cổng `--tep` ĐỎ khi lệch MONG | K13 + K1–K10 cắn; nhánh *chưa ghim ⇒ 4* ⛔ có bài ⇒ `R2-02` | ĐẠT có ghi chú |
| nhãn THẬT | — | **⛔ KHÔNG ĐO ĐƯỢC** *(khoá thật chỉ ở máy owner — O10 · `B-DATA-2`)* | ⛔ ngoài phạm vi vòng |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 5 + Đ1–Đ5)* | ĐẠT có ghi chú | Mã đúng ở mọi cổng hành vi đã đo *(S1 S2·7 lá S4 S5)*; còn **2 nhánh đỏ-khi-lạ chưa có bài** *(`R2-02`)* và 1 lỗ độ lớn *(`R2-01`)*. Đ3: mẫu số in trước tỷ lệ; Đ4: số đếm có nhãn; Đ5: `mã 4` khi chưa ghim ⇒ ⛔ bao giờ 0 *(đã chứng minh: đột biến "chưa ghim ⇒ 0" **sống** — tức bài thiếu, mã đúng)*. Đ1: `grep K14 tools/ tests/du_lieu/` = **0**, `BG-096` = 1; K13 = vân tay nhãn khớp quyết định |
| **Dữ liệu** | không áp dụng | ⛔ đọc kho thật; bản đọc **TỔNG HỢP** `_dung(7)`. Đ3: tập khác rỗng *(122 dòng thiếu · 9.967 · 9.845)* |
| **Màn hình** | không áp dụng | công cụ CLI, ⛔ màn |

**Riêng tư:** diff 627 dòng: 0 email thật *(chỉ `ke-toan@vi-du.vn` giả)*, Số CT `4366191234567890` là chuỗi **tổng hợp** của bài; 0 secret; message commit ⛔ PII.

## Kịch bản phá *(S1–S5 của `KQ-097` trên mã mới)*
| | Phá | Mong | Đo |
|---|---|---|---|
| S1 | đổi `nhan`·`lech`·`ghi_chu` hai dòng cùng kỳ | ĐỎ | **exit 1 ✅** *(+ 2 biến thể ghi_chu / lech)* |
| S2 | 7 lá tự do + khoá lạ | ĐỎ × 7 | **7/7 ✅**; ⚠ số nguyên 16 chữ số ở **4 lá số** ⇒ exit **0** × 4 *(`R2-01`)* |
| S3 | `canon_ref` mất chữ số / `parse_so` locale | — | ⛔ đổi *(GHI NHẬN `-07` `-08`, chuyển)* |
| S4 | `phan_loai` khoá tay 6 nhánh | thiết kế | 6/6 ✅ *(đã thành bài `…R1_*`)* |
| S5 | CSV khoá thô trong `docs/ITL/_tools/` | từ chối 2 | **2 ✅** *(3 dạng đường dẫn)*; ⚠ `PATH` ⛔ có `git` ⇒ mã **4** *(`R2-03`)* |
| S6 *(mới)* | `khoa_bam` hex16 tuỳ ý / đổi chỗ 2 dòng | — | exit **0** — ⛔ nằm trong K13; giới hạn hex16 *(`R2-04`)* |

## Đột biến *(R2 tự dựng — tách khỏi bộ của Dev)*
Trên bản sao `git archive isp/DT1B` *(⛔ sửa worktree; `cmp` trả nguyên sau mỗi lượt)*, chạy 76 bài, `-x`:

| Nhóm | Số | Chết | Sống |
|---|:-:|:-:|---|
| D-list R1 *(`-01` `-02`)* dựng lại | 16 | **16** | — |
| D23 D24 D28 D30 D31 *(`-03`)* | 5 | **5** | — |
| mới — R7 · K13 · R8 · cổng `--tep` · lõi ghép · R5 *(13 + 19 áp dụng được; 1 chuỗi neo ⛔ khớp bỏ)* | 32 | 15 | **17** |

**17 sống = 8 tương đương/che chồng** *(R2M3 · B2M17 nuốt lỗi vân tay: input gây lỗi sort bị K4 chặn trước; R2M4 `≥ 0` ⛔ lộ PII; R2M5 thiếu khoá; R2M12 · R2M13 `tai_lap`/bool đã bị `so()` MONG; B2M2 `max(0,·)`; B2M7 chuỗi nguyên)* **+ 9 thật** *(R2M6≡B2M15 git 128 · R2M7 `.resolve()` · R2M11 chưa ghim ⇒ 0 · B2M6 `lech` 4 trường · B2M8 ngưỡng 6→8 · B2M13 `sorted` · B2M18 · B2M19 hex16)* ⇒ `R2-02` `-04` `-05`. Mẫu số thật: **32 − 8 = 24 ⇒ bắt 15/24 = 62,5 %** — phần mới *(R7/K13/R8)* còn lỗ bài, phần cũ *(33 đột biến R1)* **21/21 = 100 %** *(D-list đã áp dụng được)*.
