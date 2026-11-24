"""Bài thử bước 07 — `WO-363` AC-3: `tools/staging/07_link_web.sh` vs một project GCP GIẢ có trạng thái.

`gcloud_gia.py` (nhánh Cloud Run · IAP · logging) + `curl_gia.py` (mặt NGOÀI của service). Học từ 3 lỗi THẬT 23/11
(`.gcloudignore` · BuildKit · CREATEROLE): giả ⛔ "cho qua" — nó mô phỏng các hành vi GCP có thể LÀM HỎNG script
(tác tử IAP chưa tồn tại · `--iap` chỉ có ở beta · `allUsers` cũ còn sau `--no-allow-unauthenticated` · ảnh chưa có).
Những gì giả ⛔ thể chứng (trang đăng nhập Google thật, cookie IAP + thẻ FLS cùng lúc) ⇒ giả định có tên ở BG-364.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess

import pytest

from tests.staging import ho_tro as H

S07 = H.STG / "07_link_web.sh"
GCLOUD_GIA = H.GOC / "tests" / "staging" / "gcloud_gia.py"
CURL_GIA = H.GOC / "tests" / "staging" / "curl_gia.py"
TAG = "thu-tag"
IMAGE = f"asia-southeast1-docker.pkg.dev/du-an-gia/fls/fls-app:{TAG}"
CHU = "chu-gia@vi-du.vn"
TAC_TU = "serviceAccount:service-123456789012@gcp-sa-iap.iam.gserviceaccount.com"
# Lệnh GHI được phép của bước 07 — ngoài tập này là phạm vi lạ (VM, firewall, Cloud SQL, xoá…)
GHI_CHO_PHEP = ("services enable", "services identity create", "builds submit", "run deploy", "beta run deploy",
                "run services add-iam-policy-binding", "run services remove-iam-policy-binding",
                "iap web add-iam-policy-binding")
DOC = ("config get-value", "projects describe", "services list", "artifacts docker images list", "sql instances describe",
       "run services describe", "run services get-iam-policy", "iap web get-iam-policy", "logging read",
       "secrets describe", "secrets get-iam-policy")
SA_APP = "serviceAccount:fls-staging-app@du-an-gia.iam.gserviceaccount.com"
DN_DA_DAT = {"fls-staging-login": {"versions": ['{"ten": "HondurasGesha", "bam": "scrypt$16384$8$1$gia$gia"}'],
                                   "iam": [{"role": "roles/secretmanager.secretAccessor", "members": [SA_APP]}]}}


class Gcp:
    def __init__(self, thu_muc, **them):
        self.dir = thu_muc
        self.tt = thu_muc / "trang_thai.json"
        self.log = thu_muc / "trang_thai.json.log"
        self.curl_log = thu_muc / "trang_thai.json.curl.log"
        for src, ten in ((GCLOUD_GIA, "gcloud"), (CURL_GIA, "curl")):
            shutil.copy(src, thu_muc / ten)
            (thu_muc / ten).chmod(0o755)
        s = {"apis": [], "conn": "du-an-gia:asia-southeast1:fls-staging", "repo": True, "repo_iam": [], "anh_tags": [TAG],
             "builds": [], "vm": None, "quyen": [], "ssh_ra": "", "fw": [], "tai_khoan": CHU,
             "secrets": json.loads(json.dumps(DN_DA_DAT))}      # như chủ đã chạy 08 trước 07
        s.update(them)
        self.dat(s)

    def doc(self):
        return json.loads(self.tt.read_text(encoding="utf-8"))

    def dat(self, s):
        self.tt.write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")

    def sua(self, f):
        s = self.doc()
        f(s)
        self.dat(s)

    def lenh(self):
        if not self.log.exists():
            return []
        return [re.sub(r"^--project=\S+ --quiet ", "", d) for d in self.log.read_text(encoding="utf-8").splitlines()]

    def chay(self, *args, tag=TAG):
        env = dict(os.environ, PATH=f"{self.dir}{os.pathsep}{os.environ['PATH']}", FLS_GIA_TRANG_THAI=str(self.tt),
                   PYTHONUTF8="1")
        return subprocess.run(["bash", str(S07), "--project", "du-an-gia", *(["--tag", tag] if tag else []), *args],
                              capture_output=True, text=True, env=env, timeout=300)


@pytest.fixture
def gcp(tmp_path):
    return Gcp(tmp_path)


def _ghi(lenh):
    return [l for l in lenh if not l.startswith(DOC)]


def test_dung_tu_trong_ra_DAT_va_in_LINK(gcp):
    r = gcp.chay("--cho-vao", "nguoi1@vi-du.vn,nguoi2@vi-du.vn")
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]
    assert "KẾT: ĐẠT" in r.stdout and not H.muc_do(r.stdout)
    assert "⭐ LINK: https://fls-staging-web-gia123-as.a.run.app" in r.stdout
    n_dat = len([k for k, v in H.dong_bao_cao(r.stdout).items() if v == "ĐẠT"])
    assert n_dat == 29, f"số mục có `mong` = {n_dat} (mong 29: 28 mục + `run deploy (exit)`) — đổi thì ghi lại bản khai"
    s = gcp.doc()
    vao = {m for b in s["iap_iam"] if b["role"] == "roles/iap.httpsResourceAccessor" for m in b["members"]}
    assert vao == {f"user:{CHU}", "user:nguoi1@vi-du.vn", "user:nguoi2@vi-du.vn"}
    assert [b for b in s["run_iam"] if b["role"] == "roles/run.invoker"] == [{"role": "roles/run.invoker", "members": [TAC_TU]}]


def test_chi_goi_lenh_GHI_dung_danh_sach__tac_tu_TRUOC_khi_gan_quyen__deploy_co_IAP_va_KHONG_cong_khai(gcp):
    r = gcp.chay()
    assert r.returncode == 0, r.stdout[-2000:]
    ghi = _ghi(gcp.lenh())
    la = [l for l in ghi if not l.startswith(GHI_CHO_PHEP)]
    assert not la, f"lệnh GHI ngoài phạm vi bước 07: {la}"
    assert not [l for l in gcp.lenh() if re.search(r"\b(compute|firewall|sql users|delete)\b", l)], "⛔ đụng VM/firewall/vai SQL/xoá"
    i_tt = next(i for i, l in enumerate(ghi) if l.startswith("services identity create"))
    i_inv = next(i for i, l in enumerate(ghi) if l.startswith("run services add-iam-policy-binding"))
    assert i_tt < i_inv, "tác tử IAP phải được TẠO trước khi gán run.invoker (GCP: 'does not exist')"
    dep = next(l for l in ghi if l.startswith("run deploy"))
    for c in ("--iap", "--no-allow-unauthenticated", "--max-instances=1", "--port=8080", "--ingress=all",
              "--args=/app/tools/staging/app/vao_cloud_run.sh", "--service-account=fls-staging-app@du-an-gia.iam.gserviceaccount.com"):
        assert c in dep.split(), f"deploy thiếu {c}: {dep}"
    assert "--allow-unauthenticated" not in dep.split()
    assert "builds submit" not in " ".join(ghi), "tag đã có ⇒ ⛔ dựng lại ảnh"
    # đo NGOÀI ⛔ mang cookie/header nào (đúng vai một trình duyệt lạ)
    for l in gcp.curl_log.read_text(encoding="utf-8").splitlines():
        assert " -H " not in f" {l} " and "--cookie" not in l and " -b " not in f" {l} ", l


def test_kiem_chi_goi_lenh_DOC_va_khong_doi_trang_thai(gcp):
    gcp.chay()
    truoc = gcp.tt.read_text(encoding="utf-8")
    gcp.log.unlink()
    r = gcp.chay("--kiem")
    assert r.returncode == 0, r.stdout[-2000:]
    assert _ghi(gcp.lenh()) == [], _ghi(gcp.lenh())
    assert gcp.tt.read_text(encoding="utf-8") == truoc


def test_chay_lai_duoc_va_khong_nhan_doi_quyen(gcp):
    assert gcp.chay().returncode == 0
    r = gcp.chay()
    assert r.returncode == 0, r.stdout[-2000:]
    # revision mới ⇒ dòng TU_DO MỚI phải khớp revision đang chạy (⛔ đọc dòng cũ)
    assert H.dong_bao_cao(r.stdout)["TRONG container · dòng TU_DO của revision đang chạy"] == "ĐẠT"


def test_tag_CHUA_co_thi_dung_anh_y_buoc_03_va_dem_ngu_canh(gcp):
    r = gcp.chay(tag="moi-tag")
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]
    b = gcp.doc()["builds"]
    assert len(b) == 1 and b[0]["tag"].endswith(":moi-tag") and "Dockerfile" in b[0]["tep"]
    assert "tools/staging/app/cong_iap.py" in b[0]["tep"] and "tools/staging/app/vao_cloud_run.sh" in b[0]["tep"]
    assert H.dong_bao_cao(r.stdout)["ngữ cảnh build · tệp tải lên = tệp ngữ cảnh (≠ 0)"] == "ĐẠT"


def test_build_HONG_thi_KHONG_deploy_va_BAO_CAO_do_co_ten(gcp):
    gcp.sua(lambda s: s.update(bo_tep=["Dockerfile"]))
    r = gcp.chay(tag="moi-tag")
    assert r.returncode == 1 and "BUILD_LOI" in r.stderr
    assert not [l for l in gcp.lenh() if "run deploy" in l]
    do = H.muc_do(r.stdout)
    assert {"dựng ảnh · gcloud builds submit (exit)", "ngữ cảnh build · tệp tải lên = tệp ngữ cảnh (≠ 0)"} <= do


def test_gcloud_CU_chi_co_iap_o_BETA_thi_thu_lai_bang_beta_va_DAT(gcp):
    gcp.sua(lambda s: s.update(iap_chi_beta=True))
    r = gcp.chay()
    assert r.returncode == 0, r.stdout[-2000:]
    l = gcp.lenh()
    assert any(x.startswith("run deploy") for x in l) and any(x.startswith("beta run deploy") for x in l)
    assert "unrecognized arguments: --iap" in r.stdout + r.stderr


def test_gia_tac_tu_IAP_chua_tao_thi_gan_quyen_DO__gia_co_rang(gcp):
    """Đồ giả phải CẮN đúng lỗi GCP mà ② phòng (Đ5): gán run.invoker cho tác tử chưa tồn tại ⇒ 'does not exist'."""
    gcp.chay()
    gcp.sua(lambda s: s.update(tac_tu_iap=False))
    env = dict(os.environ, FLS_GIA_TRANG_THAI=str(gcp.tt))
    r = subprocess.run([str(gcp.dir / "gcloud"), "run", "services", "add-iam-policy-binding", "fls-staging-web",
                        f"--member={TAC_TU}", "--role=roles/run.invoker"], capture_output=True, text=True, env=env)
    assert r.returncode == 1 and "does not exist" in r.stderr


def test_allUsers_CU_con_lai_thi_GO_va_DAT__kiem_truoc_do_DO(gcp):
    gcp.chay()
    gcp.sua(lambda s: s["run_iam"].append({"role": "roles/run.invoker", "members": ["allUsers"]}))
    rk = gcp.chay("--kiem")
    assert rk.returncode == 1
    assert {"thành viên allUsers/allAuthenticatedUsers (đếm)",
            "đường vào ⛔ qua IAP (đếm: IAP tắt · công khai · 200 khi ⛔ cookie)"} <= H.muc_do(rk.stdout)
    r = gcp.chay()
    assert r.returncode == 0 and "đã GỠ allUsers" in r.stdout, r.stdout[-2000:]
    assert not any("allUsers" in b["members"] for b in gcp.doc()["run_iam"])


def _tat_iap(s):
    del s["run"]["metadata"]["annotations"]["run.googleapis.com/iap-enabled"]
    s["run_iam"].append({"role": "roles/run.invoker", "members": ["allUsers"]})


PHA = [
    ("IAP tắt + công khai", _tat_iap,
     {"IAP bật trên service (chú thích run.googleapis.com/iap-enabled)", "thành viên allUsers/allAuthenticatedUsers (đếm)",
      "NGOÀI · GET / ⛔ cookie ⇒ HTTP", "NGOÀI · GET / ⛔ cookie ⇒ chuyển tới trang Google", "NGOÀI · GET API ⛔ cookie ⇒ HTTP",
      "đường vào ⛔ qua IAP (đếm: IAP tắt · công khai · 200 khi ⛔ cookie)"}),
    ("cửa nghe ra ngoài", lambda s: s.update(nhat_ky=[s["nhat_ky"][-1].replace("nghe_cua=127.0.0.1:8088", "nghe_cua=0.0.0.0:8088")]),
     {"TRONG · cửa CHỈ nghe 127.0.0.1"}),
    ("cổng nhận JWT giả", lambda s: s.update(nhat_ky=[s["nhat_ky"][-1].replace("cong_iap_gia=403", "cong_iap_gia=200")]),
     {"TRONG · cổng: JWT IAP chữ ký GIẢ ⇒ HTTP"}),
    ("cổng cho qua khi ⛔ JWT", lambda s: s.update(nhat_ky=[s["nhat_ky"][-1].replace("cong_khong_iap=403", "cong_khong_iap=200")]),
     {"TRONG · cổng: yêu cầu ⛔ JWT IAP ⇒ HTTP"}),
    ("API mở ⛔ thẻ", lambda s: s.update(nhat_ky=[s["nhat_ky"][-1].replace("api_khong_the=401", "api_khong_the=200")]),
     {"TRONG · API ⛔ thẻ ⇒ HTTP"}),
    ("⛔ lấy được khoá IAP", lambda s: s.update(nhat_ky=[s["nhat_ky"][-1].replace("jwks=3", "jwks=0")]),
     {"TRONG · khoá công khai IAP lấy được (đếm ≥ 1)"}),
    ("dòng TU_DO của revision CŨ", lambda s: s["run"]["status"].update(latestReadyRevisionName="fls-staging-web-00099-moi"),
     {"TRONG container · dòng TU_DO của revision đang chạy"}),
    ("⛔ có dòng TU_DO", lambda s: s.update(nhat_ky=[]),
     {"TRONG container · dòng TU_DO của revision đang chạy", "TRONG · màn hình / qua cửa ⇒ HTTP", "TRONG · API ⛔ thẻ ⇒ HTTP",
      "TRONG · tài khoản đăng nhập FLS lúc khởi động",
      "TRONG · cửa CHỈ nghe 127.0.0.1", "TRONG · cổng: yêu cầu ⛔ JWT IAP ⇒ HTTP", "TRONG · cổng: JWT IAP chữ ký GIẢ ⇒ HTTP",
      "TRONG · khoá công khai IAP lấy được (đếm ≥ 1)"}),
    ("trang lạ ⛔ phải Google", lambda s: s.update(http_ngoai={"GET /": "302 https://dang-nhap-gia.vi-du.vn/x"}),
     {"NGOÀI · GET / ⛔ cookie ⇒ chuyển tới trang Google"}),
    ("app trả 200 khi ⛔ cookie", lambda s: s.update(http_ngoai={"GET /api/fls/v1/gates": "200 "}),
     {"NGOÀI · GET API ⛔ cookie ⇒ HTTP", "đường vào ⛔ qua IAP (đếm: IAP tắt · công khai · 200 khi ⛔ cookie)"}),
    ("⛔ đọc được chính sách IAP", lambda s: s.update(iap_iam_hong=True),
     {"cho vào qua IAP: tài khoản mong có quyền (đếm)"}),
    ("người chạy mất quyền IAP", lambda s: s.update(iap_iam=[]),
     {"cho vào qua IAP: tài khoản mong có quyền (đếm)"}),
    ("ảnh khác tag", lambda s: s["run"]["spec"]["template"]["spec"]["containers"][0].update(image=IMAGE + "x"),
     {"service chạy đúng ảnh mong"}),
    ("bí mật đăng nhập bị xoá", lambda s: s.update(secrets={}),
     {"ĐĂNG NHẬP · bí mật fls-staging-login có (chạy 08 trước)", "ĐĂNG NHẬP · SA đọc được bí mật đăng nhập"}),
    ("SA mất quyền đọc bí mật đăng nhập", lambda s: s["secrets"]["fls-staging-login"].update(iam=[]),
     {"ĐĂNG NHẬP · SA đọc được bí mật đăng nhập"}),
    ("chạy 2 instance", lambda s: s["run"]["spec"]["template"]["metadata"]["annotations"].update(
        {"autoscaling.knative.dev/maxScale": "2"}), {"số instance tối đa (MỘT thẻ chung)"}),
]


@pytest.mark.parametrize("ten,pha,mong_do", PHA, ids=[p[0] for p in PHA])
def test_pha_mot_thu_thi_DUNG_muc_do__kiem(gcp, ten, pha, mong_do):
    assert gcp.chay().returncode == 0
    gcp.sua(pha)
    r = gcp.chay("--kiem")
    assert r.returncode == 1, r.stdout[-1500:]
    assert H.muc_do(r.stdout) == mong_do, f"{ten}: {H.muc_do(r.stdout) ^ mong_do}"


def test_project_TRONG_thi_kiem_DO_het_khong_muc_nao_xanh_suong__D3_D5(tmp_path):
    g = Gcp(tmp_path, anh_tags=[], tai_khoan="", secrets={})
    r = g.chay("--kiem")
    assert r.returncode == 1
    assert [k for k, v in H.dong_bao_cao(r.stdout).items() if v == "ĐẠT"] == []
    assert len(H.muc_do(r.stdout)) == 28


def test_che_do_ghi_dat_actor_NGUOI_KY(gcp):
    r = gcp.chay("--che-do", "ghi", "--nguoi-ky", "nguoi.ky")
    assert r.returncode == 0, r.stdout[-1500:]
    env = {x["name"]: x["value"] for x in gcp.doc()["run"]["spec"]["template"]["spec"]["containers"][0]["env"]}
    assert env["FLS_STG_CHE_DO"] == "ghi" and env["FLS_STG_ACTOR"] == "nguoi.ky"
    assert env["FLS_STG_CONN"] == "du-an-gia:asia-southeast1:fls-staging"
    assert not [k for k in env if re.search(r"(?i)secret|pass|jwt|dsn", k)], "⛔ bí mật trong biến môi trường service"


def test_BAO_CAO_va_toan_bo_dau_ra_KHONG_co_email(gcp):
    r = gcp.chay("--cho-vao", "nguoi1@vi-du.vn")
    assert r.returncode == 0
    assert CHU not in r.stdout + r.stderr and "nguoi1@vi-du.vn" not in r.stdout + r.stderr


@pytest.mark.parametrize("args,loi", [
    (["--che-do", "ghi"], "--nguoi-ky"),
    (["--nguoi-ky", "thu@apero.vn"], "thu@apero.vn"),
    (["--cho-vao", "khong-phai-email"], "--cho-vao"),
    (["--cho-vao", "a@b.vn,"], "--cho-vao"),
    (["--cho-vao", "a@b.vn;rm -rf /"], "--cho-vao"),
    (["--service", "Ten_Hoa"], "--service"),
    (["--che-do", "xoa"], "--che-do"),
])
def test_tham_so_xau_exit_2_va_khong_goi_gcloud(gcp, args, loi):
    r = gcp.chay(*args)
    assert r.returncode == 2 and loi in r.stderr, r.stderr
    assert gcp.lenh() == []


def test_thieu_project_exit_2():
    r = subprocess.run(["bash", str(S07)], capture_output=True, text=True)
    assert r.returncode == 2 and "--project" in r.stderr


def test_CHUA_chay_08_truoc_07_thi_DO_dung_3_muc_dang_nhap_co_ten(tmp_path):
    g = Gcp(tmp_path, secrets={})
    r = g.chay()
    assert r.returncode == 1
    assert H.muc_do(r.stdout) == {"ĐĂNG NHẬP · bí mật fls-staging-login có (chạy 08 trước)",
                                  "ĐĂNG NHẬP · SA đọc được bí mật đăng nhập",
                                  "TRONG · tài khoản đăng nhập FLS lúc khởi động"}
