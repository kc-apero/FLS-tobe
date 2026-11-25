#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 07 — LINK WEB `https://…run.app` cho màn hình + API, SAU Google IAP · WO-363
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell (repo đã `git clone`), SAU 01 + 02 + 04 `KẾT: ĐẠT`.
#  ⛔ Claude KHÔNG vào GCP — chủ chạy, rồi gửi lại PHẦN "BÁO CÁO" ở cuối (⛔ mật khẩu/khoá, ⛔ email).
#
#    bash tools/staging/07_link_web.sh --project <P> --kiem                       # chỉ ĐỌC — đo trạng thái
#    bash tools/staging/07_link_web.sh --project <P>                              # dựng; app CHỈ-ĐỌC (vai fls_doc)
#    bash tools/staging/07_link_web.sh --project <P> --cho-vao a@x.com,b@y.com    # + cho những người này vào
#    bash tools/staging/07_link_web.sh --project <P> --che-do ghi --nguoi-ky <tên>   # app GHI được (vai fls_ghi) — để KÝ
#         ⛔ --nguoi-ky = tên đứng sau MỌI chữ ký (cửa phát MỘT thẻ chung — GAP-WEB-01); email IAP chỉ GHI NHẬT KÝ
#
#  Tuỳ chọn: --region (asia-southeast1) · --service (fls-staging-web) · --instance (fls-staging)
#            --tag (mặc định: SHA ngắn của HEAD; tag CHƯA có trong Artifact Registry ⇒ dựng ảnh như bước 03)
#
#  ── VÌ SAO Cloud Run + IAP tích hợp, ⛔ HTTPS Load Balancer + IAP (đo/so ở BG-364 §3) ──────────────────────
#   Cả hai đều cần MỘT thành phần nghe ngoài loopback rồi chuyển vào cửa 127.0.0.1:8088 (cửa ⛔ nới —
#   `GAP-WEB-01`). Cloud Run + IAP: URL `*.run.app` có sẵn (⛔ tên miền, ⛔ chứng chỉ), IAP chặn MỌI lối vào kể cả
#   `run.app` (tài liệu GCP), 1 lệnh deploy, scale-về-0 ≈ 0 USD khi bỏ không. LB + IAP: ≥ 8 tài nguyên + tên miền +
#   chứng chỉ, quy tắc chuyển tiếp ≈ 18 USD/tháng + VM luôn bật.
#
#  LÀM GÌ (mỗi việc: có rồi ⇒ bỏ qua, ⛔ phá gì đã có):
#   ① bật API: run · iap (+ cloudbuild · artifactregistry nếu phải dựng ảnh)
#   ② tạo tác tử dịch vụ IAP `service-<SỐ>@gcp-sa-iap.iam.gserviceaccount.com` (`gcloud services identity create`)
#   ③ ảnh: tag đã có trong Artifact Registry ⇒ DÙNG LẠI; chưa ⇒ dựng y bước 03 (ngữ cảnh `git archive`, ⛔ .gcloudignore)
#   ④ `gcloud run deploy --iap --no-allow-unauthenticated` · SA `fls-staging-app` (đã có cloudsql.client +
#      secretAccessor 3 bí mật app + artifactregistry.reader — ⛔ cấp thêm) · điểm vào `vao_cloud_run.sh` ·
#      `--max-instances 1` (MỘT thẻ chung, MỘT tiến trình ghi) · `--min-instances 0` · cổng 8080
#   ⑤ tác tử IAP được `roles/run.invoker` trên service; GỠ `allUsers`/`allAuthenticatedUsers` nếu có (⛔ lối tắt IAP)
#   ⑥ `roles/iap.httpsResourceAccessor` (IAP · cloud-run · service) cho TÀI KHOẢN NGƯỜI CHẠY + từng `--cho-vao`
#   ⓑ ĐĂNG NHẬP FLS (bổ sung chủ 24/11): lớp thứ hai SAU IAP nằm trong cổng `cong_iap.py` — tài khoản chung đặt bằng
#      `08_dat_dang_nhap.sh` (bí mật `fls-staging-login`, băm scrypt). CHẠY 08 TRƯỚC 07: dòng `TU_DO` đo lúc khởi động.
#   ⑦ BÁO CÁO: mỗi mục khai `mong`; ĐẠT/ĐỎ hai chiều; exit 1 khi ĐỎ. Đo NGOÀI (curl ⛔ cookie ⇒ 302 về Google ·
#      POST ⇒ 401) + đo TRONG container (dòng `TU_DO` từ nhật ký Cloud Run). In URL.
#
#  ⛔ KHÔNG làm ở bước 07: đổi quyền Cloud SQL (bước 02) · nạp dữ liệu (04) · "chạy chuỗi" HD2 (lệnh ⛔ HTTP —
#     vẫn ở VM bước 03, xem README §"Chuỗi HD2"). ⛔ đụng VM `fls-staging-app` (đường hầm SSH vẫn dùng được).
#  Tắt link: `gcloud run services delete <service> --region <R>` (chủ tự gõ — script ⛔ xoá gì).
#  Luật đo (CLAUDE.md Đ3·Đ5): mục ⛔ ĐO ĐƯỢC ⇒ ĐỎ (⛔ "không thấy lệch").
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="asia-southeast1" ; SVC="fls-staging-web" ; INSTANCE="fls-staging"
CHE_DO="doc" ; TAG="" ; KIEM=0 ; CHO_VAO="" ; NGUOI_KY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --project)   PROJECT="$2"; shift 2 ;;
    --region)    REGION="$2"; shift 2 ;;
    --service)   SVC="$2"; shift 2 ;;
    --instance)  INSTANCE="$2"; shift 2 ;;
    --che-do)    CHE_DO="$2"; shift 2 ;;
    --tag)       TAG="$2"; shift 2 ;;
    --cho-vao)   CHO_VAO="$2"; shift 2 ;;
    --nguoi-ky)  NGUOI_KY="$2"; shift 2 ;;
    --kiem)      KIEM=1; shift ;;
    -h|--help)   sed -n 2,40p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
