#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 02 — di trú schema + phân quyền ba vai kho (qua Cloud SQL Auth Proxy)
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell, SAU khi bước 01 báo `KẾT: ĐẠT`.
#  ⛔ Claude KHÔNG vào GCP (quyết chủ 20/11) — chủ chạy, rồi gửi lại PHẦN "BÁO CÁO" ở cuối.
#  Phần báo cáo ⛔ chứa mật khẩu/khoá: chỉ tên, cấu hình, số đếm.
#
#    cd <repo FLS đã git clone trong Cloud Shell>
#    bash tools/staging/02_di_tru_phan_quyen.sh --project <PROJECT_ID> --kiem   # chỉ ĐỌC — đo trạng thái
#    bash tools/staging/02_di_tru_phan_quyen.sh --project <PROJECT_ID>          # làm (chạy lại được)
#
#  Tuỳ chọn: --region (asia-southeast1) · --instance (fls-staging) · --kho (fls)
#            --cong-proxy (5432 — cổng cục bộ của Auth Proxy)
#            --proxy <đường dẫn cloud-sql-proxy v2>   (mặc định tìm `cloud-sql-proxy` trong PATH)
#  Biến: FLS_STG_PYTHON = python có sẵn `psycopg` (mặc định: tự dựng venv ở ~/.fls-staging-venv)
#        FLS_STG_QT_USER = vai quản trị Cloud SQL (mặc định `postgres`)
#
#  LÀM GÌ (mỗi việc chạy lại được, ⛔ phá gì đã có):
#   ① đọc `connectionName` của máy Cloud SQL → bật Cloud SQL Auth Proxy (127.0.0.1, ⛔ mở ra ngoài;
#      xác thực = danh tính gcloud của chủ; SSL do proxy lo)
#   ①b (vai `postgres`) VAI ỨNG DỤNG `fls_ghi`/`fls_doc` TẠO BẰNG SQL (`STG-R2b-02`, lỗi THẬT GCP 23/11):
#      chưa có ⇒ `CREATE ROLE … LOGIN NOCREATEDB NOCREATEROLE` · có mà SẠCH ⇒ đồng bộ mật khẩu ·
#      có mà còn CREATEROLE/CREATEDB/siêu quyền (= do `gcloud sql users create` tạo — bản cũ của bước 01)
#      ⇒ ĐƯỜNG CHUYỂN: thu mọi quyền (`sql/02c_thu_quyen_vai.sql`, vai `fls_admin`) → `DROP ROLE` bằng SQL
#      (⛔ được ⇒ `gcloud sql users delete`) → tạo lại bằng SQL → ②–④ cấp lại như thường.
#   ② (vai `postgres`) `sql/02a_quan_tri.sql`: đổi chủ kho sang `fls_admin` · đóng cửa PUBLIC ·
#      `ALTER ROLE fls_doc SET default_transaction_read_only = on`
#   ③ (vai `fls_admin`) `python -m fls.db.pg_migrate` ⇒ phải in `pg_verify: khop`
#   ④ (vai `fls_admin`) `sql/02b_phan_quyen.sql`: `fls_ghi` DML — **riêng `fls_itl` chỉ-THÊM**
#      (`INV-I08`: ⛔ UPDATE/DELETE) · `fls_doc` chỉ SELECT
#   ⑤ BÁO CÁO: mỗi mục khai `mong`; ĐẠT/ĐỎ; exit 1 khi có mục ĐỎ.
#
#  ⛔ Mật khẩu: đọc từ Secret Manager vào BIẾN SHELL, đưa cho đúng MỘT tiến trình con qua `PGPASSWORD`
#     (⛔ `PG_DSN` mang mật khẩu, ⛔ `echo`, ⛔ `set -x`, ⛔ ghi tệp). Báo cáo ⛔ in giá trị.
#  ⛔ KHÔNG làm ở bước 02: nạp dữ liệu (bước 04) · dựng app (bước 03).
#  ⭐ Chạy lại SAU MỖI di trú mới: bảng mới ⛔ tự có quyền (cố ý — xem `02b_phan_quyen.sql`).
#
#  Luật đo (CLAUDE.md Đ3·Đ5): mỗi mục có `mong`; mục ⛔ ĐO ĐƯỢC ⇒ ĐỎ (không phải "không thấy lệch");
#  mục đếm "= 0" in kèm MẪU SỐ và ĐỎ khi mẫu số = 0.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="asia-southeast1" ; INSTANCE="fls-staging" ; KHO="fls" ; KIEM=0
CONG_PROXY=5432 ; PROXY_BIN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --project)    PROJECT="$2"; shift 2 ;;
    --region)     REGION="$2"; shift 2 ;;
    --instance)   INSTANCE="$2"; shift 2 ;;
    --kho)        KHO="$2"; shift 2 ;;
    --cong-proxy) CONG_PROXY="$2"; shift 2 ;;
    --proxy)      PROXY_BIN="$2"; shift 2 ;;
    --kiem)       KIEM=1; shift ;;
    -h|--help)    sed -n 2,40p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
