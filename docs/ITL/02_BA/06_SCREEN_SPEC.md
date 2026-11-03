# 06 — SCREEN SPEC: FLS

**Version:** v2.4 · **Ngày:** 2026-08-25 · **Chủ sở hữu:** BA/PO
**Thay thế:** v0.1 *(bản copy chương trình, 15 màn M0–M6)* — đã khai tử. Đóng `GAP-ITL-53`.

**Căn cứ:** `QĐ-ITL-38` *(app thay Google Sheets — nơi kế toán thao tác)* · `07_API_CONTRACT` v1.0 · demo `Artifacts/Demo-MVP-So-may-ITL.html` *(bản v5 — **spec hành vi sống**, đã đối chiếu 45 US)*.

**★ Wireframe đầy đủ:** [`Artifacts/FLS-Wireframe.html`](Artifacts/FLS-Wireframe.html) — 7 màn thao tác + ma trận **phủ 45 US**, bấm được. Là bản field-level sống của spec này.

> ⚠ **Đây là file rủi ro số một của cả dự án.** `QĐ-ITL-38` biến màn hình thành **nơi kế toán làm việc thật**, thay Google Sheets mà 2–3 người đó đã dùng nhiều năm. **Cổng nghiệm thu không phải "app có chạy không" mà "họ có DÙNG không"** — và họ chỉ dùng nếu app **không thua Sheets ở những thao tác hằng ngày**.

---

## §1 · Điều kiện SỐNG CÒN — hành vi Sheets bắt buộc phải có

Thiếu **bất kỳ** dòng nào dưới đây, kế toán **về Sheets** và toàn bộ FLS thành rác. Đây là danh sách nghiệm thu cứng, không phải "nice to have".

| # | Hành vi | Vì sao bắt buộc |
|--:|---|---|
| 1 | **Điều hướng bàn phím** — Tab / Enter / mũi tên di chuyển ô; Enter xuống dòng | kế toán gõ không rời tay khỏi bàn phím |
| 2 | **Dán một vùng** *(paste nhiều ô từ clipboard)* | họ copy từ file khác vào; thiếu là chậm gấp nhiều lần |
| 3 | **Kéo xuống** *(fill-down một giá trị cho nhiều dòng)* | gõ 5 trường cho một loạt dòng cùng loại |
| 4 | **Hoàn tác** `Ctrl+Z` | sai một phát là sửa được ngay, không sợ |
| 5 | **Filter view** — lọc/sắp xếp **cách nhìn**, không đổi dữ liệu | xem theo tiền, theo ngày, theo nhãn tuỳ ý |
| 6 | **Đông cứng tiêu đề** + cột khoá khi cuộn | sổ dài, mất tiêu đề là mất phương hướng |
| 7 | **Số kiểu kế toán** — `tabular-nums`, phân nhóm nghìn, âm màu đỏ | đọc tiền phải liếc ra ngay |
| 8 | **Lưu không cần bấm** — tự lưu theo lô *(debounce ~2–3s)* | Sheets không có nút Lưu; app có nút Lưu là đã thua |

★ Số 8 nối thẳng ràng buộc đã đo: BQ load-job APPEND **~2–4s/lần** ⇒ **cấm ghi mỗi ô một lần**; gom lô rồi ghi *(`QĐ-ITL` phiên 24/08, phương án 2+3)*.

### §1b · ⚠ Ba giới hạn wireframe tố cáo — spec §1 đang nhẹ tay

Dựng wireframe tương tác `SCR-F02`/`F01`/`F05` *(2026-08-24)* lộ ra ba chỗ §1 viết như thể dễ, nhưng không:

| # | §1 ghi | Thực tế |
|--:|---|---|
| 1 | *"điều hướng bàn phím · dán vùng · kéo xuống · hoàn tác"* — liệt kê như 4 dòng bảng | ⛔⛔ **CÂU NÀY ĐÃ BỊ PHÉP ĐO LẬT — giữ lại làm biên bản.** ~~Một `<table>` HTML KHÔNG làm nổi; bốn hành vi này đòi thư viện lưới thật~~. **Mũi thử 27–28/08 dựng đúng một `<table>` trần** *(⛔ không thư viện, ⛔ không mạng)* trên **dữ liệu thật** — **748 dòng × 52 cột = 38.896 ô** — và **cả 8 hành vi đều chạy**. Owner confirm ⇒ `QĐ-ITL-66`: **⛔ không thêm một phụ thuộc nào**. ★ Vì sao câu cũ sai: nó suy từ *quy mô tưởng tượng* **~192.000 ô**; bài toán thật **~39.000 ô** ⇒ **ảo hoá — lý do CHÍNH để chọn thư viện — có thể không cần**. ⇒ `GAP-SCR-01` **ĐÓNG** |
| 2 | *"lưu không cần bấm"* — một dòng | ⛔ Là **cả một cơ chế**: gõ tiếp khi lô trước đang bay · mạng đứt giữa chừng · hai người sửa một ô. Ràng buộc đo: load-job APPEND **~2–4s** ⇒ phải gom lô. Ba ca lỗi trên **chưa được đặc tả** ⇒ `GAP-SCR-04` |
| 3 | modal ghi đè *"hai nút"* — trong đó **[Sửa ở PM]** | ⚠ FLS **chỉ đọc** `fps_*` *(`QĐ-ITL-45`)* — **không sửa PM được**. Nút đó chỉ **nhắc người mở hệ PM khác**, không phải hành động trong app. Spec phải nói rõ, không để hiểu nhầm là app ghi ngược |

★ **Kết luận thẳng:** phần rẻ của màn hình *(5 màn, luồng, mã màu)* — spec đã đủ. Phần đắt *(lưới sửa được như Excel)* nằm gọn trong **một quyết định: `GAP-SCR-01`**, và nó quyết định lịch của cả `QĐ-ITL-38`.

---

## §2 · Bốn màn kế toán *(v1.5 — chỉ kế toán dùng)*

> ★ **Wireframe tương tác đã dựng 2026-08-24** cho `SCR-F02` *(sổ, drawer đối soát, sửa 7 khối + phân bổ)*, `SCR-F01` *(hàng chờ + cột lý do + bộ đếm `US-045`)*. Chúng là **spec hành vi sống** — field-level dưới đây bám theo.
>
> ⭐ **Cắt phạm vi 2026-08-25 (owner: hệ thống CHỈ kế toán dùng):** sidebar còn **4 màn có nghiệp vụ kế toán**. Ba màn bị hạ cấp/xoá vì không phải việc kế toán làm — **giữ thông tin, bỏ tab**:

| ID | Màn | Vai | Story | API |
|---|---|---|---|---|
| `SCR-F01` | **Hàng chờ** — lưới + lý do + hoãn + **Ghép lệnh** *(`OP-02`)* + ⭐ **Bỏ ghép** + ⭐ **Xong / Mở lại** | `AC-B` | `US-039/040/045` · `OP-02` | `GET /queue` · `POST /reason` · `/defer` · **`/match`** · ⭐ **`/unmatch`** *(`QĐ-ITL-69`)* · ⭐ **`/done`** · **`/reopen`** *(`QĐ-ITL-71`)* |
| `SCR-F02` | **Sổ ITL** — lưới quét + drawer đối soát, sửa **7 trường** *(`QĐ-ITL-64`)*; vùng phân bổ 🔒 **chỉ đọc** | `AC-B` | `US-025/026/030` | `GET /ledger` · `POST /adjust` · `/reverse` · ⭐ **`/done`** · **`/reopen`** |
| `SCR-F03` | **Cổng hôm nay** — 4 cổng + độ phủ + *báo cáo tuần (xuất)* | `AC-A` | `US-008/029/038` | `GET /gates` · `/coverage` |
| `SCR-F06` | **Danh mục · Nguồn** — nguồn/TK/ánh xạ + cảnh báo | `AC-C` | `US-001/018/031` | `GET /catalog` |
| *(xuyên suốt)* | **Nhật ký** — drawer 7 trường theo dòng | mọi vai | `US-030` | `GET /journal` |

**Đã bỏ khỏi sidebar kế toán** *(không mất thông tin)*:

| Cũ | Vì sao bỏ | Đi đâu |
|---|---|---|
| `SCR-F07` **Chạy · Kiểm tra** | máy/vận hành — kế toán không chạy pipeline | tín hiệu *"dữ liệu tới ngày X · DQ ✓"* → **badge** trên sidebar |
| `SCR-F05` **Một trang tuần** | tổng quan đọc, không thao tác | **nút "Xuất báo cáo tuần"** gấp trong `SCR-F03` |
| `SCR-F04` **Xu hướng nhãn** | theo dõi nhãn không là việc kế toán hằng ngày | bỏ hẳn *(luật 6 nhãn vẫn ở `US-036`/`GAP-ITL-56`)* |
| *Phủ 45 US* | ma trận cho BA/dev, không phải màn vận hành | tài liệu `Artifacts/UC-US`, không lên UI |

---

## §3 · `SCR-F02` Sổ ITL — lưới quét + panel đối soát đủ trường

⭐ **Sửa v1.2 (owner 2026-08-24):** kế toán **không thể quyết** gõ gì vào 5 trường nếu chỉ thấy 7 cột. Màn tách hai tầng: **lưới để quét**, bấm một dòng mở **panel đối soát đủ trường** để quyết rồi adjust ngay trong panel.

### Lưới (quét nhanh)
`itl_id · ngày · diễn giải · Nợ · Có · tài khoản · LE · HDCode · CDT1 · trạng thái` — lọc + "chỉ UNMAPPED". `UNMAPPED` hiện `chưa gán` nền vàng, không giá trị mặc định.

### Panel đối soát — ba nhóm đọc (bối cảnh) + hai nhóm sửa (A/B), đây mới là chỗ kế toán làm việc

