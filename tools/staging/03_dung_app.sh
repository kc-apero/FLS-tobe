#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 03 — dựng ẢNH + VM chạy CỬA API + MÀN HÌNH (người test vào bằng IAP SSH tunnel)
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell (đã `git clone` repo), SAU khi bước 01 + 02 báo `KẾT: ĐẠT`.
#  ⛔ Claude KHÔNG vào GCP (quyết chủ 20/11) — chủ chạy, rồi gửi lại PHẦN "BÁO CÁO" ở cuối (⛔ mật khẩu/khoá).
#
#    bash tools/staging/03_dung_app.sh --project <PROJECT_ID> --kiem                 # chỉ ĐỌC — đo trạng thái
#    bash tools/staging/03_dung_app.sh --project <PROJECT_ID>                        # dựng, app CHỈ-ĐỌC (vai fls_doc)
#    bash tools/staging/03_dung_app.sh --project <PROJECT_ID> --che-do ghi           # app GHI được (vai fls_ghi) — để người test KÝ
#    … --cap-quyen a@x.com,b@y.com                                                    # cho những người này vào (xem dưới)
#
#  Tuỳ chọn: --region (asia-southeast1) · --zone (<region>-b) · --vm (fls-staging-app) · --may (e2-small)
#            --instance (fls-staging — tên máy Cloud SQL, ⛔ đổi nếu bước 01 đổi) · --tag (mặc định: SHA ngắn của HEAD)
#
#  ── VÌ SAO VM + IAP, ⛔ Cloud Run (đo ở BG-326) ──────────────────────────────────────────────────────
#   Cửa API TỰ TỪ CHỐI phục vụ màn hình ngoài loopback (`fls.api.cua.kiem_phuc_vu_tep`, `GAP-WEB-01`: vỏ màn hình
#   ra TRƯỚC thẻ và `phien.js` phát MỘT thẻ `ke_toan` chung cho bất kỳ ai chạm tới cổng). ⇒ Hàng rào truy cập phải
#   nằm NGOÀI ứng dụng, và ứng dụng phải NGHE 127.0.0.1. Trên VM: container `--network host` nghe 127.0.0.1:8088,
#   VM ⛔ có firewall mở vào (chỉ dải IAP cho SSH), người test mở `gcloud compute ssh … --tunnel-through-iap -- -L`
#   (SSH forward đáp vào loopback của VM). Danh tính = IAM (có nhật ký ai mở tunnel). Cloud Run buộc cổng 0.0.0.0
#   (⇒ phải thêm một proxy sidecar tự viết đứng ở chỗ ⛔ nới luật từ chối) — ⛔ chọn.
#
#  LÀM GÌ (mỗi việc: có rồi ⇒ bỏ qua, ⛔ phá gì đã có):
#   ① bật API: compute · artifactregistry · cloudbuild · iap
#   ② kho ảnh Artifact Registry `fls` + SA `fls-staging-app` được ĐỌC (`artifactregistry.reader`)
#   ③ dựng ảnh bằng Cloud Build. ⛔⛔ Ngữ cảnh build = `git archive HEAD -- <danh sách cho phép>` ⇒ chỉ tệp ĐÃ COMMIT:
#      `sao_luu/` · `hien_vat/` · `Input_Raw/` · `.env*` (đều gitignore) ⛔ thể nào lên Cloud Build
#   ④ firewall: CHẶN mọi vào VM (tag `fls-stg-app`, ưu tiên 900) + CHO riêng dải IAP vào cổng 22 (ưu tiên 800)
#   ⑤ VM Debian 12 gắn SA `fls-staging-app` (đọc bí mật + nối Cloud SQL) — `startup-script` = `vm_khoi_dong.sh`:
#      cài docker → kéo ảnh → `docker run --network host` (vao.sh: bí mật từ Secret Manager → Auth Proxy → cửa)
#   ⑥ (--cap-quyen) cấp từng người: `roles/compute.osLogin` trên VM + `roles/iap.tunnelResourceAccessor`
#   ⑦ BÁO CÁO: mỗi mục khai `mong`; ĐẠT/ĐỎ; exit 1 khi ĐỎ; kể cả ĐO TRONG VM qua IAP (container sống · cổng 8088
#      chỉ nghe 127.0.0.1 · gọi không thẻ ⇒ 401)
#
#  ⛔ KHÔNG làm ở bước 03: nạp dữ liệu (bước 04).
#  Chi phí: ước tính ở BG-326 §Đo — ⛔ đo được từ đây (⛔ vào GCP); tự kiểm Billing. Tắt VM ngoài giờ test:
#    gcloud compute instances stop <VM> --zone <ZONE>      (bật lại: `start`; container tự lên — `--restart=always`)
#
#  Luật đo (CLAUDE.md Đ3·Đ5): mỗi mục có `mong`; mục ⛔ ĐO ĐƯỢC ⇒ ĐỎ (không phải "không thấy lệch").
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="asia-southeast1" ; ZONE="" ; VM="fls-staging-app" ; MAY="e2-small" ; INSTANCE="fls-staging"
CHE_DO="doc" ; TAG="" ; KIEM=0 ; CAP_QUYEN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --project)   PROJECT="$2"; shift 2 ;;
    --region)    REGION="$2"; shift 2 ;;
    --zone)      ZONE="$2"; shift 2 ;;
    --vm)        VM="$2"; shift 2 ;;
    --may)       MAY="$2"; shift 2 ;;
    --instance)  INSTANCE="$2"; shift 2 ;;
    --che-do)    CHE_DO="$2"; shift 2 ;;
    --tag)       TAG="$2"; shift 2 ;;
    --cap-quyen) CAP_QUYEN="$2"; shift 2 ;;
    --kiem)      KIEM=1; shift ;;
    -h|--help)   sed -n 2,45p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
