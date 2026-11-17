# KQ-105 — biên bản kiểm `BG-102` *(ISP 3.1.2 · Step 7 · CG1 · R3 — vòng xác nhận cuối)*

| | |
|---|---|
| **Thuộc** | `BG-102` · `WO-101` *(dải: WO-101 · BG-102 · KQ-103 R1 · KQ-104 R2 · KQ-105 R3)* |
| **Kiểm bởi** | `fls-test` — **R3** *(phiên cloud CON độc lập, ⛔ nhớ R1/R2)* · 2026-11-17 |
| **Đối tượng** | `isp/CG1` @ `c9917ab` *(mã `d6d50f4` y nguyên từ R1; `git diff 4dfb7bd c9917ab` = chỉ `KQ-104` + sổ)* · `isp/H2` @ `6ce257d` · `isp/S0` @ `c1cf29b` · cụm PG riêng **5444** |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA mới · 1 NHẸ đã sửa** *(`CG1-R3-01`)* **· 1 GHI NHẬN mới** *(`CG1-R3-02`)*. `CG1-R2-01` ⇒ **CHẤP NHẬN** *(cây gộp thử ĐẠT)*. Chi tiết: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_CG1.md` v0.3 |

> Điều kiện PUSH *(ISP mục 8)*: R1 ✅ · R2 ✅ · R3 ✅ *(biên bản này)*; phát hiện chặn = **0**.
> Mọi số R3 **tự chạy lại** trên ngọn *(⛔ tin R2)*. `export PG_DSN=…:5444/fls PG_DSN_TEST=…:5444/fls_test PYTHONUTF8=1`. Một cụm ⇒ một `pytest` tại một thời điểm *(`CG1-R2-03`)*: cổng chạy MỘT MÌNH, đột biến chạy riêng. Nháp ở `/tmp/r3_cg1/`.

## Cổng chạy lại
| Lệnh | `BG-102` · R2 nói | R3 đo | Khớp |
|---|---|---|:-:|
| `pytest tests/api/test_isp_gates_hd1.py` | `33 passed` | exit 0 · `33 passed in 3.03s` | ✅ |
| `pytest tests/api` | 14 node đỏ = đường nền | `3 failed · 379 passed · 11 errors` = 14 · **0** của `test_isp_gates_hd1` | ✅ |
| `--duong-nen --cong 5444` *(script NHÁNH CG1; `GOC = …/isp-cg1`; một mình)* | `26 = 26 · ≥ 2493` | **`KẾT: ĐẠT`** · `26 = 26 (thêm 0 · bớt 0)` · chạy **2600** · skipped 0 · deselected 0 · web `3 = 3 · 664` | ✅ |
| `--duong-nen` **cây gộp thử** *(script S0 + `MONG` = thu thập)* | R2 dự đoán ĐẠT nếu sửa cả bài ghim | **`KẾT: ĐẠT`** · `28 = 28 (XFAIL 2 = 2 · thêm 0 · bớt 0)` · chạy **2890** *(mong ≥ 2890)* · web `3 = 3 · 664` | ✅ *(xem dưới)* |
| `lint-imports` | `11 kept` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `soi_bang_tuyen.py` | `40 tuyen` | `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `kiem_tai_lieu.py` | *(R2 ⛔ nêu)* | ngọn R2: **K1 ĐỎ** *(header `v0.1` < changelog `v0.2` của sổ CG1)* ⇒ `CG1-R3-01`; sau sửa header ⇒ K1–K6 **OK** *(187 file · 1.945 bảng · 736 ô ngày · 104 mã QĐ)* | ⛔→✅ |
| `GET /api/fls/v1/gates` *(HTTP thật · `chay_cua.py` + thẻ tạm)* | FINAL DAT · HD1 KHONG DAT | `FINAL` **DAT** `69.510/69.510 ô (… 7 khối × 9.930 dòng giữ sau tự soi)` · `HD1_THANG` **KHONG DAT** `5/23 kỳ đạt` *(kỳ đỏ 18/23 ⇒ 5+18 = 23)* · `dat 1 · khong_dat 2 · chua_do_duoc 6` · 9 cổng | ✅ |
| `GET …/gates` *(`--tep-do=`)* | +2 chưa đo | cả hai `None` · `dat 0 · khong_dat 1 · chua_do_duoc 8` *(+2; ⛔ 200 toàn xanh)* | ✅ |
| Đột biến R3 *(15 chỗ mới, bản sao `git archive`)* | R2: 18/20 giết | **10 giết · 5 sống** *(`CG1-R3-02`)*; sha trả nguyên `2c9244ce…` | ✅ *(kèm GHI NHẬN)* |

