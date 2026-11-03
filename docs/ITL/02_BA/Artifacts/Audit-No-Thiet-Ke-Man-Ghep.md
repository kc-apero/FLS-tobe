# AUDIT NỢ THIẾT KẾ — màn **Gán lệnh chi ↔ Giao dịch** *(`SCR-F01`)*

**Ngày:** 2026-09-21 · **Chủ sở hữu:** BA · **Loại:** nghiên cứu *(⛔ không phải đợt sửa)*

**Câu owner hỏi:** *"có trường thông tin, tính năng, behavior màn hình trong tài liệu thiết kế này chưa được address trong tài liệu BA, dev, test?"*

**Đo trên:** `Artifacts/Thiet-ke-Man-Gan-Lenh-Chi.md` ＋ `fls-gan-lenh-chi_10.html` *(bản dựng)* × `BA-03` · `BA-06` · `BA-07` · `BA-08` · `BA-11` · `BA-13` · `DEV-12` · `TEST-03` × **kho `fls` THẬT** *(ảnh PM hiệu lực, `3.772` dòng lệnh · `8.387` dòng tiền)*.

> ⭐⭐ **Cách đo: ⛔ KHÔNG đọc hai tệp rồi so câu chữ.** Mỗi mục được soi xuống **kho** hoặc **mã**. Bốn phát hiện nặng nhất đều **⛔ không nhìn ra được** bằng cách đọc — chúng cần một câu lệnh đếm.

---

## §1 · Kiểm kê — thiết kế đòi gì

| Nhóm | Số mục | Đã address | ⛔ Chưa |
|---|--:|--:|--:|
| Trường thông tin *(thẻ lệnh chi ＋ khối bung ＋ dòng ứng viên)* | **38** | 31 | **7** |
| Tính năng | **11** | 8 | **3** |
| Behavior | **8** | 5 | **3** |
| | **57** | **44** | ⛔ **13** |

---

## §2 · ⭐⭐⭐ SỔ NỢ — xếp theo *(Mức × Tần suất) / Công*

### ⛔⛔ Hạng CHẶN — `4` mục

