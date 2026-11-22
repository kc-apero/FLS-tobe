# BG-282 — bàn giao WO-281 · ISP 3.1.2 · DT7b: ảnh ĐẦU VÀO PLA (GL sổ P&L + HR For PL Report) cho H8

| | |
|---|---|
| **Phiếu** | trả `WO-281` *(DT7b, làn DATA)* |
| **Bởi** | phiên cloud `fls-dev #DATA` · cụm PG **5437** · nhánh `isp/DT7B` · 2026-11-22 |
| **Nền** | `2799bbe` · commit ① mã+bài+ảnh *(sha ở tin nhắn cuối)* |
| **Dải phiếu** | `KQ-283` (R1) · `KQ-284` (R2). Số trống kế tiếp: **285** |

## 0. Kết luận
AC-1…AC-6 đạt. **Cột nguồn của `DE`/`BM` nằm CÙNG tab, CÙNG sổ P&L, ⛔ PII** ⇒ không dừng. Hai ảnh mới *(khuôn mở rộng, ⛔ chép)*:
`tests/fixture/dau_vao/gl_pl_dau_vao.json` — **7.883** hàng × 11 cột *(2,75 MB)* · `…/hr_pl_dau_vao.json` — **13.356** hàng × 8 cột *(3,30 MB)*.
**AC-4: 371/371 ô GL ↔ 414 và 119/119 ô HR ↔ 416 KHỚP, 0 lệch.** Mọi ảnh cũ đúng từng byte *(6 sha ghim)*. ⚠ Hai phát hiện cho H8 ở §2.

## 1. Công thức nguyên văn *(AC-1 — FORMULA, chỉ-đọc, 22/11)*
**GL `DE`** — `DE10` là `ArrayFormula` TRÀN: `DE11…` đọc FORMULA ra rỗng *(vd `DE3000`: giá trị `45870`, công thức rỗng)*:
```
DE10: =ArrayFormula(DATE(left(AH10:AH,4),RIGHT(AH10:AH,2),1))
```
⇒ `DE` = **ngày MÙNG 1** của tháng `yyyymm` ở cột **`AH`** *(hàng 7–8: `AH` = "Thời điểm bắt đầu sử dụng dịch vụ" · `Final`)*. `AH10/11/3000/5487/7000` đọc FORMULA đều là **HẰNG dán** *(`202410`, `202410`, `202508`, `45962`, `202603`)*.
**⚠ Trong dữ liệu hiện tại KHÔNG có hàng nào `DE` ≠ ngày 1** *(7.574/7.574 `DE` số đều là mùng 1; ⛔ "2 ô ngày ≠ 1" mà phiếu yêu cầu **không tồn tại**)*. Con số "454/1.227 ô ≠ 0 ở ngày ≠ ngày 1" của H8 là phép dựng lại từ ITL Ledge *(`svc_start`)*, ⛔ phải `DE` của sổ — `DE` luôn mùng 1, chỉ **tháng** (`AH`) mới khác tháng `A`.
**HR `BM`** — cùng một công thức ở `BM10` · `BM11` · `BM2000` · `BM5000` *(chỉ khác chỉ số hàng)*:
```
=if(BK10="","" ,if(and(BL10=2024,BK10=11),DATE(BL10,BK10,1),if(and(BL10=2024,BK10=12),DATE(BL10,BK10,1),DATE(2025,BK10,1))))
```
Nguồn: **`BK10` = `=ArrayFormula(AH10:AH)`** *(tháng PL start, 1…12; `AH` cùng tab)* · **`BL10` = hằng `2024`** *(năm; `2024` ×1.375 · `2025` ×11.981)*. Quy tắc: tháng 11–12 của `BL = 2024` giữ 2024; **mọi trường hợp khác ⇒ năm 2025**. ⛔ `BM` ⛔ phải ngày của cột `A`.
**Tái dựng chứng minh bằng ĐO** *(bằng chứng DƯƠNG, cổng `thieu_lac` + bài)*: GL `DE = DATE(AH//100, AH%100, 1)` **7.574** hàng khớp + **309** hàng `AH` rỗng ⇒ `DE = #NUM!` *(`DATE(-29…)`)*, **0 lệch**; HR `BM = f(BK,BL)` **13.356/13.356**, 0 lệch.

