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

---

## Vòng sửa sau R1 (`KQ-087`) *(CHỈ THÊM — mọi mục trên giữ nguyên làm biên bản của `3902623`)*

| | |
|---|---|
| **Thuộc** | `WO-085` · vòng sửa sau R1 `KQ-087` *(9 phát hiện: 3 NÊN SỬA · 6 GHI NHẬN)* + **một việc thêm** của orchestrator *(tách khuôn — nhắn giữa lượt)* |
| **Phát bởi** | `fls-dev` *(làn DATA, phiên mới)* · 2026-11-16 · orchestrator giao |
| **Commit** | `isp/DT2` @ **`7ec2862`** *(mã + bài)* trên `eb94901` *(orchestrator gộp `isp/C1` để có `fls/cau_hinh/fx.py`)*; mục này ở commit kế tiếp *(chỉ giấy)*. ⛔ đẩy, ⛔ gộp |
| **Cụm** | **5446** *(`PG_DSN=…:5446/fls` · `PG_DSN_TEST=…:5446/fls_test` · `PYTHONUTF8=1`)* — container khởi động lại giữa lượt, orchestrator bật lại cụm; lượt đỏ chạy TRƯỚC khi khởi động lại, mọi lượt xanh SAU |
| **Quyết định orchestrator đã áp** | `DT2-R1-03`: **một** định nghĩa `lac`/`thieu` — của C1 *(`fls/cau_hinh/fx.py`, theo `thang_dau`)*, khuôn `ix_fx` GỌI `kiem` *(import)*, `thang_dau = 202401` khai một chỗ trong khuôn · `DT2-R1-07`: **chấp nhận** *(lượt đọc ở O7; thăm dò khả năng đọc ở `TIEN_DO.md`)* · **tách khuôn**: mỗi khuôn một tệp `tools/khuon_dong_bang/<tên>.py`, `__init__.py` 0 byte, công cụ tìm theo tên |
| **Tệp chạm** | `tools/dong_bang_sheet.py` *(382 → 538 dòng)* · `tools/khuon_dong_bang/__init__.py` *(mới, 0 byte)* · `tools/khuon_dong_bang/ix_fx.py` *(mới, 76 dòng)* · `tests/du_lieu/test_dong_bang_sheet.py` *(389 → 925 dòng; **20 → 63** bài)* · phiếu này. `tests/fixture/cau_hinh/ix_fx.json` **⛔ đổi** *(xem "Ảnh")*. ⛔ chạm `fls/cau_hinh/**` *(chỉ import)* |

### Phát hiện → sửa gì → bằng chứng *(ĐỎ đo trên `eb94901` trước mã · XANH đo trên `7ec2862`)*

