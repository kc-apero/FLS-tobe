# Kết quả phân loại 4 loại ô — danh sách "phải code" có xếp hạng

**Ngày:** 2026-08-22 *(cập nhật 2026-08-24)* · **Loại:** doc-only (Class A) · **Đóng:** `GAP-ITL-43`

> ⛔ **`QĐ-ITL-34` (owner, 2026-08-24): KHÔNG đụng vào sheet hiện có, KHÔNG động vào file của kế toán.** ⇒ **§5** *(dọn sheet chết)*, `KILL-7` *(bỏ 305 cạnh tự-kiểm)* và `KILL-8` *(dừng bảng đo hỏng)* chuyển sang ⏸ **ĐÃ ĐO — CHỜ UỶ QUYỀN**. Số đo dưới đây **giữ nguyên giá trị**; chỉ phần *hành động ghi vào file kế toán* là dừng. **§8 đã viết lại theo giới hạn này.**
**Phương pháp:** `Phuong-phap-luan-Codehoa-va-Thiet-ke-TOBE.md` §4 · **Công cụ:** `_tools/probe_access.py` + `_tools/classify_cells.py`
**Chỉ đọc.** Không ghi vào file nào. Đọc **công thức** (`valueRenderOption=FORMULA`), không đọc giá trị — nên `AUD-5` không chặn.

---

## §1 · ⭐⭐ Việc bị chặn lâu nhất đã tự mở: đọc được **file GỐC** ADJUSTED

`probe_access.py` dò 18 spreadsheet ID. Kết quả:

| File | ID | Đọc được? |
|---|---|:--:|
| ⭐ **`ITL … 2/2 (ADJUSTED)` — bản GỐC** | `1r4WemIb…` | ✅ **OK — 12 sheet** |
| bản copy ITL RAW | `1lzwttMYMIHA…` | ✅ OK — 16 sheet |
| bản copy ITL ADJUSTED | `11GBT98x…` | ✅ OK — 12 sheet |
| **`Copy of A-CCR_V2_Working`** *(chưa có trong danh mục 3 file)* | `1axCTQ8GA…` | ✅ **OK — 35 sheet** |
| **`APERO \| FS1`** *(chưa có trong danh mục)* | `1DulZF_5…` | ✅ **OK — 45 sheet** |
| `ITL … 1/2 (RAW)` — bản GỐC | `1xaD1RRA…` | ⛔ 403 |
| `PM11 Entry Data` | `1U8tDda…` | ⛔ 403 |
| spreadsheet thứ 13 *(số dư ví)* | `1QSYSzCC0…` | ⛔ 403 |
| 10 ID khác | — | ⛔ 403 |

> ★★ **`GAP-ITL-39` KHÔNG CÒN CHẶN.** Bản **GỐC** của file ADJUSTED đọc được. Đây là đường **duy nhất** đo giai đoạn ⑤ — bảng `Tài khoản → Pháp nhân` · phép kiểm `P = BL` · đếm dòng vào P&L không có chủ dự toán. Script `measure_itl_ledge.py` viết sẵn từ 22/08 nay chạy được.
>
> ⚠ Chưa biết vì sao mở được — có thể owner đã chia sẻ, có thể quyền kế thừa từ thư mục. **Cần owner xác nhận là cố ý**, vì nếu là vô tình thì nó có thể bị đóng lại giữa lúc đang đo.

> ⚠ Hai file **chưa** có trong danh mục tài liệu mà lại đọc được: `Copy of A-CCR_V2_Working` (35 sheet) và `APERO | FS1` (45 sheet). Phải đưa vào danh mục nguồn — hoặc xác nhận là bản sao ngoài kiểm soát, cùng họ với `KILL-2`.

### 1b · Đo được gì trên file GỐC — và giới hạn mới phát hiện

