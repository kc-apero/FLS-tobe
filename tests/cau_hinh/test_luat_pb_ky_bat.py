# -*- coding: utf-8 -*-
"""Vòng sửa R1 `H12` *(`KQ-293` · `H12-R1-01`)* — **bật cờ IX.ALR có KÝ** *(quyết của chủ 22/11 ~10:05 UTC:
"ĐỒNG Ý ký BẬT luật phân bổ IX.ALR năm 2025 giống AS-IS" — `TIEN_DO.md`)*.

⭐ D2 giữ nguyên ở đường NẠP: `nap_ix_alr`/`dung_tu_mm` ⛔ bao giờ ra `bat=True`; `kiem` từ chối `bat=True`
   KHÔNG kèm chữ ký *(bài C11 `test_C11_D2_bat_true_trong_ban_nap_thi_LoiLuatPB` giữ nguyên)*. Bật cờ đi
   đường RIÊNG `dung_tu_tep_ky` ← tệp config CÓ PHIÊN BẢN trong repo *(`tests/fixture/cau_hinh/ix_alr_2025_bat.json`)*
   mang người ký *(tên, ⛔ email)* + căn cứ + ngày; mỗi dòng luật bật/tắt mang chữ ký ấy vào kho.
Dữ liệu TỔNG HỢP ở đây; tệp THẬT đo ở cuối tệp *(đếm `mong` hai chiều — Đ5)*.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from fls.cau_hinh import luat_pb as lp

GOC = Path(__file__).resolve().parents[2]
TEP_KY = GOC / "tests" / "fixture" / "cau_hinh" / "ix_alr_2025_bat.json"
ANH_MM = GOC / "tests" / "fixture" / "cau_hinh" / "mapping_master_cfg.json"
NEED = "Need to Allocate to CFA2"
KY = {"nguoi_ky": "Chu So", "ngay": "2026-11-22", "can_cu": "bai tong hop"}


def _bang() -> lp.BangALR:
    mm = [{"hd_code": f"G{i:02d} | gi", "need_cfa2": NEED, "method_cfa2": "By GI"} for i in range(8)]
    mm += [{"hd_code": f"{'OFR' if i == 0 else f'N{i:02d}'} | noem", "need_cfa2": NEED,
            "method_cfa2": "By NOEM"} for i in range(5)]
    mm += [{"hd_code": f"H{i:02d} | h", "need_cfa2": NEED, "method_cfa2": "H1000 Ledger"} for i in range(4)]
    return lp.kiem(lp.dung_tu_mm(mm, tu_ky=202501), nguon="bai")


def _tep(**sua):
    t = {"bang": "IX.ALR", "loai": lp.LOAI_TEP_KY, "phien_ban_tep": 1, "ky": dict(KY),
         "mong_dem": {"bat": {"BY_GI": 1, "BY_NOEM": 1}, "tat": {"BY_GI": 1}},
         "luat": [{"hd": "G00", "tu_ky": 202502, "bat": True}, {"hd": "OFR", "tu_ky": 202501, "bat": True},
                  {"hd": "G00", "tu_ky": 202601, "bat": False}]}
    t.update(sua)
    return t


def _gop(hien: lp.BangALR, moi: list[dict]) -> lp.BangALR:
    d = {lp.khoa_cua(x.hd, x.tu_ky): {"hd": x.hd, "tu_ky": x.tu_ky, "nhan_mm": x.nhan_mm, "bat": x.bat,
                                      "ngoai_le": list(x.ngoai_le_cdt1)} for x in hien.luat}
    d.update({lp.khoa_cua(r["hd"], r["tu_ky"]): r for r in moi})
    return lp.kiem(list(d.values()), nguon="gop")


def test_ky_bat__dong_mang_chu_ky_va_lay_nhan_cua_luat_hien_hanh():
    hien = _bang()
    moi = lp.dung_tu_tep_ky(_tep(), hien)
    assert [(r["hd"], r["tu_ky"], r["bat"]) for r in moi] == [("G00", 202502, True), ("OFR", 202501, True),
                                                                ("G00", 202601, False)]
    assert all(r["ky"] == KY for r in moi)
    assert moi[1]["ngoai_le"] == ["CAH"] and moi[0]["nhan_mm"] == "By GI"     # ngoại lệ AP chở theo
    b = _gop(hien, moi)
    assert b.luat_cua("G00", 202501).bat is False                              # trước mốc ký: TẮT (D2)
    x = b.luat_cua("G00", 202507)
    assert x.bat is True and x.nguoi_ky == "Chu So" and x.driver == "PE"
    assert b.luat_cua("G00", 202601).bat is False                              # tắt lại từ 2026
    assert b.luat_cua("OFR", 202503, cdt1="CAH").phuong_phap is None           # ngoại lệ vẫn là ngoại lệ
    assert b.luat_cua("OFR", 202503, cdt1="CVL").bat is True
    assert b.luat_cua("N01", 202503).bat is False                              # mã ⛔ có trong tệp ký: TẮT


def test_kiem__bat_true_khong_chu_ky_van_D2():
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.kiem([{"hd": "G00", "tu_ky": 202501, "nhan_mm": "By GI", "bat": True, "ngoai_le": []}], nguon="x")
    assert "D2" in str(e.value)


@pytest.mark.parametrize("ky, mau", [
    ({**KY, "nguoi_ky": "chu@vi.du"}, "email"),
    ({**KY, "nguoi_ky": "  "}, "nguoi_ky"),
    ({**KY, "can_cu": ""}, "can_cu"),
    ({**KY, "ngay": "2026-13-01"}, "ngay"),
    ({**KY, "ngay": "2999-01-01"}, "tương lai"),
    ({"nguoi_ky": "A", "ngay": "2026-11-22"}, "thiếu"),
    ({**KY, "la": 1}, "lạ"),
    ("A", "đối tượng"),
])
def test_kiem__chu_ky_hong_CO_TEN(ky, mau):
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.kiem([{"hd": "G00", "tu_ky": 202501, "nhan_mm": "By GI", "bat": True, "ngoai_le": [], "ky": ky}],
                nguon="x")
    assert mau in str(e.value), str(e.value)


@pytest.mark.parametrize("sua, mau", [
    ({"loai": "khac"}, "loai"),
    ({"bang": "IX.DRV"}, "bang"),
    ({"phien_ban_tep": 0}, "phien_ban_tep"),
    ({"mong_dem": {"bat": {"BY_GI": 2, "BY_NOEM": 1}, "tat": {"BY_GI": 1}}}, "mong"),     # thừa mong
    ({"mong_dem": {"bat": {"BY_GI": 1}, "tat": {"BY_GI": 1}}}, "mong"),                  # thiếu mong
    ({"luat": [{"hd": "ZZZ", "tu_ky": 202502, "bat": True}]}, "⛔ có luật"),
    ({"luat": [{"hd": "H00", "tu_ky": 202502, "bat": True}]}, "driver"),                 # H1000 ⛔ chia (Q3)
    ({"luat": [{"hd": "G00", "tu_ky": 202502, "bat": "true"}]}, "bool"),
    ({"luat": [{"hd": "G00", "tu_ky": 202502, "bat": True, "nhan_mm": "By NOEM"}]}, "cột lạ"),
    ({"luat": []}, "0 dòng"),
])
def test_tep_ky_hong__LoiLuatPB_CO_TEN(sua, mau):
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.dung_tu_tep_ky(_tep(**sua), _bang())
    assert mau in str(e.value), str(e.value)


# ── tệp THẬT *(config có phiên bản trong repo)* ───────────────────────────────────────────────────

def _tep_that() -> dict:
    return json.loads(TEP_KY.read_text(encoding="utf-8"))


def _hien_that() -> lp.BangALR:
    anh = json.loads(ANH_MM.read_text(encoding="utf-8"))
    chu = (lambda o: o.get("chu") if isinstance(o, dict) else o)
    mm = [{k: chu(r.get(k)) for k in ("hd_code", "need_cfa2", "method_cfa2")} for r in anh["dong"]]
    return lp.kiem(lp.dung_tu_mm(mm, tu_ky=202501), nguon="anh")


def test_tep_that__2025_bat_giong_AS_IS_ky_boi_chu():
    """Đếm `mong` *(khai TRƯỚC — Đ5)*: By GI **8** mã bật từ `202502` *(D3 driver PE: `GI_PE 202501` thiếu ở
    IX.DRV — 7 ô `MID3 thiếu TOTAL 202501`)* · By NOEM **5** mã bật từ `202501` · cả 13 tắt từ `202601`
    *(ATL 2026 ⛔ có công thức phân bổ)*. Người ký có TÊN, ⛔ email."""
    t = _tep_that()
    hien = _hien_that()
    moi = lp.dung_tu_tep_ky(t, hien)
    assert t["ky"]["nguoi_ky"] == "KhanhCQ" and "@" not in json.dumps(t)
    bat = sorted((r["hd"], r["tu_ky"]) for r in moi if r["bat"])
    tat = sorted((r["hd"], r["tu_ky"]) for r in moi if not r["bat"])
    gi = {"LC", "BRC", "CXP", "OSF", "FNS", "CIO", "CXB", "CXO"}
    noem = {"BON", "HCC", "OFR", "OGA", "REC"}
    assert bat == sorted([(h, 202502) for h in gi] + [(h, 202501) for h in noem])
    assert tat == sorted((h, 202601) for h in gi | noem)
    assert {x.hd for x in hien.luat if x.phuong_phap == lp.BY_GI} == gi            # đúng tập C11 (Đ2: hai nguồn)
    assert {x.hd for x in hien.luat if x.phuong_phap == lp.BY_NOEM} == noem
    b = _gop(hien, moi)
    assert sum(1 for x in b.luat if x.bat) == 13 and len(b.luat) == 17 + 13 * 2 - 5   # NOEM@202501 thay bản tắt
    assert b.luat_cua("LC", 202501).bat is False and b.luat_cua("LC", 202502).bat is True
    assert b.luat_cua("HCC", 202501).bat is True and b.luat_cua("HCC", 202601).bat is False
    assert b.luat_cua("NIS", 202503).khong_qua_allocate and not b.luat_cua("NIS", 202503).bat   # H1000 ⛔ đụng


def test_tep_that__dot_bien_mong_DO():
    t = copy.deepcopy(_tep_that())
    t["mong_dem"]["bat"]["BY_GI"] += 1
    with pytest.raises(lp.LoiLuatPB):
        lp.dung_tu_tep_ky(t, _hien_that())
