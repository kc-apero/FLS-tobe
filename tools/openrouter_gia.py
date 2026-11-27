# -*- coding: utf-8 -*-
"""Máy chủ OpenRouter GIẢ trên `127.0.0.1` — `WO-367` (bài thử AC-1/2/4 + lượt chạy GIẢ trọn ma trận fleet eval).

⭐ Nói HTTP THẬT (adapter `mo_hinh.OpenRouterChat` gọi bằng `requests` như với `openrouter.ai`) nhưng ⛔ ra mạng ngoài:
   `POST /api/v1/chat/completions` trả đáp theo khuôn OpenRouter (tra tài liệu 2026-11-27: `choices[0].message.{content,
   tool_calls, reasoning_details}` · `finish_reason` chuẩn hoá · `usage.{prompt_tokens, completion_tokens,
   prompt_tokens_details.cached_tokens, cost}` · `model` · `provider` · `id`).
⭐ Hành vi tất định như `mo_hinh.GiaLap`: lượt chưa có kết quả công cụ ⇒ gọi công cụ ĐẦU; lượt có tin `role: tool` ⇒ trả
   `luat(kết quả công cụ)` nếu công cụ có luật (`ung_vien_ghep` ⇒ `ghep_noi_dung.luat_gia_v1`, đổi theo slug được), không thì
   chép nguyên. `usage.cost` = giá danh mục × token (giả lập số OpenRouter TÍNH TIỀN); tắt được (`khong_cost`) để thử nhãn ƯỚC.
⭐ Sổ `TrangThai.yeu_cau` giữ MỌI thân + header đã nhận ⇒ bài đếm lời gọi (0 khi thiếu chốt), soi `provider`, soi khoá.
   ⛔ in khoá: sổ chỉ ghi `co_khoa` + vân tay 8 hex của header `Authorization`.
"""
from __future__ import annotations

import hashlib
import json
import sys
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Iterator

GOC = Path(__file__).resolve().parents[1]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.agent import ghep_noi_dung as gnd  # noqa: E402
from fls.agent import mo_hinh as mh  # noqa: E402


@dataclass
class TrangThai:
    """Hành vi + sổ của máy chủ giả. Mọi trường đổi được GIỮA lượt (bài thử)."""
    luat: dict[str, Callable[[Any], Any]] = field(default_factory=lambda: {"ung_vien_ghep": gnd.luat_gia_v1})
    luat_theo_slug: dict[str, dict[str, Callable[[Any], Any]]] = field(default_factory=dict)
    loi_lan_toi: list[tuple[int, dict]] = field(default_factory=list)   # (mã HTTP, thân) trả cho các lời KẾ, lần lượt
    loi_200: dict | None = None             # thân `error` trong đáp 200 (lỗi GIỮA lúc sinh)
    khong_cost: bool = False                # bỏ `usage.cost` ⇒ adapter phải ƯỚC
    mo_hinh_tra: str | None = None          # ép `model` trả về (thử ⛔ khớp ghim)
    reasoning: bool = True                  # kèm `reasoning_details` (adapter phải gửi lại NGUYÊN)
    arguments_hong: bool = False            # `tool_calls[].function.arguments` ⛔ phải JSON
    yeu_cau: list[dict] = field(default_factory=list)


def _dap(tt: TrangThai, than: dict) -> dict:
    slug = than.get("model", "")
    msgs = than.get("messages") or []
    tools = than.get("tools") or []
    so_tro_ly = sum(1 for m in msgs if m.get("role") == "assistant")
    tin: dict[str, Any] = {"role": "assistant", "content": None}
    cuoi = msgs[-1] if msgs else {}
    if cuoi.get("role") == "tool":
        ten = (tools[0].get("function") or {}).get("name") if tools else None
        luat = tt.luat_theo_slug.get(slug, tt.luat)
        van = cuoi.get("content") or ""
        if ten in luat:
            van = json.dumps(luat[ten](json.loads(van)), ensure_ascii=False, sort_keys=True)
        tin["content"], fin = van, "stop"
    elif tools:
        ten = tools[0]["function"]["name"]
        tin["tool_calls"] = [{"id": f"call_gia_{so_tro_ly:02d}", "type": "function",
                              "function": {"name": ten, "arguments": "{khong-json" if tt.arguments_hong else "{}"}}]
        fin = "tool_calls"
    else:
        tin["content"], fin = "{}", "stop"
    if tt.reasoning:
        tin["reasoning_details"] = [{"type": "reasoning.encrypted", "data": f"ma-hoa-gia-{so_tro_ly}",
                                     "format": "anthropic-claude-v1", "index": 0}]
    vao = len(json.dumps(than, ensure_ascii=False)) // 4
    ra = len(tin.get("content") or "") // 4 + 8
    usage: dict[str, Any] = {"prompt_tokens": vao, "completion_tokens": ra, "total_tokens": vao + ra,
                             "prompt_tokens_details": {"cached_tokens": 0}}
    if not tt.khong_cost:
        g = mh.bang_gia_openrouter().get(slug, {"vao": 1.0, "ra": 1.0})
        usage["cost"] = round((vao * g["vao"] + ra * g["ra"]) / 1e6, 8)
    d = {"id": f"gen-gia-{len(tt.yeu_cau):04d}", "object": "chat.completion", "model": tt.mo_hinh_tra or slug,
         "provider": "Amazon Bedrock", "choices": [{"index": 0, "finish_reason": fin, "native_finish_reason": fin,
                                                    "message": tin}], "usage": usage}
    if tt.loi_200:
        d["choices"][0]["error"] = tt.loi_200
    return d


def _lop_xu_ly(tt: TrangThai) -> type[BaseHTTPRequestHandler]:
    class XuLy(BaseHTTPRequestHandler):
        def log_message(self, *a: Any) -> None:     # ⛔ in ra stderr của pytest
            return

        def _gui(self, ma: int, d: dict, them: dict[str, str] | None = None) -> None:
            b = json.dumps(d, ensure_ascii=False).encode("utf-8")
            self.send_response(ma)
            self.send_header("Content-Type", "application/json")
            for k, v in (them or {}).items():
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_POST(self) -> None:                   # noqa: N802
            n = int(self.headers.get("Content-Length") or 0)
            than = json.loads(self.rfile.read(n) or b"{}")
            au = self.headers.get("Authorization") or ""
            tt.yeu_cau.append({"duong_dan": self.path, "than": than, "co_khoa": au.startswith("Bearer ") and len(au) > 7,
                               "van_tay_khoa": hashlib.sha256(au.encode()).hexdigest()[:8]})
            if self.path.rstrip("/") != "/api/v1/chat/completions":
                return self._gui(404, {"error": {"code": 404, "message": "không có"}})
            if not (au.startswith("Bearer ") and len(au) > 7):
                return self._gui(401, {"error": {"code": 401, "message": "No API key in the Authorization header"}})
            if tt.loi_lan_toi:
                ma, d = tt.loi_lan_toi.pop(0)
                return self._gui(ma, d, {"Retry-After": "0"} if ma in (429, 503) else None)
            return self._gui(200, _dap(tt, than))
    return XuLy


@contextmanager
def may_chu_gia(tt: TrangThai | None = None) -> Iterator[tuple[str, TrangThai]]:
    """`with may_chu_gia() as (goc_api, tt):` — `goc_api` = `http://127.0.0.1:<cổng>/api/v1` (truyền vào `goc_api=`)."""
    tt = tt or TrangThai()
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _lop_xu_ly(tt))
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}/api/v1", tt
    finally:
        srv.shutdown()
        srv.server_close()
