# BG-368 — bàn giao `WO-367` · 4 agent Voi gọi mô hình qua **OpenRouter** + **fleet eval đa mô hình** tự động

| | |
|---|---|
| **Thuộc** | `WO-367` |
| **Phát bởi** | `fls-dev` · 2026-11-27 |
| **Nhận** | `fls-test` (R1 → `KQ-369`) · CHỦ (Cloud Shell — §A/§B) |
| **Nhánh** | `claude/bold-galileo-zukpaf-isp/OR` · nền `6f996cf` · SHA đo: xem §F |
| **Kho thật** | `KHONG_CHAM` (G0 BÓNG) · **0** lời gọi API thật từ phiên này (luật WO: CHỦ chạy) · **0** lệnh GCP |

**Một câu:** đường thứ tư `FLS_NHA_CUNG_CAP=openrouter` (`OpenRouterChat`, `POST https://openrouter.ai/api/v1/chat/completions` bằng `requests`, DỊCH sang khuôn Messages nội bộ) + chốt MỚI `FLS_OPENROUTER_DU_LIEU_XAC_NHAN=1` + định tuyến `{"data_collection": "deny", "zdr": true}` ở MỌI lời gọi + USD lấy từ `usage.cost` OpenRouter trả (nhãn **THẬT**; thiếu ⇒ **ƯỚC**) + cấu hình mô hình MỘT chỗ `fls/agent/openrouter_mo_hinh.json` + `fleet_eval_voi.py --ma-tran` (ứng viên × bể A/B, chấm bằng MÃ) + script chủ `tools/staging/09_openrouter_agent.sh`. **AC-7 (cổng MCP) ⛔ làm** — AC-4 chứng minh fleet eval TỰ ĐỘNG được (§C).

## Nguồn đã tra (2026-11-27 — mạng phiên TỚI được `openrouter.ai`, 0 giả định ở URL/header/trường)

| hằng (mã) | nguồn | trích |
|---|---|---|
| `GOC_API_OPENROUTER` = `https://openrouter.ai/api/v1` + `/chat/completions` | `openrouter.ai/docs/api_reference/overview.md` | `fetch('https://openrouter.ai/api/v1/chat/completions', …)` |
| header `Authorization: Bearer <khoá>`; ⛔ gửi `HTTP-Referer`/`X-OpenRouter-Title` (tuỳ chọn, chỉ xếp hạng app) | `…/api_reference/authentication.md` · `overview.md` | *"Send one credential per request in the Authorization header as Bearer"* · *"Optional. Site URL for rankings"* |
| `DINH_TUYEN_OPENROUTER` = `provider: {"data_collection": "deny", "zdr": true}` | `…/guides/routing/provider-selection.md` · `…/guides/features/zdr.md` | `deny`: *"use only providers which do not collect user data"* · `zdr`: *"Restrict routing to only ZDR (Zero Data Retention) endpoints"* |
| ⛔ gửi `models` (rơi sang mô hình khác) | `…/guides/routing/model-fallbacks.md` | *"If the model you selected returns an error, OpenRouter will try to use the fallback model"* |
| `usage.cost` (USD THẬT) · `prompt_tokens` · `completion_tokens` · `prompt_tokens_details.cached_tokens` · `cache_write_tokens` | `…/cookbook/administration/usage-accounting.md` | *"`cost`: The total amount charged to your account"* · *"Full usage details are always included automatically"* (`usage: {include}` đã bỏ — ⛔ gửi) |
| `finish_reason` ∈ `tool_calls` · `stop` · `length` · `content_filter` · `error` ⇒ `DOI_FINISH` | `…/api_reference/overview.md` | *"OpenRouter normalizes each model's finish_reason to one of the following values"* |
| gửi lại `reasoning_details` NGUYÊN VẸN ở lượt sau | `…/guides/best-practices/reasoning-tokens.md` §Preserving Reasoning | *"Send the assistant turn back unmodified (including reasoning_details) plus the tool results"* |
| `TEN_LOI_OPENROUTER` 400/401/402/403/408/429/502/503 · `MA_THU_LAI` (⛔ 402) | `…/api_reference/errors-and-debugging.md` | *"402: … insufficient credits"* · *"429: You are being rate limited"* · *"503: no available model provider that meets your routing requirements"* · *"A 402 without the header is not a wait-and-retry case"* |
| lỗi giữa lúc sinh: HTTP 200 + `error` trong thân | cùng trang | *"errors during generation can still appear in the body of a 200 response"* |
| slug + giá + ngữ cảnh | `GET https://openrouter.ai/api/v1/models` (công khai) | **477** mô hình |
| điểm cuối ZDR mỗi slug | `GET https://openrouter.ai/api/v1/endpoints/zdr` (công khai) | **953** điểm cuối |
| `/api/v1/key` ⇒ `data.limit_remaining` (dùng ở 09) | `…/api/api-reference/api-keys/get-current-api-key.md` | `limit_remaining: 74.5` |

