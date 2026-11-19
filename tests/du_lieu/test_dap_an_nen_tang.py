"""ĐÁP ÁN MID1–MID3 của OMC · SC · PS — khuôn `{omc,sc,ps}_mid{1,2,3}` *(ISP 3.1.2 · DT9 · `WO-220`)*.

⭐ **Vì sao có tệp này.** H11 *(AL.PLT cho OMC · SC · PS)* cần 9 ẢNH đứng yên, cùng hình với GI
*(`test_dap_an_gi.py` — DT8 + DT8b)*: MID1 *(phân bổ 7 CDT1, cột thượng nguồn `f`)* · MID2 *(RATE)* ·
MID3 *(Σ chia = O/P, khoá `vendor` + `thang`)*.

⛔⛔ **Bản đọc thô thật ⛔ nằm trong repo** *(PII — `CLAUDE.md` Riêng tư)*. Bài kiểm ẢNH đã commit
+ chạy THẲNG `thieu_lac` của từng khuôn trên dòng ảnh *(ca phá = sửa một dòng ảnh ⇒ ĐỎ)*.

⭐ **Số đo 19/11 *(khoá SA chỉ-đọc — mỗi số đếm MỘT vật, Đ4)*:**
  · hàng ảnh MID1 = OMC **6.230** · SC **5.187** *(+574 hàng đệm)* · PS **8.505**;
    MID2 = **1.470** · **581** · **3.339**; MID3 *(hàng `O` là số)* = **900** · **750** *(+10 ngoài)* ·
    **594** *(+1.476 ngoài)*.
  · ⛔ **"PS thiếu 7 tháng 03–09/2026" của AP KHÔNG tái lập được như đã viết**: ba sổ nguồn
    `H2.2025` chỉ có tháng `202503/04…202512` *(OMC 10 · SC 9 · PS 9)*, ⛔ có tháng 2026 nào. Cổng
    đếm đúng điều đo được: 7/7 tháng `202603…202609` có **0** dòng ở CẢ BA sổ; PS thiếu `202503`
    so với kỳ đối chiếu OMC *(1 tháng)*.
"""
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
THU_MUC_KHUON = GOC / "tools" / "khuon_dong_bang"
DAP_AN = GOC / "tests" / "fixture" / "dap_an"

SO = ("omc", "sc", "ps")
TEN = [f"{s}_mid{m}" for s in SO for m in (1, 2, 3)]

#: Số dòng ảnh *(đếm DÒNG ảnh, ⛔ cột)* — đo độc lập với khuôn.
MONG = {"omc_mid1": 6230, "sc_mid1": 5187, "ps_mid1": 8505,
        "omc_mid2": 1470, "sc_mid2": 581, "ps_mid2": 3339,
        "omc_mid3": 900, "sc_mid3": 750, "ps_mid3": 594}
#: Dòng theo THÁNG. MID3 = hàng CÓ khoá *(`vendor` ≠ rỗng)*; hàng tổng-tháng ⛔ khoá ⇒ đếm riêng.
_T10 = [f"2025{m:02d}" for m in range(3, 13)]
_T9 = [f"2025{m:02d}" for m in range(4, 13)]
THANG_MONG = {
    "omc_mid1": {t: 623 for t in _T10}, "omc_mid2": {t: 147 for t in _T10},
    "omc_mid3": {t: 89 for t in _T10},
    "sc_mid1": {**{t: 427 for t in _T9[:3]}, **{t: 651 for t in _T9[3:]}},
    "sc_mid2": {**{t: 63 for t in _T9[:7]}, **{t: 70 for t in _T9[7:]}},
    "sc_mid3": {**{t: 61 for t in _T9[:3]}, **{t: 93 for t in _T9[3:]}},
    "ps_mid1": {t: 945 for t in _T9}, "ps_mid2": {t: 371 for t in _T9},
    "ps_mid3": {t: 65 for t in _T9},
}
#: Đ5 — phân bố ô lỗi `so!` *(loại lỗi → số ô)*, đo 19/11 trên hàng ảnh.
LOI = {
    "omc_mid1": {"u": {"#VALUE!": 84, "#DIV/0!": 4836}, "v": {"#VALUE!": 84, "#DIV/0!": 4836}},
    "sc_mid1": {"u": {"#VALUE!": 1314, "#DIV/0!": 2796}, "v": {"#VALUE!": 1314, "#DIV/0!": 2796}},
    "ps_mid1": {"u": {"#DIV/0!": 7290}, "v": {"#DIV/0!": 7290}},
    "omc_mid2": {"rate": {"#DIV/0!": 931}, "u": {"#VALUE!": 462, "#DIV/0!": 798},
                 "v": {"#VALUE!": 462, "#DIV/0!": 798}},
    "sc_mid2": {"rate": {"#DIV/0!": 273}, "u": {"#DIV/0!": 240, "#VALUE!": 254, "#REF!": 8},
                "v": {"#DIV/0!": 240, "#VALUE!": 254, "#REF!": 8}},
    "ps_mid2": {"rate": {"#DIV/0!": 3339}, "u": {"#DIV/0!": 2898}, "v": {"#DIV/0!": 2898}},
}
ITL_NA = {"omc_mid1": 559, "sc_mid1": 592, "ps_mid1": 1069}          # `R` ITL ID `#N/A`
PM_CHU = {"omc_mid1": 5899, "sc_mid1": 5038, "ps_mid1": 8359,        # `S`/`P` = 'Need to manual input'
          "omc_mid3": 559, "sc_mid3": 490, "ps_mid3": 439}
