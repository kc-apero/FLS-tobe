# KQ-129 — biên bản kiểm `BG-128` *(ISP 3.1.2 · Step 5 · DT1b tiếp · vòng **R1** — quét TOÀN diff)*

| | |
|---|---|
| **Thuộc** | `BG-128` · `WO-127` |
| **Kiểm bởi** | `fls-test` *(R1, phiên cloud mới, độc lập — vai KIỂM, ⛔ sửa mã hệ thống)* · 2026-11-18 · orchestrator giao |
| **Phạm vi** | `git diff 2b15531 isp/DT1BT` — **6** tệp *(`tools/xuat_khoa_dt1b.py` 322 dòng · `tests/du_lieu/test_xuat_khoa_dt1b.py` 14 bài · `HUONG_DAN_NHAN_THAT_DT1b.md` · sàn `3067→3081` ở `tools/dung_moi_truong_isp.sh` + bài ghim · `BG-128`)*. Ngọn `isp/DT1BT` = `1dc0bfc` *(đúng mong)* |
| **Cụm** | cổng **5437** do `dung_moi_truong_isp.sh --cong 5437` dựng — `KẾT: ĐẠT` *(7/7 phép kiểm)* |
| **Phán quyết** | **`ĐẠT`** R1 — **0 CHẶN · 6 NÊN SỬA** *(`DT1BT-R1-01` · `-02` · `-03` · `-06` · `-07` · `-08`)* · **3 GHI NHẬN** *(`-04` · `-05` · `-09`)*. Sáu AC ĐẠT trên phạm vi *dữ liệu tổng hợp*; **⛔ đo được trên tệp thật** *(O10 · `B-DATA-2`)* ⇒ hai rủi ro ⛔ loại trừ được ở container: `-01` *(nhà sinh xlsx)* · `-02` *(định nghĩa "hàng dữ liệu" vs 9.967)*. Khuyến nghị: **vòng sửa trước khi owner chạy** *(owner chạy SAU R3 — lựa chọn **A** của orchestrator)* |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1BT.md` *(tệp riêng, v0.1)* |

## Cổng chạy lại *(Test tự chạy — so với `BG-128`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_xuat_khoa_dt1b.py` | `14 passed` | `14 passed in 0.73s` | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(chạy MỘT MÌNH)* — toàn bộ | `12 failed, 3053 passed, 2 xfailed, 14 errors` · đỏ+XFAIL **28 = 28** · chạy 3081 | `12 failed, 3053 passed, 2 xfailed, 1 warning, 14 errors in 378.70s` · **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **3081** *(mong ≥ 3081)* · skipped 0 · deselected 0 | ✅ |
| …web | `3 failed, 664 passed` · đỏ **3 = 3** · chạy 667 | `3 failed, 664 passed in 178.83s` · **3 = 3** · chạy **667** · skipped 0 · deselected 0 | ✅ |
| `.venv/bin/lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ … 242 file, 2278 bảng` | `✅ cong tai lieu DAT … (243 file, 2282 bang, 776 o ngay, 104 ma QD)` — **243** gồm sổ mới của R1, **+4 bảng** *(sổ `DT1BT` — chưa phải lệch)* | ✅ *(chạy lại sau khi thêm sổ + phiếu: xem dòng cuối "Commit")* |
| `kiem_so_song` · `khop_owner` · `soi_bang_tuyen` · `kiem_thuyet_minh` | `⛔ CHƯA CHẠY` — ngoài phạm vi | ⛔ chạy *(đồng ý: WO thuần mã + bài tổng hợp, ⛔ chạm kho/tuyến/thuyết minh/schema; `git diff --stat` ⇒ 0 tệp trong `fls/` · `schema` · `web`)* | — |

