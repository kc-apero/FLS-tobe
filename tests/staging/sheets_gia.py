"""Máy chủ Google Sheets GIẢ (HTTP thật, loopback) cho bài thử bước 05 — `WO-334`.

⭐ Vì sao HTTP thật mà ⛔ mock hàm: các công cụ nạp sẵn có gọi `urllib` thẳng tới `…/v4/spreadsheets/<id>/values/<vùng>` ở BỐN chỗ
khác nhau *(`nap_that._lat/_cot_rieng` · `nap_mapping_master._cot` · `do_hinh_dang._goi/doc_cot`)*. Trỏ cả bốn về MỘT máy chủ giả qua
`FLS_SHEETS_API_GOC` thì bài thử đi **đúng đường mã thật** (cắt lát, retry, `batchGet`, `majorDimension`) — ⛔ một mock hàm sẽ chỉ chứng
minh mock.

Hành vi bắt chước Sheets thật mà các công cụ DỰA VÀO: ô rỗng CUỐI hàng bị cắt · hàng rỗng CUỐI bị cắt · `COLUMNS` cắt đuôi cột ·
`403` khi workbook không chia sẻ cho SA · vùng mở `A3:V`.
"""
from __future__ import annotations

import json
import re
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_RE = re.compile(r"^'?(?P<ten>.+?)'?!(?P<c1>[A-Z]+)(?P<r1>\d+)?(?::(?P<c2>[A-Z]+)(?P<r2>\d+)?)?$")


def cot_so(chu: str) -> int:
    n = 0
    for ch in chu:
        n = n * 26 + ord(ch) - 64
    return n - 1


class SheetsGia:
    """`kho[sid][tên tab] = list[list]` (hàng 1 = chỉ số 0). `cam` = tập sid trả 403."""

    def __init__(self) -> None:
        self.kho: dict[str, dict[str, list[list]]] = {}
        self.cam: set[str] = set()
        self.so_goi = 0
        self.ghi_phat_hien = 0          # đếm yêu cầu KHÔNG phải GET — ⛔ phải = 0 (QĐ-ITL-34)
        self._srv: ThreadingHTTPServer | None = None

    # ---- đọc vùng ----
    def vung(self, sid: str, rng: str, chieu: str) -> list[list]:
        m = _RE.match(rng)
        if not m or m["ten"] not in self.kho[sid]:
            raise KeyError(rng)
        luoi = self.kho[sid][m["ten"]]
        c1, c2 = cot_so(m["c1"]), cot_so(m["c2"] or m["c1"])
        r1 = int(m["r1"] or 1)
        r2 = int(m["r2"]) if m["r2"] else len(luoi)
        hang = []
        for i in range(r1 - 1, min(r2, len(luoi))):
            h = list(luoi[i][c1:c2 + 1])
            while h and h[-1] in (None, ""):          # Sheets cắt ô rỗng cuối hàng
                h.pop()
            hang.append(h)
        while hang and not hang[-1]:                  # …và hàng rỗng cuối vùng
            hang.pop()
        if chieu == "COLUMNS":
            rong = max((len(h) for h in hang), default=0)
            cols = [[(h[j] if j < len(h) else "") for h in hang] for j in range(rong)]
            for c in cols:
                while c and c[-1] in (None, ""):
                    c.pop()
            return cols
        return hang

    # ---- máy chủ ----
    def bat(self) -> str:
        goc = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):               # im lặng
                pass

            def _tra(self, ma: int, d: dict) -> None:
                b = json.dumps(d).encode()
                self.send_response(ma)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)

            def do_GET(self):                         # noqa: N802
                goc.so_goi += 1
                u = urllib.parse.urlsplit(self.path)
                q = urllib.parse.parse_qs(u.query)
                p = urllib.parse.unquote(u.path).strip("/")
                if p.startswith("v4/spreadsheets/"):
                    p = p[len("v4/spreadsheets/"):]
                sid, _, tail = p.partition("/")
                if sid not in goc.kho:
                    return self._tra(404, {"error": {"code": 404}})
                if sid in goc.cam:
                    return self._tra(403, {"error": {"code": 403, "status": "PERMISSION_DENIED"}})
                chieu = (q.get("majorDimension") or ["ROWS"])[0]
                try:
                    if tail == "":
                        return self._tra(200, {"spreadsheetId": sid, "sheets": [
                            {"properties": {"title": t, "gridProperties": {"rowCount": len(g), "columnCount": 40}}}
                            for t, g in goc.kho[sid].items()]})
                    if tail == "values:batchGet":
                        vr = [{"range": r, "values": goc.vung(sid, r, chieu)} for r in q.get("ranges", [])]
                        return self._tra(200, {"spreadsheetId": sid, "valueRanges": vr})
                    if tail.startswith("values/"):
                        r = tail[len("values/"):]
                        return self._tra(200, {"range": r, "majorDimension": chieu, "values": goc.vung(sid, r, chieu)})
                except KeyError:
                    return self._tra(400, {"error": {"code": 400, "message": "Unable to parse range"}})
                return self._tra(404, {})

            def _khac(self):
                goc.ghi_phat_hien += 1
                self._tra(405, {})

            do_POST = do_PUT = do_PATCH = do_DELETE = _khac   # noqa: N815

        self._srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self._srv.serve_forever, daemon=True).start()
        return f"http://127.0.0.1:{self._srv.server_address[1]}/v4/spreadsheets/"

    def tat(self) -> None:
        if self._srv:
            self._srv.shutdown()
            self._srv.server_close()
