# BG-360 — bàn giao `WO-359` · 4 agent Voi gọi Claude TRONG GCP công ty: **`claude.googleapis.com`** (chính) · Vertex AI (dự phòng) + script staging 06 + khối lệnh e2e

| | |
|---|---|
| **Thuộc** | `WO-359` |
| **Phát bởi** | `fls-dev` · 2026-11-24 |
| **Nhận** | `fls-test` (R1 → `KQ-361`) · CHỦ (chạy trên GCP — §A) |
| **Nhánh** | `claude/bold-galileo-zukpaf-isp/AG3` · SHA mã: xem §F (commit trước BG) |
| **Kho thật** | `KHONG_CHAM` (G0 BÓNG) · **0** lời gọi mô hình thật từ phiên này (Claude ⛔ vào GCP — quyết chủ 20/11) |

**Biên bản quyết đường (24/11, qua orchestrator):** ~03:15 *"dùng claude trực tiếp trong GCP, thông qua vertex AI"* ⇒ ~03:45 *"đồng ý dùng qua vertex"* ⇒ ảnh console: `fp-a-project` đã BẬT **"Anthropic managed Claude API"** (`claude.googleapis.com`) ⇒ **~03:50 *"dùng claude.googleapis.com cho nhanh"*** = quyết HIỆN HÀNH. Mã có CẢ BA đường qua MỘT lớp nhà cung cấp, chọn bằng `FLS_NHA_CUNG_CAP`: **`google-cloud` (mặc định)** · `vertex` (dự phòng — làm trước, giữ nguyên) · `anthropic` (khoá API, WO-355).

## A · Chủ làm gì, theo thứ tự

Tất cả trong **Google Cloud Shell** của `fp-a-project`, ở bản sao repo đã `git fetch` + `git checkout claude/bold-galileo-zukpaf-isp/AG3`. Mỗi bước: **mong** · **gửi lại phần nào**. ⛔ dán token/khoá/nội dung trả lời/workspace ID đầy đủ vào chat — script ⛔ in chúng (workspace in dạng `wrkspc_…(N ký tự)`).

| # | Việc | Mong | Gửi lại |
|---|---|---|---|
| **1** | **Lấy WORKSPACE ID** (bấm tay): Google Cloud console → trang sản phẩm **"Anthropic managed Claude API"** → mở **Claude Console** (cần vai `roles/claude.admin`) → **Settings → Workspaces** → chép ID dạng `wrkspc_…`. *(Nguồn: skill `claude-api` — "In the Claude Console, under Settings > Workspaces … only `roles/claude.admin` can open the Claude Console, which is reached from the Google Cloud console".)* Giữ trong biến shell, ⛔ dán chat | có chuỗi `wrkspc_…` | ⛔ gì |
| **2** | `bash tools/staging/06_vertex_agent.sh --project fp-a-project --workspace-id "$WS" --kiem` | đo NỀN, ⛔ ghi gì. `claude.googleapis.com` bật = **ĐẠT** (ảnh console); `SA có roles/claude.user` **ĐỎ** + 4 mục gọi TRONG VM **ĐỎ** (`permission_error`) — trạng thái trước, ⛔ lỗi | khối `BÁO CÁO` (từ dòng `── BÁO CÁO` tới hết) |
| **3** | `bash tools/staging/06_vertex_agent.sh --project fp-a-project --workspace-id "$WS" --cap-nguoi <email của chủ>` | ① bật API (đã bật ⇒ ⛔ đổi) ② cấp `roles/claude.user` cho SA `fls-staging-app` **và** cho tài khoản chủ (e2e §B chạy bằng danh tính ấy). BÁO CÁO **`KẾT: ĐẠT` — 14/14 mục** = project công ty · API · vai SA · vai người chạy · VM chạy bằng SA · VM có phạm vi `cloud-platform` · 2 danh tính × 2 mô hình × (HTTP `200` + mô hình trả về = mã ghim). Kèm token vào/ra + USD ƯỚC của 4 lời gọi thử (~0,0005 USD) | khối `BÁO CÁO` |
| **4** | Trả lời **câu chủ C1–C2** (§E) rồi chạy **(a) TẬP NHỎ** ở §B | `KẾT: ĐẠT` · exit **0** · A4 **4/4** · **0** ca phải-để-người bị nối · `đường google-cloud · vùng global` · USD ƯỚC ≤ trần **2** | `docs/ITL/06_Agent/vong_that/REPORT_GIA_THAT.md` (CHỈ số đếm + vân tay) + dòng `API THẬT: … USD` |
| **5** | Xem chi phí (a) trên **hoá đơn GCP** (Billing → Marketplace "Claude") ⇒ nếu ổn, chạy **(b) BỂ A/B** ở §B | `KẾT: ĐẠT` · bảng (b) có số ở cả 4 cột · 0 ca phải-để-người bị nối ở bể A và B · USD ƯỚC ≤ trần **6** | `REPORT_GIA_THAT.md` mới + số USD trên hoá đơn (để đối chiếu ƯỚC — §D) |

