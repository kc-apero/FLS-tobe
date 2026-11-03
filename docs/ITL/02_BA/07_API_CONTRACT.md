# 07 — API CONTRACT: FLS

**Version:** v3.14 · **Ngày:** 2026-10-06 · **Chủ sở hữu:** BA/PO + Tech Lead
**Thay thế:** v0.1 *(bản copy chương trình, prefix `/api/voi/`)* — đã khai tử.

**Căn cứ:** `04_DB_IMPLEMENTATION` v1.0 *(schema `fls_itl`)* · `QĐ-ITL-38` *(app là nơi thao tác)* · `QĐ-ITL-45` *(FLS độc lập)* · `FLS-vs-FPS` §7 *(append-only event-log)*.

---

## §1 · Quy ước chung

- **Prefix:** `/api/fls/v1/` — độc lập, không dùng `/api/voi/` hay `/api/fps/`.
- REST danh từ số nhiều, kebab-case; phân trang cursor `?cursor=&limit=` *(mặc định 50, max 500 — lưới kế toán cần trang lớn hơn cockpit)*.
- **Envelope:** `{data, error, meta}` với `meta = {request_id, run_id, contract_version, as_of, data_status}`.
  - `data_status ∈ {flash, reconciled, signed}` *(`INV-I14` — số chưa chốt luôn mang cờ)*.
- **AuthN/Z:** JWT ngắn hạn **fail-closed**; `actor` lấy **từ token**, không tự khai *(bài học A-CCR)*.
- ⭐⭐ **PHẠM VI ĐỌC — thêm v1.2, và nó là bắt buộc ở mọi đường đọc.** Cửa chỉ trả dòng của **lần nạp THẬT** *(`run_id` khớp `NAP-yyyy-mm-dd-NGUỒN`)*. `?run_id=<id>` hẹp thêm về **một** lần nạp nhưng **giao** với bản trắng chứ ⛔ không thay thế nó ⇒ `?run_id=T-abc` trả **rỗng**, ⛔ không mở được đường ra dấu test. ⛔ **Không có** `?pham_vi=ca_kho` — đọc cả kho là việc của công cụ soi kho, ⛔ không bao giờ của một cửa HTTP. *(Lý do: 27/08 đo được **194 dòng dấu test nằm trong hàng chờ việc của kế toán**; chỗ hỏng không phải "lọc sai" mà là **không gì bắt buộc phải lọc**.)*
- ⭐ **Cửa đọc chạy trên kết nối bị PostgreSQL chặn ghi** *(`SET default_transaction_read_only = on`)*, và máy **từ chối chạy** nếu không ⇒ *"cửa đọc không ghi"* là điều **kho cưỡng chế**, ⛔ không phải một lời hứa trong tài liệu.
- ⛔ **Tiền ra JSON là CHUỖI.** JSON không nói kiểu, nên máy đọc *(JavaScript ở `P6`)* biến mọi số thành `float64` **trước khi ai kịp chọn**.
- ⭐ **`data_status` mặc định `flash`** — ⛔ mặc định KHÔNG được là `reconciled`.
- ⭐ **Ghi = APPEND sự kiện, không UPDATE tại chỗ** — mọi sửa của người là một dòng mới; giá trị hiện tại = sự kiện mới nhất theo `(itl_id, trường)`. Đây là `AUD-1` + `INV-I08`.

---

## §2 · Nhóm ĐỌC — sổ và hàng chờ

> ⭐ **Cột trạng thái v1.2:** ✅ = **đã xây và đã chạy thật qua HTTP** *(`P4`, 27/08 — `tools/verify_cua_that.py`)* · ⬜ = **chưa xây**, phần lớn vì bảng nguồn chưa có dữ liệu. ⛔ Đừng đọc *"P4 xong"* thành *"cửa đọc xong"*: **6 trong 11 đường đọc vẫn ⬜**.

| Method · Path | Trả | Story |
|---|---|---|
| ✅ `GET /api/fls/v1/ledger` | dòng `fls_itl`, lọc `?period=&le=&status=`, phân trang. ⭐⭐ *(v3.14, `KQ-061 F-2`)* năm trường lưới gõ được *(`hd` · `pay_type` · `cdt1` · `svc_start` · `svc_end`)* **giữ** nghĩa **cột nguồn thô** *("sổ gốc nói" — ⛔ đổi trường cũ; `QĐ-ITL-73 ⓔ` *"nguồn nói X, người gõ Y"*)*; **mỗi** trường mang thêm **`<f>_final`** = giá trị bút toán người hiệu lực *(`fls_sua_tay`, có giá trị)*, ⛔ có thì cột nguồn, ⛔ có nữa `null` — **cùng luật** `BA-05` **v0.35** `DD-I15 ⓓf` *(gợi ý máy `fls_may_goi_y` / `*_thyt` **⛔ bao giờ** — `QĐ-ITL-149`)* — và **`<f>_nguon`** ∈ {`sua_tay`, `nguon`, `UNMAPPED`} *(chuỗi = hằng `ghi_tay.NGUON_TAY` / `NGUON_SO` / `NGUON_TRONG`)*. Lưới `F02` in `<f>_final` *(`BA-06` **v4.24** §3c ⑪)*. Trường **thêm** ⇒ mười tên khai **một hằng** như `TRUONG_ALLOC` *(cổng `kiem_bang_cot` hai chiều)*; tuyến **đọc thêm** `fls_sua_tay` ⇒ khai lại `bang_tuyen.py` *(cổng `soi_bang_tuyen`)*. Đo 06/10 sổ thật *(`EXPLAIN ANALYZE`, chỉ đọc)*: trang **501** dòng với năm `LEFT JOIN fls_sua_tay` = **3,28 ms** *(`fls_sua_tay` hôm nay **0** dòng hiệu lực / **4.428** bút toán — số lớn lên theo người sửa ⇒ `WO-062` đo trên kho TEST có bút toán)*. Vì sao ⛔ thay nghĩa `hd` thành Final: drawer *(`GET /ledger/{itl_id}`)* và hộp `US-025` cần **cả hai** giá trị, và `doc_mot_dong` đã khai *"⛔ trộn vào các cột nguồn"* *(`doc_bao_cao.py:457-459`)* — hai cửa mà `hd` hai nghĩa là hai sự thật | E1/E2 |
| ✅ `GET /api/fls/v1/ledger/{itl_id}` | một dòng + 36 canonical + lineage. ⭐ *(v3.6, `KQ-025 F-4`)* mỗi phần tử `but_toan[]` mang thêm **`nguon`** *(`fls_adjustment.nguon`: `sua_tay` · `may_goi_y`)* — hộp `Đảo` cần nó để nói đúng hậu quả *(gợi ý máy ⛔ đổi Final)*; trường **thêm**, ⛔ đổi trường cũ | drill |
| ✅ `GET /api/fls/v1/queue` | ⭐ **hàng chờ**: chỉ `work_status='UNMAPPED'`, **xếp theo tiền giảm TRONG TỪNG tiền tệ** + `hang` + `luy_ke_pct`; `?curr=` `?den_pct=90` *("xem tới đây là phủ 90% tiền")*. ⛔ **Bỏ *"nhãn máy dán"*** — `QĐ-ITL-56`/`58`: không có quy định nào để máy dán. ⛔⛔ Phép xếp nằm **TRONG** câu có phạm vi, ⛔ không phải một khung xem lọc ở đầu ra *(`CR#4`)* | `US-039` |
| ✅ `GET /api/fls/v1/queue/summary` | ⭐ số dòng + Σ tiền hàng chờ **theo TỪNG tiền tệ**. ⛔ **Không có dòng "tổng"** — cộng hai tiền tệ ra một con số là đúng cái sai đã tạo ra *"310 dòng phủ 90% tiền"* | `US-039` |
| ⭐ `GET /api/fls/v1/queue/lenh-cho/ro?ro=` | ⭐⭐ **cửa của `SCR-F01`** — dòng lệnh chờ **của MỘT rổ** *(`may`/`nguoi`/`khong`)*, `?tu_chung=1` thu hẹp rổ `may` về nhóm tự chứng. ⛔⛔ **Cửa này PHẢI trả `vi_sao` cho rổ `khong`** — một rổ *"⛔ không ai trả lời được"* mà ⛔ không nói vì sao thì kế toán tìm **mãi mãi** *(`US-053`)* | `US-053/054` |
| ⭐⭐ `GET /api/fls/v1/queue/lenh-da-gan` | ⭐⭐⭐ **cửa của `SCR-F01` — dòng lệnh chi ĐÃ tìm được tiền.** ⛔⛔ Trước nó, `/queue/lenh-cho` lọc cứng `NOT EXISTS (fls_moi_noi)` nên hệ ⛔ **không có đường nào** hỏi *"lệnh chi nào ĐÃ có tiền"* — và cả nửa *"đã gán"* của màn ghép **chết theo dây chuyền**. Mỗi dòng mang `itl_da_gan[]` ⭐ **một DANH SÁCH**: đo `22/09`, **`23/2.219` = `1,0%`** lệnh gắn **nhiều hơn một** dòng tiền. Hai rổ **khép về tổng**: `2.219` ＋ `1.553` = **`3.772`** | `GAP-API-08` |
| ⭐ `GET /api/fls/v1/queue/lenh-cho/summary` | ⭐ đếm **toàn bộ** theo rổ + `tong`, ⛔ **KHÔNG** đếm trên trang đang xem — một trang là `50`–`500` dòng và thứ tự là `(tiền tệ, hạng)` nên nó ⛔ **không** phải mẫu ngẫu nhiên | `US-053` |
| ⬜ `GET /api/fls/v1/queue/loi-nguon` | ⭐⭐ **rổ SỬA NGUỒN** *(mới `CR#12`)* — dòng có khuyết tật **của bảng tính nguồn**, ⛔ không phải việc ghép: ô số chứng từ giữ một **trạng thái** *(`166` dòng `Reject`)*, ô tiền tệ giữ một **con số** *(`1` dòng `20`)*. ⛔ FLS **chỉ mặt**, ⛔ không tự chữa *(`INV-I16`)* — nhưng phải có **cửa để GỬI danh sách**, vì *chỉ mặt* mà ⛔ không có **người nhận việc** thì bằng ⛔ không *(đo: `BA-12` chỉ mặt `11/09`, `18/09` lỗi ấy vẫn đứng dòng `#1`)* | `CR#12` |
| ⬜ `GET /api/fls/v1/queue/coverage` | độ phủ *(mỗi nhóm × ngày đã có người ghi chưa)* | `US-038` |
| ✅ `GET /api/fls/v1/gates` | ⛔⛔ **KHÔNG BAO GIỜ toàn xanh.** Trả cổng **đo được từ kho** *(`KHO_SACH` · `SIGMA_MOI_NOI` · `RUN_DEM_KHOP`)* **cộng** 4 cổng kế toán + `BON_DUONG` khai **tường minh** là `dat=null` = **CHƯA ĐO ĐƯỢC** kèm lý do. Một màn *"4/4 cổng xanh"* trong khi 4 cổng kế toán chưa hề đo là con số nói dối thô nhất của cả hệ. ⛔ Kiểu cưỡng chế: `dat=true` mà không nói **đã đo được gì** là **lỗi lập trình**, nổ ngay | `US-008/029` |
| ✅ `GET /api/fls/v1/journal?itl_id=` | nhật ký 7 trường của một dòng. ⭐ *(v3.6, `KQ-025 F-3`)* mỗi dòng mang thêm **`la_ban_dao`** *(boolean)* = **có** một `fls_adjustment` cùng `(itl_id, field, at, actor)` với `reversal_of IS NOT NULL` — `fls_journal` ⛔ có cột trỏ bút toán, và `_them` chèn hai dòng **trong một giao dịch** nên `at` trùng. Màn dùng nó để ⛔ in bản đảo giống một cú xoá ô *(`BA-06` v4.12)*. Đo sổ thật 02/10 khuya *(chỉ `SELECT`)*: **4.428** dòng nhật ký, ⛔ nối được **0**, khoá vừa trúng bản đảo vừa trúng bút toán thường **0**, `la_ban_dao` đúng **2**. Tuyến nay **đọc thêm** `fls_adjustment` ⇒ khai lại ở `bang_tuyen.py` *(cổng `soi_bang_tuyen`)*. ⛔ Migration *(cột `adj_id` trong `fls_journal`)* — phiếu riêng nếu phép nối theo khoá bị phá. ⭐ **`GAP-API-12`** *(v3.13, nợ — `BG-057` mục yếu 2)*: phép nối đứng trên `at` **trùng** = `now()` của **một** giao dịch; ⛔ ràng buộc máy nào canh điều ấy *(một đường ghi tương lai chèn hai bảng ở **hai** giao dịch, hay dùng `clock_timestamp()`, làm cờ **sai lặng** — bản đảo lại in như cú xoá ô)*. Hôm nay **4** đường gọi `_them` đều chèn cùng giao dịch *(`BG-057`)*; sổ thật nhập nhằng **0**, ⛔ nối được **0** / **4.428**. Lật thành phiếu khi: một đường ghi mới chèn `fls_journal`/`fls_adjustment` ngoài `_them`, **hoặc** được phép migration `adj_id` *(lúc ấy bỏ hẳn phép nối theo giờ)* | `US-030` |
| ⬜ `GET /api/fls/v1/weekly` | tổng quan tuần *(kế toán tự xem → nút "Xuất PDF" ở `SCR-F03`)* | `US-034/043` |
| ⬜ `GET /api/fls/v1/sources` | ⭐ **F06** — manifest nguồn: trạng thái·độ trễ·cut-off·#giao dịch *(đọc `fls_source`)* | `US-001` |
| ⬜ `GET /api/fls/v1/mapping-master` | ⭐ **F06** — danh mục HD→phân bổ + cảnh báo mã trùng *(đọc `fls_mapping_master`)* | `US-018` |
| ⬜ `GET /api/fls/v1/le` | ⭐ **F06** — danh mục pháp nhân + `is_entity` *(đọc `fls_le`)* | `US-031` |
| ⬜ `GET /api/fls/v1/queue/state?itl_id=` | ⭐ trạng thái hàng chờ *(lý do·hoãn·defer_count — đọc view `fls_queue_state`)* | `US-040/045` |

---

## §3 · Nhóm GHI — chỉ append, chỉ vùng người gõ

⛔⛔ **SỬA v1.3 — câu *"trường hợp-đồng cập nhật `*_thyt`"* của v1.1/v1.2 là SAI** *(`CR#5`)*. Làm đúng câu đó thì sai **hai** luật cùng lúc: ⓐ `INV-I08` — `fls_itl` là **append-only**, một câu `UPDATE` là một đường xoá lịch sử *(trigger `INV-I03` chặn sẵn)* · ⓑ `QĐ-ITL-35` — `*_thyt` là **cột ĐO PARITY**; ghi giá trị **người gõ** vào đó là **bỏ bàn tay vào cái thước**: từ đó ⛔ không ai phân biệt được *"máy suy đúng"* với *"người đã sửa"*.

⭐ **Đường đúng:** giá trị người gõ sống trong `fls_adjustment` *(**thêm** dòng)*; *"giá trị hiện tại"* là một **phép tính** — khung xem **`fls_sua_tay`** *(bút toán mới nhất của mỗi ô, trừ các bút toán đã bị đảo — migration `0010`)*. ⇒ **Không một ô nào của `fls_itl` đổi** sau bất kỳ phép ghi nào, và màn hình nói được **cả hai**: *"nguồn nói X, người gõ Y"*.

⭐ **`actor` đến TỪ THẺ.** Gửi `actor` trong thân yêu cầu ⇒ **`400`**, ⛔ không âm thầm bỏ qua *(một cái nút gửi `actor` rồi thấy nó bị bỏ qua là một kỳ vọng sai đã hình thành)*.

⭐ **Bút toán + nhật ký trong MỘT giao dịch**, và **một CHỖ DUY NHẤT** trong mã nguồn được ghi vào `fls_adjustment`/`fls_journal`/`fls_queue_event` *(cưỡng chế bằng cổng quét mã nguồn)*.

⛔ **Chỉ ghi vào vùng kế toán sửa: 7 khối Final + phân bổ + cột lý do.** Không endpoint nào ghi vào canonical hay lineage. ⭐ **Trong 7 khối, chỉ 5 khối vào hợp đồng P&L** *(`hd·pay_type·cdt1·svc_start·svc_end` — có `*_thyt`/parity)*; khối ⑥⑦ + phân bổ sửa được nhưng **ngoài P&L** *(`QĐ-owner-0824`)*.

| Method · Path | Thân | Hiệu lực |
|---|---|---|
| ✅ `GET /api/fls/v1/ledger/{itl_id}/fields/{field}` | — | ⭐ v1.3 — *"nguồn đang nói gì"*: giá trị đang có + **nó đến TỪ ĐÂU** *(`nguon` / `may_goi_y` / `sua_tay` / `UNMAPPED`)*. Màn hình gọi **trước** khi cho người gõ, để câu hỏi *"ghi đè không?"* có nội dung *(`US-025`)* |
| ✅ `POST /api/fls/v1/ledger/{itl_id}/adjust` | `{field, value, reason}` — `field ∈` **hợp đồng** `{hd,pay_type,cdt1,svc_start,svc_end}` **∪ ngoài hợp đồng** `{id_payee,invoice}`. ⛔⛔ **HẸP 2026-08-28 (`QĐ-ITL-64`): 10 → 7 tên** — bỏ `cdt1_cfa1`/`cdt1_cfa2`/`alloc_method` vì owner trả lời *"họ ko sửa"*, và 3 ô đó là **CÔNG THỨC** *(tra `Mapping Master` K/L theo `hd`)*. Gõ một trong ba tên ấy ⇒ **`400`**. ⛔ **Bản TRẮNG 7 tên** — tên trường đi vào câu SQL nên tên lạ là **`400`** | append `fls_adjustment` + `fls_journal` **trong một giao dịch**; ⛔ **không sửa `fls_itl`** *(xem đầu §3 — `CR#5`)*. ⚠ **KÊU nếu nguồn/gợi ý máy có giá trị khác** *(`US-025`)* → `409` **kèm `error.khac` nói nguồn đang là gì** + `?force=true` với `reason` **bắt buộc**. ⛔ **Kỳ đã chốt ⇒ `409` KỂ CẢ có `force`** *(`INV-I13`: `force` là để ghi đè **nguồn**, ⛔ không phải để mở một kỳ đã chốt)*. ⭐ Gõ **lại cùng giá trị** ⇒ `da_co=true`, ⛔ **không** thêm bút toán thứ hai *(một cái nút bấm hai lần ⛔ không được thành hai bút toán; đổi lại: một lần **cố ý xác nhận lại** cũng ⛔ không vào sổ — khai ra chứ không giấu)*. Override phân bổ tay ⇒ **máy chạy lại KHÔNG đè**. ⭐⭐ **KIỂM GIÁ TRỊ, thêm 2026-09-04 (`QĐ-ITL-86`)** — trước đó đường này ⛔ **không kiểm gì cả**: `hd` ngoài `Mapping Master` ⇒ **`400 FLS-UNKNOWN-CODE`**; `svc_start`/`svc_end` sai khuôn `YYYYMM` ⇒ **`400 FLS-BAD-FORMAT`**; ⛔ `force` ⛔ **không** vượt qua được cả hai *(nó chỉ để ghi đè một **bất đồng**, ⛔ không phải để tạo một giá trị **⛔ không tồn tại**)*; ⭐ giá trị **rỗng** luôn đi qua *(đó là phép **BỎ GÁN**)*; ⭐ danh mục **`0` dòng** ⇒ ⛔ **không chặn** *(`INV-I17` — máy ⛔ KHÔNG BIẾT, ⛔ chứ không phải mọi mã đều sai)*. ⛔ Ba trường `pay_type`/`cdt1`/`id_payee` ⛔ **KHÔNG** bị ép *(`INV-I18` — ép một danh sách suy từ chính dữ liệu của nó là **vòng tròn**)*. ⇒ Đường này nay **đọc** thêm bảng `fls_mapping_master`, và bảng tuyến đã khai *(cổng `soi_bang_tuyen` bắt được chỗ thiếu khai — `QĐ-ITL-79`)* |
| ✅ `POST /api/fls/v1/adjustments/{adj_id}/reverse` | `{reason}` | ⭐ v1.3 — **đảo bút toán = THÊM một dòng** có `reversal_of` *(`SM-I03`)*. ⛔ **Không** đổi `state` của dòng cũ: đổi trạng thái tại chỗ thì sổ nhật ký không còn là sổ nhật ký. Sau khi đảo, giá trị hiệu lực **tự lùi** về bút toán trước đó — hay về **giá trị nguồn** nếu không còn bút toán nào. ⛔ Đảo hai lần cùng một bút toán, hay đảo một **bản đảo**: bị chặn |
| ✅ `POST /api/fls/v1/queue/{itl_id}/reason` | `{reason}` | cột lý do của hàng chờ *(`US-039`)*; **đây là cột `US-045` đếm** |
| ✅ `POST /api/fls/v1/queue/{itl_id}/defer` | `{until, reason}` | hoãn có hạn *(`US-040`)*; ⛔ **`until` bắt buộc** — hoãn vô hạn là **bỏ qua**, không phải hoãn. Trả `so_lan_hoan` + `doi_mau` để màn hình tự đổi màu từ lần thứ 3; ⛔ **không leo cấp và ⛔ không chặn lần thứ 4** *(`QĐ-ITL-24`: luồng này không có cấp trên — chặn lại là dùng một bộ máy không có người thứ hai để xử lý)* |
| ✅ `GET /api/fls/v1/queue/{itl_id}/pm-candidates` | `?limit=` | ⭐⭐ **ghép lệnh** *(`OP-02`, `QĐ-ITL-48`)* — đọc từ **ảnh chụp `fls_pm_line`** *(`QĐ-ITL-61`, migration `0011`)*, ⛔ **không** đọc `fps_*` sống. Xếp theo **4 BẬC CÓ TÊN**: `ma` *(reference khớp — chip xanh)* › `tien` *(cùng tiền tệ + tiền bằng đúng)* › `gan_tien` *(lệch ≤ dung sai của tiền tệ đó)* › `cung_tien_te`. ⛔ **Không** một điểm số mờ 0..1: màn hình phải nói được **vì sao** phiếu này đứng đầu. ⭐ Trả kèm `anh_chup{run_id, so_dong, doc_luc_muon_nhat}` — **TUỔI của bản lưu**, và `khong_xep_duoc_theo: ["ngay","payee"]` + `vi_sao`. ⛔ Dòng `Reject` / `status` rỗng **VẪN hiện**, kèm `canh_bao` — ẩn đi là **mặc định im lặng** *(`INV-I16`)* |
| ✅ `POST /api/fls/v1/queue/{itl_id}/match` | `{pm_line_ids: [...], reason?}` `?force=` — ⭐ **v3.4 (`QĐ-ITL-149`): `reason` TUỲ Ý** *(xem `§4h ⓼`)* | ⭐⭐ **ghép = THÊM.** ⛔⛔ Thân **⛔ KHÔNG phải `{pm_id}`** *(một phiếu)* — xem `CR#6`: 526 phiếu mang 2–36 reference khác nhau, nên ghép vào phiếu thì **máy phải tự chọn dòng** = máy quyết thay người *(`INV-I16`)*. Gửi `{pm_id}` ⇒ **400 kèm lý do**. Ghi trong **MỘT giao dịch**: `fls_pm_link` *(`hinh='T'`, ⭐ **`run_pm` = ảnh PM đã dùng** — `BA-05 DD-I15 ⓒ`, migration `0024`)* + `fls_queue_event` + bút toán `hd`/`cdt1` **suy từ dòng lệnh**. ⭐⭐ **v3.4 (`QĐ-ITL-149`, owner 01/10: *"Máy gợi ý"*): bút toán suy là **GỢI Ý CỦA MÁY**, ⛔ **không** phải người chốt** — `nguon='may_goi_y'`, vào `fls_may_goi_y`, ⛔ vào `fls_sua_tay`; **Final của ô ⛔ đổi** *(luật đầy đủ: `BA-05 DD-I15 ⓓd`, bảng quyết định `BA-10 DT-I14`)*. ⛔ **`fls_itl` không đổi một ô** *(`INV-I08`)*. ★ `hd`/`cdt1` chỉ được suy khi **cả N dòng lệnh ĐỒNG Ý**; N dòng nói N thứ ⇒ trả `khong_suy_duoc` *(`INV-I16`)*, ⛔ không lấy dòng đầu tiên. ⛔ Bảy chỗ từ chối: ngoài phạm vi `404` · kỳ chốt `409` *(⛔ kể cả `force`)* · **đã ghép `409`** kèm mối nối đang có · mã dòng lệnh không có trong **ảnh chụp lệnh chi ĐANG HIỆU LỰC** của phạm vi `400` *(⚠ sửa v3.4 — `KQ-002 F-6`: câu cũ *"ảnh chụp **của chính lần nạp đó**"* già hơn `QĐ-ITL-119` 09/09; mã dùng `anh_pm_hieu_luc()` — `ghi_tay.py:587`, và UAT 01/10 ghép dòng tiền `run_id` `NAP-2026-09-10-RTANG24037` với ảnh `NAP-2026-10-01-PM0BE98A9F`)* · **tiền tệ khác `422`** *(kiểm TRƯỚC Σ)* · **`Σ` lệch `422`** kèm ba con số, giữ `UNMAPPED` *(⛔ không chia bừa)* · `status` không phải `Approve` `422` *(trừ `force`, và `force` để lại vết)* |

✅ **Hai đường trên đã MỞ 27/08** *(`QĐ-ITL-61` — owner chốt lưu ảnh chụp dòng lệnh vào kho)*. Chạy thật trên **sổ thật**: `/pm-candidates` đo trên **25 dòng hàng chờ**, ảnh chụp **3.703 dòng lệnh · 1.468 phiếu**. ⛔ Nhưng đọc kỹ **giới hạn** mới: xếp ứng viên **⛔ không có trục `ngày` và `payee`** — ảnh chụp cố ý ⛔ không mang PII và ⛔ không mang ngày *(`GAP-JOIN-04`)*. Và **⛔ chưa có đường BỎ mối nối**: ghép sai thì hiện chưa sửa được *(`GAP-JOIN-05`)*.

