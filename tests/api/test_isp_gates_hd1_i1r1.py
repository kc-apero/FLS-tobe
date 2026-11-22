# -*- coding: utf-8 -*-
"""I1 vòng sửa R1 (`KQ-305`) — cổng `HD1_THANG` phán MỌI kỳ có ảnh (26), ⛔ chỉ 23 kỳ `dat_hd1`.

Hàm thuần `bc.doc_cong_tep_do` trên tệp THẬT đã commit (+ biến thể phá/dựng ở `tmp_path`). `MONG` khai
TRƯỚC (Đ5), mỗi số kèm NHÃN nó đếm gì (Đ4):
  26 = `tu_sinh.so_ky_co_anh` (kỳ CÓ ẢNH, H15) · 23 = `dat_hd1.mau_so.so_ky` (kỳ ĐO ĐƯỢC đủ hai vế:
  dòng ghép 1-1 + ô Final) · 5 = kỳ đạt · 3 kỳ `2026-09·10·11` chỉ ở `tu_sinh` — `tu_sinh.theo_ky` chỉ
  có `o·hd·mid·lech_*·o_loi`, ⛔ có vế *dòng ghép 1-1* ⇒ `khong_do_duoc` CÓ TÊN vế ấy.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from fls.repo import doc_bao_cao as bc

GOC = Path(__file__).resolve().parents[2]
TEP_THAT = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
MONG_DA_DO = "5 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh"
KY_MOI = ("2026-09", "2026-10", "2026-11")


def _that() -> dict:
    return json.loads(TEP_THAT.read_text(encoding="utf-8"))


def _cong(tmp_path: Path, d: dict):
    p = tmp_path / "voi_so_luong.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return {c.ma: c for c in bc.doc_cong_tep_do(p)}["HD1_THANG"]


def test_I1_R1_01_tep_that_mau_so_26_ky_co_anh_x_dat_y_do_duoc():
    c = {c.ma: c for c in bc.doc_cong_tep_do(TEP_THAT)}["HD1_THANG"]
    assert c.dat is False and c.da_do == MONG_DA_DO, c
    # ba kỳ mới ĐƯỢC NÓI TÊN cùng vế ⛔ đo được; ⛔ coi là đạt, ⛔ bỏ im lặng
    for k in KY_MOI:
        assert k in c.ly_do, c.ly_do
    assert "dòng ghép 1-1" in c.ly_do and "⛔ đo được" in c.ly_do and "3/26" in c.ly_do, c.ly_do


def test_I1_R1_01_tap_khong_rong_ba_ky_moi_la_chi_o_tu_sinh(tmp_path):
    d = _that()
    ky_ts, ky_cong = set(d["tu_sinh"]["theo_ky"]), set(d["dat_hd1"]["theo_ky"])
    assert (len(ky_ts), len(ky_cong)) == (26, 23) and tuple(sorted(ky_ts - ky_cong)) == KY_MOI


def test_I1_R1_01_khong_do_duoc_khong_phai_dat_khi_23_ky_deu_dat(tmp_path):
    """Mọi kỳ `dat_hd1` ĐẠT + 3 kỳ mới ⛔ đo được vế dòng ⇒ `dat=None` (⛔ True: Đ5), mẫu số 26."""
    d = _that()
    h = d["dat_hd1"]
    for v in h["theo_ky"].values():
        v["dat"] = True
    h["ky_dat"] = sorted(h["theo_ky"])
    h["so_ky_dat"] = len(h["ky_dat"])
    c = _cong(tmp_path, d)
    assert c.dat is None and c.da_do == "23 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh", c


def test_I1_R1_01_chieu_nguoc_ca_26_ky_do_duoc_va_dat_thi_dat(tmp_path):
    """Tệp mà `tu_sinh` chỉ phủ đúng 23 kỳ của `dat_hd1` và mọi kỳ đạt ⇒ `dat=True` (hai chiều, Đ5)."""
    d = _that()
    h, t = d["dat_hd1"], d["tu_sinh"]
    for v in h["theo_ky"].values():
        v["dat"] = True
    h["ky_dat"] = sorted(h["theo_ky"])
    h["so_ky_dat"] = len(h["ky_dat"])
    for k in KY_MOI:
        del t["theo_ky"][k]
    t["so_ky_co_anh"] = 23
    c = _cong(tmp_path, d)
    assert c.dat is True and c.da_do == "23 kỳ đạt / 23 kỳ đo được / 23 kỳ có ảnh", c


def test_I1_R1_01_ky_moi_o_lech_la_do_khong_phai_khong_do_duoc(tmp_path):
    d = _that()
    d["tu_sinh"]["theo_ky"]["2026-10"]["o"] = [7265, 7266]
    c = _cong(tmp_path, d)
    assert c.dat is False and "2026-10" in c.ly_do and "ô lệch" in c.ly_do, c.ly_do


@pytest.mark.parametrize("pha", [
    lambda d: d["tu_sinh"].__setitem__("so_ky_co_anh", 25),                     # số đếm ≠ danh sách
    lambda d: d["tu_sinh"]["theo_ky"].pop("2024-10"),                           # kỳ của dat_hd1 ⛔ có ảnh
    lambda d: d["tu_sinh"]["theo_ky"]["2026-09"].__setitem__("o", "x"),         # sai kiểu
])
def test_I1_R1_01_tu_sinh_tu_mau_thuan_hoac_sai_kieu_la_do_khong_do_duoc(tmp_path, pha):
    d = _that()
    pha(d)
    c = _cong(tmp_path, d)
    assert c.dat is None and "tu_sinh" in c.ly_do, c


def test_I1_R1_01_tep_khong_co_tu_sinh_thi_giu_mau_so_cu_CG1(tmp_path):
    """Khoá CG1 (tệp chỉ có `dat_hd1`): hành vi cũ — mẫu số = `dat_hd1.mau_so.so_ky`."""
    d = _that()
    del d["tu_sinh"]
    c = _cong(tmp_path, d)
    assert c.dat is False and c.da_do == "5/23 kỳ đạt", c


# ── I1-R1-02 · `ly_do` mang TÊN nhãn DT1b + số dòng theo kỳ đỏ ───────────────────────────────
def _voi_nhan(d: dict) -> dict:
    d = copy.deepcopy(d)
    h = d["dat_hd1"]
    h["tep_nhan"] = {"duong": "tmp/nhan.json", "co": True}
    h["theo_nhan"] = {"TONG_HOP_A": {"so_dong": 23, "van_tay_dong": "x", "da_ky": False, "cam_ky": False},
                      "KHOA_LECH_B": {"so_dong": 99, "van_tay_dong": "y", "da_ky": True, "cam_ky": False}}
    h["theo_ky"]["2026-07"]["co_nhan"] = 23
    h["theo_ky"]["2025-06"]["co_nhan"] = 3
    return d


def test_I1_R1_02_ly_do_mang_TEN_nhan_va_so_dong_khi_co_nhan(tmp_path):
    c = _cong(tmp_path, _voi_nhan(_that()))
    assert "TONG_HOP_A" in c.ly_do and "KHOA_LECH_B" in c.ly_do, c.ly_do
    assert "23 dòng" in c.ly_do and "99 dòng" in c.ly_do and "2026-07: 23 (23 có nhãn)" in c.ly_do, c.ly_do
    # mẫu `kỳ: số` của các tầng trên vẫn bóc đúng 18 kỳ đỏ, ⛔ nhãn lọt vào mẫu
    import re
    cap = re.findall(r"(\d{4}-\d{2}): (\d+)", c.ly_do)
    assert len(cap) == 18, cap


def test_I1_R1_02_thieu_tep_nhan_ghi_chua_co_nhan_co_ten(tmp_path):
    c = _cong(tmp_path, _that())
    assert "chưa có nhãn DT1b" in c.ly_do, c.ly_do
    assert "TONG_HOP" not in c.ly_do
