# BG-102 — bàn giao `WO-101` *(ISP 3.1.2 · Step 7 · CG1)* — cổng HD1 vào `GET /gates`: ô chờ `FINAL` thành số đo + cổng `HD1_THANG`

| | |
|---|---|
| **Thuộc** | `WO-101` *(dải phiếu: WO-101 · BG-102 · R1/R2/R3 = KQ-103/104/105)* |
| **Phát bởi** | `fls-dev` *(làn **BE-CF**, tác giả)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-103` · R2 `KQ-104` · R3 `KQ-105` |
| **Commit** | nhánh **cục bộ** `isp/CG1` @ **`d6d50f4`** *(mã + bài thử + sàn Q8)* — tách từ nền `isp/base-w3` @ `575926e`; ⛔ đẩy *(lời giao: orchestrator gộp sau R3 rồi mới đẩy)*. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-cg1` · cụm PG riêng cổng **5434** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 7 · CG1** *(dòng `936`–`1014`; sha256 `c2c231d7d9898fdc` — khớp BG-091)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §5.3.1 HD1 · §5.3.2 AC10 · Figure 2.2 hàng ADJUST *(sha256 `5cf6e576ff46f088` — khớp WO)* · `WO-101` *(checkout chính, commit `ead0eef`)* · `KQ-092` `H2-R1-01/02` · `TIEN_DO.md` dòng 7 *(song song)* · 103 *(quyết định H2-R1-01 · hợp đồng H2 ↔ CG1)* · 98 *(Q8 = A)* · `CLAUDE.md` Đ1–Đ5 |

## Cổng vào *(`05` §5)*
- git thật: `git log -1` trước khi làm = `575926e Gộp isp/H2 vào isp/base-w3 (nền CG1)` — đúng nền WO; nhánh `isp/CG1`; `git status` sạch *(0 dòng)*.
- version hợp đồng: ISP 3.1.2 · AP v3.1.2 sha256 khớp. Run id: ⛔ cần *(WO ⛔ nói "đã chạy")*. Ghi kho thật: `KHONG` *(WO §Dữ liệu)*.
- WO đủ trường §3.1. `WO-101` · `handoff/README.md` · `08_CHANGELOG_RELEASE.md` · Dashboard · `TIEN_DO.md`: **⛔ chạm** — lời giao cấm *(việc của orchestrator)*.
- Hai tệp làn BE-HC đang vá song song — `tools/do_voi_so_luong.py` + `docs/ITL/_tools/voi_so_luong.json`: **⛔ chạm** *(`git diff 575926e..d6d50f4 --stat` trên hai tệp = rỗng; sha256 tệp đo `d58fe6a899d70d76` trước = sau)*.

