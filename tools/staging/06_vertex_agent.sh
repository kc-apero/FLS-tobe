#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 06 — 4 agent Voi gọi CLAUDE TRONG GCP của project công ty (`WO-359` AC-3)
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell (đã `git clone` repo, nhánh có WO-359), SAU khi 03 báo `KẾT: ĐẠT`
#  (VM `fls-staging-app` chạy bằng SA `fls-staging-app`). ⛔ Claude KHÔNG vào GCP (quyết chủ 20/11) — chủ chạy, rồi gửi
#  lại PHẦN "BÁO CÁO" ở cuối (chỉ mã HTTP · tên mô hình · SỐ token — ⛔ token truy cập, ⛔ nội dung trả lời).
#
#  HAI ĐƯỜNG (chủ 24/11 ~03:50 *"dùng claude.googleapis.com cho nhanh"*; tên tệp giữ `06_vertex_agent.sh` theo WO-359):
#    --duong google-cloud  ⭐ MẶC ĐỊNH — *Claude Models on Google Cloud (Anthropic managed)*, service `claude.googleapis.com`,
#                          vai `roles/claude.user`, cần WORKSPACE `wrkspc_…` của tổ chức Anthropic gắn project.
#    --duong vertex        dự phòng — Claude trên Vertex AI (Google managed), service `aiplatform.googleapis.com`,
#                          vai `roles/aiplatform.user`, bật mô hình ở Model Garden (bấm tay).
#
#    bash tools/staging/06_vertex_agent.sh --project fp-a-project --workspace-id wrkspc_… --kiem   # ĐỌC + gọi THỬ
#    bash tools/staging/06_vertex_agent.sh --project fp-a-project --workspace-id wrkspc_…          # bật API + cấp vai, rồi đo
#    bash tools/staging/06_vertex_agent.sh --project fp-a-project --duong vertex [--kiem]           # đường dự phòng
#
#  Tuỳ chọn: --region global|us|eu (chỉ vertex; mặc định global) · --vm fls-staging-app · --zone asia-southeast1-b
#            --sa fls-staging-app (tên SA) · --cap-nguoi <email> (google-cloud: cấp thêm `roles/claude.user` cho người chạy
#            Cloud Shell — e2e §B BG-360 chạy bằng danh tính ấy) · --khong-goi-thu (⛔ gọi — mục gọi thử ⇒ ĐỎ, Đ5)
#
#  LÀM GÌ (mỗi việc: có rồi ⇒ bỏ qua, ⛔ phá gì đã có):
#   ① bật service của đường — google-cloud: HAI service `claude.googleapis.com` (API + quyền IAM) và
#      `anthropic-managed-claude.cloudpartnerservices.goog` (Marketplace — ghi nhận dùng vào gói); ⚠ trước đó phải ĐĂNG KÝ
#      gói Marketplace "Claude Models on Google Cloud (Anthropic managed)" bằng tài khoản có quyền MUA trên billing account
#      (trang Anthropic 24/11) · vertex: `aiplatform.googleapis.com`. ⛔ gỡ vai nào (service agent của claude.googleapis.com
#      có vai riêng — *"Don't remove its role grants"*); mọi lệnh cấp vai mức project mang `--condition=None` (project có
#      binding CÓ ĐIỀU KIỆN ⇒ thiếu cờ là gcloud dừng hỏi — orchestrator đo 24/11).
#   ② cấp vai của đường cho SA `fls-staging-app` ở mức PROJECT (+ người chạy nếu `--cap-nguoi`)
#   ③ BƯỚC BẤM TAY, script IN chỗ bấm: google-cloud ⇒ lấy WORKSPACE ID (skill `claude-api` 24/11: *"In the Claude Console,
#      under Settings > Workspaces"*; Console mở TỪ Google Cloud console và chỉ vai `roles/claude.admin` mở được) ·
#      vertex ⇒ bật Opus 5.5 + Sonnet 5.5 ở Model Garden.
#   ④ BÁO CÁO: mỗi mục khai `mong`; ĐẠT/ĐỎ; exit 1 khi ĐỎ. Gọi THỬ 1 lời nhỏ (`max_tokens` 256) mỗi mô hình bằng HAI danh
#      tính: (a) người chạy trong Cloud Shell (`gcloud auth print-access-token`) · (b) TRONG VM qua IAP SSH bằng SA gắn VM
#      (token từ metadata server) — đúng danh tính app staging dùng. Kèm trạng thái API của đường KIA (thông tin).
#
#  ⛔ KHÔNG làm ở bước 06: chạy agent (khối lệnh BG-360 §B) · ghi kho (G0 BÓNG) · tạo khoá SA · in workspace ID đầy đủ.
#  ⛔ token/khoá: token chỉ ở biến shell + tệp tạm chmod 600 (header curl đọc từ tệp — ⛔ lộ ở `ps`), xoá khi thoát.
#  Luật đo (CLAUDE.md Đ3·Đ5): mỗi mục có `mong`; mục ⛔ ĐO ĐƯỢC ⇒ ĐỎ (không phải "không thấy lệch").
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; DUONG="google-cloud" ; REGION="global" ; VM="fls-staging-app" ; ZONE="asia-southeast1-b"
SA_NAME="fls-staging-app" ; WS="" ; CAP_NGUOI="" ; KIEM=0 ; GOI_THU=1
while [ $# -gt 0 ]; do
  case "$1" in
    --project)      PROJECT="$2"; shift 2 ;;
    --duong)        DUONG="$2"; shift 2 ;;
    --region)       REGION="$2"; shift 2 ;;
    --vm)           VM="$2"; shift 2 ;;
    --zone)         ZONE="$2"; shift 2 ;;
    --sa)           SA_NAME="$2"; shift 2 ;;
    --workspace-id) WS="$2"; shift 2 ;;
    --cap-nguoi)    CAP_NGUOI="$2"; shift 2 ;;
    --kiem)         KIEM=1; shift ;;
    --khong-goi-thu) GOI_THU=0; shift ;;
    -h|--help)      sed -n 2,40p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID> (mong: fp-a-project)" >&2; exit 2; }
