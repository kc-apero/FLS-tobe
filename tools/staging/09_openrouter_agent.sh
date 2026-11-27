#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 09 — 4 agent Voi gọi mô hình QUA OPENROUTER (`WO-367` AC-5)
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell (đã giải nén tarball nhánh có WO-367 — BG-368 §A), SAU 03 `KẾT: ĐẠT`
#  (VM `fls-staging-app` chạy bằng SA `fls-staging-app`). ⛔ Claude KHÔNG vào GCP, ⛔ thấy khoá — chủ chạy rồi gửi lại PHẦN
#  "BÁO CÁO" (chỉ mã HTTP · slug · SỐ token · USD — ⛔ khoá, ⛔ nội dung trả lời).
#
#  Vì sao TỆP MỚI (⛔ mở rộng 06 `--duong openrouter`): 06 là đường của GCP (service · vai IAM mức project · ADC · token
#  metadata trong VM) — OpenRouter ⛔ có cái nào; nó cần KHOÁ trong Secret Manager + binding MỨC BÍ MẬT. Gộp vào 06 = thêm
#  nhánh ở mọi bước và đổi số mục BÁO CÁO mà bài `test_06_vertex_agent.py` ghim (15/14). Tách tệp ⇒ 06 ⛔ đổi một byte.
#
#    bash tools/staging/09_openrouter_agent.sh --project fp-a-project          # dựng: hỏi khoá (read -s) ⇒ Secret Manager + IAM
#    bash tools/staging/09_openrouter_agent.sh --project fp-a-project --kiem   # chỉ ĐỌC + gọi thử (⛔ ghi gì)
#    bash tools/staging/09_openrouter_agent.sh --project fp-a-project --doi-khoa   # thay khoá (thêm PHIÊN BẢN bí mật mới)
#
#  Tuỳ chọn: --sa fls-staging-app (tên SA) · --tran-usd 0.10 (trần USD các lời gọi thử) · --khong-goi-thu (⇒ mục gọi thử ĐỎ, Đ5)
#
#  LÀM GÌ (mỗi việc: có rồi ⇒ bỏ qua, ⛔ phá gì đã có):
#   ① bật `secretmanager.googleapis.com`.
#   ② bí mật `fls-staging-openrouter-key`: CHƯA có (hoặc `--doi-khoa`) ⇒ hỏi khoá bằng `read -s` (⛔ vọng ra màn hình, ⛔ argv,
#      ⛔ lịch sử shell) rồi đưa vào `gcloud secrets create|versions add --data-file=-` qua STDIN (`printf` là lệnh DỰNG SẴN của
#      bash ⇒ ⛔ hiện ở `ps`).
#   ③ cấp `roles/secretmanager.secretAccessor` cho SA `fls-staging-app` CHỈ trên bí mật ấy (binding MỨC BÍ MẬT — ⛔ mức project;
#      cờ `--condition=None` chỉ cần cho binding MỨC PROJECT ở project có binding có điều kiện, nên ⛔ dùng ở đây).
#   ④ BÁO CÁO — mỗi mục khai `mong`; ĐỎ HAI CHIỀU; exit 1 khi ĐỎ:
#      khoá đọc được (độ dài + 0 khoảng trắng; ⛔ in) · SA có accessor trên bí mật · `GET /api/v1/models` = 200 và chứa MỌI slug
#      mặc định · `GET /api/v1/key` = 200 (khoá hợp lệ) · MỖI slug mặc định 1 lời gọi NHỎ = 200, mô hình trả về = slug ghim
#      (hoặc canonical), `provider` gửi kèm ZDR + deny · tổng `usage.cost` ≤ `--tran-usd`. HTTP ≠ 200 ⇒ in TÊN nguyên nhân
#      (402 HẾT CREDIT · 429 GIỚI HẠN TỐC ĐỘ · 401 khoá sai · 403 bị chặn · 503 ⛔ nhà cung cấp ZDR) — ⛔ câu chung (`AG3-GOP-01`).
#
#  Slug mặc định + giá đọc từ `fls/agent/openrouter_mo_hinh.json` (MỘT chỗ — AC-3), ⛔ chép cứng ở đây.
#  ⚠ GIẢ ĐỊNH chưa kiểm (BG-368 §G): `max_tokens` nhỏ (16) đủ cho Opus/Sonnet 5.5 (*reasoning mandatory* — tra /models
#     27/11) khi `reasoning.effort=low`; nếu OpenRouter trả 400 vì quá nhỏ ⇒ mục HTTP ĐỎ có tên "yêu cầu sai", nâng `--max-tokens`.
#  ⛔ KHÔNG làm ở bước 09: chạy agent (BG-368 §B) · ghi kho · in khoá · ghi khoá ra đĩa ngoài tệp tạm chmod 600 (xoá khi thoát).
#  Luật đo (CLAUDE.md Đ3·Đ5): mục ⛔ ĐO ĐƯỢC ⇒ ĐỎ (⛔ "không thấy lệch").
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; SA_NAME="fls-staging-app" ; KIEM=0 ; DOI_KHOA=0 ; GOI_THU=1 ; TRAN_USD="0.10" ; MAX_TOK=16
BI_MAT="fls-staging-openrouter-key"
GOC_API="https://openrouter.ai/api/v1"     # trang api_reference/overview.md (tra 2026-11-27)
while [ $# -gt 0 ]; do
  case "$1" in
    --project)       PROJECT="$2"; shift 2 ;;
    --sa)            SA_NAME="$2"; shift 2 ;;
    --kiem)          KIEM=1; shift ;;
    --doi-khoa)      DOI_KHOA=1; shift ;;
    --khong-goi-thu) GOI_THU=0; shift ;;
    --tran-usd)      TRAN_USD="$2"; shift 2 ;;
    --max-tokens)    MAX_TOK="$2"; shift 2 ;;
    --khoa|--key)    echo "⛔ khoá ⛔ đi qua argv (lộ ở ps/lịch sử) — script tự hỏi bằng read -s" >&2; exit 2 ;;
    -h|--help)       sed -n 2,40p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID> (mong: fp-a-project)" >&2; exit 2; }
