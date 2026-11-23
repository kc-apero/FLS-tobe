# -*- coding: utf-8 -*-
"""`WO-023` `(e)` · `KQ-021 F-4` + `KQ-025 F-1` — khối `SINH-KHOP` của
`khop_owner.py` chỉ mang **QUAN HỆ**; số đếm chữ tài liệu ra **màn**.

⛔⛔ Lỗi gốc *(mã khi nhận `7e67a09`)*: ô **tài liệu** của `T2`·`B5`·`C2`·`C3`·
`C4`·`C7` in số đếm *(`b.dem` / `b.dem_tep`)* ⇒ **mỗi** lần ai viết thêm một
phiếu nhắc *"7 trường"* hay `fls-ba` sửa `BA-06` là `--kiem` đỏ ⛔ vì lệch nào
*(`BG-024` tự làm `C3` `59 → 60`)*. Bài **ba** chiều:
  ⓐ ô tài liệu ⛔ chứa chữ số **ngoài** chính cụm được đếm *(`«64 cột»` …)*;
  ⓑ thêm **một** lần cụm ⇒ ô ⛔ đổi, **màn** *(`Ket.man`)* đổi — tức số đếm
     **có** đi ra màn *(⛔ bị vứt)*;
  ⓒ xoá **mọi** lần cụm ⇒ `khop` lật `False` *(phép vẫn đo — ⛔ thành hằng)*.
⭐ Gọi **hàm thật** của `khop_owner` trên `Boi` thật *(đọc toàn bộ `.md` repo)*;
⛔ chạm kho *(sáu phép này ⛔ hỏi kho — `conn=None`)*.
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import sys

import pytest

GOC = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def ko():
    sp = importlib.util.spec_from_file_location(
        "_khop_owner_wo023", GOC / "docs" / "ITL" / "_tools" / "khop_owner.py")
    m = importlib.util.module_from_spec(sp)
    # ⚠ `@dataclass` tra `sys.modules[cls.__module__]` — phải đăng ký trước
    #   *(khuôn `tests/repo/test_wo011_thuoc_nguoi_pg.py::_khop_owner`)*
    sys.modules[sp.name] = m
    sp.loader.exec_module(m)
    return m


#: phép → (hàm, cụm đếm, tệp nhận thêm cụm — `None` = một tệp mới)
PHEP = {
    "T2": ("_t2", "File 1_2", None),
    "B5": ("_b5", "gợi ý", "06_SCREEN_SPEC.md"),
    "C2": ("_c2", "64 cột", None),
    "C3": ("_c3", "7 trường", None),
    "C4": ("_c4", "52 cột", None),
    "C7": ("_c7", "24 cột nền", None),
}
#: chữ số **được phép** trong ô — chính cụm được đếm *(⛔ số đếm)*
CUM_TRONG_O = re.compile(r"«[^»]*»")


def _boi(ko):
    return ko.Boi(conn=None)


@pytest.mark.parametrize("ma", sorted(PHEP))
def test_AC5_o_TAI_LIEU_khong_mang_so_dem__MAN_mang(ko, ma):
    ten, _cum, _tep = PHEP[ma]
    k = getattr(ko, ten)(_boi(ko))
    sach = CUM_TRONG_O.sub("", k.tai_lieu)
    assert not re.search(r"\d", sach), f"⛔ ô tài liệu {ma} còn chữ số: {k.tai_lieu!r}"
    assert re.search(r"\d", k.man), f"⛔ số đếm {ma} ⛔ ra màn: {k.man!r}"
    assert k.khop is True, (ma, k)


@pytest.mark.parametrize("ma", sorted(PHEP))
def test_AC5_THEM_mot_lan_cum__o_KHONG_doi__man_DOI(ko, ma):
    ten, cum, tep = PHEP[ma]
    b = _boi(ko)
    k0 = getattr(ko, ten)(b)
    if tep:
        p = [x for x in b.md if x.name == tep][0]
        b.md[p] = b.md[p] + "\n" + cum + "\n"
    else:
        b.md[GOC / "docs" / "ITL" / "zz_thu_wo023.md"] = "# thu\n\n" + cum + "\n"
    k1 = getattr(ko, ten)(b)
    assert k1.tai_lieu == k0.tai_lieu, (ma, k0.tai_lieu, k1.tai_lieu)
    assert k1.man != k0.man, (ma, "⛔ màn ⛔ đổi — số đếm ⛔ được đo?", k0.man)
    assert k1.khop == k0.khop


@pytest.mark.parametrize("ma", ["B5", "C3"])
def test_AC5_XOA_moi_lan_cum__khop_LAT(ko, ma):
    """⭐ Chiều ĐỎ của chính phép *(`Đ5`)*: ⛔ đổi `mong`, nhưng tập rỗng phải
    lật ⇒ `--kiem` NO *(`DOI TRANG THAI`)*."""
    ten, cum, tep = PHEP[ma]
    b = _boi(ko)
    xoa = ("đề xuất", "gợi ý") if ma == "B5" else (cum,)
    for p in list(b.md):
        s = b.md[p]
        for c in xoa:
            s = s.replace(c, "x")
        b.md[p] = s
    k = getattr(ko, ten)(b)
    assert k.khop is False, (ma, k)
    assert "⛔ khong co" in k.tai_lieu, k.tai_lieu