## Bảng AC
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 | xlsx tổng hợp ⇒ CSV 7 cột đúng từng ô thô, `dong` = hàng Excel; thiếu cột ⇒ lỗi có tên, mã ≠ 0 | 5 bài AC-1 xanh. **Tự thử đọc đúng**: sharedStrings · `inlineStr` · `t="str"` · số *(`<v>4366190000000000` giữ nguyên chuỗi, ⛔ float)* · ô trống · cột thưa · tiêu đề **hàng 7+8** *(mã ĐÚNG: dữ liệu bắt đầu hàng 10)* · đúng sheet `ITL Ledge` giữa 2 sheet *(decoy `Bìa`)*. **Hở:** rels `Target` tuyệt đối ⇒ exit 1 `DT1BT-R1-01` · "hàng dữ liệu" tính cả hàng chỉ có ô công thức `DT1BT-R1-02` *(mã ⛔ sai theo spec WO — WO nói "mọi hàng dữ liệu")* · 3 đột biến sống `-05` | **ĐẠT** *(NÊN SỬA kèm: `-01` · `-02`)* |
| AC-2 | CSV L1 tổng hợp ⇒ hàng `L1` đúng, `dong` = hàng sheet | `test_AC2_*` 2 bài xanh; L1 `dong`=5/6 hình Sheets ✓; L1 non-UTF-8 / trường > 131 072 ⇒ **Traceback** `DT1BT-R1-04` | **ĐẠT** |
| AC-3 | 0 giá trị ô trên stdout/stderr · ra mặc định `hien_vat/` · từ chối đường trong repo ⛔ gitignore | **Tự đo thật 11 ca phá** *(XML hỏng · rels thiếu · zip hỏng · sheet thiếu · ô `t="e"` `t="b"` chỉ mục sst lạc · hàng ⛔ `r` · L1 cp1258 · L1 NUL · L1 trường 180 KB)* — sentinel `SECRET…` ở ô dữ liệu ∈ stdout+stderr: **0/11** · **ĐƯỜNG LỖI ⛔ có bài** — M6 · M14 SỐNG `DT1BT-R1-03`. Đường ra mặc định = `GOC/hien_vat/khoa_dt1b.csv`; `git check-ignore` ⇒ ignored *(`.gitignore:17`)*. Cột ngoài 7: `Diễn giải` + email ⛔ có trong tệp ra *(bài + đọc mã: chỉ 5 tên tiêu đề được tìm)* | **ĐẠT** *(mã sạch hôm nay; bài ⛔ khoá đường lỗi — NÊN SỬA `-03`)* |
| AC-4 | ca nối với `phan_loai_ly_do.py --khoa` chạy được | `test_AC4_*` 2 bài xanh *(Số CT số ↔ L1 khoa học `4.36619E+15` ⇒ CÙNG khoá; end-to-end exit ∈ {1,3,4}, ⛔ Traceback)* | **ĐẠT** |
| AC-5 | hướng dẫn chép-dán được trên PowerShell; có bước dọn tệp thô | 7 bước (a)–(g) có lệnh + "Mong" + bảng "Nếu thấy". Đường có `[ ]` **trong lệnh chạy** `--xlsx "…"` đúng; **3 chỗ yếu** `-06` *(`Test-Path` wildcard ⛔ đo — không có `pwsh`)* · `-07` *(`Copy-Item` ⇒ còn bản ở Downloads; ⛔ dọn ở nhánh lỗi)* · `-08` *(`⛔` đọc ngược; hàng bước (e) ngược dòng Mong)* · `-09` *(xlsx trong/ngoài repo, `Input_Raw` ⛔ gitignore)*. `kiem_tai_lieu` ĐẠT | **ĐẠT** *(NÊN SỬA kèm 3 hàng hướng dẫn)* |
| AC-6 (Q8) | sàn `3067 → 3081` + bài ghim cùng commit | `grep MONG_PYTEST_TOAN_BO` = **3081** · bài ghim `== ["3081"]` · `--duong-nen` **chạy 3081** · web 667 ⛔ đổi · `git show --stat 606ad89` chứa cả hai tệp ⇒ cùng commit | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | đúng spec WO-127 trên dữ liệu tổng hợp; 2 lỗ ở biên định dạng/định nghĩa | `-01` *(rels tuyệt đối)* · `-02` *(hàng dữ liệu)* · cột theo TÊN ⛔ gõ cứng chữ cái ✓ · `dong` = thuộc tính `r` ✓ |
| **Dữ liệu** *(kho thật, chỉ đọc)* | ⛔ đo được — công cụ ⛔ chạm kho; đường nền `kho fls RỖNG fls_itl = 0` | tệp thật `[Master] ITL_Ledge_raw.xlsx` chỉ có trên máy owner *(O10)*; mẫu số 9.967 chỉ `K11` của `phan_loai_ly_do.py` kiểm được lúc owner chạy |
| **Riêng tư** *(rủi ro số 1)* | **0 giá trị ô ra màn trong 11 ca phá + 14 bài** — nhưng đường lỗi ⛔ có bài khoá *(2 đột biến SỐNG)* | `DT1BT-R1-03` · 4 Traceback ⛔ mang giá trị `-04` · ra mặc định `hien_vat/` ✓ · từ chối đường trong repo ⛔ ignore ✓ *(M2 bị bắt)* |

