# 03 — USER STORY: FLS

**Version:** v1.5 · **Ngày:** 2026-09-18 · **Chủ sở hữu:** BA/PO
**Thay thế:** v0.1 *(bản copy chương trình)* — đã khai tử.

**Nguồn gốc:** [`Artifacts/UC-US-Ke-toan-PM-den-ITL.md`](Artifacts/UC-US-Ke-toan-PM-den-ITL.md) v0.3 — **22 UC · 45 US**, là SSOT của story. File này **không lặp lại 45 US**; nó **nhóm chúng theo phạm vi build của FLS** và gắn mỗi nhóm vào `ITL-CONTRACT` / schema / API để làm cơ sở code.

**AC dạng Given/When/Then — AC chính là test case.** Chi tiết AC lấy ở `Artifacts/UC-US` §5.

---

## §1 · Ba vai người + một vai máy *(rút từ `UC-US` §2)*

| Vai | Người thật | Làm gì | Trên đâu (TO-BE) |
|---|---|---|---|
| `AC-A` Kế toán tiền | ThomHT · AnhMC · ThuongCT | nạp sao kê · nhập thu chi quỹ · nhập số dư | Sheets *(nguồn)* + app *(xem)* |
| `AC-B` Kế toán phân loại | LAN · THƯƠNG | gõ 5 trường ADJUSTMENT · xử hàng chờ | ⭐ **app** |
| `AC-C` Giữ danh mục | *(kiêm nhiệm)* | tài khoản · quỹ · `Mapping Master` · `Index` | Sheets |
| `MÁY` | hệ thống | ghép · phân loại · cấp `itl_id` · xếp hàng chờ · nhật ký | FLS |

⛔ **Không có vai duyệt / hậu kiểm / leo thang** — vận hành thật 2–3 người *(`QĐ-ITL-27`)*. Kiểm soát đến từ **máy**, không từ người thứ hai.

---

## §2 · Bản đồ epic — theo phạm vi build FLS

| Epic | Story gốc | Ra bằng gì | Cổng |
|---|---|---|---|
| **E1 · Adapter → canonical** | `001–005` · `013–021` | adapter A–F → `ITL-CANON` 36 cột | `ACC-1…4` |
| **E2 · Lớp sổ** | `023` · `026` · `036` · `037` | `fls_itl`: `itl_id` bền · 5 câu `if` · 3 trạng thái · máy vá mã | G1 + parity |
| **E3 · Hàng chờ + nhật ký** | `028` · `030` · `039` · `040` · `045` | app: một hàng chờ theo tiền · cột lý do · nhật ký 7 trường | E2E |
| **E4 · Cổng đối soát** | `006–011` · `029` · `038` | DIF (đọc A-CCR) · cổng `Final` · độ phủ | `INV-I02` |
| **E5 · Một trang tuần** | `034` · `043` | CFO·COO chỉ đọc, ba việc | — |
| **E6 · Máy quét + xu hướng** | `036` · `041` · `042` | quét chỉ-đọc · xu hướng nhãn | — |

---

## §3 · Story ưu tiên build — 5 trường ADJUSTMENT là trục

★ Hợp đồng chỉ còn **5 trường** người gõ vào đường P&L *(`hd` · `pay_type` · `cdt1` · `svc_start` · `svc_end` — `QĐ-ITL-42`)*. Đây là trục của app.

⭐ **`QĐ-owner-0824`:** mặt kế toán **sửa** rộng hơn 5 — gồm **7 khối Final** *(thêm ⑥ Mã đối tác · ⑦ Hoá đơn)* **+ phân bổ** *(CFA1/CFA2/Method, máy gợi ý → override được)*. Chỉ 5 khối vào P&L *(có parity)*; khối ⑥⑦ + phân bổ sửa được nhưng **ngoài P&L**. Panel `SCR-F02` tách **Nhóm A** *(5 khối engine)* / **Nhóm B** *(ngoài P&L)* — `06_SCREEN` v1.4.