case "$CHE_DO" in doc|ghi) ;; *) echo "⛔ --che-do phải là doc|ghi" >&2; exit 2 ;; esac
if [ "$CHE_DO" = ghi ]; then
  [ -n "$NGUOI_KY" ] || { echo "⛔ --che-do ghi đòi --nguoi-ky <tên> (tên đứng sau MỌI chữ ký; ⛔ mặc định thu@apero.vn)" >&2; exit 2; }
else
  [ -n "$NGUOI_KY" ] || NGUOI_KY="staging-doc"
fi
case "$NGUOI_KY" in thu@apero.vn|*[!A-Za-z0-9._@-]*) echo "⛔ --nguoi-ky chỉ [A-Za-z0-9._@-] và ⛔ là thu@apero.vn (mặc định của chay_cua.py)" >&2; exit 2 ;; esac
case "$SVC$REGION" in *[!a-z0-9-]*) echo "⛔ --service/--region chỉ gồm [a-z0-9-]" >&2; exit 2 ;; esac
if [ -n "$CHO_VAO" ]; then
  case "$CHO_VAO" in *[!A-Za-z0-9@._+,-]*|*,,*|,*|*,) echo "⛔ --cho-vao: danh sách email cách nhau dấu phẩy" >&2; exit 2 ;; esac
  IFS=',' read -ra DS_KIEM <<<"$CHO_VAO"
  for e in "${DS_KIEM[@]}"; do case "$e" in ?*@?*.?*) ;; *) echo "⛔ --cho-vao: '$e' ⛔ phải email" >&2; exit 2 ;; esac; done
fi
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }
command -v curl    >/dev/null || { echo "⛔ không có curl" >&2; exit 2; }
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -n "$TAG" ] || TAG="$(git -C "$GOC" rev-parse --short HEAD 2>/dev/null || echo thu)"

AR_REPO="fls" ; AR_ANH="fls-app"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT}/${AR_REPO}/${AR_ANH}:${TAG}"
SA_EMAIL="fls-staging-app@${PROJECT}.iam.gserviceaccount.com"
DIEM_VAO="/app/tools/staging/app/vao_cloud_run.sh"
CONG_RUN=8080
G=(gcloud --project="$PROJECT" --quiet)

