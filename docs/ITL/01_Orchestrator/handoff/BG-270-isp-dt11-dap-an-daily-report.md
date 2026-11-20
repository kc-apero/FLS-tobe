# BG-270 — bàn giao `WO-269` *(ISP 3.1.2 · Step 41 · DT11: ảnh đáp án Daily Report 2 · 3, PD 607–616)*

| | |
|---|---|
| **Trạng thái** | `CHO_KIEM` — Dev xong 20/11 · nhánh `isp/DT11` *(nền `d9ac21f`)* · chưa R1 |
| **Phát bởi** | `fls-dev` làn DATA *(phiên cloud con, Sonnet 5.5)* |
| **Ghi kho thật** | `KHONG` *(cụm PG 5444 chỉ chạy đường nền)* |

## 1 · Nguồn — bước đầu đo tên tab + lưới *(Đ1: cả hai nguồn chính CÓ MẶT, 1 ứng viên mỗi nguồn ⇒ không dừng)*
| Ảnh | Sổ · id | Tab · lưới | Vùng đọc *(thật)* |
|---|---|---|---|
| `daily_report_3` *(PD 605)* | `[COPY] Report I General Ledger \| P&L Report` · `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` | `[MID][FS1][PLA5]5. Daily Report 3 (Sign off)` **137 × 203** | `A1:GU137` · 137 hàng *(127 có dữ liệu)* |
| `daily_report_2` *(PD 610)* | `[COPY] Report I General Ledger \| CF report` · `12S00TnFMd9Uz0g-NLvOA7kdmPPhY1V_SVOQJkDi1ZiU` | `5. Daily Report 2` **1114 × 44** | `A1:AR1114` ⇒ API trả **958 hàng × 38 cột** *(cắt hàng cuối rỗng; vùng dữ liệu `A1:AL958`)* |
| *đối chiếu A-CCR (D5)* | `A-CCR_V2_Working` · `1ycMOKKZg5rraLAYW-HuZDp9k3RPzr0H-iyPs_0IKL5Q` | `5. Daily Report 2` 1114×44 *(cùng lưới)* · `5. Daily Report 3` 1940×40 | DR2 `A1:AR1114` *(chỉ đọc, ⛔ đóng băng)* |
Đọc `values.get` · `UNFORMATTED_VALUE` · `SERIAL_NUMBER` · khoá SA chỉ-đọc; bản thô `/tmp/dt11` chmod 600, **đã xoá**, ⛔ commit. ⚠ `google-auth` chưa có trong `.venv` ⇒ `pip install google-auth requests` *(⛔ đổi repo)*.
**Không đọc / không đóng băng** *(WO chỉ đòi 2 ảnh)*: PD 607–609 *(`[FS2]`·`[FS1]`·`5. Daily Report 3` ở P&L Report 1424/1092/1940 × 40)* · PD 614 `9.2.Exchange Rate` · 615 `5. Daily Report` *(12521×44)* · 616 `6. CCR I DEL I W I Pdf` — chỉ ĐỔI tên tab/kích thước ở bảng trên; xem "Giả định" ①.

