"""Cổng `WP-C5c` *(ISP 3.1.2 · Step 46 · H14 · `WO-311`)* — RP.PL · RP.CF Daily Report 2 · 3 dựng theo khuôn từ LƯỚI
ENGINE ↔ đáp án 607 · 608 · 609 · 610 · 615 từng ô; 605 DỪNG có tên ⇒ cổng `null` tới khi chủ ký.

Vòng sửa R1 `KQ-313`: `-01` đáp án ô so = 0 ⇒ cổng `null` CÓ TÊN *(⛔ `true`)* · `-02` 615 so bằng khuôn CF · `-03` AC-4
⛔ đọc đáp án — bài ĐỎ được *(đầu độc ảnh đáp án thượng nguồn thật)* · `-04` chỉnh tay = chuỗi lan `AH12` 68 + 3 trùng ·
`-08` 609 = `FS1_FS2_gop` *(⛔ FS3)*.

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
          "609": (25851, 21993, 4387, 17606, 3858), "610": (12380, 12345, 2518, 9827, 35),
          "615": (13760, 13054, 2875, 10179, 706)}          # H14-R1-02: khuôn CF trên bản CHÍNH THỨC A-CCR (D5)
#: ⭐ vòng sửa tích hợp sau R2 (`KQ-314`): 615 + khối `CB` 1.380 ô *(46 cặp (LE, đơn vị) × 30 ngày; ảnh DT13 số dư)* —
#: trước: (12380, 11674, 2023, 9651, 706).
#: ô đáp án NGOÀI mẫu số vì phần ⛔ có đầu vào *(có tên)*
MONG_CHUA = {"607": {}, "608": {"luy_ke:FS1": 8421}, "609": {"luy_ke:FS1": 8402}, "610": {"hr": 1537},
             "615": {"hr": 3147, "raw_data_management": 1040, "tien_dau_bao_cao": 1071}}   # CB 1.495 hết `chua_co_dau_vao`
#: 615 — đoạn ⛔ khuôn CF *(bản sao DR3 của A-CCR đã so ở 609 · hàng ⛔ khối · giao dịch ngày 0 ô số)*
MONG_NGOAI_KHUON_615 = {"ban_sao_DR3_A_CCR": 18046, "cb_cong_thuc_doi_theo_cot": 32, "daily_transactions": 0,
                        "person_hang_khong_khoi": 2}
#: 615 — lớp lệch: 671 ô engine = đáp án 610 mà bản A-CCR khác *(bản chính thức ≠ CF report)* + 35 `ite_alias` như 610
MONG_LOP_615 = {"ite_alias": 35, "lech_ban_ccr_vs_cf": 671}
#: đáp án DỪNG cả bản — số ô SỐ ⛔ so *(Đ3: > 0)*. 615 hết DỪNG *(H14-R1-02)*.
MONG_DUNG = {"605": 13706}
#: H14-R1-04: chuỗi lan `AH12` = 17 mã × (M02 · Q1 · H1 · Y) = 68; ô 0,5 trùng ngẫu nhiên NGOÀI chuỗi = 3
MONG_CHINH_TAY = {"607": 68, "608": 0, "609": 68, "610": 0, "615": 0}
MONG_TRUNG = ["luy_ke:FS2|GROUP|NPC|2025M01", "luy_ke:FS2|GROUP|NPC|2025M02", "luy_ke:FS2|GROUP|PL5|2025M02"]
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
    assert tq.phan_xu.dat, tq.phan_xu.ly_do[:5]                          # phép so khớp `mong` hai chiều
    assert set(MONG_O) == set(c5c.DAP_AN)
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


# ── H14-R1-01 · đáp án ô so = 0 ⇒ cổng ⛔ `true` ─────────────────────────────────────────────────────────────────────

def test_R1_01_cong_null_co_ten_khi_605_o_so_0_chua_ky(tq):
    """Đ3 · Đ5: phép ⛔ đo được ⛔ xanh. 605 ô so 0/13.706 + chưa chữ ký chủ ⇒ `dat = None`, chuỗi nói 605 + 615."""
    assert c5c.DUNG_KY == {}                                              # chưa có chữ ký chủ "DỪNG có tên"
    assert tq.phan_xu.dat is True and tq.dat is None and tq.hd2_cong["dat"] is None
    (k,) = tq.hd2_cong["khong_do_duoc"]
    assert k.startswith("605: ô so 0/13706 ô số") and "chữ ký" in k
    (p,) = tq.hd2_cong["phu_mot_phan"]
    assert p.startswith("615: ô so 13760/48021 ô số · 34261 ô số chưa so") and "cash_balance_by_le" not in p


def test_R1_01_o_so_lon_hon_0_TUNG_dap_an_va_do_phu_khai(tq):
    """Mỗi đáp án: ô so > 0 *(trừ 605 DỪNG — khai riêng)*; độ phủ = ô so / ô SỐ của ảnh in cạnh nhau (Đ4)."""
    dp = tq.hd2_cong["do_phu"]
    assert set(dp) == set(c5c.DAP_AN) | set(c5c.DUNG) == {"605", "607", "608", "609", "610", "615"}
    assert {m: (v["o_so"], v["o_dap_an_so"]) for m, v in dp.items()} == {
        "607": (25649, 27290), "608": (8510, 17962), "609": (25851, 35542), "610": (12380, 26272),
        "615": (13760, 48021), "605": (0, 13706)}
    assert [m for m, v in dp.items() if v["o_so"] == 0] == ["605"]


def test_R1_01_chu_ky_DUNG_co_ten_la_ngoai_le_duy_nhat(ne, da, bao, monkeypatch):
    monkeypatch.setitem(c5c.DUNG_KY, "605", "chủ ký 'DỪNG có tên' (bài — giả lập)")
    t = c5c.so_sanh_c5c(ne, da, c5c.mong_c5c_mac_dinh(), bao=bao)
    assert t.dat is True and t.hd2_cong["khong_do_duoc"] == []


def test_R1_01_bo_khuon_615_thi_DO(ne, da, monkeypatch):
    """Chứng minh ĐỎ: xoá ánh xạ khuôn 615 ⇒ 615 ô so 0 ⇒ cổng ĐỎ có tên *(⛔ `true`)*."""
    monkeypatch.setitem(c5c.DAP_AN, "615", {k: v for k, v in c5c.DAP_AN["615"].items() if k != "phan_khuon"})
    t = c5c.so_sanh_c5c(ne, da, c5c.mong_c5c_mac_dinh())
    assert t.dat is False and any(x.startswith("615: 0 ô được so") for x in t.phan_xu.ly_do)


def test_R1_09_dap_an_DUNG_rong_DO(ne, da, bao):
    """M10 của R1: đáp án DỪNG mà ảnh 0 ô số ⇒ câu 'dừng' ⛔ nghĩa ⇒ ĐỎ."""
    d = {**da, "605": {**da["605"], "dong": []}}
    t = c5c.so_sanh_c5c(ne, d, c5c.mong_c5c_mac_dinh(), bao=bao)
    assert t.dat is False and any("605: đáp án DỪNG mà 0 ô số" in x for x in t.phan_xu.ly_do)


# ── H14-R1-02 · 615 (A-CCR, bản CHÍNH THỨC D5) qua khuôn CF ──────────────────────────────────────────────────────────

def test_R1_02_615_khuon_CF_ke_toan_du_48021_o_so(tq):
    d = tq.theo_dap_an["615"]
    assert {k: v["so_o"] for k, v in d["lop"].items()} == MONG_LOP_615
    assert d["ngoai_khuon"] == MONG_NGOAI_KHUON_615
    # Đ4: mọi ô SỐ của ảnh 615 nằm ĐÚNG MỘT rổ có tên — tổng = 48.021 *(⛔ rổ "khác")*
    ro = (d["dem"]["tong_o"] + sum(d["engine_vang"].values())
          + sum(v for k, v in d["ngoai_truc"].items() if k != "hang_khong_nhan")      # `hang_khong_nhan` đếm HÀNG, ⛔ ô
          + sum(d["chua_co_dau_vao"].values()) + sum(d["ngoai_khuon"].values()))
    assert ro == 48021 == tq.hd2_cong["do_phu"]["615"]["o_dap_an_so"]


def test_R1_02_615_lop_ban_ccr_vs_cf_la_engine_bang_610_hai_nguon(ne, da, bao):
    """Đ2: lớp `lech_ban_ccr_vs_cf` ⇔ engine = đáp án 610 cùng khoá VÀ 615 ≠ 610 — đo lại từ HAI ảnh, ⛔ qua nhãn."""
    a610, _ = c5c.o_dap_an("610", da["610"])
    r = c5c.so_mot("615", da["615"], bao["615"], ne, doi_chieu=a610)
    x = [x for x in r["_lech"] if x["lop"] == c5c.LECH_CCR_CF]
    assert len(x) == 671
    for y in x:
        e, a, b = Decimal(y["engine"]), Decimal(y["dap_an"]), a610[y["o"]]
        assert abs(e - b) <= c5c.ATOL < abs(a - b)
    # bỏ đối chiếu ⇒ 671 ô rơi về lớp chung `lech_dap_an_nguon` *(nhãn nói ít hơn — lý do có `doi_chieu`)*
    r0 = c5c.so_mot("615", da["615"], bao["615"], ne)
    assert {k: v["so_o"] for k, v in r0["lop"].items()} == {"ite_alias": 35, c5c.LECH_NGUON: 671}


def test_R1_08_anh_609_615_dinh_nghia_FS3_khac_hop_FS1_FS2():
    """Đ1: định nghĩa FS3 nằm Ở ẢNH đáp án *(⛔ chỉ tài liệu)* ⇒ 609 ⛔ mang nhãn FS3."""
    for ten in ("daily_report_3_gop", "ccr_daily_report"):
        assert (c5c.DA / f"{ten}.json").read_text(encoding="utf-8").count("FS3 là mức độ tin cậy giao dịch đủ") == 1
    assert c5c.DAP_AN["609"]["fs"] == "FS1_FS2_gop"
    assert all(cfg["fs"] != "FS3" for cfg in c5c.DAP_AN.values())


def test_AC1_lech_thua_ke_tu_lop_thuong_nguon(tq):
    """Mọi lớp là lớp C5a/C3x/C5b hoặc `lech_dap_an_nguon` — ⛔ lớp tự đặt theo khối × năm."""
    biet = {"loi_as_is", "chua_co_dau_vao", "lech_D3", "ite_alias", "as_is_truoc_CA", "as_is_416_GAC_thieu_CXA",
            c5c.LECH_NGUON, c5c.LECH_CCR_CF}
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
    # H14-R1-04: 68 = 17 mã × 4 kỳ chuỗi lan; 3 ô 0,5 ngoài chuỗi tách riêng *(⛔ gọi chỉnh tay)*
    ma = {x.split("|")[2] for x in ct["607"]}
    assert len(ma) == 17 and {x.split("|")[3] for x in ct["607"]} == {"2025M02", "2025Q1", "2025H1", "2025"}
    assert not [x for x in ct["607"] if "|SHQ" in x]
    assert {m: d["chinh_tay_trung_0_5"] for m, d in tq.theo_dap_an.items() if d["chinh_tay_trung_0_5"]} == {
        "607": MONG_TRUNG, "609": MONG_TRUNG}
    # ⛔ chép vào config: 0 chỗ `AH12`/`chinh_tay` ở tầng cấu hình *(bằng chứng âm — mẫu số: số tệp quét > 0)*
    tep = list((GOC / "fls" / "cau_hinh").glob("*.py")) + list((GOC / "tests" / "fixture" / "cau_hinh").glob("*.json"))
    assert len(tep) > 10
    assert [p.name for p in tep if "AH12" in p.read_text(encoding="utf-8")] == []


def test_R1_04_goc_chinh_tay_hai_nguon_anh_605_va_ATL():
    """Đ2: gốc `GOC_CHINH_TAY` ↔ ảnh 605 `phu.o_chinh_tay` *(hàng ATL 12 · cột `y2025_m02`)* ↔ ảnh ATL hàng 12 = `OMC`."""
    (o,) = c5c.nap_anh(c5c.DA / "daily_report_3.json")["phu"]["o_chinh_tay"]["dong"]
    assert (o["dong_sheet_atl"], o["cot_anh_atl"]["chu"], o["tru"]["chu"]) == ("12", "y2025_m02", "0.5")
    (h12,) = [r for r in c5c.nap_anh(c5a.ANH_ATL)["dong"] if r["dong_sheet"] == "12"]
    assert h12["l4"]["chu"].split(" |")[0] == c5c.GOC_CHINH_TAY[1] == "OMC"
    assert c5c.GOC_CHINH_TAY == ("GROUP", "OMC", "2025M02")


def test_R1_04_chuoi_chinh_tay_don_vi():
    """Mã mang 0,5 ĐỦ M02 · Q1 · H1 · Y ⇒ chuỗi; thiếu một kỳ ⇒ trùng; ⛔ ô gốc ⇒ chuỗi rỗng *(⛔ đoán)*."""
    ky = ("2025M02", "2025Q1", "2025H1", "2025")
    uv = [f"luy_ke:FS2|GROUP|{m}|{k}" for m in ("OMC", "PL2") for k in ky] + ["luy_ke:FS2|GROUP|NPC|2025M02",
                                                                              "luy_ke:FS2|SGO1|PL2|2025M02"]
    chuoi, trung = c5c.chuoi_chinh_tay(uv)
    assert len(chuoi) == 8 and trung == ["luy_ke:FS2|GROUP|NPC|2025M02", "luy_ke:FS2|SGO1|PL2|2025M02"]
    chuoi0, trung0 = c5c.chuoi_chinh_tay([x for x in uv if "|OMC|" not in x])
    assert chuoi0 == [] and len(trung0) == 6


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
        m["dung"]["605"] += 1
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


_KHOA_ANH = {"thu_tu", "dong_sheet", "cap", "ngay", "ky", "le", "ma_hd", "khoi", "ma", "phan", "che_do"}


def _dau_doc(anh: dict) -> dict:
    """Mọi ô SỐ ⛔ phải khoá ⇒ hằng "7" *(giữ khuôn hàng/khoá — chỉ GIÁ TRỊ đổi)*."""
    return {**anh, "dong": [{k: ("7" if k not in _KHOA_ANH and c5c._so(v) is not None and not isinstance(v, dict) else v)
                             for k, v in r.items()} for r in anh["dong"]]}


def test_AC4_engine_khong_doc_dap_an(ne, bao, monkeypatch):
    """`H14-R1-03`: ĐẦU ĐỘC mọi ảnh ĐÁP ÁN thượng nguồn mà `nguon_engine` nạp *(`tests/fixture/dap_an/*` ⛔ tên `dau_vao`:
    409 · 410 · 418 + tab PLA · 606 ATL)* rồi dựng lại ⇒ lưới + 4 báo cáo y nguyên từng ô. Bài ĐỎ được: engine đọc một ô
    đáp án ⇒ lưới khác *(đột biến ghi ở `BG-312` vòng sửa R1)*. Đ3: chứng minh đầu độc CÓ TÁC DỤNG *(đáp án thượng nguồn
    đổi · cổng thượng nguồn đỏ)* — ⛔ so hai lần cùng một thứ."""
    from tools import do_hd2 as h
    from tools import do_hd2_c3d as c3d
    goc = h.nap_anh
    doc: list[str] = []

    def nap(path):
        a = goc(path)
        p = Path(path)
        if p.parent.name == "dap_an" and "dau_vao" not in p.name:
            doc.append(p.name)
            return _dau_doc(a)
        return a

    for mod in (h, c3d, c5c):
        monkeypatch.setattr(mod, "nap_anh", nap)
    ne0 = c5c.nguon_engine(LICH, c5a.alr_ky_tu_anh(), dict(dong_pl.DINH_NGHIA))
    assert {"cfa1_daily.json", "cfa1_yhqm.json", "pla3_pm_hr_daily.json", "atl.json"} <= set(doc), sorted(doc)
    assert ne0.dap_an["atl"] != ne.dap_an["atl"] and ne0.dap_an["cfa1_daily"] != ne.dap_an["cfa1_daily"]
    assert not all(ne0.cong.values())                                     # thượng nguồn THẤY đáp án độc
    assert ne0.luoi == ne.luoi and sum(len(v) for v in ne0.luoi.values()) > 100000
    assert c5c.dung_bao(ne0) == bao


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
    assert t1.dat is None                                                 # 605 DỪNG chưa ký (H14-R1-01)
    assert (t1.hd2_cong["tong_o"], t1.hd2_cong["khop"]) == (86150, 77672)


def test_AC5_hd2_cong_json_khoi_WP_C5c_khop_lan_do(tq):
    d = json.loads(FILE_HD2.read_text(encoding="utf-8"))["WP-C5c"]
    for k in ("goi", "tong_o", "khop", "khop_co_so", "o_co_so", "o_0_0", "lech_co_chu_dich",
              "mong_lech_co_chu_dich", "lech_ngoai_ten", "dat", "dat_mong", "dap_an_dung", "check", "fs_tham_so",
              "do_phu", "khong_do_duoc", "phu_mot_phan"):
        assert d[k] == json.loads(json.dumps(tq.hd2_cong[k], ensure_ascii=False)), k
    assert (d["tong_o"], d["khop"], d["lech_co_chu_dich"], d["dat"], d["dat_mong"]) == (86150, 77672, 8478, None, True)
    assert sum(o for o, *_ in MONG_O.values()) == d["tong_o"]


# ── Vòng sửa TÍCH HỢP sau R2 (`KQ-314`) ──────────────────────────────────────────────────────────────────────────────

def test_R2_01_check_NB_0_theo_phan_loai_CHECK_cua_H13(tq):
    """`H14-R2-01`: sau gộp H13-R1 `31a6bb3` *(`pla.check_atl`: `dat_0_0` CHỈ khi kỳ-khối rỗng thật)* — `NB = 0` ở 607 phần
    ngày là 147 `dat_co_so` *(⛔ 147 `dat_0_0` như trước gộp)*. `mong` sinh lại bằng lần đo, ⛔ sửa tay."""
    c = tq.hd2_cong["check"]
    assert c["607"]["theo_phan"]["ngay"]["NB = 0"] == {"dat_co_so": 147, "dat_0_0": 0, "do": 3, "khong_do_duoc": 0}
    assert c["610"]["theo_phan"]["ngay"]["NB = 0"] == {"dat_co_so": 26, "dat_0_0": 56, "do": 8, "khong_do_duoc": 60}
    assert {m: x["so_do"] for m, x in c.items()} == {"607": 230, "608": 4, "609": 231, "610": 198, "615": 198}


#: 615 khối CB *(Đ4 — đếm Ô của khối CB theo rổ)*: 1.495 ô số = 1.380 ô so + 32 hàng 71 ngoài khuôn + 37 cột `F`
#: *(31/10, ngoài trục tháng 11)* + 46 cột `AK` *(⛔ ngày)*.
MONG_CB_615 = {"tong_o": 1380, "o_0_0": 528, "khop_co_so": 852, "khop": 1380, "lech": 0}


def test_R2i_615_khoi_CB_dung_tu_anh_so_du_DT13_khop_tung_o(tq):
    d = tq.theo_dap_an["615"]
    assert d["theo_phan"]["cb"] == MONG_CB_615
    assert MONG_CB_615["tong_o"] > 0 and MONG_CB_615["khop_co_so"] > 0              # Đ3: bằng chứng DƯƠNG
    assert (d["ngoai_truc"]["cb:f"], d["ngoai_truc"]["cb:ak"]) == (37, 46)
    assert (MONG_CB_615["tong_o"] + d["ngoai_khuon"]["cb_cong_thuc_doi_theo_cot"] + d["ngoai_truc"]["cb:f"]
            + d["ngoai_truc"]["cb:ak"]) == 1495                                       # rổ CB cũ = đúng 1.495
    assert "cash_balance_by_le" not in d["chua_co_dau_vao"]
    assert not [x for x in tq.bao["615"]["phan"] if x["id"] == "cb" and x.get("dung")]


def test_R2i_khop_tach_TINH_va_CHEP_khong_gop(tq):
    """Rào DT13: `ccr_daily_report_2` *(DR2 dán giá trị)* CHỈ là đầu vào của 615 — ô 615 "khớp" vì CHÉP ô ảnh ấy ⛔ chứng minh
    tính toán ⇒ đếm `khop_chep` RIÊNG. Engine 615 ⛔ đọc DR2 *(mọi phần `chep = False`)* ⇒ `khop_chep = 0` là KẾT QUẢ
    *(Đ3: mẫu số = ô của phần chép = 0)*; `khop_tinh` = mọi ô khớp có số."""
    for ma, d in tq.theo_dap_an.items():
        assert d["dem"]["khop_tinh"] + d["dem"]["khop_chep"] == d["dem"]["khop_co_so"], ma
    d = tq.theo_dap_an["615"]["dem"]
    assert (d["khop_tinh"], d["khop_chep"]) == (2875, 0)
    assert [p["id"] for p in tq.bao["615"]["phan"] if p.get("chep")] == []
    assert (tq.hd2_cong["khop_tinh"], tq.hd2_cong["khop_chep"]) == (sum(x[2] for x in MONG_O.values()), 0)


def test_R2i_PHA_chep_dem_rieng_khi_phan_danh_dau_chep(ne, da, bao):
    """Chứng minh nhánh `khop_chep` SỐNG: đánh dấu phần CB là chép ⇒ 852 ô khớp có số chuyển sang `khop_chep`."""
    b = copy.deepcopy(dict(bao["615"]))
    for p in b["phan"]:
        if p["id"] == "cb":
            p["chep"] = True
    a610, _ = c5c.o_dap_an("610", da["610"])
    r = c5c.so_mot("615", da["615"], b, ne, doi_chieu=a610)
    assert (r["dem"]["khop_chep"], r["dem"]["khop_tinh"]) == (852, 2875 - 852)


def test_R2i_PHA_doi_mot_o_so_du_thi_DUNG_o_CB_lech_va_cong_DO(ne, da):
    n2 = dataclasses.replace(ne, so_du=copy.deepcopy(ne.so_du))
    n2.so_du["2. CCR"][40]["2026-11-15"] += Decimal(1000)                         # ⇒ LE09 bVND ngày 15
    t = c5c.so_sanh_c5c(n2, da, c5c.mong_c5c_mac_dinh())
    d = t.theo_dap_an["615"]
    assert d["theo_phan"]["cb"]["lech"] == 1 and d["lech_FLS"] == ["cb|LE09|bVND|2026-11-15"]
    assert t.dat is False and not t.phan_xu.dat


def test_R2i_anh_so_du_vang_thi_CB_DUNG_co_ten_va_cong_DO(ne, da):
    t = c5c.so_sanh_c5c(dataclasses.replace(ne, so_du=None), da, c5c.mong_c5c_mac_dinh())
    assert t.theo_dap_an["615"]["chua_co_dau_vao"].get("cb") == 1380 and t.dat is False


def test_R2i_rao_DT13_engine_goi_kiem_va_ket_qua_vao_ly_do(ne, da, bao, monkeypatch):
    """Engine H14 GỌI `kiem_dau_vao_hop_le` *(DT13-R1-01/02)*: nạp ảnh số dư cho 615 qua rào; tự kiểm rào còn chặn
    `sign_off_dau_vao` → 605 và `ccr_daily_report_2` → 610. Mở rào ⇒ cổng ĐỎ có tên."""
    assert c5c.rao.quet_tham_chieu(GOC, "sign_off_dau_vao") == []
    assert c5c.rao.quet_tham_chieu(GOC, "ccr_daily_report_2") == []
    with pytest.raises(c5c.rao.DauVaoSaiChoError):
        c5c.rao.kiem_dau_vao_hop_le("sign_off_dau_vao", "605")
    c5c.rao.kiem_dau_vao_hop_le("ccr_so_du_ccr", "615")                       # ảnh số dư ⛔ khai rào ⇒ qua
    monkeypatch.setitem(c5c.rao.RAO, "sign_off_dau_vao", (frozenset({"608", "605"}), frozenset()))
    t = c5c.so_sanh_c5c(ne, da, c5c.mong_c5c_mac_dinh(), bao=bao)
    assert t.dat is False and any("rào DT13" in x and "605" in x for x in t.phan_xu.ly_do), t.phan_xu.ly_do[:3]
