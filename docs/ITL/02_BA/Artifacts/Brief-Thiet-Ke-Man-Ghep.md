# BRIEF THIẾT KẾ — Màn GÁN LỆNH CHI ↔ GIAO DỊCH (FLS)

**Version:** v1.0 · **Ngày:** 2026-09-18 · **Chủ sở hữu:** BA
**Gửi cho:** người thiết kế component
**Vì sao có tệp này:** owner xem bản dựng thử và nói *"chưa đẹp"* ⇒ gói toàn bộ **bối cảnh, ràng buộc và dữ liệu thật** để việc thiết kế bắt đầu từ sự thật, ⛔ không từ mô tả lại.

> ⭐ **Đọc mục `§7` trước khi vẽ.** Ở đó là những thứ **đã thử và bị bác**, kèm lý do. Nó tiết kiệm được một vòng.

---

## §1 · Màn này là gì

Một kế toán mở màn mỗi sáng và trả lời **một câu, lặp lại nhiều lần**:

> **“Lệnh chi này đã đi bằng đồng tiền nào?”**

Bên trái là **lệnh chi** *(phiếu công ty duyệt chi — gọi tắt `PM`)*. Bên phải là **giao dịch** *(dòng tiền có thật trong sao kê ngân hàng)*. Việc của họ là **nối đúng một cặp**.

| | |
|---|---|
| Người dùng | **2–3 kế toán** *(tên thật: LAN, THƯƠNG)*. ⛔ Không phải quản lý, ⛔ không phải khách |
| Nhịp | **hằng ngày**, từng giao dịch một |
| Thay thế | Google Sheets mà họ đã dùng nhiều năm |
| Nghiệm thu | ⛔ **Không** phải *"app chạy được"* mà *"họ có DÙNG không"* |

⛔⛔ **Một sự thật phải biết trước khi vẽ: màn này CHƯA AI TỪNG DÙNG.** Đo trên kho thật: số mối nối do **người** tạo = **`0`**. Toàn bộ `2.219` mối nối hiện có đều do **máy** tạo. ⇒ Mọi phán đoán về *"kế toán sẽ thích gì"* — kể cả của tôi trong tệp này — đều **chưa có bằng chứng**.

---

## §2 · Dữ liệu THẬT — và đây là ràng buộc cứng nhất

⛔ **Đừng thiết kế cho dữ liệu lý tưởng.** Số dưới đây đo ngày `2026-09-18` trên kho đang chạy.

### ⓐ Phía LỆNH CHI — `3.772` dòng

| Trường | Có |
|---|--:|
| Mã lệnh *(`PM02303-1`)* · phiếu · số tiền · đơn vị tiền | **100%** |
| Người nhận | **3.771 / 3.772** |
| Nội dung *(người lập gõ)* | **100%** |
| Ngân hàng · pháp nhân | **100%** |
| Chủ dự toán *(`CDT`)* | **3.763** |
| ⚠ Số chứng từ | **3.237 = 85,8%** |
| Ngày | ⚠ nguồn là **sê-ri Excel** *(`45813.49`)*, phải đổi ra ngày |

### ⓑ Phía GIAO DỊCH — `8.387` dòng, và nó **chỉ có bốn điều**

| Trường | Có |
|---|--:|
| Ngày | **8.387** |
| Số tiền ＋ **chiều** *(Nợ = vào · Có = ra)* | **8.387** |
| Số chứng từ | **8.383** |
| Nguồn — **một chuỗi gộp 4 thứ**: `604046904001_OCBC SGD_SGO2` = số TK · ngân hàng · tiền tệ · pháp nhân | **8.387** |
| ⭐ Diễn giải sao kê | **8.358 = 99,7%** |

⛔ **RỖNG HOÀN TOÀN** *(⛔ đừng vẽ chỗ cho chúng)*: tên đối tác · pháp nhân *(cột riêng)* · số tài khoản *(cột riêng)* · mọi ô phân loại kế toán.

### ⓒ Kích thước nội dung — để chọn cỡ chữ và số dòng

| | ngắn nhất | trung bình | dài nhất |
|---|--:|--:|--:|
| Diễn giải giao dịch | 8 | **59** | **189** ký tự |
| Nội dung lệnh chi | — | — | **77** |
| Tên người nhận | — | — | **35** |

⚠ **Diễn giải xuống dòng giữa chừng** trong nguồn *(`49/180` mẫu)* — phải gộp lại trước khi hiện.

### ⓓ Khối lượng việc

