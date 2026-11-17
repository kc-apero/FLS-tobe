# KQ-087 — biên bản kiểm `BG-086` *(ISP 3.1.2 · Step 8 · DT2 · vòng **R1** — quét TOÀN diff)*

| | |
|---|---|
| **Thuộc** | `BG-086` · `WO-085` *(orchestrator ghi sau — spec = ISP `## Step 8 · DT2`, theo lời giao)* |
| **Kiểm bởi** | `fls-test` *(R1, phiên mới, độc lập)* · 2026-11-16 · orchestrator giao |
| **Phạm vi** | `git diff 329fa68..isp/DT2` — **5** tệp, 1.268 dòng thêm *(`3902623` công cụ + bài + ảnh · `b714ba0` phiếu)*: `tools/dong_bang_sheet.py` *(382 dòng)* · `tests/du_lieu/test_dong_bang_sheet.py` *(389)* · `tests/du_lieu/__init__.py` *(0 byte)* · `tests/fixture/cau_hinh/ix_fx.json` *(368)* · `BG-086` *(129)*. Nền `329fa68` ⛔ thuộc phạm vi |
| **Cụm** | reviewer cổng **5446** *(`/home/user/fls-pg16-5446`, dựng lượt này — để CHẠY)* |
| **Phán quyết** | **`ĐẠT`** vòng R1 theo thang ISP *(0 CHẶN)* — **0 CHẶN** · **3 NÊN SỬA** *(`DT2-R1-01` · `-02` · `-03`)* · **6 GHI NHẬN**. Mọi test ID `DT2-B1…B3` và dòng mục 8 trong tầm R1 ĐẠT có bằng chứng tự đo. ⚠ Theo `10` §3.4 / mẫu `KQ` *(ĐẠT = không còn `NANG`)*, ba NÊN SỬA phải được sửa ở R2 **hoặc** orchestrator ghi lý do chấp nhận trước khi đóng `WO-085` *(sổ §1: NÊN SỬA ⛔ chặn push)* |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT2.md` *(tệp riêng — orchestrator gộp vào sổ chung ở `isp/S0` lúc gộp nhánh; tiền lệ `…_DT1a.md`)* |

## Cổng vào *(`05` §5)*
- **git:** `isp/DT2` = `b714ba0` *(phiếu)* trên `3902623` *(mã)* trên nền `329fa68` — khớp hash `BG-086` dòng **Commit**. Nhánh cục bộ, ⛔ đẩy — đúng lời giao. `git status` sạch trước và sau mọi phép đo của R1 *(mọi phép phá chạy trên bản sao `git archive isp/DT2` ở scratchpad)*.
- **version spec:** ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` `## Step 8 · DT2` *(dòng `1016`–`1098`)*; AP v3.1.2 §3.2.1 hàng `IX.FX` *("37 dòng 202401 → 202612 (kể cả dòng lạc 202306)")* · §3.2.4 hàng *"bảng tỷ giá"* — đọc trong `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html`. `WO-085` chưa có ⇒ ⛔ so được hash spec trong `WO`; nhãn *"Step 7"* của lời giao ↔ `## Step 8` ISP: BG đã nêu, R1 xác nhận *(ISP `:936` = `Step 7 · CG1`)*.
- **Quyền làn:** 5/5 tệp nằm trong quyền làn DATA *(ISP `:94`: `tests/fixture/cau_hinh/**` · `tests/du_lieu/**` · `tools/dong_bang_sheet.py`)* + phiếu `handoff/`. ⛔ tệp ngoài làn.
- **Gộp thử *(chỉ đọc, `git merge-tree --write-tree`, ⛔ ref nào đổi)*:** `isp/DT2` ↔ `isp/base-w2` · `isp/DT1A` · `isp/DT1B` · `isp/C1` · `isp/H1` · `isp/H2` — **6/6 exit 0** *(0 xung đột; `tests/du_lieu/__init__.py` cùng blob rỗng ở `DT1A` · `DT1B` · `H2` · `base-w2`)* ⇒ đóng BG yếu ⑩ *("⛔ thử gộp thật")*.
- **Quyết định orchestrator đã có — đối chiếu mã:** Q1 cổng chặt hơn chữ ISP *(đỏ khi trùng · thiếu · khoá hỏng · ô rỗng)* — mã `:252-259` ✅ · Q2 `ngay_dong_bang` = `doc_luc` — `:261` · `:272` ✅ *(xem `DT2-R1-06`)* · Q3 ⛔ đổi tên `Month` — ảnh giữ `"khoa": "Month"` ✅ · Q4 giữ id Drive trong `nguon` — ảnh `:4` ✅ *(R1 ⛔ chép id vào phiếu này: ⛔ cần cho bằng chứng)*.

