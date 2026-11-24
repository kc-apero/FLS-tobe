#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — điểm vào của ảnh KHI CHẠY TRÊN CLOUD RUN (sau Google IAP) · WO-363
# ══════════════════════════════════════════════════════════════════════════════════════════
#  `07_link_web.sh` đặt `--command bash --args /app/tools/staging/app/vao_cloud_run.sh` cho service Cloud Run;
#  ENTRYPOINT của ảnh (VM, bước 03) vẫn là `vao.sh` — ⛔ đổi gì cho đường VM.
#
#    ① `vao.sh` NGUYÊN VẸN (bí mật từ Secret Manager → Cloud SQL Auth Proxy → cửa nghe 127.0.0.1:8088)
#    ② chờ cửa lên, rồi `cong_iap.py` nghe 0.0.0.0:$PORT (Cloud Run đặt `PORT`) — kiểm chữ ký IAP, chuyển tiếp
#       vào 127.0.0.1:8088. Cloud Run chỉ gửi yêu cầu khi `$PORT` mở ⇒ ⛔ yêu cầu nào tới trước khi cửa sẵn.
#    ③ tự đo MỘT lần, in dòng `TU_DO …` (cửa / 401 / nghe loopback / cổng chặn yêu cầu ⛔ IAP / JWT giả) — vào
#       nhật ký Cloud Run; `07_link_web.sh` đọc lại bằng `gcloud logging read` (mục BÁO CÁO "TRONG container").
#    ④ một trong hai tiến trình chết ⇒ thoát ≠ 0 (Cloud Run dựng lại container) — ⛔ cổng sống mà cửa chết.
#
#  ⛔ Cửa vẫn TỰ TỪ CHỐI nghe ngoài loopback (`GAP-WEB-01`) — script này ⛔ truyền `FLS_STG_CONG` = `$PORT`.
#  Biến: như `vao.sh` + `PORT` · `K_SERVICE` · `K_REVISION` (Cloud Run đặt) · `FLS_IAP_AUD` (tuỳ — ghim `aud`).
# ══════════════════════════════════════════════════════════════════════════════════════════
set -uo pipefail
: "${PORT:?⛔ thiếu PORT — chỉ chạy trên Cloud Run}"
: "${K_SERVICE:?⛔ thiếu K_SERVICE — chỉ chạy trên Cloud Run (trên VM dùng vao.sh)}"
CONG_CUA="${FLS_STG_CONG:-8088}"
PY="${FLS_STG_PYTHON:-python}"
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
[ "$PORT" != "$CONG_CUA" ] || { echo "⛔ PORT ($PORT) trùng cổng cửa ($CONG_CUA) — đặt --port khác khi deploy" >&2; exit 2; }

FLS_STG_CONG="$CONG_CUA" bash "$GOC/tools/staging/app/vao.sh" &
VAO=$!
CONG=""
dep() { [ -n "$CONG" ] && kill "$CONG" 2>/dev/null; kill "$VAO" 2>/dev/null; wait 2>/dev/null; true; }
trap dep EXIT
trap 'exit 143' TERM INT

"$PY" "$GOC/tools/staging/app/cong_iap.py" --doi-cua --cong-cua "$CONG_CUA" --han "${FLS_STG_HAN_CUA:-90}" || exit 1
kill -0 "$VAO" 2>/dev/null || { echo "⛔ vao.sh đã chết trước khi mở cổng" >&2; exit 1; }

"$PY" "$GOC/tools/staging/app/cong_iap.py" --cong "$PORT" --cong-cua "$CONG_CUA" &
CONG=$!
"$PY" "$GOC/tools/staging/app/cong_iap.py" --doi-cua --cong-cua "$PORT" --han 30 || exit 1
"$PY" "$GOC/tools/staging/app/cong_iap.py" --tu-do --cong "$PORT" --cong-cua "$CONG_CUA" || true

wait -n "$VAO" "$CONG"
echo "⛔ một tiến trình đã thoát (vao.sh hoặc cong_iap) — container dừng để Cloud Run dựng lại" >&2
exit 1
