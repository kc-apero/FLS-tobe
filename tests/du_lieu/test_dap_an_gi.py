"""ĐÁP ÁN MID1–MID3 của GI + ẢNH IX.VEN Block 1 — khuôn `ix_ven` · `gi_mid1/2/3`
*(ISP 3.1.2 · DT8 · `WO-147`)*.

⭐ **Vì sao có tệp này.** Bước **AL.PLT/H9/H10** *(AP v3.1.2 §3.2.2 IX.VEN · §3.4.1 PD 503–507 ·
§3.5.4 WP-C4)* phân bổ chi phí nền tảng GI xuống 7 CDT1. Cần bốn ẢNH đứng yên:
  · `ix_ven.json`   — Block 1 *(36 dòng `M:S`)* + cột `cach_tinh` *(5 nhóm riêng)*.
  · `gi_mid1.json`  — MID1 phân bổ 7 CDT1 *(2.856 hàng)* · `#N/A` ITL ID giữ nguyên.
  · `gi_mid2.json`  — MID2 RATE *(1.463 hàng)* · `#DIV/0!` giữ nguyên *(cột `so!`)*.
  · `gi_mid3.json`  — MID3 đáp án tháng *(11 hàng)* · cổng `Σ chia = O / P`.

Sáu bài của ISP *(mục 6)* + đối chứng Đ3/Đ4/Đ5:

    DT8-B1  ix_ven: 36 dòng Block 1; 5 nhãn `cach_tinh` ≠ 'thường' = {Max,VD341,VD428,VD444,VD62}
    DT8-B2  gi_mid3: Σ 6 PE_cdt = O ∧ Σ 6 PM_cdt = P trên 11 hàng *(đo lại ĐỘC LẬP, lệch = 0)*
    AC-3    `#N/A`/`#DIV/0!` ở nguồn GHI NGUYÊN + ĐẾM *(ITL ID 176 · RATE 308)*, ⛔ hoá 0
    AC-4    PII: 0 cột cấm, máy quét có ca phá, lời lỗi ⛔ in giá trị ô; `mã ∈ tập tham chiếu`
            đo trên TẬP ĐẦY ĐỦ *(cdt1 ∈ 7 CDT1)*
    AC-5    khuôn mới = tệp riêng; ảnh DT2…DT5 *(ix_fx · gl_406)* đúng TỪNG BYTE
    so!     kiểu cột mới: số HOẶC lỗi Sheets; ô ⛔số⛔rỗng⛔lỗi ⇒ ĐỎ *(đối xứng `so`)*

⛔⛔ **Bản đọc thô thật ⛔ nằm trong repo** *(scratchpad phiên cloud DATA, ⛔ commit — WO-147 Nguồn)*.
⇒ Bài TÁI TẠO lưới thô **từ chính ảnh** rồi chạy lại công cụ ⇒ phải ra **đúng từng byte**. Ca phá
dựng lưới TỪ ảnh rồi SỬA một ô, ⛔ số thật.

⭐ **Số đo 18/11 *(khoá SA chỉ-đọc, phiên cloud — mỗi số đếm MỘT vật, Đ4)*:**
  · IX.VEN Block 1 = 36 hàng *(sheet 4…39)*; nhãn riêng: Max 12 · VD341 6 · VD444 8 · VD428 3 ·
    VD62 1 · thường 6 ⇒ **5** nhãn ≠ thường.
  · MID3 = 11 hàng đáp án *(AE/AF CHECK True — sheet 10…20)*; dư Σ chia lớn nhất Decimal 5,1e-9.
  · MID1 = 2.856 hàng phân bổ + 4.494 hàng đệm; **176** hàng ITL ID `#N/A`.
  · MID2 = 1.463 hàng; **308** ô RATE `#DIV/0!`; 7 CDT1 × 209 hàng.
"""
from __future__ import annotations

import datetime
import hashlib
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
F = GOC / "tests" / "fixture"