## Cổng chạy lại *(R1 tự chạy ở worktree, `PG_DSN=…:5446/fls` · `PG_DSN_TEST=…:5446/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`; log: `scratchpad/r1_dt2/`)*
| Lệnh | `BG-086` nói *(cụm 5436)* | R1 đo | Khớp |
|---|---|---|:-:|
| `bash tools/dung_moi_truong_isp.sh --cong 5446` *(dựng cụm reviewer)* | 7/7 `[ĐẠT]` | `initdb /home/user/fls-pg16-5446` · `da ap 26 migration` · `pg_verify: khop` · **7/7 `[ĐẠT]`** *(K4 `khớp 25 bảng/view (0 lệch)` · K5 `11 kept, 0 broken` · K6 `chay 9845 / co 9967` · K7 `fls_itl = 0 dòng`)* · `══ KẾT: ĐẠT` · exit 0 | ✅ |
| `pytest tests/du_lieu/test_dong_bang_sheet.py` | `20 passed in 1.97s` | `20 passed in 1.59s` · exit 0 *(`-rA`: 20 tên PASSED = 11 hàm `def test_` mở ra theo tham số)* | ✅ |
| `python tools/dong_bang_sheet.py ix_fx <bản thô> --mong 37 --ra <tạm>` ×2 | exit 0 · sha256 `e2c9fdd028bd3286` · checksum `b6d1f9e9074951f1` | exit 0 ×2 · sha256 **`e2c9fdd028bd3286…`** ×2 = ảnh commit *(`cmp` byte-identical)* · `checksum_noi_dung: b6d1f9e9074951f1` · `[ĐẠT] cổng --mong 37: 37 dòng = mong · trùng 0 · thiếu 0 · khoá hỏng 0 · ô rỗng 0/185` · `soát PII : 6/6 tên cột · 0 thuộc PM_COT_RIENG_TU` · `lạc: [202306]` | ✅ |
| bản sao bỏ `202408` · bản sao + cột `Email Address` | exit 1 · exit 2 ⛔ tệp | exit **1** `thiếu: [202408]` · exit **2** tệp/thư mục **không** *(§Chứng minh ĐỎ ①②)* | ✅ |
| `--duong-nen` **lượt 1** *(HEAD `b714ba0`)* | toàn bộ `12 failed, 2452 passed, 2 xfailed, 14 errors` · `26 = 26` · web `3 failed, 661 passed` · `3 = 3` · `KẾT: ĐẠT` | toàn bộ `12 failed, 2452 passed, 2 xfailed, 14 errors in 312.66s` · `[ĐẠT] … 26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 180.19s` · `[ĐẠT] … 3 = 3` · **`══ KẾT: ĐẠT`** exit 0 · 9 dòng `[ĐẠT]` / 0 `[ĐỎ]` | ✅ |
| `--duong-nen` **lượt 2** *(HEAD `b714ba0`)* | như trên | toàn bộ `12 failed, 2452 passed, 2 xfailed, 14 errors in 312.90s` · `26 = 26` · web `3 failed, 661 passed in 183.36s` · `3 = 3` · **`KẾT: ĐẠT`** exit 0 | ✅ |
| mẫu số *(`S0-R2-03`: cổng so tập ⛔ canh mẫu số ⇒ R1 tự đo)* | `--collect-only` = 2480 · 20 ở `tests/du_lieu/` | `2480 tests collected` = 12 + 2452 + 2 + 14 · `skipped`/`deselected` **0** cả hai lượt · **20** node `du_lieu/test_dong_bang_sheet` · tập đỏ ↔ `duong_nen_bai_do.txt`: 26 ↔ 26 · `tests/du_lieu` trong tập đỏ **0** | ✅ |
| hai bài chập chờn `tests/web/test_wo032_man_cua_that.py::test_AC3_…` / `::test_AC7_…` | ⛔ đỏ cả hai lượt BG | ⛔ đỏ **cả hai lượt** R1 *(grep `wo032_man_cua_that` trong log `FAILED`/`ERROR` web = 0 · 0)*; 3 bài đỏ web = 3 bài SỔ THẬT `wo022` · `wo022_v2` · `wo042` *(đúng đường nền)* | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` exit 0 | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `174 file, 1853 bang` | `174 file, 1853 bang, 723 o ngay, 104 ma QD` exit 0 *(đo TRƯỚC khi thêm hai tệp của R1)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech` *(đường nền)* | exit 1 · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` · `B3` `B4` `C5` `C5b` KHONG DO DUOC · `A1` `B1` `C6` DOI TRANG THAI *(kho rỗng — trùng đường nền)* | ✅ |
| `python tools/soi_bang_tuyen.py` | `40 tuyen` | `✅ ban khai KHOP SQL that o ca 40 tuyen` exit 0 | ✅ |
| `python tools/kiem_thuyet_minh.py` | `31/31` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` exit 0 | ✅ |
| `python -m fls.db.pg_migrate` | `khong co gi de ap` · `khop` | `khong co gi de ap` · `pg_verify: khop` exit 0 | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC *(`.venv/Scripts/lint-imports.exe`)* | exit 1 · `FileNotFoundError: … '/home/user/FLS-tobe/.claude/worktrees/isp-dt2/.venv/Scripts/lint-imports.exe'` — **⛔ KHÔNG ĐO ĐƯỢC** ở container *(đường nền; ⛔ do bước này)* | ✅ *(cùng đỏ)* |

