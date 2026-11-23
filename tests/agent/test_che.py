# -*- coding: utf-8 -*-
"""WO-329 AC-3 — bộ che chạy TRƯỚC mọi lời gọi.

⭐ Chủ 23/11 (sau BG-330): mặc định `mo` — agent đọc TOÀN BỘ nội dung + số TK; chỉ bỏ `Email Address`
   (`PM_COT_RIENG_TU`). Hai chế độ che cũ giữ làm tuỳ chọn — các bài dưới gọi RÕ `che_het` / `che_noi_dung`.

Chứng minh bằng nhà cung cấp GIÁN ĐIỆP: nó ghi lại ĐÚNG byte nó nhận. Bài `..._KHONG_CHE__gian_diep_THAY_PII`
chứng minh phép thử có răng: bỏ bộ che ⇒ gián điệp thấy PII (Đ5 — cổng phải được thấy ĐỎ).
"""
from __future__ import annotations

import json

import pytest

from fls.agent import che, chuoi
from fls.agent.mo_hinh import GiaLap
from fls.agent.skill import nap_bo

# PII BỊA (⛔ người thật): tên · số TK · email · số chứng từ · diễn giải
TEN, TK, EMAIL, SO_CT = "NGUYEN VAN AN", "0123456789012", "ke.toan@vidu.vn", "FT25063123456789"
DIEN_GIAI = f"CK {TEN} {TK} {EMAIL}"


class GianDiep:
    ten = "gian-diep"

    def __init__(self):
        self.nhan: list[str] = []
        self.goc = GiaLap()

    def goi(self, yc):
        self.nhan.append(json.dumps(yc, ensure_ascii=False))
        return self.goc.goi(yc)


def _cong_cu_ban():
    return {"voi:tong.co": 9967, "Diễn giải": DIEN_GIAI, "Số chứng từ": SO_CT, "Tên tài khoản": TEN,
            "Email Address": EMAIL, "so_tai_khoan": TK, "voi:la.chuoi_la": DIEN_GIAI,
            "noi:c99.noi_dung": DIEN_GIAI}


def _chay(che_do="che_het"):
    gd = GianDiep()
    s = nap_bo("A1_RI")[0]
    dn = chuoi.AGENT[0]
    ks = chuoi.chay_skill(dn, "he thong", s, gd, {s.cong_cu: _cong_cu_ban}, che_do=che_do)
    return gd, ks


@pytest.mark.parametrize("pii", [TEN, TK, EMAIL, SO_CT, DIEN_GIAI, "Diễn giải", "Số chứng từ", "Tên tài khoản",
                                 "Email Address"])
def test_nam_thu_cam_KHONG_roi_may(pii):
    gd, ks = _chay()
    assert gd.nhan, "gián điệp ⛔ nhận gì ⇒ phép thử rỗng (Đ3)"
    assert len(gd.nhan) == 2                       # lượt gọi công cụ + lượt có tool_result
    assert all(pii not in x for x in gd.nhan), f"`{pii}` rời máy"
    assert ks.so_bo_che == 7                       # 5 khoá cấm bỏ + 2 ô bị thay null (chuỗi lạ · nội dung TẮT)


def test_o_hop_le_VAN_di_qua():
    gd, _ = _chay()
    assert '\\"voi:tong.co\\": 9967' in gd.nhan[-1]


def test_KHONG_CHE__gian_diep_THAY_PII(monkeypatch):
    """Phá bộ che (đồng nhất) ⇒ PII tới gián điệp — chứng minh bài trên có răng."""
    monkeypatch.setattr(che, "che_yeu_cau", lambda yc, che_do="mo": (yc, che.BaoCaoChe()))
    gd, _ = _chay()
    assert any(TK in x for x in gd.nhan)


def test_noi_dung_TAT_mac_dinh__BAT_thi_da_che():
    gd, _ = _chay("che_het")
    assert '\\"noi:c99.noi_dung\\": null' in gd.nhan[-1]
    gd2, ks2 = _chay("che_noi_dung")
    cuoi = gd2.nhan[-1]
    assert "<TEN> <SO> <EMAIL>" in cuoi and TEN not in cuoi and TK not in cuoi and EMAIL not in cuoi
    assert ks2.the_noi_dung == 3


def test_lop2_chan_PII_trong_prompt():
    yc = {"model": "m", "system": f"liên hệ {EMAIL}", "messages": [{"role": "user", "content": "x"}]}
    with pytest.raises(che.CamGui):
        che.che_yeu_cau(yc, "che_het")
    yc2 = {"model": "m", "system": "s", "messages": [{"role": "user", "content": f"TK {TK}"}]}
    with pytest.raises(che.CamGui):
        che.che_yeu_cau(yc2, "che_het")


