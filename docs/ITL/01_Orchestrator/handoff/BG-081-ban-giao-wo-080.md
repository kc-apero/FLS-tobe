# BG-081 — bàn giao `WO-080` *(ISP 3.1.2 · Step 3 · DT1a)* — HD1 · kiểm kê 122 dòng sổ chưa 1-1 trên ảnh đóng băng, có cổng

| | |
|---|---|
| **Thuộc** | `WO-080` |
| **Phát bởi** | `fls-dev` *(làn **DATA**)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-082` · R2 `KQ-083` · R3 `KQ-084` *(dải orchestrator cấp)* |
| **Commit** | nhánh **cục bộ** `isp/DT1A` @ `b17aaa1` *(mã + bài thử + JSON)* — tách từ nền `329fa68`; ⛔ đẩy theo O2 = A *(orchestrator gộp sau R3 rồi mới đẩy)*. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-dt1a` · cụm PG riêng cổng **5437** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 3 · DT1a** *(8 trường + Substep 1/2)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §5.3.1 HD1 ★ · §5.3.2 AC10 *(sha256 đo lại `5cf6e576ff46f088` — khớp `5cf6e576…` của WO)* · `SO_PHAT_HIEN_ISP-3.1.md` cột *luật phòng tái phạm* *(10 hàng S0-R1)* · `TIEN_DO.md` §Quy ước · `CLAUDE.md` Đ1–Đ5 · `tools/do_voi_so_luong.py` |

