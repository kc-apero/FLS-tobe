# KQ-093 — biên bản kiểm `BG-091` *(ISP 3.1.2 · Step 4 · H2 · vòng **R2** — chỉ thay đổi SAU R1)*

| | |
|---|---|
| **Thuộc** | `BG-091` *(mục "Vòng sửa sau R1")* · `WO-090` *(spec là ISP Step 4 · H2)* |
| **Kiểm bởi** | `fls-test` *(R2, phiên cloud MỚI, độc lập)* · 2026-11-17 · orchestrator giao |
| **Phạm vi** | `git diff 5e63a90 isp/H2` — **5** tệp *(vòng sửa `c552773` mã + bài + hai JSON · mục BG `b701ebb`)*. Chỉ xét thay đổi SAU R1 *(`KQ-092`)*. Nền `5e63a90` ⛔ thuộc phạm vi |
| **Cụm** | reviewer cổng **5447** *(cụm PG16 riêng của R2; `pg_isready` accepting)* · venv `/home/user/FLS-tobe/.venv` · worktree `/home/user/FLS-tobe/.claude/worktrees/isp-h2` |
| **Quyết định nền** *(orchestrator 16/11, brief; ⛔ kiểm lại — nhận làm chuẩn đo)* | `H2-R1-01`=ⓐ · `-02`=ⓑ · `-06` ⛔ ký `KHAC` + ngày > hôm nay ⇒ ĐỎ · `-03/-04` M15·M17·M18·M19 phải CHẾT · `-05/-07` chỉ khai · 5 khoá `dat_hd1` giữ tên; hôm nay vẫn 5/23 |
| **Phán quyết** | **`ĐẠT` vòng R2** — **0 CHẶN** · **0 NÊN SỬA mới** · **2 GHI NHẬN** *(carry-over hoãn theo quyết định orchestrator)*. Bảy phát hiện R1 đều **ĐÃ SỬA / ĐÃ KHAI** đúng quyết định, R2 tái hiện độc lập từng cái; ⛔ hồi quy do vòng sửa đưa vào |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H2.md` *(R2 chỉ đổi ô Trạng thái bảy hàng cũ — ⛔ thêm hàng: ⛔ phát hiện mới)* |

## Cổng vào *(`05` §5)*
- git thật: `isp/H2` = `b701ebb` *(mục BG)* trên `c552773` *(mã)* trên `5e63a90` *(KQ-092)* — đúng hash brief; `isp/S0` = `c1cf29b` *(khớp mong)*. `git status` worktree **sạch** trước và sau khi kiểm.
- SHA tệp mã trước/sau kiểm **= nhau** *(⛔ kịch bản nào chạm worktree; đột biến chỉ trên bản sao `git archive` ở `/tmp/r2_h2/mut`)*:
  `tools/do_voi_so_luong.py` = `122317f8…` · `voi_so_luong.json` = `19dcf674…` · `so_ly_do_hd1.json` = `84510fc3…`.
- Môi trường dựng bằng `tools/dung_moi_truong_isp.sh --cong 5447` *(script worktree isp-s0)*: `KẾT: ĐẠT` — 7/7 `[ĐẠT]`, 26/26 di trú, `fls_itl = 0 dòng`.

## Cổng chạy lại *(R2 tự chạy · `PG_DSN=…:5447/fls` · `PG_DSN_TEST=…:5447/fls_test` · `PYTHONUTF8=1`; log ở `/tmp/r2_h2/`)*
| Lệnh | `BG` nói | R2 đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/oracle/test_do_voi_hd1.py` | `65 passed` | exit 0 · `65 passed in 20.31s` | ✅ |
| `python -m pytest tests/du_lieu tests/oracle` | `174 passed` *(=155+19)* | exit 0 · `174 passed in 22.52s` | ✅ |
| `python tools/do_voi_so_luong.py` *(⛔ `--ghi`)* | `Σ … 69510/69510` · `③ 5/23 · 2024-10…2025-04` · `④ 2026-07 23·0·0 loại 37·0·0 ô 4739/4802` | exit 0 · trùng từng chữ *(① 122 thiếu·37 loại·69769 ô·147 ngược · ② 0/122·0/122·0/37·0/37 · ③ 5/23 · ④ 2026-07 …loại 37·0·0 ô 4739/4802 · ⑤ 0 nhãn)*; sha json **⛔ đổi** | ✅ |
| `python tools/do_voi_so_luong.py` — 5 khoá CG1 | `so_ky_dat 5 · mau_so.so_ky 23 · ky_dat 5 kỳ · theo_ky[k].dat · .thieu` giữ tên | `5 · 23 · [2024-10,11,12,2025-03,04] · dat True · thieu 0` — **5 khoá giữ tên, 5/23** | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5447` *(script NHÁNH isp-h2 — bản cũ)* | `KẾT: ĐẠT` · `12 failed, 2513 passed, 2 xfailed, 14 errors` · `26=26` · web `3=3` | exit 0 · `KẾT: ĐẠT` · `12 failed, 2513 passed, 2 xfailed, 14 errors in 324.28s` · `26 = 26 (thêm 0·bớt 0)` · web `3 = 3` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5447` *(script isp-s0 — bản MỚI, đối chứng)* | *(brief: chạy thêm bản S0 vì script nhánh cũ hơn + khác hành vi)* | exit 0 · `KẾT: ĐẠT` · `12 failed, 2462 passed, 2 xfailed, 14 errors` · `28 = 28 (XFAIL 2=2 · thêm 0·bớt 0) · chạy 2490 (mong ≥2490) · skipped 0 · deselected 0` · web `3 = 3` | ✅ |
| `/home/user/FLS-tobe/.venv/bin/lint-imports` | `11 kept` | exit 0 · `Contracts: 11 kept, 0 broken.` | ✅ |

