"""Xác thực của cổng MCP từ xa — FLS là MÁY CHỦ UỶ QUYỀN OAuth 2.1 của chính nó, đăng nhập UỶ cho Google.

⛔⛔ Endpoint công khai (Cloud Run `*.run.app`) ⇒ ⛔ authless. Chỉ email trong DANH SÁCH CHO PHÉP lấy được
token; danh sách đọc từ biến/bí mật (`FLS_MCP_CHO_PHEP`), ⛔ ghim trong repo.

⭐ VÌ SAO thiết kế này *(nguồn tra 27/11/2026 — BG-372 §"Nguồn")*:
  ⓐ connector claude.ai cần OAuth theo đặc tả MCP *(claude.com/docs/connectors/building/authentication:
     "Claude follows the 2025-03-26, 2025-06-18, and 2025-11-25 authorization specifications"; "A `401` is
     required to start sign-in"; "Claude uses only the first entry in your metadata's
     `authorization_servers` list"; "the document's `resource` field must equal the URL as the user enters
     it")* — và đặc tả đòi máy chủ MCP *"MUST validate that access tokens were issued specifically for them as
     the intended audience"*, *"MUST NOT accept or transit any other tokens"* (modelcontextprotocol.io,
     2026-07-28 · authorization · security-considerations).
  ⓑ Google ⛔ làm thẳng máy chủ uỷ quyền ấy được: metadata `accounts.google.com/.well-known/openid-
     configuration` *(đọc 27/11)* ⛔ có `registration_endpoint` *(⛔ DCR)*, và token Google ⛔ gắn được
     `aud` = URL máy chủ MCP *(⛔ tìm thấy Google nhận tham số `resource` RFC 8707)*. Dùng token Google trần =
     nhận một token ⛔ phát cho mình ⇒ trái ⓐ.
  ⓒ ⇒ FLS phát token RIÊNG: `aud` = URL MCP, ký HMAC-SHA256 bằng khoá trong Secret Manager, sống 1 giờ;
     Google chỉ dùng để BIẾT AI ĐANG BẤM (OIDC `id_token`: chữ ký RS256 theo JWKS · `iss` ·
     `aud` = client id Google của FLS · `exp` · `nonce` · `email_verified`). Đúng mẫu SDK mô tả ở
     `OAuthAuthorizationServerProvider.authorize` *("redirect to a third-party provider…")*.
  ⓓ Đăng ký client: DCR (RFC 7591) — claude.ai *"Supported by default"*. ⭐ KHÔNG TRẠNG THÁI: `client_id`
     LÀ bản ký của metadata client *(redirect_uris…)*; `client_secret` = HMAC(client_id). Cloud Run
     scale-về-0 ⇒ bộ nhớ mất mỗi lần ngủ — một client lưu trong RAM sẽ bắt chủ kết nối lại mỗi sáng.
     Chỉ MÃ UỶ QUYỀN (sống 5 phút) nằm RAM: mất ⇒ người bấm đăng nhập lại, ⛔ lộ gì.
  ⓔ `redirect_uri` ⛔ tuỳ ý: chỉ `https://claude.ai/api/mcp/auth_callback` *(claude.com docs — nguyên văn
     "register exactly this redirect URI")*, `https://claude.com/api/mcp/auth_callback` *(⚠ CHƯA kiểm — chỉ
     thấy ở bài hỗ trợ cũ nay 404; để sẵn: vẫn là miền Anthropic)* và vòng lặp `http://localhost|127.0.0.1`
     *(Claude Code nối HTTP)*. Thêm bằng `FLS_MCP_REDIRECT_THEM`.

⛔ Mỗi lời gọi kiểm LẠI email ∈ danh sách ⇒ gỡ một email là token của người ấy chết NGAY lượt sau.
⚠ Giới hạn (BG-372 §giả định): token làm mới cũ ⛔ thu hồi được khi xoay (không trạng thái) — nó sống
   `han_lam_moi`; muốn cắt hết: đổi khoá ký (bí mật `fls-staging-mcp-khoa`) ⇒ mọi token/client cũ vô hiệu.
"""
from __future__ import annotations

import hashlib
import hmac
import html
import json
import secrets
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Callable

from mcp.server.auth.provider import (AccessToken, AuthorizationCode, AuthorizationParams, AuthorizeError,
                                      RefreshToken, RegistrationError, TokenError, construct_redirect_uri)
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

from fls.mcp.ky import TIEN_TO_TOKEN, Ky, _b64  # noqa: F401 — stdlib, dùng chung với BÁO CÁO của 10_mcp.sh

