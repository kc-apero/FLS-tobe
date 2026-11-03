# 10 — DECISION TABLE: quy tắc nghiệp vụ

**Version:** v0.8 | **Chủ sở hữu:** COO-CFO | **Nguồn:** sheet `Mapping Master` thật (ITL RAW), `NGUỒN-BUILD` §4, nợ dữ liệu ở `ORC-06` §3

Mỗi bảng là *điều kiện → hành động*. **Quy tắc là dữ liệu, không phải code** (`P-05`): giá trị sống trong `MAPPING-MASTER` có version; file này mô tả **cấu trúc** và **thứ tự áp**.

---

## ⭐⭐⭐ DT-I13 · LUẬT GHÉP — **hai nhánh, và kế toán chia theo VN / NƯỚC NGOÀI** *(`QĐ-ITL-144`, 2026-09-18)*

> ⭐ **Nguồn: owner BA màn hình **cùng kế toán** rồi mang luật về.** Đây là **lần đầu** dự án có một luật ghép **do người làm phát biểu**; trước đó máy ghép theo `reference` ＋ bốn bậc tiền — một luật **tôi suy từ dữ liệu**, ⛔ không ai ký.

| # | Điều kiện | Khoá ghép | FLS chạy được ⛔ không |
|:-:|---|---|---|
| ⓐ | Giao dịch **Việt Nam**, giao dịch **có PM code** | `PM code` ＋ `số tiền` ＋ ⭐ `pháp nhân` | ⚠ **gần đủ** — xem `ⓐ‑1` |
| ⓑ | Giao dịch **nước ngoài** | `từ khoá trong nội dung CK` ＋ `tên vendor` ＋ `số tiền` | ⛔ **KHÔNG** — xem `ⓑ‑1` |

### ⓐ‑1 · Nhánh VN — thiếu đúng **một** mắt xích, và nó **nối được**

⭐ **`pháp nhân` là thứ luật mới thêm so với máy hiện nay** — máy đang ghép **⛔ không** dùng pháp nhân, tức nó **lỏng hơn** luật của kế toán. Thêm vào là **chặt lại**, ⛔ không phải nới ra.

⛔⛔ **Nhưng hai bên gọi cùng một pháp nhân bằng HAI mã khác nhau** *(đo `18/09`, `pm_line_id` phân biệt)*:

| Phía | Nói thế nào | Ví dụ |
|---|---|---|
| Lệnh chi | `tho['Pháp nhân thanh toán']` — **mã ＋ tên** | `VVOH - Astronex` · `VGO2 - TeraSofts` |
| Giao dịch | ⛔ cột `le` **rỗng 0/8.387**; suy từ `source_sheet` — **mã HOẶC tên** | `ASTRONEX` · `TERASOFTS` · `VGOH` |

⭐ **Cứu được, vì chuỗi bên lệnh chi mang CẢ HAI nửa.** Khớp *"mã **hoặc** tên"*:

| Kết quả | Dòng lệnh | % |
|---|--:|--:|
| ⭐ nối được pháp nhân | **3.120** | **82,7%** |
| ⛔ phải hỏi người | **652** | **17,3%** |

⛔⛔ **`652` dòng ấy ⛔ KHÔNG được đoán** *(`INV-I16`)*, và dòng lớn nhất là một cặp **trông rất giống nhau**: lệnh chi nói **`CNC`** *(522 dòng)*, giao dịch nói **`CN`** *(906 dòng)*. Giống nhau ⛔ không phải bằng chứng — **phải hỏi**. Còn lại: `SGO1` **68** · `BGO1` **54** · `UGO` **4** · `MGO1` **4**.

⇒ Cần một **bảng bắc cầu** *(`fls_le` đã có chỗ: cột `le_name`, hiện **chỉ 2/20 mã** có tên)*. ⚠ `GAP-LE-01`.

### ⓑ‑1 · Nhánh nước ngoài — ⛔ **KHÔNG chạy được, và nó là NỬA công việc**

> ⭐⭐⭐ **ĐÍNH CHÍNH cùng ngày — `QĐ-ITL-145`.** Câu *"⛔ không chạy được"* dưới đây **đúng lúc viết** và **sai sau đó vài giờ**. Diễn giải sao kê ⛔ **chưa bao giờ thiếu**: nó nằm sẵn trong **ảnh chụp theo nhịp giờ** *(`8.589/8.592` dòng có `Description`)*, chỉ là ⛔ **không đường nào nối nó với một dòng sổ**. Khung xem `fls_dien_giai` *(migration `0026`)* nối được **`8.358/8.387` = 99,7%**. ⇒ Nhánh ⓑ nay thiếu **phép TÌM**, ⛔ không thiếu **dữ liệu**: đo mẫu `180` ứng viên thì **`177` có chữ**, và **tên vendor nằm ngay trong đó** *(`SENSORTOWER, INC.` · `OPENAI *CHATGPT SUBSCR` · `HAILUOAI.VIDEO`)*. ⛔ Bảng dưới **giữ nguyên chữ** làm bản ghi của phép đo lúc `0/8.387`.

⛔⛔ **Cả hai vế đầu của luật đều ⛔ KHÔNG có trong sổ** *(đo `18/09` trên `8.387` dòng)*:

| Luật cần | Cột | Có |
|---|---|--:|
| từ khoá trong **nội dung chuyển khoản** | `memo` | ⛔ **0 / 8.387** |
| **tên vendor** | `acct` | ⛔ **0 / 8.387** |
| số tiền | `ps_no` ／ `ps_co` | ✅ |
| ngày | `doc_date` | ✅ 8.387 |

⛔ **Quy mô:** giao dịch ⛔ không phải `VND` = **4.145 / 8.387 = 49%**. ⇒ Luật ⓑ phủ **gần một nửa** cuốn sổ, và hôm nay ⛔ **không một dòng nào** chạy được.

