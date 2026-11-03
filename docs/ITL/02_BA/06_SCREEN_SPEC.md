# 06 — SCREEN SPEC: FLS

**Version:** v4.24 · **Ngày:** 2026-10-06 · **Chủ sở hữu:** BA/PO
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
| `SCR-F01` | ⭐⭐ **Ghép lệnh chi** — **MỘT việc, HAI chế độ**: ⭐ **`Tự động`** *(máy ghép, người duyệt lô)* · ⭐ **`Thủ công`** *(người ghép từng việc)* *(`QĐ-ITL-136`)*. Một việc một lúc, ⛔ không lưới | `AC-B` | `US-039/046/053/054/055` · `OP-02` | `GET /queue/lenh-cho/ro` · `/itl-candidates` · `POST /queue/{id}/match` · **`/unmatch`** · `POST /queue/match-lo` |
| ⚰ ~~`SCR-F07`~~ | ⚰ **KHAI TỬ 2026-09-18, `QĐ-ITL-136`** — khai buổi sáng, bỏ buổi chiều. Tôi đóng khung `6.165` dòng tiền ⛔ không có lệnh chi thành một **việc KIỂM SOÁT**; owner bác **cái khung**: *"FLS ⛔ không cần trả lời câu hỏi này"*. ⭐ Dòng này **giữ làm bia**, ⛔ không xoá — `SCR-F07` đã kịp đi vào `CR#12` và `BA-14 §8` | — | — | — |
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

### ⑪  ⭐ *(v4.24)* Ô sửa được trên lưới in **FINAL**, ⛔ cột nguồn thô — và phép hỏi lại `ⓒ` ⛔ gọi chính người gõ là *"người khác"*

⛔⛔ **Lỗi đo được** *(`KQ-061 F-2`, `fls-test` 06/10, Chrome 8099 kho TEST)*: người gõ `hd` = `X` ở dòng `1`, lô lưu ghi xong *(kho TEST `adj_id 4312`)*, tải lại trang ⇒ ô in **`chưa gán`** dù `GET /ledger/1/fields/hd` trả `gia_tri X · value_source sua_tay`. Người tưởng giá trị mất, gõ lại `X` ⇒ phép hỏi lại `ⓒ` *(`man_f02.js::_ghi_mot_o` `:943`)* thấy `tay = X` khác ảnh lưới ⇒ hộp *"Ô này đã có NGƯỜI KHÁC gõ … Máy chưa ghi gì cả … cách ra là hỏi nhau"* — cho **chính** giá trị người ấy vừa gõ.

Gốc *(`fls-ba` đọc mã `Đ1` @ `7b4237f`)*: lưới đọc `GET /ledger` ⇒ `doc_bao_cao.py::doc_so` chọn `i.hd` · `i.pay_type` · `i.cdt1` · `i.svc_start` · `i.svc_end` **thô** từ `fls_itl` *(`_COT_SO` `:73-80`)*. `grep -n fls_sua_tay fls/repo/doc_bao_cao.py` ⇒ **2** chỗ: `:461` *(`doc_mot_dong` — drawer)* · `:662` *(`dem_xong_du_thieu`)* — ⛔ ở `doc_so`. Trong khi chính spec gọi năm cột ấy là **Final** *(`§3-cũ` bảng lưới: *"5 trường Final … vùng người gõ"*; `§3` panel: *"máy gợi ý → ô người sửa (Final) → nhật ký"*)* và `BA-05` v0.32 đã khai **Final = `fls_sua_tay` ∪ cột nguồn** ⇒ spec **thiếu** ở **hợp đồng cửa** *(`BA-07` v3.13 `GET /ledger` chỉ nói *"dòng `fls_itl`"*)*, ⛔ thiếu ở nghiệp vụ — `fls-ba` quyết trong thẩm quyền spec, ⛔ câu owner.

⚠ **Vì sao là việc CAO dù sổ thật hôm nay 0 ô sai** — đo 06/10 sổ thật, chỉ `SELECT`: cột nguồn của **cả năm** trường **rỗng 8.387 / 8.387** *(mỗi trường **0** dòng có giá trị)*; `*_thyt` có giá trị **0 / 8.387**; `fls_sua_tay` hiệu lực **0**. ⇒ Final hôm nay = **chỉ** lớp người ⇒ ngay **phiên sửa thật đầu tiên** *(cổng `C1` — `09` §3: ≥20 bút toán người thật trải 7 ô)*, **mọi** ô người vừa gõ trên lưới sẽ in `chưa gán` sau một lần tải lại — **100%** — và mỗi lần gõ lại là một hộp *"người khác"* ⛔ có thật. Với `2–3` kế toán *(`QĐ-ITL-27`)* câu *"hỏi nhau"* là đi hỏi một đồng nghiệp **⛔ hề gõ**.

| # | Luật v4.24 | Đo được bằng | ⛔ |
|---|---|---|---|
| ⓐ | **Năm ô sửa được của lưới in giá trị FINAL** = bút toán người hiệu lực *(`fls_sua_tay`, có giá trị)*; ⛔ có thì cột nguồn `fls_itl.<field>`; ⛔ có nữa ⇒ `chưa gán` *(lớp `unmapped` — như nay)*. Gợi ý máy *(`fls_may_goi_y` · `*_thyt`)* **⛔ bao giờ** in vào ô *(`QĐ-ITL-149` · `QĐ-ITL-35`)* — drawer vẫn nói *"máy gợi ý"* như nay. Cửa trả `<f>_final` + `<f>_nguon` *(`BA-07` **v3.14**)*; lưới đọc `<f>_final`. Luật **một chỗ** *(`BA-05` **v0.35** `DD-I15 ⓓf`)* — ⛔ bản thứ hai của phép xếp lớp | bài cửa thật kho TEST ⇒ màn | ô in cột thô; ô in gợi ý máy |
| ⓑ | Ô có `<f>_nguon = sua_tay` mang `title` *"người sửa — sổ gốc nói: &lt;giá trị thô, hay chữ trống&gt;"* *(chữ trơn; ⛔ lớp CSS / token mới)* — giữ câu *"nguồn nói X, người gõ Y"* *(`QĐ-ITL-73 ⓔ`)* ngay trên lưới | bài DOM | ô người ⛔ phân biệt được với ô nguồn khi rê chuột |
| ⓒ | **Ảnh chụp lưới** mà phép hỏi lại `ⓒ` đem so *(`ST.theo_id.get(itl)[field]`)* = **`<f>_final`** lúc tải | bài DOM | so với cột thô |
| ⓓ | Phép hỏi lại `ⓒ`: `tay` **bằng** giá trị đang định ghi *(so sau `String()`, như các vế đang có)* ⇒ **⛔ va chạm** — sổ đã giữ đúng giá trị ấy: ⛔ hộp *"NGƯỜI KHÁC gõ"*; ô sang `da-luu`; **0** dòng `fls_adjustment` mới *(Dev chọn: bỏ `POST`, hay gửi và cửa trả `da_co: true` — `ghi_tay.py:462` *"lặp lại cùng giá trị thì ⛔ chèn dòng thứ hai"*)*. Vế này cũng là đường ra an toàn của lô lưu hết giờ *(`§4.5 ⓔ` `ⓕ3` — v4.24)*: bấm `Thử lại` ⛔ gặp hộp *"người khác"* | bài DOM + cửa thật kho TEST | hộp *"người khác"* cho chính giá trị đang gõ |
| ⓔ | Hai cột lưới **Quét** `HDCode` · `CDT1` *(§3c ①)* theo cùng luật ⓐ | bài DOM chế độ Quét | Quét in thô, Gõ in Final |

⚠ **Câu treo, ⛔ chặn** *(ghi để owner biết)*: người **xoá ô** *(`/adjust value=null`)* trên một ô mà cột nguồn **có** giá trị ⇒ cả cửa ghi *(`truoc_khi_go` `ghi_tay.py:306-313`: lớp người chỉ thắng khi `tay is not None`)* lẫn phép đếm `dem_xong_du_thieu` *(`COALESCE`)* đều rơi về **nguồn** ⇒ Final = nguồn, cú xoá ⛔ có tác dụng lên Final. Lưới theo **đúng** luật ấy *(một luật, ⛔ bản thứ hai)*. Sổ thật hôm nay: cột nguồn rỗng **8.387 / 8.387** ở cả năm trường · `fls_sua_tay` giá trị rỗng **0** ⇒ ⛔ ô nào gặp. Muốn *"người xoá thì Final trống"* là đổi luật **cửa ghi** — câu của owner, phiếu riêng.

Mã ⇒ **`WO-062`**.

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

## §4 · ⭐⭐⭐ `SCR-F01` — **MỘT việc, HAI chế độ** *(viết lại 2026-09-18 chiều, `QĐ-ITL-136`)*

> ⚰⚰ **Bản `v3.2` (sáng cùng ngày) chia màn theo trục SAI, và owner sửa trục ấy.** `v3.2` tách `SCR-F01` / `SCR-F07` theo *"việc KHỚP vs việc KIỂM SOÁT"*. Owner bác **cả hai vế**: ⓐ *"FLS ⛔ không cần trả lời câu hỏi «tiền đã rời tài khoản, có ai duyệt ⛔ không»"* ⇒ `SCR-F07` **khai tử**; ⓑ *"Duyệt lô và Ghép từng việc **đều là mapping**, chia theo **người ghép** và **máy ghép**"* ⇒ trục đúng là **`Tự động` / `Thủ công`**.
>
> ⭐ **Phép đo của `v3.2` ⛔ không sai — cái khung thì sai.** `6.165` dòng tiền ⛔ không có lệnh chi **vẫn là `6.165`**; nó chỉ ⛔ **không phải một việc của FLS**. Và điều đó nhất quán với `QĐ-ITL-56`: ⛔ **không có quy định nào** nói khoản nào cần lệnh chi ⇒ ⛔ không có luật thì ⛔ không có vi phạm để soát. ⛔⛔ Dựng một màn soát trên một luật ⛔ không tồn tại là đúng thứ `INV-I16` cấm — lần này **người dựng là tôi**, ⛔ không phải máy.

### §4.0 · Trục đúng: **AI ghép**, ⛔ không phải *việc gì*

| | ⭐ `Tự động` | ⭐ `Thủ công` |
|---|---|---|
| Ai ghép | **MÁY** | **NGƯỜI** |
| Người làm gì | **duyệt một lượt** | **quyết từng dòng** |
| Điều kiện | khớp **cả** số chứng từ **lẫn** số tiền ⇒ đáp án **duy nhất** | ⛔ không đủ điều kiện tự chứng |
| Dòng *(`18/09`)* | **47** | **738** |
| Nhịp | một cú bấm mỗi sáng | hằng ngày |

⛔⛔ **Ba tên cũ *(duyệt lô · ghép từng việc · soát chi không lệnh)* trộn HAI trục khác nhau** — *ai làm* và *việc gì* — nên chúng trông như **ba việc** trong khi thật ra là **MỘT việc, HAI chế độ**, cộng thêm hai **đích cuối** ⛔ không phải việc.

### §4.1 · `Thủ công` — một việc một lúc

- ⭐⭐ **⛔ KHÔNG phải một lưới.** Lưới hợp khi người ta **so các dòng với nhau**; ở đây mỗi lệnh chi là **một câu hỏi độc lập** và đáp án nằm ở **sổ tiền**, ⛔ không nằm ở dòng bên cạnh.
- ⭐⭐⭐ **NGÂN SÁCH TRƯỜNG = `9`** *(`UI-F7`)*: người nhận · số tiền · nội dung · ngân hàng · số tài khoản · pháp nhân · phiếu · số chứng từ · câu *vì sao*. **Thêm một ⇒ bỏ một.**
- ⛔ **Ba thứ bị BỎ khỏi màn:**

  | Bỏ | Vì sao |
  |---|---|
  | `Luỹ kế %` · `hạng` | Là **vị trí trong danh sách**, ⛔ không phải thuộc tính của khoản tiền |
  | ~~nút *"Hiện đủ 28 cột"*~~ ⚰ **SỐNG LẠI `18/09`** | ⛔ Lý do cũ *("cột đáng xem thì phải ở trong 9 trường")* **SAI LÝ DO**: kế toán cần nó để **yên tâm về data**, ⛔ không phải để ghép — xem `§4.4 ⓐ` |
  | tên rổ | Người đọc **câu nói**, ⛔ không đọc tên nhóm máy tự đặt |

- ⭐ **Máy đề xuất, ⛔ không máy quyết.** Đo `500/535`: **275 (55%)** đã có **một dòng tiền khớp ĐÚNG số tiền** trong 4 ứng viên ⇒ đánh dấu **`đúng số tiền`** + chọn sẵn. **45%** còn lại ⛔ **không chọn sẵn gì**, và màn phải trông **khác** — nếu ⛔ không kế toán sẽ quen tay bấm `↵`.
- ⭐⭐ **Hai đáp án cùng đúng ⇒ máy DỪNG** *(`INV-I16`)*. Ca thật: `PM01342-1` và `PM01964-1` cùng `1.035,50 SGD`, sổ có **đúng hai** dòng cùng số ấy, **hai pháp nhân khác nhau**.
- ⭐⭐ **`Bỏ ghép` PHẢI có.** Cửa `POST /queue/{itl_id}/unmatch` **có**, nút **⛔ không có** ở lằn mặc định *(`US-056`)* ⇒ ⛔ **không** bước xác nhận trước khi ghép; đổi lại `Bỏ ghép` ở ngay dải vừa-xong.

### §4.2 · `Tự động` — người duyệt, ⛔ không người xét

- **47** dòng tự chứng. Màn hiện **lệnh ↔ dòng tiền** cạnh nhau để mắt lướt, một nút **Duyệt cả 47**.
- ⚠ **`203` dòng khớp mã nhưng LỆCH TIỀN ⛔ KHÔNG vào đây** — đó là chỗ máy **phải hỏi** *"lệnh này ăn bao nhiêu của giao dịch kia"*; gộp vào là để máy quyết thay người *(`INV-I16`)*. Chúng thuộc `Thủ công`.

### §4.2b · Hai **ĐÍCH CUỐI** — ⛔ không phải chế độ thứ ba

| Đích | Dòng | Là gì |
|---|--:|---|
| ⛔ **Ghép ⛔ không được** | **768** | Có số chứng từ nhưng sổ ⛔ không có đồng tiền nào mang số ấy. Mỗi dòng mang **câu vì sao**; `272` dòng có bạn đời ở **8 sheet đã bỏ `10/09`** |
| ⚠ **Lỗi nguồn** | **167** | ⚰⚰ **`v3.3` ghi *«`166` ô số chứng từ `Reject` ＋ `1` ô tiền tệ `20`»* — TỔNG đúng, **PHÉP CỘNG SAI**, `QĐ-ITL-142`.** Đo lại `18/09` bằng `pm_line_id` phân biệt: `ref_tho='Reject'` **167** · `curr` là một con số **1** · **giao nhau `1`** ⇒ hợp **167**, ⛔ không phải `166＋1`. ⭐ Hai khuyết tật ấy nằm trên **CÙNG MỘT DÒNG** `PM00576-1` *(`ref_tho='Reject'` · `curr='20'` · `amount=20,00`)* ⇒ nó ⛔ không phải *"một đơn vị tiền tệ tên 20"*, nó là **một dòng bị XÊ CỘT**. ⛔ FLS **chỉ mặt**, ⛔ không tự chữa *(`INV-I16`)* — nhưng **phải có nút GỬI** |

⛔ **Hai đích này ⛔ không phải việc của ai trong FLS** — chúng là chỗ một dòng **rời hàng chờ mapping** *(`INV-I20`)*, ⛔ không phải chỗ ai đó ngồi làm.

### §4.2c · Hàng chờ mapping phải có **LỐI RA**

`INV-I20`. Một dòng rời hàng chờ bằng **ba** đường: **ghép được** *(người hoặc máy)* · máy xếp vào đích **⛔ ghép không được** *(mang câu `vi_sao` **MÁY sinh**)* · máy xếp vào đích **lỗi nguồn**. ⛔⛔ **⛔ KHÔNG có đường thứ tư *«người gõ lý do»*** — `QĐ-ITL-137` hoãn cột ấy. ⭐⭐ **Thước đo lối ra ⇒ `fls_pm_link.hinh = 'T'`** *(mối nối do **NGƯỜI** tạo — `ghi_tay._HINH_TAY`)*, ⛔ không phụ thuộc một cột nhập liệu nào. Đo `18/09`: **`0`** *(`A` 2.145 · `B` 65 · `C` 52)* ⇒ **⛔ chưa một người nào từng ghép một dòng**. ⚠ `US-045` **HOÃN** theo cột lý do.

### §4.4 · ⭐⭐⭐ KẾ TOÁN NÓI — buổi BA màn hình `18/09` *(`QĐ-ITL-144`)*

> ⭐ Owner BA màn hình **cùng kế toán** rồi mang về **bốn** yêu cầu giao diện ＋ **một luật ghép** *(luật ở `BA-10 DT-I13`)*. Đây là **lần đầu** những câu này đến từ **người sẽ dùng màn**, ⛔ không từ tôi.

#### ⓐ ⚰⚰ Nút *"xem đủ trường"* — **SỐNG LẠI**, và lý do bác bỏ của tôi là **SAI LÝ DO**

`§4.1` khai tử nút *"Hiện đủ 28 cột"* với câu: *"cột đáng xem thì phải ở trong 9 trường"*. Kế toán bác, và **lý do họ đưa khác hẳn cái tôi giả định**:

| | |
|---|---|
| Tôi giả định | nút ấy phục vụ **việc ghép** ⇒ cột nào cần thì cho vào 9 trường |
| Kế toán nói | *"cần view xem tổng các giao dịch, **đủ các trường** như GGSheet/Excel — **để yên tâm về data**"* |

⇒ ⭐⭐ **Đó là hai NHU CẦU khác nhau, và tôi trộn chúng làm một.** Xem-đủ-trường ⛔ **không** phục vụ thao tác ghép — nó phục vụ **niềm tin**: *"số trong app có đúng bằng số trong sheet ⛔ không"*. Một nhu cầu **thưa** *(vài lần đầu, rồi mỗi khi nghi ngờ)*, ⛔ không phải nhu cầu **mỗi dòng**.

⇒ **Cách xử ⛔ KHÔNG phải nhét 28 cột vào danh sách làm việc** *(đó mới là thứ `UI-F7` cấm, và `UI-F7` **đứng nguyên**)*. Nó là **một mặt XEM riêng**: lưới đầy đủ, chỉ-đọc, ⛔ không nút hành động nào — **`SCR-F02` đã là đúng mặt ấy** *(`52` cột, `QĐ-ITL-65`)*. ⇒ Việc thật: **một đường đi thẳng từ màn ghép sang `F02` đã lọc sẵn đúng dòng đang xem**, ⛔ không dựng lưới thứ hai.

> ⭐⭐ **HẸP LẠI `21/09` — `QĐ-ITL-147`, owner xác nhận GIỮ *«Xem đủ trường»* ngay trong màn ghép.** Bản thiết kế bung **`17` trường** tại chỗ *(gấp lại được)*, và owner **gật**. ⇒ Câu *"⛔ không dựng lưới thứ hai"* ở trên **hẹp lại**: nó vẫn cấm nhét `28` cột vào **danh sách làm việc**, nhưng ⛔ **không** còn cấm một **khối bung theo yêu cầu** trên thẻ lệnh đang mở. ⭐ Lý do owner giữ đúng lý do kế toán đưa: nhu cầu **yên tâm về data** xảy ra **giữa lúc đang ghép**, nên bắt người **rời màn** để thoả nó là bắt họ trả giá **đúng lúc đắt nhất**. ⇒ Đường sang `SCR-F02` **⛔ không bị bỏ** — nó thôi là cách **duy nhất**. ⚠ Còn **một vế chưa xử**: `6` ô `ID PMSlip`…`ID PILine` trong khối bung vẫn là `*_id` nội bộ *(`UI-F8`)*.

⛔ **Bài học, và nó lặp lại:** tôi bỏ một nút vì **đoán sai nó phục vụ việc gì**. Cùng lớp lỗi với `QĐ-ITL-136` *(dựng `SCR-F07` cho một câu hỏi ⛔ không ai hỏi)* — **khác chiều, cùng gốc**: kết luận về nhu cầu của người dùng mà ⛔ không hỏi người dùng.

#### ⓑ Trường phải THÊM — và mỗi cái có chỗ để thêm

| Khu vực | Kế toán đòi thêm | Lấy từ đâu | Được ⛔ không |
|---|---|---|---|
| Danh sách lệnh chi | ⭐ **số PM** | `pm_line_id` ／ `pm_slip_id` | ✅ có sẵn |
| Panel · vế **lệnh chi** | **ngày** | `tho['Timestamp']` — ⚠ **sê-ri Excel** *(`45813.49`)*, phải đổi ra ngày | ✅ đổi được |
| Panel · vế **lệnh chi** | **CDT** *(chủ dự toán)* | `fls_pm_line.cdt1` | ✅ **3.763/3.772** |
| Panel · vế **giao dịch** | **ngày** | `fls_itl.doc_date` | ✅ **8.387/8.387** |
| Panel · vế **giao dịch** | ⛔ **nội dung giao dịch** | `fls_itl.memo` | ⛔⛔ **0 / 8.387** |

⛔⛔⛔ **Ô cuối là chỗ đặc tả PHẢI dừng lại và nói thật.** Kế toán đòi *nội dung giao dịch* ở panel — **đúng thứ đáng đòi nhất**, vì nó cũng là vế đầu của **luật ghép nhánh nước ngoài** *(`DT-I13 ⓑ`)*. Nhưng sổ ⛔ **không có một dòng nào**: tầng `R |` của bảng tính nguồn **chỉ có 5 cột**, và cột diễn giải **⛔ chưa bao giờ vào phạm vi**.

⇒ ⭐ **Đây là việc của NẠP, ⛔ không phải việc của màn** *(`GAP-NAP-04`)*. Màn hình ⛔ **không được** vẽ một ô trống rồi để đấy — nó phải **nói ra** rằng cột này **chưa được nạp**, ⛔ không phải *"giao dịch này không có nội dung"*. Hai câu ấy khác nhau, và lẫn là đúng bệnh `QĐ-ITL-110 ⓑ` đã xử một lần.

> ⭐⭐⭐ **ĐÍNH CHÍNH — `QĐ-ITL-145`, cùng ngày `18/09`, vài giờ sau.** Ô `⛔⛔ 0 / 8.387` ở trên **đúng lúc đo** và **⛔ không còn đúng**. Diễn giải sao kê ⛔ **chưa bao giờ thiếu**: nó nằm sẵn trong **ảnh chụp theo nhịp giờ**, chỉ là ⛔ **không đường nào nối** nó với một dòng sổ. Khung xem **`fls_dien_giai`** *(migration `0026`)* nối được **`8.358/8.387` = 99,7%**, có **kiểm chéo tiền tệ** làm chứng ⛔ không lệch hàng. ⇒ Vế *nội dung giao dịch* mà kế toán đòi **nay có thật**, và `§4.5` thiết kế quanh nó. ⛔ **Giữ nguyên chữ của bảng trên** — nó là bản ghi của phép đo lúc `0/8.387`, ⛔ không phải một câu sai cần xoá.

#### ⓒ Bốn điều một giao dịch có — và đó là **tất cả**

⚠ Đo `18/09` trên `fls_itl` *(`8.387` dòng)*: cột **CÓ** dữ liệu là `doc_date` **8.387** · `doc_no` **8.383** · `curr` **8.387** · `ps_no` **4.520** ／ `ps_co` **7.558** · `source_sheet` **8.387**. **RỖNG hoàn toàn**: `memo` · `acct` · `le` · `le_payer` · `pic` ＋ cả `7` khối `Final`／`*_thyt`.

⭐ **Thứ cứu panel là `source_sheet`** — nó mang **số tài khoản ＋ ngân hàng ＋ tiền tệ ＋ pháp nhân** trong một chuỗi *(`358468128_VPB VND_VGOH`)*, và nó **có ở 100%** dòng. ⇒ Panel dùng **nguồn** làm manh mối chính cho tới khi `GAP-NAP-04` đóng. ⛔ Ghi rõ đây là **chắp vá**, ⛔ không phải thiết kế.


### §4.5 · ⭐⭐⭐ THIẾT KẾ ĐÃ VỀ — hợp đồng hình dạng của `SCR-F01` *(2026-09-21, `QĐ-ITL-146`)*

> ⭐ **Nguồn của mục này ⛔ không phải suy luận của tôi.** Owner gói bối cảnh *(`Artifacts/Prompt-Claude-Design.md`)* đưa sang người thiết kế; bàn giao về gồm **hợp đồng thiết kế** ＋ **ba bản dựng chạy được**. Mục này là phần **đặc tả** rút từ đó, ⛔ không phải bản chép.

| Hiện vật | Đường dẫn | Vai |
|---|---|---|
| ⭐ **Hợp đồng thiết kế** | `Artifacts/Thiet-ke-Man-Gan-Lenh-Chi.md` | Luật hình dạng — đọc **trước** khi sửa UI |
| ⭐⭐ **Bản dựng CHÍNH** | `Artifacts/fls-gan-lenh-chi_10.html` | Một tệp, tự chạy. **Spec hành vi sống** |
| **Bản dựng DỮ LIỆU THẬT** | `Artifacts/man-gan-lenh-chi-v2.html` | 40 lệnh chi, kho `18/09` *(tên cá nhân **đã che**)* |
| ⚰ Bản trước | `Artifacts/fls-gan-lenh-chi_9.html` · `man-gan-lenh-chi.html` | Giữ để đối chiếu **vì sao đổi** |
| Token | `Artifacts/tokens-man-ghep.css` | ✅ **đã hợp nhất** `22/09` — `5` token vào `fls/web/tep/tokens.css`, tên cũ **giữ nguyên**. `GAP-SCR-21` ĐÓNG; xem `§7 ⓒ` |

#### ⓐ Luật BỐ CỤC — và nó đổi một hằng số cũ

```
┌ thanh trên 44px ─────────────────────────────────────────────┐
├ dải lọc ＋ số việc 36px  (thay 4 ô thống kê cũ) ─────────────┤
│ ┌ rail lệnh chi ─┐ ┌ vùng làm việc ───────────────────────┐ │
│ │ (chỉ khi đã mở)│ │ đầu: thẻ lệnh chi        (đứng yên)  │ │
│ │                │ │ thanh tra cứu            (đứng yên)  │ │
│ │                │ │ BẢNG GIAO DỊCH — vùng DUY NHẤT cuộn  │ │
│ │                │ │ thanh hành động          (đứng yên)  │ │
└─┴────────────────┴─┴──────────────────────────────────────┴─┘
```

- **Trang ⛔ không cuộn.** Khung cao bằng màn hình; mỗi vùng tự cuộn, và trong vùng làm việc chỉ **bảng giao dịch** cuộn.
- **Chưa mở lệnh nào** ⇒ một bảng sổ chiếm toàn bộ bề ngang. **Đã mở** ⇒ bảng thu về **rail**.
- ⚠⚠ **Đổi hằng số:** rail là **`clamp(300px, 26vw, 380px)`**, ⛔ không phải `--panel-san 430px` / `--panel-tran 680px` mà `§7` đang khai. Hai bộ số ⛔ không thể cùng đúng ⇒ `§7 ⓒ`.
- ⭐⭐ **Bảng ứng viên đo theo `@container` của vùng làm việc**, ⛔ **không** theo viewport — rail chiếm chỗ **trước**, nên đo theo viewport là đo sai bề rộng thật.
- ⭐⭐⭐ **THỨ TỰ HY SINH CỘT khi hẹp: `Nguồn` → `Số CT` → ⛔ KHÔNG BAO GIỜ là `Diễn giải`** *(`minmax(200px,1fr)`)*. Đây là luật **cứng**, vì diễn giải là **bằng chứng duy nhất** của nhánh nước ngoài *(`DT-I13 ⓑ` — `4.145/8.387` = 49% cuốn sổ)*.

#### ⓑ Mười component ＋ trạng thái bắt buộc

| # | Component | Trạng thái phải có |
|:-:|---|---|
| `C1` | **Dòng sổ** *(`.mrow`)* | chưa gán · đề xuất · đã gán · ⛔ không gán được · hover · con trỏ bàn phím *(`aria-current`)*. ⭐ Trạng thái đọc bằng **vạch trái 3px** ＋ chip |
| `C2` | **Thẻ lệnh chi** *(`.wh`)* | dòng 1 định danh ＋ tiền · dòng 2 lưới fact đều · dòng 3 **Xem đủ trường**. ⚠ Đếm được **11** ô — xem `ⓔ` |
| ⭐ `C3` | **Dòng ứng viên** *(`.cand`)* | cột: ○ · **bậc ①–④** · Số CT · **Diễn giải** · Ngày · Nguồn · Số tiền. Cao **36px cố định**; chỉ khi bung mới cao thêm |
| `C4` ✅ **LÀM `23/09`** | **Khối đang gán** *(`.mblock`)* | bậc · diễn giải **nguyên văn** *(tô bằng chứng)* · ngày · nguồn · số CT · số tiền · độ lệch · nút bỏ gán. ⭐ Thêm **dòng TỔNG** khi lệnh gán **hơn một** dòng tiền — xem `§4.5 ⓣ` |
| `C5` | **Bộ lọc** | `Chưa gán` ／ `Đã gán` ／ `Tất cả`, mỗi cái mang **số đếm** |
| `C6` | **Dải số việc** | gộp **một dòng**: `x/y đã gán · 47 đề xuất gán · 768 ⛔ không gán được`. ⚰ Thay `4` ô thống kê cũ |
| `C7` | **Dải cảnh báo** *(`.banner`)* | `crit` = máy ⛔ không tìm được ứng viên · `warn` = ⛔ không ứng viên nào đúng tiền · `info` = danh sách **đã cắt bớt** |
| `C8` | **Thanh hành động** | `Gán` ／ `Đổi sang giao dịch đã chọn` · bật／tắt · ⭐ **hai bước** khi lệch tiền · câu gợi ý |
| `C9` | **Rail** | ngày · mã lệnh · loại ＋ trạng thái ／ nội dung ＋ số tiền ／ `CDT` |
| `C10` | **Trạng thái khung** | rỗng *(«Hàng chờ đã sạch.»)* · ⛔ không có ứng viên · ⛔ không khớp bộ lọc |

#### ⓒ Bốn quyết định khó — và mỗi cái trả lời một câu `Brief §8`

| # | Quyết | Cách làm | Vì sao ⛔ không làm cách khác |
|:-:|---|---|---|
| ① | **Bốn bậc** | **thứ tự** ＋ **ký hiệu `①②③④` tô màu** *(good ／ info ／ warn ／ —)* ＋ vạch trái `3px`. Nghĩa nói **một lần** ở chú giải ＋ `title` | ⛔ Nhóm có tiêu đề **tốn dòng**; ⛔ bốn chip cùng cỡ thì bậc ④ *(`149/226` ứng viên)* **nhuộm hết màn** |
| ② | **Diễn giải dài `189`** | cắt **một dòng** ＋ liên kết `đủ ↓` **chỉ hiện khi THẬT SỰ bị cắt** *(đo `scrollHeight` **sau khi dàn trang**)* ＋ `title` hover | ⛔ Đoán theo **số ký tự** là sai, vì bề rộng cột đổi theo màn. ⛔ Tooltip ⛔ không được là lối **duy nhất** |
| ③ | **Đề xuất ≠ đã gán** | đề xuất = viền **đứt** ＋ nền `warn` ＋ ⭐ **⛔ KHÔNG chọn sẵn**; đã gán = khối xanh **trên** bảng, dòng tương ứng **vẫn ở trong bảng** để đổi | `INV-I16` ở tầng giao diện. Nếu hai thứ trông giống nhau thì luật *máy ⛔ không quyết* **mất hiệu lực** |
| ④ | ⭐⭐ **Chống gật phản xạ** | khi ⛔ **không** ứng viên nào đúng tiền ⇒ dải `warn` riêng · thanh hành động đổi nền · nút chính **bỏ nền đặc** · ⭐ **`Enter` BỊ KHOÁ** · phải bấm **hai lần** | `45%` ca ⛔ không có ứng viên khớp đúng tiền. Màn **phải trông khác** ở những ca ấy, nếu ⛔ không kế toán quen tay bấm `↵` |

⭐ **Bằng chứng được đánh dấu** *(`<mark>`, nền `--evi-bg`)*: số chứng từ **chỉ khi trùng đúng**, số tiền khi khớp **tuyệt đối**, tên vendor trong diễn giải. Bộ **từ rác** loại chữ pháp lý *(TNHH · JSC · INC · LTD · PTE · CP · VIỆT NAM…)* để ⛔ không tô nhiễu; quét **một lượt** bằng regex hợp nhất nên ⛔ không lồng `<mark>`.

⭐⭐ *(v4.15, `TL-033 ⓑ`)* **Quyết ① nói *"chú giải ＋ `title`"* — và chú giải ⛔ BAO GIỜ được dựng.** Đo 02/10 *(`Đ1`, grep `fls/web/` + `tests/web/`)*: `tlegend`/`chu_giai` **0** chỗ; bản dựng đã duyệt **có** *(`Artifacts/fls-gan-lenh-chi_10.html:739` `.tlegend`)*. ⇒ **cả năm** ký hiệu `①②③④≠` hôm nay chỉ đọc được bằng **di chuột** — trái quyết ② *("⛔ tooltip ⛔ được là lối **duy nhất**")*. Luật: **một** dòng chú giải ở thanh tra cứu ứng viên, **chữ sinh từ `BAC`** *(mỗi bậc `ký hiệu ＋ nghĩa`; ⛔ gõ tay — thêm bậc mà quên chú giải là nói thiếu **im lặng**)* ⇒ hôm nay `① khớp số chứng từ · ② đúng số tiền · ③ gần đúng số tiền · ④ cùng đơn vị tiền · ≠ khác tiền tệ`; hiện ở **cả** *Máy đề xuất* lẫn *Toàn sổ*; ⛔ hiện khi danh sách rỗng hoặc đang tải. Ô `.tg` từng dòng **giữ** ký hiệu ＋ `title` — ⛔ chữ bậc trên từng dòng *(lý do ở cột phải của ①)*. Dòng khác tiền tệ còn hai tín hiệu ⛔ cần chuột: ô `Tiền` kèm mã *(§5b ⓙ)* ＋ nhãn thanh hành động *"(khác tiền tệ — cửa ghi sẽ từ chối)"*. Mã ⇒ `WO-032` vòng 2 `(j)`.

⭐ *(v4.16, `KQ-036 F-4` — `BA-08` **`NFR-I29`**)* **Màu của chú giải và của ký hiệu bậc ⛔ mang tông.** Chú giải là lối đọc nghĩa bậc **⛔ cần chuột** duy nhất *(quyết ②)* — vậy mà chữ **nghĩa** của nó tô `--faint`: đo bằng máy *(`KQ-036` `AC-13`, `getComputedStyle`, 8088 + 8099)* **2,17 : 1** trên `--page`, cỡ `10.5px` *(5 / 5 mục)*. Ô `.tg` của bậc ⛔ mang tông *(④ `cung_tien_te`, `≠` `khac_tien_te` — `m: ''`)* rơi về cùng `--faint`: **2,47 : 1** trên `--surface` *(`fls-ba` tính từ `tokens.css`)* — và `≠` là ký hiệu *"cửa ghi sẽ từ chối"*. Luật: chữ nghĩa chú giải ⇒ **`--muted`** *(**4,92 : 1** trên `--page`)*; ô `.tg` ⛔ tông ⇒ **`--muted`** *(**5,59 : 1** trên `--surface`)*; ⛔ token mới. Ký hiệu `<b>` của chú giải đã `--muted` *(4,92)*. Mã ⇒ `WO-037`.

#### ⓓ Bàn phím ＋ nhịp làm việc

| Ở màn sổ | Ở vùng ghép |
|---|---|
| `↑` `↓` di chuyển con trỏ *(tự cuộn theo)* | `↑` `↓` *(`k` `j`)* đổi sang lệnh trước／sau |
| `→` hoặc `Enter` mở vùng ghép | `←` quay lại màn sổ *(giữ dòng đang chọn)* |
| — | ⭐ `Enter` gán — **CHỈ khi ứng viên đúng số tiền** |
| — | `/` nhảy vào ô tìm · `Esc` thoát ô tìm ／ đóng vùng ghép |

⭐⭐ **Gán xong thì màn TỰ NHẢY sang lệnh chưa gán kế tiếp** — nhịp là *hằng ngày, từng giao dịch một* *(`QĐ-ITL-144 ⓵`)*, nên đưa người về danh sách sau mỗi lần gán là **bắt họ tìm lại chỗ cũ**.

#### ⓔ ⛔⛔ NĂM CHỖ LỆCH — đo được, và `3` trong `5` tôi ⛔ KHÔNG tự xử

⚠⚠ **Cả năm đều đo trên `fls-gan-lenh-chi_10.html`, ⛔ không phải đọc hợp đồng rồi nhận xét.** Và ⭐ **ba chỗ đầu ⛔ không phải người thiết kế vượt rào** — chúng là chỗ **hai yêu cầu của cùng một phía va nhau**, mà ⛔ không ai trong chúng tôi thấy lúc phát biểu.

