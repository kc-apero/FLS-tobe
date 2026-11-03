# 11 — ORACLE READ SPEC: đọc gì từ sổ gốc

**Version:** v1.3 · **Ngày:** 2026-08-26 · **Chủ sở hữu:** Tech Lead
**Đóng:** việc mở *"chốt nguồn `Manual input`"* — **owner chốt 2026-08-26: lấy từ SỔ GỐC** ⇒ `QĐ-ITL-49`.

**Căn cứ:** `02_BA/05_DATA_DICTIONARY_ERD` v0.9 §DD-I01 · §DD-I04 · §DD-I06 · `01_TECH_DESIGN` v1.0 §5.2 *(oracle là cấu phần)* · `QĐ-ITL-36`/`37` · `03_IMPLEMENTATION_PLAN` v1.4 §5.6

> File này trả lời đúng một câu: **`fls/oracle/` mở file nào, sheet nào, cột nào, và tuyệt đối không mở cái nào.**

---

## §1 · Hai file, hai sheet — không thêm

| # | File | Spreadsheet ID | Chủ | Sheet | Dữ liệu bắt đầu | Dùng làm gì |
|:-:|---|---|---|---|:-:|---|
| **1** | `ITL I Input Transaction Ledger File 2_2 (ADJUSTED)` | `1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA` | lanptn@apero.vn | **`ITL Ledge`** | **dòng 10** *(9 dòng đầu là siêu dữ liệu)* | ⭐ **nguồn `Manual input`** + **oracle parity** |
| **2** | `Copy of ITL … 1_2 (RAW)` — ⭐ **bản sao SỐNG, owner chốt** *(`QĐ-ITL-50`)* | `1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E` | — | **`Transaction Mapping L1`** | **dòng 5** *(header dòng 3; dòng 4 TRỐNG; dòng 1–2 là khối khai nguồn)* | đầu vào `ITL-CANON` 36 cột |
| 2b | ~~`ITL … 1_2 (RAW)` bản gốc~~ | `1xaD1RRAeqYsbDyzUhS0EuM4gGAmED9zajUT421PvtZU` | lanptn@apero.vn | — | — | ⏸ **`HTTP 403`** — chưa mở quyền. Không còn chặn P2 vì đã có dòng 2 |

⛔ **Bốn thứ TUYỆT ĐỐI không mở** — mỗi cái đã sập một lần:

| Không dùng | Vì sao |
|---|---|
| `[Master] ITL_Ledge_raw.xlsx` | **~84 dòng MẤT MÃ** *(`ITL#` trơ)* làm **bốc hơi 19,9 tỷ** mà **tổng vẫn tự khớp** |
| **Bản sao ADJUSTED** `1Pqg_G81xQKKP-tyR8IFFcnaimT2oZ22e-Tq_mewxbN0` *(dungtt1@)* | Ngoài kiểm soát. Và bản copy **tự sản xuất giá trị mặc định** với **0 ô lỗi** ⇒ nguy hơn `#REF!`: ai kiểm theo `AUD-5` sẽ kết luận *"copy sạch"* rồi sai chắc trên ~5.000 dòng |
| `ITL_altered` | Sai **680 `HD`** + **1.048 `CDT`** |
| Mọi bản `.xlsx` xuất offline | Chỉ **2,7%** ô ngày còn nguyên kiểu *(4.117 hoán · 5.369 mất kiểu · 38 rơi)* |

### ⭐ Vì sao bản sao RAW được dùng, mà bản sao ADJUSTED thì không

⛔ **Không phải "bản sao thì dùng được".** Hai file có **hai cơ chế khác nhau**, và cái quyết định là *khi phụ thuộc đứt thì sổ nói gì*:

| | `ITL Ledge` *(ADJUSTED)* | `Transaction Mapping L1` *(RAW)* |
|---|---|---|
| Khi nguồn đứt | `iferror` ⇒ cờ `Input here` ⇒ `MID` nhận **hằng mặc định** | **giữ nguyên `#N/A`** |
| Ô lỗi thấy được | **0** ⇒ trông "sạch" | **6.648** ⇒ nói thật chỗ không biết |
| Hậu quả | sai chắc ~5.000 dòng **trong im lặng** | không bịa |