> ⚠ **Hai script `--duong-nen` khác hành vi** *(sha khác)*: bản **nhánh** *(cũ, tách từ `2664e25`)* so tập đỏ theo node id *(26=26)*, ⛔ đếm XFAIL, ⛔ gỡ `PYTEST_ADDOPTS` ⇒ `2513 passed`; bản **S0** *(mới, thêm S0-R2/R3)* so cả XFAIL *(28=28)*, gỡ `PYTEST_ADDOPTS`, canh `skipped/deselected = 0` ⇒ `2490 chạy / 2462 passed`. **Cả hai `KẾT: ĐẠT`, cả hai thêm 0 · bớt 0** — vòng sửa H2 ⛔ thêm bài đỏ nào ở cả hai cấu hình. Chênh số `passed` là do hai script đếm khác, ⛔ do H2.

## Bảng AC *(= test ID ISP mục 6 · `:728`–`:733`, đối chiếu quyết định orchestrator)*
| AC | Mong *(sau quyết định)* | R2 đo *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `H2-B1` · sổ rỗng | kỳ đạt = 5 | CLI exit 0 `③ 5/23 · 2024-10·2024-11·2024-12·2025-03·2025-04`; sổ thật `chu_ky: []`; 11 bài B1 PASSED | **ĐẠT** |
| **AC-2** · `H2-B2` · ký giả 2026-07 *(mong MỚI, errata ⑩/ⓐ)* | ký 23 dòng thiếu ⇒ **VẪN ĐỎ**; ký thêm 37 dòng tự-soi ⇒ ĐẠT, tổng 6 | **K1′ qua `phan_hd1` thật** *(mã c552773)*: ký 23 thiếu ⇒ `so_ky_dat 5` · 2026-07 `dat False · da_ky 23/23 · loai_da_ky 1/37 · o_100 False · ô 4739/4802`. **K1′(b)**: ký thêm 37 loại ⇒ `so_ky_dat 6 · 2026-07 dat True · loai_da_ky 37/37`. Đột biến **R1-M3** *(bỏ `and o_100`)* **BỊ GIẾT 3 bài**, gồm **đường thật** `test_H2_B2_qua_DUONG_THAT_…`. 3 bài B2 PASSED | **ĐẠT** |
| **AC-3** · `H2-B3` · nhãn chưa ký | vẫn đỏ | CLI `② … có nhãn ĐÃ KÝ 0/122`; 9 bài B3 PASSED; o_100 đọc `o_moi_dong*` *(N6/N9 giết)* | **ĐẠT** |
| **AC-4** · `H2-B4` · phá MONG | cổng ĐỎ rồi trả nguyên | 2 bài B4 PASSED; `--ghi` ⛔ ghi khi ĐỎ *(sha json ⛔ đổi suốt R2)* | **ĐẠT** |
| **AC-5** · mục 7 hiện vật | `so_ly_do_hd1.json` rỗng · `dat_hd1` trong `voi_so_luong.json` | `{"_vi_sao": …, "chu_ky": []}`; `dat_hd1` khoá cũ giữ tên+giá trị *(§Hợp đồng CG1)* | **ĐẠT** |
| **AC-6** · mục 3 phạm vi | miễn trừ có chữ ký; `dat_hd1_theo_ky` khai trước *(Đ5)*; chữ ký tổng hợp chỉ trong test | `MONG["dat_hd1_theo_ky"]` `:148` + `MONG["o_moi_dong"]` `:153` khai trước; sổ thật 0 chữ ký; chữ ký giả của bài = `R2_test`/`TONG_HOP…` *(⛔ tên người thật)* | **ĐẠT** |