## Phép so ĐỘC LẬP *(R1 — ⛔ import mã tác giả, ⛔ `Decimal`)*
Kịch bản `scratchpad/r1_dt2/scripts/so_doc_lap.py` *(ngoài repo, `python -I`)* đọc bản thô `drive_tho/ix_fx_9_2_effective.json` *(sha256 `f1150294c36ec071…`, 2.810 byte)* bằng `json.loads(parse_int=…, parse_float=…)` trả về **chuỗi literal** của từng số JSON — tức chữ số đúng như tệp thô, ⛔ qua kiểu số nào — rồi so với ảnh đã commit theo **tên** cột.

| Đại lượng *(nhãn — Đ4)* | R1 đo | Ảnh / BG | Khớp |
|---|---|---|:-:|
| ô so *(dòng × cột `Month` + 5 tiền tệ)* | **222** ô = 37 × 6 · **lệch 0** · khoá thừa 0 | BG *"222/222"* | ✅ |
| kiểu ô thô ở 6 cột *(mẫu số 222 — Đ3)* | số JSON **222** · chuỗi 0 · rỗng 0 · khác 0; độ dài mọi dòng thô = 6 | — | ✅ |
| dòng: bản thô ↔ ảnh *(`so_dong` · `len(dong)`)* | 37 ↔ 37 · 37; `thu_tu` = 1…37 liền | 37 | ✅ |
| thứ tự: `202306` | `thu_tu` **25**, trước `202512`, sau `202601` | BG `thu_tu 25` | ✅ |
| SGD `202507` *(giá trị, ⛔ hiển thị `20,692`)* | **`20691.51`** | `"20691.51"` | ✅ |
| tháng dải `202401→202612` có trong ảnh · ngoài dải · trùng | **36/36** · `['202306']` · 0 | — | ✅ |
| ô có phần lẻ / 185 ô tiền tệ · ô dài nhất | **24** / 185 · `19744.785` *(8 chữ số có nghĩa — ⛔ ô nào gần ngưỡng `float`)* | BG *"24"* | ✅ |
| VND = `"1"` | **37/37** | BG 37/37 | ✅ |
| USD 2026 = `26200` · 2024 · 07–12/2025 | **10/12** *(`202601` = 25500 · `202602` = 26000)* · 1 giá `25066` / 12 dòng · 6/6 = `25500` | BG ghi nhận cho `fls-ba` | ✅ |
| `checksum_noi_dung` — R1 **tự viết lại** thuật toán theo docstring `AnhChup` *(sha256(`nguon`) + `\x1f` + JSON dòng sắp)*, ⛔ import | **`b6d1f9e9074951f1`** | `b6d1f9e9074951f1` | ✅ |
| quét PII: khoá *(đỉnh 19 + `khoa` + 5 `cot` + 37 × 7 khoá dòng)* | **284** khoá · khớp `email address` **0** · ký tự `@` trong tệp **0** *(chuỗi `mail` 1 lần = tên `'Email Address'` trong câu `khong_mang_PII`)* | BG *"> 259"* | ✅ |

## Chứng minh ĐỎ *(R1 tự phá trên BẢN SAO của bản thô — `scratchpad/r1_dt2/pha/`, ⛔ chạm ảnh commit)*
Tạo **27** bản sao bản thô thật bằng `scripts/tao_ban_pha.py` *(giữ chữ số: `parse_float=Decimal`, ghi lại literal)* + **10** tệp tổng hợp nhỏ ở `pha2/` *(ca ⑫ ⑮)*; mọi lượt chạy `--ra` vào thư mục tạm riêng.

