# KQ-121 — biên bản kiểm `BG-107` *(R3b · Step 10 · DT3 — xác nhận vòng sửa sau `KQ-110`)*

| | |
|---|---|
| **Thuộc** | `BG-107` · `WO-106` · nhánh `isp/DT3` @ `796dad9` |
| **Kiểm bởi** | `fls-test` · 2026-11-17 |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA mở** *(3 hàng R3 `-01/-02/-03` ĐÃ SỬA · `-04/-05` CHẤP NHẬN)* |

## Cổng chạy lại *(Test tự chạy — cụm cổng 5446)*
| Lệnh | Đo | Khớp |
|---|---|:-:|
| `pytest tests/du_lieu` *(ngọn `796dad9`)* | **172 passed** *(R3: 167 ⇒ +5 = 4 ca tham số `D·E·F·G` thay 1, +`test_R3_01`, +`test_R3_03`)* | ✅ |
| `dung_moi_truong_isp.sh --duong-nen` *(script của nhánh)* | toàn bộ: 26 = 26 node id đỏ nền *(thêm 0 · bớt 0)*; `tests/web`: 3 = 3 *(thêm 0 · bớt 0)*; `KẾT: ĐẠT` | ✅ |
| `lint-imports` | **11 kept, 0 broken** | ✅ |
| `kiem_tai_lieu.py` | K1–K6 ĐẠT *(184 file · 1923 bảng · 731 ô ngày · 104 mã QĐ)* | ✅ |
| `git status` worktree sau mọi lần chạy | sạch *(đột biến chỉ ở `/tmp/r3b_dt3/<tên>`, bản `git archive`)* | ✅ |

## Đột biến dựng lại *(bản sao `git archive` @ `796dad9`; mẫu: mỗi phép sửa đã ÁP — `diff` ≠ 0)*
| Đột biến | Mã ở `mapping_master_cfg.py` | Bài giết | Kết quả |
|---|---|---|---|
| **M2** *(R3 sống)* | `(A≠∅ hoặc B≠∅)` → `(A≠∅)` | `test_R3_01_hang_chi_co_B_A_rong_VAN_duoc_an_danh` | **CHẾT** |
| **M3** *(R3 sống)* | `for c in "DEFG"` → `"D"` | `test_R2_02_…[cot_E]` · `[cot_F]` · `[cot_G]` | **CHẾT** |
| **M4** *(R3 sống)* | `"DEFG"` → `"DEF"` *(bỏ `G`)* | `test_R2_02_…[cot_G]` | **CHẾT** |
| M4' *(thêm — bỏ `F`)* | `"DEFG"` → `"DEG"` | `test_R2_02_…[cot_F]` | **CHẾT** |
| **M7** *(R3 sống)* | `r >= DONG_DAU_LE` → `+ 1` | `test_R3_03_bien_duoi_DONG_DAU_LE_hang_dau_tien_duoc_an_danh` | **CHẾT** |
| Trả nguyên *(ngọn)* | — | — | **172 passed XANH** |

5/5 chết ⇒ lỗ bài R3 đã đóng. *(Đ5: đột biến chỉ ĐỎ khi bài đúng nhánh ấy đỏ — đã nêu tên bài.)*

## Bảng AC
| AC | Mong | Đo được | Phán quyết |
|---|---|---|---|
| (1) dựng lại đột biến R3 | mỗi cái bị bài mới giết; trả nguyên XANH | 5/5 chết · ngọn 172/172 xanh | ĐẠT |
| (2) vòng sửa CHỈ thêm bài | `git diff 61c0e20 796dad9 -- tools fls tests/fixture` = 0 dòng | **0** dòng *(mẫu số: diff cả vòng = 2 tệp — `tests/du_lieu/test_anh_cau_hinh.py` +76/−7 và `BG-107` +35; ảnh ⛔ đổi byte nào)* | ĐẠT |
| (3) PII | 0 chuỗi `sha256_16:` · `MUOI` · `def bam` · `hashlib` ở dòng `+` của diff bài; dữ liệu tổng hợp | **0** *(mẫu số: dòng `+` của `tests/` trong `61c0e20..796dad9`, không rỗng — 76+ dòng)*; bài dùng chuỗi `GIALAPBIEN4` · `R \| 99999999_PO USD_…` giả | ĐẠT |
| (4) `-04` · `-05` | CHẤP NHẬN | `-04` ngoài bước *(số TK ở tệp nền `Ket-qua-Phan-loai-4-loai-o.md` — orchestrator chuyển người dùng)*; `-05` ghi nhận | ĐẠT |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | Mã ngọn ĐÚNG spec, bài canh đủ nhánh `A`/`B`/`A·B`, đủ cột `D·E·F·G`, đủ biên dòng 4 | 5 đột biến chết; mã ⛔ đổi |
| **Dữ liệu** | Không chạm kho thật; bài dùng dữ liệu tổng hợp trên ảnh đóng băng | ảnh `tests/fixture` 0 dòng đổi |
| **Màn hình** | Không áp dụng *(bước DATA công cụ)* | — |

## Phát hiện
**Không có phát hiện mới.** `DT3-R3-01…03` ĐÃ SỬA; `-04` *(số TK ở tệp nền, ngoài bước)* · `-05` CHẤP NHẬN. Sổ riêng `SO_PHAT_HIEN_ISP-3.1_DT3.md` v0.4.

## Bài thử mới
Không thêm tệp bài *(vai KIỂM ⛔ sửa bài của Dev)*; bằng chứng = 5 đột biến ở trên.

## Câu hỏi cho orchestrator
**Q1 — gộp `isp/DT3` vào chuỗi?** **A** *(khuyến nghị)*: gộp *(0 CHẶN · 0 NÊN SỬA mở)*, chuyển người dùng `DT3-R3-04`. **B**: chờ người dùng xử `-04` trước. *(A: `-04` ở tệp nền ngoài bước, ⛔ chặn DT3.)*
