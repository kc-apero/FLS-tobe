# Rà soát độc lập: schema ITL Ledge ⇄ wireframe SCR-F02

**Version:** v1.0 · **Ngày:** 2026-08-24 · **Người rà:** agent độc lập *(general-purpose)* · **Chủ sở hữu:** COO-CFO

**Luật:** SSOT hợp đồng = **code** (`itl_ledge_reader.py::_COLS`), không phải tài liệu. Mỗi khẳng định trỏ `file:dòng`.

**Nguồn:** `_COLS` + `NEEDED_COLS` *(FPA-T4)* · `04_DB_IMPLEMENTATION` · `05_DATA_DICTIONARY_ERD` · `FLS-Wireframe.html` · `_GUIDE_04_ITL-Xuong-song.md` *(công thức 4 tầng)*.

---

## §1 · Xác nhận phần ĐÚNG

- **14/14 trường engine đọc đều có trong wireframe** — không thiếu trường nào.
- **`le` = cột `P` (15)**, không phải `BL` — `04_DB` và `05_ERD` khớp code.
- **5 khối Final sửa được đúng ranh giới** — khối 6 (`ID Payee`) + 7 (`Hoá đơn`) chỉ đọc, ngoài hợp đồng.

## §2 · Ba lỗi schema — ĐÃ SỬA trong wireframe

| # | Lỗi | Mức | Sửa |
|--:|---|---|---|
| 1 | Đối soát pháp nhân so `le` với **ID Payee (Y = bên NHẬN)** thay vì **Pháp nhân thanh toán (L = bên TRẢ)** — lẫn payer↔payee | nghiêm trọng | ✅ thêm trường `payer` (cột L), so `LE (P) vs Pháp nhân thanh toán (L)`; `US-032` nay đúng bên |
| 2 | `Reference number` là trường bịa — không trong canonical 36, không phải cột `fls_itl`, chỉ là thành phần `content_key` | trung bình | ✅ bỏ khỏi panel |
| 3 | Tên `pt/ss/se` lệch tên hợp đồng | thấp | ✅ đổi hiển thị `pay_type/svc_start/svc_end` |

## §3 · Cơ chế 4 tầng — và đính chính của OWNER

Agent đọc công thức `_GUIDE_04`: mỗi trường có `Classifying → Manual input → MID → Final`.

⚠ **Agent kết luận (từ công thức sheet `H1000`):** `Final` là **công thức**, ô người gõ là tầng giữa.

⭐ **OWNER đính chính 2026-08-24:** *"`Final` KHÔNG phải công thức — `Final` là nơi kế toán nhập tay chỉnh sửa thông tin giao dịch."*

⇒ **Hoà giải:**

| | Sổ AS-IS *(công thức đo được)* | Ý định TO-BE *(owner chốt)* |
|---|---|---|
| `Classifying` | máy tra tự động | **máy gợi ý — chỉ đọc** |
| `MID` | áp mặc định cứng | ⛔ **BỎ** — chính là "máy tự bịa" *(`INV-I16`)* |
| `Final` | công thức trộn | ⭐ **kế toán nhập/sửa — chính thức, engine đọc** |

Mô hình wireframe *(máy gợi ý chỉ-đọc → ô Final sửa được)* **đúng ý định TO-BE**. Bỏ tầng `MID`; chỗ không suy được để **trống** *(không mặc định)*, kế toán gõ vào Final.

## §4 · Một imprecision của chính agent — cross-check bắt được

Agent nói *"ô người gõ = cột MID (U)"* dựa trên sheet **`H1000`**. Nhưng phép đo trực tiếp trên **`ITL Ledge`** *(sheet engine đọc)*: `T` = giá trị người gõ, `U` = công thức — **hai sheet hoán vai T/U**. Không đổi kết luận lớn, nhưng: *tầng người gõ nằm cột nào* phải đọc lại đúng `ITL Ledge` khi build, không tin sheet khác. ⇒ `GAP-DB-04`.

## §5 · Việc mở

| ID | Việc |
|---|---|
| `GAP-DB-04` | Đọc lại đúng công thức `ITL Ledge` T/U/V trước khi build — không ngoại suy từ `H1000` |
| `GAP-SCR-06` | `04_DB` §5.1 `*_thyt`: dưới mô hình "Final = kế toán sửa", cột `*_thyt` là để **parity với sổ cũ** *(bug-compatible)*, còn `Final` đi tới là honest. Làm rõ hai vai |

## Changelog
- **v1.0** (2026-08-24): Rà soát độc lập. Xác nhận 14/14 trường + le=P + 5 khối đúng. Sửa 3 lỗi schema *(payer/payee · reference bịa · tên trường)*. Owner đính chính **Final = ô kế toán sửa**, bỏ tầng MID. Mở `GAP-DB-04`, `GAP-SCR-06`.
