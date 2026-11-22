"""Cổng `WP-C5a` *(ISP 3.1.2 · Step 42 · H12 · `WO-291`)* — AL.KEY cờ TẮT ↔ ATL 606 *(+ tham chiếu 604)*.

AC-3: mẫu số khai TRƯỚC + nhãn Đ4; lệch `mong` hai chiều *(Đ5)*; khối `hd2_cong.json` theo hợp đồng CG2.
AC-4: đột biến 1 ô đầu vào PLA3 ⇒ đúng ô ATL tương ứng ĐỎ *(⛔ vòng tròn)*. AC-5: cờ đọc từ kho IX.ALR.
"""
from __future__ import annotations

import copy
import dataclasses
import datetime
import json
import sys
from decimal import Decimal
from pathlib import Path

import psycopg
import pytest

GOC = Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.bao_cao import pla  # noqa: E402
from fls.cau_hinh import luat_pb  # noqa: E402
from fls.cau_hinh.ky import LichKy  # noqa: E402
from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2_c5a as c5a  # noqa: E402

LICH = LichKy(nguon="bai-h12", ngay_dau=datetime.date(2024, 10, 21), luat="A")
DEN = datetime.date(2026, 2, 27)
#: mẫu số khai TRƯỚC *(Đ4 — ô so: hàng ATL có nhãn × 57 kỳ, ⛔ mã trong, ô là số)*
MONG_TONG_O, MONG_KHOP, MONG_LECH = 45674, 39843, 5831


@pytest.fixture(scope="module")
def nguon():
    gl, hr, _, fx, cay, atl, drv = c5a.nap_nguon()
    return c5a.tinh_pla3(gl, hr, fx, cay, LICH, DEN), atl, drv, cay


@pytest.fixture(scope="module")
def alr():
    return c5a.alr_tu_anh_mm()


def _chay(nguon, alr, mong=None, **thay):
    p, atl, drv, cay = nguon
    return c5a.so_sanh_c5a(thay.get("pla3", p), thay.get("atl", atl), thay.get("drv", drv), thay.get("alr_khac", alr),
                           cay, mong or c5a.mong_c5a_mac_dinh())


@pytest.fixture(scope="module")
def tq(nguon, alr):
    return _chay(nguon, alr)


def _sua(**sua) -> c5a.MongC5a:
    m = copy.deepcopy(dict(c5a.mong_c5a_mac_dinh().so))
    for k, v in sua.items():
        m[k] = v
    return c5a.MongC5a(so=m)


# ── AC-3 ─────────────────────────────────────────────────────────────────────────────────────────

def test_AC3_cong_DAT_mau_so_khai_truoc(tq):
    h = tq.hd2_cong
    assert tq.phan_xu.dat, tq.phan_xu.ly_do
    assert (h["tong_o"], h["khop"], h["lech_co_chu_dich"], h["lech_ngoai_ten"]) == (MONG_TONG_O, MONG_KHOP, MONG_LECH, 0)
    assert h["khop"] + h["lech_co_chu_dich"] == h["tong_o"] == h["mong_tong_o"]
    assert h["o_co_so"] + h["o_0_0"] == h["tong_o"] and h["khop_co_so"] + h["o_0_0"] == h["khop"]
    assert h["khop_co_so"] > 0, "Đ3: khớp toàn ô 0 = 0 ⇒ xanh trên tập rỗng"
    assert h["mong_lech_co_chu_dich"] == h["lech_co_chu_dich"]
    lt = h["lech_co_ten"]
    assert (len(lt["o_lech"]), lt["as_is_bat_phan_bo_2025"]["so_o"], lt["as_is_truoc_CA"]["so_o"]) == (224, 4932, 675)
    assert (lt["khong_so_duoc"], lt["o_trong"], lt["hang_khong_nhan_khac_0"]) == (154, 741, 7)
    assert h["tham_chieu_604"] == {"o_so": 36, "khop": 36, "o_drv": 238, "o_thieu": 146, "sigma_7": 34}


