"""CỔNG IAP — thành phần DUY NHẤT nghe ngoài loopback khi FLS chạy trên Cloud Run sau Google IAP · WO-363 AC-2.

    python tools/staging/app/cong_iap.py --cong $PORT --cong-cua 8088      # chạy cổng (do `vao_cloud_run.sh` gọi)
    python tools/staging/app/cong_iap.py --doi-cua --cong-cua 8088          # chờ cửa lên (exit 0 khi nối được)
    python tools/staging/app/cong_iap.py --tu-do --cong $PORT --cong-cua 8088   # tự đo, in MỘT dòng `TU_DO …`

⛔⛔ VÌ SAO có tệp này (và vì sao nó ⛔ nới luật cửa). Cửa `tools/chay_cua.py --cho-web` TỰ TỪ CHỐI nghe ngoài
   loopback (`fls.api.cua.kiem_phuc_vu_tep`, `GAP-WEB-01`: vỏ màn hình ra TRƯỚC thẻ, `phien.js` phát MỘT thẻ
   `ke_toan` chung). Cloud Run chỉ đưa yêu cầu vào cổng `$PORT` của container ⇒ phải có MỘT thứ nghe `$PORT` và
   chuyển tiếp vào `127.0.0.1:8088`. Cửa giữ NGUYÊN: vẫn nghe 127.0.0.1, vẫn đòi thẻ cho mọi tuyến API.
   Hàng rào truy cập THẬT là Google IAP (chỉ tài khoản được cấp `roles/iap.httpsResourceAccessor`) + Cloud Run IAM
   (`--no-allow-unauthenticated`). Tệp này là lớp THỨ BA (phòng khi ai đó lỡ tắt IAP hay cho `allUsers`):

   ⓐ ⛔ chạy ngoài Cloud Run — thiếu `K_SERVICE` (Cloud Run tự đặt) ⇒ từ chối khởi động (exit 2). Chạy nhầm trên
      VM/máy dev thì nó KHÔNG thành một cổng mở ra mạng.
   ⓑ MỌI yêu cầu phải mang `X-Goog-IAP-JWT-Assertion` có CHỮ KÝ ES256 hợp lệ theo khoá công khai của IAP
      (`https://www.gstatic.com/iap/verify/public_key-jwk`), `iss = https://cloud.google.com/iap`, chưa hết hạn,
      có `email` — đúng hướng dẫn "Securing your app with signed headers" của Google. Thiếu/sai ⇒ 403, ⛔ chuyển
      tiếp. Lấy khoá hỏng ⇒ 503 (ĐÓNG, ⛔ mở). `FLS_IAP_AUD` (tuỳ) ⇒ ghim thêm `aud`.
   ⓒ đích chuyển tiếp CỐ ĐỊNH `127.0.0.1:<cong-cua>`; `--cong` = `--cong-cua` ⇒ từ chối (vòng lặp).
   ⓓ `Authorization` của app (thẻ FLS) đi qua NGUYÊN VẸN — tệp này ⛔ phát thẻ, ⛔ đổi luật ký. `actor` của mọi
      chữ ký vẫn là `--nguoi-ky` lúc dựng (cửa phát MỘT thẻ chung). Email IAP CHỈ để GHI NHẬT KÝ ai vào
      (dòng `IAP_VAO email=… GET /đường 200`) — SSO theo người là phase sau (`GAP-WEB-01`, câu chủ ở BG-364).
   ⓔ gỡ mọi header `X-Goog-*` / `X-Serverless-Authorization` / `Cookie` trước khi chuyển tiếp — cửa ⛔ thấy gì của IAP
      hay của phiên đăng nhập.
   ⓕ (bổ sung chủ 24/11 ~03:45) ĐĂNG NHẬP FLS — lớp thứ hai SAU IAP: chưa có phiên `__Host-fls_phien` hợp lệ ⇒ API
      `401 FLS-CHUA-DANG-NHAP`, trang ⇒ `303 /login`; cửa ⛔ bị chạm. Chỉ `/login` · `/logout` đi được khi chưa đăng
      nhập ⇒ `phien.js` (thẻ `ke_toan`) chỉ ra SAU đăng nhập. Một tài khoản chung, băm scrypt trong Secret Manager
      `fls-staging-login` — chi tiết + lý do ở `dang_nhap.py`.

⭐ Kiểm ES256 bằng stdlib (P-256 thuần Python): ảnh chạy chỉ có `psycopg` (Dockerfile) — ⛔ thêm `cryptography`
   chỉ cho mấy chục dòng toán. Đúng/sai được ghim bằng VECTƠ CHUẨN RFC 6979 §A.2.5 (bài `test_cong_iap.py`) —
   một nguồn ĐỘC LẬP với mã này — và đã đối chiếu `openssl dgst -sha256 -sign` (BG-364).
⛔ In/ghi nhật ký: ⛔ thẻ, ⛔ JWT, ⛔ chuỗi truy vấn. Chỉ email + phương thức + đường dẫn + mã.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import http.client
import http.server
import json
import os
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # `dang_nhap` · `lay_bi_mat` cùng thư mục (chạy được cả `-I`)
import dang_nhap as DN  # noqa: E402

URL_JWKS_MAC_DINH = "https://www.gstatic.com/iap/verify/public_key-jwk"
ISS_IAP = "https://cloud.google.com/iap"
HEADER_IAP = "X-Goog-IAP-JWT-Assertion"
HEADER_EMAIL = "X-Goog-Authenticated-User-Email"
HOP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailer", "trailers",
       "transfer-encoding", "upgrade", "host", "content-length"}
LECH_GIO = 30            # giây — lệch đồng hồ cho phép với `iat`/`exp`

# ══ P-256 (secp256r1) — tham số chuẩn FIPS 186-4 / SEC 2 ═════════════════════════════════════════════════
_P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
_A = _P - 3
_B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
_G = (0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
      0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)


def tren_duong_cong(q) -> bool:
    x, y = q
    return 0 <= x < _P and 0 <= y < _P and (y * y - (x * x * x + _A * x + _B)) % _P == 0


def _cong(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2 and (y1 + y2) % _P == 0:
        return None
    if p1 == p2:
        m = (3 * x1 * x1 + _A) * pow(2 * y1, -1, _P) % _P
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, _P) % _P
    x3 = (m * m - x1 - x2) % _P
    return x3, (m * (x1 - x3) - y1) % _P


def nhan(k: int, q):
    """k·Q (nhân đôi-và-cộng). ⛔ dùng cho KÝ thật (⛔ thời gian hằng) — ở đây chỉ KIỂM khoá công khai."""
    kq, cur = None, q
    while k:
        if k & 1:
            kq = _cong(kq, cur)
        cur = _cong(cur, cur)
        k >>= 1
    return kq


def kiem_es256(q, bam: bytes, r: int, s: int) -> bool:
    """ECDSA-P256 verify (SEC 1 §4.1.4). `bam` = SHA-256 của thông điệp."""
    if not tren_duong_cong(q) or not (1 <= r < _N and 1 <= s < _N):
        return False
    z = int.from_bytes(bam, "big")
    w = pow(s, -1, _N)
    x = _cong(nhan(z * w % _N, _G), nhan(r * w % _N, q))
    return x is not None and x[0] % _N == r


# ══ JWT ═════════════════════════════════════════════════════════════════════════════════════════════
def _b64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


class KhoaIap:
    """Khoá công khai IAP (JWKS), giữ 1 giờ. Lấy hỏng ⇒ `None` (người gọi trả 503 — ĐÓNG)."""

    def __init__(self, url: str):
        self.url, self.khoa, self.luc, self._kh = url, None, 0.0, threading.Lock()

    def lay(self) -> dict | None:
        with self._kh:
            if self.khoa is None or time.time() - self.luc > 3600:
                try:
                    with urllib.request.urlopen(self.url, timeout=10) as r:       # noqa: S310 — URL cố định/biến môi trường
                        ds = json.loads(r.read().decode("utf-8"))["keys"]
                    k = {}
                    for j in ds:
                        if j.get("kty") == "EC" and j.get("crv") == "P-256":
                            k[j["kid"]] = (int.from_bytes(_b64(j["x"]), "big"), int.from_bytes(_b64(j["y"]), "big"))
                    if k:
                        self.khoa, self.luc = k, time.time()
                except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError) as e:
                    print(f"⛔ IAP_KHOA không lấy được khoá công khai IAP ({type(e).__name__})", file=sys.stderr, flush=True)
            return self.khoa


class JwtSai(Exception):
    pass


def kiem_jwt(jwt: str, khoa: dict, aud: str | None = None, bay_gio: float | None = None) -> dict:
    """Trả claims nếu HỢP LỆ; ⛔ ⇒ `JwtSai(lý do)` (lý do ⛔ chứa JWT)."""
    bay_gio = time.time() if bay_gio is None else bay_gio
    phan = jwt.split(".")
    if len(phan) != 3:
        raise JwtSai("khong_phai_jwt")
    try:
        dau, than, ky = json.loads(_b64(phan[0])), json.loads(_b64(phan[1])), _b64(phan[2])
    except (ValueError, TypeError):
        raise JwtSai("giai_ma_hong")
    if not isinstance(dau, dict) or not isinstance(than, dict):
        raise JwtSai("giai_ma_hong")
    if dau.get("alg") != "ES256":                     # ⛔ `none`/HS256 — chỉ đúng thuật toán IAP dùng
        raise JwtSai("alg")
    q = khoa.get(dau.get("kid"))
    if q is None:
        raise JwtSai("kid_la")
    if len(ky) != 64:
        raise JwtSai("chu_ky_do_dai")
    bam = hashlib.sha256((phan[0] + "." + phan[1]).encode("ascii")).digest()
    if not kiem_es256(q, bam, int.from_bytes(ky[:32], "big"), int.from_bytes(ky[32:], "big")):
        raise JwtSai("chu_ky")
    if than.get("iss") != ISS_IAP:
        raise JwtSai("iss")
    try:
        exp, iat = float(than["exp"]), float(than["iat"])
    except (KeyError, TypeError, ValueError):
        raise JwtSai("thieu_exp_iat")
    if exp < bay_gio - LECH_GIO or iat > bay_gio + LECH_GIO:
        raise JwtSai("het_han")
    if aud and than.get("aud") != aud:
        raise JwtSai("aud")
    if not than.get("email"):
        raise JwtSai("thieu_email")
    return than


# ══ Cổng chuyển tiếp ══════════════════════════════════════════════════════════════════════════════════
class Cong(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def _tay(cong_cua: int, khoa: KhoaIap, aud: str | None, tk: DN.TaiKhoan, khoa_sai: DN.KhoaSai, phien: DN.Phien):
    class Tay(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        server_version = "fls-cong-iap"
        sys_version = ""

        def log_message(self, *a):        # nhật ký riêng ở `_ghi` — ⛔ dòng mặc định (có chuỗi truy vấn)
            pass

        def _ghi(self, email: str, ma: int, ly_do: str = ""):
            duong = self.path.split("?", 1)[0]
            try:
                print(f"IAP_VAO email={email or '-'} {self.command} {duong} {ma}" + (f" ({ly_do})" if ly_do else ""),
                      flush=True)
            except (OSError, ValueError):
                pass

        def _tu_choi(self, ma: int, code: str, ly_do: str):
            b = json.dumps({"data": None, "error": {"code": code, "detail": ly_do}}).encode()
            self.send_response(ma)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(b)
            self._ghi("", ma, ly_do)

        def _tra(self, ma: int, than: bytes = b"", loai: str = "text/html; charset=utf-8", them: dict | None = None):
            self.send_response(ma)
            for k2, v in (them or {}).items():
                self.send_header(k2, v)
            if than:
                self.send_header("Content-Type", loai)
            self.send_header("Content-Length", str(len(than)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if self.command != "HEAD" and than:
                self.wfile.write(than)

        def _dang_nhap(self, email: str, duong: str, than: bytes):
            """Xử lý `/login` (GET màn · POST so khớp) và `/logout`. ⛔ phản chiếu chữ người gõ, ⛔ ghi mật khẩu."""
            if duong == "/logout":
                phien.thu_hoi_the(DN.doc_cookie(self.headers.get("Cookie")))
                print(f"DANG_NHAP email={email} dang_xuat", flush=True)
                return self._tra(303, them={"Location": "/login", "Set-Cookie": DN.cookie_xoa()})
            t = tk.lay()
            if self.command not in ("POST",):
                if t and phien.hop_le(DN.doc_cookie(self.headers.get("Cookie")), email, t["bam"]):
                    return self._tra(303, them={"Location": "/"})
                return self._tra(200, DN.trang("" if t else "⛔ Chưa đặt tài khoản đăng nhập — báo chủ (08_dat_dang_nhap.sh).",
                                               "" if t else "loi"))
            if not t:
                return self._tra(503, DN.trang("⛔ Chưa đặt tài khoản đăng nhập — báo chủ (08_dat_dang_nhap.sh).", "loi"))
            con = khoa_sai.con_khoa(email)
            if con:
                print(f"DANG_NHAP email={email} khoa con={con}s", flush=True)
                return self._tra(429, DN.trang(f"⛔ Sai quá {DN.SAI_TOI_DA} lần — khoá tạm, thử lại sau {(con + 59) // 60} phút.", "loi"),
                                 them={"Retry-After": str(con)})
            if len(than) > 4096:
                return self._tra(413, DN.trang("⛔ Yêu cầu quá dài.", "loi"))
            o = urllib.parse.parse_qs(than.decode("utf-8", "replace"), keep_blank_values=True)
            ten, mk = (o.get("ten") or [""])[0], (o.get("mat_khau") or [""])[0]
            ten_dung = hmac.compare_digest(ten.encode(), str(t["ten"]).encode())
            mk_dung = DN.khop(mk, t["bam"] if ten_dung else DN._bam_moi())    # tên sai vẫn tốn một lần scrypt
            del mk
            if ten_dung and mk_dung:
                khoa_sai.xoa(email)
                print(f"DANG_NHAP email={email} dung", flush=True)
                return self._tra(303, them={"Location": "/", "Set-Cookie": DN.cookie_dat(phien.tao(email, t["bam"]))})
            n = khoa_sai.ghi_sai(email)
            print(f"DANG_NHAP email={email} sai {n}/{DN.SAI_TOI_DA}", flush=True)
            if khoa_sai.con_khoa(email):
                return self._tra(429, DN.trang(f"⛔ Sai quá {DN.SAI_TOI_DA} lần — khoá tạm {DN.KHOA_GIAY // 60} phút.", "loi"),
                                 them={"Retry-After": str(DN.KHOA_GIAY)})
            return self._tra(401, DN.trang("⛔ Sai tên đăng nhập hoặc mật khẩu.", "loi"))

        def _than(self) -> bytes:
            if "chunked" in (self.headers.get("Transfer-Encoding") or "").lower():
                ra = b""
                while True:
                    n = int(self.rfile.readline().split(b";")[0].strip() or b"0", 16)
                    if n == 0:
                        while self.rfile.readline() not in (b"\r\n", b"\n", b""):
                            pass
                        return ra
                    ra += self.rfile.read(n)
                    self.rfile.readline()
            n = int(self.headers.get("Content-Length") or 0)
            return self.rfile.read(n) if n > 0 else b""

        def _di(self):
            than = self._than()
            jwt = self.headers.get(HEADER_IAP)
            if not jwt:
                return self._tu_choi(403, "FLS-IAP-THIEU", "yeu cau ⛔ di qua IAP")
            k = khoa.lay()
            if not k:
                return self._tu_choi(503, "FLS-IAP-KHOA", "⛔ lay duoc khoa cong khai IAP — DONG")
            try:
                claims = kiem_jwt(jwt, k, aud)
            except JwtSai as e:
                return self._tu_choi(403, "FLS-IAP-SAI", f"jwt IAP ⛔ hop le: {e}")
            email = str(claims.get("email"))
            if not getattr(self.server, "da_in_aud", False):
                self.server.da_in_aud = True
                print(f"IAP_AUD {claims.get('aud')}", flush=True)
            # ⓕ ĐĂNG NHẬP FLS — sau IAP, trước cửa.
            duong = self.path.split("?", 1)[0]
            if duong in ("/login", "/logout"):
                return self._dang_nhap(email, duong, than)
            t = tk.lay()
            if not (t and phien.hop_le(DN.doc_cookie(self.headers.get("Cookie")), email, t["bam"])):
                if duong.startswith("/api/") or self.command not in ("GET", "HEAD"):
                    return self._tu_choi(401, "FLS-CHUA-DANG-NHAP", "chua dang nhap FLS (hoac phien het han) — mo /login")
                self._tra(303, them={"Location": "/login"})
                return self._ghi(email, 303, "chua dang nhap")
            dau = {k2: v for k2, v in self.headers.items()
                   if k2.lower() not in HOP and not k2.lower().startswith("x-goog-")
                   and k2.lower() not in ("x-serverless-authorization", "cookie")}
            try:
                c = http.client.HTTPConnection("127.0.0.1", cong_cua, timeout=120)
                c.request(self.command, self.path, body=than if than or self.command in ("POST", "PUT", "PATCH") else None,
                          headers=dau)
                r = c.getresponse()
                b = r.read()
                c.close()
            except OSError as e:
                return self._tu_choi(502, "FLS-CUA-VANG", f"cua 127.0.0.1:{cong_cua} ⛔ tra loi ({type(e).__name__})")
            self.send_response(r.status, r.reason)
            for k2, v in r.getheaders():
                if k2.lower() not in HOP:
                    self.send_header(k2, v)
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(b)
            self._ghi(email, r.status)

        do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_HEAD = do_OPTIONS = _di

    return Tay


TEN_BI_MAT_DANG_NHAP = os.environ.get("FLS_LOGIN_BI_MAT") or "fls-staging-login"


def doc_bi_mat_dang_nhap() -> str:
    """Bản ghi băm từ Secret Manager bằng danh tính SA của Cloud Run (`lay_bi_mat.py`). Hỏng ⇒ "" (⛔ mở cửa)."""
    import lay_bi_mat
    try:
        return lay_bi_mat.lay_bi_mat(TEN_BI_MAT_DANG_NHAP, os.environ.get("FLS_STG_PROJECT", ""),
                                     os.environ.get("FLS_STG_URL_METADATA", lay_bi_mat.MAC_DINH_METADATA),
                                     os.environ.get("FLS_STG_URL_SM", lay_bi_mat.MAC_DINH_SM))
    except SystemExit as e:
        print(f"⛔ DANG_NHAP_BI_MAT {e}", file=sys.stderr, flush=True)
        return ""


def chay_cong(cong: int, cong_cua: int, url_jwks: str, aud: str | None) -> int:
    sv = Cong(("0.0.0.0", cong), _tay(cong_cua, KhoaIap(url_jwks), aud,
                                      DN.TaiKhoan(doc_bi_mat_dang_nhap), DN.KhoaSai(), DN.Phien()))
    print(f"cong_iap: nghe 0.0.0.0:{cong} → 127.0.0.1:{cong_cua} · khoá IAP {url_jwks}"
          + (f" · aud ghim" if aud else " · aud ⛔ ghim"), flush=True)
    try:
        sv.serve_forever()
    finally:
        sv.server_close()
    return 0


# ══ Tự đo (một dòng `TU_DO …` vào nhật ký Cloud Run — `07_link_web.sh` đọc lại bằng `gcloud logging read`) ══
def nghe_tren(cong: int) -> list[str]:
    """Địa chỉ đang LISTEN trên `cong` (đọc /proc/net/tcp{,6} — ảnh slim ⛔ có `ss`)."""
    ra = []
    for tep, v6 in (("/proc/net/tcp", False), ("/proc/net/tcp6", True)):
        try:
            dong = open(tep, encoding="ascii").read().splitlines()[1:]
        except OSError:
            continue
        for l in dong:
            f = l.split()
            if len(f) < 4 or f[3] != "0A":
                continue
            dc, p = f[1].split(":")
            if int(p, 16) != cong:
                continue
            raw = bytes.fromhex(dc)
            if v6:
                b = b"".join(raw[i:i + 4][::-1] for i in range(0, 16, 4))
                ra.append(f"[{socket.inet_ntop(socket.AF_INET6, b)}]:{cong}")
            else:
                ra.append(f"{socket.inet_ntoa(raw[::-1])}:{cong}")
    return sorted(set(ra))


def _ma(cong: int, duong: str, dau: dict | None = None) -> str:
    try:
        c = http.client.HTTPConnection("127.0.0.1", cong, timeout=20)
        c.request("GET", duong, headers=dau or {})
        r = c.getresponse()
        r.read()
        c.close()
        return str(r.status)
    except OSError:
        return "000"


def jwt_gia(kid: str) -> str:
    """JWT ĐÚNG HÌNH nhưng chữ ký RÁC — cổng phải trả 403 (chứng minh đang KIỂM chữ ký, ⛔ chỉ xem có header)."""
    e = lambda o: base64.urlsafe_b64encode(json.dumps(o).encode()).rstrip(b"=").decode()   # noqa: E731
    now = int(time.time())
    return (e({"alg": "ES256", "typ": "JWT", "kid": kid}) + "." +
            e({"iss": ISS_IAP, "aud": "x", "email": "gia@vi-du.invalid", "iat": now, "exp": now + 600}) + "." +
            base64.urlsafe_b64encode(b"\x01" * 64).rstrip(b"=").decode())


def tu_do(cong: int, cong_cua: int, url_jwks: str) -> str:
    k = KhoaIap(url_jwks).lay() or {}
    kid = next(iter(k), "khong-co")
    gt = {
        "revision": os.environ.get("K_REVISION", "-"),
        "man_hinh": _ma(cong_cua, "/"),
        "api_khong_the": _ma(cong_cua, "/api/fls/v1/gates"),
        "nghe_cua": ",".join(nghe_tren(cong_cua)) or "-",
        "cong_khong_iap": _ma(cong, "/"),
        "cong_iap_gia": _ma(cong, "/", {HEADER_IAP: jwt_gia(kid)}),
        "jwks": str(len(k)),
        "dang_nhap": "san_sang" if DN.TaiKhoan(doc_bi_mat_dang_nhap).lay() else "chua_dat",
    }
    return "TU_DO " + " ".join(f"{a}={b}" for a, b in gt.items())


def doi_cua(cong_cua: int, han: float) -> bool:
    """Chờ tới khi cổng TRẢ LỜI MỘT YÊU CẦU HTTP (mã bất kỳ) — chặt hơn "TCP nối được": cổng mở mà tiến trình
    chưa phục vụ (hay một tiến trình KHÁC giữ cổng) ⛔ qua. Cloud Run chỉ đưa yêu cầu vào khi `$PORT` mở, nên
    `$PORT` chỉ mở SAU khi cửa đã trả lời thật."""
    t = time.time() + han
    while time.time() < t:
        if _ma(cong_cua, "/") != "000":
            return True
        time.sleep(0.5)
    return False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cong", type=int, default=int(os.environ.get("PORT") or 0))
    ap.add_argument("--cong-cua", type=int, default=8088)
    ap.add_argument("--doi-cua", action="store_true")
    ap.add_argument("--han", type=float, default=90)
    ap.add_argument("--tu-do", action="store_true")
    a = ap.parse_args(argv)
    url_jwks = os.environ.get("FLS_IAP_URL_JWKS") or URL_JWKS_MAC_DINH
    if a.doi_cua:
        if doi_cua(a.cong_cua, a.han):
            return 0
        print(f"⛔ CUA_VANG cửa 127.0.0.1:{a.cong_cua} ⛔ lên sau {a.han:.0f} giây", file=sys.stderr)
        return 1
    if not os.environ.get("K_SERVICE"):
        print("⛔ cong_iap chỉ chạy TRÊN Cloud Run (thiếu K_SERVICE) — ⛔ mở cổng ra mạng ở nơi không có IAP đứng trước",
              file=sys.stderr)
        return 2
    if not a.cong or a.cong == a.cong_cua:
        print(f"⛔ --cong ({a.cong}) phải khác 0 và khác --cong-cua ({a.cong_cua})", file=sys.stderr)
        return 2
    if a.tu_do:
        print(tu_do(a.cong, a.cong_cua, url_jwks), flush=True)
        return 0
    return chay_cong(a.cong, a.cong_cua, url_jwks, os.environ.get("FLS_IAP_AUD") or None)


if __name__ == "__main__":
    raise SystemExit(main())