case "$CONG_PROXY" in ''|*[!0-9]*) echo "⛔ --cong-proxy phải là số" >&2; exit 2 ;; esac
case "$KHO" in ''|*[!a-z0-9_]*) echo "⛔ --kho chỉ gồm [a-z0-9_]" >&2; exit 2 ;; esac
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v psql    >/dev/null || { echo "⛔ không có psql (Cloud Shell có sẵn)" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }
[ -n "$PROXY_BIN" ] || PROXY_BIN="$(command -v cloud-sql-proxy || true)"
[ -n "$PROXY_BIN" ] && [ -x "$PROXY_BIN" ] || {
  echo "⛔ không thấy cloud-sql-proxy (bản v2). Tải một lần rồi chạy lại với --proxy <đường dẫn>:" >&2
  echo "   https://cloud.google.com/sql/docs/postgres/sql-proxy#install  (tệp linux.amd64, chmod +x)" >&2
  exit 2; }

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"      # gốc repo
SQL_DIR="$GOC/tools/staging/sql"
for f in 02a_quan_tri.sql 02b_phan_quyen.sql; do
  [ -f "$SQL_DIR/$f" ] || { echo "⛔ thiếu $SQL_DIR/$f" >&2; exit 2; }
done

ADMIN="fls_admin" ; GHI="fls_ghi" ; DOC="fls_doc" ; QT_USER="${FLS_STG_QT_USER:-postgres}"
SO="fls_itl" ; SO_DI_TRU="fls_migration"      # `fls.db.migration_runner.LEDGER`
G=(gcloud --project="$PROJECT" --quiet)
HOST=127.0.0.1

buoc() { printf '\n── %s\n' "$*"; }

# Mật khẩu từ Secret Manager vào biến — ⛔ in. Thiếu bí mật ⇒ dừng (bước 01 chưa chạy xong).
lay_mk() {
  "${G[@]}" secrets versions access latest --secret="$1" 2>/dev/null \
    || { echo "⛔ không đọc được bí mật $1 — bước 01 đã ĐẠT chưa? Tài khoản gcloud có quyền secretAccessor chưa?" >&2; return 1; }
}
MK_QT="$(lay_mk fls-staging-pg-postgres)"
MK_ADMIN="$(lay_mk fls-staging-pg-fls_admin)"
MK_GHI="$(lay_mk fls-staging-pg-fls_ghi)"
MK_DOC="$(lay_mk fls-staging-pg-fls_doc)"

# psql với vai + mật khẩu CHỈ cho tiến trình con này. $1=vai $2=mật khẩu, còn lại = đối số psql.
psql_vai() {
  local vai="$1" mk="$2"; shift 2
  PGPASSWORD="$mk" PGCONNECT_TIMEOUT=20 psql -X -h "$HOST" -p "$CONG_PROXY" -U "$vai" -d "$KHO" "$@"
}

# ① ──────────────────────────────── Cloud SQL Auth Proxy
buoc "① Cloud SQL Auth Proxy → $INSTANCE ($REGION)"
CONN="$("${G[@]}" sql instances describe "$INSTANCE" --format='value(connectionName)')"
[ -n "$CONN" ] || { echo "⛔ không đọc được connectionName của $INSTANCE — bước 01 chưa chạy?" >&2; exit 2; }
PROXY_LOG="$(mktemp)"
"$PROXY_BIN" --address "$HOST" --port "$CONG_PROXY" "$CONN" >"$PROXY_LOG" 2>&1 &
PROXY_PID=$!
tat_proxy() { kill "$PROXY_PID" 2>/dev/null || true; wait "$PROXY_PID" 2>/dev/null || true; rm -f "$PROXY_LOG"; }
trap tat_proxy EXIT
sang=0
for _ in $(seq 1 40); do
  if (exec 3<>"/dev/tcp/$HOST/$CONG_PROXY") 2>/dev/null; then sang=1; break; fi
  kill -0 "$PROXY_PID" 2>/dev/null || break
  sleep 0.5