| US | Là… tôi muốn… | AC chính | Cột schema | Cổng |
|---|---|---|---|---|
| `US-KT-026` ★★ | `AC-B`, dòng chưa biết chủ ở `UNMAPPED` **tường minh**, không bị gán mặc định | thiếu nguồn ⇒ `work_status='UNMAPPED'`, `*_thyt IS NULL`, có trong hàng chờ | `hd_thyt`… `work_status` | `INV-I16` |
| `US-KT-025` ★ | `AC-B`, khi gõ khác nguồn thì hệ **KÊU**, để công tôi không bị bỏ | nguồn có giá trị + tôi gõ khác ⇒ hiện *"nguồn đang có X"* + 2 nút; ghi đè vào nhật ký | `fls_journal` | đo *"số lần nguồn ≠ người gõ"* |
| `US-KT-039` ★★ | `AC-B`, mở **một hàng chờ, xếp theo tiền**, một cột để gõ: **lý do** | chỉ phần chưa biết · xếp tiền giảm · in tuổi việc · không nút xoá trắng | — | `US-045` |
| `US-KT-030` | `AC-B`, mọi lần gõ/sửa vào **nhật ký 7 trường** | `AUD-1`: `itl_id·trường·trước→sau·người·lúc·nguồn·lý do` | `fls_journal` | insert-only |
| `US-KT-023` | `AC-B`, **`itl_id` không bao giờ đổi** | chèn dòng ngày cũ ⇒ id cũ giữ nguyên | `itl_id` | `INV-I04a` |
| `US-KT-045` ★★ | COO-CFO, đo **có ai đọc hàng chờ không** | 4 tuần không ai gõ cột lý do = cổng chết | `fls_journal` | `GAP-ITL-35` |

⚠⚠⚠ **`US-039` THU HẸP · `US-045` HOÃN — `18/09` tối, `QĐ-ITL-137`** *(owner: *"bỏ lý do, chưa cần"*)*. ⭐ *"chưa cần"* ⇒ **HOÃN**, ⛔ không khai tử: cửa `POST /queue/{itl_id}/reason` **còn sống trong mã**, chỉ ⛔ **không lên màn**. ⛔⛔ **Tách bạch HAI thứ đều gọi là *lý do*** — ⓐ **NGƯỜI gõ** *(`fls_queue_event`)* ⇒ **hoãn**; ⓑ **MÁY sinh** *(`lenh_cho.VI_SAO`)* ⇒ ⭐ **GIỮ**, vì ⛔ không có nó thì `768` dòng *ghép ⛔ không được* là một hố ⛔ không lời giải. ⇒ `US-039` giữ vế *hàng chờ xếp theo tiền*, **bỏ** vế *một cột để gõ lý do*. ⚠ **`US-045` mất dụng cụ đo** — nó là **thước của chính owner**, nên ⛔ không lặng lẽ để nó trỏ vào một cột ⛔ không còn. ⭐⭐ **Thay bằng một thước ⛔ không cần ai gõ gì:** `fls_pm_link.hinh='T'` = mối nối **do NGƯỜI tạo**; đo `18/09` = **`0`** *(`A` 2.145 · `B` 65 · `C` 52)*.

⚠⚠ **`US-047` CHỈA LẠI — `18/09`, `QĐ-ITL-136`.** Cả ba viết cho **hàng chờ TIỀN**, mà owner vừa đưa hàng chờ ấy **ra khỏi phạm vi** *(«FLS ⛔ không cần trả lời câu hỏi này»)*. ⭐ Cả ba **⛔ KHÔNG khai tử** — chúng chỉa sang **hàng chờ MAPPING**, nơi một dòng rời đi bằng **ba** đường *(ghép được · đích ⛔ ghép-không-được kèm lý do · đích lỗi nguồn)*. ⭐⭐ Riêng **`US-045` là thước của chính owner**, nên việc nó **mất đối tượng** là chuyện phải nói ra chứ ⛔ không lặng lẽ để nó trỏ vào một màn ⛔ không còn tồn tại.


