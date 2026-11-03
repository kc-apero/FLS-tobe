# 07 — API CONTRACT: FLS

**Version:** v2.0 · **Ngày:** 2026-08-27 · **Chủ sở hữu:** BA/PO + Tech Lead
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
| ✅ `GET /api/fls/v1/ledger` | dòng `fls_itl`, lọc `?period=&le=&status=`, phân trang | E1/E2 |
| ✅ `GET /api/fls/v1/ledger/{itl_id}` | một dòng + 36 canonical + lineage | drill |
| ✅ `GET /api/fls/v1/queue` | ⭐ **hàng chờ**: chỉ `work_status='UNMAPPED'`, **xếp theo tiền giảm TRONG TỪNG tiền tệ** + `hang` + `luy_ke_pct`; `?curr=` `?den_pct=90` *("xem tới đây là phủ 90% tiền")*. ⛔ **Bỏ *"nhãn máy dán"*** — `QĐ-ITL-56`/`58`: không có quy định nào để máy dán. ⛔⛔ Phép xếp nằm **TRONG** câu có phạm vi, ⛔ không phải một khung xem lọc ở đầu ra *(`CR#4`)* | `US-039` |
| ✅ `GET /api/fls/v1/queue/summary` | ⭐ số dòng + Σ tiền hàng chờ **theo TỪNG tiền tệ**. ⛔ **Không có dòng "tổng"** — cộng hai tiền tệ ra một con số là đúng cái sai đã tạo ra *"310 dòng phủ 90% tiền"* | `US-039` |
| ⬜ `GET /api/fls/v1/queue/coverage` | độ phủ *(mỗi nhóm × ngày đã có người ghi chưa)* | `US-038` |
| ✅ `GET /api/fls/v1/gates` | ⛔⛔ **KHÔNG BAO GIỜ toàn xanh.** Trả cổng **đo được từ kho** *(`KHO_SACH` · `SIGMA_MOI_NOI` · `RUN_DEM_KHOP`)* **cộng** 4 cổng kế toán + `BON_DUONG` khai **tường minh** là `dat=null` = **CHƯA ĐO ĐƯỢC** kèm lý do. Một màn *"4/4 cổng xanh"* trong khi 4 cổng kế toán chưa hề đo là con số nói dối thô nhất của cả hệ. ⛔ Kiểu cưỡng chế: `dat=true` mà không nói **đã đo được gì** là **lỗi lập trình**, nổ ngay | `US-008/029` |
| ✅ `GET /api/fls/v1/journal?itl_id=` | nhật ký 7 trường của một dòng | `US-030` |
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
| ✅ `POST /api/fls/v1/queue/{itl_id}/match` | `{pm_line_ids: [...], reason}` `?force=` | ⭐⭐ **ghép = THÊM.** ⛔⛔ Thân **⛔ KHÔNG phải `{pm_id}`** *(một phiếu)* — xem `CR#6`: 526 phiếu mang 2–36 reference khác nhau, nên ghép vào phiếu thì **máy phải tự chọn dòng** = máy quyết thay người *(`INV-I16`)*. Gửi `{pm_id}` ⇒ **400 kèm lý do**. Ghi trong **MỘT giao dịch**: `fls_pm_link` *(`hinh='T'`)* + `fls_queue_event` + bút toán `hd`/`cdt1` **suy từ dòng lệnh**. ⛔ **`fls_itl` không đổi một ô** *(`INV-I08`)*. ★ `hd`/`cdt1` chỉ được suy khi **cả N dòng lệnh ĐỒNG Ý**; N dòng nói N thứ ⇒ trả `khong_suy_duoc` *(`INV-I16`)*, ⛔ không lấy dòng đầu tiên. ⛔ Bảy chỗ từ chối: ngoài phạm vi `404` · kỳ chốt `409` *(⛔ kể cả `force`)* · **đã ghép `409`** kèm mối nối đang có · mã dòng lệnh không có trong ảnh chụp **của chính lần nạp đó** `400` · **tiền tệ khác `422`** *(kiểm TRƯỚC Σ)* · **`Σ` lệch `422`** kèm ba con số, giữ `UNMAPPED` *(⛔ không chia bừa)* · `status` không phải `Approve` `422` *(trừ `force`, và `force` để lại vết)* |

✅ **Hai đường trên đã MỞ 27/08** *(`QĐ-ITL-61` — owner chốt lưu ảnh chụp dòng lệnh vào kho)*. Chạy thật trên **sổ thật**: `/pm-candidates` đo trên **25 dòng hàng chờ**, ảnh chụp **3.703 dòng lệnh · 1.468 phiếu**. ⛔ Nhưng đọc kỹ **giới hạn** mới: xếp ứng viên **⛔ không có trục `ngày` và `payee`** — ảnh chụp cố ý ⛔ không mang PII và ⛔ không mang ngày *(`GAP-JOIN-04`)*. Và **⛔ chưa có đường BỎ mối nối**: ghép sai thì hiện chưa sửa được *(`GAP-JOIN-05`)*.

