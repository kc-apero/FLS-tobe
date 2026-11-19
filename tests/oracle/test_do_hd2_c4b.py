"""H10 — `tools/do_hd2.py --goi WP-C4b`: AL.PLT GI **MỌI vendor theo mã 'cách tính'** ↔ MID3 từng ô
*(ISP 3.1.2 · Step 28 · `WO-216`)*.

Chuỗi: IX.VEN ĐỌC TỪ KHO test + ảnh CFA1 GI *(PD 504 — O/P TỪNG dòng Vendor × tháng × No)* + ảnh MID1
cột T *(PD 505 — PE theo CDT1, THƯỢNG NGUỒN: công thức `E` chỉ đọc Looker + VNM)* →
`chia_theo_cach_tinh` → `ks_al` → so (vendor, tháng) × 14 cột với `gi_mid3.json`. ⛔ MID2/MID3 làm đầu vào.

  · **AC-3** mẫu số khai TRƯỚC *(`MongC4b`, Đ4)*: 209 = 165 đặc biệt + 44 thường · 1.981 ô so ·
    945 ô ⛔ so được *(P chữ)* · **988 ô ≠ 0** *(tập KHÔNG rỗng — chứng minh RATE trên số thật)* · bỏ qua 0.
  · **AC-4** KS.AL đo 209 Vendor-tháng, 165 đặc biệt.
  · **AC-5** `H9-R1-05`: đổi GIÁ TRỊ một ô vendor đặc biệt ⇒ ĐỎ *(H9 chỉ đếm)*.
  · **AC-6** ⛔ vòng tròn: đột biến MỘT ô MID1 ⇒ ĐÚNG các ô PE_cdt của Vendor-tháng ấy ĐỎ.
"""
from __future__ import annotations

import copy
import dataclasses
import pathlib
import sys
from decimal import Decimal

import psycopg
import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.bao_cao import phan_bo as pb  # noqa: E402
from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2  # noqa: E402

pytestmark = pytest.mark.pg


@pytest.fixture(scope="module")
def ven():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_ven(c, str(GOC / "tests/fixture/cau_hinh/ix_ven.json"),
                       duong_cdt1=str(GOC / "tests/fixture/cau_hinh/cdt_correct.json"),
                       actor="bo-test-h10-c4b")
        return chc.doc_ven(c, so="GI")


@pytest.fixture(scope="module")
def anh():
    return (do_hd2.nap_anh(do_hd2.ANH_CFA1_GI), do_hd2.nap_anh(do_hd2.ANH_MID1),
            do_hd2.nap_anh(do_hd2.ANH_MID3))


def _chay(ven, cfa1, mid1, mid3, **mong):
    return do_hd2.so_sanh_c4b(cfa1, mid1, mid3, ven, dataclasses.replace(do_hd2.MongC4b(), **mong))


def _vm_dac_biet_co_tien(ven, cfa1):
    """Vendor-tháng ĐẶC BIỆT đầu tiên có O ≠ 0 *(chọn bằng DỮ LIỆU — ⛔ gõ tên vendor)*."""
    dac = {v for v, ns in pb.nhan_vendor(ven).items() if ns - {pb.NHAN_THUONG}}
    return next((do_hd2._chu(r["vendor"]), r["thang"]) for r in cfa1["dong"]
                if do_hd2._chu(r["vendor"]) in dac and Decimal(r["pe"]) != 0)


def test_H10_B3_WP_C4b_anh_that_DAT_mau_so_co_nhan(ven, anh):
    tq = _chay(ven, *anh)
    h = tq.hd2_cong
    assert tq.phan_xu.dat, tq.phan_xu.ly_do
    assert (h["vm"], h["vm_dac_biet"], h["vm_thuong"]) == (209, 165, 44)
    assert (h["o_so"], h["o_khong_so"], h["o_khac_0"], h["o_khac_0_dac_biet"]) == (1981, 945, 988, 988)
    assert (h["lech"], h["bo_qua"], h["ks_al_vm"], h["ks_al_dac_biet"]) == (0, 0, 209, 165)
    assert (h["muon"], h["muon_o_khac_0"], h["theo_tong_thang"]) == (11, 0, 0)


@pytest.mark.parametrize("ten,lech", [(t, d) for t in ("vm", "vm_dac_biet", "o_so", "o_khong_so",
                                                       "o_khac_0", "lech", "ks_al_dac_biet", "bo_qua",
                                                       "muon", "muon_o_khac_0", "mid1_pe_rong")
                                      for d in (-1, 1)])
def test_D5_mong_KHAC_thi_DO_ca_hai_chieu(ven, anh, ten, lech):
    tq = _chay(ven, *anh, **{ten: getattr(do_hd2.MongC4b(), ten) + lech})
    assert not tq.phan_xu.dat and any(x.startswith(f"{ten}: đo ") for x in tq.phan_xu.ly_do)


def test_AC6_dot_bien_MOT_o_MID1_chi_DUNG_vendor_thang_ay_DO(ven, anh):
    cfa1, mid1, mid3 = anh
    v, t = _vm_dac_biet_co_tien(ven, cfa1)
    m = copy.deepcopy(mid1)
    r = next(r for r in m["dong"] if do_hd2._chu(r["vendor"]) == v and r["thang"] == t
             and do_hd2._chu(r["cdt1"]).startswith("CVL") and r["pe"] not in (None, "0"))
    r["pe"] = str(Decimal(r["pe"]) * 3)
    tq = _chay(ven, cfa1, m, mid3)
    assert not tq.phan_xu.dat
    o = {(x["vendor"], x["thang"], x["cot"]) for x in tq.lech}
    assert o and {(a, b) for a, b, _ in o} == {(v, t)}           # ĐÚNG Vendor-tháng ấy
    assert all(c.endswith("_pe") and c != "pe" for _, _, c in o) and (v, t, "cvl_pe") in o


