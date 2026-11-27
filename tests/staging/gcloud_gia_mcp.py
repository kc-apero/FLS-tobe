#!/usr/bin/env python3
"""`gcloud` GIẢ cho `tools/staging/10_mcp.sh` (WO-371) — trạng thái trong tệp JSON `$FLS_GIA_MCP`.

⛔ Chỉ hiểu đúng các lệnh 10 được phép gọi; lệnh lạ ⇒ exit 99 (bài thấy ngay script gọi thêm gì). Mọi lời gọi ghi
vào `nhat_ky` (đối số đầy đủ) để bài soi: ⛔ xoá gì · ⛔ đụng tài nguyên ngoài tên FLS · bí mật ⛔ ở dòng lệnh.

Mô phỏng HÀNH VI GCP có thể làm hỏng script (học `STG-WEB-R1-03`, lỗi THẬT 24/11):
  · chính sách IAM dự án CÓ điều kiện (`policy_co_dieu_kien`, mặc định BẬT — `fp-a-project` có 2 binding
    điều kiện) ⇒ `projects add-iam-policy-binding` ⛔ `--condition` bị từ chối đúng lời gcloud;
  · `--condition=expression=…,title=…` ghi binding CÓ điều kiện (biểu thức giữ nguyên chữ).
  · `run deploy` ghi service theo khuôn `run services describe --format=json` (v1 Knative).
⚠ Tách khỏi `gcloud_gia.py` của nhánh STG-WEB (chưa gộp lúc viết) để hai nhánh ⛔ đụng một tệp.
"""
from __future__ import annotations

import json
import os
import sys

TT = os.environ["FLS_GIA_MCP"]
S = json.load(open(TT, encoding="utf-8"))
a = sys.argv[1:]
S.setdefault("nhat_ky", []).append(a)


def luu():
    json.dump(S, open(TT, "w", encoding="utf-8"), ensure_ascii=False)


def co(ten):
    for i, x in enumerate(a):
        if x == ten and i + 1 < len(a):
            return a[i + 1]
        if x.startswith(ten + "="):
            return x.split("=", 1)[1]
    return None


def vi_tri():
    return [x for x in a if not x.startswith("--")]


def ra(obj=None, txt=None, rc=0):
    luu()
    if obj is not None:
        print(json.dumps(obj))
    if txt is not None:
        print(txt)
    sys.exit(rc)


p = vi_tri()
P = S["project"]
stdin = (lambda: sys.stdin.read())

if p[:3] == ["config", "get-value", "account"]:
    ra(txt=S.get("tai_khoan", ""))
if p[:2] == ["projects", "describe"]:
    ra(txt=S.get("so_project", ""))
if p[:2] == ["services", "enable"]:
    S.setdefault("api", [])
    S["api"] = sorted(set(S["api"]) | set(p[2:]))
    ra()
if p[:2] == ["services", "list"]:
    ra(txt="\n".join(S.get("api", [])))
if p[:3] == ["iam", "service-accounts", "describe"]:
    ra(txt=p[3]) if p[3] in S.get("sa", []) else ra(rc=1)
if p[:3] == ["iam", "service-accounts", "create"]:
    S.setdefault("sa", []).append(f"{p[3]}@{P}.iam.gserviceaccount.com")
    ra()
if p[:2] == ["secrets", "describe"]:
    ra(txt=p[2]) if p[2] in S.get("bi_mat", {}) else ra(rc=1)
if p[:2] == ["secrets", "create"]:
    assert co("--data-file") == "-", a
    if p[2] in S.setdefault("bi_mat", {}):
        ra(rc=1)
    S["bi_mat"][p[2]] = {"gia_tri": [stdin()], "pol": {"bindings": []}}
    ra()
if p[:3] == ["secrets", "versions", "add"]:
    S["bi_mat"][p[3]]["gia_tri"].append(stdin())
    ra()
