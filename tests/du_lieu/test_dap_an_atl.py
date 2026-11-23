"""ẢNH IX.DRV (Allocation Table) + ĐÁP ÁN ATL (PD 604 · 606) — khuôn `ix_drv` · `atl`
*(ISP 3.1.2 · Step 27 · DT10 · `WO-196`)*.

⭐ **Vì sao có tệp này.** AP v3.1.2 §3.2.2 IX.DRV · §3.4.2 PD 511–513 · 604 · 606. Engine AL.KEY
*(H12)* cần driver theo `(driver, CDT1, tháng)`; ATL *(606)* là đáp án P&L SAU phân bổ — mà AS-IS
**chưa phân bổ** *(ô `N1` "Cần add Formula Allocate")* ⇒ ATL chỉ đối chiếu được khi cờ luật TẮT (D2).

Số đo 18/11 *(khoá SA chỉ-đọc, phiên cloud — mỗi số đếm MỘT vật, Đ4)*:
  · nguồn = `[COPY] Report I General Ledger | P&L Report` — tab `Allocation Table | By NOEM & By
    GI` *(PD 604)* · `Allocation Table | NB | By LE` · `Report I PLA3 Y H Q M | PM + HR | ATL` *(606)*.
  · LƯỚI driver AP khai **4 loại × 8 CDT1 × 12 tháng = 384 ô**; nguồn có **238** ô số =
    NOEM 7×12 + GI-PE 7×11 + GI-PM 7×11, **146** ô THIẾU CÓ TÊN: NB **96** *(NB khoá theo
    LE From×To, ⛔ theo CDT1)* + CMN **36** *(3 driver × 12; CMN gộp vào SHQ1 theo CDT Correct)* +
    GI 202501 **14** *(2 driver × 7 CDT1; MID3 chỉ có 11 dòng `TOTAL` 202502…202512)*.
  · ATL = **829** hàng dữ liệu `8…1030` + khối KIỂM **80** hàng `1031…1110` + **120** ô gạch `-`.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
from collections import Counter
from decimal import Decimal

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
THU_MUC_KHUON = GOC / "tools" / "khuon_dong_bang"
F = GOC / "tests" / "fixture"
ANH = {"ix_drv": F / "cau_hinh" / "ix_drv.json", "atl": F / "dap_an" / "atl.json"}

#: ⭐ số DÒNG ảnh chính *(Đ4: ix_drv đếm cặp (driver, CDT1); atl đếm HÀNG sheet 8…1030)*.
MONG = {"ix_drv": 21, "atl": 829}
#: checksum_noi_dung ghim *(đổi ⇒ phải có lượt đóng băng mới + lý do)*.
CHECKSUM = {"ix_drv": "b0b9c7ef329e2821", "atl": "c47e93ef352b0f47"}

DRIVER = ("NOEM", "GI_PE", "GI_PM", "NB_LE")
CDT1_8 = ("SHQ2", "SHQ1", "COR", "CVL", "CSM", "CAH", "ASA", "CMN")
CDT1_7 = tuple(c for c in CDT1_8 if c != "CMN")
THANG = tuple(f"m{m:02d}" for m in range(1, 13))
#: AP khai 4 × 8 × 12 = 384 ô; nguồn 238 + 146 thiếu có tên.
MONG_THIEU = {"NB_LE": 96, "CMN": 36, "GI 202501": 14}


# ── trợ thủ ───────────────────────────────────────────────────────────────────

def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _nap_tool():
    spec = importlib.util.spec_from_file_location("dong_bang_sheet_dt10", TOOL)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def tool():
    return _nap_tool()


def _cong(tool, ten: str, dong: list[dict]) -> dict:
    """Chạy `thieu_lac` của khuôn trên BẢN SAO dòng ảnh *(đúng đường công cụ gọi)*."""
    kh = tool.nap_khuon(ten)
    return kh.thieu_lac(copy.deepcopy(dong))


def _checksum_lai(anh: dict) -> str:
    phu = tuple({"phu": ten, "dong": r} for ten, b in anh.get("phu", {}).items() for r in b["dong"])
    import datetime
    return AnhChup(run_id=f"dong_bang_sheet:{anh['khuon']}",
                   ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([sys.executable, str(TOOL), *doi_so], cwd=GOC, env=env,
                          capture_output=True, text=True, timeout=180)


# ══ AC-5 · khuôn mới = tệp riêng; công cụ chung ⛔ đổi ══════════════════════════

def test_AC5_hai_khuon_moi_la_tep_rieng():
    for ten in ("ix_drv", "atl"):
        assert (THU_MUC_KHUON / f"{ten}.py").is_file(), f"khuôn `{ten}` phải là tệp riêng"


def test_AC5_cong_cu_chung_dong_bang_sheet_khong_doi():
    """`DT10` ⛔ sửa công cụ chung *(bài ⛔ đòi — `so!` + `phu` + `LOI_MONG` đã đủ)*: sha256[:16]
    của `tools/dong_bang_sheet.py` ở nền `fba4849`. Mọi ảnh cũ ⇒ đúng từng byte."""
    sha = hashlib.sha256(TOOL.read_bytes()).hexdigest()[:16]
    # ⭐ `DT9b` *(`WO-241`)* — ĐỔI CÓ CHỦ ĐÍCH `ae917adbf80b1c14` → `2d8c1724f8403608`: thêm kiểu khoá `so_dong_sheet`
    #   *(`_khoa_hop_le` · `_gia_tri_khoa` · `KIEU_KHOA_BIET` — khoá `<SO>!<hàng>` của IX.VEN nhiều sổ)*; mọi
    #   kiểu khoá cũ ⛔ đổi nhánh ⇒ ảnh cũ đúng từng byte *(`SHA_CU` + `CHECKSUM` ở `test_dap_an_*`)*.
    assert sha == "2d8c1724f8403608", f"công cụ chung bị sửa: {sha}"


# ══ ảnh: cổng ĐẠT + checksum ═════════════════════════════════════════════════

@pytest.mark.parametrize("ten", ["ix_drv", "atl"])
def test_anh_cong_dat_va_checksum(ten):
    anh = _doc(ANH[ten])
    assert anh["so_dong"] == MONG[ten]
    assert anh["cong"]["dat"] is True, anh["cong"]["ly_do"]
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM[ten]


# ══ AC-1 · DT10-B1 · ix_drv: 4 loại × 8 CDT1 × 12 tháng — lệch CÓ TÊN ════════════

def test_DT10_B1_ix_drv_21_dong_3_driver_x_7_cdt1():
    anh = _doc(ANH["ix_drv"])
    assert anh["bang"] == "IX.DRV" and anh["so_dong"] == 21
    cap = Counter((_chu(r["driver"]), _chu(r["cdt1"])) for r in anh["dong"])
    assert set(cap) == {(d, c) for d in DRIVER[:3] for c in CDT1_7} and set(cap.values()) == {1}


def test_DT10_B1_luoi_384_o_238_so_146_thieu_co_ten():
    """Đ4: 384 = 4 loại × 8 CDT1 × 12 tháng *(AP khai)*; 238 ô SỐ ở nguồn; 146 ô thiếu có TÊN."""
    anh = _doc(ANH["ix_drv"])
    co = {(_chu(r["driver"]), _chu(r["cdt1"]), m) for r in anh["dong"] for m in THANG
          if r[m] is not None}
    assert len(co) == 238
    luoi = {(d, c, m) for d in DRIVER for c in CDT1_8 for m in THANG}
    assert len(luoi) == 384 and not (co - luoi)
    thieu = luoi - co
    assert len(thieu) == 146
    assert {(d, c, m) for (d, c, m) in thieu if d == "NB_LE"} == {
        ("NB_LE", c, m) for c in CDT1_8 for m in THANG}                       # 96
    assert {(d, c, m) for (d, c, m) in thieu if c == "CMN" and d != "NB_LE"} == {
        (d, "CMN", m) for d in DRIVER[:3] for m in THANG}                     # 36
    assert {(d, c, m) for (d, c, m) in thieu if m == "m01" and c != "CMN" and d != "NB_LE"} == {
        (d, c, "m01") for d in ("GI_PE", "GI_PM") for c in CDT1_7}            # 14
    # ảnh CHỨA tên từng ô thiếu *(bảng phụ `o_thieu`, 146 dòng)* — ⛔ lấp.
    pt = anh["phu"]["o_thieu"]
    assert pt["so_dong"] == pt["mong"] == 146
    assert {(_chu(r["driver"]), _chu(r["cdt1"]), _chu(r["thang"])) for r in pt["dong"]} == {
        (d, c, f"2025{m[1:]}") for (d, c, m) in thieu}


def test_DT10_B1_chi_co_2025_cot_nam_va_ngoai_2025():
    """Cổng "driver chỉ có 2025": mỗi hàng `nam` = 2025 *(đọc ở tiêu đề)* và `ngoai` = 0 *(ô có dữ
    liệu ngoài 12 cột tháng — P:Z đo 0)*."""
    anh = _doc(ANH["ix_drv"])
    assert {_chu(r["nam"]) for r in anh["dong"]} == {"2025"}
    assert {_chu(r["ngoai"]) for r in anh["dong"]} == {"0"}
    assert "2026" in anh["ghi_chu_khuon"] and "D2" in anh["ghi_chu_khuon"]


def test_DT10_B1_cong_thieu_lac_khop_mong_hai_chieu(tool):
    anh = _doc(ANH["ix_drv"])
    r = _cong(tool, "ix_drv", anh["dong"])
    assert r["thieu"] == [] and r["lac"] == []
    assert "238/384" in r["dai"] and "146" in r["dai"]


def _sua(anh: dict, cap, m, gia_tri):
    d = copy.deepcopy(anh["dong"])
    for r in d:
        if (_chu(r["driver"]), _chu(r["cdt1"])) == cap:
            r[m] = gia_tri
    return d


def test_DT10_B1_PHA_mat_mot_o_thi_DO_ten_o(tool):
    anh = _doc(ANH["ix_drv"])
    r = _cong(tool, "ix_drv", _sua(anh, ("NOEM", "COR"), "m05", None))
    assert r["thieu"] and any("NOEM|COR|202505" in x for x in r["thieu"]), r["thieu"]


def test_DT10_B1_PHA_lap_o_mong_thieu_cung_DO(tool):
    """Đ5 HAI CHIỀU: ô mong THIẾU mà nay CÓ *(vd GI 202501 được lấp)* cũng ĐỎ — buộc ghi lại khai."""
    anh = _doc(ANH["ix_drv"])
    r = _cong(tool, "ix_drv", _sua(anh, ("GI_PE", "CVL"), "m01", "0.5"))
    assert r["thieu"] and any("GI_PE|CVL|202501" in x for x in r["thieu"]), r["thieu"]


def test_DT10_B1_PHA_them_dong_CMN_thi_DO(tool):
    anh = _doc(ANH["ix_drv"])
    d = copy.deepcopy(anh["dong"])
    x = copy.deepcopy(d[0]); x["cdt1"] = {"chu": "CMN"}; x["ma"] = {"chu": "NOEM|CMN"}
    d.append(x)
    r = _cong(tool, "ix_drv", d)
    assert r["thieu"], "CMN có số ⇒ lệch khai (mong CMN thiếu 36 ô)"


@pytest.mark.parametrize("cot, gia_tri", [("nam", "2026"), ("ngoai", "3")])
def test_DT10_B1_PHA_2026_hoac_cot_ngoai_thi_DO(tool, cot, gia_tri):
    anh = _doc(ANH["ix_drv"])
    d = copy.deepcopy(anh["dong"]); d[0][cot] = gia_tri
    r = _cong(tool, "ix_drv", d)
    assert r["thieu"], f"{cot}={gia_tri} ⇒ driver ⛔ còn chỉ-2025"


def test_DT10_B1_PHA_tong_khac_100_phan_tram_thi_DO(tool):
    anh = _doc(ANH["ix_drv"])
    r = _cong(tool, "ix_drv", _sua(anh, ("NOEM", "CVL"), "m03", "0.9"))
    assert any(x.startswith("tong@NOEM|202503") for x in r["thieu"]), r["thieu"]


def test_DT10_B1_Đ3_tap_rong_la_do_khong_phai_xanh(tool):
    with pytest.raises(ValueError):
        _cong(tool, "ix_drv", [])
    with pytest.raises(ValueError):
        _cong(tool, "atl", [])


def test_DT10_B1_NB_theo_LE_khoa_From_To_304_hang_balance():
    anh = _doc(ANH["ix_drv"])
    nb = anh["phu"]["nb_le"]
    assert nb["so_dong"] == nb["mong"] == 304
    assert len({_chu(r["from"]) for r in nb["dong"]}) == 16
    assert Counter(_chu(r["loai"]) for r in nb["dong"])["V"] == 96      # 16 From × 6 To loại V
    assert all(f"m{m:02d}" in nb["dong"][0] for m in range(1, 13))
    assert "CREDIT" in anh["ghi_chu_khuon"] and "DEBIT" in anh["ghi_chu_khuon"]


# ══ AC-2 · nguồn ô NOEM: tab + địa chỉ + công thức gốc ═══════════════════════════

def test_AC2_nguon_noem_96_o_tab_dia_chi_cong_thuc():
    anh = _doc(ANH["ix_drv"])
    ng = anh["phu"]["nguon_noem"]
    assert ng["so_dong"] == ng["mong"] == 96            # 8 hàng (Group + 7 CDT1) × 12 tháng
    tab = "[H1.2026][2025]H1000 I HR Report"
    dem_hr = 0
    for r in ng["dong"]:
        assert _chu(r["tab_nguon"]) == tab
        ct = _chu(r["cong_thuc"])
        assert ct.startswith("="), "công thức GỐC ghi nguyên"
        if "$A$4289:$Q$4300" in ct:
            dem_hr += 1
            assert _chu(r["o_tu"]) and _chu(r["o_mau"]), "ô HR cứng của tử / mẫu"
    assert dem_hr == 84                                  # Group 12 + 6 hàng × 12; SHQ2 = 100% − Σ (12)
    # Đ3 · tử/mẫu ĐỌC từ HR *(⛔ rỗng)* và tái dựng NOEM ra ĐÚNG số ở ảnh:
    noem = {_chu(r["cdt1"]): r for r in anh["dong"] if _chu(r["driver"]) == "NOEM"}
    xet = 0
    for r in ng["dong"]:
        if _chu(r["cdt1"]) in ("Group", "SHQ2"):
            continue
        tu, mau = Decimal(r["tu"]), Decimal(r["mau"])
        assert mau != 0
        thang = _chu(r["thang"])
        got = Decimal(noem[_chu(r["cdt1"])]["m" + thang[4:]])
        assert abs(tu / mau - got) < Decimal("1e-12"), (r["o"], tu / mau, got)
        xet += 1
    assert xet == 72                                     # 6 CDT1 × 12 tháng (mẫu số ≠ 0, Đ3)
    for t in range(1, 13):                               # SHQ2 = phần dư ⇒ Σ 7 = 100%
        s = sum(Decimal(noem[c]["m%02d" % t]) for c in CDT1_7)
        assert abs(s - 1) < Decimal("1e-12")


# ══ AC-3 · atl.json: 604 · 606 — số dòng theo kỳ ═══════════════════════════════

#: Số hàng có SỐ *(⛔ rỗng, ⛔ '-')* theo CỘT của 57 cột kỳ 2024·2025·2026 — đo 18/11 trên 829 hàng.
#: Mỗi năm 19 cột: Y · H1 · H2 · Q1…Q4 · M01…M12.
# 2025: 19 × 824; 2024/2026: 7 × 824 (Y H1 H2 Q1-4) + 12 × 816 (M01…M12).
MONG_KY = ([824] * 7 + [816] * 12) + [824] * 19 + ([824] * 7 + [816] * 12)


def _cot_ky():
    out = []
    for y in (2024, 2025, 2026):
        out += [f"y{y}_{k}" for k in ("y", "h1", "h2", "q1", "q2", "q3", "q4")]
        out += [f"y{y}_m{m:02d}" for m in range(1, 13)]
    return out


def test_AC3_atl_829_hang_57_cot_ky_dong_theo_ky_khai_mong():
    anh = _doc(ANH["atl"])
    assert anh["bang"] == "SO.PLA3-ATL" and anh["so_dong"] == 829
    cot = _cot_ky()
    assert len(cot) == 57 and all(c in anh["cot"] for c in cot)
    dem = [sum(1 for r in anh["dong"] if r[c] is not None) for c in cot]    # số HOẶC lỗi, ⛔ rỗng
    assert dem == MONG_KY, "số hàng CÓ SỐ theo kỳ ⛔ khớp mong"
    assert anh["thieu"] == [] and anh["cong"]["dat"] is True


def test_AC3_atl_2026_chi_doi_chieu_khi_co_tat_D2_va_khoi_kiem():
    anh = _doc(ANH["atl"])
    g = anh["ghi_chu_khuon"]
    assert "chỉ đối chiếu khi cờ tắt (D2)" in g and "2026" in g
    assert "N1" in g and "Formula Allocate" in g
    k = anh["phu"]["kiem"]
    assert k["so_dong"] == k["mong"] == 80               # khối KIỂM sheet 1031…1110
    assert [int(_chu(r["dong_sheet"])) for r in k["dong"]] == list(range(1031, 1111))


def test_AC3_pd604_so_dong_theo_ky_GI_202501_la_0():
    """PD 604 = tab Allocation Table: số hàng CDT1 CÓ SỐ theo tháng — GI = 0 ở 202501 rồi 7;
    NOEM = 7 cả 12 tháng *(Đ3: 0 ở 202501 là KẾT QUẢ — MID3 ⛔ có dòng `TOTAL 202501`)*."""
    anh = _doc(ANH["atl"])
    p = {_chu(r["driver"]): [int(_chu(r[m])) for m in THANG] for r in anh["phu"]["pd604_ky"]["dong"]}
    assert p == {"NOEM": [7] * 12, "GI_PE": [0] + [7] * 11, "GI_PM": [0] + [7] * 11}
    # chéo với ảnh ix_drv: cùng một sự thật, hai nơi.
    drv = _doc(ANH["ix_drv"])
    for d, dem in p.items():
        for i, m in enumerate(THANG):
            assert dem[i] == sum(1 for r in drv["dong"]
                                 if _chu(r["driver"]) == d and r[m] is not None)


def test_AC3_PHA_mat_mot_o_thi_DO_ten_cot(tool):
    anh = _doc(ANH["atl"])
    d = copy.deepcopy(anh["dong"])
    d[10]["y2025_m06"] = None
    r = _cong(tool, "atl", d)
    assert r["thieu"] and any("y2025_m06" in x for x in r["thieu"]), r["thieu"]


def test_AC3_PHA_them_mot_o_thi_DO_hai_chieu(tool):
    anh = _doc(ANH["atl"])
    d = copy.deepcopy(anh["dong"])
    hang = next(r for r in d if r["y2024_m01"] is None)
    hang["y2024_m01"] = "1"
    r = _cong(tool, "atl", d)
    assert r["thieu"] and any("y2024_m01" in x for x in r["thieu"]), r["thieu"]


# ══ AC-4 · #REF!/#N/A ghi NGUYÊN chuỗi, ĐẾM theo cột, ghim phân bố ══════════════

def test_AC4_loi_ghi_nguyen_dem_theo_cot_ghim_phan_bo():
    anh = _doc(ANH["atl"])
    co = {"y2024_y": {"#N/A": 77}, **{f"y2024_q{q}": {"#VALUE!": 21} for q in range(1, 5)}}
    assert {c: v for c, v in anh["loi_mong"].items() if v} == co and len(anh["loi_mong"]) == 57
    assert {c: sum(v.values()) for c, v in anh["loi_theo_cot"].items() if v} \
        == {"y2024_y": 77, **{f"y2024_q{q}": 21 for q in range(1, 5)}}
    assert {c: {k.split(" ")[0]: n for k, n in v.items()} for c, v in anh["loi_theo_cot"].items() if v} == co
    assert len(anh["o_loi"]) == 77 + 84
    assert all(o["gia_tri"].startswith("#") for o in anh["o_loi"])
    # chuỗi NGUYÊN *(⛔ rút gọn)*: `#N/A` ở nguồn mang đuôi giải thích.
    assert any(len(o["gia_tri"]) > 10 for o in anh["o_loi"])


def test_AC4_khoi_kiem_560_value_ghi_nguyen_theo_cot():
    anh = _doc(ANH["atl"])
    dem = Counter()
    bools = 0
    for r in anh["phu"]["kiem"]["dong"]:
        for c in _cot_ky():
            v = r.get(c)
            if isinstance(v, dict) and v["chu"].startswith("#"):
                dem[(c, v["chu"].split(" ")[0])] += 1
            if isinstance(v, bool):
                bools += 1
    assert sum(dem.values()) == 560 and bools == 1997
    assert {k[1] for k in dem} == {"#VALUE!"}


def test_AC4_o_gach_120_o_5_hang_24_cot():
    anh = _doc(ANH["atl"])
    g = anh["phu"]["o_gach"]
    assert g["so_dong"] == g["mong"] == 120
    assert Counter(int(_chu(r["dong_sheet"])) for r in g["dong"]) == {998: 24, 999: 24, 1000: 24,
                                                                       1001: 24, 1002: 24}


def test_AC4_PII_may_quet_co_ca_pha(tmp_path):
    """Bản thô có cột `Email Address` ⇒ TỪ CHỐI cả lượt ở HAI khuôn *(exit 2)*, ⛔ in giá trị."""
    for ten in ("ix_drv", "atl"):
        p = tmp_path / f"{ten}.json"
        p.write_text(json.dumps({"nguon": "x", "doc_luc": "2026-11-18", "cach_doc": "x",
                                 "cot": ["L1", "Email Address"], "values": [["a", "b@x.vn"]]}),
                     encoding="utf-8")
        kq = _chay(ten, str(p), "--mong", "1", "--ra", str(tmp_path / "ra.json"))
        assert kq.returncode == 2, (kq.stdout[-300:], kq.stderr[-300:])
        assert "PM_COT_RIENG_TU" in kq.stdout + kq.stderr and "b@x.vn" not in kq.stdout + kq.stderr


@pytest.mark.parametrize("ten", ["ix_drv", "atl"])
def test_AC4_anh_khong_mang_email_hay_cot_rieng_tu(ten):
    van = ANH[ten].read_text(encoding="utf-8")
    assert van.count("Email Address") == 1, "chỉ nhắc ở câu khai PII"      # `khong_mang_PII`
    assert "@" not in "".join(
        _chu(r[c]) or "" for r in _doc(ANH[ten])["dong"] for c in r
        if isinstance(_chu(r[c]), str))


# ══ kích thước ảnh (luật `DT4-R1-07`) ═════════════════════════════════════════

def test_kich_thuoc_anh_khai_nguyen_nhan_neu_tren_2MB():
    for ten, p in ANH.items():
        n = p.stat().st_size
        anh = _doc(p)
        assert n < 2_000_000, f"{ten}: {n} B > 2 MB phải nêu NGUYÊN NHÂN trong ghi_chu_khuon"
        assert "MB" in anh.get("ghi_chu_khuon", "") or n < 500_000
