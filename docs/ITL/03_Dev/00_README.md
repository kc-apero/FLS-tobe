# 00 — README: Dev Kit (AI-first)

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Dự án:** VOI — Hệ thống Tài chính Nội bộ | **Phiên bản bộ:** v0.1 | **Chủ sở hữu (Tech Lead):** COO-CFO + AI

Bộ artifact Dev sản xuất và duy trì, giữa **BA Kit** (spec nguồn) và **Testing Kit** (kiểm chứng). Khác P100 (back-fill từ code có sẵn), VOI là **forward-fill**: doc viết trước code — trừ phần kế thừa P100/T3 thì tham chiếu, không chép.

Quy ước: `BA-xx` / `TEST-xx` = file kit tương ứng; số trần = nội bộ Dev Kit.

---

## 1. Cấu trúc bộ (8 file)

| File | Vai trò | Nguồn chính | Độ chín v0.1 |
|---|---|---|---|
| `01_TECH_DESIGN.md` | Kiến trúc phương án A chi tiết kỹ thuật | brainstorm + `BA-08` | ● |
| `02_REPO_CONVENTIONS.md` | Cấu trúc repo, quy ước, luật phiên AI | chuẩn nội bộ + P100 | ◐ (chờ GAP-VOI-04) |
| `03_IMPLEMENTATION_PLAN.md` | Chia module → task theo GĐ, thứ tự phụ thuộc | `BA-03` + ORC-03 | ● GĐ0-1, khung GĐ2+ |
| `04_DB_IMPLEMENTATION.md` | Hiện thực schema + kỷ luật migration | `BA-05` | ● M0+M2 |
| `05_API_IMPLEMENTATION.md` | Ánh xạ contract → handler | `BA-07` | ◐ |
| `06_CICD_PIPELINE.md` | Build, cổng test, deploy | `TEST-01` + `BA-08` | ◐ |
| `07_RUNBOOK.md` | Triển khai, rollback, giám sát, sự cố | `BA-08` | ◐ |
| `08_CHANGELOG_RELEASE.md` | Nhật ký + manifest go-live | ORC-02 | ● (trống, sẵn khuôn) |

## 2. Quy tắc phiên AI (kế thừa R-A + R-D của P100, nguyên văn)

R-D1 code đúng spec đã trace, thiếu spec → GAP_REPORT · R-D2 tên trường/endpoint/state nguyên văn `BA-05/07/09` · R-D3 không hardcode quy tắc nghiệp vụ — mọi ngưỡng/quy tắc đọc từ Rule Registry (P-05) · R-D4 một phiên một task · R-D5 INV enforce tầng DB · R-D6 schema chỉ đổi qua migration.

**R-D7 (mới, riêng VOI):** module chạm tiền/duyệt/chữ ký — cấm mock DB trong test nghiệm thu; bắt buộc PG container + (khi chạm BQ) luồng live. *(bài học fake-BQ che bug)*

## 3. Thứ tự sản xuất

1. `01`+`02` trước dòng code đầu tiên → 2. `04` migration M0 → 3. `05` khung API M0 → 4. `03` task GĐ0 → code → Testing Kit → 5. `06`+`07` trước go-live GĐ0 → 6. `08` mỗi go-live.

## Changelog
- v0.1 (2026-07-17): Khởi tạo.
