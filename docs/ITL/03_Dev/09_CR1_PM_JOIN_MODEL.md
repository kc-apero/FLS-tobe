# 09 — CR#1: MÔ HÌNH GHÉP PM (thay luật OP-03 bất khả)

**Version:** v1.0 · **Ngày:** 2026-08-25 · **Chủ sở hữu:** Tech Lead + Kế toán trưởng
**Loại:** CR loại 2 *(đổi mô hình ghép, không đổi hợp đồng engine)* · **Đầu vào cho:** `QĐ-ITL-44` bước ④ *(cải thiện ghép PM)*
**Căn cứ — ba nguồn khớp nhau:** `fps/db/schema.py` *(SSOT code)* · `pm_reader.py` *(sheet PM)* · `_GUIDE_09` OP-02/03 *(thao tác người)*

---

## §1 · Vấn đề — `OP-03` "1 PMLine ↔ 1 Reference" là bất khả về cấu trúc

Guide `_GUIDE_09` OP-03 áp luật *"`ID PMLine ↔ Reference number` = 1–1"*. Đây là **luật người tự áp bằng tay** *(nguồn: một ô Note "Cần 1 key = 1 mã")*, **không phải bảo đảm schema**. Sự thật đo được:

| Khoá | Bảng (code) | Grain | Bằng chứng |
|---|---|---|---|
| `reference_number` | ⭐ **`fps_pm_slip`** | **SLIP** | `schema.py:653`; `STRING`, **không UNIQUE** — 75 mã dùng lại |
| `pm_id` | `fps_pm_slip` PK | SLIP | `schema.py:614` |
| `line_id` | ⭐ **`fps_pm_line`** PK | **LINE (1–1)** | `schema.py:665` — có id riêng, **không mang reference** |
| `pi_line_id` | `fps_pm_line` | LINE | `schema.py:667` — truy lên hoá đơn PI |
| `amount` | `fps_pm_line` | LINE | `schema.py:669` |

⇒ `reference_number` sống ở **slip**; một slip có **N line** *(nối bằng `pm_id`)*. Khi phiếu nhiều dòng, chúng **dùng chung một reference** ⇒ `VLOOKUP(reference)` ở `Transaction Mapping L1` chỉ lấy **dòng đầu**, **bỏ im lặng** phần còn lại *(đo được: 289 dòng dư bị bỏ)*. Phép ghép hiện tại **giả vờ bank↔line nhưng thực chất là bank↔slip**.

---

## §2 · `line_id` có thay được reference không? — KHÔNG

`fps_pm_line.line_id` **là** khoá 1–1 mức line thật. Nhưng **không dùng để nối bank↔line được**, vì: **phía bank chỉ có `reference_number`, mà reference nằm ở slip**. Không có `line_id` phía bank ⇒ không khoá chung nào bắc cầu bank→line trực tiếp.

---

## §3 · Quyết định — nối hai chặng + chia tiền

```
Bank txn (reference_number)
  ──(reference = fps_pm_slip.reference_number)──►  fps_pm_slip
        [1 ref → 1 slip; 75 mã trùng ⇒ tách thêm bằng ngày + số tiền]
  ──(pm_id)────────────────────────────────────►  fps_pm_line  (N dòng)
  ──phân bổ tiền bank theo fps_pm_line.amount───►  gán về từng line
        [khớp CHÍNH XÁC nếu Σ amount(line) = tiền bank]
```

| Bước | Luật |
|---|---|
| **Nối phiếu** | `bank.reference_number → fps_pm_slip.reference_number` — chấp nhận grain **slip**, KHÔNG giả vờ line |
| **Xuống dòng** | `fps_pm_slip.pm_id → fps_pm_line.pm_id` |
| **Chia tiền** | phân bổ tiền bank theo `fps_pm_line.amount`; nếu `Σ amount(line) = tiền bank` ⇒ khớp tuyệt đối; lệch ⇒ đánh dấu `UNMAPPED`, đưa vào hàng chờ *(không chia bừa)* |
| **Định danh dòng mang vào ITL** | ⭐ **`fps_pm_line.line_id`** — bền, thay hẳn `PMLine` gõ tay trong sheet *(vốn `#N/A` đầy)* |
| **Mã reference trùng (75)** | tách bằng bộ ba `reference + ngày + số tiền`; đây đúng là lý do `content_key` phải có `seq_trong_nhóm_trùng` *(`INV-I04b`)* |
| **66% không ghép** | dòng không tra được reference ⇒ `work_status='UNMAPPED'`, đếm được *(`INV-I16`)* — KHÔNG gán mặc định |