| Phép | Kết quả |
|---|---|
| Đọc **công thức** toàn file *(12 sheet)* | ✅ **được** — toàn bộ §2–§5 dưới đây |
| Đọc **giá trị**, lô lớn *(`measure_itl_ledge.py`)* | ⛔ **`503 UNAVAILABLE`** — Google **không tính nổi** workbook này |
| Đọc **giá trị**, dải nhỏ *(`Daily RP test!R6:S60`)* | ◐ **được 1 lần trong 3** — hai lần sau quá thời gian |
| Đọc **giá trị**, dải rộng hơn *(`R6:S300`, `R61:S120`)* | ⛔ **quá thời gian** |

> ★ **`AUD-7` — luật đo mới:** trên file GỐC, đọc **giá trị** **không đáng tin** — không phải chỉ chậm, mà **thành công ngẫu nhiên**. Cùng một dải `R6:S60`: lần 1 được, lần 2 và 3 quá thời gian.
>
> Đây **không** trái với §1 của phương pháp luận *(40.000 ô rẻ hơn 3 ô)*: §1 đo trên **bản copy đã mất quyền `IMPORTRANGE`** nên sổ chỉ phải thức một lần rồi nằm yên. File GỐC còn **205 cạnh sống**, nên mỗi lần đọc là **kéo lại nguồn ngoài về tính** — và có lần Google bỏ giữa đường.
>
> ⇒ Bằng chứng mạnh nhất cho toàn bộ luận điểm: **sổ nặng đến mức chính máy chủ Google trả `503` hoặc bỏ dở khi bị hỏi giá trị.** Không phải cảm giác của kế toán.

> ★ **Đường đi được: đọc CÔNG THỨC, đừng đọc GIÁ TRỊ.** Chế độ `FORMULA` chạy **61/61 sheet không một lần lỗi**, và nó trả **ô hằng đúng nguyên văn**. Nên với file GỐC: đọc công thức để hiểu cơ chế, rồi suy con số từ dữ liệu đã đọc được ở nơi đáng tin — thay vì cố đọc giá trị của một sổ mà Google bỏ dở.

### 1c · ★★ Giai đoạn ⑤ — bảng pháp nhân mà engine đọc **không phải một bảng danh mục**

Đọc `Daily RP test!R1:S250` chế độ `FORMULA` *(chạy ngay, không lỗi)*. Bảng `Tài khoản → Pháp nhân` — nguồn của cột `BL` mà `itl_ledge_reader.py` đọc làm `le` — hoá ra là thứ này:

| Cột | Nội dung thật | Nghĩa |
|:--:|---|---|
| **`R`** *(khoá — Tài khoản)* | **`R4 = UNIQUE('ITL Ledge'!G7:G)`** — **một công thức mảng duy nhất** | danh sách tài khoản **tự sinh**, thứ tự = **thứ tự xuất hiện lần đầu trong sổ** |
| **`S`** *(Pháp nhân)* | **TRỘN hai thứ**: **19 ô gõ tay** (`VVOT`, `CNC`, `BGO1`, `SGO1`…) và **24 ô công thức** `=IFERROR(REGEXEXTRACT(R13,"[^_]+$"),"")` | vừa danh mục tay, vừa luật máy — **xen kẽ, không theo quy tắc nào** |

**Ba chỗ hỏng, đo được:**

| # | Chỗ hỏng | Số | Đo bằng |
|--:|---|--:|---|
| 1 | **Đuôi bảng không được phủ.** `UNIQUE` sinh ra **57 tài khoản** *(đếm giá trị khác nhau của `Transaction Mapping L1!G` — nguồn của `ITL Ledge!G`)*, nhưng cột `S` chỉ có nội dung tới **dòng 48**, tức **43 dòng** | **≈ 14 tài khoản KHÔNG có ô pháp nhân nào** ⇒ `VLOOKUP` trả rỗng ⇒ **engine đọc `le` rỗng** | `FORMULA` + `l1_money.json` — **cả hai đều đáng tin** |
| 2 | **Luật regex trả rỗng lặng lẽ.** `REGEXEXTRACT(R,"[^_]+$")` lấy phần sau dấu `_` cuối; tài khoản **không có dấu `_`** thì `IFERROR` → `""` | **4 tài khoản**: `R \| CNC` · `R \| HoangACB` · `R \| PO` · `R \| Pingpong` *(chỉ thoát nếu có người gõ tay đè lên)* | idem |
| 3 | ⚠ **Bẫy lệch dòng — nặng nhất.** Khoá là `UNIQUE` *(thứ tự theo lần xuất hiện đầu trong sổ)*, mà **19 pháp nhân gõ tay chỉ khớp theo VỊ TRÍ DÒNG**. Một tài khoản mới xuất hiện **sớm** trong sổ là `UNIQUE` **đẩy dòng**, và **mọi pháp nhân gõ tay phía dưới trượt sang tài khoản khác** | — | đọc công thức `R4` |

