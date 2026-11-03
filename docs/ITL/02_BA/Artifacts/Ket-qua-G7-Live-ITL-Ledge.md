# Kết quả `G7` live — công thức thật của `ITL Ledge`

**Version:** v0.1 · **Ngày:** 2026-08-20 · **Nguồn:** Google Sheets API, `valueRenderOption=FORMULA`
**Xác thực:** service account `claude-code-access@fpa-t-494007.iam.gserviceaccount.com` (đã có sẵn quyền Viewer trên file ADJUSTED)
**File đọc:** `ITL I Input Transaction Ledger File 2/2 (ADJUSTED)` — `1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA`
**Đóng:** `G7-16` `G7-17` `G7-18` `G7-19` `G7-20` `G7-21` `G7-22` `G7-25` `G7-26` · **Chưa đóng:** mọi mục thuộc file RAW và PM (403 — xem §7)

---

> **PHỤ LỤC.** Nội dung diễn giải của file này **đã hợp nhất** vào [Process-PM-den-ITL.md](Process-PM-den-ITL.md) v1.0 — đó là SSOT. File này giữ lại làm **phụ lục công thức nguyên văn**. Đừng sửa hai nơi.


## §1 · Bốn khẳng định của process map — **xác nhận đúng**

| # | Khẳng định | Chứng cứ live |
|--:|---|---|
| 1 | `$B$2` = sheet nguồn = **`Transaction Mapping L1`** | `ITL Ledge!B2` = `Transaction Mapping L1`; `B1` = `ITL I Input Transaction Ledger File 1/2` |
| 2 | `ITL Ledge` chỉ kéo **8 dải** | 8 công thức ở dòng 10, nguyên văn §2 dưới |
| 3 | Bản đồ cột đúng y nguyên | **dòng 5 của `ITL Ledge` chính là hàng bản đồ**: `A→A … H→H`, **`I→S · J→T · K→AB · L→AC · M→Y · N→AD · O→AE · P→AG · Q→AL`** |
| 4 | **12 cột PM/PE/PI bị rơi** | Bản đồ không hề nhắc `I..R` của `Transaction Mapping L1`. **`ID PMLine`, `ID PMSlip`, 4 mã PE/PI, `Pháp nhân thanh toán`, `Status_Final` không có đường sang.** §5 process map **đứng vững** |

**8 công thức nguyên văn (dòng 10):**

```
A10 = filter(IMPORTRANGE($B$1,$B$2&"!A4:F"),  IMPORTRANGE($B$1,$B$2&"!A4:A")>$B$3)
G10 = filter(IMPORTRANGE($B$1,$B$2&"!G4:H"),  …)
I10 = filter(IMPORTRANGE($B$1,$B$2&"!S4:T"),  …)
K10 = filter(IMPORTRANGE($B$1,$B$2&"!AB4:AC"),…)
M10 = filter(IMPORTRANGE($B$1,$B$2&"!Y4:Y"),  …)
N10 = filter(IMPORTRANGE($B$1,$B$2&"!AD4:AE"),…)
P10 = filter(IMPORTRANGE($B$1,$B$2&"!AG4:AG"),…)
Q10 = filter(IMPORTRANGE($B$1,$B$2&"!AL4:AL"),…)
R10 = ArrayFormula("ITL#"&Q10:Q)
```

⇒ **`itl_id` sinh từ cột `No`**: `ITL#<No>`, mà `No` là cột `AL` của `Transaction Mapping L1`. Dữ liệu bắt đầu **dòng 10** (khớp `min_row=10` của engine).

**Dòng 6 là hàng tự-kiểm**: `=IMPORTRANGE($B$1,$B$2&"!"&A$5&$Q$6&":"&A$5&$Q$6)=A10` — đọc lại **một ô** từ nguồn rồi so với ô tại chỗ, ra `TRUE`/`FALSE`. `Q6 = Q10+4` là độ lệch dòng.

---

## §2 · ★ Phát hiện nặng nhất — `Input here` **không phải nhãn việc cần làm**

Nó là **lệnh gán giá trị mặc định**. Ai gõ `Input here` là **im lặng đẩy tiền vào một giá trị định sẵn**:

