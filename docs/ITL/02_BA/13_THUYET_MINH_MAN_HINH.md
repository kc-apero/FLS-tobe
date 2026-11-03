# 13 — THUYẾT MINH MÀN HÌNH: từng nút, từng ô, và `US` nào đứng sau

**Version:** v1.9 · **Ngày:** 2026-10-05 · **Chủ sở hữu:** BA
**Vì sao có tệp này:** owner hỏi *"tại từng màn hình, thuyết minh ý nghĩa của từng `UC`/`US` và các nút bấm, hiển thị"*. `BA-06` đặc tả **màn phải có gì**; tệp này đi ngược lại — nó đọc **mã đang chạy** rồi nói **mỗi thứ đang có nghĩa là gì**.

**Căn cứ:** trích thẳng từ `fls/web/tep/man_f0*.js` ngày `2026-09-14` · số đo trên kho `fls` cùng ngày.

---

## §0 · Đọc tệp này thế nào

| Dấu | Nghĩa |
|:--:|---|
| ✅ | Đang chạy — bấm được hôm nay |
| ⛔ | ⛔ Chưa có trong mã |
| ⚠ | Có, ⛔ nhưng ⛔ không ở lằn mặc định |

⭐⭐ **Cột *"nếu bỏ đi thì sao"* là cột đắt nhất của tệp này.** Một nút mà câu trả lời là *"⛔ không sao cả"* là một nút **⛔ không ai cần** — và đó là câu hỏi đáng hỏi hơn *"nút này làm gì"*.

⛔ **Cổng canh tệp này:** `tools/kiem_thuyet_minh.py` quét **mọi nhãn nút** trong `fls/web/tep/man_*.js` và **NO** nếu một nhãn ⛔ không có dòng thuyết minh. ⇒ Thêm một nút mà ⛔ không giải thích nó thì **⛔ không qua cổng**. Đây chính là *"phép đo buộc tài liệu đi theo mã"* mà `BA-03` ⛔ **không có** — và vì thế `BA-03` đã già **ba lần** trong im lặng.

---

## §A · ⭐⭐⭐ ĐẶC TẢ SỐNG sau `CR#12` — **bốn chỗ, và chỉ HAI trong đó có việc**

> ⭐ **Tầng này là thứ `BA-06` ⛔ KHÔNG tả.** `BA-06 §4` nói màn **trông ra sao** và **vì sao**;
> từ đây trở xuống nói nó **phản ứng thế nào** — bấm thì gì xảy ra, rỗng thì hiện gì,
> cửa từ chối thì đọc ra câu gì. ⛔ Thiếu tầng này thì dev **phải đoán**, và chỗ đoán là chỗ sai.
>
> **Căn cứ số:** đo `2026-09-18` trên kho `fls`, bằng **chính hàm mà cửa gọi**
> *(`lenh_cho.dem_theo_ro`)* — ⛔ không dựng lại `SQL`, đúng bài học *"đo QUAN HỆ thì gọi hàm thật"*.

### §A0 · Bốn chỗ — và vì sao ⛔ KHÔNG phải bốn màn

| Chỗ | Dòng | Ai làm | Có nút ⛔ không |
|---|--:|---|---|
| ⭐ `Tự động` | **47** | máy ghép · người **duyệt** | ✅ **một** nút |
| ⭐ `Thủ công` | **738** | người **quyết từng dòng** | ✅ ghép · bỏ ghép |
| ⛔ Ghép ⛔ không được | **768** | ⛔ **không ai** | ⛔ **không nút nào** |
| ⚠ Lỗi nguồn | **167** | người **ngoài** FLS | ✅ đúng **một** nút *(GỬI)* |

⭐⭐ **`47 ＋ 738 ＋ 768 = 1.553` — khép đúng `tong` mà cửa trả.** Một bảng phân loại ⛔ không cộng về tổng là một bảng ⛔ không kiểm được. *(`167` dòng lỗi nguồn nằm **bên trong** `768`＋`738`, ⛔ không cộng thêm — chúng là một **thuộc tính** của dòng, ⛔ không phải một rổ thứ tư.)*

⛔⛔ **Vì sao một màn, ⛔ không bốn màn.** Người ghép ⛔ **không** chọn *"hôm nay tôi vào màn nào"* — họ chọn *"hôm nay tôi làm việc này"*. Bốn mục sidebar buộc họ **biết trước** dòng của mình rơi vào rổ nào, mà đó đúng là thứ họ vào đây để **hỏi**.

### §A1 · `Tự động` — **47** dòng, **một** cú bấm

**Câu chỗ này hỏi:** *"Máy đã có đáp án **duy nhất**. Anh gật ⛔ không?"*

**Cửa:** `GET /api/fls/v1/queue/lenh-cho/ro?ro=may&tu_chung=1` → `POST /api/fls/v1/queue/match-lo`

⭐⭐ **`tu_chung=1` ⛔ KHÔNG được bỏ, và đây là chỗ tôi đã sai một lần.** Rổ `may` có **250** dòng, nhưng cửa GHI chỉ **chắc chắn nhận 47** — `250` là một con số **hứa nhiều hơn cái bấm được**. `xu_ly.py` trả **`400`** nếu `tu_chung` đi kèm rổ khác.

| Cột hiện | Lấy từ | Vì sao ở đây |
|---|---|---|
| ✅ Người nhận | `tho["Tên tài khoản"]` | Câu đầu tiên mắt người tìm |
| ✅ Số tiền ＋ đơn vị | `amount` · `curr` | `tabular-nums`, ⛔ không quy đổi |
| ✅ Số chứng từ | `ref_tho` | Chính nó là **lý do** máy dám ghép |
| ✅ Dòng tiền sẽ nối | `ung_vien_itl[0]` → ngày · nội dung · tiền | ⛔ **Phải hiện cả hai vế**, ⛔ không chỉ vế lệnh |

⛔ **Bốn cột. ⛔ Không thêm.** `UI-F7` trần `9` là cho `Thủ công`; chỗ này người **⛔ không quyết**, nên mỗi cột thêm chỉ làm chậm mắt.

**Một nút: `Duyệt cả 47`.** Bấm ⇒ hộp xác nhận nói **ba** con số *(số dòng · Σ tiền **theo từng tiền tệ** · số phiếu)*, ⛔ không một dòng *"bạn chắc chứ?"*.

⛔⛔ **Cửa ghi có BẢY chỗ từ chối, và màn phải đọc được cả bảy** *(`BA-07`)*: ngoài phạm vi `404` · kỳ chốt `409` · đã ghép `409` · mã dòng ⛔ không có trong ảnh chụp `400` · khác tiền tệ `422` · `Σ` lệch `422` · `status` ⛔ không `Approve` `422`. ⇒ Sau khi bấm, màn hiện **biên bản**: *"nhận `N` · từ chối `M`"* ＋ **danh sách dòng bị từ chối kèm lý do**. ⛔ **Không** một chữ *"Thành công"*.

### §A2 · `Thủ công` — **738** dòng, **một việc một lúc**

**Câu chỗ này hỏi:** *"Lệnh chi này đã đi bằng đồng tiền nào?"*

**Cửa:** **HAI** lời gọi — `?ro=nguoi` *(**535**)* ＋ `?ro=may&tu_chung=0` *(**203**)*. ⚠ `GAP-SCR-18`.

⭐⭐⭐ **Và HAI nhóm ấy ⛔ KHÔNG cùng một câu hỏi** — màn phải trông **khác**:

| Nhóm | Dòng | Thiếu gì | Màn đưa ra |
|---|--:|---|---|
| **⛔ không số chứng từ** | **535** | ⛔ chưa có `Reference number` | Danh sách tiền lọc theo **tiền ＋ ngày**, ⛔ **không** chọn sẵn |
| **khớp mã, lệch tiền** | **203** | có mã, `Σ` ⛔ không bằng | Máy hỏi thẳng: *"lệnh này ăn **bao nhiêu** của giao dịch kia?"* |

⭐⭐ **Con số `535` tự chứng minh chính nó.** Đo độc lập trên `tho`: **`3.237/3.772` (85,8%)** dòng lệnh có ô `Reference number` ⇒ **`3.772 − 3.237 = 535`** — **đúng bằng** rổ `nguoi` mà `dem_theo_ro` trả về. Hai phép đo **⛔ không dùng chung một câu lệnh** mà ra cùng một số ⇒ phép chia rổ ⛔ **không** phải một nhãn máy tự đặt, nó là **một sự thật của dữ liệu**.

**Chín trường — và cả chín đều ĐÃ CÓ trong kho** *(đo `18/09`, `pm_line_id` phân biệt)*:

| # | Trường | Nguồn | Có ở |
|--:|---|---|--:|
| 1 | Người nhận | `tho["Tên tài khoản"]` | **3.771/3.772** |
| 2 | Số tiền | `amount` ＋ `curr` | **3.772** |
| 3 | Nội dung | `tho["Nội dung giao dịch nhập khi lập lệnh ở bank"]` | **3.772** |
| 4 | Ngân hàng | `tho["Ngân hàng"]` | **3.772** |
| 5 | Số tài khoản | `tho["Số tài khoản"]` | **3.771** |
| 6 | Pháp nhân | `tho["Pháp nhân thanh toán"]` | **3.772** |
| 7 | Phiếu | `pm_slip_id` | **3.772** |
| 8 | Số chứng từ | `ref_tho` | ⚠ **3.237** *(85,8%)* |
| 9 | Câu **vì sao** | `vi_sao` — **MÁY sinh** | theo rổ |

⛔⛔ **Năm trong chín trường sống trong `tho` (JSON), ⛔ KHÔNG phải cột.** ⇒ Cửa `ro` **phải trả chúng ra**; nếu ⛔ không, màn ⛔ **không vẽ nổi** một dòng nào. ⚠ Và `tho` **chỉ giữ ô ⛔ không rỗng** — *"thiếu khoá"* ⇒ **ô trống ở nguồn**, ⛔ **không** phải lỗi đọc. Màn hiện **`—`**, ⛔ không hiện `null`.

**Danh sách tiền — bốn bậc CÓ TÊN** *(`ma` › `tien` › `gan_tien` › `cung_tien_te`)*. ⛔ **Không** một điểm số mờ `0..1`: màn phải nói được **vì sao** dòng này đứng đầu.

⭐ **Hai ca, và màn PHẢI trông khác nhau** *(đo `500/535`: **275 = 55%** có một dòng tiền **khớp đúng số tiền** trong 4 ứng viên)*:

- **có ứng viên đúng tiền** ⇒ chip **`đúng số tiền`** ＋ **chọn sẵn**, `↵` là gật.
- **⛔ không có** ⇒ ⛔ **không chọn gì**, và nút ghép **mờ** cho tới khi người bấm một dòng. ⛔⛔ ⛔ Không làm thế thì `45%` còn lại sẽ bị gật theo **phản xạ**.

⭐⭐ **Hai đáp án cùng đúng ⇒ máy DỪNG** *(`INV-I16`)*. Ca thật: `PM01342-1` và `PM01964-1` cùng `1.035,50 SGD`, sổ có **đúng hai** dòng mang số ấy, **hai pháp nhân khác nhau**. Màn hiện **cả hai**, ⛔ **không** chọn sẵn, kèm câu *"hai dòng cùng khớp — pháp nhân khác nhau"*.

**`Bỏ ghép` PHẢI có ở dải vừa-xong** *(`US-056`)*: ⛔ không có bước xác nhận **trước** khi ghép, nên đường lùi phải nằm **sau**. Hộp xác nhận nói **hai** điều: bỏ **CẢ CHÙM** *(`QĐ-ITL-69`)*, và **sổ giữ lịch sử** — bỏ là **thêm một dòng**, ⛔ không xoá *(`INV-I08`)*.

### §A3 · Đích **Ghép ⛔ không được** — **768** dòng, ⛔ KHÔNG nút nào

⛔⛔ **Đây ⛔ không phải một hàng chờ, nó là một KẾT LUẬN.** Có số chứng từ nhưng sổ ⛔ không có đồng tiền nào mang số ấy ⇒ ngồi tìm là **phí công tuyệt đối**.

