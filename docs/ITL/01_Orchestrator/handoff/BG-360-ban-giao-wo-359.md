# BG-360 — bàn giao `WO-359` · 4 agent Voi gọi Claude qua **Vertex AI** (`fp-a-project`) + script staging 06 + khối lệnh e2e

| | |
|---|---|
| **Thuộc** | `WO-359` |
| **Phát bởi** | `fls-dev` · 2026-11-24 |
| **Nhận** | `fls-test` (R1 → `KQ-361`) · CHỦ (chạy trên GCP — §A) |
| **Nhánh** | `claude/bold-galileo-zukpaf-isp/AG3` · SHA mã **`3ccbe6b`** (BG ở commit kế) |
| **Kho thật** | `KHONG_CHAM` (G0 BÓNG) · **0** lời gọi mô hình thật từ phiên này (Claude ⛔ vào GCP — quyết chủ 20/11) |

## A · Chủ làm gì, theo thứ tự

Tất cả trong **Google Cloud Shell** của project `fp-a-project`, ở bản sao repo đã `git fetch` + `git checkout claude/bold-galileo-zukpaf-isp/AG3` (ngọn ≥ `3ccbe6b`). Mỗi bước: **mong** · **gửi lại phần nào**. ⛔ dán token/khoá/nội dung trả lời vào chat — script ⛔ in chúng.

| # | Lệnh | Mong | Gửi lại |
|---|---|---|---|
| **1** | `bash tools/staging/06_vertex_agent.sh --project fp-a-project --kiem` | đo NỀN, ⛔ ghi gì. Mong **ĐỎ** ở: API `aiplatform` · IAM của SA · 8 mục gọi thử (chưa bật gì) — đó là trạng thái trước, ⛔ lỗi | khối `BÁO CÁO` (từ dòng `── BÁO CÁO` tới hết) |
| **2** | `bash tools/staging/06_vertex_agent.sh --project fp-a-project` | ① bật `aiplatform.googleapis.com` ② cấp `roles/aiplatform.user` cho SA `fls-staging-app` ③ IN 2 đường dẫn Model Garden. BÁO CÁO: API + IAM **ĐẠT**; gọi thử còn **ĐỎ** nếu Model Garden chưa bật (trạng thái lỗi Google in kèm, vd `FAILED_PRECONDITION`/`PERMISSION_DENIED`/`NOT_FOUND`) | khối `BÁO CÁO` |
| **3** | **BẤM TAY** — mở 2 đường dẫn script in (`…/vertex-ai/publishers/anthropic/model-garden/claude-opus-5-5?project=fp-a-project` và `…/claude-sonnet-5-5…`) ⇒ **Enable** / chấp nhận điều khoản Anthropic. Đường dẫn ⛔ mở ⇒ Vertex AI → Model Garden → tìm "Claude". | cả **Claude Opus 5.5** và **Claude Sonnet 5.5** ở trạng thái đã bật | ảnh chụp ⛔ cần — bước 4 đo |
| **4** | `bash tools/staging/06_vertex_agent.sh --project fp-a-project --kiem` | **`KẾT: ĐẠT` — 13/13 mục** = project công ty · API · IAM SA · VM chạy bằng SA · VM có phạm vi `cloud-platform` · 2 danh tính (Cloud Shell người chạy · TRONG VM bằng SA) × 2 mô hình × (HTTP `200` + mô hình trả về = mã ghim). Kèm số token vào/ra + USD ước của 4 lời gọi thử (~0,0005 USD) | khối `BÁO CÁO` |
| **5** | **Trả lời câu chủ C1–C2** (§E) rồi chạy khối lệnh e2e **(a) TẬP NHỎ** ở §B | `KẾT: ĐẠT` · exit **0** · A4 **4/4** · **0** ca phải-để-người bị nối · `đường vertex · vùng global` · USD ≤ trần **2** | tệp `docs/ITL/06_Agent/vong_that/REPORT_GIA_THAT.md` (CHỈ số đếm + vân tay) + dòng `API THẬT: … USD` |
| **6** | Xem chi phí (a) trên **Billing GCP** (Vertex AI · Claude) ⇒ nếu ổn, chạy **(b) BỂ A/B** ở §B | `KẾT: ĐẠT` · bảng (b) có số ở cả 4 cột · 0 ca phải-để-người bị nối ở bể A và B · USD ≤ trần **6** | `REPORT_GIA_THAT.md` mới + số USD Billing (để đối chiếu với ƯỚC) |

