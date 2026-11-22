#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 01 — dựng kho Cloud SQL PostgreSQL 16 + tài khoản + bí mật trên GCP
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell, với quyền admin của project.
#  ⛔ Claude KHÔNG vào GCP (quyết chủ 20/11) — chủ chạy, rồi gửi lại PHẦN "BÁO CÁO" ở cuối.
#  Phần báo cáo ⛔ chứa mật khẩu/khoá: chỉ tên, cấu hình, số đếm.
#
#    bash tools/staging/01_dung_staging_gcp.sh --project <PROJECT_ID> --kiem   # chỉ ĐỌC — xem sẽ làm gì
#    bash tools/staging/01_dung_staging_gcp.sh --project <PROJECT_ID>          # dựng (chạy lại được)
#
#  Tuỳ chọn: --region (mặc định asia-southeast1 · Singapore — gần VN nhất)
#            --instance (mặc định fls-staging) · --tier (mặc định db-custom-1-3840: 1 vCPU · 3,75 GB)
#
#  LÀM GÌ (mỗi việc: có rồi ⇒ bỏ qua, ⛔ phá gì đã có):
#   ① bật API: sqladmin · secretmanager · iam
#   ② Cloud SQL `POSTGRES_16` — ⛔ mạng ủy quyền nào (chỉ vào qua Cloud SQL Auth Proxy / connector
#      có IAM) · SSL bắt buộc (`ENCRYPTED_ONLY`) · sao lưu hằng ngày + PITR · chống xoá
#      (`deletion-protection`) · cờ `cloudsql.iam_authentication=on` để phase SSO sau gắn
#      người dùng IAM vào kho mà ⛔ cần mật khẩu.
#   ③ kho `fls`
#   ④ 3 tài khoản kho (mật khẩu ngẫu nhiên 43 ký tự, cất ở Secret Manager, ⛔ in):
#        `fls_admin` — chủ sở hữu kho, chạy di trú (`python -m fls.db.pg_migrate`)
#        `fls_ghi`   — đường GHI của ứng dụng (`mo_ghi`; công cụ ghi sổ còn đòi `FLS_CHO_GHI_THAT=1`)
#        `fls_doc`   — đường ĐỌC của cửa API: `tools/chay_cua.py` TỪ CHỐI chạy nếu kết nối còn ghi
#                      được ⇒ bước 02 đặt `default_transaction_read_only = on` cho vai này
#      + mật khẩu `postgres` (quản trị Cloud SQL) cũng ngẫu nhiên, cất Secret Manager.
#   ⑤ bí mật `fls-staging-jwt-secret` (cửa API tự từ chối nếu thiếu `FLS_JWT_SECRET`)
#   ⑥ service account `fls-staging-app` — vai `roles/cloudsql.client` + đọc ĐÚNG 5 bí mật trên
#      (dùng cho máy chạy cửa API ở bước sau). Người dùng thật: phase SSO, ⛔ ở đây.
#
#  ⛔ KHÔNG làm ở bước 01: di trú · phân quyền bảng · nạp dữ liệu thật · mở cửa API (bước 02, 03).
#  Chi phí ước tính tier mặc định: ~ 50–60 USD/tháng (instance) + lưu trữ/sao lưu — tự kiểm ở
#  trang Billing; đổi `--tier` nếu cần.
#
#  Luật đo (CLAUDE.md Đ5): phần BÁO CÁO khai `mong` cho từng mục và in ĐẠT/ĐỎ; mục ⛔ đo được ⇒ ĐỎ.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="asia-southeast1" ; INSTANCE="fls-staging" ; TIER="db-custom-1-3840" ; KIEM=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project)  PROJECT="$2"; shift 2 ;;
    --region)   REGION="$2"; shift 2 ;;
    --instance) INSTANCE="$2"; shift 2 ;;
    --tier)     TIER="$2"; shift 2 ;;
    --kiem)     KIEM=1; shift ;;
    -h|--help)  sed -n 2,40p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
command -v gcloud >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }

DB="fls"
USERS=(fls_admin fls_ghi fls_doc)
SA_NAME="fls-staging-app"
SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
SECRETS=(fls-staging-pg-postgres fls-staging-pg-fls_admin fls-staging-pg-fls_ghi fls-staging-pg-fls_doc fls-staging-jwt-secret)
G=(gcloud --project="$PROJECT" --quiet)