⭐ **Vì sao rỗng — nó ⛔ không phải lỗi nạp.** Tầng `R |` của bảng tính nguồn **chỉ có 5 cột**; cột diễn giải của sao kê **⛔ chưa bao giờ được đưa vào phạm vi**. ⇒ Đây là việc **NẠP**, ⛔ không phải việc **GHÉP**. ⚠ `GAP-NAP-04`.

> ⛔⛔⛔ **Và đây là điều phải nói thẳng: bốn bậc ứng viên hiện nay ⛔ KHÔNG PHẢI luật này.**
> Máy đang xếp theo `mã` › `tiền` › `gần tiền` › `cùng tiền tệ` — một thứ tự **tôi suy từ dữ liệu**.
> Nó **trùng một phần** nhánh ⓐ *(mã ＋ tiền)* và ⛔ **không có gì** của nhánh ⓑ.
> ⇒ ⛔ Đừng đọc *"máy đã ghép 2.222 dòng"* thành *"máy đã chạy luật của kế toán"*.

---

## ⭐⭐ DT-I14 · Ghép xong — ô `hd`/`cdt1` được ghi **gì, vào đâu** *(`QĐ-ITL-149`, 2026-10-01)*

Owner 01/10 *(câu `WO-001 Q3`)*: giá trị máy suy từ dòng lệnh khi ghép là **"Máy gợi ý"**. Bảng áp cho **mọi** đường ghép — tay *(`match`)*, lô *(`match-lo`)*, máy *(lúc nạp)* — vì cả ba dùng **một** phép suy *(`may_ghep.suy_hd_cdt1`)*. Áp **riêng từng ô** `hd`, `cdt1`. Chi tiết kho: `BA-05 DD-I15 ⓓd`.

| # | N dòng lệnh của cú ghép | Ô đã có giá trị **NGƯỜI** chốt *(`fls_sua_tay`)* | Gợi ý máy đang có *(`fls_may_goi_y`)* | ⇒ Hành động | Final của ô |
|:-:|---|---|---|---|---|
| 1 | **đồng ý** một giá trị `v` | có | — | ⛔ ghi; khai `nguoi_da_chot` | ⛔ đổi *(giữ giá trị người)* |
| 2 | đồng ý `v` | ⛔ | = `v` | ⛔ ghi *(⛔ thêm dòng rỗng)* | ⛔ đổi |
| 3 | đồng ý `v` | ⛔ | ⛔ có, hay ≠ `v` | **ghi gợi ý** `v`: `nguon='may_goi_y'`, `actor` = người bấm *(hay `may@fls` ở đường nạp)*, `evt_id` = sự kiện `match` | ⛔ đổi *(= cột nguồn, thường rỗng)* |
| 4 | nói **≥ 2** giá trị khác nhau | — | — | ⛔ ghi; khai `khong_suy_duoc` *(`INV-I16`)* | ⛔ đổi |
| 5 | mọi dòng **rỗng** ô ấy | — | — | ⛔ ghi gì | ⛔ đổi |
| ⭐ 5a *(v0.7)* | **TRỘN**: ≥ 1 dòng **rỗng** ô ấy, mọi dòng **có** giá trị đều nói **cùng** `v` | *(như 1–3)* | *(như 1–3)* | xử **như "đồng ý `v`"** ⇒ đi tiếp nhánh 1 / 2 / 3 | ⛔ đổi |

⭐ **Nhánh 5a — vì sao ô RỖNG tính là "⛔ lên tiếng", ⛔ phải "bất đồng"** *(v0.7, `fls-ba` trong thẩm quyền spec — `KQ-005 F-3`)*:
- Luật *"chỉ suy khi **cả N dòng đồng ý**"* *(`INV-I16 ⓒ`)* tồn tại để **máy ⛔ CHỌN** giữa hai câu trả lời khác nhau *(đo 18/09: **10** dòng sổ nói ≥ 2 mã `hd`)*. Ở ca trộn ⛔ có lựa chọn nào: chỉ **một** giá trị được nói ra, các dòng kia **im**.
- Cùng nghĩa với hai chỗ đã có: nhánh **5** *(mọi dòng rỗng ⇒ rỗng ⛔ phải một giá trị để suy)* và `DT-I09` nhánh 1 *(ô rỗng ⛔ phải giá trị sai)*. Đếm rỗng là "phiếu chống" thì nhánh 5 phải đổi theo — ⛔ ai muốn thế.
- Cái giá được chặn bởi `QĐ-ITL-149`: kết quả chỉ là **gợi ý**, Final ⛔ đổi, người vẫn phải gõ. Nếu dòng rỗng thật ra thuộc hợp đồng khác thì gợi ý **sai cho phần tiền của dòng ấy** — người gõ đè là xong, ⛔ mất gì.
- ⭐ **Đo 01/10 tối** *(sổ thật, chỉ `SELECT`; ảnh PM mới nhất mỗi `pm_line_id` — cách `tools/goi_y_lai.py:42`–`48` đọc)*: dòng tiền có **≥ 2** mối nối hiệu lực = **25** *(mẫu số ≠ 0, `Đ3`)*, nối đủ 25/25 vào ảnh PM ⇒ ca trộn `hd` **0/25** · `cdt1` **0/25** *(đồng ý đủ `hd` 15 · lệch `hd` 10 · đồng ý đủ `cdt1` 23 · lệch `cdt1` 2)*. Ảnh PM: dòng lệnh rỗng `hd` **4/3.820**, rỗng `cdt1` **7/3.820** ⇒ ca trộn **hiếm**, hôm nay ⛔ chạm dòng nào.
- Mã **đã** làm đúng nhánh này *(`fls/repo/may_ghep.py:68`–`69` `gt.discard("")`)* ⇒ ⛔ đổi mã, chỉ **ghim bằng bài** *(`WO-003` vòng 2 ~~`AC-15`~~ **`AC-16`** — đính chính v0.8, `KQ-007 F-4`)*. ⚠ Owner muốn ngược lại *(rỗng = bất đồng ⇒ `khong_suy_duoc`)* thì đổi đúng một dòng ấy + bài ghim.