case "$CHE_DO" in doc|ghi) ;; *) echo "⛔ --che-do phải là doc|ghi" >&2; exit 2 ;; esac
case "$VM$MAY$REGION" in *[!a-z0-9-]*) echo "⛔ --vm/--may/--region chỉ gồm [a-z0-9-]" >&2; exit 2 ;; esac
if [ -n "$CAP_QUYEN" ]; then
  case "$CAP_QUYEN" in *[!A-Za-z0-9@._+,-]*) echo "⛔ --cap-quyen: danh sách email cách nhau dấu phẩy" >&2; exit 2 ;; esac
fi
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
[ -n "$ZONE" ] || ZONE="${REGION}-b"
if [ "$KIEM" -eq 0 ]; then
  command -v git >/dev/null || { echo "⛔ không có git (cần cho git archive)" >&2; exit 2; }
  git -C "$GOC" rev-parse --git-dir >/dev/null 2>&1 || { echo "⛔ $GOC ⛔ phải repo git (ngữ cảnh build lấy từ git archive)" >&2; exit 2; }
fi
[ -n "$TAG" ] || TAG="$(git -C "$GOC" rev-parse --short HEAD 2>/dev/null || echo thu)"

AR_REPO="fls" ; AR_ANH="fls-app"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT}/${AR_REPO}/${AR_ANH}:${TAG}"
SA_NAME="fls-staging-app" ; SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
NET_TAG="fls-stg-app" ; FW_DENY="fls-stg-chan-vao" ; FW_IAP="fls-stg-cho-iap-ssh"
PRI_DENY=900 ; PRI_IAP=800 ; DAI_IAP="35.235.240.0/20"
APIS=(compute.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com iap.googleapis.com)
G=(gcloud --project="$PROJECT" --quiet)

buoc() { printf '\n── %s\n' "$*"; }
co() { "${G[@]}" "$@" >/dev/null 2>&1; }

