# KQ-074 — biên bản kiểm `BG-071` *(ISP 3.1.2 · Step 1 · `H1` · vòng **R3** — xác nhận cuối trước gộp)*

| | |
|---|---|
| **Thuộc** | [`BG-071`](BG-071-ban-giao-wo-070.md) · [`WO-070`](WO-070-isp-h1-ca-gl-thuan.md) · vòng trước: [`KQ-072`](KQ-072-kiem-h1-r1.md) *(R1)* · [`KQ-073`](KQ-073-kiem-h1-r2.md) *(R2)* |
| **Kiểm bởi** | `fls-test` *(R3 — phiên mới ở account mới, độc lập với R1 · R2 · tác giả)* · 2026-11-17 · orchestrator giao *(`chuyen_giao/brief/r3_h1.md`)* |
| **Phạm vi** | ① `git diff 1606f33 isp/H1` = **2** tệp, chỉ phiếu `KQ-073` + sổ v0.2 — **0** dòng mã/bài đổi sau R2 *(sha256 `gl.py` `c7c4094bd4e801a3…` · `test_gl.py` `05d874d84d593762…` = số R2 ghi)*. ② soát nhanh TOÀN bước `fls tests` đối chiếu `CALC_ZONE_406.md` *(nhánh chính, sha256 `e8c086c9be808818…` = R2)*. ⚠ Brief ghi `git diff e0bd4a6~1 isp/H1` — `e0bd4a6~1` = `5c0a2e2` *(commit mã đầu)* nên dải ấy BỎ SÓT chính commit mã đầu ⇒ R3 soát từ nền **`329fa68`** *(`5c0a2e2~1`)*: 3 tệp `fls/bao_cao/gl.py` +383 · `tests/bao_cao/test_gl.py` +708 · `tests/bao_cao/__init__.py` 0 byte |
| **Cụm** | reviewer **5445** *(`/home/user/fls-pg16-5445`, để CHẠY)* · log R3: `/tmp/claude-0/-home-user-FLS-tobe/262be30c-df99-57b1-a5f4-41b5c049cd87/scratchpad/r3_h1/` *(⛔ trong repo)* |
| **Phán quyết** | **`ĐẠT`** vòng R3 *(thang ISP: **0 CHẶN · 0 NÊN SỬA** còn mở ⇒ đủ điều kiện gộp + push)* — **4/4 AC ĐẠT** đo lại; **8/8 cột** BM–BT khớp công thức ô bằng phép so VI SAI ngẫu nhiên **12.000** ca · **656.409** ô · **0** lệch + **1.667/1.667** ca thiếu tỷ giá ném `ThieuTyGia` đúng hàng · tháng · tiền tệ. R2: **4** GHI NHẬN đều **CHƯA SỬA** *(⛔ mã đổi)* — R3 xét lại: **⛔ cái nào phải lên NÊN SỬA** *(§R2 xét lại)*. **3** phát hiện mới: **0** CHẶN · **0** NÊN SỬA · **3** GHI NHẬN *(`H1-R3-01…03`, lớp B1)* |
| **Sổ phát hiện** | [`docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H1.md`](../../04_Test/review/SO_PHAT_HIEN_ISP-3.1_H1.md) **v0.3** *(đổi ô Trạng thái 4 hàng `H1-R2-*` + thêm 3 hàng `H1-R3-*`)* |

