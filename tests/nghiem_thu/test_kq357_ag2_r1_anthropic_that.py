# -*- coding: utf-8 -*-
"""KQ-357 (R1 WO-355) — bài PHÁ của fls-test cho đường gọi Anthropic THẬT. ⛔ mạng ngoài, ⛔ khoá thật.

Mỗi bài trả lời MỘT câu hỏi của phiếu; bài nào là đột biến-chứng-ĐỎ có ghi ở sổ `SO_PHAT_HIEN_ISP-3.1_AG2.md`.
SDK GIẢ lấy từ `tests/agent/test_mo_hinh_that.py` (chỉ ĐỌC, ⛔ sửa).
"""
from __future__ import annotations

import http.server
import json
import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from fls.agent import chuoi as ch
from fls.agent import mo_hinh as mh
from tests.agent.test_mo_hinh_that import DU, KHOA_GIA, YC, sdk_gia  # noqa: E402

GOC = Path(__file__).resolve().parents[2]


def _dung(monkeypatch, che_do="mo", **kw):
    sdk = sdk_gia(**{k: v for k, v in kw.items() if k in ("dap", "loi", "mo_hinh_phuc_vu", "usage")})
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    ncc = mh.AnthropicMessages(mh.OPUS_5_5, co_that=True, che_do=che_do,
                               **{k: v for k, v in kw.items() if k in ("tran_usd", "nhat_ky")})
    return ncc, sdk


# ── 3 · MỖI chốt thiếu ⇒ chặn, SDK ⛔ được nhập/dựng ──────────────────────────────────────────────────────────
CHOT = [("FLS_CHO_GOI_API", None), ("FLS_CHO_GOI_API", "0"), ("FLS_CHO_GOI_API", "true"), ("FLS_CHO_GOI_API", ""),
        ("ANTHROPIC_API_KEY", None), ("ANTHROPIC_API_KEY", ""),
        ("FLS_ZDR_DA_BAT", None), ("FLS_ZDR_DA_BAT", "0"), ("FLS_ZDR_DA_BAT", "true")]


@pytest.mark.parametrize("bien,gt", CHOT)
def test_moi_chot_thieu__CamGoiThat__SDK_khong_duoc_dung(monkeypatch, bien, gt):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    if gt is None:
        monkeypatch.delenv(bien)
    else:
        monkeypatch.setenv(bien, gt)
    sdk = sdk_gia()
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    with pytest.raises(mh.CamGoiThat) as e:
        mh.AnthropicMessages(mh.OPUS_5_5, co_that=True)
    assert bien in str(e.value) or "ANTHROPIC" in str(e.value)
    assert not hasattr(sdk, "tao_voi") and sdk.da_goi == []          # ⛔ client dựng, ⛔ lời gọi


def test_chot_co_that_vang__CamGoiThat(monkeypatch):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia())
    with pytest.raises(mh.CamGoiThat, match="--that"):
        mh.AnthropicMessages(mh.OPUS_5_5, co_that=False)


def test_zdr_khong_doi_o_che_do_che_noi_dung(monkeypatch):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("FLS_ZDR_DA_BAT")
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia())
    mh.AnthropicMessages(mh.OPUS_5_5, co_that=True, che_do="che_noi_dung")        # ⛔ ném
    with pytest.raises(mh.CamGoiThat):
        mh.AnthropicMessages(mh.OPUS_5_5, co_that=True, che_do="mo")


def test_bi_danh_va_mo_hinh_la_bi_chan(monkeypatch):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia())
    for m in (mh.MoHinh("anthropic", "claude-opus-latest", True, "ANTHROPIC_API_KEY"),      # bí danh
              mh.MoHinh("anthropic", "claude-opus-5-5", False, "ANTHROPIC_API_KEY"),        # chưa ghim
              mh.MoHinh("anthropic", "claude-haiku-5-5", True, "ANTHROPIC_API_KEY")):       # ghim nhưng ⛔ trong bảng giá
        with pytest.raises(mh.CamGoiThat):
            mh.AnthropicMessages(m, co_that=True)


def test_ma_mo_hinh_ghim_dung_va_chi_anthropic():
    assert (mh.OPUS_5_5.ma, mh.SONNET_5_5.ma) == ("claude-opus-5-5", "claude-sonnet-5-5")
    assert {a.mo_hinh.ho for a in ch.AGENT} == {"anthropic"} and set(mh.ADAPTER) == {"anthropic"}
    assert mh.HO_DE_DANH == ("openai",) and set(mh.BANG_GIA) == {"claude-opus-5-5", "claude-sonnet-5-5"}
    assert [a.mo_hinh.ma for a in ch.AGENT] == ["claude-opus-5-5"] * 3 + ["claude-sonnet-5-5"]


