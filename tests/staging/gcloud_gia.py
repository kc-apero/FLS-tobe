#!/usr/bin/env python3
"""`gcloud` GIẢ CÓ TRẠNG THÁI — mô phỏng MỘT project GCP đủ cho `tools/staging/03_dung_app.sh`.

Trạng thái ở `$FLS_GIA_TRANG_THAI` (JSON). Mỗi lệnh GHI đổi trạng thái; mỗi lệnh ĐỌC trả đúng khuôn JSON/`value()`
mà script đọc. Lệnh LẠ ⇒ exit 99 (một lệnh script gọi mà giả ⛔ biết là một lỗi của bài thử, không phải "cho qua").
`builds submit` GHI LẠI danh sách tệp của ngữ cảnh build — bài thử dùng nó để chứng minh dữ liệu gitignore ⛔ lên.
Mọi lệnh gọi được ghi vào `<trang_thai>.log` (một dòng/lệnh) để bài thử đếm lệnh GHI.
"""
import json
import os
import re
import sys

TT = os.environ["FLS_GIA_TRANG_THAI"]
args = sys.argv[1:]
with open(TT + ".log", "a", encoding="utf-8") as f:
    f.write(" ".join(args) + "\n")
S = json.load(open(TT, encoding="utf-8"))
a = [x for x in args if not x.startswith("--project=") and x != "--quiet"]


def luu():
    json.dump(S, open(TT, "w", encoding="utf-8"), ensure_ascii=False)


def co(flag):
    """`--cờ=giá-trị` HOẶC `--cờ giá-trị` (gcloud nhận cả hai)."""
    for i, x in enumerate(a):
        if x.startswith(flag + "="):
            return x.split("=", 1)[1]
        if x == flag and i + 1 < len(a):
            return a[i + 1]
    return None


def lenh(*t):
    return tuple(a[:len(t)]) == t


def xuat_json(o):
    print(json.dumps(o))


def kv(chuoi):
    return dict(p.split("=", 1) for p in chuoi.split(",") if "=" in p)