> ⚠ Bước 2–3 ĐỎ ở 4 mục **Cloud Shell** với `permission_error` ⇒ tài khoản chủ chưa có `roles/claude.user` (chạy lại bước 3 có `--cap-nguoi`). ĐỎ `not_found_error` ở MỌI lời gọi ⇒ workspace chép sai. ĐỎ `invalid_request_error` chỉ ở một mô hình ⇒ tổ chức Anthropic chưa được dùng mô hình ấy (skill: *"Model … is not available for this organization's inference configuration"*). Bước 4/5 ĐỎ `LoiApi: DefaultCredentialsError (xác thực GCP/ADC …)` ⇒ `gcloud auth application-default login` rồi chạy lại. `VuotTran` ⇒ chuỗi DỪNG đúng trần — gửi report, ⛔ nâng trần khi chưa xem hoá đơn.
>
> **Dự phòng Vertex** (nếu `claude.googleapis.com` vướng): `bash tools/staging/06_vertex_agent.sh --project fp-a-project --duong vertex` ⇒ bấm 2 đường dẫn Model Garden script in ⇒ `… --duong vertex --kiem` mong **13/13**; §B đổi `FLS_NHA_CUNG_CAP=vertex` + `FLS_VERTEX_DU_LIEU_XAC_NHAN=1` (bỏ `FLS_CLAUDE_WORKSPACE_ID`).

## B · Khối lệnh e2e (Cloud Shell) — dán nguyên

