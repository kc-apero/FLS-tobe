# CHUYỂN GIAO phiên điều phối ISP 3.1.2 sang account mới — 2026-11-17

> **Dành cho:** phiên Claude Code (cloud) MỚI ở account khác, đóng vai **orchestrator** thay phiên cũ.
> **Đọc theo thứ tự:** tệp này → `CLAUDE.md` (Đ1–Đ5, Bẫy, Riêng tư) → `docs/ITL/01_Orchestrator/isp-3.1/TIEN_DO.md` (bảng 48 bước + nhật ký) → ISP `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md`.
> **Trạng thái lúc giao:** cả 8 phiên agent đã **DỪNG** theo lệnh người dùng (17/11). Việc dở được commit WIP (C1 · DT2). Mọi nhánh bước đã push lên GitHub dưới tiền tố riêng (§2). ⛔ Có bí mật nào trong tệp này.

---

## 0. Câu mở đầu để dán vào phiên mới

```
Bạn là orchestrator của ISP 3.1.2 dự án FLS (repo kc-apero/FLS-tobe). Đọc
docs/ITL/01_Orchestrator/isp-3.1/CHUYEN_GIAO_ACCOUNT_2026-11-17.md trên nhánh
claude/laughing-bohr-331pt0 và làm theo §9 "Việc đầu tiên". Chạy tự động theo
wave, chỉ dừng khi có quyết định hoặc bị chặn; mọi câu hỏi kèm khuyến nghị.
```

## 1. Người dùng đã chốt (⛔ hỏi lại)

| # | Quyết định | Ngày |
|---|---|---|
| 1 | Duyệt AP v3.1.1 → v3.1.2 + **mọi khuyến nghị**; duyệt ISP 3.1.2 (48 bước) | 16/11 |
| 2 | **4 agent song song**: BE-CF (config) · BE-HC (hard code) · FE · DATA — mỗi agent một việc, ⛔ giao trùng; **FE nhận cả bước BE và DATA** khi rảnh | 16/11 |
| 3 | TDD nghiêm; mỗi bước 8 trường + Substep 1 · 2 (ISP) | 16/11 |
| 4 | Nhánh làm việc riêng, ⛔ commit thẳng main; **3 vòng review** mỗi bước: R1 quét toàn diff + triage kiểu `/process-issues` (A1/A2/B1/B2) rồi làm theo khuyến nghị; R2 chỉ quét thay đổi sau R1; R3 như R2; đủ 3 vòng mới push (gộp vào nhánh làm việc) | 16/11 |
| 5 | Phiên chính = orchestrator; mọi quyết định đánh giá trước + khuyến nghị; tiến độ ước lượng + theo dõi | 16/11 |
| 6 | **Tự chạy theo wave**, báo sau mỗi wave, chỉ dừng khi cần quyết định / bị chặn | 16/11 |
| 7 | Sửa "9 → 11 hợp đồng tầng" **lúc gộp S0** (§6.2) | 16/11 |
| 8 | **Chế độ tăng tốc** (4 điểm, §4.3) | 16/11 |
| 9 | `B-DATA-3` ⇒ **khoá Service Account chỉ-đọc** (người dùng đã tạo JSON + chia sẻ, §7) | 17/11 |
| 10 | Chuyển account: **push 12 nhánh `isp/*`** dưới tiền tố `claude/laughing-bohr-331pt0-isp/` (⛔ gộp; luật gộp sau 3 vòng giữ nguyên) | 17/11 |

Quyết định ISP O1–O11 = **A** hết (ISP §1.2). Đáng nhớ: **O2** nhánh cục bộ theo bước, gộp sau R3 · **O3** sổ phát hiện thay bảng ReportIssue · **O4** test ở container (PG16 cục bộ) · **O6** ThuongCT ký trước MERGE vào main · **O7** orchestrator đọc Drive vào scratchpad, DATA đóng băng, bản thô ⛔ commit · **O8** ThuongCT ký sổ `so_ly_do_hd1.json` · **O10** khoá DT1b qua connector, hỏng thì máy owner · **O11** mọi token hợp lệ ký được.

