"""H6 — `tools/do_hd2.py --goi WP-C3b`: SO.CFA1 Y/H/Q/M ↔ đáp án 410 từng ô *(ISP 3.1.2 · Step 20 · WO-188)*.

Chuỗi: GL bản sao CF *(`gl_cf_dau_vao.json`)* → `tinh_gl` *(BR/BS)* → `cfa1_daily` trên trục
`truc_ngay(IX.PER, ngày đọc)` → `cuon_ky` *(Y/H/Q/M theo `ky_cua`)* → so TỪNG Ô với `cfa1_yhqm.json`.
Công thức 410 *(SA FORMULA 18/11)*: lá = `SUMIFS(Daily!hàng, Daily!$1:$1, năm, Daily!$2|$3|$4, H|Q|M)`,
cha = `sum(con)`. ⛔ 411 *(CFA3 Daily — DT5 LOẠI khỏi đóng băng, ISP Step 15)*.

  · **AC-2 · H6-B2** — ảnh thật: ô so = MẪU SỐ khai trước; 0 lệch ngoài tên; lệch có tên = MONG.
  · **Đ3** — đáp án rỗng ⇒ ĐỎ. **Đ5** — MONG khác ⇒ ĐỎ cả hai chiều; một ô +1e-12 ⇒ ĐỎ đúng ô ấy.
  · **AC-3** — IX.PER đọc TỪ KHO *(C6)*; kho chưa khai ⇒ ĐỎ *(⛔ rơi về ngày tạm)*; 20 mã KPI = H5.
  · ⛔ vòng tròn — xoá giá trị đáp án ⇒ lưới engine Y NGUYÊN.
"""
from __future__ import annotations

import copy
import dataclasses
import json
import pathlib
import sys
from datetime import date
from decimal import Decimal as D

import psycopg
import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.cau_hinh import ky  # noqa: E402
from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2  # noqa: E402

NGUON_PER = "bai-test-h6:ISP-3.1.2-Step20 (IX.PER kho = 21/10, C6)"


def _lich(ngay_dau=date(2024, 10, 21)):
    return ky.LichKy(nguon=NGUON_PER, ngay_dau=ngay_dau, luat=ky.LUAT_A)


@pytest.fixture(scope="module")
def nguon():
    return (do_hd2.nap_anh(do_hd2.ANH_GL_CF), do_hd2.nap_anh(do_hd2.ANH_YHQM),
            do_hd2.nap_fx(), do_hd2.nap_cay())


@pytest.fixture(scope="module")
def tq_that(nguon):
    return do_hd2.so_sanh_c3b(*nguon, _lich(), do_hd2.mong_c3b_mac_dinh())


def _chu(x):
    return x["chu"] if isinstance(x, dict) else x


# ── AC-2 · H6-B2 ─────────────────────────────────────────────────────────────────

def test_H6_B2_anh_that_DAT_mau_so_khai_truoc(tq_that):
    assert tq_that.phan_xu.dat, tq_that.phan_xu.ly_do
    # Đ4: 370 hàng × 57 kỳ = 21.090 ô lưới = ô so + ô KPI + ô '-' + ô kỳ-không-ngày
    assert do_hd2.MONG_C3B_TONG_O == 5 * 54 * (57 - 14) - 25 == 11585
    assert tq_that.tong_o == do_hd2.MONG_C3B_TONG_O == tq_that.khop and tq_that.lech == []
    assert tq_that.o_kpi == do_hd2.MONG_C3B_O_KPI == 5 * 20 * 57
    assert tq_that.o_loi == 25
    assert tq_that.o_ky_khong_ngay == do_hd2.MONG_C3B_O_KY_KHONG_NGAY == 5 * 54 * 14
    assert tq_that.tong_o + tq_that.o_kpi + tq_that.o_loi + tq_that.o_ky_khong_ngay == 370 * 57


