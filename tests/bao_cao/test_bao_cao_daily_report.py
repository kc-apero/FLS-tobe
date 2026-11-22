"""`fls.bao_cao.bao_cao` — RP.PL · RP.CF dựng theo khuôn *(ISP 3.1.2 · Step 46 · H14 · `WO-311`)*: bài ĐƠN VỊ trên lưới
tổng hợp *(⛔ kho, ⛔ tệp)*.

AC-2 `H14-B2`: FS1 · FS2 · FS3 = CÙNG engine khác tham số — đổi FS ⇒ ĐÚNG phần luỹ kế đổi, phần ngày giữ từng byte.
AC-3: đầu ra là JSON THUẦN theo hợp đồng C13 *(`ban_ky.checksum` nhận; cùng đầu vào ⇒ cùng checksum)*.
AC-4: đầu vào = lưới engine — đột biến 1 ô đầu vào ⇒ ĐÚNG ô báo cáo chiếu từ nó đổi, ⛔ ô nào khác.
"""
from __future__ import annotations

import datetime
import json
from decimal import Decimal

import pytest

from fls.bao_cao import bao_cao as bc
from fls.cau_hinh import ban_ky

KY = 202511
NGAY = [datetime.date(2025, 11, d) for d in range(1, 31)]
SER = [(d - datetime.date(1899, 12, 30)).days for d in NGAY]
KY_2025 = bc.cot_ky(2025)
KHOI_E = ("GROUP", "SGO2", "SGO1", "HGO6", "BGO2", "CVL", "COR", "CSM", "CAH", "ASA", "SHQ1", "SHQ2")
MA = ("GI", "OMC", "NB")


def _luoi_ngay() -> dict:
    return {(k, m, s): Decimal(i % 7) / 100 for i, (k, m, s) in
            enumerate((k, m, s) for k in KHOI_E[:5] for m in MA for s in SER)}


def _luoi_ky() -> dict:
    return {(k, m, t): Decimal(i % 11) / 10 for i, (k, m, t) in
            enumerate((k, m, t) for k in KHOI_E for m in MA for t in KY_2025)}


def _nguon(**sua) -> dict:
    n = {"pla3_daily": _luoi_ngay(), "atl": _luoi_ky()}
    n.update(sua)
    return n


def _phan(bao: dict, ph: str) -> dict:
    return {k: v for k, v in bao["o"].items() if k.split("|")[0] == ph}


# ── tham số hỏng ⇒ lỗi CÓ TÊN ─────────────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("ky", ["2025-13", "20251", "abc", 2025111])
def test_ky_hong_loi_co_ten(ky):
    with pytest.raises(bc.LoiBaoCao, match="ky="):
        bc.rp_pl(ky, "FS2", _nguon())


@pytest.mark.parametrize("fs", ["FS4", "", "fs2", None])
def test_fs_ngoai_tap_loi_co_ten(fs):
    with pytest.raises(bc.LoiBaoCao, match="fs="):
        bc.rp_pl(KY, fs, _nguon())


def test_ky_hai_khuon_cung_nghia():
    assert bc.rp_pl("2025-11", "FS2", _nguon()) == bc.rp_pl(202511, "FS2", _nguon())


# ── AC-2 · FS là THAM SỐ ──────────────────────────────────────────────────────────────────────────────────────────────

def test_AC2_FS_cung_engine_khac_tham_so():
    b1, b2, b3 = (bc.rp_pl(KY, fs, _nguon()) for fs in ("FS1", "FS2", "FS3"))
    ngay = _phan(b2, "ngay")
    assert len(ngay) == 5 * len(MA) * 30                              # Đ3: phần chung ⛔ rỗng (5 khối LE × 3 mã × 30 ngày)
    assert _phan(b1, "ngay") == ngay == _phan(b3, "ngay")              # phần CHUNG giữ từng ô
    assert [p["id"] for p in b1["phan"]] == ["ngay", "luy_ke:FS1"]
    assert [p["id"] for p in b2["phan"]] == ["ngay", "luy_ke:FS2"]
    assert [p["id"] for p in b3["phan"]] == ["ngay", "luy_ke:FS1", "luy_ke:FS2"]
    assert len(_phan(b2, "luy_ke:FS2")) == 11 * len(MA) * 19          # 11 nhãn khối (SHQ gộp) × 3 mã × 19 kỳ
    assert _phan(b3, "luy_ke:FS2") == _phan(b2, "luy_ke:FS2")
    assert b3["o"] == {**b1["o"], **b2["o"]}                            # FS3 = HỢP hai bản, ⛔ ô lạ


