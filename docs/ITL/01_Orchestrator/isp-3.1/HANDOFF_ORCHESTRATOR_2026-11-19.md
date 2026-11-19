# HANDOFF — orchestrator ISP 3.1.2 · bàn giao sang tài khoản mới · 2026-11-19

> **Dành cho:** người hoặc phiên Claude Code ở tài khoản MỚI, tiếp quản vai **orchestrator** ISP 3.1.2 của dự án FLS.
> **Đọc theo thứ tự:** tệp này → `CLAUDE.md` (Đ1–Đ5 · Bẫy · Riêng tư) → `TIEN_DO.md` (cùng thư mục — nhật ký + quyết của chủ) → ISP `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` → mẫu prompt `chuyen_giao/mau_phien_cloud/`.
> Kế thừa `CHUYEN_GIAO_ACCOUNT_2026-11-17.md` (đợt chuyển account trước — §3 môi trường test, §7 Drive/SA, §10 bẫy vẫn đúng); tệp này **thay** nó ở mọi chỗ hai tệp khác nhau.
> **Lệnh của chủ (19/11 ~11:35 UTC):** sau lượt đang chạy ⇒ DỪNG toàn bộ agents, commit + push, ghi handoff. **Next action của tài khoản mới:** viết skill + setup 4 agents, setup trên **staging** và bắt đầu chạy test (§9).

---

## 0. Câu mở đầu để dán vào phiên mới

```
Bạn là orchestrator của ISP 3.1.2 dự án FLS (repo kc-apero/FLS-tobe). Đọc
docs/ITL/01_Orchestrator/isp-3.1/HANDOFF_ORCHESTRATOR_2026-11-19.md trên nhánh
claude/bold-galileo-zukpaf, làm §8 "Việc đầu tiên" rồi §9 "Next action".
Chạy tự động theo lượt, chỉ dừng khi cần quyết định của chủ hoặc bị chặn;
mọi câu hỏi kèm khuyến nghị. Trả lời chủ bằng tiếng Việt.
```

---

## 1. Tiến độ lúc dừng

**33/48 Step ISP đã gộp** vào nhánh làm việc `claude/bold-galileo-zukpaf` (đếm chỉ Step ISP; bước bổ sung ghi riêng — bài học "34/48" đếm lẫn, đã đính chính trong `TIEN_DO`).

| Nhóm | Đã gộp |
|---|---|
| Nền · cổng | S0 · CG1 · CG2 · FG |
| Config (BE-CF) | C1 · C4 · C5 · C6 · C7 · C8 · C9 · C11 · C12 |
| Engine (BE-HC) | H1 · H2 · H4 · H5 · H6 · H9 · H10 |
| Dữ liệu (DATA) | DT1a · DT1b (+ con DT1BT · DT1BM) · DT2 · DT3 · DT4 · DT5 · DT6 · DT8 · DT9 · DT10 |
| FE | F4 |
| Bổ sung ngoài ISP (đã gộp) | DT8b (khoá vendor MID3 + CFA1 GI) · DT6b (Y2024 HR + gán kỳ 2.302 hàng) · ITE (alias, lệch AS-IS có chủ đích) · PII (làm sạch số TK cá nhân, máy quét `tools/quet_pii_repo.py`) · O9 (BA đăng ký SCR-F08) |
| Đóng theo quyết chủ | H3 ("⛔ áp dụng ở mốc 18/11") |

**Đang dở lúc viết (nhánh đã push, chưa gộp)** — kết cục điền ở "Trạng thái cuối" cuối tệp:

| Bước | Nhánh `claude/bold-galileo-zukpaf-isp/…` · ngọn | Vòng kế |
|---|---|---|
| H11 (+ DT9b gộp sẵn) | `H11` · `d929b0d` | R2 cuối `KQ-237` (phiên `session_01EC3zCUjEZocYt2aMG9vZbf`) — ĐẠT 0 · 0 ⇒ gộp |
| H7 (+ DT6c gộp sẵn) | `H7` · `a6631c8` | R1 `KQ-247` (`session_01EC3zCV4UhMqYC3cx2zncm8`) ⇒ vòng sửa nếu có ⇒ R2 `KQ-248` |
| F5 | `F5` · `2366257` | R1 `KQ-255` (`session_01EC3zCVbTmxsXzzD4f8KNg2`) ⇒ R2 `KQ-256` |