## 2 · Ảnh — dòng · cột · ô *(Đ4: mỗi số đếm MỘT vật)*
| | `daily_report_3` | `daily_report_2` |
|---|---|---|
| **Dòng ảnh** *(hàng sheet có ≥ 1 ô giá trị)* | **94** *(sheet `5…137`; + 28 hàng chỉ-nhãn ở phụ `dong_chi_nhan` + 11 hàng rỗng hẳn)* | **846** *(= `ngay` 395 · `luy_ke` 340 · `hr` 111; + 84 hàng chỉ-nhãn ở phụ)* |
| **Cột ảnh** *(khoá `dong_sheet` + chọn)* | **199** = nhãn `ma·ten·logic·nguon_j` 4 + `cap` 1 + `y24·y25` 2 + **192** kỳ `<thực thể>_<yyyymm>` | **39** = `che_do·khoi·ma·nhan_b…e` 7 + **32** cột `g…al` *(= chữ cột Sheets `G…AL`)* |
| **Ô số ≠ rỗng** *(mẫu số — Đ3)* | **13.541** / 18.236 *(94 × 194 cột giá trị)* | **26.272** / 27.072 *(846 × 32)* |
| Nhãn từng số *(Đ4)* | `ma` = `HDCode` *(cột E)* · thực thể = hàng 1 · kỳ = hàng 3 · VND | `ma` = mã trước `\|` ở nhãn B:E · nghĩa cột = phụ `tieu_de` *(356 ô)* · `ngay`/`hr`/`luy_ke` · mUSD *(hr = người)* |
| Kích thước | **0,59 MB** | **0,76 MB** *(< 2 MB, luật `DT4-R1-07`)* |
| `checksum_noi_dung` | `ef1744caf253f3bd` | `01113b55ba953108` |
- **DR3** *(Sign off)*: tab **dán giá trị — 0 ô công thức**. 8 thực thể `Group · VisionLab · TeraSofts · SuperMinds · Astronex · IOs · Headquarters · CHECKING` × 24 kỳ `202401…202512` = 192 *(cột `FW` là khe trống giữa HQ và CHECKING; 0 ô giá trị ngoài cột có tiêu đề kỳ)*; `K…GU`.
- **DR2**: `ngay` = hàng `11…425`, 5 khối `GROUP·SGO2·SGO1·HGO2·BGO2`, cột `G…AJ` = **30 ngày 01→30/11/2026** *(`From`=46327 · `To`=46356)* + cột **`AK` không có ngày** *(nhãn `Sat`, vẫn 844 ô số)*; cột `F` *(= 31/10/2026, "Month 10")* **0** ô dữ liệu. `luy_ke` = từ `CM Cumulative` *(hàng 426)*: 5 khối × 32 kỳ = `2025` Y·H1·H2·Q1…Q4·M1…M12 *(`G…Y`)* + `2026` Y·H1·H2·Q1…Q4·M1…M6 *(`Z…AL`)*. `hr` = từ `Report HR` *(hàng 843)*, 1 khối `GROUP`.

## 3 · Dải ngày/kỳ · kỳ thiếu *(AC-4)*
- DR3: **192/192** (thực thể, kỳ) có ≥ 1 ô ⇒ `CHUA_CO_DU_LIEU = ()` *(mong khai, Đ5)*. Dải `202401…202512`; **⛔ có 2026** ở tab này.
- DR2: ngày 01→30/11/2026 **31/31** cột có dữ liệu *(gồm `AK`)*. `chua_co_du_lieu` = **`hr@2026-H2` · `hr@2026-Q3` · `hr@2026-Q4`** *(3 cột số người 2026 không có ô nào)*. Bố cục luỹ kế **⛔ có cột `2026-M07…M12`** *(6 kỳ không có cột — khác với "cột có mà 0 ô", ghi ở đây, ⛔ ảnh)*.

## 4 · CHECK IX.PL trên chính đáp án *(AC-2)*
*Phép ①* `NB = 0` · *phép ②* `NIS+INT+PIT+COM = CXA+GAH+DC+MC`. Dung sai `TOL`: DR3 **0,5 VND** · DR2 **1e-9 mUSD** *(Giả định ②)*; ô rỗng/chữ/lỗi ở dòng của phép ⇒ kỳ **⛔ đo được** *(có tên, ⛔ coi đạt)*. `mong` khai theo khối ở `MONG_CHECK` của khuôn *(đo lần đầu 20/11, rồi khai)*.

| | kỳ-khối đo được ② | **đạt ②** | ⛔ đạt ② | ⛔ đo được ② | đo được ① | `NB ≠ 0` ① |
|---|---|---|---|---|---|---|
| **DR3** *(192 kỳ-thực thể)* | **29** | **14** | **15** | 163 | 168 *(+24 `CHECKING` NB trống)* | **12** |
| **DR2** *(155 ngày-khối + 160 kỳ-luỹ-kế)* | **315** | **267** | **48** | 0 | 315 | **119** |