```
3.772 lệnh chi
  ├─ 2.219 đã gán  (58,8%)   ← nhưng 0 do NGƯỜI gán
  └─ 1.553 chưa gán (41,2%)
       ├─   47  máy đề xuất — khớp CẢ số chứng từ LẪN số tiền ⇒ chỉ cần gật
       ├─  738  cần người chọn
       └─  768  ⛔ không gán được — sổ không có đồng tiền nào mang số ấy
```

Mỗi lệnh chi có **5–6 giao dịch ứng viên**, xếp theo bậc: `khớp số chứng từ` **(16)** › `đúng số tiền` **(61)** › `gần đúng số tiền` › `cùng đơn vị tiền` **(149)**.
⇒ ⭐ **Phần lớn ứng viên là bậc YẾU NHẤT.** Thiết kế phải làm cho khác biệt bậc **đọc được trong một cái liếc**, ⛔ không để bốn bậc trông như nhau.

Đơn vị tiền: **USD 21 · VND 12 · SGD 7** *(trên 40 lệnh mẫu)* ⇒ ⛔ **không** quy đổi, ⛔ **không** cộng hai đơn vị.

---

## §3 · Component cần thiết kế

> Bản dựng thử hiện tại: **https://claude.ai/artifact/4fx1gRCnLmE4m4Koy89V7P**
> Mã nguồn kèm dữ liệu thật: `Artifacts/man-gan-lenh-chi.html` *(bản dựng, ⛔ không phải sản phẩm)*

| # | Component | Trạng thái phải có |
|:-:|---|---|
| `C1` | **Dòng lệnh chi** trong danh sách | chưa gán · máy đề xuất · đã gán · đang chọn · hover · focus bàn phím |
| `C2` | **Thẻ lệnh chi** *(đầu panel)* | ba tầng: định danh → ai&bao nhiêu → bối cảnh |
| `C3` | ⭐ **Dòng giao dịch ứng viên** | chọn／không · 4 bậc · có／không diễn giải · khớp tiền／lệch tiền |
| `C4` | **Khối “đang gán với”** | chỉ xuất hiện khi lệnh đã gán; chứa `C3` ở dạng chỉ-đọc ＋ nút bỏ gán |
| `C5` | **Bộ lọc trạng thái** | `Chưa gán` ／ `Đã gán` ／ `Tất cả`, mỗi cái mang số đếm |
| `C6` | **Băng số việc** *(4 ô đầu màn)* | bình thường · nhấn mạnh tốt · nhấn mạnh cảnh báo |
| `C7` | **Dải cảnh báo trong panel** | ⚠ *“danh sách đã cắt bớt”* · ⛔ *“không gán được — vì sao”* |
| `C8` | **Thanh hành động** | `Gán` ／ `Đổi sang giao dịch đã chọn` · bật／tắt · câu gợi ý bên cạnh |
| `C9` | **Dải ngày** phân cách trong danh sách | dính đầu khi cuộn |
| `C10` | **Bốn trạng thái khung** | đang tải · rỗng · cửa lỗi · tuổi dữ liệu |

### ⭐ `C3` là component quan trọng nhất

Nó là nơi **quyết định xảy ra**. Một dòng phải trả lời ba câu, theo thứ tự:

1. **Đây là khoản gì?** → diễn giải sao kê *(bằng chứng chính)*
2. **Bao nhiêu, vào hay ra?** → số tiền ＋ chiều Nợ／Có
3. **Vì sao nó ở trong danh sách?** → nhãn bậc ＋ độ lệch tiền

Phụ: ngày · ngân hàng · 4 số cuối tài khoản · pháp nhân · số chứng từ.

---

## §4 · Luật thiết kế — ⛔ KHÔNG được vi phạm

Đây là luật của dự án, đã ký, có cổng máy canh. ⛔ Không phải sở thích.

