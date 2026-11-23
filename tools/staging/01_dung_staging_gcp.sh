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
#   ⑥ service account `fls-staging-app` — vai `roles/cloudsql.client` + `secretAccessor` trên ĐÚNG 3 bí mật
#      app dùng: `fls-staging-jwt-secret` · `fls-staging-pg-fls_ghi` · `fls-staging-pg-fls_doc`
#      (dùng cho máy chạy cửa API ở bước sau). ⛔⛔ KHÔNG đọc được `fls-staging-pg-postgres` · `fls-staging-pg-fls_admin`:
#      hai bí mật quản trị chỉ danh tính CHỦ (bước 02/04 chạy trong Cloud Shell) — người có shell trên VM gọi được
#      máy chủ metadata lấy token của SA, nên SA đọc được `fls_admin` ⇒ vòng quanh cả hai tường quyền của bước 02
#      (`STG-R1-01`). Chạy lại script ⇒ GỠ `secretAccessor` thừa nếu bản chạy cũ đã gán (idempotent).
#      Người dùng thật: phase SSO, ⛔ ở đây.
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
# ⭐ `STG-R1-01`: tách hai nhóm. `BI_MAT_APP` = ĐÚNG những gì app đọc (đo bằng grep chỗ dùng: `vao.sh` đọc
#   `fls-staging-jwt-secret` + `fls-staging-pg-$VAI` với VAI ∈ {fls_ghi, fls_doc}; `chay_chuoi.sh` đọc `fls-staging-pg-fls_doc`).
#   `BI_MAT_QUAN_TRI` = ⛔ gán cho SA, và còn bị GỠ nếu đã lỡ gán.
BI_MAT_APP=(fls-staging-pg-fls_ghi fls-staging-pg-fls_doc fls-staging-jwt-secret)
BI_MAT_QUAN_TRI=(fls-staging-pg-postgres fls-staging-pg-fls_admin)
SECRETS=("${BI_MAT_QUAN_TRI[@]}" "${BI_MAT_APP[@]}")   # 5 bí mật phải TỒN TẠI; ⛔ nghĩa là SA đọc cả 5
G=(gcloud --project="$PROJECT" --quiet)

