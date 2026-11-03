# BRIEF — panel đối soát `F02 · Sổ ITL`

**Mốc đo:** 2026-09-04 · **Nguồn số:** kho thật `fls_itl`, 10.030 dòng, phạm vi
`chi_nap_that()` *(⛔ đã trừ kho test)*

> ⭐ Mọi con số trong tệp này **đo được**, ⛔ không phải ước lượng. Chỗ nào chưa
> đo được thì ghi thẳng **⛔ chưa đo**.

---

## §1 · Ai dùng màn này, và để làm gì

Luồng `PM → ITL` thật sự chỉ có **2–3 kế toán** *(`QĐ-ITL-27`)*. Kế toán trưởng
và CFO-COO **hầu như không tham gia** ⇒ ⛔ **không có bước duyệt, ⛔ không có
maker-checker**. Người gõ là người chốt.

⇒ Đây là màn **LÀM**, ⛔ không phải màn **ĐỌC**. Kế toán quét hàng trăm dòng một
buổi. Mật độ ở đây **cố ý dày hơn** các màn khác của hệ *(`BA-06` §7)*.

**Một vòng việc:** thấy một dòng tiền ra/vào từ ngân hàng → mở panel → nhìn
chứng từ gốc + mối nối lệnh chi → **gõ 7 ô phân loại** → sang dòng sau.

## §2 · Panel hiện có gì — kiểm kê

Bố cục **master–detail**: lưới trái, panel phải. Panel mở tại chỗ, ⛔ không che
lưới.

| | Khối | Nội dung | Ghi chú thiết kế |
|---|---|---|---|
| | **Dải phán quyết** | tối đa 8 chip: *ô chưa gán · ô máy đoán · ⛔ không tra được phân bổ · ghép lệnh chi · bút toán tay · lần sửa · kỳ mở/chốt · đã xong* | bấm chip là **nhảy** xuống đúng khối |
| ① | Chứng từ | **9 ô** chỉ đọc: ngày · số chứng từ · diễn giải · tiền tệ · PS Nợ · PS Có · tài khoản · LE · pháp nhân thanh toán | ô ngắn xếp đôi, ô dài trải nguyên dòng |
| ①b | Đủ **38 cột** sổ gốc | nguyên văn ô sổ, chỉ đọc | **95% ô rỗng** ⇒ đang gấp lại, có đếm |
| ② | **7 ô SỬA ĐƯỢC** | mã hợp đồng · loại giao dịch · chủ dự toán · bắt đầu DV · kết thúc DV · mã đối tác · hoá đơn | ⭐ **đây là lý do panel tồn tại** |
| ③ | Phân bổ 🔒 | 3 ô **máy suy**, người ⛔ không gõ được | `#N/A` khi tra không ra |
| ④ | Hoá đơn | chip tệp đính kèm | có tệp chỉ có **tên** mà ⛔ không có link |
| ⑤ | Mối nối lệnh chi | bảng: lệnh chi · tiền · hình · lần | |
| ⑥ | Bút toán tay | bảng: # · ô · giá trị · ai · nút **Đảo** | |
| ⑦ | Nhật ký `AUD-1` | lịch sử sửa | |

**Tổng: 57 ô dữ liệu + 3 bảng con + 1 dải chip.** Bảy khối hiện **nặng ngang
nhau** — cùng cỡ tiêu đề, cùng viền, cùng nền.

### Bốn kiểu ô của 7 ô sửa được *(`QĐ-ITL-87`, owner chốt 03/09)*

| Ô | Kiểu | Vì sao |
|---|---|---|
| `mã hợp đồng` | gợi ý từ **danh mục 73 mã** thật | có danh mục ⇒ cửa ghi **chặn** mã bịa |
| `loại giao dịch` | **⛔ ĐÓNG** — chỉ 4 giá trị | đóng được thì đóng |
| `chủ dự toán` · `mã đối tác` | **⭐ MỞ** — gợi ý từ giá trị đang dùng, cho điền mới | danh mục **suy từ chính sổ** ⇒ ⛔ không được ép *(`INV-I18`)* |
| `hoá đơn` | **gõ tay** | owner chốt |
| `bắt đầu/kết thúc DV` | **ô chọn THÁNG** | 99,8% là `YYYYMM` — một **KỲ**, ⛔ không phải NGÀY |

## §3 · Vấn đề — đo được

### ⓐ Ký hiệu đã mất nghĩa

**235 ký hiệu / 260 câu** hiện ra màn hình — gần **một ký hiệu mỗi câu**.

```
⛔  111      ·   38      ⭐   8      ⇒   1
—    51      ⚠   12      🔒  10      →   4
```

Và đây là chỗ hỏng thật:

- **73/111 (66%)** dấu ⛔ đứng ngay trước chữ **"không"/"chưa"**
- **5 chỗ** có **⛔ ⛔** hai dấu liền nhau
- **2 dấu ⛔** nằm trong câu **báo tin TỐT**: `✓ dòng này ⛔ không còn việc`