## 2. Nguồn · hình ảnh *(AC-2 · AC-3 — mỗi số kèm nhãn, Đ4)*
Sổ P&L `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g`, đọc 22/11 ~04:55Z, `UNFORMATTED_VALUE` + `SERIAL_NUMBER`; bản đồ cột bằng hàng tiêu đề 7–8 TRƯỚC.
| Ảnh | Tab | Vùng · hàng dữ liệu | Cột |
|---|---|---|---|
| `gl_pl_dau_vao` | `Report I General Ledger` | hàng **10…7892 = 7.883** *(liên tục; cột `A` là số ở 7.883/7.883)* | `A·D·E·F·P·R·V·AH·BR·BS·DE` |
| `hr_pl_dau_vao` | `Report I H1000 Ledge (HR Allocate HD) Y2025 \| For PL Report` | hàng **10…13365 = 13.356** *(mọi hàng có `V`; `A` rỗng ở **2.571**)* | `A·P·V·BK·BL·BM·BA·BB` |
**GL theo kỳ cột `A`** *(20 kỳ, = `phan_bo_ky` ± 4 kỳ lệch có tên của 406, GỌI không chép)*: 2410=6 · 11=3 · 12=6 · 2501=748 · 02=283 · 03=297 · 04=332 · 05=408 · 06=350 · 07=549 · 08=537 · 09=501 · 10=487 · 11=477 · 12=566 · 2601=471 · 02=439 · 03=584 · 04=600 · 05=239. Cùng khoá hàng với `gl_406_dau_vao`: `dong_sheet·D·E·F·R·kỳ(A)` **0 lệch** *(bài `test_AC2_mo_rong_406_khong_lech`)*.
**HR theo kỳ PL `BM`** *(14 kỳ, ghim `MONG_KY_BM_THAT`; số hàng / trong đó có `A`)*: 2411=726/726 · 2412=649/649 · 2501=879/879 · 02=902/902 · 03=792/792 · 04=919/919 · 05=921/921 · 06=1.364/798 · 07=1.094/759 · 08=1.604/1.282 · 09=1.076/538 · 10=828/552 · 11=795/530 · 12=807/538. ⚠ **`A` rỗng chỉ rơi ở kỳ 06…12**, `BA`/`BB` rỗng CÙNG hàng ⇒ SUMIFS bỏ qua; tháng `A` ≠ tháng `BM` ở **7.578/10.785** hàng có `A`.
Khai có tên *(`mong`, Đ5)*: GL `AH` rỗng **309** · `DE` lỗi **309** `#NUM!` *(phân bố ghim)* · `AH` lạ **6** hàng sheet `5487·5556·5557·5634·5712·7098` *(serial/`yymmdd` thay `yyyymm` ⇒ `DE` vô lý: 986553 · 265168 · 257863 · 228613 · 257922; ⛔ sửa — khai y nguyên)* · `R` lỗi `#N/A ()` **4** · `D` rỗng **6** · `V` rỗng **3** · `P`: 18 giá trị *(gồm `Cash Treasury` có/không dấu cách đuôi ×537/×3 và `#N/A ()` ×4)*; `V` = 37 mã, **3 biến thể `ITE`** *(`ITE | Interest` · `ITE | ITE Interest` · `ITE | ITE Interest ` — chỉ biến thể khớp nhãn hàng PLA mới vào đáp án)*. Ngoài vùng dữ liệu: GL **208** hàng *(đọc tới hàng 8100)* có nội dung ở các cột đã đọc — `DE` đã đo kéo tới hàng 8000 ⇒ `#NUM!` — ⛔ vào ảnh; HR **35** hàng *(đọc tới 13400)* có nội dung ngoài cột `V` *(`BL` kéo tới hàng 20000)* — ⛔ vào ảnh.
Cỡ ảnh *(luật `DT4-R1-07`: > 2 MB ⇒ khai)*: GL **2,75 MB** · HR **3,30 MB** *(JSON thụt lề, mỗi ô một khoá — cùng nguyên nhân DT7; ⛔ nén được mà không sửa công cụ chung)*. ❓ orchestrator: chấp nhận.