| Khối | Cột MID | Gõ `Input here` → giá trị thật được ghi |
|---|:--:|---|
| Budget Code (HDCode) | `U` | **`OGA \| GAC - Other`** |
| Loại giao dịch | `Y` | **`Thanh toán (Regular)`** |
| Chủ dự toán (CDT1) | `AC` | **`SHQ2 \| Headquarters2`** |
| Kỳ dịch vụ — bắt đầu | `AG` | `year(A)&month(A)` — **suy từ ngày chứng từ** |
| Kỳ dịch vụ — kết thúc | `AK` | idem |
| Mã đối tác (ID Payee) | `AO` | **`VD0`** |
| File hoá đơn | `AS` | **`Nợ hoá đơn`** |

> **Nghĩa nghiệp vụ.** Con số `# Input here = 297 / 179 / 1210 / 22 / 22 / 1624 / 3489` **không phải** "còn 6.843 ô chưa làm". Nó là **6.843 lần đã dùng giá trị mặc định**. Trong đó:
>
> - **1.210 dòng** chi phí được gán cho **`SHQ2 | Headquarters2`** — không phải vì thuộc Hội sở, mà vì **không biết thuộc ai**.
> - **297 dòng** được gán **`OGA | GAC - Other`** — đúng cái thùng rác mà `gac-oth-catchall-nonopex` đã ghi nhận. **Nay biết cơ chế: đây là giá trị mặc định khi không tra được HDCode.**
> - **1.624 dòng** gán nhà cung cấp **`VD0`** — một mã giả.
>
> Đây là lời giải cho hiện tượng "Hội sở gánh nhiều" trong P&L (`[[mgm-cbl-hqkeep-ebt-leak]]`, `[[apr-comp-venture-allocation-dropped]]`): **một phần là mặc định kỹ thuật, không phải phân bổ thật**.

---

## §3 · Công thức 4 cột chuẩn — và một điều rất dễ hiểu sai

Mọi khối trong ADJUSTMENT ZONE đều theo đúng khuôn này (lấy khối HDCode làm ví dụ):

```
S (Classifying)   = ArrayFormula(iferror(I10:I, "Need to manual input"))
T (Manual input)  = người gõ
U (MID)           = ArrayFormula(if(and(T10:T="", S10:S<>"Need to manual input"), S10:S,
                                    if(T10:T="Input here", "OGA | GAC - Other", T10:T)))
V (Final)         = if(or(S10="Need to manual input", len(S10)=0), U10, S10)
```

> ⚠ **`Final` ưu tiên `Classifying`.** Nếu nguồn từ `Transaction Mapping L1` có giá trị (không lỗi, không rỗng) thì **giá trị người gõ tay bị bỏ qua hoàn toàn**. Người gõ **chỉ có tác dụng khi nguồn lỗi hoặc rỗng**.
>
> Hệ quả: sửa tay để "chữa" một dòng mà nguồn vẫn có giá trị sai ⇒ **sửa không ăn**. Đây là ứng viên `INV` mới và là câu phải hỏi LAN + THƯƠNG.

---

## §4 · ★ Cột pháp nhân mà engine đọc nằm trong sheet tên `Daily RP test`

```
ITL Ledge!BL10 = VLOOKUP(G10, 'Daily RP test'!$R$6:$S, 2, 0)
```

`BL` = `ENITY` — **chính là cột vị trí 63 mà `itl_ledge_reader.py` đọc làm `le`**. Bảng tra `Tài khoản → Pháp nhân` chỉ 2 cột, đặt trong sheet tên **`Daily RP test`**, không có chủ, không có ai soát.

**Và `ITL Ledge` có HAI cột pháp nhân, có thể trái nhau:**

| Cột | Nguồn | Ai dùng |
|:--:|---|---|
| `P` (`LE`) | `Transaction Mapping L1!AG` — tức **từ P100** | không ai — engine bỏ qua |
| `BL` (`ENITY`) | `VLOOKUP` tài khoản → `Daily RP test!R6:S` | **engine FPA-T4** |

