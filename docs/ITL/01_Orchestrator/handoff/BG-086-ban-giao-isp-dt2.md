# BG-086 — bàn giao `WO-085` *(ISP 3.1.2 · `DT2`)* — đường ống đóng băng sheet + ảnh `IX.FX` *(9.2 Exchange Rate)*

| | |
|---|---|
| **Thuộc** | `WO-085` *(orchestrator ghi sau — ISP là spec, theo lời giao)* |
| **Phát bởi** | `fls-dev` *(agent **FE** nhận một bước làn **DATA** — người dùng cho phép 16/11 khi ⛔ có bước FE sẵn sàng)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-087` · R2 `KQ-088` · R3 `KQ-089` *(dải orchestrator cấp)* |
| **Commit** | nhánh **cục bộ** `isp/DT2` @ **`3902623`** *(mã + bài + ảnh)* — tách từ `329fa68`; ⛔ đẩy, ⛔ gộp *(lời giao: orchestrator gộp sau R3)*. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-dt2` · cụm PG cổng **5436** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` mục **`## Step 8 · DT2`** *(8 trường + Substep 1/2)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §3.2.1 *(hàng `IX.FX`)* · §3.2.4 *(hàng "bảng tỷ giá")* · `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1.md` cột *Luật phòng tái phạm* *(10 hàng `S0-R1-01…10`)* · `CLAUDE.md` Đ1–Đ5 · Cổng · Bẫy |

