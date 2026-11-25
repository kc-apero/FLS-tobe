# -*- coding: utf-8 -*-
"""`WO-359` AC-3 — `tools/staging/06_vertex_agent.sh` vs một project GCP GIẢ có trạng thái (`vertex_gia.py`).

HAI đường (chủ 24/11 ~03:50): `google-cloud` (`claude.googleapis.com`, MẶC ĐỊNH) · `vertex` (dự phòng). Mỗi bài chạy cho CẢ
hai (tham số `duong`). Đo: dựng từ trống ⇒ ĐỎ đúng ở bước bấm tay (workspace sai · Model Garden chưa bật) · sửa xong ⇒ ĐẠT ·
chạy lại được (⛔ nhân đôi IAM) · `--kiem` ⛔ lệnh GHI · ĐỎ HAI CHIỀU (mỗi thứ phá ⇒ ĐÚNG mục ĐỎ) · ⛔ token/nội dung trả
lời/workspace đầy đủ trong đầu ra · lệnh trong VM chạy THẬT bằng bash (gcloud giả thi hành `--command`).
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
WS = "wrkspc_01GiaChiDeThuABCDEF"
LINH_CANH = ("TOKGIA-nguoi", "TOKGIA-sa", "NOIDUNG-GIA", "chi tiet GIA", WS)
CAM_GHI = re.compile(r"\b(delete|remove|disable|destroy|set-iam-policy|remove-iam-policy-binding|keys create)\b")
GHI = re.compile(r"^gcloud (services enable|projects add-iam-policy-binding)")
VAI = {"google-cloud": "roles/claude.user", "vertex": "roles/aiplatform.user"}
API = {"google-cloud": "claude.googleapis.com", "vertex": "aiplatform.googleapis.com"}
#: Đường google-cloud cần HAI service (trang Anthropic `anthropic-managed` 24/11: *"Enable two services"*).
API2 = {"google-cloud": "anthropic-managed-claude.cloudpartnerservices.goog", "vertex": None}
SO_MUC = {"google-cloud": 15, "vertex": 14}       # + mục `FLS_NHA_CUNG_CAP = --duong` (orchestrator 24/11)
MO_HINH = ("claude-opus-5-5", "claude-sonnet-5-5")


class Gcp:
    def __init__(self, d: Path, duong: str):
        self.d, self.tt, self.duong = d, d / "tt.json", duong
        for ten in ("gcloud", "curl"):
            shutil.copy(GIA, d / ten)
            (d / ten).chmod(0o755)
        self.dat({"project": DU_AN, "sa": SA, "apis": [], "iam": [], "model_garden": [], "workspace": WS,
                  "vm": {"sa": SA, "scopes": [CP]}})

    def doc(self):
        return json.loads(self.tt.read_text(encoding="utf-8"))

    def dat(self, s):
        self.tt.write_text(json.dumps(s), encoding="utf-8")

    def sua(self, f):
        s = self.doc()
        f(s)
        self.dat(s)

    def bam_tay(self):
        """Bước bấm tay của đường: vertex ⇒ bật 2 mô hình ở Model Garden; google-cloud ⇒ (workspace đúng sẵn) ⛔ gì."""
        self.sua(lambda s: s.update(model_garden=list(MO_HINH)))

    def lenh(self):
        p = Path(str(self.tt) + ".log")
        return [re.sub(r" --project=\S+ --quiet", "", x) for x in p.read_text(encoding="utf-8").splitlines()] if p.exists() else []

    def urls(self):
        """URL hiệu lực curl giả đã gọi (đọc từ argv HOẶC tệp `-K`) — sổ riêng, ⛔ phải argv."""
        p = Path(str(self.tt) + ".url")
        return p.read_text(encoding="utf-8").splitlines() if p.exists() else []

    def chay(self, *a, du_an=DU_AN, ws=WS, them_duong=True, ncc="__duong__"):
        env = dict(os.environ, PATH=f"{self.d}{os.pathsep}{os.environ['PATH']}", FLS_GIA_TRANG_THAI=str(self.tt))
        env.pop("FLS_GIA_DANH_TINH", None)
        env.pop("FLS_NHA_CUNG_CAP", None)
        if ncc is not None:
            env["FLS_NHA_CUNG_CAP"] = self.duong if ncc == "__duong__" else ncc
        duong = ["--duong", self.duong] if them_duong else []
        env.pop("FLS_CLAUDE_WORKSPACE_ID", None)
        if self.duong == "google-cloud" and ws is not None:     # AG3-R1-06: workspace qua BIẾN, ⛔ argv
            env["FLS_CLAUDE_WORKSPACE_ID"] = ws
        return subprocess.run(["bash", str(S06), "--project", du_an, *duong, *a], capture_output=True, text=True, env=env,
                              timeout=120)


def muc(out: str) -> dict[str, str]:
    """Dòng BÁO CÁO `[ĐẠT|ĐỎ] <tên>  …` ⇒ {tên: ĐẠT|ĐỎ}."""
    return {m.group(2).strip(): m.group(1) for m in re.finditer(r"\[(ĐẠT|ĐỎ)\] (.+?)\s{2,}", out)}


def do_cua(out: str) -> set[str]:
    return {k for k, v in muc(out).items() if v == "ĐỎ"}


def goi(nhan_ng: str, m: str, k: str = "HTTP") -> str:
    return f"{'Cloud Shell · người chạy' if nhan_ng == 'cs' else 'TRONG VM · SA'} · {m} · " + (
        "HTTP" if k == "HTTP" else "mô hình trả về (= mã ghim)")


TAT_CA_GOI = {goi(n, m, k) for n in ("cs", "vm") for m in MO_HINH for k in ("HTTP", "mo")}


@pytest.fixture(params=["google-cloud", "vertex"])
def g(tmp_path, request):
    return Gcp(tmp_path, request.param)


def test_mac_dinh_la_google_cloud(tmp_path):
    gg = Gcp(tmp_path, "google-cloud")
    r = gg.chay(them_duong=False)
    assert "══ đường google-cloud" in r.stdout and r.returncode == 0, r.stdout + r.stderr
    assert any("claude.googleapis.com/v1/projects/fp-a-project/locations/global/workspaces/" in x for x in gg.urls())


def test_dung_tu_trong__DO_dung_buoc_bam_tay_roi_DAT(g):
    if g.duong == "vertex":
        r = g.chay()                                               # Model Garden chưa bật
        assert "FAILED_PRECONDITION" in r.stdout and "model-garden/claude-opus-5-5?project=fp-a-project" in r.stdout
        assert "FAILED_PRECONDITION ⇒ mô hình CHƯA bật / CHƯA được Anthropic duyệt" in r.stdout      # ĐỎ CÓ TÊN
    else:
        r = g.chay(ws="wrkspc_SaiWorkspace")                       # workspace chép sai
        assert "not_found_error" in r.stdout and "Settings → Workspaces" in r.stdout
        assert "not_found_error ⇒ CHƯA Subscribe/Activate gói Marketplace, workspace sai" in r.stdout
    assert r.returncode == 1, r.stdout + r.stderr
    assert do_cua(r.stdout) == TAT_CA_GOI, do_cua(r.stdout)       # CHỈ 8 mục gọi thử ĐỎ — API + IAM đã dựng ĐẠT
    g.bam_tay()
    r2 = g.chay("--kiem")
    assert r2.returncode == 0, r2.stdout + r2.stderr
    # mục có mong = AC-5 · biến đường · service (1 vertex / 2 google-cloud) · IAM SA · VM-SA · VM-phạm-vi + 2 × 2 × 2 (8)
    assert "KẾT: ĐẠT" in r2.stdout and len(muc(r2.stdout)) == SO_MUC[g.duong] and not do_cua(r2.stdout)
    assert "18/5 · end_turn" in r2.stdout                         # số token đọc được (⛔ nội dung)
    assert f"API {API[g.duong]} bật" in muc(r2.stdout)


def test_kiem__KHONG_lenh_ghi_va_chay_lai_KHONG_nhan_doi(g):
    g.bam_tay()
    r = g.chay("--kiem")
    assert r.returncode == 1                                       # API chưa bật, IAM chưa cấp ⇒ ĐỎ
    assert not [x for x in g.lenh() if GHI.match(x)]
    assert {f"API {API[g.duong]} bật", f"SA có {VAI[g.duong]} ở project (⛔ điều kiện)"} <= do_cua(r.stdout)
    g.chay()
    g.chay()
    assert g.doc()["iam"] == [{"role": VAI[g.duong], "members": [f"serviceAccount:{SA}"]}]
    assert g.doc()["apis"] == [x for x in (API[g.duong], API2[g.duong]) if x]
    assert not [x for x in g.lenh() if CAM_GHI.search(x)]


def test_KHONG_in_token_noi_dung_workspace(g):
    g.bam_tay()
    r = g.chay()
    assert r.returncode == 0, r.stdout
    for lc in LINH_CANH:
        assert lc not in r.stdout + r.stderr, lc
    assert any(x.startswith("https://") for x in g.urls())   # lời gọi THẬT đã đi (lính canh vắng vì ⛔ in)
    if g.duong == "google-cloud":
        assert f"wrkspc_…({len(WS)} ký tự)" in r.stdout                 # chỉ tiền tố + độ dài


PHA = [
    ("mo_hinh_thieu", {goi("cs", "claude-sonnet-5-5"), goi("vm", "claude-sonnet-5-5")}),
    ("vm_pham_vi", {"VM phạm vi OAuth có cloud-platform", goi("vm", "claude-opus-5-5"), goi("vm", "claude-sonnet-5-5")}),
    ("vm_mat", {"VM tồn tại · chạy bằng SA", "VM phạm vi OAuth có cloud-platform",
                goi("vm", "claude-opus-5-5"), goi("vm", "claude-sonnet-5-5")}),
    ("phuc_vu_khac", {goi("cs", "claude-opus-5-5", "mo"), goi("vm", "claude-opus-5-5", "mo")}),
    ("chua_dang_nhap", {goi("cs", "claude-opus-5-5"), goi("cs", "claude-sonnet-5-5")}),
    ("ssh_hong", {goi("vm", "claude-opus-5-5"), goi("vm", "claude-sonnet-5-5")}),
    ("iam_go", {"SA có {vai} ở project (⛔ điều kiện)", goi("vm", "claude-opus-5-5"), goi("vm", "claude-sonnet-5-5")}),
    ("api_tat", {"API {api} bật"} | {goi(n, m) for n in ("cs", "vm") for m in MO_HINH}),
]


def _pha(s, ten, duong):
    if ten == "mo_hinh_thieu":
        if duong == "vertex":
            s["model_garden"].remove("claude-sonnet-5-5")
        else:
            s["to_chuc_mo_hinh"] = ["claude-opus-5-5"]   # tổ chức Anthropic ⛔ được dùng Sonnet 5.5
    elif ten == "vm_pham_vi":
        s["vm"] = {"sa": SA, "scopes": ["https://www.googleapis.com/auth/devstorage.read_only"]}
    elif ten == "vm_mat":
        s["vm"] = None
    elif ten == "phuc_vu_khac":
        s["phuc_vu"] = {"claude-opus-5-5": "claude-opus-5"}
    elif ten == "chua_dang_nhap":
        s["dang_nhap"] = False
    elif ten == "ssh_hong":
        s["ssh_duoc"] = False
    elif ten == "iam_go":
        s["iam"] = []
    elif ten == "api_tat":
        s["apis"] = []


@pytest.mark.parametrize("ten,mong_do", PHA, ids=[p[0] for p in PHA])
def test_DO_hai_chieu__pha_tung_thu__DUNG_muc_DO(g, ten, mong_do):
    g.bam_tay()
    assert g.chay().returncode == 0                                # nền ĐẠT
    g.sua(lambda s: _pha(s, ten, g.duong))
    r = g.chay("--kiem")
    assert r.returncode == 1
    mong = {x.format(vai=VAI[g.duong], api=API[g.duong]) for x in mong_do}
    if ten == "api_tat" and API2[g.duong]:
        mong.add(f"API {API2[g.duong]} bật (Marketplace)")
    do = do_cua(r.stdout)
    # mục "mô hình trả về" ĐỎ kèm khi HTTP ≠ 200 — chỉ so tập HTTP/hạ tầng, trừ ca phá chính mục ấy
    if ten != "phuc_vu_khac":
        do = {k for k in do if "mô hình trả về" not in k}
    assert do == mong, (do, mong)


def test_google_cloud__nguoi_chay_thieu_vai__DO_chi_Cloud_Shell__cap_nguoi_sua(tmp_path):
    gg = Gcp(tmp_path, "google-cloud")
    gg.sua(lambda s: s.update(nguoi_quyen=False))
    r = gg.chay()
    assert {goi("cs", m) for m in MO_HINH} <= do_cua(r.stdout)
    assert not {goi("vm", m) for m in MO_HINH} & do_cua(r.stdout)
    r2 = gg.chay("--cap-nguoi", "chu.du.an@vi-du.vn")
    assert "người chạy (--cap-nguoi) có roles/claude.user" in muc(r2.stdout)
    assert any(x.startswith("gcloud projects add-iam-policy-binding") and "user:chu.du.an@vi-du.vn" in x for x in gg.lenh())


def test_khong_goi_thu__muc_goi_thu_la_DO_khong_phai_bo_qua(g):
    g.bam_tay()
    g.chay()
    truoc = len(g.lenh())
    r = g.chay("--kiem", "--khong-goi-thu")
    assert r.returncode == 1 and do_cua(r.stdout) == TAT_CA_GOI        # Đ5: ⛔ đo được ⇒ ĐỎ
    moi = g.lenh()[truoc:]
    assert len(moi) == 3 and not any(x.startswith("curl ") or " ssh " in x for x in moi), moi   # 3 lệnh ĐỌC, ⛔ gọi


@pytest.mark.parametrize("vung", ["us", "eu"])
def test_vertex_da_vung__dung_host_rep(tmp_path, vung):
    gg = Gcp(tmp_path, "vertex")
    gg.bam_tay()
    r = gg.chay("--region", vung)
    assert r.returncode == 0, r.stdout
    assert f"aiplatform.{vung}.rep.googleapis.com/v1/projects/{DU_AN}/locations/{vung}/" in "\n".join(gg.urls())


@pytest.mark.parametrize("a,duong", [
    (["--region", "asia-southeast1"], "vertex"), (["--region", "us-east5"], "vertex"), (["--vm", "X;rm"], "vertex"),
    (["--la"], "vertex"), (["--region", "us"], "google-cloud"), (["--cap-nguoi", "khong-phai-email"], "google-cloud"),
])
def test_tham_so_xau__exit_2_truoc_moi_lenh(tmp_path, a, duong):
    gg = Gcp(tmp_path, duong)
    r = gg.chay(*a)
    assert r.returncode == 2 and not gg.lenh(), r.stderr


@pytest.mark.parametrize("ws", ["", "ws_123", "wrkspc_a;b", "wrkspc_", "wrkspc_é", "wrkspc____", "WRKSPC_x", None])
def test_google_cloud_workspace_xau__exit_2(tmp_path, ws):
    gg = Gcp(tmp_path, "google-cloud")
    r = gg.chay(ws=ws)
    assert r.returncode == 2 and not gg.lenh()


def test_project_khac_cong_ty__DO_muc_AC5(g):
    g.sua(lambda s: s.update(project="du-an-khac"))
    g.bam_tay()
    r = g.chay(du_an="du-an-khac")
    assert "project = GCP công ty (fp-a-project — AC-5)" in do_cua(r.stdout)


def test_moi_lenh_cap_vai_muc_project__co_condition_None():
    """Orchestrator đo 24/11: IAM `fp-a-project` có binding CÓ ĐIỀU KIỆN ⇒ `add-iam-policy-binding` thiếu `--condition=None`
    dừng ở câu hỏi tương tác. Mong: số lệnh có cờ = tổng số lệnh (và tổng ≥ 1 — Đ3)."""
    van = S06.read_text(encoding="utf-8")
    lenh = re.findall(r'projects add-iam-policy-binding[^\n]*\n?[^\n]*', van)
    assert len(lenh) == 2 and sum("--condition=None" in x for x in lenh) == len(lenh), lenh


def test_google_cloud__chi_bat_service_claude__thieu_Marketplace_van_DO(tmp_path):
    """Thiếu service Marketplace ⇒ mục ấy ĐỎ dù lời gọi (giả định G2) vẫn 200 — ⛔ coi 'gọi được' là đủ."""
    gg = Gcp(tmp_path, "google-cloud")
    gg.chay()
    gg.sua(lambda s: s.update(apis=["claude.googleapis.com"]))
    r = gg.chay("--kiem")
    assert do_cua(r.stdout) == {"API anthropic-managed-claude.cloudpartnerservices.goog bật (Marketplace)"}


@pytest.mark.parametrize("ncc", [None, "", "anthropic", "khac"])
def test_bien_FLS_NHA_CUNG_CAP_vang_hoac_lech__DO_co_ten(g, ncc):
    """Orchestrator 24/11: biến VẮNG ⇒ mã agent đi đường khoá API ⇒ 06 phải ĐỎ (⛔ coi vắng là đúng)."""
    g.bam_tay()
    r = g.chay(ncc=ncc)
    assert do_cua(r.stdout) == {"biến FLS_NHA_CUNG_CAP của shell = --duong (vắng ⇒ agent đi đường khoá API)"}, do_cua(r.stdout)
    assert r.returncode == 1


def test_AG3_R1_06__argv_moi_lenh_gia__0_lan_wrkspc(tmp_path):
    """Workspace ID ⛔ trong argv của BẤT KỲ lệnh nào (gcloud · curl · ssh) — đo trên nhật ký argv của lệnh giả;
    mẫu số (Đ3): đã có lời gọi Cloud Shell + lệnh ssh, và workspace THẬT SỰ được dùng (gọi thử 200 ⇒ URL đúng)."""
    gg = Gcp(tmp_path, "google-cloud")
    r = gg.chay()
    assert r.returncode == 0, r.stdout + r.stderr
    lenh = gg.lenh()
    assert sum(x.startswith("curl ") and "-K" in x for x in lenh) >= 2 and any(" ssh " in x for x in lenh)
    assert not [x for x in lenh if "wrkspc_" in x], [x for x in lenh if "wrkspc_" in x]
    assert "bash -s" in next(x for x in lenh if " ssh " in x)


def test_AG3_R1_06__co_workspace_id_trong_argv__exit_2(tmp_path):
    gg = Gcp(tmp_path, "google-cloud")
    r = gg.chay("--workspace-id", WS)
    assert r.returncode == 2 and "AG3-R1-06" in r.stderr and not gg.lenh()


def test_AG3_R1_06__workspace_id_file(tmp_path):
    gg = Gcp(tmp_path, "google-cloud")
    f = tmp_path / "ws.txt"
    f.write_text(WS + "\n", encoding="utf-8")
    f.chmod(0o600)
    r = gg.chay("--workspace-id-file", str(f), ws=None)
    assert r.returncode == 0, r.stdout + r.stderr
