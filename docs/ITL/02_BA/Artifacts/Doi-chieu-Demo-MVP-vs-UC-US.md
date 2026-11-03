# Đối chiếu bản demo MVP `Sổ máy ITL` với 22 UC / 45 US

**Version:** v0.3 · **Ngày:** 2026-08-24 *(⛔ header từng đứng ở v0.2 — sửa 27/08)* · **Tầng:** L2 · **Loại:** doc-only (Class A)

> ✅ **ĐÃ SỬA — xem §8 cho kết quả sau bản demo v2.** §1–§7 dưới đây là **biên bản đo của bản v1**, giữ nguyên để so được trước/sau. Số hiện hành **sau khi đo 24/08 chiều**: **✅ 17 · ◐ 6 · ⛔ 16 · ○ 6** — xem §8.7.

**Đối tượng đo:** [`Demo-MVP-So-may-ITL.html`](Demo-MVP-So-may-ITL.html) — 4 tab: `Hàng chờ` · `Cổng hôm nay` · `Xu hướng nhãn` · `Nhật ký`.

**Thước:** [`UC-US-Ke-toan-PM-den-ITL.md`](UC-US-Ke-toan-PM-den-ITL.md) v0.3 — **22 UC · 45 US**. Đếm bằng máy, không bằng mắt (`AUD-9`): 22 dòng UC, trạng thái ● 13 / ◐ 6 / ○ 3 = 22 ✓; 45 mã `US-KT-0xx` phân biệt ✓.

**Nhãn phủ:**

| Nhãn | Nghĩa |
|:--:|---|
| ✅ | **Đủ** — demo có màn, và nội dung khớp `AC` chính |
| ◐ | **Có mặt nhưng thiếu** — đúng chỗ để hiện, nhưng thiếu nội dung `AC` đòi |
| ⛔ | **Không có màn nào** trong demo |
| ○ | **Không cần màn mới** — luật máy chạy nền, hoặc ô người gõ ở lại Google Sheets (`T4`) |

---

## §1 · Trả lời gọn

> ### ⛔ CHƯA ĐỦ. Và khoảng cách lớn hơn cảm giác khi xem demo.

| Câu hỏi | Trả lời |
|---|---|
| 45 US phủ được bao nhiêu? | **✅ 4** · ◐ 9 · ⛔ 26 · ○ 6 |
| Trong 39 US **cần màn**, phủ đủ bao nhiêu? | **4 / 39 = 10,3%** |
| 22 UC phủ được bao nhiêu? | **✅ 2** *(`UC-KT-06`, `UC-KT-07`)* · ◐ 6 · ⛔ 13 · ○ 1 |
| 5 UC gắn ★ *(chỗ tiền và niềm tin đi qua)* | **✅ 1 / 5** — chỉ `UC-KT-07`. Còn `10`·`12`·`17` mới ở mức ◐, `19` **trắng** |
| Demo phủ mấy giai đoạn trong 5? | **①: 0/4 UC** · **②: 2/5** · **③: 0/4** · **④: 0/2** · **⑤: 0/7** |
| Vậy demo có vô dụng? | **Không.** Nó phủ đúng **1 trong 4 trụ** của thiết kế v0.2, và là trụ khó thuyết phục nhất — xem §2 |

⚠ **Cách đọc con số 10,3%:** demo được dựng để **chốt hình dạng**, không dựng để phủ backlog — tôi đã nói vậy khi giao. Nhưng câu anh hỏi là *"đã đủ chưa"*, và câu trả lời trung thực theo thước UC/US là **chưa, còn xa**. Không diễn giải lại câu hỏi cho dễ trả lời.

---

## §2 · Cách đo có ý nghĩa hơn: bốn trụ của thiết kế v0.2

`UC-US` §6 chốt: hệ này **không kiểm soát được bằng người** ⇒ kiểm soát là **4 việc máy làm mà không cần ai bấm**. Đo demo theo bốn trụ đó:

| # | Trụ | US gốc | Demo | Thiếu gì |
|--:|---|---|:--:|---|
| 1 | **Không bao giờ tự bịa** — không biết thì nói không biết | `US-KT-026` | ◐ | Có `6.843 → 0` ở tab 3. **Thiếu 4 nhóm mặc định** *(1.210 `Headquarters2` · 1.624 `VD0` · 3.489 `Nợ hoá đơn` · 297 `GAC - Other`)*, và thiếu chính trạng thái `UNMAPPED` trên một dòng cụ thể |
| 2 | **Dán nhãn loại** cho phần không cần lệnh chi | `US-KT-036` | ◐ | Phễu chỉ có **tổng 3.480**. **Thiếu 6 loại** *(lãi & phí bank · điều chuyển nội bộ & đổi tệ · lương-thưởng · thuế · doanh thu nền tảng · quẹt thẻ)* — mà chính 6 nhãn ấy là thứ giữ hàng chờ khỏi 70% rác |
| 3 | **Xếp việc theo tiền + in tuổi việc** | `US-KT-039` `US-KT-028` | **✅** | Phủ đủ: một hàng chờ chung, đảo xếp tiền ↔ tuổi việc, thanh tuổi đổi đỏ quá 3 ngày, không có nút xoá trắng. *(một sai lệch nhỏ — xem §5.2)* |
| 4 | **Ghi nhật ký mọi lần gõ và sửa** | `US-KT-030` | ◐ | Tab 4 đúng chỗ, nhưng chỉ **3 trường** *(thời điểm · ai · việc)*. `AUD-1` đòi **7 trường**, và thiếu `trước → sau` |