case "$PROJECT$SA_NAME" in *[!a-z0-9-]*) echo "⛔ --project/--sa chỉ gồm [a-z0-9-]" >&2; exit 2 ;; esac
case "$TRAN_USD" in ''|*[!0-9.]*) echo "⛔ --tran-usd phải là số" >&2; exit 2 ;; esac
case "$MAX_TOK" in ''|*[!0-9]*) echo "⛔ --max-tokens phải là số nguyên" >&2; exit 2 ;; esac
[ "$KIEM" -eq 1 ] && [ "$DOI_KHOA" -eq 1 ] && { echo "⛔ --kiem (chỉ đọc) ⛔ đi với --doi-khoa" >&2; exit 2; }
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v curl    >/dev/null || { echo "⛔ không có curl" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }

GOC_REPO="$(cd "$(dirname "$0")/../.." && pwd)"
CAU_HINH="$GOC_REPO/fls/agent/openrouter_mo_hinh.json"
[ -r "$CAU_HINH" ] || { echo "⛔ thiếu $CAU_HINH (chạy từ trong repo)" >&2; exit 2; }
SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
G=(gcloud --project="$PROJECT" --quiet)
TM="$(mktemp -d)" ; chmod 700 "$TM" ; trap 'rm -rf "$TM"' EXIT
buoc() { printf '\n── %s\n' "$*"; }
# slug mặc định = các VAI (lam · auditor), theo thứ tự, ⛔ trùng
mapfile -t MO_HINH < <(python3 -c 'import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8")); s=[]
[s.append(v) for v in d["vai"].values() if v not in s]; print("\n".join(s))' "$CAU_HINH")

co_bi_mat() { "${G[@]}" secrets describe "$BI_MAT" >/dev/null 2>&1; }

if [ "$KIEM" -eq 0 ]; then
  buoc "① bật secretmanager.googleapis.com"
  "${G[@]}" services enable secretmanager.googleapis.com

  if ! co_bi_mat || [ "$DOI_KHOA" -eq 1 ]; then
    buoc "② nhập khoá OpenRouter (⛔ hiện chữ; Enter để kết thúc)"
    KHOA=""
    IFS= read -r -s -p "   khoá OpenRouter: " KHOA ; echo
    KHOA="${KHOA//[[:space:]]/}"
    [ "${#KHOA}" -ge 20 ] || { echo "⛔ khoá rỗng/quá ngắn (${#KHOA} ký tự) — ⛔ lưu" >&2; exit 2; }
    if co_bi_mat; then
      printf '%s' "$KHOA" | "${G[@]}" secrets versions add "$BI_MAT" --data-file=- >/dev/null
      echo "   đã thêm PHIÊN BẢN mới cho $BI_MAT (${#KHOA} ký tự)"
    else
      printf '%s' "$KHOA" | "${G[@]}" secrets create "$BI_MAT" --replication-policy=automatic --data-file=- >/dev/null
      echo "   đã tạo $BI_MAT (${#KHOA} ký tự)"
    fi
    KHOA=""
  else
    buoc "② bí mật $BI_MAT đã có — giữ nguyên (đổi khoá: --doi-khoa)"
  fi

  buoc "③ cấp roles/secretmanager.secretAccessor cho SA trên RIÊNG bí mật $BI_MAT"
  "${G[@]}" secrets add-iam-policy-binding "$BI_MAT" --member="serviceAccount:$SA_EMAIL" \
      --role="roles/secretmanager.secretAccessor" >/dev/null
  echo "   SA $SA_NAME: secretAccessor (mức bí mật)"
fi

# ── ĐO ────────────────────────────────────────────────────────────────────────────────────
# Khoá ⇒ tệp header 600 (curl đọc `-H @tệp` ⇒ ⛔ ở argv), ⛔ biến xuất khẩu, xoá khi thoát.
R_KHOA_DAI=0 ; R_KHOA_TRANG=""
if "${G[@]}" secrets versions access latest --secret="$BI_MAT" > "$TM/k" 2>/dev/null; then
  chmod 600 "$TM/k"
  R_KHOA_DAI="$(wc -c < "$TM/k" | tr -d ' ')"
  if grep -q '[[:space:]]' "$TM/k"; then R_KHOA_TRANG="co"; else R_KHOA_TRANG="khong"; fi
  { printf 'Authorization: Bearer '; cat "$TM/k"; printf '\n'; } > "$TM/h" ; chmod 600 "$TM/h"
fi
rm -f "$TM/k"
R_IAM_BM="$("${G[@]}" secrets get-iam-policy "$BI_MAT" --format=json 2>/dev/null || echo '{}')"

goi() {   # $1 = tên tệp đáp · $2.. = đối số curl ⇒ in mã HTTP
  local ra="$1"; shift
  curl -sS -o "$TM/$ra" -w '%{http_code}' --max-time 120 "$@" 2>/dev/null || echo 000
}
R_MODELS="$(goi models -X GET "$GOC_API/models")"
R_KEY="000" ; R_GOI=""
if [ -f "$TM/h" ]; then
  R_KEY="$(goi key -X GET -H @"$TM/h" "$GOC_API/key")"
  if [ "$GOI_THU" -eq 1 ]; then
    i=0
    for m in "${MO_HINH[@]}"; do
      # thân CỐ ĐỊNH, ⛔ dữ liệu thật; provider ZDR + deny như adapter (DINH_TUYEN_OPENROUTER)
      python3 -c 'import json,sys
print(json.dumps({"model":sys.argv[1],"max_tokens":int(sys.argv[2]),"reasoning":{"effort":"low"},
 "provider":{"data_collection":"deny","zdr":True},"messages":[{"role":"user","content":"Trả lời đúng một từ: OK"}]}))' \
        "$m" "$MAX_TOK" > "$TM/yc"
      # tên tệp theo CHỈ SỐ — slug có `/` (`hãng/tên`) ⇒ `-o dap_<slug>` trỏ vào thư mục ⛔ có (đo 27/11: curl 000)
      ma="$(goi "dap_$i" -X POST -H @"$TM/h" -H 'Content-Type: application/json' --data-binary @"$TM/yc" "$GOC_API/chat/completions")"
      R_GOI+="$m=$ma"$'\n'
      i=$((i + 1))
    done
  fi
fi
rm -f "$TM/h"

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa khoá/nội dung trả lời) — chép từ dòng này tới hết, gửi lại"
export PROJECT SA_EMAIL BI_MAT KIEM GOI_THU TRAN_USD CAU_HINH TM R_KHOA_DAI R_KHOA_TRANG R_IAM_BM R_MODELS R_KEY R_GOI
export R_NCC="${FLS_NHA_CUNG_CAP:-}"
python3 - <<'PY'
import json, os
e = os.environ
TM = e["TM"]
ch = json.load(open(e["CAU_HINH"], encoding="utf-8"))
mac_dinh = list(dict.fromkeys(ch["vai"].values()))
# Tên nguyên nhân (trang errors-and-debugging.md §Error codes, tra 2026-11-27) — ⛔ câu chung (AG3-GOP-01)
TEN = {"400": "yêu cầu sai (tham số — thử --max-tokens lớn hơn)", "401": "khoá OpenRouter sai / đã thu hồi",
       "402": "HẾT CREDIT OpenRouter (nạp ở openrouter.ai/settings/credits)", "403": "bị CHẶN: guardrail · kiểm duyệt · hạn mức khoá",
       "408": "hết giờ phía OpenRouter", "429": "GIỚI HẠN TỐC ĐỘ (rate limit)", "502": "nhà cung cấp gốc hỏng",
       "503": "⛔ nhà cung cấp ZDR + deny nào phục vụ mô hình (kiểm settings/privacy)", "000": "⛔ tới được openrouter.ai (mạng)"}
