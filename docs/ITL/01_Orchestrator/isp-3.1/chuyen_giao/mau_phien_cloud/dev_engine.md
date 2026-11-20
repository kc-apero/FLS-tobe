# Mẫu prompt phiên con — Dev bước engine khó (Opus 5.5 medium) — ví dụ thật: H7 · WO-245

> Nguyên văn prompt `create_session` orchestrator đã dùng 19/11 (trích từ nhật ký phiên, đã soát: ⛔ PII · ⛔ khoá).
> Thay: mã bước · số phiếu · `## Step NN` · sha mong · cổng PG (mỗi phiên song song một cổng khác: 5434–5437, 5444–5447) · tên nhánh nếu tài khoản mới đổi tiền tố. Giữ nguyên các khối luật.

````text
Phiên cloud CON của orchestrator ISP 3.1.2 (repo kc-apero/FLS-tobe). Việc: **Step 32 · H7 — CA.GL dòng HR + SO.CFA3, cổng WP-C3c** theo phiếu `docs/ITL/01_Orchestrator/handoff/WO-245-isp-h7-ca-gl-hr-cfa3.md` (đọc TRỌN — mục "Đã đo" THAY chữ ISP; ISP mục `## Step 32`; `BG-165` (H5) · `BG-189` (H6) · `BG-193` + `BG-227` (DT6/DT6b) · `BG-209` + `BG-230` (hợp đồng cổng CG2 + `lech_co_chu_dich`); `CLAUDE.md` Đ1–Đ5). Người dùng đã duyệt; ⛔ AskUserQuestion. GỌN, tiết kiệm token; tin nhắn cuối ≤ 15 dòng.

Dựng (R = gốc repo; ⛔ `cd`):
```
git -C $R branch -f isp/H7 HEAD
grep -qx '.claude/worktrees/' $R/.git/info/exclude || echo '.claude/worktrees/' >> $R/.git/info/exclude
git -C $R worktree add $R/.claude/worktrees/isp-h7 isp/H7
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
env -C $R/.claude/worktrees/isp-h7 bash $R/.claude/worktrees/isp-h7/tools/dung_moi_truong_isp.sh --cong 5435
```
Nền mong = `b584561` (hoặc mới hơn). LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5435/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5435/fls_test' PYTHONUTF8=1`. Cổng HD2 đọc IX.PER qua `PG_DSN` ⇒ nạp IX.PER (+ IX.ORG) vào kho test và chạy với `PG_DSN=$PG_DSN_TEST`.

TDD (ĐỎ trước). ⛔ vòng tròn: đầu vào HR là ảnh THƯỢNG NGUỒN (như `gl_cf_dau_vao` của H5) — nếu chưa có ảnh đầu vào HR riêng ⇒ DỪNG, báo cần ảnh nào (tab + vùng + vì sao) + khuyến nghị, ⛔ đọc đáp án làm đầu vào. Dùng lại engine H4/H5/H6 (⛔ chép). CDT qua `cdt_cua` (lạ ⇒ lỗi có tên, ⛔ SHQ2). Mẫu số WP-C3c khai TRƯỚC kèm nhãn Đ4; khối `hd2_cong.json` theo hợp đồng CG2 (`khop` = ô khớp THẬT), sinh bằng `do_hd2.py --ghi`; bài quét tệp thật CG2 + `tests/api/test_isp_gates_hd2.py` xanh. Q8: nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit. Cuối: `--duong-nen --cong 5435` MỘT lần (một mình; ĐỎ ⇒ sửa + chạy lại MỘT lần) + `$R/.venv/bin/lint-imports` + `python docs/ITL/_tools/kiem_tai_lieu.py`. Bàn giao `docs/ITL/01_Orchestrator/handoff/BG-246-…md`. Commit ① mã + bài + tệp sinh lại; ② BG. Trailer = hai dòng của chính phiên bạn. Push `git -C $R/.claude/worktrees/isp-h7 push origin isp/H7:refs/heads/claude/bold-galileo-zukpaf-isp/H7`. ⛔ nhánh khác/force/PR.

TIN NHẮN CUỐI ≤ 15 dòng: kết luận · nguồn đầu vào HR · WP-C3c (GL HR · CFA3: ô so · ô ≠ 0 · lệch có tên) · hàng ky_suy xử lý · /gates C3C · tập đỏ · sàn cũ → mới · sha.
````