**Đo thật trên bản sao RAW ngày 2026-08-26** — 5 chứng cứ độc lập cùng chỉ một hướng:

| # | Đo | Kết quả |
|--:|---|---|
| 1 | Số dòng · khoảng kỳ | **9.992** dòng · 10/2024 → **08/2026** *(23 kỳ liền, kỳ hiện hành có 512 dòng)* |
| 2 | Tỷ lệ ghép PM | **33,5%** *(3.344/9.992)* — trùng khít **33,8%** đã ghi ở `GAP-ITL-29` |
| 3 | Tab nguồn còn sống | `PM_Unpivot` **3.704** dòng · `PE_Unpivot` **2.638** dòng · **0 ô lỗi** |
| 4 | Ô ngày | **9.992/9.992 = 100%** là ngày thật *(bản `.xlsx` offline chỉ còn **2,7%**)* |
| 5 | Đối chiếu chéo file | tháng 3/2026 = **584 dòng** — **khớp** số dòng cùng kỳ đọc từ `ADJUSTED` |

⭐ **Chứng cứ #2 là chứng cứ mạnh nhất**: nếu bản sao tự sản xuất mặc định thì tỷ lệ ghép sẽ **phồng lên**, không nằm đúng con số đã đo độc lập trước đó.

⛔ **Nhưng owner nói "sống" thì code vẫn phải tự kiểm** *(`cổng chưa từng thấy đỏ là cổng chưa biết có sống`)*. `fls/oracle/` **phải chặn** khi:

| Cổng | Đỏ khi | Vì sao |
|---|---|---|
| `G-ORA-LIVE-1` | kỳ mới nhất trong sổ **cũ hơn 45 ngày** so với ngày chạy | `IMPORTRANGE` của bản sao đã chết mà vẫn trả giá trị cũ |
| `G-ORA-LIVE-2` | tab nguồn nào **0 dòng** hoặc **toàn ô lỗi** | dây đứt ở thượng nguồn |
| `G-ORA-LIVE-3` | tỷ lệ ghép **rơi khỏi khoảng 25–45%** | mặc định đang được sản xuất, hoặc mapping sụp |

⇒ **Đọc LIVE qua Sheets API**, `valueRenderOption` **cả hai lượt**: `UNFORMATTED_VALUE` *(lấy giá trị)* và `FORMULA` *(lấy công thức để tự soi)*.
⚠ Drive connector **không trả công thức** và **cắt ở sheet đầu tiên** với file lớn ⇒ ⛔ không dùng cho việc này.

---

## §2 · `ITL Ledge` — vùng ADJUSTMENT: 7 khối × 4 cột

Khuôn lặp của mỗi khối: `Classifying` → **`Manual input`** → `MID` → `Final`.

| Khối | Trường | `Classifying` | ⭐ **`Manual input`** | `MID` | `Final` | Ô nhập tay | Trong hợp đồng 14 trường? |
|:-:|---|:-:|:-:|:-:|:-:|--:|:-:|
| **1** | `hd` — Budget Code (HDCode) | `S` | **`T`** | `U` | `V` | 297 | ✅ |
| **2** | `pay_type` — Loại giao dịch | `W` | **`X`** | `Y` | `Z` | 179 | ✅ |
| **3** | `cdt1` — Chủ dự toán (CDT1) | `AA` | **`AB`** | `AC` | `AD` | 1.210 | ✅ |
| **4** | `svc_start` — Bắt đầu dùng DV | `AE` | **`AF`** | `AG` | `AH` | 22 | ✅ |
| **5** | `svc_end` — Kết thúc dùng DV | `AI` | **`AJ`** | `AK` | `AL` | 22 | ✅ |
| **6** | `id_payee` — Mã đối tác | `AM` | **`AN`** | `AO` | `AP` | 1.624 | ⛔ ngoài hợp đồng P&L |
| **7** | `invoice` — File đính kèm: Hoá đơn | `AQ` | **`AR`** | `AS` | `AT` | 3.489 | ⛔ ngoài hợp đồng P&L |
| | | | | | **Tổng** | **6.843** | |

