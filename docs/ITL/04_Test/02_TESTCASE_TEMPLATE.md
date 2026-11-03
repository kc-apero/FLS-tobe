# 02 — TESTCASE TEMPLATE

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Version:** v0.1 | **Chủ sở hữu:** QA

---

## 1. Quy ước ID ↔ tên hàm

`TC-<nguồn>-<số>` ↔ `test_<nguồn viết thường>_<mô tả ngắn>`

| Nguồn | Ví dụ ID | Ví dụ tên hàm |
|---|---|---|
| User story | TC-US101-01 | `test_us101_missing_dimension_rejected` |
| State machine | TC-FPER1-01 | `test_fper1_reopen_final_period_blocked` |
| Decision table | TC-DT03-02 | `test_dt03_tranche_100pct_hard_block` |
| Invariant | TC-INV11-01 | `test_inv11_entry_balance_per_currency_property` |
| Bug production | TC-BUG-<id> | `test_bug_<id>_<mô tả>` — vĩnh viễn |

## 2. Template

```markdown
### TC-<ID> — <tên ngắn>
- **Trace:** US-xxx / T|F-xxx / DT-xx / INV-xx / SOD-xx / ERR-VOI-xxx
- **Tầng:** unit | property | integration | golden | e2e
- **Given:** <trạng thái đầu — dữ liệu, vai, kỳ, rule version>
- **When:** <hành động — API/hàm nguyên văn BA-07/DEV-05>
- **Then:** <kỳ vọng — state/mã lỗi/side-effect nguyên văn spec>
- **Ghi chú dữ liệu:** <tiền tệ, số biên, ngày đặc biệt nếu có>
```

## 3. Ví dụ điền sẵn

### TC-DT03-02 — chặn cứng khi hết tranche
- **Trace:** DT-03 / INV-07 / ERR-VOI-003 / US-102
- **Tầng:** integration (PG thật — R6)
- **Given:** task force TF-X active, tranche 1 = 100tr, lũy kế chi đã duyệt 100tr, gate chưa passed; user BU head hợp lệ
- **When:** POST đề xuất chi mới 1tr cho TF-X
- **Then:** 422 `TRANCHE_EXHAUSTED`; đề xuất không được tạo; alert `tranche_100` tồn tại với owner = TF-X owner

### TC-INV05-01 — rule effective bất biến
- **Trace:** INV-05 / F-RUL-1 / ERR-VOI-004
- **Tầng:** integration
- **Given:** rule_set allocation v2 status=effective, content_hash=H
- **When:** UPDATE payload trực tiếp bằng role app; và PATCH qua API
- **Then:** cả hai bị chặn; content_hash vẫn = H; audit không có bản ghi update thành công

## Changelog
- v0.1 (2026-07-17): Khởi tạo + 2 ví dụ.
