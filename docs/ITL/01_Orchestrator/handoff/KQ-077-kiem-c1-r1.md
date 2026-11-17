# KQ-077 — biên bản kiểm `BG-076` *(ISP 3.1.2 · Step 2 · `C1` · vòng **R1** — quét toàn bộ diff `329fa68..510cdf8`)*

| | |
|---|---|
| **Thuộc** | [`BG-076`](BG-076-ban-giao-wo-075.md) · [`WO-075`](WO-075-isp-c1-ix-fx-doc-tinh.md) |
| **Kiểm bởi** | `fls-test` *(R1 — phiên mới, độc lập)* · 2026-11-16 · cụm reviewer làn BE-CF cổng **5444** |
| **Phán quyết** | **`ĐẠT`** *(vòng R1 · thang ISP: **0 CHẶN**)* — **5/5 AC ĐẠT** *(`C1-B1…B5`)* · mục 8 dòng 1–2 ĐẠT, dòng 3–4 chờ R2/R3. **7** phát hiện: **0** CHẶN · **2** NÊN SỬA *(`C1-R1-01` hai nhánh của `thieu` ⛔ bài ghim · `C1-R1-02` `nguon_tinh` nới cổng ⓓ cho mọi tệp có thật)* · **5** GHI NHẬN |
| ⚠ **Ranh giới phán quyết** | NÊN SỬA = `NANG` *(`10_HOP_DONG_AGENT.md` §3.4)* ⇒ ⛔ chặn PUSH theo ISP Step 2 mục 8 *("phát hiện chặn = 0")*; `WO-075` ⛔ đóng cho tới khi R2 *(`KQ-078`)* xác nhận hai NÊN SỬA đã sửa **hoặc** orchestrator ghi lý do chấp nhận |
| **Sổ phát hiện** | [`docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C1.md`](../../04_Test/review/SO_PHAT_HIEN_ISP-3.1_C1.md) v0.1 *(tệp riêng — orchestrator gộp vào sổ chung)* |
| **Phạm vi R1** | 3 commit tác giả `9c964f4` *(tuyến + kiểm)* · `5582246` *(`yyyymm` → `int`)* · `510cdf8` *(phiếu)*; commit gộp `6086395` *(orchestrator — `BA-07` v3.15 §4i)* chỉ kiểm *"làm `test_ba07_phu_het_tuyen.py` xanh mà ⛔ che lỗi nào"* ⇒ `C1-R1-03` |
| ⛔ **Không tính là lệch spec** | quyết định orchestrator có trước R1: `yyyymm` = **`int`** *(ISP mục 6 ghi `['202407']` có nháy)* · `lac` = tháng trước `thang_dau`, lỗ trong dải = `thieu` · tỷ giá ra JSON là **chuỗi** · `trang_thai` = trạng thái ký *(`chua_ky` tới C7)* · `BA-07` do orchestrator khai |