## Substep 1 — test cases · kế hoạch · lệnh · giới hạn
1. **Test cases** *(mục 6, phủ mọi dòng mục 8)*: `CG1-B1` *(tệp đo thật qua tuyến thật)* · `CG1-B2` *(tệp vắng: không truyền / đường không có tệp)* · `CG1-B3` *(hồi quy `/gates` + `tests/api`)* · `CG1-B4` *(phá MONG ⇒ ĐỎ ⇒ trả nguyên ⇒ xanh)*. Thêm: mỗi phép kiểm đầu vào một ca phá *(tệp hỏng · tự mâu thuẫn · sai kiểu · `0/0`)*. FE: **N/A** — F03 hiện cổng ở FG *(ISP mục 4)*; F03 đã in `da_do` + `ly_do` của mọi cổng *(`fls/web/tep/man_f03.js:33-35`)*.
2. **Kế hoạch tối thiểu**: `doc_bao_cao.doc_cong(conn, pv, tep_do=None)` + hàm thuần `doc_cong_tep_do(tep_do)`; `FINAL` rời `_CHUA_DO_DUOC`; đường dẫn tệp đo đi **cùng đường với kết nối kho**: `tools/chay_cua.py` → `cua.dung_may(tep_do=…)` → `_May.tep_do` → `YeuCau.tep_do` → `xu_ly.cong` → `doc_cong`. Xem **Q1** về ba tệp ngoài bảng TRONG.
3. **Lệnh** *(từ gốc worktree; `export PG_DSN='postgresql://fls:fls@localhost:5434/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5434/fls_test' PYTHONUTF8=1`; venv `/home/user/FLS-tobe/.venv`)*: `python -m pytest tests/api/test_isp_gates_hd1.py tests/api` · `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` · `.venv/bin/lint-imports`.
4. **Giới hạn** *(ISP §3)*: số là của **ảnh 26/08** — `ly_do` của **cả hai** cổng ghi `số của ảnh sổ đóng băng ngày 2026-08-26 (⛔ kho sống)`.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/repo/doc_bao_cao.py` *(+205 −4)* | `doc_cong_tep_do(tep_do) → [FINAL, HD1_THANG]` *(hàm thuần, ⛔ chạm kho)*; `doc_cong(…, tep_do=None)` nối nó sau `RUN_DEM_KHOP`. `FINAL` rời `_CHUA_DO_DUOC` *(lý do cũ chép vào chú thích — Đ2, ⛔ xoá lịch sử)* ⇒ nhóm LUÔN `None` còn `DIF_BANK · VI · DONG_BO · BON_DUONG` — luật "⛔ bao giờ toàn xanh" giữ. `FINAL` đọc `tong.o_parity_khop / o_parity` *(+ `co`, `loai_tu_soi` để in nhãn Đ4)*; `HD1_THANG` đọc **đúng** năm khoá hợp đồng `dat_hd1.{so_ky_dat · mau_so.so_ky · theo_ky[k].dat · theo_ky[k].thieu · ky_dat}` + `nguon.so_dong_bang` — ⛔ tính lại luật kỳ. Tệp `None` / vắng / ⛔ JSON UTF-8 / ⛔ đối tượng ⇒ **cả hai** `dat=None`; khối hỏng / tự mâu thuẫn / sai kiểu *(`bool`, chuỗi, âm)* / mẫu số `0` ⇒ **cổng của khối ấy** `None` kèm lý do *(hai khối độc lập)*. Lý do chỉ in **TÊN** tệp, ⛔ đường dẫn |
| `fls/api/cua.py` *(+15 −4)* · `fls/api/xu_ly.py` *(+6 −1)* | `dung_may(…, tep_do=None)` → `_May.tep_do` → `YeuCau(tep_do=…)` *(trường mới, mặc định `None` — 5 chỗ dựng `YeuCau` khác ⛔ phải sửa)* → `bc.doc_cong(…, tep_do=yc.tep_do)`. ⛔ Mặc định nào ở tầng cửa *(hợp đồng tầng 7)* |
| `tools/chay_cua.py` *(+18 −1)* | `--tep-do DUONG` *(mặc định `docs/ITL/_tools/voi_so_luong.json` của repo — ở **rìa**, cùng chỗ chuỗi kết nối)*; `''` ⇒ ⛔ truyền; in ra tệp nào + `⛔ VẮNG` nếu tệp ⛔ có |
| `tests/api/test_isp_gates_hd1.py` *(mới, 356 dòng)* | **33** bài *(`--collect-only`)*: 7 bài qua **tuyến thật** *(B1 ×4 · B2 ×3 gồm 2 tham số · B4 ×1 — đếm 8 node)* + 23 node hàm thuần *(ca phá)* + 1 bài rìa `chay_cua` + 1 bài Đ2 *(MONG ↔ hiện vật DT1a)* |
| `tools/dung_moi_truong_isp.sh` *(+4 −1)* · `tests/test_dung_moi_truong_isp.py` *(+6 −2)* | **Q8 = A**: `MONG_PYTEST_TOAN_BO` **2460 → 2493** *(+33)* + bài ghim `test_S0_R2_03_hang_mau_so_khai_MOT_cho` `["2460"]` → `["2493"]`, cùng commit. Bài ghim **ĐỎ trước** khi sửa ghim: `AssertionError: assert ['2493'] == ['2460']` *(lo gốc giữ: một chỗ khai, ghim đúng số)* |

## Cổng *(kết quả nguyên văn — `PG_DSN=…:5434/fls` · `PG_DSN_TEST=…:5434/fls_test` · `PYTHONUTF8=1`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/api/test_isp_gates_hd1.py` | exit 0 · `33 passed in 2.98s` |
| `python -m pytest tests/api/test_isp_gates_hd1.py tests/api tests/repo/test_doc_bao_cao_pg.py tests/web/test_cua_phuc_vu_man_hinh_pg.py tests/web/test_cua_khong_doi_khi_tat_man_hinh.py` *(CG1-B3)* | exit 1 · `3 failed, 482 passed, 11 errors in 92.12s (0:01:32)` — 14 node đỏ = **đúng** 14 node của đường nền `duong_nen_bai_do.txt` thuộc tập này *(`diff` rỗng: 11 `test_mui_thu_luoi.py` + 3 bài SỔ THẬT `wo032_v2 AC12` · `wo037 AC2` · `wo037_v2 AC11`)*; ⛔ node nào của CG1 |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` | exit 0 · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` — 7/7 `[ĐẠT]` môi trường *(gồm `[ĐẠT] di trú + pg_verify 26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `[ĐẠT] lint-imports Contracts: 11 kept, 0 broken. (exit 0)` · `[ĐẠT] HD1 do_voi_so_luong chay 9845 / co 9967 (exit 0)` · `[ĐẠT] kho fls RỖNG fls_itl = 0 dòng (kết nối chỉ đọc)`)*; toàn bộ `12 failed, 2572 passed, 2 xfailed, 14 errors in 350.72s (0:05:50)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0) · chạy 2600 bài (mong ≥ 2493) · skipped 0 · deselected 0`; `tests/web` `3 failed, 661 passed in 186.54s (0:03:06)` · `[ĐẠT] … 3 = 3 node id (thêm 0 · bớt 0) · chạy 664 bài (mong ≥ 664)` |
| `python -m pytest --collect-only` *(Q8)* | nền `575926e`: `2567 tests collected` · `d6d50f4`: `2600 tests collected` ⇒ **+33** = `tests/api/test_isp_gates_hd1.py` `33 tests collected` |
| `.venv/bin/lint-imports` *(container: `bin/`)* | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ chạm schema ⇒ ⛔ bắt buộc; vẫn chạy: exit 0 · `khong co gi de ap` · `pg_verify: khop` |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-cg1/.venv/Scripts/lint-imports.exe'` — đỏ của đường nền *(`DUONG_NEN.md:456`: `tools/kiem_so_song.py:406` gọi cứng đường Windows)*; ⛔ do bước này |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (184 file, 1927 bang, 732 o ngay, 104 ma QD)` *(chạy SAU khi có phiếu này; tạm rút phiếu ra: `183 file, 1921 bang` — +1 tệp · +6 bảng = đúng 6 bảng của phiếu)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` · `B3` `B4` `C5` `C5b` *KHONG DO DUOC* · `A1` `B1` `C6` *DOI TRANG THAI* — **trùng khít** đường nền `DUONG_NEN.md:458` *(đỏ do kho rỗng)* |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |

## Bằng chứng từng AC
| AC | Mong | Bằng chứng *(PASSED trên `d6d50f4`)* | Kết |
|---|---|---|---|
| **AC-1** · `CG1-B1` | `FINAL` dat true · `da_do` số ô đo; `HD1_THANG` dat false · `'5/23 kỳ đạt'` · `ly_do` kỳ đỏ + số dòng thiếu + ngày ảnh | `test_CG1_B1_FINAL_DAT_69510_tren_69510_o_va_noi_DEM_O_GI` · `…HD1_THANG_KHONG_DAT_5_tren_23_ky_va_liet_ke_18_ky_do` · `…ly_do_ghi_NGAY_ANH_o_ca_hai_cong` · `…ba_con_so_tom_DEM_DUNG_danh_sach_cong` — qua HTTP thật *(thẻ + bảng tuyến + vỏ `{data,error,meta}`)*. Nguyên văn tuyến trả *(§Số ra)* | đạt |
| **AC-2** · `CG1-B2` | tệp vắng ⇒ cả hai `null`, `chua_do_duoc` **+2 đúng**; ⛔ 200 toàn xanh | `test_CG1_B2_tep_do_VANG_hai_cong_null_chua_do_duoc_tang_DUNG_2[khong_truyen]` + `[duong_khong_co_tep]` — so **cùng kho, cùng lúc** với máy có tệp: hiệu `chua_do_duoc` = 2 **và** tập cổng `null` thêm **đúng** `{FINAL, HD1_THANG}`, mọi cổng khác `dat` y nguyên *(⛔ bù trừ)*; `dat < số cổng` · `chua_do_duoc ≥ 6`. `…ly_do_tep_vang_KHONG_lo_duong_dan_may`. Máy thật `tools/chay_cua.py` trên kho `fls` 5434: có tệp `dat 1 · khong_dat 2 · chua_do_duoc 6`; `--tep-do ''` `dat 0 · khong_dat 1 · chua_do_duoc 8` *(+2)* | đạt |
| **AC-3** · `CG1-B3` | bài `/gates` sẵn có + `tests/api` xanh | `tests/api` + `tests/repo/test_doc_bao_cao_pg.py` + hai bài web chạm `/gates`: `3 failed, 482 passed, 11 errors` — 14 đỏ **trùng khít** 14 node đường nền *(`diff` rỗng)*; bài `/gates` sẵn có `test_cong_ra_duoc_va_KHONG_BAO_GIO_toan_xanh` · `test_vo_boc_du_ba_phan…` · `test_de_khong_khoe_ten_may_chu` · `test_cong_KHONG_BAO_GIO_toan_xanh` *(repo, gọi `doc_cong` ⛔ `tep_do` ⇒ `FINAL` vẫn trong tập `None`)* PASSED. Toàn bộ `--duong-nen`: 26 = 26 | đạt |
| **AC-4** · `CG1-B4` | phá MONG ⇒ ĐỎ, trả nguyên ⇒ xanh | §Chứng minh ĐỎ **B** *(4/4 phá MONG bị bắt + một lần bằng tay có dòng lỗi)* + bài `test_CG1_B4_tep_PHA_qua_tuyen_that_HAI_CHIEU` *(tệp phá ở `tmp_path` truyền qua `dung_may`: FINAL lệch 1 ô ⇒ `dat false` · `1/69.510 ô LỆCH`; mọi kỳ đạt ⇒ HD1_THANG `dat true` · `23/23 kỳ đạt` — Đ5 hai chiều, qua tuyến thật)* | đạt |
| **AC-5** · Q8 | `MONG_PYTEST_TOAN_BO` cộng bài mới, cùng commit | `2460 → 2493` *(+33 = `--collect-only` tệp mới)* ở `d6d50f4` cùng mã; `--duong-nen` `chạy 2600 bài (mong ≥ 2493)` · `26 = 26 node id`; bài ghim đỏ trước khi sửa ghim, xanh sau *(`tests/test_dung_moi_truong_isp.py` `51 passed`)* | đạt |

