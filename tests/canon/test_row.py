import pytest

from fls.canon.row import CanonRow


def _38(**kw):
    v = [None] * 38
    for k, x in kw.items():
        v[int(k[1:])] = x
    return v


def test_dung_38_phan_tu():
    r = CanonRow.from_list(_38(p0="2026-01-31"))
    assert len(r) == 38 and r.at(0) == "2026-01-31"


def test_sai_do_dai_thi_NO_khong_tu_dem_hay_cat():
    """Tu pad/cat la cach mat cot trong im lang."""
    with pytest.raises(ValueError, match="38"):
        CanonRow.from_list([None] * 37)
    with pytest.raises(ValueError, match="38"):
        CanonRow.from_list([None] * 39)


def test_truy_cap_theo_chu_cai():
    r = CanonRow.from_list(_38(p21="Da thanh toan"))
    assert r.by_letter("V") == "Da thanh toan"


def test_bon_gia_tri_AH_AK_khong_de_len_nhau():
    r = CanonRow.from_list(_38(p33="a", p34="b", p35="c", p36="d"))
    assert [r.by_letter(x) for x in ("AH", "AI", "AJ", "AK")] == ["a", "b", "c", "d"]


def test_as_jsonb_list_giu_nguyen_38_o_ke_ca_o_trong():
    r = CanonRow.from_list(_38(p0="x"))
    js = r.as_jsonb_list()
    assert len(js) == 38 and js[25] is None and js[26] is None


def test_khong_co_duong_nao_tra_ve_dict_theo_ten():
    """Luu theo key la MAT COT (4 cot AH-AK trung ten). Chan tu API."""
    r = CanonRow.from_list(_38())
    assert not hasattr(r, "as_dict")
    assert not hasattr(r, "by_name")


def test_bat_bien_khong_sua_duoc_tai_cho():
    r = CanonRow.from_list(_38(p0="x"))
    with pytest.raises((AttributeError, TypeError)):
        r.vals[0] = "y"