**Bỏ ghép** *(`unmatch`)* — áp cho từng bút toán gắn sự kiện `match` của dòng. ⭐⭐ **v0.7 *(`KQ-005 F-1`)*: xét MỌI LỚP, ⛔ chỉ lớp khung xem đang trả.**

| # | Bút toán ấy hôm nay | ⇒ Hành động |
|:-:|---|---|
| 6 | `nguon='may_goi_y'` và **⛔ có bản đảo nào** trỏ về nó *(⛔ dòng `fls_adjustment` nào có `reversal_of` = nó)* — ⭐ **bất kể lớp**: kể cả khi nó đã bị một gợi ý mới hơn **đè** nên khung xem `fls_may_goi_y` ⛔ còn trả nó | **ĐẢO** *(thêm dòng `reversal_of`, `nguon='may_goi_y'`)* |
| 7 | ⭐ *(v0.7)* **đã có bản đảo** | ⛔ làm gì · ⛔ khai vào `bo_qua` *(nó ⛔ phải giá trị người — xem định nghĩa dưới)*. ~~v0.6: *"đã bị đảo / **bị gợi ý mới hơn đè** ⇒ ⛔ làm gì"*~~ — vế *"bị đè"* **SAI**, rút: lớp bị đè vẫn **chưa đảo**, nên khi lớp trên bị đảo nó **nổi lên lại** thành gợi ý **mồ côi** *(`KQ-005 F-1`, 2/2 kịch bản)* ⇒ nay thuộc nhánh **6** |
| 8 | `nguon='sua_tay'` **cũ** *(trước `WO-003`)*, **⛔ có bản đảo** — bất kể lớp | ĐẢO, bản đảo mang `nguon='sua_tay'` *(luật cũ — đo 01/10: **0** dòng như thế chưa đảo; 2 dòng UAT đã đảo)* |
| — | giá trị **người** gõ *(`/adjust`)* — bút toán ⛔ gắn sự kiện `match` | ⛔ **chạm**; khai `bo_qua` nếu nó nằm trên một ô mà dòng từng có bút toán gắn `match` |

⭐⭐ **Luật một câu thay nhánh 7 cũ:** *bỏ ghép đảo **mọi** bút toán gắn sự kiện `match` của dòng mà **chưa có bản đảo** — mọi lớp, mọi vòng ghép trước — và ⛔ chạm bút toán nào ⛔ gắn `match`.* Vì sao *mọi* lớp: `unmatch` gỡ **cả chùm** mối nối *(`QĐ-ITL-69`)* ⇒ sau nó dòng có **0** mối nối, nên **⛔ gợi ý nào** từ sự kiện `match` còn căn cứ — lớp trên hay lớp dưới đều vậy. Khung xem `fls_may_goi_y`/`fls_sua_tay` *(migration `0025`)* trả lời *"ô này **đang** là gì"* = **lớp trên cùng**; dùng nó để chọn thứ cần đảo là hỏi **sai câu** *(luật `Đ3` họ hàng: đo trên tập của câu hỏi khác)*. Giá trị người ⛔ bao giờ bị đảo vì bút toán của nó gắn sự kiện `adjust`, ⛔ `match`.

⭐ **Bất biến đo được** *(`INV-I22`, `BA-11` v0.15)*: sau một cú bỏ ghép, dòng ấy có **0** bút toán `nguon='may_goi_y'` gắn sự kiện `match` mà chưa có bản đảo *(⇒ `fls_may_goi_y` của dòng = **0**, kể cả **lớp dưới**)*. Toàn sổ: **0** gợi ý máy chưa đảo trên dòng **không còn** mối nối hiệu lực nào. Đo 01/10 tối *(sổ thật)*: **4.424** bút toán gợi ý chưa đảo *(mọi lớp; mẫu số ≠ 0)* · trong đó nằm trên dòng **0** mối nối: **0** · ô có **≥ 2** lớp chưa đảo **0** ⇒ hôm nay ⛔ dòng thật nào dính; sẽ dính lần đầu `tools/goi_y_lai.py` chồng lớp rồi có người bỏ ghép.

⭐⭐ **Định nghĩa `bo_qua`** *(`KQ-005 F-2` — `BA-06` v4.7 `:1174` **đúng**, ⛔ đổi: *"`bo_qua` = cái máy ⛔ KHÔNG rút **(người đã gõ tay)**"*)*: **một mục `bo_qua` = một giá trị NGƯỜI** — dòng của khung xem `fls_sua_tay` *(`nguon='sua_tay'`, bút toán ⛔ gắn sự kiện `match`)* nằm trên ô mà dòng **từng** có bút toán gắn `match` *(vòng ghép nào cũng được)*. Mỗi ô **nhiều nhất một** mục; mục mang `nguon='sua_tay'`. ⛔⛔ Bút toán **máy** — đã đảo ở lượt trước *(nhánh 7)*, vừa đảo ở lượt này *(nhánh 6/8, đã nằm trong `but_toan_dao`)* — **⛔ BAO GIỜ** vào `bo_qua`: màn `F01` in mảng ấy dưới câu *"người đã gõ tay lên đó"*, nên một mục máy là **bịa về việc người làm**. Đo `KQ-005 F-2`: ghép → bỏ → ghép lại → bỏ, ⛔ ai gõ ⇒ mã hôm nay trả **2** mục *(phải **0**)*.

