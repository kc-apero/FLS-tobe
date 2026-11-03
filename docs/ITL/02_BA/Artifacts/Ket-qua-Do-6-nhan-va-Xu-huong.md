# Kết quả đo: sáu nhãn "không cần lệnh chi" và xu hướng theo tháng

**Version:** v0.3 · **Ngày:** 2026-08-24 *(⛔ header từng đứng ở v0.1 — sửa 27/08)* · **Tầng:** L1 · **Loại:** kết quả đo

**Vì sao có bản này:** ba trong bảy việc sửa demo (`việc 2` · `việc 6` · `việc 7`) không thể đóng bằng cách vẽ thêm màn — chúng cần **số đo**. Bản này là phép đo đó.

**Nguồn:** `Copy of ITL I Input Transaction Ledger File 1/2 (RAW)` ▸ sheet `Transaction Mapping L1`, dải `A5:AL10104`.
Cột dùng: `A` Ngày chứng từ · `C` Diễn giải · `E` PS Nợ · `F` PS Có · `G` Tài khoản · `N` ID PMLine.

---

## §1 · Trả lời gọn

| Câu hỏi | Trả lời |
|---|---|
| Tách được 6 nhãn không? | **Được.** `1.814` dòng · `195,60 tỷ` · **84,6% tiền** |
| Có khớp con số `3.480 / 92%` của tài liệu? | **Tiền: khớp gần đúng** (84,6% vs 92%). **Số dòng: KHÔNG** — 1.814 vs 3.480 |
| Vì sao lệch? | ⚠ **Luật sinh ra 3.480 không được ghi ở tài liệu nào, không script nào tạo ra nó** ⇒ `GAP-ITL-56` |
| Xu hướng theo tháng đo được không? | **Được** — và máy **bắt được một cái phình thật**: `Lương & thưởng` tháng 8 gấp hơn 3 lần mức thường |
| Có phép đối chứng nào không? | **Có hai, cả hai đều đạt** — xem §2 |
| ⭐ Phát hiện nặng nhất | **Chuỗi 12 dòng đúng bằng nhau `490.000.000`** tới cùng một tài khoản, đánh số `Lần 1…12`, **không dòng nào có lệnh chi** |
| ⭐ Sửa một ghi chép sai của dự án | **File GỐC `ITL ADJUSTED` ĐỌC ĐƯỢC.** Ghi chép "404 / mất quyền" là sai |

---

## §2 · Hai phép đối chứng — làm trước khi tin bất cứ số nào

Trước khi báo số mới, phải chứng minh đường đọc của tôi cho ra được **số đã biết**.

| Phép đối chứng | Tài liệu | Đo lại | Kết |
|---|--:|--:|:--:|
| Số dòng **đã ghép lệnh** *(`ID PMLine` bắt đầu `PM`)* | **3.344** | **3.344** | ✅ khớp tuyệt đối |
| **50 dòng lớn nhất** của nhóm `CHƯA BIẾT` gánh bao nhiêu tiền | **89,3%** | **89,8%** | ✅ lệch 0,5 điểm |

⇒ Đường đọc đúng. Nên khi số khác tài liệu, **cái khác là luật phân loại, không phải phép đọc**.

### ✓ `AUD-5` không chặn — đã kiểm, không phải đoán

Cột `N` có **6.756 ô lỗi**. Luật `AUD-5` bắt phải xét trước khi kết luận. Đã đếm từng giá trị:

| Giá trị lỗi | Số ô | Nghĩa |
|---|--:|---|
| `#N/A` | **6.756** | `VLOOKUP` **không tìm thấy** ⇒ đây chính là tín hiệu *"chưa ghép được lệnh"*, **là dữ liệu, không phải lỗi** |
| `#REF!` | **0** | ⇒ **không có bẫy bản copy** |

★ Đây là lý do phải đếm chứ không được nhìn: nếu tôi thấy "6.756 ô lỗi" rồi bỏ phép đo theo `AUD-5`, tôi đã bỏ mất **đúng cột mang thông tin cần đo**.

---

