# BG-360 — bàn giao `WO-359` · 4 agent Voi gọi Claude TRONG GCP công ty: **`claude.googleapis.com`** (chính) · Vertex AI (dự phòng) + script staging 06 + khối lệnh e2e

| | |
|---|---|
| **Thuộc** | `WO-359` |
| **Phát bởi** | `fls-dev` · 2026-11-24 |
| **Nhận** | `fls-test` (R1 → `KQ-361`) · CHỦ (chạy trên GCP — §A) |
| **Nhánh** | `claude/bold-galileo-zukpaf-isp/AG3` · SHA mã: xem §F (commit trước BG) |
| **Kho thật** | `KHONG_CHAM` (G0 BÓNG) · **0** lời gọi mô hình thật từ phiên này (Claude ⛔ vào GCP — quyết chủ 20/11) |

**Biên bản quyết đường (24/11, qua orchestrator):** ~03:15 *"dùng claude trực tiếp trong GCP, thông qua vertex AI"* ⇒ ~03:45 *"đồng ý dùng qua vertex"* ⇒ ảnh console: `fp-a-project` đã BẬT **"Anthropic managed Claude API"** (`claude.googleapis.com`) ⇒ **~03:50 *"dùng claude.googleapis.com cho nhanh"*** = quyết HIỆN HÀNH. Mã có CẢ BA đường qua MỘT lớp nhà cung cấp, chọn bằng `FLS_NHA_CUNG_CAP`: **`google-cloud` (chính — đặt RÕ)** · `vertex` (dự phòng — làm trước, giữ nguyên) · `anthropic` (khoá API, WO-355 — **cũng là đường khi biến VẮNG**: bài nghiệm thu R1 `KQ-357` khoá hành vi ấy, đặt mặc định `google-cloud` ⇒ **19/27** bài ấy ĐỎ — đo 24/11; Dev ⛔ sửa bài nghiệm thu).

> ⛔⛔ **Hôm nay (24/11 ~04:30, chủ qua orchestrator): CẢ HAI đường CHƯA gọi thật được** — Marketplace *Subscribe* chặn vì chủ ⛔ admin billing; *Enable* ở Model Garden mở FORM *"subject to approval by Anthropic"* và chủ hoãn tới mai (dính pháp nhân billing). ⇒ 06 `--kiem` mong **ĐỎ có tên** ở 8 mục gọi thử (`… ⇒ mô hình CHƯA bật / CHƯA được Anthropic duyệt …` hoặc `… CHƯA Subscribe/Activate …`), ⛔ "đang chờ". **Bước e2e §B CHƯA sẵn sàng** tới khi MỘT lời gọi thật = 200.

## ⓪ · Tiền đề BẤM TAY — chủ đánh dấu TRƯỚC khi chạy 06

Nguồn: trang Anthropic `platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/anthropic-managed.md` §Set up your account (đọc 24/11) + đo của orchestrator 24/11.

**Đường `google-cloud` (`claude.googleapis.com`)**
- [ ] **Subscribe** listing Marketplace *"Claude Models on Google Cloud (Anthropic managed)"* → **Manage on Console**. ⚠ Cần quyền MUA trên **billing account** — orchestrator đo 24/11: tài khoản chủ **⛔ admin billing** (`getIamPolicy` ⇒ permission denied) ⇒ bước này **ĐANG CHẶN**; cần người quản billing account làm, hoặc đi đường Vertex.
- [ ] **Hai service** bật: `claude.googleapis.com` (ảnh console chủ: *API Enabled*) **và** `anthropic-managed-claude.cloudpartnerservices.goog` (Marketplace — ghi nhận dùng vào gói; chỉ bật được bằng tài khoản đã mua). 06 bước ① bật cả hai; BÁO CÁO mong **2/2**.
- [ ] Trang Claude (**Agent Platform → Models → Claude Platform → Anthropic managed**) → **Activate** → mở thư xác nhận → điền tổ chức → chấp nhận điều khoản Anthropic.
- [ ] **Open Claude Console** (cần `roles/claude.admin`) → **Settings → Workspaces** → chép ID của *Default Workspace* (`wrkspc_…`) vào biến shell `WS` — ⛔ dán chat.
- [ ] ⛔ gỡ vai của **service agent** mà `claude.googleapis.com` tạo (*"Don't remove its role grants"*) — 06 ⛔ có bước gỡ vai nào (bài `CAM_GHI`).

**Đường `vertex` (dự phòng — chủ đang thử 24/11 vì Subscribe bị chặn)** — nguồn: trang Google `vertex-ai/generative-ai/docs/partner-models/use-partner-models` §Set required permissions (tôi đọc 24/11) + đo của chủ.
- [ ] Người bấm *Enable* có vai **Consumer Procurement Entitlement Manager** (*"Anyone who's been granted this role can enable partner models in Model Garden"*) — chủ đã cấp ở project (orchestrator đo 24/11).
- [ ] Org policy cho phép `cloudcommerceconsumerprocurement.googleapis.com` — chủ đã bật (orchestrator đo).
- [ ] **FORM duyệt của Anthropic cho TỪNG mô hình** — Opus 5.5 **và** Sonnet 5.5 (tên doanh nghiệp · website · email · trụ sở · ngành · số người dùng · mục đích · AUP) ⇒ **CHỜ DUYỆT** (trang Google ⛔ nhắc form; chủ đo trên console). ⏳ hoãn tới mai.
- [ ] `roles/aiplatform.user` cho SA `fls-staging-app` — 06 `--duong vertex` cấp, `--condition=None`.