done
[ "$sang" -eq 1 ] || { echo "⛔ proxy ⛔ lên cổng $CONG_PROXY (log proxy bên dưới)" >&2; sed -n 1,20p "$PROXY_LOG" >&2; exit 2; }
echo "   proxy lên ở $HOST:$CONG_PROXY (cục bộ — ⛔ mở ra ngoài)"

# psql bằng vai quản trị vào kho HỆ THỐNG `postgres` (vai là đối tượng của CỤM, ⛔ của kho `$KHO`; nối
# `postgres` ⇒ đường chuyển vai chạy được cả khi kho `$KHO` đã đóng PUBLIC). VERBOSITY=terse ⇒ psql ⛔ in
# lại dòng lệnh lỗi (`LINE 1: CREATE ROLE … PASSWORD '…'`) — nơi duy nhất mật khẩu có thể lọt ra màn.
psql_qt_he() {
  PGPASSWORD="$MK_QT" PGCONNECT_TIMEOUT=20 psql -X -q -h "$HOST" -p "$CONG_PROXY" -U "$QT_USER" -d postgres \
    -v ON_ERROR_STOP=1 -v VERBOSITY=terse "$@"
}

# ⭐ `STG-R2b-02` (lỗi THẬT GCP, bước 02 chủ chạy 23/11 trên `c4a0f39`): 23/24 ĐẠT, ĐỎ đúng mục
#   "siêu quyền hay CREATEROLE/CREATEDB (đếm vai) = 2"; bản cũ chạy `ALTER ROLE … NOSUPERUSER NOCREATEROLE
#   NOCREATEDB NOREPLICATION NOBYPASSRLS` và NUỐT lỗi (`>/dev/null 2>&1` ⇒ chỉ `⚠`).
#   Hai giả thuyết — CẢ HAI ⛔ đo ở GCP (lỗi gốc bị nuốt):
#     H-A  `postgres` ⛔ có ADMIN OPTION trên vai gcloud tạo ⇒ mọi ALTER/DROP bị từ chối.
#          ⚠ MÂU THUẪN với hai sự thật đã đo cùng lần chạy: `ALTER ROLE fls_doc SET …` (02a) ĐẠT và
#          `GRANT fls_admin TO CURRENT_USER` ĐẠT — PG16 đòi ADMIN OPTION cho cả hai.
#     H-B  `postgres` CÓ ADMIN OPTION nhưng ⛔ phải siêu người dùng ⇒ PG16 từ chối CẢ CÂU vì mệnh đề
#          `NOSUPERUSER` ("Only roles with the SUPERUSER attribute may change the SUPERUSER attribute")
#          — đo được trên PG 16 cục bộ 23/11; khớp mọi sự thật GCP đã đo.
#   ⇒ Đường dưới đây ĐÚNG với CẢ HAI: tạo lại bằng SQL (người tạo có ADMIN OPTION — PG16 tự cấp), và
#   `DROP ROLE` ⛔ được (H-A) thì rơi sang `gcloud sql users delete`. Lỗi THẬT của PG được IN (⛔ nuốt)
#   kèm phép đo ADMIN OPTION ⇒ lần chạy của chủ phân xử H-A/H-B.
VAI_APP=("$GHI" "$DOC")
mk_cua() { case "$1" in "$GHI") printf '%s' "$MK_GHI" ;; "$DOC") printf '%s' "$MK_DOC" ;; esac; }
# Mật khẩu nằm trong câu SQL (đi qua ỐNG từ `printf` — lệnh dựng sẵn của bash ⇒ ⛔ hiện ở `ps`, ⛔ tệp tạm).
# Bí mật do bước 01 sinh bằng `secrets.token_urlsafe(32)` ⇒ chỉ [A-Za-z0-9_-]; ký tự khác ⇒ DỪNG (⛔ tự trích dẫn).
mk_hop_le() { [[ "$1" =~ ^[A-Za-z0-9_-]{16,}$ ]]; }
che_mk() { local o="$1" m; for m in "$MK_QT" "$MK_ADMIN" "$MK_GHI" "$MK_DOC"; do [ -n "$m" ] && o="${o//"$m"/***}"; done; printf '%s' "$o"; }
# `ban` = còn thuộc tính thừa HOẶC là thành viên `cloudsqlsuperuser` (PG16: `REVOKE` chỉ thu grant do CHÍNH người
# thu cấp ⇒ `postgres` ⛔ gỡ được grant Cloud SQL đã cấp — đo trên PG 16 cục bộ; bản cũ gỡ trong khối nuốt lỗi).
trang_thai_vai() {   # $1=vai → khong | sach | ban | (rỗng = ⛔ đo được)
  psql_qt_he -tA -c "SELECT CASE WHEN count(*) = 0 THEN 'khong'
      WHEN bool_or(r.rolsuper OR r.rolcreaterole OR r.rolcreatedb OR r.rolreplication OR r.rolbypassrls
                   OR EXISTS (SELECT 1 FROM pg_auth_members m JOIN pg_roles g ON g.oid = m.roleid
                              WHERE m.member = r.oid AND g.rolname = 'cloudsqlsuperuser')) THEN 'ban'
      ELSE 'sach' END FROM pg_roles r WHERE r.rolname = '$1'" 2>/dev/null | head -1 | tr -d '\r' || true
}
tao_vai_sql() {   # $1=vai $2=CREATE|ALTER → 0/1; in lỗi PG đã che mật khẩu
  local vai="$1" lenh="$2" mk out rc=0 cau
  mk="$(mk_cua "$vai")"
  mk_hop_le "$mk" || { echo "⛔ bí mật fls-staging-pg-$vai có ký tự ngoài [A-Za-z0-9_-] (hoặc < 16) — DỪNG" >&2; return 1; }
  if [ "$lenh" = CREATE ]; then cau="CREATE ROLE %s LOGIN NOCREATEDB NOCREATEROLE PASSWORD '%s';\n"
  else cau="ALTER ROLE %s PASSWORD '%s';\n"; fi
  # shellcheck disable=SC2059   # khuôn là hằng của script, ⛔ dữ liệu ngoài
  out="$(printf "$cau" "$vai" "$mk" | psql_qt_he 2>&1)" || rc=$?
  [ -z "$out" ] || printf '      PG nói: %s\n' "$(che_mk "$out" | tr '\n' ' ')"
  return "$rc"
}
chuyen_vai() {    # đường chuyển cho vai gcloud tạo: thu quyền → DROP (SQL, rồi gcloud) → CREATE bằng SQL
  local vai="$1" out
  echo "   $vai: còn CREATEROLE/CREATEDB/siêu quyền/cloudsqlsuperuser ⇒ ĐƯỜNG CHUYỂN (thu quyền → xoá → tạo lại bằng SQL)"
  echo "      đo trước: $(psql_qt_he -tA -c "SELECT 'rolcreaterole=' || rolcreaterole || ' rolcreatedb=' || rolcreatedb
      || ' rolsuper=' || rolsuper || ' · $QT_USER có ADMIN OPTION=' || coalesce((SELECT bool_or(m.admin_option)
      FROM pg_auth_members m WHERE m.roleid = r.oid AND m.member = (SELECT oid FROM pg_roles WHERE rolname = current_user)), false)
      FROM pg_roles r WHERE rolname = '$vai'" 2>&1 | head -1)"
  out="$(PGOPTIONS='--client-min-messages=error' psql_vai "$ADMIN" "$MK_ADMIN" -q -v ON_ERROR_STOP=1 -v VERBOSITY=terse \
          -v "kho=$KHO" -v "vai=$vai" -f "$SQL_DIR/02c_thu_quyen_vai.sql" 2>&1)" \
    || { echo "⛔ VAI_THU_QUYEN_LOI: $ADMIN ⛔ thu được quyền của $vai — PG nói: $(che_mk "$out" | tr '\n' ' ')" >&2; return 1; }
  echo "      ⓐ thu mọi quyền của $vai trong kho $KHO ($ADMIN): xong"
  # VERBOSITY=default (⛔ terse): câu ⛔ mang mật khẩu, và dòng DETAIL của PG là thứ PHÂN XỬ H-A/H-B ở GCP.
  if out="$(printf 'DROP ROLE %s;\n' "$vai" | psql_qt_he -v VERBOSITY=default 2>&1)"; then
    echo "      ⓑ DROP ROLE $vai bằng SQL ($QT_USER): xong"
  else
    echo "      ⓑ DROP ROLE $vai bằng SQL bị từ chối — PG nói: $(che_mk "$out" | tr '\n' ' ')"
    echo "         ⇒ xoá qua Cloud SQL Admin API: gcloud sql users delete $vai"
    out="$("${G[@]}" sql users delete "$vai" --instance="$INSTANCE" 2>&1)" \
      || { echo "⛔ VAI_KHONG_XOA_DUOC: $vai — gcloud nói: $(printf '%s' "$out" | grep -v '^[[:space:]]*$' | tail -1)" >&2; return 1; }
    [ "$(trang_thai_vai "$vai")" = khong ] \
      || { echo "⛔ VAI_KHONG_XOA_DUOC: gcloud báo xong nhưng $vai VẪN còn trong pg_roles" >&2; return 1; }
    echo "         gcloud sql users delete $vai: xong"
  fi
  tao_vai_sql "$vai" CREATE || { echo "⛔ VAI_KHONG_TAO_DUOC: $vai (đã xoá!) — sửa rồi chạy lại 02 ngay; app ⛔ nối được tới khi xong" >&2; return 1; }
  echo "      ⓒ CREATE ROLE $vai LOGIN NOCREATEDB NOCREATEROLE (mật khẩu từ bí mật): xong"
}