## Phát hiện R1 → trạng thái R2 *(Đ: mỗi dòng R2 tái hiện ĐỘC LẬP; ⛔ tin số BG)*
| Mã | Mức | Quyết định | R2 tái hiện *(mã c552773)* | Trạng thái |
|---|---|---|---|---|
| `H2-R1-01` | NÊN SỬA | ⓐ | Vế [ô] nay đọc `o_moi_dong` *(MỌI dòng)*. **K1′**: ký 23 dòng thiếu 2026-07 ⇒ kỳ **VẪN ĐỎ** *(`o_100 False`, ô 4739/4802, `loai_da_ky 1/37`)*; chỉ ĐẠT khi ký nốt 37 dòng tự-soi *(K1′(b): `loai_da_ky 37/37`)*. R1-M3 giết trên **đường thật**. `dong_tu_soi_loai` công bố TẬP 37 dòng *(`2026-07`)* · `dat_hd1.theo_ky[k]` mang `loai_tu_soi`/`loai_da_ky`/`o_moi_dong*`. | **ĐÃ SỬA** |
| `H2-R1-02` | NÊN SỬA | ⓑ | `KHOA_CHU_KY` = 5 khoá *(+`van_tay_dong`)*. **K4d**: chữ ký 4 khoá cũ *(thiếu `van_tay_dong`)* ⇒ ĐỎ `khoá phải đúng (…5 khoá)`; thêm khoá lạ ⇒ ĐỎ. **K5b**: hai nhãn đã ký *(A·23 + C·14)*, đổi chỗ một dòng mỗi bên *(tổng y nguyên)* ⇒ ĐỎ hai dòng `chữ ký cũ, ký lại` *(vân tay dòng lệch)* — ⛔ còn vô hình. | **ĐÃ SỬA** |
| `H2-R1-03` | GHI NHẬN | M15 chết | Đột biến **M15** *(`--ghi` ghi thẳng)* trên bản sao ⇒ **BỊ GIẾT** `1 failed` *(`test_H2_ghi_XANH_dut_giua_chung_KHONG_lam_cut_hien_vat`)*. `--ghi` dùng `.tam`+`os.replace`+dọn khi đứt. | **ĐÃ SỬA** |
| `H2-R1-04` | GHI NHẬN | M17·M18·M19 chết | **M17** *(bỏ in `②`)* · **M18** *(bỏ in `④`)* ⇒ BỊ GIẾT *(bài CLI)*; **M19** *(bỏ regex ngày)* ⇒ BỊ GIẾT `test_H2_kiem_dau_vao_moi_luat_CAN[so_ngay_khuon_tuan]`. `CA_PHA` có `20261116` + `2026-W47-1`. | **ĐÃ SỬA** |
| `H2-R1-05` | GHI NHẬN | chỉ khai | `_luat` + CLI `①` khai `⛔ xét 147 dòng FLS ⛔ có dòng sổ (chiều ngược)`; `dat_hd1.ngoai_phan.dong_fls_khong_co_dong_so = 147`. | **ĐÃ KHAI** |
| `H2-R1-06` | GHI NHẬN | ⛔ `KHAC` + ngày tương lai ⇒ ĐỎ | **K4c**: `ngay 2099-12-31` ⇒ ĐỎ `sau hôm nay 2026-11-17 — ⛔ ký trước`. Ký `KHAC`·`Khác`·` khac ` ⇒ ĐỎ *(so sau `_goc_nhan`)*; ký đúng HÔM NAY vẫn hợp lệ *(đối chứng ĐẠT)*. | **ĐÃ SỬA** *(ⓐⓑ)* · ⓒ + nhãn đóng còn mở *(xem GHI NHẬN R2)* |
| `H2-R1-07` | GHI NHẬN | chỉ khai | `_luat` + `_vi_sao` khai *"dòng VẮNG trong tệp nhãn = chưa có nhãn"*; bài `test_H2_B1_tep_nhan_THIEU_dong_la_HOP_LE…` ghim. | **ĐÃ KHAI** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 4 · AP §5.3.1 HD1 · `CLAUDE.md` Đ1–Đ5)* | **ĐẠT.** Phán `(dòng 1-1 100 % ∨ mọi dòng thiếu ĐÃ KÝ) ∧ [ô] (ô MỌI dòng khớp ∨ (mọi dòng tự-soi loại ĐÃ KÝ ∧ ô dòng còn lại khớp hết))` cài đúng quyết định ⓐ; chữ ký buộc `so_dong` **và** `van_tay_dong` *(ⓑ)*; `KHAC`/ngày tương lai ĐỎ *(-06)*. **Đ3**: `o_100 = om > 0 and (…)` — `0/0` ⛔ 100 %, mẫu số `om` in ở `①`/`④`. **Đ5**: `MONG["dat_hd1_theo_ky"]` + `MONG["o_moi_dong"]` khai trước, NO cả hai chiều *(B4)*; R2 **chứng minh ĐỎ** 5 đột biến *(M15·M17·M18·M19·R1-M3)* trên bản sao, trả nguyên. **Đ4**: `①…⑤` mỗi số có nhãn; `o_parity`/`o_moi_dong`/`parity_o` tách nhãn. | §Cổng · §AC · đột biến `/tmp/r2_h2/mut` |
| **Dữ liệu** *(ảnh đóng băng; kho thật `fls_itl = 0 dòng` trên cụm 5447)* | **ĐẠT.** R2 dựng lại tập dòng ĐỘC LẬP *(⛔ import `do()`; chỉ `_nap`/`_van_tay_dong`/`soi_mot_dong`)*: thiếu **122** · loại **37** · ngược **147** · van_tay `{thieu 18047e0e…, nguoc 6ac2463a…}` **= tool công bố** *(Đ2 — hai nguồn)*. 2026-07: thiếu 23 ∩ loại 37 = 1. Khối mới của `voi_so_luong.json` thêm `dong_tu_soi_loai` *(chỉ số THỨ TỰ dòng sổ, ⛔ tiền/tên/ngày)* + vân tay *(sha256)* — ⛔ PII. | kịch bản `/tmp/r2_h2/drv.py` |
| **Màn hình** | **N/A** — ISP §4 *"Frontend: N/A — lát cắt là lệnh/cổng"*; diff ⛔ chạm `fls/web/**` *(0 tệp)*. | `git diff --name-only 5e63a90 isp/H2` |

