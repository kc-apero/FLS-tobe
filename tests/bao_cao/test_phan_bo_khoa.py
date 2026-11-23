"""`AL.KEY` — `phan_bo_khoa()` *(ISP 3.1.2 · Step 42 · H12 · `WO-291`)*.

H12-B1 · cờ IX.ALR TẮT *(mặc định C11 — D2)* ⇒ đầu ra = PLA3 PM+HR *(H8)* TỪNG Ô.
H12-B2 · bật cờ trên dữ liệu TỔNG HỢP *(⛔ dữ liệu thật — D2)*: Σ chia = tiền, đúng tỉ lệ driver; ô driver
         thiếu có tên ⇒ lỗi CÓ TÊN, ⛔ hoá 0.
AC-4 · đột biến 1 ô driver ⇒ phân bổ đổi đúng chỗ. AC-5 · cờ đọc từ `BangALR` *(⛔ hằng trong mã)*.

⭐ Đầu vào B1 = đầu ra `pla.pla_yhqm` của H8 trên ảnh đầu vào DT7b *(`tools/do_hd2_c3d.tinh_luoi`)* —
⛔ ảnh đáp án.
"""
from __future__ import annotations

import dataclasses
import datetime
import re
import sys
from decimal import Decimal
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.bao_cao import pla  # noqa: E402
from fls.bao_cao import phan_bo_khoa as pbk  # noqa: E402
from fls.bao_cao.cfa import KHOI_TONG  # noqa: E402
from fls.cau_hinh import luat_pb  # noqa: E402
from fls.cau_hinh.ky import LichKy  # noqa: E402
from tools import do_hd2_c3d as c3d  # noqa: E402
from tools import do_hd2_c5a as c5a  # noqa: E402

LICH = LichKy(nguon="bai-h12", ngay_dau=datetime.date(2024, 10, 21), luat="A")
DEN = datetime.date(2026, 2, 27)
KHOI_CDT6 = tuple(c3d.KHOI_CDT)          # CVL · COR · SHQ1 · CSM · CAH · ASA
#: mẫu số B1 khai TRƯỚC *(Đ3 · Đ4 — ô của lưới 419: 12 khối × 74 mã × 57 kỳ)*
MONG_O_419 = 12 * 74 * 57


@pytest.fixture(scope="module")
def nguon():
    return c3d.nap_nguon()


@pytest.fixture(scope="module")
def pla3(nguon):
    gl, hr, _, fx, cay = nguon
    luoi, _ = c3d.tinh_luoi(gl, hr, fx, cay, LICH, DEN, [])
    return luoi["pla3_pm_hr_yhqm"]


@pytest.fixture(scope="module")
def cay(nguon):
    return nguon[4]


@pytest.fixture(scope="module")
def alr_tat():
    return c5a.alr_tu_anh_mm(tu_ky=202410)       # cùng đường `luat_pb.dung_tu_mm` + `kiem` của C11


@pytest.fixture(scope="module")
def driver():
    return c5a.luoi_driver_tu_anh()


def _bat(alr: luat_pb.BangALR, *ma: str) -> luat_pb.BangALR:
    """Bản TỔNG HỢP có cờ bật *(chỉ trong bài — `luat_pb.kiem` cấm `bat=True`, D2)*."""
    return luat_pb.BangALR(nguon=alr.nguon + " +bật(tổng hợp)",
                           luat=tuple(dataclasses.replace(x, bat=True) if (not ma or x.hd in ma) else x
                                      for x in alr.luat))


def _chay(kq, alr, cay, driver=None):
    return pbk.phan_bo_khoa(kq, alr, cay, pla.CONG_THUC_PM, khoi_nguon=KHOI_TONG, khoi_cdt=KHOI_CDT6,
                            khoi_du=c3d.KHOI_DU, driver=driver)


# ── H12-B1 · cờ tắt = đồng nhất ─────────────────────────────────────────────────────────────────

