Bạn là reviewer **R1** (agent `fls-test`, phiên MỚI, độc lập) cho **Step 7 · CG1** của ISP 3.1.2 dự án FLS. Phiên điều phối (orchestrator) giao; báo cáo cuối gửi orchestrator. ⛔ sửa mã hệ thống (`fls/**`, `tools/**`, `tests/**` ngoài `tests/nghiem_thu/**`) — vai của bạn là KIỂM.

## Đối tượng
- Nhánh `isp/CG1` ở worktree `/home/user/FLS-tobe/.claude/worktrees/isp-cg1` (đọc trực tiếp bằng đường dẫn tuyệt đối; ⛔ checkout trong checkout chính).
- Phạm vi diff: ``git diff 575926e isp/CG1` (mã `d6d50f4` + BG `84bcdbf`; nền `575926e` = `isp/base-w3`)` — R1: quét TOÀN BỘ diff. Phiếu `WO-101` ở `/home/user/FLS-tobe/docs/ITL/01_Orchestrator/handoff/WO-101-isp-cg1-cong-hd1-vao-gates.md`. Xét kỹ: (a) luật `doc_cong` ⛔ bao giờ trả danh sách toàn xanh + `chua_do_duoc` đếm đúng khi tệp vắng/hỏng/thiếu khoá; (b) Đ4 — `FINAL` 69.510 đếm '7 khối × 9.930 dòng giữ sau tự soi' (⛔ gồm 37 dòng tự-soi loại): nhãn có đủ để người đọc ⛔ hiểu nhầm là toàn sổ (69.769 ô) không — và quan hệ với quyết định `H2-R1-01` (37 dòng ấy bị phạt ở `HD1_THANG`, ⛔ ở `FINAL`); (c) đường dẫn tệp đo truyền vào (hợp đồng tầng 7, ⛔ gõ cứng); (d) CG1 chỉ đọc 5 khoá `dat_hd1` đã chốt — H2 đang đổi luật song song (nhánh `isp/H2` @ `b701ebb`): thử bài CG1 trên `voi_so_luong.json` của ngọn `isp/H2` (bản sao ở scratch) để chứng minh hợp đồng giữ.
- Spec duy nhất: `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` mục `## Step 7 · CG1` · phiếu `WO-101` · bàn giao `BG-102` · `CLAUDE.md` (Đ1–Đ5).

## Việc
1. ⛔ tin con số trong BG — tự chạy lại: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/api/test_isp_gates_hd1.py tests/api` · `python tools/soi_bang_tuyen.py` · gọi tuyến thật `GET /api/fls/v1/gates` · `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5444` (cổng hồi quy toàn bộ: đòi `KẾT: ĐẠT`) · `/home/user/FLS-tobe/.venv/bin/lint-imports` (11 kept) · đột biến tay ≥ 6 chỗ trong phần mới của `fls/repo/doc_bao_cao.py`.
   - Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python`; `export PG_DSN='postgresql://fls:fls@localhost:5444/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5444/fls_test' PYTHONUTF8=1`; chạy từ thư mục worktree.
2. Đối chiếu TỪNG dòng mục 8 (Exit criteria) + từng test ID mục 6 với bằng chứng; Đ1 (câu phủ định phải grep cả `docs/` lẫn `fls/`+`tools/`), Đ3 (phép ra 0/100% phải có mẫu số), Đ4 (số có nhãn), Đ5 (cổng khai `mong`, đã chứng minh đỏ).
3. Tìm: lỗi, lệch spec, phạm vi lấn sang bước khác, refactor không do test đòi, tệp ngoài quyền làn (`TIEN_DO.md` §Quy ước · ISP §2.1), PII (Email Address, Diễn giải, Số chứng từ, tên người), bí mật.
3b. Phân loại mọi phát hiện kiểu `/process-issues`: lớp **A1** (lỗi mã, sửa trong bước) · **A2** (lỗi mã, lớp lỗi lặp — kèm LUẬT phòng tái phạm) · **B1** (lệch spec/thiếu bài) · **B2** (spec/ISP sai — chuyển orchestrator); mỗi hàng có một dòng *luật phòng tái phạm* cho các bước sau. Ghi vào sổ riêng `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_CG1.md` (tạo mới; đầu sổ khai luật: vòng sau chỉ đổi ô Trạng thái + thêm hàng). Khuyến nghị sửa phải cụ thể đủ để agent tác giả làm theo, ưu tiên kèm bài đề xuất đã chứng minh ĐỎ/XANH.
4. Viết phiếu **`docs/ITL/01_Orchestrator/handoff/KQ-103-kiem-cg1-r1.md`** theo `docs/ITL/01_Orchestrator/handoff/_mau/KQ.md`: mỗi tiêu chí `ĐẠT / TRƯỢT / ⛔ KHÔNG ĐO ĐƯỢC` + bằng chứng (lệnh, exit code, dòng tổng kết); mỗi phát hiện: mã, mức (CHẶN / NÊN SỬA / GHI NHẬN), tệp:dòng, khuyến nghị sửa cụ thể. Commit phiếu lên CHÍNH nhánh `isp/CG1` trong worktree ấy (chỉ thêm tệp phiếu + sổ phát hiện riêng), message kết thúc bằng:
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
   `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`

## Báo cáo cuối
- Kết luận một dòng: `ĐẠT` (0 phát hiện CHẶN) hoặc `TRƯỢT` + số phát hiện theo mức.
- Bảng phát hiện (mã · mức · tệp:dòng · khuyến nghị) — để agent tác giả sửa theo.
- Sha commit phiếu.

## Cụm PG của bạn
- Cổng **5444** (cụm reviewer riêng, đang chạy; kiểm `pg_isready -h localhost -p 5444`). ⛔ chạm cụm khác; ⛔ chạy pytest khi CHƯA export cả `PG_DSN` lẫn `PG_DSN_TEST` (bài học `S0-R3-05`: một phiên thiếu DSN rơi về mặc định 5433 và DROP kho test của làn khác). Cụm tắt ⇒ báo orchestrator, ⛔ tự `initdb`.
- Tệp nháp: `<SCRATCHPAD>/r1_cg1/` (tạo nếu chưa có).
- Chạy song song với 8 phiên khác — ⛔ `git checkout`/`git stash` ở checkout chính; ⛔ push.