| F | Kết | Sửa gì | ĐỎ trước mã | XANH sau mã | Tệp:dòng |
|---|---|---|---|---|---|
| `DT2-R1-01` | **đã sửa** | Cổng ĐỎ mà ⛔ `--ra` ⇒ ảnh đỏ ghi ra tệp **CẠNH** `<ra>.DO.json`, ⛔ đè ảnh ở đường mặc định. Có `--ra` ⇒ ghi ở `--ra` *(ISP B3 "ảnh vẫn ghi đúng nguồn" giữ)*. Lượt ĐẠT ⛔ `--ra` ⇒ đường mặc định *(lệnh ISP)*. **Vì sao chọn "tệp cạnh", ⛔ "⛔ ghi"**: giữ exit 1 **một** nghĩa — *"cổng ĐỎ, ảnh đỏ ĐÃ ghi"*, dòng `ghi :` nói ở đâu; chọn "⛔ ghi" thì exit 1 tách hai nghĩa *(có `--ra` thì ghi, ⛔ thì ⛔)*. Bài nội dung ảnh commit giờ đòi cả `cong` | `test_R1_01_cong_DO_…`: `AssertionError: lượt ĐỎ ⛔ --ra đã ĐÈ ảnh ở đường mặc định` · `assert '2b5d04f0a1b0...' == 'e2c9fdd028bd...'`. **Bản thô thật** `--mong 36` ⛔ `--ra`, cây tạm `git archive eb94901`: `exit=1 · sha256 ảnh trước=e2c9fdd028bd3286 sau=2b5d04f0a1b07133` | 3 bài xanh *(`…_cong_DO_…` · `…_cong_DAT_…_KHONG_tep_DO` · `…01b_anh_da_commit_mang_cong_DAT`)*. **Bản thô thật**, cùng lệnh, cây mới: `exit=1 · sha256 ảnh trước=e2c9fdd028bd3286 sau=e2c9fdd028bd3286 · tệp cạnh: ix_fx.DO.json` | `tools/dong_bang_sheet.py:508-516` · bài `:468` · `:498` · `:511` |
| `DT2-R1-02` | **đã sửa** | ① `_o`: ô **CHUỖI** ⇒ `{"chu": "…"}`; ô số giữ *chuỗi đúng chữ số* ⇒ ảnh SẠCH ⛔ đổi byte, ảnh có ô chữ thì ô chữ ⛔ lẫn được với ô số. ② Cổng thêm **`ô ⛔ số k/N`** *(chữ có nội dung, hoặc `bool`, ở cột chọn; `rỗng ∩ ⛔ số = ∅` — ô chỉ-khoảng-trắng vẫn là RỖNG)*. ③ Khoá `Month` phải **ô SỐ** 6 chữ số, tháng 01–12 — `{"chu": "202401"}` là khoá hỏng; dòng báo đếm `chữ k`. ④ Bên nhận C1 chạy được trên chính ảnh: bài tự ánh xạ `Month → yyyymm` rồi gọi `kiem` | 6 bài ĐỎ: `[hien_thi_formattedValue]` *(`"20,692"`)* · `[so_go_thanh_chu]` *(`"20691.51"`)* · `[khoang_trang_dau]` · `[bool]` — `assert 0 == 1` *(exit 0)*; `…khoa_Month_CHU…` `assert 0 == 1`; `…kiem_C1_chay_TREN_CHINH_ANH…` `Failed: DID NOT RAISE LoiFX` *(ảnh cũ ghi ô chữ `"20691.51"` y hệt ô số ⇒ C1 NHẬN)* | xanh. **Bản sao bản thô thật** SGD `202507` = `"20,692"` ⇒ exit 1 · `ô ⛔ số: 1/185 (chữ/bool ở cột chọn) [dòng 19 · SGD]`; `Month` toàn chuỗi ⇒ exit 1 · `khoá hỏng: [202401, …]` 37/37 · C1 *(qua khuôn)* `37 lỗi: dòng 1 ({'chu': '202401'}): yyyymm ⛔ đúng khuôn yyyymm …` | `tools/dong_bang_sheet.py:197-225` · `:269-272` · `:364-365` · bài `:527` · `:548` · `:567` |
| `DT2-R1-03` | **đã sửa** *(quyết định orchestrator)* | Công cụ **⛔ còn** định nghĩa thiếu/lạc nào *(gỡ luật "theo thứ tự sheet"; bia ở docstring)*. Khuôn `ix_fx` gọi **chính** `fls.cau_hinh.fx.kiem` *(import — bài đòi `m.kiem is fx.kiem`)*; `THANG_DAU = 202401` khai **một chỗ** kèm căn cứ AP §3.2.1 *"37 dòng 202401 → 202612 (kể cả dòng lạc 202306)"*. C1 từ chối cả bảng *(vd `VND = 2`)* ⇒ thiếu/lạc **⛔ đo được** ⇒ ảnh ghi `thieu = lac = null` *(⛔ `[]`)*, cổng ĐỎ `thiếu/lạc ⛔ đo được — <lời C1>` *(Đ5)* | 5 bài ĐỎ: `[doi_cho_202401_202402]` `assert ([], ['202401', '202306']) == ([], ['202306'])` · `[dong_lac_dung_DAU]` exit 1 *(6 tháng thiếu giả)* · `[202405_xuong_CUOI]` `['202306', '202405'] != ['202306']` · `…C1_tu_choi_bang…` `assert 0 == 1` *(VND = 2 qua cổng — R1 ⑭)* · `…KHAI_thang_dau…` `FileNotFoundError …/tools/khuon_dong_bang/ix_fx.py` | xanh; mỗi ca đòi thêm `(thieu, lac)` **bằng** `kiem` của C1 chạy trên chính ảnh. **Bản sao bản thô thật**: đổi chỗ `202401`/`202402` ⇒ exit 0 `thiếu: []` `lạc: [202306]`; dòng lạc lên ĐẦU ⇒ exit 0, `thiếu: []` `lạc: [202306]`; `VND = 2` ở `202406` ⇒ exit 1 `thiếu: ⛔ ĐO ĐƯỢC — kiem của C1 (fls/cau_hinh/fx.py) từ chối bảng — 1 lỗi: dòng 6 (202406): VND=2 ⛔ = 1` | `tools/khuon_dong_bang/ix_fx.py:40` · `:54` · `:60-76` · `tools/dong_bang_sheet.py:285-301` · `:366-367` · bài `:591` · `:611` · `:621` |
| `DT2-R1-04` | **đã sửa** | Thêm bài cho **từng** chốt phụ: mỗi đường TỪ CHỐI đòi exit 2 + đúng **một** dòng + dòng ấy nói **đúng lý do** *(`phai_noi`)* — nhờ vậy D11 *(`parse_constant`)* ⛔ còn núp sau D8 *(`_o` từ chối `float`)*; ô chỉ-khoảng-trắng; D12 canh trên **lỗi I/O thật** *(`RLIMIT_FSIZE` = 2048 byte < ảnh, đo ảnh đối chứng trước — Đ3)* | R1: 14 đột biến, bộ 20 bài bắt 3, **sống 11** *(D1–D8 · D10 · D11 · D12)* | **32** đột biến trên cây tạm *(D1–D14 theo R1 — D10 thay bằng D10a/b/c cho luật mới, D5 tách D5/D5b — + N1–N15 cho mọi thứ mới của vòng này)* ⇒ **chết 32 · sống 0** *(log ở "Cổng chạy lại")* | bài `:665` *(12 ca)* · `:683` · `:710` |
| `DT2-R1-05` | **đã sửa** | `OSError` khi ghi ⇒ **exit 3**, đúng một dòng `⛔ LỖI GHI: <Kiểu>: …`, ⛔ traceback, ⛔ ảnh mới *(ghi nguyên tử, tệp cũ giữ)*. Khuôn nổ *(lỗi lập trình, ⛔ `ValueError`)* ⇒ exit 3, traceback GIỮ để sửa khuôn + dòng cuối `⛔ LỖI`. Đọc bản thô lỗi I/O / giải mã ⇒ TỪ CHỐI exit 2 *(⛔ ghi gì)*. Bảng exit ở docstring: 0 · 1 · 2 · **3** | `…ra_la_THU_MUC…` `AssertionError: (1, 'Traceback …')` `assert 1 == 3`; `…D12_dia_DAY…` `(1, '', 'Traceback …')` *(bản cũ: traceback `File too large`, exit 1 — đúng mã "cổng ĐỎ, ảnh đã ghi" trong khi ⛔ tệp nào được ghi)* | xanh. **Bản sao bản thô thật** `--ra <thư mục>` ⇒ `exit 3 · tệp ra không` · `⛔ LỖI GHI: IsADirectoryError: [Errno 21] Is a directory: …` | `tools/dong_bang_sheet.py:228-235` · `:445-460` · `:502-506` · `:518-524` · bài `:696` · `:710` · `:894` |
| `DT2-R1-06` | **đã sửa** | `doc_luc` phải khớp `\d{4}-\d{2}-\d{2}` **và** là ngày có thật *(`date.fromisoformat`)*; `ngay_dong_bang` = `date.fromisoformat(doc_luc).isoformat()` | `[tuan_ISO]` *(`2026-W46-1`)* · `[ISO_gon]` *(`20261116`)* — `assert 0 == 2` *(exit 0)*; ba ca `co_gio` · `ngay_khong_co` · `kieu_VN` xanh sẵn *(chốt cũ, giữ để canh)* | xanh ×5. **Bản sao bản thô thật**: ``⛔ TỪ CHỐI: `doc_luc` ⛔ phải ngày YYYY-MM-DD có thật: '2026-W46-1'`` · `… '20261116'` — exit 2, ⛔ tệp | `tools/dong_bang_sheet.py:243-249` · `:372` · bài `:752` |
| `DT2-R1-07` | **chấp nhận** *(orchestrator)* | ⛔ sửa — `doc_dan`/`doc_du`/`do_kha_nang_doc` thuộc lượt đọc ở orchestrator *(O7)*; thăm dò khả năng đọc đã ghi ở `TIEN_DO.md` | — | — | — |
| `DT2-R1-08` | **đã sửa** | Cột tiêu đề **RỖNG** mà ô có giá trị ⇒ **TỪ CHỐI** exit 2 *(cùng luật "dòng dài hơn tiêu đề"; thêm lý do: cột ⛔ tên thì ⛔ soát riêng tư THEO TÊN được)* — ⛔ in giá trị ô. Cột tiêu đề rỗng mà mọi ô rỗng ⇒ nhận. Dòng báo có nhãn và **cộng lại** *(Đ4)*: `bản thô : N cột tiêu đề = khoá 1 + chọn k + ⛔ chọn m + tiêu đề rỗng r · D dòng`. `khong_mang_PII` thêm một mệnh đề **chỉ khi** r > 0 ⇒ ảnh commit *(r = 0)* giữ từng chữ | `…CO_du_lieu_thi_TU_CHOI` `assert 0 == 2` *(exit 0)*; `…MOI_O_RONG…` `assert None` *(dòng báo cũ `7 cột` ⛔ nhãn)* | xanh: `8 cột tiêu đề = khoá 1 + chọn 5 + ⛔ chọn 1 + tiêu đề rỗng 1` *(8 = 1+5+1+1)*. **Bản sao bản thô thật** + cột `""` mang chữ ⇒ exit 2 · `⛔ TỪ CHỐI: dòng 1: cột tiêu đề rỗng ở vị trí [7] mà ô có giá trị …`; bản thô nguyên ⇒ `6 cột tiêu đề = khoá 1 + chọn 5 + ⛔ chọn 0 + tiêu đề rỗng 0 · 37 dòng` | `tools/dong_bang_sheet.py:324-339` · `:376-388` · `:420-422` · bài `:767` · `:783` |
| `DT2-R1-09` | **đính chính** *(mục dưới)* | ⛔ sửa câu cũ *(biên bản)* — đính chính bằng số đo mới | — | — | phiếu này |
| **Việc thêm** *(orchestrator)* | **đã làm** | Khuôn = **một tệp** `tools/khuon_dong_bang/<tên>.py`; gói có `__init__.py` **0 byte**. Công cụ: `danh_sach_khuon()` quét thư mục *(= lựa chọn của dòng lệnh — khuôn lạ ⇒ TỪ CHỐI như cũ)*; `nap_khuon()` nạp theo **đường tệp** *(⛔ phụ thuộc `sys.path`)* và kiểm **giao kèo** `BANG · KHOA · KIEU_KHOA · COT · RA · thieu_lac()` ⇒ thiếu/sai/cú pháp hỏng ⇒ TỪ CHỐI một dòng nói tên khuôn. Khuôn nhận **bản sao** dòng ảnh *(⛔ sửa được ảnh)*. Mã công cụ ⛔ còn hằng khuôn nào *(bài quét AST: `IX.FX` · `Month` · `USD` · `VND` · đường ảnh = 0)*. Bước sau chỉ THÊM một tệp | 7 bài ĐỎ: `…la_mot_tep…` `FileNotFoundError …/tools/khuon_dong_bang/__init__.py`; 6 bài `AttributeError: <module 'dong_bang_sheet_bai' …> has no attribute 'THU_MUC_KHUON'` *(đỏ vì THIẾU chỗ cắm — bài gọi trong tiến trình)* | xanh: khuôn GIẢ `gia.py` ở thư mục tạm ⇒ `danh_sach_khuon() == ['gia']`, lệnh `gia … --mong 3` exit 0, ảnh theo khuôn ấy; sha256 công cụ trước = sau | `tools/dong_bang_sheet.py:112-190` · `tools/khuon_dong_bang/ix_fx.py` · bài `:817` · `:854` · `:881` · `:894` · `:910` |