## §3 · Việc 2 — sáu nhãn, đã tách

**Phạm vi:** `5.020` dòng **tiền RA chưa ghép được lệnh** *(có `PS Có`, không `PS Nợ`, `ID PMLine` không bắt đầu `PM`)*, tổng **231,19 tỷ** nguyên tệ.

| Nhãn | Dòng | % dòng | Tiền (nguyên tệ) | % tiền |
|---|--:|--:|--:|--:|
| **CÓ LỆNH — mã trong diễn giải** | 158 | 3,1% | 19.571.487.967 | 8,5% |
| Lãi & phí bank | 501 | 10,0% | 8.497.494 | 0,0% |
| **Điều chuyển nội bộ & đổi tệ** | **184** | **3,7%** | **179.286.150.309** | **77,6%** |
| Lương & thưởng | 98 | 2,0% | 11.868.250.807 | 5,1% |
| Thuế | 107 | 2,1% | 4.341.891.639 | 1,9% |
| Doanh thu nền tảng | **914** | **18,2%** | 45.562.344 | **0,0%** |
| Quẹt thẻ | 10 | 0,2% | 45.089.735 | 0,0% |
| **CHƯA BIẾT — việc của người** | 3.048 | 60,7% | 16.019.159.794 | 6,9% |
| **TỔNG 6 nhãn KHÔNG CẦN LỆNH** | **1.814** | **36,1%** | **195.595.442.331** | **84,6%** |

### ★★ Hai dòng của bảng này chứng minh nguyên tắc "xếp theo TIỀN"

| Nhãn | Dòng | Tiền | Đọc |
|---|--:|--:|---|
| Điều chuyển nội bộ | **3,7%** | **77,6%** | ít việc, gần hết tiền |
| Doanh thu nền tảng | **18,2%** | **0,0%** | nhiều việc, không đáng tiền |

Nếu hàng chờ xếp theo **số dòng**, người sẽ dành 18,2% công cho nhóm gánh **0,0%** tiền và bỏ qua nhóm gánh **77,6%**. Đây là bằng chứng số cho `QĐ-ITL-27`, không còn là lập luận.

Và **điều chuyển nội bộ gần như toàn bộ là một câu**: *"Chuyển khoản từ TCB sang VPbank"* — tiền đi từ túi này sang túi khác của chính công ty. Đúng loại vốn **không thể có lệnh chi**.

### Luật khớp chữ đã dùng — ⚠ luật này là của tôi

Máy chuẩn hoá diễn giải *(bỏ dấu, hạ chữ thường)* rồi xét theo **thứ tự**, dừng ở nhãn đầu tiên khớp:

| Thứ tự | Nhãn | Dấu hiệu |
|--:|---|---|
| 0 | CÓ LỆNH | mẫu `PM` + 4 chữ số trở lên trong diễn giải |
| 1 | Lãi & phí bank | `lãi tiền gửi` · `lãi suất` · `phí ngân hàng` · `phí chuyển tiền` · `phí SMS` · `phí thường niên` · `bank fee` · `interest` … |
| 2 | Điều chuyển nội bộ & đổi tệ | `điều chuyển` · `nội bộ` · `mua/bán ngoại tệ` · `quy đổi` · **mẫu `chuyển khoản/tiền … từ X sang Y`** · `nạp/rút tiền TK` |
| 3 | Lương & thưởng | `lương` · `thưởng` · `BHXH` · `bảo hiểm` · `phụ cấp` · `salary` · `bonus` … |
| 4 | Thuế | `thuế` · `VAT` · `TNCN` · `TNDN` · `GTGT` · `lệ phí` · `tax` |
| 5 | Doanh thu nền tảng | `doanh thu` · `payout` · `Google` · `Facebook` · `TikTok` · `AdMob` · `Unity` · `AppLovin` · `Apple` … |
| 6 | Quẹt thẻ | `quẹt thẻ` · `thẻ tín dụng` · `credit card` · `POS` |