## Cổng vào *(`05` §5)*
- git thật: `git log -1` ở worktree = `329fa68 Nền wave 1: nhánh làm việc + isp/S0 @ 3d8318c …` — đúng nền orchestrator giao; nhánh `isp/DT1A`.
- version hợp đồng: ISP 3.1.2 · AP v3.1.2 sha256 khớp. Run id: WO ⛔ nói "đã chạy" ⇒ ⛔ cần.
- WO đủ trường §3.1 *(Màn hình: ⛔ chạm UI; Dữ liệu: `KHONG` ghi kho thật)*. ⛔ mở `HOI` — một chỗ hai cách đọc *(§3 "chỉ ĐẾM" ↔ §7 "122 + 147 dòng")* tôi chọn cách rẻ nhất rồi hỏi ở **Câu hỏi Q1** *(`KHONG_CHAN`)*.
- `WO-080` · `handoff/README.md` · `08_CHANGELOG_RELEASE.md` · Dashboard: **⛔ chạm** — ngoài danh sách tệp của phiếu giao *(WO-080 §Rủi ro 2 · `TIEN_DO.md` §Quy ước · `S0-R1-08`)*; orchestrator ghi lúc gộp.
- Môi trường: `bash tools/dung_moi_truong_isp.sh --cong 5437` ⇒ **7/7 `[ĐẠT]`** · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` *(lần dựng đầu: `da ap 26 migration: [1, …, 26]` · `pg_verify: khop`)*.

## Substep 1 — test cases · kế hoạch tối thiểu · lệnh · giới hạn
1. **Test cases** *(mục 6 của Step 3, phủ mọi dòng mục 8)*: `DT1a-B1` → AC-1 · `DT1a-B2` → AC-2 *(kèm phá thử bằng tay)* · `DT1a-B3` → AC-3 · `DT1a-B4` → AC-4. FE: **N/A** — bước dữ liệu, đầu ra là JSON đóng băng + cổng exit code *(ISP mục 4)*.
2. **Kế hoạch thay đổi tối thiểu** *(⛔ đụng mã nghiệp vụ, ⛔ đụng kho)*: `tools/phan_loai_dong_thieu.py` *(mới)* · `tests/du_lieu/__init__.py` *(0 byte — quy ước repo, orchestrator nhắc: làn DT2 cũng tạo)* · `tests/du_lieu/test_phan_loai_dong_thieu.py` *(mới)* · `docs/ITL/_tools/phan_loai_dong_thieu.json` *(sinh máy)* · phiếu này.
3. **Lệnh** *(từ gốc worktree; `export PG_DSN='postgresql://fls:fls@localhost:5437/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5437/fls_test' PYTHONUTF8=1`)*: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/du_lieu/test_phan_loai_dong_thieu.py` · `…/python tools/phan_loai_dong_thieu.py [--ghi]` · `bash tools/dung_moi_truong_isp.sh --cong 5437 --duong-nen`.
4. **Giới hạn** *(ISP mục 3)*: ⛔ gán được LÝ DO — ảnh đã bỏ Số CT · TK · tiền *(riêng tư)*, và mã ghép đã tạo ra 9.845 ⛔ có trong repo *(fixture ghi "đọc LIVE 2026-08-26")* ⇒ DT1b. Chiều ngược 147 chỉ có **số dòng canon** — ⛔ ảnh nào mang thuộc tính của dòng canon ⛔ ghép.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/phan_loai_dong_thieu.py` *(mới)* | tập THIẾU = `dong_sheet` sổ ∖ `dong_so` đã ghép *(122)* · tập NGƯỢC = bank `pm_join` ∖ `dong_canon` đã ghép *(147)*; mỗi tập đếm **hai cách** *(trường khai của ảnh ↔ tập liệt kê)*; `MONG` khai trong tệp *(lấy từ phép đo tay độc lập của orchestrator 16/11)* + **vân tay** tập dòng; ba checksum lấy THẲNG `MONG` của `do_voi_so_luong.py`; in mẫu số trước tỷ lệ, mẫu số 0 ⇒ ĐỎ; chặn riêng tư trước khi ghi; `--thu-muc` để chứng minh ĐỎ trên bản sao *(⛔ cùng `--ghi`)*; exit 0/1/2. Lúc chạy: **25** phép so *(22 lời gọi `kiem` + vòng phân bố × 3)* + 1 quét riêng tư |
| `tests/du_lieu/__init__.py` *(mới, 0 byte)* | gói bài thử — như `tests/adapters` · `tests/canon` · `tests/ledger` *(đều 0 byte)* |
| `tests/du_lieu/test_phan_loai_dong_thieu.py` *(mới)* | **16** bài *(14 hàm `def test_`; hàm checksum chạy × 3 ảnh ⇒ 14 − 1 + 3 = 16)*: `DT1a-B1` ×4 · `DT1a-B2` ×5 · `DT1a-B3` ×2 · `DT1a-B4` ×3 · CLI/Đ5 ×2. MONG của bài **độc lập** với MONG của tool, và bài **tự giải mã** ba ảnh để so từng dòng |
| `docs/ITL/_tools/phan_loai_dong_thieu.json` *(sinh máy, 3.298 dòng · 73.280 byte)* | 122 dòng thiếu *(`dong_sheet` · kỳ · 9 ô phân loại · `nhan = null`)* + 147 dòng ngược *(`dong_canon` · `nhan = null`)* + mẫu số · đếm · theo kỳ · phân bố · bảng thuộc-tính × kỳ · vân tay |
| `docs/ITL/01_Orchestrator/handoff/BG-081-ban-giao-wo-080.md` *(mới)* | phiếu này |

## Cổng *(kết quả nguyên văn — `PG_DSN=…:5437/fls` · `PG_DSN_TEST=…:5437/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/du_lieu/` | exit 0 · `16 passed in 2.78s` *(lượt cuối, trên đúng `b17aaa1` — sau lần đổi tên biến `_ghep` → `ghep` trong bài đổi chỗ; lượt xanh đầu: `16 passed in 2.56s`)* |
| `bash tools/dung_moi_truong_isp.sh --cong 5437 --duong-nen` *(pytest TOÀN BỘ + `tests/web`, so tập đỏ theo node id)* | exit 0 · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` — 7/7 `[ĐẠT]` môi trường; pytest toàn bộ `exit 1` · `12 failed, 2448 passed, 2 xfailed, 1 warning, 14 errors in 318.26s (0:05:18)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` *(mẫu số: `2476 tests collected` = 12 + 2448 + 2 + 14; 16 bài `tests/du_lieu` nằm trong đó, 0 đỏ)*; `tests/web` `exit 1` · `3 failed, 661 passed in 178.72s (0:02:58)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` — 3 đỏ đều bài SỔ THẬT *(`test_wo022_tien_theo_tien_te_pg::test_AC5…` · `test_wo022_v2_o_tien_pg::test_AC11…` · `test_wo042_mot_tap_ky_tu_trang::test_AC11…`)*. Hai bài chập chờn `test_wo032_man_cua_that.py::test_AC3_…/test_AC7_…` **⛔ đỏ ở lượt này** *(grep `wo032` trong tập đỏ = 0)* ⇒ ⛔ cần lượt chạy lại |
| `python tools/phan_loai_dong_thieu.py` | exit 0 · `KẾT: ĐẠT — mọi phép so khớp MONG · 122 dòng thiếu + 147 dòng ngược · nhan = null (DT1b điền)` |
| `python tools/do_voi_so_luong.py` *(tiền điều kiện ISP mục 5)* | exit 0 · `Σ          9967   9845    3341    2700  30756  22290    112   13  69510/69510` |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-dt1a/.venv/Scripts/lint-imports.exe'` — đỏ của đường nền *(`DUONG_NEN.md:432`: gọi cứng đường Windows + đọc kho THẬT)*; ⛔ do bước này |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (174 file, 1854 bang, 723 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(chạy sau khi có phiếu này; trước phiếu: `173 file, 1848 bang` — +1 tệp · +6 bảng = đúng 6 bảng của phiếu)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` · `B3` `B4` `C5` `C5b` *KHONG DO DUOC* · `A1` `B1` `C6` *DOI TRANG THAI* — **trùng khít** đường nền `DUONG_NEN.md:434` *(đỏ do kho rỗng)*; ⛔ phép nào đọc tệp của bước này |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/bin/lint-imports` *(container: `bin/`, ⛔ `Scripts/*.exe`)* | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ chạm schema ⇒ ⛔ bắt buộc; script dựng đã chạy: `khong co gi de ap` · `pg_verify: khop` · `[ĐẠT] di trú + pg_verify  26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` |

