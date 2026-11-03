"""Anh chup DONG BANG: chup 2 lan cach nhau -> checksum khop (DoD 5.6 cong 1)."""
from __future__ import annotations

from datetime import date

import pytest

from fls.oracle.anh_chup import AnhChup

DONG = ({"itl_id_sheet": "ITL-1", "hd": "A"}, {"itl_id_sheet": "ITL-2", "hd": "B"})


def _chup(dong=DONG, run_id="R1", ngay=date(2026, 8, 26)) -> AnhChup:
    return AnhChup(run_id=run_id, ngay=ngay, nguon="RAW", dong=dong)


def test_hai_lan_chup_cung_noi_dung_thi_checksum_khop():
    assert _chup().checksum() == _chup().checksum()


def test_checksum_khong_phu_thuoc_THU_TU_doc():
    """Doc tang dan / cat lat khac nhau van phai ra cung mot so."""
    assert _chup(DONG).checksum() == _chup(tuple(reversed(DONG))).checksum()


def test_checksum_khong_phu_thuoc_run_id_va_ngay_chup():
    """Cung noi dung, hai lan chay khac nhau -> van khop. Neu khong, cong vo dung."""
    assert _chup(run_id="R1").checksum() == _chup(
        run_id="R2", ngay=date(2026, 9, 1)).checksum()


def test_doi_MOT_o_thi_checksum_doi():
    khac = ({"itl_id_sheet": "ITL-1", "hd": "A"},
            {"itl_id_sheet": "ITL-2", "hd": "B "})
    assert _chup().checksum() != _chup(khac).checksum()


def test_anh_chup_dong_bang_khong_sua_duoc():
    a = _chup()
    with pytest.raises(Exception):
        a.run_id = "R9"          # type: ignore[misc]


def test_chup_rong_thi_NO_TO_chu_khong_tra_checksum_rong():
    with pytest.raises(ValueError, match="rong"):
        _chup(dong=()).checksum()
