#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 10 — CỔNG MCP `fls-staging-mcp` để tài khoản Claude của CHỦ ĐỌC kho FLS · WO-371
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell (repo đã `git clone`), SAU 01 + 02 (+ 05 nếu muốn có dữ liệu).
#  ⛔ Claude KHÔNG vào GCP (quyết 20/11 GIỮ) — Claude chỉ ĐỌC dữ liệu QUA MCP, ⛔ có quyền GCP nào.
#  Gửi lại PHẦN "BÁO CÁO" ở cuối (⛔ mật khẩu/khoá/email — script ⛔ in).
#
#    bash tools/staging/10_mcp.sh --project <P> --kiem                  # chỉ ĐỌC — đo trạng thái (⛔ đổi gì)
#    bash tools/staging/10_mcp.sh --project <P> --oauth-nhap            # lần ĐẦU: hỏi client ID + secret Google (gõ ẨN)
#    bash tools/staging/10_mcp.sh --project <P>                         # dựng / dựng lại
#    bash tools/staging/10_mcp.sh --project <P> --cho-phep a@x.com,b@y.com   # ĐỔI danh sách email được kết nối
#
#  Tuỳ chọn: --region (asia-southeast1) · --service (fls-staging-mcp) · --instance (fls-staging)
#            --tag (mặc định: SHA ngắn của HEAD; chưa có trong Artifact Registry ⇒ dựng ảnh như bước 03/07)
#
#  ── THIẾT KẾ (BG-372 §3) ──────────────────────────────────────────────────────────────────────────────
#   · Connector claude.ai gọi từ hạ tầng Anthropic (tài liệu claude.com: "Anthropic's outbound traffic to your
#     server originates from 160.79.104.0/21") ⇒ ⛔ đi qua IAP được (IAP đòi cookie/đăng nhập Google của TRÌNH
#     DUYỆT). ⇒ IAP CHỈ cho web app (07); MCP là service RIÊNG, `--allow-unauthenticated` ở tầng Cloud Run
#     và ⛔ authless ở tầng ỨNG DỤNG: OAuth 2.1 của chính FLS (`fls/mcp/xac_thuc.py`), đăng nhập uỷ Google,
#     CHỈ email trong `fls-staging-mcp-cho-phep` lấy được token (mặc định: CHỈ tài khoản đang chạy script).
#   · SA RIÊNG `fls-staging-mcp`: `secretAccessor` trên ĐÚNG 4 bí mật (fls_doc + 3 bí mật của MCP) ·
#     `cloudsql.client` mức dự án CÓ ĐIỀU KIỆN chỉ instance `fls-staging` (Cloud SQL ⛔ có IAM mức instance ⇒
#     điều kiện IAM là cách hẹp duy nhất; dự án đã có 2 binding điều kiện — mẫu fps-v35, `STG-WEB-R1-03`).
#     ⛔ vai nào khác. Vai PG = `fls_doc` (bước 02: CHỈ SELECT + `default_transaction_read_only`).
#   · `--cpu-boost` + scale-về-0: claude.ai chờ "10 seconds" cho discovery/registration/token (tài liệu claude.com)
#     ⇒ khởi động lạnh phải nhanh; đo ảnh cục bộ 27/11: ~3 giây tới khi nghe (BG-372 §giả định M-6).
#   · Cloud SQL qua `--add-cloudsql-instances` (socket `/cloudsql/<conn>`) — ⛔ proxy trong container.
#   · URL = khuôn TẤT ĐỊNH của Cloud Run `https://<service>-<số project>.<vùng>.run.app` (tài liệu Cloud Run
#     "deterministic URL") ⇒ biết TRƯỚC khi deploy ⇒ khai được redirect URI cho OAuth client Google + `aud` token.
#
#  ⛔ KHÔNG làm: đụng service/tài nguyên ngoài tên `fls-staging-mcp*` (dự án có 21 service Cloud Run của người khác)
#     · gỡ/sửa binding nào ngoài của SA `fls-staging-mcp` · ghi kho · xoá gì. Tắt: `gcloud run services delete
#     fls-staging-mcp --region asia-southeast1` (chủ tự gõ).
#  Luật đo (CLAUDE.md Đ3·Đ5): mục ⛔ ĐO ĐƯỢC ⇒ ĐỎ.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="asia-southeast1" ; SVC="fls-staging-mcp" ; INSTANCE="fls-staging"
TAG="" ; KIEM=0 ; CHO_PHEP="" ; OAUTH_NHAP=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project)    PROJECT="$2"; shift 2 ;;
    --region)     REGION="$2"; shift 2 ;;
    --service)    SVC="$2"; shift 2 ;;
    --instance)   INSTANCE="$2"; shift 2 ;;
    --tag)        TAG="$2"; shift 2 ;;
    --cho-phep)   CHO_PHEP="$2"; shift 2 ;;
    --oauth-nhap) OAUTH_NHAP=1; shift ;;
    --kiem)       KIEM=1; shift ;;
    -h|--help)    sed -n 2,40p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
