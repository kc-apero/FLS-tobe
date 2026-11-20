# HANDOFF — orchestrator ISP 3.1.2 · TẠM DỪNG theo lệnh chủ · 2026-11-20

> **Dành cho:** chủ khi quay lại, và phiên orchestrator tiếp quản.
> **Kế thừa** `HANDOFF_ORCHESTRATOR_2026-11-19.md` (§3 quyết của chủ · §4 setup · §5 vận hành · §6 bẫy · §7 errata vẫn đúng) — tệp này **thay** nó ở chỗ khác nhau.
> **Lệnh của chủ (20/11 ~03:30 UTC):** "Xong thì tạm dừng … push và commit, cho tôi 1 file handoff để đọc khi quay lại."
> ⇒ Orchestrator **⛔ giao phiên mới**; 3 phiên đang chạy được để chạy xong (⛔ ngắt); một lượt kiểm cuối ghi kết cục vào mục **"Trạng thái cuối"** ở cuối tệp.

---

## 0. Câu mở đầu để dán khi quay lại

```
Bạn là orchestrator của ISP 3.1.2 dự án FLS (repo kc-apero/FLS-tobe). Đọc
docs/ITL/01_Orchestrator/isp-3.1/HANDOFF_ORCHESTRATOR_2026-11-20.md trên nhánh
claude/bold-galileo-zukpaf (mục "Trạng thái cuối" trước), dùng skill
isp-orchestrator · isp-gop-buoc · fls-moi-truong, rồi làm §5 "Việc kế".
Trả lời chủ bằng tiếng Việt; mọi câu hỏi kèm khuyến nghị.
```

---

## 1. Tóm tắt một màn hình

| | |
|---|---|
| **Tiến độ** | **36/48 Step ISP đã gộp** (34 lúc nhận + **H7** · **F5** hôm nay). Chỉ đếm Step ISP |
| **Nhánh làm việc** | `claude/bold-galileo-zukpaf` — giữ nguyên (tài khoản mới ⛔ đổi nhánh) |
| **Sàn bài** | `MONG_PYTEST_TOAN_BO=4267` · `MONG_PYTEST_WEB=681` · tập đỏ nền **28** · web **3** |
| **Đường nền gần nhất** | sau gộp F5: `KẾT: ĐẠT` — 28 = 28 · chạy 4267 · web 3 = 3 · 681 |
| **Số phiếu trống kế tiếp** | **273** |
| **Chi phí hôm nay (phiên con, Sonnet 5.5 medium)** | sửa H7 ≈ 1,65 · sửa F5 ≈ 0,93 · dev C13 ≈ 1,11 · DT7 lần 1 ≈ 0,34 USD; các phiên sau xem `get_session(<id>).external_metadata.usage.cost_usd` |

---

## 2. Quyết của chủ HÔM NAY — ⛔ hỏi lại

| Giờ (UTC) | Quyết |
|---|---|
| ~00:40 | Duyệt kế hoạch tiếp quản (Pha 0 môi trường → Pha 1 sửa H7/F5 + 1 bước mới → Pha 2 skill + agent → Pha 3 theo ISP → Pha 4 staging) |
| ~00:40 | **Agent chia theo VAI**: `fls-orchestrator` · `fls-dev` (làn CF/HC/FE/DATA đọc từ WO) · `fls-test` · `fls-ba` |
| ~00:50 | Phiên con gắn **project `fp-a-project`** — hiện bằng tag `remote-agents-project:fp-a-project` (công cụ tạo phiên ⛔ có trường "project"; tài khoản chỉ có 1 environment `Apero`) |
| ~01:05 | Đặt khoá SA cho environment ⇒ mở DT7 (chạy 4 phiên cùng lúc theo lệnh trực tiếp — luật D vẫn là ≤ 3) |
| ~03:00 | **DT7**: share **sổ GỐC** `Report I General Ledger \| CF report` cho SA (bản `[COPY]…` `12S00T…` thiếu 6 tab PLA) |
| ~03:00 | **Staging = GCP**, chủ có quyền admin, **nạp dữ liệu thật**. **Claude ⛔ vào GCP** — Claude viết script, chủ chạy trong Cloud Shell rồi gửi lại phần BÁO CÁO. Kho = **Cloud SQL PostgreSQL 16**. **Tạo tài khoản ngay; phân quyền SSO ở phase sau** |
| ~03:30 | **Tạm dừng** sau khi việc đang chạy xong |

Câu hỏi còn mở từ 19/11 (không chặn): DT6 `ky_suy` · 412 theo sổ nào · chữ C7 AC-4 · O = Σ `pe` MID1 — xem HANDOFF 19/11 §3.

---

## 3. Việc đang dở lúc viết (03:30 UTC) — kết cục ở "Trạng thái cuối"