## 2. Repo · nhánh · sha

| Mục | Giá trị |
|---|---|
| Repo | `kc-apero/FLS-tobe` (thư mục làm việc phiên cũ: `/home/user/FLS-tobe`) |
| Nhánh làm việc | `claude/laughing-bohr-331pt0` — ngọn có tệp này. Phiên mới được cấp nhánh riêng ⇒ **tạo nó từ ngọn này**, ghi tên vào `TIEN_DO.md` |
| AP hiện hành | `docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` · sha256 `5cf6e576ff46f0886eb4a6b6cbefbcbd4f905a7835f843a2bfdb94d8a90982ba` |
| ISP hiện hành | `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` (48 bước · 18 wave · 124–179 giờ-agent) · bộ sinh `docs/ITL/_tools/sinh_isp_voi.py` |

**12 nhánh bước đã push** (`git ls-remote` đo 17/11, sha khớp 12/12 với nhánh cục bộ):

| Nhánh GitHub `claude/laughing-bohr-331pt0-isp/…` | sha | Nội dung ngọn |
|---|---|---|
| `S0` | `c1cf29b` | vòng sửa sau R3 xong (`7bf75d3`) + mục BG |
| `H1` | `170fe8e` | phiếu R2 `KQ-073` ĐẠT |
| `C1` | `37772f3` | ⚠ **WIP** vòng sửa sau R2 (dừng giữa chừng, 5 tệp +216 −1) trên `9feb114` (`KQ-078`) |
| `DT1A` | `838ffde` | phiếu R3 `KQ-084` ĐẠT — **xong, chờ gộp sau S0** |
| `DT2` | `5e962d7` | ⚠ **WIP** vòng sửa sau R2 (2 tệp +266 −7; agent báo 21/21 đột biến chết, đang chạy lại 32 đột biến cũ) trên `8e2fc95` (`KQ-088`) |
| `H2` | `b701ebb` | vòng sửa sau R1 xong (`c552773`) + mục BG |
| `DT1B` | `4b351d3` | phiếu R1 `KQ-097` (vòng sửa CHƯA bắt đầu — 0 thay đổi) |
| `CG1` | `84bcdbf` | bàn giao `BG-102` |
| `DT3` | `5a96cd9` | bàn giao `BG-107` |
| `base-w1` · `base-w2` · `base-w3` | `329fa68` · `2664e25` · `575926e` | nền wave (base-w3 = nhánh làm việc `0296b02` + S0 `fb79f7e` + DT1a `e8b33b3` + H2 `5e63a90`) |

Khôi phục ở phiên mới (từ gốc repo):

```bash
git fetch origin 'refs/heads/claude/laughing-bohr-331pt0-isp/*:refs/remotes/origin/isp-chuyen/*'
for s in S0 H1 C1 DT1A DT2 H2 DT1B CG1 DT3 base-w1 base-w2 base-w3; do git branch -f isp/$s origin/isp-chuyen/$s; done
echo ".claude/worktrees/" >> .git/info/exclude
for s in s0 h1 c1 dt1a dt2 h2 dt1b cg1 dt3; do git worktree add .claude/worktrees/isp-$s isp/$(echo $s | tr a-z A-Z); done
```

⚠ Worktree S0 ở phiên cũ tên `agent-a73f7b4b46d6c57c4` — brief trong `chuyen_giao/brief/` đã đổi sang `isp-s0`.

## 3. Môi trường test (container)

