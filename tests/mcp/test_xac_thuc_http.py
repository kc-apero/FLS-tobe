"""AC-3 · AC-6 — xác thực của cổng MCP TỪ XA, đo trên máy chủ HTTP THẬT (uvicorn, cổng ngẫu nhiên) + Google GIẢ
(RS256 thật) + client OAuth CỦA SDK (`mcp.client.auth.OAuthClientProvider` — DCR · PKCE · đổi mã), y đường của
connector claude.ai.

`mong` hai chiều: chủ ⇒ 200 + công cụ chạy · ⛔ token ⇒ 401 (kèm `resource_metadata`) · người ngoài ⇒ 403 ở bước
Google gọi về, ⛔ mã · token `aud` sai / hết hạn / ký khoá khác ⇒ 401 · token thật của người ngoài / vừa bị gỡ ⇒ 403 · redirect lạ ⇒ 400 ·
`Origin` lạ ⇒ 403 · Google nói dối (khoá lạ · aud · nonce · email chưa xác minh · hết hạn) ⇒ 401, ⛔ mã.
"""
from __future__ import annotations

import json
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

import anyio
import pytest

from fls.mcp import may_chu
from fls.mcp.cong_cu import CauHinh, CongCu
from fls.mcp.xac_thuc import CauHinhXacThuc, Google, NhaCungCapOAuth
from tests.mcp import google_gia
from tests.mcp.conftest import mo_doc_vai

pytestmark = pytest.mark.pg

CHU = "chu@vi.du"
NGOAI = "nguoi.la@vi.du"
CALLBACK = "http://localhost:39871/callback"