def test_openai_chua_cho__chot_chay_truoc_roi_ChuaDung(monkeypatch):
    o = mh.MoHinh("openai", "gpt-x", True, "OPENAI_API_KEY")
    with pytest.raises(mh.CamGoiThat):                       # thiếu chốt ⇒ CamGoiThat TRƯỚC
        mh.tao_that(o, False)
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setenv("OPENAI_API_KEY", "x")
    with pytest.raises(mh.ChuaDung):
        mh.tao_that(o, True)


# ── 3 · trần USD ─────────────────────────────────────────────────────────────────────────────────────────────
def test_tran_usd__lan_goi_thu_hai_VuotTran_co_ten_va_KHONG_goi_them(monkeypatch, du_chot=None):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    ncc, sdk = _dung(monkeypatch, usage=(1_000_000, 100_000), tran_usd=5.0)      # mỗi lời gọi ~6 USD
    ncc.goi(YC)
    with pytest.raises(mh.VuotTran, match="trần"):
        ncc.goi(YC)
    assert len(sdk.da_goi) == 1


def test_tran_usd__qua_chuoi__dung_o_co_ten_VuotTran_va_so_goi_dung_ngay(monkeypatch):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    nk: list = []
    monkeypatch.delenv("FLS_HELDOUT_NOI_DUNG", raising=False)
    ncc, sdk = _dung(monkeypatch, usage=(1_000_000, 100_000), tran_usd=1.0, nhat_ky=nk)
    import chay_agent_voi as cav
    cc = cav.dung_cong_cu()
    kc = ch.chay_chuoi({a.ma: ncc for a in ch.AGENT if ch.can_mo_hinh(a.ma)}, cc, cav.dung_may(), che_do="mo")
    assert kc.dung_o and "VuotTran" in kc.dung_o, kc.dung_o
    assert len(sdk.da_goi) == 1 + 0 or len(sdk.da_goi) == 2          # lượt 1 + (lượt 2 tool_result) rồi chặn
    assert len(nk) == len(sdk.da_goi)


def test_tran_usd_vuot_trong_MOT_lan_goi_duoc_ghi_nhan_khong_cat_giua(monkeypatch):
    """Ghi nhận hành vi: trần kiểm TRƯỚC lời gọi ⇒ một lời gọi lớn có thể vượt trần (không ngắt giữa chừng)."""
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    ncc, _ = _dung(monkeypatch, usage=(5_000_000, 500_000), tran_usd=0.5)         # 30 USD ≫ 0,5
    ncc.goi(YC)
    assert ncc.nhat_ky[0].chi_phi_usd > 0.5 * 10


# ── 2 · lỗi API ⇒ ĐỎ có tên, ⛔ rơi về GIẢ ───────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("ma", [400, 401, 403, 404, 429, 500, 529])
def test_moi_ma_HTTP__LoiApi_co_ma_va_KHONG_lot_khoa_hay_noi_dung(monkeypatch, ma):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)

    def loi(m):
        e = m.APIStatusError(ma)
        e.args = (f"khoa {KHOA_GIA} noi dung 'lam di'",)           # thông điệp gốc mang khoá + nội dung
        return e
    ncc, _ = _dung(monkeypatch, loi=loi)
    with pytest.raises(mh.LoiApi) as e:
        ncc.goi(YC)
    t = f"{e.value} {e.value.__cause__} {e.value.__context__!r}"
    assert f"HTTP {ma}" in str(e.value) and KHOA_GIA not in str(e.value) and "lam di" not in str(e.value)
    assert e.value.__cause__ is None and e.value.__suppress_context__


def test_refusal_va_max_tokens__chuoi_DUNG_co_ten_khong_GIA(monkeypatch):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    import chay_agent_voi as cav
    monkeypatch.delenv(cav.BIEN_HELDOUT, raising=False)      # `bo_ca` đòi ca.json ở gốc bể (bể A/B có a/ b/) — AG2-R1-04
    for sr in ("refusal", "max_tokens", "pause_turn"):
        ncc, sdk = _dung(monkeypatch, dap=lambda kw, sr=sr: {"stop_reason": sr, "content": [{"type": "text", "text": "{}"}]})
        kc = ch.chay_chuoi({a.ma: ncc for a in ch.AGENT if ch.can_mo_hinh(a.ma)}, cav.dung_cong_cu(), cav.dung_may(), che_do="mo")
        assert kc.dung_o and sr in kc.dung_o and len(sdk.da_goi) == 1, (sr, kc.dung_o)


