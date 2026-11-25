"""Bài thử CỔNG IAP — `WO-363` AC-2: `tools/staging/app/cong_iap.py` + `vao_cloud_run.sh` CHẠY THẬT.

  ⓐ toán ES256: vectơ CHUẨN RFC 6979 §A.2.5 (nguồn ĐỘC LẬP với mã) — đúng ⇒ True, lệch 1 bit ⇒ False.
  ⓑ `kiem_jwt`: mỗi cách giả (alg none/HS256 · kid lạ · chữ ký · iss · hết hạn · aud ghim · thiếu email · sửa thân) ⇒ từ chối.
  ⓒ tiến trình cổng thật (cửa = máy chủ HTTP ghi lại header): ⛔ JWT ⇒ 403 + cửa ⛔ bị chạm · JWT giả ⇒ 403 ·
     JWT đúng ⇒ chuyển tiếp, `Authorization` NGUYÊN VẸN, `X-Goog-*` bị gỡ · khoá IAP ⛔ lấy được ⇒ 503 (ĐÓNG) ·
     ngoài Cloud Run (⛔ `K_SERVICE`) ⇒ từ chối khởi động · nhật ký ⛔ có thẻ/JWT/chuỗi truy vấn.
  ⓓ `vao_cloud_run.sh` + `vao.sh` + cửa THẬT vào kho scratch: dòng `TU_DO` đúng mong · qua cổng với JWT IAP đúng mà
     ⛔ thẻ FLS ⇒ 401 (cửa vẫn gác) · có thẻ ⇒ 200 · cửa CHỈ nghe loopback · cửa chết ⇒ container thoát.
"""
from __future__ import annotations

import base64
import hashlib
import http.server
import json
import os
import secrets
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import http.client

import pytest

from tests.staging import ho_tro as H

APP = H.STG / "app"
sys.path.insert(0, str(APP))
import cong_iap as C  # noqa: E402
import dang_nhap as DN  # noqa: E402

# ══ ⓐ ES256 — RFC 6979 §A.2.5 (P-256, SHA-256) ═════════════════════════════════════════════════════════
RFC_X = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
RFC_Q = (0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6,
         0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299)
RFC_SIG = {b"sample": (0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716,
                       0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8),
           b"test": (0xF1ABB023518351CD71D881567B1EA663ED3EFCF6C5132B354F28D3B0B7D38367,
                     0x019F4113742A2B14BD25926B49C649155F267E60D3814B4C0CC84250E46F0083)}


def test_es256_vecto_RFC6979_dung_DAT_lech_1_bit_TU_CHOI():
    assert C.nhan(RFC_X, C._G) == RFC_Q, "khoá công khai RFC = x·G — phép nhân điểm sai"
    for m, (r, s) in RFC_SIG.items():
        h = hashlib.sha256(m).digest()
        assert C.kiem_es256(RFC_Q, h, r, s), m
        assert not C.kiem_es256(RFC_Q, h, r ^ 1, s) and not C.kiem_es256(RFC_Q, h, r, s ^ 1)
        assert not C.kiem_es256(RFC_Q, hashlib.sha256(m + b"!").digest(), r, s)
    assert not C.kiem_es256((RFC_Q[0], RFC_Q[1] ^ 1), hashlib.sha256(b"test").digest(), *RFC_SIG[b"test"]), "điểm ngoài đường cong"
    assert not C.kiem_es256(RFC_Q, b"\0" * 32, 0, 1) and not C.kiem_es256(RFC_Q, b"\0" * 32, C._N, 1)


# ══ ⓑ JWT ═════════════════════════════════════════════════════════════════════════════════════════════
KHOA_BI_MAT = secrets.randbelow(C._N - 1) + 1
KHOA_CONG = C.nhan(KHOA_BI_MAT, C._G)
KID = "kid-gia-1"


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def ky(than: dict, dau: dict | None = None, d: int = KHOA_BI_MAT) -> str:
    """Ký ES256 (ECDSA thường, k ngẫu nhiên) — CHỈ cho bài thử."""
    dau = dau or {"alg": "ES256", "typ": "JWT", "kid": KID}
    vao = _b64(json.dumps(dau).encode()) + "." + _b64(json.dumps(than).encode())
    z = int.from_bytes(hashlib.sha256(vao.encode()).digest(), "big")
    while True:
        k = secrets.randbelow(C._N - 1) + 1
        r = C.nhan(k, C._G)[0] % C._N
        s = pow(k, -1, C._N) * (z + r * d) % C._N
        if r and s:
            return vao + "." + _b64(r.to_bytes(32, "big") + s.to_bytes(32, "big"))


def than_dung(**sua):
    now = int(time.time())
    t = {"iss": C.ISS_IAP, "aud": "/projects/1/locations/r/services/s", "email": "nguoi@vi-du.vn",
         "sub": "accounts.google.com:1", "iat": now, "exp": now + 600}
    t.update(sua)
    return {k: v for k, v in t.items() if v is not None}


def test_kiem_jwt_dung_tra_claims_va_tu_kiem_chu_ky_cua_bai():
    c = C.kiem_jwt(ky(than_dung()), {KID: KHOA_CONG})
    assert c["email"] == "nguoi@vi-du.vn"


