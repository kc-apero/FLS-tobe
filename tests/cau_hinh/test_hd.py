# -*- coding: utf-8 -*-
"""`C4-B1 · B2 · B3` — cây IX.HD: nạp ảnh ATL + kiểm cha–con *(ISP 3.1.2 · Step 11 ·
`C4` · `WO-122`)*.

⭐ Nạp qua **đường dẫn TRUYỀN VÀO** *(AC-4 WO-122: ⛔ gõ cứng)*: bài nạp thẳng ảnh
   DT3 `tests/fixture/cau_hinh/atl_cay.json` bằng tham số `duong=`, ⛔ qua mặc định.
⭐ `Đ3` — mọi phép đếm là **bằng chứng DƯƠNG** trên tập KHÔNG RỖNG: `74` nút · `6`
   nhóm · `37` gốc · `MONG_CAP = {1:37,2:23,3:11,4:3}` *(đo DT3, 17/11)*.
⛔ `Đ5` — cây hỏng *(chu trình · cha vắng · cấp nhảy · mã trùng)* được chứng minh
   bằng ảnh TỔNG HỢP cố ý hỏng, và lỗi mang **TÊN** *(hằng chuỗi, ⛔ `ValueError`
   trơn)*; phá một nhánh kiểm thì phải có một bài đổi màu.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fls.cau_hinh import hd

GOC = Path(__file__).resolve().parents[2]
# Chép NGUYÊN VĂN đường ảnh DT3 — ⛔ đọc lại từ hằng mã *(một bài so hằng với chính
# nó ⛔ bao giờ đỏ)*. Đây là ảnh ĐÓNG BĂNG THẬT của DT3 *(`WO-122` Nền)*.
ANH_ATL = "tests/fixture/cau_hinh/atl_cay.json"
ANH_MM = "tests/fixture/cau_hinh/mapping_master_cfg.json"

MONG_NUT = 74
MONG_NHOM = ("HDO", "HDH", "HDAP", "HDT", "HDC", "HDCI")
MONG_GOC = 37
MONG_CAP = {1: 37, 2: 23, 3: 11, 4: 3}
MONG_MM = 73
MONG_CHENH = ["NCF"]            # ATL − MM = {NCF} (`BG-107`)


def _doc_atl() -> hd.CayHD:
    """Nạp ảnh DT3 qua ĐƯỜNG TRUYỀN VÀO *(⛔ mặc định)* — tương đối gốc repo."""
    van = (GOC / ANH_ATL).read_text(encoding="utf-8")
    return hd.doc_van_ban(van, nguon=ANH_ATL)


# ── C4-B1 · nạp ảnh ATL ─────────────────────────────────────────────────────
def test_C4_B1_nap_anh_ATL_74_nut_6_nhom_goc_dung_khong_chu_trinh():
    cay = _doc_atl()
    assert len(cay.nut) == MONG_NUT, f"⛔ mong {MONG_NUT} nút, đo {len(cay.nut)}"
    assert cay.nhom == MONG_NHOM, f"⛔ 6 nhóm sai thứ tự/thiếu: {cay.nhom}"
    assert len(cay.goc) == MONG_GOC, f"⛔ mong {MONG_GOC} gốc, đo {len(cay.goc)}"
    # gốc đúng = mọi gốc có `cha` None VÀ ở cấp 1 *(nạp sạch ⇒ ⛔ HD_CAP_NHAY)*.
    theo_ma = {n.ma: n for n in cay.nut}
    assert all(theo_ma[m].cha is None and theo_ma[m].cap == 1 for m in cay.goc)
    assert cay.nguon == ANH_ATL


def test_C4_B1_cap_L1_L4_khop_MONG_CAP_cua_anh():
    """AC-1: phân cấp `37 · 23 · 11 · 3` — `Đ3` bằng chứng DƯƠNG, ⛔ "không thấy lệch"."""
    assert _doc_atl().dem_cap() == MONG_CAP


def test_C4_B1_con_cua_va_la_dung():
    """`con_cua`/`la` — đo trên ảnh thật *(`Đ3`)*: nút cụ thể, ⛔ tính chất suông."""
    cay = _doc_atl()
    assert cay.con_cua("OPC") == ("CAC", "COS")     # thứ tự ảnh, ổn định
    assert cay.con_cua("CAC") == ("MAC", "COT")
    assert cay.la("GI") is True                     # gốc-lá
    assert cay.la("OMC") is True                    # lá cấp 4
    assert cay.la("OPC") is False                   # có con
    # tổng con trực tiếp = số nút ⛔ gốc = 74 − 37 = 37.
    assert sum(len(cay.con_cua(n.ma)) for n in cay.nut) == MONG_NUT - MONG_GOC
    # 64 lá *(đo DT3)*.
    assert sum(1 for n in cay.nut if cay.la(n.ma)) == 64


def test_C4_B1_la_doi_ma_co_that():
    """`la` của một mã ⛔ có ⇒ `KeyError` *(⛔ trả `True` câm — `Đ3`)*."""
    with pytest.raises(KeyError):
        _doc_atl().la("KHONG_CO_MA_NAY")


def test_C4_B1_doc_tep_mac_dinh_doc_anh_TINH_dong_bang(tmp_path):
    """`doc_tep()` *(mặc định)* đọc ẢNH TĨNH gói `fls/cau_hinh/tinh/` — cùng 74 nút."""
    cay = hd.doc_tep()
    assert cay.nguon == hd.NGUON_TINH
    assert len(cay.nut) == MONG_NUT and len(cay.goc) == MONG_GOC


def test_anh_tinh_goi_KHOP_anh_DT3_tung_byte():
    """Ảnh gói là **chép** ảnh DT3 *(⛔ sửa DT3 — `WO-122` ràng buộc)*. Ghim byte ⇒
    một lần đổi tay là ĐỎ *(⛔ để hai ảnh lặng lẽ lệch)*."""
    assert (GOC / hd.NGUON_TINH).read_bytes() == (GOC / ANH_ATL).read_bytes()
    assert (GOC / hd.NGUON_MM).read_bytes() == (GOC / ANH_MM).read_bytes()


# ── C4-B2 · chu trình ───────────────────────────────────────────────────────
def test_C4_B2_chu_trinh_A_B_A_loi_HD_CHU_TRINH():
    """A→B→A *(tổng hợp)* ⇒ lỗi có tên `HD_CHU_TRINH`."""
    dong = [
        {"ma": {"chu": "A"}, "ten": {"chu": "a"}, "cha": {"chu": "B"},
         "cap": "2", "nhom": {"chu": "G"}, "dong_sheet": "1"},
        {"ma": {"chu": "B"}, "ten": {"chu": "b"}, "cha": {"chu": "A"},
         "cap": "2", "nhom": {"chu": "G"}, "dong_sheet": "2"},
    ]
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem(dong, nguon="tong_hop")
    assert hd.HD_CHU_TRINH in e.value.ten, e.value.ten
    # ⛔ đếm chữ: chu trình báo ĐÚNG MỘT lần *(⛔ một lần mỗi nút của vòng)*.
    assert sum(1 for t, _ in e.value.loi if t == hd.HD_CHU_TRINH) == 1


def test_C4_B2_khong_chu_trinh_tren_anh_THAT__Đ5_chieu_kia():
    """`Đ5` chiều kia: ảnh thật ⛔ chu trình ⇒ phép dò ⛔ báo oan."""
    assert hd.HD_CHU_TRINH not in _doc_atl_ten()


# ── C4-B3 · cha vắng + cấp nhảy ─────────────────────────────────────────────
def test_C4_B3_cha_vang_loi_HD_CHA_VANG():
    """Cha trỏ mã ⛔ có ⇒ `HD_CHA_VANG`."""
    dong = [
        {"ma": {"chu": "R"}, "ten": {"chu": "r"}, "cha": None,
         "cap": "1", "nhom": {"chu": "G"}, "dong_sheet": "1"},
        {"ma": {"chu": "C"}, "ten": {"chu": "c"}, "cha": {"chu": "MATKHONGCO"},
         "cap": "2", "nhom": {"chu": "G"}, "dong_sheet": "2"},
    ]
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem(dong, nguon="tong_hop")
    assert hd.HD_CHA_VANG in e.value.ten, e.value.ten
    assert any("MATKHONGCO" in c for t, c in e.value.loi if t == hd.HD_CHA_VANG)


def test_C4_B3_cap_nhay_con_cap_n_cong_2_loi_HD_CAP_NHAY():
    """Con cấp n+2 dưới cha cấp n ⇒ `HD_CAP_NHAY` *(cấp = độ sâu)*."""
    dong = [
        {"ma": {"chu": "R"}, "ten": {"chu": "r"}, "cha": None,
         "cap": "1", "nhom": {"chu": "G"}, "dong_sheet": "1"},
        {"ma": {"chu": "C"}, "ten": {"chu": "c"}, "cha": {"chu": "R"},
         "cap": "3", "nhom": {"chu": "G"}, "dong_sheet": "2"},   # nhảy 1→3
    ]
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem(dong, nguon="tong_hop")
    assert hd.HD_CAP_NHAY in e.value.ten, e.value.ten


def test_C4_B3_goc_khong_o_cap_1_cung_la_HD_CAP_NHAY():
    """Gốc *(⛔ cha)* ở cấp ≠ 1 là cùng bất biến *cấp = độ sâu* ⇒ `HD_CAP_NHAY`."""
    dong = [
        {"ma": {"chu": "R"}, "ten": {"chu": "r"}, "cha": None,
         "cap": "2", "nhom": {"chu": "G"}, "dong_sheet": "1"},
    ]
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem(dong, nguon="tong_hop")
    assert hd.HD_CAP_NHAY in e.value.ten, e.value.ten


def test_C4_B3_cap_dung_thi_XANH__Đ5_chieu_kia():
    """`Đ5`: cây tối thiểu cấp đúng ⇒ ⛔ đỏ nhầm."""
    dong = [
        {"ma": {"chu": "R"}, "ten": {"chu": "r"}, "cha": None,
         "cap": "1", "nhom": {"chu": "G"}, "dong_sheet": "1"},
        {"ma": {"chu": "C"}, "ten": {"chu": "c"}, "cha": {"chu": "R"},
         "cap": "2", "nhom": {"chu": "G"}, "dong_sheet": "2"},
    ]
    cay = hd.kiem(dong, nguon="tong_hop")
    assert cay.con_cua("R") == ("C",) and cay.la("C") is True


# ── mã trùng + ô hỏng *(phòng thủ — khai trong BG)* ─────────────────────────
def test_ma_trung_loi_HD_MA_TRUNG():
    dong = [
        {"ma": {"chu": "X"}, "ten": {"chu": "x"}, "cha": None,
         "cap": "1", "nhom": {"chu": "G"}, "dong_sheet": "1"},
        {"ma": {"chu": "X"}, "ten": {"chu": "x2"}, "cha": None,
         "cap": "1", "nhom": {"chu": "G"}, "dong_sheet": "2"},
    ]
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem(dong, nguon="tong_hop")
    assert hd.HD_MA_TRUNG in e.value.ten, e.value.ten


def test_vo_o_la_loi_HD_HONG():
    """Vỏ ô ⛔ phải `{'chu': str}` ⇒ `HD_HONG` *(⛔ đoán)*."""
    dong = [
        {"ma": {"chu": "X", "so": 1}, "ten": {"chu": "x"}, "cha": None,
         "cap": "1", "nhom": {"chu": "G"}, "dong_sheet": "1"},
    ]
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem(dong, nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


def test_tap_rong_la_HD_HONG_khong_xanh_tren_tap_rong():
    """`Đ3`: 0 nút ⇒ NỔ, ⛔ "cây sạch"."""
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem([], nguon="rong")
    assert hd.HD_HONG in e.value.ten


# ── Mapping Master — đối chiếu (⛔ hoà giải) ─────────────────────────────────
def test_doc_mm_73_ma_va_chenh_voi_ATL_la_NCF():
    """MM `73` mã; `ATL − MM = {NCF}` *(`BG-107`)* — chỉ LIỆT KÊ, ⛔ hoà giải."""
    van_mm = (GOC / ANH_MM).read_text(encoding="utf-8")
    # doc_mm đọc qua đường dẫn — ở đây dùng mặc định *(ảnh gói == DT3, đã ghim)*.
    mm = hd.doc_mm()
    assert len(mm) == MONG_MM, f"⛔ mong {MONG_MM} mã MM, đo {len(mm)}"
    atl = {n.ma for n in hd.doc_tep().nut}
    assert sorted(atl - set(mm)) == MONG_CHENH
    assert sorted(set(mm) - atl) == []        # MM ⊆ ATL
    assert van_mm  # ảnh đọc được


def _doc_atl_ten() -> frozenset[str]:
    """Tập tên lỗi khi nạp ảnh THẬT — rỗng nếu sạch *(dùng cho `Đ5` chiều kia)*."""
    try:
        _doc_atl()
        return frozenset()
    except hd.LoiHD as e:          # pragma: no cover — ảnh thật phải sạch
        return e.ten


# ════════════════════════════════════════════════════════════════════════════
# Vòng sửa sau R1 (KQ-124) — `C4-R1-01` · `C4-R1-02` · `C4-R1-03`
# ════════════════════════════════════════════════════════════════════════════
def _dong_tot(**ghi_de):
    """Một dòng ATL hợp lệ *(gốc cấp 1)*; `ghi_de` thay đúng một ô để cô lập lỗi."""
    d = {"ma": {"chu": "R"}, "ten": {"chu": "r"}, "cha": None,
         "cap": "1", "nhom": {"chu": "G"}, "dong_sheet": "1"}
    d.update(ghi_de)
    return d


def _mm_van(*hd_codes: str) -> str:
    """Văn bản ảnh MM TỔNG HỢP từ các `hd_code` cho trước *(⛔ chạm hệ tệp)*."""
    return json.dumps({"bang": hd.BANG_MM,
                       "dong": [{"hd_code": {"chu": c}} for c in hd_codes]})


# ── C4-R1-01 · mọi lối đổi chuỗi→số / JSON mang TÊN, ⛔ `ValueError` trơn ─────
@pytest.mark.parametrize("cap_xau", ["²", "١"])
def test_C4_R1_01_cap_isdigit_ngoai_ASCII_la_HD_HONG_khong_ValueError(cap_xau):
    """`'²'`(ⁿ) ⇒ `int()` NÉM · `'١'`(Ả Rập) ⇒ `int()` lặng lẽ =1: cả hai
    `isdigit()`=True. ⛔ `ValueError` trơn, ⛔ nhận oan — phải `HD_HONG` có tên
    *(WO-122: lỗi cây có TÊN; `_so` kèm `isascii()`)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem([_dong_tot(cap=cap_xau)], nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


@pytest.mark.parametrize("tt_xau", ["abc", None])
def test_C4_R1_01_thu_tu_hong_la_HD_HONG_khong_ValueError(tt_xau):
    """`thu_tu` hỏng ⇒ `HD_HONG` *(⛔ `int(...)` trơn: `'abc'`→`ValueError`,
    `None`→`TypeError`)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem([_dong_tot(thu_tu=tt_xau)], nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


def test_C4_R1_01_thu_tu_tot_duoc_dung_lam_khoa_sap():
    """`Đ5` chiều kia: `thu_tu` hợp lệ *(⛔ vị trí dòng)* phải được tôn trọng khi sắp."""
    dong = [_dong_tot(ma={"chu": "R"}, cha=None, cap="1", thu_tu=9, dong_sheet="1"),
            _dong_tot(ma={"chu": "C"}, cha={"chu": "R"}, cap="2", thu_tu=1,
                      dong_sheet="2")]
    cay = hd.kiem(dong, nguon="tong_hop")
    assert tuple(n.ma for n in cay.nut) == ("C", "R")   # sắp theo thu_tu 1 < 9


def test_C4_R1_01_doc_van_ban_JSON_hong_la_HD_HONG():
    """ATL: JSON hỏng ⇒ `HD_HONG` *(⛔ `JSONDecodeError` trơn)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.doc_van_ban("{ ⛔ khong phai JSON", nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


def test_C4_R1_01_doc_mm_van_ban_JSON_hong_la_HD_HONG():
    """MM: JSON hỏng ⇒ `HD_HONG` *(⛔ `JSONDecodeError` trơn)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.doc_mm_van_ban("{ ⛔ khong phai JSON", nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


# ── C4-R1-02 · ba nhánh `raise` của `doc_mm` được CHỨNG MINH ĐỎ (Đ5) ─────────
def test_C4_R1_02_doc_mm_ma_trung_la_HD_MA_TRUNG():
    """Ảnh MM hai dòng cùng mã ⇒ `HD_MA_TRUNG` *(giết M27: `n>=2`)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.doc_mm_van_ban(_mm_van("GI | Gross", "GI | Gross 2"), nguon="tong_hop")
    assert hd.HD_MA_TRUNG in e.value.ten, e.value.ten


def test_C4_R1_02_doc_mm_0_ma_la_HD_HONG_khong_xanh_tren_tap_rong():
    """Ảnh MM 0 dòng ⇒ `HD_HONG` *(giết M28 + `Đ3`: ⛔ đối chiếu trên tập rỗng)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.doc_mm_van_ban(_mm_van(), nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


def test_C4_R1_02_doc_mm_hd_code_rong_la_HD_HONG():
    """`hd_code` rỗng ⇒ `HD_HONG` *(nhánh thứ ba của `doc_mm`)*."""
    van = json.dumps({"bang": hd.BANG_MM, "dong": [{"hd_code": {"chu": ""}}]})
    with pytest.raises(hd.LoiHD) as e:
        hd.doc_mm_van_ban(van, nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


def test_C4_R1_02_doc_mm_van_ban_hop_le_tach_ma__Đ5_chieu_kia():
    """`Đ5` chiều kia: ảnh MM hợp lệ ⇒ trả đúng mã, ⛔ đỏ oan *(lõi == `doc_mm`)*."""
    assert hd.doc_mm_van_ban(_mm_van("GI | Gross", "NCF | Net"),
                             nguon="tong_hop") == ("GI", "NCF")


# ── C4-R1-03 · nhánh HD_HONG của `kiem` (cấp sai kiểu/giá trị · cột lạ) ──────
@pytest.mark.parametrize("cap_xau", [0, True, -1])
def test_C4_R1_03_cap_sai_la_HD_HONG(cap_xau):
    """`cap` = 0 / `True`(bool) / âm ⇒ `HD_HONG` *(giết M22 `cap=0`, M23 `cap=True`
    — cả hai SỐNG ở R1: `cap=0` nhận ⇒ đổi tên sang `HD_CAP_NHAY`, ⛔ `HD_HONG`)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem([_dong_tot(cap=cap_xau)], nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten


def test_C4_R1_03_cot_la_la_HD_HONG():
    """Cột lạ ngoài `COT`(+`thu_tu`) ⇒ `HD_HONG` *(giết M26: bỏ `if thua`)*."""
    with pytest.raises(hd.LoiHD) as e:
        hd.kiem([_dong_tot(cot_khong_co_trong_COT="x")], nguon="tong_hop")
    assert hd.HD_HONG in e.value.ten, e.value.ten