## Cổng vào
| Kiểm | Kết quả |
|---|---|
| git | worktree `isp/H1` HEAD = `170fe8e` *(`KQ-073`)* ← `1606f33` ← `7ced6b6` *(mã + bài vòng sửa)*; `git status` **0** dòng trước mọi phép đo. Nhánh có mặt ở `origin/isp-chuyen/H1` + `origin/claude/laughing-bohr-331pt0-isp/H1` — đó là đẩy **chuyển account** do người dùng chọn *(`TIEN_DO.md` 17/11)*, ⛔ phải gộp; R3 ⛔ đẩy gì |
| spec | ISP **v3.1.2** Step 1 · H1 *(`git diff --stat 1606f33 isp/H1 -- docs/ITL/02_BA` rỗng)*; errata ① `H1-B1` = 0,098039… mUSD · ② BM/BN/BQ/BT giao H1 *(`TIEN_DO.md:96`)* |
| làn | diff R3 *(1606f33..)*: 2 tệp = phiếu + sổ ✔. Toàn bước *(329fa68..)*: **7** tệp — `fls/bao_cao/gl.py` · `tests/bao_cao/{__init__,test_gl}.py` *(BE-HC)* · `BG-071` · `KQ-072` · `KQ-073` · sổ H1 *(phiếu/sổ)* ✔; ⛔ chạm `.importlinter` · `pyproject.toml` · `fls/bao_cao/__init__.py` · `TIEN_DO.md` |
| ký tự vô hình · PII · bí mật | toàn bước **1.542** dòng THÊM: **0** ký tự vô hình *(NBSP · BOM · U+200B–D · U+2000–200A · U+2028/9 · U+202F · U+205F · U+3000 · NEL · VT · FF · U+1C–1F · U+1680)* · **0** email · **0** `secret/password/token/api_key =` · **0** DSN ngoài `fls:fls@` · grep `Email Address · Diễn giải · dien_giai · Số chứng từ · so_ct` = **1** dòng, là câu tự khai của `KQ-073` *("⛔ Diễn giải, Số chứng từ…")* ⇒ **0** PII. Số ≥ 9 chữ số: **97** chuỗi, đều là chữ số thập phân/tổng hợp của bài *(mUSD tuần hoàn, `2500000000`, `2·10^27`)* |
| kho thật | **⛔ CHẠM** — container ⛔ có sổ thật; kho `fls` @5445 `fls_itl` = **0** dòng *(K7)* |

