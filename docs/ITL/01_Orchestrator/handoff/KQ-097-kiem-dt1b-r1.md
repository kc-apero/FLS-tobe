# KQ-097 — biên bản kiểm `BG-096` *(ISP 3.1.2 · Step 5 · DT1b · vòng **R1** — quét TOÀN diff)*

| | |
|---|---|
| **Thuộc** | `BG-096` · `WO-095` *(⛔ có tệp — `DT1b-R1-12`)* |
| **Kiểm bởi** | `fls-test` *(R1, phiên mới, độc lập)* · 2026-11-16 · orchestrator giao |
| **Phạm vi** | `git diff 2664e25 isp/DT1B` — **3** tệp *(`7b340c2`: `tools/phan_loai_ly_do.py` 657 dòng + `tests/du_lieu/test_phan_loai_ly_do.py` 667 dòng · `8a18599`: phiếu `BG-096`)*. Nền `2664e25` ⛔ thuộc phạm vi |
| **Cụm** | reviewer cổng **5437** *(`/home/user/fls-pg16-5437`, có sẵn, `pg_isready` ⇒ `accepting connections`)* — mọi lệnh pytest chạy với `PG_DSN=…:5437/fls` **và** `PG_DSN_TEST=…:5437/fls_test` |
| **Phán quyết** | **`ĐẠT`** vòng R1 — **0 CHẶN** · **5 NÊN SỬA** *(`DT1b-R1-01` · `-02` · `-04` · `-05` · `-06`)* · **7 GHI NHẬN**. Bốn AC ĐẠT **trên phạm vi bước đã chốt** *(bản đọc TỔNG HỢP)*; lượt nhãn THẬT là **⛔ KHÔNG ĐO ĐƯỢC** ở container — giới hạn đã khai *(`B-DATA-2` · O10)*, ⛔ tính là phát hiện. NÊN SỬA ⛔ chặn push *(sổ §1)* — sửa ở vòng kế hoặc orchestrator ghi lý do chấp nhận trước khi đóng `WO` |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1b.md` *(tệp riêng — orchestrator gộp vào sổ chung lúc gộp nhánh)* |

## Cổng vào *(`05` §5)*
- **git:** `isp/DT1B` = `8a18599` *(phiếu)* trên `7b340c2` *(mã + bài)* trên nền `2664e25` — khớp dòng **Commit** của `BG-096`. `git diff --stat 2664e25 isp/DT1B` = **3** tệp, 1.523 dòng thêm, **0** dòng xoá ⇒ ⛔ chạm tool/JSON/bài DT1a, ⛔ refactor. Nhánh cục bộ, ⛔ đẩy — **đúng** O2 = A *(`TIEN_DO.md` §Quy ước "nhánh cục bộ `isp/<bước>` (⛔ push)")*. `git status` sạch trước khi kiểm; HEAD trước = sau lượt `--duong-nen` = `8a18599…`.
- **version spec:** ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 5 · DT1b *(dòng `772`–`853`)*. `WO-095` **⛔ có tệp** *(Đ1: `handoff/` ở `isp/DT1B` · `isp/S0` · `isp/H2` · `isp/base-w2` · checkout chính = 0; `git log --all -- '*WO-095*'` = 0)* ⇒ R1 đối chiếu bốn *"quyết định orchestrator"* `BG-096:12-18` với nguồn ngoài phiếu Dev: ①② `TIEN_DO.md:93` *(checkout chính)* · ③ docstring `isp/H2:tools/do_voi_so_luong.py:37-39` + `_doc_nhan` chạy thật · ④ ⛔ nguồn nào ngoài `BG-096` ⇒ `DT1b-R1-12` *(GHI NHẬN — ⛔ chặn: brief orchestrator giao R1 chính phạm vi này)*.
- **Quyền làn:** 2 tệp mã nằm ở `tests/du_lieu/**` *(làn DATA, ISP `:94`)* + `tools/phan_loai_ly_do.py` *(⛔ có trong bảng `:94`, nhưng orchestrator giao tường minh ở `TIEN_DO.md:93`)*; ⛔ chạm `WO` · `handoff/README.md` · `08_CHANGELOG_RELEASE.md` · dashboard · `TIEN_DO.md` *(đúng `S0-R1-08`)*. ⛔ PII: quét các dòng `+` của diff — chỉ DSN mặc định công khai `fls:fls`, email tổng hợp `ke-toan@vi-du.vn`, mã mẫu `4.36619E+15`/`4366190000000000` đã có sẵn trong repo *(`tests/adapters/test_pm_join.py:58`)*; ⛔ tên người, ⛔ Số CT thật, ⛔ bí mật.

## Cổng chạy lại *(R1 tự chạy ở worktree, venv `/home/user/FLS-tobe/.venv`, `PYTHONUTF8=1`)*
| Lệnh | `BG-096` nói | R1 đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/du_lieu/test_phan_loai_ly_do.py -rA` | exit 0 · `48 passed in 11.14s` | exit 0 · `48 passed in 8.28s` *(48 dòng `PASSED` — 22 hàm `def test_` · `PHA` 24 · `SAI_DINH_DANG` 4 ⇒ 22 − 2 + 28 = 48)* | ✅ |
| `python -m pytest tests/du_lieu` *(hồi quy DT1a)* | `64 passed in 11.44s` | exit 0 · `64 passed in 11.91s` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5437` | lượt 2: `12 failed, 2496 passed, 2 xfailed, 14 errors` · `26 = 26` · web `3 failed, 661 passed` · `3 = 3` · `KẾT: ĐẠT` | exit 0 · DỰNG giữ nguyên cụm/role/kho, `pg_migrate`: `khong co gi de ap` · 7/7 `[ĐẠT]` *(K4 `26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · K6 `HD1 do_voi_so_luong chay 9845 / co 9967` · K7 `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2496 passed, 2 xfailed, 14 errors in 336.76s (0:05:36)` *(mẫu số **2.524** bài)* · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 183.82s (0:03:03)` · `[ĐẠT] … 3 = 3 node id` · **`══ KẾT: ĐẠT — mọi phép kiểm khớp mong`**. Log pytest: 26 dòng `FAILED`/`ERROR`, trong đó `tests/du_lieu` **0** · `wo032_man_cua_that` **0** | ✅ |
| `python tools/phan_loai_ly_do.py` *(cổng của bước)* | exit **3** · `⛔ CHƯA ĐO ĐƯỢC — ⛔ có tệp nhãn …` | exit **3** · cùng câu nguyên văn; `docs/ITL/_tools/` ⛔ có `phan_loai_ly_do.json` *(đếm 0)* | ✅ |
| `lint-imports` | `11 kept, 0 broken` | exit 0 · `Contracts: 11 kept, 0 broken.` *(105 tệp, 349 phụ thuộc)* | ✅ |
| `python tools/do_voi_so_luong.py` *(tiền điều kiện)* | `Σ 9967 9845 3341 2700 30756 22290 112 13 69510/69510` | exit 0 · trùng nguyên dòng `Σ` | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC *(`.venv/Scripts/lint-imports.exe`)* | exit 1 · `FileNotFoundError: … isp-dt1b/.venv/Scripts/lint-imports.exe` — **⛔ KHÔNG ĐO ĐƯỢC** ở container *(đường nền `DUONG_NEN.md:432`)*; ⛔ do bước này | ✅ *(cùng đỏ)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `177 file, 1874 bang, 725 o ngay, 104 ma QD` | exit 0 · trùng *(đo TRƯỚC khi thêm hai tệp của R1 — lượt sau khi thêm: §Môi trường R1 để lại)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech` · đường nền | exit 1 · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` · `B3` `B4` `C5` `C5b` KHONG DO DUOC · `A1` `B1` `C6` DOI TRANG THAI — trùng `DUONG_NEN.md:434` *(kho rỗng)* | ✅ |
| `python tools/soi_bang_tuyen.py` | `40 tuyen` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python tools/kiem_thuyet_minh.py` | `31/31` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` | ✅ |
| `python -m fls.db.pg_migrate` | `khong co gi de ap` · `pg_verify: khop` | exit 0 · trùng | ✅ |
| *(R1 thêm)* **gộp thử**: `git archive isp/base-w3` *(= S0 `fb79f7e` + DT1a vòng sửa `e8b33b3` + H2 `5e63a90`)* + 2 tệp của `7b340c2`, `pytest tests/du_lieu --noconftest` | — | `88 passed in 17.18s` *(**40** DT1a sau vòng sửa — đo riêng `40 passed in 7.28s` — + **48** DT1b)*; JSON DT1a ở `base-w3` giữ hai vân tay `18047e0eb0319ea1` / `6ac2463a190ff631`, `mau_so` y nguyên ⇒ gộp ⛔ vỡ DT1b | ✅ |

## Bảng AC *(= test ID ISP mục 6)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `DT1b-B1` | chạy `--khoa` trên bản đọc ⇒ Σ nhãn = 122; mỗi dòng đúng 1 nhãn; bảng đếm nhãn có MONG | R1 chạy CLI trên bản sao *(`git archive`, công cụ `cmp` = worktree)* với bản đọc tổng hợp sinh bằng chính `_dung(7)`: exit **4** · `① MẪU SỐ: bản đọc phía SO 9.967 dòng sổ · phía L1 10.185 dòng L1 · tập DT1a 122 dòng sổ thiếu · 9.845 dòng ghép (DT1a)` · `② tái lập khoá+seq: 9.845 / 9.845 dòng ghép DT1a = 100,00 %` · `③ … KHONG_CO_SAO_KE 60 · KHOA_LECH 30 · TRUNG_SEQ 20 · KHAC 12` *(Σ 122 dòng)*. Bảng nhãn × kỳ `BG-096:124-144` = bảng R1 đo **18/18 hàng × 6 cột, `diff` 0 dòng**. MONG: `tools/phan_loai_ly_do.py:142-149` *(122 · 9.967 · 9.845 · hai vân tay — mỗi số trỏ nơi ghi)*; `phan_bo_nhan = None` ⇒ mã 4 *(⛔ 0)*; ghim = thiết kế ⇒ exit 0; phân bố khác giữ Σ ⇒ exit 1 *(bài PASSED)*. ⚠ MONG chỉ canh **tổng** — `DT1b-R1-05`. Lượt THẬT: **⛔ KHÔNG ĐO ĐƯỢC** *(giới hạn đã khai)* | **ĐẠT** *(phạm vi tổng hợp)* |
| **AC-2** · `DT1b-B2` | Số CT `4.36619E+15` + tiền `'2,730,128.00'`: chuẩn hoá trước khi băm; khớp bản số thường | Bài B2 ×3 PASSED. R1 đo trực tiếp `chuan_hoa_khoa`: `'2,730,128'` ⇒ `'2730128'` · `'100,000.00'` ⇒ `'100000'`; canon Số CT khoa học = bản đệm 0. Ghép theo KHOÁ ⛔ theo vị trí: hai hạt xáo cùng kết quả *(bài)*. ⚠ bản số thường **mất chữ số** ⛔ được phủ — `DT1b-R1-07`; `'100,000'` ⇒ `'100'` — `DT1b-R1-08` | **ĐẠT** |
| **AC-3** · `DT1b-B3` | quét tệp ra: 0 Số CT thô · 0 Diễn giải | Máy quét **riêng của R1** *(đọc CSV bằng `csv.DictReader`, ⛔ mượn công cụ)* trên tệp ra tổng hợp: mẫu số **11.674** Số CT thô khác nhau + **10.251** số tiền ≥ 6 chữ số khác nhau × **418** token tệp ra ⇒ giao **0** · **0**; `@` **0** · `Did not find` **0**. Tên khoá: 0 khoá chứa `diengiai`/`sochungtu`/`soct`/`email` *(bài, ≥ 732 khoá)*. ⚠ cổng `--tep` ⛔ đóng GIÁ TRỊ — `DT1b-R1-04`; bản đọc khoá thô ⛔ bị chặn khi nằm trong repo — `DT1b-R1-06`; chốt R5/R6/R3 mới chứng minh một vế — `DT1b-R1-02` | **ĐẠT** |
| **AC-4** · `DT1b-B4` | phá: gán 2 nhãn cho 1 dòng *(bản sao)* ⇒ ĐỎ rồi trả nguyên | R1 tự phá CLI *(dòng **9866** — khác dòng 744 của BG)* trên bản sao tệp nhãn tổng hợp: ⓪ nguyên exit **4** → ① `nhan` = `['KHAC', 'TRUNG_SEQ']` ⇒ exit **1** · `dòng 9866 mang 2 nhãn ['KHAC', 'TRUNG_SEQ'] — mỗi dòng ĐÚNG một` → ② trả nguyên exit **4**; sha256-16 tệp trước = sau `218a1f271af48727`. 24 ca `PHA` + vân tay TỪNG tập + mã 3 thiếu đầu vào: PASSED | **ĐẠT** |

## Đối chiếu từng dòng mục 8 *(Exit criteria — ISP `:827`–`:831`)*
| Dòng mục 8 | Bằng chứng | Kết |
|---|---|---|
| DT1b-B1…B4 đúng | Bảng AC trên: 4/4 ĐẠT *(tổng hợp)*; B4 R1 tự thấy đỏ trên dòng khác BG | ✅ |
| 3 vòng review xong | R1 = phiếu này. R2 `KQ-098` · R3 `KQ-099` chưa chạy | ⏳ *(⛔ thuộc R1)* |
| điều kiện PUSH: đủ R1 · R2 · R3, phát hiện chặn = 0 | R1: **0 CHẶN** | ⏳ |
| *(mục 7)* `phan_loai_dong_thieu.json` có `nhan` · bảng nhãn × kỳ dán vào BG | Q2 = A *(tệp nhãn RIÊNG — `TIEN_DO.md:93`)*; bảng trong BG là của bản **tổng hợp**, R1 đo lại khớp 18/18 hàng. Tệp nhãn THẬT ⛔ sinh ở container | ⛔ KHÔNG ĐO ĐƯỢC *(giới hạn đã khai)* |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 5 + `CLAUDE.md` Đ1–Đ5)* | **ĐẠT có ghi chú.** Bảng nhãn đóng đúng ISP `:784`; R1 gọi thẳng `phan_loai` trên khoá tay — **6/6** nhánh ra đúng thiết kế *(§Kịch bản phá S4)* ⇒ mã ĐÚNG, thiếu là **bài**: đột biến biên của R1 bắt **7/29** trước 48 bài, **28/29** khi thêm 17 bài R1 *(§Đột biến)*. Đ3: mẫu số in trước `%`; CSV chỉ tiêu đề ⇒ exit 1 `mẫu số = 0 … {'so_dong_so': 0, 'so_dong_l1': 0}`. **Đ5 — mã 3 `⛔ CHƯA ĐO ĐƯỢC` ĐÚNG luật**: ≠ 0, tách khỏi 1, ⛔ bao giờ in `KẾT: ĐẠT` *(bài subprocess)*; mã 4 *"đo được, chưa ghim"* ≠ 0. Hai vết: bài hồi quy chấp nhận 4 như đạt *(`DT1b-R1-10`)* · thư mục ⇒ 3 *(`-11`)*. Đ1: ba câu phủ định của BG đúng *(§Câu trong BG-096)*; hai câu khẳng định sai *(`BG-096:176` ⇒ `-05` · `:185` ⇒ `-04`)* | §Đột biến · §Kịch bản phá · sổ `SO_PHAT_HIEN_ISP-3.1_DT1b.md` |
| **Dữ liệu** *(⛔ kho thật — công cụ ⛔ mở kết nối; container ⛔ có khoá thật)* | **ĐẠT trên tổng hợp · ⛔ KHÔNG ĐO ĐƯỢC trên dữ liệu thật** *(đã khai)*. Công cụ: grep `psycopg\|fls.db\|fls.repo\|requests\|urllib\|socket\|gspread\|googleapiclient` = **0** dòng; chỉ đọc JSON DT1a + ảnh sổ + bản đọc được trao. ⛔ đếm đôi: 122 `dong_sheet` khác nhau = tập DT1a *(bài + R1 CLI)*; ⛔ mất dòng im lặng: tập SO phải = 9.967 `dong_sheet` liền mạch `10…9976` *(R1 đo ảnh: 9.967 phần tử, liền mạch)* — xuất thiếu ⇒ K11 ĐỎ. Hợp đồng H2: `_doc_nhan` của `isp/H2` đọc tệp nhãn tổng hợp ⇒ `lỗi []` · `122 / 122` · `{KHONG_CO_SAO_KE 60, KHOA_LECH 30, TRUNG_SEQ 20, KHAC 12}`. Cụm 5437 K7 `fls_itl = 0 dòng` | §Cổng chạy lại · §Kịch bản phá S0 · S7 |
| **Màn hình** | **N/A** — ISP §4 *"Frontend: N/A — bước dữ liệu"*; diff ⛔ chạm `fls/web/**` | `git diff --stat 2664e25 isp/DT1B` |

## Đột biến *(R1 tự làm — ⛔ tin "49/50" của BG)*
Bản sao `git archive isp/DT1B` ở scratchpad *(công cụ + bài `cmp` = worktree)*; mỗi đột biến thay **đúng 1** chuỗi *(assert số lần xuất hiện = 1)*, chạy `pytest … --noconftest -x` *(⛔ chạm kho test — cụm 5437 đang chạy `--duong-nen` song song)*, trả nguyên sau mỗi lượt. Đối chứng sau cùng: `48 passed` *(chỉ bài Dev)* · `65 passed, 8 deselected` *(Dev + 17 bài R1; 8 bài `R1_DE_XUAT` bỏ vì ĐỎ sẵn)*. Máy của Dev *(`scratchpad/data_dt1b/dot_bien.py`, R1 đọc)* gồm 50 đột biến **xoá phép** *(`pass` · `if False` · `lambda *a: None`)* — đúng cho thứ nó đo; máy R1 dùng đột biến **biên / nhánh con** *(`<` → chia toàn nhóm, `min` → `max`, đảo thứ tự, bỏ một từ cấm, bỏ một dạng token)*.

| Mã | Đột biến *(`tools/phan_loai_ly_do.py`)* | 48 bài Dev | + 17 bài R1 |
|---|---|:-:|:-:|
| D01 | KHOP/TRUNG_SEQ tất-cả-hoặc-không: `if u[k].index(d) < cho` → `if cho > 0` | SỐNG | BẮT ① |
| D02 | thứ tự seq trong nhóm khoá đảo *(`sorted(thieu, reverse=True)`)* | SỐNG | BẮT ① |
| D03 | chỗ trống trừ `n_so` thay `o` | BẮT | BẮT |
| D04 | `mo_coi`: `n > o` thay `n > n_so` *(dòng L1 do dòng KHOP giữ thành ứng viên)* | SỐNG | BẮT ② |
| D05 · D06 | bỏ chốt `if k[0]` ở phía tra · phía dựng *(riêng từng cái: **tương đương**)* | SỐNG · SỐNG | SỐNG · SỐNG |
| D0506 | D05 + D06 cùng lúc | SỐNG | BẮT ④ |
| D07 | ứng viên `max` thay `min` | SỐNG | BẮT ③ |
| D08 | hoà theo thứ tự `set` *(bỏ khoá phụ `c`)* | SỐNG | BẮT ③ *(6/6 `PYTHONHASHSEED` 0–5)* |
| D09 · D10 | `theo_bon` bỏ tiền tệ *(dựng · tra)* | BẮT · BẮT | BẮT · BẮT |
| D11 | `n_l1` đếm cả khoá hỏng | SỐNG | BẮT ④ |
| D12 | `o` đếm cả khoá hỏng *(**tương đương**: `o` chỉ đọc ở khoá ⛔ hỏng; tái lập `min(o, n_l1)` mà `n_l1` bỏ khoá hỏng ⇒ 0)* | SỐNG | SỐNG |
| D13 · D14 | TK ⛔ chữ hoa · ⛔ gỡ trắng | SỐNG · SỐNG | BẮT ⑥ · BẮT ⑥ |
| D15 | `_hong` chỉ xét PS Nợ | SỐNG | BẮT ⑤ |
| D16 | tiền bỏ `.normalize()` *(**tương đương**: `parse_so` trả `int` khi nguyên; `str(float)` đã ngắn nhất)* | SỐNG | SỐNG |
| D17 | R5 bỏ nửa TIỀN *(`cam_tien.add` → `pass`)* | SỐNG | BẮT ⑦ |
| D18 · D19 | R5 bỏ dạng chuẩn hoá · bỏ dạng thô của Số CT | SỐNG · SỐNG | BẮT ⑦ · BẮT ⑦ |
| D20 · D21 | R6 bỏ `sochungtu` · bỏ `email` | SỐNG · SỐNG | BẮT ⑧ · BẮT ⑧ |
| D22 | R3 ⛔ quét TÊN khoá | SỐNG | BẮT ⑧ |
| D23 · D24 | hàng trắng ⛔ bỏ qua · cột LẶP ⛔ chặn | SỐNG · SỐNG | BẮT ⑨ · BẮT ⑩ |
| D25 | M so phân bố bằng TỔNG | BẮT | BẮT |
| D26 | tái lập đếm trên `n_so` | BẮT | BẮT |
| D27 | `_ghi` bỏ kiểm đọc lại | SỐNG | SỐNG *(phòng thủ chồng — cần khai)* |
| D28 | `_ghi` ghi thẳng lên đích *(`tam = RA`)* | SỐNG | BẮT ⑪ |
| D29 | K11 bỏ | BẮT | BẮT |
| D30 · D31 | lược đồ `nguon` · `mau_so` ⛔ đóng | SỐNG · SỐNG | BẮT ⑫ · BẮT ⑫ |
| D32 | R2 `khoa_bam` chỉ cần là chuỗi | BẮT | BẮT |

**Tổng:** 33 đột biến · **4** tương đương *(D05 · D06 · D12 · D16)* ⇒ mẫu số **29**. 48 bài Dev: **BẮT 7 / 29 = 24,1 %** *(D03 · D09 · D10 · D25 · D26 · D29 · D32)*. Thêm 17 bài R1: **BẮT 28 / 29 = 96,6 %** — sống đúng **D27**. ⚠ Lượt đầu máy R1 lọc `-k "not DE_XUAT"` khớp **tên tệp** `test_kq097_de_xuat` *(so khớp ⛔ phân biệt hoa thường)* ⇒ bỏ cả 25 bài R1 *(`48 passed, 25 deselected`)* — lượt ấy chính là phép đo *"chỉ 48 bài Dev"* cho D0506; lượt tính số dùng `-k "not R1_DE_XUAT"` *(`… passed, 8 deselected`)*.

## Kịch bản phá *(R1 — bản sao, ⛔ ghi worktree, ⛔ kho)*
| # | Kịch bản | Mong | Đo | Kết |
|---|---|---|---|---|
| S0 | đối chứng: `--khoa` tổng hợp `--ghi`, MONG phân bố ghim = thiết kế | 0 | exit **0** · `KẾT: ĐẠT …`; cổng `--tep` trên bản sao nguyên exit **0** | ✅ |
| S1 | đổi chỗ *(`nhan`, `lech`, `ghi_chu`)* dòng 8826 `KHOA_LECH` ↔ dòng 8859 `TRUNG_SEQ`, cùng kỳ `2026-07` | ĐỎ | exit **0** `KẾT: ĐẠT` | ⛔ ⇒ `DT1b-R1-05` |
| S2 | Số CT 16 chữ số / câu kiểu Diễn giải *(tổng hợp)* cấy vào 7 lá: `nguon.ban_doc_sha256_16` · `nguon.anh_so` · `_vi_sao` · `khong_mang_PII` · `mau_so.khoa_hong.SO` · `mau_so.dang_khoa_hoc.L1` · khoá `FT25123456789` | ĐỎ × 7 | exit **0** × **7/7** | ⛔ ⇒ `DT1b-R1-04` |
| S3a | `canon_ref('4366191234567890')` ↔ `canon_ref('4.36619E+15')` | — | `'4366191234567890'` ≠ `'4366190000000000'` ⇒ **KHÁC khoá**; bộ dựng: `1007440000000000` ↔ `1.00744E+15` ⇒ canon trùng *(⛔ mất chữ số)* | ⇒ `DT1b-R1-07` |
| S3b | tiền: `'100,000'` · `'100,000.00'` · `'2,730,128'` · `'1,000'` · `'2.730.128'` · `'2.730.128,00'` · `'1234,5'` | — | `'100'` · `'100000'` · `'2730128'` · `'1'` · `'2730128'` · `None` · `'1234.5'` | ⇒ `DT1b-R1-08` |
| S4 | `phan_loai` trên khoá tay: ① 4 dòng sổ cùng khoá *(1 ghép · 3 thiếu)* × 3 L1 ② dòng L1 do KHOP giữ ③ hoà 2 ứng viên ④ Số CT rỗng ⑤ L1 khoá hỏng ⑥ ô lỗi PS Có | thiết kế | ① `{2: KHOP, 3: KHOP, 4: TRUNG_SEQ}`, tái lập 1 ② dòng 12 `KHONG_CO_SAO_KE` ③ `lech ['tk']` ④ ⑤ `KHONG_CO_SAO_KE` ⑥ `KHAC KHOA_HONG:ps_co` — **6/6 đúng** | ✅ *(mã đúng — thiếu bài: `-01`)* |
| S5 | bản đọc khoá ở `docs/ITL/_tools/dt1b_khoa.csv` *(trong repo, ⛔ bị gitignore)* | TỪ CHỐI | exit **0** `KẾT: ĐẠT` | ⛔ ⇒ `DT1b-R1-06` |
| S6 | dò ngược `khoa_bam` `5e5d88384696cee0` của dòng Số CT rỗng *(tổng hợp)* | — | ra tiền **4.250.000** sau **0,01 s**; tốc độ **≈ 371.050 phép băm/s** *(2.000.001 phép / 5,39 s, Python một luồng)* | ⇒ `DT1b-R1-09` |
| S7 | `_doc_nhan` của `isp/H2` đọc tệp nhãn S0 | lỗi `[]` · 122/122 | `lỗi H2: [] · đọc được 122 / 122` · phân bố `60 · 30 · 20 · 12` | ✅ |
| S8 | CLI biên: `--khoa <thư mục>` · `--tep <thư mục>` · CSV rỗng 0 byte · CSV chỉ tiêu đề · CSV phân cách `;` · JSON rỗng · JSON `{}` · `--tep` trỏ JSON DT1a | — | **3** · **3** · 1 `bản đọc rỗng` · 1 `mẫu số = 0` · 1 `cột … thừa ['bang;dong;…']` · 1 `JSONDecodeError` · 1 `khoá ngoài lược đồ` · 1 `khoá ngoài lược đồ` — mọi dòng lỗi **một dòng**, ⛔ giá trị ô | ✅ *(thư mục ⇒ 3: `-11`)* |

## Phát hiện *(chi tiết đầy đủ + luật phòng tái phạm: `SO_PHAT_HIEN_ISP-3.1_DT1b.md`)*
| Mã | Lớp | Mức *(↔ `10` §3.4)* | Nơi | Tái hiện | Khuyến nghị | Gửi |
|---|---|---|---|---|---|---|
| `DT1b-R1-01` | B1 | **NÊN SỬA** *(`NANG`)* | `tools/phan_loai_ly_do.py:279-312` · bài `:151-181` | 10 đột biến lõi ghép SỐNG trước 48 bài *(D01 D02 D04 D0506 D07 D08 D11 D13 D14 D15)* | 6 bài đơn vị gọi thẳng `phan_loai` *(§Bài thử đề xuất ①–⑥)* | `DEV` |
| `DT1b-R1-02` | B1 | **NÊN SỬA** *(`NANG`)* | `:261-266` · `:155` · `:444-449` · docstring `:83-89` | D17–D22 SỐNG *(R5 tiền · R5 thô/chuẩn hoá · R6 `sochungtu`/`email` · R3 tên khoá)* | bài R5 × 3 qua đường đo thật + 3 ca `PHA` *(⑦ ⑧)* | `DEV` |
| `DT1b-R1-03` | B1 | GHI NHẬN *(`NHE`)* | `:244-245` · `:239` · `:419-420` · `:591-597` | D23 D24 D28 D30 D31 SỐNG · D27 SỐNG | 5 bài *(⑨–⑫)*; khai D27 phòng thủ chồng | `DEV` |
| `DT1b-R1-04` | A2 | **NÊN SỬA** *(`NANG`)* | `:403-425` · `:428-521` · docstring `:34-35` · `BG-096:185` | §Kịch bản phá S2: 7/7 lá tự do ⇒ exit 0 | so hằng / mẫu cho từng lá; câu lỗi ⛔ in giá trị *(⑬ — ĐỎ hôm nay)* | `DEV` |
| `DT1b-R1-05` | A2 | **NÊN SỬA** *(`NANG`)* | `:142-149` · `:573-588` · `BG-096:176` | §S1: đổi nhãn 2 dòng cùng kỳ ⇒ exit 0 | `MONG["van_tay_nhan"]` + K13; sửa câu `BG-096:176` *(⑭ — ĐỎ hôm nay)* | `DEV` |
| `DT1b-R1-06` | A1 | **NÊN SỬA** *(`NANG`)* | `:604-610` · `.gitignore:17` | §S5: CSV khoá thô trong `docs/ITL/_tools/` ⇒ exit 0 | từ chối đường dẫn trong repo ⛔ bị gitignore, mã 2 + bài `git init` ở `tmp_path` | `DEV` |
| `DT1b-R1-07` | B1 | GHI NHẬN | bài `:138-141` · `:173-177` · `:353-357` · `BG-096:160` · `:170` | §S3a | chẩn đoán *"khớp nếu cắt 6 chữ số"* ở dòng ② + ca tổng hợp mất chữ số; orchestrator trả nghĩa *"bản số thường"* *(ISP `:814`)* | `DEV` · orchestrator |
| `DT1b-R1-08` | B1 | GHI NHẬN | `:182-190` *(→ `parse_so`)* · `BG-096:160` | §S3b | hướng dẫn owner `#,##0.00` cả hai bảng; đếm ô tiền mơ hồ `^\d{1,3},\d{3}$` ở dòng ② | `DEV` |
| `DT1b-R1-09` | B2 | GHI NHẬN | ISP `:788` · `:205-208` · `BG-096:184` | §S6 | orchestrator chọn HMAC khoá owner giữ · bỏ `khoa_bam` *(0 người đọc)* · hoặc ghi rõ tiền/TK ⛔ bí mật | orchestrator · `BA` |
| `DT1b-R1-10` | B1 | GHI NHẬN | bài `:605-612` | đọc mã: tệp thật có ⇒ chấp nhận mã 4 | có tệp mà chưa ghim ⇒ `pytest.fail` *(⛔ `xfail`)* | `DEV` |
| `DT1b-R1-11` | A1 | GHI NHẬN | `:605-608` · `:623-626` | §S8: thư mục ⇒ 3 | có mà ⛔ phải tệp ⇒ 2; câu mã 3 in đường dẫn tuyệt đối | `DEV` |
| `DT1b-R1-12` | B2 | GHI NHẬN | `handoff/` *(⛔ `WO-095`)* · ISP `:94` `:788` `:824` `:836` | Đ1: 0 tệp, 0 commit | orchestrator ghi `WO-095` *(4 quyết định)* trước R2; vá ISP theo `DT1a-R1-08` | orchestrator |

**Theo mức:** CHẶN **0** · NÊN SỬA **5** · GHI NHẬN **7**. **Theo lớp** *(thang brief)*: A1 **2** · A2 **2** · B1 **6** · B2 **2**.

## Bài thử ĐỀ XUẤT *(⛔ commit — orchestrator chỉ cho R1 commit phiếu + sổ; Dev đưa vào `tests/du_lieu/` nếu nhận khuyến nghị)*
Một tệp `tests/du_lieu/test_kq097_de_xuat.py` *(văn bản trọn ở §Phụ lục)*, chạy trên bản sao `git archive isp/DT1B` với `--noconftest`. Trên `7b340c2`: **`8 failed, 17 passed in 2.51s`** — 17 bài giết đột biến XANH, 8 bài phát hiện ĐỎ *(đúng mong)*.

| # | Bài | Đã chứng minh ĐỎ bằng | Trên `7b340c2` |
|---|---|---|---|
| ① | `test_R1_seq_MOT_PHAN_dong_thieu_dau_KHOP_dong_sau_TRUNG_SEQ` | D01 · D02 | XANH |
| ② | `test_R1_dong_L1_do_dong_KHOP_giu_cho_KHONG_la_ung_vien` | D04 | XANH |
| ③ | `test_R1_ung_vien_IT_LECH_nhat_va_HOA_theo_khoa_nho_nhat` | D07 · D08 *(6/6 hạt băm)* | XANH |
| ④ | `test_R1_so_ct_RONG_va_khoa_HONG_khong_la_cau_ung_vien` | D0506 · D11 | XANH |
| ⑤ | `test_R1_o_loi_PS_CO_la_KHOA_HONG_ps_co` | D15 | XANH |
| ⑥ | `test_R1_TK_go_trang_va_chu_hoa` | D13 · D14 | XANH |
| ⑦ | `test_R1_R5_moi_dang_bi_chan_tren_duong_do_that[tien · so_ct_khoa_hoc_THO · so_ct_CHUAN_HOA]` | D17 · D19 · D18 | XANH × 3 |
| ⑧ | `test_R1_bat_bien_tep_nhan_CAN_tren_ban_sao[khoa_cam_So_chung_tu · khoa_cam_Email · email_o_TEN_khoa]` | D20 · D21 · D22 | XANH × 3 |
| ⑨ | `test_R1_hang_TRANG_kieu_Excel_duoc_bo_qua` | D23 | XANH |
| ⑩ | `test_R1_cot_LAP_la_DO` | D24 | XANH |
| ⑪ | `test_R1_ghi_qua_TEP_TAM_hong_luc_thay_thi_dich_NGUYEN` | D28 | XANH |
| ⑫ | `test_R1_bat_bien_tep_nhan_CAN_tren_ban_sao[nguon_thua · mau_so_thua]` | D30 · D31 | XANH × 2 |
| ⑬ | `test_R1_DE_XUAT_la_chuoi_TU_DO_bi_chan[× 7]` | **chính `7b340c2`** *(phát hiện `-04`)* | **ĐỎ × 7** — phải XANH sau sửa |
| ⑭ | `test_R1_DE_XUAT_doi_nhan_HAI_dong_cung_ky_la_DO` | **chính `7b340c2`** *(phát hiện `-05`)* | **ĐỎ** — sau sửa cần `monkeypatch` `MONG["van_tay_nhan"]` của bản tổng hợp như `phan_bo_nhan` |

## Câu trong `BG-096` — R1 đối chiếu
| `BG-096` | R1 đo | Kết |
|---|---|---|
| `:18` Đ1 *"grep `phan_loai_dong_thieu` trong công cụ: 7 dòng = 5 chú thích/docstring + 2 đường dẫn JSON · 0 `import`"* | 7 dòng *(`:6` `:13` `:33` `:153` `:216` chú thích · `:128` `:359` đường dẫn)* · 0 dòng `import` | đúng |
| `:33` Đ1 *"ba nhãn … 11 dòng ở 3 tệp ngoài hai tệp mới … 0 dòng mang một con số phân bố"* | ISP 3.1.1 **5** · ISP 3.1.2 **3** · `sinh_isp_voi.py` **3** = 11 dòng / 3 tệp; ⛔ dòng nào kèm số đếm nhãn | đúng |
| `:34` *"mã ghép tạo ra 9.845 ⛔ có trong repo"* | grep `classifying_vs_canon` ở `tools/` `fls/` `tests/` `docs/` *(.py)*: 8 tệp đọc, **0** dòng `write`/`dump` ghi nó | đúng |
| `:59` *"48 bài (22 hàm …)"* · `:65`–`:68` lượt cổng | 22 · 24 · 4 · 48; cổng: §Cổng chạy lại | đúng |
| `:101`–`:102` *"đột biến … 49/50 bắt"* | đúng với máy của Dev *(đột biến xoá phép)*; máy R1 *(đột biến biên)*: 7/29 | đúng phạm vi, **thiếu phủ** ⇒ `-01` `-02` `-03` |
| `:121` đối chiếu H2 *"lỗi H2: [] · 122 / 122"* | R1 làm lại độc lập *(S7)*: `lỗi H2: [] · 122 / 122` | đúng |
| `:124`–`:146` bảng nhãn × kỳ + dòng `KHAC`/`KHOA_LECH` + mẫu số | 18/18 hàng `diff` 0; `KHOA_HONG:ps_no 2 · KHOP_KHI_GHEP_LAI 10 ‖ ps_no 15 · so_ct 15`; `Số CT dạng khoa học: sổ 0 · L1 1.417` | đúng |
| `:176` *"từ đó cổng trả 0, và **mọi** thay đổi nhãn về sau … đều ĐỎ"* | S1: đổi nhãn 2 dòng cùng kỳ ⇒ exit 0 | **sai** ⇒ `-05` |
| `:185` yếu #7 *"đường duy nhất đưa chuỗi tự do vào là trường `ky`"* | S2: 7 lá tự do qua cổng `--tep` | **sai ở chế độ CỔNG** ⇒ `-04` |
| `:184` yếu #6 băm ≠ ẩn danh | S6 đo được giá: 0,01 s cho dòng Số CT rỗng | đúng, **đã định lượng** ⇒ `-09` |
| `:186` yếu #8 `_van_tay` chép 1 dòng | vân tay tính bằng công cụ = DT1a = H2 *(`18047e0eb0319ea1` · `6ac2463a190ff631`, cả ở `isp/base-w3`)* | đúng, rủi ro thấp |

## Q1–Q4 của `BG-096` *(R1 chỉ góp ý — quyết là của orchestrator)*
- **Q1** *(tái lập < 9.845)*: đồng ý ⓐ, **kèm** chẩn đoán `DT1b-R1-07` để một lượt màn ①–④ đủ phân biệt *"mất chữ số khoa học"* với *"L1 đổi sau 26/08"*.
- **Q2** *(ai ghim)*: đồng ý ⓐ, và **cùng WO** ghim `van_tay_nhan` *(`DT1b-R1-05`)* — ghim phân bố một mình ⛔ giữ được lời hứa `BG-096:176`.
- **Q3** *(`CAM_MO` ↔ O10)*: R1 ⛔ có thêm bằng chứng; ghi nhận mâu thuẫn chữ còn mở.
- **Q4** *(K13 Số CT khoa học phía SO = 0)*: đồng ý ⓐ — rẻ, biến lời dặn thành cổng *(cùng tinh thần `DT1b-R1-06`)*.

## Môi trường R1 để lại
Cụm `5437` **đang chạy** *(⛔ dừng)*. Worktree: chỉ thêm `KQ-097` + `SO_PHAT_HIEN_ISP-3.1_DT1b.md`. `kiem_tai_lieu.py` SAU khi thêm hai tệp: exit 0 · `✅ cong tai lieu DAT … (179 file, 1885 bang, 727 o ngay, 104 ma QD)` *(+2 tệp · +11 bảng · +2 ô ngày so với lượt trước)*. Theo brief orchestrator *(chỉ thêm phiếu + sổ riêng)* — **⛔ chạm** `docs/ITL/04_Test/03_TRACEABILITY_GAP_REPORT.md` · `handoff/README.md` · dashboard §5 · `TIEN_DO.md`: orchestrator gom lúc gộp *(`TIEN_DO.md` §Quy ước — dashboard §5 do orchestrator ghi)*; truy vết spec → bài của bước: `DT1b-B1` → 6 bài B1 · `DT1b-B2` → 3 · `DT1b-B3` → 3 · `DT1b-B4` → 35 *(tên ở `BG-096:82-85`, R1 đếm lại khớp)*. Kịch bản đo ở scratchpad phiên *(⛔ trong repo)* `scratchpad/r1_dt1b/`: `dot_bien.py` · `dot_bien2.py` · `kich_ban_pha.py` · `test_kq097_de_xuat.py` · log `dot_bien_luot1.log` · `dot_bien_luot2_co_de_xuat.log` · `kich_ban_pha.log` · `duong_nen.log` · bản sao `ban/` · `gop/`.

## Phụ lục — `tests/du_lieu/test_kq097_de_xuat.py` *(bài đề xuất, nguyên văn)*
```python
# -*- coding: utf-8 -*-
"""R1 `KQ-097` — bài ĐỀ XUẤT cho DT1b (⛔ commit: Dev đưa vào `tests/du_lieu/` nếu nhận khuyến nghị).

Hai nhóm:
  · `test_R1_*`        — XANH trên `7b340c2`, ĐỎ trên đột biến R1 đã chỉ (mỗi bài ghi đột biến nó giết).
  · `test_R1_DE_XUAT_*` — ĐỎ trên `7b340c2` (chính là phát hiện), XANH sau khi sửa theo khuyến nghị.
Chạy: đặt tệp vào `tests/du_lieu/` của bản sao, `pytest tests/du_lieu/test_kq097_de_xuat.py --noconftest`.
"""
from __future__ import annotations

import json

import pytest

from tests.du_lieu import test_phan_loai_ly_do as g


def _t():
    return g._tool()


MONG = dict(g.MONG_TONG_HOP)


# ═══ DT1b-R1-01 · lõi ghép theo NHÓM KHOÁ — nhánh bộ dựng `_dung` ⛔ chạm ════════════════════════
def test_R1_seq_MOT_PHAN_dong_thieu_dau_KHOP_dong_sau_TRUNG_SEQ():
    """Giết D01 (tất-cả-hoặc-không) · D02 (đảo thứ tự seq). Bộ dựng chỉ có nhóm 1 dòng thiếu."""
    K = ("A1", "100", "0", "1121", "VND")
    nh, tl = _t().phan_loai({1: K, 2: K, 3: K, 4: K}, {101: K, 102: K, 103: K}, [4, 2, 3])
    assert {d: (v["nhan"], v["ghi_chu"]) for d, v in nh.items()} == {
        2: ("KHAC", "KHOP_KHI_GHEP_LAI"), 3: ("KHAC", "KHOP_KHI_GHEP_LAI"), 4: ("TRUNG_SEQ", None)}
    assert tl == 1


def test_R1_dong_L1_do_dong_KHOP_giu_cho_KHONG_la_ung_vien():
    """Giết D04 (dòng L1 'chưa ai ghép' trừ dòng ĐÃ ghép thay vì mọi dòng sổ)."""
    KX, KY = ("B1", "100", "0", "1121", "VND"), ("B1", "200", "0", "1121", "VND")
    nh, _ = _t().phan_loai({11: KX, 12: KY}, {201: KX}, [11, 12])
    assert (nh[11]["nhan"], nh[11]["ghi_chu"]) == ("KHAC", "KHOP_KHI_GHEP_LAI")
    assert (nh[12]["nhan"], nh[12]["lech"]) == ("KHONG_CO_SAO_KE", [])


def test_R1_ung_vien_IT_LECH_nhat_va_HOA_theo_khoa_nho_nhat():
    """Giết D07 (max thay min) · D08 (hoà theo thứ tự set — đổi theo PYTHONHASHSEED; 12 dòng ⇒ 2⁻¹² lọt)."""
    so, l1, thieu = {}, {}, []
    for i in range(12):
        ct = f"C{i:02d}"
        so[i] = (ct, "500", "0", "1121", "VND")
        thieu.append(i)
        l1[1000 + 3 * i] = (ct, "501", "0", "1121", "VND")      # lệch ps_no
        l1[1001 + 3 * i] = (ct, "500", "0", "1122", "VND")      # lệch tk — hoà, khoá nhỏ hơn ('500' < '501')
        l1[1002 + 3 * i] = (ct, "999", "7", "9999", "USD")      # lệch 4 trường
    nh, _ = _t().phan_loai(so, l1, thieu)
    assert {d: v["lech"] for d, v in nh.items()} == {i: ["tk"] for i in range(12)}


def test_R1_so_ct_RONG_va_khoa_HONG_khong_la_cau_ung_vien():
    """Giết D05+D06 (cùng lúc — riêng từng cái là đột biến TƯƠNG ĐƯƠNG) · D11 (L1 đếm cả khoá hỏng)."""
    nh, _ = _t().phan_loai({31: ("", "300", "0", "1121", "VND"), 41: ("D1", "600", "0", "1121", "VND")},
                           {401: ("", "999", "0", "1121", "VND"), 501: ("D1", None, "0", "1121", "VND")},
                           [31, 41])
    assert nh[31]["nhan"] == nh[41]["nhan"] == "KHONG_CO_SAO_KE"


def test_R1_o_loi_PS_CO_la_KHOA_HONG_ps_co():
    """Giết D15 (KHOA_HONG chỉ xét PS Nợ) — bộ dựng chỉ có ô lỗi ở PS Nợ."""
    t = _t()
    nh, _ = t.phan_loai({51: t.chuan_hoa_khoa("E1", "", "#N/A", "1121", "VND")}, {}, [51])
    assert (nh[51]["nhan"], nh[51]["ghi_chu"]) == ("KHAC", "KHOA_HONG:ps_co")


def test_R1_TK_go_trang_va_chu_hoa():
    """Giết D13 · D14 — bộ dựng chỉ có TK 4 chữ số, ⛔ trắng, ⛔ chữ."""
    t = _t()
    assert t.chuan_hoa_khoa("X1", "1", "", " 1121a ", "VND") == t.chuan_hoa_khoa("X1", "1", "", "1121A", "VND")


# ═══ DT1b-R1-02 · R5 / R6 / R3 — mỗi vế một ca phá RIÊNG (luật `DT1a-R1-03`) ═════════════════════
def _dt1a_ky(tmp_path, gia_tri):
    d = json.loads(g.DT1A.read_text(encoding="utf-8"))
    dau = g._nen()[1][0]
    vt = [j for j, x in enumerate(d["dong_thieu"]) if x["dong_sheet"] == dau]
    assert len(vt) == 1
    d["dong_thieu"][vt[0]]["ky"] = gia_tri
    p = tmp_path / "dt1a_ban.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return p


@pytest.mark.parametrize("ten", ["tien", "so_ct_khoa_hoc_THO", "so_ct_CHUAN_HOA"])
def test_R1_R5_moi_dang_bi_chan_tren_duong_do_that(tmp_path, monkeypatch, capsys, ten):
    """Giết D17 (bỏ nửa TIỀN) · D19 (bỏ dạng THÔ) · D18 (bỏ dạng CHUẨN HOÁ)."""
    van_ban, _, tin = g._dung(7)
    if ten == "tien":
        ban, cau = sorted(tin["tien"])[0], "riêng tư: số tiền"
    elif ten == "so_ct_khoa_hoc_THO":
        ban, cau = sorted(c for c in tin["so_ct_tho"] if "E+" in c)[0], "riêng tư: Số chứng từ"
    else:   # Số CT thô KHÁC dạng chuẩn hoá (thường + gạch + trắng) ở dòng thiếu đầu; cấy dạng CHUẨN HOÁ
        dau = g._nen()[1][0]
        hang = van_ban.splitlines()
        i = next(j for j, x in enumerate(hang) if x.startswith(f"SO,{dau},"))
        cot = hang[i].split(",")
        cot[2] = "syn-x 12345"
        hang[i] = ",".join(cot)
        van_ban = "\n".join(hang) + "\n"
        ban, cau = "SYNX12345", "riêng tư: Số chứng từ"
    p = g._ghi_csv(tmp_path, van_ban)
    ra = tmp_path / "ra.json"
    ma, out, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra,
                                 dt1a=_dt1a_ky(tmp_path, ban), mong_nhan=dict(MONG))
    assert ma == 1, (ten, out)
    assert cau in err, err
    assert not ra.exists()


PHA_R1 = [
    ("nguon_thua", lambda d: d["nguon"].update(them="x"), "khoá ngoài lược đồ ở nguon"),          # giết D30
    ("mau_so_thua", lambda d: d["mau_so"].update(them=1), "khoá ngoài lược đồ ở mau_so"),        # giết D31
    ("khoa_cam_So_chung_tu", lambda d: d["mau_so"]["khoa_hong"].update({"Số chứng từ": 1}), "riêng tư: khoá cấm"),  # D20
    ("khoa_cam_Email", lambda d: d["mau_so"]["khoa_hong"].update({"Email": 1}), "riêng tư: khoá cấm"),            # D21
    ("email_o_TEN_khoa", lambda d: d["mau_so"]["khoa_hong"].update({"ke-toan@vi-du.vn": 1}), "riêng tư: email"),  # D22
]


@pytest.mark.parametrize("ten, pha, cau", PHA_R1, ids=[p[0] for p in PHA_R1])
def test_R1_bat_bien_tep_nhan_CAN_tren_ban_sao(tmp_path, monkeypatch, capsys, ten, pha, cau):
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    sao = tmp_path / "ban_sao.json"
    sao.write_text(goc, encoding="utf-8")
    assert g._kiem_tep(monkeypatch, capsys, sao, tmp_path)[0] == 0
    d = json.loads(goc)
    pha(d)
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, (ten, out)
    assert cau in err, err


# ═══ DT1b-R1-03 · đọc bản đọc · ghi hiện vật ════════════════════════════════════════════════════
def test_R1_hang_TRANG_kieu_Excel_duoc_bo_qua(tmp_path, monkeypatch, capsys):
    """Giết D23. Excel hay xuất hàng chỉ có dấu phẩy ở cuối vùng đã chạm."""
    van_ban, _, _ = g._dung(7)
    p = g._ghi_csv(tmp_path, van_ban + ",,,,,,\n,,,,,,\n")
    ma, _, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p), ra=tmp_path / "ra.json", mong_nhan=dict(MONG))
    assert ma == 0, err


def test_R1_cot_LAP_la_DO(tmp_path, monkeypatch, capsys):
    """Giết D24 — cột `tk` lặp: bản đầu dùng ÂM THẦM cột đầu."""
    van_ban, _, _ = g._dung(7)
    h = van_ban.splitlines()
    p = g._ghi_csv(tmp_path, "\n".join([h[0] + ",tk"] + [x + ",9999" for x in h[1:]]) + "\n")
    ra = tmp_path / "ra.json"
    ma, _, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, mong_nhan=dict(MONG))
    assert ma == 1 and "lặp ['tk']" in err, err
    assert not ra.exists()


def test_R1_ghi_qua_TEP_TAM_hong_luc_thay_thi_dich_NGUYEN(tmp_path, monkeypatch, capsys):
    """Giết D28 (ghi thẳng lên đích) — luật `DT1a-R1-07` có bài canh."""
    t = _t()
    van_ban, _, _ = g._dung(7)
    p = g._ghi_csv(tmp_path, van_ban)
    ra = tmp_path / "phan_loai_ly_do.json"
    ra.write_text("BAN CU", encoding="utf-8")

    def hong(*a, **k):
        raise OSError("mô phỏng hỏng lúc thay tệp")

    monkeypatch.setattr(t.os, "replace", hong)
    with pytest.raises(OSError):
        g._chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, mong_nhan=dict(MONG))
    assert ra.read_text(encoding="utf-8") == "BAN CU"


# ═══ PHÁT HIỆN — ĐỎ trên 7b340c2 (bài mong hành vi SAU khi sửa) ═══════════════════════════════════
SO_CT = "4366191234567890"
DG = "Chuyen tien cho Nguyen Van A theo HD 123"
TU_DO = [
    ("nguon_ban_doc_sha_la_SoCT", lambda d: d["nguon"].update(ban_doc_sha256_16=SO_CT)),
    ("nguon_anh_so_la_DienGiai", lambda d: d["nguon"].update(anh_so=DG)),
    ("vi_sao_mang_DienGiai", lambda d: d.update(_vi_sao=d["_vi_sao"] + " " + DG)),
    ("khong_mang_PII_la_SoCT", lambda d: d.update(khong_mang_PII=SO_CT)),
    ("khoa_hong_gia_tri_SoCT", lambda d: d["mau_so"]["khoa_hong"].update(SO=SO_CT)),
    ("dang_khoa_hoc_gia_tri_DienGiai", lambda d: d["mau_so"]["dang_khoa_hoc"].update(L1=DG)),
    ("dang_khoa_hoc_khoa_la", lambda d: d["mau_so"]["dang_khoa_hoc"].update({"FT25123456789": 1})),
]


@pytest.mark.parametrize("ten, pha", TU_DO, ids=[x[0] for x in TU_DO])
def test_R1_DE_XUAT_la_chuoi_TU_DO_bi_chan(tmp_path, monkeypatch, capsys, ten, pha):
    """DT1b-R1-04 — mọi lá chuỗi của tệp nhãn phải = hằng / ∈ tập đóng / khớp mẫu (hex16 · kỳ DT1a · số)."""
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    d = json.loads(goc)
    pha(d)
    sao = tmp_path / "ban_sao.json"
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, (ten, out)


def test_R1_DE_XUAT_doi_nhan_HAI_dong_cung_ky_la_DO(tmp_path, monkeypatch, capsys):
    """DT1b-R1-05 — tổng y nguyên, bảng kỳ y nguyên, DANH TÍNH nhãn đã khác (Đ4)."""
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    d = json.loads(goc)
    a = next(r for r in d["dong_thieu"] if r["ky"] == "2026-07" and r["nhan"] == "KHOA_LECH")
    b = next(r for r in d["dong_thieu"] if r["ky"] == "2026-07" and r["nhan"] == "TRUNG_SEQ")
    for k in ("nhan", "lech", "ghi_chu"):
        a[k], b[k] = b[k], a[k]
    sao = tmp_path / "ban_sao.json"
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, out
```
