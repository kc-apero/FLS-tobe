#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 04 — nạp config IX.* ĐÃ KÝ vào kho staging (qua Cloud SQL Auth Proxy) · WO-325 AC-3
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell, SAU khi bước 01 · 02 báo `KẾT: ĐẠT`.
#  ⛔ Claude KHÔNG vào GCP (quyết chủ 20/11) — chủ chạy, rồi gửi lại PHẦN "BÁO CÁO" ở cuối (⛔ mật khẩu/khoá).
#
#    bash tools/staging/04_nap_du_lieu.sh --project <PROJECT_ID> --kiem                       # chỉ ĐỌC — đo kho
#    FLS_CHO_GHI_THAT=1 bash tools/staging/04_nap_du_lieu.sh --project <PROJECT_ID> --nguoi-nap <tên.người>
#
#  Tuỳ chọn: --region · --instance (fls-staging) · --kho (fls) · --cong-proxy (5432) · --proxy <cloud-sql-proxy>
#  Biến: FLS_STG_PYTHON (python có `psycopg`; mặc định tự dựng venv ~/.fls-staging-venv)
#
#  LÀM GÌ:
#   ① Auth Proxy tới Cloud SQL (127.0.0.1) · đọc mật khẩu `fls_ghi` từ Secret Manager (⛔ in)
#   ② `tools/staging/nap_cau_hinh_ix.py` — gọi ĐÚNG các hàm nạp SẴN CÓ (`fls.repo.cau_hinh_repo.nap_ix_*`, ⛔ viết lại)
#      với ảnh ĐÃ KÝ commit ở `tests/fixture/cau_hinh/`: IX.FX · IX.HD · IX.PL · Mapping Master · IX.PER · IX.VEN · IX.ORG ·
#      IX.ALR (nền + bản KÝ bật cờ 2025 của KhanhCQ) · IX.DRV. Bảng ĐÃ có phiên bản ⇒ BỎ QUA (chạy lại được, ⛔ nạp chồng).
#   ③ BÁO CÁO: số dòng THẬT từng bảng + `mong` (hai chiều) + MẪU SỐ ≠ 0; thêm 3 phép đo riêng tư/phạm vi:
#      · cột nào của kho tên có "email" = 0 (`PM_COT_RIENG_TU = {"Email Address"}` ⛔ vào kho)
#      · cột `actor` của config có `@` = 0 (⛔ email làm danh tính)
#      · `fls_itl` = 0 dòng (⇒ chỉ-config; sổ ⛔ được nạp ở bước này)
#
#  ⛔⛔ DỮ LIỆU NGUỒN (sao kê/sổ — tiền THẬT) ⛔ NẠP Ở ĐÂY. "Thật hay ẩn danh" là CÂU CHỦ chưa trả lời (BG-326 §Câu chủ);
#     `--nguon-that` luôn từ chối (exit 2) và nói rõ vì sao. Các công cụ nạp nguồn sẵn có (`tools/nap_that.py`,
#     `nap_mapping_master.py`, `nap_nguon_va_khai.py`) đọc Google Sheets bằng một SA CỤC BỘ gắn cứng trong mã
#     (⛔ khoá SA trong repo/chat) ⇒ ⛔ chạy được ở Cloud Shell nếu chưa có phiếu bọc lại. Người test có thể tự nạp tệp qua
#     màn F04 `/nap` (đã có) khi chủ cho dùng dữ liệu nào.
#  ⛔ `sao_luu/` · `hien_vat/` ⛔ tải lên (⛔ đường nào tới đó); ⛔ `fls_itl` ⛔ ghi.
#
#  Luật đo (CLAUDE.md Đ3·Đ5): mỗi mục có `mong`; ⛔ đo được ⇒ ĐỎ; `0` đứng cạnh MẪU SỐ.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; REGION="asia-southeast1" ; INSTANCE="fls-staging" ; KHO="fls" ; KIEM=0 ; NGUOI="" ; NGUON_THAT=0
CONG_PROXY=5432 ; PROXY_BIN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --project)    PROJECT="$2"; shift 2 ;;
    --region)     REGION="$2"; shift 2 ;;
    --instance)   INSTANCE="$2"; shift 2 ;;
    --kho)        KHO="$2"; shift 2 ;;
    --cong-proxy) CONG_PROXY="$2"; shift 2 ;;
    --proxy)      PROXY_BIN="$2"; shift 2 ;;
    --nguoi-nap)  NGUOI="$2"; shift 2 ;;
    --nguon-that) NGUON_THAT=1; shift ;;
    --kiem)       KIEM=1; shift ;;
    -h|--help)    sed -n 2,40p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
if [ "$NGUON_THAT" -eq 1 ]; then
  cat >&2 <<'MSG'
⛔ --nguon-that: TỪ CHỐI. Hai lý do, đều đo được:
   1) "Dữ liệu thật hay ẩn danh" là CÂU CHỦ chưa trả lời (BG-326 §Câu chủ) — script ⛔ tự quyết đưa sổ kế toán thật lên staging.
   2) Công cụ nạp nguồn sẵn có (tools/nap_that.py · nap_mapping_master.py · nap_nguon_va_khai.py) lấy token Sheets bằng
      `gcloud auth print-access-token --account <SA cục bộ>` gắn cứng trong mã — ⛔ chạy được ở Cloud Shell nếu chưa có khoá SA
      (⛔ khoá SA vào repo/chat). Cần một phiếu WO bọc lại sau khi chủ trả lời câu 3.
   Trong lúc chờ: người test nạp tệp qua màn F04 /nap; config IX.* đã đủ để chạy chuỗi HD2 và xem F03.
