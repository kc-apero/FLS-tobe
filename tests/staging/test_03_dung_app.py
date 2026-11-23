"""Bài thử bước 03 — `WO-325` AC-2: `Dockerfile` · `tools/staging/03_dung_app.sh` · `app/vao.sh` · `app/lay_bi_mat.py`.

Ba phần:
  ⓐ `03_dung_app.sh` vs một **project GCP GIẢ có trạng thái** (`gcloud_gia.py`): dựng từ trống ⇒ ĐẠT; chạy lại được;
     `--kiem` chỉ đọc; phá từng thứ ⇒ ĐÚNG mục ĐỎ; ngữ cảnh build ⛔ có dữ liệu gitignore (chim hoàng yến thật).
  ⓑ `vao.sh` + `lay_bi_mat.py` **chạy thật** vào kho scratch (Secret Manager + metadata = máy chủ HTTP giả):
     cửa nghe loopback · gọi không thẻ ⇒ 401 · thiếu `FLS_JWT_SECRET` ⇒ cửa từ chối · chế độ `doc` ⇒ POST 405.
  ⓒ tĩnh: `Dockerfile` là danh sách cho phép · `.dockerignore` khớp · VM ⛔ publish cổng.
"""
from __future__ import annotations

import base64
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request

import psycopg
import pytest

from tests.staging import ho_tro as H

S03 = H.STG / "03_dung_app.sh"
GCLOUD_GIA = H.GOC / "tests" / "staging" / "gcloud_gia.py"
SA = "fls-staging-app@du-an-gia.iam.gserviceaccount.com"
TAG = "thu-tag"
IMAGE = f"asia-southeast1-docker.pkg.dev/du-an-gia/fls/fls-app:{TAG}"
GOOD_SSH = "container=running\nnghe=127.0.0.1:8088,\nhttp_khong_the=401\nhttp_man_hinh=200"
CAM_GHI = re.compile(r"\b(delete|remove|disable|unbind|destroy|set-iam-policy|remove-iam-policy-binding)\b")


# ══ ⓐ 03_dung_app.sh vs GCP giả ═══════════════════════════════════════════════════════════════

class Gcp:
    def __init__(self, thu_muc):
        self.dir = thu_muc
        self.tt = thu_muc / "trang_thai.json"
        self.log = thu_muc / "trang_thai.json.log"
        shutil.copy(GCLOUD_GIA, thu_muc / "gcloud")
        (thu_muc / "gcloud").chmod(0o755)
        self.dat({"apis": [], "conn": "du-an-gia:asia-southeast1:fls-staging", "repo": False, "repo_iam": [], "anh_tags": [],
                  "builds": [], "vm": None, "quyen": [], "ssh_ra": GOOD_SSH,
                  "fw": [{"name": "default-allow-ssh", "direction": "INGRESS", "priority": 65534,
                          "sourceRanges": ["0.0.0.0/0"], "allowed": [{"IPProtocol": "tcp", "ports": ["22"]}], "disabled": False},
                         {"name": "default-allow-internal", "direction": "INGRESS", "priority": 65534,
                          "sourceRanges": ["10.128.0.0/9"], "allowed": [{"IPProtocol": "all"}], "disabled": False}]})

    def doc(self):
        return json.loads(self.tt.read_text(encoding="utf-8"))

    def dat(self, s):
        self.tt.write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")

    def sua(self, f):
        s = self.doc()
        f(s)
        self.dat(s)

    def lenh_da_goi(self):
        """Mỗi lệnh gcloud đã gọi, BỎ `--project=… --quiet` đứng đầu (chỉ còn lệnh thật)."""
        if not self.log.exists():
            return []
        return [re.sub(r"^--project=\S+ --quiet ", "", d) for d in self.log.read_text(encoding="utf-8").splitlines()]

    def chay(self, *args, env_them=None):
        env = dict(os.environ)
        env.update({"PATH": f"{self.dir}{os.pathsep}{env['PATH']}", "FLS_GIA_TRANG_THAI": str(self.tt), "PYTHONUTF8": "1"})
        if env_them:
            env.update(env_them)
        return subprocess.run(["bash", str(S03), "--project", "du-an-gia", "--tag", TAG, *args],
                              capture_output=True, text=True, env=env, timeout=300)


@pytest.fixture
def gcp(tmp_path):
    return Gcp(tmp_path)


@pytest.fixture
def chim_hoang_yen():
    """Dữ liệu GITIGNORE thật đặt vào repo — bài chứng minh chúng ⛔ lên Cloud Build. Dọn xong trả nguyên."""
    tao = []
    for rel, nd in (("sao_luu/chim_hoang_yen_stg.txt", "SO THAT"), ("hien_vat/chim_hoang_yen_stg.html", "<p>TEN NGUOI</p>"),
                    ("Input_Raw/chim_hoang_yen_stg.csv", "TK,so"), (".env.chim_hoang_yen_stg", "SECRET=x")):
        p = H.GOC / rel
        co_thu_muc = p.parent.exists()
        p.parent.mkdir(exist_ok=True)
        p.write_text(nd, encoding="utf-8")
        tao.append((p, co_thu_muc))
    yield [p.name for p, _ in tao]
    for p, co_thu_muc in tao:
        p.unlink(missing_ok=True)
        if not co_thu_muc and p.parent.exists() and not any(p.parent.iterdir()):
            p.parent.rmdir()


def _dat(out):
    return {k for k, v in H.dong_bao_cao(out).items() if v == "ĐẠT"}