| Bước | Nhánh `claude/bold-galileo-zukpaf-isp/…` · ngọn | Phiên đang chạy | Vòng kế |
|---|---|---|---|
| **C13** · Step 36 · IX.TMP bản ký có phiên bản | `C13` · `889caec` (đã sửa `C13-R1-01/02/03`) | R2 cuối `KQ-260` — `session_01STddGrwyN7vibk315jevHr` | ĐẠT 0 · 0 ⇒ gộp + lật `07_API_CONTRACT` §4i 2 dòng `…/report/snapshot/{ky}` ⬜ → ✅ |
| **DT12** · Step 38 · ảnh Manual input ITL Ledge | `DT12` · `33ce4b2` (26 kỳ — ⛔ 23 như ISP; 12.049 dòng; ảnh ≈ 1 MB/kỳ) | R1 `KQ-267` — `session_01STddGqVUthc5M8pdhCspNa` | sửa (nếu có) ⇒ R2 cuối `KQ-268` |
| **DT7** · Step 31 · đáp án PLA (PD 414–419) | chưa có nhánh lúc viết | dev, chạy lại trên sổ gốc — `session_01STddGs8aM8JthDzEkMKge3` | R1 `KQ-263` ⇒ R2 `KQ-264` ⇒ mở **H8** |
| **DT11** · Step 41 · đáp án Daily Report 2 · 3 | `DT11` · `6ed1a29` | — (dev xong, **chưa giao R1** vì đủ 3 phiên) | R1 `KQ-271` ⇒ R2 `KQ-272` |

Dải phiếu đã cấp: C13 `WO-257` · `BG-258` · `KQ-259` · `KQ-260` · DT7 `WO-261` · `BG-262` · `KQ-263` · `KQ-264` · DT12 `WO-265` · `BG-266` · `KQ-267` · `KQ-268` · DT11 `WO-269` · `BG-270` · `KQ-271` · `KQ-272`.

---

## 4. Đã làm hôm nay (đều đã push)

| Việc | Ở đâu |
|---|---|
| Môi trường dựng mới + đường nền trên ngọn nhận: `KẾT: ĐẠT` 28 = 28 · 4219 / web 3 = 3 · 675 | `TIEN_DO` hàng 19/11 "Tiếp quản" |
| **Gộp H7 + DT6c** (`51d187f`, R2 `KQ-248` ĐẠT 0 · 0) · **Gộp F5** (`73a21d7`, R2 `KQ-256` ĐẠT 0 · 0) | `TIEN_DO` lượt 02:17–02:46 |
| **3 skill** `.claude/skills/`: `isp-orchestrator` (nhịp lượt, luật A–E, bảng quyết, mẫu prompt) · `isp-gop-buoc` (thủ tục gộp) · `fls-moi-truong` (PG, `--duong-nen`, khoá SA) | `.claude/skills/*/SKILL.md` |
| **Agent** `fls-orchestrator` mới + mục "phiên CON cloud ISP 3.1.2" thêm vào `fls-dev` · `fls-test` · `fls-ba` (chỉ THÊM) | `.claude/agents/` |
| **`tools/gop_buoc_isp.py`** — làm bước 1–2 · 4–7 · 9 của thủ tục gộp (`bat-dau <ID>` → gỡ xung đột tay → `tiep <ID> <ngày>`); mẫu sửa sàn khớp ≠ 1 lần ⇒ ĐỎ và ⛔ ghi tệp. Đã dùng thật cho H7 + F5 | `tools/gop_buoc_isp.py` |
| **Staging bước 01** — `tools/staging/01_dung_staging_gcp.sh` (chủ chạy) | §6 |
| WO-257 · 261 · 265 · 269 | `docs/ITL/01_Orchestrator/handoff/` |

---

## 5. Việc kế khi quay lại (theo thứ tự)

1. **Đọc "Trạng thái cuối"** (cuối tệp) + `list_sessions` (`children: true`) — phiên nào xong sau lượt cuối thì đọc tin cuối (`list_events kinds ["result"]`) và phiếu trên nhánh bước.
2. **Bật lại PG** nếu container mới/khởi động lại (skill `fls-moi-truong` §2) — bài pg đỏ "Connection refused" là môi trường.
3. Gỡ nhánh treo theo bảng quyết (skill `isp-orchestrator`), ≤ 3 phiên:
   - C13: gộp nếu R2 ĐẠT (nếu lượt cuối chưa gộp) — lật §4i.
   - DT12: theo `KQ-267` ⇒ sửa / R2 cuối `KQ-268` ⇒ gộp.
   - DT7: dev xong ⇒ R1 `KQ-263` ⇒ R2 `KQ-264` ⇒ gộp ⇒ **mở H8** (đường găng H7 ✅ → H8 → H12 → H13 → H14 → I2; H8 = **Opus 5.5 medium**, mẫu `dev_engine.md`).
   - DT11: R1 `KQ-271` (mẫu `r1.md`).
4. **KPI** (bước riêng chủ duyệt 19/11, chưa có WO): giao `fls-ba` viết spec + WO trước (20 mã KPI công thức chéo — EBITDA · NCF · PL2 …; nguồn đo ở `TIEN_DO` lượt 15:36 · 16:19 ngày 18/11).
5. Còn lại theo ISP §2.3: **F7** (sau C13) · H12 · H15 (sau DT12) · H13 · I1 · H14 (sau DT11 + C13) · I2.
6. **Staging bước 02** — chỉ khi chủ gửi BÁO CÁO bước 01 (§6).

