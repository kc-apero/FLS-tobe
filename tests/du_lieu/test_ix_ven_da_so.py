# -*- coding: utf-8 -*-
"""`DT9b` *(ISP 3.1.2 · `WO-241`)* — IX.VEN = MỘT bảng có cột `so` *(`GI` · `OMC` · `SC` · `PS`)*.

Đầu vào cho cổng `WP-C4c` của H11 *(`BG-235` §2)*: engine `chia_theo_cach_tinh` cần 'cách tính'
của MỌI vendor ở MID3; trước DT9b IX.VEN chỉ chứa vendor GI.

⭐ Số đo *(Đ4 — mỗi số một nhãn; nguồn: `Vendor & Network Mapping` / `Vendor & Channel Mapping`
của ba sổ DT9, 19/11, Block 1 liền từ hàng 4)*:
  · DÒNG: GI **42** · OMC **89** *(R4:X92)* · SC **93** *(N4:T96)* · PS **135** *(M4:S138)* = **359**;
  · VENDOR khác nhau: OMC **21** · SC **10** · PS **53** — đúng tập vendor ở MID3 của từng sổ;
  · `cach_tinh` ở OMC: `VD341` 3 · `VD62` 2 · `VD428` 2 · `thường` 82; SC/PS: 100% `thường`.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
F = GOC / "tests" / "fixture"
ANH = F / "cau_hinh" / "ix_ven.json"
TOOL = GOC / "tools" / "dong_bang_sheet.py"

MONG_SO = {"GI": 42, "OMC": 89, "SC": 93, "PS": 135}
MONG_VENDOR = {"OMC": 21, "SC": 10, "PS": 53}
MONG_TONG = 359
CHECKSUM_MOI = "0f2d9287d332d698"          # ⭐ ghim ĐỔI CÓ CHỦ ĐÍCH (DT9b): ảnh thêm cột `so` + 317 dòng
#: sha256[:16] của JSON chuẩn *(sort_keys)* của 42 dòng GI TRƯỚC DT9b, ⛔ cột `so` — đo ở nền `06db9f9`.
SHA_GI_CU = "eb2b497da051e6f9"
NHAN_C9 = {"Max", "VD341", "VD428", "VD444", "VD62", "thường"}


def _doc():
    return json.loads(ANH.read_text(encoding="utf-8"))


def _chu(v):
    return v["chu"] if isinstance(v, dict) else v


def _so(r):
    return _chu(r["so"])


def test_anh_co_cot_so_va_dem_theo_so():
    a = _doc()
    assert a["bang"] == "IX.VEN" and a["so_dong"] == MONG_TONG == len(a["dong"])
    assert Counter(_so(r) for r in a["dong"]) == MONG_SO
    assert a["cong"]["dat"] is True and a["cong"]["mong"] == MONG_TONG, a["cong"]


def test_dong_GI_dung_tung_byte_chi_them_so():
    gi = [{k: v for k, v in r.items() if k != "so"} for r in _doc()["dong"] if _so(r) == "GI"]
    s = json.dumps(gi, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    assert len(gi) == 42
    assert hashlib.sha256(s.encode()).hexdigest()[:16] == SHA_GI_CU
    # khoá GI giữ NGUYÊN số hàng sheet *(⛔ tiền tố)*; sổ khác mang tiền tố `<SO>!`
    assert [r["dong_sheet"] for r in _doc()["dong"] if _so(r) == "GI"] == [str(i) for i in range(4, 46)]


def test_checksum_ghim_doi_co_chu_dich():
    a = _doc()
    assert a["checksum_noi_dung"] != "77f81455901c3667", "ảnh đã đổi ⇒ checksum cũ phải đổi"
    assert a["checksum_noi_dung"] == CHECKSUM_MOI


@pytest.mark.parametrize("so", ["OMC", "SC", "PS"])
def test_vendor_MID3_deu_co_dong_va_dung_so_vendor(so):
    m3 = json.loads((F / "dap_an" / f"{so.lower()}_mid3.json").read_text(encoding="utf-8"))["dong"]
    v3 = {_chu(r["vendor"]) for r in m3 if re.fullmatch(r"VD[0-9]+", str(_chu(r["vendor"])))}
    ven = {_chu(r["vendor"]) for r in _doc()["dong"] if _so(r) == so}
    assert len(v3) > 0, "Đ3: tập vendor MID3 ⛔ rỗng"
    assert v3 <= ven, f"{so}: vendor MID3 thiếu ở IX.VEN: {sorted(v3 - ven)}"
    assert len(ven) == MONG_VENDOR[so] == len(v3), (so, len(ven), len(v3))


def test_vendor_chi_la_ma_va_cach_tinh_dung_ma_C9():
    a = _doc()
    for r in a["dong"]:
        assert re.fullmatch(r"VD[0-9]+", _chu(r["vendor"])), "cột vendor chỉ MÃ"
        assert _chu(r["cach_tinh"]) in NHAN_C9
        assert _so(r) in MONG_SO
    omc = Counter(_chu(r["cach_tinh"]) for r in a["dong"] if _so(r) == "OMC")
    assert omc == {"VD341": 3, "VD62": 2, "VD428": 2, "thường": 82}, omc
    for so in ("SC", "PS"):
        assert {_chu(r["cach_tinh"]) for r in a["dong"] if _so(r) == so} == {"thường"}


def test_PII_sheet_moi_khong_mang_ten_tai_khoan():
    """Cột `account` của OMC/SC/PS ⛔ đọc *(tên người / số TK)*; `network` SC·PS ⛔ đọc *(cột tên)*."""
    a = _doc()
    for r in a["dong"]:
        if _so(r) != "GI":
            assert r["account"] is None, "account ⛔ đọc ở sổ mới"
            if _so(r) in ("SC", "PS"):
                assert r["network"] is None
    assert not [c for c in a["cot"] if "email" in c.lower()], a["cot"]


def test_khoa_dong_sheet_duy_nhat_va_khoa_nghiep_vu_theo_so():
    a = _doc()
    ds = [_chu(r["dong_sheet"]) for r in a["dong"]]
    assert len(set(ds)) == len(ds) == MONG_TONG
    k = Counter((_so(r), _chu(r["vendor"]), _chu(r["No"]) if isinstance(r["No"], dict) else r["No"])
                for r in a["dong"])
    assert max(k.values()) == 1, [x for x, n in k.items() if n > 1][:3]


def _lit(v) -> str:
    """Ô thô → literal JSON: số *(chuỗi chữ số)* ⇒ literal SỐ *(giữ đủ chữ số)*; chuỗi khác ⇒ chuỗi."""
    if v is None:
        return "null"
    if isinstance(v, int) and not isinstance(v, bool):
        return str(v)
    if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?([eE][+-]?\d+)?", v):
        return v
    return json.dumps(v, ensure_ascii=False)


def _tho_tu_anh(tmp: pathlib.Path, bo=lambda l: l) -> pathlib.Path:
    a = _doc()
    gi = [r for r in a["dong"] if _so(r) == "GI"]
    luoi = [[_chu(r["No"]), _chu(r["vendor"]), _chu(r["network"]), _chu(r["account"]), _chu(r["pct"]),
             _chu(r["cashin_month"]), _chu(r["cashin_day"]), _so(r),
             int(re.sub(r"^.*!", "", _chu(r["dong_sheet"])))] for r in a["dong"]]
    luoi = bo(luoi)
    tho = {"nguon": a["nguon"], "doc_luc": a["ngay_dong_bang"], "cach_doc": a["cach_doc"],
           "dong_dau_sheet": 4,
           "cot": ["No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day", "so", "hang"],
           "values": luoi}
    assert gi
    p = tmp / "tho.json"
    dong = ",\n  ".join("[" + ", ".join(_lit(x) for x in h) + "]" for h in luoi)
    p.write_text("{\n" + "".join(f' "{k}": {json.dumps(v, ensure_ascii=False)},\n' for k, v in tho.items()
                                  if k != "values") + f' "values": [\n  {dong}\n ]\n}}\n',
                 encoding="utf-8")
    return p


def _chay(tho, mong, ra):
    return subprocess.run([sys.executable, str(TOOL), "ix_ven", str(tho), "--mong", str(mong),
                           "--ra", str(ra)], cwd=GOC, capture_output=True, text=True,
                          env={**__import__("os").environ, "PYTHONUTF8": "1"}, timeout=180)


def test_anh_TAI_TAO_dung_tung_byte(tmp_path):
    kq = _chay(_tho_tu_anh(tmp_path), MONG_TONG, tmp_path / "ra.json")
    assert kq.returncode == 0, (kq.stdout[-800:], kq.stderr[-400:])
    assert (tmp_path / "ra.json").read_bytes() == ANH.read_bytes()


def test_PHA_bo_mot_dong_OMC_thi_DO(tmp_path):
    def bo(l):
        i = next(j for j, h in enumerate(l) if h[7] == "OMC")
        return l[:i] + l[i + 1:]
    kq = _chay(_tho_tu_anh(tmp_path, bo), MONG_TONG, tmp_path / "ra.json")
    assert kq.returncode == 1 and "≠ mong" in kq.stdout, (kq.stdout[-500:], kq.stderr[-300:])


def test_PHA_vendor_la_ten_nguoi_thi_TU_CHOI(tmp_path):
    def bo(l):
        h = next(h for h in l if h[7] == "PS")
        h[1] = "Nguyen Van A"
        return l
    kq = _chay(_tho_tu_anh(tmp_path, bo), MONG_TONG, tmp_path / "ra.json")
    assert kq.returncode != 0 and "Nguyen" not in (kq.stdout + kq.stderr), "⛔ in giá trị ô"


def test_PHA_so_la_thi_TU_CHOI(tmp_path):
    def bo(l):
        l[-1][7] = "XYZ"
        return l
    kq = _chay(_tho_tu_anh(tmp_path, bo), MONG_TONG, tmp_path / "ra.json")
    assert kq.returncode != 0


def test_PHA_doi_mot_nhan_cach_tinh_OMC_thi_cong_thieu_lac_DO(tmp_path):
    """Phá: OMC không còn VD428 ⇒ chỉ cắt dòng *(đếm lệch)*; vendor VD341→VD999 ở MỌI sổ ⇒ mất nhãn."""
    def bo(l):
        for h in l:
            if h[1] == "VD341":
                h[1] = "VD999"
        return l
    kq = _chay(_tho_tu_anh(tmp_path, bo), MONG_TONG, tmp_path / "ra.json")
    assert kq.returncode == 1 and "VD341" in kq.stdout, (kq.stdout[-500:],)