| Kịch bản *(bản sao bản thô thật)* | Kết quả nguyên văn | Đúng mong? |
|---|---|:-:|
| ⓪ chạy 2 lần bản thô NGUYÊN, `--ra` tạm | exit 0 ×2 · sha256 cả hai = ảnh commit = `e2c9fdd028bd3286…` · `cmp` = byte-identical · `checksum_noi_dung: b6d1f9e9074951f1` | ✅ |
| ① bỏ `202408` | exit **1** · `thiếu: [202408]  (dải chính 202401→202612)` · `[ĐỎ] cổng --mong 37: 36 dòng ≠ mong 37 · thiếu 1 — ảnh đã ghi ĐÚNG NGUỒN …` · tệp ra **CÓ** *(ảnh vẫn ghi — đúng B3)* | ✅ |
| ② thêm cột `Email Address` giả *(giá trị `gia.lap.N@vi-du.invalid`)* | exit **2** · `⛔ TỪ CHỐI: bản thô có cột thuộc PM_COT_RIENG_TU: ['Email Address'] … — ⛔ ghi tệp nào` · tệp **không** · thư mục **không** · `vi-du.invalid` ⛔ lộ | ✅ |
| ②' `Email Address` biến thể NBSP · tab · tiêu đề có mà mọi ô rỗng | exit 2 ×3, ⛔ tệp | ✅ |
| ②'' `Email_Address` · `Email` · `Email` + U+200B + `Address` *(ký tự rộng 0)* · `Địa chỉ email` | exit 0 — **giá trị ⛔ vào ảnh** *(chỉ khoá + 5 cột chọn được ghi)*; tên cột vào `cot_khong_chon`. Đúng spec *(`PM_COT_RIENG_TU` = `{"Email Address"}`)* — ghi chú, ⛔ phát hiện | ✅ |
| ③ `202409` nhập lại thành `202408` *(37 dòng)* | exit 1 · `trùng: [202408]` · `thiếu: [202409]` | ✅ |
| ④ dòng ngắn *(Sheets cắt ô cuối rỗng)* · ô `" "` · dòng `[]` cuối | exit 1 · `ô rỗng: 1/185 [dòng 4 · HKD]` · `ô rỗng: 1/185 [dòng 1 · USD]` · `38 dòng ≠ mong 37 · khoá hỏng 1 · ô rỗng 5/190` | ✅ |
| ⑤ `Month` = `202401.0` | exit 1 · `khoá hỏng: [202401.0]` | ✅ |
| ⑥ dòng dài hơn tiêu đề · tiêu đề `USD ` trùng sau gộp khoảng trắng · `doc_luc` có giờ | exit 2 ×3, ⛔ tệp | ✅ |
| ⑦ đổi chỗ cột *(HKD lên đầu)* | exit 0, ảnh = ảnh gốc *(ánh xạ theo TÊN)* | ✅ |
| ⑧ SGD `202507` = chuỗi `"20,692"` | exit **0** `[ĐẠT]` | ⛔ ⇒ `DT2-R1-02` |
| ⑨ `Month` toàn chuỗi `"202401"` | exit 0 · ảnh **giống từng byte** ảnh commit | ⛔ ⇒ `DT2-R1-02` |
| ⑩ đổi chỗ `202401`/`202402` · dòng lạc lên đầu | exit 0 `lạc: [202401, 202306]` · exit 1 `thiếu: [202307 … 202312]` | ⚠ ⇒ `DT2-R1-03` |
| ⑪ cột tiêu đề `""` mang chữ | exit 0 · `bản thô : 7 cột` ↔ `khoá + 5 · ⛔ chọn 0` | ⚠ ⇒ `DT2-R1-08` |
| ⑫ `doc_luc` = `2026-W46-1` · `20261116` *(tổng hợp `pha2/`)* | exit 0 · `ngay_dong_bang` ghi nguyên chuỗi | ⚠ ⇒ `DT2-R1-06` |
| ⑬ `--ra` là thư mục · cha là tệp | traceback, exit **1**, ⛔ tệp | ⛔ ⇒ `DT2-R1-05` |
| ⑭ VND = 2 ở một dòng | exit 0 — đúng phân vai *(ISP `:1033` loại trừ kiểm nghiệp vụ ⇒ C1; C1 `kiem` ⇒ `LoiFX … VND=2 ⛔ = 1`)* | ✅ |
| ⑮ `--mong 0` · `--mong=-1` *(bản thô thật)* · bản thô 0 dòng · NaN · ô `dict` · thiếu `nguon` *(tổng hợp `pha2/`)* | exit 2 ×6, ⛔ tệp | ✅ *(⛔ bài canh — `DT2-R1-04`)* |