⭐ **Nhật ký của bản đảo — đọc thế nào** *(v0.8, `KQ-007 F-1`)*: bản đảo mang `value_before` = giá trị **của chính lớp** bị rút và `value_after` = `NULL` *(`WO-003` vòng 2 Rủi ro 2 — nhật ký đọc được *"rút HD-A"*, *"rút HD-B"* riêng)*; luật **ghi** ⛔ đổi. `NULL` ở đây nghĩa *"lớp này hết hiệu lực"*, ⛔ *"ô bị xoá"*: ở nhánh 6 *(`may_goi_y`)* Final ⛔ bao giờ đổi vì gợi ý ⛔ bao giờ là Final *(`QĐ-ITL-149`)*. Màn đọc theo `value_source` ⇒ `BA-06` v4.8 dòng *"F02 · nhật ký trong drawer"*. Nhánh 8 *(`sua_tay` cũ dưới giá trị người)* là phần còn lại **chấp nhận**: sổ thật **0** dòng và tập **đóng** *(sau `WO-003` cú ghép ⛔ còn ghi `sua_tay` — đo 01/10 tối: bút toán `sua_tay` gắn `match` chưa đảo **0**)*.

⛔ **Final chỉ đổi khi NGƯỜI gõ** *(`/adjust` ⇒ `fls_sua_tay`)*. ⚠ Hôm nay ⛔ màn nào hiện gợi ý để gật *(`GAP-SCR-33`)*.

---

## DT-I09 · Kiểm giá trị ở **CỬA GHI** *(`QĐ-ITL-86`, 2026-09-04)*

> ⛔⛔ **Trước 04/09 cửa ghi ⛔ KHÔNG kiểm gì cả** — kế toán gõ mã hợp đồng
> **bịa ra** cũng vào sổ *như thật*, trong khi máy đã biết đủ **73 mã**.

Nguồn luật: bảng `fls_mapping_master` *(73 mã `hd`)* — và đo được **0** mã `hd`
trong sổ nằm ngoài nó ⇒ bản khai này **có thẩm quyền**, ⛔ **không** phải một
danh sách gợi ý.

| # | Điều kiện | Hành động |
|---|---|---|
| 1 | Giá trị **rỗng** *(mọi trường)* | **Cho qua.** ⚠ Ô rỗng ⛔ không phải giá trị sai — nó là phép **BỎ GÁN**. Chặn nó là cắt mất đường lùi |
| 2 | `hd` có trong `fls_mapping_master` | Cho qua |
| 3 | `hd` ⛔ không có, nhưng **có một mã chỉ khác HOA-THƯỜNG** | `400` **`FLS-UNKNOWN-CODE`**, và lỗi **chỉ ra mã thật**. ⚠ Khoá `hd_code` phân biệt hoa-thường còn `VLOOKUP` của Sheets thì ⛔ không ⇒ người gõ rất dễ gặp đúng chỗ này, và một câu *"⛔ không có mã này"* sẽ làm họ đi tìm một thứ **vẫn đang ở đó** |
| 4 | `hd` ⛔ không có trong danh mục | `400` **`FLS-UNKNOWN-CODE`** — lỗi mang **số mã đang giữ** + **tên lệnh nạp lại**. ⛔ Phép chặn phải nói được **bước tiếp theo**: nếu mã vừa lập bên sổ gốc thì bản khai của FLS đang **cũ** |
| 5 | Danh mục **`0` dòng** | **Cho qua** *(`INV-I17`)* — máy ⛔ **KHÔNG BIẾT**, ⛔ chứ không phải *"mọi mã đều sai"*. ⇒ Màn **phải nói ra** chỗ rỗng ấy ngay cạnh ô gõ |
| 6 | `svc_start`/`svc_end` ⛔ không khớp `^\d{4}(0[1-9]\|1[0-2])$` | `400` **`FLS-BAD-FORMAT`** |
| 7 | Có `force=true` | ⛔ **KHÔNG vượt qua được** hai phép trên. `force` sinh ra cho *"gõ khác nguồn"* — một **bất đồng** giữa hai câu trả lời **đều có thật**; một mã ⛔ không tồn tại thì ⛔ không phải bất đồng, nó là **một cái ⛔ không có** |

⛔⛔ **Ba trường `pay_type` · `cdt1` · `id_payee` ⛔ KHÔNG bị cửa ép** — xem
`INV-I18`: ép một danh sách **suy từ chính dữ liệu của nó** là **vòng tròn**.

## DT-I11 · Khi nào bật bảng báo `KIỂM TRA` *(`QĐ-ITL-88`)*

> ⛔⛔ **Một bảng báo chỉ đáng giá bằng độ HIẾM của nó.** Đo thật: **7.682 /
> 10.030 dòng (76,6%)** đang ở trạng thái `chưa phân loại`. Nếu trạng thái ấy
> kéo theo bảng báo thì màn hình **lúc nào cũng đang kêu**, và khi có chuyện
> **thật** thì ⛔ **không còn nấc nào cao hơn để dùng**.

