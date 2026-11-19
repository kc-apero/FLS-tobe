"""H9 — `tools/do_hd2.py --goi WP-C4a`: AL.PLT GI vendor THƯỜNG ↔ MID3 từng ô *(ISP 3.1.2 · Step 24 ·
WO-200 · sau DT8b BG-205)*.

Chuỗi: IX.VEN ĐỌC TỪ KHO test + ảnh CFA1 GI *(PD 504: O = Σ pe, P = Σ pm số theo Vendor-tháng)* →
`chia_nen_tang` → `ks_al` → so (vendor, tháng) × 14 cột với `gi_mid3.json`. ⛔ MID3 làm đầu vào.

  · **AC-4** — mẫu số khai TRƯỚC *(`MongC4a`)*: 44 Vendor-tháng · 420 ô so · 196 ô ⛔ so được
    *(P chữ)* · ô ≠ 0 = **0** *(tập toàn 0 — ⛔ chứng minh RATE ⇒ H10)* · 5 nhãn / 15 vendor bỏ qua.
  · **Đ5 hai chiều** — một Vendor-tháng thường bỗng ≠ 0 *(đầu vào hay đáp án)* ⇒ ĐỎ có tên; mong khác ⇒ ĐỎ.
  · **AC-5** — đột biến một ô đáp án ⇒ ĐÚNG ô ấy lệch; ⛔ vòng tròn: xoá đáp án ⇒ engine y nguyên.
"""
from __future__ import annotations

import copy
import dataclasses
import pathlib
import sys

import psycopg
import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2  # noqa: E402

pytestmark = pytest.mark.pg


@pytest.fixture(scope="module")
def ven():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_ven(c, str(GOC / "tests/fixture/cau_hinh/ix_ven.json"),
                       duong_cdt1=str(GOC / "tests/fixture/cau_hinh/cdt_correct.json"),
                       actor="bo-test-h9-c4a")
        return chc.doc_ven(c)


@pytest.fixture(scope="module")
def anh():
    return do_hd2.nap_anh(do_hd2.ANH_CFA1_GI), do_hd2.nap_anh(do_hd2.ANH_MID3)


def _chay(ven, cfa1, mid3, **mong):
    return do_hd2.so_sanh_c4a(cfa1, mid3, ven, dataclasses.replace(do_hd2.MongC4a(), **mong))


def _dong(anh_, v, t):
    return [r for r in anh_["dong"] if do_hd2._chu(r.get("vendor")) == v and r.get("thang") == t]


def test_H9_B3_WP_C4a_anh_that_DAT_mau_so_co_nhan(ven, anh):
    tq = _chay(ven, *anh)
    h = tq.hd2_cong
    assert tq.phan_xu.dat, tq.phan_xu.ly_do
    assert (h["vm_thuong"], h["o_so"], h["o_khong_so"], h["vm_p_chu"]) == (44, 420, 196, 28)
    assert h["o_khac_0"] == 0 and "tập toàn 0" in h["o_khac_0_nhan"]       # Đ3: nói thẳng
    assert h["lech"] == 0 and h["ks_al_vm"] == 44
    assert h["bo_qua"] == {"Max": 132, "VD341": 11, "VD428": 11, "VD444": 11, "VD62": 11}
    assert h["vendor_bo_qua"] == 15 and h["vendor_thuong"] == ["VD113", "VD336", "VD58", "VD61"]


def test_CG2_R2_03_khoi_WP_C4a_khai_tong_o_va_khop_theo_hop_dong_H4(ven, anh):
    """Đ4: `tong_o` = ô SO ĐƯỢC (420, ⛔ tính 196 ô P chữ) · `khop` = ô so khớp = `o_so − lech`."""
    h = _chay(ven, *anh).hd2_cong
    assert (h["tong_o"], h["khop"]) == (420, 420) and h["tong_o"] == h["o_so"]
    assert type(h["tong_o"]) is int and type(h["khop"]) is int


def test_CG2_R2_03_khop_giam_dung_so_o_lech(ven, anh):
    mid3 = copy.deepcopy(anh[1])
    _dong(mid3, "VD61", "202507")[0]["csm_pe"] = "1"
    h = _chay(ven, anh[0], mid3).hd2_cong
    assert (h["lech"], h["tong_o"], h["khop"]) == (1, 420, 419)


def test_D5_vendor_thuong_BONG_khac_0_o_DAU_VAO_thi_DO(ven, anh):
    cfa1, mid3 = copy.deepcopy(anh[0]), anh[1]
    _dong(cfa1, "VD58", "202503")[0]["pe"] = "5"
    tq = _chay(ven, cfa1, mid3)
    assert not tq.phan_xu.dat and "VD58 · 202503: Σ PE Vendor-tháng = 0" in tq.phan_xu.mot_dong


def test_AC5_D5_dot_bien_MOT_o_dap_an_chi_DUNG_o_ay_DO(ven, anh):
    cfa1, mid3 = anh[0], copy.deepcopy(anh[1])
    _dong(mid3, "VD61", "202507")[0]["csm_pe"] = "1"
    tq = _chay(ven, cfa1, mid3)
    assert not tq.phan_xu.dat
    assert [(x["vendor"], x["thang"], x["cot"]) for x in tq.lech] == [("VD61", "202507", "csm_pe")]
    assert "lech: đo 1 ≠ mong 0" in tq.phan_xu.mot_dong and "o_khac_0: đo 1 ≠ mong 0" in tq.phan_xu.mot_dong