- Mỗi dòng **bắt buộc** mang `vi_sao` do **MÁY** sinh *(`lenh_cho.VI_SAO`)*. `QĐ-ITL-137` hoãn **cột lý do NGƯỜI gõ**, nó ⛔ **không** chạm vào câu này.
- ⭐ `272` dòng có bạn đời ở **8 sheet đã bỏ `10/09`** ⇒ câu vì sao phải nói **đúng chuyện ấy**, ⛔ không nói chung chung *"⛔ không tìm thấy"*.
- ⛔ **Không** nút `Xong`, ⛔ **không** nút `Hoãn`. Một dòng ở đây **đã rời** hàng chờ *(`INV-I20`)*.

### §A4 · Đích **Lỗi nguồn** — **167** dòng, đúng MỘT nút

⚠ **Cửa `GET /queue/loi-nguon` ⛔ CHƯA CÓ** *(`BA-07` v2.9 khai, ⬜ chưa dựng)*.

⭐⭐ **`QĐ-ITL-142` — và đây là chỗ tôi cộng sai.** `BA-06 §4.2b` viết *"`166` ô `Reject` ＋ `1` ô tiền tệ `20`"*. Đo lại bằng `pm_line_id` phân biệt: `ref_tho='Reject'` **167** · `curr` là một con số **1** · **giao nhau `1`** ⇒ hợp **167**. Hai tập **GIAO NHAU**, ⛔ không rời nhau — tổng đúng, **phép cộng sai**, và **cả hai cách cộng đều ra `167`** nên ⛔ không cổng nào thấy.

⭐ **Và dòng ấy kể một chuyện khác hẳn:** `PM00576-1` mang `ref_tho='Reject'` · `curr='20'` · `amount=20,00`. Nó ⛔ **không** phải *"một đơn vị tiền tệ tên `20`"* — nó là **một dòng bị XÊ CỘT** ở bảng tính nguồn. ⇒ Câu màn hiện phải là **cái ấy**, vì nó nói cho người sửa biết **phải sửa gì**.

**Một nút: `Gửi danh sách cho người sửa bảng tính`.** ⛔ FLS **chỉ mặt**, ⛔ không tự chữa *(`INV-I16`)* — nhưng *chỉ mặt* mà ⛔ không có người nhận việc thì **bằng ⛔ không**: `BA-12 §2ⓓ` chỉ mặt dòng này ngày `11/09`, và `18/09` nó **vẫn đứng đó**.

### §A5 · Bốn trạng thái — cho **cả bốn** chỗ

| Trạng thái | Hiện gì | ⛔ KHÔNG được |
|---|---|---|
| đang tải | khung xám giữ **đúng chiều cao** của hàng | ⛔ nhảy layout khi số về |
| **rỗng** | *"⛔ không còn việc nào ở đây"* ＋ **ngày giờ của lần nạp** | ⛔ vẽ một bảng trắng — rỗng vì **xong** và rỗng vì **chưa nạp** là hai chuyện |
| cửa lỗi | **mã lỗi ＋ câu của cửa**, nguyên văn | ⛔ nuốt lỗi rồi hiện `0` — một số `0` sai **⛔ không ai nghi ngờ** |
| tuổi dữ liệu | *"ảnh chụp lúc `hh:mm`"* ở **mọi** chỗ | ⛔ giấu — `22` ảnh PM trong kho, và người đang nhìn **một** trong số đó |

### §A6 · ⛔ Ba câu tệp này CHƯA trả lời được

| # | Câu hỏi | Vì sao chưa trả lời |
|--:|---|---|
| 1 | Nút **`Xong`** *(`QĐ-ITL-71`)* còn sống ⛔ không? | `§A0` cho một dòng **ba** đường ra, ⛔ không đường nào là `Xong`. Nhưng `QĐ-ITL-71` là **quyết định của owner** ⇒ ⛔ **không tự rút**. ⚠ `GAP-SCR-19` |
| 2 | `203` dòng lệch tiền chia tiền **thế nào** | Cần một cử chỉ *"lệnh này ăn `X` của giao dịch kia"* mà ⛔ **chưa cửa nào** nhận |
| 3 | Bàn phím | ⛔ Chưa đo ai gõ phím gì — và `BA-14 §8.2` nói thẳng: chưa **một người nào** từng ghép một dòng *(`hinh='T'` = `0`)* |

### §A7 · ⭐⭐⭐ HAI KHU VỰC sau buổi BA với kế toán `18/09` *(`QĐ-ITL-144`)*

> ⭐ Bốn yêu cầu giao diện do **kế toán** nêu. `§A1`…`§A6` viết **trước** buổi ấy; chỗ nào lệch thì **khu vực này thắng**, và `§A2` giữ nguyên chữ làm bản ghi.

#### ⓐ Khu vực **Lệnh chi chưa gán** — xếp theo **THỜI GIAN**

⛔⛔ **Bỏ hẳn phép gom nhóm.** Bản dựng `18/09` gom `2.219` dòng về `29` nhóm để giảm số cú bấm; owner bác: *"công việc mapping được thực hiện **mỗi ngày, theo từng giao dịch 1**"*. ⇒ ⭐ Gom nhóm tối ưu cho **một đợt dọn tồn**, còn màn này phục vụ **nhịp hằng ngày** — và tối ưu sai nhịp thì màn đúng về số liệu mà **sai về công việc**.

| Cột | Nguồn | Vì sao ở đây |
|---|---|---|
| dải **ngày** | `tho['Timestamp']` → ngày | Mốc của nhịp ngày. ⚠ Nguồn là **sê-ri Excel** `45813.49` — `UI-F8` cấm hiện dạng ấy, **phải đổi** |
| ⭐ **số PM** | `pm_line_id` | **Kế toán đòi** — họ đối chiếu với phiếu giấy／sheet bằng số này |
| người nhận | `tho['Tên tài khoản']` | Câu đầu mắt người tìm |
| nội dung | `tho['Nội dung giao dịch…']` | ✅ **100%** dòng lệnh có |
| số tiền ＋ đơn vị | `amount` · `curr` | `tabular-nums`, ⛔ không quy đổi |
| trạng thái | — | `đề xuất gán` ／ `đã gán` ／ *(trống = cần người chọn)* |

⭐⭐ **Chữ đúng là `đề xuất gán` và `đã gán`** *(owner sửa `18/09`)*. Bản trước tôi viết *"máy đã đoán"* ／ *"người đã chốt"* — ⛔ nói về **ai làm**, trong khi người dùng cần biết **việc đang ở đâu**.

⛔ **Và một nhãn bị BỎ: *"ô chờ gật"*.** Nó đếm **ô** *(`2.219 × 2 = 4.424`)* — **đơn vị của máy**. Người làm đếm theo **việc**. Chính `UI-F8` cấm điều đó, và tôi vi phạm ngay ở dòng đầu màn.

#### ⓑ Nút **xem đủ trường** — ⚰ sống lại, nhưng ⛔ KHÔNG nằm trong danh sách

Kế toán: *"cần view xem tổng các giao dịch, **đủ các trường** như GGSheet/Excel → **yên tâm về data**"*.

⇒ ⛔ **Không** nới `UI-F7`; mở **một đường sang `SCR-F02`** *(lưới `52` cột, chỉ-đọc, đã có)* mang sẵn bộ lọc của dòng đang xem. Lý do đầy đủ ở `BA-06 §4.4 ⓐ`.

#### ⓒ Khu vực **Giao dịch tương ứng** — hai vế, và vế phải **thiếu một trường**

**Vế LỆNH CHI** *(đang chọn)* — thêm **ngày** ＋ **CDT**:

| Trường | Nguồn | Có |
|---|---|--:|
| người nhận · số tiền · nội dung · ngân hàng · pháp nhân · số chứng từ · phiếu | `tho` ／ cột | ✅ |
| ⭐ **ngày** | `tho['Timestamp']` → ngày | ✅ |
| ⭐ **CDT** *(chủ dự toán)* | `fls_pm_line.cdt1` | ✅ **3.763/3.772** |

**Vế GIAO DỊCH** *(ứng viên)* — thêm **ngày** ＋ **nội dung**:

| Trường | Nguồn | Có |
|---|---|--:|
| ⭐ **ngày** | `fls_itl.doc_date` | ✅ **8.387/8.387** |
| nguồn *(số TK · ngân hàng · tiền tệ · pháp nhân)* | `source_sheet` | ✅ **8.387** |
| số chứng từ | `doc_no` | ✅ **8.383** |
| số tiền ＋ **chiều** | `ps_no` ／ `ps_co` | ✅ — `Nợ` = vào ＋ · `Có` = ra − *(`DT-I10`)* |
| bậc ứng viên | máy trả | `khớp số chứng từ` › `đúng số tiền` › `gần đúng` › `cùng đơn vị tiền` |
| ⛔⛔ **nội dung giao dịch** | `fls_itl.memo` | ⛔ **0 / 8.387** |

⛔⛔⛔ **Ô cuối là chỗ màn hình PHẢI nói thật.** Kế toán đòi đúng thứ đáng đòi nhất — nó cũng là **vế đầu của luật ghép nhánh nước ngoài** *(`DT-I13 ⓑ`)*. Nhưng sổ ⛔ không có. ⇒ Màn hiện **“cột này chưa được nạp”**, ⛔ **không** để một ô trống mà người đọc hiểu thành *"giao dịch này không có nội dung"*. Hai câu ấy khác nhau; lẫn là đúng bệnh `QĐ-ITL-110 ⓑ` đã xử một lần *(giữ cột, ghi **“⛔ không đọc — `QĐ-ITL-92`”**)*.

#### ⓓ ⛔ Ba điều khu vực này ⛔ CHƯA làm được

| # | Điều | Vì sao |
|:-:|---|---|
| 1 | Ghép theo **luật của kế toán** | Bốn bậc hiện nay là thứ tự **tôi suy từ dữ liệu**; luật thật ở `DT-I13` và nhánh nước ngoài ⛔ **không chạy được** |
| 2 | Lọc ứng viên theo **pháp nhân** | Hai bên gọi khác mã — nối được **82,7%**, `652` dòng **phải hỏi người** *(`GAP-LE-01`)* |
| 3 | Tìm theo **từ khoá nội dung** | ⛔ Không có nội dung để tìm *(`GAP-NAP-04`)* |

### §A8 · ⭐⭐⭐ MÀN PHẢN ỨNG THẾ NÀO — đọc từ bản dựng `21/09`, ⛔ không từ hợp đồng

> ⭐ **`BA-06 §4.5` nói màn *trông ra sao*. Mục này nói nó *làm gì khi người ta chạm vào*.** Và nó ⛔ **không** chép hợp đồng thiết kế — nó đọc **mã của bản dựng** `Artifacts/fls-gan-lenh-chi_10.html`, cùng cách `§1`–`§7` đọc `man_f0*.js`.

#### ⓐ Mỗi cử chỉ — máy làm gì, và **ca từ chối**

