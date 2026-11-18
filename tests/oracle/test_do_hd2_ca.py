"""H4 — `tools/do_hd2.py --goi WP-C2`: parity CA.GL ↔ đáp án 406 mọi kỳ *(ISP 3.1.2 · Step 13)*.

Bài dẫn từ mục 6 + 8 của Step 13 *(WO-132)*:
  · **H4-B1** — chạy WP-C2 trên ảnh thật: số ô so > 0 và = số ô ĐÁP ÁN so được; cả 8 cột BM…BT
    khớp trong dung sai; lệch CÓ TÊN đúng MONG *(6 hàng thiếu D · 4 hàng itl_id #N/A · kỳ vắng 406
    · 0 tháng thiếu tỷ giá)*; 0 lệch NGOÀI tên.
  · **H4-B2** — đáp án RỖNG ⇒ ĐỎ `0 ô` *(Đ3: mẫu số 0 là KẾT QUẢ)*.
  · **H4-B3** — MONG lệch khai TRƯỚC; khác ⇒ ĐỎ CẢ HAI CHIỀU *(Đ5)*: (a) một ô lệch NGOÀI tên ⇒
    ĐỎ; (b) tập lệch-có-tên THỰC ≠ MONG ⇒ ĐỎ.

⭐ Số dư đầu kỳ gõ tay ở hàng 24 *(5 ô — `SoDuDau`)* được GIEO từ ảnh đầu vào; thiếu nó thì BM·BN·
BQ·BT lệch ~56.84e9 bVND từ ds24 *(đo 18/11)* — bài B1 chứng cả 8 cột về 0 nhờ gieo.
"""
from __future__ import annotations

import dataclasses
import pathlib
import sys
from decimal import Decimal as D

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from tools import do_hd2  # noqa: E402


# ── trợ giúp dựng ảnh nhỏ cho B2/B3 (hình y ảnh đóng băng thật) ──────────────────

def _chu(s):
    return {"chu": s}


def _hang_vao(ds, ky, itl, d, e, f):
    return {"dong_sheet": str(ds), "ky": str(ky), "itl_id": _chu(itl),
            "D": (_chu(d) if d is not None else None),
            "E": (str(e) if e is not None else None),
            "F": (str(f) if f is not None else None)}


def _hang_dap_an(ds, ky, itl, d, **cot):
    r = {"dong_sheet": str(ds), "ky": str(ky), "itl_id": _chu(itl),
         "D": (_chu(d) if d is not None else None)}
    for c in ("BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT"):
        r[c] = (str(cot[c]) if cot.get(c) is not None else None)
    return r


def _anh_vao(dong, so_du_dau=()):
    return {"dong": dong, "phu": {"itl_id_lech": {"dong": []},
                                  "so_du_dau": {"dong": list(so_du_dau)}}}


def _fx(thang=(202501,)):
    return {t: {"USD": D("25000"), "SGD": D("18000"), "COP": D("6"),
                "VND": D("1"), "HKD": D("3200")} for t in thang}


# ── H4-B1 · ảnh thật ────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def tq_that():
    return do_hd2.chay_wp_c2()


def test_H4_R1_02_tong_o_bang_8_nhan_dong_so_khong_tu_tham_chieu(tq_that):
    """⭐ De-tautology *(H4-R1-02)*: mẫu số parity là HẰNG khai TRƯỚC + dòng feed độc lập, ⛔ so
    `tong_o` với chính `so_o_dap_an_so_duoc` *(hai biến tăng cùng chỗ ⇒ luôn bằng — Đ2)*."""
    assert tq_that.tong_o > 0
    assert tq_that.hd2_cong["dong_so"] == do_hd2.MONG_DONG_SO == 7877
    assert tq_that.tong_o == 8 * tq_that.hd2_cong["dong_so"] == do_hd2.MONG_TONG_O == 63016
    assert tq_that.so_dong_dap_an == do_hd2.MONG_SO_DONG_DAP_AN == 7883
    assert tq_that.so_o_dap_an_so_duoc == do_hd2.MONG_TONG_O


def test_H4_B1_ca_8_cot_khop_trong_dung_sai(tq_that):
    assert tq_that.khop == tq_that.tong_o, f"{tq_that.tong_o - tq_that.khop} ô lệch ngoài tên"
    assert tq_that.lech == [], tq_that.lech[:5]
    assert tq_that.phan_xu.dat, tq_that.phan_xu.mot_dong