```bash
cd ~/FLS-tobe && git fetch origin claude/bold-galileo-zukpaf-isp/AG3 && git checkout claude/bold-galileo-zukpaf-isp/AG3
python3 -m venv ~/.fls-agent-venv && ~/.fls-agent-venv/bin/pip install -q -r requirements.txt   # anthropic[google_cloud,vertex]
PY=~/.fls-agent-venv/bin/python

# ── đường gọi: claude.googleapis.com của project công ty (MẶC ĐỊNH — ⛔ khoá sk-ant) ──
export PYTHONUTF8=1 FLS_GCP_PROJECT=fp-a-project
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
| AC-3 · script GCP cho CHỦ | `06_vertex_agent.sh --project fp-a-project [--kiem]`: bật API · bước bấm tay ghi rõ · cấp vai cho SA · gọi thử 1 lời/mô hình ⇒ BÁO CÁO có `mong`, ĐỎ hai chiều, ⛔ in khoá/token | **ĐẠT** (gcloud + curl GIẢ có trạng thái) | `tools/staging/06_vertex_agent.sh` (`--duong google-cloud` mặc định · `vertex`) + **39** bài `tests/agent/test_06_vertex_agent.py` (đa số chạy CHO CẢ HAI đường) với `tests/agent/vertex_gia.py` (một tệp, hai tên `gcloud`/`curl`; lệnh TRONG VM **chạy thật bằng bash**). Đo: từ trống + bước bấm tay chưa xong (workspace sai · Model Garden chưa bật) ⇒ ĐỎ **đúng 8** mục gọi thử, API + IAM ĐẠT · xong ⇒ **13/13** · chạy 3 lần ⇒ IAM **1** binding, API **1** · `--kiem` **0** lệnh ghi · 8 phép phá × 2 đường ⇒ ĐÚNG tập mục ĐỎ · `--cap-nguoi` cấp + đo vai người chạy · `--khong-goi-thu` ⇒ 8 mục ĐỎ (Đ5) · tham số xấu ⇒ exit 2 trước MỌI lệnh · 5 lính canh (token người · token SA · nội dung trả lời · thông điệp lỗi · workspace đầy đủ) **0** lần trong đầu ra. BÁO CÁO kèm trạng thái API của đường kia (thông tin) |
| AC-4 · test e2e trên staging | lệnh CHỦ chạy: dựng bể giữ riêng từ nguồn sống (ngoài repo) ⇒ chuỗi 4 agent THẬT (tập nhỏ ⇒ xem chi phí ⇒ bể A/B) ⇒ report MỘT trang GIẢ ↔ THẬT; G0 BÓNG | **ĐẠT phần mã + khối lệnh** · số THẬT **chờ chủ** (§A 4–5) | §B. `vong_that_voi.py` ghi `đường gọi thật` + `đường · vùng` + nhãn giá; thiếu chốt ⇒ exit **2** có tên (`thiếu FLS_CLAUDE_WORKSPACE_ID` · `thiếu FLS_GCP_PROJECT`) (bài); đủ chốt + SDK giả ⇒ exit **0** `KẾT: ĐẠT` với chữ `CHƯA có bảng giá` (bài). `dung_be_giu_rieng.py` đọc sheet bằng `FLS_SHEETS_TOKEN` / `FLS_SHEETS_SA_JSON_TEP` (Cloud Shell), phạm vi CHỈ `spreadsheets.readonly` (bài). Report trong repo = lượt KHÔNG chốt (đường mặc định `google-cloud`, thiếu project/workspace) — sinh lại bởi `--ghi`, ⛔ số THẬT |
| AC-5 · an toàn | ⛔ nội dung/phản hồi thô vào repo; ⛔ khoá; `quet_pii_repo` 0; đọc toàn bộ nội dung + số TK chỉ trong GCP công ty | **ĐẠT** | `DU_AN_CONG_TY = ("fp-a-project",)` — project khác ⇒ `CamGoiThat` ở cả hai đường (5 bài); 06 có mục `project = GCP công ty` mong `fp-a-project`. Nhật ký ⛔ chứa `"lam di"` · `0123456789` (STK giả trong yêu cầu) · khoá · workspace (bài). Script 06: token chỉ ở biến + tệp 600, header đọc `@tệp`, thân trả lời → tệp tạm → CHỈ in `model`/`stop_reason`/số token, xoá ngay. `quet_pii_repo` **0** (§F) |
| AC-6 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit); `kiem_tai_lieu` · `lint-imports` | xem §F | sàn `MONG_PYTEST_TOAN_BO` **5020 → 5114** = thu thập thật (`pytest --collect-only` ⇒ **5114 tests collected**; +34 `test_mo_hinh_vertex.py` · +21 `test_mo_hinh_google_cloud.py` · +39 `test_06_vertex_agent.py`; web **690** giữ) + `tests/test_dung_moi_truong_isp.py` cùng commit |

**Bài mới đã CHỨNG MINH ĐỎ** (phá nguồn → chạy → xem cắn → trả nguyên; `cmp` xác nhận mỗi phép phá ĂN vào tệp và tệp được trả nguyên):

| phá | bài | đỏ |
|---|---|---|
| `mo_hinh` vertex: dựng `sdk.Anthropic` (đường khoá) | `test_mo_hinh_vertex.py` | **3** / 31 |
| `mo_hinh` vertex: thêm `asia-southeast1` vào `VUNG_VERTEX` | ″ | **2** / 31 |
| `mo_hinh`: bỏ chốt `DU_AN_CONG_TY` | ″ | **3** / 31 |
| `mo_hinh` vertex: bỏ chốt `FLS_VERTEX_DU_LIEU_XAC_NHAN` | ″ | **2** / 31 |
| `mo_hinh` google-cloud: `workspace_id=None` | `test_mo_hinh_google_cloud.py` | **1** / 21 |
| `mo_hinh`: mặc định về `anthropic` | ″ | **19** / 21 |
| `mo_hinh` google-cloud: bỏ kiểm dạng workspace | ″ | **4** / 21 |
| `mo_hinh` google-cloud: bỏ chốt `FLS_GC_DU_LIEU_XAC_NHAN` | ″ | **2** / 21 |
| 06: `cat` tệp header (lộ token) | `test_06_vertex_agent.py` | **23** / 39 |
| 06: google-cloud cấp nhầm `roles/aiplatform.user` | ″ | **13** / 39 |
| 06: google-cloud bỏ header `anthropic-version` | ″ | **12** / 39 |
| 06: BÁO CÁO luôn `ok = True` | ″ | **25** / 39 |
| 06: in workspace đầy đủ | ″ | **1** / 39 |
| 06: bỏ header `Metadata-Flavor` (VM ⛔ lấy được token) | ″ | **24** / 39 |

*(4 phép phá vertex chạy khi tệp còn 31 bài; sau đó thêm 3 bài ⇒ 34.)*

## D · Giá (tra 2026-11-24) — và GIẢ ĐỊNH CHƯA KIỂM

- **`google-cloud` (chính): CHƯA CÓ BẢNG GIÁ chính thức.** Skill `claude-api`: *"This skill has no per-token prices for this platform, and whether the first-party prices in SKILL.md apply is unknown."* Hoá đơn qua Google Cloud Marketplace. ⇒ Để GIỮ trần USD (chốt WO-355), `BANG_GIA_GOOGLE_CLOUD` = giá Claude API — nhãn ƯỚC ở mọi chỗ in; **số thật = hoá đơn** (chủ gửi ở bước A5).
- **Giá Claude API** (Anthropic `about-claude/pricing`, 24/11): Opus 5.5 **$4** vào · **$5** ghi cache 5' · **$0,20** đọc cache · **$20** ra; Sonnet 5.5 **$2 · $2,50 · $0,10 · $10** — khớp `BANG_GIA` **8/8** ô.
- **`vertex` (dự phòng):** trang Anthropic trỏ sang bảng giá Google + *"Regional and multi-region endpoints include a 10 percent premium over global endpoints"*. ⚠ Trang giá Google trả nội dung RỖNG cho phiên này ⇒ GIẢ ĐỊNH global = giá Claude API (vài trang tổng hợp bên thứ ba ghi Opus 5.5 $4/$20 global · $4,40/$22 đa vùng — khớp, ⛔ chính thức). ⚠ Vertex ⛔ có Batches API.

**Giả định GCP chưa kiểm** (bài GIẢ mô phỏng theo chúng; script **chỉ so `HTTP == 200`** + `model` ⇒ ⛔ phụ thuộc mã lỗi cụ thể):

| # | Giả định | Nếu sai thì |
|---|---|---|
| G1 | `claude.googleapis.com`: URL thô `https://claude.googleapis.com/v1/projects/<p>/locations/global/workspaces/<ws>/invoke/v1/messages` + `Authorization: Bearer <token Google>` + header `anthropic-version: 2026-10-21`, thân như Claude API — chép từ ví dụ cURL trang Anthropic *Claude Models on Google Cloud* 24/11 (ví dụ ấy dùng `gcloud auth application-default print-access-token`; script dùng `gcloud auth print-access-token`) | lời gọi thử Cloud Shell ĐỎ `authentication_error` ⇒ đổi sang token ADC; SDK (§B) ⛔ ảnh hưởng (SDK tự dựng URL) |
| G2 | Mã lỗi `claude.googleapis.com`: thiếu vai/API ⇒ 403 `permission_error`; workspace sai ⇒ 404 `not_found_error`; mô hình ⛔ được dùng ⇒ 400 `invalid_request_error` | chỉ đổi CHỮ dòng "trạng thái lỗi"; ĐẠT/ĐỎ ⛔ đổi |
| G3 | Tài khoản Owner CẦN `roles/claude.user` riêng để gọi (skill: *"The identity making calls needs `roles/claude.user`"*) | `--cap-nguoi` thừa nhưng vô hại |
| G4 | Đường dẫn Marketplace in ở bước ③ (`…/marketplace/product/anthropic/claude`) | script in đường thay: Marketplace → "Claude" |
| G5 | Thân đáp có trường `model` = mã trần đã gọi (cả đường SDK) | mục "mô hình trả về" ĐỎ + adapter ném `LoiApi … ≠ ghim` — chủ gửi BÁO CÁO, Dev nới so khớp có tên |
| G6 | VM `fls-staging-app` (bước 03) có `python3` + `curl` (Debian 12) và phạm vi `cloud-platform` (03 tạo với `--scopes=cloud-platform` — đọc mã nhánh `isp/STG` `03_dung_app.sh:152`) | mục VM ĐỎ có tên |
| G7 | Cloud Shell có ADC dùng được cho SDK (`google.auth.default()`) | `LoiApi: DefaultCredentialsError …` ⇒ `gcloud auth application-default login` |
| G8 | Tài khoản chủ xem được 2 workbook nguồn (cách `FLS_SHEETS_TOKEN`) | dùng cách tệp khoá SA đọc-sheet |
| G9 *(vertex)* | bật Claude ở Model Garden là BẤM TAY; mã lỗi chưa bật 400 `FAILED_PRECONDITION`; `anthropic_version: "vertex-2023-10-16"` trong thân được nhận (trang Anthropic: *"vertex-2023-10-16 or … 2026-10-21"*) | như G2 |