★ **Cột `Manual input` cần đọc: `T` · `X` · `AB` · `AF` · `AJ`** *(5 khối hợp đồng)*, **cộng `AN` · `AR`** *(khối 6–7 — `QĐ-owner-0824` mở mặt kế toán sửa lên 7 khối; không vào P&L nhưng lên màn hình)*.

⚠ **`6.843` KHÔNG phải "số ô chưa làm"** — nó là **số lần đã dùng giá trị mặc định** *(`GAC-Other` / `Headquarters2` / `VD0`)*. Đọc nó như tồn đọng công việc là hiểu sai bản chất.

---

## §3 · Đọc thêm gì, và vì sao từng cột

| Nhóm | Cột `ITL Ledge` | Vì sao **bắt buộc** |
|---|---|---|
| **Neo dòng** | `A`–`G` | 7 trường BASE — là thành phần của khoá đối sánh |
| **Pháp nhân** | `P` | `le` = SSOT *(`QĐ-owner-0820`)*. ⛔ **KHÔNG** đọc `BL` |
| **Nhãn người đọc** | `Q` *(`No`)* · `R` *(`ITL ID`)* | Đọc để **đối chiếu**, ⛔ **không** dùng làm khoá — xem §4 |
| ⭐ **`Manual input`** | `T` `X` `AB` `AF` `AJ` `AN` `AR` | **Đây là thứ máy KHÔNG suy được.** Không có nó thì không thể so 100% từng ô |
| **`Classifying`** | `S` `W` `AA` `AE` `AI` `AM` `AQ` | Đầu vào thứ hai của luật `Final`, và là vế **tự soi** |
| **`MID`** | `U` `Y` `AC` `AG` `AK` `AO` `AS` | Để kiểm luật `MID` — chỗ **mặc định cứng** nằm |
| **`Final`** | `V` `Z` `AD` `AH` `AL` `AP` `AT` | ⭐ **oracle parity** — thước chuẩn 100% từng ô |
| **ALLOCATE** | `AU` `AV` `AW` | Gợi ý máy suy; kế toán override tại `Final` *(`QĐ-owner-0824`)* |

⛔ **Không đọc:** vùng `AUDIT` `AX–BL` *(máy FLS tự tính lại, không nhập)* · cột `BL` *(cột `le` cũ, trống 60%, tháng 8/2026 trống 100%)* · mọi cột PII *(Họ tên · CMND/CCCD/Passport)*.

Cộng **một lượt `valueRenderOption=FORMULA`** cho `S:AT` **dòng 10 và dòng 8** — để kiểm luật `MID`/`Final` **vẫn đúng như `DD-I06` đo ngày 24/08**, không giả định nó bất biến.

---

## §4 · ⛔ Ba bẫy phải chặn trong code, không phải nhớ

### 4.1 · Khoá ghép sổ gốc ↔ `fls_itl` **KHÔNG được là `ITL#`**

`R` *(`ITL ID`)* trên sổ là `="ITL#" & No`, mà `No` = **số thứ tự dòng trên bảng đã SORT theo ngày**. Chèn lùi ngày là **đánh số lại toàn bộ** ⇒ `ITL#` **không bền qua hai lần đọc**. Đây chính là gốc của **1.356 dòng `FALSE`** ở vùng AUDIT.

⇒ Ghép bằng **khoá nội dung** `content_key` *(`INV-I04b`)*: `source_system` · `source_sheet` · `doc_date` · `ps_no` · `ps_co` · `doc_no` · `seq_trung`.
⚠ Có **281 dòng trùng nội dung** + **103 dòng không có số chứng từ** ⇒ `seq_trung` phải theo **một quy tắc thứ tự khai báo được**, ⛔ không phải thứ tự dòng. Đây là `GAP-DB-01`, còn mở.

