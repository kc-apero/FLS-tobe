# -*- coding: utf-8 -*-
"""Adapter `F04` — `R |` -> khuon `Bank Transactions`.

⭐ Moi bai o day do MOT cau khang dinh da chung minh tren nguon SONG, ⛔ khong
   phai mot y thich cua nguoi viet.
"""
from __future__ import annotations

from collections import Counter

import pytest

from fls.adapters import sao_ke as sk

# ban khai: cot 0=Date, 1=Description, 2=Currency, 3=Debit, 4=Credit, 5=Ref
D1 = ["1", "2", "3", "4", "5", "6"]
# mot bo tri KHAC — Date o cuoi. Do tren kho 08/09: **19** bo cot khac
# nhau tren 68 dong chay (**16** theo 5 truong FLS thuc doc).
D1_LOAN = ["4", "5", "6", "1", "2", "3"]


def _hang(ngay="10/21/2024", mo_ta="x", tt="VND", no="", co=100, ma="FT1"):
    return [ngay, mo_ta, tt, no, co, ma]


def test_doc_ban_khai_du_6():
    assert sk.doc_ban_khai(D1) == {
        "Date": 0, "Description": 1, "Currency": 2,
        "Debit": 3, "Credit": 4, "Reference number": 5}


def test_doc_ban_khai_chap_nhan_kieu_so_thuc():
    """Mot sheet OCBC ghi `5.00` thay vi `5` — do duoc tren nguon song."""
    assert sk.doc_ban_khai(["1", "2", "3", "4", "5.00", "6"])["Credit"] == 4


def test_NO_TO_khi_ban_khai_thieu_truong():
    with pytest.raises(sk.BanKhaiHong) as e:
        sk.chuyen("R | X", sk.doc_ban_khai(["1", "2", "3", "4", "5"]), [])
    assert "Reference number" in str(e.value)


def test_DOC_ban_khai_chu_KHONG_doan_vi_tri_cot():
    """⭐ Cau khang dinh trung tam cua adapter nay."""
    ra, _ = sk.chuyen("R | X", sk.doc_ban_khai(D1_LOAN),
                      [["", 100, "FT9", "10/21/2024", "mo ta", "VND"]])
    i = sk.KHUON_RA.index
    assert ra[0][i("Transaction date")] == "10/21/2024"
    assert ra[0][i("Reference number")] == "FT9"
    assert ra[0][i("Credit")] == 100


def test_Num_la_THU_TU_lan_xuat_hien_cua_ma():
    ra, _ = sk.chuyen("R | X", sk.doc_ban_khai(D1), [_hang(ma="A"), _hang(ma="B"),
                                    _hang(ma="A"), _hang(ma="A")])
    i = sk.KHUON_RA.index("Num")
    assert [r[i] for r in ra] == [1, 1, 2, 3]


def test_Num_dem_XUYEN_nhieu_sheet():
    """Ma co the lap giua cac tai khoan ⇒ bo dem phai di xuyen sheet."""
    dem = Counter()
    r1, _ = sk.chuyen("R | A", sk.doc_ban_khai(D1), [_hang(ma="Z")], dem)
    r2, _ = sk.chuyen("R | B", sk.doc_ban_khai(D1), [_hang(ma="Z")], dem)
    i = sk.KHUON_RA.index("Num")
    assert r1[0][i] == 1 and r2[0][i] == 2


def test_Source_mang_dung_ten_sheet():
    ra, _ = sk.chuyen("R | 854888_TCB VND_VGOH", sk.doc_ban_khai(D1), [_hang()])
    assert ra[0][sk.KHUON_RA.index("Source")] == "R | 854888_TCB VND_VGOH"


def test_dong_KHONG_co_ngay_la_RONG_chu_khong_phai_loi():
    """O luoi trong ⛔ khong phai mot dong — bay da dap 5 lan trong `Đ`."""
    _, tk = sk.chuyen("R | X", sk.doc_ban_khai(D1), [_hang(), _hang(ngay=""), _hang(ngay="  ")])
    assert (tk.ra, tk.rong, tk.loi) == (1, 2, 0)


def test_o_LOI_di_duong_loi_chu_KHONG_bi_nuot():
    _, tk = sk.chuyen("R | X", sk.doc_ban_khai(D1),
                      [_hang(), _hang(ngay="#REF!"), _hang(ma="#N/A")])
    assert (tk.ra, tk.rong, tk.loi) == (1, 0, 2)


def test_TONG_ba_duong_luon_bang_so_dong_VAO():
    """⛔ Khong dong nao duoc roi im lang."""
    vao = [_hang(), _hang(ngay=""), _hang(ngay="#REF!"), _hang(ma="B")]
    _, tk = sk.chuyen("R | X", sk.doc_ban_khai(D1), vao)
    assert tk.vao == len(vao) == tk.tong()


def test_hang_NGAN_hon_ban_khai_KHONG_lam_no():
    """Sheets cat duoi rong ⇒ hang co the ngan hon so cot da khai."""
    ra, tk = sk.chuyen("R | X", sk.doc_ban_khai(D1), [["10/21/2024", "x"]])
    assert tk.ra == 1 and ra[0][sk.KHUON_RA.index("Reference number")] == ""


def test_chay_lai_KHONG_nhan_doi():
    a, _ = sk.chuyen("R | X", sk.doc_ban_khai(D1), [_hang(), _hang(ma="B")])
    b, _ = sk.chuyen("R | X", sk.doc_ban_khai(D1), [_hang(), _hang(ma="B")])
    assert a == b


def test_khuon_ra_dung_10_cot_cua_Bank_Transactions():
    assert len(sk.KHUON_RA) == 10
    assert sk.KHUON_RA[:7] == ("Transaction date", "Description", "Currency",
                               "Debit", "Credit", "Reference number", "Source")


def test_CHI_MOT_BAN_KHAI_ANH_XA_trong_ca_he():
    """⛔ Hai ban sao mot luat la hai co hoi de chung lech nhau — va cai lech
    se **im lang**. Bai nay la anh em cua
    `tests/canon/test_o_loi.py::test_CHI_MOT_BAN_KHAI_trong_ca_he`.
    """
    import pathlib
    goc = pathlib.Path(__file__).resolve().parents[2]
    xau = []
    for f in list((goc / "fls").rglob("*.py")) + list((goc / "tools").rglob("*.py")):
        if f.name == "sao_ke.py":
            continue
        t = f.read_text(encoding="utf-8")
        if '"Reference number"' in t and '"Currency"' in t:
            xau.append(str(f.relative_to(goc)))
    assert not xau, "con ban sao cua ban khai anh xa: " + ", ".join(xau)
