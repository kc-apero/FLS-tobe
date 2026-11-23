"""Đọc MỘT bí mật từ Secret Manager bằng danh tính của VM (metadata server) — chỉ stdlib.

    python tools/staging/app/lay_bi_mat.py <TÊN_BÍ_MẬT>      # in GIÁ TRỊ ra stdout, ⛔ gì khác

Biến: FLS_STG_PROJECT (bắt buộc) · FLS_STG_URL_METADATA / FLS_STG_URL_SM (chỉ để bài thử trỏ vào máy chủ giả).

⛔ Giá trị bí mật CHỈ đi ra stdout (để `$(...)` bắt). Lỗi ⛔ in giá trị, ⛔ in token; chỉ in TÊN bí mật + mã HTTP.
⭐ Vì sao ⛔ dùng `gcloud` trong ảnh: ảnh slim ⛔ có gcloud; metadata server + REST là đường ngắn nhất và
   chạy bằng ĐÚNG SA `fls-staging-app` (đã được `01_dung_staging_gcp.sh` cấp `secretAccessor` trên 5 bí mật).
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request

TOKEN_URL = "/computeMetadata/v1/instance/service-accounts/default/token"
MAC_DINH_METADATA = "http://metadata.google.internal"
MAC_DINH_SM = "https://secretmanager.googleapis.com"


def _lay(url: str, headers: dict[str, str]) -> dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:       # noqa: S310 — URL do script/bài thử đặt
        return json.loads(r.read().decode("utf-8"))


def lay_bi_mat(ten: str, project: str, metadata: str = MAC_DINH_METADATA, sm: str = MAC_DINH_SM) -> str:
    try:
        tok = _lay(metadata + TOKEN_URL, {"Metadata-Flavor": "Google"})["access_token"]
    except (urllib.error.URLError, KeyError, ValueError) as e:
        raise SystemExit(f"⛔ không lấy được token SA từ metadata server ({type(e).__name__}) — đây có phải VM GCP có SA gắn?")
    url = f"{sm}/v1/projects/{project}/secrets/{ten}/versions/latest:access"
    try:
        data = _lay(url, {"Authorization": f"Bearer {tok}"})
    except urllib.error.HTTPError as e:
        raise SystemExit(f"⛔ không đọc được bí mật {ten}: HTTP {e.code} (SA đã có secretAccessor chưa?)")
    except (urllib.error.URLError, ValueError) as e:
        raise SystemExit(f"⛔ không đọc được bí mật {ten}: {type(e).__name__}")
    try:
        return base64.b64decode(data["payload"]["data"]).decode("utf-8")
    except (KeyError, ValueError):
        raise SystemExit(f"⛔ bí mật {ten}: phản hồi thiếu payload")


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not argv[1].replace("-", "").replace("_", "").isalnum():
        print("cách dùng: lay_bi_mat.py <TÊN_BÍ_MẬT>", file=sys.stderr)
        return 2
    project = os.environ.get("FLS_STG_PROJECT", "")
    if not project:
        print("⛔ thiếu FLS_STG_PROJECT", file=sys.stderr)
        return 2
    sys.stdout.write(lay_bi_mat(argv[1], project,
                                os.environ.get("FLS_STG_URL_METADATA", MAC_DINH_METADATA),
                                os.environ.get("FLS_STG_URL_SM", MAC_DINH_SM)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