## A · Chủ làm gì, theo thứ tự (Cloud Shell `fp-a-project`)

**A0 · Đưa mã lên Cloud Shell bằng tarball** (máy Windows, PowerShell, bản sao `C:\Users\Admin\Downloads\FLS-i2`):
```powershell
cd C:\Users\Admin\Downloads\FLS-i2
git fetch origin claude/bold-galileo-zukpaf-isp/OR
git archive --format=tar.gz -o fls-or.tar.gz FETCH_HEAD
git rev-parse --short FETCH_HEAD        # ghi lại sha — mong = sha ở §F
```
Cloud Shell ⇒ menu ⋮ **Upload** ⇒ chọn `fls-or.tar.gz`, rồi:
```bash
rm -rf ~/fls-or && mkdir -p ~/fls-or && tar -xzf ~/fls-or.tar.gz -C ~/fls-or && rm ~/fls-or.tar.gz
cd ~/fls-or && python3 -m venv ~/.fls-agent-venv && ~/.fls-agent-venv/bin/pip install -q -r requirements.txt
```

| # | Việc | Mong | Gửi lại |
|---|---|---|---|
| **1** | Trả lời **C2** (§E) và bật ở `openrouter.ai/settings/privacy`: **tắt** mọi lựa chọn lưu prompt / cho huấn luyện; **bật** *ZDR* toàn tài khoản, chọn **"ZDR only"** (⛔ *Safety Retention*) | ảnh/ghi chú cài đặt | câu trả lời C2 |
| **2** | Tạo khoá ở `openrouter.ai/settings/keys` **có hạn mức** (vd 10 USD) · nạp credit | khoá chép vào clipboard — ⛔ dán chat | ⛔ gì |
| **3** | `export FLS_NHA_CUNG_CAP=openrouter` rồi `bash tools/staging/09_openrouter_agent.sh --project fp-a-project` — dán khoá khi hỏi (⛔ hiện chữ) | ① bật Secret Manager ② tạo `fls-staging-openrouter-key` ③ `secretAccessor` cho SA trên RIÊNG bí mật · BÁO CÁO **`KẾT: ĐẠT` — 14/14 mục có `mong`** = project · biến · khoá đọc được · ⛔ khoảng trắng · SA accessor · `/models` 200 · 2 slug còn · `/key` 200 · 2 mô hình × (HTTP 200 + mô hình trả về = slug ghim) · `usage.cost` đo được · ≤ trần 0,10 | khối `BÁO CÁO` |
| **4** | `bash tools/staging/09_openrouter_agent.sh --project fp-a-project --kiem` | như 3, ⛔ lệnh ghi | khối `BÁO CÁO` |
| **5** | §B (a) TẬP NHỎ ⇒ xem `usage.cost` + trang *Activity* OpenRouter ⇒ (b) bể A/B ⇒ (c) ma trận | `KẾT: ĐẠT` mỗi bước | 3 tệp report (CHỈ số) |