class _KhongTheoChuyen(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


_mo = urllib.request.build_opener(_KhongTheoChuyen)


def _http(url, *, phuong="GET", than=None, dau=None):
    req = urllib.request.Request(url, data=than, method=phuong, headers=dau or {})
    try:
        with _mo.open(req, timeout=15) as r:
            return r.status, r.headers, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode()


@pytest.fixture(scope="module")
def he(kho_mcp):
    import uvicorn
    gg = google_gia.GoogleGia()
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    cong = s.getsockname()[1]
    s.close()
    url = f"http://127.0.0.1:{cong}"
    cho_phep = {CHU}
    nk: list = []
    xt = NhaCungCapOAuth(CauHinhXacThuc(
        url_goc=url, khoa=b"k" * 32, cho_phep=lambda: frozenset(cho_phep),
        google=Google(client_id=google_gia.ID, client_secret=google_gia.BI_MAT, auth_url=gg.url + "/auth",
                      token_url=gg.url + "/token", jwks_url=gg.url + "/jwks")))
    cc = CongCu(mo_doc_vai(kho_mcp["dsn_doc"]), CauHinh(toc_do_phut=1000), ghi_nhat_ky=nk.append)
    may = may_chu.tao_may(cc, nguoi=may_chu.nguoi_tu_token, xac_thuc=xt, ghi_nhat_ky=nk.append)
    srv = uvicorn.Server(uvicorn.Config(may_chu.app_http(may, url), host="127.0.0.1", port=cong,
                                        log_level="error"))
    t = threading.Thread(target=srv.run, daemon=True)
    t.start()
    han = time.time() + 15
    while not srv.started and time.time() < han:
        time.sleep(0.05)
    assert srv.started
    yield {"url": url, "mcp": url + "/mcp", "gg": gg, "xt": xt, "cho_phep": cho_phep, "nk": nk}
    srv.should_exit = True
    t.join(10)
    gg.dong()


def _dang_nhap(he, email: str, gia_mao: str | None = None):
    """Chạy luồng OAuth bằng client SDK. Trả `(ket_qua_tool | None, lỗi | None, chuỗi chuyển hướng)`."""
    import httpx2
    from mcp.client import Client
    from mcp.client.auth import OAuthClientProvider
    from mcp.client.streamable_http import streamable_http_client
    from mcp.shared.auth import AuthorizationCodeResult, OAuthClientMetadata

    he["gg"].dat_nguoi(email, gia_mao)
    vet: dict = {"buoc": []}

    class Kho:
        tok = info = None

        async def get_tokens(self):
            return self.tok

        async def set_tokens(self, t):
            self.tok = t

        async def get_client_info(self):
            return self.info

        async def set_client_info(self, i):
            self.info = i

    async def chuyen(url: str):
        # Trình duyệt: authorize → Google → /oauth/google/callback → redirect_uri của client
        for _ in range(4):
            ma, dau, than = await anyio.to_thread.run_sync(lambda: _http(url))
            vet["buoc"].append(ma)
            if ma != 302:
                vet["cuoi"] = (ma, than)
                return
            url = dau["Location"]
            if url.startswith(CALLBACK):
                vet["ve"] = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
                return

    async def ve():
        if "ve" not in vet or "code" not in vet["ve"]:
            raise RuntimeError(f"⛔ mã: {vet}")
        return AuthorizationCodeResult(code=vet["ve"]["code"], state=vet["ve"].get("state"))

    kho = Kho()
    oauth = OAuthClientProvider(
        server_url=he["mcp"], client_metadata=OAuthClientMetadata(
            redirect_uris=[CALLBACK], client_name="bai-thu", grant_types=["authorization_code", "refresh_token"],
            response_types=["code"]), storage=kho, redirect_handler=chuyen, callback_handler=ve)

    async def chay():
        async with httpx2.AsyncClient(auth=oauth, timeout=20) as hc:
            async with Client(streamable_http_client(he["mcp"], http_client=hc), mode="legacy") as c:
                ten = [t.name for t in (await c.list_tools()).tools]
                r = await c.call_tool("liet_ke_tuyen", {})
                return ten, json.loads(r.content[0].text)
    try:
        return anyio.run(chay), None, vet, kho
    except BaseException as e:                       # noqa: BLE001 — ExceptionGroup của anyio
        return None, e, vet, kho


def test_CHU_dang_nhap_Google_roi_goi_cong_cu(he):
    kq, loi, vet, kho = _dang_nhap(he, CHU)
    assert loi is None, (loi, vet)
    ten, d = kq
    assert ten == ["liet_ke_bang", "mo_ta_bang", "truy_van_doc", "liet_ke_tuyen", "goi_tuyen", "cong"]
    assert d["so_dong"] == 31
    assert vet["buoc"] == [302, 302, 302]                       # authorize → Google → gọi về → client
    assert kho.tok.access_token.startswith("fls1.") and kho.tok.refresh_token
    nk = [x for x in he["nk"] if x["cong_cu"] in ("dang_nhap_google", "liet_ke_tuyen")][-2:]
    assert [(x["ai"], x["ket_qua"]) for x in nk] == [(CHU, "ok"), (CHU, "ok")]


def test_NGUOI_NGOAI_danh_sach_bi_403_va_KHONG_co_ma(he):
    kq, loi, vet, _ = _dang_nhap(he, NGOAI)
    assert kq is None and "ve" not in vet
    assert vet["cuoi"][0] == 403 and "danh sách" in vet["cuoi"][1]
    assert he["nk"][-1]["ket_qua"] == "ngoai_danh_sach" and he["nk"][-1]["ai"] is None   # ⛔ ghi email người lạ


@pytest.mark.parametrize("gia_mao", ["khoa_la", "aud", "nonce", "chua_xac_minh", "het_han"])
def test_GOOGLE_noi_doi_thi_401_va_KHONG_co_ma(he, gia_mao):
    kq, _, vet, _ = _dang_nhap(he, CHU, gia_mao)
    assert kq is None and "ve" not in vet and vet["cuoi"][0] == 401, vet


def _goi_mcp(he, token=None, origin=None, host=None):
    than = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}}).encode()
    dau = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if token:
        dau["Authorization"] = "Bearer " + token
    if origin:
        dau["Origin"] = origin
    if host:
        dau["Host"] = host
    return _http(he["mcp"], phuong="POST", than=than, dau=dau)


def _token(he, **doi):
    bg = int(time.time())
    p = {"typ": "at", "sub": CHU, "aud": he["mcp"], "cid": "x", "scp": ["fls.doc"], "iat": bg, "exp": bg + 600,
         "jti": "t"}
    p.update(doi)
    return he["xt"].ky.ky(p)


def test_KHONG_token_401_kem_resource_metadata(he):
    ma, dau, _ = _goi_mcp(he)
    assert ma == 401
    www = dau.get("WWW-Authenticate") or dau.get("www-authenticate")
    assert "resource_metadata" in www and "/.well-known/oauth-protected-resource/mcp" in www


def test_token_HOP_LE_200(he):
    assert _goi_mcp(he, _token(he))[0] == 200


@pytest.mark.parametrize("ten,doi", [
    ("aud_sai", {"aud": "https://may-khac.vi.du/mcp"}),
    ("het_han", {"exp": 1}),
    ("loai_sai_refresh", {"typ": "rt"}),
])
def test_token_SAI_thi_401(he, ten, doi):
    assert _goi_mcp(he, _token(he, **doi))[0] == 401, ten


