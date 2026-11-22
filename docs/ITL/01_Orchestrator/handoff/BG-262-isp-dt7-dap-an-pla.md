# BG-262 — bàn giao WO-261 · ISP 3.1.2 · Step 31 · DT7: ảnh đáp án PLA1 · PLA3 HR · PLA3 PM+HR (PD 414–419)

| | |
|---|---|
| **Phiếu** | trả `WO-261` *(DT7, làn DATA)* |
| **Bởi** | phiên cloud `fls-dev #DATA` · cụm PG **5436** · nhánh `isp/DT7` · 2026-11-20 |
| **Nền** | `f903bab` + gộp ngọn `origin/claude/bold-galileo-zukpaf` `c1fc913` *(H7 + F5)* · commit ① mã+bài+ảnh *(sha ở tin nhắn cuối)* |
| **Dải phiếu** | `KQ-263` (R1) · `KQ-264` (R2 cuối). Số trống kế tiếp: **265** |

## 0. Kết luận
Đóng băng **6 ảnh** *(⛔ ba — lý do: công cụ đóng băng MỘT lưới ↔ MỘT ảnh; Daily và Y/H/Q/M là hai lưới khác trục, cùng tiền lệ `cfa1_daily`/`cfa1_yhqm`)*. Khuôn mới = tệp riêng `tools/khuon_dong_bang/_pla.py` + 6 khuôn `pla1_* · pla3_hr_* · pla3_pm_hr_*`; **⛔ sửa `dong_bang_sheet.py` · `_cfa1.py` · `cfa1_*.py`** *(`git diff f903bab HEAD` trên 4 tệp ấy = **0 tệp**; bài `test_AC7` giữ `SHA_GIU` cũ từng byte)*. Lý do không mượn `_cfa1.dung_cay`: tab PLA có **12 khối** *(⛔ 5 LE)*, `417` chỉ **1 khối**, có hàng KPI + hàng không nhãn.
Tự kiểm cộng theo vị trí ô **chạy được và có mong**: Daily **4 ô lệch** *(AS-IS, khối `GROUP`)* · Y/H/Q/M **0 ô lệch** · KPI **716 ô lệch** *(510 + 206, đếm RIÊNG)*.

## 1. Nguồn — ⚠ KHÁC phiếu: tab nằm ở sổ **P&L**, ⛔ sổ CF
Đo bằng `sa_ds.py` + `sa_meta.py` trên **67 sổ** SA đọc được *(mỗi sổ: liệt kê tên tab, lọc `Report I PLA`/`[MID]`)*: sổ CF *(bản gốc `1ITAIuCUjhIMaGm036bE6uczcHAj_TwpXtVlvXknDVP4` — 18 tab; bản `[COPY]` `12S00T…`)* có **0** tab PLA. Cả 6 tab nằm ở **`[COPY] Report I General Ledger | P&L Report`** `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` *(cùng sổ đã dùng cho 413)*, **mỗi tên đúng 1 ứng viên**; trong sổ ấy còn `Report I PLA3 Y H Q M | PM + HR | ATL` *(1110×196)* — ⛔ lấy *(khác tên)*. `UNFORMATTED_VALUE` + `SERIAL_NUMBER`; đọc `A1:SH1027` *(417: `A1:VD99`)*; đọc 2026-11-20 ~03:28Z *(= `ngay_dong_bang`)*.
| PD | Tab *(tên thật, từng ký tự)* | Lưới đọc | Ảnh |
|---|---|---|---|
| 414 | `[MID] Report I PLA1 Daily I PM only` | 1027×502 | `pla1_daily.json` |
| 415 | `[MID] Report I PLA1 Y H Q M \| PM Only` | 1027×502 *(197 cột có chữ)* | `pla1_yhqm.json` |
| 416 | `[MID] Report I PLA3 Daily \| HR Only` | 1027×502 | `pla3_hr_daily.json` |
| 417 | `[MID]  Report I PLA3 Y H Q M \| HR Only` *(HAI dấu cách sau `[MID]`)* | **99×576** *(92 hàng có chữ, 500 cột)* | `pla3_hr_yhqm.json` |
| 418 | `[MID] Report I PLA3 Daily I PM + HR` | 1027×502 | `pla3_pm_hr_daily.json` |
| 419 | `Report I PLA3 Y H Q M \| PM + HR` *(không `[MID]`)* | 1027×502 *(197 cột có chữ)* | `pla3_pm_hr_yhqm.json` |
⚠ **417 chỉ có khối `GROUP`** *(92 hàng, 1 khối × 74 mã)* và dải kỳ 26 năm *(494 cột)*; 415/419 có 12 khối × 190 cột kỳ. ⇒ Phép cộng Y/H/Q/M chỉ so được **GROUP**; 11 khối còn lại **46.398 ô** = `khong_so_duoc` *(ghi, ⛔ giả vờ khớp)*.