def test_H6_B2_o_khac_0_va_lech_co_ten_dung_MONG(tq_that):
    h = tq_that.hd2_cong
    # Đ4: "ô ≠ 0" = ô SO được mà đáp án ≠ 0 *(⛔ đếm ô KPI/'-')* — bằng chứng dương, ⛔ xanh trên 0
    assert h["o_so_khac_0"] == do_hd2.MONG_C3B_O_SO_KHAC_0 and h["o_so_khac_0"] > 0
    ct = tq_that.lech_co_ten
    assert ct["thieu_tien_te_D"] == sorted(do_hd2.MONG_C3A_THIEU_D)     # cùng feed H5
    assert ct["hd_ngoai_cay"] == do_hd2.MONG_C3A_HD_NGOAI_CAY
    assert ct["hd_khac_hoa_thuong"] == 5 and ct["dong_nhan_cha"] == 0
    # trục IX.PER 21/10 ⇒ dòng sổ 20/10 rơi khỏi trục — đo: 0 dòng (ngày sổ nhỏ nhất 2024-10-21)
    assert ct["dong_ngoai_truc"] == 0
    # kỳ ⛔ có ngày nào trên trục: đáp án ⛔ được có ô SO-được ≠ 0 ở đó (errata ㉑ — ⛔ "0 đã chốt")
    assert ct["o_khac_0_ky_khong_ngay"] == 0


def test_H6_B2_truc_ky_nam_tu_du_lieu_va_ngay_dau_IX_PER(tq_that):
    t = tq_that.hd2_cong["truc"]
    assert t["ngay_dau"] == "2024-10-21" and t["nguon_ngay_dau"] == NGUON_PER
    assert t["den"] == "2026-11-18" and t["so_ngay"] == 759
    assert t["nam"] == [2024, 2025, 2026] and t["so_ky"] == 57
    assert t["ky_khong_ngay"] == ["2024H1", "2024Q1", "2024Q2", "2024Q3"] + [
        f"2024M{m:02d}" for m in range(1, 10)] + ["2026M12"]


def test_H6_B2_hd2_cong_tep_THEM_goi_C3b_giu_nguyen_C2_C3a():
    j = json.loads(do_hd2.RA_CONG.read_text(encoding="utf-8"))
    assert j["goi"] == "WP-C2" and j["tong_o"] == do_hd2.MONG_TONG_O
    assert j["WP-C3a"]["tong_o"] == j["WP-C3a"]["khop"] == 205175
    c = j["WP-C3b"]
    assert c["goi"] == "WP-C3b" and c["dat"] is True
    assert c["tong_o"] == c["mong_tong_o"] == c["khop"] == 11585
    assert "411" in c["loai_tru"]


def test_H6_Đ3_dap_an_rong_thi_DO(nguon):
    vao, da, fx, cay = nguon
    tq = do_hd2.so_sanh_c3b(vao, dict(da, dong=[]), fx, cay, _lich(), do_hd2.mong_c3b_mac_dinh())
    assert not tq.phan_xu.dat


def test_H6_Đ5_mot_o_dap_an_lech_thi_DO_dung_o_ay(nguon):
    vao, da, fx, cay = nguon
    da2 = copy.deepcopy(da)
    r = next(r for r in da2["dong"] if _chu(r["le"]) == "SGO1" and _chu(r["ma_hd"]) == "GI"
             and _chu(r["ky"]) == "2025Q3")
    r["gt"] = str(D(r["gt"]) + D("1e-12"))
    tq = do_hd2.so_sanh_c3b(vao, da2, fx, cay, _lich(), do_hd2.mong_c3b_mac_dinh())
    assert not tq.phan_xu.dat
    assert [(x["le"], x["ma"], x["ky"]) for x in tq.lech] == [("SGO1", "GI", "2025Q3")]


def test_H6_Đ5_mong_khac_thi_DO_ca_hai_chieu(nguon):
    m = do_hd2.mong_c3b_mac_dinh()
    for mm in (dataclasses.replace(m, thieu_D=m.thieu_D[1:]),
               dataclasses.replace(m, hd_khac_hoa=m.hd_khac_hoa + 1),
               dataclasses.replace(m, tong_o=m.tong_o + 1),
               dataclasses.replace(m, o_so_khac_0=m.o_so_khac_0 - 1)):
        assert not do_hd2.so_sanh_c3b(*nguon, _lich(), mm).phan_xu.dat


def test_H6_Đ5_o_khac_0_o_ky_khong_ngay_thi_DO(nguon):
    """Đáp án có số ở kỳ ⛔ ngày nào trên trục *(vd 2026M12 chưa tới)* ⇒ ĐỎ, ⛔ coi khớp 0."""
    vao, da, fx, cay = nguon
    da2 = copy.deepcopy(da)
    da2["dong"].append({"le": {"chu": "GROUP"}, "ma_hd": {"chu": "GI"}, "ky": {"chu": "2026M12"},
                        "gt": "0.5"})
    tq = do_hd2.so_sanh_c3b(vao, da2, fx, cay, _lich(), do_hd2.mong_c3b_mac_dinh())
    assert not tq.phan_xu.dat and tq.lech_co_ten["o_khac_0_ky_khong_ngay"] == 1