## Đột biến *(bản sao `git archive isp/DT1BT`, `tests/du_lieu/test_xuat_khoa_dt1b.py`, 16 chỗ — M15 là vô hiệu, bỏ)*
| # | Đột biến | Kết quả |
|---|---|---|
| M1 | in `so[0]` ra stdout | **bị bắt** *(`test_AC3_khong_lo…`)* |
| M2 | tắt R8 (`_trong_repo_khong_ignore → False`) | **bị bắt** *(`test_AC3_tu_choi_duong_ra_trong_repo…`)* |
| M3 | Số CT qua `float` | **bị bắt** *(5 bài)* |
| M4 | lấy sheet đầu thay vì theo tên | **bị bắt** *(11 bài)* |
| M5 | đường ra mặc định ngoài `hien_vat/` | **bị bắt** *(3 bài)* |
| M6 | lỗi *"thiếu tiêu đề"* nối thêm hàng dữ liệu cuối | ⛔ **SỐNG** `14 passed` |
| M7 | `dong` +1 | **bị bắt** *(3 bài)* |
| M8 | `hang_tieu_de` `max → min` | ⛔ **SỐNG** `14 passed` |
| M9 | giữ hàng trống hẳn | **bị bắt** *(4 bài)* |
| M10 | L1 gồm hàng tiêu đề | **bị bắt** *(3 bài)* |
| M11 | bỏ `inlineStr` | **bị bắt** *(4 bài)* |
| M12 | bỏ chốt *"đường ra là thư mục"* | ⛔ **SỐNG** `14 passed` |
| M13 | bỏ chốt *"đầu vào vắng"* | **bị bắt** *(`test_AC3_dau_vao_vang_ma_2`)* |
| M14 | `except LoiDoc` in `repr(so)` | ⛔ **SỐNG** `14 passed` |
| M16 | L1 bỏ `.strip()` tiêu đề | ⛔ **SỐNG** `14 passed` |
| M17 | chỉ mục sharedStrings −1 | **bị bắt** *(5 bài)* |

**11/16 bị bắt · 5 sống** *(M6 · M14 ⇒ `-03` · M8 · M12 · M16 ⇒ `-05`)*. Lưu ý đo: lượt đầu cho kết quả méo — M2 *(tắt R8)* khiến bài từ chối ghi một tệp vào thư mục repo của bản sao, và tệp ấy làm bài từ chối đỏ ở các đột biến SAU *(M6 · M8 · M12 · M14 · M16 hiện "1 failed" giả)*; R1 dọn `git clean` giữa các lượt rồi đo lại, bảng trên là số sau dọn. Nháp: `/tmp/r1_dt1bt/mut.py` *(⛔ commit)*.

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `DT1BT-R1-01` | `NANG` | `tools/xuat_khoa_dt1b.py:123` | xlsx do `openpyxl` *(rels `Target="/xl/worksheets/sheet1.xml"`)* ⇒ exit 1 *"⛔ có tệp worksheet 'xl/xl/worksheets/sheet1.xml'"*; dạng tương đối ⇒ exit 0 | `DEV` |
| `DT1BT-R1-02` | `NANG` | `:206` *(SO)* · `:242` *(L1)* | hàng chỉ có ô công thức ở cột ngoài 5 khoá ⇒ thành "hàng dữ liệu": 3 hàng SO thay vì 1 | `DEV` *(+ orchestrator quyết định nghĩa)* |
| `DT1BT-R1-03` | `NANG` | bài `AC-3` + `main` | M6 · M14 SỐNG; thêm bài đường lỗi | `DEV` |
| `DT1BT-R1-04` | `NHE` | `:108,119,164,219` | 4 loại tệp hỏng ⇒ Traceback *(0/4 mang giá trị ô)* | `DEV` |
| `DT1BT-R1-05` | `NHE` | `tests/du_lieu/test_xuat_khoa_dt1b.py` | M8 · M12 · M16 SỐNG | `DEV` |
| `DT1BT-R1-06` | `NANG` | hướng dẫn `:100` | `Test-Path` có `[ ]` ⇒ `-LiteralPath` *(⛔ đo — không có `pwsh`)* | `DEV` |
| `DT1BT-R1-07` | `NANG` | hướng dẫn `:67` · `:179-183` | `Copy-Item` ⇒ còn bản ở Downloads; dọn ⛔ ở nhánh lỗi | `DEV` |
| `DT1BT-R1-08` | `NANG` | hướng dẫn `:144` · `:148` · `:169` | `⛔` = "không" đọc ngược; hàng bước (e) ngược dòng *Mong* | `DEV` |
| `DT1BT-R1-09` | `NHE` | hướng dẫn `:4` · `:83` · `:152-175` | `Input_Raw` ⛔ gitignore; ⛔ nói trong/ngoài repo | `DEV` |