### 4.2 · Ngày trên sổ có thể đã bị hoán ngày↔tháng

93% dòng từng bị hoán *(~181 tỷ sai kỳ)*. `parse_ngay` của `fls/canon` **đã** nổ khi mơ hồ — ⛔ **đừng** thêm `thu_tu` mặc định để "cho nó chạy". Quy tắc phải đến từ **khai báo của nguồn**, và mã bank dạng `FT<yy><ddd>` nhúng ngày thật là **chứng cứ** đối chiếu.

### 4.3 · Một lần đọc **không** lấy được cả sổ

Đo thật: chỉ được **4/7 khối mỗi buổi**; có khối trượt **3/3 lần** kể cả khi cắt lát 1.500 dòng. Sổ nặng vì **tính lại**, không vì nhiều dữ liệu *(đọc 40.000 ô = 1,5 giây · đọc 3 ô trên sổ nguội = 33,2 giây)*.

⇒ `fls/oracle/` phải: đọc **từng cột**, **retry 3–4 lần**, **lưu tăng dần** vào ảnh chụp có `run_id` + ngày, và ⛔ **không kết luận từ dữ liệu một phần**.
⚠ Khoá đệm **PHẢI mang khoảng dòng** — thiếu là **mất 22 dòng im lặng** mà `row_counts` **vẫn tự khớp**.

---

## §5 · Điều kiện xong của lượt đọc *(bổ vào `DEV-03` §5.6)*

| # | Điều kiện | Đo bằng |
|:-:|---|---|
| 1 | Ảnh chụp **đóng băng**, có `run_id` + ngày, chụp **đầu vào và đầu ra trong CÙNG một lần đọc** | metadata ảnh chụp |
| 2 | **Tự soi**: `Final == f(Classifying, MID)` từng dòng; dòng không tự nhất quán ⇒ **loại khỏi oracle** *(bị gõ giữa hai lần đọc)* | số dòng bị loại **có tên lý do** |
| 3 | Chụp **2 lần** cách nhau ⇒ checksum khớp trên phần không đổi | test |
| 4 | Một khối lỗi **không** phá cả lượt đọc | test |
| 5 | Khoá đệm mang **khoảng dòng**; tổng dòng ba đường *(chụp được · trượt · bị loại)* = tổng dòng sổ | test đối chiếu |
| 6 | ⛔ Không ô nào ghi ngược vào file *(`QĐ-ITL-34`)* | quét mã nguồn |

---

## §6 · Việc mở