## 2. Hình khối ảnh *(mỗi số kèm nhãn — Đ4)*
Bố cục như CFA1: hàng 1–6 tiêu đề *(Daily: Year·Half·Quarter·Month·Day·thứ; YHQM: hàng 5 Year, hàng 6 Period)*, cột `A` = mUSD *(⛔ vào ảnh)*, `B…E` = L1…L4, `F` nhãn lặp, dữ liệu từ cột `G`. **12 khối**: `GROUP SGO2 SGO1 HGO6 BGO2` + 7 khối nhãn `CVL · COR · SHQ1 · CSM · CAH · ASA · SHQ2` *(mở ở hàng sheet 7·115·198·281·365·448·531·614·697·780·863·946)*; mỗi khối **74 mã HD** *(= cây ATL, cổng đòi chính xác)* ⇒ **888 hàng HD** *(417: 74)*.
| Ảnh | Khối | Hàng HD | Cột trục | Ô số ≠ 0 *(dòng chính)* | Hàng HD có ≥1 ô ≠ 0 *(= 888 − toàn-0)* | Mã HD khác nhau có số | Ô chữ `-` ở hàng HD | Cột `chua_co_du_lieu` |
|---|---|---|---|---|---|---|---|---|
| 414 `pla1_daily` | 12 | 888 | 496 ngày | 9.694 | 485 *(toàn-0: 403)* | 62 | 60 | 26 |
| 415 `pla1_yhqm` | 12 | 888 | 57 kỳ | 8.844 | 485 | 62 | 60 | 10 |
| 416 `pla3_hr_daily` | 12 | 888 | 496 ngày | 4.730 | 169 *(toàn-0: 719)* | 29 | 60 | 88 |
| 417 `pla3_hr_yhqm` | **1** | 74 | 57 kỳ | 486 | 29 *(toàn-0: 45)* | 29 | 5 | 33 |
| 418 `pla3_pm_hr_daily` | 12 | 888 | 496 ngày | 10.343 | 510 *(toàn-0: 378)* | 64 | 60 | 26 |
| 419 `pla3_pm_hr_yhqm` | 12 | 888 | 57 kỳ | 9.714 | 510 | 64 | 240 | 10 |
Kích thước ảnh *(luật `DT4-R1-07`: > 2 MB ⇒ khai)*: 414 **2,32 MB** · 415 **2,23 MB** · 416 1,34 MB · 417 0,14 MB · 418 **2,44 MB** · 419 **2,45 MB** *(tổng 10,9 MB)*. **Nguyên nhân**: công cụ ghi JSON thụt lề, mỗi ô là một object `{o_id, le, ma_hd, trục, gt}` + bảng phụ `hd` 888 hàng × 9 trường và trục 496 dòng; ⛔ có cách nén trong khuôn mà không sửa công cụ chung *(AC-7)*. ❓ orchestrator: chấp nhận hay giao việc nén?
**Hàng ngoài cây** *(⛔ vào ảnh)*: vùng `CHECK ZONE`/ghi chú *(khối `GROUP`: dòng sheet 89–114)* nhận ra là `khac` và nằm SAU dữ liệu *(bất biến ④)*; ở 414 có **17 ô `#REF!`** *(cột 79 = `CA`, hàng sheet 97–113 — vùng ghi chú, ⛔ hàng HD)* ⇒ **không vào ảnh**, ghi ở đây. `hang_khong_nhan` = **0** hàng *(⛔ hàng không nhãn nào mang số)*.