## Số ra *(nguyên văn `GET /api/fls/v1/gates`, máy thật `tools/chay_cua.py`, tệp đo mặc định)*
- `FINAL` · `DAT` · `da_do` = `69.510/69.510 ô (ô Final FLS tính lại = Final AS-IS · 7 khối × 9.930 dòng giữ sau tự soi)` · `ly_do` = `số của ảnh sổ đóng băng ngày 2026-08-26 (⛔ kho sống) · sổ có 69.769 ô = 9.967 dòng × 7 khối; 259 ô ⛔ vào mẫu số = 37 dòng tự soi loại × 7 + 0 ô lỗi Sheets`
- `HD1_THANG` · `KHONG DAT` · `da_do` = `5/23 kỳ đạt` · `ly_do` = `kỳ đỏ 18/23 — kỳ: số dòng thiếu (sổ ⛔ ghép 1-1) — 2025-01: 1 · 2025-02: 2 · 2025-05: 1 · 2025-06: 3 · 2025-07: 4 · 2025-08: 4 · 2025-09: 4 · 2025-10: 9 · 2025-11: 14 · 2025-12: 5 · 2026-01: 4 · 2026-02: 5 · 2026-03: 5 · 2026-04: 8 · 2026-05: 5 · 2026-06: 12 · 2026-07: 23 · 2026-08: 13 (Σ 122 dòng) · số của ảnh sổ đóng băng ngày 2026-08-26 (⛔ kho sống) · ⛔ gồm chế độ tự sinh (H15) — luật kỳ do H2 phán, cổng này chỉ đọc `dat_hd1``
- **Đo lại `69.510/69.510`** *(WO: "đo lại, ⛔ tin")* bằng script độc lập *(scratchpad `cf_cg1/do_lai_final.py` — đọc thẳng `tests/fixture/itl_ledge_adjustment.json` + `final_rule.tinh_final` + `tu_soi.soi_mot_dong`, ⛔ qua tool)*: `khối = 7 (hd · pay_type · cdt1 · svc_start · svc_end · id_payee · invoice)` · `dòng sổ = 9967 · dòng tự soi loại = 37 {'2026-07': 37} · dòng giữ = 9930` · `ô sổ (dòng × khối) = 69769 · ô lỗi Sheets bỏ = 0` · **`(a) ô dòng GIỮ sau tự soi: khớp 69510/69510`** · `(b) ô MỌI dòng: khớp 69706/69769` *(= KQ-092 đo (b))*. Và `tools/do_voi_so_luong.py` *(⛔ `--ghi`)* exit 0 · `Σ 9967 9845 … 69510/69510` *(sha256 tệp đo trước = sau)*. ⇒ **con số ISP đúng**, nhưng **Đ4**: nó đếm ô **CHẠY** *(Figure 2.2 hàng ADJUST: "CHẠY 69.510 ô FLS tính lại · KHỚP 69.510")*, ⛔ ô **CÓ** *(69.769)* — nên `da_do` mang nhãn `7 khối × 9.930 dòng giữ sau tự soi` và `ly_do` nói `259 ô ⛔ vào mẫu số`. Xem **Q2**.

