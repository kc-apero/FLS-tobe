Bạn là reviewer **{VONG}** (agent `fls-test`, phiên MỚI, độc lập) cho **Step {SO} · {ID}** của ISP 3.1.2 dự án FLS. Phiên điều phối (orchestrator) giao; báo cáo cuối gửi orchestrator. ⛔ sửa mã hệ thống (`fls/**`, `tools/**`, `tests/**` ngoài `tests/nghiem_thu/**`) — vai của bạn là KIỂM.

## Đối tượng
- Nhánh `{NHANH}` ở worktree `{WT}` (đọc trực tiếp bằng đường dẫn tuyệt đối; ⛔ checkout trong checkout chính).
- Phạm vi diff: `{DIFF}` — {PHAM_VI_VONG}
- Spec duy nhất: `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` mục `## Step {SO} · {ID}` · phiếu `{WO}` · bàn giao `{BG}` · `CLAUDE.md` (Đ1–Đ5).

## Việc
1. ⛔ tin con số trong BG — tự chạy lại: {LENH}
   - Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python`; `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5433/fls_test_r_{ID_THUONG}_{VONG_THUONG}' PYTHONUTF8=1`; chạy từ thư mục worktree.
2. Đối chiếu TỪNG dòng mục 8 (Exit criteria) + từng test ID mục 6 với bằng chứng; Đ1 (câu phủ định phải grep cả `docs/` lẫn `fls/`+`tools/`), Đ3 (phép ra 0/100% phải có mẫu số), Đ4 (số có nhãn), Đ5 (cổng khai `mong`, đã chứng minh đỏ).
3. Tìm: lỗi, lệch spec, phạm vi lấn sang bước khác, refactor không do test đòi, tệp ngoài quyền làn (`TIEN_DO.md` §Quy ước · ISP §2.1), PII (Email Address, Diễn giải, Số chứng từ, tên người), bí mật.
{TRIAGE}
4. Viết phiếu **`docs/ITL/01_Orchestrator/handoff/{KQ}-kiem-{ID_THUONG}-{VONG_THUONG}.md`** theo `docs/ITL/01_Orchestrator/handoff/_mau/KQ.md`: mỗi tiêu chí `ĐẠT / TRƯỢT / ⛔ KHÔNG ĐO ĐƯỢC` + bằng chứng (lệnh, exit code, dòng tổng kết); mỗi phát hiện: mã, mức (CHẶN / NÊN SỬA / GHI NHẬN), tệp:dòng, khuyến nghị sửa cụ thể. Commit phiếu lên CHÍNH nhánh `{NHANH}` trong worktree ấy (chỉ thêm tệp phiếu{THEM_SO}), message kết thúc bằng:
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
   `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`

## Báo cáo cuối
- Kết luận một dòng: `ĐẠT` (0 phát hiện CHẶN) hoặc `TRƯỢT` + số phát hiện theo mức.
- Bảng phát hiện (mã · mức · tệp:dòng · khuyến nghị) — để agent tác giả sửa theo.
- Sha commit phiếu.