★ **Kết luận đúng của bản demo: nó chứng minh được trụ 3, và mới gợi hình trụ 1-2-4.** Trụ 3 là trụ khó tin nhất khi nói bằng lời (*"9.892 dòng còn ~50"*), nên demo đã làm đúng việc đáng làm trước. Nhưng ba trụ còn lại **chưa được chứng minh bằng màn hình nào**.

---

## §3 · Đối chiếu 22 UC

| UC | Tên rút gọn | GĐ | ★ | Phủ | Ở tab nào / thiếu gì |
|---|---|:--:|:--:|:--:|---|
| `UC-KT-01` | Nạp sao kê theo TK theo ngày | ① | | ⛔ | không có màn *"danh sách nguồn chậm"*; 2 nguồn trễ **407** và **264 ngày** không hiện ở đâu |
| `UC-KT-02` | Nhập thu chi quỹ và ví | ① | | ○ | ô người gõ, ở lại Sheets — tab 3 đã ghi nhận đúng là loại `1 · hằng` |
| `UC-KT-03` | Danh mục TK & quỹ kèm dải đọc | ① | | ⛔ | không có màn danh mục |
| `UC-KT-04` | 5 loại giao dịch hay bị bỏ sót | ① | | ⛔ | không phải một trong 4 cổng của demo |
| `UC-KT-05` | Chạy tổng hợp thành `111`/`112` | ② | | ⛔ | không có phép kiểm số dòng ra = vào |
| `UC-KT-06` | **Nhập số dư thật từng ngày** | ② | | **✅** | **lưới độ phủ ví × ngày**, tab 2 — đúng `AC` của `US-KT-007` |
| `UC-KT-07` | **Đọc cổng `DIF`/`EBTS`** | ② | ★ | **✅** | 4 thẻ cổng, tab 2 — kèm cả chỗ *"chưa kết luận được"* |
| `UC-KT-08` | Bút `Adjust` giải trình lệch | ② | | ⛔ | demo **không có màn nhập nào** ⇒ không thể demo *"bắt buộc có lý do"* |
| `UC-KT-09` | Kiểm kê & ký xác nhận quỹ | ② | | ⛔ | — |
| `UC-KT-10` | **Gõ `Reference number`** vào PM | ③ | ★ | ◐ | hàng chờ là đúng chỗ, nhưng **không có nhãn "thiếu mã lệnh"**; 509/3.674 dòng (13,9%) không hiện |
| `UC-KT-11` | 1 khoá = 1 mã, chặn mã trùng | ③ | | ⛔ | 75 mã trùng ⇒ 289 dòng bị bỏ im lặng — không hiện ở đâu |
| `UC-KT-12` | **Giải trình tiền RA không có lệnh** | ③ | ★ | ◐ | phễu có tổng 3.480; **thiếu 3 trạng thái trên từng dòng** và **6 nhãn loại** |
| `UC-KT-13` | `Mapping Master` | ③ | | ⛔ | — |
| `UC-KT-14` | Sổ đăng ký `Index` | ④ | | ◐ | nhật ký là đúng chỗ ghi *"đổi nguồn"*, nhưng demo **không có dòng nào** loại đó, và thiếu `trước → sau` |
| `UC-KT-15` | Refresh & soát `Export Log` | ④ | | ⛔ | không có cảnh báo *"lần này ra ít dòng hơn lần trước"* |
| `UC-KT-16` | Điền `HD code` còn thiếu | ⑤ | | ⛔ | không có nhãn `THIẾU HD CODE` trong hàng chờ |
| `UC-KT-17` | **7 trường vùng ADJUSTMENT** | ⑤ | ★ | ◐ | hàng chờ + `6.843 → 0` có; **thiếu `UNMAPPED` tường minh** và thiếu cơ chế *"hệ phải KÊU khi gõ khác nguồn"* |
| `UC-KT-18` | Đối chiếu ngược `ITL Ledge` ↔ `GL` | ⑤ | | ◐ | *"một hàng chờ chung"* đã phủ; **cổng so cột `Final` thì không** |
| `UC-KT-19` | **Hậu kiểm giá trị `Final`** | ⑤ | ★ | ⛔ | **lỗ hổng kiểm soát lớn nhất của luồng, demo trắng hoàn toàn** |
| `UC-KT-20` | Bảng `Tài khoản → Pháp nhân` | ⑤ | | ⛔ | nhãn `THIẾU PHÁP NHÂN` trong demo là **việc khác** — xem §5.3 |
| `UC-KT-21` | Xoá giao dịch + nhật ký xoá | ⑤ | | ◐ | nhật ký có chỗ; **luồng xoá và trường lý do thì không** |
| `UC-KT-22` | Chốt kỳ và ký | ⑤ | | ⛔ | không có nhãn `chưa đối soát`/`đã đối soát`, không có cut-off |