## E · Câu chủ

- **C1 · dữ liệu trên `claude.googleapis.com` (thay `FLS_ZDR_DA_BAT`).** Tra 24/11 (skill `claude-api`, `google-cloud-anthropic-managed`): nền do **Anthropic vận hành**, truy cập qua project GCP (IAM + hoá đơn GCP). Việc dựng tạo **một tổ chức Anthropic MỚI**, *"A Zero Data Retention arrangement doesn't carry over"*. ⇒ Trước khi đặt `FLS_GC_DU_LIEU_XAC_NHAN=1`, chủ xác nhận: **(1)** project là `fp-a-project` của công ty; **(2)** chấp nhận chế độ giữ dữ liệu MẶC ĐỊNH của tổ chức Anthropic mới (theo điều khoản gói Marketplace) **hoặc** đã xin ZDR cho tổ chức ấy. Khuyến nghị: chấp nhận cho test e2e staging; xin ZDR song song trước khi chạy định kỳ (quyết 23/11 *agent đọc toàn bộ nội dung + số TK* đi kèm điều kiện ZDR). *(Đường Vertex dự phòng: Google quản dữ liệu; request-response logging mặc định TẮT; ZDR đối tác xin qua account team Google — trang `data-governance` ⛔ có câu riêng về Claude.)*
- **C2 · workspace ID** là định danh của tổ chức Anthropic — tôi coi là NHẠY: chỉ ở biến môi trường (Cloud Shell) / Secret Manager, ⛔ commit, BÁO CÁO in che. Chủ đồng ý? Nếu muốn app staging gọi tự động, đề xuất lưu Secret Manager `fls-staging-claude-workspace` (phiếu sau).