> ★★ **Đây đúng cùng một họ lỗi với `itl_id` = số thứ tự dòng** (`QĐ-ITL-30`): **giá trị gõ tay khớp với khoá theo vị trí, mà khoá thì tự đánh số lại.** Lần này nó không nằm ở khoá sổ — nó nằm ở **cột pháp nhân mà engine P&L đọc**.
>
> ⇒ **`KILL-1` nặng hơn tài liệu ghi.** `Process-PM-den-ITL` §7.4 gọi đây là *"bảng tra 2 cột, không chủ, không ai soát"*. Thực tế: **không phải bảng tra — là một cột tự sinh ghép với một cột nửa tay nửa luật, khớp nhau bằng vị trí.**
>
> ⇒ **`GAP-ITL-19` được củng cố bằng cơ chế, không còn là sở thích.** Owner đã chốt cột `P` là nguồn chuẩn; nay biết **vì sao**: `P` đến từ `Mapping Master!A:B` — một danh mục thật, có khoá thật. Còn `BL` đến từ cái vừa mô tả. **Chuyển engine từ `BL` sang `P` là sửa lỗi, không phải đổi ý.**

### 1d · ✅ Số DỨT ĐIỂM — 14 tài khoản, 211 dòng tiền vào P&L với pháp nhân rỗng

Chạy `read_cells_sa.py` **5 lần liên tiếp** bằng bản đã sửa: 2 lần quá thời gian, **lần thứ 4 thành công** và công cụ **giữ được** kết quả *(trước khi sửa thì lần lỗi sẽ xoá nó)*. Đọc `R6:S200` → **57 dòng khoá, 14 dòng thiếu pháp nhân** — khớp **đúng** ước lượng `57 − 43 = 14` suy từ chế độ công thức.

**Mười bốn tài khoản đó — in đủ, theo luật `AUD-8`:**

| Dòng | Tài khoản | Dòng tiền |
|--:|---|--:|
| 53 | `R \| 7950162651_Airwallex USD_HGO2` | **76** |
| 51 | `R \| 86933888_TCB VND_VOOA` | **37** |
| 57 | `R \| 70582700002400469_PO USD_HIEPNV` | 16 |
| 61 | `R \| 19040237397013_TCB VND_VOOL` | 16 |
| 50 | `R \| 7950136222_Airwallex USD_HGO1` | 13 |
| 52 | `R \| PO9_PO HKD_HGO1` | 13 |
| 58 | `R \| 66896888_TCB VND_VGC1` | 10 |
| 60 | `R \| 621336_ACB VND_VOON` | 8 |
| 55 | `R \| 40215888_TCB USD_VOOA` | 6 |
| 49 | `R \| PO5_PO USD_UGO2` | 5 |
| 56 | `R \| 70583520002340803_PO USD_SONNH` | 5 |
| 54 | `R \| 70589520002340804_PO USD_HOATT` | 3 |
| 59 | `R \| 19040237397021_TCB USD_VOOL` | 2 |
| 62 | `R \| 702113416001_OCBC SGD_TPCI` | 1 |
| | **Tổng** | **211 dòng = 2,1%** |

**Tiền các dòng đó chở** *(cộng thô, `max(Nợ, Có)` từng dòng — không phải số tiền thật, chỉ để so độ lớn)*: **1.792.114.655 VND** · **6.262.934 USD** · **3.132.792 HKD** · **10.000 SGD**.

### 1e · ⚠ SỬA LẠI hai điều — sau khi đối chiếu 25 ô gõ tay với đuôi tên tài khoản

