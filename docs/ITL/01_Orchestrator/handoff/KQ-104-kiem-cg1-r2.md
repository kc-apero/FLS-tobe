# KQ-104 — biên bản kiểm `BG-102` *(ISP 3.1.2 · Step 7 · CG1 · R2)*

| | |
|---|---|
| **Thuộc** | `BG-102` · `WO-101` *(dải: WO-101 · BG-102 · KQ-103 R1 · KQ-104 R2 · KQ-105 R3)* |
| **Kiểm bởi** | `fls-test` — **R2** *(phiên cloud CON độc lập, ⛔ nhớ R1)* · 2026-11-17 |
| **Đối tượng** | nhánh `isp/CG1` @ `4dfb7bd` *(mã `d6d50f4` — ⛔ đổi mã sau R1; diff `84bcdbf…4dfb7bd` = chỉ `KQ-103` + sổ)* · `isp/S0` @ `c1cf29b` · `isp/H2` @ `f518bd9` · cụm PG riêng **5444** |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 1 NÊN SỬA** *(`CG1-R2-01`, orchestrator, việc lúc gộp)* **· 2 GHI NHẬN** *(`CG1-R2-02` bài hở → DEV · `CG1-R2-03` quy trình)*. Chi tiết: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_CG1.md` v0.2 |

> Điều kiện PUSH *(ISP mục 8)*: R1 ✅ · R2 ✅ *(biên bản này)* · còn **R3** *(`KQ-105`)*; chặn = 0.
> Mọi số R2 **tự chạy lại** trên ngọn *(⛔ tin số R1)*; `export PG_DSN=…:5444/fls PG_DSN_TEST=…:5444/fls_test PYTHONUTF8=1`. Đột biến + bản sao ở `/tmp/r2_cg1/`, ⛔ chạm worktree.

## Cổng chạy lại *(R2 tự đo — so với `BG-102` / R1)*
| Lệnh | `BG-102` · R1 nói | R2 đo | Khớp |
|---|---|---|:-:|
| `pytest tests/api/test_isp_gates_hd1.py` | `33 passed` | exit 0 · `33 passed in 2.95s` | ✅ |
| `pytest tests/api` | 14 node đỏ = đường nền | `3 failed · 379 passed · 11 errors` = 14 node · **0** node `test_isp_gates_hd1` | ✅ |
| `--duong-nen --cong 5444` *(script NHÁNH CG1; log in `GOC = …/isp-cg1`)* | `KẾT: ĐẠT · 26 = 26 · ≥ 2493` | **`KẾT: ĐẠT`** · `26 = 26 (thêm 0 · bớt 0)` · chạy **2600** · skipped 0 · deselected 0 · web `3 = 3 · 664` | ✅ *(lượt 2 — xem ⚠)* |
| `--duong-nen` *(script + đường nền **S0** lên bản sao `git archive isp/CG1`)* | R1: `28 = 28` | **`KẾT: ĐỎ`** · `29 (XFAIL 2) · thêm 1` — node thêm duy nhất `tests/test_dung_moi_truong_isp.py::test_S0_R2_03_hang_mau_so_khai_MOT_cho` *(`:384` ghim `"2493"`, script S0 khai `2490`)*; 28 node kia + `XFAIL 2 = 2` + chạy 2600 + web `3 = 3` đều khớp | ⚠ → `CG1-R2-01` |
| `lint-imports` | `11 kept` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `soi_bang_tuyen.py` | `40 tuyen` | `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `GET /api/fls/v1/gates` *(HTTP thật, `chay_cua.py`, token tạm)* | FINAL DAT · HD1 KHONG DAT | `FINAL` **DAT** `69.510/69.510 ô (… 7 khối × 9.930 dòng giữ sau tự soi)` · `HD1_THANG` **KHONG DAT** `5/23 kỳ đạt` *(18 kỳ đỏ)* · `dat 1 · khong_dat 2 · chua_do_duoc 6` | ✅ |
| `GET …/gates` *(`--tep-do=`)* | +2 chưa đo | cả hai `CHUA DO DUOC` · `dat 0 · khong_dat 1 · chua_do_duoc 8` *(+2)* · 9 cổng, 4 cổng kế toán + `BON_DUONG` vẫn `None` | ✅ |

⚠ **Lượt `--duong-nen` đầu ⛔ dùng được** *(lỗi quy trình của R2, `CG1-R2-03`)*: R2 chạy bộ đột biến *(pytest mở `fls_test`)* chồng lên cổng trên cùng cụm ⇒ `database "fls_test" does not exist` ⇒ `KẾT: ĐỎ · thêm 9` *(9 node `tests/api/test_cua_*_pg.py` — đều ⛔ liên quan CG1)*. Bỏ kết quả ấy *(log giữ `/tmp/r2_cg1/duongnen_cg1_chong_cheo.log`)*, chạy lại **một mình** ⇒ ĐẠT. Số ở bảng là lượt một-mình.

