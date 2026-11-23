# KQ-073 — biên bản kiểm `BG-071` *(ISP 3.1.2 · Step 1 · `H1` · vòng **R2** — CHỈ quét phần đổi SAU R1)*

| | |
|---|---|
| **Thuộc** | [`BG-071`](BG-071-ban-giao-wo-070.md) *(mục "Vòng sửa sau R1 (KQ-072)")* · [`WO-070`](WO-070-isp-h1-ca-gl-thuan.md) |
| **Kiểm bởi** | `fls-test` *(R2 — phiên mới, độc lập với R1 và với tác giả vòng sửa; ⛔ đọc lượt nào của tác giả ngoài phiếu + log scratch được dẫn)* · 2026-11-16 · orchestrator giao |
| **Phạm vi** | `git diff 30c1c4a isp/H1` — **3** tệp *(`7ced6b6` mã + bài · `1606f33` mục vòng sửa trong `BG-071`)*: `fls/bao_cao/gl.py` +222/−62 · `tests/bao_cao/test_gl.py` +382/−0 · `BG-071` +82/−0 *(chỉ thêm)*. Thêm theo lệnh orchestrator: **8 cột BM…BT** đối chiếu `docs/ITL/01_Orchestrator/isp-3.1/CALC_ZONE_406.md` *(nhánh chính, sha256 `e8c086c9be808818…`, ⛔ đổi từ `1768668`)* |
| **Cụm** | reviewer **5445** *(`/home/user/fls-pg16-5445`, để CHẠY)* · log R2: `/tmp/claude-0/-home-user-FLS-tobe/e29eef16-56df-5253-a1b1-752daec60d67/scratchpad/r2_h1/` *(⛔ trong repo)* |
| **Phán quyết** | **`ĐẠT`** vòng R2 *(thang ISP: **0 CHẶN**)* — **4/4 AC ĐẠT** trên mã mới; **8/8 cột** BM–BT khớp công thức ô NOW *(R2 tính tay `Fraction` **117** ô + kiểm **48** ô mong của bài · **0** lệch)*. Phát hiện R1: **7/7 ĐÃ SỬA** *(kể cả NÊN SỬA `H1-R1-01`)*; phần kế hoạch của `H1-R1-05` *(DT4/H4 so `AX:BL`)* còn ở orchestrator. **4** phát hiện mới: **0** CHẶN · **0** NÊN SỬA · **4** GHI NHẬN *(`H1-R2-01…04`, lớp B1 cả 4)* |
| **Sổ phát hiện** | [`docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H1.md`](../../04_Test/review/SO_PHAT_HIEN_ISP-3.1_H1.md) **v0.2** *(thêm cột Trạng thái — v0.1 khai bằng câu "cả 7 hàng đều `mở`" — đổi 7 ô + thêm 4 hàng R2)* |

## Cổng vào
| Kiểm | Kết quả |
|---|---|
| git | worktree `isp/H1` HEAD = `1606f33` *(phiếu)* ← `7ced6b6` *(mã + bài)* ← `30c1c4a` *(`KQ-072`)* ✔ đúng hash `BG-071` ghi; `git status` **0** dòng trước và sau mọi phép đo của R2. **⛔ đẩy**: `git branch -r --contains 7ced6b6` = **0** · `--contains 1606f33` = **0** — đúng O2 = A |
| spec | ISP **v3.1.2** Step 1 · H1 *(⛔ đổi trong diff — `git diff --stat 30c1c4a isp/H1 -- docs/ITL/02_BA` rỗng)* · AP sha256 đo lại `5cf6e576ff46f0886eb4a6b6cbefbcbd4f905a7835f843a2bfdb94d8a90982ba` = `WO-070` ✔ · quyết định orchestrator sau R1: `TIEN_DO.md:95` *(`R1-01` = A · `R1-05` ⇒ dựng BM · BN · BQ · BT · GHI NHẬN làm luôn)* + errata ① ② `:96` |
| làn | 3/3 tệp thuộc làn **BE-HC** hoặc phiếu *(`fls/bao_cao/**` · `tests/bao_cao/**` · `handoff/BG-071`)* ✔. ⛔ chạm `.importlinter` · `pyproject.toml` · `fls/bao_cao/__init__.py` · dashboard · README ✔ |
| ký tự vô hình · PII · bí mật | **686** dòng THÊM: **0** ký tự vô hình *(NBSP · BOM · U+200B–D · U+2000–200A · U+2028/9 · U+202F · U+205F · U+3000 · NEL · VT · FF · U+1C–1F · U+1680)* — bài viết biến thể bằng ESCAPE `\u00a0`/`\ufeff`; **0** email; **0** dạng `secret/password/token`; **0** DSN; **44** số ≥ 9 chữ số = **44/44** số TỔNG HỢP của bài *(chữ số mUSD, `2500000000`, `2·10^27`)* — ⛔ Diễn giải, Số chứng từ, tên người *(log `soi_pii.log`)* |
| kho thật | **⛔ CHẠM** — container ⛔ có sổ thật; kho `fls` @5445 `fls_itl` = **0** dòng *(K7)* |

