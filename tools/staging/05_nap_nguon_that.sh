#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 05 — nạp DỮ LIỆU NGUỒN THẬT (sổ ITL · PM · 68 dòng chảy · Mapping Master · ảnh chụp 60 sao kê) · WO-334 AC-2
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell, SAU khi 01 · 02 · 04 báo `KẾT: ĐẠT`.
#  ⛔ Claude KHÔNG vào GCP (quyết chủ 20/11) — chủ chạy, rồi gửi lại PHẦN "BÁO CÁO" (chỉ SỐ ĐẾM, ⛔ tên người/số TK/tiền dòng).
#  Quyết chủ 23/11: staging dùng DỮ LIỆU THẬT (chủ chấp nhận rủi ro tên người + tiền thật trên staging).
#
#    bash tools/staging/05_nap_nguon_that.sh --project <ID> [CÁCH CẤP QUYỀN ĐỌC SHEET] --kiem
#    FLS_CHO_GHI_THAT=1 bash tools/staging/05_nap_nguon_that.sh --project <ID> --nguoi-nap <tên.người> [CÁCH CẤP QUYỀN ĐỌC SHEET]
#
#  CÁCH CẤP QUYỀN ĐỌC SHEET — chọn MỘT (⛔ khoá nào nằm trong repo/chat; script ⛔ in khoá/token):
#    --sa-json-tep <đường dẫn>   tệp khoá SA ĐỌC-SHEET (chủ tải lên Cloud Shell, chmod 600; XOÁ sau khi nạp xong).
#                                SA phải được CHIA SẺ quyền "Người xem" (Viewer) trên các workbook nguồn (Drive).
#    --adc                       Application Default Credentials (SA gắn với máy, hoặc `gcloud auth application-default login
#                                --scopes=…/spreadsheets.readonly,…/drive.metadata.readonly` bằng tài khoản có quyền xem sheet).
#    --token-gcloud              dùng tài khoản gcloud đang đăng nhập: script chạy
#                                `gcloud auth print-access-token --scopes=…spreadsheets.readonly,…drive.metadata.readonly`
#                                (⇒ tài khoản của CHỦ phải xem được các workbook; token ~60 phút, hết ⇒ chạy lại — công cụ chạy lại được).
#    (hoặc đã đặt sẵn biến FLS_SHEETS_TOKEN / FLS_GSHEETS_SA_JSON_B64 trong môi trường — script dùng nguyên.)
#
#  Tuỳ chọn: --region · --instance (fls-staging) · --kho (fls) · --cong-proxy (5432) · --proxy <cloud-sql-proxy>
#  Biến: FLS_STG_PYTHON (python có `psycopg`+`google-auth`; mặc định tự dựng venv ~/.fls-staging-venv)
#
#  LÀM GÌ: ① Auth Proxy → Cloud SQL, mật khẩu `fls_ghi` từ Secret Manager (⛔ in) ② `tools/staging/nap_nguon_that.py --nap`
#    (4 bước theo thứ tự phụ thuộc, gọi các công cụ nạp SẴN CÓ) ③ BÁO CÁO. `--kiem` = CHỈ ĐỌC nguồn + in số đếm (⛔ ghi một dòng).
#  Chạy lại được: `fls_itl` chỉ-THÊM (INV-I08) ⇒ lần 2 ⛔ nhân đôi (dòng trùng nhảy qua, BÁO CÁO nói bao nhiêu).
#  ⛔ ghi một ô nào về sheet (QĐ-ITL-34) · ⛔ `sao_luu/` `hien_vat/` tải lên · ⛔ kho `fls-pg-1` (cổng 5433).
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="asia-southeast1" ; INSTANCE="fls-staging" ; KHO="fls" ; KIEM=0 ; NGUOI=""
CONG_PROXY=5432 ; PROXY_BIN="" ; SA_TEP="" ; DUNG_ADC=0 ; TOKEN_GCLOUD=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project)    PROJECT="$2"; shift 2 ;;
    --region)     REGION="$2"; shift 2 ;;
    --instance)   INSTANCE="$2"; shift 2 ;;
    --kho)        KHO="$2"; shift 2 ;;
    --cong-proxy) CONG_PROXY="$2"; shift 2 ;;
    --proxy)      PROXY_BIN="$2"; shift 2 ;;
    --nguoi-nap)  NGUOI="$2"; shift 2 ;;
    --sa-json-tep) SA_TEP="$2"; shift 2 ;;
    --adc)        DUNG_ADC=1; shift ;;
    --token-gcloud) TOKEN_GCLOUD=1; shift ;;
    --kiem)       KIEM=1; shift ;;
    -h|--help)    sed -n 2,34p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
case "$CONG_PROXY" in ''|*[!0-9]*) echo "⛔ --cong-proxy phải là số" >&2; exit 2 ;; esac
case "$KHO" in ''|*[!a-z0-9_]*) echo "⛔ --kho chỉ gồm [a-z0-9_]" >&2; exit 2 ;; esac
if [ "$KIEM" -eq 0 ]; then
  [ "${FLS_CHO_GHI_THAT:-}" = "1" ] || { echo "⛔ nạp nguồn là GHI vào kho — đòi FLS_CHO_GHI_THAT=1" >&2; exit 2; }
  case "$NGUOI" in ''|*@*|*[!A-Za-z0-9._-]*) echo "⛔ cần --nguoi-nap <tên.người> (chỉ [A-Za-z0-9._-]; ⛔ email, ⛔ rỗng)" >&2; exit 2 ;; esac