## Cổng chạy lại *(R3 tự chạy TỪ worktree; `PG_DSN=…localhost:5445/fls` · `PG_DSN_TEST=…localhost:5445/fls_test` · `PYTHONUTF8=1` · `PYTEST_ADDOPTS` gỡ; venv `/home/user/FLS-tobe/.venv` dựng lại ở account mới)*
| Lệnh | `BG`/R2 nói | R3 đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/bao_cao/test_gl.py` | exit 0 · `49 passed` | exit **0** · `49 passed in 0.45s` | ✅ |
| `lint-imports` | exit 0 · `11 kept, 0 broken` | exit **0** · `Contracts: 11 kept, 0 broken.` · `fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho KEPT` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5445` *(cây `170fe8e` sạch, bắt đầu `03:18:59Z`)* | exit 0 · `KẾT: ĐẠT` · toàn bộ `12 failed, 2481 passed, 2 xfailed, 14 errors` · `26 = 26` · web `3 failed, 661 passed` · `3 = 3` | exit **0** *(`03:18:59Z → 03:27:02Z`)* · 7/7 `[ĐẠT]` *(K2 `postmaster.pid cổng 5445` · K4 `26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · K5 `11 kept` · K6 `chay 9845 / co 9967` · K7 `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2481 passed, 2 xfailed, 1 warning, 14 errors in 305.42s` ⇒ `[ĐẠT] … 26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 174.15s` ⇒ `[ĐẠT] … 3 = 3 node id` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong`. **Mẫu số** *(Đ3)*: 12 + 2.481 + 2 + 14 = **2.509** = số R2 *(0 skipped · 0 deselected)*; web 664 | ✅ |
| ↳ đỏ TRƯỚC khi có mã *(mục 8 ①)* | R1: `ModuleNotFoundError` | cây `329fa68` *(`git archive`, bản sao ngoài worktree, ⛔ `tests/conftest.py`)* + `test_gl.py` của `5c0a2e2` ⇒ exit **2** · `ModuleNotFoundError: No module named 'fls.bao_cao.gl'` · `1 error in 0.07s` *(đỏ vì THIẾU mô-đun, ⛔ lỗi cú pháp)* | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `177 file, 1882 bang` *(sau `KQ-073`)* | exit **0** · `(177 file, 1882 bang, 727 o ngay, 104 ma QD)` *(TRƯỚC khi thêm phiếu này; +1 ô ngày = sổ v0.3 đổi ngày)* | ✅ |
| `python tools/soi_bang_tuyen.py` | exit 0 · 40 tuyến | exit **0** · `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python tools/kiem_thuyet_minh.py` | exit 0 · 31/31 | exit **0** · `✅ CONG THUYET MINH DAT — 31/31 nut` | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech (da do 16/20 phep)` | exit **1** · `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` — `B3` · `B4` · `C5` · `C5b` KHONG DO DUOC · `A1` · `B1` · `C6` DOI TRANG THAI *(kho rỗng)* | ✅ *(đỏ do kho rỗng — y R2)* |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` | exit **0** · `khong co gi de ap` · `pg_verify: khop` *(chạy SAU lượt đường nền — ⛔ chồng)* | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC *(đòi `.venv/Scripts/lint-imports.exe`)* | exit **1** · `FileNotFoundError: … isp-h1/.venv/Scripts/lint-imports.exe` *(đường Windows gõ cứng — ⛔ thuộc H1)* | ✅ *(khớp; tính là **⛔ ĐO ĐƯỢC** — Đ5)* |

## Tám cột CALC ZONE — so VI SAI với cài đặt NGUYÊN VĂN công thức ô *(phép đo MỚI của R3, ⛔ lặp ca tay của R1/R2)*
`cong_cu/so_sanh_o.py` cài lại TỪNG ô của `CALC_ZONE_406.md` bằng `Fraction` *(⛔ import công thức `gl.py` — chỉ gọi `tinh_gl` để lấy số so)*: `AZ11 = AZ10+AX11-AY11` cho 5 tiền tệ · BO/BP = `INDEX/MATCH(tháng, D) × E|F / 10^9` · BQ/BT luỹ kế · BR/BS = `BO|BP / SUMIFS(USD) × 10^3` · BM = `AZ×USD + BC×SGD + BF×COP + BI + BL×HKD` *(tỷ giá THÁNG CỦA DÒNG)* · BN viết **từng số hạng như ô** `(AZ + BC×SGD/USD + … + BI/USD + …)/10^6`. Sinh ngẫu nhiên *(seed `20261117` · `7` · `42`, 4.000 ca mỗi seed)*: 1–9 dòng, 1–4 tháng, đủ 5 tiền tệ, Nợ/Có/cả hai vế/0, tiền 2 chữ số lẻ tới 10^10, tỷ giá lẻ tới 30.000,00, **bảng VND ≠ 1** ở ~10 % tháng *(ba ngữ nghĩa VND)*, khoá `fx` và mã dòng mang biến thể `ma_tien_te` *(`'usd'` · BOM · NBSP · U+3000 · U+2007)*, ~12 % tháng bị khoét một tiền tệ.

| Đo *(nhãn · mẫu số)* | seed 20261117 | seed 7 | seed 42 | Tổng |
|---|---:|---:|---:|---:|
| ca chạy | 4.000 | 4.000 | 4.000 | **12.000** |
| ô so *(13 ô/dòng: 8 cột BM–BT + 5 tồn nguyên tệ)* | 220.727 | 218.036 | 217.646 | **656.409** |
| ô lệch | 0 | 0 | 0 | **0** |
| ca ném `ThieuTyGia` · khớp *(hàng · tháng · tiền tệ ∈ tập THIẾU của ô)* | 548 · 548 | 557 · 557 | 562 · 562 | **1.667 · 1.667** |
| ca ô đòi ném mà mã ⛔ ném *(mất số im lặng)* | 0 | 0 | 0 | **0** |

Dung sai: ô ⛔ chia *(BM · BO · BP · BQ · 5 tồn)* = **bằng tuyệt đối**; BN · BR · BS = `|Δ| ≤ 10^-25 × |ô|`; **BT** = `|Δ| ≤ 10^-27 × i × Σ(|BR|+|BS|)` — lượt đầu R3 dùng dung sai tương đối cho BT và báo **4** ô "lệch" ở ca 777: BR = 163,27… rồi BS = 162,93… triệt tiêu còn BT = 0,346, sai số làm tròn 28 chữ số của TỪNG BR/BS *(~5·10^-26)* chia cho 0,346 ⇒ 1,4·10^-25 tương đối. Đó là đặc tính của cột LUỸ KẾ trên số làm tròn *(Sheets IEEE-754 tệ hơn ~10^11 lần)*, ⛔ lỗi mã — ghi để H4 khai dung sai BT theo **độ lớn luỹ kế**, ⛔ theo giá trị ô *(log `so_sanh_o.log`)*.

## R2 xét lại — 4 GHI NHẬN, có cái nào thật ra phải NÊN SỬA? *(brief §b)*
| Mã | Đo lại trên `170fe8e` | Lên NÊN SỬA? | Vì sao |
|---|---|:-:|---|
| `H1-R2-01` | `R3-M01` *(`abs(tồn VND)` ở BM)* ⇒ bộ Dev `49 passed` — **SỐNG**; mã đúng: VND Có 1.000 ⇒ BM `-1000` · BN `-4E-8` | ⛔ | Lỗ ở BÀI, ⛔ ở mã; ⛔ đường nào ra số sai im lặng hôm nay. H4 so BM với đáp án 406 trên sổ thật *(tồn VND âm là thường)* ⇒ hồi quy kiểu `abs` sẽ ĐỎ ở H4. Bài dựng lại `test_R2_01_…` cắn |
| `H1-R2-02` | `R3-M02` *(khoá `fx` qua `str.strip().upper()`)* ⇒ `49 passed` — **SỐNG**; mã đúng: khoá `'﻿USD'` ⇒ `ty_gia_usd = 25000` | ⛔ | Lỗ ở bài; hỏng nếu xảy ra là **ồn** *(`ThieuTyGia`)*, ⛔ im lặng; C1 *(`fls/cau_hinh/fx.py`)* chỉ phát 5 khoá sạch |
| `H1-R2-03` | ⓐ `gl.py:66` còn nguyên; R3 tái hiện: USD 100 @202501 rồi 2 dòng USD @202502 *(USD 25.000 → 25.500)* ⇒ BM `2.575.500` / `2.601.000` ≠ BQ × 10^9 `2.525.500` / `2.551.000` **cùng tháng 202502**. ⓑ đuôi AS-IS thông điệp `:181-182` vẫn một câu cho mọi lý do | ⛔ *(nhưng sửa TRƯỚC H4)* | Chỉ là chữ; Đ1 grep `BM = BQ\|BQ × 10` ở `docs/`+`fls/`+`tools/`+`isp-3.1/` = **2** dòng: `gl.py:66` *(câu sai)* + `BG-071:156` *(ghi ĐÚNG chiều `≠`)* ⇒ hôm nay **0** chỗ dựa vào đẳng thức. Rủi ro duy nhất: H4 dùng nó làm phép soát ⇒ sẽ ĐỎ ồn, ⛔ im lặng. Khuyến nghị: sửa cùng commit gộp hoặc mục đầu WO H4 |
| `H1-R2-04` | công cụ scratch — R3 áp luật: xoá `__pycache__` + `PYTHONDONTWRITEBYTECODE=1` mỗi lượt + đối chứng sha256 mô-đun ĐÃ NẠP **13/13** khớp | ⛔ | ⛔ chạm repo; việc orchestrator *(luật chung)* |

## Đột biến R3 *(`cong_cu/dot_bien_r3.py` — bản sao ngoài worktree, ⛔ `tests/conftest.py`, DSN trỏ cổng 1 ⇒ ⛔ chạm PG; đối chứng nạp: sha256 `gl.py` trong tiến trình con = sha của đột biến, **13/13**; trả nguyên ⇒ `c7c4094bd4e801a3` KHỚP)*
| Đột biến | Bộ Dev *(49 bài)* | + bài đề xuất R3 |
|---|---|---|
| `R3-M01` `abs(tồn VND)` ở BM *(= `R2-M16`)* | **SỐNG** | cắn — `test_R2_01_…` |
| `R3-M02` khoá `fx` `str.strip().upper()` *(= `R2-M07`)* | **SỐNG** | cắn — `test_R2_02_…` |
| `R3-M03` bộ đệm `bang_chuan` sống qua các lượt *(mức mô-đun)* | cắn *(≥ 4 bài)* | cắn |
| `R3-M04` BM bỏ tồn ÂM *(`if ton[t] > 0`)* | cắn — `test_R1_05_bon_cot_…` | cắn |
| `R3-M05` BM nhân tỷ giá tiền tệ DÒNG | cắn *(2)* | cắn |
| `R3-M06` BN ÷ tỷ giá tiền tệ dòng | cắn *(≥ 4)* | cắn |
| `R3-M07` tỷ giá 0 lọt *(`gia < 0`)* | cắn — `[bang_0]` | cắn |
| `R3-M08` BM dùng tồn TRƯỚC dòng | cắn *(≥ 4)* | cắn |
| `R3-M09` `TienKhongHuuHan` phía Có mang nhãn "Nợ" | **SỐNG** ⇒ `H1-R3-02` | cắn — `test_R3_02_…[co-Có]` |
| `R3-M10` `vi_tri` đếm từ 0 | cắn *(≥ 4)* | cắn |
| `R3-M11` bỏ ngữ cảnh `_NGU_CANH` | cắn — `test_ket_qua_khong_phu_thuoc_…` | cắn |
| `R3-M12` BR × 10^6 thay 10^3 | cắn *(≥ 4)* | cắn |
| `R3-M13` tra tỷ giá BO/BP bằng chữ THÔ *(⛔ `ma_tien_te`)* | cắn *(≥ 4)* | cắn |
| **Tổng** | **13** · cắn **10** · sống **3** | **13** · cắn **13** · sống **0** |

Log: `dot_bien_r3_bo_dev.log` · `dot_bien_r3_co_de_xuat.log`.

## Bảng AC *(`WO-070` = ISP Step 1 mục 6 — đo lại trên `170fe8e`)*
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 · `H1-B1` | VND Nợ 2.500.000.000 @ USD 25.500 ⇒ bVND 2,5 · mUSD **0,098039…** *(errata ①)* | `test_H1_B1_…` + `test_R1_07_BR_dung_tuyet_doi_…` PASSED *(`str(musd_no) == "0.09803921568627450980392156863"`)*; vi sai: 12.000 ca BO/BR 0 lệch | **ĐẠT** |
| AC-2 · `H1-B2` | dòng USD Có ⇒ tách đúng cột Có; tồn = tồn trước − Có | `test_H1_B2_…` PASSED; vi sai: tồn 5 tiền tệ × mọi dòng *(trong 656.409 ô)* 0 lệch, gồm dòng cả hai vế | **ĐẠT** |
| AC-3 · `H1-B3` | tháng ⛔ có tỷ giá ⇒ lỗi CÓ TÊN, ⛔ trả 0 | 5 bài `H1-B3` + `test_R1_05_BM_ton_khac_0_…` PASSED; vi sai: **1.667/1.667** ca thiếu ⇒ `ThieuTyGia` đúng hàng/tháng/tiền tệ, **0** ca ô đòi tỷ giá mà mã trả số | **ĐẠT** |
| AC-4 · `H1-B4` | `fls/bao_cao` ⛔ chạm DB | `lint-imports` exit 0 · `11 kept`; `test_H1_B4_…` + hai bài `test_R1_06_…` *(sys.modules · cây cú pháp)* PASSED; `gl.py` import: `__future__` · `dataclasses` · `decimal` · `typing` · `fls.canon.tien_te` — **0** `environ/getenv/open(/psycopg` | **ĐẠT** |
| Goal *(ISP §2)* | đúng tay tính trên 6 dòng tổng hợp | `test_H1_sau_dong_…` *(60 ô)* + `test_R1_05_bon_cot_…` *(24 ô)* PASSED | **ĐẠT** |

## Đối chiếu ISP Step 1 mục 8
| Dòng | Bằng chứng | Phán quyết |
|---|---|---|
| ① *H1-B1…B4 xanh, đỏ trước khi có mã* | xanh: `49 passed` · `11 kept`; đỏ trước: R3 tái hiện trên cây `329fa68` ⇒ `ModuleNotFoundError: No module named 'fls.bao_cao.gl'` *(exit 2)* | **ĐẠT** |
| ② *3 vòng review xong* | R1 `KQ-072` ✔ · R2 `KQ-073` ✔ · R3 = phiếu này ✔ | **ĐẠT** |
| ③ *PUSH: đủ R1 · R2 · R3, phát hiện chặn = 0* | CHẶN: R1 **0** · R2 **0** · R3 **0**; NÊN SỬA còn mở = **0** *(`H1-R1-01` đã sửa ở R2)* ⇒ đúng thang chuyển giao §4 *"0 CHẶN và 0 NÊN SỬA còn mở"* | **ĐẠT** *(orchestrator gộp + push)* |

## Đ1 · Đ3 · Đ4 · Đ5
| Luật | Kiểm | Kết quả |
|---|---|---|
| **Đ1** *(câu phủ định — grep `docs/` + `fls/`+`tools/`)* | `gl.py:22` *"`CALC_ZONE_406.md` ⛔ có trong `isp/H1`"* ⇒ `ls docs/ITL/01_Orchestrator/isp-3.1/` của worktree = `TIEN_DO.md` ✔ · `:79-80` *"⛔ một tỷ giá nào gõ trong mã"* ⇒ hằng số duy nhất `10^3/6/9` + `0` ✔ · `:112` *"⛔ đọc kho, ⛔ đọc biến môi trường"* ⇒ grep `environ\|getenv\|open(\|psycopg` = **0** dòng mã ✔ · `:126` *"trước H1 grep `musd\|bvnd\|ty_gia` ở `fls/`+`tools/` = 2 dòng docstring"* ⇒ `git grep` @`329fa68` **có `-i`** = **2** *(`fls/bao_cao/__init__.py:3-4`)*, **⛔ `-i`** = **0** ⇒ câu đúng khi đọc là không phân biệt hoa/thường *(⛔ ghi cờ — ghi nhận nhỏ, ⛔ mở hàng sổ)* · `H1-R2-03` grep: mục trên | ĐẠT |
| **Đ3** *(0 phải có mẫu số)* | mọi "0 lệch" của phiếu kèm mẫu: 656.409 ô · 12.000 ca · 1.667 ca ném · 13 đột biến · 1.542 dòng thêm · kho `fls_itl` 0 dòng ⇒ ⛔ kết luận gì về sổ thật | ĐẠT |
| **Đ4** *(số có nhãn)* | đơn vị ô: BM = VND · BO/BP/BQ = bVND *(÷ 10^9)* · BN/BR/BS/BT = mUSD *(triệu USD)* — docstring `gl.py:43-49` khớp `CALC_ZONE_406.md` hàng 9 | ĐẠT |
| **Đ5** *(cổng khai `mong`, đã chứng minh đỏ)* | `--duong-nen` so theo node id với tệp đường nền *(`26 = 26`)* + mong mẫu số; bài H1 đều so số tay ghi sẵn *(⛔ tự sinh từ mã — R2 kiểm 48/48 ô mong bằng `Fraction`)*; đột biến 10/13 cắn trên bộ Dev | ĐẠT |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(ISP Step 1 + `CALC_ZONE_406.md` + `INV-I16` + `BA-07` §4g)* | **ĐẠT có ghi chú.** 8/8 cột + tồn luỹ kế + tháng thiếu ⇒ `ThieuTyGia` có tên đúng trên 12.000 ca vi sai; ⛔ phạm vi lấn bước khác ngoài quyết định orchestrator *(BM–BT = `TIEN_DO.md:95`)*; ⛔ refactor không do bài đòi *(R2 đã soát; R3: ⛔ mã đổi từ đó)*. Ghi chú: 3 lỗ bài *(`R2-01` · `R2-02` · `R3-02`)* + lỗi có tên ⛔ pickle được *(`R3-01`)* | `so_sanh_o.py` + `.log` · `dot_bien_r3.py` + 2 log · `de_xuat/test_kq074_h1_r3.py` |
| **Dữ liệu** *(kho, chỉ đọc)* | **⛔ ĐO ĐƯỢC trên sổ thật — đúng phạm vi H1** *(ISP §3 Loại trừ: dữ liệu thật = H4)* | `fls_itl` @5445 = **0** dòng *(K7)* ⇒ mẫu số 0 ⇒ ⛔ kết luận "không lệch" trên sổ thật |
| **Màn hình** | **N/A** | ISP Step 1 §4 *"Frontend: N/A"*; diff ⛔ chạm `fls/web/**`; ⛔ dựng 8088 |

## Phát hiện mới *(chi tiết + luật phòng tái phạm: sổ v0.3)*
| F | Mã sổ | Lớp | Mức | Nơi *(@ `7ced6b6`)* | Tái hiện *(R3 đã chạy)* | Khuyến nghị | Gửi |
|---|---|---|---|---|---|---|---|
| F-1 | `H1-R3-01` | B1 | GHI NHẬN | `fls/bao_cao/gl.py:172-183` · `:197-204` | `pickle.loads(pickle.dumps(ThieuTyGia(202501,'USD',1,'x')))` ⇒ `TypeError: ThieuTyGia.__init__() missing 3 required positional arguments: 'tien_te', 'vi_tri', and 'ly_do'`; `copy.copy` cùng lỗi; `TienKhongHuuHan` thiếu 2 ⇒ **2/2** lớp hỏng cả hai đường. Lỗi CÓ TÊN *(D1)* thành `TypeError` khi qua `ProcessPoolExecutor`/`multiprocessing`. Hôm nay grep `multiprocessing\|ProcessPool\|pickle` ở `fls/`+`tools/` = **0** ⇒ 0 tác động | thêm `__reduce__` trả `(type(self), (trường gốc…))` + giữ `ly_do`/`gia_tri` làm trường — R3 thử trên bản sao: bài đề xuất `test_R3_01_…` **XANH**, bộ Dev `49 passed` giữ *(`r3_01_do_xanh.log`)* | `DEV` *(trước H4 — H4 là bước đầu có lý do chạy song song theo kỳ)* |
| F-2 | `H1-R3-02` | B1 | GHI NHẬN | `fls/bao_cao/gl.py:267` · `tests/bao_cao/test_gl.py:410-426` | `R3-M09` *(phía Có gửi nhãn "Nợ")* ⇒ `49 passed` SỐNG — `test_R1_02_…` chỉ đòi lớp + `vi_tri`, ⛔ đòi `nhan` mà docstring `:193` khai *"Mang `vi_tri` và `nhan`"*. Mã đúng | thêm `test_R3_02_TienKhongHuuHan_mang_dung_nhan_phia[no/co]` *(cắn `R3-M09`)* | `DEV` |
| F-3 | `H1-R3-03` | B1 *(quy trình — bằng chứng)* | GHI NHẬN | `KQ-072` · `KQ-073` *(mọi câu "log `…`" + bài đề xuất)* | chuyển account 17/11 ⇒ scratchpad R1/R2 ⛔ còn: `find / -name 'test_kq07*'` = **0**; `chuyen_giao/` chỉ có brief + khuôn ⇒ Q5 của R2 *(chép bài đề xuất vào `tests/nghiem_thu/`)* ⛔ còn bài để chép | chép **`r3_h1/de_xuat/test_kq074_h1_r3.py`** *(5 bài: 2 của R2 dựng lại + 3 của R3, đã chứng minh răng)* vào `tests/nghiem_thu/test_kq074_h1_ca_gl.py` ở lượt gộp; về sau bằng chứng mà phiếu dẫn phải commit cùng phiếu hoặc ghi đủ trong phiếu | orchestrator |

⛔ **0** phát hiện làm một AC nào TRƯỢT; **0** CHẶN; **0** NÊN SỬA; **0** tệp ngoài làn; **0** PII; **0** bí mật.

## Bài thử ĐỀ XUẤT *(⛔ commit — brief chỉ cho R3 commit phiếu + sổ; tệp ở scratch `r3_h1/de_xuat/test_kq074_h1_r3.py`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `test_R2_01_BM_giu_DAU_AM_cua_ton_VND` *(dựng lại của R2)* | bản sao + `R3-M01` ⇒ đỏ đúng bài này | mã `7ced6b6` ⇒ PASSED |
| `test_R2_02_khoa_bang_ty_gia_mang_BOM_van_la_USD` *(dựng lại của R2)* | bản sao + `R3-M02` ⇒ đỏ đúng bài này | mã `7ced6b6` ⇒ PASSED |
| `test_R3_01_loi_co_ten_qua_duoc_pickle_va_copy_giu_nguyen_truong[ThieuTyGia\|TienKhongHuuHan]` | mã `7ced6b6` ⇒ **2 failed** *(`TypeError … missing … positional arguments`)* | bản sao + `__reduce__` ⇒ PASSED *(cả bộ `53 passed`)* |
| `test_R3_02_TienKhongHuuHan_mang_dung_nhan_phia[no\|co]` | bản sao + `R3-M09` ⇒ đỏ `[co-Có]` | mã `7ced6b6` ⇒ PASSED |

## Ghi chú cho orchestrator
- **Worktree**: R3 ⛔ sửa tệp nào ngoài 2 tệp commit; mọi đột biến/bản sao ngoài worktree; `git status` **0** dòng trước khi viết phiếu; HEAD trước = `170fe8e`.
- **⚠ Khi gộp `H1` SAU `S0` mới** *(`isp/S0` @ `c1cf29b`, `MONG_PYTEST_TOAN_BO=2490`)*: bài `tests/test_dung_moi_truong_isp.py::test_S0_R3_02_…` đòi hằng **=** số bài THU THẬP *(`assert (mong_tb, mong_web) == (len(nid), len(web))`)*; H1 thêm **49** bài *(`tests/bao_cao/test_gl.py`)* trên nền `3d8318c` ⇒ sau gộp phải nâng hằng **+49** trong commit gộp *(như CG1 đã làm 2460 → 2493)*, ⛔ thì bài ấy ĐỎ. Cổng `--duong-nen` của chính `isp/H1` là bản S0 cũ *(⛔ có bài ấy)* nên R1–R3 ⛔ thấy.
- **Dải brief**: `git diff e0bd4a6~1 isp/H1` bỏ sót commit mã đầu `5c0a2e2` *(xem Phạm vi)* — R3 đã soát từ `329fa68`.
- `kiem_tai_lieu` SAU khi thêm phiếu này + sổ v0.3: exit **0** · `(178 file, 1894 bang, 727 o ngay, 104 ma QD)` *(+1 tệp · +12 bảng = đúng 12 bảng của phiếu này — Đ3: tệp CÓ được soi)*.
- `--duong-nen` in thêm `1 warning` so với R2: `tools/sinh_ban_do_tang.py:214 SyntaxWarning: invalid escape sequence '\|'` — tệp ⛔ thuộc diff H1, lộ ra vì venv mới chưa có bytecode; ⛔ ảnh hưởng `KẾT`.
- **Cho H4**: ① dung sai BT theo độ lớn LUỸ KẾ *(§Tám cột)*; ② ⛔ dùng `BM = BQ × 10^9` làm phép soát *(`H1-R2-03`)*; ③ sửa `H1-R3-01` trước khi chạy song song theo kỳ.
