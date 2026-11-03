# 03 — USER STORY: FLS

**Version:** v1.1 · **Ngày:** 2026-08-28 · **Chủ sở hữu:** BA/PO
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

`UC-US` §5 đếm **38/45 story phải xây mới**. Đây là backlog gốc của FLS — không phải danh sách mong muốn. 7 story còn lại đã có hình thức nào đó đang chạy *(nạp sao kê, danh mục…)* nằm ở phía Sheets, FLS **đọc**.

⚠ **Hai story chờ QUYẾT ĐỊNH trước khi build** *(không phải chờ code)*:

| US | Chờ | Ai |
|---|---|---|
| ~~`US-KT-036`~~ | ~~luật 6 nhãn~~ ✅ **đã trả lời 27/08: KHÔNG CÓ quy định** ⇒ story khai tử, mở `CR#3` | — |
| `US-KT-037` | 70 hay 158 dòng *(`GAP-ITL-57`)* — **19,57 tỷ** phụ thuộc | kế toán |

---

## Changelog
- **v1.1** (2026-08-28): **45 → 47 story** — thêm `US-KT-046` *(bỏ mối nối)* + `US-KT-047` *(người bấm xong)*, hai thao tác **đã xây và đã chạy trên kho thật** mà ⛔ không có story nào *(chi tiết ở `UC-US` v0.4 §5.7)*. ⚠ Và hai UC được đánh dấu lại: `UC-KT-19` *(hậu kiểm)* vai `???` ⇒ **`MÁY`**; `UC-KT-21` *(xoá giao dịch)* ⇒ **TO-BE ⛔ không có thao tác xoá**, câu hỏi đúng là *"đảo một bút toán"*.
- **v1.0** (2026-08-24): Viết mới cho FLS. **Không lặp 45 US** — trỏ SSOT `Artifacts/UC-US` v0.3, nhóm thành **6 epic theo phạm vi build** và gắn vào schema/cổng. Trục app = **5 trường ADJUSTMENT** *(`QĐ-ITL-42`)*. Nêu 2 story chờ quyết định trước khi build.
