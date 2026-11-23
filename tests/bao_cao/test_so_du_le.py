"""`fls.bao_cao.so_du_le` — khối `CB I Cash Balance by LE` của Daily Report A-CCR *(PD 615)* dựng từ số dư `2. CCR` ·
`2. CCR Cash` theo LE × ngày *(ISP 3.1.2 · Step 46 · H14 · vòng sửa tích hợp sau R2 `KQ-314` · ảnh DT13 `BG-320`)*.

Bài ĐƠN VỊ *(⛔ kho, ⛔ tệp đáp án)*:
  · Đ2 — khuôn của engine ⇔ bản đồ công thức DT13 đo ĐỘC LẬP (`tests/du_lieu/test_dau_vao_dt13.py::CB_MAP`, `FORMULA`
    22/11): HAI nguồn, so từng (hàng 615 → (tab, hàng, dấu, mũ)).
  · phép tính: Σ dấu × số dư ÷ 10^mũ, ô vắng trong hàng có mặt ⇒ 0 *(SUMIFS trên ô rỗng)*; ngày ⛔ có cột ⇒ ⛔ in ô.
  · ảnh vắng ⇒ phần DỪNG `chua_co_dau_vao` *(⛔ ngầm 0)*.
  · đột biến 1 ô số dư ⇒ ĐÚNG ô báo cáo chiếu từ nó đổi.
"""
from __future__ import annotations

import datetime
from decimal import Decimal

import pytest

from fls.bao_cao import so_du_le as sd

NGAY = [datetime.date(2026, 11, d) for d in range(1, 31)]


def _so_du(gia: Decimal = Decimal("1000000")) -> dict:
    """Mọi hàng khuôn nhắc tới, mọi ngày 11/2026 = `gia` *(đơn vị gốc)*."""
    ra: dict = {}
    for nguon in sd.KHUON_CB_615.values():
        for tab, hang, _dau, _mu in nguon:
            ra.setdefault(tab, {})[hang] = {d.isoformat(): gia for d in NGAY}
    return ra


def test_khuon_46_cap_LE_don_vi_va_hang_71_ngoai_khuon_co_ten():
    assert len(sd.KHUON_CB_615) == 46                                     # 47 hàng CB − hàng 71 (Đ4: đếm CẶP (LE, đơn vị))
    assert ("LE04", "mUSD") not in sd.KHUON_CB_615 and ("LE04", "mUSD") in sd.NGOAI_KHUON_CB
    assert set(sd.TAB) == {t for v in sd.KHUON_CB_615.values() for t, *_ in v}
    assert {u for _le, u in sd.KHUON_CB_615} == {"mUSD", "mSGD", "mHKD", "bVND"}
    # đơn vị ⇔ mũ: m = 10^6 · b = 10^9 — TRỪ đúng hai cặp AS-IS chia 10^9 dù nhãn mUSD *(khai có tên)*
    lech = set()
    for (le, u), nguon in sd.KHUON_CB_615.items():
        mus = {mu for *_x, mu in nguon}
        assert len(mus) == 1, (le, u)
        if mus != {9 if u.startswith("b") else 6}:
            lech.add((le, u))
    assert lech == sd.MU_LECH_DON_VI == {("LE17", "mUSD"), ("LE19", "mUSD")}


def test_khuon_engine_khop_ban_do_cong_thuc_DT13_hai_nguon():
    """Đ2: khuôn engine *(khoá (LE, đơn vị))* ⇔ `CB_MAP` DT13 *(khoá hàng sheet 615)* — nối qua nhãn của ảnh 615."""
    import json
    import pathlib
    import sys
    goc = pathlib.Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(goc))
    from tests.du_lieu.test_dau_vao_dt13 import CB_MAP
    from tools.do_hd2_c5c import nhan_cb_615
    a = json.loads((goc / "tests" / "fixture" / "dap_an" / "ccr_daily_report.json").read_text(encoding="utf-8"))
    hang = nhan_cb_615(a)                                                  # hàng sheet → (LE, đơn vị)
    assert len(hang) == 47 and len(set(hang.values())) == 47              # (LE, đơn vị) DUY NHẤT mỗi hàng
    tu_dt13 = {hang[i]: tuple(t) for i, t in CB_MAP.items()}
    assert tu_dt13 == {k: tuple(v) for k, v in sd.KHUON_CB_615.items()}
    assert {i for i, k in hang.items() if k in sd.NGOAI_KHUON_CB} == {71}


def test_tinh_tong_dau_chia_mu_va_o_vang_la_0():
    s = _so_du()
    s["2. CCR"][101] = {d.isoformat(): None for d in NGAY}                # SGO2 USD OCBC-Deposit: ô rỗng ⇒ 0
    o = sd.bang_so_du_le(2026, 11, s)
    assert len(o) == 46 * 30
    assert o[("LE02", "mUSD", "2026-11-01")] == Decimal(2)                 # (1e6 + 0 + 1e6) ÷ 1e6
    assert o[("LE01", "bVND", "2026-11-30")] == Decimal("0.002")           # (1e6 + 1e6) ÷ 1e9
    assert all(isinstance(v, Decimal) for v in o.values())


def test_hang_khuon_vang_khoi_anh_la_0_ngay_vang_khoi_anh_khong_in():
    s = _so_du()
    del s["2. CCR"][111]                                                   # hàng ⛔ có ở ảnh (toàn rỗng) ⇒ SUMIFS = 0
    for h in s["2. CCR"].values():
        h.pop("2026-11-30")
    for h in s["2. CCR Cash"].values():
        h.pop("2026-11-30")
    o = sd.bang_so_du_le(2026, 11, s)
    assert o[("LE04", "mHKD", "2026-11-01")] == 0
    assert not any(c == "2026-11-30" for *_k, c in o)                      # ngày ⛔ có cột ⇒ ⛔ đoán
    assert len(o) == 46 * 29


@pytest.mark.parametrize("tab", ["2. CCR", "2. CCR Cash"])
def test_anh_vang_DUNG_co_ten_khong_ngam_0(tab):
    s = _so_du()
    del s[tab]
    with pytest.raises(sd.LoiSoDu, match="chua_co_dau_vao"):
        sd.bang_so_du_le(2026, 11, s)


def test_dot_bien_mot_o_so_du_doi_DUNG_o_chieu_tu_no():
    s = _so_du()
    o0 = sd.bang_so_du_le(2026, 11, s)
    s["2. CCR"][40]["2026-11-15"] += Decimal(1000)                         # VND hàng 40 ⇒ LE09 bVND ngày 15
    o1 = sd.bang_so_du_le(2026, 11, s)
    doi = [k for k in o0 if o0[k] != o1[k]]
    assert doi == [("LE09", "bVND", "2026-11-15")] and o1[doi[0]] - o0[doi[0]] == Decimal("0.000001")