buoc() { printf '\n── %s\n' "$*"; }
co() { "${G[@]}" "$@" >/dev/null 2>&1; }
TAI_KHOAN="$("${G[@]}" config get-value account 2>/dev/null | tr -d '[:space:]' || true)"
SO_PROJECT="$("${G[@]}" projects describe "$PROJECT" --format='value(projectNumber)' 2>/dev/null | tr -d '[:space:]' || true)"
TAC_TU_IAP="service-${SO_PROJECT}@gcp-sa-iap.iam.gserviceaccount.com"
# ⭐ `STG-WEB-R1-01`: ghim `aud` của JWT IAP — khuôn Cloud Run theo tài liệu "Securing your app with signed headers":
#   `/projects/PROJECT_NUMBER/locations/REGION/services/SERVICE_NAME`. Cổng TỪ CHỐI JWT IAP của app khác (aud khác)
#   và ghi dòng `IAP_AUD <aud> lech` ⇒ BÁO CÁO đối chiếu aud ĐO ĐƯỢC với aud đã ghim (khuôn sai ⇒ ĐỎ có tên).
AUD_MONG="/projects/${SO_PROJECT}/locations/${REGION}/services/${SVC}"

if [ "$KIEM" -eq 0 ]; then
  [ -n "$TAI_KHOAN" ] || { echo "⛔ gcloud chưa đăng nhập (config get-value account rỗng)" >&2; exit 2; }
  [ -n "$SO_PROJECT" ] || { echo "⛔ không đọc được số project của $PROJECT" >&2; exit 2; }

  buoc "① bật API run · iap"
  "${G[@]}" services enable run.googleapis.com iap.googleapis.com

  buoc "② tác tử dịch vụ IAP"
  # ⭐ Tác tử chỉ sinh khi có lệnh này (hoặc bật IAP lần đầu ở console) — thiếu nó thì ⑤ đỏ "does not exist".
  "${G[@]}" services identity create --service=iap.googleapis.com >/dev/null
  echo "   $TAC_TU_IAP"

  buoc "③ ảnh $IMAGE"
  if "${G[@]}" artifacts docker images list "${REGION}-docker.pkg.dev/${PROJECT}/${AR_REPO}/${AR_ANH}" --include-tags \
       --format='value(tags)' 2>/dev/null | tr ',; ' '\n\n\n' | grep -qx "$TAG"; then
    echo "   tag $TAG có rồi ⇒ DÙNG LẠI (⛔ dựng)"
    R_BUILD_RC=0
  else
    command -v git >/dev/null || { echo "⛔ không có git (cần cho git archive)" >&2; exit 2; }
    "${G[@]}" services enable cloudbuild.googleapis.com artifactregistry.googleapis.com
    CTX="$(mktemp -d)" ; BLOG="$(mktemp)"
    trap 'rm -rf "$CTX" "$BLOG"' EXIT
    # ⭐ y bước 03 (`STG-R2b-01` ⛔ .gcloudignore · `STG-R2b-05` `--tag` = bộ build CŨ ⛔ BuildKit).
    bash "$GOC/tools/staging/ngu_canh_build.sh" "$GOC" "$CTX"
    R_CTX_N="$(find "$CTX" -type f | wc -l | tr -d ' ')"
    R_BUILD_RC=0
    "${G[@]}" builds submit "$CTX" --tag "$IMAGE" --timeout=1200 2>&1 | tee "$BLOG" || R_BUILD_RC=$?
    R_TAI_N="$(sed -n 's/.*Creating temporary \(tarball \)\{0,1\}archive of \([0-9][0-9]*\) file(s).*/\2/p' "$BLOG" | tail -1)"
    [ "$R_BUILD_RC" -eq 0 ] || echo "⛔ BUILD_LOI: gcloud builds submit exit $R_BUILD_RC — bỏ ④–⑥, sang BÁO CÁO" >&2
  fi
fi