| ID | Việc | Ai |
|---|---|---|
| ~~`GAP-ORA-01`~~ | ~~Quyền đọc hai file gốc~~ ⇒ **HẠ CẤP 26/08, KHÔNG CÒN CHẶN P2.** Service-account `claude-code-access@fpa-t-494007.iam.gserviceaccount.com` **đọc được**: `ADJUSTED` **gốc** ✅ + `RAW` **bản sao sống** ✅ *(`QĐ-ITL-50`)*. Còn tồn: `RAW` **gốc** trả `HTTP 403` — chỉ cần cho việc **đối chiếu bản sao ↔ gốc**, ⛔ không chặn phát triển | owner + lanptn@ |
| `GAP-ORA-05` ⚠ | **Luật `MID` chưa xác nhận bằng công thức.** Bản `.xlsx` không còn công thức ở cột `MID`; luật bước 1 hiện lấy từ `DD-I06` *(đọc live 24/08)*. Phải đọc lại **LIVE `valueRenderOption=FORMULA`** cả 7 cột `MID` *(`U` `Y` `AC` `AG` `AK` `AO` `AS`)* rồi khoá bằng test | Tech Lead |
| `GAP-ORA-08` ⛔⛔ | **Đọc LIVE từ `ADJUSTED` bất khả thi** — workbook không trả được giá trị đã tính *(1 ô = timeout, mọi sheet, mọi endpoint)*. Xem **§8**. Cần owner tạo bản **"dán giá trị"** của `ITL Ledge` từ file gốc. Cho tới lúc đó thước chuẩn chạy trên hiện vật đóng băng, thiếu ~1,5 kỳ cuối | owner |
| `GAP-ORA-06` ⚠ | **Khối 4–5 *(`svc_start`/`svc_end`)* không có mặc định cứng** — 22 dòng, giá trị khác nhau *(`202512`×8 · `202508`×4 …)*. Máy hiện để `None` *(`INV-I16`)*. Cần luật: bỏ trống có kiểm soát, hay có quy tắc suy? | Kế toán trưởng |
| ~~`GAP-ORA-07`~~ | ⛔ **RÚT 26/08 — tôi suy sai, không phải lỗi.** Owner chốt: cột `W`/`X` tra vào `PI_Unpivot` là **CHỦ Ý THIẾT KẾ**, ⇒ `QĐ-ITL-51`. Xem §7 | — |
| `GAP-ORA-02` | Quy tắc `seq_trung` cho **281 dòng trùng** + **103 dòng không có số chứng từ** — phải khai báo được, ⛔ không lấy thứ tự dòng *(`GAP-DB-01`)* | Tech Lead + Kế toán trưởng |
| `GAP-ORA-03` | Thứ tự ngày `dmy`/`mdy` **theo từng nguồn** — cần khai báo, đối chiếu bằng mã bank `FT<yy><ddd>` | Kế toán trưởng |
| `GAP-ORA-04` | Bản sao ADJUSTED ngoài kiểm soát *(dungtt1@)* — **thu hồi hay đánh dấu rõ**? Nó tự sản xuất giá trị mặc định với 0 ô lỗi | owner |

## §8 · ⛔⛔ ĐỌC LIVE TỪ `ADJUSTED` LÀ **BẤT KHẢ THI** — `GAP-ORA-08`

**Đây là chỗ file này sai nặng nhất.** `v1.0`–`v1.2` đều viết *"Đọc **LIVE** qua Sheets API"* và coi đó là điều đương nhiên. **Không đọc được.**

### Đo thật 2026-08-26

| Phép | Thời gian | Kết quả |
|---|--:|---|
| `metadata` *(không đọc ô nào)* | **0,6s** | ✅ |
| **MỘT Ô** · `valueRenderOption=FORMULA` | **0,5s** | ✅ |
| **MỘT Ô** · giá trị đã tính | **45–90s** | ⛔ **timeout** |
| Cùng phép trên sheet **khác** của cùng workbook | **75s** | ⛔ **timeout** |
| `spreadsheets.get?includeGridData` *(endpoint khác)* | **75s** | ⛔ **timeout** |
| Drive export `.xlsx` | 0,3s | ⛔ **`403`** *(SA không có quyền đó)* |
| **1.000 ô từ `RAW` bản sao** | **1,8s** | ✅ ⇒ code · token · mạng **đều OK** |

### Nguyên nhân — nằm ngay trong công thức đọc được

```
A10 = filter(IMPORTRANGE($B$1,$B$2&"!A4:F"), IMPORTRANGE($B$1,$B$2&"!A4:A")>$B$3)
```

Một **công thức mảng kéo cả vùng từ workbook khác**. Đọc **bất kỳ** ô nào cũng bắt cả workbook tính lại toàn bộ — và nó không xong trong thời gian chờ. Chế độ `FORMULA` chạy được vì công thức là **văn bản đã lưu**, không cần tính.

⭐ **Và điều này giải thích luôn một ghi chép cũ tưởng là ngẫu nhiên** — `DoD 5.6 ③`: *"đo thật chỉ được **4/7 khối mỗi buổi**, có khối trượt **3/3 lần** kể cả khi cắt lát 1.500 dòng"*. ⛔ Không phải kích thước lát. Là **may mắn**: lần đọc đó có gặp lúc workbook còn ấm hay không. ⇒ Luật *"cắt lát nhỏ hơn"* trong `DoD 5.6 ③` là **chữa sai bệnh**.

