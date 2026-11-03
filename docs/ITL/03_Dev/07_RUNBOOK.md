# 07 — RUNBOOK: vận hành, sự cố, rollback

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Version:** v0.1 | **Chủ sở hữu:** Tech Lead | **Độ chín:** khung — điền cụ thể trước go-live GĐ0, cập nhật mỗi GĐ

---

## 1. Thông tin nền

| Mục | Giá trị |
|---|---|
| BE Core | uvicorn, port ??? (tránh lặp bài học nhầm 8000/8001 — ghi rõ khi dựng) |
| Health | `/health` (process) + `/ready` (PG, BQ, sync lag) |
| DB | dev Docker PG · prod Cloud SQL (PITR) |
| Log | JSON có requestId; ERROR = có người xem |

## 2. Quy trình chuẩn

- **Deploy:** backup/PITR checkpoint → migrate → deploy → smoke (health + 1 luồng thật mỗi module go-live) → công bố.
- **Rollback:** code = deploy tag trước; DB = down migration (nếu an toàn) hoặc PITR — quyết theo bảng phân loại sự cố dưới.
- **Sau sửa code BE:** restart + verify health + chạy luồng thật liên quan (quy ước sẵn có).

## 3. Sự cố đặc thù hệ tài chính

| Sự cố | Phản ứng |
|---|---|
| Ingest fail (contract violation) | KHÔNG force-nạp. Đọc lý do gate trả về, sửa file nguồn hoặc mở CR nếu contract sai. File hỏng lặp lại → liên hệ nguồn (network đổi format = việc nghiệp vụ, không phải bug) |
| Sync PG→BQ trễ | alert tự động; Compute run đang chạy vẫn an toàn (pin snapshot); chặn run MỚI tới khi sync xanh |
| Số liệu nghi sai sau final | KHÔNG sửa DB tay (INV-02). Đường duy nhất: adjustment entry / quy trình hồi tố DT-04. Sửa tay DB hệ tài chính = phá niềm tin toàn hệ |
| Job đối soát báo chênh | exception có owner — xử theo SM-ALERT, không tắt alert |
| Nghi ngờ độc hại/thao túng | freeze quyền user liên quan, snapshot audit_log, báo COO-CFO — khung kỷ luật ĐK10 |

## 4. Giám sát tối thiểu (GĐ0–1)

4 tín hiệu: error rate API · p95 latency (NFR-01) · sync lag (NFR-07) · alert tồn đọng quá deadline. Thêm dashboard đầy đủ ở GĐ3 cùng M6.

## Changelog
- v0.1 (2026-07-17): Khởi tạo khung.
