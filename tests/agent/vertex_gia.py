#!/usr/bin/env python3
"""`gcloud` + `curl` GIẢ CÓ TRẠNG THÁI — mô phỏng MỘT project GCP đủ cho `tools/staging/06_vertex_agent.sh` (`WO-359` AC-3):
đường `google-cloud` (`claude.googleapis.com`, hàm `claude_gc`) và đường `vertex` (`aiplatform`, phần dưới).

Cùng tệp, chép thành hai tên: `gcloud` và `curl` (hành vi theo tên gọi). Trạng thái ở `$FLS_GIA_TRANG_THAI` (JSON);
mọi lệnh ghi một dòng vào `<trang_thai>.log`. Lệnh LẠ ⇒ exit 99 (một lệnh script gọi mà giả ⛔ biết = lỗi bài thử).

⭐ Hành vi GCP mô phỏng — ĐÃ TRA (trang Anthropic `claude-models-on-google-cloud/google-managed`, 24/11):
   · URL `https://<host>/v1/projects/<p>/locations/<vùng>/publishers/anthropic/models/<mã>:rawPredict`;
     host: `global` ⇒ `aiplatform.googleapis.com` · `us`/`eu` ⇒ `aiplatform.<vùng>.rep.googleapis.com`
     · vùng đơn ⇒ `<vùng>-aiplatform.googleapis.com` NHƯNG ⛔ phục vụ Opus 5.5 / Sonnet 5.5.
   · `anthropic_version` nằm trong THÂN; `model` nằm trong URL. Quyền cần: `aiplatform.endpoints.predict`
     (`roles/aiplatform.user`). Đáp 200 = khuôn Messages (`model` · `stop_reason` · `usage`).
   · Lấy token trong VM: metadata server `…/instance/service-accounts/default/token` (header `Metadata-Flavor: Google`).
⚠ GIẢ ĐỊNH CHƯA KIỂM (ghi ở BG-360 — GCP thật có thể khác; script ⛔ dựa vào chúng, chỉ so `HTTP == 200`):
   · mô hình chưa bật ở Model Garden ⇒ 400 `FAILED_PRECONDITION` · API tắt ⇒ 403 `SERVICE_DISABLED`
   · thiếu IAM ⇒ 403 `PERMISSION_DENIED` · VM thiếu phạm vi `cloud-platform` ⇒ 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT`
   · vùng đơn với Opus/Sonnet 5.5 ⇒ 404 `NOT_FOUND` · Vertex trả `model` = mã trần đã gọi.
"""
import json
import os
import re
import subprocess
import sys

TT = os.environ["FLS_GIA_TRANG_THAI"]
TEN = os.path.basename(sys.argv[0])
args = sys.argv[1:]
with open(TT + ".log", "a", encoding="utf-8") as f:
    f.write(TEN + " " + " ".join(args) + "\n")
S = json.load(open(TT, encoding="utf-8"))


def luu():
    json.dump(S, open(TT, "w", encoding="utf-8"), ensure_ascii=False)


TOK_NGUOI = "TOKGIA-nguoi-ya29-9f3a1c77d2e04b58"      # lính canh: ⛔ được xuất hiện trong đầu ra script
TOK_SA = "TOKGIA-sa-ya29-5b8e21aa90c3d4f1"


