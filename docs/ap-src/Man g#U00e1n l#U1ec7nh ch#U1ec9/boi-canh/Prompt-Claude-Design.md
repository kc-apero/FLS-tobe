> **Cách dùng:** copy toàn bộ phần trong khung dưới đây (từ `=== BẮT ĐẦU` đến `=== HẾT`) và dán vào một phiên Claude mới.
> Bản dựng thử để đối chiếu: https://claude.ai/artifact/4fx1gRCnLmE4m4Koy89V7P
> Brief đầy đủ: https://claude.ai/artifact/PBXa6wvVxZpaw7MgU6gV9Y

---

=== BẮT ĐẦU PROMPT ===

Bạn là người thiết kế giao diện. Tôi cần bạn thiết kế **bộ component** cho một màn hình nghiệp vụ kế toán đang được xây dựng. Tôi đã có bản dựng thử nhưng **nó chưa đẹp** — bố cục rối, thông tin không có phân cấp, bốn mức độ tin cậy của gợi ý trông na ná nhau. Việc của bạn là thiết kế lại ở **tầng component**, không phải vẽ lại một trang cho đẹp mắt.

Đọc hết bối cảnh dưới đây trước khi vẽ. Đặc biệt là mục **⑦ ĐÃ THỬ VÀ BỊ BÁC** — nó tiết kiệm cho cả hai chúng ta một vòng.

---

## ① MÀN NÀY LÀ GÌ

Mỗi sáng, một kế toán mở màn và trả lời **một câu, lặp lại nhiều lần**:

> **"Lệnh chi này đã đi bằng đồng tiền nào?"**

- Bên trái: **lệnh chi** (phiếu công ty đã duyệt chi, gọi tắt `PM`) — cái công ty *định* chi.
- Bên phải: **giao dịch** (dòng tiền có thật trong sao kê ngân hàng) — cái *đã* chi.
- Việc của họ: **nối đúng một cặp**.

| | |
|---|---|
| Người dùng | **2–3 kế toán**. Không phải quản lý, không phải khách hàng |
| Nhịp làm việc | **hằng ngày, từng giao dịch một** — không phải dọn tồn theo đợt |
| Đang thay thế | Google Sheets họ đã dùng nhiều năm |
| Nghiệm thu | **Không** phải "app chạy được" mà **"họ có dùng không"** |

**Một sự thật phải biết trước khi vẽ: màn này CHƯA AI TỪNG DÙNG.** Đo trên kho dữ liệu thật: số mối nối do **người** tạo = **0**. Toàn bộ 2.219 mối nối hiện có đều do **máy** tạo tự động. Nghĩa là mọi phán đoán về "kế toán sẽ thích gì" — kể cả trong tài liệu này — đều **chưa có bằng chứng sử dụng**. Đừng thiết kế như thể đang tối ưu một thói quen đã có.

---

## ② DỮ LIỆU THẬT — ràng buộc cứng nhất

Đừng thiết kế cho dữ liệu lý tưởng. Số dưới đây đo ngày 18/09/2026 trên kho đang chạy.

### Phía LỆNH CHI — 3.772 dòng

| Trường | Tỷ lệ có |
|---|--:|
| Mã lệnh (dạng `PM02303-1`) · số phiếu · số tiền · đơn vị tiền | 100% |
| Người nhận | 3.771/3.772 |
| Nội dung (người lập tự gõ) | 100% |
| Ngân hàng · pháp nhân | 100% |
| Chủ dự toán (`CDT`) | 3.763 |
| Số chứng từ | **85,8%** — tức 1/7 lệnh **không có** |
| Ngày | nguồn là sê-ri Excel, đã đổi ra ngày thật |

### Phía GIAO DỊCH — 8.387 dòng, và nó **chỉ có bốn điều**

| Trường | Tỷ lệ có |
|---|--:|
| Ngày | 100% |
| Số tiền **＋ chiều** (Nợ = tiền vào · Có = tiền ra) | 100% |
| Số chứng từ | 8.383 |
| Nguồn — **một chuỗi gộp 4 thứ**: `604046904001_OCBC SGD_SGO2` = số tài khoản · ngân hàng · đơn vị tiền · pháp nhân | 100% |
| **Diễn giải sao kê** (dòng chữ ngân hàng ghi) | **99,7%** |

**RỖNG HOÀN TOÀN — đừng vẽ chỗ cho chúng:** tên đối tác · pháp nhân (cột riêng) · số tài khoản (cột riêng) · mọi ô phân loại kế toán. Chúng không tồn tại trong dữ liệu.

### Kích thước nội dung — để chọn cỡ chữ và số dòng