def test_dung_tu_trong_ra_DAT_va_ngu_canh_build_SACH(gcp, chim_hoang_yen):
    r = gcp.chay()
    assert r.returncode == 0, r.stdout + r.stderr
    assert "KẾT: ĐẠT" in r.stdout and not H.muc_do(r.stdout), r.stdout
    assert len(_dat(r.stdout)) >= 18, sorted(_dat(r.stdout))          # Đ3: báo cáo ĐẠT là báo cáo CÓ ĐO
    tep = set(gcp.doc()["builds"][0]["tep"])
    assert gcp.doc()["builds"][0]["tag"] == IMAGE
    # ⭐ chứng minh DƯƠNG: ngữ cảnh KHÔNG rỗng và có đúng thứ ảnh cần (Đ3 — "không có gì cấm" trên tập rỗng là vô nghĩa)
    for can in ("Dockerfile", "requirements.txt", "tools/chay_cua.py", "tools/staging/app/vao.sh",
                "tools/staging/app/lay_bi_mat.py", "fls/api/cua.py", "docs/ITL/_tools/hd2_cong.json",
                "tests/fixture/dap_an/gl_406_dau_vao.json"):
        assert can in tep, (can, len(tep))
    assert len(tep) > 200
    # ⭐ `STG-R2b-01`: gcloud tải lên ĐÚNG cả ngữ cảnh (giả nay lọc theo `.gcloudignore` như GCP đo) + mục BÁO CÁO có `mong`
    assert len(tep) == gcp.doc()["builds"][0]["ngu_canh"] and ".gcloudignore" not in tep, len(tep)
    assert H.dong_bao_cao(r.stdout)["ngữ cảnh build · tệp tải lên = tệp ngữ cảnh (≠ 0)"] == "ĐẠT"
    assert re.search(rf"tệp ngữ cảnh / tệp gcloud tải lên \(đếm\)\s+{len(tep)} / {len(tep)}\b", r.stdout), r.stdout
    # ⛔ rồi chứng minh ÂM: chim hoàng yến (đã tồn tại thật trên đĩa) ⛔ có mặt
    tren_dia = [p for p in chim_hoang_yen if (H.GOC / "sao_luu" / p).exists() or (H.GOC / "hien_vat" / p).exists()
                or (H.GOC / "Input_Raw" / p).exists() or (H.GOC / p).exists()]
    assert len(tren_dia) == 4, "chim hoàng yến chưa nằm trên đĩa — bài vô nghĩa"
    bi_lo = [t for t in tep if "chim_hoang_yen" in t or t.startswith(("sao_luu/", "hien_vat/", "Input_Raw/", ".git/"))
             or "/.env" in t or t.startswith(".env")]
    assert bi_lo == [], bi_lo
    assert not any(t.startswith(("tests/api", "tests/nghiem_thu", "docs/ITL/02_BA", "AS-IS")) for t in tep), \
        "ngữ cảnh mang cả test/BA — ảnh phình"


def test_chi_goi_lenh_GHI_dung_danh_sach_va_firewall_chan_TRUOC_khi_co_VM(gcp):
    assert gcp.chay().returncode == 0
    nk = gcp.lenh_da_goi()
    assert not [d for d in nk if CAM_GHI.search(d)], [d for d in nk if CAM_GHI.search(d)]
    ghi = [re.match(r"(services enable|artifacts repositories create|artifacts repositories add-iam-policy-binding|builds submit|"
                    r"compute firewall-rules create|compute instances (?:create|add-metadata|reset|add-iam-policy-binding)|"
                    r"projects add-iam-policy-binding)", d) for d in nk]
    ghi = {m.group(1) for m in ghi if m}
    assert ghi == {"services enable", "artifacts repositories create", "artifacts repositories add-iam-policy-binding",
                   "builds submit", "compute firewall-rules create", "compute instances create"}, ghi
    thu_tu = [i for i, d in enumerate(nk) if d.startswith("compute firewall-rules create")]
    vm = [i for i, d in enumerate(nk) if d.startswith("compute instances create")][0]
    assert len(thu_tu) == 2 and max(thu_tu) < vm, "luật chặn phải có TRƯỚC khi VM tồn tại"
    cho_iap = [d for d in nk if "firewall-rules create" in d]
    chan = [d for d in cho_iap if "--action=DENY" in d][0]
    allow = [d for d in cho_iap if "--action=ALLOW" in d][0]
    assert "--priority=900" in chan and "--priority=800" in allow
    assert "--source-ranges=35.235.240.0/20" in allow and "--rules=tcp:22" in allow, "ALLOW chỉ dải IAP, chỉ cổng 22"
    assert "0.0.0.0/0" not in allow
    tao_vm = [d for d in nk if d.startswith("compute instances create")][0]
    assert f"--service-account={SA}" in tao_vm and "--tags=fls-stg-app" in tao_vm
    assert "--shielded-secure-boot" in tao_vm and "enable-oslogin=TRUE" in tao_vm
    assert "--no-address" not in tao_vm and "--address" not in tao_vm.replace("--metadata", "")   # IP tạm: Cloud SQL cần đường ra
    assert "fls-che-do=doc" in tao_vm, "mặc định CHỈ-ĐỌC"
    assert "fls-actor=staging-doc" in tao_vm and "thu@apero.vn" not in tao_vm


def test_chay_lai_khong_tao_lai_ha_tang_chi_cap_nhat_va_khoi_dong_lai(gcp):
    assert gcp.chay().returncode == 0
    truoc = len(gcp.lenh_da_goi())
    r = gcp.chay("--che-do", "ghi", "--nguoi-ky", "tester.mot")
    assert r.returncode == 0, r.stdout + r.stderr
    moi = gcp.lenh_da_goi()[truoc:]
    assert not [d for d in moi if re.match(r"(artifacts repositories create|compute firewall-rules create|compute instances create)", d)], moi
    assert any(d.startswith("compute instances add-metadata") and "fls-che-do=ghi" in d for d in moi)
    assert any(d.startswith("compute instances reset") for d in moi)
    md = {i["key"]: i["value"] for i in gcp.doc()["vm"]["metadata"]["items"]}
    assert md["fls-che-do"] == "ghi" and md["fls-image"] == IMAGE and md["fls-actor"] == "tester.mot"


def test_kiem_chi_goi_lenh_DOC_va_khong_doi_trang_thai(gcp):
    assert gcp.chay().returncode == 0
    truoc_tt, truoc_n = gcp.doc(), len(gcp.lenh_da_goi())
    r = gcp.chay("--kiem")
    assert r.returncode == 0 and "--kiem (chỉ đọc)" in r.stdout, r.stdout
    moi = gcp.lenh_da_goi()[truoc_n:]
    assert moi and not [d for d in moi if re.match(r"(services enable|artifacts repositories (create|add)|builds|"
                                                  r"compute (firewall-rules create|instances (create|add|reset))|projects add)", d)], moi
    assert gcp.doc() == truoc_tt