**Ghi đè đường mặc định** *(cây tạm `git archive isp/DT2` + `git init`, ⛔ worktree)*: ⓐ bản thô thật `--mong 36` ⛔ `--ra` ⇒ exit 1 · ` M tests/fixture/cau_hinh/ix_fx.json` *(5+/3−)* · bộ 20 bài `1 failed, 19 passed` *(chỉ `…TAI_TAO…`)*; ⓑ bỏ `202408` ⇒ `2 failed`; ⓒ đổi chỗ hai hàng *(cổng ĐẠT)* ⇒ `1 failed`; trả nguyên `git checkout` ⇒ sha256 `e2c9fdd028bd3286`. Khớp BG yếu ⑤ ⇒ đánh mức ở `DT2-R1-01`.

**Đỏ trước mã** *(cây tạm, gỡ `tools/dong_bang_sheet.py` + `tests/fixture/cau_hinh/`)*: `20 failed in 0.51s` — khớp BG *"20/20 đỏ trước mã"*; trả nguyên sha256 công cụ `95de3f19fe7ed2aa` = BG.

**Đột biến công cụ** *(`scripts/dot_bien.py`, cây tạm; mỗi đột biến khớp mẫu đúng 1 lần, chạy 20 bài, trả nguyên `95de3f19fe7ed2aa → 95de3f19fe7ed2aa`)*: **14** đột biến, bộ bài bắt **3/14** — D9 lạc thành đỏ `4 failed` · D13 cổng đỏ ⇒ exit 0 `7 failed` · D14 bỏ `khong_mang_PII` `2 failed`; **sống 11** *(`20 passed`)*: D1–D8 · D10 · D11 · D12 ⇒ `DT2-R1-04`. Bổ sung cho M1–M11 của BG *(BG phá các cổng chính; R1 phá các chốt phụ)*.

