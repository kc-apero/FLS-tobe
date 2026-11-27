"""Ráp máy chủ MCP (SDK `mcp` 2.x · `MCPServer`) — MỘT mã cho stdio lẫn Streamable HTTP.

⭐ Nguồn (tra 27/11/2026, BG-372 §"Nguồn"):
  · SDK `mcp` **2.3.0** (PyPI, phát hành 2026-10-02) — `FastMCP` đổi tên thành `MCPServer`
    (`mcp/server/fastmcp.py` của chính gói: *"FastMCP was renamed to MCPServer"*).
  · Đặc tả MCP **2026-07-28** (bản mới nhất ở modelcontextprotocol.io) — SDK vẫn bắt tay các bản cũ
    (`mcp_types.version.HANDSHAKE_PROTOCOL_VERSIONS` = 2024-11-05 … 2025-11-25) ⇒ claude.ai *(theo tài liệu
    của nó: 2025-03-26 · 2025-06-18 · 2025-11-25)* nối được.
  · Streamable HTTP: *"Servers MUST validate the `Origin` header … If the `Origin` header is present and
    invalid, servers MUST respond with HTTP 403"* ⇒ `TransportSecuritySettings` khai TƯỜNG MINH host của URL
    Cloud Run (SDK chỉ tự bật cho host vòng lặp).

⭐ `stateless_http=True` + `json_response=True`: Cloud Run scale-về-0 + `max-instances=1` — phiên giao thức
   nằm RAM sẽ mất mỗi lần ngủ; không trạng thái thì mỗi POST tự đủ.

⛔ Ở stdio (Claude Code cục bộ, `.mcp.json`): ⛔ OAuth — người gọi là chính người đang ngồi trước máy, kết
   nối là `noi_chi_doc` của `PG_DSN` cục bộ. Danh tính ghi nhật ký = `FLS_MCP_NGUOI` (mặc định `cuc-bo`).
"""
from __future__ import annotations

import json
import urllib.parse
from typing import Any, Callable

from fls.mcp.cong_cu import CongCu, LoiCongCu

TEN = "fls"
HUONG_DAN = (
    "FLS — sổ cái ITL (kế toán) của Apero. CHỈ ĐỌC. Bắt đầu bằng `liet_ke_bang` (bảng + số dòng) và "
    "`liet_ke_tuyen` (các tuyến đọc của cửa API — đã gói sẵn luật nghiệp vụ, ưu tiên dùng `goi_tuyen` "
    "trước khi tự viết SQL). `truy_van_doc` nhận MỘT câu SELECT/WITH; tiền là CHUỖI thập phân (⛔ float). "
    "Dữ liệu là dữ liệu THẬT (tên người, tiền)."
)