buoc() { printf '\n── %s\n' "$*"; }
co_instance() { "${G[@]}" sql instances describe "$INSTANCE" --format='value(name)' >/dev/null 2>&1; }
co_secret()   { "${G[@]}" secrets describe "$1" --format='value(name)' >/dev/null 2>&1; }
mat_khau()    { python3 -c 'import secrets; print(secrets.token_urlsafe(32))'; }

# Lấy mật khẩu từ Secret Manager nếu đã có, nếu chưa thì sinh + cất. ⛔ in giá trị.
bi_mat() {
  local ten="$1" gt
  if co_secret "$ten"; then
    gt="$("${G[@]}" secrets versions access latest --secret="$ten")"
  else
    gt="$(mat_khau)"
    printf '%s' "$gt" | "${G[@]}" secrets create "$ten" --replication-policy=automatic \
        --labels=app=fls,moi-truong=staging --data-file=- >/dev/null
    echo "   tạo bí mật $ten" >&2
  fi
  printf '%s' "$gt"
}

if [ "$KIEM" -eq 0 ]; then
  buoc "① bật API"
  "${G[@]}" services enable sqladmin.googleapis.com secretmanager.googleapis.com iam.googleapis.com

  buoc "② Cloud SQL $INSTANCE ($REGION · $TIER · POSTGRES_16)"
  if co_instance; then
    echo "   có rồi ⇒ bỏ qua tạo (⛔ đổi cấu hình máy đang chạy)"
  else
    echo "   tạo — thường mất 5–15 phút…"
    "${G[@]}" sql instances create "$INSTANCE" \
      --database-version=POSTGRES_16 --edition=ENTERPRISE --tier="$TIER" --region="$REGION" \
      --storage-type=SSD --storage-size=20GB --storage-auto-increase \
      --availability-type=ZONAL \
      --backup-start-time=19:00 --enable-point-in-time-recovery --retained-backups-count=14 \
      --ssl-mode=ENCRYPTED_ONLY --deletion-protection \
      --database-flags=cloudsql.iam_authentication=on
  fi

  buoc "③ kho $DB"
  if "${G[@]}" sql databases describe "$DB" --instance="$INSTANCE" >/dev/null 2>&1; then
    echo "   có rồi ⇒ bỏ qua"
  else
    "${G[@]}" sql databases create "$DB" --instance="$INSTANCE"
  fi

  buoc "④ tài khoản kho (mật khẩu ở Secret Manager — ⛔ in)"
  PW="$(bi_mat fls-staging-pg-postgres)"
  "${G[@]}" sql users set-password postgres --instance="$INSTANCE" --password="$PW" >/dev/null
  echo "   postgres: đặt mật khẩu từ bí mật"
  for u in "${USERS[@]}"; do
    PW="$(bi_mat "fls-staging-pg-$u")"
    if "${G[@]}" sql users list --instance="$INSTANCE" --format='value(name)' | grep -qx "$u"; then
      "${G[@]}" sql users set-password "$u" --instance="$INSTANCE" --password="$PW" >/dev/null
      echo "   $u: có rồi ⇒ đồng bộ mật khẩu với bí mật"
    else
      "${G[@]}" sql users create "$u" --instance="$INSTANCE" --password="$PW" >/dev/null
      echo "   $u: tạo"
    fi
  done
  unset PW

  buoc "⑤ bí mật JWT của cửa API"
  bi_mat fls-staging-jwt-secret >/dev/null
  echo "   fls-staging-jwt-secret: sẵn"

  buoc "⑥ service account $SA_NAME"
  if "${G[@]}" iam service-accounts describe "$SA_EMAIL" >/dev/null 2>&1; then
    echo "   có rồi ⇒ bỏ qua tạo"
  else
    "${G[@]}" iam service-accounts create "$SA_NAME" --display-name="FLS staging — máy chạy cửa API"
  fi
  "${G[@]}" projects add-iam-policy-binding "$PROJECT" \
      --member="serviceAccount:$SA_EMAIL" --role=roles/cloudsql.client --condition=None >/dev/null
  for s in "${SECRETS[@]}"; do
    "${G[@]}" secrets add-iam-policy-binding "$s" \
        --member="serviceAccount:$SA_EMAIL" --role=roles/secretmanager.secretAccessor >/dev/null
  done
  echo "   cloudsql.client + secretAccessor trên ${#SECRETS[@]} bí mật"
