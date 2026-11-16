# BG-066 — bàn giao `WO-065` *(ISP 3.1.2 · Step 0 · S0)* — môi trường test ở container + đường nền đo thật + hai gói rỗng có hợp đồng tầng

| | |
|---|---|
| **Thuộc** | `WO-065` |
| **Phát bởi** | `fls-dev` *(làn **BE-CF**)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-067` · R2 `KQ-068` · R3 `KQ-069` *(dải orchestrator cấp)* |
| **Commit** | nhánh **cục bộ** `isp/S0` @ `d895878` *(mã + đường nền)* — tách từ `39524c5`; ⛔ đẩy theo O2 = A: orchestrator gộp vào `claude/laughing-bohr-331pt0` sau R3 rồi mới đẩy. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/agent-a73f7b4b46d6c57c4` |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` §1 · §2.1 · **Step 0** *(8 trường + Substep 1/2)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §1.3.3 · §5.3.1 HD5 *(sha256 đo lại `5cf6e576ff46f088…` — khớp WO)* · `CLAUDE.md` Đ1–Đ5 · Cổng · Bẫy · `TIEN_DO.md` *Quy ước chạy song song* · `10_HOP_DONG_AGENT.md` §3.3 |

## Cổng vào *(`05` §5)*
- git thật: worktree được tạo ở `33ff41c` *(tổ tiên)*, ⛔ phải `39524c5` như phiếu ⇒ tạo `isp/S0` từ đúng `39524c5` *(`git log -1` = `39524c5 Orchestrator ISP 3.1.2: sổ tiến độ + WO-065 (Step 0)`)*.
- version hợp đồng: ISP 3.1.2 · AP v3.1.2 sha256 khớp. Run id: WO ⛔ nói "đã chạy" ⇒ ⛔ cần.
- WO đủ trường §3.1 *(Màn hình: ⛔ chạm UI; Dữ liệu: có)*. `Trạng thái` đã là `DANG_LAM` khi nhận.

## Substep 1 — test cases · kế hoạch tối thiểu · lệnh · giới hạn
1. **Test cases** *(chọn từ mục 6 của Step 0, phủ mọi dòng mục 8)*: `S0-B1` → AC-1 · `S0-B2` → AC-2 · `S0-B3` → AC-3 *(kèm phá thử)* · `S0-B4` → AC-4 · `S0-F1` → AC-5 · AC-6 *(orchestrator làm rõ: kho test riêng theo agent)*. Mỗi ca là **một lệnh có `mong`** — script dựng mang sẵn 6 phép kiểm khai `mong`, chạy `--chi-kiem` TRƯỚC khi dựng để có log đỏ thật.
2. **Kế hoạch thay đổi tối thiểu** *(⛔ đụng mã nghiệp vụ)*: `tools/dung_moi_truong_isp.sh` · `.importlinter` *(+2 khối)* · `fls/cau_hinh/__init__.py` · `fls/bao_cao/__init__.py` *(chỉ docstring vai)* · `docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md`. Thêm theo hợp đồng vai Dev: một dòng `08_CHANGELOG_RELEASE.md` · phiếu này · `WO-065` → `CHO_TEST`.
3. **Lệnh** *(từ gốc worktree)*: `bash tools/dung_moi_truong_isp.sh [--duong-nen|--chi-kiem]` · `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1` · `/home/user/FLS-tobe/.venv/bin/python -m pytest` · `/home/user/FLS-tobe/.venv/bin/lint-imports` · `…/python -m fls.db.pg_migrate` · `…/python tools/do_voi_so_luong.py`.
4. **Giới hạn**: kho test là cụm cục bộ, ⛔ phải `fls-pg-1` *(O4)*; kho `fls` RỖNG ⇒ mọi bài đọc **sổ thật** tự ĐỎ đúng Đ3 ở đây; bước `I2` chạy lại trên máy owner.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/dung_moi_truong_isp.sh` *(mới)* | một lệnh dựng venv dùng chung + cụm PG16 :5433 + role `fls` `LOGIN CREATEDB` + kho `fls` RỖNG + di trú, chạy lại được; 6 phép kiểm khai `mong`; `--duong-nen` in pytest toàn bộ + `tests/web`; 5 chốt từ chối *(ghi thật · DSN lạ · thư mục lạ · cổng có PG khác · kho có `fls_itl`)* |
| `.importlinter` | hợp đồng **10** `fls.cau_hinh` · **11** `fls.bao_cao` — cấm `psycopg` · `fls.repo` · `fls.db`; chú thích vì sao khai SỚM *(tệp dùng chung tuần tự hoá về S0)* |
| `fls/cau_hinh/__init__.py` *(mới)* | gói rỗng, docstring vai: config thuần `IX.*`, ⛔ DB — làn BE-CF |
| `fls/bao_cao/__init__.py` *(mới)* | gói rỗng, docstring vai: engine báo cáo/phân bổ thuần, ⛔ DB — làn BE-HC |
| `docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md` *(mới)* | đường nền THẬT: lệnh · exit · dòng tổng kết · bài đỏ ghi TÊN *(máy sinh từ log)* |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` | một dòng 2026-11-16 |
| `docs/ITL/01_Orchestrator/handoff/WO-065-…md` | `Trạng thái` `DANG_LAM` → `CHO_TEST` *(commit phiếu)* |

## Cổng *(kết quả nguyên văn — `PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` *(kho test `fls_test` mặc định — đường nền thật)* | exit 1 · `12 failed, 2402 passed, 2 xfailed, 14 errors in 304.14s (0:05:04)` — **26** đỏ đều là bài đọc sổ thật tự ĐỎ trên kho rỗng *(Đ3)*, đỏ y hệt trên bản xuất nguyên `39524c5`: `12 failed, 2402 passed, 2 xfailed, 1 warning, 14 errors in 304.26s (0:05:04)` *(so từng node id: 26 = 26, chỉ ở một bên = 0)* |
| `python -m pytest` *(kho test `fls_test_cf` theo quy ước song song)* | exit 1 · `16 failed, 2271 passed, 2 xfailed, 1 warning, 141 errors in 247.09s (0:04:07)` — thêm **131** đỏ vì 19 tệp ghim tên `fls_test` *(Q1)* |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: … '…/agent-a73f7b4b46d6c57c4/.venv/Scripts/lint-imports.exe'` *(`tools/kiem_so_song.py:406` gọi cứng đường Windows; và nó đọc kho THẬT — container ⛔ có)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (168 file, 1817 bang, 720 o ngay, 104 ma QD)` |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` — ĐỎ do kho rỗng: `B3` `B4` `C5` `C5b` *KHONG DO DUOC* · `A1` *(`fls_source`)* `B1` *(`fls_pm_line`)* `C6` *(`fls_adjustment`+`fls_journal`)* *DOI TRANG THAI*; ⛔ phép nào đọc `.importlinter`/hai gói mới |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/bin/lint-imports` *(container: `bin/`, ⛔ `Scripts/*.exe`)* | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` *(lần đầu trên kho rỗng: `da ap 26 migration: [1, …, 26]` · `pg_verify: khop`)* |
| `bash tools/dung_moi_truong_isp.sh` | exit 0 · 6/6 `[ĐẠT]` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` |

## Bằng chứng từng AC
| AC | Mong | Bằng chứng *(lệnh · exit · dòng nguyên văn)* | Kết |
|---|---|---|---|
| AC-1 · S0-B1 | `python -m pytest` có dòng tổng kết; mọi bài đỏ/lỗi ghi TÊN | `…/python -m pytest -rfE` *(kho `fls_test`)* exit 1 · `12 failed, 2402 passed, 2 xfailed, 14 errors in 304.14s (0:05:04)`; mẫu số thu thập **2.430 bài** *(grep `def test_` = 2.044 hàm / 210 tệp — hai số đếm hai vật)*. **Tên từng bài**: `DUONG_NEN.md` §4.1 *(26 — máy sinh từ log)* + §4.2 *(131 thêm khi kho `fls_test_cf`)* | đạt *(đường nền ghi đủ; bài đỏ có sẵn ⛔ sửa)* |
| AC-2 · S0-B2 | 26/26 di trú áp; `pg_verify` exit 0 | lần đầu: `da ap 26 migration: [1, 2, …, 26]` · `pg_verify: khop` · exit 0; script đo lại qua kết nối CHỈ ĐỌC: `[ĐẠT] di trú + pg_verify  26/26 di trú áp · pg_verify khớp (0 chỗ lệch)` | đạt |
| AC-3 · S0-B3 | `lint-imports` 11 giữ; phá ⇒ ĐỎ, gỡ ⇒ xanh | trước: `Contracts: 9 kept, 0 broken.` *(script `[ĐỎ]` mong 11)*; sau: `Contracts: 11 kept, 0 broken.` exit 0. Phá thử **6/6** *(2 gói × `psycopg`/`fls.repo`/`fls.db`)*: `echo 'import psycopg' >> fls/bao_cao/__init__.py && lint-imports ⇒ exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho BROKEN · trả nguyên sha256 92bffa198321c599 → 92bffa198321c599`; 5 lượt kia cùng khuôn *(`DUONG_NEN.md` §3.1)*; sau trả nguyên: `exit=0 · Contracts: 11 kept, 0 broken.` | đạt |
| AC-4 · S0-B4 | exit 0, in `chay 9845 / co 9967` | `…/python tools/do_voi_so_luong.py` exit 0 · hàng `Σ          9967   9845    3341    2700  30756  22290    112   13  69510/69510`; script: `[ĐẠT] HD1 do_voi_so_luong  chay 9845 / co 9967 (exit 0)`. ⚠ Chuỗi nguyên văn ⛔ có trong output công cụ *(grep `fls/`+`tools/` = 0)* — đo trên hàng `Σ` *(cột `có` = 9967 dòng sổ · `chạy` = 9845 dòng ghép 1-1)*. **Xanh sẵn** cả bằng `python3` hệ thống trước khi dựng *(⛔ phá mã để có đỏ — ISP Substep 2 ③)* | đạt |
| AC-5 · S0-F1 | `pytest tests/web` có dòng tổng kết | `…/python -m pytest -rfE tests/web` *(kho `fls_test`)* exit 1 · `3 failed, 661 passed in 174.51s (0:02:54)` — 3 đỏ = A10 · A11 · A12 ở §4.1 *(sổ thật rỗng)*; `node` = `/opt/node22/bin/node` *(qua `shutil.which`, ⛔ bài nào bị bỏ qua)* | đạt |
| AC-6 | hai lượt song song, `PG_DSN_TEST` khác nhau, đều xanh; cả hai kho tồn tại | `tests/db/test_invariants_pg.py` *(6 bài, ghi `fls_itl`)*: `lượt A (fls_test_a): exit=0 · 6 passed in 0.31s` · `lượt B (fls_test_b): exit=0 · 6 passed in 0.29s`; `psql -l` có `fls_test_a` + `fls_test_b`, mỗi kho **6 dòng** `fls_itl` · 26 di trú. Đối chứng chung một kho: `lượt C2: exit=1 · 3 failed, 3 passed` · `duplicate key value violates unique constraint "pg_database_datname_index"` ⇒ phép đo ⛔ rỗng nghĩa | đạt **cho tệp ⛔ ghim tên** — ⚠ Q1 |

## Log ĐỎ → XANH *(nguyên văn đầy đủ ở `docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md` §2–§3)*
1. Trước khi dựng: `python3 -m pytest --version` ⇒ `No module named pytest` exit 1 · `pg_isready -h localhost -p 5433` ⇒ `localhost:5433 - no response` exit 2 · `python3 -m fls.db.pg_migrate` ⇒ `ModuleNotFoundError: No module named 'psycopg'` exit 1 · `.importlinter` **9** khối.
2. `bash tools/dung_moi_truong_isp.sh --chi-kiem` ⇒ **6/6 `[ĐỎ]`**, exit 1 *(mỗi dòng vì thiếu môi trường)*.
3. Dựng lần đầu *(chưa có hai gói)* ⇒ 5 `[ĐẠT]` + `[ĐỎ] lint-imports … đo: 'Contracts: 9 kept, 0 broken.'`, exit 1 — đỏ vì đúng thứ còn thiếu.
4. Thêm hai gói + hai hợp đồng ⇒ `Contracts: 11 kept, 0 broken.`; phá thử 6/6 ĐỎ rồi trả nguyên.
5. Dựng lần hai ⇒ mọi bước `đã có ⇒ giữ`/`bỏ qua`, di trú `khong co gi de ap`, `KẾT: ĐẠT` exit 0; `pg_ctl stop` rồi chạy lại ⇒ `── cụm: đang tắt ⇒ pg_ctl start` · `KẾT: ĐẠT`.
6. Chốt từ chối *(đều exit 2)*: `FLS_CHO_GHI_THAT=1` · `PG_DSN=…@10.0.0.9:5433/fls` · đối số lạ.
7. ⭐ Soát lại bản đầu tìm ra **hai lỗi của chính script** rồi vá + chứng minh ĐỎ: ⓐ bước dựng hỏng mà 6 phép kiểm vẫn ĐẠT *(nhờ cụm cũ còn chạy)* ⇒ exit 0 sai — nay bước dựng hỏng là `[ĐỎ]`: `FLS_PGDATA=<thư mục có tệp lạ>` ⇒ `⛔ … có dữ liệu mà ⛔ phải cụm PG — TỪ CHỐI` · `[ĐỎ] dựng · cụm … ⛔ tạo role/kho, ⛔ chạy di trú` · exit 1, tệp lạ còn nguyên; ⓑ cụm bị từ chối mà vẫn chạy di trú lên `PG_DSN` — nay dừng chuỗi, và di trú từ chối kho có dòng `fls_itl`: kho nháp `fls_thu_bao_ve` + 1 dòng ⇒ `⛔ kho fls_thu_bao_ve có 1 dòng fls_itl ⇒ ⛔ phải kho RỖNG cục bộ — TỪ CHỐI di trú` · exit 1 *(kho nháp đã DROP)*; ⓒ chốt cổng: tắt cụm của script, dựng tạm một cụm khác trên 5433 ⇒ `⛔ cổng 5433 đã có một PostgreSQL KHÁC đang nghe — TỪ CHỐI khởi động cụm thứ hai.` · `[ĐỎ] dựng · cụm` · exit 1; gỡ cụm tạm, chạy lại ⇒ `── cụm: đang tắt ⇒ pg_ctl start` · `KẾT: ĐẠT` exit 0.
8. Hồi quy trên **cây cuối** *(sau mọi chỉnh tài liệu/chú thích)*: `…/python -m pytest -rfE` *(kho `fls_test`)* ⇒ exit 1 · `12 failed, 2402 passed, 2 xfailed, 14 errors in 305.89s (0:05:05)` — tập đỏ trùng khít lượt 2 từng node id (26 = 26, `diff` rỗng).

## Kho thật
- `KHONG_CHAM`. Container ⛔ có sổ thật; `FLS_CHO_GHI_THAT` ⛔ đặt *(script từ chối nếu đặt)*. Kho `fls` cục bộ RỖNG, 26 di trú, **0** dòng `fls_itl`. Cụm còn các kho test `fls_test` · `fls_test_cf` · `fls_test_a` · `fls_test_b` *(dựng lại mỗi lượt pytest — vô hại)*; kho nháp `fls_thu_bao_ve` · `fls_test_chung` · `fls_test_x` và hai cụm tạm *(5434 · 5433-khác)* đã gỡ.

## Cách chạy để xem
- ⛔ chạm UI.

## Dev tự thấy còn yếu
1. **Q1 chưa giải — AC-6 chỉ đúng cho tệp ⛔ ghim tên kho.** 19 tệp *(24 dòng `== "fls_test"`, 5 tệp `nghiem_thu`)* làm quy ước `fls_test_<làn>` ĐỎ **131** bài ở lượt toàn bộ. Agent nào chạy cả bộ với `fls_test_<làn>` sẽ thấy 157 đỏ thay vì 26 — dễ bỏ sót đỏ THẬT trong đám đỏ giả.
2. Chốt *"cổng 5433 có PG khác"* đã thấy ĐỎ bằng một cụm tạm chiếm 5433 *(`⛔ cổng 5433 đã có một PostgreSQL KHÁC đang nghe — TỪ CHỐI` · exit 1 · trả nguyên ⇒ `KẾT: ĐẠT`)* — nhưng chỉ thử **một** loại "PG khác" *(cụm cùng máy, ⛔ có role `fls`)*; trên máy owner, `fls-pg-1` qua cổng Docker là loại khác nữa, ⛔ thử được ở đây. Script vốn viết cho container Linux *(`runuser`, `/usr/lib/postgresql/16`)*, ⛔ cho Windows.
3. Script ⛔ có bài pytest riêng — nó cần root + `runuser` + khởi động PG, ⛔ tất định trong bộ test; bằng chứng của nó là log `--chi-kiem` đỏ → dựng → xanh, và 6 chốt đã thử *(2 exit 2 + 3 chốt dựng/di trú + đối số lạ)*.
4. `mong` lint `11` và HD1 `9845/9967` **ghim trong script** — bước nào thêm hợp đồng tầng hay đổi HD1 *(H3 · H15)* phải sửa số ấy *(cố ý, Đ5)*, và `tools/dung_moi_truong_isp.sh` là tệp tuần tự hoá về S0 ⇒ bước sau sửa nó cần orchestrator xếp.
5. Lượt đối chứng `39524c5` chạy trên bản `git archive` *(⛔ có `.git`)*; bài nào cần git sẽ khác vì thế, ⛔ vì mã — đã đo: tập đỏ trùng khít từng node id (26 = 26) ⇒ ⛔ thấy bài nào lệch vì thiếu `.git`; nhưng bài XANH nhờ git thì phép so tập đỏ ⛔ bắt được.
6. `kiem_so_song` ⛔ chạy được ở container *(đường Windows + kho thật)* ⇒ phép so số sống ↔ máy **⛔ có** cho mọi bước ISP chạy ở đây cho tới khi O4 chạy lại trên máy owner.

## Câu hỏi cho orchestrator *(mỗi câu kèm phương án — ⛔ chặn S0)*
| # | Câu | Phương án | Khuyến nghị |
|---|---|---|---|
| Q1 | Quy ước kho test `fls_test_<làn>` *(TIEN_DO)* đụng 24 dòng ghim `== "fls_test"` ở 19 tệp *(5 trong `nghiem_thu`)* ⇒ +131 đỏ giả | **A** · mỗi agent một **cụm/cổng** riêng *(5434 cf · 5435 hc · 5436 fe · 5437 data…)*, kho vẫn tên `fls_test` — được: ⛔ sửa bài nào, chạy được ngay *(đã thử: 5433 + 5434 song song `3 passed` ×2)* · mất: thêm cụm, script cần biến cổng *(sửa tệp tuần tự hoá S0)*. **B** · một WO đổi 24 dòng thành so với `ten_kho(dsn_test())` *(đúng thiết kế ③ của `fls/db/kho.py`: "tên kho khai ở đây và chỉ ở đây")* — được: sạch lâu dài · mất: chạm 5 tệp `nghiem_thu` ⇒ cần `fls-test`, và **"sửa bài có sẵn"** cần WO riêng. **C** · tuần tự hoá lượt TOÀN BỘ trên một kho `fls_test` *(khoá `flock`)*, `fls_test_<làn>` chỉ cho tệp đích ⛔ ghim — được: ⛔ đổi gì · mất: các agent chờ nhau ~5 phút mỗi lượt | **A** ngay *(giao cho bước BE-CF kế tiếp hoặc một vá S0 vòng 2)*, **B** sau qua WO cho `fls-ba`/`fls-test` |
| Q2 | `kiem_so_song` gọi cứng `.venv/Scripts/lint-imports.exe` và đọc kho THẬT; sau gộp S0, số ghim `9 kept` ở dashboard:137 + roadmap:45 sẽ lệch máy *(11)* | **A** · orchestrator chạy `dong_bo_so_song --ghi` trên máy owner sau gộp *(và sửa `CLAUDE.md` "9 hợp đồng tầng")* · **B** · WO cho `fls-dev` làm `kiem_so_song` tìm `lint-imports` theo nền tảng | **A** khi gộp; **B** khi có bước dư |
| Q3 | AC-4 đòi *in* `chay 9845 / co 9967` — công cụ ⛔ in chuỗi ấy *(in hàng `Σ`)*; `tools/do_voi_so_luong.py` thuộc làn BE-HC | **A** · nhận đo trên hàng `Σ` *(đã làm; script in lại theo khuôn spec)* · **B** · bước BE-HC thêm một dòng in | **A** |
| Q4 | `fls/kiem/thu_tu_ngay.py:50-51` nói *"`fls.kiem` ⛔ không được biết `fls.repo`"* nhưng `.importlinter` có **0** dòng nhắc `fls.kiem` ⇒ luật ấy ⛔ máy nào canh | **A** · WO nhỏ thêm hợp đồng 12 `fls.kiem` *(cấm `psycopg`/`fls.repo`/`fls.db`)* · **B** · ghi nhận, để sau | **A** — ngoài phạm vi S0 nên ⛔ tự làm |
