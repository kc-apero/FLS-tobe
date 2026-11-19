"""H11 — `tools/do_hd2.py --goi WP-C4c`: AL.PLT **OMC · SC · PS** ↔ MID3 từng ô theo DÒNG
*(ISP 3.1.2 · Step 35 · `WO-233`; đầu vào DT9 `BG-221` + DT9b `BG-242`)*.

Chuỗi: IX.VEN ĐỌC TỪ KHO test `so=<sổ>` + ảnh MID1 *(PD 508 — THƯỢNG NGUỒN)* → CÙNG engine H10
`chia_theo_cach_tinh` *(tham số `LUAT_SO`: mượn RATE · nhánh PM tổng tháng — ⛔ chép)* → `ks_al` → so hàng MID3
có khoá ↔ nhóm (vendor, tháng, No) × 14 cột. ⛔ MID2/MID3 làm đầu vào.

  · **AC-1** mẫu số khai TRƯỚC mỗi sổ *(`MONG_C4C`, nhãn Đ4)* + Đ5 hai chiều.
  · **AC-2** lệch tách 3 lớp CÓ TÊN: `lech_fls` *(mong 0)* · `lech_nguon` *(`lac`: SC ảnh 69 hàng khoá ·
    OMC 8 hàng `LAC_OMC`)* · `lech_nghi_loi` *(cờ `nguon_nghi_loi` OMC)*.
  · **AC-3** khối `WP-C4c` theo hợp đồng CG2: `khop` = ô khớp THẬT, lệch có tên NGOÀI `tong_o`.
  · **AC-4** ⛔ vòng tròn: đột biến 1 ô MID1 ⇒ ĐÚNG các ô MID3 của hàng ấy ĐỎ.
  · **AC-5** grep mã vendor ở `fls/bao_cao` = 0.
"""
from __future__ import annotations

import copy
import dataclasses
import json
import pathlib
import re
import sys
from decimal import Decimal

import psycopg
import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.cau_hinh import vendor as cv  # noqa: E402
from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2  # noqa: E402

pytestmark = pytest.mark.pg

# ══ MONG — khai TRƯỚC (Đ5) · nhãn Đ4 ═════════════════════════════════════════════════════════════
#   (ô so · ô ≠ 0 · lệch FLS · lệch nguồn · lệch nghi lỗi) mỗi sổ
MONG_SO = {"OMC": (8547, 363, 0, 52, 0), "SC": (6230, 1216, 0, 251, 0), "PS": (5117, 0, 0, 0, 0)}
MONG_KHOI = (19591, 19591, 19894, 303)        # khop · tong_o · ô so · lệch có tên (= 52 + 251)


@pytest.fixture(scope="module")
def ven():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_ven(c, str(GOC / "tests/fixture/cau_hinh/ix_ven.json"),
                       duong_cdt1=str(GOC / "tests/fixture/cau_hinh/cdt_correct.json"),
                       actor="bo-test-h11-c4c")
        return {so: chc.doc_ven(c, so=so) for so in ("GI", *do_hd2.SO_C4C)}


@pytest.fixture(scope="module")
def anh():
    return {so: tuple(do_hd2.nap_anh(p) for p in do_hd2.anh_c4c(so)) for so in do_hd2.SO_C4C}


def _chay(ven, anh, mong=None):
    return do_hd2.so_sanh_c4c(anh, ven, mong or do_hd2.MONG_C4C)


def _sua(anh, so, i, f):
    """Bản sao ảnh với ảnh thứ `i` (0 = MID1 · 1 = MID3) của sổ `so` đã qua `f`."""
    a = dict(anh)
    x = list(a[so])
    x[i] = copy.deepcopy(x[i])
    f(x[i])
    a[so] = tuple(x)
    return a


def _hang(mid3, dk):
    return next(h for h in mid3["dong"] if h.get("vendor") is not None and dk(h))