### Đính chính `DT2-R1-09`
Substep 1 ② ở trên viết *"`tests/du_lieu/__init__.py` (0 byte, quy ước repo — **12 thư mục `tests/*`** có nó)"*. Đo lại 16/11 *(`git ls-tree -r --name-only <rev> tests`)*:

| Rev | Tệp `__init__.py` dưới `tests/` | trong đó `tests/__init__.py` | Thư mục con trực tiếp | …có `__init__.py` | …⛔ có |
|---|---|---|---|---|---|
| `329fa68` *(nền của BG)* | **12** | 1 | 14 | **11** | `api` · `fixture` · `golden` |
| `eb94901` | 14 | 1 | 16 | 13 *(+ `du_lieu` · `cau_hinh`)* | `api` · `fixture` · `golden` |

⇒ số `12` đúng, **nhãn sai**: 12 **tệp** = `tests/` + 11/14 thư mục con — ⛔ *"12 thư mục"* *(Đ4)*. Câu cũ giữ nguyên làm biên bản.

### Ảnh `tests/fixture/cau_hinh/ix_fx.json` — **⛔ đổi byte nào**
- sha256 **`e2c9fdd028bd32863b030c7d9252d13ae6b23cc0a2213fb400b4bf9d87e48c39`** *(= ảnh commit `3902623`)* · `checksum_noi_dung` **`b6d1f9e9074951f1`** *(= ghim `CHECKSUM_ANH_IX_FX`)* · `git diff eb94901..7ec2862 -- tests/fixture/` **rỗng**.
- Vì sao ⛔ phải đổi: ô SỐ ghi như cũ *(chỉ ô CHỮ được bọc — bản thô thật có **0/222** ô chữ)*; `lac`/`thieu` của C1 *(số nguyên)* trả về **chuỗi** cùng biểu diễn với `Month` của ảnh *(tra ngược được)*; `khong_mang_PII` chỉ thêm mệnh đề khi có cột tiêu đề rỗng *(bản thô thật: 0)*.
- Chứng minh: công cụ mới trên bản thô thật, `--ra` vào thư mục tạm, **2 lượt** ⇒ `exit=0` ×2 · sha256 ×2 = ảnh commit · `cmp x2: byte-identical`.

