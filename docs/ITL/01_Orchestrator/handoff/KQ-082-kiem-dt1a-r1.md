# KQ-082 — biên bản kiểm `BG-081` *(ISP 3.1.2 · Step 3 · DT1a · vòng **R1** — quét TOÀN diff)*

| | |
|---|---|
| **Thuộc** | `BG-081` · `WO-080` |
| **Kiểm bởi** | `fls-test` *(R1, phiên mới, độc lập)* · 2026-11-16 · orchestrator giao |
| **Phạm vi** | `git diff 329fa68..isp/DT1A` — **5** tệp *(`b17aaa1` công cụ + bài + JSON · `8124727` phiếu)*. Nền `329fa68` *(S0)* ⛔ thuộc phạm vi |
| **Cụm** | reviewer làn DATA cổng **5447** *(`/home/user/fls-pg16-5447`, dựng lượt này — để CHẠY)* |
| **Phán quyết** | **`ĐẠT`** vòng R1 — **0 CHẶN** · **2 NÊN SỬA** *(`DT1a-R1-01` · `-02`)* · **7 GHI NHẬN**. Mọi AC ĐẠT có bằng chứng tự đo; hai NÊN SỬA ⛔ chặn push *(sổ §1)* — sửa ở vòng kế hoặc orchestrator ghi lý do chấp nhận trước khi đóng `WO` |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1a.md` *(tệp riêng — orchestrator gộp vào sổ chung ở `isp/S0` lúc gộp nhánh)* |

## Cổng vào *(`05` §5)*
- **git:** `isp/DT1A` = `8124727` *(phiếu)* trên `b17aaa1` *(mã)* trên nền `329fa68` — khớp hash `BG-081` dòng **Commit**. Nhánh cục bộ, ⛔ đẩy — **đúng** O2 = A *(ISP §1.2)*, ⛔ phải thiếu sót. `git status` sạch trước khi kiểm.
- **version spec:** ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 3 · DT1a *(dòng `609`–`689`)* = version `WO-080` ghi; AP v3.1.2 sha256 R1 đo `5cf6e576ff46f088…` = `WO-080` `5cf6e576…` ✅.
- **Quan sát *(⛔ phát hiện — ngoài phạm vi R1)*:** `WO-080` khai *"Phụ thuộc: S0 — phải `done` (3 vòng review + gộp)"*; nền `329fa68` tự ghi *"chưa qua R2/R3 — chế độ tăng tốc"*. S0 còn vòng sửa sau R2 *(`KQ-068`: `S0-R2-03` NÊN SỬA chạm chính `--duong-nen`)* ⇒ sau khi S0 gộp, orchestrator nên chạy lại `--duong-nen` trên nhánh gộp trước khi tin dòng *"26 = 26"* dưới đây.

## Cổng chạy lại *(R1 tự chạy ở worktree, `PG_DSN=…:5447/fls` · `PG_DSN_TEST=…:5447/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | `BG-081` nói | R1 đo | Khớp |
|---|---|---|:-:|
| `bash tools/dung_moi_truong_isp.sh --cong 5447` *(dựng cụm reviewer)* | *(cụm 5437)* 7/7 `[ĐẠT]` | `initdb /home/user/fls-pg16-5447` · `da ap 26 migration` · `pg_verify: khop` · **7/7 `[ĐẠT]`** *(K7 `fls_itl = 0 dòng`)* · `══ KẾT: ĐẠT` · exit 0 | ✅ |
| `pytest tests/du_lieu/test_phan_loai_dong_thieu.py` | `16 passed in 2.78s` | `16 passed in 2.73s` · exit 0 *(`-rA`: 16 tên PASSED — đúng 14 hàm `def test_`, hàm checksum × 3)* | ✅ |
| `python tools/phan_loai_dong_thieu.py` | exit 0 · `KẾT: ĐẠT … 122 … 147` | exit 0 · `① MẪU SỐ: sổ AS-IS 9.967 dòng sổ · ghép 1-1 9.845 dòng ghép · FLS dựng lại 9.992 dòng canon` · `② … 122 / 9.967 dòng sổ = 1,22 % · rải 18/23 kỳ` · `③ … 147 / 9.992 dòng canon = 1,47 %` · `KẾT: ĐẠT` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --cong 5447 --duong-nen` | `12 failed, 2448 passed, 2 xfailed, 14 errors` · `26 = 26` · web `3 failed, 661 passed` · `3 = 3` · `KẾT: ĐẠT` | toàn bộ `12 failed, 2448 passed, 2 xfailed, 14 errors in 317.33s` *(mẫu số **2.476** bài)* · `[ĐẠT] … 26 = 26 node id (thêm 0 · bớt 0)` · `tests/du_lieu` trong tập đỏ: **0** · web `3 failed, 661 passed in 177.49s` · `[ĐẠT] … 3 = 3` *(3 bài SỔ THẬT `wo022`/`wo022_v2`/`wo042` — đúng BG)* · **`══ KẾT: ĐẠT`** exit 0 | ✅ |
| hai bài chập chờn `tests/web/test_wo032_man_cua_that.py::test_AC3_…` / `::test_AC7_…` | ⛔ đỏ ở lượt BG | **lượt 1** *(trong `--duong-nen`)*: ⛔ có trong tập đỏ web *(grep `wo032_man_cua_that` = 0)* · **lượt 2** *(chạy riêng `-k "AC3 or AC7"`)*: `5 passed, 7 deselected in 1.41s` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` exit 0 *(cũng là K5 của script dựng)* | ✅ |
| `python tools/do_voi_so_luong.py` *(tiền điều kiện ISP mục 5)* | `Σ 9967 9845 … 69510/69510` | `Σ          9967   9845    3341    2700  30756  22290    112   13  69510/69510` exit 0 | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `174 file, 1854 bang` | `174 file, 1854 bang, 723 o ngay, 104 ma QD` exit 0 *(đo TRƯỚC khi thêm hai tệp của R1)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech` · đường nền | exit 1 · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` · `B3` `B4` `C5` `C5b` KHONG DO DUOC · `A1` `B1` `C6` DOI TRANG THAI — trùng `DUONG_NEN.md:434` *(kho rỗng)* | ✅ |
| `python tools/soi_bang_tuyen.py` | `40 tuyen` | `✅ ban khai KHOP SQL that o ca 40 tuyen` exit 0 | ✅ |
| `python tools/kiem_thuyet_minh.py` | `31/31` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` exit 0 | ✅ |
| `python -m fls.db.pg_migrate` | `khong co gi de ap` · `pg_verify: khop` | `khong co gi de ap` · `pg_verify: khop` exit 0 | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC *(`.venv/Scripts/lint-imports.exe`)* | exit 1 · `FileNotFoundError: … '/home/user/FLS-tobe/.claude/worktrees/isp-dt1a/.venv/Scripts/lint-imports.exe'` — **⛔ KHÔNG ĐO ĐƯỢC** ở container *(đường nền `DUONG_NEN.md:432`)*; ⛔ do bước này | ✅ *(cùng đỏ)* |

## Phép đo ĐỘC LẬP *(R1 — ⛔ import mã tác giả)*
Kịch bản `scratchpad/do_doc_lap.py` *(ngoài repo, `python3 -I`)* đọc thẳng ba ảnh `tests/fixture/{itl_ledge_adjustment, classifying_vs_canon, pm_join}.json`, giải mã theo **tên** cột *(⛔ chỉ số cứng)*, rồi so **từng trường** của `docs/ITL/_tools/phan_loai_dong_thieu.json` đã commit. Kết: **`ĐẠT` — 0 lệch / 26 phép so** *(25 phép so với JSON + 1 phép hai nguồn trong ảnh sổ — đếm dòng `[ĐẠT]` của kịch bản)*.

| Đại lượng *(nhãn — Đ4)* | R1 đo | JSON / BG | Khớp |
|---|---|---|:-:|
| dòng sổ `dong_sheet` *(phần tử `g.dong` · khác nhau · trường khai `g.so_dong`)* | **9.967** · 9.967 · 9.967 | `mau_so.so_dong_so` 9.967 | ✅ |
| phân bố kỳ của sổ: đếm ↔ trường khai `g.phan_bo_ky` *(hai nguồn — công cụ ⛔ so phép này)* | 23 kỳ, khớp 23/23 | — | ✅ |
| dòng ghép `dong_so` *(phần tử · khác nhau · `c.so_dong_ghep`)* · `dong_canon` khác nhau | **9.845** · 9.845 · 9.845 · 9.845 | `so_dong_ghep` 9.845 | ✅ |
| dòng bank `pm_join` *(phần tử · khác nhau · `p.so_dong_bank` · `c.so_dong_canon`)* | **9.992** · 9.992 · 9.992 · 9.992 | `so_dong_canon` 9.992 | ✅ |
| `dong_so` ⊄ `dong_sheet` · `dong_canon` ⊄ bank *(mẫu số 9.845 — Đ3)* | **0** · **0** | — | ✅ |
| **THIẾU** = `dong_sheet` ∖ `dong_so` *(dòng sổ)* | **122** — danh sách = JSON **từng phần tử**, vân tay `18047e0eb0319ea1` | 122 · `18047e0eb0319ea1` | ✅ |
| **NGƯỢC** = bank ∖ `dong_canon` *(dòng canon)* | **147** — danh sách = JSON, vân tay `6ac2463a190ff631` | 147 · `6ac2463a190ff631` | ✅ |
| 122 dòng × (10 thuộc tính + `nhan = null`, ⛔ khoá thừa) = ô ảnh sổ | **0** dòng lệch / 122 | — | ✅ |
| 147 dòng: khoá đúng `{dong_canon, nhan}`, `nhan = null` | **0** dòng lệch / 147 | — | ✅ |
| phân bố kỳ thiếu | `2026-07` 23 · `2025-11` 14 · `2026-08` 13 · `2026-06` 12 · `2025-10` 9 · `2026-04` 8 · `2025-12`/`2026-02`/`2026-03`/`2026-05` 5 · `2025-07`/`2025-08`/`2025-09`/`2026-01` 4 · `2025-06` 3 · `2025-02` 2 · `2025-01`/`2025-05` 1 — **18** kỳ, Σ 122 | MONG tool + bài + ISP `:20` *(3 kỳ đầu)* | ✅ |
| kỳ ⛔ có thiếu | `2024-10` · `2024-11` · `2024-12` · `2025-03` · `2025-04` *(5)* ⇒ 18/23 | BG `:105` | ✅ |
| `hd_classifying` của 122 dòng thiếu | `Need to manual input` **121** · `GI \| Gross Inflow` 1 | ISP `:20` 121/122 | ✅ |
| `hd_final` | OGA **74** · GI **25** · DEP **8** · ITE **7** · NB 2 · OMC 2 · LC 2 · LMN 1 · BON 1 *(khác = 8)* | ISP `:20` | ✅ |
| `pay_type_final` · `cdt1_final` | Regular **71** · Thu tiền **51** · SHQ1 **60** · SHQ2 **49** · COR **9** · bốn mã ×1 | BG `:102` · `:104` | ✅ |
| `theo_ky` · `phan_bo_thuoc_tinh` *(9 thuộc tính)* · `thuoc_tinh_theo_ky` *(4)* | khớp trọn | JSON | ✅ |
| bảng thuộc-tính × kỳ của BG *(`:84`–`:101`, 18 hàng × 16 cột)* | **0** hàng lệch / 18 · Σ dòng sổ 18 kỳ = **9.323** | BG `:102` 9.323 | ✅ |
| khoá dict của JSON *(đếm cả lặp)* | **1.940** *(trong đó `dong_thieu` 1.464 · `dong_nguoc` 294)* | BG `:55` 1.940 | ✅ |
| cỡ JSON | 3.298 dòng · 73.280 byte | BG `:31` | ✅ |

⭐ **Kiểm ĐỊNH NGHĨA khoá** *(BG "yếu #2": nếu `dong_so` đánh số theo một bản sổ KHÁC thì bài và công cụ cùng sai mà vẫn khớp)*: so `cls_hd`/`cls_pay_type`/`cls_cdt1` của **ảnh ghép** với `*_classifying` của **ảnh sổ** theo **cùng số dòng** ⇒ **29.535/29.535 ô = 100,00 %**; đối chứng lệch một dòng *(`dong_so + 1`)* ⇒ 21.748/29.535 = 73,63 %. ⇒ `dong_so` và `dong_sheet` **cùng hệ đánh số** — bằng chứng HAI NGUỒN *(hai hiện vật khác nhau, cùng tệp sổ gốc `[Master] ITL_Ledge_raw.xlsx`; trường `nguon` của cả hai)* mà BG chưa có. ⚠ Nó chứng minh **cùng bản sổ**, ⛔ chứng minh mã ghép đúng — phần ấy là DT1b/H3. Đề xuất đưa phép này vào công cụ *(rẻ, đóng yếu #2)* — ⛔ ghi thành phát hiện vì BG đã tự nêu.

## Chứng minh ĐỎ *(R1 tự phá, bản sao ở scratchpad — ⛔ chạm `tests/fixture/`)*
| Kịch bản | Kết quả nguyên văn |
|---|---|
| ⓪ bản sao NGUYÊN *(đối chứng)* | exit **0** · `KẾT: ĐẠT …` |
| ① **bỏ 1 dòng ghép** — R1 chọn dòng **GIỮA** *(chỉ số 4.922: `dong_so 4974 · dong_canon 4969`, còn 9.844)*, ⛔ dòng đầu như BG | exit **1** · `② dòng sổ ⛔ ghép: 123 / 9.967 dòng sổ = 1,23 %` · stderr **12** dòng, gồm `dòng sổ ⛔ ghép (sổ ∖ ghép): đo 123 · mong 122` · `dòng FLS ⛔ có dòng sổ (canon ∖ ghép): đo 148 · mong 147` · `phân bố kỳ … '2025-11': 15` · hai vân tay đỏ |
| ② trả nguyên | exit **0** · `KẾT: ĐẠT` |
| ảnh thật | `sha256sum` 3 ảnh + JSON **trước = sau** *(`b59cb0d3…` · `34aa375d…` · `0d1a6fbb…` · `df7facae…`)* · `git status` sạch |
| ③ đổi **nhãn** cột `cdt1_mid` ↔ `cdt1_final` trong `cot` ảnh sổ *(thân y nguyên)* | exit **0** `KẾT: ĐẠT` — `cdt1_final` in ra có `∅ 1` ⇒ **`DT1a-R1-04`** |
| ④ đổi nhãn `pay_type_classifying` ↔ `cdt1_classifying` | exit **0** ⇒ **`DT1a-R1-04`** |
| ⑤ đổi `dong_canon` của dòng ghép đầu sang một dòng bank chưa ghép *(phía canon)* | exit **1**, **mọi** dòng lệch là `vân tay tập ngược` — cổng có cắn, nhưng ⛔ bài nào của Dev canh ⇒ **`DT1a-R1-02`** |

**Đột biến công cụ** *(bản sao `git archive isp/DT1A`, chạy 16 bài với `--noconftest` — ⛔ chạm kho test)*: 11 đột biến, bộ bài bắt **2/11** *(M9 mẫu số 0 · M10 checksum `pm_join`)*; sống: M1 nối `kiem_rieng_tu` · M2 vân tay ngược · M3 hai nguồn tập thiếu · M4 dòng ghép trỏ dòng sổ ⛔ có · M5 canon ⛔ thuộc bank · M6 `dong_so` trùng · M7 MONG phân bố hd/pay · M8 ghi JSON khi đỏ · M11 số kỳ. Đối chứng sau khi trả nguyên: `16 passed`. ⇒ `DT1a-R1-01` · `-02` · `-03`.

## Bảng AC *(= test ID ISP mục 6)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `DT1a-B1` | 122 dòng; 147 chiều ngược; phân bố kỳ có MONG | Công cụ exit 0: **122** / 9.967 dòng sổ · **147** / 9.992 dòng canon · 18/23 kỳ. Bốn bài B1 PASSED. **Phép đo độc lập R1** khớp danh sách 122 + 147 **từng phần tử**, 18/18 kỳ, mọi ô thuộc tính *(0 lệch / 122 dòng)*. MONG phân bố kỳ khai trong `tools/phan_loai_dong_thieu.py:90-94` + bài `:58-62` *(⚠ 15/18 kỳ do DT1a tự đo — `DT1a-R1-05`; nay R1 xác nhận độc lập)* | **ĐẠT** |
| **AC-2** · `DT1a-B2` | cổng ĐỎ (123 ≠ 122) rồi trả nguyên (Đ5) | R1 tự phá dòng ghép **giữa** *(khác dòng BG chọn)*: exit 1 · `đo 123 · mong 122`; trả nguyên exit 0; sha256 ảnh thật trước = sau. Bài `…bo_MOT_dong…` PASSED *(đối chứng 0 → phá 1 → trả 0, đòi `== 1`)* | **ĐẠT** |
| **AC-3** · `DT1a-B3` | in 9.967 dòng sổ và 9.845 dòng ghép trước tỷ lệ | stdout R1: dòng `①` mang `9.967 dòng sổ` · `9.845 dòng ghép` · `9.992 dòng canon` — đứng **trước** ký tự `%` đầu tiên *(dòng `②`)*. Mẫu số 0 ⇒ exit 1, stdout ⛔ có `%` *(bài PASSED; đột biến M9 bị bài bắt)* | **ĐẠT** |
| **AC-4** · `DT1a-B4` | 0 khoá `dien_giai` / `so_chung_tu` / `email` | R1 liệt kê **60** tên khoá khác nhau của JSON — 0 khoá cấm; quét toàn văn: `@` **0** · `Did not find` **0** · `FT`+≥ 8 ký tự **0** · chuỗi số ≥ 9 chữ số **0**; 37 giá trị chuỗi khác nhau ở `dong_thieu` + `phan_bo` = 18 kỳ + nhãn danh mục hd/pay/cdt1 *(⛔ tên người, ⛔ Số CT)*. Mẫu số: **1.940** khoá đã quét *(Đ3)*. ⚠ chốt **tự chặn** của công cụ chưa có bài chứng minh được nối ⇒ `DT1a-R1-01` *(⛔ làm AC-4 trượt: AC đòi JSON ra sạch — đã đo sạch)* | **ĐẠT** |

## Đối chiếu từng dòng mục 8 *(Exit criteria — ISP `:664`–`:667`)*
| Dòng mục 8 | Bằng chứng | Kết |
|---|---|---|
| DT1a-B1…B4 đúng; DT1a-B2 đã thấy đỏ | Bảng AC trên: 4/4 ĐẠT, B2 R1 tự thấy đỏ *(dòng ghép khác BG)* | ✅ |
| MONG khai trong tool (Đ5) | `tools/phan_loai_dong_thieu.py:82-104` — 9 khoá MONG *(4 số dòng · 2 tập · phân bố kỳ · 3 phân bố thuộc tính · 2 vân tay)*; bài `…MONG_khai_TRONG_tool…` so MONG tool = MONG bài. ⚠ `cdt1_*` và `cot` ⛔ có MONG ⇒ `DT1a-R1-04` *(GHI NHẬN)* | ✅ |
| 3 vòng review xong | R1 = phiếu này. R2 `KQ-083` · R3 `KQ-084` chưa chạy | ⏳ *(⛔ thuộc R1)* |
| điều kiện PUSH: đủ R1 · R2 · R3, phát hiện chặn = 0 | R1: **0 CHẶN** | ⏳ |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 3 + `CLAUDE.md` Đ1–Đ5)* | **ĐẠT có ghi chú.** Định nghĩa hai tập đúng chữ ISP §3 *(`dong_sheet` ∖ `dong_so`; bank ∖ `dong_canon`)*; `nhan = null` ở 269/269 dòng ⇒ ⛔ lấn sang LÝ DO *(DT1b)* — BG chỉ có một đoạn **"Quan sát, ⛔ nhãn"** *(`:107`, hai ô `cdt1_final` lệch khuôn)*, ⛔ gán. Q1 = ⓐ *(liệt kê 147 `dong_canon`, `nhan = null`)* đã được orchestrator chấp nhận. Đ3: mẫu số in trước, mẫu số 0 ⇒ ĐỎ *(đã có bài)*. Đ5: MONG khai trước, NO cả hai chiều — nhưng **9/11** đột biến sống *(`DT1a-R1-01` · `-02` · `-03`)* và checksum ⛔ phủ `cot` *(`-04`)*. Đ1/Đ4: ba câu chú thích nói quá *(`-05`)* | §Chứng minh ĐỎ · §Đột biến · `SO_PHAT_HIEN_ISP-3.1_DT1a.md` |
| **Dữ liệu** *(ảnh đóng băng trong repo; ⛔ kho thật — container ⛔ có sổ thật)* | **ĐẠT.** Phép đo độc lập 26/26 khớp; định nghĩa khoá được xác nhận HAI NGUỒN *(29.535/29.535 ô cls)*. ⛔ đếm đôi: `dong_sheet` · `dong_so` · `dong_canon` · bank đều ⛔ trùng *(9.967/9.967 · 9.845/9.845 · 9.845/9.845 · 9.992/9.992)*; ⛔ mất dòng im lặng: 9.845 + 122 = 9.967 · 9.845 + 147 = 9.992. Kho: công cụ ⛔ mở kết nối *(chỉ đọc 3 tệp)*; cụm 5447 K7 `fls_itl = 0 dòng` | `do_doc_lap.py` · §Phép đo độc lập |
| **Màn hình** | **N/A** — ISP §4 *"Frontend: N/A — bước dữ liệu"*; diff ⛔ chạm `fls/web/**` *(5 tệp, ⛔ tệp màn)* | `git diff --stat 329fa68..isp/DT1A` |

**Quyền làn:** cả 5 tệp nằm trong bảng tệp làn DATA *(ISP `:94`: `tests/du_lieu/**` · `tools/phan_loai_dong_thieu.py` · `docs/ITL/_tools/phan_loai_dong_thieu.json`)* + phiếu `BG-*` của Dev; ⛔ chạm `WO-080` · `handoff/README.md` · `08_CHANGELOG_RELEASE.md` · dashboard *(đúng `TIEN_DO.md` §Quy ước · `S0-R1-08`)*. `tests/du_lieu/__init__.py` = **0 byte** *(R1 đo)*. Đọc *(⛔ ghi)* `tools/do_voi_so_luong.py` của làn BE-HC ⇒ `DT1a-R1-06`.

## Phát hiện *(chi tiết đầy đủ + luật phòng tái phạm: `SO_PHAT_HIEN_ISP-3.1_DT1a.md`)*
| Mã | Lớp | Mức *(↔ `10` §3.4)* | Nơi | Tái hiện | Khuyến nghị | Gửi |
|---|---|---|---|---|---|---|
| `DT1a-R1-01` | B1 | **NÊN SỬA** *(`NANG`)* | `tools/phan_loai_dong_thieu.py:254` · `tests/du_lieu/test_phan_loai_dong_thieu.py:337-341` | Thay `:254` bằng `pass` *(M1)* ⇒ `16 passed`. Bài `…tool_TU_CHAN_truoc_khi_ghi` chỉ gọi hàm rời | Thêm bài cấy email vào `hd_mid` của một dòng thiếu trên bản sao, đòi dòng `riêng tư: email … hd_mid` *(§Bài thử đề xuất ①)* | `DEV` |
| `DT1a-R1-02` | B1 | **NÊN SỬA** *(`NANG`)* | `tools/phan_loai_dong_thieu.py:233` | Bỏ `kiem` vân tay ngược *(M2)* ⇒ `16 passed`; phá phía canon *(§Chứng minh ĐỎ ⑤)* chỉ vân tay ngược cắn | Thêm bài đổi chỗ phía canon *(§Bài thử đề xuất ②)* | `DEV` |
| `DT1a-R1-03` | B1 | GHI NHẬN *(`NHE`)* | `tools/phan_loai_dong_thieu.py:193-198` · `:202-203` · `:211` · `:219-223` · `:229-230` · `:308-316` | 7 đột biến M3–M8 · M11 sống | Ít nhất bài cho M8 *(`main(["--ghi"])` trên bản sao đã phá ⇒ exit 1 và hiện vật ⛔ ghi)*; còn lại khai *"phòng thủ chồng"* | `DEV` |
| `DT1a-R1-04` | B1 | GHI NHẬN | `tools/phan_loai_dong_thieu.py:172` · `:82-104` | Đổi nhãn `cdt1_mid` ↔ `cdt1_final` trong `cot` ⇒ exit 0, `cdt1_final` có `∅ 1` | MONG cho bộ 23 tên `cot` + phân bố `cdt1_final` | `DEV` |
| `DT1a-R1-05` | B1 | GHI NHẬN | `tools/phan_loai_dong_thieu.py:8-10` · `:26-27` · `:31` · `:89` · bài `:9-10` · `:13-15` · `:51` · `:57` | *"6 kỳ đầu"* — repo có 3 *(grep 0 dòng cho kỳ thứ 4–6)*; *"1.401 cặp"* = 1.401 dòng ghép *(3.810 cặp)*; *"⛔ máy nào đỏ"* — `do_voi_so_luong.py:118` · `:129` · `:138` đã ghim ba tổng | Sửa ba câu *(sổ)* | `DEV` |
| `DT1a-R1-06` | B1 | GHI NHẬN | `tools/phan_loai_dong_thieu.py:63-66` | Import `_sha` + `MONG` từ tệp làn BE-HC mà H2 *(W2)* sẽ sửa | Ghi vào `WO` của H2 *(hoặc H2 nâng `_sha` thành công khai)* | orchestrator |
| `DT1a-R1-07` | B1 | GHI NHẬN | `tools/phan_loai_dong_thieu.py:316` | Đọc mã: `write_text` thẳng lên đích | Tệp tạm + `os.replace` | `DEV` |
| `DT1a-R1-08` | B1 | GHI NHẬN | ISP `:788` · `:824` · `:836` · `:94` | Q2 = ⓐ trái chữ ISP Step 5; tệp nhãn mới ⛔ có trong bảng tệp làn DATA | Ghi Q2 + tên tệp nhãn vào `WO` DT1b và bảng tệp làn | orchestrator / `BA` |
| `DT1a-R1-09` | B1 | GHI NHẬN | `docs/ITL/_tools/phan_loai_dong_thieu.json:3` · `tools/phan_loai_dong_thieu.py:106` | Câu khai 5 thứ ⛔ mang; máy chặn 3 tên khoá | Thu câu khai hoặc mở `KHOA_CAM` *(hai bản)* | `DEV` |

**Theo mức:** CHẶN **0** · NÊN SỬA **2** · GHI NHẬN **7** — lớp **B1** cả 9 *(A1 · A2 · B2: 0 — bước ⛔ chạm FE, ⛔ chạm LLM)*.

## Bài thử ĐỀ XUẤT *(⛔ commit — orchestrator chỉ cho R1 commit phiếu + sổ; Dev đưa vào `tests/du_lieu/` nếu nhận khuyến nghị)*
Hai bài viết ở bản sao `scratchpad/ban/tests/du_lieu/test_kq082_de_xuat.py`, chạy `--noconftest`:

| Bài | Đã chứng minh ĐỎ bằng cách | Xanh |
|---|---|---|
| ① `test_R1_02_rieng_tu_NOI_vao_duong_do_that` — bản sao tạm; `bang_gia_tri.append("ke-toan@vi-du.vn")`, trỏ ô `hd_mid` của dòng THIẾU đầu tiên vào đó; `--thu-muc` ⇒ đòi exit 1 **và** một dòng stderr chứa `riêng tư: email` + `hd_mid` | đột biến M1 *(bỏ `loi.extend(kiem_rieng_tu(kq))`)* ⇒ `1 failed, 1 passed` — bài này FAILED | `b17aaa1` ⇒ PASSED · trả nguyên ⇒ PASSED |
| ② `test_R1_03_doi_cho_phia_CANON_chi_van_tay_NGUOC_can` — bản sao; `dong_canon` của dòng ghép đầu ⇒ dòng bank nhỏ nhất chưa ghép; đòi exit 1 **và** mọi dòng lệch chứa `vân tay tập ngược` | đột biến M2 *(bỏ `kiem` vân tay ngược)* ⇒ bài này FAILED | `b17aaa1` ⇒ PASSED · trả nguyên ⇒ PASSED |

## Câu trong `BG-081` — R1 đối chiếu
| `BG-081` | R1 đo | Kết |
|---|---|---|
| `:28` *"25 phép so (22 lời gọi `kiem` + vòng phân bố × 3) + 1 quét riêng tư"* | 23 lời gọi `kiem` trong mã = 22 ngoài vòng + 1 trong vòng chạy × 3 ⇒ **25** | đúng |
| `:30` *"16 bài (14 hàm `def test_`; … 14 − 1 + 3 = 16): B1 ×4 · B2 ×5 · B3 ×2 · B4 ×3 · CLI/Đ5 ×2"* | 14 hàm · 16 node · 4 + 5 + 2 + 3 + 2 = 16 | đúng |
| `:30` *"MONG của bài **độc lập** với MONG của tool"* · tool `:26` *"lấy từ phép đo TAY ĐỘC LẬP của orchestrator"* | 15/18 kỳ + tách *"khác 8"* do DT1a tự đo *(tool `:96` · bài `:64` tự ghi phần "khác 8"; phần 15 kỳ thì ghi sai thành "12 kỳ")* | **nói quá** ⇒ `DT1a-R1-05` |
| `:116` Đ1 *"tên ảnh xuất hiện ở **7** tệp `.py` … **0** dòng `write`/`dump` … `docs/` **4** tệp `.md` … `checksum_noi_dung` chỉ được so ở `test_classifying.py:103` · `test_pm_join.py:329` · `do_voi_so_luong.py:125,133`"* | grep R1: **7** tệp `.py` · **0** dòng write/dump · **4** tệp `.md` · đúng ba chỗ ấy *(các hit khác của `checksum_noi_dung` là ảnh khác / `sao_luu_kho.py`)* | đúng |
| `:117` yếu #2 *"nếu `dong_so` là số dòng của một bản sổ KHÁC … cả hai cùng sai"* | R1 đo hai nguồn: cls ảnh ghép = classifying ảnh sổ **29.535/29.535** ô ⇒ cùng bản sổ, cùng hệ đánh số *(⛔ chứng minh mã ghép đúng — DT1b/H3)* | rủi ro **đã đo — thấp** |
| `:116` yếu #1 checksum chỉ so trường ghim | Với mục đích DT1a *(danh tính tập)*: mọi phép phá **tập** R1 thử đều bị vân tay/đếm bắt; phần ⛔ phủ là ô `cls_*`/`canon_pos_*` mà DT1a ⛔ dùng *(đã có `tests/ledger/test_classifying.py:128` canh 68.915 ô)*. Lỗ thật nằm ở ảnh **sổ**: `cot` ⛔ trong checksum ⇒ `DT1a-R1-04` | rủi ro **thấp** cho DT1a |
| `:105` *"18/23 kỳ … khớp AP v3.1.2 §5.3"* · `:106` dòng thiếu duy nhất có `hd_classifying = GI` là dòng duy nhất của `2025-01` | `dong_sheet 744`, kỳ `2025-01`, kỳ ấy 1 dòng thiếu | đúng |
| `:37`/`:38` lượt cổng | khớp số đếm *(§Cổng chạy lại)* | đúng |

## Q1 · Q2 *(orchestrator đã chốt — R1 chỉ ghi hệ quả)*
- **Q1 = ⓐ** *(liệt kê 147 `dong_canon`, `nhan = null`, ⛔ thuộc tính)*: JSON đúng như thế — 147/147 dòng chỉ hai khoá *(R1 đo)*.
- **Q2 = ⓐ** *(DT1b ghi nhãn ra tệp RIÊNG khoá theo số dòng + hai vân tay)*: bài `test_DT1a_B1_json_DA_GHI_khop_lan_do_hien_tai` giữ nguyên nghĩa *(JSON DT1a ⛔ đổi)*. Nhưng ISP Step 5 vẫn ghi ngược lại ⇒ `DT1a-R1-08`.

## Môi trường R1 để lại
Cụm `5447` *(`/home/user/fls-pg16-5447`)* **đang chạy** theo yêu cầu orchestrator. Kịch bản đo của R1 ở scratchpad phiên *(⛔ trong repo)*: `do_doc_lap.py` · `dot_bien.py` · `chung_do_de_xuat.py` · `cap.py` · `bang_bg.py` · bản sao `ban/`.