def test_H9_R1_05_doi_GIA_TRI_o_vendor_dac_biet_o_CFA1_thi_DO(ven, anh):
    cfa1, mid1, mid3 = anh
    v, t = _vm_dac_biet_co_tien(ven, cfa1)
    c = copy.deepcopy(cfa1)
    r = next(r for r in c["dong"] if do_hd2._chu(r["vendor"]) == v and r["thang"] == t)
    r["pe"] = str(Decimal(r["pe"]) + 1)
    tq = _chay(ven, c, mid1, mid3)
    assert not tq.phan_xu.dat and (v, t, "pe") in {(x["vendor"], x["thang"], x["cot"]) for x in tq.lech}


def test_AC6_khong_vong_tron_xoa_dap_an_MID3_engine_Y_NGUYEN(ven, anh):
    cfa1, mid1, mid3 = anh
    goc = _chay(ven, *anh)
    m = copy.deepcopy(mid3)
    for r in m["dong"]:
        for k in r:
            if k == "pe" or k.endswith(("_pe", "_pm")) or k == "pm":
                r[k] = "0"
    tq = _chay(ven, cfa1, mid1, m)
    assert len(tq.lech) == goc.hd2_cong["o_khac_0"]             # mọi ô ≠ 0 của engine đứng NGUYÊN


def test_D5_luat_muon_RATE_bong_co_tien_thi_DO_co_ten(ven, anh):
    """Chiều thứ hai của `muon_o_khac_0 = 0`: dòng mượn RATE bỗng có O ≠ 0 ⇒ ĐỎ, buộc khai lại."""
    cfa1, mid1, mid3 = anh
    assert _chay(ven, *anh).hd2_cong["muon"] == 11
    c = copy.deepcopy(cfa1)
    # dòng mượn = dòng có O = 0 của vendor mang mã mượn — chọn bằng `ma_cach_tinh` (⛔ tên)
    ma = pb.ma_cach_tinh(ven)
    v_muon = {v for v, (_, b) in ma.items() if b is not None}
    r = next(r for r in c["dong"] if do_hd2._chu(r["vendor"]) in v_muon and Decimal(r["pe"]) == 0)
    r["pe"] = "5"
    tq = _chay(ven, c, mid1, mid3)
    assert not tq.phan_xu.dat
    assert any(x.startswith("muon_o_khac_0: đo 1 ≠ mong 0") for x in tq.phan_xu.ly_do)


def test_PHA_NGUON_bo_luat_muon_khoi_config_thi_cong_DO(ven, anh, monkeypatch):
    bang = {m: (k, None) for m, (k, _) in pb.CACH_TINH.items()}
    monkeypatch.setattr(pb, "CACH_TINH", bang)
    monkeypatch.setattr(pb.chia_theo_cach_tinh, "__kwdefaults__", {"bang": bang})
    tq = _chay(ven, *anh)
    assert not tq.phan_xu.dat and "muon: đo 0 ≠ mong 11" in tq.phan_xu.ly_do


def test_kho_CHUA_khai_IX_VEN_thi_DO_co_ten():
    tq = do_hd2.chay_wp_c4b("postgresql://fls:fls@localhost:1/khong_co")
    assert not tq.phan_xu.dat and tq.phan_xu.ly_do[0].startswith("IX.VEN ⛔ đọc được từ kho")


def test_MID1_mat_dong_cua_vendor_thang_co_tien_thi_DO_co_ten(ven, anh):
    cfa1, mid1, mid3 = anh
    v, t = _vm_dac_biet_co_tien(ven, cfa1)
    m = copy.deepcopy(mid1)
    m["dong"] = [r for r in m["dong"] if not (do_hd2._chu(r["vendor"]) == v and r["thang"] == t)]
    tq = _chay(ven, cfa1, m, mid3)
    assert not tq.phan_xu.dat and "Σ PE = 0 mà O =" in tq.phan_xu.ly_do[-1]


def test_CG2_H10_R2_01_khoi_WP_C4b_khai_tong_o_va_khop_theo_hop_dong_H4(ven, anh):
    """Đ4: `tong_o` = ô SO ĐƯỢC (1.981, ⛔ tính 945 ô P chữ) · `khop` = ô so khớp = `o_so − lech`."""
    h = _chay(ven, *anh).hd2_cong
    assert (h["tong_o"], h["khop"]) == (1981, 1981) and h["tong_o"] == h["o_so"]
    assert type(h["tong_o"]) is int and type(h["khop"]) is int


def test_CG2_H10_R2_01_khop_giam_dung_so_o_lech(ven, anh):
    """Đột biến MỘT ô đáp án MID3 (⛔ đầu vào: một ô CFA1 lan ra 6 ô PE) ⇒ `khop = tong_o − 1`."""
    cfa1, mid1, mid3 = anh
    v, t = _vm_dac_biet_co_tien(ven, cfa1)
    m = copy.deepcopy(mid3)
    r = next(r for r in m["dong"] if do_hd2._chu(r.get("vendor")) == v and r.get("thang") == t)
    r["cvl_pe"] = str(Decimal(r["cvl_pe"] or 0) + 1)
    h = _chay(ven, cfa1, mid1, m).hd2_cong
    assert (h["lech"], h["tong_o"], h["khop"]) == (1, 1981, 1980)