if [ "$KIEM" -eq 0 ]; then
  buoc "① bật API"
  "${G[@]}" services enable "${APIS[@]}"

  buoc "② kho ảnh $AR_REPO ($REGION) + SA đọc được"
  if co artifacts repositories describe "$AR_REPO" --location="$REGION"; then echo "   có rồi ⇒ bỏ qua tạo"
  else "${G[@]}" artifacts repositories create "$AR_REPO" --repository-format=docker --location="$REGION" \
         --description="FLS staging — ảnh cửa API + màn hình"; fi
  "${G[@]}" artifacts repositories add-iam-policy-binding "$AR_REPO" --location="$REGION" \
      --member="serviceAccount:$SA_EMAIL" --role=roles/artifactregistry.reader >/dev/null
  echo "   $SA_EMAIL: artifactregistry.reader"

  buoc "③ dựng ảnh $IMAGE (ngữ cảnh = git archive HEAD — ⛔ dữ liệu gitignore)"
  CTX="$(mktemp -d)"
  trap 'rm -rf "$CTX"' EXIT
  git -C "$GOC" archive --format=tar HEAD -- Dockerfile .dockerignore .gcloudignore requirements.txt \
      fls tools docs/ITL/_tools tests/fixture | tar -x -C "$CTX"
  echo "   ngữ cảnh: $(find "$CTX" -type f | wc -l | tr -d ' ') tệp, commit $(git -C "$GOC" rev-parse --short HEAD)"
  "${G[@]}" builds submit "$CTX" --tag "$IMAGE" --timeout=1200

  buoc "④ firewall: chặn mọi vào VM · chỉ IAP vào cổng 22"
  if co compute firewall-rules describe "$FW_DENY"; then echo "   $FW_DENY: có rồi"
  else "${G[@]}" compute firewall-rules create "$FW_DENY" --direction=INGRESS --action=DENY --rules=all \
         --source-ranges=0.0.0.0/0 --priority="$PRI_DENY" --target-tags="$NET_TAG" \
         --description="FLS staging: ⛔ mở vào VM app — vào bằng IAP tunnel"; fi
  if co compute firewall-rules describe "$FW_IAP"; then echo "   $FW_IAP: có rồi"
  else "${G[@]}" compute firewall-rules create "$FW_IAP" --direction=INGRESS --action=ALLOW --rules=tcp:22 \
         --source-ranges="$DAI_IAP" --priority="$PRI_IAP" --target-tags="$NET_TAG" \
         --description="FLS staging: SSH chỉ từ dải IAP TCP forwarding"; fi

  buoc "⑤ VM $VM ($ZONE · $MAY)"
  CONN="$("${G[@]}" sql instances describe "$INSTANCE" --format='value(connectionName)')"
  [ -n "$CONN" ] || { echo "⛔ không đọc được connectionName của $INSTANCE — bước 01 chưa chạy?" >&2; exit 2; }
  if co compute instances describe "$VM" --zone="$ZONE"; then
    echo "   có rồi ⇒ cập nhật ảnh/chế độ rồi KHỞI ĐỘNG LẠI (startup-script kéo ảnh mới)"
    "${G[@]}" compute instances add-metadata "$VM" --zone="$ZONE" \
        --metadata="fls-image=$IMAGE,fls-che-do=$CHE_DO,fls-project=$PROJECT,fls-conn=$CONN"
    "${G[@]}" compute instances reset "$VM" --zone="$ZONE"
  else
    "${G[@]}" compute instances create "$VM" --zone="$ZONE" --machine-type="$MAY" \
        --image-family=debian-12 --image-project=debian-cloud --boot-disk-size=20GB --boot-disk-type=pd-balanced \
        --service-account="$SA_EMAIL" --scopes=cloud-platform --tags="$NET_TAG" \
        --shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring \
        --metadata="enable-oslogin=TRUE,fls-image=$IMAGE,fls-che-do=$CHE_DO,fls-project=$PROJECT,fls-conn=$CONN" \
        --metadata-from-file="startup-script=$GOC/tools/staging/vm_khoi_dong.sh"
  fi

  if [ -n "$CAP_QUYEN" ]; then
    buoc "⑥ cấp quyền vào cho: $CAP_QUYEN"
    IFS=',' read -ra DS <<<"$CAP_QUYEN"
    for e in "${DS[@]}"; do
      "${G[@]}" compute instances add-iam-policy-binding "$VM" --zone="$ZONE" \
          --member="user:$e" --role=roles/compute.osLogin >/dev/null
      "${G[@]}" projects add-iam-policy-binding "$PROJECT" --member="user:$e" \
          --role=roles/iap.tunnelResourceAccessor --condition=None >/dev/null
      echo "   $e: osLogin (trên VM) + iap.tunnelResourceAccessor (project)"
    done
  fi
  echo; echo "   chờ VM khởi động xong (~2–4 phút lần đầu: cài docker + kéo ảnh) rồi chạy lại với --kiem để đo."