def test_H4_B1_lech_co_ten_dung_MONG(tq_that):
    lct = tq_that.lech_co_ten
    assert sorted(lct["thieu_tien_te_D"]) == list(do_hd2.MONG_THIEU_D)
    assert sorted(lct["itl_id_na"]) == list(do_hd2.MONG_ITL_NA)
    assert set(lct["ky_vang_406"]) == {str(k) for k in do_hd2.MONG_KY_VANG}
    # 0 tháng thiếu tỷ giá trong dải so được — Đ3: khai mẫu số (số tháng đã phủ)
    assert lct["thang_thieu_ty_gia"] == []
    assert tq_that.mau_so_thang > 0


# ── H4-B2 · đáp án rỗng ⇒ ĐỎ 0 ô (Đ3) ───────────────────────────────────────────

def test_H4_B2_dap_an_rong_thi_DO_0_o():
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", None, 1000)])
    tq = do_hd2.so_sanh(vao, {"dong": []}, _fx(), {202501: 1}, do_hd2.mong_mac_dinh())
    assert tq.tong_o == 0
    assert not tq.phan_xu.dat
    assert any("0" in l for l in tq.phan_xu.ly_do), tq.phan_xu.ly_do


# ── H4-B3 · MONG khai trước; khác ⇒ ĐỎ cả hai chiều (Đ5) ─────────────────────────

def test_H4_B3a_mot_o_lech_NGOAI_ten_thi_DO():
    # VND Nợ 1000 @ rate 1 ⇒ BO = 1000/1e9 = 1e-6; đáp án CỐ TÌNH ghi sai BO.
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", 1000, None)])
    da = [_hang_dap_an(10, 202501, "ITL#1", "VND", BM=1000, BN=D("0.00000004"),
                       BO=D("0.000999"), BP=0, BQ=D("0.000001"),  # BO sai (0.000999 ≠ 1e-6)
                       BR=D("0.00000004"), BS=0, BT=D("0.00000004"))]
    tq = do_hd2.so_sanh(vao, {"dong": da}, _fx(), {202501: 1}, do_hd2.mong_mac_dinh())
    assert not tq.phan_xu.dat
    assert tq.lech, "phải có ít nhất một ô lệch ngoài tên"
    assert any(x["cot"] == "BO" for x in tq.lech)


def test_H4_B3b_tap_lech_co_ten_KHAC_mong_thi_DO():
    # dữ liệu khớp sạch, 0 lệch có tên; nhưng MONG đòi 1 hàng thiếu D ⇒ lệch mong ⇒ ĐỎ.
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", 1000, None)])
    da = [_hang_dap_an(10, 202501, "ITL#1", "VND", BM=1000, BN=D("0.00000004"),
                       BO=D("0.000001"), BP=0, BQ=D("0.000001"),
                       BR=D("0.00000004"), BS=0, BT=D("0.00000004"))]
    mong = do_hd2.Mong(thieu_D=(999,), itl_na=(), ky_vang={}, thang_thieu_ty_gia=())
    tq = do_hd2.so_sanh(vao, {"dong": da}, _fx(), {202501: 1}, mong)
    assert not tq.phan_xu.dat
    assert any("thieu_tien_te_D" in l or "lệch có tên" in l or "mong" in l.lower()
               for l in tq.phan_xu.ly_do), tq.phan_xu.ly_do


def test_H4_B1_THIEU_gieo_so_du_dau_thi_DO_tu_ds24():
    """⭐ Chứng cổng: số dư đầu kỳ GÕ TAY là load-bearing. Bỏ `so_du_dau` khỏi ảnh đầu vào ⇒
    BM·BN·BQ·BT lệch từ ds24 *(đo 18/11: ~56.84e9 bVND)* ⇒ hàng NGHÌN ô lệch NGOÀI tên ⇒ ĐỎ.
    *(Đ5: phá nguồn → chạy → xem nó cắn; ảnh trả nguyên vì đọc bản sao.)*"""
    vao = do_hd2.nap_anh(do_hd2.ANH_DAU_VAO)
    vao["phu"] = dict(vao["phu"])
    vao["phu"]["so_du_dau"] = {"dong": []}            # ⛔ gieo số dư đầu kỳ
    tq = do_hd2.so_sanh(vao, do_hd2.nap_anh(do_hd2.ANH_DAP_AN), do_hd2.nap_fx(),
                        do_hd2.nap_phan_bo(), do_hd2.mong_mac_dinh())
    assert not tq.phan_xu.dat
    assert len(tq.lech) > 1000, len(tq.lech)
    assert all(int(x["dong_sheet"]) >= 24 for x in tq.lech)      # khớp sạch TRƯỚC ds24
    assert {x["cot"] for x in tq.lech} <= {"BM", "BN", "BQ", "BT"}  # chỉ cột lũy kế/đánh giá lại