> ⚠ Nếu bước 5/6 ĐỎ `LoiApi: DefaultCredentialsError (xác thực GCP/ADC …)` ⇒ chạy `gcloud auth application-default login` rồi chạy lại. ĐỎ `LoiApi: … HTTP 403/404` ⇒ quay lại bước 4 (mô hình/IAM). ĐỎ `VuotTran` ⇒ chuỗi DỪNG đúng trần — gửi lại report, ⛔ nâng trần khi chưa xem Billing.

## B · Khối lệnh e2e (Cloud Shell) — dán nguyên

```bash
cd ~/FLS-tobe && git fetch origin claude/bold-galileo-zukpaf-isp/AG3 && git checkout claude/bold-galileo-zukpaf-isp/AG3
python3 -m venv ~/.fls-agent-venv && ~/.fls-agent-venv/bin/pip install -q -r requirements.txt   # có anthropic[vertex]
PY=~/.fls-agent-venv/bin/python

# ── đường gọi: Claude trên Vertex AI của project công ty (⛔ khoá sk-ant) ──
export PYTHONUTF8=1 FLS_NHA_CUNG_CAP=vertex FLS_GCP_PROJECT=fp-a-project FLS_VERTEX_REGION=global
export FLS_CHO_GOI_API=1
export FLS_VERTEX_DU_LIEU_XAC_NHAN=1     # ⛔ đặt trước khi trả lời câu chủ C1 (§E) — đây là lời XÁC NHẬN của người vận hành

# ── bể giữ riêng từ NGUỒN SỐNG — NGOÀI repo (dir 700) ──
export FLS_HELDOUT_NOI_DUNG=$HOME/fls_heldout && mkdir -p -m 700 "$FLS_HELDOUT_NOI_DUNG"
[ -f ~/.fls_muoi_be ] || (umask 077; openssl rand -hex 16 > ~/.fls_muoi_be)   # muối vân tay BỀN qua các lần dựng
export FLS_MUOI_BE=$(cat ~/.fls_muoi_be)
# quyền ĐỌC sheet — chọn MỘT: tệp khoá SA đọc-sheet (chmod 600, XOÁ sau)  HOẶC  token tài khoản chủ (~60 phút)
export FLS_SHEETS_SA_JSON_TEP=$HOME/sa_doc_sheet.json
# export FLS_SHEETS_TOKEN=$(gcloud auth print-access-token --scopes=https://www.googleapis.com/auth/spreadsheets.readonly)
$PY tools/dung_be_giu_rieng.py --doc-song --tho /tmp/fls_be_tho/nguon.json      # mong: "bể a: 65/65 ca · thiếu không" · "bể b: 70/70 ca · thiếu không" (số BG-356)
unset FLS_SHEETS_TOKEN

# ── (a) TẬP NHỎ: 12 ca dựng + ≤ 20 ca bể B — chạy TRƯỚC, xem chi phí ──
$PY tools/vong_that_voi.py --that --tran-usd 2 --ghi
#   mong: exit 0 · "**KẾT: ĐẠT**" · "| đường gọi thật | `vertex` …" · "Sau tập nhỏ (a): N lời gọi · ~X USD"

# ── (b) BỂ A/B — CHỈ sau khi xem chi phí (a) trên Billing ──
$PY tools/vong_that_voi.py --that --be --tran-usd 6 --ghi

# ── dọn ──
rm -rf /tmp/fls_be_tho ; rm -f $HOME/sa_doc_sheet.json      # bể ~/fls_heldout GIỮ (dùng lại cho vòng sau)
```

