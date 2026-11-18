"""H6 — `cuon_ky`: cuộn lưới `SO.CFA1 Daily` thành Y/H/Q/M theo IX.PER *(ISP 3.1.2 · Step 20 · WO-188)*.

⭐ Hành vi AS-IS *(công thức SA `Report I CFA1 Y H Q M`, đọc 18/11 — FORMULA hàng 6…12)*:
  · ô LÁ = `SUMIFS(Daily!hàng, Daily!$1:$1, năm[, Daily!$2:$2 | $3:$3 | $4:$4, H/Q/M])`;
  · hàng tiêu đề Daily: `Year = YEAR(ngày)` · `Half = if(tháng<7,"H1","H2")` ·
    `Quarter = if(tháng<4,"Q1",…)` · `Month = MONTH(ngày)` ⇒ năm của **CHÍNH ngày** *(⛔ ép 2025)*;
  · ô CHA = `=sum(con)` *(Daily cha cũng = sum(con) ⇒ cuộn cha = Σ con đã cuộn)*.

  · **AC-1 · H6-B1** — Daily 2 ngày T11/2024 ⇒ Y2024 *(⛔ 2025)*; H2 · Q4 · M11 đúng; kỳ khác 0.
  · **AC-3** — trục Daily lấy từ `IX.PER` *(`truc_ngay(lich, den)`)*, ⛔ tham số ngày đầu tạm.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal as D

import pytest

from fls.bao_cao.cfa import (KHOI_TONG, DongCFA, cfa1_daily, cuon_ky, ky_truc_nam, nhan_ky,
                             truc_ngay)
from fls.cau_hinh import ky
from fls.cau_hinh.hd import CayHD, NutHD


def _sr(d: date) -> int:
    return (d - date(1899, 12, 30)).days


def _cay() -> CayHD:
    return CayHD(nguon="bai-h6", nut=(
        NutHD(ma="P", ten="Cha", cha=None, cap=1, nhom="HDO", dong_sheet="1", thu_tu=1),
        NutHD(ma="A", ten="La A", cha="P", cap=2, nhom="HDO", dong_sheet="2", thu_tu=2),
        NutHD(ma="B", ten="La B", cha="P", cap=2, nhom="HDO", dong_sheet="3", thu_tu=3),
    ))


def _lich(ngay_dau: date = date(2024, 10, 21)) -> ky.LichKy:
    return ky.LichKy(nguon="bai-h6", ngay_dau=ngay_dau, luat=ky.LUAT_A)


# ── AC-1 · H6-B1 ─────────────────────────────────────────────────────────────────

def test_H6_B1_hai_ngay_T11_2024_cuon_vao_Y2024_KHONG_2025():
    n1, n2 = date(2024, 11, 5), date(2024, 11, 28)
    truc = truc_ngay(_lich(), den=date(2024, 12, 31))
    dong = [DongCFA(_sr(n1), None, "A | La A", D("1.5"), D("0")),
            DongCFA(_sr(n2), None, "B | La B", D("0"), D("0.25"))]
    kq = cfa1_daily(dong, _cay(), ngay=truc, khoi=(KHOI_TONG,))
    cu = cuon_ky(kq.o, _cay(), ngay=truc, khoi=(KHOI_TONG,))
    assert cu.nam == (2024,)
    o = cu.o
    for k in ("2024", "2024H2", "2024Q4", "2024M11"):
        assert o[(KHOI_TONG, "A", k)] == D("1.5")
        assert o[(KHOI_TONG, "B", k)] == D("-0.25")
        assert o[(KHOI_TONG, "P", k)] == D("1.25")             # cha = Σ con
    for k in ("2024H1", "2024Q3", "2024M10", "2024M12"):
        assert o[(KHOI_TONG, "P", k)] == 0
    assert not any(k[2].startswith("2025") for k in o)          # ⛔ ép 2025


def test_H6_B1_nhan_ky_trung_khuon_dap_an_410_va_19_ky_moi_nam():
    assert ky_truc_nam(2024)[:8] == ["2024", "2024H1", "2024H2", "2024Q1", "2024Q2", "2024Q3",
                                     "2024Q4", "2024M01"]
    assert len(ky_truc_nam(2026)) == 19 and ky_truc_nam(2026)[-1] == "2026M12"
    k = ky.ky_cua(date(2026, 11, 5))
    assert nhan_ky(k) == ("2026", "2026H2", "2026Q4", "2026M11")


def test_H6_B1_ky_khong_ngay_tren_truc_duoc_KHAI__khong_phai_0_da_chot():
    """Errata ㉑: kỳ ⛔ có ngày nào trên trục *(trước ngày đầu · chưa tới)* ⇒ `ky_khong_ngay`."""
    truc = truc_ngay(_lich(), den=date(2024, 11, 18))
    kq = cfa1_daily([], _cay(), ngay=truc, khoi=(KHOI_TONG,))
    cu = cuon_ky(kq.o, _cay(), ngay=truc, khoi=(KHOI_TONG,))
    assert cu.ky_khong_ngay == ("2024H1", "2024Q1", "2024Q2", "2024Q3", "2024M01", "2024M02",
                                "2024M03", "2024M04", "2024M05", "2024M06", "2024M07", "2024M08",
                                "2024M09", "2024M12")
    assert cu.so_ngay == {"2024": 29, "2024H2": 29, "2024Q4": 29, "2024M10": 11, "2024M11": 18}


def test_H6_B1_nam_tu_du_lieu_truc_qua_nam():
    truc = truc_ngay(_lich(date(2025, 12, 30)), den=date(2026, 1, 2))
    kq = cfa1_daily([DongCFA(_sr(date(2026, 1, 1)), None, "A | La A", D("2"), D("0"))], _cay(),
                    ngay=truc, khoi=(KHOI_TONG,))
    cu = cuon_ky(kq.o, _cay(), ngay=truc, khoi=(KHOI_TONG,))
    assert cu.nam == (2025, 2026)
    assert cu.o[(KHOI_TONG, "A", "2026M01")] == 2 and cu.o[(KHOI_TONG, "A", "2025")] == 0


# ── AC-3 · trục từ IX.PER ────────────────────────────────────────────────────────

def test_H6_AC3_truc_ngay_tu_IX_PER_den_ngay_doc():
    t = truc_ngay(_lich(), den=date(2026, 11, 18))
    assert t[0] == _sr(date(2024, 10, 21)) and t[-1] == _sr(date(2026, 11, 18))
    assert len(t) == 759 and t == list(range(t[0], t[-1] + 1))


def test_H6_AC3_truc_ngay_den_truoc_ngay_dau_bi_tu_choi():
    with pytest.raises(ValueError):
        truc_ngay(_lich(), den=date(2024, 10, 20))


def test_H6_AC3_cuon_ky_luoi_thieu_o_thi_KeyError_khong_hoa_0():
    """Lưới Daily thiếu ô *(khối/nút/ngày)* ⇒ ném, ⛔ lặng lẽ coi 0."""
    truc = truc_ngay(_lich(), den=date(2024, 10, 22))
    kq = cfa1_daily([], _cay(), ngay=truc, khoi=(KHOI_TONG,))
    del kq.o[(KHOI_TONG, "A", truc[0])]
    with pytest.raises(KeyError):
        cuon_ky(kq.o, _cay(), ngay=truc, khoi=(KHOI_TONG,))
