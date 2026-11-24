# -*- coding: utf-8 -*-
"""WO-355 AC-2 · AC-4 — adapter Anthropic THẬT, đo bằng SDK `anthropic` GIẢ (⛔ mạng, ⛔ khoá thật).

SDK giả thay `sys.modules["anthropic"]` ⇒ `AnthropicMessages.__init__` nhập nó sau khi đủ chốt — đúng đường mã thật.
Nó ghi lại MỌI tham số gửi đi, trả khuôn `Message` (có `to_dict`, `_request_id`, `usage`), và ném lỗi theo lớp SDK.
"""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest

# ⚠ chạy RIÊNG tệp này (⛔ nhờ `test_chuoi.py` nạp trước) cũng phải nhập được công cụ — bản đầu đỏ 8 bài khi chạy lẻ
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from fls.agent import chuoi as ch
from fls.agent import mo_hinh as mh

KHOA_GIA = "sk-ant-GIA-chi-de-thu-0000"       # lính canh: ⛔ được xuất hiện ở bất kỳ đầu ra nào
DU = {"FLS_CHO_GOI_API": "1", "ANTHROPIC_API_KEY": KHOA_GIA, "FLS_ZDR_DA_BAT": "1"}


class _Msg:
    def __init__(self, d: dict):
        self._d, self._request_id = d, "req_gia_01"

    def to_dict(self) -> dict:
        return json.loads(json.dumps(self._d))


