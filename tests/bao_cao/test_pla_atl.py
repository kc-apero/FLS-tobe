"""`SO.PLA3-ATL` — dòng `PL2…PL8` từ **IX.PL** *(C12, `fls/cau_hinh/dong_pl.py`)* trên **lưới ATL của FLS**
*(đầu ra AL.KEY — H12)* + hai phép CHECK mỗi kỳ — ISP 3.1.2 · Step 44 · H13 · `WO-307`.

⭐ Engine `pla.dong_pl_atl` / `pla.check_atl` ⛔ chép biểu thức: định nghĩa là THAM SỐ *(IX.PL đọc từ kho ở cổng)*;
   phép tính đi qua CHÍNH `dong_pl.tinh_pl` / `dong_pl.check_pl`.
⭐ CHECK tách `dat_co_so` *(≥ 1 vế ≠ 0 mà cân)* / `dat_0_0` *(mọi mã của phép = 0 — Đ3: ⛔ "đạt" trơn)* / `do` /
   `khong_do_duoc` *(thiếu giá trị ⇒ lỗi CÓ TÊN của C12, ⛔ ngầm 0)*.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from fls.bao_cao import pla
from fls.cau_hinh import dong_pl

D = Decimal
KHOI = ("GROUP", "SGO1")
KY = ("2025M01", "2025M02")
#: mã lá mà IX.PL nhắc + mã của 2 phép CHECK *(lấy từ C12 — ⛔ gõ lại)*
MA_PL = sorted(dong_pl.ma_dung(dong_pl.DINH_NGHIA) - dong_pl.DAU_VAO_NGOAI)
MA_CHECK = sorted({m for _, t, p in dong_pl.CHECK for m in t + p})


def _luoi(gia=None) -> dict:
    """Lưới tổng hợp: mỗi (khối, mã, kỳ) một số ≠ 0 khác nhau *(Đ3: ⛔ tập 0)*."""
    o = {}
    for i, kh in enumerate(KHOI):
        for j, ma in enumerate(sorted(set(MA_PL) | set(MA_CHECK))):
            for k, ky in enumerate(KY):
                o[(kh, ma, ky)] = D(i * 1000 + j * 10 + k + 1) / D(7)
    o.update(gia or {})
    return o


def test_la_cua_PL_la_ma_HD_khong_gom_dong_PL():
    assert pla.la_cua_dong(dong_pl.DINH_NGHIA, "PL2") == frozenset({"GI", "OMC"})
    la8 = pla.la_cua_dong(dong_pl.DINH_NGHIA, "PL8")
    assert "TAC" in la8 and not any(m.startswith("PL") for m in la8) and len(la8) == 14
    assert "COM_GAG" in pla.la_cua_dong(dong_pl.DINH_NGHIA, "PL5")


def test_dong_pl_atl_bang_CHINH_tinh_pl_tung_khoi_ky():
    o = _luoi()
    kq = pla.dong_pl_atl(o, KHOI, KY, dong_pl.DINH_NGHIA)
    for kh in KHOI:
        for ky in KY:
            gt = {m: o[(kh, m, ky)] for m in MA_PL}
            mong = dong_pl.tinh_pl(gt | {"COM_GAG": D(0)})
            for pl in ("PL2", "PL3", "PL4", "PL6", "PL7", "PL8"):
                assert kq.o[(kh, pl, ky)] == mong[pl], (kh, pl, ky)
    assert len(kq.o) == len(KHOI) * len(KY) * 6          # Đ4: 6 dòng tính được × 2 khối × 2 kỳ


def test_PL5_thieu_COM_GAG_la_loi_CO_TEN_khong_lam_hong_dong_khac():
    kq = pla.dong_pl_atl(_luoi(), KHOI, KY, dong_pl.DINH_NGHIA,
                         {("GROUP", "2025M01"): {"COM_GAG": D(3)}})
    assert kq.o[("GROUP", "PL5", "2025M01")] == kq.o[("GROUP", "PL4", "2025M01")] - 3
    thieu = {k for k in kq.khong_tinh}
    assert thieu == {("GROUP", "PL5", "2025M02"), ("SGO1", "PL5", "2025M01"), ("SGO1", "PL5", "2025M02")}
    assert all(dong_pl.PL_THIEU_GIA_TRI in v for v in kq.khong_tinh.values())
    assert ("GROUP", "PL4", "2025M02") in kq.o                       # ⛔ một dòng thiếu làm hỏng dòng khác


def test_dinh_nghia_la_THAM_SO_doi_bieu_thuc_thi_doi_ket_qua():
    o = _luoi()
    dn = dict(dong_pl.DINH_NGHIA, PL2="GI - OMC")
    a = pla.dong_pl_atl(o, KHOI, KY, dong_pl.DINH_NGHIA).o
    b = pla.dong_pl_atl(o, KHOI, KY, dn).o
    assert a[("GROUP", "PL2", "2025M01")] != b[("GROUP", "PL2", "2025M01")]
    assert a[("GROUP", "PL8", "2025M01")] != b[("GROUP", "PL8", "2025M01")]   # lan qua chuỗi PL


def test_thieu_la_HD_la_loi_CO_TEN_khong_ngam_0():
    o = _luoi()
    del o[("SGO1", "GI", "2025M02")]
    kq = pla.dong_pl_atl(o, KHOI, KY, dong_pl.DINH_NGHIA)
    assert ("SGO1", "PL2", "2025M02") in kq.khong_tinh and ("SGO1", "PL8", "2025M02") in kq.khong_tinh
    assert ("SGO1", "PL2", "2025M01") in kq.o


def test_check_atl_bon_trang_thai():
    o = _luoi()
    # GROUP 2025M01: phép ① đạt 0=0, phép ② đạt CÓ SỐ *(NIS = CXA = 5, còn lại 0)*
    for m in MA_CHECK:
        o[("GROUP", m, "2025M01")] = D(0)
    o[("GROUP", "NIS", "2025M01")] = o[("GROUP", "CXA", "2025M01")] = D(5)
    # GROUP 2025M02: ② đạt 0=0 · ① đỏ *(NB = 7)*
    for m in MA_CHECK:
        o[("GROUP", m, "2025M02")] = D(0)
    o[("GROUP", "NB", "2025M02")] = D(7)
    # SGO1 2025M02: thiếu `MC` ⇒ khong_do_duoc *(cả hai phép — check_pl của C12 đòi đủ mã)*
    del o[("SGO1", "MC", "2025M02")]
    kq = {(x.khoi, x.ky, x.phep): x for x in pla.check_atl(o, KHOI, KY)}
    p1, p2 = (t for t, _, _ in dong_pl.CHECK)
    assert len(kq) == len(KHOI) * len(KY) * 2
    assert kq[("GROUP", "2025M01", p1)].trang_thai == "dat_0_0"
    assert kq[("GROUP", "2025M01", p2)].trang_thai == "dat_co_so"
    assert kq[("GROUP", "2025M02", p1)].trang_thai == "do" and kq[("GROUP", "2025M02", p1)].chenh == 7
    assert kq[("GROUP", "2025M02", p2)].trang_thai == "dat_0_0"
    assert kq[("SGO1", "2025M02", p1)].trang_thai == kq[("SGO1", "2025M02", p2)].trang_thai == "khong_do_duoc"
    assert dong_pl.PL_THIEU_GIA_TRI in kq[("SGO1", "2025M02", p2)].ly_do
    assert kq[("SGO1", "2025M01", p2)].trang_thai == "do"          # số tổng hợp ⛔ cân
    assert set(x.trang_thai for x in kq.values()) == set(pla.TRANG_THAI_CHECK)


def test_check_atl_dung_sai_float_chi_trong_nguong():
    o = _luoi()
    for m in MA_CHECK:
        o[("GROUP", m, "2025M01")] = D(0)
    o[("GROUP", "NIS", "2025M01")] = D(5)
    o[("GROUP", "CXA", "2025M01")] = D(5) + D("1e-15")               # nhiễu float sheet
    kq = {(x.khoi, x.ky, x.phep): x for x in pla.check_atl(o, KHOI, KY)}
    p2 = dong_pl.CHECK[1][0]
    assert kq[("GROUP", "2025M01", p2)].trang_thai == "dat_co_so"
    o[("GROUP", "CXA", "2025M01")] = D(5) + D("1e-6")
    kq = {(x.khoi, x.ky, x.phep): x for x in pla.check_atl(o, KHOI, KY)}
    assert kq[("GROUP", "2025M01", p2)].trang_thai == "do"


def test_engine_khong_go_cung_ma_HD():
    """⛔ chép biểu thức IX.PL vào engine: phần mã mới của `pla.py` ⛔ nhắc mã HD nào trong CHECK/PL bằng chữ."""
    import inspect
    src = inspect.getsource(pla.dong_pl_atl) + inspect.getsource(pla.check_atl) + inspect.getsource(pla.la_cua_dong)
    for ma in ("GI", "OMC", "NB", "NIS", "CXA", "TAC", "COM_GAG", "PL2", "PL4"):
        assert f'"{ma}"' not in src and f"'{ma}'" not in src, ma


@pytest.mark.parametrize("dn", [{"PL2": "GI + "}, {"PL2": "PL3", "PL3": "PL2"}])
def test_dinh_nghia_hong_la_loi_CO_TEN(dn):
    kq = pla.dong_pl_atl(_luoi(), KHOI, KY, dn)
    assert kq.khong_tinh and all(v & {dong_pl.PL_CU_PHAP, dong_pl.PL_CHU_TRINH} for v in kq.khong_tinh.values())