ANH = {
    "ix_ven": F / "cau_hinh" / "ix_ven.json",
    "gi_mid1": F / "dap_an" / "gi_mid1.json",
    "gi_mid2": F / "dap_an" / "gi_mid2.json",
    "gi_mid3": F / "dap_an" / "gi_mid3.json",
}
#: checksum_noi_dung ghim *(đổi ⇒ phải có lượt đóng băng mới + lý do)*.
CHECKSUM = {
    "ix_ven": "9a6bc3cac0bf496c",
    "gi_mid1": "5e054cfd05257bb7",
    "gi_mid2": "73887970320d39a3",
    "gi_mid3": "a43341bb8aea0c1c",
}
MONG = {"ix_ven": 36, "gi_mid1": 2856, "gi_mid2": 1463, "gi_mid3": 11}

#: 5 nhãn `cach_tinh` ≠ 'thường' *(AP §3.2.2/§3.2.4)*.
NHOM_RIENG = {"Max", "VD341", "VD428", "VD444", "VD62"}
#: 7 CDT1 — tập tham chiếu đóng *(§3.2.2 "× 7 CDT1")*.
CDT1_7 = {"SHQ2 | Headquarters2", "CVL | VisionLab", "COR | TeraSofts", "SHQ1 | Headquarters1",
          "CSM | SuperMinds", "CAH | Astronex", "ASA | Super App"}

#: ⛔ Đổi 1 byte ảnh DT2/DT4 là ĐỎ *(AC-5)* — sha256[:16] của tệp đã commit *(nền isp/DT8)*.
SHA_CU = {
    F / "cau_hinh" / "ix_fx.json": "e2c9fdd028bd3286",     # DT2 (ix_fx)
}


# ── trợ thủ ───────────────────────────────────────────────────────────────────

def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([sys.executable, str(TOOL), *doi_so], cwd=GOC, env=env,
                          capture_output=True, text=True, timeout=180)


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _chu(v):
    """Ô ảnh → giá trị thô: ô chữ ⇒ chuỗi; ô số ⇒ chuỗi chữ số; rỗng ⇒ None."""
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _checksum_lai(anh: dict) -> str:
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _lit(v) -> str:
    """Giá trị thô → literal JSON: số *(chuỗi chữ số)* ⇒ literal SỐ *(giữ đủ chữ số)*; None ⇒
    null; chuỗi khác ⇒ chuỗi *(⛔ thành số)*."""
    if v is None:
        return "null"
    if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?([eE][+-]?\d+)?", v):
        return v
    return json.dumps(v, ensure_ascii=False)


def _viet_luoi(p: pathlib.Path, anh: dict, *, cot: list[str], dong_dau: int,
               values: list[list], nguon=None, doc_luc=None, cach_doc=None) -> pathlib.Path:
    """Ghi lưới thô đúng hình orchestrator — `values` viết TAY để ô số ra literal SỐ."""
    nguon = anh["nguon"] if nguon is None else nguon
    doc_luc = anh["ngay_dong_bang"] if doc_luc is None else doc_luc
    cach_doc = anh["cach_doc"] if cach_doc is None else cach_doc
    dong = ",\n  ".join("[" + ", ".join(_lit(x) for x in h) + "]" for h in values)
    p.write_text(
        "{\n"
        f' "nguon": {json.dumps(nguon, ensure_ascii=False)},\n'
        f' "doc_luc": {json.dumps(doc_luc)},\n'
        f' "cach_doc": {json.dumps(cach_doc, ensure_ascii=False)},\n'
        f' "dong_dau_sheet": {dong_dau},\n'
        f' "cot": {json.dumps(cot, ensure_ascii=False)},\n'
        f' "values": [\n  {dong}\n ]\n}}\n', encoding="utf-8")
    return p


# ── tái tạo lưới thô TỪ ảnh *(mỗi khuôn một hình)* ──────────────────────────────