**Còn lại (12 Step):** H8 · H12 · H13 · H14 · H15 · I1 · I2 · C13 · F7 · DT7 · DT11 · DT12 — cộng **bước KPI riêng** (chủ duyệt 19/11, chưa có WO). Đã đủ phụ thuộc ngay: **C13 · DT7 · DT11 · DT12 · KPI**; H8 chờ H7; F7 · H12 · H15 · H13 · I1 · H14 · I2 nối tiếp theo bảng phụ thuộc ISP §3.

---

## 2. Ngọn các nhánh bước lúc dừng (`claude/bold-galileo-zukpaf-isp/<ID>`)

C11 `4130fed` · C12 `c9224f3` · C4 `031d048` · C5 `90829c5` · C6 `b6eab8d` · C7 `c9f6e9a` · C8 `b532430` · C9 `62f5d7e` · CG1 `df09484` · CG2 `77b2af7` · DT10 `4d03494` · DT1B `bad486c` · DT1BM `017d70f` · DT1BT `2108027` · DT2 `d9606d9` · DT3 `d5a13cc` · DT4 `edf2f29` · DT5 `79cdd7d` · DT6 `b7887da` · DT6B `059d4e7` · DT6C `2ee5ee5` · DT8 `4aae70e` · DT8B `833a273` · DT9 `a3f5153` · DT9B `0b88ca2` · DTCF `67aa88f` · F4 `a17cbb2` · F5 `2366257` · FG `55be241` · H10 `c7e43cc` · H11 `d929b0d` · H2 `6ce257d` · H4 `4f0ba26` · H5 `207d434` · H6 `a6cfda3` · H7 `a6631c8` · H9 `734eb43` · ITE `b6d9d22` · O9 `96c2c18` · PII `71e06d4`.

Nhánh đã gộp để nguyên làm lịch sử (⛔ xoá).

---

## 3. Quyết của chủ — ⛔ hỏi lại (đầy đủ trong `TIEN_DO.md`, các hàng "Quyết của chủ")

| Ngày | Quyết |
|---|---|
| 16/11 | Duyệt AP v3.1.2 + ISP 3.1.2 (48 bước) + O1–O11 = A; 4 làn song song BE-CF · BE-HC · FE · DATA |
| 18/11 | Luật vận hành **A–E**: **A** dev/sửa/review = Sonnet 5.5 medium · **B** 2 vòng review (R1 đầy đủ + R2 cuối trên **cây gộp thử**; GHI NHẬN ⇒ backlog; NÊN SỬA sau R2 ⇒ 1 vòng sửa + R2b nhẹ) · **C** `--duong-nen` 1 lần cuối phiên · **D** ≤ **3** phiên song song · **E** tin nhắn cuối phiên con ≤ 15 dòng |
| 18/11 | Bước engine khó (H5 · H6 · H7 · H9–H14) = **Opus 5.5 medium** |
| 18/11 | DT1b: mốc nhãn mới 18/11 (xlsx cũ đã mất) |
| 19/11 | C12 · PL5 = COM hàng **`GAG`** |
| 19/11 | DT3 PII: làm sạch **bản hiện hành** (⛔ viết lại lịch sử git) · H3 đóng · **20 mã KPI ⇒ bước riêng** · C8 loại 8 hàng `CN` |
| 19/11 | ITE: phương án **A** — alias `ITE \| ITE Interest` → nút `ITE` (lệch AS-IS có chủ đích, khai ở `lech_co_chu_dich`) |
| 19/11 | DT6: Y2024 lấy từ file GỐC `H1000 Ledger (APERO-HR Allocate HD_FS1)` id `1YEyGxBYXaa6n4dX9_rWXoFn6NgJStTP2DKJd64ZAoD4` (chủ share SA quyền nhận xét — DÙNG CHỈ-ĐỌC); 2.302 hàng thiếu ngày ⇒ **kỳ của hàng có ngày liền trên** |
| 19/11 | C8: IX.ORG **chỉ giữ TK → LE**; CDT1 là thuộc tính từng giao dịch, chuẩn hoá qua `CDT Correct` (đã có ở `fls/cau_hinh/to_chuc.py`) |
| 19/11 | TK **pháp nhân** không cần che ("Những người được quyền access vào hệ thống này thì không có dữ liệu gì là nhạy cảm và cần che"). Luật `CLAUDE.md` hiện hành (`Email Address` cấm vào kho …) GIỮ tới khi chủ đổi |
| 19/11 | Chưa cần luồng FE demo / tuyến báo cáo sớm — "không cần, cứ tiếp tục chạy" theo thứ tự ISP |

