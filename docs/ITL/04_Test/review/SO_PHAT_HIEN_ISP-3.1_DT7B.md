# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `DT7B` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.2 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-283` · R2 cuối `KQ-284`)* · **Nguồn:** `WO-281` · `BG-282` · nhánh `isp/DT7B` @ `915e0ae` *(R1)* → `8553ca6` *(R2)*

> **Luật của sổ:** sổ **chỉ THÊM**. Lớp: **A1** lỗi mã · **B1** lệch spec / thiếu bài · **B2** spec/ISP/hợp đồng sai. Mức: **CHẶN** · **NÊN SỬA** · **GHI NHẬN**.
> ⛔ **Riêng tư:** sổ chỉ ghi số đếm, địa chỉ ô và tên cột — ⛔ giá trị ô. Bản thô `/tmp` chmod 600, đã xoá, ⛔ commit.

## Số đo nền của R1 *(nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Đọc lại công thức bằng SA chỉ-đọc `FORMULA`: `DE10`, `BM10` + `DE11·3000·5487·7000·7892` + `AH10·11·3000·5487·5556·7000·7098` + `BM11·2000·5000·13365` + `BK10`·`BL10/11/2000` | 25 ô | **khớp BG nguyên văn**; `DE11…`/`BK11…` rỗng = phần TRÀN; `AH5487`=hằng `45962`, `AH7098`=hằng `260603` |
| Đọc lại cột bằng SA, so TỪNG Ô ảnh ↔ thô *(script riêng, ⛔ dùng khuôn)* | GL 7.883 × 11 = **86.713** ô · HR 13.356 × 8 = **106.848** ô | lệch **0 / 0**; mẫu ngẫu nhiên 500 hàng: 5.500 + 4.000 ô, lệch **0** *(mẫu số > 0)* |
| Số hàng | GL hàng 10…7892 · HR 10…13365 | **7.883** *(cột `A` là số ở 7.883)* · **13.356** *(`V` có ở 13.356; `A` rỗng 2.571)* — đúng |
| Tái dựng `DE = DATE(left(AH,4), right(AH,2), 1)` độc lập | 7.883 hàng | **7.574** số *(7.566 `AH` yyyymm hợp lệ + 8 hàng `AH` bất thường)* + **309** `#NUM!` *(`AH` rỗng)* = **7.883**, lệch **0**; `DE` số ≠ mùng 1: **0** |
| Tái dựng `BM = f(BK, BL)` độc lập | 13.356 hàng | khớp **13.356/13.356**; `BL`: 2024 ×1.375 · 2025 ×11.981; 14 kỳ `BM` = BG từng số |
| Ngoài vùng *(đọc tới 8100 / 13400)* | GL `DE` · HR `BL` | **208** · **35** hàng — khớp BG, ⛔ vào ảnh |
| AC-4 độc lập GL↔414 *(khối `GROUP`)* | ô `la` ≠ 0 của 414 = **371** | **371/371** khớp, lệch 0 — **chỉ khi** `V` khớp NHÃN `ITE \| Interest`; lọc theo MÃ `ITE` ⇒ 359/374 |
| AC-4 độc lập HR↔416 *(khối `GROUP`)* | **119** | **119/119**, lệch 0 |
| Khối khác đo được ở 414 *(chọn `P` = LE)* | `SGO2` 108 · `SGO1` 89 · `HGO6` 11 · `BGO2` 35 = **243** ô ≠ 0 | **243/243** khớp *(`DT7B-R1-03`)* |
| Khối CDT của 416 *(7 khối `CVL…SHQ2`)* | **4.381** ô ≠ 0 | ảnh HR **không có cột CDT**; thử `BP` (CDT Correct) thô ⇒ khớp **312/4.381**, `J`/`AA` **35/4.381** *(`DT7B-R1-02`)* |
| PII | ảnh · 2 commit | cột GL `A·D·E·F·P·R·V·AH·BR·BS·DE`, HR `A·P·V·BK·BL·BM·BA·BB`; **0** `@`, **0** cột `B·C·G…O·H`; tên cột cấm chỉ xuất hiện trong chú thích loại trừ; `quet_pii_repo` cây gộp + từng commit *(`e7771a2`, `915e0ae`, `git archive`)* = **0 chỗ · 0 tệp** |
| Ảnh cũ | `git diff` nền ↔ `isp/DT7B` | thêm 2 ảnh + 2 khuôn + 1 bài; sửa 2 tệp sàn; ảnh/khuôn cũ đổi byte **0** |
| Đột biến *(bản sao `git archive`, trả nguyên)* | **10** | **10/10 ĐỎ**: GL `DE`+1 · xoá 1 hàng · `BR`+1 · thêm cột `C` · `AH` rỗng→`202501`; HR `BM`+31 · xoá hàng · `BL` 2025→2024 · thêm cột `Email Address`; `MONG_GL` 7883→7884. Trả nguyên ⇒ 22 xanh *(lưu ý: đổi hằng cùng cỡ phải xoá `__pycache__`, lần đầu pyc cũ che)* |
| `--duong-nen --cong 5447` *(một lần, một mình)* | toàn bộ · `tests/web` | `12 failed · 4347 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4375** ≥ 4375, skipped 0; `tests/web` **3 = 3**, 681 |
| `lint-imports` · `kiem_tai_lieu` | — | **11 kept / 0 broken** · ĐẠT *(427 tệp · 2.826 bảng · 922 ô ngày)* |
| Xung đột gộp thử | `thu/DT7B` = nhánh làm việc `fd064b1` + `isp/DT7B` | **0** xung đột; sàn = thu thập thật = **4.375** *(tổng 12+4347+2+14)* |

## Số đo nền của R2 cuối *(`KQ-284`, `isp/DT7B` @ `8553ca6`; nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Đọc lại công thức bằng SA chỉ-đọc `FORMULA` | `BP10` · `BP11` · `BP500` · `BP13365` *(HR)* · `G` + `CB` của **6** khối CDT ở **416** và **414** *(24 ô)* | `BP10` = `ArrayFormula(iferror(VLOOKUP(J10:J,$BR$11:$BS$28,2,FALSE),…))` **khớp BG nguyên văn**; `BP11/500/13365` rỗng ở FORMULA = phần TRÀN *(giá trị thô ≠ rỗng cả 3)*. 416 `G` = `SUMIFS($BR,…,$BM,…,$J,A{khối})−SUMIFS($BS…)`, `CB` = `SUMIFS($BA,…,$BP,A{khối})−SUMIFS($BB…)`; 414 `G` **và** `CB` = `$BR/$BS` + `$AD` — đúng BG; ⛔ `G8` ở `SHQ2`: 416 `CB952` = `CB13−…` *(hàng GROUP cùng nhãn, BG chuẩn hoá về `G8`)* |
| Ảnh ↔ thô, cột `J`·`BP`·`AD`·`AH`·`DE` *(+ `BA·BB·BM·BK·BL`)* | HR **13.356** hàng · GL **7.883** hàng — mẫu số > 0 | lệch **0 / 0** *(toàn bộ hàng, không chỉ mẫu)*; mẫu ngẫu nhiên 600 + 600 hàng khớp **600/600** · **600/600**; hàng có dữ liệu ngoài ảnh: **0** |
| Bảng ánh xạ `BR11:BS28` *(đọc thô)* | **13** khoá chữ ở `BR11:BR23` + **1** ô tiêu đề `BR10` *(= 14 ô `BR`)* · 13 ô `BS` · **0** số | khớp hằng `BP_ANH_XA` **đúng thứ tự + nội dung**; **7** CDT đích; `BP = tra(J)` trên THÔ **13.356/13.356**; `J` rỗng thô **114**; `BP` ngoài 7 CDT **0** |
| PII ở `J`·`BP`·`AD` | 14 · 7 · 14 giá trị khác nhau | **0** `@` · **0** chuỗi ≥ 6 chữ số liên tiếp · mọi giá trị là mã nhóm/dự án *(chuẩn hoá dấu cách ⇒ 9 + 6 biến thể ⇒ ⛔ tên người/TK)* |
| Tái dựng ĐỘC LẬP 12 khối từ ẢNH ↔ ô `la` của 416/414 sống *(script riêng, ⛔ hàm khuôn; 40 hàng `la` × 496 cột × 12 khối)* | HR **238.080** ô · GL **238.080** ô | HR↔416 **441** ô \|v\|>1e-9 *(GROUP **119** · 4 khối LE **0 = 0** là KẾT QUẢ · 6 CDT **234** · SHQ2 **88**)*, **441/441** khớp, lệch **0**; GL↔414 **1.296** ô, **1.296/1.296**, lệch **0** *(GROUP 371 · LE 243 · CDT 368 · SHQ2 314)* |
| ⭐ "4.381 vs 4.457" — chênh **76** | 7 khối CDT của 416, mọi hàng | **4.381** = ô \|v\| > 1e-9 *(R1 đếm, đúng)*; **4.457** = ô `!= 0` CHÍNH XÁC. **76** ô = **bụi dấu phẩy động** *(max 3,05e-16)*, **tất cả ở `SHQ2`** *(= GROUP − ΣCDT)*; trong đó **29** ở hàng `la` ⇒ SHQ2 `la` thật **88**, ⛔ 117 *(`-R2-01`)*. GL: 2 ô bụi ⇒ SHQ2 **314**, ⛔ 316 |
| `AH` lạ *(đo độc lập: ⛔ yyyymm năm 2020…2029 tháng 1…12)* | `AH` có giá trị **7.574** *(309 rỗng)* | **8**: 669 *(202527)* · 5487 *(45962)* · 5556 *(45962)* · 5557 *(262601)* · 5634 *(260601)* · 5712 *(252512)* · 6230 *(202614)* · 7098 *(260603)*; trong dải `202000…203000` mà tháng ∉ 1…12: **2** *(669 · 6230)*. Thêm 2 hàng `202311` *(2634 · 3935)* hợp lệ yyyymm, ngoài lưới 2024-10 *(không lạ; nằm trong `ngay_ngoai_luoi`)* |
| Ảnh cũ | 6 ảnh cũ: sha256 cây gộp ↔ nhánh làm việc | **6/6 đúng từng byte**; `git diff` `tests/fixture` ↔ nhánh làm việc = **chỉ 2 ảnh mới** |
| PII repo | `quet_pii_repo` cây gộp + **4** cây đầy đủ `git archive` (`e7771a2` · `d2afe2a` · `48b7918` · `8553ca6`; 1.165–1.168 tệp) + 6 commit riêng lẻ *(⛔ — chỉ ruột tệp đổi ⇒ tập 0–7 tệp ⇒ máy báo ĐỎ Đ3, bỏ, thay bằng cây đầy đủ)* | **0 chỗ · 0 tệp** ở mọi cây; `@` trong 2 ảnh **0**; `email` xuất hiện **1** lần/ảnh *(câu khai "không mang")* |
| Đột biến *(cây gộp thử, trả nguyên bằng `git checkout`)* | **6** | **6/6 ĐỎ**: HR 1 ô `BP` đổi CDT *(3 bài đỏ)* · xoá 1 khoá `BP_ANH_XA` *(`BP=tra(J)` 13.205/13.356 — 2 bài)* · HR `J` chuỗi lạ *(2 bài)* · GL 1 ô `AD` sang mã hợp lệ khác *(4 bài, gồm `gl_vs_414_moi_khoi`)* · hàng `AH` lạ **thứ 9** *(3 bài)* · hàng `AH` lạ **thứ 8 → hợp lệ** *(8→7, `DE` giữ khớp — 5 bài)*: `mong` **8 hai chiều**. ⚠ Lần đầu xoá khoá bằng `sed` sai ⇒ lỗi cú pháp *(đỏ NHẦM lý do)* — làm lại sạch rồi mới tính |
| `--duong-nen --cong 5447` *(một lần, một mình)* | toàn bộ · `tests/web` | `12 failed · 4354 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4382** ≥ 4382, skipped 0; `tests/web` **3 = 3**, 681; 674 s + 198 s |
| `lint-imports` · `kiem_tai_lieu` | — | **11 kept / 0 broken** · ĐẠT *(429 tệp · 2.830 bảng · 924 ô ngày · 104 mã QĐ)* |
| Xung đột gộp thử | `thu/DT7B` = nhánh làm việc `a2ddb69` + `isp/DT7B` @ `8553ca6` | **0** xung đột; sàn = thu thập thật = **4.382** *(12+4354+2+14)* — nếu nhánh làm việc thêm DT11 trước khi gộp ⇒ sàn tăng ⇒ gộp tay, đo lại |

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `DT7B-R1-01` | DT7B | R1 | B1 | NÊN SỬA | `tools/khuon_dong_bang/gl_pl_dau_vao.py:215` *(`202000 < ah < 203000`)* · `test_dap_an_pl_dau_vao.py:153-155` · `BG-282` §2 *("AH lạ 6")* | Phủ định thiếu *(Đ1)*: `AH` bất thường là **8** hàng, ⛔ 6. Thêm sheet **669** *(`AH` tháng `27`, `DE` = 2027-03-01)* và **6230** *(tháng `14`, `DE` = 2027-02-01)*: nằm trong dải `202000…203000` nên cổng "lạ" ⛔ bắt; cả hai có `BS` ≠ 0 và `V`; `DE` ở **ngoài lưới** 2024-10-20…2026-02-27 ⇒ `SUMIFS` bỏ. `DE` ảnh vẫn ĐÚNG *(DATE tràn tháng)*; lỗ ở khai/cổng. | Cổng bắt `AH` có tháng ∉ 1…12 hoặc ngoài `yyyymm` ⇒ `MONG_AH_LA` = 8, khai có tên; báo chủ sổ như 6 hàng kia *(⛔ sửa dữ liệu)*; cho H8: hàng DE ngoài lưới loại. | Cổng `AH_la` mong **8**; đột biến đổi tháng 27→07 ⇒ ĐỎ | Đã sửa *(R2 xác nhận, `KQ-284`)* |
| `DT7B-R1-02` | DT7B | R1 | B1 | NÊN SỬA | `hr_pl_dau_vao.json` *(cột `A·P·V·BK·BL·BM·BA·BB`)* ↔ `WO-277` AC-3 | Ảnh HR **thiếu khoá khối CDT**. 416 có 8 khối; ảnh chỉ tái dựng `GROUP` *(119 ô)*, còn **4.381** ô ≠ 0 của 7 khối CDT H8 không đối soát được từ ảnh này *(hr_ledger_2025 có `cdt1` nhưng khác tab, 10.105 ≠ 13.356 hàng, ⛔ khoá nối)*. Tab HR có `J`/`AA` (CDT1, 13.242 ô), `BP` "CDT Correct" (**13.356/13.356**, 7 giá trị), `R` ITL ID (211/13.356). Thử độc lập `BP` ⇒ 312/4.381, ánh xạ khối **chưa xác định** *(ghi đo, ⛔ kết luận)*. | Dev/BA xác định cột quyết khối CDT của 416 *(đo `BP`/`AA`/công thức cột `G` 416)*, thêm vào ảnh HR; hoặc BA xác nhận H8 chỉ cần `GROUP` cho HR. | Bài: ảnh HR có cột CDT; AC-4 HR theo khối | Đã sửa *(R2 xác nhận, `KQ-284`)* |
| `DT7B-R1-03` | DT7B | R1 | B1 | GHI NHẬN | `test_dap_an_pl_dau_vao.py` `test_AC4_*` · `MONG_AC4` | Mẫu số AC-4 chỉ khối `GROUP` *(371)*. Đo được thêm 4 khối LE ở 414 chọn `P`: **243** ô ≠ 0 *(`SGO2` 108 · `SGO1` 89 · `HGO6` 11 · `BGO2` 35)*, **243/243** khớp. | Thêm vào AC-4 *(backlog)* — mạnh hơn cho H8. | — | Mở |
| `DT7B-R1-04` | DT7B | R1 | B1 | GHI NHẬN | `BG-282` §2 *("3 biến thể ITE")* | Xác nhận độc lập: khoá cộng PHẢI là nhãn `V` đầy đủ; theo mã `ITE` gộp 3 biến thể (133 · 59 · 1 hàng) ⇒ GROUP 359/374 ⇒ lệch 12–15 ô. Chỉ `ITE \| Interest` ⇒ 371/371. | Ghi vào WO H8 / bài H8: khoá `V` = chuỗi đầy đủ, ⛔ mã. | — | Mở |
| `DT7B-R2-01` | DT7B | R2 | B1 | GHI NHẬN | `tests/du_lieu/test_dap_an_pl_dau_vao.py:428` *(`if o != 0`)* · `:383-384` *(`MONG_KHOI_HR` SHQ2 117 · `MONG_KHOI_GL` SHQ2 316)* · `:485` *(351 · 470)* · `:497` *(1298)* · `BG-282` §8.1 *(bảng + câu "4.457 = 351 la + 467 tong + 3.639 KPI")* | Đ4: cột "đáp án `la` ≠ 0" đếm bằng `!= 0` CHÍNH XÁC nên gồm **bụi dấu phẩy động** ở `SHQ2` *(= GROUP − ΣCDT; max 3,05e-16)*: HR **29** ô `la` *(tổng 76 ô ở mọi hàng — chính là chênh 4.457 ↔ 4.381)*, GL **2** ô. Con số "ô `la` ≠ 0" thật *(\|v\| > 1e-9)*: HR SHQ2 **88** ⛔ 117 · 7 khối CDT **322** ⛔ 351 · 12 khối **441** ⛔ 470; GL SHQ2 **314** ⛔ 316 · 12 khối **1.296** ⛔ 1.298. Đối chiếu KHÔNG sai *(441/441 · 1.296/1.296 lệch 0 theo tái dựng độc lập)*; chỉ mẫu số bị thổi và 31 ô bụi "khớp" tầm thường. | Thêm ngưỡng `abs(o) > 1e-9` ở `_khoi_so` + ghim lại 88/322/441 · 314/1.296; sửa BG câu 4.457 *(backlog, ⛔ chặn H8)*. | Số in lên nói đếm gì + ngưỡng *(Đ4)*; mẫu số có phép trừ ⇒ ngưỡng, ⛔ `!= 0`. | Mở *(backlog)* |
| `DT7B-R2-02` | DT7B | R2 | B1 | GHI NHẬN | `tests/fixture/dau_vao/hr_pl_dau_vao.json:4` · `gl_pl_dau_vao.json:4` *(trường `nguon`)* | Dấu vết nguồn cũ: `nguon` HR còn ghi cột `A·P·V·BK·BL·BM·BA·BB` *(thiếu `J·BP`)*, GL ghi `A·D·E·F·P·R·V·AH·BR·BS·DE` *(thiếu `AD`)* trong khi `cot` đã có đủ. Dữ liệu đúng *(`cot` + ảnh ↔ thô 0 lệch)*; chỉ chuỗi khai nguồn lạc hậu — chuỗi này do bản thô *(⛔ commit)* mang vào, sửa ở lần đọc kế tiếp. | Cập nhật chuỗi `nguon` khi đọc lại ảnh lần tới *(backlog)*. | — | Mở *(backlog)* |

