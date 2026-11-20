# -*- coding: utf-8 -*-
"""`H11-R1-01` (KQ-236) — luật MID3 THEO SỔ được ghim bằng **DỮ LIỆU tổng hợp**, ⛔ bằng bài chép dict `LUAT_SO`.

Mẫu số khai thẳng *(Đ3/Đ4)*: ở ảnh thật, nhóm MID1 `O = 0 ∧ P > 0` = **0** ở OMC · SC · PS và hàng `VD62`/`VD341`
= **0** ở SC · PS ⇒ 5/6 cờ ngoài GI ⛔ có dữ liệu thật kích hoạt. Cờ chỉ chứng minh được ở đây: tay tính từng
số, mỗi sổ một ca. Đột biến R1 *(`SC.pm_tong_thang=True` · `PS.pm_tong_thang=True` · `SC.muon_rate=False` ·
`PS.muon_rate=False` · `OMC.pm_tong_thang=False`)* nay ĐỎ ở bài này ngay cả khi bỏ bài ghim dict.

Luật *(BG-242 §3, `FORMULA` MID3 19/11)*: `muon_rate` GI ✓ · OMC ✗ *(tra theo `$H`)* · SC ✓ · PS ✓;
`pm_tong_thang` GI ✓ · OMC ✓ · SC ✗ · PS ✗. **Giá trị kỳ vọng ở đây GÕ TAY** *(⛔ đọc từ `LUAT_SO`)*.
"""
from __future__ import annotations

from decimal import Decimal as D

import pytest

from fls.bao_cao import phan_bo as pb
from fls.cau_hinh.vendor import (LUAT_SO, NHAN_RIENG, NHAN_THUONG, BangVen, DongVen,
                                 cach_tinh_cua_so)

C = ("CVL", "COR")
T = "202505"
CVL, COR = C

MUON_RATE = {"GI": True, "OMC": False, "SC": True, "PS": True}          # gõ tay — ⛔ LUAT_SO
PM_TONG_THANG = {"GI": True, "OMC": True, "SC": False, "PS": False}


def _ven(dong: list[tuple]) -> BangVen:
    ds = [DongVen(i, str(i + 3), no, v, None, None, None, 1, 1, ct)
          for i, (v, no, ct) in enumerate(dong, start=1)]
    return BangVen("tong-hop", tuple(ds), C, NHAN_RIENG)


def _chay(so, dong, pe, ven):
    """Đúng cách `tools/do_hd2.py::so_sanh_so_c4c` gọi engine: tham số lấy từ `LUAT_SO[so]`."""
    return pb.chia_theo_cach_tinh(dong, pe, ven, cdt1=C, bang=cach_tinh_cua_so(so),
                                  pm_tong_thang_bat=LUAT_SO[so]["pm_tong_thang"])


# ══ ca VD62 mượn RATE của VD341 *(cột `$AU` ở SC · PS · GI; `$H` ở OMC ⇒ ⛔ mượn)* ═════════════════
VEN_MUON = _ven([("VD341", "1", "VD341"), ("VD62", "1", "VD62"), ("VD62", "2", "VD62")])
# VD341 RATE .75/.25 · VD62 RATE riêng = CVL 1 · No 2 có ΣP LỚN HƠN (8 > 5) ⇒ No 2 là No mượn.
DONG_MUON = [pb.DongCFA1("VD341", T, "1", D(40), D(40)),
             pb.DongCFA1("VD62", T, "1", D(10), D(5)), pb.DongCFA1("VD62", T, "2", D(20), D(8))]
PE_MUON = {("VD341", T): {CVL: D(30), COR: D(10)}, ("VD62", T): {CVL: D(4), COR: D(0)}}


@pytest.mark.parametrize("so", ["GI", "OMC", "SC", "PS"])
def test_H11_R1_01_VD62_muon_RATE_VD341_chi_o_GI_SC_PS_OMC_khong(so):
    kq = _chay(so, DONG_MUON, PE_MUON, VEN_MUON)
    vm = kq.chia[("VD62", T)]
    if MUON_RATE[so]:
        # No 2 mượn .75/.25: PE CVL = 10 (No1 riêng) + 20×.75 = 25 · COR = 20×.25 = 5 · PM CVL = 5 + 8×.75 = 11
        assert (vm[CVL][0], vm[COR][0], vm[CVL][1]) == (D(25), D(5), D(11))
        assert kq.muon == (("VD62", T, "2", "VD341"),)
    else:
        # ⛔ mượn: cả hai No dùng RATE riêng (CVL 1) ⇒ PE CVL = 30 · COR = 0 · PM CVL = 13
        assert (vm[CVL][0], vm[COR][0], vm[CVL][1]) == (D(30), D(0), D(13))
        assert kq.muon == ()