| # | Điều kiện | Bật bảng? | Vì sao |
|---|---|---|---|
| 1 | `PS Nợ` **và** `PS Có` đều khác 0 | ✅ | Máy ⛔ **không chọn hộ** một vế. Đo hôm nay: **0 dòng** — nhưng một nhánh *"⛔ không xảy ra"* vẫn phải có câu trả lời, ⛔ không được rơi xuống nhánh khác |
| 2 | `period_state = locked` | ✅ | `INV-I13` — ⛔ không ô nào gõ được, **kể cả với `force`** |
| 3 | `LE` ≠ `Pháp nhân thanh toán` **và cả hai thuộc từ vựng CHUNG** | ✅ | `US-032`. ⚠ Điều kiện *"cùng từ vựng"* là **bắt buộc** — xem `DT-I12` |
| 4 | `chưa phân loại` *(ô trống, máy gợi ý)* | ⛔ **KHÔNG** | Trạng thái của **76,6%** cuốn sổ ⇒ **dòng trạng thái** nền nhạt, và nói thẳng *"Việc đang chờ, không phải sự cố"* |
| 5 | `alloc_na` *(phân bổ tra không ra)* | ⛔ **KHÔNG** bật bảng | Đó là một **câu trả lời**, ⛔ không phải lỗi. Nó có **hình riêng** trong khối `PHÂN BỔ` *(viền đứt)* + một dòng trong dòng trạng thái |
| 6 | Nhiều điều kiện 1–3 cùng lúc | ✅ **MỘT** bảng | ⛔ Hai bảng đỏ cạnh nhau thì **cả hai đều nhạt đi** — đúng đường cũ quay lại. Gộp: mỗi việc một dòng `<li>` |

⛔ **Ba việc, và CHỈ ba.** Thêm một dòng vào bảng này là làm mọi dòng khác nhạt
đi ⇒ phải kèm **con số đo được** về tần số.

**Cưỡng chế:** `fls/web/tep/man_f02.js::_viec_kiem` · 5 cổng ở
`tests/web/test_drawer_f02.py`, **cả 5 đã thấy đỏ**.

---

## DT-I12 · So hai cột thì phải hỏi **CÓ SO SÁNH ĐƯỢC KHÔNG** trước *(`QĐ-ITL-89`)*

> ⛔⛔ `US-032` đòi báo khi `LE` lệch `Pháp nhân thanh toán`. Luật hiển nhiên là
> `le != le_payer`. **Đo thật: 1.304 dòng — 13,0%.** Kế toán gặp bảng đỏ **một
> trên tám dòng**.

| Đo | Số |
|---|---|
| `le` — giá trị riêng | **23** |
| `le_payer` — giá trị riêng | **16** |
| Từ vựng **CHUNG** | **12** ⇒ hai tập chỉ trùng **44%** |
| `le_payer` **trống** | **6.688 / 10.030 = 66,7%** |
| Luật `le != le_payer` | **1.304 dòng (13,0%)** |
| …trong đó `le` là giá trị **⛔ không bao giờ** có ở `le_payer` | **1.175 (90%)** |
| ⭐ Luật **thu hẹp** *(cả hai thuộc từ vựng chung)* | **79 dòng (0,8%)** |

`le` chứa `Cash Treasury`, `CN`, `HGO1` — **⛔ không phải mã pháp nhân**. So
chúng với `VGOH` là so **táo với cam**: **1.225 / 1.304** báo là kiểu ấy.

| Nhánh | Làm gì |
|---|---|
| Hai giá trị **khác nhau**, **cả hai** thuộc từ vựng chung | ✅ bật bảng `KIỂM TRA` — hai **mã pháp nhân thật, khác nhau** *(`SGO2` vs `VVOS`)* |
| Hai giá trị khác nhau, **một trong hai ⛔ không** thuộc | ⛔ **không** bật bảng, ⭐ **nhưng NÓI RA**: một dòng ghi chú ngay dưới ô. *"⛔ Không bật bảng báo"* ⛔ **không được** biến thành *"⛔ không nói gì"* — `INV-I16` |
| `le_payer` **trống** *(66,7%)* | ⛔ không so, ⛔ không nói |

⭐⭐ **Đây là phép đo CÓ SO SÁNH ĐƯỢC KHÔNG, ⛔ không phải phép đo ĐÚNG SAI** ⇒
nó ⛔ **không** phạm `INV-I18`: nó ⛔ không dùng dữ liệu để **cưỡng chế** một giá
trị, nó dùng dữ liệu để biết hai ô có cùng **đơn vị đo** hay không.

⚠ **`0,8%` là con số CỦA HÔM NAY** *(`window.FLS_LE_CHUNG`, chụp lúc khởi
động)*. Đổi luật hay nạp thêm dữ liệu thì phải **đo lại**.

⛔ **Còn mở:** `le` chứa `HIEPNV` · `HOATT` · `SONNH` — trông như **tên viết tắt
của người**, ⛔ chưa ai giải thích chúng là gì.

---

## DT-I10 · Số tiền của một dòng sổ *(`QĐ-ITL-83`)*

> ⛔⛔ Sổ gốc điền **CẢ HAI** cột `PS Nợ`/`PS Có`, một cột bằng `0`. Phép đo cũ
> là *"ô nào KHÔNG RỖNG"* — mà `0` thì ⛔ **không rỗng** ⇒ **3.630/10.030 dòng
> (36%)** hiện sai. ⚠ Và nó ⛔ **không nhìn thấy được**: 5.105 dòng còn lại có
> ô **trống thật** nên hiện đúng.

| # | Điều kiện | Hành động |
|---|---|---|
| 1 | `PS Nợ` ⛔ không rỗng **VÀ khác 0** | Số tiền = `PS Nợ`, dấu **dương** *(vào)* |
| 2 | `PS Có` ⛔ không rỗng **VÀ khác 0** | Số tiền = `PS Có`, dấu **âm** *(ra)* |
| 3 | **Cả hai** khác 0 | ⛔ **Máy KHÔNG chọn hộ** — hiện `—` và **nói ra cả hai vế**. ⚠ Đo hôm nay: **0 dòng**; nhưng một nhánh *"hôm nay ⛔ không xảy ra"* vẫn phải có câu trả lời, để rỗng là để nó **chọn hộ trong im lặng** |
| 4 | Cả hai rỗng hay bằng 0 | `—` |


## DT-I01 · Chuẩn hoá pháp nhân (LE)

Nguồn luật: khối `Mapping LE I Legal Entity` — cột `Bank Sheet` → `LE`.

