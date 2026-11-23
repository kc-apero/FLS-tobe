#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — THỬ dựng ảnh app bằng BỘ BUILD CŨ (⛔ BuildKit) — đúng bộ `gcloud builds submit --tag` dùng
# ══════════════════════════════════════════════════════════════════════════════════════════
#    bash tools/staging/thu_dung_anh.sh [--ca <tệp PEM>]      # cần dockerd; in KẾT: ĐẠT / ĐỎ (exit 0 / 1)
#
#  ⭐ `STG-R2b-05` (lỗi THẬT GCP 23/11): Cloud Build chết ở Step 9/16 "the --mount option requires BuildKit" — bài
#    cục bộ dựng bằng `docker build` CÓ BuildKit ⇒ xanh giả (cả R2 `KQ-328` cùng điểm mù). Công cụ này dựng ĐÚNG
#    ngữ cảnh của bước 03 (`ngu_canh_build.sh`) với `DOCKER_BUILDKIT=0`. ⛔ là bài pytest: đường nền đòi
#    `skipped = 0` mà dockerd ⛔ có sẵn ở mọi container — bài tĩnh `test_03…buildkit` canh cú pháp mọi lúc.
#  `--ca`: CHỈ máy dev sau proxy tự ký (Cloud Build ⛔ cần) — đi vào `--build-arg PIP_CA_PEM` của tầng `goi`;
#    ảnh cuối ⛔ mang nó (đo: `docker history` + tìm tệp — phép kiểm ③ dưới).
#  Mong (Đ5 — ⛔ đo được ⇒ ĐỎ): ① dựng exit 0 · ② `the --mount option requires BuildKit` ⛔ xuất hiện ·
#    ③ ảnh cuối ⛔ chứa CA (0 dòng `BEGIN CERTIFICATE`/`PIP_CA_PEM` trong history) · ④ chạy bằng uid 10001.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -uo pipefail
CA=""
while [ $# -gt 0 ]; do case "$1" in --ca) CA="$2"; shift 2 ;; *) echo "⛔ tham số lạ: $1" >&2; exit 2 ;; esac; done
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
docker info >/dev/null 2>&1 || { echo "⛔ KẾT: ĐỎ — ⛔ nối được dockerd (⛔ đo được ⇒ ĐỎ, Đ5)"; exit 1; }
CTX="$(mktemp -d)"; LOG="$(mktemp)"; ANH="fls-app:thu-khong-buildkit-$$"
trap 'rm -rf "$CTX" "$LOG"; docker rmi -f "$ANH" >/dev/null 2>&1 || true' EXIT
bash "$GOC/tools/staging/ngu_canh_build.sh" "$GOC" "$CTX" || { echo "⛔ KẾT: ĐỎ — ngữ cảnh hỏng"; exit 1; }
ARG=(); [ -z "$CA" ] || ARG=(--build-arg "PIP_CA_PEM=$(cat "$CA")")
DOCKER_BUILDKIT=0 docker build "${ARG[@]}" -t "$ANH" "$CTX" >"$LOG" 2>&1; RC=$?
tail -3 "$LOG" | sed 's/^/   │ /'
do=0
kq() { if [ "$2" = "$3" ]; then echo "   [ĐẠT] $1  $2"; else echo "   [ĐỎ] $1  $2  (mong $3)"; do=$((do+1)); fi; }
kq "① DOCKER_BUILDKIT=0 docker build (exit)" "$RC" 0
kq "② dòng 'requires BuildKit' (đếm)" "$(grep -c 'requires BuildKit' "$LOG")" 0
if [ "$RC" -eq 0 ]; then
  kq "③ ảnh cuối mang CA/PIP_CA_PEM trong history (đếm)" "$(docker history --no-trunc "$ANH" | grep -c 'BEGIN CERTIFICATE\|PIP_CA_PEM')" 0
  kq "④ uid chạy" "$(docker run --rm --entrypoint id "$ANH" -u)" 10001
else
  kq "③④ ảnh để soi" "⛔ có ảnh" "có ảnh"
fi
echo; echo "══ KẾT: $([ "$do" -eq 0 ] && echo ĐẠT || echo "ĐỎ — $do mục khác mong")"
exit $((do > 0))
