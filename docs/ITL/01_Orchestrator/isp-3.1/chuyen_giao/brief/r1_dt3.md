Bạn là reviewer **R1** (agent `fls-test`, phiên MỚI, độc lập) cho **Step 10 · DT3** của ISP 3.1.2 dự án FLS. Phiên điều phối (orchestrator) giao; báo cáo cuối gửi orchestrator. ⛔ sửa mã hệ thống (`fls/**`, `tools/**`, `tests/**` ngoài `tests/nghiem_thu/**`) — vai của bạn là KIỂM.

## Đối tượng
- Nhánh `isp/DT3` ở worktree `/home/user/FLS-tobe/.claude/worktrees/isp-dt3` (đọc trực tiếp bằng đường dẫn tuyệt đối; ⛔ checkout trong checkout chính).
- Phạm vi diff: ``git diff 80496ec isp/DT3` (mã `2a31f76` + BG `5a96cd9`; nền = `isp/DT2` @ `80496ec`)` — R1: quét TOÀN BỘ diff. Phiếu `WO-106` ở `/home/user/FLS-tobe/docs/ITL/01_Orchestrator/handoff/WO-106-isp-dt3-anh-ix-hd-ix-org.md` (quyết định ⑪ CDT = 13 · ⑫ `AA:AD` ⛔ thuộc RAW). Xét kỹ: (a) **PII là rủi ro số 1** — 7 hàng Mapping Master mang tên viết tắt NGƯỜI ở cột A · B · O: quét MỌI tệp của diff (ảnh, bài, BG, message commit `git log 80496ec..isp/DT3`) ⇒ 0 tên; băm có muối/khai cách, ⛔ đảo ngược được bằng từ điển nhỏ (thử: băm thử ~200 tên viết tắt kiểu `<TÊN_VIẾT_TẮT>` có khớp không — nếu băm KHÔNG muối thì là NÊN SỬA trở lên); (b) đối chiếu ảnh với bản thô orchestrator ở `<SCRATCHPAD>/drive_tho/` (đo độc lập 74 · 6 · 73 · 13); (c) Mapping Master = ĐẦU RA `fls.adapters.mapping_master.doc_cot` (⛔ khuôn đọc thứ hai); (d) DT3 đã VIẾT LẠI một bài DT2 (`test_KHUON_ix_fx_la_mot_tep_…`, ghim `danh_sach_khuon() == ['ix_fx']`) — đó cũng là `DT2-R2-02` mà vòng sửa DT2 đang làm song song ⇒ ghi nhận xung đột gộp, orchestrator sẽ lấy bản DT2 khi gộp; chỉ xét bản DT3 có làm yếu bài không; (e) Q8: nhánh ⛔ có `MONG_PYTEST_TOAN_BO` (tách trước S0 `1291ad5`) — orchestrator đã chấp nhận Q1 = A (cộng Δ = +65 lúc gộp), ⛔ tính là phát hiện.
- Spec duy nhất: `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` mục `## Step 10 · DT3` · phiếu `WO-106` · bàn giao `BG-107` · `CLAUDE.md` (Đ1–Đ5).

## Việc
1. ⛔ tin con số trong BG — tự chạy lại: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/du_lieu/test_anh_cau_hinh.py tests/du_lieu/test_dong_bang_sheet.py` · chạy lại đường ống trên ba bản thô (checksum khớp ảnh commit) · `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5446` (cổng hồi quy toàn bộ: đòi `KẾT: ĐẠT`) · `/home/user/FLS-tobe/.venv/bin/lint-imports` (11 kept) · ca phá mỗi ảnh (xoá 1 dòng ở BẢN SAO ⇒ ĐỎ đúng số).
   - Môi trường: venv `/home/user/FLS-tobe/.venv/bin/python`; `export PG_DSN='postgresql://fls:fls@localhost:5446/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5446/fls_test' PYTHONUTF8=1`; chạy từ thư mục worktree.
2. Đối chiếu TỪNG dòng mục 8 (Exit criteria) + từng test ID mục 6 với bằng chứng; Đ1 (câu phủ định phải grep cả `docs/` lẫn `fls/`+`tools/`), Đ3 (phép ra 0/100% phải có mẫu số), Đ4 (số có nhãn), Đ5 (cổng khai `mong`, đã chứng minh đỏ).
3. Tìm: lỗi, lệch spec, phạm vi lấn sang bước khác, refactor không do test đòi, tệp ngoài quyền làn (`TIEN_DO.md` §Quy ước · ISP §2.1), PII (Email Address, Diễn giải, Số chứng từ, tên người), bí mật.
3b. Phân loại mọi phát hiện kiểu `/process-issues`: lớp **A1** (lỗi mã, sửa trong bước) · **A2** (lỗi mã, lớp lỗi lặp — kèm LUẬT phòng tái phạm) · **B1** (lệch spec/thiếu bài) · **B2** (spec/ISP sai — chuyển orchestrator); mỗi hàng có một dòng *luật phòng tái phạm* cho các bước sau. Ghi vào sổ riêng `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT3.md` (tạo mới; đầu sổ khai luật: vòng sau chỉ đổi ô Trạng thái + thêm hàng). Khuyến nghị sửa phải cụ thể đủ để agent tác giả làm theo, ưu tiên kèm bài đề xuất đã chứng minh ĐỎ/XANH.
4. Viết phiếu **`docs/ITL/01_Orchestrator/handoff/KQ-108-kiem-dt3-r1.md`** theo `docs/ITL/01_Orchestrator/handoff/_mau/KQ.md`: mỗi tiêu chí `ĐẠT / TRƯỢT / ⛔ KHÔNG ĐO ĐƯỢC` + bằng chứng (lệnh, exit code, dòng tổng kết); mỗi phát hiện: mã, mức (CHẶN / NÊN SỬA / GHI NHẬN), tệp:dòng, khuyến nghị sửa cụ thể. Commit phiếu lên CHÍNH nhánh `isp/DT3` trong worktree ấy (chỉ thêm tệp phiếu + sổ phát hiện riêng), message kết thúc bằng:
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
   `Claude-Session: https://claude.ai/code/session_01Ci2qSNUDWhCHkgRnP5WyBL`

## Báo cáo cuối
- Kết luận một dòng: `ĐẠT` (0 phát hiện CHẶN) hoặc `TRƯỢT` + số phát hiện theo mức.
- Bảng phát hiện (mã · mức · tệp:dòng · khuyến nghị) — để agent tác giả sửa theo.
- Sha commit phiếu.

## Cụm PG của bạn
- Cổng **5446** (cụm reviewer riêng, đang chạy; kiểm `pg_isready -h localhost -p 5446`). ⛔ chạm cụm khác; ⛔ chạy pytest khi CHƯA export cả `PG_DSN` lẫn `PG_DSN_TEST` (bài học `S0-R3-05`: một phiên thiếu DSN rơi về mặc định 5433 và DROP kho test của làn khác). Cụm tắt ⇒ báo orchestrator, ⛔ tự `initdb`.
- Tệp nháp: `<SCRATCHPAD>/r1_dt3/` (tạo nếu chưa có).
- Chạy song song với 8 phiên khác — ⛔ `git checkout`/`git stash` ở checkout chính; ⛔ push.
