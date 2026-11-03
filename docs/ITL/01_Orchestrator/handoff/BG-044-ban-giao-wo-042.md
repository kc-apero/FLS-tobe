# BG-044 — bàn giao `WO-042`

| | |
|---|---|
| **Thuộc** | `WO-042` *(vòng 1)* |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `db0adae` *(đã đẩy)* — nền khi nhận `77737f7` *(mã `fls/**` cuối `3c13ce3`)* |
| **Câu hỏi mở kèm** | [`HOI-043`](HOI-043-ba-bai-kq041-khong-the-xpass-va-nut-thu-lai.md) `KHONG_CHAN` — ba bài `xfail(strict)` `kq041` **⛔ thể** `XPASS` bằng mã đúng spec *(gác của chính bài)*; `Thử lại` của `②b` ⛔ có từ trước |

## Đã đổi

| Tệp | Vì sao |
|---|---|
| `fls/web/tep/man_f01_ghep.js` | **(a)** `tai_danh_sach` mang số lượt `_luot`; sau **mỗi** `await` lượt bị thay **bỏ đi im lặng** *(⛔ ghi `ST.dong` · ⛔ `dang_tai` · ⛔ `loi` · ⛔ `het`/`con_tro`/`tro` · ⛔ xin trang/cửa kế)*; hàng gom vào mảng **riêng của lượt**, đặt vào `ST.dong` **một lần** khi thắng; trả `true` ⇔ thắng. `doi_chip`: bấm lại chip **đang chọn** khi `ST.dang_tai` ⇒ `return` *(**0** `GET`)*; chỉ vẽ lại khi lượt thắng. `mo_man`: ⛔ mở lượt khi một lượt đang bay *(cửa vào thứ hai của luật ②)* |
| `fls/web/tep/man_f01_lenh.js` | **(b)** hằng `LY_DO_LO` *(một lần gõ)* dùng ở ⓐ ghi chú băng + ⓑ `note ok`; ⓑ dựng bằng `textContent` *(⛔ `innerHTML`, ⛔ `⭐`/`⛔`)*; ⓒ nhãn `chỉ CHƯA NHẬN THEO LÔ`; ⓓ `RO.may` chữ v4.18; xuất `F01L.LY_DO_LO` cho bài thử |
| `fls/canon/tien_te.py` *(mới)* | **(c)** `TAP_TRANG_TIEN_TE` *(30 = Python `isspace` 29 ＋ `U+FEFF`, viết bằng **điểm mã**)* + `ma_tien_te = str(c or "").strip(TAP).upper()`. Đặt ở `fls.canon` vì `fls.adapters` *(`pm_join._cur`)* ⛔ được nhập `fls.repo` *(hợp đồng 6)* |
| `fls/repo/man_ghep.py` | `ma_tien_te` / `TAP_TRANG_TIEN_TE` nhập từ `fls.canon.tien_te` — **cùng đối tượng hàm**, giữ mọi chỗ gọi cũ *(`mg.ma_tien_te`)* |
| `fls/repo/ghi_tay.py` | `:653` `_tien_dong_so` + `:744` `ghep_lenh` *(cửa **GHI**)* ⇒ `ma_tien_te` |
| `fls/repo/do_mau_so.py` | `:415` + `:417` `ds_tu_chung` *(cổng tự chứng)* ⇒ `ma_tien_te` |
| `fls/repo/doc_bao_cao.py` | `:373` `ung_vien_pm` ⇒ `ma_tien_te` |
| `fls/adapters/pm_join.py` | `_cur` ⇒ `ma_tien_te`, **giữ** nghĩa bỏ chuỗi rỗng |
| `fls/repo/lenh_cho.py` | `_SQL_ITL_UNG_VIEN` + `_SQL_DEM_CUNG_TE`: `upper(btrim(i.curr, %(tap)s))`, tham số `tap` = hằng *(⛔ `E' \t\r\n'` gõ trong SQL)*; nhập `ma_tien_te` ở đầu tệp *(hết vòng nhập với `man_ghep` — bỏ hai lần nhập trong hàm)* |
| `fls/web/tep/thanh_phan.js` | `TP.TAP_TRANG_TIEN_TE` *(bản chép, `String.fromCharCode` theo điểm mã)*; `TP.ma_te` gỡ đúng tập ấy *(⛔ `trim()`)*; `TP.tien` gọi `ma_te` |
| `tests/web/test_wo042_doi_chip_khi_dang_tai.py` *(mới)* | `AC-1`…`AC-4` — 12 bài DOM, cửa giả **giữ** từng lượt tới khi kịch bản thả *(⛔ đồng hồ)* |
| `tests/web/test_wo042_bon_chuoi_f01l_cua_that.py` *(mới)* | `AC-6` — thân `/ro` **cửa thật** kho TEST *(ca có `t > 0` **và** `c > 0`)*; quét nguồn chữ cũ |
| `tests/web/test_wo042_mot_tap_ky_tu_trang.py` *(mới)* | `AC-8` · `AC-9` · nửa `AC-11` — Python / PG / JS 30 / 30, `U+200B` giữ, chiều đỏ luật cũ **trong bài** *(SQL 26 · JS 5 · Python 1)*; quét AST `.strip().upper()` + JS + SQL; sổ thật chỉ đọc |
| `tests/api/test_wo042_mot_tap_cua_that_pg.py` *(mới)* | `AC-10` — HTTP kho TEST: NBSP+VND vào bậc `tien` + `tong_cung_tien_te` theo oracle **Python**; BOM+VND rổ `may`; `POST /match` ⇒ `200` *(ghi kho TEST)* |
| `tests/web/ca_wo042.py` *(mới)* | ca kho TEST bốn lệnh `S M A B` *(ký tự biên bằng `chr()`)* |
| `tests/web/test_wo037_v2_bang_f01l_cua_that.py` | `GHI_CHU` sang chữ v4.18 ⓐ — **lo gốc giữ** *(`c` của cửa, ⛔ màn đếm; ba chuỗi khác vẫn v4.17)*; lý do ghi tại chỗ |
| `tests/api/test_wo037_v2_ro_nguoi_hai_cau_pg.py` | `AC-14` phía mong đếm bằng **Python** `ma_tien_te` *(trước: một bản SQL bốn ký tự — `BG-040` yếu #4; sau v3.11 nó đếm **thiếu** dòng NBSP mà ca `WO-042` để lại)*; `AC-15` ghim `upper(btrim(i.curr, %(tap)s))` ×2 — **lo gốc giữ** *(⛔ `upper(i.curr)` trần)* |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` · `12_P6_WEB_PLAN.md` *(v0.17)* | dòng changelog · quy ước thứ chín *(lượt mới nhất thắng · một tập cho ba ngôn ngữ)* |
| `handoff/HOI-043-…` *(mới)* · `WO-042` · `README.md` · dashboard §5 | phiếu |

## Cổng *(kết quả nguyên văn; `PG_DSN='postgresql://fls:fls@localhost:5433/fls'`)*

| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `2297 passed, 6 xfailed in 383.11s (0:06:23)` — **0** đỏ. 6 `xfailed` = 3 `kq021` *(`WO-023`)* ＋ **3 `kq041`** *(vẫn `xfail`, ⛔ `XPASS` — `HOI-043`)*. Nền `WO-042`: `2268 passed, 6 xfailed` ⇒ **+29** = bài mới *(12 ＋ 3 ＋ 11 ＋ 3)*; 2 bài `WO-037` sửa phía mong *(⛔ thêm/bớt)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc`. **Tách nền** *(chạy cùng phút trên cây `77737f7` qua worktree)*: nền **50** *(`⛔ … — 50 lech/khong-do-duoc`, cùng **tên** nhóm với `WO-042` bảng nền)* ＋ **5** đỏ mới, cả 5 loại *(c)* do phiếu này: `bản vẽ · caption khối 3 (canon)` nhóm 2 `5 → 6` *(tệp)* · nhóm 3 `402 → 476` *(dòng)* · `bảng tiến độ · canon` `402 → 476` · `bản vẽ · caption khối 7 (adapters)` nhóm 3 `1.350 → 1.354` · `bảng tiến độ · adapters` `1.350 → 1.354` *(tệp mới `fls/canon/tien_te.py` + 4 dòng `pm_join._cur`)*. **50 + 5 = 55** ✔. 50 tên còn lại trùng nền **50 / 50**, giá trị trôi theo nhịp *(số bài, số dòng)*. ⛔ `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (134 file, 1482 bang, 688 o ngay, 104 ma QD), khong chi 'khong thay loi'` |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` *(= nền `KQ-041` 17/20)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` *(⛔ tuyến mới)* |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` *(103 tệp, 349 phụ thuộc — `fls.canon.tien_te` được `adapters` + `repo` nhập, hợp đồng 3/6 giữ)* |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — ⛔ chạm `schema.py` / migration |

## Bằng chứng từng AC

**Chiều đỏ chung** *(Đ5)*: bốn tệp bài mới chạy trên cây `77737f7` *(worktree; chỉ chép thêm `fls/canon/tien_te.py` để bài nhập được)* ⇒ **`24 failed, 5 passed`** — 5 xanh là bài **về chính hằng** *(`AC-8` tập · Python · PG — ⛔ phụ thuộc mã đã vá)* + `AC-11` sổ thật + bài mỏ neo `AC-3` *"sau lỗi bấm lại = tải lại"* *(hành vi cũ giữ nguyên)*. Trên mã mới **32 / 32** xanh.

| AC | Bằng chứng của Dev |
|---|---|
| AC-1 | `test_wo042_doi_chip_khi_dang_tai.py::test_AC1_*` ×3 *(lượt `Chưa gán` về **sau** / về **trước** lượt `Đã gán`; lượt bị thay ⛔ xin cửa kế)*. Mã khi nhận: `⛔ chip 'Đã gán' mang hàng rổ cũ: ['G2-0','G2-1','G2-2','G1-0',…,'G3-1']` *(n 10 = 3 ＋ 5 ＋ 2 — bản thu nhỏ của `2955`)*. `kq041::test_F3_doi_chip_*` `--runxfail` trên mã mới: `tt ['da_gan']` **đúng**, đỏ **chỉ** ở gác `goi 2 >= 3` ⇒ `HOI-043` Q2 |
| AC-2 | `::test_AC2_bam_lai_chip_dang_chon_*` *(GET **2** = một lượt; mã khi nhận **4**)* · `::test_AC2_mo_man_khi_dang_tai_*` *(cửa vào thứ hai)*. `kq041::test_F3_bam_lai_*` `--runxfail`: `n 2 == khac 2` **đúng**, đỏ **chỉ** ở gác `goi 2 >= 4` — gác đòi đúng điều `ⓥ` ② cấm ⇒ `HOI-043` Q1 |
| AC-3 | `::test_AC3_*` ×5: lượt cũ xong khi lượt mới đang tải ⇒ `dang_tai true` + *"Đang hỏi sổ…"*, `.dem` vắng *(mã khi nhận: `dang_tai False`, `'7 dòng'`)* · lượt cũ **lỗi** ⇒ ⛔ câu lỗi *(mã khi nhận: `'Máy gặp lỗi bên trong.'` dưới chip mới)* · lượt **mới** lỗi ⇒ `⛔ Cửa lỗi: …`, lượt cũ về sau ⛔ đổ hàng · lượt mới **mất kết nối** + lượt cũ lỗi khác ⇒ giữ `Không nối được tới máy chủ FLS.` · hết tải bấm lại chip = tải lại. ⚠ `②b` ⛔ có nút `Thử lại` riêng *(trước và sau)* ⇒ `HOI-043` Q4 |
| AC-4 | `::test_AC4_doi_nhanh_CHUA_DA_CHUA_*` *(chỉ hàng của lượt **thứ ba** — mã `G<k>`; mã khi nhận: 3 hàng `da_gan` + hàng `G1`/`G2`)* · `::test_AC4_doi_sang_chip_CHUA_CO_CUA_*` *(`Tất cả` cũng là một lượt mới)* |
| AC-5 ⭐ | **Chrome headless 1440×900, chuột thật** *(`Input.dispatchMouseEvent` trên toạ độ `getBoundingClientRect`)*, CDP `Fetch` **giữ** `lenh-cho?ro=nguoi` **2 s** *(ⓐ ⓑ)* / mọi `/queue/lenh-` **1,5 s** *(ⓒ)*; số hàng mong = Σ `rows` của **thân cửa thật** cùng lượt *(`Network.getResponseBody`)*. Bảng dưới. Console: **0** lỗi JS / ngoại lệ — một mục `Log` duy nhất mỗi lượt là `favicon.ico 404` *(có cả ở đối chứng)*. **0** `POST` mọi lượt. |
| AC-6 | `test_wo042_bon_chuoi_f01l_cua_that.py` ×3 — thân `/ro` cửa thật kho TEST `{'may': 3, 'nguoi': 1, 'khong': 0, 'tu_chung': 2, 'tong': 4, 'nguoi_khac_tien_te': 0}` ⇒ `t 2 · c 1`; bốn chuỗi = chữ chép từ `BA-06` v4.18 *(⛔ đọc JS)*; `LY_DO_LO` giống hệt ở ⓐ ⓑ **và** = `F01L.LY_DO_LO`; **0** ký tự `CAM`; quét nguồn ngoài chú thích: 4 chuỗi cũ **0**, câu `LY_DO_LO` gõ **1** lần. Mã khi nhận: ⓐ còn chữ v4.17, `KeyError 'ly_do_lo'` |
| AC-7 ⭐ | Chrome chuột thật. **8097 sổ thật chỉ đọc** *(mã mới)*: `/ro` thân `{'may': 184, 'nguoi': 616, 'khong': 801, 'tu_chung': 64, 'tong': 1601, 'nguoi_khac_tien_te': 84}` ⇒ ghi chú băng = `Còn 120 dòng` ＋ `LY_DO_LO` ＋ ` Phải mở từng dòng. Xem 120 dòng`; bấm *Số liệu kiểm chứng* ⇒ `note ok` = `… có 64 dòng tự chứng — … Còn 120 dòng` ＋ `LY_DO_LO` ＋ ` Phải mở từng dòng.`; hàng `may` = chữ ⓓ; bấm `Xem 120 dòng` ⇒ nhãn `đang xem rổ: máy trả lời được · chỉ CHƯA NHẬN THEO LÔ`. Lưới: trang đầu **50** *(`het false`)*; cửa `ro=may&tu_chung=0` mọi trang = **120** = `c` *(đo ở `AC-5` ⓑ)*. ⚠ Nút `Xem thêm` **bị khoá** ở máy chỉ đọc *(`disabled`, `title` "⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC…" — `man_f01_lenh.js:544` đi qua `_nut` ⇒ `_chan_ghi` dù là thao tác **đọc**; có từ trước, ngoài phạm vi — xem *Phát hiện ngoài phạm vi*)* ⇒ "số hàng lưới = c" đo được bằng mắt **chỉ** ở 8099. **8099 kho TEST** *(`cho_ghi true`)*: `/ro` `{may 2, nguoi 1, tu_chung 1, tong 3}` ⇒ cùng bốn chuỗi với `c 1 · t 1`; `Xem 1 dòng` ⇒ nhãn ⓒ, lưới **1** = `c`, `het true`. Console **0** lỗi JS; **0** `POST` |
| AC-8 | `test_wo042_mot_tap_ky_tu_trang.py::test_AC8_*` ×6: tập **30** = `{c.isspace()} ∪ {U+FEFF}` *(so tập trên `sys.maxunicode`)*; `mg.ma_tien_te is ma_tien_te`; Python **30 / 30**, PG kho TEST `upper(btrim(x‖'vnd'‖x, <hằng>))` **30 / 30**, JS `TP.ma_te` **30 / 30**; `U+200B` cả ba **giữ**; tập JS đọc từ nguồn **=** tập Python; `TP.tien('100', U+0085+'usd')` = `100,00`. Chiều đỏ **trong bài**: SQL `E' \t\r\n'` hỏng **26 / 30** · JS `trim()` hỏng **U+001C…U+001F, U+0085** *(5)* · Python `strip()` hỏng **U+FEFF** *(1)*. `kq041::test_F2_*` `--runxfail`: vẫn đỏ **6 / 6** — bài so với **câu SQL của chính bài** *(`:50`)*, ⛔ SQL của mã ⇒ `HOI-043` Q3 |
| AC-9 | `::test_AC9_QUET_strip_upper_*`: `.strip().upper()` trong `fls/` *(AST — chú thích, chuỗi ⛔ tính)* = **đúng** `{canon/tien_te.py:ma_tien_te, canon/spec.py:pos_of}` *(mã khi nhận: thêm `pm_join._cur` · `doc_bao_cao.ung_vien_pm` · `do_mau_so.ds_tu_chung` · `ghi_tay._tien_dong_so` · `ghi_tay.ghep_lenh`)*; tự chứng chèn mẫu vào bản sao `ghi_tay.py` ⇒ bắt **1**; JS ngoài chú thích `trim().toUpperCase()` **0** *(mã khi nhận: 2 ở `thanh_phan.js`)*; SQL: `btrim(i.curr` **2** chỗ, cả hai `%(tap)s`, chuỗi `E' \t\r\n'` **0** ngoài docstring *(mã khi nhận: 2 + 2)* |
| AC-10 | `test_wo042_mot_tap_cua_that_pg.py` ×3 *(HTTP, kho TEST)*: ① `A` ⇒ dòng `'\xa0VND'` bậc **`tien`**; `tong_cung_tien_te` **4** = oracle Python `ma_tien_te` **4 / 4** dòng chưa nối *(trong đó luật SQL cũ bỏ sót **1**)* · ② lệnh `BOM+VND` ở rổ `may`, `nguoi_khac_tien_te 0` · ③ `POST /queue/{itl}/match` ⇒ **200**, `moi_noi` = lệnh `B`. Mã khi nhận: ① `⛔ dòng NBSP+VND … ⛔ ở danh sách ứng viên` · ② `B` ⛔ ở `may` *(`nguoi_khac_tien_te 1`)* · ③ **422** `FLS-DQ-FAILED … dong lenh la ['\ufeffVND']` |
| AC-11 | **Sổ thật chỉ đọc** *(`noi_chi_doc(dsn_that())`, `default_transaction_read_only = on`, hàm thật)*: `dem_theo_ro` mã khi nhận *(worktree `77737f7`)* = mã mới = `{'may': 184, 'nguoi': 616, 'khong': 801, 'tu_chung': 64, 'tong': 1601, 'nguoi_khac_tien_te': 84}` — **6 / 6** khoá bằng nhau, ảnh `NAP-2026-10-02-PMA07ED283` trước = sau. `curr` mang ký tự của tập ở mép: `fls_itl` **0 / 8.387** · `fls_pm_line` **0 / 276.028** *(bài `test_AC11_SO_THAT_*`, in mẫu số)* |
| AC-12 | Cổng ở trên. ⚠ **Lệch nguyên văn `AC-12`:** `kq041` **0** `XPASS` *(3 `xfailed`)* — cả ba **⛔ thể** `XPASS` dưới mã đúng spec *(`HOI-043`)*. Bằng chứng thay: bản sao ba bài ở scratchpad đổi **đúng** ba chỗ `HOI-043` nêu *(gác `>= 2` · tập SQL từ hằng)*, mọi `assert` thực chất giữ ⇒ mã mới **`3 passed`**; mã khi nhận ⇒ hai bài `F3` đỏ **đúng lý do `KQ-041`** *(`tt ['chua_gan', 'da_gan', 'chua_gan']` · `n 4 == 2`)*. 3 `kq021` vẫn `xfail` |

### `AC-5` — Chrome, số đo từng ca

| Máy · mã | Ca | Chip in | `ST.dong` theo trạng thái | Thân cửa thật cùng lượt | `GET` |
|---|---|---|---|---|---|
| **8097** sổ thật chỉ đọc · **mã khi nhận** *(đối chứng, worktree `77737f7`)* | ⓐ bấm `Đã gán` khi `ro=nguoi` đang giữ | **`2955 dòng`** | `da_gan 2219 · chua_gan 736` | `lenh-da-gan` 5 trang = **2.219** | 8 |
| ″ | ⓑ bấm lại `Chưa gán` khi đang giữ | **`1472 dòng`** *(khác **736**)* | `chua_gan 1472` | một lượt = **736** *(500 ＋ 116 ＋ 120)*; mạng **6** = mỗi đường hai lần | 6 |
| **8097** sổ thật chỉ đọc · **mã mới** | ⓐ | **`2219 dòng`** | `da_gan 2219` · **0** `chua_gan` | **2.219** | 6 *(lượt cũ dừng sau 1 trang)* |
| ″ | ⓑ | **`736 dòng`** | `chua_gan 736` *(khác 736)* | **736** | **3** = số trang của **một** lượt |
| ″ | ⓒ `Đã gán → Chưa gán → Đã gán`, mọi `/queue/lenh-` giữ 1,5 s | **`2219 dòng`** | `da_gan 2219` | lượt cuối **2.219** | 8 |
| **8099** kho TEST `--cho-ghi` · mã mới *(ca `NAP-2000-01-01-T42403259`: `Chưa gán` 2 · `Đã gán` 1)* | ⓐ | **`1 dòng`** | `da_gan 1` | **1** | 2 |
| ″ | ⓑ | **`2 dòng`** | `chua_gan 2` | **2** | **2** |
| ″ | ⓒ | **`1 dòng`** | `da_gan 1` | lượt cuối **1** | 4 |

⚠ Lượt đầu 8099 trên kho TEST **sẵn có** ra `0 dòng` cả hai chip *(ảnh hiệu lực ⛔ có lệnh nào trong phạm vi)* ⇒ **⛔ đo được** *(Đ3)* — dựng ca `dung_ca_wo042` ＋ ghép lệnh `B` bằng **hàm cửa ghi thật** `ghep_lenh` *(kho TEST)* rồi đo lại. Kịch bản: `scratchpad/cdp_f3.mjs` *(⛔ lên git — xem *Cách chạy*)*.

## Kho thật
- **`KHONG_CHAM`** — mọi phép trên sổ thật là `SELECT` qua `noi_chi_doc` *(`AC-11`)* hoặc `GET` qua máy **8097 không `--cho-ghi`** *(`AC-5`/`AC-7`: **0** `POST`)*. Máy **8088** của phiên chính **⛔ đụng**. Ghi chỉ ở **kho TEST** *(`fls_test`)*: ca `WO-042` *(bài `AC-6`/`AC-10` + ca Chrome — mỗi lần 1 `fls_run`, 4 `fls_itl`, 4 `fls_pm_line`, ≤ 1 mối nối, `reason` mang `WO-042`)*.

## Cách chạy để xem
- Bài: `PYTHONUTF8=1 .venv/Scripts/python.exe -m pytest tests/web/test_wo042_doi_chip_khi_dang_tai.py tests/web/test_wo042_bon_chuoi_f01l_cua_that.py tests/web/test_wo042_mot_tap_ky_tu_trang.py tests/api/test_wo042_mot_tap_cua_that_pg.py` *(32 bài, ~10 s)*.
- Máy sổ thật **chỉ đọc**: `PG_DSN=postgresql://fls:fls@localhost:5433/fls FLS_JWT_SECRET=<≥32 ký tự> python tools/chay_cua.py --cho-web --cong 8097` *(⛔ `--cho-ghi`)*. Máy kho TEST: `PG_DSN=…/fls_test … --cho-web --cho-ghi --cong 8099`.
- Chrome: `node cdp_f3.mjs <cổng> <a|b|c|f01l> <cổng CDP>` — kịch bản ở scratchpad phiên này *(⛔ đưa vào `tools/`: nó là công cụ đo một lần; nếu `fls-test` muốn dùng lại, nội dung đủ ở mục `AC-5`: giữ `Fetch` `Request` stage theo mẫu URL, bấm bằng `Input.dispatchMouseEvent`, đếm `rows` qua `Network.getResponseBody`)*.
- Đối chứng mã khi nhận: `git worktree add <thư mục> 77737f7` rồi chạy `chay_cua.py` **từ thư mục ấy**.

## (d) Chỗ khác trên màn cùng lớp lỗi `F-3` *(đọc mã — ⛔ đo; ⛔ sửa ngoài `(a)`)*

Hàm trong `fls/web/tep/*.js` **`await` cửa rồi ghi trạng thái dùng chung** của màn *(`ST` / `S` / biến mô-đun / hộp)*:

| # | Tệp:dòng · hàm | Ghi gì sau `await` | Chống chồng? | Kịch bản hỏng *(nghi)* |
|---|---|---|:-:|---|
| 1 | `man_f01_ghep.js:913` `tai_danh_sach` | `ST.dong` · `dang_tai` · `loi` · `het` · `tro` | ✅ **có** *(`WO-042` — `_luot`)* | — |
| 2 | `man_f01_ghep.js:1013` `mo_lenh` | `ST.ung_vien` · `ST.toan_so` *(rồi `ve()`)* | ⛔ | đổi lệnh `j`/`k` / `↓` nhanh: ứng viên của lệnh **trước** về sau và đè lên lệnh đang mở *(`ST.mo` đã là lệnh mới)* — nút `Gán` đọc `ST.ung_vien[ST.ung_vien_chon]` |
| 3 | `man_f01_ghep.js:1039` `tai_toan_so` *(gọi từ ô tìm `:1140` + `mo_lenh`)* | `ST.ung_vien` | ⛔ *(chỉ trễ 250 ms `TRE_TIM` — chú thích `:129-132` tự nêu rủi ro "lượt về sau trả lời TRƯỚC")* | gõ, dừng >250 ms, gõ tiếp ⇒ hai lượt bay; lượt chữ **cũ** về sau thắng |
| 4 | `man_f01_ghep.js:653` `gan` *(GHI `/match`)* | `ST.xac_nhan` · `ST.ung_vien_chon` · `lenh_ke_tiep` | ⛔ *(nút ⛔ khoá trong lúc chờ)* | bấm `Enter` hai lần nhanh ⇒ hai `POST` — cửa ghi chặn lần hai *(`409`)*; thuộc `WO-023` *(mã `409`)* |
| 5 | `man_f01_ghep.js:693` `bo_gan` | `ST.dang_bo_gan` · `tin_bo_gan` · `loi_bo_gan` | ✅ có *(cờ `dang_bo_gan` khoá nút — `WO-008` v2)* | — |
| 6 | `man_f01_lenh.js:570` `ve_luoi` → `:497` `_ve_luoi` | `ST.dong = ST.dong.concat(...)` · `con_tro` · `het` | ⛔ | **cùng hình `F-3`**: `_loc` *(bấm `Xem <c> dòng` / `Quay lại` / `Bắt đầu tra`)* đặt `ST.dong = []` rồi tải; lượt rổ trước về sau **nối** vào mảng mới ⇒ lưới trộn hai rổ |
| 7 | `man_f01_lenh.js:544` nút `Xem thêm` | `_ve_luoi` *(concat)* | ⛔ *(nút ⛔ khoá trong lúc chờ)* | bấm hai lần ⇒ hai lượt **cùng** con trỏ ⇒ hàng lặp |
| 8 | `man_f01_lenh.js:641` `_drawer_tim_tien` | mở hộp `HT.mo` | ⛔ | bấm `Tìm tiền` hai dòng nhanh ⇒ hộp dòng **trước** có thể mở **sau** |
| 9 | `man_f01_lenh.js:744` nút `Ghép` trong hộp | `ST.vua_ghep` | ✅ *(hộp tự khoá hàng nút khi chờ — `hop_thoai.js`)* | — |
| 10 | `man_f01.js:206` `ve_luoi` → `:141` `_ve_luoi` | `ST.dong` · `ST.con_tro` | ⛔ | đổi lọc tiền tệ / `den_pct` khi lưới đang tải ⇒ lượt lọc cũ về sau thắng |
| 11 | `man_f01.js:192` `_xem_them` | `ST.dong` concat · `con_tro` | ⛔ | như #7 |
| 12 | `man_f01.js:284` `_drawer_ghep` | hộp `HT.mo` | ⛔ | như #8 |
| 13 | `man_f02.js:119` `_ve` *(qua `TT.chay` `:102`)* | `ST.dong` · `con_tro` · `theo_id` | ⛔ *(một nơi gọi — vẽ lại cả màn)* | thấp — chỉ khi `ve()` gọi chồng |
| 14 | `man_f02.js:369` nút `Xem thêm` | `ST.dong` concat · `theo_id` | ✅ có *(`b.disabled = true` khi chờ)* | — |
| 15 | `man_f02.js:1422` `mo_drawer` | thân panel + `_nho` | ✅ có *(`_dang_xem !== itl_id` — chú thích `:1470` "một cuộc đua đã có thật ở `F01`")* | — |
| 16 | `man_f02.js:938` `_ghi_mot_o` *(đọc trước khi GHI)* | `ST.theo_id` / `_lam_moi` | ⛔ *(chưa thấy khoá)* | hai ô ghi nhanh liên tiếp — chưa đo |
| 17 | `man_f04.js:299` `_mo_chup` | `S.chup` | ⛔ | mở hai ảnh chụp nhanh ⇒ `S.chup` của ảnh **trước** đè; `_soat`/`_nhan` gửi `S.chup.chup_id` |
| 18 | `man_f04.js:355` `_ve_thu_tu` | `S.thu_tu` | ⛔ | như #17 |
| 19 | `man_f04.js:598` `_soat` *(POST xem trước)* | `S.bien_ban` · `S.nguon_soat` | ⛔ | đổi tập nguồn rồi soát lại khi lượt trước chưa về |
| 20 | `man_f04.js:730` `_nhan` *(GHI `/nap/lo`)* | `S.da_nhan` | ⛔ *(chưa thấy khoá trong hàm)* | bấm `Nhận` hai lần — chưa đo |
| 21 | `man_f04.js:888` `ve` | `S.nguon` · `S.gap_trang_thai` | ⛔ | thấp — một nơi gọi |

Không vào bảng *(chỉ vẽ vào **khung riêng** qua `TT.chay`, ⛔ ghi `ST`)*: `man_f01.js:85` · `:709` · `man_f01_lenh.js:117` · `:286` · `:354` · `man_f03.js:71` · `:144` · `:232` · `man_f04.js:205` · `:241`. ⚠ `TT.chay` *(`trang_thai.js:88`)* tự nó ⛔ có mã lượt — hai lượt vào **cùng** khung thì lượt về **sau** thắng; vô hại khi đường ⛔ đổi tham số. Đề xuất cho `fls-ba`: **#6** là hình `F-3` y hệt trên màn `F01L` *(chung tab `② Hàng chờ`)*; **#2/#3** có thể làm `Gán` ghi đúng cặp mà **màn** đang hiện sai ứng viên.

## Phát hiện ngoài phạm vi *(⛔ sửa — `fls-ba` phát phiếu nếu cần)*
- **`Xem thêm` của lưới `F01L` bị khoá ở máy chỉ đọc** — `man_f01_lenh.js:544` dựng bằng `_nut` ⇒ `_chan_ghi` *(`:61`)* khoá mọi nút qua `_nut` khi `cho_ghi = false`, kể cả thao tác **đọc**. Đo 8097 *(sổ thật, chỉ đọc)*: `{co: true, disabled: true, title: "⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC. Mọi thao tác ghi bị trả 405…"}` ⇒ rổ `may` chưa nhận theo lô *(120)* chỉ xem được **50** dòng đầu trên máy 8088. Có từ trước `WO-042`.

## Dev tự thấy còn yếu
1. **Ba bài `kq041` ⛔ `XPASS`** — `AC-1`/`AC-2`/`AC-8`/`AC-12` nguyên văn *(`--runxfail … ⇒ passed`, "đúng 3 `XPASS(strict)`")* **⛔ đạt**. Dev tin đó là lỗi **gác của bài**, ⛔ của mã *(bằng chứng bản sao trong `AC-12`)* — nhưng đó là phán đoán của bên bị kiểm; `HOI-043` để `fls-ba`/`fls-test` quyết.
2. **Lượt bị thay dừng ngay** *(⛔ xin cửa kế)* là **lựa chọn** của Dev, spec ⛔ đòi. Nếu `fls-ba` muốn lượt cũ chạy hết *(để khớp gác `goi >= 3`)* thì đó là một dòng; Dev ⛔ làm vì nó tốn một `GET` thật ~0,9 s cho kết quả bị vứt.
3. `ST.dong = []` vẫn đặt **ngay** khi lượt mới bắt đầu *(như cũ)* — trong lúc tải, màn chỉ vẽ *"Đang hỏi sổ…"* nên ⛔ thấy; nhưng **phím** `↑↓`/`Enter` đọc `ST.dong` lúc đang tải ⇒ ⛔ làm gì *(như cũ)*. ⛔ đo bằng phím thật.
4. **Chrome chạy headless** — `Input.dispatchMouseEvent` là sự kiện chuột ở tầng trình duyệt *(qua hit-test thật)*, nhưng ⛔ phải cửa sổ hiện hình. Lượt `KQ-041` dùng Chrome có giao diện; số khớp **2955 / 1472** nên tin là cùng đường — chưa chứng minh trên cửa sổ hiện hình.
5. **`AC-7` "số hàng lưới = c"** trên sổ thật chỉ đo được **trang đầu 50** *(nút `Xem thêm` bị khoá ở máy chỉ đọc — phát hiện ngoài phạm vi)*; tổng **120** lấy từ thân cửa mọi trang, ⛔ từ lưới.
6. `TP.TAP_TRANG_TIEN_TE` là **bản chép** — đồng nhất với Python chỉ được giữ bởi bài `test_AC8_JS_*`. Một cách cứng hơn *(sinh JS từ Python như `cot.js`)* ⛔ làm vì `WO` khai `JS khai một hàm` và nó đổi `chay_cua.py`.
7. Kho TEST: mỗi lượt bài `AC-6`/`AC-10` thêm **1 `fls_run` + 4 + 4 dòng** *(⛔ dọn — cùng luật `ca_wo032`/`ca_wo037`)* — đóng góp vào `fls-test-store-grows-unbounded`.
8. Công cụ soạn tệp của phiên đã **dịch** chuỗi thoát `\u…` thành ký tự **vô hình thật** trong nguồn hai lần trong lượt này *(hằng `TAP_TRANG_TIEN_TE`, chú thích `ghi_tay`/`do_mau_so`/`doc_bao_cao`)* — đã gỡ, và kiểm `grep` các byte `EF BB BF` / `C2 A0` / `E2 80 8x` / `E3 80 80` trong `fls/` + tệp bài mới ⇒ **0**. Chỗ chưa quét: các tệp `docs/` của lượt này.