def test_H12_B1_co_tat__dau_ra_bang_PLA3_tung_o(pla3, alr_tat, cay):
    assert len(pla3.o) == MONG_O_419, "Đ3: mẫu số lưới 419 ≠ khai trước"
    assert sum(1 for v in pla3.o.values() if v) > 0, "Đ3: lưới toàn 0 ⇒ so đồng nhất xanh trên tập rỗng"
    assert all(x.bat is False for x in alr_tat.luat) and len(alr_tat.luat) == 17
    kq = _chay(pla3, alr_tat, cay)
    assert set(kq.o) == set(pla3.o)
    khac = [k for k in pla3.o if kq.o[k] != pla3.o[k]]          # ⛔ dung sai: đồng nhất là ĐÚNG từng ô
    assert khac == [], khac[:5]
    assert kq.dem == {"o": MONG_O_419, "o_chia": 0, "luat_bat": 0}


def test_H12_B1_khong_co_bang_luat__loi_co_ten(pla3, cay):
    with pytest.raises(pbk.LoiPhanBoKhoa) as e:
        _chay(pla3, None, cay)
    assert e.value.ma == pbk.LUAT_THIEU


# ── lưới tổng hợp ───────────────────────────────────────────────────────────────────────────────

KY = ["2025", "2025H1", "2025H2", "2025Q1", "2025Q2", "2025Q3", "2025Q4"] + [f"2025M{m:02d}" for m in range(1, 13)] \
     + ["2026", "2026M01"]


def _tong_hop(cay, tien: dict[tuple[str, str], Decimal]) -> pla.KetQuaPLA:
    """Lưới TỔNG HỢP *(⛔ dữ liệu thật)*: lá GROUP theo `tien[(mã, tháng)]`; khối CDT/dư = 0 *(chưa chia)*;
    Y/H/Q = Σ tháng; tong/kpi theo công thức PM."""
    khoi = (KHOI_TONG,) + KHOI_CDT6 + (c3d.KHOI_DU,)
    loai = pla.loai_ma(cay, pla.CONG_THUC_PM)
    la = {(kh, n.ma, t): Decimal(0) for kh in khoi for n in cay.nut for t in KY}
    for (m, t), v in tien.items():
        assert loai[m] == "la"
        la[(KHOI_TONG, m, t)] = v
        for k in pbk.ky_gop(t):
            if k in KY:
                la[(KHOI_TONG, m, k)] += v
    for (kh, m, t), v in list(la.items()):
        if kh == c3d.KHOI_DU:
            la[(kh, m, t)] = la[(KHOI_TONG, m, t)]
    return pla.KetQuaPLA(o=pla.danh_gia(la, cay, KY, khoi, pla.CONG_THUC_PM), cot=list(KY), khoi=khoi,
                         loai=loai, la=la)


def test_H12_B1_tong_hop__co_tat_dong_nhat(cay, alr_tat, driver):
    kq0 = _tong_hop(cay, {("LC", "2025M03"): Decimal("100"), ("OFR", "2025M05"): Decimal("-7.5")})
    kq = _chay(kq0, alr_tat, cay, driver)
    assert kq.o == kq0.o and kq.dem["o_chia"] == 0


# ── H12-B2 · bật cờ trên dữ liệu tổng hợp ───────────────────────────────────────────────────────

DUNG_SAI = Decimal("1e-12")