## Cổng vào *(`05` §5)*
- **git thật**: worktree ở nhánh `isp/DT2`, `git log -1` = `329fa68 Nền wave 1: nhánh làm việc + isp/S0 @ 3d8318c` — khớp lời giao. Cây sạch khi nhận.
- **version**: ISP 3.1.2 · AP v3.1.2. Run id: ⛔ cần *(bước ⛔ nói "đã chạy")*.
- ⚠ **Số bước lệch nhãn**: lời giao gọi *"Step 7 · DT2"*; ISP v3.1.2 ghi **`## Step 8 · DT2`** *(dòng 1016)* — `Step 7` ở ISP là `CG1` *(dòng 936)*. Mã `DT2`, goal và mục 6 khớp nguyên văn lời giao ⇒ làm theo `DT2`. Xin ghi đúng `Step 8` khi soạn `WO-085`.
- **Môi trường**: `bash tools/dung_moi_truong_isp.sh --cong 5436` ⇒ exit 0 · **7/7 `[ĐẠT]`** · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` *(26/26 di trú · `pg_verify khớp 25 bảng/view (0 lệch)` · `Contracts: 11 kept, 0 broken.` · `chay 9845 / co 9967` · `fls_itl = 0 dòng`)*.

## Substep 1 — test cases · kế hoạch tối thiểu · lệnh · giới hạn
1. **Test cases** *(mục 6, phủ mọi dòng mục 8)*: `DT2-B1` *(37 dòng · checksum ổn định 2 lần chạy)* · `DT2-B2` *(cột `Email Address` ⇒ ĐỎ, ⛔ ghi tệp)* · `DT2-B3` *(thiếu 1 tháng ⇒ ảnh ghi đúng nguồn + `thiếu: [yyyymm]` + exit ≠ 0)*. Thêm **đối chứng Đ5** cho mỗi cổng công cụ có: checksum phải ĐỔI khi một ô/thứ tự đổi · `--mong` đỏ cả hai chiều · trùng bù thiếu vẫn đỏ · khoá hỏng/ô rỗng đỏ · 4 đường từ chối exit 2. Mục 8 *"ảnh ⛔ mang khoá PII (quét = 0)"* ⇒ bài quét riêng có mẫu số.
2. **Kế hoạch tối thiểu**: đúng 4 tệp lời giao cho phép — `tools/dong_bang_sheet.py` *(mới)* · `tests/du_lieu/test_dong_bang_sheet.py` *(mới)* · `tests/du_lieu/__init__.py` *(**0 byte**, quy ước repo — 12 thư mục `tests/*` có nó)* · `tests/fixture/cau_hinh/ix_fx.json` *(sinh bằng công cụ)*. ⛔ sửa `fls/**`: tái dùng bằng `import` `fls.oracle.anh_chup.AnhChup` + `fls.adapters.pm_join.PM_COT_RIENG_TU` *(chỗ khai duy nhất: `fls/adapters/pm_join.py:125`)*.
3. **Lệnh** *(từ gốc worktree; `export PG_DSN='postgresql://fls:fls@localhost:5436/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5436/fls_test' PYTHONUTF8=1`)*:
   - `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/du_lieu/test_dong_bang_sheet.py`
   - `/home/user/FLS-tobe/.venv/bin/python tools/dong_bang_sheet.py ix_fx <bản_thô.json> --mong 37`
   - `bash tools/dung_moi_truong_isp.sh --cong 5436 --duong-nen`
4. **Giới hạn**: ảnh là của MỘT ngày đọc *(2026-11-16)*; tháng mới cần lượt đóng băng mới *(HD5, ngoài bước)*. Bản thô thật nằm ở scratchpad orchestrator, ⛔ commit ⇒ bài trong repo ⛔ đọc được nó *(xem "Dev tự thấy còn yếu" ①)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/dong_bang_sheet.py` *(mới, 382 dòng)* | một lệnh: bản thô `{nguon, doc_luc, cach_doc, cot, dong}` → ảnh có `checksum_noi_dung`. Khuôn = **cột chọn + khoá** *(bảng `KHUON`, một dòng `ix_fx`)* — DT3…DT11 thêm dòng, ⛔ viết công cụ thứ hai. Exit **0** đạt · **1** cổng đỏ *(ảnh vẫn ghi đúng nguồn)* · **2** từ chối *(⛔ ghi tệp, ⛔ tạo thư mục; đúng một dòng `⛔ TỪ CHỐI …`)*. Năm quyết định ghi trong docstring: ① `Decimal` ⛔ `float` · ② `thu_tu` vào checksum *(thứ tự sheet là dữ liệu)* · ③ `ngay_dong_bang` = `doc_luc` · ④ riêng tư chặt hơn nguồn khai · ⑤ cổng ⛔ chỉ đếm dòng |
| `tests/du_lieu/test_dong_bang_sheet.py` *(mới, 20 bài)* | `DT2-B1…B3` + đối chứng Đ5; bản thô **TỔNG HỢP** dựng trong bài *(⛔ số thật)*; ảnh đã commit kiểm bằng **tái tạo bản thô từ ảnh** ⇒ chạy lại công cụ phải ra đúng từng byte; checksum ghim **khai TRƯỚC** khi có công cụ |
| `tests/du_lieu/__init__.py` *(mới, 0 byte)* | quy ước repo; DT1a song song tạo tệp y hệt ⇒ gộp ⛔ xung đột nội dung |
| `tests/fixture/cau_hinh/ix_fx.json` *(sinh máy, 368 dòng, sha256 `e2c9fdd028bd3286…`)* | ảnh `9.2.Exchange Rate` đọc `effectiveValue` 16/11: **37 dòng** = 36 tháng `202401→202612` + dòng lạc `202306` *(`thu_tu` 25, giữa `202512` và `202601`)* · `checksum_noi_dung` **`b6d1f9e9074951f1`** |

## Cổng *(kết quả nguyên văn — cụm 5436, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/du_lieu/test_dong_bang_sheet.py` | exit 0 · `20 passed in 1.97s` |
| `bash tools/dung_moi_truong_isp.sh --cong 5436 --duong-nen` · **lượt 1** *(cây trước commit, cùng mã)* | exit 0 · toàn bộ `12 failed, 2452 passed, 2 xfailed, 1 warning, 14 errors in 315.16s (0:05:15)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 177.92s (0:02:57)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong`. Mẫu số: `--collect-only` = **2480** bài = 12 + 2452 + 2 + 14, trong đó **20** ở `tests/du_lieu/` *(⛔ bài nào trong tập đỏ)*. Hai bài chập chờn `test_wo032_man_cua_that.py::test_AC3_…/::test_AC7_…` **⛔ đỏ** ở lượt này |
| `bash tools/dung_moi_truong_isp.sh --cong 5436 --duong-nen` · **lượt 2** *(trên `3902623`)* | exit 0 · toàn bộ `12 failed, 2452 passed, 2 xfailed, 14 errors in 315.03s (0:05:15)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 178.56s (0:02:58)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` *(9 dòng `[ĐẠT]` = 7 kiểm môi trường + 2 đường nền)*. Hai bài chập chờn **⛔ đỏ** ở cả hai lượt ⇒ ⛔ cần chạy lại riêng |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-dt2/.venv/Scripts/lint-imports.exe'` *(gọi cứng đường Windows + đọc kho THẬT — y hệt `BG-066`)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (174 file, 1853 bang, 723 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(đo SAU khi có phiếu này: 174 = 173 trước + BG-086)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — trùng nguyên văn đường nền `BG-066` *(kho rỗng: B3 · B4 · C5 · C5b KHONG DO DUOC; A1 · B1 · C6 DOI TRANG THAI)*; công cụ chỉ đọc `docs/**.md` + kho *(grep `tools/\|tests/\|fixture` trong nó: 0 chỗ đọc)* ⇒ bước này ⛔ chạm được nó |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/bin/lint-imports` | exit 0 · `Contracts: 11 kept, 0 broken.` *(`tools/` ngoài `root_package = fls` — import `fls.oracle` · `fls.adapters` từ công cụ ⛔ vào hợp đồng nào)* |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` *(⛔ chạm schema)* |

## Bằng chứng từng test ID
| ID | Mong | Bài · bằng chứng nguyên văn | Kết |
|---|---|---|---|
| **DT2-B1** | 37 dòng; checksum ổn định qua 2 lần chạy | `test_DT2_B1_dong_bang_37_dong_va_checksum_on_dinh_qua_hai_lan_chay` — 2 lượt cùng bản thô ⇒ **cùng từng byte**, `so_dong == len(dong) == 37`, checksum 16 hex = `AnhChup(...).checksum()[:16]` tính lại, ô 20 chữ số `19744.785000000000001` giữ nguyên. **Trên bản thô thật** *(2 lượt)*: `① lan1: exit=0 · sha256=e2c9fdd028bd3286 · checksum=b6d1f9e9074951f1` · `① lan2: exit=0 · sha256=e2c9fdd028bd3286 · checksum=b6d1f9e9074951f1` · `① bằng ảnh đã commit: True` | đạt |
| DT2-B1 · đối chứng | checksum **đổi** khi nội dung/thứ tự đổi *(Đ5)* | `test_DT2_B1_checksum_DOI_khi_mot_o_hoac_thu_tu_doi` — một xu ở SGD 202507 · đổi chỗ 202401/202402 ⇒ checksum khác | đạt |
| DT2-B1 · ảnh thật | đúng AP §3.2.1: *37 dòng 202401 → 202612 (kể cả dòng lạc 202306)* | `test_DT2_B1_anh_IX_FX_da_commit_dung_37_dong_202401_202612_va_dong_lac_202306` — 37 dòng ảnh = 36 tháng dải + 1 lạc; `(thieu, trung, lac) == ([], [], ['202306'])`; lạc giữa `202512`/`202601`; SGD 202507 = `"20691.51"` *(⛔ `20,692`)*; ô rỗng 0 / mẫu số **185** *(37 × 5)*; checksum = ghim `b6d1f9e9074951f1`. `test_DT2_B1_anh_IX_FX_TAI_TAO_dung_tung_byte_tu_cong_cu` — tái tạo bản thô từ ảnh ⇒ chạy lại ⇒ **đúng từng byte** tệp commit. So ô ngoài bài với bản thô thật: `② so ô: 222 ô (37 dòng × 6 cột) · lệch 0 []` · `② SGD 202507 = 20691.51 · số giá trị có phần lẻ: 24` | đạt |
| Mục 8 · PII | ảnh ⛔ mang khoá PII (quét = 0) | `test_DT2_B1_anh_IX_FX_khong_mang_khoa_PII_quet_bang_0` — quét khoá đỉnh + tên cột khai + khoá từng dòng *(mẫu số > 259)* với `PM_COT_RIENG_TU` *(gộp khoảng trắng, ⛔ hoa thường)* ⇒ **0** | đạt |
| **DT2-B2** | cột `Email Address` ⇒ ĐỎ, ⛔ ghi tệp | `test_DT2_B2_…[nguyen_van]` · `[khoang_trang]` *(`"  Email   Address "`)* · `[chu_thuong]` — exit 2, tệp ra ⛔ có, **thư mục cha ⛔ được tạo**, tệp có sẵn **giữ nguyên byte**, giá trị giả `…@vi-du.invalid` ⛔ lộ ra stdout/stderr. **Bản sao bản thô thật + cột giả lập**: `④ Email Address: exit=2 · tệp ra tồn tại=False · thư mục tồn tại=False · giá trị giả lộ ra màn=False` · `⛔ TỪ CHỐI: bản thô có cột thuộc PM_COT_RIENG_TU: ['Email Address'] — cột ấy ⛔ bao giờ vào kho nên cũng ⛔ vào ảnh; bỏ cột khỏi lượt đọc rồi đóng băng lại — ⛔ ghi tệp nào` | đạt |
| **DT2-B3** | thiếu 1 tháng ⇒ ảnh đúng nguồn + `thiếu: [yyyymm]` + exit ≠ 0 khi `--mong 37` lệch | `test_DT2_B3_ban_tho_thieu_mot_thang_ghi_DUNG_NGUON_va_cong_DO` — exit 1, stdout có `thiếu: [202408]` và `36 dòng ≠ mong 37`, ảnh 36 dòng đúng thứ tự nguồn *(⛔ điền)*, `cong.dat = false`. **Bản sao bản thô thật bỏ 202408**: `③ thiếu 202408: exit=1` · `thiếu: [202408]  (dải chính 202401→202612)` · `[ĐỎ] cổng --mong 37: 36 dòng ≠ mong 37 · thiếu 1 — ảnh đã ghi ĐÚNG NGUỒN, ⛔ sửa; ⛔ dùng ảnh này khi cổng chưa đạt` · `ảnh: so_dong=36 · thieu=['202408'] · 202408 trong ảnh: False` | đạt |
| DT2-B3 · đối chứng | `--mong` đỏ **cả hai chiều** | `test_DT2_B3_cong_mong_DO_ca_hai_chieu[36-1]` · `[37-0]` · `[38-1]` | đạt |
| DT2-B3 · đối chứng | 37 dòng mà trùng bù thiếu ⇒ vẫn đỏ | `test_DT2_B3_thang_TRUNG_bu_cho_thang_THIEU_van_DO` — `trùng: [202408]` + `thiếu: [202409]`, exit 1 *(ca "cộng đôi" của AP §3.2.4 — cổng chỉ đếm dòng sẽ xanh)* | đạt |
| DT2-B3 · đối chứng | khoá ⛔ `yyyymm` / ô rỗng ⇒ đỏ, in mẫu số | `test_DT2_B3_khoa_hong_va_o_rong_thi_DO[khoa_hong]` *(`2024-04`)* · `[thang_13]` *(`202413`)* · `[o_rong]` *(`ô rỗng: 1/185`)* | đạt |
| Từ chối | exit 2, ⛔ ghi | `test_DT2_tu_choi_dau_vao_sai_exit_2_va_KHONG_ghi_tep[thieu_mong]` `⛔ TỪ CHỐI: đối số: the following arguments are required: --mong — ⛔ ghi tệp nào` · `[khuon_la]` `… invalid choice: 'khong_co' (choose from 'ix_fx') …` · `[doi_so_la]` `… unrecognized arguments: --la …` · `[thieu_cot_HKD]` ``⛔ TỪ CHỐI: bản thô thiếu cột khuôn `ix_fx` chọn: ['HKD'] …``. Ngoài bài: `--mong 0` ⇒ `⛔ TỪ CHỐI: --mong 0 — cổng mong 0 dòng là cổng xanh trên tập rỗng (Đ3) — ⛔ ghi tệp nào` | đạt |
| Lệnh ISP | `python tools/dong_bang_sheet.py ix_fx <bản thô> --mong 37` exit 0 | trên bản thô thật: `[ĐẠT] cổng --mong 37: 37 dòng = mong · trùng 0 · thiếu 0 · khoá hỏng 0 · ô rỗng 0/185` · `exit=0` · `soát PII   : 6/6 tên cột · 0 thuộc PM_COT_RIENG_TU ['Email Address']` · `lạc: [202306]  (khoá nhỏ hơn khoá lớn nhất đứng trước — ghi nhận, ⛔ đỏ)` | đạt |

## Mục 8 — đối chiếu
- [x] DT2-B1…B3 xanh; **cổng đã thấy đỏ** *(20/20 đỏ trước mã · 11/11 kiểu phá đỏ · 2 đường đỏ trên bản thô thật)*
- [x] ảnh ⛔ mang khoá PII — quét = **0** trên mẫu số > 259 khoá
- [ ] 3 vòng review — chờ `KQ-087/088/089`
- [ ] điều kiện PUSH — chờ R1 · R2 · R3

## Log ĐỎ → XANH
1. **ĐỎ** *(chưa có `tools/dong_bang_sheet.py`, chưa có `tests/fixture/cau_hinh/`)*: `…/python -m pytest tests/du_lieu/test_dong_bang_sheet.py -rfE` ⇒ exit 1 · `20 failed in 0.89s`. Lý do — đều là **thiếu hành vi**, ⛔ lỗi cú pháp/setup: `can't open file '/home/user/FLS-tobe/.claude/worktrees/isp-dt2/tools/dong_bang_sheet.py': [Errno 2] No such file or directory` *(17 bài)* · `FileNotFoundError: [Errno 2] No such file or directory: '…/tests/fixture/cau_hinh/ix_fx.json'` *(3 bài đọc ảnh)*.
2. ⭐ **Chính lượt đỏ bắt một lỗ của bài**: Python thoát **2** với *"can't open file"* ⇒ 7 bài chỉ đòi `returncode == 2` *(3 B2 + 4 từ chối)* sẽ **XANH SẴN** trên công cụ vắng mặt. Đã thêm `_da_tu_choi`: đòi đúng MỘT dòng `⛔ TỪ CHỐI …` của chính công cụ ⇒ 7 bài ấy đỏ ở ``AssertionError: ('cần đúng MỘT dòng `⛔ TỪ CHỐI …`', "…can't open file…")``.
3. Checksum ghim **khai trước**: tính độc lập bằng `AnhChup` trên bản thô thật *(script scratchpad, ⛔ dùng công cụ)* ⇒ `b6d1f9e9074951f1`; công cụ ra đúng số ấy ở lượt đầu.
4. **XANH**: `20 passed in 2.01s` ⇒ sau 2 chỉnh bài *(dưới)* `20 passed in 1.97s`.
5. Soát lại bài sau khi xanh, tìm ra **2 chỗ lỏng** rồi siết: ⓐ `doc_luc` của bản thô tổng hợp là `2026-11-16` = **ngày chạy** ⇒ công cụ lấy đồng hồ máy vẫn xanh hôm nay — đổi sang `2026-03-09` *(phá thử M7 dưới đây chỉ bị bắt nhờ chỗ này)*; ⓑ B3 đòi `"36" in stdout` — chữ số 36 có thể nằm bất cứ đâu ⇒ đòi nguyên cụm `36 dòng ≠ mong 37`.

## Phá thử — mỗi cổng phải CẮN *(Đ5; phá → chạy bộ bài → trả nguyên)*
| Phá | Kết quả bộ 20 bài |
|---|---|
| M1 bỏ `_soat_rieng_tu` | `3 failed, 17 passed` — B2 ×3 |
| M2 bỏ so `--mong` | `2 failed, 18 passed` — `cong_mong[36-1]` · `[38-1]` |
| M3 bỏ tính thiếu | `2 failed` — B3 thiếu · trùng-bù-thiếu |
| M4 bỏ tính trùng | `1 failed` — trùng-bù-thiếu |
| M5 `Decimal` → `float` | `11 failed, 9 passed` *(ô kiểu `float` bị từ chối ⇒ exit 2)* |
| M6 bỏ `thu_tu` | `4 failed` — tất định · checksum-đổi · tái tạo · ô rỗng |
| M7 ngày = đồng hồ máy | `1 failed` — B1 tất định *(nhờ siết ⓐ)* |
| M8 bỏ ô rỗng | `1 failed` — `[o_rong]` |
| M9 khoá ⛔ soát tháng 01–12 | `1 failed` — `[thang_13]` |
| M10 bỏ lạc | `6 failed` |
| M11 PII phân biệt hoa thường | `1 failed` — `[chu_thuong]` |

Trả nguyên: `trả nguyên: 95de3f19fe7ed2aa → 95de3f19fe7ed2aa` *(sha256 `tools/dong_bang_sheet.py`)*.

## Luật phòng tái phạm *(`SO_PHAT_HIEN_ISP-3.1.md`)* đã áp
- `S0-R1-03` CLI từ chối **mọi** đối số ⛔ khai: `argparse.error` ⇒ `TuChoi` *(bài `[doi_so_la]`)*.
- `S0-R1-04` nguyên nhân đỏ trong **một dòng**: mọi đường exit 2 in đúng một dòng `⛔ TỪ CHỐI …` *(bài đòi `len == 1`)*.
- `S0-R1-05` dòng `[ĐẠT]`/`0 lệch` in **mẫu số**: `ô rỗng 0/185` · `khoá hỏng 0/37 dòng` · `soát PII 6/6 tên cột`; `--mong 0` và bản thô 0 dòng bị từ chối *(Đ3)*.
- `S0-R1-08` ⛔ chèn bảng nhật ký dùng chung: ⛔ chạm `08_CHANGELOG_RELEASE.md` *(lời giao)*.
- `S0-R1-09` bài ⛔ ghim tên kho: bài ⛔ nối kho. `S0-R1-01/06/10` *(DSN/cụm)*: ⛔ áp — công cụ ⛔ đọc DSN.

## Kho thật
- `KHONG_CHAM`. Công cụ ⛔ nối kho; cụm 5436 chỉ phục vụ `--duong-nen` + cổng. `FLS_CHO_GHI_THAT` ⛔ đặt.

## Cách chạy để xem
- ⛔ chạm UI. Xem ảnh: `python tools/dong_bang_sheet.py ix_fx <bản thô> --mong 37` *(in 14 dòng báo + `[ĐẠT]`)*.

## Dev tự thấy còn yếu
1. **Ảnh ↔ Drive chỉ được chứng minh NGOÀI bộ bài.** Bản thô thật ⛔ commit ⇒ bài trong repo chỉ chứng minh *"ảnh là đầu ra của công cụ trên MỘT bản thô có nội dung ấy"* *(tái tạo từ chính ảnh)*. Sự thật *"ảnh = bảng 9.2 ngày 16/11"* chỉ dựa vào phép so **222/222 ô** tôi chạy với tệp scratchpad *(`scratchpad/dt2/do_that.py`)* — R1 nên chạy lại nếu tệp còn.
2. **`doc_dan`/`doc_du` ⛔ dùng** dù ISP mục 3 kể chúng: lượt đọc ở orchestrator *(O7)*, công cụ nhận MỘT bản đọc. Bảo đảm của `doc_du` *(hai lần đọc độc lập khớp số ô có giá trị)* **⛔ có** cho ảnh này — chỉ còn phần "ô rỗng = ĐỎ" *(đo: 0/185)*. Nếu `IMPORTRANGE` ở FS2 trả ô rỗng im lặng thì chỉ bắt được dưới dạng ô rỗng.
3. **Cổng chặt hơn chữ ISP**: ISP chỉ nói exit ≠ 0 *"khi `--mong 37` lệch"*; công cụ đỏ thêm khi trùng · thiếu · khoá hỏng · ô rỗng *(lý do: AP §3.2.4 "thiếu = CHẶN", "cộng đôi"; bài trùng-bù-thiếu)*. Lạc chỉ ghi nhận. ⇒ câu hỏi Q1.
4. **Luật "lạc" là heuristic thứ tự**: dòng lạc đứng ĐẦU bảng ⛔ bị gọi lạc — dải chính kéo về nó, các tháng giữa hiện thành **thiếu** *(vẫn ĐỎ, ⛔ im lặng)*; sheet xếp **giảm dần** sẽ thành toàn lạc. Chỉ có `kieu_khoa = yyyymm`; DT3+ khoá chữ *(cây HD)* cần kiểu mới — ⛔ dựng trước *(⛔ mở rộng)*.
5. **Cổng ĐỎ vẫn GHI tệp** *(ISP B3: "ảnh vẫn ghi")* — chạy với `--ra` mặc định mà cổng đỏ sẽ **ghi đè ảnh đã commit**. Lưới đỡ **đã đo**: chạy công cụ trên bản thô thật với `--mong 36` vào đường mặc định ⇒ `[ĐỎ] cổng --mong 36: 37 dòng ≠ mong 36 …` exit 1, `git status` = ` M tests/fixture/cau_hinh/ix_fx.json`, bộ bài ⇒ `1 failed, 19 passed` — **CHỈ** `test_DT2_B1_anh_IX_FX_TAI_TAO_dung_tung_byte_tu_cong_cu` bắt *(dòng ảnh ⛔ đổi nên checksum ghim + bài nội dung vẫn xanh; chỉ khối `cong` đổi)*; trả nguyên `git checkout` ⇒ sha256 `e2c9fdd028bd3286`. ⇒ ⛔ lọt im lặng, nhưng an toàn treo trên **một** bài.
6. **Riêng tư chỉ soát TÊN cột**, ⛔ soát giá trị: một email gõ nhầm vào ô USD sẽ qua cổng PII *(nhưng thành ô số hỏng mà C1 sẽ bắt)*. Spec chỉ đòi tên cột.
7. `nguon` mang **id Drive đầy đủ** của FS2 *(ghi đúng như bản thô)*. Tiền lệ: `fls/oracle/nguon.py:36/44/55` commit id đầy đủ; nhưng `pm_join.json` cắt `1md85t…` ⇒ câu hỏi Q4.
8. `checksum_noi_dung` là **16 hex** *(64 bit — khuôn `pm_join.json`)*: đủ để phát hiện đổi, ⛔ phải bảo đảm toàn vẹn mật mã.
9. Giá trị ảnh là **chuỗi** *(đúng chữ số)* và khoá giữ tên nguồn `Month` — hợp đồng C1 dùng `yyyymm` + số ⇒ C5 phải ánh xạ `Month → yyyymm` và đọc bằng `Decimal` *(Q3)*.
10. `tests/du_lieu/__init__.py` trùng tệp DT1a tạo — cùng 0 byte nên `add/add` gộp sạch theo lý thuyết; **⛔ thử gộp thật**.
11. `kiem_so_song` ⛔ chạy được ở container *(như `BG-066` ⑥)*.

## Câu hỏi cho orchestrator *(đều `KHONG_CHAN` — đã làm theo khuyến nghị, đổi được trong vòng R)*
- **Q1 · độ chặt của cổng.** ⓐ *(đang làm)* đỏ khi `--mong` lệch **hoặc** trùng/thiếu/khoá hỏng/ô rỗng; lạc ghi nhận — giá: chặt hơn chữ ISP. ⓑ chỉ `--mong` đỏ, còn lại liệt kê — giá: 37 dòng có trùng bù thiếu XANH *(đúng ca "cộng đôi")*. **Khuyến nghị ⓐ.**
- **Q2 · `ngay_dong_bang`.** ⓐ *(đang làm)* = `doc_luc` của bản thô — giá: ⛔ ghi ngày chạy công cụ; được: tái tạo đúng từng byte. ⓑ ngày chạy + trường `ngay_doc` riêng — giá: tệp đổi mỗi ngày dù nội dung y hệt, mất phép so byte. **Khuyến nghị ⓐ.**
- **Q3 · khoá `Month` ↔ `yyyymm` của C1.** ⓐ *(đang làm)* ảnh giữ tên nguồn, C5 ánh xạ — giá: một bước ánh xạ ở C5. ⓑ khuôn đổi tên cột khi đóng băng — giá: ảnh ⛔ còn "đúng nguồn", thêm khái niệm đổi tên vào công cụ. **Khuyến nghị ⓐ.**
- **Q4 · id Drive trong `nguon`.** ⓐ *(đang làm)* giữ đầy đủ như bản thô *(tiền lệ `nguon.py`)* — giá: id FS2 lên origin khi gộp. ⓑ cắt như `pm_join.json` — giá: mất truy vết chính xác. **Khuyến nghị ⓐ**, trừ khi owner coi id FS2 là nhạy cảm.
- **Ghi nhận cho `fls-ba`** *(⛔ việc bước này)*: AP §3.2.4 viết *"2026 điền sẵn 26.200"* — ảnh đo **10/12** tháng 2026 là `26200` *(`202601` = `25500` · `202602` = `26000`)*; *"2024 một giá cả năm"* đúng *(1 giá USD / 12 dòng)*; *"07–12/2025 cố định 25.500"* đúng *(6/6)*; VND = `1` trên **37/37** dòng.

## Sha
- mã: `isp/DT2` @ `3902623` *(cục bộ)* · nền `329fa68`
- `tools/dong_bang_sheet.py` sha256 `95de3f19fe7ed2aa…` · `tests/fixture/cau_hinh/ix_fx.json` sha256 `e2c9fdd028bd3286…` · `checksum_noi_dung` `b6d1f9e9074951f1`