| # | Điều kiện | Hành động |
|---|---|---|
| 1 | `Bank Sheet` khớp chính xác một dòng `MAPPING-MASTER` | Gán `LE` tương ứng |
| 2 | Khớp nhiều dòng | **Dừng**, báo `GAP` — không tự chọn (R-A4) |
| 3 | Không khớp | `LE = unmapped`, dòng vào `unmapped`, đếm được (`INV-I06`) |
| 4 | Giá trị thuộc **danh sách không-phải-pháp-nhân** (vd nhãn tiền tệ `USD`, quỹ `HotBonus`) | `is_entity = false`, **loại khỏi hợp nhất** (`INV-I10`) |

> Nguồn LE rất bẩn (nhiều biến thể tên cho cùng một pháp nhân). Chuẩn hoá **chỉ** qua bảng này — cấm chuẩn hoá bằng chuỗi trong code.

## DT-I02 · Gán mã hạng mục (HD) qua COA

Nguồn luật: khối `Mapping HD via COA` — cột `HD`, `COA1`, `COA2`.

| # | Điều kiện | Hành động |
|---|---|---|
| 1 | Có `HD` từ chuỗi thanh toán P100 (LINK) | Giữ nguyên, **không ghi đè** bằng suy luận COA |
| 2 | Không có `HD`, `Tài khoản` khớp `COA1`/`COA2` | Gán `HD` theo bảng |
| 3 | Không suy được | `needs_input` (`SM-I02`) — vào hàng chờ khối 1 |

## DT-I03 · Phân bổ về CFA2

Nguồn luật: 3 cột thật `Need to Allocate to CFA2` · `Method to Allocate to CFA2` · `Code HR Allocate`. Đây là **mầm của bảng luật L4**.

| # | `Need to Allocate` | `Method` | Hành động |
|---|---|---|---|
| 1 | `No need` | — | `CDT1 CFA2 = CDT1 CFA1`, không rải |
| 2 | có | có method | Áp method tương ứng; sinh dòng phân bổ, **giữ tổng bằng gốc** |
| 3 | có | rỗng | **Dừng**, báo `GAP` — có yêu cầu rải nhưng không có cách rải |
| 4 | có `Code HR Allocate` | — | Dùng nhánh HR (đã rải sẵn tại nguồn H1000 theo HD/KRF), không rải lại |

> Giá trị `No need` quan sát được trong cột `Method to Allocate` (`AW`) của `ITL Ledge`. Danh mục method đầy đủ: `???` — `GAP-ITL-12`, phải liệt kê từ dữ liệu thật trước khi code.

## DT-I04 · Số thứ tự theo pháp nhân (No)

Nguồn luật: khối `Mapping No via LE` — `LE` → `No`. Dùng cho nhãn hiển thị, **không dùng làm khoá** (`INV-I04`).

## DT-I05 · Xử lý ngày chứng từ ⚠

Nợ dữ liệu nặng nhất. Ba tình huống đã đo được ở hệ hiện hành:

| # | Điều kiện | Hành động |
|---|---|---|
| 1 | Ô là kiểu ngày hợp lệ | Nhận |
| 2 | Ô là **chuỗi** | Parse theo định dạng khai báo của nguồn. Không parse được → `rejected`, đếm được (`INV-I11`). *(Đã đo ~5.369 dòng dạng này)* |
| 3 | ~~Nghi **hoán ngày↔tháng**~~ | ⛔ **RÚT LẠI 2026-08-24.** ⛔ **`AUD-12` (owner 2026-08-24): mã `FT<yy><ddd>` KHÔNG mang ý nghĩa thời gian.** Giá trị input trong sheet là **SSOT** ⇒ **không** dùng `Số chứng từ` để suy hay kiểm `Ngày chứng từ`; phát hiện *"93% hoán ngày↔tháng"* **mất căn cứ**, chờ chứng cứ khác. ⇒ **không có phép kiểm ngày nào dựa trên `Số chứng từ`**. Chỉ giữ phép kiểm **kiểu dữ liệu**: ô ngày phải là ngày, không phải chuỗi *(~5.369 dòng)*; lệch → `rejected` + báo, **không tự sửa** (`P-06`) |
| 4 | Đọc từ bản `.xlsx` export | **Cấm.** Chỉ đọc Google Sheets live qua API — bản export chỉ giữ nguyên 2,7% ô ngày |

> Quy tắc 3 chưa được owner phê là cách xử chính thức hay chỉ là cách phát hiện: `GAP-ITL-05`.

## DT-I06 · Khử trùng

| # | Điều kiện | Hành động |
|---|---|---|
| 1 | Hai dòng cùng khoá composite (`INV-I04`) | Giữ 1, ghi lineage cả hai nguồn |
| 2 | Cặp AP/AR (adapter F) đã có giao dịch tiền tương ứng | Không tạo dòng mới — tránh double-count (`INV-I09`) |
| 3 | `Reference number` trùng giữa cash txn và PM | Khớp thành một sự kiện, không cộng đôi |

## DT-I07 · Định tuyến hai làn CFA / PLA

| # | Điều kiện | Làn |
|---|---|---|
| 1 | Có ngày phát sinh tiền | Vào `CFA` theo **ngày tiền** |
| 2 | Có cửa sổ dịch vụ (`Thời điểm bắt đầu/kết thúc sử dụng dịch vụ`) | Vào `PLA` theo **kỳ ghi nhận**, rải theo cửa sổ |
| 3 | Có cả hai | Vào **cả hai làn**, thời điểm khác nhau — **đây không phải lỗi** |
| 4 | `Loại giao dịch = NB \| Lưu chuyển nội bộ` | Chỉ ảnh hưởng số dư, **không vào P&L** |

> Chênh lệch giữa hai làn là **hợp lệ** và phải giải thích được, không được ép khớp (`ORC-03` bẫy IM7).

