# -*- coding: utf-8 -*-
"""`WO-367` AC-1/AC-2/AC-3 — đường `openrouter` (chủ 27/11 *"Chuyển việc dùng Vertex sang dùng OpenRouter"*).

Đo bằng máy chủ OpenRouter GIẢ trên `127.0.0.1` (`tools/openrouter_gia.py`) — adapter gọi HTTP THẬT bằng `requests`, ⛔ mạng
ngoài. Mỗi bài khai `mong` (Đ5); bài đếm "0 lời gọi" đo trên MÁY CHỦ (sổ `tt.yeu_cau`), ⛔ trên adapter.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "tools"))

from fls.agent import chuoi as ch  # noqa: E402
from fls.agent import mo_hinh as mh  # noqa: E402

import openrouter_gia as og  # noqa: E402

#: Khoá GIẢ — chỉ sống trong `tests/` (bài grep tiền tố khoá OpenRouter ngoài `tests/` = 0).
KHOA = "sk-or-v1-GIA-0000000000000000000000000000000000000000000000000000000000000000"
DU = {"FLS_CHO_GOI_API": "1", "FLS_NHA_CUNG_CAP": "openrouter", "OPENROUTER_API_KEY": KHOA,
      "FLS_OPENROUTER_DU_LIEU_XAC_NHAN": "1"}
YC = {"model": "claude-opus-5-5", "max_tokens": 64, "system": "hệ thống",
      "tools": [{"name": "doc_so", "description": "d", "input_schema": {"type": "object", "properties": {}}}],
      "messages": [{"role": "user", "content": "làm đi"}]}


@pytest.fixture
def may():
    with og.may_chu_gia() as (goc, tt):
        yield goc, tt


def _dung(goc, mo_hinh=mh.OPUS_5_5, mt=None, **kw):
    return mh.tao_that(mo_hinh, True, moi_truong=dict(DU if mt is None else mt), goc_api=goc, ngu=lambda s: None, **kw)


# ── AC-1 · đường + dịch hợp đồng ───────────────────────────────────────────────────────────────────────────────────
def test_AC1_duong_openrouter_hop_le__bien_vang_GIU_anthropic():
    assert mh.DUONG_OPENROUTER == "openrouter" and mh.DUONG_OPENROUTER in mh.DUONG_HOP_LE
    assert mh.duong_goi({}) == mh.DUONG_MAC_DINH == "anthropic"          # KQ-357 khoá hành vi biến vắng
    assert mh.duong_goi({"FLS_NHA_CUNG_CAP": "OpenRouter "}) == "openrouter"


def test_AC1_tao_that__anthropic_va_openai_qua_openrouter(may):
    goc, _ = may
    a = _dung(goc)
    assert isinstance(a, mh.OpenRouterChat) and a.slug == "anthropic/claude-opus-5.5" and a.ten == "openrouter"
    assert _dung(goc, mh.SONNET_5_5).slug == "anthropic/claude-sonnet-5.5"
    o = _dung(goc, mh.mo_hinh_openrouter("openai/gpt-6.2-sol"))
    assert isinstance(o, mh.OpenRouterChat) and o.slug == "openai/gpt-6.2-sol"
    # ⛔ đường openrouter ⇒ họ openai VẪN chừa chỗ (KQ-357 khoá `HO_DE_DANH == ("openai",)` + ChuaDung)
    assert mh.HO_DE_DANH == ("openai",) and set(mh.ADAPTER) == {"anthropic"}
    with pytest.raises(mh.ChuaDung, match="CHỪA CHỖ"):
        mh.tao_that(mh.MoHinh("openai", "gpt-x", True, "OPENAI_API_KEY"), True,
                    moi_truong={"FLS_CHO_GOI_API": "1", "OPENAI_API_KEY": "x", "FLS_ZDR_DA_BAT": "1"})


def test_AC1_vong_tool_use_tron__dich_dung_hai_chieu_va_gui_lai_reasoning(may):
    goc, tt = may
    a = _dung(goc)
    tl1 = a.goi(YC)
    assert tl1["stop_reason"] == "tool_use"
    kieu = [k["type"] for k in tl1["content"]]
    assert kieu == ["openrouter_reasoning", "tool_use"] and tl1["content"][1]["name"] == "doc_so"
    than1 = tt.yeu_cau[-1]["than"]
    assert than1["model"] == "anthropic/claude-opus-5.5" and than1["messages"][0] == {"role": "system", "content": "hệ thống"}
    assert than1["tools"][0]["type"] == "function" and than1["tools"][0]["function"]["parameters"]["type"] == "object"
    assert than1["reasoning"] == {"effort": "medium"} and "tool_choice" not in than1 and "models" not in than1
    yc2 = dict(YC, messages=YC["messages"] + [
        {"role": "assistant", "content": tl1["content"]},
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tl1["content"][1]["id"],
                                      "content": json.dumps({"a": 1})}]}])
    tl2 = a.goi(yc2)
    assert tl2["stop_reason"] == "end_turn" and json.loads(tl2["content"][-1]["text"]) == {"a": 1}
    m2 = tt.yeu_cau[-1]["than"]["messages"]
    assert [m["role"] for m in m2] == ["system", "user", "assistant", "tool"]
    assert m2[2]["tool_calls"][0]["function"] == {"name": "doc_so", "arguments": "{}"}
    assert m2[2]["reasoning_details"] == tl1["content"][0]["reasoning_details"]       # gửi lại NGUYÊN VẸN
    assert m2[3] == {"role": "tool", "tool_call_id": "call_gia_00", "content": '{"a": 1}'}
    assert len(a.nhat_ky) == 2 and {x.duong for x in a.nhat_ky} == {"openrouter"}
    assert {x.nha_cung_cap for x in a.nhat_ky} == {"Amazon Bedrock"}


def test_AC1_chuoi_4_agent_qua_openrouter__A4_dat(may):
    """Đường ống THẬT (cổng skill · bộ che `mo` · A4) qua adapter OpenRouter + máy chủ giả ⇒ 4/4 ĐẠT như GIẢ."""
    import chay_agent_voi as cav
    goc, tt = may
    nk: list = []
    ncc = {dn.ma: _dung(goc, dn.mo_hinh, nhat_ky=nk, tran_usd=5.0) for dn in ch.AGENT if ch.can_mo_hinh(dn.ma)}
    kc, may_do, dap, nhan = cav.chay("gia", "mo", ncc=ncc)
    _, tom = cav.sinh_report(kc, may_do, dap, nhan, ncc)
    assert kc.dung_o is None and tom["agent_dat"] == tom["agent"] == 4, kc.dung_o
    assert len(nk) == len(tt.yeu_cau) > 0 and tom["mo_hinh_that"] == len(ncc)    # report nhận đường openrouter là THẬT


@pytest.mark.parametrize("ma,ten", [(402, "HẾT CREDIT"), (429, "GIỚI HẠN TỐC ĐỘ"), (401, "khoá OpenRouter sai"),
                                    (403, "bị CHẶN"), (503, "ZDR"), (502, "đang hỏng"), (400, "yêu cầu sai")])
def test_AC1_loi_HTTP__LoiApi_CO_TEN_khong_noi_dung_khong_khoa(may, ma, ten):
    goc, tt = may
    a = _dung(goc, max_retries=0)
    tt.loi_lan_toi = [(ma, {"error": {"code": ma, "message": "NOIDUNG-BI-MAT số TK 123456789",
                                      "metadata": {"limit_source": "key_limit"}}})]
    with pytest.raises(mh.LoiApi) as e:
        a.goi(YC)
    s = str(e.value)
    assert f"HTTP {ma}" in s and ten in s and "NOIDUNG-BI-MAT" not in s and KHOA not in s and "123456789" not in s
    assert a.nhat_ky == []                      # ⛔ tính tiền khi OpenRouter từ chối


def test_AC1_429_thu_lai_roi_DAT__402_KHONG_thu_lai(may):
    goc, tt = may
    a = _dung(goc, max_retries=2)
    tt.loi_lan_toi = [(429, {"error": {"code": 429}}), (503, {"error": {"code": 503}})]
    assert a.goi(YC)["stop_reason"] == "tool_use" and len(tt.yeu_cau) == 3
    tt.loi_lan_toi = [(402, {"error": {"code": 402}}), (402, {"error": {"code": 402}})]
    with pytest.raises(mh.LoiApi, match="HẾT CREDIT"):
        a.goi(YC)
    assert len(tt.yeu_cau) == 4                 # 402 ⛔ thử lại (tài liệu: "not a wait-and-retry case")


def test_AC1_loi_giua_luc_sinh__mo_hinh_khac_ghim__arguments_hong__LoiApi_va_VAN_ghi_nhat_ky(may):
    goc, tt = may
    a = _dung(goc)
    tt.loi_200 = {"code": 502, "message": "NOIDUNG"}
    with pytest.raises(mh.LoiApi, match="GIỮA lúc sinh"):
        a.goi(YC)
    tt.loi_200, tt.mo_hinh_tra = None, "anthropic/claude-opus-4.8"
    with pytest.raises(mh.LoiApi, match="≠ ghim"):
        a.goi(YC)
    tt.mo_hinh_tra = "anthropic/claude-opus-5.5-20260921"     # canonical slug ⇒ nhận
    assert a.goi(YC)["stop_reason"] == "tool_use"
    tt.mo_hinh_tra, tt.arguments_hong = None, True
    with pytest.raises(mh.LoiApi, match="arguments"):
        a.goi(YC)
    assert len(a.nhat_ky) == 4                  # tiền đã tiêu ⇒ có dấu vết, kể cả lượt ĐỎ


def test_AC1_khoa_KHONG_o_thuoc_tinh_repr_nhat_ky_va_toi_may_chu_dung_header(may):
    goc, tt = may
    a = _dung(goc)
    a.goi(YC)
    assert tt.yeu_cau[-1]["co_khoa"] is True
    assert KHOA not in repr(a) and KHOA not in json.dumps([x.dict() for x in a.nhat_ky])
    assert all(KHOA not in repr(v) for k, v in vars(a).items() if k != "_mt")
    assert KHOA not in json.dumps(tt.yeu_cau[-1]["than"])    # ⛔ trong thân


def test_AC1_grep_khoa_openrouter_ngoai_tests_bang_0():
    """Mẫu HÌNH KHOÁ (tiền tố + ≥ 16 ký tự), ⛔ chuỗi tiền tố trần: WO-367 và BG nhắc TIỀN TỐ như biên bản (Đ2) — đếm
    chữ trần cắn cả câu ấy (đo 27/11: 1 tệp, `WO-367`). Bằng chứng DƯƠNG: cùng mẫu phải thấy khoá GIẢ trong `tests/`."""
    mau = "sk-" + "or-" + "[A-Za-z0-9_-]{16,}"           # ghép để chính bài này ⛔ tự khớp
    r = subprocess.run(["git", "grep", "--untracked", "-l", "-E", mau, "--", ".", ":!tests"], cwd=GOC, capture_output=True, text=True)
    assert r.returncode in (0, 1), r.stderr
    assert r.stdout.split() == [], r.stdout
    r2 = subprocess.run(["git", "grep", "--untracked", "-l", "-E", mau, "--", "tests/agent/"], cwd=GOC, capture_output=True, text=True)
    assert "tests/agent/test_mo_hinh_openrouter.py" in r2.stdout.split(), \
        "tập RỖNG (Đ3): mẫu phải thấy khoá GIẢ trong tests/ — không thì phép grep ⛔ chứng minh được gì"


# ── AC-2 · chốt dữ liệu + chi phí ─────────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("bo,ten", [("FLS_CHO_GOI_API", "FLS_CHO_GOI_API"), ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY"),
                                    ("FLS_OPENROUTER_DU_LIEU_XAC_NHAN", "FLS_OPENROUTER_DU_LIEU_XAC_NHAN")])
@pytest.mark.parametrize("che", ["mo", "che_noi_dung", "che_het"])
def test_AC2_thieu_moi_chot__CamGoiThat_co_ten__0_loi_goi(may, bo, ten, che):
    goc, tt = may
    mt = {k: v for k, v in DU.items() if k != bo}
    with pytest.raises(mh.CamGoiThat, match=ten) as e:
        mh.tao_that(mh.OPUS_5_5, True, che_do=che, moi_truong=mt, goc_api=goc)
    assert KHOA not in str(e.value) and len(tt.yeu_cau) == 0


def test_AC2_thieu_co_that__0_loi_goi(may):
    goc, tt = may
    with pytest.raises(mh.CamGoiThat, match="--that"):
        mh.tao_that(mh.OPUS_5_5, False, moi_truong=dict(DU), goc_api=goc)
    assert len(tt.yeu_cau) == 0


def test_AC2_moi_loi_goi_mang_dinh_tuyen_ZDR_va_deny(may):
    goc, tt = may
    a = _dung(goc)
    a.goi(YC)
    a.goi(YC)
    assert [y["than"]["provider"] for y in tt.yeu_cau] == [{"data_collection": "deny", "zdr": True}] * 2


def test_AC2_usd_THAT_tu_usage_cost__thieu_cost_thi_UOC_co_nhan(may):
    goc, tt = may
    a = _dung(goc)
    a.goi(YC)
    x = a.nhat_ky[-1]
    gia = mh.bang_gia_openrouter()["anthropic/claude-opus-5.5"]
    assert x.nguon_usd == "THẬT" and x.chi_phi_usd == pytest.approx((x.token_vao * gia["vao"] + x.token_ra * gia["ra"]) / 1e6)
    tt.khong_cost = True
    a.goi(YC)
    assert a.nhat_ky[-1].nguon_usd == "ƯỚC" and a.nhat_ky[-1].chi_phi_usd > 0
    t = mh.tong_nhat_ky(a.nhat_ky)
    assert t["nguon_usd"] == {"THẬT": 1, "ƯỚC": 1} and t["ngay_tra_gia"] == mh.NGAY_TRA_GIA_OPENROUTER == "2026-11-27"
    d = a.nhat_ky[-1].dict()
    assert d["duong"] == "openrouter" and d["nguon_usd"] == "ƯỚC" and d["nha_cung_cap"] == "Amazon Bedrock"


def test_AC2_duong_API_GIU_12_khoa_nhat_ky():
    x = mh.NhatKyGoi("claude-opus-5-5", 1, 1, 0, 0, 0.1, 0.0, "end_turn", "a", "b")
    assert len(x.dict()) == 12                 # bài nghiệm thu KQ-357 ghim tập khoá đường API


def test_AC2_tran_TONG_va_tran_MO_HINH__chan_loi_KE(may):
    goc, tt = may
    nk: list = []
    a = _dung(goc, nhat_ky=nk, tran_usd=1.0, tran_usd_mo_hinh=1e-9)
    a.goi(YC)
    with pytest.raises(mh.VuotTran, match="trần MÔ HÌNH"):
        a.goi(YC)
    b = _dung(goc, mh.SONNET_5_5, nhat_ky=nk, tran_usd=1.0)     # mô hình khác ⇒ trần riêng ⛔ chặn
    b.goi(dict(YC, model="claude-sonnet-5-5"))
    c = _dung(goc, mh.SONNET_5_5, nhat_ky=nk, tran_usd=1e-9)
    with pytest.raises(mh.VuotTran, match="trần TỔNG"):
        c.goi(dict(YC, model="claude-sonnet-5-5"))
    assert len(tt.yeu_cau) == 2


# ── AC-3 · ma trận mô hình ────────────────────────────────────────────────────────────────────────────────────────
def test_AC3_cau_hinh_MOT_cho__vai_mac_dinh_slug_that_da_tra():
    mt = mh.ma_tran_openrouter()
    assert mt["vai"] == {"lam": "anthropic/claude-opus-5.5", "auditor": "anthropic/claude-sonnet-5.5"}
    assert mt["ngay_tra"] == "2026-11-27" and "api/v1/models" in mt["nguon"]["mo_hinh"]
    assert mt["vai"]["lam"] != mt["vai"]["auditor"]                       # luật hai mô hình (WO-355) giữ qua OpenRouter
    for s in [*mt["vai"].values(), *mt["ung_vien"]]:
        assert mh.loi_slug_openrouter(s) is None, s
        assert mt["mo_hinh"][s]["diem_cuoi_zdr"], f"{s}: 0 điểm cuối ZDR ⇒ zdr:true sẽ 503"
    # giá danh mục ↔ bảng giá Claude API (hai nguồn độc lập — Đ2): Opus/Sonnet 5.5 khớp 8/8 ô
    for ma, slug in (("claude-opus-5-5", mt["vai"]["lam"]), ("claude-sonnet-5-5", mt["vai"]["auditor"])):
        assert mh.bang_gia_openrouter()[slug] == mh.BANG_GIA[ma]


def test_AC3_cam_google_bi_danh_bien_the_va_ngoai_danh_muc():
    mt = mh.ma_tran_openrouter()
    assert not [s for s in [*mt["mo_hinh"], *mt["vai"].values(), *mt["ung_vien"]] if s.startswith("google/")]
    for s, ly in (("google/gemini-3-pro", "CẤM"), ("~anthropic/claude-opus-latest", "BÍ DANH"),
                  ("anthropic/claude-opus-5.5:nitro", "BIẾN THỂ"), ("anthropic/claude-opus-5.5:batch", "BIẾN THỂ"),
                  ("anthropic/claude-opus-9", "danh mục")):
        assert ly in (mh.loi_slug_openrouter(s) or ""), s


def test_AC3_slug_cam__CamGoiThat_0_loi_goi(may):
    goc, tt = may
    for s in ("google/gemini-3-pro", "~anthropic/claude-opus-latest", "anthropic/claude-opus-9"):
        with pytest.raises(mh.CamGoiThat):
            mh.tao_that(mh.MoHinh("anthropic", s, True, "OPENROUTER_API_KEY"), True, moi_truong=dict(DU), goc_api=goc)
    assert len(tt.yeu_cau) == 0


def test_AC3_doi_vai_trong_tep__agent_doi_slug_khong_sua_ma(tmp_path, monkeypatch):
    mt = mh.ma_tran_openrouter()
    mt["vai"]["lam"] = "openai/gpt-6.2-sol"
    p = tmp_path / "m.json"
    p.write_text(json.dumps(mt), encoding="utf-8")
    monkeypatch.setattr(mh, "TEP_MA_TRAN", p)
    assert mh.slug_openrouter(mh.OPUS_5_5) == "openai/gpt-6.2-sol"
    assert mh.slug_openrouter(mh.SONNET_5_5) == "anthropic/claude-sonnet-5.5"


def test_OR01_report_nhan_MOI_adapter_that_la_THAT():
    """Bia `OR-01`: tên adapter thật (đọc từ CHÍNH các lớp) ⊆ `report.NGUON_THAT`; GIẢ/phát lại ⛔ thuộc."""
    from fls.agent import report as rp
    that = {c.ten for c in (mh.AnthropicMessages, mh.AnthropicVertexMessages, mh.AnthropicGoogleCloudMessages,
                            mh.OpenRouterChat)}
    assert len(that) == 4 and that <= set(rp.NGUON_THAT)
    assert mh.GiaLap.ten not in rp.NGUON_THAT and mh.PhatLai.ten not in rp.NGUON_THAT


def test_vong_that_duong_openrouter_thieu_khoa__DO_co_ten_0_mang(monkeypatch):
    import vong_that_voi as vt
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("OPENROUTER_API_KEY")
    monkeypatch.delenv(vt.cav.BIEN_HELDOUT, raising=False)
    kq = vt.chay(co_that=True)
    assert kq["that"]["do"].startswith("thiếu OPENROUTER_API_KEY") and kq["nhat_ky"]["so_goi"] == 0
    assert "(OpenRouter — bên thứ ba" in vt.md(kq) and "⛔ thiếu OPENROUTER_API_KEY" in vt.md(kq)


def test_nhan_usd_openrouter__THAT_hay_UOC_theo_nguon():
    import chay_agent_voi as cav
    x = mh.NhatKyGoi("anthropic/claude-opus-5.5", 1, 1, 0, 0, 0.1, 0.5, "end_turn", "a", "b", duong="openrouter",
                     nguon_usd="THẬT")
    assert "USD THẬT (usage.cost" in cav.nhan_usd(mh.tong_nhat_ky([x]))
    y = mh.NhatKyGoi("anthropic/claude-opus-5.5", 1, 1, 0, 0, 0.1, 0.5, "end_turn", "a", "b", duong="openrouter",
                     nguon_usd="ƯỚC")
    assert "1 lời THẬT (usage.cost) + 1 lời ƯỚC" in cav.nhan_usd(mh.tong_nhat_ky([x, y]))