fi

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa mật khẩu/khoá) — chép từ dòng này tới hết, gửi lại"
export PROJECT REGION ZONE VM IMAGE TAG SA_EMAIL NET_TAG FW_DENY FW_IAP PRI_DENY DAI_IAP CHE_DO KIEM AR_REPO AR_ANH
export R_APIS="$("${G[@]}" services list --enabled --format='value(config.name)' 2>/dev/null | tr '\n' ' ' || true)"
export R_REPO="$("${G[@]}" artifacts repositories describe "$AR_REPO" --location="$REGION" --format='value(name)' 2>/dev/null || true)"
export R_ANH="$("${G[@]}" artifacts docker images list "${REGION}-docker.pkg.dev/${PROJECT}/${AR_REPO}/${AR_ANH}" --include-tags --format='value(tags)' 2>/dev/null | tr '\n' ' ' || true)"
export R_REPO_IAM="$("${G[@]}" artifacts repositories get-iam-policy "$AR_REPO" --location="$REGION" --format=json 2>/dev/null || echo '{}')"
export R_VM="$("${G[@]}" compute instances describe "$VM" --zone="$ZONE" --format=json 2>/dev/null || echo '{}')"
export R_FW="$("${G[@]}" compute firewall-rules list --format=json 2>/dev/null || echo '[]')"
# Đo TRONG VM qua IAP SSH (chỉ đọc). Mỗi dòng một sự kiện; ⛔ in bí mật.
DO_TRONG='echo "container=$(sudo docker inspect -f {{.State.Status}} fls-app 2>/dev/null || echo none)";
echo "nghe=$(ss -ltnH "sport = :8088" 2>/dev/null | awk "{print \$4}" | sort -u | tr "\n" ,)";
echo "http_khong_the=$(curl -s -o /dev/null -w %{http_code} --max-time 10 http://127.0.0.1:8088/api/fls/v1/gates 2>/dev/null || echo 000)";
echo "http_man_hinh=$(curl -s -o /dev/null -w %{http_code} --max-time 10 http://127.0.0.1:8088/ 2>/dev/null || echo 000)"'
export R_TRONG="$("${G[@]}" compute ssh "$VM" --zone="$ZONE" --tunnel-through-iap --command="$DO_TRONG" 2>/dev/null || true)"

python3 - <<'PY'
import ipaddress, json, os
e = os.environ
def js(k, mac):
    try: return json.loads(e[k] or mac)
    except ValueError: return json.loads(mac)
vm, fw, iam = js("R_VM", "{}"), js("R_FW", "[]"), js("R_REPO_IAM", "{}")
meta = {i.get("key"): i.get("value") for i in vm.get("metadata", {}).get("items", [])}
sa = (vm.get("serviceAccounts") or [{}])[0].get("email")
ip = None
for ni in vm.get("networkInterfaces", []):
    for ac in ni.get("accessConfigs", []):
        ip = ac.get("natIP") or ip
trong = dict(l.split("=", 1) for l in e["R_TRONG"].splitlines() if "=" in l)
cap = set(e["R_APIS"].split())
can = {"compute.googleapis.com", "artifactregistry.googleapis.com", "cloudbuild.googleapis.com", "iap.googleapis.com"}
reader = any("roles/artifactregistry.reader" == b.get("role") and f"serviceAccount:{e['SA_EMAIL']}" in b.get("members", [])
             for b in iam.get("bindings", []))
tag, pri_deny, iap = e["NET_TAG"], int(e["PRI_DENY"]), ipaddress.ip_network(e["DAI_IAP"])

def ap_dung(r):                      # luật áp lên VM của ta?
    tt = r.get("targetTags")
    return not r.get("disabled") and r.get("direction") == "INGRESS" and (not tt or tag in tt)
