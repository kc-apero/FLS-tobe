# Mẫu prompt phiên con — Bước DỮ LIỆU nhỏ mở khi engine thiếu đầu vào (Sonnet) — ví dụ thật: DT6c · WO-249

> Nguyên văn prompt `create_session` orchestrator đã dùng 19/11 (trích từ nhật ký phiên, đã soát: ⛔ PII · ⛔ khoá).
> Thay: mã bước · số phiếu · `## Step NN` · sha mong · cổng PG (mỗi phiên song song một cổng khác: 5434–5437, 5444–5447) · tên nhánh nếu tài khoản mới đổi tiền tố. Giữ nguyên các khối luật.

````text
Phiên cloud CON của orchestrator ISP 3.1.2 (repo kc-apero/FLS-tobe). Việc: **DT6c — ảnh ĐẦU VÀO HR 2025 + công thức CFA3 cho H7** theo phiếu `docs/ITL/01_Orchestrator/handoff/WO-249-isp-dt6c-dau-vao-hr-2025-cho-h7.md` (đọc TRỌN; thêm `BG-227` (DT6b — khuôn `hr_ledger_2024`), `BG-193`, `CLAUDE.md` Đ1–Đ5 + Riêng tư). Người dùng đã duyệt; ⛔ AskUserQuestion. GỌN; tin nhắn cuối ≤ 15 dòng.

Dựng (R = gốc repo; ⛔ `cd`):
```
git -C $R branch -f isp/DT6C HEAD
grep -qx '.claude/worktrees/' $R/.git/info/exclude || echo '.claude/worktrees/' >> $R/.git/info/exclude
git -C $R worktree add $R/.claude/worktrees/isp-dt6c isp/DT6C
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
env -C $R/.claude/worktrees/isp-dt6c bash $R/.claude/worktrees/isp-dt6c/tools/dung_moi_truong_isp.sh --cong 5436
```
Nền mong = `b8afd74` (hoặc mới hơn). LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5436/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5436/fls_test' PYTHONUTF8=1`.

Khoá SA CHỈ-ĐỌC (⛔ ghi/nhận xét lên file của chủ): env `FLS_GSHEETS_SA_JSON_B64`/`FLS_GSHEETS_SA_JSON`; `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`; `$R/.venv/bin/python -I` (thiếu `google-auth` ⇒ `pip install` vào venv phiên); tên tab có `/`·`|` ⇒ `urllib.parse.quote` cả vùng. ⛔⛔ PII (sổ HR): bản đồ cột bằng hàng tiêu đề TRƯỚC; chỉ đọc 9 cột của khuôn `hr_ledger_2024`; ⛔ `Số chứng từ` · `Diễn giải` · tên người · email · ID Payee; TK cá nhân che `R` như DT6b; ⛔ in giá trị số TK ra log/BG. Bản thô `/tmp` (chmod 600), xoá sau dùng, ⛔ commit.

TDD (ĐỎ trước). Mở rộng khuôn (⛔ chép); mọi ảnh cũ đúng từng byte. Q8: nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit. Cuối: `--duong-nen --cong 5436` MỘT lần (một mình; ĐỎ ⇒ sửa + chạy lại MỘT lần) + `$R/.venv/bin/lint-imports` + `python docs/ITL/_tools/kiem_tai_lieu.py`. Bàn giao `docs/ITL/01_Orchestrator/handoff/BG-250-…md` (nguồn tab + vùng; hàng/kỳ; đối chiếu `gl_hr_408` theo kỳ; 2.302 hàng có ngày ở nguồn?; công thức CFA3 + For PL Report nguyên văn). Commit ① mã + bài + ảnh; ② BG. Trailer = hai dòng của chính phiên bạn. Push `git -C $R/.claude/worktrees/isp-dt6c push origin isp/DT6C:refs/heads/claude/bold-galileo-zukpaf-isp/DT6C`. ⛔ nhánh khác/force/PR.

TIN NHẮN CUỐI ≤ 15 dòng: kết luận · hàng/kỳ · đối chiếu 408 · 2.302 hàng · công thức CFA3 (tóm tắt) · tập đỏ · sàn cũ → mới · sha.
````