def test_H12_B2_by_GI__sigma_chia_bang_tien__dung_ti_le_driver(cay, alr_tat, driver):
    tien = Decimal("100")
    kq0 = _tong_hop(cay, {("LC", "2025M03"): tien})
    kq = _chay(kq0, _bat(alr_tat, "LC"), cay, driver)
    chia = {kh: kq.o[(kh, "LC", "2025M03")] for kh in KHOI_CDT6}
    for kh in KHOI_CDT6:                                         # đúng tỉ lệ driver PE *(D3: By GI ⇒ PE)*
        assert chia[kh] == tien * driver.o[("GI_PE", kh, 202503)], kh
    du = kq.o[(KHOI_TONG, "LC", "2025M03")] - sum(chia.values())
    assert kq.o[(c3d.KHOI_DU, "LC", "2025M03")] == du
    assert abs(du - tien * driver.o[("GI_PE", "SHQ2", 202503)]) <= DUNG_SAI      # dư SHQ2 = phần driver SHQ2
    assert abs(sum(chia.values()) + du - tien) <= DUNG_SAI                        # Σ chia = tiền
    co_so = sum(1 for kh in KHOI_CDT6 if driver.o[("GI_PE", kh, 202503)])
    assert co_so >= 5 and sum(1 for v in chia.values() if v) == co_so, "Đ3: chia ra 0 ⇒ ⛔ đo được tỉ lệ"
    # cuộn kỳ + cây + KPI tính LẠI: Q1/H1/Y của khối CDT = tháng; tong `COS` ⊇ `LC`
    for kh in KHOI_CDT6:
        for k in ("2025Q1", "2025H1", "2025"):
            assert kq.o[(kh, "LC", k)] == chia[kh]
        assert kq.o[(kh, "PL3", "2025M03")] == kq.o[(kh, "PL2", "2025M03")] + chia[kh]   # PL3 = PL2 + API + SC + LC
    assert kq.dem["o_chia"] == 6 and kq.dem["luat_bat"] == 1
    assert kq.o[(KHOI_TONG, "LC", "2025M03")] == kq0.o[(KHOI_TONG, "LC", "2025M03")]   # GROUP ⛔ đổi


def test_H12_B2_by_NOEM__ngoai_le_OFR_CAH_giu_nguyen(cay, alr_tat, driver):
    kq0 = _tong_hop(cay, {("OFR", "2025M05"): Decimal("-7.5"), ("REC", "2025M05"): Decimal("3")})
    kq = _chay(kq0, _bat(alr_tat, "OFR", "REC"), cay, driver)
    d = {kh: driver.o[("NOEM", kh, 202505)] for kh in (*KHOI_CDT6, c3d.KHOI_DU)}
    for kh in KHOI_CDT6:
        assert kq.o[(kh, "REC", "2025M05")] == Decimal("3") * d[kh]
        # AP §3.2.5: CAH ⛔ chia By NOEM. ⭐ Vòng sửa R1 `H12` *(SA FORMULA ATL 22/11, ô `OFR` khối CDT 2025)*: AS-IS
        #   chia phần CÒN LẠI theo NOEM chuẩn hoá TRỪ ngoại lệ — `NOEM_khối / (NOEM_GAG − NOEM_CAH)`.
        mong_ofr = Decimal(0) if kh == "CAH" else Decimal("-7.5") * (d[kh] / (1 - d["CAH"]))
        assert kq.o[(kh, "OFR", "2025M05")] == mong_ofr, kh
    assert kq.dem["o_chia"] == 11
    assert d["CAH"] != 0, "Đ3: driver CAH = 0 ⇒ chuẩn hoá ⛔ đo được"


def test_H12_R1_06_by_NOEM__sigma_DOC_LAP_voi_cong_thuc_du(cay, alr_tat, driver):
    """`H12-R1-06` — Σ chia so với tiền × driver đo NGOÀI công thức dư *(dư := GROUP − Σ CDT ⇒ "Σ = tiền" luôn
    đúng)*: dư SHQ2 phải bằng tiền × NOEM_SHQ2 *(⇔ Σ7 NOEM = 1)*; OFR: tiền × NOEM_SHQ2 / (1 − NOEM_CAH)."""
    tien_rec, tien_ofr = Decimal("3"), Decimal("-7.5")
    kq0 = _tong_hop(cay, {("REC", "2025M05"): tien_rec, ("OFR", "2025M05"): tien_ofr})
    kq = _chay(kq0, _bat(alr_tat, "OFR", "REC"), cay, driver)
    d = {kh: driver.o[("NOEM", kh, 202505)] for kh in (*KHOI_CDT6, c3d.KHOI_DU)}
    assert abs(kq.o[(c3d.KHOI_DU, "REC", "2025M05")] - tien_rec * d[c3d.KHOI_DU]) <= DUNG_SAI
    assert abs(kq.o[(c3d.KHOI_DU, "OFR", "2025M05")] - tien_ofr * d[c3d.KHOI_DU] / (1 - d["CAH"])) <= DUNG_SAI
    assert d[c3d.KHOI_DU] != 0, "Đ3: driver SHQ2 = 0 ⇒ dư = 0 xanh trên tập rỗng"