---

## §4 · Story trục dữ liệu — E1/E4

| US | Story rút gọn | Nối vào |
|---|---|---|
| `US-KT-037` ★ | máy đọc mã lệnh **trong diễn giải** để vá dòng chưa ghép | `GAP-ITL-57` — **70 hay 158 dòng?** chờ chốt luật |
| ~~`US-KT-036`~~ ⛔ **KHAI TỬ 27/08** | ~~máy dán **6 nhãn "không cần lệnh chi"**~~ | `QĐ-ITL-56`: **không có quy định nào** nói khoản nào cần lệnh chi ⇒ máy dán nhãn đó là **máy tự đặt ra quy định** *(`INV-I16` cấm)*. Thay bằng **xếp hàng chờ theo TIỀN** — 310 dòng *(4%)* phủ **90% tiền**. Xem `QĐ-ITL-58` *(`CR#3` đã đóng: **bỏ hẳn**)* |
| `US-KT-038` | đếm **tài khoản không kiểm được** mỗi ngày | adapter C |
| `US-KT-008/009` | thấy `DIF ≠ 0` theo ngày·pháp nhân·tài khoản, **cảnh báo không chặn** | đọc A-CCR dòng 226 |
| `US-KT-029` ★ | cổng đối soát so cột **`Final`**, không so `Classifying` | `INV-I15` đã đóng — `le`=`P` |
| `US-KT-042` | máy quét đọc sổ sống **chỉ đọc, không ghi** | `QĐ-ITL-34` |

---

## §5 · 38 story NEW = phạm vi build gốc

⚠⚠ **CẬP NHẬT 2026-08-28: 45 → 47 story** *(`UC-US` v0.4 §5.7)*. Hai thao tác **đã xây và đã chạy trên kho thật** mà **⛔ không có story nào**:

| US | Là… tôi muốn… | Vì sao nó thiếu |
|---|---|---|
| `US-KT-046` ⭐⭐ | `AC-B`, **gỡ được mối nối** ghép sai để ghép lại | `US-KT-039` nói *"mở một bảng việc"* mà ⛔ **không nói gì về việc RỜI bảng** — nên đường lùi ⛔ không có chỗ trong backlog |
| `US-KT-047` ⭐⭐ | `AC-B`, **bấm "xong"** để một dòng rời hàng chờ | Owner chốt **người bấm**, ⛔ không phải máy tự nhả: máy tự nhả thì kế toán **mất chỗ đánh dấu việc đang làm dở** *(`QĐ-ITL-71`)*; và ⛔ **không đòi lý do** *(`QĐ-ITL-72`)* |

★ Đây là **code đi trước đặc tả** — cùng lớp với `GAP-DOC-03`, và nó lộ ra vì owner hỏi *"US/UC tương ứng với hai màn là gì"*.


### ⭐⭐⭐ CẬP NHẬT 2026-09-09: `47 → 51` story — và lần này thiếu **CẢ MỘT LẰN**

⛔⛔ **Hình bệnh ở trên LẶP LẠI, to hơn.** Lần trước *(28/08)* thiếu **hai thao tác**; lần này thiếu **toàn bộ lằn NẠP** — màn `SCR-F04` + 9 cửa + 4 bảng kho, dựng từ `07/09` đến `09/09`, **đã chạy thật trên 60 nguồn · 8.368 dòng**, mà `BA-03` ⛔ **không có một chữ**.

⭐ Và nó lộ ra **theo đúng cách cũ**: owner yêu cầu *"cập nhật tài liệu BA phản ánh hiện trạng"*. ⇒ Cùng lớp `GAP-DOC-03`, và ⛔ **không** phải *"quên"* — nó là hệ quả cấu trúc: `BA-06`/`BA-07` được cập nhật **mỗi đợt** vì mã chạm vào chúng, còn `BA-03` thì ⛔ **không có phép đo nào** buộc nó theo.