**Đếm:** ✅ **2** · ◐ **6** · ⛔ **13** · ○ **1** = 22 ✓

---

## §4 · Đối chiếu 45 US

### 4.1 · Giai đoạn ① `P100` — 0/5

| US | Phủ | Ghi chú |
|---|:--:|---|
| `US-KT-001` | ⛔ | thiếu **danh sách tài khoản chậm > 2 ngày** |
| `US-KT-002` | ○ | luật chặn khi nạp sai cột ngày — không phải màn |
| `US-KT-003` | ○ | ô người gõ, ở lại Sheets |
| `US-KT-004` | ⛔ | thiếu chỗ hiện *"script báo lỗi, không im lặng bỏ tài khoản"* |
| `US-KT-005` | ⛔ | thiếu phép kiểm 5 loại giao dịch bỏ sót |

### 4.2 · Giai đoạn ② `ĐỐI SOÁT` — 2/10

| US | Phủ | Ghi chú |
|---|:--:|---|
| `US-KT-006` | ⛔ | thiếu phép kiểm *"số dòng ra = số dòng vào − dòng không ngày"* |
| `US-KT-007` | **✅** | **lưới độ phủ** — đúng `AC`: thiếu ô thì hiện *"chưa đủ số dư"*, không im lặng kéo ngang |
| `US-KT-008` | ◐ | có tổng `−9,53 tỷ` + *"từ 20/08"*; **thiếu bóc theo ngày · pháp nhân · tài khoản · số lệch** |
| `US-KT-009` | **✅** | cảnh báo, vào hàng chờ, **không chặn** — đúng `QĐ-ITL-26`; có cả tuổi việc 4 ngày |
| `US-KT-010` | ⛔ | thiếu phép kiểm *"hai phía `DIF` cộng cùng tập loại tiền"* |
| `US-KT-011` | ⛔ | **demo không có màn nhập nào** ⇒ không demo được *"`Adjust` bắt buộc lý do + người + thời điểm"* |
| `US-KT-012` | ⛔ | biên bản kiểm kê quỹ |

### 4.3 · Giai đoạn ③ `PM & Mapping` — 0/7

| US | Phủ | Ghi chú |
|---|:--:|---|
| `US-KT-013` | ○ | ô người gõ trên PM |
| `US-KT-014` | ⛔ | thiếu **danh sách dòng thiếu mã theo tài khoản, theo ngày** |
| `US-KT-015` | ○ | chặn tại chỗ khi gõ mã trùng — luật, không phải màn. **Nhưng số 75 mã trùng nên hiện** ⇒ xem §5.4 |
| `US-KT-016` | ◐ | có nhãn `CHƯA GHÉP ĐƯỢC LỆNH`, **nhưng con số trong demo sai lệch nặng** — §5.1 |
| `US-KT-017` | ◐ | **thiếu 3 trạng thái trên từng dòng**; phễu chỉ nói tổng |
| `US-KT-018` | ⛔ | thiếu báo *"tài khoản mới chưa khai `Mapping Master`"* |
| `US-KT-019` | ⛔ | phép kiểm `AK` *(pháp nhân theo TK = pháp nhân trả tiền)* không có ở đâu |

### 4.4 · Giai đoạn ④ `ITL Raw` — 0/4

| US | Phủ | Ghi chú |
|---|:--:|---|
| `US-KT-020` | ◐ | nhật ký đúng chỗ; thiếu dòng *"đổi nguồn"* và thiếu `trước → sau` |
| `US-KT-021` | ⛔ | thiếu trạng thái *đang dùng / đang làm / đã bỏ* của 18 dòng `Index` |
| `US-KT-022` | ⛔ | thiếu cảnh báo refresh ra ít dòng hơn |
| `US-KT-023` | ○ | `itl_id` đóng băng — luật nền, không phải màn |

### 4.5 · Giai đoạn ⑤ `ITL Adjust` — 1/16

