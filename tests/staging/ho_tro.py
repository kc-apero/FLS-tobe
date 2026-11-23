"""Đồ nghề CHUNG cho bài thử script staging (`tools/staging/*.sh`).

⭐ Vì sao có tệp này. Các script staging chạy ở Cloud Shell của chủ, ⛔ Claude vào GCP. Cách duy nhất
để chứng minh chúng đúng (và ĐỎ khi hỏng — luật `Đ5`) là dựng **mọi thứ ngoài GCP bằng đồ thật**:

  · `gcloud`          → GIẢ (một tệp bash chỉ hiểu đúng các lệnh script được phép gọi; lệnh lạ ⇒ exit 99)
  · `cloud-sql-proxy` → GIẢ (ngủ; ghi đối số) — kết nối thật đi thẳng tới cụm PG cục bộ của phiên
  · `psql` · `python -m fls.db.pg_migrate` · `pg_verify` · GRANT/REVOKE → **THẬT** trên một kho
    scratch `fls_stg_<pid>` ⇒ quyền kiểm là quyền PostgreSQL thật, ⛔ một lời nói dối của mock.

⛔ Bài thử ⛔ chạm kho `fls`/`fls_test` của phiên: chỉ tạo/xoá kho scratch + các vai `fls_admin`,
`fls_ghi`, `fls_doc` (+ một vai quản trị `stg_qt_<pid>`) và dọn khi xong.
"""
from __future__ import annotations

import os
import re
import stat
import subprocess
import sys
import urllib.parse
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
STG = GOC / "tools" / "staging"

MK = {   # mật khẩu GIẢ của "Secret Manager" — chuỗi dễ nhận để bài thử quét rò rỉ
    "fls-staging-pg-postgres": "MKGIA-qt-9f3a1c77d2e04b58",
    "fls-staging-pg-fls_admin": "MKGIA-admin-5b8e21aa90c3d4f1",
    "fls-staging-pg-fls_ghi": "MKGIA-ghi-71c0e6d4b2a8953f",
    "fls-staging-pg-fls_doc": "MKGIA-doc-c4d19e7a3b60f258",
    "fls-staging-jwt-secret": "MKGIA-jwt-0a6f3e8d1c5b9472-e71b4c09d2f85a36",
}


def cong_pg() -> int:
    dsn = os.environ.get("PG_DSN_TEST") or os.environ.get("PG_DSN") or ""
    return urllib.parse.urlparse(dsn).port or 5432


def chay_quan_tri(sql: str, kho: str = "postgres") -> str:
    """Chạy SQL bằng SIÊU QUYỀN của cụm cục bộ (peer `postgres` qua socket). Skip nếu không có."""
    cmd = ["runuser", "-u", "postgres", "--", "psql", "-p", str(cong_pg()), "-d", kho, "-X", "-tA",
           "-v", "ON_ERROR_STOP=1", "-c", sql]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, PermissionError):
        pytest.skip("⛔ không có runuser→postgres để tạo vai (chỉ container cloud)")
    if r.returncode != 0:
        if "could not connect" in r.stderr or "No such file" in r.stderr:
            pytest.skip(f"⛔ không nối được cụm cục bộ bằng peer postgres: {r.stderr.strip()[:120]}")
        raise RuntimeError(f"SQL quản trị đỏ: {r.stderr.strip()}\n  {sql[:200]}")
    return r.stdout.strip()


def _viet_chay_duoc(p: Path, noi_dung: str) -> Path:
    p.write_text(noi_dung, encoding="utf-8")
    p.chmod(p.stat().st_mode | stat.S_IXUSR)
    return p


def dung_gia(thu_muc: Path, *, thieu_bi_mat: str | None = None) -> dict:
    """Dựng thư mục đồ GIẢ: `gcloud` · `cloud-sql-proxy`. Trả đường dẫn + tệp nhật ký."""
    thu_muc.mkdir(parents=True, exist_ok=True)
    nhat_ky = thu_muc / "gcloud.log"
    proxy_log = thu_muc / "proxy.log"
    proxy_pid = thu_muc / "proxy.pid"
    for ten, mk in MK.items():
        if ten != thieu_bi_mat:
            (thu_muc / f"secret_{ten}").write_text(mk, encoding="utf-8")
    _viet_chay_duoc(thu_muc / "gcloud", f"""#!/usr/bin/env bash
# gcloud GIẢ — chỉ hiểu các lệnh ĐỌC mà bước 02/03/04 được phép gọi. Lệnh lạ ⇒ exit 99.
echo "$*" >> "{nhat_ky}"
args="$*"
case "$args" in
  *"secrets versions access latest --secret="*)
      ten="${{args##*--secret=}}"; ten="${{ten%% *}}"
      f="{thu_muc}/secret_$ten"; [ -f "$f" ] && cat "$f" || {{ echo "NOT_FOUND $ten" >&2; exit 1; }} ;;
  *"sql instances describe"*"connectionName"*) echo "du-an-gia:asia-southeast1:fls-staging" ;;
  *) echo "gcloud GIẢ: lệnh lạ hoặc lệnh GHI: $args" >&2; exit 99 ;;
esac
""")
    _viet_chay_duoc(thu_muc / "cloud-sql-proxy", f"""#!/usr/bin/env bash
echo "$*" > "{proxy_log}"; echo $$ > "{proxy_pid}"
exec sleep 600
""")
    return {"dir": thu_muc, "gcloud_log": nhat_ky, "proxy_log": proxy_log, "proxy_pid": proxy_pid,
            "proxy": thu_muc / "cloud-sql-proxy"}


def chay_script(ten: str, gia: dict, kho: str, qt_user: str, *args: str,
                env_them: dict | None = None, thoi_gian: int = 240) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update({
        "PATH": f"{gia['dir']}{os.pathsep}{env['PATH']}",
        "FLS_STG_PYTHON": sys.executable,
        "FLS_STG_QT_USER": qt_user,
        "PYTHONUTF8": "1",
        "HOME": str(gia["dir"]),
    })
    for k in ("PG_DSN", "PG_DSN_TEST", "PGPASSWORD", "FLS_CHO_GHI_THAT"):
        env.pop(k, None)       # ⛔ rò kho thật của phiên vào script
    if env_them:
        env.update(env_them)
    return subprocess.run(
        ["bash", str(STG / ten), "--project", "du-an-gia", "--kho", kho,
         "--cong-proxy", str(cong_pg()), "--proxy", str(gia["proxy"]), *args],
        capture_output=True, text=True, env=env, timeout=thoi_gian)


def dong_bao_cao(out: str) -> dict[str, str]:
    """`{nhãn: 'ĐẠT'|'ĐỎ'}` từ các dòng `[ĐẠT] nhãn …` của BÁO CÁO."""
    kq: dict[str, str] = {}
    for m in re.finditer(r"^\s+\[(ĐẠT|ĐỎ)\] (.+?)\s{2,}", out, re.M):
        kq[m.group(2).strip()] = m.group(1)
    return kq


def muc_do(out: str) -> set[str]:
    return {k for k, v in dong_bao_cao(out).items() if v == "ĐỎ"}