**Riêng tư:** grep dòng THÊM của diff *(4 tệp mã+json)* với `email·dien_giai·Diễn giải·số CT·so_ct·secret·client_secret·password·@…·ThuongCT` = chỉ gặp **`ThuongCT`** *(vai O8, khai ISP `:51` — ⛔ PII mới, R1 đã thông)* trong **chú thích/`_vi_sao`** *(⛔ dữ liệu)*, và `@functools.lru_cache` *(decorator, dương tính giả của regex `@`)*. Khối JSON mới chỉ có **số đếm + chỉ số dòng + vân tay**, ⛔ `Email`/`Diễn giải`/tiền. ⛔ `Client secret`.

**Làn:** 5/5 tệp thuộc làn BE-HC *(ISP Step 4 §4+§7)*: `tools/do_voi_so_luong.py` · `tests/oracle/test_do_voi_hd1.py` · `docs/ITL/_tools/voi_so_luong.json` · `docs/ITL/_tools/so_ly_do_hd1.json` + phiếu BG. **0** tệp ngoài làn; ⛔ chạm `fls/**` *(0)*; ⛔ tệp mới/xoá *(5× `M`)*; ⛔ tuyến/màn/config ngoài mục 7 *(chỉ cờ `--ghi`)*; ⛔ refactor ngoài test đòi.

## Hợp đồng CG1 — hình dạng `voi_so_luong.json` *(so dict `5e63a90` ↔ `isp/H2`)*
- Khoá **top-level y nguyên** *(10 khoá)*; khoá MẤT **0**; khoá THÊM **126**, **tất cả** dưới `dat_hd1/*` *(`dong_tu_soi_loai` · `ngoai_phan` · `theo_nhan` · `theo_ky[k]` thêm 5 trường · `mau_so` thêm 2)*.
- Khoá CHUNG ngoài `dat_hd1` đổi giá trị: **KHÔNG**. Trong `dat_hd1` khoá cũ đổi giá trị: **2** — `_luat` *(chuỗi luật, cố ý)* + `theo_ky["2026-07"].o_100` *(`true → false`, nghĩa mới H2-R1-01)*.
- 5 khoá CG1 đọc *(`so_ky_dat` · `mau_so.so_ky` · `ky_dat` · `theo_ky[k].dat` · `theo_ky[k].thieu`)*: giữ TÊN, **5/23** y nguyên *(`o_100` ⛔ thuộc 5 khoá ấy — đổi an toàn cho CG1)*.