⇒ Cần một phép kiểm `P = BL`; lệch là dấu hiệu sai pháp nhân trong P&L. Ứng viên `INV` mới.

**`Daily RP test` không phải sheet test.** `A3` là một **view báo cáo thật**:

```
A3 = QUERY({'ITL Ledge'!A7:G, 'ITL Ledge'!V7:V, 'ITL Ledge'!P7:P,
            'ITL Ledge'!AD7:AD, 'ITL Ledge'!AH7:AH, 'ITL Ledge'!AL7:AL}, …)
```
→ 7 cột tiền + `Final HDCode` + `LE` + `Final CDT1` + `Final` kỳ đầu/cuối. Cột `N` = `Pháp nhân` = `VLOOKUP(G4,$R$6:$S,2,0)`.

---

## §5 · ★ Bảng đo `[RAW ITL]Data Management` **đếm sai đối tượng** — vì sao nó báo 100%

Công thức thật (dòng 8, nguồn đầu tiên):

```
I8 = IMPORTRANGE(B8, C8&"!V2:V2")                                    <- MẪU SỐ: lấy từ ô V2 của sheet BANK
T8 = COUNTIFS('ITL Ledge'!T:T,"Input here",'ITL Ledge'!$G:$G,$C8)/$I8
S8 = 1-T8                                                            <- cot "Yes"
```

**Ba lỗi cùng lúc:**

| # | Lỗi | Hệ quả |
|--:|---|---|
| 1 | **Tử và mẫu khác tổng thể** — tử đếm dòng trong `ITL Ledge`, mẫu lấy từ ô `V2` của **sheet ngân hàng nguồn** | tỷ lệ **không có nghĩa**; mẫu lớn ⇒ luôn ra ~0% ⇒ cột `Yes` ~100% |
| 2 | **Chỉ đếm ô có chữ `Input here`** | ô **để trống hoàn toàn** cũng được tính là `Yes` ⇒ bảng đo **mù với dòng chưa ai xử** |
| 3 | Đo `Input here` = **đo số lần dùng mặc định**, không phải đo độ phủ | tên cột `Yes`/`No` gợi sai hoàn toàn |

**Bản đồ 5 trường đo `Data Reporting` → cột trong `ITL Ledge`:**

| Trường đo | Đếm cột | Là khối nào |
|---|:--:|---|
| `HD/KRF Code` | `T` | Budget Code |
| `ID Vendor` | `AN` | Mã đối tác |
| `Service Execution Time (PL Date)` | `AF` | Kỳ dịch vụ bắt đầu |
| `Type of Transaction (Regular or Advance)` | `X` | Loại giao dịch |
| `PI Attached` | `AR` | File hoá đơn |

**Bốn trường `ID PC` / `ID PM` / `ID PE` / `ID PI`** (cột `J..R`) **không tính ở đây** — chúng là `IMPORTRANGE` từ **file RAW** (`1xaD1RRA…`). Hai file soi gương nhau đúng như §0.1 checklist.

⇒ **Kết luận về nghi vấn "100% ghép PM"**: **không kết luận được từ bảng này** vì bảng đo hỏng. Phải đếm trực tiếp `COUNTIF` trên `Transaction Mapping L1!N:N` (cần quyền file RAW). `GAP-ITL-25` mới.

**Bộ đếm dòng 3 dùng dải lệch nhau:**

```
T3  = "# Input here = " & COUNTIF(T10:T6747, "Input here")     <- 6747
X3  = … COUNTIF(X10:X5777, …)   AB3, AF3, AJ3, AN3, AR3  <- 5777
```
Chênh **970 dòng**. Nếu dữ liệu vượt 5777 thì **6 trong 7 bộ đếm báo thiếu**. Trong khi `AY8`…`BI8` lại dùng dải **mở đuôi** `COUNTIF(AY10:AY,"FALSE")`. Không nhất quán ⇒ `GAP-ITL-26`.

---

## §6 · Vùng AUDIT — nó **không** kiểm cái ta tưởng

```
AX10 = IMPORTRANGE($AX$2, $AX$3 & AX4)       AX2 = "Report I General Ledger"
AY10 = ArrayFormula(AX10:AX = R10:R)
```