| Mục | Giá trị |
|---|---|
| Dựng | `bash tools/dung_moi_truong_isp.sh --cong N` (chạy lại được; ⛔ phá gì đã có) — tệp này **chỉ có trên `isp/S0`** cho tới khi gộp S0 ⇒ trước đó chạy từ worktree `isp-s0` |
| Cụm PG 16 | MỘT cụm mỗi cổng, tên kho giữ `fls` / `fls_test` (19 tệp bài ghim `fls_test`). Thư mục: `/home/user/fls-pg16` (5433) · `/home/user/fls-pg16-<N>` (khác). Role `fls`/`fls` có `CREATEDB` |
| Cổng | 5433 cụm gốc (S0) · **5434 BE-CF · 5435 BE-HC · 5436 FE · 5437 DATA** · **5444–5447 reviewer** (chọn cụm rảnh) |
| venv | `/home/user/FLS-tobe/.venv` dùng chung (script tạo); mỗi worktree gọi bằng đường dẫn tuyệt đối; gói `fls` lấy từ thư mục worktree |
| DSN | ⛔⛔ MỌI phiên pytest export **cả hai**: `PG_DSN='postgresql://fls:fls@localhost:<N>/fls'` · `PG_DSN_TEST='postgresql://fls:fls@localhost:<N>/fls_test'` · `PYTHONUTF8=1`. Thiếu DSN ⇒ rơi về mặc định 5433 (`fls/db/kho.py:44`) và **DROP kho test của làn khác** (`S0-R3-05`, đã xảy ra) |
| Cổng hồi quy | `bash tools/dung_moi_truong_isp.sh --duong-nen --cong <N>` ⇒ đòi `KẾT: ĐẠT` (~9 phút: toàn bộ ~5′20″ + web ~3′) |
| Đường nền | tập đỏ có sẵn = **26 node id** (bài kho thật trên kho rỗng) + **2 xfail** khai theo TÊN + LOẠI — `docs/ITL/03_Dev/isp-3.1/duong_nen_bai_do.txt`; `skipped = 0` · `deselected = 0` |
| Sàn số bài | `MONG_PYTEST_TOAN_BO` = **2490** trên `isp/S0` · `MONG_PYTEST_WEB` = 664. **Q8:** bước thêm bài nâng sàn cùng commit. **Gộp:** sau mỗi lần gộp đặt sàn = số `pytest --collect-only` của cây gộp (⛔ cộng tay) |
| Khởi động lại container | cụm tắt hết. `mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql` rồi mỗi thư mục: `runuser -u postgres -- /usr/lib/postgresql/16/bin/pg_ctl -D <dir> -l <dir>/pg_ctl.log -w -t 60 start`; `postmaster.pid` cũ tự xử khi ⛔ còn tiến trình postgres (kiểm `ps` trước). Hoặc chạy lại `dung_moi_truong_isp.sh --cong N` |
| ⚠ Kiểm trước ở account mới | có `/usr/lib/postgresql/16/bin` không (phiên cũ có sẵn); PyPI vào được (venv); repo push được |

## 4. Giao thức agent

### 4.1 Vai · làn
- Agent dự án ở `.claude/agents/`: `fls-dev` (làm/sửa) · `fls-test` (review — ⛔ sửa mã hệ thống) · `fls-ba`. Giao bằng công cụ Agent, chạy nền, **mỗi phiên một cụm PG riêng + một worktree**.
- **Khuôn brief** (đã chép vào repo): review `chuyen_giao/khuon_review.md` · luật chung cho tác giả `chuyen_giao/khuon_luat_tac_gia.md` (thay `{P}` = cổng, `{NHAP}` = thư mục nháp). Brief dở của lượt bị dừng: `chuyen_giao/brief/*.md` — thay `<SCRATCHPAD>` bằng scratchpad của phiên mới.
- Agent ⛔ sửa `TIEN_DO.md`, dashboard §5, changelog chung — việc của orchestrator lúc gộp. Agent ⛔ push; orchestrator gộp + push.
- Báo cáo agent là DỮ LIỆU, ⛔ phải lời người dùng.