## 3. Đối chiếu AC-4 *(CHỈ ĐO — ⛔ đầu vào; bài `test_AC4_*`)*
Khoá `(mã HD, ngày)`; so Σ trên ảnh mới với ô `la` *(40 mã)* khối `GROUP`; dung sai |Δ| ≤ 1e-6 mUSD; nhãn khớp = `<mã> | <tên>` đúng chuỗi *(không phân biệt hoa thường — như `SUMIFS`)*. **Mẫu số trước (Đ3)**: tập 40 mã `la` khác rỗng; 496 ngày.
| | GL ↔ 414 `pla1_daily` | HR ↔ 416 `pla3_hr_daily` |
|---|---|---|
| Ô `la` GROUP ≠ 0 của đáp án *(mẫu số đáp án)* | **371** | **119** |
| Ô `(mã HD, ngày)` có Σ ≠ 0 ở ảnh vào | 446 *(trong đó 74 ngoài lưới 496 ngày — tháng ≤ 2024-10 hoặc ≥ 2026-03)* | 127 *(0 ngoài lưới)* |
| Ô so *(hợp hai tập, trong lưới)* · trong đó có số ≠ 0 | 372 · **371** | 127 · **119** |
| **Khớp** · **lệch có tên** | **371** · **0** | **119** · **0** |
| Hàng ảnh KHÔNG vào phép *(V không là nhãn `la`, hoặc `DE` = `#NUM!`)* | 360 *(= 309 `DE = #NUM!` + 51 hàng `DE` số mà `V` rỗng ×2 / không là nhãn `la` ×49 — đo: 7.523 hàng vào phép tính ra ô, 7.883 − 360)* | 0 |
⇒ Đáp án 414/416 **tái dựng đúng** từ đầu vào + `DE`/`BM` đọc từ sổ; **mọi ô đáp án ≠ 0 đều được ảnh vào tạo ra** *(khớp = mẫu số đáp án)*. **Cho H8:** khoá cộng là `(V, DE)` / `(V, BM)` *(⛔ `A`)*; `DE` ở hàng `AH` rỗng ⇒ ⛔ vào ô nào; hàng `AH` lạ cho `DE` ngoài lưới — phải loại như `SUMIFS` *(ngày không là cột trục)*.

## 4. PII *(AC-5)*
Bản đồ cột bằng hàng tiêu đề 7–8 TRƯỚC; chỉ đọc cột khai; ⛔ `B` Số chứng từ · `C` Diễn giải · `G…O` *(Tài khoản · Payment Type · Budget Code · CDT · ID Payee…)*; HR ⛔ thêm `H`. 0 `@`; 0 tên cột cấm; `D`·`P`·`R`·`V` là TẬP ĐÓNG *(chuỗi lạ ⇒ cổng ĐỎ, ⛔ in giá trị)*; không cột nào mang số tài khoản ⇒ **0** ô phải che. `python tools/quet_pii_repo.py` = `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` *(trước commit)*. Bản thô `/tmp/dt7b/` *(chmod 600)* **đã xoá** sau BG; ⛔ commit.

## 5. Bài · đột biến *(Đ5)*
`tests/du_lieu/test_dap_an_pl_dau_vao.py`: **22 bài** *(RED trước: `FileNotFoundError` — ảnh chưa có · ảnh GL/HR · tái dựng `DE`/`BM` · phân bố kỳ · PII · tái tạo lưới thô ⇒ đúng TỪNG BYTE · mở rộng 406 0 lệch · 6 sha ảnh cũ · AC-4)*. Ca phá — mỗi đột biến 1 ô ⇒ cổng ĐỎ: GL **5** *(`DE`+1 · đổi `AH` · `P` lạ · `V` là số · `#NUM!` thành số)* · HR **5** *(`BM`+31 · đổi `BK` · đổi `BL` · `P` lạ · `A` có mà `BA`/`BB` rỗng)*; trả nguyên ⇒ xanh *(bài tái tạo)*. 
**Q8:** sàn `MONG_PYTEST_TOAN_BO` **4351 → 4375** *(= số bài thu thập `pytest --collect-only`)* ở `tools/dung_moi_truong_isp.sh` + bài ghim `tests/test_dung_moi_truong_isp.py:423` cùng commit; web giữ 681.

## 6. Cổng
`--duong-nen --cong 5437` MỘT lần (một mình): **KẾT ĐẠT** — tập đỏ + XFAIL **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)*, chạy **4375** (mong ≥ 4375) · skipped 0 · deselected 0; `tests/web` **3 = 3**, chạy 681. `lint-imports` **11 kept / 0 broken** · `kiem_tai_lieu` ĐẠT *(426 tệp · 2.823 bảng · 922 ô ngày)* · `quet_pii_repo` ĐẠT. Ghi kho THẬT: `KHONG`.