## Log ĐỎ → XANH
**① ĐỎ — chưa có mã** *(`python -m pytest tests/api/test_isp_gates_hd1.py -rfE`, nền `575926e`, bài lúc ấy 31 node)*: exit 1 · `24 failed, 1 passed, 6 errors in 0.79s`. Đếm dòng `E` — mọi đỏ vì **THIẾU hành vi**:
- 22 × `AttributeError: module 'fls.repo.doc_bao_cao' has no attribute 'doc_cong_tep_do'`
- 8 × `TypeError: dung_may() got an unexpected keyword argument 'tep_do'` *(6 lỗi dựng fixture + 2 bài tự dựng máy)* — tuyến **chưa nhận** tệp đo truyền vào
- xanh sẵn: `test_MONG_ky_do_TRUNG_hien_vat_DT1a` — so **hai nguồn của MONG** *(⛔ gọi mã CG1)* ⇒ xanh sẵn là đúng.

**② ĐỎ đúng lý do ISP** *("ô chờ còn `dat = null`")* — chỉ đặt **ống** *(API nhận `tep_do`; `doc_cong_tep_do` tạm trả **đúng** ô chờ cũ; ⛔ commit)*: exit 1 · `29 failed, 2 passed in 3.27s`:
- `CG1-B1` FINAL: `AssertionError: {'ma': 'FINAL', 'ten': 'Luat Final tai hien tung o', 'dat': None, 'nhan': 'CHUA DO DUOC', ...}` · `assert (None is True)` — **ô chờ `dat = null`**
- `CG1-B1` HD1: `KeyError: 'HD1_THANG'` — cổng chưa có
- `CG1-B2`: `assert ('vắng' in 'cong nay chay ngoai kho tren anh chup so goc (`fls/oracle/cong_parity.py`), ⛔ khong doc duoc tu mot cau SQL' or …)` — lý do cũ ⛔ nói tệp vắng
- `CG1-B4`: `assert (None is False)` — ô chờ ⛔ đỏ được
- 22 × `assert {'FINAL'} == {'FINAL', 'HD1_THANG'}` *(ca phá hàm thuần)*
- xanh sẵn thêm: `test_CG1_B1_ba_con_so_tom_DEM_DUNG_danh_sach_cong` — đếm tóm + bốn cổng LUÔN `None` là bất biến **đã có** ⇒ bài canh hồi quy, ⛔ đỏ-trước.