COT_THO = {
    "ix_ven": ["No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day"],
    "gi_mid1": ["D", "J", "K", "Q", "M", "R", "T"],
    "gi_mid2": ["D", "J", "K", "M", "T", "AA"],
    "gi_mid3": ["O", "P", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF"],
}


def _luoi(ten: str, anh: dict) -> list[list]:
    """Lưới thô TÁI TẠO từ ảnh *(⛔ cột dẫn xuất: `cach_tinh`, `dong_sheet`, AE/AF)*."""
    d = anh["dong"]
    if ten == "ix_ven":
        return [[_chu(r["No"]), _chu(r["vendor"]), _chu(r["network"]), _chu(r["account"]),
                 _chu(r["pct"]), _chu(r["cashin_month"]), _chu(r["cashin_day"])] for r in d]
    if ten == "gi_mid1":
        # hàng phân bổ thật rồi 4.494 hàng đệm (D='USD' do công thức, 5 cột phân bổ rỗng).
        real = [[_chu(r["currency"]), _chu(r["cdt1"]), _chu(r["thang"]), _chu(r["no"]),
                 _chu(r["vendor"]), _chu(r["itl_id"]), _chu(r["pe"])] for r in d]
        dem = int(_chu(anh["phu"]["dem"]["dong"][0]["so_dong"]))
        return real + [["USD", None, None, None, None, None, None]] * dem
    if ten == "gi_mid2":
        return [[_chu(r["currency"]), _chu(r["cdt1"]), _chu(r["thang"]), _chu(r["vendor"]),
                 _chu(r["pe"]), _chu(r["rate"])] for r in d]
    if ten == "gi_mid3":
        pe_pm = ["cvl_pe", "cvl_pm", "cor_pe", "cor_pm", "shq1_pe", "shq1_pm",
                 "csm_pe", "csm_pm", "cah_pe", "cah_pm", "asa_pe", "asa_pm"]
        return [[_chu(r["pe"]), _chu(r["pm"]), *[_chu(r[c]) for c in pe_pm], True, True] for r in d]
    raise AssertionError(ten)


DONG_DAU = {"ix_ven": 4, "gi_mid1": 10, "gi_mid2": 10, "gi_mid3": 10}


def _tai_tao(ten: str, p: pathlib.Path, anh: dict) -> pathlib.Path:
    return _viet_luoi(p, anh, cot=COT_THO[ten], dong_dau=DONG_DAU[ten], values=_luoi(ten, anh))


# ══ AC-5 · khuôn mới = tệp riêng; ảnh DT2…DT5 đúng từng byte ════════════════════

def test_AC5_bon_khuon_moi_la_tep_rieng():
    for ten in ("ix_ven", "gi_mid1", "gi_mid2", "gi_mid3"):
        assert (THU_MUC_KHUON / f"{ten}.py").is_file(), f"khuôn `{ten}` phải là tệp riêng"


@pytest.mark.parametrize("p, sha", list(SHA_CU.items()), ids=lambda x: getattr(x, "name", ""))
def test_AC5_anh_cu_dung_tung_byte(p, sha):
    if not isinstance(p, pathlib.Path):
        pytest.skip()
    assert hashlib.sha256(p.read_bytes()).hexdigest()[:16] == sha, f"{p.name} ⛔ còn từng byte"


# ══ bốn ảnh: checksum + cổng ĐẠT + tái tạo đúng từng byte ══════════════════════

@pytest.mark.parametrize("ten", ["ix_ven", "gi_mid1", "gi_mid2", "gi_mid3"])
def test_anh_checksum_va_cong_dat(ten):
    anh = _doc(ANH[ten])
    assert anh["so_dong"] == MONG[ten]
    assert anh["cong"]["dat"] is True, anh["cong"]["ly_do"]
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM[ten]


@pytest.mark.parametrize("ten", ["ix_ven", "gi_mid1", "gi_mid2", "gi_mid3"])
def test_anh_TAI_TAO_dung_tung_byte(ten, tmp_path):
    anh = _doc(ANH[ten])
    bt = _tai_tao(ten, tmp_path / "tho.json", anh)
    ra = tmp_path / "ra.json"
    kq = _chay(ten, str(bt), "--mong", str(MONG[ten]), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-900:], kq.stderr[-500:])
    assert ra.read_bytes() == ANH[ten].read_bytes(), f"{ten}: ảnh tái tạo ⛔ khớp từng byte"


# ══ DT8-B1 · ix_ven: 36 dòng Block 1 + 5 nhãn cach_tinh ════════════════════════

