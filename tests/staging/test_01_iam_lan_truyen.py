"""Bước 01 — lỗi THẬT 23/11: IAM lan truyền trễ ở ⑥ (`projects add-iam-policy-binding` báo SA "does not exist" ngay sau khi tạo).

gcloud GIẢ: lệnh `projects add-iam-policy-binding` thất bại N lần rồi thành công (hoặc mãi mãi). Mong: N=2 ⇒ ĐẠT mục
"SA có cloudsql.client"; thất bại mãi ⇒ lỗi CÓ TÊN `IAM_KHONG_LAN_TRUYEN` + VẪN in BÁO CÁO (mục ấy ĐỎ), ⛔ chết im.
"""
from __future__ import annotations

import os
import re
import stat
import subprocess

import pytest

from tests.staging import ho_tro as H

SA = "fls-staging-app@du-an-gia.iam.gserviceaccount.com"


def _gcloud(thu_muc, hong_n, *, sa_co_san=(), go_hong=False, them_bm_hong=False, doc_chinh_sach_hong=False):
    """`sa_co_san`: bí mật mà SA ĐÃ có secretAccessor (mô phỏng bản chạy THẬT 23/11 đã gán cả 5).
    `go_hong`: `secrets remove-iam-policy-binding` PERMISSION_DENIED · `them_bm_hong`: `secrets add-iam-policy-binding` PERMISSION_DENIED ·
    `doc_chinh_sach_hong`: `secrets get-iam-policy` lỗi (⛔ đo được)."""
    d = thu_muc / "bin"
    d.mkdir()
    acc = thu_muc / "acc"
    acc.mkdir()
    for b in sa_co_san:
        (acc / b).touch()
    ten = lambda: 'for a in "$@"; do case "$a" in fls-staging-*) echo "$a";; esac; done | head -1'  # noqa: E731
    them_bm = 'echo "ERROR: (gcloud.secrets.add-iam-policy-binding) PERMISSION_DENIED: cấm" >&2; exit 1' if them_bm_hong else ":"
    go = 'echo "ERROR: (gcloud.secrets.remove-iam-policy-binding) PERMISSION_DENIED: cấm gỡ" >&2; exit 1' if go_hong else ":"
    doc = "echo 'ERROR: 500' >&2; exit 1" if doc_chinh_sach_hong else ":"
    cnt = thu_muc / "dem"
    cnt.write_text("0")
    g = d / "gcloud"
    g.write_text(f"""#!/usr/bin/env bash
echo "$*" >> "{thu_muc}/log"
case "$*" in
  *"projects add-iam-policy-binding"*)
      # `STG-WEB-R1-03`: chính sách dự án CÓ điều kiện (đo THẬT 24/11) ⇒ thiếu `--condition` ⇒ gcloud từ chối, ⛔ tính là lần thử
      case "$*" in *"--condition"*) ;; *) echo "ERROR: (gcloud.projects.add-iam-policy-binding) Adding a binding without specifying a condition to a policy containing conditions is prohibited in non-interactive mode. Run the command again with --condition=None" >&2; exit 1 ;; esac
      n=$(cat "{cnt}"); echo $((n+1)) > "{cnt}"
      if [ "$n" -lt {hong_n} ]; then echo "ERROR: INVALID_ARGUMENT: Service account {SA} does not exist." >&2; exit 1; fi
      touch "{thu_muc}/da_gan"; exit 0 ;;
  *"projects get-iam-policy"*) [ -f "{thu_muc}/da_gan" ] && echo roles/cloudsql.client; exit 0 ;;
  *"secrets add-iam-policy-binding"*)
      {them_bm}
      b=$({ten()}); touch "{acc}/$b"; exit 0 ;;
  *"secrets remove-iam-policy-binding"*)
      {go}
      b=$({ten()}); rm -f "{acc}/$b"; exit 0 ;;
  *"secrets get-iam-policy"*)
      {doc}
      b=$({ten()}); [ -f "{acc}/$b" ] && echo "serviceAccount:{SA}"; exit 0 ;;
  *"secrets describe"*|*"sql instances describe"*) exit 1 ;;   # chưa có ⇒ script tạo
  *"secrets versions access"*) echo bimatgia; exit 0 ;;
  *"sql users list"*) exit 0 ;;
  *) exit 0 ;;
esac
""")
    g.chmod(g.stat().st_mode | stat.S_IXUSR)
    return d, cnt


