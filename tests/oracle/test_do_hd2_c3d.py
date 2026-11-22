"""H8 *(ISP 3.1.2 · Step 39 · WO-277)* — cổng WP-C3d: SO.PLA1 · PLA3 HR · PLA3 PM+HR ↔ đáp án 414–419.

Chuỗi: `gl_pl_dau_vao` *(DT7b)* → `tinh_gl` *(H4)* + ngày ghi nhận C6 *(D4 A từ `AH`)* → `pla.pla_daily` *(= H5
`cfa1_daily` + công thức tab)*; `hr_pl_dau_vao` → `BA/BB` + ngày `BK/BL`; PM+HR cộng THEO KHOÁ; Y/H/Q/M = `cuon_ky` (H6).

  · **AC-2** — đầu vào thượng nguồn, ⛔ đáp án: xoá giá trị đáp án ⇒ lưới engine y nguyên; `DE`/`BM`/`BR`/`BS` của
    sổ chỉ ĐỐI CHIẾU *(đổi chúng ⇒ đếm lệch đối chiếu, lưới y nguyên)*.
  · **AC-3** — ảnh thật ĐẠT; mẫu số khai TRƯỚC *(Đ4)*; `mong` khác ⇒ ĐỎ cả hai chiều *(Đ5)*; đáp án rỗng ⇒ ĐỎ *(Đ3)*.
  · **AC-5** — đột biến 1 dòng ĐẦU VÀO *(GL · HR)* ⇒ ĐỎ đúng ô *(Daily + Y/H/Q/M)*; cộng theo VỊ TRÍ ⇒ ĐỎ.
"""
from __future__ import annotations

import copy
import dataclasses
import datetime
import json
import pathlib
import sys
from decimal import Decimal as D

import psycopg
import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.bao_cao import pla  # noqa: E402
from fls.cau_hinh.ky import LichKy  # noqa: E402
from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2_c3d as c3d  # noqa: E402

LICH = LichKy(nguon="bai-h8", ngay_dau=datetime.date(2024, 10, 21), luat="A")
DEN = datetime.date(2026, 2, 27)
NGUON_PER = "bai-test-h8:ISP-3.1.2-Step39 (IX.PER kho = 21/10, C6)"


@pytest.fixture(scope="module")
def nguon():
    return c3d.nap_nguon()


@pytest.fixture(scope="module")
def tq_that(nguon):
    return _chay(nguon)


def _chay(nguon, mong=None, **thay):
    gl, hr, da, fx, cay = nguon
    gl, hr, da = thay.get("gl", gl), thay.get("hr", hr), thay.get("da", da)
    return c3d.so_sanh_c3d(gl, hr, da, fx, cay, LICH, DEN, mong or c3d.mong_c3d_mac_dinh())


def _sua_mong(**sua) -> c3d.MongC3d:
    m = copy.deepcopy(dict(c3d.mong_c3d_mac_dinh().so))
    for k, v in sua.items():
        m[k] = v
    return c3d.MongC3d(so=m)


# ── AC-3 · ảnh thật ─────────────────────────────────────────────────────────────

def test_H8_AC3_anh_that_DAT_mau_so_khai_truoc(tq_that):
    assert tq_that.phan_xu.dat, tq_that.phan_xu.ly_do
    h = tq_that.hd2_cong
    assert (h["tong_o"], h["khop"], h["lech_co_chu_dich"], h["lech_ngoai_ten"]) == (1289415, 1287624, 1791, 0)
    assert (h["o_co_so"], h["khop_co_so"], h["o_0_0"]) == (44501, 42710, 1244914)
    assert h["khop"] + h["lech_co_chu_dich"] == h["tong_o"] == h["mong_tong_o"]


def test_H8_AC3_khoi_va_KPI_tach_theo_tab(tq_that):
    t = tq_that.hd2_cong["theo_tab"]
    assert t["pla1_daily"]["thuong"]["o_so"] == 12 * 50 * 495 and t["pla1_daily"]["kpi"]["o_so"] == 12 * 17 * 495
    assert t["pla3_hr_yhqm"]["thuong"]["o_so"] == 1 * 50 * 57
    assert [t[x]["kpi"]["lech"] for x in t] == [0, 418, 414, 0, 0, 439]    # chỉ lệch AS-IS (8 GAC + trước CA)
    assert [t[x]["thuong"]["lech"] for x in t] == [0, 116, 112, 0, 0, 292]
    assert tq_that.hd2_cong["lech_co_ten"]["khong_so_duoc"] == 46398       # 11 × 74 × 57 (417 chỉ GROUP)