def test_H4_B3_khop_sach_khi_dung_mong_thi_DAT():
    """Chiều DƯƠNG của Đ5: khớp sạch + lệch-có-tên = mong ⇒ ĐẠT (cổng ⛔ xanh mù)."""
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", 1000, None)])
    da = [_hang_dap_an(10, 202501, "ITL#1", "VND", BM=1000, BN=D("0.00000004"),
                       BO=D("0.000001"), BP=0, BQ=D("0.000001"),
                       BR=D("0.00000004"), BS=0, BT=D("0.00000004"))]
    mong = do_hd2.Mong(thieu_D=(), itl_na=(), ky_vang={}, thang_thieu_ty_gia=())
    tq = do_hd2.so_sanh(vao, {"dong": da}, _fx(), {202501: 1}, mong)
    assert tq.phan_xu.dat, tq.phan_xu.mot_dong
    assert tq.tong_o == 8 and tq.khop == 8


# ── Vòng sửa sau R1 (KQ-134) — H4-R1-01/02/03 trên ẢNH THẬT ─────────────────────
# Mỗi bài ĐỎ-trước: chứng cổng CŨ (atol 1e-6 chung / mẫu số tự đếm / no-op chỉ lời) XANH, cổng
# MỚI ĐỎ. Đột biến chạy trên BẢN SAO ảnh đáp án trong bộ nhớ *(⛔ chạm fixture trên đĩa)*.

@pytest.fixture(scope="module")
def that():
    """Ảnh thật + fx + phân bổ — nạp MỘT lần cho mọi bài đột biến."""
    return (do_hd2.nap_anh(do_hd2.ANH_DAU_VAO), do_hd2.nap_anh(do_hd2.ANH_DAP_AN),
            do_hd2.nap_fx(), do_hd2.nap_phan_bo())


def _ban_sao_da(da):
    return {"dong": [dict(r) for r in da["dong"]]}


def _chay(vao, da, fx, pb, mong=None):
    return do_hd2.so_sanh(vao, da, fx, pb, mong or do_hd2.mong_mac_dinh())


def _mong_atol_cu_bo():
    """`mong_mac_dinh` nhưng BO về `atol 1e-6` CŨ — để chứng ngưỡng load-bearing (red-first)."""
    dsc = dict(do_hd2.DUNG_SAI_COT)
    dsc["BO"] = do_hd2.DungSaiCot(atol=D("1e-6"))
    return dataclasses.replace(do_hd2.mong_mac_dinh(), dung_sai=dsc)


def _dat_o(da, ds, cot, val):
    for r in da["dong"]:
        if int(do_hd2._so(r["dong_sheet"])) == ds:
            r[cot] = val
            return
    raise AssertionError(f"⛔ thấy ds {ds}")


# H4-R1-01 — dung sai THEO CỘT ────────────────────────────────────────────────────

def test_H4_R1_01_BO_lech_9e_7_thi_DO__atol_cu_thi_XANH(that):
    """`BO +9e-7` *(900 VND)* ở hàng |BO| LỚN nhất *(rtol áp đảo)*: dung sai cột ⇒ ĐỎ;
    `atol 1e-6` cũ ⇒ XANH hoàn toàn *(ngưỡng load-bearing — Đ5)*."""
    vao, da, fx, pb = that
    ds_max, bo_max = None, D(0)
    for r in da["dong"]:
        v = do_hd2._so(r.get("BO"))
        if v is not None and abs(v) > abs(bo_max):
            bo_max, ds_max = v, int(do_hd2._so(r["dong_sheet"]))
    da2 = _ban_sao_da(da)
    _dat_o(da2, ds_max, "BO", str(bo_max + D("9e-7")))
    tq = _chay(vao, da2, fx, pb)
    assert not tq.phan_xu.dat
    assert any(x["cot"] == "BO" and int(x["dong_sheet"]) == ds_max for x in tq.lech), tq.lech[:3]
    # red-first: atol 1e-6 cũ ⇒ ô này khớp ⇒ cổng XANH
    assert _chay(vao, da2, fx, pb, _mong_atol_cu_bo()).phan_xu.dat


