# HOI-063 — *"Lý do mới nhất"* của view `fls_queue_state` **⛔ xác định** trên **8.256 / 8.387** dòng hàng chờ sổ thật — thêm khoá phụ `evt_id` *(migration)* hay giữ?

| | |
|---|---|
| **Thuộc** | `WO-051` *(phần `(b)` — phát hiện khi đo `AC-4`)* |
| **Hỏi bởi** | `fls-dev` · 2026-10-06 |
| **Loại** | `LECH_DU_LIEU` *(spec nói "lý do mới nhất" một nghĩa; dữ liệu cho tới **20** ứng viên ngang hạng)* |
| **Trạng thái** | `MO` |
| **Chặn** | `KHONG_CHAN` *(`WO-051` giữ **đúng** cách gom của mã khi nhận ⇒ `AC-4` lệch **0 / 8.387**; câu hỏi này là **nợ** cho một phiếu sau)* |

## Bằng chứng
- Chỗ 1 — định nghĩa view: `fls/db/schema.py:708-713` *(`_V_QUEUE_STATE`)* — *"`(ARRAY_AGG(reason ORDER BY at DESC) FILTER (WHERE evt_type = 'reason'))[1] AS reason`"*. Khoá xếp **chỉ** `at`; ⛔ khoá phụ.
- Chỗ 2 — dữ liệu sổ thật *(06/10, `psql` `default_transaction_read_only=on`)*:
  - `fls_queue_event` `evt_type='reason'` = **108.128** sự kiện; actor `dung-lai-so@apero.vn` mang **2** giá trị `at` duy nhất *(lần dựng lại 10/09 — một giao dịch ⇒ `now()` trùng)*.
  - Dòng có lý do: **8.387**; dòng mà `at` lớn nhất bị **≥ 2** sự kiện cùng giữ: **8.387 / 8.387**; trong đó **≥ 2 chuỗi lý do KHÁC nhau** ở hạng đầu: **8.256 / 8.387**; nhiều nhất **20** sự kiện cùng hạng đầu.
- Chỗ 3 — đo được là nó **đổi theo kế hoạch truy vấn**: cùng sổ, cùng giờ, cột `reason` trả về ở **398 / 8.387** hàng khác nhau giữa hai cách gom *(gom **cả bảng** — `GroupAggregate` + `Incremental Sort` của mã cũ ↔ gom **từng `itl_id`** — `LEFT JOIN LATERAL … WHERE v.itl_id = t.itl_id OFFSET 0`)*; ví dụ `itl_id 46903`: cách một ⇒ `"S2 · co tien thi phai co MA · S3 · … · S7 · …"`, cách hai ⇒ `"S3 · moi dong phai co TIEN (No hoac Co)"` — **cả hai** cùng `at = 2026-09-10 11:25:01.230762+00`. Lệnh: `tools/do_trang_hang_cho.py` *(oracle lệch `SGD 1/145 · USD 218/3980 · VND 179/4242 · None 398/8387` trên bản `LATERAL`)*.
- Hệ quả hôm nay: chip `lý do: …` của `F01` *(`man_f01.js` `_the_dong`)* cho một dòng có thể **đổi chữ** khi kế hoạch đổi *(thêm sự kiện, `ANALYZE` tự động, đổi chỉ mục)* — ⛔ ai bấm gì. Và cách nối nhanh nhất cho `doc_hang_cho` *(O(một trang), 0,021 s)* bị **loại** chỉ vì nó chạm đúng chỗ ⛔ xác định này.

## Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | Thêm khoá phụ vào view: `ORDER BY at DESC, evt_id DESC` *(sự kiện chèn **sau** thắng — `evt_id` lấy từ dãy)* ⇒ "mới nhất" xác định; sau đó `doc_hang_cho` đổi sang `LATERAL` O(một trang) | **migration** đổi view *(`schema.py` + hiện vật sinh máy + golden)*; chữ chip `lý do` của **tới 8.256** dòng có thể **đổi một lần** so với hôm nay *(về đúng sự kiện chèn sau cùng)* — `fls-ba` xác nhận đó là nghĩa "mới nhất" mong muốn; một phiếu `WO` mới | ⭐ |
| 2 | Giữ nguyên view; `doc_hang_cho` giữ cách gom cả bảng *(bản `WO-051`, ~60 ms/trang trên 110.349 sự kiện, tuyến tính)* | lý do vẫn **⛔ xác định** theo kế hoạch *(chưa ai thấy vì kế hoạch hôm nay ổn định)*; trang chạm `2 s` ở cỡ ~3,6 triệu sự kiện | |
| 3 | Dọn dữ liệu: gộp ~13 sự kiện `reason` cùng `at` của lần dựng lại 10/09 thành **một** | ⛔ được — `fls_queue_event` **chỉ-thêm** *(`INV-I08`)*; mọi "dọn" là ghi kho thật | |

---

# TL-063 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | … |
| **Ai quyết** | … |
| **Spec đã sửa** | … |
