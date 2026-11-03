"""Doc co retry + tich luy tang dan; MOT khoi loi KHONG pha ca luot doc (DoD 5.6 ③).

Do that: co khoi truot 3/3 lan ke ca khi cat lat 1.500 dong. Nen "mot khoi loi
lam do ca luot doc" la thiet ke khong dung duoc voi so nay.
"""
from __future__ import annotations

import pytest

from fls.oracle.doc import doc_dan


def _no(_r):
    raise TimeoutError("500")


def test_doc_du_ba_khoang_khi_moi_thu_binh_thuong():
    duoc, truot = doc_dan(lambda r: [r], ("A1:A9", "B1:B9", "C1:C9"))
    assert set(duoc) == {"A1:A9", "B1:B9", "C1:C9"} and truot == []


def test_mot_khoang_loi_thi_van_lay_duoc_cac_khoang_con_lai():
    def lay(r):
        if r == "B1:B9":
            raise TimeoutError("503")
        return [r]
    duoc, truot = doc_dan(lay, ("A1:A9", "B1:B9", "C1:C9"), lan_thu=2)
    assert set(duoc) == {"A1:A9", "C1:C9"}
    assert len(truot) == 1 and "B1:B9" in truot[0] and "503" in truot[0]


def test_thu_lai_thanh_cong_o_lan_hai():
    dem = {"n": 0}

    def lay(r):
        dem["n"] += 1
        if dem["n"] == 1:
            raise TimeoutError("503")
        return [r]
    duoc, truot = doc_dan(lay, ("A1:A9",), lan_thu=3)
    assert duoc and truot == [] and dem["n"] == 2


def test_khong_thu_lai_vo_han():
    dem = {"n": 0}

    def lay(r):
        dem["n"] += 1
        raise TimeoutError("503")
    doc_dan(lay, ("A1:A9",), lan_thu=3)
    assert dem["n"] == 3


def test_truot_het_thi_bao_ro_chu_khong_tra_rong_im_lang():
    duoc, truot = doc_dan(_no, ("A1:A9", "B1:B9"), lan_thu=1)
    assert duoc == {} and len(truot) == 2


def test_khoang_trung_nhau_bi_chan_thay_vi_doc_hai_lan():
    with pytest.raises(ValueError, match="trung"):
        doc_dan(lambda r: [r], ("A1:A9", "A1:A9"))
