# -*- coding: utf-8 -*-
"""`WO-359` AC-3 — `tools/staging/06_vertex_agent.sh` vs một project GCP GIẢ có trạng thái (`vertex_gia.py`).

Đo: dựng từ trống ⇒ chỉ còn ĐỎ ở Model Garden (bước bấm tay) · sau khi "bấm" ⇒ ĐẠT · chạy lại được (⛔ nhân đôi IAM) ·
`--kiem` ⛔ lệnh GHI · ĐỎ HAI CHIỀU (mỗi thứ phá ⇒ ĐÚNG mục ĐỎ) · ⛔ token/nội dung trả lời trong đầu ra ·
lệnh trong VM chạy THẬT bằng bash (gcloud giả chạy `--command`) ⇒ chuỗi lệnh gửi vào VM được đo, ⛔ chỉ được tin.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
S06 = GOC / "tools" / "staging" / "06_vertex_agent.sh"
GIA = Path(__file__).with_name("vertex_gia.py")
DU_AN = "fp-a-project"
SA = f"fls-staging-app@{DU_AN}.iam.gserviceaccount.com"
CP = "https://www.googleapis.com/auth/cloud-platform"
LINH_CANH = ("TOKGIA-nguoi", "TOKGIA-sa", "NOIDUNG-GIA", "chi tiet GIA")
CAM_GHI = re.compile(r"\b(delete|remove|disable|destroy|set-iam-policy|remove-iam-policy-binding|keys create)\b")
GHI = re.compile(r"^gcloud (services enable|projects add-iam-policy-binding)")


class Gcp:
    def __init__(self, d: Path):
        self.d, self.tt = d, d / "tt.json"
        for ten in ("gcloud", "curl"):
            shutil.copy(GIA, d / ten)
            (d / ten).chmod(0o755)
        self.dat({"project": DU_AN, "sa": SA, "apis": [], "iam": [], "model_garden": [],
                  "vm": {"sa": SA, "scopes": [CP]}})

    def doc(self):
        return json.loads(self.tt.read_text(encoding="utf-8"))

    def dat(self, s):
        self.tt.write_text(json.dumps(s), encoding="utf-8")

    def sua(self, f):
        s = self.doc()
        f(s)
        self.dat(s)

    def lenh(self):
        p = Path(str(self.tt) + ".log")
        return [re.sub(r" --project=\S+ --quiet", "", x) for x in p.read_text(encoding="utf-8").splitlines()] if p.exists() else []

    def chay(self, *a, du_an=DU_AN):
        env = dict(os.environ, PATH=f"{self.d}{os.pathsep}{os.environ['PATH']}", FLS_GIA_TRANG_THAI=str(self.tt))
        env.pop("FLS_GIA_DANH_TINH", None)
        return subprocess.run(["bash", str(S06), "--project", du_an, *a], capture_output=True, text=True, env=env,
                              timeout=120)


def muc(out: str) -> dict[str, str]:
    """Dòng BÁO CÁO `[ĐẠT|ĐỎ] <tên>  …` ⇒ {tên: ĐẠT|ĐỎ}."""
    return {m.group(2).strip(): m.group(1) for m in re.finditer(r"\[(ĐẠT|ĐỎ)\] (.+?)\s{2,}", out)}


def do_cua(out: str) -> set[str]:
    return {k for k, v in muc(out).items() if v == "ĐỎ"}


@pytest.fixture
def g(tmp_path):
    return Gcp(tmp_path)


def _bat_mg(s):
    s["model_garden"] = ["claude-opus-5-5", "claude-sonnet-5-5"]


def test_dung_tu_trong__chi_DO_o_Model_Garden_roi_DAT_sau_khi_bam(g):
    r = g.chay()
    assert r.returncode == 1, r.stdout + r.stderr
    do = do_cua(r.stdout)
    # mong: CHỈ mục gọi thử ĐỎ (Model Garden chưa bật = bước bấm tay) — 2 danh tính × 2 mô hình × (HTTP + mô hình)
    assert do and all("· HTTP" in k or "mô hình trả về" in k for k in do), do
    assert len(do) == 8, do
    assert "FAILED_PRECONDITION" in r.stdout                      # trạng thái Google được BÁO (⛔ nội dung)
    assert "model-garden/claude-opus-5-5?project=fp-a-project" in r.stdout
    g.sua(_bat_mg)                                                # chủ "bấm Enable"
    r2 = g.chay("--kiem")
    assert r2.returncode == 0, r2.stdout + r2.stderr
    # 13 mục có mong = AC-5 · API · IAM · VM-SA · VM-phạm-vi (5) + 2 danh tính × 2 mô hình × (HTTP + mô hình) (8)
    assert "KẾT: ĐẠT" in r2.stdout and len(muc(r2.stdout)) == 13 and not do_cua(r2.stdout)
    assert "18/5 · end_turn" in r2.stdout                         # số token đọc được (⛔ nội dung)


def test_kiem__KHONG_lenh_ghi_va_chay_lai_KHONG_nhan_doi(g):
    g.sua(_bat_mg)
    r = g.chay("--kiem")
    assert r.returncode == 1                                       # API chưa bật, IAM chưa cấp ⇒ ĐỎ
    assert not [x for x in g.lenh() if GHI.match(x)]
    assert {"API aiplatform.googleapis.com bật", "SA có roles/aiplatform.user ở project (⛔ điều kiện)"} <= do_cua(r.stdout)
    g.chay()
    g.chay()
    iam = g.doc()["iam"]
    assert iam == [{"role": "roles/aiplatform.user", "members": [f"serviceAccount:{SA}"]}]
    assert not [x for x in g.lenh() if CAM_GHI.search(x)]


def test_KHONG_in_token_noi_dung_tra_loi(g):
    g.sua(_bat_mg)
    r = g.chay()
    assert r.returncode == 0, r.stdout
    for lc in LINH_CANH:
        assert lc not in r.stdout + r.stderr, lc
    # lời gọi thật có mang token (⇒ lính canh ⛔ vắng vì ⛔ dùng tới)
    assert any(x.startswith("curl ") and ":rawPredict" in x for x in g.lenh())


@pytest.mark.parametrize("pha,mong_do", [
    (lambda s: s["model_garden"].remove("claude-sonnet-5-5"),
     {"Cloud Shell · người chạy · claude-sonnet-5-5 · HTTP", "TRONG VM · SA · claude-sonnet-5-5 · HTTP"}),
    (lambda s: s.update(vm={"sa": SA, "scopes": ["https://www.googleapis.com/auth/devstorage.read_only"]}),
     {"VM phạm vi OAuth có cloud-platform", "TRONG VM · SA · claude-opus-5-5 · HTTP", "TRONG VM · SA · claude-sonnet-5-5 · HTTP"}),
    (lambda s: s.update(vm=None),
     {"VM tồn tại · chạy bằng SA", "VM phạm vi OAuth có cloud-platform",
      "TRONG VM · SA · claude-opus-5-5 · HTTP", "TRONG VM · SA · claude-sonnet-5-5 · HTTP"}),
    (lambda s: s.update(phuc_vu={"claude-opus-5-5": "claude-opus-5"}),
     {"Cloud Shell · người chạy · claude-opus-5-5 · mô hình trả về (= mã ghim)",
      "TRONG VM · SA · claude-opus-5-5 · mô hình trả về (= mã ghim)"}),
    (lambda s: s.update(dang_nhap=False),
     {"Cloud Shell · người chạy · claude-opus-5-5 · HTTP", "Cloud Shell · người chạy · claude-sonnet-5-5 · HTTP"}),
    (lambda s: s.update(ssh_duoc=False),
     {"TRONG VM · SA · claude-opus-5-5 · HTTP", "TRONG VM · SA · claude-sonnet-5-5 · HTTP"}),
])
def test_DO_hai_chieu__pha_tung_thu__DUNG_muc_DO(g, pha, mong_do):
    g.sua(_bat_mg)
    assert g.chay().returncode == 0                                # nền ĐẠT
    g.sua(pha)
    r = g.chay("--kiem")
    assert r.returncode == 1
    do = {k for k in do_cua(r.stdout) if "mô hình trả về" not in k or "mô hình trả về" in " ".join(mong_do)}
    assert mong_do <= do_cua(r.stdout) and do == mong_do, (do, mong_do)


def test_IAM_SA_bi_go__DO_ca_muc_IAM_lan_goi_trong_VM(g):
    g.sua(_bat_mg)
    g.chay()
    g.sua(lambda s: s.update(iam=[]))
    r = g.chay("--kiem")
    do = do_cua(r.stdout)
    assert "SA có roles/aiplatform.user ở project (⛔ điều kiện)" in do
    assert {"TRONG VM · SA · claude-opus-5-5 · HTTP", "TRONG VM · SA · claude-sonnet-5-5 · HTTP"} <= do
    assert "PERMISSION_DENIED" in r.stdout
    assert not any(k.startswith("Cloud Shell") for k in do)        # người chạy (chủ) vẫn gọi được — đúng hai danh tính


def test_khong_goi_thu__muc_goi_thu_la_DO_khong_phai_bo_qua(g):
    g.sua(_bat_mg)
    g.chay()
    truoc = len(g.lenh())
    r = g.chay("--kiem", "--khong-goi-thu")
    assert r.returncode == 1 and len(do_cua(r.stdout)) == 8        # Đ5: ⛔ đo được ⇒ ĐỎ
    moi = g.lenh()[truoc:]
    assert len(moi) == 3 and not any(x.startswith("curl ") or " ssh " in x for x in moi), moi   # 3 lệnh ĐỌC, ⛔ gọi


@pytest.mark.parametrize("vung", ["us", "eu"])
def test_vung_da_vung__dung_host_rep(g, vung):
    g.sua(_bat_mg)
    r = g.chay("--region", vung)
    assert r.returncode == 0, r.stdout
    assert f"aiplatform.{vung}.rep.googleapis.com/v1/projects/{DU_AN}/locations/{vung}/" in "\n".join(g.lenh())


@pytest.mark.parametrize("a", [["--region", "asia-southeast1"], ["--region", "us-east5"], ["--vm", "X;rm"], ["--la"]])
def test_tham_so_xau__exit_2_truoc_moi_lenh(g, a):
    r = g.chay(*a)
    assert r.returncode == 2 and not g.lenh()


def test_project_khac_cong_ty__DO_muc_AC5(g):
    g.sua(lambda s: s.update(project="du-an-khac"))
    g.sua(_bat_mg)
    r = g.chay(du_an="du-an-khac")
    assert "project = GCP công ty (fp-a-project — AC-5)" in do_cua(r.stdout)