## Đánh giá hướng dẫn owner *(đọc như người ⛔ lập trình viên, Windows PowerShell — ⚠ container ⛔ có `pwsh`: câu về hành vi PowerShell là **kiến thức**, ⛔ đo)*
| Bước | Chép-dán được? | Kết quả mong rõ? | Nếu thấy…? | Riêng tư | Ghi chú |
|---|:-:|:-:|:-:|:-:|---|
| Chuẩn bị `cd "…"` · `$env:PYTHONUTF8="1"` | ✅ | ✅ | — | ✅ | đúng cú pháp PowerShell |
| (a) `git fetch` · `checkout` · `pull` · `Test-Path tools\…` | ✅ | ✅ *(Test-Path đường ⛔ có `[ ]`)* | ✅ | ✅ | giả định **A** đúng *(owner chạy sau gộp)*; ⛔ nói gì nếu cây có thay đổi dở *(git ⛔ cho checkout)* — nhẹ |
| (b) tải CSV L1 · `Copy-Item "$env:USERPROFILE\Downloads\*…*.csv"` | ✅ | ✅ | ✅ | ⛔ **`-07`**: `Copy-Item` để lại bản ở Downloads | nhiều tệp khớp ⇒ ghi đè/ lỗi — nhẹ |
| (c) `.venv\Scripts\python.exe tools\xuat_khoa_dt1b.py --xlsx "Input_Raw\[Master] …" --l1 …` | ✅ *(ngoặc kép đủ cho Python)* | ✅ *(in số đếm; nêu 9967)* | ✅ *(4 hàng)*; ⛔ **`-06`**: `Test-Path` ⛔ `-LiteralPath` | ✅ | ⛔ **`-01`**: nếu xlsx do nhà sinh khác Excel ⇒ exit 1 ngay, bảng ⛔ có hàng cho câu này *("⛔ có tệp worksheet 'xl/xl/…'")*; ⛔ **`-02`**: K11 lệch |
| (d) `phan_loai_ly_do.py --khoa …` · `exit=$LASTEXITCODE` | ✅ | ✅ *(mã 4 + ①②③ + K11 ⛔ kêu)* | ✅ *(1/2/3/0)*; ⛔ **`-08`**: *"K11 ⛔ kêu lệch"* đọc là *"cấm kêu"* | ✅ *(K11/K10 in số + vài số hàng — 0 giá trị khoá, đọc mã `:370-376`)* | ⛔ dừng ⇒ ⛔ dọn tệp thô `-07` |
| (e) `--ghi` ở mã 4 | ✅ | ✅ | ⛔ **`-08`**: hàng *"⛔ dòng ✅ đã ghi dù mã 4"* ngược dòng Mong | ✅ | `--ghi` ghi ở mã 4: **xác nhận** — `tools/phan_loai_ly_do.py:716` `if ghi and ma in (DAT, CHUA_GHIM)`, `CHUA_GHIM = 4` |
| (f) `git status` · `git add <MỘT tệp>` · commit · push | ✅ | ✅ | ⛔ **`-08`** hàng `hien_vat` nhiều `⛔` ⇒ mơ hồ | ⛔ **`-09`**: `Input_Raw` ⛔ gitignore; nhưng `git add <MỘT tệp>` ⛔ `-A` ⇒ an toàn | tệp nhãn: **`phan_loai_ly_do.json` hôm nay ⛔ có trong cây** *(`ls` ⇒ không)* ⇒ `git status` hiện `??`, vẫn đúng *"chỉ MỘT tệp"* |
| (g) `Remove-Item hien_vat\…` | ✅ | ✅ | — | ⛔ **`-07`**: chỉ 2 tệp; ⛔ Downloads · ⛔ nhánh lỗi | `Remove-Item` ⇒ ⛔ vào Thùng rác *(đúng ý)* |
| Báo kết quả | ✅ | ✅ | — | ✅ *(chỉ mã thoát + bảng đếm, ⛔ khoá)* | — |