## DT-I08 · Trường nào tự điền được (cứu 6.843 ô nhập tay)

Xếp hạng theo khối lượng thật để biết code hoá đâu lời nhất:

| Khối | Trường | Ô | Suy được thành luật? | Đường suy đề xuất |
|---|---|---|---|---|
| 7 | `File đính kèm: Hóa đơn` | **3.489** | Rất khả thi | Kéo từ PI/PE theo `ID PILine`/`ID PELine` — link đã tồn tại ở nguồn |
| 6 | `Mã đối tác (ID Payee)` | **1.624** | Khả thi | Tra `Vendor & Channel Mapping` (Platform) + đối tác từ PE/PI |
| 3 | `Chủ dự toán (CDT1)` | **1.210** | Một phần | Từ `HD` + `Tài khoản` qua `MAPPING-MASTER`; phần còn lại cần phán đoán |
| 1 | `Budget Code (HDCode)` | **297** | Một phần | `DT-I02` |
| 2 | `Loại giao dịch (Payment Type)` | **179** | Một phần | Từ chiều tiền (Nợ/Có) + đối ứng nội bộ |
| 4–5 | Ngày bắt đầu/kết thúc dịch vụ | **22 + 22** | Ít | Giữ nhập tay — khối lượng nhỏ, cần phán đoán |

**93% khối lượng nằm ở 3 khối đầu, cả ba đều là tra cứu chứ không phải phán đoán kế toán.** Đây là luận cứ ROI của dự án.

> Mỗi đường suy phải được **chứng minh trên dữ liệu thật** trước khi thành luật: chạy thử, so với giá trị người đã nhập, công bố tỷ lệ khớp. Luật nào khớp < ngưỡng thì để `needs_input`. Ngưỡng: `???` — `GAP-ITL-07`.

## DT-I09 · Nhận diện chuyển nội bộ

| # | Điều kiện | Hành động |
|---|---|---|
| 1 | Hai dòng ngược chiều, cùng số tiền, cùng/kề ngày, hai tài khoản cùng nhóm pháp nhân | Gắn cặp `internal_transfer`, loại khỏi dòng tiền ròng hợp nhất |
| 2 | `Loại giao dịch` đã ghi `NB \| Lưu chuyển nội bộ` | Tin nhãn nguồn, vẫn chạy kiểm tra 1 để tìm vế còn lại |
| 3 | Chỉ tìm được **một vế** | Cảnh báo — vế kia có thể nằm ở nguồn chưa nạp |

## DT-I10 · Bốn loại giao dịch hay bị bỏ sót — DQ test bắt buộc ⚠

Nguồn: `ITL RAW ▸ Check list mapping` — sổ sự cố **do chính kế toán ghi**. 4/7 vấn đề có cùng một giải pháp *"nhập bổ sung lên P100"* ⇒ gốc rễ là **dữ liệu vào P100 không đủ**, không phải lỗi tính ở ITL.

| # | Loại giao dịch hay thiếu | DQ test TO-BE |
|--:|---|---|
| 1 | **Lãi và phí ngân hàng** trả hằng tháng | Mỗi tài khoản × mỗi tháng phải có ≥1 dòng phí/lãi, hoặc giải trình vì sao không |
| 2 | **Điều chuyển nội bộ** — mua bán ngoại tệ, điều chuyển | Cặp nội bộ phải khớp 2 vế (`DT-I09`); một vế lẻ ⇒ cảnh báo |
| 3 | **Chi phí năm cũ thanh toán năm sau** | Dòng có kỳ dịch vụ < kỳ tiền ≥ 12 tháng ⇒ đánh dấu kiểm |
| 4 | **Giao dịch quẹt thẻ** chưa vào PM100 | Giao dịch có dấu hiệu quẹt thẻ mà không có `ID PMLine` ⇒ vào hàng chờ |

Hai vấn đề còn lại chưa có giải pháp trong file (⇒ câu hỏi phỏng vấn `_GUIDE_09` §6 câu 17):
- *"Logic của công thức là đi từ số lượng transaction để quy đổi…"*
- *"Tài khoản đã đóng và các bank ít giao dịch nhưng vẫn tính ng…"*

## Thứ tự áp bắt buộc

```
DT-I05 (ngày)  →  DT-I01 (LE)  →  DT-I06 (khử trùng)  →  DT-I09 (nội bộ)
   →  DT-I02 (HD)  →  DT-I08 (tự điền)  →  DT-I07 (làn)  →  DT-I03 (phân bổ)
```

Đảo thứ tự sinh lỗi thật: chuẩn hoá LE trước khi parse ngày làm hỏng khoá khử trùng; phân bổ trước khi định tuyến làn làm rải nhầm sang dòng không vào P&L.

## GAP của file này

| ID | Câu hỏi | Ai đóng |
|---|---|---|
| `GAP-ITL-12` | Danh mục đầy đủ `Method to Allocate to CFA2` — liệt kê từ dữ liệu thật | BA session + Kế toán trưởng |
| `GAP-ITL-05` | Luật xử ngày hoán: tự phát hiện rồi chặn, hay sửa hàng loạt trước? | Kế toán trưởng + ThanhNC |
| `GAP-ITL-07` | Ngưỡng khớp tối thiểu để một đường suy được phép thành luật tự động | Diễn đàn QT |

