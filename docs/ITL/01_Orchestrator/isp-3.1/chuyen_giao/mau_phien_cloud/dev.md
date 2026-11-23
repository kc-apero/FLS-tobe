# Mẫu prompt phiên con — Dev bước thường (Sonnet 5.5 medium) — ví dụ thật: F5 · WO-253

> Nguyên văn prompt `create_session` orchestrator đã dùng 19/11 (trích từ nhật ký phiên, đã soát: ⛔ PII · ⛔ khoá).
> Thay: mã bước · số phiếu · `## Step NN` · sha mong · cổng PG (mỗi phiên song song một cổng khác: 5434–5437, 5444–5447) · tên nhánh nếu tài khoản mới đổi tiền tố. Giữ nguyên các khối luật.

````text
Phiên cloud CON của orchestrator ISP 3.1.2 (repo kc-apero/FLS-tobe). Việc: **Step 37 · F5 — SCR-F08 ký tháng tỷ giá (D1) có hộp xác nhận** theo phiếu `docs/ITL/01_Orchestrator/handoff/WO-253-isp-f5-ky-thang-ty-gia-f08.md` (đọc TRỌN; ISP mục `## Step 37`; `06_SCREEN_SPEC.md` §9; `BG-161` (F4) · `BG-213` (C7); `CLAUDE.md` Đ1–Đ5). Người dùng đã duyệt; ⛔ AskUserQuestion. GỌN; tin nhắn cuối ≤ 15 dòng.

Dựng (R = gốc repo; ⛔ `cd`):
```
git -C $R branch -f isp/F5 HEAD
grep -qx '.claude/worktrees/' $R/.git/info/exclude || echo '.claude/worktrees/' >> $R/.git/info/exclude
git -C $R worktree add $R/.claude/worktrees/isp-f5 isp/F5
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
env -C $R/.claude/worktrees/isp-f5 bash $R/.claude/worktrees/isp-f5/tools/dung_moi_truong_isp.sh --cong 5446
```
Nền mong = `7cc8d04` (hoặc mới hơn). LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5446/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5446/fls_test' PYTHONUTF8=1`. Playwright + Chromium có sẵn (`require('playwright')`/`python -m playwright` — ⛔ `playwright install`); khuôn bài headless theo bài F4 trong `tests/web/`.

TDD (ĐỎ trước). Dùng `hop_thoai.js` (⛔ dựng hộp mới); chữ lỗi qua `goi_cua.js`; ⛔ gửi `actor` trong thân; sau ký nút khoá + hiện 'đã ký · người ký · ngày'. Q8: nâng `MONG_PYTEST_TOAN_BO` + `MONG_PYTEST_WEB` (nếu thêm bài web) + bài ghim cùng commit. Cuối: `--duong-nen --cong 5446` MỘT lần (một mình; ĐỎ ⇒ sửa + chạy lại MỘT lần) + `$R/.venv/bin/lint-imports` + `python docs/ITL/_tools/kiem_tai_lieu.py` + `python tools/kiem_thuyet_minh.py`. Chụp 2 ảnh (trước/sau ký, deviceScaleFactor 1) vào BG làm bằng chứng (tệp ảnh ⛔ commit nếu > 300 KB — mô tả thay). Bàn giao `docs/ITL/01_Orchestrator/handoff/BG-254-…md`. Commit ① mã + bài; ② BG. Trailer = hai dòng của chính phiên bạn. Push `git -C $R/.claude/worktrees/isp-f5 push origin isp/F5:refs/heads/claude/bold-galileo-zukpaf-isp/F5`. ⛔ nhánh khác/force/PR.

TIN NHẮN CUỐI ≤ 15 dòng: kết luận · F5-F1/F2/F3 · mã lỗi có chữ · tập đỏ (toàn bộ + web) · sàn cũ → mới · sha.
````
