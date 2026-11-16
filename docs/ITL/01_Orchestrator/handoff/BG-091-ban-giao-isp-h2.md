# BG-091 — bàn giao `WO-090` *(ISP 3.1.2 · Step 4 · H2)* — HD1 · cổng nhận *"lệch có tên lý do và owner ký"*, sổ lý do RỖNG, có cổng

| | |
|---|---|
| **Thuộc** | `WO-090` *(dải phiếu orchestrator cấp: WO-090 · BG-091 · R1/R2/R3 = KQ-092/093/094; WO do orchestrator ghi sau — spec là ISP)* |
| **Phát bởi** | `fls-dev` *(làn **BE-HC**)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-092` · R2 `KQ-093` · R3 `KQ-094` |
| **Commit** | nhánh **cục bộ** `isp/H2` @ `9cf9999` *(mã + bài thử + hai JSON)* — tách từ nền `2664e25` *(nhánh làm việc + S0 + DT1a)*; ⛔ đẩy theo O2 = A *(orchestrator gộp sau R3 rồi mới đẩy)*. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-h2` · cụm PG riêng cổng **5435** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 4 · H2** *(dòng `691`–`770`; sha256 `c2c231d7d9898fdc`)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §5.3.1 HD1 ★ · §5.3.2 AC10 · §5.3.3 Figure 5.3.3 *(sha256 đo lại `5cf6e576ff46f088` — khớp `5cf6e576…` của WO-080)* · ISP §1.2 `O8` · Step 5 DT1b · Step 7 CG1 · Step 43 H15 · `SO_PHAT_HIEN_ISP-3.1.md` *(bản mới nhất ở worktree `agent-a73f7b4b46d6c57c4`, 15 hàng S0)* + `SO_PHAT_HIEN_ISP-3.1_DT1a.md` *(9 hàng)* — cột luật phòng tái phạm · `TIEN_DO.md` dòng 91 + 93 *(quyết định `R1-06` · `R1-08`)* · `CLAUDE.md` Đ1–Đ5 · `BG-081` · `KQ-082` |

## Cổng vào *(`05` §5)*
- git thật: `git log -1` ở worktree trước khi làm = `2664e25 KQ-082: R1 kiểm BG-081 …` — đúng nền orchestrator giao; nhánh `isp/H2`; `git status` sạch.
- version hợp đồng: ISP 3.1.2 · AP v3.1.2 sha256 khớp. Run id: ⛔ cần *(⛔ phiếu nào nói "đã chạy")*.
- `WO-090` **chưa tồn tại** ở thời điểm làm *(orchestrator ghi sau — lời giao nói rõ "ISP là spec")* ⇒ tôi đối chiếu 8 trường của ISP Step 4 thay cho §3.1. Ba chỗ spec **thiếu / lệch** — ⛔ chế spec, tôi chọn đúng lời giao của orchestrator rồi hỏi ở **§Câu hỏi** *(cả ba `KHONG_CHAN`)*: Q1 khuôn tệp nhãn DT1b · Q2 "5/23" ↔ Figure 5.3.3 "0/23" · Q3 chữ ký mù trước đổi chỗ.
- `WO-090` · `handoff/README.md` · `08_CHANGELOG_RELEASE.md` · Dashboard · `TIEN_DO.md`: **⛔ chạm** — ngoài danh sách tệp của lời giao *(`S0-R1-08`)*; orchestrator ghi lúc gộp.
- Môi trường: `bash tools/dung_moi_truong_isp.sh --cong 5435 --duong-nen` ⇒ xem §Cổng.

