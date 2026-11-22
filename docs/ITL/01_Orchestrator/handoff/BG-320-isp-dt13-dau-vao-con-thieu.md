# BG-320 — bàn giao `WO-319` *(ISP 3.1.2 · DT13 · đóng băng ĐẦU VÀO còn thiếu cho WP-C5a · C5b · C5c)*

| | |
|---|---|
| **Thuộc** | `WO-319` |
| **Phát bởi** | `fls-dev` làn DATA · phiên cloud · cụm PG **5436** · 2026-11-22 |
| **Nhận** | `fls-test` *(R1 → `KQ-321`, R2 cuối → `KQ-322`)* |
| **Commit** | `isp/DT13` ⇒ `claude/bold-galileo-zukpaf-isp/DT13` · ① mã + bài + ảnh · ② BG này |
| **Kho thật** | `KHONG_CHAM` · khoá SA chỉ-đọc · bản thô ở scratchpad chmod 600, xoá sau, ⛔ commit |

## Kết luận một dòng
**6 ảnh `dau_vao` mới** đóng băng xong cho **615 (khối CB + mUSD/CM)**, **MID3 TOTAL**, **COM theo CDT**, **Sign off làm đầu vào của luỹ kế FS1**; AC-3 dựng lại khớp 5 nhóm ô. **605 DỪNG** *(0 ứng viên thượng nguồn)*; **HR DR2** và **By NOEM** *(cần `H1000 I HR Report`)* **chưa làm** — bảng §4.

## 1 · AC-1 — ô đáp án → sổ · tab · vùng *(đọc `FORMULA` chỉ-đọc 22/11; Đ4: mỗi số đếm MỘT vật)*
| Ô đáp án | Công thức đọc được *(đại diện ≥ 3 ô/nguồn)* | Nguồn | Xếp |
|---|---|---|---|
| **615** khối `CB I Cash Balance by LE` *(1.497 ô công thức)* | `=SUMIFS('2. CCR Cash'!$K10:10,…$K$5:$5,F$5)/10^6+SUMIFS('2. CCR'!$K10:10,…)/10^6` *(hàng 56)* · hàng 61 · hàng 89 `/10^9` | A-CCR `2. CCR` *(236×741)* · `2. CCR Cash` *(175×719)*; thượng nguồn của hai tab = `1.1/1.2 Ledger` · `Cash Ledger Transactions` *(sổ cái, PII — ⛔)* | **(a) đóng băng** |
| **615** `Unit: mUSD` · `CM Cumulative` · `person GROUP` | `='5. Daily Report 2'!<cùng cột><hàng+hằng>` — **21.014** công thức, 100 % cùng cột, độ lệch hằng theo khối | A-CCR `5. Daily Report 2`: **dán giá trị** *(26.459 hằng, 31 công thức ở hàng 1)* — ⛔ trùng bản CF report *(BG-270: 1.120 ô lệch)* | **(b) đóng băng** |
| **615** `person [FS1/FS2][PLA3]` từng CDT | `='5. Daily Report 3'!…` | A-CCR `5. Daily Report 3`: dán giá trị; **35.542/35.542** ô số trùng ảnh `daily_report_3_gop` | không ảnh mới *(đã có)* |
| **605** Sign off | tab **0 công thức** *(đo cả `A1:GU137`)* | tab `[MID][FS1][PLA5]5. Daily Report 3 (Sign off)` — dán giá trị; tab gốc `[FS1][PLA5]` ⛔ còn trong sổ *(24 tab P&L Report, 0 ứng viên)* | **DỪNG** việc *tái lập* 605; giá trị dán đã có (DT11) |
| **608/609** luỹ kế FS1 `CM Cumulative` | `='[MID]…(Sign off)'!W5/sumifs('9.2.Exchange Rate'…)/10^6[*-1]` *(1.363 ô)* · `='[FS2]5. Daily Report 3'!T435` · `=…ATL!AG35` · `=SUMIFS(T$430:T$510,…)*INDEX('Allocation Table \| By NOEM & By GI'…)` | Sign off · FS2 *(ảnh 607)* · ix_fx · ATL · `Allocation Table` *(By GI ← MID3 TOTAL; **By NOEM ← HR Report**)* | **(b)** Sign off ✔ · By GI ✔ *(tính từ `mid3_total`: 66/66 + 66/66, đo)* · By NOEM ⛔ |
| **ATL** lá `GI·OMC·SC·PS` khối CDT | `SUMIFS` hàng `TOTAL yyyymm` cột PM ÷10⁶ | P&L Report 4 tab `CFA2 \| MID 3 \| …` | **(a) đóng băng** |
| **ATL** PL5 khối CDT | `=sumifs('[2025][RPT] NOEM PL & COM'!F$18:F$26,…,left(A…,3))/USD/10^6*-1+PL4` | tab dán giá trị *(0 công thức ở `F18:Q26`)* | **(b) đóng băng** |
| **610** `hr` *(1.537 ô)* | `='H1000 I HR Report'!NZ7`… | CF report `[H1.2026][2025]H1000 I HR Report` *(4.314×23, đếm người)* — **1 ứng viên** | **chưa làm** *(§4)* |

