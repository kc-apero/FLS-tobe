"""AC-4 · bộ đo BÁO CÁO `tools/staging/app/do_mcp.py` chạy vào máy chủ MCP THẬT cục bộ (uvicorn + OAuth + kho TEST).

⭐ Đây là nửa "mặt ngoài" của BÁO CÁO bước 10 — nửa gcloud (GIẢ) ở `tests/staging/test_10_mcp.py`. Bài này chứng
minh mọi mục `mong` của 10 ra ĐÚNG giá trị trên một máy chủ đúng, và ra giá trị KHÁC khi máy chủ hỏng (Đ5).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from tests.mcp.test_xac_thuc_http import CHU, he  # noqa: F401 — fixture module-scope

pytestmark = pytest.mark.pg
GOC = Path(__file__).resolve().parents[2]

MONG = {"khong_token": "401", "www_resource_metadata": "co", "prm_resource_khop": "True", "prm_as_khop": "True",
        "as_issuer_khop": "True", "dang_ky_redirect_la": "400", "token_khoa_gia": "401", "token_aud_sai": "401",
        "token_het_han": "401", "nguoi_ngoai": "403", "chu_khoi_tao": "200", "chu_insert": "chan",
        "rieng_tu_email": "0/0"}


def _do_mcp():
    spec = importlib.util.spec_from_file_location("do_mcp", GOC / "tools" / "staging" / "app" / "do_mcp.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_do_mcp_ra_DUNG_mong_tren_may_chu_dung(he):  # noqa: F811
    d = _do_mcp().do(he["url"], b"k" * 32, CHU)
    for k, v in MONG.items():
        assert d[k] == v, (k, d[k])
    assert int(d["chu_so_bang"]) > 0 and int(d["chu_bang_co_dong"]) > 0 and int(d["chu_cong"]) >= 5
    so_cot, dong_tho = map(int, d["rieng_tu_mau_so"].split("/"))
    assert so_cot > 100 and dong_tho >= 2                                  # mẫu số ⛔ rỗng (Đ3)


def test_do_mcp_DO_khi_khoa_sai_hoac_chu_bi_go(he):  # noqa: F811
    """Đ5: khoá đo ≠ khoá máy chủ ⇒ `chu_khoi_tao` 401; chủ bị gỡ ⇒ 403 — BÁO CÁO sẽ ĐỎ."""
    m = _do_mcp()
    assert m.do(he["url"], b"z" * 32, CHU)["chu_khoi_tao"] == "401"
    he["cho_phep"].discard(CHU)
    try:
        d = m.do(he["url"], b"k" * 32, CHU)
        assert (d["chu_khoi_tao"], d["chu_insert"]) == ("403", "loi:403")
    finally:
        he["cho_phep"].add(CHU)


def test_do_mcp_KHONG_in_email_token(he, capsys, monkeypatch):  # noqa: F811
    monkeypatch.setenv("FLS_MCP_KHOA_DO", (b"k" * 32).hex())
    monkeypatch.setenv("FLS_MCP_DO_CHU", CHU)
    _do_mcp().main(["--url", he["url"]])
    out = capsys.readouterr().out
    assert "chu_khoi_tao=200" in out and CHU not in out and "fls1." not in out and "@" not in out