def test_H8_D3_dap_an_rong_thi_DO(nguon):
    gl, hr, da, fx, cay = nguon
    da0 = copy.deepcopy(da)
    for a in da0.values():
        a["dong"] = []
    tq = _chay(nguon, da=da0)
    assert not tq.phan_xu.dat


@pytest.mark.parametrize("duong, v", [(("lop", "gl", "AH_RONG"), 308), (("lop", "gl", "AH_RONG"), 310),
                                      (("lop", "tab", "pla1_daily", "chua_co_dau_vao"), 1),
                                      (("lop", "tu_kiem_dap_an", "daily", "thuong"), 3),
                                      (("lop", "khong_so_duoc"), 0), (("tong_o",), 1289414), (("lop", "la_cdt_truoc_CA_khac_0", "engine"), 37)])
def test_H8_D5_mong_lop_khac_thi_DO_ca_hai_chieu(nguon, duong, v):
    m = copy.deepcopy(dict(c3d.mong_c3d_mac_dinh().so))
    o = m
    for k in duong[:-1]:
        o = o[k]
    o[duong[-1]] = v
    assert not _chay(nguon, c3d.MongC3d(so=m)).phan_xu.dat


def test_H8_D5_o_lech_khai_thieu_thua_sai_gia_tri_thi_DO(nguon):
    ol = dict(c3d.mong_c3d_mac_dinh().so["o_lech"])
    k0 = next(iter(ol))
    thieu = {k: v for k, v in ol.items() if k != k0}
    thua = {**ol, "pla1_daily|GROUP#GI#45597": ("0", "0")}
    sai = {**ol, k0: (str(D(ol[k0][0]) + D("1e-6")), ol[k0][1])}
    for x in (thieu, thua, sai):
        assert not _chay(nguon, _sua_mong(o_lech=x)).phan_xu.dat


def test_H8_mong_vang_thi_DO(nguon):
    assert not _chay(nguon, c3d.MongC3d(so=None)).phan_xu.dat
    assert not _chay(nguon, c3d.MongC3d(so={"den": "2026-02-27"})).phan_xu.dat


def test_H8_chung_DO_dung_sai_mot_o_dap_an_1e_11(nguon):
    gl, hr, da, fx, cay = nguon
    da1 = copy.deepcopy(da)
    x = next(r for r in da1["pla1_yhqm"]["dong"] if r["le"]["chu"] == "SGO1" and r["ma_hd"]["chu"] == "GI")
    x["gt"] = str(D(x["gt"]) + D("1e-11"))
    tq = _chay(nguon, da=da1)
    assert not tq.phan_xu.dat and any("pla1_yhqm|SGO1#GI#" in s for s in tq.phan_xu.ly_do)


def test_H8_as_is_truoc_CA_doi_gia_tri_mot_o_thi_DO_va_ngoai_vung_thi_ngoai_ten(nguon, tq_that):
    """Lớp `as_is_truoc_CA` *(72 cột 2024 của 416, bản dán cũ)*: băm GIÁ TRỊ ⇒ đổi một ô đáp án trong vùng ⇒ ĐỎ;
    ô lệch NGOÀI vùng *(cột ≥ CA)* ⛔ được lớp nuốt."""
    gl, hr, da, fx, cay = nguon
    assert tq_that.so["la_cdt_truoc_CA_khac_0"] == {"dap_an": 0, "engine": 38}     # Đ3: tập ⛔ rỗng
    x = next(x for x in tq_that.lech if c3d.la_truoc_ca(x) and x["tab"] == "pla3_pm_hr_daily")
    kh, ma, t = x["o"].split("#")
    da1 = copy.deepcopy(da)
    r = next((r for r in da1["pla3_pm_hr_daily"]["dong"] if r["o_id"]["chu"] == x["o"]), None)
    if r is None:
        da1["pla3_pm_hr_daily"]["dong"].append({"o_id": {"chu": x["o"]}, "le": {"chu": kh}, "ma_hd": {"chu": ma},
                                                "ngay": t, "gt": "0.5"})
    else:
        r["gt"] = str(D(r["gt"]) + D("0.5"))
    tq = _chay(nguon, da=da1)
    assert not tq.phan_xu.dat and any(s.startswith("as_is_truoc_CA.sha256") for s in tq.phan_xu.ly_do)
    assert not c3d.la_truoc_ca({"tab": "pla3_hr_daily", "o": "CVL#GI#45658"})          # cột CA ⛔ thuộc lớp
    assert not c3d.la_truoc_ca({"tab": "pla3_hr_daily", "o": "GROUP#GI#45600"})        # GROUP ⛔ thuộc lớp
    assert not c3d.la_truoc_ca({"tab": "pla1_daily", "o": "CVL#GI#45600"})             # PLA1 ⛔ thuộc lớp