if [ "$KIEM" -eq 0 ] && [ "${R_BUILD_RC:-0}" -eq 0 ]; then
  buoc "④ Cloud Run $SVC ($REGION) — IAP BẬT, ⛔ cho người lạ"
  CONN="$("${G[@]}" sql instances describe "$INSTANCE" --format='value(connectionName)')"
  [ -n "$CONN" ] || { echo "⛔ không đọc được connectionName của $INSTANCE — bước 01 chưa chạy?" >&2; exit 2; }
  TRIEN=(run deploy "$SVC" --region="$REGION" --image="$IMAGE" --service-account="$SA_EMAIL"
         --no-allow-unauthenticated --iap --ingress=all --port="$CONG_RUN"
         --cpu=1 --memory=1Gi --min-instances=0 --max-instances=1 --cpu-boost --timeout=300
         --command=bash --args="$DIEM_VAO"
         --set-env-vars="FLS_STG_PROJECT=$PROJECT,FLS_STG_CONN=$CONN,FLS_STG_CHE_DO=$CHE_DO,FLS_STG_ACTOR=$NGUOI_KY,FLS_IAP_AUD=$AUD_MONG")
  DLOG="$(mktemp)"
  R_DEPLOY_RC=0
  "${G[@]}" "${TRIEN[@]}" 2>&1 | tee "$DLOG" || R_DEPLOY_RC=$?
  # ⚠ Giả định G-2 (BG-364): `--iap` có ở `gcloud run` GA (tài liệu hiện hành không ghi `beta`). Bản gcloud cũ
  #   chỉ có ở `beta` ⇒ đúng lời gcloud "unrecognized arguments: --iap" ⇒ thử lại MỘT lần bằng `gcloud beta`.
  if [ "$R_DEPLOY_RC" -ne 0 ] && grep -q "unrecognized arguments.*--iap" "$DLOG"; then
    echo "   gcloud GA ⛔ biết --iap ⇒ thử gcloud beta run deploy"
    R_DEPLOY_RC=0
    "${G[@]}" beta "${TRIEN[@]}" 2>&1 | tee "$DLOG" || R_DEPLOY_RC=$?
  fi
  rm -f "$DLOG"
  if [ "$R_DEPLOY_RC" -ne 0 ]; then
    echo "⛔ DEPLOY_LOI: gcloud run deploy exit $R_DEPLOY_RC — bỏ ⑤–⑥, sang BÁO CÁO" >&2
  else
    buoc "⑤ tác tử IAP gọi được service · ⛔ allUsers/allAuthenticatedUsers"
    "${G[@]}" run services add-iam-policy-binding "$SVC" --region="$REGION" \
        --member="serviceAccount:$TAC_TU_IAP" --role=roles/run.invoker >/dev/null
    echo "   $TAC_TU_IAP: run.invoker"
    CS="$("${G[@]}" run services get-iam-policy "$SVC" --region="$REGION" --format=json 2>/dev/null || echo '{}')"
    for m in allUsers allAuthenticatedUsers; do
      for r in $(printf '%s' "$CS" | python3 -c 'import json,sys
m=sys.argv[1]
for b in json.load(sys.stdin).get("bindings",[]):
    if m in b.get("members",[]): print(b["role"])' "$m"); do
        "${G[@]}" run services remove-iam-policy-binding "$SVC" --region="$REGION" --member="$m" --role="$r" >/dev/null
        echo "   ⚠ đã GỠ $m khỏi $r (lối vào ⛔ qua IAP)"
      done
    done

    N_THEM=0; [ -z "$CHO_VAO" ] || N_THEM="$(printf '%s' "$CHO_VAO" | tr ',' '\n' | grep -c .)"
    buoc "⑥ cho vào qua IAP (iap.httpsResourceAccessor): người chạy script + $N_THEM người --cho-vao (⛔ in email)"
    DS=("$TAI_KHOAN")
    if [ -n "$CHO_VAO" ]; then IFS=',' read -ra THEM <<<"$CHO_VAO"; DS+=("${THEM[@]}"); fi
    for e in "${DS[@]}"; do
      "${G[@]}" iap web add-iam-policy-binding --resource-type=cloud-run --service="$SVC" --region="$REGION" \
          --member="user:$e" --role=roles/iap.httpsResourceAccessor >/dev/null
    done
    echo "   ${#DS[@]} tài khoản (xem email bằng: gcloud iap web get-iam-policy --resource-type=cloud-run --service=$SVC --region=$REGION)"
    echo; echo "   Cloud Run cần ~10–60 giây để mở revision mới; nhật ký TU_DO có thể trễ ~1 phút ⇒ ĐỎ mục TRONG thì chạy lại --kiem."
  fi
fi

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa mật khẩu/khoá/email) — chép từ dòng này tới hết, gửi lại"
export PROJECT REGION SVC IMAGE TAG SA_EMAIL CHE_DO KIEM NGUOI_KY CONG_RUN DIEM_VAO TAI_KHOAN TAC_TU_IAP CHO_VAO AUD_MONG
export R_CTX_N="${R_CTX_N:-}" R_TAI_N="${R_TAI_N:-}" R_BUILD_RC="${R_BUILD_RC:-}" R_DEPLOY_RC="${R_DEPLOY_RC:-}"
export R_APIS="$("${G[@]}" services list --enabled --format='value(config.name)' 2>/dev/null | tr '\n' ' ' || true)"
export R_SVC="$("${G[@]}" run services describe "$SVC" --region="$REGION" --format=json 2>/dev/null || echo '{}')"
export R_RUN_IAM="$("${G[@]}" run services get-iam-policy "$SVC" --region="$REGION" --format=json 2>/dev/null || echo '')"
export R_IAP_IAM="$("${G[@]}" iap web get-iam-policy --resource-type=cloud-run --service="$SVC" --region="$REGION" --format=json 2>/dev/null || echo '')"
export R_DN_CO="$("${G[@]}" secrets describe fls-staging-login --format='value(name)' >/dev/null 2>&1 && echo co || echo khong)"
export R_DN_IAM="$("${G[@]}" secrets get-iam-policy fls-staging-login --format=json 2>/dev/null || echo '')"
export R_TT_CO="$("${G[@]}" secrets describe fls-staging-phien --format='value(name)' >/dev/null 2>&1 && echo co || echo khong)"
export R_TT_IAM="$("${G[@]}" secrets get-iam-policy fls-staging-phien --format=json 2>/dev/null || echo '')"
export R_IAP_AUD="$("${G[@]}" logging read "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"$SVC\" AND textPayload:\"IAP_AUD \"" \
    --limit=1 --freshness=7d --format='value(textPayload)' 2>/dev/null | head -1 || true)"