## 2 · Ảnh mới *(AC-2 — `mong` Đ5 · nhãn Đ4 · checksum TÍNH LẠI · < 2 MB)*
| Ảnh `tests/fixture/dau_vao/` | Dòng × cột *(gồm khoá)* | Ô SỐ | MB | `checksum_noi_dung` |
|---|---|---|---|---|
| `ccr_so_du_ccr` | 191 × 36 | 5.921 | 0,21 | `9693d0a529bef99e` |
| `ccr_so_du_cash` | 62 × 36 | 1.922 | 0,07 | `f5822422a91a0f58` |
| `ccr_daily_report_2` | 846 × 40 | 25.426 | 0,76 | `db3ca1baedf59413` |
| `mid3_total` | 39 × 17 | 546 | 0,04 | `710889dbe81db12f` |
| `noem_com_cdt` | 9 × 15 | 108 | 0,005 | `eaa7fd6008a66569` |
| `sign_off_dau_vao` | 94 × 200 | 13.541 | 0,59 | `ef1744caf253f3bd` *(= ảnh đáp án 605, cùng nội dung)* |
- Khuôn: `_ccr_so_du.py` + `ccr_so_du_ccr|cash` · `ccr_daily_report_2` *(nạp NGUYÊN `daily_report_2.chuan_bi`)* · `mid3_total` · `noem_com_cdt` *(dùng hằng `noem_com_gag`)* · `sign_off_dau_vao` *(nạp `daily_report_3`)*. `dong_bang_sheet.py` + 6 ảnh `dau_vao` cũ **đúng từng byte** *(sha ghim ở bài)*; 22 ảnh `dap_an` ⛔ đụng.
- `sign_off_dau_vao` trùng ảnh đáp án vì engine cấm đọc đáp án *(AC-4 H14)*: cần bản ĐẦU VÀO riêng.
- Cột ngày `ccr_so_du_*` = 31 ngày 31/10→30/11/2026; mọi ngày có 191 / 62 ô *(ngày 0 ô: 0)*.

