#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — điểm vào của ảnh: bí mật từ Secret Manager → Cloud SQL Auth Proxy → CỬA API + MÀN HÌNH
# ══════════════════════════════════════════════════════════════════════════════════════════
#  Biến (do `tools/staging/vm_khoi_dong.sh` đặt từ metadata VM):
#    FLS_STG_PROJECT  project GCP                                  (bắt buộc)
#    FLS_STG_CONN     connectionName `project:region:instance`     (bắt buộc)
#    FLS_STG_CHE_DO   `doc` (mặc định, CHỈ ĐỌC · vai fls_doc) | `ghi` (vai fls_ghi + `--cho-ghi`: cho người
#                     test KÝ — tỷ giá tháng, bản báo cáo; nhóm ghi mở ⇒ sửa số THẬT trên staging)
#    FLS_STG_CONG_PROXY (5432) · FLS_STG_CONG (8088)
#    FLS_STG_PYTHON · FLS_STG_PROXY (đường dẫn cloud-sql-proxy) · FLS_STG_KHO (fls)   — chỉ để bài thử
#
#  ⛔ Cửa vẫn TỰ TỪ CHỐI (⛔ nới ở đây): thiếu FLS_JWT_SECRET · kết nối ĐỌC còn ghi được · `--dia-chi`
#     ngoài loopback khi `--cho-web`. Script này ⛔ truyền `--dia-chi` nào khác 127.0.0.1.
#  ⛔ Mật khẩu/khoá ⛔ in, ⛔ ghi tệp, ⛔ vào `docker inspect` (đọc LÚC CHẠY, không phải `-e`), ⛔ `PG_DSN`.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

: "${FLS_STG_PROJECT:?⛔ thiếu FLS_STG_PROJECT}"
: "${FLS_STG_CONN:?⛔ thiếu FLS_STG_CONN (project:region:instance)}"
CHE_DO="${FLS_STG_CHE_DO:-doc}"
CONG_PROXY="${FLS_STG_CONG_PROXY:-5432}"
CONG="${FLS_STG_CONG:-8088}"
KHO="${FLS_STG_KHO:-fls}"
PY="${FLS_STG_PYTHON:-python}"
PROXY="${FLS_STG_PROXY:-cloud-sql-proxy}"
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
case "$CHE_DO" in
  doc) VAI="fls_doc"; CO_GHI=() ;;
  ghi) VAI="fls_ghi"; CO_GHI=(--cho-ghi) ;;
  *) echo "⛔ FLS_STG_CHE_DO phải là doc|ghi (nhận: $CHE_DO)" >&2; exit 2 ;;
esac

lay() { "$PY" "$GOC/tools/staging/app/lay_bi_mat.py" "$1"; }
# Thiếu khoá JWT ⇒ DỪNG TRƯỚC khi mở proxy/kho (cùng tinh thần cửa: "không có chìa khoá thì không mở cửa").
JWT="$(lay fls-staging-jwt-secret)"
[ -n "$JWT" ] || { echo "⛔ khoá JWT rỗng" >&2; exit 1; }
MK="$(lay "fls-staging-pg-$VAI")"
[ -n "$MK" ] || { echo "⛔ mật khẩu $VAI rỗng" >&2; exit 1; }

"$PROXY" --address 127.0.0.1 --port "$CONG_PROXY" "$FLS_STG_CONN" &
PROXY_PID=$!
APP_PID=""
dep() { [ -n "$APP_PID" ] && kill "$APP_PID" 2>/dev/null || true; kill "$PROXY_PID" 2>/dev/null || true; }
trap dep EXIT
trap 'exit 143' TERM INT

"$PY" - "$CONG_PROXY" <<'PYEOF'
import socket, sys, time
cong = int(sys.argv[1]); han = time.time() + 30
while time.time() < han:
    try:
        socket.create_connection(("127.0.0.1", cong), timeout=1).close(); sys.exit(0)
    except OSError:
        time.sleep(0.5)
sys.exit("⛔ Cloud SQL Auth Proxy ⛔ lên cổng %d sau 30 giây" % cong)
PYEOF

echo "vao.sh: chế độ=$CHE_DO vai=$VAI kho=$KHO proxy=127.0.0.1:$CONG_PROXY cửa=127.0.0.1:$CONG"
# Bí mật chỉ vào môi trường của MỘT tiến trình con (cửa). `PG_DSN` KHÔNG mang mật khẩu — psycopg đọc PGPASSWORD.
cd "$GOC"
FLS_JWT_SECRET="$JWT" PGPASSWORD="$MK" PG_DSN="postgresql://$VAI@127.0.0.1:$CONG_PROXY/$KHO" \
  "$PY" tools/chay_cua.py --cho-web --dia-chi 127.0.0.1 --cong "$CONG" "${CO_GHI[@]}" &
APP_PID=$!
unset JWT MK
wait "$APP_PID"