| | ngắn nhất | trung bình | **dài nhất** |
|---|--:|--:|--:|
| Diễn giải giao dịch | 8 | 59 | **189 ký tự** |
| Nội dung lệnh chi | — | — | **77** |
| Tên người nhận | — | — | **35** |

### Khối lượng việc

```
3.772 lệnh chi
  ├─ 2.219 đã gán   (58,8%)   ← nhưng 0 do NGƯỜI gán
  └─ 1.553 chưa gán (41,2%)
       ├─   47  máy đề xuất — khớp CẢ số chứng từ LẪN số tiền ⇒ chỉ cần gật
       ├─  738  cần người chọn
       └─  768  không gán được — sổ không có đồng tiền nào mang số ấy
```

Mỗi lệnh chi có **5–6 giao dịch ứng viên**, xếp theo bậc tin cậy giảm dần:

| Bậc | Nghĩa | Số ứng viên (trên 40 lệnh mẫu) |
|---|---|--:|
| 1 | khớp **số chứng từ** | 16 |
| 2 | **đúng số tiền** | 61 |
| 3 | **gần đúng** số tiền | — |
| 4 | chỉ **cùng đơn vị tiền** | **149** |

**Phần lớn ứng viên là bậc yếu nhất.** Thiết kế phải làm khác biệt giữa bốn bậc **đọc được trong một cái liếc** — không để chúng trông như nhau rồi gắn bốn cái nhãn chữ nhỏ.

Đơn vị tiền lẫn lộn: **USD 21 · VND 12 · SGD 7** trên 40 lệnh mẫu. **Không quy đổi, không cộng gộp hai đơn vị** ở bất kỳ đâu.

---

## ③ BỘ COMPONENT CẦN THIẾT KẾ

| # | Component | Trạng thái bắt buộc phải có |
|:-:|---|---|
| `C1` | **Dòng lệnh chi** trong danh sách trái | chưa gán · máy đề xuất · đã gán · đang chọn · hover · focus bàn phím |
| `C2` | **Thẻ lệnh chi** (đầu panel phải) | ba tầng: định danh → ai & bao nhiêu → bối cảnh |
| `C3` | ⭐ **Dòng giao dịch ứng viên** | chọn/không · **4 bậc** · có/không diễn giải · khớp tiền/lệch tiền |
| `C4` | **Khối "đang gán với"** | chỉ xuất hiện khi lệnh đã gán; chứa `C3` dạng chỉ-đọc ＋ nút bỏ gán |
| `C5` | **Bộ lọc trạng thái** | `Chưa gán` / `Đã gán` / `Tất cả`, mỗi cái mang số đếm |
| `C6` | **Băng số việc** (4 ô đầu màn) | bình thường · nhấn mạnh tốt · nhấn mạnh cảnh báo |
| `C7` | **Dải cảnh báo trong panel** | "danh sách đã cắt bớt" · "không gán được — vì sao" |
| `C8` | **Thanh hành động** | `Gán` / `Đổi sang giao dịch đã chọn` · bật/tắt · câu gợi ý bên cạnh |
| `C9` | **Dải ngày** phân cách trong danh sách | dính đầu khi cuộn |
| `C10` | **Bốn trạng thái khung** | đang tải · rỗng · cửa lỗi · tuổi dữ liệu |

### `C3` là component quan trọng nhất — dành phần lớn công sức ở đây

Nó là nơi **quyết định thực sự xảy ra**. Một dòng ứng viên phải trả lời ba câu, **theo đúng thứ tự này**:

1. **Đây là khoản gì?** → diễn giải sao kê *(bằng chứng chính)*
2. **Bao nhiêu, vào hay ra?** → số tiền ＋ chiều Nợ/Có
3. **Vì sao nó nằm trong danh sách?** → nhãn bậc ＋ độ lệch tiền

Thông tin phụ, không được lấn: ngày · ngân hàng · 4 số cuối tài khoản · pháp nhân · số chứng từ.

---

## ④ LUẬT THIẾT KẾ — KHÔNG được vi phạm

Đây là luật đã ký của dự án, có kiểm tra tự động canh. Không phải sở thích cá nhân.

