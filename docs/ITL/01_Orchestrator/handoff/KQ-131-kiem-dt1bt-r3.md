# KQ-131 — biên bản kiểm `BG-128` *(ISP 3.1.2 · Step 5 · DT1b tiếp · vòng **R3 — cuối**, trước khi owner chạy dữ liệu THẬT)*

| | |
|---|---|
| **Thuộc** | `BG-128` *(mục "Vòng sửa sau R2 (KQ-130)")* · `WO-127` |
| **Kiểm bởi** | `fls-test` *(R3, phiên cloud con, độc lập — vai KIỂM, ⛔ sửa mã hệ thống)* · 2026-11-18 · orchestrator giao |
| **Phạm vi** | `git diff 29db42b isp/DT1BT` — **6** tệp *(`tools/xuat_khoa_dt1b.py` +44/−… · `tests/du_lieu/test_xuat_khoa_dt1b.py` +100 · `HUONG_DAN_NHAN_THAT_DT1b.md` v1.2 · sàn `3105→3112` ở `tools/dung_moi_truong_isp.sh` + bài ghim · `BG-128`)* + KIỂM TOÀN CỤC cây gộp thử. Ngọn `isp/DT1BT` = `c198f48` *(đúng mong)* |
| **Cụm** | cổng **5447** do `dung_moi_truong_isp.sh --cong 5447` dựng — `KẾT: ĐẠT` *(7/7 phép kiểm)* |
| **Phán quyết** | **`ĐẠT`** R3 — **0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** *(`R3-01` · `-02` · `-03`)*. **15/15** phát hiện R1+R2 cũ: **đóng hết** *(R1-06 đóng ở văn bản — hành vi PowerShell ⛔ đo được ở container)*. **Đủ điều kiện GỘP** *(0 CHẶN · 0 NÊN SỬA mở)*. **Hướng dẫn v1.2 đủ để owner chạy**, với điều kiện owner làm đúng khung ⚠ *(chạy thử (0)/(g) trước)* |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1BT.md` *(v0.3: đổi ô Trạng thái 9 hàng · thêm 3 hàng `DT1BT-R3-01…03`)* |

## Cổng chạy lại *(Test tự chạy — so với `BG-128` §Vòng sửa sau R2)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `dung_moi_truong_isp.sh --duong-nen --cong 5447` *(chạy MỘT MÌNH)* — toàn bộ | sàn **3112** | `12 failed, 3084 passed, 2 xfailed, 1 warning, 14 errors in 393.16s` · **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **3112** *(mong ≥ 3112)* · skipped 0 · deselected 0 | ✅ |
| …web | 667 | `3 failed, 664 passed in 183.02s` · **3 = 3** · chạy **667** · skipped 0 · deselected 0 | ✅ |
| `lint-imports` · `pg_verify` · HD1 | — | `11 kept, 0 broken` · `26/26 di trú, 25 bảng/view, 0 lệch` · `chay 9845 / co 9967` | ✅ |
| `pytest tests/du_lieu/test_xuat_khoa_dt1b.py` *(bản sao `git archive` + `git init`)* | `45 passed` | `45 passed` | ✅ |
| `kiem_so_song` · `khop_owner` · `soi_bang_tuyen` · `kiem_thuyet_minh` | `CHƯA CHẠY` | ⛔ chạy — đồng ý: `git diff --stat 29db42b` ⇒ 0 tệp trong `fls/` · schema · web | — |

## Thử phá mã *(vùng R2-02 · R2-03; ⛔ nuốt lỗi · ⛔ Traceback · ⛔ byte)*
**`_chuan_dich_rels` — 14 dạng `Target`** *(xlsx tổng hợp có sheet `ITL Ledge` ở `xl/worksheets/sheet2.xml`; chạy công cụ thật)*:

| Target | Kết quả | |
|---|---|:-:|
| `/xl/worksheets/sheet2.xml` · `xl/worksheets/sheet2.xml` · `worksheets/sheet2.xml` · `./worksheets/sheet2.xml` · `//xl//worksheets/./sheet2.xml` | exit 0, xuất đủ | ✅ *(5/5)* |
| `../worksheets/sheet2.xml` *(theo OPC ⇒ `worksheets/…` ngoài `xl/`)* · `worksheets/sheet%322.xml` *(unquote ⇒ `sheet22`)* · `""` · `xl` · `worksheets\sheet2.xml` · `worksheets/%00x` | exit 1, **một dòng** `LOI đọc: xlsx ⛔ có tệp worksheet '…'` | ✅ *(6/6; `\` ⇒ `R3-01`)* |
| `../../etc/passwd` · `/../../etc/passwd` · `%2e%2e/%2e%2e/etc` | exit 1, một dòng `rels: đích … thoát khỏi gốc gói` | ✅ *(3/3)* |

**Luồng nén** — lật {1 · 8 · 64} byte giữa luồng của 4 phần (`workbook.xml` · `workbook.xml.rels` · `sharedStrings.xml` · `worksheets/sheet2.xml`) ⇒ **12/12**: exit 1 · đúng **1** dòng `LOI đọc: <phần>: luồng nén hỏng` · ⛔ Traceback · sentinel ∉ stdout+stderr. **CRC-32 thật** *(`ZIP_STORED`, lật 1 byte nội dung sheet2, CRC giữ nguyên ⇒ `BadZipFile 'Bad CRC-32'`)*: exit 1 · 1 dòng · ⛔ Traceback · sentinel ∉ màn. ⛔ ca nào exit 0 khi tệp hỏng *(nuốt lỗi)*: **0/16**.
⚠ Đ3 *(tập rỗng)*: lần đo CRC đầu **exit 0** vì lật nhầm `<sheetData>` của sheet **decoy** `Bìa` *(đọc không tới)* — đổi sang lần xuất hiện CUỐI *(sheet2)* mới ra exit 1; mẫu số 16 ca đều đã xác nhận có tệp hỏng thật *(tên phần ∈ câu lỗi)*.

## Đột biến *(bản sao `git archive isp/DT1BT` + `git init`; nền `45 passed`; dọn bản sao mỗi lượt)*
⚠ Lần đầu **11/11 đỏ giả**: `git archive` ⛔ mang `.git` ⇒ 3 bài `AC3_*`/`R1_09` *(gọi `git check-ignore`)* đỏ ở NỀN — đo nền trước ⇒ thêm `git init`. *(Bài học R1 lặp: đo nền trước khi tin "bị bắt".)*

| # | Đột biến | Phủ | Kết quả |
|---|---|---|---|
| M1 | bỏ `unquote` | R2-02 | **bị bắt** *(`R2_02_chuan_dich_rels_dang_ngoai`)* |
| M2 | bỏ nhánh `xl/` sẵn | R2-02 | **bị bắt** *(đơn vị + `xl_tien_to`)* |
| M3 | bỏ `normpath` | R2-02 | **bị bắt** *(đơn vị + `cham`/`cham_cham`)* |
| M4 | bỏ chặn thoát gốc *(`if False`)* | R2-02 | **sống — tương đương hành vi** *(`../etc` ⇒ `KeyError` ⇒ `LoiDoc` một dòng; chỉ khác câu chữ)* ⇒ `R3-02` |
| M5 | chặn thu hẹp *(`startswith("../x")`)* | R2-02 | **sống — tương đương hành vi** ⇒ `R3-02` |
| M6 | `_doc_phan_zip` bỏ `zlib.error` | R2-03 | **bị bắt** *(`R1_04[zlib_hong]` · `R2_03`)* |
| M7 | `_doc_phan_zip` bỏ `BadZipFile` | R2-03 | **sống — ⛔ tương đương**: CRC-32 hỏng ⇒ `BadZipFile` tràn ⇒ Traceback; ⛔ bài lật CRC ⇒ `R3-02` |
| M8 | sheet đọc `z.read` trần | R2-03 | **bị bắt** |
| M9 | `sharedStrings` đọc `z.read` trần | R2-03 | **sống — ⛔ tương đương**: ca `zlib_hong` chỉ lật sheet ⇒ `R3-02` |
| M10 | `workbook.xml.rels` đọc `z.read` trần | R2-03 | **sống — ⛔ tương đương** ⇒ `R3-02` |
| M11 | câu lỗi `_doc_phan_zip` nối `z.read(ten)[:5]` *(rò byte)* | AC-3 | **bị bắt** *(sentinel ∈ màn)* |

**6/11 bị bắt · 5 sống** *(2 tương đương hành vi · 3 là lỗ hổng bài — chỉ GHI NHẬN vì mã hiện tại ĐÚNG đo trực tiếp 16/16)*. Nháp: `scratchpad/mut.py` *(⛔ commit)*.

## Cây gộp thử *(`/tmp/r3_dt1bt/gop`; `origin/moi/lam_viec` @ `eab6a21` + `merge --no-ff --no-commit isp/DT1BT`; ⛔ commit/push)*
| Mục | Đo |
|---|---|
| **Xung đột** | **2** tệp, đúng dự kiến: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(`CONFLICT (content)`; 0 tệp khác)* ⇒ `checkout --ours` *(giữ nhánh làm việc)*; sàn nhánh làm việc `3141` |
| **Sàn mới** | `pytest --collect-only -q -o addopts=""` trên cây gộp = **3186** *(= `3141` + **45** bài `test_xuat_khoa_dt1b.py`; web `667` ⛔ đổi)* ⇒ `MONG_PYTEST_TOAN_BO=3186` + bài ghim `== ["3186"]` *(chỉ cây gộp, ⛔ commit)* |
| **`--duong-nen --cong 5447`** *(chạy MỘT MÌNH)* | toàn bộ `12 failed, 3158 passed, 2 xfailed, 14 errors in 398.41s` · **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **3186** *(mong ≥ 3186)* · skipped 0 · deselected 0 · web `3 failed, 664 passed` · **3 = 3** · chạy 667 |
| **`lint-imports`** | `Contracts: 11 kept, 0 broken.` |
| **`kiem_tai_lieu.py`** | `✅ cong tai lieu DAT — 260 file, 2384 bang, 790 o ngay, 104 ma QD` |
| **`KẾT`** | **`ĐẠT — mọi phép kiểm khớp mong`** |

Ghi chú: ở đo thu thập đầu, `python3` hệ thống ⛔ có `psycopg` ⇒ 100 lỗi thu thập giả; dùng venv dùng chung `/home/user/FLS-tobe/.venv` ⇒ 3186 *(mẫu số > 0, xác nhận)*.

## Đánh giá hướng dẫn owner **v1.2** *(đọc từ đầu tới cuối như người ⛔ lập trình viên · Windows PowerShell — ⚠ container ⛔ có `pwsh`: hành vi PowerShell là **kiến thức, ⛔ đo**; chuỗi công cụ in thì ĐO bằng cách chạy công cụ)*
| Bước | Chép-dán được? | Mong khớp màn? | "Nếu thấy"? | Riêng tư | Ghi chú |
|---|:-:|:-:|:-:|:-:|---|
| Khung ⚠ đầu · Chuẩn bị | ✅ | — | — | ✅ | `$REPO` khai **một lần** `:43`; `Set-Location -LiteralPath $REPO` mở **12** khối; dặn *chỉ gửi True/False/số*; `$env:PYTHONUTF8` ✅ |
| **(0)** `Test-Path`/`Resolve-Path -LiteralPath` | ✅ | ✅ *(`True` + 2 đường)* | ✅ *(3 hàng)* | ✅ | `-LiteralPath` ở mọi đường có `[ ]`; có khung "chạy thử trước" |
| (a) `git fetch/checkout/pull` | ✅ | ✅ | ✅ | ✅ | phụ thuộc **đã gộp** — câu A/B của `BG-128` còn mở cho orchestrator |
| (b) tải CSV · `Move-Item -Force -LiteralPath (Get-ChildItem …).FullName` | ✅ | ✅ | ✅ *(5 hàng gồm "đích đã tồn tại" & "nhiều file")* | ✅ *(Downloads ⛔ còn bản)* | pattern `*Transaction Mapping L1*.csv` là wildcard **chủ ý**; đường đưa vào `-LiteralPath` là `.FullName` ✅ |
| (c) `xuat_khoa_dt1b.py --xlsx $XLSX --l1 …` | ✅ | ✅ *(chạy công cụ: `✅ xuất <tuyệt đối> — SO n hàng · L1 m hàng (7 cột bang,dong,so_ct,ps_no,ps_co,tk,tien_te)` · `hàng có ≥1 ô khoá / hàng 0 ô khoá — SO: a / b · L1: c / d` · `ô rỗng/cột` · `▶ bước kế`)* | ✅ *(6 hàng; chuỗi trích "không thấy …" là **dịch** của `⛔ thấy …` ⇒ `R3-03`)* | ✅ *(0 giá trị ô — sentinel 0/16)* | số mong `SO 9967` · `hàng 0 khoá = 0` khớp mã |
| (d) `phan_loai_ly_do.py --khoa` | ✅ | ⚠ *(① ② ③ ④ khớp `in_bao_cao`; `exit=4` khớp `CHUA_GHIM=4`; **dòng KẾT**: hướng dẫn "chưa phải ĐẠT" ≠ màn `⛔ phải ĐẠT` ⇒ `R3-03`)* | ✅ *(2 hàng K11 tách theo "0 khoá" > 0)* | ✅ | K11 `9967` không dấu chấm ✅ *(`:373`)* |
| (e) `--ghi` ở mã 4 | ✅ | ✅ *(`✅ đã ghi phan_loai_ly_do.json (mã 4)` = `:718`)* | ✅ | ✅ | ghi cả mã 4 xác minh `:716` |
| (f) `git status --porcelain` · `git add <MỘT tệp>` · commit · push | ✅ | ✅ *(đúng **một** dòng `?? docs/ITL/_tools/phan_loai_ly_do.json`: `git ls-files` chỉ có `phan_loai_dong_thieu.json` ⇒ `??` đúng; nếu đã theo dõi ⇒ ` M`)* | ✅ *(nhiều dòng / dòng khác ⇒ DỪNG, ⛔ `git add -A`)* | ✅ *(`hien_vat/` `.gitignore:17` · `Input_Raw/` `:23`)* | `git add` tên **một** tệp ✅ |
| (g) dọn | ✅ | ✅ *(`False`/`False`/`0` + danh sách `hien_vat` rỗng)* | — | ✅ | tự đủ `Set-Location`; `Remove-Item -LiteralPath`; Downloads dọn bằng `ForEach-Object … .FullName`; chạy được ở mọi nhánh dừng; có khung chạy thử |
| Báo kết quả | ✅ | ✅ | — | ✅ | chỉ mã thoát + bảng đếm; ⛔ dán giá trị khoá |

Kết luận hướng dẫn: **đủ** — 0 chỗ lộ dữ liệu *(⛔ bước nào bảo dán giá trị / commit tệp thô; `git add` một tệp)*; rủi ro còn lại là **kiến thức PowerShell chưa đo** *(đã khai + có chạy thử (0)/(g))* và `R3-03` *(chữ `⛔` trên màn)*.

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `DT1BT-R3-01` | GHI NHẬN · A1 | `tools/xuat_khoa_dt1b.py:134-151` | `Target="worksheets\sheet2.xml"` ⇒ `LoiDoc` một dòng, exit 1 *(không hồi quy; chờ tệp thật)* | `DEV` *(nếu gặp)* |
| `DT1BT-R3-02` | GHI NHẬN · B1 | `tests/du_lieu/test_xuat_khoa_dt1b.py:715-728` | M4 · M5 *(tương đương)* · M7 · M9 · M10 sống ⇒ thêm ca lật nén theo 4 phần + ca CRC + bài thoát gốc | `DEV` |
| `DT1BT-R3-03` | GHI NHẬN · B1 | hướng dẫn (d) *Mong* KẾT · bảng (c) | `phan_loai_ly_do.py:654` in `⛔ CHƯA GHIM MONG … ⛔ phải ĐẠT`; hướng dẫn trích bản đã dịch; owner thấy `⛔` trên màn | `DEV` |

## Bài thử mới
⛔ commit *(lệnh giao R3: chỉ phiếu + sổ)*. Đề xuất cho Dev: xem `R3-02`.

## Đối chiếu luật `Đ1…Đ5`
- **Đ1** *(phủ định)*: *"không có Traceback ở đường lỗi"* — đo 16 ca, `"Traceback" in stderr` = **0/16**; *"hướng dẫn ⛔ có `⛔`"* — `grep -c ⛔ HUONG_DAN…` = **0** *(đo lại)*, ngược lại công cụ in `⛔` ở `:114` `:126` `:152` `:161` `:170`… ⇒ `R3-03`; *"`phan_loai_ly_do.json` chưa có trong cây"* — `git ls-files docs/ITL/_tools | grep phan_loai` = `phan_loai_dong_thieu.json` *(⛔ phải `phan_loai_ly_do.json`)*, `ls` ⇒ không có.
- **Đ2**: so **hai nguồn** hướng dẫn ↔ mã *(chuỗi `Mong`)*: (c) · (e) khớp; (d) KẾT lệch ⇒ `R3-03`.
- **Đ3**: nền đột biến phải **> 0 bài xanh** trước khi đếm "bị bắt" — lần đầu 11/11 "bị bắt" là **đỏ giả** *(nền 3 đỏ do thiếu `.git`)*; lần đo CRC đầu exit 0 vì lật nhầm sheet decoy. Cả hai sửa trước khi kết luận.
- **Đ4**: `45` = số bài của `test_xuat_khoa_dt1b.py` · `3112` = chạy `--duong-nen` trên `isp/DT1BT` · `3186` = thu thập cây gộp *(= `3141` nhánh làm việc + 45)* · `29` = số dòng chứa `-LiteralPath` *(R2 từng báo 13 dòng ở v1.1; v1.2 thêm `$REPO`/`Set-Location`)*.
- **Đ5**: bài ghim `== ["3112"]` ĐỎ khi sai *(R2 đã chứng minh N18)*; công cụ ⛔ tự dừng khi "0 khoá" > 0 *(quyết A)*; đột biến M4/M5/M7/M9/M10 sống = cổng chưa canh.

## Câu hỏi cho orchestrator *(kèm khuyến nghị)*
1. **Gộp `isp/DT1BT` vào nhánh làm việc?** **Khuyến nghị A: GỘP** — 0 CHẶN · 0 NÊN SỬA; xung đột 2 tệp, giải bằng `--ours` + đặt sàn `3186` *(xem cây gộp)*; B: sửa 3 GHI NHẬN trước *(đổi chữ + 3 bài, ~5 phút)* rồi gộp.
2. **3 GHI NHẬN** *(`R3-02` bài · `R3-03` một câu chữ · `R3-01` chờ tệp thật)*: **Khuyến nghị A** — làm `R3-03` *(một câu)* + `R3-02` cùng vòng với việc ghim MONG sau số thật; ⛔ chặn owner chạy.
3. **A/B của `BG-128`** *(owner `git checkout claude/bold-galileo-zukpaf` ⇒ phải gộp trước)*: **Khuyến nghị A** — owner chạy **sau** khi gộp; hướng dẫn bước (a) đã giả định vậy.

## Commit
Chỉ phiếu `KQ-131` + sổ `SO_PHAT_HIEN_ISP-3.1_DT1BT.md` v0.3 *(đổi ô Trạng thái 9 hàng · thêm 3 hàng · changelog · bump header theo K1)*.