# ── AC-2 · đầu vào thượng nguồn — ⛔ vòng tròn ──────────────────────────────────

def test_H8_AC2_xoa_gia_tri_dap_an_luoi_engine_y_nguyen(nguon, tq_that):
    gl, hr, da, fx, cay = nguon
    da0 = copy.deepcopy(da)
    for a in da0.values():
        for r in a["dong"]:
            r["gt"] = "0"
    tq = _chay(nguon, da=da0)
    assert all(tq.luoi[t].o == tq_that.luoi[t].o for t in c3d.TAB)


def test_H8_AC2_DE_BM_BR_cua_so_chi_doi_chieu(nguon, tq_that):
    gl, hr, da, fx, cay = nguon
    gl1, hr1 = copy.deepcopy(gl), copy.deepcopy(hr)
    r = next(x for x in gl1["dong"] if x["AH"] == "202503" and x.get("D"))
    r["DE"], r["BR"] = str(int(r["DE"]) + 1), "123"
    h = next(x for x in hr1["dong"] if x["BK"] == "3")
    h["BM"] = str(int(h["BM"]) + 31)
    tq = _chay(nguon, gl=gl1, hr=hr1)
    assert all(tq.luoi[t].o == tq_that.luoi[t].o for t in c3d.TAB)       # ⛔ đọc DE/BM/BR làm đầu vào
    lop = c3d._so_lop(tq.so)
    assert (lop["gl"]["de_lech"], lop["gl"]["br_lech"], lop["hr"]["bm_lech"]) == (1, 1, 1)
    assert not tq.phan_xu.dat                                             # đối chiếu lệch ⇒ ĐỎ (mong 0)


# ── AC-5 · đột biến một dòng ĐẦU VÀO ⇒ đúng ô ĐỎ ──────────────────────────────────

def _o_do(tq) -> set[str]:
    """Mọi ô lệch NGOÀI bản khai *(⛔ đọc `ly_do` — nó cắt ở 20 dòng)*; kèm cổng ĐỎ."""
    assert not tq.phan_xu.dat
    khai = set(c3d.mong_c3d_mac_dinh().so["o_lech"])
    return {f"{x['tab']}|{x['o']}" for x in tq.lech if not c3d.la_truoc_ca(x)} - khai


def test_H8_AC5_dot_bien_mot_dong_GL_do_dung_o_PLA1_va_PM_HR(nguon):
    gl, hr, da, fx, cay = nguon
    gl1 = copy.deepcopy(gl)
    r = next(x for x in gl1["dong"] if x["AH"] == "202503" and (x.get("V") or {}).get("chu") == "GI | Gross Inflow"
             and (x.get("P") or {}).get("chu") == "SGO1" and x.get("E"))
    r["E"] = str(D(r["E"]) * 2)
    o = _o_do(_chay(nguon, gl=gl1))
    t = "45717"                                                               # 2025-03-01 (D4 A)
    assert {f"pla1_daily|GROUP#GI#{t}", f"pla1_daily|SGO1#GI#{t}", f"pla3_pm_hr_daily|GROUP#GI#{t}",
            "pla1_yhqm|GROUP#GI#2025M03", "pla1_yhqm|SGO1#GI#2025Q1", "pla3_pm_hr_yhqm|GROUP#GI#2025"} <= o
    assert not any(x.startswith("pla3_hr_") for x in o)                     # HR ⛔ đổi
    assert not any("SGO2#" in x for x in o)                                 # khối khác ⛔ đổi