# ── python có `psycopg` cho pg_migrate/pg_verify
tim_python() {
  if [ -n "${FLS_STG_PYTHON:-}" ]; then printf '%s' "$FLS_STG_PYTHON"; return; fi
  local venv="$HOME/.fls-staging-venv"
  if [ ! -x "$venv/bin/python" ]; then
    python3 -m venv "$venv" >&2
    "$venv/bin/pip" install --quiet "$(grep -i '^psycopg' "$GOC/requirements.txt" | head -1)" >&2
  fi
  printf '%s' "$venv/bin/python"
}

if [ "$KIEM" -eq 0 ]; then
  # ①b ─────────────────────────────── vai ứng dụng — TẠO BẰNG SQL (`STG-R2b-02`)
  buoc "①b vai ứng dụng ${VAI_APP[*]}: tạo/tái tạo bằng SQL ($QT_USER) — ⛔ gcloud sql users create"
  for vai in "${VAI_APP[@]}"; do
    case "$(trang_thai_vai "$vai")" in
      khong) tao_vai_sql "$vai" CREATE || { echo "⛔ VAI_KHONG_TAO_DUOC: $vai" >&2; exit 1; }
             echo "   $vai: tạo bằng SQL (LOGIN NOCREATEDB NOCREATEROLE)" ;;
      sach)  tao_vai_sql "$vai" ALTER || { echo "⛔ VAI_KHONG_DONG_BO_MK: $vai — $QT_USER ⛔ đổi được mật khẩu" >&2; exit 1; }
             echo "   $vai: có rồi, SẠCH ⇒ đồng bộ mật khẩu với bí mật" ;;
      ban)   chuyen_vai "$vai" || exit 1 ;;
      *)     echo "⛔ ⛔ đo được trạng thái vai $vai ($QT_USER nối kho postgres?) — DỪNG" >&2; exit 1 ;;
    esac
  done

  # ② ──────────────────────────────── quản trị (postgres)
  buoc "② quản trị: đổi chủ kho · đóng PUBLIC · fls_doc mặc định chỉ-đọc"
  PGOPTIONS='--client-min-messages=warning' psql_vai "$QT_USER" "$MK_QT" -v ON_ERROR_STOP=1 \
      -v "kho=$KHO" -v "admin=$ADMIN" -v "ghi=$GHI" -v "doc=$DOC" -f "$SQL_DIR/02a_quan_tri.sql" >/dev/null
  echo "   02a_quan_tri.sql: xong"
  # ⭐ `STG-R2b-02`: bản cũ ở đây `ALTER ROLE … NOSUPERUSER NOCREATEROLE …` + `REVOKE cloudsqlsuperuser …` rồi NUỐT lỗi
  #   (`>/dev/null 2>&1` ⇒ chỉ `⚠`). Đã thay bằng ①b: vai app tạo bằng SQL ⇒ ⛔ còn thuộc tính/nhóm nào để gỡ;
  #   vai lạc vào lại ⇒ lần chạy kế đi đường chuyển. Kết quả THẬT vẫn ở hai mục BÁO CÁO cuối (ĐỎ hai chiều).

  # ③ ──────────────────────────────── di trú
  buoc "③ di trú — python -m fls.db.pg_migrate (vai $ADMIN)"
  PY="$(tim_python)"
  ( cd "$GOC" && PGPASSWORD="$MK_ADMIN" PYTHONUTF8=1 \
      PG_DSN="postgresql://$ADMIN@$HOST:$CONG_PROXY/$KHO" "$PY" -m fls.db.pg_migrate ) \
    || { echo "⛔ pg_migrate đỏ — DỪNG (⛔ phân quyền trên schema lệch)" >&2; exit 1; }

  # ④ ──────────────────────────────── phân quyền
  buoc "④ phân quyền — $GHI DML (fls_itl chỉ-THÊM) · $DOC SELECT"
  PGOPTIONS='--client-min-messages=warning' psql_vai "$ADMIN" "$MK_ADMIN" -v ON_ERROR_STOP=1 \
      -v "ghi=$GHI" -v "doc=$DOC" -v "so=$SO" -v "so_di_tru=$SO_DI_TRU" \
      -f "$SQL_DIR/02b_phan_quyen.sql" >/dev/null
  echo "   02b_phan_quyen.sql: xong"
