# KQ-130 — biên bản kiểm `BG-128` *(ISP 3.1.2 · Step 5 · DT1b tiếp · vòng **R2** — chỉ thay đổi kể từ R1)*

| | |
|---|---|
| **Thuộc** | `BG-128` *(mục "Vòng sửa sau R1 (KQ-129)")* · `WO-127` |
| **Kiểm bởi** | `fls-test` *(R2, phiên cloud con, độc lập — vai KIỂM, ⛔ sửa mã hệ thống)* · 2026-11-18 · orchestrator giao |
| **Phạm vi** | `git diff 5f5d3b4 isp/DT1BT` — **7** tệp *(`tools/xuat_khoa_dt1b.py` +77 · `tests/du_lieu/test_xuat_khoa_dt1b.py` +254 · `HUONG_DAN_NHAN_THAT_DT1b.md` v1.1 · `.gitignore` +5 · sàn `3081→3105` ở `tools/dung_moi_truong_isp.sh` + bài ghim · `BG-128`)*. Ngọn `isp/DT1BT` = `8055222` *(đúng mong)* |
| **Cụm** | cổng **5447** do `dung_moi_truong_isp.sh --cong 5447` dựng — `KẾT: ĐẠT` *(7/7 phép kiểm)* |
| **Phán quyết** | **`ĐẠT`** R2 — **0 CHẶN · 3 NÊN SỬA** *(`DT1BT-R2-01` · `-04` · `-05` — cả ba ở **hướng dẫn owner**)* · **3 GHI NHẬN** *(`-02` · `-03` · `-06`)*. **9/9** phát hiện R1: **6 đóng hẳn** *(`-01` · `-02` · `-03` · `-05` · `-08` · `-09`)* · **3 đóng một phần/chờ** *(`-04` · `-06` · `-07`)*. Khuyến nghị: **một vòng sửa nhỏ chỉ chạm hướng dẫn** *(3 NÊN SỬA là chữ, ⛔ mã)* trước khi owner chạy thật |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1BT.md` *(v0.2: đổi ô Trạng thái 9 hàng R1 · thêm 6 hàng `DT1BT-R2-01…06`)* |

## Cổng chạy lại *(Test tự chạy — so với `BG-128` §Vòng sửa)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_xuat_khoa_dt1b.py` | `38 passed` | `38 passed in 1.62s` | ✅ |
| `pytest tests/du_lieu` | — | `340 passed in 26.21s` | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5447` *(chạy MỘT MÌNH)* — toàn bộ | `12 failed, 3077 passed, 2 xfailed, 14 errors` · **28 = 28** · chạy 3105 | `12 failed, 3077 passed, 2 xfailed, 1 warning, 14 errors in 370.03s` · **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **3105** *(mong ≥ 3105)* · skipped 0 · deselected 0 | ✅ |
| …web | `3 failed, 664 passed` · **3 = 3** · 667 | `3 failed, 664 passed in 177.52s` · **3 = 3** · chạy **667** · skipped 0 · deselected 0 | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` *(cả trong `--duong-nen`)* | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `245 file, 2291 bảng` | `✅ DAT — 246 file, 2303 bảng, 779 ô ngày, 104 mã QĐ` *(đo lại SAU khi thêm phiếu này; +12 bảng so `BG` = sổ+phiếu R1/R2; sau khi thêm sổ v0.2 lần đầu **ĐỎ K1** "header v0.1 < changelog v0.2" ⇒ bump header ⇒ XANH)* | ✅ |
| `kiem_so_song` · `khop_owner` · `soi_bang_tuyen` · `kiem_thuyet_minh` | `CHƯA CHẠY` | ⛔ chạy — đồng ý: `git diff --stat 5f5d3b4` ⇒ 0 tệp trong `fls/` · schema · web | — |

