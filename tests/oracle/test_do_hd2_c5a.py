"""Cổng `WP-C5a` *(ISP 3.1.2 · Step 42 · H12 · `WO-291`)* — AL.KEY ↔ ATL 606 *(+ tham chiếu 604)*.

⭐ Vòng sửa R1 *(`KQ-293` · `H12-R1-01`)*: cổng đo ở **cờ BẬT 2025** = phiên bản KÝ `ix_alr_2025_bat.json` *(quyết
của chủ 22/11)*; lớp lệch gán bằng PHÉP ĐO phản thực *(`loi_as_is` · `chua_co_dau_vao` · `lech_D3` · lệch FLS = 0)*,
`mong` TỪNG LỚP hai chiều. Cờ TẮT = bài đồng nhất `H12-B1` *(`tests/bao_cao/test_phan_bo_khoa.py`)*.
⚠ Kho config TÍCH LUỸ *(`C11-R1-01`)* ⇒ bài chạm kho chạy trong GIAO DỊCH rồi ROLLBACK *(⛔ để lại bản ký cho bài
C11 chạy sau)*; bài "thiếu IX.ALR" dùng SCHEMA TẠM RỖNG *(`H12-R1-05`: ⛔ nhánh `if` trên kho chung)*.

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
MONG_TONG_O, MONG_KHOP, MONG_LECH = 45674, 40556, 5118
#: lớp lệch *(Đ4 — đếm ô lệch trong 11.764 ô có số)*: loi_as_is = 224 từng ô + 675 (2024) + 29 (dư SHQ2 mang −0,5 tay)
MONG_LOP = {"o_lech": 224, "as_is_truoc_CA": 675, "as_is_tay_lan_du": 29, "chua_co_dau_vao": 1091, "lech_D3": 3099}


@pytest.fixture(scope="module")
def nguon():
    gl, hr, _, fx, cay, atl, drv = c5a.nap_nguon()
    return c5a.tinh_pla3(gl, hr, fx, cay, LICH, DEN), atl, drv, cay


@pytest.fixture(scope="module")
def alr():
    return c5a.alr_ky_tu_anh()                   # cờ BẬT 2025 = ảnh MM + tệp ký *(cùng phép gộp `ky_bat_ix_alr`)*


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
    assert {k: (len(lt[k]) if k == "o_lech" else lt[k]["so_o"]) for k in MONG_LOP} == MONG_LOP
    assert sum(MONG_LOP.values()) == h["lech_co_chu_dich"] and h["loi_as_is"] == 224 + 675 + 29
    assert (h["khop_co_so_co_tat"], h["khop_co_so"], h["o_co_so"]) == (5932, 6646, 11764)     # cờ tắt → bật
    assert h["la_cdt_2025"]["OFR"] == {"o": 72, "khop": 72, "chua_co_dau_vao": 0}               # OFR: nguồn FLS ⇒ khớp
    for ma in ("GI", "OMC", "PS", "SC"):                                                        # nguồn ⛔ có ảnh
        x = h["la_cdt_2025"][ma]
        assert x["o"] == 72 and x["khop"] + x["chua_co_dau_vao"] == 72 and x["chua_co_dau_vao"] >= 51, (ma, x)
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
    ({"sha": "as_is_truoc_CA"}, "sha256"),
    ({"sha": "as_is_tay_lan_du"}, "sha256"),
    ({"sha": "chua_co_dau_vao"}, "sha256"),
    ({"sha": "lech_D3"}, "sha256"),
    ({"dem_khoi": "chua_co_dau_vao", "d": 1}, "theo_khoi"),           # khai THỪA một ô
    ({"dem_khoi": "lech_D3", "d": -1}, "theo_khoi"),                  # khai THIẾU một ô
    ({"la": ("GI", "khop")}, "la_cdt_2025"),
    ({"la": ("OFR", "chua_co_dau_vao")}, "la_cdt_2025"),
    ({"bo_lop": "lech_D3"}, "lop_do"),
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
        m["lop_do"][sua["sha"]]["sha256"] = "0" * 64
    if "dem_khoi" in sua:
        m["lop_do"][sua["dem_khoi"]]["theo_khoi"]["CVL"] += sua["d"]
    if "la" in sua:
        m["la_cdt_2025"][sua["la"][0]][sua["la"][1]] += 1
    if "bo_lop" in sua:
        m["lop_do"].pop(sua["bo_lop"])
    if "gia_tri" in sua:
        k = next(iter(m["o_lech"]))
        m["o_lech"][k] = [m["o_lech"][k][0], str(Decimal(m["o_lech"][k][1]) + 1)]
    t = _chay(nguon, alr, mong=c5a.MongC5a(so=m))
    assert not t.phan_xu.dat and any(mau in x for x in t.phan_xu.ly_do), t.phan_xu.ly_do[:3]


def test_R1_01_khong_con_lop_quy_tac_2025():
    """`H12-R1-01`: lớp 2025 ⛔ còn gán bằng quy tắc khối × năm — chỉ lớp H8 2024 giữ quy tắc."""
    assert c5a._lop_2024({"o": "CVL#LC#2025M03"}) is None
    assert c5a._lop_2024({"o": "SHQ2#GI#2024Q4"}) == "as_is_truoc_CA"
    assert c5a._lop_2024({"o": "GROUP#LC#2024M03"}) is None
    assert not hasattr(c5a, "_lop"), "⛔ giữ hàm lớp quy tắc cũ"


def test_R1_01_lech_FLS_that__ngoai_ten_DO(nguon, alr):
    """Đột biến engine-đầu-vào ở khối CDT 2025 *(lá By GI ⛔ phải nguồn nền tảng)*: phản thực ⛔ cứu được ⇒ ngoài
    tên ⇒ ĐỎ *(lớp đo ⛔ nuốt lệch FLS — Đ5)*."""
    p, atl, drv, cay = nguon
    la = dict(p.la)
    la[("GROUP", "REC", "2025M05")] += Decimal("1")          # tiền nguồn By NOEM ⇒ 6 lá CDT + dư + lan
    p2 = dataclasses.replace(p, la=la, o=pla.danh_gia(la, cay, p.cot, p.khoi, pla.CONG_THUC_PM))
    t = _chay(nguon, alr, pla3=p2)
    ng = set(t.so["ngoai_ten_o"])
    assert not t.phan_xu.dat and {f"{kh}#REC#2025M05" for kh in c5a.KHOI_CDT6} <= ng, sorted(ng)[:8]


def test_R1_01_phan_thuc_khong_vao_dau_ra_cong(nguon, alr):
    """Phản thực đọc ATL CHỈ để gán nhãn: đổi ATL lá `GI` khối CDT ⇒ lưới engine *(`dem_phan_bo`)* y nguyên."""
    p, atl, drv, cay = nguon
    a2 = copy.deepcopy(atl)
    for kh, ma, r in c5a.hang_atl(a2)[0]:
        if ma == "GI" and kh in c5a.KHOI_CDT6:
            r["y2025_m05"] = "0"
    t = _chay(nguon, alr, atl=a2)
    from fls.bao_cao import phan_bo_khoa as pbk
    k = pbk.phan_bo_khoa(p, alr, cay, pla.CONG_THUC_PM, khoi_nguon="GROUP", khoi_cdt=c5a.KHOI_CDT6,
                         khoi_du="SHQ2", driver=c5a.luoi_driver_tu_anh(drv))
    assert t.so["dem_phan_bo"] == k.dem == {"o": 50616, "o_chia": 648, "luat_bat": 11}


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
    """Xoá mọi giá trị ATL ⇒ lưới engine y nguyên *(đáp án chỉ ĐỌC ở bước so)*. Cờ BẬT ⇒ so với lần chạy engine
    thứ hai *(⛔ còn đồng nhất PLA3 — đó là bài H12-B1)*; engine ⛔ có tham số đáp án."""
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
    import inspect
    k2 = pbk.phan_bo_khoa(p, alr, cay, pla.CONG_THUC_PM, khoi_nguon="GROUP", khoi_cdt=c5a.KHOI_CDT6,
                          khoi_du="SHQ2", driver=c5a.luoi_driver_tu_anh(drv))
    assert not t.phan_xu.dat and k1.o == k2.o and k1.o != p.o
    assert not {"atl", "dap_an"} & set(inspect.signature(pbk.phan_bo_khoa).parameters)


# ── AC-5 · cờ từ kho ─────────────────────────────────────────────────────────────────────────────

def test_AC5_co_TAT__cong_DO_co_ten(nguon):
    """Cổng đo ở cờ BẬT ký: bảng luật cờ TẮT *(chưa ký)* ⇒ ĐỎ CÓ TÊN *(⛔ xanh lặng lẽ ở cờ tắt)*."""
    t = _chay(nguon, c5a.alr_tu_anh_mm())
    assert not t.phan_xu.dat
    assert any("⛔ có luật nào BẬT" in x for x in t.phan_xu.ly_do) and any("dem_phan_bo" in x for x in t.phan_xu.ly_do)


def test_AC5_bat_moi_co_ngoai_ky_ky__cong_bao_ten(nguon, alr):
    """Bật MỌI luật mọi kỳ *(ngoài tệp ký — chỉ dựng trong bài)* ⇒ 2026 ⛔ có driver ⇒ ĐỎ có tên."""
    bat = luat_pb.BangALR(nguon="tong-hop", luat=tuple(dataclasses.replace(x, bat=True) for x in alr.luat))
    t = _chay(nguon, alr, alr_khac=bat)
    assert not t.phan_xu.dat and any("DRIVER_THIEU" in x or "ngoài tên" in x or "dem_phan_bo" in x
                                     for x in t.phan_xu.ly_do)


def _nap_nen(c) -> None:
    """IX.PER + IX.ALR nền *(17 luật `@202501`, ⛔ tích luỹ mốc khác của bài C11 — `nap` trực tiếp)*."""
    chc.nap_ix_per(c, actor="bai-h12", ngay_dau="2024-10-21", luat="A",
                   nguon="bai-test-h12:ISP-3.1.2-Step42 (IX.PER kho = 21/10, C6)")
    nen = c5a.alr_tu_anh_mm()
    chc.nap(c, luat_pb.BANG, [(luat_pb.khoa_cua(x.hd, x.tu_ky),
                               {"hd": x.hd, "tu_ky": x.tu_ky, "nhan_mm": x.nhan_mm, "bat": x.bat,
                                "ngoai_le": list(x.ngoai_le_cdt1)}) for x in nen.luat],
            nguon=f"bai-h12:{c5a.ANH_MM.name}", actor="bai-h12")


def test_AC5_chay_tu_kho__co_tat_DO_roi_ky_bat_DAT():
    """Kho: bản nền cờ TẮT ⇒ ĐỎ có tên; `ky_bat_ix_alr` *(phiên bản MỚI, actor = người ký)* ⇒ ĐẠT. Giao dịch ROLLBACK."""
    with psycopg.connect(dsn_test()) as c:
        _nap_nen(c)
        t = c5a.chay_wp_c5a(conn=c)
        assert not t.phan_xu.dat and any("⛔ có luật nào BẬT" in x for x in t.phan_xu.ly_do)
        ban = chc.ky_bat_ix_alr(c, str(c5a.TEP_KY), actor="KhanhCQ")
        assert ban.actor == "KhanhCQ"
        t = c5a.chay_wp_c5a(conn=c)
        c.rollback()
    assert t.phan_xu.dat, t.phan_xu.ly_do[:3]
    assert (t.hd2_cong["tong_o"], t.hd2_cong["khop"]) == (MONG_TONG_O, MONG_KHOP)


def test_R1_05_kho_RONG_thieu_IX_ALR__DO_khong_dieu_kien():
    """`H12-R1-05`: ⛔ `if co_alr == 0` trên kho chung — bảng config ở SCHEMA TẠM RỖNG *(cùng hình bảng thật)*,
    giao dịch ROLLBACK ⇒ nhánh âm chạy MỌI lần."""
    with psycopg.connect(dsn_test()) as c:
        c.execute("CREATE SCHEMA h12_tam")
        for b in ("fls_cau_hinh_ban", "fls_cau_hinh_dong"):
            c.execute(f"CREATE TABLE h12_tam.{b} (LIKE public.{b} INCLUDING ALL)")
        c.execute("SET LOCAL search_path TO h12_tam")
        assert c.execute("SELECT count(*) FROM fls_cau_hinh_ban").fetchone()[0] == 0          # Đ3: rỗng THẬT
        t = c5a.chay_wp_c5a(conn=c)
        c.rollback()
    assert not t.phan_xu.dat and any("IX.ALR" in x and "ChuaKhai" in x for x in t.phan_xu.ly_do), t.phan_xu.ly_do


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