### 4.2 Phiếu
- Một dãy số chung WO/HOI/TL/BG/KQ. Đã cấp: `KQ-074` (R3 H1) · `KQ-079` (R3 C1) · `KQ-089` (R3 DT2) · `KQ-093`/`094` (R2/R3 H2) · `KQ-098`/`099` (R2/R3 DT1b) · `KQ-100` (R3b S0) · CG1 `WO-101 · BG-102 · KQ-103/104/105` · DT3 `WO-106 · BG-107 · KQ-108/109/110`. **Số trống kế tiếp: 111.**
- Sổ phát hiện: riêng mỗi bước `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_<ID>.md`; sổ chung `SO_PHAT_HIEN_ISP-3.1.md` (trên `isp/S0`) — orchestrator gộp sổ riêng vào sổ chung lúc gộp bước.
- Thang: **được gộp + push = 0 CHẶN và 0 NÊN SỬA còn mở** sau R3 (NÊN SỬA còn ⇒ vòng sửa + vòng xác nhận "R3b").

### 4.3 Chế độ tăng tốc (người dùng duyệt 16/11)
1. Bước được GIAO khi phụ thuộc đã **bàn giao (BG) + R1 có 0 CHẶN** (⛔ chờ R3).
2. Review chạy song song với bước kế của tác giả; **vòng sửa giao phiên MỚI cùng làn**.
3. Nền wave là nhánh gộp cục bộ `isp/base-wN`.
4. Orchestrator đọc trước dữ liệu Drive. ⛔ bỏ vòng review nào.

### 4.4 Commit
- Message kết thúc bằng hai dòng trailer **mà phiên mới được cấp** (`Co-Authored-By: …` + `Claude-Session: <URL phiên mới>`). ⛔ ghi định danh model vào commit / tệp.

## 5. Trạng thái từng bước lúc dừng + việc kế (bảng đầy đủ 48 bước: `TIEN_DO.md`)

| Step · ID | Làn | Trạng thái | Việc kế (brief) | Cụm gợi ý |
|---|---|---|---|---|
| 0 · S0 | BE-CF | sửa sau R3 xong | **R3b** `KQ-100` trên `fb79f7e..isp/S0` (`brief/r3b_s0.md`) ⇒ ĐẠT thì **gộp S0 đầu tiên** (§6) | 5433 |
| 1 · H1 | BE-HC | R2 ĐẠT 0 NÊN SỬA | **R3** `KQ-074` xác nhận (`brief/r3_h1.md`) ⇒ gộp | 5445 |
| 2 · C1 | BE-CF | vòng sửa sau R2 **dở (WIP `37772f3`)** | làm nốt `C1-R2-01` (tỷ giá `'0'` phải bị từ chối có tên; hai đột biến `<=→<` · gỡ chốt phải CHẾT) + GHI NHẬN rẻ + mục BG (`brief/sua_c1.md`; ⚠ nền nay là `37772f3`, đọc diff WIP trước) ⇒ **R3** `KQ-079` | 5434 |
| 3 · DT1a | DATA | **R3 ĐẠT — done** | gộp ngay sau S0 | — |
| 4 · H2 | BE-HC | sửa sau R1 xong | **R2** `KQ-093` trên `5e63a90..isp/H2` (`brief/r2_h2.md`) ⇒ R3 `KQ-094` | 5447 |
| 5 · DT1b | DATA | R1: 5 NÊN SỬA; sửa **chưa bắt đầu** | vòng sửa (`brief/sua_dt1b.md`) ⇒ R2 `KQ-098` ⇒ R3 `KQ-099`. Nhãn THẬT: thử RAW gốc bằng khoá SA (§7) — gỡ được thì gỡ luôn `B-DATA-2` | 5437 |
| 7 · CG1 | BE-CF | bàn giao `BG-102` | **R1** `KQ-103` (`brief/r1_cg1.md`) | 5444 |
| 8 · DT2 | FE↩DATA | vòng sửa sau R2 **dở (WIP `5e962d7`)** | làm nốt `DT2-R2-01` (`nap_khuon` đăng ký `sys.modules`) · `-02` (bài `danh_sach_khuon` đòi `ix_fx ∈` + tham số hoá) + chạy cổng + mục BG (`brief/sua_dt2.md`) ⇒ **R3** `KQ-089` | 5436 |
| 10 · DT3 | FE↩DATA | bàn giao `BG-107` | **R1** `KQ-108` (`brief/r1_dt3.md`; PII rủi ro số 1) | 5446 |
| 6 · H3 | BE-HC | `blocked` `B-DATA-2` | cần nhãn THẬT của DT1b | — |
| 9 · FG | FE | `planned` | giao khi R1 CG1 có 0 CHẶN | 5436 |
| 11 · C4 | BE-CF | `planned` | giao khi R1 DT3 có 0 CHẶN | 5434 |
| 12 · DT4 … DT12 | DATA (FE nhận được) | `blocked` `B-DATA-3` | gỡ bằng khoá SA (§7) ⇒ DT4 giao đầu tiên | 5437 |