def test_H8_AC5_dot_bien_mot_dong_HR_do_dung_o_HR_va_PM_HR(nguon):
    gl, hr, da, fx, cay = nguon
    hr1 = copy.deepcopy(hr)
    r = next(x for x in hr1["dong"] if x["BK"] == "5" and (x.get("V") or {}).get("chu") == "NIS | Net Income Staff"
             and x.get("BA") not in (None, "0"))
    r["BA"] = str(D(r["BA"]) + 1)
    o = _o_do(_chay(nguon, hr=hr1))
    t = "45778"                                                               # 2025-05-01
    assert {f"pla3_hr_daily|GROUP#NIS#{t}", f"pla3_pm_hr_daily|GROUP#NIS#{t}", "pla3_hr_yhqm|GROUP#NIS#2025M05",
            "pla3_pm_hr_yhqm|GROUP#NIS#2025Q2"} <= o
    assert not any(x.startswith("pla1_") for x in o)


def test_H8_AC5_doi_AH_mot_dong_so_dich_sang_thang_khac(nguon):
    gl, hr, da, fx, cay = nguon
    gl1 = copy.deepcopy(gl)
    r = next(x for x in gl1["dong"] if x["AH"] == "202503" and (x.get("V") or {}).get("chu") == "GI | Gross Inflow"
             and x.get("D"))
    r["AH"] = "202504"
    o = _o_do(_chay(nguon, gl=gl1))
    assert {"pla1_daily|GROUP#GI#45717", "pla1_daily|GROUP#GI#45748"} <= o


def test_H8_AC5_cong_theo_VI_TRI_thi_DO(nguon, monkeypatch):
    def vi_tri(a, b, khoa):
        k = list(khoa)
        return dict(zip(k, (x + y for x, y in zip(a.values(), b.values()))))
    monkeypatch.setattr(pla, "cong_theo_khoa", vi_tri)
    tq = _chay(nguon)
    assert not tq.phan_xu.dat and any(x.startswith("pla3_pm_hr_") for x in _o_do(tq))


# ── C6 · IX.PER TỪ KHO ──────────────────────────────────────────────────────────

def test_H8_IX_PER_tu_kho_DAT():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bai-h8", ngay_dau="2024-10-21", luat="A", nguon=NGUON_PER)
    tq = c3d.chay_wp_c3d(dsn=dsn_test())
    assert tq.phan_xu.dat, tq.phan_xu.ly_do


def test_H8_IX_PER_ngay_dau_khac_thi_truc_doi_va_DO():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bai-h8", ngay_dau="2024-11-05", luat="A", nguon=NGUON_PER + " · 05/11")
        try:
            tq = c3d.chay_wp_c3d(dsn=dsn_test())
        finally:
            chc.nap_ix_per(c, actor="bai-h8", ngay_dau="2024-10-21", luat="A", nguon=NGUON_PER)
    assert not tq.phan_xu.dat and any("truc" in s for s in tq.phan_xu.ly_do)


# ── AC-4 · khối `hd2_cong.json` THẬT theo hợp đồng CG2 ─────────────────────────────

def test_H8_AC4_khoi_hd2_cong_tep_that_theo_hop_dong_CG2(tq_that):
    b = json.loads((GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json").read_text(encoding="utf-8"))["WP-C3d"]
    assert (b["goi"], b["dat"], b["tong_o"], b["khop"], b["lech_co_chu_dich"], b["mong_lech_co_chu_dich"]) == \
        ("WP-C3d", True, 1289415, 1287624, 1791, 1791)
    assert b["khop_co_so"] + b["o_0_0"] == b["khop"] and b["o_co_so"] + b["o_0_0"] == b["tong_o"]
    assert b["theo_tab"] == json.loads(json.dumps(tq_that.hd2_cong["theo_tab"]))   # sinh bằng --ghi, ⛔ sửa tay
