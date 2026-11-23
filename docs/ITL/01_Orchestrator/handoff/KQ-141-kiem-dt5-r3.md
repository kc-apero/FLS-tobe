# KQ-141 — biên bản kiểm `BG-138` *(R3 · vòng cuối · ISP 3.1.2 · Step 15 · DT5)*

| | |
|---|---|
| **Thuộc** | `BG-138` · `WO-137` · `KQ-139` · `KQ-140` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R3)* · 2026-11-18 |
| **Phán quyết** | **`ĐẠT` — đủ điều kiện GỘP**: **0 CHẶN · 0 NÊN SỬA mở · 3 GHI NHẬN mới** *(`DT5-R3-01` A2 · `-02` A1 · `-03` B2)*. Mã ⛔ đổi từ R2 *(`git diff 5b8f7b5 isp/DT5` = chỉ `KQ-140` + sổ)*; mã cuối `91a7f1f` |
| **Cổng vào** | `git rev-parse --short isp/DT5` = `5d05a67` ✅ · `dung_moi_truong_isp.sh --cong 5445` `KẾT: ĐẠT` |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT5.md` *(v0.3)* |

## Cổng chạy lại
`PG_DSN=…:5445/fls` · `PG_DSN_TEST=…:5445/fls_test` · `PYTHONUTF8=1`.

| Lệnh | Mong | Đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_dap_an_cfa1.py` *(worktree `isp/DT5`)* | 31 | **31 passed** | ✅ |
| checksum ảnh *(đọc từ `checksum_noi_dung`)* | `6e01ee2b0f2207a3` · `ff9e76976cda1401` | **khớp 2/2** *(+ bài ghim `CHECKSUM_D/Y` xanh)* | ✅ |
| `kiem_tai_lieu.py` *(worktree, kèm sổ v0.3 + phiếu này)* | OK | **ĐẠT** *(252 file · 2.333 bảng · 785 ô ngày)* | ✅ |
| **Cây gộp thử** `/tmp/r3_dt5/gop` = `origin/moi/lam_viec`@`8e3566c` + `merge --no-ff --no-commit isp/DT5` | — | xem dưới | |