Sáu dải nguồn ở dòng 4: `AX4=!R10:R` · `AZ4=!S10:S` · `BB4=!W10:W` · `BD4=!AE10:AE` · `BF4=!AI10:AI` · `BH4=!AM10:AM`

| Cặp | So cột nào của `ITL Ledge` | Cột đó là gì |
|---|---|---|
| `AY` | `R` | ITL ID |
| `BA` | `S` | **`Classifying`** HDCode |
| `BC` | `W` | **`Classifying`** Loại giao dịch |
| `BE` | `AE` | **`Classifying`** kỳ bắt đầu |
| `BG` | `AI` | **`Classifying`** kỳ kết thúc |
| `BI` | `AM` | **`Classifying`** mã đối tác |

> ⚠ AUDIT so **cột `Classifying`** — tức **giá trị thô từ nguồn**. Nó **không** so cột `Final` (`V`/`Z`/`AD`/`AH`/`AL`/`AP`) là cái engine đọc, và **không** so phần người gõ tay.
>
> ⇒ 6.711 dòng `FALSE` nghĩa là **hai file thượng nguồn không khớp nhau**, **không** nói gì về việc số cuối vào P&L đúng hay sai. Ngược lại: **phần người gõ tay và giá trị `Final` hiện KHÔNG có cổng kiểm nào cả.** Đây là câu trả lời sắc hơn cho `GAP-ITL-11` và là lỗ hổng kiểm soát lớn nhất tìm được đến nay.

---

## §7 · Vùng ALLOCATE — khoá là **HD Code**, không phải Bank Sheet

```
AU10 = ArrayFormula(AD10:AD)                                   <- CFA1 = Final CDT1
AV10 = if(VLOOKUP(V10:V, {'[Importrange]Mapping Master'!H:H, …!K:K}, 2, FALSE)
          = "Need to Allocate to CFA2", "Need to Allocate to CFA2", AU10:AU)
AW10 = if(VLOOKUP(V10:V, {…!H:H, …!L:L}, 2, FALSE) <> "", <đó>, "No need")
```

⇒ Khoá nối là **`Final HDCode` (`V`) → `Mapping Master!H` (`HD Code`)**, lấy cột `K` (`Need to Allocate to CFA2`) và `L` (`Method to Allocate to CFA2`). **Sửa khoá #10 của process map**: khoá là cột **`H`**, không phải cột `A` (`Bank Sheet`).

---

## §8 · Tên sheet live khác bản `.xlsx` — 8 sheet bị đổi tên khi xuất

| Tên thật (live) | Tên trong bản `.xlsx` |
|---|---|
| `[RAW ITL]Data Management` | `RAW ITLData Management` |
| `[Importrange]Mapping Master` | `ImportrangeMapping Master` |
| `H1000 Ledge NIS/INT/COM (HR Allocate HD) Y2025` | `H1000 Ledge NISINTCOM (HR Alloc` |
| `H1000 Ledge NIS/INT/COM (HR Allocate HD) Y2024` | **`Sheet16`** |
| `H1000 Ledge NIS/INT/COM (HR Allocate HD) Y2026` | **`Sheet15`** |
| `H1000 Ledge PIT (HR Allocate HD) Y2025` | `H1000 Ledge PIT (HR Allocate HD` |
| `H1000 Ledge PIT (HR Allocate HD) Y2024` | **`Sheet17`** hoặc **`Sheet18`** |
| `H1000 Ledge PIT (HR Allocate HD) Y2026` | idem |

⇒ **Bốn "Sheet15/16/17/18" bí ẩn trong `_GUIDE_00_Inventory` chính là 4 sổ H1000 của năm 2024 và 2026.** Bản xuất cắt dấu `/` `[` `]` và tên dài. **Mọi tham chiếu sheet trong code TO-BE phải dùng tên live, không dùng tên bản xuất.**

Xác nhận `Index`: 9 dòng `Transaction Mapping L2/L3` và `AP Transaction Original/Audited/L2/L3` **chỉ có tên + `AL`**, **không có `Source`, không có `Flow`** ⇒ **khai mà chưa xây**, không phải đã bỏ.