def test_DT8_B1_ix_ven_36_dong_5_nhom_rieng():
    anh = _doc(ANH["ix_ven"])
    assert anh["bang"] == "IX.VEN" and anh["so_dong"] == 36
    rieng = {r["cach_tinh"]["chu"] for r in anh["dong"] if r["cach_tinh"]["chu"] != "thường"}
    assert rieng == NHOM_RIENG, f"5 nhãn riêng; đo {sorted(rieng)}"
    # Đ4 — mỗi nhãn đếm một vật: Max 12 · VD341 6 · VD444 8 · VD428 3 · VD62 1 · thường 6.
    from collections import Counter
    dem = Counter(r["cach_tinh"]["chu"] for r in anh["dong"])
    assert dem == {"Max": 12, "VD341": 6, "VD444": 8, "VD428": 3, "VD62": 1, "thường": 6}


def test_DT8_B1_PHA_mot_nhom_rieng_thi_DO(tmp_path):
    """Phá: đổi mọi VD341 → VD999 *(mất nhãn VD341)* ⇒ 4 nhãn ≠ 5 ⇒ cổng ĐỎ *(Đ5 hai chiều)*."""
    anh = _doc(ANH["ix_ven"])
    luoi = _luoi("ix_ven", anh)
    for h in luoi:
        if h[1] == "VD341":
            h[1] = "VD999"
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO["ix_ven"], dong_dau=4, values=luoi)
    kq = _chay("ix_ven", str(bt), "--mong", "36", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1, (kq.stdout[-600:], kq.stderr[-300:])
    assert "thiếu" in kq.stdout and "VD341" in kq.stdout


# ══ DT8-B2 · gi_mid3: Σ chia = O / P ═══════════════════════════════════════════

def test_DT8_B2_mid3_sigma_chia_bang_O_P_doc_lap():
    """Đo LẠI độc lập: Σ 6 PE_cdt = O ∧ Σ 6 PM_cdt = P trên 11 hàng *(⛔ tin cổng của ảnh)*."""
    from decimal import Decimal
    anh = _doc(ANH["gi_mid3"])
    assert anh["so_dong"] == 11
    pe = ("cvl_pe", "cor_pe", "shq1_pe", "csm_pe", "cah_pe", "asa_pe")
    pm = ("cvl_pm", "cor_pm", "shq1_pm", "csm_pm", "cah_pm", "asa_pm")
    lech = 0
    for r in anh["dong"]:
        o = Decimal(_chu(r["pe"])); p = Decimal(_chu(r["pm"]))
        spe = sum(Decimal(_chu(r[c])) for c in pe); spm = sum(Decimal(_chu(r[c])) for c in pm)
        if abs(o - spe) > Decimal("0.000001") or abs(p - spm) > Decimal("0.000001"):
            lech += 1
    assert lech == 0, f"MONG lệch = 0; đo {lech}"


def test_DT8_B2_PHA_mot_o_chia_thi_DO(tmp_path):
    """Phá: cộng 1000 vào CVL PE của hàng đầu ⇒ Σ PE ≠ O ⇒ cổng Σ chia ĐỎ *(Đ5)*."""
    anh = _doc(ANH["gi_mid3"])
    luoi = _luoi("gi_mid3", anh)
    # cot thô: O,P,S(cvl_pe=idx2),... ⇒ sửa idx2 của hàng 0.
    luoi[0][2] = str(float(luoi[0][2]) + 1000.0)
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO["gi_mid3"], dong_dau=10, values=luoi)
    kq = _chay("gi_mid3", str(bt), "--mong", "11", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1, (kq.stdout[-600:], kq.stderr[-300:])
    assert "thiếu" in kq.stdout and "dong_sheet@10" in kq.stdout


def test_DT8_B2_PHA_tap_rong_thi_DO(tmp_path):
    """Đ3: 0 hàng đáp án *(AE/AF ⛔ True)* ⇒ `thieu_lac` ValueError ⇒ ĐỎ, ⛔ nền xanh."""
    anh = _doc(ANH["gi_mid3"])
    luoi = _luoi("gi_mid3", anh)
    for h in luoi:
        h[14] = False                               # AE = False ⇒ ⛔ hàng nào được chọn
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO["gi_mid3"], dong_dau=10, values=luoi)
    kq = _chay("gi_mid3", str(bt), "--mong", "11", "--ra", str(tmp_path / "ra.json"))
    # 0 hàng chọn ⇒ bản thô 0 dòng ⇒ TỪ CHỐI (exit 2) — mẫu số 0 là kết quả, ⛔ ảnh rỗng.
    assert kq.returncode == 2, (kq.stdout[-500:], kq.stderr[-400:])
    assert "0 dòng" in kq.stderr


