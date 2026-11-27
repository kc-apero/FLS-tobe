#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — điểm vào Cloud Run của CỔNG MCP `fls-staging-mcp` (WO-371) · CÙNG ảnh với app, KHÁC điểm vào
# ══════════════════════════════════════════════════════════════════════════════════════════
#  Biến (do `tools/staging/10_mcp.sh` đặt khi deploy):
#    FLS_STG_PROJECT   project GCP                                                (bắt buộc)
#    FLS_STG_CONN      connectionName `project:region:instance` — Cloud Run gắn socket `/cloudsql/<CONN>`
#                      (`--add-cloudsql-instances`; ⛔ cloud-sql-proxy trong container)       (bắt buộc)
#    FLS_MCP_URL       URL công khai của chính service (https://….run.app) — `aud` của token + issuer OAuth (bắt buộc)
#    PORT              Cloud Run đặt (8080)
#    FLS_STG_KHO (fls) · FLS_STG_PYTHON · FLS_STG_SOCKET_GOC (/cloudsql)            — chỉ để bài thử
#
#  Bí mật đọc LÚC CHẠY bằng SA `fls-staging-mcp` (`lay_bi_mat.py` — metadata server), ⛔ `--set-secrets`/biến service
#  (⛔ hiện trong `gcloud run services describe`):
#    fls-staging-pg-fls_doc     mật khẩu vai CHỈ ĐỌC `fls_doc` (bước 01/02)
#    fls-staging-mcp-khoa       khoá ký HMAC (hex, 64 byte) — 10 tự sinh
#    fls-staging-mcp-oauth      JSON {"client_id","client_secret"} của OAuth client Google (chủ tạo ở Console)
#    fls-staging-mcp-cho-phep   danh sách email cách dấu phẩy — mặc định CHỈ tài khoản chạy 10
#
#  ⛔ Vai `fls_ghi` · khoá JWT của cửa · mật khẩu quản trị: SA ⛔ có quyền đọc (10 cấp ĐÚNG 4 bí mật trên).
#  ⛔ Bí mật ⛔ in, ⛔ ghi tệp; chỉ vào môi trường của MỘT tiến trình con (`exec`).
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

: "${FLS_STG_PROJECT:?⛔ thiếu FLS_STG_PROJECT}"
: "${FLS_STG_CONN:?⛔ thiếu FLS_STG_CONN (project:region:instance)}"
: "${FLS_MCP_URL:?⛔ thiếu FLS_MCP_URL (URL công khai của service)}"
CONG="${PORT:-8080}"
KHO="${FLS_STG_KHO:-fls}"
PY="${FLS_STG_PYTHON:-python}"
SOCK="${FLS_STG_SOCKET_GOC:-/cloudsql}/$FLS_STG_CONN"
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
case "$FLS_MCP_URL" in https://*) ;; *) echo "⛔ FLS_MCP_URL phải https:// (nhận: $FLS_MCP_URL)" >&2; exit 2 ;; esac

lay() { "$PY" "$GOC/tools/staging/app/lay_bi_mat.py" "$1"; }
MK="$(lay fls-staging-pg-fls_doc)";          [ -n "$MK" ]    || { echo "⛔ mật khẩu fls_doc rỗng" >&2; exit 1; }
KHOA="$(lay fls-staging-mcp-khoa)";          [ -n "$KHOA" ]  || { echo "⛔ khoá ký rỗng" >&2; exit 1; }
OAUTH="$(lay fls-staging-mcp-oauth)";        [ -n "$OAUTH" ] || { echo "⛔ OAuth client rỗng" >&2; exit 1; }
CHO="$(lay fls-staging-mcp-cho-phep)";       [ -n "$CHO" ]   || { echo "⛔ danh sách cho phép rỗng" >&2; exit 1; }
GID="$(printf '%s' "$OAUTH" | "$PY" -c 'import json,sys; print(json.load(sys.stdin)["client_id"])')"
GSEC="$(printf '%s' "$OAUTH" | "$PY" -c 'import json,sys; print(json.load(sys.stdin)["client_secret"])')"
N_CHO="$(printf '%s' "$CHO" | tr ',' '\n' | grep -c . || true)"

echo "vao_mcp.sh: vai=fls_doc kho=$KHO socket=$SOCK url=$FLS_MCP_URL cong=$CONG cho_phep=$N_CHO"
cd "$GOC"
# `PG_DSN` ⛔ mang mật khẩu — psycopg đọc PGPASSWORD. host = thư mục socket Cloud SQL.
export PGPASSWORD="$MK" PG_DSN="postgresql://fls_doc@/$KHO?host=$SOCK" \
       FLS_MCP_KHOA="$KHOA" FLS_MCP_GOOGLE_ID="$GID" FLS_MCP_GOOGLE_SECRET="$GSEC" FLS_MCP_CHO_PHEP="$CHO"
unset MK KHOA OAUTH CHO GSEC
exec "$PY" tools/chay_mcp.py --http --dia-chi 0.0.0.0 --cong "$CONG"