### ⚠ Ba lần tôi đoán sai trước khi đo — ghi lại để không lặp

| | Giả thuyết | Đã thử | Kết quả |
|--:|---|---|---|
| ⓐ | *"lát 2.000 dòng quá to"* | giảm còn 500 | vẫn treo |
| ⓑ | *"hình dạng câu hỏi sai"* | lát-dòng · một-cột · `batchGet` nhiều cột | **cả ba treo y hệt 90s** ⇒ không phải hình dạng |
| ⓒ | *"chính mình đang tự chặn"* | kill việc chạy nền | vẫn treo |

★ **Bài học:** khi ba giả thuyết liên tiếp sai, **thôi đoán — đi đo từ nhỏ nhất**. Một ô. Chính phép đo một-ô mới lật được vấn đề. Và ⛔ **timeout 300s là bẫy**: một lần chờ vô vọng × nhiều lát = treo cả giờ mà không biết gì *(thực tế: treo 40 phút, 0 dòng, 0 thông tin)*.

### Cách làm MỚI — thước chuẩn chạy trên hiện vật đóng băng

| | |
|---|---|
| **Hiện vật** | `tests/fixture/itl_ledge_adjustment.json` — **9.219 dòng · 22 kỳ**, chỉ **28 cột vùng ADJUSTMENT + cột ngày**; nội bảng giá trị *(1.526 giá trị duy nhất)* ⇒ **4,50 MB → 0,82 MB**; có `checksum` + test khoá |
| **Kết quả** | ⭐ **parity 64.393/64.393 ô = 100,0000%**, 22 kỳ, **0 ô lệch**, **0 ô phải chuẩn hoá số** *(bản 1 kỳ trước đó có 396)* |
| **Loại khỏi thước** | **20 dòng**, ⛔ không rải đều — **dồn hết vào kỳ cuối**, khoảng dòng **8872–9041**, ba khối *(`hd` 8 · `cdt1` 6 · `invoice` 6)* ⇒ đọc được: file được lưu khi mấy dòng cuối còn đang settle |
| ⚠ **Giới hạn ①** | Đóng băng 26/08 nhưng dữ liệu chỉ **tận 2026-07** *(425 dòng kỳ cuối; sổ sống có 686)* ⇒ **thiếu ~1,5 kỳ cuối** |
| ⚠ **Giới hạn ②** | Lấy từ bản `.xlsx`. Hợp lệ **chỉ vì** đo được: 28 cột này **0 ô lỗi** và ngày **100% nguyên kiểu**. ⛔ Không lấy `H`–`O` *(6.126–8.821 ô lỗi)*, ⛔ không lấy `Diễn giải`/`Số chứng từ` *(có thể có tên người)* |

⭐ **Cách gỡ dứt điểm — cần owner.** Tạo một bản **"dán giá trị"** của `ITL Ledge` từ **file gốc** *(copy → paste values only)*. Bản đó đọc tức thì, và **đúng là "ảnh chụp đóng băng từ file gốc"** mà `DoD 5.6 ①` yêu cầu — không phải một ngoại lệ, mà là **cách đúng** để làm điều DoD đã đòi.

---

## §7 · ⭐ `W`/`X` `#N/A` là CÂU TRẢ LỜI, không phải lỗi *(`QĐ-ITL-51`)*

**Tôi đã báo sai một lần ở đây — ghi lại để không ai lặp.** Ngày 26/08 tôi kết luận `W`/`X` là *"dây đứt"* vì thấy **hai chỗ nói trái nhau**:

```
W2 (khai nguồn)  →  [Importrange]PE_Unpivot   ID PELine
W5 (công thức)   →  VLOOKUP($P5:$P, {'[Importrange]PI_Unpivot'!$R:$R, …
```