**Câu hỏi còn mở cho chủ (không chặn):**
1. **DT6 `ky_suy`:** DT6c đo 1.125/2.302 hàng thiếu ngày khớp nội dung với ledger nguồn ghi **2025-10**, trong khi quy tắc "hàng trên" gán kỳ khác; 1.101 hàng không khớp. Bằng chứng yếu ⇒ GIỮ quyết chủ + khai lớp lệch riêng `ky_suy`. Hỏi: có đổi quyết gán kỳ không?
2. **412:** bản ở sổ CF khác `gl_406` — BA xác nhận 412 theo sổ nào (`BG-193`).
3. **C7 AC-4** ghi "bỏ qua `actor`" nhưng `07_API_CONTRACT` §1 ghi `400` ⇒ BA sửa chữ AC (`C7-R1-04`).
4. **O = Σ `pe` MID1** cho OMC · SC · PS (orchestrator chốt; CFA1 ba sổ ⇒ backlog) — chưa có duyệt riêng của chủ.

---

## 4. Setup — tài khoản mới cần gì

### 4.1 Repo · nhánh
| Mục | Giá trị |
|---|---|
| Repo | `kc-apero/FLS-tobe` |
| Nhánh làm việc (gộp) | `claude/bold-galileo-zukpaf` — ngọn có tệp này. Tài khoản mới được cấp nhánh khác ⇒ **tạo từ ngọn này**, ghi tên nhánh mới vào `TIEN_DO.md` |
| Nhánh bước | `<nhánh làm việc>-isp/<ID>` — phiên con chỉ push vào đúng nhánh bước của nó |
| ⛔ | PR · force push · `docker compose down` · push nhánh ngoài 2 dạng trên |
| Trailer commit | 2 dòng do hệ thống cấp cho TỪNG phiên (`Co-Authored-By` + `Claude-Session` của chính phiên đó); ⛔ ghi id model ở chỗ khác |

### 4.2 Môi trường cloud (environment của tài khoản mới)
| Mục | Cách |
|---|---|
| Model | orchestrator: Opus 5.5; phiên con theo luật A (§3) |
| Network | cần: GitHub · PyPI · `sheets.googleapis.com` · `oauth2.googleapis.com` · `www.googleapis.com` (Drive API) |
| Khoá SA (đọc Google Sheets/Drive) | biến môi trường **`FLS_GSHEETS_SA_JSON_B64`** (base64 của JSON) hoặc `FLS_GSHEETS_SA_JSON`, đặt ở *environment secrets*. ⛔ dán vào chat · ⛔ ghi tệp repo · ⛔ in log. SA đã được share: CF report · P&L report · ITL RAW/ADJUSTED (SA có quyền Editor ở `1r4Wem…` — vẫn dùng chỉ-đọc) · H1000 Ledger gốc · các sổ GI/OMC/SC/PS (67 sổ SA thấy — liệt kê bằng `sa_ds.py`) |
| CA bundle | `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt` (proxy của container) |
| Python đọc SA | `.venv/bin/python -I` (venv có `google-auth`; thiếu ⇒ `pip install google-auth requests`). Tên tab có `/` `\|` `[` ⇒ `urllib.parse.quote` cả vùng |
| Dữ liệu thô Drive | chỉ ở scratchpad hoặc `/tmp` (chmod 600), xoá sau dùng; ⛔ commit |
| PostgreSQL 16 | 9 cụm: `/home/user/fls-pg16` (5433 — cụm orchestrator) · `/home/user/fls-pg16-<N>` (5434–5437, 5444–5447 — mỗi phiên con một cụm). Dựng: `bash tools/dung_moi_truong_isp.sh --cong <N>` (chạy lại được) |
| Container khởi động lại | các cụm TẮT ⇒ chạy vòng bật lại (§4.3) TRƯỚC mọi pytest — bài pg đỏ "Connection refused" là môi trường, không phải lỗi mã |
| Biến luôn export | `PYTHONUTF8=1` · `PG_DSN='postgresql://fls:fls@localhost:<N>/fls'` · `PG_DSN_TEST='postgresql://fls:fls@localhost:<N>/fls_test'` |