**③ XANH**: `31 passed in 3.01s`. Sau đó thêm **2** bài phủ *(xanh ngay, ⛔ đỏ-trước — chứng minh bằng đột biến)*: `test_FINAL_lech_MOT_o_thi_DO_va_noi_so_o_lech` *(M1 trước chỉ một bài bắt)* · `test_chay_cua_MAC_DINH_tro_DUNG_tep_do_that` *(M13)* ⇒ `33 passed in 2.98s`.

## Chứng minh ĐỎ
**A · Đột biến MÃ** *(script `cf_cg1/dot_bien.py … ma`: sửa `fls/repo/doc_bao_cao.py` **một** chỗ — mẫu phải khớp **đúng 1** lần —, chạy tệp bài, trả nguyên byte; sha256 so lại `True`, sau trả nguyên `33 passed`)*: **12/12 bị giết** + M13 trên `tools/chay_cua.py` ⇒ **13/13**.

| Đột biến | Kết |
|---|---|
| M1 FINAL bỏ phép khớp *(`dat=True`)* | `2 failed` |
| M2 HD1 đạt khi có ≥ 1 kỳ đạt | `3 failed` |
| M3 FINAL `0/0` ô coi là đo được *(bỏ Đ3)* | `1 failed` |
| M4 tệp vắng ⇒ hai cổng **biến mất** | `7 failed` |
| M5 bỏ phép `ky_dat` ↔ `theo_ky` | `1 failed` |
| M6 kỳ đỏ lọc theo `thieu > 0` | `1 failed` |
| M7 bỏ qua đường được truyền *(gõ cứng tệp thật)* | `25 failed` |
| M8 mặc định lén khi ⛔ truyền | `1 failed` |
| M9 `_dem` nhận `bool` | `1 failed` |
| M10 lý do lộ đường dẫn tuyệt đối | `1 failed` |
| M11 bỏ phép `ô ≤ 7 khối × dòng giữ` | `1 failed` |
| M12 HD1 bỏ ngày ảnh | `2 failed` |
| M13 `tools/chay_cua.py` trỏ sai tệp mặc định | `1 failed` — `test_chay_cua_MAC_DINH_tro_DUNG_tep_do_that` |

**B · Phá MONG trong bài** *(`CG1-B4` — script `cf_cg1/dot_bien.py … mong`; trả nguyên sha256 `True` ⇒ `exit=0 · 33 passed`)*: **4/4 bị bắt**:

| Phá | Kết |
|---|---|
| `MONG_FINAL_DA_DO_DAU` `69.510` → `69.511` | `exit=1 · 2 failed, 31 passed` |
| `MONG_HD1_DA_DO` `5/23` → `6/23` | `exit=1 · 2 failed, 31 passed` |
| `MONG_KY_DO` bớt `2026-08` | `exit=1 · 2 failed, 31 passed` |
| `MONG_NGAY_ANH` → `2026-08-27` | `exit=1 · 1 failed, 32 passed` |

Bằng tay *(`cf_cg1/pha_mong_tay.py`, `MONG_HD1_DA_DO = "6/23 kỳ đạt"`)*: `pytest tests/api/test_isp_gates_hd1.py · exit 1` · `E       assert '5/23 kỳ đạt' == '6/23 kỳ đạt'` · `FAILED …::test_CG1_B1_HD1_THANG_KHONG_DAT_5_tren_23_ky_va_liet_ke_18_ky_do` · `FAILED …::test_ham_thuan_TEP_THAT_cung_dap_an_voi_tuyen` · `2 failed, 31 passed in 2.97s` ⇒ trả nguyên `sha256 = gốc ? True` ⇒ `exit 0 · 33 passed in 2.96s`.

