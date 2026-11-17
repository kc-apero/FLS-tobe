# Vòng sửa C1 sau R2 (`KQ-078`) — ISP 3.1.2 · Step 2 · C1 · làn BE-CF

- Worktree `/home/user/FLS-tobe/.claude/worktrees/isp-c1` · nhánh `isp/C1` @ `9feb114` · cụm PG **5434**. Sau bạn: R3 = `KQ-079` (orchestrator phát).
- Đọc: `docs/ITL/01_Orchestrator/handoff/KQ-078-kiem-c1-r2.md` · `BG-076` · ISP Step 2 · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C1.md`.

## Việc
1. **`C1-R2-01` (NÊN SỬA):** chốt `if d <= 0` của `_so` (`fls/cau_hinh/fx.py:192-193`) ⛔ bài nào ghim — đột biến `<= → <` và gỡ hẳn chốt đều `150 passed`; tỷ giá **`'0'`** (khớp khuôn `[0-9]+`) phải bị TỪ CHỐI có tên — đúng lỗi *"SUMIFS = 0 ⇒ mất số không báo"* bước này sinh ra để chặn. Thêm bài ca `'0'` · `'0.0'` · `'0,00'` (⇒ lỗi có tên), sửa nhãn ca `"-5"` ở `tests/cau_hinh/test_fx.py:166` cho đúng thứ nó chặn; chứng minh hai đột biến ấy CHẾT.
- **GHI NHẬN** của vòng ấy: sửa những cái phiếu ghi người làm `DEV` mà rẻ (≲ 15 dòng mã, ⛔ lấn phạm vi bước); cái nào ⛔ sửa thì liệt kê kèm lý do trong mục BG. ⛔ đụng việc phiếu ghi cho orchestrator/BA.
2. Thêm mục **"Vòng sửa sau R2 (KQ-078)"** vào `BG-076` (chỉ THÊM). Commit mã + commit phiếu.

## Luật chung (mọi phiên làm/sửa của lượt này)
- Bạn là agent `fls-dev` (phiên MỚI). Orchestrator = phiên điều phối ISP 3.1.2 của dự án FLS; báo cáo cuối gửi orchestrator. Đọc `CLAUDE.md` (Đ1–Đ5, Bẫy, Riêng tư) trong worktree trước khi làm.
- Chỉ làm trong worktree được giao (đường dẫn tuyệt đối); ⛔ `git checkout`/`git stash` ở checkout chính `/home/user/FLS-tobe`; ⛔ push; ⛔ sửa `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md`, `TIEN_DO.md`, changelog chung — việc của orchestrator.
- Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python` (+ `/home/user/FLS-tobe/.venv/bin/lint-imports`); LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5434/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5434/fls_test' PYTHONUTF8=1` TRƯỚC mọi pytest (bài học `S0-R3-05`: phiên thiếu DSN rơi về 5433 và DROP kho test của làn khác). Cụm tắt ⇒ báo orchestrator, ⛔ `initdb`.
- TDD nghiêm: bài ĐỎ trước (ghi lệnh + exit + dòng lỗi), mã tối thiểu, XANH; mỗi cổng mới chứng minh ĐỎ (phá → chạy → cắn → trả nguyên).
- Q8: bước thêm N bài ⇒ nâng `MONG_PYTEST_TOAN_BO` trong `tools/dung_moi_truong_isp.sh` (và bài ghim của nó nếu nhánh có) trong CÙNG commit; ghi số mới + cách đếm (`pytest --collect-only`) vào BG.
- Xác minh cuối: bài của bước + `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` (đòi `KẾT: ĐẠT`) + `lint-imports` (11 kept).
- ⛔ PII vào repo: Email Address · Diễn giải · Số chứng từ · tên người. ⛔ bí mật.
- Commit trên nhánh của bạn, message kết thúc bằng hai dòng:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`
- Chỗ mơ hồ ⇒ ⛔ đoán: dừng và báo orchestrator câu hỏi kèm khuyến nghị (A/B + vì sao).
- Tệp nháp: `<SCRATCHPAD>/cf_c1_sua_r2/`.

## Báo cáo cuối (gửi orchestrator)
- Một dòng kết luận + sha commit mã + sha commit phiếu.
- Bảng: mỗi tiêu chí/phát hiện → ĐÃ SỬA/ĐẠT · bằng chứng (lệnh · exit · dòng tổng kết) · ĐỎ-trước có/không.
- `MONG_PYTEST_TOAN_BO` cũ → mới.
- Câu hỏi còn treo (nếu có) kèm khuyến nghị.