## Trạng thái 9 phát hiện R1 *(đo lại, ⛔ tin lời `BG`)*
| Mã | `BG` nói | R2 đo | Trạng thái |
|---|---|---|---|
| `-01` rels tuyệt đối | đã sửa | `_chuan_dich_rels("/xl/worksheets/sheet1.xml")` ⇒ `xl/worksheets/sheet1.xml` ✓ · tương đối ⇒ nối `xl/` ✓ · **đột biến N1** *(luôn nối `xl/`)* ⇒ bị bắt. **Nhưng** dạng ngoài hai loại ấy: `xl/worksheets/…` *(bản cũ đọc được ⇒ hồi quy)* · `../` · `./` · `%20` ⇒ 4/8 chuỗi thử ra đường không tồn tại ⇒ `LoiDoc` một dòng | **đóng** · mở `R2-02` *(GHI NHẬN)* |
| `-02` hàng dữ liệu | A: giữ + in số đếm | dòng in `hàng có ≥1 ô khoá / hàng 0 ô khoá — SO: a / b · L1: c / d` ✓ *(chạy thật: `SO: 3 / 0 · L1: 1 / 0`)*; giá trị ô ∉ màn ✓; **đột biến N2** *(bỏ in)* · **N7** *(đảo cặp)* · **N14** *(in `hang[0]`)* ⇒ cả ba bị bắt. Hướng dẫn (c)(d) có nhánh *"K11 lệch mà 0 khoá > 0 ⇒ dừng, báo hai số"* ✓ *(đúng quyết A)* | **đóng** *(⛔ đo được trên tệp thật — O10)* |
| `-03` quét đường lỗi | 7 ca | `test_DT1BT_R1_03_…` 7 ca xanh; **tái đột biến M6 = N6** *(câu "thiếu tiêu đề" nối hàng dữ liệu)* · **M14 = N8** *(`except LoiDoc` in `__context__`)* ⇒ **bị bắt** | **đóng** |
| `-04` Traceback | 8 ca | 8/8 ca một dòng `LOI…`, exit 1, ⛔ Traceback; **N3** *(`_parse_xml` để `ParseError` tràn)* · **N4** *(bỏ chốt NUL)* · **N5** *(in `e` của `UnicodeDecodeError`)* · **N16** · **N17** ⇒ bị bắt. **Hở:** lật 8 byte luồng nén của sheet ⇒ `zlib.error` ⇒ **Traceback** *(0 giá trị ô trên màn)* | **đóng một phần** · mở `R2-03` |
| `-05` ghim M8/M12/M16 | đã ghim | **N10a** *(`max→min` ngoài)* · **N10b** *(chỉ tiêu đề đầu)* · **N12** · **N11** ⇒ bị bắt | **đóng** |
| `-06` `-LiteralPath` | 13 chỗ | **13 dòng** có `-LiteralPath` *(= số tác giả khai; `grep -c`)* · **16 lần** xuất hiện *(`grep -o`)*; lệnh chạm `[`/`]` — `Test-Path`/`Resolve-Path` bước (0), `Move-Item`/`Remove-Item` (b)(g) — đều dùng. ⛔ đo hành vi — không `pwsh` | **đóng ở văn bản** · hướng dẫn **chưa nói** "chưa thử" ⇒ `R2-01` |
| `-07` `Move-Item` + dọn | đã làm | `Move-Item` ✓ · (g) là lệnh ✓ + khung "mọi nhánh" ✓; **hở:** (g) không `cd` ⇒ đổi cửa sổ thì kiểm xanh giả `R2-04` | **đóng một phần** |
| `-08` bỏ `⛔` | 0 | `grep -c ⛔ HUONG_DAN…` = **0** ✓; hàng (e) khớp dòng **Mong** ✓ | **đóng** |
| `-09` `Input_Raw` | `.gitignore` | `git check-ignore -v Input_Raw/x.xlsx` ⇒ `.gitignore:23:Input_Raw/` ✓ *(cả `Input_Raw/[Master] ITL_Ledge_raw.xlsx`)*; **N9** *(gỡ dòng)* ⇒ bị bắt; hướng dẫn (0) nói trong/ngoài repo ✓. Chữ cổng (f) ⇒ `R2-05` | **đóng** |

