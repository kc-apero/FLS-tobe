"""H7 *(ISP 3.1.2 · Step 32 · WO-245)* — cổng WP-C3c: CA.GL dòng HR ↔ `gl_hr_408` + SO.CFA3 ↔ `cfa3`.

Chuỗi: `hr_ledger_2025` *(ĐẦU VÀO thượng nguồn — DT6c, BG-250)* → `hd_final_hr` *(IX.HD `code_hr`)* +
`cdt1_hr` *(IX.ORG, `cdt_cua`)* → `tinh_gl` *(H1/H4)* → ① Σ BA/BB theo (kỳ, nhãn V) ↔ 408 · ② `cfa1_daily`
*(H5 — trục = KỲ tháng)* ↔ `cfa3` Σ ngày → tháng.

  · **AC-1** — ảnh thật ĐẠT, mẫu số khai TRƯỚC *(Đ4)*; mong lệch ĐỎ cả hai chiều *(Đ5)*; đáp án rỗng ĐỎ *(Đ3)*.
  · **AC-2** — CDT lạ ⇒ lớp `cdt_la` có tên *(⛔ SHQ2)*; bài đơn vị ở `tests/bao_cao/test_gl_hr.py`.
  · **AC-3** — 2.302 hàng `ky_suy`: đếm + Σ PS Có + `BA`/`BB` rỗng ⇒ lớp riêng, ⛔ hoá 0, ⛔ tính là FLS sai.
  · **AC-4** — khối `hd2_cong.json` theo hợp đồng CG2 *(`khop` = ô khớp THẬT + `lech_co_chu_dich`)*.
  · **AC-5** — ⛔ vòng tròn: đột biến 1 dòng ĐẦU VÀO ⇒ đúng ô GL + lá CFA3 + tổ tiên ĐỎ.
"""
from __future__ import annotations

import copy
import dataclasses
import json
import pathlib
import sys
from decimal import Decimal as D

import psycopg
import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2, do_hd2_c3c as c3c  # noqa: E402


@pytest.fixture(scope="module")
def nguon():
    return c3c.nap_nguon()


@pytest.fixture(scope="module")
def tq_that(nguon):
    return c3c.so_sanh_c3c(*nguon, c3c.mong_c3c_mac_dinh())


def _chay(nguon, **thay):
    n = dict(zip(("vao", "gl", "cfa3", "fx", "cay", "code_hr", "org"), nguon))
    n.update(thay)
    return c3c.so_sanh_c3c(n["vao"], n["gl"], n["cfa3"], n["fx"], n["cay"], n["code_hr"], n["org"],
                           thay.get("mong", c3c.mong_c3c_mac_dinh()))


# ── AC-1 · ảnh thật ─────────────────────────────────────────────────────────────

def test_H7_B1_anh_that_DAT_mau_so_khai_truoc(tq_that):
    h = tq_that.hd2_cong
    assert tq_that.phan_xu.dat, tq_that.phan_xu.ly_do
    m = c3c.mong_c3c_mac_dinh()
    # Đ4: GL 12 kỳ × 10 nhãn V × {BA, BB} = 240 · CFA3 54 mã ⛔ KPI × 12 kỳ = 648
    assert (h["gl"]["o_so"], h["cfa3"]["o_so"]) == (m.gl_o_so, m.cfa3_o_so) == (240, 648)
    assert h["tong_o"] == 888 and h["khop"] + h["lech_co_chu_dich"] == h["tong_o"]
    assert (h["lech_co_chu_dich"], h["mong_lech_co_chu_dich"], h["lech_ngoai_ten"]) == (53, 53, 0)
    # Đ3: bằng chứng DƯƠNG — ô so mà đáp án ≠ 0
    assert (h["gl"]["o_so_dap_an_khac_0"], h["cfa3"]["o_so_dap_an_khac_0"]) == (m.gl_o_khac_0, m.cfa3_o_khac_0)
    assert m.gl_o_khac_0 > 0 and m.cfa3_o_khac_0 > 0


def test_H7_B1_lech_co_ten_theo_lop_dung_MONG(tq_that):
    h = tq_that.hd2_cong
    lop = h["lech_co_ten"]
    assert lop["thieu_tien_te_D"] == 462 and lop["hd_mac_dinh_oga"] == 20
    assert lop["cdt_la"] == {"COR_Terasofts": 592, "(rỗng)": 59, "INT | Insurance Total": 4,
                             "NIS | Net Income Staff": 3, "COM | COM Total": 1}
    assert lop["ky_suy"] == {"so_hang": 2302, "tong_F": "6763528503", "ba_bb_rong": 2302}
    assert lop["chua_co_dau_vao"]["gl_hang"] == {"202601": 269}
    assert lop["chua_co_dau_vao"]["cfa3_o_thang_khac_0"] == 17
    assert h["gl"]["lech_theo_ky"] == {"202502": 2, "202504": 2, "202506": 1, "202508": 1, "202509": 1,
                                       "202510": 7, "202512": 6}
    assert h["cfa3"]["lech_theo_ky"] == {"202502": 4, "202504": 3, "202510": 13, "202512": 13}


def test_H7_Đ3_dap_an_rong_thi_DO(nguon):
    gl = copy.deepcopy(nguon[1])
    gl["dong"] = []
    tq = _chay(nguon, gl=gl)
    assert not tq.phan_xu.dat
    cf = copy.deepcopy(nguon[2])
    cf["dong"] = []
    assert not _chay(nguon, cfa3=cf).phan_xu.dat