# ═══════════════════════════════════════ curl ═══════════════════════════════════════
def curl():
    url, ra, viet, hdr, du_lieu = None, None, None, [], None
    i = 0
    while i < len(args):
        x = args[i]
        if x in ("-sS", "-s", "-S"):
            i += 1
        elif x in ("-o", "-w", "--max-time", "-X", "-H", "--data-binary"):
            v = args[i + 1]
            if x == "-o":
                ra = v
            elif x == "-w":
                viet = v
            elif x == "-H":
                hdr.append(open(v[1:], encoding="utf-8").read().strip() if v.startswith("@") else v)
            elif x == "--data-binary":
                du_lieu = open(v[1:], encoding="utf-8").read() if v.startswith("@") else v
            i += 2
        elif x.startswith("http"):
            url = x
            i += 1
        else:
            print(f"curl GIẢ: cờ lạ {x}", file=sys.stderr)
            sys.exit(99)
    # metadata server (chỉ có TRONG VM)
    if url.startswith("http://metadata.google.internal/"):
        if os.environ.get("FLS_GIA_DANH_TINH") != "sa" or "Metadata-Flavor: Google" not in hdr:
            sys.exit(6)                                          # curl: (6) Could not resolve host
        print(json.dumps({"access_token": TOK_SA, "expires_in": 3599, "token_type": "Bearer"}))
        return
    auth = next((h for h in hdr if h.startswith("Authorization: Bearer ")), "")
    tok = auth.split(" ", 2)[2] if auth else ""
    g = re.match(r"https://claude\.googleapis\.com/v1/projects/([^/]+)/locations/([^/]+)/workspaces/([^/]+)/invoke/v1/messages$", url)
    if g:
        return claude_gc(g, tok, hdr, du_lieu, ra, viet)
    m = re.match(r"https://([^/]+)/v1/projects/([^/]+)/locations/([^/]+)/publishers/anthropic/models/([^/:]+):rawPredict$", url)
    if not m:
        print(f"curl GIẢ: URL lạ {url}", file=sys.stderr)
        sys.exit(99)
    host, du_an, vung, mo_hinh = m.groups()

    def tra(ma, body):
        if ra:
            open(ra, "w", encoding="utf-8").write(json.dumps(body))
        sys.stdout.write(viet.replace("%{http_code}", str(ma)) if viet else "")

    def loi(ma, status):
        tra(ma, {"error": {"code": ma, "message": "chi tiet GIA — KHONG duoc in", "status": status}})

    host_mong = ("aiplatform.googleapis.com" if vung == "global" else
                 f"aiplatform.{vung}.rep.googleapis.com" if vung in ("us", "eu") else f"{vung}-aiplatform.googleapis.com")
    yc = json.loads(du_lieu or "{}")
    if host != host_mong or du_an != S["project"]:
        return loi(404, "NOT_FOUND")
    if tok not in (TOK_NGUOI, TOK_SA):
        return loi(401, "UNAUTHENTICATED")
    if "aiplatform.googleapis.com" not in S["apis"]:
        return loi(403, "SERVICE_DISABLED")
    if tok == TOK_SA:
        if "https://www.googleapis.com/auth/cloud-platform" not in (S["vm"] or {}).get("scopes", []):
            return loi(403, "ACCESS_TOKEN_SCOPE_INSUFFICIENT")
        if not any(b["role"] == "roles/aiplatform.user" and f"serviceAccount:{S['sa']}" in b["members"] for b in S["iam"]):
            return loi(403, "PERMISSION_DENIED")
    if vung not in ("global", "us", "eu"):
        return loi(404, "NOT_FOUND")
    if mo_hinh not in S["model_garden"]:
        return loi(400, "FAILED_PRECONDITION")
    if "anthropic_version" not in yc or "model" in yc or not yc.get("messages"):
        return loi(400, "INVALID_ARGUMENT")
    tra(200, {"id": "msg_gia", "type": "message", "role": "assistant", "model": S.get("phuc_vu", {}).get(mo_hinh, mo_hinh),
              "content": [{"type": "text", "text": "NOIDUNG-GIA-khong-duoc-in"}], "stop_reason": "end_turn",
              "usage": {"input_tokens": 18, "output_tokens": 5}})