def test_H12_R1_OFR_driver_ngoai_le_thieu__loi_co_ten(cay, alr_tat, driver):
    o2 = {k: v for k, v in driver.o.items() if k != ("NOEM", "CAH", 202505)}
    kq0 = _tong_hop(cay, {("OFR", "2025M05"): Decimal("-7.5")})
    with pytest.raises(pbk.LoiPhanBoKhoa) as e:
        _chay(kq0, _bat(alr_tat, "OFR"), cay, dataclasses.replace(driver, o=o2))
    assert e.value.ma == pbk.DRIVER_THIEU and "NOEM|CAH|202505" in str(e.value)


@pytest.mark.parametrize("ma, thang, mau", [
    ("LC", "2025M01", "GI_PE|CVL|202501"),        # o_thieu `GI 202501` (MID3 thiếu TOTAL 202501)
    ("LC", "2026M01", "GI_PE|CVL|202601"),        # chỉ 2025 có driver *(ISP mục 3)*
])
def test_H12_B2_driver_thieu__loi_co_ten__khong_hoa_0(cay, alr_tat, driver, ma, thang, mau):
    kq0 = _tong_hop(cay, {(ma, thang): Decimal("5")})
    with pytest.raises(pbk.LoiPhanBoKhoa) as e:
        _chay(kq0, _bat(alr_tat, ma), cay, driver)
    assert e.value.ma == pbk.DRIVER_THIEU
    assert mau in str(e.value) and len(e.value.o_thieu) == 6, e.value.o_thieu   # MỌI ô thiếu, ⛔ ô đầu
    if thang == "2025M01":
        assert "MID3" in str(e.value)             # lý do có tên lấy từ bảng `o_thieu` của ảnh


def test_H12_B2_bat_co_ma_khong_co_driver__loi_co_ten(cay, alr_tat):
    kq0 = _tong_hop(cay, {("LC", "2025M03"): Decimal("1")})
    with pytest.raises(pbk.LoiPhanBoKhoa) as e:
        _chay(kq0, _bat(alr_tat, "LC"), cay, None)
    assert e.value.ma == pbk.DRIVER_THIEU


def test_H12_B2_H1000_khong_qua_allocate(cay, alr_tat, driver):
    kq0 = _tong_hop(cay, {("NIS", "2025M03"): Decimal("9")})
    kq = _chay(kq0, _bat(alr_tat, "NIS"), cay, driver)
    assert kq.o == kq0.o and kq.dem["o_chia"] == 0          # Q3: H1000 ⛔ qua ALLOCATE dù cờ bật


# ── AC-4 · đột biến driver ───────────────────────────────────────────────────────────────────────

def test_AC4_dot_bien_mot_o_driver__chi_doi_dung_cho(cay, alr_tat, driver):
    kq0 = _tong_hop(cay, {("LC", "2025M03"): Decimal("100"), ("LC", "2025M04"): Decimal("50")})
    a = _chay(kq0, _bat(alr_tat, "LC"), cay, driver)
    o2 = dict(driver.o)
    o2[("GI_PE", "COR", 202504)] += Decimal("0.01")
    b = _chay(kq0, _bat(alr_tat, "LC"), cay, dataclasses.replace(driver, o=o2))
    doi = {k for k in a.o if a.o[k] != b.o[k] and k[1] != "NPC"}     # NPC = Σ HẬU TỐ ⇒ đổi mọi kỳ trước
    assert all(a.o[k] != b.o[k] for k in [("COR", "NPC", "2025M01"), (c3d.KHOI_DU, "NPC", "2025M04")])
    assert doi and {(kh, t) for kh, _, t in doi} <= {("COR", t) for t in ("2025M04", "2025Q2", "2025H1", "2025")} \
        | {(c3d.KHOI_DU, t) for t in ("2025M04", "2025Q2", "2025H1", "2025")}, sorted(doi)[:10]
    assert b.o[("COR", "LC", "2025M04")] - a.o[("COR", "LC", "2025M04")] == Decimal("0.5")


# ── AC-5 · cờ đọc từ IX.ALR, ⛔ hằng ─────────────────────────────────────────────────────────────

