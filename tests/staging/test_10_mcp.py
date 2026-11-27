"""AC-4 · `tools/staging/10_mcp.sh` + `tools/staging/app/vao_mcp.sh` trên gcloud GIẢ (`gcloud_gia_mcp.py`).

Nửa "mặt ngoài" của BÁO CÁO (bộ đo `do_mcp.py` vào máy chủ THẬT) ở `tests/mcp/test_do_mcp.py`; ở đây bộ đo được thay
bằng một tệp in sẵn kết quả (`FLS_STG_DO_MCP`) để soi ĐƯỜNG NỐI của BÁO CÁO — kể cả chiều ĐỎ.
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
SH = GOC / "tools" / "staging" / "10_mcp.sh"
VAO = GOC / "tools" / "staging" / "app" / "vao_mcp.sh"
P, SO = "du-an-thu", "123456789"
CHU = "chu.du.an@vi.du"
SA = f"serviceAccount:fls-staging-mcp@{P}.iam.gserviceaccount.com"
URL = f"https://fls-staging-mcp-{SO}.asia-southeast1.run.app"
GID, GSEC = "1234-gia.apps.googleusercontent.com", "GOCSPX-gia-bi-mat-9f3a"
DO_DAT = "\n".join(["khong_token=401", "www_resource_metadata=co", "prm_resource_khop=True", "prm_as_khop=True",
                    "as_issuer_khop=True", "dang_ky_redirect_la=400", "token_khoa_gia=401", "token_aud_sai=401",
                    "token_het_han=401", "nguoi_ngoai=403", "chu_khoi_tao=200", "chu_so_bang=27",
                    "chu_bang_co_dong=0", "chu_insert=chan", "rieng_tu_mau_so=310/0", "rieng_tu_email=0/0",
                    "chu_cong=9"])


def _dung(tmp_path: Path, **them) -> dict:
    bin_ = tmp_path / "bin"
    bin_.mkdir()
    shutil.copy(GOC / "tests" / "staging" / "gcloud_gia_mcp.py", bin_ / "gcloud")
    (bin_ / "gcloud").chmod(0o755)
    tt = {"project": P, "so_project": SO, "tai_khoan": CHU, "api": [], "sa": [], "tag": [],
          "bi_mat": {"fls-staging-pg-fls_doc": {"gia_tri": ["MKGIA-doc"], "pol": {"bindings": []}},
                     "fls-staging-jwt-secret": {"gia_tri": ["MKGIA-jwt"], "pol": {"bindings": [
                         {"role": "roles/secretmanager.secretAccessor",
                          "members": [f"serviceAccount:fls-staging-app@{P}.iam.gserviceaccount.com"]}]}}},
          "proj_pol": {"bindings": [{"role": "roles/x", "members": ["user:khac@vi.du"],
                                     "condition": {"expression": "true", "title": "fps-v35"}}]}}
    tt.update(them)
    (tmp_path / "tt.json").write_text(json.dumps(tt), encoding="utf-8")
    do = tmp_path / "do_gia.py"
    do.write_text("import os,sys\nassert len(os.environ['FLS_MCP_KHOA_DO']) == 128, 'khoa'\n"
                  f"assert os.environ['FLS_MCP_DO_CHU'] in ({CHU!r}, 'a@vi.du')\nassert sys.argv[1:] == ['--url', {URL!r}]\n"
                  f"print({DO_DAT!r})\n", encoding="utf-8")
    return {"tt": tmp_path / "tt.json", "env": dict(os.environ, PATH=f"{bin_}:{os.environ['PATH']}",
                                                     FLS_GIA_MCP=str(tmp_path / "tt.json"), FLS_STG_DO_MCP=str(do))}


def _chay(h, *doi, nhap: str = ""):
    r = subprocess.run(["bash", str(SH), "--project", P, *doi], capture_output=True, text=True, env=h["env"],
                       input=nhap, timeout=120)
    return r, json.loads(h["tt"].read_text(encoding="utf-8"))


def _bao_cao(out: str) -> str:
    return out[out.index("── BÁO CÁO"):]


def test_KIEM_tren_du_an_trong_CHI_DOC_va_DO(tmp_path):
    h = _dung(tmp_path)
    r, s = _chay(h, "--kiem")
    assert r.returncode == 1 and "KẾT: ĐỎ" in r.stdout, r.stderr
    doi = [x for x in s["nhat_ky"] if any(k in x for k in ("create", "add", "enable", "deploy", "submit"))]
    assert doi == [], doi                                                 # --kiem ⛔ đổi gì


def test_THIEU_oauth_thi_KHONG_deploy_va_in_redirect_uri(tmp_path):
    h = _dung(tmp_path)
    r, s = _chay(h)
    assert r.returncode == 1 and f"{URL}/oauth/google/callback" in r.stdout
    assert not any(x[2:4] == ["run", "deploy"] or x[:2] == ["run", "deploy"] for x in s["nhat_ky"])
    assert "fls-staging-mcp-khoa" in s["bi_mat"] and len(s["bi_mat"]["fls-staging-mcp-khoa"]["gia_tri"][0]) == 128
    assert s["bi_mat"]["fls-staging-mcp-cho-phep"]["gia_tri"] == [CHU]   # mặc định CHỈ người chạy


def test_DUNG_DU_thi_KET_DAT_va_quyen_DUNG_hep(tmp_path):
    h = _dung(tmp_path)
    r, s = _chay(h, "--oauth-nhap", nhap=f"{GID}\n{GSEC}\n")
    bc = _bao_cao(r.stdout)
    assert r.returncode == 0 and "KẾT: ĐẠT" in bc, bc + r.stderr
    assert len(re.findall(r"\[ĐẠT\]", bc)) == 39 and "[ĐỎ]" not in bc
    assert json.loads(s["bi_mat"]["fls-staging-mcp-oauth"]["gia_tri"][-1]) == {"client_id": GID, "client_secret": GSEC}
    # quyền: 4 bí mật · ⛔ jwt · MỘT binding dự án CÓ điều kiện
    doc = sorted(t for t, b in s["bi_mat"].items() if any(SA in x["members"] for x in b["pol"]["bindings"]))
    assert doc == ["fls-staging-mcp-cho-phep", "fls-staging-mcp-khoa", "fls-staging-mcp-oauth", "fls-staging-pg-fls_doc"]
    cua_sa = [b for b in s["proj_pol"]["bindings"] if SA in b["members"]]
    assert cua_sa == [{"role": "roles/cloudsql.client", "members": [SA], "condition": {
        "expression": f'resource.name == "projects/{P}/instances/fls-staging"', "title": "fls-staging-mcp-chi-fls-staging"}}]
    dep = next(x for x in s["nhat_ky"] if "deploy" in x)
    assert "--allow-unauthenticated" in dep and f"--set-env-vars=FLS_STG_PROJECT={P},FLS_STG_CONN={P}:asia-southeast1:fls-staging,FLS_MCP_URL={URL}" in dep


def test_BAO_CAO_va_dong_lenh_KHONG_lo_email_bi_mat(tmp_path):
    h = _dung(tmp_path)
    r, s = _chay(h, "--oauth-nhap", nhap=f"{GID}\n{GSEC}\n")
    assert GSEC not in r.stdout + r.stderr and CHU not in _bao_cao(r.stdout)
    assert not any(GSEC in " ".join(x) or CHU in " ".join(x) for x in s["nhat_ky"])     # ⛔ ở dòng lệnh (ps)
    assert re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", _bao_cao(r.stdout).replace(f"@{P}.iam.gserviceaccount.com", "")) == []


def test_KHONG_dung_tai_nguyen_ngoai_FLS_va_KHONG_xoa(tmp_path):
    h = _dung(tmp_path)
    _, s = _chay(h, "--oauth-nhap", nhap=f"{GID}\n{GSEC}\n")
    for x in s["nhat_ky"]:
        van = " ".join(x)
        assert not re.search(r"\b(delete|remove-iam-policy-binding|set-iam-policy|update)\b", van), van
        if x[2:4] == ["run", "deploy"] or "services" in x and "describe" in x and "run" in x:
            assert "fls-staging-mcp" in van, van
        for t in re.findall(r"secrets \S+ (?:\S+ )?(fls-[\w-]+)", van):
            assert t.startswith("fls-staging-"), van


def test_DE_cho_phep_ghi_phien_ban_moi(tmp_path):
    h = _dung(tmp_path)
    _chay(h, "--oauth-nhap", nhap=f"{GID}\n{GSEC}\n")
    r, s = _chay(h, "--cho-phep", "a@vi.du,b@vi.du")
    assert s["bi_mat"]["fls-staging-mcp-cho-phep"]["gia_tri"] == [CHU, "a@vi.du,b@vi.du"] and r.returncode == 0
    assert "a@vi.du" not in r.stdout


@pytest.mark.parametrize("pha,mong_do", [
    ("sa_doc_jwt", "SA đọc được bí mật NGOÀI"),
    ("cloudsql_khong_dieu_kien", "binding MỨC DỰ ÁN của SA"),
    ("do_nguoi_ngoai_200", "token thật của NGƯỜI NGOÀI"),
    ("do_insert_lot", "truy_van_doc INSERT"),
    ("do_email", "riêng tư: cột *email*"),
    ("do_khong_chay", "token của CHỦ"),
])
def test_PHA_thi_BAO_CAO_DO_dung_muc(tmp_path, pha, mong_do):
    """Đ5 — mỗi hỏng hóc có tên ⇒ ĐỎ ĐÚNG mục ấy (và KẾT ĐỎ)."""
    h = _dung(tmp_path)
    _chay(h, "--oauth-nhap", nhap=f"{GID}\n{GSEC}\n")
    s = json.loads(h["tt"].read_text(encoding="utf-8"))
    do = Path(h["env"]["FLS_STG_DO_MCP"])
    if pha == "sa_doc_jwt":
        s["bi_mat"]["fls-staging-jwt-secret"]["pol"]["bindings"][0]["members"].append(SA)
    elif pha == "cloudsql_khong_dieu_kien":
        s["proj_pol"]["bindings"].append({"role": "roles/cloudsql.client", "members": [SA]})
    elif pha == "do_khong_chay":
        do.write_text("import sys; sys.exit(3)\n", encoding="utf-8")
    else:
        cu, moi = {"do_nguoi_ngoai_200": ("nguoi_ngoai=403", "nguoi_ngoai=200"),
                   "do_insert_lot": ("chu_insert=chan", "chu_insert=LOT"),
                   "do_email": ("rieng_tu_email=0/0", "rieng_tu_email=0/3")}[pha]
        do.write_text(do.read_text(encoding="utf-8").replace(cu, moi), encoding="utf-8")
    h["tt"].write_text(json.dumps(s), encoding="utf-8")
    r, _ = _chay(h, "--kiem")
    do_dong = [d for d in r.stdout.splitlines() if "[ĐỎ]" in d]
    assert r.returncode == 1 and any(mong_do in d for d in do_dong), do_dong


def test_vao_mcp_noi_bi_mat_vao_MOI_TRUONG_khong_vao_doi_so(tmp_path):
    """`vao_mcp.sh` đến tận `exec chay_mcp.py`: python GIẢ trả bí mật (thay `lay_bi_mat.py`) và chụp môi trường."""
    py = tmp_path / "py"
    chup = tmp_path / "chup.json"
    py.write_text(f"""#!/usr/bin/env bash
