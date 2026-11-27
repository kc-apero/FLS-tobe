# -*- coding: utf-8 -*-
"""`WO-367` AC-5 — `tools/staging/09_openrouter_agent.sh` vs gcloud + curl GIẢ có trạng thái (`openrouter_gcp_gia.py`).

Đo: dựng từ trống (khoá vào bằng STDIN, ⛔ argv) ⇒ ĐẠT · chạy lại ⛔ hỏi khoá, ⛔ nhân đôi IAM · `--kiem` ⛔ lệnh GHI ·
binding MỨC BÍ MẬT (⛔ mức project) · ĐỎ HAI CHIỀU (mỗi thứ phá ⇒ ĐÚNG mục ĐỎ, 402/429 in TÊN) · ⛔ khoá/nội dung trong
đầu ra và argv · mỗi lời gọi thử mang `provider` ZDR + deny.
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
S09 = GOC / "tools" / "staging" / "09_openrouter_agent.sh"
GIA = Path(__file__).with_name("openrouter_gcp_gia.py")
DU_AN = "fp-a-project"
SA = f"fls-staging-app@{DU_AN}.iam.gserviceaccount.com"
BM = "fls-staging-openrouter-key"
KHOA = "khoa-GIA-openrouter-0123456789abcdef"
OPUS, SONNET = "anthropic/claude-opus-5.5", "anthropic/claude-sonnet-5.5"
GHI = re.compile(r"^gcloud .*(services enable|secrets create|secrets versions add|add-iam-policy-binding)")


class May:
    def __init__(self, d: Path):
        self.d, self.tt = d, d / "tt.json"
        for ten in ("gcloud", "curl"):
            shutil.copy(GIA, d / ten)
            (d / ten).chmod(0o755)
        self.tt.write_text(json.dumps({"apis": [], "secrets": {}, "secret_iam": {}, "models": [OPUS, SONNET, "x/y"],
                                       "khoa_hop_le": KHOA, "loi_goi": {}, "model_tra": {}, "cost": 0.0001}),
                           encoding="utf-8")

    def doc(self):
        return json.loads(self.tt.read_text(encoding="utf-8"))

    def sua(self, f):
        s = self.doc()
        f(s)
        self.tt.write_text(json.dumps(s), encoding="utf-8")

    def lenh(self):
        p = Path(str(self.tt) + ".log")
        return p.read_text(encoding="utf-8").splitlines() if p.exists() else []

    def than(self):
        p = Path(str(self.tt) + ".than")
        return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()] if p.exists() else []

    def chay(self, *a, khoa: str | None = KHOA, ncc: str | None = "openrouter"):
        env = dict(os.environ, PATH=f"{self.d}{os.pathsep}{os.environ['PATH']}", FLS_GIA_TRANG_THAI=str(self.tt))
        env.pop("FLS_NHA_CUNG_CAP", None)
        if ncc:
            env["FLS_NHA_CUNG_CAP"] = ncc
        return subprocess.run(["bash", str(S09), "--project", DU_AN, *a], capture_output=True, text=True, env=env,
                              input=(khoa + "\n") if khoa is not None else "", timeout=120)


def muc(out: str) -> dict[str, str]:
    return {m.group(2).strip(): m.group(1) for m in re.finditer(r"\[(ĐẠT|ĐỎ)\] (.+?)\s{2,}", out)}


def do_cua(out: str) -> set[str]:
    return {k for k, v in muc(out).items() if v == "ĐỎ"}


@pytest.fixture
def g(tmp_path):
    return May(tmp_path)


@pytest.fixture
def dung(g):
    r = g.chay()
    assert r.returncode == 0, r.stdout + r.stderr
    return g


def test_dung_tu_trong__khoa_qua_STDIN__DAT__binding_MUC_BI_MAT(g):
    r = g.chay()
    assert r.returncode == 0 and "KẾT: ĐẠT" in r.stdout, r.stdout + r.stderr
    s = g.doc()
    assert s["secrets"][BM] == [KHOA] and "secretmanager.googleapis.com" in s["apis"]
    assert s["secret_iam"][BM] == [{"role": "roles/secretmanager.secretAccessor", "members": [f"serviceAccount:{SA}"]}]
    assert not any("projects add-iam-policy-binding" in x for x in g.lenh())      # ⛔ mức project
    # mong 14 mục có `mong` = 8 chung (project · biến NCC · khoá đọc · khoá trắng · SA · /models · slug · /key)
    #   + 2 mô hình × 2 (HTTP · mô hình trả về) + 2 USD (đo được · ≤ trần); 0 ĐỎ
    assert len(muc(r.stdout)) == 14 and not do_cua(r.stdout)


def test_khoa_va_noi_dung_KHONG_o_argv_dau_ra(dung):
    r = dung.chay("--kiem")
    lo = "\n".join(dung.lenh()) + r.stdout + r.stderr
    assert KHOA not in lo and "NOIDUNG-GIA" not in lo
    assert len(dung.lenh()) > 0                                    # sổ argv KHÔNG rỗng (Đ3)


def test_chay_lai__KHONG_hoi_khoa__KHONG_nhan_doi(dung):
    r = dung.chay(khoa=None)
    assert r.returncode == 0, r.stdout
    s = dung.doc()
    assert len(s["secrets"][BM]) == 1 and len(s["secret_iam"][BM]) == 1


def test_doi_khoa__them_PHIEN_BAN(dung):
    r = dung.chay("--doi-khoa", khoa=KHOA)
    assert r.returncode == 0 and len(dung.doc()["secrets"][BM]) == 2


def test_kiem__KHONG_lenh_GHI(dung):
    n = len(dung.lenh())
    r = dung.chay("--kiem", khoa=None)
    assert r.returncode == 0, r.stdout
    moi = dung.lenh()[n:]
    assert moi and not [x for x in moi if GHI.search(x)], moi


def test_moi_loi_goi_thu_mang_provider_ZDR_deny(dung):
    t = dung.than()
    assert [x["model"] for x in t] == [OPUS, SONNET]
    assert all(x["provider"] == {"data_collection": "deny", "zdr": True} for x in t)


@pytest.mark.parametrize("pha,mong_do,ten", [
    (lambda s: s["secret_iam"].update({BM: []}), {"SA có secretAccessor TRÊN bí mật"}, None),
    (lambda s: s["loi_goi"].update({OPUS: 402}), {f"gọi thử · {OPUS} · HTTP", f"gọi thử · {OPUS} · mô hình trả về = slug ghim/canonical",
                                                 "tổng usage.cost (USD THẬT do OpenRouter trả) đo được ở MỌI lời gọi thử",
                                                 "tổng usage.cost ≤ trần --tran-usd 0.10"}, "HẾT CREDIT"),
    (lambda s: s["loi_goi"].update({SONNET: 429}), {f"gọi thử · {SONNET} · HTTP", f"gọi thử · {SONNET} · mô hình trả về = slug ghim/canonical",
                                                   "tổng usage.cost (USD THẬT do OpenRouter trả) đo được ở MỌI lời gọi thử",
                                                   "tổng usage.cost ≤ trần --tran-usd 0.10"}, "GIỚI HẠN TỐC ĐỘ"),
    (lambda s: s["model_tra"].update({OPUS: "anthropic/claude-opus-4.8"}),
     {f"gọi thử · {OPUS} · mô hình trả về = slug ghim/canonical"}, None),
    (lambda s: s.update(cost=0.5), {"tổng usage.cost ≤ trần --tran-usd 0.10"}, None),
    (lambda s: s.update(models=[OPUS]), {"mọi slug mặc định còn trong /models"}, None),
])
def test_DO_HAI_CHIEU__moi_thu_pha_DUNG_muc_DO(dung, pha, mong_do, ten):
    dung.sua(pha)
    r = dung.chay("--kiem", khoa=None)
    assert r.returncode == 1 and do_cua(r.stdout) == mong_do, (do_cua(r.stdout), r.stdout)
    if ten:
        assert ten in r.stdout


def test_DO__khoa_sai__key_401_co_ten(dung):
    dung.sua(lambda s: s.update(khoa_hop_le="khoa-khac-hoan-toan-0000000000"))
    r = dung.chay("--kiem", khoa=None)
    d = do_cua(r.stdout)
    assert "GET /api/v1/key · HTTP (khoá hợp lệ)" in d and "khoá OpenRouter sai" in r.stdout and r.returncode == 1


def test_DO__bien_NCC_vang(dung):
    r = dung.chay("--kiem", khoa=None, ncc=None)
    assert do_cua(r.stdout) == {"biến FLS_NHA_CUNG_CAP của shell (agent đi đường này)"}


def test_DO__khong_goi_thu(dung):
    r = dung.chay("--kiem", "--khong-goi-thu", khoa=None)
    assert {f"gọi thử · {OPUS} · HTTP", f"gọi thử · {SONNET} · HTTP"} <= do_cua(r.stdout) and r.returncode == 1


def test_DO__chua_dung_bi_mat__kiem_DO(g):
    r = g.chay("--kiem", khoa=None)
    assert "khoá đọc được từ Secret Manager (≥ 20 ký tự)" in do_cua(r.stdout) and r.returncode == 1
    assert not [x for x in g.lenh() if GHI.search(x)]


def test_khoa_argv_bi_tu_choi__khoa_ngan_tu_choi(g):
    assert g.chay("--khoa", "abc").returncode == 2
    r = g.chay(khoa="ngan")
    assert r.returncode == 2 and BM not in g.doc()["secrets"]


def test_slug_mac_dinh_doc_tu_cau_hinh_MOT_cho():
    s = S09.read_text(encoding="utf-8")
    assert "claude-opus-5.5" not in s and "openrouter_mo_hinh.json" in s


def test_tinh__khoa_hoi_bang_read_s__qua_STDIN_gcloud():
    """Đột biến M16 (bỏ `-s`) SỐNG SÓT qua phép chạy: STDIN là ống ⇒ `read` ⛔ vọng chữ dù thiếu `-s`. ⇒ canh TĨNH:
    MỌI `read` trong script mang `-s`; khoá vào gcloud CHỈ bằng `--data-file=-` (STDIN), ⛔ `--data-file=<tệp>`."""
    s = S09.read_text(encoding="utf-8")
    doc = [x.strip() for x in s.splitlines() if re.match(r"^\s*(IFS=\S*\s+)?read\b", x)]
    assert doc and all(re.search(r"\bread\b[^|;]*\s-[a-z]*s", x) for x in doc), doc
    tep = re.findall(r"--data-file=([^\s`]+)", s)
    assert tep and set(tep) == {"-"}, tep