| Mã | Nợ | Loại | Đo được | Ai xử |
|---|---|---|---|---|
| ⭐⭐⭐ `ND-01` | **«Bỏ gán» và «Đổi sang giao dịch khác» ⛔ KHÔNG CÓ CỬA TƯƠNG THÍCH** — `POST /queue/{itl_id}/unmatch` bỏ **TOÀN BỘ** mối nối của dòng tiền và **⛔ không nhận `pm_line_ids`** *(`QĐ-ITL-69`)*. Lý do ⛔ không phải sơ suất: bỏ lẻ làm `Σ mối nối ≠ tiền bank`, đúng trạng thái cổng `SIGMA_MOI_NOI` dựng ra để bắt. ⛔ Thiết kế lại cho nút **bỏ một cặp**, và `C8` *«Đổi sang giao dịch đã chọn»* cũng là **bỏ một cặp rồi nối lại** | Cấu trúc | ⭐ **Đo, và nó THU NHỎ vấn đề:** chỉ **`25/2.222` = 1,1%** dòng tiền mang **chùm** *(>1 mối nối)*; **`65/2.262` = 2,9%** mối nối nằm trong chùm. Chùm lớn nhất: **10** dòng lệnh trên một dòng tiền ⇒ ⭐ **Cửa ĐỨNG NGUYÊN; MÀN phải nói ra thiệt hại**: ở `1,1%` ca ấy nút `Bỏ gán` hiện nay sẽ **âm thầm gỡ tới 9 dòng lệnh khác** | BA ＋ Dev |
| ⭐⭐⭐ `ND-02` | **Khối «Xem đủ trường» GIẤU IM LẶNG trường vắng** — `kv()` **bỏ qua** hàng khi giá trị rỗng *(`if(r[1]==null‖r[1]==="")return;`)* ⇒ trường vắng **biến mất ⛔ không một chữ nào** | ⚠ Accessibility ＋ Cấu trúc | ⛔⛔ **`tho` có `41` HÌNH DẠNG khác nhau** trên `3.772` dòng *(`27` khoá, mỗi dòng mang `18–23`)*: `Chi nhánh` **440 = 11,7%** · `PE (Urgent)` **17 = 0,45%** · `PE (Advance)` **483** · `ID PESlip` **500** · `Ghi chú` **626** · `Status_Final` **3.532**. ⭐ Khối này tồn tại để kế toán **YÊN TÂM VỀ DATA** *(`QĐ-ITL-144 ⓐ`)* ⇒ nó là **chỗ tệ nhất** để một trường biến mất ⛔ không lời giải thích: *"FLS ⛔ chưa đọc"* và *"dòng này ⛔ không có"* trông **y hệt nhau** — đúng cặp `INV-I16` cấm, và đúng cặp **hợp đồng thiết kế tự khai** là phải phân biệt **bằng hình** | BA ＋ Dev |
| ⭐⭐ `ND-03` | **`ung_vien[]` ⛔ CHƯA KHAI MỘT TRƯỜNG NÀO** — `BA-07` ghi `itl-candidates` trả `ung_vien[]` rồi **dừng**. Thiết kế cần **10** trường mỗi ứng viên: `itl_id` · ngày · số CT · **diễn giải** · số tiền · **chiều Nợ/Có** · đơn vị tiền · **nguồn tách 4 mảnh** · **bậc** · **độ lệch** | Tài liệu | ⛔ `0/10` trường được khai ⇒ **dev phải đoán `10` lần**. ⭐ Bậc thì **có** khai *(`ma › tien › gan_tien › cung_tien_te`)*, nhưng nó nằm ở **văn xuôi**, ⛔ không ở khuôn trả về | BA |
| ⭐⭐ `ND-04` | **Chế độ «Toàn sổ» ⛔ KHÔNG CÓ CỬA** — nó đổi **nguồn** danh sách sang toàn bộ sổ **và tính lại bậc theo lệnh đang mở**. Cửa gần nhất `GET /ledger` chỉ lọc `?period=&le=&status=` — ⛔ **không tìm chữ**, ⛔ **không** biết lệnh nào đang mở nên ⛔ **không** tính lại bậc được | Cấu trúc | ⭐ Và nó ⛔ không phải tính năng phụ: hợp đồng cho nó **bật sẵn** với lệnh máy ⛔ không tìm được ứng viên — tức nó là **lối thoát khỏi ngõ cụt** cho **`768`** dòng | BA ＋ Dev |

### ⚠ Hạng VỪA — `6` mục