DEM = {"omc_mid1": 0, "sc_mid1": 574, "ps_mid1": 0}                   # hàng đệm MID1
MID3_TONG = {"omc_mid3": 10, "sc_mid3": 9, "ps_mid3": 9}              # hàng tổng-tháng ⛔ khoá
MID3_NGOAI = {"omc_mid3": 0, "sc_mid3": 10, "ps_mid3": 1476}          # hàng `O` ⛔ số — ⛔ vào ảnh
MID3_LECH_PE = {"omc_mid3": 0, "sc_mid3": 72, "ps_mid3": 0}           # Σ 6 PE_cdt ≠ O *(nguồn lệch)*
MID3_PE_KHAC0 = {"omc_mid3": 431, "sc_mid3": 1014, "ps_mid3": 0}      # ô ≠ 0 vế PE *(cdt PE + O)*

CHECKSUM = {
    "omc_mid1": "a2149d4ec0384a88",
    "omc_mid2": "f12998c1e36fa48c",
    "omc_mid3": "00a16cbcac66f723",
    "sc_mid1": "a0122790698b1e24",
    "sc_mid2": "7a0690e9a60130c3",
    "sc_mid3": "ec677675b14fe365",
    "ps_mid1": "977dd197ff287f06",
    "ps_mid2": "44da3e83c3b56d32",
    "ps_mid3": "4ca2a71220e1da09"
}   # ghim lượt đóng băng 19/11 — đổi ⇒ lượt mới + lý do

CDT1_7 = {"SHQ2 | Headquarters2", "CVL | VisionLab", "COR | TeraSofts", "SHQ1 | Headquarters1",
          "CSM | SuperMinds", "CAH | Astronex", "ASA | Super App"}
COT_CAM = {"email address"}
#: ảnh đã commit ở DT2/DT8 — ⛔ đổi 1 byte *(AC-6)*; sha256[:16] của tệp.
SHA_CU = {"gi_mid1": "4a412ede8946411d", "gi_mid2": "d44d45e6dae613bb", "gi_mid3": "0b70c1c05cd29066"}


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _anh(ten: str) -> dict:
    p = DAP_AN / f"{ten}.json"
    assert p.is_file(), f"ảnh {p.name} chưa có"
    return _doc(p)


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _khuon(ten: str):
    spec = importlib.util.spec_from_file_location("dong_bang_sheet_nt", TOOL)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m.nap_khuon(ten)


def _checksum_lai(anh: dict) -> str:
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _theo_thang(dong: list[dict], chi_co_khoa: bool = False) -> dict[str, int]:
    out: dict[str, int] = {}
    for d in dong:
        if chi_co_khoa and _chu(d.get("vendor")) is None:
            continue
        t = d["thang"]
        out[t] = out.get(t, 0) + 1
    return dict(sorted(out.items()))


# ── AC-1 · 9 ảnh · số dòng · tháng ────────────────────────────────────────────

@pytest.mark.parametrize("ten", TEN)
def test_AC1_anh_co_dung_so_dong_va_cong_dat(ten):
    anh = _anh(ten)
    assert anh["so_dong"] == len(anh["dong"]) == MONG[ten]
    assert anh["cong"]["dat"] is True, anh["cong"]
    assert anh["trung"] == [] and anh["khoa_hong"] == [] and anh["o_rong"] == []