## Đột biến *(bản sao `git archive isp/DT1BT`; `tests/du_lieu/test_xuat_khoa_dt1b.py`; 20 chỗ + 1 đo nền)*
Nền không đột biến trên bản sao: `38 passed`. Dọn bản sao giữa **mỗi** lượt *(bài học R1: tệp rác của lượt trước làm đỏ giả)*.

| # | Đột biến | Phủ | Kết quả |
|---|---|---|---|
| N1 | `_chuan_dich_rels` luôn nối `xl/` | R1-01 | **bị bắt** |
| N2 | bỏ dòng in số đếm hàng-khoá | R1-02 | **bị bắt** |
| N3 | `_parse_xml` để `ParseError` tràn | R1-04 | **bị bắt** |
| N4 | bỏ chốt NUL của L1 | R1-03/04 | **bị bắt** |
| N5 | `UnicodeDecodeError` in `e` | R1-04 | **bị bắt** |
| N6 | **M6** — câu "thiếu tiêu đề" nối hàng dữ liệu | R1-03 | **bị bắt** |
| N7 | `_dem_khoa` đảo cặp | R1-02 | **bị bắt** |
| N8 | **M14** — `except LoiDoc` in `__context__` | R1-03 | **bị bắt** |
| N9 | gỡ `Input_Raw/` khỏi `.gitignore` | R1-09 | **bị bắt** |
| N10 | `max→min` **bên trong** từng tiêu đề | — | **sống** — *tương đương*: mỗi tiêu đề chỉ có 1 vị trí ⇒ `min = max` *(⛔ lỗ hổng bài)* |
| N10a | **M8 gốc** `max→min` ngoài | R1-05 | **bị bắt** |
| N10b | `hang_tieu_de or …` *(chỉ tiêu đề đầu)* | R1-05 | **bị bắt** |
| N11 | **M16** bỏ `.strip()` tiêu đề L1 | R1-05 | **bị bắt** |
| N12 | **M12** bỏ chốt "đường ra là thư mục" | R1-05 | **bị bắt** |
| N13 | tắt R8 *(M2)* | AC-3 | **bị bắt** |
| N14 | `_dem_khoa` in `hang[0]` | R1-02 / riêng tư | **bị bắt** |
| N15 | bỏ `tgt.strip()` ở rels | R1-01 | **sống** — vô hại *(chỉ khác khi `Target` có khoảng trắng; ⛔ tìm thấy ở tệp thật nào)* |
| N16 | bỏ bắt `UnicodeDecodeError` | R1-04 | **bị bắt** |
| N17 | bỏ bắt `csv.Error` | R1-04 | **bị bắt** |
| N18 | `tools/dung_moi_truong_isp.sh` `MONG_PYTEST_TOAN_BO` `3105→3104` | AC-6 | **bị bắt** *(`tests/test_dung_moi_truong_isp.py::test_S0_R2_03_…`, chạy riêng một bài)* |

**18/20 bị bắt · 2 sống** *(N10 tương đương ⇒ ⛔ phát hiện; N15 vô hại ⇒ ⛔ phát hiện)*. Nháp: `scratchpad/mut.py` *(⛔ commit)*.

## Thử phá *(đường lỗi · bọc có nuốt lỗi? · rò byte?)*
| Câu hỏi | Đo | Kết luận |
|---|---|---|
| Bọc mới có **nuốt** lỗi thật *(exit 0 khi hỏng)*? | `_CA_HONG` 8 ca + `_CA_RORI` 7 ca *(bài xanh: `returncode == 1`/`≠ 0`, `k.csv` ⛔ tạo)* + **3 ca tự thêm** ở scratchpad *(`.xlsx` rỗng · CSV rỗng · `zlib`)* ⇒ **exit 1** cả 3 *(zlib kèm Traceback)* | ⛔ nuốt |
| In byte/giá trị? | sentinel nhúng vào tệp hỏng ∈ stdout+stderr: **0/7** *(bài `R1_03`)* + **0/1** *(ca `zlib` tự thêm)*; `0x`/`position`/`byte` ∉ câu lỗi `UnicodeDecodeError` | sạch |
| Còn Traceback? | **1** loại: `zlib.error` *(luồng nén bị lật)* — `R2-03` | hở nhẹ |
| `_chuan_dich_rels` với `../` · `./` · `%20` · `xl/…` | 4/8 ra đường không tồn tại ⇒ `LoiDoc` một dòng ⇒ exit 1 | `R2-02` |
| Chạy thật mặc định *(xlsx tuyệt-đối-rels tên `[Master] …xlsx` + L1)* | exit 0 · `SO 3 hàng · L1 1 hàng` · số đếm `3 / 0 · 1 / 0` · `git status` ⇒ **rỗng** *(`hien_vat/` ignore `:17`)*; **đường in tuyệt đối** *(ví dụ **Mong** trong hướng dẫn in tương đối ⇒ `R2-06`)* | đúng |