| Mã | Nợ | Loại | Đo được | Ai xử |
|---|---|---|---|---|
| ⭐⭐ `ND-05` | **Luật tách `source_sheet` ⛔ chưa đặc tả — và MỌI tài liệu đang trích SAI giá trị thật** | Tài liệu | ⛔⛔ Giá trị thật mang **tiền tố `R \| `**: `R \| PO2_OCBC USD_SGO2`, **`8.387/8.387`** dòng. `BA-06 §4.4 ⓒ`, hợp đồng thiết kế và brief đều trích **⛔ không có tiền tố** ⇒ phép tách chép theo tài liệu **hỏng ngay ký tự đầu**. ⭐ Tin tốt: sau khi bóc tiền tố, tách **4 mảnh** *(số TK · ngân hàng · tiền tệ · pháp nhân)* được **`8.387/8.387` trên `49` nguồn**. ⚠ Nhưng **`6` tài khoản ⛔ KHÔNG phải số** *(`PO1`·`PO2`·`PO3`·`PO5`·`PO6`·`PO9` — tài khoản thẻ)* ⇒ luật *"rút còn 4 số cuối"* cho ra **`••PO2`** | BA |
| ⭐⭐ `ND-06` | **`fls_dien_giai` ⛔ KHÔNG cửa API nào trả** — khung xem có từ `18/09` *(migration `0026`, **99,7%**)*, `BA-07` ⛔ chưa cập nhật | Tài liệu | Thiết kế đặt diễn giải là **cột ⛔ không bao giờ bị hy sinh** và là **bằng chứng duy nhất** của `49%` cuốn sổ ⇒ cửa ⛔ không trả nó thì cột ấy **rỗng** | BA |
| ⭐ `ND-07` | **⛔ KHÔNG một yêu cầu a11y nào trong cả bộ** — `BA-08` ⛔ không có `WCAG` · tương phản · `focus` · `aria` · bàn phím | Accessibility | ⭐ Nghịch lý: **bản thiết kế LÀM TỐT HƠN yêu cầu** *(`aria-current` · vòng focus · `9` phím tắt · nền sáng/tối)*, nhưng ⛔ **không cổng nào giữ** ⇒ lần sửa sau **rơi mất trong im lặng**, đúng hình `339 → 735` | BA |
| ⭐ `ND-08` | **Nền tối chỉ sống trong hiện vật thiết kế** — `BA-06`／`BA-08` ⛔ không nhắc một chữ | Tài liệu | **Một nửa** `tokens-man-ghep.css` là cho nền tối *(`2` khối × `17` token)*. ⛔ ⛔ Không khai thì nó ⛔ không phải yêu cầu, và người cài **bỏ được mà ⛔ không sai spec** | BA |
| ⭐ `ND-09` | **Trường `Người lập` trong khối bung ⛔ KHÔNG CÓ NGUỒN** | Tài liệu | Quét **`27`** khoá `tho` trên cả ảnh: ⛔ **không** khoá nào là *người lập* ／ *email*. ⚠ Và nếu tìm được thì nó là **dữ liệu cá nhân** — phải qua `QĐ` riêng | BA ＋ Owner |
| ⭐ `ND-10` | **Cửa `unmatch` đòi `reason`, mà `QĐ-ITL-137` đã HOÃN cột lý do** | Tài liệu | Thân yêu cầu *"chỉ có `reason`"* *(`BA-07` v1.7)*; màn mới ⛔ **không thu** lý do nào ⇒ hoặc `reason` thành **tuỳ chọn**, hoặc màn phải hỏi — ⛔ không được để dev tự chọn | BA |

### ⬜ Hạng NHẸ — `3` mục

| Mã | Nợ | Đo được |
|---|---|---|
| `ND-11` | **`Status_Log` có trong kho, thiết kế ⛔ không hiện** | **`3.125/3.772`** dòng mang trường này. Cố ý hay bỏ sót — ⛔ chưa ai nói ra |
| `ND-12` | **Bản dựng dữ liệu thật tự vi phạm luật của chính hợp đồng** | `man-gan-lenh-chi-v2.html` in **nguyên** `3759017445`, trong khi `_10` che còn `••4001`. ⚠ Là tài khoản **công ty**, ⛔ không phải dữ liệu cá nhân ⇒ ⛔ không phải sự cố riêng tư |
| `ND-13` | **Bộ lọc `3` chip gộp `768` đích cuối** ⇒ `G-a` trượt | Đã có mã riêng: **`GAP-SCR-20 ⓑ`** — ⛔ không mở mã thứ hai |

---

## §3 · Nợ TEST — ⛔ không mục nào có bài gọi tên

| Hành vi thiết kế | Bất biến đứng sau | Bài gọi tên |
|---|---|--:|
| Máy ⛔ không chọn sẵn ứng viên | `INV-I16` ở **tầng màn** | ⛔ **0** |
| `Enter` bị khoá ở ca lệch tiền | `INV-I16` | ⛔ **0** |
| Hai bước xác nhận khi lệch | `INV-I16` | ⛔ **0** |
| Bỏ gán = **THÊM** một dòng | `INV-I08` | ⚠ có bài `I08`, ⛔ **không** bài nào đi qua cửa `unmatch` |
| `768` đích cuối ⛔ không trộn vào việc | ⭐ `INV-I20` | ⛔⛔ **0** — `INV-I20` ⛔ **chưa một bài nào gọi tên** *(so: `INV-I16` có **45**)* |

⛔⛔ **`TEST-03` đang khai `13/21` bất biến ⛔ không bài nào gọi tên.** `INV-I20` — bất biến **chính** của màn này — nằm trong `13` ấy. ⇒ Cổng `G-a` trượt mà ⛔ **không cổng máy nào** báo, vì ⛔ không có bài nào hỏi câu ấy.

