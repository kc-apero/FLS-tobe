"""Đọc MỘT bí mật từ Secret Manager bằng danh tính của VM (metadata server) — chỉ stdlib.

    python tools/staging/app/lay_bi_mat.py <TÊN_BÍ_MẬT>      # in GIÁ TRỊ ra stdout, ⛔ gì khác

Biến: FLS_STG_PROJECT (bắt buộc) · FLS_STG_URL_METADATA / FLS_STG_URL_SM (chỉ để bài thử trỏ vào máy chủ giả).

⛔ Giá trị bí mật CHỈ đi ra stdout (để `$(...)` bắt). Lỗi ⛔ in giá trị, ⛔ in token; chỉ in TÊN bí mật + mã HTTP.
⭐ Vì sao ⛔ dùng `gcloud` trong ảnh: ảnh slim ⛔ có gcloud; metadata server + REST là đường ngắn nhất và
   chạy bằng ĐÚNG SA `fls-staging-app` (đã được `01_dung_staging_gcp.sh` cấp `secretAccessor` trên ĐÚNG 3 bí mật app — `jwt` · `fls_ghi` · `fls_doc`; ⛔ `postgres` · `fls_admin`, `STG-R1-01`).
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


# ══ ĐƯỜNG GHI — chỉ cho trạng thái phiên đăng nhập `fls-staging-phien` (WO-363 · `STG-WEB-R1-02`) ══════════════════
#  SA `fls-staging-app` được `secretVersionManager` + `secretAccessor` trên ĐÚNG bí mật ấy (08 cấp) — ⛔ bí mật nào khác.
def _token(metadata: str) -> str:
    try:
        return _lay(metadata + TOKEN_URL, {"Metadata-Flavor": "Google"})["access_token"]
    except (urllib.error.URLError, KeyError, ValueError) as e:
        raise SystemExit(f"⛔ không lấy được token SA từ metadata server ({type(e).__name__})")


def _post(url: str, tok: str, than: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(than).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:       # noqa: S310 — URL do mã/bài thử đặt
        return json.loads(r.read().decode("utf-8") or "{}")


def lay_kem_ten(ten: str, project: str, metadata: str = MAC_DINH_METADATA, sm: str = MAC_DINH_SM) -> tuple[str, str]:
    """(giá trị, tên đầy đủ phiên bản `projects/…/secrets/…/versions/N`) của phiên bản mới nhất."""
    tok = _token(metadata)
    try:
        data = _lay(f"{sm}/v1/projects/{project}/secrets/{ten}/versions/latest:access", {"Authorization": f"Bearer {tok}"})
        return base64.b64decode(data["payload"]["data"]).decode("utf-8"), str(data.get("name", ""))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"⛔ không đọc được bí mật {ten}: HTTP {e.code}")
    except (urllib.error.URLError, KeyError, ValueError) as e:
        raise SystemExit(f"⛔ không đọc được bí mật {ten}: {type(e).__name__}")


def them_phien_ban(ten: str, project: str, gia_tri: str, metadata: str = MAC_DINH_METADATA, sm: str = MAC_DINH_SM) -> str:
    """`secrets/<ten>:addVersion` — trả tên phiên bản mới. Hỏng ⇒ SystemExit (⛔ in giá trị)."""
    tok = _token(metadata)
    try:
        o = _post(f"{sm}/v1/projects/{project}/secrets/{ten}:addVersion", tok,
                  {"payload": {"data": base64.b64encode(gia_tri.encode("utf-8")).decode()}})
        return str(o.get("name", ""))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"⛔ không ghi được bí mật {ten}: HTTP {e.code} (SA có secretVersionManager chưa?)")
    except (urllib.error.URLError, ValueError) as e:
        raise SystemExit(f"⛔ không ghi được bí mật {ten}: {type(e).__name__}")


def huy_phien_ban(ten_day_du: str, metadata: str = MAC_DINH_METADATA, sm: str = MAC_DINH_SM) -> None:
    """`…/versions/N:destroy` — phiên bản CŨ của trạng thái (⛔ để phiên bản dồn lại). Hỏng ⇒ SystemExit."""
    if not ten_day_du.startswith("projects/") or "/versions/" not in ten_day_du:
        raise SystemExit("⛔ tên phiên bản lạ")
    try:
        _post(f"{sm}/v1/{ten_day_du}:destroy", _token(metadata), {})
    except (urllib.error.URLError, ValueError) as e:
        raise SystemExit(f"⛔ không huỷ được phiên bản cũ: {type(e).__name__}")


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