- **Danh tính gọi mô hình ở §B** = tài khoản CHỦ trong Cloud Shell (ADC của Cloud Shell; quyền Owner có `aiplatform.endpoints.predict`). **Danh tính SA `fls-staging-app`** (cái app staging dùng) được đo riêng ở bước 4 (gọi thử TRONG VM). Chạy chuỗi agent TRONG VM cần dựng môi trường Python trong VM — ⛔ làm ở `WO-359`, đề xuất phiếu sau nếu chủ muốn.
- **G0 BÓNG**: `vong_that_voi.py` ⛔ mở kho (đo: chạy trọn với `PG_DSN` **gỡ khỏi** môi trường ⇒ report sinh bình thường, exit theo chốt); mọi công cụ agent chỉ đọc ảnh/tệp đo trong repo + bể ngoài repo ⇒ ⛔ chạm Cloud SQL staging.
- Report ghi vào bản sao repo ở Cloud Shell (CHỈ số + vân tay — luật WO-355). **⛔ commit từ Cloud Shell**: chủ gửi lại nội dung `.md`, phiên Dev/Test đối chiếu.

## C · Bảng AC → bằng chứng

| AC | Mong | Kết | Bằng chứng |
|---|---|---|---|
| AC-1 · nhà cung cấp Vertex | đường `anthropic-vertex` (`AnthropicVertex`, `project_id` · `region`, mã Vertex Opus/Sonnet 5.5, vùng hỗ trợ); chọn bằng `FLS_NHA_CUNG_CAP=vertex` · `FLS_GCP_PROJECT` · `FLS_VERTEX_REGION`; ADC/SA; giữ API-key dự phòng | **ĐẠT** (SDK GIẢ, ⛔ mạng) | `fls/agent/mo_hinh.py`: `AnthropicVertexMessages` (`ten = "anthropic-vertex"`) dựng `anthropic.AnthropicVertex(project_id=…, region=…, max_retries=…)` — chữ ký đối chiếu trên SDK THẬT **`anthropic` 2.13.0** (`region` · `project_id` · `access_token` · `credentials` · `max_retries`…; bài `test_AC1_chu_ky_lop_SDK_that__…`); `ADAPTER_DUONG` chọn theo `duong_goi()`; biến vắng ⇒ `AnthropicMessages` (WO-355 nguyên). Mã Vertex = mã TRẦN `claude-opus-5-5` / `claude-sonnet-5-5` (tra trang Anthropic *Claude Models on Google Cloud (Google managed)* §API model IDs 24/11). Vùng nhận `global` (mặc định) · `us` · `eu`; vùng đơn ⇒ `CamGoiThat` vì *"Regional endpoints serve Claude Sonnet 4.6 and earlier models only"*. Chuỗi 4 agent chạy TRỌN trên đường vertex (SDK giả) ⇒ A4 **4/4**, mọi lời gọi `claude-opus-5-5`, nhật ký `duong = vertex` (bài `test_AC1_chuoi_4_agent__chay_tron_tren_vertex`) |
| AC-2 · chốt + chi phí | 3 chốt + trần giữ; bỏ đòi khoá ở vertex; THAY `FLS_ZDR_DA_BAT` bằng xác nhận hợp Vertex (chính sách TRA, ⛔ đoán); nhật ký token + USD (giá Vertex, ngày tra) | **ĐẠT** + **câu chủ C1** | Chốt chung giữ: `--that` · `FLS_CHO_GOI_API=1` · ghim (bài tham số hoá). Đường vertex: ⛔ đòi `ANTHROPIC_API_KEY` (bài chạy với khoá VẮNG) · đòi `FLS_GCP_PROJECT` ∈ `DU_AN_CONG_TY` · vùng hợp lệ · chế độ `mo` đòi **`FLS_VERTEX_DU_LIEU_XAC_NHAN=1`** — `FLS_ZDR_DA_BAT=1` ⛔ thay được (bài `test_AC2_ZDR_cu_KHONG_thay_duoc_…`). Trần USD giữ (`VuotTran` ở lời thứ 3 khi trần 5, mỗi lời ~4 USD). Nhật ký +2 trường `duong` · `vung`; `ngay_tra_gia` = **2026-11-24** trên vertex. Giá: §D. Lỗi `google.auth` ⇒ `LoiApi` CÓ TÊN, ⛔ lộ đường dẫn tệp ADC; lỗi khác ném nguyên (2 bài). Chính sách dữ liệu: §E C1 |
| AC-3 · script GCP cho CHỦ | `06_vertex_agent.sh --project fp-a-project [--kiem]`: bật API · Model Garden (bấm tay — ghi rõ) · `roles/aiplatform.user` cho SA · gọi thử 1 lời/mô hình ⇒ BÁO CÁO có `mong`, ĐỎ hai chiều, ⛔ in khoá/token | **ĐẠT** (gcloud + curl GIẢ có trạng thái) | `tools/staging/06_vertex_agent.sh` + **18** bài `tests/agent/test_06_vertex_agent.py` với `tests/agent/vertex_gia.py` (một tệp, hai tên `gcloud`/`curl`; lệnh TRONG VM được **chạy thật bằng bash** — gcloud giả thi hành `--command` với `curl` giả + metadata server giả). Đo: dựng từ trống ⇒ ĐỎ **đúng 8** mục gọi thử (Model Garden chưa bật) · "bấm" xong ⇒ **13/13 ĐẠT** · chạy 3 lần ⇒ IAM **1** binding · `--kiem` **0** lệnh ghi · 6 phép phá ⇒ ĐÚNG tập mục ĐỎ · `--khong-goi-thu` ⇒ 8 mục ĐỎ (Đ5) · tham số xấu ⇒ exit 2 trước MỌI lệnh · 4 lính canh (token người · token SA · nội dung trả lời · thông điệp lỗi) **0** lần trong đầu ra |
| AC-4 · test e2e trên staging | lệnh CHỦ chạy: dựng bể giữ riêng từ nguồn sống (ngoài repo) ⇒ chuỗi 4 agent THẬT (tập nhỏ ⇒ xem chi phí ⇒ bể A/B) ⇒ report MỘT trang GIẢ ↔ THẬT; G0 BÓNG | **ĐẠT phần mã + khối lệnh** · số THẬT **chờ chủ** (§A bước 5–6) | §B. `vong_that_voi.py` ghi `đường gọi thật` + `đường · vùng` + ngày tra giá Vertex vào report; thiếu chốt vertex ⇒ exit **2** `thiếu FLS_GCP_PROJECT (đường vertex)` (bài); đủ chốt + SDK giả ⇒ exit **0** `KẾT: ĐẠT` (bài). `dung_be_giu_rieng.py` nay đọc sheet bằng `FLS_SHEETS_TOKEN` / `FLS_SHEETS_SA_JSON_TEP` (Cloud Shell, ⛔ cần secret phiên cloud), phạm vi CHỈ `spreadsheets.readonly` (bài). Report trong repo hiện tại = lượt KHÔNG chốt (đường API, thiếu khoá) — sinh lại bởi `--ghi` ở `3ccbe6b`, ⛔ số THẬT |
| AC-5 · an toàn | ⛔ nội dung/phản hồi thô vào repo; ⛔ khoá; `quet_pii_repo` 0; đọc toàn bộ nội dung + số TK chỉ trong GCP công ty | **ĐẠT** | `DU_AN_CONG_TY = ("fp-a-project",)` — project khác ⇒ `CamGoiThat` (3 bài: dự án cá nhân · `fpa-t-494007` (project của SA máy chủ cũ) · `fp-a-project-x`); 06 có mục `project = GCP công ty` mong `fp-a-project`. Nhật ký: ⛔ `"lam di"` · ⛔ `0123456789` (STK giả trong yêu cầu) · ⛔ khoá (bài). Script 06: token chỉ ở biến + tệp 600, header đọc `@tệp` (⛔ lộ ở `ps`), thân trả lời → tệp tạm → CHỈ in `model`/`stop_reason`/số token, xoá ngay. `quet_pii_repo` **0** chỗ · 0 tệp (§F) |
| AC-6 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit); `kiem_tai_lieu` · `lint-imports` | xem §F | sàn `MONG_PYTEST_TOAN_BO` **5020 → 5072** = thu thập thật (`pytest --collect-only` ⇒ **5072 tests collected**; +34 `test_mo_hinh_vertex.py` · +18 `test_06_vertex_agent.py`; web **690** giữ) + `tests/test_dung_moi_truong_isp.py` cùng commit |

