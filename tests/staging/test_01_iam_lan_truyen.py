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


def _gcloud(thu_muc, hong_n):
    d = thu_muc / "bin"
    d.mkdir()
    cnt = thu_muc / "dem"
    cnt.write_text("0")
    g = d / "gcloud"
    g.write_text(f"""#!/usr/bin/env bash
echo "$*" >> "{thu_muc}/log"
case "$*" in
  *"projects add-iam-policy-binding"*)
      n=$(cat "{cnt}"); echo $((n+1)) > "{cnt}"
      if [ "$n" -lt {hong_n} ]; then echo "ERROR: INVALID_ARGUMENT: Service account {SA} does not exist." >&2; exit 1; fi
      touch "{thu_muc}/da_gan"; exit 0 ;;
  *"projects get-iam-policy"*) [ -f "{thu_muc}/da_gan" ] && echo roles/cloudsql.client; exit 0 ;;
  *"secrets describe"*|*"sql instances describe"*) exit 1 ;;   # chưa có ⇒ script tạo
  *"secrets versions access"*) echo bimatgia; exit 0 ;;
  *"sql users list"*) exit 0 ;;
  *) exit 0 ;;
esac
""")
    g.chmod(g.stat().st_mode | stat.S_IXUSR)
    return d, cnt


def _chay(tmp_path, hong_n):
    d, cnt = _gcloud(tmp_path, hong_n)
    env = dict(os.environ, PATH=f"{d}{os.pathsep}{os.environ['PATH']}", FLS_STG_CHO_GIAY="0", FLS_STG_THU_LAI="5")
    r = subprocess.run(["bash", str(H.STG / "01_dung_staging_gcp.sh"), "--project", "du-an-gia"],
                       capture_output=True, text=True, env=env, timeout=120)
    return r, int(cnt.read_text())


def test_binding_that_bai_2_lan_roi_thanh_cong_thi_muc_SA_DAT(tmp_path):
    r, so_lan = _chay(tmp_path, 2)
    assert so_lan == 3, f"mong 3 lần gọi binding cloudsql.client (2 hỏng + 1 được), thấy {so_lan}"
    assert "IAM_KHONG_LAN_TRUYEN" not in r.stderr
    assert re.search(r"\[ĐẠT\] SA có cloudsql\.client", r.stdout), r.stdout[-800:]
    assert "cloudsql.client + secretAccessor trên 5 bí mật" in r.stdout


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
