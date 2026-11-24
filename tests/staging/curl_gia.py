#!/usr/bin/env python3
"""`curl` GIẢ cho bước 07 — trả lời như MẶT NGOÀI của một service Cloud Run (đọc `$FLS_GIA_TRANG_THAI` của `gcloud_gia.py`).

Chỉ hiểu đúng MỘT dạng lệnh script gọi: `curl -s -o /dev/null -w '%{http_code} %{redirect_url}' --max-time N -X M URL`.
Dạng khác ⇒ exit 99 (một lệnh lạ là lỗi của bài thử, ⛔ "cho qua"). Mọi lệnh ghi vào `<trang_thai>.curl.log`.

Hành vi mô phỏng (giả định G-1 · G-6 của BG-364 — chưa đo ở GCP, BÁO CÁO thật sẽ phân xử):
  · service ⛔ có / URL lạ                  ⇒ curl exit 6 (⛔ phân giải tên)
  · IAP BẬT, ⛔ cookie: GET ⇒ 302 về `accounts.google.com` · POST ⇒ 401 (FAQ IAP: trình duyệt ⛔ chuyển hướng POST)
  · IAP TẮT + `allUsers` invoker: tới thẳng app — `/` ⇒ 200 · API ⛔ thẻ ⇒ 401
  · IAP TẮT, ⛔ công khai: Cloud Run IAM ⇒ 403
  `S["http_ngoai"]` (bài phá) ghi đè: {"GET /": "200 "} …
"""
import json
import os
import sys
import urllib.parse

TT = os.environ["FLS_GIA_TRANG_THAI"]
a = sys.argv[1:]
with open(TT + ".curl.log", "a", encoding="utf-8") as f:
    f.write(" ".join(a) + "\n")
mau = ["-s", "-o", "/dev/null", "-w", "%{http_code} %{redirect_url}", "--max-time"]
if a[:6] != mau or len(a) != 10 or a[7] != "-X":
    print("curl GIẢ: dạng lệnh lạ: " + " ".join(a), file=sys.stderr)
    sys.exit(99)
pt, url = a[8], a[9]
S = json.load(open(TT, encoding="utf-8"))
run = S.get("run")
if not run or not url.startswith(run["status"]["url"] + "/"):
    sys.exit(6)
duong = urllib.parse.urlparse(url).path
de = S.get("http_ngoai", {}).get(f"{pt} {duong}")
if de is not None:
    sys.stdout.write(de)
    sys.exit(0)
iap = run["metadata"]["annotations"].get("run.googleapis.com/iap-enabled") == "true"
cong_khai = any(m in ("allUsers", "allAuthenticatedUsers") for b in S.get("run_iam", []) for m in b["members"])
if iap:
    sys.stdout.write("302 https://accounts.google.com/o/oauth2/v2/auth?client_id=gia" if pt == "GET" else "401 ")
elif cong_khai:
    sys.stdout.write("200 " if duong == "/" else "401 ")
else:
    sys.stdout.write("403 ")
