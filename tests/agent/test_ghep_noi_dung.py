# -*- coding: utf-8 -*-
"""Ghép theo NỘI DUNG (A2.04) + fleet eval nhiều vòng — luật cứng · chấm mù · bar."""
from __future__ import annotations

import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "tools"))

import fleet_eval_voi as fe  # noqa: E402

from fls.agent import ghep_noi_dung as gnd  # noqa: E402
from fls.agent.cong_skill import cong_luat_ghep  # noqa: E402


def test_cham_rubric_0_1_2():
    dap = {"noi:a.chon": "PM-1", "noi:a.nhom": "phai_noi", "noi:b.chon": "DE_NGUOI", "noi:b.nhom": "phai_nguoi",
           "noi:c.chon": "PM-3", "noi:c.nhom": "phai_noi"}
    ra = gnd.cham({"noi:a.chon": "PM-1", "noi:a.ly_do": "mã", "noi:b.chon": "PM-9", "noi:c.chon": "DE_NGUOI"}, dap)
    assert [(x["ca"], x["diem"]) for x in ra] == [("a", 2), ("b", 0), ("c", 1)]
    th = gnd.tong_hop(ra)
    assert th["phai_nguoi_bi_noi"] == 1 and th["noi_sai"] == 1 and th["ti_le_noi_sai"] == 0.5


def test_ti_le_noi_sai_0_tren_0_la_None_KHONG_phai_0():
    assert gnd.tong_hop(gnd.cham({"noi:a.chon": "DE_NGUOI"}, {"noi:a.chon": "PM-1", "noi:a.nhom": "phai_noi"}))[
        "ti_le_noi_sai"] is None


def test_cong_luat_ghep__chon_ngoai_ung_vien_hoac_lech_tien__DO():
    cc = {"noi:a.tien": 100, "noi:a.cur": "VND", "noi:a.uv.0.pm": "PM-1", "noi:a.uv.0.tien": 5000,
          "noi:a.uv.0.cur": "VND"}
    assert cong_luat_ghep({"noi:a.chon": "PM-1"}, "", {"cong_cu": cc})[0] is False      # lệch 4.900 > 1.000
    assert cong_luat_ghep({"noi:a.chon": "PM-7"}, "", {"cong_cu": cc})[0] is False      # ngoài ứng viên
    assert cong_luat_ghep({"noi:a.chon": "DE_NGUOI"}, "", {"cong_cu": cc})[0] is True
    assert cong_luat_ghep({}, "", {"cong_cu": {}})[0] is False                           # Đ3


def test_fleet_eval_ba_vong__khai_mong():
    """Mong (Đ5) trên bể DỰNG 12 ca: v0 0 nối · v1 tắt nội dung 2 nối · v1 bật nội dung 6 nối; 0 nối sai;
    0 ca phải-để-người bị nối. Sửa luật/bể ⇒ ĐỎ ⇒ khai lại."""
    ca, dap, _ = fe.cav.bo_ca(cho_heldout=False)
    ds = [fe.chay_vong(m, l, c, ca, dap) for m, l, c in fe.VONG]
    assert [(v["tong_hop"]["so_noi"], v["tong_hop"]["noi_sai"], v["tong_hop"]["phai_nguoi_bi_noi"]) for v in ds] == \
        [(0, 0, 0), (2, 0, 0), (6, 0, 0)]
    assert [x["ket"] for x in fe.phan_xu(ds)] == ["ĐẠT bar"] * 3


def test_fleet_eval__luat_noi_bua_bi_CHAN():
    """Luật "nối ứng viên đầu tiên" phải bị CHẶN (nối ca phải-để-người) — chứng minh bar có răng."""
    def bua(cells):
        return {f"noi:{c}.chon": cells[f"noi:{c}.uv.0.pm"] for c in gnd._ca(cells)}
    ca, dap, _ = fe.cav.bo_ca(cho_heldout=False)
    v = fe.chay_vong("bua", bua, True, ca, dap)
    # luật cứng của skill chặn trước cả bộ chấm (ca c05/c06 lệch tiền tệ/tiền)
    assert v.get("loi") or v["cong_skill"]["dat"] is False or fe.phan_xu([v])[0]["chan"]