| Cử chỉ | Máy làm | ⛔ Ca TỪ CHỐI — và màn nói gì |
|---|---|---|
| Mở một lệnh *(`→` ／ `Enter` ／ bấm dòng)* | Bày thẻ lệnh ＋ danh sách ứng viên | ⭐⭐ **⛔ KHÔNG chọn sẵn ứng viên nào** — kể cả lệnh máy **đề xuất**. Đề xuất chỉ được **đánh dấu** *(viền đứt ＋ nền `warn`)* |
| Bấm `○` một ứng viên | Chọn; nút chính **bật** | Bấm lại ⇒ **bỏ chọn**, và ⭐ **xoá cả trạng thái xác nhận** đang chờ |
| `Gán` — ứng viên **đúng số tiền** | Ghi mối nối · ⭐ **tự nhảy sang lệnh chưa gán kế tiếp** | — |
| ⭐⭐ `Gán` — ứng viên **lệch tiền** | **Lần 1 ⛔ KHÔNG ghi**: nút đổi chữ *«Xác nhận gán lệch … ?»*, hiện thêm nút `Huỷ`. **Lần 2** mới ghi | ⭐⭐⭐ **`Enter` BỊ KHOÁ ở ca này** — câu gợi ý nói thẳng *«số tiền lệch — bấm hai lần để xác nhận, Enter ⛔ không gán»* |
| `Gán` khi **chưa chọn** ứng viên | ⛔ Không gì | Nút ở trạng thái **tắt** ⇒ ⛔ không có cú bấm nào để hiểu nhầm |
| Lệnh **đã gán** | Nút chính đổi chữ ⇒ *«Đổi sang giao dịch đã chọn»*; khối xanh hiện mối nối **hiện tại** ＋ nút **Bỏ gán** | ⭐ Dòng đang gán **vẫn nằm trong bảng ứng viên** — đổi mapping ⛔ không phải bỏ rồi gán lại |
| Máy ⛔ **không tìm được** ứng viên nào | ⭐ Bật sẵn chế độ **Toàn sổ** | ⛔ Màn **⛔ không bao giờ là ngõ cụt**; dải `crit` nói vì sao |
| Diễn giải bị cắt | Hiện liên kết `đủ ↓` | ⭐ Chỉ hiện khi **THẬT SỰ** bị cắt *(so `scrollHeight` **sau khi dàn trang**)*, ⛔ không đoán theo số ký tự |
| `/` | Nhảy vào ô tìm giao dịch | `Esc` thoát ô tìm; `Esc` lần nữa đóng vùng ghép |

#### ⓑ ⭐⭐ Chế độ **Toàn sổ** — đổi NGUỒN danh sách, ⛔ không đổi bộ lọc

Chip `Toàn sổ` đổi nguồn từ *ứng viên máy đề xuất* sang **toàn bộ giao dịch trong sổ**, và **bậc được TÍNH LẠI theo lệnh đang mở** *(khớp số CT ⇒ ①, đúng số tiền ⇒ ②, ⭐ khác tiền tệ lệnh ⇒ `≠` *(`WO-032`, mã `9c100ac`)*, còn lại ⇒ ④)*.

⚠ *(v1.7, `TL-033`)* Hai chỗ màn **hôm nay** nói sai/thiếu, đã có việc: ⓐ khối *"✓ Đang gán"* ⛔ bao giờ hiện `①` — cửa `lenh-da-gan` ⛔ tính vế mã *(sổ thật 02/10: **0 / 2.219** lệnh đã gán, dù **2.262 / 2.262** mối nối khớp số chứng từ; chip đang nói `②` 2.121 · `④` 98)*; ⓑ nghĩa năm ký hiệu `①②③④≠` chỉ có trong `title` *(chú giải `BA-06 §4.5 ⓒ ①` ⛔ dựng)*. Cả hai ⇒ `WO-032` vòng 2.

⛔⛔ **Đây ⛔ không phải một bộ lọc nới rộng — nó là một câu hỏi khác.** Danh sách ứng viên trả lời *«máy nghĩ những dòng nào hợp»*; Toàn sổ trả lời *«sổ có những dòng nào»*. Gộp hai câu vào một điều khiển thì khi màn rỗng, người dùng ⛔ không phân biệt được **«máy ⛔ không tìm ra»** với **«sổ ⛔ không có»** — đúng cặp `INV-I16` bắt phải phân biệt.

#### ⓒ ⛔ Ba điều bản dựng **CHƯA** làm — và chúng là việc của bước cài

| ⛔ Chưa có | Hệ quả nếu quên |
|---|---|
| Bấm `Gán` ⛔ **không ghi gì** *(chưa nối kho)* | Bản dựng là **spec hành vi**, ⛔ không phải sản phẩm dùng thử được |
| ⭐⭐ **Bỏ gán phải là THÊM một dòng**, ⛔ không phải xoá | `INV-I08` — sổ là sách **chỉ-thêm**. Một `DELETE` ở đây xoá mất bằng chứng *ai từng nối gì* |
| *«Sang màn Sổ»* phải mở **`SCR-F02` đã lọc sẵn** đúng dòng đang xem | Nếu mở màn Sổ **trắng**, kế toán phải tự tìm lại ⇒ nhu cầu *yên tâm về data* ⛔ không được phục vụ *(`QĐ-ITL-144 ⓐ`)* |

⚠ **Và ⛔ cố ý ⛔ không có:** chọn nhiều dòng · gán hàng loạt · ghi chú trên mối nối. Nhịp là **từng giao dịch một** *(`QĐ-ITL-144 ⓵`)*; ba thứ ấy tối ưu cho **đợt dọn tồn**, ⛔ không cho nhịp hằng ngày.

---

> ⚰⚰ **BIA — `CR#12`, `2026-09-18`.** Từ đây trở xuống, tệp này tả **màn hình TRƯỚC `CR#12`**.
> Nó ⛔ **không còn là đặc tả sống**, nhưng **giữ nguyên chữ**: nó là bản ghi trung thực nhất
> về thứ owner gọi là *overdone*, và ⛔ không có nó thì `BA-14` ⛔ không chứng minh được gì.
>
> ⭐ Hai chỗ tệp này **nói đúng và `CR#12` giữ lại**: chiều hỏi từ phía **LỆNH CHI** *(`US-052`)*,
> và luật ⛔ **không gộp** `47` tự chứng với `203` lệch tiền vào một nút *(`US-054`, `INV-I16`)*.
>
> ⛔ Chỗ tệp này **⛔ không thấy**: nó thuyết minh **từng nút một** rất kỹ — và đó chính là
> hình dạng của lỗi. Cột *"nếu bỏ đi thì sao"* hỏi đúng câu, nhưng hỏi **cho từng thứ riêng lẻ**,
> nên mọi thứ đều **đáng giữ riêng lẻ** trong khi tổng thì ⛔ không ai chịu nổi.
> ⇒ `UI-F7` *(ngân sách trường)* là câu trả lời: hỏi **tổng** trước, ⛔ không hỏi **từng cái**.

### §A10 · ⭐⭐⭐ BỐN cử chỉ **MỚI** sau khi owner nhìn màn thật *(2026-09-23)*

| Cử chỉ | Ở đâu | Nó làm gì | ⛔ Bẫy đã tránh |
|---|---|---|---|
| **Kéo** mép giữa rail ＋ bàn làm việc | `.keo` *(`role=separator`)* | đổi bề rộng cột lệnh chi | ⛔ Bề rộng sống trong **`ST.rail_w`**, ⛔ không trong DOM — `ve()` dựng lại cả cây, đặt thẳng vào phần tử thì kéo xong bấm một cái là **nhảy về cũ** và người ta tưởng **tay kéo hỏng**. ⭐ Chặn `260`…`720px`: **hai đầu đều là *"màn hỏng"*** |
| `←` `→` khi tay kéo có **focus** | `.keo` | đổi bề rộng `24px` mỗi nhịp | ⛔ Một cử chỉ chỉ dùng được bằng chuột là một cử chỉ **⛔ không tồn tại** với người dùng bàn phím *(`NFR-I24`)* |
| `Esc` khi *«Xem đủ trường»* đang mở | `document` | đóng **lớp phủ**, ⛔ **không** đóng lệnh | ⛔⛔ `Esc` phải **bóc từng lớp một**: đóng thẳng cả lệnh thì người vừa mở khối để đối chiếu **mất luôn dòng đang làm**, ⛔ không cách nào quay lại ngoài tìm lại trong `738` dòng |
| **`✕`** trên lớp phủ | `.more .dong` | đóng lớp phủ | ⭐ `Esc` là đường ra của người **biết** nó tồn tại ⇒ phải có một **nút nhìn thấy được** |
| **`bỏ gán`** ngay trên khối `C4` | `.mblock .mh button` | gỡ mối nối | ⭐ Một **đường ra tại chỗ** — ⛔ không bắt người ta đi tìm nó ở thanh dưới cùng. ⚠ Chùm `>1` vẫn **hỏi trước** và **nêu tên từng dòng** *(`QĐ-ITL-148 ⓔ`)* |

⭐⭐ **Và một cử chỉ CŨ đổi hành vi:** bấm chọn một giao dịch nay **⛔ không** làm danh sách nhảy về đầu. ⛔⛔ Lỗi ấy do **chính phép sửa cùng ngày** đẻ ra *(cho `.cands` cuộn riêng ⇒ `ve()` dựng lại cây ⇒ `scrollTop` về `0`)*; trước đó nó ⛔ không tồn tại vì cả trang cuộn và trình duyệt tự giữ vị trí.

⛔ Giữ chỗ cuộn **⛔ không phải luôn luôn đúng**: đổi sang một **lệnh khác** thì danh sách ứng viên là một danh sách **khác hẳn** ⇒ luật là **giữ chỗ khi vẽ lại cùng một cảnh, về đầu khi đổi cảnh**.

---

## §1 · `SCR-F01` lằn **LỆNH CHI** — màn MẶC ĐỊNH

> **Câu màn này hỏi:** *"Lệnh chi nào **chưa tìm được tiền**?"*
> **⛔ Không phải:** *"Dòng tiền nào chưa có lệnh?"* — đó là lằn kia.

⭐ Vì sao chiều hỏi này: đo cùng một kho, hỏi phía **TIỀN** cần xem **`799`** dòng để phủ `90%` tiền; hỏi phía **LỆNH** chỉ cần **`69`**. Chênh **`11,6` lần**. `QĐ-ITL-122` · `US-KT-052`.

### ⓪ Băng *"Việc của bạn hôm nay"*

⛔⛔ **Băng này ra đời vì một lời chê.** Owner mở màn và nói *"tôi ⛔ không hiểu ý nghĩa của những bảng thông tin này"*. Ba bảng đầu màn khi ấy là thứ **tôi** dựng để **tự chứng minh phép chia đúng** — việc của **tôi**, ⛔ không phải của kế toán, mà chiếm hai phần ba màn hình và **đứng TRÊN** chỗ có việc.

| Hiển thị | Nghĩa | `US` | Nếu bỏ đi |
|---|---|:--:|---|
| ✅ `250 dòng` · **máy ghép được — bạn chỉ DUYỆT** | Số chứng từ khớp **đúng một** dòng tiền trong sổ. ⛔ Không cần suy nghĩ | `053` | Kế toán ngồi tra lại thứ máy **đã biết** |
| ✅ `535 dòng` · **CẦN BẠN tra bằng tiền + ngày** | ⛔ Chưa có số chứng từ ⇒ **việc thật** | `039` `053` | Việc thật lẫn vào việc giả |
| ✅ `768 dòng` · **⛔ KHÔNG làm được** | Có số chứng từ nhưng ⛔ **không dòng tiền nào** mang số ấy. Ngồi tìm là **phí công tuyệt đối** | `053` | Kế toán tìm **mãi mãi** — đúng điều màn cũ bắt họ làm |
| ✅ ⚠ `203 dòng` khớp mã **lệch tiền** | Trả nhiều đợt, hay một giao dịch gánh nhiều lệnh ⇒ ⛔ **không** ghép lô được | `054` | Chúng **biến mất giữa hai nhóm**: ⛔ không phải "bấm duyệt", cũng ⛔ không phải "⛔ không làm được" |
| ⛔ chân băng: *"cột lý do đã gõ **N** lần trong 4 tuần"* | ⭐ **Thước của COO-CFO**: `4` tuần ⛔ không ai gõ = **cổng đã chết** | `045` | ⛔ **Không ai biết hệ kiểm soát còn sống hay đã chết** |

★ **`250` = `47` tự chứng + `203` lệch tiền.** Hai nhóm ấy ⛔ **KHÔNG được gộp vào một nút**: nhóm `47` máy ghép được và người chỉ **duyệt**; nhóm `203` là chỗ máy **phải hỏi** *"lệnh này ăn bao nhiêu của giao dịch kia"* — gộp lại là để **máy quyết thay người** *(`INV-I16`)*.