Làn BE-HC hiện rảnh (H3 chờ nhãn thật; H4 chờ DT4).

## 6. Gộp vào nhánh làm việc (chỉ orchestrator, chỉ sau R3 sạch)

### 6.1 Thứ tự + xung đột đã biết
`S0` → `DT1A` → `H1` → `C1` → `DT2` (đã chứa gộp C1 `eb94901`) → `H2` → `CG1` (chứa S0 + DT1a + H2) → `DT1B` → `DT3` (chứa DT2).
- `tools/dung_moi_truong_isp.sh` dòng `MONG_PYTEST_TOAN_BO`: mỗi nhánh nâng riêng ⇒ xung đột ⇒ đặt = số thu thập của cây gộp.
- `tests/du_lieu/test_dong_bang_sheet.py` bài `danh_sach_khuon`: DT3 viết lại theo cách riêng ⇒ **giữ bản vòng sửa DT2** (`DT2-R2-02`).
- `docs/ITL/_tools/voi_so_luong.json`: chỉ H2 ghi; CG1 chỉ đọc 5 khoá `dat_hd1` (`so_ky_dat` · `mau_so.so_ky` · `ky_dat` · `theo_ky[k].dat` · `theo_ky[k].thieu`).

### 6.2 Việc kèm theo khi gộp
- **S0:** đổi "9 → 11 hợp đồng tầng" ở `CLAUDE.md:73` · `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md:137` · `docs/ITL/01_Orchestrator/08_MIGRATION_ROADMAP.md:45` · `docs/ITL/02_BA/08_NFR.md:51` (`NFR-I16`). ⛔ đụng `06_ORCHESTRATOR_DASHBOARD.md:573` và `Design-F02-Panel/DA-DUNG.md:90` (biên bản 17/09 — Đ2). `WO-065` → `DONG`; một dòng dashboard §5; một dòng changelog.
- **C1:** BA-07 `docs/ITL/02_BA/07_API_CONTRACT.md` §4i — dòng `/config/fx` ⬜ → ✅ (`C1-R1-03`).
- **Ghi vào phiếu C7 (khi phát):** `C1-R1-05` — dải `thieu` ⛔ biên cuối ⇒ `fx_cua` CHẶN theo tháng được hỏi.
- Mỗi lần gộp: chạy lại cổng trên cây gộp (§3 + `CLAUDE.md` mục Cổng), cập nhật `TIEN_DO.md`, commit, push nhánh làm việc. Hook dừng của repo đòi ⛔ còn thay đổi chưa commit.

## 7. Dữ liệu Drive · khoá Service Account (`B-DATA-3`, gỡ được cả `B-DATA-2`)