| Luật | Nghĩa khi vẽ |
|---|---|
| ⭐⭐⭐ **Máy không trả lời thay người** | Máy **đề xuất**, người **quyết**. Nếu hai đáp án cùng đúng, máy **dừng lại và nói ra**, không tự chọn bừa. Giao diện phải phản ánh điều này |
| ⭐⭐ **Ngân sách trường = 9** cho màn làm việc | Thêm một trường ⇒ phải bỏ một trường. Đo được: màn cũ phình từ 339 lên 735 dòng qua 7 lần sửa, **không lần nào giảm** |
| ⭐⭐ **Số của MÁY không lên màn của NGƯỜI** | Cấm hiện: thứ hạng · luỹ kế % · mọi `id` nội bộ · cờ true/false · tên rổ kỹ thuật · dấu thời gian dạng sê-ri. Cách nhận biết: một trường là **của người** nếu người ta **làm khác đi** tuỳ theo giá trị của nó |
| ⭐ **Một sự thật, một chỗ hiện** | Đo được 8/36 trường trên màn cũ là **bản sao nguyên văn** của trường khác |
| **Tiền** | dùng `tabular-nums`, **giữ nguyên đơn vị gốc**, không có dòng "tổng" gộp hai đơn vị |
| **Màn chỉ hiện việc cần làm** | Hàng chờ rỗng = khoẻ mạnh, không phải lỗi. Trạng thái rỗng phải trông như thành tựu, không như hỏng |

### Ba cặp phải phân biệt được bằng **HÌNH**, không bằng chữ nhỏ

1. **"chưa có dữ liệu"** ≠ **"chưa đọc được"** ≠ **"không có"** — ba trạng thái khác nhau. Nhầm lẫn giữa chúng đã cắn dự án này một lần.
2. **"máy đề xuất"** ≠ **"người đã chốt"** — nếu hai thứ trông giống nhau thì luật số 1 ở trên **mất hiệu lực hoàn toàn**.
3. **"danh sách đã cắt bớt"** ≠ **"không có ứng viên nào"** — cắt im lặng khiến người ta kết luận sai.

---

## ⑤ HỆ THỊ GIÁC ĐANG CÓ — dùng lại, đừng vẽ hệ thứ hai

Đây là token đang chạy trong sản phẩm. Có kiểm tra tự động báo lỗi nếu một mã màu xuất hiện ngoài tệp token.

```
chữ       IBM Plex Sans (giao diện) · IBM Plex Mono (số, mã, ngày)

mực       --ink       #14201e    nền thanh trên + chữ chính
          --muted     #5c6b68    chữ phụ
          --faint     #9aa8a5    chữ mờ

bề mặt    --surface   #ffffff    nền thẻ
          --alt       #f6f8f8    nền tiêu đề bảng
          --page      #eef1f1    nền trang
          --line      #dde4e3    mọi đường kẻ

tương tác --accent    #0e7570
          --accent-hi #0a5c58
          --focus-ring #0e757022

ngữ nghĩa — TÁCH HẲN khỏi màu tương tác
          --good #2c7a4b   nền #e8f4ec   viền #bcdcc8
          --warn #c07414   nền #fdf4e7   viền #f0dcbe
          --crit #c73a3a   nền #fbeaea   viền #f3cdcd
          --info #2563eb   nền #e9effd   viền #b9cdf7

mật độ    --row 30px · --grid-fs 12.5px    (màn LÀM, dày hơn màn ĐỌC)
bo góc    4 / 6 / 8 / 999px
panel     sàn 430px · trần 680px — clamp(430px, 34vw, 680px)
```

Phải chạy được **cả nền sáng và nền tối** — trang hiển thị theo cài đặt của người xem.

Nếu bạn cần thêm một token mới (ví dụ để phân biệt 4 bậc ứng viên), **hãy đề xuất nó rõ ràng thành một danh sách riêng** kèm lý do, đừng rải mã màu vào trong component.

---

## ⑥ LUẬT NGHIỆP VỤ — để thiết kế biết mình phục vụ cái gì

Kế toán vừa phát biểu luật ghép (chưa được lập trình, nhưng thiết kế nên chừa chỗ):

| Nhánh | Khoá để ghép | Trạng thái |
|---|---|---|
| **Giao dịch Việt Nam** (có mã PM ngay trong giao dịch) | mã PM ＋ số tiền ＋ pháp nhân | chạy được 82,7% |
| **Giao dịch nước ngoài** | **từ khoá trong diễn giải** ＋ **tên vendor** ＋ số tiền | dữ liệu đã có, phép tìm chưa viết |

**Hệ quả cho thiết kế:** diễn giải sao kê **không phải chữ trang trí**. Với gần **một nửa** số giao dịch (nước ngoài, 4.145/8.387) nó là **bằng chứng duy nhất** để quyết. Tên vendor nằm ngay bên trong nó:

```
Card charge (OPENAI *CHATGPT SUBSCR)
FUNDS TRF - TT 1OR606160155C01 · SENSORTOWER, INC.
PAYMENT/TRANSFER CSDB STRIPE PAYMENTS SIN STRIPE LKuWsFH5A
03088010516666-123728-CK 24/7 cho 19033369015016 - Cp hc ns
```

Đừng cắt nó xuống một dòng mờ ở cuối thẻ. Nhưng nó dài tới **189 ký tự** ⇒ cần một phép **rút gọn có kiểm soát** ＋ một cách xem đầy đủ.

---

