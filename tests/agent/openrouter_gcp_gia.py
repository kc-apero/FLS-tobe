#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`gcloud` + `curl` GIẢ cho `tools/staging/09_openrouter_agent.sh` (`WO-367` AC-5) — một tệp, vai theo TÊN gọi (argv[0]).

Trạng thái: JSON ở `$FLS_GIA_TRANG_THAI`. Sổ: `<tt>.log` = argv MỌI lệnh (bài soi khoá ⛔ ở argv) · `<tt>.than` = thân POST
chat/completions (bài soi `provider`). ⛔ mạng, ⛔ GCP.
"""
import json
import os
import sys
from pathlib import Path

TT = Path(os.environ["FLS_GIA_TRANG_THAI"])
VAI = Path(sys.argv[0]).name
A = sys.argv[1:]


def doc():
    return json.loads(TT.read_text(encoding="utf-8"))


def ghi(s):
    TT.write_text(json.dumps(s), encoding="utf-8")


with open(str(TT) + ".log", "a", encoding="utf-8") as f:
    f.write(" ".join([VAI, *A]) + "\n")


def gcloud():
    s = doc()
    a = [x for x in A if not x.startswith("--project=") and x != "--quiet"]
    if a[:2] == ["services", "enable"]:
        s["apis"] = sorted(set(s["apis"]) | set(a[2:]))
        return ghi(s) or 0
    if a[0] != "secrets":
        print(f"gcloud giả: lệnh lạ {a}", file=sys.stderr)
        return 2
    cam_api = "secretmanager.googleapis.com" not in s["apis"]
    if a[1] == "describe":
        return 0 if a[2] in s["secrets"] and not cam_api else 1
    if a[1] == "create":
        if cam_api or a[2] in s["secrets"]:
            return 1
        s["secrets"][a[2]] = [sys.stdin.read()]
        return ghi(s) or 0
    if a[1:3] == ["versions", "add"]:
        if a[3] not in s["secrets"]:
            return 1
        s["secrets"][a[3]].append(sys.stdin.read())
        return ghi(s) or 0
    if a[1:3] == ["versions", "access"]:
        ten = next(x.split("=", 1)[1] for x in a if x.startswith("--secret="))
        if cam_api or ten not in s["secrets"]:
            return 1
        sys.stdout.write(s["secrets"][ten][-1])
        return 0
    if a[1] == "add-iam-policy-binding":
        m = next(x.split("=", 1)[1] for x in a if x.startswith("--member="))
        r = next(x.split("=", 1)[1] for x in a if x.startswith("--role="))
        b = s["secret_iam"].setdefault(a[2], [])
        if not any(x["role"] == r and m in x["members"] for x in b):
            b.append({"role": r, "members": [m]})
        return ghi(s) or 0
    if a[1] == "get-iam-policy":
        if a[2] not in s["secrets"]:
            return 1
        print(json.dumps({"bindings": s["secret_iam"].get(a[2], [])}))
        return 0
    print(f"gcloud giả: lệnh lạ {a}", file=sys.stderr)
    return 2


def curl():
    s = doc()
    ra, w, pp, hdr, data, url = None, "", "GET", [], None, None
    i = 0
    while i < len(A):
        x = A[i]
        if x in ("-o", "-w", "-X", "-H", "--data-binary", "--max-time"):
            v = A[i + 1]
            if x == "-o":
                ra = v
            elif x == "-w":
                w = v
            elif x == "-X":
                pp = v
            elif x == "-H":
                hdr.append(Path(v[1:]).read_text(encoding="utf-8").strip() if v.startswith("@") else v)
            elif x == "--data-binary":
                data = Path(v[1:]).read_text(encoding="utf-8") if v.startswith("@") else v
            i += 2
            continue
        if not x.startswith("-"):
            url = x
        i += 1
    au = next((h.split(":", 1)[1].strip() for h in hdr if h.lower().startswith("authorization:")), "")
    hop_le = au == f"Bearer {s['khoa_hop_le']}"
    duong = url.split("/api/v1", 1)[1]
    if duong == "/models":
        ma, d = 200, {"data": [{"id": m} for m in s["models"]]}
    elif duong == "/key":
        ma, d = (200, {"data": {"limit_remaining": 7.5, "label": "che"}}) if hop_le else (401, {"error": {"code": 401}})
    elif duong == "/chat/completions" and pp == "POST":
        than = json.loads(data)
        with open(str(TT) + ".than", "a", encoding="utf-8") as f:
            f.write(json.dumps(than, ensure_ascii=False) + "\n")
        slug = than["model"]
        if not hop_le:
            ma, d = 401, {"error": {"code": 401, "message": "NOIDUNG-GIA"}}
        elif slug in s["loi_goi"]:
            c = s["loi_goi"][slug]
            ma, d = c, {"error": {"code": c, "message": "NOIDUNG-GIA chi tiet"}}
        else:
            ma, d = 200, {"id": "gen-gia", "model": s["model_tra"].get(slug, slug), "provider": "Amazon Bedrock",
                          "choices": [{"finish_reason": "stop", "message": {"content": "NOIDUNG-GIA-OK"}}],
                          "usage": {"prompt_tokens": 12, "completion_tokens": 3, "cost": s["cost"]}}
    else:
        ma, d = 404, {}
    if ra:
        Path(ra).write_text(json.dumps(d), encoding="utf-8")
    if "%{http_code}" in w:
        sys.stdout.write(str(ma))
    return 0


sys.exit(gcloud() if VAI == "gcloud" else curl())