MSG
  exit 2
fi
case "$CONG_PROXY" in ''|*[!0-9]*) echo "⛔ --cong-proxy phải là số" >&2; exit 2 ;; esac
case "$KHO" in ''|*[!a-z0-9_]*) echo "⛔ --kho chỉ gồm [a-z0-9_]" >&2; exit 2 ;; esac
if [ "$KIEM" -eq 0 ]; then
  [ "${FLS_CHO_GHI_THAT:-}" = "1" ] || { echo "⛔ nạp config là GHI vào kho — đòi FLS_CHO_GHI_THAT=1 (cùng cổng các công cụ ghi sổ)" >&2; exit 2; }
  case "$NGUOI" in ''|*@*|*[!A-Za-z0-9._-]*) echo "⛔ cần --nguoi-nap <tên.người> (chỉ [A-Za-z0-9._-]; ⛔ email, ⛔ rỗng) — cột actor là hành vi của NGƯỜI" >&2; exit 2 ;; esac
fi
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v psql    >/dev/null || { echo "⛔ không có psql" >&2; exit 2; }
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
  if [ ! -x "$venv/bin/python" ]; then
    python3 -m venv "$venv" >&2
    "$venv/bin/pip" install --quiet "$(grep -i '^psycopg' "$GOC/requirements.txt" | head -1)" >&2
  fi
  printf '%s' "$venv/bin/python"
}
PY="$(tim_python)"
export PYTHONUTF8=1
dsn_gia_tri() { printf 'postgresql://%s@%s:%s/%s' "$VAI" "$HOST" "$CONG_PROXY" "$KHO"; }

if [ "$KIEM" -eq 0 ]; then
  buoc "② nạp config IX.* đã ký (người nạp: $NGUOI)"
  ( cd "$GOC" && PGPASSWORD="$MK" PG_DSN="$(dsn_gia_tri)" FLS_CHO_GHI_THAT=1 \
      "$PY" tools/staging/nap_cau_hinh_ix.py --nguoi-nap "$NGUOI" ) \
    || echo "   ⚠ trình nạp thoát ≠ 0 — xem BÁO CÁO bên dưới (chạy lại được)"
fi

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa mật khẩu/khoá) — chép từ dòng này tới hết, gửi lại"
rc_cfg=0
( cd "$GOC" && PGPASSWORD="$MK" PG_DSN="$(dsn_gia_tri)" "$PY" tools/staging/nap_cau_hinh_ix.py --kiem ) || rc_cfg=$?

do_mot() { PGPASSWORD="$MK" PGCONNECT_TIMEOUT=20 psql -X -h "$HOST" -p "$CONG_PROXY" -U "$VAI" -d "$KHO" -tA -v ON_ERROR_STOP=1 -c "$1" 2>/dev/null | head -1 | tr -d '\r' || true; }
export R_EMAIL="$(do_mot "SELECT count(*) FROM information_schema.columns WHERE table_schema = 'public' AND column_name ILIKE '%email%'")"
export R_COT="$(do_mot "SELECT count(*) FROM information_schema.columns WHERE table_schema = 'public'")"
export R_ACTOR_AT="$(do_mot "SELECT count(*) FROM fls_cau_hinh_ban WHERE actor LIKE '%@%'")"
export R_ACTOR_N="$(do_mot "SELECT count(*) FROM fls_cau_hinh_ban")"
export R_SO="$(do_mot "SELECT count(*) FROM fls_itl")"
export R_RC="$rc_cfg" R_KIEM="$KIEM"
python3 - <<'PY'
import os
e = os.environ
def so(v):
    try: return int(v)
    except (TypeError, ValueError): return None
cot, n_ban = so(e["R_COT"]), so(e["R_ACTOR_N"])
hang = [
  ("MẪU SỐ — số cột của kho (đếm)",              cot,                               None),
  ("mẫu số cột ≠ 0",                              None if cot is None else cot > 0,  True),
  ("cột tên có 'email' (đếm, ⛔ vào kho)",         so(e["R_EMAIL"]),                  0),
  ("MẪU SỐ — số bản config (đếm)",                n_ban,                             None),
  ("mẫu số bản config ≠ 0",                       None if n_ban is None else n_ban > 0, True),
  ("bản config có actor chứa '@' (đếm)",          so(e["R_ACTOR_AT"]),               0),
  ("fls_itl số dòng (chỉ-config ⇒ 0; ⛔ sổ ở bước này)", so(e["R_SO"]),             0),
  ("trình đo config thoát",                       so(e["R_RC"]),                     0),
]
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print(f"   {ten:62}  {gt}")
    else:
        ok = gt == mong
        do += not ok
        print(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {ten:60}  {gt!r}  (mong {mong!r})")
che_do = "--kiem (chỉ đọc)" if e["R_KIEM"] == "1" else "nạp"
print(f"\n══ chế độ: {che_do} · KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
raise SystemExit(1 if do else 0)
PY