@pytest.mark.parametrize("mong", [{"o_so": 419}, {"o_khac_0": 1}, {"vm_thuong": 45},
                                  {"vendor_bo_qua": 14}, {"o_khong_so": 0}])
def test_D5_mong_KHAC_thi_DO_ca_hai_chieu(ven, anh, mong):
    assert not _chay(ven, *anh, **mong).phan_xu.dat


def test_D5_P_chu_KHONG_hoa_0_o_PM_khong_so(ven, anh):
    cfa1 = copy.deepcopy(anh[0])
    for r in cfa1["dong"]:
        r["pm_ghi_chu"] = None                                  # bỏ chữ ⇒ 196 ô PM thành ô so
    tq = _chay(ven, cfa1, anh[1])
    assert not tq.phan_xu.dat and tq.hd2_cong["o_so"] == 616 and tq.hd2_cong["o_khong_so"] == 0


def test_D3_MID3_mat_khoa_thi_DO_co_ten(ven, anh):
    mid3 = copy.deepcopy(anh[1])
    for r in mid3["dong"]:
        r["vendor"] = None
    tq = _chay(ven, anh[0], mid3)
    assert not tq.phan_xu.dat and "MID3 thiếu Vendor-tháng" in tq.phan_xu.mot_dong


def test_khong_vong_tron_xoa_dap_an_engine_Y_NGUYEN(ven, anh):
    from fls.bao_cao import phan_bo as pb
    cfa1 = anh[0]
    o, p = {}, {}
    for r in cfa1["dong"]:
        k = (do_hd2._chu(r["vendor"]), r["thang"])
        o[k] = o.get(k, 0) + do_hd2.Decimal(r["pe"])
        p[k] = p.get(k, 0) + do_hd2.Decimal(r["pm"] or 0)
    cdt = tuple(c for c in ven.cdt1 if not c.startswith("SHQ2"))
    a = pb.chia_nen_tang({k: {} for k in o}, o, p, ven, cdt1=cdt)
    assert len(a.chia) == 44                                    # engine ⛔ chạm MID3


def test_kho_CHUA_khai_IX_VEN_thi_DO_co_ten():
    tq = do_hd2.chay_wp_c4a("postgresql://fls:fls@localhost:1/khong_co")
    assert not tq.phan_xu.dat and "IX.VEN ⛔ đọc được từ kho" in tq.phan_xu.mot_dong


# ───────── Vòng sửa sau R1 (KQ-202) ─────────
def test_H9_R1_01_dot_bien_dap_an_o_Vendor_thang_P_chu_thi_DO_co_ten(ven, anh):
    """Đúng đột biến R1: `cvl_pm` VD336·202506 *(P = chữ ⇒ ô ⛔ so được)* = 1 từng XANH."""
    cfa1, mid3 = anh[0], copy.deepcopy(anh[1])
    assert _dong(cfa1, "VD336", "202506")[0]["pm_ghi_chu"] is not None      # đúng Vendor-tháng P-chữ
    _dong(mid3, "VD336", "202506")[0]["cvl_pm"] = "1"
    tq = _chay(ven, cfa1, mid3)
    assert not tq.phan_xu.dat and tq.hd2_cong["o_khong_so_khac_0"] == 1
    assert "o_khong_so_khac_0: đo 1 ≠ mong 0" in tq.phan_xu.mot_dong


def test_H9_R1_01_anh_that_196_o_dap_an_deu_0_va_mong_khac_thi_DO(ven, anh):
    tq = _chay(ven, *anh)
    assert tq.hd2_cong["o_khong_so"] == 196 and tq.hd2_cong["o_khong_so_khac_0"] == 0   # mẫu số 196 ≠ 0 (Đ3)
    assert tq.hd2_cong["mong"]["o_khong_so_khac_0"] == 0
    assert not _chay(ven, *anh, o_khong_so_khac_0=1).phan_xu.dat                   # Đ5 chiều ngược


def test_H9_R1_01_dap_an_P_chu_la_chu_cung_la_DO(ven, anh):
    mid3 = copy.deepcopy(anh[1])
    _dong(mid3, "VD336", "202506")[0]["pm"] = "Need to manual input"            # ⛔ đo được ⇒ ĐỎ
    tq = _chay(ven, anh[0], mid3)
    assert not tq.phan_xu.dat and tq.hd2_cong["o_khong_so_khac_0"] == 1


def test_H9_R1_02_ks_al_vm_lay_tu_engine_va_co_mong(ven, anh, monkeypatch):
    from fls.bao_cao import phan_bo as pb
    assert _chay(ven, *anh).hd2_cong["mong"]["ks_al_vm"] == 44
    monkeypatch.setattr(pb, "ks_al", lambda *a, **k: 43)          # đột biến M: ⛔ gọi/hằng 44 ⇒ ĐỎ
    tq = _chay(ven, *anh)
    assert not tq.phan_xu.dat and "ks_al_vm: đo 43 ≠ mong 44" in tq.phan_xu.mot_dong