| Mã | Luật | Nghĩa khi vẽ |
|---|---|---|
| ⭐⭐⭐ `INV-I16` | **Máy ⛔ không trả lời thay người** | Máy **đề xuất**; người **quyết**. Hai đáp án cùng đúng ⇒ máy **dừng** và nói ra, ⛔ không chọn bừa |
| ⭐⭐ `UI-F7` | **Ngân sách trường = 9** cho màn làm việc | Thêm một trường ⇒ **bỏ một**. Đo được: tệp màn cũ đi `339 → 735` dòng qua 7 lần sửa, ⛔ không lần nào giảm |
| ⭐⭐ `UI-F8` | **Số của MÁY ⛔ không lên màn của NGƯỜI** | Cấm: `hạng` · `luỹ kế %` · mọi `*_id` nội bộ · cờ `bool` · tên rổ · **dấu thời gian sê-ri**. Luật nhận biết: một trường là **của người** nếu người ta **làm khác đi** tuỳ giá trị của nó |
| ⭐ `UI-F9` | **Một sự thật, một chỗ hiện** | Đo được `8/36` trường trên màn cũ là **bản sao nguyên văn** của trường khác |
| `UI-F3` | Tiền dùng `tabular-nums`, **giữ đơn vị gốc** | ⛔ Không quy đổi, ⛔ không có dòng “tổng” gộp hai đơn vị |
| `UI-F2` | Màn chỉ hiện **việc cần làm** | Hàng chờ rỗng = khoẻ, ⛔ không phải lỗi |

### ⭐ Ba câu phải phân biệt được bằng **hình**, ⛔ không bằng chữ nhỏ

1. **“chưa có dữ liệu”** ≠ **“chưa đọc được”** ≠ **“không có”** — ba trạng thái khác nhau, đã cắn dự án một lần.
2. **“máy đề xuất”** ≠ **“người đã chốt”** — đây là `INV-I21` ở tầng giao diện. Nếu hai thứ trông giống nhau thì luật số 1 mất hiệu lực.
3. **“danh sách đã cắt bớt”** ≠ **“không có ứng viên nào”** — cắt im lặng làm người ta kết luận sai.

---

## §5 · Hệ thị giác đang có — ⛔ dùng lại, ⛔ đừng vẽ hệ thứ hai

Nguồn duy nhất: **`fls/web/tep/tokens.css`**. Có cổng máy `test_khong_ma_mau_go_tay.py` **NO** nếu một mã màu xuất hiện ở tệp khác.

```
chữ      IBM Plex Sans (giao diện) · IBM Plex Mono (số, mã, ngày)

mực      --ink      #14201e      nền thanh trên + chữ chính
         --muted    #5c6b68      chữ phụ
         --faint    #9aa8a5      chữ mờ

bề mặt   --surface  #ffffff      nền thẻ
         --alt      #f6f8f8      nền tiêu đề bảng
         --page     #eef1f1      nền trang
         --line     #dde4e3      mọi đường kẻ

tương tác --accent     #0e7570
          --accent-hi  #0a5c58
          --focus-ring #0e757022

ngữ nghĩa — TÁCH HẲN khỏi màu tương tác
         --good #2c7a4b  nền #e8f4ec  viền #bcdcc8
         --warn #c07414  nền #fdf4e7  viền #f0dcbe
         --crit #c73a3a  nền #fbeaea  viền #f3cdcd
         --info #2563eb  nền #e9effd  viền #b9cdf7

mật độ   --row 30px · --grid-fs 12.5px       (màn LÀM, dày hơn màn ĐỌC)
bo góc   4 / 6 / 8 / 999px
panel    sàn 430px · trần 680px — `clamp(sàn, 34vw, trần)`
```

⚠ **Phải làm được cả hai nền** *(sáng ／ tối)*: trang hiện theo cài đặt của người xem.

---

## §6 · Luật NGHIỆP VỤ của phép ghép — để thiết kế biết mình phục vụ cái gì

Kế toán phát biểu `18/09` *(`DT-I13`)*. ⛔ **Chưa được cài**, nhưng thiết kế nên chừa chỗ:

| Nhánh | Khoá ghép | Trạng thái |
|---|---|---|
| **Giao dịch Việt Nam** *(có mã PM trong giao dịch)* | mã PM ＋ số tiền ＋ **pháp nhân** | ⚠ chạy được **82,7%** |
| **Giao dịch nước ngoài** | **từ khoá trong diễn giải** ＋ **tên vendor** ＋ số tiền | ⚠ dữ liệu đã có, **phép tìm chưa viết** |

⇒ ⭐ **Hệ quả cho thiết kế:** diễn giải sao kê ⛔ không chỉ là chữ trang trí — với gần **một nửa** giao dịch *(nước ngoài, `4.145/8.387`)* nó là **bằng chứng duy nhất** để quyết. Tên vendor nằm **ngay trong** đó:

```
Card charge (OPENAI *CHATGPT SUBSCR)
FUNDS TRF - TT 1OR606160155C01 · SENSORTOWER, INC.
PAYMENT/TRANSFER CSDB STRIPE PAYMENTS SIN STRIPE LKuWsFH5A
03088010516666-123728-CK 24/7 cho 19033369015016 - Cp hc ns
```

