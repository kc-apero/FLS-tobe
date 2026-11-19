# -*- coding: utf-8 -*-
"""`H10` — `AL.PLT` · 5 vendor đặc biệt theo mã **'cách tính'** *(ISP 3.1.2 · Step 28 · `WO-216`)*.

AC-1 `H10-B1` bảng hàm theo mã *(mỗi mã một ca TAY TÍNH; mã lạ ⇒ lỗi CÓ TÊN)* · AC-2 `H10-B2` grep
tên vendor trong `fls/bao_cao` = 0 · AC-5 `H9-R1-04` ⓐ ⓑ bằng công thức AS-IS · AC-6 ⛔ vòng tròn
*(đột biến MỘT ô MID1 đầu vào ⇒ ĐÚNG các ô MID3 của Vendor-tháng ấy đổi)*. Cổng `WP-C4b` *(AC-3 · AC-4)*
ở `tests/oracle/test_do_hd2_c4b.py`.

⭐ Công thức AS-IS đọc NGUYÊN VĂN bằng `FORMULA` 19/11 *(chép trong `fls/bao_cao/phan_bo.py` +
`BG-217`)*. Ở đây số TAY TÍNH; tên mã `cach_tinh` là DỮ LIỆU config *(`fls.cau_hinh.vendor.CACH_TINH`)*.
"""
from __future__ import annotations

import re
import subprocess
from decimal import Decimal as D
from pathlib import Path

import pytest

from fls.bao_cao import phan_bo as pb
from fls.cau_hinh.vendor import CACH_TINH, NHAN_RIENG, NHAN_THUONG, BangVen, DongVen

GOC = Path(__file__).resolve().parents[2]
C6 = ("CVL", "COR", "SHQ1", "CSM", "CAH", "ASA")
C7 = (*C6, "SHQ2")
T = "202505"


def _ven(dong: list[tuple]) -> BangVen:
    """dong = (vendor, No, network, pct, cach_tinh) theo THỨ TỰ sheet."""
    ds = [DongVen(i, str(i + 3), no, v, net, None, None if pct is None else D(pct), 1, 1, ct)
          for i, (v, no, net, pct, ct) in enumerate(dong, start=1)]
    return BangVen("tong-hop", tuple(ds), C7, NHAN_RIENG)


# Bảng IX.VEN TỔNG HỢP — cùng hình với ảnh DT8: dòng đầu của vendor quyết hàm PE *(VLOOKUP khớp
# dòng ĐẦU)*; VQ mang `Max` rồi mã mượn RATE *(hình VD62)*; VT thuần thường.
VEN = _ven([
    ("VM", "1", "Max", "0.25", "Max"),
    ("VQ", "1", "Max", "0.5", "Max"),
    ("VA", "1", "NetA", "1", "VD341"), ("VA", "2", "NetZ", "1", "VD341"),
    ("VB", "1", "NetB", "1", "VD444"),
    ("VC", "1", "Store1", "1", "VD428"), ("VC", "2", "Store2", "1", "VD428"), ("VC", "3", None, None, "VD428"),
    ("VQ", "2", None, None, "VD62"),
    ("VT", "1", "NetT", "1", NHAN_THUONG),
])
# Bảng mã → hàm cho bài: cùng KIỂU với config thật, khoá là mã tổng hợp *(⛔ tên vendor thật)*.
BANG = {NHAN_THUONG: ("khong", None), "Max": ("mang_ty_le_no1", None),
        "VD341": ("mang_theo_no", None), "VD444": ("mang_theo_no", None),
        "VD428": ("mang_dong_no", None), "VD62": ("khong", "VA")}

L = [pb.DongLooker("Max", None, T, "CVL", D(80)), pb.DongLooker("Max", None, T, "COR", D(20)),
     pb.DongLooker("Max", None, "202504", "CVL", D(999)),
     pb.DongLooker("NetA", "1", T, "CVL", D(7)), pb.DongLooker("NetA", "2", T, "CVL", D(5)),
     pb.DongLooker("NetZ", "2", T, "CVL", D(1000)),
     pb.DongLooker("NetB", "1", T, "CAH", D(3)), pb.DongLooker("NetB", "1", T, "CAH", D(4)),
     pb.DongLooker("Store1", "9", T, "CSM", D(11)), pb.DongLooker("Store2", None, T, "CSM", D(13)),
     pb.DongLooker("NetT", "1", T, "CVL", D(500))]


def _pe(v, no, c):
    return pb.pe_tu_looker(VEN, L, v, T, no, c, bang=BANG)


