"""WO-226 — alias nhãn HD `ITE | ITE Interest` → nút `ITE` *(ISP 3.1.2 · phương án A của chủ 19/11)*.

  · AC-1 — alias là CẤU HÌNH `hd_cfg.ALIAS_NHAN_HD` *(⛔ `if` theo nhãn trong engine)*; so khớp sau `strip()`.
  · AC-2 — `hd_ngoai_cay` 162 → 9; 153 dòng ITE vào nút `ITE` *(Đ4: đếm DÒNG)*.
  · AC-3 — ô lệch 409/410 do alias khai `mong` CÓ TÊN *(Đ5 hai chiều)*; ô khác khớp 100 %; `tong_o == khop`.
"""
from __future__ import annotations

import copy
import json
import pathlib
import sys
from datetime import date
from decimal import Decimal as D

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.bao_cao.cfa import DongCFA, cfa1_daily  # noqa: E402
from fls.cau_hinh import hd as hd_cfg  # noqa: E402
from fls.cau_hinh import ky  # noqa: E402
from tools import do_hd2  # noqa: E402

LICH = ky.LichKy(nguon="bai-test-wo226", ngay_dau=date(2024, 10, 21), luat=ky.LUAT_A)
NGAY = 45700
KHOI = ("GROUP", "SGO2")


@pytest.fixture(scope="module")
def cay():
    return do_hd2.nap_cay()


def _dong(nhan, no="2"):
    return DongCFA(ngay=NGAY, le="SGO2", hd=nhan, musd_no=D(no), musd_co=D(0))


def _o_ite(kq):
    return kq.o[("GROUP", "ITE", NGAY)]


# ── AC-1 · engine ────────────────────────────────────────────────────────────────

def test_AC1_engine_khong_nhet_nhan_ITE_Đ1():
    """⛔ `if` theo nhãn trong engine: 0 lần `ITE Interest` ở `cfa.py`; tệp ⛔ rỗng (Đ3)."""
    van = (GOC / "fls/bao_cao/cfa.py").read_text(encoding="utf-8")
    assert len(van) > 5000 and van.count("ITE Interest") == 0
    assert hd_cfg.ALIAS_NHAN_HD == {"ITE | ITE Interest": "ITE"}


def test_AC1_khong_alias_thi_ngoai_cay_co_alias_thi_vao_nut(cay):
    d = [_dong("ITE | ITE Interest")]
    kq0 = cfa1_daily(d, cay, [NGAY], KHOI)
    assert kq0.dong_ngoai_cay == [0] and _o_ite(kq0) == 0
    kq = cfa1_daily(d, cay, [NGAY], KHOI, alias=hd_cfg.ALIAS_NHAN_HD)
    assert kq.dong_ngoai_cay == [] and kq.dong_alias == [0] and _o_ite(kq) == D(2)
    assert kq.o[("SGO2", "ITE", NGAY)] == D(2)


@pytest.mark.parametrize("nhan", ["ITE | ITE Interest ", " ITE | ITE Interest", "  ITE | ITE Interest  "])
def test_AC1_chuan_hoa_khoang_trang_hai_dau(cay, nhan):
    kq = cfa1_daily([_dong(nhan)], cay, [NGAY], KHOI, alias=hd_cfg.ALIAS_NHAN_HD)
    assert kq.dong_ngoai_cay == [] and _o_ite(kq) == D(2)


@pytest.mark.parametrize("nhan", ["ITE | ITE  Interest", "ITE|ITE Interest", "Server Cost", "GAC - Other", None])
def test_AC1_nhan_khac_GIU_ngoai_cay(cay, nhan):
    kq = cfa1_daily([_dong(nhan)], cay, [NGAY], KHOI, alias=hd_cfg.ALIAS_NHAN_HD)
    assert kq.dong_ngoai_cay == [0] and kq.dong_alias == []


def test_AC1_alias_tro_ma_khong_co_trong_cay_thi_NO(cay):
    with pytest.raises(ValueError, match="mã đích"):
        cfa1_daily([], cay, [NGAY], KHOI, alias={"x": "KHONG_CO"})


# ── AC-2/AC-3 · ảnh thật ─────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def nguon():
    return (do_hd2.nap_anh(do_hd2.ANH_GL_CF), do_hd2.nap_fx(), do_hd2.nap_cay())