def tao_may(cong_cu: CongCu, *, nguoi: Callable[[], str], xac_thuc: Any = None,
            url_goc: str | None = None, ghi_nhat_ky: Callable[[dict], None] | None = None):
    """Dựng `MCPServer`. `xac_thuc` = `NhaCungCapOAuth` (HTTP từ xa) hoặc `None` (stdio cục bộ)."""
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError
    from mcp_types import ToolAnnotations
    import anyio

    kw: dict[str, Any] = {}
    if xac_thuc is not None:
        from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
        from fls.mcp.xac_thuc import PHAM_VI
        ch = xac_thuc.ch
        kw = dict(auth_server_provider=xac_thuc, auth=AuthSettings(
            issuer_url=ch.url_goc, resource_server_url=ch.url_mcp, required_scopes=[PHAM_VI],
            client_registration_options=ClientRegistrationOptions(
                enabled=True, valid_scopes=[PHAM_VI], default_scopes=[PHAM_VI]),
            revocation_options=RevocationOptions(enabled=False),
            # ⭐ `aud` do `load_access_token` TỰ kiểm (so ĐÚNG chuỗi `url_mcp`) — bài `test_xac_thuc`.
            validate_token_resource=False))
    may = MCPServer(TEN, instructions=HUONG_DAN, version="wo-371", **kw)
    doc = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

    async def _goi(ham, *a, **k) -> dict:
        try:
            ai = nguoi()                              # đọc danh tính TRƯỚC khi sang luồng (contextvar)
            return await anyio.to_thread.run_sync(lambda: ham(ai, *a, **k))
        except LoiCongCu as e:
            raise ToolError(str(e)) from None

    @may.tool(annotations=doc, description="Liệt kê mọi bảng/view schema public + số dòng đếm thật.")
    async def liet_ke_bang() -> dict:
        return await _goi(cong_cu.liet_ke_bang)

    @may.tool(annotations=doc, description="Mô tả một bảng/view: cột · kiểu · NULL được · chú thích.")
    async def mo_ta_bang(ten: str) -> dict:
        return await _goi(cong_cu.mo_ta_bang, ten)

    @may.tool(annotations=doc, description=(
        "Chạy MỘT câu SELECT hoặc WITH…SELECT (chỉ đọc; ⛔ DML/DDL/COPY/SET/nhiều câu/hàm có tác dụng phụ). "
        "gioi_han = số dòng tối đa (mặc định 200, trần 1000). Hết hạn 5 giây/câu."))
    async def truy_van_doc(sql: str, gioi_han: int | None = None) -> dict:
        return await _goi(cong_cu.truy_van_doc, sql, gioi_han)

    @may.tool(annotations=doc, description="Liệt kê các tuyến ĐỌC của cửa API FLS (tên · đường · tham số · mô tả).")
    async def liet_ke_tuyen() -> dict:
        return await _goi(cong_cu.liet_ke_tuyen)

    @may.tool(annotations=doc, description=(
        "Gọi một tuyến ĐỌC của cửa API FLS bằng tên (xem liet_ke_tuyen). tham_so: tham số đường "
        "(vd itl_id) + tham số truy vấn (vd period, run_id) — y như ?k=v của cửa HTTP."))
    async def goi_tuyen(ten: str, tham_so: dict[str, str] | None = None) -> dict:
        return await _goi(cong_cu.goi_tuyen, ten, tham_so or {})

    @may.tool(annotations=doc, description="Cổng HD1/HD2 + cổng kế toán (= tuyến GET /gates).")
    async def cong() -> dict:
        return await _goi(cong_cu.cong)

    if xac_thuc is not None:
        from starlette.requests import Request
        from starlette.responses import HTMLResponse, RedirectResponse
        from fls.mcp.xac_thuc import DUONG_GOOGLE_VE

        log = ghi_nhat_ky or (lambda _b: None)

        @may.custom_route(DUONG_GOOGLE_VE, methods=["GET"])
        async def google_ve(request: Request):
            ma, than, toi, ket = await xac_thuc.google_ve(dict(request.query_params))
            ai = ket[3:] if ket.startswith("ok:") else None
            log({"ai": ai, "cong_cu": "dang_nhap_google", "sql_bam": None, "so_dong": None, "ms": None,
                 "ket_qua": "ok" if ai else ket})
            if toi is not None:
                return RedirectResponse(toi, status_code=302)
            return HTMLResponse(than, status_code=ma)
    return may


def app_http(may, url_goc: str):
    """App Starlette Streamable HTTP ở `/mcp` — Host/Origin khoá vào URL công khai."""
    from mcp.server.transport_security import TransportSecuritySettings

    host = urllib.parse.urlparse(url_goc).netloc
    an_ninh = TransportSecuritySettings(
        enable_dns_rebinding_protection=True, allowed_hosts=[host],
        allowed_origins=[url_goc.rstrip("/"), "https://claude.ai", "https://claude.com"])
    return may.streamable_http_app(stateless_http=True, json_response=True, transport_security=an_ninh,
                                   host=urllib.parse.urlparse(url_goc).hostname or "127.0.0.1")


def nguoi_tu_token() -> str:
    """Danh tính của lời gọi HTTP — `sub` của token FLS (đã qua `load_access_token`)."""
    from mcp.server.auth.middleware.auth_context import get_access_token
    from fls.mcp.xac_thuc import PHAM_VI
    t = get_access_token()
    if t is None or not t.subject:
        raise LoiCongCu("CHUA_XAC_THUC", "⛔ token")
    if PHAM_VI not in (t.scopes or []):            # lớp hai sau `required_scopes` của SDK (người ngoài ⇒ phạm vi rỗng)
        raise LoiCongCu("KHONG_DUOC_PHEP", "tài khoản ⛔ trong danh sách cho phép")
    return t.subject


def json_gon(d: Any) -> str:
    return json.dumps(d, ensure_ascii=False)