## Trạng thái phát hiện R1
| Mã | Mức R1 | R2 xét | Trạng thái |
|---|---|---|---|
| `CG1-R1-01` | NÊN SỬA | Orchestrator quyết: lúc gộp lấy script + đường nền S0, sàn = số thu thập cây gộp. R2 **đồng ý** — bản S0 bắt đủ: `-rfEx` + 2 `XFAIL` + che DSN; trên mã CG1 chỉ lệch đúng 1 node là **bài ghim 2493** ở `CG1-R2-01`. `git merge-tree isp/CG1 isp/S0` *(chỉ đọc)* ⇒ **CONFLICT** ở cả `tools/dung_moi_truong_isp.sh` lẫn `tests/test_dung_moi_truong_isp.py` ⇒ xung đột **lộ**, ⛔ im lặng | **CHẤP NHẬN** *(+ điều kiện gộp `CG1-R2-01`)* |
| `CG1-R1-03` | NÊN SỬA | Đo **9/9 khoá** trên `isp/H2:docs/ITL/_tools/voi_so_luong.json` @ `f518bd9`: `dat_hd1` ← `mau_so.so_ky=23` · `so_ky_dat=5` · `ky_dat` (5) · `theo_ky` (23 mục, mỗi mục `dat: bool` · `thieu: int`) ; `nguon.so_dong_bang='2026-08-26'` ; `tong.o_parity=69510` · `o_parity_khop=69510` · `co=9967` · `loai_tu_soi=37` *(cả bốn `int`)*. H2 thêm khoá `dong_tu_soi_loai · ngoai_phan · theo_nhan …`, ⛔ bỏ khoá nào. Chép tệp ấy vào bản sao CG1 ⇒ **33/33 xanh** *(tệp khác bản CG1 — `cmp` ⇒ `differ`, ⛔ tập rỗng)*. Sau gộp, `CG1-B1` đọc tệp thật ⇒ ĐỎ nếu ai đổi tên khoá | **CHẤP NHẬN** |
| `-02` Q2 mẫu số `FINAL` | GHI NHẬN | Đo lại tuyến thật: `da_do` nói *"7 khối × 9.930 dòng giữ sau tự soi"*; `ly_do` nói *"sổ có 69.769 ô = 9.967 dòng × 7 khối; 259 ô ⛔ vào mẫu số = 37 dòng tự soi loại × 7 + 0 ô lỗi Sheets"* — hai mẫu số, mỗi số kèm nhãn *(Đ4 đủ)*. Q2 vẫn chờ orchestrator/BA | mở |
| `-04` 3 tệp ngoài bảng TRONG | GHI NHẬN | `lint-imports` 11 kept; mặc định tệp ở `tools/chay_cua.py`, ⛔ ở `fls/` *(đã soi mã `cua.py`/`xu_ly.py`)* | mở *(⛔ lấn)* |
| `-05` `BA-07` §2 | GHI NHẬN | Việc của `fls-ba` | mở |

## Bảng AC *(từng dòng mục 8 + test ID mục 6)*
| AC *(test)* | Mong | R2 đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** `CG1-B1` | `FINAL` dat true · `'69.510/69.510 ô'`; `HD1_THANG` dat false · `'5/23 kỳ đạt'` · `ly_do` kỳ đỏ + dòng thiếu + ngày ảnh | Tuyến HTTP thật *(bảng trên)*; `ly_do` HD1 liệt kỳ `2025-01: 1 · 2025-02: 2 …` kèm `(Σ 122 dòng)` + `2026-08-26`. Bài `CG1-B1` ×4 xanh | **ĐẠT** |
| **AC-2** `CG1-B2` | tệp vắng ⇒ hai `null` · `chua_do_duoc` +2 · ⛔ 200 toàn xanh | `6 → 8`; 4 cổng kế toán + `BON_DUONG` luôn `None` ⇒ ⛔ toàn xanh; `ly_do` chỉ TÊN tệp *(bài `…KHONG_lo_duong_dan_may` xanh; đột biến N11 giết)* | **ĐẠT** |
| **AC-3** `CG1-B3` | bài `/gates` sẵn có + `tests/api` xanh | 14 node đỏ = đường nền; `--duong-nen` `26 = 26`, chạy 2600 | **ĐẠT** |
| **AC-4** `CG1-B4` | phá MONG ⇒ ĐỎ, trả nguyên ⇒ xanh *(hai chiều)* | R2 tự dựng **20 đột biến** khác bộ R1 *(bảng dưới)*: 18 giết, 2 sống *(1 hở bài ⇒ `CG1-R2-02`)*; `CG1-B4` qua tuyến thật xanh; sha trả nguyên | **ĐẠT** *(kèm `CG1-R2-02`)* |
| **AC-5** `Q8` | bài mới cộng sàn cùng commit | `2493` ở nhánh *(+33)*; thực chạy 2600. Điều kiện gộp ở `CG1-R2-01` | **ĐẠT** |
| Mục 8 · `3 vòng review` · `điều kiện PUSH` | R1 · R2 · R3, chặn = 0 | R1 ✅ · R2 ✅ · R3 chưa | *(chờ R3)* |