| # | Lệch | Đo ở đâu | Ai xử |
|:-:|---|---|---|
| ① | ✅ ~~**Thẻ lệnh chi có `11` ô, ngân sách `UI-F7` là `9`**~~ ⇒ ⭐ **ĐÓNG `21/09` — owner nới trần `9 → 11`** *(`QĐ-ITL-147`)* | `buildHead()`: mã lệnh · trạng thái · loại phiếu · nội dung · số tiền — rồi Người nhận · Số CT · Pháp nhân · Ngân hàng · Tài khoản · `CDT`. **Bỏ** *câu vì sao* *(−1)*, **thêm** mã lệnh ＋ trạng thái ＋ `CDT` *(＋3)*. ⭐ Cả `3` ô thêm đều do **owner ＋ kế toán đòi** *(`QĐ-ITL-144`)* ⇒ owner chọn **giữ yêu cầu, nới trần**, ⛔ không bỏ ô | ✅ **Owner đã quyết** — `UI-F7` `F01` = **`11`**; `CR#12 G-b` đổi ngưỡng theo |
| ② | ⭐⭐⭐ **Danh sách mặc định là `1.553`, cổng `G-a` đòi `738`** | `visible()`: bộ lọc `Chưa gán` = *mọi dòng ⛔ không phải `đã gán`* ⇒ nó **gộp cả `768` dòng ⛔ không gán được** vào việc hằng ngày. ⭐ Ba chip lọc *(`Chưa gán` ／ `Đã gán` ／ `Tất cả`)* ⛔ **không có** chỗ cho **đích cuối** — mà `INV-I20` nói đó là nơi một dòng **rời** hàng chờ, ⛔ không phải nơi ai đó ngồi làm | ⭐ **BA** — thiếu **chip thứ tư** *(`⛔ Không gán được`)*, ⛔ không phải lỗi hình dạng. ⇒ `GAP-SCR-20` |
| ③ | ✅ ~~**«Xem đủ trường» dựng LƯỚI THỨ HAI ngay trong `F01`**~~ ⇒ ⭐ **ĐÓNG `21/09` — owner xác nhận GIỮ trong màn ghép** *(`QĐ-ITL-147`)* | `state.showMore` bung **`17` trường** *(Nguồn dự toán `7` · Lập lệnh `4` · Mã hệ thống `6`)*. ⭐ Owner xác nhận: nhu cầu **yên tâm về data** được phục vụ **tại chỗ**, ⛔ không bắt người rời màn đang làm. ⇒ `QĐ-ITL-144 ⓐ` **hẹp lại**: đường sang `SCR-F02` ⛔ **không còn là cách DUY NHẤT** | ✅ **Owner đã quyết** — ⚠ **còn MỘT vế chưa xử**: `6` ô `ID PMSlip`…`ID PILine` vẫn là **`*_id` nội bộ** *(`UI-F8`)* ⇒ `GAP-SCR-20 ⓒ'` |
| ④ | ⚠⚠ **Token ĐỔI TÊN `6` cái đã có** | `--font-sans`／`--font-mono` ↔ kho `--sans`／`--mono`; `--radius-sm/md/lg/pill` ↔ `--bo-nho`／`--bo`／`--bo-the`／`--bo-tron`. ⭐ Thật sự **mới** chỉ `4`: `--hair` · `--evi-bg` · `--rail` · `--shadow-card` *(＋`--b` đặt inline)*. ⛔ Hợp đồng khai *"kế thừa **nguyên văn**"* — ⛔ **không đúng** với `6` cái này | BA ＋ Dev ⇒ `GAP-SCR-21` |
| ⑤ | ⚠ **`§10` hợp đồng đo THỜI GIAN thao tác** | *«Thời gian từ lúc mở một lệnh tới lúc bấm Gán»* ＋ *«tỷ lệ ca lệch xác nhận dưới 2 giây»*. ⛔ Owner **đã bỏ yêu cầu bấm giờ** *(`CR#12`)* ⇒ hai phép đo ấy **⛔ không hiệu lực**; thước sống là **`fls_pm_link.hinh='T'` đi từ `0` lên khác `0`** *(`G-d`)* | ⭐ **Đã xử tại đây** — ⛔ **gốc là lỗi của tôi**: `Prompt-Claude-Design.md` ⛔ không chở ràng buộc ấy sang, nên người thiết kế ⛔ không có cách nào biết |

#### ⓕ ⭐ Cái thiết kế này **SỬA ĐƯỢC** — ⛔ không chỉ là làm đẹp

⛔ **Một bản thiết kế chỉ đáng nhận nếu nó đóng được khuyết tật đo được, ⛔ không phải nếu nó trông khá hơn.** Bốn cái đóng được:

| Khuyết tật cũ | Đo lúc mở | Ở bản dựng |
|---|---|---|
| ⚰ ~~**`Timestamp` hiện ra là `45813.49394`**~~ ⇒ ⛔⛔ **ĐÍNH CHÍNH `21/09`, xem `ⓗ ①`** | sê-ri Excel trần | ⛔ **CÂU NÀY SAI.** Bản dựng hiện `18/09/2026 09:14` vì **dữ liệu mẫu do người thiết kế tự gõ**; kho thật vẫn **`3.772/3.772` sê-ri**, `0` dòng có dấu ngày. Tôi **đo bản dựng mà tưởng đã đo kho** |
| ⭐⭐ **Máy chọn sẵn ứng viên** | `55%` ca được chọn sẵn ⇒ dạy gật phản xạ | ✅ ⛔ **⛔ không chọn sẵn bất kỳ ca nào**, kể cả ca máy đề xuất |
| ⭐⭐ **`45%` ca lệch tiền trông GIỐNG ca khớp** | ⛔ không phân biệt | ✅ dải `warn` riêng · nút bỏ nền đặc · ⭐ **`Enter` khoá** · bấm **hai lần** |
| ⭐ **Diễn giải sao kê ⛔ không có chỗ** | `memo` `0/8.387` | ✅ là **cột ⛔ không bao giờ bị hy sinh**, có `<mark>` đánh dấu vendor *(`fls_dien_giai` **99,7%**)* |

#### ⓗ ⛔⛔⛔ BỐN CHỖ THIẾT KẾ **SAI SO VỚI CẤU TRÚC DỮ LIỆU THẬT** *(đo `21/09`)*

> ⛔⛔ **`ⓔ` và `ⓕ` đo *bản dựng*. Mục này đo *KHO*. Và nó lật một câu của chính `ⓕ`.**
> ⭐ Bài học ở tầng phương pháp: một bản dựng mang **dữ liệu mẫu** thì mọi thứ trông đã xong — vì người thiết kế gõ giá trị **đúng như nó nên là**, ⛔ không phải như nó **đang là**.

| # | Thiết kế GIẢ ĐỊNH | Kho THẬT | Hệ quả |
|:-:|---|---|---|
| ⭐⭐⭐ ① | Ngày lệnh chi là **ngày đọc được** *(`18/09/2026 09:14`)* | ⛔ **`45726.759012696755`** — sê-ri **`3.772/3.772`**, **`0`** dòng có dấu ngày | ⛔ Phép đổi sê-ri → ngày **⛔ CHƯA AI VIẾT**. ⚠ Và nó có bẫy: gốc sê-ri `1900` hay `1904` cho lệch **4 năm 1 ngày**, mà ⛔ không ô nào trên màn nói cho biết đã chọn gốc nào |
| ⭐⭐⭐ ② | *"Người nhận"* là **một trường riêng** | ⛔ `fls_pm_line` có **18 cột**, ⛔ **không cột nào** là người nhận. Nó là `tho['Tên tài khoản']` *(**3.771**)* | ⛔⛔ Và **chính ô ấy** cũng nằm trong khối *«Xem đủ trường»* dưới tên `Tên tài khoản` ⇒ **một sự thật, hai nhãn, hiện CÙNG LÚC** — đúng thứ `UI-F9` sinh ra để bắt, **tái phát** trong thiết kế mới |
| ⭐⭐ ③ | Chế độ **Toàn sổ** tính lại bậc ① bằng *"khớp số CT"* | ⛔ Bản dựng so **chuỗi THÔ** *(`ct === o.ct`)* | ⛔ `BA-07` cấm rõ: bậc `ma` phải tính bằng **`canon_ref` ở Python**, vì ITL chỉ có `doc_no` **thô**. **Đã đo**: `regexp` cho `560`, luật thật cho **`475`** ⇒ lệch **`17,9%`** |
| ⭐⭐ ④ | *"Nguồn"* và *"Số CT"* là **hai trường** | ⛔ Bản dựng **CẮT CHUỖI hiển thị** *(`meta.split(" · ")`, nhặt phần bắt đầu bằng `CT#`)* | ⛔ Cấu trúc ấy là **giả** — nó là hệ quả trực tiếp của `GAP-API-07 ⓐ`: `ung_vien[]` ⛔ chưa khai một trường nào, nên người dựng **⛔ không có gì để nhận** ngoài một chuỗi |

#### ⓘ ✅ Một chỗ tôi tưởng sai mà hoá **ĐÚNG** — và luật của nó vẫn phải viết

Thiết kế hiện **một** chiều `Nợ/Có` cho mỗi giao dịch. Đo `fls_itl`:

| | Dòng |
|---|--:|
| Mang **cả hai** ô `ps_no` ＋ `ps_co` | **3.691** *(44%)* |
| ⭐ Trong đó **cả hai đều khác `0`** | ⛔ **`0`** |
| Chỉ `ps_no` | 829 |
| Chỉ `ps_co` | 3.867 |

⇒ **"Một chiều" là ĐÚNG**, vì bên còn lại luôn bằng `0`. ⛔⛔ **Nhưng luật *"bên nào ≠ 0 thì đó là chiều"* ⛔ CHƯA VIẾT Ở ĐÂU** — và dự án **đã từng đọc nhầm cột này một lần** *(lấy dấu từ `pay_type` thay vì cột `Nợ/Có`)*. ⇒ Phải khai thành một dòng đặc tả, ⛔ không để dev suy lại.

#### ⓙ ⭐⭐ Dữ liệu cá nhân trên màn — **owner quyết `21/09`** *(`QĐ-ITL-148`)*

Ô *"Người nhận"* chứa **tên người thật** lẫn tên pháp nhân: `HA THU PHUONG` · `Do Nguyen Huy Hoang` · `Công Ty Bảo Hiểm Bưu Điện Thời Đại Số`. Ô `Chủ dự toán *` trong khối bung cũng là **tên người**.

⇒ ✅ **Owner chốt: HIỆN NGUYÊN.** Lý do: kế toán đang đọc **đúng ô ấy** trên Google Sheets hằng ngày, và nó là bằng chứng chính của nhánh ghép VN — che nó là **bắt họ quay về sheet**.

⭐⭐ **Và quyết định này VẼ RA một ranh giới mà bộ tài liệu ⛔ chưa từng vẽ:**

| Loại | Ví dụ | Luật |
|---|---|---|
| ⛔ **Hồ sơ nhân sự** | `Số CMND/CCCD/Passport` · `ID Employee` · khối nhân sự `9`…`14` | ⛔ **CẤM NẠP** — `QĐ-ITL-107`, mã đã siết *(`RE_TRUONG_CAM`)* |
| ✅ **Danh tính bên nhận tiền** | `Tên tài khoản` · `Chủ dự toán *` | ✅ **Nạp và HIỆN** — đây là **nội dung của khoản chi**, ⛔ không phải hồ sơ về một con người |

⚠ **Luật che vẫn ĐỨNG cho HIỆN VẬT xuất ra ngoài** *(bản dựng · ảnh chụp màn · tệp gửi đi)*: tên cá nhân rút còn chữ cái đầu, số tài khoản còn `4` số cuối. ⛔ Hai luật khác nhau cho **hai nơi khác nhau**, và lẫn chúng là cách một trong hai bị bỏ.

⭐⭐ **Và quyết định này ⛔ KHÔNG phải một luật mới — nó là một CA CỤ THỂ của `NFR-I13 ①`** *(owner phát biểu `17/09`: *"hệ **CÓ** mang một phần dữ liệu có thể chứa thông tin cá nhân, và đó là **quyết định có chủ đích**"*)*. ⛔ `NFR-I13` **đã đo** chính ô này: `Tên tài khoản` có `HA THU PHUONG` **896** lần. ⇒ Việc `21/09` chỉ là **nói rõ nó được HIỆN**, ⛔ không phải mở thêm phạm vi. ⚠ Nợ cũ **vẫn nguyên**: kho ⛔ chưa mã hoá cột, ⛔ chưa phân quyền theo hàng — `GAP-DB-07`.

#### ⓖ ⭐ Cái ĐÃ ĐO ĐƯỢC trong bản dựng — ⛔ không phải lời khai

⛔⛔ **Một hợp đồng thiết kế nói *"đã cài"* thì đó vẫn là một câu, ⛔ không phải một phép đo.** Bốn câu nặng nhất được soi thẳng vào `fls-gan-lenh-chi_10.html`:

| Câu trong hợp đồng | Soi ở đâu | Kết |
|---|---|---|
| `Enter` bị khoá khi lệch tiền | trình xử phím: `if(o && state.selectedCand!=null && exact(o, …)) doAssign(o)` | ✅ **đúng** — ⛔ không nhánh nào gán khi `exact` sai |
| Lệch tiền phải bấm **hai lần** | `doAssign`: `if(!exact(…) && !state.confirm){ state.confirm=true; return; }` | ✅ **đúng** |
| `đủ ↓` đo **sau khi dàn trang** | `soatCat()` so `scrollHeight` của ô diễn giải | ✅ **đúng** — ⛔ không đếm ký tự |
| ⛔ Không mã màu ngoài khối token | quét `#rrggbb` ／ `rgb(` ／ `hsl(` ngoài `:root` | ✅ **0 chỗ** — hợp `test_khong_ma_mau_go_tay` khi lên `fls/web/` |

⚠ **Một chỗ bản dựng TỰ VI PHẠM hợp đồng của nó:** `_10` che số tài khoản còn **4 số cuối** *(`••4001`)*, nhưng `man-gan-lenh-chi-v2.html` *(dữ liệu thật)* in **nguyên** số tài khoản *(`3759017445`)*. ⛔ Đây là **tài khoản công ty**, ⛔ không phải dữ liệu cá nhân *(tên người nhận **đã che** — `B. C. S. C. G.`)*, nên ⛔ không phải sự cố riêng tư; nhưng luật *"rút còn 4 số cuối"* là luật của chính hợp đồng ⇒ bản dựng thật phải theo.

---

#### ⓚ ⛔⛔⛔ Số sê-ri **VẪN CÒN** trên màn — đo `2026-09-22` trên **cửa thật**

`§4.5 ⓕ` khai *"✅ `Timestamp` thôi hiện `45813.49394`"*; `v3.9` đã đính chính rằng phép đo ấy đo **bản dựng** chứ ⛔ không đo kho. Nay mở BE ＋ FE và gọi cửa thật: `Timestamp` ra **`46091.42265217593`** ở **`3.772/3.772`** dòng, trong khối *«Xem đủ trường»*.

⭐⭐ **Đây là lần thứ HAI cùng một sai lầm, ở hai hình dạng khác nhau.** Lần đầu: đo bản dựng rồi tưởng đã đo kho. Lần này: **sửa lời khai mà ⛔ không kiểm lại đường đi thật của giá trị** — câu chữ đúng lên, còn con số vẫn chạy nguyên xi ra màn hình.

⇒ Đổi ở **tầng đọc** *(`KHOA_NGAY_SE_RI` trong `fls/repo/man_ghep.py`)*, dùng lại `ngay_tu_seri` — phép đổi **đã được đo** bằng một nguồn độc lập. ⛔ **Không** viết bản thứ hai bằng JS: làm thế là mở lại đúng câu hỏi *"nên là ngày nào"* mà dự án **đã trả lời bằng phép đo**.

⚠ **⛔ Không đổi được thì GIỮ NGUYÊN**, ⛔ không xoá: *"⛔ không đọc được"* khác *"⛔ không có"*, và một giá trị lạ phải **hiện ra** để người ta thấy chính cái lạ ấy.

#### ⓛ ⛔⛔ Màn **⛔ KHÔNG tự nạp danh sách** — lỗi cả hai cổng `B3` bỏ qua

Đo `2026-09-22` khi mở máy thật: `man_f01_ghep.js` **⛔ không hề có một dòng nào** gọi cửa lấy danh sách lệnh chi. Mở trên trình duyệt, màn **luôn** hiện *"Hàng chờ đã sạch."* — một câu **sai** trước `1.553` dòng đang chờ.

| Cổng | Vì sao nó ⛔ không thấy |
|---|---|
| `test_b3_fe_bam_thiet_ke.py` *(quét mã)* | ⛔ Nó ⛔ không hỏi *"danh sách lấy từ đâu"* |
| `test_b3_man_ghep_chay_duoc.py` *(chạy mã)* | ⛔⛔ **Khuôn thử TỰ NHÉT `ST.dong`** vào trước khi gọi `ve()` |

⭐⭐⭐ **Một khuôn thử cung cấp thứ mà bản thật phải tự đi lấy thì nó CHE MẤT chỗ thiếu ấy.** ⇒ Cổng thứ ba `test_b3_man_ghep_tu_nap_danh_sach.py` **⛔ KHÔNG gán `ST.dong`** một lần nào; **diễn tập phá**: gỡ lời gọi nạp ⇒ `3` bài mới **ĐỎ**, hai cổng cũ vẫn **XANH**.

⛔ Và chỉ **`2/4`** chip có cửa *(`GAP-API-08`)* — màn **NÓI RA** điều đó thay vì vẽ một danh sách rỗng, vì một danh sách rỗng đọc **y hệt** *"đã xong hết"* (`INV-I16`).

#### ⓜ ⛔⛔⛔ BỐN lỗi CHẶN — và **ba** cổng đều xanh suốt thời gian ấy

Kiểm **độc lập** `2026-09-22` *(đối chiếu mã ↔ hợp đồng ↔ bản dựng)* tìm ra bốn đường đi **⛔ không dùng được** trên trình duyệt. Cả bốn cùng **một hình dạng**:

| # | Lỗi | Vì sao cổng ⛔ không thấy |
|:-:|---|---|
| ① | `ST.dong` — ⛔ không ai gọi cửa nạp danh sách | khuôn thử **tự nhét** `ST.dong` |
| ② | `phim()` viết đủ `9` phím, ⛔ không ai đăng ký `keydown` | khuôn thử **gọi thẳng** `F01G.phim(…)` |
| ③ | `#ghep-tim` — ô nhập có trong vỏ, ⛔ không ai nghe `input` | ⛔ không cổng nào hỏi *"ai đọc ô này"* |
| ④ | `bo_gan` đọc `itl_id_da_gan` — khoá **⛔ không ai sinh ra** | nhánh *"đã gán"* **⛔ chưa bao giờ bật** nên ⛔ không ai tới được nút ấy |

⭐⭐⭐ **Gốc chung: bài thử với tay VÀO gọi thứ mà sản phẩm phải với tay RA nối.** Một khuôn thử cung cấp thứ bản thật phải tự đi lấy thì nó **che mất** chỗ thiếu ấy.

⇒ Cổng `tests/web/test_moi_o_nhap_deu_co_nguoi_nghe.py` đo **chiều ngược lại**: một phần tử **tồn tại trong vỏ** thì phải có mã chạm tới, và một **ô nhập** thì phải có ai **nghe** hoặc **đọc giá trị**. ⭐ *Một ô nhập chỉ được nhảy vào mà ⛔ không được đọc còn **tệ hơn** một ô ⛔ không có: nó **MỜI** người ta gõ.*

⚠ Cổng ấy **⛔ không thay được** một cổng CHẠY — nó vẫn là phép quét chữ. Nó là **lưới thưa**: bắt chỗ **quên hẳn**; còn *"nối nhưng nối sai"* thì phải là một bài chạy.

#### ⓝ ⭐⭐ Hai lỗi **hình dạng** lộ ra khi dựng `đủ ↓`

⛔ **Nút lồng nút.** Bản đầu dựng `đủ ↓` bằng `<button>` **nằm trong** `<button class="cand">` — HTML **⛔ không hợp lệ**, trình duyệt thật ⛔ không xử lý được nút trong, còn **DOM giả cho chạy ngon lành**. ⇒ Đây là lớp lỗi một **bài chạy ⛔ KHÔNG THỂ** bắt *(nó ⛔ không phân tích HTML)*; phải đo ở **mã nguồn**. ⭐ Bản dựng đã giải đúng chỗ này: `<span role="button" tabindex="0" data-mo=…>` ＋ bắt click ở **nút ngoài** qua `closest`.

⛔ **Đụng tên lớp.** `.mo` đã mang nghĩa *"dòng sổ đang mở"* (`.mrow.mo`) ⇒ `querySelectorAll('.mo')` trả **cả hai**, và bài thử **lặng lẽ đo nhầm phần tử**. Đổi thành `.doc-du`.

#### ⓞ ⭐⭐⭐ HAI VIEW — bảng sổ ⇄ rail ＋ bàn làm việc

Hợp đồng `§4` khai **hai** view, chuyển qua lại bằng *"đã mở lệnh nào chưa"*. Màn `21/09`→`22/09` **⛔ chỉ có một**: luôn là rail ＋ bàn làm việc, kể cả khi ⛔ chưa chọn gì.

| | Wireframe | Màn trước `22/09` |
|---|---|---|
| ⛔ Chưa mở lệnh | **bảng sổ `12` cột**, toàn bề ngang | rail `380px` ＋ một câu *"Chọn một lệnh chi bên trái"* chiếm phần còn lại |
| Đã mở lệnh | rail ＋ bàn làm việc | *(giống)* |

⛔⛔ **Hệ quả đo được:** lúc mở màn, phần lớn bề ngang là một **lời nhắc**, còn danh sách bị nén vào một cột ⛔ **không đủ chỗ** cho `Ngày` · `Loại` · `CDT` · `Số CT`. ⭐ Bảng cho người **QUÉT** cả trăm dòng; rail cho người **đang làm một dòng** — hai việc khác nhau, hai hình.

⭐ **Mười hai cột**, nguyên văn bản dựng: `Ngày · Mã PM · Loại · Nội dung · CDT · Số tiền · Trạng thái · Số CT · → · Giao dịch đã gán · Số tiền GD · Bậc`. ⛔ Cột `→` *(`20px`)* là một **cột thật**: nó chia bảng thành **bên lệnh chi** ＋ **bên giao dịch**, và đó là toàn bộ câu hỏi của màn này.

⭐ **Rail ba dòng**: *(ngày · mã · loại ∣ chip trạng thái)* / *(nội dung ∣ tiền)* / *CDT*. Bản trước có **3 mục trên một dòng** ⇒ mất `Ngày`, `Loại`, chip trạng thái, `CDT` — người đang ghép phải **mở từng dòng ra mới biết dòng nào đáng mở**.

#### ⓟ ⛔⛔ Ba cột cuối cần một phép nối **⛔ CHƯA có ở cửa**

Đo `22/09`: `ung_vien_itl` = `[47298]` · `itl_da_gan` = `[28338]` — **chỉ ID**. ⛔ Không cửa nào chở `diễn giải` · `số tiền` · `bậc` của giao dịch, mà ba cột cuối cần đúng thứ đó. Tra từng dòng là **`738` lượt gọi cửa** cho một lần mở màn.

⇒ `lc.gd_theo_itl()` — **một** truy vấn cho **cả trang**, dùng lại **đúng** `_SQL_ITL_THEO_ID` mà bậc `ma` đang dùng. ⛔ Viết câu thứ hai là tạo **bản sự thật thứ hai** về *"một dòng tiền trông thế nào"*.

⭐⭐ **Và bậc tính ở tầng cửa, ⛔ không ở JS**: phép chia bậc dùng `canon_ref`, và một bản thứ hai bằng JS sẽ lệch **đúng ở chỗ nó hay lệch nhất** *(đã đo: `regexp` trong SQL lệch **`17,9%`** so với `canon_ref`)*.

⛔⛔⛔ **Một dòng hỏng ⛔ KHÔNG được làm sập cả trang.** `tach_nguon` **ném** khi `source_sheet` sai khuôn — đúng ở tầng đọc *(`INV-I16`)*. ⛔ Nhưng trong một **danh sách**, một ngoại lệ trả `500` cho cả trang ⇒ kế toán mất **cả `738` dòng** vì **một** dòng. ⇒ Ô ấy nói *"⛔ không đọc được nguồn"*, và `loi_nguon` vốn **đã là một trong ba đường ra** của `DUONG_RA` — một trạng thái **đã có tên**, ⛔ không phải một chỗ vá.

⭐ Ô `Giao dịch đã gán` nói **năm** câu khác nhau: *đã gán* · *đề xuất* *(viền **đứt** ＋ nền warn — `§6.3`)* · *sổ ⛔ không có số tiền này* · *⛔ không đọc được nguồn* · *— chưa chọn*.

⭐ *(v4.16, `KQ-036 F-6` — `BA-07` **v3.9** `§4g ⓹`)* **Câu thứ sáu:** dòng `gd = null` mang `vi_sao = ma_khop_khac_tien_te` ⇒ ô in **chính câu `vi_sao` của cửa** *(nó nói mã tiền tệ của dòng khớp)*, ⛔ *"— chưa chọn"* — đó là **84** lệnh sổ thật hôm nay *(trước: *"đề xuất: …"* một dòng tiền khác tiền tệ)*. ⛔ Một câu màn tự ghép; chữ ⛔ `--faint` *(câu mang nghĩa — `NFR-I29`)*. Trên `F01L` câu `vi_sao` đã in sẵn ở `hint` dưới mã lệnh *(`man_f01_lenh.js:416`)* ⇒ ⛔ đổi.

⭐ *(v4.17, `TL-038` — `HOI-038` phương án **B**)* **Câu thứ sáu đọc `the.vi_sao`** *(`BA-07` **v3.10** `§4h ⓵'`)*: khoá ấy **chỉ có mặt** ở đúng nhánh *khớp mã chỉ ở tiền tệ khác* ⇒ màn in khi `gd = null` **và** `the.vi_sao` có — ⛔ tự nhận câu nào là câu thứ sáu *(so chuỗi hay chép điều kiện `ro`/mã ở JS — luật thứ hai, `ⓟ` cấm)*. Tập: **84** ô sổ thật, ⛔ **616** *(532 lệnh ⛔ số chứng từ **giữ** *"— chưa chọn"*: ô ấy là cột *Giao dịch*, và *"chưa có giao dịch nào được chọn"* là câu **đúng** cho chúng; câu vì sao của chúng đã ở `F01L`)*. ⚠ Đính chính `WO-037 (g)`: chữ *"`vi_sao` có"* đọc là **`the.vi_sao` có**.

#### ⓤ ⭐ `F01L` băng *"Việc của bạn hôm nay"* + bảng rổ — rổ `nguoi` có **hai** loại lệnh *(v4.17, `TL-038` — `BG-039` yếu #1)*

⛔ **Câu đang in sai sự thật.** Sau `WO-037` rổ `nguoi` gồm lệnh **⛔ số chứng từ** *(câu `khong_co_so_chung_tu`)* **và** lệnh có số chứng từ khớp một dòng tiền **tiền tệ khác** *(câu `ma_khop_khac_tien_te`)*. Băng in *"Chưa có số chứng từ. Đây là việc thật của kế toán."* cho cả rổ ⇒ sai **84 / 616** lệnh *(`fls-ba` 02/10, sổ thật chỉ đọc, hàm thật `xep_ro` mọi trang: `nguoi` **616** = ⛔ mã **532** ＋ khớp mã khác tệ **84**)*. Và dòng ⚠ *"N dòng khớp số chứng từ nhưng **lệch tiền**"* *(`may − tu_chung`)* sai cho **42 / 120** lệnh: đo cùng lượt trên **120** lệnh `may` ⛔ tự chứng — **một** dòng cùng tệ lệch tiền **52** · ≥ 2 dòng, mọi dòng lệch **26** · ⭐ **một** dòng cùng tệ **khớp đúng tiền** mà cửa ghi vẫn ⛔ nhận theo lô **39** · ≥ 2 dòng có dòng khớp tiền **3** ⇒ *"lệch tiền"* đúng **78 / 120**. *(Cổng nào của cửa ghi giữ 39 lệnh ấy: **chưa đo** — câu mới ⛔ khẳng định.)*

Chữ **nguyên văn** *(so chuỗi; `<n>` = `TP.so(...)` của số **cửa** trả — ⛔ màn đếm; ⛔ ký hiệu `⛔ ⚠ ⭐ 🔒` — luật `test_luat_ky_hieu_man_hinh.py`)*:

| Chỗ | Chữ v4.17 | Số từ đâu |
|---|---|---|
| băng · dòng 2 · tiêu đề | `CẦN BẠN tra — máy chưa đề xuất được dòng tiền` | — |
| băng · dòng 2 · `hint` câu ① | `<a> dòng chưa có số chứng từ: tra bằng tiền + ngày.` | `a = nguoi − nguoi_khac_tien_te` *(`/lenh-cho/ro`)* |
| băng · dòng 2 · `hint` câu ② *(chỉ khi `b > 0`)* | ` <b> dòng có số chứng từ nhưng dòng tiền khớp mang tiền tệ khác: cửa ghi chưa ghép được hai tiền tệ.` *(mở đầu một dấu cách)* | `b = nguoi_khac_tien_te` |
| băng · dòng ghi chú `note warn` *(khi `c > 0`)* | `Còn <c> dòng khớp số chứng từ cùng tiền tệ nhưng cửa ghi chưa nhận theo lô — lệch tiền, nhiều dòng tiền cùng mã, hoặc vướng một cổng khác của cửa ghi. Phải mở từng dòng.` ＋ liên kết `Xem <c> dòng` *(như cũ)* | `c = may − tu_chung` *(như cũ)* |
| bảng rổ · hàng `nguoi` · *Nghĩa là gì* | `Máy chưa đề xuất được dòng tiền — chưa có số chứng từ, hoặc số chứng từ khớp một dòng tiền bằng tiền tệ khác. Mỗi dòng nói vì sao.` | — |

Chip *(`<nguoi> dòng`)*, nút *Bắt đầu tra* *(lọc `?ro=nguoi` — cả hai loại; mỗi hàng đã in `vi_sao` ở `hint`)*, dòng 1 + dòng 3 của băng, hàng `may`/`khong` của bảng rổ: **⛔ đổi**. Sổ thật hôm nay: `a` **532** · `b` **84** · `c` **120** *(ảnh trôi theo nhịp — Dev đo lại, cùng ảnh)*.

**Năm trạng thái** *(băng `ve_viec`, `TT.chay`)*: tải · lỗi · mất kết nối **⛔ đổi**; **rỗng** *(`tong = 0`)* ⛔ đổi; **có dữ liệu** = bảng trên. Ca biên: `b = 0` ⇒ `hint` chỉ câu ①; `a = 0 ∧ b > 0` ⇒ câu ① in `0 dòng chưa có số chứng từ…` *(⛔ giấu — một con số `0` là một câu trả lời)*.

⭐ *(v4.18, `KQ-041 F-1` — `fls-test` 05/10)* **Ba chỗ khác của `F01L` vẫn hứa *"lệch tiền"* / *"chỉ DUYỆT"* cho cả rổ `may`, và câu ghi chú v4.17 gọi sai tên một cổng.** Đo *(`KQ-041` lăng kính **Dữ liệu** — sổ thật chỉ đọc, gọi **hàm thật** `ds_tu_chung`, ảnh `NAP-2026-10-02-PMA07ED283`)*: rổ `may` **184** = tự chứng **64** ＋ cửa ghi ⛔ nhận theo lô **120**. Trong **120**: **một** dòng cùng tệ lệch tiền **52** · ≥ 2 dòng cùng tệ, mọi dòng lệch **26** · ≥ 2 dòng có dòng khớp tiền **3** · **một** dòng cùng tệ **khớp đúng tiền 39** — cửa ghi giữ vì `chum_lech_tien` **25** *(mã của dòng tiền khớp **nhiều dòng LỆNH** cùng ảnh, Σ cả chùm ≠ tiền bank — vd. `PM00028-8` ↔ `itl 28857`)* ＋ `co_dong_chua_duyet` **14** *(một dòng lệnh **khác** cùng chùm ⛔ `Approve` — vd. `PM00415-3`)*. ⇒ *"lệch tiền"* đúng **78 / 120**; *"khớp đúng một dòng tiền"* sai **≥ 29 / 184**; *"người chỉ DUYỆT"* sai **120 / 184**; câu v4.17 *"nhiều dòng tiền cùng mã"* đúng cho **29**, còn **25** là nhiều dòng **lệnh** cùng mã.

| Chỗ *(`man_f01_lenh.js`)* | Chữ cũ *(biên bản)* | Chữ v4.18 *(nguyên văn — so `textContent`; `<t>` = `TP.so(tu_chung)`, `<c>` = `TP.so(may − tu_chung)` của **cửa** `/lenh-cho/ro`)* |
|---|---|---|
| ⓐ băng · dòng ghi chú `note warn` *(khi `c > 0`)* — **thay** chữ v4.17 | `Còn <c> dòng khớp số chứng từ cùng tiền tệ nhưng cửa ghi chưa nhận theo lô — lệch tiền, nhiều dòng tiền cùng mã, hoặc vướng một cổng khác của cửa ghi. Phải mở từng dòng.` | `Còn <c> dòng` ＋ **`LY_DO_LO`** ＋ ` Phải mở từng dòng. ` ＋ liên kết `Xem <c> dòng` *(như cũ)* |
| ⓑ dưới bảng rổ *(khối Số liệu kiểm chứng)* · `note ok` *(khi `t > 0`)* | `⭐ Trong rổ “máy trả lời được” có <t> dòng TỰ CHỨNG — … <c> dòng còn lại khớp số chứng từ nhưng lệch tiền, và chúng ⛔ KHÔNG được ghép theo lô: …` | `Trong rổ “máy trả lời được” có <t> dòng tự chứng — khớp cả số chứng từ, số tiền và tiền tệ; cửa ghi nhận chúng theo lô. Còn <c> dòng` ＋ **`LY_DO_LO`** ＋ ` Phải mở từng dòng.` |
| ⓒ thanh lọc khi đang xem rổ `may` ⛔ tự chứng *(`ST.tu_chung === false`)* | `đang xem rổ: máy trả lời được · chỉ LỆCH TIỀN` | `đang xem rổ: máy trả lời được · chỉ CHƯA NHẬN THEO LÔ` |
| ⓓ bảng rổ · hàng `may` · *Nghĩa là gì* | `Số chứng từ khớp đúng một dòng tiền trong sổ — người chỉ DUYỆT.` | `Số chứng từ khớp ít nhất một dòng tiền cùng tiền tệ — máy đề xuất được dòng tiền. Dòng tự chứng được duyệt theo lô; các dòng còn lại phải mở từng dòng.` |

**`LY_DO_LO`** *(**một** hằng, dùng ở ⓐ và ⓑ — ⛔ hai bản gõ; mở đầu một dấu cách)*: ` khớp số chứng từ cùng tiền tệ nhưng cửa ghi chưa nhận theo lô — lệch tiền, nhiều dòng tiền cùng mã, một dòng tiền mang mã của nhiều dòng lệnh mà tổng các dòng lệnh khác tiền bank, có dòng lệnh cùng chùm chưa được duyệt, hoặc vướng một cổng khác của cửa ghi.`

Vì sao từng vế *(phủ **120 / 120** hôm nay)*: *lệch tiền* **52 ＋ 26** · *nhiều dòng tiền cùng mã* **26 ＋ 3** · *một dòng tiền mang mã của nhiều dòng lệnh* **25** · *dòng lệnh cùng chùm chưa duyệt* **14** · *cổng khác* — cửa ghi `ds_tu_chung` còn lý do `ung_vien_da_bi_ghep` *(hôm nay **0** trong nhóm)*; giữ vế ấy để câu ⛔ khẳng định thiếu khi sổ đổi. Bốn chuỗi **0** ký tự `CAM` *(ⓑ cũ mang `⭐` + `⛔` ×1)*. ⛔ Đổi: dòng 1/2/3 băng, hàng `nguoi`/`khong` bảng rổ, `RO.khong` *(còn `⛔` — nợ `THEO_LUAT`)*.

⚠ **Câu chung, ⛔ câu từng hàng.** Hàng của 120 lệnh ấy hôm nay ⛔ nói vì sao *(`xep_ro` đặt `vi_sao = ""` cho mọi lệnh rổ `may` — `lenh_cho.py:676`; lý do có sẵn trong `ds_tu_chung` theo `itl_id` mà ⛔ cửa đọc nào chở)* ⇒ **`GAP-SCR-34`** *(mới 05/10)*: người mở một trong **39** lệnh *"khớp đúng tiền"* ⛔ biết vì sao ⛔ duyệt được. Cần một khoá cửa mới ⇒ phiếu sau, ⛔ trong `WO-042`. Mã ⇒ **`WO-042` `(b)`**.

#### ⓥ ⭐ `F01G` `②b` — đổi chip khi danh sách **đang tải**: lượt **MỚI NHẤT** thắng *(v4.18, `KQ-041 F-3` `NANG`)*

⛔ **Hôm nay** *(`man_f01_ghep.js:890` `tai_danh_sach`, có từ `9ed4d4a` 22/09)*: mỗi cú bấm chip mở một lượt tải, gán `ST.dong = []` **mới**, trong khi lượt cũ vẫn đang `await` rồi `push` vào **mảng của lượt mới**. Đo `KQ-041` *(8088 sổ thật chỉ đọc, chuột thật)*: bấm `Đã gán` trong ~1,2 s đầu ⇒ chip in **`2955 dòng`** = **2.219** đã gán ＋ **736** chưa gán *(đối chứng đợi tải xong: `2219 dòng`)*; bấm lại chip đang chọn `Chưa gán` khi đang tải ⇒ **1.472** = 736 × 2, mạng **6** `GET` *(mỗi đường hai lần)*. Cửa ghi vẫn chặn ⇒ **0** ghi sai; hại là **một con số sai** và **rổ trộn** trên đúng màn của vòng ghép thật đầu tiên. ⛔ Bài nào thấy: cửa giả `khung_node` trả lời **ngay** — lần thứ tư của lớp *"khuôn thử nhanh hơn đời thật"* *(`KQ-002 F-3` cùng hàm)*.

| Luật | Hành vi |
|---|---|
| ① đổi sang chip **khác** khi đang tải | lượt cũ bị **bỏ**: kết quả của nó ⛔ vào `ST.dong`, ⛔ tắt cờ *đang tải*, lỗi của nó ⛔ hiện, ⛔ đặt con trỏ trang. Màn chỉ in kết quả của lượt **mới nhất**; số dòng chip = số hàng cửa của chip ấy trả |
| ② bấm lại chip **đang chọn** khi đang tải | ⛔ mở lượt mới *(**0** `GET` thêm)*; lượt đang chạy đi tiếp |
| ③ lượt mới nhất xong / rỗng / lỗi / mất kết nối | năm trạng thái như cũ *(tải · rỗng · lỗi · mất kết nối · có dữ liệu)* — **chỉ** của lượt ấy; khung *tải* giữ tới khi **nó** xong |
| ④ đổi chip nhiều lần liên tiếp | sau lần cuối, màn = chip cuối; ⛔ một hàng nào của chip trước |

⛔ Huỷ hẳn yêu cầu mạng của lượt cũ *(`AbortController`)* **⛔ bắt buộc** — đổi `goi_cua.js` là việc khác; luật chỉ đòi kết quả cũ **⛔ được dùng**. Cách làm *(số lượt, mã lượt…)* là việc Dev. Bài thử phải dựng độ trễ **có kiểm soát** *(cửa giả chậm, CDP giữ phản hồi)* — ⛔ một bài *"bấm nhanh rồi mong"*. Mã ⇒ **`WO-042` `(a)`**.

⭐ **Đoạn v4.19** *(2026-10-05, `TL-043` — `HOI-043` của `fls-dev`)*: hai chỗ bảng trên **⛔ nói**, đo được khi Dev làm `WO-042`:
- **① thêm:** lượt **bị thay** **được dừng ngay** ở lần chờ cửa kế tiếp — ⛔ bắt buộc xin tiếp trang / cửa còn lại cho một kết quả sẽ bị vứt *(cửa thật ~0,9 s/trang — `KQ-041`)*; cũng ⛔ cấm đi tiếp. Luật chỉ đòi kết quả của nó **⛔ được dùng**. ⇒ Bài thử ⛔ được đếm *"lượt cũ đã gọi đủ N cửa"* làm điều kiện *"đo được"*; đếm **mỗi chip đã có ít nhất một lượt bay** *(theo đường)*.
- **⑤ mới — `Thử lại` của `②b`.** Đo 05/10 *(`Đ1`)*: nhánh lỗi `②b` chỉ in `banner crit` *"⛔ Cửa lỗi: <câu>"* *(`man_f01_ghep.js:1473`)*, chữ `Thử lại` trong tệp **0** chỗ ⇒ đường thử lại duy nhất là **bấm lại chip đang chọn** *(khi ⛔ đang tải — `:991`)*, và màn **⛔ nói** điều ấy. Luật: trạng thái **lỗi** và **mất kết nối** của `②b` có **nút `Thử lại`** ngay dưới câu lỗi *(lớp nút `b tiny` có sẵn — cùng lớp **mọi** nút nhỏ của màn ghép, `nut('tiny', …)`; ⛔ token, ⛔ lớp CSS mới. ⭐ **Đính chính v4.21** *(`TL-049`)*: bản v4.19 viết thêm *"cùng dáng nút của khung `TT.chay` `trang_thai.js:78`"* — **sai**: nút `Thử lại` của `TT.loi` mang lớp **`b`** *(`trang_thai.js:76`, cỡ thường + `marginTop 10px`)*, ⛔ `b tiny`. Chữ **lớp** thắng: `②b` là danh sách trong màn ghép, nút đứng cạnh các nút `tiny` khác; ⛔ mượn dáng của khung lỗi **cả màn**)*; bấm ⇒ tải lại **chip đang chọn** = cùng đường với bấm lại chip *(một lượt mới theo `ⓥ`)*. ⛔ Đổi câu lỗi. Mã ⇒ **`WO-045` `(e)`** *(⛔ `WO-042` — phiếu ấy viết "+ `Thử lại`" là lỗi viết phiếu, đính chính ở `TL-043`)*.