def test_H6_B2_dot_bien_mot_dong_so_do_dung_la_to_tien_x_4_ky(nguon):
    vao, da, fx, cay = nguon
    vao2 = copy.deepcopy(vao)
    nut = {n.ma: n for n in cay.nut}
    nhan = {f"{n.ma} | {n.ten}": n.ma for n in cay.nut}
    r = next(r for r in vao2["dong"] if _chu(r["le"]) == "SGO2" and r["E"] is not None
             and _chu(r["D"]) and nhan.get(_chu(r["hd_final"])) in nut
             and cay.la(nhan[_chu(r["hd_final"])]) and nut[nhan[_chu(r["hd_final"])]].cha)
    ma = nhan[_chu(r["hd_final"])]
    chuoi = [ma]
    while nut[chuoi[-1]].cha is not None:
        chuoi.append(nut[chuoi[-1]].cha)
    r["E"] = str(D(r["E"]) + 1)
    tq = do_hd2.so_sanh_c3b(vao2, da, fx, cay, _lich(), do_hd2.mong_c3b_mac_dinh())
    n = date(1899, 12, 30).toordinal() + int(r["ngay"])
    k = ky.ky_cua(date.fromordinal(n))
    kys = {f"{k.nam}", f"{k.nam}H{k.nua}", f"{k.nam}Q{k.quy}", f"{k.nam}M{k.thang:02d}"}
    mong = {(kh, m, x) for kh in ("GROUP", "SGO2") for m in chuoi for x in kys}
    assert {(x["le"], x["ma"], x["ky"]) for x in tq.lech} == mong and not tq.phan_xu.dat


def test_H6_dung_sai_theo_khoi_co_so_do():
    ds = do_hd2.DUNG_SAI_C3B
    assert set(ds) == {"la", "cha"}
    for k, v in do_hd2.DO_C3B_MAX_LECH.items():
        assert ds[k].rtol == 0 and ds[k].atol >= 10 * v


def test_H6_vong_tron__xoa_gia_tri_dap_an_luoi_y_nguyen(nguon, tq_that):
    vao, da, fx, cay = nguon
    da0 = copy.deepcopy(da)
    for r in da0["dong"]:
        r["gt"] = "0"
    tq = do_hd2.so_sanh_c3b(vao, da0, fx, cay, _lich(), do_hd2.mong_c3b_mac_dinh())
    assert tq.luoi == tq_that.luoi and not tq.phan_xu.dat


# ── AC-3 · IX.PER từ KHO · KPI nhất quán với H5 ─────────────────────────────────

def test_H6_AC3_IX_PER_doc_tu_kho_C6(nguon):
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bo-test-h6", ngay_dau="2024-10-21", luat="A", nguon=NGUON_PER)
        lich = chc.doc_per(c)
    assert lich.ngay_dau == date(2024, 10, 21)
    tq = do_hd2.so_sanh_c3b(*nguon, lich, do_hd2.mong_c3b_mac_dinh())
    assert tq.phan_xu.dat, tq.phan_xu.ly_do


def test_H6_AC3_IX_PER_khac_ngay_dau_khai_thi_DO(nguon):
    tq = do_hd2.so_sanh_c3b(*nguon, _lich(date(2024, 10, 20)), do_hd2.mong_c3b_mac_dinh())
    assert not tq.phan_xu.dat
    assert any("ngày đầu" in x for x in tq.phan_xu.ly_do)


def test_H6_AC3_kho_chua_khai_IX_PER_thi_DO_khong_roi_ve_ngay_tam(monkeypatch):
    def _nem(_c):
        raise chc.ChuaKhai("IX.PER chua co")
    monkeypatch.setattr(chc, "doc_per", _nem)
    tq = do_hd2.chay_wp_c3b(dsn=dsn_test())
    assert not tq.phan_xu.dat and any("IX.PER" in x for x in tq.phan_xu.ly_do)


def test_H6_AC3_KPI_nhat_quan_H5():
    assert do_hd2.MA_KPI_C3B is do_hd2.MA_KPI and len(do_hd2.MA_KPI) == 20
