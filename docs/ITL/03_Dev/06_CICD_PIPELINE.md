# 06 — CI/CD PIPELINE

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Version:** v0.1 | **Chủ sở hữu:** Tech Lead | **Độ chín:** thiết kế — dựng thật ở T0.x trước go-live GĐ0

---

## 1. Pipeline CI (mọi push/PR)

| Bước | Nội dung | Cổng |
|---|---|---|
| 1. Lint + format | ruff/black (BE), eslint/prettier (FE) | fail = chặn |
| 2. Type check | mypy/pyright · tsc | fail = chặn |
| 3. Import-linter | ranh giới module `01` §4 (cấm import vòng, cấm bypass m0) | fail = chặn |
| 4. Unit + property | pytest; property test từ INV (Hypothesis — harness P100 sẵn) | fail = chặn |
| 5. Integration | PG container (services trong CI); migration apply→down→apply | fail = chặn |
| 6. Golden-run | engine thay đổi → chạy kỳ chuẩn, so byte (INV-09/NFR-13) | lệch = chặn, phải giải trình |
| 7. Mutation smoke | `mutation_smoke.py` module chạm tiền, gate ≥70% killed (pattern P100) | dưới gate = chặn |
| 8. Audit deps | pip audit / npm audit | critical = chặn |
| 9. Coverage | ≥80% line mới | giảm = chặn |

Test chạm BQ live: job riêng nightly (không chặn PR) — kết quả vào dashboard, đỏ 2 đêm liên tiếp = dừng merge module liên quan.

## 2. CD

| Tầng | Cách | Ghi chú |
|---|---|---|
| dev | Docker compose local | $0 |
| staging | ??? (VM/Cloud Run — chốt trước GĐ1) | dữ liệu thật ẩn danh hóa? ??? |
| prod | deploy tay có checklist (`07` runbook) giai đoạn đầu; tự động hóa dần | team 1-2 người — đơn giản trước |

Mỗi go-live GĐ: tag + manifest (ORC-02 §4) + backup DB trước migrate.

## Changelog
- v0.1 (2026-07-17): Khởi tạo thiết kế; 2 ô ??? staging.
