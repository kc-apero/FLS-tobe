#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — script KHỞI ĐỘNG của VM `fls-staging-app` (GCE `startup-script`, chạy bằng root mỗi lần boot)
# ══════════════════════════════════════════════════════════════════════════════════════════
#  Do `tools/staging/03_dung_app.sh` đặt làm metadata `startup-script`. ⛔ Chạy tay.
#  Đọc cấu hình từ metadata thuộc tính của VM (⛔ bí mật nào ở đây): fls-image · fls-project · fls-conn · fls-che-do
#  Chạy lại (reset VM sau khi đổi `fls-image`) ⇒ kéo ảnh mới + thay container.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail
MD="http://metadata.google.internal/computeMetadata/v1"
md() { curl -fsS -H 'Metadata-Flavor: Google' "$MD/$1"; }

IMAGE="$(md instance/attributes/fls-image)"
PROJECT="$(md instance/attributes/fls-project)"
CONN="$(md instance/attributes/fls-conn)"
CHE_DO="$(md instance/attributes/fls-che-do || echo doc)"

command -v docker >/dev/null || { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker.io; }
systemctl enable --now docker

# Đăng nhập Artifact Registry bằng token của SA gắn VM (⛔ khoá tệp)
HOST="${IMAGE%%/*}"
md instance/service-accounts/default/token | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])' \
  | docker login -u oauth2accesstoken --password-stdin "$HOST" >/dev/null

docker pull "$IMAGE"
docker rm -f fls-app >/dev/null 2>&1 || true
# `--network host`: cửa nghe 127.0.0.1:8088 của CHÍNH VM (⛔ publish cổng); proxy nghe 127.0.0.1:5432.
docker run -d --name fls-app --restart=always --network host \
  -e FLS_STG_PROJECT="$PROJECT" -e FLS_STG_CONN="$CONN" -e FLS_STG_CHE_DO="$CHE_DO" \
  "$IMAGE"