export R_TU_DO="$("${G[@]}" logging read "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"$SVC\" AND textPayload:\"TU_DO \"" \
    --limit=1 --freshness=7d --format='value(textPayload)' 2>/dev/null | head -1 || true)"
URL="$(printf '%s' "$R_SVC" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("status",{}).get("url",""))
except ValueError: print("")' 2>/dev/null || true)"
export URL
do_http() {   # $1 = phương thức, $2 = đường — ⛔ cookie, ⛔ header gì ⇒ "mã chuyển_tới"
  [ -n "$URL" ] || { echo "000 "; return; }
  curl -s -o /dev/null -w '%{http_code} %{redirect_url}' --max-time 20 -X "$1" "$URL$2" 2>/dev/null || echo "000 "
}
export R_HTTP_MAN="$(do_http GET /)"
export R_HTTP_API="$(do_http GET /api/fls/v1/gates)"
export R_HTTP_POST="$(do_http POST /api/fls/v1/config/fx/202601/sign)"

python3 - <<'PY'
import json, os, urllib.parse
e = os.environ
def js(k):
    try: return json.loads(e[k]) if e[k].strip() else None
    except ValueError: return None
svc = js("R_SVC") or {}
md = svc.get("metadata", {}) or {}
ann = md.get("annotations", {}) or {}
tpl = (svc.get("spec", {}) or {}).get("template", {}) or {}
tann = (tpl.get("metadata", {}) or {}).get("annotations", {}) or {}
tsp = tpl.get("spec", {}) or {}
ct = (tsp.get("containers") or [{}])[0]
env = {x.get("name"): x.get("value") for x in ct.get("env", []) or []}
st = svc.get("status", {}) or {}
san_sang = any(c.get("type") == "Ready" and c.get("status") == "True" for c in st.get("conditions", []) or [])
run_iam, iap_iam = js("R_RUN_IAM"), js("R_IAP_IAM")
def thanh_vien(pol, vai):
    if pol is None: return None
    return {m for b in pol.get("bindings", []) or [] if b.get("role") == vai for m in b.get("members", [])}
inv = thanh_vien(run_iam, "roles/run.invoker")
cong_khai = None if run_iam is None else sum(m in ("allUsers", "allAuthenticatedUsers")
                                              for b in run_iam.get("bindings", []) or [] for m in b.get("members", []))
vao = thanh_vien(iap_iam, "roles/iap.httpsResourceAccessor")
dn_doc = thanh_vien(js("R_DN_IAM"), "roles/secretmanager.secretAccessor")
sa_m = f'serviceAccount:{e["SA_EMAIL"]}'
tt_iam = js("R_TT_IAM")
tt_quyen = None if tt_iam is None else (sa_m in (thanh_vien(tt_iam, "roles/secretmanager.secretAccessor") or set())
                                        and sa_m in (thanh_vien(tt_iam, "roles/secretmanager.secretVersionManager") or set()))