def test_cap_quyen_cho_nguoi_test_ghi_dung_hai_quyen_moi_nguoi(gcp):
    r = gcp.chay("--cap-quyen", "a@x.com,b.c@y.org")
    assert r.returncode == 0, r.stdout + r.stderr
    q = gcp.doc()["quyen"]
    assert sorted((x["member"], x["role"]) for x in q) == sorted(
        [("user:a@x.com", "roles/compute.osLogin"), ("user:a@x.com", "roles/iap.tunnelResourceAccessor"),
         ("user:b.c@y.org", "roles/compute.osLogin"), ("user:b.c@y.org", "roles/iap.tunnelResourceAccessor")]), q
    # ⛔ không cấp vai rộng
    assert not [x for x in q if x["role"] in ("roles/owner", "roles/editor", "roles/compute.admin", "roles/compute.instanceAdmin.v1")]


# (tên, hàm phá trạng thái, tập mục ĐỎ mong — nguyên văn nhãn)
def _fw_mo_ssh(s):
    s["fw"].append({"name": "ai-do-mo-ssh", "direction": "INGRESS", "priority": 700, "sourceRanges": ["0.0.0.0/0"],
                    "targetTags": ["fls-stg-app"], "allowed": [{"IPProtocol": "tcp"}], "disabled": False})


PHA = [
    ("vm_sai_SA", lambda s: s["vm"].__setitem__("serviceAccounts", [{"email": "1234-compute@developer.gserviceaccount.com"}]),
     {"VM chạy bằng SA"}),
    ("firewall_mo_ssh_toan_cau_uu_tien_700", _fw_mo_ssh,
     {"firewall: luật ALLOW áp lên VM, nguồn ngoài dải IAP, ⛔ bị DENY đè (đếm)"}),
    ("mat_luat_chan_lo_default_allow_ssh", lambda s: s["fw"].__setitem__(slice(None), [r for r in s["fw"] if r["name"] != "fls-stg-chan-vao"]),
     {"firewall: luật CHẶN vào (tag, ưu tiên 900)", "firewall: luật ALLOW áp lên VM, nguồn ngoài dải IAP, ⛔ bị DENY đè (đếm)"}),
    ("luat_cho_iap_mo_rong_nguon", lambda s: [r.__setitem__("sourceRanges", ["0.0.0.0/0"]) for r in s["fw"] if r["name"] == "fls-stg-cho-iap-ssh"],
     {"firewall: luật cho IAP vào cổng 22",     # nguồn nới ra 0.0.0.0/0 ⇒ ⛔ còn là luật "chỉ IAP", VÀ nó mở ra ngoài
      "firewall: luật ALLOW áp lên VM, nguồn ngoài dải IAP, ⛔ bị DENY đè (đếm)"}),
    ("vm_tat", lambda s: s["vm"].__setitem__("status", "TERMINATED"), {"VM trạng thái"}),
    ("vm_chay_sai_anh", lambda s: [i.__setitem__("value", "x/y/z:cu") for i in s["vm"]["metadata"]["items"] if i["key"] == "fls-image"],
     {"VM chạy đúng ảnh mong"}),
    ("vm_sai_che_do", lambda s: [i.__setitem__("value", "ghi") for i in s["vm"]["metadata"]["items"] if i["key"] == "fls-che-do"],
     {"VM chế độ app"}),
    ("vm_actor_la_thu_apero", lambda s: [i.__setitem__("value", "thu@apero.vn") for i in s["vm"]["metadata"]["items"] if i["key"] == "fls-actor"],
     {"VM actor của mọi chữ ký"}),
    ("vm_het_oslogin", lambda s: [i.__setitem__("value", "FALSE") for i in s["vm"]["metadata"]["items"] if i["key"] == "enable-oslogin"],
     {"VM dùng OS Login"}),
    ("vm_mat_tag", lambda s: s["vm"].__setitem__("tags", {"items": []}), {"VM gắn tag firewall"}),
    ("anh_chua_co", lambda s: s.__setitem__("anh_tags", []), {"ảnh có tag mong"}),
    ("SA_khong_doc_duoc_kho_anh", lambda s: s.__setitem__("repo_iam", []), {"SA fls-staging-app đọc được kho ảnh"}),
    ("thieu_API_iap", lambda s: s["apis"].remove("iap.googleapis.com"), {"API bật (đếm / 4)"}),
    ("container_chet",
     lambda s: s.__setitem__("ssh_ra", "container=exited\nnghe=\nhttp_khong_the=000\nhttp_man_hinh=000"),
     {"TRONG VM · container fls-app", "TRONG VM · cổng 8088 nghe (số địa chỉ)", "TRONG VM · cổng 8088 chỉ nghe 127.0.0.1",
      "TRONG VM · gọi API không thẻ ⇒ HTTP", "TRONG VM · màn hình / ⇒ HTTP"}),
    ("cong_8088_nghe_ra_ngoai", lambda s: s.__setitem__("ssh_ra", GOOD_SSH.replace("127.0.0.1:8088", "0.0.0.0:8088")),
     {"TRONG VM · cổng 8088 chỉ nghe 127.0.0.1"}),
    ("api_khong_xac_thuc_tra_200", lambda s: s.__setitem__("ssh_ra", GOOD_SSH.replace("=401", "=200")),
     {"TRONG VM · gọi API không thẻ ⇒ HTTP"}),
    ("IAP_ssh_khong_vao_duoc", lambda s: s.__setitem__("ssh_hong", True),
     {"TRONG VM · container fls-app", "TRONG VM · cổng 8088 nghe (số địa chỉ)", "TRONG VM · cổng 8088 chỉ nghe 127.0.0.1",
      "TRONG VM · gọi API không thẻ ⇒ HTTP", "TRONG VM · màn hình / ⇒ HTTP"}),
]


@pytest.mark.parametrize("ten,pha,mong_do", PHA, ids=[p[0] for p in PHA])
def test_pha_mot_thu_thi_DUNG_muc_do(gcp, ten, pha, mong_do):
    assert gcp.chay().returncode == 0, "nền chưa ĐẠT"
    gcp.sua(pha)
    r = gcp.chay("--kiem")
    assert r.returncode == 1 and "KẾT: ĐỎ" in r.stdout, (ten, r.stdout)
    assert H.muc_do(r.stdout) == mong_do, (ten, H.muc_do(r.stdout) ^ mong_do, r.stdout)