@pytest.fixture(scope="module")
def tq_a(nguon):
    vao, fx, cay = nguon
    return do_hd2.so_sanh_c3a(vao, do_hd2.nap_anh(do_hd2.ANH_CFA1), fx, cay, LICH,
                              do_hd2.mong_c3a_mac_dinh())


@pytest.fixture(scope="module")
def tq_b(nguon):
    vao, fx, cay = nguon
    return do_hd2.so_sanh_c3b(vao, do_hd2.nap_anh(do_hd2.ANH_YHQM), fx, cay, LICH,
                              do_hd2.mong_c3b_mac_dinh())


@pytest.mark.parametrize("tq", ["tq_a", "tq_b"])
def test_AC2_hd_ngoai_cay_162_thanh_9_va_153_dong_ITE(tq, request):
    t = request.getfixturevalue(tq)
    ct = t.lech_co_ten
    assert ct["hd_ngoai_cay"] == {"Server Cost": 7, "GAC - Other": 1, "<rỗng>": 1}
    assert sum(ct["hd_ngoai_cay"].values()) == 9
    assert ct["hd_alias"] == {"ITE | ITE Interest": 152, "ITE | ITE Interest ": 1}
    assert sum(ct["hd_alias"].values()) == 153
    assert t.phan_xu.dat, t.phan_xu.ly_do


@pytest.mark.parametrize("tq", ["tq_a", "tq_b"])
def test_AC3_lech_co_chu_dich_khai_ten_va_o_khac_khop_100(tq, request):
    t = request.getfixturevalue(tq)
    li = t.hd2_cong["lech_co_chu_dich_ite"]
    assert li["so_o"] == len(t.lech_ite) > 0                      # Đ3: tập ⛔ rỗng
    assert li["ma"] == ["ITE"] and li["theo_khoi"]["GROUP"] > 0
    assert t.lech == [] and t.hd2_cong["lech_ngoai_ten"] == 0     # ô khác khớp 100 %
    assert t.khop + len(t.lech_ite) == t.tong_o                   # KQ-231: khop = khớp đáp án THẬT
    h = t.hd2_cong
    assert h["khop"] == t.tong_o - li["so_o"] and "khop_dap_an" not in h
    assert h["lech_co_chu_dich"] == h["mong_lech_co_chu_dich"] == li["so_o"]
    # mọi ô lệch có chủ đích: lệch thật (≠ đáp án), ⛔ ô khớp bị gán nhầm
    assert all(D(x["lech"]) != 0 and x["ma"] == "ITE" for x in t.lech_ite)


def test_AC3_C3a_khai_so_o_ngay_tong_musd(tq_a):
    li = tq_a.hd2_cong["lech_co_chu_dich_ite"]
    assert (li["so_o"], li["so_cot_ngay"]) == (35, 26)
    assert (li["ngay_dau"], li["ngay_cuoi"]) == ("2025-02-24", "2026-10-31")
    # Đ4: Σ khối GROUP = lãi ITE ròng WO-226 ≈ 0,01197 mUSD; Σ mọi khối cộng cả khối LE
    assert abs(D(li["tong_musd_group"]) - D("0.01197")) < D("1e-5")
    assert li["theo_khoi"] == {"BGO2": 1, "GROUP": 26, "SGO2": 8}


def test_AC3_C3b_khai_so_o_ky_tong_musd(tq_b):
    li = tq_b.hd2_cong["lech_co_chu_dich_ite"]
    assert (li["so_o"], li["so_ky"], li["ky_dau"], li["ky_cuoi"]) == (42, 24, "2025", "2026Q4")
    # Σ ô C3b = 4 cấp kỳ chồng (Y·H·Q·M) × Σ C3a — Đ4 ghi trong MONG
    assert abs(D(li["tong_musd_group"]) - 4 * D("0.011973111599")) < D("1e-9")


# ── Đ5 · hai chiều ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("sua", [{"so_o": 34}, {"so_o": 36}, {"ngay_cuoi": "2026-10-30"},
                                 {"tong_musd_group": "0.011973111600"}, {"ma": ["ITE", "X"]}])
def test_D5_mong_ite_C3a_khac_thi_DO(nguon, sua):
    vao, fx, cay = nguon
    m = do_hd2.mong_c3a_mac_dinh()
    m = type(m)(**{**m.__dict__, "lech_ite": {**do_hd2.MONG_LECH_ITE_C3A, **sua}})
    tq = do_hd2.so_sanh_c3a(vao, do_hd2.nap_anh(do_hd2.ANH_CFA1), fx, cay, LICH, m)
    assert not tq.phan_xu.dat and any("lech_co_chu_dich_ite" in s for s in tq.phan_xu.ly_do)