## Ghi chú kiểm *(⛔ phát hiện)*
- Hai quyết orchestrator: 2 ảnh > 2 MB chấp nhận *(đã khai `DT4-R1-07`)*; 6 hàng `AH` serial/`yymmdd` giữ nguyên + khai có tên — ảnh KHAI đúng 6 *(`-01` bổ sung thêm 2)*.
- `BK10 = ArrayFormula(AH10:AH)` là `AH` của CHÍNH tab HR *(không phải `AH` tab GL)* — BG đúng.
- Đã đo `V`: GL 35 mã, HR 10 mã; các chuỗi `V` lạ ⇒ 0.

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `DT7B`, `KQ-283`)*: khởi tạo — **4** phát hiện `DT7B-R1-01…04` *(**0 CHẶN** · **2 NÊN SỬA** · 2 GHI NHẬN)*.
- **v0.2** *(2026-11-22, `fls-test` R2 cuối của `DT7B`, `KQ-284`)*: thêm bảng "Số đo nền của R2" + **2** phát hiện `DT7B-R2-01…02` *(**0 CHẶN** · **0 NÊN SỬA** · 2 GHI NHẬN)*; `DT7B-R1-01/-02` xác nhận ĐÃ SỬA *(8 hàng `AH` hai chiều · khoá `BP`/`AD` 12 khối lệch 0)*.
