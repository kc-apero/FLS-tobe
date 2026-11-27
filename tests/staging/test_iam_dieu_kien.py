"""`STG-WEB-R1-03` — binding IAM MỨC DỰ ÁN phải nói `--condition=None` (lỗi THẬT 24/11: `fp-a-project` có 2 binding điều kiện;
gcloud ⛔ tương tác từ chối thêm binding không điều kiện vào chính sách có điều kiện).

Hai lớp canh: ⓐ TĨNH — mọi lệnh `projects add/remove-iam-policy-binding` trong `tools/staging/*.sh` (gộp dòng `\\`) có
`--condition=None`, VÀ chỉ nằm ở script đã KHAI trong `KHAI_BINDING_DU_AN` (MỘT chỗ duy nhất); ⓑ ĐỘNG — đồ giả `gcloud_gia.py`
mặc định mô phỏng chính sách CÓ điều kiện và cắn đúng lời GCP (đột biến bỏ cờ ở 03 ⇒ 1 ĐỎ · ở 01 ⇒ 4 ĐỎ — `BG-364` §12).

⭐ Sửa tích hợp 27/11 (gộp thử STG-WEB × AG3, orchestrator): bản đầu ghim CỨNG tập `{01, 03}` ở câu assert ⇒ `06_vertex_agent.sh`
(AG3, đã có `--condition=None`) làm bài ĐỎ dù ⛔ sai gì. Ý bài là "mọi binding mức dự án có `--condition=None`" + "danh sách
script có binding mức dự án được KHAI ở MỘT chỗ" — nay danh sách là hằng `KHAI_BINDING_DU_AN` (kèm lý do), và bài
`test_script_MOI_co_binding_ma_CHUA_khai_thi_DO` chứng minh thường trực rằng script mới chưa khai vẫn bị cắn.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from tests.staging import ho_tro as H

GIA = H.GOC / "tests" / "staging" / "gcloud_gia.py"

# ⭐ MỘT chỗ khai: script nào được phép cấp quyền MỨC DỰ ÁN, và vì sao. Thêm script mới ⇒ thêm dòng ở đây (kèm lý do).
#   07/08 cố ý ⛔ có: quyền theo TÀI NGUYÊN (service Cloud Run · IAP · bí mật).
KHAI_BINDING_DU_AN = {
    "01_dung_staging_gcp.sh": "SA fls-staging-app: roles/cloudsql.client (Cloud SQL ⛔ có IAM theo instance)",
    "03_dung_app.sh": "người test (--cap-quyen): roles/iap.tunnelResourceAccessor cho đường hầm SSH",
    "06_vertex_agent.sh": "AG3 · WO-359 (KQ-361/362): SA + người chạy roles/aiplatform.user hoặc roles/claude.user mức project",
}


def lenh_binding_du_an(thu_muc: Path) -> list[tuple[str, str]]:
    ra = []
    for p in sorted(thu_muc.glob("*.sh")):
        van = re.sub(r"\\\n\s*", " ", p.read_text(encoding="utf-8"))          # gộp dòng tiếp nối
        for dong in van.splitlines():
            if dong.lstrip().startswith("#"):
                continue
            if re.search(r"\bprojects\s+(add|remove)-iam-policy-binding\b", dong):
                ra.append((p.name, dong.strip()))
    return ra


def vi_pham(thu_muc: Path) -> tuple[list, list]:
    """(binding THIẾU `--condition=None`, script có binding mà CHƯA khai)."""
    ds = lenh_binding_du_an(thu_muc)
    thieu = [(t, d[:120]) for t, d in ds if "--condition=None" not in d]
    chua_khai = sorted({t for t, _ in ds} - set(KHAI_BINDING_DU_AN))
    return thieu, chua_khai


def test_tinh_MOI_binding_muc_du_an_co_condition_None_va_DA_KHAI():
    ds = lenh_binding_du_an(H.STG)
    assert len(ds) >= 2, f"tập rỗng ⇒ bài vô nghĩa (Đ3): {ds}"
    thieu, chua_khai = vi_pham(H.STG)
    assert not thieu, f"binding mức dự án THIẾU --condition=None: {thieu}"
    assert not chua_khai, f"script có binding mức dự án mà CHƯA khai ở KHAI_BINDING_DU_AN: {chua_khai}"
    thua = sorted(set(KHAI_BINDING_DU_AN) - {t for t, _ in ds})
    assert not thua, f"khai mà script ⛔ (còn) có binding mức dự án — xoá dòng khai: {thua}"


def test_script_MOI_co_binding_ma_CHUA_khai_thi_DO(tmp_path):
    """Chứng minh ĐỎ thường trực (Đ5): chép `tools/staging/*.sh` + thêm MỘT script mới có binding ⇒ phép kiểm cắn."""
    for p in H.STG.glob("*.sh"):
        shutil.copy(p, tmp_path / p.name)
    assert vi_pham(tmp_path) == ([], []), "nền phải sạch trước khi phá"
    (tmp_path / "99_moi.sh").write_text('gcloud projects add-iam-policy-binding "$P" \\\n    --member=user:a@b.c --role=roles/x --condition=None\n')
    assert vi_pham(tmp_path) == ([], ["99_moi.sh"]), "script mới CHƯA khai phải bị cắn"
    (tmp_path / "99_moi.sh").write_text('gcloud projects add-iam-policy-binding "$P" --member=user:a@b.c --role=roles/x\n')
    thieu, chua_khai = vi_pham(tmp_path)
    assert [t for t, _ in thieu] == ["99_moi.sh"] and chua_khai == ["99_moi.sh"], "thiếu cờ cũng phải bị cắn"


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
