#!/usr/bin/env python3
"""`gcloud` GIẢ CÓ TRẠNG THÁI — mô phỏng MỘT project GCP đủ cho `tools/staging/03_dung_app.sh`.

Trạng thái ở `$FLS_GIA_TRANG_THAI` (JSON). Mỗi lệnh GHI đổi trạng thái; mỗi lệnh ĐỌC trả đúng khuôn JSON/`value()`
mà script đọc. Lệnh LẠ ⇒ exit 99 (một lệnh script gọi mà giả ⛔ biết là một lỗi của bài thử, không phải "cho qua").
`builds submit` GHI LẠI danh sách tệp của ngữ cảnh build — bài thử dùng nó để chứng minh dữ liệu gitignore ⛔ lên.
Mọi lệnh gọi được ghi vào `<trang_thai>.log` (một dòng/lệnh) để bài thử đếm lệnh GHI.
"""
import json
import os
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
    ctx = a[2]
    tep = sorted(os.path.relpath(os.path.join(d, n), ctx) for d, _, ns in os.walk(ctx) for n in ns)
    S["builds"].append({"tag": co("--tag"), "tep": tep})
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