def test_lop2_KHONG_bat_so_tien_dang_so_va_van_tay_hex():
    yc = {"model": "m", "system": "s", "messages": [{"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "t", "content": json.dumps(
            {"noi:c1.tien": 120000000, "nguon:gi.van_tay": "0e39e49cd95901ed", "voi:a.b": 1234567890})}]}]}
    ra, bc = che.che_yeu_cau(yc, "che_het")
    assert bc.so_bo == 0 and "120000000" in json.dumps(ra)


def test_che_ten_KHONG_nuot_ma_PM():
    """Bia của lỗi 23/11: bản đầu nuốt `PM` ⇒ mã mất ⇒ ca c12 trượt ghép."""
    assert che.che_noi_dung("TRAN THI B PM-1201-01 tam ung")[0] == "<TEN> PM-1201-01 tam ung"


# ── AG-R1-03 · ca khó (chuỗi BỊA của KQ-331 — ⛔ người thật) ──────────────────────────────────────────────────
CA_KHO = [
    ("CK 1234.5678.9012 tien hang", "1234.5678.9012"),          # số TK chấm
    ("TK 0123-4567-8901-2 nhan", "0123-4567-8901-2"),            # số TK gạch
    ("the 9704-1234-5678-9012", "9704-1234-5678-9012"),          # số thẻ gạch
    ("the 9704 1234 5678 9012", "9704 1234 5678 9012"),          # số thẻ cách
    ("goi 098-765-4321 xac nhan", "098-765-4321"),               # điện thoại gạch
    ("Vo Thi Lan chuyen tien", "Vo Thi Lan"),                    # tên Hoa-thường
    ("hoan ung Nguyen Van An", "Nguyen Van An"),                 # tên Hoa-thường, giữa câu
]


@pytest.mark.parametrize("van,bi_mat", CA_KHO)
def test_AG_R1_03_ca_kho__che_noi_dung_BAT(van, bi_mat):
    ra, n = che.che_noi_dung(van)
    assert bi_mat not in ra and n >= 1, ra
    assert not any(t in ra for t in bi_mat.replace(".", " ").replace("-", " ").split() if len(t) >= 3), ra


@pytest.mark.parametrize("van,bi_mat", [c for c in CA_KHO if any(ch.isdigit() for ch in c[1])])
def test_AG_R1_03_lop2_bat_cum_so_CO_DAU(van, bi_mat):
    """Lớp 2 (`kiem_den`): cụm ≥ 9 chữ số SAU KHI BỎ DẤU ⇒ `CamGui` — kể cả khi lớp 1 bị vượt (prompt)."""
    yc = {"model": "m", "system": "s", "messages": [{"role": "user", "content": van}]}
    with pytest.raises(che.CamGui, match="dãy ≥ 9"):
        che.che_yeu_cau(yc, "che_het")


def test_AG_R1_03_co_RANG__bo_luat_cum_so_thi_LOT(monkeypatch):
    """Phá luật cụm (về bản cũ chỉ bắt dãy liền) ⇒ ca khó LỌT ⇒ hai bài trên có răng (Đ5)."""
    monkeypatch.setattr(che, "cum_so_dai", lambda van, toi_thieu: [])
    assert "1234.5678.9012" in che.che_noi_dung(CA_KHO[0][0])[0]
    assert che.kiem_den({"messages": [{"role": "user", "content": CA_KHO[1][0]}]}) == []


def test_AG_R1_03_KHONG_che_nham__ky_ngay_ma_PM_chu_thuong():
    for van in ("ky 2025-01 2025-02 ngay 2026-08-26", "PM-1201-01 tam ung do to ha", "so tien 15.000"):
        assert che.che_noi_dung(van) == (van, 0)
    assert che.kiem_den({"messages": [{"role": "user", "content": "ky 2025-01 2025-02 2025-03 ngay 2026-08-26"}]}) == []


def test_MAC_DINH_mo__noi_dung_va_so_TK_di_nguyen__chi_bo_Email_Address():
    """Quyết định chủ 23/11: agent học mapping từ nội dung + số TK ⇒ ⛔ che. `Email Address` vẫn bỏ (CLAUDE.md)."""
    assert che.CHE_DO_MAC_DINH == "mo"
    gd = GianDiep()
    s = nap_bo("A1_RI")[0]
    ks = chuoi.chay_skill(chuoi.AGENT[0], "he thong", s, gd, {s.cong_cu: _cong_cu_ban})
    cuoi = gd.nhan[-1]
    assert TK in cuoi and TEN in cuoi and SO_CT in cuoi and "Diễn giải" in cuoi
    assert "Email Address" not in cuoi and ks.so_bo_che == 1


def test_che_do_la__ValueError():
    with pytest.raises(ValueError):
        che.che_yeu_cau({"messages": []}, "khong-co")