## Bằng chứng từng AC
| AC | Mong | Bằng chứng *(bài · lệnh · exit · dòng nguyên văn)* | Kết |
|---|---|---|---|
| **AC-1** · `DT1a-B1` | 122 dòng; 147 chiều ngược; phân bố kỳ có MONG | `test_DT1a_B1_tap_thieu_DUNG_122_dong_va_chieu_nguoc_147` PASSED — bài **tự giải mã** ba ảnh: mẫu số `(9967, 9845, 9992)` trước, rồi `sorted(set(so) − ghep)` = 122 = danh sách `dong_sheet` của tool **từng phần tử**, mỗi dòng 12 khoá đúng tập, 10 thuộc tính = ô của ảnh; `sorted(bank − canon)` = 147 = `9992 − 9845`. `test_DT1a_B1_phan_bo_ky_va_thuoc_tinh_DUNG_MONG` PASSED — 18 kỳ đúng MONG; `hd_classifying` NTMI **121**/122; `hd_final` OGA 74 · GI 25 · DEP 8 · ITE 7 · khác 8; `pay_type_final` Regular 71 · Thu tiền 51. `test_DT1a_B1_MONG_khai_TRONG_tool…` PASSED *(MONG của tool = MONG độc lập của bài; exit 0 · `KẾT: ĐẠT`)*. `test_DT1a_B1_json_DA_GHI_khop_lan_do_hien_tai` PASSED *(JSON đã commit = lần đo hiện tại)*. Lệnh: `② dòng sổ ⛔ ghép: 122 / 9.967 dòng sổ = 1,22 % · rải 18/23 kỳ · hiệu 9.967 − 9.845` · `③ dòng FLS ⛔ có dòng sổ: 147 / 9.992 dòng canon = 1,47 % · hiệu 9.992 − 9.845` | đạt |
| **AC-2** · `DT1a-B2` | cổng ĐỎ (123 ≠ 122) rồi trả nguyên | xem **§Chứng minh ĐỎ** dưới: bản sao tạm bỏ dòng ghép `dong_so 10 · dong_canon 5` ⇒ `exit=1` · `dòng sổ ⛔ ghép (sổ ∖ ghép): đo 123 · mong 122`; trả nguyên ⇒ `exit=0`; ảnh thật ⛔ chạm *(sha256 bản sao = gốc `34aa375d…`, `git status --short tests/fixture` rỗng)*. Bài: `…bo_MOT_dong_khoi_tap_ghep_thi_DO_123_khac_122_roi_tra_nguyen` PASSED *(đối chứng 0 → phá 1 → trả 0; đòi exit **= 1**, ⛔ "≠ 0")* · `…doi_cho_CUNG_KY_tong_van_122_nhung_VAN_TAY_do` PASSED · `…checksum_BA_anh_la_cong[×3]` PASSED | đạt |
| **AC-3** · `DT1a-B3` | in 9.967 dòng sổ và 9.845 dòng ghép trước tỷ lệ | `test_DT1a_B3_in_MAU_SO_truoc_ty_le` PASSED — cả hai số nằm trước ký tự `%` đầu tiên, và dòng chứa chúng mang nhãn `dòng sổ` / `ghép` *(Đ4)*: `① MẪU SỐ: sổ AS-IS 9.967 dòng sổ · ghép 1-1 9.845 dòng ghép · FLS dựng lại 9.992 dòng canon` *(dòng ② mới có `%`)*. `test_DT1a_B3_mau_so_0_la_DO_khong_phai_0_phan_tram` PASSED — `exit=1` · `mẫu số = 0 — ⛔ đo được tỷ lệ nào (Đ3): {'so_dong_so': 0, 'so_dong_ghep': 9845, 'so_dong_canon': 9992}` · stdout ⛔ có `%` | đạt |
| **AC-4** · `DT1a-B4` | 0 khoá `dien_giai` / `so_chung_tu` / `email` | `test_DT1a_B4_json_ra_0_khoa_dien_giai_so_chung_tu_email` PASSED — máy quét RIÊNG của bài *(⛔ mượn tool)* quét **1.940** khoá *(ngưỡng Đ3 của bài: ≥ 538 = 2 × (122 + 147))*, 0 vi phạm, trên cả kết quả đo lẫn tệp đã commit; `test_DT1a_B4_may_quet_cua_bai_CAN_tren_mau_ban` PASSED *(cắn `Diễn giải` · `so_chung_tu` · `Email Address` · một email · ô `#N/A (Did not find value 'FT1'…)`)*; `test_DT1a_B4_tool_TU_CHAN_truoc_khi_ghi` PASSED. Grep độc lập trên JSON: `@: 0 · Did not find: 0 · khoá dien_giai/so_chung_tu/email: 0` | đạt |

