# -*- coding: utf-8 -*-
"""`WO-359` — đường CHÍNH `google-cloud` (chủ 24/11 ~03:50: *"dùng claude.googleapis.com cho nhanh"*).

*Claude Models on Google Cloud (Anthropic managed)*: `anthropic.AnthropicGoogleCloud(project=…, workspace_id=…)`, service
`claude.googleapis.com`, ADC/SA + `roles/claude.user`, ⛔ khoá, mã mô hình như Claude API (tra skill `claude-api` 24/11).
SDK GIẢ dùng chung `sdk_gia` của `test_mo_hinh_vertex.py` (lớp `AnthropicGoogleCloud` ghi đối số dựng).
"""
from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from fls.agent import mo_hinh as mh
from tests.agent.test_mo_hinh_vertex import KHOA_GIA, YC, sdk_gia

WS = "wrkspc_01GiaChiDeThu"
#: Đủ chốt đường google-cloud — đường chọn RÕ, ⛔ khoá, ⛔ `FLS_ZDR_DA_BAT`.
DU_GC = {"FLS_CHO_GOI_API": "1", "FLS_NHA_CUNG_CAP": "google-cloud", "FLS_GCP_PROJECT": "fp-a-project", "FLS_CLAUDE_WORKSPACE_ID": WS,
         "FLS_GC_DU_LIEU_XAC_NHAN": "1"}


@pytest.fixture
def gc(monkeypatch):
    for k in ("ANTHROPIC_API_KEY", "FLS_ZDR_DA_BAT", "FLS_NHA_CUNG_CAP", "FLS_VERTEX_DU_LIEU_XAC_NHAN",
              "FLS_VERTEX_REGION"):
        monkeypatch.delenv(k, raising=False)
    for k, v in DU_GC.items():
        monkeypatch.setenv(k, v)


def _dung(monkeypatch, mo_hinh=mh.OPUS_5_5, **kw):
    sdk = sdk_gia(**kw)
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    return mh.tao_that(mo_hinh, co_that=True), sdk


def test_chon_ro_google_cloud__dung_AnthropicGoogleCloud_project_workspace(monkeypatch, gc):
    assert mh.duong_goi() == "google-cloud"
    assert mh.duong_goi({}) == mh.DUONG_MAC_DINH == "anthropic"     # biến vắng ⇒ WO-355 (bài nghiệm thu KQ-357 khoá)
    ncc, sdk = _dung(monkeypatch)
    assert isinstance(ncc, mh.AnthropicGoogleCloudMessages) and ncc.ten == "anthropic-google-cloud"
    assert sdk.lop == "AnthropicGoogleCloud"
    assert sdk.tao_voi == {"project": "fp-a-project", "workspace_id": WS, "max_retries": 2}   # ⛔ khoá · ⛔ URL tự viết
    ncc.goi(YC)
    kw = sdk.da_goi[0]
    assert kw["model"] == "claude-opus-5-5" and kw["output_config"] == {"effort": "medium"}
    assert not {"thinking", "tool_choice", "temperature", "top_p", "top_k", "fallbacks", "betas"} & set(kw)


def test_chu_ky_lop_SDK_that__project_workspace_id():
    sdk = pytest.importorskip("anthropic")
    ts = inspect.signature(sdk.AnthropicGoogleCloud.__init__).parameters
    assert {"project", "workspace_id", "max_retries"} <= set(ts)


def test_khong_doi_khoa_khong_doi_ZDR_cu(gc):
    mh.kiem_chot_that(mh.OPUS_5_5, True)


@pytest.mark.parametrize("bo,ten", [("FLS_CHO_GOI_API", "FLS_CHO_GOI_API"), ("FLS_GCP_PROJECT", "FLS_GCP_PROJECT"),
                                    ("FLS_CLAUDE_WORKSPACE_ID", "FLS_CLAUDE_WORKSPACE_ID"),
                                    ("FLS_GC_DU_LIEU_XAC_NHAN", "FLS_GC_DU_LIEU_XAC_NHAN")])
def test_moi_chot_thieu__CamGoiThat_co_ten(monkeypatch, gc, bo, ten):
    monkeypatch.delenv(bo)
    with pytest.raises(mh.CamGoiThat, match=ten):
        mh.kiem_chot_that(mh.OPUS_5_5, True)


@pytest.mark.parametrize("ws", ["wrkspc", "ws_123", "wrkspc_a;b", "sk-ant-xyz",
                                "wrkspc_", "wrkspc_é", "wrkspc____", "wrkspc_a b", "WRKSPC_x"])   # +5: `AG3-R1-04`
def test_workspace_sai_dang__CHAN(monkeypatch, gc, ws):
    monkeypatch.setenv("FLS_CLAUDE_WORKSPACE_ID", ws)
    with pytest.raises(mh.CamGoiThat, match="đúng dạng"):
        mh.kiem_chot_that(mh.OPUS_5_5, True)