## Cây gộp thử *(⛔ commit · ⛔ push)*
| Hạng mục | Đo |
|---|---|
| **Tệp xung đột** | **2** *(đúng dự kiến)*: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` ⇒ `checkout --ours` *(giữ bản nhánh làm việc)*; còn 0 dấu `<<<<<<<` |
| **Số thu thập** | `pytest --collect-only -q` *(venv chung, addopts mặc định)* = **3174** *(= 3141 nhánh làm việc + 33 bài DT5)* ⇒ `MONG_PYTEST_TOAN_BO` 3141 → **3174**; bài ghim `== ["3141"]` → `== ["3174"]`; web **667** giữ |
| `--duong-nen --cong 5445` *(một mình)* | toàn bộ: `12 failed, 3146 passed, 2 xfailed, 14 errors` · tập đỏ **28 = 28** *(thêm 0 · bớt 0 · XFAIL 2 = 2)* · chạy **3174 (mong ≥ 3174)**; web: `3 failed, 664 passed` · **3 = 3** · chạy 667 ⇒ **`KẾT: ĐẠT`** |
| `lint-imports` | **11 kept, 0 broken** |
| `kiem_tai_lieu.py` | **ĐẠT** *(259 file · 2.374 bảng · 790 ô ngày · 104 mã QĐ)* |

## Câu R2 orchestrator đã chốt — sổ ghi rõ
| Mã | Chốt | Trạng thái ở sổ v0.3 |
|---|---|---|
| `DT5-R2-01` *(`_an_toan` danh sách trắng)* | A | **Chuyển backlog DEV** *("siết `_an_toan` thành tập đóng")* |
| `DT5-R2-02` *(ảnh ĐỎ mang ô thô; `--ra` tuỳ ý)* | A | **Chuyển backlog DEV** *("`--ra` phải là đường gitignore" — công cụ chung)* |
| `DT5-R1-05` *(errata ISP)* | A | **Chuyển orchestrator** *(ghi lúc gộp)* |
| `DT5-R1-06` *(ảnh 6,8 MB)* | chấp nhận | **Chấp nhận A — đóng cho DT5** |

⇒ ⛔ hàng nào còn `Mở` mơ hồ; sổ ⛔ NÊN SỬA/CHẶN mở.

## Đột biến mới *(BẢN SAO `git archive isp/DT5` ở `/tmp/r3_dt5/mut`, lưới TỔNG HỢP; ⛔ đụng worktree)*
18 ca *(2 baseline + 16)*, vùng ít đụng *(R2 đã phủ mã HD · `o_loi` · serial · dow · Period 1…12)*. **Mong** khai trước *(Đ5)*; đối chứng baseline `D-base`/`Y-base` exit 0.

| Vùng | Ca | Mong | Đo |
|---|---|---|---|
| **Khuôn Y/H/Q/M** | `Y-h1low` Period `h1` · `Y-H1H2` hoán `H1↔H2` · `Y-yrstr` Year chuỗi · `Y-doc25` `doc_luc` lùi năm | TỪ CHỐI · TỪ CHỐI · TỪ CHỐI · ĐỎ | exit 2 *(Period ⛔ thuộc năm·H·Q·tháng)* · 2 *(thứ tự kỳ vị trí 1)* · 2 · **1** *(`ky_truc 38 ≠ 57`)* ✅ ×4 |
| | `Y-futnum` số ở cột năm tương lai · `Y-fut-dash` `"-"` ở cột tương lai | TỪ CHỐI | exit 2 ×2 ✅ |
| | **`Y-yr.5`** Year `2024.5` | TỪ CHỐI | **exit 0 `[ĐẠT]`** ⛔ ⇒ **`DT5-R3-01`** |
| | **`Y-blankfut`** xoá nhãn Period cột tương lai, có `9.0` | TỪ CHỐI | **exit 0 `[ĐẠT]`** ⛔ ⇒ **`DT5-R3-02`** |
| **Mốc / `ghi_chu_khuon`** | `D-doc17` `doc_luc` lùi 1 ngày | ĐỎ | exit 1 *(`ngay_truc 759 ≠ 760`)* ✅ |
| | `D-docbad` `18/11/2026` · `D-docISO` có múi giờ | TỪ CHỐI · ĐẠT | exit 2 · 0 ✅ ✅ |
| | `D-doc19` *(+1 ngày, lưới tổng hợp ⛔ cột thừa)* | ĐẠT | exit 0 ✅ *(⛔ lỗi: lưới ⛔ có cột 19/11)* |
| | **`D-blankfut`** xoá nhãn Day cột tương lai, có `7.0` · đối chứng `D-futnum` có nhãn | TỪ CHỐI | **exit 0** ⛔ ⇒ **`DT5-R3-02`** · `D-futnum` exit 2 ✅ |
| **Ô lạ** | `D-bool` `True` · `D-numtext` `"12.5"` ở ô dữ liệu | ĐỎ | exit 1 *(`o_loi 26 ≠ 25`)* ×2 ✅ |
| **Ghi ảnh cờ ĐỎ** *(⛔ `--ra`)* | `#REF!` thay `-` ở lưới Y/H/Q/M, chạy ⛔ `--ra` | exit 1 · ghi `cfa1_yhqm.DO.json` · ảnh commit ⛔ đổi | exit 1 · `.DO.json` CÓ · `cong.dat=False` · **sha 2/2 ảnh commit trước = sau** ✅ |

⇒ **16/16 ca có mong khai trước**: **13 đúng mong · 3 ⛔ cắn** *(2 lỗ khác nhau: `Y-yr.5` · `D/Y-blankfut`)*; `Y-doc25` · `D-doc17` chứng minh mốc cổng cắn hai chiều. `ghi_chu_khuon` mốc *(2024-10-20 … ngày đọc · "cắt 52 cột" · "cắt 133 cột")* sinh từ **dữ liệu** *(không hằng)*: đổi `doc_luc` ⇒ cổng ĐỎ trước khi ghi chú sai kịp vào ảnh *(mẫu số: 2/2)*.