## Substep 1 — test cases · kế hoạch tối thiểu · lệnh · giới hạn
1. **Test cases** *(mục 6 của Step 4, phủ mọi dòng mục 8)*: `H2-B1` *(cổng · sổ rỗng ⇒ 5)* · `H2-B2` *(đơn vị · ký giả mọi dòng 2026-07 ⇒ 6)* · `H2-B3` *(đơn vị · nhãn có mà chưa ký ⇒ vẫn đỏ)* · `H2-B4` *(chứng minh đỏ · phá MONG)*. Thêm: mỗi phép kiểm đầu vào mới một ca phá *(`DT1a-R1-03`)*. FE: **N/A** — lát cắt là lệnh/cổng, đầu ra JSON + exit code *(ISP mục 4)*.
2. **Kế hoạch thay đổi tối thiểu** *(⛔ đụng mã nghiệp vụ, ⛔ đụng kho, ⛔ đụng `tools/phan_loai_dong_thieu.py`)*: `tools/do_voi_so_luong.py` *(thêm `phan_hd1` + 8 hàm nhỏ *(`_van_tay_dong` · `_duong` · `_doc_json` · `_co_chu` · `_so_nguyen` · `_ngay_that` · `_doc_nhan` · `_doc_so`)*, `do(nhan=…, so_ly_do=…)`, `MONG["dat_hd1_theo_ky"]`, 4 dòng in `HD1 · ①…④`, `--ghi` qua tệp tạm)* · `docs/ITL/_tools/so_ly_do_hd1.json` *(mới, RỖNG)* · `docs/ITL/_tools/voi_so_luong.json` *(sinh máy, chỉ THÊM khối `dat_hd1`)* · `tests/oracle/test_do_voi_hd1.py` *(mới)* · phiếu này.
3. **Lệnh** *(từ gốc worktree; `export PG_DSN='postgresql://fls:fls@localhost:5435/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5435/fls_test' PYTHONUTF8=1`)*: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/oracle/test_do_voi_hd1.py` · `…/python tools/do_voi_so_luong.py [--ghi]` · `…/python -m pytest tests/du_lieu tests/oracle` *(hồi quy gồm DT1a)* · `bash tools/dung_moi_truong_isp.sh --cong 5435 --duong-nen`.
4. **Giới hạn** *(ISP mục 3)*: khi chưa có chữ ký thật, số kỳ đạt giữ **5/23**; tệp nhãn DT1b **chưa có** *(⛔ ở worktree này, ⛔ ở `isp-dt1b` lúc làm — `ls` cả hai: "No such file")* ⇒ mọi 122 dòng thiếu là "chưa có nhãn"; ký thật là việc owner *(O8)*; sửa mã ghép là `H3`; tự sinh theo kỳ là `H15`.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/do_voi_so_luong.py` *(+236 −3)* | khối `dat_hd1`: kỳ **ĐẠT** ⇔ *(dòng 1-1 100 % **hoặc** mọi dòng thiếu của kỳ có nhãn **ĐÃ KÝ**)* **∧** *(ô Final 7 khối 100 %, mẫu số > 0)*. `phan_hd1(theo_ky, thieu, van_tay, tep_nhan, tep_so)` trả *(khối, lỗi)*; đầu vào hỏng ⇒ *(None, lỗi)* — ⛔ phán kỳ nào. Đọc nhãn từ `docs/ITL/_tools/phan_loai_ly_do.json` *(DT1b; **vắng** ⇒ mọi dòng "chưa có nhãn", ⛔ lỗi)* theo khuôn của chính `phan_loai_dong_thieu.json` + hai vân tay **tính lại từ ảnh** *(cùng công thức `_van_tay` của DT1a)*; đọc chữ ký từ `so_ly_do_hd1.json` *(**vắng** ⇒ ĐỎ)*; `so_dong` của chữ ký phải **bằng** số dòng thiếu mang nhãn ấy. `MONG["dat_hd1_theo_ky"]` = 5 kỳ khai trước *(nguồn: AP §5.3.1 "5/23 tháng đủ" + BG-081 — ⛔ lần chạy đầu)*; `MONG.get` ⇒ mất khoá là ĐỎ một dòng. **`_sha`, `MONG` và mọi khoá cũ giữ nguyên tên + nghĩa** *(`DT1a-R1-06`)*. In mẫu số trước tỷ lệ (Đ3); `--ghi` qua tệp tạm + `os.replace` *(`DT1a-R1-07`)*; câu đầu của thông điệp ĐỎ thêm "hoặc ⛔ đo được" *(giữ tiền tố `⛔ VOI SỐ LƯỢNG ĐỎ` mà `DUONG_NEN.md:88` trích)*. Hàng `Σ` y nguyên |
| `docs/ITL/_tools/so_ly_do_hd1.json` *(mới, 4 dòng)* | sổ lý do **RỖNG** — `{"_vi_sao": …, "chu_ky": []}`; `_vi_sao` khai bốn khoá *(nhãn · số dòng · người ký · ngày)*, luật số dòng, O8 = ThuongCT, ⛔ agent ký |
| `docs/ITL/_tools/voi_so_luong.json` *(sinh máy, +217 −0)* | chỉ THÊM khối `dat_hd1` ở cuối; phần cũ **y nguyên byte** *(`git diff --numstat`: `217 0`)* — trước khi sửa, tôi đã đo `do()` cũ = tệp đã commit *(so dict: `True`)* |
| `tests/oracle/test_do_voi_hd1.py` *(mới, 500 dòng)* | **46** bài *(node pytest)* = `H2-B1` 8 + `H2-B2` 2 + `H2-B3` 5 + `H2-B4` 1 + kiểm đầu vào 30 *(1 đối chứng + **26** ca phá tham số hoá + 2 qua đường thật + 1 phòng thủ hai ca)*. MONG của bài **độc lập** với tool; bài đọc 122 dòng thiếu từ **hiện vật DT1a**, ⛔ từ tool đang kiểm |
| `docs/ITL/01_Orchestrator/handoff/BG-091-ban-giao-isp-h2.md` *(mới)* | phiếu này |