## 3. Dải ngày · kỳ *(AC-4)*
- **Daily** *(414/416/418)*: **496 cột LIÊN TỤC** serial 45585…46080 = **2024-10-20 (CN) … 2026-02-27**; cắt cột = 0 *(đều ≤ ngày đọc 2026-11-20)*. ⚠ **Mốc 2024-10-20 ≠ 21/10/2024 của AP** — giữ mốc THẬT của sheet *(như CFA1)*; thứ ngày khớp `(serial+6)%7` mọi cột.
- **Kỳ** *(415/417/419)*: **57 cột = 2024·2025·2026 × 19** *(Y · H1 H2 · Q1…Q4 · M01…M12)*; **cắt cột tương lai** *(năm > 2026)* — số ô ≠ 0 bị cắt = **0** *(kiểm ③)*.
- **`chua_co_du_lieu`** *(cột trục không có ô ≠ 0 ở hàng HD nào — ghi tên, ⛔ hoá 0)*: PLA1 Daily **26** *(từ 46055 = 2026-02-01 → 02-27)* · PLA1 Y/H/Q/M **10** *(2026M03…M12)* · **HR Daily 88** *(từ 45993 = 2025-12-02 → 2026-02-27: sổ HR là `Y2025`)* · HR Y/H/Q/M 33 · PM+HR Daily 26 · PM+HR Y/H/Q/M 10.
- **419: ô CHỮ `-` ở cột TƯƠNG LAI bị cắt = 420** *(mã `AR`·`CP*` gõ tay)*: `_cfa1.kiem_tuong_lai_rong` coi chữ là ≠ 0 và từ chối cả tab ⇒ khuôn mới (`_pla.kiem_tuong_lai_rong`) chỉ đòi **số** = 0, ghi phân bố ở bảng phụ `tuong_lai_chu` *(`{"-": 420}`, cổng Đ5 ĐỎ khi khác)* — ⛔ cắt im lặng.

## 4. Tự kiểm cộng theo VỊ TRÍ ô *(AC-2 · AC-3 — hàm `tu_kiem`, `tests/du_lieu/test_dap_an_pla.py`)*
Khoá ô = `(khối, mã HD, ngày|kỳ)`; dung sai **|Δ| ≤ 1e-6 mUSD** *(khai)*; so ô có ở cả 3 ảnh.
| | Daily *(418 vs 414+416)* | Y/H/Q/M *(419 vs 415+417)* |
|---|---|---|
| **Ô so được** *(hàng HD × cột trục có ở cả 3 ảnh)* | **440.448** = 888 × 496 | **4.218** = 74 × 57 *(chỉ GROUP)* |
| …`0 = 0 = 0` | 430.084 | 2.639 |
| …có số thật *(≥1 giá trị ≠ 0)* | 10.364 | 1.579 |
| Khớp, **không-KPI** có số thật *(bằng chứng DƯƠNG)* | 2.699 | 1.094 |
| **Ô LỆCH không-KPI (của AS-IS)** | **4** | **0** |
| Ô lệch **KPI** *(AC-5, RIÊNG)* | **510** *(`NPC` 408 · `EBITDA`/`EBIT`/`EBT`/`NP`/`PL6`/`PL7`/`PL8` 14 mỗi mã …)* | **206** |
| Không so được *(417 thiếu 11 khối)* | 0 | **46.398** = 11 × 74 × 57 |
**4 ô lệch không-KPI của AS-IS** *(khối `GROUP`; chênh = `PM+HR − (PLA1+HR)`, mUSD)*:
| Khoá ô | PM+HR | PLA1 | HR | Chênh |
|---|---|---|---|---|
| `GROUP#GAC#45597` *(2024-11-01)* | −0,11718595749216483 | −0,010968281594147093 | −0,08978994140086179 | −0,016427734497155947 |
| `GROUP#GAC#45627` *(2024-12-01)* | −0,2887267269098367 | −0,14829451539814809 | −0,10779161576274277 | −0,03264059574894584 |
| `GROUP#NCFO#45597` | 0,007054497739929413 | 0,0013814979550873484 | 0,022100734281998005 | −0,0164277344971559404 |
| `GROUP#NCFO#45627` | 1,9217150524867188 | 1,9056845184802604 | 0,048671129755405294 | −0,032640595748946894 |
Hai cặp trùng chênh *(−0,016428 · −0,032641)* ⇒ cùng một nguyên nhân gốc ở `GAC`, lan sang `NCFO` *(⛔ truy nguyên — ngoài phạm vi; lệch là của AS-IS, ⛔ của FLS)*.
**KPI vì sao lệch (đo, không phải lỗi)**: công thức hàng KPI tính CHÉO hàng và dấu HR **ngược** PM: 414/418 `EBITDA = G8+G9+G23`, 416/417 `G8-G9-G23` ⇒ `EBITDA(PM+HR) ≠ EBITDA(PLA1)+EBITDA(HR)` về cấu trúc. Phép cộng vị trí chỉ áp cho hàng `la` + `tong`.
**Mong khai** ở `MONG_TU_KIEM` *(+ hash danh sách lệch `dbfddf4a…`·`2fe00184…` Daily · `4f53cda1…`·`2b1f1041…` Y/H/Q/M)*. **Chứng minh ĐỎ** *(Đ5)*: đột biến **1 ô** — đổi `PM+HR`, xoá ô `PLA1`, đổi ô `HR` — ở cả Daily lẫn Y/H/Q/M ⇒ `lech` tăng đúng **+1** *(6 ca xanh = cổng cắn)*; đột biến 1e-9 *(dưới dung sai)* ⇒ ⛔ đỏ. Cổng khuôn trên bản thô đột biến: đổi nhãn mã thành mã lạ ⇒ `[ĐỎ] thiếu 4` · thêm ô `#REF!` ⇒ `[ĐỎ] phụ o_loi 61 ≠ 60` · đổi 1 ô số ⇒ `[ĐỎ] 9695 ≠ 9694` *(exit 1 cả ba)*.

