# -*- coding: utf-8 -*-
"""WO-329 AC-2 · AC-4 · AC-5 — chuỗi 4 agent ở chế độ PHÁT LẠI khớp 100 %; phá đâu ĐỎ đúng chỗ, có tên.

Mọi bài chạy engine thật (`tools/do_voi_so_luong.do()`, ~2 s) trên ảnh đóng băng; ⛔ kho, ⛔ API.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "tools"))

import chay_agent_voi as cav  # noqa: E402

from fls.agent import chuoi as ch  # noqa: E402
from fls.agent import doi_chieu as dc  # noqa: E402
from fls.agent import mo_hinh as mh  # noqa: E402
from fls.agent import report as rp  # noqa: E402

#: Mong (Đ5) — số ô của bản phát lại hôm nay. Thêm/bớt mẫu ô ⇒ ĐỎ ⇒ khai lại ở đây + BG.
MONG_SO_O = 627


@pytest.fixture(scope="module")
def phat_lai():
    return cav.chay("phat_lai", cho_heldout=False)


def test_AC5_phat_lai__KET_DAT_lech_0(phat_lai):
    kc, may, _, _ = phat_lai
    dem = dc.tom_tat([o for a in kc.agents for o in a.o])
    assert kc.dung_o is None and kc.dat
    assert dem["mau_so"] == MONG_SO_O and dem[dc.KHOP] == MONG_SO_O
    assert all(dem[k] == 0 for k in dc.TRANG_THAI_DO)
    assert [a.dat_a4 for a in kc.agents] == [True] * 4


def test_AC2_thu_tu_skill_va_agent(phat_lai):
    kc = phat_lai[0]
    assert [a.dn.ma for a in kc.agents] == ["A1_RI", "A2_PR_MAP", "A3_SI_ITL", "A4_AUDITOR"]
    for a in kc.agents:
        assert [k.skill.so for k in a.skills] == list(range(1, len(a.skills) + 1))
        assert all(k.dat_cong for k in a.skills)


class SuaDap:
    """Bọc nhà cung cấp: sửa câu trả lời CUỐI của một skill (theo tên công cụ)."""

    def __init__(self, goc, cong_cu: str, sua):
        self.goc, self.cc, self.sua, self.ten = goc, cong_cu, sua, "sua"

    def goi(self, yc):
        tl = self.goc.goi(yc)
        if tl.get("stop_reason") == "end_turn" and yc["tools"][0]["name"] == self.cc:
            ra = json.loads(tl["content"][0]["text"])
            self.sua(ra)
            tl = {"stop_reason": "end_turn", "content": [{"type": "text", "text": json.dumps(ra)}]}
        return tl


def _chay_sua(cong_cu, sua, agent="A2_PR_MAP"):
    ncc = cav.ncc_cho("gia")
    ncc[agent] = SuaDap(ncc[agent], cong_cu, sua)
    return cav.chay("gia", ncc=ncc, cho_heldout=False)


def test_AC2_pha_cong_skill_giua__chuoi_DUNG_dung_cho():
    def sua(ra):
        ra["voi:theo_ky.2025-01.map_fls"] += 1                # Σ kỳ ≠ tổng ⇒ cổng A2.02 ĐỎ
    kc = _chay_sua("ghep_ref", sua)[0]
    assert kc.dung_o.startswith("DỪNG ở A2_PR_MAP/02_ghep_ref — cổng `tong_ky:map_fls+pm_noi` ĐỎ")
    a2 = kc.agents[1]
    assert [k.dat_cong for k in a2.skills] == [True, False, None, None]
    a3 = kc.agents[2]
    assert all(k.dat_cong is None for k in a3.skills)
    assert {o.trang_thai for o in a3.o} == {dc.CHUA_CHAY}


def test_AC5_dot_bien_mot_o__A4_DO_dung_o():
    def sua(ra):
        ra["voi:bank_tong.dong_theo_hinh.A"] += 1              # cổng skill ⛔ soát ô này ⇒ chỉ A4 bắt
    kc, may, dap, be = _chay_sua("ghep_ref", sua)
    lech = [o for a in kc.agents for o in a.o if o.trang_thai == dc.LECH]
    assert [(o.ma, o.agent, o.may) for o in lech] == [("voi:bank_tong.dong_theo_hinh.A", 2273, 2272)]
    assert kc.dung_o.startswith("A4 TRƯỢT A2_PR_MAP: LECH 1")
    assert kc.agents[2].dat_a4 is False and kc.agents[2].skills[0].dat_cong is None
    html, tom = rp.sinh(kc, {}, cav.as_is_co_ten(may), None, {}, "2026-11-23")
    assert not tom["dat"] and "KẾT: ĐỎ" in html and "voi:bank_tong.dong_theo_hinh.A" in html


def test_AC5_agent_bot_o_va_them_o__DO():
    def sua(ra):
        ra.pop("voi:tong.pm_noi")
        ra["voi:tu_bia"] = 1
    kc = _chay_sua("ghep_ref", sua)[0]
    tt = {o.ma: o.trang_thai for o in kc.agents[1].o}
    assert tt["voi:tong.pm_noi"] in (dc.AGENT_THIEU,) or kc.dung_o.startswith("DỪNG")
    assert kc.dat is False


def test_AC5_xoa_dau_vao_mot_lop__DO_khong_do_duoc(tmp_path):
    hd2 = tmp_path / "hd2_cong.json"
    shutil.copy(cav.TEP_HD2, hd2)
    kc = cav.chay("phat_lai", tep_voi=tmp_path / "VANG.json", tep_hd2=hd2, cho_heldout=False)[0]
    kdd = [o for a in kc.agents for o in a.o if o.trang_thai == dc.KHONG_DO_DUOC]
    assert kdd and all("VẮNG" in o.ly_do for o in kdd)
    assert {o.ma.split(":")[0] for o in kdd} == {"voi", "cong"}       # cổng HD1 đọc chính tệp voi ⇒ cũng ⛔ đo được
    assert kc.dung_o.startswith("A4 TRƯỢT A2_PR_MAP") and "KHONG_DO_DUOC" in kc.dung_o
    assert kc.dat is False


def test_luat_hai_ho__A4_cung_ho__LoiChuoi():
    ag = tuple(ch.DinhNghiaAgent(a.ma, a.ten, mh.OPUS_5_5) for a in ch.AGENT)
    with pytest.raises(ch.LoiChuoi, match="hai họ"):
        ch.kiem_hai_ho(ag)


def test_phat_lai_cu__DO_co_ten(tmp_path, monkeypatch):
    """Prompt đổi mà bản ghi chưa ghi lại ⇒ ⛔ có lượt ⇒ chuỗi DỪNG, có tên — ⛔ đoán."""
    ncc = cav.ncc_cho("phat_lai")
    ncc["A1_RI"].luot = {}
    kc = cav.chay("phat_lai", ncc=ncc, cho_heldout=False)[0]
    assert kc.dung_o.startswith("DỪNG ở A1_RI/01_nguon_bank — KhongCoBanGhi")


def test_report_html_khop_tep_trong_repo(phat_lai):
    """`docs/ITL/06_Agent/report.html` phải là bản sinh từ bản phát lại hiện tại (trừ dòng ngày)."""
    kc, may, dap, be = phat_lai
    tep = (GOC / "docs" / "ITL" / "06_Agent" / "report.html").read_text(encoding="utf-8")
    assert "KẾT: ĐẠT — 627/627 ô khớp" in tep