def test_H11_B1_WP_C4c_anh_that_DAT_mau_so_co_nhan(ven, anh):
    tq = _chay(ven, anh)
    h = tq.hd2_cong
    assert tq.phan_xu.dat, tq.phan_xu.ly_do
    do = {so: (k["o_so"], k["o_khac_0"], k["lech_fls"], k["lech_nguon"], k["lech_nghi_loi"])
          for so, k in h["so"].items()}
    assert do == MONG_SO
    assert (h["khop"], h["tong_o"], h["o_so"], h["lech_co_ten"]) == MONG_KHOI
    assert {so: k["vm"] for so, k in h["so"].items()} == {"OMC": 210, "SC": 87, "PS": 477}
    assert {so: (k["dong_so"], k["dong_ngoai_anh"]) for so, k in h["so"].items()} == \
        {"OMC": (890, 0), "SC": (741, 0), "PS": (585, 630)}
    assert {so: k["ks_al_vm"] for so, k in h["so"].items()} == {"OMC": 210, "SC": 87, "PS": 477}


def test_chua_co_dap_an_CO_TEN_khong_phai_dat(ven, anh):
    h = _chay(ven, anh).hd2_cong
    ky = tuple(f"2026{m:02d}" for m in range(3, 10))
    assert h["so"]["OMC"]["chua_co_dap_an"] == ky
    assert h["so"]["SC"]["chua_co_dap_an"] == h["so"]["PS"]["chua_co_dap_an"] == ("202503",) + ky
    assert {so: len(k["thang"]) for so, k in h["so"].items()} == {"OMC": 10, "SC": 9, "PS": 9}


@pytest.mark.parametrize("so,ten,lech", [(s, t, d) for s in ("OMC", "SC", "PS")
                                         for t in ("vm", "dong", "o_so", "o_khong_so", "o_khac_0",
                                                   "o_trong_dap_an", "lech_nguon", "lech_fls",
                                                   "lech_nghi_loi", "dong_ngoai_anh")
                                         for d in (-1, 1)])
def test_D5_mong_KHAC_thi_DO_ca_hai_chieu(ven, anh, so, ten, lech):
    m = dict(do_hd2.MONG_C4C)
    m[so] = dataclasses.replace(m[so], **{ten: getattr(m[so], ten) + lech})
    tq = _chay(ven, anh, m)
    assert not tq.phan_xu.dat and any(x.startswith(f"{so} · {ten}: đo ") for x in tq.phan_xu.ly_do)


# ══ AC-2 · ba lớp lệch có tên ════════════════════════════════════════════════════════════════════
def test_lop_FLS_SC_doi_mot_o_ngoai_lac_thi_DO(ven, anh):
    lac = {x.split("@")[1] for x in anh["SC"][1]["lac"]}

    def f(m3):
        h = _hang(m3, lambda h: h["dong_sheet"] not in lac and h["cvl_pe"] not in (None, "0"))
        h["cvl_pe"] = str(Decimal(h["cvl_pe"]) + 1)
    tq = _chay(ven, _sua(anh, "SC", 1, f))
    assert not tq.phan_xu.dat
    assert tq.hd2_cong["so"]["SC"]["lech_fls"] == 1 and "SC · lech_fls: đo 1 ≠ mong 0" in tq.phan_xu.ly_do
    assert tq.hd2_cong["khop"] == tq.hd2_cong["tong_o"] - 1          # khop = ô khớp THẬT


def test_lop_NGHI_LOI_OMC_doi_mot_o_ngoai_lac_thi_DO_ten_nghi_loi(ven, anh):
    def f(m3):
        h = _hang(m3, lambda h: h["dong_sheet"] not in do_hd2.LAC_OMC and h["cor_pe"] not in (None, "0"))
        h["cor_pe"] = str(Decimal(h["cor_pe"]) * 2)
    tq = _chay(ven, _sua(anh, "OMC", 1, f))
    k = tq.hd2_cong["so"]["OMC"]
    assert not tq.phan_xu.dat and (k["lech_nghi_loi"], k["lech_fls"]) == (1, 0)


def test_lop_NGHI_LOI_mat_co_thi_lech_OMC_thanh_FLS(ven, anh):
    def f(m3):
        m3["phu"].pop("nguon_nghi_loi")
        h = _hang(m3, lambda h: h["dong_sheet"] not in do_hd2.LAC_OMC and h["cor_pe"] not in (None, "0"))
        h["cor_pe"] = str(Decimal(h["cor_pe"]) * 2)
    k = _chay(ven, _sua(anh, "OMC", 1, f)).hd2_cong["so"]["OMC"]
    assert (k["lech_nghi_loi"], k["lech_fls"], k["co_nguon_nghi_loi"]) == (0, 1, False)