## 3 · AC-3 — dựng lại *(chỉ để ĐO; mẫu số khai TRƯỚC — Đ3)*
| Nhóm ô đáp án | Phép dựng | Mẫu số | Khớp |
|---|---|---|---|
| 615 CB `G…AJ` | Σ dấu × `2. CCR`/`Cash`[hàng, ngày] ÷10^6 hoặc 10^9 | 46 hàng × 30 ngày = **1.380** | **1.380** *(hàng **71** ⛔ vào: cấu trúc đổi giữa các cột)* |
| 615 `Unit: mUSD` 5 khối | ô = `DR2[hàng+hằng]` | 12.245 | **12.245** |
| 615 `CM Cumulative` GROUP | idem | 2.176 | **2.176** |
| 615 `CM Cumulative` 4 khối LE | idem | 8.704 | 7.724 — **980 lệch có tên**: ô 615 ⛔ phải tham chiếu trực tiếp |
| ATL lá MID3 `GI·OMC·SC·PS` × 6 CDT | PM ÷10⁶ *(×−1 trừ GI)* | 39 × 6 = **234** | **231** — 3 lệch = `PS` 202512 *(SHQ1·CSM·CAH)*; khớp BG-292 *(PS 51/54)* |
| ATL PL5 7 khối × 12 tháng | `PL4 − COM/USD/10⁶` | **84** | **84** |
| 608 `CM Cumulative` ô Sign off | `Sign off ÷ USD(tháng) ÷10⁶ [×−1]` | **1.363** | **1.363** |
Mỗi nhóm có bài PHA *(đổi 1 ô nguồn ⇒ số khớp −1, đúng ô)*.

## 4 · Còn lại — chưa làm / DỪNG
| Việc | Trạng thái | Cần gì |
|---|---|---|
| 605 tái lập | **DỪNG** — tab gốc `[FS1][PLA5]` không còn | chủ chỉ tab/ảnh nguồn |
| HR DR2 (610 `hr` 1.537 ô) · By NOEM *(luỹ kế CDT FS1)* | **chưa làm** — hết thời gian; ứng viên duy nhất `[H1.2026][2025]H1000 I HR Report` | đóng băng + soát PII từng hàng ở vòng sau |
| Raw Data Management / Daily Transactions của 615 *(220 công thức nội bộ)* | **chưa đo** | — |
| Luỹ kế FS1 tháng sau Sign off *(`GI MID3 cột O × F`)* | chưa đo đủ | — |

## 5 · PII
Bản đồ cột bằng tiêu đề trước. Chỉ đọc `A·B·C·F` + cột ngày của `2. CCR`/`Cash` *(⛔ `E` số TK · `G` · **`H` ID · `I` Pass** · `J`)*; nhãn `R | <tên người>` che `TK_CA_NHAN_1` *(1 nhãn)*; MID3: chỉ hàng khớp `TOTAL <yyyymm>` *(⛔ `Số chứng từ`)*. `quet_pii_repo.py`: **0 chỗ · 0 tệp**. Bài PII: `HoangACB`/`Hoang` 0 trong ảnh, 0 nhãn ≥ 8 chữ số.

## 6 · Cổng
| Lệnh | Kết quả |
|---|---|
| ĐỎ trước | `test_dau_vao_dt13.py`: 14 failed · 12 errors *(chưa ảnh)* ⇒ 40 passed |
| Đột biến `mong` khuôn *(trả nguyên, `git diff` rỗng)* | `ccr_so_du_ccr` `o_so`+1 ⇒ ĐỎ · `mid3_total` `PS` 9→10 ⇒ ĐỎ |
| `--duong-nen --cong 5436` *(một mình, MỘT lần)* | **KẾT: ĐẠT** — `12 failed · 4696 passed · 2 xfailed · 14 errors`: tập đỏ nền **28 = 28** · chạy **4724** *(mong ≥ 4724; Q8 4678 → 4724 cùng commit)*; `tests/web` 3 = 3, 690 |
| `lint-imports` | 11 kept, 0 broken |
| `kiem_tai_lieu.py` | ĐẠT *(chạy lại sau BG)* |
| `quet_pii_repo.py` | 0 chỗ · 0 tệp |

## Câu hỏi
1. 605: có nguồn khác thay tab `[FS1][PLA5]` đã mất không, hay chấp nhận 605 chỉ là giá trị dán?
2. Mở vòng DATA kế cho HR Report *(610 `hr` + By NOEM)*?