fi

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa mật khẩu/khoá) — chép từ dòng này tới hết, gửi lại"

# Mỗi phép đo là MỘT câu SQL trả MỘT giá trị. Không đo được (kết nối/quyền/cú pháp hỏng) ⇒ rỗng ⇒ ĐỎ (Đ5).
do_mot() {   # $1=vai $2=mật khẩu $3=SQL → in giá trị (rỗng nếu lỗi)
  psql_vai "$1" "$2" -tA -v ON_ERROR_STOP=1 -c "$3" 2>/dev/null | head -1 | tr -d '\r' || true
}
thu_ghi() {  # $1=vai $2=mật khẩu $3=SQL → in LỜI của PG (cả lỗi) để mục khớp chữ; rỗng nếu không nối được
  psql_vai "$1" "$2" -tA -c "$3" 2>&1 | head -3 | tr '\n' ' ' | tr -d '\r' || true
}

KHO_LIT="'$KHO'"
LOP='n.nspname = '"'public'"' AND c.relkind IN ('"'r','p'"')'       # bảng (kể bảng chia)
LOP_V='n.nspname = '"'public'"' AND c.relkind IN ('"'r','p','v'"')' # bảng + view
JOIN='FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace'

export R_PROJECT="$PROJECT" R_INSTANCE="$INSTANCE" R_KHO="$KHO" R_CONN="$CONN" R_KIEM="$KIEM"
export R_PHIEN_BAN="$(do_mot "$ADMIN" "$MK_ADMIN" "SHOW server_version_num")"
export R_SO_TEP_DI_TRU="$(ls "$GOC"/fls/db/migrations/*.sql 2>/dev/null | wc -l | tr -d ' ')"
export R_DA_AP="$(do_mot "$ADMIN" "$MK_ADMIN" "SELECT count(*) FROM $SO_DI_TRU")"
PY="${PY:-$(tim_python)}"
export R_PG_VERIFY="$( ( cd "$GOC" && PGPASSWORD="$MK_ADMIN" PYTHONUTF8=1 \
    PG_DSN="postgresql://$ADMIN@$HOST:$CONG_PROXY/$KHO" "$PY" -m fls.db.pg_verify 2>&1 ) | head -1 | tr -d '\r' || true )"
