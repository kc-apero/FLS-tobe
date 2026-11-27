"""Đo MẶT NGOÀI của cổng MCP đã dựng (`fls-staging-mcp`) — BÁO CÁO của `tools/staging/10_mcp.sh`. CHỈ stdlib.

    FLS_MCP_KHOA_DO=<hex khoá ký> FLS_MCP_DO_CHU=<email chủ> python3 tools/staging/app/do_mcp.py --url https://….run.app

In ra stdout các dòng `khoá=giá_trị` (⛔ email · ⛔ token · ⛔ nội dung kho — chỉ MÃ HTTP và SỐ ĐẾM).

⭐ Vì sao ký token THỬ ngay trong Cloud Shell: luồng thật cần trình duyệt + Google; BÁO CÁO phải đo được
`200 chủ · 403 người ngoài · INSERT bị chặn · số bảng > 0` KHÔNG cần ai bấm. Khoá ký đọc từ Secret Manager
bằng quyền CHỦ (`gcloud secrets versions access`), truyền qua MÔI TRƯỜNG (⛔ dòng lệnh); token sống 300 giây,
`cid` = `bao-cao-10`, ⛔ in. Khuôn ký = `fls.mcp.ky.Ky` (cùng mã với máy chủ — bài `tests/staging/test_10_mcp.py`
chạy tệp này vào máy chủ THẬT cục bộ).
⛔ Mục ⛔ đo được ⇒ giá trị `000`/`loi:…` ⇒ BÁO CÁO ĐỎ (Đ5), ⛔ "không thấy lệch".
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from fls.mcp.ky import Ky  # noqa: E402

NGOAI = "nguoi-ngoai@example.invalid"
PHIEN_BAN = "2025-06-18"


class _KhongTheo(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


_MO = urllib.request.build_opener(_KhongTheo)


def http(url: str, *, phuong: str = "GET", than: bytes | None = None, dau: dict | None = None):
    req = urllib.request.Request(url, data=than, method=phuong, headers=dau or {})
    try:
        with _MO.open(req, timeout=30) as r:
            return r.status, r.headers, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as e:
        return 0, {}, type(e).__name__


def rpc(url_mcp: str, token: str | None, method: str, params: dict, *, sau_khoi_tao: bool = True):
    dau = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if token:
        dau["Authorization"] = "Bearer " + token
    if sau_khoi_tao:
        dau["MCP-Protocol-Version"] = PHIEN_BAN
    than = json.dumps({"jsonrpc": "2.0", "id": secrets.randbelow(10**6), "method": method, "params": params}).encode()
    return http(url_mcp, phuong="POST", than=than, dau=dau)


def _khoi_tao(url_mcp, tok):
    return rpc(url_mcp, tok, "initialize", {"protocolVersion": PHIEN_BAN, "capabilities": {},
                                            "clientInfo": {"name": "bao-cao-10", "version": "1"}},
               sau_khoi_tao=False)


def goi_cong_cu(url_mcp: str, tok: str, ten: str, args: dict) -> tuple[int, dict | None, bool]:
    ma, _, b = rpc(url_mcp, tok, "tools/call", {"name": ten, "arguments": args})
    if ma != 200:
        return ma, None, True
    try:
        r = json.loads(b)["result"]
        txt = r["content"][0]["text"]
        return ma, (None if r.get("isError") else json.loads(txt)), bool(r.get("isError"))
    except (ValueError, KeyError, IndexError, TypeError):
        return ma, None, True


def do(url: str, khoa: bytes, chu: str) -> dict[str, str]:
    url = url.rstrip("/")
    url_mcp = url + "/mcp"
    ky = Ky(khoa)
    bg = int(time.time())

    def tok(sub: str, **doi) -> str:
        p = {"typ": "at", "sub": sub, "aud": url_mcp, "cid": "bao-cao-10", "scp": ["fls.doc"], "iat": bg,
             "exp": bg + 300, "jti": secrets.token_hex(6)}
        p.update(doi)
        return ky.ky(p)

    ra: dict[str, str] = {}
    ma, dau, _ = _khoi_tao(url_mcp, None)
    ra["khong_token"] = str(ma)
    www = (dau.get("WWW-Authenticate") if hasattr(dau, "get") else "") or ""
    ra["www_resource_metadata"] = "co" if "resource_metadata=" in www else "khong"
    ma, _, b = http(url + "/.well-known/oauth-protected-resource/mcp")
    try:
        prm = json.loads(b) if ma == 200 else {}
    except ValueError:
        prm = {}
    ra["prm_resource_khop"] = str(prm.get("resource") == url_mcp)
    ra["prm_as_khop"] = str([x.rstrip("/") for x in prm.get("authorization_servers", [])] == [url])
    ma, _, b = http(url + "/.well-known/oauth-authorization-server")
    try:
        asm = json.loads(b) if ma == 200 else {}
    except ValueError:
        asm = {}
    ra["as_issuer_khop"] = str(str(asm.get("issuer", "")).rstrip("/") == url)
    than = json.dumps({"redirect_uris": ["https://ke-xau.example.invalid/cb"], "grant_types": ["authorization_code"],
                       "response_types": ["code"], "token_endpoint_auth_method": "none"}).encode()
    ra["dang_ky_redirect_la"] = str(http(url + "/register", phuong="POST", than=than,
                                         dau={"Content-Type": "application/json"})[0])
    ra["token_khoa_gia"] = str(_khoi_tao(url_mcp, Ky(secrets.token_bytes(32)).ky(
        {"typ": "at", "sub": chu, "aud": url_mcp, "cid": "x", "scp": ["fls.doc"], "exp": bg + 300}))[0])
    ra["token_aud_sai"] = str(_khoi_tao(url_mcp, tok(chu, aud="https://may-khac.example.invalid/mcp"))[0])
    ra["token_het_han"] = str(_khoi_tao(url_mcp, tok(chu, exp=bg - 10))[0])
    ra["nguoi_ngoai"] = str(_khoi_tao(url_mcp, tok(NGOAI))[0])
    t = tok(chu)
    ra["chu_khoi_tao"] = str(_khoi_tao(url_mcp, t)[0])
    ma, d, loi = goi_cong_cu(url_mcp, t, "liet_ke_bang", {})
    ra["chu_so_bang"] = str(d.get("so_dong")) if d else f"loi:{ma}"
    ra["chu_bang_co_dong"] = str(sum(1 for x in d["bang"] if (x.get("so_dong") or 0) > 0)) if d else f"loi:{ma}"
    ma, d, loi = goi_cong_cu(url_mcp, t, "truy_van_doc", {"sql": "insert into fls_run (run_id) values ('X')"})
    ra["chu_insert"] = "chan" if (ma == 200 and loi) else ("LOT" if d is not None else f"loi:{ma}")
    ma, d, loi = goi_cong_cu(url_mcp, t, "truy_van_doc", {"sql": (
        "select (select count(*) from information_schema.columns where table_schema='public'),"
        " (select count(*) from information_schema.columns where table_schema='public' and column_name ilike '%email%'),"
        " (select count(*) from fls_pm_line where tho is not null),"
        " (select count(*) from fls_pm_line where tho::jsonb ? 'Email Address')")})
    if d and d.get("dong"):
        so_cot, cot_email, dong_tho, dong_email = d["dong"][0]
        ra["rieng_tu_mau_so"] = f"{so_cot}/{dong_tho}"
        ra["rieng_tu_email"] = f"{cot_email}/{dong_email}"
    else:
        ra["rieng_tu_mau_so"] = ra["rieng_tu_email"] = f"loi:{ma}"
    ma, d, loi = goi_cong_cu(url_mcp, t, "cong", {})
    ra["chu_cong"] = str(len(d["data"]["cong"])) if d else f"loi:{ma}"
    return ra


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    a = ap.parse_args(argv)
    try:
        khoa = bytes.fromhex(os.environ.get("FLS_MCP_KHOA_DO", ""))
    except ValueError:
        khoa = b""
    chu = os.environ.get("FLS_MCP_DO_CHU", "").strip().lower()
    if len(khoa) < 32 or not chu:
        print("do_mcp=loi:thieu_khoa_hoac_chu")
        return 0
    for k, v in do(a.url, khoa, chu).items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