## Cổng chạy lại *(R2 tự chạy TỪ worktree; `PG_DSN=…localhost:5445/fls` · `PG_DSN_TEST=…localhost:5445/fls_test` · `PYTHONUTF8=1` · `PYTEST_ADDOPTS` trống; venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | `BG` nói *(vòng sửa)* | Test đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/bao_cao/test_gl.py` | exit 0 · `49 passed` | exit **0** · `49 passed in 0.77s`; `--collect-only tests/bao_cao` ⇒ `49 tests collected`; sha256 `gl.py` = `c7c4094bd4e801a3…` · `test_gl.py` = `05d874d84d593762…` = số `BG` ghi | ✅ |
| ↳ bộ bài MỚI trên mã CŨ *(`gl.py` @ `30c1c4a` sha256 `82c1921bc2763492…`, bản sao ngoài worktree)* | `28 failed, 21 passed` *(R1-01 7 · R1-02 14 · R1-05 4 · R1-07 3)* | exit **1** · `28 failed, 21 passed in 0.54s` — đỏ theo hàm: `R1_01` 1+4+1+1 = **7** · `R1_02` 8+6 = **14** · `R1_05` **4** · `R1_07` 1+2 = **3** | ✅ |
| `lint-imports` | exit 0 · `11 kept, 0 broken` | exit **0** · `Contracts: 11 kept, 0 broken.` · `fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho KEPT` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5445` *(`15:23:06Z → 15:31:36Z`, cây = `1606f33` sạch)* | exit 0 · `KẾT: ĐẠT` · `12 failed, 2481 passed, 2 xfailed, 14 errors` · `26 = 26` · web `3 failed, 661 passed` · `3 = 3` | exit **0** · 7/7 `[ĐẠT]` *(K2 `postmaster.pid cổng 5445` · K4 `26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · K5 `11 kept` · K6 `chay 9845 / co 9967` · K7 `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2481 passed, 2 xfailed, 14 errors in 322.13s (0:05:22)` ⇒ `[ĐẠT] … 26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 182.38s (0:03:02)` ⇒ `[ĐẠT] … 3 = 3 node id` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong`. **Mẫu số** *(Đ3)*: `pytest --collect-only` ⇒ `2509 tests collected` = 12 + 2.481 + 2 + 14 = **2.509** = 2.478 *(R1 trên `e0bd4a6`)* + **31**; **0** `skipped` · **0** `deselected`; tệp đường nền **26** node id | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `176 file, 1872 bang` | exit **0** · `(176 file, 1872 bang, 725 o ngay, 104 ma QD)` *(TRƯỚC khi thêm phiếu này — lượt sau: §Ghi chú)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech (da do 16/20 phep)` | exit **1** · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` — `B3` · `B4` · `C5` · `C5b` KHONG DO DUOC · `A1` · `B1` · `C6` DOI TRANG THAI *(kho rỗng)* | ✅ *(đỏ do kho rỗng)* |
| `python tools/soi_bang_tuyen.py` | exit 0 · 40 tuyến | exit **0** · `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python tools/kiem_thuyet_minh.py` | exit 0 · 31/31 | exit **0** · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` | ✅ |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` | exit **0** · y hệt | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC | exit **1** · `FileNotFoundError: … isp-h1/.venv/Scripts/lint-imports.exe` | ✅ *(khớp `BG`; tính là **⛔ ĐO ĐƯỢC** — Đ5)* |
| Đột biến của `BG` *(`hc_h1_sua/dot_bien.py`, R2 chạy lại bản chép có chặn bytecode — `H1-R2-04`)* | `23 · bị cắn: 23` | `đột biến: 23 · bị cắn: 23 · sống/⛔ đo được: 0` · đối chứng `49 passed` · sha256 trả `c7c4094bd4e801a3` KHỚP *(log `dev_dot_bien/dot_bien_dev_sach_pyc.log`)* | ✅ |

## Tám cột CALC ZONE ↔ công thức ô NOW *(`CALC_ZONE_406.md` — R2 đọc từng ô, tính tay ĐỘC LẬP bằng `Fraction`, ⛔ import `gl.py` để tính mong)*
| Cột | Công thức ô *(nguyên văn)* | Mã `7ced6b6` | Đơn vị · luỹ kế | Bài ghim · đột biến R2 cắn | Kết |
|---|---|---|---|---|---|
| **BM** | `AZ*SUMIFS(9.2!B,…) + BC*SUMIFS(…C…) + BF*SUMIFS(…D…) + BI + BL*SUMIFS(…F…)` — tỷ giá THÁNG CỦA DÒNG | `gl.py:290-297` tồn VND + Σ `ton[t] × fx[tháng dòng][t]` cho USD · SGD · COP · HKD khi `ton[t] ≠ 0` | **VND** *(⛔ chia — hàng 9 "VND")*; đánh giá lại mỗi dòng | `R2-M01` bỏ tồn âm · `M02` tỷ giá tiền tệ dòng · `M03` tỷ giá LỊCH SỬ · `M11` bộ đệm nhầm tháng · `M12` quên BI · `M14` quên HKD ⇒ **cắn cả 6**. ⚠ `M16` *(`abs(BI)`)* **SỐNG** ⇒ `H1-R2-01` | ✔ |
| **BN** | `(AZ + BC*SGD/USD + BF*COP/USD + BI/USD + BL*HKD/USD)/10^6` | `:298` `BM ÷ USD ÷ 10^6` *(một lần làm tròn — V1)* | **mUSD = triệu USD** *(VND ÷ VND/USD ÷ 10^6)* | `R2-M04` BN từ BQ · `M13` ÷ tỷ giá dòng ⇒ cắn. R2 viết BN **từng số hạng như ô** ⇒ lệch tương đối ≤ 10^-26 ở 9/9 dòng | ✔ |
| **BO · BP** | `iferror(INDEX/MATCH(tháng, D10) * E10\|F10 / 10^9)` | `:281-282` `fx[tháng][ma] × no\|co / 10^9` | **bVND** = ÷ 10^9 | R1-M2 *(BP = 0 khi E ≠ 0)* ⇒ cắn | ✔ |
| **BQ** | `BQ10 = BO10-BP10` · `BQ11 = BQ10+BO11-BP11` | `:285` | bVND · **luỹ kế cả bảng** | `R2-M06` *(đặt lại khi đổi tháng)* ⇒ cắn | ✔ |
| **BR · BS** | `iferror(BO10\|BP10 / SUMIFS(USD, tháng) * 10^3)` | `:283-284` | **mUSD** = bVND ÷ VND/USD × 10^3 | R1-M3 · R1-M4 *(ngữ cảnh)* ⇒ cắn | ✔ |
| **BT** | `BT10 = BR10-BS10` · `BT11 = BT10+BR11-BS11` | `:286` | mUSD · **luỹ kế** theo tỷ giá LỊCH SỬ | `R2-M05` *(BT = BQ ÷ USD hiện tại — đánh giá lại)* ⇒ cắn | ✔ |
| tồn `AZ·BC·BF·BI·BL` | `AZ11 = AZ10+AX11-AY11` | `:279` `ton[ma] = ton[ma] + no - co` | nguyên tệ · luỹ kế | R1-M1 · R1-M6 ⇒ cắn | ✔ |
| **tháng thiếu** | BO·BP·BR·BS `iferror` ⇒ ô **rỗng** · BM × `SUMIFS = 0` ⇒ **mất số im lặng** · BN `#DIV/0!` | `ThieuTyGia` có tên cho CẢ lượt *(`:355-383`)*, kể cả nhánh BM *(tồn SGD ≠ 0 mà tháng dòng thiếu/0/NaN SGD ⇒ `ThieuTyGia(tien_te='SGD')`)* | **⛔ 0 im lặng** — D1 | `R2-M15` *(nhãn tiền tệ sai ở nhánh BM)* ⇒ cắn; kịch bản phá R2 #2 · #3 · #21 đúng mong | ✔ |