export R_MAU_SO="$(do_mot "$ADMIN" "$MK_ADMIN" "SELECT count(*) $JOIN WHERE $LOP_V")"
export R_KHONG_CHU="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(*) $JOIN WHERE n.nspname='public' AND c.relkind IN ('r','p','v','S') AND pg_get_userbyid(c.relowner) <> '$ADMIN'")"
export R_CHU_KHO="$(do_mot "$ADMIN" "$MK_ADMIN" "SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname = $KHO_LIT")"
export R_PUBLIC_CO_QUYEN="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(*) FROM (SELECT (aclexplode(c.relacl)).grantee g $JOIN WHERE $LOP_V AND c.relacl IS NOT NULL) x WHERE g = 0")"

# fls_ghi
export R_GHI_THIEU_DML="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(*) $JOIN WHERE $LOP AND c.relname NOT IN ('$SO','$SO_DI_TRU') AND NOT (
     has_table_privilege('$GHI', c.oid, 'SELECT') AND has_table_privilege('$GHI', c.oid, 'INSERT')
     AND has_table_privilege('$GHI', c.oid, 'UPDATE') AND has_table_privilege('$GHI', c.oid, 'DELETE'))")"
export R_GHI_SO_QUYEN="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT coalesce(string_agg(p, ',' ORDER BY p), '') FROM unnest(ARRAY['SELECT','INSERT','UPDATE','DELETE','TRUNCATE','REFERENCES','TRIGGER']) p
    WHERE has_table_privilege('$GHI', '$SO', p)")"