## 7. Giả định · khuyến nghị
1. `DE` ở hàng `AH` lỗi/lạ giữ NGUYÊN *(chuỗi `#NUM!` · số vô lý)* — engine H8 phải bỏ như `SUMIFS` bỏ ô không bằng ngày cột trục; ❓ BA: 6 hàng `AH` serial là lỗi nhập liệu nguồn cần sửa ở sổ?
2. HR ảnh lấy **13.356** hàng *(mọi hàng có `V`)*, ⛔ chỉ 10.785 hàng có `A`: để H8 thấy cả 2.571 hàng `A` rỗng *(đóng góp 0)*.
3. Errata AP/phiếu: phiếu viết "2 ô `DE` ngày ≠ 1" — không có; ghi v3.1.3.

## 8. Vòng sửa sau R1 *(`KQ-283` — 0 CHẶN · 2 NÊN SỬA · 2 GHI NHẬN; người dùng đã duyệt)* — 22/11, `fls-dev #DATA`, cụm 5437
> Phần này **chỉ THÊM**. Nhánh `isp/DT7B` @ `d2afe2a` + gộp nhánh làm việc *(chỉ `TIEN_DO.md`, 0 xung đột)*. Ảnh cũ *(mọi ảnh ngoài 2 ảnh DT7b)* **đúng từng byte** *(6 sha ghim, bài `test_OLD_*`)*.

### 8.1 `DT7B-R1-02` — khoá khối CDT *(đọc FORMULA bằng SA chỉ-đọc, ⛔ tin mù tin nhắn bổ sung)*
**Bản đồ cột bằng tiêu đề TRƯỚC:** GL `AD` = hàng 7 `AA`=`=J7` *("Chủ dự toán (CDT1)")* · hàng 8 `Final`; HR `J` = "Chủ dự toán (CDT1)", `BP` = "CDT Correct", `BR:BS` ở HR = **bảng ánh xạ CHỮ** `BR11:BS28` *(14 ô `BR` gồm tiêu đề · 13 ô `BS` · **0 số**; đọc `BR1:BS13500`)*.
**Công thức nguyên văn** *(rút gọn tên tab HR = `H!`; mỗi nhóm đếm bằng chuẩn hoá chỉ số hàng/cột trên 12 khối × 2 hàng `la` × 496 cột)*:
```
416 GROUP   G8 (496/496 cột):  =SUMIFS(H!$BA:$BA,H!$BM:$BM,G$5,H!$V:$V,$F8)-SUMIFS(H!$BB:$BB,H!$BM:$BM,G$5,H!$V:$V,$F8)
416 HGO6    G282 (496/496):    …BA/BB…,H!$V:$V,$F282,H!$P:$P,$A$281)  ← khoá P = mã LE
416 SGO2    CA116 (424 cột CA…SH): BA−BB … H!$P:$P,$A$115      ·  G116 (72 cột G…BX): BR−BS … H!$P:$P,$A$115   ⇒ 0 (BR/BS chữ)
416 SGO1    như SGO2 (CA199 / G199, $A$198)
416 BGO2    CA366 (424): BA−BB … P=$A$365   ·  G366 (72): =SUMIFS(H!$BA…)-SUMIFS(H!$BS…)  ⇒ chỉ ΣBA
416 CDT ×6  CB454 (424): =SUMIFS(H!$BA:$BA,H!$BM:$BM,CB$5,H!$V:$V,$F454,H!$BP:$BP,A448)-SUMIFS(H!$BB:$BB,… ,H!$BP:$BP,A448)
            G449 (72): =SUMIFS(H!$BR:$BR,…,$F449,H!$J:$J,A448)-SUMIFS(H!$BS:$BS,…)  ⇒ 0
416 SHQ2     G947 / CB952 (496): =G8-SUMIFS(G$448:G$945,$F$448:$F$945,$F947)   ⇒ GROUP − Σ 6 khối CDT
HR  BP10:   =ArrayFormula(iferror(VLOOKUP(J10:J,$BR$11:$BS$28,2,FALSE),"SHQ2 | Headquarters2"))
414 CDT G449 (496/496): =SUMIFS(GL!$BR:$BR,GL!$DE:$DE,G$5,GL!$V:$V,$F449,GL!$AD:$AD,A448)-SUMIFS(GL!$BS:$BS,…)   ·  LE: GL!$P:$P,$A$115…  ·  SHQ2 = G8−SUMIFS(G448:G945…)
```
**Kết luận:** (1) **cột khối CDT HR = `BP`** *(nguồn `J` + bảng ánh xạ `BR11:BS28` cùng tab, ⛔ PII; mã nhóm)*; GL = **`AD`**; ⛔ `BR`/`BS` của HR *(tin nhắn bổ sung ghi `J`+`BR`+`BS` — SAI cho HR: `BR:BS` là chữ, SUMIFS = 0)*. (2) **72 cột đầu của 416 `G…BX` = 2024-10-20…2024-12-30 (kỳ `BM` 2411·2412)** còn là bản dán cũ `BR−BS` ⇒ `SGO2/SGO1/6 CDT` = 0, `SHQ2 = GROUP`, `BGO2` = ΣBA; từ `CA` (serial ≥ 45657) mọi khối `BA−BB`. Đo: **38** ô (6 khối CDT × mã `la` × kỳ 2411·2412) có Σ(BA−BB) theo `BP` ≠ 0 mà ô đáp án = 0 — engine H8 phải **tái hiện** quy tắc cột, ⛔ "sửa".
Ảnh mới *(khuôn, ⛔ sửa tay JSON)*: HR **13.356** hàng × **10** cột `A·P·V·BK·BL·BM·BA·BB·J·BP` *(4,56 MB; checksum `d6085f433469b7cc`; cũ 3,30 MB)* · GL **7.883** × **12** cột thêm `AD` *(3,15 MB; `94f794fdbb2c10ee`; cũ 2,75 MB)* — > 2 MB ⇒ khai *(`DT4-R1-07`, orchestrator đã chấp nhận)*. Cổng mới ở khuôn: `J` ∈ tập đóng 14 + rỗng · `BP` ∈ 7 · **`BP = tra(J)` 13.356/13.356** · `J` rỗng **114** · phân bố `BP` *(7 giá trị ghim)* · `AD` tập đóng **14 giá trị** *(gồm biến thể lệch dấu cách ×5, `SUMIFS` khớp chuỗi ⇒ rơi vào `SHQ2`)* + phân bố ghim. PII: `J`/`AD`/`BP` là mã nhóm/dự án *(0 tên người · 0 TK · 0 `@`)*; `quet_pii_repo` = 0.