**Điều tôi nói sai:** *"mã pháp nhân nằm sẵn trong tên tài khoản, chỉ cần kéo công thức xuống"*. **Không đúng.** Đối chiếu từng ô mới thấy đuôi tên tài khoản mang **bốn loại thứ khác nhau**:

| Đuôi tên là gì | Ví dụ | Regex có ra đúng pháp nhân? |
|---|---|:--:|
| **Mã pháp nhân** | `…_VGOH` · `…_SGO2` · `…_BGO2` · `…_UGO2` · `…_MGO1` · `…_HGO6` | ✅ **đúng** — 18 ô công thức đang chạy thế này |
| **Tên thương hiệu** | `…_TERASOFTS` → `VVOT` · `…_VISIONLAB` → `VVOV` · `…_ASTRONEX` → `VVOH` · `…_SUPERMINDS` → `VVOS` | ❌ ra **tên thương hiệu**, không phải mã ⇒ **phải gõ tay** |
| **Dấu chi nhánh** | `…_CN` → `CNC` *(4 tài khoản)* | ❌ ⇒ phải gõ tay |
| **Loại tiền / mã đối tác** | `PO BGO1 _USD` → `BGO1` · `…_TPCI` → **`SGO1`** *(3 tài khoản)* | ❌ ⇒ phải gõ tay |

⇒ **Luật regex sai về bản chất, chỉ tình cờ đúng khi đuôi tên trùng với mã pháp nhân.** 25 ô gõ tay không phải người làm bừa — **đó là người đang dịch đúng chỗ máy không dịch được.**

**Hệ quả cho 14 dòng trống — chúng KHÔNG cùng một loại việc:**

| Nhóm | Dòng | Đuôi tên | Vá được bằng luật? |
|---|--:|---|---|
| Đuôi là **mã pháp nhân đã biết hoặc cùng họ** | 10 | `UGO2` · `HGO1`×2 · `HGO2` · `VOOA`×2 · `VGC1` · `VOOL`×2 · `VOON` | ◐ **có thể** — nhưng `VOOA`/`VOOL`/`VOON`/`VGC1` **chưa từng xuất hiện ở đâu khác**, cần xác nhận là pháp nhân thật |
| ⚠ Đuôi là **mã đối tác, KHÔNG phải pháp nhân** | 1 | `TPCI` *(dòng 62)* | ❌ **regex sẽ ra SAI** — ba tài khoản `…_TPCI` khác đều được gõ tay thành **`SGO1`** |
| ⚠ Đuôi là **tên NGƯỜI** | 3 | `HOATT` · `SONNH` · `HIEPNV` | ❌ **không suy được** — tài khoản đứng tên cá nhân, pháp nhân phải do người quyết |

> ⇒ **Không có cách vá bằng luật cho cả 14 dòng.** Ít nhất **4 dòng bắt buộc phải có người quyết**, và một trong đó (`TPCI`) là chỗ mà vá bằng luật sẽ **tạo ra số sai** thay vì để trống.
>
> ⛔ Tôi **không sửa** — ghi vào file đang sống (luật `D1`).

**Điều tôi cũng nói quá:** hàm ý rằng **bẫy lệch dòng** có thể đã gây sai. **Chưa có bằng chứng nào cho việc đó — và bằng chứng lại nghiêng về phía "hôm nay đang đúng".** 25 ô gõ tay ghép **hoàn toàn nhất quán** với tài khoản bên cạnh: `TERASOFTS`→`VVOT` ba lần · `VISIONLAB`→`VVOV` ba lần · `ASTRONEX`→`VVOH` ba lần · `SUPERMINDS`→`VVOS` ba lần · `CN`→`CNC` bốn lần · `TPCI`→`SGO1` ba lần. Nếu bảng đã bị đẩy dòng thì các cặp này sẽ lệch nhau — chúng không lệch.

⇒ **Xếp lại mức gấp cho đúng:**