case "$SVC$REGION$INSTANCE" in *[!a-z0-9-]*) echo "⛔ --service/--region/--instance chỉ gồm [a-z0-9-]" >&2; exit 2 ;; esac
case "$SVC" in fls-staging-mcp*) ;; *) echo "⛔ --service phải bắt đầu bằng fls-staging-mcp (⛔ đụng service người khác)" >&2; exit 2 ;; esac
if [ -n "$CHO_PHEP" ]; then
  case "$CHO_PHEP" in *[!A-Za-z0-9@._+,-]*|*,,*|,*|*,) echo "⛔ --cho-phep: danh sách email cách nhau dấu phẩy" >&2; exit 2 ;; esac
  IFS=',' read -ra DS_KIEM <<<"$CHO_PHEP"
  for e in "${DS_KIEM[@]}"; do case "$e" in ?*@?*.?*) ;; *) echo "⛔ --cho-phep: một mục ⛔ phải email" >&2; exit 2 ;; esac; done
fi
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -n "$TAG" ] || TAG="$(git -C "$GOC" rev-parse --short HEAD 2>/dev/null || echo thu)"

AR_REPO="fls" ; AR_ANH="fls-app"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT}/${AR_REPO}/${AR_ANH}:${TAG}"
SA_TEN="fls-staging-mcp"
SA_EMAIL="${SA_TEN}@${PROJECT}.iam.gserviceaccount.com"
DIEM_VAO="/app/tools/staging/app/vao_mcp.sh"
BM_DOC="fls-staging-pg-fls_doc" ; BM_KHOA="fls-staging-mcp-khoa" ; BM_OAUTH="fls-staging-mcp-oauth" ; BM_CHO="fls-staging-mcp-cho-phep"
BM_CUA_SA=("$BM_DOC" "$BM_KHOA" "$BM_OAUTH" "$BM_CHO")
BM_CAM=(fls-staging-jwt-secret fls-staging-pg-fls_ghi fls-staging-pg-fls_admin fls-staging-pg-postgres fls-staging-login fls-staging-phien)
G=(gcloud --project="$PROJECT" --quiet)
DO_MCP="${FLS_STG_DO_MCP:-$GOC/tools/staging/app/do_mcp.py}"      # bài thử thay bằng bộ đo giả

buoc() { printf '\n── %s\n' "$*"; }
TAI_KHOAN="$("${G[@]}" config get-value account 2>/dev/null | tr -d '[:space:]' || true)"
SO_PROJECT="$("${G[@]}" projects describe "$PROJECT" --format='value(projectNumber)' 2>/dev/null | tr -d '[:space:]' || true)"
URL_MONG="https://${SVC}-${SO_PROJECT}.${REGION}.run.app"
DK_BIEU_THUC="resource.name == \"projects/${PROJECT}/instances/${INSTANCE}\""
DK_TEN="fls-staging-mcp-chi-${INSTANCE}"
bm_co() { "${G[@]}" secrets describe "$1" --format='value(name)' >/dev/null 2>&1; }