## F · Cổng (dán thật — container cloud, cụm PG 16 cổng **5437**)

_điền ở commit kế sau `--duong-nen`_

## G · Phát hiện / ghi chú cho R1

1. **Đ1 — `vertex` / `claude.googleapis.com` trước WO-359**: WO khai `git grep -i vertex` trên `docs/ fls/ tools/` = **0**. Nay mã sống ở `fls/agent/mo_hinh.py` · `tools/staging/06_vertex_agent.sh` · `tools/vong_that_voi.py` · `tools/chay_agent_voi.py` · `tools/sinh_the_agent.py` + 4 thẻ.
2. **Tên tệp `06_vertex_agent.sh` giữ theo WO** dù đường chính nay là `claude.googleapis.com` — đổi tên là việc của phiếu (tránh lệch WO ↔ repo).
3. **Thẻ eval của BA** (`05_FleetEval/eval-cards/_chung.md` · `a4-soat.md`) — BG-356 phát hiện #3 vẫn mở (Gemini / "khác họ"); nay thêm: đường vận hành `claude.googleapis.com`, ⛔ bảng giá ⇒ cột chi phí thẻ eval cần BA cập nhật. Dev ⛔ sửa spec.
4. **Mặc định đổi** `FLS_NHA_CUNG_CAP` vắng ⇒ `google-cloud` (trước: `anthropic`). Bài WO-329/WO-355 đo đường khoá nay chọn RÕ `FLS_NHA_CUNG_CAP=anthropic` (`test_mo_hinh.py` · `test_mo_hinh_that.py` — sửa cùng commit, lý do ghi tại chỗ). Họ khác `anthropic` (vd `openai` chừa chỗ) ⛔ chịu luật đường — giữ chốt khoá của họ.
5. `NhatKyGoi.dict()` +2 khoá (`duong` · `vung`) — bài ghim tập khoá WO-355 cập nhật cùng commit (14 trường).
6. `AnthropicMessages.__init__` nhận `moi_truong` (tiêm được) và **từ chối** dựng khi `FLS_NHA_CUNG_CAP` ≠ đường của lớp ⇒ ⛔ ai dựng thẳng lớp khoá khi cấu hình nói đường GCP.
7. `requirements.txt`: `anthropic[google_cloud,vertex]>=2.12`; venv container đã cài `2.13.0` với cả hai phần thêm.
8. Bể dựng ở Cloud Shell có **muối riêng** (`~/.fls_muoi_be`) ⇒ vân tay ≠ `DEM_BE.json` trong repo — đúng thiết kế `HELD-R1-05`; ⛔ commit `DEM_BE.json` sinh ở Cloud Shell.
9. `kiem_so_song.py` gọi cứng `.venv/Scripts/lint-imports.exe` (đường Windows) — ở container Linux tôi đặt symlink cục bộ (`.venv` gitignore) để đo được.