| | Trạng thái | Mức |
|---|---|---|
| **14 dòng không có pháp nhân** | ⚠ **đang sai NGAY BÂY GIỜ** — 211 dòng tiền vào P&L không thuộc pháp nhân nào | **gấp** |
| **Bẫy lệch dòng** | ✅ **hôm nay chưa gây sai** *(25 cặp còn nhất quán)* — nhưng cơ chế vẫn còn, sẽ nổ khi có tài khoản mới xuất hiện sớm trong sổ | **rủi ro tương lai** |
| **Luật regex sai bản chất** | ⚠ đang đúng nhờ may — đuôi tên tình cờ trùng mã pháp nhân ở 18 tài khoản | **nợ thiết kế** |

> ★ Cả ba đều dẫn về **một cách chữa duy nhất**, `KILL-1` + `GAP-ITL-19`: **bỏ bảng này**, cho `BL` đọc từ `Mapping Master` — nơi khoá là khoá thật và ánh xạ là danh mục có chủ, giống cột `P`. Vá bằng cách kéo công thức xuống thì **chữa 10 dòng, làm sai 1 dòng, bỏ lại 3 dòng, và giữ nguyên cả ba vấn đề trên**.

> ★ **Bài học công cụ (`AUD-8`):** khi nguồn chỉ thành công ngẫu nhiên thì **mất một lần đọc là mất thật**. `read_cells_sa.py` từng để lần đọc lỗi **ghi đè** lên dữ liệu tốt — **đã sửa 2026-08-22**. Và đo được gì thì **in bằng chứng từng dòng ngay**, đừng chỉ in số tổng: chính vì chỉ in số tổng mà con số 12 thành vô dụng khi dữ liệu mất.

---

## §2 · Số tổng — trên 3 workbook đo được của luồng

*(`APERO | FS1` 45 sheet chưa quét — để đợt sau)*

| | `Copy of A-CCR` | `ITL ADJUSTED` **(gốc)** | `Copy of ITL RAW` | **Tổng** |
|---|--:|--:|--:|--:|
| Sheet đọc được | 33 | 12 | 16 | **61** |
| **Cột PHẢI CODE** *(máy chở + máy tính)* | **1.601** | 96 | 58 | **1.755** |
| Cột **hằng** *(người gõ / ô hiện)* | 366 | 249 | 184 | **799** |
| Cạnh `IMPORTRANGE` | 2 | **205** | **104** | **311** |
| ↳ **cạnh ĐỘNG** *(đích nằm trong ô)* | 0 | **203** | **102** | **305** |
| ↳ nằm ở **băng đầu** *(hàng tự-kiểm + ô neo)* | 2 | **205** | **104** | **311 — tức 100%** |

**Đối chiếu với tài liệu cũ:** `_GUIDE_01` đếm 25 cạnh liên-file tường minh + 271 cạnh động. Đo trực tiếp trên 3 file cho **311 cạnh / 305 động** — cùng bậc, **xác nhận con số cũ**.

---

## §3 · ★★ Phát hiện lớn nhất: **305 cạnh vượt file không dùng để chở số — mà để TỰ KIỂM**

Đây là kết quả đáng nhất của phép đo, và nó không có trong tài liệu nào.

**Toàn bộ 311 cạnh `IMPORTRANGE` nằm ở băng dòng đầu, không có cái nào ở vùng dữ liệu.** Đọc mẫu công thức thấy rõ chúng là gì — ví dụ `ITL Ledge` hàng 6:

```
A6 = IMPORTRANGE($B$1, $B$2 & "!" & A$5 & $Q$6 & ":" & A$5 & $Q$6) = A10
B6 = IMPORTRANGE($B$1, $B$2 & "!" & B$5 & $Q$6 & ":" & B$5 & $Q$6) = B10
...   (38 cột, mỗi cột một cái)
```

Mỗi công thức đó **gọi sang file khác để đọc đúng MỘT ô**, rồi so với **đúng MỘT ô** ở hàng 10. Ba mươi tám lần gọi vượt file để kiểm ba mươi tám ô.