fi

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa mật khẩu/khoá) — chép từ dòng này tới hết, gửi lại"
export PROJECT REGION INSTANCE DB SA_EMAIL
export USERS_S="${USERS[*]}" SECRETS_S="${SECRETS[*]}"
export INST_JSON="$("${G[@]}" sql instances describe "$INSTANCE" --format=json 2>/dev/null || echo '{}')"
export USERS_JSON="$("${G[@]}" sql users list --instance="$INSTANCE" --format=json 2>/dev/null || echo '[]')"
export DBS_JSON="$("${G[@]}" sql databases list --instance="$INSTANCE" --format=json 2>/dev/null || echo '[]')"
SEC_DONG=""
for s in "${SECRETS[@]}"; do
  n="$("${G[@]}" secrets versions list "$s" --filter='state=ENABLED' --format='value(name)' 2>/dev/null | wc -l | tr -d ' ')" || n=0
  SEC_DONG+="$s=$n "
done
export SEC_DONG
export SA_CO="$("${G[@]}" iam service-accounts describe "$SA_EMAIL" --format='value(email)' 2>/dev/null || true)"
export SA_VAI="$("${G[@]}" projects get-iam-policy "$PROJECT" --flatten='bindings[].members' \
   --filter="bindings.members:serviceAccount:$SA_EMAIL" --format='value(bindings.role)' 2>/dev/null | tr '\n' ' ' || true)"
export KIEM

python3 - <<'PY'
import json, os
e = os.environ
i = json.loads(e["INST_JSON"] or "{}")
s = i.get("settings", {})
ip = s.get("ipConfiguration", {})
bk = s.get("backupConfiguration", {})
co = {f.get("name"): f.get("value") for f in s.get("databaseFlags", [])}
users = sorted(u.get("name") for u in json.loads(e["USERS_JSON"] or "[]"))
dbs = sorted(d.get("name") for d in json.loads(e["DBS_JSON"] or "[]"))
sec = dict(x.split("=") for x in e["SEC_DONG"].split())
mong_users = sorted(["postgres"] + e["USERS_S"].split())
hang = [
  ("project · region · instance", f'{e["PROJECT"]} · {e["REGION"]} · {e["INSTANCE"]}', None),
  ("connectionName", i.get("connectionName", "—"), None),
  ("trạng thái máy",      i.get("state"),                         "RUNNABLE"),
  ("phiên bản",           i.get("databaseVersion"),               "POSTGRES_16"),
  ("tier",                s.get("tier"),                          None),
  ("SSL",                 ip.get("sslMode"),                      "ENCRYPTED_ONLY"),
  ("mạng ủy quyền (đếm)", len(ip.get("authorizedNetworks", [])) if i else None, 0),
  ("sao lưu",             bk.get("enabled"),                      True),
  ("PITR",                bk.get("pointInTimeRecoveryEnabled"),   True),
  ("chống xoá",           s.get("deletionProtectionEnabled"),     True),
  ("cờ IAM auth",         co.get("cloudsql.iam_authentication"),  "on"),
  ("kho",                 ",".join(dbs),                          None),
  ("có kho fls",          "fls" in dbs,                           True),
  ("tài khoản kho",       ",".join(users),                        None),
  ("đủ 4 tài khoản",      all(u in users for u in mong_users),   True),
  ("bí mật (số bản bật)", " ".join(f"{k}:{v}" for k, v in sec.items()), None),
  ("đủ 5 bí mật ≥ 1 bản", len(sec) == 5 and all(int(v) >= 1 for v in sec.values()), True),
  ("service account",     e["SA_CO"] or "—",                      None),
  ("SA có cloudsql.client", "roles/cloudsql.client" in e["SA_VAI"], True),
]
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:24} {gt}")
    else:
        ok = gt == mong
        do += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:22} {gt!r}  (mong {mong!r})")
che_do = "--kiem (chỉ đọc)" if e["KIEM"] == "1" else "dựng"
print(f"\n══ chế độ: {che_do} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