# ── AC-1 · H10-B1 — mỗi mã một ca TAY TÍNH ───────────────────────────────────────────────────────
def test_H10_B1_ma_Max_mang_x_ty_le_chi_No_1():
    # Σ K[I = Max, O = T, S = CVL] = 80 ; × % dòng đầu VM = 0,25 ⇒ 20 ; No ≠ 1 ⇒ 0
    assert _pe("VM", "1", "CVL") == D(20) and _pe("VM", "1", "COR") == D(5)
    assert _pe("VM", "2", "CVL") == 0


def test_H10_B1_ma_VD341_VD444_mang_dong_DAU_loc_theo_No():
    # VA dòng đầu network NetA ⇒ No 2 vẫn lọc I = NetA *(⛔ NetZ của dòng No 2 — VLOOKUP dòng đầu)*
    assert _pe("VA", "1", "CVL") == D(7) and _pe("VA", "2", "CVL") == D(5)
    assert _pe("VB", "1", "CAH") == D(7) and _pe("VB", "2", "CAH") == 0


def test_H10_B1_ma_VD428_mang_theo_dong_No_KHONG_loc_No():
    # No 1 ⇒ Store1 (Σ mọi No Looker = 11) · No 2 ⇒ Store2 = 13 · No 3 network rỗng ⇒ 0
    assert (_pe("VC", "1", "CSM"), _pe("VC", "2", "CSM"), _pe("VC", "3", "CSM")) == (11, 13, 0)


def test_H10_B1_ma_VD62_PE_theo_dong_DAU_Max_va_thuong_bang_0():
    # VQ dòng đầu `Max` ⇒ hàm Max × 0,5 ; No 2 ⇒ 0. Vendor thuần thường ⇒ 0 *(nhánh `else 0` AS-IS)*
    assert _pe("VQ", "1", "CVL") == D(40) and _pe("VQ", "2", "CVL") == 0
    assert _pe("VT", "1", "CVL") == 0


def _dong(*xs):
    return [pb.DongCFA1(v, t, no, D(o), None if p is None else D(p)) for v, t, no, o, p in xs]


PE = {("VA", T): {"CVL": D(1), "COR": D(3)},         # RATE VA = ¼ · ¾
      ("VQ", T): {"CSM": D(2), "CAH": D(2)},         # RATE VQ = ½ · ½
      ("VM", T): {"ASA": D(9)}}


def test_H10_B1_ma_VD62_MUON_RATE_cho_No_co_P_LON_HON_va_hoa_thi_No_sau():
    # AS-IS AT = if(ΣP No1 > ΣP No2, "<mượn>", "<chính nó>"); No còn lại lấy phần kia
    kq = pb.chia_theo_cach_tinh(_dong(("VQ", T, "1", 8, 4), ("VQ", T, "2", 4, 0),
                                      ("VA", T, "1", 0, 0)), PE, VEN, cdt1=C6, bang=BANG)
    # No1 P=4 > 0 ⇒ No1 mượn RATE VA: CVL ¼×8 = 2, COR ¾×8 = 6 ; No2 RATE VQ: CSM ½×4 = 2, CAH 2
    d = kq.chia[("VQ", T)]
    assert (d["CVL"][0], d["COR"][0], d["CSM"][0], d["CAH"][0]) == (2, 6, 2, 2)
    assert d["CVL"][1] == 1 and d["COR"][1] == 3            # P 4 × RATE VA
    assert kq.muon == (("VQ", T, "1", "VA"),)
    hoa = pb.chia_theo_cach_tinh(_dong(("VQ", T, "1", 8, 0), ("VQ", T, "2", 4, 0),
                                       ("VA", T, "1", 0, 0)), PE, VEN, cdt1=C6, bang=BANG)
    assert hoa.muon == (("VQ", T, "2", "VA"),)              # hoà ⇒ No sau mượn *(nhánh `else`)*
    d = hoa.chia[("VQ", T)]
    assert (d["CSM"][0], d["CVL"][0], d["COR"][0]) == (4, 1, 3)


def test_H10_B1_muon_RATE_can_DUNG_2_No_khac_thi_LOI_CO_TEN():
    with pytest.raises(pb.LoiPhanBo, match=r"VQ · 202505: mượn RATE cần đúng 2 No, đo 1"):
        pb.chia_theo_cach_tinh(_dong(("VQ", T, "1", 8, 0), ("VA", T, "1", 0, 0)), PE, VEN,
                               cdt1=C6, bang=BANG)


def test_H10_B1_ma_LA_thi_LOI_CO_TEN_khong_im():
    with pytest.raises(pb.LoiPhanBo, match=r"mã 'cách tính' ⛔ có hàm: 'VD341' \(vendor VA\)"):
        pb.ma_cach_tinh(VEN, {k: v for k, v in BANG.items() if k != "VD341"})
    with pytest.raises(pb.LoiPhanBo, match=r"kiểu hàm PE lạ 'nhan_doi' \(mã 'Max'\)"):
        pb.ma_cach_tinh(VEN, {**BANG, "Max": ("nhan_doi", None)})