⛔ **Bỏ luật `OP-03`** *(1 PMLine ↔ 1 ref)* khỏi TO-BE — nó tả một điều schema không cho phép. Thay bằng **§3 slip-join + amount-split**.

---

## §4 · Hai hệ quả sang quyết định khác

| Gap | Đóng/hẹp lại |
|---|---|
| **`GAP-ERD-10`** *(le_payer từ đâu)* | ⭐ `fps_pm_slip` có sẵn **`payer_id` · `payer_name` · `payer_account_*`** *(schema.py:641-647)* ⇒ nghiêng **`le_payer ← fps_pm_slip.payer_id`** *(nguồn code, không phải cột Sheet dễ vỡ)*. Cột L (Mapping L1) chỉ dùng đối chiếu |
| **`GAP-ITL-58`** *(kiểu svc date)* | `fps_pm_slip.service_start/end_date` là **`DATE`** *(schema.py:630-631)* ⇒ nguồn gốc FPS đã là date; `yyyymm` chỉ là **cách ITL Ledge trình bày**. Spike thu hẹp: chỉ cần xác nhận kiểu ô ITL Ledge, **không** phải nghi ngờ nguồn |

---

## §5 · Ảnh hưởng thi công

★ **`QĐ-ITL-48`: mapping là việc của FLS, không đẩy lên FPS.** Hai lối ghép:
- **Auto** *(pipeline, §3)*: máy ghép theo reference → slip → line → chia tiền. Phần lớn dòng đi đường này.
- **Tay** *(dòng rớt)*: màn **`F01` nút Ghép** — drawer gợi ý `fps_pm_slip` ứng viên *(xếp theo reference/tiền/ngày/payee)*, kế toán **chọn phiếu**, máy xuống line + chia tiền, `Σ line = tiền bank` mới cho ghép *(lệch ⇒ giữ UNMAPPED)*. Đây là bản số hoá `OP-02` **trong FLS**, không phải deep-link sang FPS. Wireframe đã dựng.

- **Adapter ghép PM** *(bước ④)*: viết theo §3 — đọc `fps_pm_slip` + `fps_pm_line` *(read-only, `QĐ-ITL-45`)*, không dùng `PM_Unpivot` sheet.
- **`fls_itl`**: `content_key` giữ `reference` + `seq`; cân nhắc mang `pm_line_id` *(= `fps_pm_line.line_id`)* vào `canon` như khoá lineage bền thay `PMLine` gõ tay.
- **`le_payer`**: adapter lấy `fps_pm_slip.payer_id` *(sửa nguồn trong `04_DB` khi build ④)*.
- **Cổng đối soát**: thêm phép kiểm *"Σ amount(line) = tiền bank"* cho mỗi phiếu ghép — lệch ⇒ hàng chờ.

## §6 · Việc mở

| ID | Việc |
|---|---|
| `GAP-CR1-01` | Ngưỡng chấp nhận khi `Σ amount(line) ≠ tiền bank` *(chênh lẻ do phí/tỷ giá)* — chốt với kế toán |
| `GAP-CR1-02` | `reference + ngày + số tiền` có đủ tách 75 mã trùng không, hay còn va — đo trên dữ liệu thật |

## Changelog
- **v1.0** (2026-08-25): Viết mới từ rà 3 nguồn *(FPS schema · pm_reader · guide OP-03)*. Kết luận: reference ở **slip**, `line_id` không nối bank được ⇒ **slip-join + amount-split + `line_id` identity**, bỏ `OP-03`. Hẹp `GAP-ERD-10` *(le_payer ← `payer_id`)* + `GAP-ITL-58` *(nguồn FPS là DATE)*.
