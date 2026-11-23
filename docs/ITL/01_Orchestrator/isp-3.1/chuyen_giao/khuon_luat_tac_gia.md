
## Luật chung (mọi phiên làm/sửa của lượt này)
- Bạn là agent `fls-dev` (phiên MỚI). Orchestrator = phiên điều phối ISP 3.1.2 của dự án FLS; báo cáo cuối gửi orchestrator. Đọc `CLAUDE.md` (Đ1–Đ5, Bẫy, Riêng tư) trong worktree trước khi làm.
- Chỉ làm trong worktree được giao (đường dẫn tuyệt đối); ⛔ `git checkout`/`git stash` ở checkout chính `/home/user/FLS-tobe`; ⛔ push; ⛔ sửa `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md`, `TIEN_DO.md`, changelog chung — việc của orchestrator.
- Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python` (+ `/home/user/FLS-tobe/.venv/bin/lint-imports`); LUÔN `export PG_DSN='postgresql://fls:fls@localhost:{P}/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:{P}/fls_test' PYTHONUTF8=1` TRƯỚC mọi pytest (bài học `S0-R3-05`: phiên thiếu DSN rơi về 5433 và DROP kho test của làn khác). Cụm tắt ⇒ báo orchestrator, ⛔ `initdb`.
- TDD nghiêm: bài ĐỎ trước (ghi lệnh + exit + dòng lỗi), mã tối thiểu, XANH; mỗi cổng mới chứng minh ĐỎ (phá → chạy → cắn → trả nguyên).
- Q8: bước thêm N bài ⇒ nâng `MONG_PYTEST_TOAN_BO` trong `tools/dung_moi_truong_isp.sh` (và bài ghim của nó nếu nhánh có) trong CÙNG commit; ghi số mới + cách đếm (`pytest --collect-only`) vào BG.
- Xác minh cuối: bài của bước + `bash tools/dung_moi_truong_isp.sh --duong-nen --cong {P}` (đòi `KẾT: ĐẠT`) + `lint-imports` (11 kept).
- ⛔ PII vào repo: Email Address · Diễn giải · Số chứng từ · tên người. ⛔ bí mật.
- Commit trên nhánh của bạn, message kết thúc bằng hai dòng:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`
- Chỗ mơ hồ ⇒ ⛔ đoán: dừng và báo orchestrator câu hỏi kèm khuyến nghị (A/B + vì sao).
- Tệp nháp: `<SCRATCHPAD>/{NHAP}/`.

## Báo cáo cuối (gửi orchestrator)
- Một dòng kết luận + sha commit mã + sha commit phiếu.
- Bảng: mỗi tiêu chí/phát hiện → ĐÃ SỬA/ĐẠT · bằng chứng (lệnh · exit · dòng tổng kết) · ĐỎ-trước có/không.
- `MONG_PYTEST_TOAN_BO` cũ → mới.
- Câu hỏi còn treo (nếu có) kèm khuyến nghị.
