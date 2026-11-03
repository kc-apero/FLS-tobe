"""CONG PARITY THAT — doi chieu luat khoi voi 584 dong that cua thang 3/2026.

Day khong phai unit test tren du lieu bia. Fixture la anh chup DONG BANG tu
`ITL I Input Transaction Ledger File 2_2 (ADJUSTED)` > `ITL Ledge`, dong 10+.

⭐ Chinh cong nay bat duoc lo: ban dau `tinh_final` nhan `Manual input` lam doi
so thu hai => 6/7 khoi khop nhung khoi 7 lech **521/584**. Cong thuc that la
`Final = f(Classifying, MID)`. Doi lai thi 4.088/4.088 o khop 100%.
"""

import json
import pathlib

import pytest

from fls.ledger.final_rule import (
    BAY_KHOI,
    CO_INPUT_HERE,
    MAC_DINH_THEO_KHOI,
    dung_khoi,
    tinh_final,
)

FIX = pathlib.Path(__file__).resolve().parents[1] / "fixture" / "itl_ledge_2026_03.json"
TEN = [a for a, _ in BAY_KHOI]


def _chuan(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def _la_so(s: str):
    try:
        return float(s)
    except ValueError:
        return None


def khop_o(tinh, cua_so) -> tuple[bool, bool]:
    """So MOT o. Tra (khop, phai_chuan_hoa_so).

    ⚠ Chuan hoa CO KIEM SOAT: chi coi la khop khi ca hai ben doc duoc thanh
    CUNG MOT SO. Khong the che mot lech that — `202603` vs `202604` van lech.
    Can thiet vi o `MID` cua khoi 4/5 luu dang so (`202603.0`) con `Final` luu
    dang so nguyen/chu (`202603`) — artefact KIEU, khong phai lech gia tri.
    """
    a, b = _chuan(tinh), _chuan(cua_so)
    if a == b:
        return True, False
    fa, fb = _la_so(a), _la_so(b)
    if fa is not None and fb is not None and fa == fb:
        return True, True
    return False, False


@pytest.fixture(scope="module")
def so():
    d = json.loads(FIX.read_text(encoding="utf-8"))
    assert d["so_dong"] == len(d["dong"])
    return d["dong"]


def test_fixture_dung_584_dong_thang_3_2026(so):
    assert len(so) == 584
    assert all(r["ngay"].startswith("2026-03") for r in so)


def test_PARITY_100_PHAN_TRAM_TUNG_O_tren_bay_khoi(so):
    """★★ Cong ra cua P2: khop tung o, ⛔ CAM dung sai."""
    lech = []
    tong = can_chuan_hoa = 0
    for r in so:
        for k in TEN:
            tong += 1
            tinh = tinh_final(r[f"{k}_classifying"], r[f"{k}_mid"])
            ok, ch = khop_o(tinh, r[f"{k}_final"])
            can_chuan_hoa += ch
            if not ok:
                lech.append((r["dong_sheet"], k, r[f"{k}_classifying"],
                             r[f"{k}_mid"], r[f"{k}_final"], tinh))
    assert tong == 584 * 7 == 4088
    assert not lech, f"{len(lech)}/{tong} o lech, 5 vi du dau: {lech[:5]}"
    # Cong bo so o phai chuan hoa kieu — de khong ai tuong 100% la "sach tuyet doi"
    assert can_chuan_hoa == 396, (
        f"so o phai chuan hoa kieu doi tu 396 -> {can_chuan_hoa}; "
        "kiem lai truoc khi sua con so nay")


def test_dung_khoi_che_do_oracle_cung_khop_100(so):
    """dung_khoi(mid=…) phai cho ket qua y het tinh_final."""
    for r in so:
        for k in TEN:
            kq = dung_khoi(k, r[f"{k}_classifying"], r[f"{k}_manual"],
                           mid=r[f"{k}_mid"])
            assert khop_o(kq.parity, r[f"{k}_final"])[0], (r["dong_sheet"], k)


def test_o_may_tu_bia_thi_thyt_bi_bo_trong(so):
    """Cho noi that: parity khop so, nhung thyt = None."""
    dem = 0
    for r in so:
        for k in TEN:
            kq = dung_khoi(k, r[f"{k}_classifying"], r[f"{k}_manual"],
                           mid=r[f"{k}_mid"])
            if _chuan(r[f"{k}_manual"]) == CO_INPUT_HERE:
                dem += 1
                assert kq.may_tu_bia is True, (r["dong_sheet"], k)
                assert kq.thyt is None
                assert kq.parity is not None, "parity van phai khop so"
    assert dem == 521, f"thang 3/2026 co 521 o con co Input here, dem duoc {dem}"


def test_mac_dinh_moi_khoi_MOT_HANG_RIENG_khong_dung_chung(so):
    """★★ Do tren 9.219 dong: 5 khoi co hang rieng, 2 khoi chua suy duoc."""
    co_hang = {k: v for k, v in MAC_DINH_THEO_KHOI.items() if v is not None}
    assert len(set(co_hang.values())) == len(co_hang), "hai khoi khong duoc trung hang"
    assert MAC_DINH_THEO_KHOI["hd"] == "OGA | GAC - Other"
    assert MAC_DINH_THEO_KHOI["invoice"] == "Nợ hoá đơn"
    assert MAC_DINH_THEO_KHOI["svc_start"] is None
    assert MAC_DINH_THEO_KHOI["svc_end"] is None


def test_khoi_7_dung_dung_mac_dinh_rieng_khong_phai_cua_khoi_1(so):
    """Chinh cho nay lech 521/584 khi con dung mot hang dung chung."""
    hang7 = [r for r in so
             if _chuan(r["invoice_manual"]) == CO_INPUT_HERE]
    assert hang7, "thang 3/2026 phai co dong khoi 7 con co Input here"
    fin = {_chuan(r["invoice_final"]) for r in hang7}
    assert fin == {"Nợ hoá đơn"}, fin
    assert MAC_DINH_THEO_KHOI["hd"] not in fin
