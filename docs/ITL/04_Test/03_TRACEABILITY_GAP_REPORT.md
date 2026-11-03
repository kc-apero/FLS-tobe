# 03 — TRACEABILITY & GAP REPORT

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Version:** v0.1 (sống) | **Chủ sở hữu:** QA

---

## 1. Ma trận truy vết (cập nhật mỗi khi thêm test)

| Spec | Tổng mục | Có TC | Có code test | Gap |
|---|---|---|---|---|
| BA-09 SM (5 máy) | 16 T + 8 F | 0 | 0 | chưa vào GĐ0 build |
| BA-10 DT (7 bảng) | ~20 nhánh | 0 | 0 | — |
| BA-11 INV (12) | 12 + 3 job | 0 | 0 | — |
| BA-03 US (EP-00/01) | 11 story | 0 | 0 | — |
| BA-04 RP/SOD | ma trận + 4 SOD | 0 | 0 | — |
| BA-07 ERR | 10 mã | 0 | 0 | — |

*(Bảng này là forward-fill: 0 là đúng hiện trạng — dự án chưa code. Khác P100 back-fill.)*

## 2. GAP_REPORT (spec thiếu/mâu thuẫn — AI không tự đóng, R5)

| ID | Mô tả | Phát hiện bởi | Quyết định con người |
|---|---|---|---|
| *(trống)* | | | |

## 3. ERROR_REPORT (bug tìm thấy khi test)

| ID | Mô tả | TC tái hiện | Trạng thái |
|---|---|---|---|
| *(trống)* | | | |

## 4. Checklist trước đóng băng mỗi GĐ

- [ ] 100% T/F của SM liên quan GĐ có test pass/chặn
- [ ] 100% ERR liên quan có negative test
- [ ] INV liên quan có property test + job kiểm chạy trong CI
- [ ] Mutation smoke module chạm tiền ≥70% killed
- [ ] Critic session đã chạy, GAP mở có quyết định con người
- [ ] Người vận hành chạy thử kịch bản nghiệm thu (ORC-03) trên staging

## Changelog
- v0.1 (2026-07-17): Khởi tạo khuôn forward-fill.