def _chay(tmp_path, hong_n, **kw):
    d, cnt = _gcloud(tmp_path, hong_n, **kw)
    env = dict(os.environ, PATH=f"{d}{os.pathsep}{os.environ['PATH']}", FLS_STG_CHO_GIAY="0", FLS_STG_THU_LAI="5")
    r = subprocess.run(["bash", str(H.STG / "01_dung_staging_gcp.sh"), "--project", "du-an-gia"],
                       capture_output=True, text=True, env=env, timeout=120)
    return r, int(cnt.read_text())


def test_binding_that_bai_2_lan_roi_thanh_cong_thi_muc_SA_DAT(tmp_path):
    r, so_lan = _chay(tmp_path, 2)
    assert so_lan == 3, f"mong 3 lần gọi binding cloudsql.client (2 hỏng + 1 được), thấy {so_lan}"
    assert "IAM_KHONG_LAN_TRUYEN" not in r.stderr
    assert re.search(r"\[ĐẠT\] SA có cloudsql\.client", r.stdout), r.stdout[-800:]
    assert "cloudsql.client + secretAccessor trên 3 bí mật app (0 bí mật quản trị)" in r.stdout


def test_binding_that_bai_mai_thi_loi_CO_TEN_va_van_in_BAO_CAO_do(tmp_path):
    r, so_lan = _chay(tmp_path, 10**6)
    assert so_lan == 5, f"hết hạn thử lại: mong đúng 5 lần, thấy {so_lan}"
    assert "IAM_KHONG_LAN_TRUYEN" in r.stderr and "cloudsql.client" in r.stderr
    assert "BÁO CÁO" in r.stdout, "chết im — ⛔ in BÁO CÁO"
    assert re.search(r"\[ĐỎ\] SA có cloudsql\.client", r.stdout)
    assert r.returncode == 1 and "KẾT: ĐỎ" in r.stdout


def test_binding_thanh_cong_ngay_khong_cho_gi(tmp_path):
    r, so_lan = _chay(tmp_path, 0)
    assert so_lan == 1 and "chưa được" not in r.stdout


# ══ `STG-R1-01` — SA ⛔ được đọc bí mật quản trị (`postgres`, `fls_admin`); bước 01 đã CHẠY THẬT 23/11 nên binding thừa ĐANG TỒN TẠI ══
APP = ["fls-staging-jwt-secret", "fls-staging-pg-fls_doc", "fls-staging-pg-fls_ghi"]
QUAN_TRI = ["fls-staging-pg-fls_admin", "fls-staging-pg-postgres"]


def _acc(tmp_path):
    return sorted(p.name for p in (tmp_path / "acc").iterdir())


def _log(tmp_path):
    return (tmp_path / "log").read_text(encoding="utf-8").splitlines()


def test_SA_chi_duoc_gan_dung_3_bi_mat_app_va_KHONG_bao_gio_goi_gan_cho_postgres_fls_admin(tmp_path):
    r, _ = _chay(tmp_path, 0)
    assert _acc(tmp_path) == APP, _acc(tmp_path)          # mẫu số: đúng 3 bí mật app, ≠ 0
    gan = [d for d in _log(tmp_path) if "secrets add-iam-policy-binding" in d]
    assert len(gan) == 3, gan
    assert not [d for d in gan if any(q in d for q in QUAN_TRI)], gan
    # trạng thái SAU khi chủ đã gỡ tay (23/11): SA không có binding thừa ⇒ chạy lại KHÔNG gỡ, KHÔNG lỗi `GO_QUYEN_THUA_LOI`
    assert not [d for d in _log(tmp_path) if "secrets remove-iam-policy-binding" in d], "gỡ khi không có gì để gỡ"
    assert "GO_QUYEN_THUA_LOI" not in r.stderr, r.stderr
    assert re.search(r"\[ĐẠT\] SA đọc đúng bí mật app \(đếm/mẫu số\)\s+'3/3'", r.stdout), r.stdout[-1500:]
    assert re.search(r"\[ĐẠT\] SA đọc 0 bí mật quản trị \(đếm/mẫu số\)\s+'0/2'", r.stdout), r.stdout[-1500:]