aud_do = e["R_IAP_AUD"].split()                       # ["IAP_AUD", "<aud>"] hoặc [..., "lech"]
aud_khop = (aud_do[1] == e["AUD_MONG"] and len(aud_do) == 2) if len(aud_do) >= 2 and aud_do[0] == "IAP_AUD" else "chưa đo (chưa ai vào link)"
can_vao = ["user:" + x for x in ([e["TAI_KHOAN"]] if e["TAI_KHOAN"] else []) + [y for y in e["CHO_VAO"].split(",") if y]]
iap_bat = ann.get("run.googleapis.com/iap-enabled")           # ⚠ giả định G-3 (BG-364): khoá chú thích này
def http(k):
    ma, _, toi = e[k].partition(" ")
    return ma, urllib.parse.urlparse(toi.strip()).hostname or ""
man_ma, man_toi = http("R_HTTP_MAN")
api_ma, api_toi = http("R_HTTP_API")
post_ma, _ = http("R_HTTP_POST")
ve_google = lambda h: h == "accounts.google.com" or h.endswith(".google.com") or h.endswith(".googleapis.com")
tu = dict(x.split("=", 1) for x in e["R_TU_DO"].split()[1:] if "=" in x) if e["R_TU_DO"].startswith("TU_DO ") else {}
# ⭐ "đường vào ⛔ qua IAP" — đếm mọi lối đã biết: IAP tắt · thành viên công khai · trả 200 khi ⛔ cookie. Mục ⛔ đo được ⇒ None ⇒ ĐỎ.
loi_tat = None if (not svc or run_iam is None or man_ma == "000") else \
    (iap_bat != "true") + (cong_khai or 0) + (man_ma == "200") + (api_ma == "200")
