# -*- coding: utf-8 -*-
"""`WO-367` AC-4 — fleet eval TỰ ĐỘNG đa mô hình: ma trận ứng viên OpenRouter × bể A/B (`fleet_eval_voi.py --ma-tran`).

Mọi lời gọi tới máy chủ OpenRouter GIẢ `127.0.0.1` (`tools/openrouter_gia.py`) — ⛔ mạng ngoài, ⛔ tiền. Bể A/B dựng trong
`tmp_path` từ 12 ca DỰNG (bể thật ở ngoài repo). Mỗi bài khai `mong` (Đ5).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "tools"))

from fls.agent import ghep_noi_dung as gnd  # noqa: E402
from fls.agent import mo_hinh as mh  # noqa: E402

import chay_agent_voi as cav  # noqa: E402
import fleet_eval_voi as fe  # noqa: E402
import openrouter_gia as og  # noqa: E402

OPUS, SONNET, SOL = "anthropic/claude-opus-5.5", "anthropic/claude-sonnet-5.5", "openai/gpt-6.2-sol"
MT_GIA = {"FLS_CHO_GOI_API": "1", "FLS_NHA_CUNG_CAP": "openrouter", "OPENROUTER_API_KEY": "khoa-gia-bai-thu",
          "FLS_OPENROUTER_DU_LIEU_XAC_NHAN": "1"}


@pytest.fixture
def be(tmp_path):
    """Bể A/B trong tmp: cùng 12 ca dựng (đủ để đo ĐƯỜNG ỐNG ma trận)."""
    for c in ("a", "b"):
        (tmp_path / "be" / c).mkdir(parents=True)
        shutil.copy(cav.CA_DUNG, tmp_path / "be" / c / "ca.json")
        shutil.copy(cav.DAP_AN_DUNG, tmp_path / "be" / c / "dap_an.json")
    return tmp_path / "be"


@pytest.fixture
def ra_tmp(tmp_path, monkeypatch):
    monkeypatch.setattr(fe, "TM_VONG", tmp_path / "vong")
    monkeypatch.setattr(fe, "TEP_MT_MD", tmp_path / "vong" / "MA_TRAN_OPENROUTER.md")
    monkeypatch.setattr(fe, "TEP_MT_JSON", tmp_path / "vong" / "MA_TRAN_OPENROUTER.json")
    return tmp_path / "vong"


def _a(**kw):
    d = dict(ung_vien="", tran_usd=2.0, tran_usd_mo_hinh=None, that=False, ghi=False)
    d.update(kw)
    return argparse.Namespace(**d)


def _dung_ncc(goc, tran=5.0, tran_mh=None):
    def f(slug, nk):
        return mh.OpenRouterChat(mh.mo_hinh_openrouter(slug), True, tran_usd=tran, tran_usd_mo_hinh=tran_mh, nhat_ky=nk,
                                 moi_truong=dict(MT_GIA), goc_api=goc, thay_cho="claude-opus-5-5", ngu=lambda s: None)
    return f


def test_AC4_luot_GIA_TRON_ma_tran__3_ung_vien_x_be_A_B__DAT_va_report_MOT_trang(be, ra_tmp, monkeypatch, capsys):
    monkeypatch.setenv(fe.BIEN_BE, str(be))
    assert fe.main(["--ma-tran", "--ung-vien", f"{OPUS},{SONNET},{SOL}", "--ghi"]) == 0
    kq = json.loads((ra_tmp / "MA_TRAN_OPENROUTER.json").read_text(encoding="utf-8"))
    assert kq["che_do"] == "gia" and set(kq["o"]) == {OPUS, SONNET, SOL}
    assert all(set(c) == {"a", "b"} for c in kq["o"].values())                  # 3 × 2 = 6 ô
    for c in kq["o"].values():
        for x in c.values():
            assert x["so_goi"] == 2 and x["mau_so_chinh"] == 12 and x["phai_nguoi_bi_noi"] == 0 and "loi" not in x
    md = (ra_tmp / "MA_TRAN_OPENROUTER.md").read_text(encoding="utf-8")
    assert "**KẾT: ĐẠT**" in md and md.count(f"| `{SOL}` |") == 2 and "GIẢ (máy chủ 127.0.0.1" in md
    assert "THẬT (usage.cost" not in md                     # số máy chủ giả ⛔ mang nhãn THẬT
    assert kq["nhat_ky"]["so_goi"] == 12
    assert not list((GOC / "docs/ITL/06_Agent/nhat_ky").glob("*fleet_ma_tran*"))     # GIẢ ⛔ ghi nhật ký tiền thật


def test_AC4_be_vang__chi_be_dung_KHAI_ro(ra_tmp, monkeypatch):
    monkeypatch.delenv(fe.BIEN_BE, raising=False)
    assert fe.main(["--ma-tran", "--ghi"]) == 0
    md = (ra_tmp / "MA_TRAN_OPENROUTER.md").read_text(encoding="utf-8")
    assert "bể giữ riêng A/B VẮNG" in md and "| `dung` |" in md


def test_AC4_so_nguoc_ban_truoc(be, ra_tmp, monkeypatch):
    monkeypatch.setenv(fe.BIEN_BE, str(be))
    assert fe.main(["--ma-tran", "--ung-vien", OPUS, "--ghi"]) == 0
    assert fe.main(["--ma-tran", "--ung-vien", f"{OPUS},{SONNET}", "--ghi"]) == 0
    md = (ra_tmp / "MA_TRAN_OPENROUTER.md").read_text(encoding="utf-8")
    assert "1.9167 → 1.9167" in md and f"| `{SONNET}` | `a` | MỚI |" in md


def test_AC4_chi_doi_MO_HINH__cham_bang_MA_doc_lap(be):
    """Ô khác nhau CHỈ ở mô hình: luật của SONNET bị phá (nối mọi ca) ⇒ chỉ hàng SONNET đổi; chấm = MÃ ↔ đáp án."""
    be_ds = {c: (json.loads((be / c / "ca.json").read_text()), json.loads((be / c / "dap_an.json").read_text()))
             for c in ("a", "b")}
    tt = og.TrangThai(luat_theo_slug={SONNET: {"ung_vien_ghep": _noi_het}})
    with og.may_chu_gia(tt) as (goc, _):
        nk: list = []
        o = fe.chay_ma_tran([OPUS, SONNET], be_ds, _dung_ncc(goc), nk)
    assert o[OPUS]["a"]["phai_nguoi_bi_noi"] == 0 and o[SONNET]["a"]["phai_nguoi_bi_noi"] > 0
    assert fe.ket_ma_tran(o)[0] is False and any("phải-để-người" in x and SONNET in x for x in fe.ket_ma_tran(o)[1])
    # yêu cầu gửi đi giống nhau trừ `model` (cùng ca · cùng skill · cùng che)
    goi = [y["than"] for y in tt.yeu_cau if not any(m.get("role") == "tool" for m in y["than"]["messages"])]
    assert len({json.dumps({k: v for k, v in g.items() if k != "model"}, sort_keys=True) for g in goi}) == 1


def _noi_het(o: dict) -> dict:
    """Luật PHÁ: như `luat_gia_v1` nhưng ca nào để-người thì NỐI ứng viên đầu (kể cả ca phải-để-người)."""
    ra = gnd.luat_gia_v1(o)
    for k, v in list(ra.items()):
        if k.endswith(".chon") and v == gnd.DE_NGUOI:
            uv = gnd.ung_vien(o, k[len("noi:"):-len(".chon")])
            if uv:
                ra[k] = uv[0]["pm"]
    return ra


def test_AC4_tran_TONG__dung_loi_KE_va_bo_qua_co_ten(be):
    be_ds = {c: (json.loads((be / c / "ca.json").read_text()), json.loads((be / c / "dap_an.json").read_text()))
             for c in ("a", "b")}
    with og.may_chu_gia() as (goc, tt):
        o = fe.chay_ma_tran([OPUS, SONNET], be_ds, _dung_ncc(goc, tran=1e-9), [])
    assert o[OPUS]["a"]["loi"].startswith("VuotTran") and "trần TỔNG" in o[OPUS]["a"]["loi"]
    assert "bo_qua" in o[OPUS]["b"] and "bo_qua" in o[SONNET]["a"] and "bo_qua" in o[SONNET]["b"]
    assert len(tt.yeu_cau) == 1                                   # lời 1 lọt (trần chặn lời KẾ — AG2-R1-03), rồi DỪNG


def test_AC4_tran_MO_HINH__chi_dung_mo_hinh_ay(be):
    be_ds = {c: (json.loads((be / c / "ca.json").read_text()), json.loads((be / c / "dap_an.json").read_text()))
             for c in ("a", "b")}
    with og.may_chu_gia() as (goc, tt):
        o = fe.chay_ma_tran([OPUS, SONNET], be_ds, _dung_ncc(goc, tran=5.0, tran_mh=1e-9), [])
    assert "trần MÔ HÌNH" in o[OPUS]["a"]["loi"] and "bo_qua" in o[OPUS]["b"]
    assert "trần MÔ HÌNH" in o[SONNET]["a"]["loi"]               # trần riêng áp cho TỪNG mô hình
    assert len(tt.yeu_cau) == 2


def test_AC4_LoiApi_mot_o__o_khac_van_chay(be):
    be_ds = {c: (json.loads((be / c / "ca.json").read_text()), json.loads((be / c / "dap_an.json").read_text()))
             for c in ("a", "b")}
    tt = og.TrangThai(loi_lan_toi=[(402, {"error": {"code": 402}})])
    with og.may_chu_gia(tt) as (goc, _):
        o = fe.chay_ma_tran([OPUS, SONNET], be_ds, _dung_ncc(goc), [])
    assert "HẾT CREDIT" in o[OPUS]["a"]["loi"] and "noi_sai" in o[OPUS]["b"] and "noi_sai" in o[SONNET]["b"]


def test_AC4_THAT_thieu_chot__moi_o_DO_co_ten__0_loi_goi(be, ra_tmp, monkeypatch):
    monkeypatch.setenv(fe.BIEN_BE, str(be))
    for k, v in MT_GIA.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("FLS_OPENROUTER_DU_LIEU_XAC_NHAN")
    with og.may_chu_gia() as (goc, tt):
        assert fe.main_ma_tran(_a(that=True), goc_api=goc) == 1
    assert len(tt.yeu_cau) == 0
    monkeypatch.setenv("FLS_NHA_CUNG_CAP", "google-cloud")
    assert fe.main_ma_tran(_a(that=True)) == 2


def test_AC4_ung_vien_cam__exit_2():
    for s in ("google/gemini-3-pro", "~anthropic/claude-opus-latest", "anthropic/claude-opus-9"):
        assert fe.main(["--ma-tran", "--ung-vien", s]) == 2


def test_AC4_THAT_nhat_ky_tren_MOI_loi_thoat(be, ra_tmp, monkeypatch, tmp_path):
    """`AG3-R1-01`: trả về bình thường · ô lỗi · ngoại lệ CHƯA lường ⇒ đều để lại nhật ký (chuyển hướng tmp bởi conftest)."""
    monkeypatch.setenv(fe.BIEN_BE, str(be))
    for k, v in MT_GIA.items():
        monkeypatch.setenv(k, v)
    tm = tmp_path / "nhat_ky"
    with og.may_chu_gia() as (goc, tt):
        assert fe.main_ma_tran(_a(that=True, ung_vien=OPUS), goc_api=goc) == 0
        assert len(list(tm.glob("*fleet_ma_tran_openrouter.json"))) == 1
        tt.loi_lan_toi = [(429, {"error": {"code": 429}})] * 5
        assert fe.main_ma_tran(_a(that=True, ung_vien=OPUS), goc_api=goc) == 1
        that = fe.chay_ma_tran

        def no_giua(uv, be_ds, dung, nk):
            dung(uv[0], nk).goi({"model": "claude-opus-5-5", "max_tokens": 8, "messages": [{"role": "user", "content": "x"}]})
            raise KeyError("lỗi chưa lường")
        monkeypatch.setattr(fe, "chay_ma_tran", no_giua)
        with pytest.raises(KeyError):
            fe.main_ma_tran(_a(that=True, ung_vien=OPUS), goc_api=goc)
        monkeypatch.setattr(fe, "chay_ma_tran", that)
    tep = sorted(tm.glob("*fleet_ma_tran_openrouter.json"))
    assert len(tep) == 3, tep                          # OR-02: 3 lượt (kể cả cùng giây) ⇒ 3 tệp, ⛔ ghi đè
    d = [json.loads(p.read_text(encoding="utf-8")) for p in tep]
    assert any("KeyError" in (x.get("loi") or "") for x in d)
    for x in d:
        assert "khoa-gia-bai-thu" not in json.dumps(x)
