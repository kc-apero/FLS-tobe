# Vòng sửa DT1b sau R1 (`KQ-097`) — ISP 3.1.2 · Step 5 · DT1b · làn DATA

- Worktree `/home/user/FLS-tobe/.claude/worktrees/isp-dt1b` · nhánh `isp/DT1B` @ `4b351d3` · cụm PG **5437**. Sau bạn: R2 = `KQ-098`.
- Đọc: `docs/ITL/01_Orchestrator/handoff/KQ-097-kiem-dt1b-r1.md` (bảng phát hiện + **§Bài thử đề xuất ①–⑭** + §Kịch bản phá S1–S5) · `BG-096` · ISP Step 5 · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1b.md`.

## Việc — 5 NÊN SỬA (mỗi cái tái hiện ĐỎ trên `8a18599` trước)
1. **`DT1b-R1-01`:** 10 đột biến lõi ghép (`tools/phan_loai_ly_do.py:279-312`) sống ⇒ 6 bài đơn vị gọi thẳng `phan_loai` (đề xuất ①–⑥); chứng minh 10 đột biến CHẾT.
2. **`DT1b-R1-02`:** đột biến D17–D22 sống (R5 tiền · R5 thô/chuẩn hoá · R6 `sochungtu`/`email` · R3 tên khoá) ⇒ bài R5 × 3 qua đường đo thật + 3 ca `PHA` (⑦ ⑧).
3. **`DT1b-R1-04`:** 7/7 lá tự do ⇒ exit 0 (S2) ⇒ so hằng/mẫu cho từng lá; câu lỗi ⛔ in GIÁ TRỊ khoá (⑬).
4. **`DT1b-R1-05`:** đổi nhãn 2 dòng cùng kỳ ⇒ exit 0 (S1) ⇒ `MONG["van_tay_nhan"]` + K13; sửa câu `BG-096:176` bằng đính chính chỉ-THÊM (⑭).
5. **`DT1b-R1-06`:** CSV khoá THÔ đặt trong repo (`docs/ITL/_tools/`) ⇒ exit 0 (S5) ⇒ từ chối mọi đường dẫn đầu vào nằm trong repo mà ⛔ bị gitignore (mã 2) + bài `git init` ở `tmp_path`.
- **GHI NHẬN** của vòng ấy: sửa những cái phiếu ghi người làm `DEV` mà rẻ (≲ 15 dòng mã, ⛔ lấn phạm vi bước); cái nào ⛔ sửa thì liệt kê kèm lý do trong mục BG. ⛔ đụng việc phiếu ghi cho orchestrator/BA.
6. Thêm mục **"Vòng sửa sau R1 (KQ-097)"** vào `BG-096` (chỉ THÊM). Commit mã + commit phiếu.
- ⚠ Nhãn THẬT vẫn chờ (`B-DATA-2`): người dùng đang dựng khoá SA chỉ-đọc — có thể đọc được RAW gốc về sau; bước này vẫn chỉ trên dữ liệu TỔNG HỢP, ⛔ đoán khoá thật.

## Luật chung (mọi phiên làm/sửa của lượt này)
- Bạn là agent `fls-dev` (phiên MỚI). Orchestrator = phiên điều phối ISP 3.1.2 của dự án FLS; báo cáo cuối gửi orchestrator. Đọc `CLAUDE.md` (Đ1–Đ5, Bẫy, Riêng tư) trong worktree trước khi làm.
- Chỉ làm trong worktree được giao (đường dẫn tuyệt đối); ⛔ `git checkout`/`git stash` ở checkout chính `/home/user/FLS-tobe`; ⛔ push; ⛔ sửa `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md`, `TIEN_DO.md`, changelog chung — việc của orchestrator.
- Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python` (+ `/home/user/FLS-tobe/.venv/bin/lint-imports`); LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5437/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5437/fls_test' PYTHONUTF8=1` TRƯỚC mọi pytest (bài học `S0-R3-05`: phiên thiếu DSN rơi về 5433 và DROP kho test của làn khác). Cụm tắt ⇒ báo orchestrator, ⛔ `initdb`.
- TDD nghiêm: bài ĐỎ trước (ghi lệnh + exit + dòng lỗi), mã tối thiểu, XANH; mỗi cổng mới chứng minh ĐỎ (phá → chạy → cắn → trả nguyên).
- Q8: bước thêm N bài ⇒ nâng `MONG_PYTEST_TOAN_BO` trong `tools/dung_moi_truong_isp.sh` (và bài ghim của nó nếu nhánh có) trong CÙNG commit; ghi số mới + cách đếm (`pytest --collect-only`) vào BG.
- Xác minh cuối: bài của bước + `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5437` (đòi `KẾT: ĐẠT`) + `lint-imports` (11 kept).
- ⛔ PII vào repo: Email Address · Diễn giải · Số chứng từ · tên người. ⛔ bí mật.
- Commit trên nhánh của bạn, message kết thúc bằng hai dòng:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`
- Chỗ mơ hồ ⇒ ⛔ đoán: dừng và báo orchestrator câu hỏi kèm khuyến nghị (A/B + vì sao).
- Tệp nháp: `<SCRATCHPAD>/data_dt1b_sua_r1/`.

## Báo cáo cuối (gửi orchestrator)
- Một dòng kết luận + sha commit mã + sha commit phiếu.
- Bảng: mỗi tiêu chí/phát hiện → ĐÃ SỬA/ĐẠT · bằng chứng (lệnh · exit · dòng tổng kết) · ĐỎ-trước có/không.
- `MONG_PYTEST_TOAN_BO` cũ → mới.
- Câu hỏi còn treo (nếu có) kèm khuyến nghị.