| US | Phủ | Ghi chú |
|---|:--:|---|
| `US-KT-024` | ⛔ | thiếu nhãn `THIẾU HD CODE` |
| `US-KT-025` | ⛔ | **thiếu toàn bộ cơ chế "hệ phải KÊU khi gõ khác nguồn"** + thiếu thước *"số lần nguồn ≠ người gõ"* |
| `US-KT-026` | ◐ | `6.843 → 0` có; thiếu `UNMAPPED` trên dòng và 4 nhóm mặc định |
| `US-KT-027` | ⛔ | thiếu bộ đếm tồn cùng một dải mở đuôi |
| `US-KT-028` | **✅** | **một hàng chờ chung, xếp theo tiền, in rõ tuổi việc** — phủ đủ |
| `US-KT-029` | ⛔ | ★ **cổng so cột `Final`** — không có trong 4 cổng của demo |
| `US-KT-030` | ◐ | nhật ký 3 trường, `AUD-1` đòi 7 |
| `US-KT-031` | ⛔ | màn danh mục có chủ |
| `US-KT-032` | ⛔ | phép kiểm `P = BL` |
| `US-KT-033` | ⛔ | luồng xoá kèm người + lý do |
| `US-KT-034` | ⛔ | **không có nhãn `chưa đối soát` / `đã đối soát`** |
| `US-KT-035` | ⛔ | không có cut-off; `$B$3` rỗng không hiện ở đâu |

### 4.6 · Story máy của v0.2 — 2/10

| US | Phủ | Ghi chú |
|---|:--:|---|
| `US-KT-036` | ◐ | thiếu **6 nhãn loại** — trụ 2, xem §2 |
| `US-KT-037` | ⛔ | **70 dòng máy vá được từ mã trong diễn giải, gồm một dòng 1,89 tỷ** — không hiện ở đâu. Đây là bằng chứng *"máy làm được việc người đang làm tay"* mạnh nhất đang có, và demo bỏ mất |
| `US-KT-038` | ◐ | lưới độ phủ **đúng hình dạng** cho việc này, nhưng đang đo ví — thiếu **6.450 cặp (ngày × TK) = 15% không kiểm được** và khoản **4,09 tỷ** nằm trong khe |
| `US-KT-039` | ◐ | phủ gần đủ; **thiếu đúng một thứ `AC` đòi: cột lý do để gõ** — §5.2 |
| `US-KT-040` | ⛔ | hoãn có hạn, lần thứ 3 đổi màu |
| `US-KT-041` | ⛔ | ⚠ **tab tên `Xu hướng nhãn` nhưng không chứa `US-KT-041`** — §5.5 |
| `US-KT-042` | **✅** | máy **chỉ đọc**, kết quả về Sheet riêng — ghi ở đầu trang và chân trang |
| `US-KT-043` | ⛔ | **một trang mỗi tuần cho CFO·COO** — cả một vai đọc không có màn nào |
| `US-KT-044` | ○ | không gõ lại lần hai — nguyên tắc chạy song song |
| `US-KT-045` | ⛔ | **đo xem có ai đọc bảng việc không** — phép kiểm của chính hệ kiểm soát |

**Đếm toàn bộ:** ✅ **4** · ◐ **9** · ⛔ **26** · ○ **6** = 45 ✓

---

## §5 · Sáu lỗi của chính bản demo — tìm ra khi đối chiếu

### 5.1 · Một số `mẫu` đang **nói ngược** một số `đo` ⚠ nặng nhất

Nhãn `CHƯA GHÉP ĐƯỢC LỆNH` trong demo ghi **12 dòng** *(dấu `mẫu`)*. Nhưng số **đã đo**: phần `chưa biết` là **1.478 dòng**, trong đó 70 dòng máy tự vá.

⇒ Một ô `mẫu` **thấp hơn sự thật hơn 100 lần**, ngay cạnh những ô `đo`. Luật hai dấu tôi tự đặt vẫn giữ, nhưng **chưa đủ**: dấu `mẫu` chỉ nói *"không phải số thật"*, nó không ngăn con số đó **mâu thuẫn với một phép đo đã có**.

★ **Luật bổ sung:** nếu một chỉ tiêu **đã có số đo** thì ô `mẫu` **không được phép tồn tại** ở chỉ tiêu đó — phải dùng số đo. `mẫu` chỉ dành cho chỉ tiêu **chưa đo lần nào**.

### 5.2 · Thiếu đúng thứ `US-KT-039` đòi: **cột lý do**

`AC`: *"có **một cột duy nhất để tôi gõ: lý do**"*. Demo có **nút `đã xử lý`** thay cho cột đó.

Khác biệt không nhỏ: nút chỉ ghi *"đã xong"*; cột lý do ghi *"vì sao"*. Và `US-KT-045` **đo chính cột lý do đó** để biết cổng còn sống hay đã chết. ⇒ Bỏ cột lý do là **bỏ luôn thước đo duy nhất của hệ kiểm soát**.

### 5.3 · Nhãn `THIẾU PHÁP NHÂN` không phải `UC-KT-20`

Demo hiện **211 dòng pháp nhân trống** (`GAP-ITL-47`). Còn `UC-KT-20` / `US-KT-032` là việc khác: **hai cột pháp nhân `P` và `BL` lệch nhau** trong khi engine chỉ đọc `BL` ⇒ sai pháp nhân trong P&L mà không ai thấy. Trống và lệch là **hai lỗi khác nhau**, demo mới phủ cái nhẹ hơn.