if [ "$KIEM" -eq 0 ]; then
  [ -n "$TAI_KHOAN" ] || { echo "⛔ gcloud chưa đăng nhập (config get-value account rỗng)" >&2; exit 2; }
  [ -n "$SO_PROJECT" ] || { echo "⛔ không đọc được số project của $PROJECT" >&2; exit 2; }

  buoc "① bật API run · secretmanager · sqladmin"
  "${G[@]}" services enable run.googleapis.com secretmanager.googleapis.com sqladmin.googleapis.com

  buoc "② SA riêng $SA_TEN"
  if "${G[@]}" iam service-accounts describe "$SA_EMAIL" >/dev/null 2>&1; then echo "   có rồi"
  else "${G[@]}" iam service-accounts create "$SA_TEN" --display-name="FLS staging MCP (chi doc)" >/dev/null; echo "   đã tạo"; fi

  buoc "③ bí mật của MCP (⛔ in giá trị)"
  if bm_co "$BM_KHOA"; then echo "   $BM_KHOA: có rồi (⛔ xoay — xoay = mọi token/kết nối cũ chết)"
  else
    python3 -c 'import secrets; print(secrets.token_hex(64), end="")' \
      | "${G[@]}" secrets create "$BM_KHOA" --replication-policy=automatic --data-file=- >/dev/null
    echo "   $BM_KHOA: đã sinh 64 byte ngẫu nhiên"
  fi
  if [ "$OAUTH_NHAP" -eq 1 ]; then
    echo "   OAuth client Google (Console › APIs & Services › Credentials › OAuth client ID › Web application)"
    echo "   Authorized redirect URI phải là:  ${URL_MONG}/oauth/google/callback"
    read -r  -p "   Client ID: " GID
    read -rs -p "   Client secret (gõ ẨN): " GSEC; echo
    case "$GID" in *.apps.googleusercontent.com) ;; *) echo "⛔ Client ID phải kết thúc .apps.googleusercontent.com" >&2; exit 2 ;; esac
    [ "${#GSEC}" -ge 10 ] || { echo "⛔ client secret quá ngắn" >&2; exit 2; }
    J="$(GID="$GID" GSEC="$GSEC" python3 -c 'import json,os; print(json.dumps({"client_id":os.environ["GID"],"client_secret":os.environ["GSEC"]}), end="")')"
    if bm_co "$BM_OAUTH"; then printf '%s' "$J" | "${G[@]}" secrets versions add "$BM_OAUTH" --data-file=- >/dev/null
    else printf '%s' "$J" | "${G[@]}" secrets create "$BM_OAUTH" --replication-policy=automatic --data-file=- >/dev/null; fi
    unset GSEC J
    echo "   $BM_OAUTH: đã ghi phiên bản mới"
  fi
  if [ -n "$CHO_PHEP" ] || ! bm_co "$BM_CHO"; then
    DS="${CHO_PHEP:-$TAI_KHOAN}"
    if bm_co "$BM_CHO"; then printf '%s' "$DS" | "${G[@]}" secrets versions add "$BM_CHO" --data-file=- >/dev/null
    else printf '%s' "$DS" | "${G[@]}" secrets create "$BM_CHO" --replication-policy=automatic --data-file=- >/dev/null; fi
    echo "   $BM_CHO: $(printf '%s' "$DS" | tr ',' '\n' | grep -c .) email (⛔ in)"
  else echo "   $BM_CHO: giữ nguyên"; fi

  buoc "④ quyền SA: secretAccessor trên ĐÚNG ${#BM_CUA_SA[@]} bí mật · cloudsql.client CÓ ĐIỀU KIỆN"
  for b in "${BM_CUA_SA[@]}"; do
    if bm_co "$b"; then
      "${G[@]}" secrets add-iam-policy-binding "$b" --member="serviceAccount:$SA_EMAIL" \
          --role=roles/secretmanager.secretAccessor >/dev/null
    else echo "   ⚠ $b chưa có — bỏ qua"; fi
  done
  # ⭐ Mức DỰ ÁN có điều kiện (⛔ `--condition=None`): Cloud SQL ⛔ có chính sách IAM theo instance.
  "${G[@]}" projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA_EMAIL" \
      --role=roles/cloudsql.client --condition="expression=${DK_BIEU_THUC},title=${DK_TEN}" >/dev/null
  echo "   cloudsql.client ⇐ điều kiện: $DK_BIEU_THUC"

  OAUTH_CO=1; bm_co "$BM_OAUTH" || OAUTH_CO=0
  if [ "$OAUTH_CO" -eq 0 ]; then
    echo; echo "⛔ CHƯA có $BM_OAUTH ⇒ ⛔ deploy (máy sẽ tự từ chối chạy). Làm theo BG-372 §A bước ②, rồi chạy lại với --oauth-nhap."
    echo "   Authorized redirect URI:  ${URL_MONG}/oauth/google/callback"
  fi

  R_BUILD_RC=0
  if [ "$OAUTH_CO" -eq 1 ]; then
    buoc "⑤ ảnh $IMAGE"
    if "${G[@]}" artifacts docker images list "${REGION}-docker.pkg.dev/${PROJECT}/${AR_REPO}/${AR_ANH}" --include-tags \
         --format='value(tags)' 2>/dev/null | tr ',; ' '\n\n\n' | grep -qx "$TAG"; then
      echo "   tag $TAG có rồi ⇒ DÙNG LẠI (⛔ dựng)"
    else
      command -v git >/dev/null || { echo "⛔ không có git (cần cho git archive)" >&2; exit 2; }
      "${G[@]}" services enable cloudbuild.googleapis.com artifactregistry.googleapis.com
      CTX="$(mktemp -d)"
      trap 'rm -rf "$CTX"' EXIT
      bash "$GOC/tools/staging/ngu_canh_build.sh" "$GOC" "$CTX"
      "${G[@]}" builds submit "$CTX" --tag "$IMAGE" --timeout=1200 || R_BUILD_RC=$?
      [ "$R_BUILD_RC" -eq 0 ] || echo "⛔ BUILD_LOI: exit $R_BUILD_RC — bỏ ⑥, sang BÁO CÁO" >&2
    fi
  fi

  if [ "$OAUTH_CO" -eq 1 ] && [ "$R_BUILD_RC" -eq 0 ]; then
    buoc "⑥ Cloud Run $SVC ($REGION) — ⛔ IAP (claude.ai ⛔ qua được); OAuth của FLS ở tầng ứng dụng"
    CONN="$("${G[@]}" sql instances describe "$INSTANCE" --format='value(connectionName)')"
    [ -n "$CONN" ] || { echo "⛔ không đọc được connectionName của $INSTANCE — bước 01 chưa chạy?" >&2; exit 2; }
    R_DEPLOY_RC=0
    "${G[@]}" run deploy "$SVC" --region="$REGION" --image="$IMAGE" --service-account="$SA_EMAIL" \
        --allow-unauthenticated --ingress=all --port=8080 --add-cloudsql-instances="$CONN" \
        --cpu=1 --memory=1Gi --min-instances=0 --max-instances=1 --concurrency=20 --timeout=60 --cpu-boost \
        --command=bash --args="$DIEM_VAO" \
        --set-env-vars="FLS_STG_PROJECT=$PROJECT,FLS_STG_CONN=$CONN,FLS_MCP_URL=$URL_MONG" || R_DEPLOY_RC=$?
    [ "$R_DEPLOY_RC" -eq 0 ] || echo "⛔ DEPLOY_LOI: exit $R_DEPLOY_RC — sang BÁO CÁO (xem BG-372 §giả định M-2: chính sách tổ chức chặn allUsers?)" >&2
  fi