**DR3 — kỳ ⛔ đạt ②** *(kỳ · chênh VND = vế trái − vế phải)*: `Group@202410`=145.298.916 · `202411`=775.085.821 · `202412`=−2.079.550 · `202501`=−432.428.076 · `202502`=−818.524.347 · `202503`=506.642.500 · `Headquarters@202411`=205.622.500 · `202412`=3.837.952.354 · `202501`=3.990.082.885 · `202502`=3.582.996.844 · `202503`=4.882.706.764 · `202504`=4.482.553.322 · `202505`=4.826.358.961 · `202506`=4.820.715.416 · `202507`=125.000.000. **`NB ≠ 0`** *(12)*: `Group@202405 · 06 · 11 · 12 · 202501 … 08`.
- ⛔ đo được ② ở DR3 = chỉ **6/24 kỳ `Group`** + **23/24 `Headquarters`** có đủ 8 dòng HR+chi phí; 6 thực thể còn lại *(VisionLab · TeraSofts · SuperMinds · Astronex · IOs · CHECKING)* **0 kỳ** *(dòng NIS·INT·PIT·COM rỗng)*. **`Group@202510` ⛔ đo được vì 2 ô CHỮ** `AF87` *(NIS)* · `AF89` *(PIT)* dạng `7.252.699.436`/`941.719.401` *(dấu chấm nghìn)* ⇒ ⛔ ép số, ghi nguyên ở phụ `o_chu_so` — **Đ3: ô không "đạt", ô "không đo được"**.

**DR2 — kỳ ⛔ đạt ②** *(chênh mUSD, 4 chữ số)*:
`ngay:GROUP` *(6)*: 2026-11-02=−0,1081 · 11-03=−0,0020 · 11-05=−0,0641 · 11-09=−0,0128 · 11-10=−0,0555 · 11-11=−0,2906 · `ngay:SGO2` *(1)*: 11-10=−0,0553 · `ngay:SGO1` *(1)*: 11-09=−0,0128 · `ngay:HGO2` · `BGO2`: 0.
`luy_ke:GROUP` *(32/32)*: 2025-Y=−3,8143 · 2025-H1=−1,6289 · 2025-H2=−2,1854 · 2025-Q1=−0,6992 · Q2=−0,9297 · Q3=−1,1131 · Q4=−1,0723 · M01…M12 = −0,2032 −0,2472 −0,2487 −0,3651 −0,2567 −0,3078 −0,3889 −0,3933 −0,3309 −0,4672 −0,2957 −0,3095 · 2026-Y=−4,3983 · H1=−2,2304 · H2=−2,1678 · Q1=−1,1093 · Q2=−1,1211 · Q3=−1,2302 · Q4=−0,9377 · M01…M06 = −0,3917 −0,3464 −0,3712 −0,4215 −0,3501 −0,3496 · `luy_ke:SGO2` *(4)*: 2026-Y=−0,1345 · H2=−0,1345 · Q3=−0,0632 · Q4=−0,0713 · `luy_ke:SGO1` *(4)*: 2026-Y=−0,0640 · H2=−0,0640 · Q3=−0,0512 · Q4=−0,0128 · `HGO2` · `BGO2`: 0.
**DR2 `NB ≠ 0`**: ngày 8 *(GROUP 11-04·05·09·10·11 · SGO2 11-10 · SGO1 11-04·10)* · luỹ kế 111 *(GROUP 32/32 · SGO2 25 · SGO1 31 · HGO2 11 · BGO2 12)*; danh sách đầy đủ = `MONG_CHECK` của `daily_report_2.py`.
- **Đây là SỐ LIỆU AS-IS của sổ, ⛔ lỗi đọc** — đáp án khai nguyên; H14 phải so với đáp án này *và* gắn nhãn "CHECK ⛔ đạt ở nguồn" cho các kỳ trên. Khuyến nghị BA: phép ① của IX.PL chỉ khẳng định được ở DR2 ngày `HGO2·BGO2` *(0 lệch)* và 156/168 kỳ-thực thể DR3.
- **Chứng minh ĐỎ** *(AC-2)*: đột biến 1 ô ở ảnh thật `daily_report_3.json` *(`CXA × headquarters_202508` +1)* ⇒ `4 failed, 24 passed` *(`test_AC2_check_so_ky_dat…[daily_report_3]` · `…liet_ke_15_ky…` · hai bài PHA)*; trả nguyên ⇒ `28 passed`. Bài PHA tự phá trong bộ nhớ: `CXA`/`DC` +1000/+1 · `NB` 0→1 · `MC` → `#REF!` · xoá cả cột ngày · tập rỗng · `MONG_CHECK` rỗng — **đều ĐỎ**.