### 5.4 · Demo **không có màn nhập nào**

Chỉ có một nút. Kéo theo **6 US không thể demo**: `011` *(lý do cho `Adjust`)* · `024` *(điền `HD code`)* · `025` *(hệ KÊU + hai nút)* · `033` *(lý do xoá)* · `039` *(cột lý do)* · `040` *(hoãn có hạn)*.

### 5.5 · Tab `Xu hướng nhãn` không chứa xu hướng nhãn

Tên tab lấy từ `US-KT-041`, nhưng nội dung là: giá tính lại · 4 loại ô · `6.843 → 0`. Ba thứ đó thuộc **phương pháp luận code hoá**, không phải một US của kế toán. ⇒ **Tab đặt tên hứa một việc rồi giao việc khác** — đúng loại lỗi mà chính dự án này đang đi vá *(cột `Diff After Adjuts` không phải chênh lệch; cổng ví không đo tiền ví)*. Sửa: đổi tên tab thành `Phương pháp` và mở tab `Xu hướng nhãn` thật.

### 5.6 · Vai `RD-1` CFO·COO trắng hoàn toàn

`US-KT-034` + `US-KT-043` — *"một trang mỗi tuần, đúng ba việc, không đòi hành động"*. Đây là **vai đọc duy nhất còn sống** sau khi v0.2 khai tử 3 vai. Demo không có gì cho vai này.

---

## §6 · Việc mở ra từ bản đối chiếu này

| ID | Việc | Vì sao |
|---|---|---|
| `GAP-ITL-53` ⭐ | **ITL chưa có `SCREEN_SPEC` riêng.** `06_SCREEN_SPEC.md` và `04_Test/03_TRACEABILITY_GAP_REPORT.md` đều còn banner *"bản copy chương trình — chưa dẫn xuất cho ITL"* ⇒ **bản demo đang là spec màn hình đầu tiên trên thực tế**, mà nó chưa được nâng thành spec. Không có hợp đồng màn hình thì code ra không có gì nghiệm thu | §1 |
| `GAP-ITL-54` | **Luật hai dấu chưa đủ** — ô `mẫu` được phép mâu thuẫn với ô `đo`. Chốt luật §5.1 vào mọi bản demo sau | §5.1 |
| `AUD-10` | `UC-US` §4 ghi *"**6** UC gắn ★"* nhưng đếm bằng máy trong bảng chỉ có **5** dấu ★ *(`07`·`10`·`12`·`17`·`19`)*. **Nêu ra, không tự chọn bên** (`R-A4`) — hoặc con chữ sai, hoặc một UC bị mất dấu ★ | đo 2026-08-24 |
| `GAP-ITL-55` | **`US-KT-045` chưa có chỗ đứng.** Nó đo *"có ai đọc bảng việc không"* — nhưng nó đo **cột lý do**, mà demo đã bỏ cột đó. Phải khôi phục cột lý do trước, rồi mới đo được | §5.2 |

---

## §7 · Nghĩa gì và làm gì tiếp

**Nghĩa:** demo **chưa đủ**, nhưng nó **không sai hướng** — nó phủ đúng trụ khó thuyết phục nhất *(xếp việc theo tiền, 9.892 còn ~50)*. Cái nó chưa làm là **chứng minh ba trụ còn lại bằng màn hình**, và **cả giai đoạn ⑤ — nơi công người dồn về** *(7 UC · 16 US · 1 US phủ đủ)*.

**Thứ tự sửa demo — theo trụ, không theo số lượng US:**

| # | Việc | Đóng được |
|--:|---|---|
| 1 | **Khôi phục cột lý do** trong hàng chờ *(bỏ nút `đã xử lý`)* | `US-KT-039` đủ · mở đường cho `045` |
| 2 | **Dán 6 nhãn loại** vào phễu và vào hàng chờ | trụ 2 · `US-KT-036` · `UC-KT-12` |
| 3 | **Trạng thái `UNMAPPED` trên dòng** + 4 nhóm mặc định | trụ 1 · `US-KT-026` · `UC-KT-17` |
| 4 | **Nhật ký 7 trường** + dòng `trước → sau` | trụ 4 · `US-KT-030` · `US-KT-020` |
| 5 | **Tab thứ 5: một trang cho CFO·COO**, đúng ba việc | `US-KT-034` · `US-KT-043` · vai `RD-1` |
| 6 | **Đổi tên tab 3** và mở `Xu hướng nhãn` thật | `US-KT-041` · sửa §5.5 |
| 7 | **Thêm cổng so cột `Final`** | `US-KT-029` · `UC-KT-19` — lỗ hổng lớn nhất |