## Changelog
- **v0.8** *(2026-10-01 tối, `fls-ba`, `KQ-007`)*: `F-4 ⓐ` đính chính tham chiếu bài ghim nhánh `5a` — ~~`AC-15`~~ ⇒ **`AC-16`** *(`WO-003` vòng 2: ca trộn = `AC-16`; `AC-15` là `bo_qua`)*; `F-1` thêm đoạn *Nhật ký của bản đảo — đọc thế nào* *(luật ghi ⛔ đổi; cách màn đọc ⇒ `BA-06` v4.8)*.
- **v0.7** *(2026-10-01 tối, `fls-ba`, `KQ-005` — `fls-test` TRƯỢT `WO-003 AC-7`)*: ⭐⭐ **`DT-I14` nhánh 7 SAI một vế, rút:** *"bị gợi ý mới hơn đè ⇒ ⛔ làm gì"* làm lớp gợi ý bị đè **⛔ bao giờ đảo** ⇒ bỏ ghép xong nó **nổi lên lại** thành gợi ý mồ côi trên dòng **0** mối nối *(`F-1`, 2/2 kịch bản trên kho TEST)*. Luật mới: bỏ ghép đảo **mọi** bút toán gắn `match` **chưa có bản đảo** — **mọi lớp**; nhánh 7 chỉ còn *"đã có bản đảo"*; nhánh 8 cũng xét mọi lớp. Thêm **bất biến đo được** ⇒ `INV-I22` *(`BA-11` v0.15)*. ⭐ **Định nghĩa `bo_qua`** = chỉ giá trị **người** *(`F-2`; `BA-06:1174` đúng, ⛔ đổi)*. ⭐ **Thêm nhánh `5a` — ca TRỘN** *(một dòng lệnh rỗng ô, dòng kia có `v`)* ⇒ rỗng = **⛔ lên tiếng** ⇒ gợi ý `v` *(`F-3`; đo 01/10: **0/25** dòng ≥ 2 mối nối rơi vào ca này; mã đã làm vậy — chỉ ghim bài)*.
- **v0.6** *(2026-10-01, `fls-ba`, `QĐ-ITL-149` — owner: *"Máy gợi ý"*)*: ⭐⭐ **Thêm `DT-I14` — ô `hd`/`cdt1` sau ghép:** 5 nhánh ghép + 3 nhánh bỏ ghép; **Final chỉ đổi khi người gõ**. Một bảng cho cả ba đường ghép *(tay · lô · máy)* vì cả ba dùng **một** phép suy.
- **v0.5** *(2026-09-18, `QĐ-ITL-144` — owner BA màn hình **cùng kế toán** rồi mang luật về)*: ⭐⭐⭐ **Thêm `DT-I13` — LUẬT GHÉP, và đây là lần ĐẦU dự án có một luật ghép do NGƯỜI LÀM phát biểu.** Trước đó máy ghép theo `reference` ＋ bốn bậc tiền — một thứ tự **tôi suy từ dữ liệu**, ⛔ không ai ký. ⭐ Luật thật có **hai nhánh**: **VN** *(PM code ＋ số tiền ＋ **pháp nhân**)* và **nước ngoài** *(từ khoá nội dung CK ＋ tên vendor ＋ số tiền)*. ⛔⛔ **Đo ngay: một nhánh gần đủ, một nhánh KHÔNG chạy được.** Nhánh VN thiếu `pháp nhân` — cột `le` **rỗng 0/8.387**, nhưng suy được từ `source_sheet`; trở ngại thật là **hai bên gọi cùng một pháp nhân bằng hai mã khác nhau** *(`VVOH - Astronex` ↔ `ASTRONEX`)*. Khớp *mã HOẶC tên* được **3.120/3.772 = 82,7%**; **652 dòng (17,3%) phải hỏi người**, lớn nhất là cặp **`CNC` (522) ↔ `CN` (906)** — giống nhau ⛔ **không phải bằng chứng** *(`INV-I16`)*. ⛔ Nhánh nước ngoài thiếu **cả hai** vế đầu *(`memo` **0/8.387** · `acct` **0/8.387**)* và nó phủ **49%** cuốn sổ ⇒ ⛔ **không một dòng nào** chạy được; gốc là tầng `R |` chỉ có **5 cột**, tức việc **NẠP**, ⛔ không phải việc **GHÉP**. ⚠ Mở `GAP-LE-01` *(bảng bắc cầu pháp nhân)* ＋ `GAP-NAP-04` *(nạp cột diễn giải sao kê)*.
- **v0.4** *(2026-09-04, `QĐ-ITL-88·89`)*: ⭐⭐ Thêm **`DT-I11`** *(khi nào bật bảng báo `KIỂM TRA` — **ba** việc, và **chỉ** ba; `chưa phân loại` **⛔ KHÔNG** thuộc nhóm đó vì nó là trạng thái của **76,6%** cuốn sổ)* và **`DT-I12`** *(so hai cột thì phải hỏi **CÓ SO SÁNH ĐƯỢC KHÔNG** trước — `US-032` viết là `le != le_payer` thì báo trên **13,0%** sổ, mà **90%** trong số đó là so **táo với cam**: hai cột chỉ trùng từ vựng **44%**)*.
- **v0.3** *(2026-09-04, `QĐ-ITL-83·86·87`)*: ⭐ Thêm **`DT-I09`** *(kiểm giá trị ở cửa ghi — 7 nhánh, gồm cả nhánh **rỗng** và nhánh **danh mục `0` dòng**)* và **`DT-I10`** *(số tiền của một dòng sổ: `Nợ`=vào(+) · `Có`=ra(−), và một vế **có tiền** khi nó ⛔ không rỗng **VÀ khác 0**)*. ⛔ Phép đo cũ *"ô nào không rỗng"* làm **3.630/10.030 dòng (36%)** hiện sai, và nó ⛔ **không nhìn thấy được**.
- v0.2 (2026-08-18): Thêm `DT-I10` — 4 loại giao dịch hay bị bỏ sót, dẫn xuất từ sổ sự cố `Check list mapping` (kế toán tự ghi).
- v0.1 (2026-08-18): Khởi tạo — 9 bảng quyết định dẫn xuất từ `Mapping Master` thật; `DT-I08` xếp hạng 7 khối nhập tay theo ROI; chốt thứ tự áp.
