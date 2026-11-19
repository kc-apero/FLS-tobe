# Mẫu prompt phiên con — Vòng sửa sau R1 (Sonnet) — ví dụ thật: H11 · KQ-236

> Nguyên văn prompt `create_session` orchestrator đã dùng 19/11 (trích từ nhật ký phiên, đã soát: ⛔ PII · ⛔ khoá).
> Thay: mã bước · số phiếu · `## Step NN` · sha mong · cổng PG (mỗi phiên song song một cổng khác: 5434–5437, 5444–5447) · tên nhánh nếu tài khoản mới đổi tiền tố. Giữ nguyên các khối luật.

````text
Phiên cloud CON của orchestrator ISP 3.1.2 (repo kc-apero/FLS-tobe). Việc NHỎ: **vòng sửa sau R1 của Step 35 · H11 (+DT9b)**. R1 = `KQ-236`: 0 CHẶN · 2 NÊN SỬA · 4 GHI NHẬN. Người dùng đã duyệt. GỌN; tin nhắn cuối ≤ 15 dòng. Đọc `KQ-236` + sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H11.md`, `BG-235`, `BG-230` (hợp đồng `/gates` + `lech_co_chu_dich`), `CLAUDE.md` (Đ1–Đ5).

Dựng (R = gốc repo; ⛔ `cd`):
```
git -C $R fetch origin 'refs/heads/claude/bold-galileo-zukpaf-isp/H11:refs/remotes/origin/moi/H11' claude/bold-galileo-zukpaf
git -C $R branch -f isp/H11 origin/moi/H11
grep -qx '.claude/worktrees/' $R/.git/info/exclude || echo '.claude/worktrees/' >> $R/.git/info/exclude
git -C $R worktree add $R/.claude/worktrees/isp-h11 isp/H11
git -C $R/.claude/worktrees/isp-h11 merge --no-ff --no-edit origin/claude/bold-galileo-zukpaf
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
env -C $R/.claude/worktrees/isp-h11 bash $R/.claude/worktrees/isp-h11/tools/dung_moi_truong_isp.sh --cong 5444
```
Sha mong `isp/H11` = a6e09fc. Xung đột khi gộp nhánh làm việc: sàn ⇒ bản nhánh làm việc + đặt = thu thập thật; `hd2_cong.json`/`do_hd2.py` giữ CẢ HAI; `07_API_CONTRACT` changelog giữ cả hai. LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5444/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5444/fls_test' PYTHONUTF8=1`. Nạp IX.VEN mới vào kho test.

Việc (mỗi mục ĐỎ trước bằng đúng đột biến R1, chạy trên bản sao — ghi vào BG):
1. **`H11-R1-01`:** luật theo sổ được ghim bằng DỮ LIỆU tổng hợp (⛔ chỉ bài ghim dict `LUAT_SO`): ca O = 0 ∧ P > 0 · ca `VD62` mượn `VD341` ở SC/PS (cột `$AU`) vs OMC (`$H`, ⛔ mượn) — 5 đột biến R1 sống khi bỏ bài dict phải ĐỎ. Thêm bài giết 2 đột biến sống: `doc_ven(so="GI")` trong `chay_wp_c4c` và bỏ nhánh `tt` của engine.
2. **`H11-R1-02`:** khối `WP-C4c`: `khop` = ô khớp THẬT (19.591 − ?) — 303 ô lệch nguồn (SC 251 · OMC 52) khai `lech_co_chu_dich` + `mong_lech_co_chu_dich` theo hợp đồng ITE (đã gộp) ⇒ `/gates` `HD2_WP_C4C` hiện số lệch; nhãn ⛔ nói "19591/19591 khớp" khi có 303 lệch ngoài + 8.611 ô rỗng — thêm đếm ô rỗng vào khối (Đ4). Sinh lại bằng `do_hd2.py --ghi` (⛔ sửa tay). Bài CG2 xanh.
3. Làm kèm (rẻ): `-04` một bài chạy đường đọc kho của CLI. `-03`, `DT9B-R1-01/02` ⇒ backlog.
- TDD. Q8: sàn = thu thập thật + bài ghim cùng commit. Cuối: `--duong-nen --cong 5444` (một mình; ĐỎ ⇒ sửa + chạy lại MỘT lần) + `$R/.venv/bin/lint-imports` + `python tools/soi_bang_tuyen.py`.
- Thêm mục "Vòng sửa sau R1 (KQ-236)" vào `BG-235` (chỉ THÊM). Commit (merge + ① mã/bài/tệp sinh lại; ② BG). Trailer = hai dòng của chính phiên bạn. Push `git -C $R/.claude/worktrees/isp-h11 push origin isp/H11:refs/heads/claude/bold-galileo-zukpaf-isp/H11` (fast-forward). ⛔ nhánh khác/force/PR/AskUserQuestion.

TIN NHẮN CUỐI ≤ 15 dòng: kết luận · đột biến R1 nay chết x/7 · /gates C4C (khop · tong_o · lech_co_chu_dich · ô rỗng) · tập đỏ · sàn · sha.
````