@pytest.mark.parametrize("ten,jwt_f,aud,ly_do", [
    ("alg none", lambda: _b64(b'{"alg":"none","kid":"kid-gia-1"}') + "." + _b64(json.dumps(than_dung()).encode()) + ".", None, "alg"),
    ("alg HS256", lambda: ky(than_dung(), {"alg": "HS256", "kid": KID}), None, "alg"),
    ("kid lạ", lambda: ky(than_dung(), {"alg": "ES256", "kid": "khac"}), None, "kid_la"),
    ("khoá khác ký", lambda: ky(than_dung(), d=12345), None, "chu_ky"),
    ("iss lạ", lambda: ky(than_dung(iss="https://ke-gia.vi-du.vn")), None, "iss"),
    ("hết hạn", lambda: ky(than_dung(exp=int(time.time()) - 3600, iat=int(time.time()) - 7200)), None, "het_han"),
    ("iat tương lai", lambda: ky(than_dung(iat=int(time.time()) + 3600, exp=int(time.time()) + 7200)), None, "het_han"),
    ("aud ghim khác", lambda: ky(than_dung()), "/projects/2/x", "aud"),
    ("thiếu email", lambda: ky(than_dung(email=None)), None, "thieu_email"),
    ("sửa thân sau ký", lambda: (lambda j: j.split(".")[0] + "." + _b64(json.dumps(than_dung(email="ke@gia.vn")).encode())
                                 + "." + j.split(".")[2])(ky(than_dung())), None, "chu_ky"),
    ("không phải JWT", lambda: "abc", None, "khong_phai_jwt"),
])
def test_kiem_jwt_moi_cach_gia_deu_TU_CHOI(ten, jwt_f, aud, ly_do):
    with pytest.raises(C.JwtSai) as e:
        C.kiem_jwt(jwt_f(), {KID: KHOA_CONG}, aud)
    assert str(e.value) == ly_do, ten


# ══ ⓒ tiến trình cổng thật ═════════════════════════════════════════════════════════════════════════════
class _May(http.server.ThreadingHTTPServer):
    daemon_threads = True