def _mau_re(mau):
    """Một mẫu `.gcloudignore` → regex khớp CẢ đường dẫn tương đối: `**` = 0..n thành phần, `*`/`?` ⛔ qua `/`."""
    mau = mau.strip("/")
    tp = []
    for i, phan in enumerate(mau.split("/")):
        if phan == "**":
            tp.append("(?:[^/]+/)*" if i < len(mau.split("/")) - 1 else ".*")
            continue
        r = "".join("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c) for c in phan)
        tp.append(r + ("/" if i < len(mau.split("/")) - 1 else ""))
    return re.compile("^" + "".join(tp).replace("(?:[^/]+/)*/", "(?:[^/]+/)*") + "$")


def _gcloud_tai_len(ctx, tat_ca):
    """Tập tệp gcloud TẢI LÊN. Không `.gcloudignore` ⇒ mặc định của gcloud (bỏ `.gcloudignore` · `.git` · `.gitignore`).
    Có ⇒ với MỖI tiền tố đường dẫn (`fls`, `fls/api`, `fls/api/cua.py`), mẫu khớp SAU CÙNG quyết; một tiền tố bị BỎ ⇒ tệp bị bỏ.
    ⚠ ⛔ phải ngữ nghĩa gitignore thuần (đo: gitignore thuần cho 1/398, GCP thật 292/398) — xem `ngu_canh_build.sh`."""
    p = os.path.join(ctx, ".gcloudignore")
    if os.path.exists(os.path.join(ctx, ".gitignore")):
        print("gcloud GIẢ: ⛔ mô phỏng `#!include:.gitignore` — ngữ cảnh ⛔ được có .gitignore", file=sys.stderr)
        sys.exit(99)
    dong = open(p, encoding="utf-8").read().splitlines() if os.path.exists(p) else [".gcloudignore", ".git", ".gitignore"]
    mau = [(l.startswith("!"), _mau_re(l.lstrip("!"))) for l in (x.strip() for x in dong) if l and not l.startswith("#")]
    giu = []
    for t in tat_ca:
        phan = t.split("/")
        bo = False
        for k in range(1, len(phan) + 1):
            tien_to, qd = "/".join(phan[:k]), None
            for mo_lai, rx in mau:
                if rx.match(tien_to):
                    qd = "giu" if mo_lai else "bo"
            if qd == "bo":
                bo = True
                break
        if not bo:
            giu.append(t)
    return giu


def _can_buildkit(df):
    """Bộ build CŨ (⛔ BuildKit) — đúng chữ docker in. Đo `DOCKER_BUILDKIT=0 docker build` 23/11: `RUN --mount` ⇒ câu dưới."""
    for l in df.splitlines():
        s = l.strip()
        if re.match(r"RUN\s+--(mount|network|security)\b", s):
            return f"the --{re.match(r'RUN\s+--(\w+)', s).group(1)} option requires BuildKit. Refer to https://docs.docker.com/go/buildkit/"
        if re.match(r"(COPY|ADD)\s+.*--(link|parents|exclude)\b", s) or re.match(r"#\s*syntax\s*=", s) or re.search(r"<<-?\w", s):
            return "the instruction requires BuildKit. Refer to https://docs.docker.com/go/buildkit/"
    return None


if lenh("services", "enable"):
    for x in a[2:]:
        if x not in S["apis"]:
            S["apis"].append(x)
    luu()
elif lenh("services", "list"):
    print("\n".join(S["apis"]))
elif lenh("sql", "instances", "describe"):
    print(S["conn"])
elif lenh("artifacts", "repositories", "describe"):
    if not S["repo"]:
        sys.exit(1)
    print("projects/p/locations/l/repositories/" + a[3])
elif lenh("artifacts", "repositories", "create"):
    S["repo"] = True
    luu()
elif lenh("artifacts", "repositories", "add-iam-policy-binding"):
    S["repo_iam"].append({"role": co("--role"), "members": [co("--member")]})
    luu()
elif lenh("artifacts", "repositories", "get-iam-policy"):
    xuat_json({"bindings": S["repo_iam"]})
elif lenh("artifacts", "docker", "images", "list"):
    print("\n".join(S["anh_tags"]))
elif lenh("builds", "submit"):
    # ⭐ `STG-R2b-01` · `-05` (lỗi THẬT GCP 23/11): giả cũ "tải" MỌI tệp ngữ cảnh và "dựng" mọi Dockerfile ⇒ xanh giả hai lần.
    #   Nay mô phỏng ĐÚNG hai hành vi đã đo: ① gcloud lọc ngữ cảnh bằng `.gcloudignore` (mô hình `_gcloud_tai_len`,
    #   hiệu chỉnh trên số đo thật 398 → 292 — bài `test_gia_gcloudignore_khop_so_do_THAT_GCP`) và in dòng
    #   `Creating temporary archive of N file(s)`; ② `--tag` = bộ build CŨ: ⛔ Dockerfile ⇒ `lstat`; cú pháp BuildKit ⇒ đỏ.
    ctx = a[2]
    tat_ca = sorted(os.path.relpath(os.path.join(d, n), ctx) for d, _, ns in os.walk(ctx) for n in ns)
    tep = [t for t in _gcloud_tai_len(ctx, tat_ca) if t not in S.get("bo_tep", [])]   # `bo_tep`: bài phá — gcloud "lọc mất" tệp
    print(f"Creating temporary archive of {len(tep)} file(s) totalling 1.0 MiB before compression.", file=sys.stderr)
    S["builds"].append({"tag": co("--tag"), "tep": tep, "ngu_canh": len(tat_ca)})
    luu()
    if "Dockerfile" not in tep:
        print("ERROR: build step 0 \"gcr.io/cloud-builders/docker\" failed: unable to prepare context: unable to evaluate "
              "symlinks in Dockerfile path: lstat /workspace/Dockerfile: no such file or directory", file=sys.stderr)
        sys.exit(1)
    loi = _can_buildkit(open(os.path.join(ctx, "Dockerfile"), encoding="utf-8").read())
    if loi:
        print(loi, file=sys.stderr)
        print("ERROR: build step 0 \"gcr.io/cloud-builders/docker\" failed: step exited with non-zero status: 1", file=sys.stderr)
        sys.exit(1)
    S["anh_tags"].append(co("--tag").rsplit(":", 1)[1])
    luu()
elif lenh("compute", "firewall-rules", "describe"):
    if not any(r["name"] == a[3] for r in S["fw"]):
        sys.exit(1)
elif lenh("compute", "firewall-rules", "create"):
    act = co("--action")
    r = {"name": a[3], "direction": co("--direction"), "priority": int(co("--priority")),
         "sourceRanges": co("--source-ranges").split(","), "targetTags": co("--target-tags").split(","),
         "disabled": False}
    r["allowed" if act == "ALLOW" else "denied"] = [{"IPProtocol": "all"}]
    S["fw"].append(r)
    luu()
elif lenh("compute", "firewall-rules", "list"):
    xuat_json(S["fw"])
elif lenh("compute", "instances", "describe"):
    if not S["vm"]:
        sys.exit(1)
    xuat_json(S["vm"])
elif lenh("compute", "instances", "create"):
    md = kv(co("--metadata"))
    md["startup-script"] = open(kv(co("--metadata-from-file"))["startup-script"], encoding="utf-8").read()
    S["vm"] = {"name": a[3], "status": "RUNNING", "machineType": co("--machine-type"),
               "serviceAccounts": [{"email": co("--service-account")}],
               "tags": {"items": co("--tags").split(",")},
               "metadata": {"items": [{"key": k, "value": v} for k, v in md.items()]},
               "networkInterfaces": [{"accessConfigs": [{"natIP": "203.0.113.7"}]}]}
    luu()
elif lenh("compute", "instances", "add-metadata"):
    for k, v in kv(co("--metadata")).items():
        for i in S["vm"]["metadata"]["items"]:
            if i["key"] == k:
                i["value"] = v
                break
        else:
            S["vm"]["metadata"]["items"].append({"key": k, "value": v})
    luu()
elif lenh("compute", "instances", "reset"):
    S["vm"]["status"] = "RUNNING"
    luu()
elif lenh("projects", "add-iam-policy-binding") and S.get("policy_co_dieu_kien", True) and co("--condition") is None:
    # ⭐ `STG-WEB-R1-03` (lỗi THẬT 24/11, `fp-a-project` có 2 binding điều kiện): gcloud ở chế độ ⛔ tương tác
    #   từ chối thêm binding KHÔNG nói điều kiện vào chính sách CÓ điều kiện. Mặc định BẬT — giống project thật.
    print("ERROR: (gcloud.projects.add-iam-policy-binding) Adding a binding without specifying a condition to a policy "
          "containing conditions is prohibited in non-interactive mode. Run the command again with `--condition=None`",
          file=sys.stderr)
    sys.exit(1)
elif lenh("compute", "instances", "add-iam-policy-binding") or lenh("projects", "add-iam-policy-binding"):
    S["quyen"].append({"lenh": " ".join(a[:3]), "member": co("--member"), "role": co("--role")})
    luu()
elif lenh("compute", "ssh"):
    if not S["vm"] or S.get("ssh_hong"):
        sys.exit(255)
    print(S["ssh_ra"])
# ══ bước 07 (WO-363) · Cloud Run + IAP ═══════════════════════════════════════════════════════════════════
#  ⭐ Học từ 3 lỗi THẬT 23/11 (giả cũ "cho qua" ⇒ xanh giả): mỗi nhánh dưới mô phỏng một HÀNH VI GCP đã biết, kể cả
#  khi nó LÀM HỎNG script: tác tử IAP CHƯA tồn tại trước `services identity create` ⇒ gán quyền đỏ "does not exist";
#  `deploy` ảnh chưa có ⇒ đỏ; `deploy` của service ĐÃ có `allUsers` ⇒ GIỮ `allUsers` (`--no-allow-unauthenticated`
#  ⛔ gỡ binding cũ — giả định bi quan, BG-364 G-4); `iap_chi_beta` ⇒ GA ⛔ biết `--iap` (đúng câu gcloud).
#  Mỗi revision mới "khởi động MỘT instance lúc deploy" (giả định G-5) ⇒ ghi một dòng `TU_DO` vào nhật ký.
elif lenh("config", "get-value", "account"):
    print(S.get("tai_khoan", ""))
elif lenh("projects", "describe"):
    print(S.get("so_project", "123456789012"))
elif lenh("services", "identity", "create"):
    if co("--service") != "iap.googleapis.com":
        sys.exit(99)
    S["tac_tu_iap"] = True
    luu()
    print(f"Service identity created: service-{S.get('so_project', '123456789012')}@gcp-sa-iap.iam.gserviceaccount.com")
elif lenh("run", "deploy") or lenh("beta", "run", "deploy"):
    beta = a[0] == "beta"
    if "--iap" in a and S.get("iap_chi_beta") and not beta:
        print("ERROR: (gcloud.run.deploy) unrecognized arguments: --iap", file=sys.stderr)
        sys.exit(2)
    if "run.googleapis.com" not in S["apis"]:
        print("ERROR: (gcloud.run.deploy) PERMISSION_DENIED: Cloud Run Admin API has not been used in project", file=sys.stderr)
        sys.exit(1)
    anh = co("--image")
    if anh.rsplit(":", 1)[1] not in S["anh_tags"]:
        print(f"ERROR: (gcloud.run.deploy) Image '{anh}' not found.", file=sys.stderr)
        sys.exit(1)
    ten = a[3] if beta else a[2]
    env = [{"name": k, "value": v} for k, v in kv(co("--set-env-vars")).items()]
    cu = S.get("run") or {}
    so = int(re.search(r"-(\d{5})-", cu.get("status", {}).get("latestReadyRevisionName") or "x-00000-").group(1)) + 1
    rev = f"{ten}-{so:05d}-gia"
    ann = {"run.googleapis.com/ingress": co("--ingress") or "all"}
    if "--iap" in a:
        ann["run.googleapis.com/iap-enabled"] = "true"
    S["run"] = {"apiVersion": "serving.knative.dev/v1", "kind": "Service",
                "metadata": {"name": ten, "annotations": ann},
                "spec": {"template": {"metadata": {"annotations": {"autoscaling.knative.dev/maxScale": co("--max-instances"),
                                                                    "autoscaling.knative.dev/minScale": co("--min-instances")}},
                                      "spec": {"serviceAccountName": co("--service-account"),
                                               "containers": [{"image": anh, "command": [co("--command")],
                                                               "args": [co("--args")],
                                                               "ports": [{"containerPort": int(co("--port")), "name": "http1"}],
                                                               "env": env}]}}},
                "status": {"url": S.get("url", "https://fls-staging-web-gia123-as.a.run.app"), "latestReadyRevisionName": rev,
                           "conditions": [{"type": "Ready", "status": "True"}]}}
    S.setdefault("run_iam", [])
    if "--allow-unauthenticated" in a:
        S["run_iam"].append({"role": "roles/run.invoker", "members": ["allUsers"]})
    sa = "serviceAccount:" + co("--service-account")

    def _sa_co(ten, *vai):
        bm = S.get("secrets", {}).get(ten)
        return bool(bm and bm["versions"]) and all(any(b["role"] == v and sa in b["members"] for b in bm["iam"]) for v in vai)
    san_sang = _sa_co("fls-staging-login", "roles/secretmanager.secretAccessor")
    tt_san = _sa_co("fls-staging-phien", "roles/secretmanager.secretAccessor", "roles/secretmanager.secretVersionManager")
    aud_ghim = bool(kv(co("--set-env-vars")).get("FLS_IAP_AUD"))
    S.setdefault("nhat_ky", []).append(S.get("tu_do", "TU_DO revision={rev} man_hinh=200 api_khong_the=401 "
                                                     "nghe_cua=127.0.0.1:8088 cong_khong_iap=403 cong_iap_gia=403 jwks=3 "
                                                     "dang_nhap={dn} trang_thai={tt} aud={aud}")
                                       .format(rev=rev, dn="san_sang" if san_sang else "chua_dat",
                                               tt="san_sang" if tt_san else "chua_dat", aud="ghim" if aud_ghim else "chua_ghim"))
    luu()
elif lenh("run", "services", "describe"):
    if not S.get("run"):
        print("ERROR: (gcloud.run.services.describe) Cannot find service", file=sys.stderr)
        sys.exit(1)
    xuat_json(S["run"])
elif lenh("run", "services", "get-iam-policy"):
    if not S.get("run"):
        sys.exit(1)
    xuat_json({"bindings": S.get("run_iam", [])})
elif lenh("run", "services", "add-iam-policy-binding"):
    m = co("--member")
    if "gcp-sa-iap" in m and not S.get("tac_tu_iap"):
        print(f"ERROR: (gcloud.run.services.add-iam-policy-binding) INVALID_ARGUMENT: Service account {m.split(':', 1)[1]} "
              "does not exist.", file=sys.stderr)
        sys.exit(1)
    S.setdefault("run_iam", []).append({"role": co("--role"), "members": [m]})
    luu()
elif lenh("run", "services", "remove-iam-policy-binding"):
    for b in S.get("run_iam", []):
        if b["role"] == co("--role") and co("--member") in b["members"]:
            b["members"].remove(co("--member"))
    S["run_iam"] = [b for b in S.get("run_iam", []) if b["members"]]
    luu()
elif lenh("iap", "web", "add-iam-policy-binding"):
    if co("--resource-type") != "cloud-run" or not S.get("run"):
        print("ERROR: (gcloud.iap.web.add-iam-policy-binding) NOT_FOUND", file=sys.stderr)
        sys.exit(1)
    S.setdefault("iap_iam", []).append({"role": co("--role"), "members": [co("--member")]})
    luu()
elif lenh("iap", "web", "get-iam-policy"):
    if not S.get("run") or S.get("iap_iam_hong"):
        sys.exit(1)
    xuat_json({"bindings": S.get("iap_iam", [])})
elif lenh("secrets", "describe"):
    if a[2] not in S.get("secrets", {}):
        sys.exit(1)
    print(f"projects/{S.get('so_project', '123456789012')}/secrets/{a[2]}")
elif lenh("secrets", "create"):
    if a[2] in S.setdefault("secrets", {}):
        print("ERROR: (gcloud.secrets.create) ALREADY_EXISTS", file=sys.stderr)
        sys.exit(1)
    S["secrets"][a[2]] = {"versions": [sys.stdin.read()], "iam": []}
    luu()
elif lenh("secrets", "versions", "add"):
    if a[3] not in S.get("secrets", {}):
        print("ERROR: (gcloud.secrets.versions.add) NOT_FOUND", file=sys.stderr)
        sys.exit(1)
    S["secrets"][a[3]]["versions"].append(sys.stdin.read())
    luu()
elif lenh("secrets", "versions", "access"):
    ten = co("--secret")
    if ten not in S.get("secrets", {}):
        sys.exit(1)
    sys.stdout.write(S["secrets"][ten]["versions"][-1])
elif lenh("secrets", "add-iam-policy-binding"):
    if a[2] not in S.get("secrets", {}):
        sys.exit(1)
    S["secrets"][a[2]]["iam"].append({"role": co("--role"), "members": [co("--member")]})
    luu()
elif lenh("secrets", "get-iam-policy"):
    if a[2] not in S.get("secrets", {}) or S.get("secrets_iam_hong"):
        sys.exit(1)
    xuat_json({"bindings": S["secrets"][a[2]]["iam"]})
elif lenh("logging", "read"):
    m = re.search(r'textPayload:"([^"]+)"', a[2])
    for d in reversed(S.get("nhat_ky", [])):
        if m and d.startswith(m.group(1)):
            print(d)
            break
else:
    print("gcloud GIẢ: lệnh lạ: " + " ".join(args), file=sys.stderr)
    sys.exit(99)