def test_AC2_FS1_thieu_nguon_DUNG_co_ten_khong_ngam_0():
    b1 = bc.rp_pl(KY, "FS1", _nguon())
    assert _phan(b1, "luy_ke:FS1") == {}
    (c,) = b1["chua_co_dau_vao"]
    assert (c["phan"], c["nguon"]) == ("luy_ke:FS1", "atl_fs1") and "FS1" in c["can"]
    assert c["khoi"] == ["GROUP", "CVL", "COR", "CSM", "CAH", "ASA", "SHQ"]
    # có nguồn ⇒ hết dừng, cùng engine
    b1b = bc.rp_pl(KY, "FS1", _nguon(atl_fs1=_luoi_ky()))
    assert b1b["chua_co_dau_vao"] == [] and len(_phan(b1b, "luy_ke:FS1")) == 7 * len(MA) * 19


def test_khoi_SHQ_la_tong_SHQ1_SHQ2_HGO2_la_HGO6():
    n = _nguon()
    b = bc.rp_pl(KY, "FS2", n)
    for t in KY_2025:
        assert Decimal(b["o"][f"luy_ke:FS2|SHQ|GI|{t}"]) == n["atl"][("SHQ1", "GI", t)] + n["atl"][("SHQ2", "GI", t)]
        assert Decimal(b["o"][f"luy_ke:FS2|HGO2|OMC|{t}"]) == n["atl"][("HGO6", "OMC", t)]
    assert not [k for k in b["o"] if "|HGO6|" in k or "|SHQ1|" in k]


def test_tong_do_dang_khong_in():
    """SHQ thiếu MỘT phần ⇒ ô ⛔ in *(⛔ tổng dở, ⛔ 0)*."""
    a = _luoi_ky()
    del a[("SHQ2", "GI", "2025M03")]
    b = bc.rp_pl(KY, "FS2", _nguon(atl=a))
    assert "luy_ke:FS2|SHQ|GI|2025M03" not in b["o"] and "luy_ke:FS2|SHQ|GI|2025M04" in b["o"]


def test_truc_ngay_theo_thang_thang_12_co_31():
    b = bc.rp_pl(202512, "FS2", _nguon(pla3_daily={("GROUP", "GI", 46022): Decimal(1)}))
    assert b["o"] == {"ngay|GROUP|GI|2025-12-31": "1", **_phan(b, "luy_ke:FS2")}
    assert len(next(p for p in b["phan"] if p["id"] == "ngay")["cot"]) == 31


def test_CF_hai_nam_luy_ke_va_hr_dung():
    b = bc.rp_cf(202611, {"cfa1_daily": {("GROUP", "GI", 46327): Decimal(2)},
                          "cfa1_yhqm": {("GROUP", "GI", "2025M01"): Decimal(3), ("GROUP", "GI", "2026"): Decimal(4)}})
    assert b["fs"] is None and b["loai"] == "CF"
    assert b["o"]["ngay|GROUP|GI|2026-11-01"] == "2"
    assert b["o"]["luy_ke|GROUP|GI|2025M01"] == "3" and b["o"]["luy_ke|GROUP|GI|2026"] == "4"
    assert [c["phan"] for c in b["chua_co_dau_vao"]] == ["hr"]


# ── AC-3 · JSON THUẦN theo hợp đồng C13 ───────────────────────────────────────────────────────────────────────────────

