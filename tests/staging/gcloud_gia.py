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
elif lenh("compute", "instances", "add-iam-policy-binding") or lenh("projects", "add-iam-policy-binding"):
    S["quyen"].append({"lenh": " ".join(a[:3]), "member": co("--member"), "role": co("--role")})
    luu()
elif lenh("compute", "ssh"):
    if not S["vm"] or S.get("ssh_hong"):
        sys.exit(255)
    print(S["ssh_ra"])
else:
    print("gcloud GIẢ: lệnh lạ: " + " ".join(args), file=sys.stderr)
    sys.exit(99)
