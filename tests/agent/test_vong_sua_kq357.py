# -*- coding: utf-8 -*-
"""Vòng sửa sau R1 `KQ-357` (sổ `SO_PHAT_HIEN_ISP-3.1_AG2.md`) — `AG2-R1-02` · `-04` (bài cho `-01` ở `test_phu_thuoc_agent.py`)."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from tests.agent.test_mo_hinh_that import DU, sdk_gia


def test_AG2_R1_02__bo_ca_nhan_bo_cuc_a_b_cua_dung_be(monkeypatch, tmp_path):
    import chay_agent_voi as cav
    (tmp_path / "b").mkdir()
    shutil.copy(cav.CA_DUNG, tmp_path / "b" / "ca.json")
    shutil.copy(cav.DAP_AN_DUNG, tmp_path / "b" / "dap_an.json")
    monkeypatch.setenv(cav.BIEN_HELDOUT, str(tmp_path))
    ca, dap, nhan = cav.bo_ca()
    assert nhan == "giữ riêng — bể B (ngoài repo)" and ca["ca"] and dap["noi"]
    shutil.copy(cav.CA_DUNG, tmp_path / "ca.json")
    shutil.copy(cav.DAP_AN_DUNG, tmp_path / "dap_an.json")
    assert cav.bo_ca()[2] == "giữ riêng (ngoài repo)"                 # bố cục phẳng cũ vẫn ưu tiên


def test_AG2_R1_02__thu_muc_rong__DO_co_ten(monkeypatch, tmp_path):
    import chay_agent_voi as cav
    monkeypatch.setenv(cav.BIEN_HELDOUT, str(tmp_path))
    with pytest.raises(FileNotFoundError, match="b/ca.json"):
        cav.bo_ca()


def test_AG2_R1_04__nhat_ky_ghi_LUON_khi_co_loi_goi_that__khong_can_ghi(monkeypatch, tmp_path, capsys):
    import chay_agent_voi as cav
    import vong_that_voi as vt
    from fls.agent import ghep_noi_dung as gnd
    from fls.agent import mo_hinh as mh
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setenv("FLS_NHA_CUNG_CAP", "anthropic")
    monkeypatch.delenv(cav.BIEN_HELDOUT, raising=False)
    monkeypatch.setitem(sys.modules, "anthropic", sdk_gia(dap=lambda kw: mh.GiaLap({"ung_vien_ghep": gnd.luat_gia_v1}).goi(kw)))
    goc = cav.ghi_nhat_ky
    monkeypatch.setattr(cav, "ghi_nhat_ky", lambda ncc, nhan, tm=None: goc(ncc, nhan, tmp_path))
    monkeypatch.setattr(vt, "TM_RA", tmp_path / "khong_duoc_ghi")
    vt.main(["--that", "--tran-usd", "50"])                           # ⛔ `--ghi`
    tep = list(tmp_path.glob("*_vong_that.json"))
    assert len(tep) == 1 and json.loads(tep[0].read_text(encoding="utf-8"))["tong"]["so_goi"] > 0
    assert not (tmp_path / "khong_duoc_ghi").exists()                 # report ⛔ ghi khi thiếu `--ghi`


def test_AG2_R1_04__thieu_chot__0_loi_goi__KHONG_sinh_tep(monkeypatch, tmp_path):
    import chay_agent_voi as cav
    import vong_that_voi as vt
    monkeypatch.delenv("FLS_CHO_GOI_API", raising=False)
    monkeypatch.delenv(cav.BIEN_HELDOUT, raising=False)
    goc = cav.ghi_nhat_ky
    monkeypatch.setattr(cav, "ghi_nhat_ky", lambda ncc, nhan, tm=None: goc(ncc, nhan, tmp_path))
    assert vt.main(["--that"]) == 2
    assert not list(tmp_path.iterdir())


# ── vòng sửa sau R1 `KQ-361` ───────────────────────────────────────────────────────────────────────────────
def _sdk_loi_o_loi_thu(k: int, loi_cua):
    """SDK giả: lời 1…k-1 trả như mô hình GIẢ, lời thứ k ném lỗi `loi_cua(module_sdk)`."""
    from fls.agent import ghep_noi_dung as gnd
    from fls.agent import mo_hinh as mh
    dem = {"n": 0}

    def dap(kw):
        dem["n"] += 1
        if dem["n"] == k:
            raise loi_cua(sdk)
        return mh.GiaLap({"ung_vien_ghep": gnd.luat_gia_v1}).goi(kw)
    sdk = sdk_gia(dap=dap)
    return sdk


@pytest.mark.parametrize("loai", ["ket_noi", "xac_thuc"])
def test_AG3_R1_01__LoiApi_giua_chung__nhat_ky_co_k_tru_1_loi_goi_va_dong_loi(monkeypatch, tmp_path, capsys, loai):
    """Lời thứ 3 hỏng (mạng / token ADC hết hạn) ⇒ nhật ký có ĐÚNG 2 lời đã tính tiền + 1 dòng `loi` CÓ TÊN · exit ≠ 0 ·
    report in `LoiApi` (bản cũ: traceback, 0 tệp)."""
    import chay_agent_voi as cav
    import vong_that_voi as vt
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setenv("FLS_NHA_CUNG_CAP", "anthropic")
    monkeypatch.delenv(cav.BIEN_HELDOUT, raising=False)

    class DefaultCredentialsError(Exception):
        pass
    DefaultCredentialsError.__module__ = "google.auth.exceptions"
    loi = (lambda m: m.APIConnectionError("mat mang — NOI DUNG khong lot")) if loai == "ket_noi" else \
          (lambda m: DefaultCredentialsError("/home/x/adc.json het han"))
    sdk = _sdk_loi_o_loi_thu(3, loi)
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    if loai == "xac_thuc":                      # đường khoá chỉ đổi tên lỗi google.auth khi ở đường GCP ⇒ dùng vertex
        for k, v in {"FLS_NHA_CUNG_CAP": "vertex", "FLS_GCP_PROJECT": "fp-a-project",
                     "FLS_VERTEX_DU_LIEU_XAC_NHAN": "1"}.items():
            monkeypatch.setenv(k, v)

        class AnthropicVertex:
            def __init__(self, **kw):
                self.messages = sdk.Anthropic().messages
        sdk.AnthropicVertex = AnthropicVertex
    monkeypatch.setattr(vt, "TM_RA", tmp_path / "ra")
    rc = vt.main(["--that", "--tran-usd", "50"])
    out = capsys.readouterr().out
    assert rc != 0 and "LoiApi giữa chừng" in out, out[-600:]
    tep = list((tmp_path / "nhat_ky").glob("*_vong_that.json"))
    assert len(tep) == 1, tep
    d = json.loads(tep[0].read_text(encoding="utf-8"))
    assert d["tong"]["so_goi"] == len(d["goi"]) == 2
    assert "LoiApi" in d["loi"] and ("APIConnectionError" in d["loi"] or "DefaultCredentialsError" in d["loi"])
    van = json.dumps(d, ensure_ascii=False) + out
    assert "NOI DUNG" not in van and "adc.json" not in van


def test_AG3_R1_01__ngoai_le_chua_luong__van_ghi_nhat_ky_roi_nem_lai(monkeypatch, tmp_path):
    import chay_agent_voi as cav
    import vong_that_voi as vt
    for k, v in DU.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setenv("FLS_NHA_CUNG_CAP", "anthropic")
    monkeypatch.delenv(cav.BIEN_HELDOUT, raising=False)
    monkeypatch.setitem(sys.modules, "anthropic", _sdk_loi_o_loi_thu(2, lambda m: KeyboardInterrupt()))
    monkeypatch.setattr(vt, "TM_RA", tmp_path / "ra")
    with pytest.raises(KeyboardInterrupt):
        vt.main(["--that", "--tran-usd", "50"])
    d = json.loads(next((tmp_path / "nhat_ky").glob("*_vong_that.json")).read_text(encoding="utf-8"))
    assert d["tong"]["so_goi"] == 1 and d["loi"].startswith("KeyboardInterrupt")


@pytest.mark.parametrize("duong,chu", [("google-cloud", "CHƯA có bảng giá"), ("vertex", "giả định chưa kiểm"),
                                       ("anthropic", "giá Claude API")])
def test_AG3_R1_03__moi_dong_USD_in_ra__co_nhan_UOC(monkeypatch, tmp_path, capsys, duong, chu):
    """Chạy THẬT (SDK giả) cả `chay_agent_voi` lẫn `vong_that_voi` trên MỖI đường ⇒ MỌI dòng stdout có `USD` (trừ
    tiêu đề cột bảng) mang `ƯỚC`; nguồn giá đúng đường."""
    import chay_agent_voi as cav
    import vong_that_voi as vt
    from fls.agent import ghep_noi_dung as gnd
    from fls.agent import mo_hinh as mh
    env = {**DU, "FLS_NHA_CUNG_CAP": duong, "FLS_GCP_PROJECT": "fp-a-project", "FLS_CLAUDE_WORKSPACE_ID": "wrkspc_01Gia",
           "FLS_GC_DU_LIEU_XAC_NHAN": "1", "FLS_VERTEX_DU_LIEU_XAC_NHAN": "1"}
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv(cav.BIEN_HELDOUT, raising=False)
    sdk = sdk_gia(dap=lambda kw: mh.GiaLap({"ung_vien_ghep": gnd.luat_gia_v1}).goi(kw))
    sdk.AnthropicVertex = sdk.AnthropicGoogleCloud = lambda **kw: sdk.Anthropic()
    monkeypatch.setitem(sys.modules, "anthropic", sdk)
    monkeypatch.setattr(vt, "TM_RA", tmp_path / "ra")
    cav.main(["--that", "--tran-usd", "50"])
    vt.main(["--that", "--tran-usd", "50"])
    import re
    dong = [d for d in capsys.readouterr().out.splitlines()
            if re.search(r"(?<![_A-Za-z])USD(?![_A-Za-z])", d) and not d.startswith("| lời gọi")]   # ⛔ "_USD_" trong đường tmp
    assert len(dong) >= 3, dong                                           # Đ3: mẫu số ≠ 0 (API THẬT · Sau tập nhỏ · Giá tra)
    thieu = [d for d in dong if "ƯỚC" not in d.upper() and "ước" not in d]
    assert not thieu, thieu
    assert any(chu in d for d in dong), dong


def test_AG3_R1_05__thu_muc_co_san_KHONG_bi_doi_quyen__thu_muc_moi_700(tmp_path, capsys):
    import os
    import dung_be_giu_rieng as bg
    co_san = tmp_path / "co_san"
    co_san.mkdir()
    os.chmod(co_san, 0o755)
    da_tao = bg.tao_thu_muc_rieng(co_san / "be" / "b")
    assert [p.name for p in da_tao] == ["b", "be"]
    assert oct(co_san.stat().st_mode & 0o777) == "0o755"                     # có sẵn ⇒ GIỮ
    assert all(oct(p.stat().st_mode & 0o777) == "0o700" for p in da_tao)     # tự tạo ⇒ 700
    assert "rộng hơn 700" in capsys.readouterr().out
    assert bg.tao_thu_muc_rieng(co_san / "be" / "b") == []                   # chạy lại ⇒ ⛔ tạo, ⛔ đổi
    assert oct(co_san.stat().st_mode & 0o777) == "0o755"
