# -*- coding: utf-8 -*-
"""`WO-359` AC-1 · AC-2 · AC-5 — đường **Claude trên Vertex AI** (`FLS_NHA_CUNG_CAP=vertex`), đo bằng SDK `anthropic` GIẢ.

SDK giả có lớp `AnthropicVertex(project_id=…, region=…)` (đúng chữ ký tra 24/11 trên `anthropic` 2.13.0:
`region` · `project_id` · `access_token` · `credentials` · `max_retries`…) và ghi lại đối số dựng + mọi tham số gửi.
⛔ mạng · ⛔ khoá · ⛔ ADC thật. Lỗi xác thực mô phỏng bằng một lớp lỗi đặt `__module__ = "google.auth.exceptions"` —
đúng nơi `google-auth` khai `DefaultCredentialsError` (đo: `google.auth.exceptions.DefaultCredentialsError.__module__`).
"""
from __future__ import annotations

import inspect
import json
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from fls.agent import chuoi as ch
from fls.agent import mo_hinh as mh

KHOA_GIA = "sk-ant-GIA-chi-de-thu-0000"
#: Đủ chốt đường VERTEX — cố ý ⛔ có `ANTHROPIC_API_KEY` (AC-2: bỏ đòi khoá) và ⛔ có `FLS_ZDR_DA_BAT` (đã THAY).
DU_VX = {"FLS_CHO_GOI_API": "1", "FLS_NHA_CUNG_CAP": "vertex", "FLS_GCP_PROJECT": "fp-a-project",
         "FLS_VERTEX_DU_LIEU_XAC_NHAN": "1"}


class _Msg:
    def __init__(self, d: dict):
        self._d, self._request_id = d, ""            # Vertex: request-id có thể RỖNG — nhật ký phải chịu được

    def to_dict(self) -> dict:
        return json.loads(json.dumps(self._d))