**Tính tay R2** *(`tinh_tay_r2.py` · log `tinh_tay_r2.log`)*: ca **R2-A** 7 dòng, 3 tháng *(202503 → 202505)*, đủ 5 tiền tệ, tồn đổi dấu *(USD · COP âm)*, tồn HKD về **0 đúng** rồi sang tháng ⛔ có HKD *(V3)*, dòng hai vế bằng nhau *(SGD 333,33 / 333,33)*, tỷ giá lẻ *(`25432.1` · `19876.54` · `6.1234` · `3271.09`)*; ca **R2-B** bảng VND = 2 *(V2)*. **9 dòng × 13 ô = 117 ô so · 0 lệch** *(ô ⛔ chia: bằng tuyệt đối; ô có chia: `|Δ|/|tay| ≤ 10^-26`)*. Cộng: **48/48** ô mong ghi trong bài *(`MONG_BM_BT` 6 × 4 · `MONG_R1` 4 × 6)* khớp `Fraction` của R2 tới `10^-30` tương đối *(`kiem_mong_bai.log`)* — mong của Dev ⛔ phải số tự-sinh từ mã.

## Từng phát hiện R1 → R2 tự kiểm *(⛔ tin `BG` — mỗi dòng có phép đo R2 tự chạy)*
| Mã | Mức R1 | Đo của R2 *(ĐỎ trên bản cũ → XANH trên bản mới)* | Trạng thái |
|---|---|---|---|
| `H1-R1-01` | **NÊN SỬA** | `gl.py:268` + `:362` gọi `ma_tien_te` *(grep `ma_tien_te(` = **2** dòng mã; `d.tien_te` còn **1** chỗ ngoài `:268` = thông điệp `:271`)*. Bài ĐỀ XUẤT của R1 `test_R1_03_so_tien_te_qua_ma_tien_te[4]`: mã `30c1c4a` ⇒ **4/4 ĐỎ** → mã `7ced6b6` ⇒ **XANH** *(`r1_de_xuat_cu_moi.log`)*; 7 bài `test_R1_01_…` của Dev: 7 ĐỎ → XANH. Đột biến `R2-M08` *(mã dòng qua `str.strip().upper()`)* ⇒ cắn *(`[BOM_dau]`)*. ⚠ Khoá `fx` chỉ được ghim với `'usd'`/`' VND'` ⇒ `R2-M07` SỐNG ⇒ `H1-R2-02` *(⛔ mở lại `R1-01`: mã đúng)* | **ĐÃ SỬA** |
| `H1-R1-02` | GHI NHẬN | Bài R1 `test_R1_02_…[NaN/Infinity/-Infinity]`: **3/3 ĐỎ** → XANH; 14 bài Dev ĐỎ → XANH. Đột biến `R2-M09` *(chỉ chặn NaN)* ⇒ **4** đỏ. Kịch bản phá: Nợ `sNaN` ⇒ `TienKhongHuuHan` *(⛔ còn `InvalidOperation`)*; Có `-Infinity` dòng 3 ⇒ `vi_tri = 3`; tỷ giá SGD NaN ở nhánh BM ⇒ `ThieuTyGia('SGD')` | **ĐÃ SỬA** |
| `H1-R1-03` | GHI NHẬN | R1-M1 · M2 · M6 trên mã MỚI: bộ bài `30c1c4a` ⇒ `18 passed` **(SỐNG)** → bộ bài `7ced6b6` ⇒ `2 failed` mỗi lượt *(`dot_bien_bai_cu.log`)* | **ĐÃ SỬA** |
| `H1-R1-04` | GHI NHẬN | Docstring `gl.py:20-33` chép công thức ô AX…BT — đối chiếu `CALC_ZONE_406.md` **8/8** cột khớp *(BM viết `tháng` thay `DATE(YEAR(A),MONTH(A),1)`)*; ② tách **ba** ngữ nghĩa tra; ⓐ theo bảng "Hai NGỮ NGHĨA" *(rỗng · mất số · `#DIV/0!` · trùng tháng)*; thông điệp `ThieuTyGia` `:179-183` hết câu "lỗi SUMIFS = 0" cho mọi cột. ⚠ Câu MỚI `:66` sai với chính mã ⇒ `H1-R2-03` | **ĐÃ SỬA** |
| `H1-R1-05` | GHI NHẬN | **Phần H1**: `KetQuaDongGL` +4 trường BM · BN · BQ · BT *(`:238-245`)* — §Tám cột: 117 + 48 ô · 0 lệch. **Phần kế hoạch** *(DT4/H4 so thêm `AX:BL` hoặc ghi lý do)*: errata ② `TIEN_DO.md:96` sửa câu tả DT4 + ghi "4 cột tồn giao H1", **⛔** nhắc so `AX:BL` *(grep ISP v3.1.2 `AX:BL` = **0**)* | **ĐÃ SỬA** *(phần H1)* · phần ISP: việc orchestrator |
| `H1-R1-06` | GHI NHẬN | `R1-I1` *(`importlib.import_module('fls.db.kho')` lúc nạp)*: bộ bài cũ `18 passed` + lint `11 kept` **(SỐNG)** → bộ bài mới `2 failed`, lint vẫn `11 kept` *(đúng điểm mù)*. R2 thêm `R2-I2` *(`getattr(builtins, '__imp'+'ort__')` trong `tinh_gl` — cây cú pháp ⛔ thấy)* ⇒ `1 failed` *(phép đo `sys.modules` bắt)* | **ĐÃ SỬA** |
| `H1-R1-07` | GHI NHẬN | R1-M3 *(prec 12)* · R1-M4 *(`ROUND_DOWN`)*: bộ bài cũ `18 passed` **(SỐNG)** → mới `6 failed` · `2 failed`; `S-M01` *(`HALF_UP`)* · `S-M02` *(`HALF_DOWN`)* của Dev chạy lại sạch bytecode ⇒ mỗi con `1 failed` | **ĐÃ SỬA** |