## Cây gộp thử *(`CG1-R2-01`)* — ⛔ commit cây thật · ⛔ push
1. `git worktree add --detach /tmp/gop_thu origin/lam_viec` *(@ `7ef70f0`; đã chứa S0 `c1cf29b` — `merge-base lam_viec isp/S0` = `c1cf29b`)*.
2. `git merge --no-ff --no-commit isp/H2` ⇒ sạch. Nhưng gộp lần hai khi chưa commit bị chặn *(`MERGE_HEAD exists`)* ⇒ dùng **bát phân một lệnh**: `git merge --no-ff --no-commit isp/H2 isp/CG1` ⇒ **xung đột đúng 2 tệp**: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(= dự đoán R2; `duong_nen_bai_do.txt` ⛔ xung đột, mang 2 dòng `XFAIL` của S0)*.
3. Giải theo quyết định A: `git checkout --ours <hai tệp>` *(giữ bản S0 đã gộp: `-rfEx` · `XFAIL` · `che_tu_choi`)* + `git add`; đếm thu thập cây gộp `pytest --collect-only` ⇒ **2.890** bài *(219 tệp)* · web **664** ⇒ `sed` `MONG_PYTEST_TOAN_BO=2792 → 2890` *(script `:420`)* **và** bài ghim `test_S0_R2_03_…` `["2792"] → ["2890"]` *(còn một hằng ghim; `test_S0_R3_02_…` đòi hằng = thu thập cũng thoả)*.
4. `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5444` ⇒ **`KẾT: ĐẠT — mọi phép kiểm khớp mong`** · `28 = 28` · `XFAIL 2 = 2` · chạy 2890 ≥ 2890 · exit 0.
5. `git merge --abort` · `git worktree remove --force /tmp/gop_thu` — không còn dấu vết.

⇒ Quyết định A **đủ chặn** lỗi `CG1-R2-01` *(không giải thì ĐỎ `thêm 1`; giải đúng thì ĐẠT)*. ⚠ Hai điểm cho orchestrator: **(i)** gộp thật theo lệnh bát phân thì xung đột hiện đúng hai tệp ấy — ⛔ lấy `--theirs`; **(ii)** `2890` là số của cây thử `lam_viec @ 7ef70f0` + H2 + CG1 — gộp thật phải **đo lại** `--collect-only` *(nhánh làm việc có thể đã tiến)*, ⛔ cộng tay.

## Bảng AC *(từng dòng mục 8 + test ID mục 6)*
| AC *(test)* | Mong | R3 đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **CG1-B1** | `FINAL` dat true `'69.510/69.510 ô'`; `HD1_THANG` dat false `'5/23 kỳ đạt'`, `ly_do` kỳ đỏ + dòng thiếu + ngày ảnh | Tuyến HTTP thật *(bảng trên)*: `69.510` = **ô** Final trên 7 khối × 9.930 dòng giữ; `ly_do` FINAL nói `69.769 ô = 9.967 dòng × 7 khối; 259 ô ⛔ vào mẫu số = 37 dòng tự soi × 7 + 0 ô lỗi Sheets`; HD1 `18/23` kỳ đỏ kèm số dòng thiếu + `2026-08-26`. 33 bài xanh | **ĐẠT** |
| **CG1-B2** | tệp vắng ⇒ hai `null`, `chua_do_duoc` +2, ⛔ 200 toàn xanh | `6 → 8`; 4 cổng kế toán + `BON_DUONG` luôn `None` | **ĐẠT** |
| **CG1-B3** | bài `/gates` sẵn có + `tests/api` xanh | 14 node đỏ = đường nền; `--duong-nen` `26 = 26` · 2600 bài; cây gộp `28 = 28` · 2890 | **ĐẠT** |
| **CG1-B4** | phá MONG ⇒ ĐỎ, trả nguyên ⇒ xanh | 15 đột biến mới: 10 giết, 5 sống ở bài hở *(mã đúng)*; sha trả nguyên | **ĐẠT** *(kèm `CG1-R3-02`)* |
| Mục 8 · *3 vòng review · điều kiện PUSH* | R1 · R2 · R3, chặn = 0 | R1 ✅ · R2 ✅ · R3 ✅ · chặn **0** | **ĐẠT** |