⇒ ⛔ **Đừng cắt nó xuống một dòng mờ.** Nhưng nó dài tới **189 ký tự** ⇒ cần một phép **rút gọn có kiểm soát** ＋ cách xem đầy đủ.

---

## §7 · ⚰ ĐÃ THỬ VÀ BỊ BÁC — đọc để khỏi làm lại

| Đã thử | Ai bác | Vì sao |
|---|---|---|
| **Gom `2.219` dòng về `29` nhóm** để giảm cú bấm | Owner | *"Mapping làm **mỗi ngày, theo từng giao dịch 1**"* ⇒ gom nhóm tối ưu cho **một đợt dọn tồn**, ⛔ không cho **nhịp hằng ngày**. Tối ưu **sai nhịp** thì màn đúng số mà **sai việc** |
| Nhãn **“ô chờ gật”** ở đầu màn | Owner hỏi *"là gì?"* | Nó đếm **ô** *(`2.219 × 2`)* — **đơn vị của máy**. Người làm đếm theo **việc**. Vi phạm chính `UI-F8` |
| Chữ **“máy đã đoán” ／ “người đã chốt”** | Owner | Nói về **ai làm**; người dùng cần biết **việc đang ở đâu** ⇒ **`đề xuất gán` ／ `đã gán`** |
| **Bỏ** nút *“xem đủ trường”* | Kế toán | Tôi tưởng nó phục vụ **việc ghép**; họ cần nó để **YÊN TÂM VỀ DATA**. ⇒ Hai nhu cầu khác nhau: xem-đủ là nhu cầu **thưa**, ghép là nhu cầu **mỗi dòng**. Cách đúng: một **đường sang màn Sổ**, ⛔ không nới `UI-F7` |
| In nguyên chuỗi nguồn `604046904001_OCBC SGD_SGO2` | — | Chuỗi kỹ thuật, và nó **lặp pháp nhân** đã hiện chỗ khác *(`UI-F9`)* ⇒ tách thành phần, rút số TK còn **4 số cuối** |
| Một màn **soát chi không lệnh** | Owner | *"FLS ⛔ không cần trả lời câu hỏi đó"* — màn dựng cho một câu **không ai hỏi** |

---

## §8 · Câu hỏi mở — thiết kế ⛔ không tự trả lời được

| # | Câu | Ai trả lời |
|:-:|---|---|
| 1 | Diễn giải dài `189` ký tự: rút gọn **mấy dòng**, và xem đầy đủ **bằng cách nào** *(mở rộng tại chỗ ／ tooltip ／ panel phụ)*? | Thiết kế ＋ kế toán |
| 2 | Bốn bậc ứng viên nên phân biệt bằng **màu**, **thứ tự**, hay **nhóm có tiêu đề**? `149/226` ứng viên là bậc yếu nhất | Thiết kế |
| 3 | Khi lệnh đã gán, mối nối hiện tại nên nằm **trên** danh sách ứng viên hay **trong** nó *(đánh dấu)*? | Thiết kế ＋ kế toán |
| 4 | Nút `Xong` *(`QĐ-ITL-71`)* còn sống ⛔ không? Thiết kế mới cho một dòng **ba** đường ra, ⛔ không đường nào là `Xong` | **Owner** |
| 5 | Pháp nhân dùng để **lọc** ứng viên hay chỉ để **xếp trên**? Đo được: một pháp nhân **trả hộ** pháp nhân khác là chuyện **có thật** | **Kế toán** |

---

## §9 · Cái gì là thành công

⛔ **Không** phải *"trông hiện đại"*. Ba phép đo:

1. ⭐ **Có người thật dùng** — mối nối do người tạo đi từ `0` lên một số khác `0`.
2. **Mắt tìm được bằng chứng trong một cái liếc** — diễn giải và số tiền là hai thứ quyết định.
3. **Người ⛔ không gật theo phản xạ** — `45%` ca ⛔ không có ứng viên khớp đúng tiền, và màn **phải trông khác** ở những ca ấy, nếu không kế toán sẽ quen tay bấm `↵`.

---

## Changelog
- **v1.0** *(2026-09-18)*: bản đầu. Gói bối cảnh ＋ ràng buộc dữ liệu thật ＋ 10 component ＋ luật ⛔ không được vi phạm ＋ những thứ **đã bị bác** kèm lý do. ⭐ Mọi con số trong tệp **đo trên kho đang chạy** ngày `18/09`, ⛔ không dẫn lại từ tài liệu.
