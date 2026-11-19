# -*- coding: utf-8 -*-
"""`H9` — `AL.PLT` · phân bổ nền tảng GI + `KS.AL` *(ISP 3.1.2 · Step 24 · `WO-200`)*.

AC-1 `H9-B1` RATE + Σ chia = O = P · AC-2 `H9-B2` O = 0 ∧ P > 0 ⇒ tổng tháng · AC-3 lỗi CÓ TÊN ·
AC-5 đột biến MỘT ô đầu vào ⇒ ĐÚNG Vendor-tháng ấy đổi. Đầu vào TỔNG HỢP *(⛔ MID3 đáp án)*.
AC-4 `H9-B3` *(cổng WP-C4a)* — sau DT8b ở `tests/oracle/test_do_hd2_c4a.py` *(BG-201 «Sau DT8b»)*.
"""
from __future__ import annotations

import json
from decimal import Decimal as D
from pathlib import Path

import pytest

from fls.bao_cao import phan_bo as pb
from fls.cau_hinh.vendor import NHAN_RIENG, BangVen, DongVen

GOC = Path(__file__).resolve().parents[2]
C6 = ("CVL", "COR", "SHQ1", "CSM", "CAH", "ASA")
C7 = (*C6, "SHQ2")


def _ven(nhan: dict[str, list[str]]) -> BangVen:
    ds, i = [], 0
    for v, ls in nhan.items():
        for n in ls:
            i += 1
            ds.append(DongVen(i, str(i + 3), str(i), v, None, None, None, 1, 1, n))
    return BangVen("tong-hop", tuple(ds), C7, NHAN_RIENG)


VEN = _ven({"VA": ["thường"], "VB": ["thường", "thường"], "VC": ["thường"],
            "VX": ["Max", "thường"], "VD341": ["VD341"]})


def _chia(pe, o, p, ven=VEN):
    return pb.chia_nen_tang(pe, o, p, ven, cdt1=C6)


def _bo():
    pe = {("VA", "202502"): {"CVL": D(1), "COR": D(3)},
          ("VB", "202502"): {"CSM": D(2), "CAH": D(2)},
          ("VX", "202502"): {"CVL": D(10)},
          ("VD341", "202502"): {"ASA": D(5)}}
    o = {("VA", "202502"): D(100), ("VB", "202502"): D(-8),
         ("VX", "202502"): D(7), ("VD341", "202502"): D(9)}
    p = {("VA", "202502"): D(40), ("VB", "202502"): D(0),
         ("VX", "202502"): D(0), ("VD341", "202502"): D(0)}
    return pe, o, p


def test_H9_B1_rate_va_sigma_chia_bang_O_va_P():
    kq = _chia(*_bo())
    k = ("VA", "202502")
    assert kq.rate[k]["CVL"] == D("0.25") and kq.rate[k]["COR"] == D("0.75")
    assert kq.chia[k]["CVL"] == (D(25), D(10)) and kq.chia[k]["COR"] == (D(75), D(30))
    assert kq.chia[k]["ASA"] == (D(0), D(0))
    assert kq.chia[("VB", "202502")]["CSM"] == (D(-4), D(0))          # O âm vẫn chia theo RATE
    assert pb.ks_al(kq, _bo()[1], _bo()[2]) == 2                       # mẫu số: 2 Vendor-tháng


def test_H9_B3_vendor_dac_biet_bo_qua_CO_DEM_du_5_nhan_co_ten():
    kq = _chia(*_bo())
    assert set(kq.chia) == {("VA", "202502"), ("VB", "202502")}
    assert tuple(kq.bo_qua) == NHAN_RIENG and len(kq.bo_qua) == 5     # đủ 5 khoá, kể cả 0
    assert kq.bo_qua["Max"] == (("VX", "202502"),)                     # Max + thường ⇒ đặc biệt
    assert kq.bo_qua["VD341"] == (("VD341", "202502"),)
    assert kq.bo_qua["VD62"] == () and kq.bo_qua["VD428"] == ()


def test_H9_B2_O_bang_0_P_duong_chia_theo_TONG_THANG():
    pe, o, p = _bo()
    o[("VA", "202502")], p[("VA", "202502")] = D(0), D(20)
    kq = _chia(pe, o, p)
    k = ("VA", "202502")
    assert k in kq.theo_tong_thang
    # AS-IS `P×S10/O10` *(H10-R1-01)*: S10 = Σ RATE×O mọi vendor tháng ấy — CVL 7 · CSM −4 ·
    # CAH −4 · ASA 9 ; O10 = 0 − 8 + 7 + 9 = 8 ⇒ RATE tổng tháng = S10/O10, ⛔ PE/ΣPE.
    assert kq.rate[k]["CVL"] == D(7) / D(8) and kq.rate[k]["ASA"] == D(9) / D(8)
    assert kq.rate[k]["CSM"] == D(-4) / D(8)
    assert abs(sum(x[1] for x in kq.chia[k].values()) - D(20)) <= pb.TOL
    assert all(x[0] == 0 for x in kq.chia[k].values())