export R_GHI_DI_TRU_QUYEN="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT coalesce(string_agg(p, ',' ORDER BY p), '') FROM unnest(ARRAY['SELECT','INSERT','UPDATE','DELETE','TRUNCATE']) p
    WHERE has_table_privilege('$GHI', '$SO_DI_TRU', p)")"
# `WHERE false` ⇒ ⛔ chạm một dòng; quyền được kiểm TRƯỚC khi quét dòng ⇒ bị chặn thì có chữ "permission denied".
export R_GHI_UPDATE_SO="$(thu_ghi "$GHI" "$MK_GHI" "UPDATE $SO SET itl_id = itl_id WHERE false")"
export R_GHI_DELETE_SO="$(thu_ghi "$GHI" "$MK_GHI" "DELETE FROM $SO WHERE false")"
export R_GHI_SELECT_SO="$(do_mot "$GHI" "$MK_GHI" "SELECT count(*) >= 0 FROM $SO")"

# fls_doc
export R_DOC_THIEU_SELECT="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(*) $JOIN WHERE $LOP_V AND NOT has_table_privilege('$DOC', c.oid, 'SELECT')")"
export R_DOC_CO_GHI="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(*) $JOIN WHERE $LOP AND (has_table_privilege('$DOC', c.oid, 'INSERT') OR has_table_privilege('$DOC', c.oid, 'UPDATE')
     OR has_table_privilege('$DOC', c.oid, 'DELETE') OR has_table_privilege('$DOC', c.oid, 'TRUNCATE'))")"
export R_DOC_PHIEN="$(do_mot "$DOC" "$MK_DOC" "SHOW default_transaction_read_only")"
export R_DOC_VAI_CAU_HINH="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT coalesce(bool_or('default_transaction_read_only=on' = ANY(rolconfig)), false) FROM pg_roles WHERE rolname = '$DOC'")"
# `CREATE TABLE` trong phiên chỉ-đọc ⇒ PG nổ "read-only transaction" TRƯỚC khi xét quyền schema.
# ⭐ `STG-R1-08`: bọc `BEGIN … ROLLBACK` — nếu `fls_doc` còn `CREATE` trên `public` và HẾT chỉ-đọc, bảng ⛔ được để lại (trước đây
#   `--kiem` "chỉ ĐỌC" tạo bảng THẬT rồi `02b` chết `permission denied for table fls_probe_doc_ghi`); khi đó mục này ĐỎ vì ⛔ có chữ "read-only".
export R_DOC_THU_GHI="$(thu_ghi "$DOC" "$MK_DOC" "BEGIN; CREATE TABLE fls_probe_doc_ghi (i int); ROLLBACK;")"
export R_SUPER="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(*) FROM pg_roles WHERE rolname IN ('$GHI','$DOC') AND (rolsuper OR rolcreaterole OR rolcreatedb OR rolreplication OR rolbypassrls)")"
export R_THANH_VIEN="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(*) FROM pg_auth_members m JOIN pg_roles g ON g.oid = m.roleid JOIN pg_roles u ON u.oid = m.member
    WHERE g.rolname = 'cloudsqlsuperuser' AND u.rolname IN ('$GHI','$DOC')")"
export R_MAU_VAI="$(do_mot "$ADMIN" "$MK_ADMIN" "SELECT count(*) FROM pg_roles WHERE rolname IN ('$GHI','$DOC','$ADMIN')")"
# Phép đo phân xử H-A/H-B (`STG-R2b-02`) — CHỈ IN, ⛔ chấm: vai SQL tạo ⇒ PG16 cấp ADMIN OPTION cho người tạo ⇒ mong 2.
export R_QT_ADMIN="$(do_mot "$ADMIN" "$MK_ADMIN" \
  "SELECT count(DISTINCT r.rolname) FROM pg_auth_members m JOIN pg_roles r ON r.oid = m.roleid JOIN pg_roles u ON u.oid = m.member
    WHERE r.rolname IN ('$GHI','$DOC') AND u.rolname = '$QT_USER' AND m.admin_option")"