**Bài mới đã CHỨNG MINH ĐỎ** (phá nguồn → chạy → xem cắn → trả nguyên; `cmp` xác nhận mỗi phép phá ĂN vào tệp):

| phá | bài | đỏ |
|---|---|---|
| `mo_hinh`: vertex dựng `sdk.Anthropic` (đường khoá) | `test_mo_hinh_vertex.py` | **3** / 31 |
| `mo_hinh`: thêm `asia-southeast1` vào `VUNG_VERTEX` | ″ | **2** / 31 |
| `mo_hinh`: bỏ chốt `DU_AN_CONG_TY` | ″ | **3** / 31 |
| `mo_hinh`: bỏ chốt `FLS_VERTEX_DU_LIEU_XAC_NHAN` | ″ | **2** / 31 |
| 06: `cat` tệp header (lộ token) | `test_06_vertex_agent.py` | **11** / 18 |
| 06: bỏ lệnh cấp IAM | ″ | **12** / 18 |
| 06: host đa vùng sai (`<vùng>-aiplatform`) | ″ | **2** / 18 |
| 06: BÁO CÁO luôn `ok = True` | ″ | **11** / 18 |
| 06: mục phạm vi VM luôn `True` | ″ | **2** / 18 |
| 06: bỏ header `Metadata-Flavor` (VM ⛔ lấy được token) | ″ | **11** / 18 |