def test_H4_R1_01_BO_lech_1_VND_o_hang_gan_0_thi_DO__atol_cu_thi_XANH(that):
    """`BO +1e-9` *(1 VND)* ở hàng `BO = 0` *(atol quyết định)*: cột atol 1e-12 ⇒ ĐỎ; cũ ⇒ XANH."""
    vao, da, fx, pb = that
    ds0 = next(int(do_hd2._so(r["dong_sheet"])) for r in da["dong"]
               if do_hd2._so(r.get("BO")) == 0
               and int(do_hd2._so(r["dong_sheet"])) not in do_hd2.MONG_THIEU_D)
    da2 = _ban_sao_da(da)
    _dat_o(da2, ds0, "BO", str(D("1e-9")))
    tq = _chay(vao, da2, fx, pb)
    assert not tq.phan_xu.dat
    assert any(x["cot"] == "BO" and int(x["dong_sheet"]) == ds0 for x in tq.lech)
    assert _chay(vao, da2, fx, pb, _mong_atol_cu_bo()).phan_xu.dat


# H4-R1-02 — khoá MẪU SỐ ───────────────────────────────────────────────────────────

def test_H4_R1_02_xoa_cot_BO_BP_thi_DO(that):
    vao, da, fx, pb = that
    da2 = _ban_sao_da(da)
    for r in da2["dong"]:
        r["BO"] = None
        r["BP"] = None
    tq = _chay(vao, da2, fx, pb)
    assert not tq.phan_xu.dat
    assert tq.tong_o == do_hd2.MONG_TONG_O - 2 * do_hd2.MONG_DONG_SO == 47262
    assert any("mẫu số" in l for l in tq.phan_xu.ly_do), tq.phan_xu.ly_do


def test_H4_R1_02_xoa_100_o_BT_thi_DO(that):
    vao, da, fx, pb = that
    da2 = _ban_sao_da(da)
    n = 0
    for r in da2["dong"]:
        if (do_hd2._so(r.get("BT")) is not None
                and int(do_hd2._so(r["dong_sheet"])) not in do_hd2.MONG_THIEU_D):
            r["BT"] = None
            n += 1
            if n == 100:
                break
    tq = _chay(vao, da2, fx, pb)
    assert not tq.phan_xu.dat
    assert tq.tong_o == do_hd2.MONG_TONG_O - 100 == 62916


def test_H4_R1_02_xoa_hang_dap_an_cuoi_thi_DO(that):
    vao, da, fx, pb = that
    da2 = {"dong": [dict(r) for r in da["dong"][:-1]]}
    tq = _chay(vao, da2, fx, pb)
    assert not tq.phan_xu.dat
    assert tq.so_dong_dap_an == do_hd2.MONG_SO_DONG_DAP_AN - 1
    assert any("hàng đáp án" in l for l in tq.phan_xu.ly_do), tq.phan_xu.ly_do


def test_H4_R1_02_nhan_doi_hang_dap_an_thi_DO(that):
    vao, da, fx, pb = that
    da2 = {"dong": [dict(r) for r in da["dong"]] + [dict(da["dong"][0])]}
    tq = _chay(vao, da2, fx, pb)
    assert not tq.phan_xu.dat
    assert tq.so_dong_dap_an == do_hd2.MONG_SO_DONG_DAP_AN + 1


# H4-R1-03 — ô bỏ đếm được + no-op đo được ─────────────────────────────────────────

def test_H4_R1_03_o_dap_an_bo_bang_36_va_no_op_sach(tq_that):
    assert tq_that.o_dap_an_bo == 36                      # 6 hàng thiếu D × 6 ô khác rỗng
    assert tq_that.no_op_lech == []                        # BM·BQ·BT = hàng trên (6/6)
    assert tq_that.hd2_cong["o_dap_an_bo_hang_thieu_D"] == 36


def test_H4_R1_03_no_op_vo_thi_DO(that):
    """Đổi BM của hàng thiếu D *(ds4962)* khác hàng trên ⇒ no-op vỡ ⇒ ĐỎ *(trước chỉ là LỜI)*."""
    vao, da, fx, pb = that
    da2 = _ban_sao_da(da)
    cur = do_hd2._so(next(r for r in da2["dong"]
                          if int(do_hd2._so(r["dong_sheet"])) == 4962)["BM"])
    _dat_o(da2, 4962, "BM", str(cur + D("1")))
    tq = _chay(vao, da2, fx, pb)
    assert 4962 in tq.no_op_lech
    assert not tq.phan_xu.dat
    assert any("no-op" in l for l in tq.phan_xu.ly_do), tq.phan_xu.ly_do