def test_token_THAT_cua_NGUOI_NGOAI_thi_403(he):
    """Token đúng chữ ký + đúng `aud` + còn hạn, nhưng `sub` ⛔ trong danh sách ⇒ 403 `insufficient_scope`."""
    ma, dau, _ = _goi_mcp(he, _token(he, sub=NGOAI))
    assert ma == 403 and "insufficient_scope" in (dau.get("WWW-Authenticate") or "")


def test_token_ky_KHOA_KHAC_thi_401(he):
    from fls.mcp.xac_thuc import Ky
    bg = int(time.time())
    gia = Ky(b"z" * 32).ky({"typ": "at", "sub": CHU, "aud": he["mcp"], "cid": "x", "scp": ["fls.doc"],
                           "iat": bg, "exp": bg + 600})
    assert _goi_mcp(he, gia)[0] == 401
    assert _goi_mcp(he, "ya29.token-google-tran")[0] == 401          # ⛔ nhận token KHÁC (passthrough)


def test_GO_khoi_danh_sach_thi_token_dang_song_CHET_ngay(he):
    tok = _token(he)
    assert _goi_mcp(he, tok)[0] == 200
    he["cho_phep"].discard(CHU)
    try:
        assert _goi_mcp(he, tok)[0] == 403
    finally:
        he["cho_phep"].add(CHU)


def test_ORIGIN_la_403_HOST_la_bi_tu_choi(he):
    assert _goi_mcp(he, _token(he), origin="https://ke-xau.vi.du")[0] == 403
    assert _goi_mcp(he, _token(he), origin="https://claude.ai")[0] == 200
    assert _goi_mcp(he, _token(he), host="ke-xau.vi.du")[0] in (400, 421)


def test_DANG_KY_redirect_LA_bi_400(he):
    for ru, mong in (("https://ke-xau.vi.du/cb", 400), ("https://claude.ai/api/mcp/auth_callback", 201)):
        than = json.dumps({"redirect_uris": [ru], "client_name": "x", "grant_types": ["authorization_code"],
                           "response_types": ["code"], "token_endpoint_auth_method": "none"}).encode()
        ma, _, b = _http(he["url"] + "/register", phuong="POST", than=than, dau={"Content-Type": "application/json"})
        assert ma == mong, (ru, b)


def test_METADATA_dung_khuon_claude_ai(he):
    _, _, b = _http(he["url"] + "/.well-known/oauth-protected-resource/mcp")
    prm = json.loads(b)
    assert prm["resource"] == he["mcp"]                                  # "must equal the URL as the user enters it"
    assert [x.rstrip("/") for x in prm["authorization_servers"]] == [he["url"]]
    _, _, b = _http(he["url"] + "/.well-known/oauth-authorization-server")
    asm = json.loads(b)
    assert asm["issuer"].rstrip("/") == he["url"] and "S256" in asm["code_challenge_methods_supported"]
    assert asm["registration_endpoint"].endswith("/register")


def test_client_id_KHONG_trang_thai_song_qua_khoi_dong_lai(he):
    """Cloud Run ngủ ⇒ RAM mất. client_id + token phải còn dùng được với một NhaCungCapOAuth MỚI cùng khoá."""
    moi = NhaCungCapOAuth(he["xt"].ch)
    tok = _token(he)
    assert anyio.run(moi.load_access_token, tok).subject == CHU


def test_http_THIEU_bien_xac_thuc_thi_TU_CHOI_chay(monkeypatch):
    import tools.chay_mcp as cm
    with pytest.raises(SystemExit, match="authless"):
        cm.dung_xac_thuc({"FLS_MCP_URL": "https://x.run.app"})
    with pytest.raises(SystemExit, match="email"):
        cm.dung_xac_thuc({"FLS_MCP_URL": "https://x.run.app", "FLS_MCP_KHOA": "ab" * 32, "FLS_MCP_GOOGLE_ID": "i",
                          "FLS_MCP_GOOGLE_SECRET": "s", "FLS_MCP_CHO_PHEP": "khong-phai-email"})
    with pytest.raises(ValueError, match="32"):
        cm.dung_xac_thuc({"FLS_MCP_URL": "https://x.run.app", "FLS_MCP_KHOA": "ab" * 8, "FLS_MCP_GOOGLE_ID": "i",
                          "FLS_MCP_GOOGLE_SECRET": "s", "FLS_MCP_CHO_PHEP": "a@b.vn"})
