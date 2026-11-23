# Mẫu prompt phiên con — R2 cuối trên CÂY GỘP THỬ (Sonnet) — ví dụ thật: H11 · KQ-237

> Nguyên văn prompt `create_session` orchestrator đã dùng 19/11 (trích từ nhật ký phiên, đã soát: ⛔ PII · ⛔ khoá).
> Thay: mã bước · số phiếu · `## Step NN` · sha mong · cổng PG (mỗi phiên song song một cổng khác: 5434–5437, 5444–5447) · tên nhánh nếu tài khoản mới đổi tiền tố. Giữ nguyên các khối luật.

````text
Phiên cloud CON của orchestrator ISP 3.1.2 (repo kc-apero/FLS-tobe). Việc: **R2 CUỐI · Step 35 · H11 (+DT9b) · phiếu KQ-237**. Nhẹ: soát vòng sửa sau R1 (`KQ-236`) + **cây gộp thử** lên nhánh làm việc. GHI NHẬN ⇒ backlog. GỌN; tin nhắn cuối ≤ 15 dòng. Người dùng đã duyệt. Vai KIỂM: ⛔ sửa mã. Đọc `KQ-236`, mục "Vòng sửa sau R1 (KQ-236)" trong `BG-235`, sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H11.md`, `CLAUDE.md` (Đ1–Đ5).

Dựng (R = gốc repo; ⛔ `cd`):
```
git -C $R fetch origin 'refs/heads/claude/bold-galileo-zukpaf-isp/H11:refs/remotes/origin/moi/H11' claude/bold-galileo-zukpaf
git -C $R branch -f isp/H11 origin/moi/H11
grep -qx '.claude/worktrees/' $R/.git/info/exclude || echo '.claude/worktrees/' >> $R/.git/info/exclude
git -C $R worktree add -b thu/H11 $R/.claude/worktrees/thu-h11 origin/claude/bold-galileo-zukpaf
git -C $R/.claude/worktrees/thu-h11 merge --no-ff --no-edit isp/H11
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
env -C $R/.claude/worktrees/thu-h11 bash $R/.claude/worktrees/thu-h11/tools/dung_moi_truong_isp.sh --cong 5444
```
Sha mong `isp/H11` = d929b0d. Xung đột ⇒ ghi lại, gộp tay hợp lý (sàn = thu thập thật; `hd2_cong.json`/`do_hd2.py` giữ CẢ HAI; `07_API_CONTRACT` changelog giữ cả hai). LUÔN `export PG_DSN='postgresql://fls:fls@localhost:5444/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5444/fls_test' PYTHONUTF8=1`. Nạp IX.VEN mới (+ IX.PER) vào kho test.

Soát: (1) `H11-R1-01` đóng: luật theo sổ ghim bằng DỮ LIỆU tổng hợp — 5 đột biến R1 (khi bỏ bài dict) + 2 đột biến sống (`doc_ven(so="GI")`, bỏ nhánh `tt`) nay CHẾT; (2) `H11-R1-02` đóng: `/gates` `HD2_WP_C4C` hiện `khop` = ô khớp THẬT + `lech_co_chu_dich` 303 (SC 251 · OMC 52) + đếm ô rỗng; C4 cha (3 con) đúng; bài CG2 xanh; `hd2_cong.json` sinh bằng máy; (3) `-04` bài đường đọc kho CLI chạy; (4) đột biến ≥ 3 chỗ khác; (5) trên cây gộp thử: chạy lại `do_hd2.py --goi WP-C4a/C4b/C4c` (số không đổi) + `--duong-nen --cong 5444` MỘT lần (một mình) + `$R/.venv/bin/lint-imports` + `python docs/ITL/_tools/kiem_tai_lieu.py` + `python tools/soi_bang_tuyen.py`.

Ghi sổ H11 (THÊM hàng R2 + bump Version khớp changelog) + phiếu `docs/ITL/01_Orchestrator/handoff/KQ-237-kiem-h11-r2.md`. Commit lên `isp/H11` (chỉ 2 tệp; ⛔ commit cây gộp thử; worktree riêng trên `isp/H11`), trailer = hai dòng của chính phiên bạn. Push `push origin isp/H11:refs/heads/claude/bold-galileo-zukpaf-isp/H11` (fast-forward). ⛔ nhánh khác/force/PR/AskUserQuestion.

TIN NHẮN CUỐI ≤ 15 dòng: kết luận ĐẠT/TRƯỢT + số CHẶN·NÊN SỬA · đột biến R1 nay chết x/7 · /gates C4C · xung đột · tập đỏ · sàn · sha phiếu.
````