## Bảng AC *(`WO-070` = ISP Step 1 mục 6 — đo lại trên `7ced6b6`)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 · `H1-B1` | VND Nợ 2.500.000.000 @ USD 25.500 ⇒ bVND 2,5 · mUSD **0,098039…** *(errata ① — ISP ghi `98,039…` = nghìn USD)* | `test_H1_B1_…` PASSED; nay ghim tuyệt đối `str(musd_no) == "0.09803921568627450980392156863"` *(28 chữ số)*, BN · BT cùng giá trị. R2 `Fraction`: `2,5 / 25.500 × 10^3` = `0.0980392156862745098039215686\|27…` ⇒ chữ số 28 làm tròn lên `…6863` ✔ | **ĐẠT** |
| AC-2 · `H1-B2` | dòng USD Có ⇒ tách đúng cột Có; tồn = tồn trước − Có | `test_H1_B2_…` PASSED; tồn luỹ kế nguyên tệ ghim thêm bởi dòng hai vế *(`test_R1_03_…`: 0 + 100 − 30 = 70)* + ca SGD 4 dòng của R1 | **ĐẠT** |
| AC-3 · `H1-B3` | tháng ⛔ có tỷ giá ⇒ lỗi CÓ TÊN, ⛔ trả 0 | 5 bài `H1-B3` PASSED + nhánh BM `test_R1_05_BM_ton_khac_0_…` *(`ThieuTyGia(202502, 'SGD', 2)`)*; kịch bản phá R2 #2 *(SGD = 0)* · #3 *(SGD NaN)* · #20 *(tháng `str`)* · #21 *(thiếu ở dòng 3 ⇒ ném cả lượt)* ⇒ `ThieuTyGia` 4/4, **0** số 0 im lặng | **ĐẠT** |
| AC-4 · `H1-B4` | `fls/bao_cao` ⛔ chạm DB *(lint-imports)* | `lint-imports` exit 0 · `11 kept`; `test_H1_B4_…` PASSED; hai phép đo động mới cắn `R1-I1` *(2)* · `R2-I2` *(1)* trong khi lint vẫn `11 kept`. `gl.py` import thêm `fls.canon.tien_te` — `fls/canon/__init__.py` **0** import · `tien_te.py` chỉ `__future__` + `typing` | **ĐẠT** |
| Goal *(ISP §2)* | đúng tay tính trên 6 dòng tổng hợp | `test_H1_sau_dong_…` PASSED *(60 ô)* + `test_R1_05_bon_cot_…` *(24 ô BM–BT trên CÙNG 6 dòng — R2 kiểm lại 24/24 bằng `Fraction`)* | **ĐẠT** |

