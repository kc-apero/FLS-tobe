# Vòng sửa DT2 sau R2 (`KQ-088`) — ISP 3.1.2 · Step 8 · DT2 · làn FE ↩ DATA

- Worktree `/home/user/FLS-tobe/.claude/worktrees/isp-dt2` · nhánh `isp/DT2` @ `8e2fc95` · cụm PG **5436**. Sau bạn: R3 = `KQ-089`.
- Đọc: `docs/ITL/01_Orchestrator/handoff/KQ-088-kiem-dt2-r2.md` · `BG-086` · ISP Step 8 · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT2.md`.

## Việc
1. **`DT2-R2-01` (NÊN SỬA):** `nap_khuon` (`tools/dong_bang_sheet.py:165-170`) nạp khuôn theo đường tệp mà ⛔ đăng ký `sys.modules` ⇒ khuôn hợp lệ dùng `@dataclass` + `from __future__ import annotations` (lối CHUẨN của repo) bị TỪ CHỐI `AttributeError`. Sửa: đăng ký module trước `exec_module` (và gỡ khi nạp lỗi); bài: khuôn tạm có `@dataclass` nạp được.
2. **`DT2-R2-02` (NÊN SỬA):** bài `tests/du_lieu/test_dong_bang_sheet.py:823` ghim `danh_sach_khuon() == ["ix_fx"]` ⇒ thêm một khuôn là ĐỎ. Sửa: đòi `"ix_fx" in danh_sach_khuon()` + một bài THAM SỐ HOÁ trên `danh_sach_khuon()`: mọi khuôn có mặt đều qua `nap_khuon` và khai đủ hợp đồng khuôn. ⚠ Nhánh `isp/DT3` (song song) đã thêm 3 khuôn (`atl_cay` · …) và tự viết lại bài này theo cách riêng — **bản của bạn là bản orchestrator giữ khi gộp** ⇒ viết sao cho chạy đúng cả khi có thêm khuôn của DT3…DT12; ⛔ sửa nhánh DT3.
- **GHI NHẬN** của vòng ấy: sửa những cái phiếu ghi người làm `DEV` mà rẻ (≲ 15 dòng mã, ⛔ lấn phạm vi bước); cái nào ⛔ sửa thì liệt kê kèm lý do trong mục BG. ⛔ đụng việc phiếu ghi cho orchestrator/BA.
3. Thêm mục **"Vòng sửa sau R2 (KQ-088)"** vào `BG-086` (chỉ THÊM). Commit mã + commit phiếu.

## Luật chung (mọi phiên làm/sửa của lượt này)
- Bạn là agent `fls-dev` (phiên MỚI). Orchestrator = phiên điều phối ISP 3.1.2 của dự án FLS; báo cáo cuối gửi orchestrator. Đọc `CLAUDE.md` (Đ1–Đ5, Bẫy, Riêng tư) trong worktree trước khi làm.
- Chỉ làm trong worktree được giao (đường dẫn tuyệt đối); ⛔ `git checkout`/`git stash` ở checkout chính `/home/user/FLS-tobe`; ⛔ push; ⛔ sửa `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md`, `TIEN_DO.md`, changelog chung — việc của orchestrator.
- Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python` (+ `/home/user/FLS-tobe/.venv/bin/lint-imports`); LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5436/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5436/fls_test' PYTHONUTF8=1` TRƯỚC mọi pytest (bài học `S0-R3-05`: phiên thiếu DSN rơi về 5433 và DROP kho test của làn khác). Cụm tắt ⇒ báo orchestrator, ⛔ `initdb`.
- TDD nghiêm: bài ĐỎ trước (ghi lệnh + exit + dòng lỗi), mã tối thiểu, XANH; mỗi cổng mới chứng minh ĐỎ (phá → chạy → cắn → trả nguyên).
- Q8: bước thêm N bài ⇒ nâng `MONG_PYTEST_TOAN_BO` trong `tools/dung_moi_truong_isp.sh` (và bài ghim của nó nếu nhánh có) trong CÙNG commit; ghi số mới + cách đếm (`pytest --collect-only`) vào BG.
- Xác minh cuối: bài của bước + `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5436` (đòi `KẾT: ĐẠT`) + `lint-imports` (11 kept).
- ⛔ PII vào repo: Email Address · Diễn giải · Số chứng từ · tên người. ⛔ bí mật.
- Commit trên nhánh của bạn, message kết thúc bằng hai dòng:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`
- Chỗ mơ hồ ⇒ ⛔ đoán: dừng và báo orchestrator câu hỏi kèm khuyến nghị (A/B + vì sao).
- Tệp nháp: `<SCRATCHPAD>/data_dt2_sua_r2/`.

## Báo cáo cuối (gửi orchestrator)
- Một dòng kết luận + sha commit mã + sha commit phiếu.
- Bảng: mỗi tiêu chí/phát hiện → ĐÃ SỬA/ĐẠT · bằng chứng (lệnh · exit · dòng tổng kết) · ĐỎ-trước có/không.
- `MONG_PYTEST_TOAN_BO` cũ → mới.
- Câu hỏi còn treo (nếu có) kèm khuyến nghị.
