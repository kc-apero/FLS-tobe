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
#: 627 → 631 (vòng sửa sau KQ-331, AG-R1-02): gộp nhánh làm việc mang gói H14 `WP-C5c` ⇒ +3 ô `hd2` A3.04 · +1 ô
#: `cong:HD2` A4.03. Hai nhóm (AG-R1-01, Đ4): ĐỘC LẬP `voi` 557 · VÒNG TRÒN `hd2`+`cong`+`nguon` 74.
MONG_SO_O = 631
MONG_DOC_LAP = 557
MONG_VONG_TRON = 74


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
    nhom = dc.tom_tat_nhom([o for a in kc.agents for o in a.o])
    assert (nhom[dc.DOC_LAP]["mau_so"], nhom[dc.DOC_LAP][dc.KHOP]) == (MONG_DOC_LAP, MONG_DOC_LAP)
    assert (nhom[dc.VONG_TRON]["mau_so"], nhom[dc.VONG_TRON][dc.KHOP]) == (MONG_VONG_TRON, MONG_VONG_TRON)


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


def test_WO355_luat_hai_mo_hinh__A4_trung_mo_hinh__LoiChuoi():
    """WO-355: một hãng ⇒ luật hai HỌ thay bằng luật hai MÔ HÌNH. A4 = Opus như A1–A3 ⇒ ⛔ chạy; mặc định (Sonnet) ⇒ qua."""
    ag = tuple(ch.DinhNghiaAgent(a.ma, a.ten, mh.OPUS_5_5) for a in ch.AGENT)
    with pytest.raises(ch.LoiChuoi, match="hai mô hình"):
        ch.kiem_a4_khac_mo_hinh(ag)
    ch.kiem_a4_khac_mo_hinh()
    assert [a.mo_hinh.ma for a in ch.AGENT] == ["claude-opus-5-5"] * 3 + ["claude-sonnet-5-5"]
    assert {a.mo_hinh.ho for a in ch.AGENT} == {"anthropic"}


def test_phat_lai_cu__DO_co_ten(tmp_path, monkeypatch):
    """Prompt đổi mà bản ghi chưa ghi lại ⇒ ⛔ có lượt ⇒ chuỗi DỪNG, có tên — ⛔ đoán."""
    ncc = cav.ncc_cho("phat_lai")
    ncc["A1_RI"].luot = {}
    kc = cav.chay("phat_lai", ncc=ncc, cho_heldout=False)[0]
    assert kc.dung_o.startswith("DỪNG ở A1_RI/01_nguon_bank — KhongCoBanGhi")


def test_report_html_khop_tep_trong_repo(phat_lai):
    """`docs/ITL/06_Agent/report.html` phải là bản sinh từ bản phát lại hiện tại — BẰNG TỪNG BYTE (lấy ngày của tệp).

    Bản đầu chỉ tìm chuỗi `"KẾT: ĐẠT — 627/627 ô khớp"` ⇒ trang đổi khối nào khác cũng xanh.
    """
    import re
    kc, may, dap, be = phat_lai
    tep = (GOC / "docs" / "ITL" / "06_Agent" / "report.html").read_text(encoding="utf-8")
    ngay = re.findall(r"--ghi-report</code> · (\d{4}-\d{2}-\d{2})", tep)
    assert len(ngay) == 1
    html_, tom = cav.sinh_report(kc, may, dap, be, cav.ncc_cho("phat_lai"), ngay=ngay[0])
    assert tom["dat"] and html_ == tep


# ── AG-R1-01 · trung thực của report ─────────────────────────────────────────────────────────────────────────
def _o_hd2_dau(kc) -> str:
    return next(o.ma for a in kc.agents for o in a.o if o.ma.startswith("hd2:") and o.ma.endswith(".khop"))


