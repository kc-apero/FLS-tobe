# -*- coding: utf-8 -*-
"""I1 (ISP 3.1.2 · Step 45 · `WO-303`) — HD1 xuyên suốt: công cụ đo → `voi_so_luong.json` →
`GET /gates` → F03. Mỗi tầng là CHÍNH mã thật, ⛔ tầng nào tự dựng envelope.

Ba tầng so cùng một thứ — *số kỳ đạt* và *danh sách kỳ đỏ*:
  ① công cụ  `tools/do_voi_so_luong.do()` chạy THẬT → ghi tệp tạm (⛔ chạm tệp đã commit);
  ② tuyến    `GET /gates` qua máy chủ thử, `tep_do` = tệp tạm ở ①;
  ③ màn      F03 — node-vm (`man_f03.js` thật) VÀ Chromium headless THẬT.

⭐ `I1-R1-01/02` (vòng sửa sau `KQ-305`, orchestrator quyết): cổng `HD1_THANG` phán MỌI kỳ có ảnh
  = **26** (`tu_sinh.so_ky_co_anh`); 23 kỳ `dat_hd1` ĐO ĐƯỢC đủ hai vế; 3 kỳ `2026-09·10·11` chỉ có ở
  `tu_sinh` (⛔ vế dòng ghép 1-1) ⇒ `khong_do_duoc` có tên vế. `da_do` = "x kỳ đạt / y kỳ đo được /
  26 kỳ có ảnh" ở CẢ ba tầng; `ly_do` mang TÊN nhãn DT1b (hoặc "chưa có nhãn DT1b" có tên tệp).
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import pytest

from fls.web.phuc_vu import lam_nguoi_phuc_vu  # noqa: F401  (đảm bảo gói web nạp được)
from tests.web import khung_node as kn
from tests.web.test_isp_f03_hd import (  # chỉ HÀM/HẰNG gạch dưới — ⛔ nhập bài `test_*`
    _TEN_FINAL, _TEN_HD1, _do_tran, _gates, _lop, _may, _the, _ve_f03, can_browser)

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
DT1A = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"
SO_LY_DO_THAT = GOC / "docs" / "ITL" / "_tools" / "so_ly_do_hd1.json"
TEP_THAT = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"

# ══ MONG — khai TRƯỚC (Đ5), mỗi số kèm NHÃN nó đếm gì (Đ4) ═══════════════════════════════════════
# Mốc sổ HAI LỚP (Đ4) — WO-345 (chủ 23/11: nguồn sống là chuẩn; `DT12-R1-05` đã quyết): 3 kỳ ảnh sống 23/11
# (2025-10 · 2026-03 · 2026-11 — nội dung đổi) · 23 kỳ đóng băng lại ra checksum ≡ ảnh 20/11.
# CŨ (trước WO-345): 25 kỳ "20/11 (sổ hiện tại)" · 2026-03 "mốc CŨ (ảnh chụp sổ cũ — chủ chưa quyết đóng băng lại)".
NHAN_MOC_MOI = "23/11 (nguồn sống — ảnh _20261123; chủ quyết nguồn sống là chuẩn)"
NHAN_MOC_CU = "23/11 ≡ 20/11 (đóng băng lại ra checksum BẰNG ảnh 20/11 — đọc ảnh 20/11)"
MONG_KY_MOC_MOI = ("2025-10", "2026-03", "2026-11")
MONG_SO_KY_CONG = 23            # kỳ của ẢNH sổ 26/08 — mẫu số `HD1_THANG` (khối `dat_hd1`)
MONG_SO_KY_TU_SINH = 26         # kỳ của manifest DT12 — khối `tu_sinh` (H15)
MONG_KY_CHI_O_TU_SINH = ("2026-09", "2026-10", "2026-11")
MONG_KY_DAT = ("2024-10", "2024-11", "2024-12", "2025-03", "2025-04")      # 5/23 kỳ đạt (sổ lý do RỖNG)
MONG_KY_DO = (                                                              # kỳ: số dòng sổ ⛔ ghép 1-1
    ("2025-01", 1), ("2025-02", 2), ("2025-05", 1), ("2025-06", 3), ("2025-07", 4),
    ("2025-08", 4), ("2025-09", 4), ("2025-10", 9), ("2025-11", 14), ("2025-12", 5),
    ("2026-01", 4), ("2026-02", 5), ("2026-03", 5), ("2026-04", 8), ("2026-05", 5),
    ("2026-06", 12), ("2026-07", 23), ("2026-08", 13),
)
MONG_NGAY_ANH = "2026-08-26"
# `tu_sinh` (H15, BG-288/KQ-290): ô Final khớp/tổng trên 26 kỳ · HD khớp/tổng · 8 kỳ lệch (92 ô)
# WO-345 (ảnh sống 23/11: 2026-11 659 → 748 dòng) — CŨ: O [88339, 88431] · HD [12633, 12633]
MONG_TU_SINH_O = [88962, 89054]
MONG_TU_SINH_HD = [12722, 12722]
MONG_TU_SINH_KY_LECH = ("2025-02", "2025-03", "2025-05", "2025-10", "2025-11", "2025-12", "2026-01", "2026-07")
# Chữ ký GIẢ — ⛔ chữ ký thật (O8 = chủ). Kỳ ký giả = 2026-07 (nhiều dòng thiếu nhất, 23/686).
KY_GIA = "2026-07"
NGUOI_KY_GIA = "TONG_HOP_TEST"
HOM_NAY = date(2026, 11, 22)
NGAY_KY = "2026-11-22"

_CAP_KY = re.compile(r"(\d{4}-\d{2}): (\d+)")      # `yyyy-mm: n` — ⛔ khớp ngày ảnh `2026-08-26`


# ── tầng ① ───────────────────────────────────────────────────────────────────────────────────
def _nap_tool():
    """Nạp công cụ MỘT BẢN RIÊNG (⛔ chung `MONG` giữa các bài — bài ký giả sửa `MONG` của bản mình)."""
    s = importlib.util.spec_from_file_location("_i1_do_voi_so_luong", GOC / "tools" / "do_voi_so_luong.py")
    m = importlib.util.module_from_spec(s)
    sys.modules[s.name] = m
    s.loader.exec_module(m)
    return m


def _van_tay(ds) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(sorted(ds), separators=(",", ":")).encode()).hexdigest()[:16]


def _do(tmp: Path, *, nhan: Path | None = None, so: Path | None = None, mong_ky: tuple | None = None) -> Path:
    """Chạy `do()` THẬT ⇒ ghi `tmp/voi_so_luong.json`. Trả đường dẫn tệp (cho `tep_do` của máy)."""
    dv = _nap_tool()
    if mong_ky is not None:
        dv.MONG["dat_hd1_theo_ky"] = mong_ky
    kq = dv.do(nhan=nhan or dv.NHAN, so_ly_do=so or dv.SO_LY_DO, hom_nay=HOM_NAY)
    p = tmp / "voi_so_luong.json"
    p.write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def _tang1(p: Path) -> dict:
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d["dat_hd1"]
    return {"so_dat": h["so_ky_dat"], "so_ky": h["mau_so"]["so_ky"], "ky_dat": tuple(h["ky_dat"]),
            "ky_do": tuple(sorted((k, v["thieu"]) for k, v in h["theo_ky"].items() if not v["dat"])),
            "d": d}


def _tang2(p: Path) -> tuple[dict, dict]:
    """`GET /gates` qua máy thật ⇒ (data, cổng HD1_THANG)."""
    with _may(str(p)) as (m, tok):
        data = _gates(m, tok)["data"]
    return data, {c["ma"]: c for c in data["cong"]}["HD1_THANG"]


def _doc_cong(g: dict) -> dict:
    """Bóc `da_do` + `ly_do` của cổng ⇒ (số đạt, số kỳ, các cặp kỳ đỏ)."""
    m = re.fullmatch(r"(\d+) kỳ đạt / (\d+) kỳ đo được / (\d+) kỳ có ảnh", g["da_do"])
    assert m, g["da_do"]
    return {"so_dat": int(m[1]), "so_ky": int(m[2]), "so_anh": int(m[3]), "ky_do": tuple(sorted((k, int(n)) for k, n in _CAP_KY.findall(g["ly_do"])))}


@pytest.fixture(scope="module")
def chuoi_that(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("i1_that")
    p = _do(tmp)
    data, g = _tang2(p)
    return {"p": p, "t1": _tang1(p), "data": data, "g": g}


# ═══ AC-1 · I1-B1 — ba tầng CÙNG số kỳ đạt + danh sách kỳ đỏ ═══════════════════════════════════
def test_B1_ba_tang_cung_so_ky_dat_va_danh_sach_ky_do(chuoi_that):
    t1, g = chuoi_that["t1"], chuoi_that["g"]
    # Đ3 — mẫu số KHÔNG rỗng, và mong khai TRƯỚC (⛔ so tầng với tầng trên tập rỗng)
    assert t1["so_ky"] == MONG_SO_KY_CONG and len(t1["ky_do"]) == len(MONG_KY_DO) == 18
    assert (t1["so_dat"], t1["ky_dat"]) == (5, MONG_KY_DAT)
    assert t1["ky_do"] == MONG_KY_DO
    c = _doc_cong(g)
    assert g["dat"] is False
    assert (c["so_dat"], c["so_ky"]) == (t1["so_dat"], t1["so_ky"]) == (5, 23)          # ① = ②
    assert c["so_anh"] == MONG_SO_KY_TU_SINH == len(t1["d"]["tu_sinh"]["theo_ky"])      # mẫu số = 26
    assert c["ky_do"] == t1["ky_do"]
    # Đ2 — nguồn THỨ HAI: tệp ĐÃ COMMIT (ảnh tĩnh) = lần đo sống ở ①
    that = json.loads(TEP_THAT.read_text(encoding="utf-8"))["dat_hd1"]
    assert (that["so_ky_dat"], tuple(that["ky_dat"])) == (t1["so_dat"], t1["ky_dat"])


def test_B1_nhan_ly_do_ngay_anh_va_nhan_moc_so_o_tang_cong_va_tang_tu_sinh(chuoi_that):
    g, d = chuoi_that["g"], chuoi_that["t1"]["d"]
    assert MONG_NGAY_ANH in g["ly_do"] and "kỳ đỏ 18/23" in g["ly_do"], g["ly_do"]
    assert "H15" in g["ly_do"], g["ly_do"]          # cổng NÓI nó ⛔ đo chế độ tự sinh
    moc = d["tu_sinh"]["moc_so"]
    assert len(moc) == MONG_SO_KY_TU_SINH
    assert tuple(k for k, v in moc.items() if v == NHAN_MOC_MOI) == MONG_KY_MOC_MOI
    assert sum(1 for v in moc.values() if v == NHAN_MOC_CU) == MONG_SO_KY_TU_SINH - len(MONG_KY_MOC_MOI)
    assert sum(v == NHAN_MOC_MOI for v in moc.values()) == 3          # WO-345 · CŨ: 25 kỳ "20/11 (sổ hiện tại)"


# ═══ I1-R1-01 — cổng phán 26 kỳ có ảnh; 3 kỳ ⛔ đo được vế dòng có TÊN ═══════════════════════════
def test_R1_01_cong_phan_26_ky_co_anh_ba_ky_moi_khong_do_duoc_ve_dong(chuoi_that):
    d, g = chuoi_that["t1"]["d"], chuoi_that["g"]
    ts = d["tu_sinh"]
    assert ts["so_ky_co_anh"] == len(ts["theo_ky"]) == MONG_SO_KY_TU_SINH and ts["chua_do"] == {}
    ky_cong, ky_ts = set(d["dat_hd1"]["theo_ky"]), set(ts["theo_ky"])
    assert len(ky_cong) == MONG_SO_KY_CONG and ky_cong < ky_ts
    assert tuple(sorted(ky_ts - ky_cong)) == MONG_KY_CHI_O_TU_SINH
    c = _doc_cong(g)
    assert (c["so_dat"], c["so_ky"], c["so_anh"]) == (5, MONG_SO_KY_CONG, MONG_SO_KY_TU_SINH)
    assert g["dat"] is False
    # ba kỳ mới được NÓI TÊN cùng vế ⛔ đo được (⛔ đạt, ⛔ bỏ im lặng)
    assert all(k in g["ly_do"] for k in MONG_KY_CHI_O_TU_SINH), g["ly_do"]
    assert "3/26 kỳ ⛔ đo được vế dòng ghép 1-1" in g["ly_do"], g["ly_do"]


def test_R1_02_ly_do_tep_nhan_vang_noi_chua_co_nhan_DT1b_co_ten_tep(chuoi_that):
    g = chuoi_that["g"]
    assert not re.search(r"TONG_HOP|KHONG_CO_SAO_KE|KHOA_LECH|TRUNG_SEQ|\bKHAC\b", g["ly_do"]), g["ly_do"]
    assert chuoi_that["t1"]["d"]["dat_hd1"]["tep_nhan"]["co"] is False          # DT1b chưa ghi tệp nhãn
    assert "chưa có nhãn DT1b (tệp nhãn docs/ITL/_tools/phan_loai_ly_do.json VẮNG)" in g["ly_do"], g["ly_do"]


def test_tu_sinh_26_ky_so_o_khop_MONG(chuoi_that):
    ts = chuoi_that["t1"]["d"]["tu_sinh"]
    assert (ts["tong"]["o"], ts["tong"]["hd"]) == (MONG_TU_SINH_O, MONG_TU_SINH_HD)
    lech = tuple(k for k, v in sorted(ts["theo_ky"].items()) if v["o"][0] != v["o"][1])
    assert lech == MONG_TU_SINH_KY_LECH
    assert sum(v["o"][1] - v["o"][0] for v in ts["theo_ky"].values()) == 92 == MONG_TU_SINH_O[1] - MONG_TU_SINH_O[0]


# ═══ AC-3 · I1-F1 — F03 (node-vm + Chromium THẬT) ghi đúng x/23 như cổng ═══════════════════════
@kn.can_node
def test_F1_vm_the_HD1_khop_cong_tung_chuoi(chuoi_that):
    g = chuoi_that["g"]
    ve = _ve_f03(chuoi_that["data"])
    hd1 = _the(ve, _TEN_HD1)
    assert "fail" in _lop(hd1) and "KHÔNG ĐẠT" in hd1["txt"], hd1
    assert g["da_do"] in hd1["txt"] and "5 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh" in hd1["txt"], hd1["txt"][:160]
    assert g["ly_do"] in hd1["txt"]                       # danh sách kỳ đỏ ĐẦY ĐỦ trên thẻ
    assert {k for k, _ in _CAP_KY.findall(hd1["txt"])} == {k for k, _ in MONG_KY_DO}


@can_browser
def test_F1_chromium_that_the_HD1_khop_cong(chuoi_that):
    g = chuoi_that["g"]
    with _may(str(chuoi_that["p"])) as (m, _tok):
        res = _do_tran("http://%s:%d/" % m.server_address, 390)
    hd1 = [x for x in res["gates"] if _TEN_HD1 in x["txt"]]
    assert len(hd1) == 1, [x["txt"][:40] for x in res["gates"]]          # đúng MỘT thẻ (Đ5)
    assert g["da_do"] in hd1[0]["txt"] and g["ly_do"] in hd1[0]["txt"], hd1[0]["txt"][:200]
    assert "fail" in hd1[0]["cls"].split() and "unk" not in hd1[0]["cls"].split()


# ═══ AC-2 · I1-B2 — tệp đo vắng ⇒ null (⛔ false, ⛔ true) ═════════════════════════════════════
def test_B2_tep_do_vang_hai_cong_null_dung_hop_dong_200(tmp_path, chuoi_that):
    vang = tmp_path / "khong-co.json"
    assert not vang.exists()
    data, _ = _tang2(vang)                      # `_gates` đòi 200 + vỏ `{data,error,meta}` — hợp đồng CG1
    g = {c["ma"]: c for c in data["cong"]}
    for ma in ("FINAL", "HD1_THANG"):
        assert g[ma]["dat"] is None, g[ma]      # ⛔ False, ⛔ True
        assert "tệp đo vắng" in g[ma]["ly_do"] and str(tmp_path) not in g[ma]["ly_do"], g[ma]["ly_do"]
    # Đ4: `chua_do_duoc` đếm CỔNG `dat=None` (gồm HD2 sau CG2) — ⛔ gõ tay 6; so với tệp THẬT: vắng ⇒ +2 đúng
    dat_none = sum(c["dat"] is None for c in data["cong"])
    assert data["chua_do_duoc"] == dat_none
    that = chuoi_that["data"]
    assert data["chua_do_duoc"] - that["chua_do_duoc"] == 2 and that["chua_do_duoc"] > 0   # Đ3: tập ⛔ rỗng


# ═══ AC-4 · I1-F2 — đường lỗi ⇒ thẻ "KHÔNG ĐO ĐƯỢC" (⛔ xanh, ⛔ trống) ════════════════════════
@kn.can_node
def test_F2_vm_tep_vang_hai_the_KHONG_DO_DUOC(tmp_path):
    data, _ = _tang2(tmp_path / "khong-co.json")
    ve = _ve_f03(data)
    for ten in (_TEN_FINAL, _TEN_HD1):
        c = _the(ve, ten)
        assert "unk" in _lop(c) and "pass" not in _lop(c) and "KHÔNG ĐO ĐƯỢC" in c["txt"], c


@can_browser
def test_F2_chromium_that_tep_vang_the_KHONG_DO_DUOC(tmp_path):
    with _may(str(tmp_path / "khong-co.json")) as (m, _tok):
        res = _do_tran("http://%s:%d/" % m.server_address, 390)
    for ten in (_TEN_FINAL, _TEN_HD1):
        c = [x for x in res["gates"] if ten in x["txt"]]
        assert len(c) == 1, ten
        cl = c[0]["cls"].split()
        assert "unk" in cl and "pass" not in cl and "KHÔNG ĐO ĐƯỢC" in c[0]["txt"], c[0]


# ═══ AC-5 — chữ ký GIẢ ⇒ kỳ xanh ở cả ba tầng; gỡ ⇒ đỏ lại ═════════════════════════════════════
def _gan_ca_loai(d: dict) -> dict[int, str]:
    """Nhãn TỔNG HỢP (⛔ nhãn DT1b thật): dòng thiếu 2026-07 → `TONG_HOP_A`; dòng thiếu khác →
    `TONG_HOP_B`; dòng tự-soi loại chưa có nhãn → `TONG_HOP_L`."""
    dt = json.loads(DT1A.read_text(encoding="utf-8"))
    gan = {x["dong_sheet"]: ("TONG_HOP_A" if x["ky"] == KY_GIA else "TONG_HOP_B") for x in dt["dong_thieu"]}
    for ds in d["dat_hd1"]["dong_tu_soi_loai"][KY_GIA]:
        gan.setdefault(ds, "TONG_HOP_L")
    return gan


def _ck(nhan: str, gan: dict) -> dict:
    ds = [x for x, n in gan.items() if n == nhan]
    return {"nhan": nhan, "so_dong": len(ds), "van_tay_dong": _van_tay(ds),
            "nguoi_ky": NGUOI_KY_GIA, "ngay": NGAY_KY}


@kn.can_node
def test_AC5_chu_ky_GIA_ky_2026_07_xanh_o_ca_ba_tang_go_chu_ky_thi_do_lai(chuoi_that, tmp_path):
    """⛔ chữ ký thật (O8): chỉ sống trong tệp TẠM của bài (`NGUOI_KY_GIA`); sổ lý do thật phải còn RỖNG."""
    gan = _gan_ca_loai(chuoi_that["t1"]["d"])
    nhan = tmp_path / "nhan.json"
    nhan.write_text(json.dumps({"van_tay": json.loads(DT1A.read_text(encoding="utf-8"))["van_tay"],
                                "dong_thieu": [{"dong_sheet": d, "nhan": n} for d, n in gan.items()]}),
                    encoding="utf-8")
    so = tmp_path / "so.json"
    so.write_text(json.dumps({"chu_ky": [_ck("TONG_HOP_A", gan), _ck("TONG_HOP_L", gan)]}), encoding="utf-8")
    ky_dat_ky = tuple(sorted(MONG_KY_DAT + (KY_GIA,)))
    ky_do_ky = tuple(x for x in MONG_KY_DO if x[0] != KY_GIA)

    # ── ký ⇒ xanh ở ba tầng ──
    p = _do(tmp_path, nhan=nhan, so=so, mong_ky=ky_dat_ky)
    t1 = _tang1(p)
    assert (t1["so_dat"], t1["ky_dat"], t1["ky_do"]) == (6, ky_dat_ky, ky_do_ky)             # ①
    data, g = _tang2(p)
    c = _doc_cong(g)
    assert (c["so_dat"], c["so_ky"], c["so_anh"], c["ky_do"]) == (6, 23, 26, ky_do_ky) and g["dat"] is False  # ②
    # I1-R1-02 (Đ3: nhãn CÓ trong đầu vào — tệp nhãn tmp): TÊN nhãn + số dòng vào `ly_do`, ở ②
    for ten in ("TONG_HOP_A", "TONG_HOP_B", "TONG_HOP_L"):
        assert ten in g["ly_do"], (ten, g["ly_do"])
    assert f"TONG_HOP_A {t1['d']['dat_hd1']['theo_nhan']['TONG_HOP_A']['so_dong']} dòng (đã ký)" in g["ly_do"]
    assert "chưa có nhãn DT1b" not in g["ly_do"]
    ve = _ve_f03(data)
    hd1 = _the(ve, _TEN_HD1)
    assert "6 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh" in hd1["txt"] and g["ly_do"] in hd1["txt"], hd1["txt"][:160]  # ③ vm
    assert "TONG_HOP_A" in hd1["txt"] and "TONG_HOP_B" in hd1["txt"]
    assert KY_GIA not in {k for k, _ in _CAP_KY.findall(hd1["txt"])}
    if not can_browser.args[0]:                                                                 # ③ Chromium
        with _may(str(p)) as (m, _tok):
            res = _do_tran("http://%s:%d/" % m.server_address, 390)
        h = [x for x in res["gates"] if _TEN_HD1 in x["txt"]]
        assert len(h) == 1 and "6 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh" in h[0]["txt"] \
            and "TONG_HOP_B" in h[0]["txt"] and KY_GIA not in {k for k, _ in _CAP_KY.findall(h[0]["txt"])}

    # ── gỡ chữ ký ⇒ đỏ lại ở ba tầng (đo tay: chữ ký chỉ là tệp tạm) ──
    so.write_text(json.dumps({"chu_ky": []}), encoding="utf-8")
    p2 = _do(tmp_path, nhan=nhan, so=so)
    t2 = _tang1(p2)
    assert (t2["so_dat"], t2["ky_dat"], t2["ky_do"]) == (5, MONG_KY_DAT, MONG_KY_DO)
    data2, g2 = _tang2(p2)
    c2 = _doc_cong(g2)
    assert (c2["so_dat"], c2["ky_do"]) == (5, MONG_KY_DO) and (KY_GIA, 23) in c2["ky_do"]
    assert "5 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh" in _the(_ve_f03(data2), _TEN_HD1)["txt"]
    # biên: sổ lý do THẬT còn RỖNG (⛔ chữ ký thật O8 ở repo)
    assert json.loads(SO_LY_DO_THAT.read_text(encoding="utf-8")).get("chu_ky") == []
    assert os.path.exists(os.fspath(TEP_THAT))