case "$DUONG" in google-cloud|vertex) ;; *) echo "⛔ --duong phải là google-cloud|vertex" >&2; exit 2 ;; esac
case "$REGION" in global|us|eu) ;; *) echo "⛔ --region phải là global|us|eu — vùng đơn ($REGION) ⛔ phục vụ Opus 5.5/Sonnet 5.5" >&2; exit 2 ;; esac
if [ "$DUONG" = google-cloud ]; then
  [ "$REGION" = global ] || { echo "⛔ đường google-cloud: vị trí giữ global (skill: \"Leave it there\")" >&2; exit 2; }
  case "$WS" in wrkspc_*) ;; *) echo "⛔ đường google-cloud cần --workspace-id wrkspc_… (Claude Console → Settings → Workspaces)" >&2; exit 2 ;; esac
  case "$WS" in *[!A-Za-z0-9_]*) echo "⛔ --workspace-id chỉ gồm [A-Za-z0-9_]" >&2; exit 2 ;; esac
fi
case "$PROJECT$VM$ZONE$SA_NAME" in *[!a-z0-9-]*) echo "⛔ --project/--vm/--zone/--sa chỉ gồm [a-z0-9-]" >&2; exit 2 ;; esac
if [ -n "$CAP_NGUOI" ]; then
  case "$CAP_NGUOI" in *@*.*) ;; *) echo "⛔ --cap-nguoi <email>" >&2; exit 2 ;; esac
  case "$CAP_NGUOI" in *[!A-Za-z0-9@._+-]*) echo "⛔ --cap-nguoi: email lạ" >&2; exit 2 ;; esac
fi
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v curl    >/dev/null || { echo "⛔ không có curl" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }

SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
MO_HINH=(claude-opus-5-5 claude-sonnet-5-5)      # mã TRẦN ở cả hai đường (⛔ tiền tố, ⛔ `@ngày`) — tra 24/11
if [ "$DUONG" = google-cloud ]; then
  API="claude.googleapis.com" ; API2="anthropic-managed-claude.cloudpartnerservices.goog"
  API_KIA="aiplatform.googleapis.com" ; VAI="roles/claude.user"
  HOST="claude.googleapis.com"
  # URL theo trang Anthropic *Claude Models on Google Cloud* (24/11): …/locations/global/workspaces/<ws>/invoke/v1/messages
  URL_MAU="https://${HOST}/v1/projects/${PROJECT}/locations/global/workspaces/${WS}/invoke/v1/messages"