def test_AC3_atl_rong__DO(nguon, alr):
    p, atl, drv, cay = nguon
    rong = {**atl, "dong": []}
    t = _chay(nguon, alr, atl=rong)
    assert not t.phan_xu.dat and any("0 ô được so" in x for x in t.phan_xu.ly_do)


def test_AC3_mong_chua_khai__DO(nguon, alr):
    t = _chay(nguon, alr, mong=c5a.MongC5a(so=None))
    assert not t.phan_xu.dat and any("chưa khai" in x for x in t.phan_xu.ly_do)


@pytest.mark.parametrize("sua, mau", [
    ({"tong_o": MONG_TONG_O + 1}, "tong_o"),
    ({"o_lech": {}}, "ngoài tên"),                                    # bỏ khai 224 ô ⇒ ngoài tên
    ({"o_lech_them": True}, "nay KHỚP"),                              # khai thừa một ô ⇒ chiều ngược
    ({"sha": True}, "sha256"),
    ({"dem_khoi": True}, "theo_khoi"),
    ({"gia_tri": True}, "ngoài tên"),                                 # đổi GIÁ TRỊ một ô khai từng ô
])
def test_AC3_mong_hai_chieu__DO(nguon, alr, sua, mau):
    m = copy.deepcopy(dict(c5a.mong_c5a_mac_dinh().so))
    if "tong_o" in sua:
        m["tong_o"] = sua["tong_o"]
    if "o_lech" in sua:
        m["o_lech"] = {}
    if "o_lech_them" in sua:
        m["o_lech"] = {**m["o_lech"], "GROUP#GI#2025": ["0", "0"]}
    if "sha" in sua:
        m["lop_quy_tac"]["as_is_truoc_CA"]["sha256"] = "0" * 64
    if "dem_khoi" in sua:
        m["lop_quy_tac"]["as_is_bat_phan_bo_2025"]["theo_khoi"]["CVL"] += 1
    if "gia_tri" in sua:
        k = next(iter(m["o_lech"]))
        m["o_lech"][k] = [m["o_lech"][k][0], str(Decimal(m["o_lech"][k][1]) + 1)]
    t = _chay(nguon, alr, mong=c5a.MongC5a(so=m))
    assert not t.phan_xu.dat and any(mau in x for x in t.phan_xu.ly_do), t.phan_xu.ly_do[:3]


def test_AC3_lop_quy_tac_chi_khoi_CDT_SHQ2_va_nam_2024_2025():
    assert c5a._lop({"o": "CVL#LC#2025M03"}) == "as_is_bat_phan_bo_2025"
    assert c5a._lop({"o": "SHQ2#GI#2024Q4"}) == "as_is_truoc_CA"
    assert c5a._lop({"o": "CVL#LC#2026M01"}) is None           # 2026 ⛔ có lớp ⇒ lệch ngoài tên
    assert c5a._lop({"o": "GROUP#LC#2025M03"}) is None and c5a._lop({"o": "SGO1#DC#2025"}) is None


def test_AC3_604_lech__DO(nguon, alr):
    p, atl, drv, cay = nguon
    a2 = copy.deepcopy(atl)
    a2["phu"]["pd604_ky"]["dong"][0]["m05"] = "6"
    t = _chay(nguon, alr, atl=a2)
    assert not t.phan_xu.dat and any("604" in x for x in t.phan_xu.ly_do)


# ── AC-4 · ⛔ vòng tròn ──────────────────────────────────────────────────────────────────────────