@pytest.mark.parametrize("ten", TEN)
def test_AC1_checksum_dung_noi_dung(ten):
    anh = _anh(ten)
    assert anh["checksum_noi_dung"] == _checksum_lai(anh)
    assert CHECKSUM.get(ten) == anh["checksum_noi_dung"], f"ghim lại {ten}"


@pytest.mark.parametrize("ten", TEN)
def test_AC1_so_dong_theo_thang_khai_MONG(ten):
    anh = _anh(ten)
    dem = _theo_thang(anh["dong"], chi_co_khoa=ten.endswith("mid3"))
    assert dem == THANG_MONG[ten]
    assert sum(THANG_MONG[ten].values()) > 0                          # Đ3: mẫu số ≠ 0


def test_AC1_PS_thang_2026_khong_co_dong_nao_bay_thang_03_den_09():
    """AP: *"PS thiếu 03–09/2026"* ⇒ đo: 7/7 tháng `202603…202609` có 0 dòng ở MỌI ảnh PS
    *(và ở OMC · SC — AP ⛔ phân biệt PS)*; PS thiếu `202503` so với kỳ OMC."""
    thang_thieu = [f"2026{m:02d}" for m in range(3, 10)]
    assert len(thang_thieu) == 7
    for ten in TEN:
        co = {d["thang"] for d in _anh(ten)["dong"] if d.get("thang")}
        assert not (co & set(thang_thieu)), ten
        assert not any(t.startswith("2026") for t in co), ten
    ps = {d["thang"] for d in _anh("ps_mid1")["dong"]}
    assert sorted(set(_T10) - ps) == ["202503"]


@pytest.mark.parametrize("ten", TEN)
def test_AC1_cong_IN_ro_thang_thieu_va_mau_so(ten):
    ket = _khuon(ten).thieu_lac(_anh(ten)["dong"])
    assert ket["thieu"] == []
    assert "202603" in ket["dai"] and "7/7" in ket["dai"], ket["dai"]   # 7 tháng 03–09/2026 IN RÕ


# ── AC-2 · khoá + cột thượng nguồn ────────────────────────────────────────────

@pytest.mark.parametrize("ten", ["omc_mid3", "sc_mid3", "ps_mid3"])
def test_AC2_mid3_mang_khoa_vendor_va_thang(ten):
    anh = _anh(ten)
    assert "vendor" in anh["cot"] and "thang" in anh["cot"]
    co_khoa = [d for d in anh["dong"] if _chu(d["vendor"]) is not None]
    tong = [d for d in anh["dong"] if _chu(d["vendor"]) is None]
    assert len(tong) == MID3_TONG[ten] and len(co_khoa) + len(tong) == MONG[ten]
    assert all(re.fullmatch(r"VD[0-9]+", _chu(d["vendor"])) for d in co_khoa)
    assert all(re.fullmatch(r"20[0-9]{2}(0[1-9]|1[0-2])", d["thang"]) for d in co_khoa)


@pytest.mark.parametrize("ten", ["omc_mid1", "sc_mid1", "ps_mid1"])
def test_AC2_mid1_mang_cot_thuong_nguon_f_bang_T(ten):
    """MID1 `T` = `ArrayFormula(F)` *(F = `sumifs` Source (Looker) — ⛔ MID2/MID3, BG)*: ảnh mang
    `f` và `f == pe` trên MỌI hàng *(thượng nguồn đo được, ⛔ vòng tròn)*."""
    anh = _anh(ten)
    assert "f" in anh["cot"] and "pm" in anh["cot"] and "pm_ghi_chu" in anh["cot"]
    assert all(d["f"] == d["pe"] and d["f"] is not None for d in anh["dong"])


# ── AC-3 · cờ nguon_nghi_loi OMC ──────────────────────────────────────────────

@pytest.mark.parametrize("ten", ["omc_mid1", "omc_mid2", "omc_mid3"])
def test_AC3_omc_co_nguon_nghi_loi_kem_pham_vi(ten):
    ph = _anh(ten)["phu"]["nguon_nghi_loi"]["dong"]
    assert len(ph) == 1
    r = ph[0]
    assert _chu(r["ly_do"]) and "row[45]" in _chu(r["ly_do"])
    assert int(r["hang"]) == MONG[ten] and int(r["cot"]) > 0
    assert int(r["o"]) == int(r["hang"]) * int(r["cot"])