## Đo từ ảnh thật *(⛔ đọc lại SA; ảnh R2 đã tái sinh từng byte)*
Y/H/Q/M 2026: **18/19** kỳ có dòng; **`2026M12` = 0 dòng** *(`2026M11` CÓ)*; `ky_truc` 57 = 3 × 19 ⇒ **57 là cột ≤ NĂM đọc** ⇒ `DT5-R3-03`.

## Bảng AC *(tổng hợp ba vòng)*
| AC | Đo | Phán quyết |
|---|---|---|
| AC-1/2 *(mã HD ∈ cây ATL; lạ · vắng · trùng ĐỎ)* | R2 ĐỎ 5/5 *(kể cả 164 hàng toàn-0)*; R3 ⛔ đụng mã — `31 passed` | **ĐẠT** |
| AC-3 *(ô lỗi giữ chuỗi + đếm + phân bố)* | R3 thêm `D-bool` · `D-numtext` ĐỎ | **ĐẠT** |
| AC-4 *(trục · PII)* | 13/16 mong đúng; 2 lỗ cột-tương-lai · Year lẻ = GHI NHẬN, nguồn thật ⛔ dính | **ĐẠT** · ghi nhận |
| AC-5 *(Q8 sàn)* | cây gộp 3174 = thu thập · 28 = 28 · web 3 = 3 | **ĐẠT** |
| Giữ ảnh | checksum 2/2 · `SHA_GIU` 5/5 xanh | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | ĐẠT | cổng mốc cắn hai chiều; phân luồng ĐỎ/TỪ CHỐI đúng; 3 lỗ ⛔ vào dữ liệu hôm nay |
| **Dữ liệu** | ĐẠT | checksum khớp; ảnh R2 tái sinh từng byte; đo `2026M12` = 0 |
| **Màn hình** | N/A | bước dữ liệu |

## Phát hiện mới *(sổ v0.3)*
| F | Mức | Lớp | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|---|
| `DT5-R3-01` | `NHE` | A2 | `cfa1_yhqm.py:92` `int(yr[j])` | Year `2024.5` ⇒ exit 0 | `DEV` *(backlog; khuyến nghị A)* |
| `DT5-R3-02` | `NHE` | A1 | `cfa1_daily.py:82` · `cfa1_yhqm.py:88` ↔ `_cfa1.kiem_tuong_lai_rong` | nhãn cột tương lai trống + ô ≠ 0 ⇒ exit 0 *(2/2)* | `DEV` *(backlog; khuyến nghị A)* |
| `DT5-R3-03` | `NHE` | B2 | spec H6 / `BG-138` | 57 = cột ≤ năm đọc; `2026M12` = 0 dòng | `orchestrator` *(gộp vào errata `R1-05`)* |

## Bài thử mới
Không thêm vào `tests/nghiem_thu/` *(đột biến chạy trên bản sao; vai KIỂM ⛔ sửa mã/bài Dev)*.

## Câu hỏi kèm khuyến nghị *(cho orchestrator)*
- **Q1** `DT5-R3-01`/`-02`: chấp nhận cho DT5 và đưa backlog *"siết trục"* *(A)*, hay quay Dev vá trước gộp *(B)*? **Khuyến nghị A** — nguồn thật ⛔ dính, ⛔ đổi dữ liệu hôm nay; gom cùng backlog `R2-01`/`-02`.
- **Q2** Gộp `isp/DT5`: nhớ đặt `MONG_PYTEST_TOAN_BO = 3174` *(sàn = thu thập cây gộp)* sau khi giữ bản nhánh làm việc ở 2 tệp xung đột. **Khuyến nghị: gộp.**
