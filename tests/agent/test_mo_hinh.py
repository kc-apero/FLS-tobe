# -*- coding: utf-8 -*-
"""WO-329 AC-3 — gọi API THẬT chỉ khi đủ chốt; mặc định PHÁT LẠI; ⛔ bí danh; giao diện ⛔ cứng một hãng."""
from __future__ import annotations

import sys

import pytest

from fls.agent import mo_hinh as mh

#: + `FLS_ZDR_DA_BAT` (vòng sửa sau KQ-331, AG-R1-11): chốt thứ năm khi chế độ che `mo` — "đủ chốt" nay gồm nó.
#: + `FLS_NHA_CUNG_CAP=anthropic` (`WO-359`): mặc định nay là đường `google-cloud` ⇒ bài đường KHOÁ phải chọn RÕ đường.
DU = {"FLS_CHO_GOI_API": "1", "ANTHROPIC_API_KEY": "khoa-gia-de-thu", "FLS_ZDR_DA_BAT": "1", "FLS_NHA_CUNG_CAP": "anthropic"}


def test_du_chot__khong_nem():
    mh.kiem_chot_that(mh.OPUS_5_5, True, DU)


@pytest.mark.parametrize("co_that,mt,chu", [
    (False, DU, "--that"),
    (True, {"FLS_NHA_CUNG_CAP": "anthropic", "ANTHROPIC_API_KEY": "k"}, "FLS_CHO_GOI_API"),
    (True, {"FLS_NHA_CUNG_CAP": "anthropic", "FLS_CHO_GOI_API": "0", "ANTHROPIC_API_KEY": "k"}, "FLS_CHO_GOI_API"),
    (True, {"FLS_NHA_CUNG_CAP": "anthropic", "FLS_CHO_GOI_API": "1"}, "ANTHROPIC_API_KEY"),
])
def test_thieu_mot_chot__CamGoiThat(co_that, mt, chu):
    with pytest.raises(mh.CamGoiThat, match=chu):
        mh.kiem_chot_that(mh.OPUS_5_5, co_that, mt)


def test_AG_R1_11_che_do_mo_thieu_ZDR__CamGoiThat__che_het_KHONG_doi():
    """Quyết chủ 23/11: `mo` gửi nguyên văn tên · số TK ⇒ đi KÈM ZDR — nay là chốt trong mã (bia AG-R1-11)."""
    khong_zdr = {k: v for k, v in DU.items() if k != "FLS_ZDR_DA_BAT"}
    with pytest.raises(mh.CamGoiThat, match="FLS_ZDR_DA_BAT"):
        mh.kiem_chot_that(mh.OPUS_5_5, True, khong_zdr)                       # mặc định = `mo`
    with pytest.raises(mh.CamGoiThat, match="FLS_ZDR_DA_BAT"):
        mh.kiem_chot_that(mh.OPUS_5_5, True, {**khong_zdr, "FLS_ZDR_DA_BAT": "0"}, che_do="mo")
    mh.kiem_chot_that(mh.OPUS_5_5, True, khong_zdr, che_do="che_het")
    mh.kiem_chot_that(mh.OPUS_5_5, True, khong_zdr, che_do="che_noi_dung")


def test_bi_danh_va_chua_ghim__bi_chan():
    with pytest.raises(mh.CamGoiThat, match="bí danh"):
        mh.kiem_chot_that(mh.MoHinh("anthropic", "claude-opus-latest", True, "ANTHROPIC_API_KEY"), True, DU)
    with pytest.raises(mh.CamGoiThat, match="CHƯA ghim"):
        mh.kiem_chot_that(mh.MoHinh("anthropic", "claude-ten-tam", False, "ANTHROPIC_API_KEY"), True, DU)


def test_that_khong_chot__KHONG_nhap_sdk(monkeypatch):
    monkeypatch.delenv("FLS_CHO_GOI_API", raising=False)
    sys.modules.pop("anthropic", None)
    with pytest.raises(mh.CamGoiThat):
        mh.tao_that(mh.OPUS_5_5, co_that=True)
    assert "anthropic" not in sys.modules


def test_WO355_giao_dien_theo_ho__openai_chua_cho__chot_truoc_roi_moi_ChuaDung(monkeypatch):
    """Chủ 23/11: giai đoạn sau dùng OpenAI ⇒ họ `openai` CHỪA CHỖ: chốt chạy trước, rồi `ChuaDung` (⛔ adapter)."""
    oa = mh.MoHinh("openai", "gpt-x-ghim", True, "OPENAI_API_KEY")
    with pytest.raises(mh.CamGoiThat):
        mh.tao_that(oa, co_that=False)
    for k, v in {**DU, "OPENAI_API_KEY": "k"}.items():
        monkeypatch.setenv(k, v)
    with pytest.raises(mh.ChuaDung, match="CHỪA CHỖ"):
        mh.tao_that(oa, co_that=True)
    with pytest.raises(mh.ChuaDung):
        mh.tao_that(mh.MoHinh("hang-khac", "x-1", True, "X"), co_that=True)


def test_WO355_khong_con_ho_google__chi_anthropic_ghim():
    """Chủ 23/11: *"không dùng gemini nữa"* — ⛔ hằng, ⛔ adapter, ⛔ nguồn thật họ google."""
    from fls.agent import chuoi as ch
    from fls.agent import report as rp
    assert not hasattr(mh, "GEMINI_FLASH") and not hasattr(mh, "GoogleChuaDung")
    assert set(mh.ADAPTER) == set(mh.HO_CO_ADAPTER) == {"anthropic"} and mh.HO_DE_DANH == ("openai",)
    assert rp.NGUON_THAT[0] == "anthropic" and "google" not in rp.NGUON_THAT     # OR-01: + tên adapter Vertex/GC/OpenRouter
    assert (mh.OPUS_5_5.ma, mh.SONNET_5_5.ma) == ("claude-opus-5-5", "claude-sonnet-5-5")
    for m in (mh.OPUS_5_5, mh.SONNET_5_5):
        assert m.ghim and m.loi_ghim() is None and m.ma in mh.BANG_GIA
    assert {a.mo_hinh.ho for a in ch.AGENT} == {"anthropic"}


def test_phat_lai_vang_tep__KhongCoBanGhi(tmp_path):
    with pytest.raises(mh.KhongCoBanGhi):
        mh.PhatLai(tmp_path / "khong_co.json")


def test_phat_lai_yeu_cau_la__KhongCoBanGhi(tmp_path):
    p = tmp_path / "a.json"
    p.write_text('{"luot": []}', encoding="utf-8")
    with pytest.raises(mh.KhongCoBanGhi, match="đã đổi"):
        mh.PhatLai(p).goi({"model": "m", "messages": []})