python3 - <<'PY'
import os, re
e = os.environ
def so(v):
    try: return int(v)
    except (TypeError, ValueError): return None          # ⛔ đo được ⇒ None ⇒ ĐỎ
def co(chuoi, mau): return bool(re.search(mau, chuoi or "", re.I))

da_ap, tep = so(e["R_DA_AP"]), so(e["R_SO_TEP_DI_TRU"])
mau_so = so(e["R_MAU_SO"])
hang = [
  ("project · instance · kho", f'{e["R_PROJECT"]} · {e["R_INSTANCE"]} · {e["R_KHO"]}', None),
  ("connectionName", e["R_CONN"], None),
  # ── nền: máy đúng loại, di trú đủ, kho khớp khai báo ──
  ("PG phiên bản chính",           e["R_PHIEN_BAN"][:2] or None,                  "16"),
  ("tệp di trú trong repo (đếm)",  tep,                                            None),
  ("di trú đã áp = số tệp",        None if (da_ap is None or not tep) else da_ap == tep, True),
  ("pg_verify (4 ký tự đầu)",      (e["R_PG_VERIFY"] or "")[:4] or None,           "khop"),
  ("MẪU SỐ bảng+view (đếm)",       mau_so,                                         None),
  ("mẫu số ≠ 0",                   None if mau_so is None else mau_so > 0,         True),
  ("chủ kho",                      e["R_CHU_KHO"] or None,                         "fls_admin"),
  ("bảng/view/seq KHÔNG thuộc fls_admin", so(e["R_KHONG_CHU"]),                    0),
  ("bảng/view còn quyền cho PUBLIC",      so(e["R_PUBLIC_CO_QUYEN"]),              0),
  # ── fls_ghi ──
  ("fls_ghi · bảng thiếu DML (trừ fls_itl, fls_migration)", so(e["R_GHI_THIEU_DML"]), 0),
  ("fls_ghi · quyền trên fls_itl", e["R_GHI_SO_QUYEN"] or None,                    "INSERT,SELECT"),
  ("fls_ghi · quyền trên fls_migration", e["R_GHI_DI_TRU_QUYEN"] or None,          "SELECT"),
  ("fls_ghi · UPDATE fls_itl bị chặn",  co(e["R_GHI_UPDATE_SO"], "permission denied"),   True),
  ("fls_ghi · DELETE fls_itl bị chặn",  co(e["R_GHI_DELETE_SO"], "permission denied"),   True),
  ("fls_ghi · SELECT fls_itl chạy được", e["R_GHI_SELECT_SO"] == "t",               True),
  # ── fls_doc ──
  ("fls_doc · bảng/view thiếu SELECT",  so(e["R_DOC_THIEU_SELECT"]),                0),
  ("fls_doc · bảng có quyền GHI",       so(e["R_DOC_CO_GHI"]),                      0),
  ("fls_doc · default_transaction_read_only (phiên mới)", e["R_DOC_PHIEN"] or None, "on"),
  ("fls_doc · ALTER ROLE đã đặt",       e["R_DOC_VAI_CAU_HINH"] == "t",             True),
  ("fls_doc · CREATE TABLE bị PG từ chối vì chỉ-đọc", co(e["R_DOC_THU_GHI"], "read-only transaction"), True),
  # ── hai vai ứng dụng ⛔ quyền thừa ──
  ("MẪU SỐ vai (fls_admin·ghi·doc)",    so(e["R_MAU_VAI"]),                         3),
  ("fls_ghi/fls_doc: siêu quyền hay CREATEROLE/CREATEDB (đếm vai)", so(e["R_SUPER"]), 0),
  ("fls_ghi/fls_doc là thành viên cloudsqlsuperuser (đếm)", so(e["R_THANH_VIEN"]), 0),
  ("(đo, ⛔ chấm) vai quản trị có ADMIN OPTION trên fls_ghi/fls_doc (đếm vai)", so(e["R_QT_ADMIN"]), None),
]
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:58}  {gt}")
    else:
        ok = gt == mong
        do += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:56}  {gt!r}  (mong {mong!r})")
che_do = "--kiem (chỉ đọc)" if e["R_KIEM"] == "1" else "làm"
print(f"\n══ chế độ: {che_do} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