buoc() { printf '\n── %s\n' "$*"; }
co_instance() { "${G[@]}" sql instances describe "$INSTANCE" --format='value(name)' >/dev/null 2>&1; }
co_secret()   { "${G[@]}" secrets describe "$1" --format='value(name)' >/dev/null 2>&1; }
# SA đang đọc được bí mật $1? In `co`/`khong`; ⛔ đo được ⇒ `khong_do` (Đ5: phép ⛔ đo được là ĐỎ, ⛔ là "không thấy lệch").
sa_doc_duoc() {
  local out
  out="$("${G[@]}" secrets get-iam-policy "$1" --flatten='bindings[].members' \
      --filter="bindings.role=roles/secretmanager.secretAccessor AND bindings.members=serviceAccount:$SA_EMAIL" \
      --format='value(bindings.members)' 2>/dev/null)" || { echo khong_do; return 0; }
  [ -n "$out" ] && echo co || echo khong
}
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
  # ⭐ Lần chạy THẬT 23/11: `iam service-accounts create` xong ngay, nhưng `add-iam-policy-binding` ngay sau đó báo
  #   `INVALID_ARGUMENT: Service account … does not exist` (IAM lan truyền trễ) ⇒ `set -e` chết im, ⛔ in BÁO CÁO.
  #   ⇒ thử lại CÓ HẠN (≤ 12 lần × 5 giây, chỉnh bằng FLS_STG_THU_LAI / FLS_STG_CHO_GIAY); hết hạn ⇒ lỗi CÓ TÊN, ⛔ dừng:
  #   vẫn đi tiếp tới BÁO CÁO để phép ⛔ đo được hiện ĐỎ (Đ5).
  THU_LAI="${FLS_STG_THU_LAI:-12}"; CHO_GIAY="${FLS_STG_CHO_GIAY:-5}"
  LOI_CUOI=""
  thu_lai() {   # chạy "$@" tới khi được hoặc hết lượt; giữ DÒNG LỖI CUỐI của gcloud trong LOI_CUOI (`STG-R1-04b`:
                # trước đây `>/dev/null 2>&1` nuốt chữ thật ⇒ PERMISSION_DENIED bị dán nhãn "IAM lan truyền")
    local i out
    for i in $(seq 1 "$THU_LAI"); do
      if out="$("$@" 2>&1 >/dev/null)"; then return 0; fi
      LOI_CUOI="$(printf '%s\n' "$out" | grep -v '^[[:space:]]*$' | tail -1)"
      [ "$i" -lt "$THU_LAI" ] && { echo "   (lần $i/$THU_LAI chưa được — chờ ${CHO_GIAY}s cho IAM lan truyền)"; sleep "$CHO_GIAY"; }
    done
    return 1
  }
  IAM_LOI=0
  thu_lai "${G[@]}" projects add-iam-policy-binding "$PROJECT" \
      --member="serviceAccount:$SA_EMAIL" --role=roles/cloudsql.client --condition=None \
    || { echo "⛔ IAM_KHONG_LAN_TRUYEN: không gán được roles/cloudsql.client cho $SA_EMAIL sau $THU_LAI lần — gcloud nói: $LOI_CUOI" >&2; IAM_LOI=1; }
  for s in "${BI_MAT_APP[@]}"; do
    thu_lai "${G[@]}" secrets add-iam-policy-binding "$s" \
        --member="serviceAccount:$SA_EMAIL" --role=roles/secretmanager.secretAccessor \
      || { echo "⛔ IAM_KHONG_LAN_TRUYEN: không gán được secretAccessor trên $s sau $THU_LAI lần — gcloud nói: $LOI_CUOI" >&2; IAM_LOI=1; }
  done
  # ⭐ `STG-R1-01`: GỠ secretAccessor của SA trên hai bí mật quản trị nếu bản chạy cũ (23/11) đã lỡ gán. Có ⇒ gỡ; ⛔ có ⇒ bỏ qua.
  #   `khong_do` ⇒ KHÔNG đoán là sạch: báo lỗi có tên, BÁO CÁO sẽ ĐỎ.
  for s in "${BI_MAT_QUAN_TRI[@]}"; do
    case "$(sa_doc_duoc "$s")" in
      co)  thu_lai "${G[@]}" secrets remove-iam-policy-binding "$s" \
               --member="serviceAccount:$SA_EMAIL" --role=roles/secretmanager.secretAccessor \
             && echo "   gỡ secretAccessor thừa của SA trên $s" \
             || { echo "⛔ GO_QUYEN_THUA_LOI: không gỡ được secretAccessor của SA trên $s — gcloud nói: $LOI_CUOI" >&2; IAM_LOI=1; } ;;
      khong_do) echo "⛔ GO_QUYEN_THUA_LOI: ⛔ đo được chính sách IAM của $s" >&2; IAM_LOI=1 ;;
      *)   echo "   SA ⛔ đọc được $s ✔" ;;
    esac
  done
  [ "$IAM_LOI" -eq 0 ] && echo "   cloudsql.client + secretAccessor trên ${#BI_MAT_APP[@]} bí mật app (0 bí mật quản trị)" \
    || echo "   ⛔ gán/gỡ vai chưa đủ — sang BÁO CÁO (mục \"gán vai đủ\" ĐỎ); chạy lại script khi IAM ổn"
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
export SA_DOC_APP="" SA_DOC_QT=""
for s in "${BI_MAT_APP[@]}";      do SA_DOC_APP+="$s=$(sa_doc_duoc "$s") "; done
for s in "${BI_MAT_QUAN_TRI[@]}"; do SA_DOC_QT+="$s=$(sa_doc_duoc "$s") ";  done
export BI_MAT_APP_S="${BI_MAT_APP[*]}" IAM_LOI="${IAM_LOI:-0}"
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
app = dict(x.split("=") for x in e["SA_DOC_APP"].split())
qt = dict(x.split("=") for x in e["SA_DOC_QT"].split())
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
  # ⭐ `STG-R1-01` — quyền THỪA (trước đây chỉ canh quyền THIẾU). Hai chiều: thiếu bí mật app ⇒ ĐỎ · còn đọc bí mật quản trị ⇒ ĐỎ ·
  #   ⛔ đo được (`khong_do`) ⇒ ĐỎ. Mẫu số in ra cạnh: số bí mật app mong = len(APP) ≠ 0 (Đ3).
  # `mong` GHIM CỨNG "3/3" · "0/2" (khai trước kết quả): thêm/bớt một bí mật ở mảng ⇒ cổng ĐỎ ⇒ buộc ghi lại bản khai.
  ("SA đọc đúng bí mật app (đếm/mẫu số)", f'{sum(v == "co" for v in app.values())}/{len(app)}', "3/3"),
  ("SA đọc 0 bí mật quản trị (đếm/mẫu số)", f'{sum(v != "khong" for v in qt.values())}/{len(qt)}', "0/2"),
  ("gán/gỡ vai đủ (không lỗi IAM)", e["IAM_LOI"] == "0", True),
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