Làm hết 7 việc: **✅ đi từ 4 lên ~13 US**, ★ đi từ 1/5 lên 4/5, và **cả bốn trụ có màn hình chứng minh**. Vẫn chưa phủ 45 — vì 26 US ⛔ phần lớn thuộc giai đoạn ①③④, cần adapter đọc dữ liệu thật, không phải cần thêm màn.

---


---

## §8 · Sau bản demo v2 — đo lại toàn bộ 45 US

**Đối tượng:** [`Demo-MVP-So-may-ITL.html`](Demo-MVP-So-may-ITL.html) bản **v2**, 6 tab: `Hàng chờ` · `Cổng hôm nay` · `Xu hướng nhãn` · `Máy tự điền` · `Một trang tuần` · `Nhật ký`.

### 8.1 · Kết quả

| | ✅ đủ | ◐ thiếu | ⛔ trắng | ○ không cần màn |
|---|--:|--:|--:|--:|
| **45 US · bản v1** | 4 | 9 | 26 | 6 |
| **45 US · bản v2** | **14** | 9 | **16** | 6 |
| **22 UC · bản v1** | 2 | 6 | 13 | 1 |
| **22 UC · bản v2** | **3** | **10** | **8** | 1 |

**Trong 39 US cần màn:** phủ đủ **14/39 = 35,9%** *(v1: 10,3%)*. **Không còn US nào ở ⛔ mà thuộc bốn trụ.**

### 8.2 · ⚠ Tôi dự đoán sai một chỗ

Khi đề xuất 7 việc, tôi viết *"★ đi từ 1/5 lên **4/5**"*. **Đo lại: chỉ 2/5.**

| UC ★ | v1 | v2 | Vì sao chưa đủ |
|---|:--:|:--:|---|
| `UC-KT-07` cổng `DIF` | ✅ | ✅ | |
| `UC-KT-10` gõ `Reference number` | ◐ | ◐ | có nhãn `THIẾU MÃ LỆNH` 509/3.674 <span>đo</span>, nhưng **chưa bóc theo tài khoản và theo ngày** |
| `UC-KT-12` tiền RA không lệnh | ◐ | ◐ | 3 trạng thái + 70 dòng máy vá đã có; **6 nhãn loại vẫn chưa tách được số** |
| `UC-KT-17` 7 trường ADJUSTMENT | ◐ | ◐ | `UNMAPPED` + bảng 7 trường đã có; **thiếu "hệ phải KÊU khi gõ khác nguồn"** (`US-KT-025`) |
| `UC-KT-19` hậu kiểm `Final` | ⛔ | **✅** | nhật ký 7 trường + thước *"có ai đọc bảng việc không"* — cả hai `US` của UC này đều đủ |

★ **Điều đúng hơn con số:** cả 5 UC ★ **không còn cái nào trắng**. Nhưng *"4/5"* là tôi đếm lạc quan trước khi đo — đúng loại lỗi mà `AUD-9` đã dạy một lần.

### 8.3 · Mười US đi từ ⛔ hoặc ◐ lên ✅

| US | v1 | v2 | Cái được thêm |
|---|:--:|:--:|---|
| `US-KT-016` | ◐ | ✅ | **thay số `mẫu` 12 dòng bằng số đo 1.478 dòng** — sửa lỗi nặng nhất của v1 |
| `US-KT-017` | ◐ | ✅ | cột **Trạng thái**: `CÓ LỆNH` · `KHÔNG CẦN LỆNH` · `CHƯA BIẾT` · `UNMAPPED`; phễu hiện đủ 4 nhóm đã đo *(3.344 · 3.480 · 1.590 · 1.478)* |
| `US-KT-020` | ◐ | ✅ | nhật ký có dòng **đổi nguồn `Index!E12`** kèm `trước → sau` và người |
| `US-KT-026` | ◐ | ✅ | `UNMAPPED` tường minh trong hàng chờ + **bảng 7 trường** kèm giá trị máy tự gán |
| `US-KT-030` | ◐ | ✅ | **nhật ký 7 trường** đúng `AUD-1` |
| `US-KT-034` | ⛔ | ✅ | nhãn `chưa đối soát` / `đã đối soát`, **số chưa đối soát in nghiêng gạch chấm** — nhìn khác thật |
| `US-KT-037` | ⛔ | ✅ | **70 dòng máy vá được**, gồm dòng **1,89 tỷ** `TERASOFTS … PM02279-1` |
| `US-KT-039` | ◐ | ✅ | **khôi phục cột lý do**, bỏ nút `đã xử lý` |
| `US-KT-043` | ⛔ | ✅ | **một trang tuần**, đúng ba việc, có câu *"trang này không đòi anh làm gì"* |
| `US-KT-045` | ⛔ | ✅ | bộ đếm **"cột lý do đã được gõ: N lần"** + luật *4 tuần không ai gõ = cổng đã chết* |

