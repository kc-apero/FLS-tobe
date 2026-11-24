#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 06 — 4 agent Voi gọi CLAUDE TRÊN VERTEX AI của project công ty (`WO-359` AC-3)
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell (đã `git clone` repo, nhánh có WO-359), SAU khi 03 báo `KẾT: ĐẠT`
#  (VM `fls-staging-app` chạy bằng SA `fls-staging-app`). ⛔ Claude KHÔNG vào GCP (quyết chủ 20/11) — chủ chạy, rồi gửi
#  lại PHẦN "BÁO CÁO" ở cuối (chỉ mã HTTP · tên mô hình · SỐ token — ⛔ token truy cập, ⛔ nội dung trả lời).
#
#    bash tools/staging/06_vertex_agent.sh --project fp-a-project --kiem     # chỉ ĐỌC + gọi THỬ 1 lời nhỏ mỗi mô hình
#    bash tools/staging/06_vertex_agent.sh --project fp-a-project            # bật API + cấp quyền SA, rồi đo như --kiem
#
#  Tuỳ chọn: --region global|us|eu (mặc định global) · --vm fls-staging-app · --zone asia-southeast1-b
#            --sa fls-staging-app (tên SA, ⛔ email) · --khong-goi-thu (⛔ gọi mô hình — các mục gọi thử ⇒ ĐỎ, Đ5)
#
#  LÀM GÌ (mỗi việc: có rồi ⇒ bỏ qua, ⛔ phá gì đã có):
#   ① bật API `aiplatform.googleapis.com`
#   ② cấp `roles/aiplatform.user` (quyền `aiplatform.endpoints.predict`) cho SA `fls-staging-app` ở mức PROJECT
#   ③ Claude Opus 5.5 + Sonnet 5.5 trong **Model Garden**: ⚠ BƯỚC BẤM TAY — script IN đường dẫn, ⛔ tự bật (giả định
#      chưa kiểm: điều khoản đối tác của Anthropic phải được chấp nhận trên giao diện; ⛔ tìm thấy lệnh gcloud chính thức).
#      Script ĐO kết quả bằng lời gọi thử: chưa bật ⇒ HTTP ≠ 200 ⇒ ĐỎ, kèm mã trạng thái Google trả (⛔ nội dung).
#   ④ BÁO CÁO: mỗi mục khai `mong`; ĐẠT/ĐỎ; exit 1 khi ĐỎ. Gọi THỬ 1 lời nhỏ (`max_tokens` 256, ~vài chục token) mỗi mô
#      hình theo HAI danh tính: (a) người chạy trong Cloud Shell (`gcloud auth print-access-token`) — đo Model Garden +
#      vùng; (b) TRONG VM qua IAP SSH bằng SA gắn VM (token từ metadata server) — đo đúng danh tính agent dùng trên staging.
#
#  VÙNG (tra 24/11, trang `claude-models-on-google-cloud/google-managed`): `global` (khuyên; giá gốc) · `us`/`eu` (đa vùng,
#   +10 %). Vùng ĐƠN (vd `asia-southeast1`) **chỉ phục vụ Sonnet 4.6 trở về trước** ⇒ script ⛔ nhận.
#  ⛔ KHÔNG làm ở bước 06: chạy agent (khối lệnh BG-360 §B) · ghi kho (G0 BÓNG) · tạo khoá SA.
#  ⛔ token/khoá: token chỉ ở biến shell + tệp tạm chmod 600 (header curl đọc từ tệp — ⛔ lộ ở `ps`), xoá khi thoát.
#  Luật đo (CLAUDE.md Đ3·Đ5): mỗi mục có `mong`; mục ⛔ ĐO ĐƯỢC ⇒ ĐỎ (không phải "không thấy lệch").
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="global" ; VM="fls-staging-app" ; ZONE="asia-southeast1-b" ; SA_NAME="fls-staging-app"
KIEM=0 ; GOI_THU=1
while [ $# -gt 0 ]; do
  case "$1" in
    --project)  PROJECT="$2"; shift 2 ;;
    --region)   REGION="$2"; shift 2 ;;
    --vm)       VM="$2"; shift 2 ;;
    --zone)     ZONE="$2"; shift 2 ;;
    --sa)       SA_NAME="$2"; shift 2 ;;
    --kiem)     KIEM=1; shift ;;
    --khong-goi-thu) GOI_THU=0; shift ;;
    -h|--help)  sed -n 2,33p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID> (mong: fp-a-project)" >&2; exit 2; }