### Đột biến R2 *(bản sao `git archive isp/CG1` + `voi_so_luong.json` ngọn H2; chạy `tests/api/test_isp_gates_hd1.py -x`)*
| # | Phá | Kết |
|---|---|---|
| N1 | bỏ `khop > o` | giết |
| N2 | bỏ `o_loi < 0` | giết |
| N3 | bỏ `giu < 0` | **sống — tương đương** *(`giu<0 ⇒ o_loi<0` đã bắt)* |
| N4 | bỏ `len(set(ky_dat)) != len(ky_dat)` | **sống — hở bài** *(R2 dựng tệp: gốc ⇒ `None`; đột biến ⇒ `5/23` + `19/23 đỏ`, 5+19>23)* |
| N5 | bỏ `set(ky_dat) != dat_ky` | giết |
| N6 | kỳ đỏ sắp theo `thieu` thay vì thời gian | giết |
| N7 | `_vn` bỏ đổi dấu `.` | giết |
| N8 | `_dem` nhận số âm | giết |
| N9 | `tong` ⛔ coi vắng = 0 | giết |
| N10 | bỏ tiền tố `ô LỆCH` | giết |
| N11 | `ly_do` lộ đường dẫn đầy đủ | giết |
| N12 | `dat` nhận `0/1` thay vì `bool` | giết |
| N13 | `Σ` dòng thiếu thành số kỳ | giết |
| N14 | bỏ `len(theo_ky) != so_ky` | giết |
| N15 | `da_do` FINAL in `co` thay `giu` | giết |
| N16 | `FINAL` `None` kéo `HD1_THANG` `None` | **sống — hở bài** *(chiều ngược 0 bài; mã gốc đúng — R2 đo tay)* |
| N17 | tệp vắng trả `{}` thay `None` | giết |
| N18 | `dat` HD1 = `so_dat > 0` | giết |
| N19 | bỏ Đ3 `so_ky == 0` | giết |
| N20 | JSON mảng lọt | giết |
Sha `fls/repo/doc_bao_cao.py` sau khi trả nguyên: `4ab3dfc4…` *(= bản `isp/CG1`)*.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | **ĐẠT** | `HD1_THANG` chỉ ĐỌC hợp đồng 9 khoá, ⛔ tính lại luật kỳ; Đ3 `0/0` ⇒ `None` *(N19 giết)*; Đ5 cổng xanh đỏ hai chiều; hai khối độc lập *(HD1 hỏng ⇒ FINAL nguyên có bài; chiều ngược đo tay)* |
| **Dữ liệu** | **ĐẠT** *(N/A kho)* | Cổng đọc **tệp đo tĩnh** `voi_so_luong.json` *(ảnh 2026-08-26)*, ⛔ kho; kho `fls` cụm 5444 rỗng `fls_itl = 0`; hợp đồng 9 khoá đo trên tệp H2 ngọn |
| **Màn hình** | **N/A có lý do** | ISP mục 4: *"bước này ⛔ sửa màn"*; diff `84bcdbf…4dfb7bd` ⛔ chạm `fls/web/tep/` |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `CG1-R2-01` | **NÊN SỬA** | `tests/test_dung_moi_truong_isp.py:384` *(CG1)* ↔ `:422` *(S0)* · `tools/dung_moi_truong_isp.sh:420` | script S0 trên mã CG1 ⇒ `thêm 1` = bài ghim `2493`; gộp có CONFLICT ở cả hai tệp. Cùng commit gộp phải: script + đường nền S0, `MONG` = thu thập cây gộp, **một** hằng ghim cùng số | orchestrator |
| `CG1-R2-02` | GHI NHẬN | `tests/api/test_isp_gates_hd1.py:300-312` | N4 · N16 sống *(mã đúng, bài hở)* | DEV *(không chặn)* |
| `CG1-R2-03` | GHI NHẬN | quy trình — cụm chung `fls_test` | hai `pytest` chồng nhau ⇒ ĐỎ giả `database "fls_test" does not exist` | orchestrator *(brief R3)* |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| *(không)* | R2 ⛔ thêm bài nghiệm thu: 18/20 đột biến đã bị bài của Dev giết; hai chỗ hở ghi ở `CG1-R2-02` cho DEV *(vai KIỂM ⛔ sửa bài của Dev, ⛔ sửa mã)* | — |

## Môi trường R2 *(tự dựng)*
`tools/dung_moi_truong_isp.sh --cong 5444` *(script S0)* ⇒ `KẾT: ĐẠT` · sha `isp/S0` `c1cf29b` · `isp/CG1` `4dfb7bd` · `isp/H2` `f518bd9` *(khớp brief)*.
