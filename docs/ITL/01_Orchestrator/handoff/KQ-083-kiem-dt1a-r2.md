# KQ-083 — biên bản kiểm `BG-081` *(ISP 3.1.2 · Step 3 · DT1a · vòng **R2** — CHỈ quét phần đổi SAU R1)*

| | |
|---|---|
| **Thuộc** | `BG-081` *(mục "Vòng sửa sau R1 (`KQ-082`)")* · `WO-080` |
| **Kiểm bởi** | `fls-test` *(R2, phiên mới, độc lập với R1 và với tác giả vòng sửa)* · 2026-11-16 · orchestrator giao |
| **Phạm vi** | `git diff 2664e25..isp/DT1A` — **4** tệp *(`6903096` công cụ + bài + JSON · `fb0cfbd` mục vòng sửa trong `BG-081`)*: `tools/phan_loai_dong_thieu.py` +111/−24 · `tests/du_lieu/test_phan_loai_dong_thieu.py` +360/−14 · `docs/ITL/_tools/phan_loai_dong_thieu.json` 1 dòng · `BG-081` +68 *(chỉ thêm)*. Phần trước `2664e25` là việc của R1 *(`KQ-082`)* |
| **Cụm** | reviewer làn DATA cổng **5447** *(`/home/user/fls-pg16-5447`, để CHẠY)* · log R2: scratchpad phiên `…/scratchpad/r2_dt1a/` *(⛔ trong repo)* |
| **Phán quyết** | **`ĐẠT`** vòng R2 — **0 CHẶN** · **0 NÊN SỬA** mới · **3 GHI NHẬN** mới *(`DT1a-R2-01…03`, lớp B1 cả 3)*. Phát hiện R1: **7** ĐÃ SỬA *(cả hai NÊN SỬA `R1-01` · `R1-02`)* · **2** CHẤP NHẬN *(`R1-06` · `R1-08` — việc orchestrator)* · **0** CÒN |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1a.md` **v0.2** *(đổi Trạng thái 9 hàng R1 + thêm 3 hàng R2)* |

## Cổng vào *(`05` §5)*
- **git:** `isp/DT1A` = `fb0cfbd` *(giấy)* ← `6903096` *(mã)* ← `2664e25` *(phiếu R1)* — khớp dòng **Commit** của mục vòng sửa *(`BG-081:138`)*. Nhánh cục bộ, ⛔ đẩy — đúng O2 = A. `git status` sạch trước khi kiểm.
- **version spec:** diff ⛔ chạm `docs/ITL/02_BA/**` *(`git diff --stat 2664e25..isp/DT1A -- docs/ITL/02_BA` rỗng)*; AP v3.1.2 sha256 R2 đo `5cf6e576ff46f088…` = `WO-080:23` ✅. ISP Step 3 · DT1a giữ nguyên như R1 đọc.
- **Ảnh thật:** `sha256sum` ba ảnh `tests/fixture/` + JSON hiện vật **trước = sau** lượt R2 *(`b59cb0d3…` · `34aa375d…` · `0d1a6fbb…` · `6ba06ada…` — `sha256sum -c` OK × 4)*. Mọi phép phá của R2 chạy trên **bản sao** `git archive` ở scratchpad.

## Cổng chạy lại *(R2 tự chạy ở worktree, `PG_DSN=…:5447/fls` · `PG_DSN_TEST=…:5447/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | `BG-081` *(vòng sửa)* nói | R2 đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_phan_loai_dong_thieu.py` | `40 passed in 7.96s` | `40 passed in 8.08s` · exit 0 *(`-rA`: **40** dòng PASSED — 20 hàm `def test_` − 2 + 19 ca + 3 checksum)* | ✅ |
| `python tools/phan_loai_dong_thieu.py` | exit 0 · 122 · 147 · 18/23 | exit 0 · `① MẪU SỐ: sổ AS-IS 9.967 dòng sổ · ghép 1-1 9.845 dòng ghép · FLS dựng lại 9.992 dòng canon` · `② … 122 / 9.967 dòng sổ = 1,22 % · rải 18/23 kỳ` · `③ … 147 / 9.992 dòng canon = 1,47 %` · `vân tay: thiếu 18047e0eb0319ea1 · ngược 6ac2463a190ff631` · `KẾT: ĐẠT` | ✅ |
| JSON `2664e25` ↔ `isp/DT1A` *(so đệ quy từng lá — kịch bản R2 `so_json.py`)* | 1 trường đổi | **1** lá khác / **2.735** nút *(cũ = mới)*: `/khong_mang_PII`; vân tay · `dem` *(122 · 147 · 23 · 18)* · `dong_thieu` · `dong_nguoc` y nguyên · **3.298** dòng · **73.677** byte | ✅ |
| `--ghi` trên **bản sao** `git archive isp/DT1A` *(xoá JSON trước)* | ghi qua tệp tạm, 0 `.tam` | exit 0 · `✅ đã ghi …` · sha256 `6ba06ada…` = tệp đã commit *(`cmp` byte y nguyên)* · **0** tệp `.tam` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` exit 0 | ✅ |
| `bash tools/dung_moi_truong_isp.sh --cong 5447 --duong-nen` · **lượt 1** | `12 failed, 2472 passed, 2 xfailed, 14 errors` · `26 = 26` · web `3 failed, 661 passed` · `3 = 3` · `KẾT: ĐẠT` | 7/7 `[ĐẠT]` môi trường *(`26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `chay 9845 / co 9967` · `fls_itl = 0 dòng`)*; toàn bộ `12 failed, 2472 passed, 2 xfailed, 14 errors in 331.28s` — mẫu số **2.500** bài *(R1 `KQ-082`: 2.476 ⇒ **+24** = 40 − 16 bài `tests/du_lieu` — đúng số bài thêm; số bài thu ≥ sàn)* · `[ĐẠT] … 26 = 26 node id (thêm 0 · bớt 0)` · `tests/du_lieu` trong tập đỏ: **0**; web `3 failed, 661 passed in 188.66s` *(664 = 664)* · `[ĐẠT] … 3 = 3` *(`wo022` · `wo022_v2` · `wo042` — SỔ THẬT)* · **`══ KẾT: ĐẠT`** exit 0 | ✅ |
| hai bài chập chờn `tests/web/test_wo032_man_cua_that.py` `AC3`/`AC7` | ⛔ đỏ ở cả hai lượt BG | **lượt 1** *(trong `--duong-nen`)*: grep `wo032_man_cua_that` trong tập đỏ web = **0** · **lượt 2** *(chạy riêng `-k "AC3 or AC7"`)*: `5 passed, 7 deselected in 1.39s` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` *(trước khi thêm hai tệp R2)* | `176 file, 1868 bang, 725 o ngay` | `176 file, 1868 bang, 725 o ngay, 104 ma QD` exit 0 | ✅ |
| `python tools/kiem_so_song.py` | *(R1: ⛔ KHÔNG ĐO ĐƯỢC ở container)* | exit 1 · `FileNotFoundError: … '.venv/Scripts/lint-imports.exe'` — **⛔ KHÔNG ĐO ĐƯỢC** *(đường nền `DUONG_NEN.md:432`; ⛔ do diff)* | ✅ *(cùng đỏ)* |
| `soi_bang_tuyen` · `kiem_thuyet_minh` · `khop_owner` | — | **⛔ chạy lại** — diff ⛔ chạm `fls/**` / tuyến / nút *(4 tệp: công cụ DATA, bài, JSON, phiếu)*; R1 đã chạy trên cùng nền | — |

## Từng phát hiện R1 → R2 tự kiểm *(⛔ tin BG — mỗi dòng có phép đo R2 tự chạy)*
Hai bản để so: **CŨ** = `git archive 2664e25` *(công cụ = `b17aaa1`)* · **MỚI** = `git archive isp/DT1A`. Bài chạy `pytest --noconftest` *(⛔ chạm kho)*.
- **Bài MỚI trên công cụ CŨ** *(chép tệp bài `isp/DT1A` vào bản CŨ)*: `6 failed, 34 passed in 7.73s` — đúng sáu bài BG kể, mỗi bài đỏ vì **thiếu hành vi**: `KeyError: 'cot_so'` · hai ca `cot_doi_nhan_*` `assert 0 == 1` *(công cụ cũ in `KẾT: ĐẠT`)* · ca `M7_phan_bo_cdt1_final` *(chỉ dòng `checksum itl_ledge_adjustment (tính lại)` cắn, ⛔ dòng `phân bố cdt1_final …`)* · `câu khai thiếu khoá cấm 'diengiai'` · tệp tạm `assert 0 == 1 … main(['--ghi'])`. Ba bài `-01` · `-02` · M8 **xanh** trên bản CŨ — đúng: hành vi đã có, ĐỎ chứng minh bằng đột biến *(dưới)*.
- **Bài CŨ trên công cụ MỚI** *(tệp bài `2664e25` vào bản MỚI)*: `16 passed in 2.69s` ⇒ ⛔ bài cũ nào cần sửa để xanh.
- **Bài MỚI trên công cụ MỚI** *(bản sao)*: `40 passed`; worktree: `40 passed in 8.08s`.
- **Kịch bản đột biến của tác giả** *(`fe_dt1a_sua/dot_bien_vong_sua.py`, sha256 `fabd7f1d…` — R2 chép nguyên vào `r2_dt1a/kb/`, chạy trên bản sao MỚI riêng)*: đường nền `40 passed · đỏ 0` · **`TỔNG: bị bắt 36 · sống 0 · không áp được 0`** · đối chứng sau khi trả nguyên `40 passed · = đường nền: True` — **khớp** `BG-081` bước 4. ⚠ Đọc kịch bản: *"bị bắt"* = THÊM ≥ 1 node đỏ; lớp đột biến = *"bỏ hẳn một `kiem`"* + M1 · M8 · V1 *(tác giả tự nêu — yếu #2)* ⇒ R2 thêm 14 đột biến lớp khác *(§Đột biến R2)*.

| Mã R1 | Mức R1 | R2 kết | Bằng chứng R2 *(tự đo)* |
|---|---|---|---|
| `DT1a-R1-01` | NÊN SỬA | **ĐÃ SỬA** | Bài `test_DT1a_B4_rieng_tu_NOI_vao_duong_do_that_email_o_hd_mid_dong_thieu` *(bài `:603`)* đi qua CLI thật trên bản sao, đòi đúng dòng `riêng tư: email ở /dong_thieu[0]/hd_mid`. Đột biến **M1** *(bỏ `loi.extend(kiem_rieng_tu(kq))`, tool `:320`)* ⇒ `1 failed, 39 passed` — node đỏ **duy nhất** là bài này. Đột biến R2 **N3** *(xoá nhánh email)* · **N4** *(⛔ đi vào list)* ⇒ bài này đỏ. Hai bài đề xuất của R1 *(`scratchpad/ban/tests/du_lieu/test_kq082_de_xuat.py`)* chép vào bản MỚI ⇒ `2 passed in 0.71s`. ⚠ Nhánh `#N/A` của cùng chốt ⛔ có ca ⇒ `DT1a-R2-01` |
| `DT1a-R1-02` | NÊN SỬA | **ĐÃ SỬA** | Bài `…doi_cho_phia_CANON_tong_van_147_nhung_VAN_TAY_NGUOC_do` *(`:373`)*: tự dựng tập 147 trước *(Đ3)*, đòi stdout vẫn `147 / 9.992 dòng canon` **và** mọi dòng lệch bắt đầu `vân tay tập ngược`. **M2** · **K24** *(bỏ `kiem` vân tay ngược)* ⇒ node đỏ duy nhất là bài này; đột biến R2 **N12** *(vân tay ngược trả thẳng hằng MONG)* ⇒ bài này đỏ |
| `DT1a-R1-03` | GHI NHẬN | **ĐÃ SỬA** | 19 ca `CA_PHA` + bài M8 `…cong_DO_thi_KHONG_ghi_de_hien_vat`. M3–M8 · M11 *(R1: sống)* nay mỗi cái ⇒ ca riêng đỏ; K01–K24 ⇒ 24/24 *(log R2 `07_dot_bien_tac_gia.log`)*. R2 đối chiếu từng lời gọi `kiem` *(23 ngoài vòng + 1 trong vòng × 4 = **27** phép so — đếm lại trong `do()`, khớp `BG-081:169`)* ↔ ca: đủ. ⚠ Docstring bài `:520-521` trỏ cổng `sổ ∖ ghép` sang sai bài ⇒ `DT1a-R2-03` |
| `DT1a-R1-04` | GHI NHẬN | **ĐÃ SỬA** | R2 lặp phá ③ ④ của R1 bằng CLI trên bản sao: ③ đổi nhãn `cdt1_mid` ↔ `cdt1_final` ⇒ exit 1 · **2** dòng lệch *(`tên cột ảnh sổ (cot, 23 tên theo thứ tự)` + `phân bố cdt1_final của dòng thiếu`)*; ④ `pay_type_classifying` ↔ `cdt1_classifying` ⇒ exit 1 · **1** dòng *(chỉ cổng tên cột)*. Thêm: thêm cột thứ 24 `so_chung_tu` ⇒ exit 1 *(checksum + tên cột)*; đổi tên cột cuối `invoice_final` ⇒ exit 1 *(chỉ tên cột)*; đổi tên `hd_mid` ⇒ exit 1 `LOI KeyError: 'hd_mid'` *(MỘT dòng — đỏ trước khi cổng tên cột kịp in; vẫn đúng Đ5)*. Bộ 23 tên: bài **dựng** từ khuôn `2 + 7 × 3` *(`do_voi_so_luong.py:54` `KHOI`)* = MONG tool = trường `cot` ảnh thật — ba nguồn khớp |
| `DT1a-R1-05` | GHI NHẬN | **ĐÃ SỬA** | R2 đo lại *(kịch bản `do_cap.py`, ⛔ import tool)*: khoá 4 trường **1.401** dòng ghép · **3.810** cặp; khoá 5 trường **764** · **1.742**; `do_voi_so_luong.py:118` · `:129` · `:138` đúng là `kiem` ba tổng 9.967 · 9.845 · 9.992; ISP `:20` · `:649` đúng 3 kỳ đầu. ⚠ Câu Đ1 ở bài `:80-82` *("grep … ⇒ 1 dòng/mẫu, đều ở sổ phát hiện R1")* đúng **lúc đo**; nay mỗi mẫu **3** dòng vì chính `BG-081:161` và bài `:80-81` trích lại — biên bản (`Đ2`), ⛔ đổi kết luận *(15 kỳ chỉ có nguồn là DT1a)* — ⛔ ghi thành phát hiện |
| `DT1a-R1-06` | GHI NHẬN | **CHẤP NHẬN** | Việc orchestrator *(lệnh giao R2: H2 giữ `_sha`/`MONG`)*. R2 đo: `isp/H2` @ `33d333b` — `tools/do_voi_so_luong.py:51` ghi *"`_sha` và `MONG` … được `tools/phan_loai_dong_thieu.py` (DT1a) import — GIỮ NGUYÊN"*, `def _sha` ở `:127`. Gộp thử `git merge-tree isp/DT1A isp/H2` ⇒ **sạch** *(cây `650f7e38…`)*; trên cây gộp: `tests/oracle/test_do_voi_hd1.py` + `tests/du_lieu` ⇒ `86 passed in 23.68s`, `phan_loai_dong_thieu.py` exit 0, `do_voi_so_luong.py` exit 0 |
| `DT1a-R1-07` | GHI NHẬN | **ĐÃ SỬA** | `_ghi_qua_tep_tam` *(tool `:357-370`)*: tệp tạm cùng thư mục → đọc lại → `os.replace`; `finally` dọn. Bài `…ghi_qua_TEP_TAM_loi_luc_thay…` *(`:684`)*. Đột biến: **V1** *(tác giả)* · R2 **N6** *(bỏ dọn)* · **N7** *(bỏ `except OSError` ⇒ traceback)* · **N13** *(tệp tạm = chính đích)* ⇒ đều bị bắt. `--ghi` trên bản sao ⇒ byte y nguyên, 0 `.tam`. ⚠ Bước *"đọc lại kiểm"* ⛔ có ca ⇒ `DT1a-R2-02` |
| `DT1a-R1-08` | GHI NHẬN | **CHẤP NHẬN** | Việc orchestrator / `fls-ba` *(lệnh giao R2)*. Quan sát: `isp/DT1B` @ `7b340c2` *(WO-095)* làm **tệp MỚI** `tools/phan_loai_ly_do.py`, ⛔ sửa `phan_loai_dong_thieu.json` — đúng Q2 = ⓐ; gộp thử `isp/DT1A` + `7b340c2` ⇒ sạch, `tests/du_lieu` `88 passed in 17.28s`. Chữ ISP `:788` · `:824` · `:836` · `:94` vẫn chờ vá — ⛔ thuộc DT1a |
| `DT1a-R1-09` | GHI NHẬN | **ĐÃ SỬA** *(chọn THU câu khai — lý do CHẤP NHẬN)* | Câu khai mới `KHAI_RIENG_TU` *(tool `:168-172`)* **dựng** từ `KHOA_CAM` + `THUOC_TINH` ⇒ phần KHOÁ bằng tập máy chặn; bài `…khong_mang_PII_BANG_tap_may_chan` *(`:629`)*: đột biến R2 **N14** *(thêm lại "Tài khoản · tiền")* ⇒ bài này + `json_DA_GHI` đỏ. Đánh giá lý do *(tool `:153-162`)*: **③** đúng và là lý do quyết định — R2 đo: ảnh sổ **23** cột, ảnh ghép **22** cột *(`dong_so` · `dong_canon` · 13 `canon_pos_*` · 7 `cls_*`)*, **0** cột Số CT/TK/tiền; `pm_join.bank` có `tien` · `ref_tho` · `cur` · `dong` nhưng `do()` chỉ đọc `dong`; JSON ra mỗi dòng đúng tập khoá *(bài B1 `:270`)* ⇒ chặn tên khoá ⛔ bao giờ sinh = cổng trên tập rỗng (Đ3). **②** đúng *(`_bo_dau`: `tien_te` → `tiente`, `uu_tien` → `uutien` đều chứa `tien`)*. **①** đúng chữ `CLAUDE.md` *("`Tên tài khoản` thì GIỮ")*, nhưng quyết định 11/09 nói về **kho** — với hiện vật trong **git**, số TK là câu còn chờ owner *(`11_BOI_CANH` §7: "52 dòng số TK đầy đủ trong git")*; kết luận vẫn đúng: mở chặn là quyết định chính sách ⇒ đã nêu thành **Q3** cho orchestrator. ⚠ Phần GIÁ TRỊ của câu khai *(email · `#N/A`)* chỉ được chứng minh một nửa ⇒ `DT1a-R2-01` |

**Bài CŨ bị sửa** — `test_DT1a_B2_doi_cho_CUNG_KY_tong_van_122_nhung_VAN_TAY_do` *(bài `:340`)*: R2 kết luận **⛔ làm yếu khẳng định**.
- Diff bài: **0** dòng `assert` bị bỏ · **33** dòng `assert` thêm; ở bài này chỉ đổi `khoa` *(4 → 5 trường, thêm `cdt1_final`)* + docstring — khẳng định `loi and all("vân tay" in d …)` nguyên chữ.
- Tác giả khai *"chưa từng đỏ — cặp tình cờ trùng `cdt1_final`"*: R2 đo độc lập *(`do_cap.py`)* — cặp đầu tiên **cả hai** khoá đều là chỉ số `646` · `dong_so 656 → 744`, `cdt1_final` hai đầu cùng một mã ⇒ bản 4 trường trên công cụ MỚI vẫn xanh *(chạy bài CŨ trên công cụ MỚI: `16 passed`)* ⇒ ⛔ phải "sửa bài cho xanh".
- Thêm `cdt1_final` vào khoá là **giữ tiền đề** *"mọi phân bố có MONG y nguyên"* sau khi `-04` thêm MONG `cdt1_final` — khoá hẹp hơn *(1.401 → 764 dòng ứng viên, Đ3 vẫn ≫ 0)*, bài **chặt hơn**: nếu dữ liệu đổi khiến cặp đầu khác `cdt1_final`, bản 4 trường sẽ đỏ vì phân bố `cdt1_final` *(sai lý do)*, bản 5 trường vẫn đo đúng thứ nó canh.

**PII · ký tự vô hình** *(quét **540** dòng THÊM của diff — kịch bản `quet_vo_hinh.py`)*: ký tự `Cf`/`Cc`/`Co`/`Cs`/`Zl`/`Zp`/khoảng trắng lạ **0** · dòng ⛔ NFC **0** · tab **0** · khoảng trắng cuối dòng **0** · dạng email **2** dòng, đều `ke-toan@vi-du.vn` *(địa chỉ GIẢ của bài cấy, miền `vi-du`)* · chuỗi số ≥ 9 chữ số **0** · `FT` + ≥ 8 ký tự **0** · số dạng tiền ≥ 1.000.000 **0**. Giá trị `cdt1_final` trong MONG *(mã trung tâm chi phí + tên dự án/công ty)* đã có trong JSON từ `b17aaa1` *(R1 đã soát)* — ⛔ tên người, ⛔ Số CT. ⛔ có máy quét email toàn repo nào trên `tests/` *(grep `MAU_EMAIL` ở `tests`/`tools`/`fls`: chỉ hai tệp DT1a)*. Bảng mới trong `BG-081` từ dòng 130: **27** hàng, lệch số cột **0** *(⛔ dấu `\|` trần)*.

## Đột biến R2 *(lớp NGOÀI kịch bản tác giả — `r2_dt1a/kb/dot_bien_r2.py`, bản sao `git archive isp/DT1A`, `pytest --noconftest` tệp bài DT1a)*
Đường nền bản sao `40 passed · đỏ 0`; mỗi mẫu khớp **đúng 1** lần *(0 "không áp được")*; đối chứng sau khi trả nguyên `40 passed · = đường nền: True`. **`TỔNG R2: bị bắt 11 · sống 3 · không áp được 0`**.

| Đột biến | Kết | Bài bắt |
|---|---|---|
| N1 xoá nhánh `#N/A` *(`MAU_REF_TRONG_LOI`)* trong `kiem_rieng_tu` | **⛔ SỐNG** `40 passed` | — ⇒ `DT1a-R2-01` |
| N2 xoá nhánh khoá cấm | bị bắt | `…tool_TU_CHAN…` |
| N3 xoá nhánh email | bị bắt | `…NOI_vao_duong_do_that…` · `…tool_TU_CHAN…` |
| N4 `kiem_rieng_tu` ⛔ đi vào list | bị bắt | như N3 |
| N5 xoá bước đọc lại tệp tạm | **⛔ SỐNG** `40 passed` | — ⇒ `DT1a-R2-02` |
| N6 bỏ dọn tệp tạm *(`finally`)* | bị bắt | `…ghi_qua_TEP_TAM…` |
| N7 `except OSError` ⇒ `except ZeroDivisionError` *(traceback)* | bị bắt | `…ghi_qua_TEP_TAM…` |
| N8 cổng tên cột chỉ so 22 tên đầu | **⛔ SỐNG** `40 passed` | — *(**tương đương về nghĩa**: cột 23 `invoice_final` ⛔ được `do()` giải mã — đổi nhãn nó ⛔ đổi đầu ra; R2 ⛔ ghi thành phát hiện)* |
| N9 cổng tên cột so theo TẬP *(bỏ thứ tự)* | bị bắt | hai ca `cot_doi_nhan_*` |
| N10 `PHAN_BO_CO_MONG` bỏ `cdt1_final` | bị bắt | `M7_phan_bo_cdt1_final` · `cot_doi_nhan_cdt1_mid_final` |
| N11 `kiem` chỉ so KHOÁ khi `mong` là dict | bị bắt | ba ca `M7_*` |
| N12 vân tay ngược = hằng MONG | bị bắt | `…doi_cho_phia_CANON…` |
| N13 tệp tạm = chính đích | bị bắt | `…KHONG_ghi_de…` · `…ghi_qua_TEP_TAM…` |
| N14 câu khai thêm lại "Tài khoản · tiền" | bị bắt | `…khong_mang_PII_BANG…` · `json_DA_GHI…` |
| K17 *(của tác giả — bỏ cổng `dòng sổ ⛔ ghép (sổ ∖ ghép)`)*, chạy riêng `-k bo_MOT` | bài `…bo_MOT_dong…` **PASSED** `1 passed, 39 deselected` | cổng do `CA_PHA` `M4_*` + `MONG_so_dong_so` bắt ⇒ `DT1a-R2-03` |

## Bảng AC *(= test ID ISP mục 6 — R2 đo lại trên `isp/DT1A`)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** · `DT1a-B1` | 122 dòng; 147 chiều ngược; phân bố kỳ có MONG | Công cụ exit 0: **122** / 9.967 dòng sổ · **147** / 9.992 dòng canon · 18/23 kỳ; vân tay `18047e0eb0319ea1` / `6ac2463a190ff631` *(= JSON `2664e25` — danh sách 122 + 147 y nguyên từng phần tử)*. Bốn bài B1 PASSED, nay thêm MONG `cdt1_final` *(Σ 122)* + bộ 23 tên cột | **ĐẠT** |
| **AC-2** · `DT1a-B2` | cổng ĐỎ (123 ≠ 122) rồi trả nguyên (Đ5) | Bỏ 1 dòng ghép trên bản sao ⇒ exit 1, có dòng `dòng sổ ⛔ ghép (sổ ∖ ghép): đo 123 · mong 122` *(R1 + R2 đều thấy)*; trả nguyên ⇒ exit 0; ảnh thật sha256 trước = sau. ⚠ Bài AC-2 *(`:331`)* ⛔ đòi CHÍNH dòng ấy ⇒ `DT1a-R2-03` *(GHI NHẬN — cổng vẫn được ca `CA_PHA` canh)* | **ĐẠT** |
| **AC-3** · `DT1a-B3` | in 9.967 dòng sổ và 9.845 dòng ghép trước tỷ lệ | stdout dòng `①` mang `9.967 dòng sổ` · `9.845 dòng ghép` · `9.992 dòng canon`, đứng trước `%` đầu tiên *(dòng `②`)*; M9 *(bỏ phép mẫu số 0)* ⇒ bị bắt | **ĐẠT** |
| **AC-4** · `DT1a-B4` | 0 khoá `dien_giai` / `so_chung_tu` / `email` | Bài quét riêng `…json_ra_0_khoa…` PASSED trên JSON thật *(R2 đếm **1.940** khoá đã quét; bài đòi ≥ 538 = `(122 + 147) × 2` — Đ3)*; JSON chỉ đổi trường `khong_mang_PII` *(chuỗi — ⛔ khoá mới)*; chốt tự chặn nay có bài nối đường đo *(`R1-01` đã sửa)*. ⚠ nhánh `#N/A` của chốt tự chặn ⛔ có ca ⇒ `DT1a-R2-01` *(⛔ làm AC-4 trượt: AC đòi JSON ra sạch — đã đo sạch)* | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 3 + `CLAUDE.md` Đ1–Đ5)* | **ĐẠT có ghi chú.** Vòng sửa **chỉ thêm** cổng *(tên cột · phân bố `cdt1_final`)*, bài và một đường ghi an toàn — ⛔ đổi định nghĩa hai tập *(122 / 147 y nguyên từng phần tử)*. Đ5: mỗi `kiem` có ca phá riêng *(36/36 tác giả · 11/14 R2; ba con sống: hai lời khai chưa có ca + một đột biến tương đương)*. Đ1/Đ4: ba câu R1-05 đã sửa đúng số; ba câu mới khai rộng hơn bài *(`DT1a-R2-01…03`)* | §Từng phát hiện R1 · §Đột biến R2 · sổ v0.2 |
| **Dữ liệu** *(ảnh đóng băng trong repo; ⛔ kho thật — container ⛔ có sổ thật)* | **ĐẠT.** JSON: 1 lá khác / 2.735 nút; `--ghi` lại trên bản sao ⇒ byte y nguyên. Định nghĩa khoá giữ nguyên *(R1 đã chứng minh hai nguồn 29.535/29.535 ô cls)*. Cụm 5447: K7 `fls_itl = 0 dòng`; công cụ ⛔ mở kết nối | `so_json.py` · `09_ghi_ban_sao.log` · `05_duong_nen_luot1.log` |
| **Màn hình** | **N/A** — ISP §4 *"Frontend: N/A — bước dữ liệu"*; diff ⛔ chạm `fls/web/**` | `git diff --stat 2664e25..isp/DT1A` *(4 tệp)* |

**Quyền làn:** 4 tệp nằm trong bảng tệp làn DATA *(ISP `:94`)* + phiếu `BG-081` *(chỉ thêm — `+68`, `−0`)*; ⛔ chạm `tools/do_voi_so_luong.py` *(làn BE-HC)*, fixture, ISP, AP, `WO-080`, dashboard, `TIEN_DO.md`.

## Phát hiện mới *(chi tiết đầy đủ + luật phòng tái phạm: sổ v0.2)*
| Mã | Lớp | Mức *(↔ `10` §3.4)* | Nơi | Tái hiện | Khuyến nghị | Gửi |
|---|---|---|---|---|---|---|
| `DT1a-R2-01` | B1 | GHI NHẬN *(`NHE`)* | `tools/phan_loai_dong_thieu.py:219-220` *(nhánh)* · `:168-172` *(câu khai)* · `:44-48` · bài `:594-600` · `:629-643` · `:520-522` | Đột biến N1 *(xoá nhánh `MAU_REF_TRONG_LOI`)* ⇒ `40 passed`. Câu khai mới của JSON nói máy chặn *"ô lỗi #N/A nhúng mã giao dịch"*; bài *"BẰNG tập máy chặn"* chỉ so phần `KHOA_CAM`. Vô hại hôm nay: ảnh sổ **0 / 1.575** giá trị chứa `Did not find value` *(Đ3)*; máy quét riêng của bài có nhánh `#N/A` và quét JSON thật | Ca `#N/A` cho bài nối đường đo *(§Bài thử đề xuất ①)* | `DEV` |
| `DT1a-R2-02` | B1 | GHI NHẬN | `tools/phan_loai_dong_thieu.py:366-367` · `:358` · `BG-081:163` | Đột biến N5 *(xoá bước đọc lại tệp tạm)* ⇒ `40 passed`; lời khai *"đọc lại kiểm"* ⛔ có ca hỏng | Ca ghi CỤT tệp tạm *(§Bài thử đề xuất ②)*, hoặc bỏ chữ khỏi lời khai | `DEV` |
| `DT1a-R2-03` | B1 | GHI NHẬN | bài `:520-521` · `:331` | Đột biến K17 *(bỏ cổng `dòng sổ ⛔ ghép (sổ ∖ ghép)`)* ⇒ bài AC-2 `…bo_MOT_dong…` PASSED — khẳng định `"123" in d and "122" in d` thoả bởi dòng cổng HIỆU *(`đo 122 · mong 123`)*; docstring mới trỏ cổng ấy sang bài này. Cổng vẫn được hai ca `CA_PHA` bắt | `:331` đòi đúng dòng `dòng sổ ⛔ ghép (sổ ∖ ghép): đo 123 · mong 122`; sửa `:520-521` | `DEV` |

**Theo mức:** CHẶN **0** · NÊN SỬA **0** · GHI NHẬN **3** — lớp **B1** cả 3 *(A1 · A2 · B2: 0 — bước ⛔ chạm FE, ⛔ chạm LLM)*. Ba phát hiện cùng một lớp gốc: **lời khai viết ở vòng sửa rộng hơn bài chứng minh nó** — đúng thứ vòng sửa vừa đi sửa ở `R1-05` · `R1-09`, nay ở mức nhánh/bước.

## Bài thử ĐỀ XUẤT *(⛔ commit — orchestrator chỉ cho R2 commit phiếu + sổ; Dev đưa vào `tests/du_lieu/` nếu nhận khuyến nghị)*
Tệp `scratchpad/r2_dt1a/de_xuat/test_kq083_de_xuat.py` *(mượn trợ thủ của bài DT1a)*; kịch bản chứng minh `r2_dt1a/kb/chung_do_de_xuat_r2.sh` — bản sao riêng, `pytest --noconftest`:

| Bài | Đã chứng minh ĐỎ bằng cách | Xanh |
|---|---|---|
| ① `test_R2_01_rieng_tu_O_LOI_NA_NOI_vao_duong_do_that` — bản sao; thêm `#N/A (Did not find value 'FT1' in VLOOKUP evaluation.)` vào `bang_gia_tri`, trỏ ô `hd_mid` của dòng THIẾU đầu; CLI `--thu-muc` ⇒ đòi exit 1 **và** đúng dòng `riêng tư: ô lỗi nhúng mã giao dịch ở /dong_thieu[0]/hd_mid` | N1 ⇒ `1 failed, 1 passed` — bài này FAILED | `isp/DT1A` ⇒ PASSED · trả nguyên ⇒ PASSED · công cụ cũ `b17aaa1` ⇒ PASSED *(nhánh có từ đầu — cái mới là lời khai)* |
| ② `test_R2_02_doc_lai_tep_tam_LECH_thi_hien_vat_cu_Y_NGUYEN` — `main(["--ghi"])` trong tiến trình *(`_tool_moi` + `_tro_ve_ban_sao`)*; vá `pathlib.Path.write_text` chỉ cho tên `.tam` ghi NỬA nội dung ⇒ đòi exit 1, hiện vật cũ y nguyên byte, ⛔ tệp tạm sót | N5 ⇒ bài này FAILED · công cụ cũ `b17aaa1` *(ghi thẳng)* ⇒ FAILED | `isp/DT1A` ⇒ PASSED · trả nguyên ⇒ PASSED |

## Câu hỏi của vòng sửa *(Q3 · Q4 — orchestrator chốt; R2 chỉ góp ý có số)*
- **Q3** *(tập chặn riêng tư rộng hơn ba khoá?)*: R2 đồng ý **ⓐ** *(giữ, ghi vào `WO` DT1b)*. Số: ảnh đầu vào DT1a **0** cột Số CT/TK/tiền ⇒ mở thêm hôm nay là cổng trên tập rỗng. Nhưng DT1b `7b340c2` đọc nguồn có Số CT/TK/tiền *(docstring `tools/phan_loai_ly_do.py:83-95` ở `isp/DT1B` tự khai chốt riêng R1–R6: `KHOA_CAM` riêng có thêm `soct`, R5 chặn token trùng Số CT / tiền ≥ 6 chữ số của đầu vào, câu `khong_mang_PII` = đúng tập máy chặn theo luật `DT1a-R1-09`)* — nên chỗ đặt chặn rộng hơn là **công cụ DT1b**, ⛔ DT1a; R1/R2/R3 của DT1b nên soát câu ấy theo luật `DT1a-R2-01` *(mỗi thứ được khai phải có một ca phá riêng)*.
- **Q4** *(kịch bản đột biến vào repo?)*: R2 đồng ý **ⓐ** cho bước này. Ghi chú đo: một lượt kịch bản tác giả trên container = **38** lượt pytest × ~8,5 s ≈ **5,4** phút; lớp "bỏ một `kiem`" bỏ sót đúng ba con sống của R2 — nếu sau này thành cổng thì nên thêm lớp nhánh/bước *(như N1 · N5)*.

## Môi trường R2 để lại
Cụm `5447` *(`/home/user/fls-pg16-5447`)* **đang chạy** theo yêu cầu orchestrator. Worktree chỉ đổi hai tệp của R2 *(phiếu này + sổ)*. Log + kịch bản ở scratchpad phiên `…/scratchpad/r2_dt1a/` *(⛔ trong repo)*: `01_pytest_moi.log` · `02_tool.log` · `03_lint.log` · `05_duong_nen_luot1.log` *(+ `05a`/`05b` log pytest)* · `06_wo032_rieng.log` · `07_dot_bien_tac_gia.log` · `08_dot_bien_r2.log` · `09_ghi_ban_sao.log` · `10_bai_moi_tren_tool_cu.log` · `11_bai_cu_tren_tool_moi.log` · `12_gop_DT1A_H2.log` · `14_de_xuat_r2.log` · `16_pha_cot.log` · `17_kiem_so_song.log` · `18_gop_DT1A_DT1B.log` · kịch bản `kb/` · bản sao `ban_*`.