## Kho thật
- `KHONG_CHAM`. Bài dùng kho **TEST** `fls_test` cụm 5434 *(kết nối chỉ đọc)*; máy thật `tools/chay_cua.py` chạy **chỉ đọc** trên kho `fls` cụm 5434 *(RỖNG — `fls_itl = 0 dòng`)*; `FLS_CHO_GHI_THAT` ⛔ đặt. Tệp đo là ảnh tĩnh đã commit, ⛔ ghi.

## Cách chạy để xem
- `PG_DSN=… FLS_JWT_SECRET=… python tools/chay_cua.py --cong 8088` *(chỉ đọc; dòng in thứ hai nói tệp đo nào)* · `python tools/chay_cua.py --the-tam 120` ⇒ `curl -H "Authorization: Bearer …" http://127.0.0.1:8088/api/fls/v1/gates`. `--tep-do ''` ⇒ hai cổng `CHUA DO DUOC`. Màn F03: ⛔ sửa ở bước này *(FG)*.

## Dev tự thấy còn yếu
1. **`FINAL` ĐẠT trên mẫu số đã BỎ 259 ô.** `69.510/69.510` đếm ô của **9.930** dòng giữ sau tự soi; trên **mọi** dòng là `69.706/69.769` *(63 ô lệch ở 37 dòng 2026-07 — KQ-092 (b), tôi đo lại khớp)*. Quyết định `H2-R1-01` đưa vế ô của **HD1 theo kỳ** về **mọi** dòng; `FINAL` giữ nghĩa oracle *(`test_parity_100_phan_tram_tung_o_tren_CA_SO` ghim `69510` + `len(loai) == 37`)* vì ISP ghi nguyên chữ "69.510/69.510 ô (ĐẠT)". Sau vòng sửa H2, màn F03 có thể có **hai** câu về ô Final với **hai** mẫu số — nhãn Đ4 ở `da_do`/`ly_do` là thứ duy nhất phân biệt. Xem **Q2**.
2. **Đọc khoá ngoài danh sách hợp đồng H2 ↔ CG1.** Hợp đồng liệt kê năm khoá `dat_hd1.*` + ngày ảnh; `FINAL` **buộc** phải đọc `tong.o_parity` · `o_parity_khop` *(khối `dat_hd1` ⛔ có số ô)* và tôi đọc thêm `tong.co` · `tong.loai_tu_soi` cho nhãn Đ4. Bốn khoá này có từ trước H2 và được `MONG["parity_o"]` · `MONG["dong_loai_tu_soi"]` của tool ghim — nhưng ⛔ ai **hứa** giữ tên. Đổi tên ⇒ `FINAL` ra `CHƯA ĐO ĐƯỢC` *(⛔ xanh)* và B1 ĐỎ. Xem **Q3**.
3. **"7 khối" lấy từ MÃ (`final_rule.BAY_KHOI`), ⛔ từ tệp** — tệp ⛔ ghi nó đo khối nào. Chặn một nửa: `ô ≤ 7 × dòng giữ` *(M11)*; một tệp đo **ít** khối hơn sẽ hiện thành "N ô lỗi Sheets" thay vì "N khối ít hơn".
4. **Ba tệp ngoài bảng TRONG** *(`fls/api/cua.py` · `xu_ly.py` · `tools/chay_cua.py`)* — bắt buộc bởi chính câu TRONG "đường dẫn **truyền vào** (hợp đồng tầng 7)": ⛔ có đường nào khác để tuyến biết tệp. Xem **Q1**.
5. **Tệp đọc lại MỖI lần `GET /gates`** *(⛔ đệm; 17.911 byte)* — sinh lại tệp đo khi cửa đang chạy thì số đổi ngay, ⛔ phải khởi động lại *(khác `danh_muc.js` — ảnh lúc khởi động)*. Tôi cho là đúng nghĩa "đọc tệp đo", nhưng ⛔ có bài canh hành vi này.
6. **Kiểm tự mâu thuẫn của `dat_hd1` chỉ trên phần ĐẾM** *(`so_ky` ↔ `theo_ky` · `so_ky_dat` ↔ `ky_dat` ↔ `theo_ky[k].dat`)*; `theo_ky[k].thieu` ⛔ được đối chiếu với gì *(CG1 ⛔ tính lại luật)* — H2 ghi sai `thieu` thì cổng in đúng cái sai ấy. Bài Đ2 `test_MONG_ky_do_TRUNG_hien_vat_DT1a` so MONG của bài với hiện vật DT1a, ⛔ so tệp đo với DT1a.
7. **Chuỗi mới có dấu, chuỗi cũ ⛔ dấu** *(`ten` của `FINAL` giữ `Luat Final tai hien tung o` để ⛔ đổi thứ ⛔ cần)* — F03 sẽ hiện lẫn hai giọng; ISP đòi nguyên chữ `'5/23 kỳ đạt'`.
8. **`BA-07` §2 dòng `/gates` nay lệch mã** — vẫn khai "4 cổng kế toán + `BON_DUONG` … `dat=null`"; sau CG1 `FINAL` là số đo khi có tệp. `02_BA` ⛔ của Dev ⇒ việc `fls-ba` *(§4i dòng 860 đã khai trước CG1)*. `tools/verify_cua_that.py` dựng máy ⛔ truyền tệp ⇒ hai cổng `null` — phép `chua_do_duoc < 5` của nó vẫn đúng, nhưng nó ⛔ chạm hai cổng mới *(⛔ sửa — ngoài phạm vi)*.
9. **Sàn Q8 sẽ xung đột khi gộp** — vòng sửa S0 *(`S0-R3-02`)* có thể nâng cùng dòng `MONG_PYTEST_TOAN_BO`; Q8 = A: orchestrator cộng *(+33 của CG1)*.
10. Hai bài phủ thêm sau mã ⛔ có đỏ-trước *(§Log ③)*; một bài *(`…ba_con_so_tom…`)* xanh từ pha ② vì canh bất biến cũ.