def doc(ten):
    try:
        return json.load(open(os.path.join(TM, ten), encoding="utf-8"))
    except Exception:
        return {}
def ma_loi(d):
    x = d.get("error") if isinstance(d, dict) else None
    return x.get("code") if isinstance(x, dict) else None
iam = json.loads(e["R_IAM_BM"] or "{}")
co_acc = any(b.get("role") == "roles/secretmanager.secretAccessor" and f"serviceAccount:{e['SA_EMAIL']}" in b.get("members", [])
             for b in iam.get("bindings", []))
models = doc("models")
ids = {m.get("id") for m in (models.get("data") or [])} if isinstance(models, dict) else set()
key = doc("key").get("data") or {}
goi = dict(l.split("=", 1) for l in e["R_GOI"].splitlines() if "=" in l)
hang = [
    ("project · SA · bí mật", f"{e['PROJECT']} · {e['SA_EMAIL']} · {e['BI_MAT']}", None),
    ("project = GCP công ty", e["PROJECT"], "fp-a-project"),
    ("biến FLS_NHA_CUNG_CAP của shell (agent đi đường này)", e["R_NCC"] or None, "openrouter"),
    ("khoá đọc được từ Secret Manager (≥ 20 ký tự)", int(e["R_KHOA_DAI"]) >= 20, True),
    ("khoá ⛔ chứa khoảng trắng/xuống dòng", e["R_KHOA_TRANG"] or None, "khong"),
    ("SA có secretAccessor TRÊN bí mật", co_acc, True),
    ("GET /api/v1/models · HTTP", e["R_MODELS"], "200"),
    ("mọi slug mặc định còn trong /models", sorted(set(mac_dinh) - ids) if ids else None, []),
    ("GET /api/v1/key · HTTP (khoá hợp lệ)", e["R_KEY"], "200"),
]
if e["R_KEY"] != "200":
    hang.append(("GET /api/v1/key · nguyên nhân", TEN.get(e["R_KEY"], "lỗi HTTP chưa có tên"), None))
