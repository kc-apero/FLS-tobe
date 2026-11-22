"""Cổng `WP-C5c` *(ISP 3.1.2 · Step 46 · H14 · `WO-311`)* — RP.PL · RP.CF Daily Report 2 · 3 dựng theo khuôn từ LƯỚI
ENGINE ↔ đáp án 607 · 608 · 609 · 610 từng ô; 605 · 615 DỪNG có tên.

AC-1 `H14-B1`: mẫu số khai TRƯỚC *(Đ4, theo đáp án)* · ô so > 0 mỗi đáp án so được *(Đ3)* · lệch THỪA KẾ lớp bằng truy
      ngược ô nguồn · lệch FLS 0 · `mong` hai chiều *(Đ5)* · ô chỉnh tay liệt kê có tên.
AC-3: đưa bản báo cáo vào `dua_ban_ky` *(kho TEST, schema tạm, ROLLBACK)* — 2 lần cùng đầu vào ⇒ `khong_doi`.
AC-4: ⛔ vòng tròn — đột biến 1 ô LƯỚI ENGINE ⇒ đúng ô báo cáo ĐỎ `lech_FLS`; bỏ lớp thượng nguồn ⇒ ĐỎ.
AC-5: khối `hd2_cong.json` = lần đo *(hợp đồng CG2)*.
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

from fls.bao_cao import bao_cao as bc  # noqa: E402
from fls.cau_hinh import dong_pl  # noqa: E402
from fls.cau_hinh.ky import LichKy  # noqa: E402
from fls.db.kho import dsn_test  # noqa: E402
from fls.repo import cau_hinh_repo as chc  # noqa: E402
from tools import do_hd2_c5a as c5a  # noqa: E402
from tools import do_hd2_c5c as c5c  # noqa: E402

LICH = LichKy(nguon="bai-h14", ngay_dau=datetime.date(2024, 10, 21), luat="A")
#: mẫu số khai TRƯỚC *(Đ4)* — (ô so · khớp · khớp THẬT · ô 0 = 0 · lệch có chủ đích); ô so = ô đáp án là số × cột thuộc
#: trục × phần có đầu vào × engine có ô. 608: luỹ kế FS1 DỪNG ⇒ chỉ phần ngày *(270 ô có số, khớp 270)*.
MONG_O = {"607": (25649, 21770, 4365, 17405, 3879), "608": (8510, 8510, 270, 8240, 0),
          "609": (25851, 21993, 4387, 17606, 3858), "610": (12380, 12345, 2518, 9827, 35)}
#: ô đáp án NGOÀI mẫu số vì phần ⛔ có đầu vào *(có tên)*
MONG_CHUA = {"607": {}, "608": {"luy_ke:FS1": 8421}, "609": {"luy_ke:FS1": 8402}, "610": {"hr": 1537}}
#: đáp án DỪNG cả bản — số ô SỐ ⛔ so *(Đ3: > 0)*
MONG_DUNG = {"605": 13706, "615": 48021}
MONG_CHINH_TAY = {"607": 71, "608": 0, "609": 71, "610": 0}
FILE_HD2 = GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json"


@pytest.fixture(scope="module")
def ne():
    n = c5c.nguon_engine(LICH, c5a.alr_ky_tu_anh(), dict(dong_pl.DINH_NGHIA))
    assert all(n.cong.values()), n.cong                                   # nền thượng nguồn ĐẠT
    return n


@pytest.fixture(scope="module")
def da():
    return c5c.nap_dap_an()


@pytest.fixture(scope="module")
def bao(ne):
    return c5c.dung_bao(ne)


@pytest.fixture(scope="module")
def tq(ne, da, bao):
    return c5c.so_sanh_c5c(ne, da, c5c.mong_c5c_mac_dinh(), bao=bao)


def _sua(**sua) -> c5c.MongC5c:
    m = copy.deepcopy(dict(c5c.mong_c5c_mac_dinh().so))
    m.update(sua)
    return c5c.MongC5c(so=m)


# ── AC-1 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────

def test_AC1_dat_va_mau_so_khai_truoc(tq):
    assert tq.phan_xu.dat, tq.phan_xu.ly_do[:5]
    for ma, (o, khop, that, o00, lech) in MONG_O.items():
        d = tq.theo_dap_an[ma]
        assert (d["dem"]["tong_o"], d["dem"]["khop"], d["dem"]["khop_co_so"], d["dem"]["o_0_0"]) == (o, khop, that, o00)
        assert sum(v["so_o"] for v in d["lop"].values()) == lech and khop + lech == o
        assert o > 0 and d["dem"]["o_co_so"] > 0                           # Đ3: bằng chứng DƯƠNG ở mỗi đáp án
        assert d["lech_FLS"] == []
        assert d["chua_co_dau_vao"] == MONG_CHUA[ma]


def test_AC1_dap_an_dung_co_ten_va_mau_so_khong_rong(tq):
    dg = tq.hd2_cong["dap_an_dung"]
    assert {k: v["o_dap_an_so"] for k, v in dg.items()} == MONG_DUNG
    assert all(v["trang_thai"] == "chua_co_dau_vao" and "ảnh" in v["can"] for v in dg.values())


def test_AC1_lech_thua_ke_tu_lop_thuong_nguon(tq):
    """Mọi lớp là lớp C5a/C3x/C5b hoặc `lech_dap_an_nguon` — ⛔ lớp tự đặt theo khối × năm."""
    biet = {"loi_as_is", "chua_co_dau_vao", "lech_D3", "ite_alias", "as_is_truoc_CA", "as_is_416_GAC_thieu_CXA",
            c5c.LECH_NGUON}
    lop = {p for d in tq.theo_dap_an.values() for l in d["lop"] for p in l.split("+")}
    assert lop and lop <= biet, lop
    assert tq.hd2_cong["lech_ngoai_ten"] == 0


def test_AC1_truy_nguoc_mot_o_lech_D3_la_lop_C5a_cua_o_nguon(ne, bao, da):
    r = c5c.so_mot("607", da["607"], bao["607"], ne)
    x = next(x for x in r["_lech"] if x["lop"] == "lech_D3" and "|SHQ|" not in x["o"])
    _, kh, ma, t = x["o"].split("|")
    (k,) = [k for n, ks in bc.KHOI_LE + bc.KHOI_CDT if n == kh for k in ks]
    assert ne.lop["atl"][(k, ma, t)] == "lech_D3"
    assert ne.luoi["atl"][(k, ma, t)] == Decimal(x["engine"])


def test_AC1_chinh_tay_liet_ke_co_ten_khong_vao_config(tq):
    ct = {m: d["chinh_tay"] for m, d in tq.theo_dap_an.items()}
    assert {m: len(v) for m, v in ct.items()} == MONG_CHINH_TAY
    assert all("|GROUP|" in x for x in ct["607"]) and "luy_ke:FS2|GROUP|OMC|2025M02" in ct["607"]
    assert tq.hd2_cong["lech_co_ten"]["chinh_tay_actor"]["607"] == ct["607"]
    # ⛔ chép vào config: 0 chỗ `AH12`/`chinh_tay` ở tầng cấu hình *(bằng chứng âm — mẫu số: số tệp quét > 0)*
    tep = list((GOC / "fls" / "cau_hinh").glob("*.py")) + list((GOC / "tests" / "fixture" / "cau_hinh").glob("*.json"))
    assert len(tep) > 10
    assert [p.name for p in tep if "AH12" in p.read_text(encoding="utf-8")] == []


@pytest.mark.parametrize("sua", ["tong_o+1", "bo_lop", "them_lop", "dung+1", "check_do+1"])
def test_AC1_mong_hai_chieu(ne, da, bao, sua):
    m = copy.deepcopy(dict(c5c.mong_c5c_mac_dinh().so))
    if sua == "tong_o+1":
        m["dap_an"]["607"]["dem"]["tong_o"] += 1
    elif sua == "bo_lop":
        m["dap_an"]["609"]["lop"].pop("lech_D3")
    elif sua == "them_lop":
        m["dap_an"]["610"]["lop"]["loi_as_is"] = {"so_o": 1, "sha256": "0"}
    elif sua == "dung+1":
        m["dung"]["615"] += 1
    else:
        m["check"]["610"]["so_do"] += 1
    t = c5c.so_sanh_c5c(ne, da, c5c.MongC5c(so=m), bao=bao)
    assert not t.phan_xu.dat


def test_AC1_mong_chua_khai_DO(ne, da, bao):
    t = c5c.so_sanh_c5c(ne, da, c5c.MongC5c(so=None), bao=bao)
    assert not t.phan_xu.dat and any("chưa khai" in x for x in t.phan_xu.ly_do)


def test_AC1_dap_an_rong_DO_D3(ne, da, bao):
    d = dict(da)
    d["610"] = {**da["610"], "dong": []}
    t = c5c.so_sanh_c5c(ne, d, c5c.mong_c5c_mac_dinh(), bao=bao)
    assert not t.phan_xu.dat and any("610: 0 ô được so" in x for x in t.phan_xu.ly_do)


# ── AC-4 · ⛔ vòng tròn ───────────────────────────────────────────────────────────────────────────────────────────────

def _ne_sua(ne, nguon: str, khoa: tuple, delta: Decimal):
    luoi = {**ne.luoi, nguon: dict(ne.luoi[nguon])}
    luoi[nguon][khoa] = luoi[nguon][khoa] + delta
    return dataclasses.replace(ne, luoi=luoi, tom={})


def test_AC4_dot_bien_o_PLA3_daily_dung_o_bao_cao_DO(ne, da):
    s = (datetime.date(2025, 11, 3) - datetime.date(1899, 12, 30)).days
    n2 = _ne_sua(ne, "pla3_daily", ("SGO1", "GI", s), Decimal("0.001"))
    t = c5c.so_sanh_c5c(n2, da, c5c.mong_c5c_mac_dinh())
    assert not t.phan_xu.dat
    assert t.theo_dap_an["607"]["lech_FLS"] == ["ngay|SGO1|GI|2025-11-03"]
    assert t.theo_dap_an["608"]["lech_FLS"] == ["ngay|SGO1|GI|2025-11-03"]
    assert t.theo_dap_an["609"]["lech_FLS"] == [] and t.theo_dap_an["610"]["lech_FLS"] == []


def test_AC4_dot_bien_o_ATL_dung_o_luy_ke_DO(ne, da):
    n2 = _ne_sua(ne, "atl", ("BGO2", "GI", "2025M07"), Decimal("0.01"))
    t = c5c.so_sanh_c5c(n2, da, c5c.mong_c5c_mac_dinh())
    assert t.theo_dap_an["607"]["lech_FLS"] == ["luy_ke:FS2|BGO2|GI|2025M07"]
    assert t.theo_dap_an["609"]["lech_FLS"] == ["luy_ke:FS2|BGO2|GI|2025M07"]
    assert t.theo_dap_an["608"]["lech_FLS"] == []                        # FS1 ⛔ dùng ATL


def test_AC4_dot_bien_o_CFA1_dung_o_610_DO(ne, da):
    n2 = _ne_sua(ne, "cfa1_yhqm", ("GROUP", "GI", "2026Q1"), Decimal("0.5"))
    t = c5c.so_sanh_c5c(n2, da, c5c.mong_c5c_mac_dinh())
    assert t.theo_dap_an["610"]["lech_FLS"] == ["luy_ke|GROUP|GI|2026Q1"]


def test_AC4_bo_lop_thuong_nguon_thi_DO(ne, da, bao):
    k = next(k for k, v in ne.lop["atl"].items() if v == "loi_as_is" and k[0] == "GROUP" and k[2] == "2025M02")
    lop = {**ne.lop, "atl": {kk: v for kk, v in ne.lop["atl"].items() if kk != k}}
    t = c5c.so_sanh_c5c(dataclasses.replace(ne, lop=lop), da, c5c.mong_c5c_mac_dinh(), bao=bao)
    assert not t.phan_xu.dat
    assert f"luy_ke:FS2|GROUP|{k[1]}|2025M02" in t.theo_dap_an["607"]["lech_FLS"]


def test_AC4_engine_khong_doc_dap_an(ne, bao):
    """Báo cáo dựng CHỈ từ lưới engine: xoá mọi giá trị đáp án ⇒ báo cáo y nguyên từng byte."""
    da0 = {m: {**a, "dong": [{k: (None if len(k) <= 2 else v) for k, v in r.items()} for r in a["dong"]]}
           for m, a in c5c.nap_dap_an().items()}
    assert da0["607"]["dong"][0].get("g") is None
    assert c5c.dung_bao(ne) == bao


# ── AC-3 · JSON → `dua_ban_ky` ───────────────────────────────────────────────────────────────────────────────────────

def _schema_tam(c, ten: str) -> None:
    c.execute(f"CREATE SCHEMA {ten}")
    for b in ("fls_cau_hinh_ban", "fls_cau_hinh_dong"):
        c.execute(f"CREATE TABLE {ten}.{b} (LIKE public.{b} INCLUDING ALL)")
    c.execute(f"SET LOCAL search_path TO {ten}")
    assert c.execute("SELECT count(*) FROM fls_cau_hinh_ban").fetchone()[0] == 0          # Đ3: rỗng THẬT


@pytest.mark.pg
def test_AC3_dua_ban_ky_hai_lan_cung_dau_vao_khong_doi(ne, bao):
    b2 = c5c.dung_bao(ne)["607"]                                          # lần dựng THỨ HAI, cùng đầu vào
    assert json.dumps(b2, sort_keys=True) == json.dumps(bao["607"], sort_keys=True)
    with psycopg.connect(dsn_test()) as c:
        _schema_tam(c, "h14_tam")
        v1 = chc.dua_ban_ky(c, bao["607"]["ky"], bao["607"], actor="engine-h14")
        v2 = chc.dua_ban_ky(c, b2["ky"], b2, actor="engine-h14")
        v3 = chc.dua_ban_ky(c, bao["608"]["ky"], bao["608"], actor="engine-h14")    # cùng kỳ, FS khác ⇒ bản MỚI
        nd = chc.doc_noi_dung_ban_ky(c, 202511, 1)
        c.rollback()
    assert (v1.phien_ban, v1.khong_doi, v1.trang_thai) == (1, False, "chua_ky")
    assert (v2.phien_ban, v2.khong_doi, v2.checksum) == (1, True, v1.checksum)
    assert (v3.phien_ban, v3.khong_doi) == (2, False)
    assert nd == bao["607"] and len(nd["o"]) > 0


# ── AC-5 · kho + hd2_cong.json ───────────────────────────────────────────────────────────────────────────────────────

@pytest.mark.pg
def test_AC5_kho_rong_DO_roi_nap_nen_DAT():
    with psycopg.connect(dsn_test()) as c:
        _schema_tam(c, "h14_kho")
        t0 = c5c.chay_wp_c5c(conn=c)
        c5c.nap_nen_kho(c)
        t1 = c5c.chay_wp_c5c(conn=c)
        c.rollback()
    assert not t0.phan_xu.dat and any("IX.PER" in x for x in t0.phan_xu.ly_do), t0.phan_xu.ly_do
    assert t1.phan_xu.dat, t1.phan_xu.ly_do[:3]
    assert (t1.hd2_cong["tong_o"], t1.hd2_cong["khop"]) == (72390, 64618)


def test_AC5_hd2_cong_json_khoi_WP_C5c_khop_lan_do(tq):
    d = json.loads(FILE_HD2.read_text(encoding="utf-8"))["WP-C5c"]
    for k in ("goi", "tong_o", "khop", "khop_co_so", "o_co_so", "o_0_0", "lech_co_chu_dich",
              "mong_lech_co_chu_dich", "lech_ngoai_ten", "dat", "dap_an_dung", "check", "fs_tham_so"):
        assert d[k] == json.loads(json.dumps(tq.hd2_cong[k], ensure_ascii=False)), k
    assert (d["tong_o"], d["khop"], d["lech_co_chu_dich"], d["dat"]) == (72390, 64618, 7772, True)
    assert sum(o for o, *_ in MONG_O.values()) == d["tong_o"]
