Bạn là reviewer **R3b** (agent `fls-test`, phiên MỚI, độc lập) cho **Step 0 · S0** của ISP 3.1.2 dự án FLS. Phiên điều phối (orchestrator) giao; báo cáo cuối gửi orchestrator. ⛔ sửa mã hệ thống (`fls/**`, `tools/**`, `tests/**` ngoài `tests/nghiem_thu/**`) — vai của bạn là KIỂM.

## Đối tượng
- Nhánh `isp/S0` ở worktree `/home/user/FLS-tobe/.claude/worktrees/isp-s0` (đọc trực tiếp bằng đường dẫn tuyệt đối; ⛔ checkout trong checkout chính).
- Phạm vi diff: ``git diff fb79f7e isp/S0` (vòng sửa sau R3: mã `7bf75d3` + mục BG `c1cf29b`)` — R3b = vòng XÁC NHẬN lại của R3 chỉ trên thay đổi sau `KQ-069` (thang orchestrator: được gộp + push khi 0 CHẶN **và** 0 NÊN SỬA còn mở). Xét 5 phát hiện `S0-R3-01…05`: `-01` xfail có `mong` theo TÊN + LOẠI (tái hiện plugin biến bài xanh thành xfail ⇒ phải `KẾT: ĐỎ`) · `-02` sàn `MONG_PYTEST_TOAN_BO` (2490) = số thu thập · `-03` DSN sai lược đồ ⛔ lộ mật khẩu · `-04` câu khai §4.3 · `-05` khai quy ước `PG_DSN`. ⚠ Chạy `--duong-nen` ít nhất 2 lượt sạch; nếu một lượt đỏ do phiên LẠ, chứng minh bằng log cụm như R3 đã làm.
- Spec duy nhất: `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` mục `## Step 0 · S0` · phiếu `WO-065` · bàn giao `BG-066` · `CLAUDE.md` (Đ1–Đ5).

## Việc
1. ⛔ tin con số trong BG — tự chạy lại: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/test_dung_moi_truong_isp.py` · `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5433` (cổng hồi quy toàn bộ: đòi `KẾT: ĐẠT`) · `/home/user/FLS-tobe/.venv/bin/lint-imports` (11 kept) · ca phá xfail của R3 (scratch `r3_s0/`) trên mã mới.
   - Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python`; `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5433/fls_test' PYTHONUTF8=1`; chạy từ thư mục worktree.
2. Đối chiếu TỪNG dòng mục 8 (Exit criteria) + từng test ID mục 6 với bằng chứng; Đ1 (câu phủ định phải grep cả `docs/` lẫn `fls/`+`tools/`), Đ3 (phép ra 0/100% phải có mẫu số), Đ4 (số có nhãn), Đ5 (cổng khai `mong`, đã chứng minh đỏ).
3. Tìm: lỗi, lệch spec, phạm vi lấn sang bước khác, refactor không do test đòi, tệp ngoài quyền làn (`TIEN_DO.md` §Quy ước · ISP §2.1), PII (Email Address, Diễn giải, Số chứng từ, tên người), bí mật.
3b. Chỉ xét THAY ĐỔI sau vòng trước: mỗi phát hiện vòng trước ⇒ `ĐÃ SỬA` (tái hiện ĐỎ trên bản cũ, XANH trên bản mới) / `CHƯA SỬA` / `CHẤP NHẬN` (orchestrator đã quyết); tìm hồi quy do chính vòng sửa đưa vào. Cập nhật sổ chung `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1.md`: chỉ đổi ô Trạng thái hàng cũ + thêm hàng mới, phân loại A1/A2/B1/B2 + luật phòng tái phạm.
4. Viết phiếu **`docs/ITL/01_Orchestrator/handoff/KQ-100-kiem-s0-r3b.md`** theo `docs/ITL/01_Orchestrator/handoff/_mau/KQ.md`: mỗi tiêu chí `ĐẠT / TRƯỢT / ⛔ KHÔNG ĐO ĐƯỢC` + bằng chứng (lệnh, exit code, dòng tổng kết); mỗi phát hiện: mã, mức (CHẶN / NÊN SỬA / GHI NHẬN), tệp:dòng, khuyến nghị sửa cụ thể. Commit phiếu lên CHÍNH nhánh `isp/S0` trong worktree ấy (chỉ thêm tệp phiếu + sổ phát hiện chung (cập nhật)), message kết thúc bằng:
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
   `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`

## Báo cáo cuối
- Kết luận một dòng: `ĐẠT` (0 phát hiện CHẶN) hoặc `TRƯỢT` + số phát hiện theo mức.
- Bảng phát hiện (mã · mức · tệp:dòng · khuyến nghị) — để agent tác giả sửa theo.
- Sha commit phiếu.

## Cụm PG của bạn
- Cổng **5433** (cụm reviewer riêng, đang chạy; kiểm `pg_isready -h localhost -p 5433`). ⛔ chạm cụm khác; ⛔ chạy pytest khi CHƯA export cả `PG_DSN` lẫn `PG_DSN_TEST` (bài học `S0-R3-05`: một phiên thiếu DSN rơi về mặc định 5433 và DROP kho test của làn khác). Cụm tắt ⇒ báo orchestrator, ⛔ tự `initdb`.
- Tệp nháp: `<SCRATCHPAD>/r3b_s0/` (tạo nếu chưa có).
- Chạy song song với 8 phiên khác — ⛔ `git checkout`/`git stash` ở checkout chính; ⛔ push.