@pytest.mark.parametrize("ten", [t for t in TEN if not t.startswith("omc")])
def test_AC3_sc_ps_khong_co_co_nguon_nghi_loi(ten):
    assert "nguon_nghi_loi" not in _anh(ten).get("phu", {})


# ── AC-4 · lỗi ghi nguyên · đếm theo cột · PM chữ tách cột ghi chú ────────────

@pytest.mark.parametrize("ten", sorted(LOI))
def test_AC4_o_loi_ghi_nguyen_dem_theo_cot_va_loai(ten):
    def ngan(x):          # `#DIV/0! (Function …)` ⇒ `#DIV/0!` — gộp theo LOẠI lỗi
        return {c: {k.split(" (")[0]: n for k, n in v.items()} for c, v in x.items()}
    assert ngan(_anh(ten)["loi_theo_cot"]) == LOI[ten]
    assert ngan(_anh(ten)["loi_mong"]) == LOI[ten]


@pytest.mark.parametrize("ten", sorted(ITL_NA))
def test_AC4_itl_id_NA_ghi_nguyen_va_dem(ten):
    anh = _anh(ten)
    na = [d for d in anh["dong"] if (_chu(d["itl_id"]) or "").startswith("#N/A")]
    assert len(na) == ITL_NA[ten] == len(anh["phu"]["itl_id_loi"]["dong"])
    assert anh["phu"]["dem"]["dong"][0]["so_dong"] == str(DEM[ten])


@pytest.mark.parametrize("ten", sorted(PM_CHU))
def test_AC4_pm_chu_tach_sang_cot_ghi_chu_khong_hoa_0(ten):
    anh = _anh(ten)
    chu = [d for d in anh["dong"] if d["pm_ghi_chu"] is not None]
    assert len(chu) == PM_CHU[ten]
    assert {_chu(d["pm_ghi_chu"]) for d in chu} == {"Need to manual input"}
    assert all(d["pm"] is None for d in chu)                          # ⛔ hoá 0
    assert all(d["pm_ghi_chu"] is None for d in anh["dong"] if d["pm"] is not None)


@pytest.mark.parametrize("ten", ["omc_mid3", "sc_mid3", "ps_mid3"])
def test_AC4_mid3_sigma_chia_lech_ghi_nhan_dung_so_va_mau_so_ve(ten):
    anh = _anh(ten)
    assert len(anh["lac"]) == MID3_LECH_PE[ten]
    ket = _khuon(ten).thieu_lac(anh["dong"])
    assert f"PE: {MID3_PE_KHAC0[ten]}/" in ket["dai"] and "PM: 0/" in ket["dai"]
    assert "vế này chưa đo được" in ket["dai"]                        # vế PM 0 ô ≠ 0 — Đ3
    assert anh["phu"]["ngoai_anh"]["dong"][0]["so_dong"] == str(MID3_NGOAI[ten])


# ── Đ5 hai chiều · ca PHÁ ──────────────────────────────────────────────────────

@pytest.mark.parametrize("ten", TEN)
def test_PHA_tap_rong_thi_DO(ten):
    with pytest.raises(ValueError):
        _khuon(ten).thieu_lac([])


@pytest.mark.parametrize("ten", TEN)
def test_PHA_bot_mot_dong_thi_lech_thang_DO(ten):
    anh = _anh(ten)
    dong = anh["dong"][1:]                  # MID3: hàng đầu = tổng-tháng ⇒ `tong_lech`
    ket = _khuon(ten).thieu_lac(dong)
    assert any(x.startswith("thang_lech@") or x.startswith("tong_lech") for x in ket["thieu"]), ket["thieu"]


@pytest.mark.parametrize("ten", TEN)
def test_PHA_mot_thang_2026_lot_vao_thi_DO(ten):
    anh = _anh(ten)
    dong = [dict(d) for d in anh["dong"]]
    dong[-1]["thang"] = "202603"
    ket = _khuon(ten).thieu_lac(dong)
    assert any(x.startswith("thang_lech@") or x.startswith("thang_2026@") for x in ket["thieu"]), ket["thieu"]


@pytest.mark.parametrize("ten", TEN)
def test_PHA_vendor_la_thi_DO(ten):
    anh = _anh(ten)
    dong = [dict(d) for d in anh["dong"]]
    i = next(i for i, d in enumerate(dong) if _chu(d.get("vendor")) is not None)
    dong[i]["vendor"] = {"chu": "Nguyen Van A"}                        # tên người ⛔ lọt cột mã
    ket = _khuon(ten).thieu_lac(dong)
    assert any(x.startswith("vendor_la@") for x in ket["thieu"]), ket["thieu"]