## 5 · Ô chỉnh tay `AH12` *(AC-3)* · ô lỗi *(AC-5)*
- **ATL `AH12`** *(tab `Report I PLA3 Y H Q M | PM + HR | ATL`, PD 606)* đọc `valueRenderOption=FORMULA`: **`='Report I PLA3 Y H Q M | PM + HR'!AH12-0.5`** — ô chỉnh tay "− 0,5". Cột ATL `AH` = `y2025_m02` ở ảnh `atl.json`, hàng sheet `12` *(có thật, số)*. Ghi ở **phụ `o_chinh_tay` của ảnh DR3**: `ten = chinh_tay_ATL_AH12`, `o = AH12`, `cot_anh_atl = y2025_m02`, `dong_sheet_atl = 12`, `cong_thuc` nguyên văn. ⛔ config. *(Đ1: ở tab Sign off, `AH12` là ô RỖNG và tab có **0** ô công thức — đo 28.697 công thức ở DR2, 0 ở DR3; ⇒ chỉnh tay nằm ở ATL, ⛔ ở DR3.)*
- **Ô lỗi Sheets: 0** ở cả 194 cột giá trị DR3 và 32 cột DR2 *(`o_loi = []`; `loi_mong` khai `0` RÕ RÀNG mọi cột, luật `DT5-R1-04`; `#REF!`/`#N/A` lọt ⇒ ĐỎ)*. Ô chữ ≠ lỗi: **2** *(§4, `AF87`·`AF89`)*; ô `-`: 0.

## 6 · Đối chiếu A-CCR (D5) — DR2 *(số ô, ⛔ ảnh thứ ba)*
`5. Daily Report 2` bản CF report ↔ bản A-CCR `A1:AR1114`: **27.446** ô khớp · **1.120** ô lệch *(1.089 lệch > 1e-9 · 31 lệch ≤ 1e-9)* trên **231/958** hàng *(gồm hàng 1: `C1` hôm nay, cờ bool)*. DR3: bản A-CCR `5. Daily Report 3` **1940 × 40** khác bố cục với Sign off **137 × 203** ⇒ ⛔ so từng ô được *(thiếu khoá ghép đã đo)* — ghi ở "Giả định" ③.

## 7 · Công thức hàng mẫu *(nguyên văn; Đ4: hàng sheet · cột)*
DR2 *(28.697 ô công thức ở `A1:AL958`; 0 `ArrayFormula`)*: `G13` *(GI, ngày)* = `=SUMIFS('Report I CFA1 Daily'!$CA8:8,'Report I CFA1 Daily'!$CA$5:$5,G$5)` · `G37` *(CXA)* = `…$CA32:32…` · `G53` *(NIS)* = `…$CA48:48…` · `G60` *(NB)* = `…$CA55:55…` · luỹ kế `G430` *(GI)* = `='Report I CFA1 Y H Q M'!Z8` · `G470` *(NIS)* = `…!Z48` · `G477` *(NB)* = `…!Z55`. DR3 Sign off: **0** công thức.