## 5. KPI đếm riêng *(AC-5)*
**17 mã KPI** *(công thức CHÉO hàng, đo từ cột G tab 418, đồng nhất cả 12 khối)*: `CRO COO COI CRF COF NCF NPC EBITDA EBIT EBT NP PL2 PL3 PL4 PL6 PL7 PL8` ⇒ **204 hàng** *(17 × 12; 417: 17)*. Ô ≠ 0 nằm ở hàng KPI: 414 **7.493** · 415 4.317 · 416 3.681 · 417 80 · 418 7.661 · 419 4.441 — ⛔ trộn vào "số ô khớp". Loại khác: `la` **40 mã** *(ô tra sổ `SUMIFS` / `=PLA1!G+HR!G`)* · `tong` **10** *(`OPC CAC MAC COS GAC CDC CXI NCFO NCFI NCFF`: `=sum(G…)`)* · `trong` **7** *(`AR CP1.1 (PL2) CP1.2 CP2 CP3 CFO PL5`: ⛔ công thức ở `G`; 5 mã đầu mang `-` gõ tay)* ⇒ 40+10+17+7 = 74. Khai ở `_pla.LOAI_MA`; mã chưa khai ⇒ `?` ⇒ cổng ĐỎ.
Công thức nguyên văn — **hàng mẫu GI (dòng 8), cột G**:
- 414: `=SUMIFS('Report I General Ledger'!$BR:$BR,'Report I General Ledger'!$DE:$DE,G$5,'Report I General Ledger'!$V:$V,$F8)-SUMIFS('Report I General Ledger'!$BS:$BS,'Report I General Ledger'!$DE:$DE,G$5,'Report I General Ledger'!$V:$V,$F8)`
- 416: `=SUMIFS('Report I H1000 Ledge (HR Allocate HD) Y2025 | For PL Report'!$BA:$BA,…!$BM:$BM,G$5,…!$V:$V,$F8)-SUMIFS(…!$BB:$BB,…)` *(cùng khuôn, nguồn HR Y2025; cắt gọn ở `…`)*
- **418: `='[MID] Report I PLA1 Daily I PM only'!G8+'[MID] Report I PLA3 Daily | HR Only'!G8`** ⇒ **xác nhận "PM+HR = PLA1 + PLA3 HR cùng vị trí"** *(451 ô cột G dạng `…!G+…!G`; hàng `tong`/KPI tự tính trong tab)*
- 415: `=sumifs('[MID] Report I PLA1 Daily I PM only'!$G8:8,'[MID] Report I PLA1 Daily I PM only'!$G$1:$1,G$6)`; 417: cùng dạng, nguồn `…PLA3 Daily | HR Only`; **419: cùng dạng, nguồn `[MID] Report I PLA3 Daily I PM + HR` (418), ⛔ 415+417** ⇒ Y/H/Q/M của PM+HR là Σ-kỳ của Daily PM+HR.
- Hàng KPI: 414/418 `EBITDA G64 = G8+G9+G23`; 416/417 `=G8-G9-G23`; `NCF G69 = G70+G73+G76` mọi tab.