---

## §4 · Nợ USER STORY

`BA-03` có `US-KT-052`…`056` cho màn ghép. Soi vào thiết kế:

| Thiết kế | US |
|---|---|
| Hỏi từ phía lệnh chi | ✅ `US-KT-052` |
| Biết ai trả lời được *(rổ)* | ✅ `US-KT-053` |
| Duyệt cả lô tự chứng | ✅ `US-KT-054` |
| ⭐ Xem đủ trường của phiếu | ✅ `US-KT-055` |
| Gỡ mối nối | ✅ `US-KT-056` |
| ⛔ **Tra cứu TOÀN SỔ** | ⛔ **⛔ chưa có** |
| ⛔ **ĐỔI mapping sang giao dịch khác** | ⛔ **⛔ chưa có** — owner nêu `18/09`: *"UC thay đổi mapping"* |
| ⛔ **Đọc nguyên văn diễn giải bị cắt** | ⛔ **⛔ chưa có** |
| ⛔ **⛔ Không gật theo phản xạ** | ⛔ **⛔ chưa có** — và đây là `AC` **đo được**, ⛔ không phải sở thích |

---

## §5 · Kế hoạch xử — ⛔ KHÔNG phải một đợt sửa

| Nhóm | Mục | Vì sao xếp vào đây |
|---|---|---|
| ⭐ **Thắng nhanh** *(công thấp, sửa được ngay)* | `ND-03` khai `10` trường `ung_vien[]` · `ND-05` đặc tả luật tách `source_sheet` *(＋ sửa `3` chỗ trích sai)* · `ND-06` khai `fls_dien_giai` vào `BA-07` · `ND-08` khai nền tối · `ND-10` chốt `reason` tuỳ chọn | Đều là **viết một đoạn đặc tả**, ⛔ không chạm mã, ⛔ không chạm kho |
| ⛔ **Việc cấu trúc** *(cần thiết kế ＋ mã)* | `ND-01` màn phải **nói ra chùm** trước khi bỏ gán · `ND-02` khối bung phải **hiện trường vắng** ⛔ không giấu · `ND-04` cửa tra cứu toàn sổ | Cả ba đổi **hành vi**, phải vào lộ trình |
| ⚠ **Nợ test** | `INV-I20` ＋ `4` hành vi chống gật | ⭐ Làm **trước** khi cài, ⛔ không sau — `TEST-03` đã chỉ ra *việc đáng làm trước tiên là ĐẶT MÃ SPEC vào tên bài* |
| ⬜ **Ghi rồi hoãn** | `ND-09` `Người lập` · `ND-11` `Status_Log` · `ND-12` che số TK ở bản `v2` | ⛔ Chưa ai đòi, và `ND-09` cần một quyết định riêng về dữ liệu cá nhân |

---

## §6 · ⭐⭐ Ba điều audit này khai về CHÍNH NÓ

1. ⛔ **`4` phát hiện nặng nhất ⛔ KHÔNG đọc ra được.** `41` hình dạng `tho` · tiền tố `R \| ` · `1,1%` chùm mối nối · `0` bài gọi tên `INV-I20` — cả bốn cần **một câu lệnh đếm**. Một đợt audit chỉ đọc tài liệu sẽ **báo xanh**.
2. ⚠ **Sổ này ⛔ không đo được *«thiết kế có dùng được ⛔ không»*.** Nó đo **độ khớp giữa thiết kế và bộ tài liệu** — hai thứ đều do **cùng một phía** viết ra. Phép đo thật vẫn là `G-d`: **mối nối do NGƯỜI tạo đi từ `0` lên khác `0`**.
3. ⭐ **`31/38` trường ĐÃ có chỗ**, và đó là con số đáng mừng — phần lớn thiết kế **đứng trên đặc tả đã có**. `13` mục thiếu tập trung ở **hai chỗ**: *khuôn trả về của cửa* và *cái màn phải nói khi dữ liệu vắng*.