def sdk_gia(loi=None, mo_hinh_phuc_vu=None, usage=(1000, 200), luat=None):
    m = types.ModuleType("anthropic")

    class APIError(Exception):
        pass

    class APIStatusError(APIError):
        def __init__(self, status_code: int):
            super().__init__(f"HTTP {status_code}")
            self.status_code, self.request_id = status_code, None

    class APIConnectionError(APIError):
        pass

    m.APIError, m.APIStatusError, m.APIConnectionError = APIError, APIStatusError, APIConnectionError
    m.da_goi, m.tao_voi = [], None

    class _Messages:
        def create(self, **kw):
            m.da_goi.append(kw)
            if loi is not None:
                raise loi(m)
            tl = mh.GiaLap(luat).goi({**kw, "tools": kw.get("tools", [])})
            return _Msg({**tl, "model": mo_hinh_phuc_vu or kw["model"],
                         "usage": {"input_tokens": usage[0], "output_tokens": usage[1],
                                   "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}})

    class AnthropicVertex:
        def __init__(self, *, region, project_id, max_retries=2, **kw):
            m.tao_voi = {"region": region, "project_id": project_id, "max_retries": max_retries, **kw}
            m.lop = "AnthropicVertex"
            self.messages = _Messages()

    class Anthropic:                                  # dựng nhầm lớp này ở đường vertex ⇒ bài phải ĐỎ
        def __init__(self, **kw):
            m.tao_voi, m.lop = kw, "Anthropic"
            self.messages = _Messages()

    class AnthropicGoogleCloud:                       # WO-359 đường chính: chữ ký đối chiếu SDK 2.13.0 (`project` · `workspace_id`)
        def __init__(self, *, project=None, workspace_id=None, max_retries=2, **kw):
            m.tao_voi = {"project": project, "workspace_id": workspace_id, "max_retries": max_retries, **kw}
            m.lop = "AnthropicGoogleCloud"
            self.messages = _Messages()

    m.AnthropicVertex, m.Anthropic, m.AnthropicGoogleCloud = AnthropicVertex, Anthropic, AnthropicGoogleCloud
    return m


@pytest.fixture
def vx(monkeypatch):
    for k in ("ANTHROPIC_API_KEY", "FLS_ZDR_DA_BAT", "FLS_VERTEX_REGION"):
        monkeypatch.delenv(k, raising=False)
    for k, v in DU_VX.items():
        monkeypatch.setenv(k, v)


def _dung(monkeypatch, mo_hinh=mh.OPUS_5_5, **kw):
    sdk = sdk_gia(**kw)
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    return mh.tao_that(mo_hinh, co_that=True), sdk


YC = {"model": "claude-opus-5-5", "max_tokens": 16000, "system": "he thong",
      "tools": [{"name": "cc", "description": "d", "input_schema": {"type": "object", "properties": {}}}],
      "messages": [{"role": "user", "content": "STK 0123456789 lam di"}]}


# ── AC-1 · chọn đường bằng cấu hình, dựng ĐÚNG lớp `AnthropicVertex` ─────────────────────────────────────────
def test_AC1_vertex__dung_AnthropicVertex_project_region_global__ma_tran(monkeypatch, vx):
    ncc, sdk = _dung(monkeypatch)
    assert isinstance(ncc, mh.AnthropicVertexMessages) and ncc.ten == "anthropic-vertex"
    assert sdk.lop == "AnthropicVertex"
    assert sdk.tao_voi == {"region": "global", "project_id": "fp-a-project", "max_retries": 2}   # ⛔ khoá nào
    ncc.goi(YC)
    kw = sdk.da_goi[0]
    # mã Vertex của Opus 5.5 = mã TRẦN (⛔ tiền tố `anthropic.`, ⛔ `@ngày`) — tra 24/11
    assert kw["model"] == "claude-opus-5-5" and "@" not in kw["model"]
    # CÙNG tham số như đường API (WO-355): effort RÕ · ⛔ thinking/tool_choice/sampling/fallbacks
    assert kw["output_config"] == {"effort": "medium"}
    assert not {"thinking", "tool_choice", "temperature", "top_p", "top_k", "fallbacks", "betas"} & set(kw)


@pytest.mark.parametrize("vung", ["us", "eu"])
def test_AC1_vung_da_vung__nhan_va_gui_dung(monkeypatch, vx, vung):
    monkeypatch.setenv("FLS_VERTEX_REGION", vung)
    _, sdk = _dung(monkeypatch, mo_hinh=mh.SONNET_5_5)
    assert sdk.tao_voi["region"] == vung


def test_AC1_duong_API_du_phong__chon_RO_bang_bien(monkeypatch):
    """`FLS_NHA_CUNG_CAP=anthropic` ⇒ đường khoá (WO-355 giữ làm dự phòng). Biến VẮNG ⇒ cũng `anthropic` (KQ-357 khoá)."""
    for k, v in {"FLS_CHO_GOI_API": "1", "ANTHROPIC_API_KEY": KHOA_GIA, "FLS_ZDR_DA_BAT": "1",
                 "FLS_NHA_CUNG_CAP": "anthropic"}.items():
        monkeypatch.setenv(k, v)
    ncc, sdk = _dung(monkeypatch)
    assert type(ncc) is mh.AnthropicMessages and sdk.lop == "Anthropic" and mh.duong_goi() == "anthropic"
    monkeypatch.delenv("FLS_NHA_CUNG_CAP")
    assert mh.duong_goi() == "anthropic"


def test_AC1_chu_ky_lop_SDK_that__co_region_project_id():
    """Bài canh SDK THẬT (đã cài `anthropic[vertex]`): tên lớp + tên tham số mà adapter truyền phải tồn tại."""
    sdk = pytest.importorskip("anthropic")
    ts = inspect.signature(sdk.AnthropicVertex.__init__).parameters
    assert {"region", "project_id", "max_retries"} <= set(ts)


# ── AC-2 · chốt: giữ 3 chốt chung · bỏ khoá · THAY ZDR ──────────────────────────────────────────────────────
def test_AC2_vertex__KHONG_doi_ANTHROPIC_API_KEY(vx):
    mh.kiem_chot_that(mh.OPUS_5_5, True)            # ⛔ ném = được gọi (khoá vắng, ZDR vắng)


@pytest.mark.parametrize("bo,ten", [
    ("FLS_CHO_GOI_API", "FLS_CHO_GOI_API"),
    ("FLS_GCP_PROJECT", "FLS_GCP_PROJECT"),
    ("FLS_VERTEX_DU_LIEU_XAC_NHAN", "FLS_VERTEX_DU_LIEU_XAC_NHAN"),
])
def test_AC2_moi_chot_thieu__CamGoiThat_co_ten(monkeypatch, vx, bo, ten):
    monkeypatch.delenv(bo)
    with pytest.raises(mh.CamGoiThat, match=ten):
        mh.kiem_chot_that(mh.OPUS_5_5, True)


def test_AC2_co_that_vang__van_chan(vx):
    with pytest.raises(mh.CamGoiThat, match="--that"):
        mh.kiem_chot_that(mh.OPUS_5_5, False)


def test_AC2_ZDR_cu_KHONG_thay_duoc_xac_nhan_vertex(monkeypatch, vx):
    """`FLS_ZDR_DA_BAT=1` (xác nhận của tài khoản Anthropic) ⛔ mở được đường Vertex — hai cam kết khác nhau."""
    monkeypatch.delenv("FLS_VERTEX_DU_LIEU_XAC_NHAN")
    monkeypatch.setenv("FLS_ZDR_DA_BAT", "1")
    with pytest.raises(mh.CamGoiThat, match="FLS_VERTEX_DU_LIEU_XAC_NHAN"):
        mh.kiem_chot_that(mh.OPUS_5_5, True)


@pytest.mark.parametrize("che", ["che_noi_dung", "che_het"])
def test_AC2_che_lai__khong_doi_xac_nhan_du_lieu(monkeypatch, vx, che):
    monkeypatch.delenv("FLS_VERTEX_DU_LIEU_XAC_NHAN")
    mh.kiem_chot_that(mh.OPUS_5_5, True, che_do=che)


@pytest.mark.parametrize("vung", ["asia-southeast1", "us-east5", "europe-west1", "khong-co"])
def test_AC2_vung_don__CHAN_vi_khong_phuc_vu_Opus_Sonnet_5_5(monkeypatch, vx, vung):
    """Tra 24/11: *"Regional endpoints serve Claude Sonnet 4.6 and earlier models only"* — ⛔ để GCP trả 404 lúc chạy."""
    monkeypatch.setenv("FLS_VERTEX_REGION", vung)
    with pytest.raises(mh.CamGoiThat, match=f"vùng Vertex `{vung}`"):
        mh.kiem_chot_that(mh.OPUS_5_5, True)


def test_AC2_duong_la__CamGoiThat_co_ten(monkeypatch, vx):
    monkeypatch.setenv("FLS_NHA_CUNG_CAP", "gemini")
    with pytest.raises(mh.CamGoiThat, match="FLS_NHA_CUNG_CAP=gemini"):
        mh.tao_that(mh.OPUS_5_5, True)


def test_AC2_tran_USD_giu_nguyen_tren_vertex(monkeypatch, vx):
    nk: list = []
    sdk = sdk_gia(usage=(1_000_000, 0))
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    ncc = mh.tao_that(mh.OPUS_5_5, True, tran_usd=5.0, nhat_ky=nk)
    ncc.goi(YC)                                       # ~4 USD
    ncc.goi(YC)                                       # ~8 USD (đã tiêu 4 < 5 ⇒ vẫn gọi)
    with pytest.raises(mh.VuotTran):
        ncc.goi(YC)
    assert len(sdk.da_goi) == 2


def test_AC2_nhat_ky__duong_vung_gia_vertex__KHONG_noi_dung(monkeypatch, vx):
    ncc, _ = _dung(monkeypatch, usage=(1_000_000, 100_000))
    ncc.goi(YC)
    x = ncc.nhat_ky[0].dict()
    assert (x["duong"], x["vung"]) == ("vertex", "global")
    assert x["ngay_tra_gia"] == mh.NGAY_TRA_GIA_VERTEX == "2026-11-24"
    assert x["chi_phi_usd"] == pytest.approx(4.0 + 2.0)       # global = giá Claude API (giả định chưa kiểm, BG-360)
    van = json.dumps(x, ensure_ascii=False)
    assert "lam di" not in van and "0123456789" not in van and "he thong" not in van and KHOA_GIA not in van
    t = mh.tong_nhat_ky(ncc.nhat_ky)
    assert t["duong"] == ["vertex"] and t["vung"] == ["global"] and t["ngay_tra_gia"] == "2026-11-24"


def test_AC2_gia_da_vung__cong_10_phan_tram(monkeypatch, vx):
    monkeypatch.setenv("FLS_VERTEX_REGION", "eu")
    ncc, _ = _dung(monkeypatch, mo_hinh=mh.SONNET_5_5, usage=(1_000_000, 1_000_000))
    ncc.goi({**YC, "model": "claude-sonnet-5-5"})
    assert ncc.nhat_ky[0].chi_phi_usd == pytest.approx(1.1 * 12.0)
    with pytest.raises(KeyError):
        mh.chi_phi("claude-opus-5-5", 1, 1, duong="vertex", vung="asia-southeast1")   # ⛔ đoán hệ số


def test_AC2_loi_xac_thuc_google_auth__LoiApi_co_ten(monkeypatch, vx):
    class DefaultCredentialsError(Exception):
        pass
    DefaultCredentialsError.__module__ = "google.auth.exceptions"

    def loi(_m):
        return DefaultCredentialsError("File /home/x/adc.json was not found — chi tiet KHONG lot")
    ncc, _ = _dung(monkeypatch, loi=loi)
    with pytest.raises(mh.LoiApi, match="DefaultCredentialsError .*xác thực GCP") as e:
        ncc.goi(YC)
    assert "adc.json" not in str(e.value) and "lam di" not in str(e.value)


def test_AC2_loi_khac_KHONG_bi_doi_ten(monkeypatch, vx):
    def loi(_m):
        return ZeroDivisionError("loi lap trinh")
    ncc, _ = _dung(monkeypatch, loi=loi)
    with pytest.raises(ZeroDivisionError):
        ncc.goi(YC)


def test_AC2_HTTP_403_Model_Garden_chua_bat__LoiApi(monkeypatch, vx):
    def loi(m):
        return m.APIStatusError(403)
    ncc, _ = _dung(monkeypatch, loi=loi)
    with pytest.raises(mh.LoiApi, match="HTTP 403"):
        ncc.goi(YC)


def test_AC2_Vertex_phuc_vu_bang_mo_hinh_khac__DO(monkeypatch, vx):
    ncc, _ = _dung(monkeypatch, mo_hinh_phuc_vu="claude-opus-5")
    with pytest.raises(mh.LoiApi, match="≠ ghim"):
        ncc.goi(YC)


def test_AC2_adapter_sai_duong__CamGoiThat(monkeypatch, vx):
    """Dựng thẳng `AnthropicMessages` khi cấu hình nói vertex ⇒ ĐỎ (⛔ lặng lẽ đi đường khoá)."""
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia())
    with pytest.raises(mh.CamGoiThat):
        mh.AnthropicMessages(mh.OPUS_5_5, True)


# ── AC-5 · chỉ GCP của công ty ──────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("du_an", ["du-an-ca-nhan", "fpa-t-494007", "fp-a-project-x"])
def test_AC5_project_ngoai_cong_ty__CHAN(monkeypatch, vx, du_an):
    monkeypatch.setenv("FLS_GCP_PROJECT", du_an)
    with pytest.raises(mh.CamGoiThat, match="GCP công ty"):
        mh.kiem_chot_that(mh.OPUS_5_5, True)


def test_AC5_danh_sach_project_cong_ty__dung_mot():
    assert mh.DU_AN_CONG_TY == ("fp-a-project",)


def test_AC1_chuoi_4_agent__chay_tron_tren_vertex(monkeypatch, vx):
    """Chuỗi 4 agent qua `chay_agent_voi` trên đường vertex ⇒ mọi adapter là Vertex, A4 4/4, nhật ký ghi đường."""
    import chay_agent_voi as cav
    from fls.agent import ghep_noi_dung as gnd
    sdk = sdk_gia(luat={"ung_vien_ghep": gnd.luat_gia_v1})
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    ncc = cav.ncc_cho("that", True, che="mo", tran_usd=2.0)
    assert ncc and all(isinstance(n, mh.AnthropicVertexMessages) for n in ncc.values())
    kc, *_ = cav.chay("that", ncc=ncc, cho_heldout=False)
    assert kc.dat and kc.dung_o is None, kc.dung_o
    assert sdk.da_goi and {k["model"] for k in sdk.da_goi} == {"claude-opus-5-5"}      # A4 ⛔ lượt (MÃ tới G1)
    assert {x.duong for x in cav.nhat_ky_cua(ncc)} == {"vertex"}


# ── AC-4 · bể giữ riêng dựng được ở Cloud Shell (⛔ đòi secret của phiên cloud) ─────────────────────────────
def test_AC4_be_giu_rieng__cach_xac_thuc_theo_thu_tu__chi_TEN():
    import dung_be_giu_rieng as bg
    assert bg.cach_xac_thuc({"FLS_SHEETS_TOKEN": "t", "FLS_GSHEETS_SA_JSON_B64": "x"}) == "FLS_SHEETS_TOKEN"
    assert bg.cach_xac_thuc({"FLS_SHEETS_SA_JSON_TEP": "/tmp/k.json"}) == "FLS_SHEETS_SA_JSON_TEP"
    assert bg.cach_xac_thuc({"FLS_GSHEETS_SA_JSON_B64": "x"}) == "FLS_GSHEETS_SA_JSON_B64"
    with pytest.raises(RuntimeError, match="thiếu quyền đọc sheet"):
        bg.cach_xac_thuc({})
    assert bg.PHAM_VI_DOC == ["https://www.googleapis.com/auth/spreadsheets.readonly"]      # ⛔ phạm vi ghi


def test_AC4_vong_that__duong_vertex_thieu_project__exit_2__DO_co_ten(monkeypatch, capsys, tmp_path):
    import vong_that_voi as vt
    for k in ("FLS_GCP_PROJECT", "FLS_CHO_GOI_API", "ANTHROPIC_API_KEY", vt.cav.BIEN_HELDOUT):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("FLS_NHA_CUNG_CAP", "vertex")
    monkeypatch.setattr(vt, "TM_RA", tmp_path)
    assert vt.main(["--that"]) == 2
    ra = capsys.readouterr().out
    assert "**KẾT: ĐỎ** — thiếu FLS_GCP_PROJECT (đường vertex)" in ra
    assert "| đường gọi thật | `vertex` (Claude trên Vertex AI — dự phòng, WO-359) |" in ra
    assert "| A4 ĐẠT (agent) | 4/4 | ⛔ thiếu FLS_GCP_PROJECT |" in ra and "**0 lời gọi thật**" in ra
    assert "ANTHROPIC_API_KEY" not in ra                              # AC-2: đường vertex ⛔ đòi khoá


def test_AC4_vong_that__chay_THAT_tren_vertex__report_ghi_duong_vung_gia(monkeypatch, capsys, tmp_path, vx):
    """Đủ chốt vertex + SDK GIẢ ⇒ vòng (a) chạy, report ghi đường · vùng · ngày tra giá Vertex; ⛔ nội dung."""
    import vong_that_voi as vt
    from fls.agent import ghep_noi_dung as gnd
    monkeypatch.delenv(vt.cav.BIEN_HELDOUT, raising=False)
    monkeypatch.setattr(vt, "TM_RA", tmp_path)
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia(luat={"ung_vien_ghep": gnd.luat_gia_v1}))
    rc = vt.main(["--that", "--tran-usd", "2"])
    ra = capsys.readouterr().out
    assert rc == 0, ra
    assert "**KẾT: ĐẠT**" in ra and "giả định chưa kiểm" in ra and "đường vertex · vùng global" in ra
    assert "2026-11-24" in ra
