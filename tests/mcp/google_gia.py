"""Google OIDC GIẢ cho bài xác thực MCP — đủ ba điểm cuối mà `fls.mcp.xac_thuc` gọi: `/auth` · `/token` · `/jwks`.

⭐ ĐỒ THẬT ở mọi chỗ trừ danh tính: `id_token` ký RS256 bằng khoá RSA sinh LÚC CHẠY (`cryptography`), JWKS
phục vụ qua HTTP thật, PKCE S256 kiểm thật, `client_secret` kiểm thật. Bài chọn AI đăng nhập bằng
`dat_nguoi(email)` và có thể làm Google NÓI DỐI (`gia_mao`: ký bằng khoá KHÁC · `aud` khác · `nonce` khác ·
email chưa xác minh) để chứng minh máy chủ ⛔ tin mù.
"""
from __future__ import annotations

import base64
import hashlib
import json
import secrets
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

ID = "gia-client.apps.googleusercontent.com"
BI_MAT = "gia-bi-mat-" + secrets.token_hex(6)


def _b64(n: int) -> str:
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


class GoogleGia:
    def __init__(self):
        self.khoa = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.khoa_la = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.nguoi = "chu@vi.du"
        self.gia_mao: str | None = None
        self.ma: dict[str, dict] = {}
        self.goi_token = 0
        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), self._tay())
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def dong(self):
        self.srv.shutdown()

    def dat_nguoi(self, email: str, gia_mao: str | None = None):
        self.nguoi, self.gia_mao = email, gia_mao

    def _id_token(self, rec: dict) -> str:
        bg = int(time.time())
        c = {"iss": "https://accounts.google.com", "aud": ID, "sub": "g-" + rec["email"], "email": rec["email"],
             "email_verified": True, "nonce": rec["nonce"], "iat": bg, "exp": bg + 3600}
        khoa = self.khoa
        if self.gia_mao == "khoa_la":
            khoa = self.khoa_la
        elif self.gia_mao == "aud":
            c["aud"] = "app-khac.apps.googleusercontent.com"
        elif self.gia_mao == "nonce":
            c["nonce"] = "khac"
        elif self.gia_mao == "chua_xac_minh":
            c["email_verified"] = False
        elif self.gia_mao == "het_han":
            c["iat"], c["exp"] = bg - 7200, bg - 3600
        return jwt.encode(c, khoa, algorithm="RS256", headers={"kid": "k1"})

    def _tay(self):
        g = self

        class Tay(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _json(self, ma, d):
                b = json.dumps(d).encode()
                self.send_response(ma)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)

            def do_GET(self):
                p = urllib.parse.urlparse(self.path)
                q = dict(urllib.parse.parse_qsl(p.query))
                if p.path == "/jwks":
                    pub = g.khoa.public_key().public_numbers()
                    return self._json(200, {"keys": [{"kty": "RSA", "kid": "k1", "alg": "RS256", "use": "sig",
                                                      "n": _b64(pub.n), "e": _b64(pub.e)}]})
                if p.path == "/auth":
                    assert q["client_id"] == ID and q["response_type"] == "code"
                    assert q["code_challenge_method"] == "S256" and "email" in q["scope"].split()
                    ma = "G-" + secrets.token_urlsafe(8)
                    g.ma[ma] = {"email": g.nguoi, "nonce": q["nonce"], "cc": q["code_challenge"],
                                "ru": q["redirect_uri"]}
                    toi = q["redirect_uri"] + "?" + urllib.parse.urlencode({"code": ma, "state": q["state"]})
                    self.send_response(302)
                    self.send_header("Location", toi)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                self._json(404, {})

            def do_POST(self):
                n = int(self.headers.get("Content-Length") or 0)
                f = dict(urllib.parse.parse_qsl(self.rfile.read(n).decode()))
                if self.path != "/token":
                    return self._json(404, {})
                g.goi_token += 1
                rec = g.ma.pop(f.get("code", ""), None)
                if (rec is None or f.get("client_id") != ID or f.get("client_secret") != BI_MAT
                        or f.get("redirect_uri") != rec["ru"]):
                    return self._json(400, {"error": "invalid_grant"})
                cc = base64.urlsafe_b64encode(hashlib.sha256(f.get("code_verifier", "").encode()).digest())
                if cc.rstrip(b"=").decode() != rec["cc"]:
                    return self._json(400, {"error": "invalid_grant", "error_description": "pkce"})
                self._json(200, {"access_token": "ya29.gia", "token_type": "Bearer", "expires_in": 3599,
                                 "id_token": g._id_token(rec)})
        return Tay