⛔⛔ **Không có** `PUT`/`DELETE` trên `fls_itl` — và từ v1.3 luật này mạnh hơn: ⛔ **không tuyến nào, DÙ PHƯƠNG THỨC GÌ, được GHI vào `fls_itl`**. Mỗi tuyến khai tường minh **bảng nào nó ghi**, và cổng quét bảng tuyến chặn `fls_itl` ở mọi phương thức. *(Luật cũ chỉ kiểm `PUT`/`DELETE`/`PATCH` — nên một `POST .../adjust` ghi thẳng vào sổ sẽ **đi qua trong im lặng**, đúng cái đặc tả v1.1 từng mở đường cho. Cổng chung **#12**.)*

⭐⭐ **Và cửa GHI ⛔ không làm yếu cửa ĐỌC:** **bảng tuyến** chọn kết nối, ⛔ không phải hàm xử lý chọn. Mọi tuyến `GET` **luôn** chạy trên kết nối bị PostgreSQL **chặn ghi**, kể cả khi máy đang mở nhóm ghi *(đo bằng cách đếm số lần mở kết nối ghi = **0** sau bốn đường `GET`)*. Máy mặc định chạy ở chế độ **CHỈ ĐỌC**: mọi đường ghi trả `405` cho tới khi có `--cho-ghi` tường minh.

---

## §4 · Nhóm CHẠY — máy quét & pipeline

| Method · Path | Vai |
|---|---|
| `POST /api/fls/v1/runs` | chạy adapter → canonical → sổ; trả `run_id` + biên bản `ACC-1…4` |
| `GET /api/fls/v1/runs/{run_id}` | trạng thái + kết quả 4 bất biến; `ACC` fail ⇒ `dq_failed` |
| `GET /api/fls/v1/runs/{run_id}/parity` | biên bản đối chiếu G2/G3 — **chênh liệt kê từng dòng**, ⛔ không phần trăm |

---

## §5 · Mã lỗi

| Mã | Khi | HTTP |
|---|---|---|
| `FLS-CONFLICT-SOURCE` | gõ khác nguồn, chưa `force` *(`US-025`)* | 409 |
| `FLS-LOCKED-PERIOD` | ghi vào kỳ `locked` *(`INV-I13`)* | 409 |
| `FLS-CONTRACT-DRIFT` | reader lệch `ITL-CONTRACT` *(G1)* | 500, chặn |
| `FLS-DQ-FAILED` | `ACC-1…4` không đạt | 422 |
| `FLS-UNMAPPED-HIDDEN` | cố ghi giá trị cứng vào chỗ `UNMAPPED` *(`INV-I16`)* | 422 |

| `FLS-UNKNOWN-CODE` ⭐ | `hd` ⛔ **không có** trong `Mapping Master` *(`DT-I09`)*. ⚠ Lỗi mang **số mã đang giữ** + **tên lệnh nạp lại**, và nếu có mã chỉ khác **hoa-thường** thì **chỉ ra mã thật**. ⛔ `force` ⛔ **không** vượt qua được | 400 |

| `FLS-BAD-FORMAT` ⭐ | giá trị sai **khuôn** — hôm nay chỉ áp `svc_start`/`svc_end`, khuôn **KỲ** `YYYYMM` *(`DT-I09` #6)* | 400 |
| `FLS-ACCR-UNREADABLE` | không đọc được kết quả A-CCR ⇒ cổng số dư chặn | 503 |
| `FLS-UNAUTHORIZED` | ⭐ v1.2 — thiếu thẻ hay thẻ không hợp lệ. ⛔ **Kiểm thẻ TRƯỚC định tuyến**: người không có thẻ ⛔ không được biết đường nào tồn tại. ⛔ Lý do chi tiết *(hết hạn? sai chữ ký?)* **chỉ vào log**, ⛔ không ra ngoài — nói cho người gõ thẻ biết họ sai ở đâu là giúp họ dò thẻ | 401 |
| `FLS-NOT-FOUND` | ⭐ v1.2 — **không có, HAY có nhưng ngoài phạm vi**. ⛔ Cùng một câu trả lời cho cả hai: một `403` nói *"có dòng này nhưng anh không được xem"* — tức là **tiết lộ dòng đó tồn tại** | 404 |
| `FLS-METHOD` | ⭐ v1.2 — đường có, phương thức không. `P4` chỉ đọc nên mọi `PUT`/`DELETE`/`PATCH`/`POST` về đây | 405 |
| `FLS-BAD-REQUEST` | ⭐ v1.2 — tham số sai *(`limit` không phải số, thiếu `?itl_id=`)*. ⛔ Phải là `400`, ⛔ không được thành `500` | 400 |
| `FLS-TOO-LARGE` | ⭐ v1.3 — thân yêu cầu quá to *(> 64 KB)*. ⛔ Máy **từ chối mà không đọc hết** thân — đọc hết là làm đúng cái việc mà giới hạn này dựng ra để tránh — nên nó **đóng kết nối** *(nếu không, byte còn lại sẽ bị đọc thành yêu cầu SAU)* | 413 |
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
| `GAP-API-03` ⭐ | **Cổng *"bốn đường"* ⛔ KHÔNG đo được từ kho.** Bốn đường là `vào = sổ + loại + rỗng + trùng`, mà **`rỗng` và `trùng` ⛔ không được lưu ở bảng nào** — chúng chỉ in ra lúc chạy `nap_that.py` rồi mất. ⇒ Muốn có cổng này thì phải **ghi bốn con số vào `fls_run`**. *(Phát hiện 27/08 khi cổng cũ **đỏ GIẢ**: nó so `row_count` với `count()+count()`, trong khi `row_count` **được đếm từ chính bảng đó** ⇒ phép so **vòng tròn**. Cổng chung **#11**.)* |

---

## Changelog
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