## Cổng vào
| Kiểm | Kết quả |
|---|---|
| git | worktree `isp/C1` HEAD = `6086395` *(gộp)* ← `510cdf8` *(phiếu)* ← `5582246` *(mã cuối, `BG-076` trỏ)* ← `9c964f4` ← `329fa68` *(nền wave 1)* ✔. Cây sạch trước kiểm *(`git status` 0 dòng)*. Nhánh **cục bộ, ⛔ đẩy** — đúng O2 = A *(BG: orchestrator gộp sau R3)*, ⛔ phải lỗi |
| spec | ISP **v3.1.2** Step 2 · C1 = bản `WO-075` ghi ✔ · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` sha256 đo lại `5cf6e576ff46f088…` = `WO-075` ✔ |
| làn | **9/9** tệp diff thuộc làn BE-CF *(ISP §2.1: `fls/cau_hinh/**` · `bang_tuyen.py` · `xu_ly.py` · `tests/cau_hinh/**` · `tests/api/test_isp_*.py` · `tools/soi_bang_tuyen.py`)* + phiếu `BG-076`. ⛔ chạm kho/di trú *(C5)*, ⛔ ký *(C7)* — grep `sign\|da_ky` trên 9 tệp diff = **5** dòng, **0** dòng mã ký *(2 chú thích mới `xu_ly.py:1010` · `fx.py:71` · 2 khớp nhầm trong mã cũ `Design`/`isinstance` · 1 dòng phiếu)* |
| môi trường | `bash tools/dung_moi_truong_isp.sh --cong 5444` ⇒ **7/7 `[ĐẠT]`** · `KẾT: ĐẠT` *(venv Python 3.13.18 · psycopg 3.3.9 · pytest 9.2.0 · import-linter 2.16 · `26/26 di trú áp · pg_verify khớp 25 bảng/view` · `11 kept` · `chay 9845 / co 9967` · `fls_itl = 0 dòng`)*. `PG_DSN=…5444/fls` · `PG_DSN_TEST=…5444/fls_test` · `PYTHONUTF8=1` · `PYTEST_ADDOPTS` **⛔ đặt**. Log: `scratchpad/r1_c1/` *(thư mục riêng)* |
| kho thật | **⛔ CHẠM** — container ⛔ có sổ thật. Kho `fls` cụm 5444: `fls_itl` **0** dòng; lượt gọi tuyến của R1 dùng kết nối **chỉ đọc** vào kho `fls` *(⛔ `fls_test`, để ⛔ giẫm lượt `--duong-nen` đang chạy)* |
| ký tự vô hình · PII | **9/9** tệp diff: **0** ký tự vô hình *(NBSP · BOM · U+200B–D · U+2000–200A · U+2028/9 · U+202F · U+205F · U+3000 · NEL · U+001C–1F · VT · FF)*; email duy nhất `ke.toan.thu@vi-du.invalid` *(miền `.invalid` của bài HTTP)*. Nguồn tĩnh: USD `10001…10004` · SGD `7001…` · COP `5.01…` · HKD `1301…` — cách xa tỷ giá thật *(AP §3.2.4: `25.500` · `26.200`)*, tệp tự khai `"tong_hop": true` |

## Cổng chạy lại *(Test tự chạy từ worktree, cây `6086395` — so với `BG-076` @ `5582246`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/cau_hinh/test_fx.py tests/api/test_isp_config_fx.py tests/api/test_bang_tuyen.py tests/api/test_soi_bang_tuyen.py tests/api/test_ba07_phu_het_tuyen.py` | 4 tệp đầu: `75 passed` *(tệp thứ năm đỏ — Q1)* | exit **0** · `77 passed in 1.72s` *(5 tệp; = 75 + 2 bài của `test_ba07_phu_het_tuyen.py`, xanh nhờ gộp `6086395`)* | ✅ |
| `python -m pytest tests/api` | `4 failed, 353 passed, 11 errors` *(+1 `test_moi_tuyen_THAT_deu_co_mat_trong_BA07`)* | exit 1 · `3 failed, 354 passed, 11 errors in 87.20s` — mẫu số **368** bài. Tập đỏ **14** so node id với `duong_nen_bai_do.txt` phần `tests/api/` *(**14** dòng)*: thêm **0** · bớt **0** | ✅ *(bài +1 của BG đã xanh sau gộp)* |
| `bash tools/dung_moi_truong_isp.sh --cong 5444 --duong-nen` *(lượt 1, cây `6086395`)* | lượt 3 `KẾT: ĐỎ` — 27 = 26 + 1 THÊM *(Q1)* | exit **0** · 7/7 `[ĐẠT]` · toàn bộ `12 failed, 2462 passed, 2 xfailed, 14 errors in 317.78s` *(mẫu số **2.490** bài thu thập = 12 + 2.462 + 2 + 14; trừ **30** bài C1 còn **2.460** = số nền `BG-076` ghi cho `329fa68`; **0** skipped · **0** deselected — luật `S0-R2-03`)* ⇒ `[ĐẠT] 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 184.37s` *(**664** bài)* ⇒ `[ĐẠT] 3 = 3` · **`══ KẾT: ĐẠT`**. Hai bài chập chờn `test_wo032_man_cua_that.py::test_AC3_…/::test_AC7_…` **⛔ chập** *(cả hai qua)* ⇒ ⛔ cần lượt 2 | ✅ |
| `/home/user/FLS-tobe/.venv/bin/python tools/soi_bang_tuyen.py` | exit 0 · `OK /api/fls/v1/config/fx` · `TINH : […] · vet 7 ham` · 41 tuyến | exit **0** · `OK /api/fls/v1/config/fx` · `TINH : ['fls/cau_hinh/tinh/ix_fx_mau.json'] · vet 7 ham` · `✅ ban khai KHOP SQL that o ca 41 tuyen` *(41 dòng `OK`; nền `329fa68`: **40** dòng `Tuyen(` → nay **41**)* | ✅ |
| `/home/user/FLS-tobe/.venv/bin/lint-imports` | exit 0 · `11 kept, 0 broken` | exit **0** · `Contracts: 11 kept, 0 broken.` · hợp đồng 10 `fls.cau_hinh la config thuan, khong duoc biet tang kho KEPT` | ✅ |
| ↳ **phá** `fls/cau_hinh/fx.py` *(thêm `import psycopg` sau `import json`)* | `9 kept, 2 broken` · `C1-B5` `1 failed` | `lint-imports` exit **1** · `Chi fls.repo va fls.db duoc import driver DB BROKEN` · `fls.cau_hinh la config thuan, khong duoc biet tang kho BROKEN` · `Contracts: 9 kept, 2 broken.` · `C1-B5` exit 1 `1 failed in 0.63s` · `git checkout -- fls/cau_hinh/fx.py` ⇒ sha256 `044eb3e4e68fb96e` → `044eb3e4e68fb96e` | ✅ |
| ↳ phép đo **động** *(luật `H1-R1-06`)* | — | tiến trình con `import fls.cau_hinh.fx` ⇒ `sys.modules` ∩ `{psycopg, fls.*}` = `['fls', 'fls.cau_hinh', 'fls.cau_hinh.fx']` — **0** `psycopg`/`fls.db`/`fls.repo` | ✅ |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` | exit **0** · như `BG` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `174 file, 1853 bang, 723 o ngay` | exit **0** · `175 file, 1856 bang, 724 o ngay, 104 ma QD` *(cây gộp: +`CALC_ZONE_406.md` · `BA-07` §4i; trước khi thêm 2 tệp của R1)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech (da do 16/20 phep)` | exit **1** · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` — kho `fls` rỗng, y `BG-066` | ✅ *(đỏ do kho rỗng)* |
| `python tools/kiem_thuyet_minh.py` | exit 0 · 31/31 | exit **0** · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC | exit **1** · `FileNotFoundError: …/isp-c1/.venv/Scripts/lint-imports.exe` *(đường Windows cứng — đã biết từ `BG-066`)* | ✅ *(khớp `BG`; tính là **⛔ ĐO ĐƯỢC**, ⛔ phải xanh — Đ5)* |
| **ĐỎ trước mã** *(bản sao `git archive 329fa68` + 2 tệp bài của `5582246`, `--noconftest`)* | `9c964f4`-bản: `23 failed, 2 passed` *(25 bài)* | exit **1** · `28 failed, 2 passed in 1.03s` *(**30** bài bản cuối)* — đỏ vì **thiếu hành vi**: **21** `ModuleNotFoundError: No module named 'fls.cau_hinh.fx'` · HTTP `404 FLS-NOT-FOUND` · `TypeError: … 'nguon_tinh'` ×2 · `mong đúng 1 tuyến …, đo 0` · `soi đo 0 lần tuyến`; 2 xanh sẵn = `C1-B5` + `401` *(như `BG` khai)* | ✅ |

## Bảng AC *(`WO-075` = ISP mục 6)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 · `C1-B1` | 4 dòng, VND = 1, `thieu = trung = lac = []` | `::test_C1_B1_nap_BON_thang_hop_le_tu_nguon_tinh` + `::test_C1_B1_nguon_tinh_TU_KHAI_la_so_TONG_HOP` xanh; R1 gọi máy thật: `ky` **4** dòng *(mẫu số khác 0 — Đ3)* · **4** tháng khác nhau `202406…202409` · VND `"1"` ở **4/4** dòng · `thieu = trung = lac = []`. Ca vào **đảo thứ tự** *(R1 dò)* ⇒ vẫn `[202406…202409]` | **ĐẠT** |
| AC-2 · `C1-B2` | `trung = ['202407']`; ⛔ cộng đôi | bài xanh: `trung == (202407,)`, **2** dòng `202407` hiện riêng `[20002, 20008]`, ⛔ dòng nào mang tổng `40010`, 5 vào ⇒ 5 ra. Đột biến `n >= 2 → n > 2` ⇒ bài **đỏ**. R1 dò thêm: hai dòng **giống hệt** ⇒ vẫn `trung = [202407]` · tháng LẠC trùng `202306 ×2` ⇒ `trung = lac = [202306]`. `yyyymm` là `int` *(⛔ tính lệch — chốt orchestrator)* | **ĐẠT** |
| AC-3 · `C1-B3` | `thieu = ['202408']` | bài xanh: `thieu == (202408,)`, `ky = [202406, 202407, 202409]` *(⛔ dòng `0` bịa)*. ⚠ Hai nhánh khác của `thieu` *(qua năm · lỗ đầu dải)* ⛔ bài ghim ⇒ `C1-R1-01` *(mã hôm nay đúng ở cả hai — R1 dò)* | **ĐẠT** |
| AC-4 · `C1-B4` | 200, đúng hợp đồng; `soi_bang_tuyen` xanh với tuyến mới | 8 bài `test_isp_config_fx.py` xanh. R1 **tự gọi** máy thật *(`cua.dung_may`, kết nối chỉ đọc, thẻ JWT thử)*: `HTTP 200 · 13.0 ms · 799 byte`; vỏ `{data, error, meta}`; tập khoá `data` = `{bang, ky, lac, nguon, thieu, trung}` **bằng** hợp đồng ISP mục 7; khoá mỗi kỳ = `{COP, HKD, SGD, USD, VND, trang_thai, yyyymm}`; `bang = 'IX.FX'` · `nguon = 'fls/cau_hinh/tinh/ix_fx_mau.json'`; kiểu `yyyymm` = `{int}` · tỷ giá = `{str}`; `trang_thai = 'chua_ky'` ×4; `meta.data_status = 'flash'`. ⛔ thẻ ⇒ `401 FLS-UNAUTHORIZED` · thẻ **hết hạn** ⇒ `401` · `POST`/`DELETE` ⇒ `405 FLS-METHOD` · `/config/FX` ⇒ `404`. `soi`: `OK` + `TINH` + 41/41. ⚠ `?run_id=` làm `meta` khai một phạm vi ⛔ áp ⇒ `C1-R1-07` | **ĐẠT** |
| AC-5 · `C1-B5` | `fls/cau_hinh` ⛔ import psycopg/repo/db | `11 kept`; phá `import psycopg` ⇒ `BROKEN` + `C1-B5` đỏ, trả nguyên sha khớp *(bảng trên)*; `.importlinter` hợp đồng 10 cấm đúng **3** thứ `psycopg` · `fls.repo` · `fls.db`; phép đo động: **0** module cấm trong `sys.modules` | **ĐẠT** |

## Đối chiếu mục 8 *(Exit criteria)*
| Dòng mục 8 | Đo | Kết |
|---|---|---|
| `C1-B1…B5` xanh, đỏ trước khi có mã | xanh: `77 passed` *(5 tệp)*. Đỏ trước: `28 failed, 2 passed` trên `329fa68` + bài cuối — 2 xanh sẵn *(`C1-B5` · `401`)* là bài canh hồi quy, `BG` tự khai; `C1-B5` được chứng minh đỏ **sau** khi có `fx.py` *(phá `import psycopg`)* | **ĐẠT** |
| regression `tests/api` xanh | tập đỏ **14** = đường nền **14**, thêm 0 · bớt 0 *(đọc "xanh" = ⛔ đỏ MỚI so đường nền S0)*; `--duong-nen` toàn bộ `26 = 26` · web `3 = 3` · `KẾT: ĐẠT` | **ĐẠT** *(trên cây gộp `6086395`; trên `5582246` đơn thuần là +1 đỏ — Q1, đã gỡ bằng `BA-07` §4i)* |
| 3 vòng review xong | R1 = phiếu này; R2 `KQ-078` · R3 `KQ-079` chưa | ⏳ |
| điều kiện PUSH: đủ R1 · R2 · R3, chặn = 0 | R1: **0** CHẶN | ⏳ *(R1 phần mình: đạt)* |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + AP §3.2.1 · §3.2.4 · D1)* | **ĐẠT có điều kiện** — hành vi hôm nay đúng spec ở mọi ca R1 dò *(31 ca biên thuần + 9 lượt gọi HTTP)*; **2 NÊN SỬA** về độ phủ bài *(`C1-R1-01`)* và độ hẹp của ngoại lệ cổng *(`C1-R1-02`)* | Khuôn bảng khớp AP §3.2.1 *("`yyyymm` × USD · SGD · COP · VND (=1) · HKD")*: `TIEN_TE` cùng thứ tự; `fls.canon.tien_te.ma_tien_te` của `usd`/` VND`/`SGD`+NBSP/`cop`/`hkd` ra đúng **5/5** mã của `TIEN_TE` ⇒ khoá tra của engine H4 sẽ khớp *(luật `H1-R1-01`)*. §3.2.4 *"thiếu ⇒ 0 · trùng ⇒ cộng đôi"*: ⛔ phép cộng nào trên dòng của tháng, mọi dòng hiện nguyên. Chặn ô sai: `NaN` · `Infinity` · `sNaN` · `0` · `-5` · `''` · `None` · `float` · `'10,001'` ⇒ `LoiFX` **một dòng**, nói tháng + cột *(luật `S0-R1-04`)*; cột `trang_thai: da_ky` trong nguồn ⇒ *cột lạ* *(⛔ giả chữ ký)*. Đột biến: **13** thử, **5** bị bắt, **8** sống *(`C1-R1-01` M1 · M3; `C1-R1-04` M2 · M4 · M5 · M6 · M9 · M10)*. Ngoại lệ `nguon_tinh`: 4 tuyến cố ý khai sai, 3 qua `kiem_bang_tuyen` *(`C1-R1-02`)*. Câu `Đ1` trong `fx.py:27-31` đo lại khớp: `dòng lạc\|tháng lạc` ở `docs/` @ `329fa68` = **8** tệp · `lạc\|\blac\b` ở `fls/`+`tools/` = **3** tệp, đều nghĩa khác *(`nap_cua.py:439` · `khai_cot.py:308` · `kiem_so_song.py`)* |
| **Dữ liệu** *(kho thật chỉ đọc)* | **⛔ ĐO ĐƯỢC kho thật — và bước ⛔ cần nó** | Container ⛔ có `fls-pg-1` *(O4 = A)*; bước ⛔ đọc/ghi kho *(tuyến chỉ mở kết nối đọc vô dụng — `BG` yếu #5)*. Dữ liệu duy nhất là **4** dòng tổng hợp: tự khai `tong_hop: true` + `ghi_chu "⛔ SỐ TỔNG HỢP"`, giá trị cố ý lộ là bịa. *"Số tổng hợp có bị nhầm là số thật"*: vỏ tuyến ⛔ có khoá `tong_hop` *(hợp đồng chốt tập khoá)*, nhưng ⓐ `data_status = flash` · ⓑ `trang_thai = chua_ky` ×4 ⇒ `fx_cua()` của C7 sẽ CHẶN *(D1)* · ⓒ màn tiêu thụ là `F4` *(Step 18)* chạy **sau** `C5` *(Step 14)* gỡ tệp tĩnh ⇒ ⛔ đường nào đưa 4 số bịa tới người dùng hay engine trước `C5`. Kho `fls` cụm 5444: `fls_itl` **0** trước = sau |
| **Màn hình** | **N/A** *(ISP mục 6: FE = N/A — bước mở tuyến; màn ở `F4`)* | Thay bằng **cửa trả đúng khuôn đã khai** *(bài học `GAP-API-09/10`)*: R1 gọi máy thật, so khoá **bằng** *(⛔ "có chứa")* với ISP mục 7 và `BA-07` §4i dòng `:850` — khớp cả tên khoá, kiểu `yyyymm` *(số nguyên)*, kiểu tỷ giá *(chuỗi)*, miền `trang_thai` |

## Phát hiện *(chi tiết + luật phòng tái phạm ở sổ riêng)*
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `C1-R1-01` | **NÊN SỬA** *(`NANG`)* | `fls/cau_hinh/fx.py:142-144` · `:205-210` · `tests/cau_hinh/test_fx.py` | bản sao `6086395`: **M1** `_thang_ke` ⇒ `return m + 1` · **M3** vòng `thieu` từ `trong_dai[0]` ⇒ cả hai **22 passed**. M3 làm tháng đầu dải thiếu biến mất **im lặng** | `DEV` *(làn BE-CF — chép 2 bài đề xuất dưới)* |
| `C1-R1-02` | **NÊN SỬA** *(`NANG`)* | `fls/api/bang_tuyen.py:182` · `:745` · `:749` · `tools/soi_bang_tuyen.py:277-281` | tuyến xấu A *(đọc `fls_itl`, `bang=()`, `nguon_tinh=('pyproject.toml',)`)* ⇒ `kiem_bang_tuyen` XANH; B *(`CLAUDE.md`)* · D *(`../…/etc/hostname`)* ⇒ **cả hai cổng XANH**; C *(chuỗi thay tuple)* ⇒ `kiem_bang_tuyen` XANH, `soi` 32 câu rác | `DEV` + orchestrator *(xác nhận khái niệm `nguon_tinh` tới C5; C4 sẽ dùng lại)* |
| `C1-R1-03` | GHI NHẬN *(`NHE`)* | `tests/api/test_ba07_phu_het_tuyen.py:61-63` · `docs/ITL/02_BA/07_API_CONTRACT.md:850` · `:919` | bản sao: xoá dòng `GET /config/fx` ⇒ `2 passed`; xoá cả hai dòng bảng ⇒ `2 passed` *(chuỗi còn ở changelog — Đ2)*; dòng `:850` ghi `⬜ chưa xây` cho tuyến đã chạy ⇒ ⛔ bài nào đỏ | orchestrator *(đổi ⬜ → ✅ lúc gộp)* · `DEV` *(WO riêng — tệp ngoài làn)* |
| `C1-R1-04` | GHI NHẬN | `fls/cau_hinh/fx.py:118-120` · `:133` · `:139` · `:214` · `:224-225` · `tests/cau_hinh/test_fx.py:186` | 6 đột biến sống *(M2 · M4 · M5 · M6 · M9 · M10)*; câu *"`True` sẽ lọt thành tháng 1"* sai với cơ chế `str(v)` | `DEV` |
| `C1-R1-05` | GHI NHẬN | `fls/cau_hinh/fx.py:193` · `:205-210` | `+202504` vào 4 tháng ⇒ `thieu` **6** tháng; tháng cuối chưa nhập ⛔ vào `thieu` | orchestrator ⇒ phiếu `C7` *(`fx_cua` chặn theo tháng hỏi)* · `C5`/`DT2` *(`thang_cuoi`)* |
| `C1-R1-06` | GHI NHẬN | `fls/cau_hinh/fx.py:223-224` · `:126-139` · `:81` | khoá JSON trùng ⇒ giữ bản cuối im lặng; `'1e4'` ⇒ `"1E+4"`; `'１２３'` ⇒ `123`; `'000001'` ⇒ `lac = [1]` | `DEV` *(trước `C5` nạp ảnh `DT2`)* |
| `C1-R1-07` | GHI NHẬN | `fls/api/xu_ly.py:55-63` · `:1012-1027` · `fls/api/cua.py:319-320` | `GET /config/fx?run_id=NAP-2026-01-01-X` ⇒ `meta.pham_vi = 'lan nap …'`, `data` trùng khít lượt trơn | `DEV` |

## Bài thử đề xuất *(R1 viết + chứng minh trên bản sao; ⛔ commit — lệnh orchestrator: lượt này chỉ commit phiếu + sổ. Tác giả chép vào `tests/cau_hinh/test_fx.py` ở vòng sửa)*
| Bài | Chứng minh ĐỎ bằng | Xanh trên `5582246` |
|---|---|---|
| `test_R1_01a_thieu_QUA_NAM_dung_thang_1_nam_sau` — `kiem([202411, 202412, 202502], thang_dau=202411).thieu == (202501,)` | **M1** `_thang_ke` ⇒ `return m + 1`: `1 failed, 3 passed` | ✅ |
| `test_R1_01b_lo_DAU_dai_tu_thang_dau_la_THIEU` — `kiem([202407, 202408, 202409], thang_dau=202406).thieu == (202406,)` | **M3** vòng `thieu` từ `trong_dai[0]`: `1 failed, 3 passed` | ✅ |
| `test_R1_01c_so_KHONG_huu_han_thi_NO` — USD ∈ `NaN` · `Infinity` · `-Infinity` · `sNaN` ⇒ `LoiFX` | **M2** bỏ `is_finite()`: `1 failed, 3 passed` | ✅ |
| `test_R1_01d_ky_SAP_theo_thang_du_dau_vao_dao` — vào `[202409, 202406, 202408, 202407]` ⇒ `ky` theo tháng | **M4** bỏ sắp: `1 failed, 3 passed` | ✅ |

*(Cả 4 bài trên mã gốc: `4 passed in 0.01s`; trả nguyên `fx.py` sha256 `044eb3e4e68fb96e` sau mỗi đột biến. Mã nguồn bài: `scratchpad/r1_c1/test_r1_c1_de_xuat.py`; kịch bản chứng minh: `scratchpad/r1_c1/chung_minh_do.py`.)*

## Phép phá / dò R1 đã chạy *(mọi phép trên BẢN SAO `git archive 6086395` ngoài worktree, `--noconftest` — ⛔ chạm kho test của cụm trong lúc `--duong-nen` chạy; riêng phá `import psycopg` làm ở worktree rồi `git checkout --`)*
| Phép | Mong | Đo | Kết |
|---|---|---|---|
| 13 đột biến `fx.py` × bộ `test_fx.py` 22 bài | bài ghim mọi nhánh | **5** bắt *(M7 trùng · M8 cột lạ · M11 VND = 1 · M12 tập rỗng · M13 thiếu cột)* · **8** sống | `C1-R1-01` · `C1-R1-04` |
| 4 tuyến cố ý khai sai `nguon_tinh` × hai cổng | mỗi tuyến đỏ ≥ 1 cổng, câu đọc được | A: chỉ `soi` đỏ · B, D: **0** cổng đỏ · C: `soi` 32 câu rác · E *(thư mục)*: `soi` đỏ đúng · F *(⛔ bảng, ⛔ nguồn — cổng ⓓ cũ)*: `kiem_bang_tuyen` đỏ đúng | `C1-R1-02` |
| Xoá dòng hợp đồng `/config/fx` ở `BA-07` × `test_ba07_phu_het_tuyen.py` | đỏ | P1 · P2 đều `2 passed`; sha trả nguyên `2925561a04175798` | `C1-R1-03` |
| 31 ca biên thuần `fx.kiem` | `LoiFX` một dòng hay bảng đúng | 25 đúng mong · 6 qua mà méo/im *(`'1e4'` · `'1.00'` · `'１２３'` · `202504` sau dải · `'000001'` · khoá JSON trùng)* | `C1-R1-05` · `C1-R1-06` |
| 9 lượt gọi HTTP máy thật | 200/401/405/404 đúng hợp đồng | 9/9 mã HTTP đúng; `?run_id=` làm `meta` khai sai phạm vi | AC-4 · `C1-R1-07` |

## Về các câu `BG-076` hỏi orchestrator
| Câu | Trạng thái R1 thấy |
|---|---|
| Q1 *(`BA-07` thiếu dòng `/config/fx`)* | **đã gỡ** bằng gộp `6086395` *(phương án A — `BA-07` v3.15 §4i)*; bài xanh **thật** hôm nay vì dòng `:850` có mặt, nhưng bài ⛔ canh được dòng ấy ⇒ `C1-R1-03` |
| Q2 *(định nghĩa `lac`)* · Q3 *(`trang_thai` = ký)* · Q4 *(tỷ giá chuỗi · `yyyymm` int)* | orchestrator **đã chốt** đúng phương án `BG` làm ⇒ ⛔ tính lệch. ⚠ ISP mục 6 `C1-B2`/`B3` và `C5-B1` vẫn ghi `['202407']` có nháy — `BA-07` §4i đã ghi *"`yyyymm` (số nguyên)"*; nên vá chữ ISP ở bản kế *(việc `fls-ba`, ⛔ việc `C1`)* |
| Q5 *(scratchpad dùng chung)* | R1 ghi log vào thư mục riêng `scratchpad/r1_c1/` ⇒ ⛔ trùng tên với làn nào |

## Ghi chú cho R2 *(`KQ-078`)*
1. Soi lại hai NÊN SỬA trước: `C1-R1-01` *(chạy lại M1 · M3 trên mã vòng sửa — phải ĐỎ)* · `C1-R1-02` *(4 tuyến A–D phải đỏ ≥ 1 cổng)*.
2. `BG-076` "Dev tự thấy còn yếu" #3 · #4 trùng `C1-R1-02`; #6 *(nguồn tĩnh hỏng ⇒ `500` ⛔ bài HTTP)* R1 ⛔ đo thêm — vẫn mở.
3. Cụm 5444 để **CHẠY** *(lệnh orchestrator)*.
4. ⚠ Container **khởi động lại giữa lượt R1** *(orchestrator báo 16/11; cụm 5444 được bật lại)*. Lượt `--duong-nen` đã **xong trước** khi khởi động lại *(`KẾT: ĐẠT`, exit 0 — log còn nguyên)* ⇒ ⛔ chạy lại; R1 chạy lại bộ 5 tệp mục tiêu trên cụm vừa bật: exit **0** · `77 passed in 3.31s` *(= lượt trước)*.