## Cổng *(kết quả nguyên văn — `PG_DSN=…:5435/fls` · `PG_DSN_TEST=…:5435/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/oracle/test_do_voi_hd1.py` | exit 0 · `46 passed in 15.68s` *(chạy lại trên đúng `9cf9999` sau khi container khởi động lại; `git diff HEAD -- tools tests docs/ITL/_tools` rỗng)* |
| `python -m pytest tests/du_lieu tests/oracle` *(hồi quy, gồm 16 bài DT1a)* | exit 0 · `155 passed in 19.12s` *(sau khởi động lại; lượt trước commit `155 passed in 15.59s`; nền `2664e25`: `109 passed in 2.84s` ⇒ +46 = đúng số bài mới; DT1a ⛔ vỡ)* |
| `python tools/phan_loai_dong_thieu.py` *(DT1a import `_sha` + `MONG` của tệp này — `DT1a-R1-06`)* | exit 0 · `KẾT: ĐẠT — mọi phép so khớp MONG · 122 dòng thiếu + 147 dòng ngược · nhan = null (DT1b điền)` |
| `python tools/do_voi_so_luong.py` | exit 0 · `Σ          9967   9845    3341    2700  30756  22290    112   13  69510/69510` *(y nguyên nền)* · `HD1 · ① MẪU SỐ: 23 kỳ · 9967 dòng sổ · 122 dòng thiếu (sổ ⛔ ghép 1-1) · tệp nhãn DT1b docs/ITL/_tools/phan_loai_ly_do.json: VẮNG · sổ lý do docs/ITL/_tools/so_ly_do_hd1.json: 0 chữ ký` · `HD1 · ② dòng thiếu có nhãn 0/122 · có nhãn ĐÃ KÝ 0/122` · `HD1 · ③ kỳ đạt (…): 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04` · `HD1 · ④ kỳ đỏ 18/23 (dòng thiếu · có nhãn · đã ký): 2025-01 1·0·0 · … · 2026-07 23·0·0 · 2026-08 13·0·0` |
| `bash tools/dung_moi_truong_isp.sh --cong 5435 --duong-nen` — **lượt 1** *(trên `9cf9999`, chạy xong TRƯỚC khi container khởi động lại)* | exit 0 · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` — 7/7 `[ĐẠT]` môi trường *(gồm `[ĐẠT] HD1 do_voi_so_luong chay 9845 / co 9967 (exit 0)` · `[ĐẠT] lint-imports Contracts: 11 kept, 0 broken.` · `[ĐẠT] di trú + pg_verify 26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `[ĐẠT] kho fls RỖNG fls_itl = 0 dòng`)*; pytest toàn bộ `exit 1` · `12 failed, 2494 passed, 2 xfailed, 1 warning, 14 errors in 334.10s (0:05:34)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` *(mẫu số **2.522** node = 12 + 2.494 + 2 + 14; so BG-081 `2.476` ⇒ +46 = đúng số bài mới, 0 trong tập đỏ)*; `tests/web` `3 failed, 661 passed in 176.43s` · `[ĐẠT] … 3 = 3 node id (thêm 0 · bớt 0)` |
| cùng lệnh — **lượt 2** *(sau khi container khởi động lại; orchestrator báo cụm 5435 đã bật lại)* | exit 0 · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` — 7/7 `[ĐẠT]`; toàn bộ `12 failed, 2494 passed, 2 xfailed, 14 errors in 346.75s (0:05:46)` · `26 = 26 node id (thêm 0 · bớt 0)`; web `3 failed, 661 passed in 180.88s (0:03:00)` · `3 = 3 node id (thêm 0 · bớt 0)`. Ở **cả hai lượt**: grep `test_do_voi_hd1` / `tests/du_lieu` / `tests/oracle` trong dòng `FAILED`/`ERROR` = **0**; 3 đỏ web = 3 bài SỔ THẬT `wo022`/`wo022_v2`/`wo042` *(đúng BG-081)* |
| hai bài chập chờn `tests/web/test_wo032_man_cua_that.py::test_AC3_…` / `::test_AC7_…` | **⛔ đỏ ở lượt nào**: grep `wo032_man_cua_that` trong dòng `FAILED`/`ERROR` của 4 log *(toàn bộ + web × 2 lượt)* = **0 · 0 · 0 · 0** *(hàng `wo032` duy nhất trong tập đỏ là `tests/api/test_wo032_v2_bac_da_gan_pg.py::test_AC12_SO_THAT…` — bài SỔ THẬT của đường nền 26)*. Chạy riêng thêm một lượt: `pytest tests/web/test_wo032_man_cua_that.py -k "AC3 or AC7"` ⇒ `5 passed, 7 deselected in 1.43s` |
| `.venv/bin/lint-imports` *(container: `bin/`, ⛔ `Scripts/*.exe`)* | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ chạm schema ⇒ ⛔ bắt buộc; vẫn chạy: exit 0 · `khong co gi de ap` · `pg_verify: khop` |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-h2/.venv/Scripts/lint-imports.exe'` — đỏ của đường nền *(`DUONG_NEN.md:432`: gọi cứng đường Windows)*; ⛔ do bước này |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (177 file, 1871 bang, 725 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(chạy SAU khi có phiếu này; tạm rút phiếu ra: `176 file, 1865 bang` — +1 tệp · +6 bảng = đúng 6 bảng của phiếu; `OK K3 bang markdown khong lech`)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` · `B3` `B4` `C5` `C5b` *KHONG DO DUOC* · `A1` `B1` `C6` *DOI TRANG THAI* — **trùng khít** đường nền `DUONG_NEN.md:434` *(đỏ do kho rỗng)*; ⛔ phép nào đọc tệp của bước này |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |

## Bằng chứng từng test ID
| ID *(ISP mục 6)* | Mong | Bài *(PASSED trên `9cf9999`)* · số đo | Kết |
|---|---|---|---|
| **H2-B1** · cổng · sổ rỗng | kỳ đạt = 5 (= AP v3.1.2) | `test_H2_B1_so_rong_ky_dat_DUNG_5_tren_23` — `mau_so = {so_ky: 23, dong_so: 9967, dong_thieu: 122}` *(mẫu số ⛔ rỗng, Đ3)* · `ky_dat = (2024-10, 2024-11, 2024-12, 2025-03, 2025-04)` · `so_chu_ky = 0` · `da_ky = 0` · mỗi kỳ đỏ mang `thieu` = `phan_bo_ky_thieu` của MONG DT1a *(18 kỳ, Σ 122)* · `o_100` đúng ở 23/23 kỳ. `…hai_nguon_cho_5_ky_dat_khop_nhau` — MONG độc lập *(AP + BG-081)* = phần bù 23 − 18 kỳ có thiếu trong MONG DT1a (Đ2). `…so_ly_do_khoi_tao_RONG_0_chu_ky` — `chu_ky == []`. `…MONG_dat_hd1_theo_ky_khai_TRUOC_va_giu_khoa_DT1a_dung` — khoá mới = 5 kỳ; `checksum` = `nguon.checksum` của hiện vật DT1a; `so_dong_so` 9967 · `so_ky` 23 · `so_dong_ghep_canon` 9845 · `so_dong_bank` 9992; `_sha([1],[2])` = sha256 `[[1],[2]]`. `…van_tay_tap_dong_TRUNG_DT1a` — `{thieu: 18047e0eb0319ea1, nguoc: 6ac2463a190ff631}` = hiện vật DT1a = BG-081. `…json_DA_GHI_khop_lan_do_hien_tai`. `…CLI_in_MAU_SO_truoc_ty_le_va_hang_Sigma_y_nguyen` — dòng `HD1 · ① MẪU SỐ: 23 kỳ · 9967 dòng sổ · 122 dòng thiếu …` đứng TRƯỚC dòng `HD1 · ③ kỳ đạt … 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04`; `Σ 9967 9845`. `…tep_DT1a_dung_lam_tep_nhan_hop_le_0_nhan` — hiện vật DT1a *(mọi `nhan = null`)* là một tệp nhãn HỢP LỆ ⇒ 0 nhãn ⇒ 5 kỳ | đạt |
| **H2-B2** · đơn vị · ký giả 2026-07 | 2026-07 thành đạt; tổng 6 | `test_H2_B2_ky_gia_moi_dong_2026_07_thi_2026_07_DAT_tong_6` — nhãn tổng hợp *(23 dòng 2026-07 = `TONG_HOP_A`, 99 dòng khác = `TONG_HOP_B`)*, sổ tạm ký `TONG_HOP_A · 23 dòng` ⇒ `ky_dat` 6 kỳ = 5 + `2026-07`; 2026-07 `{thieu 23 · co_nhan 23 · da_ky 23 · dong_100 False · o_100 True · dat True}`; `dem = {thieu 122 · co_nhan 122 · da_ky 23}`; 17 kỳ đỏ còn lại ⛔ đổi phán. `…qua_DUONG_THAT_do_6_ky_va_cong_DO_vi_khac_MONG_5` — cùng đầu vào qua `do()` thật ⇒ ĐỎ: `kỳ đạt HD1 (dat_hd1_theo_ky): đo ('2024-10', '2024-11', '2024-12', '2025-03', '2025-04', '2026-07') · mong ('2024-10', '2024-11', '2024-12', '2025-03', '2025-04')` — chứng minh `do()` ĐỌC cả hai tệp được truyền vào *(`DT1a-R1-01`)* và một chữ ký thật BUỘC khai lại MONG (Đ5) | đạt |
| **H2-B3** · đơn vị · nhãn chưa ký | vẫn đỏ | `test_H2_B3_co_nhan_ma_CHUA_KY_van_do_qua_duong_that` — 122/122 dòng có nhãn, sổ **thật** rỗng, qua `do()` ⇒ exit 0, `ky_dat` 5 *(⛔ thêm kỳ nào)*, `dem = {122 · 122 · 0}`, 2026-07 `co_nhan 23 · da_ky 0 · dat False`. `…ky_MOT_PHAN_nhan_cua_ky_thi_ky_VAN_do` — 2026-07 mang hai nhãn *(22 + 1)*, ký một ⇒ `da_ky 22/23` ⇒ `dat False`. `…chu_ky_LECH_so_dong_la_DO_qua_duong_that` — ký `TONG_HOP_A · 22` mà tệp có 23 ⇒ ĐỎ `… ghi số dòng 22 · tệp nhãn có 23 dòng thiếu mang nhãn ấy — chữ ký cũ, ký lại`. `…chu_ky_khi_tep_nhan_VANG_la_DO_qua_duong_that` — `… ghi số dòng 1 · tệp nhãn có 0 dòng …`. `…o_chua_100_thi_chu_ky_KHONG_cuu_duoc_ky` — 2026-07 đã ký đủ mà 1 ô lệch ⇒ đỏ; 2024-10 đủ dòng mà 1 ô lệch ⇒ đỏ; 2024-11 ô `0/0` ⇒ đỏ (Đ3) ⇒ `ky_dat = (2024-12, 2025-03, 2025-04)` | đạt |
| **H2-B4** · chứng minh đỏ | phá MONG ⇒ ĐỎ rồi trả nguyên | `test_H2_B4_pha_MONG_ca_hai_chieu_cong_DO_roi_tra_nguyen` — phá **trong bộ nhớ** *(⛔ chạm tệp)*: MONG thiếu một kỳ ⇒ `exit 1`; thừa một kỳ ⇒ `exit 1`; mất khoá ⇒ `exit 1`, mỗi lần stderr có `dat_hd1_theo_ky`, ⛔ `Traceback`; phá + `--ghi` ⇒ `exit 1` và sha256 `voi_so_luong.json` ⛔ đổi; trả nguyên ⇒ CLI `exit 0`, sha256 tool ⛔ đổi. Phá **trên tệp thật** bằng tay: xem §Chứng minh ĐỎ | đạt |

## Log ĐỎ → XANH
**① Đỏ thật trước khi có mã** *(`…/python -m pytest tests/oracle/test_do_voi_hd1.py -rA`, mã tool còn ở `2664e25`)*: exit 1 · `45 failed, 1 passed in 2.85s`. Lý do đếm theo dòng `E` — **mọi đỏ vì THIẾU hành vi**, ⛔ lỗi cú pháp/dựng:
- 39 × ``Failed: ⛔ tools/do_voi_so_luong.py chưa có `phan_hd1` — hành vi H2 chưa có``
- 1 × ``AssertionError: ⛔ chưa có docs/ITL/_tools/so_ly_do_hd1.json — hiện vật H2 chưa có``
- 1 × ``AssertionError: ⛔ voi_so_luong chưa có khối `dat_hd1` — trường mới chưa có``
- 1 × ``AssertionError: ⛔ MONG chưa khai `dat_hd1_theo_ky` ``
- 1 × ``KeyError: 'dat_hd1'`` *(bài vân tay)* · 1 × ``AssertionError: ⛔ voi_so_luong.json chưa có `dat_hd1` — chưa `--ghi` ``
- 1 × ``AssertionError: ⛔ CLI chưa in đúng một dòng HD1 mẫu số + một dòng kỳ đạt: [...]``
- **Bài xanh sẵn duy nhất**: `test_H2_B1_hai_nguon_cho_5_ky_dat_khop_nhau` — nó so **hai nguồn của MONG độc lập của bài** *(AP + BG-081 ↔ MONG DT1a)*, ⛔ gọi tool H2 ⇒ xanh sẵn là **đúng** *(Substep 2 ③: ghi bằng chứng, ⛔ phá mã)*.

**② Xanh**: sau mã + `--ghi` ⇒ `46 passed in 14.99s`. Sau đó tôi **siết** bài ca phá *(bản đầu chỉ đòi "có một lỗi chứa mẫu" — mẫu `nhãn` khớp được cả câu `tệp nhãn …` của một luật KHÁC)*: nay đòi **đúng 1 lỗi**, **đúng nguồn** *(`tệp nhãn` / `sổ lý do`)*, **đúng luật**; và thêm ca phá thứ hai cho phép phòng thủ "kỳ ngoài bảng" *(trước đó ⛔ có ca riêng — `DT1a-R1-03`)* ⇒ `46 passed in 16.16s`.

## Chứng minh ĐỎ
**A · Đột biến MÃ** *(script ở scratchpad `hc_h2/dot_bien.py`: sửa `tools/do_voi_so_luong.py` một chỗ, chạy `tests/oracle/test_do_voi_hd1.py`, trả nguyên — sha256 tool + `voi_so_luong.json` so lại `True`)*: **15/16 đột biến bị giết**.

| Đột biến | Kết *(bài đỏ)* |
|---|---|
| M1 bỏ phép chữ ký ↔ số dòng | `4 failed` — B3 lệch số dòng · B3 tệp nhãn vắng · ca `so_lech_so_dong` · `so_nhan_khong_ai_gan` |
| M2 ký MỘT PHẦN nhãn của kỳ cũng đạt *(`ky > 0`)* | `1 failed` — B3 một phần |
| M3 bỏ vế ô 100 % | `1 failed` — B3 ô chưa 100 % |
| M4 nhãn chưa ký tính như đã ký | `6 failed` — B2 ×2 · B3 chưa ký · B3 một phần · B3 ô · đối chứng |
| M5 bỏ vân tay tập ngược · M6 bỏ vân tay tập thiếu | `1 failed` mỗi cái — đúng ca `nhan_van_tay_NGUOC_sai` / `…THIEU_sai` *(`DT1a-R1-02`: mỗi tập một ca)* |
| M7 bỏ cổng `MONG dat_hd1_theo_ky` | `7 failed` — B1 ×4 · B2 đường thật · B3 chưa ký · B4 |
| M8 tệp nhãn hỏng rơi về "chưa có nhãn" | `2 failed` |
| M9 sổ lý do vắng coi như sổ rỗng | `2 failed` |
| M10 ô `0/0` coi là 100 % | `1 failed` |
| M11 bỏ phòng thủ `có − chạy` · M16 bỏ phòng thủ "kỳ ngoài bảng" | `1 failed` mỗi cái |
| M12 bỏ chặn dòng trùng · M13 bỏ chặn ngoài tập | `1 failed` mỗi cái |
| M14 vân tay khác công thức DT1a | `5 failed` |
| **M15 `--ghi` ghi thẳng** *(phá đường tệp tạm)* | **SỐNG** — `46 passed`: ⛔ bài nào chạy một `--ghi` XANH *(grep `"--ghi"` trong hai tệp bài chạm `do_voi_so_luong`: 2 chỗ — `test_phan_loai_dong_thieu.py:356` gọi tool DT1a, `test_do_voi_hd1.py:378` gọi khi MONG đã phá ⇒ dừng TRƯỚC khi ghi)*. Khai ở §Dev tự thấy còn yếu #1 |

**B · Phá MONG trên TỆP THẬT bằng tay** *(script `hc_h2/pha_mong_tay.py`: sửa dòng MONG, chạy `--ghi`, trả byte gốc)*:

| Kịch bản | Kết quả nguyên văn |
|---|---|
| bỏ `2025-04` khỏi MONG *(MONG thiếu một kỳ)* · `--ghi` | `exit=1` · `kỳ đạt HD1 (dat_hd1_theo_ky): đo ('2024-10', '2024-11', '2024-12', '2025-03', '2025-04') · mong ('2024-10', '2024-11', '2024-12', '2025-03')` · `voi_so_luong.json đổi byte? False` |
| thêm `2026-07` vào MONG *(thừa một kỳ)* · `--ghi` | `exit=1` · `… đo ('2024-10', …, '2025-04') · mong ('2024-10', …, '2025-04', '2026-07')` · `voi_so_luong.json đổi byte? False` |
| **trả nguyên** | `exit=0 · sha tool = gốc: True` · `Σ          9967   9845 …  69510/69510` · `HD1 · ③ … 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04` |

**C · Ba đầu vào tổng hợp qua `do()` thật** *(script `hc_h2/b2_b3_bang_chung.py`, tệp tạm ở scratchpad — ⛔ sổ thật)*:
- ký giả `TONG_HOP_A·23` ⇒ `ĐỎ · kỳ đạt HD1 (dat_hd1_theo_ky): đo (… '2025-04', '2026-07') · mong (… '2025-04')`
- 122 nhãn, sổ thật RỖNG ⇒ `exit 0 · kỳ đạt 5/23 · dem {'thieu': 122, 'co_nhan': 122, 'da_ky': 0} · 2026-07 {'dat': False, 'thieu': 23, 'co_nhan': 23, 'da_ky': 0, 'dong_100': False, 'o_100': True}`
- hiện vật DT1a làm tệp nhãn ⇒ `exit 0 · kỳ đạt 5/23 · dem {'thieu': 122, 'co_nhan': 0, 'da_ky': 0}`

## Hợp đồng tệp nhãn mà H2 ĐỌC *(cho DT1b — xem Q1)*
- Đường: `docs/ITL/_tools/phan_loai_ly_do.json`. **Vắng** ⇒ mọi dòng thiếu "chưa có nhãn" *(đỏ, ⛔ lỗi)*.
- Khuôn: `{"van_tay": {"thieu": "<16 hex>", "nguoc": "<16 hex>"}, "dong_thieu": [{"dong_sheet": <int>, "nhan": "<chuỗi>" hoặc null}, …]}` — **đúng khuôn của `phan_loai_dong_thieu.json`** *(DT1a)*; khoá thừa *(ở gốc lẫn ở từng dòng — `ky`, `dong_nguoc`, …)* bỏ qua.
- ĐỎ khi *(mỗi luật một ca phá)*: JSON hỏng · thiếu `van_tay`/`dong_thieu` · vân tay ≠ vân tay tính lại từ ảnh *(hiện `18047e0eb0319ea1` / `6ac2463a190ff631`)* · `dong_sheet` ⛔ phải số nguyên *(kể cả `True`)* · ngoài tập 122 dòng · trùng · `nhan` rỗng/khác kiểu.

## Kho thật
- `KHONG_CHAM`. Công cụ chỉ đọc ba ảnh `tests/fixture/*.json` + `phan_loai_ly_do.json` *(vắng)* + `so_ly_do_hd1.json`; ⛔ mở kết nối PG; `FLS_CHO_GHI_THAT` ⛔ đặt. Kho `fls` cụm 5435 vẫn `fls_itl = 0 dòng` *(K7 của script dựng)*.

## Cách chạy để xem
- N/A — ⛔ chạm UI. Xem bằng `…/python tools/do_voi_so_luong.py` *(bốn dòng `HD1 · ①…④` sau bảng)*.

## Dev tự thấy còn yếu
1. **Đột biến M15 sống** — đường `--ghi` qua tệp tạm + `os.replace` ⛔ có bài canh: mọi bài chạy `--ghi` đều chạy khi cổng ĐỎ *(dừng trước khi ghi)*. Bằng chứng tay: sau các lượt `--ghi` của tôi, `ls docs/ITL/_tools/ | grep -c tam` = `0`. Một bài chạy `--ghi` XANH sẽ ghi đè hiện vật đã commit — tôi ⛔ viết.
2. **Chữ ký chỉ buộc bằng SỐ DÒNG, ⛔ bằng TẬP dòng** — đúng bốn khoá ISP *(nhãn · số dòng · người ký · ngày)*, nhưng mù trước một phép **đổi chỗ**: DT1b chạy lại mà đổi nhãn của hai dòng ở hai kỳ khác nhau *(tổng mỗi nhãn y nguyên)* ⇒ chữ ký cũ vẫn "khớp", và kỳ đạt có thể đổi mà owner ⛔ thấy *(đúng bẫy Đ4 · DT1a-R1-02)*. Phần bù hiện có: tệp nhãn bị khoá vào TẬP 122 dòng bằng vân tay, và `MONG["dat_hd1_theo_ky"]` đỏ khi tập kỳ đạt đổi. Xem Q3.
3. **`nguoi_ky` là chữ tự do** — công cụ ⛔ kiểm người ký là ThuongCT *(O8)*; ai sửa được tệp thì "ký" được. Bằng chứng thật là **commit** của owner + review. ⛔ gõ tên người vào mã — nếu cần chặn thì là danh sách người ký trong config *(như O11 ⓑ)*.
4. **Khuôn tệp nhãn là tôi CHỌN** *(khuôn DT1a)* — DT1b làm song song; ghi khác khuôn ⇒ `do_voi_so_luong.py` ĐỎ ngay khi tệp về *(đúng Đ5, nhưng là đỏ lúc gộp)*. Và khi tệp về, `voi_so_luong.json` phải `--ghi` lại *(`tep_nhan.co` · `co_nhan` đổi)* ⇒ `test_H2_B1_json_DA_GHI…` đỏ tới lúc đó — cố ý. Xem Q1.
5. **"5/23" của khối này ≠ "tháng đạt HD1" của Figure 5.3.3** *(AP v3.1.2 ghi "Hôm nay: 0/23 tháng" — đòi CẢ tự sinh, chỉ đo được 2026-03)*. Tôi làm đúng lời giao + ISP B1 *(⛔ gồm tự sinh)*; khoá `_luat` của khối và docstring tool ghi rõ hai phép, hai nhãn (Đ4). Xem Q2.
6. **MONG "độc lập" chỉ độc lập một nửa**: 5 kỳ lấy từ AP §5.3.1 + BG-081 — nhưng con số AP do `sinh_ap_voi_v31.py` sinh từ **chính** `voi_so_luong.json` *(`DU_DONG = chay == co`)*, và BG-081 đo trên **cùng** ba ảnh. Nó chứng minh "tập ⛔ đổi", ⛔ chứng minh "định nghĩa dòng thiếu đúng".
7. `_van_tay_dong` là **bản thứ hai** của công thức `_van_tay` DT1a *(⛔ import được: DT1a đã import tệp này — vòng)*; canh bằng `test_H2_B1_van_tay_tap_dong_TRUNG_DT1a` + đột biến M14.
8. **Ô 100 % của 2026-07 tính trên ô của dòng ⛔ bị tự soi loại** *(`o_parity` bỏ **37** dòng `loai_tu_soi` của kỳ ấy — thừa kế từ `do()` cũ)*: nếu owner ký đủ 23 dòng thiếu, 2026-07 "đạt" mà 37 dòng loại ⛔ góp ô nào.
9. Bài thử đơn vị dùng `theo_ky` của `voi_so_luong.json` **đã commit** làm đầu vào *(⛔ gọi `do()` mỗi bài cho nhanh)* — buộc vào hiện vật mà `…json_DA_GHI…` ghim. Bộ 46 bài tốn **~15 s** *(6 lần `do()` thật + 5 tiến trình con)*.
10. Bài B2 đường thật **tách thông điệp ĐỎ bằng regex** — đổi khuôn câu `đo … · mong …` thì bài ĐỎ ồn ào *(mẫu phải khớp đúng 1 dòng)*, ⛔ xanh lặng.

## Câu hỏi *(`KHONG_CHAN` cả ba — orchestrator chốt; ⛔ hỏi người dùng)*
- **Q1 · Khuôn tệp nhãn DT1b.** ⓐ *(khuyến nghị)* orchestrator chuyển §"Hợp đồng tệp nhãn mà H2 ĐỌC" vào phiếu DT1b **ngay** — giá: DT1b bị buộc một khuôn, nhưng khuôn ấy là khuôn DT1a nó đã có *(bài `…tep_DT1a_dung_lam_tep_nhan_hop_le_0_nhan` chứng minh)*; được: gộp ⛔ đỏ. ⓑ để DT1b tự chọn, H2 sửa vòng 2 khi tệp về — giá: một vòng R1–R3 nữa + đỏ lúc gộp. Kèm: sau khi gộp DT1b phải chạy `python tools/do_voi_so_luong.py --ghi` *(hiện vật đổi `tep_nhan.co`)*.
- **Q2 · "5/23" ↔ Figure 5.3.3 "0/23".** ⓐ *(đã làm — khuyến nghị)* giữ phép của lời giao *(dòng ∨ ký) ∧ ô*, CG1 in nhãn đủ *("5/23 kỳ đạt — ⛔ gồm tự sinh")*, `H15` thêm vế tự sinh theo kỳ — giá: hai con số HD1 cùng sống tới H15, phải luôn kèm nhãn. ⓑ thêm vế tự sinh ngay ⇒ **0/23** *(chỉ 2026-03 đo được, mà 2026-03 thiếu 5 dòng)* — giá: H2-B1/B2 của ISP thành sai *(5 → 0, 6 → 0)*, cần ISP sửa.
- **Q3 · Chữ ký buộc vào TẬP dòng.** ⓐ giữ bốn khoá ISP *(đã làm)* — giá: mù trước đổi chỗ *(yếu #2)*. ⓑ *(khuyến nghị, TRƯỚC khi O8 ký thật)* thêm khoá `van_tay_dong` *(sha256 của các `dong_sheet` mang nhãn — công cụ in sẵn để owner chép)* — giá: một bước vá nhỏ + ISP thêm một trường; được: chữ ký chết khi tập dòng đổi. ⓒ thêm `ky` *(ký theo kỳ)* — giá: owner ký nhiều dòng hơn; được: miễn trừ hẹp hơn.
