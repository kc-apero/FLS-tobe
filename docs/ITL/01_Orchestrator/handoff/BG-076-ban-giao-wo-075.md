# BG-076 — bàn giao `WO-075` *(ISP 3.1.2 · Step 2 · C1)* — IX.FX đọc tĩnh: kiểm tỷ giá + `GET /api/fls/v1/config/fx`

| | |
|---|---|
| **Thuộc** | `WO-075` |
| **Phát bởi** | `fls-dev` *(làn **BE-CF**)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-077` · R2 `KQ-078` · R3 `KQ-079` *(dải orchestrator cấp)* |
| **Commit** | nhánh **cục bộ** `isp/C1` @ `5582246` *(mã + bài — hai commit: `9c964f4` tuyến + kiểm, `5582246` `yyyymm` số nguyên theo chốt liên làn)* — tách từ `329fa68` *(nền wave 1)*; ⛔ đẩy theo O2 = A: orchestrator gộp vào `claude/laughing-bohr-331pt0` sau R3 rồi mới đẩy. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-c1` · cụm PG riêng cổng **5434** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` §1.3 · §2.1 · **Step 2 · C1** *(8 trường + Substep 1/2)* · Step 14 · C5 + Step 18 · F4 + Step 33 · C7 *(để hợp đồng ⛔ chặn bước sau)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §3.2.1 · §3.2.4 · §3.5.3 D1 · §3.5.4 · AC9 *(sha256 đo lại `5cf6e576ff46f0886eb4a6b6cbefbcbd4f905a7835f843a2bfdb94d8a90982ba` — khớp WO)* · `SO_PHAT_HIEN_ISP-3.1.md` cột *luật phòng tái phạm* *(10 hàng `S0-R1-01…10`)* · `TIEN_DO.md` §Quy ước · `CLAUDE.md` Đ1–Đ5 · Cổng · Bẫy |

## Cổng vào *(`05` §5)*
- git thật: `git log -1` trong worktree = `329fa68 Nền wave 1: nhánh làm việc + isp/S0 @ 3d8318c` — đúng nền orchestrator giao; cây sạch khi nhận.
- version hợp đồng: ISP 3.1.2 · AP v3.1.2 sha256 khớp. Run id: WO ⛔ nói "đã chạy" ⇒ ⛔ cần.
- WO đủ trường §3.1 *(Màn hình: ⛔ chạm UI; Dữ liệu: `KHONG`)*. ⚠ `Trạng thái` của `WO-075` **⛔ đổi** ở nhánh này: lệnh giao việc giới hạn tệp được ghi *(`fls/cau_hinh/**` · `bang_tuyen.py` · `xu_ly.py` · `tests/cau_hinh/**` · `tests/api/test_isp_*.py` · `soi_bang_tuyen.py` · phiếu này)* ⇒ `WO-075` → `CHO_TEST` và `handoff/README.md` để orchestrator ghi lúc gộp.

## Substep 1 — test chọn · kế hoạch tối thiểu · lệnh · giới hạn
1. **Test cases** *(mục 6, phủ mọi dòng mục 8)*: `C1-B1` → AC-1 · `C1-B2` → AC-2 · `C1-B3` → AC-3 · `C1-B4` → AC-4 · `C1-B5` → AC-5. FE: N/A *(bước mở tuyến; màn ở F4)*. ⭐ **Bổ sung ngoài mục 6** *(bài `test_phu_*` — phủ phần "kiểm" mà phạm vi khai nhưng mục 6 ⛔ có ID)*: lạc · VND ≠ 1 · thiếu tiền tệ · ô rỗng/⛔ số/≤ 0/float · cột lạ · tháng sai khuôn · tập rỗng; và **Đ5 cho hai cổng** vừa đổi *(`kiem_bang_tuyen` · `soi_bang_tuyen`)*.
2. **Kế hoạch tối thiểu**: hàm thuần `fx.kiem` + `fx.doc_tep` · nguồn tĩnh 4 tháng · 1 hàm `ty_gia` ở `xu_ly.py` · 1 dòng `Tuyen` · khai nguồn tĩnh cho hai cổng *(trường `Tuyen.nguon_tinh` — xem "Vì sao có trường mới")*. Đường nguồn tĩnh khai **một chỗ**: `fx.NGUON_TINH`; `bang_tuyen` khai `nguon_tinh=(fx.NGUON_TINH,)`, hàm xử lý gọi `fx.doc_tep()` với mặc định là nó.
3. **Lệnh** *(gốc worktree; `export PG_DSN='postgresql://fls:fls@localhost:5434/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5434/fls_test' PYTHONUTF8=1`)*: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/cau_hinh/test_fx.py tests/api/test_isp_config_fx.py` · `…/python tools/soi_bang_tuyen.py` · `/home/user/FLS-tobe/.venv/bin/lint-imports` · `…/python -m pytest tests/api` · `bash tools/dung_moi_truong_isp.sh --cong 5434 --duong-nen`.
4. **Giới hạn**: số trả về là **TỔNG HỢP** cho tới `C5` *(ISP mục 3)*; ⛔ ký *(C7)*; ⛔ kho *(C5)*; `C1-B4` cần PG thật *(cửa mở kết nối chỉ đọc cho mọi tuyến)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/cau_hinh/fx.py` *(mới, 228 dòng)* | nạp + kiểm **thuần** `IX.FX`, **`yyyymm` là `int`** *(nguồn ghi chuỗi 6 chữ số được chuẩn về `int` ở `_thang`, ⛔ `bool`)*: một dòng/tháng · VND = 1 · đủ 5 tiền tệ; `thieu`/`trung`/`lac` là ba danh sách tháng có tên, mọi dòng *(kể cả trùng, lạc)* hiện nguyên trong `ky` — ⛔ cộng đôi, ⛔ thành 0 *(AP §3.2.4)*. Dòng hỏng ⇒ `LoiFX` mang **mọi** lý do, mỗi lý do nói tháng + cột, gói **một dòng** *(luật `S0-R1-04`)*; tập rỗng ⇒ `LoiFX` *(Đ3)*. Mọi dòng `trang_thai = 'chua_ky'` *(ký là C7)* |
| `fls/cau_hinh/tinh/ix_fx_mau.json` *(mới)* | nguồn tĩnh **4 tháng TỔNG HỢP** `202406…202409` *(tháng là số nguyên JSON)*, tự khai `"tong_hop": true` + `ghi_chu` *"⛔ SỐ TỔNG HỢP — bịa có chủ đích"*; khuôn số cố ý lộ là bịa *(USD `1000k` · SGD `700k` · COP `5.0k` · HKD `130k`, VND `1`)*; `thang_dau = 202406` |
| `fls/api/bang_tuyen.py` | `+ Tuyen.nguon_tinh` *(ngoại lệ HẸP: chỉ `GET` ⛔ ghi)*; cổng ⓓ *"⛔ khai bảng nào"* nay đòi ⛔ bảng **và** ⛔ nguồn tĩnh; `+ Tuyen("GET", f"{TIEN_TO}/config/fx", "ty_gia", (), nguon_tinh=(fx.NGUON_TINH,))` |
| `fls/api/xu_ly.py` | `+ ty_gia(yc)` — chỉ đọc + dọn hình theo hợp đồng nguyên văn; tỷ giá là `Decimal` ⇒ vỏ in **chuỗi**; `data_status = flash`; ghi danh `HAM` |
| `tools/soi_bang_tuyen.py` | phép canh ⓔ: tệp `nguon_tinh` phải **có thật**; bản đo mang `nguon_tinh`; dòng in `TINH : […] · vet N ham` |
| `tests/cau_hinh/__init__.py` · `tests/cau_hinh/test_fx.py` *(mới)* | **22** bài: `C1-B1` ×2 · `C1-B2` · `C1-B3` · `C1-B5` + **17** bài phụ *(lạc 1 · dòng sai 8 · tháng sai khuôn 5 · chuỗi ⇒ `int` 1 · tập rỗng 2)* |
| `tests/api/test_isp_config_fx.py` *(mới)* | **8** bài `C1-B4`: HTTP 200 hợp đồng · 401 · 405 · bảng tuyến · `soi` + Đ5 ×3 |

### Vì sao có trường mới `Tuyen.nguon_tinh` *(khái niệm thứ hai, ⛔ có trong ISP mục 3)*
`kiem_bang_tuyen` từ chối tuyến *"⛔ khai bảng nào"* và bài cũ `tests/api/test_bang_tuyen.py::test_cong_BAT_duong_khong_khai_bang_nao` ghim điều ấy *(⛔ sửa bài cũ)*; `BANG_CHO_PHEP` chỉ nhận `fls_*` và `soi_bang_tuyen` báo *"khai THỪA"* nếu gõ tên tệp vào `bang`. ⇒ Tuyến tĩnh **đầu tiên** của bảng *(40/40 tuyến trước đều chạm ≥ 1 bảng)* cần một câu *"tôi chạm cái này"* riêng. `C5` đổi tuyến sang bảng kho config và có thể gỡ trường.

## Cổng *(kết quả nguyên văn — `PG_DSN=…5434/fls` · `PG_DSN_TEST=…5434/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` *(qua `--duong-nen`, **lượt 3 — cây cuối `5582246`**)* | exit 1 · `13 failed, 2461 passed, 2 xfailed, 14 errors in 313.15s (0:05:13)` — mẫu số **2.490** bài thu thập *(S0: 2.460 + **30** bài của bước này)*; tập đỏ **27** = 26 đường nền + **1 THÊM**: `tests/api/test_ba07_phu_het_tuyen.py::test_moi_tuyen_THAT_deu_co_mat_trong_BA07` *(⚠ Q1)* |
| `python -m pytest` *(lượt 1 — cây làm việc trước commit, khác `9c964f4` chỉ ở hai chỉnh docstring `fx.py`; lượt 2 — `9c964f4`; cả hai trước chốt `int`)* | lượt 1: `13 failed, 2456 passed, 2 xfailed, 14 errors in 309.82s (0:05:09)` · lượt 2: `13 failed, 2456 passed, 2 xfailed, 14 errors in 314.58s (0:05:14)` — **2.485** bài; cùng **1 THÊM** ấy, bớt 0 |
| `python -m pytest tests/api` | trước *(cây `329fa68`)*: exit 1 · `3 failed, 346 passed, 11 errors in 84.91s` *(14 đỏ — cả 14 có tên ở `duong_nen_bai_do.txt`)* · sau *(cây cuối `5582246`)*: exit 1 · `4 failed, 353 passed, 11 errors in 85.05s` — `diff` với đường nền: **+1** `test_moi_tuyen_THAT_deu_co_mat_trong_BA07` · bớt 0 *(⚠ Q1)* |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '…/isp-c1/.venv/Scripts/lint-imports.exe'` *(`tools/kiem_so_song.py:406` gọi cứng đường Windows — đã biết từ `BG-066`, việc ngoài ISP)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (174 file, 1853 bang, 723 o ngay, 104 ma QD)` *(tính cả phiếu này — trước khi thêm phiếu: `173 file, 1848 bang`; 5 bảng mới đều qua K3)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — **trùng khít** lượt chạy trên `git archive 329fa68` cùng kho *(`diff` chỉ khác 2 dòng `SyntaxWarning` do bản xuất ⛔ có `__pycache__`)*; 5 lệch đều vì kho `fls` cục bộ RỖNG *(B3 · B4 · C5 · C5b `KHONG DO DUOC` · A1 · B1 · C6 `DOI TRANG THAI`)* — y `BG-066` |
| `python tools/soi_bang_tuyen.py` | exit 0 · `OK /api/fls/v1/config/fx` · `TINH : ['fls/cau_hinh/tinh/ix_fx_mau.json'] · vet 7 ham` · `✅ ban khai KHOP SQL that o ca 41 tuyen` *(40 → 41)* |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/bin/lint-imports` | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` *(⛔ chạm schema — chạy theo ISP Substep 2 ⑥)* | exit 0 · `khong co gi de ap` · `pg_verify: khop` |
| `bash tools/dung_moi_truong_isp.sh --cong 5434 --duong-nen` | **3 lượt, cả 3 cùng kết**. Lượt 3 *(cây cuối `5582246`)*: exit 1 · 7/7 `[ĐẠT]` phần kiểm môi trường · `[ĐỎ]  đường nền toàn bộ mong: tập đỏ = 26 node id của duong_nen_bai_do.txt — đo: 27 · thêm 1 · bớt 0` · `+ THÊM  tests/api/test_ba07_phu_het_tuyen.py::test_moi_tuyen_THAT_deu_co_mat_trong_BA07` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` *(`3 failed, 661 passed in 178.06s (0:02:58)`)* · `══ KẾT: ĐỎ — 1 phép kiểm khác mong hoặc ⛔ đo được`. Lượt 1 *(`tests/web` `3 failed, 661 passed in 180.14s`)* · lượt 2 *(`… 179.08s`)* — y hệt: `KẾT: ĐỎ`, đúng 1 node THÊM. Hai bài chập chờn đã biết *(`test_wo032_man_cua_that.py::test_AC3_…/::test_AC7_…`)* **⛔ chập** ở lượt nào |

## Bằng chứng từng AC
| AC | Mong | Bằng chứng *(bài · đo · dòng nguyên văn)* | Kết |
|---|---|---|---|
| AC-1 · `C1-B1` | 4 dòng, VND = 1, `thieu = trung = lac = []` | `tests/cau_hinh/test_fx.py::test_C1_B1_nap_BON_thang_hop_le_tu_nguon_tinh` — nạp **chính** tệp tĩnh qua `fx.doc_tep()`: mẫu số **4** dòng · **4** tháng khác nhau *(Đ3)*, `yyyymm` là `int`, mỗi dòng đủ đúng 5 tiền tệ, VND `== Decimal(1)`, mọi giá trị là `Decimal` *(⛔ float)*, `trang_thai == 'chua_ky'`, `(thieu, trung, lac) == ((), (), ())`, `nguon == 'fls/cau_hinh/tinh/ix_fx_mau.json'`; `::test_C1_B1_nguon_tinh_TU_KHAI_la_so_TONG_HOP` — tệp tự khai `tong_hop: true` + chữ `TỔNG HỢP` | đạt |
| AC-2 · `C1-B2` | `trung = ['202407']`; ⛔ cộng đôi | `::test_C1_B2_thang_202407_HAI_dong_thi_TRUNG_va_KHONG_cong_doi` — 5 dòng vào *(202407 hai lần: USD `20002` · `20008`)* ⇒ `trung == (202407,)`, **cả hai** dòng 202407 hiện trong `ky` với giá trị **riêng** `[20002, 20008]`, ⛔ dòng nào mang tổng `40010`, 5 dòng ra. Phá thử *"gộp dòng trùng"* ⇒ `assert () == (202407,)` | đạt |
| AC-3 · `C1-B3` | `thieu = ['202408']` | `::test_C1_B3_thieu_202408_GIUA_dai_thi_THIEU` — bỏ 202408 khỏi 4 tháng ⇒ `thieu == (202408,)`, `ky` = `[202406, 202407, 202409]` *(⛔ dòng `0` bịa)*. Phá thử *"bỏ vòng tìm tháng thiếu"* ⇒ `assert () == (202408,)` | đạt |
| AC-4 · `C1-B4` | 200, đúng hợp đồng; `soi_bang_tuyen` xanh với tuyến mới | `tests/api/test_isp_config_fx.py::test_C1_B4_GET_config_fx_200_DUNG_hop_dong` — máy THẬT + thẻ JWT thử: `200`; vỏ `{data, error, meta}`, `error = null`; **tập khoá BẰNG** `{bang, nguon, ky, thieu, trung, lac}` và mỗi kỳ `{yyyymm, USD, SGD, COP, VND, HKD, trang_thai}` *(khoá thừa cũng đỏ — phá thử *"thêm khoá `thua`"* ⇒ `⛔ lệch hợp đồng: ['thua']`)*; `bang = 'IX.FX'`; 4 kỳ `yyyymm` = `[202406, 202407, 202408, 202409]` là **số nguyên JSON**; tỷ giá là **chuỗi** *(phá thử `float(...)` ⇒ `AssertionError: (202406, 'USD', 10001.0)`)*; VND `"1"`; `meta.data_status = 'flash'`. `::test_C1_B4_khong_the_thi_401_cua_san_co` · `::test_C1_B4_chi_GET__POST_cung_duong_la_405`. `soi`: `::test_C1_B4_soi_bang_tuyen_XANH_va_THAT_SU_do_tuyen_moi` — `loi == []`, bản đo tuyến mới `khai = that = []` **và** `vet` chạm `fls.cau_hinh.fx.*` *(Đ3: tập rỗng là KẾT QUẢ vì phép đo đã bám tới hàm — 7 hàm)*, `nguon_tinh` có thật; lệnh: `✅ ban khai KHOP SQL that o ca 41 tuyen` | đạt *(⚠ nhưng mục 8 *"regression `tests/api` xanh"* **CHƯA** — Q1)* |
| AC-5 · `C1-B5` | `fls/cau_hinh` ⛔ import psycopg/repo/db | `::test_C1_B5_fls_cau_hinh_KHONG_biet_tang_kho__lint_imports` — gọi `lint-imports` của venv *(đường theo hệ điều hành)*, dòng hợp đồng 10 khớp **đúng 1** lần và kết `KEPT`; lệnh: `Contracts: 11 kept, 0 broken.`. **Xanh sẵn** trước khi có mã *(hợp đồng 10 khai ở S0, gói chỉ có `__init__.py`)* ⇒ ⛔ phá mã để có đỏ trước; chứng minh ĐỎ SAU khi có `fx.py`: thêm `import psycopg` vào `fx.py` ⇒ `fls.cau_hinh la config thuan, khong duoc biet tang kho BROKEN` · `Contracts: 9 kept, 2 broken.` *(vỡ thêm hợp đồng 1 vì `fls.api` → `fx` → `psycopg` bắc cầu)* · bài B5 `1 failed`; trả nguyên sha256 `044eb3e4e68fb96e → 044eb3e4e68fb96e` | đạt |

## Log ĐỎ → XANH
1. **ĐỎ** *(cây `329fa68` + chỉ hai tệp bài)*: `…/python -m pytest tests/cau_hinh/test_fx.py tests/api/test_isp_config_fx.py -rfE` ⇒ exit 1 · `23 failed, 2 passed in 1.11s`. Lý do — đều là **thiếu hành vi**, ⛔ lỗi dựng bài: 16 bài `E   ModuleNotFoundError: No module named 'fls.cau_hinh.fx'` *(nạp trễ ⇒ mỗi test ID đỏ riêng)* · HTTP `assert 404 == 200` với `'code': 'FLS-NOT-FOUND'` · `assert (404 == 405)` · `⛔ mong đúng 1 tuyến /api/fls/v1/config/fx, đo 0` · `` ⛔ `soi` đo 0 lần tuyến /api/fls/v1/config/fx `` · 2× `TypeError: Tuyen.__init__() got an unexpected keyword argument 'nguon_tinh'` · `IndexError: list index out of range` *(⛔ có tuyến để thay `nguon_tinh`)*. 2 bài xanh sẵn: `C1-B5` *(xem AC-5)* · `401` *(thẻ được kiểm TRƯỚC định tuyến — bài canh hồi quy, ⛔ hành vi mới)*.
2. **XANH** *(`9c964f4`)*: cùng lệnh ⇒ exit 0 · `25 passed in 1.05s`.
3. **Chốt liên làn giữa chừng** *(orchestrator 16/11: engine H1 `fls/bao_cao/gl.py` khoá tỷ giá theo `int` yyyymm)* — viết lại kỳ vọng sang `int` + 5 ca tháng sai khuôn *(kể cả `True`)* + 1 bài chuỗi ⇒ `int` TRƯỚC: exit 1 · `6 failed, 24 passed in 1.14s` — `assert ('202407',) == (202407,)` · `assert ('202408',) == (202408,)` · `assert ('202306',) == (202306,)` · `At index 0 diff: <class 'str'> != <class 'int'>` · HTTP `['202406', '202407', '202408', '202409']` *(đỏ vì kiểu, ⛔ vì dựng bài)*. Sau `5582246`: `30 passed in 0.93s`; thêm `tests/api/test_bang_tuyen.py` + `tests/api/test_soi_bang_tuyen.py` ⇒ `75 passed in 1.44s`.

## Phá thử *(Đ5 — sửa một chỗ, chạy bài, trả nguyên, so sha256 16 ký tự đầu · chạy lại trên cây cuối `5582246`)*
| Phá | Bài/lệnh | Kết | Trả nguyên |
|---|---|---|---|
| `import psycopg` vào `fx.py` | `lint-imports` | exit 1 · `… tang kho BROKEN` · `Contracts: 9 kept, 2 broken.` | `044eb3e4e68fb96e` ✓ |
| như trên | `C1-B5` | exit 1 · `1 failed` | ✓ |
| gộp dòng trùng *(giữ dòng cuối)* | `C1-B2` | exit 1 · `assert () == (202407,)` | ✓ |
| bỏ vòng tìm tháng thiếu | `C1-B3` | exit 1 · `assert () == (202408,)` | ✓ |
| `lac = ()` | bài phụ lạc | exit 1 · `assert () == (202306,)` | ✓ |
| bỏ phép kiểm VND = 1 | bài phụ dòng sai | exit 1 · `1 failed, 7 passed` *(đúng ca `VND`)* | ✓ |
| bỏ phép canh `nguon_tinh` có thật | `soi` Đ5 | exit 1 · `1 failed` | `7f692c6bb7e72e16` ✓ |
| bỏ luật `nguon_tinh` chỉ GET | `kiem_bang_tuyen` Đ5 | exit 1 · `2 failed` | `dc7f1ab44b761e72` ✓ |
| thêm khoá `thua` vào `data` | `C1-B4` 200 | exit 1 · `⛔ lệch hợp đồng: ['thua']` | `e5790360b5a57a30` ✓ |
| tỷ giá ra `float` | `C1-B4` 200 | exit 1 · `(202406, 'USD', 10001.0)` | ✓ |

## Kho thật
- `KHONG_CHAM`. Container ⛔ có sổ thật; `FLS_CHO_GHI_THAT` ⛔ đặt. Bước ⛔ chạm schema; kho `fls` cụm 5434 RỖNG *(`fls_itl = 0 dòng`)*, 26/26 di trú. Kho `fls_test` của cụm 5434 được `conftest` dựng lại mỗi lượt — vô hại.

## Cách chạy để xem
- ⛔ chạm UI. Tuyến xem qua bài `tests/api/test_isp_config_fx.py` *(máy thật, cổng tuỳ hệ điều hành)*.

## Câu hỏi cho orchestrator *(mỗi câu ≥ 2 phương án + cái giá; tôi đã chọn mặc định đảo ngược được cho câu `KHONG_CHAN`)*
1. **Q1 · `CHAN` cho mục 8 *"regression `tests/api` xanh"* + `--duong-nen`.** Cổng phủ tuyến `tests/api/test_ba07_phu_het_tuyen.py::test_moi_tuyen_THAT_deu_co_mat_trong_BA07` đòi **mọi** tuyến thật có mặt trong `docs/ITL/02_BA/07_API_CONTRACT.md`; grep `config` ở BA-07 = **0** dòng *(v3.14, 2026-10-06)*; ISP §2.1 ⛔ giao `07_API_CONTRACT.md` cho làn nào ⇒ bài **đỏ ngay khi tuyến tồn tại**. Tôi ⛔ được sửa `02_BA/**` hay bài cũ.
   - **A** *(khuyến nghị)* · `fls-ba` *(hay orchestrator đội vai BA)* thêm một dòng `✅ GET /api/fls/v1/config/fx` vào BA-07 trước khi gộp `C1` — được: cổng xanh **thật**, hợp đồng tuyến có chỗ ở *(F4 đọc từ đó)*; mất: một sửa đổi chéo làn, `C1` chờ nó mới đủ mục 8. Gợi ý nội dung *(bài chỉ soi chuỗi `/config/fx`)*: tuyến · *IX.FX tỷ giá tháng × 5 tiền tệ (VND = 1); `thieu`/`trung`/`lac` là trường riêng; tỷ giá ra chuỗi; nguồn TĨNH 4 tháng tổng hợp tới C5* · AP §3.2.1 · D1.
   - **B** · thêm node ấy vào `duong_nen_bai_do.txt` — được: `--duong-nen` ĐẠT ngay; mất: đúng thứ hợp đồng vai cấm *(gõ tên vào danh sách miễn trừ để cổng xanh)*, và che một khoảng trống tài liệu thật.
   - **C** · rút tuyến khỏi `BANG_TUYEN` tới khi BA-07 có — được: hồi quy xanh; mất: mất sản phẩm chính của `C1`, F4/H4 chờ.
   ⚠ Lớp lỗi lặp lại ở **mọi** bước mở tuyến *(C4 · C6 · C7 · C9 · C10 · C11 · C13)* ⇒ nên chốt luôn *"ai thêm dòng BA-07 cho tuyến mới"* cho cả ISP.
2. **Q2 · `KHONG_CHAN` — định nghĩa `lac`.** Spec ⛔ định nghĩa *(Đ1: `docs/` 8 tệp đều chép câu "kể cả dòng lạc 202306"; `fls/`+`tools/` 0 định nghĩa)*. **A** *(đã làm)* · nguồn khai `thang_dau`; tháng `< thang_dau` là lạc; dải `[thang_dau … tháng lớn nhất]`, lỗ trong dải là thiếu — được: tất định, ⛔ phụ thuộc thứ tự dòng, ⛔ ngưỡng; mất: mỗi nguồn phải khai `thang_dau` ⇒ **DT2/C5 phải mang `thang_dau = 202401`** cho ảnh thật thì `C5-B1` *(`lac = ['202306']`)* mới đạt. **B** · lạc = dòng sai thứ tự trong sheet — được: ⛔ cần khai thêm; mất: `AnhChup` ⛔ hứa giữ thứ tự, sắp lại sheet là `202306` thành 6 tháng THIẾU `202307…202312`. **C** · ⛔ có khái niệm lạc *(dải = [min, max])* — mất: ảnh thật ra 6 tháng CHẶN giả, `C5-B1` trượt. Khuyến nghị **A**, và orchestrator báo làn DATA thêm `thang_dau` vào `tests/fixture/cau_hinh/ix_fx.json` ở DT2.
3. **Q3 · `KHONG_CHAN` — nghĩa `trang_thai`.** **A** *(đã làm)* · trạng thái **ký** — C1 mọi dòng `chua_ky`, C7 thêm `da_ky` *(khớp `C7-B1`)*; nhãn TRÙNG/LẠC/CHẶN do F4 suy từ ba danh sách. **B** · trạng thái **kiểm** *(`hop_le`/`trung`/`lac`)* — mất: đụng `da_ky` của C7, phải tách hai trường. Khuyến nghị **A**.
4. **Q4 · `KHONG_CHAN` — kiểu trong JSON.** ⓐ **tỷ giá**: hợp đồng ISP ⛔ ghi kiểu; tôi theo luật `fls/api/bao.py` *"tiền ra JSON là CHUỖI"* ⇒ `"USD": "10001"`, `"VND": "1"` — F4 đọc chuỗi thập phân; phương án số JSON mất chữ số khi qua `float64` ở JS. Khuyến nghị giữ. ⓑ **`yyyymm`**: **số nguyên** theo chốt liên làn của orchestrator *(engine H1)* — ⚠ **lệch dấu nháy** với ISP mục 6 *(`trung = ['202407']` · `thieu = ['202408']`)* và `C5-B1` *(`lac = ['202306']`)*: tôi đọc dấu nháy ấy là cách viết, ⛔ là kiểu; R1 đối chiếu ISP nguyên văn sẽ thấy lệch — ghi ở đây để ⛔ tính là lỗi. Nếu muốn ISP khớp chữ: `fls-ba` sửa ba ô ấy ở bản ISP kế tiếp.
5. **Q5 · ghi nhận — môi trường.** Thư mục scratchpad của phiên **dùng chung** cho ba làn song song: làn H1 ghi `scratchpad/duong_nen_1.log` — **trùng tên** tệp log lượt `--duong-nen` đầu của tôi ⇒ tôi dừng lượt ấy *(chỉ tiến trình của mình, lọc theo `cwd` worktree)* và chạy lại vào `scratchpad/c1/`. Khuyến nghị: mỗi làn một thư mục con trong scratchpad.

## Dev tự thấy còn yếu
1. **Mục 8 chưa đủ**: `tests/api` hồi quy **+1 đỏ** *(Q1)* — `C1` ⛔ được coi là xong cho tới khi BA-07 có dòng `/config/fx`.
2. **`lac` là định nghĩa CỦA TÔI** *(Q2)*; `C1-B1…B3` ⛔ ghim nó — chỉ bài phụ `test_phu_thang_LAC_…` ghim. Nếu orchestrator chọn khác, đổi **một hàm** `fx.kiem` + một bài.
3. **`soi_bang_tuyen` chỉ canh tệp `nguon_tinh` CÓ THẬT, ⛔ canh hàm xử lý ĐỌC đúng tệp ấy**: phép đo tĩnh ⛔ theo được tham số mặc định `doc_tep(duong=NGUON_TINH)` ⇒ một hàm đọc tệp khác vẫn qua `soi`. Lưới đỡ: bài HTTP ghim `nguon == 'fls/cau_hinh/tinh/ix_fx_mau.json'` *(chuỗi chép tay, cố ý ⛔ đọc lại từ hằng)*.
4. **Trường `Tuyen.nguon_tinh` là khái niệm thứ hai** ngoài *"miền config"* ISP khai — cần vì cổng ⓓ + bài cũ; nếu `C5` quên gỡ thì trường sống thừa *(⛔ có bài nào canh "⛔ còn tuyến nào dùng `nguon_tinh`")*.
5. **Tuyến tĩnh vẫn phụ thuộc kho**: `cua.py` mở kết nối chỉ đọc cho MỌI tuyến trước khi gọi hàm ⇒ kho tắt thì `/config/fx` cũng `500`, dù ⛔ dùng kết nối. Cố ý ⛔ thêm nhánh vào `cua.py` *(tệp đã qua rà soát P4, ngoài làn)*.
6. **Nguồn tĩnh hỏng ⇒ `500 FLS-INTERNAL`** *(`LoiFX` lọt lên cửa, lý do vào nhật ký máy)*, ⛔ mã riêng: `MA_LOI` ở `bao.py` + BA-07 §5 ngoài làn. Chưa có bài HTTP cho nhánh này *(chỉ bài đơn vị `LoiFX`)*.
7. **`yyyymm` đổi `str` → `int` giữa chừng** *(chốt liên làn, commit `5582246`)*: mô hình, nguồn tĩnh, JSON tuyến đều `int`; nguồn chuỗi 6 chữ số được chuẩn về `int` *(có bài)*. ⛔ Hàm chuyển cho H1 *(việc H4)* ⇒ hai bên mới **cùng kiểu khoá**, ⛔ đã được **nối thử** lần nào. ISP ghi dấu nháy *(Q4 ⓑ)*.
8. **Hai bài xanh sẵn trước mã** *(`C1-B5` · `401`)* là bài canh hồi quy, ⛔ chứng minh hành vi mới; đỏ của `C1-B5` chỉ chứng được SAU khi có `fx.py` *(phá thử)*.
9. **`C1-B5` gọi `lint-imports` bằng tiến trình con** theo đường hệ điều hành *(`bin/` · `Scripts/*.exe`)* — đường Windows ⛔ thử được ở container.
10. Bài B1/B4 ghim **4** dòng của tệp tĩnh ⇒ `C5` *(GỠ tệp tĩnh)* phải viết lại hai bài ấy — dây chuyền dự kiến, ⛔ bất ngờ.