def test_project_TRONG_thi_kiem_ra_DO_het_khong_muc_nao_xanh_suong__D3_D5(gcp):
    r = gcp.chay("--kiem")
    assert r.returncode == 1, r.stdout
    assert _dat(r.stdout) == set(), sorted(_dat(r.stdout))


def test_gcloud_HONG_het_thi_0_muc_DAT__D5(gcp, tmp_path):
    hong = tmp_path / "hong"
    hong.mkdir()
    (hong / "gcloud").write_text("#!/usr/bin/env bash\nexit 1\n")
    (hong / "gcloud").chmod(0o755)
    env = dict(os.environ, PATH=f"{hong}{os.pathsep}{os.environ['PATH']}")
    r = subprocess.run(["bash", str(S03), "--project", "p", "--kiem"], capture_output=True, text=True, env=env, timeout=120)
    assert r.returncode == 1 and _dat(r.stdout) == set(), r.stdout


@pytest.mark.parametrize("args,loi", [
    (("--che-do", "ghi;rm"), "--che-do phải là doc|ghi"),
    (("--vm", "a;b"), "chỉ gồm"),
    (("--cap-quyen", "a b;rm -rf"), "--cap-quyen"),
    (("--la",), "tham số lạ"),
    (("--che-do", "ghi"), "--nguoi-ky"),                                   # ghi mà ⛔ nói ai ký ⇒ chữ ký mang tên mặc định
    (("--nguoi-ky", "thu@apero.vn"), "thu@apero.vn"),                      # ⛔ mượn tên mặc định của chay_cua.py
    (("--che-do", "ghi", "--nguoi-ky", "a b;rm"), "--nguoi-ky chỉ"),
])
def test_tham_so_xau_exit_2_va_khong_goi_gcloud(gcp, args, loi):
    r = gcp.chay(*args)
    assert r.returncode == 2 and loi in r.stderr, (args, r.stderr)
    assert gcp.lenh_da_goi() == [], "đã gọi gcloud trước khi kiểm tham số"


def test_thieu_project_exit_2():
    r = subprocess.run(["bash", str(S03)], capture_output=True, text=True)
    assert r.returncode == 2 and "thiếu --project" in r.stderr


# ══ ⓑ lay_bi_mat.py + vao.sh CHẠY THẬT ═══════════════════════════════════════════════════════════

class MayChuGia(http.server.ThreadingHTTPServer):
    """Metadata server + Secret Manager GIẢ trong một cổng. `thieu` = tên bí mật ⇒ 404."""
    daemon_threads = True