def _jwks_sv(hong=False):
    class T(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def do_GET(self):
            if hong:
                self.send_response(500); self.end_headers(); return
            b = json.dumps({"keys": [{"kty": "EC", "crv": "P-256", "alg": "ES256", "kid": KID,
                                      "x": _b64(KHOA_CONG[0].to_bytes(32, "big")),
                                      "y": _b64(KHOA_CONG[1].to_bytes(32, "big"))}]}).encode()
            self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    sv = _May(("127.0.0.1", 0), T)
    threading.Thread(target=sv.serve_forever, daemon=True).start()
    return sv


def _cua_gia():
    """'Cửa' giả: ghi lại MỌI yêu cầu (phương thức, đường, header, thân); trả 207 + thân JSON có dấu."""
    class T(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a): pass

        def _di(self):
            n = int(self.headers.get("Content-Length") or 0)
            self.server.thay.append((self.command, self.path, dict(self.headers), self.rfile.read(n) if n else b""))
            b = b'{"data":"tu-cua"}'
            self.send_response(207); self.send_header("Content-Length", str(len(b))); self.send_header("X-Tu-Cua", "1")
            self.end_headers(); self.wfile.write(b)
        do_GET = do_POST = _di
    sv = _May(("127.0.0.1", 0), T)
    sv.thay = []
    threading.Thread(target=sv.serve_forever, daemon=True).start()
    return sv


def _cong_trong():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def _doi(cong, han=20):
    t = time.time() + han
    while time.time() < t:
        try:
            socket.create_connection(("127.0.0.1", cong), timeout=1).close(); return True
        except OSError:
            time.sleep(0.2)
    return False


def _goi(cong, duong="/", dau=None, ph="GET", than=None):
    """Một yêu cầu, ⛔ đi theo chuyển hướng (303 → /login phải THẤY được)."""
    c = http.client.HTTPConnection("127.0.0.1", cong, timeout=20)
    c.request(ph, duong, body=than, headers=dau or {})
    r = c.getresponse()
    b = r.read()
    c.close()
    return r.status, b, {k: v for k, v in r.getheaders()}


TEN_DN = "HondurasGesha"
MK_THU = "mat-khau-THU-chi-cho-bai-7f3a"          # chuỗi dễ nhận để quét rò rỉ — ⛔ mật khẩu thật
BAN_GHI_DN = json.dumps({"ten": TEN_DN, "bam": DN.bam(MK_THU)})


def _dang_nhap(cong, jwt, ten=TEN_DN, mk=MK_THU):
    than = urllib.parse.urlencode({"ten": ten, "mat_khau": mk}).encode()
    return _goi(cong, "/login", {C.HEADER_IAP: jwt, "Content-Type": "application/x-www-form-urlencoded"}, "POST", than)


def _cookie(hd):
    sc = hd.get("Set-Cookie", "")
    return sc.split(";", 1)[0], sc


class SmGia(http.server.ThreadingHTTPServer):
    """Metadata server + Secret Manager GIẢ có GHI — mô phỏng đúng 3 lời REST cổng gọi: `versions/latest:access` (trả
    `name` = `projects/<SỐ>/secrets/<s>/versions/<N>`) · `secrets/<s>:addVersion` · `…/versions/<N>:destroy`. Huỷ
    phiên bản đang là mới nhất ⇒ đọc lại ra phiên bản trước (như GCP: `latest` = bản mới nhất CHƯA huỷ). Sống ngoài
    tiến trình cổng ⇒ dùng chung qua các lần "khởi động lại" (`STG-WEB-R1-02`). `ghi_hong=True` ⇒ addVersion 403."""
    daemon_threads = True


def sm_gia(bi_mat: dict[str, str]):
    import base64 as b64
    import re as _re

    class T(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def _ra(self, ma, o):
            b = json.dumps(o).encode()
            self.send_response(ma); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

        def _tok(self):
            return self.headers.get("Authorization") == "Bearer TOKEN-GIA-123"

        def do_GET(self):
            if self.path == "/computeMetadata/v1/instance/service-accounts/default/token":
                return self._ra(200, {"access_token": "TOKEN-GIA-123", "expires_in": 3000})
            m = _re.fullmatch(r"/v1/projects/[^/]+/secrets/([^/]+)/versions/latest:access", self.path)
            if m and self._tok():
                ds = [(n, v) for n, v in enumerate(self.server.kho.get(m[1], []), 1) if v is not None]
                if not ds:
                    return self._ra(404, {})
                n, v = ds[-1]
                return self._ra(200, {"name": f"projects/123/secrets/{m[1]}/versions/{n}",
                                      "payload": {"data": b64.b64encode(v.encode()).decode()}})
            self._ra(403, {})

        def do_POST(self):
            than = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            if not self._tok():
                return self._ra(403, {})
            m = _re.fullmatch(r"/v1/projects/[^/]+/secrets/([^/:]+):addVersion", self.path)
            if m:
                if self.server.ghi_hong or m[1] not in self.server.kho:
                    return self._ra(403, {})
                self.server.kho[m[1]].append(b64.b64decode(than["payload"]["data"]).decode())
                self.server.so_ghi += 1
                return self._ra(200, {"name": f"projects/123/secrets/{m[1]}/versions/{len(self.server.kho[m[1]])}"})
            m = _re.fullmatch(r"/v1/projects/123/secrets/([^/]+)/versions/(\d+):destroy", self.path)
            if m:
                self.server.kho[m[1]][int(m[2]) - 1] = None
                self.server.so_huy += 1
                return self._ra(200, {})
            self._ra(404, {})

    sv = SmGia(("127.0.0.1", 0), T)
    sv.kho = {k: [v] for k, v in bi_mat.items()}
    sv.ghi_hong, sv.so_ghi, sv.so_huy = False, 0, 0
    threading.Thread(target=sv.serve_forever, daemon=True).start()
    return sv


TRANG_THAI_DN = json.dumps(DN.trang_thai_moi())


def _moi_trang_thai() -> str:
    return json.dumps(DN.trang_thai_moi())


@pytest.fixture
def cong_chay():
    dang = []

    def chay(jwks_hong=False, env_them=None, ban_ghi=BAN_GHI_DN, trang_thai=True, sm=None, cua=None):
        jw = _jwks_sv(jwks_hong)
        cua = cua or _cua_gia()
        if sm is None:
            bm = {}
            if ban_ghi:
                bm["fls-staging-login"] = ban_ghi
            if trang_thai:
                bm["fls-staging-phien"] = _moi_trang_thai()
            sm = sm_gia(bm)
        cua.sm = sm
        cong = _cong_trong()
        env = dict(os.environ, K_SERVICE="fls-staging-web", PYTHONUTF8="1",
                   FLS_IAP_URL_JWKS=f"http://127.0.0.1:{jw.server_port}/jwk", FLS_STG_PROJECT="du-an-gia",
                   FLS_STG_URL_METADATA=f"http://127.0.0.1:{sm.server_port}", FLS_STG_URL_SM=f"http://127.0.0.1:{sm.server_port}")
        env.update(env_them or {})
        p = subprocess.Popen([sys.executable, "-I", str(APP / "cong_iap.py"), "--cong", str(cong),
                              "--cong-cua", str(cua.server_port)], env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        dang.append((p, jw, cua, sm))
        assert _doi(cong), p.communicate(timeout=5)
        return p, cong, cua
    yield chay
    for p, jw, cua, sm in dang:
        if p.poll() is None:
            p.terminate()
            try:
                p.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                p.kill()
        jw.shutdown()
    for _, _, cua, sm in dang:
        cua.shutdown(); sm.shutdown()


def _xong(p):
    p.terminate()
    out, err = p.communicate(timeout=10)
    return out + err


def test_cong_khong_JWT_hay_JWT_gia_thi_403_va_CUA_KHONG_bi_cham(cong_chay):
    p, cong, cua = cong_chay()
    ma, than, _ = _goi(cong, "/api/fls/v1/gates", {"Authorization": "Bearer the-fls-gia"})
    assert ma == 403 and json.loads(than)["error"]["code"] == "FLS-IAP-THIEU"
    assert _goi(cong, "/", {C.HEADER_IAP: C.jwt_gia(KID)})[0] == 403
    assert _goi(cong, "/", {C.HEADER_IAP: ky(than_dung(), d=777)})[0] == 403, "ký bằng khoá KHÁC"
    assert _goi(cong, "/", {C.HEADER_IAP: ky(than_dung(exp=1, iat=0))})[0] == 403, "hết hạn"
    assert _goi(cong, "/", {C.HEADER_IAP: "a.b.c"}, ph="POST", than=b"{}")[0] == 403
    assert cua.thay == [], f"cửa bị chạm khi ⛔ qua IAP: {cua.thay}"
    log = _xong(p)
    assert "the-fls-gia" not in log


def test_cong_JWT_dung_thi_chuyen_tiep_Authorization_NGUYEN_VEN_go_X_Goog_va_ghi_ai_vao(cong_chay):
    p, cong, cua = cong_chay()
    jwt = ky(than_dung())
    ck, _ = _cookie(_dang_nhap(cong, jwt)[2])
    dau = {C.HEADER_IAP: jwt, "Authorization": "Bearer the-fls-123", C.HEADER_EMAIL: "accounts.google.com:nguoi@vi-du.vn",
           "X-Serverless-Authorization": "Bearer noi-bo", "Content-Type": "application/json", "Cookie": ck}
    ma, than, hd = _goi(cong, "/api/fls/v1/ledger?bi_mat_trong_query=1", dau)
    assert (ma, than) == (207, b'{"data":"tu-cua"}') and hd.get("X-Tu-Cua") == "1", "mã/thân/header của cửa phải về NGUYÊN"
    ma2, _, _ = _goi(cong, "/api/fls/v1/config/fx/202601/sign", dau, ph="POST", than=b'{"x":1}')
    assert ma2 == 207
    (m1, d1, h1, b1), (m2, d2, h2, b2) = cua.thay
    assert (m1, d1) == ("GET", "/api/fls/v1/ledger?bi_mat_trong_query=1") and (m2, d2, b2) == ("POST", "/api/fls/v1/config/fx/202601/sign", b'{"x":1}')
    assert h1.get("Authorization") == "Bearer the-fls-123", "thẻ FLS phải đi qua NGUYÊN VẸN (cửa vẫn là nơi xét thẻ)"
    assert not [k for k in h1 if k.lower().startswith("x-goog-") or k.lower() in ("x-serverless-authorization", "cookie")], h1
    log = _xong(p)
    assert "IAP_VAO email=nguoi@vi-du.vn GET /api/fls/v1/ledger 207" in log
    assert "IAP_VAO email=nguoi@vi-du.vn POST /api/fls/v1/config/fx/202601/sign 207" in log
    assert "IAP_AUD /projects/1/locations/r/services/s" in log
    assert jwt not in log and jwt.split(".")[2] not in log and "the-fls-123" not in log and "bi_mat_trong_query" not in log


def test_cong_KHONG_lay_duoc_khoa_IAP_thi_503_DONG(cong_chay):
    p, cong, cua = cong_chay(jwks_hong=True)
    ma, than, _ = _goi(cong, "/", {C.HEADER_IAP: ky(than_dung())})
    assert ma == 503 and json.loads(than)["error"]["code"] == "FLS-IAP-KHOA"
    assert _dang_nhap(cong, ky(than_dung()))[0] == 503, "khoá IAP hỏng ⇒ cả /login cũng ĐÓNG"
    assert cua.thay == []


def test_cong_aud_GHIM_thi_aud_khac_403(cong_chay):
    p, cong, cua = cong_chay(env_them={"FLS_IAP_AUD": "/projects/9/khac"})
    assert _goi(cong, "/", {C.HEADER_IAP: ky(than_dung())})[0] == 403 and cua.thay == []


def test_cong_TU_CHOI_khoi_dong_ngoai_Cloud_Run_hoac_cong_trung_cong_cua():
    env = {k: v for k, v in os.environ.items() if k != "K_SERVICE"}
    r = subprocess.run([sys.executable, "-I", str(APP / "cong_iap.py"), "--cong", "18089", "--cong-cua", "18088"],
                       env=env, capture_output=True, text=True, timeout=30)
    assert r.returncode == 2 and "K_SERVICE" in r.stderr
    r2 = subprocess.run([sys.executable, "-I", str(APP / "cong_iap.py"), "--cong", "18088", "--cong-cua", "18088"],
                        env=dict(env, K_SERVICE="x"), capture_output=True, text=True, timeout=30)
    assert r2.returncode == 2 and "--cong-cua" in r2.stderr


# ══ ⓓ vao_cloud_run.sh + vao.sh + cửa THẬT (kho scratch) ═════════════════════════════════════════════════
def test_vao_cloud_run_cua_that_TU_DO_dung_mong_va_cua_van_gac_the(kho_san):
    from tests.staging.test_03_dung_app import JWT_GIA, _cay_tien_trinh, _the
    sv = sm_gia({"fls-staging-jwt-secret": JWT_GIA, "fls-staging-pg-fls_doc": H.MK["fls-staging-pg-fls_doc"],
                 "fls-staging-login": BAN_GHI_DN, "fls-staging-phien": _moi_trang_thai()})
    jw = _jwks_sv()
    cong, cong_cua = _cong_trong(), _cong_trong()
    gia = kho_san["gia"]["dir"]
    proxy = gia / "proxy-run"
    proxy.write_text("#!/usr/bin/env bash\nexec sleep 600\n"); proxy.chmod(0o755)
    env = dict(os.environ, PORT=str(cong), K_SERVICE="fls-staging-web", K_REVISION="fls-staging-web-00001-thu",
               FLS_STG_PROJECT="du-an-gia", FLS_STG_CONN="du-an-gia:asia-southeast1:fls-staging", FLS_STG_CHE_DO="doc",
               FLS_STG_CONG_PROXY=str(H.cong_pg()), FLS_STG_CONG=str(cong_cua), FLS_STG_KHO=kho_san["kho"],
               FLS_STG_PYTHON=sys.executable, FLS_STG_PROXY=str(proxy),
               FLS_STG_URL_METADATA=f"http://127.0.0.1:{sv.server_port}", FLS_STG_URL_SM=f"http://127.0.0.1:{sv.server_port}",
               FLS_IAP_URL_JWKS=f"http://127.0.0.1:{jw.server_port}/jwk", PYTHONUTF8="1")
    for k in ("PG_DSN", "PG_DSN_TEST", "PGPASSWORD", "FLS_JWT_SECRET", "FLS_STG_ACTOR"):
        env.pop(k, None)
    p = subprocess.Popen(["bash", str(APP / "vao_cloud_run.sh")], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)
    dong_ra: list[str] = []
    threading.Thread(target=lambda: dong_ra.extend(iter(p.stdout.readline, "")), daemon=True).start()
    try:
        # ⭐ CHỜ dòng `TU_DO` trước khi gọi/giết cửa. Bản đầu chỉ chờ cổng mở ⇒ bài gọi xong và GIẾT cửa trước khi
        #   `TU_DO` (khởi động python + lấy khoá IAP) kịp đo ⇒ `man_hinh=000` **4/10 lượt** — chập chờn của BÀI, ⛔ của mã.
        t = time.time() + 60
        while time.time() < t and not any(l.startswith("TU_DO ") for l in dong_ra) and p.poll() is None:
            time.sleep(0.2)
        assert any(l.startswith("TU_DO ") for l in dong_ra), "⛔ có dòng TU_DO sau 60 giây"
        assert _doi(cong, 5), "cổng ⛔ mở"
        jwt = ky(than_dung())
        assert _goi(cong, "/", {C.HEADER_IAP: jwt})[:1] == (303,), "chưa đăng nhập FLS ⇒ chuyển /login"
        assert _goi(cong, "/phien.js", {C.HEADER_IAP: jwt})[0] == 303, "thẻ `ke_toan` ⛔ ra trước đăng nhập"
        ck, _ = _cookie(_dang_nhap(cong, jwt)[2])
        iap = {C.HEADER_IAP: jwt, "Cookie": ck}
        assert _goi(cong, "/", iap)[0] == 200, "màn hình qua cổng"
        assert _goi(cong, "/phien.js", iap)[0] == 200, "sau đăng nhập mới phát thẻ"
        assert _goi(cong, "/api/fls/v1/gates", iap)[0] == 401, "⛔ thẻ FLS ⇒ cửa VẪN 401 dù đã qua IAP"
        the = _the(kho_san)
        assert _goi(cong, "/api/fls/v1/gates", dict(iap, Authorization=f"Bearer {the}"))[0] == 200
        assert _goi(cong, "/api/fls/v1/gates", {"Authorization": f"Bearer {the}"})[0] == 403, "thẻ FLS ⛔ thay được IAP"
        assert C.nghe_tren(cong_cua) == [f"127.0.0.1:{cong_cua}"], "cửa CHỈ nghe loopback"
        assert C.nghe_tren(cong) == [f"0.0.0.0:{cong}"], "chỉ cổng IAP nghe ngoài loopback"
        assert len(_cay_tien_trinh(p.pid)) >= 4, "bash + vao.sh + proxy + cửa + cổng"
        # cửa chết ⇒ container thoát ≠ 0 (⛔ cổng sống mà cửa chết)
        cua_pid = next(int(d) for d in _cay_tien_trinh(p.pid)
                       if "chay_cua.py" in open(f"/proc/{d}/cmdline", "rb").read().decode("utf-8", "ignore"))
        os.kill(cua_pid, signal.SIGKILL)
        p.wait(timeout=30)
        assert p.returncode != 0
    finally:
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
        err = p.stderr.read()
        sv.shutdown(); jw.shutdown()
    time.sleep(0.3)
    out = "".join(dong_ra)
    dong = [l for l in out.splitlines() if l.startswith("TU_DO ")]
    assert len(dong) == 1, out[-2000:] + err[-2000:]
    tu = dict(x.split("=", 1) for x in dong[0].split()[1:])
    assert tu == {"revision": "fls-staging-web-00001-thu", "man_hinh": "200", "api_khong_the": "401",
                  "nghe_cua": f"127.0.0.1:{cong_cua}", "cong_khong_iap": "403", "cong_iap_gia": "403", "jwks": "1", "dang_nhap": "san_sang",
                  "trang_thai": "san_sang", "aud": "chua_ghim"}, tu
    assert JWT_GIA not in out + err and "MKGIA" not in out + err and MK_THU not in out + err


def test_vao_cloud_run_TU_CHOI_ngoai_Cloud_Run_va_PORT_trung_cong_cua():
    env = {k: v for k, v in os.environ.items() if k not in ("K_SERVICE", "PORT")}
    r = subprocess.run(["bash", str(APP / "vao_cloud_run.sh")], env=dict(env, PORT="8080"), capture_output=True, text=True, timeout=30)
    assert r.returncode != 0 and "K_SERVICE" in r.stderr
    r2 = subprocess.run(["bash", str(APP / "vao_cloud_run.sh")], env=dict(env, PORT="8088", K_SERVICE="x"),
                        capture_output=True, text=True, timeout=30)
    assert r2.returncode == 2 and "trùng" in r2.stderr


def test_tinh_vao_cloud_run_KHONG_dua_PORT_cho_cua_va_KHONG_doi_dia_chi_cua():
    s = (APP / "vao_cloud_run.sh").read_text(encoding="utf-8")
    ma = "\n".join(l for l in s.splitlines() if not l.lstrip().startswith("#"))
    assert "--dia-chi" not in ma and "0.0.0.0" not in ma
    assert 'FLS_STG_CONG="$CONG_CUA" bash' in ma and "FLS_STG_CONG=\"$PORT\"" not in ma
    assert 'ENTRYPOINT ["bash", "/app/tools/staging/app/vao.sh"]' in (H.GOC / "Dockerfile").read_text(encoding="utf-8"), \
        "đường VM (bước 03) giữ nguyên điểm vào"


# ══ ⓔ ĐĂNG NHẬP FLS sau IAP (bổ sung chủ 24/11 ~03:45) ═════════════════════════════════════════════════
def test_bam_scrypt_khop_dung_sai_va_ban_ghi_hong():
    b = DN.bam(MK_THU)
    assert b.startswith("scrypt$16384$8$1$") and MK_THU not in b
    assert DN.khop(MK_THU, b) and not DN.khop(MK_THU + "x", b) and not DN.khop("", b)
    assert DN.bam(MK_THU) != b, "muối ngẫu nhiên — hai lần băm khác nhau"
    for hong in ("", "bcrypt$x", b.replace("scrypt", "md5"), "scrypt$1048577$8$1$AAAAAAAAAAA$AAAAAAAAAAAAAAAAAAAAAA",
                 "scrypt$16384$8$1$x$y"):
        assert not DN.khop(MK_THU, hong), hong
    nguon = (APP / "dang_nhap.py").read_text(encoding="utf-8")
    assert nguon.count("hmac.compare_digest") >= 2 and "== h" not in nguon, "so khớp thời gian hằng"


def test_khoa_tam_sau_5_lan_sai_theo_tung_email__toan_cuc_20__het_khoa():
    st = DN.trang_thai_moi()
    now = 1000.0
    for i in range(1, 5):
        assert DN.ghi_sai(st, "a@x", now) == i and DN.con_khoa(st, "a@x", now) == 0
    assert DN.ghi_sai(st, "a@x", now) == 5
    assert DN.con_khoa(st, "a@x", now) == DN.KHOA_GIAY and DN.con_khoa(st, "b@x", now) == 0, "khoá theo email"
    assert DN.con_khoa(st, "a@x", now + DN.KHOA_GIAY + 1) == 0
    st = DN.trang_thai_moi()
    for i in range(DN.SAI_TOAN_CUC - 1):                    # 19 email khác nhau, mỗi email 1 lần sai
        DN.ghi_sai(st, f"e{i}@x", now)
    assert DN.con_khoa(st, "moi@x", now) == 0
    DN.ghi_sai(st, "e99@x", now)                           # lần sai thứ 20 toàn cục ⇒ khoá CHUNG (`STG-WEB-R1-07`)
    assert DN.con_khoa(st, "moi@x", now) == DN.KHOA_GIAY, "nhiều tài khoản Google ⛔ nhân hạn mức đoán"
    st = DN.trang_thai_moi()
    for _ in range(4):
        DN.ghi_sai(st, "c@x", now)
    assert DN.ghi_sai(st, "c@x", now + DN.CUA_SO_GIAY + 1) == 1, "lần sai cũ ngoài cửa sổ ⛔ tính"


def test_phien_gan_email_het_han_sua_dang_xuat_va_doi_khoa():
    st = DN.trang_thai_moi()
    t = DN.tao_phien(st, "a@x", 1000)
    assert DN.phien_hop_le(t, "a@x", st, 1001)
    assert not DN.phien_hop_le(t, "b@x", st, 1001), "cookie mang sang tài khoản Google khác"
    assert not DN.phien_hop_le(t[:-2] + ("AA" if not t.endswith("AA") else "BB"), "a@x", st, 1001), "sửa chữ ký"
    assert not DN.phien_hop_le(t, "a@x", DN.trang_thai_moi(), 1001), "khoá mới (08 đổi mật khẩu) ⇒ phiên cũ mất"
    assert not DN.phien_hop_le(None, "a@x", st, 1001) and not DN.phien_hop_le("rac", "a@x", st, 1001)
    assert not DN.phien_hop_le(t, "a@x", None, 1001), "⛔ đọc được trạng thái ⇒ ĐÓNG"
    assert not DN.phien_hop_le(t, "a@x", st, 1000 + DN.PHIEN_GIAY + 1), "hết hạn"
    DN.dang_xuat(st, "a@x")
    assert not DN.phien_hop_le(t, "a@x", st, 1001), "đã đăng xuất (thế hệ +1)"
    assert DN.phien_hop_le(DN.tao_phien(st, "a@x", 1000), "a@x", st, 1001), "phiên MỚI sau đăng xuất vẫn được"


def test_khoa_HMAC_KHONG_suy_tu_ban_ghi_bam__STG_WEB_R1_06():
    """Đọc được `fls-staging-login` (bản ghi băm) ⛔ đủ để rèn cookie: khoá HMAC là 32 byte ngẫu nhiên ở bí mật KHÁC."""
    st = DN.trang_thai_moi()
    rec = json.loads(BAN_GHI_DN)
    import hashlib as hl
    import hmac as hm
    than = f"v2.0.{int(time.time()) + 3600}.{DN._b64(b'ke-gia@x')}"
    for khoa in (hl.sha256(b"fls-phien-v1|" + rec["bam"].encode()).digest(), rec["bam"].encode()):
        gia = than + "." + DN._b64(hm.new(khoa, than.encode(), hl.sha256).digest())
        assert not DN.phien_hop_le(gia, "ke-gia@x", st, time.time())
    nguon = (APP / "dang_nhap.py").read_text(encoding="utf-8")
    assert 'b"fls-phien-v1|"' not in nguon and "_khoa(ban_ghi_bam" not in nguon


def test_kiem_dang_nhap_DUNG_MOT_lan_scrypt_ca_ten_dung_lan_sai_va_KHONG_so_bang_bang(monkeypatch):
    """`STG-WEB-R1-04`: bằng chứng DƯƠNG — đếm lần gọi scrypt (tên sai mà bỏ scrypt ⇒ 0 ⇒ ĐỎ) + AST cấm `==`/`!=`."""
    import ast
    t = json.loads(BAN_GHI_DN)
    dem = []
    goc = DN.hashlib.scrypt
    monkeypatch.setattr(DN.hashlib, "scrypt", lambda *a, **k: (dem.append(1), goc(*a, **k))[1])
    for ten, mk, mong in ((TEN_DN, MK_THU, True), (TEN_DN, "sai", False), ("TenKhac", MK_THU, False), ("", "", False)):
        dem.clear()
        assert DN.kiem_dang_nhap(ten, mk, t) is mong
        assert len(dem) == 1, f"{ten!r}: {len(dem)} lần scrypt (mong 1 — thời gian hằng)"
    cay = ast.parse((APP / "dang_nhap.py").read_text(encoding="utf-8"))
    for ham in [n for n in ast.walk(cay) if isinstance(n, ast.FunctionDef) and n.name in ("kiem_dang_nhap", "khop", "phien_hop_le")]:
        ss = [n for n in ast.walk(ham) if isinstance(n, ast.Compare) and any(isinstance(o, (ast.Eq, ast.NotEq)) for o in n.ops)
              and not any(isinstance(c, ast.Constant) for c in [n.left, *n.comparators])
              and not (ham.name == "phien_hop_le" and "the_he" in ast.unparse(n))]
        assert not ss, f"{ham.name}: so `==` giữa dữ liệu bí mật: {[ast.unparse(x) for x in ss]}"


def test_cong_CHUA_dang_nhap_API_401_trang_303_login_va_CUA_KHONG_bi_cham(cong_chay):
    p, cong, cua = cong_chay()
    jwt = ky(than_dung())
    ma, than, _ = _goi(cong, "/api/fls/v1/gates", {C.HEADER_IAP: jwt, "Authorization": "Bearer the-fls"})
    assert ma == 401 and json.loads(than)["error"]["code"] == "FLS-CHUA-DANG-NHAP"
    ma, _, hd = _goi(cong, "/", {C.HEADER_IAP: jwt})
    assert ma == 303 and hd["Location"] == "/login"
    assert _goi(cong, "/phien.js", {C.HEADER_IAP: jwt})[0] == 303
    assert _goi(cong, "/api/fls/v1/config/fx/202601/sign", {C.HEADER_IAP: jwt}, "POST", b"{}")[0] == 401
    ma, than, hd = _goi(cong, "/login", {C.HEADER_IAP: jwt})
    assert ma == 200 and b'name="mat_khau"' in than and b'type="password"' in than and b"<script" not in than
    assert _goi(cong, "/login")[0] == 403, "/login cũng nằm SAU IAP"
    assert _goi(cong, "/", {C.HEADER_IAP: jwt, "Cookie": f"{DN.COOKIE}=v1.9999999999.YUB4.gia"})[0] == 303, "cookie giả"
    assert cua.thay == [], cua.thay


def test_cong_dang_nhap_DUNG_dat_cookie_an_toan_roi_di_qua__dang_xuat_thu_hoi(cong_chay):
    p, cong, cua = cong_chay()
    jwt = ky(than_dung())
    ma, _, hd = _dang_nhap(cong, jwt)
    assert ma == 303 and hd["Location"] == "/"
    ck, sc = _cookie(hd)
    assert ck.startswith(DN.COOKIE + "=v2.0."), "khuôn v2.<thế hệ>.… (R1-02: thế hệ phiên bền)"
    for c in ("HttpOnly", "Secure", "SameSite=Strict", "Path=/", f"Max-Age={DN.PHIEN_GIAY}"):
        assert c in sc, (c, sc)
    assert _goi(cong, "/api/fls/v1/gates", {C.HEADER_IAP: jwt, "Cookie": ck})[0] == 207
    assert _goi(cong, "/login", {C.HEADER_IAP: jwt, "Cookie": ck})[:1] == (303,), "đã đăng nhập ⇒ về /"
    khac = ky(than_dung(email="nguoi-khac@vi-du.vn"))
    assert _goi(cong, "/api/fls/v1/gates", {C.HEADER_IAP: khac, "Cookie": ck})[0] == 401, "cookie ⛔ dùng được cho email IAP khác"
    ma, _, hd = _goi(cong, "/logout", {C.HEADER_IAP: jwt, "Cookie": ck})
    assert ma == 303 and hd["Location"] == "/login" and "Max-Age=0" in hd["Set-Cookie"]
    assert _goi(cong, "/api/fls/v1/gates", {C.HEADER_IAP: jwt, "Cookie": ck})[0] == 401, "phiên đã thu hồi"
    assert len(cua.thay) == 1
    log = _xong(p)
    assert "DANG_NHAP email=nguoi@vi-du.vn dung" in log and "dang_xuat" in log
    assert MK_THU not in log
    assert json.loads(BAN_GHI_DN)["bam"].split("$")[-1] not in log, "băm ⛔ vào nhật ký (`STG-WEB-R1-04` b)"


def test_cong_dang_nhap_SAI_401__5_lan_khoa_429_ca_khi_dung__email_khac_van_vao(cong_chay):
    p, cong, cua = cong_chay()
    jwt = ky(than_dung())
    assert _dang_nhap(cong, jwt, mk="sai-mat-khau-1")[0] == 401
    assert _dang_nhap(cong, jwt, ten="NguoiKhac")[0] == 401, "tên sai ⇒ 401 (cùng thời gian scrypt)"
    for _ in range(2):
        assert _dang_nhap(cong, jwt, mk="sai-mat-khau-2")[0] == 401
    ma, than, hd = _dang_nhap(cong, jwt, mk="sai-lan-5")
    assert ma == 429 and "Retry-After" in hd
    ma, than, _ = _dang_nhap(cong, jwt)
    assert ma == 429 and "Set-Cookie" not in _, "đang khoá ⇒ mật khẩu ĐÚNG cũng ⛔ vào"
    assert _dang_nhap(cong, ky(than_dung(email="nguoi-khac@vi-du.vn")))[0] == 303, "khoá theo email IAP"
    assert cua.thay == []
    log = _xong(p)
    assert "sai 1/5" in log and "khoa con=" in log
    assert MK_THU not in log and "sai-mat-khau" not in log and "sai-lan-5" not in log


def test_cong_CHUA_dat_tai_khoan_thi_login_503_va_KHONG_ai_vao(cong_chay):
    p, cong, cua = cong_chay(ban_ghi=None)
    jwt = ky(than_dung())
    assert _dang_nhap(cong, jwt)[0] == 503
    assert _goi(cong, "/", {C.HEADER_IAP: jwt})[0] == 303
    assert _goi(cong, "/api/fls/v1/gates", {C.HEADER_IAP: jwt})[0] == 401
    assert cua.thay == []


def test_dang_nhap_cli_bam_tu_STDIN_tu_choi_ngan_va_trung_ten():
    def chay(mk, ten=TEN_DN):
        return subprocess.run([sys.executable, "-I", str(APP / "dang_nhap.py"), "--bam", "--ten", ten], input=mk,
                              capture_output=True, text=True, timeout=60)
    r = chay(MK_THU + "\n")
    o = json.loads(r.stdout)
    assert r.returncode == 0 and o["ten"] == TEN_DN and DN.khop(MK_THU, o["bam"]) and MK_THU not in r.stdout + r.stderr
    assert chay("ngan").returncode == 2
    assert chay("HondurasGesha12", ten="HondurasGesha12").returncode == 2


@pytest.mark.parametrize("dn,tt,aud,mong", [(True, True, "/projects/1/x", ("san_sang", "san_sang", "ghim")),
                                            (False, False, "", ("chua_dat", "chua_dat", "chua_ghim")),
                                            (True, False, "", ("san_sang", "chua_dat", "chua_ghim"))])
def test_tu_do_bao_dang_nhap_trang_thai_aud_DUNG_moi_chieu(dn, tt, aud, mong):
    """`TU_DO` là mục BÁO CÁO của 07 — phải ĐO, ⛔ gắn cứng (đột biến `"san_sang"` cố định lọt bài cũ)."""
    bm = {}
    if dn:
        bm["fls-staging-login"] = BAN_GHI_DN
    if tt:
        bm["fls-staging-phien"] = _moi_trang_thai()
    sm = sm_gia(bm)
    try:
        env = dict(os.environ, K_SERVICE="x", PYTHONUTF8="1", FLS_STG_PROJECT="du-an-gia", FLS_IAP_AUD=aud,
                   FLS_STG_URL_METADATA=f"http://127.0.0.1:{sm.server_port}", FLS_STG_URL_SM=f"http://127.0.0.1:{sm.server_port}",
                   FLS_IAP_URL_JWKS="http://127.0.0.1:9/khong")
        r = subprocess.run([sys.executable, "-I", str(APP / "cong_iap.py"), "--tu-do", "--cong", str(_cong_trong()),
                            "--cong-cua", str(_cong_trong())], env=env, capture_output=True, text=True, timeout=60)
    finally:
        sm.shutdown()
    tu = dict(x.split("=", 1) for x in r.stdout.split()[1:])
    assert r.returncode == 0 and (tu["dang_nhap"], tu["trang_thai"], tu["aud"]) == mong, r.stdout + r.stderr
    assert tu["jwks"] == "0" and tu["man_hinh"] == "000", "khoá/cửa vắng ⇒ số đo ĐỎ (07 chấm), ⛔ xanh"


def test_dang_xuat_va_khoa_tam_BEN_qua_KHOI_DONG_LAI__STG_WEB_R1_02(cong_chay):
    """Instance chết (scale-về-0 / revision mới) rồi dậy: cookie đã `/logout` VẪN 401; khoá tạm VẪN 429."""
    p, cong, cua = cong_chay()
    jwt = ky(than_dung())
    ck, _ = _cookie(_dang_nhap(cong, jwt)[2])
    ck_may_khac, _ = _cookie(_dang_nhap(cong, jwt)[2])            # cùng email, "máy" thứ hai
    assert _goi(cong, "/api/fls/v1/gates", {C.HEADER_IAP: jwt, "Cookie": ck})[0] == 207
    _goi(cong, "/logout", {C.HEADER_IAP: jwt, "Cookie": ck})
    jwt2 = ky(than_dung(email="ke-doan@vi-du.vn"))
    for _ in range(DN.SAI_TOI_DA):
        _dang_nhap(cong, jwt2, mk="sai-mat-khau-x")
    _xong(p)
    p2, cong2, _ = cong_chay(sm=cua.sm, cua=cua)                     # "instance mới", CÙNG Secret Manager
    assert _goi(cong2, "/api/fls/v1/gates", {C.HEADER_IAP: jwt, "Cookie": ck})[0] == 401, "cookie đã đăng xuất hợp lệ lại"
    assert _goi(cong2, "/api/fls/v1/gates", {C.HEADER_IAP: jwt, "Cookie": ck_may_khac})[0] == 401, \
        "đăng xuất thu hồi MỌI phiên của email (thế hệ +1)"
    assert _dang_nhap(cong2, jwt2)[0] == 429, "khoá tạm mất sau khởi động lại"
    assert _dang_nhap(cong2, jwt)[0] == 303, "đăng nhập lại sau đăng xuất vẫn được"
    assert cua.sm.so_ghi >= 1 + DN.SAI_TOI_DA and cua.sm.so_huy >= 1, (cua.sm.so_ghi, cua.sm.so_huy)
    con = [v for v in cua.sm.kho["fls-staging-phien"] if v is not None]
    assert len(con) == 1, f"phiên bản cũ phải bị huỷ (còn {len(con)})"
    assert MK_THU not in "".join(con) and json.loads(BAN_GHI_DN)["bam"] not in "".join(con)


def test_ghi_trang_thai_HONG_thi_dang_xuat_van_thu_hoi_TAI_instance_va_bao_loi(cong_chay):
    p, cong, cua = cong_chay()
    jwt = ky(than_dung())
    ck, _ = _cookie(_dang_nhap(cong, jwt)[2])
    cua.sm.ghi_hong = True
    _goi(cong, "/logout", {C.HEADER_IAP: jwt, "Cookie": ck})
    assert _goi(cong, "/api/fls/v1/gates", {C.HEADER_IAP: jwt, "Cookie": ck})[0] == 401
    assert "DANG_NHAP_GHI_LOI" in _xong(p)


def test_CHUA_co_trang_thai_phien_thi_KHONG_ai_vao__DONG(cong_chay):
    p, cong, cua = cong_chay(trang_thai=False)
    jwt = ky(than_dung())
    assert _dang_nhap(cong, jwt)[0] == 503 and cua.thay == []


def test_than_KHONG_LO_khong_JWT_bi_tu_choi_NGAY_khong_doc_than__STG_WEB_R1_05(cong_chay):
    p, cong, cua = cong_chay()
    for dau_them, mong in (({}, 403), ({C.HEADER_IAP: ky(than_dung())}, 413)):
        s_ = socket.create_connection(("127.0.0.1", cong), timeout=5)
        dau = "".join(f"{k}: {v}\r\n" for k, v in dau_them.items())
        s_.sendall(f"POST /api/fls/v1/x HTTP/1.1\r\nHost: x\r\nContent-Length: 50000000\r\n{dau}\r\nabc".encode())
        t0 = time.time()
        dong = s_.recv(200).decode("latin-1").split("\r\n", 1)[0]
        s_.close()
        assert dong.split()[1] == str(mong) and time.time() - t0 < 1.0, (dong, time.time() - t0)
    s_ = socket.create_connection(("127.0.0.1", cong), timeout=5)
    s_.sendall(f"POST /x HTTP/1.1\r\nHost: x\r\n{C.HEADER_IAP}: {ky(than_dung())}\r\nTransfer-Encoding: chunked\r\n\r\n".encode())
    assert s_.recv(200).decode("latin-1").split()[1] == "411"
    s_.close()
    assert cua.thay == []


def test_aud_GHIM_thieu_aud_cung_403_va_aud_LECH_duoc_ghi_nhat_ky(cong_chay):
    p, cong, cua = cong_chay(env_them={"FLS_IAP_AUD": "/projects/1/locations/r/services/s"})
    assert _goi(cong, "/login", {C.HEADER_IAP: ky(than_dung(aud=None))})[0] == 403, "JWT IAP thiếu aud"
    assert _goi(cong, "/login", {C.HEADER_IAP: ky(than_dung(aud="/projects/1/locations/r/services/APP-KHAC"))})[0] == 403
    assert _goi(cong, "/login", {C.HEADER_IAP: ky(than_dung())})[0] == 200
    log = _xong(p)
    assert "IAP_AUD /projects/1/locations/r/services/APP-KHAC lech" in log and "IAP_AUD /projects/1/locations/r/services/s\n" in log