def test_H9_B2_O_P_bang_0_va_sigma_PE_0_thi_chia_0_khong_loi():
    pe, o, p = _bo()
    pe[("VC", "202503")], o[("VC", "202503")], p[("VC", "202503")] = {}, D(0), D(0)
    kq = _chia(pe, o, p)
    assert kq.chia[("VC", "202503")] == {c: (D(0), D(0)) for c in C6}


def test_AC3_sigma_PE_0_ma_tien_khac_0_LOI_CO_TEN():
    pe, o, p = _bo()
    pe[("VC", "202503")], o[("VC", "202503")], p[("VC", "202503")] = {"CVL": D(0)}, D(5), D(0)
    with pytest.raises(pb.LoiPhanBo, match=r"VC · 202503: Σ PE Vendor-tháng = 0"):
        _chia(pe, o, p)
    # O = 0 ∧ P > 0 mà tổng THÁNG cũng 0
    pe, o, p = {("VC", "202503"): {}}, {("VC", "202503"): D(0)}, {("VC", "202503"): D(3)}
    with pytest.raises(pb.LoiPhanBo, match=r"tổng tháng Σ O = 0"):
        _chia(pe, o, p)


def test_AC3_KS_AL_sigma_chia_khac_tien_LOI_CO_TEN_vendor_thang_lech():
    pe, o, p = _bo()
    kq = _chia(pe, o, p)
    kq.chia[("VA", "202502")]["CVL"] = (D(26), D(10))                  # PHÁ một ô chia
    with pytest.raises(pb.LoiPhanBo, match=r"KS\.AL VA · 202502 · PE: Σ chia − tiền = 1"):
        pb.ks_al(kq, o, p)
    kq.chia[("VA", "202502")]["CVL"] = (D(25), D(9))
    with pytest.raises(pb.LoiPhanBo, match=r"VA · 202502 · PM: Σ chia − tiền = -1"):
        pb.ks_al(kq, o, p)


def test_AC3_KS_AL_tap_rong_la_DO():
    pe, o, p = {("VX", "202502"): {}}, {("VX", "202502"): D(1)}, {("VX", "202502"): D(0)}
    with pytest.raises(pb.LoiPhanBo, match="0 Vendor-tháng đã chia"):
        _chia(pe, o, p)                                                 # mọi vendor đặc biệt


@pytest.mark.parametrize("pha, mau", [
    (lambda pe, o, p: o.update({("VQ", "202502"): D(1)}), "khoá lệch"),
    (lambda pe, o, p: (o.update({("VQ", "202502"): D(1)}), p.update({("VQ", "202502"): D(0)}),
                       pe.update({("VQ", "202502"): {}})), "VQ · 202502: vendor ⛔ có trong IX.VEN"),
    (lambda pe, o, p: pe[("VA", "202502")].update({"SHQ2": D(1)}), "CDT1 lạ ở PE"),
    (lambda pe, o, p: (o.clear(), p.clear(), pe.clear()), "0 Vendor-tháng"),
])
def test_AC3_dau_vao_hong_LOI_CO_TEN_khong_im(pha, mau):
    pe, o, p = _bo()
    pha(pe, o, p)
    with pytest.raises(pb.LoiPhanBo, match=mau):
        _chia(pe, o, p)


def test_AC5_dot_bien_MOT_o_dau_vao_chi_doi_DUNG_vendor_thang_ay():
    pe, o, p = _bo()
    goc = _chia(pe, o, p)
    pe[("VA", "202502")]["CVL"] = D(2)
    moi = _chia(pe, o, p)
    doi = {k for k in goc.chia if goc.chia[k] != moi.chia[k]}
    assert doi == {("VA", "202502")}, doi


# ── AC-4 `H9-B3` · WP-C4a — ghim số đo nền *(Đ3 · Đ5)*; cổng: tests/oracle/test_do_hd2_c4a.py ──

def _anh(ten):
    return json.loads((GOC / "tests" / "fixture" / ten).read_text(encoding="utf-8"))


def _chu(x):
    return x.get("chu") if isinstance(x, dict) else x


def test_H9_B3_sau_DT8b_MID3_CO_khoa_vendor_thang_209_hang():
    """Bản đầu ghim "MID3 ⛔ khoá" ⇒ ĐỎ khi DT8b thêm khoá (Đ5 cắn đúng) ⇒ khai lại: 209 có khoá."""
    m3 = _anh("dap_an/gi_mid3.json")
    assert m3["so_dong"] == 253 and "vendor" in m3["cot"] and "thang" in m3["cot"], m3["cot"]
    assert sum(r["vendor"] is not None for r in m3["dong"]) == 209
    assert [c for c in m3["cot"] if c.endswith("_pe")] == [f"{c.lower()}_pe" for c in C6]  # 6 CDT1