@pytest.mark.parametrize("sua", [{"so_o": 41}, {"so_o": 43}, {"ky_dau": "2024"}])
def test_D5_mong_ite_C3b_khac_thi_DO(nguon, sua):
    vao, fx, cay = nguon
    m = do_hd2.mong_c3b_mac_dinh()
    m = type(m)(**{**m.__dict__, "lech_ite": {**do_hd2.MONG_LECH_ITE_C3B, **sua}})
    tq = do_hd2.so_sanh_c3b(vao, do_hd2.nap_anh(do_hd2.ANH_YHQM), fx, cay, LICH, m)
    assert not tq.phan_xu.dat and any("lech_co_chu_dich_ite" in s for s in tq.phan_xu.ly_do)


def test_D5_mong_ite_vang_thi_DO(nguon):
    vao, fx, cay = nguon
    m = do_hd2.mong_c3a_mac_dinh()
    m = type(m)(**{**m.__dict__, "lech_ite": None})
    tq = do_hd2.so_sanh_c3a(vao, do_hd2.nap_anh(do_hd2.ANH_CFA1), fx, cay, LICH, m)
    assert not tq.phan_xu.dat


def test_D5_go_alias_thi_DO_ca_hai_goi(nguon, monkeypatch):
    """Gỡ bảng alias ⇒ 162 dòng ngoài cây quay lại ⇒ ĐỎ ở `hd_ngoai_cay` + `hd_alias` + ô lệch ITE = 0."""
    vao, fx, cay = nguon
    monkeypatch.setattr(hd_cfg, "ALIAS_NHAN_HD", {})
    a = do_hd2.so_sanh_c3a(vao, do_hd2.nap_anh(do_hd2.ANH_CFA1), fx, cay, LICH, do_hd2.mong_c3a_mac_dinh())
    b = do_hd2.so_sanh_c3b(vao, do_hd2.nap_anh(do_hd2.ANH_YHQM), fx, cay, LICH, do_hd2.mong_c3b_mac_dinh())
    for t in (a, b):
        assert not t.phan_xu.dat and sum(t.lech_co_ten["hd_ngoai_cay"].values()) == 162
        assert t.lech_ite == []


def test_D5_mot_o_ngoai_ite_lech_thi_DO_o_lech_ngoai_ten(nguon):
    """Ô ⛔ phải ITE mà lệch ⇒ vào `lech` (ngoài tên), ⛔ chui vào `lech_ite`."""
    vao, fx, cay = nguon
    da = copy.deepcopy(do_hd2.nap_anh(do_hd2.ANH_CFA1))
    r = next(r for r in da["dong"] if do_hd2._chu(r["le"]) == "SGO1" and do_hd2._chu(r["ma_hd"]) == "GI")
    r["gt"] = str(D(r["gt"]) + D("1e-12"))
    tq = do_hd2.so_sanh_c3a(vao, da, fx, cay, LICH, do_hd2.mong_c3a_mac_dinh())
    assert not tq.phan_xu.dat and len(tq.lech) >= 1 and len(tq.lech_ite) == 35


# ── tệp sinh ra ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("goi,mong", [("WP-C3a", do_hd2.MONG_LECH_ITE_C3A), ("WP-C3b", do_hd2.MONG_LECH_ITE_C3B)])
def test_tep_hd2_cong_khoi_khai_lech_ite_va_hop_dong_CG2(goi, mong):
    j = json.loads(do_hd2.RA_CONG.read_text(encoding="utf-8"))[goi]
    assert j["dat"] is True and j["tong_o"] == j["khop"] + j["lech_co_chu_dich"] > 0
    assert j["lech_co_chu_dich_ite"] == j["mong_lech_co_chu_dich_ite"] == mong
    assert j["lech_co_chu_dich"] == j["mong_lech_co_chu_dich"] == mong["so_o"] and j["lech_ngoai_ten"] == 0
    assert "khop_dap_an" not in j
    assert sum(j["lech_co_ten"]["hd_ngoai_cay"].values()) == 9
    assert sum(j["lech_co_ten"]["hd_alias"].values()) == 153