def test_lop_NGUON_bo_mot_ten_lac_SC_thi_lech_ay_thanh_FLS_DO(ven, anh):
    def f(m3):
        khoa = {h["dong_sheet"] for h in m3["dong"] if h.get("vendor") is not None}
        m3["lac"] = [x for x in m3["lac"] if x.split("@")[1] not in khoa][:0] + \
            [x for x in m3["lac"] if x.split("@")[1] in khoa][1:]
    tq = _chay(ven, _sua(anh, "SC", 1, f))
    k = tq.hd2_cong["so"]["SC"]
    assert not tq.phan_xu.dat and k["lech_fls"] > 0 and k["hang_lech_nguon"] == 68


def test_lop_NGUON_them_ten_lac_khong_lech_thi_DO(ven, anh):
    def f(m3):
        h = _hang(m3, lambda h: f"dong_sheet@{h['dong_sheet']}" not in m3["lac"])
        m3["lac"] = [*m3["lac"], f"dong_sheet@{h['dong_sheet']}"]
    tq = _chay(ven, _sua(anh, "SC", 1, f))
    assert not tq.phan_xu.dat and any(x.startswith("hàng `lac` có khoá ≠ hàng lệch nguồn") for x in tq.phan_xu.ly_do)


def test_lop_NGUON_OMC_LAC_dung_8_hang_7_VD61_1_VD654(ven, anh):
    m3 = anh["OMC"][1]
    ten = sorted(do_hd2._chu(h["vendor"]) for h in m3["dong"] if h["dong_sheet"] in do_hd2.LAC_OMC)
    assert ten == ["VD61"] * 7 + ["VD654"]                      # BG-242 §4 — ⛔ "8 VD61" (Đ1)


# ══ AC-4 · ⛔ vòng tròn ══════════════════════════════════════════════════════════════════════════
def test_AC4_dot_bien_MOT_o_MID1_thi_DUNG_hang_MID3_ay_DO(ven, anh):
    m1, m3 = anh["OMC"]
    vm_lac = {(do_hd2._chu(h["vendor"]), h["thang"]) for h in m3["dong"] if h["dong_sheet"] in do_hd2.LAC_OMC}
    r0 = next(r for r in m1["dong"] if Decimal(r["pe"]) != 0
              and (do_hd2._chu(r["vendor"]), r["thang"]) not in vm_lac and r["cdt1"]["chu"].startswith("CVL")
              and r["no"] == "1")
    v, t = do_hd2._chu(r0["vendor"]), r0["thang"]

    def f(m):
        r = next(x for x in m["dong"] if x["dong_sheet"] == r0["dong_sheet"])
        r["pe"] = str(Decimal(r["pe"]) * 3)
    tq = _chay(ven, _sua(anh, "OMC", 0, f))
    moi = {(x["dong_sheet"], x["cot"]) for x in tq.lech if x["lop"] != "lech_nguon"}
    assert not tq.phan_xu.dat and moi
    assert {(x["vendor"], x["thang"]) for x in tq.lech if x["lop"] != "lech_nguon"} == {(v, t)}
    assert {c for _, c in moi} <= {"pe"} | {f"{c}_pe" for c in do_hd2.MID3_CDT}   # ⛔ PM nào


def test_AC4_MID3_khong_phai_dau_vao_doi_O_MID3_chi_lam_lech_o_O(ven, anh):
    def f(m3):
        h = _hang(m3, lambda h: h["dong_sheet"] not in do_hd2.LAC_OMC and h["pe"] not in (None, "0"))
        h["pe"] = str(Decimal(h["pe"]) + 7)
    tq = _chay(ven, _sua(anh, "OMC", 1, f))
    assert [x["cot"] for x in tq.lech if x["lop"] != "lech_nguon"] == ["pe"]   # engine ⛔ đọc O MID3


# ══ tham số theo sổ (một nguồn sự thật) ══════════════════════════════════════════════════════════
def test_LUAT_SO_khai_dung_FORMULA_BG242():
    assert cv.LUAT_SO == {"GI": {"muon_rate": True, "pm_tong_thang": True},
                          "OMC": {"muon_rate": False, "pm_tong_thang": True},
                          "SC": {"muon_rate": True, "pm_tong_thang": False},
                          "PS": {"muon_rate": True, "pm_tong_thang": False}}
    assert all(m is None for _, m in cv.cach_tinh_cua_so("OMC").values())
    assert cv.cach_tinh_cua_so("GI") == cv.CACH_TINH
    with pytest.raises(cv.LoiVen):
        cv.cach_tinh_cua_so("XX")


