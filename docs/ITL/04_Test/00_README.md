# 00 — README: Testing Kit (AI-first)

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Dự án:** VOI — Hệ thống Tài chính Nội bộ | **Phiên bản bộ:** v0.1 | **Chủ sở hữu (QA):** COO-CFO + AI

Khác P100 (back-fill test có sẵn), VOI là **forward-fill**: spec BA viết trước → test sinh từ spec → code phải qua test. Hệ này đụng tiền thật và quyền lợi thật — kỷ luật test là hàng rào cuối trước khi mất niềm tin.

Quy ước: `BA-xx`/`DEV-xx` = file kit tương ứng; số trần = nội bộ.

---

## 1. Cấu trúc bộ (3 file)

| File | Vai trò |
|---|---|
| `01_TESTING_FRAMEWORK.md` | Nguyên tắc, pyramid, 5 kỹ thuật, DoD, quy tắc AI |
| `02_TESTCASE_TEMPLATE.md` | Template Given/When/Then + quy ước ID |
| `03_TRACEABILITY_GAP_REPORT.md` | Ma trận truy vết spec→test + GAP/ERROR_REPORT |

## 2. Input bắt buộc từ BA Kit

| Spec | Dùng cho | ID |
|---|---|---|
| `BA-09` State Machines (5 SM) | state transition testing: mọi T pass, mọi F chặn | T-*/F-* |
| `BA-10` Decision Tables (7 DT) | test biên ngưỡng (80%/100% tranche, ngưỡng trọng yếu…) | DT-01..07 |
| `BA-11` Invariants (12 INV) | property-based test + job kiểm đêm | INV-01..12 |
| `BA-03` User Story | AC = test case | US-xxx |
| `BA-04` Role-Permission + SoD | test phân quyền từng ô + 4 SOD | RP/SOD |
| `BA-07` API Contract | mã lỗi ERR-VOI-001..010 trong test negative | ERR |

## 3. Quy trình 4 giai đoạn (reset context giữa giai đoạn)

**A** sinh test case từ spec (phiên AI riêng) → **B** triển khai theo tầng pyramid (mỗi tầng một phiên) → **C** kiểm chứng bộ test: mutation smoke + phiên critic CHỈ nhận spec+TC (không code), đóng vai "kẻ xấu nội bộ tìm cách thao túng số" → **D** vào CI, bug prod = test tái hiện trước fix.

## 4. Quy tắc bất di bất dịch (kế thừa R1–R5 P100 nguyên văn + bổ sung)

- R1 không sửa test cho pass · R2 mỗi tầng một phiên · R3 critic không xem code · R4 bug prod → `TC-BUG-<id>` vĩnh viễn · R5 GAP không AI tự đóng.
- **R6 (VOI):** module tiền/duyệt/chữ ký cấm mock DB ở test nghiệm thu (R-D7); luồng thật trước khi claim done.
- **R7 (VOI):** critic GĐ4 bắt buộc thêm kịch bản thao túng: đẩy chi phí chéo BU, attribution khi app đổi chủ, sửa số sau ký (phải bị hash bắt), rule đổi giữa kỳ.

## Changelog
- v0.1 (2026-07-17): Khởi tạo.