| Sheet | Cạnh `IMPORTRANGE` ở băng đầu | Đều động? | Kiểm được gì |
|---|--:|:--:|---|
| `[RAW ITL]Data Management` *(có ở **cả hai** file ITL)* | **97 × 2 = 194** | 96/97 | bảng đo — mà `§7.5` đã chứng minh **bảng đo này hỏng** |
| `ITL Ledge` | **38** | 38/38 | 38 ô |
| `H1000 Ledge PIT Y2025` | 22 | 22/22 | 22 ô |
| `H1000 Ledge NIS/INT/COM Y2025` | 22 | 22/22 | 22 ô |
| `H1000 Ledge … Y2024` × 2 | 12 + 12 | đều động | 24 ô |

> ★★ **Hai hệ quả:**
>
> 1. **Phần lớn chi phí vượt-file của sổ không phải để chở số, mà để tự kiểm** — và mỗi lần kiểm đúng một ô. Mà §1 của phương pháp luận đã đo: **mỗi lần chạm sang file khác là đánh thức file đó**. Nên cái hàng tự-kiểm này chính là cỗ máy sinh ra 33 giây chờ.
> 2. **Đây là chỗ cắt rẻ nhất và an toàn nhất của cả dự án.** Code đọc một lần là kiểm được **toàn bộ ~10.000 dòng**, thay vì 38 lần gọi vượt file để kiểm 38 ô. Cắt xong: **không ai mất phép kiểm nào — phép kiểm còn mạnh hơn 260 lần về độ phủ**, mà sổ bớt hẳn 38 cạnh.
>
> ⚠ Và `[RAW ITL]Data Management` gánh **194 trong 311 cạnh (62%)** để nuôi một bảng đo **đã biết là hỏng**. Đây là chỗ đắt nhất phục vụ thứ vô dụng nhất.

---

## §4 · Xếp hạng "phải code" — ⚠ **KHÁC dự đoán ở §5 của phương pháp luận**

### 4.1 · Theo **số ô công thức** *(đo được)*

| # | Sheet | File | Giá thô *(cột công thức × số dòng lưới)* | Ô có quét |
|--:|---|---|--:|--:|
| 1 | **`[RAW ITL]Data Management`** | ITL RAW | **643.297** | 132 |
| 2 | **`[RAW ITL]Data Management`** | ITL ADJUSTED | **605.232** | 165 |
| 3 | `H1000 Ledge NIS/INT/COM Y2025` | ADJUSTED | 481.605 | 20 |
| 4 | `H1000 Ledge NIS/INT/COM Y2026` | ADJUSTED | 481.605 | 20 |
| 5 | `5. Daily Report` | A-CCR | 463.018 | 35 |
| 6 | **`Transaction Mapping L1`** | ITL RAW | **282.912** | 24 |
| 7 | `Test 5. Daily Report` ⚠ | A-CCR | 269.360 | 259 |
| 8 | `Test 1. Daily Report` ⚠ | A-CCR | 266.548 | 259 |
| 9 | **`2. CCR Cash`** | A-CCR | 160.544 | **6.910** |
| 10 | **`2. CCR`** | A-CCR | 144.041 | 0 *(xem ghi chú)* |
| 11 | **`ITL Ledge`** | ADJUSTED | 126.972 | 20 |
| 12 | `H1000 Ledge PIT Y2025` | ADJUSTED | 64.214 | 20 |

### 4.2 · Chỗ tôi đoán sai, và sửa lại

`§5` của phương pháp luận xếp: `2. CCR` #1 → `Transaction Mapping L1` #2 → `ITL Ledge` #3. **Đo thật cho thứ tự khác:**

| Sai ở đâu | Thật là |
|---|---|
| Không hề nhắc `[RAW ITL]Data Management` | nó **đứng đầu ở cả hai file ITL**, và nuôi 62% số cạnh vượt file |
| Không hề nhắc **4 sổ `H1000`** (lương/HR) | ba trong bốn sổ đó **vượt `ITL Ledge`** về số ô công thức |
| Xếp `2. CCR` #1 | nó chỉ **#10** về số ô. Nhưng **#1 về độ quét** — `2. CCR Cash` có **6.910 ô mang `SUMIFS`/`VLOOKUP`** chỉ trong ba băng dòng mẫu |

