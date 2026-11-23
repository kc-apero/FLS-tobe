# -*- coding: utf-8 -*-
"""WO-329 AC-3 — gọi API THẬT chỉ khi đủ chốt; mặc định PHÁT LẠI; ⛔ bí danh; giao diện ⛔ cứng một hãng."""
from __future__ import annotations

import sys

import pytest

from fls.agent import mo_hinh as mh

DU = {"FLS_CHO_GOI_API": "1", "ANTHROPIC_API_KEY": "khoa-gia-de-thu"}


def test_du_chot__khong_nem():
    mh.kiem_chot_that(mh.OPUS_5_5, True, DU)


@pytest.mark.parametrize("co_that,mt,chu", [
    (False, DU, "--that"),
    (True, {"ANTHROPIC_API_KEY": "k"}, "FLS_CHO_GOI_API"),
    (True, {"FLS_CHO_GOI_API": "0", "ANTHROPIC_API_KEY": "k"}, "FLS_CHO_GOI_API"),
    (True, {"FLS_CHO_GOI_API": "1"}, "ANTHROPIC_API_KEY"),
])
def test_thieu_mot_chot__CamGoiThat(co_that, mt, chu):
    with pytest.raises(mh.CamGoiThat, match=chu):
        mh.kiem_chot_that(mh.OPUS_5_5, co_that, mt)


def test_bi_danh_va_chua_ghim__bi_chan():
    with pytest.raises(mh.CamGoiThat, match="bí danh"):
        mh.kiem_chot_that(mh.MoHinh("anthropic", "claude-opus-latest", True, "ANTHROPIC_API_KEY"), True, DU)
    with pytest.raises(mh.CamGoiThat, match="CHƯA ghim"):
        mh.kiem_chot_that(mh.GEMINI_FLASH, True, {**DU, "GEMINI_API_KEY": "k"})


def test_that_khong_chot__KHONG_nhap_sdk(monkeypatch):
    monkeypatch.delenv("FLS_CHO_GOI_API", raising=False)
    sys.modules.pop("anthropic", None)
    with pytest.raises(mh.CamGoiThat):
        mh.tao_that(mh.OPUS_5_5, co_that=True)
    assert "anthropic" not in sys.modules


def test_giao_dien_theo_ho__google_chot_truoc_roi_moi_ChuaDung(monkeypatch):
    with pytest.raises(mh.CamGoiThat):
        mh.tao_that(mh.GEMINI_FLASH, co_that=False)
    with pytest.raises(mh.ChuaDung):
        mh.tao_that(mh.MoHinh("hang-khac", "x-1", True, "X"), co_that=True)


def test_phat_lai_vang_tep__KhongCoBanGhi(tmp_path):
    with pytest.raises(mh.KhongCoBanGhi):
        mh.PhatLai(tmp_path / "khong_co.json")


def test_phat_lai_yeu_cau_la__KhongCoBanGhi(tmp_path):
    p = tmp_path / "a.json"
    p.write_text('{"luot": []}', encoding="utf-8")
    with pytest.raises(mh.KhongCoBanGhi, match="đã đổi"):
        mh.PhatLai(p).goi({"model": "m", "messages": []})