#### ⓦ ⭐ Luật `ⓥ` cho **mọi** lượt tải ghi trạng thái chung của màn · chế độ **chỉ đọc** khoá **chỉ** thao tác GHI *(v4.19, `BG-044` `(d)` + phát hiện ngoài phạm vi)*

**① Lượt mới nhất thắng — ở mọi màn.** `BG-044` `(d)` *(Dev đọc mã 05/10 — ⛔ đo)*: **21** hàm trong `fls/web/tep/*.js` `await` cửa rồi ghi trạng thái dùng chung; **5** có chống chồng, **16** ⛔. Luật `ⓥ` ①…④ áp cho mọi hàm **đọc** sau đây — kết quả của lượt **đã bị thay** *(cùng hàm, tham số khác — lệnh khác, rổ khác, lọc khác, ảnh khác)* ⛔ được ghi vào trạng thái, ⛔ được vẽ, lỗi của nó ⛔ hiện:

| Ưu tiên | Màn · hàm *(`BG-044` `(d)` #)* | Vì sao ở mức này | Mong sau khi sửa |
|:-:|---|---|---|
| ① | `F01G` `mo_lenh` *(#2)* · `tai_toan_so` *(#3)* | đổi lệnh bằng `j`/`k`/`↓` hoặc gõ ô tìm *(trễ `TRE_TIM` 250 ms ⇒ hai lượt bay — chú thích `:129-132` tự nêu)* ⇒ ứng viên của lệnh **trước** / chữ **cũ** đè lên lệnh đang mở *(`ST.mo` đã là lệnh mới)*; `gan` gửi `itl_id` lấy từ **chính** danh sách ấy kèm `ma_lenh` **đang mở** *(`:653-661`)* ⇒ chỗ **duy nhất** trong 21 đứng sát một cú **GHI** của vòng ghép thật. Cửa ghi còn chặn lệch tiền / khác tệ, nhưng một cặp sai mà **trong dung sai** ⛔ bị chặn *(chưa đo)* | ứng viên trên màn **luôn** là của `ST.mo`; ⛔ cú `Gán` nào gửi `itl_id` của lệnh khác |
| ② | `F01L` `_loc` → `ve_luoi` / `_ve_luoi` *(#6)* · `Xem thêm` *(#7)* | **cùng hình `F-3`** trên màn chung tab `② Hàng chờ`: `_loc` đặt `ST.dong = []`, lượt rổ trước về sau **nối** vào ⇒ lưới trộn hai rổ; `Xem thêm` bấm hai lần ⇒ hai lượt cùng con trỏ ⇒ hàng lặp | lưới chỉ mang hàng của rổ / lọc **đang hiện**; `Xem thêm` ⛔ mở lượt thứ hai khi lượt trước còn bay *(như `F02` `:369` — nút khoá trong lúc chờ)* |
| ③ | `F01` hàng chờ `ve_luoi` *(#10)* · `_xem_them` *(#11)* | đổi lọc tiền tệ / `den_pct` lúc đang tải ⇒ lọc cũ thắng; cùng lỗi `Xem thêm` | như ② |
| ④ | `F04` `_mo_chup` *(#17)* · `_ve_thu_tu` *(#18)* | mở hai ảnh chụp nhanh ⇒ ảnh **trước** về sau thắng; màn vẽ và `S.chup` cùng từ một lượt ⇒ **nhất quán** với nhau *(`Nhận` gửi đúng ảnh đang **hiện**)*, chỉ sai so với **cú bấm cuối** — nhẹ nhất | màn = ảnh bấm **cuối**; `S.chup` / `S.thu_tu` cùng ảnh ấy |

⛔ Ngoài luật này *(lớp khác)*: bấm **GHI** hai lần *(#4 `gan` · #16 `_ghi_mot_o` · #19 `_soat` · #20 `_nhan`)* — đó là *"khoá nút trong lúc chờ cửa ghi"*, nhà của nó là lớp hộp chờ cửa / mã `409` *(`WO-023`)*; hộp mở muộn *(#8 · #12)* — hộp tự mang danh tính dòng, ⛔ trộn; #13 · #21 một nơi gọi. ⛔ `AbortController` *(như `ⓥ`)*.

**② Chế độ chỉ đọc khoá chỉ thao tác GHI.** `BA-08` `NFR-I03`: *"`--cho-ghi` mặc định **TẮT** ⇒ mọi đường **ghi** trả `405`"* — luật nói về đường **ghi**. Đo 05/10 *(`BG-044`, 8097 sổ thật chỉ đọc; `fls-ba` đọc lại mã)*: `F01L` dựng **mọi** nút bằng `_nut` *(`man_f01_lenh.js:69`)* ⇒ `_chan_ghi` *(`:61`)* khoá cả hai nút **đọc**: `Xem thêm` *(`:544`)* và `Tìm tiền` mỗi hàng *(`:491` — mở hộp xem ứng viên)*. Lưới trang **50** *(`:554`)* ⇒ ở chế độ mặc định mỗi rổ chỉ thấy **50** dòng đầu: `may` chưa nhận theo lô **50 / 120** · `nguoi` **50 / 616** · `khong` **50 / 801** *(số `/ro` sổ thật, `BG-044` `AC-7`)* — và nút xám mang câu *"Mọi thao tác ghi bị trả 405"* cho một thao tác **⛔ ghi**. Ai bị: **mọi** người mở sổ thật ⛔ bật ghi — owner xem & quyết, kế toán tra trước khi ghép, mọi phép đo của `fls-test`/`fls-ba` trên 8088 *(`WO-042` `AC-7` chỉ đo được trang đầu)*. Kế toán ghép thật chạy `--cho-ghi` ⇒ ⛔ bị. Màn `F01` *(`man_f01.js:168` — `Xem thêm` gắn `onclick` thẳng)* ⛔ có lỗi này ⇒ đây là lệch **giữa hai màn**, ⛔ chủ ý.

| Thao tác | Chế độ chỉ đọc |
|---|---|
| `Xem thêm` *(lật trang)* · `Xem <c> dòng` · lọc · chip | **chạy** *(đọc)* |
| `Tìm tiền` *(mở hộp ứng viên)* | **chạy** — hộp mở, xem được ứng viên; nút **`Ghép`** trong hộp khoá + câu `405` như nay |
| `Ghép` · `Gán` · `Bỏ gán` · `Lý do` · `Hoãn` · `Xong` · `Mở lại` · `Ghép N dòng tự chứng` | **khoá** + câu `405` như nay — ⚠ *(đính chính v4.23, `ⓦ` ⑧ ⓑ)*: *"như nay"* đúng ở `F01L`; `F01G` `Gán` · `Bỏ gán` hôm nay **⛔ khoá** ⇒ **`WO-060`** ⓑ |

⛔ Đổi câu `405`, ⛔ đổi `NFR-I03` *(đường ghi vẫn `405` ở cửa — luật này chỉ sửa **màn** khoá thừa)*. Mã ⇒ **`WO-045`**.

**③ Chữ trên nút ⛔ mang số đo cứng** *(v4.20, `KQ-046 F-3` — `fls-test` 05/10)*. Thanh lằn `F01` *(`man_f01.js:766`, `_thanh_lan`)*: `title` nút `Theo LỆNH CHI` = *"1.345 dòng lệnh đang chờ tiền — câu hỏi của việc (QĐ-ITL-122)"* — **1.345** là số đo **09/09** gõ vào mã; sổ thật hôm nay `/lenh-cho/ro` `tong` **1.601** *(và ⛔ cùng định nghĩa — `tong` đếm lệnh **chưa nhận**, ⛔ "dòng đang chờ tiền")*. Màn in một con số **⛔ ai đo lại** — cùng họ `UI-F8` *(số của máy ⛔ lên màn người)*; con số sẽ sai thêm mỗi lần nạp.

| Phương án | Cái giá | |
|---|---|:-:|
| ⓐ **Bỏ số** — `title` = `Lệnh chi đang chờ tiền — câu hỏi của việc (QĐ-ITL-122)` | mất cỡ của việc trong `title` — nhưng cỡ đã có **ở chính lằn** *(băng `F01L` đọc `/lenh-cho/ro` mỗi lần vẽ)* | ⭐ |
| ⓑ Đọc số từ cửa `/lenh-cho/ro` | thêm **1** `GET` mỗi lần vẽ thanh lằn *(`F01L` đã gọi `/ro` **3** lần mỗi lần vẽ — `KQ-046`)*; phải chọn **định nghĩa** đếm *(`tong` 1.601 ≠ "dòng đang chờ tiền")* — một câu nghĩa mới cho một tooltip | |

⇒ **ⓐ**: chuỗi `title` nguyên văn trên; ⛔ chữ số nào trong `title` hai nút thanh lằn **ngoài mã quyết định `QĐ-ITL-<n>`** *(nút `Theo dòng tiền` hôm nay đã ⛔ có số — giữ)*. ⭐ **Đính chính v4.21** *(`TL-049`)*: v4.20 viết *"⛔ chữ số nào"* trơn — mâu thuẫn với chính chuỗi ⓐ *(mã `QĐ-ITL-122` mang **3** chữ số — `HOI-049`)*. Luật là **⛔ số đo cứng**; mã quyết định là **tên** của một lời chốt, ⛔ số đo — ⛔ trôi khi sổ đổi ⇒ **giữ** trên nút làm dấu vết. Phép đo: bỏ mọi `QĐ-ITL-\d+` rồi đếm `/[0-9]/` ⇒ **0**. ⛔ Đổi nhãn nút, ⛔ đổi `ST.lan`. Chú thích mã cạnh đó *(`man_f01.js:756-758` "**7.682** · **1.345** · **69**")* là **bia** đo 09/09 — **giữ** *(`Đ2`: biên bản, ⛔ chữ in)*. Mã ⇒ **`WO-045` ⑤**.

**④ Vùng ứng viên `F01G` — năm trạng thái** *(v4.21, `TL-049` — `BG-048` mục yếu 2)*. Trước `WO-045` vùng này ⛔ có khung **tải** / **lỗi**: lượt ứng viên ghi `ST.ung_vien` rồi vẽ, lỗi ném ra ngoài. `WO-045` ① *(xoá ngay danh sách lệnh cũ khi đổi lệnh)* buộc vùng ấy có hai khung mới; Dev dựng bằng **đúng** chữ + lớp của danh sách lệnh `②b` *(`man_f01_ghep.js:1618-1621` @ `2b804e3`)*. ⇒ **Phê chuẩn**: một màn **một giọng** cho cùng một trạng thái — người vừa thấy `Đang hỏi sổ…` ở danh sách lệnh đọc được ngay cùng câu ở vùng ứng viên; ⛔ chữ mới, ⛔ lớp mới.

| Trạng thái | Vùng `.cands` *(dưới hàng tên cột `ve_dau_gd`)* | Dải *Toàn sổ* + chú giải | Mã |
|---|---|---|---|
| tải *(lượt **mới nhất** đang bay)* | `banner info` `Đang hỏi sổ…` | ⛔ | ✅ `WO-045` |
| rỗng | `banner crit` `Sổ không có dòng tiền nào.` *(như nay)* | dải *Toàn sổ* như nay; ⛔ chú giải | ✅ có sẵn |
| lỗi | `banner crit` `⛔ Cửa lỗi: <e.cau>` ＋ ⭐ nút **`Thử lại`** lớp `b tiny` ngay dưới ⇒ chạy lại **đúng** lượt vừa lỗi *(ô tìm rỗng ⇒ `mo_lenh(ST.mo)`; ô tìm có chữ ⇒ tra lại chữ ấy — ⛔ xoá chữ người đã gõ)*; một lượt mới theo `ⓥ` | ⛔ | ✅ câu · ⏳ nút ⇒ **`WO-023` `(h)`** |
| mất kết nối | như lỗi — `e.cau` của `FLS-MAT-KET-NOI` *(`goi_cua.js:140`)* | ⛔ | như lỗi |
| có dữ liệu | như nay | như nay | ✅ có sẵn |

Vì sao nút `Thử lại` ⛔ vào `WO-045`: phiếu ấy đòi **luật lượt** *(`ⓦ` ①)* và nút cho **danh sách lệnh** *(`ⓥ` ⑤)*; vùng ứng viên hôm nay lối ra là bấm lại hàng lệnh / `j` rồi `k` — đi được, chỉ là màn ⛔ nói. ⛔ Lỗi mã trong phạm vi `WO-045`.

**⑤ Lỗi của một cú bấm ⛔ được rơi ra console** *(v4.21, `TL-049` — `BG-048` mục yếu 3 + 5; `fls-ba` đọc lại mã `Đ1` @ `2b804e3`)*. Ba chỗ:

| # | Chỗ *(mã @ `2b804e3`)* | Hôm nay | Luật | Mã |
|---|---|---|---|---|
| ⓐ | `F01G` `gan` *(`man_f01_ghep.js:657-668`)* — `await FLS.ghi('/queue/<itl>/match', …)` ⛔ `try`; `nut()` *(`:267-273`)* gắn `click` thẳng, ⛔ bọc | cửa ghi trả `4xx` *(vd `422` — `BG-048` `AC-11`: **cả hai** cú `POST` của hai lượt Chrome đều `422`)* ⇒ `Uncaught (in promise) LoiCua`, màn **⛔ một chữ**: nút `Gán` vẫn đó, `ST.xac_nhan` vẫn bật. Người bấm ⛔ biết lệnh **chưa** gán — đúng lỗ `F-3` của `bo_gan` đã vá ở `WO-008` vòng 2 *(`BA-06` v4.10 ⓔ ca ⑤)* | khuôn ca ⑤ `Bỏ gán`: dòng lỗi trong khối hành động *"Gán chưa xảy ra — Cửa lỗi: <e.cau>"* ＋ `e.lam_gi` *(nếu có)* — ⭐ mã `FLS-HET-GIO` ⇒ *"Chưa rõ gán đã xảy ra chưa — Cửa lỗi: <e.cau>"* *(v4.23, `ⓕ3` — `TL-056`)*; nút `Gán` **khoá** trong lúc chờ cửa *(lớp "bấm GHI hai lần" #4 — `ⓦ` ① đoạn ⛔ Ngoài)*; **0** `Uncaught` | ⏳ **`WO-023` `(h)`** |
| ⓑ | `F01G` `mo_lenh` gọi từ phím `j`/`k`/`↓` *(`:1136`)*, chuột hàng *(`:1401` · `:1444`)*, ô tìm *(`:1245`)* ⛔ `await`/`catch` | lỗi lượt **mới nhất** ⇒ vùng ứng viên **đã** in `⛔ Cửa lỗi:` *(④)* **và** `Uncaught (in promise)` trên console | `mo_lenh` **vẫn ném** cho người gọi đọc nó *(`bo_gan` `:818` — bài `test_wo008_v2…AC12`)*; nơi gọi từ **phím / chuột / ô tìm** nuốt lỗi *(màn đã nói)* ⇒ **0** `Uncaught` | ⏳ **`WO-023` `(h)`** |
| ⓒ | `F04` `_soat` / `_nhan` *(`man_f04.js:612` · `:744`)* đọc `S.chup` | bấm mở ảnh mới ⇒ khung tải hiện, `S.chup` **vẫn** ảnh cũ tới khi lượt mới về *(`:318`)* ⇒ `Soát` / `Nhận` bấm đúng lúc ấy gửi `chup_id` của ảnh **⛔ còn trên màn** | mở ảnh mới ⇒ `S.chup = null` + `S.nguon_soat = null` **ngay** *(cùng khuôn `ⓦ` ① "xoá ngay" của `F01G`)* ⇒ hai nút **khoá** theo luật có sẵn `:879` *(`!S.chup`)* tới khi ảnh mới về | ⏳ **`GAP-SCR-35`** — nợ, ⛔ phiếu *(xem dưới)* |

Vì sao ⓒ chỉ là **nợ**: sổ thật `fls_chup` **158** ảnh, người chụp **0** *(`nhip@fls` **146** · `nhip@fls(tay)` **10** · `tools/chup_sao_ke.py` **2** — `fls-ba` `SELECT actor, count(*)` 05/10)* ⇒ màn `F04` chưa là đường nạp của người; cú bấm phải rơi đúng vào cửa sổ **một lượt đọc** *(vài trăm ms)* sau khi chính người ấy vừa bấm mở ảnh khác; và `Soát` in **mã ảnh** trong biên bản *(`:729`)* trước khi `Nhận` ⇒ còn một lần nhìn. Lật thành phiếu khi `F04` có người nạp thứ hai, hoặc khi `WO-023` được nhận *(gom vào `(h)` nếu Dev thấy rẻ — cùng lớp "nút ghi khoá khi trạng thái chưa sẵn")*. Vì sao ⓐⓑ vào **`WO-023`** *(⛔ vòng 2 `WO-045`)*: lớp *"lỗi cửa nói với người đang nhìn"* + *"khoá nút trong lúc chờ cửa ghi"* là đúng nhà của `WO-023` *(`ⓕ2`…`ⓕ4` — đã ghi ở đoạn ⛔ Ngoài của ①)*; `WO-045` ⛔ đòi, mã `WO-045` ⛔ làm sai điều nào nó đòi.

**⑥ Lựa chọn ứng viên `F01G` gắn theo `itl_id`, ⛔ theo chỉ số** *(v4.22, `KQ-050 F-3` — `fls-test` 05/10; `fls-ba` đọc lại mã `Đ1` @ `c903eb3`)*. Hôm nay `ST.ung_vien_chon` là **chỉ số mảng** *(`man_f01_ghep.js:146` `null` = ⛔ chọn sẵn · bấm hàng `:554` `= i` · `gan` `:658` + `Enter` `:1155` + `ve_thanh` `:617` đọc `ST.ung_vien[ST.ung_vien_chon]`)*. Lựa chọn chỉ bị xoá ở **đầu** một lượt *(`mo_lenh` `:1032` · ô tìm `:1227` khi hẹn giờ `TRE_TIM` nổ)* — ⛔ ở **cuối** lượt, khi danh sách mới **thay** `ST.ung_vien` *(`_tai_toan_so` `:1112` · `mo_lenh` `:1062`)*. Trong khoảng ấy danh sách cũ **vẫn trên màn** và bấm được *(lượt chữ ⛔ xoá danh sách; mở lại **cùng** lệnh sau `Bỏ gán` giữ danh sách — `ⓦ` ① đoạn `WO-045`)* ⇒ người bấm hàng `k` của danh sách **cũ**, lượt mới về, chỉ số `k` giờ trỏ vào một dòng tiền **khác**: màn **tô sẵn** dòng ấy và `Gán` gửi `/queue/<itl người ⛔ chọn>/match`. `ST.xac_nhan` *(bước hai của ca lệch)* cũng sống qua lượt ⇒ nhãn *"Xác nhận gán …"* nay là của dòng mới, **một** cú bấm là ghi.

| | Hôm nay | Luật v4.22 |
|---|---|---|
| Danh tính lựa chọn | chỉ số `i` trong `ST.ung_vien` | **`itl_id`** của dòng người bấm *(tên biến Dev chọn — `BG` ghi)*; `null` = ⛔ chọn *(`INV-I16` giữ)* |
| Lượt **mới nhất** thay `ST.ung_vien` *(mọi đường: `mo_lenh` cùng lệnh · ô tìm · Toàn sổ tự bật)* — `itl_id` đang chọn **có** trong danh sách mới | chỉ số giữ ⇒ có thể trỏ dòng khác | **giữ** lựa chọn — tô đúng hàng mang `itl_id` ấy, ở **vị trí mới** của nó |
| …— `itl_id` đang chọn **⛔ có** trong danh sách mới | chỉ số giữ ⇒ tô dòng người ⛔ chọn | **bỏ** lựa chọn *(`null`)* ⇒ thanh hành động về *"Chọn một giao dịch bên trên."* *(câu có sẵn `:647`)*, nút `Gán` khoá |
| `ST.xac_nhan` khi danh sách bị thay | giữ | **luôn** về `false` — cả khi giữ lựa chọn: cú xác nhận là của một danh sách người **đã nhìn**; danh sách đổi ⇒ bấm lại hai lần |
| `gan` / `Enter` / `ve_thanh` | đọc `ST.ung_vien[i]` | tìm theo `itl_id` trong `ST.ung_vien`; ⛔ thấy ⇒ **0** `POST`, ⛔ đoán |
| Đổi sang lệnh **khác** · đổi chip | `null` | như nay *(`null`)* |

Vì sao **giữ khi còn**, ⛔ luôn bỏ: luật đúng là *"gửi đúng dòng người đã bấm"* — `itl_id` đã chọn còn trong danh sách thì nó **vẫn** là dòng ấy, cùng tiền, cùng mã; bỏ nó là bắt người chọn lại sau **mỗi** lượt tìm *(rẻ, nhưng ⛔ cần)*. Cái giá: một phép tìm trong ≤ 50 hàng mỗi lần vẽ. ⛔ Đổi cửa, ⛔ đổi `TRE_TIM`, ⛔ xoá danh sách khi lượt chữ bay *(người còn đang đọc nó)*.

⚠ **Mức** *(PO 05/10 — `KQ-050` ghi `NHE`; `fls-ba` nâng **`NANG`**)*: ① của `KQ-050` đo **cửa ghi nhận mọi cặp trong dung sai** *(`200` — kho TEST `link_id 4163`)* ⇒ ở ca `F-3` cặp `(dòng người ⛔ chọn, lệnh đang mở)` lọt cửa nếu tiền nằm trong `min(1.000 đ; 0,5%)`; khớp **đúng** tiền thì **một phím `Enter`** là ghi *(`NFR-I25` chỉ chặn ca **lệch**)* ⇒ một mối nối sai vào sổ **chỉ-thêm** *(`INV-I08`)* + hai ô `hd`/`cdt1` máy gợi ý *(`QĐ-ITL-149`)*; đường lùi là `Bỏ ghép`. ⛔ `CHAN`: cùng **một** lệnh *(⛔ sai cặp lệnh như ① `WO-045`)*, màn **tô** hàng mới ⇒ người còn một lần nhìn, sổ thật **0** thao tác người. Mã ⇒ **`WO-023` `(i)`** *(đầu phiếu)*.

**⑦ `F01` `Xem thêm` — khung chờ + lỗi ⛔ xoá lưới** *(v4.22, `KQ-050 F-1`; `fls-ba` đọc mã `man_f01.js:181` · `:214-232` @ `c903eb3`)*. Hôm nay bấm `Xem thêm` ⇒ nút **khoá** *(đúng `ⓦ` ① — `WO-045`)* mà **⛔ một chữ** nói máy đang làm; trang 2 `VND` sổ thật mất **104,33 s** *(`fls-ba` đo 05/10, hàm thật `doc_hang_cho`, `noi_chi_doc` — `KQ-050` đo **95,1 / 81,1 s**)* ⇒ người thấy một nút xám **gần hai phút** và kết luận màn treo. Và lượt `Xem thêm` lỗi ⇒ `TT.loi(o, …)` thay **cả** khung `o` ⇒ **50** hàng người đang đọc biến mất theo.

| Trạng thái của lượt `Xem thêm` | Hiện gì |
|---|---|
| tải | nút `Xem thêm` **khoá** + chữ đổi thành `Đang tải thêm…` *(lớp `b tiny` như nay — ⛔ lớp mới)*; hàng đã có **giữ nguyên**; ⛔ lượt thứ hai *(như nay)* |
| có dữ liệu | hàng mới nối dưới, nút về `Xem thêm` *(còn trang)* / chip `hết danh sách` *(hết)* — như nay |
| lỗi · mất kết nối | hàng đã có **giữ nguyên**; dưới lưới dòng `⛔ Cửa lỗi: <e.cau>` *(khuôn chữ `ⓦ` ④ — ⛔ câu mới)* ＋ nút **`Thử lại`** lớp `b tiny` ⇒ lật lại **đúng** con trỏ vừa lỗi, **một** lượt |
| rỗng | ⛔ áp *(`Xem thêm` chỉ hiện khi cửa trả `next_cursor`)* |

Ngân sách thời gian: **`NFR-I30`** *(`BA-08` v1.4 — một trang danh sách việc ≤ **2 s**)*. Khung chờ là **lưới an toàn**, ⛔ thay cho sửa cửa: hiện cả khi cửa nhanh *(chớp một lần — chấp nhận)*. ⛔ Đếm giây trên nút *(một con số chạy là một lời hứa thời gian máy ⛔ giữ được)*. `F01L` / `F02` `Xem thêm` **⛔** trong ⑦: đo nhanh *(`/lenh-cho` **0,64–0,74 s**/trang — `fls-ba` 05/10; `/ledger` `NFR-I07`)*. Mã ⇒ **`WO-051`**.

**⑧ Ba chỗ màn nói sai việc, hay mời một cú GHI chắc chắn bị từ chối** *(v4.23 — phát hiện ngoài phạm vi `WO-023`: `BG-053` mục 3 · `BG-052` mục 6 · `BG-057` mục 5; `fls-ba` đọc lại mã `Đ1` @ `12b7230` + sổ thật chỉ `SELECT` 05/10)*. Xếp theo **tầm** *(ai gặp, bao nhiêu lần)* — ⓐ trước:

| # | Chỗ *(mã @ `12b7230`)* | Hôm nay *(đo)* | Luật v4.23 | Tầm |
|---|---|---|---|---|
| ⓐ | Câu + `lam_gi` của mã **`FLS-DQ-FAILED`** *(`goi_cua.js:117-120`)* | `cau` *"Cổng kiểm chất lượng không đạt nên máy chặn phép ghi này."* · `lam_gi` *"Mở màn “Cổng hôm nay” xem cổng nào đỏ."* — nhưng mã này **⛔ bao giờ** đến từ một cổng: `ghi_tay.py` mang nó ở **5** lớp lỗi của **cửa ghi** *(`LoiGhi` gốc `:106` · `ThieuLyDo` `:213` · `KhacTienTe` `:243` · `LechTong` `:249` · `ChuaDuyet` `:255`)*, **0** nơi ném nó từ `ACC-1…4` *(`grep -rl FLS-DQ-FAILED fls tools` ⇒ chỉ `bao.py` · `ghi_tay.py` · `goi_cua.js`)*. Lý do thật đi trong `chi_tiet` *(vd `dong so la 'USD' nhung dong lenh la ['VND']` — `BG-053` `AC-10`; `adj_id=… da bi dao truoc do` — `ghi_tay.py:535`)*, mà màn **đã** in chữ nhỏ dưới dòng lỗi *(ca ⑤ · `ⓦ` ⑤ ⓐ · `HT.loi_trong_hop`)* ⇒ người bị chỉ sang một màn mà mọi cổng có thể đang **xanh** | `cau` ⇒ *"Phép ghi này trái một luật kiểm của cửa ghi nên máy chặn."* · `lam_gi` ⇒ *"Đọc dòng chi tiết ngay dưới: nó nói luật nào — khác tiền tệ, lệch tổng, lệnh chưa duyệt, thiếu lý do hay bút toán đã đảo. Mỗi lý do sửa một đường khác nhau."* — hai chuỗi **nguyên văn**, chữ trơn *(luật ký hiệu)*. ⛔ Đổi mã, ⛔ đổi HTTP `422`, ⛔ dịch `chi_tiet`. `bao.py::MA_LOI` mô tả theo `BA-07` **v3.13** §5. ⚠ Vì sao ⛔ **tách mã** *(mỗi lớp một mã, một câu)*: đổi hợp đồng cửa + mọi bài đọc mã; `chi_tiet` đã nói đúng lý do từng ca ⇒ câu chung chỉ cần **⛔ chỉ sai đường** | **mọi** `422` của cửa ghi: `F01G` `Gán` *(ca khác tiền tệ / lệch tổng — đúng vòng ghép thật `B5`)*, `F01L` `Ghép`, `F02` `Đảo` / gõ ô. Cú bị từ chối ⛔ để lại dòng sổ ⇒ ⛔ đếm được số lần; đếm được **đường**: **5** lớp |
| ⓑ | Chế độ **chỉ đọc**: `F01G` `Gán` *(cả `Xác nhận gán …` và phím `Enter`)* · `Bỏ gán` · `F02` ⑥ `Đảo` | `man_f01_ghep.js` hỏi `cho_ghi` **0** lần *(`grep`)*; `nut()` `:300` ⛔ hỏi; nút `Gán` `:694` · `Bỏ gán` `:698` bấm được. `F02` nút `Đảo` `man_f02.js:1828` dựng ⛔ hỏi `cho_ghi()` *(hàm có ở `:94`, chỉ dùng cho lưới `:420` · `:888` · `:1970`)*. ⇒ ⚠ **Đính chính `ⓦ` ②**: hàng *"`Gán` · `Bỏ gán` … **khoá** + câu `405` **như nay**"* — *"như nay"* **chỉ đúng ở `F01L`** *(`_chan_ghi` `man_f01_lenh.js:61`)*, ⛔ ở `F01G`. Sau `WO-023` `(h)` bấm ⇒ cửa `405` ⇒ dòng *"Gán chưa xảy ra — Cửa lỗi: Việc này chưa mở trên cửa đang chạy."* — **0** ghi, nhưng người đi trọn một vòng *(ca lệch: hai cú bấm; `Đảo`: gõ lý do)* mới biết | ở chế độ chỉ đọc *(`FLS_PHIEN.cho_ghi` ⛔ `true`)*: ba nút **khoá** *(`disabled`)* + `title` = **nguyên văn** câu `405` của `_chan_ghi` *(`man_f01_lenh.js:63-64`)* — **một** hằng dùng chung, ⛔ bản gõ thứ hai *(chỗ đặt: Dev chọn)*; phím `Enter` của `F01G` ⛔ gửi; hộp `Đảo` ⛔ mở. **0** `POST`. Nút **đọc** ⛔ đổi *(`ⓦ` ② bảng giữ)*. ⛔ Đổi câu `405`, ⛔ đổi `NFR-I03` | **mọi** người mở sổ thật ⛔ bật ghi *(owner xem · `fls-test` · `fls-ba` trên 8088/8097)*; nút `Đảo` tới được: **4.426** *(sổ thật `fls_adjustment` **4.428** bút toán − **2** bản đảo đã là chip)*. Kế toán ghép thật chạy `--cho-ghi` ⇒ ⛔ bị |
| ⓒ | `F02` ⑥ nút `Đảo` trên bút toán **đã bị đảo** | `man_f02.js:1826-1832` chỉ đổi nút thành chip khi **chính** bút toán là bản đảo *(`x.reversal_of`)*; bút toán **đã bị** một bản khác đảo vẫn mang nút ⇒ bấm, gõ lý do, `Ghi` ⇒ `422 FLS-DQ-FAILED` *"adj_id=… da bi dao truoc do"* *(`ghi_tay.py:535`)* ＋ `lam_gi` ⓐ sai việc | bút toán có **một** bút toán khác trong **cùng** mảng `but_toan[]` mang `reversal_of` = `adj_id` của nó ⇒ thay nút bằng chip lớp `chip lock` *(có sẵn — cùng lớp chip `bản đảo của #N`)*, chữ *"đã bị đảo bởi #M"*. Đọc từ chính mảng cửa đã trả *(`doc_bao_cao.py:478-482` chở **mọi** bút toán của dòng)* ⇒ ⛔ trường mới, ⛔ đổi cửa. ⛔ Đổi luật **ai được đảo dòng nào** *(`SM-I03`)* — cửa vẫn từ chối như nay | sổ thật **2** nút *(`#163563` · `#163565`, dòng `27728` UAT — `SELECT` 05/10)*; tập **mở**: mỗi cú `Đảo` thêm một |

Phép canh + nợ đi kèm *(cùng phát hiện)*:
- **ⓓ Cổng quét `HT.nuot_phim`** *(`BG-054` mục yếu 2)*: mọi trình nghe phím của màn trong `fls/web/tep/man_*.js` — cả `addEventListener('keydown'` **và** gán `.onkeydown =` — phải hỏi `HT.nuot_phim(e)`, **hoặc** mang chú thích miễn **có lý do đo được** ngay trên dòng ấy. Đếm @ `12b7230`: `addEventListener('keydown'` **3** *(cả 3 hỏi — `man_f01_ghep.js:1348` · `:1652` · `man_f02.js:718`)* ＋ `.onkeydown =` **2** **⛔ hỏi** *(`man_f02.js:848` ô sửa lưới · `:2018` ô panel — chỉ chạy khi ô ấy có focus; `BG-054` đếm **thiếu** hai chỗ này vì chỉ `grep` một dạng)*. Hai chỗ ấy hỏi, hay mang chú thích miễn sau khi Dev đo *"hộp `HT` mở thì ô ngoài hộp còn nhận phím không"* ⇒ cổng xanh. Một bài `tests/web/` tĩnh. Mã ⇒ **`WO-060`** ⓓ.
- **ⓔ `ST.dg_mo` gắn theo `itl_id`** *(`BG-052` mục yếu 5)*: hàng ứng viên đang mở rộng diễn giải *(`đủ ↓`)* lưu **chỉ số** *(`man_f01_ghep.js:182` · `:501` · `:519` · `:583`)* ⇒ lượt mới thay danh sách thì phần mở rộng nhảy sang dòng khác. Cùng luật `⑥`: giữ nếu `itl_id` còn, bỏ nếu ⛔. Chỉ đổi **chữ hiện**, ⛔ chạm ghi ⇒ **THẤP**. Mã ⇒ **`WO-060`** ⓔ.
- **Nợ, ⛔ phiếu**: `la_ban_dao` nối theo `at` trùng mà ⛔ ràng buộc máy canh ⇒ **`GAP-API-12`** *(`BA-07` v3.13 — điều kiện lật ở đó)*. Dấu `e._hop_thoai` là thuộc tính tự đặt lên sự kiện trình duyệt *(`BG-054` mục yếu 1)* — đo được trên Chrome 154, ⛔ chuẩn nào hứa ⇒ **giới hạn đã biết**, đo lại khi đổi trình duyệt đích. `GAP-SCR-35` *(`F04` `S.chup`)* — Dev ⛔ gom ở `WO-023` `(h)` ⓓ ⇒ **vẫn nợ** *(`ⓦ` ⑤ ⓒ, điều kiện lật giữ)*.

**⑨ Kết quả một cú `Gán` thuộc về LỆNH của nó, ⛔ thuộc lệnh đang mở lúc cửa trả** *(v4.24 — `KQ-061` lăng kính **Logic** ⓖ, nghi **chưa chứng**; `fls-ba` đọc mã `man_f01_ghep.js:752-779` · `:1184-1185` @ `7b4237f`)*. Đọc mã: `gan(lenh)` chờ `/match` mà **⛔** khoá phím đổi lệnh *(`ⓕ1` chỉ áp khi có **hộp**; nút `Gán` nằm trong khối hành động, ⛔ hộp)* ⇒ người có thể `j` / chuột sang lệnh `B` trong lúc cú `Gán` của `A` đang bay. Khi cửa trả: ⓐ `200` ⇒ `ST.chon_itl = null` + `_nguoi_mo(lenh_ke_tiep(A))` — màn **rời** `B` sang lệnh kế của `A`, xoá lựa chọn người đang làm ở `B`; ⓑ lỗi ⇒ `ST.loi_gan = {ma: A …}`, chỉ vẽ khi đang mở `A` *(`ve_dong_gan` `:717`)*, mà mở lại `A` từ `B` là **đổi** lệnh ⇒ `mo_lenh` `:1185` xoá `loi_gan` ⇒ lỗi của một cú ghi **⛔ ai thấy** bị xoá; ⓒ `ST.dang_gan` là cờ **chung** ⇒ nút `Gán` của `B` khoá theo cú của `A` *(an toàn, nhưng ⛔ nói vì sao)*. ⛔ Chưa ai dựng ca ⇒ mức **chưa xếp** *(`Đ5`)*: phiếu đòi **tái hiện trước**, ⛔ chứng thì ⛔ sửa.

| # | Luật v4.24 *(áp khi tái hiện được)* | ⛔ |
|---|---|---|
| ⓐ | Cửa `/match` trả `200` mà `ST.mo` khác lệnh của cú `Gán` ⇒ **⛔** đổi `ST.mo`, **⛔** chạm `chon_itl` / `xac_nhan` của lệnh đang mở, **⛔** tự mở lệnh kế; thẻ `A` đổi rổ ở lượt tải danh sách kế tiếp như mọi cú ghi khác. `ST.mo` **là** lệnh của cú `Gán` ⇒ như nay *(sang lệnh kế)* | kéo người khỏi lệnh đang đọc |
| ⓑ | Cửa lỗi *(kể cả `FLS-HET-GIO`)* mà `ST.mo` khác lệnh của cú `Gán` ⇒ `loi_gan` **giữ** theo mã lệnh `A` cho tới khi người **mở lại `A`** và dòng lỗi được **vẽ** một lần; đổi lệnh **sau** lần vẽ ấy thì xoá như nay *(tín hiệu một lần — khuôn `ⓕ5`)* | xoá một lỗi ghi chưa ai thấy |
| ⓒ | Trong lúc cú `Gán` của `A` bay mà người đang ở `B`: nút `Gán` của `B` khoá **kèm** `title` *"Đang chờ máy trả lời cú Gán của lệnh &lt;A&gt;."* *(chữ trơn)* | nút khoá ⛔ lý do |

Tầm: sổ thật **0** cú `Gán` của người *(`fls_pm_link` **2.263** = 2.262 dựng 10/09 + 1 UAT)*; lượt ghi kho TEST trung vị **~0,1 s** *(`BG-055`: `/unmatch` **0,102 s**)* ⇒ khe để `j` lọt hẹp trên máy đơn, rộng khi mạng chậm *(tới `30 s` — `ⓕ3`)*. Mã ⇒ **`WO-060` `(f)`** *(tái hiện trước)*.

#### ⓠ ⭐⭐ BẢY góp ý của owner khi nhìn màn THẬT lần đầu (`23/09`)

⭐⭐⭐ Đây là **lần đầu một con người nhìn màn này bằng mắt** — `NFR-I10` cho tới hôm qua vẫn **CHƯA ĐO**. Bảy góp ý ấy ⛔ **không phải "ý thích"**: mỗi cái là một chỗ màn **nói khó hơn mức cần thiết**, và ⛔ không cổng nào trong `8` cổng đang chạy chạm tới được — vì chúng đo *"có đúng ⛔ không"*, ⛔ không đo *"đọc có mệt ⛔ không"*.

| | Góp ý | Điều đo được đằng sau |
|---|---|---|
| `1.1` | bỏ cột `Bậc` ở bảng | lúc **quét**, câu hỏi là *"dòng nào chưa xong"* — ⛔ không phải *"dòng này khớp ở mức nào"* |
| `1.2` | *"phông chữ và cỡ chữ chưa đều, rối mắt"* | **`10`** cỡ chữ khác nhau trên một màn ＋ `--mono` dùng **`14`** chỗ, gồm cả câu văn xuôi |
| `1.3` | bỏ dải nhắc `GAP-SPEC-01` | nó nói về **tình trạng dự án**, ⛔ không về việc kế toán đang làm — mà đọc lại ở **mọi** lần mở màn |
| `2.1` | khối *«Xem đủ trường»* theo wireframe | bản `22/09` xếp **dọc** ⇒ một cú bấm đẩy phần dưới màn xuống gần **một màn hình** |
| `2.2` | *"cột lệnh chi text toàn màu đen"* | mã `PM…` là thứ người ta **quét mắt** để tìm dòng, mà nó ⛔ không khác gì câu nội dung |
| `2.3` | cho chỉnh bề rộng cột lệnh chi | nội dung lệnh chi dài ngắn **rất khác nhau** giữa các rổ; một bề rộng chạm chết vừa rổ này thì cắt cụt rổ kia |
| `2.4` | bảng giao dịch thiếu tên cột | **`7`** cột ⛔ không một cái tên — `CT88210` là số chứng từ hay mã gì? `OCBC · ••4001 · SGO2` là cái gì? |

##### ⭐⭐ `1.2` — **`10` cỡ chữ ⛔ không phải một thang, mà là `10` lần chọn riêng lẻ**

Đo `23/09` trên khối `SCR-F01` của `hinh.css`: `10 · 10,5 · 11 · 11,5 · 12 · 12,5 · 13 · 13,5 · 14 · 15px`. Mỗi con số là một lần ai đó *(hoặc tôi)* gõ một giá trị **"trông cho vừa"*. Mắt người đọc thấy đúng cái đó: ⛔ **không tìm ra đâu là bậc trên, đâu là bậc dưới** ⇒ mọi thứ tranh nhau nói.

⇒ **`5` bậc**, mỗi bậc trả lời **một câu hỏi khác nhau**: `--fs-nhan` *(nhãn HOA)* · `--fs-phu` *(thứ đọc sau)* · `--fs-than` *(thân bài)* · `--fs-manh` *(một mục nhấn)* · `--fs-to` *(số tiền)*. `29` khai báo về một thang, `0` bỏ sót.

⭐⭐ Và một luật một câu cho `--mono`: **nó dành cho thứ cần so cột theo ký tự** — mã, số tiền, ngày, số chứng từ. Một **CÂU VĂN** trong `--mono` đọc như một bản in máy; `.goi-phim` *(câu hướng dẫn)* và `.more dd` *(`Approve` · `VPBANK` · tên người nhận)* đã chuyển về `--sans`. Đó là **một nửa** của cảm giác *"rối mắt"*.

##### ⛔⛔ `2.4` — hàng tiêu đề phải dùng **ĐÚNG lưới của dòng**

Cột ⛔ **không được khai hai lần**. Nếu tiêu đề khai lưới riêng, có **hai bản sự thật** cho cùng câu hỏi *"bảng này có mấy cột"*, và khi chúng lệch thì **mọi nhãn đọc sang cột bên cạnh** — một lỗi đọc **rất thuyết phục** vì nó ⛔ không trông như lỗi. ⇒ Tách `.cand-cols`, tiêu đề và dòng **cùng đọc một bản khai**.

##### ⛔⛔ `2.3` — bề rộng đã kéo phải sống trong `ST`, ⛔ KHÔNG trong DOM

`ve()` dựng lại **toàn bộ** cây mỗi lần. Đặt bề rộng thẳng vào phần tử thì kéo xong bấm một cái là **nhảy về cũ** — và người dùng sẽ tưởng **tay kéo hỏng**, chứ ⛔ không nghĩ là màn vẽ lại. ⇒ `ST.rail_w`, và `ve()` đọc lại nó.

⭐ Kéo có **chặn hai đầu** *(`RAIL_MIN 260` / `RAIL_MAX 720`)*: một rail `120px` thì ⛔ không còn đọc được mã lệnh nào, một rail `1200px` thì bàn làm việc ⛔ không còn chỗ cho `7` cột giao dịch. **Hai đầu đều là *"màn hỏng"***.

⚠ **`--rail` và `--rail-w` đã gộp về MỘT tên** — cổng token bắt được `--rail-w` ⛔ chưa khai, và đúng lúc ấy lộ ra tôi đang có **hai tên cho cùng một bề rộng**. Hai tên cho một con số là hai bản sự thật, và rồi sẽ có chỗ đọc bản này, chỗ đọc bản kia.

⛔ **Bậc ⛔ KHÔNG biến mất khỏi màn** khi bỏ khỏi bảng: nó vẫn là `①②③④` trên **từng dòng ứng viên** — đúng chỗ người ta **đang chọn**. `test_BAC_VAN_CON_tren_dong_ung_vien` giữ điều đó.

#### ⓡ ⭐⭐⭐ Vòng góp ý thứ HAI — và một **lỗi CHẶN** lộ ra khi đo

##### ⛔⛔⛔ `/itl-candidates` trả **HÀNG THÔ** — đường chính của màn

Đo `23/09` trên cửa thật, `PM01089-1`:

| khoá màn đọc | `/itl-candidates` *(máy đề xuất)* | `/so` *(Toàn sổ)* |
|---|---|---|
| `amount` | ⛔ **⛔ không có** *(cửa gửi `tien`)* | `2036.80` |
| `chieu` | ⛔ **⛔ không có** *(cửa gửi `ps_no`/`ps_co`)* | `co` |
| `nguon` | ⛔ **⛔ không có** *(cửa gửi `source_sheet`)* | `{tk, bank, curr, le}` |

⛔ Hàm vẽ `ve_ung_vien` đọc `uv.amount` · `uv.chieu` · `uv.nguon` ⇒ **hai cột rỗng**; và `khop_dung_tien` so `Number(undefined)` ⇒ **MỌI ứng viên đều thành *"lệch"*** ⇒ nút `Gán` luôn đi đường cảnh báo. ⭐⭐ **Một phép khớp ĐÚNG được trình bày như một phép khớp SAI** — tệ hơn là ⛔ không hiện gì, vì nó dạy người ta rằng cảnh báo là chuyện thường.

⛔⛔ **Vì sao nó sống sót:** bài thử cũ `test_UNG_VIEN_TIEN_bac_ma_dung_dau` chỉ hỏi `bac` và `itl_id` — **đúng hai khoá mà hàng thô TÌNH CỜ cũng có**. ⭐ Một bài thử hỏi vài khoá giao nhau thì **⛔ không bao giờ thấy hai khuôn là HAI**.

⭐ Và ảnh chụp của owner ⛔ không lộ ra, vì màn lúc ấy đang ở chế độ **Toàn sổ** — cửa **KIA**, và cửa kia **đã** nắn khuôn. Hai cửa nuôi **một** hàm vẽ mà nói **hai** thứ tiếng.

⇒ `ung_vien_tien` nay nắn qua `khuon_ung_vien`; hai bài thử mới đo **khuôn hợp đồng `10` trường**, ⛔ không đo vài khoá.

⛔⛔ Kèm theo: `khuon_ung_vien` **⛔ không còn ném** khi `source_sheet` sai khuôn — nó trả `nguon: null` ＋ `loi_nguon`. Cùng một lý lẽ đã dùng ở cửa danh sách `22/09`: `tach_nguon` ném là **đúng ở tầng đọc** *(`INV-I16`)*, nhưng khuôn này chạy trên **từng dòng của một danh sách**, và một ngoại lệ ở đây trả `500` cho **cả trang** ⇒ mất **`50` ứng viên** vì **một**. ⭐ Và nó **giữ lại** `dien_giai`/`amount` — người ta vẫn đọc được **bằng chứng** dù ⛔ không biết dòng tiền ấy từ tài khoản nào.

##### ⭐⭐⭐ `3` — *"các cột ⛔ không thẳng hàng"* ⛔ KHÔNG phải lỗi căn lề

`.cand-cols` kết thúc bằng một vệt `auto`. Mà **hàng tiêu đề và mỗi dòng ứng viên là những LƯỚI RIÊNG BIỆT** ⇒ `auto` *(và phần dư của `1fr`)* tính lại **theo nội dung TỪNG DÒNG**: dòng `2.037 USD Có` được vệt cuối rộng hơn dòng `19 USD Có`, phần dư dồn ngược vào `1fr`. **Một bản khai lưới, `14` kết quả khác nhau.**

⇒ Chữa duy nhất: **mọi vệt phải tiên đoán được** — một con số cố định hoặc một phần `fr`. Lúc ấy `14` lưới riêng cho ra `14` kết quả **y hệt nhau**, và đó chính là định nghĩa của *"thẳng hàng"*.

⭐ Và số tiền: `flex` ＋ `justify-content:flex-end` căn theo **chữ `Có`** ⇒ các **con số** lệch từng bậc. Nay `.amt` là lưới **ba ô cố định** — `Δ` ｜ số ｜ `Nợ/Có` — và ô `Δ` **giữ chỗ cả khi ⛔ không có Δ**: nếu nó co lại thì con số sẽ **nhảy sang trái** ở đúng những dòng có lệch, tức lại lệch lần nữa.

##### ⭐⭐ `2` — bàn làm việc **dừng yên**, chỉ danh sách cuộn

Rail **đã** làm đúng thế này từ trước *(`sticky` ＋ cuộn riêng)*; bàn làm việc thì ⛔ chưa — nên cuộn xuống dòng thứ `40` là **thẻ PM biến mất**, và người ta ⛔ không còn biết mình đang ghép cho lệnh nào. `.work` nay dùng **cùng khuôn** với `.rail` — ⛔ không bịa một cách thứ hai cho cùng một ý.

⛔⛔ Dòng quan trọng nhất là **`min-height:0`** trên `.cands`: một mục flex mặc định **⛔ không co nhỏ hơn nội dung của nó**, nên thiếu dòng ấy thì `overflow:auto` **⛔ không bao giờ kích hoạt** — hộp cứ phình ra bằng `50` dòng, `.work` tràn khỏi `max-height`, và cả trang lại cuộn. **Tức ⛔ không sửa được gì**, mà CSS ⛔ không báo một lỗi nào.

##### ⭐⭐ `1` — khối *«Xem đủ trường»* là **lớp phủ**

Nó phục vụ **niềm tin vào dữ liệu** *(`QĐ-ITL-144 ⓐ`)*, ⛔ **không** phục vụ việc ghép. Một phép **TRA CỨU** ⛔ không được đòi chỗ với công việc chính ⇒ nó **nổi lên trên**, và đóng lại là mọi thứ về đúng chỗ cũ — ⛔ không một pixel nào dịch. So với một hộp cuộn trong thẻ, cách này ⛔ **không ăn một chút chiều cao nào** của danh sách.

⛔ Kèm `max-height` ＋ `overflow:auto`: một thẻ `27` trường sẽ chạy **quá đáy màn hình**, và phần cuối ⛔ không ai với tới được.

⛔⛔ Và `Esc` phải **bóc từng lớp một**. Nếu nó đóng thẳng cả lệnh thì một người vừa mở *«Xem đủ trường»* để đối chiếu sẽ **mất luôn dòng lệnh đang làm** chỉ vì muốn đóng một lớp phủ — và ⛔ không cách nào quay lại ngoài việc tìm lại dòng ấy trong `738` dòng.

#### ⓢ ⭐⭐⭐ *"Kế toán cần nhìn rõ khu vực này"* — và một huy hiệu **lặp lại bậc**

Owner `23/09`, ảnh chụp thứ ba: `SUPE…` · `ASTR…` · `TERA…` ở cột `Nguồn`, và `15.000.000…` ở cột `Số tiền`. ⛔⛔ **Lỗi của tôi ở vòng trước**: tôi cố định bề rộng **để cột thẳng hàng**, và ⛔ **không đo thứ phải nằm vừa trong đó**. *Thẳng hàng mà ⛔ không đọc được thì chỉ là đổi một lỗi lấy một lỗi.*

##### Số đo — `200` ứng viên một lệnh ＋ `1.761` ứng viên của `30` lệnh

| cột | p50 | max | chuỗi dài nhất | cần | tôi đã cho |
|---|---|---|---|---|---|
| `doc_no` | `12` | **`36`** | *(có cả UUID)* | — | `112px` |
| `nguon` ghép | `19` | **`25`** | `Airwallex · ••2651 · HGO2` | **`~188px`** | ⛔ `150px` |
| `số tiền` | `7` | **`17`** | `1.150.000.000 VND` | **`~128px`** ＋ ô `Nợ/Có` | ⛔ `146px` **trừ** `34px` ô `Δ` ⇒ còn `87px` |

⭐ `bank · tk · le` là **ba mảnh của MỘT câu trả lời** — *"dòng tiền này từ đâu"*. Cắt mất một mảnh thì hai mảnh còn lại ⛔ không còn trả lời được gì.

##### ⭐⭐⭐ Huy hiệu `Δ` là một **hàm của bậc** — nó bị bỏ

Đo trên `1.761` ứng viên máy đề xuất, ánh xạ **một-một**:

| bậc | `Δ` | n |
|---|---|---|
| `cung_tien_te` ④ | **khác `0`** | `1.664` |
| `ma` ① | **vắng** | `51` |
| `tien` ② | **`= 0`** | `46` |

⇒ `Δ` ⛔ **không mang một chút tin nào mới** *(`UI-F9` — một sự thật, một chỗ hiện)*. Và nó có mặt ở **`97,1%`** dòng ⇒ ⛔ **không còn là một dấu hiệu**: *một báo động chỉ đáng giá bằng độ HIẾM của nó*. Ở cửa `/so` *(Toàn sổ)* nó là **`0/1.800`**, tức `34px` giữ chỗ trên mọi dòng cho thứ ⛔ **không bao giờ xuất hiện**.

⛔⛔ Cái giá: `34px` giữ chỗ ＋ tới `90px` khi hiện *(`Δ 1550304.54`)* — lấy đúng của hai cột kế toán phải đọc. Và `1550304.54` là **khuôn của máy** *(⛔ không dấu phân cách)* lọt lên màn của người *(`UI-F8`)*.

⭐ Con số ấy ⛔ **không bị vứt**: nó chuyển sang đúng lúc nó **đổi một quyết định** — câu xác nhận khi kế toán chọn một ứng viên lệch. `97,1%` tiếng ồn trong một danh sách ⇒ `100%` tín hiệu ở một thời điểm.

##### ⛔⛔⛔ Và một lỗi **tôi để lại** ở vòng trước

Hai khối `@container` vẫn khai lưới trên **`.cand`** với bản **CŨ** — còn vệt `auto`. Hai bộ chọn cùng độ đặc hiệu, mà `@container` nằm **sau** trong tệp ⇒ nó **THẮNG**: ở mọi màn hẹp hơn `860px` thì vệt `auto` **quay lại** và mọi cột lại lệch — **im lặng**, ⛔ không một lỗi nào. ⭐⭐ Tệ hơn: nó `display:none` đúng cột **`Nguồn`** — cái owner vừa nói là phải nhìn rõ.

⭐ Thứ tự hy sinh cột là một **quyết định về thông tin**, ⛔ không phải một tiện nghi CSS. `Nguồn` ＋ `Số tiền` ＋ `Diễn giải` là ba thứ kế toán đối chiếu. ⇒ `Ngày` đi trước *(đã có trên thẻ PM, và thường có cả trong diễn giải)*; `Số CT` đi sau *(có khi là một **UUID `36` ký tự** ⛔ không ai đọc)*; **`Nguồn` ⛔ KHÔNG BAO GIỜ**.

#### ⓣ ⭐⭐⭐ `C4` **ĐÃ LÀM** — và một lỗi **phép sửa trước đẻ ra**

##### ⛔⛔ `1` · *"bấm chọn một Transaction, danh sách nhảy về đầu"*

⭐⭐ Đây là một lỗi **do chính phép sửa `v4.5` sinh ra**. `ve()` dựng lại **toàn bộ** cây DOM mỗi lần ⇒ `scrollTop` của mọi hộp cuộn về `0`. Trước `23/09` nó ⛔ **không tồn tại**: cả trang cuộn, và trình duyệt tự giữ vị trí trang. Tôi vừa cho `.cands` cuộn riêng *(`§4.5 ⓡ`, góp ý `2`)*, và **ngay đó** sinh ra nó.

⭐ *Một phép sửa mở ra một lỗi mới thì phải có một bài thử **đi kèm**, ⛔ không phải một lần nhìn lại.*

⛔⛔ Và giữ chỗ **⛔ không phải luôn luôn đúng**: đổi sang một **lệnh khác** thì danh sách ứng viên là một danh sách **khác hẳn**; giữ `scrollTop = 420` ở đó là mở ra **giữa** một danh sách mới. ⇒ Luật: **giữ chỗ khi vẽ lại cùng một cảnh, về đầu khi đổi cảnh.**

##### ⭐⭐⭐ `2` · `C4` — lệnh đã gán phải nói **nó gán với dòng tiền NÀO**

Hợp đồng `§4` khai `C4` *(khối đang gán)* từ đầu. Nó **⛔ chưa bao giờ được làm**. Trước `23/09` màn chỉ hiện chip `Đã gán` trên thẻ — tức nó nói *"việc này xong rồi"* mà ⛔ **không nói xong bằng gì**. Kế toán mở một lệnh đã gán ra thì thấy một danh sách `20` ứng viên **do máy đề xuất**, và ⛔ không một dấu hiệu nào chỉ ra dòng nào trong số đó *(hoặc dòng nào **ngoài** số đó)* đang được gán.

⛔⛔ Cửa **⛔ không chở đủ**: `_gan_gd` xưa lấy `ds[0]` — với một chùm `7` dòng, cửa nói về **một**. Đo `23/09` trên `2.219` lệnh đã gán: **`23` (`1,0%`)** gán nhiều hơn một dòng tiền, nhiều nhất **`7`**. ⭐⭐ Một `1,0%` là cớ để **⛔ không bật hộp thoại xác nhận** *(`QĐ-ITL-148 ⓔ`)* — ⛔ **không** phải cớ để **giấu mất sáu dòng tiền**. ⇒ `gd_ds`. Giá: tập `id` tăng từ ~`500` lên ~`505` mỗi trang — **một** truy vấn vẫn là **một**.

##### ⭐⭐⭐ `3` · Chùm khớp **chính xác ở TỔNG**, mà bậc từng dòng nói `④`

Đo trên cửa thật, `PM00001-1`:

```
itl_da_gan = [28338, 28339]
29.211.750 ＋ 40.513.971 = 69.725.721   ≡  số tiền lệnh
```

⇒ Chùm ấy là một phép khớp **chính xác đến từng đồng**. ⛔⛔ Nhưng `_bac` tính **từng dòng một**, nên cả hai đều ra `cung_tien_te` — **bậc yếu nhất**. Màn vẽ hai khối `④` cạnh nhau thì kế toán đọc được *"hai phép gán yếu"*, trong khi sự thật là *"một phép gán khớp đúng"*.

⭐ Sửa **⛔ không phải ở `_bac`** — bậc của **một** dòng tiền so với **một** dòng lệnh vẫn đúng như thế. Sửa ở chỗ **nói ra cái mà từng dòng ⛔ không nói được**: một dòng **TỔNG** ＋ một câu *"khớp"* / *"lệch bao nhiêu"*.

⛔ Và chỉ vẽ khi có **hơn một**: tổng của một số là chính nó, nên một dòng *"Tổng: 29.211.750"* ngay dưới đúng con số `29.211.750` là một dòng ⛔ không nói gì — mà nó sẽ xuất hiện ở **`99,0%`** số lệnh.

### §4.6 · ⭐⭐⭐ NĂM SỬA BẮT BUỘC trước khi dựng — chặng `B0` *(2026-09-21, `QĐ-ITL-148`)*

> ⭐ Cửa đã khai ở `BA-07 §4h`. Mục này là phần **màn phải làm khác** so với bản dựng `_10`.

#### ⓐ ⭐⭐⭐ Khối *«Xem đủ trường»* phải **HIỆN trường vắng**, ⛔ không giấu

⛔⛔ Bản dựng **bỏ qua** hàng khi giá trị rỗng ⇒ trường vắng **biến mất ⛔ không một chữ nào**. Ở đúng khối sinh ra để kế toán **yên tâm về data**, đó là chỗ tệ nhất để một trường im lặng biến mất.

⭐⭐ **Và dữ liệu ⛔ KHÔNG đều** — đo `21/09` trên ảnh PM hiệu lực *(`3.772` dòng)*: `tho` có **`27` khoá** và **`41` HÌNH DẠNG** khác nhau, mỗi dòng mang `18`–`23` khoá.

| Trường | Có | Ghi khi vắng |
|---|--:|---|
| `Chi nhánh` | **440** = 11,7% | ⛔ *"⛔ không có"* |
| `PE (Urgent)` | **17** = 0,45% | như trên |
| `PE (Advance)` | 483 | như trên |
| `ID PESlip` ／ `ID PELine` | 500 | như trên |
| `Ghi chú` | 626 | như trên |
| `Status_Final` | 3.532 | như trên |
| khối `PI` | 3.272 | như trên |

⭐ **Một phép đo làm việc này DỄ hơn tưởng:** đếm *"có khoá"* và *"có chữ"* cho **cả `27` khoá** ⇒ **hai số bằng nhau ở mọi khoá**. Nghĩa là ⛔ **không có ca chuỗi rỗng** — chỉ cần phân biệt **VẮNG** với **CÓ**, ⛔ không phải ba trạng thái.

#### ⓑ ⭐⭐ Gỡ **trùng lặp** `Người nhận` ↔ `Tên tài khoản`

Cùng **một ô** *(`tho['Tên tài khoản']`)* hiện **hai nhãn**, và khi bung thì hiện **cùng lúc** ⇒ `UI-F9`. ⇒ **Giữ trên thẻ** *(tên `Người nhận` — đó là chữ kế toán dùng)*, **bỏ** khỏi khối bung.

⚠ **Đây là `8/36` của `CR#12` tái phát**, và nó tái phát vì thiết kế đọc **hai nguồn khác nhau** *(thẻ đọc `BA-06`, khối bung đọc thẳng `tho`)* mà ⛔ không ai đặt hai danh sách cạnh nhau.

#### ⓒ Bỏ trường `Người lập` — **⛔ không có nguồn**

Quét **`27`** khoá `tho`: ⛔ **không** khoá nào là *người lập* ／ *email*. ⇒ ⛔ Không vẽ. ⛔ **⛔ Không** vẽ ô trống chờ dữ liệu — *"⛔ chưa nạp"* và *"⛔ không có"* là hai câu khác nhau, và ở đây **cả hai đều sai**: trường ấy **⛔ chưa bao giờ tồn tại**.

#### ⓓ ⭐⭐ **Chip lọc thứ tư** — và nó là thiếu một KHÁI NIỆM

Bản dựng có `Chưa gán` ／ `Đã gán` ／ `Tất cả`, trong đó `Chưa gán` = *mọi dòng ⛔ không phải đã gán* ⇒ **gộp cả `768` dòng ⛔ không gán được** vào việc hằng ngày.

⛔⛔ `INV-I20` nói một dòng rời hàng chờ bằng **ba** đường, và `768` dòng ấy là **ĐÍCH CUỐI** — nơi một dòng **rời** hàng chờ, ⛔ không phải nơi ai đó ngồi làm.

| Chip | Dòng | Là gì |
|---|--:|---|
| ⭐ `Chưa gán` | **738** | **việc thật** — mặc định |
| `Đã gán` | 2.219 | |
| ⛔ `Không gán được` | **768** | ⛔ **⛔ không nút hành động nào** — mỗi dòng mang câu `vi_sao` |
| `Tất cả` | 3.772 | |

⇒ Cổng `G-a` *(danh sách mặc định `738`)* **ĐẠT**.

#### ⓔ ⭐⭐⭐ Hộp thoại **BỎ GÁN** khi dòng tiền mang **chùm**

Cửa `unmatch` bỏ **TOÀN BỘ** mối nối của một dòng tiền *(`QĐ-ITL-69`)*. Owner chốt **giữ cửa, màn nói ra thiệt hại**.

| Đo `21/09` | |
|---|--:|
| Dòng tiền đã có mối nối | 2.222 |
| ⭐ Mang chùm *(>1)* | **25** = **1,1%** |
| Chùm lớn nhất | **10** dòng lệnh |

| Ca | Màn làm gì |
|---|---|
| **`98,9%`** — dòng tiền chỉ nối `1` lệnh | Bấm `Bỏ gán` ⇒ gỡ ngay. ⛔ **⛔ Không** hộp thoại — hỏi ở đây là hỏi thừa **2.197** lần |
| ⭐ **`1,1%`** — dòng tiền mang chùm | Gọi `GET /queue/{itl_id}/chum` ⇒ hộp thoại **liệt kê TÊN từng dòng lệnh** sắp bị gỡ, rồi mới hỏi |

⛔⛔ **⛔ Không được hỏi ở cả hai ca *"cho chắc"*.** Một hộp thoại bật `2.222` lần để đúng `25` lần là cách nhanh nhất dạy người ta bấm `OK` ⛔ không đọc — và khi ấy nó ⛔ không còn cản được gì ở đúng `25` lần cần cản.

⭐ **v4.8 — BÁO SAU khi bỏ gán *(⛔ hỏi trước)*** *(`fls-ba` 01/10 tối, `KQ-007 F-3`)*: cửa `unmatch` trả `bo_qua[]` = giá trị **người** đã gõ trên ô mà phép ghép từng gợi ý *(định nghĩa ở `BA-10` `DT-I14`)*. Bỏ gán xong mà `bo_qua` **⛔ rỗng** ⇒ màn ghép mở **một hộp báo** — một nút `Đã hiểu`, ⛔ nút huỷ *(việc đã xong, ⛔ còn gì để hỏi)* — cùng nội dung hộp *"Đã bỏ ghép"* của `F01` *(dòng `F01/F02 · nút Bỏ ghép` ở bảng cửa ↔ màn — **một** hàm dựng, ⛔ hai bản câu)*. `bo_qua` **rỗng** ⇒ ⛔ hộp nào, màn về lệnh như hôm nay.
- Vì sao báo: dòng tiền vừa **rời** lệnh chi nhưng ô `hd`/`cdt1` **vẫn giữ** giá trị người gõ lúc còn ghép — giá trị ấy có thể đã sai theo. Giấu đi thì kế toán tưởng bỏ gán đã dọn sạch *(lý do `bo_qua` **phải hiện**)*.
- Vì sao ⛔ trái câu *"⛔ hỏi ở cả hai ca"* ngay trên: câu ấy cấm hộp **hỏi trước** để khỏi dạy người bấm `OK` mù. Hộp này **báo sau**, và **hiếm**: chỉ bật khi người đã gõ tay lên ô của một dòng đang ghép — đo 01/10 tối trên sổ thật: `fls_sua_tay` **0** dòng ⇒ hộp bật **0** lần hôm nay *(luật báo động hiếm: đếm trước khi bật)*.
- ⛔ Báo `but_toan_dao` *(gợi ý máy vừa rút)* trên màn ghép khi `bo_qua` rỗng: mỗi cú bỏ gán rút ~**2** gợi ý *(đo 01/10 tối: **4.424** gợi ý chưa đảo trên **2.219** dòng)* ⇒ báo nó là báo **mỗi lần** = tiếng ồn; gợi ý máy ⛔ bao giờ là Final *(`QĐ-ITL-149`)* nên rút nó ⛔ đổi gì người thấy ở cột Final.

⭐⭐ **v4.10 — NĂM ca của nút `Bỏ gán` trên màn ghép, và màn nói gì SAU cú bấm** *(`fls-ba` 02/10, `KQ-019` `F-1`…`F-4` — trong thẩm quyền spec: cách màn trình bày dữ liệu cửa **đã trả**; ⛔ đổi cửa, ⛔ đổi sổ, ⛔ đổi *"con số đến từ đâu"*)*

Vì sao có đoạn này: v4.0 khai *"hỏi trước ở ca chùm"*, v4.8 khai *"báo sau khi `bo_qua` ⛔ rỗng"* — nhưng ⛔ câu nào nói màn ghép hiện gì khi cú bỏ gán **xong mà `bo_qua` rỗng** *(hôm nay **100%** ca: `fls_sua_tay` **0** dòng, đo 02/10 chỉ `SELECT`)*, khi cửa **lỗi**, hay khi lệnh gắn **≥ 2** dòng tiền. Câu v4.8 *"màn về lệnh như hôm nay"* **ngầm giả định màn tự nói** — đo `KQ-019` trên máy `8099` *(kho TEST)*: sau `200` thẻ vẫn `Đã gán`, khối *"✓ Đang gán với giao dịch …"* còn nguyên, bấm lại ⇒ `409` im lặng. ⇒ Đính chính *(⛔ xoá câu v4.8)*: *"về lệnh như hôm nay"* đọc là **ca ③ dưới đây**. Và nhánh hỏi trước gọi `HT.hoi` — hàm **⛔ có**: `hop_thoai.js` xuất đúng **3** hàm `{ mo, dong, loi_trong_hop }`; đo 02/10 `grep HT\.<tên>` trong `fls/web/tep/*.js`: `HT.mo` **21** · `HT.loi_trong_hop` **9** · `HT.hoi` **2** chỗ gọi *(cả hai trong `man_f01_ghep.js::bo_gan`)* · **0** chỗ định nghĩa ⇒ hộp hỏi **⛔ bao giờ mở**.

| Ca | Đo 02/10 sổ thật *(`fls_moi_noi` **2.262** mối nối · **2.222** dòng tiền · **2.219** lệnh)* | Màn làm gì | ⛔ |
|---|--:|---|---|
| ① Lệnh gắn **≥ 2** dòng tiền | **23** lệnh | Hộp **báo** dựng bằng `HT.mo` — tiêu đề *"Lệnh này đang gắn N giao dịch"*; thân: FLS ⛔ tự chọn hộ bỏ giao dịch nào, hãy bỏ gán từ màn **Sổ ITL**; **một** nút `Đã hiểu`. **0** lượt `/chum`, **0** lượt `/unmatch` | bỏ đại một giao dịch *(`INV-I16`)* |
| ② Dòng tiền mang **chùm** *(`GET /queue/{itl_id}/chum` trả `can_hoi=true`)* | **25** dòng tiền | Hộp **hỏi** dựng bằng `HT.mo` — tiêu đề *"Bỏ gán sẽ gỡ CẢ N lệnh chi"*; thân liệt kê **từng** mã lệnh + số tiền + tiền tệ; **hai** nút theo thứ tự `Thôi` · `Gỡ cả N` *(nút sau `danger`)*. `Thôi` / `Esc` / bấm ra ngoài ⇒ **0** lượt `/unmatch` *(luật ⓒ của `hop_thoai.js`)*. `Gỡ cả N` ⇒ gọi `/unmatch` **bên trong** hàm của nút; cửa lỗi ⇒ `HT.loi_trong_hop(e)` + trả `false` ⇒ hộp **ở nguyên**, lỗi hiện **trong hộp** *(cùng khuôn `F01` ⑥ `_bo_ghep`)*; cửa `200` ⇒ đi tiếp ca ③ | gọi bất kỳ hàm hộp nào `hop_thoai.js` ⛔ xuất; thêm hàm hộp mới vào `hop_thoai.js` *(một lớp hộp thứ hai phải qua lại ba luật ⓐⓑⓒ — ⛔ trong việc này)* |
| ③ Bỏ gán **xong** *(`200`)* | mọi cú bỏ gán tới được cửa | ⓐ **Thẻ đổi tại chỗ, ngay**: mọi lệnh đang có trong danh sách màn mà `ma_lenh` ∈ `da_bo[].pm_line_id` của **thân trả** ⇒ bỏ `itl_id` vừa gỡ khỏi `itl_da_gan` và `gd_ds`; `itl_da_gan` hết ⇒ `trang_thai` · `trang_thai_nhan` · `trang_thai_mau` = **đúng bộ ba `khuon_the_lenh` trả cho lệnh ⛔ gán** *(`fls/repo/man_ghep.py::khuon_the_lenh` — hôm nay `chua_gan` · `Chưa gán` · rỗng)*. Hệ quả nhìn thấy: khối *"✓ Đang gán với giao dịch"* + nút `Bỏ gán` **biến mất**, nút `Gán` trở lại. ⓑ **Một dòng tín hiệu** trong khối hành động của lệnh: *"↩ Đã bỏ gán khỏi giao dịch #&lt;itl_id&gt; — lệnh về Chưa gán. Sổ giữ lịch sử."* *(chùm: thêm *"· gỡ cả N lệnh chi"*)* — **⛔ hộp**, ⛔ nút; mất khi mở lệnh khác. ⓒ `bo_qua` ⛔ rỗng ⇒ **thêm** hộp *"Đã bỏ ghép"* của `F01` *(v4.8 giữ nguyên)*. ⓓ Lệnh **ở yên** chỗ trong danh sách — kể cả đang ở chip `Đã gán` | để thẻ nói `Đã gán` sau `200`; nhảy sang lệnh kế; tải lại **cả** danh sách *(≤ **3.000** dòng, mất chỗ đứng — luật giữ chỗ `§4.5 ⓣ`)* |
| ④ Bỏ gán xong, **đọc lại ứng viên lỗi** *(`itl-candidates`)* | — | ⓐⓑⓒ của ③ **vẫn** xảy ra, và xảy ra **trước** lượt đọc lại; lượt đọc lỗi ⇒ thêm dòng *"Chưa tải lại được giao dịch gợi ý: &lt;câu cửa&gt;"* dưới dòng tín hiệu | nói *"bỏ gán lỗi"* — sổ **đã** ghi; để lỗi đọc lại nuốt hộp `bo_qua` |
| ⑤ Cửa `/chum` hoặc `/unmatch` **lỗi** *(`4xx` · `5xx` · mất kết nối)* ngoài hộp hỏi | — | Dòng lỗi trong khối hành động: *"Bỏ gán chưa xảy ra — Cửa lỗi: &lt;e.cau&gt;"* + `e.lam_gi` *(nếu có)* + `e.chi_tiet` chữ nhỏ *(cùng ba trường `HT.loi_trong_hop` đọc)*; thẻ **giữ** `Đã gán`; **0** hộp *"Đã bỏ ghép"*. `bo_gan` **⛔ ném** ra trình nghe `click` ⇒ **0** dòng `Uncaught` trên console | chỉ ghi console; thay cả màn bằng banner `ST.loi` *(đó là trạng thái lỗi của **danh sách**, ⛔ của một cú bấm)* |

**Năm trạng thái của vùng `Bỏ gán`** *(luật UIUX — mỗi màn đủ 5)*:

| Trạng thái | Hiện gì |
|---|---|
| tải | trong lúc chờ `/chum` hoặc `/unmatch`: nút `Bỏ gán` **khoá** *(`disabled`)* — hai cú bấm liền ⇒ **1** lượt `/unmatch` *(lượt thứ hai hôm nay ra `409` im lặng — `KQ-019`)* |
| rỗng | lệnh ⛔ gán ⇒ ⛔ có nút `Bỏ gán` *(như nay)* |
| lỗi | ca ⑤ *(ngoài hộp)* · ca ② *(trong hộp, hộp ở nguyên)* |
| mất kết nối | như lỗi, câu của `FLS-MAT-KET-NOI` *("Không nối được tới máy chủ FLS.")* |
| có dữ liệu | ca ③ *(+ ④ khi đọc lại lỗi)* |

⚠ **Nợ đã biết, ⛔ trong đoạn này:** cửa `unmatch` trả `409` cho *"⛔ còn mối nối để bỏ"* bằng mã `FLS-CONFLICT-SOURCE` *(`fls/repo/ghi_tay.py` lớp `KhongCoMoiNoi`)* ⇒ `goi_cua.js` dịch thành *"Giá trị bạn gõ khác với giá trị nguồn đang có."* — **sai nghĩa** cho cú bỏ gán. Ca ③ làm lượt bấm thứ hai **⛔ còn xảy ra** trên một màn; ca hai người bỏ gán cùng lúc vẫn gặp câu ấy *(dòng `e.chi_tiet` ở ca ⑤ mang câu thật của máy)*. Đổi mã lỗi = đổi hợp đồng cửa `BA-07` ⇒ phiếu khác.

⛔ Ký hiệu trong chữ mới: chỉ `↩` *(đã dùng ở hộp `F01`)* và `✓`; ⛔ `⛔ ⚠ ⭐ 🔒` *(luật `tests/web/test_luat_ky_hieu_man_hinh.py` — `man_f01_ghep.js` hôm nay ngoài danh sách `THEO_LUAT`, nhưng viết đúng từ đầu)*.

⭐⭐ **v4.11 — hộp đang mở là của NGƯỜI ĐANG ĐỌC NÓ: bàn phím ⛔ đi qua hộp, hộp đang ghi ⛔ đóng giữa chừng, và lỗi `409` nói đúng chuyện** *(`fls-ba` 02/10 khuya, `KQ-021` `F-1` · `F-2` + nợ `409` của v4.10 — trong thẩm quyền spec: cách màn **trình bày** + hợp đồng mã lỗi `BA-07`; ⛔ đổi sổ, ⛔ đổi *"con số đến từ đâu"*)*

Vì sao: vòng 2 của `WO-008` **mở** hai hộp trên màn ghép, và hai đường mới tới được *(đo `KQ-021`, Chrome `8099` phím thật)*: ⓐ hộp ①/② đang mở ⇒ `Esc` đóng hộp **và** đóng luôn lệnh *(`ST.mo` → `null`)* — trái câu `§4.5` *"`Esc` phải **bóc từng lớp một**"*; gõ `j` ⇒ màn **sau lưng hộp** đổi sang lệnh khác trong khi `Gỡ cả 2` vẫn gỡ lệnh cũ *(tầm: **88** lệnh ca ①/②)*. ⓑ bấm `Gỡ cả N` ⇒ cửa treo ⇒ `Esc` ⇒ hộp đóng ⇒ cửa lỗi ⇒ câu lỗi rơi vào `#dlg-b` của hộp **đã đóng**, màn **im** *(0 `Uncaught`)*. Gốc của ⓑ là luật ⓒ của `hop_thoai.js` *("`Esc` và bấm ra ngoài đóng hộp, và đóng hộp luôn là ⛔ làm gì")* — luật ấy **chỉ đúng TRƯỚC** khi bấm nút; **sau** khi nút đã gửi lượt ghi, đóng hộp ⛔ huỷ được lượt ghi đang bay ⇒ đóng hộp lúc ấy là **nói dối** *("không làm gì")*. Đo 02/10: `fls/web/tep` có **0** dòng `AbortController` / `timeout` *(cửa ⛔ có hạn chờ — `goi_cua.js:196` gọi `fetch` trần)*.

| # | Luật | Đo được bằng | ⛔ |
|---|---|---|---|
| ⓕ1 | **Hộp đang mở là MODAL với bàn phím.** Khi một hộp `HT.mo` đang mở, **mọi** phím tắt của màn sau lưng nằm im *(`j`/`k`/mũi tên/`Enter`/`/`/`Ctrl+Z`…)*; `Esc` **chỉ** đóng hộp *(một lớp)*, lệnh / ô đang chọn **ở nguyên**. Áp cho **mọi** màn có trình nghe phím trên `document` *(đo 02/10: `man_f01_ghep.js:968` · `man_f02.js:715`)*. Luật **⛔ được phụ thuộc thứ tự đăng ký** trình nghe *(trình nghe của `hop_thoai.js` gắn **lười** ở lần `HT.mo` đầu tiên — sau trình nghe của màn)* | bài đổi cả **hai** thứ tự đăng ký; `KQ-021` `test_F1_*` ×2 | `Esc` đóng hộp **và** lệnh; `j` đổi lệnh sau lưng hộp |
| ⓕ2 | **Hộp có nút đang chờ cửa ⛔ đóng bằng `Esc` / bấm ra ngoài.** Trong lúc hàng nút khoá *(hàm nút trả `Promise` chưa xong)*: `Esc` và bấm ra ngoài **bị nuốt**, hộp hiện thêm dòng *"Đang ghi vào sổ — chờ máy trả lời."*; cửa trả ⇒ đi đúng ca ② *(`200` ⇒ đóng + ca ③ · lỗi ⇒ `HT.loi_trong_hop`, hộp ở nguyên, nút mở lại)*. Luật ⓒ của `hop_thoai.js` đọc lại thành: *"`Esc` / bấm ngoài đóng hộp khi **chưa** có lượt ghi nào đang bay — và lúc ấy đóng là ⛔ làm gì"* | `KQ-021` `test_F2_*` | lỗi viết vào hộp đã đóng; màn im |
| ⓕ3 | **Cửa GHI có hạn chờ `30 giây`.** Quá hạn ⇒ lỗi mã **`FLS-HET-GIO`** *(mã **phía màn**, ⛔ của máy chủ — như `FLS-MAT-KET-NOI`)*, câu *"Máy chưa trả lời sau 30 giây — chưa biết lượt ghi đã vào sổ hay chưa."*, `lam_gi` *"Tải lại để xem trạng thái thật trước khi bấm lại."* — **⛔ được** nói *"chưa xảy ra"*: lượt ghi có thể **đã** vào sổ. Ca ⑤ của nút `Bỏ gán` với mã này in *"Chưa rõ bỏ gán đã xảy ra chưa — …"* thay *"Bỏ gán chưa xảy ra — …"*. ⭐ *(v4.23, `TL-056` — `HOI-056`)* **Cùng luật cho cú `Gán`** *(`§4.5 ⓦ` ⑤ ⓐ)*: mã `FLS-HET-GIO` ⇒ *"Chưa rõ gán đã xảy ra chưa — Cửa lỗi: &lt;e.cau&gt;"*; mã khác ⇒ *"Gán chưa xảy ra — Cửa lỗi: &lt;e.cau&gt;"* *(như v4.21)*. Khuôn chung cho **mọi** dòng lỗi một cú GHI mang tiền tố *"&lt;Việc&gt; chưa xảy ra — "*: với mã này tiền tố đổi thành *"Chưa rõ &lt;việc&gt; đã xảy ra chưa — "*; phần sau tiền tố *(`e.cau` + `e.lam_gi` + `e.chi_tiet`)* ⛔ đổi. Đếm 05/10 *(`fls-ba` `grep "chưa xảy ra — "` `fls/web/tep/` @ `12b7230`)*: đúng **2** nơi in tiền tố — `man_f01_ghep.js:725` *(`Gán`)* · `:1002` *(`Bỏ gán`)*; hộp `HT` *(`loi_trong_hop`)* ⛔ in tiền tố ⇒ ⛔ áp. Vì sao `30 s`: đó là trần để `ⓕ2` ⛔ nhốt người trong hộp mãi; lượt cửa chậm nhất **đã đo** trên sổ thật là một lượt **đọc** — **8,16 s** *(`lenh-cho`, `KQ-021`)* ⇒ `30 s` gấp **~3,7 lần** lượt chậm nhất, ⛔ cắt nhầm một lượt bình thường *(lượt **ghi** chưa ai đo giờ — `fls-dev` dán số đo vào `BG`)*. Cửa **đọc** ⛔ đổi trong lượt này. ⭐⭐ *(v4.24, `KQ-061 F-1` — **đính chính phép đếm "2 nơi"**)*: phép đếm tiền tố đếm **chuỗi**, ⛔ đếm **khẳng định** ⇒ sót **lô lưu `F02`** — hộp `Lô lưu DỪNG giữa chừng` *(`man_f02.js::_bao_hong` `:1044`)* in *"N ô dưới đây CHƯA vào sổ"* và dòng trạng thái *(`_bay` `:929`)* in *"N ô CHƯA vào sổ"* cho **cả** ô đang bay lúc hết giờ *(đo `KQ-061`: Chrome 8099 hạn thật **32,5 s**, thả lượt ⇒ cửa `200`, kho TEST `adj_id 4312` — ô **đã** vào sổ)*. Khuôn đọc lại: luật áp cho **mọi** câu khẳng định *"chưa xảy ra / chưa vào sổ / chưa ghi"* về một lượt ghi **đã gửi**, bất kể chữ. Lô lưu với mã này: ô **đang bay** *(ô đầu của phần còn lại — lô dừng ngay ở ô hỏng, `§3c ④`)* in riêng *"1 ô dưới đây CHƯA RÕ đã vào sổ chưa — máy đã gửi nhưng không nhận được trả lời:"* + dòng ô ấy; các ô **sau** nó *(chưa gửi — khẳng định **đúng**)* giữ *"M ô dưới đây CHƯA vào sổ"* + danh sách *(⛔ in khi `M = 0`)*; câu cuối hộp *"Bấm Thử lại: máy hỏi sổ trước khi ghi từng ô, nên ô đã vào sổ sẽ không bị ghi lần hai."* *(đúng nhờ `§3c ⑪ ⓓ` + cửa ghi `da_co`)*; dòng trạng thái *"1 ô chưa rõ đã vào sổ chưa"* + *" · M ô CHƯA vào sổ"* khi `M > 0`, lớp `crit` như nay; ô đang bay giữ viền vàng *(`chua-luu`)* kèm `title` *"chưa rõ đã vào sổ chưa"*. `e.cau` + `e.lam_gi` trong hộp ⛔ đổi. Mã khác ⇒ ⛔ đổi. ⚠ Đếm lại theo **chỗ gọi** *(`fls-ba` 06/10 @ `7b4237f`)*: `FLS.ghi(` ở `fls/web/tep` = **19** dòng = **18** chỗ gọi + **1** chú thích *(`man_f01_ghep.js:739`)* — `man_f01.js` 7 · `man_f01_ghep.js` 3 · `man_f01_lenh.js` 1 · `man_f02.js` 3 · `man_f04.js` 4; ngoài `F01G` ⑤ và lô lưu, chưa ai đọc **từng** chỗ còn lại in gì cho mã này ⇒ `WO-062` đòi Dev kiểm kê **18 / 18** theo **nghĩa**, ⛔ theo chuỗi | bài cửa giả treo quá hạn | nói *"chưa xảy ra"* khi ⛔ biết; hộp treo vô hạn |
| ⓕ4 | **Nợ `409` trả xong — mỗi chuyện một mã.** Mã `FLS-CONFLICT-SOURCE` hôm nay bị **bốn** lớp lỗi dùng chung *(`fls/repo/ghi_tay.py`: `KhacNguon` `:130` · `DaGhep` `:171` · `ChuaXong` `:178` · `KhongCoMoiNoi` `:200`)* ⇒ `goi_cua.js` dịch **cả bốn** thành *"Giá trị bạn gõ khác với giá trị nguồn đang có."* — đúng cho **một**, sai cho **ba** *(ghép dòng đã ghép · mở lại dòng chưa xong · bỏ gán dòng ⛔ còn mối nối)*. Tách thành ba mã mới, vẫn **`409`** *(`BA-07` **v3.5** §5)*: `FLS-DA-GHEP` *"Giao dịch này đã được gán với lệnh khác rồi."* / *"Tải lại để thấy lệnh đang gán; muốn đổi thì Bỏ gán trước rồi gán lại."* · `FLS-KHONG-CON-MOI-NOI` *"Giao dịch này không còn gán với lệnh nào — có thể vừa có người bỏ gán trước bạn."* / *"Tải lại lệnh để thấy trạng thái thật. Không cần làm gì thêm."* · `FLS-CHUA-XONG` *"Dòng này chưa từng được bấm Xong — không có gì để mở lại."* / *"Dòng vẫn ở hàng chờ; làm tiếp như bình thường."*. `FLS-CONFLICT-SOURCE` **chỉ** còn cho *"gõ khác nguồn"* *(`US-025`)* | bài `bao.py` + `goi_cua.js`: mỗi lớp lỗi ⇒ đúng mã ⇒ đúng câu | một mã cho bốn chuyện |
| ⓕ5 | *(đính chính ③ⓑ, `KQ-021` yếu #4 — ⛔ xoá câu cũ)* dòng tín hiệu *"↩ Đã bỏ gán…"* mất khi **rời** lệnh — **kể cả** quay lại **chính** lệnh ấy. Đó là hành vi đã đo trên `8099` và **được chấp nhận**: bằng chứng **bền** là thẻ đã về `Chưa gán` + nhật ký sổ; tín hiệu chỉ để người bấm **thấy ngay** | — | giữ tín hiệu qua các lần mở lệnh *(một dòng chữ sống lâu hơn việc nó báo là tiếng ồn)* |

⚠ ⛔ Trong đoạn này: đổi chữ ký `HT.mo` *(vẫn `mo(tieu_de, than, nut)`)*; thêm **hàm hộp** mới vào `hop_thoai.js` *(luật v4.10 giữ)*. Luật ⓕ1/ⓕ2 sửa **hành vi** của `hop_thoai.js` + trình nghe phím của màn — ⛔ thêm lớp hộp thứ hai.


---

### §4.3 · ⚰ BIA — đặc tả `§4` cũ *(v1.x–v3.1, giữ nguyên làm lịch sử)*

> ⛔ Khối dưới đây tả `SCR-F01` như **một lưới có năm hành động mỗi dòng**. Nó ⛔ **không còn là đặc tả sống** từ `CR#12`, nhưng **giữ nguyên chữ** — phần lớn nội dung của nó nay là đặc tả của **`SCR-F07`** *(§4.2)*, và sửa chữ trong một biên bản là viết lại lịch sử.

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
| ⭐⭐ UI-F7 | **NGÂN SÁCH TRƯỜNG.** Mỗi màn khai một **trần** số trường hiện cùng lúc — ⭐ **`F01` = `11`** *(owner nới `9 → 11` ngày `21/09`, `QĐ-ITL-147`)*. Thêm một ⇒ **bỏ một**. ⛔ Không có trần thì màn chỉ biết to lên — đo được: `man_f01_lenh.js` đi **`339 → 735` dòng qua 7 lần sửa trong 2 ngày**, ⛔ **không** lần nào tổng đi xuống. ⚠⚠ **Trần nới thì LUẬT ⛔ KHÔNG nới:** `11` là trần **mới**, ⛔ không phải *"trần co giãn được"* — lần sau thêm trường thứ `12` vẫn phải **bỏ một**, hoặc xin một quyết định nữa. ⛔ Một trần đổi được **không cần ai ký** thì nó ⛔ không phải trần |
| ⭐⭐ UI-F8 | ⛔ **Số của MÁY ⛔ không lên màn của NGƯỜI.** Danh sách đen: `hạng` · `luỹ kế %` · mọi `*_id` nội bộ · cờ `bool` · tên rổ · số dòng ảnh chụp · dấu thời gian dạng sê-ri *(`Timestamp = 45813.49394`)*. Luật nhận biết: một trường là **của người** nếu người ta **làm khác đi** tuỳ giá trị của nó |
| ⭐ UI-F9 | ⛔ **Một sự thật, một chỗ hiện.** Đo `18/09` trên `F01`: **8/36** trường là **bản sao nguyên văn** của trường khác — số chứng từ hiện dưới **3** tên, số tiền **3**, chủ dự toán **3** |
| ⭐⭐ UI-F10 | ⭐ *(v4.11, `KQ-021 F-3`)* **Tiền in đủ số lẻ CỦA TIỀN TỆ NÓ — ⛔ bao giờ làm tròn giá trị sổ khi in.** Số chữ số thập phân theo **ISO 4217** *(VND `0` · USD/SGD/HKD/EUR `2`)*; dấu `.` nghìn, `,` thập phân *(quy ước `vi-VN` đang dùng)*; tổng và lệch tính trên **số nguyên đơn vị nhỏ nhất**, ⛔ cộng số thực. Luật đủ ở **§5b** |

### §5b · ⭐⭐ `UI-F10` — in tiền theo tiền tệ *(v4.11, `fls-ba` 02/10 — `KQ-021 F-3`)*

**Vì sao có mục này.** Hàm in tiền dùng chung `TP.tien` *(`fls/web/tep/thanh_phan.js:29`–`:34`)* gọi `toLocaleString('vi-VN', { maximumFractionDigits: 0 })` cho **mọi** tiền tệ ⇒ mọi số lẻ bị **làm tròn về đơn vị**. Đo `KQ-021` trên máy `8099` *(kho TEST)*: chùm USD `1234.56` + `765.44` ⇒ hộp in **`1.235 USD`** · **`765 USD`**. Đo lại 02/10 khuya *(`fls-ba`, kho thật chỉ `SELECT`)* — **dòng sổ `fls_itl` có `ps_no` hoặc `ps_co` mang phần lẻ**, theo tiền tệ:

| Tiền tệ | Dòng sổ | Có phần lẻ | Lẻ tới chữ số thứ hai *(vd. `.56`)* | Mối nối `fls_moi_noi` có phần lẻ |
|---|--:|--:|--:|--:|
| USD | **3.980** | **2.413** *(60,6%)* | **2.123** | **72 / 218** |
| SGD | **145** | **74** | **54** | **4 / 5** |
| HKD | **20** | **20** | **18** | — |
| VND | **4.242** | **11** *(0,26%)* | **1** | **0 / 2.039** |

⚠ `KQ-021` ghi USD *"có phần lẻ **2.325** / 3.980"* — phép đếm của `KQ` ⛔ khai định nghĩa; con số ở bảng trên là định nghĩa **`ps_no` ∨ `ps_co` có phần lẻ** *(`ps_co` riêng: **2.095**; `ps_no` riêng: **318**)*. Kết luận ⛔ đổi: **đa số** dòng ngoại tệ đang in sai trên màn.

Hại thật là **đọc sai**, ⛔ ghi sai *(cửa ghi so số thật; `khop_dung_tien` so `Number` đủ lẻ)* — nhưng nó **trái thẳng** `QĐ-ITL-62` *(ngoại tệ ⛔ dung sai, **dù vài xu**)*: màn **giấu đúng vài xu ấy**. Đo `node` 02/10 trên chính lời gọi hôm nay: lệch `−0,40 USD` in thành **`-0`**; Σ hai dòng `0.10 + 0.20` trừ tiền bank `0.30` ra `5,55·10⁻¹⁷` ⇒ phép `Math.abs(lech) <= dung_sai` với dung sai ngoại tệ **0** ra **`false`** — hộp ghép nhiều dòng `F01` *(`man_f01.js` `_tinh`, `:353`–`:364`)* **khoá nút Ghép** trên một chùm **khớp đúng từng xu** *(cửa ghi sẽ nhận)*.

| # | Luật | Ví dụ *(chuỗi cửa trả → chữ trên màn)* | ⛔ |
|---|---|---|---|
| ⓐ | **Số chữ số thập phân = số lẻ ISO 4217 của tiền tệ**, **cố định** *(luôn đủ — cột số thẳng hàng, `UI-F3` `tabular-nums`)*. Bảng khai **một chỗ** *(hằng trong `thanh_phan.js`)*: `VND 0` · `USD 2` · `SGD 2` · `HKD 2` · `EUR 2` — đúng **5** mã cửa đang biết *(`man_f01_lenh.js:715` liệt kê cùng 5 mã)*. Khi `fls_tien_te(ma, so_le)` ra đời *(`BA-05` `DD-I11` ❶)* thì bảng này đọc từ đó | `"1234.56" USD` → `1.234,56` · `"1234" USD` → `1.234,00` · `"765.44" USD` → `765,44` · `"39457436" VND` → `39.457.436` · `"12.5" SGD` → `12,50` | in `1.235 USD`; in `1.234 USD` cho `1234.00` *(cột lệch hàng)* |
| ⓑ | ⭐ **⛔ bao giờ làm tròn giá trị sổ khi in.** Giá trị có **nhiều** chữ số lẻ hơn bảng ⓐ *(hôm nay: **11** dòng VND — vd. `1.306.103,80`)* ⇒ in **đủ** chữ số thật *(tối đa `2` = thang `numeric(20,2)` của kho)*. Đây là **mặc định**; câu còn treo `Q-TIEN-1` *(owner)* | `"1306103.80" VND` → `1.306.103,80` | in `1.306.104` — một số **⛔ có** trên sổ |
| ⓒ | ⭐ *(v4.13, `HOI-026` — một luật, ⛔ hai nhánh)* Tiền tệ **lạ hoặc thiếu** *(⛔ có trong bảng ⓐ — vd. `curr = '20'`: **71** dòng trong các ảnh `fls_pm_line`, có lẻ **0**; `NULL`)* ⇒ coi số lẻ bảng = **0**, ⛔ đoán tiền tệ: số nguyên in nguyên; có phần lẻ ⇒ in **đủ thang kho 2** — **đúng như nhánh ⓑ** của mã trong bảng. **Luật chung ⓐ+ⓑ+ⓒ:** số lẻ in = bảng của mã nếu giá trị vừa bảng, ngược lại = **2** *(kho `numeric(20,2)` ⇒ chữ số thật của giá trị sổ **là** 2)*. Mã tiền tệ in **nguyên văn** cạnh số như hôm nay | `"100.50" '20'` → `100,50` · `"100" '20'` → `100` · `"0.5" null` → `0,50` · `"1306103.8" VND` → `1.306.103,80` | in như USD *(`100,00`)*; ~~v4.11: `100,5`~~ — cắt số 0 đuôi làm một cột cùng mã có `100,5` cạnh `12,25`, dấu phẩy ⛔ thẳng hàng *(`UI-F3`)* |
| ⓓ | **Dấu phân cách:** `.` hàng nghìn, `,` thập phân *(quy ước `vi-VN` mà `TP.tien`/`TP.so` đã dùng; khớp mọi ví dụ trong spec — `15.000.000`, `39.457.436 VND`)*. Dấu âm **⛔ đổi** trong lượt này | `"-0.40" USD` → `-0,40` | đổi sang `1,234.56` kiểu Mỹ cho riêng ngoại tệ *(một màn hai quy ước = đọc nhầm nghìn thành lẻ)* |
| ⓔ | **Tiền tệ đi cùng số, tại chỗ gọi:** hàm in nhận **cả** giá trị lẫn mã tiền tệ — mọi chỗ gọi trong `fls/web/tep` *(đo 02/10: **38** chỗ `TP.tien`, trong **6** tệp màn)* truyền mã. Chỗ nào ⛔ biết tiền tệ ⇒ đó là **lỗi màn** *(⛔ cộng / so khác tiền tệ — §4.3 BIA)*, ⛔ lý do để gọi thiếu | — | gọi một đối số rồi để hàm đoán |
| ⓕ | ⭐ **Tổng và lệch trên màn tính bằng SỐ NGUYÊN đơn vị nhỏ nhất** *(xu — nhân `10^2`, làm tròn **một lần** khi đổi chuỗi cửa trả sang số nguyên)*, rồi mới in theo ⓐ. **Khớp ⇔ lệch = 0 trên số nguyên** *(ngoại tệ: `QĐ-ITL-62`)*; lệch **≠ 0** ⛔ bao giờ in thành `0` / `-0` / `0,00` ⭐ *(v4.13, `HOI-026`)* **Con số in cạnh một phép so là đúng con số đã đem so:** dung sai so bằng **sàn** xu *(`TP.xu(ds, 'san')` — luật cửa ghi `QĐ-ITL-63`)* ⇒ in **`TP.tien(TP.chuoi_xu(sàn), cur)`**, ⛔ in chuỗi cửa trả *(làm tròn nửa-ra-xa ⇒ lệch 1 xu với phép so)* ⭐⭐ *(v4.14, `KQ-031` `F-1` + `F-2`)* **Lệch CHỈ có khi CÙNG tiền tệ.** Hai số khác tiền tệ ⛔ bao giờ trừ nhau *(`QĐ-ITL-62`; cửa ghi `ghep_lenh` ném `KhacTienTe` — `fls/repo/ghi_tay.py:746`, `BA-07 §3` dòng `match`: *"tiền tệ khác `422` (kiểm TRƯỚC Σ)"*)* ⇒ màn so **mã tiền tệ TRƯỚC** khi đổi sang xu *(mã so sau `trim` + chữ hoa — như `F01G.khop_dung_tien`)*. Khác mã ⇒ ô `Lệch` in chữ **`khác tiền tệ`** *(⛔ một con số, ⛔ `—`)*; câu so in hai số **kèm mã** và kết luận *"⇒ ⛔ khác tiền tệ — cửa ghi sẽ TỪ CHỐI"*, lớp `crit`; nhãn xác nhận gán ⛔ nói *"trong dung sai"* / ⛔ một *"(lệch …)"*, mà nói *"(khác tiền tệ — cửa ghi sẽ từ chối)"*. Ký hiệu **`—`** để dành cho **thiếu số** *(một bên `amount`/`curr` rỗng)* — hai nghĩa ⛔ chung một ký hiệu *(`INV-I16`)*. Ô bảng đọc `lech` của cửa *(`BA-07 §4h ⓵` **v3.7**: số ở **mọi** bậc khi cùng tiền tệ, `null` ⇔ ⛔ so được)*; câu so trong hộp tự tính trên xu như trên. Tầm sổ thật *(`KQ-031`, rổ `may` **268** lệnh, đo qua cửa thật 8088)*: **165 / 5.360** ứng viên khác tiền tệ lệnh — hôm nay in một *"lệch"* trừ hai đơn vị *(vd. `8.000 USD` ↔ `206.000.000 VND`)*; **4** lệnh có ứng viên bậc `ma` khác tiền tệ **cùng số** ⇒ hộp nói *"lệch 0 ⇒ trong dung sai"* cho cặp cửa ghi **từ chối** | Σ `0.10 + 0.20` vs bank `0.30` USD ⇒ lệch `0,00`, **khớp**; `1234.56` vs `1234.16` ⇒ lệch `0,40 USD`, **⛔ khớp** · dung sai `"617.285"` VND ⇒ in `617,28`; lệch `617,29` ⇒ **⛔ khớp** *(chữ và phép so cùng một số)* · ⭐ lệnh `"100000" VND` ↔ ứng viên `"100000.00" USD` ⇒ ô `Lệch` **`khác tiền tệ`**, câu *"tiền lệnh 100.000 VND ↔ tiền bank 100.000,00 USD · khác tiền tệ ⇒ ⛔ cửa ghi sẽ TỪ CHỐI"* | cộng `Number` rồi so `<= 0`; in lệch `-0`; in dung sai `617,29` cạnh *"⛔ lệch quá dung sai"* cho lệch `617,29` · ⭐ in *"lệch 0 ⇒ trong dung sai"* cho cặp VND↔USD cùng số *(8088 `PM00329-1`)*; in `12.890,00` = `14.800 HKD − 1.910 USD` *(8088 `PM01089-1`)*; in `—` cho ứng viên bậc `ma` cùng tiền tệ mà lệch thật `21.586,78` *(8088 `PM02117-1`)* |
| ⓖ | Hàm in **⛔ dùng để TÍNH** *(luật cũ đầu hàm `tien`, giữ)*; con số **gửi lên cửa** vẫn là chuỗi cửa trả, ⛔ chuỗi đã in | — | gửi `"1.234,56"` lên cửa |
| ⓗ | `TP.so` *(đếm dòng, phần trăm)* **⛔ đổi** — ⛔ phải tiền | — | — |
| ⓘ | ⭐⭐ *(v4.13, `HOI-026`)* **Ô tiền rộng theo NGÂN SÁCH KÝ TỰ đo trên sổ thật, ở phông RỘNG NHẤT của `--mono`.** Ngân sách hôm nay = **18** ký tự *(chuỗi ô in `TP.tien(v, curr) + ' ' + curr` dài nhất: lệnh `103.950.000,00 USD` · sổ `11.742.361.787 VND` — đo 02/10, `HOI-026` TL)*; một ký tự `--mono` ở `--fs-than` `12.5px` rộng tối đa **7,5px** *(`IBM Plex Mono` 0,600em — `fls/web` ⛔ có `@font-face`, chữ ra phông cài trên máy: `Cascadia Mono` 7,32 · `Consolas` 6,88)* ⇒ ô ≥ `18 × 7,5 = 135` ⇒ **`136px`**. Áp cho **mọi** ô tiền có bề rộng cố định — hôm nay: bảng danh sách lệnh `.mcols` cột `Số tiền` *(~~`108px`~~)* và `Số tiền GD` *(~~`116px`~~)* · ⭐ *(v4.14, `KQ-029` `F-3`)* vùng ứng viên màn ghép `.cand-cols` *(`hinh.css:747`)* cột số tiền **`160px`** cố định ở **cả ba** bề rộng khung *(`:747` · `@container ≤900px` · `≤700px`)* ⇒ ô chữ `.cand .amt>span` = `160 − 18` *(ô `Nợ/Có`)* `− 5` *(khe)* = **`137px` ≥ 135** ✔ *(đo `KQ-029` 8088: 18 ký tự Cascadia `131,8` · `0,6em` `135` ⇒ ⛔ cắt)* — đã có `ellipsis`, **thiếu `title`** ⇒ thêm `title` = đúng chuỗi in; ~~nhãn lệch `.cand .amt .lech` cùng luật~~ *(⛔ v4.16, `KQ-036 F-5 ⓒ`: JS ⛔ sinh phần tử `.cand .amt .lech` từ 23/09 — đo **0** phần tử; lệch in ở cột `Lệch` riêng)*. Ô tiền **co giãn** *(`minmax`/`1fr`)* ⛔ thuộc ⓘ. Chuỗi **vượt** ngân sách ⇒ ô in `…` cuối + `title` = chuỗi đủ — **lưới an toàn**, ⛔ cách hiển thị thường *(hôm nay **0** dòng)*; ⛔ bao giờ cắt **im lặng**. Đổi `--fs-than` hoặc phông `--mono` ⇒ tính lại ô | `11.742.361.787 VND` vừa ô `136px` | ô `108px` in `2.259.942,94 US` / `11.742.361.78…` *(**426** dòng lệnh VND ≥ 15 ký tự cắt **từ trước** `WO-022`)*; rút gọn `11,7 tỷ` *(trái ⓑ)*; hạ cỡ chữ về `--fs-phu` *(tiền là thứ đọc để LÀM VIỆC)* |
| ⓙ | ⭐ *(v4.14, `KQ-031` `F-1`)* **Một bảng mà các dòng CÓ THỂ khác tiền tệ với nhau hoặc với dòng ghim ⇒ ô tiền in KÈM MÃ** *(`TP.tien(v, curr) + ' ' + curr`)*. Hôm nay: hộp *Tìm tiền* `F01L` cột `Tiền` *(ứng viên bậc `ma` khớp **mã**, ⛔ lọc tiền tệ — **165 / 5.360** ứng viên khác tiền tệ lệnh, `KQ-031`)* in `100.000,00` trần cạnh lệnh `100.000 VND` — chỉ phần lẻ `,00` lộ ra là ngoại tệ. Vùng ứng viên `F01G` *(`.cand .amt`)* **đã** in kèm mã — giữ. Ngân sách ⓘ đã tính **cả** mã *(18 ký tự = số + dấu cách + 3 chữ)* | ứng viên `"100000.00" USD` ⇒ ô `100.000,00 USD` | in `100.000,00` cạnh dòng ghim `100.000 VND` *(mắt đọc hai số **bằng nhau**)* |

**Năm trạng thái** *(luật này là cách **in** một ô — ⛔ thêm trạng thái màn)*: tải · lỗi · mất kết nối **⛔ đổi**; **rỗng** = ô ⛔ giá trị in `—` *(như nay)*; **có dữ liệu** = luật ⓐ…ⓕ + ⓙ. ⭐ *(v4.14, `KQ-031` `F-4` + `KQ-029` `F-2`)* Trạng thái **rỗng của MÀN** *(cửa trả `data: null` / thân rỗng — chế độ `?gia_lap=rong`)* phải **vẽ được** ở mọi hộp/khối đọc thân ấy: hộp *Tìm tiền* `F01L` mở ra câu rỗng *"⛔ Không có dòng tiền nào ứng"* *(cùng câu nhánh `uv.length = 0` đã có)*, khối `#nap-chon` `F04` in câu rỗng của `F04` — ⛔ `TypeError` *(hôm nay: `man_f01_lenh.js:578` đọc `d.ung_vien` khi `d = null` · `man_f04.js:894` đọc `d.nguon` khi `d = null`)*. Cửa thật hôm nay ⛔ trả `data: null` với `200` *(lệnh lạ ⇒ `404`)* ⇒ chỉ chạm chế độ giả lập — nhưng giả lập là **bằng chứng duy nhất** năm trạng thái có thật.


---

## §7 · ⭐⭐⭐ `SCR-F04` **Nạp sao kê** — màn nhập ngân hàng *(mới 2026-09-07, `CR#11`)*

> ⛔⛔ **VA CHẠM DANH TÍNH — xử ngay ở dòng đầu, ⛔ không để ai vấp sau.** `§2` của chính tệp này có một dòng **`SCR-F04` = *"Xu hướng nhãn"* — đã BỎ HẲN** *(v1.5, 25/08)*. Nay `CR#10` + `QĐ-ITL-90` đặt tên **`F04`** cho **màn nhập `Bank Transactions`**, và cái tên ấy đã đi vào **~10 tệp tài liệu + mã nguồn** *(`fls/adapters/sao_ke.py`)* + sổ commit.
>
> ⇒ **Chốt: `SCR-F04` từ nay CHỈ có nghĩa MÀN NẠP SAO KÊ.** Nghĩa cũ **khai tử**, và dòng ở `§2` giữ lại **làm bia**, ⛔ không xoá — xoá đi thì phiên sau đọc `SCR-F04` ở tài liệu cũ sẽ hiểu nhầm mà ⛔ không có gì cản. ⚠ Đây đúng lớp lỗi đã ghi sáng nay ở `06 §6.-1` *(hai dòng cùng số `17`)*: **số thứ tự ⛔ không tự nó là danh tính** — phải có người tuyên bố.

### ⓵ Màn này thay đúng MỘT việc

```
HÔM NAY:  kế toán dán sao kê vào 60 sheet `R |`  →  bấm `Run`  →  ⛔ im lặng
                                                                  ↓
                                            ⛔ cú chép tay sang A-CCR (trễ 19 ngày)

TO-BE:    kế toán DÁN vào `R |` y như cũ  →  công thức của sheet chuẩn hoá
                                              ↓  (⛔ hai bước trên KHÔNG đổi)
          FLS: chọn phạm vi  →  ĐỌC vùng CHUẨN  →  ⭐ SOÁT 9 luật (GỘP)  →  nhận
```

> ⛔⛔ **SỬA 2026-09-08 — `QĐ-ITL-109`.** Bản v2.5 vẽ TO-BE là *"kế toán **TẢI TỆP lên** → khai cột → soát"*. **Sai mô hình.** Owner chốt FLS đọc **vùng CHUẨN** của sheet, ⛔ **không** thay phép chuẩn hoá ⇒ cử chỉ nhập **ở lại Google Sheets**, và `F04` ⛔ **không có một ô nhập nào** cho dữ liệu giao dịch.
>
> ⭐ Lý do ranh giới ấy được **ký thành quyết định** chứ ⛔ không để tuỳ nghi: đo sống 60 nguồn bank thì **36** nguồn bóc ngày bằng công thức riêng và **23** nguồn **ĐỔI DẤU** *(`Credit = <cột thô> × (−1)`, kèm hoán vế Nợ ↔ Có)*. Chở 60 phép biến đổi ấy sang FLS là mở một chỗ để **sai DẤU tiền**.
>
> ⭐⭐ **Và `⓹` của chính tệp này HOÁ RA ĐÚNG NGAY TỪ ĐẦU.** Nó ghi **4/8** và loại **#2 dán vùng** với lý do *"màn này ⛔ không phải chỗ GÕ"*. Bản vẽ 08/09 sáng gọi lý do ấy là **sai** và đẩy lên **5/8** — ⛔ **cái sai là bản vẽ**, ⛔ không phải đặc tả. Giữ nguyên **4/8**; ghi lại đây làm bia.

⛔ **⛔ KHÔNG thay việc gõ tay của kế toán ở chỗ khác**, ⛔ không đụng `P100` *(`QĐ-ITL-34`)*.

### ⓶ Năm trạng thái — và trạng thái ③ là lý do màn này tồn tại

| # | Trạng thái | Màn hiện gì |
|--:|---|---|
| ① | **Chọn phạm vi** ⭐ *(sửa 08/09)* | danh sách **75 nguồn** *(`fls_source`, đo 09/09 — trong đó **65** `src_type='Bank'`)*, mặc định **tick tất cả** — vì nút `Run` hôm nay cũng gom cả lượt. ⚠ Bản trước ghi **68**: con số ấy **đúng lúc đo 08/09** và **⛔ không** được gõ lại bằng tay ở đây nữa — nó là thứ `kiem_so_song` phải ghim. ⚠⚠ Nguồn `InActive`/`Closed` hiện **mờ, bỏ tick sẵn**, ⛔ **không giấu**: giấu thì *thiếu sheet* và *đóng hợp lệ* trông giống hệt nhau — ⛔ **NHƯNG câu này ⛔ CHƯA DỰNG ĐỦ ĐƯỢC**, xem `⓶b` |
| ② | **FLS đọc** ⭐ *(sửa 08/09)* | số nguồn đọc được · số dòng · **dấu thời điểm đọc** · lưới xem trước **6 cột vùng CHUẨN, CHỈ-ĐỌC**. ⛔ Bản v2.5 ghi *"đã chọn tệp · 10 dòng đầu dạng thô"* — ⛔ **không còn đúng**: FLS ⛔ không nhận tệp, và ⛔ không đọc vùng thô. ⚠ *Sửa 08/09 chiều:* màn đọc **một ẢNH CHỤP** *(`QĐ-ITL-110`)*, ⛔ không gọi Sheets — xem `⓶b` |
| **②b** | ⭐⭐⭐ **CÁCH ĐỌC NGÀY của từng nguồn** *(mới 08/09 — `QĐ-ITL-113`)* | Bảng các nguồn có ngày **đọc được hai cách**: đã khai gì · **bằng chứng máy đo được, kèm CON SỐ** · **hai** nút ấn định *(`ngày/tháng` · `tháng/ngày`)*, nút máy đề xuất được **đánh dấu**. ⛔⛔ **Máy ĐỀ XUẤT, ⛔ KHÔNG QUYẾT** — quyền ấn định kỳ kế toán ở **người**. ⛔ **Một nút duy nhất** *"khai theo đề xuất"* là **máy quyết** khoác áo một cú bấm của người. ⭐⭐⭐ **Và từ 09/09 (`QĐ-ITL-117`) khối này CÓ một cú bấm GỘP — nhưng nó ⛔ KHÔNG phải nút *"khai tất cả"*.** Câu cũ ở đây *(⛔ không nút gộp, vì "một nút gộp là một nút được bấm mà ⛔ không ai đọc")* **bị hẹp** sau một phép đo: **34/34** nguồn chuỗi **tự chứng minh bằng dữ liệu của chính nó** *(2.296 dòng có phần không thể là tháng; `chac_dmy` = **0** khắp 60 nguồn; mâu thuẫn **0**)* ⇒ máy đề xuất `mdy` **34 lần, 34 lần một đáp án**, và bắt người bấm **27** cú để trả lời một câu dữ liệu đã tự trả lời là bắt họ **bấm theo phản xạ** — **đúng cái lo cũ**, chỉ tốn thêm 26 cú. ⇒ Nút gộp **chỉ nhận nguồn TỰ CHỨNG**, mang **ba con số** *(bao nhiêu nguồn · bao nhiêu dòng làm chứng · bao nhiêu dòng mơ hồ sẽ vào sổ)*, và cửa nó gọi ⛔ **không nhận `thu_tu`** ⇒ màn ⛔ **không có đường nào** chọn hộ thứ tự. Nguồn ⛔ không tự chứng hiện ở một ghi chú **nêu TÊN** + phải ấn định **từng nguồn** ở bảng dưới. ⭐ Hệ quả nêu bằng **con số**: *"n nguồn chưa khai · m dòng sẽ vào hàng loại · các dòng còn lại **vẫn vào sổ**"* — câu *"có thể một số dòng bị loại"* ⛔ **không giúp ai quyết định gì**. ⛔ `chưa khai` hiện **thành chữ**, ⛔ không hiện ô trống *(ô trống đọc y hệt *"⛔ không áp dụng"*)*; nguồn ⛔ **không cần** khai hiện ở **một ghi chú riêng** *(cùng khuôn *"nguồn đọc ra 0 dòng"*)* — lọc hẳn thì kế toán ⛔ không biết máy **đã soi** chúng |
| ③ | ⭐ **BẢN KHAI — để XEM** *(sửa 08/09)* | ánh xạ **trường → cột** kèm `version` · người khai · mốc hiệu lực. ⛔ **⛔ Không phải một bước của mỗi lần nạp** — nó là **cấu hình của nguồn**, đặt một lần. Sửa khai nằm sau **nút riêng**, vì nó sinh `version` mới |
| ④ | ⭐⭐⭐ **BIÊN BẢN SOÁT — GỘP** ⭐ *(sửa 09/09)* | **9** luật `S1`…`S8` + `S10`, mỗi luật **một dòng**: **hạng · đạt/đỏ · ĐÃ ĐO BAO NHIÊU · thông điệp · ⭐ NGUỒN DÍNH**. ⛔⛔ Bản `v2.5`–`v2.9` ghi *"8 luật `S1`…`S8`"* — **sai từ 08/09**: `S10` *(hai bản khai trỏ **cùng một cột**)* thêm vào từ `GAP-KHAI-01`, và `S9` *(số dư)* **chỉ** áp cho lằn quỹ. ⭐⭐⭐ Và từ `QĐ-ITL-112` nó là biên bản **GỘP**: 60 nguồn × 9 luật = **540** kết quả cuộn lên **9 dòng**, mỗi dòng **bung ra** đúng tên nguồn dính. Dải đầu nói **`n vào sổ · m bị chừa`**; `hạng` = **nặng nhất** trong 60; `Đã đo` = **Σ** của 60 *(⛔ không phải của nguồn đầu)*. ⛔⛔ Hai ô nguồn-dính là **HAI** thứ ⛔ không được lẫn: `nguồn ⛔ không đạt` *(đo được mà đỏ)* ≠ `nguồn chưa đo` *(đọc ra **0 dòng** — **10/60** nguồn thật, tài khoản đã mở mà chưa dùng, ⛔ **không** phải khuyết tật)*. Gộp bằng `all(dat)` thì **6/9** luật ĐỎ oan vì 10 tài khoản rỗng, và **một báo động đỏ oan là một báo động sẽ bị bỏ qua** |
| ⑤ | **Đã nhận** | `run_id` · số dòng vào sổ · số dòng vào **hàng chờ** · liên kết sang `SCR-F01` |

### ⓶b · ⭐⭐⭐ MỖI TRẠNG THÁI ĐI QUA CỬA NÀO — ✅ **cả 5 cửa NAY ĐÃ CÓ** *(đóng 09/09; bảng dưới giữ nguyên làm BIA của phép đo 08/09)*

> ✅ **Đo lại 09/09** *(`tools/soi_bang_tuyen.py`)*: **29** tuyến, và cả **5** cửa của năm trạng thái **đều tồn tại** — `20 → 24` *(`QĐ-ITL-110`, lằn ảnh chụp)* → `26` *(`113`, thứ tự ngày)* → `28` *(`111`/`112`, nạp cả lô)* → **29** *(`117`, khai thứ tự cả lô)*. ⭐ Màn nay **LUÔN** đi đường **lô** *(`POST /nap/lo/xem-truoc` + `POST /nap/lo` — `BA-07 §4f`)*, kể cả khi tick **một** nguồn: giữ hai đường là giữ **hai chỗ để chúng lệch nhau**, và cái lệch ấy hiện ra dưới dạng *"soát thấy 9 luật xanh, nạp ra số khác"*.
>
> ⛔⛔ **Nhưng bảng dưới ⛔ KHÔNG bị xoá.** Nó là bằng chứng của một hình bệnh sẽ trở lại: **năm trạng thái ấy được viết mà ⛔ không ai soi xuống bảng tuyến**, nên `3/5` cửa ⛔ không tồn tại trong khi tài liệu màn hình đọc như một màn **đã chạy được**. ⇒ Từ 09/09 có cổng `test_ba07_phu_het_tuyen` canh **hai chiều** *(cửa thật mà hợp đồng ⛔ không nói · đường hợp đồng nói mà ⛔ chưa tồn tại phải mang `⬜`)* — và ngay lần chạy đầu nó bắt **2** tuyến *(`/nap/lo`, `/nap/lo/xem-truoc`)* sống trọn một ngày ngoài hợp đồng.

⛔⛔ **Năm trạng thái ở trên được viết mà ⛔ KHÔNG ai soi xuống bảng tuyến.** Soi ngày 08/09 *(`tools/soi_bang_tuyen.py` — **20** tuyến thật)*:

| Trạng thái | Cần cửa gì | Có? |
|:--:|---|:--:|
| ① | `GET /sources` — 68 nguồn, bản khai, lần đọc cuối | ⛔ **KHÔNG** |
| ② | một đường đọc **vùng CHUẨN** | ⛔ **KHÔNG** |
| ③ | `GET /sources/{id}/khai-cot` | ⛔ **chỉ có `POST`** |
| ④ | `POST /nap/xem-truoc` | ✅ có |
| ⑤ | `POST /nap` | ✅ có |

⛔ **Và hai cửa CÓ thì vẫn ⛔ không chạy được**, vì cả hai đòi người gọi **đưa sẵn `dong`** vào thân yêu cầu — tiền đề *"màn hình đã cầm tệp trong tay người dùng"* của `QĐ-ITL-105` ⓷, thứ mà **`QĐ-ITL-109` đã lật**. Trình duyệt ⛔ không đọc được Google Sheets ⇒ **⛔ không có đường nào đưa dữ liệu vào**.

⭐ **`QĐ-ITL-110` mở đường:** phép đọc 60 sheet đi qua **một ẢNH CHỤP trong kho**; màn `F04` đọc ảnh chụp, ⛔ không gọi Sheets. Bốn tuyến mới ở `BA-07` **§4c** *(**20 → 24**)*.

⛔⛔ **Hai câu của đặc tả này ⛔ CHƯA DỰNG ĐỦ ĐƯỢC, và tôi ⛔ không im lặng vẽ quanh chúng:**

| Câu | Đo được gì | GAP |
|---|---|---|
| ① *"nguồn `InActive`/`Closed` hiện mờ"* | `fls_source` có **7 cột** *(`source_id`·`source_key`·`src_type`·`last_seen_at`·`lag_days`·`cutoff_date`·`txn_count`)* — ⛔ **không cột nào là trạng thái**. `Account Status` *(`Closed` **10** · `InActive` **5**)* chỉ được đọc **SỐNG** từ sheet AS-IS ở `fls/kiem/nguon_song.py` `L8`, ⛔ chưa bao giờ vào kho | `GAP-CHUP-02` |
| ② lưới xem trước *"**6 cột** vùng CHUẨN"* | ⭐⭐ **SỬA 17/09 — `QĐ-ITL-128` LẬT chỗ này: đủ `6/6` cột CÓ DỮ LIỆU.** Owner mở lại `QĐ-ITL-92` sau khi **đo cả hai vế** trên `58/60` sheet `R \|` *(`7.712` ô có chữ)*: dữ liệu người ~`4,3–4,8%` so với `23,0%` tín hiệu ghép ⇒ chốt hình **rộng nhất** — *nạp cả chuỗi, ⛔ không siết thêm*. ⇒ `TRUONG_DOC_DUOC == SAU_TRUONG` = **6/6**. ~~Câu cũ: *"chỉ 5 cột có dữ liệu, `TRUONG_DOC_DUOC` = 5/6"*~~ — **đúng tới 17/09**, giữ làm bia. ⛔⛔ Bản vẽ 08/09 vẽ nó **CÓ nội dung** *("THANH TOAN HD DV T7")* — **cái sai là BẢN VẼ**, ⛔ không phải đặc tả | `GAP-SCR-14` |

⭐ **Cách xử cột `Description`: GIỮ cột, ghi thẳng *"⛔ không đọc — `QĐ-ITL-92`"*.** ⛔ Bỏ cột đi thì *"cấm đọc"* và *"quên đọc"* **trông giống hệt nhau** — cùng lý do ① ⛔ không giấu nguồn `InActive`.

### ⓷ ⭐⭐ Trạng thái ③ — hình dạng lấy TỪ THỨ KẾ TOÁN ĐÃ TỰ LÀM

Đây ⛔ **không phải phát minh**: dòng 1 của mỗi sheet `R |` **đã là** một bản khai ánh xạ, kế toán tự duy trì, đo được **68/68 sheet khai đủ 6 trường** trên **19 bố cục cột** khác nhau *(đo trên kho 08/09; **16** nếu chỉ đếm **5 trường FLS thực đọc**. ⚠ Bản trước ghi **9** — con số ấy **đúng** nhưng chỉ nhìn **3/6 trường**)*. Màn này chỉ **dời chỗ ở** của nó *(`DD-I10`)*.

| Luật của ③ | Vì sao |
|---|---|
| ⛔ **Đủ 6 trường mới cho đi tiếp** — nút `Soát` **tắt** khi còn thiếu | `sao_ke.BanKhaiHong`. Nạp một phần = **mất cột trong im lặng**, và cột mất có thể là cột tiền |
| ⛔ **⛔ KHÔNG tự đoán từ tên tiêu đề** | Đoán đúng **59/60** vẫn là **sai tiền ở tài khoản thứ 60** |
| ⛔ **⛔ KHÔNG có bản khai mặc định** | Mặc định im lặng chính là cơ chế đẻ ra **6.843** ô *"Input here"* của AS-IS — sai mà ⛔ không ai thấy |
| ⭐ Đổi khai ⇒ **sinh `version` mới**, ⛔ không sửa đè | Dòng nạp tháng trước phải giải thích được bằng bản khai **hiệu lực lúc ấy** |

### ⓸ ⭐⭐⭐ Trạng thái ④ — BIÊN BẢN, ⛔ không phải một chữ *"OK"*

| Hạng | Màn làm gì | Nút `Nhận` |
|---|---|:--:|
| **`CHẶN`** đỏ | băng đỏ + tên luật + **⛔ 0 dòng sẽ vào sổ** | ⛔ **TẮT** |
| **`CỜ`** đỏ | vẫn đỏ, ghi rõ **bao nhiêu dòng** và **vì sao**, kèm câu *"những dòng này là **tiền thật**, chúng vào **hàng chờ có lý do**"* | ⭐ **BẬT** |
| **`CANH`** | dòng xám | bật |

⛔⛔ **Mỗi luật PHẢI hiện `đã đo bao nhiêu`.** *"Đạt"* mà ⛔ không nói đã đo mấy dòng là **chưa đo** — đây là luật nền của cả hai cổng, và nó **đã cứu một lần thật** *(`L6` cổng #17 báo đo `0` ⇒ đỏ, nếu không có luật này thì cổng **xanh giả**)*.

### ⓹ Hành vi Sheets bắt buộc — màn này cần **4/8**

| Cần | ⛔ Không cần | Vì sao |
|---|---|---|
| **7** số kiểu kế toán · **6** đông cứng tiêu đề · **5** filter view · **1** điều hướng bàn phím *(trên lưới xem trước)* | **2** dán vùng · **3** kéo xuống · **4** hoàn tác · **8** tự lưu | ⭐ Màn này **⛔ không phải chỗ GÕ** — nó là chỗ **NẠP và SOÁT**. Bốn hành vi kia thuộc `SCR-F02`. ⚠ Ghi ra để lần nghiệm thu ⛔ **không** trượt vì đòi đủ 8 ở sai màn |

### ⓺ ⛔ Màn này CỐ Ý ⛔ không có

| ⛔ Không có | Vì sao |
|---|---|
| ⛔ **Nút đẩy sang `A-CCR`** | Đó là **chặng 3**, và nó **chặn ở owner** *(`GAP-PLAN-05`)*. Dựng sẵn một nút chưa được phép bấm là **mời người bấm nhầm** |
| ⛔ **Sửa giá trị ô ngay trên màn nạp** | Sửa là **thêm bút toán** *(`INV-I08`)*, và chỗ sửa là `SCR-F02`. Cho sửa lúc nạp = **sửa nguồn trong im lặng**, mất đối chiếu với tệp gốc |
| ⛔ **Bước duyệt của người thứ hai** | `QĐ-ITL-27` — vận hành thật **2–3 kế toán**, ⛔ không có người thứ hai. Kiểm soát nằm ở **MÁY** *(biên bản ④)* |

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

### ⓒ ⚠⚠ Token của bàn giao `21/09` — `4` cái THẬT SỰ mới, `6` cái ĐỔI TÊN

⛔⛔ **Hợp đồng thiết kế khai *"kế thừa nguyên văn `fls/web/tep/tokens.css`"* — đo thì ⛔ không đúng với `6` cái.** Và đây đúng là bệnh `§7` mở đầu bằng cách chữa: **hai bản sự thật về cùng một thứ**. Lần này ⛔ không phải hai bộ **giá trị** *(giá trị trùng khít)* mà hai bộ **TÊN** — thứ lệch âm thầm hơn, vì mọi thứ vẫn hiện đúng màu cho tới lần ai đó sửa một chỗ mà ⛔ không biết chỗ kia tồn tại.

| Bàn giao gọi | Kho đang gọi | Xử |
|---|---|---|
| `--font-sans` ／ `--font-mono` | `--sans` ／ `--mono` | ⇒ **giữ tên kho**, sửa bản dựng |
| `--radius-sm` ／ `-md` ／ `-lg` ／ `-pill` | `--bo-nho` ／ `--bo` ／ `--bo-the` ／ `--bo-tron` | ⇒ **giữ tên kho** *(tiếng Việt là quy ước của cả tệp)* |

| Thật sự MỚI | Giá trị | Vì sao cần |
|---|---|---|
| `--hair` | `color-mix(in srgb, var(--line) 30%, var(--surface))` | ⭐ Đường kẻ giữa các dòng của **lưới dày** — `--line` quá đậm khi xếp 30–40 dòng |
| `--evi-bg` | `#0e757024` *(tối `#4bb5ad33`)* | ⭐⭐ Nền đánh dấu **BẰNG CHỨNG** *(số CT trùng · tiền khớp · tên vendor)* — nó là **màu ngữ nghĩa thứ năm**, ⛔ không phải một sắc nhạt của `--accent` |
| `--rail` | `clamp(300px,26vw,380px)` | ⚠ **Đè lên** `--panel-san 430px` ／ `--panel-tran 680px`. Hai bộ số ⛔ không cùng đúng ⇒ phải chọn **một** |
| `--shadow-card` | `0 1px 2px … , 0 4px 14px …` | Kho có `drawer` ／ `dlg` ／ `modal`, ⛔ **không có** bóng cho **thẻ** |

⚠ **`--b`** *(màu bậc của một dòng ứng viên)* cố ý đặt **inline theo dòng**, trỏ lại `good` ／ `info` ／ `warn` ／ `line` ⇒ ⛔ **không** là token thứ năm, và ⛔ không phải một mã màu mới.

✅ **ĐÃ hợp nhất `2026-09-22`** — `GAP-SCR-21` **ĐÓNG**. Vào `fls/web/tep/tokens.css`: `--hair` · `--evi-bg` · `--rail` · `--shadow-card` ＋ `--row-ghep` *(chiều cao dòng ứng viên `36px`, riêng khỏi `--row 30px` của lưới `F02`)*. ⛔ **Tên cũ của kho GIỮ NGUYÊN** — `--sans`/`--mono`/`--bo-*`, ⛔ không nhận `--font-sans`/`--radius-md` của bản giao: đổi tên là sửa **toàn hệ** *(`12` tệp dùng chung)* mà ⛔ không mua được một pixel nào. Qua `test_khong_ma_mau_go_tay`, và có thêm `test_moi_token_deu_duoc_khai` canh chiều ngược lại.

⛔⛔ **Và việc hợp nhất lộ ra một lỗi CÓ SẴN đã sống câm lặng ở ba chỗ.** `--accent-soft` được **dùng** trong `hinh.css` dòng `247` · `251` · `297` và **⛔ CHƯA BAO GIỜ được khai**:

| Dòng | Hệ quả thật |
|---|---|
| `247` `@keyframes soi` | hiệu ứng **soi dòng** chạy từ *trong suốt* sang *trong suốt* ⇒ **⛔ không thấy gì** |
| `251` `@media (prefers-reduced-motion)` | người **tắt chuyển động** đáng lẽ nhận một **nền tĩnh** thay animation — họ nhận **⛔ không gì cả** |
| `297` `.gapfold:hover` | hover của gấp-mở **⛔ không đổi nền** |

⭐⭐ Cổng màu canh *"có mã màu ngoài `tokens.css` ⛔ không"* — một câu hỏi **đúng**, nhưng chỉ **một chiều**. Chiều còn lại — *"tên token này có thật ⛔ không"* — thì **⛔ không ai hỏi**, và CSS **⛔ không bao giờ báo lỗi**: một `var(--khong-co)` chỉ lặng lẽ ⛔ không áp gì, y hệt như ⛔ chưa ai viết dòng ấy. ⇒ `tests/web/test_moi_token_deu_duoc_khai.py`, **diễn tập phá** chỉ thẳng cả ba dòng. `GAP-SCR-25`.

---

## §8 · Binding: màn · thành phần ↔ cửa API ↔ trường

> ⭐ Nối từng thành phần với **một cửa API có thật** *(`BA-07` v1.9)* và **trường
> trong phản hồi**. ⛔ Ô nào ⛔ không tìm được cửa thì đó là một **lỗ đặc tả**, ⛔ không
> phải *"dev tự lo"* — cột **Ghi chú** nói thẳng.

| Màn · thành phần | Cửa | Trường chính | Ghi chú |
|---|---|---|---|
| ⭐⭐⭐ **F01** · chọn chế độ `Tự động` ↔ `Thủ công` | `GET /queue/lenh-cho/summary` | `may · nguoi · khong · tu_chung · tong` | ⭐ Đo `18/09` bằng **chính hàm cửa gọi** *(`dem_theo_ro`)*: `may` **250** · `nguoi` **535** · `khong` **768** · `tu_chung` **47** · `tong` **1.553**. ⛔ Cửa đếm **TOÀN BỘ**, ⛔ không đếm trang đang xem |
| ⭐⭐ F01 · lằn **`Tự động`** | `GET /queue/lenh-cho/ro?ro=may&tu_chung=1` | `pm_line_id · ref_tho · amount · curr · ung_vien_itl[]` | ⭐⭐ **`tu_chung=1` là BẮT BUỘC, ⛔ không phải bộ lọc tiện tay.** `ro=may` **250** dòng, nhưng cửa GHI chỉ chắc chắn nhận **47** — `250` là một con số **hứa nhiều hơn cái bấm được**. `xu_ly.py` từ chối `tu_chung` đi kèm rổ khác *(`400`)* |
| ⭐⭐ F01 · lằn **`Thủ công`** | **HAI** lần gọi: `?ro=nguoi` **＋** `?ro=may&tu_chung=0` | như trên, cộng `vi_sao` rỗng | ⛔⛔ **⛔ KHÔNG có một cửa nào trả đúng `738`** — đó là **`535` ＋ `203`**, và `203` *(khớp mã, lệch tiền)* nằm trong rổ `may`. ⇒ Màn **cộng hai lời gọi**; một cửa gộp sẵn sẽ **giấu mất** rằng `203` dòng ấy máy **phải hỏi** *(`INV-I16`)*. ⚠ Mở `GAP-SCR-18` |
| ⛔ F01 · đích **Ghép ⛔ không được** | `GET /queue/lenh-cho/ro?ro=khong` | `vi_sao` **BẮT BUỘC** | **768** dòng. ⛔ **Không nút hành động nào** — đây là chỗ một dòng **rời** hàng chờ *(`INV-I20`)*. `vi_sao` do **MÁY** sinh *(`lenh_cho.VI_SAO`)*, và `QĐ-ITL-137` ⛔ **không** cắt nó |
| ⚠ F01 · đích **Lỗi nguồn** ⬜ | `GET /queue/loi-nguon` **⛔ CHƯA CÓ** | `pm_line_id · khuyet_tat[] · o_sai` | **167** dòng *(đo `18/09`)*. ⭐ Phải có **nút GỬI** — *chỉ mặt* mà ⛔ không có người nhận việc thì bằng ⛔ không |
| ⚰ F01 · ~~cột lý do + bộ đếm `US-045`~~ | ~~`POST /queue/{id}/reason`~~ | — | ⚰ **HOÃN `QĐ-ITL-137`** *(owner: «bỏ lý do, chưa cần»)*. ⛔ Cửa **⛔ không bị xoá** khỏi `BA-07`; chỉ **màn** ⛔ không vẽ nó. Lối ra nay đo bằng `fls_pm_link.hinh='T'` |
| ⚠ F01 · lằn **TIỀN** *(lằn CŨ, ⛔ không mặc định)* · lưới | `GET /queue?curr=&den_pct=` | `itl_id · doc_date · doc_no · curr · le · memo · tien` ＋ `hang · luy_ke_pct` | ⛔⛔ **`hang` · `luy_ke_pct` cửa VẪN trả, và màn ⛔ VẪN KHÔNG được IN chúng** *(`UI-F8`)* — chúng là **đầu vào của phép XẾP**, ⛔ không phải thuộc tính của khoản tiền. ⚠ Hai câu ấy ⛔ **không** mâu thuẫn, nhưng chúng **trông** mâu thuẫn, nên phải viết ra |
| ⚠ F01 lằn TIỀN · chân màn | `GET /queue/summary` | mảng **theo từng tiền tệ** | ⛔ **Không có dòng "tổng"** — cộng hai đơn vị tiền là một con số vô nghĩa |
| ⚠ F01 · nút Hoãn *(lằn TIỀN)* | `POST /queue/{id}/defer` | `until` · `so_lan_hoan` · `doi_mau` | lần 3 **đổi màu**, ⛔ không báo ai *(`QĐ-ITL-24`)* |
| F01 · nút **Ghép** → drawer | `GET /queue/{id}/pm-candidates` → `POST /queue/{id}/match` | ứng viên **4 bậc CÓ TÊN** *(`ma`/`tien`/`gan_tien`/`cung_tien_te`)* + `da_ghep` · thân `{pm_line_ids: [...]}` | ⛔ **Không** `{pm_id}` *(một PHIẾU)*: **526 phiếu mang 2–36 reference khác nhau** ⇒ ghép vào phiếu là **máy quyết thay người** *(`CR#6`)*. Kèm **TUỔI của ảnh chụp** |
| F01 · **Σ ở drawer ghép** | *(máy trả)* | `tien_bank · tong_lenh · dung_sai` | Lệch quá dung sai ⇒ **`422`, nút mờ**. Dung sai tay = **`min(1.000 đồng, 0,5%)`** *(`QĐ-ITL-63`)* — ⛔ khác dung sai máy |
| F01/F02 · nút ⭐ **Bỏ ghép** | `POST /queue/{id}/unmatch` | `da_bo[]` · `but_toan_dao[]` · ⭐ `bo_qua[]` | Hộp xác nhận phải nói **bỏ CẢ CHÙM** và **sổ giữ lịch sử**. ⭐ `bo_qua` = cái máy ⛔ KHÔNG rút *(người đã gõ tay)* — **phải hiện**. ⭐ *(v4.9, `HOI-016` ⓐ)* mỗi mục in **tên ô và giá trị người**: *"… người đã gõ tay lên đó sau khi ghép: `hd = HD-K7B`"* — câu cảnh báo giữ nguyên; người đọc thấy ngay giá trị máy ⛔ rút, ⛔ phải mở `F02` tra. ⭐ *(v4.8, `KQ-007 F-2`)* câu đảo nói theo **Ô**, ⛔ theo bút toán: *"↩ Đã rút gợi ý máy trên **N ô** (`cdt1, hd`)"* — mỗi tên ô **một lần**, theo thứ tự xuất hiện đầu tiên trong `but_toan_dao`; khi số bút toán **> N** thêm *"· M bút toán, gồm lớp gợi ý cũ bị đè"*. ⛔ In tên ô lặp *("cdt1, hd, hd, cdt1" — đo `KQ-007`, dòng 2 ô ra 4 tên)*: người đọc đếm ra 4 ô trên một dòng chỉ có 2. Màn ghép dùng **chính** hộp này khi `bo_qua` ⛔ rỗng *(mục ⓔ *Hộp thoại BỎ GÁN*, đoạn v4.8)* |
| F01/F02 · nút ⭐ **Xong** | `POST /queue/{id}/done` | `da_co · thieu_truong[] · ky_da_chot · ghi_de_ket_luan_may` | ⛔ **Không đòi lý do** *(`QĐ-ITL-72`)*. Bấm lại ⇒ `da_co=true` kèm **ai đã bấm · lúc nào** ⇒ hiện *"đã xong bởi X"* thay vì báo lỗi |
| F01/F02 · nút ⭐ **Mở lại** | `POST /queue/{id}/reopen` | `mo_lai_cua · xong_boi · xong_luc` | `reason` **BẮT BUỘC** · `409` nếu dòng ⛔ chưa từng xong |
| **F02** · lưới sổ | `GET /ledger?...` | ⭐ **24 cột nền** + **28 vị trí canon** *(tên tiếng Việt lấy từ khuôn canon qua `nhan_cua` — **một nguồn duy nhất**; danh sách ở `cot_so.CANON_LEN_LUOI`)* | **52 cột** = `len(cot_so.BANG_COT)` *(`QĐ-ITL-65`)*; `UNMAPPED` ⇒ `chưa gán` **nền vàng**, ⛔ không giá trị mặc định |

> ⛔⛔ **Ô trên từng ghi *"38 cột canon + 14 cột hợp đồng"* — TỔNG đúng, CÁCH CỘNG sai, và hai phép cộng ấy **cùng ra `52`** nên ⛔ không ai bắt được.** Đo thẳng ở mã 17/09: `BANG_COT` có **24** cột ⛔ không mang `canon=` và **28** cột mang — ⛔ **không phải** cả `38` vị trí canon *(lưới cố ý bỏ `9` vị trí `A·B·C·D·E·F·G·L·AG` vì chúng **đã là cột nền** — chú thích có sẵn trong `cot_so.py`)*, và ⛔ **không có** khối *"14 cột hợp đồng"* nào trên lưới. ⇒ Phép `C7` của `khop_owner.py` canh chỗ này.
| F02 · drawer nhóm 1–3 *(bối cảnh)* | `GET /ledger/{id}` | giao dịch gốc · chuỗi lệnh · đối soát pháp nhân | ⛔ Chỉ đọc. Thiếu bối cảnh thì ô sửa chỉ là **một dropdown đoán mò** |
| F02 · **7 ô sửa** | `GET /ledger/{id}/before-edit` → `POST /ledger/{id}/adjust` | `gia_tri · value_source ∈ {nguon, may_goi_y, sua_tay, UNMAPPED}` | Gõ khác nguồn ⇒ **`409`** + modal *"nguồn đang có X"* *(`US-025`)*; ghi đè cần **xác nhận + lý do** |
| F02 · **hoàn tác** | `POST /ledger/{id}/reverse` *(theo `adj_id`)* | `dao_cua · value_before` | Đảo là **thêm một dòng**, ⛔ không xoá. ⭐⭐ *(v4.12, `KQ-025 F-4`)* **Hộp `Đảo` nói hậu quả theo LỚP của bút toán bị đảo**, đọc từ `but_toan[].nguon` *(`GET /ledger/{itl_id}` — `BA-07` **v3.6**)*. Hôm nay hộp nói *"Sau khi đảo, giá trị lùi về bút toán trước đó, hay về giá trị của sổ gốc…"* cho **mọi** bút toán — kể cả gợi ý máy, nơi đảo **⛔ đổi Final** *(`QĐ-ITL-149`; đo `KQ-025` 8099 **A**: `fls_sua_tay` 0 → 0)*. Tầm: **4.424** nút `Đảo` trên dòng máy tới được trên sổ thật *(đo 02/10 khuya: bút toán `may_goi_y` chưa bị đảo)*. Câu đầu hộp giữ *("Đảo không xoá gì cả — nó thêm một dòng nữa trỏ ngược lại")*; câu **hậu quả** theo bảng: ⓐ `nguon = may_goi_y` ⇒ tiêu đề *"Rút gợi ý máy #N"*; *"Đây là gợi ý của máy, không phải giá trị người đã chốt. Rút nó **không đổi Final** — Final vẫn là giá trị người đã gõ, hay giá trị của sổ gốc."*; ⓑ `nguon = sua_tay` ⇒ tiêu đề *"Đảo bút toán #N"*; *"Giá trị này hết hiệu lực. Nếu nó đang là Final thì Final lùi về giá trị người gõ trước đó, hay về giá trị của sổ gốc nếu không còn."*; ⓒ mã khác / thiếu ⇒ tiêu đề *"Đảo bút toán #N"*; *"Bút toán này hết hiệu lực. Máy chưa biết nó thuộc lớp nào (<mã>) nên không nói trước Final sẽ ra sao — mở nhật ký sau khi đảo để xem."* *(⛔ đoán)*. Chữ trơn *(luật ký hiệu — `⛔` cấm trong văn bản màn)*. Nút, lý do bắt buộc, khoá khi chờ: ⛔ đổi. ⛔ Đổi luật **ai được đảo dòng nào** *(`SM-I03`)*. Mã ⇒ **`WO-023` (g)** |
| F02 · ⭐ vùng **PHÂN BỔ** 🔒 | *(máy suy — `ledger/allocate.py` + `fls_mapping_master`)* | `cfa1 · cfa2 · method · can_phan_bo · khong_tra_duoc` | ⛔ **Không ô gõ**. `#N/A` khi ⛔ không tra được · **`0`** khi `Method` rỗng *(bẫy `VLOOKUP` — hiện **đúng `0`**)* |
| F02 · ⭐ **chip hoá đơn** | `GET /ledger/{id}` *(trường `invoice`)* | chuỗi **N đường dẫn** phân cách dấu phẩy | Vẽ **N chip bấm được**; **22 dòng tên trơ** ⇒ trạng thái riêng *(`GAP-SCR-08`)* |
| F02 · nhật ký trong drawer | `GET /ledger/{id}/journal` | **7 trường `AUD-1`** | Cập nhật mỗi lần sửa *(`US-030`)*. ⭐ *(v4.8, `KQ-007 F-1`)* cột **thành** + **nguồn** đọc theo `value_source`: ⓐ `may_goi_y` có giá trị ⇒ *"gợi ý: X"*; ⓑ `may_goi_y` **rỗng** *(bản đảo khi bỏ ghép)* ⇒ *"rút gợi ý"* — ⛔ in ô trống; ⓒ `sua_tay` ⇒ như nay *(giá trị người — chỉ lằn này là Final)*. Cột nguồn in nhãn người đọc, ⛔ mã: `may_goi_y` ⇒ ~~*"máy gợi ý · ⛔ đổi Final"*~~ ⭐ *"máy gợi ý · không đổi Final"* *(đính chính v4.9 — `HOI-016`: tệp màn nằm trong luật ký hiệu, `⛔` cấm trong văn bản ⇒ chữ trơn)* · `sua_tay` ⇒ *"người sửa"* · mã khác ⇒ in nguyên mã *(⛔ đoán nhãn)*. Vì sao: gợi ý máy **⛔ bao giờ** vào Final *(`QĐ-ITL-149`)* nên dòng *"X → trống"* của nó **⛔ phải** là ô bị xoá — in ô trống làm người đọc từ trên xuống tưởng giá trị người vừa gõ đã mất. Đo 01/10 tối *(sổ thật, chỉ `SELECT`)*: `fls_journal` `may_goi_y` có giá trị **4.424** · rỗng **0** · `sua_tay` có giá trị **2** · rỗng **2** *(cả 4 dòng `sua_tay` là UAT `27728`)* ⇒ ca ⓑ xuất hiện lần đầu ở cú bỏ ghép thật đầu tiên. ⚠ Phần còn lại **chấp nhận**: bản đảo `sua_tay` **cũ** nằm **dưới** giá trị người *(`BA-10` `DT-I14` nhánh 8)* vẫn in ô trống với nguồn *"người sửa"* — tập ấy trên sổ thật = **0** và **đóng** *(từ `WO-003` cú ghép ⛔ còn ghi `sua_tay`)*, chỉ dựng được trên kho thử ⭐⭐ *(v4.9, `HOI-016` ⓑ — `TL-016`)* **`value_source` của một dòng nhật ký = LỚP của CHÍNH dòng ấy** *(ai nói `value_after`: `may_goi_y` máy · `sua_tay` người; bản đảo = lớp của dòng bị đảo)* — ⛔ *"nguồn của giá trị trước khi gõ"*. Định nghĩa ở `BA-05` v0.34 `DD-I15 ⓓe`; khớp `AUD-1` *(`BA-04`: *"nguồn giá trị (máy suy/người nhập/sửa lại)"*)*. Màn **⛔ đổi**: nhãn đọc theo `value_source` là **đúng** khi cửa ghi giữ luật ấy. ⚠ Lệch đã đo: cú `/adjust` của người hôm nay ghi nguồn **trước** khi gõ *(`ghi_tay.py:446`)* ⇒ hàng người gõ in `UNMAPPED`/`nguon`, và ô có `*_thyt` ≠ `NULL` sẽ in *"gợi ý: X · máy gợi ý"* cho giá trị **người**; sổ thật 02/10: dòng nhật ký từ `/adjust` = **0** / 4.428 · ô `*_thyt` ≠ `NULL` = **0** / 8.387 ⇒ sửa ở **cửa ghi** `WO-018`, ⛔ ở màn ⭐⭐ *(v4.12, `KQ-025 F-3`)* **Bản đảo của giá trị NGƯỜI ⛔ được in giống một cú xoá ô.** Đo `KQ-025` *(8099, chuột thật)*: người gõ `HD-NGUOI-C` rồi bấm `Đảo` ⇒ ⑦ in `HD-NGUOI-C → (trống) · người sửa`, trong khi Final **lùi về** giá trị sổ gốc; người gõ ô **rỗng** *(`/adjust value=null` — phép bỏ gán)* in **y hệt**. Hai việc khác nhau, một hình ⇒ hậu kiểm đọc *"người đã xoá ô"*. Câu *"chấp nhận"* của v4.8 dựa trên *"tập đóng"* — sai: nút `Đảo` ở ⑥ có trên **mọi** bút toán ⛔ phải bản đảo *(`man_f02.js` khối ⑥)* ⇒ tập **mở**. ⇒ Cửa `GET /journal` trả thêm **`la_ban_dao`** *(`BA-07` **v3.6**)*; ô **thành** đọc theo bảng: ⓐ `la_ban_dao` ∧ `may_goi_y` ⇒ *"rút gợi ý"* *(như v4.8 — ⛔ đổi)*; ⓑ `la_ban_dao` ∧ `sua_tay` ⇒ chữ mờ *"đảo — giá trị này hết hiệu lực"*; ⓒ ⛔ `la_ban_dao` ∧ `sua_tay` ∧ `value_after` rỗng ⇒ chữ mờ *"xoá ô"*; ⓓ còn lại ⇒ như v4.8 *(giá trị in đậm / *"gợi ý: X"*)*; ⓔ cửa ⛔ trả `la_ban_dao` *(thiếu trường, hay `null`)* ⇒ in như hôm nay *(ô trống)* — ⛔ đoán. Cột **nguồn** ⛔ đổi *(`sua_tay` vẫn *"người sửa"*)*. ⚠ Vì sao ⛔ in *"Final về <lớp dưới>"*: đảo một giá trị người **⛔ nằm trên cùng** *(người gõ A rồi B, đảo A)* thì Final **⛔ đổi** — khung xem `fls_sua_tay` lấy bút toán `sua_tay` **mới nhất chưa bị đảo** *(migration `0025` `:60`–`:70`)*; câu *"giá trị này hết hiệu lực"* **luôn đúng**, câu về Final thì ⛔. Đo sổ thật 02/10 khuya *(chỉ `SELECT`)*: nối `fls_journal` ↔ `fls_adjustment` theo `(itl_id, field, at, actor)` ⇒ **4.428** dòng nhật ký, ⛔ nối được **0**, nhập nhằng *(cùng khoá có cả bản đảo lẫn bút toán thường)* **0**, bản đảo **2** *(cả hai là UAT `27728`, `sua_tay`)*; cú xoá ô *(`sua_tay`, ⛔ bản đảo, rỗng)* **0** ⇒ màn 8088 dòng `27728` đổi **2** hàng *"(trống)"* ⇒ *"đảo — giá trị này hết hiệu lực"*. Mã ⇒ **`WO-023` (f)** |
| **F03** · 4 cổng + độ phủ | `GET /gates` | mỗi cổng: `ma · ten · dat ∈ {true,false,null} · da_do · ly_do` | ⭐⭐ **`dat=null` ⛔ KHÔNG được vẽ như ĐẠT** — nó là *"⛔ không đo được"*, và đó là **luật số 1** của dự án |
| F03 · nút *Xuất báo cáo tuần* | *(gấp trong F03)* | — | `SCR-F05` đã bỏ khỏi sidebar, ⛔ không mất thông tin |
| **F06** · danh mục · nguồn | `GET /catalog` ⚠ | nguồn · TK · ánh xạ + cảnh báo | ⚠ **Cửa này ⛔ CHƯA CÓ** — nằm trong **6 đường đọc còn thiếu** của `BA-07` §2 ⇒ **việc của `P6`**, ⛔ không phải giả định |
| F06 · ⭐ **danh mục phân bổ** | `GET /mapping-master` ⚠ | **73 mã `hd`** · `need_cfa2` · `method_cfa2` | ⚠ Cửa ⛔ chưa có. Dữ liệu **đã vào kho** *(`QĐ-ITL-70`)* |
| *(xuyên suốt)* · chip niềm tin | mọi phản hồi | `flash / đối_soát / đã_ký` | Component **tái dùng từ `A-CCR`** |

⛔⛔ **Bảng này khai ra ĐÚNG HAI cửa còn thiếu** *(`/catalog` · `/mapping-master`)*,
và đó là **việc thật của `P6`** — ⛔ không phải thứ để dev tự bịa một cửa mới.

> ⚰⚰⚰ **BIA — `§8` đã TỰ CÃI `§5` suốt một ngày, và ⛔ không cổng nào thấy.** Bản `v3.2`
> *(18/09 sáng)* thêm `UI-F8` *(«số của MÁY ⛔ không lên màn của NGƯỜI», danh sách đen mở đầu
> bằng **`hạng` · `luỹ kế %`**)* và `v3.4` hoãn cột lý do *(`QĐ-ITL-137`)* — nhưng **⛔ không lần
> nào chạm xuống `§8`**, nơi vẫn đang **yêu cầu dev vẽ đúng hai thứ ấy**. Hai phát biểu ngược
> nhau nằm **trong cùng một tệp**, cách nhau `~300` dòng, và **cả hai đều đúng ngữ pháp**.
>
> ⛔⛔ **Vì sao ⛔ không cổng nào bắt được.** `K1`…`K6` canh **hình dạng** *(phiên bản ↔ changelog,
> số cột bảng, mã quyết định trùng)*; `kiem_so_song` canh **con số**. ⛔ **Không cổng nào canh
> *«hai câu trong một tệp có cùng nói một chuyện ⛔ không»*** — đúng lớp bệnh mà `doc_set_silent_drift`
> đã ghi: *cổng canh **SỐ**, ⛔ không canh **CÂU**, nên số đúng cạnh câu sai vẫn **XANH***.
>
> ⭐ **Và cách sửa ⛔ KHÔNG phải xoá `hang` khỏi bảng.** Cửa `GET /queue` **vẫn phải trả** nó —
> nó là **đầu vào của phép XẾP**. Luật đúng là: **cửa trả ≠ màn in**. `UI-F8` cấm **IN**,
> ⛔ không cấm **TRẢ**. Một lần xoá nhầm ở đây sẽ giết luôn phép xếp theo tiền của `CR#4`.
>
> ⇒ Nợ lại: một phép canh *«mỗi trường trong danh sách đen của `UI-F8` ⛔ không được xuất hiện ở
> cột **Trường chính** của một dòng `§8` mà ⛔ không kèm chữ «⛔ không in»»*. Ghi thành `GAP-CONG-02`.

---

## Changelog
- **v4.24** *(2026-10-06, `fls-ba`, nghiệm thu PO `WO-023` + xếp `KQ-061` `F-1` · `F-2` · nghi ⓖ; trong thẩm quyền spec: hành vi trạng thái màn + chữ màn in + hợp đồng cửa một trường **thêm** — ⛔ token, ⛔ lớp CSS mới, ⛔ tuyến mới, ⛔ đổi sổ, ⛔ đổi luật Final của cửa ghi)*: ⭐⭐ **§3c ⑪ mới** — năm ô sửa được của lưới `F02` *(và hai cột Quét)* in **FINAL** *(bút toán người hiệu lực ?? cột nguồn; gợi ý máy ⛔ bao giờ)*, đọc `<f>_final` của `GET /ledger` *(`BA-07` v3.14)*; `title` *"người sửa — sổ gốc nói: …"*; ảnh chụp cho phép hỏi lại `ⓒ` = Final; `tay` bằng giá trị đang ghi ⇒ ⛔ va chạm *(`F-2` — sổ thật cột nguồn rỗng **8.387 / 8.387** ở cả năm trường ⇒ phiên sửa thật đầu tiên `C1` gặp **100%**)*; câu treo *"người xoá ô thì Final"* ghi lại, ⛔ chặn. ⭐ **`ⓕ3` đính chính phép đếm "2 nơi"** — đếm khẳng định, ⛔ chuỗi: lô lưu `F02` hết giờ in riêng ô đang bay *"CHƯA RÕ đã vào sổ chưa"*, ô sau giữ *"CHƯA vào sổ"*; kiểm kê **18** chỗ `FLS.ghi(` theo nghĩa *(`F-1`)*. ⭐ **`§4.5 ⓦ` ⑨ mới** — kết quả cú `Gán` thuộc lệnh của nó *(nghi ⓖ chưa chứng — tái hiện trước)*. Mã ⇒ **`WO-062`** *(⑪ + `ⓕ3`)* · **`WO-060` `(f)`** *(⑨)*. `WO-023` ✅ `DONG` *(`KQ-061` 17/17)*.
- **v4.23** *(2026-10-05, `fls-ba`, `TL-056` + `TL-058` + xếp phát hiện ngoài phạm vi `WO-023` *(`BG-052` mục 5/6 · `BG-053` mục 3 · `BG-054` mục 1/2 · `BG-057` mục 2/5)*; trong thẩm quyền spec: chữ màn in + hành vi trạng thái màn — ⛔ token, ⛔ lớp CSS mới, ⛔ tuyến, ⛔ đổi sổ)*: ⭐ `ⓕ3` + `ⓦ` ⑤ ⓐ — cú `Gán` hết giờ `FLS-HET-GIO` in *"Chưa rõ gán đã xảy ra chưa — Cửa lỗi: <e.cau>"* *(phương án 1 `HOI-056` — Dev đã làm)*; khuôn chung cho mọi tiền tố *"<Việc> chưa xảy ra — "* *(hôm nay **2** nơi)*. `TL-058`: dòng *"F02 · nhật ký"* v4.12 **⛔ đổi** — bài nghiệm thu đọc oracle v4.8 phải theo v4.12. ⭐ `§4.5 ⓦ` ⑧ mới — ⓐ câu + `lam_gi` `FLS-DQ-FAILED` *(**0** đường từ cổng `ACC-1…4`, **5** lớp cửa ghi)* · ⓑ chế độ chỉ đọc khoá `F01G` `Gán`/`Bỏ gán` + `F02` `Đảo` *(**đính chính** `ⓦ` ② *"như nay"*)* · ⓒ chip *"đã bị đảo bởi #M"* thay nút `Đảo` *(sổ thật **2**)* · ⓓ cổng quét `HT.nuot_phim` phủ cả `.onkeydown =` *(**2** chỗ ⛔ hỏi mà `BG-054` đếm sót)* · ⓔ `ST.dg_mo` theo `itl_id`; nợ `GAP-API-12` *(`BA-07` v3.13)*. Mã ⇒ **`WO-060`**. ⛔ Vòng 2 `WO-023`.
- **v4.22** *(2026-10-05, `fls-ba`, nghiệm thu PO `WO-045` + xếp `KQ-050` `F-1` · `F-3`; trong thẩm quyền spec: hành vi trạng thái màn + chữ màn in — ⛔ token, ⛔ lớp CSS mới, ⛔ tuyến, ⛔ đổi sổ)*: ⭐ `§4.5 ⓦ` ⑥ mới — lựa chọn ứng viên `F01G` gắn theo **`itl_id`**: danh sách bị lượt mới nhất thay ⇒ **giữ** nếu `itl_id` còn, **bỏ** nếu ⛔; `ST.xac_nhan` luôn về `false`; `gan`/`Enter` tìm theo `itl_id`, ⛔ thấy ⇒ 0 `POST` *(`KQ-050 F-3`; mức nâng **`NANG`** vì cửa ghi nhận cặp trong dung sai — ① `KQ-050`)* ⇒ `WO-023` `(i)`. ⭐ `ⓦ` ⑦ mới — `F01` `Xem thêm` khung chờ `Đang tải thêm…` + lỗi ⛔ xoá lưới + `Thử lại` *(`KQ-050 F-1`; trang 2 `VND` **104,33 s** đo lại)*; ngân sách `NFR-I30` *(`BA-08` v1.4)* ⇒ `WO-051`.
- **v4.21** *(2026-10-05, `fls-ba`, `TL-049` — `HOI-049` + `BG-048` mục yếu 2/3/5; trong thẩm quyền spec: chữ màn in + hành vi trạng thái màn — ⛔ token, ⛔ lớp CSS mới, ⛔ tuyến, ⛔ đổi sổ)*: hai **đính chính** — `ⓥ` ⑤ nút `Thử lại` `②b` lớp **`b tiny`**, bỏ vế *"cùng dáng `TT.chay`"* *(nút `TT.loi` lớp `b` — `trang_thai.js:76`)*; `ⓦ` ③ *"⛔ chữ số"* đọc là **ngoài mã `QĐ-ITL-<n>`** *(chuỗi ⓐ mang `QĐ-ITL-122` = 3 chữ số)*. ⭐ `ⓦ` ④ mới — vùng ứng viên `F01G` năm trạng thái: phê chuẩn khung `Đang hỏi sổ…` / `⛔ Cửa lỗi:` của `WO-045`; nút `Thử lại` ⇒ `WO-023` `(h)`. ⭐ `ⓦ` ⑤ mới — lỗi một cú bấm ⛔ rơi ra console: ⓐ `gan` cửa `4xx` ⇒ màn im *(cùng lỗ `F-3` `bo_gan` `WO-008`)* + ⓑ `mo_lenh` từ phím/chuột ⇒ `WO-023` `(h)`; ⓒ `F04` `S.chup` cũ trong lúc ảnh mới tải ⇒ **`GAP-SCR-35`** *(nợ — `fls_chup` người chụp **0** / 158)*. ⛔ Vòng 2 `WO-045`.
- **v4.20** *(2026-10-05, `fls-ba`, nghiệm thu PO `WO-042` + xếp `KQ-046 F-3`; trong thẩm quyền spec: chữ màn in — ⛔ token, ⛔ lớp CSS, ⛔ tuyến, ⛔ đổi sổ)*: `§4.5 ⓦ` ③ mới — `title` nút `Theo LỆNH CHI` *(thanh lằn `F01`, `man_f01.js:766`)* ⛔ còn mang số đo cứng **1.345** *(09/09; sổ thật hôm nay `/ro` `tong` **1.601**, ⛔ cùng định nghĩa)* ⇒ phương án ⓐ bỏ số, chuỗi nguyên văn; ⓑ đọc từ cửa bị loại *(thêm `GET` + một định nghĩa đếm mới cho một tooltip)*. Mã ⇒ **`WO-045` ⑤**.
- **v4.19** *(2026-10-05, `fls-ba`, `TL-043` — `HOI-043` + `BG-044` `(d)` / phát hiện ngoài phạm vi; trong thẩm quyền spec: hành vi trạng thái màn + màn khoá nút nào ở chế độ chỉ đọc — ⛔ token, ⛔ lớp CSS mới, ⛔ tuyến, ⛔ đổi sổ, ⛔ đổi `NFR-I03`)*: `§4.5 ⓥ` đoạn v4.19 — ① lượt bị thay **được dừng ngay** *(gác `goi >= 3` của `kq041` đòi điều spec ⛔ đòi)* · ⑤ nút `Thử lại` cho lỗi / mất kết nối `②b` *(hôm nay **0** — `WO-042` viết "+ `Thử lại`" là lỗi phiếu)*. ⭐ **`§4.5 ⓦ` mới** — luật `ⓥ` áp cho mọi lượt tải **đọc** ghi trạng thái chung *(16 / 21 hàm ⛔ chống — `BG-044` `(d)`; xếp ① `F01G` `mo_lenh`/`tai_toan_so` · ② `F01L` lưới · ③ `F01` · ④ `F04`)* + chế độ chỉ đọc khoá **chỉ** thao tác GHI *(`F01L` `Xem thêm` / `Tìm tiền` bị khoá ⇒ mỗi rổ chỉ thấy 50 dòng: `may` 50 / 120 · `nguoi` 50 / 616 · `khong` 50 / 801)*. Mã ⇒ **`WO-045`**.
- **v4.18** *(2026-10-05, `fls-ba`, nghiệm thu PO `WO-037` + xếp `KQ-041` `F-1`/`F-3`; trong thẩm quyền spec: chữ màn in + hành vi trạng thái màn — ⛔ token, ⛔ lớp CSS, ⛔ khoá cửa mới, ⛔ đổi sổ)*: ⭐ **`§4.5 ⓤ` đoạn v4.18** — bốn chuỗi `F01L` *(ghi chú băng · `note ok` dưới bảng rổ · nhãn lọc `chỉ LỆCH TIỀN` · hàng `may` *"khớp đúng một dòng — người chỉ DUYỆT"*)* ⇒ một câu `LY_DO_LO` nêu đủ bốn lý do cửa ghi giữ *(sổ thật: *"lệch tiền"* đúng **78 / 120**, *"chỉ DUYỆT"* sai **120 / 184**)*; lý do **từng hàng** ⇒ `GAP-SCR-34`. ⭐ **`§4.5 ⓥ` mới** — đổi chip khi đang tải: lượt **mới nhất** thắng *(`KQ-041 F-3` `NANG`: chip `Đã gán` in **2.955** thay **2.219**; bấm lại chip ⇒ **1.472** = 736 × 2)*. Mã ⇒ **`WO-042`**. Đi cùng `BA-07` **v3.11** · `BA-13` **v1.9**.
- **v4.17** *(2026-10-02, `fls-ba`, `TL-038` — `HOI-038` + `BG-039` yếu #1/#4; trong thẩm quyền spec: chữ màn in + nguồn khoá cửa đã khai — ⛔ token, ⛔ lớp CSS, ⛔ đổi sổ)*: `§4.5` câu thứ sáu đọc **`the.vi_sao`** *(`BA-07` **v3.10**; tập **84**, ⛔ 616 — đính chính `WO-037 (g)`)* · ⭐ **`§4.5 ⓤ`** `F01L` băng *Việc của bạn hôm nay* + bảng rổ: rổ `nguoi` nói **hai** câu theo `nguoi_khac_tien_te` của cửa *(câu cũ sai **84 / 616**)*; dòng ghi chú `may − tu_chung` ⛔ còn nói *"lệch tiền"* cho cả nhóm *(đúng **78 / 120**)*; chữ ⛔ ký hiệu cấm. Mã ⇒ **`WO-037` vòng 2**.
- **v4.16** *(2026-10-02, `fls-ba`, nghiệm thu PO `WO-032` + xếp `KQ-036` `F-4`/`F-5 ⓒ`/`F-6`; trong thẩm quyền spec: cách màn **in** câu cửa đã trả + màu từ token có sẵn — ⛔ token mới, ⛔ đổi sổ)*: `§4.5 ⓒ ①` chữ nghĩa chú giải + ô `.tg` ⛔ tông ⇒ **`--muted`** *(đo `--faint` **2,17** · **2,47 : 1** ⇒ `--muted` **4,92** · **5,59**; ngưỡng `BA-08` **`NFR-I29`**)* · `§4.5` ô `Giao dịch đã gán` **câu thứ sáu** — `vi_sao` `ma_khop_khac_tien_te` *(84 lệnh sổ thật — `BA-07` **v3.9** `§4g ⓹`)* · `§5b ⓘ` gạch câu `.cand .amt .lech` *(**0** phần tử từ 23/09)*. Mã ⇒ **`WO-037`**.
- **v4.15** *(2026-10-02, `fls-ba`, `TL-033` — `BG-034` yếu #7; trong thẩm quyền spec: cách màn **nói** nghĩa một ký hiệu đã có, ⛔ đổi bậc, ⛔ token mới)*: ⭐⭐ **`§4.5 ⓒ ①` — chú giải bậc PHẢI có và sinh từ `BAC`**: quyết ① viết *"nghĩa nói một lần ở chú giải ＋ `title`"* từ 21/09 nhưng chú giải **⛔ được dựng** *(grep **0**; bản dựng v10 `:739` có)* ⇒ năm ký hiệu `①②③④≠` chỉ đọc được bằng di chuột. Chip `≠` *(bậc `khac_tien_te`, `WO-032`)* ⇒ **⛔ đủ một mình**, nhưng cách sửa là **chú giải**, ⛔ chữ trên từng dòng. Cho phép **một** lớp `.tlegend` từ bản dựng v10, chỉ token có sẵn. Mã ⇒ **`WO-032` vòng 2**. Đi cùng `BA-07` **v3.8** · `BA-13` **v1.7**.
- **v4.14** *(2026-10-02, `fls-ba`, nghiệm thu PO `WO-022` + xếp `KQ-031` `F-1`…`F-4` và `KQ-029` `F-2`/`F-3` — trong thẩm quyền spec: cách màn **in** và **so** chuỗi cửa đã trả; ⛔ đổi sổ, ⛔ đổi luật dung sai, ⛔ đổi cửa ghi)*: ⭐⭐ **§5b ⓕ thêm — lệch CHỈ có khi CÙNG tiền tệ**: so mã **trước** khi đổi xu; khác mã ⇒ ô `Lệch` in **`khác tiền tệ`**, câu so *"… ⇒ ⛔ khác tiền tệ — cửa ghi sẽ TỪ CHỐI"* `crit`; `—` chỉ cho **thiếu số**. Căn cứ đo `KQ-031` *(8088 sổ thật, rổ `may` 268 lệnh)*: **4** lệnh hộp *Tìm tiền* nói *"lệch 0 ⇒ trong dung sai"* cho cặp VND↔USD/SGD↔USD cùng số mà cửa ghi ném `KhacTienTe`; **165 / 5.360** ứng viên khác tiền tệ in *"lệch"* trừ hai đơn vị. ⭐ **ⓙ mới — bảng có thể trộn tiền tệ ⇒ ô tiền in kèm mã** *(hộp *Tìm tiền* cột `Tiền`)*. ⭐ **ⓘ thêm `.cand-cols`** *(`KQ-029 F-3`: cột `160px` ⇒ ô chữ `137px` ≥ 135 ✔, thiếu `title`)*. ⭐ **Năm trạng thái: rỗng của MÀN phải vẽ được** ở hộp *Tìm tiền* `F01L` + khối `#nap-chon` `F04` *(`KQ-031 F-4` + `KQ-029 F-2` — hai `TypeError` ở `?gia_lap=rong`)*. Đi cùng `BA-07` **v3.7** *(`lech` ở mọi bậc khi cùng tiền tệ · `khoa_to` khai · bậc `khac_tien_te` ở `/so`)* + `BA-13` **v1.6**. `Q-TIEN-1` *(owner)* **⛔ đổi**, vẫn treo. Mã ⇒ **`WO-032`**.
- **v4.13** *(2026-10-02, `fls-ba`, trả `HOI-026` + yếu #1/#4 của `BG-027` — trong thẩm quyền spec: cách màn **in** chuỗi cửa đã trả; ⛔ đổi sổ, ⛔ đổi cửa, ⛔ đổi luật dung sai)*: ⭐⭐ **§5b ⓘ mới — ô tiền rộng theo ngân sách ký tự**: chuỗi ô in dài nhất trên sổ thật **18** ký tự *(đo `node` gọi `TP.tien` thật; lệnh **3.820** dòng · sổ **8.387** giá trị)* × **7,5px** *(phông rộng nhất của `--mono`)* ⇒ `.mcols` `Số tiền` `108 → 136px` **và** `Số tiền GD` `116 → 136px` *(cột GD cắt **383 / 8.387** giá trị sổ ≥ 16 ký tự — `HOI` chưa nêu)*; vượt ngân sách ⇒ `…` + `title`, ⛔ cắt im lặng. ⭐ **ⓒ viết lại** — mã lạ có lẻ in **đủ 2** như ⓑ *(`100,50`, ~~`100,5`~~)*: một luật số lẻ cho mọi mã; tầm sổ hôm nay **0** dòng. ⭐ **ⓕ thêm**: dung sai in = dung sai **đem so** *(sàn xu — `617,28`, ~~`617,29`~~)*; tầm **250 / 4.242** dòng tiền VND. `Q-TIEN-1` *(owner)* **⛔ đổi**, vẫn treo. Mã ⇒ **`WO-022` vòng 2** *(`AC-10`…`AC-15`)*.
- **v4.12** *(2026-10-02 khuya, `fls-ba`, `KQ-025` `F-3` + `F-4` — trong thẩm quyền spec: cách màn **in** dữ liệu cửa đã trả + hai trường **thêm** ở `BA-07` v3.6; ⛔ đổi sổ, ⛔ đổi "con số đến từ đâu")*: ⓐ dòng *"F02 · nhật ký"*: bản đảo của giá trị **người** in *"đảo — giá trị này hết hiệu lực"*, cú **xoá ô** in *"xoá ô"* — hai việc ⛔ còn chung một hình *(`F-3`)*; rút lại câu *"chấp nhận"* nhánh 8 của v4.8 *(tập **mở**, ⛔ đóng)*; đọc theo trường mới `la_ban_dao` của `GET /journal`. ⓑ dòng *"F02 · hoàn tác"*: hộp `Đảo` nói hậu quả theo **lớp** của bút toán *(`may_goi_y` ⇒ *"không đổi Final"* · `sua_tay` ⇒ *"hết hiệu lực; nếu đang là Final thì lùi…"* · mã lạ ⇒ ⛔ đoán)* — `F-4`, tầm **4.424** nút. Đo sổ thật chỉ `SELECT`: cặp nhật ký ↔ bút toán theo `(itl_id, field, at, actor)` **4.428**, nhập nhằng **0**, bản đảo **2**, xoá ô **0**. Mã ⇒ **`WO-023` (f)(g)**. §5b / `UI-F10` *(`WO-022`)* **⛔ đổi**.
- **v4.11** *(2026-10-02 khuya, `fls-ba`, `KQ-021` `F-1` · `F-2` · `F-3` + nợ `409` của v4.10 — trong thẩm quyền spec: cách màn **in** và **trình bày** dữ liệu cửa đã trả + mã lỗi `BA-07`; ⛔ đổi sổ)*: ⭐⭐ **Thêm `UI-F10` + §5b — in tiền theo tiền tệ** *(ISO 4217: VND `0` · USD/SGD/HKD/EUR `2`, cố định; ⛔ làm tròn giá trị sổ khi in — **11** dòng VND có lẻ in đủ, mặc định chờ owner `Q-TIEN-1`; tiền tệ lạ in đủ chữ số thật; `.` nghìn `,` thập phân; tổng / lệch tính trên **số nguyên xu**, khớp ⇔ lệch = 0)*. Căn cứ đo kho thật chỉ `SELECT`: USD **2.413 / 3.980** dòng sổ có phần lẻ · SGD **74/145** · HKD **20/20** · VND **11/4.242**; `node`: lệch `−0,40 USD` in `-0`, Σ `0.10+0.20` vs `0.30` khoá nút Ghép. Mã ⇒ **`WO-022`**. ⭐ Mục ⓔ thêm đoạn **v4.11** `ⓕ1`…`ⓕ5`: hộp đang mở là **modal với bàn phím** *(`KQ-021 F-1`)* · hộp có nút đang chờ cửa ⛔ đóng bằng `Esc`/bấm ngoài + cửa ghi hạn chờ **30 s** mã màn `FLS-HET-GIO` *(⛔ nói "chưa xảy ra")* *(`F-2`)* · nợ `409` trả bằng **ba** mã mới `FLS-DA-GHEP` / `FLS-KHONG-CON-MOI-NOI` / `FLS-CHUA-XONG` *(`BA-07` **v3.5**)* · đính chính tín hiệu ③ⓑ mất khi rời lệnh kể cả quay lại *(yếu #4 — chấp nhận)*. Mã ⇒ **`WO-023`**.
- **v4.10** *(2026-10-02, `fls-ba`, `KQ-019` `F-1`…`F-4` — trong thẩm quyền spec: cách màn trình bày dữ liệu cửa đã trả)*: mục ⓔ thêm đoạn ⭐⭐ **NĂM ca của nút `Bỏ gán` trên màn ghép** — ① lệnh gắn ≥ 2 dòng tiền *(**23** lệnh)* ⇒ hộp báo `Đã hiểu`, 0 lượt ghi; ② chùm *(**25** dòng tiền)* ⇒ hộp hỏi dựng bằng **`HT.mo`** *(`HT.hoi` ⛔ tồn tại — `hop_thoai.js` chỉ xuất `mo`/`dong`/`loi_trong_hop`)*, nút `Thôi` · `Gỡ cả N`, lỗi trong hộp; ③ sau `200` thẻ đổi **tại chỗ** theo `da_bo[]` của thân trả *(bộ ba trạng thái = `khuon_the_lenh` cho lệnh ⛔ gán)* + **một dòng tín hiệu** *"↩ Đã bỏ gán khỏi giao dịch #…"* — ⛔ hộp; ④ đọc lại ứng viên lỗi ⛔ nuốt tín hiệu / hộp `bo_qua`; ⑤ cửa lỗi ⇒ dòng *"Bỏ gán chưa xảy ra — Cửa lỗi: …"*, **0** `Uncaught`. Thêm bảng 5 trạng thái của vùng `Bỏ gán` *(tải: nút khoá — hai cú bấm = 1 lượt ghi)*. Đính chính câu v4.8 *"về lệnh như hôm nay"* ⇒ ca ③ *(⛔ xoá câu cũ)*. Ghi nợ: `409` của `unmatch` mang mã `FLS-CONFLICT-SOURCE` ⇒ câu sai nghĩa *(đổi hợp đồng cửa — phiếu khác)*. Mã ⇒ `WO-008` **vòng 2**.
- **v4.9** *(2026-10-02, `fls-ba`, `TL-016` — trả `HOI-016` của `fls-dev`, trong thẩm quyền spec)*: ⓐ dòng *"F02 · nhật ký"*: khai nghĩa `value_source` = **lớp của chính dòng** *(`BA-05` v0.34 `DD-I15 ⓓe`)*; lệch ở cửa ghi `/adjust` *(nguồn trước khi gõ)* ⇒ `WO-018`, màn ⛔ đổi; ⓑ đính chính nhãn *"máy gợi ý · ⛔ đổi Final"* ⇒ *"máy gợi ý · không đổi Final"* *(luật ký hiệu)*; ⓒ dòng *"Bỏ ghép"*: khối `bo_qua` in **tên ô + giá trị người** *(nhận phương án ⭐ của Dev — `WO-008 AC-4`)*.
- **v4.8** *(2026-10-01 tối, `fls-ba`, `KQ-007` `F-1`…`F-3` — trong thẩm quyền spec: chữ trên màn của dữ liệu cửa đã trả; ⛔ đổi cửa, ⛔ đổi sổ)*: ⓐ `F02` nhật ký — cột *thành*/*nguồn* đọc theo `value_source`; bản đảo gợi ý máy in *"rút gợi ý"*, ⛔ ô trống *(`F-1`)*; ⓑ hộp *"Đã bỏ ghép"* nói theo **ô**, ⛔ lặp tên ô *(`F-2`)*; ⓒ màn ghép **báo sau** `Bỏ gán` khi `bo_qua` ⛔ rỗng — một hộp `Đã hiểu`, ⛔ hỏi trước; hôm nay bật **0** lần *(`fls_sua_tay` 0)* *(`F-3`)*. Mã ⇒ `WO-008` *(ưu tiên thấp, sau `WO-001`)*.
- **v4.7** *(2026-09-23, owner: *"bấm chọn 1 Transaction danh sách nhảy về đầu"* ＋ *"PM đã gán phải hiện Transaction đã map"*)*: ⭐⭐⭐ **Thêm `§4.5 ⓣ`. ✅ `C4` ĐÃ LÀM** — hợp đồng `§4` khai khối *«đang gán»* từ đầu và nó **⛔ chưa bao giờ được làm**: trước `23/09` màn chỉ hiện chip `Đã gán` trên thẻ, tức nói *"việc này xong rồi"* mà ⛔ **không nói xong bằng gì** — kế toán mở một lệnh đã gán ra thì thấy `20` ứng viên **do máy đề xuất** và ⛔ không dấu hiệu nào chỉ ra dòng nào đang được gán. ⛔⛔ Cửa cũng ⛔ không chở đủ: `_gan_gd` lấy `ds[0]` nên với một chùm `7` dòng nó nói về **một** ⇒ thêm `gd_ds` *(tập `id` tăng ~`500`→~`505` mỗi trang, **một** truy vấn vẫn là **một**)*; đo `2.219` lệnh đã gán: **`23` (`1,0%`)** gán hơn một dòng tiền, nhiều nhất **`7`** — một `1,0%` là cớ để ⛔ không bật hộp thoại *(`QĐ-ITL-148 ⓔ`)*, ⛔ **không** phải cớ để **giấu sáu dòng tiền**. ⭐⭐⭐ **Và một phép đo ⛔ không ai hỏi**: `PM00001-1` có `29.211.750`＋`40.513.971` = **`69.725.721`** ≡ đúng số tiền lệnh ⇒ chùm là một phép khớp **chính xác ở TỔNG**, mà `_bac` tính **từng dòng** nên cả hai ra `cung_tien_te` — **bậc yếu nhất**; hai khối `④` cạnh nhau đọc thành *"hai phép gán yếu"* trong khi sự thật là *"một phép gán khớp đúng"*. ⭐ Sửa ⛔ **không ở `_bac`** *(bậc của một dòng so với một dòng vẫn đúng)* mà ở chỗ **nói ra cái từng dòng ⛔ không nói được**: một dòng **TỔNG** ＋ *"khớp"* / *"lệch bao nhiêu"*, và **chỉ vẽ khi có hơn một** *(tổng của một số là chính nó — dòng ấy sẽ vô nghĩa ở `99,0%` số lệnh)*. ⭐⭐ **Lỗi `1` là do chính `v4.6` đẻ ra**: `ve()` dựng lại **toàn bộ** cây ⇒ `scrollTop` mọi hộp về `0`; trước `23/09` nó ⛔ **không tồn tại** vì cả trang cuộn và trình duyệt tự giữ vị trí — chính phép sửa *"chỉ danh sách giao dịch cuộn"* sinh ra nó. *Một phép sửa mở ra một lỗi mới thì phải có một bài thử **đi kèm**, ⛔ không phải một lần nhìn lại.* ⛔⛔ Và giữ chỗ ⛔ **không phải luôn luôn**: đổi sang **lệnh khác** thì danh sách là một danh sách **khác hẳn** ⇒ luật là **giữ chỗ khi vẽ lại cùng một cảnh, về đầu khi đổi cảnh**.
- **v4.6** *(2026-09-23, owner: *"kế toán cần nhìn rõ khu vực này, các thông tin trong cột nguồn"*)*: ⭐⭐⭐ **Thêm `§4.5 ⓢ`.** ⛔⛔ **Lỗi của tôi ở `v4.5`**: tôi cố định bề rộng **để cột thẳng hàng** và ⛔ **không đo thứ phải nằm vừa trong đó** ⇒ `SUPE…` · `ASTR…` · `15.000.000…`. *Thẳng hàng mà ⛔ không đọc được thì chỉ là đổi một lỗi lấy một lỗi.* Đo `200` ứng viên một lệnh ＋ `1.761` ứng viên của `30` lệnh: `nguon` ghép max **`25`** ký tự *(`Airwallex · ••2651 · HGO2`)* ⇒ cần **`~188px`** mà tôi cho `150px`; `số tiền` max **`17`** ký tự *(`1.150.000.000 VND`)* ⇒ cần **`~128px`** mà chỗ thật chỉ còn `87px` sau khi trừ ô `Δ`. ⭐ `bank · tk · le` là **ba mảnh của MỘT câu trả lời** — cắt một mảnh thì hai mảnh kia ⛔ không còn trả lời được gì. ⭐⭐⭐ **Huy hiệu `Δ` bị BỎ** — đo cho ánh xạ **một-một** với bậc: `cung_tien_te` ④ → Δ khác `0` *(`1.664`)* ｜ `ma` ① → Δ vắng *(`51`)* ｜ `tien` ② → Δ `= 0` *(`46`)* ⇒ nó ⛔ **không mang một chút tin nào mới** *(`UI-F9`)*, có mặt ở **`97,1%`** dòng nên ⛔ **không còn là một dấu hiệu** *(một báo động chỉ đáng giá bằng độ HIẾM)*, và ở cửa `/so` là **`0/1.800`** — `34px` giữ chỗ cho thứ ⛔ không bao giờ xuất hiện. Cái giá là `34`–`90px` lấy đúng của hai cột phải đọc, cộng thêm `1550304.54` là **khuôn của máy** lọt lên màn của người *(`UI-F8`)*. ⭐ Con số ấy ⛔ **không bị vứt**: nó lên **câu xác nhận** — `97,1%` tiếng ồn trong danh sách ⇒ `100%` tín hiệu ở một thời điểm. ⛔⛔⛔ **Lỗi tôi để lại ở `v4.5`**: hai khối `@container` vẫn khai lưới trên `.cand` với bản **CŨ** *(còn `auto`)*; cùng độ đặc hiệu mà nằm **sau** trong tệp ⇒ nó **THẮNG** ⇒ mọi màn hẹp hơn `860px` thì `auto` **quay lại** và cột lại lệch — **im lặng**; tệ hơn, nó `display:none` đúng cột **`Nguồn`**. ⭐ Thứ tự hy sinh cột là **quyết định về thông tin**: `Ngày` trước, `Số CT` sau, **`Nguồn` ⛔ KHÔNG BAO GIỜ**.
- **v4.5** *(2026-09-23, vòng góp ý thứ HAI ＋ một lỗi CHẶN lộ ra khi đo)*: ⭐⭐⭐ **Thêm `§4.5 ⓡ`.** ⛔⛔⛔ **Lỗi CHẶN, ⛔ không nằm trong ba câu hỏi của owner**: `/itl-candidates` — **đường chính, ứng viên do MÁY đề xuất** — trả **HÀNG THÔ** từ SQL *(`tien` · `ps_no` · `ps_co` · `source_sheet`)* trong khi màn đọc `amount` · `chieu` · `nguon` ⇒ **hai cột rỗng**, và `khop_dung_tien` so `Number(undefined)` ⇒ **MỌI ứng viên đều thành *"lệch"*** ⇒ nút `Gán` luôn đi đường cảnh báo: **một phép khớp ĐÚNG được trình bày như một phép khớp SAI**. ⛔⛔ Nó sống sót vì bài thử cũ chỉ hỏi `bac` và `itl_id` — **đúng hai khoá mà hàng thô TÌNH CỜ cũng có**; một bài thử hỏi vài khoá giao nhau thì ⛔ không bao giờ thấy **hai khuôn là HAI**. ⭐ Ảnh chụp của owner ⛔ không lộ ra vì màn lúc ấy ở chế độ **Toàn sổ** — cửa KIA, và cửa kia **đã** nắn khuôn ⇒ hai cửa nuôi **một** hàm vẽ mà nói **hai** thứ tiếng. Kèm: `khuon_ung_vien` **⛔ không còn ném** khi `source_sheet` sai khuôn *(trả `nguon:null` ＋ `loi_nguon`, giữ lại `dien_giai`/`amount`)* — cùng lý lẽ đã dùng ở cửa danh sách `22/09`. ⭐⭐⭐ **`3`** *(owner: "các cột Transaction không align thẳng hàng")* ⛔ **không phải lỗi căn lề**: `.cand-cols` kết thúc bằng vệt `auto`, mà **hàng tiêu đề và mỗi dòng là những LƯỚI RIÊNG BIỆT** ⇒ `auto` tính lại theo nội dung **TỪNG DÒNG** — **một bản khai lưới, `14` kết quả khác nhau**; chữa duy nhất là **mọi vệt phải tiên đoán được**. ⭐ Và `.amt` đổi từ `flex` *(căn theo chữ `Có` ⇒ các CON SỐ lệch từng bậc)* sang lưới **ba ô cố định** `Δ｜số｜Nợ/Có`, ô `Δ` **giữ chỗ cả khi ⛔ không có Δ**. ⭐⭐ **`2`** bàn làm việc `sticky` ＋ cuộn riêng, **cùng khuôn** với `.rail` đã có; ⛔⛔ dòng quan trọng nhất là **`min-height:0`** trên `.cands` — một mục flex mặc định ⛔ không co nhỏ hơn nội dung, nên thiếu nó thì `overflow:auto` **⛔ không bao giờ kích hoạt** và ⛔ **không sửa được gì**, mà CSS ⛔ không báo một lỗi nào. ⭐⭐ **`1`** khối *«Xem đủ trường»* thành **LỚP PHỦ** *(owner chọn)*: nó phục vụ **niềm tin vào dữ liệu** `QĐ-ITL-144 ⓐ`, ⛔ không phục vụ việc ghép ⇒ một phép **TRA CỨU** ⛔ không được đòi chỗ với công việc chính — nổi lên trên, đóng lại là mọi thứ về đúng chỗ cũ, ⛔ **không ăn một chút chiều cao nào** của danh sách; ⛔⛔ và `Esc` **bóc từng lớp một** — đóng thẳng cả lệnh thì người vừa mở khối để đối chiếu **mất luôn dòng đang làm**, ⛔ không cách nào quay lại ngoài tìm lại trong `738` dòng.
- **v4.4** *(2026-09-23, owner nhìn màn THẬT lần đầu — `7` góp ý)*: ⭐⭐⭐ **Thêm `§4.5 ⓠ`.** Đây là lần đầu `NFR-I10` **được đo bằng mắt người**, và ⛔ không cổng nào trong `8` cổng đang chạy chạm tới được `7` điều ấy — vì chúng đo *"có đúng ⛔ không"*, ⛔ không đo *"đọc có mệt ⛔ không"*. ⭐⭐ **`1.2` là điều đáng nhất**: khối `SCR-F01` có **`10`** cỡ chữ khác nhau *(`10 · 10,5 · 11 · 11,5 · 12 · 12,5 · 13 · 13,5 · 14 · 15px`)* — ⛔ **không phải một thang, mà là `10` lần chọn riêng lẻ**, và mắt thấy đúng cái đó: ⛔ không tìm ra đâu là bậc trên, đâu là bậc dưới ⇒ mọi thứ tranh nhau nói. ⇒ **`5` bậc** `--fs-nhan`/`--fs-phu`/`--fs-than`/`--fs-manh`/`--fs-to`, `29` khai báo về một thang, `0` bỏ sót. ⭐⭐ Kèm một luật một câu: **`--mono` dành cho thứ cần so cột theo ký tự** *(mã · tiền · ngày · số CT)*; một **CÂU VĂN** trong mono đọc như bản in máy ⇒ `.goi-phim` và `.more dd` về `--sans` — đó là **một nửa** của *"rối mắt"*. ⛔⛔ **`2.4`**: `7` cột ⛔ không một cái tên *(`CT88210` là số chứng từ hay mã gì? `OCBC · ••4001 · SGO2` là cái gì?)* ⇒ kế toán **đoán**; hàng tiêu đề phải dùng **ĐÚNG lưới `.cand-cols` của dòng** — hai bản khai lệch nhau thì **mọi nhãn đọc sang cột bên cạnh**, một lỗi đọc rất thuyết phục vì nó ⛔ không trông như lỗi. ⛔⛔ **`2.3`**: bề rộng đã kéo phải sống trong `ST`, ⛔ **KHÔNG** trong DOM — `ve()` dựng lại toàn bộ cây, đặt thẳng vào phần tử thì kéo xong bấm một cái là **nhảy về cũ** và người ta tưởng **tay kéo hỏng**; kéo có chặn `RAIL_MIN 260`/`RAIL_MAX 720` vì **hai đầu đều là *"màn hỏng"***. ⚠ Cổng token bắt `--rail-w` ⛔ chưa khai, và đúng lúc ấy lộ ra **hai tên cho cùng một bề rộng** ⇒ đã **gộp về một**. ⭐ **`1.1`** bỏ cột `Bậc` *(`12`⇒`11`)*: lúc **quét**, câu hỏi là *"dòng nào chưa xong"*, ⛔ không phải *"dòng này khớp ở mức nào"* — bậc ⛔ **không mất khỏi màn**, nó vẫn là `①②③④` trên từng dòng ứng viên, và một bài thử giữ điều đó. **`1.3`** bỏ dải nhắc `GAP-SPEC-01` khỏi vỏ *(nó nói về **tình trạng dự án**, ⛔ không về việc kế toán đang làm, mà đọc lại ở **mọi** lần mở màn)* — ⚠ `GAP-SPEC-01` **⛔ không bị xoá khỏi sổ**, nó vẫn ở `06_ORCHESTRATOR_DASHBOARD`. **`2.1`** khối *«Xem đủ trường»* xếp **nhiều cột** `auto-fit` đúng bản dựng *(bản `22/09` xếp dọc ⇒ một cú bấm đẩy phần dưới màn xuống gần **một màn hình**)*, mỗi nhóm bọc trong **một khối con riêng** — nếu `h4` và `dl` rời nhau thì `auto-fit` đặt **tên nhóm ở cột này, giá trị ở cột kia**. **`2.2`** mã `PM…` tô `--accent` ở **cả** rail lẫn bảng *(nó là thứ người ta **quét mắt** để tìm dòng)*; ⛔ chỉ **một** mục được tô — tô cả ba thì ⛔ không còn mục nào nổi.
- **v4.3** *(2026-09-22, owner: *"tôi muốn UIUX giống wireframe"*)*: ⭐⭐⭐ **Thêm `§4.5 ⓞ` — HAI VIEW.** Hợp đồng `§4` khai **hai** view *(bảng sổ toàn bề ngang ⇄ rail ＋ bàn làm việc)*; màn `21/09`→`22/09` **⛔ chỉ có một** — luôn là rail, kể cả khi ⛔ chưa chọn gì, nên lúc mở màn phần lớn bề ngang là một **lời nhắc** còn danh sách bị nén vào `380px` ⛔ **không đủ chỗ** cho `Ngày`·`Loại`·`CDT`·`Số CT`. ⭐ Bảng cho người **QUÉT** cả trăm dòng; rail cho người **đang làm một dòng**. Bảng **`12` cột** nguyên văn bản dựng, trong đó cột `→` *(`20px`)* là **cột thật** — nó chia bảng thành bên lệnh chi ＋ bên giao dịch. Rail đổi sang **`3` dòng** *(mất `Ngày`·`Loại`·chip trạng thái·`CDT` là bắt người ta **mở từng dòng ra mới biết dòng nào đáng mở**)*. ⭐⭐ Thêm **`§4.5 ⓟ`** — ba cột cuối cần một phép nối **⛔ chưa có ở cửa**: `ung_vien_itl` và `itl_da_gan` **chỉ là ID**, nên ⇒ `lc.gd_theo_itl()` **một** truy vấn cho cả trang, dùng lại **đúng** `_SQL_ITL_THEO_ID` của bậc `ma`; bậc tính ở **tầng cửa** vì `canon_ref` bằng JS sẽ lệch *(đã đo `17,9%`)*. ⛔⛔⛔ **Và một dòng hỏng ⛔ KHÔNG được làm sập cả trang**: `tach_nguon` ném khi `source_sheet` sai khuôn — đúng ở tầng đọc, nhưng trong một danh sách nó trả `500` cho cả trang ⇒ mất **`738`** dòng vì **một**; ô ấy nay nói *"⛔ không đọc được nguồn"*, dùng `loi_nguon` — một trong **ba đường ra** đã có tên của `DUONG_RA`.
- **v4.2** *(2026-09-22, plan vá bốn lỗi CHẶN — chặng `1`…`5`)*: ⭐⭐⭐ **Thêm `§4.5 ⓜ` — BỐN lỗi CHẶN, và ba cổng đều xanh suốt thời gian ấy.** Kiểm **độc lập** đối chiếu mã ↔ hợp đồng ↔ bản dựng: bàn phím `9/9` viết đủ mà **⛔ không ai đăng ký `keydown`** ⇒ `0/9` phím dùng được; `#ghep-tim` có trong vỏ mà **⛔ không ai nghe `input`** ⇒ cửa `?q=` **⛔ chưa bao giờ nhận một chữ**; `bo_gan` đọc `itl_id_da_gan` — một khoá **⛔ KHÔNG AI SINH RA** ⇒ URL thành `/queue/undefined/chum`. ⭐⭐⭐ **Gốc chung: bài thử với tay VÀO gọi thứ mà sản phẩm phải với tay RA nối** — một khuôn thử cung cấp thứ bản thật phải tự đi lấy thì nó **che mất** chỗ thiếu ấy. ⇒ Cổng mới đo **chiều ngược lại** *(mọi ô nhập phải có người nghe hoặc người đọc giá trị)*; ⚠ nó **⛔ không thay được** một cổng CHẠY, nó là **lưới thưa** bắt chỗ *quên hẳn*. ⭐⭐ Thêm **`§4.5 ⓝ`** — hai lỗi **hình dạng**: **nút lồng nút** *(HTML ⛔ không hợp lệ; DOM giả cho chạy ngon lành ⇒ lớp lỗi một bài chạy **⛔ KHÔNG THỂ** bắt)* và **đụng tên lớp** *(`.mo` đã mang nghĩa "dòng sổ đang mở" ⇒ `querySelectorAll` trả cả hai và bài thử lặng lẽ đo nhầm)*. ✅ **`đủ ↓` ＋ `<mark>` đánh dấu bằng chứng ĐÃ LÀM** — `§4.6` nay đủ: diễn giải ⛔ không còn chỉ đọc được bằng hover, đúng câu `§6.2` của hợp đồng *("⛔ không dùng tooltip làm lối duy nhất")*. ⛔ **`GAP-SCR-26` mở**: chip `Tất cả` vẫn ⛔ chưa có cửa — nó là **hợp** của hai rổ, và gộp ở màn thì `x/y` thành một **số của máy** (`UI-F8`).
- **v4.1** *(2026-09-22, chặng `B3` — mở BE ＋ FE thật)*: ✅ **`GAP-SCR-21` ĐÓNG** — `5` token vào `fls/web/tep/tokens.css`, **tên cũ giữ nguyên** *(đổi tên là sửa toàn hệ `12` tệp mà ⛔ không mua được một pixel)*; khối kiểu của `SCR-F01` vào `hinh.css` *(`531 → 752` dòng)*. ⛔⛔ **Việc hợp nhất lộ một lỗi CÓ SẴN sống câm lặng ba chỗ**: `--accent-soft` được **dùng** ở `hinh.css:247/251/297` và **⛔ CHƯA BAO GIỜ được khai** ⇒ hiệu ứng soi dòng chạy *trong suốt → trong suốt*, và người **tắt chuyển động** *(`prefers-reduced-motion`)* nhận **⛔ không gì cả** thay vì một nền tĩnh. ⭐⭐ Cổng màu chỉ canh **một chiều** *(có hex ngoài token ⛔ không)*; chiều kia *(tên token có thật ⛔ không)* thì **⛔ không ai hỏi**, và CSS **⛔ không bao giờ báo lỗi** ⇒ `GAP-SCR-25` ＋ `test_moi_token_deu_duoc_khai`. ⭐⭐⭐ Thêm **`§4.5 ⓚ`** — **số sê-ri VẪN CÒN**: đo trên **cửa thật**, `Timestamp` ra `46091.42265217593` ở **`3.772/3.772`** dòng; đây là **lần thứ hai** cùng một sai lầm — lần đầu đo bản dựng tưởng đo kho, lần này **sửa lời khai mà ⛔ không kiểm lại đường đi thật của giá trị**. ⭐⭐⭐ Thêm **`§4.5 ⓛ`** — **màn ⛔ KHÔNG tự nạp danh sách**, và **cả hai** cổng `B3` bỏ qua: cổng quét mã ⛔ không hỏi *"danh sách lấy từ đâu"*, cổng chạy mã **tự nhét `ST.dong`** vào trước khi vẽ ⇒ **một khuôn thử cung cấp thứ mà bản thật phải tự đi lấy thì nó CHE MẤT chỗ thiếu ấy**; cổng thứ ba ⛔ không gán `ST.dong` một lần nào, diễn tập phá cho `3` bài đỏ trong khi hai cổng cũ vẫn xanh. ⛔ **`GAP-SCR-24` mở** — *"khung cao bằng màn hình, trang ⛔ không cuộn"* của hợp đồng `§4` **⛔ chưa làm**: vỏ `index.html` là một trang **cuộn** và `4` màn khác đang sống trong nó, nên đổi kiểu cuộn là đổi cả `4` màn trong một cú — một quyết định riêng, ⛔ không phải một dòng CSS.
- **v4.0** *(2026-09-21, `QĐ-ITL-148` — chặng `B0` của plan, phần MÀN)*: ⭐⭐⭐ **Thêm `§4.6` — NĂM sửa bắt buộc trước khi dựng.** Cửa đã khai ở `BA-07 §4h`; mục này là phần **màn phải làm khác** bản dựng. ⓐ ⭐⭐ **Khối *«Xem đủ trường»* phải HIỆN trường vắng** — đo `tho` có **`27` khoá / `41` HÌNH DẠNG**, `Chi nhánh` **11,7%** · `PE (Urgent)` **0,45%**; ⭐ và một phép đo làm việc này **dễ hơn tưởng**: *"có khoá"* ≡ *"có chữ"* ở **cả `27` khoá** ⇒ ⛔ không có ca **chuỗi rỗng**, chỉ cần phân biệt **VẮNG** với **CÓ**. ⓑ **Gỡ trùng `Người nhận` ↔ `Tên tài khoản`** — **cùng một ô**, hai nhãn, hiện **cùng lúc** khi bung ⇒ `UI-F9` tái phát; ⭐ và nó tái phát vì hai chỗ **đọc hai nguồn khác nhau** *(thẻ đọc `BA-06`, khối bung đọc thẳng `tho`)* mà ⛔ không ai đặt hai danh sách cạnh nhau. ⓒ **Bỏ `Người lập`** — quét `27` khoá: ⛔ không khoá nào là người lập／email ⇒ ⛔ **không vẽ ô trống chờ dữ liệu**, vì ở đây cả *"⛔ chưa nạp"* lẫn *"⛔ không có"* đều **sai**: trường ấy **⛔ chưa bao giờ tồn tại**. ⓓ ⭐⭐ **Chip lọc THỨ TƯ** *(`⛔ Không gán được` — `768`)* ⇒ mặc định về **`738`**, cổng `G-a` **ĐẠT**; ⭐ đây là **thiếu một KHÁI NIỆM** *(`INV-I20`: đích cuối ⛔ không phải việc)*, ⛔ không phải thiếu một cú bấm. ⓔ ⭐⭐⭐ **Hộp thoại BỎ GÁN chỉ bật ở `1,1%` ca có chùm** *(`25/2.222`, chùm lớn nhất **`10`**)* và phải **liệt kê TÊN từng dòng lệnh** sắp gỡ. ⛔⛔ **⛔ Không hỏi ở cả hai ca *"cho chắc"*:** một hộp thoại bật **`2.222`** lần để đúng **`25`** lần là cách nhanh nhất **dạy người ta bấm `OK` ⛔ không đọc** — và khi ấy nó ⛔ không còn cản được gì ở đúng `25` lần cần cản. ⭐ `§4.5 ⓙ` thêm liên kết: quyết định *hiện nguyên tên người nhận* là **một ca cụ thể của `NFR-I13 ①`**, ⛔ không phải một luật thứ hai; nợ `GAP-DB-07` *(kho ⛔ chưa mã hoá cột)* **vẫn nguyên**.
- **v3.9** *(2026-09-21, `QĐ-ITL-148` — owner trả lời 4 câu trước khi lập plan)*: ⛔⛔⛔ **ĐÍNH CHÍNH MỘT CÂU TÔI VIẾT HÔM QUA: `§4.5 ⓕ` ghi *"✅ `Timestamp` thôi hiện `45813.49394`"* — SAI.** Bản dựng hiện `18/09/2026 09:14` vì **dữ liệu mẫu do người thiết kế tự gõ**; kho thật vẫn **`3.772/3.772` sê-ri**, **`0`** dòng có dấu ngày ⇒ ⭐⭐ **tôi đo BẢN DỰNG mà tưởng đã đo KHO**. Một bản dựng mang dữ liệu mẫu là **cái bẫy hoàn hảo** cho lớp lỗi ấy: người thiết kế gõ giá trị **đúng như nó nên là**, nên mọi thứ trông đã xong. ⇒ Thêm **`§4.5 ⓗ`** — **bốn** chỗ thiết kế **SAI so với cấu trúc dữ liệu**: ngày sê-ri *(phép đổi **⛔ chưa ai viết**, gốc `1900`／`1904` lệch **4 năm 1 ngày**)* · ⭐⭐ ***"Người nhận" ⛔ không phải một trường*** — `fls_pm_line` có **18 cột**, ⛔ không cột nào là người nhận; nó là `tho['Tên tài khoản']`, **và chính ô ấy cũng ở trong khối bung** ⇒ `UI-F9` **tái phát** · bậc ① của **Toàn sổ** so **chuỗi thô** *(đo lệch **`17,9%`**)* · *"Nguồn"*／*"Số CT"* bóc bằng **cắt chuỗi hiển thị** ⇒ cấu trúc **giả**. ✅ Thêm **`ⓘ`** — chỗ tôi tưởng sai mà hoá **đúng**: chiều `Nợ/Có` có **`3.691`** dòng mang **cả hai** ô nhưng **`0`** dòng cả hai khác `0`; ⚠ luật *"bên nào ≠ 0"* **⛔ chưa viết ở đâu** mà dự án **đã đọc nhầm cột này một lần**. ⭐⭐ Thêm **`ⓙ`** — owner chốt **hiện nguyên tên người nhận**, và quyết định ấy **vẽ ra một ranh giới bộ tài liệu ⛔ chưa từng vẽ**: *hồ sơ nhân sự* *(**cấm nạp** — `QĐ-ITL-107`)* ≠ *danh tính bên nhận tiền* *(**nạp và hiện** — đó là **nội dung của khoản chi**, ⛔ không phải hồ sơ về một con người)*; ⚠ luật che **vẫn đứng** cho hiện vật xuất ra ngoài — **hai luật cho hai nơi**, và lẫn chúng là cách một trong hai bị bỏ.
- **v3.8** *(2026-09-21, `QĐ-ITL-147` — owner xử `GAP-SCR-20`)*: ⭐⭐⭐ **`UI-F7` cho `F01` đi `9 → 11`, và đó là một quyết định ĐƯỢC KÝ, ⛔ không phải một cái trần bị trôi.** Owner chọn **giữ yêu cầu** *(mã lệnh ở đầu thẻ · trạng thái · `CDT` — do chính owner ＋ kế toán đòi ở `QĐ-ITL-144`)* và **nới trần**, thay vì bỏ `2` ô. ⚠⚠ **Và `§5` ghi kèm điều kiện làm nó vẫn là một luật:** trường thứ `12` vẫn phải **bỏ một** hoặc **xin một quyết định nữa** — một trần đổi được **⛔ không cần ai ký** thì nó ⛔ không phải trần, và đó đúng là con đường `339 → 735`. ⭐ Owner cũng **xác nhận giữ *«Xem đủ trường»* ngay trong màn ghép** ⇒ `§4.4 ⓐ` **hẹp lại**: câu *"⛔ không dựng lưới thứ hai"* vẫn cấm nhét `28` cột vào **danh sách làm việc**, nhưng thôi cấm một **khối bung theo yêu cầu** trên thẻ đang mở — vì nhu cầu *yên tâm về data* xảy ra **giữa lúc đang ghép**, nên bắt người **rời màn** là bắt họ trả giá **đúng lúc đắt nhất**. ⇒ `§4.5 ⓔ` đóng `①` và `③`. ⛔⛔ **Còn hai vế MỞ, và cả hai nặng hơn cái vừa đóng:** `6` ô `*_id` nội bộ trong khối bung vẫn vi phạm `UI-F8`; và **khối bung GIẤU IM LẶNG trường vắng** — đo được `tho` có **`41` hình dạng** trên `3.772` dòng *(`Chi nhánh` **11,7%** · `PE (Urgent)` **0,45%**)* ⇒ ở đúng nơi sinh ra để yên tâm về data, *"FLS ⛔ chưa đọc"* và *"dòng này ⛔ không có"* trông **y hệt nhau** *(`GAP-SCR-23`)*. ⭐ Audit đầy đủ ở `Artifacts/Audit-No-Thiet-Ke-Man-Ghep.md` — **`13`** mục nợ, **`4`** hạng chặn.
- **v3.7** *(2026-09-21, `QĐ-ITL-146` — bàn giao thiết kế về)*: ⭐⭐⭐ **Thêm `§4.5` — `SCR-F01` lần đầu có HỢP ĐỒNG HÌNH DẠNG, ⛔ không còn là mô tả bằng lời.** Owner gói bối cảnh đưa sang người thiết kế; về **một hợp đồng ＋ ba bản dựng chạy được**. Đặc tả rút ra: luật bố cục *(trang ⛔ không cuộn · một vùng cuộn duy nhất · bảng đo theo `@container` ⛔ không theo viewport)* · **10 component ＋ trạng thái** · **4 quyết định khó** · bàn phím ＋ **tự nhảy sang lệnh kế tiếp** · chế độ **tra cứu toàn sổ**. ⭐⭐⭐ **Luật đắt nhất: THỨ TỰ HY SINH CỘT `Nguồn → Số CT → ⛔ KHÔNG BAO GIỜ Diễn giải`** — vì diễn giải là **bằng chứng duy nhất** của `49%` cuốn sổ *(`DT-I13 ⓑ`)*, nên cột nào cũng bỏ được **trừ nó**. ⭐⭐ **Và tôi ⛔ KHÔNG chép hợp đồng vào spec — tôi soi nó vào bản dựng.** Bốn câu nặng nhất *(`Enter` khoá khi lệch · hai bước xác nhận · `đủ ↓` đo `scrollHeight` ⛔ không đếm ký tự · ⛔ không mã màu ngoài token)* đều **đúng như khai**. ⛔⛔ **NĂM chỗ lệch thì ⛔ không — và `2` trong `5` là CỔNG NGHIỆM THU của `CR#12` trượt:** ⓐ ⭐⭐⭐ **thẻ lệnh chi có `11` ô, `G-b` đòi `≤ 9`**; cả `3` ô thêm đều do **owner ＋ kế toán đòi** *(`QĐ-ITL-144`)*, nên đây ⛔ **không phải** người thiết kế vượt rào mà là **hai yêu cầu của cùng một phía va nhau**, và ⛔ không ai trong chúng tôi thấy lúc phát biểu; ⓑ ⭐⭐⭐ **danh sách mặc định `1.553`, `G-a` đòi `738`** — bộ lọc `Chưa gán` gộp cả **`768` dòng ⛔ không gán được**, tức gộp **đích cuối** vào **việc hằng ngày** *(`INV-I20`)*; thiếu **một chip thứ tư**, ⛔ không phải thiếu hình dạng; ⓒ ⭐⭐ *«Xem đủ trường»* bung **`17` trường ngay trong `F01`**, trong đó **`6` mã nội bộ** *(`UI-F8` cấm)* — mà `QĐ-ITL-144 ⓐ` đã chốt cách xử là **đường sang `SCR-F02`**, ⛔ không dựng lưới thứ hai ⇒ đổi nó là **đổi một quyết định đã ký**; ⓓ token khai *"kế thừa nguyên văn"* nhưng **đổi tên `6` cái đã có** — thật sự mới chỉ **`4`** ⇒ `GAP-SCR-21`; ⓔ `§10` hợp đồng đo **thời gian thao tác**, mà owner **đã bỏ yêu cầu bấm giờ** ⇒ ⛔ **gốc là lỗi của tôi**: brief ⛔ không chở ràng buộc ấy sang. ⇒ `GAP-SCR-20` gom ⓐⓑⓒ cho **owner**. ⭐⭐ **Và `ⓕ` ghi bốn khuyết tật thiết kế này ĐÓNG ĐƯỢC** — `Timestamp` thôi hiện `45813.49394` · máy ⛔ không chọn sẵn ca nào · `45%` ca lệch tiền nay **trông khác** · diễn giải thành cột **⛔ không bao giờ bị hy sinh**. ⭐ `§7` thêm `ⓒ` *(bảng đổi tên ＋ 4 token mới, `--rail` **đè** `--panel-san`)*. ⭐ `§4.4 ⓑ` thêm **đính chính** — ô `memo 0/8.387` **⛔ không còn đúng** từ `QĐ-ITL-145` *(`fls_dien_giai` **99,7%**)*, chữ cũ **giữ nguyên** làm bản ghi phép đo.
- **v3.6** *(2026-09-18, `QĐ-ITL-144` — owner BA màn hình **cùng kế toán**)*: ⭐⭐⭐ **Thêm `§4.4` — và nó LẬT một quyết định của tôi, bằng một lý do tôi ⛔ KHÔNG nghĩ tới.** `§4.1` khai tử nút *"Hiện đủ 28 cột"* với lập luận *"cột đáng xem thì phải ở trong 9 trường"*; kế toán đòi lại nó, nhưng để **YÊN TÂM VỀ DATA** — *"số trong app có đúng bằng số trong sheet ⛔ không"* — ⛔ **không** phải để ghép. ⇒ ⭐⭐ **Hai NHU CẦU khác nhau mà tôi trộn làm một**: xem-đủ-trường là nhu cầu **THƯA** *(niềm tin)*, ghép là nhu cầu **MỖI DÒNG** *(thao tác)*. ⛔ Cách xử ⛔ **không** phải nhét 28 cột vào danh sách làm việc *(`UI-F7` **đứng nguyên**)* mà là **một đường đi thẳng sang `SCR-F02`** — mặt xem đủ `52` cột **đã có sẵn**. ⛔⛔ Bài học lặp: tôi bỏ một nút vì **đoán sai nó phục vụ việc gì** — cùng gốc với `QĐ-ITL-136` *(dựng `SCR-F07` cho một câu ⛔ không ai hỏi)*, khác chiều. ⭐ Bốn trường phải thêm: **số PM** *(danh sách)* · **ngày ＋ CDT** *(vế lệnh chi)* · **ngày ＋ nội dung** *(vế giao dịch)* — ba cái đầu **có sẵn**, riêng ⛔ **nội dung giao dịch RỖNG `0/8.387`**. ⛔⛔ Và đó ⛔ không phải lỗi màn: tầng `R |` chỉ có **5 cột**, cột diễn giải **chưa bao giờ vào phạm vi** ⇒ việc của **NẠP** *(`GAP-NAP-04`)*; màn phải nói *"chưa được nạp"*, ⛔ **không** để trống như thể *"giao dịch này không có nội dung"*. ⭐ Đo lại `fls_itl`: chỉ **`doc_date` · `doc_no` · `curr` · `ps_no`／`ps_co` · `source_sheet`** có dữ liệu; `memo`·`acct`·`le`·`le_payer`·`pic` ＋ cả 7 khối `Final`／`*_thyt` **rỗng hoàn toàn** ⇒ một giao dịch hôm nay chỉ có **bốn điều**, và `source_sheet` *(mang số TK ＋ ngân hàng ＋ tiền tệ ＋ pháp nhân)* là thứ **cứu panel** — ⛔ ghi rõ đây là **chắp vá**.
- **v3.5** *(2026-09-18 tối muộn, `QĐ-ITL-142` — owner: *"kiểm tra spec các màn hình thiết kế mới, đã có thiết kế chi tiết chưa"*)*: ⛔⛔⛔ **Câu hỏi của owner bắt được một chỗ tệp này TỰ CÃI CHÍNH NÓ.** `§5` khai `UI-F8` *(cấm `hạng`·`luỹ kế %` lên màn)* và `QĐ-ITL-137` hoãn cột lý do — nhưng `§8` **vẫn đang yêu cầu dev vẽ cả ba**, suốt một ngày, **trong cùng một tệp**. ⭐ Sửa `§8`: `9` dòng `F01` viết lại quanh **trục `Tự động`/`Thủ công`** và nối vào **cửa CÓ THẬT** *(`queue/lenh-cho/ro` · `queue/lenh-cho/summary`)*. ⛔⛔ **Và cách sửa ⛔ KHÔNG phải xoá `hang`:** cửa **vẫn phải trả** nó — nó là **đầu vào của phép XẾP** *(`CR#4`)*; luật đúng là **cửa trả ≠ màn in**. ⭐⭐ **Đo bằng chính hàm cửa gọi** *(`dem_theo_ro`, ⛔ không dựng lại SQL)*: `may` **250** · `nguoi` **535** · `khong` **768** · `tu_chung` **47** · `tong` **1.553** ⇒ lằn `Thủ công` = **`535`＋`203`** và ⛔ **KHÔNG cửa nào trả đúng `738`** *(`GAP-SCR-16`)*. ⭐⭐⭐ **`QĐ-ITL-142` — `§4.2b` cộng SAI:** *"`166` `Reject` ＋ `1` tiền tệ `20`"* là **hai tập GIAO NHAU**, ⛔ không rời nhau — đo lại: `Reject` **167** · `curr` là số **1** · **giao `1`** ⇒ hợp **167**. Tổng đúng, phép cộng sai, **cả hai đều ra `167`** nên ⛔ không cổng nào thấy — **đúng lớp lỗi `v3.1`** *(«38＋14=52»)*, lặp lại **lần thứ hai trên cùng một tệp**. ⭐ Và dòng ấy ⛔ không phải *"đơn vị tiền tệ tên 20"*: `PM00576-1` mang `ref_tho='Reject'` · `curr='20'` · `amount=20,00` — nó là **một dòng bị XÊ CỘT**. ⚠ Mở `GAP-CONG-02` *(⛔ không cổng nào canh «hai câu trong một tệp có cùng nói một chuyện ⛔ không»)*.
- **v3.4** *(2026-09-18 tối, `QĐ-ITL-137` — owner: *"bỏ lý do, chưa cần"*)*: `§4.2c` bỏ đường ra *«người gõ lý do»*. ⛔⛔ **Phải tách HAI thứ đều gọi là *lý do*, vì gộp lại là cắt nhầm:** câu `vi_sao` do **MÁY** sinh *(`lenh_cho.VI_SAO`)* ⭐ **GIỮ** — ⛔ không có nó thì `768` dòng ở đích *ghép ⛔ không được* là một hố ⛔ không lời giải thích, và đó đúng là thứ `US-053` sinh ra để chặn. ⭐⭐ **Lối ra nay đo bằng `fls_pm_link.hinh='T'`** — mối nối do **NGƯỜI** tạo, một cột **đã có sẵn trong kho** và ⛔ không đòi ai nhập gì. Đo `18/09`: **`0`** ⇒ ⛔ **chưa một người nào từng ghép một dòng**, và đó là câu trả lời thẳng nhất cho *«màn này có ai dùng ⛔ không»*.
- **v3.3** *(2026-09-18 chiều, `QĐ-ITL-136` — owner sửa TRỤC của bản sáng)*: ⭐⭐⭐ **`v3.2` chia màn theo trục SAI, và nó là lỗi của tôi chứ ⛔ không của máy.** `v3.2` tách `SCR-F01`/`SCR-F07` theo *"việc KHỚP vs việc KIỂM SOÁT"*. Owner bác **cả hai vế**: ⓐ *"FLS ⛔ không cần trả lời câu «tiền đã rời tài khoản — có ai duyệt ⛔ không»"* ⇒ **`SCR-F07` KHAI TỬ**, khai buổi sáng bỏ buổi chiều *(dòng `§2` giữ làm **bia**)*; ⓑ *"Duyệt lô và Ghép từng việc **đều là mapping**, chia theo **người ghép** và **máy ghép**"* ⇒ trục đúng là **`Tự động` / `Thủ công`**. ⭐⭐ **Phép đo ⛔ không sai — cái KHUNG thì sai:** `6.165` dòng tiền ⛔ không có lệnh chi **vẫn là `6.165`**, nó chỉ ⛔ **không phải một việc của FLS**. ⛔⛔ Và nó nhất quán với `QĐ-ITL-56` *(owner 27/08: **⛔ không có quy định nào** nói khoản nào cần lệnh chi)* — ⛔ không luật thì ⛔ không vi phạm để soát, nên **dựng một màn soát trên một luật ⛔ không tồn tại là đúng thứ `INV-I16` cấm**, chỉ khác là lần này người dựng là **tôi**. ⭐ Ba tên cũ *(duyệt lô · ghép từng việc · soát chi không lệnh)* trộn **hai trục** — *ai làm* và *việc gì* — nên trông như **ba việc** trong khi là **MỘT việc, HAI chế độ** + **hai đích cuối** *(`768` ghép ⛔ không được · `167` lỗi nguồn)* ⛔ không phải việc của ai.
- **v3.2** *(2026-09-18, `CR#12` — owner: *"màn ghép overdone, thiết kế tổng thể hơn"*)*: ⭐⭐⭐ **`§4` viết lại: HAI LẰN là HAI VIỆC, ⛔ không phải hai cách xem một việc.** Chữ **`lằn`** xuất hiện **0 lần** trong cả tệp này suốt **9 ngày** kể từ `GAP-SCR-14` *(09/09)* — đặc tả tả **một** lằn, sản phẩm chạy **hai**, và `§4` cũ tả đúng cái lằn ⛔ **không** phải mặc định. ⇒ Tách **`SCR-F07` Soát chi không lệnh** *(việc **KIỂM SOÁT** — **6.165** dòng tiền ⛔ không có lệnh chi nào)* khỏi **`SCR-F01` Ghép lệnh chi** *(việc **KHỚP** — **738** việc thật)*. ⛔⛔ **Và hàng chờ tiền ⛔ KHÔNG CÓ LỐI RA:** `8.387/8.387` dòng `= UNMAPPED`, nút `Xong` mà `QĐ-ITL-71` gọi là *"cách DUY NHẤT một dòng rời hàng chờ"* **⛔ chưa được bấm một lần nào** ⇒ nó ⛔ không phải hàng chờ, nó là một cái kho. ⭐ `§4` cũ giữ **nguyên chữ** làm **bia** *(`§4.3`)* — phần lớn nội dung của nó nay là đặc tả của `F07`. ⭐⭐ Thêm **`UI-F7`** *(ngân sách trường — `F01` trần `9`)*, **`UI-F8`** *(số của máy ⛔ không lên màn của người)*, **`UI-F9`** *(một sự thật một chỗ hiện — đo **8/36** trường là bản sao). Ba nguyên tắc ấy ra đời từ một phép đo về **quy trình**, ⛔ không về gu: `man_f01_lenh.js` đi **339 → 735** dòng qua **7** lần sửa trong **2** ngày và ⛔ **không** lần nào tổng đi xuống.
- **v3.1** *(2026-09-17, audit alignment `C3`)*: ⛔⛔ **`§6` khai SAI CÁCH CỘNG ra `52` — tổng đúng, phép cộng sai, và ⛔ không cổng nào thấy vì cả hai đều ra `52`.** Ô ghi *«38 cột canon + 14 cột hợp đồng»*; đo thẳng ở mã 17/09 thì `BANG_COT` = **`24` cột nền + `28` vị trí canon**. Lưới **⛔ không** lấy cả `38` vị trí canon — nó **cố ý bỏ `9`** *(`A·B·C·D·E·F·G·L·AG`)* vì chúng **đã là cột nền** *(lý do có sẵn trong `cot_so.py`)* — và **⛔ không có** khối *«14 cột hợp đồng»* nào trên lưới. ⭐ Con số **`52` thì ĐÚNG**: `len(cot_so.BANG_COT)` = `52`, nên `GAP-SPEC-03` *(«thật ra 23»)* là **ảnh chụp của 03/09**, trước khi `CANON_LEN_LUOI` lên lưới. Phép `C7` của `docs/ITL/_tools/khop_owner.py` nay canh chỗ này bằng **bằng chứng dương** *(«câu đúng có chưa»)*, ⛔ không bằng phép đếm chuỗi sai.
- **v3.0** *(2026-09-09, rà HIỆN TRẠNG)*: ⛔⛔ **BA câu của tệp này SAI so với màn đang chạy, và ⛔ không cổng nào thấy.** ⓐ `④` ghi *"**8** luật `S1`…`S8`"* — biên bản thật có **9** *(thêm `S10` từ `GAP-KHAI-01`)* và từ `QĐ-ITL-112` nó là biên bản **GỘP** *(540 kết quả → **9 dòng** + cột **Nguồn dính**, hai ô `⛔ không đạt` / `chưa đo` ⛔ không được lẫn)*; ⓑ `①` ghi **68 nguồn** — đo 09/09 là **69** *(60 `Bank`)*; ⓒ `⓶b` còn để nguyên bảng *"3/5 cửa ⛔ KHÔNG TỒN TẠI"* trong khi cả **5** nay đã có *(**29** tuyến)*. ⭐⭐ Và cái đắt nhất: **lằn nạp CẢ LÔ ⛔ không có một chữ nào trong `BA-07`** suốt một ngày sau khi nó chạy thật trên 60 nguồn ⇒ thêm `BA-07 §4f` + cổng `test_ba07_phu_het_tuyen`. ⛔ Bảng `⓶b` **giữ nguyên làm bia** — nó là bằng chứng của hình bệnh *"viết năm trạng thái mà ⛔ không soi xuống bảng tuyến"*.
- **v2.9** *(2026-09-09, `QĐ-ITL-117`)*: ⭐⭐⭐ **Khối `②b` nay có một cú bấm GỘP — và câu *"⛔ không có nút khai tất cả"* của `v2.8` BỊ HẸP.** Owner soi màn **đã chạy** rồi hỏi: *"cách đọc ngày của từng nguồn — bước này hơi buồn cười, trong GGSheet đang đưa về định dạng chung như thế nào?"* ⇒ đo: vùng THÔ ⛔ **không** có khuôn chung *(sê-ri **4.175** · chuỗi **4.190**; khác biệt **theo SHEET**: 16 toàn sê-ri · 34 toàn chuỗi · **0** trộn)*, còn tab `Bank Transactions` **có** chuẩn hoá hết — nhưng nó là **THƯỚC** của `oracle-parity`, ⛔ không phải đầu vào. ⭐⭐⭐ Và trên **4.187** ô chuỗi: phần **trước** dấu `/` lớn nhất **12** *(0 lần >12)*, phần **sau** lớn nhất **31** *(**2.296** lần >12)* ⇒ **34/34** nguồn **tự chứng**, mâu thuẫn **0**. ⇒ **27** cú bấm cho **một** đáp án là *"bấm theo phản xạ"* — đúng cái lo cũ. ⇒ Nút gộp **chỉ nhận nguồn tự chứng** · mang **ba con số** · cửa ⛔ **không nhận `thu_tu`**; nguồn ⛔ không tự chứng bị **nêu tên** và ở **ngoài** lô. ⛔ Cổng cũ `test_man_KHONG_co_nut_KHAI_TAT_CA` ⛔ **không bị xoá** — **viết lại giữ nguyên lo gốc**: lô phải chứa **đúng** nguồn tự chứng, và thân **⛔ không mang `thu_tu`**. Cửa ở `BA-07` §4e *(28 → **29** tuyến)*.
- **v2.8** *(2026-09-08, `QĐ-ITL-113`)*: ⭐⭐⭐ **Thêm trạng thái `②b` — CÁCH ĐỌC NGÀY của từng nguồn.** Đo trên ảnh chụp thật *(8.368 dòng)*: ⛔ **1.894 dòng (22,6%)** có ngày đọc được **hai** cách, trải **29/60 nguồn** ⇒ ⛔ **không phải ca lẻ mà là phần lớn của lô**. ⭐⭐⭐ Và phép đo **LẬT** đúng cái mặc định ai cũng sẽ chọn: **29/29** nguồn ấy là **`mdy`**, ⛔ **0** nguồn `dmy` *(OCBC Singapore · TCB USD — sao kê nước ngoài)* ⇒ một mặc định `dmy` *"vì đây là Việt Nam"* sẽ **hoán ngày↔tháng trên 1.894 dòng**, đúng lớp `QĐ-ITL-17` *(~181 tỷ sai kỳ)*. ⇒ Màn **⛔ không chọn hộ**: máy đề xuất **kèm con số**, người bấm khai; ⛔ **không** nút *"khai tất cả"*. Hai cửa mới ở `BA-07` §4d *(24 → **26** tuyến)*.
- **v2.7** *(2026-09-08, `QĐ-ITL-110`)*: ⭐⭐⭐ **Thêm `§7 ⓶b` — và nó khai một chỗ tôi đã viết 5 trạng thái mà ⛔ KHÔNG soi xuống bảng tuyến.** Soi ngày 08/09 *(20 tuyến thật)*: `F04` cần **5** cửa, **3 cửa ⛔ KHÔNG TỒN TẠI** *(`GET /sources` · một đường đọc vùng CHUẨN · `GET …/khai-cot` — chỉ có `POST`)*; và **hai cửa CÓ vẫn ⛔ không chạy được**, vì cả hai đòi người gọi **đưa sẵn `dong`** — tiền đề *"màn hình đã cầm tệp"* của `QĐ-ITL-105` ⓷ mà `QĐ-ITL-109` **đã lật**. ⇒ Owner chốt **`QĐ-ITL-110`: đọc qua một ẢNH CHỤP trong kho**; **4 tuyến mới** ở `BA-07` §4c *(20 → 24)*. ⛔⛔ **Và hai câu của chính đặc tả này bị khai là CHƯA DỰNG ĐỦ ĐƯỢC** thay vì để dev vẽ quanh: ⓐ ① *"nguồn `InActive`/`Closed` hiện mờ"* — `fls_source` có **7 cột**, ⛔ **không cột nào là trạng thái**; `Account Status` *(`Closed` 10 · `InActive` 5)* chỉ đọc **sống** từ sheet AS-IS *(`GAP-CHUP-02`)*; ⓑ ② lưới *"**6 cột**"* — chỉ **5 cột có dữ liệu**, vì `QĐ-ITL-92`/`107` cấm `Description` và `TRUONG_DOC_DUOC` = 5/6 ⇒ ⛔ **bản vẽ 08/09 vẽ cột ấy CÓ nội dung là SAI**, ⛔ không phải đặc tả sai *(`GAP-SCR-14`)*. ⭐ Cách xử: **giữ cột, ghi *"⛔ không đọc — `QĐ-ITL-92`"*** — bỏ cột thì *cấm đọc* và *quên đọc* trông giống hệt nhau, đúng lý do ① ⛔ không giấu nguồn `InActive`.
- **v2.6** *(2026-09-08, `QĐ-ITL-109`)*: ⛔⛔ **Sửa `§7` — `SCR-F04` ⛔ KHÔNG PHẢI màn TẢI TỆP.** Owner chốt FLS đọc **vùng CHUẨN** của sheet `R |`, ⛔ **không** thay phép chuẩn hoá ⇒ cử chỉ nhập **ở lại Google Sheets** và màn này ⛔ **không có một ô nhập nào** cho dữ liệu giao dịch. Lý do được **ký thành quyết định** chứ ⛔ không để tuỳ nghi: đo sống 60 nguồn bank thì **36** nguồn bóc ngày bằng công thức riêng, **23** nguồn **ĐỔI DẤU** *(`Credit = <cột thô> × (−1)`, kèm hoán vế)* — chở 60 phép biến đổi sang FLS là mở chỗ để **sai DẤU tiền**. ⇒ Sơ đồ `⓵` viết lại; trạng thái `①` *ô kéo-thả* → **chọn phạm vi 68 nguồn** *(mặc định tick tất cả, `InActive` hiện **mờ** chứ ⛔ không giấu)*, `②` *đã chọn tệp · 10 dòng thô* → **FLS đọc, lưới 6 cột vùng CHUẨN CHỈ-ĐỌC**, `③` *khai cột* hạ từ **một bước của mỗi lần nạp** xuống **cấu hình của nguồn, để XEM**. ⭐⭐ **Và `⓹` hoá ra ĐÚNG ngay từ đầu**: nó ghi **4/8** và loại `#2` dán vùng với lý do *"màn này ⛔ không phải chỗ GÕ"*; bản vẽ 08/09 sáng gọi lý do ấy là **sai** và đẩy lên **5/8** — ⛔ **cái sai là bản vẽ**. Giữ **4/8**, ghi lại làm bia. ⇒ `GAP-SCR-12` ĐÓNG.
- **v2.5** *(2026-09-07, `CR#11`)*: ⭐⭐⭐ **Thêm §7 — `SCR-F04` Màn NẠP SAO KÊ ⇒ `GAP-SCR-10` ĐÓNG** *(mở 07/09)*. ⛔⛔ **Xử một VA CHẠM DANH TÍNH ngay ở dòng đầu**: `§2` của chính tệp này đang có **`SCR-F04` = *"Xu hướng nhãn"*, đã bỏ hẳn** *(v1.5)*, trong khi `CR#10` đã đặt **`F04`** cho **màn nhập** — tên ấy nay nằm trong **~10 tệp + mã nguồn**. ⇒ Chốt **`SCR-F04` chỉ còn nghĩa MÀN NẠP**; dòng cũ **giữ làm bia**, ⛔ không xoá. ⭐ **Năm trạng thái**, và ③ **KHAI CỘT** là lý do màn tồn tại — hình dạng lấy từ thứ **kế toán ĐÃ tự làm** *(dòng 1 mỗi sheet `R |`, **68/68** khai đủ trên **9** bố trí)*. ⭐⭐ ④ **BIÊN BẢN** 8 luật, mỗi luật **phải hiện *đã đo bao nhiêu*** — luật nền đã cứu thật một lần. `CHẶN` ⇒ nút `Nhận` **TẮT**; `CỜ` ⇒ **BẬT** *(dòng ấy là **tiền thật**)*. ⭐ Chỉ cần **4/8** hành vi Sheets — ghi rõ để nghiệm thu ⛔ không trượt vì đòi đủ 8 ở **sai màn**. ⛔ **Cố ý ⛔ không có**: nút đẩy sang `A-CCR` *(chặn ở owner, `GAP-PLAN-05`)* · sửa ô lúc nạp · bước duyệt của người thứ hai (`QĐ-ITL-27`).
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