### 4.3 Vòng bật lại PG (dán nguyên)
```bash
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
for d in /home/user/fls-pg16 /home/user/fls-pg16-*; do p=$(basename $d | sed 's/fls-pg16-\?//'); p=${p:-5433}
  if [ -f $d/postmaster.pid ]; then pid=$(head -1 $d/postmaster.pid); ps -o args= -p $pid 2>/dev/null | grep -q "$d" || rm -f $d/postmaster.pid; fi
  l=/var/run/postgresql/.s.PGSQL.$p.lock; if [ -f $l ]; then pid=$(head -1 $l); ps -o args= -p $pid 2>/dev/null | grep -q "$d" || rm -f $l /var/run/postgresql/.s.PGSQL.$p; fi
  runuser -u postgres -- /usr/lib/postgresql/16/bin/pg_ctl -D $d -l $d/pg_ctl.log -w -t 60 start >/dev/null 2>&1; echo -n "$p:$? "; done; echo
```
Mỗi cổng in `:0` là bật được.

### 4.4 Công cụ orchestrator
| Tệp | Dùng |
|---|---|
| `chuyen_giao/cong_cu/gop_so.py <repo> <ID> <v0.NN> <ngày> <sha>` | gộp sổ phát hiện riêng `SO_PHAT_HIEN_ISP-3.1_<ID>.md` vào sổ chung (bump version) |
| `chuyen_giao/cong_cu/sa_ds.py` · `sa_meta.py <id>` · `sa_lay.py` · `sa_cong_thuc.py <id> <vùng> <r0>` · `sa_quet_cong_thuc.py` | liệt kê sổ SA thấy · tab + lưới · lấy giá trị · công thức (chỉ-đọc) |
| `tools/dung_moi_truong_isp.sh --duong-nen --cong <N>` | cổng hồi quy: đòi `KẾT: ĐẠT` (tập đỏ nền = **28** node id · web **3**) |
| `tools/quet_pii_repo.py` | quét số TK cá nhân trên `git ls-files` (đọc cả ruột zip; tệp không đọc được ⇒ ĐỎ có tên) — 0 ⇒ ĐẠT |
| `docs/ITL/_tools/kiem_tai_lieu.py` · `tools/soi_bang_tuyen.py` · `.venv/bin/lint-imports` · `tools/kiem_thuyet_minh.py` | cổng giấy K1–K5 · tuyến ↔ SQL (46 tuyến) · 11 hợp đồng tầng · thuyết minh màn |
| `tools/do_hd2.py --goi <WP> --ghi` | sinh lại khối cổng ở `docs/ITL/_tools/hd2_cong.json` (⛔ sửa tay) |

Sàn số bài hiện hành: `MONG_PYTEST_TOAN_BO=4101` · `MONG_PYTEST_WEB=675` (dòng 420–421 `tools/dung_moi_truong_isp.sh`; bài ghim ở `tests/test_dung_moi_truong_isp.py`).

---

## 5. Vận hành — vòng lặp orchestrator (cách đã chạy 18–19/11)