⚠ **Luật còn lỗ tôi đã biết.** Dòng `CHƯA BIẾT` lớn nhất là **1,07 tỷ**, diễn giải `NTDT+KB:0011-Kho bac Nha nuoc Khu vuc I+NgayNT:02082026+MST:` — đó là **nộp thuế điện tử**, đáng vào nhãn `Thuế`, nhưng luật của tôi tìm chữ `thuế` nên không bắt được `NTDT` và `Kho bạc`. ⇒ **Luật phải do kế toán chốt, không phải do tôi đoán.**

---

## §4 · ⚠ `GAP-ITL-56` — con số `3.480 / 92%` không lặp lại được

| | Số dòng | % tiền |
|---|--:|--:|
| Tài liệu ghi *(đo 22/08)* | **3.480** | **92%** |
| Đo lại 24/08, luật ghi rõ ở §3 | **1.814** | **84,6%** |

**Đã tìm:** không tài liệu `.md` nào ghi luật khớp 6 nhãn; không script `.py` nào trong repo sinh ra `3.480`. Bốn tên nhãn có trong `QĐ-ITL-28`, nhưng **cách nhận ra chúng thì không**.

**Ý nghĩa, tách làm hai — không gộp:**

| Kết luận | Trạng thái |
|---|---|
| *"Phần lớn TIỀN đi qua đường không cần lệnh chi"* | ✅ **VẪN ĐỨNG** — 84,6% và 92% cùng nói một điều. `QĐ-ITL-28` không bị lung lay |
| *"Sau khi dán nhãn, hàng chờ còn **1.478 dòng**"* | ⚠ **KHÔNG lặp lại được** — luật của tôi để lại **3.048 dòng**, gấp hơn hai lần |

⇒ Việc phải làm: **kế toán chốt luật 6 nhãn**, rồi chạy lại một lần. Trước khi có luật đó, mọi con số *số dòng* của hàng chờ là **số theo luật của người đo**, không phải sự thật của sổ.

★ Đây cũng là ví dụ sống cho luật `GAP-ITL-54`: một con số **đã đo** vẫn có thể **không tái lập được** nếu **luật đo không được ghi lại cùng nó**. Từ nay mọi phép đo phân loại phải ghi kèm luật.

---

## §5 · Việc 6 — xu hướng theo tháng, đã đo

Số dòng mỗi nhãn theo tháng, trên cùng tập `5.020` dòng:

| Nhãn | 2026-03 | 04 | 05 | 06 | 07 | 08 | Báo |
|---|--:|--:|--:|--:|--:|--:|---|
| Lãi & phí bank | 30 | 36 | 35 | 47 | 47 | 23 | — |
| Điều chuyển nội bộ & đổi tệ | 13 | 17 | 12 | 16 | 5 | 3 | — |
| **Lương & thưởng** | 2 | 4 | 4 | 2 | 8 | **13** | 🔴 **hơn 3 lần mức thường (4)** |
| Thuế | 6 | 23 | 5 | 2 | 10 | 14 | — |
| Doanh thu nền tảng | 56 | 57 | 66 | 85 | 98 | 108 | — *(tăng đều, không phải phình)* |
| Quẹt thẻ | 0 | 0 | 0 | 0 | 0 | 0 | — |
| `CHƯA BIẾT` | 257 | 218 | 150 | 159 | 162 | 136 | — |

**Ba hình dạng đáng đọc:**

1. 🔴 **`Lương & thưởng` phình** — 13 dòng so với mức thường 4. Máy **không phán khoản đó sai**; máy nói *"chỗ này đang phình, đi xem"*. Đây đúng là điều `US-KT-041` cần: **cái nhãn không được thành cửa sau**.
2. **`Doanh thu nền tảng` tăng đều 56 → 108** — tăng thật, không phải phình. Luật báo *"gấp 3 lần mức thường"* **không bắn** ở đây, tức luật đủ tinh để không báo động giả.
3. **`Quẹt thẻ` bằng 0 cả 6 tháng** trong khi tổng có 10 dòng ⇒ **cả 10 dòng cũ hơn tháng 3**. Nhãn này gần như **không còn dùng** — đáng hỏi kế toán có nên giữ, vì một nhãn chết vẫn là một cửa mở.

