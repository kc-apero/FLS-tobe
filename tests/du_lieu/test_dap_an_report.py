"""ẢNH ĐÁP ÁN Daily Report 2 · 3 — khuôn `daily_report_2` · `daily_report_3` *(ISP 3.1.2 · Step 41 · DT11 · `WO-269`)*.

⭐ Số đo 20/11 *(khoá SA chỉ-đọc; mỗi số đếm MỘT vật — Đ4)*:
  · **DR3** = tab `[MID][FS1][PLA5]5. Daily Report 3 (Sign off)` *(P&L Report, PD 605)*: **94** hàng sheet có giá trị
    *(5…137)* × **192** cột kỳ *(8 thực thể × 24 kỳ `202401…202512`)* + 2 cột năm = **13.541** ô số ≠ rỗng.
  · **DR2** = tab `5. Daily Report 2` *(CF report, PD 610)*: **846** hàng × **32** cột `G…AL` = **26.272** ô số ≠ rỗng.
  · CHECK IX.PL ② `NIS+INT+PIT+COM = CXA+GAH+DC+MC`: DR3 đo được **29**/192 kỳ-thực thể, đạt **14**; DR2 đo được
    **315**/315 kỳ-khối, đạt **267**. CHECK ① `NB = 0`: DR3 đo được **168**, ≠ 0 ở **12**; DR2 đo được **315**, ≠ 0 ở **119**.
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import importlib.util
import json
import pathlib
import sys
from decimal import Decimal

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
F = GOC / "tests" / "fixture" / "dap_an"
KH = GOC / "tools" / "khuon_dong_bang"
TEN = ("daily_report_2", "daily_report_3")

#: ⭐ số DÒNG ảnh *(Đ4: hàng sheet có giá trị)* · số cột ảnh *(khoá + chọn)* · ô số ≠ rỗng *(mẫu số — Đ3)*.
MONG = {"daily_report_2": (846, 39, 26272), "daily_report_3": (94, 199, 13541)}
CHECKSUM = {"daily_report_2": "01113b55ba953108", "daily_report_3": "ef1744caf253f3bd"}

#: ⭐ AC-2 — CHECK trên chính đáp án *(đo lần đầu 20/11 rồi khai — Đ5)*.
#: ⭐ `DT11-R1-03`: "đạt ②" tách làm hai ngăn — `cb_dat_co_so` *(≥ 1 trong 8 vế ≠ 0 mà vẫn cân = BẰNG CHỨNG DƯƠNG)* ·
#: `cb_dat_0_0` *(cả 8 vế đúng 0 ⇒ 0 = 0, ⛔ chứng minh gì)*. Đo 22/11: **0** kỳ nào có số mà cân ở CẢ HAI ảnh.
#: ⭐ `DT11-R1-04`: DR2 đếm trên NGÀY THẬT — 5 khối × 30 ngày = 150 + 160 kỳ luỹ kế = **310** kỳ-khối ② *(cột `AK` tách riêng)*.
MONG_CB = {"daily_report_2": {"cb_do": 310, "cb_dat": 262, "cb_dat_co_so": 0, "cb_dat_0_0": 262, "cb_khong_dat": 48,
                              "nb_do": 310, "nb_khac_0": 119, "cb_khong_do": 0},
           "daily_report_3": {"cb_do": 29, "cb_dat": 14, "cb_dat_co_so": 0, "cb_dat_0_0": 14, "cb_khong_dat": 15,
                              "nb_do": 168, "nb_khac_0": 12, "cb_khong_do": 163}}
#: kỳ KHÔNG đạt CHECK ② của DR3 *(kỳ · chênh = vế trái − vế phải, VND)*.
KHONG_DAT_DR3 = {
    "Group@202410": "145298916", "Group@202411": "775085821", "Group@202412": "-2079550",
    "Group@202501": "-432428076", "Group@202502": "-818524347", "Group@202503": "506642500",
    "Headquarters@202411": "205622500", "Headquarters@202412": "3837952354", "Headquarters@202501": "3990082885",
    "Headquarters@202502": "3582996844", "Headquarters@202503": "4882706764", "Headquarters@202504": "4482553322",
    "Headquarters@202505": "4826358961", "Headquarters@202506": "4820715416", "Headquarters@202507": "125000000"}
#: DR2: băm danh sách (kỳ · chênh làm tròn 1e-9) của 48 kỳ-khối không đạt *(danh sách đầy đủ ở BG-270)*.
BAM_DR2 = "d8bca5bddc797032"


def _doc(ten: str) -> dict:
    return json.loads((F / f"{ten}.json").read_text(encoding="utf-8"))


def _checksum_lai(anh: dict) -> str:
    """⭐ `DT11-R1-01`: TÍNH LẠI checksum từ `dong` + `phu` của CHÍNH tệp ảnh *(như `test_dap_an_atl`/`_gi`)*.
    Bản đầu chỉ so `a["checksum_noi_dung"]` *(chữ ghi sẵn trong ảnh)* với ghim ⇒ đổi +1 một ô NGOÀI 9 dòng CHECK
    ở DR3 và DR2 vẫn 28/28 xanh. Chữ ghi sẵn ⛔ phải bằng chứng; chỉ phép băm lại nội dung mới là."""
    phu = tuple({"phu": ten, "dong": r} for ten, b in anh.get("phu", {}).items() for r in b["dong"])
    return AnhChup(run_id=f"dong_bang_sheet:{anh['khuon']}",
                   ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _nap(ten: str):
    spec = importlib.util.spec_from_file_location(f"kh_{ten}_t", KH / f"{ten}.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module", params=TEN)
def bo(request):
    return request.param, _doc(request.param), _nap(request.param)


def _cot_so(ten, K):
    return K.COT_KY if ten.endswith("3") else K.COT_GT


# ── AC-1 ────────────────────────────────────────────────────────────────────

def test_AC1_anh_dong_cot_o_khac_0_va_cong_dat(bo):
    ten, a, K = bo
    n, c, o = MONG[ten]
    assert a["so_dong"] == len(a["dong"]) == n and a["cong"]["dat"] is True and a["cong"]["mong"] == n
    assert len(a["cot"]) == c and o > 0                                       # Đ3: mẫu số ≠ 0
    assert sum(1 for d in a["dong"] for x in _cot_so(ten, K) if d[x] is not None) == o
    assert a["checksum_noi_dung"] == _checksum_lai(a) == CHECKSUM[ten] and a["thieu"] == [] and a["trung"] == [] and a["o_rong"] == []
    assert a["bang"] == K.BANG


def test_AC1_gom_tren_dong_pl_va_ky_nhan_tung_so(bo):
    ten, a, K = bo
    khoa = [d["dong_sheet"] for d in a["dong"]]
    assert len(set(khoa)) == len(khoa) and all(k.isdigit() for k in khoa)
    if ten.endswith("3"):
        assert [c for c in a["cot"] if c.startswith("group_")] == [f"group_{y}{m:02d}" for y in (2024, 2025) for m in range(1, 13)]
    else:
        assert {d["che_do"]["chu"] for d in a["dong"]} == {"ngay", "luy_ke", "hr"}


# ── AC-2 · hai phép CHECK của IX.PL ─────────────────────────────────────────

def _tong(ck):
    return {"cb_do": sum(c["cb_do"] for c in ck.values()), "cb_dat": sum(c["cb_dat"] for c in ck.values()),
            "cb_dat_co_so": sum(c["cb_dat_co_so"] for c in ck.values()), "cb_dat_0_0": sum(c["cb_dat_0_0"] for c in ck.values()),
            "cb_khong_dat": sum(len(c["cb_khong_dat"]) for c in ck.values()), "nb_do": sum(c["nb_do"] for c in ck.values()),
            "nb_khac_0": sum(len(c["nb_khac_0"]) for c in ck.values()), "cb_khong_do": sum(c["cb_khong_do"] for c in ck.values())}


def test_AC2_check_so_ky_dat_khai_mong_mau_so_khac_0(bo):
    ten, a, K = bo
    ck = K.do_check(copy.deepcopy(a["dong"]))
    t = _tong(ck)
    assert t == MONG_CB[ten]
    assert t["cb_do"] > 0 and t["nb_do"] > 0                                  # Đ3: tập đo được ≠ rỗng
    assert t["cb_do"] == t["cb_dat"] + t["cb_khong_dat"]                       # mỗi kỳ vào ĐÚNG một ngăn
    assert t["cb_dat"] == t["cb_dat_co_so"] + t["cb_dat_0_0"]                  # `DT11-R1-03`: "đạt" = có số + 0=0
    assert t["cb_dat_0_0"] > 0                                                 # Đ3: ngăn 0=0 KHÔNG rỗng ⇒ nói thẳng nó là 0=0
    assert t["cb_dat_co_so"] == 0                                              # bằng chứng dương = 0 kỳ — khai RÕ, ⛔ để im


def test_R1_03_dai_goi_0_0_la_0_0_khong_goi_dat_tron(bo):
    """Nhãn ở dải in ra: ⛔ có chữ "đạt ②" trơn — luôn tách `có số` / `0=0` *(Đ3: mẫu số của bằng chứng dương)*."""
    ten, a, K = bo
    dai = K.thieu_lac(copy.deepcopy(a["dong"]))["dai"]
    assert "đạt ② có số" in dai and "đạt ② 0=0" in dai, dai
    assert "đạt ② có số 0" in dai                                                # bằng chứng dương khai 0 RÕ RÀNG


@pytest.mark.parametrize("ten", TEN)
def test_R1_03_PHA_ky_0_0_thanh_ky_co_so_thi_dat_co_so_tang_va_cong_DO(ten):
    """Đ5 hai chiều: biến MỘT kỳ 0=0 thành kỳ CÓ SỐ mà vẫn cân *(NIS += x, CXA += x)* ⇒ `cb_dat_co_so` 0 → 1 ⇒ ĐỎ."""
    a, K = _doc(ten), _nap(ten)
    d2 = copy.deepcopy(a["dong"])
    cot = "headquarters_202508" if ten.endswith("3") else "g"
    pick = lambda m: next(d for d in d2 if isinstance(d["ma"], dict) and d["ma"]["chu"] == m
                          and (ten.endswith("3") or (d["che_do"]["chu"] == "ngay" and d["khoi"]["chu"] == "HGO2")))
    n, c = pick("NIS"), pick("CXA")
    if ten.endswith("2"):
        cot = "j"                                                                # HGO2 · một ngày 0=0 chắc chắn đạt
    assert n[cot] is not None and c[cot] is not None
    n[cot] = str(Decimal(n[cot]) + Decimal("7")); c[cot] = str(Decimal(c[cot]) + Decimal("7"))
    ck = K.do_check(d2)
    assert sum(x["cb_dat_co_so"] for x in ck.values()) == 1
    r = K.thieu_lac(d2)
    assert r["thieu"], "đổi một kỳ 0=0 thành có-số mà cổng vẫn xanh"


def test_AC2_dr3_liet_ke_15_ky_khong_dat_ky_va_chenh():
    a = _doc("daily_report_3")
    ck = _nap("daily_report_3").do_check(a["dong"])
    got = {k: str(v) for c in ck.values() for k, v in c["chenh"].items()}
    assert got == KHONG_DAT_DR3 and len(got) == 15


def test_AC2_dr3_nhom_24_ky_group_202510_khong_do_duoc_vi_2_o_chu_so():
    """NIS · PIT của Group 202510 là ô CHỮ `7.252…`/`941.…` ⇒ ⛔ ép số ⇒ kỳ ấy ⛔ đo được (có tên, ⛔ coi là đạt)."""
    a = _doc("daily_report_3")
    K = _nap("daily_report_3")
    ck = K.do_check(a["dong"])
    assert ck["Group"]["cb_do"] == 6 and ck["Group"]["cb_khong_do"] == 18
    ma = {d["ma"]["chu"]: d for d in a["dong"] if isinstance(d["ma"], dict)}
    assert ma["NIS"]["group_202510"] is None and ma["PIT"]["group_202510"] is None
    assert [(r["o"]["chu"], r["cot"]["chu"]) for r in a["phu"]["o_chu_so"]["dong"]] == [("AF87", "group_202510"), ("AF89", "group_202510")]


def test_AC2_dr2_ban_48_ky_khong_dat_bam_khop():
    a = _doc("daily_report_2")
    ck = _nap("daily_report_2").do_check(a["dong"])
    q = Decimal("0.000000001")
    h = hashlib.sha256(json.dumps([(k, str(v.quantize(q))) for c in ck.values() for k, v in sorted(c["chenh"].items())]).encode()).hexdigest()[:16]
    assert h == BAM_DR2


@pytest.mark.parametrize("ten,ma,cot,them", [
    ("daily_report_3", "CXA", "headquarters_202508", "1000"),        # kỳ ĐẠT → thêm 1000 ⇒ ĐỎ
    ("daily_report_3", "NB", "visionlab_202401", "1"),               # NB = 0 → 1 ⇒ ĐỎ
    ("daily_report_2", "DC", "g", "1"),                              # (ngay,GROUP) 01/11 — ĐẠT → ĐỎ
])
def test_AC2_PHA_dot_bien_mot_o_thi_DO(ten, ma, cot, them):
    a, K = _doc(ten), _nap(ten)
    d2 = copy.deepcopy(a["dong"])
    hang = next(d for d in d2 if isinstance(d["ma"], dict) and d["ma"]["chu"] == ma
                and (ten.endswith("3") or (d["che_do"]["chu"] == "ngay" and d["khoi"]["chu"] == "GROUP")))
    assert hang[cot] is not None                                       # mẫu số của phép phá ≠ 0 (Đ3)
    assert K.thieu_lac(copy.deepcopy(a["dong"]))["thieu"] == []        # nền XANH trước khi phá
    hang[cot] = str(Decimal(hang[cot]) + Decimal(them))
    r = K.thieu_lac(d2)
    assert r["thieu"], "phá một ô mà cổng vẫn xanh"


def test_AC2_PHA_o_trong_hay_o_loi_la_khong_do_duoc_thi_DO(bo):
    ten, a, K = bo
    d2 = copy.deepcopy(a["dong"])
    hang = next(d for d in d2 if isinstance(d["ma"], dict) and d["ma"]["chu"] == "MC"
                and (ten.endswith("3") or (d["che_do"]["chu"] == "ngay" and d["khoi"]["chu"] == "GROUP")))
    cot = "headquarters_202508" if ten.endswith("3") else "g"
    hang[cot] = {"chu": "#REF!"}                                       # ô lỗi ở dòng của CHECK ⇒ ⛔ đo được ⇒ ĐỎ
    assert K.thieu_lac(d2)["thieu"]


def test_AC2_D3_tap_rong_va_mong_chua_khai_deu_do(bo, monkeypatch):
    ten, a, K = bo
    with pytest.raises(ValueError):
        K.thieu_lac([])
    monkeypatch.setattr(K, "MONG_CHECK", {})
    with pytest.raises(ValueError):
        K.thieu_lac(copy.deepcopy(a["dong"]))


# ── AC-3 · ô chỉnh tay ──────────────────────────────────────────────────────

def test_AC3_atl_AH12_tru_0_5_la_o_chinh_tay_co_ten_ghi_trong_anh_dr3():
    a = _doc("daily_report_3")
    t = a["phu"]["o_chinh_tay"]
    assert t["so_dong"] == t["mong"] == 1
    r = t["dong"][0]
    assert r["ten"]["chu"] == "chinh_tay_ATL_AH12" and r["o"]["chu"] == "AH12" and r["cong_thuc"]["chu"].endswith("AH12-0.5")
    atl = json.loads((F / "atl.json").read_text(encoding="utf-8"))
    hang = [d for d in atl["dong"] if d["dong_sheet"] == r["dong_sheet_atl"]]
    assert len(hang) == 1 and hang[0][r["cot_anh_atl"]["chu"]] is not None   # ô ATL có THẬT trong ảnh ATL
    assert "o_chinh_tay" not in _doc("daily_report_2")["phu"]


# ── AC-4 · dải ngày / kỳ ────────────────────────────────────────────────────

def test_AC4_dr3_8_thuc_the_x_24_ky_khong_ky_thieu():
    K = _nap("daily_report_3")
    a = _doc("daily_report_3")
    assert len(K.ENT) == 8 and len(K.KY) == 24 and K.KY[0] == "202401" and K.KY[-1] == "202512" and len(K.COT_KY) == 192
    assert K.CHUA_CO_DU_LIEU == ()                                     # đo 20/11: 192/192 (thực thể, kỳ) có ≥ 1 ô
    assert all(any(d[c] is not None for d in a["dong"]) for c in K.COT_KY)


def test_AC4_dr2_dai_ngay_01_30_11_2026_va_luy_ke_2025_den_2026_M6():
    a = _doc("daily_report_2")
    K = _nap("daily_report_2")
    td = {(r["dong_sheet"], r["cot"]["chu"]): r["gia_tri"] for r in a["phu"]["tieu_de"]["dong"]}
    assert [td[("9", c)] for c in ("G", "AJ")] == ["46327", "46356"]        # 2026-11-01 … 2026-11-30
    assert K.KY_NGAY[0][0] == "2026-11-01" and K.KY_NGAY[29][0] == "2026-11-30" and len(K.KY_NGAY) == 30
    # ⭐ `DT11-R1-04`: `AK` ⛔ ngày — trục RIÊNG `khong_ngay`, ⛔ lẫn vào 30 ngày thật
    assert K.COT_KHONG_NGAY == ("ak",) and K.NHAN_KHONG_NGAY == "khong_ngay" and "ak" not in {c for _, c in K.KY_NGAY}
    assert ("5", "AK") not in td and ("9", "AK") not in td and td[("6", "AK")] == {"chu": "Sat"}   # AK5 rỗng · "Sat" = serial 0
    assert [td[("428", c)] for c in ("G", "Z", "AG", "AL")] == ["2025", "2026", "1", "6"]   # Y2025 · Y2026 · M1 · M6
    assert td[("428", "H")] == {"chu": "H1"}
    assert K.KY_LUY_KE[-1][0] == "2026-M06" and len(K.KY_LUY_KE) == 32      # ⛔ có 2026-M07…M12 trong bố cục
    # kỳ có CỘT mà 0 ô ⇒ chua_co_du_lieu có tên (hr: số người 2026 H2·Q3·Q4)
    assert K.CHUA_CO_DU_LIEU == ("hr@2026-H2", "hr@2026-Q3", "hr@2026-Q4")
    assert all(any(d[c] is not None for d in a["dong"] if d["che_do"]["chu"] == "ngay") for _, c in K.KY_NGAY)


def test_R1_04_ngay_thuc_150_ngay_khoi_va_AK_dem_rieng_khong_cong_vao():
    """Đ4: `150` = 5 khối × 30 ngày THẬT *(⛔ 155 = 150 + 5 `AK`)*; `AK` có 844 ô số nhưng là vết kéo công thức."""
    a, K = _doc("daily_report_2"), _nap("daily_report_2")
    ck = K.do_check(copy.deepcopy(a["dong"]))
    assert sum(c["cb_do"] for k, c in ck.items() if k.startswith("ngay:")) == 150 == len(K.KHOI) * len(K.KY_NGAY)
    assert sum(c["cb_do"] for k, c in ck.items() if k.startswith("luy_ke:")) == 160
    ak = K.do_check_khong_ngay(copy.deepcopy(a["dong"]))
    assert set(ak) == {f"ngay:{k}" for k in K.KHOI} and sum(c["cb_do"] for c in ak.values()) == 5
    assert sum(1 for d in a["dong"] if d["che_do"]["chu"] == "ngay" and d["ak"] is not None) == 395 > 0   # Đ3: AK ở chế độ `ngay` = 395 ô (838 = cả 3 chế độ: ngay 395 · luy_ke 340 · hr 103)
    assert set(K.MONG_AK) == set(ak)


def test_R1_04_PHA_doi_mot_o_AK_thi_cong_DO_va_ngay_thuc_khong_doi():
    """AK RIÊNG ⇒ đổi AK (NB 0 → 1) làm `MONG_AK` ĐỎ mà `MONG_CHECK` *(ngày thật)* xanh — hai trục độc lập."""
    a, K = _doc("daily_report_2"), _nap("daily_report_2")
    d2 = copy.deepcopy(a["dong"])
    nb = next(d for d in d2 if d["che_do"]["chu"] == "ngay" and d["khoi"]["chu"] == "HGO2" and isinstance(d["ma"], dict) and d["ma"]["chu"] == "NB")
    assert nb["ak"] is not None                                             # mẫu số phép phá ≠ 0 (Đ3)
    nb["ak"] = "1"
    r = K.thieu_lac(d2)
    assert r["thieu"] and all("@ak" in x for x in r["thieu"]), r["thieu"]


def test_AC4_PHA_xoa_ca_cot_ngay_thi_chua_co_du_lieu_doi_va_DO():
    a, K = _doc("daily_report_2"), _nap("daily_report_2")
    d2 = copy.deepcopy(a["dong"])
    for d in d2:
        if d["che_do"]["chu"] == "ngay":
            d["aj"] = None
    assert "ngay@2026-11-30" in K.chua_co(d2) and K.thieu_lac(d2)["thieu"]


# ── AC-5 · ô lỗi ghi nguyên + đếm theo cột ──────────────────────────────────

def test_AC5_o_loi_dem_theo_cot_ghim_phan_bo_0_va_ghi_nguyen(bo):
    ten, a, K = bo
    assert a["o_loi"] == [] and set(a["loi_mong"].values()) == {0}
    assert set(a["loi_mong"]) == set(a["loi_theo_cot"]) == set(c for c in a["cot"] if c in K.KIEU_COT and K.KIEU_COT[c] == "so!")
    assert all(v == {} for v in a["loi_theo_cot"].values())
    assert sum(1 for d in a["dong"] for c in a["loi_mong"] if isinstance(d[c], dict)) == 0   # ô chữ ⛔ lọt vào cột so!


# ── AC-6 · khuôn mới = tệp riêng; ảnh cũ + công cụ chung đúng từng byte ─────

#: sha256 ghim — 22 ảnh `dap_an/*.json` có trước DT11 + `tools/dong_bang_sheet.py` *(⛔ đổi byte nào)*.
SHA_CU = {
    "atl.json": "0555a8b8a6656a688e1eb7518cbc66c84c6b3eef81b7da204d15bd5049f2d54e",
    "cfa1_daily.json": "7ae200cd36609c3bf4f9367baafbfb44ed4abea049d239dd120c5fe82fc20c65",
    "cfa1_yhqm.json": "eb6ac7bca1563cf6d46abb59ca9d118a684b6eb3a14e342a6db57c4f37e6409e",
    "cfa3.json": "2d5f9655018c275f33e37e3136a300e78a168bc5150a1150615bffc9da133246",
    "gi_mid1.json": "4a412ede8946411d1ce3a6a960db7ac2ca859fd3c981502b73a7b58e6cf9698f",
    "gi_mid2.json": "d44d45e6dae613bb7f809413c88913b5dbf770a9abd4d7dea78c4a6306fbdd21",
    "gi_mid3.json": "0b70c1c05cd29066b6c9a7fc8925c38e0724b4dc06dacf0a2ca72ac9ada7bcf4",
    "gl_406.json": "91987833e9bb15ecff46fd6631d00c8cf68d09da7ae575162b4d7850b5f81d90",
    "gl_406_dau_vao.json": "bf4a40aafa405954031b7d0f9a25ce76ca0e4da4a7eda48faf10615913084f82",
    "gl_cf_dau_vao.json": "e3f46e6c146db88e45414aa8b976b026b3b6e090874b2c7e42747bbebf57bad5",
    "gl_hr_407.json": "24383ccc578d1119a4644c991c1bc4b0453bea11019043a8814de0cf3e55e8a1",
    "gl_hr_408.json": "6361ee89258c74d548009e04b0ef075cc4528f87be443b641759f2611da8f419",
    "gl_hr_413.json": "356a5d7b2fee45790a065dd462b7266b6a781b1e4625ea64629e55d7db5672fa",
    "omc_mid1.json": "0a028cb052e7a9f784379acf5cae3cdab3eaf661ebd855cb23215c1b104e848b",
    "omc_mid2.json": "6798affb43aee6782b845d3acbf93664c5fe9f0174f8bcc7664d457876ac7cb2",
    "omc_mid3.json": "d355039020d0ce72758091d3c9aded8fa019755134e428240b4189b1ac23ed95",
    "ps_mid1.json": "77a63259337c05d9f1cbee30bccabf4f1565bc54564d87fc9feca796ea68e22b",
    "ps_mid2.json": "abe2404d3acb6aa583d645ffa638232609d2dc185d6d692eb749562dbadba22c",
    "ps_mid3.json": "f03e626255eb8cdbe4932d1c9810bd73fd5356968125e75ca1e11211fd6d12cc",
    "sc_mid1.json": "64168ac662f9ab237ff02e88c657cda8b95a53e12b4436c901842b7b8755214d",
    "sc_mid2.json": "b2bf949fd4358977b36e3bc00909143cc9c21bdeffc2a905d9ca92d24aad1d64",
    "sc_mid3.json": "5b887ef7ff4588f3c9191b916fe837d966d9c397641466d763fe4143033e0b9b",
    "dong_bang_sheet.py": "2d8c1724f8403608ffdc1766f148c8c01e22e6da914bb64b701aba4f3cd291c9",
}


def test_AC6_anh_cu_va_cong_cu_chung_dung_tung_byte():
    ten_cu = {k for k in SHA_CU if k != "dong_bang_sheet.py"}
    assert len(ten_cu) == 22
    for k in sorted(ten_cu):
        assert hashlib.sha256((F / k).read_bytes()).hexdigest() == SHA_CU[k], k
    assert hashlib.sha256((GOC / "tools" / "dong_bang_sheet.py").read_bytes()).hexdigest() == SHA_CU["dong_bang_sheet.py"]
    # ảnh DT11 là tệp mới, ngoài 22 ảnh cũ
    # + 4 ảnh H14 *(`DT11-R1-02`, vòng sửa KQ-271: PD 607·608·609·615)* — tệp MỚI, ⛔ đụng 22 ảnh cũ · 2 ảnh DT11
    assert {f.name for f in F.glob("*.json")} - ten_cu == {
        "daily_report_2.json", "daily_report_3.json", "daily_report_3_fs2.json", "daily_report_3_fs1.json",
        "daily_report_3_gop.json", "ccr_daily_report.json"}


def test_AC6_hai_khuon_la_tep_rieng_khong_dung_chung_than():
    for ten in TEN:
        assert (KH / f"{ten}.py").is_file()
    assert (KH / "_daily_report.py").is_file()


def test_AC6_anh_khong_mang_email_hay_cot_rieng_tu(bo):
    ten, a, K = bo
    assert not any("email" in c.casefold() for c in a["cot"])
    assert a["cot_khong_chon"] == []
    assert not any(isinstance(v, dict) and "@" in v.get("chu", "") for d in a["dong"] for v in d.values())


def test_kich_thuoc_anh_duoi_2MB_luat_DT4_R1_07(bo):
    ten, a, K = bo
    assert (F / f"{ten}.json").stat().st_size < 2 * 1024 * 1024        # DR2 ≈ 0,76 MB · DR3 ≈ 0,59 MB