⛔⛔ **Không có** `PUT`/`DELETE` trên `fls_itl` — và từ v1.3 luật này mạnh hơn: ⛔ **không tuyến nào, DÙ PHƯƠNG THỨC GÌ, được GHI vào `fls_itl`**. Mỗi tuyến khai tường minh **bảng nào nó ghi**, và cổng quét bảng tuyến chặn `fls_itl` ở mọi phương thức. *(Luật cũ chỉ kiểm `PUT`/`DELETE`/`PATCH` — nên một `POST .../adjust` ghi thẳng vào sổ sẽ **đi qua trong im lặng**, đúng cái đặc tả v1.1 từng mở đường cho. Cổng chung **#12**.)*

⭐⭐ **Và cửa GHI ⛔ không làm yếu cửa ĐỌC:** **bảng tuyến** chọn kết nối, ⛔ không phải hàm xử lý chọn. Mọi tuyến `GET` **luôn** chạy trên kết nối bị PostgreSQL **chặn ghi**, kể cả khi máy đang mở nhóm ghi *(đo bằng cách đếm số lần mở kết nối ghi = **0** sau bốn đường `GET`)*. Máy mặc định chạy ở chế độ **CHỈ ĐỌC**: mọi đường ghi trả `405` cho tới khi có `--cho-ghi` tường minh.

---

## §4 · Nhóm CHẠY — máy quét & pipeline

> ⛔⛔ **CẢ BA đường dưới ⛔ CHƯA TỒN TẠI, và trước 09/09 chúng nằm TRƠN trong bảng này.** `§2`/`§3`/`§4b` đều dùng `✅`/`⬜` đúng luật, riêng `§4` thì ⛔ không — nên một người đọc hợp đồng sẽ **tưởng `POST /runs` là cửa đã có** rồi đi gọi nó. ⇒ Đánh dấu `⬜`, và cổng `test_ba07_phu_het_tuyen` nay **canh cả chiều này**.
>
> ⚠ Lằn này thuộc `IM0` *(pipeline adapter → canonical → sổ)*. Việc **đang** làm cùng vai là **`§4b`/`§4f`** *(nạp từ ảnh chụp)* — hai lằn khác nhau, ⛔ đừng đọc lẫn.

| Method · Path | Vai | Có? |
|---|---|:--:|
| `POST /api/fls/v1/runs` | chạy adapter → canonical → sổ; trả `run_id` + biên bản `ACC-1…4` | ⬜ |
| `GET /api/fls/v1/runs/{run_id}` | trạng thái + kết quả 4 bất biến; `ACC` fail ⇒ `dq_failed` | ⬜ |
| `GET /api/fls/v1/runs/{run_id}/parity` | biên bản đối chiếu G2/G3 — **chênh liệt kê từng dòng**, ⛔ không phần trăm | ⬜ |

---

## §4b · ⭐⭐⭐ Nhóm NẠP — cửa vào của khuôn *(mới 2026-09-07, `CR#11`)*

> ⛔⛔ **Hôm nay nhóm này ⛔ KHÔNG TỒN TẠI.** Đo được: **0/17** tuyến là cửa nạp — 8 `GET` + 9 `POST`, và **mọi `POST` đều SỬA một dòng ĐÃ CÓ**. Đường duy nhất đưa dữ liệu vào kho là `tools/nap_that.py`, **một lệnh dòng lệnh đọc Google Sheets**. ⇒ Bỏ Google Sheets mà ⛔ không dựng nhóm này thì **⛔ không còn đường nào vào**.

### ⓵ Ba tuyến

| Method · Path | Vai |
|---|---|
| `POST /api/fls/v1/sources/{source_id}/khai-cot` | ghi **bản khai ánh xạ cột** — sinh `version` **MỚI**, ⛔ không sửa khai cũ *(`DD-I10`)* |
| `POST /api/fls/v1/nap/xem-truoc` | ⭐ **SOÁT mà ⛔ KHÔNG GHI** — trả biên bản **9 luật** `S1`…`S10` *(sửa 08/09: `S9` số dư — **chỉ lằn quỹ**; `S10` **hai bản khai phải trỏ cùng một cột** — `GAP-KHAI-01`)* |
| `POST /api/fls/v1/nap` | nạp thật → trả `run_id` + **cùng biên bản ấy** |

⛔ **⛔ Không có `PUT`, ⛔ không có `DELETE`.** Sổ chỉ-thêm *(`INV-I08`)* — nạp nhầm thì **nạp bản đúng rồi đảo**, ⛔ không xoá.

### ⓶ ⭐⭐ Vì sao XEM TRƯỚC là một tuyến RIÊNG, ⛔ không phải một cờ

Vì **hai việc khác nhau về hậu quả** thì ⛔ **không được khác nhau bằng một chữ trong thân yêu cầu**. Một cờ `?that=true` gõ thiếu là **ghi thật khi định thử**. Hai đường riêng thì gõ nhầm đường **⛔ không mất gì** — nó chỉ soát.

⭐ Và đây chính là thứ chặng `Run` của trang tính ⛔ **không có**: hôm nay kế toán dán vào ô rồi **mong** công thức chạy đúng; ⛔ không có bước nào nói *"lô này có sạch không"* **trước khi** nó vào sổ.

### ⓷ Biên bản soát — cả hai tuyến trả CÙNG một khuôn

```json
{ "so_dong_vao": 8341, "so_dong_ra": 8338, "rong": 3, "loi": 0,
  "luat": [ { "ten": "S1 · ba đường cân", "hang": "CHAN",
              "dat": true, "da_do": 60, "thong_diep": "…" } ],
  "chan": [], "co": ["S2 · 7/8338 dòng có tiền mà ⛔ không có mã"] }
```

⛔ **`da_do` ⛔ không được vắng mặt.** Luật nền của cả hai cổng: **đo được `0` thứ ⇒ ⛔ KHÔNG ĐẠT**. Một biên bản chỉ nói *"đạt"* mà ⛔ không nói **đã đo bao nhiêu** là một biên bản **⛔ không đọc được**.

### ⓸ ⭐⭐ Ba hạng quyết định HTTP — và hạng `CỜ` ⛔ KHÔNG chặn

| Hạng | Nghĩa | HTTP | Ghi vào sổ? |
|---|---|:--:|---|
| **`CHẶN`** | **lỗi của FLS** — dòng rơi im lặng | **422** `FLS-SOAT-CHAN` | ⛔ **KHÔNG một dòng nào** |
| **`CỜ`** | khuyết tật **có sẵn trong sổ kế toán** | **201** | ⭐ **CÓ** — và dòng bị cờ vào **hàng chờ có lý do** |
| **`CANH`** | hiện sạch, guard | **201** | có |

⛔⛔ **Hạng `CỜ` trả `201` ⛔ KHÔNG phải nới lỏng.** Chặn ở đây nghĩa là FLS **⛔ không bao giờ nạp được gì** *(đo sống: **5/9** luật đang cờ — `S2`·`S3`·`S4`·`S7`·`S8`; `CHẶN` = `S1`·`S10`; `CẢNH` = `S5`·`S6`)*, và những dòng ấy là **TIỀN THẬT** — vứt chúng là vi phạm ***"⛔ 0 dòng rơi im lặng"***. Biên bản **vẫn ghi đỏ**, và số cờ **phải hiện trên màn** *(`SCR-F04`)*.

### ⓹ Nạp hai lần ⇒ ⛔ KHÔNG nhân đôi — và cơ chế ĐÃ có sẵn

`fls_itl.content_key` là `NOT NULL` **từ migration `0001`**. ⇒ Cùng một tệp nạp lại: khoá trùng ⇒ dòng **bị bỏ qua có đếm**, biên bản ghi `trung: N`. ⛔ **Không** dựng cơ chế chống trùng thứ hai — hai cơ chế chống trùng là hai chỗ để chúng lệch nhau.

### ⓹b · ⭐⭐ `S10` — luật ⛔ KHÔNG nhìn vào dữ liệu *(thêm 08/09)*

Hệ có **HAI** bản khai cho cùng một phép ánh xạ: **dòng 1** của sheet `R |` *(FLS đọc)* và `Range_Condition/Debit/Credit` ở `BankAccountList`/`Cash Ledger List` *(**script `Run` của trang tính** đọc)*. Quét mã ngày 08/09: **0 tham chiếu `Range_`** ⇒ bản khai mà **chính cái máy đang chạy** dùng thì FLS **⛔ chưa từng đọc**.

⛔⛔ **Lệch ở đây nguy một cách IM LẶNG.** Sửa dòng 1 mà quên danh mục *(hoặc ngược lại)* thì FLS và trang tính **đọc hai cột khác nhau**, và **cả hai vẫn chạy bình thường**: ⛔ không câu lệnh nào lỗi · ⛔ không dòng nào rơi *(`S1` **vẫn cân**)* · số tổng vẫn **trông hợp lý**. ⇒ Lớp khuyết tật này ⛔ **không phép kiểm nào trên MỘT phía bắt được**.

| | |
|---|---|
| Hạng | **`CHẶN`** — lệch hai bản khai nghĩa là **FLS đang đọc sai cột**, tức **lỗi của FLS** |
| ⛔ Chưa thu dải | cũng **`CHẶN`**, và **cố ý**: ⛔ chưa thu ⇒ ⛔ **không biết FLS có đang đọc đúng cột ⛔ không**, mà đọc nhầm cột là **sai tiền**. Thông báo nói thẳng **chạy lệnh nào** |
| Ô ⛔ không suy được | đếm là **CHƯA ĐO**, ⛔ **không** đếm là *khớp* *(đo 08/09: **6 ô `Range_*` RỖNG**)*. Cộng chúng vào vế khớp là **tự cho điểm trên tập rỗng** |
| Ở cửa vs ở công cụ | cửa so được **một** nguồn; `tools/nap_nguon_dai.py` so **cả 68** — và nó bắt được thứ cửa ⛔ không thấy: một nguồn **⛔ chưa ai nạp lần nào** vẫn có thể đã lệch |

⭐ Chạy thật 08/09: **192 phép so, `0` lệch / 66 nguồn**.

### ⓺ Bốn mã lỗi mới

| Mã | Khi | HTTP |
|---|---|:--:|
| `FLS-KHAI-KHONG-CO` | nguồn **⛔ chưa có bản khai nào** ⇒ ⛔ **không đoán cột** *(`DD-I10`)* | 409 |
| `FLS-KHAI-THIEU` | bản khai thiếu trường trong 6 ⇒ **NỔ TO**, ⛔ không nạp một phần | 422 |
| `FLS-SOAT-CHAN` | có luật hạng **`CHẶN`** đỏ ⇒ ⛔ **không ghi dòng nào** | 422 |
| `FLS-NGUON-LA` | `source_id` ⛔ không có trong `fls_source` | 404 |

⚠ `FLS-KHAI-KHONG-CO` là **409 ⛔ không phải 404**: nguồn **có tồn tại**, chỉ là **chưa ai khai cách đọc nó**. Hai câu trả lời khác nhau dẫn người dùng đi hai đường sửa khác nhau.

---

## §4c · ⭐⭐⭐ Nhóm ẢNH CHỤP — chỗ ở của vùng CHUẨN *(mới 2026-09-08, `QĐ-ITL-110`)*

> ⛔⛔ **Nhóm NẠP §4b ⛔ KHÔNG CÓ ĐƯỜNG VÀO, và điều đó chỉ lộ ra khi soi màn `F04`.** Cả `POST /nap/xem-truoc` và `POST /nap` đòi người gọi **đưa sẵn `dong`** vào thân yêu cầu; lý do viết trong chính mã nguồn là *"đọc `.xlsx`/`.csv` là việc của **màn hình** — nó đã cầm tệp trong tay người dùng"*. Câu ấy đứng trên **`QĐ-ITL-105` ⓷** *(đường vào = **TẢI TỆP** + khai cột)*, mà **`QĐ-ITL-109` đã lật đúng mô hình đó**: `F04` ⛔ **không có một ô nhập nào**, cử chỉ dán **ở lại Google Sheets**. ⇒ Trình duyệt ⛔ không đọc được Sheets, cửa thì ⛔ không tự đọc — **⛔ không có đường nào đưa `dong` vào**.
>
> ⭐ **Owner chốt `QĐ-ITL-110`: phép đọc 60 sheet ĐI QUA MỘT ẢNH CHỤP TRONG KHO**, ⛔ không đọc Sheets sống trong cửa.

### ⓵ Vì sao ảnh chụp — và ⛔ KHÔNG phải vì tốc độ

⚠⚠ **Lập luận đầu tiên tôi đưa ra là SAI — ghi lại làm bia.** Tôi dẫn `GAP-API-04` *("nguồn chập chờn, **timeout 3/3**")* để chống đường đọc sống. Phép đo ấy chạy trên workbook **`ADJUSTED`** — đầy `IMPORTRANGE`. Đo **chính nguồn `R \|`** ngày 08/09: liệt kê sheet **1,8 s** + đọc & chuyển **2,7 s** = ⭐ **4,4 giây** cho **60 sheet · 8.365 dòng**, thừa sức trong hạn chờ **10 s** của client. ⇒ Tôi đã lấy một con số **đúng của sổ KHÁC** làm bằng chứng cho sổ này.

⭐⭐ **Lý do THẬT, và nó ⛔ không liên quan tới tốc độ:** §4b ⓶ hứa *"xem trước cho ra **đúng thứ** nạp sẽ ghi"*. Nếu mỗi cửa tự đọc Sheets **sống** thì hai cửa đọc sheet ở **hai thời điểm khác nhau** ⇒ lời hứa ấy **vỡ trong im lặng**, và người dùng tin **cái họ vừa nhìn thấy**. Với ảnh chụp, cả hai cửa đọc **cùng một `chup_id`** ⇒ lời hứa đúng **bằng CẤU TRÚC**, ⛔ không bằng kỷ luật người viết.

⚠ Cộng một ràng buộc đã đo: hạn mức đọc Sheets là **tài nguyên dùng CHUNG với owner đang mở chính file đó** — đã ăn `429` **thật** khi gọi 60 lượt thay vì gộp. Một màn đọc sống mỗi lần bấm là một màn **tiêu hạn mức của người khác**.

### ⓶ Ảnh chụp giữ CÁI GÌ — ⭐ ô NGUYÊN VĂN, ⛔ không phải khuôn RA

Ảnh chụp giữ **ô của vùng CHUẨN như sheet đã trả**, ⛔ **TRƯỚC** phép `chuyen()`. Ba hệ quả, cả ba đều là lý do:

| | |
|---|---|
| ⭐ Nó đúng nghĩa **ảnh chụp** | *"sheet nói gì lúc `15:02:41`"* — cùng vai `fls_pm_line` *(`QĐ-ITL-61`)* |
| ⭐ Phép biến đổi ⛔ **không bị chép thành bản thứ hai** | `KHUON_RA` · luật `Num` · `GAP-CANON-02` *(lằn quỹ **11 cột**)* ở lại **trong `adapters`** |
| ⛔ **Kiểu ô PHẢI giữ** ⇒ `jsonb`, ⛔ không `text` | Ép về `text` là **tự dựng lại** đúng cái bẫy đã cắn **HAI lần**: `doc_cot` ép ô về chuỗi làm sê-ri ngày thành `"45586"` *(`QĐ-ITL-102` ⓶)*, và làm `L6` của cổng #17 đo được **0 dòng** ⇒ đỏ |

⭐⭐ **SỬA 17/09 (`QĐ-ITL-128`): `Description` ĐƯỢC ĐỌC — ảnh chụp mang đủ `6/6` trường**, cưỡng chế ở `TRUONG_DOC_DUOC == SAU_TRUONG`. ~~Câu cũ: *"`Description` ⛔ KHÔNG có mặt trong ảnh chụp — 5/6 trường"*~~ *(`QĐ-ITL-92`/`107`)* — **đúng tới 17/09**, giữ làm bia.
⛔ Riêng **khối nhân sự `9`…`14`** thì vẫn **CẤM** *(`QĐ-ITL-107`)*, và phép canh đặt ở **TỪ VỰNG** chứ ⛔ không ở dữ liệu — `RE_TRUONG_CAM` + bài `test_tu_vung_doc_duoc_KHONG_duoc_chua_truong_CAM`.

### ⓷ Ba bảng, và ⛔ KHÔNG một con số nào lưu hai lần

| Bảng | Một dòng là gì | Vì sao nó có |
|---|---|---|
| `fls_chup` | **một LẦN ĐỌC** — `doc_luc` · workbook · lằn · `giay` · `actor` | trạng thái ② của `F04` cần *"đọc lúc nào"* mà ⛔ không phải chạm 8.365 dòng |
| `fls_chup_nguon` | **một nguồn trong một lần đọc** + `khai_version` **đã dùng** | ⭐⭐ nguồn đọc ra **0 dòng** vẫn **CÓ MẶT** — đúng điểm mù `S8` đã tự lộ *("sheet ra 0 dòng biến mất khỏi chính phép kiểm sinh ra để tìm nó")* |
| `fls_chup_dong` | **một dòng vùng CHUẨN**, ô để `jsonb` theo **tên trường** | dữ liệu |

⛔⛔ **⛔ KHÔNG lưu `so_dong`/`so_nguon` ở bảng đầu.** Cả hai **suy được** từ hai bảng dưới, và một cái đầu ghi `so_dong = 8.365` cạnh một bảng dòng **RỖNG** là **một lời nói dối mà ⛔ không cổng nào thấy** — đúng luật nền *"đo được 0 thứ ⇒ ⛔ KHÔNG ĐẠT"*. `giay` thì **giữ**, vì nó ⛔ không suy được từ đâu.

⭐ **Bản khai dùng lúc nạp ⛔ KHÔNG cần một cơ chế mới:** `repo.khai_cot.doc_khai(conn, source_id, tai=doc_luc)` **đã** trả bản khai *hiệu lực tại một mốc* — đó chính là việc tham số `tai=` được dựng ra để làm *(task `2`)*. `fls_chup_nguon.khai_version` **ghim** kết quả ấy để đối chiếu được, ⛔ **không** để thay nó.

### ⓸ Bốn tuyến mới — **20 → 24**

| Method · Path | Vai | Trạng thái `F04` |
|---|---|:--:|
| `GET /api/fls/v1/sources` | **68 nguồn** + `khai_version` hiện hiệu lực *(`null` = ⛔ chưa ai khai)* + `chup_cuoi` | ① |
| `GET /api/fls/v1/sources/{source_id}/khai-cot` | bản khai hiện hiệu lực + **cả dãy `version`** *(ai khai · lúc nào)* | ③ |
| `GET /api/fls/v1/chup` | danh sách ảnh chụp, **mới nhất trước** | ② |
| `GET /api/fls/v1/chup/{chup_id}` | một ảnh chụp: đầu + từng nguồn + `?limit` dòng đầu để xem trước | ② |

⛔ **Vẫn ⛔ KHÔNG có `PUT`/`DELETE`.** Ảnh chụp là **chỉ-THÊM**: chụp lại ⇒ **`chup_id` MỚI**, ảnh cũ ⛔ không đổi một ô — cùng kỷ luật `fls_khai_cot` và `fls_pm_line`.

### ⓹ `chup_id` XOR `dong` — hai đường vào, và chỉ MỘT là đường thật

Thân yêu cầu của `xem-truoc`/`nap` phải mang **đúng một trong hai**; cả hai, hay ⛔ không cái nào ⇒ **400 `FLS-BAD-REQUEST`**.

| Khoá | Vai |
|---|---|
| `chup_id` | ⭐ **đường THẬT** — đường màn `F04` đi |
| `dong` | ⛔ **CHỈ** cho **test và phép đo đối chứng**, ⛔ **không** phải một đường vận hành *(cùng lời khai với tham số `khai_theo` của `nap_sao_ke.nap()`)*. Nó ở lại vì **31 bài test hiện hành** *(17 ở cửa + 14 ở `nap_lo`)* chứng minh **9 luật soát** đi qua nó — vứt nó là vứt phép chứng minh |

⭐⭐ **Nên `fls_run` có thêm `chup_id` — `nullable`, và ⛔ CỐ Ý nullable** *(cùng lý do `khai_id`, `R-A1`)*: một lô vào bằng đường `dong` sẽ **HIỆN RA** là `chup_id = NULL`, tức **⛔ không có ảnh chụp nào đứng sau nó**. Khai `NOT NULL` là buộc phải **bịa** một ảnh chụp cho mọi lô test — tức làm bẩn đúng cái cột dựng ra để nói thật.

### ⓺ ⛔ Cái nhóm này CỐ Ý ⛔ KHÔNG giải

| ⛔ Không có | Vì sao |
|---|---|
| ⛔ Cửa **BẮT ĐẦU một lần chụp** | Chụp là việc **đọc Google Sheets**, và đường đọc ấy ở `tools/`, ⛔ không ở tầng cửa *(`import-linter` hợp đồng `1` cấm `fls.api` chạm `psycopg`; hợp đồng `7` cấm nó biết tầng kho)*. Mở một đường mạng trong cửa là đúng thứ `QĐ-ITL-110` vừa quyết ⛔ không làm. ⇒ **Ai bấm chụp, theo nhịp nào** — `GAP-CHUP-01` |
| ⛔ Trạng thái `InActive`/`Closed` của nguồn | ⛔⛔ **⛔ KHÔNG có trong kho.** `fls_source` có **7 cột**, ⛔ không cột nào là trạng thái; `Account Status` *(`Closed` **10** · `InActive` **5**)* chỉ được đọc **SỐNG** từ sheet AS-IS ở `fls/kiem/nguon_song.py` `L8`. ⇒ `BA-06` §7 ① *("hiện mờ, bỏ tick sẵn")* ⛔ **chưa dựng đủ được** — `GAP-CHUP-02` |
| ⛔ Cửa **XOÁ ảnh chụp cũ** | Kho **chỉ-THÊM**. Mỗi lần chụp thêm ~**8.365 dòng · 480 KB thô** ⇒ chụp hằng ngày là ~**3 triệu dòng/năm**. Số ấy PostgreSQL chịu được, nhưng *"dọn khi nào"* là **quyết định của chủ sổ**, ⛔ không của code — cùng hạng với `GAP-KHO-02`. ⇒ `GAP-CHUP-03` |

---


## §4d · ⭐⭐⭐ THỨ TỰ NGÀY — hai cửa, và cả hai đều nói *"máy ⛔ không quyết"* *(mới 2026-09-08, `QĐ-ITL-113`)*

> ⛔⛔ **`GAP-NAP-02` ghi *"lô thật gần như chắc chắn có ngày mơ hồ"* — đó là một SUY LUẬN. Đo thật thì nó là phần lớn của lô.**

Đo trên ảnh chụp thật `chup_id 23719` *(60 nguồn · 8.368 dòng)*:

| | |
|---|--:|
| ô `Date` là **số** *(seri Google — ⛔ không mơ hồ)* | 4.175 |
| ô `Date` là **chuỗi** | 4.193 |
| ⛔ **MƠ HỒ** *(cả hai phần ≤ 12)* | ⛔ **1.894 = 22,6%** |
| ⇒ trải trên | ⛔ **29/60 nguồn** |

### ⓵ ⭐⭐⭐ Phép đo LẬT đúng cái mặc định mà ai cũng sẽ chọn

| | |
|---|--:|
| nguồn suy được thứ tự **từ chính nó** *(có ≥1 dòng phần nào > 12)* | ⭐ **29/29** |
| ⛔ nguồn **MÂU THUẪN** *(có cả bằng chứng `dmy` lẫn `mdy`)* | ⛔ **0** |
| nguồn chắc chắn **`dmy`** *(ngày/tháng — kiểu VN)* | ⛔⛔ **0** |
| nguồn chắc chắn **`mdy`** *(tháng/ngày)* | ⭐⭐ **29/29** |
| nguồn trộn cả ngày-số lẫn ngày-chuỗi | ⛔ **0/50** *(⇒ luật `S6` đứng)* |

⇒ ⭐⭐⭐ **Một mặc định `dmy` *"vì đây là Việt Nam"* sẽ HOÁN ngày↔tháng trên 1.894 dòng** — đúng lớp lỗi `QĐ-ITL-17` *(**93%** dòng từng bị hoán, ~**181 tỷ** sai kỳ)*. Các nguồn ấy là **OCBC Singapore** và **TCB USD**: sao kê **nước ngoài**, `mm/dd/yyyy` là **ĐÚNG**.

⭐ Và một nguồn **ĐỘC LẬP** xác nhận: `tools/dung_lai_bank_transactions.py:50` ghi *"chuỗi ở đây là `mm/dd/yyyy` — đọc được từ chính `Bank Transactions`"*. **Hai phép đo độc lập, cùng kết luận** ⇒ ⛔ không phải trùng hợp.

### ⓶ Chỗ ở: `fls_khai_cot.thu_tu`, ⛔ KHÔNG một bảng mới

`fls_khai_cot` **đã** là *một dòng cho một trường* — khoá `(source_id, version, truong)`, và `cot` trả lời *"đọc **cột nào**"*. `thu_tu` trả lời *"đọc **thế nào**"*: **cùng bản chất**, cùng một dòng, và được **`version` + `actor` miễn phí** *(chỉ-thêm, truy vết được ai khai lúc nào)*.

⭐ Nó cũng biến nhận xét của `GAP-CHUP-04` từ *"sai mô hình"* thành *"mô hình per-field là **ĐÚNG**"*.

⛔⛔ **`NULL` ⛔ KHÔNG có nghĩa *"coi như `dmy`"*** — nó có nghĩa *"nguồn này ⛔ **chưa khai**"*, và lúc ấy ngày mơ hồ **vẫn bị loại** kèm lý do, ⛔ không bị đoán.

⛔ Ràng buộc `fls_khai_cot_thu_tu_ck` **neo vào HAI cột**: `thu_tu IS NULL OR (truong = 'Date' AND thu_tu IN ('dmy','mdy'))`. Đây là `CHECK` **đầu tiên** của cả kho *(đo 08/09: **0** ràng buộc `CHECK`)*, nên `pg_verify` được **mở rộng cùng lượt** để canh nó — trước đó nó so `FK` · khoá chính · `UNIQUE` và ⛔ **không** so `CHECK`.

### ⓷ Hai tuyến mới — **24 → 26**

| Method · Path | Vai | Trạng thái `F04` |
|---|---|:--:|
| `GET /api/fls/v1/chup/{chup_id}/thu-tu` | **BẰNG CHỨNG** từng nguồn: `da_khai` · `de_xuat` · `mau_thuan` · `cau` *(một câu **có con số**)* · `bang_chung` *(6 ô, **kể cả ô `0`**)* + `so_can_khai` · `so_con_thieu` · `so_dong_mo_ho` | ②b |
| `POST /api/fls/v1/sources/{source_id}/thu-tu` | khai **CHỈ** thứ tự — sinh `version` MỚI, **GIỮ NGUYÊN `cot`** | ②b |

⛔⛔ **Khoá trả về là `de_xuat`, ⛔ KHÔNG phải `thu_tu`** — quyền ấn định kỳ kế toán ở **NGƯỜI**. Đổi tên khoá ấy là đổi **ai quyết**, mà một cú đổi tên thì ⛔ không cổng nào khác thấy ⇒ có một bài test ghim đúng cái tên.

⭐⭐ **Vì sao `GET …/thu-tu` là tuyến RIÊNG chứ ⛔ không nhét vào `GET /chup/{id}`:** cửa ấy trả **50 dòng đầu** *(đúng cho một lưới xem trước)*, còn phép đo này phải soi **MỌI dòng** — bằng chứng quyết định có thể nằm ở **dòng cuối** *(nguồn nặng nhất: **905** dòng mơ hồ trong **2.168** dòng)*. Hai câu hỏi khác nhau ⇒ hai cửa.

⭐⭐⭐ **Vì sao `POST …/thu-tu` là tuyến RIÊNG chứ ⛔ không dùng `POST …/khai-cot`:** bản khai là **chỉ-THÊM** nên một `version` mới phải chở **đủ 6 trường** ⇒ qua cửa kia, màn phải **đọc `cot` hiện hành rồi gửi lại** = một chu trình **ĐỌC-SỬA-GHI**. Ai khai `cot` mới trong khe giữa hai lượt sẽ bị **đè lại bằng `cot` CŨ**, mà `version` **vẫn tăng** ⇒ ⛔ **không cổng nào thấy**, vì mọi dòng riêng lẻ đều hợp lệ. Cửa này **đọc + ghi trong CÙNG một giao dịch**.

⛔ Ở cửa này `thu_tu` là **BẮT BUỘC**, ⛔ không tuỳ chọn: gọi *"khai thứ tự"* mà ⛔ không đưa thứ tự thì ⛔ không có việc gì làm — và lặng lẽ ghi `NULL` là **XOÁ** thứ tự người ta đã khai, một cú xoá đi qua một cửa mang tên *"khai"*.

⛔ Nguồn ⛔ **chưa khai `cot`** ⇒ **409 `FLS-KHAI-KHONG-CO`**, ⛔ **không** tự dựng một bản khai rỗng để có chỗ đậu `thu_tu`: đoán vị trí cột là thứ `sao_ke` cấm thẳng vì *"đoán ⛔ không phải kém chính xác — nó là **sai tiền**"*.

### ⓸ ⛔ Cái nhóm này CỐ Ý ⛔ KHÔNG giải

| ⛔ Không có | Vì sao |
|---|---|
| ⛔⛔ ~~Cửa *"khai tất cả theo đề xuất"*~~ — **BỊ LẬT 2026-09-09 bởi `QĐ-ITL-117`, xem `§4e`** | **29 nguồn = 29 cú bấm, MỘT LẦN trong đời nguồn ấy** *(bản khai có `version`, chỉ bump khi bank đổi mẫu)*. Một nút gộp là một nút **được bấm mà ⛔ không ai đọc** ⇒ đổi mất chính cái `QĐ-ITL-113` mua: **người đọc bằng chứng rồi mới ấn định** |
| ⛔ Máy tự khai khi bằng chứng *"quá rõ"* | **0 mâu thuẫn / 0 nguồn `dmy`** là bằng chứng rất mạnh, nhưng đây là **máy quyết kỳ kế toán của một bút toán**. Và một nguồn **MỚI** chưa có bằng chứng thì máy sẽ suy trên **⛔ không gì** |
| ⛔ Xoá / sửa một `thu_tu` đã khai | Chỉ-THÊM. Đổi ⇒ `version` **MỚI**; bản cũ giải thích được các lô **đã nạp trước đó** |

## §4e · ⭐⭐⭐ KHAI THỨ TỰ CẢ LÔ — cửa *"DỮ LIỆU tự ấn định"* *(mới 2026-09-09, `QĐ-ITL-117`)*

> ⛔⛔ **Owner soi màn đã chạy rồi hỏi: *"cách đọc ngày của từng nguồn — bước này hơi buồn cười, trong GGSheet đang đưa về định dạng chung như thế nào?"*** — và ba phép đo cho thấy câu hỏi **đúng**.

### ⓵ GGSheet **có** đưa về khuôn chung — nhưng ở tab mà FLS ⛔ không được đọc

| Đo trên ảnh `23719` *(8.368 dòng)* | |
|---|--:|
| ô `Date` là **số sê-ri** *(Sheets đã hiểu là ngày)* | 4.175 · 49,9% |
| ô `Date` là **CHUỖI** *(Sheets ⛔ chưa hiểu)* | 4.190 · 50,1% |
| ô rỗng *(⛔ không phải số, ⛔ không phải chuỗi)* | 3 |
| nguồn **toàn sê-ri** · **toàn chuỗi** · **trộn** · rỗng | 16 · 34 · ⭐ **0** · 10 |

⇒ Vùng THÔ ⛔ **không** có khuôn chung, và khác biệt là **theo SHEET** *(cách dán vào)*, ⛔ **không theo dòng** — nên nó **là** một thuộc tính của nguồn, đúng chỗ `fls_khai_cot.thu_tu` đang ở.

⛔⛔ **Còn tab `Bank Transactions` thì CHUẨN HOÁ HẾT về ngày** *(`tools/dung_lai_bank_transactions.py:50`)*. ⇒ Câu trả lời cho owner là *"có"* — nhưng tab ấy là **THƯỚC** của nhánh `oracle-parity`, ⛔ **không phải đầu vào**: nếu `F04` đọc nó thì FLS **mất khả năng bắt nó sai**, mà nó **đã sai** — hoán ngày↔tháng trên **93%** dòng, `~181 tỷ` lệch kỳ *(`QĐ-ITL-17`)*.

### ⓶ ⭐⭐⭐ Bằng chứng **đồng nhất VÀ tự chứng** — đây là chỗ quyết định đổi

| Đếm trên **4.187** ô chuỗi khớp khuôn `d/d/yyyy` | |
|---|--:|
| phần **TRƯỚC** dấu `/`: lớn nhất | **12** |
| phần **TRƯỚC**: số lần `> 12` | ⭐⭐ **0** |
| phần **SAU** dấu `/`: lớn nhất | **31** |
| phần **SAU**: số lần `> 12` | ⭐⭐ **2.296** |

⇒ Khe đầu là **tháng**. Và ⛔ **không phải suy ở mức sổ**: **34/34** nguồn chuỗi **tự chứng minh bằng dữ liệu của CHÍNH NÓ** *(mỗi nguồn có ≥1 dòng phần-sau `> 12`)*; `chac_dmy` = **0** ở khắp **60** nguồn; mâu thuẫn **0**.

⇒ ⭐⭐⭐ Máy đề xuất `mdy` **34 lần** và **34 lần một đáp án**. **Bắt kế toán bấm 27 cú** *(29 cần khai − 2 đã khai)* **để trả lời một câu mà dữ liệu đã tự trả lời là bắt họ đọc 27 lần rồi BẤM THEO PHẢN XẠ** — tức **đúng cái lo** mà câu *"⛔ không có nút khai tất cả"* ở `§4d ⓸` dựng ra để chặn, chỉ tốn thêm 26 cú.

### ⓷ Tuyến **thứ 29** — và nó ⛔ KHÔNG nhận `thu_tu`

| Method · Path | Thân | Trạng thái `F04` |
|---|---|:--:|
| `POST /api/fls/v1/chup/{chup_id}/thu-tu` | **chỉ** `source_ids: [int]` — ⛔ **KHÔNG** `thu_tu` | ②b |

⛔⛔⛔ **Cả điểm của tuyến này nằm ở chỗ nó ⛔ không nhận `thu_tu`.** `POST /sources/{id}/thu-tu` là cửa *"NGƯỜI ấn định"* ⇒ nó **phải** nhận. Cửa lô là cửa *"DỮ LIỆU tự ấn định"* ⇒ nó **đo lại** bằng chứng phía máy chủ rồi ghi **đúng cái nó đo ra**. Nếu nó nhận `thu_tu`, màn hình thành **cỗ máy khai `dmy` cho 27 nguồn bằng một cú bấm** — đúng cái `QĐ-ITL-113` dựng ra để chặn, chỉ nhanh hơn 27 lần, và biên bản sẽ trông **hoàn toàn bình thường**.

Trả về: `so_nguon_yeu_cau` · `so_nguon_khai_moi` · `so_nguon_da_dung` · `so_nguon_khong_can` · `so_dong_lam_chung` · `so_dong_mo_ho` + `nguon[]` *(mỗi nguồn: `ket_qua` ∈ `khai_moi`|`da_dung`|`khong_can`, `thu_tu`, `version`, `cau`)*.

⭐ **`so_dong_lam_chung` và `so_dong_mo_ho` PHẢI đi cạnh nhau**: cái thứ nhất là *"bao nhiêu dòng tự nói ra thứ tự"*, cái thứ hai là **HẬU QUẢ** — *"bao nhiêu dòng nhờ bản khai vừa ghi mà vào sổ"*. Nói cái thứ nhất mà ⛔ không nói cái thứ hai là báo một phép đo ⛔ **không có hậu quả**.

### ⓸ ⛔ Ba cái NỔ — và chúng LÀ giá trị của cửa

| Khi | HTTP | Vì sao ⛔ không thể nhẹ hơn |
|---|:--:|---|
| thân mang `thu_tu` | **400** | Xem ⓷. Câu lỗi **chỉ ra cửa đúng** *(`POST /sources/{id}/thu-tu`)* — một câu chỉ nói *"⛔ không được"* sẽ làm người gọi đi tìm cách lách |
| nguồn ⛔ **không tự chứng** *(`de_xuat = null`: hết chứng hay **mâu thuẫn**)* | **422** · `FLS-THU-TU-KHONG-TU-CHUNG` | ⛔ **CẢ LÔ**, ⛔ 0 bản khai mới. Một lô *"thành công 25/27"* là: người bấm thấy xanh · 2 nguồn lặng lẽ ở lại `NULL` · và ⛔ **không cổng nào đỏ** vì mọi dòng `fls_khai_cot` đều hợp lệ |
| `da_khai` **khác** `de_xuat` | **422** | Người bảo `dmy`, dữ liệu bảo `mdy` là **một bất đồng THẬT**. Lặng lẽ ghi theo máy là **xoá một câu trả lời của người** — bằng một `version` mới trông y hệt mọi `version` khác. Câu lỗi nêu **cả hai** giá trị |

⛔ **Nguồn `mo_ho = 0` thì cửa ⛔ KHÔNG GHI GÌ** *(`ket_qua = khong_can`)*: `parse_ngay` chỉ hỏi `thu_tu` khi **cả hai** phần `<= 12` ⇒ với **16/60** nguồn toàn sê-ri *(và 5 nguồn nữa toàn chuỗi nhưng `mo_ho = 0`)*, `thu_tu` **⛔ không bao giờ được đọc**. Ghi vào là dựng một bản khai **gợi ý rằng nó có tác dụng** — và lần sau ai đó sẽ **sửa nó để chữa một dòng ⛔ không liên quan**.

⛔ Bấm **lần hai** ⇒ `so_nguon_khai_moi = 0`, `so_nguon_da_dung = N`, và ⛔ **không** sinh một `version` y hệt bản cũ. Sổ chỉ-thêm ⛔ không **cấm** điều đó, nhưng một cú bấm lần hai ⛔ không được **trông như** N lần khai mới.

### ⓹ ⛔⛔ Một khuyết tật THẬT trong mã, do bộ test bắt

Bản đầu xếp nhánh *"⛔ không có bằng chứng"* **lên TRƯỚC** nhánh *"⛔ không cần khai"* ⇒ một nguồn **toàn ngày sê-ri** bị xếp vào *"⛔ không tự chứng"* và **làm NỔ CẢ LÔ** — trong khi nó ⛔ **không cần khai gì**. ⇒ *"⛔ Không có bằng chứng"* chỉ là một vấn đề khi **có câu hỏi cần trả lời** *(`can_khai`)*. Thứ tự bốn nhánh ấy nay mang ghi chú **⛔ đừng đổi**.

## §4f · ⭐⭐⭐ NẠP CẢ LÔ — lằn mà màn `F04` nay **LUÔN** đi qua *(mới 2026-09-08, `QĐ-ITL-111` + `112`)*

> ⛔⛔ **Mục này viết muộn một ngày, và chỗ muộn ấy đáng ghi hơn nội dung nó.** Hai tuyến dưới **dựng xong 08/09** và đã **chạy thật trên 60 nguồn · 8.368 dòng**, nhưng tới **09/09** thì `BA-07` vẫn ⛔ **không có một chữ** về chúng — trong khi `kiem_so_song` **XANH 67/67**, `kiem_tai_lieu` **XANH 5/5**, `soi_bang_tuyen` **XANH 29/29**.
>
> ⭐⭐ Lý do ⛔ không cổng nào thấy: cả ba canh **SỐ**, **bảng**, và **SQL** — ⛔ không cổng nào hỏi *"hợp đồng có NÓI tới cửa này ⛔ không"*. ⇒ Cổng `test_ba07_phu_het_tuyen` sinh ra từ đúng chỗ trống ấy, và nó bắt **hai chiều** *(cửa thật mà tài liệu ⛔ không nói · đường tài liệu nói mà ⛔ chưa tồn tại phải mang `⬜`)*.

### ⓵ Hai tuyến — và vì sao là tuyến RIÊNG chứ ⛔ không thêm một khoá

| Method · Path | Thân | Có? |
|---|---|:--:|
| `POST /api/fls/v1/nap/lo/xem-truoc` | `chup_id` + `source_ids: [int]` ⛔ **KHÔNG rỗng** | ✅ |
| `POST /api/fls/v1/nap/lo` | y hệt, thêm `run_id` | ✅ |

⛔⛔ **⛔ KHÔNG thêm một khoá `source_ids` vào `§4b`** — ⛔ không phải vì *"lô to hơn"*, mà vì **khuôn TRẢ VỀ khác hẳn**: biên bản gộp mang `so_nguon` · `so_nguon_vao` · `so_nguon_chua`, và **mỗi luật** mang `nguon_khong_dat[]` + `nguon_chua_do[]`. Một tuyến trả **hai khuôn** là một tuyến mà người gọi ⛔ **không biết mình đang đọc khuôn nào** — và lúc ấy mọi phép đọc đều phải **đoán**.

⭐ `source_ids` **⛔ không có mặc định *"lấy hết"***: máy ⛔ không tự chọn nguồn nào cho một **lô tiền**. Đúng 59 lần rồi sai lần thứ 60 là nạp **dữ liệu ⛔ không ai yêu cầu**, và biên bản sẽ trông **hoàn toàn bình thường**.

### ⓶ ⛔⛔ Một BẪY MÃ phải nói trước — nó là lý do lô **lặp theo từng nguồn**

`NgucCanh.source_sheet` nằm trong **`content_key`** *(khoá chống trùng)*. ⇒ Nối 60 nguồn thành **một danh sách phẳng** dưới **một** `NgucCanh` thì mọi dòng mang **cùng một `source_sheet`**, và dòng của **hai bank khác nhau** sẽ **bị đếm là TRÙNG rồi bỏ đi trong im lặng** — tiền thật, biến mất, ⛔ không một dòng đỏ nào.

⇒ Lô **lặp theo từng nguồn**, mỗi nguồn một `NgucCanh` *(`source_sheet` = khoá nguồn ấy, `thu_tu` = bản khai của nguồn ấy)*, **tất cả trong MỘT giao dịch**. Cổng: hai nguồn có **dòng nội dung y hệt** ⇒ **cả hai** phải vào sổ.

### ⓷ ⭐⭐⭐ Biên bản GỘP: **9 dòng**, ⛔ không 540 ô

60 nguồn × 9 luật = **540** kết quả. Màn hiện **9 dòng**, mỗi dòng **bung ra** đúng tên nguồn dính.

| Ô của mỗi luật | Nghĩa |
|---|---|
| `hang` | **nặng nhất** trong 60 nguồn *(`CHAN` > `CO` > `CANH`)* |
| `da_do` | **Σ** số dòng đã soi của cả 60 nguồn — ⛔ không phải của nguồn đầu tiên |
| `nguon_khong_dat[]` · `so_nguon_khong_dat` | tên các nguồn **đo được mà ⛔ không đạt** |
| `nguon_chua_do[]` · `so_nguon_chua_do` | tên các nguồn **⛔ không có gì để đo** *(đọc ra 0 dòng)* |

⛔⛔ **VÀ ĐÂY LÀ CHỖ MỘT PHÉP GỘP NGÂY THƠ SẼ BÁO OAN.** Đo trên ảnh chụp thật: **10/60 nguồn đọc ra 0 dòng** *(tài khoản đã mở mà chưa dùng — ⛔ **không** phải khuyết tật)*. Với chúng, `S2`…`S7` trả `dat=False, da_do=0` — **đúng theo luật nền** *"xanh trên tập RỖNG là CHƯA ĐO"*. ⇒ Gộp bằng `all(dat)` thì **6/9 luật của cả lô ĐỎ** chỉ vì 10 tài khoản rỗng, trong khi 50 nguồn thật **đều đạt**. **Một báo động đỏ oan là một báo động sẽ bị bỏ qua** — lúc ấy cả biên bản mất tác dụng.

### ⓸ ⛔⛔⛔ Một khuyết tật THẬT trong phép gộp, do chính bộ test bắt

Bản đầu tách hai ô trên bằng `da_do`: `da_do == 0` ⇒ *"chưa đo"*. ⛔ **Sai** — `s10_o_cua` khi ⛔ chưa thu dải trả `(CHAN, dat=False, da_do=0)`, nên nó bị xếp vào ô *"chưa đo"* và biên bản báo **`S10` ĐẠT trong khi `S10` đang CHỪA chính nguồn đó**.

⭐⭐ **`da_do = 0` ⛔ KHÔNG phân biệt được hai thứ khác nhau về bản chất:** *"⛔ không có gì để đo"* và *"CÓ thứ để đo mà ⛔ không đo được"*. **Hạng** thì phân biệt được — một `CHAN` **⛔ không bao giờ** được tha bằng câu *"chưa đo"*.

⇒ Luật đúng: `khong_dat` = ⛔ không xanh **VÀ** *(hạng `CHAN` **HOẶC** `da_do > 0`)* · `chua_do` = `da_do == 0` **VÀ** hạng ⛔ không phải `CHAN`. Kèm một **bất biến CHÉO** nổ ngay tại cửa: mọi luật đang **chừa** một nguồn thì **phải** hiện ra là ⛔ không đạt **và** phải có tên nguồn ấy trong `nguon_khong_dat`. *(Lùi cú vá ⇒ **4 bài ĐỎ** và bất biến nổ đúng câu.)*

### ⓹ Hậu quả: nguồn `CHẶN` **bị CHỪA**, lô **ĐI TIẾP**

| | |
|---|---|
| Nguồn có luật hạng `CHẶN` đỏ | **bị chừa** — `bi_chua = true`, `chua_vi = [tên luật]`, ⛔ **0 dòng** của nó vào sổ |
| Các nguồn còn lại | **vào sổ bình thường**, cùng **một** `run_id` |
| HTTP | **200** *(⛔ không 422)* — vì lô **có** phần vào sổ; `422` chỉ khi ⛔ **không nguồn nào** vào được |

⭐⭐⭐ **Chạy thật cả 60 nguồn qua HTTP** *(08/09, lặp lại 09/09 trên máy dựng từ `HEAD`)*: **58 vào sổ · 2 bị chừa** *(`MauBank USD_MGO1` · `PO_Payoneer USD_CGO1` — luật `S10`, hai bản khai trỏ **cùng một cột**)*, `8.368 − 12 = 8.356` dòng — **khớp từng dòng** với dự báo đưa ra **trước khi viết mã**, và **10** nguồn rỗng vào ô `chưa đo` ⛔ **không** bị kể thành không-đạt.

### ⓺ ⭐⭐ Màn `F04` nay **LUÔN** đi đường lô — kể cả khi tick **một** nguồn

⛔ Giữ hai đường *(một-nguồn và cả-lô)* là giữ **hai chỗ để chúng lệch nhau**, và cái lệch ấy hiện ra dưới dạng câu *"soát thấy 9 luật xanh, nạp ra số khác"* — thứ ⛔ **không ai** truy được trong một chiều nạp. ⇒ `§4b` hai tuyến một-nguồn **vẫn còn** *(chúng là cửa của một lô `dong` gõ thẳng, và bộ test dùng chúng)*, nhưng **màn ⛔ không gọi chúng nữa**.

## §4g · ⭐⭐⭐ MẪU SỐ + GHÉP CẢ LÔ — chặng ① của lộ trình *(mới 2026-09-09, `QĐ-ITL-118`)*

> ⛔⛔⛔ **Nhóm này bắt đầu bằng việc lật một con số tôi viết ra một ngày trước đó.** Lộ trình `13` §0 ⓵ ghi *"**584** dòng TỰ CHỨNG (8,0%) ⇒ cửa ghép lô dọn được ngay"*. Con số ấy là **68 (0,9%)** — nhỏ hơn **8,6 lần**.

### ⓵ ⭐⭐⭐ Vì sao `584` sai: đo bằng luật của **danh sách ứng viên**, ⛔ không phải của **cửa GHI**

`584` được đo bằng *"đúng MỘT ứng viên bậc `ma` chưa bị ghép"* — luật của `ung_vien_pm`, một cửa **ĐỌC** để **người CHỌN**. Nhưng cửa **GHI** (`ghep_lenh`) còn bốn cổng nữa. Đo lại trên đúng tập `652` dòng *"PM CÓ mang mã ấy"*:

| Trong `652` dòng có mã, vì sao ⛔ không tự chứng | Cổng của `ghep_lenh` | Số dòng |
|---|:--:|--:|
| ⭐ **TỰ CHỨNG** — cửa ghi **chắc chắn nhận** | — | ⭐ **68** |
| số tiền một dòng PM lệch ngoài dung sai `QĐ-ITL-63` | `ⓕ` | ⛔ **301** |
| ⛔ không dòng PM nào **cùng tiền tệ** | `ⓔ` | **202** |
| ≥2 dòng cùng mã, **Σ cả chùm** vẫn lệch | `ⓕ` | 51 |
| chùm có dòng `status` ⛔ không phải `Approve` | `ⓖ` | 30 |
| dòng PM cùng mã **đã bị ghép** cho dòng khác | `ⓒ` | 0 |

⛔ Và `301` dòng ấy ⛔ **không** phải một dung sai đặt quá chặt: đo hình của cái lệch cho thấy chỉ **16/491** nằm trong khoảng phí bank *(`< 0,1%`)*, còn lại lệch **hàng chục lần** *(vd `68,53 USD` bank ↔ `54.000 USD` PM — một mã tham chiếu ứng với hai số tiền khác nhau)*. ⇒ Cửa ghi **từ chối đúng**, và việc đó là việc của **người**.

⇒ ⭐⭐ Bài học, và là **lần thứ hai trong hai ngày**: *"đo QUAN HỆ thì gọi hàm thật"* ⛔ **không đủ** — phải gọi **đúng hàm của CÂU HỎI**. Câu hỏi là *"một cú bấm LÔ ghép được bao nhiêu dòng"*, nên luật phải là luật của **cửa GHI**. Tôi đã gọi một hàm thật, và nó là hàm **trả lời câu khác**.

⭐ Một lần sửa **ngược chiều** nữa: luật cũ *"đúng MỘT dòng"* còn **chặt hơn** cửa ghi, vì `ghep_lenh` nhận **N dòng** và chỉ đòi `Σ`. Nên `tự chứng` nay lấy **CẢ CHÙM** cùng mã — và ⛔ **không bao giờ một tập con**: ba dòng cùng mã mà chỉ hai trong ba cộng đúng tiền bank thì chọn hai dòng nào là **một quyết định nghiệp vụ** ⇒ máy từ chối *(`chum_lech_tien`)*.

### ⓶ ⭐⭐⭐ MẪU SỐ: `10.030` là sai — con số đúng là `8.246`

| Vế của sổ | Dòng | Đã nối lệnh chi | Độ phủ |
|---|--:|--:|--:|
| `PS Có > 0` | **8.246** | **2.562** | ⭐ **31,1%** |
| `PS Nợ > 0` | 1.784 | 139 | ⛔ **7,8%** |
| cả hai vế · ⛔ không vế nào | **0** · **0** | 0 · 0 | ⛔ *không đo được* |

⇒ Dòng ghép được **dồn hẳn** về vế `PS Có` ⇒ đó là **vế của lệnh chi**. Mẫu số thật của tác vụ ① là **8.246** *(⛔ không 10.030)*, và đích còn lại là **5.684** *(⛔ không 7.329)*.

⛔ **Hai vế RỖNG vẫn PHẢI có mặt trong bản trả về**, và tỷ lệ của chúng là `null` ⛔ **không phải `0`**: một phép phân hoạch bỏ mất hai nhóm rỗng sẽ làm `Σ ≠ tổng` **ngay dòng đầu tiên** có cả hai vế — và nó sẽ **im lặng**, vì tổng lấy từ `count(*)` chứ ⛔ không từ Σ các nhóm.

### ⓷ ⭐⭐⭐ *"Lệch 353"* ⛔ KHÔNG phải mâu thuẫn — nó là một **HIỆU** che đi `1.203` dòng

Lộ trình `13` §0 ⓸ gọi nó là *"một mâu thuẫn nội bộ"*. Đo ra bốn ô, **mỗi ô một TÊN**:

| Ô `work_status` × `có mối nối` | Số dòng | Tên |
|---|--:|---|
| ⛔ chưa phân loại · ⛔ chưa nối | **6.904** | `chua_phan_loai__chua_noi` — **đích thật** của tác vụ ① |
| đủ phân loại · đã nối | 1.923 | `da_phan_loai__da_noi` — hoàn chỉnh |
| ⭐ **đã nối** mà nhãn còn `UNMAPPED` | **778** | `da_noi__nhan_con_UNMAPPED` |
| ⭐ đủ phân loại mà **⛔ chưa nối** | **425** | `du_phan_loai__chua_noi` |

`778 − 425 = 353`. ⇒ Con số `353` **che đi 1.203 dòng** — nó nói **nhỏ hơn sự thật 3,4 lần**, và nó sẽ **về 0** nếu hai nhóm cùng tăng.

⛔⛔ **Và nó ⛔ không phải một lỗi để vá.** Hai cột trả lời **hai câu hỏi khác nhau**: `work_status` trả lời *"máy có suy đủ 5 trường phân loại không"* *(`fls/ledger/build.py`, `INV-I16`, **đóng băng lúc nạp** — mọi cửa ghi đều ⛔ không đụng `fls_itl`, `INV-I08`)*; `fls_moi_noi` trả lời *"dòng này đã nối với một dòng lệnh chi chưa"*. Một dòng **đủ phân loại mà chưa nối** là hoàn toàn bình thường — và cả **425/425** dòng ấy đều có `hd` + `pay_type` + `cdt1` + `doc_no`. ⇒ Cái sai là **phép TRỪ**, ⛔ không phải dữ liệu.

⭐ `fls_da_xong` = **0** trên toàn kho ⇒ chiều thứ ba *(người bấm xong)* hiện ⛔ chưa ai đi qua. Đo, ⛔ không giả định.

### ⓸ Ba tuyến mới — **29 → 32**

| Method · Path | Thân | Ghi |
|---|---|:--:|
| `GET /api/fls/v1/queue/mau-so` | — | ⛔ |
| `GET /api/fls/v1/queue/tu-chung` | — | ⛔ |
| `POST /api/fls/v1/queue/match-lo` | **chỉ** `itl_ids: [int]` + `reason` | ✅ |

⛔⛔⛔ **Cửa ghi lô ⛔ KHÔNG nhận `pm_line_ids`, và ⛔ KHÔNG BAO GIỜ nhận `force`** — cùng luật với `§4e ⓷`. Cửa ghép TAY nhận danh sách dòng lệnh **vì người đã chọn**; cửa LÔ ⛔ không có người chọn, nên nó **đo lại phía máy chủ** rồi ghép đúng cái nó đo ra. Nếu nó nhận danh sách thì một cú bấm thành **N phép ghép tay ⛔ không ai xem**. Và `force` là cách người ghi đè kết luận của máy cho **MỘT** dòng có lý do cụ thể *(`ghep_lenh ⓖ`)* — rải nó lên cả lô là **bỏ cổng duyệt cho N dòng bằng một cú bấm**.

Trả về: `so_dong_yeu_cau` · `so_dong_da_ghep` · `so_moi_noi` + `dong[]` *(mỗi dòng: `pm_line_ids`, `tien_bank`, `tong_lenh`, `evt_id`, `but_toan`)*.

### ⓹ ⭐⭐⭐ Ba tuyến **PHÍA LỆNH CHI** — **32 → 35** *(`QĐ-ITL-122`, `GAP-SCR-14`)*

> Owner chốt chiều đo 09/09: *"`Trans` map vào `PM` (số lượng Trans vốn nhiều hơn PM; ⛔ ko cần question các Trans không được map)"*.

⛔⛔⛔ **Đo trên bảng tuyến cùng ngày: `10` tuyến khoá theo `itl_id`, ⛔ `0` tuyến khoá theo dòng lệnh.** ⇒ Cả hệ ⛔ **không có một đường nào** hỏi được câu *"lệnh chi nào ⛔ chưa tìm được tiền"* — tức **đúng câu hỏi của việc**. Và màn `F01` đang hiển thị **7.682** dòng `Trans`, tức đang hỏi **đúng cái câu owner vừa nói là ⛔ không cần hỏi**.

★ Hai con số của **cùng một kho**, đọc cạnh nhau:

| Hỏi từ phía | Danh sách việc | Số dòng để phủ **90% tiền** |
|---|--:|--:|
| **TIỀN** *(cách cũ)* | **5.684** dòng chưa nối | **799** |
| ⭐ **LỆNH CHI** *(nay)* | **1.345** dòng chưa có tiền */* **698** phiếu | ⭐ **69** |

⇒ **69** thay vì **799**: chênh **11,6 lần**, và **cùng một dữ liệu**.

| Method · Path | Thân | Ghi |
|---|---|:--:|
| `GET /api/fls/v1/queue/lenh-cho` | — *(`?curr=` · `?duyet=0\|1` · `?den_pct=` · ⭐ `?ro=may\|nguoi\|khong` · ⭐ `?tu_chung=0\|1` · `?cursor=` · `?limit=`)* | ⛔ |
| `GET /api/fls/v1/queue/lenh-cho/summary` | — *(`?muc_pct=`, mặc định `90`)* | ⛔ |
| ⭐ `GET /api/fls/v1/queue/lenh-cho/ro` | — | ⛔ |
| ⭐⭐ `GET /api/fls/v1/queue/lenh-da-gan` | — *(`?cursor=` · `?limit=`)* | ⛔ |
| `GET /api/fls/v1/queue/lenh/{pm_line_id}/itl-candidates` | — *(`?limit=`)* | ⛔ |

⛔⛔⛔ **CẢ BỐN ĐỀU LÀ `GET`, và đó là điều quan trọng nhất của mục này.** Cú ghép vẫn đi qua `POST /api/fls/v1/queue/{itl_id}/match` — **một chuyến**. Màn hình phía lệnh chi chỉ **đổi thứ tự hỏi**: chọn dòng lệnh trước, rồi chọn dòng tiền, rồi gọi **đúng cửa ghi cũ**.

⇒ Mở một cửa ghi thứ hai sẽ làm hai việc, và cả hai đều xấu: ⓐ cổng quét mã nguồn *(chi-một-chỗ-ghi-tay)* **ĐỎ** — đúng như nó phải đỏ; ⓑ nặng hơn: hai đường ghi sẽ **lệch nhau** ở bốn cổng của `ghep_lenh` *(cùng tệ · chưa ghép · đã duyệt · Σ trong dung sai)*, và một cửa ghi **dễ hơn** cửa kia là một **đường tắt vòng qua kiểm tra** mà ⛔ không ai thấy. Có bài ghim: `test_KHONG_them_mot_duong_GHI_nao`.

**`lenh-cho`** trả mỗi dòng: `pm_line_id` · `pm_slip_id` · `ref_tho` · `ref_canon` · `amount` · `curr` · `status` · `hd` · `cdt1` · `source_row` · `tien` · `duyet` · `hang` · `luy_ke_pct`.

⭐ *(v3.9, `KQ-036 F-5 ⓐ`)* ＋ **`ma_canon`** *(`text | null` — `canon_ref(ref_tho)`: mã dòng lệnh mà phép chia **bậc** và **rổ** dùng; `null` khi ⛔ chuẩn hoá được)* trên **cả hai** cửa danh sách `lenh-cho` + `lenh-da-gan`, gắn ở **một** chỗ *(`lenh_cho.gan_ma_canon`, `WO-032` vòng 2)*. Nó khác `ref_canon` *(chuẩn hoá **lúc nạp**, lưu trong kho)* ở **nguồn**, ⛔ ở giá trị: đo ảnh PM `NAP-2026-10-02-PMF7DEEC9F` lệch **0 / 3.820** dòng *(`KQ-036` `AC-12`)*. Màn **⛔ đọc** khoá này *(grep `fls/web/tep/` **0** — `KQ-036 F-5`)*: nó là khoá **giải thích** cho người đọc cửa *("máy chia bậc theo mã nào")*, ⛔ khoá vẽ. ⛔ Bỏ nó: một bài thử đối chiếu bậc với mã cần đọc được mã ấy **từ cửa**, ⛔ tự tính lại.

⭐⭐⭐ **＋ khoá `the`** *(mới `2026-09-22`)* — khuôn **`11` trường** của thẻ lệnh chi ở màn ghép: `ma_lenh` · `trang_thai` · `loai_phieu` · `noi_dung` · `so_tien` · `nguoi_nhan` · `so_chung_tu` · `phap_nhan` · `ngan_hang` · `tai_khoan` · `cdt`, kèm `curr` · `trang_thai_nhan` · `trang_thai_mau` · `nhom_du_truong[]`.

⛔⛔ **Vì sao phải là một khoá của CỬA, ⛔ không phải việc của màn hình.** Đo `22/09`: **`6/11`** trường **⛔ KHÔNG cửa nào gọi tên** — chúng chỉ sống trong túi `tho`, khoá theo **TÊN CỘT CỦA GOOGLE SHEETS** *(`"Tên tài khoản"`, `"Pháp nhân thanh toán"`, `"Ngân hàng"`, `"Số tài khoản"`, `"Nội dung giao dịch nhập khi lập lệnh ở bank"`, `"Loại giao dịch (Payment Type)"`)*. Nếu JS tự móc mấy tên ấy thì **màn hình đọc thẳng tên cột của bảng tính** — thứ **đã đổi một lần rồi** — và lần sau chỗ hỏng là **một ô trống trong im lặng**, ⛔ không bài thử nào bắt được vì bài thử sẽ gõ **y hệt tên ấy**.

⭐ **THÊM, ⛔ không THAY.** Lằn `F01` cũ đang đọc `pm_line_id`/`tho`/`ro`/`hang`/`luy_ke_pct`; bỏ chúng là phá một màn đang chạy. Và ⛔ **không** một cửa riêng: hai cửa trả **cùng một danh sách** với hai hình dạng là **hai bản sự thật**, và chúng sẽ lệch.

| Luật của `the` | Đo được |
|---|---|
| `null` là một **câu trả lời**, ⛔ không phải chỗ để bỏ khoá | `so_chung_tu` vắng **`535/3.772`** = **`14,2%`** |
| `tai_khoan` đi qua **đúng phép che** của `nguon.tk` | `6` tài khoản là **thẻ** *(`PO1`…`PO9`)* ⇒ ⛔ không cắt 4 số cuối |
| `nguoi_nhan` hiện **NGUYÊN** trên màn | `QĐ-ITL-148 ②` — tên người nhận là **nội dung khoản chi**; luật che chỉ áp cho **bản xuất ra ngoài kho** |
| `loai_phieu` rút gọn bằng **bảng tra**, ⛔ không regex | `4` giá trị; một giá trị lạ phải hiện **nguyên văn** chứ ⛔ không bị bóp im lặng |
| `Timestamp` đổi **sê-ri → ngày** ở tầng đọc | ⛔ ra **`46091.42265217593`** ở **`3.772/3.772`** dòng nếu ⛔ không đổi |
| Khoá `tho` ⛔ chưa khai vẫn hiện, ở nhóm `Khác` | `27` khoá · `10` đã lên thẻ · `17` trong các nhóm ⇒ `Khác` **rỗng hôm nay**, và nó tồn tại cho **ngày mai** |

⭐⭐⭐ **`GAP-API-08` — ĐÓNG một nửa `2026-09-22`: tuyến `40` `GET /queue/lenh-da-gan`.**

`/queue/lenh-cho` lọc cứng `NOT EXISTS (fls_moi_noi)`, tức nó **chỉ** trả dòng **chưa nối** ⇒ ⛔ **không** đường nào hỏi *"lệnh chi nào ĐÃ có tiền"*. Hệ quả **dây chuyền** trước khi mở tuyến `40`:

| Thứ chết theo | Vì sao |
|---|---|
| `trang_thai` | **vĩnh viễn** `chua_gan` — `khuon_the_lenh` đọc một khoá ⛔ không cửa nào sinh |
| nhãn *"Đổi sang giao dịch đã chọn"* | ⛔ không bao giờ hiện |
| nút **Bỏ gán** | ⛔ không bao giờ bật — và nó gọi `/queue/undefined/chum` vì `itl_id_da_gan` **⛔ không ai sinh ra** |
| `.mrow.da_gan` | CSS **chết** |
| `lenh_ke_tiep` | ⛔ không bỏ qua được dòng nào |

⭐ Đo `22/09` bằng cách **gọi cửa thật**:

| Chip | Cửa | Đếm |
|---|---|---|
| `Chưa gán` | `?ro=nguoi` ＋ `?ro=may&tu_chung=0` | **`738`** ✅ `G-a` |
| `Không gán được` | `?ro=khong` | **`768`** ✅ `INV-I20` |
| ⭐ `Đã gán` | **tuyến `40`** `/queue/lenh-da-gan` | **`2.219`** |
| ⛔ `Tất cả` | **⛔ vẫn chưa có** — `GAP-SCR-26` | — |

⛔⛔ **`itl_da_gan` là một DANH SÁCH, ⛔ không một số.** Đo `22/09` trên kho thật: **`23/2.219`** = **`1,0%`** lệnh chi gắn **nhiều hơn một** dòng tiền. Một khoá số ít **im lặng bỏ mất** mối nối thứ hai — đúng ở chỗ người ta bấm `Bỏ gán`. ⭐ `1,0%` gần đúng **`1,1%`** ca có chùm: **cùng một sự thật** *(tiền ↔ lệnh là quan hệ **nhiều ↔ nhiều**)* nhìn từ **hai phía**.

⭐⭐ **Một tuyến RIÊNG chứ ⛔ không một cờ trên `lenh-cho`:** tên `lenh-cho` nghĩa là *"đang chờ"*; cho nó trả dòng đã nối là để một cái tên **nói dối**, và mọi người đọc mã sau này sẽ tin cái tên. ⚠ Và ⛔ không dùng lại `_CTE_LENH_CHO`: bộ máy xếp hạng theo tiền *(`row_number` ＋ `luy_ke_pct`)* trả lời câu *"xem tới đâu thì đủ"* — một câu **chỉ có nghĩa với việc đang chờ**.

⛔⛔⛔ **Và câu con `fls_moi_noi` PHẢI lọc phạm vi — qua phía ITL.** `pm_line_id` là một **khoá nghiệp vụ** *(lặp ở mọi lần nạp)*, còn `itl_id` là khoá của **một dòng trong một ảnh chụp**. Một câu con chỉ hỏi `WHERE m.pm_line_id = …` sẽ vơ cả mối nối của **mọi lần nạp khác** — bài thử bắt được ngay: `[2, 3, 23, 24]` thay vì `[23, 24]`. ⚠ Lọc ở **phía ITL** *(`i.run_id`)*, ⛔ không phải phía PM: ảnh chụp ngân hàng và ảnh chụp PM là **hai lần nạp khác nhau**.

⛔ Chip `Tất cả` **vẫn chưa có cửa** — nó là **HỢP** của hai rổ, và gộp hai cửa ở màn thì con số `x/y` sẽ do **màn tự cộng**, tức một **số của máy** (`UI-F8`). ⇒ `GAP-SCR-26`.


⭐ Xếp theo tiền GIẢM **trong TỪNG tiền tệ** *(`PARTITION BY curr` — `QĐ-ITL-58`, giữ nguyên từng chữ)*. ⛔ Ở đây luật ấy còn gắt hơn ở lằn cũ: dòng lệnh **USD** nhiều hơn **VND** *(`700` vs `590`)*, nên gộp lại thì **cả vế USD bị dìm xuống dưới**.

⛔⛔ **`?duyet=` mặc định là *KHÔNG LỌC* — hiện cả hai.** `275` dòng ⛔ chưa duyệt ⛔ **không phải việc của kế toán ITL** *(cửa ghép đòi `force` kèm lý do)*, nhưng ẩn chúng **theo mặc định** là một **mặc định im lặng** *(`INV-I16`)*: kế toán biết phiếu ấy tồn tại, ⛔ không thấy nó trong danh sách, và sẽ kết luận **hệ mất dữ liệu**. ⇒ Hiện, kèm cờ `duyet`, và để **người** bật bộ lọc. Giá trị lạ ⇒ **`400`**, ⛔ không âm thầm bỏ qua.

⭐⭐⭐ **`lenh-cho/ro` — BA RỔ theo *"AI trả lời được câu này"*** *(`G2`, `BA-12 §2`)*. Trả `may` · `nguoi` · `khong` · `tu_chung` · `tong`.

⭐⭐ *(v3.10, `TL-038` — `BG-039` yếu #1)* **＋ `nguoi_khac_tien_te`** *(`int`, **luôn có mặt**, `0` khi ⛔ lệnh nào)*: số lệnh rổ `nguoi` ở **đúng** nhánh *"khớp mã chỉ ở tiền tệ khác"* — đếm bằng **`lc.la_khop_ma_chi_khac_tien_te`** *(cùng hàm quyết `the.vi_sao`, `§4h ⓵'`)*, ⛔ so chuỗi `vi_sao`, ⛔ đếm lại ở JS. Bất biến: `0 ≤ nguoi_khac_tien_te ≤ nguoi`; phần còn lại `nguoi − nguoi_khac_tien_te` là lệnh **⛔ có số chứng từ**. **Vì sao cần:** sau `WO-037` rổ `nguoi` có **hai** loại lệnh, mà băng *"Việc của bạn hôm nay"* của `F01L` nói một câu cho cả rổ *"Chưa có số chứng từ"* — đo `fls-ba` 02/10 *(sổ thật chỉ đọc, gọi hàm thật `xep_ro` mọi trang, `dem_theo_ro` = `may` 184 · `nguoi` 616 · `khong` 801 · `tu_chung` 64 · `tong` 1.601)*: câu ấy **sai cho 84 / 616** lệnh *(số chứng từ **có**, chỉ khớp tiền tệ khác)*, đúng cho **532 / 616**. Màn tách hai câu theo con số **cửa** trả *(`BA-06` v4.17 `§4.5 ⓤ`)*.

⛔⛔ **Vì sao là một cửa RIÊNG chứ ⛔ không nhét vào `/summary`.** Cái kia đếm theo **đơn vị tiền tệ** *(`QĐ-ITL-58`)*, cái này đếm theo **ai trả lời được**. Gộp hai trục vào một cửa ra một bảng hai chiều mà ⛔ không ai hỏi, và làm **cả hai** khó đọc.

★ **Ba rổ PHẢI khép về `tong`** — một bảng phân loại ⛔ không cộng về tổng là một bảng ⛔ không kiểm được. Màn hình **tự kiểm** và nói ra. Đo `11/09`: `250 + 535 + 768 = 1.553` ✓.

⛔⛔⛔ **Và bậc `ma` của phép chia này tính ở PYTHON, ⛔ KHÔNG trong SQL.** `fls_pm_line.ref_canon` **đã chuẩn hoá**; `fls_itl.doc_no` thì **thô**. Một câu `i.doc_no = l.ref_canon` là **bản sao thứ hai** của `canon_ref` và nó ⛔ **không tương đương** — đo `11/09`: SQL cho `121` dòng rổ `may`, `canon_ref` thật cho **`250`** *(**sai 107%**)*, và sai cùng chiều ở rổ `khong` *(`514` → `768`)*. Cùng lớp lỗi mà `_SQL_ITL_MA` đã cảnh báo bằng một con số khác *(`560` vs `475`, `09/09`)*. Có bài ghim: `test_BAC_MA_tinh_bang_canon_ref_chu_KHONG_bang_so_sanh_THO`.

⚠ `tu_chung` chỉ `True` khi **đúng một** ứng viên khớp **cả tiền lẫn đơn vị tiền tệ**. Nhóm *"khớp mã nhưng lệch tiền"* *(`160` dòng)* ⛔ **KHÔNG** vào đây và ⛔ **không** được ghép theo lô: ở đó máy **phải** hỏi *"lệnh này ăn bao nhiêu của giao dịch kia"* — trả lời hộ là **máy quyết thay người** *(`INV-I16`)*.

⭐⭐⭐ *(v3.9, `KQ-036 F-6` — `fls-ba` đo 02/10 trên sổ thật **chỉ đọc**, gọi **hàm thật** `doc_lenh_cho_theo_ro` + `xu_ly._gan_gd` + `ung_vien_itl`, ảnh PM `NAP-2026-10-02-PMA07ED283`)* **Rổ `may` đo theo luật của CỬA GHI: một lệnh vào `may` chỉ khi có ≥ 1 dòng tiền khớp mã VÀ CÙNG tiền tệ.** `xep_ro` hôm nay xét **mã** mà ⛔ xét tiền tệ ⇒ **84 / 268** lệnh rổ `may` *(lệnh USD 63 · VND 15 · SGD 5 · HKD 1)* có **mọi** dòng tiền khớp mã đều **khác tiền tệ** — **84 / 84**, ⛔ lệnh nào trong nhóm có một dòng khớp mã cùng tiền tệ. Câu *"máy trả lời được — người chỉ DUYỆT"* sai ở **31,3 %** rổ: câu trả lời duy nhất của máy là một cặp cửa ghi **từ chối** *(`QĐ-ITL-62`, `BA-06 §4.3`)*. Cùng lớp lỗi đã đo một lần ở `tap_tu_chung` *(`584` → `68` — một con số hứa nhiều hơn cái bấm được)*.

| | Luật v3.9 |
|---|---|
| ⓐ rổ | `may` ⇔ ∃ dòng tiền **chưa nối** có `canon_ref(doc_no) = ma_canon` **và** `ma_tien_te(curr) = ma_tien_te(curr lệnh)` *(**cùng** hàm so tiền tệ của khuôn `§4h ⓵` — `trim` + chữ hoa)*. Khớp mã **chỉ** ở tiền tệ khác ⇒ rổ **`nguoi`**, `vi_sao` khoá mới **`ma_khop_khac_tien_te`** — câu nói **mã tiền tệ thật** của dòng khớp: *"số chứng từ khớp một dòng tiền bằng `<mã>` — cửa ghi ⛔ ghép hai tiền tệ; ⛔ ghép theo một số tiền trùng"* *(chữ v3.9 — ⭐ **chữ in v3.10** ở bảng ngay dưới: ⛔ ký hiệu cấm, `TL-038`)* |
| ⓑ `ung_vien_itl` | chỉ mang dòng khớp mã **cùng** tiền tệ *(đó mới là đề xuất của máy)* ⇒ `the.gd` *(`§4h ⓵'`)* của lệnh **chưa gán** ⛔ bao giờ là dòng khác tiền tệ. Lệnh rổ `nguoi` do ⓐ ⇒ `ung_vien_itl = []`, `gd = null` |
| ⓒ `tu_chung` | ⛔ đổi — đã hỏi cửa ghi *(`ds_tu_chung`)*; đo: **0 / 84** lệnh trong nhóm mang `tu_chung` |
| ⓓ chip | `Chưa gán` = `nguoi` ＋ `may` ⛔ tự chứng ⇒ **⛔ đổi** *(84 lệnh đi từ `may` ⛔ tự chứng sang `nguoi` — trong **cùng** chip)*. Đo hôm nay: `may` **268 → 184** · `nguoi` **532 → 616** · `khong` **801** · `tu_chung` **64** · `tong` **1.601** ⛔ đổi |

⭐⭐ *(v3.10, `TL-038` — `BG-039` yếu #4)* **Câu `vi_sao` là chữ cửa trả cho màn IN ⇒ nó theo luật ký hiệu màn hình: 0 ký tự trong `⛔ ⚠ ⭐ 🔒`** *(bộ `CAM` của `tests/web/test_luat_ky_hieu_man_hinh.py` — luật ra đời từ lời kế toán 04/09 *"vùng panel quá nhiều note, ký hiệu → khó nhìn"*)*. Đo 02/10 *(`lc.VI_SAO`, mã `4c3b2ae`)*: **3 / 3** câu mang ký hiệu cấm — `khong_co_tien_trong_so` **1** · `khong_co_so_chung_tu` **1** *(＋ `⇒`)* · `ma_khop_khac_tien_te` **2**; Chrome 8099 vẽ `⛔` thành **biểu tượng tròn đỏ giữa câu** ở `F01L` `hint` *(`BG-039` yếu #4)*. Cổng ký hiệu hôm nay chỉ quét `man_f02.js` + `man_f04.js` *(`THEO_LUAT`)* và ⛔ quét chuỗi Python ⇒ ⛔ cổng nào canh câu cửa. Ba câu **v3.10** *(so chuỗi — giữ nguyên khoá, chỉ đổi chữ)*:

| Khoá `vi_sao` | Câu v3.10 *(nguyên văn)* |
|---|---|
| `khong_co_tien_trong_so` | `có số chứng từ nhưng KHÔNG dòng tiền nào trong sổ mang số ấy — tiền chưa về, hay nằm trên sheet đã bị xoá khỏi workbook` |
| `khong_co_so_chung_tu` | `chưa có số chứng từ — phải tra bằng TIỀN + NGÀY` |
| `ma_khop_khac_tien_te` | `số chứng từ khớp một dòng tiền bằng {ma} — cửa ghi không ghép hai tiền tệ, và không ghép theo một số tiền trùng` *(`{ma}` như cũ: mã thật, trùng gộp, xếp chữ cái, rỗng ⇒ `(trống)`)* |

⚠ Chỉ đổi **chữ in**, ⛔ đổi **nghĩa** hay **tập** lệnh nào mang câu nào *(sổ thật: `khong` **801** · `khong_co_so_chung_tu` **532** · `ma_khop_khac_tien_te` **84**)*. Luật áp cho **mọi** câu cửa đặt trong `VI_SAO` từ nay *(khoá mới phải qua cổng)*.

⭐ *(v3.10, `TL-038` — `BG-039` yếu #3; trước: `WO-037` Rủi ro 2 NGOÀI)* **Phép so tiền tệ trong SQL của `itl-candidates` cũng là `ma_tien_te`**: `_SQL_ITL_UNG_VIEN` + `_SQL_DEM_CUNG_TE` so `upper(i.curr) = <mã lệnh đã qua ma_tien_te>` — **⛔ `trim` phía sổ**, trong khi rổ *(ⓐ)* và bậc `ma` *(Python)* `trim`. Luật: vế sổ trong SQL là `upper(btrim(i.curr, E' \t\r\n'))` — cùng tập khoảng trắng mà `str.strip()` gỡ ở ca thường *(space · tab · CR · LF)*. Sổ thật 02/10 *(`fls-ba`, chỉ `SELECT`)*: `curr` có khoảng trắng đầu/cuối **0 / 8.387** dòng `fls_itl`, chữ thường **0 / 8.387** ⇒ **0** ca đổi hôm nay; sửa để **một** luật so, ⛔ vì báo động.

⭐⭐ *(v3.11, `KQ-041 F-2` — `fls-test` 05/10)* **MỘT tập ký tự trắng cho MỌI phép so tiền tệ — khai ở một chỗ; Python · SQL · JS cùng đọc.** Đoạn v3.10 trên khai vế sổ SQL `btrim(i.curr, E' \t\r\n')` *"cùng tập `str.strip()` gỡ ở ca thường"* — tự giới hạn, và `KQ-041` đo đúng chỗ hở: PG thật, 6 chuỗi biên *(NBSP `U+00A0` · `\v` · `\f` · `U+3000` · khoảng trắng hẹp · `U+0085` ở mép mã)* ⇒ SQL giữ nguyên, Python ra mã sạch — lệch **6 / 6**. `fls-ba` đo thêm 05/10 *(đọc mã)*: phép so tiền tệ đang sống ở **ba** tập khác nhau —
- Python `str.strip()` **29** ký tự: `man_ghep.ma_tien_te` ＋ **6** bản viết tay — `ghi_tay.py:653` · `:744` *(cửa **GHI** `ghep_lenh`)* · `do_mau_so.py:415` · `:417` *(`ds_tu_chung` — cổng tự chứng)* · `doc_bao_cao.py:373` · `pm_join.py:435`;
- SQL `btrim(…, E' \t\r\n')` **4** ký tự: `lenh_cho.py:218` · `:225`;
- JS `String.trim()` **25** ký tự *(đo bằng `node`)*: `thanh_phan.js:138` *(`TP.tien`)* · `:192` *(`ma_te`)* — **có** `U+FEFF` mà Python ⛔ gỡ, **thiếu** `U+001C`…`U+001F` ＋ `U+0085` mà Python gỡ.

Sổ thật 05/10 *(`fls-ba`, chỉ `SELECT`)*: `fls_itl.curr` ngoài `^[A-Z]{3}$` **0 / 8.387** · `fls_pm_line.curr` **73 / 276.028** *(toàn giá trị `'20'` — ⛔ khoảng trắng)* ⇒ **0** ca đổi; sửa để **một** luật, ⛔ vì báo động.

| Luật v3.11 | |
|---|---|
| Tập **`TAP_TRANG_TIEN_TE`** | **30** ký tự = mọi `c` có `c.isspace()` ở Python *(**29**: `U+0009`…`U+000D` · `U+001C`…`U+001F` · `U+0020` · `U+0085` · `U+00A0` · `U+1680` · `U+2000`…`U+200A` · `U+2028` · `U+2029` · `U+202F` · `U+205F` · `U+3000`)* **＋ `U+FEFF`** *(BOM — thứ hay dính nhất khi chép từ CSV / Sheets; JS đã gỡ, Python chưa)*. ⛔ `U+200B` *(khoảng trắng độ rộng 0 — cả ba ngôn ngữ hôm nay đều ⛔ gỡ; giữ thế)* |
| Một chỗ khai | **một** hằng Python *(chỗ đặt do Dev chọn, giữ `lint-imports` **9 / 0**)*; `ma_tien_te(c) = str(c or "").strip(TAP_TRANG_TIEN_TE).upper()` |
| Python | **mọi** phép so tiền tệ trong `fls/` gọi `ma_tien_te` — **6** bản viết tay trên thay bằng lời gọi, **kể cả cửa ghi** *(giữ đúng nghĩa từng chỗ — vd. `pm_join._cur` vẫn bỏ chuỗi rỗng)* |
| SQL | vế sổ `upper(btrim(i.curr, %(tap)s))` — tập truyền **từ hằng** làm tham số; ⛔ chuỗi gõ lại trong SQL |
| JS | `TP` khai **một** hàm mã tiền tệ trên tập ấy *(⛔ `String.trim()`)*; `ma_te` + `TP.tien` gọi nó; bài thử so tập JS **=** tập Python |
| Chữ hoa | ⛔ đổi *(Python `.upper()` · PG `upper()` · JS `toUpperCase()` khác nhau ngoài ASCII — sổ thật `curr` ngoài `[A-Z0-9]` **0** ⇒ ngoài phạm vi, ghi lại)* |

⇒ Một dòng `curr = '\u00a0VND'` *(⛔ mã)*: rổ, bậc tiền `itl-candidates`, `tong_cung_tien_te`, màn và cửa ghi **cùng** coi là `VND`. **Cái giá:** cửa ghi nhận thêm `U+FEFF` ở mép mã như khoảng trắng *(hôm nay coi là một ký tự của mã ⇒ `KhacTienTe`)* — **0** dòng sổ thật chạm; `QĐ-ITL-62` ⛔ đổi *(một tiền tệ vẫn là **một** mã sau chuẩn hoá)*. Mã ⇒ **`WO-042` `(c)`**.

⭐⭐ *(v3.12, `KQ-046 F-1` — `fls-test` 05/10)* **Kiểm kê v3.11 ⛔ đủ — luật đúng, danh sách chỗ áp thiếu.** Kiểm kê v3.11 *("SQL 2 chỗ")* chỉ tìm `btrim(` — ⛔ tìm `upper(` trần, ⛔ tìm phép so chuỗi thô ⇒ bỏ sót chiều **ngược** `ung_vien_pm` *(cửa `/so/{itl_id}/pm-candidates`, lằn *Theo dòng tiền* `F01` — hộp ghép)*. `KQ-046` đo *(kho TEST, hàm thật)*: lệnh cùng số tiền với dòng tiền `VND` mà `curr` = `' vnd '` · `U+00A0`＋`VND` · `U+FEFF`＋`VND` · `VND`＋`U+0085` · `U+3000`＋`VND` ⇒ **5/5** ⛔ có mặt ở bậc nào, trong khi chiều thuận, rổ và cửa ghi coi là `VND`. Lệch cả ca **thường** `' vnd '` ⇒ trái cả v3.10. Có từ `0f6f054`; sổ thật **0** ca.

`fls-ba` kiểm kê lại 05/10 *(`Đ1` — grep `fls/` + `tools/`: `upper(` · `lower(` · `btrim(` · `trim(` · `.strip()` · `.upper()` · `PARTITION BY` / `GROUP BY` / `ORDER BY` / `= %s` trên cột `curr`; phép so `==` / `!=` / `===` trên khoá `curr`; mẫu số: **15** lời gọi `ma_tien_te(` Python · **5** lời gọi `ma_te(` JS · **2** `btrim(i.curr, %(tap)s)` SQL đã đúng)*:

| Lớp | Chỗ *(tệp:dòng @ `47e9fa4`)* | Hôm nay | Luật v3.12 |
|---|---|---|---|
| ⓐ **So giữa HAI nguồn** *(lệnh ↔ dòng tiền)* — SQL | `fls/repo/doc_bao_cao.py:309` · `:310` · `:317` *(`_SQL_UNG_VIEN`, `ung_vien_pm`)* | vế lệnh `upper(l.curr)` **trần**; vế dòng tiền `s.cur = ma_tien_te(…)` *(`:377`)* ⇒ **hai** tập trong **một** câu | ⭐ **áp** — `upper(btrim(l.curr, %(tap)s))`, tham số **từ hằng** `TAP_TRANG_TIEN_TE` *(như `lenh_cho.py:225` · `:232`)* |
| ⓐ **So giữa HAI nguồn** — Python | `fls/repo/man_ghep.py:631` *(`khoa_bang_chung` — điều kiện ⓑ tô sáng **số tiền** khi cùng đơn vị; gọi từ `xu_ly.py:740` · `:903`)* | `str(uv.get("curr")) == str(lenh.get("curr"))` — **⛔ chuẩn hoá gì** *(phân biệt hoa/thường, ký tự trắng)* | ⭐ **áp** — `ma_tien_te(uv) == ma_tien_te(lenh)` **và** mã ⛔ rỗng — cùng luật màn đã dùng *(`man_f01_ghep.js:227` `TP.ma_te(uv.curr) !== '' && …`)*: thiếu tiền tệ ⇒ ⛔ nói *"cùng đơn vị"*. ⚠ Hôm nay hai vế cùng thiếu ⇒ `'None' == 'None'` ⇒ **có** tô — đổi này là **chủ ý** |
| ⓑ **Gom theo tiền tệ để ĐẾM** *(một nguồn, ra số in)* | `fls/repo/do_mau_so.py:297` *(`_SQL_PM_CHUA_THEO_TE` — tiền tệ của lệnh chưa có tiền)* | `upper(COALESCE(l.curr,'?'))` ⇒ `' VND'` thành nhóm riêng cạnh `VND` | ⭐ **áp** — `upper(btrim(COALESCE(l.curr,'?'), %(tap)s))` *(nhóm `'?'` giữ nghĩa: thiếu tiền tệ)* |
| ⓒ **Xếp / gom / lọc hàng chờ** *(một nguồn, khứ hồi chip ⇄ lọc)* | `doc_bao_cao.py:507` · `:510` · `:513` · `:523` · `:563` · `:584` · `lenh_cho.py:111` · `:114` · `:117` · `:127` · `:139` · `:309` | `PARTITION BY q.curr` · `GROUP BY x.curr` · `AND x.curr = %s` trên giá trị **thô** — chip in giá trị thô, lọc nhận lại **đúng** giá trị ấy ⇒ **tự nhất quán** | ⛔ **NGOÀI** — luật xếp `QĐ-ITL-58` / `CR#4` *"`PARTITION BY curr` giữ nguyên từng chữ"*; đổi phải đổi **cả** chip lẫn lọc *(một lượt khứ hồi)*. Sổ thật **0** ca ⇒ nợ ghi, ⛔ phiếu tới khi có ca |
| ⓓ **Cùng nguồn, so danh tính** | `fls/web/tep/man_f01.js:60` *(`ST.curr === r.curr` — chip đang chọn)* | hai vế cùng từ một thân cửa `/queue` | ⛔ áp *(cho phép — ⛔ phép so hai tiền tệ)* |
| ⓔ Công cụ **ngoài** `fls/` | `tools/demo_dong.py:203` · `:231` *(`.strip().upper()`, đọc sheet sống cho bản demo)* | tập `isspace` *(29)* | ⛔ NGOÀI *(công cụ demo, ⛔ đường của màn hay cửa)* — ghi lại |

⇒ Sau v3.12, câu *"mọi phép so tiền tệ"* của v3.11 có **danh sách đủ**: lớp ⓐ ⓑ áp; ⓒ ⓓ ⓔ ngoài phạm vi **có lý do**. Cổng một chỗ *(`AC-9` `WO-042`)* phải quét **cả** `upper(` / `lower(` trần trên `curr` và phép so `==` thô trên khoá `curr` — ⛔ chỉ `btrim(i.curr`. Sổ thật 05/10 *(`fls-ba`, chỉ `SELECT`)*: `fls_pm_line.curr` chữ thường / ký tự trắng ở mép / `U+00A0` / `U+FEFF` / `U+3000` / `U+0085` **0 / 276.028** · `fls_itl.curr` **0 / 8.387** ⇒ **0** ca đổi. Mã ⇒ **`WO-047`**.

 *(phương án `KQ-036 F-6` nêu)*: trên **84** lệnh, ứng viên cùng tiền tệ đầu tiên là bậc `tien` **45** · `cung_tien_te` **36** · `gan_tien` **3** — khớp mã **0**. **45** lệnh có ứng viên cùng tiền tệ **lệch 0**, nhưng mỗi lệnh có trung vị **16** dòng cùng đúng số tiền ấy *(1 → 19)*, cách dòng khớp mã trung vị **294 ngày** *(≤ 7 ngày: **2 / 45**)*; **0 / 45** mang mã của một dòng lệnh khác ⇒ đó là **trùng tiền tình cờ**, ⛔ bằng chứng. Đẩy chúng lên đầu là đổi một cú bấm bị cửa ghi **TỪ CHỐI** *(an toàn — 0 ghi sai)* lấy một cú ghép **SAI mà cửa ghi NHẬN** — đúng chiều nguy hiểm. ⇒ **Đề xuất của máy phải vừa được cửa ghi nhận VỪA có bằng chứng mã**; ⛔ có ⇒ **⛔ đề xuất** *(`gd = null`)*, và lệnh sang `nguoi` kèm câu vì sao.

⚠ Nhóm 84 phần lớn trông như **lệnh trả bằng một tiền tệ khác** *(tỷ số tiền bank ÷ tiền lệnh: HKD→USD **0,129** · SGD→USD trung vị **0,81** · VND→USD trung vị **1 / 25.400**; riêng USD→VND trung vị **37.950** nhưng tản từ **12** tới **9,2 triệu** ⇒ lẫn cả trùng mã)*. **Kế toán ghi nhận ca ấy thế nào là câu của OWNER** *(`Q-FX-1`, `WO-037`)*; luật trên chỉ dừng máy **nói** rằng nó trả lời được.

⭐⭐ **`?ro=` — lọc theo RỔ**, và nó **⛔ không dùng chung** với `?curr=`/`?duyet=`: hai trục hỏi hai câu khác nhau *(ai trả lời được · đồng tiền nào nặng)*, trộn lại ra một tập ⛔ không ai đọc được ý nghĩa. `?tu_chung=` chỉ có nghĩa kèm `ro=may`; gửi một mình ⇒ **`400`**, ⛔ không âm thầm bỏ qua *(`INV-I16`)*. `ro` lạ ⇒ **`400`**, ⛔ **không** trả danh sách rỗng — rỗng nói *"⛔ không còn dòng nào"*, một câu **sai**, và người đọc sẽ kết luận đã xong việc.

⚠ **Cửa này TỐN hơn khi có `?ro=`, và khai ra chứ ⛔ không giấu:** rổ tính ở **Python** *(`canon_ref` trên cả hai vế)* nên ⛔ không lọc được trong `WHERE` ⇒ kéo hết dòng lệnh chưa nối, xếp rổ, lọc, **rồi mới** cắt trang. Trần thật là số dòng lệnh của **một** ảnh PM *(`3.772`)*, và nó ⛔ **không** lớn theo kích thước sổ. ⛔ Đừng "tối ưu" bằng cách đưa phép chuẩn hoá vào SQL — đó đúng là cái đã cho ra `121` thay vì `250`.

**`lenh-cho/summary`** trả `theo_tien_te[]`: `curr` · `so_dong` · `so_phieu` · `tien` · `so_dong_duyet` · `so_dong_chua_duyet` · `so_dong_phu` · `pct_that`. ⛔ **Không có dòng "tổng"**.

⭐ `so_phieu` đếm **DISTINCT**: `526` phiếu mang **2–36** reference khác nhau *(`CR#6`)*, nên *"bao nhiêu dòng"* và *"bao nhiêu phiếu"* là **hai con số**, và màn phải nói được cả hai.

⭐⭐ `so_dong_phu` có thể là **`null`** = ⛔ **KHÔNG ĐO ĐƯỢC** *(Σ tiền của tiền tệ ấy = `0` ⇒ câu hỏi ⛔ không có nghĩa)*. Màn hình **PHẢI** vẽ nó khác `0`: vẽ `0` nói *"xem 0 dòng là đủ"* — một câu **sai**, và sai theo hướng **nguy hiểm** *(kế toán bỏ qua cả tiền tệ ấy)*. Có bài ghim ở tầng màn hình.

**`itl-candidates`** trả `dong_lenh` · `dung_sai` · `ung_vien[]` · `bi_cat` · `tong_cung_tien_te` · `canh_bao` · `anh_pm` · `pham_vi`.

⭐ Bốn bậc **soi gương** chiều thuận, và **tên bậc giữ y nguyên**: `ma` › `tien` › `gan_tien` › `cung_tien_te`. Đổi tên ở một phía sẽ làm người đọc tưởng đây là **hai thang đo khác nhau**.

⭐ *(v3.9, `KQ-036 F-6`)* **Trong bậc `ma`: dòng CÙNG tiền tệ đứng trước dòng khác tiền tệ** *(rồi `itl_id` như cũ)*. ⛔ **Không** hạ dòng khớp mã khác tiền tệ xuống dưới ba bậc tiền: với lệnh có nó, nó là **bằng chứng duy nhất** *(sổ thật 84 / 84)*, còn bậc tiền bên dưới là trùng tiền tình cờ *(đoạn rổ ⓐ trên)*. Hạ nó xuống là đặt một cặp **cửa ghi nhận mà sai** lên dòng đầu. An toàn đã nằm ở chỗ khác: màn ⛔ chọn sẵn ứng viên nào *(`INV-I16`, `man_f01_ghep.js:28`)* và đã nói *"khác tiền tệ ⇒ cửa ghi sẽ TỪ CHỐI"* *(`WO-032`)*; thứ máy **đề xuất** là `the.gd`, và nó đi theo rổ ⓑ. Thứ tự đủ: `ma` cùng tệ › `ma` khác tệ › `tien` › `gan_tien` › `cung_tien_te`. Sổ thật hôm nay **0** lệnh có **cả hai** loại dòng khớp mã ⇒ thứ tự này **chỉ đo được trên kho TEST** *(`Đ3`)*.

⛔⛔ **Bậc `ma` tính ở PYTHON bằng `canon_ref`, ⛔ KHÔNG bằng một câu `regexp` trong SQL** — và đây là một **ràng buộc THẬT của kho**, ⛔ không phải một lựa chọn: `fls_pm_line.ref_canon` đã chuẩn hoá *(lưu sẵn lúc nạp)*, nhưng phía ITL kho **chỉ có `doc_no` THÔ** — ⛔ không một cột chuẩn hoá nào. Một câu `regexp_replace(i.doc_no,'[^A-Za-z0-9]','','g')` là **bản thứ hai** của `canon_ref` và nó ⛔ **không tương đương**: `canon_ref` còn gỡ **ký hiệu khoa học** *(`4.36619E+15` → `4366190000000000`)*, chuẩn hoá `NFKC`, và loại **ô lỗi** *(`#N/A`)*.

⭐ **Và nó ⛔ không phải giả thuyết:** con số *"`560` dòng ghép được ngay"* đo ngày 09/09 bằng đúng câu `regexp` ấy; luật **THẬT** cho **`475`** — lệch **`17,9%`**. Có bài ghim ở cả hai tầng, và **đã diễn tập**: đổi sang `regexp` ⇒ bài ĐỎ.

⛔⛔ **Bậc `cung_tien_te` của chiều NGƯỢC BỊ CẮT, và cửa KHAI RA mình đã cắt** *(`bi_cat` + `tong_cung_tien_te`)*. Đây là một **bất đối xứng THẬT**: chiều thuận hỏi *"dòng lệnh nào cho dòng tiền này"* — tập ứng viên là **3.772**; chiều ngược hỏi *"dòng tiền nào cho dòng lệnh này"* — tập ứng viên là **10.030**, và riêng bậc *"cùng tiền tệ"* có thể trả về **hàng nghìn** dòng ⛔ không nói lên điều gì. Cắt mà **im** là một mặc định im lặng: người gõ sẽ tưởng danh sách là **đầy đủ** và kết luận *"⛔ không có dòng tiền nào khớp"*.

⭐ `dung_sai` lấy từ **cùng phép dung sai mà cửa GHI dùng** *(`dung_sai_ghep_tay`)*. Một bản riêng ở tầng đọc sẽ **vẽ một ứng viên vào bậc `gan_tien` rồi cửa ghi TỪ CHỐI nó** — một cái bẫy.

`404 FLS-NOT-FOUND` khi `pm_line_id` ⛔ không có trong **ảnh chụp hiệu lực** của phạm vi — **cùng một câu trả lời** cho *"⛔ không có"* và *"có nhưng ngoài phạm vi"*.


### ⓹ ⛔ Hai cái NỔ

| Khi | HTTP | Vì sao ⛔ không thể nhẹ hơn |
|---|:--:|---|
| thân mang `pm_line_ids` hay `force`, hay `itl_ids` rỗng | **400** | Câu lỗi **chỉ ra cửa đúng** *(`POST /queue/{itl_id}/match`)* |
| có dòng ⛔ **không tự chứng** *(hay ngoài phạm vi / đã nối)* | **422** · `FLS-GHEP-KHONG-TU-CHUNG` | ⛔ **CẢ LÔ**, ⛔ 0 mối nối mới. Phần `khac.dong[]` nêu **`ly_do` từng dòng** + một **câu tiếng Việt** — bốn cổng của `ghep_lenh` dẫn người đọc đi **bốn đường sửa khác nhau**, nên một câu chỉ nói *"⛔ không tự chứng"* sẽ làm họ đi sửa dung sai trong khi dòng ấy khác **TIỀN TỆ** |

⭐ Bấm **lần hai** trên cùng danh sách ⇒ **422** *(`ngoai_pham_vi_hay_da_noi`)*, ⛔ **không** phải `200` với *"0 dòng"*: một cú bấm lại mà trả `200` sẽ làm người ta tưởng nó vừa ghép thêm.

### ⓺ ⭐⭐ Màn hình PHẢI nói ra con số NHỎ

Khối ghép lô ở `F01` vẽ **ba thứ cùng lúc**: bấm được **68** dòng · bốn lý do từ chối **kèm số dòng** · và **`6.577` dòng nút thắt thật** *(có mã chuẩn hoá được mà ⛔ KHÔNG một dòng PM nào mang mã ấy ⇒ thiếu **dữ liệu lệnh chi**, việc của mốc `A3`)*.

⛔ Và `0` dòng tự chứng ⛔ **KHÔNG** phải trạng thái RỖNG: đúng lúc ấy khối này mới cần nói *"việc nằm ở chỗ khác"*. Coi `0` là rỗng thì màn biến mất **đúng vào ngày** cửa ghép lô hết việc, và ⛔ không ai còn thấy `6.577`.

### ⓻ ⛔⛔ Một khuyết tật THẬT trong mã, do chính phép đo bắt

Bản đầu của `ds_tu_chung` xét *"đã bị ghép"* **TRƯỚC** *"cùng tiền tệ"* ⇒ **202 dòng** khác tiền tệ bị dán nhãn `lech_tien_ngoai_dung_sai`. Người đọc sẽ đi **nới dung sai** để chữa một chuyện ⛔ không liên quan gì đến dung sai. ⇒ Bốn tên lý do nay **soi gương bốn cổng của `ghep_lenh` theo ĐÚNG thứ tự nó kiểm**: `ⓔ` tiền tệ → `ⓒ` đã ghép → `ⓖ` chưa duyệt → `ⓕ` lệch tổng.

## §4h · ⭐⭐⭐ CỬA CHO MÀN GÁN LỆNH CHI — chặng `B0` của plan *(mới 2026-09-21, `QĐ-ITL-148`)*

> ⭐⭐ **Mục này lấp `4` GAP hạng chặn của audit `21/09`** — `GAP-API-07` · `GAP-SCR-22` · `GAP-SCR-23` · `GAP-SPEC-04`. ⛔ Mỗi luật dưới đây **đo trên kho**, ⛔ không suy từ bản dựng: bản dựng mang **dữ liệu mẫu**, và nó đã lừa tôi một lần *(`BA-06 §4.5 ⓗ ①`)*.

### ⓵ ⭐⭐⭐ Khuôn `ung_vien[]` — **`10` trường**, và trước mục này nó có **`0`**

⛔⛔ `§4g ⓹` khai `itl-candidates` trả `ung_vien[]` rồi **dừng**. Người dựng ⛔ không có gì để nhận ngoài một chuỗi, nên bản dựng **cắt chuỗi hiển thị** để lấy lại cấu trúc — một cấu trúc **giả**.

| Trường | Kiểu | Nguồn | ⛔ Bẫy |
|---|---|---|---|
| `itl_id` | `bigint` | `fls_itl.itl_id` | ⛔ **⛔ KHÔNG lên màn** *(`UI-F8`)* — chỉ để gửi lại ở cửa GHI |
| `doc_date` | `date` | `fls_itl.doc_date` | **8.387/8.387** |
| `doc_no` | `text \| null` | `fls_itl.doc_no` | `8.383` — `4` dòng ⛔ không có ⇒ **null**, ⛔ không chuỗi rỗng |
| ⭐ `dien_giai` | `text \| null` | khung xem `fls_dien_giai` | xem `⓺` — **`null` có HAI nghĩa**, cửa phải tách |
| `amount` | `numeric` | `fls_itl` | |
| ⭐ `chieu` | `'no' \| 'co'` | xem `⓷` | ⛔ **⛔ KHÔNG** lấy từ `pay_type` |
| `curr` | `text` | `fls_itl.curr` | |
| ⭐ `nguon` | **object** `{tk, bank, curr, le}` | xem `⓶` | ⛔ **object, ⛔ KHÔNG phải chuỗi** |
| ⭐ `bac` | `'ma' \| 'tien' \| 'gan_tien' \| 'cung_tien_te'` · ⭐ *(v3.7)* `'khac_tien_te'` **chỉ ở cửa `/so`** *(`⓹`)* | `canon_ref` ở **Python** | ⛔ Tên bậc **giữ y nguyên** hai chiều *(`§4g ⓹`)*. ⛔ Màn gặp bậc **lạ** ⇒ in nguyên tên, ⛔ rơi về `cung_tien_te` *(hôm nay `man_f01_ghep.js:428` `BAC[uv.bac] \|\| BAC.cung_tien_te` — nói dối im lặng)* · ⭐ *(v3.9, `KQ-036 F-3`)* ở **mọi** hàm vẽ ký hiệu bậc — kể cả khối *"Đang gán"* *(`ve_dang_gan`, hôm nay bỏ chip **im lặng**)*. ⭐ *(v3.9, `KQ-036 F-2`)* `khac_tien_te` **cũng** ở `the.gd`/`the.gd_ds` *(`⓵'`)*: thứ tự chia **giống hệt** `/so` — `ma` *(khớp mã, mọi tiền tệ)* › **khác tiền tệ** ⇒ `khac_tien_te` › `tien` › `cung_tien_te`; cửa `itl-candidates` vẫn ⛔ sinh nó *(ba bậc tiền ở SQL đã lọc cùng tiền tệ)*. ⭐ *(v3.9, `KQ-036 F-1`)* mọi phép so tiền tệ của phép chia bậc dùng **cùng** hàm với `lech` *(`man_ghep.ma_tien_te` — `trim` + chữ hoa)*; hôm nay `xu_ly._bac:764` so bằng bản riêng ⛔ `trim` *(sổ thật **0** giá trị `curr` có khoảng trắng ⇒ **0** ca)* |
| `lech` | `numeric \| null` | ~~`amount` ứng viên − dòng lệnh~~ ⭐ *(v3.7, `KQ-031` `F-2`)* **`\|amount ứng viên − amount dòng lệnh\|`** — **trị tuyệt đối** *(đúng mã `lenh_cho.py:200` từ trước; thứ tự xếp dùng chính nó)* | ~~`null` khi **khớp tuyệt đối**~~ ⭐ *(v3.7)* **Có số ở MỌI bậc** *(kể cả `ma`)* và ở **MỌI cửa trả khuôn này** *(`itl-candidates` · `/so` · `the.gd` · `the.gd_ds` — so với dòng lệnh **của chính cửa/thẻ**)*; khớp tuyệt đối ⇒ **`0`**, ⛔ `null`. **`null` ⇔ ⛔ so được**: tiền tệ ứng viên ≠ tiền tệ dòng lệnh *(so sau `trim` + chữ hoa)*, hoặc một bên thiếu `amount`/`curr`. ⛔ `null` vì *"bậc `ma`"*. Đo `KQ-031` *(8088, rổ `may` 268 lệnh)*: hôm nay **338 / 448** ứng viên bậc `ma` có tiền ≠ tiền lệnh mà `lech = null` *(mã `lenh_cho.py:420`)*; cửa `/so` + `the.gd`/`gd_ds` trả `null` ở **mọi** dòng *(`man_ghep.py:306` · `xu_ly.py:683`/`:717` — `lech_tuyet_doi=None`)* |
| ⭐ `loi_nguon` | `text` — **CHỈ CÓ khi `nguon` là `null`** | `23/09` | ⛔ Khoá này **vắng mặt** ở ca thường, ⛔ không phải `null`: một khoá luôn có mặt sẽ đẩy tầng trên vào thói quen **kiểm giá trị thay vì kiểm sự tồn tại** — hai phép kiểm ấy lệch nhau ở đúng ca `null` |
| ⭐ `dien_giai_vi_sao` | `'rong' \| 'chua_noi_duoc'` — **CHỈ CÓ khi `dien_giai` là `null`** | `⓺` | *(v3.7 — khai vào bảng; luật đã ở `⓺` từ v3.0, mã `man_ghep.py:205`)* cùng kiểu *"vắng mặt ở ca thường"* như `loi_nguon` |
| ⭐ `khoa_to` | `text[]` — **luôn có mặt**; `[]` khi ⛔ tô gì | `mg.khoa_bang_chung(thẻ lệnh, ứng viên)` — gắn ở **tầng cửa** *(`xu_ly.py::_gan_khoa_to`)* | *(v3.7, `KQ-031` `F-3`)* Các chuỗi màn tô `<mark>` trong `dien_giai`, **dài trước** *(chồng nhau ⇒ HTML vỡ)*; ba nguồn, mỗi nguồn một điều kiện: số chứng từ **trùng đúng** · số tiền **khớp tuyệt đối CẢ đơn vị tiền** · tên bên nhận sau lọc từ rác. ⛔ Màn tự tính *(luật nghiệp vụ, ⛔ mẹo hiển thị)*. Có ở **mọi** cửa trả khuôn này — kể cả `the.gd`/`the.gd_ds` *(`⓵'`)*: đo `KQ-031` 8088 hôm nay **0 / 768** `gd` mang khoá ⇒ khối *"Đang gán"* ⛔ bao giờ tô bằng chứng, trong khi bài `tests/web/test_b3_cuon_va_khoi_dang_gan.py:34` **tự nhét** `khoa_to` |

⭐ *(v3.7)* Bảng trên nay **`13`** trường *(`10` gốc + `loi_nguon` 23/09 + `dien_giai_vi_sao` + `khoa_to`)*; tên mục giữ *"`10` trường"* làm biên bản. ⛔⛔ **Luật cho bài thử của mọi cửa trả khuôn này:** thân dùng để vẽ màn trong bài phải **lấy từ cửa thật trên kho TEST** — một khoá do bài tự đặt là cách lớp lỗi *"khuôn thử tự nhét"* sống sót **ba lần** *(`KQ-019` `HT.hoi` · `KQ-029 F-1` `u.tien` · `KQ-031 F-3` `khoa_to`)*.

⛔⛔⛔ **`tach_nguon` ⛔ KHÔNG còn được ném từ trong khuôn này** *(sửa `23/09`)*. Nó ném khi `source_sheet` sai khuôn — **đúng ở tầng đọc** *(`INV-I16`: máy ⛔ không đoán)*. ⛔ Nhưng khuôn này chạy trên **từng dòng của một DANH SÁCH**, và một ngoại lệ ở đây trả `500` cho **cả trang** ⇒ kế toán mất **`50` ứng viên** vì **một**. ⭐ `nguon: null` ＋ `loi_nguon` — một trạng thái **đã có tên** ở `DUONG_RA`; và nó **giữ lại** `dien_giai`/`amount`, tức người ta vẫn đọc được **bằng chứng** dù ⛔ không biết dòng tiền ấy từ tài khoản nào.

⛔⛔⛔ **Và một vi phạm hợp đồng sống `2` ngày:** tuyến `/queue/lenh/{pm_line_id}/itl-candidates` — **đường chính, ứng viên do MÁY đề xuất** — trả **HÀNG THÔ** từ SQL *(`tien` · `ps_no` · `ps_co` · `source_sheet`)*, ⛔ **không** đi qua khuôn trên. Màn đọc `amount` · `chieu` · `nguon` ⇒ **hai cột rỗng**, và phép so *khớp đúng tiền* so `Number(undefined)` ⇒ **MỌI ứng viên đều thành *"lệch"*** ⇒ nút `Gán` luôn đi đường cảnh báo: **một phép khớp ĐÚNG được trình bày như một phép khớp SAI**.
⛔⛔ Nó sống sót vì bài thử cũ chỉ hỏi `bac` và `itl_id` — **đúng hai khoá mà hàng thô TÌNH CỜ cũng có**. ⭐ Một bài thử hỏi **vài khoá giao nhau** thì ⛔ **không bao giờ** thấy **hai khuôn là HAI**; phép đo đúng là hỏi **cả `10` trường của hợp đồng**. ⇒ `tests/api/test_cua_lenh_cho_pg.py::test_UNG_VIEN_TIEN_tra_dung_KHUON_HOP_DONG…` ＋ `test_HAI_CUA_ung_vien_noi_CUNG_MOT_KHUON`.
⭐ Cửa `/so` *(Toàn sổ)* **đã** nắn khuôn từ đầu ⇒ **hai cửa nuôi MỘT hàm vẽ mà nói HAI thứ tiếng** — và ảnh chụp của owner ⛔ không lộ ra vì màn lúc ấy ở chế độ Toàn sổ, tức cửa **KIA**.

### ⓵' ⭐⭐ `gd` ＋ `gd_ds` trên **hai cửa danh sách** *(mới 23/09)*

`/queue/lenh-cho` và `/queue/lenh-da-gan` trả `ung_vien_itl[]` / `itl_da_gan[]` — **chỉ ID**. Bảng sổ `11` cột cần `diễn giải` · `số tiền` của giao dịch, và khối `C4` cần **cả chùm**.

| Khoá | Ở đâu | Là gì | ⛔ Bẫy |
|---|---|---|---|
| `the.gd` | **cả hai** cửa | **một** giao dịch — đã gán *(nếu có)*, ⛔ không thì đề xuất đầu của máy | `da_gan: bool` phân biệt *đã chốt* với *máy đề xuất* — hai thứ ⛔ **KHÔNG** được trông giống nhau |
| ⭐ `the.gd_ds` | **chỉ** `lenh-da-gan` | **MỌI** dòng tiền đã gán | ⛔ Với dòng ⛔ chưa gán, `ung_vien_itl` là **đề xuất của máy** *(tới `20` dòng)* — cho cả `20` vào đây là trộn *"đã chốt"* với *"máy đoán"*, đúng thứ `§6.3` của hợp đồng thiết kế cấm |
| ⭐ `the.vi_sao` *(v3.10, `TL-038`)* | **chỉ** `lenh-cho` *(+ `/ro`)* · **chỉ có mặt** khi `gd = null` **và** `lc.la_khop_ma_chi_khac_tien_te(dòng)` — **vắng** ở mọi thẻ khác | **chính** `vi_sao` của hàng *(câu `ma_khop_khac_tien_te`)* — ⛔ sự thật thứ hai, ⛔ câu màn ghép | ⛔ Chép `vi_sao` vào `the` cho **mọi** hàng *(`HOI-038` phương án A — **616** ô đổi, **532** lệnh ⛔ số chứng từ mất *"— chưa chọn"*)*; ⛔ để màn tự nhận câu nào là câu thứ sáu *(phương án C — luật thứ hai ở JS, `BA-06 §4.5 ⓟ` cấm)*. Cùng kiểu *"vắng ở ca thường"* của `loi_nguon` / `dien_giai_vi_sao`. Sổ thật *(`BG-039`, ảnh `NAP-2026-10-02-PMA07ED283`)*: có mặt **84** thẻ trên `may` ＋ `nguoi` **800** — đúng tập rời `may` |

⭐ *(v3.7, `KQ-031` `F-2`/`F-3`)* Mỗi phần tử `gd` / `gd_ds` là **đúng khuôn `⓵`** ＋ `da_gan` — **đủ** trường, kể cả `lech` *(so với dòng lệnh **của chính thẻ**)* và `khoa_to`. ⛔ Một khuôn *"rút gọn cho danh sách"*: màn có **một** hàm vẽ bằng chứng, và nó ⛔ được biết thân đến từ cửa nào. Sổ thật 02/10 *(`fls-ba`, chỉ `SELECT`)*: mối nối khác tiền tệ với dòng lệnh **0 / 2.262** ⇒ với `gd` **đã gán**, `lech = null` hôm nay ⛔ xảy ra; với `gd` **máy đề xuất** *(bậc `ma` khớp mã, ⛔ lọc tiền tệ)* thì có.

⭐ **MỘT** truy vấn cho **cả trang** *(`lc.gd_theo_itl`, dùng lại đúng `_SQL_ITL_THEO_ID` của bậc `ma`)* — ⛔ không `738` lượt gọi cửa cho một lần mở màn. ⛔ Viết câu SQL thứ hai là tạo **bản sự thật thứ hai** về *"một dòng tiền trông thế nào"*.

⭐⭐ Đo `23/09` trên `2.219` lệnh đã gán: **`23` (`1,0%`)** gán **hơn một** dòng tiền, nhiều nhất **`7`**. ⛔⛔ Một `1,0%` là cớ để **⛔ không bật hộp thoại xác nhận** *(`QĐ-ITL-148 ⓔ`)* — ⛔ **không** phải cớ để **giấu mất sáu dòng tiền**. Giá của `gd_ds`: tập `id` tăng từ ~`500` lên ~`505` mỗi trang — **một** truy vấn vẫn là **một**.

⭐⭐ *(v3.8, `TL-033` — `HOI-033`)* **`bac` của `gd`/`gd_ds` so với `canon_ref(ref_tho)` của CHÍNH dòng lệnh, ở CẢ HAI cửa danh sách.** Bậc `ma` đòi biết **mã của dòng lệnh**; cửa `lenh-cho` có nó vì chạy `xep_ro` *(gắn `ma_canon`)*, cửa `lenh-da-gan` **⛔ chạy** ⇒ `_bac` ⛔ bao giờ ra `ma` ở cửa ấy. Đo sổ thật 02/10 *(`fls-ba`, chỉ đọc, gọi hàm thật mọi trang)*: mối nối `gd_ds` khớp mã **2.262 / 2.262**, cửa trả `ma` **0** *(`tien` 2.128 · `cung_tien_te` 134)*; khối *"✓ Đang gán"* *(`gd`, một mỗi lệnh)* chip `①` **0 / 2.219** *(`②` 2.121 · `④` 98)*. Luật: phép chia bậc của `gd`/`gd_ds` **giống hệt** khuôn `⓵` — `ma` khi `canon_ref(doc_no) == canon_ref(ref_tho)` của dòng lệnh, rồi mới tới `tien` › … ; **một** chỗ gắn mã dòng lệnh dùng chung cho cả hai cửa *(⛔ bản thứ hai của phép chia `canon_ref`)*. Mã ⇒ `WO-032` vòng 2 `(i)`.

⭐⭐ *(v3.9, `KQ-036 F-2` + `F-6`)* **`the.gd` của lệnh CHƯA gán *(`da_gan = false`)* ⛔ bao giờ là dòng khác tiền tệ** — nó là phần tử đầu của `ung_vien_itl`, và theo `§4g ⓹` rổ ⓑ danh sách ấy chỉ mang dòng khớp mã **cùng** tiền tệ. Đo hôm nay *(sổ thật chỉ đọc, hàm thật)*: **84 / 268** lệnh rổ `may` có `gd` khác tiền tệ — `gd` trùng ứng viên đầu của `itl-candidates` **268 / 268** ⇒ đó **là** *"đề xuất đầu của máy"* trên cột *Giao dịch* *("đề xuất: …")*; mong **0**. `gd`/`gd_ds` **đã gán** mà khác tiền tệ ⛔ khớp mã *(mối nối dựng ngoài cửa ghi — cửa ghi chặn mọi cặp khác tiền tệ)* ⇒ `bac = 'khac_tien_te'`, ⛔ `cung_tien_te`; sổ thật **0 / 2.262** mối nối khác tiền tệ ⇒ ca biên, đo trên kho TEST. Mã ⇒ `WO-037`.

### ⓶ ⭐⭐ Tách `nguon` — và **mọi tài liệu trước mục này trích SAI giá trị thật**

⛔⛔ Giá trị trong kho mang **tiền tố `R \| `** — đo **`8.387/8.387`**:

```
kho thật :  R | PO2_OCBC USD_SGO2
tài liệu :  604046904001_OCBC SGD_SGO2      ⛔ thiếu tiền tố
```

⇒ Một phép tách chép theo tài liệu **hỏng ngay ký tự đầu**.

| Bước | Luật | Đo |
|---|---|---|
| 1 | Bóc tiền tố `R \| ` *(tên tầng sheet nguồn)* | **`8.387/8.387`** có tiền tố |
| 2 | Cắt theo `_` ⇒ **3** mảnh: `<tk>` · `<bank> <curr>` · `<le>` | **`8.387/8.387`** đúng khuôn trên **`49`** nguồn |
| 3 | Mảnh giữa cắt theo khoảng trắng ⇒ `bank` ＋ `curr` *(`curr` là **3 chữ hoa**)* | như trên |
| ⚠ 4 | `tk` rút còn **4 số cuối** — ⛔ **CHỈ KHI** nó toàn chữ số | ⛔ **`6`** tài khoản ⛔ không phải số: `PO1` · `PO2` · `PO3` · `PO5` · `PO6` · `PO9` *(tài khoản thẻ)* ⇒ **giữ nguyên**, ⛔ không ra `••PO2` |

### ⓷ ⭐⭐ Chiều `Nợ/Có` — luật này CHƯA TỪNG được viết, và dự án đã đọc nhầm một lần

| Đo trên `fls_itl` | Dòng |
|---|--:|
| Mang **cả hai** ô `ps_no` ＋ `ps_co` | **3.691** *(44%)* |
| ⭐ Trong đó **cả hai đều khác `0`** | ⛔ **`0`** |
| Chỉ `ps_no` | 829 |
| Chỉ `ps_co` | 3.867 |

⇒ **Luật: bên nào ≠ `0` thì đó là chiều.** `Nợ` = tiền **vào** · `Có` = tiền **ra** *(`BA-06 §3c ⑤`)*.

⛔⛔ **⛔ KHÔNG lấy dấu từ `pay_type`** — đã sai một lần theo đúng đường ấy. Vì `0` dòng nào có cả hai ô khác `0`, luật này **⛔ không có ca nhập nhằng**, và đó là điều phải ghim bằng một bài thử.

### ⓸ ⭐⭐⭐ Đổi **sê-ri Excel → ngày** — gốc `1900`, và nó được ĐO chứ ⛔ không chọn

⛔ Kho có **`3.772/3.772`** ô `Timestamp` là **sê-ri**, **`0`** dòng có dấu ngày. Chọn sai gốc lệch **4 năm 1 ngày** — và ⛔ không ô nào trên màn nói cho biết đã chọn gốc nào.

| Gốc | Dải ngày ra | Lệch so với ngày dòng tiền **đã nối** |
|---|---|---|
| ⭐ **`1900`** *(nền `1899-12-30`)* | `2025-03-10` … `2026-08-29` | **trung vị `3` ngày** · `285/400` trong vòng `7` ngày |
| `1904` | `2029-03-11` … `2030-08-30` | trung vị **`1.462`** ngày · `0/400` |

⇒ ⭐⭐ **Phép kiểm dùng một nguồn ĐỘC LẬP**: ngày của **dòng tiền đã nối** *(`fls_itl.doc_date`)*, ⛔ không phải một dải ngày *"trông hợp lý"*. Dải ngày một mình ⛔ không đủ — `1904` cho `2029` trông sai, nhưng nếu lệch nhỏ hơn thì mắt ⛔ không bắt được.

⭐ **`3` ngày là một sự thật nghiệp vụ:** lệnh chi lập **trước**, tiền ra **sau**.

### ⓹ Tuyến **thứ 36** — `GET /queue/lenh/{pm_line_id}/so` *(tra cứu TOÀN SỔ)*

| | |
|---|---|
| Vì sao **⛔ không** dùng `GET /ledger` | `ledger` lọc `?period=&le=&status=` — ⛔ **không tìm chữ**, và ⛔ **không biết lệnh nào đang mở** nên ⛔ không tính lại bậc được |
| Tham số | `?q=` *(tìm trong `dien_giai` ＋ `doc_no`)* · `?limit=` · `?cursor=` |
| Trả | **cùng khuôn `ung_vien[]`** của `⓵` — ⛔ không khuôn thứ hai |
| ⭐⭐ Bậc | **tính lại theo `pm_line_id`**: khớp `canon_ref` ⇒ `ma` · đúng tiền ⇒ `tien` · còn lại ⇒ `cung_tien_te` · ⭐ *(v3.7)* ~~còn lại~~ còn lại **cùng tiền tệ** ⇒ `cung_tien_te`, **khác tiền tệ** ⇒ **`khac_tien_te`** *(⛔ `cung_tien_te`)*. ⛔ Cửa này là **toàn sổ**, ⛔ lọc tiền tệ ⇒ mã hôm nay *(`man_ghep.py:305` nhánh `else`)* dán *"cùng tiền tệ"* lên **mọi** dòng khác tiền tệ. Tầm *(02/10, `fls-ba`, chỉ `SELECT`)*: dòng sổ chưa nối **6.165** — USD **3.766** · VND **2.239** · SGD **140** · HKD **20** ⇒ với một lệnh VND, **3.926 / 6.165** dòng toàn sổ mang nhãn sai. ⛔ Lọc bỏ chúng: toàn sổ trả lời *"sổ có những dòng nào"* — người phải **thấy** tiền đã đi bằng ngoại tệ; màn chỉ ⛔ được gọi chúng là *"cùng tiền tệ"* và ⛔ được mời gán *(cửa ghi `422`)* |
| ⛔⛔ Bẫy | Bậc `ma` phải tính bằng **`canon_ref` ở Python**. Đo: `regexp` trong SQL cho **`560`**, luật thật cho **`475`** ⇒ lệch **`17,9%`** |

⭐ Vì sao cửa này ⛔ **không phải tính năng phụ**: nó **bật sẵn** với lệnh máy ⛔ không tìm được ứng viên nào ⇒ nó là **lối thoát khỏi ngõ cụt** của **`768`** dòng. ⛔ ⛔ Không có nó thì màn **là** ngõ cụt.

### ⓺ `dien_giai` — `null` có **HAI nghĩa**, và cửa phải tách

| Trạng thái | Dòng | Cửa trả |
|---|--:|---|
| Nối được, **có chữ** | **8.358** | `dien_giai` = chuỗi |
| Nối được, ⛔ không chữ | **3** | `dien_giai` = `null` · `dien_giai_vi_sao` = `"rong"` |
| ⛔ **⛔ Không nối được** | **26** | `dien_giai` = `null` · `dien_giai_vi_sao` = `"chua_noi_duoc"` |

⛔⛔ **Gộp hai ca cuối thành một `null` là đúng thứ `INV-I16` cấm:** *"giao dịch này ⛔ không có nội dung"* và *"FLS ⛔ chưa đọc được"* là **hai câu khác nhau**, và màn phải nói khác nhau.

### ⓻ `unmatch` — trả **danh sách chùm**, và `reason` thành **tuỳ chọn**

⛔ Cửa `POST /queue/{itl_id}/unmatch` *(`QĐ-ITL-69`)* bỏ **TOÀN BỘ** mối nối của dòng tiền và **⛔ không nhận `pm_line_ids`** — bỏ lẻ làm `Σ mối nối ≠ tiền bank`. ✅ **Owner chốt `21/09`: cửa ĐỨNG NGUYÊN, MÀN nói ra thiệt hại** *(`QĐ-ITL-148 ③`)*.

| Đo `21/09` | |
|---|--:|
| Dòng tiền đã có mối nối | **2.222** |
| ⭐ Mang **chùm** *(>1 mối nối)* | **25** = **1,1%** |
| Chùm lớn nhất | **10** dòng lệnh trên một dòng tiền |
| Mối nối nằm trong một chùm | **65/2.262** = 2,9% |

⇒ **Hai thay đổi:**

| # | Đổi | Vì sao |
|:-:|---|---|
| ⓐ | ⭐ Thêm `GET /queue/{itl_id}/chum` — trả **danh sách dòng lệnh** sẽ bị gỡ | Màn **phải hỏi trước** ở `1,1%` ca ấy, và hỏi **kèm tên từng dòng**. ⛔ Một nút `Bỏ gán` im lặng sẽ gỡ tới **9** dòng lệnh người dùng ⛔ không định động tới |
| ⓑ | `reason` trong thân ⇒ **TUỲ CHỌN** | `QĐ-ITL-137` **đã hoãn** cột lý do ⇒ màn ⛔ không thu lý do nào. ⛔ Để `reason` bắt buộc là đòi một thứ màn ⛔ không có |

⚠ **`GET /queue/{itl_id}/chum` là tuyến thứ 37.**

⛔ **Đính chính v3.4 *(`KQ-002 F-1`, 01/10)*:** dòng ⓑ khai `reason` tuỳ chọn từ v3.0, nhưng mã **cả hai tầng** vẫn bắt *(`fls/api/xu_ly.py:458` `_chu(yc.than, "reason")` · `fls/repo/ghi_tay.py:776` `ThieuLyDo`)* ⇒ nút `Bỏ gán` trên máy thật trả **`400`**. Lỗi **mã**, ⛔ lỗi spec — luật thống nhất ở `⓼` dưới, sửa ở `WO-003`.

### ⓼ ⭐⭐⭐ `reason` TUỲ Ý cho cả `match` lẫn `unmatch` — và vết **⛔ BAO GIỜ rỗng** *(mới v3.4, `QĐ-ITL-149`)*

Owner 01/10, nguyên văn: ***"bỏ yêu cầu lý do cho cú Ghép"***. Căn cứ đo *(`KQ-002 F-1`, `CHAN`)*: màn ghép **⛔ có ô lý do** *(`QĐ-ITL-137` hoãn)* ⇒ màn gửi `{pm_line_ids:[…]}` cho `Gán` và `{}` cho `Bỏ gán` *(`man_f01_ghep.js:556`, `:599`)*, cửa đòi `reason` ⇒ **`400`** cả hai. ⛔ Không bài nào thấy vì bài cửa tự gửi `{"reason": "x"}` *(`tests/web/test_vong_f01_pg.py:164`, `:190`, `:287`)*.

| Cửa | Thân | `reason` thiếu / rỗng / toàn khoảng trắng | `reason` có |
|---|---|---|---|
| `POST /queue/{itl_id}/match` | `{pm_line_ids, reason?}` | ⭐ **được** — máy ghi **lý do mặc định** `LY_DO_MAC_DINH_GHEP` | ghi đúng chữ người gửi |
| `POST /queue/{itl_id}/unmatch` | `{reason?}` | ⭐ **được** — máy ghi `LY_DO_MAC_DINH_BO_GHEP` | ghi đúng chữ người gửi |
| `POST /queue/match-lo` | `{itl_ids, reason}` | ⛔ **`400` — GIỮ NGUYÊN** | — |

**Hai hằng — chuỗi là HỢP ĐỒNG, khai một chỗ trong mã** *(`fls/repo/ghi_tay.py`)*:

```
LY_DO_MAC_DINH_GHEP    = "(may dien) ghep tren man - nguoi bam khong ghi ly do"
LY_DO_MAC_DINH_BO_GHEP = "(may dien) bo ghep tren man - nguoi bam khong ghi ly do"
```

⭐ **Vì sao điền mặc định, ⛔ để rỗng** *(quyết trong thẩm quyền spec)*:
- ⓐ **Lỗ đã cắn 27/08** *(chú thích `ghi_tay.py:544`–`548`)*: một phép ghép đi qua với `reason` **rỗng** ⇒ sổ vết có dòng ⛔ trả lời được *"vì sao"*. Mặc định có nhãn ⇒ cột `reason` **⛔ bao giờ rỗng**, và người đọc vết **phân biệt được** *"người ⛔ ghi lý do"* với *"lý do bị mất"* — đúng tinh thần `INV-I16` *(⛔ giấu chỗ trống)*.
- ⓑ **Điền ở tầng REPO, ⛔ ở cửa** *(`ghep_lenh` / `bo_moi_noi`)*: mọi đường gọi *(cửa HTTP, công cụ, bài thử)* nhận **cùng một** hành vi — hai chỗ điền là hai chỗ để chúng lệch. Hệ quả: `ThieuLyDo` **⛔ còn** được ném từ hai hàm ấy; `_them()` *(cửa `/adjust`)* **giữ** luật bắt buộc.
- ⓒ **Tiền tố `(may dien)` ASCII**, cùng giọng với các lý do máy đã ghi *(`may tu ghep …`, `… · ghep tay N dong lenh`)*: lọc được bằng `reason LIKE '(may dien)%'`; ⛔ trùng tiền tố `UAT ` mà `WO-001 T1b` lọc.
- ⓓ ⚠ **Nhãn nói *"chữ do máy điền"*, ⛔ nói *"máy bấm"*.** `actor` **vẫn là người** *(lấy từ THẺ, `§3`)* ⇒ cổng đếm *"người thật đã làm"* *(mốc `B`, `WO-001 T1a`)* **phải** đếm cú bấm này — nó lọc theo **`actor`**, ⛔ theo `reason`.

⛔ **Ngoài phạm vi:** cửa **lô** `match-lo` giữ `reason` bắt buộc — ⛔ có người chọn dòng *(`§4g ⓓ`)*, và owner chỉ nói về **cú Ghép** trên màn. `reverse`, `reopen`, `/adjust` với `force` giữ luật cũ.

---

## §5 · Mã lỗi

| Mã | Khi | HTTP |
|---|---|---|
| `FLS-CONFLICT-SOURCE` | gõ khác nguồn, chưa `force` *(`US-025`)*. ⭐ v3.5: **CHỈ** ca này — ba ca khác từng mượn mã này nay có mã riêng ngay dưới | 409 |
| `FLS-DA-GHEP` ⭐ v3.5 | `POST /queue/{itl_id}/match` trên dòng **đã có** mối nối hiệu lực *(lớp `DaGhep`)*. `khac.moi_noi` giữ nguyên | 409 |
| `FLS-KHONG-CON-MOI-NOI` ⭐ v3.5 | `POST /queue/{itl_id}/unmatch` trên dòng **⛔ còn** mối nối hiệu lực *(lớp `KhongCoMoiNoi` — vd. người khác vừa bỏ gán trước)* | 409 |
| `FLS-CHUA-XONG` ⭐ v3.5 | `POST .../reopen` trên dòng **chưa từng** bấm xong *(lớp `ChuaXong`)* | 409 |
| `FLS-LOCKED-PERIOD` | ghi vào kỳ `locked` *(`INV-I13`)* | 409 |
| `FLS-CONTRACT-DRIFT` | reader lệch `ITL-CONTRACT` *(G1)* | 500, chặn |
| `FLS-DQ-FAILED` | ~~`ACC-1…4` không đạt~~ ⭐ *(đính chính v3.13 — `BA-06` v4.23 `ⓦ` ⑧ ⓐ)* phép **ghi** trái một luật kiểm của **cửa ghi** — khác tiền tệ *(`KhacTienTe`)* · lệch tổng *(`LechTong`)* · lệnh chưa duyệt *(`ChuaDuyet`)* · thiếu lý do *(`ThieuLyDo`)* · đảo một bản đảo / bút toán đã bị đảo · thiếu `actor` *(lớp gốc `LoiGhi`)*. Đo `fls-ba` 05/10 @ `12b7230`: mã này mang ở **5** lớp `ghi_tay.py` *(`:106` · `:213` · `:243` · `:249` · `:255`)*, **0** nơi ném nó từ một cổng `ACC-1…4` *(`grep -rl FLS-DQ-FAILED fls tools` ⇒ chỉ `bao.py` · `ghi_tay.py` · `goi_cua.js`)*. Lý do thật đi trong `chi_tiet`. ⛔ Đổi mã, ⛔ đổi HTTP, ⛔ tách mã *(xem `BA-06` `ⓦ` ⑧ ⓐ — vì sao)* | 422 |
| `FLS-UNMAPPED-HIDDEN` | cố ghi giá trị cứng vào chỗ `UNMAPPED` *(`INV-I16`)* | 422 |
| `FLS-UNKNOWN-CODE` ⭐ | `hd` ⛔ **không có** trong `Mapping Master` *(`DT-I09`)*. ⚠ Lỗi mang **số mã đang giữ** + **tên lệnh nạp lại**, và nếu có mã chỉ khác **hoa-thường** thì **chỉ ra mã thật**. ⛔ `force` ⛔ **không** vượt qua được | 400 |
| `FLS-BAD-FORMAT` ⭐ | giá trị sai **khuôn** — hôm nay chỉ áp `svc_start`/`svc_end`, khuôn **KỲ** `YYYYMM` *(`DT-I09` #6)* | 400 |
| `FLS-ACCR-UNREADABLE` | không đọc được kết quả A-CCR ⇒ cổng số dư chặn | 503 |
| `FLS-UNAUTHORIZED` | ⭐ v1.2 — thiếu thẻ hay thẻ không hợp lệ. ⛔ **Kiểm thẻ TRƯỚC định tuyến**: người không có thẻ ⛔ không được biết đường nào tồn tại. ⛔ Lý do chi tiết *(hết hạn? sai chữ ký?)* **chỉ vào log**, ⛔ không ra ngoài — nói cho người gõ thẻ biết họ sai ở đâu là giúp họ dò thẻ | 401 |
| `FLS-NOT-FOUND` | ⭐ v1.2 — **không có, HAY có nhưng ngoài phạm vi**. ⛔ Cùng một câu trả lời cho cả hai: một `403` nói *"có dòng này nhưng anh không được xem"* — tức là **tiết lộ dòng đó tồn tại** | 404 |
| `FLS-METHOD` | ⭐ v1.2 — đường có, phương thức không. `P4` chỉ đọc nên mọi `PUT`/`DELETE`/`PATCH`/`POST` về đây | 405 |
| `FLS-BAD-REQUEST` | ⭐ v1.2 — tham số sai *(`limit` không phải số, thiếu `?itl_id=`)*. ⛔ Phải là `400`, ⛔ không được thành `500` | 400 |
| `FLS-TOO-LARGE` | ⭐ v1.3 — thân yêu cầu quá to *(> 64 KB)*. ⛔ Máy **từ chối mà không đọc hết** thân — đọc hết là làm đúng cái việc mà giới hạn này dựng ra để tránh — nên nó **đóng kết nối** *(nếu không, byte còn lại sẽ bị đọc thành yêu cầu SAU)* | 413 |
| `FLS-THU-TU-KHONG-TU-CHUNG` ⭐⭐ | `QĐ-ITL-117` — lô khai thứ tự có nguồn **⛔ không tự chứng** *(hết bằng chứng, hay **mâu thuẫn**)*, hay **BẤT ĐỒNG** với bản khai của người. ⛔ **Từ chối CẢ LÔ, ⛔ 0 bản khai mới** — *"thành công 25/27"* là xanh-trên-tập-con. Câu lỗi **nêu TÊN** từng nguồn vướng + câu bằng chứng của nó | 422 |
| `FLS-GHEP-KHONG-TU-CHUNG` ⭐⭐ | `QĐ-ITL-118` — lô ghép lệnh chi có dòng **⛔ không tự chứng**. ⛔ **Từ chối CẢ LÔ, ⛔ 0 mối nối mới**. `khac.dong[]` nêu **`ly_do` từng dòng** + một **câu tiếng Việt**: bốn cổng của `ghep_lenh` *(khác tiền tệ · đã bị ghép · chưa duyệt · lệch tiền)* dẫn người đọc đi **bốn đường sửa khác nhau**, nên một câu gộp sẽ làm họ đi nới dung sai trong khi dòng ấy khác **TIỀN TỆ** | 422 |
| `FLS-INTERNAL` | ⭐ v1.2 — lỗi trong máy. ⛔ **Vết ngăn xếp ⛔ không ra ngoài** *(nó là bản đồ đường dẫn + phiên bản thư viện)*: ghi log, trả mã trơn | 500 |

---

## §6 · Ranh giới — đọc gì từ đâu

| Nguồn | Cách | Ghi? |
|---|---|---|
| `fps_*` / P100 | vendor read-only | ⛔ không |
| A-CCR (BQ) | đọc kết quả, dòng 226 | ⛔ không |
| Google Sheets | Sheets API viewer | ⛔ không |
| **`fls_*` (PG riêng)** | repo layer | ✅ **chỉ append** |
| FPA (BQ ITL) | ⏸ **hoãn** *(`QĐ-ITL-46`)* | — |

---

## §7 · Việc mở

| ID | Việc |
|---|---|
| `GAP-API-01` | Chốt hành vi `409` khi gõ khác nguồn: `force` một lần hay xác nhận từng lần *(`US-025`)* |
| `GAP-API-02` | `weekly` lấy mốc chốt từ đâu — nối `pm_settled_through` |
| ~~`GAP-API-04`~~ ✅ **ĐÓNG 27/08** *(owner chốt đường (a) — `QĐ-ITL-61`)* | ⛔⛔ **`/match` + `/pm-candidates` BỊ CHẶN, ⛔ không phải chưa làm.** Cả hai cần `fps_pm_slip`/`fps_pm_line`, mà **FLS ⛔ không có bảng đó trong kho `fls_*`** *(`QĐ-ITL-45`: FLS đọc `fps_*` chỉ-đọc, nhưng đường đọc đó **chưa tồn tại** — bộ nạp ghép PM lấy dòng lệnh từ **Google Sheets lúc chạy** rồi **không lưu lại**)*. Hai đường ra, cần owner chọn: **(a)** lúc nạp thì **lưu lại các dòng lệnh chưa ghép** vào một bảng `fls_*` để cửa `/match` tra ⇒ thêm 1 bảng + 1 migration, và phải trả lời *"bản lưu đó già đi thì sao"* · **(b)** đọc Google Sheets **sống** ngay trong một đường HTTP ⇒ ⛔ **không nên**: nguồn đã đo được là **chập chờn** *(timeout 3/3 lần ở tab `IMPORTRANGE`)*, và một cửa ghi treo vì mạng là một cửa kế toán sẽ bỏ. ⇒ ⛔ Đừng đọc *"P5 xong"* thành *"ghép tay xong"* |
| `GAP-JOIN-04` ⭐⭐ | ⛔⛔ **Xếp ứng viên ghép lệnh ⛔ KHÔNG có trục `ngày` và `payee`** — §2 của chính tài liệu này mong *"xếp theo reference / tiền / ngày / payee"*, nhưng ảnh chụp `fls_pm_line` **cố ý ⛔ không mang PII** *(Tên tài khoản · Số tài khoản · Ghi chú · Diễn giải)* và ⛔ **không đọc cột ngày**. ⇒ chỉ còn **hai** trục thật. Muốn có hai trục kia thì phải **mở phạm vi đọc nguồn** — quyết định của chủ sổ, ⛔ không phải của code. ⚠ Hệ quả đo được trên sổ thật: trong **25 dòng** hàng chờ thử, chỉ **1 dòng** có ứng viên bậc `ma` ⇒ phần lớn việc ghép tay sẽ dựa vào **tiền**, và thiếu `ngày`/`payee` là thiếu thật |
| `GAP-JOIN-05` ⭐ | ⛔ **Chưa có đường BỎ mối nối.** Ghép xong rồi phát hiện sai thì hiện **⛔ không sửa được**: `POST /match` lần hai trả `409`. Đường bỏ phải là **thêm một bút toán đảo** *(cùng luật `SM-I03`)*, ⛔ không phải `DELETE` — nhưng `fls_pm_link` chưa có cột nào mang khái niệm *"đã bỏ"*. ⇒ cần một quyết định thiết kế trước khi làm màn `F01` |
| `GAP-CR1-04` ✅ **ĐÓNG 28/08 — `QĐ-ITL-63`: cửa ghép TAY đòi CẢ HAI, lấy cái NHỎ hơn — lệch ≤ 1.000 đồng VÀ ≤ 0,5% tiền bank** *(hai điều kiện bằng nhau tại 200.000 đồng; cửa TỰ ĐỘNG giữ `QĐ-ITL-57`; ngoại tệ vẫn 0 vì `min(0, tỷ lệ) = 0`)*. `409`/`422` của `/match` nay trả **cả ba số** *(Σ · tiền bank · dung sai đã dùng, kèm tỷ lệ)*. Nội dung cũ: | ⛔⛔ ~~**Dung sai `1.000 VND` TUYỆT ĐỐI quá rộng cho cửa ghép TAY.**~~ Con số `QĐ-ITL-57` được đo và duyệt trên phép ghép **TỰ ĐỘNG**, nơi khoảng lệch **lớn nhất thật** chỉ là **2,00 đồng** *(làm tròn thuần)*. Trên cửa ghép **tay** thì người gõ chọn dòng lệnh nào cũng được, nên cùng con số ấy **cho ghép một dòng bank `100 VND` với một dòng lệnh `1.099 VND` — lệch 999% của chính nó**. Đó đúng là hình nguy mà ghi chú bộ nạp đã cảnh cho USD *(lệch 660,04 USD trên giao dịch 59,96 USD = 1.100%)*. ⚠ Nó đã làm **hai** bài test của tôi **xanh SAI** trong một buổi. ⇒ **Câu hỏi cho kế toán trưởng:** dung sai trên cửa ghép tay có nên là một con số **tuyệt đối**, hay phải kèm một **tỷ lệ**? ⛔ Tôi không tự đặt ngưỡng tỷ lệ — đó là quyết định kế toán |
| ⭐⭐ `GAP-API-10` **MỚI 23/09** | ⛔⛔ **⛔ Không cổng nào hỏi *"cửa có TRẢ đúng khuôn hợp đồng ⛔ không"*.** `/itl-candidates` trả hàng thô suốt `2` ngày mà `40/40` tuyến vẫn xanh: `soi_bang_tuyen` so **bảng đã khai ↔ SQL thật**, `test_ba07_phu_het_tuyen` so **tuyến đã khai ↔ tuyến có thật** — ⛔ **không** cổng nào so **khuôn đã khai ↔ khoá thật trả về**. ⭐ Hai bài mới chỉ phủ **một** tuyến; việc mở là **sinh phép so ấy cho mọi tuyến có khuôn khai trong `BA-07`** |
| ⭐ `GAP-API-11` **MỚI 02/10** *(`BG-034` yếu #3, `TL-033 ⓒ`)* | ⛔ **Một dòng tiền ⛔ có chiều làm sập cả trang Toàn sổ.** `man_ghep.chieu_tien` **ném** khi `ps_no`/`ps_co` đều `0`/rỗng — đúng ở tầng đọc *(`INV-I16`: máy ⛔ đoán chiều)*, nhưng nó chạy trong khuôn `⓵` của **một danh sách** ⇒ cửa `/so` ⛔ lọc `q` trả `500` cho **cả trang**. Đo 02/10: sổ thật **0 / 8.387** dòng `fls_itl` hai ô đều `0`/rỗng *(và **0** dòng hai ô đều ≠ 0)*; kho TEST **11**. Hướng đã khai: **cùng luật `tach_nguon` 23/09** *(`⓵`, đoạn ⛔⛔⛔ dưới bảng — một dòng hỏng ⛔ được sập trang; trả một trạng thái **có tên**, giữ `dien_giai`/`amount`)*; tên khoá + chữ màn quyết khi phát `WO`. Ưu tiên **THẤP** — nâng lên **TRƯỚC** lần nạp sao kê có dòng tiền `0` đầu tiên |
| `GAP-API-03` ⭐ | **Cổng *"bốn đường"* ⛔ KHÔNG đo được từ kho.** Bốn đường là `vào = sổ + loại + rỗng + trùng`, mà **`rỗng` và `trùng` ⛔ không được lưu ở bảng nào** — chúng chỉ in ra lúc chạy `nap_that.py` rồi mất. ⇒ Muốn có cổng này thì phải **ghi bốn con số vào `fls_run`**. *(Phát hiện 27/08 khi cổng cũ **đỏ GIẢ**: nó so `row_count` với `count()+count()`, trong khi `row_count` **được đếm từ chính bảng đó** ⇒ phép so **vòng tròn**. Cổng chung **#11**.)* |

---

## Changelog
- **v3.14** *(2026-10-06, `fls-ba`, xếp `KQ-061 F-2`; trong thẩm quyền spec: hợp đồng cửa đọc thêm trường áp **một luật đã có** — `BA-05` v0.32 *"Final = `fls_sua_tay` ∪ cột nguồn"*, ⛔ đổi luật, ⛔ đổi sổ, ⛔ đổi trường cũ)*: `GET /ledger` thêm `<f>_final` + `<f>_nguon` cho năm trường lưới gõ được; tuyến đọc thêm `fls_sua_tay`. Gốc: lưới `F02` in cột thô ⇒ ô người vừa gõ hiện `chưa gán` sau khi tải lại và phép hỏi lại gọi chính người gõ là *"người khác"* *(sổ thật cột nguồn rỗng **8.387 / 8.387** ⇒ gặp **100%** ở phiên sửa thật đầu tiên)*. Mã ⇒ **`WO-062`**.
- **v3.13** *(2026-10-05, `fls-ba`, xếp phát hiện ngoài phạm vi `WO-023` — `BG-053` mục 3 · `BG-057` mục 2; trong thẩm quyền spec: **mô tả** một mã lỗi đã có + ghi nợ — ⛔ đổi mã, ⛔ đổi HTTP, ⛔ tuyến mới, ⛔ đổi sổ)*: ⭐ **`§5` đính chính dòng `FLS-DQ-FAILED`** — mã ấy ⛔ bao giờ là *"`ACC-1…4` không đạt"*: **0** đường ném nó từ cổng, **5** lớp lỗi của cửa ghi mang nó *(khác tiền tệ · lệch tổng · chưa duyệt · thiếu lý do · lớp gốc)*. Câu màn + `bao.py` theo ⇒ **`WO-060`** ⓐ *(`BA-06` v4.23 `ⓦ` ⑧)*. ⭐ **`GAP-API-12`** mới *(nợ)*: `la_ban_dao` nối theo `at` trùng mà ⛔ ràng buộc máy canh.
- **v3.12** *(2026-10-05, `fls-ba`, nghiệm thu PO `WO-042` + xếp `KQ-046 F-1`; trong thẩm quyền spec: danh sách chỗ áp một luật đã có — ⛔ đổi luật, ⛔ đổi sổ, ⛔ tuyến mới, ⛔ khoá mới)*: ⭐ **`§4g` đoạn v3.12 — kiểm kê ĐỦ** mọi phép so / gom tiền tệ *(grep `upper(`/`lower(`/`btrim(`/`.strip()`/`==` trên `curr`)*: lớp ⓐ so giữa hai nguồn — `doc_bao_cao.py:309`/`:310`/`:317` *(chiều ngược `ung_vien_pm`, `upper(l.curr)` trần — `KQ-046` lệch **5/5** ca biên, kể cả `' vnd '`)* ＋ `man_ghep.py:631` *(`khoa_bang_chung`, so chuỗi thô — `fls-ba` tìm thêm)* · lớp ⓑ gom để đếm — `do_mau_so.py:297` ⇒ **áp**; lớp ⓒ xếp/lọc hàng chờ *(`QĐ-ITL-58`, khứ hồi tự nhất quán)* · ⓓ cùng nguồn · ⓔ `tools/demo_dong.py` ⇒ **ngoài, có lý do**. Sổ thật **0** ca. Mã ⇒ **`WO-047`**.
- **v3.11** *(2026-10-05, `fls-ba`, nghiệm thu PO `WO-037` + xếp `KQ-041 F-2`; trong thẩm quyền spec: tập ký tự của phép chuẩn hoá mã tiền tệ — ⛔ đổi sổ, ⛔ tuyến mới, ⛔ khoá mới)*: ⭐⭐ **`§4g` đoạn v3.11 — MỘT tập ký tự trắng `TAP_TRANG_TIEN_TE`** *(30 = Python `isspace` 29 ＋ `U+FEFF`)* cho **mọi** phép so tiền tệ: Python *(`ma_tien_te` ＋ **6** bản viết tay, kể cả cửa ghi)* · SQL *(`btrim` tham số từ hằng — trước **4** ký tự)* · JS *(trước `trim()` **25** ký tự)*. Sổ thật **0** ca *(`fls_itl` 0 / 8.387 · `fls_pm_line` 0 khoảng trắng / 276.028)*. Mã ⇒ **`WO-042`**. Đi cùng `BA-06` **v4.18** · `BA-13` **v1.9**.
- **v3.10** *(2026-10-02, `fls-ba`, `TL-038` — `HOI-038` + bốn mục yếu `BG-039`; trong thẩm quyền spec: **khai** khoá cửa đọc đã chạy, **chữ in** câu cửa, một luật so tiền tệ đã có — ⛔ đổi sổ, ⛔ đổi cửa ghi, ⛔ tuyến mới)*: ⭐ **`§4h ⓵'` khai `the.vi_sao`** *(phương án **B** của `HOI-038`: chỉ có mặt khi `gd = null` ∧ `la_khop_ma_chi_khac_tien_te` — **84** thẻ sổ thật; ⛔ A — 616 ô; ⛔ C — luật thứ hai ở JS)*. ⭐ **`lenh-cho/ro` ＋ `nguoi_khac_tien_te`** — băng `F01L` nói *"Chưa có số chứng từ"* cho cả rổ `nguoi`, sai **84 / 616** *(`BG-039` yếu #1)*. ⭐ **Câu `VI_SAO` ⛔ ký hiệu cấm** *(3 / 3 câu mang `⛔` — `BG-039` yếu #4)*: chữ in mới ba câu, khoá + tập ⛔ đổi. ⭐ **SQL `itl-candidates` vế sổ `btrim`** *(`BG-039` yếu #3; sổ thật **0 / 8.387** ca)*. Mã ⇒ **`WO-037` vòng 2**. Đi cùng `BA-06` **v4.17** · `BA-13` **v1.8**.
- **v3.9** *(2026-10-02, `fls-ba`, nghiệm thu PO `WO-032` + xếp `KQ-036` `F-1`/`F-2`/`F-3`/`F-5 ⓐ`/`F-6`; trong thẩm quyền spec: **nghĩa** và **thứ tự** của trường cửa đọc đã trả + phép chia rổ theo luật **cửa ghi** đã có — ⛔ đổi sổ, ⛔ đổi Final, ⛔ đổi cửa ghi, ⛔ tuyến mới)*: ⭐⭐⭐ **`§4g ⓹` — rổ `may` đo theo cửa GHI**: lệnh vào `may` chỉ khi có dòng tiền khớp mã **cùng** tiền tệ; sổ thật **84 / 268** lệnh rổ `may` chỉ khớp mã ở tiền tệ khác *(đề xuất đầu là cặp cửa ghi từ chối)* ⇒ sang `nguoi` + `vi_sao` `ma_khop_khac_tien_te`; chip `Chưa gán` ⛔ đổi. ⛔ Chọn *"đưa ứng viên cùng tiền tệ lên đầu"*: **45** lệnh có ứng viên cùng tiền tệ lệch 0 nhưng là **trùng tiền tình cờ** *(trung vị 16 dòng cùng số, cách 294 ngày)* ⇒ đổi cú bấm bị từ chối lấy cú ghép sai được nhận. Thứ tự trong bậc `ma`: cùng tệ trước. **`§4h ⓵`** dòng `bac`: `khac_tien_te` cũng ở `gd`/`gd_ds` *(`F-2`)* · một hàm so tiền tệ *(`F-1`)* · bậc lạ in nguyên tên ở **mọi** hàm vẽ *(`F-3`)*. **`§4h ⓵'`**: `gd` chưa gán ⛔ khác tiền tệ *(84 → 0)*. Dòng `lenh-cho`: khai `ma_canon` *(`F-5 ⓐ`)*. Câu owner mới `Q-FX-1` *(lệnh trả bằng tiền tệ khác)* ⛔ chặn. Mã ⇒ **`WO-037`**. Đi cùng `BA-06` **v4.16** · `BA-08` **v1.3**.
- **v3.8** *(2026-10-02, `fls-ba`, `TL-033` — `HOI-033` của `fls-dev`; trong thẩm quyền spec: **nghĩa** trường `bac` cửa đã trả, ⛔ đổi luật xếp bậc, ⛔ đổi HTTP)*: ⭐⭐ **`§4h ⓵'` — `bac` của `gd`/`gd_ds` tính theo mã của CHÍNH dòng lệnh ở CẢ HAI cửa danh sách**: cửa `lenh-da-gan` ⛔ chạy `xep_ro` ⇒ ⛔ bao giờ trả `ma` — sổ thật **0 / 2.262** mối nối khớp mã, khối *"Đang gán"* chip `①` **0 / 2.219** lệnh *(`②` 2.121 · `④` 98)*. Chọn **sửa mã** *(⛔ đính chính `AC-2`)*: `⓵'` v3.7 đã đòi *"đúng khuôn `⓵`"*; một `bac` thiếu vế mã là trường **có mà sai**. ⭐ **`§7` `GAP-API-11`** — `chieu_tien` ném trong khuôn danh sách ⇒ `/so` `500` cả trang khi một dòng tiền `0` *(sổ thật **0 / 8.387**)*. Mã ⇒ **`WO-032` vòng 2**. Đi cùng `BA-06` **v4.15** · `BA-13` **v1.7**.
- **v3.7** *(2026-10-02, `fls-ba`, `KQ-031` `F-2` + `F-3` — `fls-test` hỏi *"chữ `BA-07 ⓵` hay mã — chọn một"*; trong thẩm quyền spec: **nghĩa** một trường cửa đọc đã trả, ⛔ đổi sổ, ⛔ đổi HTTP, ⛔ đổi cửa ghi)*: ⭐⭐ **`§4h ⓵` `lech` — chọn GIỮ trị tuyệt đối của mã, SỬA luật `null`**: số ở **mọi** bậc và **mọi** cửa trả khuôn `⓵` *(`itl-candidates` · `/so` · `the.gd` · `the.gd_ds`)*, khớp ⇒ `0`; **`null` ⇔ ⛔ so được** *(khác tiền tệ / thiếu số)*. Vì sao ⛔ chọn *"sửa chữ cho khớp mã"*: mã cho `null` ở **338 / 448** ứng viên bậc `ma` có lệch thật *(`KQ-031`, 8088)* ⇒ hộp *Tìm tiền* in `—` cho lệch `21.586,78`, nhãn xác nhận `F01G` mất *"(lệch …)"* — đúng chỗ độ lệch **đổi một quyết định**; khai theo mã là ghi luật cho một lỗ. ⭐⭐ **Khai `khoa_to`** *(luôn có, `text[]`)* + **`dien_giai_vi_sao`** vào bảng `⓵` *(13 trường)*; `⓵'` — `gd`/`gd_ds` mang **đủ** khuôn `⓵` *(hôm nay `khoa_to` **0 / 768**)*. ⭐ **`⓹` bậc `khac_tien_te`** cho dòng toàn sổ khác tiền tệ lệnh *(hôm nay dán `cung_tien_te` — **3.926 / 6.165** dòng chưa nối với một lệnh VND)*; màn gặp bậc lạ ⛔ rơi về `cung_tien_te`. ⭐ Luật bài thử: thân vẽ màn lấy **từ cửa thật** trên kho TEST. Mã ⇒ **`WO-032`**. Đi cùng `BA-06` **v4.14**.
- **v3.6** *(2026-10-02 khuya, `fls-ba`, `KQ-025` `F-3` + `F-4` — trong thẩm quyền spec; hai trường **THÊM**, ⛔ đổi/bỏ trường cũ, ⛔ đổi HTTP)*: ⓐ `GET /journal` mỗi dòng thêm `la_ban_dao` *(nối `fls_adjustment` theo `(itl_id, field, at, actor)`, `reversal_of IS NOT NULL`)* — màn phân biệt bản đảo với cú xoá ô; ⓑ `GET /ledger/{itl_id}` `but_toan[]` thêm `nguon` — hộp `Đảo` nói đúng hậu quả cho gợi ý máy. Đo sổ thật: cặp **4.428**, nhập nhằng **0**, bản đảo **2**. Mã ⇒ `WO-023` (f)(g).
- **v3.5** *(2026-10-02 khuya, `fls-ba` — trả nợ `409` ghi ở `BA-06` v4.10; `KQ-021` đo lại trên `8099`)*: ⭐ §5 thêm **ba** mã `409` — `FLS-DA-GHEP` · `FLS-KHONG-CON-MOI-NOI` · `FLS-CHUA-XONG`. Vì sao: `FLS-CONFLICT-SOURCE` bị **bốn** lớp lỗi dùng chung *(`fls/repo/ghi_tay.py` `KhacNguon` `:130` · `DaGhep` `:171` · `ChuaXong` `:178` · `KhongCoMoiNoi` `:200`)* ⇒ màn dịch cả bốn thành *"Giá trị bạn gõ khác với giá trị nguồn đang có."* — sai nghĩa cho ba. HTTP **⛔ đổi** *(vẫn `409`)*; thân lỗi ⛔ đổi khuôn. Câu tiếng Việt cho từng mã ở `BA-06` v4.11 `ⓕ4`. Mã phía **màn** *(`FLS-MAT-KET-NOI`, `FLS-HET-GIO` mới)* ⛔ thuộc bảng này — chúng ⛔ bao giờ ra từ máy chủ. Sửa kèm: bảng §5 bị **hai dòng trống** chẻ làm ba bảng *(vỡ bảng)* — nối lại, ⛔ đổi chữ nào. Mã ⇒ `WO-023`.
- **v3.4** *(2026-10-01, `fls-ba`, `QĐ-ITL-149` — owner trả `WO-001 Q3` *"Máy gợi ý"* + `KQ-002 F-1` *"bỏ yêu cầu lý do cho cú Ghép"*)*: ⭐⭐⭐ **Thêm `§4h ⓼` — `reason` TUỲ Ý cho `match` + `unmatch`, thiếu thì máy điền lý do mặc định có nhãn `(may dien)`** *(⛔ để rỗng — lỗ 27/08)*; điền ở **tầng repo**; `match-lo` **giữ** bắt buộc. ⭐⭐ **`§3` dòng `match`: `hd`/`cdt1` suy lúc ghép là GỢI Ý CỦA MÁY** (`nguon='may_goi_y'`, ⛔ `fls_sua_tay`, Final ⛔ đổi) — trước đây ghi `sua_tay` nhân danh người bấm *(`ghi_tay.py:686`–`697`)*; thêm `run_pm` vào danh sách ghi *(`KQ-002 F-4`)*. ⛔ **Sửa `F-6`:** *"ảnh chụp của chính lần nạp đó"* ⇒ **ảnh PM đang hiệu lực** *(`QĐ-ITL-119`)*. ⛔ Đính chính dưới `§4h ⓻ ⓑ`: spec đã khai `unmatch` tuỳ ý từ v3.0 mà mã chưa theo ⇒ lỗi mã *(`WO-003`)*.
- **v3.3** *(2026-09-23, owner xem màn thật — `4` vòng góp ý)*: ⭐⭐⭐ **Một VI PHẠM HỢP ĐỒNG sống `2` ngày và `40/40` tuyến vẫn xanh.** `/queue/lenh/{pm_line_id}/itl-candidates` — **đường chính, ứng viên do MÁY đề xuất** — trả **HÀNG THÔ** từ SQL *(`tien` · `ps_no` · `ps_co` · `source_sheet`)* thay vì khuôn `⓵`; màn đọc `amount` · `chieu` · `nguon` ⇒ **hai cột rỗng**, và phép so *khớp đúng tiền* so `Number(undefined)` ⇒ **MỌI ứng viên đều thành *"lệch"*** ⇒ nút `Gán` luôn đi đường cảnh báo — **một phép khớp ĐÚNG trình bày như một phép khớp SAI**, tệ hơn ⛔ không hiện gì vì nó dạy người ta rằng cảnh báo là chuyện thường. ⛔⛔ **Nó sống sót vì bài thử cũ chỉ hỏi `bac` và `itl_id` — đúng HAI khoá mà hàng thô TÌNH CỜ cũng có**; một bài thử hỏi vài khoá **giao nhau** thì ⛔ không bao giờ thấy **hai khuôn là HAI**. ⭐ Cửa `/so` **đã** nắn khuôn từ đầu ⇒ **hai cửa nuôi MỘT hàm vẽ mà nói HAI thứ tiếng**; ảnh chụp của owner ⛔ không lộ ra vì màn lúc ấy ở chế độ **Toàn sổ** — cửa KIA. ⇒ `GAP-API-10`: ⛔ **không cổng nào** hỏi *"cửa có trả đúng khuôn đã khai ⛔ không"*. ⭐⭐ Thêm trường thứ **`11`** **`loi_nguon`** — **chỉ có mặt khi `nguon` là `null`**, ⛔ không phải một khoá luôn có *(một khoá luôn có đẩy tầng trên vào thói quen **kiểm giá trị thay vì kiểm sự tồn tại**)*: `tach_nguon` ⛔ **không còn được ném từ trong khuôn**, vì khuôn chạy trên **từng dòng của một DANH SÁCH** và một ngoại lệ ở đó trả `500` cho **cả trang** ⇒ mất `50` ứng viên vì **một**; `nguon:null` ＋ `loi_nguon` **giữ lại** `dien_giai`/`amount`. ⭐⭐ Thêm **`§4h ⓵'`** — `the.gd` *(cả hai cửa danh sách)* ＋ **`the.gd_ds`** *(chỉ `lenh-da-gan`, **MỌI** dòng tiền đã gán)*: hai cửa chỉ trả **ID**, mà bảng sổ cần `diễn giải`/`số tiền` và khối `C4` cần **cả chùm** ⇒ **MỘT** truy vấn cho cả trang, ⛔ không `738` lượt. Đo `2.219` lệnh đã gán: **`23` (`1,0%`)** gán hơn một dòng tiền, nhiều nhất **`7`** — một `1,0%` là cớ để ⛔ không bật hộp thoại *(`QĐ-ITL-148 ⓔ`)*, ⛔ **không** phải cớ để **giấu sáu dòng tiền**; giá là tập `id` ~`500`→~`505` mỗi trang. ⛔ `gd_ds` **chỉ** cho dòng đã gán — với dòng chưa gán, `ung_vien_itl` là **đề xuất của máy**, trộn vào là trộn *"đã chốt"* với *"máy đoán"*.
- **v3.2** *(2026-09-22, chặng `4` của plan vá bốn lỗi CHẶN)*: ⭐⭐⭐ **Tuyến `40` `GET /queue/lenh-da-gan` — `GAP-API-08` ĐÓNG một nửa.** ⛔⛔ Trước nó, `/queue/lenh-cho` lọc cứng `NOT EXISTS (fls_moi_noi)` nên ⛔ **không** đường nào hỏi *"lệnh chi nào ĐÃ có tiền"*, và **cả nửa *"đã gán"* của màn ghép chết theo dây chuyền**: `trang_thai` vĩnh viễn `chua_gan`, nút `Bỏ gán` ⛔ không bao giờ bật — mà nếu bật thì nó gọi `/queue/undefined/chum`, vì `itl_id_da_gan` là một khoá **⛔ KHÔNG AI SINH RA** trong cả kho. ⭐⭐⭐ **Và khoá ấy phải là một DANH SÁCH:** đo `22/09` trên kho thật, **`23/2.219` = `1,0%`** lệnh chi gắn **nhiều hơn một** dòng tiền ⇒ một số ít **im lặng bỏ mất** mối nối thứ hai, đúng ở chỗ người ta bấm `Bỏ gán`; ⭐ `1,0%` gần đúng `1,1%` ca có chùm — **cùng một sự thật** *(tiền ↔ lệnh là nhiều ↔ nhiều)* nhìn từ hai phía. ⭐ Một tuyến **riêng** chứ ⛔ không một cờ trên `lenh-cho`: tên `lenh-cho` nghĩa là *"đang chờ"*, cho nó trả dòng đã nối là để một cái tên **nói dối**. ⛔⛔ **Câu con `fls_moi_noi` phải lọc phạm vi qua phía ITL** — `pm_line_id` là khoá **nghiệp vụ** *(lặp ở mọi lần nạp)* còn `itl_id` là khoá của **một dòng trong một ảnh chụp**; thiếu phép lọc thì mối nối của mọi lần nạp khác lọt vào *(bài thử bắt: `[2, 3, 23, 24]` thay vì `[23, 24]`)*, và phải lọc `i.run_id` chứ ⛔ không `run_pm` vì ảnh ngân hàng và ảnh PM là **hai lần nạp khác nhau**. ⚠ Chip `Tất cả` **vẫn chưa có cửa** *(`GAP-SCR-26`)*: nó là **hợp** của hai rổ, và gộp ở màn thì `x/y` thành một **số của máy** (`UI-F8`).
- **v3.1** *(2026-09-22, chặng `B3` — mở BE ＋ FE thật)*: ⭐⭐⭐ **Khai khoá `the` trên `/queue/lenh-cho` — khuôn `11` trường của thẻ lệnh chi.** ⛔⛔ **Chỗ tệ nhất được lấp: `6/11` trường của thẻ ⛔ KHÔNG cửa nào gọi tên** — chúng chỉ sống trong túi `tho`, khoá theo **tên cột của Google Sheets**, thứ **đã đổi một lần rồi**; để màn hình tự móc là để chỗ hỏng lần sau thành **một ô trống trong im lặng** mà ⛔ không bài thử nào bắt được *(bài thử sẽ gõ y hệt tên ấy)*. ⭐ **THÊM chứ ⛔ không THAY**, và ⛔ **không** một cửa riêng: hai cửa trả cùng một danh sách với hai hình dạng là hai bản sự thật. ⛔⛔ **`GAP-API-08` mở**: `/queue/lenh-cho` lọc cứng `NOT EXISTS (fls_moi_noi)` ⇒ ⛔ **không** đường nào hỏi *"lệnh chi nào ĐÃ có tiền"*, nên **`2/4`** chip của màn ghép *(`Đã gán` · `Tất cả`)* ⛔ không gọi được — màn **NÓI RA** điều đó thay vì vẽ một danh sách rỗng, vì một danh sách rỗng đọc **y hệt** *"đã xong hết"* (`INV-I16`). ⭐ Hai chip còn lại đo **bằng cách gọi cửa thật**: `?ro=nguoi` ＋ `?ro=may&tu_chung=0` = **`738`** *(đúng `G-a` của `CR#12`)* · `?ro=khong` = **`768`** *(`INV-I20`)*. ⚠ Cửa chặn `limit` ở **`500`** mà rổ `khong` có **`768`** ⇒ màn **phải lật trang**; lấy trang đầu rồi thôi là mất **`268`** dòng và `lenh_ke_tiep` sẽ **im lặng dừng** giữa chừng. ⛔⛔ **Và số sê-ri VẪN CÒN**: `BA-06 §4.5 ⓕ` khai *"đã hết timestamp sê-ri"*, đo lại trên **cửa thật** thì `Timestamp` ra `46091.42265217593` ở **`3.772/3.772`** dòng ⇒ đổi ở tầng đọc, dùng lại `ngay_tu_seri` **đã đo**, ⛔ không viết bản thứ hai bằng JS.
- **v3.0** *(2026-09-21, `QĐ-ITL-148` — chặng `B0` của plan màn ghép)*: ⭐⭐⭐ **Thêm `§4h` — lấp `4` GAP hạng chặn của audit `21/09`, và `35 → 37` tuyến.** ⛔⛔ **Chỗ tệ nhất được lấp: `ung_vien[]` khai `0` trường suốt từ `09/09`** — hợp đồng ghi *"trả `ung_vien[]`"* rồi **dừng**, nên người dựng ⛔ không có gì để nhận ngoài một chuỗi và đã **cắt chuỗi hiển thị** để lấy lại cấu trúc. Nay khai đủ **`10`** trường, trong đó ⭐ **`nguon` là OBJECT** `{tk, bank, curr, le}`, ⛔ không phải chuỗi. ⭐⭐⭐ **Và luật tách `nguon` khai ra một chỗ MỌI TÀI LIỆU ĐANG TRÍCH SAI:** giá trị thật mang **tiền tố `R \|`** — đo **`8.387/8.387`** — trong khi `BA-06`, hợp đồng thiết kế và brief đều trích **thiếu** ⇒ một phép tách chép theo tài liệu **hỏng ngay ký tự đầu**. Bóc tiền tố rồi tách **4 mảnh** được **`8.387/8.387` trên `49` nguồn**; ⚠ **`6` tài khoản ⛔ không phải số** *(`PO1`…`PO9`, tài khoản thẻ)* ⇒ luật *4 số cuối* phải có **nhánh riêng**. ⭐⭐ **Chiều `Nợ/Có` — luật CHƯA TỪNG được viết** dù dự án **đã đọc nhầm cột này một lần**: `3.691/8.387` dòng mang **cả hai** ô, nhưng **`0`** dòng cả hai khác `0` ⇒ *"bên nào ≠ 0 thì đó là chiều"*, và ⛔ **⛔ KHÔNG** lấy dấu từ `pay_type`. ⭐⭐⭐ **Gốc sê-ri Excel được ĐO, ⛔ không chọn:** gốc `1900` cho `2025-03-10 … 2026-08-29` và lệch **trung vị `3` ngày** so với ngày **dòng tiền đã nối**; gốc `1904` cho `2029…2030`, lệch **`1.462`** ngày ⇒ **`1900`**. ⭐ Phép kiểm dùng một **nguồn độc lập** *(ngày dòng tiền)*, ⛔ không phải một dải ngày *"trông hợp lý"* — dải ngày một mình ⛔ không đủ, vì gốc sai với độ lệch nhỏ hơn thì mắt ⛔ không bắt được. ⭐ Tuyến **36** `GET /queue/lenh/{pm_line_id}/so` *(tra cứu toàn sổ, **tính lại bậc** theo lệnh đang mở — bậc `ma` bằng `canon_ref` ở Python, `regexp` lệch **`17,9%`**)*; tuyến **37** `GET /queue/{itl_id}/chum` — vì `unmatch` bỏ **cả chùm** và ở **`25/2.222` = 1,1%** ca nó gỡ tới **`10`** dòng lệnh, nên màn **phải hỏi trước kèm tên từng dòng**. ⚠ `reason` của `unmatch` thành **tuỳ chọn** — `QĐ-ITL-137` đã hoãn cột lý do, để bắt buộc là đòi một thứ màn ⛔ không có. ⭐ `dien_giai` **`null` mang HAI nghĩa** *(`3` rỗng · `26` ⛔ chưa nối được)* ⇒ thêm `dien_giai_vi_sao`, vì gộp chúng là đúng thứ `INV-I16` cấm.
- **v2.9** *(2026-09-18, `CR#12`)*: ⭐⭐ **Khai hai cửa ĐÃ CHẠY nhưng ⛔ chưa có trong hợp đồng — `queue/lenh-cho/ro` và `queue/lenh-cho/summary`.** Cả hai phục vụ lằn **LỆNH CHI**, tức lằn **mặc định** của `F01` từ `09/09`, và suốt `9` ngày hợp đồng cửa ⛔ **không** nhắc tới chúng. ⭐ Cửa `summary` mang một luật đáng ghi: nó đếm **toàn bộ**, ⛔ **không** đếm trên trang đang xem — đúng lớp lỗi `do_phu` từng dính *(đếm số dòng trả về của một cửa có trần `500` ⇒ con số **im lặng dừng ở 500**)*, và ở đây còn tệ hơn vì thứ tự `(tiền tệ, hạng)` làm một trang ⛔ **không** phải mẫu ngẫu nhiên. ⭐⭐ Mở cửa mới `queue/loi-nguon` — **rổ SỬA NGUỒN**: `166` dòng có ô số chứng từ giữ chữ `Reject`, `1` dòng có đơn vị tiền tệ tên `20`. ⛔⛔ Cửa này ⛔ **không** sửa gì *(`INV-I16`)*, nó tồn tại để **GỬI được danh sách cho người sửa bảng tính** — vì đo được rằng *chỉ mặt* mà ⛔ không có người nhận việc thì bằng ⛔ không: `BA-12 §2ⓓ` chỉ mặt con tiền tệ ma ngày `11/09`, và `18/09` nó **vẫn đứng dòng `#1`** của màn.
- **v2.8** *(2026-09-09, `QĐ-ITL-122` · `GAP-SCR-14`)*: ⭐⭐⭐ **Thêm `§4 ⓹` — BA TUYẾN PHÍA LỆNH CHI, `32 → 35`.** Owner chốt chiều đo: *"`Trans` map vào `PM` (số lượng Trans vốn nhiều hơn PM; ⛔ ko cần question các Trans không được map)"*. ⛔⛔⛔ **Đo trên bảng tuyến cùng ngày: `10` tuyến khoá `itl_id`, ⛔ `0` tuyến khoá dòng lệnh** ⇒ cả hệ ⛔ **không có đường nào** hỏi *"lệnh chi nào ⛔ chưa tìm được tiền"* — tức **đúng câu hỏi của việc**; và màn `F01` đang hiển thị **7.682** dòng `Trans`, tức hỏi **đúng cái câu owner vừa nói là ⛔ không cần hỏi**. ⇒ Hai con số của **cùng một kho**: hỏi phía TIỀN cho **5.684** dòng */* **799** dòng để phủ 90% tiền; hỏi phía LỆNH cho **1.345** dòng */* **698** phiếu */* ⭐ **69** dòng để phủ 90% — chênh **11,6 lần**. ⛔⛔ **CẢ BA TUYẾN ĐỀU LÀ `GET`**, và đó là điều quan trọng nhất: cú ghép vẫn đi qua `POST …/{itl_id}/match` — một chuyến. Hai đường ghi sẽ **lệch nhau** ở bốn cổng của `ghep_lenh`, và cửa dễ hơn là một **đường tắt vòng qua kiểm tra** ⛔ không ai thấy *(bài `test_KHONG_them_mot_duong_GHI_nao`)*. ⭐ Bốn bậc **soi gương** chiều thuận, **tên giữ y nguyên**. ⛔⛔ Bậc `ma` tính ở **PYTHON bằng `canon_ref`**, ⛔ không bằng `regexp` trong SQL — kho **chỉ có `doc_no` THÔ**, ⛔ không cột chuẩn hoá nào; một câu tự dựng là **bản thứ hai** và ⛔ không tương đương *(ký hiệu khoa học · `NFKC` · ô lỗi)*. ⭐ Đã cắn thật: con số *"`560` ghép được ngay"* đo bằng câu `regexp` ấy, luật thật cho **`475`** — lệch **`17,9%`**. ⛔ Bậc `cung_tien_te` chiều ngược **BỊ CẮT** *(tập ứng viên `10.030` thay vì `3.772`)* và cửa **KHAI RA** mình đã cắt *(`bi_cat` + `tong_cung_tien_te`)* — cắt mà im là mặc định im lặng *(`INV-I16`)*. ⛔ `?duyet=` **mặc định KHÔNG LỌC**: ẩn `275` dòng ⛔ chưa duyệt theo mặc định sẽ làm kế toán kết luận **hệ mất dữ liệu**; giá trị lạ ⇒ **`400`**. ⭐⭐ `so_dong_phu` có thể là **`null`** = ⛔ **không đo được** *(Σ tiền = `0`)*, và màn **PHẢI** vẽ khác `0` — vẽ `0` nói *"xem 0 dòng là đủ"*.
- **v2.7** *(2026-09-09, `QĐ-ITL-118`)*: ⭐⭐⭐ **Thêm `§4g` — MẪU SỐ + GHÉP CẢ LÔ, ba tuyến **29 → 32**.** Và nó mở đầu bằng việc **lật một con số tôi viết ra một ngày trước đó**: lộ trình `13` §0 ⓵ ghi *"**584** dòng TỰ CHỨNG (8,0%)"* — con số thật là **68 (0,9%)**, nhỏ hơn **8,6 lần**. ⓐ Vì sao: `584` đo bằng luật của **danh sách ứng viên** *(`ung_vien_pm` — một cửa ĐỌC để người CHỌN)*, ⛔ không bằng luật của **cửa GHI** *(`ghep_lenh` còn bốn cổng)*. Đo lại trên đúng tập `652` dòng có mã: **301** lệch tiền ngoài dung sai · **202** khác tiền tệ · **51** chùm Σ vẫn lệch · **30** chưa duyệt · **0** đã bị ghép. Và `301` ⛔ không phải dung sai quá chặt — chỉ **16/491** nằm trong khoảng phí bank, còn lại lệch **hàng chục lần** ⇒ cửa ghi **từ chối đúng**. ⇒ Bài học **lần thứ hai trong hai ngày**: *"đo QUAN HỆ thì gọi hàm thật"* ⛔ **không đủ** — phải gọi **đúng hàm của CÂU HỎI**. ⓑ **MẪU SỐ**: `10.030` sai, con số đúng là **8.246** *(vế `PS Có` — **31,1%** so với `PS Nợ` **7,8%** ⇒ đó là vế của lệnh chi)*, đích còn lại **5.684** *(⛔ không 7.329)*. ⓒ *"Lệch 353"* ⛔ **KHÔNG phải mâu thuẫn**: nó là **HIỆU** của **778** dòng *(đã nối mà nhãn còn `UNMAPPED` — `work_status` đóng băng lúc nạp, `INV-I08`)* trừ **425** dòng *(đủ phân loại mà chưa nối — cả **425/425** đều có `hd`+`pay_type`+`cdt1`+`doc_no`)* ⇒ nó **che đi 1.203 dòng**, nói **nhỏ hơn sự thật 3,4 lần**, và sẽ **về 0** nếu hai nhóm cùng tăng. Hai cột trả lời **hai câu hỏi khác nhau** ⇒ cái sai là **phép TRỪ**. ⓓ Cửa lô ⛔ **KHÔNG nhận `pm_line_ids`** và ⛔ **KHÔNG BAO GIỜ nhận `force`** *(cùng luật `§4e ⓷`)*; `tự chứng` lấy **CẢ CHÙM** cùng mã và ⛔ không bao giờ một **tập con**. **+1 mã lỗi** `FLS-GHEP-KHONG-TU-CHUNG`. ⛔⛔ Và chính phép đo bắt **một khuyết tật thật**: `ds_tu_chung` xét *"đã bị ghép"* trước *"cùng tiền tệ"* ⇒ **202 dòng** khác tiền tệ bị dán nhãn *"lệch tiền"*.
- **v2.5** *(2026-09-09, `QĐ-ITL-117`)*: ⭐⭐⭐ **Thêm `§4e` — KHAI THỨ TỰ CẢ LÔ, tuyến **thứ 29**, và nó ⛔ **KHÔNG nhận `thu_tu`**.** Sinh ra từ một câu hỏi của owner khi soi màn đã chạy: *"bước này hơi buồn cười, trong GGSheet đang đưa về định dạng chung như thế nào?"* — và ba phép đo cho thấy câu hỏi **đúng**. ① Vùng THÔ ⛔ không có khuôn chung *(sê-ri **4.175** · chuỗi **4.190** · 3 ô rỗng)*, và khác biệt là **theo SHEET** *(16 nguồn toàn sê-ri · 34 toàn chuỗi · **0** trộn)*, ⛔ không theo dòng. ② Tab `Bank Transactions` **CÓ** chuẩn hoá hết — nhưng nó là **THƯỚC** của nhánh `oracle-parity`, ⛔ không phải đầu vào: đọc nó là mất khả năng bắt nó sai, mà nó **đã sai** *(93% dòng, ~181 tỷ lệch kỳ)*. ③ ⭐⭐⭐ Trên **4.187** ô chuỗi: phần **TRƯỚC** dấu `/` lớn nhất **12** — `0` lần `>12`; phần **SAU** lớn nhất **31** — **2.296** lần `>12`. Và ⛔ không phải suy ở mức sổ: **34/34** nguồn chuỗi **tự chứng minh bằng dữ liệu của chính nó**; `chac_dmy` = **0** khắp 60 nguồn; mâu thuẫn **0** ⇒ máy đề xuất `mdy` **34 lần, 34 lần một đáp án**. ⇒ Bắt kế toán bấm **27** cú để trả lời một câu dữ liệu đã tự trả lời là bắt họ **bấm theo phản xạ** — **đúng cái lo** mà câu *"⛔ không có nút khai tất cả"* ở `§4d ⓸` dựng ra để chặn. ⇒ `§4d ⓸` dòng đầu **BỊ LẬT**, và ranh giới mới nằm ở **TỰ CHỨNG**: cửa **đo lại** phía máy chủ rồi ghi đúng cái nó đo ra. **+1 mã lỗi** `FLS-THU-TU-KHONG-TU-CHUNG` *(422 — từ chối **CẢ LÔ**, ⛔ 0 bản khai mới)*. ⛔⛔ Và bộ test bắt **một khuyết tật thật**: nhánh *"⛔ không có bằng chứng"* xếp trước *"⛔ không cần khai"* làm nguồn **toàn ngày sê-ri** (16/60) NỔ CẢ LÔ.
- **v2.4** *(2026-09-08, `QĐ-ITL-113`)*: ⭐⭐⭐ **Thêm `§4d` — THỨ TỰ NGÀY, hai cửa mới (24 → 26 tuyến).** `GAP-NAP-02` ghi *"lô thật gần như chắc chắn có ngày mơ hồ"* — đó là một **suy luận**; đo thật trên ảnh chụp `chup_id 23719`: ⛔ **1.894/8.368 dòng (22,6%), trải 29/60 nguồn**. ⭐⭐⭐ Và phép đo **LẬT** đúng cái mặc định ai cũng sẽ chọn: **29/29** nguồn ấy là **`mdy`**, ⛔ **0** nguồn `dmy` ⇒ một mặc định `dmy` *"vì đây là Việt Nam"* sẽ **hoán ngày↔tháng trên 1.894 dòng** *(lớp `QĐ-ITL-17`, ~181 tỷ sai kỳ)*. Chỗ ở: `fls_khai_cot.thu_tu` *(migration `0019`)* — `cot` nói *đọc cột nào*, `thu_tu` nói *đọc thế nào*, **cùng bản chất** ⇒ cùng một dòng. ⛔ Khoá cửa trả là `de_xuat` ⛔ **không** phải `thu_tu`: **máy đề xuất, NGƯỜI quyết**. Và ⛔ không có cửa *"khai tất cả"*.
- **v2.3** *(2026-09-08, `QĐ-ITL-110`)*: ⭐⭐⭐ **Thêm §4c — nhóm ẢNH CHỤP, và nó sinh ra vì §4b ⛔ KHÔNG CÓ ĐƯỜNG VÀO.** Đo trên bảng tuyến thật: **20** tuyến, và `F04` cần **5** cửa thì **3 cửa ⛔ không tồn tại** *(`GET /sources` · `GET …/khai-cot` · một đường đọc vùng CHUẨN)*; hai cửa **có** thì cả hai đòi người gọi **đưa sẵn `dong`** — một tiền đề của `QĐ-ITL-105` ⓷ *(tải tệp)* mà **`QĐ-ITL-109` đã lật**. ⇒ Owner chốt **đường ẢNH CHỤP**: 3 bảng `fls_chup`/`fls_chup_nguon`/`fls_chup_dong` + **4 tuyến mới (20 → 24)** + `fls_run.chup_id` **nullable cố ý**. ⚠⚠ **Và bia cho một lập luận SAI của tôi:** tôi dẫn `GAP-API-04` *("timeout 3/3")* để chống đường đọc sống — phép đo ấy là của workbook **`ADJUSTED`**, ⛔ không phải của `R \|`; đo chính `R \|` ngày 08/09 ra ⭐ **4,4 giây / 60 sheet / 8.365 dòng**. ⇒ Lý do thật của ảnh chụp ⛔ **không phải tốc độ** mà là **§4b ⓶**: hai cửa đọc Sheets sống ở **hai thời điểm** thì lời hứa *"xem trước = thứ sẽ ghi"* **vỡ trong im lặng**; cùng một `chup_id` thì nó đúng **bằng cấu trúc**. ⭐ Ảnh chụp giữ **ô NGUYÊN VĂN trước `chuyen()`** ở `jsonb` — ép về `text` là dựng lại đúng cái bẫy đã cắn hai lần *(sê-ri ngày thành `"45586"`)*. ⛔ Khai luôn **3 thứ nhóm này CỐ Ý không giải**: `GAP-CHUP-01` *(ai bấm chụp)* · `GAP-CHUP-02` *(⛔ kho ⛔ không có trạng thái `InActive`/`Closed` ⇒ `BA-06` §7 ① chưa dựng đủ được)* · `GAP-CHUP-03` *(dọn ảnh chụp cũ — ~3 triệu dòng/năm)*.
- **v2.2** *(2026-09-08, `GAP-KHAI-01`)*: ⭐⭐ **Biên bản đi từ 8 lên 9 luật** — thêm **§4b ⓹b `S10`** *(hai bản khai phải trỏ cùng một cột)*, và ghi rõ `S9` *(số dư)* **chỉ áp cho lằn quỹ**. ⛔⛔ **Và khai một khoá đáp ứng bị BỎ QUÊN:** đường `422` `FLS-SOAT-CHAN` vẫn luôn kèm `error.bien_ban` — câu ấy **đúng** *(nói “bị chặn” mà ⛔ không nói **chặn vì luật nào** là bắt người dùng đoán)* — nhưng khoá ấy ⛔ **chưa bao giờ được khai** ở tầng đóng gói, nên đường ấy **NỔ** ngay lần đầu có một lô thật bị chặn. Nó sống sót vì ⛔ **không bài nào từng làm ĐỎ một luật hạng `CHẶN`** — mọi bài đều dùng dữ liệu sạch. ⇒ **Một nhánh lỗi ⛔ chưa ai đi qua là một nhánh CHƯA BIẾT CÓ CHẠY.**
- **v2.1** *(2026-09-07, `CR#11`)*: ⭐⭐⭐ **Thêm **§4b — nhóm NẠP**, nhóm mà hôm nay ⛔ **KHÔNG TỒN TẠI**: đo được **0/17** tuyến là cửa nạp *(8 `GET` + 9 `POST`, mọi `POST` đều **sửa một dòng ĐÃ CÓ**)*, và đường duy nhất vào kho là **một lệnh dòng lệnh đọc Google Sheets**. Ba tuyến: ghi **bản khai ánh xạ cột** · **xem trước** · **nạp**. ⭐⭐ **Xem trước là TUYẾN RIÊNG, ⛔ không phải một cờ** — hai việc khác nhau về **hậu quả** thì ⛔ không được khác nhau bằng một chữ trong thân yêu cầu. ⭐ **Ba hạng quyết định HTTP**: `CHẶN` ⇒ **422** và ⛔ không ghi dòng nào; `CỜ` ⇒ **201** *(vẫn ghi đỏ trong biên bản — những dòng ấy là **tiền thật**, vứt đi là vi phạm *"⛔ 0 dòng rơi im lặng"*)*. ⭐ Chống trùng **dùng lại `content_key`** đã `NOT NULL` từ migration `0001` — ⛔ **không dựng cơ chế chống trùng thứ hai**. **+4 mã lỗi** `FLS-KHAI-KHONG-CO` *(409, ⛔ không phải 404 — nguồn **có**, chỉ là chưa ai khai cách đọc)* · `FLS-KHAI-THIEU` · `FLS-SOAT-CHAN` · `FLS-NGUON-LA`.
- **v2.0** *(2026-09-04, `QĐ-ITL-83·86·87`)*: ⭐ Hai mã lỗi mới — **`FLS-UNKNOWN-CODE`** *(`hd` ngoài `Mapping Master`)* và **`FLS-BAD-FORMAT`** *(kỳ sai khuôn `YYYYMM`)*. ⛔⛔ Trước 04/09 đường `/adjust` **⛔ không kiểm gì cả**. ⭐ `force` ⛔ **không** vượt qua được hai phép này *(nó để ghi đè một **bất đồng**, ⛔ không phải để tạo một giá trị **⛔ không tồn tại**)*; giá trị **rỗng** luôn đi qua *(phép **BỎ GÁN**)*; danh mục **`0` dòng** ⇒ ⛔ **không chặn** *(`INV-I17`)*. Đường này nay **đọc** thêm `fls_mapping_master` — cổng `soi_bang_tuyen` bắt được chỗ thiếu khai.
- **v1.9** (2026-08-28, `QĐ-ITL-72`/`QĐ-ITL-73`): ⛔ **`POST .../done`: `reason` ⛔ KHÔNG bắt buộc trong MỌI trường hợp** — owner bỏ hàng rào *(nguyên văn "ko cần ghi lý do")*, kể cả khi dòng còn thiếu trường hoặc **kỳ đã chốt**. ⇒ mã `422` *"thiếu lý do"* của v1.8 **⛔ không còn xảy ra** ở đường này. ★ Lý do: **một ô lý do bị bắt buộc thì nó thành một ô RÁC** *(gõ một chữ rồi bấm)*, và một cột lý do toàn chữ "x" **tệ hơn** một cột trống — cột trống còn thành thật. Cái giữ lại: `actor`/`at` + phép đếm dòng bấm-xong-mà-còn-thiếu. ⚠ **`POST .../reopen` VẪN đòi `reason`** *(`400`)* — owner ⛔ chưa nói về nó, và nó là chuyện khác: kéo lại một dòng người khác đã kết luận là xong thì **lật kết luận của người khác**. ⭐ **Ghi rõ hành vi đã ĐO** *(`QĐ-ITL-73`)*: `POST /ledger/{itl_id}/adjust` trên một ô **đã có giá trị** ⇒ `409 FLS-CONFLICT-SOURCE` kèm giá trị đang có; gửi lại với `force=true` ⇒ ghi được; sửa **lần hai/ba** ⇒ được, mỗi lần một dòng nhật ký; `POST .../reverse` **hoàn tác** ⇒ giá trị lùi về bút toán trước. ⭐ **Cột nguồn ⛔ KHÔNG bị ghi đè**. ⛔ **31 cột còn lại** chỉ-đọc *(gõ tên khác ⇒ `400`, kèm danh sách 7 trường)*; **kỳ đã CHỐT** ⇒ `409` kể cả `force`. ⭐ Dòng **đã bấm xong VẪN sửa được**, và nó ⛔ không tự quay lại hàng chờ.
- **v1.8** (2026-08-28, `QĐ-ITL-71`): ⭐⭐ **Thêm `POST /queue/{itl_id}/done` + `POST /queue/{itl_id}/reopen`** *(đóng `GAP-JOIN-06`)*. Owner chốt: **NGƯỜI bấm xong** mới rời hàng chờ, ⛔ không phải máy tự nhả khi thấy đủ 5 trường — căn cứ nghiệp vụ: máy tự nhả thì kế toán **mất chỗ đánh dấu việc đang làm dở**. `done`: thân yêu cầu `reason` **tuỳ ý** khi dòng đã đủ 5 trường hợp đồng, **BẮT BUỘC** *(`422`)* khi còn thiếu trường hoặc **kỳ đã chốt** — lúc đó người đang **ghi đè kết luận của máy** *(`INV-I16`)*; thông báo **nói ra thiếu trường nào**. Bấm hai lần ⛔ không thành hai sự kiện: trả `da_co=true` kèm **ai đã bấm** và **lúc nào**. ⭐⭐ **Kỳ đã chốt VẪN bấm xong được — cố ý KHÁC `INV-I13`** *(mọi cửa ghi khác từ chối kỳ chốt)*: kỳ chốt thì kế toán ⛔ không sửa được giá trị nào, nếu cũng ⛔ không đánh dấu xong được thì những dòng ấy nằm trong hàng chờ **vĩnh viễn** mà ⛔ không ai làm gì được ⇒ hàng chờ tự biến thành **rác**. `reopen`: `reason` **BẮT BUỘC** *(khác `done` — dòng này đã có NGƯỜI kết luận là xong, kéo lại là **lật kết luận của người khác**)*; `409` nếu dòng ⛔ chưa từng được bấm xong *(`ChuaXong` — cố ý **khác** *"đã xong"*: màn hình vẽ hai nút khác nhau)*. ⇒ `GET /ledger/{itl_id}` thêm **`da_xong`** *(ai bấm · lúc nào · lý do)*: một dòng "xong" mà màn hình ⛔ không nói ai bấm thì nút đó là một cái nút **⛔ không ai chịu trách nhiệm**.
- **v1.7** (2026-08-28, `QĐ-ITL-69`, `CR#9`): ⭐⭐ **Thêm `POST /queue/{itl_id}/unmatch` — ĐƯỜNG LÙI của phép ghép** *(đóng `GAP-JOIN-05`)*. Thân yêu cầu **chỉ có `reason`**; ⛔ **không** nhận `pm_line_ids`: đường này bỏ **TOÀN BỘ** mối nối của dòng. Bỏ lẻ một mối nối làm `Σ mối nối ≠ tiền bank`, tức **tạo ra đúng cái trạng thái sai** mà cổng `SIGMA_MOI_NOI` dựng ra để bắt — muốn đổi một dòng lệnh thì **bỏ cả chùm rồi ghép lại**. ⚠ `POST` chứ ⛔ **không** `DELETE`: bỏ một mối nối là **THÊM một dòng** *(`INV-I08`)*, và một cửa `DELETE` mở tư duy đúng cái hành vi cả tầng ghi cấm. Trả về: `da_bo` *(các mối nối đã bỏ, kèm `lan`)* · `but_toan_dao` · ⭐ **`bo_qua`** *(bút toán của phép ghép mà cửa này CỐ Ý ⛔ không đảo — vì **người** đã gõ tay lên ô ấy sau phép ghép)* · `evt_id`. Mã lỗi: `409` khi ⛔ không có mối nối nào *(`KhongCoMoiNoi` — cố ý **khác** `DaGhep`: chưa ghép và đã ghép là hai trạng thái, và màn hình vẽ hai nút khác nhau)* · `409` kỳ đã chốt *(⛔ kể cả `force`)* · `400` thiếu `reason`.
- **v1.6** (2026-08-28, `QĐ-ITL-64`): ⛔⛔ **Tập ghi 10 → 7 tên** — bỏ `cdt1_cfa1`/`cdt1_cfa2`/`alloc_method` khỏi `/adjust`. Owner trả lời *"họ ko sửa [vùng ALLOCATE], chỉ sửa các trường đã liệt kê trước đó"*, và owner đưa **nguyên văn 3 công thức** cho thấy cả ba ô là **công thức** tra `Mapping Master` K/L theo `hd` ⇒ **máy suy**, ⛔ không ai override. ★ Đây là lần **lật một phần `QĐ-owner-0824`** *(câu "7 khối + vùng phân bổ" nay chỉ còn 7 khối)*; biên bản cũ **giữ nguyên**, chỉ đánh dấu **BỊ HẸP**. Gõ một trong ba tên ⇒ `400`, và có **bài test khoá cửa** *(⛔ không chỉ bỏ tên khỏi danh sách — ba cột vẫn tồn tại trong `fls_itl` nên câu SQL viết tay vẫn chạm được)*.
- **v1.5** (2026-08-28): ⭐⭐⭐ **`QĐ-ITL-63` đóng `GAP-CR1-04`** — cửa ghép **TAY** đòi **CẢ HAI** điều kiện, lấy cái **nhỏ hơn**: lệch ≤ **1.000 đồng** VÀ ≤ **0,5%** tiền bank. Một mình con số tuyệt đối hở đầu khoản **nhỏ** *(`100 ↔ 1.099` = lệch 999%)*; một mình tỷ lệ hở đầu khoản **lớn** *(0,5% của 3,7 tỷ = 18,5 triệu)*. Hai điều kiện **bằng nhau tại 200.000 đồng**. ⛔ Cửa **TỰ ĐỘNG** giữ `QĐ-ITL-57`; ngoại tệ vẫn **0** *(`QĐ-ITL-62`, `min(0, tỷ lệ) = 0`)*. ⭐ `/pm-candidates` trả **đúng con số cửa sẽ cưỡng chế** *(⛔ không phải con số rộng hơn — nếu không, bậc "gần tiền" thành một cái bẫy)*; `/match` `422` trả **Σ · tiền bank · dung sai + tỷ lệ**.
- **v1.4** (2026-08-27, sau khi ghép lệnh chạy thật): ✅ **Hai đường `/pm-candidates` + `/match` từ ⛔ BỊ CHẶN sang ĐÃ CHẠY THẬT** — owner chốt **`QĐ-ITL-61`** *(lưu ảnh chụp dòng lệnh vào kho, `fls_pm_line`, migration `0011`)*, đóng **`GAP-API-04`**. ⛔⛔ **`CR#6` sửa đặc tả**: thân `/match` là `{pm_line_ids}` chứ ⛔ không phải `{pm_id}` — 526 phiếu mang 2–36 reference khác nhau nên ghép vào phiếu là **máy quyết thay người**. ⭐ Ứng viên xếp theo **4 bậc CÓ TÊN** + trả **TUỔI của ảnh chụp**; `/match` ghi **THÊM** *(`fls_pm_link` `hinh='T'` + sự kiện + bút toán `hd`/`cdt1`)* và sổ ⛔ không đổi một ô. ⛔ Mở **`GAP-JOIN-04`** *(⛔ không xếp được theo ngày/payee — ảnh chụp không mang PII; trên sổ thật chỉ 1/25 dòng có ứng viên bậc `ma`)*, **`GAP-JOIN-05`** *(⛔ chưa có đường BỎ mối nối)*, **`GAP-CR1-04`** *(dung sai tuyệt đối 1.000 VND cho ghép 100 VND với 1.099 VND — đã làm 2 bài test xanh SAI)*. **589 phép thử** · `pg_verify` **15 bảng/view**.
- **v1.3** (2026-08-27, sau khi `P5` chạy thật): ⛔⛔ **SIÊU BỎ câu *"trường hợp-đồng cập nhật `*_thyt`"*** *(`CR#5`)* — nó sai `INV-I08` **và** `QĐ-ITL-35`; giá trị người gõ vào `fls_adjustment` + khung xem `fls_sua_tay`, và ⛔ **không một ô nào của `fls_itl` đổi**. ✅ **4 đường ghi đã xây và chạy thật** + thêm `✅ /ledger/{id}/fields/{field}` *(hỏi nguồn trước khi gõ)* và `✅ /adjustments/{id}/reverse` *(đảo = thêm dòng)*. Thêm luật **`actor` từ THẺ** *(gửi trong thân ⇒ 400)*, **một chỗ duy nhất được ghi**, **bút toán + nhật ký một giao dịch**, `409` kèm `error.khac`, **kỳ chốt 409 kể cả `force`**, `until` bắt buộc, gõ lại cùng giá trị ⇒ `da_co`. Luật *"không `PUT`/`DELETE`"* mạnh lên thành **⛔ không tuyến nào DÙ PHƯƠNG THỨC GÌ được ghi vào `fls_itl`**. Thêm mã **`413`**. ⛔ **`/match` + `/pm-candidates` đánh dấu BỊ CHẶN** ⇒ mở **`GAP-API-04`**.
- **v1.2** (2026-08-27, sau khi `P4` chạy thật): ⭐⭐ **Thêm §1 luật PHẠM VI ĐỌC** — cửa chỉ trả dòng của lần nạp **thật**; `?run_id=` **giao** bản trắng chứ ⛔ không thay thế; ⛔ **không có** `?pham_vi=ca_kho`. Thêm luật **kết nối bị kho chặn ghi** *(máy từ chối chạy nếu không)*, **tiền ra JSON là chuỗi**, `data_status` mặc định `flash`. ✅ Đánh dấu **5 đường đã xây và chạy thật** + thêm `✅ /queue/summary` *(⛔ không có dòng "tổng")*; **6 đường còn ⬜**. ⛔ **`/queue` bỏ *"nhãn máy dán"*** *(`QĐ-ITL-56`/`58`)* và ghi rõ phép xếp nằm **trong** câu có phạm vi *(`CR#4`)*. ⛔⛔ **`/gates` KHÔNG BAO GIỜ toàn xanh**: 4 cổng kế toán + `BON_DUONG` khai tường minh **CHƯA ĐO ĐƯỢC**; `dat=true` mà không nói *đã đo được gì* là **lỗi nổ ngay**. Thêm **5 mã lỗi** `401/404/405/400/500` kèm lý do từng cái. Mở **`GAP-API-03`**.
- **v1.1** (2026-08-25, rà ERD↔màn hình + grill): **⛔ "chỉ ghi 5 trường" của v1.0 đã SIÊU BỎ** — tập ghi = 5 hợp đồng ∪ `{id_payee,invoice,cdt1_cfa1,cdt1_cfa2,alloc_method}` *(`QĐ-owner-0824`, §3)*. Thêm **3 endpoint đọc F06** `/sources`·`/mapping-master`·`/le` + `/queue/state` *(view `fls_queue_state`)*. **Gỡ `/labels/trend`** *(màn Xu hướng đã bỏ)*. `/weekly` đổi vai: kế toán tự xem → nút Xuất PDF ở F03.
- **v1.0** (2026-08-24): Viết mới cho FLS. Prefix `/api/fls/v1/`; **ghi = APPEND** *(`AUD-1`/`INV-I08`)*; ⛔ chỉ ghi 5 trường ADJUSTMENT + lý do, không cửa `PUT/DELETE` trên sổ; `409 FLS-CONFLICT-SOURCE` cho *"hệ KÊU khi gõ khác nguồn"* *(`US-025`)*; cột lý do là chỗ `US-045` đếm; ranh giới đọc-chỉ với mọi nguồn ngoài `fls_*`.