else:
    hang.append(("khoá · hạn mức còn (limit_remaining; None = ⛔ đặt hạn mức)", key.get("limit_remaining"), None))
usd = 0.0
usd_do_duoc = True
for i, m in enumerate(mac_dinh):
    ma = goi.get(m) if e["GOI_THU"] == "1" else None
    d = doc(f"dap_{i}")
    hang.append((f"gọi thử · {m} · HTTP", ma, "200"))
    if ma and ma != "200":
        ml = str(ma_loi(d) or ma)
        hang.append((f"gọi thử · {m} · nguyên nhân (⛔ nội dung)", f"HTTP {ma} — {TEN.get(ma, TEN.get(ml, 'lỗi HTTP chưa có tên'))}", None))
    tra = d.get("model") if ma == "200" else None
    ghim = {m, ch["mo_hinh"].get(m, {}).get("canonical")}
    hang.append((f"gọi thử · {m} · mô hình trả về = slug ghim/canonical", tra in ghim if ma == "200" else None, True))
    if ma == "200":
        u = d.get("usage") or {}
        c = u.get("cost")
        if isinstance(c, (int, float)):
            usd += c
        else:
            usd_do_duoc = False
        hang.append((f"gọi thử · {m} · token vào/ra · nhà cung cấp gốc · finish", f"{u.get('prompt_tokens')}/{u.get('completion_tokens')}"
                     f" · {d.get('provider')} · {(d.get('choices') or [{}])[0].get('finish_reason')}", None))
    else:
        usd_do_duoc = False
hang.append(("tổng usage.cost (USD THẬT do OpenRouter trả) đo được ở MỌI lời gọi thử", usd_do_duoc, True))
hang.append((f"tổng usage.cost ≤ trần --tran-usd {e['TRAN_USD']}", (usd <= float(e["TRAN_USD"])) if usd_do_duoc else None, True))
hang.append(("tổng usage.cost (USD THẬT)", round(usd, 6), None))
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:72}  {gt}")
    else:
        ok = gt == mong
        do += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:70}  {gt!r}  (mong {mong!r})")
che = "--kiem (chỉ đọc + gọi thử)" if e["KIEM"] == "1" else "dựng"
if e["GOI_THU"] != "1":
    che += " · --khong-goi-thu (mục gọi thử ⛔ đo ⇒ ĐỎ)"
print(f"\n══ đường openrouter · chế độ: {che} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