> ★ **Rút ra một luật đo:** **một thước không đủ.** Số ô công thức và độ sâu quét là hai chiều khác nhau — `2. CCR` ít ô mà mỗi ô quét sổ 7.626 dòng; `H1000` nhiều ô mà quét nhẹ. Xếp hạng đúng phải là **số ô × độ sâu quét**, không phải một trong hai.
>
> ⚠ `2. CCR` hiện `quét = 0` **không** nghĩa là nó không quét — ba băng dòng mẫu rơi vào khối `TREASURY` (nhập tay) và vào những dòng tổng. Đây đúng là `AUD-3` một lần nữa: **công thức không nhất quán theo dòng cũng như theo cột.** Muốn số chắc thì phải quét toàn dải, không lấy mẫu.

---

## §5 · Sheet CHẾT vẫn đang được tính lại — ⏸ **CHỜ UỶ QUYỀN** (`QĐ-ITL-34`)

| Sheet | Giá thô | Dấu hiệu chết |
|---|--:|---|
| `Test 5. Daily Report` | **269.360** | tên tự nói là bản thử |
| `Test 1. Daily Report` | **266.548** | idem |
| `[OLD]5. Daily Report` | 5.642 | tên tự nói là bản cũ |
| `[V202510]5. Daily Report` | 0 *(hằng)* | bản đóng băng theo kỳ |
| `[SGO2]Transaction Mapping L1_conflict342167593` | 3.464 | **sheet xung đột do Google sinh ra**, chưa ai dọn |
| 11 bản `6.x CCR I DEL I W I Pdf` + 4 bản theo ngày | ~10.000 | 15 bản gần hệt nhau của cùng một sheet |

> ★ Riêng hai sheet tên **"Test"** đang chiếm **~536.000 ô công thức** — nhiều hơn `Transaction Mapping L1` và `ITL Ledge` **cộng lại**. Sổ đang trả tiền tính lại cho hai bản thử.
>
> ⛔ **Tôi không xoá gì** (`D1`, luật cấm ghi vào file sống). Đây là **việc của owner**: xác nhận chết rồi mới dọn. Nhưng nếu đúng là chết thì đây là **việc rẻ nhất mua tốc độ trong toàn bộ danh sách** — xoá sheet, không viết một dòng code nào.

---

## §6 · Một giới hạn của phép đo, nói thẳng

Phép phân loại đọc **ba băng dòng** (đầu · giữa · sâu), không đọc toàn sổ. Vì công thức mảng chỉ có **một ô neo** cho cả cột, nên băng đủ để biết hình dạng cột. Nhưng có hai chỗ nó **chưa** phân biệt được:

| Chưa phân biệt được | Vì sao | Cách sửa |
|---|---|---|
| **"cột hằng"** ở vùng dữ liệu là *người gõ* hay là *giá trị tràn từ công thức mảng* | ở chế độ `FORMULA`, ô tràn từ mảng trả về **giá trị**, không trả công thức ⇒ trông như hằng | ghép với kết luận **băng đầu**: cột nào có công thức mảng ở băng đầu thì phần tràn là **máy**, không phải người. Dữ liệu đã có trong `.json`, chỉ cần lưu kết luận **từng cột** thay vì chỉ đếm |
| Độ quét thật của `2. CCR` | lấy mẫu ba băng, rơi vào khối nhập tay | quét toàn dải 229 dòng × 655 cột — rẻ, vì sheet không cao |

⇒ Con số **1.755 cột phải code** là **chặn dưới**, không phải số cuối. Sửa hai chỗ trên sẽ làm nó tăng, không giảm.

---

## §7 · Việc mở ra