---

## §6 · ⭐⭐ Phát hiện nặng: chuỗi 12 dòng đúng bằng nhau

Trong nhóm `CHƯA BIẾT`, mười hai dòng lớn nhất *(sau hai dòng đầu)* là:

| Số tiền | Tài khoản nguồn | Diễn giải |
|--:|---|---|
| `490.000.000` × **12 dòng** | `R \| 03088010516666_MSB VND_CN` | `03088010516666-…-CK 24/7 cho 01100018000784- Lần 1 … Lần 12` |

**Tổng ≈ 5,88 tỷ, tới cùng một tài khoản đích `01100018000784`, đánh số Lần 1…12, không dòng nào có lệnh chi.**

Đây gần như chắc chắn là **cùng một việc** với câu phỏng vấn số 3 đang treo trong `UC-US` §8 — *"chuỗi 13 lần chuyển, tổng đúng 6 tỷ, tới cùng một tài khoản, không lần nào có lệnh chi"*. Bản này **tìm lại được nó một cách độc lập**, và bổ sung ba thứ mà câu hỏi cũ chưa có: **số tài khoản đích**, **cách đánh số `Lần n`**, và **tài khoản nguồn**.

> ⛔ **Không kết luận gì về bản chất khoản này.** Chia nhỏ có thể chỉ vì **hạn mức một lần chuyển** — hoàn toàn bình thường. Điều đo được và đáng nói chỉ có một: **quy trình phải giải thích được chuyện này, và hiện không có gì giải thích.** Đúng luật `R-A4`: nêu ra, không tự chọn bên.

---

## §7 · `US-KT-037` — hai luật cho cùng một việc

| Luật | Dòng vá được | Tiền |
|---|--:|--:|
| Tài liệu *(22/08)* | **70** | gồm một dòng 1,89 tỷ |
| Của tôi: mẫu `PM` + ≥4 chữ số | **158** | **19,57 tỷ** |

Cả hai đều tìm được **dòng `TERASOFTS TT CP server T06.2026 - PM02279-1`, 1.894.982.832 đ**. Nhưng luật của tôi rộng hơn gấp đôi.

⇒ Việc phải làm: **chốt một luật**. Nếu 158 đúng thì đây là **19,57 tỷ máy tự ghép được, không cần ai gõ** — thuộc loại việc rẻ nhất trong toàn bộ dự án.

---

## §8 · ⭐ Sửa một ghi chép sai của dự án: file GỐC `ADJUSTED` đọc được

| Ghi chép cũ | Đo 24/08 |
|---|---|
| `ITL ADJUSTED` **gốc** đã 404 / mất quyền; `GAP-ITL-36` đóng theo hướng *"bản copy không giải được"*; `GAP-ITL-39` xin quyền | **`ok = True`** — đọc được metadata: sheet `ITL Ledge` **10.581 × 69**, `[RAW ITL]Data Management` 37.827 × 29, `[Importrange]Mapping Master` 4.964 × 26 |

**Vì sao trước đó tưởng mất:** file này **đọc được không đều** — chính `read_cells_sa.py` đã ghi lại: *"đọc file GỐC ADJUSTED thành công 1 lần, hai lần sau timeout"*. Lần đo 24/08 gặp `HTTP 503` ở lần đọc ô đầu tiên, rồi metadata lại ra bình thường. ⇒ **Không phải mất quyền, là bảng nặng.** Đúng với phép đo 33,2 giây cho 3 ô.

**Hệ quả:**

| Việc | Trạng thái mới |
|---|---|
| `GAP-ITL-39` *(xin quyền file gốc)* | **Có thể đóng** — quyền đã có. Việc còn lại là **kỹ thuật đọc**, không phải quyền |
| `AUD-5` | **Vẫn đúng** nhưng phải bổ sung: *"bản copy trả `#REF!`"* chỉ là **một** trong hai lý do; lý do kia là **timeout của bảng nặng**, và nó **giả dạng thành mất quyền** |
| `việc 7` — cổng `Final` | **Đo được**, đang chạy: đọc 14 cột `Classifying`/`Final` của 7 khối, từng khối một, có thử lại |