PHAM_VI = "fls.doc"
REDIRECT_CLAUDE = ("https://claude.ai/api/mcp/auth_callback", "https://claude.com/api/mcp/auth_callback")
DUONG_GOOGLE_VE = "/oauth/google/callback"


@dataclass(frozen=True)
class Google:
    """Điểm cuối OIDC của Google — mặc định = giá trị đọc từ discovery 27/11; bài thử trỏ vào IdP giả."""
    client_id: str
    client_secret: str
    auth_url: str = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url: str = "https://oauth2.googleapis.com/token"
    jwks_url: str = "https://www.googleapis.com/oauth2/v3/certs"
    issuers: tuple[str, ...] = ("https://accounts.google.com", "accounts.google.com")


@dataclass
class CauHinhXacThuc:
    url_goc: str                                  # https://fls-staging-mcp-….run.app (⛔ "/" cuối)
    khoa: bytes                                   # ≥ 32 byte — ký token/client_id/state
    google: Google
    cho_phep: Callable[[], frozenset[str]]        # email chữ thường
    han_truy_cap: int = 3600
    han_lam_moi: int = 30 * 86400
    han_ma: int = 300
    han_state: int = 600
    redirect_them: tuple[str, ...] = ()
    dong_ho: Callable[[], float] = time.time
    goi_token: Callable[[str, dict], dict] | None = None   # (url, form) -> JSON; None ⇒ urllib POST

    def __post_init__(self):
        if len(self.khoa) < 32:
            raise ValueError("⛔ khoá ký < 32 byte")
        if not self.url_goc.startswith(("https://", "http://127.0.0.1", "http://localhost")):
            raise ValueError("⛔ url_goc phải https (trừ vòng lặp cho bài thử)")
        self.url_goc = self.url_goc.rstrip("/")

    @property
    def url_mcp(self) -> str:
        return self.url_goc + "/mcp"


def redirect_hop_le(uri: str, them: tuple[str, ...] = ()) -> bool:
    if uri in REDIRECT_CLAUDE or uri in them:
        return True
    p = urllib.parse.urlparse(uri)
    return p.scheme == "http" and p.hostname in ("localhost", "127.0.0.1") and not p.username


