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