# ── 4 · khoá / nội dung ⛔ lộ ra stdout · log · tệp ───────────────────────────────────────────────────────────
def test_chay_that_day_du__khoa_va_noi_dung_KHONG_o_stdout_tep(monkeypatch, capsys):
    import shutil
    tmp_path = GOC / ".kq357_tmp"
    shutil.rmtree(tmp_path, ignore_errors=True)
    tmp_path.mkdir()
    import chay_agent_voi as cav
    import vong_that_voi as vt
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv(cav.BIEN_HELDOUT, raising=False)
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia())
    monkeypatch.setattr(vt, "TM_RA", tmp_path / "vt")
    monkeypatch.setattr(vt, "TEP_MD", tmp_path / "vt" / "r.md")
    monkeypatch.setattr(vt, "TEP_JSON", tmp_path / "vt" / "r.json")
    monkeypatch.setattr(cav, "TM_NHAT_KY", tmp_path / "nk")
    goc_ghi = cav.ghi_nhat_ky
    monkeypatch.setattr(cav, "ghi_nhat_ky", lambda ncc, nhan, tm=None: goc_ghi(ncc, nhan, tmp_path / "nk"))
    rc = vt.main(["--that", "--ghi", "--tran-usd", "50"])
    out = capsys.readouterr().out
    tep = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert rc in (0, 1) and len(tep) >= 3, (rc, tep, out[-400:])
    gop = out + "\n".join(p.read_text(encoding="utf-8") for p in tep)
    assert KHOA_GIA not in gop and "sk-ant" not in gop
    # nội dung: đoạn prompt skill + chuỗi bất kỳ của ca dựng ⛔ xuất hiện ở tệp/nhật ký
    pr = ch.nap_bo("A1_RI")[0].prompt
    assert pr[:60] not in gop
    nk = json.loads(next(p for p in tep if p.parent.name == "nk").read_text(encoding="utf-8"))
    assert nk["tong"]["so_goi"] == len(nk["goi"]) > 0
    shutil.rmtree(tmp_path, ignore_errors=True)
    assert all(set(x) == {"mo_hinh", "token_vao", "token_ra", "cache_doc", "cache_ghi", "giay", "chi_phi_usd", "stop_reason",
                          "van_tay_yeu_cau", "van_tay_dap", "request_id", "ngay_tra_gia"} for x in nk["goi"])


# ── 2 · SDK THẬT (lớp client của `anthropic`) trước một máy chủ cục bộ — ⛔ mạng ngoài ─────────────────────────
def test_sdk_that_gui_dung_tham_so_toi_may_chu_cuc_bo(monkeypatch):
    got: dict = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):                                                          # noqa: N802
            got["path"], got["hdr"] = self.path, dict(self.headers)
            got["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            r = json.dumps({"id": "msg_1", "type": "message", "role": "assistant", "model": "claude-opus-5-5",
                            "content": [{"type": "text", "text": "{}"}], "stop_reason": "end_turn", "stop_sequence": None,
                            "usage": {"input_tokens": 123, "output_tokens": 45, "cache_read_input_tokens": 6,
                                      "cache_creation_input_tokens": 7}}).encode()
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("request-id", "req_cuc_bo")
            self.send_header("content-length", str(len(r)))
            self.end_headers()
            self.wfile.write(r)

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        for k, v in DU.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setenv("ANTHROPIC_BASE_URL", f"http://127.0.0.1:{srv.server_port}")
        monkeypatch.delenv("HTTPS_PROXY", raising=False)
        monkeypatch.delenv("HTTP_PROXY", raising=False)
        monkeypatch.setenv("NO_PROXY", "127.0.0.1")
        ncc = mh.AnthropicMessages(mh.OPUS_5_5, co_that=True)                      # SDK THẬT (⛔ monkeypatch sys.modules)
        out = ncc.goi(YC)
    finally:
        srv.shutdown()
    assert out["stop_reason"] == "end_turn" and got["path"].endswith("/v1/messages")
    b = got["body"]
    assert b["model"] == "claude-opus-5-5" and b["output_config"] == {"effort": "medium"} and b["max_tokens"] == 16000
    assert not {"thinking", "tool_choice", "temperature", "top_p", "top_k", "fallbacks"} & set(b)
    h = {k.lower(): v for k, v in got["hdr"].items()}
    assert KHOA_GIA in (h.get("x-api-key") or "") + (h.get("authorization") or "")      # khoá đi bằng header, ⛔ body
    assert KHOA_GIA not in json.dumps(b)
    x = ncc.nhat_ky[0]
    assert (x.token_vao, x.token_ra, x.cache_doc, x.cache_ghi, x.request_id) == (123, 45, 6, 7, "req_cuc_bo")
    assert x.chi_phi_usd == pytest.approx((123 * 4 + 45 * 20 + 6 * 0.2 + 7 * 5) / 1e6)