else
  API="aiplatform.googleapis.com" ; API2="" ; API_KIA="claude.googleapis.com" ; VAI="roles/aiplatform.user"
  if [ "$REGION" = global ]; then HOST="aiplatform.googleapis.com"; else HOST="aiplatform.${REGION}.rep.googleapis.com"; fi
  URL_MAU="https://${HOST}/v1/projects/${PROJECT}/locations/${REGION}/publishers/anthropic/models/MOHINH:rawPredict"
fi
G=(gcloud --project="$PROJECT" --quiet)
TM="$(mktemp -d)" ; chmod 700 "$TM" ; trap 'rm -rf "$TM"' EXIT

buoc() { printf '\n── %s\n' "$*"; }

if [ "$KIEM" -eq 0 ]; then
  buoc "① bật service $API${API2:+ + $API2}"
  "${G[@]}" services enable "$API" ${API2:+"$API2"}

  buoc "② cấp $VAI (mức project)"
  "${G[@]}" projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA_EMAIL" \
      --role="$VAI" --condition=None >/dev/null
  echo "   SA $SA_NAME: $VAI"
  if [ -n "$CAP_NGUOI" ]; then
    "${G[@]}" projects add-iam-policy-binding "$PROJECT" --member="user:$CAP_NGUOI" \
        --role="$VAI" --condition=None >/dev/null
    echo "   người chạy (--cap-nguoi): $VAI"
  fi
fi

if [ "$DUONG" = google-cloud ]; then
  buoc "③ BƯỚC BẤM TAY — chỉ khi chưa xong (script ⛔ làm thay được)"
  echo "   a) Marketplace → listing \"Claude Models on Google Cloud (Anthropic managed)\" → Subscribe (tài khoản có quyền MUA"
  echo "      trên billing account) → Manage on Console. ⚠ ① ĐỎ 'không tìm thấy anthropic-managed-claude.cloudpartnerservices.goog'"
  echo "      ⇒ chạy bằng tài khoản đã mua (trang Anthropic)."
  echo "   b) Trang Claude (Agent Platform → Models → Claude Platform → Anthropic managed) → Activate → mở thư xác nhận."
  echo "   c) WORKSPACE ID: nút Open Claude Console (cần roles/claude.admin) → Settings → Workspaces → ID 'Default Workspace'"
  echo "      dạng wrkspc_… ⇒ --workspace-id"
else
  buoc "③ Model Garden — BƯỚC BẤM TAY (mỗi mô hình một lần cho project; script ⛔ tự bật)"
  for m in "${MO_HINH[@]}"; do
    echo "   mở: https://console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/${m}?project=${PROJECT}"
  done
  echo "   ⇒ bấm 'Enable' / chấp nhận điều khoản Anthropic; nếu đường dẫn ⛔ mở được: Vertex AI → Model Garden → tìm 'Claude'."
fi
echo "   (đo bên dưới bằng lời gọi thử — chưa xong ⇒ HTTP ≠ 200 ⇒ ĐỎ, kèm trạng thái lỗi Google/Anthropic, ⛔ nội dung)"

# ── gọi THỬ ───────────────────────────────────────────────────────────────────────────────
# Thân yêu cầu: một câu CỐ ĐỊNH, ⛔ dữ liệu thật. google-cloud: như Claude API (`model` trong thân, `anthropic-version`
# ở HEADER) · vertex: `model` trong URL, `anthropic_version` trong THÂN — cả hai theo trang Anthropic 24/11.
yeu_cau() {   # $1 = mã mô hình
  if [ "$DUONG" = google-cloud ]; then
    printf '{"model":"%s","max_tokens":256,"messages":[{"role":"user","content":"Trả lời đúng một từ: OK"}]}' "$1"
  else
    printf '{"anthropic_version":"vertex-2023-10-16","max_tokens":256,"messages":[{"role":"user","content":"Trả lời đúng một từ: OK"}]}'
  fi
}
if [ "$DUONG" = google-cloud ]; then HDR_THEM="anthropic-version: 2026-10-21"; else HDR_THEM="Accept: application/json"; fi
# Đọc đáp: CHỈ mã trạng thái · mô hình · stop_reason · số token. ⛔ in `content` (luật cứng: ⛔ phản hồi thô).
DOC_DAP='import json,sys
try: d=json.load(open(sys.argv[1],encoding="utf-8"))
except Exception: d={}
if isinstance(d,list): d=d[0] if d and isinstance(d[0],dict) else {}
e=d.get("error") if isinstance(d,dict) else None
u=d.get("usage") or {}
print("|".join([str(d.get("model") or ""),str(d.get("stop_reason") or ""),str(u.get("input_tokens") or ""),
 str(u.get("output_tokens") or ""),str((e or {}).get("status") or (e or {}).get("type") or "") if isinstance(e,dict) else ""]))'

