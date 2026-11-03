# HOI-049 — `AC-13` đòi `title` **0** chữ số mà chuỗi spec mang `QĐ-ITL-122`; nút `Thử lại` `b tiny` ⟷ "cùng dáng `TT.chay`" *(lớp `b`)*

| | |
|---|---|
| **Thuộc** | `WO-045` |
| **Hỏi bởi** | `fls-dev` · 2026-10-05 |
| **Loại** | `MAU_THUAN` *(hai chỗ, mỗi chỗ một câu)* |
| **Trạng thái** | ✅ `DONG` *(`fls-ba` trả `TL-049` 05/10 — câu 1 + câu 2 phương án **1** = đúng điều Dev đã làm; spec đính chính `BA-06` **v4.21**; ⛔ vòng 2 `WO-045`; mục yếu ②③ ⇒ `WO-023` `(h)`, ⑤ ⇒ `GAP-SCR-35`)* |
| **Chặn** | `KHONG_CHAN` — `fls-dev` làm theo phương án ⭐ của từng câu, bàn giao trong `BG-048`; `fls-ba` đổi ý ⇒ một dòng mã + một dòng bài |

## Câu 1 — chữ số trong `title` thanh lằn

### Bằng chứng
- Chỗ 1: `WO-045` `AC-13` — *"`title` **cả hai** nút thanh lằn khớp `/[0-9]/` **0** lần"*; cùng ý `BA-06` v4.20 `§4.5 ⓦ` ③ *(`06_SCREEN_SPEC.md:755`)* — *"⛔ chữ số nào trong `title` hai nút thanh lằn"*.
- Chỗ 2: `BA-06` v4.20 `§4.5 ⓦ` ③ phương án ⓐ *(`06_SCREEN_SPEC.md:752`)* — `title` = `Lệnh chi đang chờ tiền — câu hỏi của việc (QĐ-ITL-122)` **nguyên văn** ⇒ chuỗi ấy mang **3** chữ số *(`1`, `2`, `2` của mã quyết định)*.
- Phép đo: `re.findall(r"[0-9]", "Lệnh chi đang chờ tiền — câu hỏi của việc (QĐ-ITL-122)")` ⇒ `['1', '2', '2']` *(3 chữ số, mẫu số 1 chuỗi)* — hai câu ⛔ thể cùng xanh nguyên văn.

### Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | Giữ chuỗi spec **nguyên văn**; vế *"0 chữ số"* đọc theo **ý** `ⓦ` ③ *("⛔ mang **số đo** cứng")* — bỏ **mã quyết định** `QĐ-ITL-<n>` rồi mới đếm chữ số *(bài `test_AC13_title_HAI_nut_KHONG_chu_so_ngoai_ma_quyet_dinh`, tự chứng: chuỗi cũ `1.345 …` ⇒ bắt `1345`)* | `AC-13` vế hai ⛔ còn nguyên văn — `fls-test` phải đọc bài để biết phép trừ mã QĐ | ⭐ |
| 2 | Bỏ `(QĐ-ITL-122)` khỏi `title` ⇒ `/[0-9]/` **0** nguyên văn | đổi chuỗi spec ⓐ *(spec đã chọn có mã)*; mất dấu vết quyết định trên chính nút | |

## Câu 2 — lớp nút `Thử lại` của `②b`

### Bằng chứng
- Chỗ 1: `BA-06` v4.19 `§4.5 ⓥ` ⑤ *(`06_SCREEN_SPEC.md:723`)* — *"lớp nút `b tiny` có sẵn — cùng dáng nút của khung `TT.chay` `trang_thai.js:78`"*; `WO-045` Phạm vi `(e)` — *"lớp `b tiny` có sẵn"*.
- Chỗ 2: `fls/web/tep/trang_thai.js:76` *(mã khi nhận `db0adae`)* — nút `Thử lại` của `TT.loi`: `b.className = 'b';` ⇒ lớp **`b`**, ⛔ `b tiny` *(và có `marginTop: 10px`)*. Hai vế của một câu chỉ hai dáng khác nhau.

### Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | `b tiny` *(chữ **lớp** spec + `WO` ghi hai lần; cùng lớp mọi nút nhỏ trong màn ghép — `nut('tiny', …)`)* | ⛔ cùng dáng với nút `Thử lại` của `TT.loi` *(nhỏ hơn)* | ⭐ |
| 2 | `b` *(cùng dáng `TT.chay`)* | trái chữ lớp spec + `WO` | |

---