## Log ĐỎ → XANH
**① Đỏ thật trước khi có mã** *(`…/python -m pytest tests/du_lieu/test_phan_loai_dong_thieu.py -rA`)*:
- Lượt 1: `14 failed, 2 passed in 0.88s`. **Hai bài xanh khi công cụ CHƯA tồn tại** — soi từng bài:
  - `test_DT1a_B4_may_quet_cua_bai_CAN_tren_mau_ban` — tự kiểm máy quét **của bài thử**, ⛔ phụ thuộc tool ⇒ xanh sẵn là **đúng** *(Substep 2 ③: ghi bằng chứng, ⛔ phá mã)*.
  - `test_CLI_doi_so_LA_va_ghi_tu_thu_muc_LA_bi_tu_choi` — ⛔ **XANH GIẢ**: bản đầu chỉ đòi `returncode == 2`, mà python thoát **2** với *"can't open file"* — trùng mã `2` của argparse. Sửa **bài** *(chưa có mã nào để "cho xanh")*: mỗi lần từ chối phải mang CÂU của công cụ *(`unrecognized arguments: --la` · `TỪ CHỐI … --thu-muc`)*. Bia ghi trong docstring của bài.
- Lượt 2 *(sau khi sửa bài)*: `15 failed, 1 passed in 0.85s` — mọi đỏ vì **thiếu hành vi**, ⛔ lỗi cú pháp/dựng. Lý do đếm theo dòng `E`: `8 × can't open file '…/tools/phan_loai_dong_thieu.py'` · `6 × assert 2 == 1` · `5 × ⛔ chưa có tools/phan_loai_dong_thieu.py — hành vi DT1a chưa có` · `2 × assert 2 == 0` · `1 × ⛔ chưa ghi docs/ITL/_tools/phan_loai_dong_thieu.json` · `1 × assert (2 == 2 and 'unrecognized arguments: --la' in "…can't open file…")`.

