# BG-117 — bàn giao `WO-116` *(ISP 3.1.2 · Step 9 · FG)* — F03 'Cổng hôm nay' hiện cổng HD1 đọc tuyến thật

| | |
|---|---|
| **Thuộc** | `WO-116` *(dải phiếu: WO-116 · BG-117 · R1/R2/R3 = KQ-118/119/120)* |
| **Phát bởi** | `fls-dev` *(làn **FE**, tác giả)* · phiên cloud · 2026-11-17 |
| **Nhận** | `fls-test` — R1 `KQ-118` · R2 `KQ-119` · R3 `KQ-120` |
| **Commit** | nhánh **cục bộ** `isp/FG` @ **`4933038`** *(mã bài + sàn Q8)* — nền `4dfb7bd` *(ngọn CG1 sau R1 — `KQ-103`)*; đẩy `claude/bold-galileo-zukpaf-isp/FG`. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-fg` · cụm PG riêng cổng **5436** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 9 · FG** *(§1 · §2.1 · Step 7 CG1 để biết `/gates`)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §5.2 UF-2 · §5.3.1 HD1 · Hình 5.3.3 · `fls/web/tep/man_f03.js` *(`_muc`, lớp `.gate.unk`)* · `BG-102` · `KQ-103` *(hợp đồng `/gates` CG1)* · `CLAUDE.md` Đ1–Đ5 · Bẫy · Riêng tư · `WO-116` |

## Cổng vào
- git thật: nền `isp/FG` = `4dfb7bd KQ-103: R1 kiểm CG1 (ISP 3.1.2 · Step 7 · WO-101) — ĐẠT, 0 CHẶN` — đúng nền WO *(`git rev-parse isp/FG` mở đầu `4dfb7bd`)*. `git status` sạch trước khi làm.
- version hợp đồng: ISP 3.1.2 · AP v3.1.2. Ghi kho thật: `KHONG` *(WO §Dữ liệu)*.
- **⛔ chạm** *(ràng buộc WO)*: tuyến `/gates`, `fls/repo/doc_bao_cao.py`, `fls/api/cua.py`/`xu_ly.py` *(CG1 — DÙNG, ⛔ sửa)*; màn mới; `TIEN_DO.md`, Dashboard, `08_CHANGELOG`. Hợp đồng H2 ↔ CG1: FG chỉ đọc khoá `/gates` trả, ⛔ đọc thẳng `voi_so_luong.json` *(bài lấy envelope qua HTTP thật, ⛔ mở tệp đo)*.
- **`man_f03.js` KHÔNG sửa** *(đo được: lý do 23 kỳ ⛔ tràn ở 390 px — xem AC-3)*. `git diff 4dfb7bd -- fls/` = rỗng.

## Substep 1 — test cases · kế hoạch · giới hạn
1. **Test cases** *(mục 6 ISP, phủ mọi dòng mục 8)*: `FG-F1` *(tệp đo thật qua máy thật ⇒ render)* · `FG-F2` *(tệp vắng ⇒ hai thẻ `.gate.unk`)* · `FG-F3` *(lý do 23 kỳ ở 390 px ⛔ tràn)* · `FG-F4` *(hồi quy `tests/web` — đo bằng `--duong-nen`, ⛔ bài mới)*.
2. **Kế hoạch tối thiểu**: một tệp bài `tests/web/test_isp_f03_hd.py`. FG-F1/F2 đi qua **máy chủ thử** *(`cua.dung_may` + `phuc_vu.lam_nguoi_phuc_vu`)* lấy envelope THẬT của `GET /gates`, rồi render `man_f03.js` qua **node headless** *(`tests/web/khung_node._chay` + `dom_gia.js`)* — hai vế đối chiếu bằng CHÍNH chuỗi tuyến trả. `man_f03.js` sửa **chỉ nếu** lý do dài vỡ thẻ — đo thấy ⛔ vỡ ⇒ ⛔ sửa.
3. **Giới hạn** *(ISP §3)*: thẻ `HD2` 'KHÔNG ĐO ĐƯỢC' tới khi CG2 + H4 xong — đúng nghĩa *(ngoài bước)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tests/web/test_isp_f03_hd.py` *(mới, 281 dòng)* | **3** bài *(`--collect-only`)*: `FG-F1` *(máy thật + `tep_do` thật ⇒ `FINAL` ĐẠT · `HD1_THANG` KHÔNG ĐẠT `5/23` · số 'chưa đo được' trên màn = tuyến trả)* · `FG-F2` *(tệp vắng ⇒ `FINAL`+`HD1_THANG` lớp `.gate.unk`, ⛔ xanh)* · `FG-F3` *(Chromium thật ở 390 px ⇒ thẻ HD1 `scrollWidth ≤ clientWidth`)*. FG-F1/F2 qua `khung_node._chay(tep=[thanh_phan·goi_cua·trang_thai·man_f03], vo="")` + envelope HTTP thật nạp vào `_TRA['/gates']` |
| `tools/dung_moi_truong_isp.sh` *(+6 −2)* | **Q8 = A**: `MONG_PYTEST_TOAN_BO` **2493 → 2496** · `MONG_PYTEST_WEB` **664 → 667** *(+3 = `pytest --collect-only tests/web/test_isp_f03_hd.py`)* + chú thích vì sao +3 và ghi chú FG-F3 cần Chromium *(thiếu ⇒ `skipped>0` ⇒ `--duong-nen` ĐỎ, đúng Đ5)* |
| `tests/test_dung_moi_truong_isp.py` *(+4 −2)* | bài ghim `test_S0_R2_03_hang_mau_so_khai_MOT_cho`: `["2493"]`→`["2496"]`, `["664"]`→`["667"]`, cùng commit *(lo gốc: số khai MỘT chỗ, ghim đúng số)* |