| US | Là… tôi muốn… | Vì sao nó thiếu · căn cứ |
|---|---|---|
| `US-KT-048` ⭐⭐⭐ | `AC-B`, **nạp sao kê CẢ LÔ** *(60 nguồn, một `run_id`)* và thấy **biên bản 9 luật GỘP** trước khi nhận, để ⛔ không phải nạp 60 lượt rồi tự cộng | `US-KT-023`/`026` nói về **lớp sổ**, ⛔ không nói ai **đưa dòng vào** sổ. Lằn này sinh ra vì đo được: đường duy nhất vào kho là **một lệnh dòng lệnh của Dev** *(`CR#11`)*. Căn cứ `QĐ-ITL-111`/`112`, `BA-07 §4f` |
| `US-KT-049` ⭐⭐⭐ | `AC-B`, **ấn định cách đọc ngày** của một nguồn *(`ngày/tháng` hay `tháng/ngày`)* sau khi đọc **bằng chứng có con số** máy đo được | ⛔ **1.894/8.368 dòng (22,6%)** có ngày đọc được **hai** cách. ⛔ Máy ⛔ không được quyết: đây là **kỳ kế toán của một bút toán**. Căn cứ `QĐ-ITL-113`, `BA-07 §4d` |
| `US-KT-050` ⭐⭐ | `AC-B`, khai cách đọc ngày **một cú cho cả lô** với những nguồn mà **chính dữ liệu của nó** đã loại trừ được một cách đọc | Đo: **34/34** nguồn chuỗi **tự chứng**, `chac_dmy` = **0** ⇒ **27** cú bấm cho **một** đáp án là *"bấm theo phản xạ"*. ⛔ Nguồn ⛔ không tự chứng **vẫn phải** bấm riêng. Căn cứ `QĐ-ITL-117`, `BA-07 §4e` |
| `US-KT-051` ⭐ | `AC-B`, **xem bản khai ánh xạ cột** của một nguồn — cả **dãy `version`**, ai khai, hiệu lực từ khi nào | Câu *"vì sao lô tháng trước đọc cột khác"* chỉ trả lời được nếu **thấy được bản cũ** — đó là cả lý do bảng khai là **chỉ-THÊM**. Căn cứ `QĐ-ITL-110`, `BA-06 §7 ⓶ ③` |
| `US-KT-052` ⭐⭐ | `AC-B`, hỏi **từ phía LỆNH CHI** *("lệnh nào chưa ra tiền")*, ⛔ không từ phía tiền | `QĐ-ITL-122`. Đo cùng kho: phủ `90%` tiền cần **`799`** dòng nếu hỏi phía TIỀN, **`69`** nếu hỏi phía LỆNH — chênh **`11,6` lần** |
| `US-KT-053` ⭐⭐⭐ | `AC-B`, biết **AI trả lời được** một dòng trước khi ngồi tra — và rổ *⛔ không ai trả lời được* phải mang **câu vì sao** | ⛔⛔ **`768/1.553` = `49,5%`** danh sách ⛔ không phải việc của kế toán; ⛔ không có câu vì sao thì họ tìm **mãi mãi** |
| `US-KT-054` ⭐⭐ | `AC-B`, **duyệt cả lô** những dòng máy đã tự chứng — và ⛔ **KHÔNG** được gộp dòng *lệch tiền* vào cùng nút | `47` tự chứng vs `203` lệch tiền. Gộp = để **máy quyết thay người** *(`INV-I16`)* |
| `US-KT-055` ⭐ | `AC-B`, thấy **các dòng khác cùng phiếu** và đủ trường của phiếu khi cần | `526` phiếu mang `2`–`36` số chứng từ khác nhau; **`1.088/1.553` = `70,1%`** dòng chờ nằm trong phiếu nhiều dòng ⇒ nhìn một dòng lẻ mà quyết là nhìn một mảnh |
| `US-KT-056` ⭐⭐ | `AC-B`, **gỡ mối nối** ngay trên lằn đang làm — ⛔ không phải đổi lằn mới gỡ được | ⛔ Đo `18/09`: cửa `POST /queue/{itl_id}/unmatch` **có**, nút có ở lằn TIỀN, **⛔ không có** ở lằn LỆNH CHI — tức lằn **mặc định**. Mở rộng `US-KT-046` |