---

## §9 · Việc mở

| ID | Việc | Vì sao |
|---|---|---|
| `GAP-ITL-56` ⭐⭐ | **Kế toán chốt luật 6 nhãn.** Con số `3.480 / 92%` **không tái lập được** vì luật không được ghi lại. Kết luận về *tiền* vẫn đứng; kết luận về *số dòng hàng chờ* thì không | §4 |
| `GAP-ITL-57` ⭐ | **Chốt luật đọc mã lệnh trong diễn giải**: 70 dòng hay 158 dòng? Nếu 158 thì **19,57 tỷ ghép được miễn phí** | §7 |
| `GAP-ITL-58` | **Chuỗi 12 × 490 triệu tới TK `01100018000784`** — hỏi kế toán quy trình nào cho phép, và vì sao không lần nào có lệnh chi. **Không phán trước** | §6 |
| `GAP-ITL-59` | **Nhãn `Quẹt thẻ` có thể đã chết** — 0 dòng trong 6 tháng. Một nhãn chết vẫn là một cửa mở | §5 |
| `AUD-11` | **Bổ sung `AUD-5`:** một bảng nặng timeout **giả dạng thành mất quyền**. Trước khi ghi *"mất quyền"* phải thử lại ≥3 lần và probe metadata riêng | §8 |
| ~~`GAP-ITL-39`~~ | ~~Xin quyền chỉ-xem file GỐC ADJUSTED~~ | **ĐÓNG** — quyền đã có, xem §8 |

---

---

## §10 · Việc 7 — cổng hậu kiểm `Final`, đo được trên FILE GỐC

**Cách đo:** mỗi trường có 4 cột theo khuôn `Classifying → Manual input → MID → Final`.
Vùng AUDIT của sổ **so cột `Classifying`**. Engine P&L **đọc cột `Final`**. Vậy chỉ cần so hai cột đó.

Đọc từng khối một, có thử lại 3 lần. **Đọc xong 4 / 7 khối** — 3 khối còn lại `TimeoutError` cả 3 lần; file gốc đọc không đều.

| Trường | Máy trả lời thay người | Khớp | `Final` trống | Cả hai có, **khác nhau** |
|---|--:|--:|--:|--:|
| Budget Code (HDCode) · `S→V` | **6.558 · 66%** | 3.328 | 34 | **13** |
| Chủ dự toán (CDT1) · `AA→AD` | **6.589 · 66%** | 3.337 | 7 | **0** |
| Thời điểm kết thúc DV · `AI→AL` | **7.562 · 76%** | 2.364 | 7 | **0** |
| **File đính kèm: Hoá đơn** · `AQ→AT` | **8.428 · 85%** | 1.424 | 41 | **0** |
| **TỔNG 4/7 khối** | **29.137 · 73,4%** | **10.453** | **89** | **13** |
| 3 khối còn lại *(Payment Type · Bắt đầu DV · Mã đối tác)* | *timeout cả 3 lần thử* | | | |

★★ **`13 / 39.692 = 0,033%`.** Qua **bốn khối độc lập**, tỷ lệ *"cả hai có giá trị mà khác nhau"* gần bằng không. Kết luận không còn là suy đoán từ hai khối.

⚠ **Khối `File đính kèm: Hoá đơn` nặng nhất — 85%.** `Final` = `Nợ hoá đơn` trên **7.189 dòng**, trong khi cả trường này chỉ có **3.489 ô người từng gõ**. Kể cả nếu mọi ô người gõ đều nói *Nợ hoá đơn*, vẫn còn **hơn 3.700 dòng mang nhãn đó mà chưa ai gõ**.

### ★★ Kết quả nói gì

Cột `Classifying` ghi thẳng **`Need to manual input`** trên **6.589 dòng**. Cột `Final` — cái duy nhất đi vào P&L — **vẫn có giá trị cụ thể** trên gần hết số đó:

