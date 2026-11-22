"""Cổng `WP-C5b` *(ISP 3.1.2 · Step 44 · H13 · `WO-307`)* — dòng `PL2…PL8` từ IX.PL *(C12)* trên ATL của FLS
*(đầu ra AL.KEY H12, cờ 2025 BẬT ký)* ↔ dòng PL của ATL 606 + hai phép CHECK mỗi kỳ.

AC-1: mẫu số khai TRƯỚC *(Đ4)*: ô so · khớp *(THẬT + 0 = 0)* · lệch theo lớp THỪA KẾ từ lá *(lan nhãn bằng PHÉP
      ĐO: thay lá lệch của lớp ấy bằng giá trị ATL ⇒ dòng PL hồi phục — ⛔ quy tắc khối × năm, `H12-R1-01`)* ·
      lệch FLS = 0; `mong` hai chiều *(Đ5)*.
AC-2: CHECK ① ② mỗi kỳ-khối: `dat_co_so` · `dat_0_0` · `do` · `khong_do_duoc`; kỳ đỏ CÓ TÊN *(kỳ · phép · chênh)*.
AC-3: chứng minh đỏ — đột biến 1 ô lá ATL ⇒ đúng dòng PL + đúng phép CHECK của kỳ ấy ĐỎ; đổi biểu thức IX.PL ⇒ ĐỎ.
AC-4: khối `hd2_cong.json` theo hợp đồng CG2. AC-5: chênh định nghĩa ATL ↔ MM có tên trong báo cáo cổng.
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

from fls.cau_hinh import dong_pl, luat_pb  # noqa: E402
from fls.cau_hinh.ky import LichKy  # noqa: E402
from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2_c5a as c5a  # noqa: E402
from tools import do_hd2_c5b as c5b  # noqa: E402

LICH = LichKy(nguon="bai-h13", ngay_dau=datetime.date(2024, 10, 21), luat="A")
DEN = datetime.date(2026, 2, 27)
#: mẫu số khai TRƯỚC *(Đ4)*: ô so = hàng PL có nhãn của ATL × 57 kỳ, ô là số, IX.PL TÍNH ĐƯỢC *(PL5 chỉ GROUP × 12
#: tháng 2025 — đầu vào `COM_GAG`)*; khớp = THẬT + 0 = 0; lệch = 923 ô, TẤT CẢ thừa kế lớp từ lá; lệch FLS 0
MONG_TONG_O, MONG_KHOP, MONG_KHOP_THAT, MONG_O_0_0, MONG_LECH = 4102, 3179, 884, 2295, 923
#: ô PL5 có số ở ATL mà IX.PL ⛔ tính được *(thiếu `COM_GAG` khối/kỳ ấy)* — ngoài mẫu số, CÓ TÊN
MONG_PL5_KHONG_DO = 252
#: CHECK trên ATL của FLS *(684 kỳ-khối = 12 khối × 57 kỳ mỗi phép)*
P1, P2 = (t for t, _, _ in dong_pl.CHECK)
#: `H13-R1-01` *(KQ-309)*: `dat_0_0` = TẬP BẰNG CHỨNG của phép rỗng — ① *(một vế)* = kỳ-khối có MỌI mã LÁ = 0 *(359)*;
#: ② *(hai vế)* = 8 mã của phép = 0 *(470)*. Trước sửa ① `dat_0_0` 537 trộn 178 kỳ-khối CÓ lá ≠ 0 mà `NB` cân đúng 0.
MONG_CHECK_FLS = {P1: {"dat_co_so": 178, "dat_0_0": 359, "do": 147, "khong_do_duoc": 0},
                  P2: {"dat_co_so": 0, "dat_0_0": 470, "do": 214, "khong_do_duoc": 0}}


@pytest.fixture(scope="module")
def nen():
    gl, hr, _, fx, cay, atl, drv = c5a.nap_nguon()
    p = c5a.tinh_pla3(gl, hr, fx, cay, LICH, DEN)
    tq5a = c5a.so_sanh_c5a(p, atl, drv, c5a.alr_ky_tu_anh(), cay, c5a.mong_c5a_mac_dinh())
    assert tq5a.phan_xu.dat, tq5a.phan_xu.ly_do                       # nền = WP-C5a ĐẠT ở cờ BẬT
    return tq5a, atl, c5b.com_gag_ngoai()


def _chay(nen, mong=None, dn=None, tq5a=None, atl=None):
    t, a, ng = nen
    return c5b.so_sanh_c5b(tq5a or t, atl or a, dn or dict(dong_pl.DINH_NGHIA), ng, mong or c5b.mong_c5b_mac_dinh())


@pytest.fixture(scope="module")
def tq(nen):
    return _chay(nen)


def _sua(**sua) -> c5b.MongC5b:
    m = copy.deepcopy(dict(c5b.mong_c5b_mac_dinh().so))
    m.update(sua)
    return c5b.MongC5b(so=m)


def _o_moi(tq5a, sua: dict):
    o = dict(tq5a.o)
    o.update(sua)
    return dataclasses.replace(tq5a, o=o)


# ── AC-1 ─────────────────────────────────────────────────────────────────────────────────────────

def test_AC1_cong_DAT_mau_so_khai_truoc(tq):
    h = tq.hd2_cong
    assert tq.phan_xu.dat, tq.phan_xu.ly_do
    assert (h["tong_o"], h["khop"], h["khop_co_so"], h["o_0_0"], h["lech_co_chu_dich"], h["lech_ngoai_ten"]) == \
        (MONG_TONG_O, MONG_KHOP, MONG_KHOP_THAT, MONG_O_0_0, MONG_LECH, 0)
    assert h["khop"] + h["lech_co_chu_dich"] == h["tong_o"] == h["mong_tong_o"]
    assert h["o_co_so"] + h["o_0_0"] == h["tong_o"] and h["khop_co_so"] + h["o_0_0"] == h["khop"]
    assert h["lech_co_ten"]["pl5_khong_tinh_duoc"]["so_o"] == MONG_PL5_KHONG_DO
    assert h["o_co_so"] > 0 and h["khop_co_so"] > 0                    # Đ3: bằng chứng DƯƠNG ⛔ rỗng


def test_AC1_moi_o_lech_THUA_KE_lop_tu_la__lop_hop_le(tq):
    lop = tq.hd2_cong["lech_co_ten"]["lop_thua_ke"]
    assert sum(v["so_o"] for v in lop.values()) == MONG_LECH
    goc = set(c5b.LOP_GOC)
    for ten in lop:
        assert ten != "lech_FLS" and set(ten.split("+")) <= goc, ten       # mỗi nhãn = tập lớp LÁ của C5a
    # mỗi ô lệch: hồi phục khi thay ĐÚNG các lá thuộc nhãn ấy bằng ATL *(phép đo, ⛔ quy tắc)*
    assert all(x["lop"] in lop for x in tq.lech)
    assert all(x["la_lech"] for x in tq.lech)                           # ô lệch nào cũng có ≥ 1 lá lệch


def test_AC1_hai_dinh_nghia_PL__IX_PL_trung_KPI_pla_cua_H8(tq):
    """IX.PL *(C12)* ↔ KPI `PL*` của `pla.CONG_THUC_PM` *(H8)* trên CÙNG lưới FLS: 0 ô chênh *(Đ2: so HAI nguồn)*."""
    s = tq.so["hai_dinh_nghia"]
    assert s["o_so"] > 0 and s["chenh"] == 0, s


def test_AC1_nhan_thua_ke_chua_nhan_C5a_cua_chinh_o_PL(tq):
    """Bằng chứng ĐỘC LẬP: C5a gán lớp cho ô KPI `PL*` bằng phản thực CẢ lưới; nhãn thừa kế của H13 PHẢI chứa nó."""
    s = tq.so["nhan_c5a"]
    assert s["khac"] == 0 and s["trung"] > 0, s


def test_AC1_dap_an_khong_vao_engine(nen):
    """Xoá mọi giá trị dòng PL của ATL ⇒ dòng PL engine y nguyên *(⛔ đọc đáp án làm đầu vào)*."""
    t, atl, ng = nen
    a2 = copy.deepcopy(atl)
    for r in a2["dong"]:
        nhan = next((r[k] for k in ("l1", "l2", "l3", "l4") if r.get(k)), None)
        if nhan and str(nhan.get("chu", "")).startswith("PL"):
            for c in a2["cot"]:
                if c[:1] == "y":
                    r[c] = "0"
    x = c5b.so_sanh_c5b(t, a2, dict(dong_pl.DINH_NGHIA), ng, c5b.mong_c5b_mac_dinh())
    y = _chay(nen)
    assert x.pl == y.pl and len(y.pl) > 0


def test_AC1_mong_lech_hai_chieu(nen):
    m = c5b.mong_c5b_mac_dinh().so
    assert not _chay(nen, _sua(tong_o=m["tong_o"] + 1)).phan_xu.dat
    lop = copy.deepcopy(m["lop_thua_ke"])
    k = sorted(lop)[0]
    lop[k]["so_o"] += 1
    assert not _chay(nen, _sua(lop_thua_ke=lop)).phan_xu.dat
    lop2 = copy.deepcopy(m["lop_thua_ke"])
    lop2.pop(k)
    assert not _chay(nen, _sua(lop_thua_ke=lop2)).phan_xu.dat                 # ô lệch có lớp mà ⛔ khai
    lop3 = copy.deepcopy(m["lop_thua_ke"])
    lop3[k]["sha256"] = "0" * 64
    assert not _chay(nen, _sua(lop_thua_ke=lop3)).phan_xu.dat
    assert not _chay(nen, c5b.MongC5b(so=None)).phan_xu.dat                    # `mong` chưa khai ⇒ ĐỎ


def test_AC1_dap_an_rong_DO(nen):
    t, atl, ng = nen
    a2 = dict(atl, dong=[])
    tq = c5b.so_sanh_c5b(t, a2, dict(dong_pl.DINH_NGHIA), ng, c5b.mong_c5b_mac_dinh())
    assert not tq.phan_xu.dat and any("Đ3" in x for x in tq.phan_xu.ly_do)


def test_AC1_nen_C5a_DO_thi_C5b_DO(nen):
    t, _, _ = nen
    t2 = dataclasses.replace(t, phan_xu=dataclasses.replace(t.phan_xu, dat=False, ly_do=("pha",)))
    tq = _chay(nen, tq5a=t2)
    assert not tq.phan_xu.dat and any("WP-C5a" in x for x in tq.phan_xu.ly_do)


# ── AC-2 ─────────────────────────────────────────────────────────────────────────────────────────

def test_AC2_CHECK_moi_ky_khoi_bon_trang_thai(tq):
    c = tq.hd2_cong["check"]
    assert c["fls"] == MONG_CHECK_FLS
    for p in (P1, P2):
        assert sum(c["fls"][p].values()) == 12 * 57                        # Đ4: kỳ-khối
    # Đ3: "đạt" ⛔ trơn — ② 0 kỳ-khối cân CÓ SỐ *(mọi "đạt" ② là 0 = 0 — trùng DT11)*; ① 178 kỳ-khối có lá ≠ 0 mà
    # `NB` cân *(`H13-R1-01`: ⛔ gọi là 0 = 0)*; ① `dat_0_0` ⊆ ② `dat_0_0` *(kỳ-khối rỗng ⇒ 8 mã của ② cũng 0)*
    assert c["fls"][P2]["dat_co_so"] == 0 and c["fls"][P1]["dat_co_so"] > 0
    assert c["fls"][P1]["dat_0_0"] <= c["fls"][P2]["dat_0_0"]


def test_AC2_ky_do_CO_TEN_ky_phep_chenh(tq):
    c = tq.hd2_cong["check"]
    do = c["do_theo_ky"]
    assert sum(len(v) for v in do.values()) == 147 + 214
    assert any(x.startswith(f"{P1} @GROUP:") for x in do["2025M01"]), do["2025M01"]
    assert c["so_ky_do"] == len(do) > 0
    assert all(Decimal(x.rsplit(":", 1)[1]) != 0 for v in do.values() for x in v)


def test_AC2_CHECK_FLS_doi_chieu_dap_an_lech_thua_ke_lop(tq):
    c = tq.hd2_cong["check"]
    assert c["doi_chieu_dap_an"]["lech_FLS"] == 0
    assert c["doi_chieu_dap_an"]["khop"] + sum(c["doi_chieu_dap_an"]["lop_thua_ke"].values()) \
        + c["doi_chieu_dap_an"]["dap_an_khong_do_duoc"] == 2 * 12 * 57


# ── AC-3 · chứng minh đỏ ─────────────────────────────────────────────────────────────────────────

def test_AC3_dot_bien_1_la_GI_DO_dung_dong_PL_cua_ky_ay(nen):
    t, _, _ = nen
    k = ("GROUP", "GI", "2025M05")
    tq = _chay(nen, tq5a=_o_moi(t, {k: t.o[k] + Decimal("1e-3")}))
    assert not tq.phan_xu.dat
    assert sorted(tq.so["ngoai_ten_o"]) == sorted(f"GROUP#{p}#2025M05" for p in dong_pl.DINH_NGHIA)
    assert tq.hd2_cong["check"]["fls"] == MONG_CHECK_FLS                 # GI ⛔ trong CHECK


def test_AC3_dot_bien_1_la_NB_DO_dung_phep_CHECK_1_cua_ky_ay(nen):
    t, _, _ = nen
    k = ("SGO2", "NB", "2025M07")
    tq = _chay(nen, tq5a=_o_moi(t, {k: t.o[k] + Decimal(1)}))
    assert not tq.phan_xu.dat
    assert tq.so["ngoai_ten_o"] == []                                    # NB ⛔ trong dòng PL nào
    assert tq.so["check_ngoai_ten"] == [f"{P1}@SGO2#2025M07"], tq.so["check_ngoai_ten"]


def test_AC3_doi_bieu_thuc_IX_PL_DO(nen):
    dn = dict(dong_pl.DINH_NGHIA, PL2="GI - OMC")
    tq = _chay(nen, dn=dn)
    assert not tq.phan_xu.dat and len(tq.so["ngoai_ten_o"]) > 0


# ── AC-4 · AC-5 ──────────────────────────────────────────────────────────────────────────────────

def test_AC5_chenh_dinh_nghia_ATL_MM_co_ten(tq):
    ch = tq.hd2_cong["chenh_dinh_nghia_mm"]
    assert ch == [{"dong": pl, "ma": ma, "ly_do": ly} for pl, ma, ly in dong_pl.CHENH_VOI_MM] and ch


def test_hd2_cong_json_khoi_WP_C5b_khop_lan_do(tq):
    d = json.loads((GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json").read_text(encoding="utf-8"))
    b = d["WP-C5b"]
    for k in ("tong_o", "khop", "lech_co_chu_dich", "dat", "o_co_so", "khop_co_so", "o_0_0", "lech_ngoai_ten"):
        assert b[k] == tq.hd2_cong[k], k
    assert b["dat"] is True and b["check"]["fls"] == MONG_CHECK_FLS


# ── kho *(IX.PER + IX.ALR ký + IX.PL)* — SCHEMA TẠM RỖNG, giao dịch ROLLBACK *(`H12-R1-05`: ⛔ `if` trên kho chung)* ──

def _schema_tam(c, ten: str) -> None:
    c.execute(f"CREATE SCHEMA {ten}")
    for b in ("fls_cau_hinh_ban", "fls_cau_hinh_dong"):
        c.execute(f"CREATE TABLE {ten}.{b} (LIKE public.{b} INCLUDING ALL)")
    c.execute(f"SET LOCAL search_path TO {ten}")
    assert c.execute("SELECT count(*) FROM fls_cau_hinh_ban").fetchone()[0] == 0          # Đ3: rỗng THẬT


def _nap_nen(c) -> None:
    chc.nap_ix_per(c, actor="bai-h13", ngay_dau="2024-10-21", luat="A",
                   nguon="bai-test-h13:ISP-3.1.2-Step44 (IX.PER kho = 21/10, C6)")
    nen = c5a.alr_tu_anh_mm()
    chc.nap(c, luat_pb.BANG, [(luat_pb.khoa_cua(x.hd, x.tu_ky),
                               {"hd": x.hd, "tu_ky": x.tu_ky, "nhan_mm": x.nhan_mm, "bat": x.bat,
                                "ngoai_le": list(x.ngoai_le_cdt1)}) for x in nen.luat],
            nguon=f"bai-h13:{c5a.ANH_MM.name}", actor="bai-h13")
    chc.ky_bat_ix_alr(c, str(c5a.TEP_KY), actor="KhanhCQ")


@pytest.mark.pg
def test_kho_thieu_IX_PL_DO_roi_nap_IX_PL_DAT():
    with psycopg.connect(dsn_test()) as c:
        _schema_tam(c, "h13_tam")
        _nap_nen(c)
        t0 = c5b.chay_wp_c5b(conn=c)
        chc.nap_ix_pl(c, actor="bai-h13")
        assert chc.doc_pl(c) == dict(dong_pl.DINH_NGHIA)
        t1 = c5b.chay_wp_c5b(conn=c)
        c.rollback()
    assert not t0.phan_xu.dat and any("IX.PL" in x for x in t0.phan_xu.ly_do), t0.phan_xu.ly_do
    assert t1.phan_xu.dat, t1.phan_xu.ly_do[:3]
    assert (t1.hd2_cong["tong_o"], t1.hd2_cong["khop"]) == (MONG_TONG_O, MONG_KHOP)


@pytest.mark.pg
def test_kho_IX_PL_doi_bieu_thuc_DO():
    """IX.PL đọc TỪ KHO *(⛔ hằng)*: nạp phiên bản PL2 = GI − OMC ⇒ cổng ĐỎ có ô ngoài tên."""
    with psycopg.connect(dsn_test()) as c:
        _schema_tam(c, "h13_tam2")
        _nap_nen(c)
        chc.nap_ix_pl(c, actor="bai-h13", dinh_nghia=dict(dong_pl.DINH_NGHIA, PL2="GI - OMC"))
        t = c5b.chay_wp_c5b(conn=c)
        c.rollback()
    assert not t.phan_xu.dat and t.so["ngoai_ten_o"], t.phan_xu.ly_do[:3]


def test_kho_hong_DO():
    t = c5b.chay_wp_c5b(dsn="postgresql://fls:fls@localhost:1/khong_co")
    assert not t.phan_xu.dat and t.hd2_cong["dat"] is False and len(t.phan_xu.ly_do) == 3


def test_H13_R1_03_thua_ke_lay_tap_lop_NHO_NHAT_khong_lay_hop():
    """`H13-R1-03` *(KQ-309, GHI NHẬN — rẻ nên làm)*: dữ liệu thật ⛔ có ca nhãn ⊊ hợp *(923/923 nhãn = hợp)* ⇒ nhánh
    "tập NHỎ NHẤT" chưa từng cắn. Ca tổng hợp: 2 lá lệch thuộc 2 lớp, dòng chỉ phụ thuộc lá thứ nhất *(sai số lá thứ
    hai ⛔ vào dòng)* ⇒ nhãn = MỘT lớp, ⛔ `lech_D3+loi_as_is`."""
    lop_o = {"X#A#2025M01": "loi_as_is", "X#B#2025M01": "lech_D3"}
    o = {("X", "A", "2025M01"): Decimal(1), ("X", "B", "2025M01"): Decimal(5)}
    atl = {("X", "A", "2025M01"): Decimal(2), ("X", "B", "2025M01"): Decimal(9)}
    nhan, la_lech = c5b._thua_ke("X", "2025M01", frozenset({"A", "B"}), lop_o, o, atl, {},
                                 lambda gt: gt["A"], Decimal(2))
    assert sorted(la_lech) == ["A:loi_as_is", "B:lech_D3"]                 # Đ3: CẢ hai lá đều lệch *(tập ⛔ rỗng)*
    assert nhan == "loi_as_is"