def test_AC4_dot_bien_mot_o_dau_vao_PLA3__dung_o_ATL_DO(nguon, alr):
    p, atl, drv, cay = nguon
    la = dict(p.la)
    la[("SGO2", "OFR", "2025M05")] += Decimal("1e-6")
    p2 = dataclasses.replace(p, la=la, o=pla.danh_gia(la, cay, p.cot, p.khoi, pla.CONG_THUC_PM))
    t = _chay(nguon, alr, pla3=p2)
    assert not t.phan_xu.dat
    ngoai = [x for x in t.phan_xu.ly_do if "ngoài tên" in x]
    assert any("`SGO2#OFR#2025M05`" in x for x in ngoai), ngoai[:5]
    assert all("SGO2#" in x for x in ngoai if x.startswith("ô lệch")), ngoai[:5]


def test_AC4_dap_an_khong_vao_engine(nguon, alr):
    """Xoá mọi giá trị ATL ⇒ lưới engine y nguyên *(đáp án chỉ ĐỌC ở bước so)*."""
    p, atl, drv, cay = nguon
    a2 = copy.deepcopy(atl)
    for r in a2["dong"]:
        for c in r:
            if c[:1] == "y":
                r[c] = None
    from fls.bao_cao import phan_bo_khoa as pbk
    k1 = pbk.phan_bo_khoa(p, alr, cay, pla.CONG_THUC_PM, khoi_nguon="GROUP", khoi_cdt=c5a.KHOI_CDT6,
                          khoi_du="SHQ2", driver=c5a.luoi_driver_tu_anh(drv))
    t = _chay(nguon, alr, atl=a2)
    assert not t.phan_xu.dat and k1.o == p.o


# ── AC-5 · cờ từ kho ─────────────────────────────────────────────────────────────────────────────

def test_AC5_bat_co_tren_du_lieu_that__cong_bao_ten(nguon, alr):
    """Cờ bật *(⛔ được ở kho — chỉ dựng trong bài)* ⇒ lưới đổi ⇒ cổng ĐỎ có tên *(D2: parity ở cờ TẮT)*."""
    bat = luat_pb.BangALR(nguon="tong-hop", luat=tuple(dataclasses.replace(x, bat=True) for x in alr.luat))
    t = _chay(nguon, alr, alr_khac=bat)
    assert not t.phan_xu.dat and any("DRIVER_THIEU" in x or "ngoài tên" in x or "dem_phan_bo" in x
                                     for x in t.phan_xu.ly_do)


def test_AC5_chay_tu_kho__thieu_luat_DO_roi_nap_DAT():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bai-h12", ngay_dau="2024-10-21", luat="A",
                       nguon="bai-test-h12:ISP-3.1.2-Step42 (IX.PER kho = 21/10, C6)")
        co_alr = c.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang = 'IX.ALR'").fetchone()[0]
        if co_alr == 0:
            t = c5a.chay_wp_c5a(dsn=dsn_test())
            assert not t.phan_xu.dat and any("IX.ALR" in x for x in t.phan_xu.ly_do)
        chc.nap_ix_alr(c, str(c5a.ANH_MM), tu_ky=c5a.TU_KY_ALR, actor="bai-h12")
    t = c5a.chay_wp_c5a(dsn=dsn_test())
    assert t.phan_xu.dat, t.phan_xu.ly_do[:3]
    assert t.hd2_cong["tong_o"] == MONG_TONG_O


def test_AC5_kho_hong__DO():
    t = c5a.chay_wp_c5a(dsn="postgresql://fls:fls@localhost:1/khong_co")
    assert not t.phan_xu.dat and t.hd2_cong["dat"] is False and len(t.phan_xu.ly_do) == 2


# ── hợp đồng CG2 trên tệp thật ───────────────────────────────────────────────────────────────────

def test_hd2_cong_json_khoi_WP_C5a_khop_lan_do(tq):
    d = json.loads((GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json").read_text(encoding="utf-8"))
    b = d["WP-C5a"]
    assert b["goi"] == "WP-C5a" and b["dat"] is True
    for k in ("tong_o", "khop", "lech_co_chu_dich", "mong_lech_co_chu_dich", "o_co_so", "khop_co_so", "o_0_0"):
        assert b[k] == tq.hd2_cong[k], k
