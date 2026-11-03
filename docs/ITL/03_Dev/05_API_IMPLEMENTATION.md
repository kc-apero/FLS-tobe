# 05 — API IMPLEMENTATION: contract → handler

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Version:** v0.1 | **Chủ sở hữu:** Tech Lead | **Nguồn:** `BA-07` | **Độ chín:** khung + nhóm M0; JIT theo GĐ

---

## 1. Khung chung

- FastAPI router per module (`01` §4); mọi router qua middleware: auth (JWT fail-closed) → RBAC/row-level (`BA-04`) → audit (mutation).
- Response envelope + `data_status` + `requestId` build ở dependency chung — handler không tự chế envelope.
- Mã lỗi nghiệp vụ map ERR-VOI-xxx (`BA-07` §2) qua exception class chung; HTTP: 400/401/403/404/409/422/429/500 chuẩn.
- Validation: Pydantic schema per endpoint; reject sớm, không sanitize-rồi-tiếp.

## 2. Ánh xạ nhóm M0

| API | Handler | Ghi chú hiện thực |
|---|---|---|
| API-001 org-units | `m0_spine/router.py::create_org_unit / activate` | activate chạy validate SM-ORG T-ORG-1 (task force phải đủ tranche+gate+exit — trả 422 danh sách thiếu) |
| API-002 AU + mappings | `::create_au / add_mapping` | bắt ERR-VOI-008 từ EXCLUDE constraint → message thân thiện |
| API-003 owner?at= | `::resolve_owner` | 1 query trên mapping; index sẵn |
| API-004 rule-sets | `::create_rule / approve_rule / list_rules` | approve yêu cầu resolution; GET theo `period` resolve đúng version hiệu lực (INV-05); trả kèm content_hash |
| API-005 audit-log | `shared/audit.py::query` | read-only, phân trang cursor |

## 3. Quy tắc handler (mọi module)

1. Handler mỏng: parse/validate → gọi service → map lỗi. Logic nằm ở service (test không cần HTTP).
2. Service chạm nhiều bảng = transaction; không commit giữa chừng.
3. Đọc rule: luôn qua `rules.get(rule_type, period)` — cấm query rule_sets trực tiếp từ module khác.
4. Endpoint trả số liệu: bắt buộc khai báo `data_status` nguồn (flash/reconciled/signed) — thiếu → review chặn.

`???` — bảng ánh xạ M1 delta/M2/M3/M5/M6/M4: JIT đầu GĐ tương ứng.

## Changelog
- v0.1 (2026-07-17): Khởi tạo.