và vì đo được **0/430** khoá `ID PELine` tồn tại ở `PI_Unpivot!R`, trong khi **430/430** tồn tại ở `PE_Unpivot!S`. Suy ra *"tra sai bảng"*. **Suy luận đó sai.**

**Owner chốt: đây là chủ ý thiết kế.** Hai cột đọc `PI_Unpivot` là **có mục đích** — và điều đó làm đổi hoàn toàn ý nghĩa của `#N/A`:

| | `W`/`X` | `AB`/`AC` |
|---|---|---|
| Khoá tra | `ID PELine` *(cột `P`)* | `ID PILine` *(cột `R`)* |
| Bảng tra | `PI_Unpivot` | `PI_Unpivot` |
| Nghĩa | thời gian dịch vụ **theo đường lệnh chi** | …**theo đường hoá đơn** |
| Đo được | `#N/A` 100% | 23,7% |

⇒ **`#N/A` ở `W`/`X` là một câu trả lời có nghĩa**, không phải chỗ hỏng: *dòng này chưa có hoá đơn xác nhận thời gian dịch vụ.* Và cả **hai cột đều tra `PI_Unpivot`** — nên "sai bảng" là kết luận không đứng được ngay từ đầu; đúng ra tôi phải hỏi *vì sao hai đường*, không phải kết luận *một đường sai*.

⚠ **Bài học cho chính máy đo:** tôi lấy **sự khác nhau giữa nhãn và công thức** làm bằng chứng lỗi. Trong sổ này nhãn dòng 2 là **nhãn nhóm cột**, ⛔ không phải khai báo nguồn bắt buộc của từng cột. Đọc nhãn thành hợp đồng là lỗi của người đọc.

### ⛔ Hệ quả BẮT BUỘC trong code

| Luật | Nội dung |
|---|---|
| `R-ORA-07a` | `#N/A` ở `W`/`X` ⇒ **trống có kiểm soát** *(`svc_start`/`svc_end` = `NULL`)*, ⛔ **KHÔNG** vào `fls_reject`, ⛔ **KHÔNG** tính là "sai kiểu" |
| `R-ORA-07b` | ⛔ **KHÔNG** lấy `AB`/`AC` lấp vào `W`/`X` — hai đường mang **hai nghĩa khác nhau**; trộn là làm mất thông tin *"chưa có hoá đơn"* |
| `R-ORA-07c` | Cột `Z`/`AA` **rỗng, không tiêu đề, không công thức** ⇒ **không đọc**, giữ đúng 38 vị trí *(`INV-I11`: chỗ trống vẫn là một vị trí)* |
| `R-ORA-07d` | Cổng `G-ORA-LIVE-3` ⛔ **không** được đặt ngưỡng trên `W`/`X` — 0% là **trạng thái đúng** ở đây |

⚠ **Còn nợ thật:** khoá `ID PELine` *(cột `P`)* `#N/A` trên **6.648/9.992 dòng**; chỉ **430** dòng có khoá thật. Cái này **là** nợ dữ liệu, cùng gốc với tỷ lệ ghép **33,5%** — nhưng nó thuộc `GAP-ITL-29`, ⛔ không phải một việc mở mới.

---

## Changelog