*(4 phép phá `mo_hinh` chạy khi tệp còn 31 bài; sau đó thêm 3 bài AC-4 ⇒ 34.)*

## D · Giá Vertex (tra 2026-11-24) — và GIẢ ĐỊNH CHƯA KIỂM

- **Tra được (Anthropic `about-claude/pricing`, 24/11):** Claude API: Opus 5.5 **$4** vào · **$5** ghi cache 5' · **$0,20** đọc cache · **$20** ra; Sonnet 5.5 **$2 · $2,50 · $0,10 · $10** — khớp `BANG_GIA` **8/8** ô. Vertex: *"For official pricing on Claude Models on Google Cloud (Google managed) … visit cloud.google.com/vertex-ai/generative-ai/pricing#claude-models"* và *"Regional and multi-region endpoints include a 10 percent premium over global endpoints"* (Claude 4.5 trở đi).
- ⚠ **GIẢ ĐỊNH CHƯA KIỂM #1 — giá global Vertex = giá Claude API.** Trang giá Google trả nội dung RỖNG cho phiên này (⛔ đọc được bảng); vài trang tổng hợp bên thứ ba ghi Opus 5.5 Vertex global $4/$20 · đa vùng $4,40/$22 — khớp giả định, nhưng ⛔ là nguồn chính thức. ⇒ `BANG_GIA_VERTEX` = `BANG_GIA` × hệ số vùng (`global` 1,0 · `us`/`eu` 1,1). USD in ra là ƯỚC; **Billing GCP là số thật** — chủ gửi lại ở bước 6 để đối chiếu.
- ⚠ **Batches API ⛔ có trên Vertex** (trang Anthropic §Features not supported) ⇒ mức −50 % của fleet eval theo lô (thẻ agent 23/11) **mất** trên đường Vertex; fleet eval gửi TỪNG lời. Thẻ agent đã sửa câu này.

**Giả định GCP khác chưa kiểm** (bài GIẢ mô phỏng theo chúng; script **chỉ so `HTTP == 200`** + `model` ⇒ ⛔ phụ thuộc mã lỗi cụ thể):

