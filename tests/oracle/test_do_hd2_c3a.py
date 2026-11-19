"""H5 — `tools/do_hd2.py --goi WP-C3a`: SO.CFA1 Daily ↔ đáp án 409 từng ô *(ISP 3.1.2 · Step 16)*.

Nguồn ĐẦU VÀO *(orchestrator 18/11, đọc công thức SA của `Report I CFA1 Daily`)*: ô lá khối GROUP =
`SUMIFS(GL!BR, GL!A, ngày, GL!V, nhãn HD) − SUMIFS(GL!BS, …)`; khối LE thêm `GL!P = mã LE`; hàng
cha `=sum(con)`. ⇒ đầu vào = sheet `Report I General Ledger` CỦA BẢN SAO CF report, đóng băng ở
`gl_cf_dau_vao.json` *(A·D·E·F·P·R·V; ⛔ B:C)*; BR/BS do `tinh_gl` *(H4)* tính lại từ E/F + `ix_fx`
— ⛔ đọc BR/BS của sheet *(vòng tròn)*. Đáp án 409 CHỈ cấp giá trị mong + trục ngày.

  · **AC-2 / H5-B2** — ảnh thật: ô so > 0 và = MẪU SỐ khai trước; 0 lệch ngoài tên; lệch có tên = MONG.
  · **Đ3** — đáp án rỗng ⇒ ĐỎ.  **Đ5** — MONG khác ⇒ ĐỎ cả hai chiều.
  · **AC-3** — đột biến MỘT dòng sổ *(+1 VND)* ⇒ ĐỎ đúng ô lá ấy + mọi tổ tiên, ở GROUP và khối LE
    của dòng; dung sai theo khối có số đo.
  · **AC-4** — ⛔ vòng tròn: xoá giá trị đáp án ⇒ lưới engine Y NGUYÊN; đổi đầu vào ⇒ lưới đổi.
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
    return (do_hd2.nap_anh(do_hd2.ANH_GL_CF), do_hd2.nap_anh(do_hd2.ANH_CFA1),
            do_hd2.nap_fx(), do_hd2.nap_cay())


@pytest.fixture(scope="module")
def tq_that(nguon):
    return do_hd2.so_sanh_c3a(*nguon, _lich(), do_hd2.mong_c3a_mac_dinh())


def _chu(x):
    return x["chu"] if isinstance(x, dict) else x


# ── AC-2 · H5-B2 ─────────────────────────────────────────────────────────────────

def test_H5_B2_anh_that_DAT_mau_so_khai_truoc(tq_that):
    assert tq_that.phan_xu.dat, tq_that.phan_xu.ly_do
    # Đ3/Đ4: mẫu số = 5 khối × 54 mã so được × 760 ngày − 25 ô "-" của đáp án = 205.175
    assert do_hd2.MONG_C3A_TONG_O == 5 * 54 * 760 - 25 == 205175
    assert tq_that.tong_o == do_hd2.MONG_C3A_TONG_O
    assert tq_that.khop == tq_that.tong_o and tq_that.lech == []
    assert tq_that.o_kpi == do_hd2.MONG_C3A_O_KPI == 5 * 20 * 760
    assert tq_that.o_loi == 25


def test_H5_B2_lech_co_ten_dung_MONG(tq_that):
    ct = tq_that.lech_co_ten
    assert ct["thieu_tien_te_D"] == sorted(do_hd2.MONG_C3A_THIEU_D) and len(ct["thieu_tien_te_D"]) == 12
    assert ct["hd_ngoai_cay"] == do_hd2.MONG_C3A_HD_NGOAI_CAY
    assert sum(ct["hd_ngoai_cay"].values()) == 162
    assert ct["hd_khac_hoa_thuong"] == 5
    assert ct["dong_nhan_cha"] == 0 and ct["dong_ngoai_truc"] == 0
    assert tq_that.hd2_cong["dong_so"] == do_hd2.MONG_C3A_DONG_SO == 12385 - 12


def test_H5_B2_truc_ngay_20_10_va_ngay_co_so_cuoi(tq_that):
    """Errata ㉑: cột đầu 2024-10-20 *(⛔ 21/10)*; 760 cột; dòng sổ cuối 2026-11-11 ⇒ 7 cột cuối CHƯA CÓ SỐ."""
    h = tq_that.hd2_cong
    assert h["truc_ngay"]["dau"] == "2024-10-20" and h["truc_ngay"]["so_cot"] == 760
    assert h["truc_ngay"]["ngay_so_cuoi"] == "2026-11-11"
    assert h["truc_ngay"]["cot_chua_co_so"] == 7


def test_H5_B2_hd2_cong_tep_THEM_goi_C3a_giu_nguyen_C2():
    j = json.loads(do_hd2.RA_CONG.read_text(encoding="utf-8"))
    assert j["goi"] == "WP-C2" and j["tong_o"] == do_hd2.MONG_TONG_O      # WP-C2 y nguyên
    c = j["WP-C3a"]
    assert c["goi"] == "WP-C3a" and c["dat"] is True
    assert c["tong_o"] == c["mong_tong_o"] == c["khop"] == 205175
    assert set(c["dung_sai_theo_khoi"]) == {"la", "cha"}


def test_H5_Đ3_dap_an_rong_thi_DO(nguon):
    vao, da, fx, cay = nguon
    rong = dict(da, dong=[])
    tq = do_hd2.so_sanh_c3a(vao, rong, fx, cay, _lich(), do_hd2.mong_c3a_mac_dinh())
    assert not tq.phan_xu.dat


def test_H5_Đ5_mot_o_dap_an_lech_thi_DO_dung_o_ay(nguon):
    vao, da, fx, cay = nguon
    da2 = copy.deepcopy(da)
    r = next(r for r in da2["dong"] if _chu(r["le"]) == "SGO1" and _chu(r["ma_hd"]) == "GI")
    r["gt"] = str(D(r["gt"]) + D("1e-12"))
    tq = do_hd2.so_sanh_c3a(vao, da2, fx, cay, _lich(), do_hd2.mong_c3a_mac_dinh())
    assert not tq.phan_xu.dat
    assert [(x["le"], x["ma"], x["ngay"]) for x in tq.lech] == [("SGO1", "GI", int(r["ngay"]))]


def test_H5_Đ5_mong_lech_co_ten_khac_thi_DO_ca_hai_chieu(nguon):
    m = do_hd2.mong_c3a_mac_dinh()
    bot = dataclasses.replace(m, thieu_D=m.thieu_D[1:])
    them = dataclasses.replace(m, hd_khac_hoa=m.hd_khac_hoa + 1)
    for mm in (bot, them):
        tq = do_hd2.so_sanh_c3a(*nguon, _lich(), mm)
        assert not tq.phan_xu.dat


# ── AC-3 · đột biến một dòng sổ ⇒ đúng ô lá + mọi cha ĐỎ ─────────────────────────

def test_H5_AC3_dot_bien_mot_dong_so_do_dung_la_va_to_tien(nguon):
    vao, da, fx, cay = nguon
    vao2 = copy.deepcopy(vao)
    nut = {n.ma: n for n in cay.nut}
    nhan = {f"{n.ma} | {n.ten}": n.ma for n in cay.nut}
    # dòng khối SGO2 có E, nhãn là LÁ có ≥ 2 tổ tiên *(đo: thấy được trên ảnh thật)*
    def _sau(m):
        return 0 if nut[m].cha is None else 1 + _sau(nut[m].cha)
    r = next(r for r in vao2["dong"] if _chu(r["le"]) == "SGO2" and r["E"] is not None
             and _chu(r["D"]) and nhan.get(_chu(r["hd_final"])) in nut
             and cay.la(nhan[_chu(r["hd_final"])]) and _sau(nhan[_chu(r["hd_final"])]) >= 2)
    ma = nhan[_chu(r["hd_final"])]
    chuoi = [ma]
    while nut[chuoi[-1]].cha is not None:
        chuoi.append(nut[chuoi[-1]].cha)
    r["E"] = str(D(r["E"]) + 1)          # +1 nguyên tệ ≥ ~4e-11 mUSD (VND) ≫ atol 1e-14
    tq = do_hd2.so_sanh_c3a(vao2, da, fx, cay, _lich(), do_hd2.mong_c3a_mac_dinh())
    ngay = int(r["ngay"])
    mong = {(k, m, ngay) for k in ("GROUP", "SGO2") for m in chuoi}
    assert len(chuoi) >= 3
    assert {(x["le"], x["ma"], x["ngay"]) for x in tq.lech} == mong
    assert not tq.phan_xu.dat


def test_H5_AC3_dung_sai_theo_khoi_co_so_do():
    ds = do_hd2.DUNG_SAI_C3A
    assert set(ds) == {"la", "cha"}
    for k in ds.values():
        assert k.atol == D("1e-14") and k.rtol == 0
    # căn cứ đo 18/11 (max|lệch| engine↔đáp án trên 205.175 ô): lá 1,0e-15 · cha 7,5e-16 ⇒ biên ≥ ×10
    assert do_hd2.DO_C3A_MAX_LECH == {"la": D("1.0e-15"), "cha": D("7.6e-16")}
    for k, v in do_hd2.DO_C3A_MAX_LECH.items():
        assert ds[k].atol >= 10 * v


# ── AC-4 · ⛔ vòng tròn ────────────────────────────────────────────────────────────

def test_H5_AC4_dap_an_khong_phai_dau_vao__xoa_gia_tri_dap_an_luoi_y_nguyen(nguon, tq_that):
    vao, da, fx, cay = nguon
    da0 = copy.deepcopy(da)
    for r in da0["dong"]:
        r["gt"] = "0"
    tq = do_hd2.so_sanh_c3a(vao, da0, fx, cay, _lich(), do_hd2.mong_c3a_mac_dinh())
    assert tq.luoi == tq_that.luoi                        # engine ⛔ đọc đáp án
    assert not tq.phan_xu.dat                             # …nhưng cổng ĐỎ (mong là thật)


def test_H5_AC4_doi_ty_gia_thi_luoi_doi(nguon, tq_that):
    vao, da, fx, cay = nguon
    fx2 = {t: dict(v) for t, v in fx.items()}
    t0 = 202410                                           # tháng có dòng sổ đầu tiên
    fx2[t0]["USD"] = fx2[t0]["USD"] * 2
    tq = do_hd2.so_sanh_c3a(vao, da, fx2, cay, _lich(), do_hd2.mong_c3a_mac_dinh())
    assert tq.luoi != tq_that.luoi


#: H5-R1-03 — ghim 20 mã KPI *(đọc FORMULA `F53:H93` 18/11)*: thêm/bớt mã ⇒ mẫu số đổi im lặng ⇒ ĐỎ.
MA_KPI_GHIM = ("EBITDA", "EBIT", "EBT", "NP", "NPC", "NCF", "NCFO", "CRO", "COO", "NCFI", "COI",
               "NCFF", "CRF", "COF", "PL2", "PL3", "PL4", "PL6", "PL7", "PL8")


def test_H5_R1_03_MA_KPI_ghim_20_ma():
    assert do_hd2.MA_KPI == MA_KPI_GHIM and len(set(MA_KPI_GHIM)) == 20


# ── H6-R1-02 · trục WP-C3a TỪ IX.PER (kho), ⛔ từ đáp án 409 ─────────────────────────

def test_H6_R1_02_truc_C3a_khong_doc_dap_an_409(nguon, tq_that):
    """Xoá `phu.ngay_truc` của đáp án ⇒ kết quả Y NGUYÊN *(trục không còn đến từ 409)*."""
    vao, da, fx, cay = nguon
    da2 = copy.deepcopy(da)
    da2.get("phu", {}).pop("ngay_truc", None)
    tq = do_hd2.so_sanh_c3a(vao, da2, fx, cay, _lich(), do_hd2.mong_c3a_mac_dinh())
    assert tq.phan_xu.dat, tq.phan_xu.ly_do
    assert (tq.khop, tq.tong_o) == (tq_that.khop, tq_that.tong_o) == (205175, 205175)


def test_H6_R1_02_IX_PER_doi_ngay_dau_thi_truc_C3a_doi_va_DO(nguon):
    """Ngày đầu IX.PER 25/10 ⇒ cột đầu 24/10 *(= ngày đầu − 1, errata ㉑)* ≠ mong 20/10 ⇒ ĐỎ."""
    tq = do_hd2.so_sanh_c3a(*nguon, _lich(date(2024, 10, 25)), do_hd2.mong_c3a_mac_dinh())
    assert tq.hd2_cong["truc_ngay"]["dau"] == "2024-10-24"
    assert not tq.phan_xu.dat and any("ngày đầu trục" in x for x in tq.phan_xu.ly_do)


def test_H6_R1_02_chay_wp_c3a_doc_IX_PER_tu_kho_DAT_205175():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bo-test-h6-r1", ngay_dau="2024-10-21", luat="A", nguon=NGUON_PER)
    tq = do_hd2.chay_wp_c3a(dsn=dsn_test())
    assert tq.phan_xu.dat, tq.phan_xu.ly_do
    assert tq.khop == tq.tong_o == 205175
    assert tq.hd2_cong["truc_ngay"]["so_cot"] == 760


def test_H6_R1_02_chay_wp_c3a_kho_doi_IX_PER_thi_truc_doi():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bo-test-h6-r1", ngay_dau="2024-10-25", luat="A", nguon=NGUON_PER + " · 25/10")
    try:
        tq = do_hd2.chay_wp_c3a(dsn=dsn_test())
        assert tq.hd2_cong["truc_ngay"]["dau"] == "2024-10-24" and not tq.phan_xu.dat
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as c:
            chc.nap_ix_per(c, actor="bo-test-h6-r1", ngay_dau="2024-10-21", luat="A", nguon=NGUON_PER)


def test_H6_R1_02_kho_chua_khai_IX_PER_thi_C3a_DO(monkeypatch):
    def _nem(_c):
        raise chc.ChuaKhai("IX.PER chua co")
    monkeypatch.setattr(chc, "doc_per", _nem)
    tq = do_hd2.chay_wp_c3a(dsn=dsn_test())
    assert not tq.phan_xu.dat and any("IX.PER" in x for x in tq.phan_xu.ly_do)