| Giá trị `Final` tự có | Số dòng |
|---|--:|
| `SHQ2 \| Headquarters2` *(Chủ dự toán)* | **5.545** |
| `OGA \| GAC - Other` *(Budget Code)* | **1.704** |
| `NB \| Lưu chuyển nội bộ` | **1.225** |
| `LC \| License Cost` | 1.566 |

★ **Cột "cả hai có, khác nhau" chỉ có 13 và 0 dòng.** Đây là chi tiết quan trọng nhất, và nó **đổi hướng vấn đề**:

| Giả thuyết | Đo được |
|---|---|
| *"Máy ghi đè công người gõ"* | ❌ **Gần như không xảy ra** — 13 dòng và 0 dòng |
| *"Máy điền vào chỗ không ai điền"* | ✅ **6.558 và 6.589 dòng** |

⇒ `US-KT-025` *(hệ phải KÊU khi người gõ khác nguồn)* vẫn nên làm, nhưng **nó không phải chỗ chảy máu**. Chỗ chảy máu là `US-KT-026`: **để trống là trống**.

### ⚠ Và nó sửa cách đọc con số `6.711`

Vùng AUDIT báo **6.711 dòng `FALSE`**, chia 6 cột `1.356 · 552 · 146 · 2.310 · 2.308 · 39`. Con số này từng được đọc là *"sổ tự biết mình lệch"*.

Đo trên file gốc cho thấy `Classifying` phần lớn **chỉ đang nói "cần người điền"**. ⇒ **6.711 không phải "lệch đối soát" mà là "chưa ai điền"** — và ở đúng những dòng đó, `Final` đã tự có đáp án.

★ Đây là lần thứ **hai** trong dự án một con số bị đọc sai bản chất, sau `Diff After Adjuts` *(tưởng là khoản lệch, thật ra là số dư tiền)*. Cùng một dạng lỗi: **nhãn của cột không nói đúng cột chứa gì.**

---

## Changelog

- **v0.3** (2026-08-24, tối): §10 hoàn tất **4/7 khối**. `Classifying ≠ Final` **29.137 / 39.692 = 73,4%**; khối `Hoá đơn` **85%**. ★★ *"Cả hai có giá trị mà khác nhau"* = **13 / 39.692 = 0,033%** qua bốn khối độc lập ⇒ kết luận **máy điền vào chỗ không ai điền** đã vững, không còn là suy đoán từ hai khối. 3 khối còn lại timeout cả 3 lần thử.
- **v0.2** (2026-08-24): Thêm **§10 — việc 7 đo được trên FILE GỐC**. `Classifying` ≠ `Final` trên **66,0%** *(HDCode)* và **66,3%** *(CDT1)*. ★★ Chỉ **13** và **0** dòng là *cả hai có giá trị mà khác nhau* ⇒ vấn đề **không phải ghi đè công người gõ**, mà là **máy điền vào chỗ không ai điền** *(6.558 và 6.589 dòng)*. ⚠ Sửa cách đọc `6.711`: đó là **"chưa ai điền"**, không phải *"lệch đối soát"* — cùng dạng lỗi với `Diff After Adjuts`. Đã đọc 2/7 khối; 5 khối còn lại chờ file gốc.
- **v0.1** (2026-08-24): Khởi tạo. Đo `việc 2` + `việc 6`. **Hai phép đối chứng đều đạt** *(3.344 khớp tuyệt đối; 89,8% vs 89,3%)*. `AUD-5` đã kiểm: 6.756 ô lỗi **toàn bộ là `#N/A`**, không có `#REF!`. Sáu nhãn: **1.814 dòng · 84,6% tiền**; ⚠ **không tái lập được `3.480 / 92%`** ⇒ `GAP-ITL-56`. Xu hướng tháng: máy bắt được **`Lương & thưởng` phình hơn 3 lần**. ⭐⭐ Tìm lại độc lập **chuỗi 12 × 490 triệu** tới một tài khoản ⇒ `GAP-ITL-58`. ⭐ **File GỐC ADJUSTED đọc được** ⇒ **đóng `GAP-ITL-39`**, mở `AUD-11`. Mở `GAP-ITL-56/57/58/59`.