---

## §9 · Còn chặn

| # | Chặn | Cách mở |
|--:|---|---|
| 1 | SA `claude-code-access@fpa-t-494007.iam.gserviceaccount.com` bị **403** trên file **RAW** (`1xaD1RRA…`) và **PM** (`1U8tDda…`) | **chia sẻ 2 file đó cho email SA, quyền Người xem** — 30 giây, mở được toàn bộ mục còn lại gồm `G7-02` công thức ghép PM↔tiền |
| 2 | Đọc `FORMATTED_VALUE` **treo hoàn toàn** — đã thử cả dải 3 ô (`ITL Ledge!B1:B3`) và cả sheet nhẹ không có `IMPORTRANGE` (`Index!A4:H6`): **cùng timeout**. Nghĩa là **cả workbook phải tính lại** khi đọc giá trị (31 `IMPORTRANGE` chỉ riêng `ITL Ledge`) | chỉ lấy được **công thức**. Muốn lấy giá trị: xuất bản `.xlsx` mới, hoặc `Daily RP test` (view nhẹ) làm cửa đọc, hoặc chấp nhận đọc qua Drive connector |
| 3 | Chưa đọc được `$B$3` (mốc ngày lọc) — ô rỗng ở chế độ `FORMULA` | thuộc chặn #2. **Nếu `B3` thật sự rỗng thì bộ lọc `>$B$3` cho qua mọi dòng** — cần xác nhận |
| 4 | ADC của `thanhnc@apero.vn`: gcloud cảnh báo Google **sắp chặn** scope `spreadsheets.readonly`/`drive.readonly` với client ID mặc định | **không nên đi đường này** — dùng SA ở #1 |

---

## §10 · Việc mở ra từ bước này

| ID | Việc | Vì sao |
|---|---|---|
| `GAP-ITL-25` | Đếm trực tiếp `COUNTIF('Transaction Mapping L1'!N:N,"PM*")` để biết **thật sự** bao nhiêu dòng ghép được PM | bảng đo hiện tại hỏng (§5) |
| `GAP-ITL-26` | Dải bộ đếm lệch nhau `6747` vs `5777` | 6/7 bộ đếm có thể báo thiếu |
| `INV-I15` *(mới)* | `ITL Ledge!P` phải bằng `ITL Ledge!BL` | hai cột pháp nhân, engine chỉ đọc một |
| `INV-I16` *(mới)* | `Final` **không được** bỏ qua giá trị người gõ khi `Classifying` có giá trị | §3 — sửa tay không ăn |
| `AUD-2` *(mới)* | Cổng kiểm cho cột **`Final`** và cho phần **gõ tay** | AUDIT hiện chỉ so `Classifying` (§6) |
| `KILL-1` | `Daily RP test` phải đổi tên và có chủ, hoặc tách bảng `Tài khoản → Pháp nhân` ra sheet danh mục riêng | engine phụ thuộc nó (§4) |
| `QĐ-ITL-19` *(đề xuất)* | Bỏ cơ chế `Input here` → mặc định im lặng; thay bằng **trạng thái `UNMAPPED` tường minh** + báo cáo tồn | §2 — mặc định giấu 6.843 dòng không biết chủ |

---

## Changelog

- **v0.1** (2026-08-20): Đọc live `ITL Ledge` bằng Sheets API `FORMULA` qua SA có sẵn. Xác nhận 4 khẳng định của process map (gồm **12 cột PM/PE/PI bị rơi**). 6 phát hiện mới: **`Input here` = gán mặc định** (`GAC-Other`, `Headquarters2`, `VD0`) · **`Final` bỏ qua giá trị gõ tay khi nguồn có giá trị** · **cột `le` của engine đến từ sheet `Daily RP test`** · **hai cột pháp nhân trái nhau** · **bảng đo đếm sai tổng thể nên luôn báo 100%** · **AUDIT chỉ so `Classifying`, không so `Final`**. Giải mã 4 sheet `Sheet15..18`. Mở `GAP-ITL-25/26`, `INV-I15/16`, `AUD-2`, `KILL-1`, đề xuất `QĐ-ITL-19`.