⇒ Dấu ⛔ ⛔ **không còn đánh dấu nguy hiểm**. Nó đã dính vào **chữ phủ định** và
thành một **tật chính tả**. Một tín hiệu dùng 111 lần trên một màn ⛔ không còn
là tín hiệu.

### ⓑ Trạng thái báo động **chính là** trạng thái bình thường

| `work_status` | dòng | % |
|---|---|---|
| `UNMAPPED` | **7.682** | **76,6%** |
| `ok` | 2.348 | 23,4% |

⇒ *"Dòng này chưa xong"* là chuyện của **ba phần tư cuốn sổ**. Vẽ nó bằng ngôn
ngữ báo động thì màn hình lúc nào cũng đang **kêu**, và khi có **chuyện thật**
thì ⛔ không còn nấc nào cao hơn để dùng.

⭐ **Gợi ý hướng:** *chưa phân loại* nên là trạng thái **BÌNH THẢN** *(việc đang
chờ)*, để dành ngôn ngữ báo động cho **ít, hiếm và thật**: cả hai vế tiền đều
khác 0 · kỳ đã chốt mà vẫn sửa · gõ khác nguồn · tra không ra phân bổ.

### ⓒ Bảy khối nặng ngang nhau

Kế toán mở panel để **gõ khối ②**. Sáu khối kia là để **tra khi cần**. Hiện tất
cả cùng một trọng lượng thị giác, và khối ② nằm **sau** hai khối chỉ đọc — trong
đó có khối ①b **38 cột / 95% rỗng**.

### ⓓ Chữ trên màn đang giảng bài

Câu dài nhất hiện ra màn hình: **73 ký tự**, và nhiều câu đang giải thích **nội
bộ hệ thống** *(`GAP-SCR-09`, `VLOOKUP`, `QĐ-ITL-64`, `INV-I16`)* cho một người
chỉ cần biết **phải làm gì**.

## §4 · ⛔ MƯỜI BA RÀNG BUỘC CỨNG

> ⛔⛔ Mỗi cái đến từ **một lỗi đã xảy ra thật** hoặc **một luật của cuốn sổ**.
> Thiết kế đẹp mà phá một trong 13 cái này thì ⛔ **không dùng được**.
> ⭐ Lật được — nhưng phải lật **công khai**, ⛔ không lặng lẽ.

| # | Ràng buộc | Vì sao |
|---|---|---|
| 1 | ⛔ **⛔ Không bao giờ mặc định im lặng.** Tra không ra thì **nói ra** | `INV-I16`. Sổ Gsheet có **6.843 ô** đã bị gán mặc định trong im lặng — chính là cái đẻ ra `GAC-OTH` |
| 2 | ⛔ **`#N/A` hiện nguyên**, ⛔ đừng chữa cho đẹp | Đó là **câu trả lời đúng**; sổ thật cũng đang hiện `#N/A` ở đúng chỗ đó |
| 3 | ⛔ **Bản khai RỖNG = máy ⛔ KHÔNG BIẾT**, ⛔ ≠ *"mọi giá trị đều sai"* | `INV-I17`. Hai câu này người dùng ⛔ không có cách nào phân biệt nếu màn vẽ giống nhau |
| 4 | ⭐ **Một ô có BA nguồn** — *sổ gốc nói gì · máy đoán gì · người gõ gì* — cả ba **phải phân biệt được bằng mắt** | `QĐ-ITL-35`. Gộp lại là xoá mất câu *"sổ gốc nói gì"* |
| 5 | 🔒 **Ba ô phân bổ là MÁY suy** — ⛔ phải ⛔ không trông như gõ được | `QĐ-ITL-64`. Một dấu `✎` mà ⛔ không có gì phía sau là một **lời hứa**, ⛔ không phải tính năng |
| 6 | ⭐ **Tiền: `Nợ` = vào (+) · `Có` = ra (−).** Một vế **có tiền** khi nó ⛔ không rỗng **VÀ khác 0**. Cả hai vế khác 0 ⇒ máy ⛔ **không chọn hộ** | `DT-I10`. Phép cũ *"ô nào không rỗng"* làm **3.630/10.030 dòng (36%)** hiện **sai số tiền** — và ⛔ **không ai nhìn thấy được** |
| 7 | ⛔ **Tiền ⛔ KHÔNG BAO GIỜ là `float`** — luôn là chuỗi | làm tròn nhị phân trên một cuốn sổ tiền |
| 8 | ⭐ **Mặc định chữ MÁY (`mono`)**; chữ thường **chỉ cho `Diễn giải`** | gần hết giá trị ở đây là **mã** — `FT24295070629325` · `R \| PO2_OCBC USD_SGO2`. Chữ máy thì ký tự **thẳng cột**, một ký tự bị đổi **nhìn ra được** |
| 9 | ⛔ **Màu ⛔ không bao giờ là thứ DUY NHẤT chở một nghĩa** | mù màu · in ra giấy · và đây là cuốn **sổ tiền** |
| 10 | ⛔ **⛔ Không bịa mã màu mới.** Chỉ `tokens.css` được có `#rrggbb` | có bài quét **NO** mọi tệp khác. Trước đây bộ màu tồn tại ở **ba chỗ** và chúng đã lệch |
| 11 | ⚠ **`430px` là SÀN, ⛔ không phải số cố định** | nó là con số bản vẽ, đang **chờ UAT trả lời có đủ không** *(`GAP-SCR-03`)*. Bỏ nó đi là vứt mất câu hỏi ấy |
| 12 | ⛔ **Tên ô lấy TỪ BẢN KHAI**, ⛔ không gõ tay | có cổng đối chiếu **hai chiều**. Gõ tay thì mai sổ đổi tên cột, màn vẫn hiện tên cũ và ⛔ **không phép thử nào đo** |
| 13 | ⛔ **Kỳ đã CHỐT thì ⛔ không ô nào gõ được**, kể cả có `force` | `INV-I13` |