### 5.1 Nhịp một lượt
1. Giao ≤ 3 phiên con: `create_session` với `source_url` repo · `source_revision` = nhánh làm việc · `model` theo luật A · `effort` medium · `tags` `isp-3.1.2` + vai · `prompt` từ mẫu §5.4.
2. Hẹn lượt kiểm sau **40 phút** bằng `send_later` (nội dung = việc lượt kế + id các phiên). Không poll ngắn.
3. Lượt kiểm: `list_sessions` (`children: true`) → với từng phiên xong: `list_events` (`kinds ["result"]`, `limit 100`) đọc tin cuối ≤ 15 dòng → nếu cần, đọc phiếu `BG`/`KQ` đã commit trên nhánh bước (`git fetch` + `git show`) → quyết theo bảng §5.2.
4. Ghi một hàng `TIEN_DO.md` (dấu `|` trong ô phải viết `\|` — dấu trần vỡ bảng, K3 đỏ), chạy `kiem_tai_lieu.py`, commit, push, hẹn lượt kế.
5. Phiên con DỪNG vì THIẾU ĐẦU VÀO ⇒ orchestrator đo nguồn (SA chỉ-đọc), chốt cách làm (hỏi chủ khi là quyết nghiệp vụ, kèm khuyến nghị), mở **bước dữ liệu nhỏ** (tiền lệ DT8b · DT9b · DT6b · DT6c), rồi `send_message` cho phiên tác giả (giữ ngữ cảnh, rẻ hơn phiên mới) bảo gộp nhánh dữ liệu và làm tiếp.
6. Phiên con đang chạy: ⛔ ngắt; chờ thêm 15–20 phút.

### 5.2 Vòng đời một bước + bảng quyết
`WO` (orchestrator viết `handoff/WO-<n>-…md`, commit trên nhánh làm việc) → **dev** (TDD, `--duong-nen` 1 lần, viết `BG-(n+1)`) → **R1** (`KQ-(n+2)`, sổ riêng, đầy đủ: tái đo độc lập · đột biến ≥ 6 trên bản sao `git archive` · Đ1–Đ5 · PII) → **R2 cuối** (`KQ-(n+3)`) trên **cây gộp thử** (worktree `thu/<ID>` gộp nhánh bước lên ngọn nhánh làm việc; ⛔ commit cây thử) → **orchestrator gộp** (§5.3).

| Kết quả về | Việc kế |
|---|---|
| dev xong, `--duong-nen` ĐẠT | R1 (phiên mới, `fls-test`, mẫu `r1.md`) |
| R1 ĐẠT 0 CHẶN · 0 NÊN SỬA | R2 cuối (`r2_cay_gop_thu.md`) |
| R1 có CHẶN/NÊN SỬA | phiên sửa (`sua.md`; thêm mục "Vòng sửa sau R1" vào BG) → R2 cuối |
| R2 ĐẠT 0 · 0 | gộp (§5.3) |
| R2 có NÊN SỬA | 1 vòng sửa + **R2b nhẹ** (chỉ soát phần sửa + cây gộp thử) |
| GHI NHẬN | vào backlog sổ phát hiện, ⛔ chặn |
| gộp đỏ ở `--duong-nen` | ⛔ push; `git reset --hard origin/<nhánh>` (chỉ bỏ commit chưa push); phiên sửa tích hợp trên nhánh bước |
| phiên dừng vì thiếu dữ liệu | §5.1 bước 5 |

Số phiếu: WO cấp dải 4 số `WO-n` · `BG-(n+1)` · `KQ-(n+2)` · `KQ-(n+3)`. **Số trống kế tiếp: 257.**