def test_H7_Đ5_mong_khac_thi_DO_ca_hai_chieu(nguon):
    m = c3c.mong_c3c_mac_dinh()
    for thay in ({"gl_o_so": 241}, {"cfa3_o_khac_0": m.cfa3_o_khac_0 - 1}, {"thieu_D": 461},
                 {"lech_gl": {**m.lech_gl, "202504": 1}}, {"lech_cfa3": {**m.lech_cfa3, "202503": 1}},
                 {"cdt_la": {**m.cdt_la, "(rỗng)": 58}}, {"ky_suy_hang": 2301}, {"hd_mac_dinh": 21}):
        tq = _chay(nguon, mong=dataclasses.replace(m, **thay))
        assert not tq.phan_xu.dat, thay


def test_H7_Đ5_mot_o_dap_an_lech_thi_DO_dung_o_ay(nguon):
    gl = copy.deepcopy(nguon[1])
    r = next(x for x in gl["dong"] if x["ky"] == "202503" and x.get("BA") not in (None, "0"))
    r["BA"] = str(D(r["BA"]) + D("1e-12"))
    tq = _chay(nguon, gl=gl)
    assert not tq.phan_xu.dat
    assert [(x["phan"], x["ky"]) for x in tq.lech] == [("gl", "202503")]


# ── AC-3 · ky_suy ───────────────────────────────────────────────────────────────

def test_H7_AC3_ky_suy_KHONG_hoa_0_bot_mot_hang_thi_DO(nguon):
    gl = copy.deepcopy(nguon[1])
    i = next(i for i, x in enumerate(gl["dong"]) if x.get("ky_suy"))
    del gl["dong"][i]
    tq = _chay(nguon, gl=gl)
    assert not tq.phan_xu.dat and any("ky_suy" in l for l in tq.phan_xu.ly_do)
    gl2 = copy.deepcopy(nguon[1])
    x = next(x for x in gl2["dong"] if x.get("ky_suy"))
    x["BA"] = "0"                                    # hàng gán kỳ mà có mUSD ⇒ ⛔ đúng mô tả ⇒ ĐỎ
    assert not _chay(nguon, gl=gl2).phan_xu.dat


# ── AC-5 · ⛔ vòng tròn ─────────────────────────────────────────────────────────

def test_H7_AC5_dot_bien_mot_dong_DAU_VAO_do_dung_o_GL_va_la_to_tien_CFA3(nguon):
    vao = copy.deepcopy(nguon[0])
    r = next(x for x in vao["dong"] if x["ky"] == "202503" and (x.get("hd") or {}).get("chu") == "GAH"
             and x.get("D"))
    r["E"] = str(D(r.get("E") or 0) + D(10 ** 9))
    tq = _chay(nguon, vao=vao)
    assert not tq.phan_xu.dat
    cha = {n.ma: n.cha for n in nguon[4].nut}
    to_tien, m = ["GAH"], "GAH"
    while cha[m] is not None:
        m = cha[m]
        to_tien.append(m)
    mong = {("gl", "202503", "GAH | GA HR Cost·BA")} | {("cfa3", "202503", t) for t in to_tien}
    o = {(x["phan"], x["ky"], x["o"]) for x in tq.lech}
    assert len(to_tien) >= 2 and o == mong, sorted(o)


def test_H7_AC5_xoa_gia_tri_dap_an_ket_qua_engine_y_nguyen(nguon, tq_that):
    gl = copy.deepcopy(nguon[1])
    for x in gl["dong"]:
        x["BA"] = x["BB"] = None
    cf = copy.deepcopy(nguon[2])
    for x in cf["dong"]:
        x["gt"] = "0"
    tq = _chay(nguon, gl=gl, cfa3=cf)
    assert tq.luoi == tq_that.luoi and not tq.phan_xu.dat


# ── IX.ORG đọc TỪ KHO · AC-4 hợp đồng CG2 ──────────────────────────────────────

def test_H7_IX_ORG_tu_kho_va_chua_khai_thi_DO():
    tq = c3c.chay_wp_c3c("postgresql://fls:sai@localhost:1/khong_co")
    assert not tq.phan_xu.dat and "IX.ORG" in tq.phan_xu.ly_do[0]
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_org(c, str(c3c.CDT_CORRECT), str(c3c.MM), actor="bai-h7")
    tq = c3c.chay_wp_c3c(dsn_test())
    assert tq.phan_xu.dat, tq.phan_xu.ly_do


def test_H7_AC4_khoi_hd2_cong_tep_that_theo_hop_dong_CG2():
    d = json.loads(do_hd2.RA_CONG.read_text(encoding="utf-8"))
    b = d["WP-C3c"]
    assert b["goi"] == "WP-C3c" and b["dat"] is True
    assert isinstance(b["tong_o"], int) and isinstance(b["khop"], int) and b["tong_o"] > 0
    assert b["khop"] + b["lech_co_chu_dich"] == b["tong_o"]
    assert b["lech_co_chu_dich"] == b["mong_lech_co_chu_dich"]
    assert d["goi"] == "WP-C2" and d["WP-C3a"]["dat"] is d["WP-C3b"]["dat"] is True      # CHỈ THÊM
