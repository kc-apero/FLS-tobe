"""Bài thử bước 08 — `tools/staging/08_dat_dang_nhap.sh` (WO-363 bổ sung 24/11: tài khoản đăng nhập chung sau IAP).

gcloud GIẢ có trạng thái (`gcloud_gia.py`, nhánh `secrets`). Mật khẩu vào script bằng STDIN (như `read -s` từ bàn
phím). Canh: chỉ BẢN GHI BĂM lên "Secret Manager" · mật khẩu ⛔ trong argv của BẤT KỲ lệnh gcloud nào, ⛔ trong
đầu ra · gõ lại khác / ngắn ⇒ exit 2 và ⛔ lệnh GHI nào · chạy lại = phiên bản mới · `--kiem` chỉ đọc.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

import pytest

from tests.staging import ho_tro as H
from tests.staging.test_07_link_web import Gcp, SA_APP

sys.path.insert(0, str(H.STG / "app"))
import dang_nhap as DN  # noqa: E402

S08 = H.STG / "08_dat_dang_nhap.sh"
MK = "mat-khau-THU-buoc-08-c41d"
GHI = ("services enable", "secrets create", "secrets versions add", "secrets add-iam-policy-binding")


def _chay(g, *args, nhap=f"{MK}\n{MK}\n"):
    env = dict(os.environ, PATH=f"{g.dir}{os.pathsep}{os.environ['PATH']}", FLS_GIA_TRANG_THAI=str(g.tt), PYTHONUTF8="1")
    return subprocess.run(["bash", str(S08), "--project", "du-an-gia", *args], input=nhap,
                          capture_output=True, text=True, env=env, timeout=120)


@pytest.fixture
def g(tmp_path):
    return Gcp(tmp_path, secrets={})


def _ghi(g):
    return [l for l in g.lenh() if l.startswith(GHI)]


def test_dat_lan_dau_DAT_chi_BAN_GHI_BAM_len_bi_mat_va_SA_doc_duoc(g):
    r = _chay(g)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-1000:]
    assert "KẾT: ĐẠT" in r.stdout and len(H.dong_bao_cao(r.stdout)) == 4
    bm = g.doc()["secrets"]["fls-staging-login"]
    rec = json.loads(bm["versions"][-1])
    assert rec["ten"] == "HondurasGesha" and DN.khop(MK, rec["bam"]) and MK not in bm["versions"][-1]
    assert bm["iam"] == [{"role": "roles/secretmanager.secretAccessor", "members": [SA_APP]}]
    assert MK not in r.stdout + r.stderr, "mật khẩu ⛔ in"
    assert MK not in g.log.read_text(encoding="utf-8"), "mật khẩu ⛔ trong argv của gcloud"
    assert rec["bam"] not in r.stdout + r.stderr, "băm ⛔ in"
    la = [l for l in g.lenh() if l.startswith(("run ", "iap ", "compute", "sql", "projects add"))]
    assert not la, f"⛔ đụng gì ngoài bí mật đăng nhập: {la}"


def test_chay_lai_them_PHIEN_BAN_moi_va_mat_khau_moi_khop(g):
    assert _chay(g).returncode == 0
    moi = "mat-khau-MOI-sau-doi-9b2e"
    r = _chay(g, nhap=f"{moi}\n{moi}\n")
    assert r.returncode == 0, r.stdout[-1500:]
    v = g.doc()["secrets"]["fls-staging-login"]["versions"]
    assert len(v) == 2 and DN.khop(moi, json.loads(v[-1])["bam"]) and not DN.khop(MK, json.loads(v[-1])["bam"])
    assert not [l for l in g.lenh() if "destroy" in l or "delete" in l], "⛔ xoá phiên bản cũ"


@pytest.mark.parametrize("nhap,loi", [
    (f"{MK}\n{MK}x\n", "KHÁC nhau"),
    ("ngan\nngan\n", "ngắn hơn"),
    ("HondurasGesha\nHondurasGesha\n", "trùng tên"),
    ("\n\n", "ngắn hơn"),
])
def test_go_lai_khac_hay_mat_khau_yeu_exit_2_va_KHONG_ghi_gi(g, nhap, loi):
    r = _chay(g, nhap=nhap)
    assert r.returncode == 2 and loi in r.stderr, r.stderr
    assert _ghi(g) == []
    assert MK not in r.stdout + r.stderr


def test_mat_khau_trung_ten_tu_choi(g):
    r = _chay(g, "--ten", "TenRatDaiDuMuoiHai", nhap="TenRatDaiDuMuoiHai\nTenRatDaiDuMuoiHai\n")
    assert r.returncode == 2 and "trùng tên" in r.stderr and _ghi(g) == []


def test_kiem_chi_doc__truoc_khi_dat_DO_co_ten__sau_DAT(g):
    r = _chay(g, "--kiem", nhap="")
    assert r.returncode == 1 and _ghi(g) == []
    assert H.muc_do(r.stdout) == {"bí mật đăng nhập có", "SA fls-staging-app đọc được bí mật đăng nhập",
                                  "bản ghi mới nhất: tên đăng nhập = mong", "bản ghi mới nhất: băm scrypt (⛔ mật khẩu thô)"}
    _chay(g)
    n = len(_ghi(g))
    r2 = _chay(g, "--kiem", nhap="")
    assert r2.returncode == 0 and len(_ghi(g)) == n


def test_ban_ghi_THO_khong_bam_thi_DO(g):
    _chay(g)
    g.sua(lambda s: s["secrets"]["fls-staging-login"]["versions"].append('{"ten": "HondurasGesha", "bam": "matkhauthothuong"}'))
    r = _chay(g, "--kiem", nhap="")
    assert r.returncode == 1 and H.muc_do(r.stdout) == {"bản ghi mới nhất: băm scrypt (⛔ mật khẩu thô)"}


@pytest.mark.parametrize("args,loi", [(["--ten", "co dau cach"], "--ten"), (["--bi-mat", "Hoa_Thuong"], "--bi-mat"),
                                      (["--mat-khau", "x"], "tham số lạ")])
def test_tham_so_xau_exit_2_va_khong_goi_gcloud(g, args, loi):
    r = _chay(g, *args)
    assert r.returncode == 2 and loi in r.stderr and g.lenh() == []


def test_tinh_script_doc_mat_khau_bang_read_s_va_khong_echo():
    s = H.STG.joinpath("08_dat_dang_nhap.sh").read_text(encoding="utf-8")
    ma = "\n".join(l for l in s.splitlines() if not l.lstrip().startswith("#"))
    assert len(re.findall(r"read -rs ", ma)) == 2
    assert not re.search(r'echo[^\n]*\$MK\b', ma) and not re.search(r'echo[^\n]*\$BAN_GHI', ma)
    assert "set -x" not in ma and "bash -x" not in ma