## 6. `#REF!`/`-` ở nguồn *(AC-6)*
Ô `#REF!` ở **hàng HD** = **0** *(17 ô `#REF!` ở 414 nằm vùng ghi chú, §2)*; tập ô chữ ở hàng HD = **{`-`}** *(ghim)*: 414/415/416/418 **60** ô *(đúng 1 cột — cột đầu — × 5 mã × 12 khối)*; 417 **5**; **419 240 ô / 37 cột**. Giữ NGUYÊN chuỗi, đếm theo cột; thêm `#REF!`/`#N/A` ⇒ cổng ĐỎ *(luật `DT5-R1-04`)*; lời lỗi ⛔ in giá trị ô *(`_an_toan` + bài `test_AC6_loi_tu_choi…`)*.

## 7. PII *(AC-8)*
Lưới chỉ có mã khối/mã HD/số; `soat_pii_luoi` quét 7 hàng tiêu đề + cột `A…F` *(`Email Address` = 0 trùng)*; ảnh chứa `@` = **0**. `python tools/quet_pii_repo.py` → `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp`. Bản thô ở `/tmp/dt7` *(chmod 600, xoá sau dùng)*, ⛔ commit.

## 8. TDD · cổng
- **ĐỎ trước** *(bài thật, đỏ vì THIẾU ảnh)*: `python -m pytest tests/du_lieu/test_dap_an_pla.py` ⇒ **exit 1 · `9 failed`** *(`FileNotFoundError …/pla1_yhqm.json`)*.
- **XANH sau**: cùng lệnh ⇒ **48 passed**; + `test_dap_an_cfa1.py` ⇒ 79 passed.
- **Q8**: `MONG_PYTEST_TOAN_BO` **4267 → 4321** *(= `pytest --collect-only`: 4.321)*, bài ghim `tests/test_dung_moi_truong_isp.py:423` cùng commit; `MONG_PYTEST_WEB` 681 *(⛔ đổi)*.
- `quet_pii_repo` exit 0 · `lint-imports` **11 kept, 0 broken** · `kiem_tai_lieu.py` ✅ *(410 file · 2.783 bảng · 909 ô ngày · 104 mã QĐ)*.
- `--duong-nen --cong 5436`: **KẾT: ĐẠT** — toàn bộ: tập đỏ + XFAIL = đường nền 28 = 28 node id *(XFAIL 2 = 2, thêm 0, bớt 0)* · chạy **4321** bài *(mong ≥ 4321)*, skipped 0 · `tests/web` 3 = 3 · chạy **681** *(mong ≥ 681)*. ⚠ Lần chạy đầu bị container khởi động lại giữa chừng *(mất, ⛔ có kết quả)* ⇒ dựng lại cụm 5436 và chạy lại MỘT lần, ĐẠT.

## 9. Giả định *(chọn phương án hẹp nhất)* · khuyến nghị
1. **Nguồn = sổ P&L `19NNTb…`**, ⛔ sổ CF như phiếu — 6 tab chỉ ở đó, mỗi tên 1 ứng viên. ❓ Orchestrator xác nhận sổ.
2. **Sáu ảnh** thay vì ba *(lý do §0)*.
3. `loai` hàng suy từ **công thức cột G tab 418**, đồng nhất 12 khối × 74 mã *(0 mã không đồng nhất)*; ⛔ kiểm lại ở 414/416.
4. Mốc ngày 2024-10-20; cắt kỳ theo **năm ≤ năm đọc** *(2026)*, không theo tháng — 2026M03…M12 giữ `chua_co_du_lieu`, ⛔ hoá 0.
5. 417 chỉ GROUP ⇒ 11 khối không so được — ❓ BA: H8 có cần HR Y/H/Q/M đủ 12 khối không *(nếu có thì thiếu đáp án)*.
6. 4 ô lệch `GAC`/`NCFO` của AS-IS **giữ nguyên làm đáp án** *(⛔ sửa)* — H8 cần quyết dung sai.
