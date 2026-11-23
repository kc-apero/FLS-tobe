# HOI-016 — Nhật ký `F02` ⑦ đọc nhãn theo `value_source`, nhưng với cú gõ của NGƯỜI cột ấy là **nguồn TRƯỚC khi gõ**, ⛔ "ai ghi dòng này" · và khối `bo_qua` có in giá trị không

| | |
|---|---|
| **Thuộc** | `WO-008` |
| **Hỏi bởi** | `fls-dev` · 2026-10-02 |
| **Loại** | ⓑ `LECH_DU_LIEU` *(chính)* · ⓐ `MAU_THUAN` *(nhỏ)* |
| **Trạng thái** | ✅ **`DONG`** *(02/10 — `TL-016` bên dưới: ⓑ nghĩa cột = **lớp của chính dòng**, sửa ở **cửa ghi** ⇒ [`WO-018`](WO-018-nhat-ky-value-source-la-lop-cua-dong.md); ⓐ nhận phương án ⭐; nhãn chữ trơn nhận; `WO-008` ⛔ mở lại)* |
| **Chặn** | `KHONG_CHAN` — mã `WO-008` đã làm theo phương án ⭐ của cả hai câu; đổi phương án = đổi **một hàm** + **một bài** |

## ⓑ `value_source` của dòng nhật ký NGƯỜI = nguồn của giá trị **trước** khi gõ

### Bằng chứng
- Spec: `02_BA/06_SCREEN_SPEC.md` v4.8 `:1190` — *"cột **thành** + **nguồn** đọc theo `value_source`: ⓐ `may_goi_y` có giá trị ⇒ "gợi ý: X" … Cột nguồn in nhãn: `may_goi_y` ⇒ "máy gợi ý · ⛔ đổi Final" · `sua_tay` ⇒ "người sửa"…"* — spec đọc `value_source` như **"ai/cái gì ghi dòng này"**.
- Mã ghi: `fls/repo/ghi_tay.py:446` — cú `/adjust` của người ghi `fls_journal.value_source = t["value_source"]`, với `t = truoc_khi_go(...)` *(`:263`–`:286`)*: `sua_tay` nếu ô đã có giá trị người · `nguon` nếu sổ gốc có giá trị · **`may_goi_y` nếu cột `*_thyt` có gợi ý** *(`:282`)* · `UNMAPPED` nếu cả ba rỗng *(`:284`)*. ⇒ Với cú gõ của NGƯỜI, `value_source` là **nguồn của giá trị bị thay**. Còn dòng máy *(`:571`, `may_goi_y`)* và bản đảo *(`:973`, `nguon` của dòng bị đảo)* thì `value_source` đúng là **lớp của chính dòng**. Một cột, hai nghĩa.
- Đo kho TEST *(bài `tests/web/test_wo008_than_that_bo_ghep_pg.py::test_AC2…`, dòng B dựng qua cửa thật)*: dòng người gõ `hd = HD-K7B` mang `value_source = 'UNMAPPED'` *(gợi ý của phép ghép nằm ở `fls_may_goi_y`, ⛔ ở `hd_thyt`, nên `truoc_khi_go` thấy ô rỗng)* ⇒ màn in `HD-K7B` · nguồn `UNMAPPED` — ⛔ *"người sửa"*.
- Đo kho THẬT *(chỉ `SELECT` qua `noi_chi_doc`, 02/10)*: `fls_journal` theo `value_source`: `may_goi_y` có giá trị **4.424** · `sua_tay` có giá trị **2** · `sua_tay` rỗng **2** *(mẫu số 4.428)*; `fls_itl` **8.387** dòng, cả **7** cột `*_thyt` khác `NULL` = **0** ⇒ ca xấu dưới đây hôm nay **⛔ xảy ra được**.
- **Ca xấu** *(chưa xảy ra, ⛔ có bài dựng)*: một dòng có `hd_thyt` ≠ `NULL`, người gõ `hd = X` ⇒ dòng nhật ký `value_source = 'may_goi_y'`, `value_after = X` ⇒ theo spec v4.8 màn in **"gợi ý: X" · "máy gợi ý · không đổi Final"** cho một giá trị **NGƯỜI**, **là Final** — đúng lớp lỗi `F-1` muốn xoá, theo chiều ngược.

### Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | **Giữ** spec v4.8 *(mã `WO-008` làm đúng vậy)*; thêm câu vào `BA-06` + `BA-10` `DT-I14`: *"với dòng người gõ, `value_source` là nguồn **trước** khi gõ; nhãn `người sửa` chỉ hiện khi người gõ đè giá trị người; ca `*_thyt` ≠ NULL chấp nhận vì sổ thật 0"* | Ca xấu bật lại khi có nguồn nào điền `*_thyt` *(hôm nay ⛔ nguồn nào)*. Dòng người gõ đầu tiên trên ô rỗng in mã `UNMAPPED` / `nguon` — đúng luật "mã khác ⇒ in nguyên mã" nhưng ⛔ nói được "người" | ⭐ *(⛔ chặn, đủ cho hôm nay)* |
| 2 | Đổi luật **GHI**: cú `/adjust` ghi `value_source = 'sua_tay'` *(lớp của chính dòng)*, nguồn trước khi gõ chuyển sang chỗ khác hoặc bỏ | Đổi nghĩa một cột đã có **4.428** dòng *(dòng cũ giữ nghĩa cũ — chỉ-thêm `INV-I08`)* ⇒ một cột hai nghĩa **theo thời gian**; ngoài phạm vi `WO-008` *(⛔ đổi luật ghi nhật ký)*; cần `WO` mới + `BA-05` | |
| 3 | Thêm cột `adj_id` vào `fls_journal` để màn đọc `nguon` của bút toán *(lớp thật)* | Migration — `WO-008` NGOÀI phạm vi ghi rõ *"⛔ thêm cột `adj_id`/`reversal_of`"*; dòng cũ ⛔ có `adj_id` | |

## ⓐ Khối `bo_qua` có in **giá trị** người không

### Bằng chứng
- `WO-008` `:33` Phạm vi (b): *"Khối `bo_qua` (cảnh báo "người đã gõ tay") **giữ** như nay"* — bản cũ chỉ in **tên ô** *(`man_f01.js` trước `WO-008`: `bo.map(x => x.truong || x.field || x)`)*.
- `WO-008` `:44` `AC-4`: *"cửa trả `bo_qua=[{field:'hd', value_after:'HD-K7B'}]` ⇒ **1** hộp mở, chứa `hd` **và `HD-K7B`**"* — bản cũ ⛔ in được `HD-K7B`.

### Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | In thêm giá trị bên cạnh tên ô: *"… người đã gõ tay lên đó sau khi ghép: `hd = HD-K7B`"*; câu cảnh báo giữ nguyên | Đổi một chút khối "giữ như nay" — người đọc thấy luôn **giá trị** máy ⛔ rút, ⛔ phải mở `F02` tra | ⭐ *(mã `WO-008` làm vậy)* |
| 2 | Giữ khối như cũ *(chỉ tên ô)*; `AC-4` đổi thành "chứa `hd`" | `AC-4` đổi chữ; người đọc phải đi tra giá trị | |

---

# TL-016 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⓑ ⛔ phương án 1 *(giữ nghĩa kép)*, ⛔ phương án 3 *(migration)* — ⭐ **phương án 2 thu hẹp**: `fls_journal.value_source` = **lớp của CHÍNH dòng** *(ai nói `value_after`)*; cửa ghi `/adjust` + `dao_but_toan` sửa theo ⇒ **[`WO-018`](WO-018-nhat-ky-value-source-la-lop-cua-dong.md)** *(phiếu mới, ⛔ gộp `WO-015`)*. Màn `F02` ⑦ **⛔ đổi**, `WO-008` **⛔ mở lại**. · ⓐ phương án ⭐ **1** *(in `hd = HD-K7B`)* — `WO-008` Phạm vi (b) đính chính. · Nhãn chữ trơn *"máy gợi ý · không đổi Final"* — **nhận**, spec + `AC-1` đính chính |
| **Ai quyết** | `fls-ba` *(trong thẩm quyền spec)* — ⓑ đưa cửa ghi về **định nghĩa owner đã chốt**: `AUD-1` *(`BA-04`, `QĐ-ITL-16`)* *"nguồn giá trị (máy suy/người nhập/sửa lại)"* = nguồn của giá trị **được ghi**; `INV-I21` *(`QĐ-ITL-149`)* *"ai nói con số"*. ⛔ Câu nào thuộc owner *(⛔ đổi "con số trên màn đến từ đâu")* |
| **Spec đã sửa** | `02_BA/05_DATA_DICTIONARY_ERD.md` **v0.33 → v0.34** *(+`DD-I15 ⓓe` — nghĩa cột + bất biến `value_source = fls_adjustment.nguon` cùng giao dịch)* · `02_BA/06_SCREEN_SPEC.md` **v4.8 → v4.9** *(dòng *"F02 · nhật ký"*: nghĩa cột + đính chính nhãn; dòng *"Bỏ ghép"*: `bo_qua` in tên ô + giá trị)* · `WO-008` *(đính chính Phạm vi (a)(b) + `AC-1`, ⛔ xoá câu cũ)* · `WO-015` *(thứ tự: sau `WO-018`)* |