| # | Giả định | Nếu sai thì |
|---|---|---|
| G1 | Bật Claude ở Model Garden là bước BẤM TAY (chấp nhận điều khoản đối tác) — ⛔ tìm thấy lệnh gcloud chính thức | chủ báo; thêm lệnh vào 06 |
| G2 | Đường dẫn `console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/<mã>?project=…` mở đúng thẻ mô hình | script đã in đường thay: Vertex AI → Model Garden → "Claude" |
| G3 | Mã lỗi: chưa bật Model Garden ⇒ 400 `FAILED_PRECONDITION`; thiếu IAM ⇒ 403 `PERMISSION_DENIED`; API tắt ⇒ 403 `SERVICE_DISABLED`; VM thiếu phạm vi ⇒ 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT` | chỉ đổi CHỮ ở dòng "trạng thái lỗi Google"; ĐẠT/ĐỎ ⛔ đổi |
| G4 | Thân đáp `:rawPredict` có trường `model` = mã trần đã gọi (cả đường SDK) | mục "mô hình trả về" ĐỎ + adapter ném `LoiApi … ≠ ghim` — chủ gửi BÁO CÁO, Dev nới so khớp có tên |
| G5 | `anthropic_version: "vertex-2023-10-16"` trong thân được chấp nhận cho Opus/Sonnet 5.5 (trang Anthropic: *"Set it to `vertex-2023-10-16` or to API version `2026-10-21`"*) | lời gọi thử 400 `INVALID_ARGUMENT` ⇒ đổi sang `2026-10-21` |
| G6 | VM `fls-staging-app` (bước 03) có `python3` + `curl` (Debian 12) và phạm vi `cloud-platform` (03 tạo với `--scopes=cloud-platform` — đọc mã nhánh `isp/STG` `03_dung_app.sh:152`) | mục VM ĐỎ có tên |
| G7 | Cloud Shell có ADC dùng được cho SDK (`AnthropicVertex` → `google.auth.default()`) | `LoiApi: DefaultCredentialsError …` ⇒ `gcloud auth application-default login` |
| G8 | Tài khoản chủ xem được 2 workbook nguồn (cách `FLS_SHEETS_TOKEN`) | dùng cách tệp khoá SA đọc-sheet |

## E · Câu chủ

- **C1 · dữ liệu trên Vertex (thay `FLS_ZDR_DA_BAT`).** Đã tra 24/11: trang Anthropic — *"Google Cloud governs data handling for Claude Models on Google Cloud (Google managed)"*; trang Google `vertex-ai/generative-ai/docs/data-governance` — ⛔ huấn luyện trên dữ liệu khách khi chưa được phép (áp cho mọi mô hình managed) · *request-response logging "is disabled by default"*, muốn ZDR thì *"do not enable this feature"* · ZDR cho mô hình ĐỐI TÁC phải **xin qua account team** (trang chỉ tả quy trình cho OpenAI, **⛔ một câu riêng về Claude**) · các *Advanced AI features* có thể ghi log thêm. ⇒ Trước khi đặt `FLS_VERTEX_DU_LIEU_XAC_NHAN=1`, chủ xác nhận: **(1)** project là `fp-a-project` của công ty; **(2)** request-response logging cho mô hình Claude **đang TẮT** trên project; **(3)** chấp nhận chế độ giữ dữ liệu theo điều khoản GCP hiện tại **hoặc** đã xin ZDR qua account team Google. Khuyến nghị: chấp nhận (1)+(2) cho test e2e staging; xin ZDR song song trước khi chạy định kỳ.
- **C2 · vùng.** Mặc định `global` (rẻ nhất, khuyên dùng; dữ liệu có thể xử lý ở bất kỳ vùng có năng lực). Muốn giữ trong Mỹ/EU ⇒ `--region us` / `FLS_VERTEX_REGION=us` (+10 %). Vùng Singapore (`asia-southeast1`) **⛔ phục vụ** Opus/Sonnet 5.5. Khuyến nghị: `global`.

## F · Cổng (dán thật — container cloud, cụm PG 16 cổng **5437**, SHA `3ccbe6b`)

| cổng | kết | dán |
|---|---|---|
| `--duong-nen` | _điền sau_ | _điền sau_ |
| `pytest tests/agent` | **ĐẠT** | `185 passed in 78.37s` |
| `kiem_tai_lieu.py` | **ĐẠT** | `✅ cong tai lieu DAT — va no da do duoc that (520 file, 3066 bang, 986 o ngay, 104 ma QD)` |
| `lint-imports` | **ĐẠT** | `Contracts: 11 kept, 0 broken.` |
| `quet_pii_repo.py` | **ĐẠT** | `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` |
| `soi_bang_tuyen.py` | **ĐẠT** | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
| `kiem_thuyet_minh.py` | **ĐẠT** | `✅ CONG THUYET MINH DAT — 35/35 nut co mat trong CA 2 ban` |
| `pg_migrate` | **ĐẠT** | `khong co gi de ap` · `pg_verify: khop` |
| `khop_owner.py --kiem` | **ĐỎ — có sẵn, ⛔ do WO-359** | `A1 · B1 · C6 ⛔ DOI TRANG THAI: mong KHOP, do duoc LECH` · exit **1**. Chạy trên cây GỐC (`git stash -u` ⇒ ngọn `93f3e5a`) cho đầu ra **giống từng byte** (`diff` rỗng) ⇒ do kho 5437 của container RỖNG (chưa nạp), ⛔ do thay đổi này |
| `kiem_so_song.py` | **⛔ ĐO ĐƯỢC — ĐỎ (môi trường)** | `⛔ khong do duoc: kho ⛔ khong co dau thoi diem cua lan nap / anh chup — cong ⛔ khong duoc phep xanh` · exit **1** (kho trống). *(Công cụ gọi cứng `.venv/Scripts/lint-imports.exe` (Windows) — tôi đặt symlink cục bộ `.venv/Scripts/lint-imports.exe → ../bin/lint-imports`, `.venv` gitignore)* |

## G · Phát hiện / ghi chú cho R1

1. **Đ1 — "vertex" trước WO-359**: WO khai `git grep -i vertex` trên `docs/ fls/ tools/` = **0**. Sau `3ccbe6b`: mã sống ở `fls/agent/mo_hinh.py` · `tools/staging/06_vertex_agent.sh` · `tools/vong_that_voi.py` · `tools/chay_agent_voi.py` · `tools/sinh_the_agent.py` + 4 thẻ.
2. **Thẻ eval của BA** (`05_FleetEval/eval-cards/_chung.md` · `a4-soat.md`) — BG-356 phát hiện #3 vẫn mở (Gemini / "khác họ"); nay thêm: đường vận hành là Vertex, **⛔ Batches** ⇒ cột chi phí thẻ eval cần BA cập nhật. Dev ⛔ sửa spec.
3. `NhatKyGoi.dict()` +2 khoá (`duong` · `vung`) — bài ghim tập khoá của WO-355 cập nhật cùng commit (14 trường).
4. Lớp `AnthropicMessages.__init__` nay nhận `moi_truong` (tiêm được) và **từ chối** dựng khi `FLS_NHA_CUNG_CAP` ≠ đường của lớp ⇒ ⛔ ai dựng thẳng lớp khoá khi cấu hình nói vertex (bài `test_AC2_adapter_sai_duong__CamGoiThat`).
5. `requirements.txt`: `anthropic[vertex]>=2.12` (kéo `google-auth`); venv container đã cài `anthropic[vertex]==2.13.0`.
6. Bể dựng ở Cloud Shell có **muối riêng** (`~/.fls_muoi_be`) ⇒ vân tay bể ≠ `DEM_BE.json` trong repo (muối dẫn từ secret phiên cloud) — đúng thiết kế `HELD-R1-05`; ⛔ commit `DEM_BE.json` sinh ở Cloud Shell.