def test_AC5_co_lay_tu_bang_ALR__chi_ma_bat_moi_chia(cay, alr_tat, driver):
    kq0 = _tong_hop(cay, {("LC", "2025M03"): Decimal("10"), ("BRC", "2025M03"): Decimal("20")})
    kq = _chay(kq0, _bat(alr_tat, "BRC"), cay, driver)
    assert all(kq.o[(kh, "LC", "2025M03")] == 0 for kh in KHOI_CDT6)
    assert all(kq.o[(kh, "BRC", "2025M03")] == Decimal(20) * driver.o[("GI_PE", kh, 202503)] for kh in KHOI_CDT6)
    assert any(kq.o[(kh, "BRC", "2025M03")] for kh in KHOI_CDT6)


def test_AC5_hieu_luc_theo_ky(cay, alr_tat, driver):
    """Luật có `tu_ky` 202506 ⇒ tháng 2025M03 ⛔ chia, 2025M07 chia *(`luat_cua` của C11)*."""
    muon = luat_pb.BangALR(nguon="tong-hop", luat=tuple(dataclasses.replace(x, tu_ky=202506, bat=True)
                                                       for x in alr_tat.luat if x.hd == "LC"))
    kq0 = _tong_hop(cay, {("LC", "2025M03"): Decimal("10"), ("LC", "2025M07"): Decimal("10")})
    kq = _chay(kq0, muon, cay, driver)
    assert all(kq.o[(kh, "LC", "2025M03")] == 0 for kh in KHOI_CDT6)
    assert all(kq.o[(kh, "LC", "2025M07")] == Decimal(10) * driver.o[("GI_PE", kh, 202507)] for kh in KHOI_CDT6)
    assert any(kq.o[(kh, "LC", "2025M07")] for kh in KHOI_CDT6)


def test_AC5_ma_nguon_khong_go_cung_ma_HD():
    van = (GOC / "fls" / "bao_cao" / "phan_bo_khoa.py").read_text(encoding="utf-8")
    ma = ["LC", "BRC", "CXP", "OSF", "FNS", "CIO", "CXB", "CXO", "OFR", "HCC", "REC", "BON", "OGA", "CAH"]
    trung = [m for m in ma if re.search(rf"[\"']{m}[\"']", van)]
    assert trung == [], trung


def test_ky_gop_va_ky_la():
    assert pbk.ky_gop("2025M05") == ("2025Q2", "2025H1", "2025")
    assert pbk.thang_cua("2025M05") == 202505 and pbk.thang_cua("2025Q2") is None
    with pytest.raises(pbk.LoiPhanBoKhoa) as e:
        pbk.ky_gop("2025X9")
    assert e.value.ma == pbk.KY_LA


# ── Vòng sửa R1 `H12` *(`KQ-293`)* — cờ BẬT 2025 theo tệp KÝ *(quyết của chủ 22/11)* trên lưới THẬT ─────────

def test_H12_R1_co_ky_2025__ky_ngoai_2025_dong_nhat_tru_NPC_hau_to(pla3, cay, driver):
    """Luật ký chỉ hiệu lực 202501…202512 ⇒ mọi ô kỳ 2024/2026 GIỮ NGUYÊN `==` *(⛔ dung sai)*, trừ `NPC` 2024 —
    `NPC` = Σ HẬU TỐ ⇒ kéo theo kỳ sau *(AC-4)*. Đo trước sửa: 6 ô `SHQ2` `BON`/`HCC` 2026 Y/H1/Q1 lệch 1e-29
    *(dư SHQ2 tính lại CẢ kỳ ⛔ chia)*."""
    kq = _chay(pla3, c5a.alr_ky_tu_anh(), cay, driver)
    assert kq.dem["o_chia"] > 0 and kq.dem["luat_bat"] == 11, kq.dem      # 13 mã bật − CXP, CXO (GROUP 2025 = 0)
    doi = [k for k in pla3.o if k[2][:4] != "2025" and kq.o[k] != pla3.o[k]]
    assert {k[1] for k in doi} <= {"NPC"} and all(k[2][:4] == "2024" for k in doi), sorted(doi)[:8]
    assert doi, "Đ3: NPC hậu tố phải đổi — ⛔ thì phép chia ⛔ chạm lưới"