Đ1 *(phủ định)*: câu "⛔ lấn ngoài phạm vi" ở `CG1-R1-04` — grep `tep_do` ở `fls/` **và** `tools/`: mặc định tệp chỉ ở `tools/chay_cua.py` *(`TEP_DO_MAC_DINH`, 1 hit)*, `fls/` 0 mặc định. Đ3: mọi `0` đo trên mẫu số khác 0 *(33 bài · 15 đột biến · 28 node id · 2.890 bài)*. Đ4: `69.510` nhãn **ô** · `9.930` **dòng giữ** · `9.967` **dòng sổ** · `2890` **bài thu thập cây gộp thử** · `2600` **bài chạy trên `isp/CG1`** *(⛔ cùng một số)*. Đ5: cổng cây gộp đã tự chứng minh ĐỎ ở R2 *(`thêm 1`)* và ĐẠT sau giải.

## Xét các phát hiện mở
| Mã | R3 xét | Trạng thái |
|---|---|---|
| `CG1-R2-01` | Cây gộp thử ĐẠT *(trên)* | **CHẤP NHẬN** |
| `CG1-R2-02` *(N4 · N16)* | Có phải NÊN SỬA? **Không**: mã đúng, chỉ hai nhánh phòng thủ ngoài đường dữ liệu thật; N4 chỉ hiện khi tệp tự mâu thuẫn *(đã bị `so_dat`/`set` bắt ở các ngả khác)*. R3 thêm 5 chỗ hở *(`CG1-R3-02`)* — cùng bản chất | GHI NHẬN · DEV *(mở)* |
| `CG1-R1-02` *(mẫu số `FINAL`)* | ISP §2/§8 ghi nguyên chữ `69.510/69.510`; mã ĐÚNG spec; nhãn Đ4 trên tuyến thật đủ | GHI NHẬN · chờ Q2 orchestrator/BA *(⛔ chặn)* |
| `CG1-R1-04` *(3 tệp ngoài bảng TRONG)* | truy về câu "truyền vào tầng 7"; `lint-imports` 11 kept | **CHẤP NHẬN** |
| `CG1-R1-05` *(`BA-07` §2)* | tài liệu BA lệch mã *(`07_API_CONTRACT.md:40` ⛔ nhắc 2 cổng HD1)*; việc `fls-ba` | GHI NHẬN · BA *(mở)* |
| `CG1-R2-03` *(chồng cụm)* | R3 tuân: cổng chạy một mình | ghi |

## Soát nhanh `git diff 575926e isp/CG1 -- fls tools tests` *(7 tệp, +610 −13)*
`doc_bao_cao.py` *(+209)*: hai hàm cổng thuần, ⛔ chạm kho, ⛔ tính lại luật kỳ; `_dem` loại `bool`/âm; Đ3 `0/0 ⇒ None` ở cả hai cổng; `ly_do` chỉ TÊN tệp. `cua.py` · `xu_ly.py` · `chay_cua.py`: ống `tep_do` truyền vào, mặc định chỉ ở rìa `tools/`. `dung_moi_truong_isp.sh` +5 · `test_dung_moi_truong_isp.py` +8: chỉ hằng sàn `2460 → 2493` + ghim *(Q8 = A)*; sẽ thay bằng số cây gộp lúc gộp. `test_isp_gates_hd1.py` +356 *(33 bài)*. **Không thấy lỗi mã mới.**

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | **ĐẠT** | cổng chỉ ĐỌC hợp đồng 9 khoá; Đ3/Đ5 hai chiều; hai khối độc lập |
| **Dữ liệu** | **ĐẠT** *(N/A kho)* | đọc tệp đo tĩnh ảnh 2026-08-26; kho `fls` 5444 rỗng `fls_itl = 0`; `chua_do_duoc` 6 ↔ 8 |
| **Màn hình** | **N/A có lý do** | ISP mục 4: ⛔ sửa màn; diff ⛔ chạm `fls/web/tep/` |

## Phát hiện mới
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `CG1-R3-01` | NHẸ · **đã sửa** | sổ CG1 header · K1 | `kiem_tai_lieu.py` ⇒ `K1 … header v0.1 < changelog v0.2` ⇒ ĐỎ; sau nâng v0.3 ⇒ OK | — |
| `CG1-R3-02` | GHI NHẬN | `tests/api/test_isp_gates_hd1.py` | 5 đột biến sống A2 · A7 · A12 · A14 · A15 *(HD1 12/23 · ngày ảnh toàn trắng · nhánh `OSError` lộ đường dẫn · kỳ đỏ xáo thứ tự · `--tep-do=`)* — mã đúng | DEV *(không chặn)* |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| *(không)* | vai KIỂM ⛔ sửa bài của Dev; 5 hở ghi cho DEV | — |

## Môi trường R3 *(tự dựng)*
`tools/dung_moi_truong_isp.sh --cong 5444` *(script S0)* ⇒ `KẾT: ĐẠT` · sha `isp/CG1` `c9917ab` · `isp/H2` `6ce257d` *(khớp brief)*.