⛔⛔ **HẸP v2.0 (owner 2026-08-28, `QĐ-ITL-64`): kế toán ⛔ KHÔNG sửa vùng phân bổ** — *"họ ko sửa, chỉ sửa các trường đã liệt kê trước đó"* ⇒ trường gõ được **10 → 7**; ba cột `CFA1`/`CFA2`/`Method` là **🔒 chỉ-đọc, máy suy** *(owner đưa nguyên văn 3 công thức: chúng tra `Mapping Master` K/L theo `hd`)*. Câu v1.4 giữ lại làm biên bản: ⭐ **Sửa v1.4 (owner 2026-08-24, `QĐ-owner-0824`):** kế toán **sửa tay tại Final cả 7 khối + phân bổ**, không chỉ 5 khối engine đọc. Panel tách rõ **Nhóm A** *(5 khối vào hợp đồng P&L)* và **Nhóm B** *(khối ⑥⑦ + phân bổ — sửa được nhưng ngoài P&L)* để không ai nhầm cái nào chạm báo cáo.

| Nhóm | Trường | Vai |
|---|---|:--:|
| **1 · Giao dịch gốc** | Ngày CT · Số CT · Diễn giải · Đơn vị tiền · PS Nợ · PS Có · Tài khoản | ⛔ chỉ đọc |
| **2 · Chuỗi lệnh** *(truy vết — vì sao gán được)* | ID PMSlip · **ID PMLine** *(`#N/A` = chưa ghép)* · ID PESlip/PILine | ⛔ chỉ đọc |
| **3 · Đối soát pháp nhân** | **LE (P) vs pháp nhân trả (L)** — lệch thì đỏ *(`US-032`)* | ⛔ chỉ đọc |
| **A · 5 khối engine P&L đọc** *(hợp đồng — đóng băng)* | HDCode · Loại GD · CDT1 · bắt đầu DV · kết thúc DV | ✅ **sửa** · có `*_thyt`/parity |
| **B · kế toán sửa — NGOÀI hợp đồng P&L** | **Mã đối tác** *(ID Payee)* · **Hoá đơn** *(N chip bấm được → Drive; ⛔ không tải tệp vào FLS — `QĐ-ITL-67`)* | ✅ **sửa** · KHÔNG parity |
| **C · vùng PHÂN BỔ** 🔒 | **CFA1 · CFA2 · Method** | ⛔ **CHỈ ĐỌC — máy suy** *(`QĐ-ITL-64`/`65`)*. ⛔ Không có ô gõ, ⛔ không có nút override |

★ **Mỗi trường sửa (A và B) đều: máy gợi ý *(Classifying)* → ô người sửa *(Final)* → nhật ký.**

⛔⛔ **ĐÍNH CHÍNH v2.2 — câu v1.4 dưới đây SAI, giữ lại làm biên bản:** ~~*ALLOCATE (CFA1/2/Method) máy suy làm gợi ý mặc định; kế toán override thì máy chạy lại không đè, và override khác gợi ý ⇒ KÊU*~~. Owner chốt kế toán **⛔ KHÔNG sửa vùng này** *(`QĐ-ITL-64`)*, và ba ô ấy là **CÔNG THỨC** nên suy lại được 100% *(`QĐ-ITL-65`, đã bỏ khỏi khuôn kho — migration `0012`)*. ⇒ Vùng `C` **⛔ không có ô gõ nào**, và cũng ⛔ **không có "override"** — một cái nút override ở đây sẽ tạo **cột thứ hai cạnh một con số suy được**, tức hai bản sự thật.

⭐ **Vùng `C` hiển thị thế nào** *(đã có dữ liệu thật từ `QĐ-ITL-70`: 73 mã `hd` trong `fls_mapping_master`)*:

| Máy suy ra | Màn hình hiện | Vì sao |
|---|---|---|
| tra được, có cờ phân bổ | `Need to Allocate to CFA2` | ⭐ **2.922 dòng** đo được |
| tra được, ⛔ không cờ | rơi về `CDT1` *(= `CFA1`)* | đúng công thức `AV` |
| `hd` ⛔ không tra được | **`#N/A`** ở **cả hai** ô | ⛔ **không bịa**, ⛔ không để trống trông như *"chưa ai điền"*. Đo: **6.691 dòng**, và **TẤT CẢ** vì `hd` rỗng ⇒ việc của **hàng chờ**, ⛔ không của danh mục |
| ô `Method` của `Mapping Master` **rỗng** | **`0`** *(⛔ không phải `No need`)* | ⚠ **bẫy `VLOOKUP` của Sheets**, ⛔ không phải lỗi FLS. Đo: **52/73 mã** · **547 dòng**. Màn hình phải hiện **đúng `0`** để khớp sổ — ⛔ đừng "chữa cho đẹp" |

⭐ **Hoá đơn ⛔ KHÔNG phải một ô text** *(`QĐ-ITL-67`, đo trên nguồn sống)*: **1.400/1.422 dòng (98%)** đã là **đường dẫn Drive**, và **422 ô chứa NHIỀU đường dẫn** *(nhiều nhất **10 link trong MỘT ô**, phân cách bằng dấu phẩy)* ⇒ quan hệ thật là **1 dòng sổ ↔ N tệp**. Màn hình vẽ **N chip bấm được**, ⛔ **không** một chuỗi dài cắt cụt. ⚠ Hai chi tiết: **22 dòng** chỉ có **tên tệp trơ** *(cần người bổ sung link — máy ⛔ không đoán được tệp nào)* và **33 link trỏ tới một Google **Sheets**** *(⛔ không phải tệp hoá đơn)*.

★ **Vì sao đủ nhóm 1–3 mới adjust được A/B:** để điền `HDCode`/`CDT1` cho dòng `UNMAPPED`, kế toán phải **truy chuỗi lệnh** *(nhóm 2 — dòng này thuộc lệnh PM nào?)*, **xem chứng từ hoá đơn** *(nhóm B — đính kèm)*, và **đối chiếu diễn giải** *(nhóm 1)*. Bỏ bối cảnh thì ô sửa chỉ là một dropdown đoán mò.

### Ba quy tắc hiển thị bắt buộc

1. ⭐ Mỗi trường Final hiện **nguồn gợi ý** ngay cạnh ô sửa: `Need to manual input` *(nền vàng)* nếu Classifying rỗng, hoặc giá trị nguồn nếu có. Người quyết dựa trên gợi ý đó, không mò.
2. ⭐ **Gõ khác nguồn** *(`US-025`)* → modal *"nguồn đang có X"* + [Sửa ở PM] / [Ghi đè kèm lý do]; ghi đè **bắt buộc** lý do → `409`.
3. **Số chưa chốt** *(`flash`)* in nghiêng/mờ.

### Nhật ký trong panel
7 trường `AUD-1` ngay dưới, cập nhật mỗi lần sửa *(`US-030`)*.

---

## §3c · `SCR-F02` — **CÁI ĐÃ DỰNG THẬT** *(03–04/09 · `QĐ-ITL-82..87`)*

> ⚠ Mục này ta **hành vi đang chạy**, đo được trên máy. Nó **hẹp lại** vài câu
> của §3 *(viết 25/08, trước khi màn được dựng)*; câu cũ ⛔ **không bị xoá**.

### ①  Hai chế độ, có công tắc — `Quét` ↔ `Gõ`

| | `Quét` *(mặc định)* | `Gõ` |
|---|---|---|
| Số cột lưới | **10** — `itl_id · ngày · diễn giải · Nợ · Có · tài khoản · LE · HDCode · CDT1 · trạng thái` | **52** *(= độ dài `BANG_COT`)* |
| Sửa ở đâu | **chỉ trong panel** | gõ thẳng trên ô, 8 hành vi §1 |