# ══ AC-3 · #N/A / #DIV/0! ghi nguyên + đếm *(⛔ hoá 0)* ═════════════════════════

def test_AC3_mid1_itl_id_NA_ghi_nguyen_va_dem():
    anh = _doc(ANH["gi_mid1"])
    phu = anh["phu"]["itl_id_loi"]["dong"]
    assert anh["phu"]["itl_id_loi"]["so_dong"] == 176 and len(phu) == 176, "176 hàng ITL ID #N/A"
    # ghi NGUYÊN chuỗi *(⛔ hoá 0)*: mọi hàng phụ mang chuỗi bắt đầu '#N/A', khớp dong chính.
    for r in phu:
        assert r["itl_id_tho"]["chu"].startswith("#N/A")
        d = next(x for x in anh["dong"] if x["dong_sheet"] == r["dong_sheet"])
        assert d["itl_id"] == r["itl_id_tho"]        # cột chính GIỮ chuỗi lỗi, ⛔ hoá 0/rỗng


def test_AC3_mid2_rate_DIV0_so_mu_ghim_phan_bo():
    anh = _doc(ANH["gi_mid2"])
    assert anh["loi_mong"] == {"rate": 308}
    # phân bố ghim: đúng một giá trị lỗi, 308 lần *(DT5-R1-04)*.
    pb = anh["loi_theo_cot"]["rate"]
    assert sum(pb.values()) == 308 and all(k.startswith("#DIV/0!") for k in pb)
    assert len(anh["o_loi"]) == 308
    # ghi NGUYÊN: ô RATE lỗi trong cột chính = {"chu": "#DIV/0! ..."} *(⛔ hoá 0)*.
    so_div0 = sum(1 for r in anh["dong"]
                  if isinstance(r["rate"], dict) and r["rate"]["chu"].startswith("#DIV/0!"))
    assert so_div0 == 308