**Đối chiếu đo (⛔ đầu vào; bài `test_R102_*`)** — Σ(BA−BB) theo `(khối, mã HD ở V, ngày BM)` ↔ ô `la` *(40 mã)*; mẫu số đáp án trước *(Đ3)*; dung sai 1e-6 mUSD:
| Khối | HR↔416: đáp án `la` ≠ 0 · ô so · khớp | GL↔414: đáp án `la` ≠ 0 · ô so · khớp |
|---|---|---|
| GROUP | 119 · 119 · 119 | 371 · 371 · 371 |
| SGO2 · SGO1 · HGO6 · BGO2 | **0 · 0 · 0** *(mẫu số = 0 là KẾT QUẢ: HR không có `P` = 4 mã ấy)* | 108·108 · 89·89 · 11·11 · 35·35 |
| CVL · COR · SHQ1 · CSM · CAH · ASA | 42 · 43 · 29 · 42 · 48 · 30 *(khớp hết)* | 45 · 77 · 154 · 38 · 49 · 5 *(khớp hết)* |
| SHQ2 *(dư)* | 117 · 117 · 117 | 316 · 316 · 316 |
| **Tổng** | **470 / 470**, lệch **0** *(trong đó 7 khối CDT = 351)* | **1.298 / 1.298**, lệch **0** |
⇒ "4.381 ô ≠ 0 ở 7 khối CDT" của R1 được **giải thích**: đo lại trên đáp án 416 = **4.457** ô ≠ 0 ở 7 khối *(= 351 `la` + 467 `tong` + 3.639 KPI; R1 ghi 4.381, chênh 76 không tái hiện được — không ảnh hưởng)*; **`la` 351 khớp 351/351** từ ảnh vào, còn `tong`/KPI là công thức cộng/chéo hàng trên `la` *(H8 tự cộng, ⛔ cần ảnh riêng)*. GL: 7 khối nhãn *(6 CDT + SHQ2)* = 684 ô `la` khớp 684/684 + 4 khối LE 243/243 *(`-03` đã đo ở R1)*.

