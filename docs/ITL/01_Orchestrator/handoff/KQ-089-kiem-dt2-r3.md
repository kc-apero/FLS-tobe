# KQ-089 — biên bản kiểm `BG-086` *(ISP 3.1.2 · Step 8 · DT2 · vòng **R3** — vòng xác nhận cuối trước gộp + push)*

| | |
|---|---|
| **Thuộc** | `BG-086` mục *"Vòng sửa sau R2 (`KQ-088`)"* · `WO-085` *(phiếu `WO-085` ⛔ có ở nhánh nào — spec = ISP `## Step 8 · DT2` + lời giao, như R1/R2)* |
| **Kiểm bởi** | `fls-test` *(R3, phiên cloud CON độc lập, phiên mới)* · 2026-11-17 · orchestrator ISP 3.1.2 giao |
| **Phạm vi** | `git diff 8e2fc95 isp/DT2` — vòng sửa sau R2: `f3f2240` *(mã + bài: `tools/dong_bang_sheet.py` +27/−7 · `tests/du_lieu/test_dong_bang_sheet.py` +297)* + `d46e817` *(giấy: `BG-086` +61 dòng)*. **3 tệp**, ⛔ chạm `fls/**` |
| **Cụm** | reviewer cổng **5446** *(`/home/user/fls-pg16-5446` — R3 tự dựng bằng `dung_moi_truong_isp.sh --cong 5446` từ worktree `isp-s0`; `KẾT: ĐẠT`, 7/7 `[ĐẠT]`)* |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA còn mở · 1 GHI NHẬN mới** *(`DT2-R3-01`)*. Thang PUSH *(0 CHẶN **và** 0 NÊN SỬA mở)* ⇒ **đủ điều kiện gộp + push**. 2 NÊN SỬA của R2 *(`DT2-R2-01` · `-02`)*: **ĐÃ SỬA** *(tái hiện ĐỎ trên `8e2fc95`, XANH trên `d46e817`)*. 4 GHI NHẬN R2: `-03` **ĐÃ SỬA** · `-06` **ĐÃ SỬA** · `-04` · `-05` **CHẤP NHẬN** *(orchestrator đã quyết — ⛔ tính là phát hiện mở)* |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT2.md` v0.3 *(đổi ô Trạng thái 6 hàng R2 + thêm 1 hàng `DT2-R3-01`)* |

## Cổng vào *(`05` §5)*
- **git:** worktree `isp/DT2` HEAD = **`d46e817`** *(giấy)* trên `f3f2240` *(mã)* trên `8e2fc95` *(`KQ-088`)* — khớp dòng **Commit** của mục "Vòng sửa sau R2" trong `BG-086`. Sha mong khớp lời giao: `isp/S0` = `c1cf29b` · `isp/DT2` = `d46e817` · `isp/DT3` = `5a96cd9`. Nhánh cục bộ, ⛔ đẩy — đúng lời giao. `git status --short` = **0** dòng trước và sau mọi phép đo *(mọi phép phá chạy trên bản sao `git archive` ở `/tmp/r3_dt2/`)*.
- **version spec:** ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` `## Step 8 · DT2` *(dòng `1016`–`1098`)*.
- **Quyền làn:** 3 tệp chạm — `tools/dong_bang_sheet.py` · `tests/du_lieu/**` *(DATA)* · `BG-086` *(giấy handoff)*. ⛔ tệp `fls/**`. ⛔ lấn bước DT3…DT12 *(⛔ thêm khuôn nào; `tools/khuon_dong_bang/ix_fx.py` ⛔ đổi byte)*. Mã công cụ đổi gói gọn ở `nap_khuon` + `_thieu_lac` — do `DT2-R2-01`/`-03` đòi, ⛔ refactor ngoài test.
- **Sha hiện vật** *(R3 đo độc lập trên bản sao `git archive`)*: `tools/dong_bang_sheet.py` sha256[:16] = **`25ffaac32df9a4fb`** *(= BG)* · `tools/khuon_dong_bang/ix_fx.py` = **`14e6b782f92c2c14`** *(= BG, ⛔ đổi)* · `tests/fixture/cau_hinh/ix_fx.json` = **`e2c9fdd028bd3286`** *(= BG "⛔ đổi byte")* · old `8e2fc95` tool = `b0827a75de05cb24`.