def test_AC3_json_thuan_checksum_on_dinh():
    b = bc.rp_pl(KY, "FS3", _nguon())
    s = json.dumps(b, sort_keys=True, ensure_ascii=False, allow_nan=False)  # ⛔ Decimal/date lọt
    assert json.loads(s) == b
    assert ban_ky.checksum(b) == ban_ky.checksum(bc.rp_pl(KY, "FS3", _nguon()))
    assert ban_ky.checksum(b) != ban_ky.checksum(bc.rp_pl(KY, "FS2", _nguon()))


# ── AC-4 · đột biến 1 ô đầu vào ⇒ đúng ô báo cáo ─────────────────────────────────────────────────────────────────────

def _khac(a: dict, b: dict) -> set:
    return {k for k in set(a["o"]) | set(b["o"]) if a["o"].get(k) != b["o"].get(k)}


def test_AC4_dot_bien_mot_o_ngay_dung_mot_o_bao_cao():
    n = _nguon()
    d = _luoi_ngay()
    d[("HGO6", "OMC", SER[4])] += Decimal("0.001")
    assert _khac(bc.rp_pl(KY, "FS3", n), bc.rp_pl(KY, "FS3", _nguon(pla3_daily=d))) == {"ngay|HGO2|OMC|2025-11-05"}


def test_AC4_dot_bien_SHQ1_dung_o_SHQ_moi_ban_FS():
    a = _luoi_ky()
    a[("SHQ1", "NB", "2025Q2")] += Decimal(1)
    kq = _khac(bc.rp_pl(KY, "FS3", _nguon(atl_fs1=_luoi_ky())), bc.rp_pl(KY, "FS3", _nguon(atl=a, atl_fs1=_luoi_ky())))
    assert kq == {"luy_ke:FS2|SHQ|NB|2025Q2"}                           # FS1 có nguồn RIÊNG ⇒ ⛔ đổi


def test_dau_vao_ngoai_thang_khong_lot():
    """Ô đầu vào ngoài tháng `ky` ⇒ ⛔ vào báo cáo *(trục = tháng của kỳ)*."""
    n = _nguon()
    d = dict(n["pla3_daily"])
    d[("GROUP", "GI", SER[0] - 1)] = Decimal(99)
    assert _khac(bc.rp_pl(KY, "FS2", n), bc.rp_pl(KY, "FS2", _nguon(pla3_daily=d))) == set()


# ── CHECK: chỉ đếm + liệt kê ──────────────────────────────────────────────────────────────────────────────────────────

def test_check_chi_dem_va_liet_ke():
    from fls.cau_hinh import dong_pl
    b = bc.rp_pl(KY, "FS2", _nguon())
    ch = b["check"]
    tong = sum(sum(d.values()) for x in ch["theo_phan"].values() for d in x.values())
    assert tong == 2 * (5 * 30 + 11 * 19)                               # Đ3: mỗi (phần, khối, cột) × 2 phép
    # lưới thiếu mã CHECK ⇒ MỌI ô `khong_do_duoc` *(⛔ "đạt")*
    assert all(d["khong_do_duoc"] == sum(d.values()) for x in ch["theo_phan"].values() for d in x.values())
    # đủ mã, mọi vế 0 trừ NB một ô ⇒ đúng MỘT đỏ có tên, ⛔ phán
    ma = sorted({m for _, tr, ph in dong_pl.CHECK for m in tr + ph})
    d = {("GROUP", m, s): Decimal(0) for m in ma for s in SER}
    d[("GROUP", "NB", SER[2])] = Decimal("0.25")
    b = bc.rp_pl(KY, "FS2", _nguon(pla3_daily=d))
    assert b["check"]["do"] == ["ngay|GROUP|2025-11-03|NB = 0: 0.250000000"]
    assert b["check"]["theo_phan"]["ngay"]["NB = 0"] == {"dat_co_so": 0, "dat_0_0": 29, "do": 1, "khong_do_duoc": 120}  # 4 khối LE ⛔ mã