**② Lần chạy đầu của tool** — mọi MONG độc lập khớp ngay; chỉ hai vân tay đặt chỗ `TODO` đỏ *(chính cổng vân tay tự chứng minh nó cắn)*: `vân tay tập thiếu (sha256 của 122 dong_sheet đã sắp): đo '18047e0eb0319ea1' · mong 'TODO'` · `… tập ngược …: đo '6ac2463a190ff631' · mong 'TODO'` · `exit=1` ⇒ ghim ⇒ `exit=0`.

**③ Xanh**: `16 passed in 2.56s` *(exit 0 — lượt xanh đầu)*. Sau đó sửa phép hai nguồn của tập thiếu *(bản đầu so `9.967 − số ghép TỰ ĐẾM` với tập liệt kê — một nguồn so với chính nó; nay so trường KHAI `so_dong_so − so_dong_ghep` của ảnh ghép)* và thêm phép `trường so_dong_so ↔ đếm ảnh sổ` ⇒ `16 passed in 2.74s`; JSON ra **y nguyên byte** *(`cmp` = 0)*.

**④ Bằng chứng §Chứng minh ĐỎ dưới đây chạy lại trên đúng `b17aaa1`** *(`git diff --stat b17aaa1 -- tools tests` rỗng)*.

## Chứng minh ĐỎ *(bằng tay, bản sao ở scratchpad — ⛔ chạm `tests/fixture/`)*
| Kịch bản | Lệnh / thao tác | Kết quả nguyên văn |
|---|---|---|
| ⓪ bản sao NGUYÊN *(đối chứng)* | `cp tests/fixture/{3 ảnh} <tạm>/` · `--thu-muc <tạm>` | `KẾT: ĐẠT — …` · `exit=0` |
| ① **bỏ 1 dòng khỏi tập ghép** *(DT1a-B2)* | `c["dong"].pop(0)` ⇒ `đã bỏ dòng ghép: dong_so 10 dong_canon 5 · còn 9844` | `exit=1` · `② dòng sổ ⛔ ghép: 123 / 9.967 dòng sổ = 1,23 % · rải 19/23 kỳ · hiệu 9.967 − 9.844` · stderr **12** dòng lệch, trong đó `dòng sổ ⛔ ghép (sổ ∖ ghép): đo 123 · mong 122` · `dòng sổ ⛔ ghép: hiệu trường khai so_dong_so − so_dong_ghep ↔ tập liệt kê: đo 122 · mong 123` · `dòng FLS ⛔ có dòng sổ (canon ∖ ghép): đo 148 · mong 147` · `số dòng ghép: trường so_dong_ghep của ảnh ↔ đếm: đo 9845 · mong 9844` · `vân tay tập thiếu (sha256 của 123 dong_sheet đã sắp): đo '4c86ef09163e1f4d' · mong '18047e0eb0319ea1'` |
| ② **trả nguyên** | `cp tests/fixture/classifying_vs_canon.json <tạm>/` | `KẾT: ĐẠT — …` · `exit=0` |
| ③ **đổi chỗ cùng kỳ** *(bẫy Đ4)* | dòng ghép `#646` `dong_so 656 → 744` · khoá `('2025-01', 'GI \| Gross Inflow', 'GI \| Gross Inflow', 'Thu tiền')` | `exit=1` · stdout **vẫn** `122 / 9.967 dòng sổ = 1,22 % · rải 18/23 kỳ` · stderr **đúng 1** dòng: `vân tay tập thiếu (sha256 của 122 dong_sheet đã sắp): đo 'd21847c4095c384b' · mong '18047e0eb0319ea1'` — mọi cổng TỔNG xanh, chỉ vân tay cắn |
| ④ mẫu số 0 | ảnh sổ `dong = []` | `exit=1` · stdout dừng ở `① MẪU SỐ: sổ AS-IS 0 dòng sổ · …` *(⛔ `%`)* · `mẫu số = 0 — ⛔ đo được tỷ lệ nào (Đ3): …` |
| ⑤ thiếu tệp ảnh | `--thu-muc <thư mục rỗng>` | `exit=1` · **một** dòng `LOI FileNotFoundError: [Errno 2] No such file or directory: '…/rong/itl_ledge_adjustment.json'` *(⛔ traceback — `S0-R1-04`)* |
| ⑥ đối số lạ · ghi từ bản sao | `--la` · `--ghi --thu-muc <tạm>` | `error: unrecognized arguments: --la` `exit=2` · `⛔ TỪ CHỐI: --ghi chỉ ghi từ ảnh thật tests/fixture/ — ⛔ ghi hiện vật từ bản sao (--thu-muc)` `exit=2` |