### 8.2 `DT7B-R1-01` — `AH` bất thường = 8
Phép nhận dạng cũ `202000<AH<203000` sót hàng có THÁNG ∉ 1…12 nằm trong dải. Mới: `ah_la(AH) = ⛔(202000 < AH < 203000 ∧ 1 ≤ AH%100 ≤ 12)` *(hàm ở khuôn, bài gọi chung)*. Khai CÓ TÊN `MONG_AH_LA` = **8** hàng sheet: **669** *(tháng 27 ⇒ `DE` 2027-03-01)* · 5487 · 5556 · 5557 · 5634 · 5712 · **6230** *(tháng 14 ⇒ `DE` 2027-02-01)* · 7098; `DE` vẫn ĐÚNG công thức *(DATE tràn tháng)*, ⛔ sửa dữ liệu. `MONG_DE_KHOP` 7.574 giữ *(gồm 8 hàng)*. **Chữa Đ1:** câu "`AH` lạ **6**" ở §2 *(dòng 37)* là SAI — đúng là 8. Grep `docs/`+`tools/`+`tests/`+`fls/` *(22/11)*: còn **3** chỗ ghi "6" ở docs *(BG-282 §2 dòng 37 · sổ R1 `DT7B` ×2 — là BIÊN BẢN, giữ nguyên, Đ2)*; mã + bài đã đổi 6→8 *(`MONG_AH_LA`, `test_B1_gl_DE_tai_dung_tu_AH`)*.

### 8.3 Đỏ trước · đột biến · sàn
- **ĐỎ trước** *(chạy bài mới trên mã/ảnh cũ)*: **8 bài đỏ** — `test_B1_gl_DE_tai_dung_tu_AH` *(mong 8)* · `test_R101_AH_la_bat_thang_la` *(`G.ah_la` chưa có)* · `test_R101_cong_AH_la_do_khi_them_hang_la` · `test_R102_hr_co_J_BP` · `test_R102_gl_co_AD` · `test_R102_hr_vs_416_moi_khoi` · `test_R102_gl_vs_414_moi_khoi` · `test_R102_ca_pha_BP_J_AD_do`. Sau sửa **xanh** *(29/29 ở tệp bài)*.
- **Cổng mới chứng minh ĐỎ** *(Đ5, `test_R102_ca_pha_*` + `test_R101_cong_*`)*: HR đổi `BP` 1 ô · `J` thành chuỗi lạ · tên cột `J`→`Email Address`; GL `AD` chuỗi lạ · `AD` sang mã HỢP LỆ khác *(phân bố lệch)* · `AH` hợp lệ→`202513` *(`DE` giữ khớp ⇒ chỉ cổng "lạ" bắt)* ⇒ exit ≠ 0 cả 6; trả nguyên ⇒ xanh *(bài tái tạo từng byte `test_AC2_*`)*.
- **Sàn Q8:** `MONG_PYTEST_TOAN_BO` **4375 → 4382** *(= `pytest --collect-only` toàn bộ; +7 bài)* ở `tools/dung_moi_truong_isp.sh` + bài ghim `tests/test_dung_moi_truong_isp.py:423` cùng commit; web giữ 681.
- Bản thô `/tmp/dt7b2` *(chmod 600)* đọc bằng SA chỉ-đọc; chiếu về 9/12 cột cũ rồi chạy khuôn CŨ ⇒ **đúng từng byte** hai ảnh cũ *(GL `725fab7b8140c6af`, HR `71b0434574bba96f`)* — chứng minh lần đọc lại KHÔNG trôi. Đã xoá sau BG; ⛔ commit.

### 8.4 Ghi nhận · việc còn lại
`DT7B-R1-03` *(AC-4 thêm 4 khối LE)* · `DT7B-R1-04` *(khoá `V` = chuỗi đầy đủ, ⛔ mã `ITE`)* ⇒ **backlog** *(AC-4 mới ở §8.1 đã đo cả 12 khối; chuyển WO H8 ghi khoá `V` đầy đủ)*. ❓ BA/orchestrator: 72 cột 2024 của 416 là bản dán cũ *(lỗi nguồn P&L)* — H8 tái hiện hay đòi sửa sổ? Số trống kế tiếp: **285**.

### 8.5 Cổng *(sau vòng sửa)*
`--duong-nen --cong 5437` MỘT lần, một mình: **KẾT ĐẠT** — toàn bộ `12 failed · 4354 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4382** (mong ≥ 4382), skipped 0, deselected 0; `tests/web` **3 = 3**, chạy 681. `lint-imports` **11 kept / 0 broken**. `quet_pii_repo` = `0 chỗ · 0 tệp`. Ghi kho THẬT: `KHONG`.
