# KQ-092 — biên bản kiểm `BG-091` *(ISP 3.1.2 · Step 4 · H2 · vòng **R1** — quét TOÀN diff)*

| | |
|---|---|
| **Thuộc** | `BG-091` · `WO-090` *(orchestrator ghi sau — spec là ISP Step 4)* |
| **Kiểm bởi** | `fls-test` *(R1, phiên mới, độc lập)* · 2026-11-16 · orchestrator giao |
| **Phạm vi** | `git diff 2664e25..isp/H2` — **5** tệp *(`9cf9999` công cụ + bài + hai JSON · `33d333b` phiếu)*. Nền `2664e25` *(nhánh làm việc + S0 + DT1a)* ⛔ thuộc phạm vi |
| **Cụm** | reviewer cổng **5444** *(đang chạy — để CHẠY)* |
| **Phán quyết** | **`ĐẠT`** vòng R1 — **0 CHẶN** · **2 NÊN SỬA** *(`H2-R1-01` · `-02`)* · **5 GHI NHẬN**. Bốn test ID `H2-B1…B4` ĐẠT có bằng chứng tự đo + đo độc lập; hai NÊN SỬA ⛔ chặn push *(sổ §1)* nhưng **cả hai phải đóng TRƯỚC chữ ký thật đầu tiên của O8** — orchestrator chốt spec *(`-01` cần BA sửa ISP H2-B2; `-02` cần ISP thêm trường)* |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H2.md` *(tệp riêng — orchestrator gộp vào sổ chung lúc gộp nhánh)* |

## Cổng vào *(`05` §5)*
- git thật: `isp/H2` = `33d333b` *(phiếu)* trên `9cf9999` *(mã)* trên `2664e25` — đúng hash `BG-091`; worktree `git status` sạch trước khi kiểm. Nhánh **cục bộ**, ⛔ đẩy *(O2 = A — đúng lời giao)*.
- version spec: ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` sha256 `c2c231d7d9898fdc…` · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` sha256 `5cf6e576ff46f088…` — **cả hai khớp** `BG-091` *(R1 đo lại)*. Step 4 · H2 ở `:691`–`:770`.
- Quyết định orchestrator R1 nhận làm nền *(⛔ kiểm lại)*: tệp nhãn RIÊNG `phan_loai_ly_do.json` theo khuôn H2 *(Q1)*; `5/23` = *(dòng ∨ ký) ∧ ô*, **⛔ gồm tự sinh** *(Q2)*; `_sha`/`MONG` giữ tên + nghĩa *(`DT1a-R1-06`)*; chữ ký buộc bằng số dòng *(Q3 — R1 được hỏi đánh giá mức ⇒ §Q3)*.
- **Lỗi quy trình của R1, khai trước:** lượt `--duong-nen` **1** của R1 chạy **song song** với các phiên pytest đột biến của chính R1 trên **cùng** cụm 5444 — `tests/conftest.py:15` *(fixture phiên, `autouse`)* `DROP DATABASE fls_test` ở đầu **mỗi** phiên ⇒ lượt 1 có 1 bài đỏ THÊM vì `database "fls_test" does not exist — It seems to have just been dropped`. Lượt 1 ⛔ dùng làm bằng chứng; xem §Cổng.

## Cổng chạy lại *(R1 tự chạy ở worktree, `PG_DSN=…:5444/fls` · `PG_DSN_TEST=…:5444/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`; log ở scratchpad `r1_h2/`)*
| Lệnh | `BG` nói | R1 đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/oracle/test_do_voi_hd1.py` | `46 passed` | exit 0 · `46 passed in 15.40s` *(collect: 46 node)* | ✅ |
| `python -m pytest tests/du_lieu tests/oracle` | `155 passed`; nền `109` | exit 0 · `155 passed in 17.60s`; nền bản sao `2664e25`: `109 passed in 3.38s` ⇒ **+46** = đúng số bài mới | ✅ |
| `python tools/do_voi_so_luong.py` | exit 0 · `Σ 9967 9845 …` · `③ 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04` | exit 0 · `Σ          9967   9845    3341    2700  30756  22290    112   13  69510/69510` · `HD1 · ① MẪU SỐ: 23 kỳ · 9967 dòng sổ · 122 dòng thiếu … tệp nhãn … VẮNG · sổ lý do …: 0 chữ ký` · `② … 0/122 · … 0/122` · `③ … 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04` · `④ kỳ đỏ 18/23 … 2026-07 23·0·0 · 2026-08 13·0·0` | ✅ |
| `python tools/phan_loai_dong_thieu.py` *(DT1a import `_sha` + `MONG`)* | exit 0 `KẾT: ĐẠT` | exit 0 · `KẾT: ĐẠT — mọi phép so khớp MONG · 122 dòng thiếu + 147 dòng ngược` | ✅ |
| `.venv/bin/lint-imports` | `11 kept, 0 broken` | exit 0 · `Contracts: 11 kept, 0 broken.` | ✅ |
| `python -m fls.db.pg_migrate` | `khong co gi de ap` · `pg_verify: khop` | exit 0 · cùng chữ | ✅ |
| `bash tools/dung_moi_truong_isp.sh --cong 5444 --duong-nen` — **lượt 1** | `KẾT: ĐẠT` | exit 1 · `KẾT: ĐỎ` — 7/7 `[ĐẠT]` môi trường; toàn bộ `13 failed, 2493 passed, 2 xfailed, 14 errors in 350.91s` · `[ĐỎ] … đo: 27 · thêm 1 · bớt 0` — **THÊM** `tests/api/test_cua_nap_lo_pg.py::test_CA_LO_deu_CHAN_thi_422_KEM_bien_ban`: `500` vì `OperationalError … database "fls_test" does not exist — It seems to have just been dropped` *(13:04:50)*. **Nguyên nhân = R1**: các phiên pytest đột biến + đỏ-trước của R1 chạy CÙNG LÚC trên cùng cụm, mỗi phiên `DROP DATABASE fls_test` *(`tests/conftest.py:15`)*. web `3 failed, 661 passed` · `3 = 3` | **⛔ KHÔNG ĐO ĐƯỢC** *(nhiễu do R1 — ⛔ lỗi H2)* |
| cùng lệnh — **lượt 2** *(⛔ phiên pytest nào khác trên 5444)* | `KẾT: ĐẠT` | exit 0 · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` — 7/7 `[ĐẠT]` *(gồm `HD1 do_voi_so_luong chay 9845 / co 9967` · `lint-imports 11 kept` · `di trú + pg_verify 26/26 · 25 bảng/view (0 lệch)` · `kho fls RỖNG fls_itl = 0 dòng`)*; toàn bộ `12 failed, 2494 passed, 2 xfailed, 14 errors in 336.43s` *(mẫu số **2.522** node)* · `26 = 26 node id (thêm 0 · bớt 0)`; web `3 failed, 661 passed in 182.28s` · `3 = 3` | ✅ |
| hai bài chập chờn `test_wo032_man_cua_that.py::test_AC3_…` / `::test_AC7_…` | ⛔ đỏ ở lượt nào | grep `wo032_man_cua_that` trong dòng `FAILED`/`ERROR` của **4** log *(toàn bộ + web × 2 lượt)* = **0 · 0 · 0 · 0**; grep `test_do_voi_hd1` · `tests/du_lieu` · `tests/oracle` = **0 · 0 · 0 · 0** | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC *(đường Windows)* | exit 1 · `FileNotFoundError … .venv/Scripts/lint-imports.exe` — đỏ của đường nền | ✅ *(⛔ đo được — ⛔ do H2)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `177 file, 1871 bang` | exit 0 · `177 file, 1871 bang` trước phiếu R1; sau khi thêm KQ + sổ: `179 file, 1883 bang` *(+2 tệp · +12 bảng = đúng 11 bảng KQ + 1 bảng sổ)* · `OK K3 bang markdown khong lech` | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `11/16 khop · 5 lech` = đường nền | exit 1 · `11/16 khop · 5 lech (da do 16/20 phep)` · cùng 7 mã; **giống hệt** lượt trên bản sao nền `2664e25` | ✅ |
| `python tools/soi_bang_tuyen.py` | `40 tuyen` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python tools/kiem_thuyet_minh.py` | `31/31` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut` | ✅ |

## Phép đo ĐỘC LẬP *(R1 — ⛔ import `tools/do_voi_so_luong.py`; chỉ dùng hằng `MA_LOI` của `fls/canon/o_loi.py`)*
Kịch bản `do_doc_lap.py` *(scratchpad)* đọc **ba ảnh** `tests/fixture/{itl_ledge_adjustment, classifying_vs_canon, pm_join}.json` + hiện vật DT1a `phan_loai_dong_thieu.json`, tự viết lại `f(Classifying, MID)` *(`Need to manual input` hoặc rỗng ⇒ MID, ngược lại Classifying)* và phép so ô, rồi tính tập kỳ *"dòng 100 % ∧ ô 100 %"*.

| Phép *(nhãn — nó đếm gì)* | Mẫu số | R1 đo | Công cụ / hiện vật | Khớp |
|---|---|---|---|:-:|
| dòng sổ · kỳ | 9.967 dòng sổ · 23 kỳ | 9.967 · 23 | `mau_so` `{23, 9967, 122}` | ✅ |
| **dòng thiếu** = `dong_sheet` sổ ∖ `dong_so` ghép | 9.967 − 9.845 | **122** · giao với DT1a **122** · chỉ-R1 **0** · chỉ-DT1a **0** | `dem.thieu` 122 | ✅ |
| vân tay tập thiếu / ngược *(sha256-16 danh sách đã sắp)* | 122 / 147 dòng | `18047e0eb0319ea1` / `6ac2463a190ff631` | `dat_hd1.van_tay` = DT1a | ✅ |
| kỳ có dòng thiếu | 23 kỳ | **18** kỳ · Σ 122 | `④ kỳ đỏ 18/23` | ✅ |
| **(a) ô — bỏ dòng tự-không-nhất-quán** *(như oracle)* | 69.510 ô *(9.930 dòng × 7)* | 69.510 / 69.510 · kỳ có ô < 100 %: **0/23** | `Σ … 69510/69510` · `o_100` 23/23 | ✅ |
| **(b) ô — MỌI dòng** *(⛔ bỏ dòng nào)* | 69.769 ô *(9.967 × 7, ô lỗi Sheets 0)* | **69.706 / 69.769** — **63** ô lệch, cả 63 ở **37** dòng của **2026-07** *(kỳ ấy 4.739 / 4.802)* | ⛔ có — công cụ chỉ in (a) | ⚠ `H2-R1-01` |
| `loai_tu_soi` theo kỳ | 23 kỳ | `{2026-07: 37}`, 22 kỳ còn lại 0 · 37 dòng ∩ 23 dòng thiếu 2026-07 = **1** | `theo_ky.2026-07.loai_tu_soi` 37 | ✅ |
| **TẬP kỳ đạt** *(dòng 100 % ∧ ô 100 %)* — theo (a) | 23 kỳ | **5**: `2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04` | `ky_dat` = 5 kỳ ấy | ✅ **khớp từng phần tử** |
| TẬP kỳ đạt — theo (b) | 23 kỳ | **5**, cùng 5 kỳ *(2026-07 đã đỏ vì dòng)* | — | ✅ hôm nay; lệch khi ký 2026-07 ⇒ `H2-R1-01` |
| so từng kỳ `o_parity` · `o_parity_khop` · `loai_tu_soi` · `thieu` công cụ ↔ R1 | 23 kỳ × 4 số | **0** kỳ lệch | `voi_so_luong.json` | ✅ |

Đ3: mọi phép trên có mẫu số ≠ 0 *(in ở cột 2)*. Đ4: (a) và (b) là **hai** phép, **hai** nhãn — `5/23` của công cụ là phép (a).

## Kịch bản phá qua đường thật *(R1 — `kich_ban.py` · `kich_ban2.py` ở scratchpad; mọi tệp nhãn/sổ là BẢN TẠM, MONG phá **trong bộ nhớ**; sau cùng sha256 `voi_so_luong.json` · `do_voi_so_luong.py` · `so_ly_do_hd1.json` **= trước**, `git status` sạch)*

| # | Kịch bản | Mong | Đo *(nguyên văn rút gọn)* | Kết |
|---|---|---|---|---|
| K1 | ký giả `R1_A · 23` *(mọi dòng thiếu 2026-07; 99 dòng còn lại nhãn `R1_B` chưa ký)*, MONG gốc | ĐỎ vì 6 ≠ 5 | exit 1 · `kỳ đạt HD1 (dat_hd1_theo_ky): đo (… '2025-04', '2026-07') · mong (… '2025-04')` | ✅ |
| K1′ | như K1, MONG khai 6 kỳ | 2026-07 đạt, tổng 6 | exit 0 · `so_ky_dat 6` · 2026-07 `{dat True · thieu 23 · co_nhan 23 · da_ky 23 · dong_100 False · o_100 True}` · **`loai_tu_soi` 37 · `o_parity` 4.543 / `co×7` 4.802** | ✅ H2-B2 · ⚠ `H2-R1-01` |
| K2 | 122/122 dòng có nhãn, sổ bản sao **rỗng** | vẫn 5, 2026-07 đỏ | exit 0 · 5 kỳ · `dem {thieu 122 · co_nhan 122 · da_ky 0}` · 2026-07 `dat False` | ✅ H2-B3 |
| K3 | ký `R1_B · 99` *(17 kỳ)*, ⛔ ký `R1_A` | 22 kỳ đạt, 2026-07 đỏ | exit 0 · `so_ky_dat 22` | ✅ |
| K4a | chữ ký `'R1_A '` *(dấu cách thừa)* | ĐỎ | `chữ ký 'R1_A ' … ghi số dòng 23 · tệp nhãn có 0 dòng … ký lại` | ✅ |
| K4b | nhãn NFC `Lý do A` ↔ chữ ký NFD | ĐỎ *(⛔ khớp nhầm, ⛔ lặng)* | `… tệp nhãn có 0 dòng …` | ✅ |
| K4c | `ngay` = `2099-12-31` | ĐỎ *(ngày tương lai)* | **⛔ lỗi đầu vào** — chỉ ĐỎ vì MONG 6 ≠ 5 | ⚠ `H2-R1-06` |
| K4d | chữ ký thêm khoá `van_tay_dong` | *(ghi nhận)* | ĐỎ `khoá phải đúng ('nhan', 'so_dong', 'nguoi_ky', 'ngay')` ⇒ thêm khoá về sau = đổi khuôn | ⚠ `H2-R1-02` |
| K4e | tệp nhãn chỉ liệt kê 23/122 dòng | *(ghi nhận)* | ⛔ lỗi đầu vào; 99 dòng = chưa có nhãn | ⚠ `H2-R1-07` |
| K5 | chữ ký cũ `R1_A · 23`; nhãn đổi chỗ 2026-07 ↔ 2025-11 *(A ↔ B chưa ký)* | ĐỎ | ĐỎ vì tập kỳ đổi *(2026-07 mất đạt)* | ✅ |
| K5b | **hai** nhãn đã ký `A · 23` + `C · 14`; đổi chỗ một dòng mỗi bên | ĐỎ *(tập dòng đã ký đổi)* | **exit 0** · `ky_dat` 7 = 7 · dòng `8826` từ A sang C — vô hình | ⛔ `H2-R1-02` |
| K6 | phá MONG: thiếu `2025-04` · thừa `2026-07` · mất khoá · `()` — mỗi cái + `--ghi` | exit 1, ⛔ ghi | rc **1 · 1 · 1 · 1**; mỗi lần đúng **1** dòng stderr chứa `dat_hd1`; `voi_so_luong.json đổi? False` × 4 | ✅ H2-B4 |
| K6′ | trả nguyên | exit 0 | rc 0 · `Σ 9967 9845 … 69510/69510` · `HD1 · ③ … 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04` | ✅ |
| K7 | `--ghi` XANH trên đích tạm | byte = tệp commit, ⛔ sót `.tam` | `True` · `[]` | ✅ |

**Khoá cũ của `voi_so_luong.json`** *(mong: chỉ THÊM `dat_hd1`)*: `git diff --numstat` `217 0`; so dict `2664e25` ↔ `isp/H2`: 9 khoá cũ **y nguyên giá trị** *(`True`)*, thứ tự khoá y nguyên, khoá thêm **duy nhất** `dat_hd1`, khoá mất **0**; byte: **14.144 / 14.146** byte đầu trùng — 2 byte cuối cũ `\n}` thành `,\n "dat_hd1": {…}` *(tệp cũ ⛔ có xuống dòng cuối)*. ⇒ ĐẠT.

## Bảng AC *(= test ID ISP mục 6 · `:728`–`:733`)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `H2-B1` · cổng · sổ rỗng | kỳ đạt = 5 (= AP v3.1.2) | CLI R1 exit 0: `HD1 · ① MẪU SỐ: 23 kỳ · 9967 dòng sổ · 122 dòng thiếu` **trước** `HD1 · ③ … 5/23 · 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04`; sổ thật `chu_ky: []` *(0 chữ ký)*. **Đo độc lập R1** = cùng 5 kỳ, khớp từng phần tử *(§Phép đo độc lập)*. 8 bài B1 PASSED | **ĐẠT** |
| **AC-2** · `H2-B2` · ký giả 2026-07 | 2026-07 thành đạt; tổng 6 | K1′: `so_ky_dat 6`, 2026-07 `dat True · da_ky 23/23`; K1 qua `do()` thật với MONG gốc ⇒ ĐỎ `đo (…, '2026-07') · mong (5 kỳ)`. 2 bài B2 PASSED. ⚠ đạt **đúng chữ ISP** — nhưng 2026-07 có 37 dòng / 63 ô lệch ô ⛔ nhãn ⇒ `H2-R1-01` *(spec)* | **ĐẠT** *(kèm `H2-R1-01`)* |
| **AC-3** · `H2-B3` · nhãn chưa ký | vẫn đỏ | K2: 122/122 có nhãn, 0 ký ⇒ 5 kỳ, 2026-07 `dat False`; ký một phần *(bài)* ⇒ 22/23 ⇒ đỏ; lệch số dòng ⇒ ĐỎ; tệp nhãn vắng + có chữ ký ⇒ ĐỎ; K4a/K4b khác chữ ⇒ ĐỎ. 5 bài B3 PASSED | **ĐẠT** |
| **AC-4** · `H2-B4` · phá MONG | cổng ĐỎ rồi trả nguyên | K6: thiếu · thừa · mất khoá · `()` ⇒ exit **1 × 4**, mỗi lần đúng 1 dòng nguyên nhân, `--ghi` ⛔ ghi *(sha256 trước = sau)*; trả nguyên ⇒ exit 0. Bài B4 PASSED | **ĐẠT** |
| **AC-5** · mục 7 hiện vật | `so_ly_do_hd1.json` rỗng · `dat_hd1` trong `voi_so_luong.json` | `{"_vi_sao": …, "chu_ky": []}` · khối `dat_hd1` ở cuối, khoá cũ y nguyên *(§Khoá cũ)* | **ĐẠT** |
| **AC-6** · mục 3 phạm vi | 4 khoá chữ ký; MONG `dat_hd1_theo_ky` khai trước; ⛔ ký thật; chữ ký tổng hợp chỉ trong test | `KHOA_CHU_KY` `:83` = 4 khoá ISP; MONG `:110` *(đọc trước lần đo — nguồn AP + BG-081)*; sổ thật 0 chữ ký; grep `TONG_HOP` ngoài `tests/` = 0 | **ĐẠT** |

## Đối chiếu từng dòng mục 8 *(Exit criteria — ISP `:744`–`:748`)*
| Dòng | Bằng chứng R1 | Phán |
|---|---|---|
| `H2-B1…B4 đúng` | AC-1…AC-4 trên; `pytest tests/oracle/test_do_voi_hd1.py` R1 chạy `46 passed`; đỏ-trước tái hiện trên bản sao `2664e25` + bài mới: `45 failed, 1 passed` *(39 × thiếu `phan_hd1` + 6 câu thiếu hiện vật — **khớp từng dòng** `BG-091` §Log ĐỎ)* | **ĐẠT** |
| `3 vòng review xong` | R1 xong *(phiếu này)*; R2 `KQ-093` · R3 `KQ-094` chưa chạy | **⛔ chưa tới** *(⛔ phải TRƯỢT — vòng sau)* |
| `điều kiện PUSH: đủ R1·R2·R3, phát hiện chặn = 0` | R1 góp **0 CHẶN**; 2 NÊN SỬA chờ orchestrator *(sửa ở R2 hoặc ghi lý do chấp nhận)* | **R1: đạt phần mình** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 4 · AP §5.3.1 HD1 · `CLAUDE.md` Đ1–Đ5)* | **ĐẠT có ghi chú.** Phép phán `(dòng 100 % ∨ mọi dòng thiếu có nhãn ĐÃ KÝ) ∧ ô 100 %` cài đúng lời giao *(Q2)*; nhãn chưa ký ⇒ đỏ; ký một phần ⇒ đỏ; lệch số dòng / sổ vắng / tệp nhãn hỏng / vân tay khác ⇒ ĐỎ một dòng, ⛔ phán kỳ *(26 ca phá + K4a/K4b)*. Đ3: mẫu số in trước tỷ lệ, `0/0` ⛔ 100 %. Đ5: MONG khai trước, NO cả hai chiều *(K6)*. **Hai lỗ:** vế ô lọc bỏ đúng 37 dòng nó phải bắt *(`H2-R1-01` — gốc spec)*; chữ ký mù trước đổi chỗ giữa hai nhãn đã ký *(`H2-R1-02` — K5b)*. Đột biến: M15 + 3 đột biến R1 sống *(`-03` · `-04`)* | §Kịch bản · §Đột biến · sổ |
| **Dữ liệu** *(ảnh đóng băng trong repo; kho thật ⛔ có ở container)* | **ĐẠT.** Đo độc lập tập kỳ đạt khớp từng phần tử *(5/5)*; 122 dòng thiếu khớp DT1a từng phần tử; ⛔ đếm đôi *(phép `trùng` có ca phá; `có − chạy` ↔ dòng thiếu liệt kê là phòng thủ chồng có ca phá)*; ⛔ mất dòng im lặng: 9.845 + 122 = 9.967. **Nhưng** 63 ô lệch của 37 dòng 2026-07 nằm ngoài mẫu số ô *(phép (b) 69.706 / 69.769)* và 147 dòng FLS ⛔ có dòng sổ ⛔ vào phán kỳ nào *(`-05`)*. Kho: công cụ ⛔ mở kết nối *(R1 grep `psycopg\|connect\|PG_DSN` trong `tools/do_voi_so_luong.py` = 0)*; cụm 5444 K7 `fls_itl = 0 dòng` | §Phép đo độc lập |
| **Màn hình** | **N/A** — ISP §4 *"Frontend: N/A — lát cắt là lệnh/cổng"*; diff ⛔ chạm `fls/web/**` *(5 tệp, ⛔ tệp màn)* | `git diff --stat 2664e25..isp/H2` |

**Riêng tư:** diff ⛔ mang email / `Diễn giải` / Số CT / tên tài khoản *(grep `@…` · `Email` · `Diễn giải` · `dien_giai` · `Tên tài khoản` trên diff = 0 dòng ngoài decorator Python)*; `voi_so_luong.json` khối mới chỉ có **số đếm** + vân tay, ⛔ `dong_sheet` nào. Tên `ThuongCT` *(6 chỗ trong diff)* là vai O8 đã khai ở ISP `:51` — ⛔ PII mới. Chữ ký giả của bài = `TONG_HOP_TEST` *(⛔ tên người)*.

**Làn:** 5/5 tệp thuộc làn BE-HC theo ISP Step 4 §4 + §7 *(`tools/do_voi_so_luong.py` · `docs/ITL/_tools/voi_so_luong.json` · `tests/oracle/test_do_voi_hd1.py` · `docs/ITL/_tools/so_ly_do_hd1.json` + phiếu BG)* — **0** tệp ngoài làn; ⛔ chạm `tools/phan_loai_dong_thieu.py` *(DT1a)*, ⛔ chạm `fls/**`, ⛔ chạm `handoff/README.md` · changelog *(đúng `S0-R1-08`)*.

## Đột biến *(R1 chạy trên bản sao `git archive isp/H2`, ⛔ chạm worktree; `dot_bien.py`; mỗi đột biến chạy `tests/oracle/test_do_voi_hd1.py`, trả nguyên — `cmp` bản sao = `isp/H2`)*
| Đột biến | Kết |
|---|---|
| M15 *(BG)* `--ghi` ghi thẳng | **SỐNG** `46 passed` — xác nhận BG yếu #1 ⇒ `H2-R1-03` |
| R1-M3 bỏ `and o_100` | giết `1 failed` — **chỉ** `test_H2_B3_o_chua_100…` *(`theo_ky` tổng hợp)* ⇒ `H2-R1-01` |
| R1-M17 bỏ dòng in `②` · R1-M18 bỏ dòng in `④` | **SỐNG** × 2 ⇒ `H2-R1-04` |
| R1-M19 bỏ regex ngày *(chỉ `date.fromisoformat`)* | **SỐNG** ⇒ `H2-R1-04` |
| R1-M20 bỏ `dong_100 or` | SỐNG — **tương đương** *(`0 == 0`)*, ⛔ lỗi |
| R1-M21 `co_nhan = len(ds)` | giết — `json_DA_GHI…` |
| R1-M22 lệch số dòng chỉ đỏ khi `đếm < so_dong` | giết — `B3 …LECH_so_dong…` |

## Phát hiện *(chi tiết đầy đủ + luật phòng tái phạm: `SO_PHAT_HIEN_ISP-3.1_H2.md`)*
| Mã | Mức | Nơi | Tái hiện | Khuyến nghị | Gửi |
|---|---|---|---|---|---|
| `H2-R1-01` | **NÊN SỬA** *(`NANG`)* | `tools/do_voi_so_luong.py:387` · `:279-280` · `:285` · ISP `:731` | K1′ + đo (b): ký 23 dòng thiếu 2026-07 ⇒ 2026-07 `dat True · o_100 True` trong khi **37** dòng *(36 đã ghép 1-1)* mang **63** ô `Final ≠ f(Cls, MID)` ⛔ nhãn ⛔ ký; vế ô ⛔ đỏ được trên đường thật *(tautology — R1-M3 chỉ giết bằng dữ liệu tổng hợp)* | ⓐ BA sửa ISP H2-B2: kỳ đạt đòi `loai_tu_soi == 0` hoặc dòng tự-soi loại cũng có nhãn ĐÃ KÝ; ⓑ tối thiểu Dev: `loai_tu_soi` vào `dat_hd1.theo_ky` + CLI `④`, đổi nhãn `o_100`. Trước chữ ký O8 đầu tiên + trước CG1 | `BA` + orchestrator *(spec)* · `DEV` *(nhãn)* |
| `H2-R1-02` | **NÊN SỬA** *(`NANG`)* | `:83` · `:225` · `:265-269` | K5b: hai nhãn đã ký, đổi chỗ một dòng mỗi bên ⇒ exit 0, `ky_dat` 7 = 7 — dòng `8826` sang lý do khác, vô hình | Q3 ⓑ: khoá `van_tay_dong` — **làm khi sổ còn 0 chữ ký**; ISP §3 thêm trường | orchestrator *(spec)* · `DEV` |
| `H2-R1-03` | GHI NHẬN *(`NHE`)* | `:519-524` | M15 sống `46 passed`; bài đề xuất XANH/ĐỎ | thêm bài đứt-giữa-chừng + `--ghi` XANH trên đích tạm | `DEV` |
| `H2-R1-04` | GHI NHẬN | `:164-165` · `:509` · `:513-518` · bài `:242-254` | R1-M17/M18/M19 sống | ca phá `20261116`; bài CLI đòi `②` `④` | `DEV` |
| `H2-R1-05` | GHI NHẬN | `:285-286` · `:413-419` | 147 dòng FLS ⛔ có dòng sổ, `ky` ở 0/147 ⇒ ⛔ vào phán; `_luat` ⛔ nói | khai chiều bỏ ngoài (Đ4); BA chốt chiều ngược khi DT2 có ngày | `DEV` · `BA` |
| `H2-R1-06` | GHI NHẬN | `:229-236` · `so_ly_do_hd1.json:2` | ký `KHAC` được nhận; `ngay` `2099-12-31` được nhận *(K4c)*; `nguoi_ky` tự do | BA: cấm ký `KHAC`; Dev: `ngay` ≤ hôm nay; người ký từ config | `BA` · `DEV` |
| `H2-R1-07` | GHI NHẬN | `:193-213` · BG §Hợp đồng | tệp nhãn 23/122 dòng vẫn hợp lệ *(K4e)* | khai "dòng vắng = chưa có nhãn" hoặc đòi đủ 122 | `DEV` |

## Q3 — R1 đánh giá *(orchestrator hỏi: khoá `van_tay_dong` có nên là NÊN SỬA ngay không)*
**Có — NÊN SỬA, làm ngay khi sổ còn 0 chữ ký** *(`H2-R1-02`)*. Ba lý do đo được: ① K5b chứng minh mù trước đổi chỗ **thật sự xảy ra** với đầu vào hợp lệ *(exit 0)*, ⛔ chỉ lý thuyết; ② DT1b chỉ có **4** nhãn *(ISP `:784`)* nên mỗi chữ ký phủ hàng chục dòng ở nhiều kỳ — xác suất một lượt DT1b chạy lại giữ nguyên tổng mỗi nhãn ⛔ nhỏ; ③ `:225` đòi **đúng** bốn khoá ⇒ thêm khoá thứ năm SAU khi có chữ ký thật là đổi khuôn + làm ĐỎ chữ ký cũ ⇒ **rẻ nhất là bây giờ**. ⛔ CHẶN: hôm nay sổ rỗng, ⛔ có chữ ký nào để mù — nên ⛔ chặn gộp H2; nhưng **chặn chữ ký thật đầu tiên**. Cần orchestrator/BA thêm trường vào ISP Step 4 §3 *(Dev ⛔ tự nới)*.

## Bài thử ĐỀ XUẤT *(⛔ commit — lời giao chỉ cho R1 commit phiếu + sổ; Dev đưa vào `tests/oracle/test_do_voi_hd1.py` nếu nhận khuyến nghị)*
Tệp scratchpad `de_xuat/test_h2_r1_ghi_va_ngay.py` *(chạy với `H2_GOC=<gốc worktree>`)* — **4** bài:

| Bài | Xanh trên `9cf9999` *(bản sao)* | ĐỎ trên |
|---|---|---|
| `test_R1_ghi_XANH_dut_giua_chung_KHONG_lam_cut_hien_vat` — `main()` trong tiến trình, `RA` → `tmp_path`, vá `Path.write_text` ghi nửa chuỗi rồi `OSError`; đòi đích **nguyên byte** | ✅ | **M15** — `1 failed` *(đích cụt)* |
| `test_R1_ghi_XANH_ra_dung_byte_tep_da_commit` — `--ghi` XANH trên đích tạm ⇒ byte = tệp commit, ⛔ sót `.tam` | ✅ | *(đối chứng)* |
| `test_R1_ngay_ky_khuon_co_ban_la_DO[20261116]` · `[2026-W47-1]` | ✅ × 2 | **R1-M19** — `2 failed` |

Tổng: `4 passed` trên mã · `1 failed, 3 passed` trên M15 · `2 failed, 2 passed` trên R1-M19. Bài cho `H2-R1-01` ⛔ viết: mong của nó *(2026-07 VẪN đỏ sau khi ký)* chờ BA chốt spec.

## Câu trong `BG-091` — R1 đối chiếu *(Đ1: grep cả `docs/` lẫn `tools/` + `tests/` + `fls/`)*
| Câu BG | R1 đo | Kết |
|---|---|---|
| `voi_so_luong.json` *"chỉ THÊM khối `dat_hd1`; phần cũ y nguyên byte"* — numstat `217 0` | numstat `217 0`; dict 9 khoá cũ y nguyên giá trị; **14.144/14.146** byte đầu trùng, 2 byte cuối `\n}` đổi thành `,` + khối mới *(⛔ "y nguyên byte" tuyệt đối — nhưng đúng nghĩa: ⛔ giá trị cũ nào đổi)* | ✅ |
| *"`_sha`, `MONG` và mọi khoá cũ giữ nguyên tên + nghĩa"* | `tools/phan_loai_dong_thieu.py:65-66` import `MONG as MONG_VOI` + `_sha`; DT1a R1 chạy exit 0 `KẾT: ĐẠT … 122 + 147`; bài B1 ghim `_sha([1],[2])` + 4 khoá số | ✅ |
| MONG 5 kỳ *"nguồn: AP §5.3.1 '5/23 tháng đủ' + BG-081"* | AP grep `5/23 tháng đủ` = **1**; `BG-081:105` liệt kê đúng 5 kỳ | ✅ *(⚠ BG yếu #6 tự khai: cùng ba ảnh ⇒ độc lập một nửa — R1 đo độc lập lại: khớp)* |
| §Log ĐỎ: `45 failed, 1 passed` trên mã `2664e25` | R1 tái hiện trên bản sao `git archive 2664e25` + bài mới: `45 failed, 1 passed in 3.39s`; 39 × `chưa có phan_hd1` + 6 câu, đúng từng câu | ✅ |
| `46 passed` · hồi quy `155 passed` | R1: `46 passed in 15.40s` · `155 passed in 17.60s` | ✅ |
| `DUONG_NEN.md:88` trích tiền tố `⛔ VOI SỐ LƯỢNG ĐỎ` | grep tiền tố toàn repo: `DUONG_NEN.md:88` · `tools/do_voi_so_luong.py:441` · `BG-091:28` — tiền tố giữ | ✅ |
| `kiem_so_song` ⛔ CHƯA ĐO ĐƯỢC *(`DUONG_NEN.md:432`)* · `khop_owner` `11/16 khop · 5 lech` *(`:434`)* | R1: cùng `FileNotFoundError … Scripts/lint-imports.exe`; `khop_owner` **giống hệt** lượt chạy trên bản sao nền `2664e25` *(diff chỉ khác một `SyntaxWarning` do bản sao ⛔ có `__pycache__`)* | ✅ — ⛔ do H2 |
| *"Công cụ ⛔ mở kết nối PG"* | grep `psycopg` · `connect` · `PG_DSN` trong `tools/do_voi_so_luong.py` = **0** | ✅ |
| §Chứng minh ĐỎ *"15/16 đột biến bị giết, M15 sống"* | R1 chạy lại **M15**: sống `46 passed` ✅; 15 cái còn lại ⛔ chạy lại *(R1 chạy 7 đột biến riêng — §Đột biến)* | ✅ phần đo |
| yếu #8 *"37 dòng `loai_tu_soi` ⛔ góp ô nào"* | đúng; R1 đo thêm cái BG ⛔ đo: **63** ô lệch trong 37 dòng ấy, 36 dòng đã ghép 1-1 ⇒ nâng thành `H2-R1-01` | ✅ + nâng mức |

## Môi trường R1 để lại
- Cụm **5444** để **CHẠY** *(R1 ⛔ dừng)*; kho `fls` `fls_itl = 0 dòng` *(K7)*; `fls_test` do lượt 2 dựng lại.
- Worktree `isp-h2`: R1 chỉ THÊM hai tệp *(phiếu này + sổ)*; sha256 `tools/do_voi_so_luong.py` · `voi_so_luong.json` · `so_ly_do_hd1.json` **= trước khi kiểm** *(so lại sau mọi kịch bản)*. Đột biến chỉ trên bản sao ở scratchpad.
- Bài học cho R2/R3 *(⛔ lỗi H2)*: ⛔ chạy phiên pytest nào khác trên **cùng** cụm khi `--duong-nen` đang chạy — fixture phiên `DROP DATABASE fls_test` ⇒ đỏ giả.