def _post_form(url: str, form: dict) -> dict:
    req = urllib.request.Request(url, data=urllib.parse.urlencode(form).encode(), method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded",
                                          "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:                       # noqa: S310 — URL cấu hình
        return json.loads(r.read().decode())


@dataclass
class _MaUyQuyen:
    ma: AuthorizationCode
    email: str


class NhaCungCapOAuth:
    """`OAuthAuthorizationServerProvider` của SDK `mcp` 2.x — xem docstring tệp."""

    def __init__(self, ch: CauHinhXacThuc):
        self.ch = ch
        self.ky = Ky(ch.khoa)
        self._ma: dict[str, _MaUyQuyen] = {}
        self._jwks = None

    def duoc_phep(self, email: str | None) -> bool:
        return bool(email) and email.lower() in self.ch.cho_phep()

    # ── client (DCR, không trạng thái) ───────────────────────────────────────────────────────
    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        uris = [str(u) for u in (client_info.redirect_uris or [])]
        sai = [u for u in uris if not redirect_hop_le(u, self.ch.redirect_them)]
        if not uris or sai:
            raise RegistrationError(error="invalid_redirect_uri",
                                    error_description="redirect_uri ⛔ trong danh sách FLS: " + ", ".join(sai))
        meta = client_info.model_dump(mode="json", exclude={"client_id", "client_secret"}, exclude_none=True)
        cid = self.ky.ky({"typ": "cid", "m": meta})
        client_info.client_id = cid
        if client_info.client_secret is not None:
            client_info.client_secret = self.ky.bi_mat_client(cid)

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        d = self.ky.mo(client_id, "cid")
        if d is None:
            return None
        m = dict(d.get("m") or {})
        bi_mat = None if m.get("token_endpoint_auth_method") == "none" else self.ky.bi_mat_client(client_id)
        return OAuthClientInformationFull.model_validate({**m, "client_id": client_id, "client_secret": bi_mat})

    # ── /authorize → Google ──────────────────────────────────────────────────────────────────
    def _verifier_google(self, nonce: str) -> str:
        return _b64(hmac.new(self.ch.khoa, b"pkce:" + nonce.encode(), hashlib.sha256).digest())

    async def authorize(self, client: OAuthClientInformationFull, params: AuthorizationParams) -> str:
        ru = str(params.redirect_uri)
        if not redirect_hop_le(ru, self.ch.redirect_them):
            raise AuthorizeError(error="invalid_request", error_description="redirect_uri ⛔ được phép")
        if params.resource and params.resource.rstrip("/") != self.ch.url_mcp:
            raise AuthorizeError(error="invalid_request", error_description="resource ⛔ phải máy chủ này")
        nonce = secrets.token_urlsafe(16)
        state = self.ky.ky({"typ": "st", "cid": client.client_id, "ru": ru,
                            "rx": params.redirect_uri_provided_explicitly, "cc": params.code_challenge,
                            "s": params.state, "scp": params.scopes or [PHAM_VI],
                            "n": nonce, "exp": int(self.ch.dong_ho()) + self.ch.han_state})
        cc_g = _b64(hashlib.sha256(self._verifier_google(nonce).encode()).digest())
        return self.ch.google.auth_url + "?" + urllib.parse.urlencode({
            "client_id": self.ch.google.client_id, "redirect_uri": self.ch.url_goc + DUONG_GOOGLE_VE,
            "response_type": "code", "scope": "openid email", "state": state, "nonce": nonce,
            "prompt": "select_account", "code_challenge": cc_g, "code_challenge_method": "S256"})

    # ── Google gọi về ─────────────────────────────────────────────────────────────────────────
    def _kiem_id_token(self, id_token: str, nonce: str) -> dict:
        import jwt                                                    # pyjwt — phụ thuộc của `mcp`
        if self._jwks is None:
            self._jwks = jwt.PyJWKClient(self.ch.google.jwks_url, cache_keys=True, lifespan=3600)
        khoa = self._jwks.get_signing_key_from_jwt(id_token).key
        d = jwt.decode(id_token, khoa, algorithms=["RS256"], audience=self.ch.google.client_id,
                       options={"require": ["exp", "iat", "iss", "aud", "sub"]}, leeway=30)
        if d.get("iss") not in self.ch.google.issuers:
            raise ValueError("iss lạ")
        if d.get("nonce") != nonce:
            raise ValueError("nonce lệch")
        if d.get("email_verified") is not True:
            raise ValueError("email chưa xác minh")
        return d

    async def google_ve(self, query: dict[str, str]) -> tuple[int, str, str | None, str]:
        """`/oauth/google/callback` ⇒ `(mã HTTP, thân HTML, Location|None, kết quả để GHI NHẬT KÝ)`.

        ⛔ Kết quả nhật ký ⛔ mang email người NGOÀI danh sách (chỉ `ngoai_danh_sach`).
        """
        import anyio

        st = self.ky.mo(query.get("state", ""), "st")
        if st is None or st.get("exp", 0) < self.ch.dong_ho():
            return 400, _trang("Phiên đăng nhập hết hạn hoặc sai — quay lại Claude và kết nối lại."), None, "state_sai"
        if query.get("error") or not query.get("code"):
            return 302, "", construct_redirect_uri(st["ru"], error="access_denied", state=st.get("s")), "google_tu_choi"
        form = {"code": query["code"], "client_id": self.ch.google.client_id,
                "client_secret": self.ch.google.client_secret, "redirect_uri": self.ch.url_goc + DUONG_GOOGLE_VE,
                "grant_type": "authorization_code", "code_verifier": self._verifier_google(st["n"])}
        goi = self.ch.goi_token or _post_form
        try:
            tl = await anyio.to_thread.run_sync(lambda: goi(self.ch.google.token_url, form))
            d = await anyio.to_thread.run_sync(lambda: self._kiem_id_token(tl.get("id_token", ""), st["n"]))
        except Exception as e:                                       # noqa: BLE001
            return 401, _trang(f"Google ⛔ xác nhận được danh tính ({type(e).__name__})."), None, \
                "id_token_sai_" + type(e).__name__
        email = str(d.get("email", "")).lower()
        if not self.duoc_phep(email):
            return 403, _trang("Tài khoản này ⛔ có trong danh sách được kết nối FLS. Nhờ chủ dự án thêm."), \
                None, "ngoai_danh_sach"
        from pydantic import AnyUrl
        ma = secrets.token_urlsafe(32)
        self._don_ma()
        self._ma[ma] = _MaUyQuyen(AuthorizationCode(
            code=ma, scopes=st["scp"], expires_at=self.ch.dong_ho() + self.ch.han_ma, client_id=st["cid"],
            code_challenge=st["cc"], redirect_uri=AnyUrl(st["ru"]), redirect_uri_provided_explicitly=st["rx"],
            resource=self.ch.url_mcp, subject=email), email)
        return 302, "", construct_redirect_uri(st["ru"], code=ma, state=st.get("s")), "ok:" + email

    def _don_ma(self) -> None:
        bg = self.ch.dong_ho()
        for k in [k for k, v in self._ma.items() if v.ma.expires_at < bg]:
            del self._ma[k]

    # ── /token ────────────────────────────────────────────────────────────────────────────────
    async def load_authorization_code(self, client: OAuthClientInformationFull, authorization_code: str):
        v = self._ma.get(authorization_code)
        if v is None or v.ma.client_id != client.client_id or v.ma.expires_at < self.ch.dong_ho():
            return None
        return v.ma

    def _phat(self, client_id: str, email: str, scopes: list[str]) -> OAuthToken:
        bg = int(self.ch.dong_ho())
        chung = {"sub": email, "aud": self.ch.url_mcp, "cid": client_id, "scp": scopes, "iat": bg}
        at = self.ky.ky({"typ": "at", **chung, "exp": bg + self.ch.han_truy_cap, "jti": secrets.token_hex(8)})
        rt = self.ky.ky({"typ": "rt", **chung, "exp": bg + self.ch.han_lam_moi, "jti": secrets.token_hex(8)})
        return OAuthToken(access_token=at, token_type="Bearer", expires_in=self.ch.han_truy_cap,
                          scope=" ".join(scopes), refresh_token=rt)

    async def exchange_authorization_code(self, client: OAuthClientInformationFull,
                                          authorization_code: AuthorizationCode) -> OAuthToken:
        v = self._ma.pop(authorization_code.code, None)       # dùng MỘT lần
        if v is None or not self.duoc_phep(v.email):
            raise TokenError(error="invalid_grant", error_description="mã ⛔ còn hiệu lực")
        return self._phat(client.client_id, v.email, list(authorization_code.scopes))

    async def load_refresh_token(self, client: OAuthClientInformationFull, refresh_token: str):
        d = self.ky.mo(refresh_token, "rt")
        if (d is None or d.get("cid") != client.client_id or d.get("exp", 0) < self.ch.dong_ho()
                or d.get("aud") != self.ch.url_mcp or not self.duoc_phep(d.get("sub"))):
            return None
        return RefreshToken(token=refresh_token, client_id=client.client_id, scopes=d.get("scp") or [PHAM_VI],
                            expires_at=d["exp"], resource=d["aud"], subject=d["sub"])

    async def exchange_refresh_token(self, client: OAuthClientInformationFull, refresh_token: RefreshToken,
                                     scopes: list[str]) -> OAuthToken:
        if not self.duoc_phep(refresh_token.subject):
            raise TokenError(error="invalid_grant", error_description="tài khoản ⛔ còn được phép")
        return self._phat(client.client_id, refresh_token.subject or "", scopes or list(refresh_token.scopes))

    # ── mỗi yêu cầu MCP ───────────────────────────────────────────────────────────────────────
    async def load_access_token(self, token: str) -> AccessToken | None:
        d = self.ky.mo(token, "at")
        if d is None or d.get("exp", 0) < self.ch.dong_ho() or d.get("aud") != self.ch.url_mcp:
            return None                                       # ⇒ 401 (token ⛔ hợp lệ cho máy này)
        # ⭐ Token THẬT của FLS nhưng người ⛔ (còn) trong danh sách ⇒ trả token RỖNG phạm vi ⇒ SDK đáp 403
        #   `insufficient_scope` (đã xác thực, ⛔ được phép). `nguoi_tu_token` kiểm LẠI phạm vi — hai lớp.
        duoc = self.duoc_phep(d.get("sub"))
        return AccessToken(token=token, client_id=d["cid"], scopes=(d.get("scp") or []) if duoc else [],
                           expires_at=d["exp"], resource=d["aud"], subject=d["sub"], claims={"email": d["sub"]})

    async def revoke_token(self, token) -> None:      # thu hồi TẮT (không trạng thái) — xem docstring tệp
        return None

    async def exchange_identity_assertion(self, client, params) -> OAuthToken:
        raise TokenError(error="unsupported_grant_type", error_description="⛔ hỗ trợ")


def _trang(loi: str) -> str:
    return ("<!doctype html><meta charset=utf-8><title>FLS MCP</title>"
            f"<body style='font-family:sans-serif;margin:3em'><h2>FLS</h2><p>{html.escape(loi)}</p></body>")