### 5.3 Thủ tục gộp (orchestrator, máy cục bộ, cụm 5433)
1. `git fetch origin refs/heads/claude/bold-galileo-zukpaf-isp/<ID>` · `git branch -f isp/<ID> FETCH_HEAD`
2. `git merge --no-ff --no-commit isp/<ID>`
3. Gỡ xung đột MÃ trước — giữ CẢ HAI khi hai bước thêm khối song song (`hd2_cong.json` · `do_hd2.py` · `cau_hinh_repo.py` · changelog `07_API_CONTRACT`)
4. `git checkout --ours tools/dung_moi_truong_isp.sh tests/test_dung_moi_truong_isp.py`
5. N = tổng các dòng `tests/…: n` của `pytest --collect-only -q` (máy cộng; chỉ đếm khi đã hết dấu xung đột)
6. Đặt `MONG_PYTEST_TOAN_BO=N` (dòng 420 script) + bài ghim `== ["N"]` + chú thích `+ \`isp/<ID>\` ⇒ **N**` (thêm `MONG_PYTEST_WEB` nếu số bài web đổi)
7. `python3 -I docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/gop_so.py /home/user/FLS-tobe <ID> v0.NN <ngày> <sha>`
8. Nếu bước mở tuyến/đổi hợp đồng: `07_API_CONTRACT.md` §4i lật ⬜ → ✅ + bump version + changelog
9. Bật PG (§4.3) · `kiem_tai_lieu.py` · `lint-imports` (11 kept) · `soi_bang_tuyen.py` · chạy bài liên quan
10. Commit ("Gộp isp/<ID> (…): R2 cuối KQ-… ĐẠT 0 · 0" + trailer) → `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5433` chạy NỀN (~25 phút) → chỉ push khi `KẾT: ĐẠT` (28 = 28 · web 3 = 3)
11. Hàng `TIEN_DO` → commit → push

### 5.4 Mẫu prompt phiên con
Ở `chuyen_giao/mau_phien_cloud/` (7 tệp — nguyên văn prompt đã chạy 19/11): `dev.md` · `dev_engine.md` · `du_lieu.md` · `r1.md` · `sua.md` · `r2_cay_gop_thu.md` · `nhan_tiep.md` (`send_message`). Đầu mỗi tệp ghi phần cần thay. Mẫu cũ hơn theo từng bước ở `chuyen_giao/brief/*.md` (ví dụ thật) và `chuyen_giao/khuon_review.md`.

### 5.5 Chi phí (đo bằng `get_session(<id>).external_metadata.usage.cost_usd`)
- Sonnet 5.5 medium: review ≈ 0,5–1,7 USD · dev/sửa ≈ 0,5–3 USD · bước dữ liệu ≈ 1,5–3 USD.
- Opus 5.5 medium (engine, cả phiên kể nhắn tiếp): H9 ≈ 2,1 · H10 ≈ 4,9 · H11 ≈ 6,7 · H7 ≈ 7,8 USD.
- 19/11: giới hạn dùng **7 ngày** đã ở mức `allowed_warning` — tài khoản mới theo dõi `rate_limit_info` trong `get_session`.

---

## 6. Bài học / bẫy mới 18–19/11 (cộng thêm vào §10 của `CHUYEN_GIAO_ACCOUNT_2026-11-17.md`)