## Câu hỏi *(cả ba `KHONG_CHAN` — orchestrator chốt)*
- **Q1 · Ba tệp ngoài bảng TRONG.** ⓐ *(đã làm — khuyến nghị)* giữ: ống `tep_do` qua `fls/api` là cách **duy nhất** tuyến biết tệp mà ⛔ gõ cứng *(y đường `mo_doc`)*; `chay_cua.py` cho máy thật đo được *(⛔ thì F03 thật luôn "CHƯA ĐO ĐƯỢC" và FG ⛔ được sửa backend)* — giá: R1 phải soi thêm 3 tệp *(+39 −6 dòng)*. ⓑ bỏ phần `chay_cua.py`, để I1/FG nối — giá: máy thật ⛔ hiện cổng HD1 tới I1; FG phải xin sửa backend.
- **Q2 · Mẫu số của `FINAL`.** ⓐ *(đã làm — khuyến nghị cho W3)* giữ nghĩa oracle + nhãn Đ4 *(ISP nguyên chữ)* — giá: hai mẫu số cùng sống. ⓑ đổi `FINAL` sang **mọi** dòng *(như `H2-R1-01` cho HD1)* ⇒ hôm nay **KHÔNG ĐẠT `69.706/69.769`** — giá: ISP §2 + AC-1 sai, cần errata; tool cần một khoá tổng mới *(làn BE-HC)*.
- **Q3 · Hợp đồng H2 ↔ CG1 thiếu bốn khoá `tong.*`.** ⓐ *(khuyến nghị)* orchestrator thêm `tong.o_parity` · `tong.o_parity_khop` · `tong.co` · `tong.loai_tu_soi` vào lệnh "giữ tên — chỉ THÊM" của vòng sửa H2 — giá: một dòng trong TIEN_DO. ⓑ để nguyên — giá: đổi tên ⇒ `FINAL` âm thầm thành "CHƯA ĐO ĐƯỢC" *(an toàn, ⛔ xanh — nhưng chỉ bài B1 biết)*.