> ĐỎ có tên ở 3/4 ⇒ đọc nguyên nhân in cạnh mục: `HTTP 402 — HẾT CREDIT` (nạp) · `HTTP 429 — GIỚI HẠN TỐC ĐỘ` (đợi, chạy lại) · `HTTP 401 — khoá sai` (`--doi-khoa`) · `HTTP 503 — ⛔ nhà cung cấp ZDR + deny nào phục vụ` (cài đặt privacy chặn hết — kiểm bước 1) · `HTTP 400 — yêu cầu sai` (thử `--max-tokens 64` — §G giả định #1).

## B · Khối lệnh e2e (Cloud Shell) — dán nguyên

```bash
cd ~/fls-or && PY=~/.fls-agent-venv/bin/python
export PYTHONUTF8=1 FLS_NHA_CUNG_CAP=openrouter FLS_CHO_GOI_API=1
export OPENROUTER_API_KEY="$(gcloud secrets versions access latest --secret=fls-staging-openrouter-key --project=fp-a-project)"
export FLS_OPENROUTER_DU_LIEU_XAC_NHAN=1     # ⛔ đặt trước khi trả lời C2 — đây là lời XÁC NHẬN của người vận hành
unset ANTHROPIC_API_KEY FLS_GCP_PROJECT FLS_CLAUDE_WORKSPACE_ID

# ── bể giữ riêng NGOÀI repo (như BG-360 §B — giữ nguyên nếu ~/fls_heldout đã có) ──
export FLS_HELDOUT_NOI_DUNG=$HOME/fls_heldout
[ -f ~/.fls_muoi_be ] && export FLS_MUOI_BE=$(cat ~/.fls_muoi_be)
# (dựng lại: xem BG-360 §B — `tools/dung_be_giu_rieng.py --doc-song`)

# ── (a) TẬP NHỎ (12 ca dựng + ≤ 20 ca bể B) — TRẦN 2 USD ──
$PY tools/vong_that_voi.py --that --tran-usd 2 --ghi
#   mong: exit 0 · "**KẾT: ĐẠT**" · "| đường gọi thật | `openrouter` (OpenRouter — bên thứ ba …" · "Sau tập nhỏ (a): N lời gọi · ~X USD THẬT (usage.cost …)"

# ── (b) BỂ A/B (A2.04, Opus 5.5) — CHỈ sau khi xem chi phí (a) ──
$PY tools/vong_that_voi.py --that --be --tran-usd 6 --ghi

# ── (c) FLEET EVAL ĐA MÔ HÌNH — ma trận ứng viên × bể A/B (ứng viên = câu C1; vắng ⇒ 2 slug mặc định) ──
$PY tools/fleet_eval_voi.py --ma-tran --that --tran-usd 4 --tran-usd-mo-hinh 2 --ghi
#   thêm ứng viên C1: --ung-vien anthropic/claude-opus-5.5,anthropic/claude-sonnet-5.5,openai/gpt-6.2-sol
#   mong: exit 0 · "**KẾT: ĐẠT**" · mỗi ô có số · cột "USD + nguồn" = "THẬT (usage.cost OpenRouter trả)"

unset OPENROUTER_API_KEY
```
- Nhật ký lời gọi THẬT ghi LUÔN ở `docs/ITL/06_Agent/nhat_ky/` (CHỈ số + vân tay) — kể cả lượt DỪNG giữa chừng. **⛔ commit từ Cloud Shell**: gửi lại nội dung `.md`.
- Trần chặn lời gọi **KẾ** (⛔ cắt lời đang chạy — `AG2-R1-03`): một lời lớn có thể vượt trần một chút.

## C · Bảng AC → bằng chứng

| AC | Mong | Kết | Bằng chứng |
|---|---|---|---|
| **AC-1** đường `openrouter` | `DUONG_OPENROUTER` ∈ `DUONG_HOP_LE`; adapter dịch đúng hợp đồng; `openai` có adapter qua OR; khoá ⛔ repo/log/argv/báo cáo; biến vắng ⇒ `anthropic` | **ĐẠT** | `tests/agent/test_mo_hinh_openrouter.py` (36 bài · máy chủ GIẢ `127.0.0.1`, HTTP THẬT qua `requests`): vòng tool_use trọn 2 chiều + gửi lại `reasoning_details` · chuỗi 4 agent qua OR ⇒ A4 **4/4** · 7 mã HTTP ⇒ `LoiApi` CÓ TÊN, ⛔ `message`/khoá/số TK · 429/503 thử lại, 402 ⛔ · lỗi giữa lúc sinh / mô hình ≠ ghim / `arguments` hỏng ⇒ `LoiApi` **sau** khi ghi nhật ký · khoá ⛔ ở `repr`/thuộc tính/nhật ký/thân · grep **hình khoá** ngoài `tests/` = **0** tệp (bằng chứng dương: mẫu thấy khoá GIẢ ở `tests/`). Nghiệm thu `KQ-357`: xanh trọn (§F) |
| **AC-2** chốt + chi phí | thiếu từng chốt ⇒ 0 lời gọi; `provider` ZDR+deny mỗi lời; USD có nhãn nguồn | **ĐẠT** | 3 chốt × 3 chế độ che = **9** bài + `--that` vắng: mỗi bài đếm `tt.yeu_cau` trên MÁY CHỦ = **0** · `provider == {"data_collection": "deny", "zdr": true}` ở **2/2** lời · `usage.cost` ⇒ `THẬT` (= giá × token của máy chủ giả), bỏ `cost` ⇒ `ƯỚC`; `tong_nhat_ky.nguon_usd = {THẬT: 1, ƯỚC: 1}` · trần TỔNG + trần MÔ HÌNH chặn lời KẾ. Đường API giữ **12** khoá nhật ký |
| **AC-3** ma trận mô hình | MỘT chỗ; mặc định slug THẬT; ⛔ `google/*` | **ĐẠT** | `fls/agent/openrouter_mo_hinh.json`: vai `lam` = `anthropic/claude-opus-5.5` · `auditor` = `anthropic/claude-sonnet-5.5` (tra `/models` 27/11); giá **8/8** ô khớp `BANG_GIA` Claude API (hai nguồn); cả hai có điểm cuối ZDR (`amazon-bedrock` · `google-vertex/global`). Bài: ⛔ `google/` · bí danh `~…`/`latest` · biến thể `:nitro`/`:batch` · ngoài danh mục ⇒ `CamGoiThat`, 0 lời gọi · đổi vai trong tệp ⇒ agent đổi slug, ⛔ sửa mã |
| **AC-4** fleet eval tự động | ma trận ứng viên × bể; chấm ⛔ bằng mô hình; report 1 trang + so ngược; trần tổng + mô hình; nhật ký mọi lối thoát | **ĐẠT** | `fleet_eval_voi.py --ma-tran` · `tests/agent/test_fleet_ma_tran_openrouter.py` (10 bài): lượt GIẢ **trọn** 3 ứng viên × bể A/B = **6/6** ô chạy, 12 lời gọi, KẾT ĐẠT · phá luật của MỘT mô hình ⇒ CHỈ hàng ấy đổi, yêu cầu gửi đi giống nhau trừ `model` (chấm = MÃ `_cham_mu`) · trần TỔNG ⇒ ô sau `bo_qua` có tên (1 lời lọt) · trần MÔ HÌNH ⇒ chỉ mô hình ấy dừng · 402 ở một ô ⇒ ô khác vẫn chạy · thiếu chốt ⇒ mọi ô ĐỎ, **0** lời · nhật ký **3/3** lối thoát (trả về · ô lỗi · `KeyError` chưa lường). Lượt CLI GIẢ thật (bể vắng ⇒ `dung`): `KẾT: ĐẠT`, 4 lời |
| **AC-5** script chủ | Secret Manager + binding mức bí mật; `--kiem` có `mong`, ĐỎ hai chiều, 402/429 có TÊN | **ĐẠT** | `tools/staging/09_openrouter_agent.sh` · `tests/agent/test_09_openrouter_agent.py` (18 bài, gcloud+curl GIẢ có trạng thái): dựng từ trống ⇒ **14/14** · khoá qua STDIN (`read -s` ⇒ `printf \| gcloud … --data-file=-`), argv mọi lệnh chứa **0** lần khoá · binding MỨC BÍ MẬT (0 lệnh `projects add-iam-policy-binding`) · chạy lại ⛔ nhân đôi · `--kiem` 0 lệnh ghi · 6 phép phá ⇒ ĐÚNG tập mục ĐỎ (accessor · 402 + "HẾT CREDIT" · 429 + "GIỚI HẠN TỐC ĐỘ" · mô hình ≠ ghim · vượt trần · slug mất khỏi `/models`) + khoá sai ⇒ `/key` 401 có tên · biến NCC vắng · `--khong-goi-thu`. **Chọn tệp MỚI** (⛔ mở rộng 06): lý do ở đầu script |
| **AC-6** cổng | `--duong-nen` ĐẠT · `kiem_tai_lieu` · `lint-imports` 11 · `quet_pii_repo` 0 · `requirements.txt` đủ | xem §F | `requests` đã có (dòng 6, ghi thêm WO-367); `test_phu_thuoc_agent.py` xanh |
| **AC-7** cổng MCP (dự phòng) | CHỈ khi AC-4 ⛔ tự động được | **⛔ LÀM — có lý do** | AC-4 chạy trọn ma trận TỰ ĐỘNG bằng CLI (một lệnh §B(c)) — điều kiện kích hoạt AC-7 ⛔ xảy ra |

## D · Bảng đột biến (phá → chạy bài canh → cắn → trả nguyên; sha tệp trước = sau)

Chạy bằng script ngoài repo (scratchpad `dot_bien.py`): mỗi phép thay ĐÚNG 1 chỗ (mẫu khớp ≠ 1 lần ⇒ ĐỎ ⛔ đo được), chạy `pytest -x` tệp canh, trả byte gốc, `assert` sha256 trước = sau. **16/16 CẮN** (lượt đầu 15/16 — M16 SỐNG SÓT ⇒ thêm bài tĩnh `test_tinh__khoa_hoi_bang_read_s__qua_STDIN_gcloud` ⇒ chạy lại: cắn).

| # | Tệp | Phá | Bài canh cắn | Kết |
|---|---|---|---|---|
| M1 | `fls/agent/mo_hinh.py` | `DINH_TUYEN_OPENROUTER` bỏ `data_collection: deny` | `test_AC2_moi_loi_goi_mang_dinh_tuyen_ZDR_va_deny` | CẮN |
| M2 | `mo_hinh.py` | bỏ chốt `FLS_OPENROUTER_DU_LIEU_XAC_NHAN` | `test_AC2_thieu_moi_chot…` | CẮN |
| M3 | `mo_hinh.py` | ⛔ đọc `usage.cost` (luôn ƯỚC) | `test_AC2_usd_THAT_tu_usage_cost…` | CẮN |
| M4 | `mo_hinh.py` | bỏ cấm `google/*` | `test_AC3_cam_google…` | CẮN |
| M5 | `mo_hinh.py` | bỏ trần MÔ HÌNH | `test_AC2_tran_TONG_va_tran_MO_HINH…` | CẮN |
| M6 | `mo_hinh.py` | ⛔ gửi lại `reasoning_details` | `test_AC1_vong_tool_use_tron…` | CẮN |
| M7 | `mo_hinh.py` | nhận mô hình trả về ≠ ghim | `test_AC1_loi_giua_luc_sinh__mo_hinh_khac_ghim…` | CẮN |
| M8 | `mo_hinh.py` | `MA_THU_LAI` thêm 402 | `test_AC1_429_thu_lai_roi_DAT__402_KHONG_thu_lai` | CẮN |
| M9 | `tools/fleet_eval_voi.py` | trần TỔNG ⛔ dừng các ô sau | `test_AC4_tran_TONG…` | CẮN |
| M10 | `fleet_eval_voi.py` | ⛔ ghi nhật ký khi ngoại lệ chưa lường | `test_AC4_THAT_nhat_ky_tren_MOI_loi_thoat` | CẮN |
| M11 | `tools/staging/09_openrouter_agent.sh` | binding mức PROJECT thay mức bí mật | `test_dung_tu_trong…` | CẮN |
| M12 | `09_…sh` | 402 ⇒ câu chung "lỗi" | `test_DO_HAI_CHIEU…[402]` | CẮN |
| M13 | `tools/chay_agent_voi.py` | nhật ký cùng giây ghi đè (`OR-02`) | `test_AC4_THAT_nhat_ky…` | CẮN |
| M14 | `fls/agent/report.py` | `NGUON_THAT = ("anthropic",)` (`OR-01`) | `test_AC1_chuoi_4_agent…` | CẮN |
| M15 | `fleet_eval_voi.py` | số máy chủ GIẢ mang nhãn THẬT | `test_AC4_luot_GIA_TRON…` | CẮN |
| M16 | `09_…sh` | `read -r -s` ⇒ `read -r` (khoá hiện màn hình) | lượt 1: ⛔ SỐNG SÓT (STDIN ống ⛔ vọng) · lượt 2: `test_tinh__khoa_hoi_bang_read_s…` | CẮN |

## E · Câu chủ (Dev ⛔ tự quyết)

**C1 · ứng viên fleet eval** — slug THẬT còn hiệu lực (`GET /api/v1/models` 2026-11-27), giá USD / 1M token vào · ra, ngữ cảnh, điểm cuối ZDR (`/endpoints/zdr`). Hôm nay `ung_vien` = 2 dòng đầu. Chủ chọn ⇒ Dev thêm vào `ung_vien` (hoặc chạy `--ung-vien …`).

| slug | vào | ra | ngữ cảnh | ZDR | ghi chú |
|---|---|---|---|---|---|
| `anthropic/claude-opus-5.5` | 4 | 20 | 1.000.000 | bedrock · vertex | ⭐ mặc định agent LÀM |
| `anthropic/claude-sonnet-5.5` | 2 | 10 | 1.000.000 | bedrock · vertex | ⭐ mặc định Auditor |
| `anthropic/claude-haiku-5.5` | 0,10 | 0,50 | 1.000.000 | bedrock · vertex | rẻ nhất họ Anthropic |
| `anthropic/claude-fable-5.2` | 8 | 40 | 1.000.000 | **0** | ⚠ 0 điểm cuối ZDR ⇒ `zdr: true` sẽ **503** — ⛔ dùng được với chốt hiện hành |
| `openai/gpt-6.2-sol` | 2 | 10 | 1.050.000 | azure | OpenAI mới nhất, giá ngang Sonnet |
| `openai/gpt-6.2-sol-pro` | 2 | 10 | 1.050.000 | azure | |
| `openai/gpt-6.2-astra` | 8 | 40 | 1.050.000 | azure | hạng cao nhất OpenAI |
| `openai/gpt-6.1-terra` | 1 | 5 | 1.050.000 | azure | |
| `openai/gpt-6-luna` | 0,10 | 0,50 | 1.050.000 | azure | rẻ nhất |

Ngoài bảng (có trong `/models`, ⛔ vào danh mục): bản cũ `anthropic/claude-opus-5`, `-4.8`, `-4.7`… · `openai/gpt-5.x` (một số hết hạn **2026-12-11**) · biến thể `:batch` (⛔ ghim — đổi định tuyến/giá) · bí danh `~anthropic/claude-*-latest`, `~openai/gpt-*-latest` (⛔ ghim). Thêm slug ngoài bảng = Dev tra lại `/models` + `/endpoints/zdr` rồi thêm dòng danh mục (có review).

**C2 · dữ liệu qua bên thứ ba** — với chế độ che `mo` (chủ 23/11), OpenRouter nhận NGUYÊN VĂN nội dung sổ (số TK, tên người, tiền) rồi chuyển tới nhà cung cấp gốc (Bedrock / Vertex / Azure). Mã ép `zdr: true` + `data_collection: "deny"` ở mỗi lời (⇒ chỉ điểm cuối ZDR). Chủ xác nhận: ① chấp nhận dữ liệu đi qua OpenRouter · ② đã **tắt** lưu prompt / huấn luyện và bật **ZDR only** ở `openrouter.ai/settings/privacy` (*Safety Retention* cho phép lưu để chống lạm dụng — tài liệu: *"If you haven't chosen, self-serve accounts allow Safety Retention"*) · ③ khoá có **hạn mức** chi. Chỉ sau đó đặt `FLS_OPENROUTER_DU_LIEU_XAC_NHAN=1`.

## F · Cổng (dán thật — container cloud, cụm PG 16 cổng **5436**)

<!-- CONG -->

## G · Giả định CHƯA kiểm (cần lời gọi THẬT — chủ chạy §A3)

1. **`max_tokens` 16 + `reasoning.effort=low`** ở lời gọi thử của 09 đủ để Opus/Sonnet 5.5 (*reasoning mandatory* theo `/models`) trả 200. Sai ⇒ mục HTTP ĐỎ có tên "yêu cầu sai" ⇒ `--max-tokens 64`.
2. **`model` trả về** = slug ghim hoặc `canonical_slug` (`…-20260921`). Ví dụ tài liệu trả đúng slug yêu cầu; nếu OpenRouter trả dạng khác ⇒ `LoiApi … ≠ ghim` CÓ TÊN (⛔ nhận im lặng) — 09 đo mục này trước khi chạy agent.
3. **Tool calling Opus 5.5 qua Chat Completions** khi điểm cuối là Bedrock/Vertex (ZDR) — máy chủ giả theo đúng khuôn tài liệu; hành vi thật (vd. khối `reasoning_details` mã hoá bắt buộc gửi lại) mới đo được ở §B(a).
4. **`effort` adapter = `medium`** (như WO-355) — `/models` nói mặc định OpenRouter cho Opus/Sonnet 5.5 là `high`; ta đặt RÕ.

## H · Sổ phát hiện (10 cột)

| # | Mã | Mức | Tệp:dòng | Hiện tượng | Đo | Nguyên nhân | Sửa | Bài canh | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `OR-01` | NÊN SỬA | `fls/agent/report.py` `NGUON_THAT` | adapter thật `anthropic-vertex` · `anthropic-google-cloud` (WO-359) bị report in *"bản phát lại sinh bằng mô hình GIẢ — 0 lượt API thật"* | `ten` adapter ∈ `NGUON_THAT`: **1/3** đường thật trước sửa (chỉ `anthropic`) | danh sách cứng từ WO-355, ⛔ cập nhật khi thêm lớp | `NGUON_THAT` = tên MỌI adapter thật (4) | `test_OR01_report_nhan_MOI_adapter_that_la_THAT` (đọc `ten` từ chính các lớp) · đột biến M14 | ĐÃ SỬA |
| 2 | `OR-02` | NÊN SỬA | `tools/chay_agent_voi.py` `ghi_nhat_ky` | hai lượt THẬT trong cùng giây ⇒ tệp nhật ký sau GHI ĐÈ tệp trước (mất dấu vết tiền) | bài ma trận 3 lượt ⇒ **1** tệp trước sửa · **3** sau | tên tệp theo giây | hậu tố `-2`, `-3`… | `test_AC4_THAT_nhat_ky_tren_MOI_loi_thoat` · M13 | ĐÃ SỬA |
| 3 | `OR-03` | GHI NHẬN | `tools/staging/09_openrouter_agent.sh` (bản nháp) | tệp đáp `-o dap_<slug>` — slug có `/` ⇒ curl ⛔ ghi được ⇒ `000` | bài 09 dựng-từ-trống: 4 mục gọi thử ĐỎ `000` | slug `hãng/tên` | tên tệp theo chỉ số | `test_dung_tu_trong…` | ĐÃ SỬA (trước commit) |
| 4 | `OR-04` | GHI NHẬN | `tests/agent/test_mo_hinh_openrouter.py` (bản nháp) | bài grep tiền tố khoá cắn **câu biên bản** của `WO-367` (Đ2); lần 2 xanh trên **tập rỗng** vì tệp chưa track (Đ3) | 1 tệp WO · 0 tệp tests | đếm chữ trần · `git grep` bỏ tệp chưa track | mẫu HÌNH KHOÁ + `--untracked` + bằng chứng dương | chính bài ấy | ĐÃ SỬA (trước commit) |
| 5 | `OR-05` | GHI NHẬN | `fls/agent/openrouter_mo_hinh.json` | `anthropic/claude-fable-5.2` **0** điểm cuối ZDR | `/endpoints/zdr` 27/11 | nhà cung cấp chưa ZDR | ⛔ vào `ung_vien`; ghi ở C1 | `test_AC3_cau_hinh_MOT_cho…` (ứng viên phải có ≥ 1 ZDR) | MỞ (chủ C1) |