fi
# ── Cách cấp quyền đọc sheet: đúng MỘT, hoặc đã có sẵn trong môi trường ──
co=0
[ -n "$SA_TEP" ] && co=$((co+1)); [ "$DUNG_ADC" -eq 1 ] && co=$((co+1)); [ "$TOKEN_GCLOUD" -eq 1 ] && co=$((co+1))
[ "$co" -le 1 ] || { echo "⛔ chọn MỘT cách cấp quyền đọc sheet (--sa-json-tep | --adc | --token-gcloud)" >&2; exit 2; }
if [ -n "$SA_TEP" ]; then
  [ -f "$SA_TEP" ] || { echo "⛔ không thấy tệp khoá: $SA_TEP" >&2; exit 2; }
  export FLS_SHEETS_SA_JSON_TEP="$SA_TEP"
elif [ "$DUNG_ADC" -eq 1 ]; then
  export FLS_SHEETS_ADC=1
fi
if [ "$co" -eq 0 ] && [ -z "${FLS_SHEETS_TOKEN:-}" ] && [ -z "${FLS_GSHEETS_SA_JSON_B64:-}" ] && [ -z "${FLS_GSHEETS_SA_JSON:-}" ]; then
  echo "⛔ chưa khai cách cấp quyền ĐỌC sheet. Chọn: --sa-json-tep <tệp> | --adc | --token-gcloud (xem đầu tệp)." >&2; exit 2
fi
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }
[ -n "$PROXY_BIN" ] || PROXY_BIN="$(command -v cloud-sql-proxy || true)"
[ -n "$PROXY_BIN" ] && [ -x "$PROXY_BIN" ] || {
  echo "⛔ không thấy cloud-sql-proxy (bản v2). Tải một lần rồi chạy lại với --proxy <đường dẫn>:" >&2
  echo "   https://cloud.google.com/sql/docs/postgres/sql-proxy#install  (tệp linux.amd64, chmod +x)" >&2
  exit 2; }

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
G=(gcloud --project="$PROJECT" --quiet)
HOST=127.0.0.1 ; VAI="fls_ghi"
buoc() { printf '\n── %s\n' "$*"; }

if [ "$TOKEN_GCLOUD" -eq 1 ]; then
  FLS_SHEETS_TOKEN="$(gcloud auth print-access-token \
     --scopes=https://www.googleapis.com/auth/spreadsheets.readonly,https://www.googleapis.com/auth/drive.metadata.readonly 2>/dev/null)" \
    || { echo "⛔ gcloud không cấp được token với phạm vi chỉ-đọc Sheets/Drive — tài khoản đăng nhập có quyền ấy chưa?" >&2; exit 2; }
  [ -n "$FLS_SHEETS_TOKEN" ] || { echo "⛔ token rỗng" >&2; exit 2; }
  export FLS_SHEETS_TOKEN
fi

MK="$("${G[@]}" secrets versions access latest --secret=fls-staging-pg-fls_ghi 2>/dev/null)" \
  || { echo "⛔ không đọc được bí mật fls-staging-pg-fls_ghi — bước 01 đã ĐẠT chưa?" >&2; exit 1; }

buoc "① Cloud SQL Auth Proxy → $INSTANCE ($REGION)"
CONN="$("${G[@]}" sql instances describe "$INSTANCE" --format='value(connectionName)')"
[ -n "$CONN" ] || { echo "⛔ không đọc được connectionName của $INSTANCE" >&2; exit 2; }
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
[ "$sang" -eq 1 ] || { echo "⛔ proxy ⛔ lên cổng $CONG_PROXY" >&2; sed -n 1,20p "$PROXY_LOG" >&2; exit 2; }
echo "   proxy lên ở $HOST:$CONG_PROXY"

tim_python() {
  if [ -n "${FLS_STG_PYTHON:-}" ]; then printf '%s' "$FLS_STG_PYTHON"; return; fi
  local venv="$HOME/.fls-staging-venv"
  if [ ! -x "$venv/bin/python" ]; then python3 -m venv "$venv" >&2; fi
  # idempotent: thiếu gói nào thì cài (psycopg cho kho; google-auth+requests cho SA/ADC)
  "$venv/bin/python" -c "import psycopg, google.auth, requests" >/dev/null 2>&1 || \
    "$venv/bin/pip" install --quiet "$(grep -i '^psycopg' "$GOC/requirements.txt" | head -1)" google-auth requests >&2
  printf '%s' "$venv/bin/python"
}
PY="$(tim_python)"
export PYTHONUTF8=1
export PG_DSN="postgresql://$VAI@$HOST:$CONG_PROXY/$KHO"

if [ "$KIEM" -eq 1 ]; then
  buoc "② CHỈ ĐỌC nguồn (--kiem; ⛔ ghi một dòng)"
  ( cd "$GOC" && PGPASSWORD="$MK" "$PY" tools/staging/nap_nguon_that.py --kiem ) || rc=$?
else
  buoc "② nạp nguồn THẬT (người nạp: $NGUOI) + BÁO CÁO"
  ( cd "$GOC" && PGPASSWORD="$MK" FLS_CHO_GHI_THAT=1 "$PY" tools/staging/nap_nguon_that.py --nap --nguoi-nap "$NGUOI" ) || rc=$?
fi
echo
echo "══ chế độ: $([ "$KIEM" -eq 1 ] && echo '--kiem (chỉ đọc)' || echo 'nạp') · thoát: ${rc:-0}  (0 = BÁO CÁO ĐẠT; 1 = có mục ĐỎ có tên — gửi lại BÁO CÁO)"
echo "⚠ Nhớ XOÁ tệp khoá SA khỏi Cloud Shell nếu đã tải lên: rm -f <tệp>"
exit "${rc:-0}"