fi

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa mật khẩu/khoá/email) — chép từ dòng này tới hết, gửi lại"
export PROJECT REGION SVC IMAGE SA_EMAIL KIEM DIEM_VAO URL_MONG DK_BIEU_THUC TAI_KHOAN INSTANCE
export R_BUILD_RC="${R_BUILD_RC:-}" R_DEPLOY_RC="${R_DEPLOY_RC:-}"
export R_APIS="$("${G[@]}" services list --enabled --format='value(config.name)' 2>/dev/null | tr '\n' ' ' || true)"
export R_SA_CO="$("${G[@]}" iam service-accounts describe "$SA_EMAIL" --format='value(email)' >/dev/null 2>&1 && echo co || echo khong)"
export R_SVC="$("${G[@]}" run services describe "$SVC" --region="$REGION" --format=json 2>/dev/null || echo '{}')"
export R_RUN_IAM="$("${G[@]}" run services get-iam-policy "$SVC" --region="$REGION" --format=json 2>/dev/null || echo '')"
export R_PROJ_IAM="$("${G[@]}" projects get-iam-policy "$PROJECT" --format=json 2>/dev/null || echo '')"
export R_CONN="$("${G[@]}" sql instances describe "$INSTANCE" --format='value(connectionName)' 2>/dev/null || true)"
BM_JSON="{"
for b in "${BM_CUA_SA[@]}" "${BM_CAM[@]}"; do
  co=khong; bm_co "$b" && co=co
  pol="$("${G[@]}" secrets get-iam-policy "$b" --format=json 2>/dev/null || echo 'null')"
  [ -n "$pol" ] || pol=null
  BM_JSON="$BM_JSON\"$b\":{\"co\":\"$co\",\"pol\":$pol},"