- **v1.3** (2026-08-26): ⛔⛔ **SỬA SAI NẶNG NHẤT CỦA FILE NÀY: "đọc LIVE qua Sheets API" là BẤT KHẢ THI với `ADJUSTED`.** Đo thật: `metadata` 0,6s ✅ · **một ô** chế độ `FORMULA` 0,5s ✅ · **một ô** giá trị đã tính **timeout** ⛔ *(mọi sheet, mọi endpoint, cả `includeGridData`)*; `1.000 ô` từ `RAW` bản sao 1,8s ✅ ⇒ code/token/mạng đều OK. Nguyên nhân trong chính công thức: `filter(IMPORTRANGE(...))` kéo cả vùng từ workbook khác ⇒ đọc ô nào cũng bắt tính lại toàn bộ. ⭐ **Giải thích luôn ghi chép cũ** *"4/7 khối mỗi buổi, có khối trượt 3/3 lần"* — không phải kích thước lát, là **may mắn** ⇒ luật "cắt lát nhỏ hơn" ở `DoD 5.6 ③` **chữa sai bệnh**. Thêm **§8** với 3 giả thuyết sai của tôi *(lát to · hình dạng câu hỏi · tự chặn mình)* và bài học **"ba lần đoán sai thì thôi đoán, đi đo từ một ô"** + bẫy **timeout 300s** *(treo 40 phút, 0 dòng, 0 thông tin)*. Cách làm mới: hiện vật đóng băng **9.219 dòng · 22 kỳ · 0,82 MB** ⇒ ⭐ **parity 64.393/64.393 = 100,0000%**, 20 dòng loại **dồn hết kỳ cuối**. Mở ⛔ `GAP-ORA-08`.
- **v1.2** (2026-08-26): ⛔ **RÚT `GAP-ORA-07`.** Owner chốt `W`/`X` tra `PI_Unpivot` là **chủ ý thiết kế** *(`QĐ-ITL-51`)* ⇒ `#N/A` 100% là **câu trả lời** *("chưa có hoá đơn xác nhận")*, không phải dây đứt. Thêm **§7** với 4 luật cưỡng chế `R-ORA-07a…d` *(trống có kiểm soát ⛔ không reject · ⛔ không lấy `AB`/`AC` lấp · ⛔ không đọc `Z`/`AA` · ⛔ không đặt ngưỡng cổng trên `W`/`X`)*. ⚠ Ghi lại **lỗi suy luận của chính máy đo**: lấy khác biệt nhãn↔công thức làm bằng chứng lỗi, trong khi nhãn dòng 2 chỉ là **nhãn nhóm cột**. Nợ thật còn lại là khoá `P` `#N/A` **6.648/9.992** — thuộc `GAP-ITL-29`.
- **v1.1** (2026-08-26): ⭐ **P2 HẾT BỊ CHẶN.** Owner chốt **bản sao RAW sống** `1md85t…` làm nguồn đầu vào *(`QĐ-ITL-50`)*; `ADJUSTED` **gốc** đã đọc được. Thêm §*"vì sao bản sao RAW được dùng mà bản sao ADJUSTED thì không"* — **5 chứng cứ đo thật** *(9.992 dòng · 23 kỳ tới 08/2026 · ghép **33,5%** khớp **33,8%** · ngày sạch **100%** · tháng 3/2026 = **584** khớp chéo với `ADJUSTED`)*, cộng **3 cổng tự kiểm** `G-ORA-LIVE-1/2/3` để biến lời cam kết "sống" thành thứ máy chặn được. Sửa **dòng bắt đầu dữ liệu RAW: 4 → 5** *(dòng 4 trống — off-by-one này làm rơi 1 dòng trong im lặng)*. Hạ cấp `GAP-ORA-01`; mở `GAP-ORA-05` *(công thức `MID`)*, `GAP-ORA-06` *(khối 4–5 không hằng)*, ⛔ `GAP-ORA-07` *(**`W`/`X` `#N/A` 100%** — dây `PE_Unpivot` đứt)*.
- **v1.0** (2026-08-26): Khởi tạo sau khi owner chốt **`Manual input` lấy từ SỔ GỐC** *(`QĐ-ITL-49`)*. Chốt **2 file · 2 sheet**, cột `Manual input` = **`T` `X` `AB` `AF` `AJ`** *(+ `AN` `AR` cho khối 6–7)*, đủ bộ cột cần đọc kèm lý do từng cột, **4 thứ tuyệt đối không mở**, **3 bẫy chặn trong code** *(khoá không được là `ITL#` · ngày có thể đã hoán · một lần đọc không lấy hết sổ)*, 6 điều kiện xong của lượt đọc. Mở `GAP-ORA-01…04` — trong đó `GAP-ORA-01` *(quyền service-account)* **chặn P2**.