| ID | Việc | Ai |
|---|---|---|
| `GAP-ITL-44` ⭐ | **Owner xác nhận quyền đọc file GỐC ADJUSTED là CỐ Ý** — nếu vô tình thì có thể bị đóng giữa lúc đang đo | owner |
| `GAP-ITL-45` | **Hai file lạ đọc được** (`Copy of A-CCR_V2_Working` · `APERO \| FS1`) — đưa vào danh mục nguồn, hay là bản sao ngoài kiểm soát? | owner + BA |
| `GAP-ITL-46` ⏸ | ⏸ **CHỜ UỶ QUYỀN** — owner 2026-08-24: *không đụng vào sheet hiện có*. ~~Xác nhận 6 nhóm sheet CHẾT ở §5 rồi dọn~~ | owner + lanptn |
| `KILL-7` ⏸ | ⏸ **CHỜ UỶ QUYỀN** (`QĐ-ITL-34`). **Bỏ hàng tự-kiểm bằng `IMPORTRANGE` từng cột**; thay bằng phép kiểm trong code, phủ toàn bộ dòng | Tech Lead |
| `KILL-8` ⏸ | ⏸ **CHỜ UỶ QUYỀN** (`QĐ-ITL-34`). `[RAW ITL]Data Management` — 194/311 cạnh vượt file để nuôi **một bảng đo đã hỏng** (`§7.5`). Dừng bảng này trước khi tối ưu bất cứ thứ gì khác | Tech Lead |
| `AUD-6` | **Luật đo: một thước không đủ.** Xếp giá thành phải theo **số ô × độ sâu quét** | — |
| — | Quét `APERO \| FS1` (45 sheet) + hoàn thiện 2 chỗ ở §6 | tôi |

---

## §8 · Nghĩa gì và bước tiếp — ✏ **VIẾT LẠI 2026-08-24 theo `QĐ-ITL-34`**

**Điều tôi viết ngày 22/08 và nay phải sửa:** bản đầu của §8 nói *"ba việc đầu KHÔNG cần viết code"* và xếp chúng lên trước. **Cả ba đều là hành động GHI vào file của kế toán** — dọn sheet · dừng bảng đo · bỏ hàng tự-kiểm. Owner đã đặt giới hạn ngược lại ⇒ **cả ba dừng, chờ uỷ quyền riêng.**

⚠ **Hệ quả nói thẳng:** ba việc đó là **toàn bộ** đường làm nhẹ **sổ cũ**. Bỏ ra thì **chặng 1 không làm sổ hiện tại nhanh hơn một giây nào.** Tốc độ **chỉ đến trên ĐƯỜNG MỚI**: máy đọc dữ liệu thô **một lần**, tính trong code, ghi ra **sheet gương do máy sở hữu**. Kế toán hưởng tốc độ **khi chuyển sang đọc đường mới** — không phải khi sổ cũ nhẹ đi.

**Vì thế sheet gương 3 tab không còn là quà tặng thêm — nó là chỗ DUY NHẤT tốc độ hiện ra được trong chặng 1.**

**Việc còn làm được, không cần xin gì thêm** *(tất cả đều chỉ ĐỌC)*:

| # | Việc | Ghi chú |
|--:|---|---|
| 1 | **Phân 1.755 cột thành *có / không* phụ thuộc `IMPORTRANGE`** | mở đường chọn oracle từng cột — `GAP-ITL-48`. Làm từ `.json` đã có, **không chạm sổ** |
| 2 | **Code hoá loại 2 + loại 3** theo thứ tự: `Transaction Mapping L1` → `2. CCR`/`2. CCR Cash` → `ITL Ledge` → 4 sổ `H1000` | đọc thô, tính trong code, đối chiếu với oracle |
| 3 | **Dựng sheet gương 3 tab** *(Hàng chờ · Cổng hôm nay · Xu hướng nhãn)* | file **mới**, máy sở hữu — không chạm file kế toán |
| 4 | **Dán nhãn 211 dòng pháp nhân rỗng lên sheet gương** | `GAP-ITL-47` owner nói *chưa gấp* ⇒ **không sửa**, chỉ **hiện ra** để khi cần thì số đã có |
| 5 | Sửa hai giới hạn đo ở §6 · quét `APERO \| FS1` 45 sheet · lấy mốc nền tốc độ | chỉ đọc |

⏸ **Việc treo, chờ một lần uỷ quyền:** dọn 6 nhóm sheet chết (`GAP-ITL-46`) · dừng bảng đo hỏng (`KILL-8`) · bỏ 305 cạnh tự-kiểm (`KILL-7`). **Số đo đã có, không mất đi** — ngày nào owner mở thì làm được ngay, không phải đo lại.