### Cổng chạy lại *(mục 5 của lời giao — cụm 5446, venv `/home/user/FLS-tobe/.venv`, log `scratchpad/data_dt2_sua/`)*
| Lệnh | Kết quả nguyên văn |
|---|---|
| ĐỎ trước mã: `pytest tests/du_lieu/test_dong_bang_sheet.py -rA` *(bài mới + công cụ `eb94901`)* | exit 1 · `26 failed, 37 passed in 5.55s` — 26 ĐỎ = 26 bài mới chứng minh thiếu hành vi *(lý do từng bài ở bảng trên — ⛔ lỗi cú pháp/setup)*; 37 xanh = 20 bài cũ + 17 bài canh chốt CÓ SẴN *(12 ca R1-04 · 3 ca R1-06 · `…01b…` · `…cong_DAT_…`)* — chúng đỏ trên đột biến, ⛔ trên bản cũ |
| `pytest tests/du_lieu/test_dong_bang_sheet.py tests/cau_hinh/test_fx.py` | exit 0 · `85 passed in 4.43s` *(mẫu số `--collect-only`: `63 tests collected` + `22 tests collected`)* |
| công cụ trên **bản thô thật** `ix_fx <bản thô> --mong 37 --ra <tạm>` ×2 | `that lan1 exit=0 sha256=e2c9fdd0…48c39` · `that lan2 exit=0 sha256=e2c9fdd0…48c39` · `anh commit sha256=e2c9fdd0…48c39` · `cmp x2: byte-identical` · `[ĐẠT] cổng --mong 37: 37 dòng = mong · trùng 0 · thiếu 0 · khoá hỏng 0 · ô rỗng 0/185 · ô ⛔ số 0/185` · `thiếu: []  (dải 202401→202612 · thang_dau 202401 của khuôn · kiem của C1)` · `lạc: [202306]` · `checksum_noi_dung: b6d1f9e9074951f1` |
| đột biến *(`scratchpad/data_dt2_sua/dot_bien.py`, cây tạm, mỗi mẫu khớp đúng 1 lần)* | `đối chứng (⛔ đột biến): 63 passed` · … · `TỔNG: 32 đột biến · chết 32 · sống 0 []` · `trả nguyên: tools/dong_bang_sheet.py b0827a75de05cb24 → b0827a75de05cb24 · tools/khuon_dong_bang/ix_fx.py 14e6b782f92c2c14 → 14e6b782f92c2c14` |
| 17 bài đề xuất của R1 trên mã mới *(cây tạm)* | `2 failed, 15 passed` — đỏ **có chủ đích**: `test_R1_01_…` gọi bảng `KHUON` đã gỡ *(`AttributeError: … has no attribute 'KHUON'`; ý định giữ ở `test_R1_01_cong_DO_…` của tôi)* · `test_R1_04c_…` đòi `lạc: [202306, 202405]` theo luật thứ tự sheet đã BỎ *(`DT2-R1-03`; ca ngược lại ở `[202405_xuong_CUOI]`)* |
| `lint-imports` | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `bash tools/dung_moi_truong_isp.sh --cong 5446 --duong-nen` · **lượt 1** *(cây làm việc = `7ec2862` trước commit, cùng mã)* | exit 0 · `[ĐẠT]` ×7 kiểm môi trường *(`26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `Contracts: 11 kept, 0 broken.` · `chay 9845 / co 9967` · `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2525 passed, 2 xfailed, 14 errors in 322.21s (0:05:22)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 190.17s (0:03:10)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong`. Mẫu số: `2553 tests collected` = 12 + 2525 + 2 + 14 *(2480 của BG + 43 bài mới DT2 + 30 bài gộp từ `isp/C1` — `--collect-only` trên `tests/cau_hinh/test_fx.py` + `tests/api/test_isp_config_fx.py` = `30 tests collected`)*; `tests/du_lieu` trong tập đỏ **0**; hai bài chập chờn `test_wo032_man_cua_that.py::test_AC3_…/::test_AC7_…` **⛔ đỏ** *(grep `FAILED`/`ERROR` = 0)* |
| `… --duong-nen` · **lượt 2** *(trên `7ec2862`)* | exit 0 · HEAD `7ec2862`, `git status` sạch · `[ĐẠT]` ×7 kiểm môi trường *(như lượt 1)* · toàn bộ `12 failed, 2525 passed, 2 xfailed, 14 errors in 335.11s (0:05:35)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 186.33s (0:03:06)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` *(9 dòng `[ĐẠT]` · 0 `[ĐỎ]`)*. `skipped`/`deselected` **0** cả hai log; `tests/du_lieu` trong tập đỏ **0**; hai bài chập chờn `wo032_man_cua_that` **⛔ đỏ** *(grep = 0 · 0)* — ⛔ cần chạy lại riêng |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 41 tuyen` *(41 = 40 của BG + `GET /config/fx` gộp từ `isp/C1`)* |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` *(⛔ chạm schema)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — trùng nguyên văn đường nền *(log R1 `r1_dt2/khop.log`: cùng dòng tổng, cùng B3 · B4 · C5 · C5b KHONG DO DUOC, A1 · B1 · C6 DOI TRANG THAI, cùng dòng `khoi trong lo trinh LECH`)*; công cụ chỉ đọc `docs/**.md` + kho ⇒ vòng này ⛔ chạm được nó |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (178 file, 1875 bang, 726 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(đo SAU khi nối mục này; R1 đo `174 file, 1853 bang` trước `KQ-087` + sổ DT2 và trước gộp `isp/C1`)* |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-dt2/.venv/Scripts/lint-imports.exe'` *(gọi cứng đường Windows — y hệt BG ⑪ · R1)* |

### Dev tự thấy còn yếu *(vòng sửa)*
1. **Hệ quả của `DT2-R1-03` làm cổng CHẶT hơn R1 ⑭.** `VND = 2` *(hay bất kỳ dòng nào C1 từ chối)* giờ là **ĐỎ** *(thiếu/lạc ⛔ đo được)*, trong khi R1 ghi ⑭ *"exit 0 — đúng phân vai"*. Lý do: `kiem` của C1 là API duy nhất mang định nghĩa thiếu/lạc, và nó từ chối cả bảng. Tôi ⛔ viết lại luật nào của C1 — nhưng cổng DT2 giờ **gián tiếp** mang luật nghiệp vụ của C1 *(⇒ câu hỏi Q5)*.
2. **D12 chỉ canh được trên hệ có `resource`** *(Linux/macOS)*. Máy owner chạy Windows ⇒ bài `…D12_dia_DAY…` **bỏ qua** ở đó; ghi nguyên tử chỉ được canh ở container. Lượt này `skipped = 0` *(Linux)*.
3. **Tệp `.DO.json` ⛔ được gitignore.** Lượt đỏ ⛔ `--ra` để lại `tests/fixture/cau_hinh/ix_fx.DO.json` *(tệp chưa theo dõi — hiện ở `git status`, nhưng `git add -A` sẽ cuốn vào)*. Lượt ĐẠT sau ⛔ dọn tệp `.DO` cũ. `.gitignore` ngoài quyền lượt này ⇒ Q6.
4. **Khuôn là MÃ chạy được.** `nap_khuon` thực thi mọi `tools/khuon_dong_bang/<tên>.py` có tên `[a-z][a-z0-9_]*` — tin thư mục repo như tin `tools/`. Khuôn nạp lỗi ⇒ TỪ CHỐI *(exit 2)*; khuôn nổ lúc chạy ⇒ exit 3; khuôn `raise ValueError` vì lỗi lập trình sẽ **giả** thành "⛔ đo được" *(vẫn ĐỎ, vẫn in lời — ⛔ im lặng)*.
5. **Phụ thuộc C1 qua import.** Khuôn `ix_fx` đọc `fls/cau_hinh/fx.py` từ `isp/C1` đã gộp ở `eb94901`. C1 đổi chữ ký `kiem`/`LoiFX` ở R2/R3 ⇒ khuôn nạp lỗi *(exit 2, ⛔ im lặng)* — nhưng `isp/DT2` phải gộp lại C1 mới thấy.
6. **Dòng báo hiện khoá chữ ⛔ nháy**: `khoá hỏng: [202401, …]` — kiểu chỉ thấy qua số đếm `(37/37 dòng · chữ 37)` và trong JSON ảnh *(`{"chu": …}`)*. Giữ ⛔ nháy vì bài cũ `[khoa_hong]` đòi nguyên cụm `khoá hỏng: [2024-04]` ⇒ ⛔ sửa bài cũ cho xanh.
7. **Lời C1 trong `cong.ly_do` dài**: khuôn cắt về 3 lỗi đầu + `…` *(37 lỗi khi `Month` toàn chữ)*; danh sách đủ chỉ có khi chạy `kiem` lại.
8. **Bài trong tiến trình vá biến module** `GOC` · `THU_MUC_KHUON` *(như bài đề xuất R1)* — gắn với tên nội bộ; đổi tên là bài đỏ *(ồn, ⛔ im)*.
9. `kiem_so_song` vẫn ⛔ chạy được ở container *(như BG ⑪)*.

### Câu hỏi cho orchestrator *(đều `KHONG_CHAN` — đã làm theo khuyến nghị)*
- **Q5 · C1 từ chối bảng ⇒ cổng DT2 ĐỎ?** ⓐ *(đang làm)* ĐỎ, `thieu = lac = null` — giá: cổng DT2 mang gián tiếp luật nghiệp vụ C1 *(VND = 1, tỷ giá > 0)*, trái chữ R1 ⑭; được: ảnh "ĐẠT" thì C1 **chắc chắn** nạp được *(luật phòng tái phạm `DT2-R1-02`)* và Đ5 *"⛔ đo được là ĐỎ"*. ⓑ C1 tách một hàm thuần `phan_tich_thang(thang, thang_dau)` để DT2 đo thiếu/lạc **độc lập** tính hợp lệ của dòng — giá: sửa làn BE-CF *(ngoài quyền tôi)* + một API nữa. **Khuyến nghị ⓐ.**
- **Q6 · `.DO.json`.** ⓐ orchestrator thêm `tests/fixture/**/*.DO.json` vào `.gitignore` — giá: một dòng ở tệp dùng chung. ⓑ để vậy — giá: lỡ `git add -A` là commit ảnh đỏ. **Khuyến nghị ⓐ.**
- **Q7 · Hợp đồng ô chữ cho C5.** Ảnh giờ có hai dạng ô: chuỗi đúng chữ số *(số)* và `{"chu": …}` *(chữ)*. C5 nạp ảnh **ĐẠT** thì ⛔ gặp dạng thứ hai *(cổng chặn)*; xin ghi vào `WO` của C5: *"ô `{"chu": …}` ⇒ từ chối"* — hoặc C5 chỉ nhận ảnh có `cong.dat = true`. **Khuyến nghị**: C5 đòi `cong.dat = true` *(một chốt)*.

## Vòng sửa sau R2 (`KQ-088`) *(CHỈ THÊM — mọi mục trên giữ nguyên làm biên bản của `3902623` · `7ec2862`)*

| | |
|---|---|
| **Thuộc** | `WO-085` · vòng sửa sau R2 `KQ-088` *(2 NÊN SỬA `DT2-R2-01` · `-02` + 4 GHI NHẬN `-03` … `-06`)* |
| **Phát bởi** | `fls-dev` *(làn DATA, phiên mới)* · 2026-11-17 · orchestrator giao |
| **Commit** | `isp/DT2` @ **`f3f2240`** *(mã + bài)* trên `8e2fc95` *(KQ-088)*; mục này ở commit kế tiếp *(chỉ giấy)*. ⛔ đẩy, ⛔ gộp |
| **Nối tiếp WIP** | Vòng này nối tiếp commit tạm **`5e962d7`** *("WIP … DỪNG GIỮA CHỪNG", phiên trước dừng vì chuyển account)*. Phiên này ⛔ tin phần WIP: đọc lại `git diff 8e2fc95 5e962d7`, chạy lại mọi bài, chứng minh lại ĐỎ-trước trên `8e2fc95`, dựng lại + chạy lại đột biến *(log đột biến của vòng R1 và của WIP mất cùng scratchpad cũ)*, rồi `git reset --soft 8e2fc95` và commit sạch. Phiên này thêm so với WIP: gỡ `sys.modules` cả khi **sai giao kèo** *(bài mới ĐỎ trên `5e962d7`)*, ca `M9_COT_rong`, bài `cong.ly_do` nêu đúng nguyên nhân *(4 đột biến cổng sống — xem dưới)* |
| **Cụm** | **5436** *(`PG_DSN=…:5436/fls` · `PG_DSN_TEST=…:5436/fls_test` · `PYTHONUTF8=1`)* · venv `/home/user/FLS-tobe/.venv` · log `scratchpad/data_dt2_sua_r2/` |
| **Tệp chạm** | `tools/dong_bang_sheet.py` *(538 → 561 dòng; mã thực thi đổi ≈ 11 dòng, còn lại chú thích/docstring)* · `tests/du_lieu/test_dong_bang_sheet.py` *(925 → 1212 dòng; **63 → 88** bài)* · phiếu này. Ảnh `tests/fixture/cau_hinh/ix_fx.json` **⛔ đổi** · khuôn `tools/khuon_dong_bang/ix_fx.py` **⛔ đổi** · ⛔ chạm `fls/**` |

### Phát hiện → sửa gì → bằng chứng *(ĐỎ đo trên `8e2fc95` trước mã · XANH đo trên `f3f2240`)*

| F | Kết | Sửa gì | ĐỎ trước mã | XANH sau mã | Tệp:dòng |
|---|---|---|---|---|---|
| `DT2-R2-01` *(NÊN SỬA)* | **đã sửa** | `nap_khuon`: `sys.modules[spec.name] = m` **trước** `exec_module`; `pop` khi nạp lỗi **và** khi sai giao kèo *(khuôn bị khước từ ⛔ nằm lại cho lần nạp/bài sau)* | `test_R2_01_khuon_co_dataclass…`: ``AssertionError: ⛔ TỪ CHỐI: khuôn `gia_dc` (gia_dc.py) nạp lỗi: AttributeError: 'NoneType' object has no attribute '__dict__'`` · `assert 2 == 0`. `test_R2_01_khuon_SAI_GIAO_KEO…` ĐỎ trên WIP `5e962d7`: `assert {'khuon_dong_…sai_giao_keo'} == set()` *(xanh sẵn trên `8e2fc95` — khi ấy ⛔ đăng ký gì)*. Khuôn `@dataclass` đặt THẬT vào `tools/khuon_dong_bang/` của cây `8e2fc95` ⇒ bài tham số hoá `[zz_dc]` ĐỎ `Failed: khuôn zz_dc bị TỪ CHỐI … AttributeError` | 3 bài xanh *(`…dataclass…NAP_DUOC` — khuôn chạy được `typing.get_type_hints` lúc CHẠY, module còn ở `sys.modules` · `…NAP_LOI…` · `…SAI_GIAO_KEO…`)*; cùng khuôn `zz_dc` trên mã mới ⇒ `3 passed` | `tools/dong_bang_sheet.py:174` · `:178` · `:200` · bài `:978` · `:1001` · `:1020` |
| `DT2-R2-02` *(NÊN SỬA)* | **đã sửa** | Bài khuôn đòi `"ix_fx" in danh_sach_khuon()` **và** tập = glob ĐỘC LẬP của bài *(`*.py` trừ `_…`)* — lo gốc giữ: ⛔ bỏ sót tệp, ⛔ thấy tệp ⛔ có. Thêm bài **tham số hoá trên `danh_sach_khuon()`** *(lấy lúc thu thập, ⛔ danh sách gõ tay)*: mỗi khuôn có mặt ⇒ qua `nap_khuon` + bài tự kiểm ĐỘC LẬP từng điều khoản *(`bang/khoa/ra` chuỗi khác rỗng · `kieu_khoa ∈ KIEU_KHOA_BIET` của chính công cụ · `cot` tuple chuỗi khác rỗng · khoá + cột đôi một khác tên · `RA` tương đối · `thieu_lac` gọi được)*. Tập rỗng ⇒ ca `RONG` **ĐỎ**, ⛔ `skipped` *(Đ3)* | Cây `8e2fc95` + bài CŨ + tệp khuôn `zz_gia.py` ⇒ `AssertionError: assert ['ix_fx', 'zz_gia'] == ['ix_fx']` · `1 failed, 62 passed` | Cây mới + `zz_gia.py` ⇒ `83 passed` *(có `[ix_fx]` · `[zz_gia]`)*. Bài tham số hoá CẮN: khuôn `KHOA ∈ COT` ⇒ `[zz_hong]` ĐỎ `sai giao kèo: KHOA + COT ⛔ được trùng tên: ['Thang']`; thư mục khuôn rỗng ⇒ `[RONG]` ĐỎ `danh_sach_khuon() rỗng — ⛔ khuôn nào để canh (Đ3)` | bài `:821` · `:1041` · `:1045` |
| `DT2-R2-03` *(GHI NHẬN · DEV)* | **đã sửa** *(rẻ: ≈ 7 dòng mã)* | ① `nap_khuon` từ chối `KHOA + COT` trùng tên *(khoá nằm trong `COT` · `COT` lặp)*. ② `_thieu_lac` đòi `thieu`/`lac` là `list`/`tuple` — chuỗi/set ⇒ `LoiKhuon` exit 3. ③ Mỗi điều khoản giao kèo một ca phá riêng *(M1 · M2 · M3 · M9 · trùng tên)*; hình dạng kết quả khuôn 5 ca; traceback THẬT trỏ tệp + hàm khuôn *(M6)*; ô chỉ-khoảng-trắng ở cột tiêu đề rỗng *(M7)*. ④ **Thêm** — bài `cong.ly_do` nêu ĐÚNG từng nguyên nhân *(xem "Đột biến")* | 5 ca ĐỎ trên `8e2fc95`: `[KHOA_nam_trong_COT]` · `[COT_trung]` `assert 0 == 2` *(exit 0 `[ĐẠT]`)*; `[thieu_la_CHUOI]` `assert 1 == 3` *(`thiếu 6` — đếm từng ký tự)*; `[lac_la_CHUOI]` · `[lac_la_SET]` `assert 0 == 3` *(exit 0 `[ĐẠT]`)*. Còn lại xanh sẵn — canh chốt có sẵn, chứng minh bằng đột biến | xanh | `tools/dong_bang_sheet.py:191-196` · `:317-319` · bài `:1098` · `:1129` · `:1152` · `:1177` · `:1201` |
| `DT2-R2-04` *(GHI NHẬN · orchestrator)* | **⛔ sửa** | `.gitignore` cho `*.DO.json` — phiếu gửi orchestrator *(Q6)*; ⛔ đụng | — | — | — |
| `DT2-R2-05` *(GHI NHẬN · orchestrator)* | **⛔ sửa** | Ghi Q5 vào `WO-085`/errata + gộp lại `isp/C1` mới — việc orchestrator; ⛔ đụng | — | — | — |
| `DT2-R2-06` *(GHI NHẬN · DEV)* | **đã sửa** | Docstring `test_DT2_B1_checksum_DOI…` bỏ câu khai *"lạc vì đứng sau 202512"*, thay *"`202306` đứng sau `202512` — đúng chỗ nó nằm ở sheet"* + ghi chú `DT2-R2-06` trích câu cũ *(biên bản)*. ⛔ đổi `assert` nào *(`git diff 8e2fc95 f3f2240` của tệp bài: dòng `-` chỉ ở 2 docstring + đúng 1 `assert` của `-02`)* | — *(chữ)* | — | bài `:184` |

### Đột biến *(`scratchpad/data_dt2_sua_r2/dot_bien.py`, cây tạm `git archive` + 2 tệp mới; mỗi mẫu khớp ĐÚNG 1 lần; chạy bộ 88 bài)*
- **Dựng lại**, ⛔ chép: log 32 đột biến vòng R1 *(`scratchpad/data_dt2_sua/`)* và 21 đột biến của WIP mất cùng scratchpad phiên cũ ⇒ bộ mới **57**: `R2-N1…N10` *(mã vòng này — đăng ký bỏ/sau exec/sai tên · bỏ từng `pop` · chốt trùng tên bỏ/chỉ một vế · nhận `str`/`set` · chỉ soát một khoá)* · `R2-M1…M11` *(14 đột biến mịn R2 + bỏ vế `not cot` · bỏ lọc tên khuôn · hẹp `except ValueError`)* · `D1…D29` *(chốt có sẵn: riêng tư · `float` · NaN · ngày · tháng 13 · trùng · `--mong` một chiều · từng `ly_do` · ô chữ · bool · dòng dài · cột ⛔ tên · 0 dòng · tệp `.DO` · `OSError` · tệp tạm · `--mong 0` · khoá chữ · thiếu cột · ngày ảnh · xuất xứ · hoa thường)* · `K1…K3` *(khuôn `ix_fx`)*.
- **Lượt 1** *(bài của WIP + bài `SAI_GIAO_KEO`, 83 bài)*: `TỔNG: 57 đột biến · chết 52 · sống 5 ['R2-M9 bỏ COT rỗng', 'D8 thiếu ⛔ đỏ', 'D9 ô rỗng ⛔ đỏ', 'D12 khoá hỏng ⛔ đỏ', 'D13 trùng ⛔ đỏ']`. ⭐ D8/D9/D12/D13 = gỡ hẳn dòng `ly_do.append` của một nguyên nhân mà 83/83 vẫn xanh. Đo `cong.ly_do` từng ca: khoá hỏng / ô rỗng ⇒ `kiem` C1 từ chối bảng ⇒ cổng vẫn ĐỎ qua *"thiếu/lạc ⛔ đo được"*; trùng `202408` thay `202509` ⇒ ĐỎ qua `thiếu 1`; thiếu ⇒ ĐỎ qua `--mong` lệch. Mọi bài cũ chỉ đòi exit 1 + dòng in *(dòng in có cả khi lý do ⛔ vào cổng)* ⇒ thêm `test_R2_03_cong_ly_do_NEU_DUNG_tung_nguyen_nhan` *(4 ca, ca *thiếu* đặt `--mong 36` ⇒ `ly_do == ['thiếu 1']`)* + ca `M9_COT_rong`.
- **Lượt 2** *(88 bài)*: `đối chứng (⛔ đột biến): exit 0 · 88 passed` · … · **`TỔNG: 57 đột biến · chết 57 · sống 0 []`** · `trả nguyên: tools/dong_bang_sheet.py 25ffaac32df9a4fb → 25ffaac32df9a4fb · tools/khuon_dong_bang/ix_fx.py 14e6b782f92c2c14 → 14e6b782f92c2c14` *(sha256[:16] của `tools/dong_bang_sheet.py` @ `f3f2240` = `25ffaac32df9a4fb`)*.

### Chạy đúng khi gộp DT3…DT12 *(lời giao: bản này là bản orchestrator giữ)*
`git merge-tree --write-tree --name-only f3f2240 isp/DT3` *(⛔ ref nào đổi)* ⇒ exit 1, **xung đột duy nhất** `tests/du_lieu/test_dong_bang_sheet.py` *(đúng các dòng `-02` mà DT3 tự viết lại)*; `tools/dong_bang_sheet.py` **tự gộp** *(0 dấu `<<<<<<<`)*. Cây gộp `5b6b137` + tệp bài của `f3f2240` *(giữ bản DT2)* ⇒ `pytest tests/du_lieu` **`156 passed`**; bài tham số hoá ra **4 ca** `[atl_cay]` · `[cdt_correct]` · `[ix_fx]` · `[mapping_master_cfg]` PASSED — ⛔ sửa dòng nào. ⛔ chạm nhánh `isp/DT3`.

### Ảnh `tests/fixture/cau_hinh/ix_fx.json` — **⛔ đổi byte nào**
`git diff 8e2fc95 f3f2240 -- tests/fixture/` rỗng. Bản thô thật ⛔ có ở container phiên này *(scratchpad orchestrator cũ đã mất)* ⇒ tái tạo bản thô **từ chính ảnh** *(hàm `_ban_tho_tu_anh` của bài)*, chạy công cụ mới ×2: `lượt 1 exit=0 sha256=e2c9fdd028bd3286` · `lượt 2 exit=0 sha256=e2c9fdd028bd3286` · `ảnh commit sha256=e2c9fdd028bd3286` · `[ĐẠT] cổng --mong 37: 37 dòng = mong · trùng 0 · thiếu 0 · khoá hỏng 0 · ô rỗng 0/185 · ô ⛔ số 0/185` · `lạc: [202306]` · `checksum_noi_dung: b6d1f9e9074951f1`.

### Cổng chạy lại *(cụm 5436)*
| Lệnh | Kết quả nguyên văn |
|---|---|
| ĐỎ trước mã: bài mới trên công cụ `8e2fc95` *(cây tạm)* | exit 1 · `6 failed, 82 passed in 4.05s` — 6 ĐỎ = `R2_01…dataclass…` + 5 ca `R2_03` *(lý do ở bảng)*; 82 xanh = 63 bài cũ + 19 bài canh chốt có sẵn *(đỏ trên đột biến)* |
| bài mới trên WIP `5e962d7` | exit 1 · `1 failed, 87 passed in 4.11s` — `…SAI_GIAO_KEO…` |
| `pytest tests/du_lieu/test_dong_bang_sheet.py tests/cau_hinh` | exit 0 · `110 passed in 4.16s` *(mẫu số `--collect-only`: `88 tests collected` + `22 tests collected`)* |
| `lint-imports` | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5436` *(HEAD `f3f2240`)* | exit 0 · `[ĐẠT]` ×7 kiểm môi trường *(`26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `Contracts: 11 kept, 0 broken.` · `chay 9845 / co 9967` · `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2550 passed, 2 xfailed, 1 warning, 14 errors in 305.62s (0:05:05)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 173.74s (0:02:53)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · **`══ KẾT: ĐẠT — mọi phép kiểm khớp mong`**. Mẫu số: 12 + 2550 + 2 + 14 = **2578** = 2553 *(KQ-088)* + 25; `skipped`/`deselected` **0** cả hai log; `tests/du_lieu` · `wo032_man_cua_that` trong `FAILED`/`ERROR`: **0**. `1 warning` = `SyntaxWarning: invalid escape sequence '\|'` ở `tools/sinh_ban_do_tang.py:214` *(⛔ tệp của vòng này)* |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 41 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` *(⛔ chạm schema)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — trùng nguyên văn đường nền *(KQ-088)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (179 file, 1885 bang, 727 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(đo SAU khi nối mục này)* |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: … '.venv/Scripts/lint-imports.exe'` *(đường Windows cứng — y hệt BG ⑪ · R1 · R2)* |

**Q8 · `MONG_PYTEST_TOAN_BO`:** nhánh `isp/DT2` **⛔ có** hằng ấy — grep `MONG_PYTEST` trong worktree *(`--include=*.sh/*.py/*.md`)* = **0** tệp; `tools/dung_moi_truong_isp.sh` chỉ có `MONG_LINT_*` · `MONG_HD1_*`. Theo quyết định orchestrator 17/11 *(`TIEN_DO.md`: DT3 Q1 = A — nhánh tách trước `1291ad5` ⛔ có hằng ⇒ orchestrator đặt sàn lúc gộp = số `--collect-only` của cây gộp)* ⇒ ⛔ nâng gì ở đây. Δ bài của vòng: **+25** *(`tests/du_lieu/test_dong_bang_sheet.py` 63 → 88, `pytest --collect-only`)*; toàn bộ `2553 → 2578`.

### Dev tự thấy còn yếu *(vòng sửa sau R2)*
1. **Bộ đột biến là bộ DỰNG LẠI**, ⛔ đúng 32 đột biến của vòng R1 *(log mất)* — tên `D…` ở đây ⛔ trùng nghĩa `D…` của R1/BG trên. 57/57 chết là của bộ này.
2. **Bài tham số hoá kiểm giao kèo LÚC NẠP, ⛔ chạy khuôn.** Khuôn của DT3…DT12 nạp được + khai đủ hằng nhưng `thieu_lac` sai thì bài này ⛔ thấy — bài riêng của bước ấy phải canh. Mục tuỳ chọn của bước sau *(DT3: `KIEU_COT` · `chuan_bi` · `PHU_MONG`)* ⛔ bị bài này đòi — chủ ý, để bài ⛔ phải sửa khi gộp.
3. **`KHUON_CO_MAT` tính lúc THU THẬP** *(nạp công cụ một lần ở cấp module)*: công cụ hỏng cú pháp ⇒ lỗi thu thập cả tệp *(ồn, ⛔ im)*.
4. **Đăng ký `sys.modules` theo tên `khuon_dong_bang_<tên>`** — nạp lại cùng khuôn sẽ THAY module cũ; một module khác trùng tên ấy *(⛔ có hôm nay)* sẽ bị đè.
5. Chốt *"cổng nêu đúng nguyên nhân"* chỉ phủ 4 nguyên nhân *(thiếu · trùng · khoá hỏng · ô rỗng)*; `ô ⛔ số` và `mong` đã có bài riêng đòi đúng chữ.
6. `kiem_so_song` vẫn ⛔ chạy được ở container.

### Câu hỏi cho orchestrator
⛔ câu mới. Q5 · Q6 *(trên)* vẫn chờ quyết định — `DT2-R2-04` · `-05` là việc orchestrator.