## ⑦ ĐÃ THỬ VÀ BỊ BÁC — đọc để khỏi làm lại

| Đã thử | Ai bác | Vì sao |
|---|---|---|
| **Gom 2.219 dòng về 29 nhóm** để giảm số cú bấm | Chủ dự án | "Mapping làm **mỗi ngày, theo từng giao dịch một**". Gom nhóm tối ưu cho **một đợt dọn tồn**, không cho **nhịp hằng ngày**. Tối ưu sai nhịp thì màn đúng số mà **sai việc** |
| Nhãn **"ô chờ gật"** ở băng đầu màn | Chủ dự án hỏi *"là gì?"* | Nó đếm **ô** (2.219 × 2) — **đơn vị của máy**. Người làm đếm theo **việc** |
| Chữ **"máy đã đoán" / "người đã chốt"** | Chủ dự án | Nói về **ai làm**; người dùng cần biết **việc đang ở đâu** ⇒ đổi thành **"đề xuất gán" / "đã gán"** |
| **Bỏ** nút *"xem đủ trường"* | Kế toán | Tôi tưởng nó phục vụ việc ghép; thật ra họ cần nó để **yên tâm về dữ liệu**. Hai nhu cầu khác nhau: xem-đủ là nhu cầu **thưa**, ghép là nhu cầu **mỗi dòng**. Cách đúng: một **đường dẫn sang màn Sổ**, không nhồi thêm trường vào màn này |
| In nguyên chuỗi `604046904001_OCBC SGD_SGO2` | — | Chuỗi kỹ thuật, lại **lặp pháp nhân** đã hiện chỗ khác ⇒ phải tách thành phần, rút số tài khoản còn **4 số cuối** |
| Một màn riêng "soát chi không lệnh" | Chủ dự án | Màn dựng cho một câu hỏi **không ai hỏi** |

---

## ⑧ CÂU HỎI MỞ — tôi muốn bạn trả lời bằng thiết kế

1. Diễn giải dài 189 ký tự: rút gọn còn **mấy dòng**, và xem đầy đủ **bằng cách nào** — mở rộng tại chỗ, tooltip, hay panel phụ?
2. Bốn bậc ứng viên nên phân biệt bằng **màu**, bằng **thứ tự**, hay bằng **nhóm có tiêu đề**? Nhớ rằng **149/226 ứng viên là bậc yếu nhất** — giải pháp nào làm bậc yếu chiếm hết màu sẽ hỏng.
3. Khi lệnh đã gán rồi, mối nối hiện tại nên nằm **trên** danh sách ứng viên hay **trong** danh sách đó (được đánh dấu)? Người dùng có nhu cầu **đổi mapping đã có**.
4. Làm sao để người dùng **không gật theo phản xạ**? 45% số ca **không có** ứng viên nào khớp đúng tiền — màn hình **phải trông khác đi** ở những ca ấy, nếu không kế toán sẽ quen tay bấm Enter.

---

## ⑨ CÁI GÌ LÀ THÀNH CÔNG

Không phải "trông hiện đại". Ba phép đo:

1. ⭐ **Có người thật dùng** — số mối nối do người tạo đi từ `0` lên một số khác `0`.
2. **Mắt tìm được bằng chứng trong một cái liếc** — diễn giải và số tiền là hai thứ quyết định.
3. **Người không gật theo phản xạ** — xem câu hỏi 4 ở trên.

---

## ⑩ TÔI CẦN BẠN GIAO LẠI CÁI GÌ

Một **trang HTML tự chạy được** (một tệp, không phụ thuộc bên ngoài ngoài Google Fonts) đóng vai **bảng component**, gồm:

1. **Bộ token** bạn dùng — kế thừa hệ ở mục ⑤, và liệt kê riêng bất cứ token nào bạn thêm, kèm lý do.
2. **Từng component C1–C10**, hiện **đủ mọi trạng thái đã liệt kê**, đặt cạnh nhau để so sánh được. Dùng dữ liệu mẫu giống thật (mã dạng `PM02303-1`, diễn giải dài thật, ba đơn vị tiền lẫn lộn, có cả ca lệch tiền và ca không có ứng viên).
3. **Một bản ráp thử** của màn hình hoàn chỉnh từ các component đó — danh sách trái ＋ panel phải — để thấy chúng sống với nhau thế nào.
4. **Ghi chú thiết kế ngắn** cho mỗi quyết định khó: bạn chọn gì cho 4 bậc, cho diễn giải dài, cho phân biệt "đề xuất" với "đã gán" — và **vì sao**.

Ưu tiên rõ ràng hơn ấn tượng. Đây là màn một người nhìn **hàng trăm lần mỗi tuần**, không phải trang giới thiệu.

=== HẾT PROMPT ===