def test_H9_B3_CHAN_vendor_thuong_co_PE_0_tren_moi_o_MID2():
    """Vendor THUẦN `thường` theo IX.VEN = 4 mã; trên ảnh MID2 *(209 Vendor-tháng × 7 CDT1)*
    4 × 11 tháng × 7 = 308 ô PE, ô ≠ 0 = **0** ⇒ WP-C4a vendor thường đo trên tập toàn 0 (Đ3)."""
    ven, m2 = _anh("cau_hinh/ix_ven.json"), _anh("dap_an/gi_mid2.json")
    nhan: dict[str, set] = {}
    for r in ven["dong"]:
        nhan.setdefault(_chu(r["vendor"]), set()).add(_chu(r["cach_tinh"]))
    thuong = sorted(v for v, s in nhan.items() if s == {"thường"})
    assert thuong == ["VD113", "VD336", "VD58", "VD61"], thuong
    assert len([v for v, s in nhan.items() if s - {"thường"}]) == 15
    o = [r for r in m2["dong"] if _chu(r["vendor"]) in thuong]
    assert len(o) == 308 and sum(D(r["pe"]) != 0 for r in o) == 0


@pytest.mark.pg
def test_H9_IX_VEN_doc_tu_KHO_phan_loai_19_vendor_4_thuong_5_nhan():
    """IX.VEN đọc từ KHO test *(nạp ảnh DT8 như bài C9)* — ⛔ đọc tệp ảnh vào engine."""
    import psycopg
    from fls.db.kho import dsn_test
    from fls.repo import cau_hinh_repo as chc
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_ven(c, str(GOC / "tests/fixture/cau_hinh/ix_ven.json"),
                       duong_cdt1=str(GOC / "tests/fixture/cau_hinh/cdt_correct.json"),
                       actor="bo-test-h9")
        ven = chc.doc_ven(c)
    cdt = tuple(x for x in ven.cdt1 if not x.startswith("SHQ2"))
    assert len(ven.cdt1) == 7 and len(cdt) == 6                       # 7 CDT1 IX.VEN · 6 chia
    vs = sorted({d.vendor for d in ven.dong})
    pe = {(v, "202502"): {cdt[0]: D(1)} for v in vs}
    o = {(v, "202502"): D(10) for v in vs}
    p = {(v, "202502"): D(0) for v in vs}
    kq = pb.chia_nen_tang(pe, o, p, ven, cdt1=cdt)
    assert len(vs) == 19 and sorted(k[0] for k in kq.chia) == ["VD113", "VD336", "VD58", "VD61"]
    assert {n: len(x) for n, x in kq.bo_qua.items()} == \
        {"Max": 12, "VD341": 1, "VD428": 1, "VD444": 1, "VD62": 1}    # vendor-tháng / nhãn
    assert len({k for x in kq.bo_qua.values() for k in x}) == 15       # 15 vendor (VD62 ở 2 nhãn)


def test_H10_R1_01_MOT_nguon_tong_thang_ca_TONG_HOP_O_khac_sigma_PE():
    """Ca R1: VC `O = 0 · P = 60`; VA `O = 100` PE `30/10`; VB `O = 20` PE `10/30`. O ≠ Σ PE ⇒ hai
    cơ sở cũ lệch *(`PE/ΣPE` ⇒ 30/30 · `S10/O10` ⇒ 40/20)*. Hai cổng PHẢI cùng ra 40/20 *(AS-IS)*."""
    t = "202502"
    pe = {("VA", t): {"CVL": D(30), "COR": D(10)}, ("VB", t): {"CVL": D(10), "COR": D(30)},
          ("VC", t): {}}
    o = {("VA", t): D(100), ("VB", t): D(20), ("VC", t): D(0)}
    p = {("VA", t): D(0), ("VB", t): D(0), ("VC", t): D(60)}
    a = pb.chia_nen_tang(pe, o, p, VEN, cdt1=C6)
    dong = [pb.DongCFA1("VA", t, "1", D(100), D(0)), pb.DongCFA1("VB", t, "1", D(20), D(0)),
            pb.DongCFA1("VC", t, "1", D(0), D(60))]
    b = pb.chia_theo_cach_tinh(dong, pe, VEN, cdt1=C6)
    for kq in (a, b):
        assert (kq.chia[("VC", t)]["CVL"][1], kq.chia[("VC", t)]["COR"][1]) == (D(40), D(20))
    assert all(a.chia[k][c] == b.chia[k][c] for k in a.chia for c in C6)
