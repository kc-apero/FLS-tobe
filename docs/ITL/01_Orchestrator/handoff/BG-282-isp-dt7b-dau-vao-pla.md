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