Và **6 US đi từ ⛔ lên ◐**: `014` *(nhãn thiếu mã lệnh)* · `024` *(nhãn thiếu `HD code`)* · `029` *(cổng `Final`)* · `032` *(lệch pháp nhân `P ≠ BL`)* · `033` *(nhật ký có trường lý do)* · `041` *(tab xu hướng nhãn thật)*.

### 8.4 · Sáu lỗi của bản v1 — trạng thái

| # | Lỗi | Đã sửa? |
|--:|---|:--:|
| 5.1 | ô `mẫu` nói ngược ô `đo` *(12 vs 1.478)* | ✅ dùng số đo; và **ghi luật vào đầu trang**: chỉ tiêu đã có số đo thì **không được có ô `mẫu`** |
| 5.2 | bỏ cột lý do | ✅ khôi phục; kèm bộ đếm cho `US-KT-045` |
| 5.3 | nhãn `THIẾU PHÁP NHÂN` không phải `UC-KT-20` | ✅ tách thành **hai nhãn**: `THIẾU PHÁP NHÂN` *(211 dòng, đo)* và `LỆCH PHÁP NHÂN · P ≠ BL` *(chưa đo được)* |
| 5.4 | không có màn nhập nào | ◐ đã có **một** ô nhập — cột lý do. Còn thiếu form cho `Adjust` (`011`), `HD code` (`024`), hoãn có hạn (`040`) |
| 5.5 | tab `Xu hướng nhãn` không chứa `US-KT-041` | ✅ tab **đúng nội dung**: 6 nhãn × 6 tháng + luật báo *"cao gấp 3 lần mức thường thì đổi đỏ"*; nội dung phương pháp chuyển thành **phụ lục** của tab `Máy tự điền` |
| 5.6 | vai CFO·COO trắng | ✅ tab **Một trang tuần** |

### 8.5 · ★ Một phép đo tìm ra khi sửa, đáng hơn cả bảng phủ

Tôi định dùng *"4 nhóm mặc định"* của `UC-US` §5.5 — bốn số **1.210 · 1.624 · 3.489 · 297**, cộng ra **6.620**, lệch **223** so với 6.843. Nghi là mâu thuẫn tài liệu.

**Không phải.** [`01_BRD.md`](../01_BRD.md) §2 có bảng đầy đủ: **7 trường**, cộng đúng **6.843** — và 223 chính là ba trường mà `UC-US` không nêu *(179 + 22 + 22)*.

| # | Cột | Trường nhập tay | Số ô | Giá trị máy tự gán | Người giữ |
|--:|---|---|--:|---|---|
| 1 | `S–V` | Budget Code (HDCode) | 297 | `GAC - Other` | LAN + THƯƠNG |
| 2 | `W–Z` | Loại giao dịch (Payment Type) | 179 | *chưa nêu* | THƯƠNG |
| 3 | `AA–AD` | Chủ dự toán (CDT1) | 1.210 | `Headquarters2` | THƯƠNG |
| 4 | `AE–AH` | Thời điểm bắt đầu dùng DV | 22 | *chưa nêu* | THƯƠNG |
| 5 | `AI–AL` | Thời điểm kết thúc dùng DV | 22 | *chưa nêu* | THƯƠNG |
| 6 | `AM–AP` | Mã đối tác (ID Payee) | 1.624 | `VD0` | THƯƠNG |
| 7 | `AQ–AT` | File đính kèm: Hoá đơn | 3.489 | `Nợ hoá đơn` | THƯƠNG |
| | | **Tổng** | **6.843** | 4 trường có mặc định · 3 trường *(223 ô)* chưa nêu | |

★★ **Cột cuối là phát hiện nặng nhất của lần sửa này:** **THƯƠNG giữ 6/7 trường = 6.546 ô = 95,7%.** Rủi ro *"một người rời đi"* của `GAP-ITL-38` **không phải nói chung** — nó **có tên và có con số**. Đã đưa vào demo tab `Máy tự điền`.

⇒ **Không mở `AUD-11`.** Nghi vấn 223 tự đóng khi đọc đúng nguồn — và nó là ví dụ sống cho luật `GAP-ITL-54`: nếu tôi rải 4 số đó lên demo cho đủ bảng, tôi đã dựng một bảng thiếu 223 ô mà trông như đầy.

### 8.6 · Còn 16 US trắng — và vì sao thêm màn không giải được

| Nhóm | US | Cần gì |
|---|---|---|
| **Cần adapter đọc dữ liệu thật** | `001` `004` `005` `006` `010` `018` `021` `022` `027` `035` | 10 US này là **phép kiểm trên dữ liệu**, không phải màn hình. Máy phải đọc được sổ đăng ký `Index`, `Export Log`, `Mapping Master`, cut-off — hiện chưa nối |
| **Cần màn nhập** | `011` `024` `040` | form `Adjust` có lý do · điền `HD code` · hoãn có hạn |
| **Cần quyền file GỐC** | `031` `032`*(◐)* | `GAP-ITL-39` — bản copy trả `#REF!` (`AUD-5`) |
| **Cần thiết kế riêng** | `019` `025` | phép kiểm `AK` · cơ chế *"hệ KÊU khi người gõ khác nguồn"* + thước `nguồn ≠ người gõ` |
| **Ngoài phạm vi màn** | `012` | biên bản kiểm kê quỹ có ký |