def test_AG_R1_01_sua_hd2__o_VONG_TRON_van_khop__KHONG_duoc_dem_la_doc_lap(tmp_path, phat_lai):
    """Sửa `hd2_cong.json` ⇒ vẫn ĐẠT (vòng tròn: công cụ và máy cùng đọc tệp) — nên ô ấy ⛔ được vào nhóm ĐỘC LẬP,
    và mẫu số độc lập ⛔ đổi. Đối chứng cùng bài: sửa `voi_so_luong.json` ⇒ ô ĐỘC LẬP LECH 1 (nhóm độc lập có răng)."""
    ma = _o_hd2_dau(phat_lai[0])
    goi, truong = ma.split(":", 1)[1].split(".")
    d = json.loads(cav.TEP_HD2.read_text(encoding="utf-8"))
    (d[goi] if goi in d else d)[truong] -= 1
    hd2 = tmp_path / "hd2_cong.json"
    hd2.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    kc, may, dap, be = cav.chay("gia", tep_hd2=hd2, ncc=cav.ncc_cho("gia"), cho_heldout=False)
    assert kc.dat, "sửa hd2 mà ĐỎ ⇒ tiền đề vòng tròn đã đổi — khai lại AG-R1-01"
    o = [x for a in kc.agents for x in a.o if x.ma == ma]
    assert len(o) == 1 and o[0].trang_thai == dc.KHOP and dc.nhom_o(ma) == dc.VONG_TRON
    html_, tom = cav.sinh_report(kc, may, dap, be, cav.ncc_cho("gia"), ngay="2026-11-23")
    assert tom["doc_lap"] == {"mau_so": MONG_DOC_LAP, "khop": MONG_DOC_LAP}
    assert tom["vong_tron"] == {"mau_so": MONG_VONG_TRON, "khop": MONG_VONG_TRON}
    assert f"<code>{ma}</code></td><td>vòng tròn</td>" in html_

    v = json.loads(cav.TEP_VOI.read_text(encoding="utf-8"))
    v["bank_tong"]["dong_theo_hinh"]["A"] += 1
    voi = tmp_path / "voi_so_luong.json"
    voi.write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
    kc2 = cav.chay("gia", tep_voi=voi, ncc=cav.ncc_cho("gia"), cho_heldout=False)[0]
    lech = [x for a in kc2.agents for x in a.o if x.trang_thai == dc.LECH]
    assert [(x.ma, dc.nhom_o(x.ma)) for x in lech] == [("voi:bank_tong.dong_theo_hinh.A", dc.DOC_LAP)]


def test_AG_R1_01_trang_khai_chung_minh_gi__va_nhan_mo_hinh_GIA(phat_lai):
    kc, may, dap, be = phat_lai
    html_, tom = cav.sinh_report(kc, may, dap, be, cav.ncc_cho("phat_lai"), ngay="2026-11-23")
    assert "Báo cáo này chứng minh gì / ⛔ chứng minh gì" in html_
    assert html_.count("bản phát lại sinh bằng mô hình GIẢ") == 3            # A1 · A2 · A3 (A4 là mã)
    assert "<td>✅</td>" not in html_ and tom["mo_hinh_that"] == 0 and tom["nguon_tra_loi"] == ["gia-lap"]
    assert "câu trả lời do mô hình GIẢ (0 lượt API thật)" in rp.dong_ket(tom)
    # đối chứng: nguồn trả lời THẬT ⇒ nhãn GIẢ biến mất, ✅ được in (nhãn đọc từ nhà cung cấp, ⛔ hằng)
    pb = {a.dn.ma: {"nguon_tra_loi": "anthropic"} for a in kc.agents}
    html2, tom2 = rp.sinh(kc, pb, [], None, {}, "2026-11-23", may=may)
    assert "mô hình GIẢ" not in html2 and "<td>✅</td>" in html2 and tom2["mo_hinh_that"] == 3


def test_AG_R1_05_do_phu_khai_phan_KHONG_vao_mau_so(phat_lai):
    kc, may, dap, be = phat_lai
    html_, tom = cav.sinh_report(kc, may, dap, be, cav.ncc_cho("phat_lai"), ngay="2026-11-23")
    assert "Độ phủ — phần tệp đo ⛔ vào mẫu số" in html_
    # số đo KQ-331 (voi) · hd2 đổi theo gói WP-C5c của cây gộp
    assert tom["do_phu"]["voi"] == {"la": 1045, "la_vao": 557, "so": 660, "so_vao": 318}
    assert tom["do_phu"]["hd2"]["la_vao"] == 30 and tom["do_phu"]["hd2"]["la"] > 900


# ── AG-R1-06 · A4 mã thuần tới G1 (quyết chủ C2) ─────────────────────────────────────────────────────────────
def test_AG_R1_06_A4_ma_thuan__KHONG_dung_nha_cung_cap(monkeypatch, phat_lai):
    from fls.agent.skill import nap_bo
    assert {s.loai for s in nap_bo("A4_AUDITOR")} == {"ma"} and not ch.can_mo_hinh("A4_AUDITOR")
    goi: list[str] = []
    monkeypatch.setattr(cav.mh, "tao_that", lambda m, co, che_do="mo", **kw: goi.append(m.ma) or object())
    ncc = cav.ncc_cho("that", True)
    assert sorted(ncc) == ["A1_RI", "A2_PR_MAP", "A3_SI_ITL"] and goi == ["claude-opus-5-5"] * 3   # ⛔ Sonnet cho A4 hôm nay
    a4 = phat_lai[0].agents[3]
    assert [k.so_luot for k in a4.skills] == [0, 0, 0, 0] and a4.dat_a4
    assert {o.ma.split(":")[0] for o in a4.o} == {"cong", "voi"}               # ô A4 vẫn qua cửa ②