# ══ ca `O = 0 ∧ P > 0` — PM chia theo tổng tháng `P×S10/O10` *(GI · OMC)* hay `RATE×P` *(SC · PS)* ═══
VEN_TT = _ven([("VX", "1", NHAN_THUONG), ("VX", "2", NHAN_THUONG), ("VY", "1", NHAN_THUONG),
               ("VZ", "1", NHAN_THUONG)])
# VX RATE .75/.25: No 1 O=100 P=100 · No 2 O=0 P=50 ⇐ ca `O = 0 ∧ P > 0`. VY: O=100, RATE CVL 1.
# Tổng tháng: S10 CVL = 75 + 100 = 175 · COR = 25 · O10 = 200.
DONG_TT = [pb.DongCFA1("VX", T, "1", D(100), D(100)), pb.DongCFA1("VX", T, "2", D(0), D(50)),
           pb.DongCFA1("VY", T, "1", D(100), D(0))]
PE_TT = {("VX", T): {CVL: D(3), COR: D(1)}, ("VY", T): {CVL: D(1)}}


@pytest.mark.parametrize("so", ["GI", "OMC", "SC", "PS"])
def test_H11_R1_01_O0_P_duong_nhanh_tong_thang_chi_o_GI_OMC(so):
    kq = _chay(so, DONG_TT, PE_TT, VEN_TT)
    vx = kq.chia[("VX", T)]
    assert (vx[CVL][0], vx[COR][0]) == (D(75), D(25))               # PE: dòng O = 0 góp 0
    if PM_TONG_THANG[so]:
        # No 2: PM CVL = 50 × 175 / 200 = 43,75 · COR = 50 × 25 / 200 = 6,25 ⇒ cộng No 1 (75 · 25)
        assert (vx[CVL][1], vx[COR][1]) == (D("118.75"), D("31.25"))
        assert kq.theo_tong_thang == (("VX", T, "2"),)
    else:
        # RATE × P: No 2 PM CVL = 50 × .75 = 37,5 · COR = 12,5 ⇒ 112,5 · 37,5
        assert (vx[CVL][1], vx[COR][1]) == (D("112.5"), D("37.5"))
        assert kq.theo_tong_thang == ()


# VZ: O = 0 · P = 10 · ⛔ có PE nào (RATE rỗng). GI · OMC ⇒ PM chia theo tổng tháng (10 × 100/100); SC · PS ⇒
# ⛔ chia 0 ⇒ lỗi CÓ TÊN *(⛔ rơi im về 0)* — nhánh `tt` của engine là thứ duy nhất phân biệt hai bên.
DONG_RONG = [pb.DongCFA1("VZ", T, "1", D(0), D(10)), pb.DongCFA1("VY", T, "1", D(100), D(0))]
PE_RONG = {("VY", T): {CVL: D(1)}}


@pytest.mark.parametrize("so", ["GI", "OMC", "SC", "PS"])
def test_H11_R1_01_O0_P_duong_RATE_rong_nhanh_tt_cho_qua_hay_loi_co_ten(so):
    if PM_TONG_THANG[so]:
        kq = _chay(so, DONG_RONG, PE_RONG, VEN_TT)
        assert kq.chia[("VZ", T)][CVL] == (D(0), D(10)) and kq.theo_tong_thang == (("VZ", T, "1"),)
    else:
        with pytest.raises(pb.LoiPhanBo, match="Σ PE = 0 mà O = 0 · P = 10"):
            _chay(so, DONG_RONG, PE_RONG, VEN_TT)


def test_H11_R1_01_Đ3_mau_so_ba_ca_khong_rong():
    """Đ3: ca nào cũng có dòng KÍCH HOẠT luật *(tập rỗng ⇒ bài xanh vô nghĩa)*."""
    assert sum(1 for r in DONG_TT if r.o == 0 and r.p and r.p > 0) == 1
    assert sum(1 for r in DONG_RONG if r.o == 0 and r.p and r.p > 0) == 1
    assert {r.vendor for r in DONG_MUON} >= {"VD62", "VD341"} and len({r.no for r in DONG_MUON if r.vendor == "VD62"}) == 2