goi_thu_cloud_shell() {    # $1 = mã mô hình ⇒ in "http|model|stop|vao|ra|trang_thai_loi"
  local m="$1" tok ma
  tok="$(gcloud auth print-access-token 2>/dev/null || true)"
  [ -n "$tok" ] || { echo "000|||||khong-lay-duoc-token"; return; }
  printf 'Authorization: Bearer %s\n' "$tok" > "$TM/h" ; chmod 600 "$TM/h" ; tok=""
  yeu_cau "$m" > "$TM/yc"
  ma="$(curl -sS -o "$TM/dap" -w '%{http_code}' --max-time 120 -X POST "${URL_MAU/MOHINH/$m}" \
        -H @"$TM/h" -H 'Content-Type: application/json' -H "$HDR_THEM" --data-binary @"$TM/yc" 2>/dev/null || echo 000)"
  rm -f "$TM/h"
  echo "${ma}|$(python3 -c "$DOC_DAP" "$TM/dap" 2>/dev/null || echo '|||||')"
  rm -f "$TM/dap"
}

# Lệnh chạy TRONG VM (SA gắn VM). Token metadata ⛔ in, chỉ nằm trong tệp 600 rồi xoá. Mỗi dòng: `vm_<mã>=http|…`.
YC_VM=""
for m in "${MO_HINH[@]}"; do YC_VM+="printf '%s' '$(yeu_cau "$m")' > \$T/yc_$m; "; done
DO_TRONG="set -u; T=\$(mktemp -d); chmod 700 \$T;
tok=\$(curl -sS -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token' 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get(\"access_token\",\"\"))' 2>/dev/null);
printf 'Authorization: Bearer %s\n' \"\$tok\" > \$T/h; chmod 600 \$T/h; tok=;
$YC_VM
cat > \$T/doc.py <<'PYEOF'
$DOC_DAP
PYEOF
for m in ${MO_HINH[*]}; do
  u='$URL_MAU'; u=\${u/MOHINH/\$m};
  ma=\$(curl -sS -o \$T/dap -w '%{http_code}' --max-time 120 -X POST \"\$u\" -H @\$T/h -H 'Content-Type: application/json' -H '$HDR_THEM' --data-binary @\$T/yc_\$m 2>/dev/null || echo 000);
  echo \"vm_\$m=\$ma|\$(python3 \$T/doc.py \$T/dap 2>/dev/null)\"; rm -f \$T/dap;
done; rm -rf \$T"

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa token/khoá/nội dung trả lời/workspace đầy đủ) — chép từ dòng này tới hết, gửi lại"
export PROJECT DUONG REGION VM ZONE SA_EMAIL VAI API API2 API_KIA KIEM GOI_THU HOST CAP_NGUOI
export WS_CHE="${WS:+${WS:0:7}…(${#WS} ký tự)}"
export R_APIS="$("${G[@]}" services list --enabled --format='value(config.name)' 2>/dev/null | tr '\n' ' ' || true)"
export R_IAM="$("${G[@]}" projects get-iam-policy "$PROJECT" --format=json 2>/dev/null || echo '{}')"
export R_VM="$("${G[@]}" compute instances describe "$VM" --zone="$ZONE" --format=json 2>/dev/null || echo '{}')"
export R_CS="" R_TRONG=""
if [ "$GOI_THU" -eq 1 ]; then
  for m in "${MO_HINH[@]}"; do R_CS+="cs_${m}=$(goi_thu_cloud_shell "$m")"$'\n'; done
  R_TRONG="$("${G[@]}" compute ssh "$VM" --zone="$ZONE" --tunnel-through-iap --command="$DO_TRONG" 2>/dev/null || true)"
fi
export R_CS R_TRONG

python3 - <<'PY'
import json, os
e = os.environ
def js(k, mac):
    try: return json.loads(e[k] or mac)
    except ValueError: return json.loads(mac)