case "$REGION" in global|us|eu) ;; *) echo "⛔ --region phải là global|us|eu — vùng đơn ($REGION) ⛔ phục vụ Opus 5.5/Sonnet 5.5" >&2; exit 2 ;; esac
case "$PROJECT$VM$ZONE$SA_NAME" in *[!a-z0-9-]*) echo "⛔ --project/--vm/--zone/--sa chỉ gồm [a-z0-9-]" >&2; exit 2 ;; esac
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v curl    >/dev/null || { echo "⛔ không có curl" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }

SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
MO_HINH=(claude-opus-5-5 claude-sonnet-5-5)      # mã Vertex = mã TRẦN (⛔ tiền tố, ⛔ `@ngày`) — tra 24/11
VAI="roles/aiplatform.user"
if [ "$REGION" = global ]; then HOST="aiplatform.googleapis.com"; else HOST="aiplatform.${REGION}.rep.googleapis.com"; fi
G=(gcloud --project="$PROJECT" --quiet)
TM="$(mktemp -d)" ; chmod 700 "$TM" ; trap 'rm -rf "$TM"' EXIT

buoc() { printf '\n── %s\n' "$*"; }

if [ "$KIEM" -eq 0 ]; then
  buoc "① bật API aiplatform.googleapis.com"
  "${G[@]}" services enable aiplatform.googleapis.com

  buoc "② cấp $VAI cho SA $SA_NAME (mức project)"
  "${G[@]}" projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA_EMAIL" \
      --role="$VAI" --condition=None >/dev/null
  echo "   $SA_EMAIL: $VAI"
fi

buoc "③ Model Garden — BƯỚC BẤM TAY (mỗi mô hình một lần cho project; script ⛔ tự bật)"
for m in "${MO_HINH[@]}"; do
  echo "   mở: https://console.cloud.google.com/vertex-ai/publishers/anthropic/model-garden/${m}?project=${PROJECT}"
done
echo "   ⇒ bấm 'Enable' / chấp nhận điều khoản Anthropic; nếu đường dẫn ⛔ mở được: Vertex AI → Model Garden → tìm 'Claude'."
echo "   (đo bên dưới bằng lời gọi thử — chưa bật ⇒ HTTP ≠ 200 ⇒ ĐỎ)"

# ── gọi THỬ ───────────────────────────────────────────────────────────────────────────────
# Thân yêu cầu: một câu CỐ ĐỊNH, ⛔ dữ liệu thật. `anthropic_version` trong THÂN (⛔ header) — đúng trang Vertex 24/11.
YEU_CAU='{"anthropic_version":"vertex-2023-10-16","max_tokens":256,"messages":[{"role":"user","content":"Trả lời đúng một từ: OK"}]}'
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
  local m="$1" tok
  tok="$(gcloud auth print-access-token 2>/dev/null || true)"
  [ -n "$tok" ] || { echo "000|||||khong-lay-duoc-token"; return; }
  printf 'Authorization: Bearer %s\n' "$tok" > "$TM/h" ; chmod 600 "$TM/h" ; tok=""
  printf '%s' "$YEU_CAU" > "$TM/yc"
  local ma
  ma="$(curl -sS -o "$TM/dap" -w '%{http_code}' --max-time 120 -X POST \
        "https://${HOST}/v1/projects/${PROJECT}/locations/${REGION}/publishers/anthropic/models/${m}:rawPredict" \
        -H @"$TM/h" -H 'Content-Type: application/json' --data-binary @"$TM/yc" 2>/dev/null || echo 000)"
  rm -f "$TM/h"
  echo "${ma}|$(python3 -c "$DOC_DAP" "$TM/dap" 2>/dev/null || echo '|||||')"
  rm -f "$TM/dap"
}