## Bảng AC *(chỉ AC chịu ảnh hưởng của vòng sửa)*
| AC | Mong | Đo được | Phán quyết |
|---|---|---|---|
| AC-1 | xlsx ⇒ CSV 7 cột đúng từng ô | 38 bài xanh · rels tuyệt đối đọc được *(R1-01)* | **ĐẠT** |
| AC-3 | 0 giá trị ô trên màn *(cả đường lỗi)* · ra `hien_vat/` · từ chối đường trong repo ⛔ ignore | đường lỗi **0/7 sentinel** *(+0/1 ca `zlib`)*; M6/M14 bị bắt; R8 bị bắt | **ĐẠT** |
| AC-5 | hướng dẫn chép-dán được; có bước dọn | 7 bước + (0) có lệnh, **Mong**, bảng "Nếu thấy"; `-LiteralPath` đúng chỗ; ⛔ `⛔`. **3 NÊN SỬA** *(chữ)*: `R2-01` · `-04` · `-05` | **ĐẠT** *(NÊN SỬA kèm 3 hàng)* |
| AC-6 (Q8) | sàn `3081 → 3105` cùng commit | `grep MONG_PYTEST_TOAN_BO` = **3105** · bài ghim `== ["3105"]` · `--duong-nen` chạy **3105** · web 667 ⛔ đổi · `git show --stat 613ff49` chứa cả `.sh` + bài ghim | **ĐẠT** |