@pytest.mark.parametrize("ten", ["omc_mid1", "sc_mid1", "ps_mid1"])
def test_PHA_f_khac_pe_thi_DO(ten):
    dong = [dict(d) for d in _anh(ten)["dong"]]
    dong[3]["f"] = "123456789"
    ket = _khuon(ten).thieu_lac(dong)
    assert any(x.startswith("f_khac_pe@") for x in ket["thieu"]), ket["thieu"]


@pytest.mark.parametrize("ten", ["omc_mid3", "sc_mid3", "ps_mid3"])
def test_PHA_doi_mot_o_chia_thi_lech_sigma_DO(ten):
    anh = _anh(ten)
    dong = [dict(d) for d in anh["dong"]]
    i = next(i for i, d in enumerate(dong) if d["pe"] is not None and d["cvl_pe"] is not None)
    dong[i]["cvl_pe"] = str(float(dong[i]["cvl_pe"]) + 1000)
    ket = _khuon(ten).thieu_lac(dong)
    assert any(x.startswith("sigma_lech") for x in ket["thieu"]), ket["thieu"]


# ── AC-5 · PII ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("ten", TEN)
def test_AC5_anh_0_cot_cam(ten):
    anh = _anh(ten)
    cot = {" ".join(c.split()).lower() for c in [anh["khoa"], *anh["cot"]]}
    assert not (cot & COT_CAM)
    cho_phep = {"dong_sheet", "currency", "cdt1", "thang", "no", "vendor", "itl_id", "pe", "u", "v",
                "f", "pm", "pm_ghi_chu", "rate", "cvl_pe", "cvl_pm", "cor_pe", "cor_pm", "shq1_pe",
                "shq1_pm", "csm_pe", "csm_pm", "cah_pe", "cah_pm", "asa_pe", "asa_pm"}
    assert cot <= cho_phep, cot - cho_phep


@pytest.mark.parametrize("ten,cot", [("omc_mid2", ["D", "J", "K", "M", "T", "AA", "U", "V"]),
                                     ("sc_mid2", ["D", "J", "K", "M", "T", "AA", "U", "V"]),
                                     ("ps_mid2", ["D", "J", "K", "M", "T", "AA", "U", "V"])])
def test_AC5_PII_co_ca_PHA_email_bi_tu_choi(ten, cot, tmp_path):
    bt = tmp_path / "tho.json"
    bt.write_text(json.dumps({"nguon": "x", "doc_luc": "2026-11-19", "cach_doc": "x",
                              "dong_dau_sheet": 10, "cot": [*cot, "Email Address"],
                              "values": [["USD", "CVL | VisionLab", 202504, "VD1", 1, 0.5, "", "",
                                          "ai@do.vn"]]}), encoding="utf-8")
    kq = subprocess.run([sys.executable, str(TOOL), ten, str(bt), "--mong", "1",
                         "--ra", str(tmp_path / "ra.json")], cwd=GOC, capture_output=True, text=True,
                        env=dict(os.environ, PYTHONUTF8="1"), timeout=120)
    assert kq.returncode == 2 and "PM_COT_RIENG_TU" in kq.stderr
    assert "ai@do.vn" not in kq.stderr                                 # lời lỗi ⛔ in giá trị ô


def test_AC5_vendor_chi_khop_mau_ma_khong_khop_ten():
    for ten in TEN:
        kh = _khuon(ten)
        assert kh.thieu_lac is not None
    import re as _re
    for ten in TEN:
        for d in _anh(ten)["dong"]:
            v = _chu(d.get("vendor"))
            assert v is None or _re.fullmatch(r"VD[0-9]+", v)


# ── AC-6 · khuôn = tệp riêng; ảnh cũ đúng từng byte ───────────────────────────

def test_AC6_chin_khuon_la_tep_rieng():
    for ten in TEN:
        assert (THU_MUC_KHUON / f"{ten}.py").is_file()


@pytest.mark.parametrize("ten", sorted(SHA_CU))
def test_AC6_anh_GI_cu_dung_tung_byte(ten):
    p = DAP_AN / f"{ten}.json"
    assert hashlib.sha256(p.read_bytes()).hexdigest()[:16] == SHA_CU[ten]
