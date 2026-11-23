# KQ-094 — biên bản kiểm `BG-091` *(ISP 3.1.2 · Step 4 · H2 · vòng **R3** — xác nhận cuối trước gộp + push)*

| | |
|---|---|
| **Thuộc** | `BG-091` *(mục "Vòng sửa sau R1")* · `WO-090` *(spec là ISP Step 4 · H2)* |
| **Kiểm bởi** | `fls-test` *(R3, phiên cloud MỚI, độc lập)* · 2026-11-17 · orchestrator ISP 3.1.2 giao |
| **Phạm vi** | `git diff b701ebb isp/H2` = **chỉ** phiếu R2 + sổ *(`f518bd9`, 2 tệp, ⛔ mã)*; vì vậy R3 **tự chạy lại MỌI cổng trên ngọn** *(⛔ tin số R2)* và soát nhanh **toàn** diff bước `git diff 5e63a90~1 isp/H2 -- fls tools tests docs/ITL/_tools` *(4 tệp: `tools/do_voi_so_luong.py` · `tests/oracle/test_do_voi_hd1.py` · `voi_so_luong.json` · `so_ly_do_hd1.json`; `fls/**` = **0** tệp)* |
| **Cụm** | R3 cổng **5447** *(cụm PG16 riêng, dựng bằng `dung_moi_truong_isp.sh --cong 5447` ở worktree `isp-s0`: `KẾT: ĐẠT` 7/7, 26/26 di trú, `fls_itl = 0 dòng`)* · venv `/home/user/FLS-tobe/.venv` |
| **Sha vào** | `isp/S0` = `c1cf29b` · `isp/H2` = `f518bd9` · `isp/CG1` = `4dfb7bd` *(đúng mong)* · `git status` worktree **sạch** trước và sau kiểm |
| **Phán quyết** | **`ĐẠT` vòng R3** — **0 CHẶN** · **0 NÊN SỬA** *(mới hay mở)* · **2 GHI NHẬN** mở *(`H2-R2-01` · `H2-R2-02` — R3 xét lại, **giữ GHI NHẬN**, lý do §"Xét hai GHI NHẬN của R2")* · **0** phát hiện mới. Thang gộp *(0 CHẶN ∧ 0 NÊN SỬA mở)* **đạt** |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H2.md` *(v0.3: đổi ô Trạng thái hai hàng R2 + ghi chú R3; ⛔ thêm hàng — ⛔ phát hiện mới)* |

## Cổng vào
- Dựng đúng thứ tự brief: `fetch` ba nhánh → `branch -f isp/{S0,H2,CG1}` → worktree `isp-s0` · `isp-h2` → `dung_moi_truong_isp.sh --cong 5447` ⇒ `KẾT: ĐẠT`.
- SHA ba tệp mã/json **trước = sau** kiểm *(⛔ kịch bản nào chạm worktree; đột biến chỉ ở bản sao `git archive` `/tmp/r3_h2/mut_*`)*: `tools/do_voi_so_luong.py` = `122317f8…` · `voi_so_luong.json` = `19dcf674…` · `so_ly_do_hd1.json` = `84510fc3…` *(trùng R2 — đúng: R2→R3 ⛔ đổi mã)*.

## Cổng chạy lại *(R3 tự chạy · `PG_DSN=…:5447/fls` · `PG_DSN_TEST=…:5447/fls_test` · `PYTHONUTF8=1`; log ở `/tmp/r3_h2/`)*
| Lệnh | `BG`/R2 nói | R3 đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/oracle/test_do_voi_hd1.py` | `65 passed` | exit 0 · `65 passed in 30.82s` | ✅ |
| `python -m pytest tests/du_lieu tests/oracle` | `174 passed` | exit 0 · `174 passed in 33.45s` | ✅ |
| `python tools/do_voi_so_luong.py` *(⛔ `--ghi`)* | `Σ 69510/69510` · `③ 5/23` | exit 0 · Σ `9967 · 9845 · 69510/69510` · `① 122 thiếu · 37 loại · 69769 ô · 147 ngược` · `② 0/122 · 0/37` · `③ 5/23 · 2024-10…2025-04` · `④ 18/23 đỏ · 2026-07 … ô 4739/4802` · `⑤ 0 nhãn`; sha json **không đổi** | ✅ |
| `do()` ↔ `voi_so_luong.json` đã commit *(Đ2 — hai nguồn)* | — | so **byte** `json.dumps(do(), indent=1)` ↔ tệp: **bằng nhau** `21976 = 21976` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5447` *(script **nhánh** `isp-h2`; log in `GOC = …/isp-h2`)* | `KẾT: ĐẠT` · `12 failed, 2513 passed, 2 xfailed, 14 errors` · `26=26` · web `3=3` | exit 0 · `KẾT: ĐẠT` · `12 failed, 2513 passed, 2 xfailed, 1 warning, 14 errors in 358.65s` · `26 = 26 (thêm 0 · bớt 0)` · web `3 failed, 661 passed` · `3 = 3` | ✅ |
| `python -m pytest --collect-only` *(⛔ mẫu số — script nhánh cũ hơn S0 nên tự đo, `Đ3`)* | — | thu được **2541** = `12 + 2513 + 2 + 14` ⇒ **chạy hết 2541, 0 skipped, 0 deselected** *(mẫu số ≠ 0, khớp tổng)* | ✅ |
| `.venv/bin/lint-imports` | `11 kept` | exit 0 · `Contracts: 11 kept, 0 broken.` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | — | `OK K1…K6` *(180 tệp · 1895 bảng · 728 ô ngày · 104 mã QĐ — mẫu số ≠ 0)* | ✅ |

> ⚠ Bài đỏ có sẵn ở đường nền *(12 failed + 14 errors + 3 web)* **là của nhánh S0/nền**, `26 = 26` và `3 = 3` node id — H2 **thêm 0 · bớt 0**. ⛔ chạy `pytest` khác trên cùng cụm khi `--duong-nen` đang chạy *(conftest `DROP DATABASE fls_test`)* — R3 chạy **tuần tự**.

## Bảng AC *(= test ID ISP mục 6 · `:728`–`:733`)*
| AC | Mong | R3 đo *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `H2-B1` · sổ rỗng | kỳ đạt = 5 | CLI `③ 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04`; `so_ly_do_hd1.json` = `{"_vi_sao": …, "chu_ky": []}` *(0 chữ ký)* | **ĐẠT** |
| **AC-2** · `H2-B2` · ký giả mọi dòng 2026-07 | *(mong MỚI sau R1, errata ⑩ ⓐ)* ký 23 dòng thiếu ⇒ **vẫn đỏ**; ký thêm 37 dòng tự-soi ⇒ đạt, tổng 6 | **K1′** *(tự dựng, `do()` thật, tệp nhãn + sổ tạm; tập dòng dựng **độc lập**: thiếu `122` · loại `37` · giao `1`; 2026-07 thiếu `23` · loại `37`)*: ký 23 thiếu ⇒ `so_ky_dat 5`, 2026-07 `dat False` *(đo ≠ MONG-có-2026-07 ⇒ ĐỎ)*. **K1′(b)**: ký thêm 37 loại ⇒ `so_ky_dat 6 · 2026-07 dat True · loai_da_ky 37` | **ĐẠT** |
| **AC-3** · `H2-B3` · nhãn chưa ký | vẫn đỏ | CLI `② … có nhãn ĐÃ KÝ 0/122` · `0/37`; chữ ký ⛔ cứu kỳ có `o_100` đỏ *(M6/M1 giết)*; **K5b** *(đổi chỗ một dòng giữa hai nhãn đã ký, tổng y nguyên)* ⇒ ĐỎ `chữ ký cũ, ký lại · vân tay dòng 6bda3a76… ≠ d7ff57d5…` | **ĐẠT** |
| **AC-4** · `H2-B4` · phá MONG | cổng ĐỎ rồi trả nguyên | đột biến **M7** *(MONG thiếu 1 kỳ)* ⇒ ĐỎ; trả nguyên *(sha trước = sau)*; `--ghi` ⛔ ghi khi ĐỎ | **ĐẠT** |
| **AC-5** · mục 7 hiện vật | `so_ly_do_hd1.json` rỗng · `dat_hd1` trong `voi_so_luong.json` | cả hai có; `chu_ky: []`; `dat_hd1` 126 khoá mới *(xem §Hợp đồng CG1)* | **ĐẠT** |
| **AC-6** · mục 3 phạm vi | miễn trừ có chữ ký; `dat_hd1_theo_ky` khai trước *(Đ5)*; chữ ký tổng hợp chỉ trong test | `MONG["dat_hd1_theo_ky"]` `:148` + `MONG["o_moi_dong"]` `:153` khai trước; sổ thật **0** chữ ký; chữ ký giả của R3 = `R3_test` *(⛔ tên người thật)*; ⛔ H15 *(chế độ tự sinh)*, ⛔ H3 *(mã ghép)* | **ĐẠT** |

## Đột biến tự dựng *(Đ5 — "phép không chứng minh được ĐỎ thì chưa tin")* — **14/14 BỊ GIẾT**
Mỗi đột biến chạy trên **bản sao riêng** `git archive isp/H2` *(`/tmp/r3_h2/mut_N`)*, `pytest tests/oracle/test_do_voi_hd1.py -x`; mỗi dòng nêu **bài giết đầu tiên** *(⛔ chỉ "exit 1" — đã đọc tên bài, để chắc ⛔ chết vì lỗi setup)*.

| # | Đột biến | Bài giết đầu tiên |
|---|---|---|
| R3-M1 | bỏ `and o_100` ở `"dat"` | `test_H2_B2_ky_gia_23_dong_thieu_2026_07_thi_2026_07_VAN_DO_vi_dong_tu_soi_loai` |
| R3-M2 | `ky == len(ds)` → `ky >= 0` *(chữ ký 0 dòng cũng cứu)* | `test_H2_B1_so_rong_ky_dat_DUNG_5_tren_23` |
| R3-M3 | chữ ký chỉ buộc `so_dong`, bỏ `van_tay_dong` | `test_H2_B3_doi_cho_MOT_dong_giua_HAI_nhan_DA_KY_la_DO_qua_duong_that` |
| R3-M4 | bỏ kiểm ngày ở tương lai | `test_H2_kiem_dau_vao_moi_luat_CAN[so_ngay_tuong_lai]` |
| R3-M5 | `NHAN_CAM_KY = ()` | `…CAN[so_nhan_KHAC]` |
| R3-M6 | bỏ `om > 0` *(Đ3: `0/0` ⇒ 100 %)* | `test_H2_B3_o_chua_100_thi_chu_ky_KHONG_cuu_duoc_ky` |
| R3-M7 | `MONG["dat_hd1_theo_ky"]` thiếu `2025-04` | `test_H2_B1_so_rong_ky_dat_DUNG_5_tren_23` |
| R3-M8 | vế ô bỏ điều kiện `lk == len(ls)` | `test_H2_B1_so_rong_ky_dat_DUNG_5_tren_23` |
| R3-M9 | `da_ky = set(nhan.values())` *(mọi nhãn tính là đã ký)* | `test_H2_B2_ky_gia_23_…_VAN_DO_vi_dong_tu_soi_loai` |
| R3-M10 | `hom_nay` → `date.max` | `…CAN[so_ngay_tuong_lai]` |
| R3-M11 | cho ký trùng nhãn | `…CAN[so_nhan_ky_trung]` |
| R3-M12 | bỏ kiểm dòng ngoài tập hợp lệ | `…CAN[nhan_dong_ngoai_tap]` |
| R3-M13 | `--ghi` ghi thẳng lên đích *(bỏ `.tam` + `os.replace`)* | `test_H2_ghi_XANH_dut_giua_chung_KHONG_lam_cut_hien_vat` |
| R3-M14 | bỏ phòng thủ `có − chạy` ↔ dòng thiếu liệt kê | `test_H2_phong_thu_chong_co_tru_chay_KHAC_dong_thieu_liet_ke_la_DO` |

## Kịch bản chữ ký *(`do()` thật · tệp tạm · `/tmp/r3_h2/drv.py` — ⛔ commit, lời giao: chỉ KQ + sổ)*
| Ca | Kết quả R3 | Phán |
|---|---|---|
| **K4c** ký `ngay 2099-12-31` / `2026-11-18` *(hôm nay giả `2026-11-17`)* | ĐỎ `ngày … sau hôm nay 2026-11-17 — ⛔ ký trước` | ✅ |
| **K4c** ký `KHAC` · `Khác` · ` khac ` | ĐỎ cả ba `KHAC ⛔ ký được` *(so sau `_goc_nhan`)* | ✅ |
| **K4c** ký `ngay` = hôm nay | ⛔ lỗi về ngày *(chỉ đỏ vì MONG kỳ đạt — đối chứng đúng)* | ✅ |
| **K4d** chữ ký thiếu `van_tay_dong` / thừa khoá lạ | ĐỎ `khoá phải đúng ('nhan','so_dong','van_tay_dong','nguoi_ky','ngay')` | ✅ |
| **K5b** đổi chỗ 1 dòng giữa `KHONG_CO_SAO_KE`·23 và `KHOA_LECH`·14 | ĐỎ `chữ ký cũ, ký lại` *(vân tay dòng lệch; tổng mỗi nhãn y nguyên)* | ✅ |

## Hợp đồng H2 ↔ CG1 *(orchestrator 17/11: giữ NGUYÊN tên, chỉ THÊM)* — đo trên `voi_so_luong.json` của ngọn H2
- So dict phẳng *(nền `9cf9999~1` = trước H2, 479 khoá lá ↔ ngọn H2, 755 khoá lá)*: khoá **MẤT = 0** · khoá THÊM **ngoài `dat_hd1` = 0** *(tất cả 276 khoá thêm dưới `dat_hd1/*`)* · khoá cũ **đổi giá trị = 0** *(ngoài `dat_hd1/_luat`, cố ý)* · 10 khoá top-level y nguyên.
- **5 khoá `dat_hd1`**: `so_ky_dat = 5` · `mau_so.so_ky = 23` · `ky_dat = [2024-10, 2024-11, 2024-12, 2025-03, 2025-04]` · `theo_ky[k].dat` *(kiểu `bool`)* · `theo_ky[k].thieu` *(`2025-01` = 1)* — giữ tên, **5/23** y nguyên.
- **4 khoá `tong.*`**: `o_parity = 69510` · `o_parity_khop = 69510` · `co = 9967` · `loai_tu_soi = 37` — **đủ, giữ tên**.
- **Chạy bài CG1 trên tệp H2**: `git archive isp/CG1` → thay `docs/ITL/_tools/voi_so_luong.json` bằng bản ngọn H2 → `pytest tests/api/test_isp_gates_hd1.py` ⇒ **`33 passed`** *(CG1 ↔ H2 tương thích; khác biệt CG1↔H2 của tệp = chỉ `_luat` + `o_100`, các dòng còn lại thêm dấu phẩy/khoá mới)*.

## Xét hai GHI NHẬN của R2 *(brief (b): "cái nào thực ra phải NÊN SỬA?")* — **cả hai giữ GHI NHẬN**
| Mã | Đo thêm của R3 | Kết luận |
|---|---|---|
| `H2-R2-01` · `NHAN_CAM_KY = ("KHAC",)` chỉ một phần tử | Ký nhãn `OTHER` **chỉ xanh khi tệp nhãn DT1b đã có dòng mang nhãn `OTHER`**: R3 ký `OTHER` khi tệp nhãn **chỉ** có `KHONG_CO_SAO_KE` ⇒ ĐỎ `chu_ky[0] so_dong phải là số nguyên > 0 — có 0` *(chữ ký buộc `so_dong`/`van_tay_dong` vào TẬP dòng mà tệp nhãn gán)*. Nghĩa là bề mặt hở nằm **ở bên GHI** *(DT1b — nơi định nghĩa danh mục đóng, ISP Step 5 `:784`)*, ⛔ ở cổng H2: cổng H2 canh **chữ ký ↔ tệp nhãn**, nhãn là việc của DT1b. Vẫn **chưa** có danh mục đóng để H2 so *(⛔ đoán danh mục — H2 mà tự gõ danh sách nhãn là gõ tên vào danh sách cho cổng xanh)*. Sổ **0** chữ ký ⇒ ⛔ tác động | **GHI NHẬN** — đóng ở **Step 5 · DT1b** *(canh `NHAN_CAM_KY`/kiểm nhãn theo danh mục)* hoặc **trước** chữ ký thật đầu tiên của O8, cái nào tới trước |
| `H2-R2-02` · `hom_nay or date.today()` = đồng hồ máy | `date.today()` đúng **1** chỗ ở `tools/do_voi_so_luong.py:339` *(grep `fls/ tools/ docs/ITL`: các chỗ ghi múi giờ VN khác = `fls/repo/nhip_chup.py:42,77,82` · `tools/kiem_so_song.py:679` — repo **đã có** mẫu `zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")`)*. Máy VN *(Windows của owner)* ⇒ `date.today()` = ngày VN ⇒ **không** lệch; chỉ **runner UTC** *(container/CI)* lệch ~7 giờ đầu ngày VN và lệch theo chiều **an toàn** *(ĐỎ giả, ⛔ XANH giả)*. Sổ **0** chữ ký ⇒ hiện **không** đo được tác động | **GHI NHẬN** — sửa 1 dòng theo mẫu `nhip_chup.MUI` **trước** chữ ký thật đầu tiên của O8, chỉ cần khi O8 ký từ runner UTC |

> ℹ️ Vì cả hai là **điều kiện trước O8** mà không cơ chế nào trong H2 tự canh *(O8 không phải bước H2)*, R3 **ghi rõ điều kiện đóng vào sổ** *(cột Trạng thái)* và đề xuất orchestrator đưa vào tiến độ — xem **Câu hỏi** cuối phiếu.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 4 · AP §5.3.1 HD1 · `CLAUDE.md` Đ1–Đ5)* | **ĐẠT.** Phán `(dòng 1-1 100 % ∨ mọi dòng thiếu ĐÃ KÝ) ∧ [ô]` cài đúng; chữ ký buộc `so_dong` ∧ `van_tay_dong`; `KHAC`/ngày tương lai ĐỎ. **Đ1**: câu phủ định của phiếu này ("`fls/**` 0 tệp", "ngoài `dat_hd1` 0 khoá thêm", "`date.today()` đúng 1 chỗ") **đều có số đếm** từ `git diff --name-only` / so dict / grep trong **chính lượt này**. **Đ3**: `o_100 = om > 0 and …` *(R3-M6 giết)*; mẫu số in ở `①`; `collect-only` = 2541 ≠ 0. **Đ4**: `①…⑤` mỗi số có nhãn; `69510` *(= 9.930 dòng tự nhất quán × 7)* ≠ `69769` *(= 9.967 dòng × 7, mọi dòng)* ≠ `4739/4802` *(ô 2026-07 mọi dòng)*. **Đ5**: `MONG["dat_hd1_theo_ky"]` + `MONG["o_moi_dong"]` khai trước, NO hai chiều; **14/14** đột biến chết | §Cổng · §Đột biến · §Kịch bản |
| **Dữ liệu** *(ảnh đóng băng; kho thật `fls_itl = 0 dòng` — cụm 5447)* | **ĐẠT.** R3 dựng lại tập dòng **độc lập** *(⛔ import `do()`; chỉ `_nap` + đọc fixture)*: thiếu **122** · loại **37** · giao **1** · 2026-07 thiếu **23** ∩ loại **37**. `do()` ↔ JSON đã commit bằng **byte**. Khối `dat_hd1` chỉ có **số đếm + chỉ số dòng + vân tay sha256**, ⛔ tiền/tên/Email/Diễn giải | `/tmp/r3_h2/drv.py` · so byte |
| **Màn hình** | **N/A** — ISP §4 *"Frontend: N/A — lát cắt là lệnh/cổng"*; diff ⛔ chạm `fls/web/**` *(0 tệp)* | `git diff --name-only 5e63a90~1 isp/H2` |

**Riêng tư:** grep dòng THÊM của diff bước *(mã + test + JSON)* với `email · diễn giải · dien_giai · so_ct · secret · password · token · api_key · @domain` = **1** khớp, là decorator `@functools.lru_cache` *(dương tính giả của regex `@`)*. `ThuongCT` = **2** lần, trong chú thích/`_vi_sao` *(vai O8 — ISP `:51`)*, ⛔ dữ liệu. ⛔ `Client secret`. `sao_luu/` · `hien_vat/` ⛔ chạm.

**Làn:** diff bước = 4 tệp mã/json + phiếu `BG-091` + hai `KQ` + sổ — tất cả thuộc làn BE-HC *(ISP Step 4 §4 + §7)*; **0** tệp ngoài làn; ⛔ chạm `fls/**` *(0)*; ⛔ tuyến/màn/config ngoài mục 7 *(chỉ cờ `--ghi` có từ trước)*; ⛔ lấn H3/H15/DT1b *(H2 chỉ ĐỌC tệp nhãn; chế độ tự sinh khai ⛔ xét)*.

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| — | — | — | **0 phát hiện mới.** 2 GHI NHẬN mở là carry-over của R2 *(`H2-R2-01` · `-02`)* — R3 xét lại, giữ mức | — |

## Đối chiếu từng dòng mục 8 *(Exit criteria — ISP `:744`–`:748`)*
| Dòng | Bằng chứng R3 | Phán |
|---|---|---|
| `H2-B1…B4 đúng` | AC-1…AC-4 ĐẠT · `pytest tests/oracle/test_do_voi_hd1.py` = `65 passed` · 14/14 đột biến chết *(gồm 4 chỗ AC-2/3/4 trực tiếp)* | **ĐẠT** |
| `3 vòng review xong` | R1 `KQ-092` ✅ · R2 `KQ-093` ✅ · R3 `KQ-094` *(phiếu này)* ✅ | **ĐẠT** |
| `điều kiện PUSH: đủ R1·R2·R3, phát hiện chặn = 0` | CHẶN = **0** *(R1 0 · R2 0 · R3 0)*; NÊN SỬA mở = **0** | **ĐẠT** |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| — *(R3 ⛔ thêm bài: bài trong `tests/oracle/test_do_voi_hd1.py` đã giết 14/14 đột biến của R3; kịch bản chữ ký ở `/tmp/r3_h2/drv.py` chạy ngoài repo)* | — | — |

## Môi trường R3 để lại
- Cụm **5447** để CHẠY *(R3 ⛔ dừng)*; `fls` `fls_itl = 0 dòng`; `fls_test` do `--duong-nen` dựng lại.
- Worktree `isp-h2`: R3 chỉ THÊM phiếu này + cập nhật sổ; sha ba tệp mã/json **= trước khi kiểm**. Đột biến ở `/tmp/r3_h2/mut_{1..14}`.

## Câu hỏi cho orchestrator *(khuyến nghị)*
**Q1 — Gộp `isp/H2` ngay, hay mở thêm một vòng sửa nhỏ cho `H2-R2-02` trước khi gộp?**
- **A *(khuyến nghị)*:** **gộp + push ngay.** Thang gộp đạt; hai GHI NHẬN có tác động = 0 ở trạng thái hiện tại *(sổ 0 chữ ký)*. Đưa cả hai vào **điều kiện vào của O8** *(chữ ký thật đầu tiên)*: `H2-R2-01` đóng cùng/sau **Step 5 · DT1b** *(danh mục nhãn đóng)*; `H2-R2-02` sửa 1 dòng theo mẫu `fls/repo/nhip_chup.py:MUI`.
- **B:** làm tròn `H2-R2-02` ngay *(1 dòng + 1 bài ca `hom_nay` theo múi VN)* ⇒ kéo thêm R1–R3 mới cho H2 chỉ để đổi hành vi **chưa ai thấy được**.