def ngoai_iap(r):                    # có nguồn ⛔ nằm trọn trong dải IAP?
    return any(not ipaddress.ip_network(s, strict=False).subnet_of(iap) for s in r.get("sourceRanges", []) or ["0.0.0.0/0"])
# ⭐ "Mở ra ngoài" = luật ALLOW áp lên VM, có nguồn NGOÀI dải IAP, mà ⛔ bị luật DENY (mọi giao thức) áp lên VM đè
#   (GCP: số ưu tiên NHỎ hơn thắng; bằng nhau thì DENY thắng). Nhờ vậy `default-allow-ssh` (65534, 0.0.0.0/0) chỉ
#   ⛔ tính khi luật chặn của ta MẤT — và một luật ALLOW ưu tiên 700 ta lỡ thêm thì bị tính.
chan_tat_ca = [r.get("priority", 1000) for r in fw if ap_dung(r) and any(x.get("IPProtocol") == "all" for x in r.get("denied") or [])]
mo = [r["name"] for r in fw if ap_dung(r) and r.get("allowed") and ngoai_iap(r)
      and not any(d <= r.get("priority", 1000) for d in chan_tat_ca)]
chan = [r for r in fw if r.get("name") == e["FW_DENY"] and ap_dung(r) and r.get("denied")]
cho_iap = [r for r in fw if r.get("name") == e["FW_IAP"] and ap_dung(r) and r.get("allowed")
           and all(ipaddress.ip_network(s, strict=False).subnet_of(iap) for s in r.get("sourceRanges", [])) and r.get("sourceRanges")]
nghe = [x for x in trong.get("nghe", "").split(",") if x]
hang = [
  ("project · vùng · zone · VM", f'{e["PROJECT"]} · {e["REGION"]} · {e["ZONE"]} · {e["VM"]}', None),
  ("ảnh mong", e["IMAGE"], None),
  ("API bật (đếm / 4)",           len(can & cap),                                     4),
  ("kho ảnh Artifact Registry",   bool(e["R_REPO"]),                                  True),
  ("ảnh có tag mong",             e["TAG"] in e["R_ANH"].split(),                     True),
  ("SA fls-staging-app đọc được kho ảnh", reader,                                     True),
  ("VM trạng thái",               vm.get("status"),                                   "RUNNING"),
  ("VM chạy bằng SA",             sa,                                                 e["SA_EMAIL"]),
  ("VM gắn tag firewall",         tag in (vm.get("tags") or {}).get("items", []),    True),
  ("VM dùng OS Login",            str(meta.get("enable-oslogin", "")).upper(),        "TRUE"),
  ("VM chạy đúng ảnh mong",       meta.get("fls-image"),                              e["IMAGE"]),
  ("VM chế độ app",               meta.get("fls-che-do"),                             e["CHE_DO"]),
  ("VM IP ngoài (thông tin — Cloud SQL cần đường ra)", ip or "—",                     None),
  ("firewall: luật CHẶN vào (tag, ưu tiên 900)", len(chan),                           1),
  ("firewall: luật cho IAP vào cổng 22", len(cho_iap),                                1),
  ("firewall: luật ALLOW áp lên VM, nguồn ngoài dải IAP, ⛔ bị DENY đè (đếm)", len(mo) if fw else None, 0),   # Đ3: ⛔ đọc được luật nào ⇒ ĐỎ, ⛔ "0 luật mở"
  ("TRONG VM · container fls-app", trong.get("container"),                            "running"),
  ("TRONG VM · cổng 8088 nghe (số địa chỉ)", len(nghe),                               1),
  ("TRONG VM · cổng 8088 chỉ nghe 127.0.0.1", nghe == ["127.0.0.1:8088"],             True),
  ("TRONG VM · gọi API không thẻ ⇒ HTTP",  trong.get("http_khong_the"),               "401"),
  ("TRONG VM · màn hình / ⇒ HTTP",         trong.get("http_man_hinh"),                "200"),
]
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:70}  {gt}")
    else:
        ok = gt == mong
        do += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:68}  {gt!r}  (mong {mong!r})")
che_do = "--kiem (chỉ đọc)" if e["KIEM"] == "1" else "dựng"
print(f"\n══ chế độ: {che_do} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