## Đối chiếu ISP Step 1 mục 8
| Dòng | Bằng chứng | Phán quyết |
|---|---|---|
| ① *H1-B1…B4 xanh, đỏ trước khi có mã* | xanh: `49 passed` *(B1…B4 trong đó)*; đỏ trước: R1 đã chứng minh *(`ModuleNotFoundError`)*; vòng sửa: bộ bài mới trên mã cũ `28 failed` đúng lý do *(bảng trên)* | **ĐẠT** |
| ② *3 vòng review xong* | R1 `KQ-072` ✔ · R2 = phiếu này ✔ · R3 `KQ-074` chưa chạy | **CHƯA TỚI** *(2/3)* |
| ③ *PUSH: đủ R1 · R2 · R3, phát hiện chặn = 0* | CHẶN = **0** *(R1 0 · R2 0)*; NÊN SỬA còn mở = **0**; thiếu R3 | **CHƯA TỚI** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 1 + `CALC_ZONE_406.md` + `INV-I16` + `BA-07` §4g)* | **ĐẠT có ghi chú.** 8/8 cột đúng công thức ô *(§Tám cột)*; vòng sửa ⛔ lấn bước khác ngoài quyết định orchestrator *(BM–BT = `TIEN_DO.md:95`)*; tách `_kieu_dung`/`_so_dung` và bộ đệm `bang_chuan` là hệ quả trực tiếp của `R1-02`/`R1-01` *(⛔ refactor cho gọn)*. **Đột biến R2 — 23** *(bản sao ngoài worktree, ⛔ `tests/conftest.py`, xoá `__pycache__` + `PYTHONDONTWRITEBYTECODE=1` mỗi lượt)*: **21 cắn · 2 SỐNG** *(`R2-M07` ⇒ `H1-R2-02` · `R2-M16` ⇒ `H1-R2-01`)*; riêng phần MỚI của `gl.py`: **16** con, **14** cắn. **Kịch bản phá — 21** *(`kich_ban_pha_r2.log`)*: 20 đúng mong; 1 trái *(#18 — câu docstring `:66`)* ⇒ `H1-R2-03`. Hành vi ghi lại *(⛔ phát hiện)*: mơ hồ ở tiền tệ ⛔ cần *(khoá `SGD`+`sgd`, tồn SGD 0)* ⇒ ⛔ ném *(tra lười; bảng của C1 chỉ mang đúng 5 khoá — `isp/C1` `fls/cau_hinh/fx.py:227-229` xếp khoá khác vào *cột lạ*)*; tiền tệ `None` ⇒ `TienTeNgoaiGL` *(`ma_tien_te(None) = ''`)*; `'\u200bVND'` ⇒ `TienTeNgoaiGL` *(ZWSP ⛔ thuộc 30 ký tự — ồn)*; hai lượt liên tiếp ⛔ rò bộ đệm; `fx` vào ⛔ bị sửa; ngữ cảnh người gọi prec 5 ⇒ BM/BN/BQ/BT y nguyên | `dot_bien_r2.py` + `.log` · `dot_bien_bai_cu.log` · `kich_ban_pha_r2.py` + `.log` · `tinh_tay_r2.log` |
| **Dữ liệu** *(kho, chỉ đọc)* | **⛔ ĐO ĐƯỢC trên sổ thật — đúng phạm vi H1** *(ISP §3 Loại trừ: dữ liệu thật = H4)* | Kho `fls` @5445 `fls_itl` = **0** dòng *(K7 — Đ3: mẫu số 0 ⇒ ⛔ kết luận "không lệch")*; container ⛔ có Docker. Mọi số của phiếu là số TỔNG HỢP; tỷ giá lẻ duy nhất mượn từ thăm dò O7 *(`20691.51`)* |
| **Màn hình** | **N/A** | ISP Step 1 §4 *"Frontend: N/A — lát cắt là hàm thuần"*; diff ⛔ chạm `fls/web/**`; ⛔ dựng 8088 |

## Phát hiện mới *(chi tiết + luật phòng tái phạm: sổ v0.2)*
| F | Mã sổ | Lớp | Mức | Nơi *(@ `7ced6b6`)* | Tái hiện *(R2 đã chạy)* | Khuyến nghị | Gửi |
|---|---|---|---|---|---|---|---|
| F-1 | `H1-R2-01` | B1 | GHI NHẬN | `fls/bao_cao/gl.py:290` · `tests/bao_cao/test_gl.py:465-497` · `:535-566` · `:601-618` | Đột biến `R2-M16` `vnd_ton_all = abs(ton[_DON_VI_BM])` ⇒ `49 passed` *(SỐNG)*: mọi ca BM có tồn VND đều **dương** *(`2.500.000.000`)* hoặc 0. Mã đúng *(kịch bản #17: VND Có 1.000 ⇒ BM = −1.000)* | thêm bài tồn VND ÂM *(đề xuất `test_R2_01_BM_giu_DAU_AM_cua_ton_VND` — §Bài thử)* | `DEV` |
| F-2 | `H1-R2-02` | B1 | GHI NHẬN | `fls/bao_cao/gl.py:362` · `tests/bao_cao/test_gl.py:388-394` | Đột biến `R2-M07` khoá `fx` chuẩn hoá bằng `str(khoa).strip().upper()` ⇒ `49 passed` *(SỐNG)*: bài khoá `fx` chỉ thử `'usd'` · `' VND'` — cả hai `str.strip()` cũng gỡ. Ký tự `ma_tien_te` gỡ mà `str.strip()` ⛔ gỡ: **1/30** *(U+FEFF)*. Mã đúng *(kịch bản #6: khoá `'\ufeffUSD'` ⇒ USD)* | thêm biến thể BOM cho khoá `fx` *(đề xuất `test_R2_02_…`)*; đổi tay sang hàm tự chế sẽ ĐỎ | `DEV` |
| F-3 | `H1-R2-03` | B1 | GHI NHẬN | `fls/bao_cao/gl.py:64-66` · `:179-183` ↔ `:377-382` | ⓐ Câu *"⇒ trong MỘT tháng `BM = BQ × 10^9`, sang tháng mới hai cột tách nhau"* — kịch bản #18: USD 100 @202501 rồi 2 dòng USD @202502 ⇒ dòng 2: BM `2.525.000` ≠ BQ × 10^9 `2.575.000`; dòng 3: `2.550.000` ≠ `2.600.000` — **cùng tháng 202502 mà vẫn khác** *(BQ giữ tỷ giá LỊCH SỬ của dòng 1)*; ca R2-B *(VND = 2, một tháng)*: BM `10^9` ≠ BQ × 10^9 `2·10^9`. Đúng chỉ khi **mọi dòng từ đầu bảng** cùng tháng *(và VND = 1)* — đúng như chú thích bài `test_gl.py:478`. ⓑ Thông điệp `ThieuTyGia` gắn đuôi AS-IS của *tháng VẮNG* *("BO·BP·BR·BS rỗng do iferror")* vào **mọi** lý do — với tỷ giá = 0 chính lý do `:380` nói *"INDEX trả rỗng ⇒ BO/BP = 0"* ⇒ một thông điệp nói hai điều ngược | ⓐ viết lại: *"BM = BQ × 10^9 chỉ khi mọi dòng TỪ ĐẦU BẢNG cùng một tháng (VND = 1); một lần đổi tháng là tách vĩnh viễn"* — H4 ⛔ được dùng đẳng thức này làm phép soát. ⓑ để đuôi AS-IS theo từng lý do *(vắng tháng · ô trống · mơ hồ)* | `DEV` *(H4 hoặc vòng sửa kế)* |
| F-4 | `H1-R2-04` | B1 *(công cụ đột biến — scratch)* | GHI NHẬN | `…/scratchpad/hc_h1_sua/dot_bien.py:111-113` · `…/scratchpad/r1_h1/dot_bien_r1.py` *(⛔ trong repo)* | Lượt 1 của chính R2 báo `R2-M08` **SỐNG** *(`49 passed`)*; chạy tay cùng đột biến ⇒ `1 failed`. Nguyên nhân: `M07` và `M08` cùng tăng tệp **+9 byte**, ghi trong cùng một giây ⇒ khoá `.pyc` *(mtime giây + cỡ)* trùng ⇒ Python nạp bytecode của `M07`. Thêm xoá `__pycache__` + `PYTHONDONTWRITEBYTECODE=1` ⇒ `M08` cắn *(`dot_bien_r2_luot1_PYC_CU.log` ↔ `dot_bien_r2.log`)*. Kịch bản của Dev *(chỉ bỏ `__pycache__` lúc CHÉP bản sao)* và R1 ⛔ xoá bytecode giữa các lượt; R2 chạy lại kịch bản Dev có chặn ⇒ **23/23** như `BG` ⇒ ⛔ số nào của `BG` sai | mọi kịch bản đột biến ghi đè cùng một tệp: xoá `__pycache__` + `PYTHONDONTWRITEBYTECODE=1` mỗi lượt *(`-p no:cacheprovider` ⛔ đủ — nó chỉ tắt `.pytest_cache`, ⛔ chạm `.pyc` của mô-đun nguồn)* | orchestrator *(luật chung cho Dev + Test)* |

⛔ **0** phát hiện làm một AC nào TRƯỢT; **0** CHẶN; **0** NÊN SỬA; **0** tệp ngoài làn; **0** PII.

## Bài thử ĐỀ XUẤT *(⛔ commit — orchestrator chỉ cho R2 commit phiếu + sổ)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `…/scratchpad/r2_h1/de_xuat/test_kq073_h1_r2.py::test_R2_01_BM_giu_DAU_AM_cua_ton_VND` | bản sao + `R2-M16` ⇒ `1 failed` *(đúng bài này)* | mã `7ced6b6` ⇒ PASSED |
| `…::test_R2_02_khoa_bang_ty_gia_mang_BOM_van_la_USD` | bản sao + `R2-M07` ⇒ `1 failed` *(đúng bài này)* | mã `7ced6b6` ⇒ PASSED *(log `chung_minh_de_xuat.log`)* |
| bài đề xuất của R1 `…/scratchpad/r1_h1/de_xuat/test_kq072_h1_r1.py` *(8 bài)* | mã `30c1c4a` ⇒ `7 failed, 1 passed` *(R2 chạy lại)* | mã `7ced6b6` ⇒ `8 passed` |

## Câu hỏi của vòng sửa *(Q5 · Q6 · Q7 — orchestrator chốt; R2 góp ý có số)*
- **Q5** *(chuyển bài đề xuất vào `tests/nghiem_thu/`)*: R2 đồng ý **A**, nhưng lệnh lượt này giới hạn commit đúng 2 tệp ⇒ hai tệp đề xuất *(R1: 8 bài · R2: 2 bài)* nằm ở scratch, đã chứng minh răng; orchestrator cho R3 hoặc lượt gộp chép vào.
- **Q6** *(BM/BN với VND)*: R2 đồng ý **A** — R2 viết BM độc lập từ ô *(`… + BI + …`)* và khớp mã; ca R2-B cho thấy hai cách chỉ khác trên bảng VND ≠ 1, mà C1 *(`isp/C1` `fls/cau_hinh/fx.py:22`)* xếp *"VND ≠ 1"* vào **dòng hỏng**.
- **Q7** *(đổi trạng thái sổ)*: R2 đã đổi — sổ v0.2.

## Ghi chú cho orchestrator
- **Worktree**: R2 ⛔ sửa tệp nào trong worktree ngoài 2 tệp commit; mọi đột biến chạy trên bản sao ngoài worktree; `git status` **0** dòng trước khi viết phiếu; HEAD trước = `1606f33`.
- **Cụm 5445**: lượt đường nền dựng lại `fls_test` như mọi lượt; R2 ⛔ chạy pytest nào song song với lượt đường nền *(phiên khác DROP `fls_test` giữa chừng — bài học `S0-R3-05`)*; ⛔ tạo kho khác.
- **Ngoài phạm vi commit của R2** *(đúng 2 tệp theo lệnh)*: dashboard §5 · `handoff/README.md` · ma trận `03_TRACEABILITY_GAP_REPORT.md` · trạng thái `WO-070`.
- `kiem_tai_lieu` SAU khi thêm phiếu này + sổ v0.2: exit **0** · `✅ cong tai lieu DAT — va no da do duoc that (177 file, 1882 bang, 726 o ngay, 104 ma QD)` *(+1 tệp · +10 bảng = đúng 10 bảng của phiếu này; sổ ⛔ thêm bảng — `K3 bang markdown khong lech (da do: 1882 bang)` ⇒ cả hai tệp CÓ được soi, Đ3)*.
- **Cho H4** *(⛔ phát hiện)*: `str(Decimal)` của ô ra số mũ ⛔ chuẩn *(`bvnd_ton = 0.000000` · `musd_ton = 0E-9` · `BM = -564396449.240840`)* — như R1 đã ghi; và ⛔ dùng `BM = BQ × 10^9` làm phép soát *(F-3)*.