if [[ "$1" == *lay_bi_mat.py ]]; then
  case "$2" in
    fls-staging-pg-fls_doc) printf MKGIA-doc ;; fls-staging-mcp-khoa) printf 'ab%.0s' {{1..64}} ;;
    fls-staging-mcp-oauth) printf '{{"client_id":"{GID}","client_secret":"{GSEC}"}}' ;;
    fls-staging-mcp-cho-phep) printf '{CHU}' ;; *) exit 9 ;;
  esac; exit 0
fi
if [ "$1" = "-c" ]; then exec python3 "$@"; fi
python3 -c 'import json,os,sys; json.dump({{"argv":sys.argv[1:],"env":{{k:v for k,v in os.environ.items() if k.startswith(("FLS_MCP","PG"))}}}},open("{chup}","w"))' "$@"
""", encoding="utf-8")
    py.chmod(0o755)
    env = dict(os.environ, FLS_STG_PROJECT=P, FLS_STG_CONN=f"{P}:asia-southeast1:fls-staging", FLS_MCP_URL=URL,
               FLS_STG_PYTHON=str(py), PORT="8080", FLS_STG_KHO="kho_thu")
    r = subprocess.run(["bash", str(VAO)], capture_output=True, text=True, env=env, timeout=30)
    assert r.returncode == 0, r.stderr
    d = json.loads(chup.read_text())
    assert d["argv"] == ["tools/chay_mcp.py", "--http", "--dia-chi", "0.0.0.0", "--cong", "8080"]
    e = d["env"]
    assert (e["PG_DSN"], e["PGPASSWORD"]) == (f"postgresql://fls_doc@/kho_thu?host=/cloudsql/{P}:asia-southeast1:fls-staging",
                                              "MKGIA-doc")
    assert (e["FLS_MCP_GOOGLE_ID"], e["FLS_MCP_GOOGLE_SECRET"], e["FLS_MCP_CHO_PHEP"], e["FLS_MCP_URL"]) == (GID, GSEC, CHU, URL)
    assert len(e["FLS_MCP_KHOA"]) == 128
    assert GSEC not in r.stdout + r.stderr and "MKGIA" not in r.stdout + r.stderr and CHU not in r.stdout
    r2 = subprocess.run(["bash", str(VAO)], capture_output=True, text=True, env={**env, "FLS_MCP_URL": "http://x"})
    assert r2.returncode == 2 and "https" in r2.stderr                     # ⛔ URL không TLS


def test_bash_n_hai_script():
    for p in (SH, VAO):
        assert subprocess.run(["bash", "-n", str(p)]).returncode == 0, p