## Bảng AC *(= test ID ISP mục 6 + từng dòng mục 8)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `DT2-B1` | đóng băng từ bản thô ⇒ 37 dòng; checksum ổn định qua 2 lần chạy *(tất định)* | Bản thô thật, 2 lượt `--ra` tạm: exit 0 ×2 · **37** dòng ảnh · sha256 tệp ra = nhau = ảnh commit `e2c9fdd0…` · `checksum_noi_dung` `b6d1f9e9074951f1` ×2. Phép so độc lập: 222/222 ô, lệch 0; checksum tự viết lại khớp. 5 bài `test_DT2_B1_*` PASSED. Đối chứng Đ5: bài checksum-đổi PASSED *(một xu · đổi chỗ)*; D9/D14 bị bài bắt | **ĐẠT** |
| **AC-2** · `DT2-B2` | bản thô có cột `Email Address` giả lập ⇒ ĐỎ, ⛔ ghi tệp | Bản sao bản thô thật + cột giả: exit **2** · một dòng `⛔ TỪ CHỐI … PM_COT_RIENG_TU …` · tệp **không**, thư mục cha **không**, giá trị giả ⛔ lộ ra màn; biến thể NBSP/tab/ô rỗng cũng exit 2. 3 bài `test_DT2_B2_*` PASSED *(gồm "tệp có sẵn giữ nguyên byte")* | **ĐẠT** |
| **AC-3** · `DT2-B3` | bản thô thiếu 1 tháng ⇒ ảnh vẫn ghi đúng nguồn + cổng in `thiếu: [yyyymm]` + exit ≠ 0 khi `--mong 37` lệch | Bản sao bỏ `202408`: exit **1** · `thiếu: [202408]` · `36 dòng ≠ mong 37` · ảnh 36 dòng, ⛔ có `202408`, ⛔ điền. 7 bài `test_DT2_B3_*` PASSED *(gồm `--mong` 36/37/38, trùng-bù-thiếu, khoá hỏng ×2, ô rỗng)* | **ĐẠT** |
| **AC-4** · mục 8 *"DT2-B1…B3 xanh; cổng đã thấy đỏ"* | 20 bài xanh; cổng chứng minh đỏ | `pytest tests/du_lieu/test_dong_bang_sheet.py` ⇒ `20 passed in 1.59s` *(`-rA`: 20 tên PASSED)*; đỏ trước mã `20 failed` *(R1 tái hiện)*; cổng `--mong` đỏ hai chiều trên bản thô thật *(R1 ①)*. ⚠ 11/14 đột biến chốt phụ sống ⇒ `DT2-R1-04` *(⛔ làm AC trượt: AC nói "cổng" — cổng `--mong`/thiếu/trùng đã thấy đỏ)* | **ĐẠT** |
| **AC-5** · mục 8 *"ảnh ⛔ mang khoá PII (quét = 0)"* | quét = 0, mẫu số ≠ 0 | R1 quét **284** khoá ⇒ 0; toàn văn `@` 0. Bài `…khong_mang_khoa_PII_quet_bang_0` PASSED *(mẫu số > 259)* | **ĐẠT** |
| AC-6 · mục 8 *"3 vòng review xong"* | R1 · R2 · R3 | R1 = phiếu này; R2 `KQ-088` · R3 `KQ-089` chưa có | *(ngoài tầm R1)* |
| AC-7 · mục 8 *"điều kiện PUSH: đủ R1·R2·R3, phát hiện chặn = 0"* | — | R1: **0 CHẶN** | *(ngoài tầm R1)* |
| AC-8 · mục 7 *hiện vật* | `tests/fixture/cau_hinh/ix_fx.json` có `nguon` · `ngay_dong_bang` · `khong_mang_PII` · `checksum_noi_dung`; `tools/dong_bang_sheet.py` | 4/4 trường có, khác rỗng *(`ngay_dong_bang` = `2026-11-16` = `doc_luc` bản thô)*; công cụ có | **ĐẠT** |
| AC-9 · mục 2 *goal* | một lệnh: bản đọc → ảnh có checksum + cổng; IX.FX 37 dòng `202401→202612` kể cả lạc `202306` | lệnh ISP chạy đúng *(exit 0, 14 dòng báo + `[ĐẠT]`)*; 36/36 tháng dải + `202306` ở `thu_tu` 25 | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec ISP Step 8 + AP §3.2.1/§3.2.4 + Đ1–Đ5)* | **Đúng spec cho mọi test ID; 3 NÊN SỬA** | Tái dùng đúng, ⛔ chép: `from fls.oracle.anh_chup import AnhChup` · `.checksum()[:16]` *(`:80`, `:262-263`)* và `from fls.adapters.pm_join import PM_COT_RIENG_TU` *(`:79`; chỗ khai duy nhất `fls/adapters/pm_join.py:125`; grep `PM_COT_RIENG_TU\s*[:=]` cả `fls/`+`tools/`+`tests/` = 1)*. Số giữ chữ số: `parse_float=Decimal` *(`:140-141`)*, ô `float` bị từ chối *(`:125`)* — ⛔ mất chữ số nào trên 222 ô *(độc lập)*. Thứ tự sheet vào checksum qua `thu_tu` ✅. Phân vai đúng ISP `:1033`: VND = 1 để C1 *(⑭)*. Lỗ: ô chữ qua cổng *(`-02`)* · `lac`/`thieu` khác C1 *(`-03`)* · lượt đỏ ghi đè ảnh commit *(`-01`)*; ghi nhận `-04`…`-09` |
| **Dữ liệu** *(kho: bước ⛔ chạm kho; dữ liệu = ảnh ↔ bản thô)* | **Ảnh = bản thô, 0 lệch** | 222/222 ô · 37/37 dòng · thứ tự · SGD `202507` = `20691.51` · checksum tự tính khớp · 0 khoá/ký tự PII. Công cụ ⛔ nối kho *(grep `psycopg` · `PG_DSN` · `connect` trong công cụ = 0 dòng)*; cụm 5446 chỉ phục vụ cổng; `fls_itl = 0 dòng` *(K7)*. Kho THẬT `fls-pg-1` ⛔ có ở container ⇒ ⛔ đọc — ⛔ cần cho bước này |
| **Màn hình** | **N/A** | ISP Step 8 §4 *"Frontend: N/A — bước dữ liệu"*; ⛔ dựng máy xem màn |