def test_PHA_NGUON_OMC_bat_muon_RATE_thi_cong_DO(ven, anh, monkeypatch):
    monkeypatch.setitem(cv.LUAT_SO, "OMC", {"muon_rate": True, "pm_tong_thang": True})
    tq = _chay(ven, anh)
    assert not tq.phan_xu.dat


def test_engine_chia_dong_GOP_lai_dung_chia_vendor_thang(ven, anh):
    """`chia_dong` *(H11)* và `chia` *(H10)* là CÙNG một phép — gộp dòng ⇒ đúng (vendor, tháng)."""
    from fls.bao_cao import phan_bo as pb
    cdt = tuple(c for c in ven["GI"].cdt1 if c.split(" |")[0].lower() in do_hd2.MID3_CDT)
    cfa1, mid1 = do_hd2.nap_anh(do_hd2.ANH_CFA1_GI), do_hd2.nap_anh(do_hd2.ANH_MID1)
    dong = [pb.DongCFA1(do_hd2._chu(r["vendor"]), r["thang"], r["no"], Decimal(r["pe"]),
                        None if r.get("pm_ghi_chu") is not None or r.get("pm") is None else Decimal(r["pm"]))
            for r in cfa1["dong"]]
    pe: dict = {}
    for r in mid1["dong"]:
        c = do_hd2._chu(r["cdt1"])
        if c in cdt and r.get("pe") is not None:
            k = (do_hd2._chu(r["vendor"]), r["thang"])
            pe.setdefault(k, {}).setdefault(c, Decimal(0))
            pe[k][c] += Decimal(r["pe"])
    kq = pb.chia_theo_cach_tinh(dong, pe, ven["GI"], cdt1=cdt)
    gop: dict = {}
    for r, x in kq.chia_dong:
        for c, (a, _) in x.items():
            gop[(r.vendor, r.thang, c)] = gop.get((r.vendor, r.thang, c), Decimal(0)) + a
    assert len(kq.chia_dong) == len(dong) == 408
    assert all(abs(gop[(v, t, c)] - d[c][0]) <= Decimal("1e-12") for (v, t), d in kq.chia.items() for c in cdt)


# ══ AC-3 · hợp đồng CG2 ══════════════════════════════════════════════════════════════════════════
def test_khoi_WP_C4c_theo_hop_dong_CG2(ven, anh):
    h = _chay(ven, anh).hd2_cong
    assert h["goi"] == "WP-C4c" and h["dat"] is True
    assert type(h["tong_o"]) is int and type(h["khop"]) is int and h["khop"] == h["tong_o"] > 0
    assert h["tong_o"] == h["o_so"] - h["lech_co_ten"]                # lệch có tên NGOÀI mẫu số, ⛔ trong khop
    assert "lech_co_chu_dich" not in h                                # nền ⛔ có ITE — xem BG-235


def test_tep_that_khoi_WP_C4c_khop_lan_chay(ven, anh):
    d = json.loads((GOC / "docs/ITL/_tools/hd2_cong.json").read_text(encoding="utf-8"))["WP-C4c"]
    h = _chay(ven, anh).hd2_cong
    assert (d["khop"], d["tong_o"], d["o_so"], d["lech_co_ten"], d["dat"]) == \
        (h["khop"], h["tong_o"], h["o_so"], h["lech_co_ten"], True) == (*MONG_KHOI[:2], *MONG_KHOI[2:], True)


def test_kho_CHUA_khai_IX_VEN_thi_DO_co_ten():
    tq = do_hd2.chay_wp_c4c("postgresql://fls:fls@localhost:1/khong_co")
    assert not tq.phan_xu.dat and tq.phan_xu.ly_do[0].startswith("IX.VEN ⛔ đọc được từ kho")


# ══ AC-5 · ⛔ tên vendor trong engine ═════════════════════════════════════════════════════════════
def test_AC5_grep_ma_vendor_o_fls_bao_cao_bang_0():
    tep = sorted((GOC / "fls" / "bao_cao").glob("*.py"))
    assert tep                                                         # Đ3: tập ⛔ rỗng
    trung = [(p.name, m) for p in tep for m in re.findall(r"\bVD\d+\b", p.read_text(encoding="utf-8"))]
    assert trung == [], trung