# Lệnh chạy TRONG VM (SA gắn VM). Token metadata ⛔ in, chỉ nằm trong tệp 600 rồi xoá. Mỗi dòng: `vm_<mã>=http|…`.
DO_TRONG="set -u; T=\$(mktemp -d); chmod 700 \$T;
tok=\$(curl -sS -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token' 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get(\"access_token\",\"\"))' 2>/dev/null);
printf 'Authorization: Bearer %s\n' \"\$tok\" > \$T/h; chmod 600 \$T/h; tok=;
printf '%s' '$YEU_CAU' > \$T/yc;
cat > \$T/doc.py <<'PYEOF'
$DOC_DAP
PYEOF
for m in ${MO_HINH[*]}; do
  ma=\$(curl -sS -o \$T/dap -w '%{http_code}' --max-time 120 -X POST \"https://${HOST}/v1/projects/${PROJECT}/locations/${REGION}/publishers/anthropic/models/\$m:rawPredict\" -H @\$T/h -H 'Content-Type: application/json' --data-binary @\$T/yc 2>/dev/null || echo 000);
  echo \"vm_\$m=\$ma|\$(python3 \$T/doc.py \$T/dap 2>/dev/null)\"; rm -f \$T/dap;
done; rm -rf \$T"

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa token/khoá/nội dung trả lời) — chép từ dòng này tới hết, gửi lại"
export PROJECT REGION VM ZONE SA_EMAIL VAI KIEM GOI_THU HOST
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
sa_tv = f"serviceAccount:{e['SA_EMAIL']}"
co_vai = any(b.get("role") == e["VAI"] and sa_tv in b.get("members", []) and not b.get("condition")
             for b in iam.get("bindings", []))
vm_sa = (vm.get("serviceAccounts") or [{}])[0]
pham_vi = vm_sa.get("scopes") or []
dong = dict(l.split("=", 1) for l in (e["R_CS"] + "\n" + e["R_TRONG"]).splitlines() if "=" in l)
GIA = {"claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00)}   # USD/1M — tra 24/11; us/eu ×1,1
HE = {"global": 1.0, "us": 1.1, "eu": 1.1}[e["REGION"]]
usd = 0.0
def tach(k):
    p = (dong.get(k) or "").split("|")
    return (p + [""] * 6)[:6] if dong.get(k) else [None] * 6
hang = [
  ("project · vùng · host · SA", f'{e["PROJECT"]} · {e["REGION"]} · {e["HOST"]} · {e["SA_EMAIL"]}', None),
  ("project = GCP công ty (fp-a-project — AC-5)", e["PROJECT"], "fp-a-project"),
  ("API aiplatform.googleapis.com bật", "aiplatform.googleapis.com" in e["R_APIS"].split(), True),
  (f"SA có {e['VAI']} ở project (⛔ điều kiện)", co_vai if iam else None, True),
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
            hang.append((f"{nhan} · {m} · trạng thái lỗi Google (⛔ nội dung)", loi or "—", None))
        if ma == "200":
            try:
                v, r = int(vao or 0), int(ra or 0)
                usd += HE * (v * GIA[m][0] + r * GIA[m][1]) / 1e6
                hang.append((f"{nhan} · {m} · token vào/ra · stop_reason", f"{v}/{r} · {stop}", None))
            except ValueError:
                hang.append((f"{nhan} · {m} · token vào/ra (đọc được số)", None, True))
hang.append(("chi phí ước các lời gọi thử (USD, giá tra 24/11 — Billing GCP là số thật)", round(usd, 6), None))
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
print(f"\n══ chế độ: {che_do} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
