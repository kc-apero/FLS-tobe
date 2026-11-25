"""`STG-WEB-R1-03` — binding IAM MỨC DỰ ÁN phải nói `--condition=None` (lỗi THẬT 24/11: `fp-a-project` có 2 binding điều kiện;
gcloud ⛔ tương tác từ chối thêm binding không điều kiện vào chính sách có điều kiện).

Hai lớp canh: ⓐ TĨNH — đếm mọi lệnh `projects add-iam-policy-binding` trong `tools/staging/*.sh` (gộp dòng `\\`), số có
`--condition=None` = tổng; ⓑ ĐỘNG — đồ giả `gcloud_gia.py` mặc định mô phỏng chính sách CÓ điều kiện và cắn đúng lời GCP
(bài `test_03`/`test_01` chạy script trên đó; đột biến bỏ cờ ở 03 ⇒ 1 ĐỎ · ở 01 ⇒ 4 ĐỎ — `BG-364` §12).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess

from tests.staging import ho_tro as H

GIA = H.GOC / "tests" / "staging" / "gcloud_gia.py"


def _lenh_projects_binding():
    ra = []
    for p in sorted(H.STG.glob("*.sh")):
        van = re.sub(r"\\\n\s*", " ", p.read_text(encoding="utf-8"))          # gộp dòng tiếp nối
        for dong in van.splitlines():
            if dong.lstrip().startswith("#"):
                continue
            if re.search(r"\bprojects\s+(add|remove)-iam-policy-binding\b", dong):
                ra.append((p.name, dong.strip()))
    return ra


def test_tinh_MOI_binding_muc_du_an_co_condition_None():
    ds = _lenh_projects_binding()
    assert len(ds) >= 2, f"tập rỗng ⇒ bài vô nghĩa (Đ3): {ds}"                 # 01 (cloudsql.client) + 03 (tunnelResourceAccessor)
    thieu = [(t, d[:120]) for t, d in ds if "--condition=None" not in d]
    assert not thieu, f"binding mức dự án THIẾU --condition=None: {thieu}"
    assert {t for t, _ in ds} <= {"01_dung_staging_gcp.sh", "03_dung_app.sh"}, \
        f"binding mức dự án ở script mới — 07/08 cố ý ⛔ có (quyền theo tài nguyên): {ds}"


def test_gia_CO_dieu_kien_cat_dung_loi_GCP_va_cho_qua_khi_co_co(tmp_path):
    shutil.copy(GIA, tmp_path / "gcloud")
    (tmp_path / "gcloud").chmod(0o755)
    tt = tmp_path / "tt.json"
    tt.write_text(json.dumps({"quyen": []}))
    env = dict(os.environ, FLS_GIA_TRANG_THAI=str(tt))
    goi = [str(tmp_path / "gcloud"), "projects", "add-iam-policy-binding", "p", "--member=user:a@b.c", "--role=roles/x"]
    r = subprocess.run(goi, capture_output=True, text=True, env=env)
    assert r.returncode == 1 and "policy containing conditions" in r.stderr and "--condition=None" in r.stderr
    r2 = subprocess.run(goi + ["--condition=None"], capture_output=True, text=True, env=env)
    assert r2.returncode == 0 and json.loads(tt.read_text())["quyen"][0]["role"] == "roles/x"