## Phát hiện R2
| Mã | Mức | Lớp | Tệp:dòng | Tái hiện | Khuyến nghị | Gửi |
|---|---|---|---|---|---|---|
| `H2-R2-01` | **GHI NHẬN** | B1 | `tools/do_voi_so_luong.py:119` *(`NHAN_CAM_KY = ("KHAC",)`)* · `:285` | Danh sách cấm ký chỉ **một** phần tử *(`KHAC`, so sau bỏ dấu/cách/hoa)*. R2 đo: ký nhãn `OTHER` *(hoặc `LY_DO_KHAC`…)* vẫn XANH — "lệch CÓ TÊN lý do" của AP §5.3.1 chưa buộc nhãn thuộc **danh mục đóng** của DT1b. **⛔ hồi quy**: bản v1 *(`9cf9999`)* nhận MỌI nhãn *(gồm `KHAC`)* ⇒ v2 nghiêm hơn hẳn; đây là **đóng chưa trọn**, Dev tự khai *(BG "Dev tự thấy còn yếu" #5)* và trùng `Q1` của BG-091. | BA/orchestrator: chốt danh mục nhãn DT1b đóng *(Step 5)* rồi `NHAN_CAM_KY`/kiểm nhãn canh theo danh mục ấy — **trước chữ ký thật đầu tiên của O8**. ⛔ chặn gộp H2 *(sổ rỗng)*. | `BA` · `DEV` |
| `H2-R2-02` | **GHI NHẬN** | B1 | `tools/do_voi_so_luong.py:317` · `:339` *(`hom_nay or date.today()`)* | `hom_nay` của CLI = đồng hồ MÁY *(container UTC)*. Owner ký sáng sớm giờ VN *(UTC+7)* với `ngay` = ngày VN ⇒ trong ~7 giờ đầu ngày, máy UTC thấy *"sau hôm nay"* ⇒ ĐỎ giả *(chiều an toàn, tự hết sau 07:00 VN)*. Dev tự khai *(BG #4)*. | Dev *(trước O8 ký)*: `hom_nay` theo múi giờ VN *(Asia/Ho_Chi_Minh)* thay vì `date.today()` của máy; hoặc owner ký với `ngay` = ngày UTC. | `DEV` |

> ⚠ Cả hai **GHI NHẬN** là carry-over Dev đã khai và orchestrator đã HOÃN *(`-06` ⓒ + nhãn đóng = `Q1`; múi giờ = chiều an toàn)* — **⛔ chặn** vòng này. R2 ⛔ nâng mức: quyết định orchestrator chỉ đòi `KHAC` + ngày tương lai, cả hai đã ĐỎ.

## Đối chiếu từng dòng mục 8 *(Exit criteria — ISP `:744`–`:748`)*
| Dòng | Bằng chứng R2 | Phán |
|---|---|---|
| `H2-B1…B4 đúng` | AC-1…AC-4 ĐẠT; `pytest tests/oracle/test_do_voi_hd1.py` = `65 passed`; đỏ-trước BG tái hiện *(Dev: `58 failed,7 passed` trên mã cũ)* — R2 ⛔ chạy lại bản cũ nhưng đã GIẾT 5 đột biến then chốt trên bản mới | **ĐẠT** |
| `3 vòng review xong` | R1 `KQ-092` ✅ · R2 `KQ-093` *(phiếu này)* ✅ · R3 `KQ-094` **chưa chạy** | **⛔ chưa tới** *(đúng — gate vòng sau, ⛔ phải TRƯỢT ở R2)* |
| `điều kiện PUSH: đủ R1·R2·R3, phát hiện chặn = 0` | R2 góp **0 CHẶN**; 2 GHI NHẬN carry-over hoãn | **R2: đạt phần mình** |

## Môi trường R2 để lại
- Cụm **5447** để CHẠY *(R2 ⛔ dừng)*; `fls` `fls_itl = 0 dòng`; `fls_test` do `--duong-nen` dựng lại.
- Worktree `isp-h2`: R2 chỉ THÊM hai tệp *(phiếu này + sổ phát hiện cập nhật)*; sha ba tệp mã/json **= trước khi kiểm**. Đột biến chỉ trên bản sao `/tmp/r2_h2/mut`, đã trả nguyên *(sha bản sao = worktree)*.
- Bài học giữ *(⛔ lỗi H2)*: ⛔ chạy phiên pytest khác trên **cùng** cụm khi `--duong-nen` đang chạy *(conftest `DROP DATABASE fls_test`)* — R2 chạy mọi lệnh **tuần tự** nên ⛔ vướng.
