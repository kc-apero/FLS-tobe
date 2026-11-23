# -*- coding: utf-8 -*-
"""Một chỗ LẤY THÔNG TIN XÁC THỰC để ĐỌC Google Sheets — `WO-334` AC-2.

⭐ **Vì sao có tệp này** *(Đ1 — đo cả hai nơi 23/11: `grep -rn "print-access-token" tools fls` = 7 tệp, ⛔ 0 trong `fls/`)*:
   các công cụ nạp nguồn sẵn có (`tools/nap_that.py` · `tools/nap_mapping_master.py` · `tools/do_hinh_dang.py` → `chup_sao_ke` ·
   `nap_nguon_va_khai`) đều gọi `gcloud auth print-access-token --account <SA GẮN CỨNG>` ⇒ chạy được ở máy chủ, ⛔ ở Cloud Shell/VM
   (BG-326 phát hiện #6). Nay cả bốn đi qua `lay_token()` ở đây; ⛔ còn đường cũ khi KHÔNG khai gì *(⇒ máy chủ chạy y như trước)*.

THỨ TỰ *(dừng ở cái đầu tiên có)*:
  ① `FLS_SHEETS_TOKEN`           — một access token ĐƯA SẴN *(vd Cloud Shell: `export FLS_SHEETS_TOKEN=$(gcloud auth print-access-token
                                    --scopes=…spreadsheets.readonly,…drive.readonly)`; hết hạn sau ~60 phút ⇒ chạy lại)*
  ② `FLS_SHEETS_SA_JSON_TEP`     — ĐƯỜNG DẪN tệp khoá SA *(⛔ nội dung khoá không bao giờ qua đây)* ·
     `FLS_GSHEETS_SA_JSON(_B64)` — khoá SA trong biến môi trường *(đúng tên mà environment secrets của phiên cloud dùng)*
  ③ `FLS_SHEETS_ADC=1`           — Application Default Credentials *(SA gắn với máy/VM staging, hoặc `gcloud auth application-default login`)*
  ④ ⛔ KHÔNG khai ⇒ đường CŨ `gcloud auth print-access-token --account <SA máy chủ>` *(tương thích)*.

⛔ CHỈ-ĐỌC: phạm vi `spreadsheets.readonly` + `drive.metadata.readonly` — ⛔ `QĐ-ITL-34` (không ghi/nhận xét sheet). ⛔ Tệp này ⛔ in
   giá trị token/khoá; `mo_ta()` chỉ trả TÊN đường.
Gốc API: `FLS_SHEETS_API_GOC` *(mặc định Google; bài thử trỏ về máy chủ Sheets GIẢ)*.
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import threading
import time

API_GOC_MAC_DINH = "https://sheets.googleapis.com/v4/spreadsheets/"
SA_MAY_CHU = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
PHAM_VI = ("https://www.googleapis.com/auth/spreadsheets.readonly",
           "https://www.googleapis.com/auth/drive.metadata.readonly")
HAN_GIU_GIAY = 30 * 60           # token sống ~60 phút; làm mới sau 30 để một lượt đọc dài ⛔ chết giữa chừng

_khoa = threading.Lock()
_nho: dict = {"tok": None, "luc": 0.0, "cred": None, "kieu": None}


def api_goc() -> str:
    g = os.environ.get("FLS_SHEETS_API_GOC") or API_GOC_MAC_DINH
    return g if g.endswith("/") else g + "/"


def _khoa_sa() -> tuple[str, dict] | None:
    tep = os.environ.get("FLS_SHEETS_SA_JSON_TEP")
    if tep:
        with open(tep, encoding="utf-8") as f:
            return "sa-tep", json.load(f)
    raw = os.environ.get("FLS_GSHEETS_SA_JSON")
    if raw:
        return "sa-env", json.loads(raw)
    b64 = os.environ.get("FLS_GSHEETS_SA_JSON_B64")
    if b64:
        return "sa-env-b64", json.loads(base64.b64decode(b64).decode())
    return None


def _cu_gcloud() -> str:
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA_MAY_CHU, "--scopes", PHAM_VI[0]],
        capture_output=True, text=True, shell=(os.name == "nt"))
    t = r.stdout.strip()
    if not t:
        raise SystemExit("⛔ khong lay duoc token (duong cu gcloud): " + r.stderr.strip()[:200])
    return t


def kieu() -> str:
    """TÊN đường sẽ dùng — ⛔ không lộ giá trị. `token-dua-san` · `sa-tep` · `sa-env` · `sa-env-b64` · `adc` · `gcloud-cu`."""
    if os.environ.get("FLS_SHEETS_TOKEN"):
        return "token-dua-san"
    if (os.environ.get("FLS_SHEETS_SA_JSON_TEP") or os.environ.get("FLS_GSHEETS_SA_JSON")
            or os.environ.get("FLS_GSHEETS_SA_JSON_B64")):
        return "sa-tep" if os.environ.get("FLS_SHEETS_SA_JSON_TEP") else (
            "sa-env" if os.environ.get("FLS_GSHEETS_SA_JSON") else "sa-env-b64")
    if os.environ.get("FLS_SHEETS_ADC") == "1":
        return "adc"
    return "gcloud-cu"


def lay_token() -> str:
    k = kieu()
    if k == "token-dua-san":
        return os.environ["FLS_SHEETS_TOKEN"].strip()
    if k == "gcloud-cu":
        return _cu_gcloud()
    with _khoa:
        if _nho["tok"] and time.time() - _nho["luc"] < HAN_GIU_GIAY and _nho["kieu"] == k:
            return _nho["tok"]
        try:
            import google.auth.transport.requests as gtr
        except ImportError as e:   # ⛔ im lặng lùi về đường cũ — nổ, có tên
            raise SystemExit("⛔ thieu goi `google-auth` (pip install google-auth requests) — can cho duong %s: %s" % (k, e))
        if k == "adc":
            import google.auth
            cred, _ = google.auth.default(scopes=list(PHAM_VI))
        else:
            from google.oauth2 import service_account
            _, info = _khoa_sa()
            cred = service_account.Credentials.from_service_account_info(info, scopes=list(PHAM_VI))
        cred.refresh(gtr.Request())
        _nho.update(tok=cred.token, luc=time.time(), cred=cred, kieu=k)
        return cred.token


def mo_ta() -> str:
    return "%s · gốc API %s · phạm vi %s" % (kieu(), api_goc(), "+".join(p.rsplit("/", 1)[1] for p in PHAM_VI))