**Chung**: mọi lệnh cấp vai mức project trong 06 mang `--condition=None` (project có **2** binding CÓ ĐIỀU KIỆN — thiếu cờ là gcloud dừng hỏi; bài tĩnh `test_moi_lenh_cap_vai_muc_project__co_condition_None` đếm **2/2**).

**Đường nào chính** = đường nào bấm *Enable*/*Subscribe* được trước. Mã chọn bằng MỘT biến `FLS_NHA_CUNG_CAP` (`google-cloud` mặc định · `vertex`), ⛔ sửa mã.

## A · Chủ làm gì, theo thứ tự

Tất cả trong **Google Cloud Shell** của `fp-a-project`, ở bản sao repo đã `git fetch` + `git checkout claude/bold-galileo-zukpaf-isp/AG3`. Mỗi bước: **mong** · **gửi lại phần nào**. ⛔ dán token/khoá/nội dung trả lời/workspace ID đầy đủ vào chat — script ⛔ in chúng (workspace in dạng `wrkspc_…(N ký tự)`).

| # | Việc | Mong | Gửi lại |
|---|---|---|---|
| **1** | **Lấy WORKSPACE ID** (bấm tay): Google Cloud console → trang sản phẩm **"Anthropic managed Claude API"** → mở **Claude Console** (cần vai `roles/claude.admin`) → **Settings → Workspaces** → chép ID dạng `wrkspc_…`. *(Nguồn: skill `claude-api` — "In the Claude Console, under Settings > Workspaces … only `roles/claude.admin` can open the Claude Console, which is reached from the Google Cloud console".)* Giữ trong biến shell, ⛔ dán chat | có chuỗi `wrkspc_…` | ⛔ gì |
| **2** | `bash tools/staging/06_vertex_agent.sh --project fp-a-project --workspace-id "$WS" --kiem` | đo NỀN, ⛔ ghi gì. `claude.googleapis.com` bật = **ĐẠT** (ảnh console); service Marketplace = ĐỎ nếu chưa Subscribe; `SA có roles/claude.user` **ĐỎ** + 4 mục gọi TRONG VM **ĐỎ** (`permission_error`) — trạng thái trước, ⛔ lỗi | khối `BÁO CÁO` (từ dòng `── BÁO CÁO` tới hết) |
| **3** | `bash tools/staging/06_vertex_agent.sh --project fp-a-project --workspace-id "$WS" --cap-nguoi <email của chủ>` | ① bật 2 service (đã bật ⇒ ⛔ đổi) ② cấp `roles/claude.user` cho SA `fls-staging-app` **và** cho tài khoản chủ (e2e §B chạy bằng danh tính ấy). BÁO CÁO **`KẾT: ĐẠT` — 15/15 mục** = project công ty · **2** service · vai SA · vai người chạy · VM chạy bằng SA · VM có phạm vi `cloud-platform` · 2 danh tính × 2 mô hình × (HTTP `200` + mô hình trả về = mã ghim). Kèm token vào/ra + USD ƯỚC của 4 lời gọi thử (~0,0005 USD) | khối `BÁO CÁO` |
| **4** | Trả lời **câu chủ C1–C2** (§E) rồi chạy **(a) TẬP NHỎ** ở §B | `KẾT: ĐẠT` · exit **0** · A4 **4/4** · **0** ca phải-để-người bị nối · `đường google-cloud · vùng global` · USD ƯỚC ≤ trần **2** | `docs/ITL/06_Agent/vong_that/REPORT_GIA_THAT.md` (CHỈ số đếm + vân tay) + dòng `API THẬT: … USD` |
| **5** | Xem chi phí (a) trên **hoá đơn GCP** (Billing → Marketplace "Claude") ⇒ nếu ổn, chạy **(b) BỂ A/B** ở §B | `KẾT: ĐẠT` · bảng (b) có số ở cả 4 cột · 0 ca phải-để-người bị nối ở bể A và B · USD ƯỚC ≤ trần **6** | `REPORT_GIA_THAT.md` mới + số USD trên hoá đơn (để đối chiếu ƯỚC — §D) |

> ⚠ Bước 2–3 ĐỎ ở 4 mục **Cloud Shell** với `permission_error` ⇒ tài khoản chủ chưa có `roles/claude.user` (chạy lại bước 3 có `--cap-nguoi`). ĐỎ `not_found_error` ở MỌI lời gọi ⇒ workspace chép sai. ĐỎ `invalid_request_error` chỉ ở một mô hình ⇒ tổ chức Anthropic chưa được dùng mô hình ấy (skill: *"Model … is not available for this organization's inference configuration"*). Bước 4/5 ĐỎ `LoiApi: DefaultCredentialsError (xác thực GCP/ADC …)` ⇒ `gcloud auth application-default login` rồi chạy lại. `VuotTran` ⇒ chuỗi DỪNG đúng trần — gửi report, ⛔ nâng trần khi chưa xem hoá đơn.
>
> **Dự phòng Vertex** (nếu `claude.googleapis.com` vướng): `bash tools/staging/06_vertex_agent.sh --project fp-a-project --duong vertex` ⇒ bấm 2 đường dẫn Model Garden script in ⇒ `… --duong vertex --kiem` mong **13/13** (1 service); §B đổi `FLS_NHA_CUNG_CAP=vertex` + `FLS_VERTEX_DU_LIEU_XAC_NHAN=1` (bỏ `FLS_CLAUDE_WORKSPACE_ID`).

## B · Khối lệnh e2e (Cloud Shell) — dán nguyên

```bash
cd ~/FLS-tobe && git fetch origin claude/bold-galileo-zukpaf-isp/AG3 && git checkout claude/bold-galileo-zukpaf-isp/AG3
python3 -m venv ~/.fls-agent-venv && ~/.fls-agent-venv/bin/pip install -q -r requirements.txt   # anthropic[google_cloud,vertex]
PY=~/.fls-agent-venv/bin/python

# ── đường gọi: claude.googleapis.com của project công ty (MẶC ĐỊNH — ⛔ khoá sk-ant) ──
export PYTHONUTF8=1 FLS_NHA_CUNG_CAP=google-cloud FLS_GCP_PROJECT=fp-a-project     # đường chọn RÕ (vắng ⇒ khoá API)
export FLS_CLAUDE_WORKSPACE_ID="$WS"        # wrkspc_… (bước A1) — ⛔ ghi vào tệp repo
export FLS_CHO_GOI_API=1
export FLS_GC_DU_LIEU_XAC_NHAN=1            # ⛔ đặt trước khi trả lời câu chủ C1 (§E) — đây là lời XÁC NHẬN của người vận hành
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN ANTHROPIC_PROFILE   # skill: các biến này ⛔ dùng ở nền này — gỡ cho sạch

# ── bể giữ riêng từ NGUỒN SỐNG — NGOÀI repo (dir 700) ──
export FLS_HELDOUT_NOI_DUNG=$HOME/fls_heldout && mkdir -p -m 700 "$FLS_HELDOUT_NOI_DUNG"
[ -f ~/.fls_muoi_be ] || (umask 077; openssl rand -hex 16 > ~/.fls_muoi_be)   # muối vân tay BỀN qua các lần dựng
export FLS_MUOI_BE=$(cat ~/.fls_muoi_be)
# quyền ĐỌC sheet — chọn MỘT: tệp khoá SA đọc-sheet (chmod 600, XOÁ sau)  HOẶC  token tài khoản chủ (~60 phút)
export FLS_SHEETS_SA_JSON_TEP=$HOME/sa_doc_sheet.json
# export FLS_SHEETS_TOKEN=$(gcloud auth print-access-token --scopes=https://www.googleapis.com/auth/spreadsheets.readonly)
$PY tools/dung_be_giu_rieng.py --doc-song --tho /tmp/fls_be_tho/nguon.json
#   mong: "bể a: 65/65 ca · thiếu không" · "bể b: 70/70 ca · thiếu không" (số BG-356)
unset FLS_SHEETS_TOKEN

# ── (a) TẬP NHỎ: 12 ca dựng + ≤ 20 ca bể B — chạy TRƯỚC, xem chi phí ──
$PY tools/vong_that_voi.py --that --tran-usd 2 --ghi
#   trần = chặn lời gọi KẾ khi tổng ≥ trần — ⛔ cắt lời đang chạy (AG2-R1-03); nhật ký lời gọi ghi LUÔN (AG2-R1-04)
#   mong: exit 0 · "**KẾT: ĐẠT**" · "| đường gọi thật | `google-cloud` …" · "Sau tập nhỏ (a): N lời gọi · ~X USD"

# ── (b) BỂ A/B — CHỈ sau khi xem chi phí (a) trên hoá đơn ──
$PY tools/vong_that_voi.py --that --be --tran-usd 6 --ghi

# ── dọn ──
rm -rf /tmp/fls_be_tho ; rm -f $HOME/sa_doc_sheet.json      # bể ~/fls_heldout GIỮ (dùng lại cho vòng sau)
```

- **Danh tính gọi mô hình ở §B** = tài khoản CHỦ (ADC của Cloud Shell) ⇒ cần `roles/claude.user` (bước A3 `--cap-nguoi`). **Danh tính SA `fls-staging-app`** (cái app staging dùng) được đo riêng ở bước A3 (gọi thử TRONG VM qua IAP). Chạy CHUỖI agent TRONG VM cần dựng môi trường Python trong VM — ⛔ làm ở `WO-359`; đề xuất phiếu sau (mục tiêu kế của chủ: nối 4 agent với staging FE+BE).
- **G0 BÓNG**: `vong_that_voi.py` ⛔ mở kho (đo: chạy trọn với `PG_DSN` **gỡ** khỏi môi trường ⇒ report sinh bình thường); công cụ agent chỉ đọc ảnh/tệp đo trong repo + bể ngoài repo ⇒ ⛔ chạm Cloud SQL staging.
- Report ghi vào bản sao repo ở Cloud Shell (CHỈ số + vân tay). **⛔ commit từ Cloud Shell**: chủ gửi lại nội dung `.md`.

## C · Bảng AC → bằng chứng

| AC | Mong | Kết | Bằng chứng |
|---|---|---|---|
| AC-1 · nhà cung cấp trong GCP | đường gọi Claude trong GCP chọn bằng cấu hình; xác thực ADC/SA (⛔ khoá trong repo); giữ đường API-key dự phòng. *(WO viết cho Vertex; chủ đổi đường chính sang `claude.googleapis.com` 24/11 ~03:50 — Vertex GIỮ làm dự phòng)* | **ĐẠT** (SDK GIẢ, ⛔ mạng) | `fls/agent/mo_hinh.py`: **`AnthropicGoogleCloudMessages`** dựng `anthropic.AnthropicGoogleCloud(project=…, workspace_id=…, max_retries=…)` · **`AnthropicVertexMessages`** dựng `anthropic.AnthropicVertex(project_id=…, region=…)` — chữ ký CẢ HAI đối chiếu SDK THẬT **`anthropic` 2.13.0** (2 bài `importorskip`). `ADAPTER_DUONG` chọn theo `duong_goi()`; biến vắng ⇒ `google-cloud`. Mã mô hình = mã TRẦN `claude-opus-5-5` / `claude-sonnet-5-5` ở cả hai đường (skill + trang Anthropic 24/11). Vertex: vùng `global`/`us`/`eu`; vùng đơn ⇒ `CamGoiThat` (*"Regional endpoints serve Claude Sonnet 4.6 and earlier models only"*). Chuỗi 4 agent chạy TRỌN trên MỖI đường (SDK giả) ⇒ A4 **4/4**, nhật ký ghi đúng `duong` (2 bài) |
| AC-2 · chốt + chi phí | 3 chốt + trần giữ; bỏ đòi khoá; THAY `FLS_ZDR_DA_BAT` bằng xác nhận hợp đường (chính sách TRA); nhật ký token + USD (giá, ngày tra) | **ĐẠT** + **câu chủ C1** | Chốt chung giữ: `--that` · `FLS_CHO_GOI_API=1` · ghim. `google-cloud`: đòi `FLS_GCP_PROJECT` ∈ `DU_AN_CONG_TY` · `FLS_CLAUDE_WORKSPACE_ID` dạng `wrkspc_[A-Za-z0-9_]` (4 dạng xấu bị chặn) · chế độ `mo` đòi **`FLS_GC_DU_LIEU_XAC_NHAN=1`** — `FLS_ZDR_DA_BAT=1` lẫn `FLS_VERTEX_DU_LIEU_XAC_NHAN=1` ⛔ thay được (skill: *"A Zero Data Retention arrangement doesn't carry over"*). `vertex`: `FLS_VERTEX_DU_LIEU_XAC_NHAN=1`. ⛔ đòi `ANTHROPIC_API_KEY` ở cả hai (bài chạy với khoá VẮNG). Trần USD: `VuotTran` ở lời thứ 3 (trần 5, mỗi lời ~4 USD) — mỗi đường 1 bài. Nhật ký +2 trường `duong` · `vung`; `ngay_tra_gia` **2026-11-24** ở đường GCP. Lỗi `google.auth` ⇒ `LoiApi` CÓ TÊN, ⛔ lộ đường dẫn tệp ADC; lỗi khác ném nguyên. Giá: §D |
| AC-3 · script GCP cho CHỦ | `06_vertex_agent.sh --project fp-a-project [--kiem]`: bật API · bước bấm tay ghi rõ · cấp vai cho SA · gọi thử 1 lời/mô hình ⇒ BÁO CÁO có `mong`, ĐỎ hai chiều, ⛔ in khoá/token | **ĐẠT** (gcloud + curl GIẢ có trạng thái) | `tools/staging/06_vertex_agent.sh` (`--duong google-cloud` mặc định · `vertex`) + **41** bài `tests/agent/test_06_vertex_agent.py` (đa số chạy CHO CẢ HAI đường) với `tests/agent/vertex_gia.py` (một tệp, hai tên `gcloud`/`curl`; lệnh TRONG VM **chạy thật bằng bash**). Đo: từ trống + bước bấm tay chưa xong (workspace sai · Model Garden chưa bật) ⇒ ĐỎ **đúng 8** mục gọi thử, service + IAM ĐẠT · xong ⇒ **14/14** (google-cloud, 2 service) · **13/13** (vertex) · thiếu service Marketplace ⇒ ĐỎ ĐÚNG mục ấy dù lời gọi 200 · `--condition=None` **2/2** lệnh cấp vai (bài tĩnh) · chạy 3 lần ⇒ IAM **1** binding, service **2** (google-cloud) / **1** (vertex) · `--kiem` **0** lệnh ghi · 8 phép phá × 2 đường ⇒ ĐÚNG tập mục ĐỎ · `--cap-nguoi` cấp + đo vai người chạy · `--khong-goi-thu` ⇒ 8 mục ĐỎ (Đ5) · tham số xấu ⇒ exit 2 trước MỌI lệnh · 5 lính canh (token người · token SA · nội dung trả lời · thông điệp lỗi · workspace đầy đủ) **0** lần trong đầu ra. BÁO CÁO kèm trạng thái API của đường kia (thông tin) |
| AC-4 · test e2e trên staging | lệnh CHỦ chạy: dựng bể giữ riêng từ nguồn sống (ngoài repo) ⇒ chuỗi 4 agent THẬT (tập nhỏ ⇒ xem chi phí ⇒ bể A/B) ⇒ report MỘT trang GIẢ ↔ THẬT; G0 BÓNG | **ĐẠT phần mã + khối lệnh** · số THẬT **chờ chủ** (§A 4–5) | §B. `vong_that_voi.py` ghi `đường gọi thật` + `đường · vùng` + nhãn giá; thiếu chốt ⇒ exit **2** có tên (`thiếu FLS_CLAUDE_WORKSPACE_ID` · `thiếu FLS_GCP_PROJECT`) (bài); đủ chốt + SDK giả ⇒ exit **0** `KẾT: ĐẠT` với chữ `CHƯA có bảng giá` (bài). `dung_be_giu_rieng.py` đọc sheet bằng `FLS_SHEETS_TOKEN` / `FLS_SHEETS_SA_JSON_TEP` (Cloud Shell), phạm vi CHỈ `spreadsheets.readonly` (bài). Report trong repo = lượt KHÔNG chốt (đường mặc định `google-cloud`, thiếu project/workspace) — sinh lại bởi `--ghi`, ⛔ số THẬT |
| AC-5 · an toàn | ⛔ nội dung/phản hồi thô vào repo; ⛔ khoá; `quet_pii_repo` 0; đọc toàn bộ nội dung + số TK chỉ trong GCP công ty | **ĐẠT** | `DU_AN_CONG_TY = ("fp-a-project",)` — project khác ⇒ `CamGoiThat` ở cả hai đường (5 bài); 06 có mục `project = GCP công ty` mong `fp-a-project`. Nhật ký ⛔ chứa `"lam di"` · `0123456789` (STK giả trong yêu cầu) · khoá · workspace (bài). Script 06: token chỉ ở biến + tệp 600, header đọc `@tệp`, thân trả lời → tệp tạm → CHỈ in `model`/`stop_reason`/số token, xoá ngay. `quet_pii_repo` **0** (§F) |
| AC-6 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit); `kiem_tai_lieu` · `lint-imports` | xem §F | sàn `MONG_PYTEST_TOAN_BO` **5020 → 5150** = thu thập thật sau gộp AG2 + vòng sửa §H (`pytest --collect-only` ⇒ **5150 tests collected**; WO-359 đến 5116: +34 `test_mo_hinh_vertex.py` · +21 `test_mo_hinh_google_cloud.py` · +41 `test_06_vertex_agent.py`; web **690** giữ) + `tests/test_dung_moi_truong_isp.py` cùng commit |

**Bài mới đã CHỨNG MINH ĐỎ** (phá nguồn → chạy → xem cắn → trả nguyên; `cmp` xác nhận mỗi phép phá ĂN vào tệp và tệp được trả nguyên):

| phá | bài | đỏ |
|---|---|---|
| `mo_hinh` vertex: dựng `sdk.Anthropic` (đường khoá) | `test_mo_hinh_vertex.py` | **3** / 31 |
| `mo_hinh` vertex: thêm `asia-southeast1` vào `VUNG_VERTEX` | ″ | **2** / 31 |
| `mo_hinh`: bỏ chốt `DU_AN_CONG_TY` | ″ | **3** / 31 |
| `mo_hinh` vertex: bỏ chốt `FLS_VERTEX_DU_LIEU_XAC_NHAN` | ″ | **2** / 31 |
| `mo_hinh` google-cloud: `workspace_id=None` | `test_mo_hinh_google_cloud.py` | **1** / 21 |
| `mo_hinh`: mặc định (biến vắng) về `google-cloud` | `tests/nghiem_thu/test_kq357_…` (chủ `fls-test`) | **19** / 27 — lý do giữ mặc định `anthropic` |
| `mo_hinh` google-cloud: bỏ kiểm dạng workspace | ″ | **4** / 21 |
| `mo_hinh` google-cloud: bỏ chốt `FLS_GC_DU_LIEU_XAC_NHAN` | ″ | **2** / 21 |
| 06: `cat` tệp header (lộ token) | `test_06_vertex_agent.py` | **23** / 39 |
| 06: google-cloud cấp nhầm `roles/aiplatform.user` | ″ | **13** / 39 |
| 06: google-cloud bỏ header `anthropic-version` | ″ | **12** / 39 |
| 06: BÁO CÁO luôn `ok = True` | ″ | **25** / 39 |
| 06: in workspace đầy đủ | ″ | **1** / 39 |
| 06: bỏ header `Metadata-Flavor` (VM ⛔ lấy được token) | ″ | **24** / 39 |
| 06: chỉ bật `claude.googleapis.com` (bỏ service Marketplace) | ″ (lọc 6 bài liên quan) | **2** / 6 |
| 06: bỏ `--condition=None` ở lệnh cấp vai đầu | ″ (lọc 6 bài) | **1** / 6 |

*(4 phép phá vertex chạy khi tệp còn 31 bài ⇒ nay 34; 6 phép phá 06 đầu chạy khi tệp có 39 bài ⇒ nay 41.)*

## D · Giá (tra 2026-11-24) — và GIẢ ĐỊNH CHƯA KIỂM

- **`google-cloud` (chính): GIÁ CHƯA ĐO — chưa có bảng giá theo token cho nền này.** Skill `claude-api`: *"This skill has no per-token prices for this platform, and whether the first-party prices in SKILL.md apply is unknown."* Trang Anthropic §Billing: *"bills through Google Cloud Marketplace. Anthropic meters your usage … in Claude Consumption Units. One Claude Consumption Unit is $0.01 USD"* — ⛔ nói giá mỗi token; xem số thật ở trang **Usage/Cost** của Claude Console hoặc hoá đơn GCP. ⇒ Để GIỮ trần USD (chốt WO-355), `BANG_GIA_GOOGLE_CLOUD` = giá Claude API — nhãn ƯỚC ở mọi chỗ in; **số thật = hoá đơn** (chủ gửi ở bước A5).
- **Giá Claude API** (Anthropic `about-claude/pricing`, 24/11): Opus 5.5 **$4** vào · **$5** ghi cache 5' · **$0,20** đọc cache · **$20** ra; Sonnet 5.5 **$2 · $2,50 · $0,10 · $10** — khớp `BANG_GIA` **8/8** ô.
- **`vertex` (dự phòng):** trang Anthropic trỏ sang bảng giá Google + *"Regional and multi-region endpoints include a 10 percent premium over global endpoints"*. ⚠ Trang giá Google trả nội dung RỖNG cho phiên này ⇒ GIẢ ĐỊNH global = giá Claude API (vài trang tổng hợp bên thứ ba ghi Opus 5.5 $4/$20 global · $4,40/$22 đa vùng — khớp, ⛔ chính thức). ⚠ Vertex ⛔ có Batches API.

**Giả định GCP chưa kiểm** (bài GIẢ mô phỏng theo chúng; script **chỉ so `HTTP == 200`** + `model` ⇒ ⛔ phụ thuộc mã lỗi cụ thể):

| # | Giả định | Nếu sai thì |
|---|---|---|
| G1 | `claude.googleapis.com`: URL thô `https://claude.googleapis.com/v1/projects/<p>/locations/global/workspaces/<ws>/invoke/v1/messages` + `Authorization: Bearer <token Google>` + header `anthropic-version: 2026-10-21`, thân như Claude API — chép từ ví dụ cURL trang Anthropic *Claude Models on Google Cloud* 24/11 (ví dụ ấy dùng `gcloud auth application-default print-access-token`; script dùng `gcloud auth print-access-token`) | lời gọi thử Cloud Shell ĐỎ `authentication_error` ⇒ đổi sang token ADC; SDK (§B) ⛔ ảnh hưởng (SDK tự dựng URL) |
| G2 | Mã lỗi `claude.googleapis.com`: thiếu vai/API ⇒ 403 `permission_error`; workspace sai ⇒ 404 `not_found_error`; mô hình ⛔ được dùng ⇒ 400 `invalid_request_error` | chỉ đổi CHỮ dòng "trạng thái lỗi"; ĐẠT/ĐỎ ⛔ đổi |
| G3 | Tài khoản Owner CẦN `roles/claude.user` riêng để gọi (skill: *"The identity making calls needs `roles/claude.user`"*) | `--cap-nguoi` thừa nhưng vô hại |
| G4 | Lời gọi vẫn 200 khi THIẾU service Marketplace (bài giả mô phỏng thế để chứng minh mục service ĐỎ riêng) | ⛔ ảnh hưởng — mục service Marketplace có `mong` riêng |
| G5 | Thân đáp có trường `model` = mã trần đã gọi (cả đường SDK) | mục "mô hình trả về" ĐỎ + adapter ném `LoiApi … ≠ ghim` — chủ gửi BÁO CÁO, Dev nới so khớp có tên |
| G6 | VM `fls-staging-app` (bước 03) có `python3` + `curl` (Debian 12) và phạm vi `cloud-platform` (03 tạo với `--scopes=cloud-platform` — đọc mã nhánh `isp/STG` `03_dung_app.sh:152`) | mục VM ĐỎ có tên |
| G7 | Cloud Shell có ADC dùng được cho SDK (`google.auth.default()`) | `LoiApi: DefaultCredentialsError …` ⇒ `gcloud auth application-default login` |
| G8 | Tài khoản chủ xem được 2 workbook nguồn (cách `FLS_SHEETS_TOKEN`) | dùng cách tệp khoá SA đọc-sheet |
| ~~G10~~ *(vertex)* | ĐÃ ĐÓNG bằng nguồn: vai *Consumer Procurement Entitlement Manager* (trang Google `use-partner-models`, đọc 24/11) | — |
| G9 *(vertex)* | bật Claude ở Model Garden là BẤM TAY; mã lỗi chưa bật 400 `FAILED_PRECONDITION`; `anthropic_version: "vertex-2023-10-16"` trong thân được nhận (trang Anthropic: *"vertex-2023-10-16 or … 2026-10-21"*) | như G2 |

## E · Câu chủ

- **C1 · dữ liệu trên `claude.googleapis.com` (thay `FLS_ZDR_DA_BAT`).** Tra 24/11 (skill `claude-api` + trang Anthropic `anthropic-managed` §Data retention): nền do **Anthropic vận hành**, truy cập qua project GCP; *"follows the same data retention policy as the Claude API … Zero Data Retention (ZDR) is available on request. Contact your Anthropic account representative."* Việc dựng tạo **một tổ chức Anthropic MỚI** — *"A ZDR arrangement on another Anthropic organization doesn't carry over"*. ⇒ Trước khi đặt `FLS_GC_DU_LIEU_XAC_NHAN=1`, chủ xác nhận: **(1)** project là `fp-a-project` của công ty; **(2)** chấp nhận chế độ giữ dữ liệu MẶC ĐỊNH của tổ chức Anthropic mới (theo điều khoản gói Marketplace) **hoặc** đã xin ZDR cho tổ chức ấy. Khuyến nghị: chấp nhận cho test e2e staging; xin ZDR song song trước khi chạy định kỳ (quyết 23/11 *agent đọc toàn bộ nội dung + số TK* đi kèm điều kiện ZDR). *(Đường Vertex dự phòng: Google quản dữ liệu; request-response logging mặc định TẮT; ZDR đối tác xin qua account team Google — trang `data-governance` ⛔ có câu riêng về Claude.)*
- **C2 · workspace ID** là định danh của tổ chức Anthropic — tôi coi là NHẠY: chỉ ở biến môi trường (Cloud Shell) / Secret Manager, ⛔ commit, BÁO CÁO in che. Chủ đồng ý? Nếu muốn app staging gọi tự động, đề xuất lưu Secret Manager `fls-staging-claude-workspace` (phiếu sau).

## H · Vòng sửa sau R1 `KQ-357` (AG2 gộp vào AG3 — orchestrator 24/11 ~04:35)

Gộp `origin/…-isp/AG2` @ `a37f2bb` (KQ-357 + sổ `SO_PHAT_HIEN_ISP-3.1_AG2.md` + 27 bài nghiệm thu) — ⛔ xung đột. 27/27 bài KQ-357 **xanh** trên AG3 (sau khi giữ mặc định = đường khoá và 12 khoá nhật ký ở đường API).

| Mã | Mức | Xử lý | Bằng chứng |
|---|---|---|---|
| `AG2-R1-01` | NÊN SỬA *(orchestrator: NẶNG)* | **SỬA** — `requirements.txt` + `google-auth>=2.0` · `requests>=2.0` · `anthropic[google_cloud,vertex]`. Bài canh MỌI import bên thứ ba (kể cả nhập muộn) của `fls/agent/**` + `tools/*voi*.py` + `dung_be_giu_rieng.py` ⊆ requirements; hiểu `google.auth.transport.requests` ⇒ cần `requests`; extra `anthropic` khớp lớp mã gọi | `tests/agent/test_phu_thuoc_agent.py` **3** bài; 3 phép phá (xoá `google-auth` · xoá `requests` · bỏ extra `google_cloud`) ⇒ mỗi phép **1** đỏ. **Venv MỚI** dựng từ `requirements.txt` (scratchpad, xoá sau): nhập được `google.auth` · `requests` · `AnthropicGoogleCloud` · `AnthropicVertex` (`anthropic 2.13.0`); `dung_be_giu_rieng.py --doc-song` chạy TRỌN bằng SA chỉ-đọc ⇒ `bể a: 65/65 · bể b: 70/70 · thiếu không · kỳ A↔B KHỚP` (bể ngoài repo, đã xoá). ⚠ Ảnh Docker staging (`Dockerfile` nhánh `isp/STG`, ⛔ có trên AG3) chỉ cài `psycopg` — agent chạy ở venv Cloud Shell theo §B, ⛔ trong ảnh; cài gói agent vào ảnh là việc của phiếu "agent chạy trong VM" |
| `AG2-R1-02` | GHI NHẬN | **SỬA** — `chay_agent_voi.bo_ca` nhận cả bố cục phẳng lẫn `a/ b/` (⇒ bể **B**); thư mục thiếu cả hai ⇒ `FileNotFoundError` có tên | `test_vong_sua_kq357.py` 2 bài; phá (bỏ nhánh `b/`) ⇒ **1** đỏ |
| `AG2-R1-03` | GHI NHẬN | **KHAI** — `--help` của 2 công cụ + docstring `VuotTran` + §B: *"chặn lời gọi KẾ khi tổng ≥ trần; ⛔ cắt lời gọi ĐANG chạy"* (đổi ngữ nghĩa trần = đổi bài nghiệm thu `test_tran_usd_vuot_trong_MOT_lan_goi…` ⇒ ⛔ làm) | đọc `--help` |
| `AG2-R1-04` | GHI NHẬN | **SỬA** — `vong_that_voi.py` ghi nhật ký vòng LUÔN khi ≥ 1 lời gọi thật (⛔ phụ thuộc `--ghi`); 0 lời gọi ⇒ ⛔ sinh tệp (Đ3) | 2 bài; phá (`if ncc and a.ghi`) ⇒ **1** đỏ |
| `AG2-R1-05` | GHI NHẬN | **⛔ SỬA (chủ BA)** — thẻ eval `_chung.md` · `a4-soat.md` còn Gemini; nay thêm: đường vận hành GCP, giá chưa đo ⇒ đề xuất `HOI`/`WO` cho `fls-ba` | — |
| `AG2-R1-06` | GHI NHẬN | **SỬA** — `dung_be_giu_rieng.py` ⛔ ghi `DEM_BE.json` khi chỉ khác `ngay_doc`; + thư mục bể GỐC `chmod 700` (đo 24/11: `--ra` mới tạo ⇒ `755`) | chạy `--doc-song` thật ở venv mới TRƯỚC khi sửa ⇒ `M DEM_BE.json` chỉ dòng `ngay_doc` (tái hiện); ⚠ chưa có bài tự động (cần nguồn sống) |
| `AG2-R1-07` | GHI NHẬN | **KHAI** — `refusal` ⇒ chuỗi DỪNG có tên, ⛔ `fallbacks` (quyết một mô hình ghim). Trên Vertex `fallbacks` phía máy chủ vốn ⛔ có | §C AC-1 |
| `AG2-R1-08` | GHI NHẬN | **ĐÓNG bởi WO-359** — chốt tương đương cho 2 đường GCP (project · workspace/vùng · xác nhận dữ liệu), mỗi chốt chứng minh ĐỎ | §C bảng phá |

## F · Cổng (dán thật — container cloud, cụm PG 16 cổng **5437**)

_điền ở commit kế sau `--duong-nen`_

## G · Phát hiện / ghi chú cho R1

1. **Đ1 — `vertex` / `claude.googleapis.com` trước WO-359**: WO khai `git grep -i vertex` trên `docs/ fls/ tools/` = **0**. Nay mã sống ở `fls/agent/mo_hinh.py` · `tools/staging/06_vertex_agent.sh` · `tools/vong_that_voi.py` · `tools/chay_agent_voi.py` · `tools/sinh_the_agent.py` + 4 thẻ.
2. **Tên tệp `06_vertex_agent.sh` giữ theo WO** dù đường chính nay là `claude.googleapis.com` — đổi tên là việc của phiếu (tránh lệch WO ↔ repo).
3. **Thẻ eval của BA** (`05_FleetEval/eval-cards/_chung.md` · `a4-soat.md`) — BG-356 phát hiện #3 vẫn mở (Gemini / "khác họ"); nay thêm: đường vận hành `claude.googleapis.com`, ⛔ bảng giá ⇒ cột chi phí thẻ eval cần BA cập nhật. Dev ⛔ sửa spec.
4. **Mặc định GIỮ** `FLS_NHA_CUNG_CAP` vắng ⇒ `anthropic` (đã thử đổi sang `google-cloud` ở `87cfb3d` → `b20fbcd`; gộp KQ-357 cho thấy 19/27 bài nghiệm thu ĐỎ ⇒ trả về). Bài Dev WO-329/WO-355 vẫn chọn RÕ `FLS_NHA_CUNG_CAP=anthropic` (vô hại). Họ khác `anthropic` (vd `openai` chừa chỗ) ⛔ chịu luật đường — giữ chốt khoá của họ.
5. `NhatKyGoi.dict()`: đường API giữ ĐÚNG **12** khoá (bài nghiệm thu KQ-357 ghim); đường GCP thêm `duong` · `vung` (14).
6. `AnthropicMessages.__init__` nhận `moi_truong` (tiêm được) và **từ chối** dựng khi `FLS_NHA_CUNG_CAP` ≠ đường của lớp ⇒ ⛔ ai dựng thẳng lớp khoá khi cấu hình nói đường GCP.
7. `requirements.txt`: `anthropic[google_cloud,vertex]>=2.12`; venv container đã cài `2.13.0` với cả hai phần thêm.
8. Bể dựng ở Cloud Shell có **muối riêng** (`~/.fls_muoi_be`) ⇒ vân tay ≠ `DEM_BE.json` trong repo — đúng thiết kế `HELD-R1-05`; ⛔ commit `DEM_BE.json` sinh ở Cloud Shell.
9. `kiem_so_song.py` gọi cứng `.venv/Scripts/lint-imports.exe` (đường Windows) — ở container Linux tôi đặt symlink cục bộ (`.venv` gitignore) để đo được.