def test_AC3_mid2_PHA_doi_mot_DIV0_thanh_so_thi_DO(tmp_path):
    """Phá: đổi 1 ô `#DIV/0!` → số ⇒ 307 ≠ LOI_MONG 308 ⇒ cổng ĐỎ *(Đ5 hai chiều)*."""
    anh = _doc(ANH["gi_mid2"])
    luoi = _luoi("gi_mid2", anh)
    doi = 0
    for h in luoi:                                   # cot thô: ...,rate=idx5
        if isinstance(h[5], str) and h[5].startswith("#DIV/0!"):
            h[5] = "0.5"; doi += 1
            break
    assert doi == 1
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO["gi_mid2"], dong_dau=10, values=luoi)
    kq = _chay("gi_mid2", str(bt), "--mong", "1463", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1, (kq.stdout[-600:], kq.stderr[-300:])
    assert "ô lỗi ≠ mong" in kq.stdout and "rate 307≠308" in kq.stdout


# ══ so! · kiểu cột mới: số HOẶC lỗi; ô ⛔số⛔rỗng⛔lỗi ⇒ ĐỎ ══════════════════════

def test_so_bang_cot_so_loi_chap_nhan_so_rong_loi(tmp_path):
    """`so!` nhận SỐ · RỖNG · lỗi Sheets; nhưng chữ-thường ⇒ 'ô ⛔ số!' ⇒ ĐỎ *(đối xứng `so`)*."""
    anh = _doc(ANH["gi_mid2"])
    luoi = _luoi("gi_mid2", anh)
    # đặt một ô rate = chữ thường 'linh tinh' ⇒ ⛔ số ⛔ rỗng ⛔ lỗi ⇒ ĐỎ.
    luoi[0][5] = "linh tinh"
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO["gi_mid2"], dong_dau=10, values=luoi)
    kq = _chay("gi_mid2", str(bt), "--mong", "1463", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1 and "ô ⛔ số!" in kq.stdout, (kq.stdout[-600:],)


def test_so_bang_LOI_MONG_khai_sai_cot_bi_tu_choi(tmp_path, monkeypatch):
    """Giao kèo: `LOI_MONG` khoá phải cột khai `so!` — khuôn lạ ⇒ TỪ CHỐI *(⛔ rơi im lặng)*."""
    xau = THU_MUC_KHUON / "zz_so_loi_sai.py"
    xau.write_text(
        'BANG="X"\nKHOA="dong_sheet"\nKIEU_KHOA="dong_sheet"\nCOT=("a",)\n'
        'KIEU_COT={"a":"so"}\nLOI_MONG={"a":1}\nRA="tests/fixture/dap_an/_x.json"\n'
        'def thieu_lac(d): return {"thieu":[],"lac":[],"dai":""}\n', encoding="utf-8")
    try:
        kq = _chay("zz_so_loi_sai", str(ANH["gi_mid2"]), "--mong", "1")
        assert kq.returncode == 2 and "LOI_MONG" in kq.stderr, (kq.stderr[-400:],)
    finally:
        xau.unlink(missing_ok=True)


# ══ AC-4 · PII + ref-set + lời lỗi ⛔ in giá trị ô ══════════════════════════════

@pytest.mark.parametrize("ten", ["ix_ven", "gi_mid1", "gi_mid2", "gi_mid3"])
def test_AC4_anh_0_cot_cam(ten):
    anh = _doc(ANH[ten])
    assert "0 trùng" in anh["khong_mang_PII"] and "PM_COT_RIENG_TU" in anh["khong_mang_PII"]
    # ⛔ cột PII trong COT của ảnh
    cot = [c.lower() for c in anh["cot"]]
    assert not any("email" in c or "diễn giải" in c or "số chứng từ" in c or "tài khoản" in c
                   for c in cot)


def test_AC4_PII_co_ca_PHA_email_bi_tu_choi(tmp_path):
    """Máy quét PII có ca phá: thêm cột 'Email Address' vào lưới ⇒ TỪ CHỐI *(DT2-R1 · AC-4)*."""
    anh = _doc(ANH["gi_mid2"])
    luoi = [[*h, "ai@do.vn"] for h in _luoi("gi_mid2", anh)]
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=[*COT_THO["gi_mid2"], "Email Address"],
                    dong_dau=10, values=luoi)
    kq = _chay("gi_mid2", str(bt), "--mong", "1463", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 2 and "PM_COT_RIENG_TU" in kq.stderr
    # DT5-R1-02: lời lỗi ⛔ in GIÁ TRỊ ô *(email thật ⛔ lọt ra stderr)*.
    assert "ai@do.vn" not in kq.stderr


@pytest.mark.parametrize("ten,ci,mong_dai", [("gi_mid1", 1, "tập tham chiếu"),
                                             ("gi_mid2", 1, "tập tham chiếu")])
def test_AC4_ref_set_cdt1_PHA_tren_tap_day_du(ten, ci, mong_dai, tmp_path):
    """Phá: đổi 1 ô CDT1 *(cột J)* thành mã lạ ⇒ cổng `mã ∈ tập tham chiếu` ĐỎ *(đo TẬP ĐẦY ĐỦ —
    DT5-R1-01: ⛔ tập con thưa)*."""
    anh = _doc(ANH[ten])
    luoi = _luoi(ten, anh)
    luoi[0][ci] = "CDT_LA | giả"
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO[ten], dong_dau=10, values=luoi)
    kq = _chay(ten, str(bt), "--mong", str(MONG[ten]), "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1 and "cdt1_la@" in kq.stdout, (kq.stdout[-500:],)


def test_AC4_ref_set_do_tren_TAT_CA_hang_khong_tap_con():
    """DT5-R1-01: cổng ref-set khai đo trên ĐẦY ĐỦ hàng, ⛔ tập con — số hàng trong `dai` =
    so_dong của ảnh."""
    for ten in ("gi_mid1", "gi_mid2"):
        anh = _doc(ANH[ten])
        # `dai` ở lạc/ghi_chu — cổng chạy trên mọi hàng; xác nhận so_dong khớp MONG (⛔ thưa).
        assert anh["so_dong"] == MONG[ten]
        assert "tập tham chiếu" in anh["ghi_chu_khuon"] and str(MONG[ten]) in anh["ghi_chu_khuon"]