## Chứng minh ĐỎ *(behavior sẵn có ⇒ mỗi cổng phá → chạy → cắn → trả nguyên — Việc #2)*
| Cổng | Phá | Chạy | Cắn | Trả |
|---|---|---|---|---|
| FG-F1 | `_muc(dat===true)` → `{lop:'fail'}` *(thẻ ĐẠT hoá đỏ)* | `pytest …::test_FG_F1…` | `1 failed` · `test_isp_f03_hd.py:170 AssertionError` *(`"pass" in _lop(final)`)* | `git checkout -- man_f03.js` ⇒ xanh lại |
| FG-F2 | `_muc(dat===null)` → `{lop:'pass'}` *(cổng chưa đo hoá xanh — phá luật số 1)* | `pytest …::test_FG_F2…` | `1 failed` *(`"unk" in _lop(card)`)* | trả nguyên ⇒ xanh |
| FG-F3 | lý do render `white-space:nowrap` *(ép ⛔ xuống dòng)* | `pytest …::test_FG_F3…` | `1 failed` *(thẻ HD1 `over=true`: sw>cw ở 390 px)* | trả nguyên ⇒ xanh |

## Cổng *(kết quả nguyên văn — `PG_DSN=…:5436/fls` · `PG_DSN_TEST=…:5436/fls_test` · `PYTHONUTF8=1`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/web/test_isp_f03_hd.py` | exit 0 · `3 passed in 2.88s` |
| `python -m pytest tests/web/test_isp_f03_hd.py --collect-only -q` | `tests/web/test_isp_f03_hd.py: 3` |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5436` *(script NHÁNH — GOC = …/isp-fg)* | exit 0 · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` — 7/7 `[ĐẠT]` môi trường *(gồm `di trú + pg_verify 26/26 · 25 bảng/view 0 lệch` · `lint-imports 11 kept, 0 broken` · `HD1 do_voi_so_luong chay 9845 / co 9967` · `kho fls RỖNG fls_itl = 0 dòng`)*; toàn bộ `12 failed, 2575 passed, 2 xfailed, 14 errors in 352.03s` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0) · chạy 2603 bài (mong ≥ 2496) · skipped 0 · deselected 0`; `tests/web` `3 failed, 664 passed in 186.04s` · `[ĐẠT] … tests/web 3 = 3 node id (thêm 0 · bớt 0) · chạy 667 bài (mong ≥ 667) · skipped 0 · deselected 0` |
| `.venv/bin/lint-imports` | exit 0 · `Contracts: 11 kept, 0 broken.` |

## Bằng chứng từng AC
| AC | Mong | Bằng chứng *(PASSED trên `isp/FG`)* | Kết |
|---|---|---|---|
| **AC-1** · FG-F1 | mở F03 qua máy thật + tệp đo thật ⇒ `FINAL` ĐẠT · `HD1_THANG` KHÔNG ĐẠT `5/23` · số 'chưa đo được' = tuyến trả | `test_FG_F1_tep_do_that_FINAL_dat_HD1_khong_dat_5_tren_23`: tuyến trả `FINAL dat=True` · `HD1_THANG dat=False` · `da_do`="5/23 kỳ đạt" · `chua_do_duoc=4`; màn vẽ thẻ `.gate.pass` chứa `ĐẠT`+da_do FINAL, `.gate.fail` chứa `KHÔNG ĐẠT`+`5/23 kỳ đạt`, `.note` chứa `4 ⛔ chưa đo được` *(= tuyến trả, ⛔ hằng số)* | đạt |
| **AC-2** · FG-F2 | tệp vắng ⇒ hai thẻ `.gate.unk` 'KHÔNG ĐO ĐƯỢC', ⛔ xanh | `test_FG_F2_tep_do_vang_hai_the_KHONG_DO_DUOC_khong_xanh`: `tep_do` = đường ⛔ có tệp ⇒ `FINAL`+`HD1_THANG` `dat=None`; màn vẽ cả hai lớp `unk`, `pass` KHÔNG trong lớp, văn bản `KHÔNG ĐO ĐƯỢC` | đạt |
| **AC-3** · FG-F3 | lý do 23 kỳ ở 390 px ⇒ ⛔ tràn ngang | `test_FG_F3_ly_do_23_ky_khong_tran_ngang_o_390px` *(Chromium thật)*: thẻ HD1 mang `5/23` *(tập ⛔ rỗng)*, `over=False` *(scrollWidth==clientWidth)* ở 390 px *(đo thêm 360 px lúc dò: cũng ⛔ tràn)*. ⇒ `man_f03.js` ⛔ cần sửa | đạt |
| **AC-4** · FG-F4 | `tests/web` sẵn có xanh *(token màu · một bản mẫu · phím)* | `--duong-nen` `tests/web`: `3 failed, 664 passed` · `3 = 3 node id (thêm 0 · bớt 0)` · chạy 667 (mong ≥ 667) — tập đỏ = đường nền *(thêm 0 · bớt 0)*, skipped 0 | đạt |
| **AC-5** · Q8 | nhánh có `MONG_PYTEST_*` CG1 ⇒ nâng cùng commit theo `--collect-only` | `MONG_PYTEST_WEB 664→667` · `MONG_PYTEST_TOAN_BO 2493→2496` *(+3)* ở cùng commit mã; bài ghim đổi cùng chỗ; `--duong-nen` `chạy 2603 bài (mong ≥ 2496)` · `26 = 26 node id (thêm 0 · bớt 0)` · skipped 0 | đạt |

## Số ra *(nguyên văn `GET /api/fls/v1/gates` qua máy thử, kho `fls_test` 5436 RỖNG, tệp đo mặc định nhánh)*
- `FINAL` · `DAT` · `da_do` = `69.510/69.510 ô (ô Final FLS tính lại = Final AS-IS · 7 khối × 9.930 dòng giữ sau tự soi)`
- `HD1_THANG` · `KHONG DAT` · `da_do` = `5/23 kỳ đạt` · `ly_do` = `kỳ đỏ 18/23 — … 2026-07: 23 · 2026-08: 13 (Σ 122 dòng) · số của ảnh sổ đóng băng ngày 2026-08-26 (⛔ kho sống) · ⛔ gồm chế độ tự sinh (H15)…`
- tóm tuyến: tệp thật `dat=3 · khong_dat=2 · chua_do_duoc=4`; tệp vắng `dat=2 · khong_dat=1 · chua_do_duoc=6` *(+2 đúng = hợp đồng BG-102)*.

## Kho thật
- `KHONG_CHAM` — bài chỉ đọc kho `fls_test` RỖNG; ⛔ ghi.

## Cách chạy để xem *(chạm UI)*
- `tools/chay_cua.py` cổng `8088` chế độ `chỉ đọc`, mở F03 — hoặc dò lại: máy thử + Chromium ở 390 px *(nháp `/tmp/fg/probe_overflow.*`)*.

## Dev tự thấy còn yếu / Câu hỏi
- **Q-FG-1 *(công cụ FG-F3 — cần R1 xác nhận)*.** ISP đặt công cụ FE = "node headless `khung_node` + `dom_gia.js`". Nhưng `dom_gia.js` **tự khai** *(dòng 11–16)* rằng câu hỏi pixel bố cục *("346px có đủ không")* nó **⛔ kiểm được, còn nằm ở `B7 · UAT`* — nó ⛔ có `offsetWidth`/`scrollWidth` thật. ⇒ "tràn ngang ở 390 px" của AC-3 là câu pixel, chỉ trình duyệt thật trả được.
  - **Khuyến nghị A *(đã làm)*:** FG-F3 đo bằng **Chromium thật** *(headless, tất định; `/opt/pw-browsers`)*, skip khi thiếu trình duyệt — nhưng skip làm `--duong-nen` ĐỎ *(Đ5: pixel ⛔ đo được là ĐỎ)*, nên môi trường gộp phải có Chromium. Honest: đo đúng cái AC nói.
  - **Phương án B:** chuyển FG-F3 thành bài **cấu trúc** dom_gia *(khẳng định lý do là khối chữ xuống-dòng-được, ⛔ `nowrap`)* + chuyển câu pixel 390 px sang `B7 · UAT`. Nhẹ phụ thuộc, nhưng là cổng **ĐẠI DIỆN**, ⛔ đo pixel thật *(rủi ro Đ4)*.
  - R1 chọn A hay B? Mặc định giữ **A**.
- **Giới hạn đo được *(ngoài phạm vi, ⛔ thuộc AC-3)*:** ở 390 px **cả trang** F03 tràn ngang *(`documentElement.scrollWidth=690 > 390`)* — do bố cục rail/shell `.wrap` *(`grid-template-columns: var(--rail-w) …`)* + bảng `mẫu số`/`độ phủ`, ⛔ do thẻ cổng HD1 *(thẻ `scrollWidth==clientWidth`)*. Đây là việc đáp ứng responsive của cả màn, WO loại trừ *(⛔ màn mới · ⛔ khoan từng dòng)* — nêu để R1 biết, ⛔ sửa trong bước này.