def claude_gc(g, tok, hdr, du_lieu, ra, viet):
    """`claude.googleapis.com` (Anthropic managed). ĐÃ TRA (skill `claude-api` 24/11): URL
    `/v1/projects/<p>/locations/global/workspaces/<wrkspc_…>/invoke/v1/messages` · `Authorization: Bearer <token Google>` ·
    header `anthropic-version` · thân như Claude API (`model` trong thân) · cần API `claude.googleapis.com` bật + vai
    `roles/claude.user` · lỗi theo khuôn Claude API `{"type":"error","error":{"type":…}}`.
    ⚠ GIẢ ĐỊNH CHƯA KIỂM: thiếu vai/API ⇒ 403 · workspace sai ⇒ 404 `not_found_error` · tài khoản người chạy (Owner)
    gọi được khi có `roles/claude.user` (trạng thái `nguoi_quyen`)."""
    du_an, vi_tri, ws = g.groups()

    def tra(ma, body):
        if ra:
            open(ra, "w", encoding="utf-8").write(json.dumps(body))
        sys.stdout.write(viet.replace("%{http_code}", str(ma)) if viet else "")

    def loi(ma, kieu):
        tra(ma, {"type": "error", "error": {"type": kieu, "message": "chi tiet GIA — KHONG duoc in"}})

    yc = json.loads(du_lieu or "{}")
    if du_an != S["project"] or vi_tri != "global":
        return loi(404, "not_found_error")
    if tok not in (TOK_NGUOI, TOK_SA):
        return loi(401, "authentication_error")
    if "claude.googleapis.com" not in S["apis"]:
        return loi(403, "permission_error")
    if tok == TOK_SA:
        if "https://www.googleapis.com/auth/cloud-platform" not in (S["vm"] or {}).get("scopes", []):
            return loi(403, "permission_error")
        if not any(b["role"] == "roles/claude.user" and f"serviceAccount:{S['sa']}" in b["members"] for b in S["iam"]):
            return loi(403, "permission_error")
    elif not S.get("nguoi_quyen", True):
        return loi(403, "permission_error")
    if ws != S.get("workspace"):
        return loi(404, "not_found_error")
    if not any(h.lower().startswith("anthropic-version: ") for h in hdr) or "anthropic_version" in yc:
        return loi(400, "invalid_request_error")
    mo_hinh = yc.get("model")
    if mo_hinh not in S.get("to_chuc_mo_hinh", ["claude-opus-5-5", "claude-sonnet-5-5"]):
        return loi(400, "invalid_request_error")
    tra(200, {"id": "msg_gia", "type": "message", "role": "assistant", "model": S.get("phuc_vu", {}).get(mo_hinh, mo_hinh),
              "content": [{"type": "text", "text": "NOIDUNG-GIA-khong-duoc-in"}], "stop_reason": "end_turn",
              "usage": {"input_tokens": 18, "output_tokens": 5}})


# ═══════════════════════════════════════ gcloud ═══════════════════════════════════════
def gcloud():
    a = [x for x in args if not x.startswith("--project=") and x != "--quiet"]

    def co(flag):
        for i, x in enumerate(a):
            if x.startswith(flag + "="):
                return x.split("=", 1)[1]
            if x == flag and i + 1 < len(a):
                return a[i + 1]
        return None

    def lenh(*t):
        return tuple(a[:len(t)]) == t

    if lenh("services", "enable"):
        for x in a[2:]:
            if not x.startswith("-") and x not in S["apis"]:
                S["apis"].append(x)
        luu()
    elif lenh("services", "list"):
        print("\n".join(S["apis"]))
    elif lenh("projects", "add-iam-policy-binding"):
        vai, tv = co("--role"), co("--member")
        b = next((b for b in S["iam"] if b["role"] == vai), None)
        if b is None:
            S["iam"].append({"role": vai, "members": [tv]})
        elif tv not in b["members"]:
            b["members"].append(tv)
        luu()
    elif lenh("projects", "get-iam-policy"):
        print(json.dumps({"bindings": S["iam"]}))
    elif lenh("compute", "instances", "describe"):
        if not S["vm"]:
            sys.exit(1)
        print(json.dumps({"name": a[3], "status": "RUNNING",
                          "serviceAccounts": [{"email": S["vm"]["sa"], "scopes": S["vm"]["scopes"]}]}))
    elif lenh("auth", "print-access-token"):
        if not S.get("dang_nhap", True):
            sys.exit(1)
        print(TOK_NGUOI)
    elif lenh("compute", "ssh"):
        # ⭐ CHẠY THẬT lệnh `--command` (bash) với `curl` GIẢ + danh tính SA ⇒ đo đúng chuỗi lệnh script gửi vào VM.
        if not S["vm"] or not S.get("ssh_duoc", True):
            sys.exit(255)
        lenh_vm = co("--command")
        env = dict(os.environ, FLS_GIA_DANH_TINH="sa")
        r = subprocess.run(["bash", "-c", lenh_vm], env=env, capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    else:
        print(f"gcloud GIẢ: lệnh lạ {' '.join(a)}", file=sys.stderr)
        sys.exit(99)


curl() if TEN == "curl" else gcloud()