## §5 · Bộ màu đang có

Xem `tokens.SNAPSHOT.css`. **Bốn màu ngữ nghĩa** *(mỗi màu 3 sắc: chữ · nền ·
viền)* — và chúng đang **bị dùng rất ít**:

```
--crit  #c73a3a   nguy — hiện gần như chỉ dùng cho số âm
--warn  #c07414   cảnh
--good  #2c7a4b   xong
--info  #2563eb   tin
```

Màu tương tác là **xanh mòng két** `--accent #0e7570` — tách hẳn khỏi 4 màu ngữ
nghĩa, ⛔ và phải giữ tách.

⇒ ⭐ **Kế toán xin thêm màu, và bộ màu đã có sẵn — vấn đề là nó chưa được
dùng.** Việc cần làm ⛔ không phải thêm màu; là **gán nghĩa cho màu đã có** rồi
dùng nhất quán.

## §6 · Dữ liệu thật — `DATA.json`

**6 dòng thật**, 6 tình huống khác nhau, mỗi dòng **49 trường + mảng `canon` 38
vị trí**:

| `itl_id` | tình huống |
|---|---|
| 9828 | sạch nhất — đã phân loại, có ghép lệnh chi |
| 10049 | `UNMAPPED` — chưa ai phân loại *(76,6% sổ là thế này)* |
| 10043 | **tiền vào** *(PS Nợ khác 0)* — dấu ngược với đa số |
| 9643 | **ngoại tệ** |
| 10029 | **diễn giải dài** *(134 ký tự)* — thử thách bề rộng ô |
| 9850 | đã có **người gõ tay đè** lên giá trị nguồn |

⛔⛔ **Văn xuôi trong tệp này là chữ TỔNG HỢP.** `Diễn giải` và 4 vị trí văn
xuôi khác trong `canon` *(Nội dung PE/PI · Ghi chú)* có thể mang **tên người**
⇒ chúng đã bị thay bằng chữ tổng hợp **giữ đúng độ dài và hình dạng**, ⛔ không
giữ nội dung. Hai ô đính kèm mang **link Drive nội bộ** cũng đã thay. Mọi giá
trị **mã** *(tài khoản · pháp nhân · mã hợp đồng · ngày · tiền)* là **thật**.

⭐ Có cổng kiểm phép thay này, và nó **đã được chứng minh đỏ** trước khi tin.

### Hình dạng giá trị thật — để canh bề rộng ô

| Trường | Giá trị riêng | Dài nhất | Hay gặp nhất |
|---|---|---|---|
| `acct` | 57 | **35** | `R \| PO2_OCBC USD_SGO2` |
| `hd` | 30 | **43** | `HCC \| HR Culture Activities` |
| `pay_type` | **4** | 29 | `Thanh toán (Regular)` |
| `cdt1` | **9** | 20 | `SHQ2 \| Headquarters2` |
| `curr` | **4** | 3 | `VND` `USD` `SGD` |
| `le` | 23 | 13 | `SGO2` `CN` `VGOH` |
| `doc_no` | 9.091 | 40 | `PC00060VVOV` · `FT26230301024824` |
| `pm_hinh` | **3** | 1 | `A` `B` `C` |

## §7 · Việc mở — ⛔ chưa làm, ⛔ và ⛔ không giấu

Năm việc kế toán chỉ ra, ⛔ chưa dựng — ⭐ nếu thiết kế của bạn chạm tới thì
**nói ra**:

1. ⛔ **⛔ Không có nút *Xong*** ở `F02` — vòng việc **hở ở cả hai đầu**
2. Bộ lọc chỉ soi **200 dòng đã nạp** — *"không tìm thấy"* và *"chưa nạp tới"*
   trông **y hệt nhau**
3. ⛔ **⛔ Không xếp được thứ tự cột**
4. `LE` *(cột P)* vs `Pháp nhân thanh toán` *(cột L)* lệch nhau thì **phải đỏ**
   *(`US-032`)* — màn hiện **⛔ chưa so**
5. Chia việc theo **CỘT** *(`PIC: LAN` / `PIC: THƯƠNG`)* — ⛔ chưa được mô hình
   hoá