hang = [
  ("project · vùng · service", f'{e["PROJECT"]} · {e["REGION"]} · {e["SVC"]}', None),
  ("ảnh mong", e["IMAGE"], None),
  ("API bật: run · iap (đếm / 2)", len({"run.googleapis.com", "iap.googleapis.com"} & set(e["R_APIS"].split())), 2),
  ("service Cloud Run sẵn sàng (Ready)",              san_sang,                                             True),
  ("service chạy đúng ảnh mong",                      ct.get("image"),                                      e["IMAGE"]),
  ("service chạy bằng SA",                            tsp.get("serviceAccountName"),                        e["SA_EMAIL"]),
  ("điểm vào = vao_cloud_run.sh",                     " ".join((ct.get("command") or []) + (ct.get("args") or [])), "bash " + e["DIEM_VAO"]),
  ("cổng container ($PORT)",                          ((ct.get("ports") or [{}])[0]).get("containerPort"),  int(e["CONG_RUN"])),
  ("số instance tối đa (MỘT thẻ chung)",               tann.get("autoscaling.knative.dev/maxScale"),         "1"),
  ("chế độ app",                                      env.get("FLS_STG_CHE_DO"),                            e["CHE_DO"]),
  ("actor của mọi chữ ký",                            env.get("FLS_STG_ACTOR"),                             e["NGUOI_KY"]),
  ("IAP bật trên service (chú thích run.googleapis.com/iap-enabled)", iap_bat,                              "true"),
  ("tác tử IAP có run.invoker",                       None if inv is None else f'serviceAccount:{e["TAC_TU_IAP"]}' in inv, True),
  ("thành viên allUsers/allAuthenticatedUsers (đếm)", cong_khai,                                            0),
  ("cho vào qua IAP: tài khoản mong có quyền (đếm)",  None if vao is None else sum(x in vao for x in can_vao), len(can_vao)),
  ("cho vào qua IAP: tổng tài khoản có quyền (thông tin)", None if vao is None else len(vao),               None),
  ("NGOÀI · GET / ⛔ cookie ⇒ HTTP",                    man_ma,                                               "302"),
  ("NGOÀI · GET / ⛔ cookie ⇒ chuyển tới trang Google", ve_google(man_toi),                                  True),
  ("NGOÀI · chuyển tới (máy chủ — thông tin)",         man_toi or "—",                                       None),
  ("NGOÀI · GET API ⛔ cookie ⇒ HTTP",                  api_ma,                                               "302"),
  ("NGOÀI · POST API ⛔ cookie ⇒ HTTP",                 post_ma,                                              "401"),
  ("đường vào ⛔ qua IAP (đếm: IAP tắt · công khai · 200 khi ⛔ cookie)", loi_tat,                            0),
  ("TRONG container · dòng TU_DO của revision đang chạy", bool(tu) and tu.get("revision") == st.get("latestReadyRevisionName"), True),
  ("TRONG · màn hình / qua cửa ⇒ HTTP",                tu.get("man_hinh"),                                   "200"),
  ("TRONG · API ⛔ thẻ ⇒ HTTP",                          tu.get("api_khong_the"),                              "401"),
  ("TRONG · cửa CHỈ nghe 127.0.0.1",                   tu.get("nghe_cua"),                                   "127.0.0.1:8088"),
  ("TRONG · cổng: yêu cầu ⛔ JWT IAP ⇒ HTTP",           tu.get("cong_khong_iap"),                             "403"),
  ("TRONG · cổng: JWT IAP chữ ký GIẢ ⇒ HTTP",          tu.get("cong_iap_gia"),                               "403"),
  ("ĐĂNG NHẬP · bí mật fls-staging-login có (chạy 08 trước)", e["R_DN_CO"],                            "co"),
  ("ĐĂNG NHẬP · SA đọc được bí mật đăng nhập",       None if dn_doc is None else f'serviceAccount:{e["SA_EMAIL"]}' in dn_doc, True),
  ("TRONG · tài khoản đăng nhập FLS lúc khởi động",  tu.get("dang_nhap"),                                  "san_sang"),
  ("ĐĂNG NHẬP · trạng thái phiên fls-staging-phien có (08)", e["R_TT_CO"],                                "co"),
  ("ĐĂNG NHẬP · SA đọc + ghi phiên bản trạng thái phiên", tt_quyen,                                         True),
  ("TRONG · trạng thái phiên đọc được lúc khởi động", tu.get("trang_thai"),                                 "san_sang"),
  ("aud ghim trong service (FLS_IAP_AUD = khuôn Cloud Run)", env.get("FLS_IAP_AUD"),                        e["AUD_MONG"]),
  ("TRONG · cổng chạy với aud ghim",                  tu.get("aud"),                                        "ghim"),
  ("aud IAP ĐO trong nhật ký = aud ghim (mở link 1 lần rồi --kiem)", aud_khop,                             True),
  ("aud IAP đo trong nhật ký (thông tin)",            " ".join(aud_do[1:]) or "—",                          None),
  ("TRONG · khoá công khai IAP lấy được (đếm ≥ 1)",    (tu.get("jwks", "0").isdigit() and int(tu["jwks"]) >= 1) if tu else None, True),
]
if e["KIEM"] != "1":
    def _so(v):
        try: return int(v)
        except (TypeError, ValueError): return None
    them = [("gcloud run deploy (exit)", _so(e["R_DEPLOY_RC"]), 0)]
    if e["R_CTX_N"]:            # đã DỰNG ảnh ở lượt này (tag chưa có) — y mục bước 03
        ctx_n, tai_n = _so(e["R_CTX_N"]), _so(e["R_TAI_N"])
        them = [("ngữ cảnh build · tệp ngữ cảnh / tệp gcloud tải lên (đếm)", f"{ctx_n} / {tai_n}", None),
                ("ngữ cảnh build · tệp tải lên = tệp ngữ cảnh (≠ 0)",
                 None if ctx_n is None or tai_n is None else (tai_n == ctx_n and ctx_n > 0), True),
                ("dựng ảnh · gcloud builds submit (exit)", _so(e["R_BUILD_RC"]), 0)] + them
    hang[2:2] = them
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:72}  {gt}")
    else:
        ok = gt == mong
        do += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:70}  {gt!r}  (mong {mong!r})")
print(f"\n   ⭐ LINK: {e['URL'] or '— (chưa có service)'}")
print("      mở bằng trình duyệt ⇒ đăng nhập Google ⇒ /login (tài khoản chung của 08) ⇒ màn hình FLS")
che_do = "--kiem (chỉ đọc)" if e["KIEM"] == "1" else "dựng"
print(f"\n══ chế độ: {che_do} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
