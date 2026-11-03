# 04 — DEVELOPMENT LOOP: vòng lặp phát triển

**Version:** v0.2 | **Chủ sở hữu:** COO-CFO | **Bối cảnh:** team 1–2 người + AI agent

Khác chương trình FIN ERP: ở đó vòng trong chạy **theo story**. Ở ITL vòng trong chạy **theo adapter/nguồn** — vì đơn vị rủi ro của dự án này là *một nguồn dữ liệu*, không phải *một tính năng*. Mỗi milestone `IM2–IM5` = thêm đúng một nguồn rồi đối chiếu tới khi khớp (`P-ITL-02`).

---

## 1. Vòng ngoài — theo milestone

```
Đầu IM: chốt phần nguồn sẽ thêm + mắt xích Gsheet sẽ cắt + số dòng nhập tay sẽ khai tử
   ↓
Vòng trong × n (theo adapter / theo vùng của ITL Ledge)
   ↓
Đối soát oracle phần nguồn đó → "khớp hoặc giải thích được"
   ↓
Chạy song song sổ Gsheet (strangler-fig) — KHÔNG cắt sổ cũ
   ↓
Value review hàng tháng: "tháng này thao tác tay nào biến mất?"
   2 tháng không giảm được thao tác tay nào → DỪNG BUILD, xem lại hướng
   ↓
Gate review cuối IM (`03` §2) → người vận hành ký nghiệm thu
```

## 2. Vòng trong — theo adapter (6 bước)

| # | Bước | Ràng buộc |
|---|---|---|
| 1 | **Đọc cấu trúc nguồn thật** | Đọc sheet thật trong `NGUỒN-FILES`, không suy từ trí nhớ. Google Sheets đọc **live qua Sheets API** — không đánh giá bằng `.xlsx` offline (bản export phá huỷ ngày, chỉ 2,7% ô ngày còn nguyên kiểu) |
| 2 | **Spec map cột nguồn → `ITL-CANON`** | Tên trường lấy **nguyên văn** (R-A2). Nguồn thiếu trường → để trống **có kiểm soát**, không bịa (`P-ITL-05`) |
| 3 | **Build adapter** | Một phiên AI = một adapter (hoặc một vùng). Xuất đúng 36 cột + `source_id` + provenance |
| 4 | **DQ test** | Row-count vs sheet nguồn · referential integrity · parse ngày/số · **fail-loud khi schema nguồn đổi**. Luật cứng: **0 dòng rơi im lặng** |
| 5 | **Đối soát oracle** | So với `ITL RAW`/`ITL ADJUSTED` cũ theo **dòng + tổng**. Lệch phải phân loại: lệch thật vs cash-vs-accrual hợp lệ |
| 6 | **Review + cập nhật trạng thái** | Phiên AI reviewer **riêng** (không phải phiên build), rồi con người duyệt merge → cập nhật `06` + changelog |

## 3. Luật riêng cho pipeline tài chính

- **Không bước nào là "nhấn nút thủ công".** Mỗi nguồn là một node DAG **idempotent, retriable**. Chạy lại 2 lần cho cùng kết quả, không nhân đôi dữ liệu.
- **Golden-run vs oracle trước mỗi merge.** Adapter/engine đổi gì cũng chạy lại kỳ chuẩn; lệch dòng nào phải giải trình được.
- **Test tương thích hợp đồng chạy ở mọi milestone**, không chỉ `IM0` (rủi ro #1).
- ⭐ **Bốn cổng chạy ở CUỐI MỖI PHA và trong mọi PR** — `DEV-03` §1. Drift ERD↔thiết kế là bệnh đã tái phát ở dự án này, nên cổng là **test**, không phải một buổi rà bằng mắt:

| Cổng | Nội dung |
|---|---|
| **G-ERD-1** | ERD **sinh từ** `pg_schema.py` == ERD đã commit ⇒ đổi schema mà quên sinh lại = **build đỏ** |
| **G-ERD-2** | **hai chiều**: mọi bảng/view trong code phải có trên ERD của BA, **và** mọi entity trên ERD phải tồn tại trong code |
| **G-ERD-3** | mọi bảng phải với tới được `fls_itl` qua FK, nếu không **phải** khai `ERD_ISLANDS` **kèm lý do bằng chữ** |
| **`INV-I07`** | khoá 14 trường `ITL-CONTRACT` v1.0, `le` = cột `P` |

  ⛔ **ERD là hiện vật SINH RA, không phải hình vẽ tay.** Sửa ERD bằng tay là bị G-ERD-1 bắt. Bước cuối mỗi pha *(đồng bộ ERD của BA)* không phải việc tuỳ tâm — G-ERD-2 **đỏ cho tới khi làm xong**, nên tài liệu không thể già đi trong im lặng.
- **Đo bảo toàn tiền bằng net theo output-sheet**, không cộng dồn cả bảng (rủi ro #2).
- **Điều chỉnh là journal append-only.** Không có đường code nào được ghi đè `RAW` (`P-ITL-04`).
- **Bug production: viết test tái hiện TRƯỚC khi fix** (`TC-BUG-<id>`).
- **Sau sửa code BE: tự restart + verify.** BE chạy persistent không `--reload` ⇒ không restart thì kết quả vẫn là bytecode cũ.

## 4. Vòng lặp cho vùng ADJUSTMENT (đặc thù `IM6`)

Vùng này không phải "một nguồn" mà là **~6.843 dòng thao tác người**. Vòng lặp khác:

1. **Phân loại** các khối nhập tay (297 · 179 · 1210 · 22 · 22 · 1624 · 3489) theo *lý do điều chỉnh*, không theo thứ tự sheet.
2. Khối nào **suy được thành luật** → chuyển thành bút toán tự sinh có luật.
3. Khối nào **không suy được thành luật** → giữ là nhập tay nhưng qua UI *(`BA-06`)*, không gõ trực tiếp vào sổ. ⛔ **Sửa 2026-08-26: KHÔNG có maker-checker** — `QĐ-ITL-16` bỏ bước duyệt riêng, `QĐ-ITL-27` khai tử người thứ hai *(vận hành thật 2–3 kế toán)*. Người gõ **là** người chốt; bù lại **bắt buộc nhật ký `AUD-1` 7 trường** — đó là chỗ kiểm soát duy nhất còn lại.
4. Đối soát: kết quả tự sinh + nhập tay còn lại **= tổng vùng ADJUSTMENT cũ**.

> Đây là chỗ code hoá cứu được nhiều nhất, và cũng là chỗ dễ mất số nhất — vì không có "nguồn" để đối chiếu ngoài chính vùng cũ.

## Changelog
- **v0.2 (2026-08-26): thêm 4 cổng chạy được vào §3** *(G-ERD-1/2/3 + `INV-I07`)* — chạy cuối mỗi pha và mọi PR, vì drift ERD↔thiết kế đã tái phát *(`DEV-03` §1: ERD của BA và DDL của Dev chỉ khớp 3/10 entity)*. Chốt **ERD là hiện vật sinh ra từ code**, sửa tay là build đỏ. ⛔ **Sửa §4 mục 3**: bỏ *"maker-checker"* — `QĐ-ITL-16` bỏ bước duyệt, `QĐ-ITL-27` khai tử người thứ hai; kiểm soát chuyển sang nhật ký `AUD-1`.
- v0.1 (2026-08-18): Khởi tạo — vòng trong đổi từ "theo story" (chương trình) sang **theo adapter**; thêm §4 vòng lặp riêng cho vùng ADJUSTMENT; 7 luật pipeline tài chính.
