"""Bản ký `fls1.<payload>.<hmac-sha256>` của cổng MCP — THUẦN stdlib (⛔ `mcp`, ⛔ kho).

Tách khỏi `xac_thuc.py` để BÁO CÁO của `tools/staging/10_mcp.sh` (Cloud Shell của CHỦ — ⛔ cài `mcp`) ký được
token THỬ bằng ĐÚNG khuôn máy chủ kiểm: đo `200 chủ · 403 người ngoài · INSERT bị chặn` mà ⛔ cần trình
duyệt. Khoá đọc từ Secret Manager bằng quyền chủ; token thử sống 5 phút, ⛔ in ra.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json

TIEN_TO_TOKEN = "fls1"


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


class Ky:
    """Bản ký `fls1.<payload>.<hmac>` — một khuôn cho access/refresh token, client_id, state."""

    def __init__(self, khoa: bytes):
        self._k = khoa

    def _mac(self, phan: str) -> str:
        return _b64(hmac.new(self._k, phan.encode(), hashlib.sha256).digest())

    def ky(self, payload: dict) -> str:
        p = _b64(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
        phan = f"{TIEN_TO_TOKEN}.{p}"
        return f"{phan}.{self._mac(phan)}"

    def mo(self, chuoi: str, loai: str) -> dict | None:
        """⛔ `None` nếu sai khuôn · sai chữ ký · sai loại. (Hạn do người gọi xét — mỗi loại một luật.)"""
        if not isinstance(chuoi, str) or chuoi.count(".") != 2 or len(chuoi) > 8192:
            return None
        tt, p, mac = chuoi.split(".")
        if tt != TIEN_TO_TOKEN or not hmac.compare_digest(mac, self._mac(f"{tt}.{p}")):
            return None
        try:
            d = json.loads(_unb64(p))
        except (ValueError, UnicodeDecodeError):
            return None
        return d if isinstance(d, dict) and d.get("typ") == loai else None

    def bi_mat_client(self, client_id: str) -> str:
        return hmac.new(self._k, b"client_secret:" + client_id.encode(), hashlib.sha256).hexdigest()