def sdk_gia(dap=None, loi=None, mo_hinh_phuc_vu=None, usage=(1000, 200)):
    """Mô-đun `anthropic` giả. `dap(kw)` ⇒ dict {stop_reason, content}; mặc định = mô hình GIẢ tất định."""
    m = types.ModuleType("anthropic")

    class APIError(Exception):
        pass

    class APIStatusError(APIError):
        def __init__(self, status_code: int):
            super().__init__(f"HTTP {status_code} — noi dung yeu cau KHONG duoc lot ra")
            self.status_code, self.request_id = status_code, "req_loi_01"

    class RateLimitError(APIStatusError):
        pass

    class APIConnectionError(APIError):
        pass

    m.APIError, m.APIStatusError, m.RateLimitError, m.APIConnectionError = (
        APIError, APIStatusError, RateLimitError, APIConnectionError)
    m.da_goi = []

    class _Messages:
        def create(self, **kw):
            m.da_goi.append(kw)
            if loi is not None:
                raise loi(m)
            tl = dap(kw) if dap else mh.GiaLap().goi({**kw, "tools": kw.get("tools", [])})
            return _Msg({**tl, "model": mo_hinh_phuc_vu or kw["model"],
                         "usage": {"input_tokens": usage[0], "output_tokens": usage[1],
                                   "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}})

    class Anthropic:
        def __init__(self, **kw):
            m.tao_voi = kw
            self.messages = _Messages()

    m.Anthropic = Anthropic
    return m


@pytest.fixture
def du_chot(monkeypatch):
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("FLS_NHA_CUNG_CAP", raising=False)     # WO-359: bài này đo đường API-key (dự phòng)


def _dung(monkeypatch, mo_hinh=mh.OPUS_5_5, **kw_sdk):
    sdk = sdk_gia(**kw_sdk)
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    return mh.tao_that(mo_hinh, co_that=True), sdk


YC = {"model": "claude-opus-5-5", "max_tokens": 16000, "system": "he thong",
      "tools": [{"name": "cc", "description": "d", "input_schema": {"type": "object", "properties": {}}}],
      "messages": [{"role": "user", "content": "lam di"}]}


# ── AC-2 · tham số đúng chuẩn (skill `claude-api`, tra 23/11) ──────────────────────────────────────────────
def test_tham_so_gui__dung_chuan_opus_5_5(monkeypatch, du_chot):
    ncc, sdk = _dung(monkeypatch)
    ncc.goi(YC)
    kw = sdk.da_goi[0]
    assert kw["model"] == "claude-opus-5-5" and kw["output_config"] == {"effort": "medium"}
    assert kw["system"] == "he thong" and kw["tools"] == YC["tools"] and kw["max_tokens"] == 16000
    # ⛔ thinking (Opus 5.5: disabled/budget ⇒ 400) · ⛔ tool_choice ép (400) · ⛔ sampling (400) · ⛔ fallbacks
    assert not {"thinking", "tool_choice", "temperature", "top_p", "top_k", "fallbacks", "betas"} & set(kw)


def test_nhat_ky__token_gio_chi_phi_van_tay__KHONG_noi_dung(monkeypatch, du_chot):
    ncc, _ = _dung(monkeypatch, usage=(1_000_000, 100_000))
    ncc.goi(YC)
    assert len(ncc.nhat_ky) == 1
    x = ncc.nhat_ky[0].dict()
    assert (x["token_vao"], x["token_ra"]) == (1_000_000, 100_000)
    assert x["chi_phi_usd"] == pytest.approx(4.0 + 2.0)                       # Opus 5.5: $4 vào · $20 ra / 1M
    assert x["mo_hinh"] == "claude-opus-5-5" and x["stop_reason"] == "tool_use" and x["giay"] >= 0
    assert x["ngay_tra_gia"] == mh.NGAY_TRA_GIA == "2026-11-23" and x["request_id"] == "req_gia_01"
    assert x["van_tay_yeu_cau"] == mh.van_tay(YC) and len(x["van_tay_dap"]) == 16
    van = json.dumps(x, ensure_ascii=False)
    assert "lam di" not in van and "he thong" not in van and KHOA_GIA not in van      # ⛔ nội dung, ⛔ khoá


def test_bang_gia__sonnet_5_5_va_mo_hinh_la():
    assert mh.chi_phi("claude-sonnet-5-5", 1_000_000, 1_000_000) == pytest.approx(12.0)
    assert mh.chi_phi("claude-opus-5-5", 0, 0, cache_doc=1_000_000) == pytest.approx(0.20)
    with pytest.raises(KeyError):
        mh.chi_phi("claude-chua-co-gia", 1, 1)                                   # ⛔ đoán giá 0


def test_tong_nhat_ky_rong__so_goi_0():
    t = mh.tong_nhat_ky([])
    assert t["so_goi"] == 0 and t["chi_phi_usd"] == 0 and t["ngay_tra_gia"] == mh.NGAY_TRA_GIA


# ── AC-2 · lỗi API ⇒ ĐỎ CÓ TÊN, ⛔ rơi về GIẢ ──────────────────────────────────────────────────────────────
def test_loi_API__LoiApi_co_ten__khong_noi_dung(monkeypatch, du_chot):
    ncc, _ = _dung(monkeypatch, loi=lambda m: m.RateLimitError(429))
    with pytest.raises(mh.LoiApi) as e:
        ncc.goi(YC)
    assert "RateLimitError HTTP 429" in str(e.value) and "req_loi_01" in str(e.value)
    assert "noi dung yeu cau" not in str(e.value) and e.value.__cause__ is None      # ⛔ kéo theo thông điệp gốc


def test_loi_mang__LoiApi(monkeypatch, du_chot):
    ncc, _ = _dung(monkeypatch, loi=lambda m: m.APIConnectionError("het gio"))
    with pytest.raises(mh.LoiApi, match="mạng/hết giờ"):
        ncc.goi(YC)


def test_loi_API_trong_chuoi__DUNG_co_ten__KHONG_roi_ve_GIA(monkeypatch, du_chot):
    """Lỗi ở lời gọi đầu ⇒ skill đầu ĐỎ `LoiApi`, chuỗi DỪNG — ⛔ agent nào chạy bằng GIẢ thay."""
    import chay_agent_voi as cav
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia(loi=lambda m: m.APIStatusError(529)))
    ncc = cav.ncc_cho("that", True)
    assert {type(v) for v in ncc.values()} == {mh.AnthropicMessages}
    kc = cav.chay("that", ncc=ncc, cho_heldout=False)[0]
    assert kc.dung_o.startswith("DỪNG ở A1_RI/01_nguon_bank — LoiApi: APIStatusError HTTP 529")
    assert not kc.dat and all(k.so_luot == 0 for a in kc.agents[1:] for k in a.skills)


def test_mo_hinh_phuc_vu_khac_ghim__LoiApi(monkeypatch, du_chot):
    ncc, _ = _dung(monkeypatch, mo_hinh_phuc_vu="claude-opus-5")
    with pytest.raises(mh.LoiApi, match="≠ ghim"):
        ncc.goi(YC)
    assert len(ncc.nhat_ky) == 1                                                # lời gọi đã tốn tiền ⇒ vẫn ghi


def test_tran_usd__VuotTran(monkeypatch, du_chot):
    sdk = sdk_gia(usage=(1_000_000, 0))
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    ncc = mh.tao_that(mh.OPUS_5_5, co_that=True, tran_usd=5.0)
    ncc.goi(YC)                                                                 # 4 USD < 5
    ncc.goi(YC)                                                                 # trước gọi: 4 < 5 ⇒ được; sau: 8
    with pytest.raises(mh.VuotTran, match="trần 5.0"):
        ncc.goi(YC)
    assert len(sdk.da_goi) == 2                                                 # lời thứ ba ⛔ tới SDK


def test_nhat_ky_chung__tran_tinh_tren_ca_vong(monkeypatch, du_chot):
    import chay_agent_voi as cav
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia())
    ncc = cav.ncc_cho("that", True)
    assert len({id(n.nhat_ky) for n in ncc.values()}) == 1


# ── chuỗi chạy TRỌN qua adapter thật (SDK giả trả như mô hình GIẢ) ─────────────────────────────────────────
def test_chuoi_qua_adapter_that__A4_4_4__report_tinh_la_THAT__nhat_ky_chi_so(monkeypatch, du_chot, tmp_path):
    import chay_agent_voi as cav
    from fls.agent import ghep_noi_dung as gnd
    sdk = sdk_gia(dap=lambda kw: mh.GiaLap({"ung_vien_ghep": gnd.luat_gia_v1}).goi(kw))
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    ncc = cav.ncc_cho("that", True)
    kc, may, dap, nhan = cav.chay("that", ncc=ncc, cho_heldout=False)
    assert kc.dat and kc.dung_o is None
    _, tom = cav.sinh_report(kc, may, dap, nhan, ncc)
    assert tom["mo_hinh_that"] == 3 and tom["agent_dat"] == 4
    nk = cav.nhat_ky_cua(ncc)
    so_skill_mo_hinh = sum(1 for a in kc.agents for k in a.skills if k.skill.loai in ("lam", "bong"))
    assert len(nk) == len(sdk.da_goi) == 2 * so_skill_mo_hinh                 # mỗi skill: tool_use + end_turn
    assert {x.mo_hinh for x in nk} == {"claude-opus-5-5"}                       # A4 ⛔ lượt (MÃ tới G1)
    p = cav.ghi_nhat_ky(ncc, "thu", tm=tmp_path)
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["tong"]["so_goi"] == len(nk)
    assert set(d["goi"][0]) == {"mo_hinh", "token_vao", "token_ra", "cache_doc", "cache_ghi", "giay", "chi_phi_usd",
                                "stop_reason", "van_tay_yeu_cau", "van_tay_dap", "request_id", "ngay_tra_gia",
                                "duong", "vung"}                   # WO-359: + đường đã gọi · vùng Vertex
    assert KHOA_GIA not in p.read_text(encoding="utf-8")


def test_ghi_nhat_ky_0_goi__KHONG_ghi(tmp_path):
    import chay_agent_voi as cav
    assert cav.ghi_nhat_ky(cav.ncc_cho("gia"), "x", tm=tmp_path) is None and not list(tmp_path.iterdir())


# ── mô hình theo skill · JSON câu trả lời ──────────────────────────────────────────────────────────────────
def test_mo_hinh_skill__lam_bong_theo_agent__ma_la_None():
    from fls.agent.skill import nap_bo
    for a in ch.AGENT:
        for s in nap_bo(a.ma):
            m = ch.mo_hinh_skill(a, s)
            assert (m is None) == (s.loai == "ma") and (m is None or m.ma == "claude-opus-5-5")


@pytest.mark.parametrize("van,mong", [('{"a": 1}', {"a": 1}), ('```json\n{"a": 1}\n```', {"a": 1}),
                                      ('```\n{"a": 2}\n```', {"a": 2})])
def test_doc_json_tra_loi__chiu_mot_rao(van, mong):
    assert ch.doc_json_tra_loi(van) == mong


@pytest.mark.parametrize("van", ['Đây là kết quả: {"a": 1}', '```python\n{"a": 1}\n```', '{"a": 1}\n```x```'])
def test_doc_json_tra_loi__chu_thua__DO(van):
    with pytest.raises(json.JSONDecodeError):
        ch.doc_json_tra_loi(van)


# ── AC-3 · thiếu khoá ⇒ ĐỎ CÓ TÊN · AC-4 khoá ⛔ lộ ───────────────────────────────────────────────────────────
def test_AC3_thieu_khoa__exit_2__DO_co_ten__khong_so_THAT(monkeypatch, capsys, tmp_path):
    import vong_that_voi as vt
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("FLS_NHA_CUNG_CAP", raising=False)        # WO-359: bài này đo đường API-key
    monkeypatch.delenv(vt.cav.BIEN_HELDOUT, raising=False)
    monkeypatch.setattr(vt, "TM_RA", tmp_path)
    rc = vt.main(["--that"])
    ra = capsys.readouterr().out
    assert rc == 2 and "**KẾT: ĐỎ** — thiếu ANTHROPIC_API_KEY" in ra
    assert "| A4 ĐẠT (agent) | 4/4 | ⛔ thiếu ANTHROPIC_API_KEY |" in ra and "**0 lời gọi thật**" in ra


def test_AC4_khoa_co_nhung_thieu_chot__khoa_KHONG_in(monkeypatch, capsys):
    import vong_that_voi as vt
    monkeypatch.setenv("ANTHROPIC_API_KEY", KHOA_GIA)
    monkeypatch.delenv("FLS_CHO_GOI_API", raising=False)
    monkeypatch.delenv(vt.cav.BIEN_HELDOUT, raising=False)
    assert vt.main(["--that"]) == 2
    ra = capsys.readouterr().out
    assert KHOA_GIA not in ra and "FLS_CHO_GOI_API" in ra and "thiếu ANTHROPIC_API_KEY" not in ra


def test_AC3_mau_qua_20__tu_choi():
    import vong_that_voi as vt
    assert vt.main(["--mau", "21"]) == 2
