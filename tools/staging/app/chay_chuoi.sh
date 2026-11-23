#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — "CHẠY CHUỖI" HD2: chạy mọi gói `tools/do_hd2.py --goi …` TRONG container app · WO-325 AC-4
# ══════════════════════════════════════════════════════════════════════════════════════════
#    docker exec fls-app bash /app/tools/staging/app/chay_chuoi.sh          # đo, ⛔ ghi tệp
#    docker exec fls-app bash /app/tools/staging/app/chay_chuoi.sh --ghi    # + ghi docs/ITL/_tools/hd2_cong.json (cửa đọc MỖI yêu cầu ⇒ F03 đổi ngay)
#
#  ⭐ "Chuỗi" là LỆNH (CPU ~28 giây · đỉnh 630 MB RSS — đo ở BG-326), ⛔ phải một yêu cầu HTTP: nên ⛔ có giới hạn
#     thời gian yêu cầu nào của cửa/Cloud Run dính vào nó.
#  Đọc kho bằng vai `fls_doc` (chỉ-ĐỌC) qua Auth Proxy của chính container; bí mật từ Secret Manager như `vao.sh`.
#  Danh sách gói lấy từ `tools.do_hd2.GOI_BIET` (⛔ chép tay ở đây). Gói nào ĐỎ ⇒ in tên + exit 1 (⛔ dừng giữa chừng).
# ══════════════════════════════════════════════════════════════════════════════════════════
set -uo pipefail
: "${FLS_STG_PROJECT:?⛔ thiếu FLS_STG_PROJECT}"
GHI=()
case "${1:-}" in "") ;; --ghi) GHI=(--ghi) ;; *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;; esac
CONG_PROXY="${FLS_STG_CONG_PROXY:-5432}"; KHO="${FLS_STG_KHO:-fls}"; PY="${FLS_STG_PYTHON:-python}"
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$GOC"
MK="$("$PY" tools/staging/app/lay_bi_mat.py fls-staging-pg-fls_doc)" || exit 1
[ -n "$MK" ] || { echo "⛔ mật khẩu fls_doc rỗng" >&2; exit 1; }
export PGPASSWORD="$MK" PG_DSN="postgresql://fls_doc@127.0.0.1:$CONG_PROXY/$KHO" PYTHONUTF8=1
unset MK
GOI="$("$PY" -c 'from tools.do_hd2 import GOI_BIET; print(*GOI_BIET)')" || { echo "⛔ không đọc được GOI_BIET" >&2; exit 1; }
sai=0; n=0
printf '%-9s %-6s %s\n' GOI THOAT GIAY
for g in $GOI; do
  t0=$(date +%s%N)
  "$PY" tools/do_hd2.py --goi "$g" "${GHI[@]}" >"/tmp/chuoi_$g.log" 2>&1; rc=$?
  t1=$(date +%s%N); ms=$(( (t1 - t0) / 1000000 ))
  printf '%-9s %-6s %d.%d\n' "$g" "$rc" $((ms / 1000)) $((ms % 1000 / 100))
  [ "$rc" -eq 0 ] || { sai=$((sai+1)); grep -m1 -E "ChuaKhai|KHONG DAT|✗" "/tmp/chuoi_$g.log" | cut -c1-200 | sed 's/^/    ⛔ /'; }
  n=$((n+1))
done
echo "══ CHUỖI: $n gói · ĐỎ $sai · KẾT: $([ "$sai" -eq 0 ] && echo ĐẠT || echo "ĐỎ — $sai gói")${GHI[*]:+ · đã ghi hd2_cong.json}"
[ "$sai" -eq 0 ]
