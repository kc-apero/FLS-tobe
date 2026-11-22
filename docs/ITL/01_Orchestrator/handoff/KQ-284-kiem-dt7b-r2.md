# KQ-284 — R2 CUỐI kiểm `WO-281` · `BG-282` §8 · DT7b *(ảnh đầu vào PLA cho H8)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN** *(+ `DT7B-R1-01` · `-02` xác nhận ĐÃ SỬA)*. Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT7B.md` (v0.2). Đo trên cây gộp thử `thu/DT7B` *(nhánh làm việc `a2ddb69` + `isp/DT7B` @ `8553ca6`, **0** xung đột)*, cụm `5447`. Khoá SA chỉ-đọc; bản thô chmod 600, đã xoá, ⛔ commit; ⛔ in giá trị ô.

| Việc | Kết |
|---|---|
| (1) Đọc lại FORMULA | `BP10` **khớp BG nguyên văn**; `BP11/500/13365` rỗng = TRÀN *(giá trị thô ≠ rỗng cả 3)*. `G` + `CB` của **6** khối CDT ở **416 và 414** *(24 ô)*: 416 `G` = `BR−BS` theo `$J` *(bản dán cũ)*, `CB` = `BA−BB` theo `$BP`; 414 `AD` cả hai — đúng BG |
| Ảnh ↔ thô `J·BP·AD·AH·DE` | HR **13.356** · GL **7.883** hàng, mẫu số > 0: lệch **0**; mẫu 600+600 khớp 600/600 |
| Ánh xạ `BR11:BS28` | **13** khoá chữ *(+1 ô tiêu đề `BR10` = 14 ô `BR`; ⛔ "14 khoá")* → **7** CDT; khớp hằng `BP_ANH_XA` đúng thứ tự; `BP=tra(J)` trên THÔ **13.356/13.356**; PII ở `J·BP·AD` = **0** `@` · 0 TK · mã nhóm/dự án |
| (2) Tái dựng ĐỘC LẬP 12 khối *(script riêng)* | HR↔416 **441/441**, lệch **0** *(GROUP **119** · 4 khối LE **0 = 0** là KẾT QUẢ · 6 CDT 234 · SHQ2 88)*; GL↔414 **1.296/1.296**, lệch **0** *(GROUP 371 · LE 243 · CDT 368 · SHQ2 314)* |
| ⭐ Chênh **76** ô | R1 **4.381** = ô \|v\| > 1e-9; dev **4.457** = `!= 0` chính xác. **76 ô = bụi dấu phẩy động** *(≤ 3,05e-16)*, **tất cả ở `SHQ2`** — **29** ở hàng `la` ⇒ SHQ2 `la` thật **88** ⛔ 117 · 7 khối CDT **322** ⛔ 351 · 12 khối **441** ⛔ 470; GL 2 ô ⇒ 314 ⛔ 316 · **1.296** ⛔ 1.298 *(`-R2-01`, GHI NHẬN: đối chiếu đúng, chỉ mẫu số bị thổi — Đ4)* |
| (3) `-01` 8 hàng `AH` | Đo độc lập *(⛔ yyyymm 2020…2029, tháng 1…12)* = đúng **8**: 669 · 5487 · 5556 · 5557 · 5634 · 5712 · 6230 · 7098; trong dải 202000…203000 mà tháng ∉ 1…12: **2** *(669 · 6230)*. `mong` 8 **hai chiều**: thêm hàng thứ 9 ⇒ ĐỎ · lạ → hợp lệ *(8→7, `DE` giữ khớp)* ⇒ ĐỎ |
| (4) Ảnh cũ · PII | **6/6** ảnh cũ đúng từng byte; `git diff tests/fixture` ↔ nhánh làm việc = chỉ 2 ảnh mới. `quet_pii_repo` = **0 chỗ · 0 tệp** trên cây gộp + 4 cây đầy đủ `git archive` *(`e7771a2` · `d2afe2a` · `48b7918` · `8553ca6`)* |
| (5) Đột biến mới | **6/6 ĐỎ**: 1 ô `BP` · xoá 1 khoá ánh xạ · `J` chuỗi lạ · 1 ô `AD` sang mã hợp lệ khác · `AH` lạ thứ 9 · `AH` lạ 8→7 |
| (6) Cổng | `--duong-nen --cong 5447` *(một lần, một mình)*: `12 failed · 4354 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4382** ≥ 4382; web **3 = 3**/681; `lint-imports` 11 kept / 0 broken; `kiem_tai_lieu` ĐẠT *(429 tệp · 2.831 bảng)* |

## GHI NHẬN ⇒ backlog *(⛔ chặn H8; ⛔ chặn gộp)*
- `DT7B-R2-01` mẫu số bụi dấu phẩy động ở SHQ2 *(`test_dap_an_pl_dau_vao.py:428` · `:383-384` · `:485` · `:497` · `BG-282` §8.1)*: thêm `abs(o) > 1e-9`, ghim lại 88/322/441 · 314/1.296.
- `DT7B-R2-02` chuỗi `nguon` ở 2 ảnh còn liệt kê cột cũ *(thiếu `J·BP` / `AD`)* — dữ liệu đúng, chỉ dấu vết nguồn lạc hậu.

## Cho H8
Ảnh đủ: GL *(`V·P·BR·BS·DE·AD`)* + HR *(`V·P·BA·BB·BM·J·BP`)*. **Quy tắc cột 416 H8 phải tái hiện:** 72 cột đầu `G…BX` (serial < 45657) là bản dán cũ — `SGO2/SGO1` = 0, 6 CDT = 0, `SHQ2` = GROUP, `BGO2` = ΣBA; từ `CA` mọi khối `BA−BB`. Khoá `V` = chuỗi đầy đủ *(⛔ mã `ITE`)*; `AD` biến thể lệch dấu cách rơi vào `SHQ2` *(SUMIFS khớp chuỗi)*. **Sàn cây gộp = 4.382**; nhánh làm việc thêm DT11 trước khi gộp ⇒ sàn tăng ⇒ gộp tay, đo lại. Số trống kế tiếp: **285**.