## Phát hiện *(chi tiết + luật phòng tái phạm: sổ riêng `SO_PHAT_HIEN_ISP-3.1_DT2.md`)*
| F | Mức | Nơi | Tái hiện *(R1 đo)* | Khuyến nghị | Gửi |
|---|---|---|---|---|---|
| `DT2-R1-01` | **NÊN SỬA** *(`NANG`)* | `tools/dong_bang_sheet.py:363-364` · `:7` · `tests/du_lieu/test_dong_bang_sheet.py:204-231` | Lượt ĐỎ ⛔ `--ra` ghi đè ảnh đã commit: `--mong 36` ⇒ ` M …/ix_fx.json`, chỉ 1/20 bài *(`…TAI_TAO…`)* bắt; bài nội dung ⛔ đòi `cong.dat`; checksum ⛔ phủ `cong`. ⛔ phải CHẶN vì: ISP B3 đòi ghi, ⛔ im lặng, chưa ai tiêu thụ | Lượt đỏ ⛔ `--ra` ⇒ ghi `ix_fx.DO.json` *(hoặc đòi `--ra`)*; bài nội dung đòi `cong == {mong 37, so_dong 37, dat True, ly_do []}` | `DEV` *(làn DATA)* |
| `DT2-R1-02` | **NÊN SỬA** *(`NANG`)* | `tools/dong_bang_sheet.py:119-125` · `:128-129` · `:248-249` | SGD `202507` = `"20,692"` ⇒ `[ĐẠT]` exit 0; `Month` chuỗi ⇒ ảnh giống từng byte ảnh commit; C1 `kiem` trên ảnh ấy ⇒ `LoiFX` | Khuôn khai cột SỐ; ô chuỗi/bool ở đó ⇒ ĐỎ `ô ⛔ số k/185` | `DEV` |
| `DT2-R1-03` | **NÊN SỬA** *(`NANG`)* | `tools/dong_bang_sheet.py:56-61` · `:181-207` ↔ `isp/C1:fls/cau_hinh/fx.py:27-43` · `:192-210` | Cùng ảnh, hai định nghĩa: đổi chỗ `202401`/`202402` ⇒ DT2 `lac=['202401','202306']` ↔ C1 `['202306']`; lạc đứng đầu ⇒ DT2 `thieu` 6 tháng *(ĐỎ)* ↔ C1 `thieu=[]`. Ảnh commit: khớp | Orchestrator chốt một định nghĩa trước C5: DT2 dùng `thang_dau` *(luật C1)* hoặc đổi tên trường thành `sai_thu_tu` | orchestrator · `BA` |
| `DT2-R1-04` | GHI NHẬN *(`NHE`)* | `tools/dong_bang_sheet.py:136-157` · `:221-241` · `:128-129` · `:203` · `:355` | 11/14 đột biến chốt phụ sống trước 20 bài; mọi chốt chạy đúng lúc chạy | Thêm 11 bài `test_R1_04*` *(đã viết, xanh; bắt D1–D8 · D10)* | `DEV` |
| `DT2-R1-05` | GHI NHẬN | `tools/dong_bang_sheet.py:363-364` · `:318-330` · `:7` | `--ra <thư mục>` ⇒ traceback, exit 1 *(= mã "cổng ĐỎ, ảnh đã ghi")*, ⛔ tệp | Bắt `OSError`, một dòng, mã riêng | `DEV` |
| `DT2-R1-06` | GHI NHẬN | `tools/dong_bang_sheet.py:149-152` · `:261` · `:272` | `doc_luc` `2026-W46-1` / `20261116` ⇒ ĐẠT, ghi nguyên vào `ngay_dong_bang` | Ghi `.isoformat()` | `DEV` |
| `DT2-R1-07` | GHI NHẬN | ISP `:1032` · `:50` · `BG-086` | `doc_dan`/`doc_du` ⛔ dùng *(O7, BG tự nêu)*; `do_kha_nang_doc` grep BG/công cụ/bài = 0/0/0; một lượt đọc | `WO-085` ghi chúng thuộc lượt đọc + ai làm; DT3+ đọc hai lần | orchestrator · `BA` |
| `DT2-R1-08` | GHI NHẬN | `tools/dong_bang_sheet.py:221` · `:264` · `:302-305` · `:238-240` | cột tiêu đề `""` có dữ liệu ⇒ exit 0, báo 7 cột ↔ 1 + 5 + 0 | Đếm/báo cột ⛔ tên có dữ liệu, hoặc từ chối như dòng dài | `DEV` |
| `DT2-R1-09` | GHI NHẬN | `BG-086` Substep 1 ② | *"12 thư mục `tests/*`"* = 12 **tệp** = `tests/` + 11/14 thư mục con | Ghi đúng nhãn ở phiếu sau | `DEV` |

## Bài đề xuất *(⛔ commit ở R1 — lời giao chỉ cho commit phiếu + sổ; tệp: `scratchpad/r1_dt2/de_xuat_bai/test_r1_dt2_de_xuat.py`, 17 bài)*
Chạy trên cây tạm `git archive isp/DT2` *(GOC = gốc cây)*.