⭐ **Vì sao `CDT1` phải có trên lưới Quét:** nó là một trong **5 trường engine
P&L đọc**, và đo trên kho *(10.030 dòng)* thì **6.694 dòng — hai phần ba sổ —
⛔ chưa có `cdt1`**, gần như **y hệt `hd`** *(6.691, lệch **3 dòng**)*. ⇒ Bày
`hd` mà giấu `cdt1` là một lựa chọn **tuỳ tiện**.
⛔ *(Bản `QĐ-ITL-84` từng biện minh bằng con số "1.210 ô, gấp bốn lần cột kế
tiếp" — **con số ấy SAI**, đã lật bởi `QĐ-ITL-85`.)*

### ②  Bố cục: master–detail, panel là **cột bên phải**

- `.f02-wrap.split` = `minmax(0,1fr)` + `clamp(430px, 30vw, 680px)`
- ⭐ **`430px` là SÀN, ⛔ không phải số cố định** — nó là con số §2 khai *cho
  `B7 · UAT` trả lời có đủ hay không* *(`GAP-SCR-03`)*; thay nó bằng một số mới
  là **vứt mất câu hỏi ấy**, và vứt **im lặng** vì màn sẽ trông đẹp hơn.
- Trang nới theo màn *(≥1600px dùng tới 1880px)*. Đo thật: màn owner **1894px**
  mà trang khoá **1440px** ⇒ **~450px bỏ phí**.
- ⛔ **KHÔNG dùng hộp che kín màn.** Bản đầu làm vậy: chạy đúng nhưng **phá
  đúng cái câu trong ngoặc của wireframe** — *"dòng vẫn trong tầm mắt"*.

### ③  **Bảy ô sửa được — BỐN kiểu ô, theo bốn quyết định khác nhau**

| Ô | Kiểu điều khiển | Nguồn danh sách | Cửa có ép? |
|---|---|---|:--:|
| `hd` Budget Code | gõ **có gợi ý** *(`datalist`)* | **`fls_mapping_master` — 73 mã, BẢN KHAI THẬT** *(0 mã trong sổ nằm ngoài nó)* | ✅ `FLS-UNKNOWN-CODE` |
| `pay_type` Loại giao dịch | **ô CHỌN** *(`select`, đóng)* | suy từ **4** giá trị đang dùng | ⛔ |
| `cdt1` Chủ dự toán | gõ **có gợi ý** *(mở)* | suy từ **9** giá trị đang dùng | ⛔ |
| `id_payee` Mã đối tác | gõ **có gợi ý** *(mở)* | suy từ **27** giá trị · ⚠ **3 nhóm chỉ khác hoa-thường** | ⛔ |
| `svc_start` · `svc_end` | **ô chọn THÁNG** | khuôn **`YYYYMM`** | ✅ `FLS-BAD-FORMAT` |
| `invoice` Hoá đơn | gõ tay | — | ⛔ |

⛔ **Bốn kiểu ấy ⛔ KHÔNG được trông giống nhau:** một ô **đóng** mà trông y hệt
một ô **mở** thì kế toán sẽ gõ vào rồi **mới biết** nó ⛔ không nhận.

⚠⚠ **Ba danh sách *suy* ⛔ KHÔNG phải danh mục** — màn **phải gọi đúng tên**:
*"suy từ N giá trị đang dùng trong sổ — ⛔ không phải danh mục"*. Hai chỗ hỏng
đã đo được: nó ⛔ **không đưa ra được giá trị chưa ai dùng** *(⇒ `cdt1` và
`id_payee` **phải mở**; đóng lại thì một đơn vị mới lập sẽ ⛔ không nhập
được)*, và nó **đưa luôn cả lỗi gõ của người trước**. ⇒ Màn **đánh dấu** nhóm
trùng hoa-thường; ⛔ máy **không gộp và không bỏ bớt một bên** *(chọn cách viết
nào đúng là việc của **người**)*.

⛔⛔ **Bẫy im lặng nhất của một ô CHỌN:** nếu giá trị đang có ⛔ không nằm trong
danh sách thì `<select>` **nhảy về mục đầu tiên**, rồi lần lưu đầu tiên **ghi
cái mục ấy vào sổ** — một dòng **bị đổi giá trị mà ⛔ không ai bấm gì cả**, và
sổ chỉ-thêm nên chữa được thì phải **đảo**. ⇒ Giá trị lạ **giữ lại làm một
mục**, đánh dấu *⚠ ngoài danh sách*, nói ra bên dưới.

⭐ Danh sách lên màn bằng khuôn của `cot.js` *(bơm lúc khởi động)*, ⛔ **không**
dựng cửa `GET /catalog` — cửa ấy là `GAP-SPEC-01`, **⛔ chưa ai đặc tả**. ⚠ Giá
phải trả: **ảnh chụp lúc khởi động** ⇒ màn nói ra cả **số mã** lẫn **lúc chụp**.

### ④  Lưu — ô panel ghi khi **RỜI Ô / Enter**, ⛔ không theo từng phím

⛔⛔ Bản đầu ghi theo **từng phím**. Gõ `SHQ2 | Headquarters2` là **20 ký tự** và
người ta **ngừng giữa chừng để tra bảng mã** ⇒ ngừng 2,5s là **ghi nửa chữ vào
sổ**, mà sổ **chỉ-thêm** nên rác **ở lại vĩnh viễn** và nhật ký `AUD-1` — thứ
đưa ra khi có người hỏi *"ai đổi số này"* — **mất giá trị**.

⭐ Kèm: panel ⛔ **không tự dựng lại khi còn người đang gõ trong nó** — nhưng
lần vẽ lại ấy bị **HOÃN**, ⛔ **không bị QUÊN**.
⭐ Điền **lý do** xong thì **hẹn lại lô đang treo** *(chỉ khi còn ô chờ)*.

### ⑤  Số tiền trên đầu panel — `Nợ` = **vào (+)** · `Có` = **ra (−)**

Một vế **có tiền** khi nó ⛔ không rỗng **VÀ khác 0**. Xem `BA-10 · DT-I10`.
⛔ Phép đo cũ *"ô nào không rỗng"* làm **3.630/10.030 dòng (36%)** hiện sai, và
nó ⛔ **không nhìn thấy được** *(5.105 dòng còn lại có ô **trống thật** nên hiện
đúng)*.

### ⑥  Một luật chữ: **hình thức đi theo ô đó LÀ GÌ**, ⛔ không theo giá trị dài hay ngắn

Nhãn **một kiểu duy nhất** *(bỏ chữ HOA — tiếng Việt viết hoa toàn bộ có dấu
thì các dấu đội vào nhau)*. Giá trị **chữ máy là mặc định** *(đây là cuốn sổ,
gần hết là mã; mã đặt chữ máy thì ký tự thẳng cột nên **một ký tự bị đổi nhìn
ra được**)*; **văn xuôi là ngoại lệ và ĐƯỢC KHAI** *(`VAN_XUOI`)*.
⚠ `kieu` ⛔ **không dùng được** cho việc này: **38/52** cột mang kiểu `"chu"`.

### ⑦  ~~Dải phán quyết~~ → **MỘT bảng `KIỂM TRA` + MỘT dòng trạng thái**

> ⛔⛔ **Mục này bị thay 04/09 (`QĐ-ITL-88`). Giữ lại làm BIÊN BẢN** — dải chip
> là thiết kế của 03/09 và nó **đã chạy thật một ngày**. ⛔ Không xoá.

**Thiết kế cũ *(03/09)*:** một hàng chip ngoài vùng cuộn, mỗi chip **nhảy** tới
đúng nhóm. `⛔ chưa gán` và `⚠ máy đoán` là hai chip riêng; dòng sạch thì dải
nói thẳng *"✓ không còn việc"*.

**Vì sao thay.** Dải ấy ⛔ không sai — **mỗi chip là một phép đếm thật**. Nhưng
nó bày **tám** tín hiệu cùng một lúc và **cùng một trọng lượng**, nên mắt ⛔
không biết nhìn đâu trước. Cộng với **111** dấu `⛔` quanh đó thì thành đúng cái
kế toán gọi là *"quá nhiều note, ký hiệu → khó nhìn"* *(04/09)*.

**Cái đã dựng thay:**

| | Là gì | Luật |
|---|---|---|
| **Bảng `KIỂM TRA`** | nền `--crit`, đầu panel | ⭐ **TỐI ĐA MỘT bảng/panel.** Nhiều việc cùng lúc thì **gộp vào một** bảng, mỗi việc một dòng |
| **Dòng trạng thái** | ngay dưới | xong → nền `--good` *"✓ Đã phân loại · N lệnh chi đã ghép"*; còn việc → nền nhạt *"Chưa phân loại — còn N ô trống, M ô máy gợi ý… **Việc đang chờ, không phải sự cố**"* |

⭐⭐ **Phép đếm GIỮ NGUYÊN.** `chưa gán` và `máy gợi ý` vẫn là **hai con số
tách**: gộp lại thì kế toán đối soát với một con số **máy đoán** mà tưởng là số
**đã chốt**.

⛔⛔ **Và bảng báo chỉ được dùng cho BA việc** *(xem `BA-10 · DT-I11`)*. Lý do là
một con số: **7.682 / 10.030 dòng (76,6%)** đang ở trạng thái `chưa phân loại`.
Nếu trạng thái ấy kéo theo bảng báo thì màn hình **lúc nào cũng đang kêu**, và
khi có chuyện **thật** thì ⛔ **không còn nấc nào cao hơn để dùng**.
⇒ `chưa phân loại` lấy **nền nhạt chữ mờ**, ⛔ không còn nền vàng chữ nghiêng.

⚠ **Cái MẤT khi bỏ dải chip: phép NHẢY xuống nhóm.** Bù bằng việc **xếp lại thứ
hạng** *(xem `⑨`)* — khối cần đến nhất nay ở ngay dưới dòng trạng thái. ⛔ Nhưng
đây là một mất **thật**. Và với dòng **chưa** phân loại thì dòng trạng thái ⛔
**không** còn nhắc *"chưa ghép lệnh chi"* — tin ấy chỉ còn ở khối `③`.

### ⑧  Thứ tự các khối — xếp lại theo **THỨ HẠNG** *(04/09)*

⛔⛔ **Trước đó bảy khối nặng ngang nhau**, và khối **7 ô gõ được** nằm **thứ
ba** — sau hai khối **chỉ đọc**, trong đó có khối *"đủ 38 cột"* với **95% ô
rỗng**. Kế toán mở panel ra là để **gõ 7 ô**; sáu khối kia là để **tra khi
cần**.

```
vùng ⛔ KHÔNG CUỘN  ┌ số tiền 24px · đơn vị · chip hướng tiền · ngày
  (digest)         │ Số chứng từ
                   │ Diễn giải
                   │ Tài khoản · LE · Pháp nhân thanh toán
                   ├ bảng KIỂM TRA   (nếu có — tối đa 1)
                   └ dòng trạng thái
vùng cuộn          ① PHÂN LOẠI · 7 ô gõ được   ← ⭐ lý do panel tồn tại
                   ② PHÂN BỔ  (máy suy)
                   ③ Mối nối lệnh chi
                   ④ Hoá đơn
                   ⑤ Bút toán tay
                   ⑥ Sổ gốc · 38 cột  (gấp lại, có ĐẾM)
                   ⑦ Nhật ký · AUD-1
```

⭐⭐ **Khối `① Chứng từ` cũ ⛔ KHÔNG bị xoá — nó HOÀ TAN vào digest.** Cả **chín**
ô của nó *(ngày · số chứng từ · diễn giải · đơn vị tiền · PS Nợ · PS Có · tài
khoản · LE · pháp nhân thanh toán)* nay nằm ở vùng **⛔ không cuộn** ⇒ cuộn xuống
gõ ô thứ bảy **vẫn thấy** ngày/tiền/tài khoản để đối chiếu. **Kế toán xin đúng
điều này.** Giữ lại khối cũ là hiện **hai lần cùng một dữ liệu**, và kế toán sẽ
hỏi *"cái nào đúng"* — một câu hỏi màn hình tự tạo ra.

⚠ `Đơn vị tiền tệ` ⛔ **không còn nhãn**: nó nằm **ngay cạnh số tiền**
*(`−1.500.000 VND`)* nên một nhãn là chữ thừa.

### ⑨  Khối **PHÂN BỔ** — ba trạng thái, **BA hình**

⛔⛔ **Lỗi thật trước 04/09:** `#N/A` vẽ bằng màu **cảnh báo** ⇒ trông như một
**lỗi**, mà nó là một **câu trả lời**; ô **rỗng** vẽ bằng `—` xám ⇒ trông y hệt
*"⛔ chưa ai gán"*. Hai thứ khác hẳn bị vẽ gần giống nhau, và **cả hai bị vẽ sai
loại**.

| Trạng thái | Nghĩa | Hình |
|---|---|---|
| có giá trị | máy đã suy ra | chữ máy |
| **`#N/A`** | máy **đã tra và ⛔ không ra** *(câu trả lời của MÁY)* | **viền đứt** + *"máy tra không ra — đây là câu trả lời"* |
| **rỗng** | máy **⛔ chưa ghi gì** vào đây | *"rỗng — máy chưa ghi gì"*, chữ nghiêng mờ |

⭐ Và trên **lưới**, ô `#N/A` nay dùng lớp riêng *(`td.na`)*, ⛔ **không** dùng
lại lớp của `chưa gán` — trước đó chúng dùng chung một lớp nên trông y hệt nhau.

⭐ Dấu `🔒` *(đã bị cắt khỏi văn bản)* thay bằng một **thẻ chữ** màu `--info` ở
tiêu đề: *"máy suy — không gõ được"*. ⛔ Màu ⛔ không bao giờ là thứ **DUY NHẤT**
chở một nghĩa ⇒ thẻ này **luôn có chữ**.

### ⑩  Luật ký hiệu — nay có **MÁY canh**

| Dấu | Được dùng ở đâu | Tối đa |
|---|---|---|
| `⛔` `⚠` `⭐` `🔒` | ⛔ **KHÔNG** — cắt hẳn khỏi văn bản hiện ra màn hình | **0** |
| `✓` | việc **đã xong** | 1 |

⭐ Cưỡng chế: `tests/web/test_luat_ky_hieu_man_hinh.py`. **Chú thích trong mã ⛔
KHÔNG bị cấm** — ký hiệu ở đó là cho lập trình viên đọc, nó ⛔ không làm rối mắt
kế toán.

⛔⛔ **Cắt một lần thì nó sẽ BÒ LẠI** — người sau *(kể cả tác giả bản này)* sẽ
viết `⛔ không…` vì cả bộ tài liệu quanh đây đều viết thế. Một luật ⛔ không có
máy canh là một luật **sẽ trôi**. Đó là lý do cổng tồn tại, ⛔ không phải vì
phép cắt cần một phép thử.

### ⑧  Việc còn mở của màn này

| Mã | Việc |
|---|---|
| `GAP-SCR-03` | **`B7 · UAT`** — cảm giác khi gõ · thời gian vẽ · `346px` cột khoá có đủ · `430px` panel có đủ. ⛔ **Máy ⛔ không đóng được** |
| `GAP-SPEC-01` | `GET /catalog` ⛔ chưa ai đặc tả — vẫn **chặn `B6`** |
| `GAP-SCR-09` | Cửa ghi ⛔ không thấy **hai người sửa một ô** |
| ⭐ mới | ⛔ **Không có nút *Xong*** ở `F02` *(chỉ ở `F01`)* ⇒ vòng việc **đứt hai đầu** |
| ⭐ mới | Ô lọc chỉ soi **200 dòng đã nạp** ⇒ *"không tìm thấy"* và *"chưa tải tới"* **trông y hệt nhau** |
| ⭐ mới | ⛔ **Không xếp được thứ tự** — §1 hành vi 5 đòi *"lọc/**sắp xếp**"* |
| ✅ **đóng 04/09** | ~~`LE` (P) vs `Pháp nhân thanh toán` (L) lệch thì phải ĐỎ *(`US-032`)* — màn ⛔ chưa so~~ ⇒ **đã so**, nhưng luật phải **THU HẸP**: `le != le_payer` báo trên **1.304 dòng (13%)**; chỉ báo khi **cả hai** thuộc **từ vựng CHUNG** thì còn **79 dòng (0,8%)**. Xem `QĐ-ITL-89` · `BA-10 · DT-I12` |
| ⭐ mới | **Khoá kỹ thuật dưới mỗi nhãn** *(`hd`, `pay_type`…)* — bản thiết kế đề nghị, ⛔ **CHƯA dựng**: đó là tên cột **trong máy**, ⛔ không phải tên trên **sheet** kế toán dùng *(`Budget Code · Final`)* ⇒ **bảy mẩu chữ nữa** cho một người ⛔ không dùng đến, đúng lớp lỗi `DOC_NO`. **Chờ owner** |
| ⭐ mới | **Phép NHẢY xuống nhóm** mất theo dải chip *(xem `⑦`)* |
| ⭐ mới | Sổ cũ **chia việc theo CỘT** *(`PIC: LAN` / `PIC: THƯƠNG`)*; màn ⛔ chưa có |


---

## §3-cũ · đặc tả field-level *(giữ để tham chiếu)*


**Bố cục lưới** *(đọc theo tên, thứ tự trình bày ≠ vị trí `_COLS`)*:

| Cột hiển thị | Nguồn | Sửa? | Ghi chú |
|---|---|:--:|---|
| `itl_id` | danh tính | ⛔ | đóng băng, mã cho người đọc |
| ngày · số CT · diễn giải · tiền · tài khoản · LE | BASE + `le` | ⛔ | chỉ đọc — engine đọc `le`=`P` |
| **HDCode · Loại GD · CDT1 · bắt đầu DV · kết thúc DV** | 5 trường Final | ✅ | ⭐ **vùng người gõ** |
| `trạng thái` | `work_status` | ⛔ | `ok` / **`UNMAPPED`** / `rejected` |

**Ba quy tắc hiển thị bắt buộc:**

1. ⭐ **`UNMAPPED` phải trông KHÁC `ok`** — ô để trống, nền nhạt, chữ *"chưa gán"*; ⛔ **cấm** hiện một giá trị mặc định nghe hợp lý *(`INV-I16`)*. Đây là điểm sửa lỗi gốc của sổ AS-IS.
2. ⭐ **Khi gõ khác nguồn** *(`US-025`)*: ô hiện cảnh báo *"nguồn đang có: X"* + hai nút **[Sửa ở PM]** / **[Ghi đè kèm lý do]**. Ghi đè **bắt buộc** ô lý do; vào nhật ký. `POST /adjust` trả `409` → UI hiện cảnh báo này.
3. **Số chưa chốt** *(`data_status=flash`)* in **nghiêng/mờ**, khác số `reconciled`/`signed`.

---

## §4 · `SCR-F01` Hàng chờ — chỗ `US-045` sống hay chết

- Chỉ chứa **phần chưa biết** *(`UNMAPPED` + chưa ghép)*, **xếp theo tiền giảm**, in **tuổi việc** *(thanh đổi đỏ quá 3 ngày)*.
- **Năm hành động mỗi dòng** *(v2.2 — thêm hai)*: **LÝ DO** *(gõ → nhật ký + bộ đếm `US-045`)* · **Hoãn** *(`US-040`, lần 3 đổi màu, ⛔ không leo cấp)* · ⭐ **Ghép** *(`OP-02` — `QĐ-ITL-48`)* · ⭐⭐ **Bỏ ghép** *(`QĐ-ITL-69`)* · ⭐⭐ **Xong** *(`QĐ-ITL-71`)*. ⛔ **Không có nút xoá trắng.**
- ⭐⭐ **`Xong` là cách DUY NHẤT một dòng rời hàng chờ** *(`QĐ-ITL-71` — owner chốt: **người bấm**, ⛔ không phải máy tự nhả khi thấy đủ 5 trường; căn cứ nghiệp vụ: máy tự nhả thì kế toán **mất chỗ đánh dấu việc đang làm dở**)*. ⛔ **Không đòi lý do** *(`QĐ-ITL-72`)* — kể cả khi dòng còn thiếu trường hay kỳ đã chốt: một ô lý do **bắt buộc** thì nó thành một ô **rác**. Bấm nhầm ⇒ **Mở lại** *(nút này thì **đòi** lý do — kéo lại một dòng người khác đã kết luận là xong là **lật kết luận của người khác**)*.
  - ⚠ Màn hình **PHẢI hiện** khi bấm xong mà dòng **còn thiếu trường**: một nhãn *"xong · còn thiếu `hd`, `cdt1`"* — máy trả sẵn `thieu_truong`. ⛔ Không chặn, nhưng ⛔ **không im lặng**.
  - ⚠ **Kỳ đã chốt VẪN bấm xong được** — cố ý **khác** mọi cửa ghi khác *(`INV-I13` chặn kỳ chốt)*: kỳ chốt thì kế toán ⛔ không sửa được gì, nếu cũng ⛔ không đánh dấu xong được thì những dòng ấy nằm trong hàng chờ **vĩnh viễn** ⇒ hàng chờ **tự biến thành rác**, và một hàng chờ đầy rác thì ⛔ không ai đọc nữa.
- ⭐⭐ **`Bỏ ghép` bỏ CẢ CHÙM mối nối của dòng, ⛔ không bỏ lẻ** *(`QĐ-ITL-69`)* — bỏ lẻ làm `Σ mối nối ≠ tiền bank`, tức **tạo ra đúng cái trạng thái sai** mà cổng dựng ra để bắt. Màn hình phải nói câu ấy trong hộp xác nhận, ⛔ không để kế toán tưởng mình mất dữ liệu: **sổ giữ cả lịch sử**, bỏ chỉ là **thêm một dòng**. Máy trả `but_toan_dao` *(cái nó đã rút lại)* + ⭐ **`bo_qua`** *(cái nó ⛔ KHÔNG rút — vì **người** đã gõ tay lên ô ấy)*; **cả hai phải hiện**.
- ⭐ **Ghép lệnh** *(nút Ghép → drawer)*: máy **gợi ý phiếu `fps_pm_slip`** ứng viên *(xếp theo reference/tiền/ngày/payee)* → kế toán **chọn phiếu** → máy xuống `fps_pm_line` + **chia tiền theo `amount`**; **`Σ line = tiền bank` mới cho ghép**, lệch ⇒ giữ `UNMAPPED` *(không chia bừa, `INV-I16`)*. Gán `line_id` + reference, vào nhật ký. Bám `CR#1`.
- Chân màn: *"cột lý do đã được gõ: N lần"* — thước của `US-045`: **4 tuần không ai gõ = cổng đã chết**.
- ⛔ ~~Nhãn nhóm theo **6 loại "không cần lệnh"**~~ **BỎ 27/08** *(`QĐ-ITL-58`)* — `QĐ-ITL-56`: **không có quy định nào** nói khoản nào cần lệnh chi, nên máy dán nhãn đó là **máy tự đặt ra quy định** *(`INV-I16`)*.
- ⭐⭐ **Thay bằng: xếp theo TIỀN** — `GET /api/fls/v1/queue?curr=&den_pct=90` cho mỗi dòng một **hạng** và một **% tiền luỹ kế**, để màn hình nói được *"xem tới đây là phủ 90% tiền"*. Nó ⛔ **không** nói dòng nào *"không cần lệnh"*, nó chỉ nói **xem cái này trước**. Kèm `GET /queue/summary` cho số dòng + Σ tiền **theo từng tiền tệ** *(⛔ không có dòng "tổng")*.
- ⚠ **Hình thức đã đổi 27/08** *(`CR#4`)*: ban đầu là khung xem `fls_queue_xep_tien` *(migration `0008`)*, **đã bỏ** ở `0009` — khung xem SQL ⛔ không nhận tham số nên không mang được **phạm vi**, và **lọc ở đầu ra ⛔ không sửa được một thứ tự đã xếp sai**. Màn hình đọc **cửa API**, ⛔ không đọc thẳng kho.
- ⛔⛔ **Màn hình PHẢI hiện tiền tệ và xếp trong TỪNG tiền tệ.** Hàng chờ có **USD 4.492 dòng** *(58%)* vs **VND 2.987**; gộp lại xếp theo con số thì **toàn bộ dòng USD bị dìm xuống dưới** — một khoản 300.000 USD xếp sau một khoản 400.000 đồng. Đo được: phủ 90% tiền cần **VND 310 · USD 444 · SGD 13 · HKD 32 ⇒ 799 dòng = 10,4%**.
- Còn lại: **`UNMAPPED`** + **thiếu mã lệnh**.

---

## §5 · Nguyên tắc UI xuyên suốt

| ID | Nguyên tắc |
|---|---|
| UI-F1 | Mọi số kèm nhãn trạng thái `flash / reconciled / signed` |
| UI-F2 | Màn chỉ hiện việc cần làm — hàng chờ rỗng = khỏe |
| UI-F3 | Tiền `tabular-nums`, tiền tệ gốc; quy đổi ở cột phụ/hover |
| UI-F4 | Mọi số drill được về dòng gốc ≤ 3 click *(lineage sẵn trong `fls_itl`)* |
| UI-F5 | ⛔ Máy **không tự điền thay người** — trống là trống *(`INV-I16`)* |
| UI-F6 | ⛔ CFO·COO **chỉ đọc** — `SCR-F05` không có nút hành động nào *(`QĐ-ITL-27`)* |

---

## §6 · Việc mở

| ID | Việc |
|---|---|
| `GAP-SCR-01` ✅ **ĐÓNG 28/08** | ~~chọn thư viện lưới~~ ⇒ **bảng HTML trần, ⛔ không thư viện** *(`QĐ-ITL-66`)*. Mũi thử chạy **748 × 52 = 38.896 ô** với **cả 8 hành vi §1**; bài toán thật ~39.000 ô nên **ảo hoá có thể không cần**. ⇒ ⛔ Không thêm một phụ thuộc nào cho màn nặng nhất |
| `GAP-SCR-03` ⚠ **HẠ, ⛔ không còn chặn** | ~~chạy thử với LAN/THƯƠNG trước khi build~~. Phần *"đủ trường"* **đóng bằng chính người dùng** *(kế toán **2/2** xác nhận — `QĐ-ITL-68`)*. Ba thứ còn lại — **cảm giác khi gõ · thời gian vẽ trên máy kế toán · 346px cột khoá có đủ** — chuyển vào **UAT tuần đầu**, vì **đo cảm giác trên một tệp THÔ thì ra cảm giác của tệp thô** |
| **`GAP-SCR-07`** ⭐ **MỚI 28/08** *(đổi mã — xem ⚠ dưới bảng)* | Đặc tả **cơ chế lưu theo lô** cho 3 ca lỗi: gõ tiếp khi lô đang bay · mạng đứt giữa chừng · hai người sửa một ô. ⚠ **Ràng buộc đã đo:** cửa ghi hiện **một bút toán = một giao dịch**, nên *"lưu theo lô"* là việc của **màn hình**, ⛔ không của kho. **Việc thật của `P6`**, ⛔ không phải câu hỏi |
| `GAP-SCR-05` | Nút **[Sửa ở PM]** dẫn đi đâu — FLS ⛔ không sửa `fps_*` được; là deep-link sang hệ PM hay chỉ chỉ dẫn |
| `GAP-SCR-02` | Wireframe field-level `SCR-F02`/`SCR-F01` — JIT khi vào `P6` |
| **`GAP-SCR-08`** ⭐ **MỚI 28/08** | **22 dòng hoá đơn chỉ có TÊN TỆP trơ** *(⛔ không link)* — máy ⛔ không đoán được tệp nào. Cần **người bổ sung link**, và màn hình cần một trạng thái riêng cho ca này *(⛔ không vẽ chip chết)*. Kèm **33 link trỏ tới một Google Sheets** ⛔ không phải tệp hoá đơn |

⚠⚠ **ĐỔI MÃ, và ghi ra vì sao:** việc *"lưu theo lô"* trước đây mang mã `GAP-SCR-04` — **nhưng `GAP-SCR-04` đã bị dùng cho một việc KHÁC** ở `06_DASHBOARD` *(cột hoá đơn, đã đóng 28/08 bằng `QĐ-ITL-67`)*. **Một mã hai nghĩa** thì mọi câu *"`GAP-SCR-04` đã đóng chưa"* đều có hai câu trả lời đúng — nên việc còn mở được **đổi sang `GAP-SCR-07`**, và mã cũ ⛔ không tái sử dụng. *(⛔ `GAP-SCR-06` cũng ⛔ không dùng lại: nó đã thuộc `Artifacts/Ra-soat-doc-lap-Schema-vs-Wireframe` §`*_thyt`.)*

---

## §6b · Khảo sát thư viện lưới `SCR-F02` — quyết định `GAP-SCR-01` *(2026-08-24)*

> ⛔⛔ **ĐỌC KHỐI NÀY TRƯỚC KHI TIN BẢNG DƯỚI — ba con số của bài toán đã bị ĐO LẬT** *(`CR#7`, 2026-08-27, `tools/do_luoi_f02.py` trên kho thật)*:
>
> | | §6b viết *(ước lượng từ tài liệu AS-IS)* | **Đo trên kho thật** |
> |---|---|---|
> | Cột lưới | ~**64** | **52** *(38 canon + 14 hợp đồng)* |
> | Cột sửa được | **5** | **10** — `QĐ-owner-0824` đã mở 5 → 10 |
> | Dòng một lát | *"vài nghìn"* | **748** *(kỳ dày nhất; `F02` lọc theo kỳ, ⛔ không ai mở cả sổ 10.030 dòng)* |
>
> ⛔⛔ **ĐÍNH CHÍNH 2 (2026-08-28, `QĐ-ITL-64`): con số `10 cột sửa được` dưới đây nay là `7`** — owner trả lời kế toán ⛔ **không** sửa vùng phân bổ *("họ ko sửa")*, nên `cdt1_cfa1`/`cdt1_cfa2`/`alloc_method` là **🔒 chỉ-đọc, máy suy**. ⇒ `F02`: **55 cột · 7 gõ được · 48 chỉ-đọc**.
>
> ⛔⛔ **ĐÍNH CHÍNH 2026-08-28 (`CR#8`): con số `52` dưới đây là THIẾU — số đúng là `55`.** `BA-07` §3 cho người gõ **10 trường**, mà **5 trường nằm ngoài 14 cột hợp đồng**; ba trong số đó *(`cdt1_cfa1` · `cdt1_cfa2` · `alloc_method`)* ⛔ **không có ở đâu cả** ⇒ `F02` phải có thêm **3 cột thật**. Bài toán thật: **748 × 55 = 41.140 ô** *(vẫn ⛔ không phải ~192.000, nên kết luận *ảo hoá có thể không cần* ⛔ không đổi)*. Phát hiện vì **owner mở nguyên mẫu và báo thiếu 2 trường** — máy đo 11 phép thử thì ⛔ không thấy.
>
> ⇒ Bài toán thật là **~750 × 52 ≈ 39.000 ô**, ⛔ không phải *"3.000 × 64"*. **Ở quy mô đó, ảo hoá CÓ THỂ không cần** — mà **ảo hoá là lý do CHÍNH** để mục này chọn `react-datasheet-grid`. Nên **tiền đề của quyết định đã đổ**, và quyết định phải được **xem lại**, ⛔ không phải mặc định giữ.
>
> ⭐ **Ứng viên thứ tám xuất hiện, và nó rẻ nhất: một bảng HTML trần, KHÔNG thư viện.** Đã dựng nguyên mẫu chạy được trên dữ liệu thật *(`tools/mui_thu_luoi.py` — 748 dòng × 52 cột = 38.896 ô, một tệp **1.293 KB** tự chứa)*, và **cả 8 hành vi §1 đều có trong đó**, không thư viện nào. ⭐⭐ Chỗ mục này gọi là **yếu nhất** — *đông cứng N cột trái* — đã **bị bỏ** chứ không phải đo kỹ hơn: `left` của cột đông cứng ⛔ không còn là **ước lượng** bề rộng *(ước sai thì hai cột đè lên nhau)* mà là **tổng đúng theo định nghĩa** của 3 bề rộng đã **khai** *(0/76/176, tổng **346px**)*; có bài test cộng lại và so.
>
> ⛔ **Ba thứ nguyên mẫu ⛔ KHÔNG tự chứng minh được**, khai ra chứ không để người đọc tự suy: ⓐ **cảm giác** *"có thua Sheets ở đâu"* — cần LAN/THƯƠNG ngồi gõ thật; ⓑ **thời gian vẽ** của trình duyệt — máy dựng nó ⛔ không có trình duyệt; ⓒ **346px cột khoá có đủ** để không mất phương hướng — phải ngồi cuộn mới biết. ⇒ `GAP-SCR-03` **còn mở**, nhưng nay nó là **một buổi ngồi cùng kế toán**, ⛔ không còn là một dự án khảo sát.
>
> ⛔ **Bảng và phần *Quyết định* bên dưới GIỮ NGUYÊN** làm biên bản của ngày 24/08 — sửa chữ trong đó là **viết lại lịch sử**. Chúng vẫn đúng *cho bài toán mà chúng tưởng*.


Bài toán riêng của F02: lưới **~64 cột × vài nghìn dòng, chỉ 5 cột sửa được**, còn lại chỉ-đọc; phải **cảm giác như Sheets**; **ưu tiên license miễn phí** *(app nội bộ thương mại — bản trả phí là chi phí thật)*.

### 8 hành vi §1 × ứng viên

`✅` sẵn · `⚠` phải cấu hình / tự viết thêm · `❌` thiếu hoặc **chỉ có ở bản trả phí**

| Thư viện | Bàn phím | Dán vùng | Kéo xuống | Hoàn tác | Filter cột | Đông cứng | Số kế toán | Gom lô | License | Ảo hoá |
|---|---|---|---|---|---|---|---|---|---|---|
| **react-datasheet-grid** ⭐ | ✅ | ✅ | ⚠ | ⚠ | ❌ | ⚠ | ⚠ | ⚠ | **MIT** | ✅ |
| **AG Grid Community** | ✅ | ⚠¹ | ❌² | ❌² | ⚠ | ✅ | ⚠ | ⚠ | **MIT** | ✅ |
| AG Grid Enterprise | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | ⚠ | 💰 trả phí/dev | ✅ |
| Handsontable | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | 💰 **không OSS từ v8** | ✅ |
| Glide Data Grid | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ⚠ | ⚠ | MIT | ✅ canvas |
| TanStack Table | ❌ | ❌ | ❌ | ❌ | ⚠ | ⚠ | ❌ | ❌ | MIT | ⚠ tự ghép |
| Univer / Luckysheet | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠ | Apache/MIT³ | ✅ |

¹ AG Grid Community: **dán từ clipboard ngoài nhiều ô** là tính năng Enterprise *(copy thì có)*. ² **Kéo-xuống (fill handle) + Hoàn tác là Enterprise-only.** ³ Luckysheet **đã ngừng bảo trì** *(tác giả trỏ sang Univer)*; Univer nặng, vài module trả phí — quá tay cho sổ mostly-read-only.

⛔ **Bẫy license — không phải "có trên npm" là miễn phí:** Handsontable **không còn OSS từ v8**; ở AG Grid, đúng **4 cử chỉ Sheets** kế toán cần nhất *(dán vùng · kéo xuống · hoàn tác · filter giàu)* đều nằm sau tường phí Enterprise.

### Quyết định

★ **Chọn `react-datasheet-grid` (MIT)** — sinh ra đúng cho hình dạng này: React-native, ảo hoá, **cấu hình sửa-được/chỉ-đọc theo từng cột** khớp "5/64 cột sửa". Tự viết thêm ~5 mảnh gọn *(ước ~1–2 tuần-người)*: định dạng số kế toán *(~0,5 ngày, `Intl.NumberFormat` + `tabular-nums` + âm đỏ/ngoặc)* · gom-lô + dirty-set *(~1 ngày)* · kéo-xuống/Ctrl+D *(~1–2 ngày)* · hoàn tác/làm-lại chỉ trên 5 cột sửa *(~1–2 ngày)* · **filter view** *(~2–3 ngày — mảnh nặng nhất)*.

★ **Dự phòng `AG Grid Community` (MIT)** — ảo hoá + **đông cứng cột/hàng ở bản free** là điểm mạnh; đổi lại 4 cử chỉ Enterprise phải tự viết hoặc mua. Chọn nếu spike cho thấy **đông cứng cột** hoặc **hiệu năng ở số dòng thật** của `react-datasheet-grid` không đạt.

⛔ **Loại:** Handsontable *(license)* · Luckysheet *(ngừng bảo trì)* · Univer *(quá tay)* · TanStack thuần *(headless — tự dựng cả bề mặt sửa, ~vài tuần-người, không đáng)*.

⚠ **Điểm yếu nhất cần thử trước:** **đông cứng N cột trái** của `react-datasheet-grid`. ⇒ **`GAP-SCR-03` spike** phải đo: đông cứng cột + hiệu năng ~64 cột × số dòng thật, trên **2 ứng viên**, trước khi chốt build. *"Không có ứng viên nào đạt qua spike ⇒ lật lại `QĐ-ITL-38`"* vẫn là mệnh đề thoát.

---

## §7 · Hệ thị giác — **DÙNG LẠI `A-CCR`**, ⛔ không thiết kế lại từ đầu

> ✅ **ĐÃ VẼ 2026-08-28: `Artifacts/FLS-Design-P6.html`** — 4 màn + 3 drawer/hộp thoại + khối **4 trạng thái**, tự chứa *(⛔ không thư viện, ⛔ không cần mạng)*. Token màu **lấy nguyên** từ `A-CCR` Foundation Tokens. Đây là **cổng ra của bước 1** trong `DEV-12`, và nó là **spec hình dạng sống** — phần chữ dưới đây bám theo nó.

⛔⛔ **Đây là một quyết định phạm vi, ⛔ không phải một gợi ý.** Đội đã có một bộ
thiết kế **đã qua review sâu** cho `A-CCR` *(`A-CCR/02_BA/Artifacts/UIUX_HANDOFF.md`
+ `Phương pháp thiết kế UIUX/` — Foundation Tokens · Wireframes · Hi-fi Prototype ·
Handoff Spec)*. Vẽ lại một hệ thị giác thứ hai cho FLS là **tạo ra hai bản sự thật
về màu và khoảng cách**, đúng cái bệnh cả bộ tài liệu này chữa ở tầng số liệu.

| Lấy nguyên từ `A-CCR` | Vì sao dùng được ngay |
|---|---|
| **Token nền** *(màu · chữ · khoảng cách · bo · đổ bóng)* | ⛔ Không có gì thuộc riêng nghiệp vụ tiền |
| **Màu ngữ nghĩa** 🔴 critical · 🟠 warning · 🟢 good · 🔵 info | Tách khỏi màu tương tác — luật ấy đúng cho mọi màn |
| ⭐ **Chip niềm tin tái dùng** `flash / đối_soát / đã_ký` | FLS có **đúng ba cờ ấy** *(`UI-F1`)*; hover → tooltip *(as-of · owner)* |
| **Số kiểu kế toán** `tabular-nums` · tệ gốc · âm đỏ | Trùng khít `UI-F3` + hành vi §1-7 |
| **Global shell** *(top bar · control bar · badge as-of)* | Cùng hình dạng: chọn phạm vi rồi mới đọc số |
| **Drawer audit-grade** *(`Drawer-E`)* | `SCR-F02` cần đúng thứ đó cho drawer đối soát |
| **4 trạng thái mỗi component** *(mặc định · rỗng · đang tải · lỗi)* | Kỷ luật đã có sẵn — ⛔ không phát minh lại |

⛔ **Cái FLS phải tự làm** *(⛔ không có trong `A-CCR`)*:

| Thành phần | Vì sao `A-CCR` ⛔ không có |
|---|---|
| ⭐⭐ **Lưới sửa được** *(8 hành vi §1)* | `A-CCR` là màn **CHỈ ĐỌC** cho CFO/COO. Đây là phần **đắt nhất** của cả `P6`, và cơ chế đã có mũi thử chứng minh *(`QĐ-ITL-66`)* |
| **Drawer ghép lệnh** *(4 bậc ứng viên + Σ)* | Nghiệp vụ riêng của FLS *(`OP-02`)* |
| **Chip hoá đơn N tệp** | Quan hệ 1↔N, đo được **422 ô nhiều link** |
| **Nút Xong / Mở lại / Bỏ ghép** | Ba thao tác `28/08` |

⚠ **Khác biệt vai phải giữ:** `A-CCR` phục vụ **CFO·COO đọc**; FLS phục vụ **kế
toán LÀM** *(`QĐ-ITL-27`: ⛔ không có vai hậu kiểm)*. ⇒ Cùng token, nhưng **mật độ
dày hơn** *(nhiều dòng trên một màn)* và **⛔ không có màn tổng quan đẹp** — hàng
chờ rỗng là màn đẹp nhất *(`UI-F2`)*.

---

## §8 · Binding: màn · thành phần ↔ cửa API ↔ trường

> ⭐ Nối từng thành phần với **một cửa API có thật** *(`BA-07` v1.9)* và **trường
> trong phản hồi**. ⛔ Ô nào ⛔ không tìm được cửa thì đó là một **lỗ đặc tả**, ⛔ không
> phải *"dev tự lo"* — cột **Ghi chú** nói thẳng.

| Màn · thành phần | Cửa | Trường chính | Ghi chú |
|---|---|---|---|
| **F01** · lưới hàng chờ | `GET /queue?curr=&den_pct=` | `itl_id · doc_date · doc_no · curr · le · memo · tien · hang · luy_ke_pct` | ⛔ **Xếp trong TỪNG tiền tệ** — gộp lại là dìm toàn bộ dòng USD |
| F01 · chân màn *(số dòng · Σ tiền)* | `GET /queue/summary` | mảng **theo từng tiền tệ** | ⛔ **Không có dòng "tổng"** — cộng hai đơn vị tiền là một con số vô nghĩa |
| F01 · cột lý do + bộ đếm `US-045` | `POST /queue/{id}/reason` · `GET /queue/reason-weekly` | `reason` · `so_lan` theo tuần | **4 tuần không ai gõ = cổng đã chết** |
| F01 · nút Hoãn | `POST /queue/{id}/defer` | `until` · `so_lan_hoan` · `doi_mau` | lần 3 **đổi màu**, ⛔ không báo ai *(`QĐ-ITL-24`)* |
| F01 · nút **Ghép** → drawer | `GET /queue/{id}/pm-candidates` → `POST /queue/{id}/match` | ứng viên **4 bậc CÓ TÊN** *(`ma`/`tien`/`gan_tien`/`cung_tien_te`)* + `da_ghep` · thân `{pm_line_ids: [...]}` | ⛔ **Không** `{pm_id}` *(một PHIẾU)*: **526 phiếu mang 2–36 reference khác nhau** ⇒ ghép vào phiếu là **máy quyết thay người** *(`CR#6`)*. Kèm **TUỔI của ảnh chụp** |
| F01 · **Σ ở drawer ghép** | *(máy trả)* | `tien_bank · tong_lenh · dung_sai` | Lệch quá dung sai ⇒ **`422`, nút mờ**. Dung sai tay = **`min(1.000 đồng, 0,5%)`** *(`QĐ-ITL-63`)* — ⛔ khác dung sai máy |
| F01/F02 · nút ⭐ **Bỏ ghép** | `POST /queue/{id}/unmatch` | `da_bo[]` · `but_toan_dao[]` · ⭐ `bo_qua[]` | Hộp xác nhận phải nói **bỏ CẢ CHÙM** và **sổ giữ lịch sử**. ⭐ `bo_qua` = cái máy ⛔ KHÔNG rút *(người đã gõ tay)* — **phải hiện** |
| F01/F02 · nút ⭐ **Xong** | `POST /queue/{id}/done` | `da_co · thieu_truong[] · ky_da_chot · ghi_de_ket_luan_may` | ⛔ **Không đòi lý do** *(`QĐ-ITL-72`)*. Bấm lại ⇒ `da_co=true` kèm **ai đã bấm · lúc nào** ⇒ hiện *"đã xong bởi X"* thay vì báo lỗi |
| F01/F02 · nút ⭐ **Mở lại** | `POST /queue/{id}/reopen` | `mo_lai_cua · xong_boi · xong_luc` | `reason` **BẮT BUỘC** · `409` nếu dòng ⛔ chưa từng xong |
| **F02** · lưới sổ | `GET /ledger?...` | 38 cột canon *(tên tiếng Việt — lấy từ khuôn canon, **một nguồn duy nhất**)* + 14 cột hợp đồng | **52 cột** *(`QĐ-ITL-65`)*; `UNMAPPED` ⇒ `chưa gán` **nền vàng**, ⛔ không giá trị mặc định |
| F02 · drawer nhóm 1–3 *(bối cảnh)* | `GET /ledger/{id}` | giao dịch gốc · chuỗi lệnh · đối soát pháp nhân | ⛔ Chỉ đọc. Thiếu bối cảnh thì ô sửa chỉ là **một dropdown đoán mò** |
| F02 · **7 ô sửa** | `GET /ledger/{id}/before-edit` → `POST /ledger/{id}/adjust` | `gia_tri · value_source ∈ {nguon, may_goi_y, sua_tay, UNMAPPED}` | Gõ khác nguồn ⇒ **`409`** + modal *"nguồn đang có X"* *(`US-025`)*; ghi đè cần **xác nhận + lý do** |
| F02 · **hoàn tác** | `POST /ledger/{id}/reverse` *(theo `adj_id`)* | `dao_cua · value_before` | Đảo là **thêm một dòng**, ⛔ không xoá |
| F02 · ⭐ vùng **PHÂN BỔ** 🔒 | *(máy suy — `ledger/allocate.py` + `fls_mapping_master`)* | `cfa1 · cfa2 · method · can_phan_bo · khong_tra_duoc` | ⛔ **Không ô gõ**. `#N/A` khi ⛔ không tra được · **`0`** khi `Method` rỗng *(bẫy `VLOOKUP` — hiện **đúng `0`**)* |
| F02 · ⭐ **chip hoá đơn** | `GET /ledger/{id}` *(trường `invoice`)* | chuỗi **N đường dẫn** phân cách dấu phẩy | Vẽ **N chip bấm được**; **22 dòng tên trơ** ⇒ trạng thái riêng *(`GAP-SCR-08`)* |
| F02 · nhật ký trong drawer | `GET /ledger/{id}/journal` | **7 trường `AUD-1`** | Cập nhật mỗi lần sửa *(`US-030`)* |
| **F03** · 4 cổng + độ phủ | `GET /gates` | mỗi cổng: `ma · ten · dat ∈ {true,false,null} · da_do · ly_do` | ⭐⭐ **`dat=null` ⛔ KHÔNG được vẽ như ĐẠT** — nó là *"⛔ không đo được"*, và đó là **luật số 1** của dự án |
| F03 · nút *Xuất báo cáo tuần* | *(gấp trong F03)* | — | `SCR-F05` đã bỏ khỏi sidebar, ⛔ không mất thông tin |
| **F06** · danh mục · nguồn | `GET /catalog` ⚠ | nguồn · TK · ánh xạ + cảnh báo | ⚠ **Cửa này ⛔ CHƯA CÓ** — nằm trong **6 đường đọc còn thiếu** của `BA-07` §2 ⇒ **việc của `P6`**, ⛔ không phải giả định |
| F06 · ⭐ **danh mục phân bổ** | `GET /mapping-master` ⚠ | **73 mã `hd`** · `need_cfa2` · `method_cfa2` | ⚠ Cửa ⛔ chưa có. Dữ liệu **đã vào kho** *(`QĐ-ITL-70`)* |
| *(xuyên suốt)* · chip niềm tin | mọi phản hồi | `flash / đối_soát / đã_ký` | Component **tái dùng từ `A-CCR`** |

⛔⛔ **Bảng này khai ra ĐÚNG HAI cửa còn thiếu** *(`/catalog` · `/mapping-master`)*,
và đó là **việc thật của `P6`** — ⛔ không phải thứ để dev tự bịa một cửa mới.

---

## Changelog
- **v2.2** (2026-08-28, `QĐ-ITL-63..73`): ⭐⭐ **Đặc tả màn hình khớp lại 11 quyết định của ngày 28/08 — và sửa HAI chỗ TỰ MÂU THUẪN.** ⓵ §3 bảng *Nhóm B* còn ghi `CFA1`/`CFA2`/`Method` là **✅ sửa** trong khi khối ⛔ HẸP ngay **trên nó** nói `10→7` và ba ô ấy là 🔒 chỉ-đọc ⇒ tách thành **Nhóm C · vùng PHÂN BỔ 🔒**, và câu v1.4 giữ lại **gạch đi** làm biên bản. ⓶ ⚠⚠ **`GAP-SCR-04` mang HAI nghĩa**: ở `06_DASHBOARD` là **cột hoá đơn** *(đã đóng — `QĐ-ITL-67`)*, ở §6 là *"đặc tả lưu theo lô"* *(còn mở)* ⇒ **một mã hai nghĩa** thì câu *"đã đóng chưa"* có hai câu trả lời đúng; việc còn mở đổi sang **`GAP-SCR-07`**, mã cũ ⛔ không tái sử dụng. ⭐ §1b dòng 1 **đã bị phép đo lật** *(một `<table>` trần LÀM ĐƯỢC cả 8 hành vi trên 38.896 ô — `QĐ-ITL-66`)* ⇒ `GAP-SCR-01` **đóng**; câu cũ giữ lại **gạch đi**. ⭐ §4: **năm** hành động mỗi dòng *(+`Bỏ ghép` +`Xong`)*, và `Xong` là **cách duy nhất** một dòng rời hàng chờ. §2: bổ sung `/unmatch` · `/done` · `/reopen` vào hai màn. ⭐⭐ **Thêm §7 — hệ thị giác DÙNG LẠI `A-CCR`** *(token · màu ngữ nghĩa · chip niềm tin · shell · drawer · 4 trạng thái)*, ⛔ không thiết kế lại: vẽ hệ thứ hai là tạo **hai bản sự thật về màu và khoảng cách**. Kèm bảng **cái FLS phải tự làm** *(lưới sửa được · drawer ghép · chip hoá đơn N tệp · ba nút mới)*. ⭐⭐ **Thêm §8 — binding màn ↔ cửa API ↔ trường** *(field-level, theo khuôn `A-CCR` §10)*. Nó khai ra **đúng hai cửa còn thiếu**: `GET /catalog` và `GET /mapping-master` ⇒ **việc thật của `P6`**, ⛔ không phải thứ để dev bịa một cửa mới. ⚠ **Mở `GAP-SCR-08`**: **22 dòng** hoá đơn chỉ có **tên tệp trơ** — cần người bổ sung link, và màn hình cần một trạng thái riêng *(⛔ không vẽ chip chết)*.
- **v2.4** (2026-09-04, `QĐ-ITL-88·89`): ⭐⭐ **Code hoá bản thiết kế panel.** `⑦` **thay dải 8 chip** bằng *một* bảng `KIỂM TRA` + *một* dòng trạng thái *(bản cũ giữ làm **biên bản**, ⛔ không xoá)*; `⑧` **thứ tự khối xếp lại theo thứ hạng** — khối 7 ô gõ lên **đầu**, sổ gốc 38 cột xuống **cuối**, khối `① Chứng từ` **hoà tan vào digest** *(vùng ⛔ không cuộn)*; `⑨` khối **PHÂN BỔ ba trạng thái ba hình** *(`#N/A` ⛔ không còn dùng chung lớp với `chưa gán`)*; `⑩` **luật ký hiệu nay có MÁY canh** *(`⛔ ⚠ ⭐ 🔒` từ **235** xuống **0**)*. ⭐ Đóng dòng `US-032` ở `⑧` — nhưng luật phải **thu hẹp**, và con số là lý do: **13% → 0,8%**. ⛔ Ghi thẳng **một chỗ ⛔ KHÔNG làm theo bản vẽ** *(khoá kỹ thuật dưới nhãn)* và **một thứ MẤT** *(phép nhảy xuống nhóm)*.
- **v2.3** *(2026-09-04, `QĐ-ITL-83·86·87`)*: ⭐⭐ Thêm **§3c — `SCR-F02` CÁI ĐÃ DỰNG THẬT**: hai chế độ `Quét`(10 cột)/`Gõ`(52) · bố cục master–detail với **`430px` là SÀN** *(⛔ không phải số cố định — nó là con số đang chờ `B7·UAT` trả lời)* · **bảy ô sửa được, BỐN kiểu ô** theo bốn quyết định của owner · lưu khi **rời ô** *(⛔ không theo từng phím — ghi nửa chữ vào một cuốn sổ **chỉ-thêm** là rác **vĩnh viễn**)* · luật số tiền · một luật chữ · dải phán quyết. ⚠ **§3 cũ giữ nguyên**, ⛔ không xoá. ⭐ §3c ⑧ khai **năm việc mở MỚI** do kế toán chỉ ra *(⛔ không có nút **Xong** ở `F02` · lọc chỉ soi 200 dòng đã nạp · ⛔ không xếp được thứ tự · `LE` vs `Pháp nhân thanh toán` lệch **chưa so** · chia việc theo **CỘT**)*.
- **v2.1** (2026-08-28, `QĐ-ITL-68`): ⭐ **Kế toán (2/2) xác nhận ĐỦ trường cần sửa** ⇒ **7 trường** là đủ. ⛔⛔ Và **nói rõ một hiểu sai**: `hien_vat/mui_thu_luoi_F02.html` là **mũi thử KỸ THUẬT** của ô khó nhất *(8 thao tác gõ)*, ⛔ **không phải bản thiết kế** và ⛔ **không phải thứ giao cho kế toán dùng**. Màn thật làm theo **`FLS-Wireframe.html` + `Demo-MVP-So-may-ITL.html`**, có một lượt thiết kế đầy đủ *(dùng lại bộ token/handoff UIUX của `A-CCR`)*, và lưới bên trong dựng bằng **bảng HTML trần** *(`QĐ-ITL-66`)*. ⇒ Ba thứ chưa đo *(cảm giác · thời gian vẽ · 346px)* trả lời bằng **UAT tuần đầu trên màn thật**, ⛔ không bằng một buổi trên nguyên mẫu thô.
- **v2.0** (2026-08-28, `QĐ-ITL-64`): ⛔⛔ **Cột sửa được 10 → 7.** Owner: *"họ ko sửa, chỉ sửa các trường đã liệt kê trước đó"* ⇒ ba cột vùng `ALLOCATE` là **🔒 chỉ-đọc, máy suy** *(owner đưa nguyên văn 3 công thức — chúng tra `Mapping Master` K/L theo `hd`)*. ⇒ `F02` = **55 cột · 7 gõ được · 48 chỉ-đọc**. ⛔ **Hẹp một phần `QĐ-owner-0824`**; biên bản 24/08 **giữ nguyên**, đính chính đặt **phía trên**. Nguyên mẫu đã sinh lại với 3 cột khoá và nhãn nói rõ **máy suy**.
- **v1.9** (2026-08-28, `CR#8`): ⛔⛔ **Đính chính con số `52 cột` ở đầu §6b — số đúng là `55`.** `BA-07` §3 cho gõ **10 trường**, **5 trường nằm ngoài 14 cột hợp đồng**; ba trường *(`cdt1_cfa1` · `cdt1_cfa2` · `alloc_method`)* ⛔ không có ở đâu ⇒ `F02` cần thêm **3 cột thật**. Bài toán thật **748 × 55 = 41.140 ô** — kết luận *ảo hoá có thể không cần* ⛔ **không đổi**. ⛔ Khối cảnh báo 27/08 **giữ nguyên**, đính chính đặt **phía trên** nó. ★ Owner mở nguyên mẫu và báo thiếu `Mã đối tác` + `File đính kèm: Hóa đơn`; máy ⛔ không thấy vì nó đo hình dạng, ⛔ chưa đo việc gõ vào đúng trường.
- **v1.8** (2026-08-27, sau mũi thử `GAP-SCR-03`): ⛔⛔ **Thêm khối cảnh báo đầu §6b — ba con số của bài toán đã bị ĐO LẬT** *(`CR#7`)*. Đo trên kho thật: **52** cột *(38 canon + 14 hợp đồng)* · **10** cột sửa được · **748** dòng một lát *(kỳ dày nhất)* · **705 byte/dòng** · **36,1%** ô rỗng — ⛔ không phải *"~64 cột × vài nghìn dòng, chỉ 5 cột sửa được"*. ⇒ ảo hoá **có thể không cần**, mà đó là lý do chính để §6b chọn `react-datasheet-grid` ⇒ **quyết định phải xem lại**. ⭐ Xuất hiện **ứng viên thứ tám: bảng HTML trần, không thư viện** — đã có nguyên mẫu chạy trên dữ liệu thật với **cả 8 hành vi §1**, và chỗ *đông cứng N cột trái* **đã bị bỏ** *(`left` = tổng đúng của bề rộng đã khai, ⛔ không còn ước lượng)*. ⛔ Bảng khảo sát 24/08 **giữ nguyên** làm biên bản. `GAP-SCR-03` còn mở nhưng đổi hình: nay là **một buổi ngồi cùng kế toán**, ⛔ không còn là dự án khảo sát.
- **v1.7** (2026-08-25, `QĐ-ITL-48`): **`SCR-F01` thêm hành động Ghép lệnh** *(`OP-02` số hoá — mapping là việc của FLS)*: drawer gợi ý `fps_pm_slip` → chọn phiếu → chia tiền theo `fps_pm_line.amount`, `Σ=tiền bank` mới cho ghép *(`CR#1`)*. Wireframe dựng + test. `§2` thêm endpoint `/queue/{itl_id}/match`.
- **v1.6** (2026-08-25, rà ERD↔màn hình + grill): khớp màn với schema. **F03 cổng Final** đổi tautology → **hai số** `*_thyt NULL` + override *(US-025/029)*. **F02** cột → *"Trạng thái ghép"* *(khác `audit_status`)*; drawer thêm `audit_status`; đối soát LE↔trả nay có nền cột `le_payer` + `is_intercompany`. **F01** thêm **nút Hoãn** *(US-040)*. **Badge kỳ** `period_state` ở sidebar. **F06** có endpoint `/sources`·`/mapping-master`·`/le`. `pic` giữ schema, chưa lên UI.
- **v1.5** (2026-08-25, owner: chỉ kế toán dùng): **Cắt sidebar còn 4 màn có nghiệp vụ kế toán** *(F01·F02·F03·F06)*. Bỏ tab **F07 Chạy·Kiểm tra** → badge *"dữ liệu tới X · DQ ✓"*; **F05 Một trang tuần** → nút *Xuất báo cáo tuần* gấp trong F03; **F04 Xu hướng nhãn** bỏ hẳn; **Phủ 45 US** = tài liệu, không lên UI. Layout F02 chuyển drawer + đầy trang + ghim cụm nhận diện. Sidebar phẳng 4 mục.
- **v1.4** (2026-08-24, `QĐ-owner-0824`): **Mở rộng mặt kế toán sửa từ 5 → 7 khối + phân bổ.** §3 panel tách **Nhóm A** *(5 khối engine P&L đọc — hợp đồng)* và **Nhóm B** *(khối ⑥ Mã đối tác · ⑦ Hoá đơn · ALLOCATE CFA1/CFA2/Method — sửa được nhưng ngoài P&L, máy gợi ý + override)*. Sửa nhãn cụt `HD/PT/CDT/SS/SE` → tên đầy đủ. Wireframe cập nhật khớp.
- **v1.3** (2026-08-24): **§6b — khảo sát thư viện lưới, đóng phần khảo sát `GAP-SCR-01`.** Đề xuất `react-datasheet-grid` (MIT) + dự phòng AG Grid Community; bảng 8-hành-vi × 7 ứng viên; bẫy license *(Handsontable không OSS, 4 cử chỉ AG Grid là Enterprise-only)*; điểm yếu cần spike = đông cứng cột trái ⇒ nối vào `GAP-SCR-03`.
- **v1.2** (2026-08-24): **`SCR-F02` tách lưới-quét + panel đối soát đủ trường** *(owner: sổ cần đủ trường để kế toán đối chiếu trước khi adjust)*. Panel 4 nhóm: giao dịch gốc · chuỗi lệnh PM/PE/PI · chứng từ + đối soát LE-vs-pháp-nhân-trả · 5 trường Final sửa được kèm nguồn gợi ý. Wireframe `FLS-Wireframe.html` cập nhật khớp.
- **v1.1** (2026-08-24): Dựng **3 wireframe tương tác** `SCR-F02/F01/F05` → lộ **§1b: ba giới hạn** spec đang nhẹ tay *(lưới HTML không làm nổi 4 hành vi ⇒ cần thư viện lưới; lưu-theo-lô là cả cơ chế; nút [Sửa ở PM] không ghi ngược được)*. Nâng **`GAP-SCR-01` thành rủi ro lịch lớn nhất** kèm danh sách ứng viên + tiêu chí; mở `GAP-SCR-04/05`.
- **v1.0** (2026-08-24): Viết mới cho FLS, đóng `GAP-ITL-53`. **§1 — 8 hành vi Sheets bắt buộc** *(điều kiện sống còn: thiếu là kế toán về Sheets)*. 5 màn `SCR-F01…F05` + drawer nhật ký, gắn story + API. `SCR-F02` đặc tả field-level với 3 quy tắc *(`UNMAPPED` phải khác `ok`; KÊU khi gõ khác nguồn; flash in mờ)*. `SCR-F01` là chỗ `US-045` đo cổng sống/chết. Nguồn: demo v5 làm spec hành vi sống.