def _may_chu(bi_mat: dict[str, str], thieu: set[str] = frozenset()):
    class Tay(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def do_GET(self):
            if self.path == "/computeMetadata/v1/instance/service-accounts/default/token":
                if self.headers.get("Metadata-Flavor") != "Google":
                    self.send_response(403); self.end_headers(); return
                return self._ra(200, {"access_token": "TOKEN-GIA-123", "expires_in": 3000})
            m = re.fullmatch(r"/v1/projects/(?P<p>[^/]+)/secrets/(?P<s>[^/]+)/versions/latest:access", self.path)
            if m and self.headers.get("Authorization") == "Bearer TOKEN-GIA-123":
                if m["s"] in thieu or m["s"] not in bi_mat:
                    return self._ra(404, {"error": "not found"})
                self.server.da_doc.append((m["p"], m["s"]))
                return self._ra(200, {"payload": {"data": base64.b64encode(bi_mat[m["s"]].encode()).decode()}})
            self._ra(403, {})

        def _ra(self, ma, o):
            b = json.dumps(o).encode()
            self.send_response(ma); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(b)

    sv = MayChuGia(("127.0.0.1", 0), Tay)
    sv.da_doc = []
    threading.Thread(target=sv.serve_forever, daemon=True).start()
    return sv


JWT_GIA = H.MK["fls-staging-jwt-secret"]            # ≥ 32 ký tự: cửa từ chối khoá ngắn (`fls.api.the.khoa`)


def _chay_lay(ten, sv, project="du-an-gia", extra=None):
    env = dict(os.environ, FLS_STG_PROJECT=project, FLS_STG_URL_METADATA=f"http://127.0.0.1:{sv.server_port}",
               FLS_STG_URL_SM=f"http://127.0.0.1:{sv.server_port}", PYTHONUTF8="1")
    if extra:
        env.update(extra)
    return subprocess.run([sys.executable, "-I", str(H.STG / "app" / "lay_bi_mat.py"), ten],
                          capture_output=True, text=True, env=env, timeout=60)


def test_lay_bi_mat_tra_gia_tri_dung_va_chi_ra_stdout():
    sv = _may_chu(dict(H.MK))
    try:
        r = _chay_lay("fls-staging-pg-fls_doc", sv)
        assert r.returncode == 0 and r.stdout == H.MK["fls-staging-pg-fls_doc"] and r.stderr == "", (r.stdout, r.stderr)
        assert sv.da_doc == [("du-an-gia", "fls-staging-pg-fls_doc")]
    finally:
        sv.shutdown()


def test_lay_bi_mat_loi_KHONG_in_gia_tri_hay_token():
    sv = _may_chu(dict(H.MK), thieu={"fls-staging-jwt-secret"})
    try:
        r = _chay_lay("fls-staging-jwt-secret", sv)
        assert r.returncode != 0 and "HTTP 404" in r.stderr and "fls-staging-jwt-secret" in r.stderr
        assert "TOKEN-GIA" not in r.stdout + r.stderr and "MKGIA" not in r.stdout + r.stderr
        r2 = _chay_lay("khong co;rm", sv)
        assert r2.returncode == 2
        r3 = _chay_lay("fls-staging-jwt-secret", sv, extra={"FLS_STG_PROJECT": ""})
        assert r3.returncode == 2 and "FLS_STG_PROJECT" in r3.stderr
        r4 = _chay_lay("fls-staging-jwt-secret", sv, extra={"FLS_STG_URL_METADATA": "http://127.0.0.1:9"})
        assert r4.returncode != 0 and "metadata" in r4.stderr
    finally:
        sv.shutdown()


def _cong_trong():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def _vao(kho_san, sv, che_do="doc", actor=None):
    """Chạy `vao.sh` thật (host python, proxy GIẢ ngủ, kho = scratch cục bộ). Trả (Popen, cổng cửa)."""
    cong = _cong_trong()
    gia = kho_san["gia"]["dir"]
    proxy = gia / "proxy-vao"
    proxy.write_text("#!/usr/bin/env bash\nexec sleep 600\n"); proxy.chmod(0o755)
    env = dict(os.environ, FLS_STG_PROJECT="du-an-gia", FLS_STG_CONN="du-an-gia:asia-southeast1:fls-staging",
               FLS_STG_CHE_DO=che_do, FLS_STG_CONG_PROXY=str(H.cong_pg()), FLS_STG_CONG=str(cong),
               FLS_STG_KHO=kho_san["kho"], FLS_STG_PYTHON=sys.executable, FLS_STG_PROXY=str(proxy),
               FLS_STG_URL_METADATA=f"http://127.0.0.1:{sv.server_port}", FLS_STG_URL_SM=f"http://127.0.0.1:{sv.server_port}",
               PYTHONUTF8="1")
    for k in ("PG_DSN", "PG_DSN_TEST", "PGPASSWORD", "FLS_JWT_SECRET", "FLS_STG_ACTOR"):
        env.pop(k, None)
    if actor is not None:
        env["FLS_STG_ACTOR"] = actor
    p = subprocess.Popen(["bash", str(H.STG / "app" / "vao.sh")], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p, cong


def _doi_cong(cong, han=40):
    t = time.time() + han
    while time.time() < t:
        try:
            socket.create_connection(("127.0.0.1", cong), timeout=1).close(); return True
        except OSError:
            time.sleep(0.4)
    return False


def _get(cong, duong, the=None, ph="GET"):
    h = {"Authorization": f"Bearer {the}"} if the else {}
    if ph == "POST":
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(f"http://127.0.0.1:{cong}{duong}", method=ph, data=b"{}" if ph == "POST" else None, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def _cay_tien_trinh(goc: int) -> list[int]:
    """`goc` và mọi hậu duệ (đi theo ppid trong /proc/*/stat)."""
    con: dict[int, list[int]] = {}
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                ppid = int(open(f"/proc/{d}/stat").read().rsplit(")", 1)[1].split()[1])
            except (OSError, IndexError, ValueError):
                continue
            con.setdefault(ppid, []).append(int(d))
    ra, hang = [], [goc]
    while hang:
        x = hang.pop()
        ra.append(x)
        hang += con.get(x, [])
    return ra


def _the(kho_san, jwt=JWT_GIA):
    r = subprocess.run([sys.executable, str(H.GOC / "tools" / "chay_cua.py"), "--the-tam", "300"],
                       env=dict(os.environ, FLS_JWT_SECRET=jwt, PG_DSN=f"postgresql://x@127.0.0.1:1/{kho_san['kho']}"),
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def _dung(p):
    p.terminate()
    try:
        out, err = p.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        p.kill(); out, err = p.communicate()
    return out, err


def test_vao_sh_che_do_doc_cua_nghe_loopback_401_khong_the_405_ghi(kho_san):
    sv = _may_chu({"fls-staging-jwt-secret": JWT_GIA, "fls-staging-pg-fls_doc": H.MK["fls-staging-pg-fls_doc"],
                   "fls-staging-pg-fls_ghi": H.MK["fls-staging-pg-fls_ghi"]})
    p, cong = _vao(kho_san, sv, "doc")
    try:
        assert _doi_cong(cong), _dung(p)
        assert _get(cong, "/")[0] == 200, "màn hình"
        assert _get(cong, "/api/fls/v1/gates")[0] == 401, "không thẻ ⇒ 401 (fail-closed)"
        the = _the(kho_san)
        ma, than = _get(cong, "/api/fls/v1/gates", the)
        assert ma == 200, than[:200]
        assert _get(cong, "/api/fls/v1/ledger", the)[0] == 200
        # chế độ CHỈ-ĐỌC ⇒ tuyến GHI trả 405 (nhóm ghi TẮT), ⛔ 404/500
        assert _get(cong, "/api/fls/v1/config/fx/202601/sign", the, "POST")[0] == 405
        # chỉ nghe loopback: nối bằng địa chỉ NGOÀI loopback của máy phải bị từ chối
        ip_ngoai = socket.gethostbyname(socket.gethostname())
        if not ip_ngoai.startswith("127."):
            with pytest.raises(OSError):
                socket.create_connection((ip_ngoai, cong), timeout=3)
        # bí mật: ⛔ trong cmdline của BẤT KỲ tiến trình nào thuộc cây của `vao.sh` (đọc /proc; ⛔ quét cả máy —
        # sẽ bắt trúng chính dòng lệnh của người chạy bài thử)
        cay = _cay_tien_trinh(p.pid)
        assert len(cay) >= 3, f"cây tiến trình quá nhỏ ({cay}) — bài vô nghĩa (Đ3)"      # bash + proxy + cửa
        for d in cay:
            try:
                cl = open(f"/proc/{d}/cmdline", "rb").read().decode("utf-8", "ignore")
            except OSError:
                continue
            assert JWT_GIA not in cl and "MKGIA" not in cl, f"bí mật nằm trong cmdline pid {d}"
        # dùng ĐÚNG vai fls_doc và ⛔ đọc fls_ghi
        assert ("du-an-gia", "fls-staging-pg-fls_doc") in sv.da_doc and not [x for x in sv.da_doc if x[1].endswith("fls_ghi")]
    finally:
        out, err = _dung(p)
        sv.shutdown()
    gop = out + err
    assert JWT_GIA not in gop and "MKGIA" not in gop and "TOKEN-GIA" not in gop, "bí mật rò ra log"
    assert "chế độ=doc vai=fls_doc actor=staging-doc" in out


def test_vao_sh_che_do_ghi_mo_nhom_ghi_dung_vai_fls_ghi_va_actor_la_NGUOI_KY(kho_san):
    # nạp config (IX.FX) vào kho scratch bằng ĐÚNG trình nạp của bước 04 ⇒ có tháng để ký
    dsn_ghi = f"postgresql://fls_ghi:{H.MK['fls-staging-pg-fls_ghi']}@127.0.0.1:{H.cong_pg()}/{kho_san['kho']}"
    nap = subprocess.run([sys.executable, str(H.STG / "nap_cau_hinh_ix.py"), "--nguoi-nap", "khanh.thu"],
                         env=dict(os.environ, PG_DSN=dsn_ghi, FLS_CHO_GHI_THAT="1", PYTHONUTF8="1"), capture_output=True, text=True)
    assert nap.returncode == 0, nap.stdout + nap.stderr
    sv = _may_chu({"fls-staging-jwt-secret": JWT_GIA, "fls-staging-pg-fls_doc": H.MK["fls-staging-pg-fls_doc"],
                   "fls-staging-pg-fls_ghi": H.MK["fls-staging-pg-fls_ghi"]})
    p, cong = _vao(kho_san, sv, "ghi", actor="tester.mot")
    try:
        assert _doi_cong(cong), _dung(p)
        # ⭐ thẻ do cửa tự phát cho `--actor` — ⛔ thẻ ta tự đúc: lấy từ màn hình (phien.js) như trình duyệt
        ma_js, js = _get(cong, "/phien.js")
        assert ma_js == 200, js[:200]
        the = re.search(rb'"the"\s*:\s*"([^"]+)"', js) or re.search(rb"'the'\s*:\s*'([^']+)'", js) or re.search(rb"([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)", js)
        assert the, js[:300]
        the = the.group(1).decode()
        ma, than = _get(cong, "/api/fls/v1/config/fx/202401/sign", the, "POST")
        assert ma == 201, (ma, than[:300])                  # tuyến GHI MỞ (⛔ 405) và ký được
        chi_tiet = json.loads(than)["data"]
        assert chi_tiet["actor"] == "tester.mot", f"chữ ký mang tên {chi_tiet['actor']!r} thay vì người ký"
        assert chi_tiet["actor"] != "thu@apero.vn"
        with psycopg.connect(dsn_ghi, autocommit=True) as c:      # và ở KHO: cột actor của bản ký
            actors = {r[0] for r in c.execute("SELECT actor FROM fls_cau_hinh_ban WHERE bang = 'IX.FX · KY'").fetchall()}
        assert actors == {"tester.mot"}, actors
        assert _get(cong, "/api/fls/v1/config/fx/202401/sign", the, "POST")[0] == 409        # ký lại ⇒ 409 có tên
        # kết nối ĐỌC của cửa vẫn chỉ-đọc dù vai là fls_ghi (`noi_chi_doc`): GET không ghi được gì
        assert _get(cong, "/api/fls/v1/ledger", the)[0] == 200
        assert ("du-an-gia", "fls-staging-pg-fls_ghi") in sv.da_doc
    finally:
        out, err = _dung(p)
        sv.shutdown()
    assert "chế độ=ghi vai=fls_ghi actor=tester.mot" in out


def test_vao_sh_che_do_ghi_ma_KHONG_noi_ai_ky_hay_la_ten_mac_dinh_thi_exit_2(kho_san):
    sv = _may_chu({})
    try:
        for actor, loi in ((None, "FLS_STG_ACTOR"), ("", "FLS_STG_ACTOR"), ("thu@apero.vn", "thu@apero.vn"), ("a b", "FLS_STG_ACTOR")):
            p, _ = _vao(kho_san, sv, "ghi", actor=actor)
            out, err = p.communicate(timeout=30)
            assert p.returncode == 2 and loi in err, (actor, p.returncode, err)
        assert sv.da_doc == [], "đã đọc bí mật trước khi kiểm actor"
    finally:
        sv.shutdown()


def test_vao_sh_thieu_khoa_JWT_dung_TRUOC_khi_mo_proxy_hay_kho(kho_san):
    sv = _may_chu({"fls-staging-pg-fls_doc": H.MK["fls-staging-pg-fls_doc"]})       # ⛔ có jwt
    p, cong = _vao(kho_san, sv, "doc")
    try:
        out, err = p.communicate(timeout=60)
    finally:
        sv.shutdown()
    assert p.returncode != 0 and "fls-staging-jwt-secret" in err and "HTTP 404" in err, (out, err)
    assert not _doi_cong(cong, han=1)
    assert [x for x in sv.da_doc] == [], "đã đọc bí mật khác khi thiếu JWT"


def test_vao_sh_che_do_la_exit_2(kho_san):
    sv = _may_chu({})
    try:
        p, _ = _vao(kho_san, sv, "xoa-het")
        out, err = p.communicate(timeout=30)
    finally:
        sv.shutdown()
    assert p.returncode == 2 and "doc|ghi" in err


def test_cua_van_TU_CHOI__thieu_JWT__ngoai_loopback__ket_noi_doc_con_ghi_duoc(kho_san):
    """Ba luật từ chối của cửa (⛔ nới) còn nguyên khi chạy qua `chay_cua.py` thật và qua cổng của nó."""
    dsn = f"postgresql://fls_doc:{H.MK['fls-staging-pg-fls_doc']}@127.0.0.1:{H.cong_pg()}/{kho_san['kho']}"
    base = dict(os.environ, PG_DSN=dsn, PYTHONUTF8="1")
    base.pop("FLS_JWT_SECRET", None)
    chay = [sys.executable, str(H.GOC / "tools" / "chay_cua.py"), "--cho-web", "--cong", str(_cong_trong())]
    # ⓐ thiếu khoá
    r = subprocess.run(chay, env=base, capture_output=True, text=True, timeout=60)
    assert r.returncode != 0 and "FLS_JWT_SECRET" in r.stderr, r.stderr[-400:]
    # ⓑ màn hình ngoài loopback
    r = subprocess.run(chay + ["--dia-chi", "0.0.0.0"], env=dict(base, FLS_JWT_SECRET=JWT_GIA),
                       capture_output=True, text=True, timeout=60)
    assert r.returncode != 0 and "khong phai loopback" in r.stderr and "GAP-WEB-01" in r.stderr, r.stderr[-400:]
    # ⓒ kết nối ĐỌC còn ghi được ⇒ cổng của cửa nổ (đo bằng chính hàm cửa gọi lúc dựng máy)
    from fls.api.cua import kiem_truoc_khi_mo
    with psycopg.connect(f"postgresql://fls_ghi:{H.MK['fls-staging-pg-fls_ghi']}@127.0.0.1:{H.cong_pg()}/{kho_san['kho']}",
                         autocommit=True) as c:
        with pytest.raises(RuntimeError, match="GHI duoc"):
            kiem_truoc_khi_mo(c)


# ══ ⓒ tĩnh ═══════════════════════════════════════════════════════════════════════════════════

def test_tinh_dockerfile_la_DANH_SACH_CHO_PHEP_va_dockerignore_khop():
    df = (H.GOC / "Dockerfile").read_text(encoding="utf-8")
    di = [l.strip() for l in (H.GOC / ".dockerignore").read_text(encoding="utf-8").splitlines()
          if l.strip() and not l.lstrip().startswith("#")]
    cho_phep = [l[1:] for l in di if l.startswith("!")]
    assert di[0] == "*", "`.dockerignore` phải mở đầu bằng `*` (danh sách CHO PHÉP)"
    code = [l for l in df.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    copy = [l.split() for l in code if l.startswith("COPY ")]
    for c in copy:
        if "--from=proxy" in c:
            continue
        src = [x for x in c[1:] if not x.startswith("--")][0]       # bỏ cờ (`--chown=…`)
        assert src not in (".", "./", "*") and not src.startswith(("/", "..")), f"COPY quá rộng: {c}"
        assert any(src.rstrip("/") == a.rstrip("/") for a in cho_phep), f"COPY {src} ⛔ nằm trong `!` của .dockerignore"
    for loai in ("sao_luu", "hien_vat", "Input_Raw", ".env"):
        assert not [a for a in cho_phep if loai in a], loai
        assert any(loai in l for l in di if not l.startswith("!")), f"{loai} phải bị loại tường minh"
    assert not [l for l in code if re.match(r"(ADD|EXPOSE)\b", l)], "⛔ ADD / EXPOSE"
    assert not [l for l in code if re.search(r"(PASSWORD|SECRET|TOKEN|KEY)\s*=", l, re.I) and l.startswith(("ENV", "ARG"))], \
        "⛔ bí mật trong ENV/ARG của ảnh"
    assert any(l.startswith("USER fls") for l in code) and "ENTRYPOINT" in df
    assert re.search(r"cloud-sql-proxy:\d+\.\d+\.\d+", df) and ":latest" not in df, "ghim phiên bản proxy"
    # ⭐ `STG-R2b-01` (lỗi THẬT GCP): bài cũ ở đây đòi `.gcloudignore` == `.dockerignore` — chính tệp ấy làm gcloud lọc mất
    #   106/398 tệp (có Dockerfile). Ngữ cảnh đã là danh sách cho phép (`ngu_canh_build.sh`) ⇒ tệp bị XOÁ; lo gốc (ngữ cảnh
    #   ⛔ mang rác/dữ liệu) giữ nguyên ở `.dockerignore` + bài chim hoàng yến.
    assert not (H.GOC / ".gcloudignore").exists(), "`.gcloudignore` quay lại — gcloud sẽ lọc ngữ cảnh (STG-R2b-01)"


def test_tinh_vm_khoi_dong_va_vao_sh_khong_cong_ra_khong_bi_mat():
    vm = (H.STG / "vm_khoi_dong.sh").read_text(encoding="utf-8")
    vao = (H.STG / "app" / "vao.sh").read_text(encoding="utf-8")
    ma_vm = "\n".join(l for l in vm.splitlines() if not l.lstrip().startswith("#"))
    ma_vao = "\n".join(l for l in vao.splitlines() if not l.lstrip().startswith("#"))
    assert "--network host" in ma_vm and not re.search(r"\s-p\s|--publish|-P\b", ma_vm), "⛔ publish cổng"
    assert "0.0.0.0" not in ma_vm + ma_vao
    assert "--dia-chi 127.0.0.1" in ma_vao
    for m in (ma_vm, ma_vao):
        assert not re.search(r"^\s*set\s+-[a-z]*x", m, re.M)
        assert not re.search(r"postgresql://[^@/\s\"']+:[^@\s\"']+@", m)
    assert "FLS_JWT_SECRET=" in ma_vao and "-e FLS_JWT_SECRET" not in ma_vm and "PGPASSWORD" not in ma_vm
    assert "-e FLS_STG_PROJECT" in ma_vm       # chỉ cấu hình ⛔ bí mật
    assert not re.search(r"-e\s+\S*(PASSWORD|JWT|SECRET|MK)", ma_vm)
    for sh in (S03, H.STG / "vm_khoi_dong.sh", H.STG / "app" / "vao.sh"):
        assert subprocess.run(["bash", "-n", str(sh)]).returncode == 0, sh
    s03 = "\n".join(l for l in S03.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#"))
    assert "--allow-unauthenticated" not in s03 and "allUsers" not in s03 and "allAuthenticatedUsers" not in s03
    nc = (H.STG / "ngu_canh_build.sh").read_text(encoding="utf-8")
    assert "ngu_canh_build.sh" in s03 and "git -C \"$GOC\" archive --format=tar HEAD" in nc \
        and "builds submit \"$CTX\"" in s03, "ngữ cảnh build PHẢI từ git archive (qua ngu_canh_build.sh — STG-R2b-01)"
    assert not re.search(r"builds submit\s+(\.|\"?\$GOC)", s03), "⛔ submit cả thư mục làm việc"


# ══ `STG-R2b-01` · `-04` · `-05` — lỗi THẬT GCP bước 03 (23/11): `.gcloudignore` lọc mất Dockerfile · Cloud Build ⛔ BuildKit ══

def _ngu_canh(goc_rev: str, dich, them_gcloudignore: bool):
    """Ngữ cảnh như bước 03 CŨ ở commit `goc_rev` (có/không `.gcloudignore`)."""
    ds = ["Dockerfile", ".dockerignore", "requirements.txt", "fls", "tools", "docs/ITL/_tools", "tests/fixture"]
    if them_gcloudignore:
        ds.insert(2, ".gcloudignore")
    dich.mkdir()
    a = subprocess.run(["git", "-C", str(H.GOC), "archive", "--format=tar", goc_rev, "--", *ds], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", str(dich)], input=a.stdout, check=True)
    return sum(len(ns) for _, _, ns in os.walk(dich))


def _submit_gia(gcp, ctx):
    env = dict(os.environ, FLS_GIA_TRANG_THAI=str(gcp.tt))
    return subprocess.run([sys.executable, str(GCLOUD_GIA), "--project=du-an-gia", "--quiet", "builds", "submit", str(ctx),
                           "--tag", IMAGE], capture_output=True, text=True, env=env, timeout=60)


def test_gia_gcloudignore_khop_so_do_THAT_GCP_398_ra_292_va_thieu_Dockerfile(gcp, tmp_path):
    """Hiệu chỉnh đồ GIẢ trên SỐ ĐO THẬT (chủ chạy bước 03 ở `c4a0f39`): ngữ cảnh 398 tệp, gcloud tải 292, Cloud Build
    `lstat /workspace/Dockerfile`. Giả cũ "tải" cả 398 ⇒ xanh giả. ⚠ Ngữ nghĩa gitignore THUẦN cho 1 (⛔ 292) — đã đo."""
    n = _ngu_canh("c4a0f39", tmp_path / "ctx", True)
    assert n == 398, n
    r = _submit_gia(gcp, tmp_path / "ctx")
    assert r.returncode == 1 and "Creating temporary archive of 292 file(s)" in r.stderr, r.stderr
    assert "lstat /workspace/Dockerfile: no such file or directory" in r.stderr
    tep = gcp.doc()["builds"][-1]["tep"]
    assert sum(t.startswith("fls/") for t in tep) == 141 and sum(t.startswith("tools/") for t in tep) == 150 \
        and "requirements.txt" in tep and not [t for t in tep if t.startswith(("docs/", "tests/"))], len(tep)


def test_gia_bo_build_CU_tu_choi_RUN_mount_dung_chu_docker(gcp, tmp_path):
    """`gcloud builds submit --tag` = bộ build CŨ. Đo cục bộ `DOCKER_BUILDKIT=0 docker build` (23/11) trên Dockerfile `c4a0f39`:
    `the --mount option requires BuildKit` ở Step 9/16 — ĐÚNG câu Cloud Build in. Giả phải từ chối y vậy."""
    _ngu_canh("c4a0f39", tmp_path / "ctx", False)
    r = _submit_gia(gcp, tmp_path / "ctx")
    assert r.returncode == 1 and "the --mount option requires BuildKit" in r.stderr, r.stderr
    assert "Creating temporary archive of 397 file(s)" in r.stderr     # ⛔ .gcloudignore ⇒ ⛔ lọc gì


def test_tinh_Dockerfile_KHONG_cu_phap_doi_BuildKit_va_co_cong_cu_thu_bo_build_cu():
    df = (H.GOC / "Dockerfile").read_text(encoding="utf-8")
    code = [l.strip() for l in df.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    assert not [l for l in code if re.match(r"RUN\s+--", l)], "RUN --mount/--network/--security đòi BuildKit (STG-R2b-05)"
    assert not [l for l in code if re.match(r"(COPY|ADD)\s.*--(link|parents|exclude|chmod)\b", l)]
    assert not re.search(r"^#\s*syntax\s*=", df, re.M) and not [l for l in code if re.search(r"<<-?\w", l)]
    # CA proxy của máy dev chỉ sống ở tầng `goi`; tầng chạy ⛔ ARG/ENV nào mang nó
    tang = df.split("\nFROM ")
    assert len(tang) >= 4 and "AS goi" in tang[2] and "PIP_CA_PEM" in tang[2], "tầng gói riêng (multi-stage)"
    assert "PIP_CA_PEM" not in tang[-1] and "COPY --from=goi /goi /usr/local" in tang[-1]
    cc = H.STG / "thu_dung_anh.sh"
    assert subprocess.run(["bash", "-n", str(cc)]).returncode == 0 and "DOCKER_BUILDKIT=0 docker build" in cc.read_text(encoding="utf-8")


def test_ngu_canh_build_KHONG_co_tep_loc_va_tu_choi_dich_ban(tmp_path):
    d = tmp_path / "ctx"
    d.mkdir()
    r = subprocess.run(["bash", str(H.STG / "ngu_canh_build.sh"), str(H.GOC), str(d)], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    tep = {os.path.relpath(os.path.join(a, n), d) for a, _, ns in os.walk(d) for n in ns}
    assert "Dockerfile" in tep and ".gcloudignore" not in tep and ".gitignore" not in tep and len(tep) > 200
    assert re.search(rf"ngữ cảnh: {len(tep)} tệp, commit [0-9a-f]+", r.stdout), r.stdout
    r2 = subprocess.run(["bash", str(H.STG / "ngu_canh_build.sh"), str(H.GOC), str(d)], capture_output=True, text=True)
    assert r2.returncode == 2 and "NGU_CANH_DICH_BAN" in r2.stderr


def test_ngu_canh_build_repo_CHUA_commit_thi_loi_CO_TEN__STG_R2b_04(tmp_path):
    g = tmp_path / "repo"
    subprocess.run(["git", "init", "-q", str(g)], check=True)
    (tmp_path / "ctx").mkdir()
    r = subprocess.run(["bash", str(H.STG / "ngu_canh_build.sh"), str(g), str(tmp_path / "ctx")], capture_output=True, text=True)
    assert r.returncode == 2 and "NGU_CANH_RONG" in r.stderr, r.stderr


def test_gcloud_loc_mat_Dockerfile_thi_BUILD_LOI_khong_dung_VM_va_BAO_CAO_DO_co_ten(gcp):
    gcp.sua(lambda s: s.__setitem__("bo_tep", ["Dockerfile"]))
    r = gcp.chay()
    assert r.returncode == 1 and "BUILD_LOI" in r.stderr and "BÁO CÁO" in r.stdout, r.stdout + r.stderr
    do = H.muc_do(r.stdout)
    assert {"ngữ cảnh build · tệp tải lên = tệp ngữ cảnh (≠ 0)", "dựng ảnh · gcloud builds submit (exit)", "ảnh có tag mong"} <= do, do
    assert not [d for d in gcp.lenh_da_goi() if d.startswith(("compute instances create", "compute firewall-rules create"))]


def test_gcloud_loc_mat_MOT_tep_ma_build_van_qua_thi_DUNG_muc_dem_ĐỎ(gcp):
    """Mục đếm phải có răng ngay cả khi Cloud Build tình cờ qua (tệp mất ⛔ phải Dockerfile)."""
    gcp.sua(lambda s: s.__setitem__("bo_tep", ["tools/chay_cua.py"]))
    r = gcp.chay()
    assert r.returncode == 1 and H.muc_do(r.stdout) == {"ngữ cảnh build · tệp tải lên = tệp ngữ cảnh (≠ 0)"}, r.stdout