⛔⛔ **`052`–`056` được KHAI MUỘN — `CR#12`, `2026-09-18`.** Năm story này đã được `BA-13` **trích làm căn cứ** cho từng nút, từng cột của màn `F01` từ `14/09`, trong khi `BA-03` chỉ có tới **`051`**. ⇒ Suốt bốn ngày, **đặc tả thuyết minh viện dẫn năm điều luật ⛔ chưa ai ban hành**. ⭐ Chúng ⛔ **không** phải story mới nghĩ ra hôm nay — chúng là **đặc tả hồi tố** của thứ đã xây và đang chạy; cái mới là **chỗ ở hợp lệ** cho chúng. ⚠ Cùng lớp lỗi với `GAP-DOC-*`: *một chỗ nói thật, một chỗ ⛔ không nói gì, và ⛔ không cái gì báo gì.*

⛔ **Cả 4 story này ĐÃ XÂY XONG và đang chạy** — chúng vào đây làm **đặc tả hồi tố**, ⛔ không phải backlog. ⚠ Việc ấy ⛔ **không** vô hại: một story viết **sau** khi mã chạy thì nó có nguy cơ chỉ **kể lại mã**, ⛔ không **đối chất** với mã. ⇒ Chỗ để đối chất là cột *"Vì sao nó thiếu · căn cứ"*: mỗi dòng phải trỏ về một **phép đo** hay một **quyết định**, ⛔ không trỏ về một hàm.


`UC-US` §5 đếm **38/45 story phải xây mới**. Đây là backlog gốc của FLS — không phải danh sách mong muốn. 7 story còn lại đã có hình thức nào đó đang chạy *(nạp sao kê, danh mục…)* nằm ở phía Sheets, FLS **đọc**.

⚠ **Hai story chờ QUYẾT ĐỊNH trước khi build** *(không phải chờ code)*:

| US | Chờ | Ai |
|---|---|---|
| ~~`US-KT-036`~~ | ~~luật 6 nhãn~~ ✅ **đã trả lời 27/08: KHÔNG CÓ quy định** ⇒ story khai tử, mở `CR#3` | — |
| `US-KT-037` | 70 hay 158 dòng *(`GAP-ITL-57`)* — **19,57 tỷ** phụ thuộc | kế toán |

---