if p[:3] == ["secrets", "versions", "access"]:
    b = S.get("bi_mat", {}).get(co("--secret"))
    if b is None:
        ra(rc=1)
    sys.stdout.write(b["gia_tri"][-1])
    luu()
    sys.exit(0)
if p[:2] == ["secrets", "add-iam-policy-binding"]:
    pol = S["bi_mat"][p[2]]["pol"]
    pol["bindings"].append({"role": co("--role"), "members": [co("--member")]})
    ra()
if p[:2] == ["secrets", "get-iam-policy"]:
    b = S.get("bi_mat", {}).get(p[2])
    ra(obj=b["pol"]) if b else ra(rc=1)
if p[:2] == ["projects", "add-iam-policy-binding"]:
    dk = co("--condition")
    if dk is None and S.get("policy_co_dieu_kien", True):
        print("ERROR: (gcloud.projects.add-iam-policy-binding) Adding a binding without specifying a condition to a "
              "policy containing conditions is prohibited in non-interactive mode. Run the command again with "
              "`--condition=None`", file=sys.stderr)
        ra(rc=1)
    b = {"role": co("--role"), "members": [co("--member")]}
    if dk and dk != "None":
        expr, _, title = dk.partition(",title=")
        b["condition"] = {"expression": expr.removeprefix("expression="), "title": title}
    if b not in S.setdefault("proj_pol", {"bindings": []})["bindings"]:
        S["proj_pol"]["bindings"].append(b)
    ra()
if p[:2] == ["projects", "get-iam-policy"]:
    ra(obj=S.get("proj_pol", {"bindings": []}))
if p[:3] == ["sql", "instances", "describe"]:
    ra(txt=f"{P}:asia-southeast1:{p[3]}") if p[3] == "fls-staging" else ra(rc=1)
if p[:4] == ["artifacts", "docker", "images", "list"]:
    ra(txt="\n".join(S.get("tag", [])))
if p[:2] == ["builds", "submit"]:
    S.setdefault("tag", []).append(co("--tag").rsplit(":", 1)[1])
    ra(txt="Creating temporary archive of 9 file(s)")
if p[:2] == ["run", "deploy"]:
    if S.get("deploy_loi"):
        print("ERROR: " + S["deploy_loi"], file=sys.stderr)
        ra(rc=1)
    env = [{"name": k, "value": v} for k, v in (x.split("=", 1) for x in co("--set-env-vars").split(","))]
    ten = p[2]
    url_hash = f"https://{ten}-abc123-as.a.run.app"
    S.setdefault("run", {})[ten] = {
        "metadata": {"name": ten, "annotations": {"run.googleapis.com/urls": json.dumps(
            [url_hash, f"https://{ten}-{S['so_project']}.{co('--region')}.run.app"])}},
        "spec": {"template": {"metadata": {"annotations": {
            "autoscaling.knative.dev/maxScale": co("--max-instances"),
            "run.googleapis.com/cloudsql-instances": co("--add-cloudsql-instances")}},
            "spec": {"serviceAccountName": co("--service-account"), "containers": [{
                "image": co("--image"), "command": [co("--command")], "args": [co("--args")], "env": env}]}}},
        "status": {"url": url_hash, "conditions": [{"type": "Ready", "status": "True"}]}}
    S.setdefault("run_iam", {})[ten] = {"bindings": [{"role": "roles/run.invoker", "members": ["allUsers"]}]} \
        if "--allow-unauthenticated" in a else {"bindings": []}
    ra()
if p[:3] == ["run", "services", "describe"]:
    s = S.get("run", {}).get(p[3])
    ra(obj=s) if s else ra(rc=1)
if p[:3] == ["run", "services", "get-iam-policy"]:
    s = S.get("run_iam", {}).get(p[3])
    ra(obj=s) if s is not None else ra(rc=1)

print(f"gcloud GIẢ: lệnh lạ {a}", file=sys.stderr)
ra(rc=99)