done
export R_BM="${BM_JSON%,}}"
export BM_CUA_SA_DS="${BM_CUA_SA[*]}" BM_CAM_DS="${BM_CAM[*]}"
# Mặt NGOÀI — chỉ đo khi service đã có. Khoá ký đọc bằng quyền CHỦ, vào MÔI TRƯỜNG của bộ đo (⛔ dòng lệnh, ⛔ in).
R_DO=""
if [ "$(printf '%s' "$R_SVC" | python3 -c 'import json,sys
try: print(bool(json.load(sys.stdin).get("status")))
except ValueError: print(False)')" = True ]; then
  KHOA_DO="$("${G[@]}" secrets versions access latest --secret="$BM_KHOA" 2>/dev/null || true)"
  CHU_DO="$("${G[@]}" secrets versions access latest --secret="$BM_CHO" 2>/dev/null | cut -d, -f1 || true)"
  R_DO="$(FLS_MCP_KHOA_DO="$KHOA_DO" FLS_MCP_DO_CHU="$CHU_DO" python3 "$DO_MCP" --url "$URL_MONG" 2>/dev/null || echo 'do_mcp=loi:chay')"
  unset KHOA_DO CHU_DO
fi
export R_DO

python3 - <<'PY'
import json, os
e = os.environ
def js(k):
    try: return json.loads(e[k]) if e[k].strip() else None
    except ValueError: return None
svc = js("R_SVC") or {}
md = svc.get("metadata", {}) or {}
tpl = (svc.get("spec", {}) or {}).get("template", {}) or {}
tann = (tpl.get("metadata", {}) or {}).get("annotations", {}) or {}
tsp = tpl.get("spec", {}) or {}
ct = (tsp.get("containers") or [{}])[0]
env = {x.get("name"): x.get("value") for x in ct.get("env", []) or []}
st = svc.get("status", {}) or {}
san_sang = any(c.get("type") == "Ready" and c.get("status") == "True" for c in st.get("conditions", []) or [])
sa_m = f'serviceAccount:{e["SA_EMAIL"]}'
run_iam = js("R_RUN_IAM")
cong_khai = None if run_iam is None else any(
    b.get("role") == "roles/run.invoker" and "allUsers" in b.get("members", []) for b in run_iam.get("bindings", []) or [])
proj = js("R_PROJ_IAM")
cua_sa = None if proj is None else [b for b in proj.get("bindings", []) or [] if sa_m in b.get("members", [])]
dk_dung = None if cua_sa is None else sum(
    b.get("role") == "roles/cloudsql.client" and (b.get("condition") or {}).get("expression", "").replace("'", '"') == e["DK_BIEU_THUC"]
    for b in cua_sa)
bm = js("R_BM") or {}
def doc_duoc(ten):
    x = bm.get(ten) or {}
    pol = x.get("pol")
    if x.get("co") != "co":
        return None
    return any(b.get("role") in ("roles/secretmanager.secretAccessor", "roles/owner", "roles/editor",
                                 "roles/secretmanager.admin") and sa_m in b.get("members", [])
               for b in (pol or {}).get("bindings", []) or [])
cua = e["BM_CUA_SA_DS"].split(); cam = e["BM_CAM_DS"].split()
do = dict(x.split("=", 1) for x in e["R_DO"].splitlines() if "=" in x)
urls = set([st.get("url", "")] + list(st.get("urls") or []) + [ (svc.get("metadata", {}).get("annotations", {}) or {}).get("run.googleapis.com/urls", "") ])
url_tat_dinh = None if not svc else any(e["URL_MONG"] in u for u in urls if u)
def so(k):
    try: return int(do.get(k, ""))
    except ValueError: return None
hang = [
  ("project · vùng · service", f'{e["PROJECT"]} · {e["REGION"]} · {e["SVC"]}', None),
  ("⭐ URL MCP (thêm vào claude.ai)", e["URL_MONG"] + "/mcp", None),
  ("redirect URI khai ở OAuth client Google (Console)", e["URL_MONG"] + "/oauth/google/callback", None),
  ("API bật: run · secretmanager · sqladmin (đếm / 3)",
   len({"run.googleapis.com", "secretmanager.googleapis.com", "sqladmin.googleapis.com"} & set(e["R_APIS"].split())), 3),
  ("SA riêng fls-staging-mcp có", e["R_SA_CO"], "co"),
  *[(f"bí mật {b} có", (bm.get(b) or {}).get("co"), "co") for b in cua],
  *[(f"SA đọc được {b}", doc_duoc(b), True) for b in cua],
  ("SA đọc được bí mật NGOÀI 4 cái trên (đếm, trong số bí mật FLS có thật)",
   sum(bool(doc_duoc(b)) for b in cam), 0),
  ("binding MỨC DỰ ÁN của SA (đếm — chỉ cloudsql.client có điều kiện)", None if cua_sa is None else len(cua_sa), 1),
  ("cloudsql.client CÓ điều kiện = chỉ instance", dk_dung, 1),
  ("service sẵn sàng (Ready)", san_sang, True),
  ("service chạy đúng ảnh mong", ct.get("image"), e["IMAGE"]),
  ("service chạy bằng SA riêng", tsp.get("serviceAccountName"), e["SA_EMAIL"]),
  ("điểm vào = vao_mcp.sh", " ".join((ct.get("command") or []) + (ct.get("args") or [])), "bash " + e["DIEM_VAO"]),
  ("Cloud SQL gắn = instance fls-staging", tann.get("run.googleapis.com/cloudsql-instances"), e["R_CONN"] or "—"),
  ("số instance tối đa", tann.get("autoscaling.knative.dev/maxScale"), "1"),
  ("FLS_MCP_URL = URL tất định", env.get("FLS_MCP_URL"), e["URL_MONG"]),
  ("URL tất định có trong URL của service", url_tat_dinh, True),
  ("allUsers run.invoker (CỐ Ý — claude.ai ⛔ qua IAM/IAP; OAuth ở ứng dụng)", cong_khai, True),
  ("NGOÀI · ⛔ token ⇒ HTTP", do.get("khong_token"), "401"),
  ("NGOÀI · 401 mang resource_metadata (claude.ai bắt đầu đăng nhập)", do.get("www_resource_metadata"), "co"),
  ("NGOÀI · PRM resource = URL MCP", do.get("prm_resource_khop"), "True"),
  ("NGOÀI · PRM authorization_servers = [URL]", do.get("prm_as_khop"), "True"),
  ("NGOÀI · issuer OAuth = URL", do.get("as_issuer_khop"), "True"),
  ("NGOÀI · đăng ký client redirect lạ ⇒ HTTP", do.get("dang_ky_redirect_la"), "400"),
  ("NGOÀI · token ký khoá GIẢ ⇒ HTTP", do.get("token_khoa_gia"), "401"),
  ("NGOÀI · token aud SAI ⇒ HTTP", do.get("token_aud_sai"), "401"),
  ("NGOÀI · token HẾT HẠN ⇒ HTTP", do.get("token_het_han"), "401"),
  ("NGOÀI · token thật của NGƯỜI NGOÀI danh sách ⇒ HTTP", do.get("nguoi_ngoai"), "403"),
  ("NGOÀI · token của CHỦ ⇒ HTTP", do.get("chu_khoi_tao"), "200"),
  ("NGOÀI · chủ · liet_ke_bang: số bảng > 0", (so("chu_so_bang") or 0) > 0 if do else None, True),
  ("NGOÀI · chủ · số bảng (thông tin)", do.get("chu_so_bang", "—"), None),
  ("NGOÀI · chủ · bảng có ≥ 1 dòng (thông tin — 0 ⇒ chưa nạp 05)", do.get("chu_bang_co_dong", "—"), None),
  ("NGOÀI · chủ · truy_van_doc INSERT ⇒", do.get("chu_insert"), "chan"),
  ("NGOÀI · riêng tư: cột *email* / dòng PM mang 'Email Address'", do.get("rieng_tu_email"), "0/0"),
  ("NGOÀI · riêng tư: mẫu số cột / dòng PM có thô (thông tin, Đ3)", do.get("rieng_tu_mau_so", "—"), None),
  ("NGOÀI · chủ · cong (số cổng)", (so("chu_cong") or 0) >= 1 if do else None, True),
]
if e["KIEM"] != "1":
    def _so(v):
        try: return int(v)
        except (TypeError, ValueError): return None
    hang[3:3] = [("dựng ảnh (exit)", _so(e["R_BUILD_RC"]), 0), ("gcloud run deploy (exit)", _so(e["R_DEPLOY_RC"]), 0)]
do_ = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:72}  {gt}")
    else:
        ok = gt == mong
        do_ += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:70}  {gt!r}  (mong {mong!r})")
print(f"\n   ⭐ claude.ai › Settings › Connectors › Add custom connector › URL: {e['URL_MONG']}/mcp")
print("      (OAuth Client ID/Secret: ĐỂ TRỐNG — máy chủ hỗ trợ đăng ký động; xem BG-372 §B)")
che_do = "--kiem (chỉ đọc)" if e["KIEM"] == "1" else "dựng"
print(f"\n══ chế độ: {che_do} · KẾT: {'ĐẠT' if do_ == 0 else f'ĐỎ — {do_} mục khác mong'}")
raise SystemExit(1 if do_ else 0)
PY