⭐ *(v1.8, `TL-038` — `BG-039` yếu #1; chữ nguyên văn ở `BA-06` **v4.17** `§4.5 ⓤ`)* **Dòng 2 và dòng ⚠ của băng đã nói sai sau `WO-037`.** Rổ *cần người* nay gồm **hai** loại lệnh: ⛔ số chứng từ **532** ＋ số chứng từ khớp một dòng tiền **tiền tệ khác** **84** *(sổ thật 02/10, `nguoi` **616**)* — câu *"Chưa có số chứng từ"* sai cho **84**. Dòng *"khớp mã **lệch tiền**"* *(`may − tu_chung` = **120**)* đúng cho **78**: **39** lệnh có **một** dòng cùng tệ **khớp đúng tiền** mà cửa ghi vẫn ⛔ nhận theo lô *(cổng nào — chưa đo)* ＋ **3** lệnh nhiều dòng có dòng khớp tiền. Bảng trên giữ số **18/09** *(biên bản)*; nghĩa mới:

| Hiển thị *(v1.8)* | Nghĩa | Nếu bỏ đi |
|---|---|---|
| **CẦN BẠN tra — máy chưa đề xuất được dòng tiền** · `hint` hai câu: `a` dòng chưa có số chứng từ *(tra bằng tiền + ngày)* · `b` dòng khớp mã ở tiền tệ khác *(cửa ghi chưa ghép được hai tiền tệ)* | `a`, `b` do **cửa** đếm *(`nguoi_khac_tien_te`)*, ⛔ màn đếm | Kế toán bấm *Bắt đầu tra* cho **84** lệnh tưởng là ⛔ có số chứng từ, tra theo tiền + ngày một lệnh mà câu trả lời đã nằm ở tiền tệ khác |
| Ghi chú `c` dòng *khớp số chứng từ cùng tiền tệ nhưng cửa ghi chưa nhận theo lô* | ⛔ còn hứa *"lệch tiền"* cho cả nhóm | Người mở **39** lệnh tìm chỗ lệch tiền mà ⛔ có |

⭐ *(v1.9, `KQ-041 F-1` + `F-3`; chữ nguyên văn ở `BA-06` **v4.18** `§4.5 ⓤ` + `ⓥ`)* **Ba chỗ nữa của `F01L` hứa *"lệch tiền"* / *"chỉ DUYỆT"* cho cả rổ `may`, và danh sách `②b` đếm sai khi đổi chip lúc đang tải.** Sổ thật *(`KQ-041`)*: rổ `may` **184** = tự chứng **64** ＋ chưa nhận theo lô **120** *(lệch tiền 78 · nhiều dòng có dòng khớp 3 · **một** dòng khớp **đúng tiền** 39 = một dòng tiền mang mã nhiều dòng lệnh 25 ＋ dòng lệnh cùng chùm chưa duyệt 14)*.

| Hiển thị *(v1.9)* | Nghĩa | Nếu bỏ đi |
|---|---|---|
| Hàng `may` bảng rổ: *khớp **ít nhất một** dòng tiền cùng tiền tệ — máy đề xuất được; tự chứng duyệt theo lô, còn lại mở từng dòng* | `184` lệnh có đề xuất **ghi được**; chỉ `64` duyệt lô | Người tưởng **184** dòng *"chỉ duyệt"* — bấm `Duyệt` ở **120** dòng cửa ghi ⛔ nhận lô |
| Ghi chú băng + `note ok`: một câu nêu **bốn** lý do cửa ghi giữ | câu đúng cho **120 / 120** *(câu cũ *"lệch tiền"* đúng 78)* | Người mở **39** lệnh tìm chỗ lệch tiền mà ⛔ có |
| Nhãn lọc `chỉ CHƯA NHẬN THEO LÔ` | tên **tập**, ⛔ tên **một** lý do | Nhãn *"chỉ LỆCH TIỀN"* đặt trên 42 dòng ⛔ lệch |
| Chip `②b` in số của **lượt tải mới nhất** | đổi chip lúc đang tải ⛔ cộng hai rổ | Chip `Đã gán` in **2.955** thay **2.219**; bấm lại chip ⇒ **1.472** thay **736** |

Lý do **từng hàng** của 120 lệnh ⛔ có ⇒ `GAP-SCR-34`.

### ⓪b Nút trên băng

| Nút | Làm gì | `US` | Ghi vào đâu |
|---|---|:--:|---|
| ✅ **Duyệt cả `47` dòng** | Mở khối duyệt lô — **dùng lại** khối của lằn TIỀN, ⛔ không dựng đường ghi thứ hai | `054` | `POST /queue/match-lo` ⇒ `fls_pm_link` + `fls_moi_noi` |
| ✅ **Bắt đầu tra** | Lọc lưới về rổ *cần người* | `039` | ⛔ không ghi gì |
| ✅ **Xem vì sao** | Lọc lưới về rổ *⛔ không ai trả lời được*, mỗi dòng mang **câu vì sao** | `053` | ⛔ không ghi gì |

⛔⛔ Con số `47` là **cửa GHI nói thế** *(`ds_tu_chung`)*, ⛔ không phải phép đo của màn. Bản trước tôi tự tính ra **`90`** trong khi cửa ghi chỉ nhận **`47`** ⇒ nút *"Duyệt cả 90"* sẽ bị **từ chối CẢ LÔ**. ***Một con số hứa nhiều hơn cái bấm được là một con số nói dối.***

### ① Khối *"Số liệu kiểm chứng"* — gấp lại, đóng sẵn

| Bảng | Ba cột | Nghĩa | `US` |
|---|---|---|:--:|
| ✅ Ba rổ | `Rổ` · `Dòng` · `Nghĩa là gì` | Màn **tự kiểm**: `250+535+768` có `= 1.553` ⛔ không. Một bảng phân loại ⛔ không cộng về tổng là bảng **⛔ không kiểm được** | `053` |
| ✅ Theo tiền tệ | `Tiền tệ` · `Dòng chờ` · `Phiếu` · `Tiền` · `Đã duyệt` · `⛔ Chưa duyệt` · `Xem mấy dòng là phủ 90% tiền` | ⛔ **⛔ KHÔNG có dòng "tổng"** — cộng hai đơn vị tiền ra một con số là **vô nghĩa**, và nó từng đẻ ra *"310 dòng phủ 90%"* trong khi thật là **799** | `039` |

⭐ Ô *"phủ 90%"* trả **`null`** khi `Σ` tiền `= 0` ⇒ màn vẽ **"⛔ không đo được"**, ⛔ **không** vẽ `0`. Vẽ `0` nói *"xem **0** dòng là đủ"* — một câu **sai**, và sai theo hướng **nguy hiểm**: kế toán bỏ qua cả đơn vị tiền ấy.

### ② Lưới dòng lệnh

| Cột | Nghĩa | `US` | Ghi chú thiết kế |
|---|---|:--:|---|
| ✅ `# · phủ` | Hạng trong danh sách + *"đọc tới đây là phủ bao nhiêu % tiền"* | `039` | ⭐ **Ghim trái.** Gộp hai thứ vì cả hai đều là **vị trí trong danh sách** — `Luỹ kế %` ⛔ **không phải** một cột tiền |
| ✅ `Số chứng từ` | `Reference number` — **một tên duy nhất** trên mọi màn | `013` | ⭐ **Ghim trái.** Trước `G1` trường này có **NĂM** tên, trong đó `F01` và `F02` gọi **khác nhau** |
| ✅ `Phiếu` + huy hiệu `còn chờ/tổng` | Phiếu này có mấy dòng lệnh, mấy dòng còn chờ | `055` | ⭐ **`1.088/1.553` = `70,1%`** dòng chờ nằm trong phiếu nhiều dòng; phiếu to nhất **`44`** dòng. Phiếu **một dòng** ⛔ **không** đeo huy hiệu — dấu hiệu có mặt trên **mọi** dòng thì ⛔ không còn là dấu hiệu |
| ✅ `Tiền lệnh` | Số tiền của lệnh | `039` | Xếp **giảm dần TRONG TỪNG** đơn vị tiền *(`QĐ-ITL-58`)* |
| ✅ `Trạng thái` | `Approve` / trạng thái nguồn | `039` | ⭐ Rỗng vẽ **"⛔ RỖNG = không biết"**, ⛔ **không** vẽ *"đã duyệt"* |
| ✅ `HĐ` · `CĐT` | Mã hợp đồng · chủ dự toán — **chỉ MÃ** `4` ký tự | `055` | ⭐ Rút gọn hợp lệ vì **song ánh**: `hd` **31 mã ↔ 31 tên**, `cdt1` **9 ↔ 9**. Tên đầy đủ ở `title` ⇒ ⛔ **không mất thông tin**. `9` dòng ⛔ không có dấu `\|` giữ **nguyên văn** |
| ✅ `2` hay `28` cột GGSheet | *Nội dung ghi ở bank* · *Người nhận* … | `055` | ⭐ **`535`** dòng ⛔ không có số chứng từ **chỉ tra được** bằng hai cột ấy. ⛔ Cột `Email Address` **⛔ không bao giờ** vào kho |
| ✅ `Ai trả lời được` | Rổ + **câu vì sao** ngay trên dòng | `053` | Rổ *"⛔ không bao giờ"* mà ⛔ không nói vì sao thì kế toán tìm **mãi mãi** |
| ⛔ `Tuổi việc` | *"treo 47 ngày"* | `039` | ⛔ **CHƯA CÓ.** `US-KT-039` đòi *"in rõ tuổi việc"* |
| ✅ `Việc` | Nút hành động | — | ⭐ **Ghim phải.** Với 28 cột, cuộn ngang đẩy nút ra khỏi tầm nhìn |

### ②b Nút trên mỗi dòng

| Nút | Khi nào hiện | Nghĩa | `US` |
|---|---|---|:--:|
| ✅ **Duyệt** | rổ `máy` + **tự chứng** | Khớp cả mã · tiền · đơn vị ⇒ chỉ xác nhận | `054` |
| ✅ **Mở để chia** | rổ `máy` + **lệch tiền** | Phải mở từng dòng: *"lệnh này ăn bao nhiêu của giao dịch kia"* | `054` |
| ✅ **Tra tiền** | rổ `người` | Việc thật — tra bằng tiền + ngày | `039` |
| ✅ **Xem vì sao** | rổ `không` | Mở ra để **thấy ⛔ không có ứng viên nào**, ⛔ không mời đi tìm | `053` |
| ⛔ **Lý do** | — | ⛔ **CHƯA CÓ** ở lằn này | `039` `045` |
| ⛔ **Hoãn** | — | ⛔ **CHƯA CÓ** ở lằn này | `040` |
| ⛔ **Bỏ ghép** | — | ⛔ **CHƯA CÓ** ở lằn này | `046` `056` |
| ⛔ **Xong · Mở lại** | — | ⛔ **CHƯA CÓ** ở lằn này | `047` |

⛔⛔⛔ **Bốn nút cuối thiếu ⛔ KHÔNG phải vì ai quên vẽ.** `fls_queue_event` và `fls_da_xong` **chỉ treo được vào `itl_id`** — dòng **TIỀN**. Một dòng **LỆNH** ⛔ **không có chỗ nào** để mang lý do, hạn hoãn, hay dấu *"xong"*. ⇒ ⛔ Không có gì để ghi vào. Ba đường xử ở `Artifacts/Ban-ve-TOBE-Man-Ghep-PM.html §2` — **chờ owner quyết**.

### ③ Nút khác trên màn

| Nút | Nghĩa | `US` |
|---|---|:--:|
| ✅ **Hiện ĐỦ các cột của GGSheet** ↔ **← Chỉ 2 cột nhận diện** | Bật `2` → `28` cột. ⛔ Mặc định **⛔ không** đổ 28 cột: lưới 28 cột ⛔ không đọc được. **Người** chọn, ⛔ không phải máy chọn hộ | `055` |
| ✅ **Xem thêm** | Trang tiếp *(`50` dòng/trang, con trỏ `tiền tệ:hạng`)* | `039` |
| ✅ **← Quay lại toàn bộ** | Rời chế độ xem một rổ | `053` |

### ④ Ngăn kéo **Tìm tiền** — nơi cú ghép xảy ra

| Phần | Nghĩa | `US` |
|---|---|:--:|
| ✅ Dòng lệnh **ghim** đầu ngăn kéo | Tiền · đơn vị · số chứng từ · phiếu — để ⛔ không quyết trong trí nhớ | `013` |
| ✅ **Bảng PM đủ `28` cột** — **hai tầng** | `n/28` cột có dữ liệu. ⭐ **Sáu cột ƯU TIÊN** lên trước *(`Nội dung ghi ở bank` · `Tên tài khoản` · `Số tài khoản` · `Ngân hàng` · `Pháp nhân thanh toán` · `Loại giao dịch`)*, rồi một vạch **«— các cột còn lại —»**, rồi phần còn lại **theo đúng thứ tự tờ giấy**. ⛔ Vạch ấy ⛔ không phải trang trí: nó nói *"từ đây trở xuống máy ⛔ không sắp theo mức quan trọng nữa"* | `055` |
| ✅ **Cả phiếu** — các dòng khác cùng `PMSlip` | ⚠ `526` phiếu mang `2`–`36` số chứng từ khác nhau ⇒ **nhìn một dòng lẻ mà quyết là nhìn một mảnh của tờ giấy** | `055` |
| ✅ Bảng ứng viên: `Dòng tiền` · `Độ khớp` · `Ngày` · `Số chứng từ` · `Tiền` · `Lệch` · `Diễn giải` | Bốn bậc khớp: `mã khớp` · `tiền khớp` · `gần tiền` · `cùng tiền tệ` — **cùng bộ từ** với lằn TIỀN. ⭐ *(v1.6, `BA-06` v4.14 §5b ⓕ/ⓙ)* `Tiền` in **kèm mã** *(ứng viên `mã khớp` có thể khác tiền tệ lệnh — **165 / 5.360**)*; `Lệch` có số ở **mọi** bậc khi cùng tiền tệ, khác tiền tệ in chữ **`khác tiền tệ`**, `—` chỉ khi thiếu số | `013` |
| ✅ **dung sai Σ** | Cùng phép dung sai mà **cửa GHI** dùng — ⛔ không phải một con số của màn | `013` |
| ✅ **Σ hai con số**, tính lại mỗi lần chọn | `tiền lệnh ↔ tiền bank · lệch` ⇒ *"trong dung sai"* hay *"⛔ VƯỢT — cửa ghi sẽ TỪ CHỐI"* · ⭐ *(v1.6)* khác tiền tệ ⇒ *"khác tiền tệ — cửa ghi sẽ TỪ CHỐI"*, ⛔ một con số lệnh trừ hai đơn vị | `013` |
| ✅ Ô **vì sao ghép cặp này** — ~~**BẮT BUỘC**~~ ⭐ *(v1.6)* **tuỳ ý** | Vào nhật ký. ⛔ *(`QĐ-ITL-149 ⓑ`, owner 01/10: *"bỏ yêu cầu lý do cho cú Ghép"*)* — bỏ trống ⇒ cửa điền `(may dien) …` *(`BA-07 §4h ⓼`)*. Mã hôm nay *(`man_f01_lenh.js:650` · `man_f01.js:345`)* còn chặn nút `Ghép` khi ô trống ⇒ `WO-032` | `030` |
| ✅ Khai *"Danh sách bị **CẮT**"* | ⭐ Cắt mà im là **mặc định im lặng** *(`INV-I16`)*: người gõ tưởng danh sách đầy đủ rồi kết luận *"⛔ không có dòng tiền nào khớp"* | `039` |
| ✅ Nút **Ghép** / **Thôi** | `POST /queue/{itl_id}/match` — ⛔ **đúng cửa ghi cũ**, ⛔ không có đường thứ hai | `013` |

---

### ⚠⚠ ĐÍNH CHÍNH `14/09` — một con số tôi đưa ngày `11/09` **ĐÚNG** mà **vẫn gây hiểu sai**

Tôi nói: *"hai cột **Nội dung ghi ở bank** và **Tên tài khoản** điền **100%** ⇒ đó là hai thứ giúp nhận ra khoản tiền, và **535** dòng ⛔ không có số chứng từ **chỉ tra được** bằng chúng"*. Tỷ lệ điền ấy **đúng**. ⛔ Nhưng ***"có điền" ⛔ KHÔNG phải "có nghĩa"***.

Đo lại trên **đủ cả `535` dòng** của rổ *cần người tra*:

| Cột | Điền | Thật sự dùng được | Vì sao |
|---|:--:|:--:|---|
| **Nội dung ghi ở bank** | `100%` | ⭐ **`100%`** | Luôn là **nội dung thật** người lập lệnh gõ vào bank |
| **Tên tài khoản** | `99,8%` | ⛔ **`52,7%`** *(282/535)* | ⛔ **`252` dòng (`47,1%`)** giữ một **CHỖ ĐIỀN**, ⛔ không phải tên ai: `Thanh toán thẻ` · `Tiền mặt` · `STK CBNV` · `Ghi chú` · `Danh sách đính kèm` |

⇒ ⭐ **Gần một nửa số dòng cần tra thì cột ấy ⛔ không nói được người nhận là ai.**

★ Ví dụ owner gửi ảnh `14/09`: `PM01698-1` có **ba** ô *Ngân hàng* · *Số tài khoản* · *Tên tài khoản* cùng mang **`Thanh toán thẻ`** — **`294` dòng (`7,8%`)** của cả ảnh chụp như vậy. ⛔ Đó ⛔ **không** phải lỗi đọc cột: hàng thô lưu **đúng** cái tờ giấy ghi.

⚠ Và nó ⛔ **không** lật quyết định giữ cột — cột vẫn cứu được **`282`** dòng, và nó vẫn **có thể mang tên người** *(giá trị hay gặp thứ hai là một tên người thật, **`128`** dòng ⇒ mối lo riêng tư là có thật)*. Nó chỉ đổi **cái nên trông đợi**: ⛔ **không phải một lời giải cho cả `535`**.

---

## §2 · `SCR-F01` lằn **TIỀN** — lằn cũ, ⛔ KHÔNG bị xoá

> **Câu màn này hỏi:** *"Dòng tiền nào chưa ghép được lệnh?"*

⛔ Nó ⛔ **không** bị bỏ, vì nó là đường **duy nhất** để làm **bốn việc** `QĐ-ITL-71`/`72` đã chốt — và bốn việc ấy ⛔ **chưa có** ở lằn lệnh chi.

| Cột | Nghĩa | `US` |
|---|---|:--:|
| ✅ `Hạng` · `% luỹ kế` | Vị trí trong danh sách xếp theo tiền | `039` |
| ✅ `Mã dòng` | `itl_id` — **⛔ không bao giờ đổi** *(`INV-I04a`)* | `023` |
| ✅ `Số chứng từ` | `doc_no` — **cùng một tên** với lằn kia | `013` |
| ✅ `Diễn giải` | `memo` — ⚠ có thể mang **tên người** | — |
| ✅ `Tiền` · `Pháp nhân` | | `032` |
| ✅ `Việc` | Chỗ năm hành động nằm | |

| Nút | Nghĩa | `US` | Nếu bỏ đi |
|---|---|:--:|---|
| ✅ **Lý do** → *Ghi lý do* | Gõ vì sao dòng này còn treo. ⭐ **Đây là ô `US-045` đếm** | `039` `045` | Mất **thước đo duy nhất** của cả hệ kiểm soát |
| ✅ **Hoãn** | **Bắt buộc có hạn** — hoãn vô hạn là **bỏ qua**, ⛔ không phải hoãn. Lần thứ `3` **tự đổi màu**, ⛔ **không leo cấp** *(⛔ không có ai ở trên)* | `040` | Việc treo ⛔ không ai biết đang chờ gì |
| ✅ **Ghép** / **Ghép cả lô** | Nối dòng tiền với dòng lệnh | `013` `054` | — |
| ✅ **Bỏ ghép** → *Bỏ cả chùm* | ⭐ Bỏ **CẢ CHÙM**, ⛔ không bỏ lẻ — bỏ lẻ làm `Σ ≠ tiền bank`, tức **tạo ra đúng trạng thái sai mà cổng dựng ra để bắt**. Sổ **THÊM** dòng, ⛔ **không `DELETE`** *(`INV-I08`)*. Máy **đảo** bút toán nó tự suy ra, ⛔ **KHÔNG** đảo ô **người** gõ tay — và **khai ra** thứ nó ⛔ không đảo | `046` | Một dòng ghép sai thành **dòng chết cứng** |
| ✅ **Xong** | Dòng **rời hàng chờ ngay**, `fls_itl` ⛔ **không đổi một ô nào** *("xong chưa" là một **phép tính**)*. ⛔ **KHÔNG đòi lý do** — một ô lý do **bắt buộc** thì nó thành ô **rác**. ⭐ Kỳ đã chốt **VẪN bấm được**: kỳ chốt thì kế toán ⛔ không sửa được gì, nếu cũng ⛔ không đánh dấu xong được thì hàng chờ **tự biến thành rác** | `047` | Hàng chờ thành danh sách **máy tự quản**, ⛔ không phải việc còn lại của người |
| ✅ **Mở lại** | **Đòi lý do** — vì nó **lật kết luận của người khác** | `047` | ⛔ Không sửa được một cú bấm nhầm |
| ✅ Bảng *"Dòng CÓ mã mà ⛔ không tự chứng"* | `Số dòng` · **`Vì sao — và sửa ở đâu`** | `053` | Kế toán ⛔ không biết đi sửa ở đâu |
| ✅ **Đã hiểu** | ⭐⭐ Nút **xác nhận đã đọc** của hai hộp thoại *sau khi máy làm xong một việc* — và **nội dung** hai hộp ấy mới là thứ đáng kể *(nút chỉ để đóng)*. Xem ngay dưới | `047` `054` | Hai câu dưới đây **⛔ không ai nói** ⇒ kế toán kết luận sai rằng máy hỏng |

⭐⭐ **Hai câu mà nút *"Đã hiểu"* đóng lại — chúng là chỗ máy TỰ KHAI một điều dễ bị đọc nhầm thành lỗi:**

| Sau khi | Máy nói gì | Vì sao phải nói |
|---|---|---|
| **Ghép cả lô** *(`US-054`)* | *"Những dòng này rời hàng chờ **⛔ không phải** vì ai bấm «xong» — nhãn `work_status` bị **đóng băng lúc nạp** (`INV-I08`) nên nó **vẫn nói `UNMAPPED`**."* | ⛔ Kế toán nhìn thấy `UNMAPPED` sau khi vừa ghép thành công sẽ tưởng **cú ghép hỏng**. Sự thật: nhãn trả lời câu *phân loại*, mối nối trả lời câu *đã nối lệnh chi* — **hai câu hỏi khác nhau** |
| **Xong** *(`US-047`)* | ⓐ *"đã bấm xong từ trước bởi **X** lúc **Y**; bấm lại ⛔ không tạo thêm sự kiện"* · ⓑ *"**Xong mà còn thiếu:** …  ⛔ Máy ⛔ không chặn — **nhưng nó đếm riêng** những dòng như thế"* · ⓒ *"**Kỳ đã chốt** — vẫn bấm xong được, và đó là **cố ý**"* | ⭐ Cả ba đều là chỗ hành vi **⛔ không như trực giác**. ⓑ đặc biệt: ⛔ không chặn **nhưng ⛔ không im lặng**, để nút *Xong* ⛔ **không thành đường tắt làm sạch hàng chờ** |

---

## §3 · `SCR-F02` Sổ ITL

> **Câu màn này hỏi:** *"Dòng này đang mang giá trị gì, **từ đâu ra**, và tôi sửa được gì?"*

| Khối | Cột | Nghĩa | `US` |
|---|---|---|:--:|
| ✅ Mối nối | `lệnh chi` · `tiền` · `hình` · `lần` | `hình` = **hình dạng ghép** `A`–`F`: `A`=1×1 · `B`=1×N · `C`=N×1 · `D`=N×N **máy từ chối** *(nhiều cách chia đều đúng như nhau)* · `E`=**khác đơn vị tiền** · `F`=lệch tổng quá dung sai | `046` |
| ✅ `7` ô sửa | `#` · `ô` · `giá trị` · `ai` | ⭐ Cột **`ai`** là cột đắt nhất: `nguồn` / `máy gợi ý` / `sửa tay` / `UNMAPPED`. ⛔ Một giá trị ⛔ không nói mình **từ đâu ra** thì ⛔ không ai kiểm được nó | `025` `026` |
| ✅ Nhật ký | `lúc` · `ô` · `từ` · `thành` · `ai` · `nguồn` · `vì sao` | **`7` trường `AUD-1`**, chỉ-THÊM. ⭐ Giữ lại ⛔ **không phải** vì có người soi — **⛔ không có ai soi và sẽ ⛔ không có**. Giữ vì **rủi ro thật là một người rời đi**: `2` người đang giữ `6.843` quyết định trong đầu | `030` |

| Nút | Nghĩa | `US` |
|---|---|:--:|
| ✅ **chỉ UNMAPPED** | Lọc về dòng **chưa biết chủ** — `UNMAPPED` là trạng thái **tường minh**, ⛔ không phải ô trống | `026` |
| ✅ **Ghi đè** / **Lấy giá trị của họ** / **Giữ số của tôi, để tôi hỏi lại họ** | ⭐⭐ Ba nút của cú **`409`** khi bạn gõ **khác nguồn**. `QĐ-ITL-29`: **nguồn vẫn thắng** *(để lỗi được sửa **tận gốc**, chỉ một lần)* — **⛔ nhưng ⛔ không được im lặng**. Ghi đè **bắt buộc lý do**, vào nhật ký. Số lần *"nguồn ≠ người gõ"* là **thước chất lượng của PM** | `025` |
| ✅ **Đảo** / **Để nguyên, không ghi** | Đảo một bút toán. ⛔ **⛔ KHÔNG có thao tác XOÁ** trong TO-BE *(`INV-I08`)* — `UC-KT-21` hỏi *"xoá thì ghi nhật ký thế nào"*, và câu đúng của TO-BE là ***"đảo thế nào"***, với **người + lý do bắt buộc** | `033` |
| ✅ **Thử lại** / **Thử lại ngay** | Gọi lại cửa khi lỗi mạng — ⛔ không phải một thao tác nghiệp vụ | — |
| ✅ **Xem thêm** / **Đóng** | Phân trang · đóng ngăn kéo | — |

---

## §4 · `SCR-F03` Cổng hôm nay — **⛔ KHÔNG có nút nào**

> **Câu màn này hỏi:** *"Số trên màn hôm nay **tin được đến đâu**?"*

⛔ Màn này **chỉ đọc**, và đó là **có chủ ý**: nó là chỗ **máy báo cáo về chính nó**.

| Hiển thị | Nghĩa | `US` |
|---|---|:--:|
| ✅ `✓ ĐẠT` · `✗ KHÔNG ĐẠT` · **`— ⛔ KHÔNG ĐO ĐƯỢC`** | ⭐⭐⭐ **Ba trạng thái, ⛔ không hai.** Một cổng ⛔ chưa đo được mà vẽ thành *"đạt"* là **con số nói dối thô nhất của cả hệ** | `008` `029` |
| ✅ *"`N` cổng chưa từng đo"* | Khai **tường minh**, ⛔ không giấu trong một tỷ lệ phần trăm | `008` |
| ✅ *"Độ tin của số trên màn: `N%`"* | ⛔ Nhãn **⛔ không thể nói quá**: nó suy từ số dòng đã đối soát | `034` |
| ✅ *"Máy ⛔ không khai một cổng nào canh sổ. **Báo người dựng hệ**."* | ⭐ Màn **⛔ không tự bịa** một câu trấn an khi cửa trả rỗng | `008` |
| ✅ *"Hàng chờ rỗng"* | Rỗng là một **tin**, ⛔ không phải một ô trắng | `039` |
| ⛔ Độ phủ theo nhóm × ngày | ⛔ **CHƯA CÓ** — cửa `/queue/coverage` ⛔ chưa dựng | `038` |
| ⛔ Nút **Xuất báo cáo tuần** | ⛔ **CHƯA CÓ** — cửa `/weekly` ⛔ chưa dựng. `SCR-F05` được **gấp vào đây** có chủ ý | `034` `043` |

---

## §5 · `SCR-F04` Nạp sao kê

> **Câu màn này hỏi:** *"Lô này có **nhận được** ⛔ không, và nếu ⛔ không thì **vì sao**?"*

| Nút · hiển thị | Nghĩa | `US` |
|---|---|:--:|
| ✅ **Xem trước** | Chạy **`9` luật soát** rồi trả **biên bản GỘP** — ⛔ không phải nạp `60` lượt rồi tự cộng | `048` |
| ✅ **Khai theo bằng chứng · `…`** | ⭐⭐ **`1.894/8.368` = `22,6%`** dòng có ngày đọc được **HAI** cách *(`ngày/tháng` hay `tháng/ngày`)*. ⛔ **Máy ⛔ KHÔNG được quyết** — đây là **kỳ kế toán của một bút toán**. Nút trả **bằng chứng có con số**, người ấn định | `049` |
| ✅ Khai **cả lô** cho nguồn **tự chứng** | Đo: **`34/34`** nguồn chuỗi tự chứng, `chac_dmy` = **`0`** ⇒ **`27`** cú bấm cho **một** đáp án là *"bấm theo phản xạ"*. ⛔ Nguồn ⛔ **không** tự chứng **vẫn phải** bấm riêng | `050` |
| ✅ **Bỏ qua vì trùng** | `content_key` **tự chống trùng** — nạp lại cùng tầng là **hợp lệ** | `048` |
| ✅ **Nhận được `N`** | Số dòng **vào sổ**, và số dòng **vào hàng chờ** | `048` |
| ✅ **Mở hàng chờ để xử `N`** | Liên kết thẳng sang `SCR-F01` | `039` |
| ⛔ Xem **cả dãy `version`** bản khai cột | Câu *"vì sao lô tháng trước đọc cột khác"* chỉ trả lời được nếu **thấy được bản cũ** — đó là cả lý do bảng khai là **chỉ-THÊM** | `051` |

---

## §6 · `SCR-F06` Danh mục · Nguồn — **⛔ CHƯA DỰNG**

⛔ Ba story ⛔ **không có chỗ nào để nhìn**:

| `US` | Nội dung | Hậu quả của việc thiếu |
|:--:|---|---|
| `001` | Manifest nguồn — trạng thái · độ trễ · cut-off | `2` nguồn trễ **`407`** và **`264` ngày** vẫn nằm trong danh mục đang đo |
| `018` | `Mapping Master` + cảnh báo **mã trùng** | **`75`** mã bị dùng lại ⇒ **`289`** dòng PM bị `VLOOKUP` bỏ **im lặng** |
| `031` | Danh mục pháp nhân | Bảng `Tài khoản → Pháp nhân` nằm trong sheet tên **`Daily RP test`** — ⛔ không chủ, ⛔ không ai soát |

---

## §7 · Nội dung **các hộp thoại** hiện ra

⭐⭐ **Chỗ đáng nhìn nhất ⛔ không phải cái hộp HỎI, mà cái hộp BÁO LẠI.** Bốn hộp *"Đã …"* tồn tại để nói ra thứ máy **⛔ KHÔNG làm** — và nếu chúng im, kế toán sẽ tưởng máy đã dọn sạch mọi thứ.

### ⓐ `F01` lằn TIỀN — hộp **HỎI**

| Hộp | Câu nó nói | Vì sao | `US` |
|---|---|---|:--:|
| **Lý do** → *Ghi lý do* | *"Câu trả lời vào **nhật ký** và vào **bộ đếm tuần**"* + ⚠ *"Đây là thước của `US-045`: **4 tuần ⛔ không ai gõ = cổng đã chết**. ⛔ Gõ bừa một chữ làm hỏng đúng cái thước ấy"* | ⭐⭐ Hiếm: một ô nhập **tự khai** rằng gõ bừa sẽ **làm hỏng phép đo**. Ô rỗng ⇒ ⛔ không đóng hộp, vì một sự kiện lý do **rỗng** vẫn cộng vào bộ đếm ⇒ **làm loãng chính cái thước** | `039` `045` |
| **Hoãn** → *Hoãn* | *"Hoãn **CÓ HẠN**: đến ngày ấy dòng quay lại hàng chờ. ⛔ Không phải cách để bỏ qua một dòng"* · từ lần 2: *"Lần thứ ba **đổi màu** để nhìn thấy — và ⛔ **không báo cho ai**, vì ⛔ không có vai nào nhận báo"* | Thiếu ngày ⇒ ⛔ không lưu: **hoãn vô hạn là BỎ QUA**. ⭐ Câu *"⛔ không báo cho ai"* là chỗ màn **⛔ từ chối giả vờ có quy trình leo cấp** — vận hành thật `2`–`3` người *(`QĐ-ITL-27`)* | `040` |
| **Ghép lệnh** → *Ghép* | Dòng tiền **ghim** + **tuổi ảnh chụp** · ⭐⭐ *"**Máy ⛔ không xếp được theo: ngày · người nhận**"* · ứng viên *"đã ghép nơi khác"* vẫn hiện · `Σ` hai con số tính lại mỗi lần tích | ⭐⭐ Câu *"⛔ không xếp được theo"* là **câu quan trọng nhất của cả hộp**: im lặng ⇒ người dùng tưởng thứ tự ứng viên **đã tính cả ngày và người nhận**, và tin một xếp hạng **⛔ không tồn tại** | `013` `015` |
| **Ghép cả lô** → *Ghép cả lô* | *"⚠ **Một dòng ⛔ không đạt ⇒ CẢ LÔ bị từ chối** và ⛔ không một mối nối nào được ghi. ⛔ Không có chế độ «ghép được bao nhiêu thì ghép»"* | Khai **trước** cái giá, ⛔ không để người phát hiện sau một cú `422` | `054` |
| **Bỏ ghép** → *Bỏ cả chùm* | *"Bỏ **CẢ CHÙM**, ⛔ không bỏ lẻ — bỏ lẻ làm `Σ ≠ tiền bank`, tức **tạo ra đúng trạng thái sai mà cổng dựng ra để bắt**"* + *"⭐ **Sổ ⛔ không mất gì**: bỏ là **THÊM một dòng**"* | Hạ nhiệt đúng chỗ: người ngại bấm vì sợ mất dữ liệu sẽ **để nguyên một mối nối họ biết là sai** | `046` |
| **Xong** → *Xong* | *"⛔ **Không cần lý do** (`QĐ-ITL-72`)"* + *"Bấm nhầm thì **Mở lại** — mở lại là **THÊM một sự kiện**, ⛔ không xoá gì"* | ⭐⭐ **`Hoãn` đòi lý do mà `Xong` ⛔ không — ⛔ đây ⛔ không phải bất nhất.** *Hoãn* = việc **chưa xử** ⇒ phải nói chờ gì. *Xong* = việc **đã xử** ⇒ một ô lý do **bắt buộc** chỉ đẻ ra chữ **rác** | `047` |
| **Mở lại** → *Mở lại* | *"⚠ **Lý do BẮT BUỘC** ở đây — khác nút *Xong*. Dòng này đã có **người** kết luận là xong; kéo lại là **lật kết luận của người khác**"* | Bất đối xứng **có chủ ý** và **nói ra lý do** ngay trong hộp | `047` |

### ⓑ `F01` lằn TIỀN — bốn hộp **BÁO LẠI**

| Hộp | Câu nó nói | Nếu im thì sao | `US` |
|---|---|---|:--:|
| **Đã ghép · nhưng máy ⛔ KHÔNG tự điền được** | *"**Các dòng lệnh nói nhiều giá trị khác nhau** cho `hd` · `cdt1`. Máy ⛔ **không tự chọn** — chọn thay người là máy quyết định thay người (`INV-I16`)"* | Kế toán tưởng dòng đã đầy đủ và **bỏ qua hai ô trống** — chúng đi thẳng vào P&L dưới dạng `UNMAPPED` | `026` `046` |
| **Đã bỏ ghép** | Ba câu: ⓐ đã bỏ `N` mối nối · ⓑ **đã đảo** bút toán nào · ⓒ ⭐ *"**⛔ KHÔNG đảo** `N` ô — **người** đã gõ tay lên đó sau khi ghép. **Máy ⛔ không rút lại thứ người đã quyết**"* | ⭐⭐ Bỏ ⓒ ⇒ kế toán tưởng *"bỏ ghép đã dọn sạch mọi thứ"*, và một ô `pay_type` còn sót sẽ sống tiếp **⛔ không ai biết** | `046` |
| **Đã ghi** *(sau `Xong`)* | ⓐ *"đã bấm xong từ trước bởi **X** lúc **Y**"* · ⓑ ⭐⭐ *"**Xong mà còn thiếu** … ⛔ Máy ⛔ không chặn — **nhưng nó đếm riêng**"* · ⓒ *"**Kỳ đã chốt** — vẫn bấm được, **cố ý**"* | ⓐ bấm hai lần ⛔ không thành hai sự kiện **và ⛔ không báo lỗi** — câu đúng là *"có người làm rồi"* ⛔ không phải *"bạn làm sai"*. ⓑ chặn thì mất chỗ đánh dấu việc dở; im thì nút thành **đường tắt làm sạch hàng chờ** | `047` |
| ⭐⭐⭐ **Đã ghép cả lô** | *"Những dòng này rời hàng chờ **⛔ không phải** vì ai bấm «xong» — nhãn `work_status` bị **đóng băng lúc nạp** (`INV-I08`) nên nó **vẫn nói `UNMAPPED`**"* | **Hộp đắt nhất trong bốn.** Kế toán vừa ghép `47` dòng mà thấy `UNMAPPED` sẽ kết luận **cú ghép hỏng** — rồi bấm lại, rồi báo lỗi. Nhãn là **phân loại**, mối nối là **đã nối lệnh chi** — **hai câu hỏi khác nhau** | `054` |

### ⓒ `F02` — panel phải và ba hộp xung đột

| Phần | Câu nó nói | Vì sao | `US` |
|---|---|---|:--:|
| **Panel BÊN PHẢI**, ⛔ không che màn | Vùng trên **⛔ KHÔNG cuộn** và **vẽ NGAY** *(tiền + diễn giải)*; vùng dưới cuộn *(bảy nhóm)* | ⭐ Dòng đang xem **vẫn trong tầm mắt** — cả ý đồ của bố cục *master–detail*. Vẽ ngay từ dữ liệu đã có trên lưới ⇒ panel **⛔ không bao giờ là một khung trống** trong lúc đợi cửa | — |
| **Giá trị bạn gõ KHÁC cái đang có** → *Ghi đè* / *Để nguyên, không ghi* | Bảng **hai dòng**: `nguồn đang có` / `bạn gõ`. + *"Ghi đè ⛔ không xoá gì cả — sổ **chỉ thêm**… Nhưng **phải nói vì sao** bạn tin số của mình hơn"* | ⭐⭐ Hai giá trị đặt **cạnh nhau**, ⛔ không bắt nhớ: câu hỏi *"ghi đè ⛔ không"* chỉ có nội dung khi người thấy **cả hai**. ⭐ Nút *"Để nguyên, không ghi"* dài mà **cố ý** — nó nói đúng hệ quả; một nút *"Huỷ"* ⛔ không cho biết **số của bạn sẽ ⛔ không vào sổ** | `025` |
| **Ô này đã có NGƯỜI KHÁC gõ** | Hộp **RIÊNG**, cố ý ⛔ không gộp vào hộp báo hỏng | ⭐ Ở đây ⛔ **không có gì hỏng** — chỉ là **hai người cùng làm một việc**, và câu trả lời là **một cuộc nói chuyện**, ⛔ không phải một lần bấm *"Thử lại"* | `025` `030` |
| **Lô lưu DỪNG giữa chừng** → *Thử lại ngay* / *Đóng* | Liệt kê **đúng những ô CHƯA vào sổ**, và *"chúng vẫn **viền vàng** trên lưới"* + *"Chúng ⛔ không mất"* | ⭐⭐ Một câu *"lưu thất bại"* trống rỗng để kế toán ⛔ không biết **ô nào đã vào, ô nào chưa** — và đó là lúc người ta **gõ lại thứ đã lưu rồi** | `030` |
| **Đảo bút toán #N** → *Đảo* / *Thôi* | *"Đảo **⛔ không xoá** gì cả — nó **thêm một dòng nữa** trỏ ngược lại. Sau khi đảo, giá trị **lùi về bút toán trước đó**, hay về **giá trị của sổ gốc** nếu ⛔ không còn bút toán nào"* | Nói rõ **lùi về đâu**. Thiếu câu ấy thì *"đảo"* đọc như *"xoá"* — mà **⛔ KHÔNG có thao tác xoá** nào trong TO-BE *(`INV-I08`)* | `033` |

⭐ **Luật chung của cả bốn hộp báo:** máy **rút lại được** thứ **chính nó** suy ra; nó ⛔ **không rút lại** thứ **người** đã quyết — và nó **nói ra ranh giới ấy** mỗi lần.

⚠ **Và `F02` tự khai HAI chỗ nó CỐ Ý ⛔ không vẽ** ở chân màn: ⓐ *hai người sửa một ô* — cửa ghi **⛔ không phát hiện được** *(`GAP-SCR-09`)*; màn có hỏi lại ngay trước khi ghi, nhưng đó là một phép **KIỂM**, ⛔ không phải một **BẢO ĐẢM**. ⓑ Hai trường ⛔ **không có trên lưới** vì cửa `GET /ledger` ⛔ không trả chúng — chúng gõ ở **ngăn kéo**.

⇒ ***Khai ra một chỗ trống còn tốt hơn để nó trông như một chỗ đã đầy.***

---

## §8 · Bảng tra ngược — `US` → nó sống ở nút nào

| `US` | Sống ở | Trạng thái |
|:--:|---|:--:|
| `013` | F01 cả hai lằn · ngăn kéo **Ghép** | ✅ |
| `014` | F01 lệnh chi · rổ **cần người tra** | ✅ |
| `015` | ⛔ ⛔ không có phép chặn mã trùng ở cửa ghép | ⛔ |
| `016` | F01 lằn **TIỀN** | ⚠ |
| `023` `026` `030` | F02 · `itl_id` · `UNMAPPED` · nhật ký `7` trường | ✅ |
| `025` | F02 · ba nút của cú `409` | ✅ |
| `033` | F02 · **Đảo** | ✅ |
| `039` | F01 · lưới + xếp tiền ✅ · **tuổi việc** ⛔ · **cột lý do** ⚠ | ◐ |
| `040` `046` `047` | Chỉ lằn **TIỀN** | ⚠ |
| `045` | ⛔ Cửa `/queue/reason-weekly` ⛔ không tồn tại | ⛔ |
| `048`–`051` | F04 · `051` ⛔ chưa có | ◐ |
| `052`–`055` | F01 lệnh chi | ✅ |
| `056` | ⛔ Sửa/map lại trên lằn mặc định | ⛔ |
| ~~`017`~~ ~~`036`~~ ~~`041`~~ | **KHAI TỬ** — `QĐ-ITL-56` · `QĐ-ITL-131` | ⛔ |

---

### §A9 · ⭐⭐ BỐN cử chỉ **⛔ chưa dùng được** — và nay đã dùng được *(2026-09-22)*

`§A8` đọc **bản dựng**. Mục này đọc **mã đang chạy**, và ba ngày sau nó nói một chuyện khác hẳn: ba cử chỉ của `§A8` **⛔ không hề nối vào màn thật**.

| Cử chỉ | Trạng thái `21/09` | Nay |
|---|---|---|
| `↑` `↓` `←` `→` `Enter` `Esc` `/` `j` `k` | ⛔ **`0/9` dùng được** — `phim()` viết đủ, ⛔ không ai đăng ký `keydown` | ✅ nối trên `document`, tự chặn khi màn ⛔ không bật |
| Gõ vào ô **Tìm giao dịch** | ⛔ **ô chết** — `#ghep-tim` ⛔ không ai nghe `input` | ✅ gõ ⇒ **bật Toàn sổ** ＋ gọi `?q=`, chờ `250ms` |
| `đủ ↓` ／ `thu gọn ↑` | ⛔ **⛔ không tồn tại** | ✅ chỉ mời khi diễn giải **thật sự bị cắt** *(đo `scrollHeight`)* |
| **Bỏ gán** | ⛔ gọi `/queue/undefined/chum` | ✅ đọc `itl_da_gan[]`; gắn **nhiều hơn một** giao dịch ⇒ màn **nói ra** và chỉ sang `SCR-F02` |

⭐⭐ **Ô tìm bật Toàn sổ** — đây cũng là **lối bật bằng tay** mà hợp đồng `§8` đòi và màn `21/09` ⛔ không có: `ST.toan_so` khi ấy **chỉ TỰ bật** khi máy ⛔ không tìm được ứng viên nào.

⛔⛔ **Vì sao ba cử chỉ chết mà `§A8` vẫn mô tả chúng như đang sống.** `§A8` đọc **bản dựng** — nơi mọi thứ **có nối**. Mã sản phẩm thì có hàm mà ⛔ không có dây. ⇒ Một tệp *thuyết minh* đọc **bản dựng** nói được *"màn NÊN phản ứng thế nào"*, ⛔ **không** nói được *"màn CÓ phản ứng ⛔ không"*.

⭐ Và một cử chỉ nữa **⛔ chưa có**: bấm `đủ ↓` **⛔ không** kéo theo chọn ứng viên — *"cho tôi đọc hết câu này"* và *"tôi chọn dòng này"* là **hai ý định khác nhau**, nên cú bấm ấy dừng lại ở nút ngoài qua `closest`.


## Changelog
- **v1.9** *(2026-10-05, `fls-ba`, xếp `KQ-041`)*: `F01L ⓪` bốn chuỗi `F01L` *(hàng `may` · ghi chú băng · `note ok` · nhãn lọc)* ⛔ còn hứa *"lệch tiền"* / *"chỉ DUYỆT"* cho cả rổ `may` *(đúng **78 / 120**)* ＋ chip `②b` đếm theo lượt tải mới nhất *(`F-3`: **2.955** thay **2.219**)*. Spec `BA-06` **v4.18** `§4.5 ⓤ` + `ⓥ`. Mã ⇒ `WO-042`.
- **v1.8** *(2026-10-02, `fls-ba`, `TL-038`)*: `F01L ⓪` băng *Việc của bạn hôm nay* — dòng 2 tách hai câu theo `nguoi_khac_tien_te` *(câu cũ sai **84 / 616**)* · dòng ghi chú `may − tu_chung` ⛔ còn nói *"lệch tiền"* *(đúng **78 / 120**)*. Spec `BA-06` **v4.17** `§4.5 ⓤ` · `BA-07` **v3.10**. Mã ⇒ `WO-037` vòng 2.
- **v1.7** *(2026-10-02, `fls-ba`, `TL-033`)*: `F01G ⓑ` Toàn sổ thêm bậc `≠ khác tiền tệ` *(mã `9c100ac`)* + ghi hai chỗ màn đang nói sai/thiếu *(khối *"Đang gán"* `①` **0 / 2.219** · chú giải bậc ⛔ dựng)*. Mã ⇒ `WO-032` vòng 2.
- **v1.6** *(2026-10-02, `fls-ba`, nghiệm thu PO `WO-022` + `KQ-031`)*: ④ ngăn kéo *Tìm tiền* — ⓐ dòng *Bảng ứng viên*: `Tiền` in **kèm mã**, `Lệch` có số ở mọi bậc khi cùng tiền tệ, khác tiền tệ in **`khác tiền tệ`** *(`BA-06` v4.14 §5b ⓕ/ⓙ — **165 / 5.360** ứng viên khác tiền tệ lệnh)*; ⓑ dòng *Σ hai con số*: khác tiền tệ ⇒ *"khác tiền tệ — cửa ghi sẽ TỪ CHỐI"* *(hôm nay **4** lệnh sổ thật được nói *"trong dung sai"*)*; ⓒ ô *vì sao ghép cặp này* ~~BẮT BUỘC~~ ⇒ **tuỳ ý** *(`QĐ-ITL-149 ⓑ`, owner 01/10 — mã còn chặn ở `man_f01_lenh.js:650`)*. Mã ⇒ `WO-032`.
- **v1.5** *(2026-09-23, owner nhìn màn THẬT — `4` vòng góp ý)*: ⭐⭐⭐ **Thêm `§A10` — NĂM cử chỉ MỚI, và một cử chỉ CŨ đổi hành vi.** ⭐⭐ **Tay kéo** bề rộng cột lệnh chi *(`role=separator`, chuột ＋ `←→`)* — ⛔⛔ bề rộng sống trong **`ST.rail_w`**, ⛔ **không** trong DOM: `ve()` dựng lại **cả cây**, nên đặt thẳng vào phần tử thì kéo xong bấm một cái là **nhảy về cũ** và người ta tưởng **tay kéo hỏng**; chặn `260`…`720px` vì **hai đầu đều là *"màn hỏng"***. ⭐⭐ **`Esc` nay bóc TỪNG LỚP MỘT** — khi *«Xem đủ trường»* đang mở thì nó đóng **lớp phủ**, ⛔ không đóng lệnh: đóng thẳng cả lệnh thì người vừa mở khối để đối chiếu **mất luôn dòng đang làm**, ⛔ không cách nào quay lại ngoài tìm lại trong `738` dòng. ⭐ Nút **`✕`** trên lớp phủ *(`Esc` là đường ra của người **biết** nó tồn tại ⇒ phải có một nút **nhìn thấy được**)*; nút **`bỏ gán`** ngay trên khối `C4` — một **đường ra tại chỗ**, ⛔ không bắt người ta đi tìm ở thanh dưới cùng *(chùm `>1` vẫn **hỏi trước** và **nêu tên từng dòng** — `QĐ-ITL-148 ⓔ`)*. ⛔⛔ **Cử chỉ cũ đổi hành vi:** bấm chọn một giao dịch nay ⛔ **không** làm danh sách nhảy về đầu — lỗi ấy do **chính phép sửa cùng ngày** đẻ ra *(cho `.cands` cuộn riêng ⇒ `ve()` dựng lại cây ⇒ `scrollTop` về `0`)*, và trước `23/09` nó ⛔ **không tồn tại** vì cả trang cuộn và trình duyệt tự giữ vị trí. ⭐ Giữ chỗ cuộn ⛔ **không phải luôn luôn đúng**: đổi sang một **lệnh khác** thì danh sách là một danh sách **khác hẳn** ⇒ luật là **giữ chỗ khi vẽ lại cùng một cảnh, về đầu khi đổi cảnh**.
- **v1.4** *(2026-09-22, plan vá bốn lỗi CHẶN)*: ⭐⭐ **Thêm `§A9` — BA cử chỉ của `§A8` ⛔ KHÔNG hề nối vào màn thật.** `§A8` đọc **bản dựng** *(nơi mọi thứ có nối)*; mã sản phẩm thì **có hàm mà ⛔ không có dây**: `phim()` viết đủ `9` phím và **⛔ không ai đăng ký `keydown`** ⇒ `0/9` dùng được; `#ghep-tim` ⛔ **không ai nghe `input`** ⇒ cửa `?q=` **⛔ chưa bao giờ nhận một chữ**; `đủ ↓` ⛔ **không tồn tại**; `Bỏ gán` gọi `/queue/undefined/chum`. ⭐⭐⭐ **Bài học cho chính tệp này: một thuyết minh đọc BẢN DỰNG nói được *"màn NÊN phản ứng thế nào"*, ⛔ KHÔNG nói được *"màn CÓ phản ứng ⛔ không"*.** ⇒ `§A9` đọc **mã đang chạy**. ⭐ Ô tìm nay **bật Toàn sổ** — cũng là lối bật **bằng tay** mà hợp đồng `§8` đòi và màn `21/09` ⛔ không có *(khi ấy `ST.toan_so` chỉ **TỰ** bật khi máy ⛔ không tìm được ứng viên nào)*. ⭐ Bấm `đủ ↓` **⛔ không** kéo theo chọn ứng viên: *"cho tôi đọc hết câu này"* và *"tôi chọn dòng này"* là hai ý định khác nhau.
- **v1.3** *(2026-09-21, `QĐ-ITL-146` — bàn giao thiết kế về)*: ⭐⭐⭐ **Thêm `§A8` — tầng *phản ứng thế nào* nay đọc được từ MÃ, ⛔ không còn từ mô tả.** `v1.1` dựng `§A` vì ⛔ không tệp nào nói màn phản ứng ra sao; nhưng lúc ấy nó vẫn là **đặc tả mong muốn**. Nay có **bản dựng chạy được** ⇒ `§A8` đọc thẳng `fls-gan-lenh-chi_10.html`, đúng cách `§1`–`§7` đọc `man_f0*.js`. ⭐⭐ **Chín cử chỉ, mỗi cái kèm ca TỪ CHỐI** — và ca quan trọng nhất là **lệch tiền**: lần bấm đầu ⛔ **không ghi**, nút đổi thành *«Xác nhận gán lệch …»*, và ⭐⭐⭐ **`Enter` bị KHOÁ** *(câu gợi ý nói thẳng ra điều đó)*. `45%` ca ⛔ không có ứng viên đúng tiền, nên nếu `Enter` vẫn gán được thì màn **dạy người ta gật theo phản xạ**. ⭐ **Máy ⛔ KHÔNG chọn sẵn ứng viên** — kể cả dòng nó đề xuất; đề xuất chỉ được **đánh dấu**. Đó là `INV-I16` ở tầng ngón tay, ⛔ không phải ở tầng dữ liệu. ⭐⭐ Thêm `ⓑ` — chế độ **Toàn sổ** đổi **NGUỒN** danh sách *(⛔ không phải nới bộ lọc)* và **tính lại bậc** theo lệnh đang mở; nó **bật sẵn** khi máy ⛔ không tìm được ứng viên nào ⇒ màn **⛔ không bao giờ là ngõ cụt**. ⛔ Gộp hai thứ vào một điều khiển thì màn rỗng ⛔ không phân biệt được *«máy ⛔ không tìm ra»* với *«sổ ⛔ không có»*. ⛔ `ⓒ` khai **ba việc bản dựng CHƯA làm**, trong đó nặng nhất: **bỏ gán phải là THÊM một dòng** *(`INV-I08`)* — một `DELETE` ở đó xoá mất bằng chứng *ai từng nối gì*.
- **v1.2** *(2026-09-18, `QĐ-ITL-144` — owner BA màn hình **cùng kế toán**)*: ⭐⭐⭐ **Thêm `§A7` — bốn yêu cầu do NGƯỜI SẼ DÙNG nêu, và một trong số đó lật phép gom nhóm tôi vừa dựng.** Owner: *"công việc mapping được thực hiện **mỗi ngày, theo từng giao dịch 1** → sort theo thời gian"* ⇒ ⛔ **bỏ hẳn gom nhóm**. ⭐ Bài học: gom nhóm tối ưu cho **một đợt dọn tồn**, màn này phục vụ **nhịp hằng ngày** — tối ưu **sai nhịp** thì màn đúng về số liệu mà **sai về công việc**. ⭐⭐ Đổi chữ theo owner: *máy đã đoán* → **`đề xuất gán`**, *người đã chốt* → **`đã gán`** — chữ cũ nói về **ai làm**, chữ mới nói **việc đang ở đâu**. ⛔ Và **BỎ nhãn *"ô chờ gật"*** — nó đếm **ô** *(`2.219 × 2 = 4.424`)*, đơn vị của **máy**; người làm đếm theo **việc**. Chính `UI-F8` cấm điều đó và tôi vi phạm ngay ở dòng đầu màn. ⭐ Bốn trường thêm: **số PM** *(danh sách)* · **ngày ＋ CDT** *(vế lệnh chi)* · **ngày ＋ nội dung** *(vế giao dịch)* — ba cái đầu có sẵn, ⛔ **nội dung giao dịch `0/8.387`** ⇒ màn phải nói *"chưa được nạp"*, ⛔ không để trống như thể *"giao dịch này không có nội dung"* *(`GAP-NAP-04`)*.
- **v1.1** *(2026-09-18 tối muộn, `CR#12` bước **spec-first**, owner: *"đã có thiết kế chi tiết chưa"*)*: ⭐⭐⭐ **Thêm `§A` — TẦNG BA của thiết kế, thứ mà cả `BA-06` lẫn `BA-14` đều ⛔ KHÔNG tả.** `BA-14 §8` nói **vì sao**, `BA-06 §4` nói **trông ra sao**, và suốt một ngày ⛔ **không tệp nào** nói **màn phản ứng thế nào** — bấm thì gì xảy ra, rỗng thì hiện gì, cửa từ chối thì đọc ra câu gì. ⛔⛔ Chỗ ⛔ không tả là chỗ dev **phải đoán**. ⭐⭐ `§A` phủ **bốn chỗ** *(`Tự động` 47 · `Thủ công` 738 · ghép ⛔ không được 768 · lỗi nguồn 167)*, mỗi chỗ có **cửa thật** · **cột hiện** · **nút** · **ca từ chối** · **bốn trạng thái** *(đang tải · rỗng · cửa lỗi · tuổi dữ liệu)*. ⭐⭐⭐ **Và một phép đo TỰ KHỚP:** đo `tho` độc lập ra **`3.237/3.772` (85,8%)** dòng lệnh có ô `Reference number` ⇒ **`535`** dòng ⛔ không có — **đúng bằng** rổ `nguoi` mà `dem_theo_ro` trả về, bằng **một câu lệnh khác hẳn** ⇒ phép chia rổ ⛔ **không** phải nhãn máy tự đặt. ⭐ **Cả `9` trường của `UI-F7` đều CÓ trong kho**, nhưng **`5` trong số đó sống trong `tho` (JSON) ⛔ không phải cột** ⇒ cửa `ro` **phải trả chúng ra**, nếu ⛔ không thì màn ⛔ không vẽ nổi một dòng. ⛔ `§A6` khai thẳng **ba câu chưa trả lời được**, trong đó `GAP-SCR-19`: `§A0` cho một dòng **ba** đường ra và ⛔ không đường nào là nút `Xong` — nhưng `QĐ-ITL-71` là **quyết định của owner** nên ⛔ **không tự rút**. ⚠ Phần từ `BIA` trở xuống **giữ nguyên từng chữ** làm bản ghi của thứ owner gọi là *overdone*.
- **v1.0** *(2026-09-14, owner: *"tại từng màn hình, thuyết minh ý nghĩa của từng `UC`/`US` và các nút bấm, hiển thị"*)*: bản đầu. ⭐ **Dựng từ MÃ ĐANG CHẠY**, ⛔ không từ đặc tả — trích nhãn nút và tiêu đề cột thẳng từ `fls/web/tep/man_f0*.js`. ⭐⭐ Kèm cổng `tools/kiem_thuyet_minh.py`: một nhãn nút ⛔ không có dòng thuyết minh thì **⛔ không qua cổng**. Đó chính là **phép đo buộc tài liệu đi theo mã** mà `BA-03` ⛔ không có — và vì thiếu nó, `BA-03` đã già trong im lặng **ba lần** *(`28/08` thiếu 2 thao tác · `09/09` thiếu cả lằn NẠP · `14/09` thiếu cả lằn LỆNH CHI)*.