### Vì sao — ⓑ *(đo 02/10, kho thật chỉ `SELECT`)*
- **Spec đã có nghĩa, mã `/adjust` lệch nó.** `AUD-1` đòi nguồn của giá trị **được ghi**; `DD-I15 ⓓd` ghi dòng máy `value_source='may_goi_y'` *(lớp của dòng)*; `bo_moi_noi` chép lớp của dòng bị đảo. Chỉ `ghi_but_toan` *(`:446`)* ghi nguồn **trước** khi gõ — và chú thích cột `fls/db/schema.py:180` *"nguon goi y luc go"* là dấu vết của nghĩa ấy.
- **Bất biến đo được, và đang ĐÚNG trên sổ thật:** nối `fls_journal` ↔ `fls_adjustment` theo `(itl_id, field, at, actor)` *(khoá **0** trùng trên `fls_adjustment`)* ⇒ **4.428 / 4.428** cặp, **4.428 / 4.428** có `value_source = nguon` *(4.426 bút toán + 2 bản đảo)*. ⇒ Đổi luật ghi **⛔ đẻ** cột hai nghĩa theo thời gian trên sổ thật — cái giá *"4.428 dòng giữ nghĩa cũ"* của phương án 2 trong phiếu là **⛔ đúng**: cả 4.428 dòng **đã** mang nghĩa mới; dòng từ `/adjust` trên sổ thật = **0** *(4.424 `may@fls` + 4 UAT đường ghép cũ)*.
- **Vì sao sửa NGAY chứ ⛔ để phương án 1:** nhật ký chỉ-thêm *(`INV-I08`)* ⇒ cú gõ thật đầu tiên của kế toán sẽ ghi một dòng nghĩa cũ **vĩnh viễn**. Hôm nay rẻ nhất.
- **Vì sao ⛔ sửa ở màn:** màn ⛔ có tín hiệu nào khác phân biệt được. `actor ∉ ACTOR_MAY` ⛔ dùng được — dòng máy của cú ghép **tay** mang `actor` = người bấm *(`INV-I21` v0.14)*; `nguon` của bút toán chỉ đọc được qua cửa `GET /journal` mới hay cột `adj_id` *(cả hai `WO-008` NGOÀI phạm vi)*. Sửa cửa ghi thì nhãn hiện có của màn tự đúng.
- **"Nguồn trước khi gõ" ⛔ mất:** thân trả `/adjust` *(`KetQuaGhi.value_source`)* và cửa `before-edit` **giữ** nghĩa ấy *(`US-025`)*; nhật ký giữ `value_before`, lớp của nó đọc lại ở dòng trước của cùng ô hay sổ gốc *(`BA-05 ⓓe`)*.
- Kèm theo: `dao_but_toan` *(`:480`–`:482`)* ghi cứng `NGUON_TAY` cho **mọi** bản đảo ⇒ đảo một dòng `may_goi_y` qua cửa đảo phá bất biến *(sổ thật: **0** bản đảo qua đường này)* ⇒ cùng vào `WO-018`.

### Vì sao — ⓐ và nhãn
- ⓐ `AC-4` đòi `HD-K7B` có mặt; *"giữ như nay"* ở Phạm vi (b) là câu của `fls-ba` viết trước khi nghĩ tới giá trị — in thêm giá trị ⛔ đổi câu cảnh báo, chỉ cho người đọc thấy ngay cái máy ⛔ rút. `AC-4` đúng, Phạm vi (b) đính chính.
- Nhãn: `⛔` trong spec là ký hiệu **của tài liệu**; tệp màn chịu luật ký hiệu *(`test_luat_ky_hieu_man_hinh.py`)* — đúng điều `WO-008` Rủi ro 1 đã dặn. Chữ trơn *"không đổi Final"* cùng nghĩa.

### Việc của ai sau `TL`
- `fls-dev`: ⛔ việc gì thêm cho `WO-008`. Nhận [`WO-018`](WO-018-nhat-ky-value-source-la-lop-cua-dong.md) **sau** khi `WO-008` ĐẠT *(phiếu ấy lật đúng một `assert` trong bài `WO-008` — `("HD-K7B", "UNMAPPED")` ⇒ `("HD-K7B", "người sửa")`)*.
- `fls-test`: kiểm `BG-017` theo `WO-008` **đã đính chính**. Hàng người gõ in nguồn `UNMAPPED` trên kho TEST là **đã biết, ⛔ nâng thành `F`** — `WO-018` sửa ở cửa ghi. ⚠ `BA-05` đổi *(v0.34)* ⇒ rà truy vết `04_Test/03` cho `DD-I15 ⓓe`.

**Trạng thái `HOI-016`: `DONG`** *(02/10, `fls-ba`)*.