## Cổng chạy lại *(R3 tự chạy ở worktree, `PG_DSN=…:5446/fls` · `PG_DSN_TEST=…:5446/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`; log `/tmp/r3_dt2/logs/`)*
| Lệnh | `BG-086` *(vòng sửa R2)* nói | R3 đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_dong_bang_sheet.py tests/cau_hinh` | `110 passed` *(88 + 22)* | exit 0 · **`110 passed in 5.42s`** · `--collect-only`: `tests/du_lieu` = **88** · `tests/cau_hinh` = **22** | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5446` *(script của **nhánh DT2**, GOC = isp-dt2 ⇒ **mã DT2**)* | exit 0 · `12 failed, 2550 passed, 2 xfailed, 14 errors` · `26 = 26` · web `3 failed, 661 passed` · `3 = 3` · `KẾT: ĐẠT` | exit **0** · 7 `[ĐẠT]` môi trường · toàn bộ **`12 failed, 2550 passed, 2 xfailed, 14 errors in 340.83s`** · `[ĐẠT] … 26 = 26 node id (thêm 0 · bớt 0)` · web **`3 failed, 661 passed in 183.90s`** · `3 = 3` · **`KẾT: ĐẠT`** | ✅ |
| mẫu số của lượt trên *(Đ3 — R3 tự đo vì cổng DT2 ⛔ khai `MONG_PYTEST_TOAN_BO`)* | — *(BG Q8: nhánh DT2 ⛔ có hằng)* | `--collect-only` toàn bộ = **2578** = run `12+2550+2+14` · web **664** = `3+661` · **collect = run** *(⛔ teo im lặng)* · `skipped`/`deselected` trong hai log pytest: **0** dòng · `tests/du_lieu` · `wo032_man_cua_that` trong `FAILED`/`ERROR`: **0** | ✅ |
| `bash …/isp-s0/tools/dung_moi_truong_isp.sh --duong-nen --cong 5446` *(script **nhánh S0**, GOC = isp-s0 ⇒ **mã S0** — chạy thêm vì cổng DT2 KHÁC bản S0 về hành vi: S0 có sàn `MONG_PYTEST_TOAN_BO=2490` + XFAIL-theo-tên, DT2 ⛔ có)* | — | exit **0** · toàn bộ `12 failed, 2462 passed, 2 xfailed, 1 warning, 14 errors` · `[ĐẠT] … 28 = 28 node id (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 2490 bài (mong ≥ 2490) · skipped 0 · deselected 0` · web `3 = 3 · chạy 664` · **`KẾT: ĐẠT`** | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` exit 0 | ✅ |
| `python tools/soi_bang_tuyen.py` | `41 tuyen` | `✅ ban khai KHOP SQL that o ca 41 tuyen` exit 0 | ✅ |
| `python tools/kiem_thuyet_minh.py` | `31/31` | `✅ CONG THUYET MINH DAT — 31/31 nut …` exit 0 | ✅ |
| `python -m fls.db.pg_migrate` | `khong co gi de ap` · `khop` | `khong co gi de ap` · `pg_verify: khop` exit 0 | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `179 file, 1885 bang` | exit 0 · `179 file, 1885 bang, 727 o ngay, 104 ma QD` *(đo TRƯỚC khi thêm phiếu này)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech` *(đường nền)* | exit 1 · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` · B3 · B4 · C5 · C5b KHONG DO DUOC · A1 · B1 · C6 DOI TRANG THAI *(kho rỗng — trùng đường nền; grep `tools/`/`tests/`/`fixture` trong công cụ = 0 ⇒ bước này ⛔ chạm được nó)* | ✅ *(cùng đỏ nền)* |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC | exit 1 · `FileNotFoundError: … '.venv/Scripts/lint-imports.exe'` — **⛔ KHÔNG ĐO ĐƯỢC** ở container *(đường Windows cứng — đường nền, ⛔ do bước này)* | ✅ *(cùng đỏ)* |

> **Hai lượt `--duong-nen`** chạy vì cổng của nhánh DT2 KHÁC bản S0 về **hành vi** *(`diff` hai `dung_moi_truong_isp.sh`: DT2 là bản CŨ — `so_tap_do` ⛔ canh mẫu số `chạy ≥ mong · skipped 0 · deselected 0`, ⛔ `-rfEx`/XFAIL-theo-tên)*. Vì cổng DT2 yếu hơn, R3 **tự** đo mẫu số *(collect = run = 2578 · 0 skipped · 0 deselected)* và chạy thêm cổng S0 để chứng cụm + sàn S0 lành. Cả hai `KẾT: ĐẠT`. *(Chênh 2578 ≠ 2490 là do khác CÂY mã: DT2 có +88 bài `du_lieu` + bài gộp `isp/C1`; S0 là nền.)*

## Bảng AC *(= test ID ISP mục 6 + từng dòng mục 8, R3 đo trên `d46e817`)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `DT2-B1` | 37 dòng; checksum ổn định qua 2 lần chạy | R3 tái tạo bản thô **ĐỘC LẬP** từ ảnh *(⛔ dùng helper của bài)*, chạy công cụ: exit 0 · **37** dòng · sha256 ra = **`e2c9fdd028bd3286`** = ảnh commit *(byte-identical)* · `checksum_noi_dung = b6d1f9e9074951f1`; 5 bài `test_DT2_B1_*` PASSED | **ĐẠT** |
| **AC-2** · `DT2-B2` | cột `Email Address` ⇒ ĐỎ, ⛔ ghi | 3 bài `B2` PASSED *(nguyên văn · khoảng trắng · chữ thường)*; quét ảnh commit: `@` = 0, khoá `email address` *(chuẩn hoá)* = 0 | **ĐẠT** |
| **AC-3** · `DT2-B3` | thiếu 1 tháng ⇒ ảnh đúng nguồn + `thiếu: [yyyymm]` + exit ≠ 0 | 7 bài `B3` PASSED; cổng ĐỎ cả hai chiều có bài `[36-1]·[37-0]·[38-1]` | **ĐẠT** |
| **AC-4** · mục 8 *"B1…B3 xanh; cổng đã thấy đỏ"* | xanh + đỏ đã thấy | 88/88 xanh; R3 tự tái hiện **6 ĐỎ** trên `8e2fc95` *(`R2_01_dataclass` + 5 ca `R2_03`)*; **8 đột biến tự dựng** ở phần mới ⇒ **7 chết** *(nap_khuon ×3 · giao kèo ×3 · ly_do thiếu)* · **1 sống** ⇒ `DT2-R3-01` *(GHI NHẬN)* | **ĐẠT** |
| **AC-5** · mục 8 *"ảnh ⛔ mang khoá PII (quét = 0)"* | 0, mẫu số ≠ 0 | R3 quét ảnh commit: khoá `email address` **0** · ký tự `@` **0**; mẫu số = **29** khoá JSON + **259** khoá-từng-dòng *(≠ 0 — Đ3)*; `khong_mang_PII`: "máy soát 6 tên cột … 0 trùng" | **ĐẠT** |
| **AC-6** · mục 8 *"3 vòng review xong"* | R1 · R2 · R3 | R1 `KQ-087` ✅ · R2 `KQ-088` ✅ · R3 = phiếu này ✅ | **ĐẠT** |
| **AC-7** · mục 8 *"điều kiện PUSH"* | đủ R1·R2·R3, chặn = 0 **và** *(thang lời giao)* 0 NÊN SỬA mở | R3: **0 CHẶN · 0 NÊN SỬA mở** ⇒ **ĐỦ** | **ĐẠT** |
| **AC-8** · mục 7 *hiện vật* | `ix_fx.json` có `nguon` · `ngay_dong_bang` · `khong_mang_PII` · `checksum_noi_dung`; `tools/dong_bang_sheet.py` | 4/4 trường có *(ảnh ⛔ đổi byte)*; công cụ + khuôn `tools/khuon_dong_bang/ix_fx.py` có | **ĐẠT** |
| **AC-9** · mục 2 *goal* | một lệnh → ảnh 37 dòng `202401→202612` + lạc `202306` | lệnh ISP exit 0; `thiếu: []` `lạc: [202306]` *(định nghĩa khuôn `ix_fx` = `kiem` của C1, `thang_dau 202401`)* | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 8 + quyết định orchestrator + Đ1–Đ5)* | **2 NÊN SỬA + 2 GHI NHẬN của R2 ĐÃ SỬA đúng, ⛔ sửa bài cũ cho xanh; 0 hồi quy; 1 lỗ phủ mịn mới `DT2-R3-01`** | ① `DT2-R2-01`: `nap_khuon` đăng ký `sys.modules[spec.name] = m` **trước** `exec_module` *(`:174`)*, `pop` khi nạp lỗi *(`:178`)* **và** khi sai giao kèo *(`:200`)* — R3 đặt khuôn THẬT `@dataclass` + `from __future__ import annotations` *(`get_type_hints` LÚC CHẠY)* vào cây `8e2fc95` ⇒ **ĐỎ** `AttributeError: 'NoneType'…`, vào `d46e817` ⇒ **XANH**; 3 đột biến R3 *(gỡ từng dòng `sys.modules`)* đều CHẾT. ② `DT2-R2-02`: bài đổi `== ["ix_fx"]` → `"ix_fx" in …` + glob độc lập + bài tham số hoá trên `danh_sach_khuon()` *(`:823`/`:1041`)* — R3 THÊM một tệp khuôn hợp lệ: bài CŨ *(ghim)* ĐỎ `['ix_fx','zz_gia'] == ['ix_fx']`, bài MỚI XANH. **Kiểm gộp DT3** *(lời giao)*: `git merge-tree --write-tree d46e817 isp/DT3` ⇒ xung đột **duy nhất** `tests/du_lieu/test_dong_bang_sheet.py`, `tools/dong_bang_sheet.py` **tự gộp**; cây gộp + giữ bản bài DT2 ⇒ bài tham số hoá ra **4 ca** `[atl_cay]·[cdt_correct]·[ix_fx]·[mapping_master_cfg]` **4 PASSED** — mọi khuôn DT3 nạp được + đủ giao kèo. ③ `DT2-R2-03`: chốt `KHOA + COT ⛔ trùng tên` *(`:191-196`)* + `thieu/lac` phải `list/tuple` *(`:316-319`)* — 5 ca ĐỎ trên `8e2fc95`, XANH trên `d46e817`; đột biến R3 *(vô hiệu hai chốt)* đều CHẾT. ④ `DT2-R2-06`: `git diff 8e2fc95 d46e817` tệp bài — **đúng 1 `assert` bỏ** *(của `-02`)*, phần còn lại là docstring + bài mới ⇒ ⛔ đụng `assert` nào cho `-06`. ⑤ Phạm vi: 3 tệp, ⛔ `fls/**`, ⛔ thêm khuôn, ⛔ refactor ngoài test |
| **Dữ liệu** *(bước ⛔ chạm kho; dữ liệu = ảnh ↔ bản thô)* | **Ảnh ⛔ đổi byte; công cụ tái tạo đúng từng byte (R3 tự dựng)** | sha256 ảnh = `e2c9fdd0…` = ảnh R1/R2 *(R1 đã so độc lập 222/222 ô ⇒ phép so còn hiệu lực)*; `cong` ảnh = `{mong 37, so_dong 37, dat true, ly_do []}`. R3 dựng lại bản thô TỪ ảnh *(script riêng `/tmp/r3_dt2/`, ⛔ dùng `_ban_tho_tu_anh` của bài)* ⇒ công cụ ra byte-identical. Công cụ ⛔ nối kho *(grep `psycopg`/`PG_DSN`/`connect` ở `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/` = 0)*; `fls_itl = 0 dòng`. Kho THẬT `fls-pg-1` ⛔ có ở container ⇒ ⛔ đọc |
| **Màn hình** | **N/A** | ISP Step 8 §4 *"Frontend: N/A — bước dữ liệu"* |

## Phát hiện R2 — trạng thái sau R3
| F R2 | Mức R2 | Kết R3 | Tái hiện *(R3 đo)* |
|---|---|---|---|
| `DT2-R2-01` | NÊN SỬA | **ĐÃ SỬA** | Khuôn `@dataclass` + `__future__` nạp **ĐỎ** trên `8e2fc95` *(`AttributeError: 'NoneType'`)*, **XANH** trên `d46e817`; 3 đột biến `sys.modules` *(đăng ký trước exec · pop nạp lỗi · pop sai giao kèo)* đều CHẾT; không rò `sys.modules` khi nạp lỗi/sai giao kèo |
| `DT2-R2-02` | NÊN SỬA | **ĐÃ SỬA** | Thêm tệp khuôn ⇒ bài CŨ ĐỎ `['ix_fx','zz_gia'] == ['ix_fx']`, bài MỚI XANH; cây gộp DT3 *(4 khuôn)* ⇒ bài tham số hoá 4 ca PASSED, `tools/dong_bang_sheet.py` tự gộp — ⛔ xung đột ở công cụ |
| `DT2-R2-03` | GHI NHẬN | **ĐÃ SỬA** | 5 ca `[KHOA_nam_trong_COT]·[COT_trung]·[thieu_la_CHUOI]·[lac_la_CHUOI]·[lac_la_SET]` ĐỎ trên `8e2fc95`, XANH trên `d46e817`; đột biến R3 vô hiệu hai chốt ⇒ CHẾT |
| `DT2-R2-04` | GHI NHẬN · orchestrator | **CHẤP NHẬN** | Q6 = ⓐ *(lời giao)*: `.gitignore` cho `*.DO.json` ở **nhánh làm việc**, ⛔ `isp/DT2`. R3 đo: isp/DT2 ⛔ có `.DO.json` theo dõi *(git ls-files = 0)* · `.gitignore` ⛔ có dòng ấy *(đúng)* · cây sạch. ⛔ tính là phát hiện mở |
| `DT2-R2-05` | GHI NHẬN · orchestrator | **CHẤP NHẬN** | Q5 = ⓐ *(lời giao)*: cổng DT2 ĐỎ khi C1 từ chối bảng — C1 mới đến qua thứ tự gộp C1 → DT2. ⛔ tính là phát hiện mở. *(Khuôn `ix_fx` gọi `fls.cau_hinh.fx.kiem` qua import — `ix_fx.py` ⛔ đổi byte)* |
| `DT2-R2-06` | GHI NHẬN | **ĐÃ SỬA** | docstring `test_DT2_B1_checksum_DOI…` *(`:188`)* bỏ câu KHAI định nghĩa cũ; `git diff` xác nhận ⛔ đụng `assert` nào của `-06` *(1 assert bỏ là của `-02`)* |

## Phát hiện mới *(R3)*
| F | Mức | Nơi | Tái hiện *(R3 đo)* | Khuyến nghị | Gửi |
|---|---|---|---|---|---|
| `DT2-R3-01` | **GHI NHẬN** *(`NHE` — ⛔ chặn push)* | `tools/dong_bang_sheet.py:388` · `tests/du_lieu/test_dong_bang_sheet.py:1177` | *(tái phạm MỊN lớp `DT2-R2-03` — chốt "cổng nêu đúng nguyên nhân")* Nhãn mục `cong.ly_do` của nguyên nhân **`ô ⛔ số`** *(`:388`, ⛔ dấu hai chấm)* là **1/7** nhãn mà **⛔ bài nào đòi** nội dung trong `cong.ly_do`. R3 đột biến `ly_do.append(f"ô ⛔ số …")` → `f"XXX …"` *(bản sao `git archive`, trả nguyên sha256 ✓)* ⇒ **88/88 vẫn xanh**. Bài `R2_03_cong_ly_do_NEU_DUNG_tung_nguyen_nhan` *(`:1177`)* chỉ tham số **4** nguyên nhân *(thiếu · trùng · khoá hỏng · ô rỗng)*; bài `:544`/`:694` đòi **dòng CHI TIẾT** `ô ⛔ số: n/185` *(`:453`, CÓ dấu hai chấm)* — ⛔ đòi mục `cong.ly_do`. BG *("Dev tự thấy còn yếu" R2 ⑤)* khai *"`ô ⛔ số` … đã có bài riêng đòi đúng chữ"* — ĐÚNG cho dòng chi tiết stdout, **⛔ đúng** cho mục `cong.ly_do`. *(`thiếu/lạc ⛔ đo được` ⛔ phải lỗ: bài `:640` đòi `"thiếu/lạc ⛔ đo được" in x` trên `cong.ly_do`; `{len} dòng ≠ mong` được canh qua stdout. Chỉ `ô ⛔ số` hở mục `cong.ly_do`.)* | Thêm `ô ⛔ số` làm ca thứ 5 của `test_R2_03_cong_ly_do_NEU_DUNG_tung_nguyen_nhan` *(đặt `--mong` = số dòng ⇒ `ô ⛔ số` là lý do duy nhất ⇒ `cong.ly_do == ["ô ⛔ số k/185"]`)*. ⛔ CHẶN: hành vi công cụ ĐÚNG *(`dat = not ly_do` nên cổng vẫn ĐỎ đúng)*, ⛔ có bên tiêu thụ `cong.ly_do[i]` *(C5 chưa dựng)*; chỉ là lỗ PHỦ của bài cùng lớp `-03` | `DEV` *(làn DATA)* |

## Bài thử mới *(⛔ commit ở R3 — lời giao chỉ cho commit phiếu + sổ; tệp ở `/tmp/r3_dt2/`)*
| Bài | Đã chứng minh bằng | Kết |
|---|---|---|
| `dot_bien_r3.py` *(8 đột biến tự dựng ở `nap_khuon` · kiểm giao kèo · `cong.ly_do`)* | bản sao `git archive d46e817`, mỗi mẫu khớp đúng 1 lần, trả nguyên `25ffaac32df9a4fb → 25ffaac32df9a4fb` | **chết 7 · sống 1** *(`DT2-R3-01`)* |
| `ly_do_map.py` *(phủ từng nhãn `cong.ly_do`)* | đổi mỗi nhãn → `XXX_`, chạy 88 bài | 4 CHẾT *(trùng·thiếu·khoá hỏng·ô rỗng)* · `ô ⛔ số` SỐNG *(lỗ)* · `dòng ≠ mong`/`thiếu/lạc ⛔ đo được` "sống" do tiền tố giữ chuỗi đòi — **⛔ lỗ** *(đo lại: `:640` phủ `đo được`; stdout phủ `mong`)* |
| tái tạo ảnh ĐỘC LẬP | dựng bản thô từ ảnh *(script riêng)* → chạy công cụ ×1 → sha256 = ảnh commit | byte-identical `e2c9fdd028bd3286` |

## Ngoài phạm vi lượt này *(theo lời giao)*
- **Chỉ commit** phiếu này + sổ riêng `SO_PHAT_HIEN_ISP-3.1_DT2.md` lên `isp/DT2`; **push** `isp/DT2 → refs/heads/claude/bold-galileo-zukpaf-isp/DT2` *(fast-forward từ `d46e817`, người dùng đã duyệt ĐÚNG một nhánh)*; ⛔ push nhánh khác, ⛔ force, ⛔ PR, ⛔ comment GitHub.
- ⛔ cập nhật `handoff/README.md`, `04_Test/03_TRACEABILITY_GAP_REPORT.md`, dòng nhật ký §5 — orchestrator gom khi gộp *(tiền lệ `S0-R1-08`, `KQ-087`, `KQ-088`)*.
- Tệp R3 ở `/tmp/r3_dt2/` *(⛔ commit — bản sao mang số thật)*: `old/` · `new/` · `redprobe/` · `addold/` · `addnew/` · `merged/` · `dot_bien_r3.py` · `ly_do_map.py` · `logs/duongnen_dt2.log` · `logs/duongnen_s0.log`.