## Bảng đếm thuộc-tính × kỳ *(đếm DÒNG trong 122 dòng thiếu; sinh bằng script từ JSON đã ghi, ⛔ gõ tay; `NTMI` = `Need to manual input`; mã = phần trước `\|`)*
| kỳ | dòng sổ của kỳ | thiếu | % kỳ | hd_cls = NTMI | hd_final OGA | hd_final GI | hd_final DEP | hd_final ITE | hd_final khác | pay_final Regular | pay_final Thu tiền | cdt1_final SHQ1 | cdt1_final SHQ2 | cdt1_final COR | cdt1_final khác |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025-01 | 748 | 1 | 0,13 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| 2025-02 | 283 | 2 | 0,71 | 2 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 2 | 0 | 0 |
| 2025-05 | 408 | 1 | 0,25 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 2025-06 | 350 | 3 | 0,86 | 3 | 3 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 3 | 0 | 0 |
| 2025-07 | 549 | 4 | 0,73 | 4 | 4 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 4 | 0 | 0 |
| 2025-08 | 537 | 4 | 0,74 | 4 | 3 | 0 | 0 | 0 | 1 | 1 | 3 | 0 | 4 | 0 | 0 |
| 2025-09 | 501 | 4 | 0,80 | 4 | 4 | 0 | 0 | 0 | 0 | 2 | 2 | 2 | 2 | 0 | 0 |
| 2025-10 | 487 | 9 | 1,85 | 9 | 4 | 1 | 4 | 0 | 0 | 8 | 1 | 3 | 3 | 2 | 1 |
| 2025-11 | 477 | 14 | 2,94 | 14 | 3 | 1 | 4 | 6 | 0 | 10 | 4 | 7 | 6 | 1 | 0 |
| 2025-12 | 566 | 5 | 0,88 | 5 | 3 | 1 | 0 | 0 | 1 | 4 | 1 | 1 | 3 | 1 | 0 |
| 2026-01 | 471 | 4 | 0,85 | 4 | 3 | 1 | 0 | 0 | 0 | 3 | 1 | 1 | 3 | 0 | 0 |
| 2026-02 | 439 | 5 | 1,14 | 5 | 3 | 1 | 0 | 0 | 1 | 3 | 2 | 1 | 3 | 1 | 0 |
| 2026-03 | 584 | 5 | 0,86 | 5 | 3 | 1 | 0 | 0 | 1 | 3 | 2 | 0 | 4 | 0 | 1 |
| 2026-04 | 600 | 8 | 1,33 | 8 | 5 | 1 | 0 | 0 | 2 | 4 | 4 | 3 | 3 | 1 | 1 |
| 2026-05 | 537 | 5 | 0,93 | 5 | 5 | 0 | 0 | 0 | 0 | 2 | 3 | 3 | 1 | 0 | 1 |
| 2026-06 | 613 | 12 | 1,96 | 12 | 8 | 4 | 0 | 0 | 0 | 7 | 5 | 8 | 1 | 3 | 0 |
| 2026-07 | 686 | 23 | 3,35 | 23 | 13 | 9 | 0 | 0 | 1 | 12 | 11 | 19 | 4 | 0 | 0 |
| 2026-08 | 487 | 13 | 2,67 | 13 | 9 | 4 | 0 | 0 | 0 | 6 | 7 | 12 | 1 | 0 | 0 |
| **Σ 18 kỳ** | 9.323 *(cả sổ 9.967)* | **122** | 1,22 *(/ cả sổ)* | **121** | **74** | **25** | **8** | **7** | **8** | **71** | **51** | **60** | **49** | **9** | **4** |