## Đánh giá hướng dẫn owner v1.1 *(đọc như người ⛔ lập trình viên · Windows PowerShell — ⚠ container ⛔ có `pwsh`: hành vi PowerShell là **kiến thức, ⛔ đo**)*
| Bước | Chép-dán được? | Mong rõ? | "Nếu thấy"? | Riêng tư | Ghi chú |
|---|:-:|:-:|:-:|:-:|---|
| Chuẩn bị `cd` · `$env:PYTHONUTF8` | ✅ | ✅ | — | ✅ | `cd` duy nhất ở `:33` *(liên quan `R2-04`)* |
| **(0)** `Test-Path -LiteralPath` · `Resolve-Path` | ✅ | ✅ | ✅ *(3 hàng: False · trong repo ⛔ `Input_Raw\` · ngoài repo)* | ✅ | ⛔ **không nói "chưa thử trên Windows, owner xác nhận trước"** — **`R2-01`** *(đúng quyết A của orchestrator)* |
| (a) `git fetch/checkout/pull` · `Test-Path tools\…` | ✅ | ✅ | ✅ | ✅ | giả định **A** *(owner chạy sau gộp)* — câu A/B của `BG-128` vẫn mở ở orchestrator |
| (b) tải CSV · `Move-Item -LiteralPath (Get-ChildItem …).FullName` | ✅ | ✅ | ✅ | ✅ *(⛔ còn bản ở Downloads)* | pattern `*Transaction Mapping L1*.csv` khớp tên Google `[Master] … - Transaction Mapping L1.csv` ✓ *(`[ ]` trong **tên**, ⛔ trong pattern)*; `-Force` ⛔ có ⇒ `R2-06` |
| (c) `xuat_khoa_dt1b.py --xlsx $XLSX …` | ✅ | ⚠ *(ví dụ in đường tương đối; thật in tuyệt đối — `R2-06`)* | ✅ *(6 hàng)* ⛔ hàng cho `zlib` hỏng ⇒ Traceback `R2-03` | ✅ | số đếm `SO / 0 khoá` có và đúng |
| (d) `phan_loai_ly_do.py --khoa …` | ✅ | ✅ | ✅ *(2 hàng K11 tách theo "0 khoá" > 0 — đúng quyết A)* | ✅ | trích *"≠ 9.967"* — mã in `9967` ⇒ `R2-06` |
| (e) `--ghi` ở mã 4 | ✅ | ✅ | ✅ *(hàng khớp dòng **Mong**)* | ✅ | `phan_loai_ly_do.py:716` `if ghi and ma in (DAT, CHUA_GHIM)` ✓ |
| (f) `git status` · `git add <MỘT tệp>` · commit · push | ✅ | ✅ | ⛔ **`R2-05`**: cổng viết *"Changes to be committed"* ⇒ **không bao giờ** có trước `add` | ✅ *(`git add <một tệp>`, ⛔ `-A`)* | `git status` thật ⇒ ⛔ liệt kê `hien_vat`/`Input_Raw` *(ignore `:17`/`:23`)* ✓; `phan_loai_ly_do.json` hôm nay ⛔ có trong cây ⇒ hiện `??` — "chỉ MỘT tệp" vẫn đúng |
| (g) dọn | ✅ | ✅ | — | ⛔ **`R2-04`**: đường tương đối, ⛔ `cd` ⇒ xanh giả khi đổi cửa sổ | 3 chỗ dọn + 3 dòng kiểm ✓; `Remove-Item` xoá thẳng ✓ |
| Báo kết quả | ✅ | ✅ | — | ✅ | chỉ mã thoát + bảng đếm |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | đúng spec; 1 hồi quy biên + 1 lớp Traceback còn hở | `R2-02` · `R2-03` |
| **Dữ liệu** | ⛔ đo được — công cụ ⛔ chạm kho; nền `fls_itl = 0 dòng` | tệp thật `[Master] ITL_Ledge_raw.xlsx` chỉ có máy owner *(O10)*; hai rủi ro còn *(nhà sinh xlsx · "hàng 0 khoá" thật)* nay có **chẩn đoán in số** |
| **Riêng tư** *(rủi ro số 1)* | **0/8 sentinel** ở đường lỗi; số đếm ⛔ giá trị; `Input_Raw/` ignore thật. Hai chỗ **hướng dẫn** hở: dọn thô `R2-04` · cổng git `R2-05` | N6 · N8 · N14 · N9 bị bắt |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `DT1BT-R2-01` | `NANG` | `HUONG_DAN_NHAN_THAT_DT1b.md` đầu · (0) · (g) | `grep` 3 khớp "xác nhận/Windows/…", 0 là lời dặn owner-tự-xác-nhận (0)+(g) | `DEV` |
| `DT1BT-R2-02` | `NHE` | `tools/xuat_khoa_dt1b.py:117-125` | `Target="xl/worksheets/…"` ⇒ `xl/xl/…` *(cũ đọc được)*; `../` · `./` · `%20` ⇒ `LoiDoc` | `DEV` |
| `DT1BT-R2-03` | `NHE` | `doc_xlsx_ledge` | lật 8 byte luồng nén sheet ⇒ `zlib.error` ⇒ Traceback | `DEV` |
| `DT1BT-R2-04` | `NANG` | hướng dẫn (g) | cửa sổ mới ⇒ `Test-Path hien_vat\…` False/False/0 trên thư mục sai; tệp thật còn | `DEV` |
| `DT1BT-R2-05` | `NANG` | hướng dẫn (f) `:199` `:209-210` | cổng chữ "Changes to be committed" trước `add` ⇒ không bao giờ khớp | `DEV` |
| `DT1BT-R2-06` | `NHE` | hướng dẫn `:97` `:123` `:161` | ví dụ **Mong** in tương đối vs thật tuyệt đối · "9.967" vs `9967` · `Move-Item` ⛔ `-Force` | `DEV` |

## Bài thử mới
⛔ commit *(lệnh giao R2: chỉ phiếu + sổ)*. Đề xuất cho Dev: ca `zlib_hong` vào `_CA_HONG`/`_CA_RORI` *(⛔ `adv.py` ở scratchpad dựng sẵn bằng lật byte)* · 3 ca `_chuan_dich_rels` *(`xl/…` · `../` · `%20`)* · ca quét `N10` *(hai tiêu đề cùng tên ở 2 hàng ⇒ `thay` > 1 vị trí)*.

## Đối chiếu luật `Đ1…Đ5`
- **Đ1** *(phủ định)*: *"hướng dẫn ⛔ nói chưa thử trên Windows"* — `grep -n -i "xác nhận\|chưa đo\|chưa kiểm\|thử trước\|trên Windows\|container\|Linux"` ở hướng dẫn ⇒ **3** khớp, **0** là lời dặn *(⛔ viết "không có" mà chưa grep)*; "⛔ còn `⛔`": `grep -c` = **0**. *"Input_Raw ⛔ ignore"* **đã đảo**: `grep -n Input_Raw .gitignore` ⇒ **2** dòng *(`:22` chú thích · `:23` luật)*, `git check-ignore -v` ⇒ `:23`.
- **Đ2**: so **hai nguồn** — hướng dẫn ↔ mã: `Mong` (c) *(tương đối)* ↔ thật in *(tuyệt đối)* ⇒ lệch `R2-06`; "≠ 9.967" ↔ `phan_loai_ly_do.py:373` `{len}` ⇒ lệch. Câu đúng *đã* có ở (e) *(`:716`)*.
- **Đ3** *(tập rỗng)*: (g) `False/False/0` xanh trên **thư mục sai** = chính xác bẫy Đ3 ⇒ `R2-04`. Bài đột biến: mọi đột biến chạy trên nền `38 passed` *(mẫu số 38 > 0)*; N10/N15 sống **được giải thích**, ⛔ bỏ qua.
- **Đ4**: `3105` = thu thập `--duong-nen` ✓; `13` *(tác giả khai)* = số **dòng** chứa `-LiteralPath` ✓ *(đo `grep -c`)*, `16` = số **lần xuất hiện** *(`grep -o`; vài dòng có 2–3 lệnh)* — ⛔ lệch, chỉ khác nhãn *(thiếu chữ "dòng" ở `BG-128`)*.
- **Đ5**: bài ghim `== ["3105"]` ĐỎ khi sai *(R2 tự đo: **N18** đổi `.sh` `3105→3104` ⇒ `test_S0_R2_03_…` **FAILED**)*; công cụ in số đếm nhưng ⛔ tự dừng khi "0 khoá" > 0 *(quyết A ⇒ chờ số thật)*.

## Câu hỏi cho orchestrator *(kèm khuyến nghị)*
1. **Vòng sửa hướng dẫn trước khi owner chạy?** *(`R2-01` · `-04` · `-05` đều là chữ, không đụng mã)*. **Khuyến nghị A:** một vòng `fls-dev` ngắn chỉ sửa `HUONG_DAN…` — thêm khung "bước (0)/(g) chưa thử trên Windows" + `cd` ở (g) + sửa chữ cổng (f); kèm sửa `R2-06` cùng lúc. **B:** gộp luôn không sửa, owner tự chịu.
2. **`R2-02` + `R2-03`** *(mã, GHI NHẬN)*: làm trong cùng vòng *(A, ~10 dòng + 4 bài, hỏng-đóng nên không gấp)* hay để sau số thật *(B)*? **Khuyến nghị A** — rẻ, và `R2-03` là lớp lỗi lặp của `R1-04`.
3. **A/B của `BG-128` (checkout nhánh làm việc vs `…-isp/DT1BT`)** còn mở từ R1. **Khuyến nghị A** *(đã viết)*: owner chạy sau khi gộp.

## Commit
Chỉ phiếu `KQ-130` + sổ `SO_PHAT_HIEN_ISP-3.1_DT1BT.md` v0.2 *(đổi ô Trạng thái 9 hàng · thêm 6 hàng · changelog · bump header theo K1)*.