# TL-049 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⭐ **Câu 1 — phương án 1** *(giữ chuỗi nguyên văn có `QĐ-ITL-122`; *"0 chữ số"* đếm **sau khi bỏ** mọi `QĐ-ITL-\d+`)*. Lỗi ở **chữ spec**, ⛔ ở mã: `ⓦ` ③ cấm **số đo cứng** — con số trôi khi sổ đổi *(`1.345` 09/09 ⟷ `/ro` `tong` **1.601** 05/10)*. Mã quyết định là **tên** một lời chốt, ⛔ trôi ⇒ giữ trên nút làm dấu vết. Bài `test_AC13_title_HAI_nut_KHONG_chu_so_ngoai_ma_quyet_dinh` đo **đúng** ý ấy *(tự chứng chuỗi cũ ⇒ `1345`)* — ⛔ đổi bài. ⭐ **Câu 2 — phương án 1** *(`b tiny`)*. Vế *"cùng dáng nút của khung `TT.chay` `trang_thai.js:78`"* là **lỗi viết spec** của `fls-ba` ở v4.19: nút `Thử lại` của `TT.loi` mang lớp **`b`** *(`trang_thai.js:76` — `fls-ba` đọc lại 05/10, `Đ1`)*. Chữ **lớp** thắng vì `②b` là **một danh sách trong màn ghép** — nút đứng cạnh các nút `nut('tiny', …)` khác; khung lỗi `TT.loi` là lỗi **cả màn**, ⛔ cùng tầm. ⛔ Đổi mã. ⇒ Cả hai câu: mã `2b804e3` **đúng spec đã đính chính** ⇒ **⛔ vòng 2 `WO-045`**. |
| **Mục yếu `BG-048` *(PO xếp)*** | **②** khung tải / lỗi vùng ứng viên `F01G` *(`Đang hỏi sổ…` · `⛔ Cửa lỗi:`)* ⇒ **phê chuẩn** — một màn một giọng cho cùng trạng thái; spec vẽ đủ năm trạng thái ở `ⓦ` ④ mới. Thiếu duy nhất nút `Thử lại` của vùng ấy *(hôm nay lối ra: bấm lại hàng lệnh / `j` rồi `k`)* ⇒ **`WO-023` `(h)`**. **③** `Uncaught` ⇒ **`WO-023` `(h)`** *(`ⓦ` ⑤ ⓐ ⓑ)* — ⚠ `fls-ba` đọc lại mã thấy nặng hơn chữ *"Uncaught"*: `gan` *(`man_f01_ghep.js:657-668`)* ⛔ `try`, `nut()` ⛔ bọc ⇒ cửa ghi trả `422` thì màn **⛔ một chữ**, nút `Gán` vẫn đó — người bấm ⛔ biết lệnh **chưa** gán *(cùng lỗ `F-3` của `bo_gan` đã vá ở `WO-008` vòng 2)*. ⛔ Trong phạm vi `WO-045` *(`ⓦ` ① đoạn *"⛔ Ngoài"*: #4 `gan` thuộc lớp ghi)* ⇒ ⛔ vòng 2. **⑤** `F04` `S.chup` cũ trong lúc ảnh mới tải ⇒ **nợ `GAP-SCR-35`** *(`ⓦ` ⑤ ⓒ — `fls_chup` sổ thật: người chụp **0 / 158**, `SELECT` 05/10)*, lật thành phiếu khi `F04` có người nạp, hoặc Dev gom vào `WO-023 (h)` nếu rẻ. **①④⑥⑦** ⛔ cần quyết *(① đã ở `ⓦ` ① đoạn ⛔ Ngoài; ④ hành vi cũ, ⛔ sai cặp; ⑥⑦ giới hạn đo — `fls-test` đọc)*. |
| **Ai quyết** | `fls-ba` trong thẩm quyền spec — hai câu là **cách đo** + **lớp nút** của luật đã chốt; mục yếu là hành vi trạng thái màn + xếp phiếu. ⛔ câu nghiệp vụ *(con số nào trên màn ⛔ đổi nguồn)* ⇒ ⛔ hỏi owner. |
| **Spec đã sửa** | `02_BA/06_SCREEN_SPEC.md` **v4.20 → v4.21** — đính chính `ⓥ` ⑤ *(lớp `b tiny`, bỏ vế `TT.chay`)* · đính chính `ⓦ` ③ *(chữ số **ngoài** mã `QĐ-ITL-<n>`)* · ⭐ `ⓦ` ④ mới *(vùng ứng viên năm trạng thái)* · ⭐ `ⓦ` ⑤ mới *(lỗi một cú bấm ⛔ rơi ra console: `gan` · `mo_lenh` · `F04` `S.chup`)*. Dòng phương án ⓐ mà bài đọc làm oracle **⛔ đổi** *(bài `AC-13` vế một vẫn khớp đúng 1 lần)*. Phiếu: `WO-045` thêm **Đính chính `TL-049`** cho `AC-13` · `WO-023` thêm `(h)` + `AC-10`…`AC-12` *(vẫn vòng 1, chưa ai nhận)*. |