| Mục | Giá trị |
|---|---|
| Khoá | JSON service account (project `fp-a-project`), người dùng đã tạo + chia sẻ quyền Viewer. Đặt vào **environment của account mới** (Edit → Network secrets, hoặc biến môi trường) tên **`FLS_GSHEETS_SA_JSON`** = toàn bộ nội dung JSON. ⛔ dán vào chat · ⛔ ghi ra tệp trong repo · ⛔ in ra log |
| Network | nếu Limited: thêm `sheets.googleapis.com` · `oauth2.googleapis.com` vào Allowed domains (giữ ô package managers) |
| Đọc | Sheets API v4 `spreadsheets.values.get`/`batchGet` với **`valueRenderOption=UNFORMATTED_VALUE`** + `dateTimeRenderOption=SERIAL_NUMBER`, scope `spreadsheets.readonly`, **theo lát kỳ** (lát hỏng = ĐỎ, ⛔ "không thấy lệch"). Python: `google-auth` (`service_account.Credentials.from_service_account_info(json.loads(os.environ["FLS_GSHEETS_SA_JSON"]), scopes=[…])` + `AuthorizedSession`). Lỗi TLS ⇒ đọc `/root/.ccr/README.md` |
| O7 | orchestrator đọc → scratchpad (⛔ commit bản thô) → agent DATA đóng băng bằng `tools/dong_bang_sheet.py` + khuôn `tools/khuon_dong_bang/<tên>.py` (mỗi nguồn một tệp) |
| Phép thử đầu | đọc 1 ô `9.2.Exchange Rate!A2` của bản sao P&L; rồi thử RAW gốc (`B-DATA-2`) |

Tệp Drive đã biết (tên thật dùng dấu gạch đứng — ở đây viết `·` để ⛔ vỡ bảng):

| Tệp | id | Ghi chú đo được |
|---|---|---|
| `[COPY] Report I General Ledger · P&L Report` | `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` | sheet `Report I General Ledger` (406 — CALC ZONE AX:BU, công thức ở `isp-3.1/CALC_ZONE_406.md`) · `9.2.Exchange Rate` (IMPORTRANGE, đã thông) · `Report I H1000 Ledge (HR Allocate HD) Y2025 · For PL Report` (CDT Correct BR11:BS23 = 13 dòng) · `Report I PLA3 Y H Q M · PM + HR · ATL` (cây ATL A7:F88) |
| `[COPY] ITL I Input Transaction Ledger File 1/2 (RAW)` | `1Llidn1FS61hw6asZ5HZp4uwlZwAuGIvaoJloXyUAJm0` | `Mapping Master` (dữ liệu A:P; `Q1:AN120` rỗng; ⚠ 7 hàng tên viết tắt NGƯỜI ở cột A · B · O) · `Transaction Mapping L1` |
| `[COPY] ITL … 2/2 (ADJUSTED)` | (tìm theo tên) | `get_values` hết giờ 60 s (`GAP-ORA-08`) |
| RAW **gốc** | `1md85t…` (tìm theo tên) | connector: Permission denied — thử bằng SA |
| `[COPY] APERO · FS2` | (tìm theo tên) | `9.2.Exchange Rate` gốc (37 dòng); Mapping Master FS2 `R → LE · AA:AD Cash/Bank` (cho C8 — errata ⑫) |
| Thư mục AS-IS | 25 mục: 22 `[COPY]` + `[FS2] PD Now – Logic & Rules script` + 1 nháp + thư mục `[COPY] Payroll` | — |

Bản thô ở scratchpad phiên cũ (ix_fx · mapping_master · atl · cdt) **⛔ chuyển** (một tệp mang tên người) — phiên mới đọc lại bằng SA khi cần.

## 8. Errata gom cho bản vá ISP/AP v3.1.3 (AP vá chỉ trỏ §A.30)
① `H1-B1` = **0,098039… mUSD** (⛔ 98,039) · ② DT4 §3: 5 tiền tệ là AX:BL; BM/BN/BQ/BT thuộc H1 · ③ FE nhận bước DATA · ④ DT1b dùng `tools/phan_loai_ly_do.py` + `docs/ITL/_tools/phan_loai_ly_do.json` · ⑤ chế độ tăng tốc · ⑥ BA-07 §4i · ⑦ `yyyymm` kiểu `int` · ⑧ khuôn đóng băng mỗi nguồn một tệp `tools/khuon_dong_bang/` · ⑨ `lac`/`thieu` chỉ một định nghĩa (C1) · ⑩ `H2-B2` mong mới (ký 23 dòng thiếu 2026-07 ⇒ vẫn ĐỎ vì 37 dòng tự-soi; vế ô trên MỌI dòng) · ⑪ CDT Correct **13** dòng (⛔ 18) · ⑫ `AA:AD Cash/Bank` là Mapping Master FS2 (C8) · ⑬ chữ ký H2 có `van_tay_dong` bắt buộc + ⛔ ký `KHAC` + `ngay` ≤ hôm nay.