---

## 6. Staging — trạng thái

| | |
|---|---|
| **Đã có** | `tools/staging/01_dung_staging_gcp.sh` — chủ chạy trong Cloud Shell: `bash tools/staging/01_dung_staging_gcp.sh --project <PROJECT_ID> --kiem` (chỉ đọc) rồi bỏ `--kiem` để dựng |
| **Script dựng** | Cloud SQL PG16 `asia-southeast1` tier `db-custom-1-3840` (~ 50–60 USD/tháng) · SSL bắt buộc · 0 mạng ủy quyền · sao lưu + PITR · chống xoá · cờ `cloudsql.iam_authentication=on` (cho SSO sau) · kho `fls` · tài khoản `fls_admin` (di trú) · `fls_ghi` (đường ghi) · `fls_doc` (đường đọc của cửa API) + `postgres` — mật khẩu ngẫu nhiên chỉ ở Secret Manager · bí mật `fls-staging-jwt-secret` · SA `fls-staging-app` (`cloudsql.client` + đọc đúng 5 bí mật) |
| **Báo cáo** | 12 mục có `mong`, in `KẾT: ĐẠT/ĐỎ` (exit 1 khi ĐỎ); ⛔ chứa mật khẩu/khoá. Đã thử bằng gcloud GIẢ hai chiều (đúng ⇒ ĐẠT · rỗng ⇒ 12 ĐỎ) — **chưa chạy thật trên GCP** |
| **Chờ** | chủ gửi phần BÁO CÁO |
| **Bước 02 (chưa viết)** | di trú `python -m fls.db.pg_migrate` qua Cloud SQL Auth Proxy bằng `fls_admin` · phân quyền bảng: `fls_ghi` DML (giữ chỉ-THÊM `fls_itl` — `INV-I08`), `fls_doc` SELECT + `ALTER ROLE fls_doc SET default_transaction_read_only = on` (cửa `tools/chay_cua.py` từ chối nếu đường đọc ghi được) · `pg_verify` · BÁO CÁO có `mong` |
| **Bước 03 (chưa viết)** | nạp dữ liệu thật (F04 `/nap` hoặc công cụ; IX.* vào kho config) — luật riêng tư `CLAUDE.md`: `Email Address` ⛔ vào kho; công cụ ghi đòi `FLS_CHO_GHI_THAT=1`; rồi chạy test trên staging (pytest với tập đỏ nền khai trước · cổng HD2 · luồng FE Playwright) |
| **Phase SSO** | sau — người dùng IAM gắn vào kho bằng cờ IAM auth đã bật |

---

## 7. Bẫy / bài học mới hôm nay

| Bẫy | Cách chặn |
|---|---|
| Bản `[COPY]` của sổ AS-IS **thiếu tab** (CF report copy ⛔ có 6 tab PLA) | nguồn chuẩn = danh mục PD Now `docs/ITL/_tools/pdnow_buoc.json` (sổ · tab đúng từng ký tự — tab 417 có HAI dấu cách sau `[MID]`); WO luôn có luật "không thấy / ≥ 2 ứng viên ⇒ DỪNG báo ứng viên" — DT7 dừng đúng luật, tốn 0,34 USD |
| Secret đặt SAU khi container của orchestrator dựng ⇒ orchestrator ⛔ thấy biến; phiên con mới thì thấy | kiểm `test -n` ở phiên con; orchestrator ⛔ cần khoá nếu không tự đọc sheet |
| Container khởi động lại giữa phiên ⇒ cụm 5433 tắt | vòng bật lại (skill `fls-moi-truong` §2) trước khi gộp |
| `gop_buoc_isp.py` bản đầu ghi lặp chú thích chuỗi gộp khi nhánh bước đã tự ghi | đã vá: sàn không đổi ⇒ ⛔ thêm chú thích |
| `git checkout --ours` trên tệp KHÔNG xung đột lấy bản đã gộp (không phải bản nhánh làm việc) | vô hại vì sàn luôn đặt lại = thu thập thật; nhớ khi đọc log |
| ISP ghi số kỳ/số tab sai dữ liệu (DT12: 26 kỳ ⛔ 23) | đo trước, khai `mong` theo dữ liệu; gom errata v3.1.3 (HANDOFF 19/11 §7) |

Errata thêm cho v3.1.3: ㉛ Step 38 (DT12): sổ ADJUSTED có **26 kỳ** theo cột ngày (`2024-10…2026-11`; 3 kỳ 2024 = 15 hàng lạc đầu sổ) — ⛔ "22 kỳ còn lại" · ㉜ Step 31 (DT7): 6 tab PLA chỉ có ở **sổ gốc** CF report, ⛔ bản `[COPY]`.

---

## Trạng thái cuối *(lượt kiểm cuối điền)*

*(chưa điền — lượt kiểm cuối hẹn 04:09 UTC)*