| Bài | Trên `3902623` | Chứng minh ĐỎ/XANH bằng cách | Sau bản vá thử *(cây tạm, `scripts/va_thu.py`)* |
|---|---|---|---|
| `test_R1_01_cong_DO_khong_ghi_de_anh_o_duong_mac_dinh` | **ĐỎ** | gọi `main()` trong tiến trình, `GOC` trỏ thư mục tạm có "ảnh commit" giả, bản thô thiếu `202408` ⛔ `--ra` ⇒ ảnh giả bị ghi đè | ✅ |
| `test_R1_01b_anh_da_commit_mang_cong_DAT` | xanh | ĐỎ sau khi chạy bản thô thật `--mong 36` vào đường mặc định *(`1 failed`)*; `git checkout` ⇒ xanh | ✅ |
| `test_R1_02_o_chu_trong_cot_tien_te_thi_DO` ×3 | **ĐỎ** ×3 *(exit 0)* | ô `"20,692"` · `"20691.51"` · `" 20691.51"` ở SGD dòng 19 | ✅ |
| `test_R1_04_moi_duong_tu_choi_exit_2_khong_ghi` ×9 · `…04b` · `…04c` | xanh ×11 | mỗi đột biến D1–D8 · D10 làm ≥ 1 bài ĐỎ *(`scripts/dot_bien_r1.py`)*; D11 sống *(phòng thủ chồng với D8)* | ✅ |
| `test_R1_05_loi_ghi_khong_trung_ma_cong_DO` | **ĐỎ** | `--ra` là thư mục ⇒ exit 1 + traceback | ✅ |

Tổng trên `3902623`: `5 failed, 12 passed`; sau bản vá thử **+12 · −1** dòng *(chỉ cây tạm — `scratchpad/r1_dt2/ban_va_thu.diff`: 5 dòng cho `-02`, 7 cho `-01` + `-05`)*: 20 bài DT2 + 17 bài đề xuất = **`37 passed`** ⇒ ba khuyến nghị `-01`/`-02`/`-05` làm được mà ⛔ phá bài nào của Dev.

## Đ1 · đối chiếu các câu khẳng định của `BG-086` *(R1 đo lại — ⛔ tin phiếu)*
| Câu `BG-086` | R1 đo | Kết |
|---|---|:-:|
| *"chỗ khai duy nhất: `fls/adapters/pm_join.py:125`"* | grep `PM_COT_RIENG_TU\s*[:=]` ở `fls/`+`tools/`+`tests/` = **1** dòng, `pm_join.py:125` | ✅ |
| *"20/20 đỏ trước mã"* | cây tạm gỡ công cụ + `cau_hinh/` ⇒ `20 failed in 0.51s` | ✅ |
| yếu ⑤ *"CHỈ `…TAI_TAO…` bắt"* *(lượt `--mong 36` vào đường mặc định)* | `1 failed, 19 passed` — đúng bài ấy | ✅ ⇒ mức ở `DT2-R1-01` |
| *"đối chứng Đ5 cho mỗi cổng công cụ có"* | 11/14 đột biến chốt phụ sống | ⚠ ⇒ `DT2-R1-04` |
| *"12 thư mục `tests/*` có nó"* | 12 **tệp** = `tests/` + 11/14 thư mục con | ⚠ ⇒ `DT2-R1-09` |
| *"`tests/du_lieu/__init__.py` … gộp sạch theo lý thuyết; ⛔ thử gộp thật"* | `merge-tree` với 6 nhánh: 6/6 exit 0 | ✅ *(đóng yếu ⑩)* |
| ghi nhận cho `fls-ba`: *"2026 điền sẵn 26.200"* ↔ ảnh 10/12 | 10/12 *(`202601` 25500 · `202602` 26000)*; *"2024 một giá"* 1/12; *"07–12/2025 = 25.500"* 6/6; VND = 1 37/37 | ✅ — R1 đồng ý chuyển `fls-ba` *(AP §3.2.4 viết gọn quá: 2/12 tháng 2026 ⛔ phải 26.200)* |

## Ngoài phạm vi lượt này *(theo lời giao)*
- **Chỉ commit** phiếu này + sổ riêng lên `isp/DT2`; ⛔ push, ⛔ merge. ⛔ cập nhật `handoff/README.md`, `04_Test/03_TRACEABILITY_GAP_REPORT.md`, dòng nhật ký §5 — orchestrator gom khi gộp *(tiền lệ `S0-R1-08`: tệp dùng chung do orchestrator ghi lúc gộp)*.
- **Bài thử mới:** ⛔ thêm vào `tests/nghiem_thu/` ở R1 — 17 bài đề xuất nằm ở scratchpad *(§Bài đề xuất)*; Dev/orchestrator chọn nhận vào `tests/du_lieu/` *(làn DATA)* hay để `fls-test` thêm vào `tests/nghiem_thu/` ở R2.
- **Cụm 5446** để CHẠY *(`/home/user/fls-pg16-5446`)*.
- Tệp R1 ở scratchpad *(⛔ commit — bản thô thật và bản sao mang số thật)*: `scratchpad/r1_dt2/{scripts,pha,pha2,de_xuat_bai}/` · log `dung_5446.log` · `duong_nen_{1,2}.log` · `pytest_dt2.log` · `so_doc_lap.log` · `so_c1.log` · `dot_bien.log` · `dot_bien_r1.log` · `ban_va_thu.diff`.