def test_H10_B1_bang_config_THAT_du_6_ma_va_kieu_deu_co_ham():
    assert set(CACH_TINH) == {NHAN_THUONG, *NHAN_RIENG}
    assert {k for k, _ in CACH_TINH.values()} <= set(pb.HAM_PE)
    assert sum(m is not None for _, m in CACH_TINH.values()) == 1    # chỉ một mã mượn RATE (VD62)


def test_H10_thuong_va_dac_biet_cung_mot_duong_bo_qua_0():
    kq = pb.chia_theo_cach_tinh(_dong(("VA", T, "1", 100, 40), ("VM", T, "1", 9, None)), PE, VEN,
                                cdt1=C6, bang=BANG)
    assert kq.chia[("VA", T)]["CVL"] == (D(25), D(10)) and kq.chia[("VA", T)]["COR"] == (D(75), D(30))
    assert kq.chia[("VM", T)]["ASA"] == (D(9), None)        # P chữ ⇒ PM ⛔ xác định *(⛔ hoá 0)*
    assert all(len(x) == 0 for x in kq.bo_qua.values()) and set(kq.bo_qua) == set(NHAN_RIENG)
    assert pb.ks_al(kq, kq.o, kq.p) == 2


# ── AC-5 · H9-R1-04 — "tổng tháng" theo công thức AS-IS `$P*S10/O10` ──────────────────────────────
def test_H9_R1_04_a_tong_thang_la_SIGMA_CHIA_moi_dong_thang_chia_SIGMA_O():
    # S10/O10 = Σ chia PE CDT1 mọi dòng CFA1 của tháng (kể cả đặc biệt) ÷ Σ O tháng.
    # dòng VA (O 100): CVL 25 · COR 75 ; VM (O 9): ASA 9 ⇒ S = 25 · 75 · 9, O tháng = 109.
    kq = pb.chia_theo_cach_tinh(_dong(("VA", T, "1", 100, 0), ("VM", T, "1", 9, 0),
                                      ("VT", T, "1", 0, 218)), PE, VEN, cdt1=C6, bang=BANG)
    d = kq.chia[("VT", T)]
    assert (d["CVL"][1], d["COR"][1], d["ASA"][1]) == (D(50), D(150), D(18))
    assert kq.theo_tong_thang == (("VT", T, "1"),)


def test_H9_R1_04_b_O_0_P_AM_khong_vao_tong_thang_sigma_PE_0_LOI_CO_TEN():
    # AS-IS `and($O=0,$P>0)` ⇒ P < 0 đi nhánh RATE riêng; Σ PE = 0 ⇒ AS-IS iferror ⇒ 0 IM.
    # TO-BE: lỗi CÓ TÊN *(giữ luật H9 — ⛔ chia 0 im)*.
    with pytest.raises(pb.LoiPhanBo, match=r"VT · 202505 · No 1: Σ PE = 0 mà O = 0 · P = -3"):
        pb.chia_theo_cach_tinh(_dong(("VA", T, "1", 100, 0), ("VT", T, "1", 0, -3)), PE, VEN,
                               cdt1=C6, bang=BANG)


def test_KS_AL_cat_dung_vendor_thang_lech():
    kq = pb.chia_theo_cach_tinh(_dong(("VA", T, "1", 100, 40)), PE, VEN, cdt1=C6, bang=BANG)
    kq.chia[("VA", T)]["CVL"] = (D(26), D(10))
    with pytest.raises(pb.LoiPhanBo, match=r"KS.AL VA · 202505 · PE: Σ chia − tiền = 1"):
        pb.ks_al(kq, kq.o, kq.p)


# ── AC-2 · H10-B2 — ⛔ `if` theo tên vendor ────────────────────────────────────────────────────────
TEN = ("VD341", "VD444", "VD428", "Max", "VD62")


def _dem(thu_muc: str) -> int:
    r = subprocess.run(["grep", "-rcE", r"\b(" + "|".join(TEN) + r")\b", "--include=*.py", thu_muc],
                       cwd=GOC, capture_output=True, text=True)
    return sum(int(x.rsplit(":", 1)[1]) for x in r.stdout.splitlines())


def test_H10_B2_grep_ten_vendor_trong_fls_bao_cao_BANG_0_va_doi_chung_duong():
    assert _dem("fls/bao_cao") == 0
    assert _dem("fls/cau_hinh") > 0          # Đ3: phép grep ⛔ mù — tên sống ở CONFIG
    assert re.search(r"\bVD62\b", (GOC / "fls/cau_hinh/vendor.py").read_text(encoding="utf-8"))