## Bài thử mới
⛔ commit *(lệnh giao R1: chỉ phiếu + sổ)*. Đề xuất cho Dev ở nháp `/tmp/r1_dt1bt/pha.py` *(ca rels tuyệt đối — ĐỎ trên `606ad89`)* · `mut.py` · `demo2.py` *(hàng chỉ-công-thức)*; vòng sửa của Dev tự viết bài trong `tests/du_lieu/`.

## Đối chiếu luật `Đ1…Đ5`
- **Đ1** *(phủ định)*: *"⛔ có bài đường lỗi"* — `grep -n "stderr" tests/du_lieu/test_xuat_khoa_dt1b.py` ⇒ mọi ca lỗi chỉ `assert "Tài khoản" in stderr`; không ca nào khẳng định sentinel ∉ — **kèm đột biến M6/M14 SỐNG** *(không chỉ đếm chữ)*. *Input_Raw ⛔ gitignore*: `grep Input_Raw .gitignore` ⇒ **0**, `git check-ignore -v` ⇒ exit 1.
- **Đ3** *(tập rỗng)*: các bài AC-1…AC-4 khẳng định số hàng > 0; bài quét riêng tư có ca phá *(sentinel CÓ trong tệp ra)* ⇒ phép quét ⛔ xanh trên tập rỗng ✓.
- **Đ4** *(con số nói đếm gì)*: bản in nói `SO N hàng · L1 M hàng` + `ô rỗng/cột`; hướng dẫn *"9967 hàng"* nói *"số dòng dữ liệu `ITL Ledge`, hàng 10…9976"* ✓ *(9976−10+1 = 9.967)*. Số `3081` = thu thập `pytest --collect-only` ✓ *(đường nền chạy 3081)*.
- **Đ5** *(mong, cả hai chiều)*: bài ghim sàn `== ["3081"]` ĐỎ khi sai ✓; cổng K11 ở `phan_loai_ly_do.py` bắt tập dòng lệch — nhưng công cụ xuất ⛔ tự báo *(`-02`)*.

## Câu hỏi cho orchestrator *(kèm khuyến nghị)*
1. **`DT1BT-R1-02` — định nghĩa "hàng dữ liệu"**: theo 5 cột khoá *(khuyến nghị **A**: đúng ý WO, ⛔ đếm hàng chỉ có công thức)* hay giữ "bất kỳ ô" + chỉ thêm số đếm chẩn đoán *(B)*? ⛔ đo được trên tệp thật ⇒ nếu có hàng thật 0 khoá thuộc 9.967 thì A làm K11 lệch. **Khuyến nghị: làm CẢ HAI** — in số đếm `≥1 khoá / 0 khoá` *(⛔ giá trị)* + giữ định nghĩa hiện tại cho tới khi owner chạy.
2. **`-01`**: đưa vào vòng sửa *(khuyến nghị **A** — một dòng, hỏng đóng hôm nay nhưng chặn owner)* hay hỏi owner nhà sinh của `[Master] ITL_Ledge_raw.xlsx` trước *(B)*?
3. Có thể nhờ owner xác nhận hai điều trên Windows trước khi chạy thật: `Test-Path "…\[Master] …"` trả gì · tệp xlsx nằm trong hay ngoài `C:\Users\0_Apero Project\FLS\` *(`-06` · `-09`)*.

## Commit
Chỉ phiếu `KQ-129` + sổ `SO_PHAT_HIEN_ISP-3.1_DT1BT.md`. `kiem_tai_lieu` chạy lại **sau** khi thêm hai tệp — kết quả ở tin nhắn cuối.