def test_ZDR_cu_va_xac_nhan_vertex_KHONG_thay_duoc(monkeypatch, gc):
    """Tổ chức Anthropic MỚI — *"A Zero Data Retention arrangement doesn't carry over"* ⇒ hai xác nhận cũ ⛔ mở cổng."""
    monkeypatch.delenv("FLS_GC_DU_LIEU_XAC_NHAN")
    monkeypatch.setenv("FLS_ZDR_DA_BAT", "1")
    monkeypatch.setenv("FLS_VERTEX_DU_LIEU_XAC_NHAN", "1")
    with pytest.raises(mh.CamGoiThat, match="FLS_GC_DU_LIEU_XAC_NHAN"):
        mh.kiem_chot_that(mh.OPUS_5_5, True)
    mh.kiem_chot_that(mh.OPUS_5_5, True, che_do="che_het")        # che lại ⇒ ⛔ đòi


@pytest.mark.parametrize("du_an", ["du-an-ca-nhan", "fpa-t-494007"])
def test_AC5_project_ngoai_cong_ty__CHAN(monkeypatch, gc, du_an):
    monkeypatch.setenv("FLS_GCP_PROJECT", du_an)
    with pytest.raises(mh.CamGoiThat, match="GCP công ty"):
        mh.kiem_chot_that(mh.OPUS_5_5, True)


def test_nhat_ky__duong_google_cloud__gia_uoc_ngay_tra__KHONG_noi_dung(monkeypatch, gc):
    ncc, _ = _dung(monkeypatch, usage=(1_000_000, 100_000))
    ncc.goi(YC)
    x = ncc.nhat_ky[0].dict()
    assert (x["duong"], x["vung"], x["ngay_tra_gia"]) == ("google-cloud", "global", "2026-11-24")
    assert x["chi_phi_usd"] == pytest.approx(6.0)                 # ƯỚC = giá Claude API (CHƯA có bảng giá chính thức)
    van = json.dumps(x, ensure_ascii=False)
    assert "0123456789" not in van and "lam di" not in van and KHOA_GIA not in van and WS not in van


def test_tran_USD_giu(monkeypatch, gc):
    sdk = sdk_gia(usage=(1_000_000, 0))
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    ncc = mh.tao_that(mh.OPUS_5_5, True, tran_usd=5.0)
    ncc.goi(YC)
    ncc.goi(YC)
    with pytest.raises(mh.VuotTran):
        ncc.goi(YC)
    assert len(sdk.da_goi) == 2


def test_loi_xac_thuc__LoiApi_co_ten(monkeypatch, gc):
    class RefreshError(Exception):
        pass
    RefreshError.__module__ = "google.auth.exceptions"
    ncc, _ = _dung(monkeypatch, loi=lambda _m: RefreshError("token /home/x/adc.json het han"))
    with pytest.raises(mh.LoiApi, match="RefreshError .*đường `google-cloud`") as e:
        ncc.goi(YC)
    assert "adc.json" not in str(e.value)


def test_HTTP_403_thieu_claude_user__LoiApi(monkeypatch, gc):
    ncc, _ = _dung(monkeypatch, loi=lambda m: m.APIStatusError(403))
    with pytest.raises(mh.LoiApi, match="HTTP 403"):
        ncc.goi(YC)


def test_chuoi_4_agent__duong_google_cloud__A4_4_4(monkeypatch, gc):
    import chay_agent_voi as cav
    from fls.agent import ghep_noi_dung as gnd
    sdk = sdk_gia(luat={"ung_vien_ghep": gnd.luat_gia_v1})
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    ncc = cav.ncc_cho("that", True, che="mo", tran_usd=2.0)
    assert ncc and all(isinstance(n, mh.AnthropicGoogleCloudMessages) for n in ncc.values())
    kc, *_ = cav.chay("that", ncc=ncc, cho_heldout=False)
    assert kc.dat and kc.dung_o is None, kc.dung_o
    assert {x.duong for x in cav.nhat_ky_cua(ncc)} == {"google-cloud"}


def test_vong_that__thieu_workspace__exit_2__DO_co_ten(monkeypatch, capsys, tmp_path, gc):
    import vong_that_voi as vt
    monkeypatch.delenv("FLS_CLAUDE_WORKSPACE_ID")
    monkeypatch.delenv(vt.cav.BIEN_HELDOUT, raising=False)
    monkeypatch.setattr(vt, "TM_RA", tmp_path)
    assert vt.main(["--that"]) == 2
    ra = capsys.readouterr().out
    assert "**KẾT: ĐỎ** — thiếu FLS_CLAUDE_WORKSPACE_ID" in ra
    assert "| đường gọi thật | `google-cloud`" in ra and "ANTHROPIC_API_KEY" not in ra


def test_vong_that__chay_THAT_google_cloud__report_ghi_chua_co_bang_gia(monkeypatch, capsys, tmp_path, gc):
    import vong_that_voi as vt
    from fls.agent import ghep_noi_dung as gnd
    monkeypatch.delenv(vt.cav.BIEN_HELDOUT, raising=False)
    monkeypatch.setattr(vt, "TM_RA", tmp_path)
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia(luat={"ung_vien_ghep": gnd.luat_gia_v1}))
    rc = vt.main(["--that", "--tran-usd", "2"])
    ra = capsys.readouterr().out
    assert rc == 0, ra
    assert "**KẾT: ĐẠT**" in ra and "CHƯA có bảng giá" in ra and "đường google-cloud" in ra and WS not in ra