- `hd_final` khác 8 = `NB \| Lưu chuyển nội bộ` 2 · `OMC \| Online Marketing Cost` 2 · `LC \| License Cost` 2 · `LMN \| Loan/Borrowing` 1 · `BON \| Bonus` 1. `cdt1_final` khác 4 = `CAH \| Astronex` 1 · `TOR \| Project A` 1 · `SHQ2 \| Headquarters1` 1 · `SHQ1\| Headquarters1` 1.
- **5** kỳ ⛔ có dòng thiếu: `2024-10` · `2024-11` · `2024-12` · `2025-03` · `2025-04` ⇒ 18/23 kỳ có thiếu — khớp AP v3.1.2 §5.3 *"tháng còn thiếu là 18/23"* *(hai nguồn)*.
- Dòng thiếu **duy nhất** mà máy CÓ trả lời *(`hd_classifying = GI | Gross Inflow`, ⛔ NTMI)* là dòng thiếu duy nhất của kỳ `2025-01`.
- ⚠ **Quan sát, ⛔ nhãn** *(nhãn là việc DT1b)*: hai ô `cdt1_final` trông như gõ tay lệch khuôn — `SHQ1| Headquarters1` *(thiếu dấu cách)* · `SHQ2 | Headquarters1` *(mã ↔ tên chéo)*.

## Kho thật
- `KHONG_CHAM`. Công cụ chỉ đọc ba tệp `tests/fixture/*.json`; ⛔ mở kết nối PG, ⛔ đọc Drive/mạng; `FLS_CHO_GHI_THAT` ⛔ đặt. Kho `fls` cụm 5437 vẫn `fls_itl = 0 dòng` *(script kiểm, kết nối chỉ đọc)*.

## Cách chạy để xem
- N/A — ⛔ chạm UI. Xem bằng `…/python tools/phan_loai_dong_thieu.py` *(in bảng)*.