## 9. Việc đầu tiên của phiên mới (theo thứ tự)
1. Đọc §1–§8; khôi phục nhánh + worktree (§2); dựng 9 cụm (§3) — chạy `dung_moi_truong_isp.sh --cong N` từ worktree `isp-s0` cho N ∈ 5433–5437, 5444–5447; kiểm `pg_isready`.
2. Kiểm khoá SA (§7): biến `FLS_GSHEETS_SA_JSON` có mặt (⛔ in nội dung) + đọc thử 1 ô. Hỏng ⇒ báo người dùng tên host bị chặn / lỗi quyền, kèm khuyến nghị.
3. Phát lượt 8 phiên đã dừng (§5): R3b S0 · R3 H1 · R2 H2 · R1 CG1 · R1 DT3 · làm nốt sửa C1 · làm nốt sửa DT2 · sửa DT1b — dùng `chuyen_giao/brief/*.md`.
4. SA thông ⇒ đọc trước nguồn DT4 (406 CALC ZONE BM–BT theo dòng × kỳ) vào scratchpad, phát `WO-111` DT4 (làn DATA) theo ISP Step 12.
5. R3b S0 ĐẠT ⇒ gộp S0 (§6.2), rồi DT1a, rồi các bước đạt R3; báo người dùng sau mỗi wave.
6. Cập nhật `TIEN_DO.md` sau mỗi thay đổi; commit + push.

## 10. Bẫy đã cắn trong phiên cũ
- **Hạn mức 5 giờ:** 7–8 phiên song song tiêu hết hạn mức trong ~4 giờ (dừng 1 lần, HTTP 429). Khi chạm trần, việc dở vẫn nằm trong worktree; gọi lại agent sau giờ đặt lại.
- **Container khởi động lại 3 lần** ⇒ cụm tắt hết; kết quả agent nền có thể ⛔ được báo — đọc phiếu đã commit trên nhánh để biết kết quả.
- `cd` trong lệnh shell có thể đổi thư mục làm việc của phiên sang worktree ⇒ dùng `git -C <đường>` và đường dẫn tuyệt đối.
- Connector Sheets `get_values` trả số **đã định dạng** (SGD `20,692` ≠ `20691.51`) ⇒ đáp án đọc `effectiveValue` / `UNFORMATTED_VALUE`.
- Hai bước định nghĩa cùng khái niệm khác nhau (DT2 ↔ C1 `lac`/`thieu`) ⇒ orchestrator chốt MỘT định nghĩa, gộp nhánh nguồn vào nhánh dùng.
- Bài ghim DANH SÁCH đầy đủ (`== ['ix_fx']`) phá chạy song song ⇒ bài đòi phần tử (`∈`) + tham số hoá.
- `CLAUDE.md` Bẫy: ⛔ `docker compose down` · `PYTHONUTF8=1` · ⛔ thêm `-q` · `.xlsx` offline phá ngày · `|` trần trong bảng markdown · ⛔ sửa tệp qua hai lớp shell.

## 11. Riêng tư
`PM_COT_RIENG_TU = {"Email Address"}` CẤM vào kho · ⛔ Diễn giải / Số chứng từ / tên người trong fixture · `sao_luu/` · `hien_vat/` gitignore đúng vì mang tên người + tiền thật · `fls_itl` chỉ-THÊM · công cụ ghi sổ đòi `FLS_CHO_GHI_THAT=1` · ⛔ bí mật qua chat. Quét 17/11: 12 nhánh `isp/*` thêm **0** tệp có tên viết tắt người (6 tệp có sẵn từ trước, giống hệt nhau trên mọi nhánh, thuộc quyết định owner 11/09 "Tên tài khoản GIỮ").