def test_binding_THUA_cua_ban_chay_cu_bi_GO_va_chay_lai_khong_go_nua(tmp_path):
    """Trạng thái THẬT 23/11: SA đã có secretAccessor trên cả 5. Chạy lại ⇒ gỡ đúng 2 quyền quản trị; lần 2 ⇒ 0 lệnh gỡ."""
    d, _ = _gcloud(tmp_path, 0, sa_co_san=APP + QUAN_TRI)
    env = dict(os.environ, PATH=f"{d}{os.pathsep}{os.environ['PATH']}", FLS_STG_CHO_GIAY="0", FLS_STG_THU_LAI="2")
    cmd = ["bash", str(H.STG / "01_dung_staging_gcp.sh"), "--project", "du-an-gia"]
    r1 = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    go1 = [x for x in _log(tmp_path) if "secrets remove-iam-policy-binding" in x]
    assert len(go1) == 2 and all(q in " ".join(go1) for q in QUAN_TRI), go1
    assert _acc(tmp_path) == APP
    assert re.search(r"\[ĐẠT\] SA đọc 0 bí mật quản trị .*'0/2'", r1.stdout), r1.stdout[-1500:]
    subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    go2 = [x for x in _log(tmp_path) if "secrets remove-iam-policy-binding" in x]
    assert len(go2) == 2, f"chạy lần 2 phải KHÔNG gỡ thêm (idempotent), thấy {len(go2)}"


def test_khong_go_duoc_binding_thua_thi_ĐỎ_exit1_va_in_chu_gcloud_that(tmp_path):
    r, _ = _chay(tmp_path, 0, sa_co_san=APP + QUAN_TRI, go_hong=True)
    assert re.search(r"\[ĐỎ\] SA đọc 0 bí mật quản trị .*'2/2'.*\(mong '0/2'\)", r.stdout), r.stdout[-1500:]
    assert "GO_QUYEN_THUA_LOI" in r.stderr and "PERMISSION_DENIED" in r.stderr, r.stderr
    assert re.search(r"\[ĐỎ\] gán/gỡ vai đủ", r.stdout) and r.returncode == 1 and "KẾT: ĐỎ" in r.stdout


def test_chinh_sach_IAM_khong_doc_duoc_thi_ĐỎ_khong_phai_sach(tmp_path):
    """Đ5: phép ⛔ đo được là ĐỎ — `get-iam-policy` lỗi ⇒ ⛔ coi là "SA không đọc được gì"."""
    r, _ = _chay(tmp_path, 0, doc_chinh_sach_hong=True)
    assert re.search(r"\[ĐỎ\] SA đọc 0 bí mật quản trị .*'2/2'", r.stdout), r.stdout[-1500:]
    assert re.search(r"\[ĐỎ\] SA đọc đúng bí mật app .*'0/3'", r.stdout), r.stdout[-1500:]


# ══ `STG-R1-04` — `secretAccessor` hỏng 5/5 ⇒ KẾT ĐỎ + chữ gcloud thật (trước đây ĐẠT · exit 0 · nhãn "IAM lan truyền") ══
def test_secretAccessor_PERMISSION_DENIED_ra_ĐỎ_va_hien_chu_that(tmp_path):
    r, _ = _chay(tmp_path, 0, them_bm_hong=True)
    assert r.stderr.count("IAM_KHONG_LAN_TRUYEN") == 3 and "PERMISSION_DENIED" in r.stderr, r.stderr
    assert re.search(r"\[ĐỎ\] gán/gỡ vai đủ", r.stdout), r.stdout[-1500:]
    assert re.search(r"\[ĐỎ\] SA đọc đúng bí mật app .*'0/3'", r.stdout)
    assert r.returncode == 1 and "KẾT: ĐỎ" in r.stdout
    assert "sẽ ĐỎ" not in r.stdout or "gán/gỡ vai đủ" in r.stdout        # câu in ra phải đúng với báo cáo bên dưới


# ══ `STG-R2b-02` — bước 01 ⛔ còn tạo vai ứng dụng bằng gcloud (gcloud gắn CREATEROLE/CREATEDB mà `postgres` ⛔ hạ được) ══

def test_buoc01_KHONG_tao_hay_dat_mat_khau_vai_app_bang_gcloud_nhung_van_sinh_bi_mat(tmp_path):
    r, _ = _chay(tmp_path, 0)
    nk = _log(tmp_path)
    users = [d for d in nk if re.search(r"\bsql users (create|set-password)\b", d)]
    assert [d for d in users if re.search(r"\bfls_(ghi|doc)\b", d)] == [], users
    assert [re.search(r"sql users create (\S+)", d).group(1) for d in users if "users create" in d] == ["fls_admin"], users
    tao_bm = sorted(re.search(r"secrets create (\S+)", d).group(1) for d in nk if "secrets create" in d)
    assert tao_bm == sorted(APP + QUAN_TRI), tao_bm          # bí mật vai app VẪN sinh ở bước 01 (bước 02 đọc nó)
    assert "vai tạo ở BƯỚC 02 bằng SQL" in r.stdout
    assert "đủ tài khoản gcloud (postgres · fls_admin)" in r.stdout