iam, vm = js("R_IAM", "{}"), js("R_VM", "{}")
def co_vai(tv):
    return any(b.get("role") == e["VAI"] and tv in b.get("members", []) and not b.get("condition")
               for b in iam.get("bindings", []))
vm_sa = (vm.get("serviceAccounts") or [{}])[0]
pham_vi = vm_sa.get("scopes") or []
dong = dict(l.split("=", 1) for l in (e["R_CS"] + "\n" + e["R_TRONG"]).splitlines() if "=" in l)
# USD/1M — tra 24/11. google-cloud: CHƯA có bảng giá chính thức ⇒ ƯỚC theo giá Claude API · vertex: us/eu ×1,1
GIA = {"claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00)}
HE = {"global": 1.0, "us": 1.1, "eu": 1.1}[e["REGION"]] if e["DUONG"] == "vertex" else 1.0
apis = e["R_APIS"].split()
usd = 0.0
def tach(k):
    p = (dong.get(k) or "").split("|")
    return (p + [""] * 6)[:6] if dong.get(k) else [None] * 6
hang = [
  ("đường · project · vùng · host · SA", f'{e["DUONG"]} · {e["PROJECT"]} · {e["REGION"]} · {e["HOST"]} · {e["SA_EMAIL"]}', None),
  ("project = GCP công ty (fp-a-project — AC-5)", e["PROJECT"], "fp-a-project"),
  (f"API {e['API']} bật", e["API"] in apis, True),
] + ([(f"API {e['API2']} bật (Marketplace)", e["API2"] in apis, True)] if e["API2"] else []) + [
  (f"API {e['API_KIA']} (đường kia — thông tin)", e["API_KIA"] in apis, None),
  (f"SA có {e['VAI']} ở project (⛔ điều kiện)", co_vai(f"serviceAccount:{e['SA_EMAIL']}") if iam else None, True),
]
if e["CAP_NGUOI"]:
    hang.append((f"người chạy (--cap-nguoi) có {e['VAI']}", co_vai(f"user:{e['CAP_NGUOI']}") if iam else None, True))
if e["DUONG"] == "google-cloud":
    hang.append(("workspace (che)", e["WS_CHE"] or "—", None))
hang += [
  ("VM tồn tại · chạy bằng SA", vm_sa.get("email"), e["SA_EMAIL"]),
  ("VM phạm vi OAuth có cloud-platform", "https://www.googleapis.com/auth/cloud-platform" in pham_vi if vm else None, True),
]
for nguon, nhan in (("cs", "Cloud Shell · người chạy"), ("vm", "TRONG VM · SA")):
    for m in ("claude-opus-5-5", "claude-sonnet-5-5"):
        ma, mo, stop, vao, ra, loi = tach(f"{nguon}_{m}")
        if e["GOI_THU"] != "1":
            ma = mo = None
        hang.append((f"{nhan} · {m} · HTTP", ma, "200"))
        hang.append((f"{nhan} · {m} · mô hình trả về (= mã ghim)", mo if ma == "200" else None, m))
        if ma and ma != "200":
            hang.append((f"{nhan} · {m} · trạng thái lỗi (⛔ nội dung)", loi or "—", None))
        if ma == "200":
            try:
                v, r = int(vao or 0), int(ra or 0)
                usd += HE * (v * GIA[m][0] + r * GIA[m][1]) / 1e6
                hang.append((f"{nhan} · {m} · token vào/ra · stop_reason", f"{v}/{r} · {stop}", None))
            except ValueError:
                hang.append((f"{nhan} · {m} · token vào/ra (đọc được số)", None, True))
hang.append(("chi phí ƯỚC các lời gọi thử (USD; google-cloud CHƯA có bảng giá — số thật ở hoá đơn GCP)", round(usd, 6), None))
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:72}  {gt}")
    else:
        ok = gt == mong
        do += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:70}  {gt!r}  (mong {mong!r})")
che_do = "--kiem (chỉ đọc + gọi thử)" if e["KIEM"] == "1" else "dựng"
if e["GOI_THU"] != "1":
    che_do += " · --khong-goi-thu (mục gọi thử ⛔ đo ⇒ ĐỎ)"
print(f"\n══ đường {e['DUONG']} · chế độ: {che_do} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