## Dev tự thấy còn yếu
1. **Checksum hai ảnh `classifying_vs_canon` · `pm_join` chỉ so TRƯỜNG đã ghim, ⛔ tính lại từ nội dung** — thừa kế đúng cách của `do_voi_so_luong.py` *(tôi thử 4 tổ hợp `dong`/`bang_gia_tri`/`cot` cho ảnh ghép và 4 cho `pm_join`: ⛔ tổ hợp nào ra `7226ef112dbd00f7` / `6ec10945e6c1636a`; tệp sinh ra hai ảnh ⛔ có trong repo — Đ1, đo 16/11: tên ảnh xuất hiện ở **7** tệp `.py` của `fls/`+`tools/`+`tests/` *(gồm 2 tệp của bước này)*, **0** dòng `write`/`dump` ra chúng; `docs/` **4** tệp `.md` nhắc tên, **0** dòng "sinh/tạo"; trường `checksum_noi_dung` của hai ảnh chỉ được so ở `tests/ledger/test_classifying.py:103` · `tests/adapters/test_pm_join.py:329` · `tools/do_voi_so_luong.py:125,133`)*. Hệ quả: sửa NỘI DUNG ảnh ghép mà giữ trường ⇒ checksum vẫn xanh. Phần bù của bước này: vân tay tập dòng + 5 phép so trường-khai ↔ đếm *(`tools/phan_loai_dong_thieu.py:196` · `:197` · `:202` · `:219` · `:222`)* + 3 phép ⛔ trùng + 2 phép tập con — kịch bản ① và ③ đều bị bắt, nhưng một phép sửa ô `cls_*` của ảnh ghép thì **chỉ** `tests/ledger/test_classifying.py` bắt *(68.915 ô)*, ⛔ công cụ này.
2. **Vân tay là MONG tự ghim**, ⛔ độc lập: ghim ở lần chạy đầu, sau khi mọi MONG khác đã khớp phép đo tay của orchestrator. Nó chứng minh "tập ⛔ đổi kể từ 16/11", ⛔ chứng minh "tập đúng". Phần "đúng" dựa vào bài B1 tự tính lại tập từ ba ảnh — nhưng bài ấy và công cụ dùng **cùng định nghĩa** *(hiệu tập theo số dòng)*; nếu định nghĩa sai *(vd. `dong_so` của ảnh ghép là số dòng của một bản sổ KHÁC bản `itl_ledge_adjustment`)* thì cả hai cùng sai mà vẫn khớp. Bằng chứng ngược hiện có: `do_voi_so_luong.py` dùng đúng khoá ấy *(`ky_cua_dong.get(dso)`)* và ra `bank_khong_ky = 147` — trùng số ngược ở đây, nhưng đó cũng là cùng định nghĩa.
3. **Bài B1 `json_DA_GHI_khop_lan_do_hien_tai` ghim `nhan = null`** — khi DT1b điền nhãn **vào chính tệp này**, bài sẽ ĐỎ. Đúng ý *(⛔ sửa tay hiện vật)*, nhưng DT1b phải chọn: ghi nhãn ra tệp riêng, hoặc mở rộng công cụ — xem Q2.
4. **`MAU_EMAIL` / `KHOA_CAM` là hai bản** *(một trong tool, một trong bài thử)* — cố ý, để bài ⛔ dùng máy quét của chính đối tượng nó kiểm; giá: sửa luật một bên thì phải sửa bên kia.
5. Thông điệp lệch dạng `đo X · mong Y` ở các phép so **hai nguồn** *(vd. `trường so_dong_ghep của ảnh ↔ đếm: đo 9845 · mong 9844`)* đọc hơi ngược — "mong" ở đây là vế phải, ⛔ phải số đã ghim. Phán đúng, chữ có thể gây hiểu nhầm.
6. `tests/du_lieu/__init__.py` cũng được làn DT2 tạo song song — cả hai 0 byte nên gộp ⛔ xung đột; nếu một bên ⛔ còn 0 byte thì sẽ xung đột.
7. Công cụ `import` **hàm riêng** `_sha` *(và `MONG`)* từ `tools/do_voi_so_luong.py` — để giữ MỘT bản khai cách băm + checksum *(ISP mục 5)*. Giá: `do_voi_so_luong.py` đổi tên/cách băm ⇒ công cụ này đỏ theo *(ồn ào: `LOI ImportError …` exit 1, hoặc lệch checksum — ⛔ im lặng)*; và kéo theo import `fls.adapters.pm_join` · `fls.oracle.tu_soi` mà bước này ⛔ dùng.

## Câu hỏi *(`KHONG_CHAN` cả hai — orchestrator chốt)*
- **Q1 · ISP §3 "chiều ngược … (chỉ ĐẾM)" ↔ §7 "`phan_loai_dong_thieu.json` (122 + 147 dòng, thuộc tính, `nhan = null`)".** Tôi đã làm **ⓐ**: liệt kê 147 `dong_canon` + `nhan = null`, ⛔ thuộc tính *(ảnh ⛔ có)*.
  - ⓐ *(đã làm — khuyến nghị)* liệt kê số dòng, ⛔ thuộc tính — giá: DT1b có số dòng để gán nhãn; ⛔ thêm dữ liệu nào ngoài số dòng.
  - ⓑ chỉ đếm 147, ⛔ liệt kê — giá: đúng chữ §3, nhưng DT1b phải tự dựng lại tập *(một bản khai thứ hai của cùng phép trừ)*.
  - ⓒ liệt kê kèm `cur`/`hinh` từ `pm_join` — giá: thêm thuộc tính hữu ích cho DT1b, nhưng ngoài phạm vi "chỉ ĐẾM" và đụng `xep_ca_lat`.
- **Q2 · DT1b ghi nhãn vào đâu?** ⓐ *(khuyến nghị)* tệp riêng khoá theo `dong_sheet`/`dong_canon` + vân tay `18047e0eb0319ea1`/`6ac2463a190ff631` của bước này làm khoá ghép — giá: hai tệp, nhưng tập dòng bị khoá, đổi tập ⇒ DT1b đỏ · ⓑ DT1b mở rộng `phan_loai_dong_thieu.py` ghi `nhan` — giá: sửa công cụ và bài `json_DA_GHI…` của bước này.
