"""Chạy cổng MCP của FLS (`WO-371`). Đây là CHỖ DUY NHẤT nối `fls.mcp` với kho — y khuôn `chay_cua.py`.

    # Claude Code cục bộ (stdio) — `.mcp.json` ở gốc repo gọi đúng lệnh này
    PG_DSN=postgresql://… python tools/chay_mcp.py

    # HTTP từ xa (connector claude.ai) — Cloud Run gọi qua `tools/staging/app/vao_mcp.sh`
    PG_DSN=… FLS_MCP_URL=https://….run.app FLS_MCP_KHOA=<hex ≥ 64> FLS_MCP_GOOGLE_ID=… \\
      FLS_MCP_GOOGLE_SECRET=… FLS_MCP_CHO_PHEP=a@x.com[,b@y.com] python tools/chay_mcp.py --http --cong 8080

⛔ Máy TỪ CHỐI chạy nếu: kết nối còn GHI được (`fls.api.cua.kiem_truoc_khi_mo`) · `--http` mà thiếu một
   trong năm biến xác thực (⛔ chế độ "tạm mở" — endpoint công khai ⇒ ⛔ authless) · danh sách cho phép rỗng.
⛔ Bí mật chỉ đọc từ MÔI TRƯỜNG của tiến trình (⛔ cờ dòng lệnh — lộ trong `ps`).
"""
from __future__ import annotations

import argparse
import contextlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fls.api.cua import kiem_truoc_khi_mo                         # noqa: E402
from fls.db.kho import dsn_that, noi_chi_doc                      # noqa: E402
from fls.mcp.cong_cu import CauHinh, CongCu, ghi_nhat_ky_stderr   # noqa: E402

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEP_DO = os.path.join(GOC, "docs", "ITL", "_tools", "voi_so_luong.json")
TEP_HD2 = os.path.join(GOC, "docs", "ITL", "_tools", "hd2_cong.json")
BIEN_XAC_THUC = ("FLS_MCP_URL", "FLS_MCP_KHOA", "FLS_MCP_GOOGLE_ID", "FLS_MCP_GOOGLE_SECRET", "FLS_MCP_CHO_PHEP")
HAN_PHIEN_MS = 15_000     # statement_timeout mặc định của PHIÊN — tuyến `goi_tuyen` (truy_van_doc đặt riêng 5 s)


def mo_doc(dsn: str):
    """Hàm mở kết nối CHỈ ĐỌC (PG chặn ghi) — một kết nối MỖI lời gọi, đóng ngay sau."""
    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn)
        try:
            conn.execute(f"SET statement_timeout = {HAN_PHIEN_MS}")
            yield conn
        finally:
            conn.close()
    return mo


def danh_sach_cho_phep(chuoi: str) -> frozenset[str]:
    ds = frozenset(x.strip().lower() for x in chuoi.split(",") if x.strip())
    sai = [x for x in ds if x.count("@") != 1 or "." not in x.split("@")[1]]
    if sai:
        raise SystemExit(f"⛔ FLS_MCP_CHO_PHEP có {len(sai)} mục ⛔ phải email")
    return ds


def dung_xac_thuc(env: dict[str, str]):
    from fls.mcp.xac_thuc import CauHinhXacThuc, Google, NhaCungCapOAuth

    thieu = [b for b in BIEN_XAC_THUC if not env.get(b, "").strip()]
    if thieu:
        raise SystemExit("⛔ --http đòi đủ biến xác thực (⛔ chế độ authless): thiếu " + ", ".join(thieu))
    try:
        khoa = bytes.fromhex(env["FLS_MCP_KHOA"].strip())
    except ValueError:
        raise SystemExit("⛔ FLS_MCP_KHOA phải là hex") from None
    ds = danh_sach_cho_phep(env["FLS_MCP_CHO_PHEP"])
    if not ds:
        raise SystemExit("⛔ FLS_MCP_CHO_PHEP rỗng")
    them = tuple(x.strip() for x in env.get("FLS_MCP_REDIRECT_THEM", "").split(",") if x.strip())
    return NhaCungCapOAuth(CauHinhXacThuc(
        url_goc=env["FLS_MCP_URL"].strip(), khoa=khoa, cho_phep=lambda: ds, redirect_them=them,
        google=Google(client_id=env["FLS_MCP_GOOGLE_ID"].strip(), client_secret=env["FLS_MCP_GOOGLE_SECRET"].strip())))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--http", action="store_true", help="Streamable HTTP (mặc định: stdio)")
    ap.add_argument("--cong", type=int, default=int(os.environ.get("PORT", "8080")))
    ap.add_argument("--dia-chi", default="127.0.0.1")
    a = ap.parse_args(argv)

    dsn = dsn_that()
    mo = mo_doc(dsn)
    with mo() as conn:
        kiem_truoc_khi_mo(conn)          # ⛔ NỔ nếu kết nối còn ghi được
    cc = CongCu(mo, CauHinh(tep_do=TEP_DO, tep_hd2=TEP_HD2), ghi_nhat_ky=ghi_nhat_ky_stderr)

    from fls.mcp import may_chu
    if not a.http:
        ten = os.environ.get("FLS_MCP_NGUOI", "cuc-bo")
        may_chu.tao_may(cc, nguoi=lambda: ten).run("stdio")
        return 0

    xt = dung_xac_thuc(dict(os.environ))
    may = may_chu.tao_may(cc, nguoi=may_chu.nguoi_tu_token, xac_thuc=xt, ghi_nhat_ky=ghi_nhat_ky_stderr)
    app = may_chu.app_http(may, xt.ch.url_goc)
    import uvicorn
    sys.stderr.write(f"chay_mcp: HTTP {a.dia_chi}:{a.cong} · url={xt.ch.url_mcp} · cho_phep={len(xt.ch.cho_phep())}\n")
    uvicorn.run(app, host=a.dia_chi, port=a.cong, log_level="warning", proxy_headers=True,
                forwarded_allow_ips="*", server_header=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