## 8 · Việc đã làm
| Tệp | Nội dung |
|---|---|
| `tools/khuon_dong_bang/daily_report_2.py` · `daily_report_3.py` · `_daily_report.py` *(mới, ⛔ khuôn cũ)* | mỗi ảnh một khuôn riêng + thân CHECK chung; `MONG_*` khai theo khối |
| `tests/fixture/dap_an/daily_report_2.json` · `daily_report_3.json` | 2 ảnh |
| `tests/du_lieu/test_dap_an_report.py` | **28** bài |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | `MONG_PYTEST_TOAN_BO` **4.267 → 4.297** *(= số thu thập; Q8)*; web 681 giữ |
- **⛔ sửa `tools/dong_bang_sheet.py`: KHÔNG**; 22 ảnh cũ đúng từng byte *(sha ghim ở `test_AC6_anh_cu…`)*.
- **ĐỎ trước** *(đỏ vì THIẾU ảnh)*: `pytest tests/du_lieu/test_dap_an_report.py` ⇒ **exit 1** · `2 failed` *(lệnh: `python -m pytest tests/du_lieu/test_dap_an_report.py` · exit **1** · `FAILED …[daily_report_2]` · `FAILED …[daily_report_3]`)* ⇒ sau khuôn + ảnh: `28 passed`.
- `python tools/quet_pii_repo.py`: **[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp**.

## 9 · Cổng cuối
- `--duong-nen --cong 5444` **lần 1 ĐỎ**: `13 failed · 4268 passed` — **THÊM 1** `tests/canon/test_o_loi.py::test_CHI_MOT_BAN_KHAI_trong_ca_he` *(hai khuôn mới tự viết `startswith("#")`)* ⇒ sửa dùng `fls.canon.o_loi.la_o_loi` *(commit `f1ad615`; ảnh sinh lại đúng từng byte)*.
- **Lần 2 (một mình): KẾT ĐẠT** — toàn bộ `12 failed · 4269 passed · 2 xfailed · 14 errors` = tập đỏ nền 28 = 28 node id *(thêm 0 · bớt 0)*, chạy **4297** bài *(mong ≥ 4297; skipped 0 · deselected 0)*; `tests/web` `3 failed · 678 passed` = nền 3 = 3, chạy 681.
- `lint-imports`: 11 kept · 0 broken. `kiem_tai_lieu.py`: ĐẠT. `quet_pii_repo.py`: 0. Bản thô `/tmp/dt11` xoá sau commit.

## 10 · Giả định *(chỗ mơ hồ ngoài WO ⇒ phương án hẹp nhất)*
① **Chỉ 2 ảnh** như WO *(`daily_report_2` · `daily_report_3`)*; PD 607–609 · 614–616 *(5 tab + 3 tab A-CCR)* ⛔ đóng băng. *Khuyến nghị:* nếu H14 cần ảnh cho bản `[FS1]`/`[FS2]`/`5. Daily Report 3` (PD 607–609) hoặc A-CCR, mở WO riêng — cùng khuôn.
② **Dung sai**: DR3 0,5 VND, DR2 1e-9 mUSD *(đo: ở DR3 mọi ngưỡng 0…1000 cho cùng 14 đạt; DR2 chênh lớn nhất 4,40 mUSD ⇒ không do làm tròn)*. Đổi dung sai ⇒ sửa `TOL` + `mong`.
③ **A-CCR DR3** *(`5. Daily Report 3` 1940×40)* ⛔ so ô với Sign off *(bố cục khác)*; chỉ DR2 so được.
④ **2 ô chữ-số** `AF87` `AF89` ⛔ ép số *(dấu chấm nghìn kiểu VN, ⛔ chắc là VND nguyên hay nghìn)* ⇒ kỳ `Group@202510` **⛔ đo được ②**. *Khuyến nghị:* chủ xác nhận/định dạng lại hai ô trước khi H14 đòi kỳ này.
⑤ **Hình ảnh DR2 gộp 3 chế độ** *(`ngay` · `luy_ke` · `hr`)* trong MỘT ảnh, khoá hàng sheet + cột `che_do·khoi` — bám "theo (dòng PL, ngày/kỳ)" bằng bảng `tieu_de`; cột `AK` *(ngày 31, ⛔ nhãn ngày)* giữ nguyên tên `ak`.
⑥ `AH12` đặt ở ảnh **DR3** *(P&L)* dù ô nằm ở tab ATL; ⛔ thêm vào DR2.