★ **Nghĩa:** demo đã gần cạn phần *"thêm màn thì phủ được"*. Từ đây trở đi, **phủ thêm US = nối dữ liệu thật**, đúng như `GAP-ITL-48` đã cảnh báo: phải phân 1.755 cột theo phụ thuộc vượt file **trước** khi code.

### 8.7 · Sau khi ĐO (24/08 chiều) — ba việc còn ◐ đã đóng

Ba việc `2` · `6` · `7` không thể đóng bằng vẽ thêm màn; chúng cần số đo. Đã đo *(xem [`Ket-qua-Do-6-nhan-va-Xu-huong.md`](Ket-qua-Do-6-nhan-va-Xu-huong.md))*:

| US | Trước đo | Sau đo | Số đo được |
|---|:--:|:--:|---|
| `US-KT-036` sáu nhãn | ◐ | **✅** | 6 nhãn có số dòng và số tiền riêng; `1.814` dòng · `84,6%` tiền |
| `US-KT-041` xu hướng nhãn | ◐ | **✅** | 6 nhãn × 6 tháng; máy **bắt được `Lương & thưởng` phình hơn 3 lần** |
| `US-KT-029` cổng `Final` | ◐ | **✅** | `Classifying ≠ Final` trên **66,0%** dòng; **bắt được cả 13 dòng** *"cả hai có giá trị mà khác nhau"* — đúng `AC` |

**Tổng cuối:**

| | ✅ đủ | ◐ thiếu | ⛔ trắng | ○ không cần màn |
|---|--:|--:|--:|--:|
| **45 US** · v1 | 4 | 9 | 26 | 6 |
| **45 US** · v2 | 14 | 9 | 16 | 6 |
| **45 US** · **sau đo** | **17** | **6** | 16 | 6 |
| **22 UC** · **sau đo** | **5** | **8** | 8 | 1 |

Trong 39 US cần màn: **43,6%** *(v1: 10,3%)*. UC gắn ★: **3 / 5** — `UC-KT-12` và `UC-KT-18` cùng lên ✅ nhờ phép đo.

⇒ **16 US ⛔ còn lại không đổi** — và đó là kết luận vững nhất của cả hai lần đếm: phần còn lại **không giải được bằng màn hình hay phép đo lẻ**, phải nối adapter đọc dữ liệu thật.

---

## Changelog

- **v0.3** (2026-08-24, chiều): **§8.7** — ba việc `2`/`6`/`7` đóng bằng **số đo**, không bằng vẽ thêm màn. US **✅ 14 → 17**, ◐ **9 → 6**; UC **✅ 3 → 5**; ★ **2/5 → 3/5**. Trong 39 US cần màn: **43,6%**. **16 US ⛔ không đổi** ⇒ phải nối adapter.
- **v0.2** (2026-08-24): **Đã sửa 7 việc, đo lại toàn bộ.** US **✅ 4 → 14** · ⛔ **26 → 16**; UC **✅ 2 → 3**, ⛔ **13 → 8**. Trong 39 US cần màn: **10,3% → 35,9%**. **10 US lên ✅**, 6 US lên ◐. Cả 5 UC ★ **không còn cái nào trắng** — nhưng ⚠ **tôi dự đoán 4/5, đo ra 2/5**. Sáu lỗi của v1: **sửa xong 5, còn 1 ở ◐** (chưa đủ màn nhập). ★ Tìm ra bảng **7 trường** của `01_BRD.md` §2 cộng đúng **6.843** ⇒ nghi vấn *lệch 223* tự đóng, **không mở `AUD-11`**; và lộ ra **THƯƠNG giữ 6/7 trường = 6.546 ô = 95,7%** — rủi ro *một người rời đi* nay có tên và có số. Còn **16 US trắng**, phần lớn **không giải được bằng thêm màn** mà cần adapter đọc dữ liệu thật.
- **v0.1** (2026-08-24): Khởi tạo. Đối chiếu demo MVP với 22 UC / 45 US. Kết quả **✅ 4 · ◐ 9 · ⛔ 26 · ○ 6**; UC **✅ 2 · ◐ 6 · ⛔ 13 · ○ 1**; ★ **1/5**. Đo bốn trụ v0.2: phủ đủ **1**, gợi hình 3. **Sáu lỗi của chính bản demo** ở §5 — nặng nhất là ô `mẫu` nói ngược ô `đo` (`CHƯA GHÉP ĐƯỢC LỆNH` 12 vs 1.478 đã đo) và **bỏ cột lý do** mà `US-KT-045` cần để đo. Mở `GAP-ITL-53/54/55`, `AUD-10`.