## Changelog
- **v1.5** *(2026-09-18 tối, `QĐ-ITL-137` — owner: *"bỏ lý do, chưa cần"*)*: **`US-039` thu hẹp** *(bỏ vế «một cột để gõ lý do»)*, **`US-045` HOÃN**. ⛔⛔ **Chỗ suýt cắt nhầm:** trong hệ có **HAI** thứ đều gọi là *lý do* — ⓐ **NGƯỜI gõ** *(`fls_queue_event(evt_type='reason')`)* và ⓑ **MÁY sinh** *(`lenh_cho.VI_SAO` — câu «có số chứng từ nhưng ⛔ không dòng tiền nào mang số ấy»)*. Owner bỏ ⓐ; ⭐ ⓑ **PHẢI GIỮ**, vì ⛔ không có nó thì đích *ghép ⛔ không được* là một hố **`768`** dòng ⛔ không lời giải thích. ⚠⚠ **`US-045` là thước của chính owner và nó vừa mất dụng cụ đo** — ⭐ thay bằng `fls_pm_link.hinh='T'` *(mối nối do **NGƯỜI** tạo)*, đo thẳng từ kho, ⛔ không phụ thuộc một cột nhập liệu nào; hôm nay **`0`**.
- **v1.4** *(2026-09-18 chiều, `QĐ-ITL-136`)*: **`US-039`/`045`/`047` chỉa lại sang hàng chờ MAPPING.** Cả ba viết cho **hàng chờ TIỀN**, thứ owner vừa đưa ra khỏi phạm vi. ⭐ ⛔ Không story nào khai tử — nhưng ⭐⭐ **`US-045` là thước của chính owner** *(«4 tuần ⛔ không ai gõ cột lý do = cổng chết»)*, nên việc nó **mất đối tượng** phải được nói ra, ⛔ không để nó lặng lẽ trỏ vào một màn ⛔ không còn tồn tại — đó đúng là lớp lỗi cả bộ này dựng ra để chặn.
- **v1.3** *(2026-09-18, `CR#12`)*: ⭐⭐ **Khai `US-KT-052`…`056` — năm story đã được `BA-13` TRÍCH LÀM CĂN CỨ từ `14/09` nhưng ⛔ CHƯA BAO GIỜ ĐƯỢC KHAI ở đây.** Đo: `BA-13` dẫn tới `056`, tệp này dừng ở `051` ⇒ bốn ngày liền một đặc tả thuyết minh viện dẫn **năm điều luật ⛔ chưa ai ban hành**, và ⛔ không cổng nào hỏi câu *"mã story được trích có tồn tại ⛔ không"*. ⭐ Cả năm là **đặc tả hồi tố** của thứ đang chạy — cái được thêm là **chỗ ở hợp lệ**, ⛔ không phải việc mới. ⭐⭐ Nặng nhất là `US-KT-053` *(«biết AI trả lời được trước khi ngồi tra»)*: nó chống lưng cho phép chia rổ, mà phép chia ấy quyết định **`49,5%`** danh sách ⛔ không phải việc của kế toán.
- **v1.2** *(2026-09-09, rà HIỆN TRẠNG)*: ⛔⛔⛔ **`47 → 51` story — và lần này thiếu CẢ MỘT LẰN.** Màn `SCR-F04` + lằn NẠP *(9 cửa, 4 bảng kho, `07/09`→`09/09`, **đã chạy thật 60 nguồn · 8.368 dòng**)* ⛔ **không có một story nào**. ⭐ Hình bệnh y hệt `v1.1` *(28/08: thiếu 2 thao tác)*, chỉ to hơn — và nó lộ ra **theo đúng cách cũ**: owner hỏi. ⛔ Nguyên nhân cấu trúc: `BA-06`/`BA-07` được cập nhật mỗi đợt vì **mã chạm vào chúng**, còn `BA-03` ⛔ **không có phép đo nào** buộc nó theo. Thêm `US-KT-048` *(nạp cả lô + biên bản gộp)* · `049` *(ấn định cách đọc ngày theo bằng chứng)* · `050` *(khai cả lô cho nguồn tự chứng)* · `051` *(xem cả dãy `version` bản khai)*. ⚠ Cả 4 là **đặc tả hồi tố** — và một story viết sau mã có nguy cơ chỉ **kể lại mã**; chỗ đối chất là cột *căn cứ*, phải trỏ về một **phép đo** hay một **quyết định**, ⛔ không về một hàm.
- **v1.1** (2026-08-28): **45 → 47 story** — thêm `US-KT-046` *(bỏ mối nối)* + `US-KT-047` *(người bấm xong)*, hai thao tác **đã xây và đã chạy trên kho thật** mà ⛔ không có story nào *(chi tiết ở `UC-US` v0.4 §5.7)*. ⚠ Và hai UC được đánh dấu lại: `UC-KT-19` *(hậu kiểm)* vai `???` ⇒ **`MÁY`**; `UC-KT-21` *(xoá giao dịch)* ⇒ **TO-BE ⛔ không có thao tác xoá**, câu hỏi đúng là *"đảo một bút toán"*.
- **v1.0** (2026-08-24): Viết mới cho FLS. **Không lặp 45 US** — trỏ SSOT `Artifacts/UC-US` v0.3, nhóm thành **6 epic theo phạm vi build** và gắn vào schema/cổng. Trục app = **5 trường ADJUSTMENT** *(`QĐ-ITL-42`)*. Nêu 2 story chờ quyết định trước khi build.