| Bẫy | Cách chặn |
|---|---|
| **Hợp đồng khối cổng HD2**: gói mới (`WP-C4a` của H9 · `WP-C4b` của H10) thiếu `tong_o`/`khop` ⇒ `/gates` trả `null` + bài CG2 ĐỎ khi gộp (cắn 2 lần) | mọi WO engine ghi rõ: khối `hd2_cong.json` theo hợp đồng CG2 (`tong_o`/`khop` = ô khớp THẬT; lệch có chủ đích ở `lech_co_chu_dich` + `mong_lech_co_chu_dich`), sinh bằng `do_hd2.py --ghi`; bài đọc tập cổng TỪ TỆP (⛔ ghim cứng số cổng); R2 luôn chạy trên cây gộp thử |
| `khop` cộng cả lệch có chủ đích ⇒ `/gates` giấu lệch (ITE) | mỗi số một nghĩa (Đ4); trường riêng `lech_co_chu_dich` |
| Phiên engine thiếu ảnh đầu vào ⇒ dễ lấy đáp án làm đầu vào (vòng tròn) | luật WO: thiếu đầu vào ⇒ DỪNG báo ảnh cần thêm; orchestrator mở bước DATA nhỏ |
| Tập toàn 0 (vendor thường GI · PE của PS) | Đ3: khai là KẾT QUẢ; phép so ô ≠ 0 chuyển sang bước có số thật |
| AP/ISP ghi sai dữ liệu ("PS thiếu 7 tháng 2026", "4 × 8 driver", "IX.ORG TK → CDT1") | đo trước, khai `mong` theo dữ liệu, gom errata v3.1.3 (§7) |
| Máy quét PII bỏ qua im lặng tệp không giải mã được (37 số TK trong zip) | máy quét đếm "tệp đã đọc"; tệp không đọc được ⇒ ĐỎ có tên |
| PG tắt sau khi container khởi động lại ⇒ bài `/gates` đỏ giả | vòng bật lại §4.3 trước mọi pytest |
| Sàn số bài ở nhánh bước lệch cây gộp (2–9 bài) | luôn đặt sàn = thu thập thật của CÂY GỘP, sau khi gỡ xung đột |
| Đếm "x/48" lẫn bước bổ sung | chỉ đếm Step ISP |
| Orchestrator/phiên con lỡ in giá trị nhạy cảm ra đầu ra công cụ khi dò tiêu đề sheet | dò tiêu đề chỉ in **tên cột** của hàng tiêu đề đã biết; dữ liệu chỉ ĐẾM, ⛔ in giá trị; ⛔ in số TK dù vài chữ số |

---

## 7. Errata gom cho ISP/AP v3.1.3 (nối tiếp ①–㉓ ở tệp chuyển giao 17/11)
㉔ Step 23 (DT6) tiêu đề: 412 · 413 là GL, CFA3 Daily thuộc PD 411 · ㉕ Step 22 (C8) đổi tên: "IX.ORG: TK → LE; CDT1 theo giao dịch qua CDT Correct" · ㉖ Step 27 (DT10): driver đo được 3/4 loại × 7/8 CDT1 (NB khoá theo LE; CMN gộp SHQ1) · ㉗ Step 34 DT9-B1 + AP §3.4.1: ba sổ OMC · SC · PS chỉ có tháng 2025, không có tháng 2026 nào · ㉘ Step 35 (H11): kỳ không có đáp án ⇒ `chua_co_dap_an` theo dữ liệu · ㉙ C12 PL5 = PL4 − COM `GAG` (tab `[2025][RPT] NOEM PL & COM` hàng 18) · ㉚ hợp đồng khối HD2 (`tong_o`/`khop`/`lech_co_chu_dich`) vào AP §3.5.4.

---

## 8. Việc đầu tiên của tài khoản mới
1. Đọc §1–§7; tạo nhánh làm việc mới từ ngọn `claude/bold-galileo-zukpaf` (nếu được cấp tên khác); ghi tên vào `TIEN_DO.md`.
2. Kiểm môi trường (§4.2): có PG16 không; dựng cụm bằng `dung_moi_truong_isp.sh --cong 5433`; venv; khoá SA (kiểm biến có mặt bằng `test -n` — ⛔ in; đọc thử một ô công khai không nhạy cảm, ví dụ tab tỉ giá sổ P&L).
3. Chạy `--duong-nen --cong 5433` trên ngọn ⇒ đòi `KẾT: ĐẠT` 28 = 28 · web 3 = 3.
4. Xử lý nhánh còn treo theo "Trạng thái cuối": đọc phiếu R1/R2 đã commit trên nhánh (`KQ-237` · `KQ-247` · `KQ-255`) ⇒ sửa / R2 / gộp theo §5.
5. Rồi §9.

---

## 9. Next action (chủ giao 19/11): viết skill + setup 4 agents · setup staging · chạy test

### 9.1 Skill — khuyến nghị
Đặt ở `.claude/skills/` (repo chưa có thư mục này — `ls -a .claude/` lúc viết ra 4 mục: `agents/` · `hooks/` · `settings.json` · `worktrees/`). Ba skill:

| Skill | Nội dung | Nguồn lấy |
|---|---|---|
| `isp-orchestrator` | vòng lượt §5.1 + bảng quyết §5.2 + luật A–E + mẫu prompt (tài nguyên) | tệp này §5 + `chuyen_giao/mau_phien_cloud/` |
| `isp-gop-buoc` | thủ tục gộp §5.3 — khuyến nghị viết thêm script `tools/gop_buoc_isp.sh <ID> <ngày>` tự làm bước 1–2, 4–7, 9 (bước 3 · 8 · 10 cần mắt người) | §5.3 + `gop_so.py` |
| `fls-moi-truong` | dựng/bật lại PG, export DSN, khoá SA chỉ-đọc, `--duong-nen` | §4 |

Dùng skill `skill-creator` để viết và đo (eval) từng skill; mô tả kích hoạt bằng tiếng Việt khớp cách chủ nói ("gộp bước", "lượt kiểm", "giao phiên").

### 9.2 Bốn agent — khuyến nghị
Quyết 16/11: 4 làn BE-CF · BE-HC · FE · DATA. Repo có sẵn 3 định nghĩa `.claude/agents/` (`fls-ba` · `fls-dev` · `fls-test`) giao tiếp qua phiếu. Cách ghép đề xuất:

| Agent | Vai | Model | Ghi chú |
|---|---|---|---|
| `fls-orchestrator` (mới) | giao việc, gộp, hỏi chủ | Opus 5.5 | dùng skill `isp-orchestrator` + `isp-gop-buoc`; ⛔ viết mã bước |
| `fls-dev` (làn qua tham số WO: CF · HC · FE · DATA) | dev + sửa | Sonnet 5.5 medium; làn HC = Opus 5.5 medium | giữ một định nghĩa, làn đọc từ WO — tránh 4 tệp trùng lặp |
| `fls-test` | R1 / R2 / R2b | Sonnet 5.5 medium | ⛔ sửa mã; tái đo độc lập; cây gộp thử |
| `fls-ba` | WO · TL · nghiệm thu PO · errata v3.1.3 | Sonnet 5.5 medium | trả 3 câu hỏi §3 mục 2–3 |

Nếu chủ muốn đúng 4 agent theo **làn** thay vì theo vai: `fls-dev-cf` · `fls-dev-hc` · `fls-dev-fe` · `fls-dev-data`, mỗi tệp kế thừa `fls-dev.md` + quyền tệp theo ISP §2.1 — cần hỏi chủ chọn cách nào (khuyến nghị cách theo **vai** ở bảng trên, vì luật review 2 vòng cần agent test độc lập).

### 9.3 Staging — cần chốt với chủ trước khi dựng (orchestrator cũ không có thông tin này)
- **Staging là gì:** máy/kho nào (PostgreSQL riêng, container, URL)? Ai truy cập? Đây là kho có dữ liệu thật ⇒ luật riêng tư `CLAUDE.md` áp dụng.
- **Kho:** `python -m fls.db.pg_migrate` (tự chạy `pg_verify`); `fls_itl` chỉ-THÊM (`INV-I08`); công cụ ghi sổ đòi `FLS_CHO_GHI_THAT=1` — chỉ bật ở kho staging.
- **Cửa API:** `PG_DSN=… FLS_JWT_SECRET=… python tools/chay_cua.py --cong 8088` (cửa tự từ chối nếu thiếu `FLS_JWT_SECRET`). Bí mật đặt ở biến môi trường, ⛔ repo/chat.
- **Dữ liệu:** nạp qua F04 (`/nap` · `/nap/lo`) hoặc công cụ; IX.* nạp vào kho config (C5) từ ảnh đóng băng.
- **"Chạy test" trên staging:** (a) `python -m pytest` toàn bộ với `PG_DSN` staging (khai trước tập đỏ nền — Đ5); (b) cổng HD2 `do_hd2.py --goi …` so số máy ↔ sổ AS-IS; (c) luồng FE F04 → F02 → F01 → F03 → F08 bằng Playwright.
- ⛔ `docker compose down` (kho trên volume vô danh); ⛔ `Client secret` qua chat/repo.

---

## Trạng thái cuối *(lượt cuối 19/11 điền)*

_(đang chờ lượt cuối)_
