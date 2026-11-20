"""ẢNH MANUAL INPUT của `ITL Ledge` — các kỳ NGOÀI 2026-03 *(ISP 3.1.2 · Step 38 · DT12 · `WO-265`)*.

⭐ **Vì sao.** Chế độ TỰ SINH *(H15 → I1)* so MID/Final FLS tự tính với MID/Final của sổ ADJUSTED, kỳ nào có
cột `Manual input`. Trước bước này mới có MỘT kỳ *(`tests/fixture/itl_ledge_2026_03.json`, 584 dòng)*.

Số đo 20/11 *(khoá SA chỉ-đọc; mỗi số đếm MỘT vật — Đ4)*:
  · sổ `ITL I Input Transaction Ledger File 2/2 (ADJUSTED)` · tab `ITL Ledge` *(lưới 12.684 × 69)*;
  · **12.633** hàng dữ liệu có NGÀY ở cột A *(hàng `10…12642`, 0 hàng có chữ ở A)* thuộc **26 kỳ**
    `2024-10 … 2026-11` — ⛔ phải 23 như ISP *(22 + 2026-03)*: 3 kỳ `2024-10/11/12` *(15 hàng lạc)* ở đầu sổ;
  · bỏ 2026-03 *(ảnh có sẵn, ⛔ đụng)* ⇒ **25** kỳ · **12.049** dòng.
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
F = GOC / "tests" / "fixture"
DAP_AN = F / "dap_an"
TOOL = GOC / "tools" / "dong_bang_sheet.py"
KHUON = GOC / "tools" / "khuon_dong_bang" / "itl_ledge_ky.py"
ANH_03 = F / "itl_ledge_2026_03.json"
MANIFEST = DAP_AN / "itl_ledge_cac_ky.json"

#: ⭐ Đ5 — phân bố kỳ ĐẾM ĐỘC LẬP trên cột A *(ngày)* của sổ, ⛔ qua khuôn; số dòng mỗi kỳ.
MONG = {"2024-10": 6, "2024-11": 3, "2024-12": 6, "2025-01": 748, "2025-02": 283, "2025-03": 297,
        "2025-04": 332, "2025-05": 408, "2025-06": 348, "2025-07": 546, "2025-08": 537, "2025-09": 501,
        "2025-10": 487, "2025-11": 477, "2025-12": 566, "2026-01": 471, "2026-02": 439, "2026-04": 600,
        "2026-05": 537, "2026-06": 613, "2026-07": 686, "2026-08": 724, "2026-09": 737, "2026-10": 1038,
        "2026-11": 659}
#: Đ5 — ô `itl_id` = `#N/A ()` *(hàng chưa gán ITL ID)* mỗi kỳ, ĐẾM ĐỘC LẬP ở cột `R` bản thô *(đo 20/11)*; kỳ ⛔ ghi = 0.
ITL_ID_LOI = {'2025-11': 2, '2026-02': 1, '2026-04': 1, '2026-05': 1, '2026-06': 2, '2026-07': 3, '2026-09': 35, '2026-10': 47, '2026-11': 27}
#: checksum_noi_dung ghim — đổi ⇒ phải có lượt đóng băng mới + lý do.
CHECKSUM = {'2024-10': '42be93a5618d36f4', '2024-11': 'cb1eb227df517d0b', '2024-12': 'cc171dd3f506982d', '2025-01': '888e3fa40bd2c195', '2025-02': 'a4268fc55c80dbcd', '2025-03': '211e71d545a9b867', '2025-04': '563eab98883aa1a5', '2025-05': 'b8e94ba589572282', '2025-06': '9113d66b3bb512f8', '2025-07': '4b73312b2cdfab99', '2025-08': '853a733c023dc17e', '2025-09': '8caf00d18f9b0291', '2025-10': '59a383f029e74e13', '2025-11': '3a290605a5cac7a0', '2025-12': '9981c74cb2e6b5d5', '2026-01': '4c0e262cb8eb7fd0', '2026-02': '2d916d9b2f568eba', '2026-04': 'dd5ba3ad2517d100', '2026-05': 'c561fe05684c2b33', '2026-06': 'b9ae8898a5fe65bf', '2026-07': '5133b774e0963193', '2026-08': '2b6e9e9e23153f09', '2026-09': 'ab94e45031f2e272', '2026-10': '1e4e21409740a433', '2026-11': '9035a581129ed2d1'}
#: Luật `DT4-R1-07`: ảnh > 2 MB phải có nguyên nhân — đo 20/11: lớn nhất 1.826.670 byte ⇒ ⛔ ảnh nào.
TRAN_BYTE = 2 * 1024 * 1024
#: Số KỲ của sổ — gồm 2026-03 *(ảnh cũ)*. ISP khai 23 *(22 + 2026-03)*; đo 26 — lý do ở docstring.
MONG_KY_SO = 26
MONG_TONG_DONG = 12049
#: sha256 ảnh 2026-03 hiện có — ⛔ đổi *(AC-3: đúng từng byte)*.
SHA_ANH_03 = "fa9e4ca32f1eb4074695e0620ef9d5e469117cdbef6875862963a3fa586cb6b7"
#: Cột CẤM vào ảnh *(AC-4)*: `Diễn giải` · `Số chứng từ` · `Email Address` + tên người.
CAM = ("diễn giải", "số chứng từ", "số ct", "email address", "tên")


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _anh(ky: str) -> pathlib.Path:
    return DAP_AN / f"itl_ledge_{ky}.json"


def _cot_khuon() -> list[str]:
    """Khuôn cột = ĐÚNG ảnh 2026-03: `itl_id_sheet · ngay` + 28 cột *(thứ tự các khoá của dòng ảnh cũ)*."""
    return [k for k in _doc(ANH_03)["dong"][0] if k != "dong_sheet"]


def _nap_khuon():
    spec = importlib.util.spec_from_file_location("khuon_itl_ledge_ky", KHUON)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _checksum_lai(anh: dict) -> str:
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]), nguon=anh["nguon"],
                   dong=tuple(anh["dong"])).checksum()[:16]


# ── AC-1 ────────────────────────────────────────────────────────────────────────
def test_mong_la_phep_do_doc_lap_khong_rong():
    """Đ3: mẫu số của mọi phép so dưới đây KHÔNG rỗng — 25 kỳ · 12.049 dòng, ⛔ 0."""
    assert len(MONG) == 25 and sum(MONG.values()) == MONG_TONG_DONG and "2026-03" not in MONG


def test_AC1_moi_ky_ngoai_2026_03_co_anh_dung_so_dong():
    thieu = [k for k in MONG if not _anh(k).is_file()]
    assert not thieu, f"{len(thieu)}/25 kỳ chưa có ảnh: {thieu}"
    sai = {}
    for k, n in MONG.items():
        a = _doc(_anh(k))
        if not (a["so_dong"] == len(a["dong"]) == n and a["cong"]["dat"] and a["cong"]["mong"] == n):
            sai[k] = (a["so_dong"], len(a["dong"]), n)
    assert not sai, sai
    assert sum(_doc(_anh(k))["so_dong"] for k in MONG) == MONG_TONG_DONG


def test_AC1_moi_dong_co_ngay_dung_ky_va_khoa_dong_sheet_khong_trung():
    for k in MONG:
        a = _doc(_anh(k))
        ngay = {(r["ngay"]["chu"] if isinstance(r["ngay"], dict) else r["ngay"])[:7] for r in a["dong"]}
        assert ngay == {k}, (k, ngay)
        ds = [r["dong_sheet"] for r in a["dong"]]
        assert len(set(ds)) == len(ds)


def test_AC1_manifest_doc_duoc_cong_hong_bang_so_ky_cua_so():
    """Cổng liệt kê kỳ đọc được / hỏng: đọc được + hỏng = số kỳ của sổ *(⛔ bỏ im)*."""
    m = _doc(MANIFEST)
    assert m["so_ky_cua_so"] == MONG_KY_SO and m["mong_so_ky_cua_so"] == MONG_KY_SO
    assert m["tab"] == "ITL Ledge" and m["spreadsheet_id"] == "1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA"
    doc, hong = m["doc_duoc"], m["hong"]
    assert len(doc) + len(hong) + 1 == m["so_ky_cua_so"]          # +1 = 2026-03 (ảnh cũ, ⛔ đóng băng lại)
    assert doc == MONG and hong == {}, hong
    assert m["ky_bo_qua"] == {"2026-03": "ảnh có sẵn — ⛔ đụng"}


# ── AC-2 ────────────────────────────────────────────────────────────────────────
def test_AC2_ky_hong_phai_blocked_co_ten_va_tap_rong_la_do():
    k = _nap_khuon()
    # kỳ hỏng sau 3 lần thử ⇒ blocked CÓ TÊN, ⛔ ảnh rỗng
    assert k.so_lan_thu == 3
    ket = k.phan_loai_ky({"2026-04": 600, "2026-05": None}, mong=2)
    assert ket["hong"] == {"2026-05": "blocked"} and ket["doc_duoc"] == {"2026-04": 600} and not ket["dat"]
    # tập rỗng ⇒ ĐỎ (Đ3)
    assert not k.phan_loai_ky({}, mong=0)["dat"]
    # đủ ⇒ ĐẠT
    assert k.phan_loai_ky({"2026-04": 600}, mong=1)["dat"]


def test_AC2_cong_do_khi_mong_khac_so_dong(tmp_path):
    """Chiều ĐỎ của `--mong`: lệch 1 dòng ⇒ exit 1, ảnh vẫn ghi đúng nguồn ở `--ra`."""
    p = _tho_mau(tmp_path)
    ra = tmp_path / "ra.json"
    r = subprocess.run([sys.executable, str(TOOL), "itl_ledge_ky", str(p), "--mong", "3", "--ra", str(ra)],
                       capture_output=True, text=True, cwd=GOC)
    assert r.returncode == 1 and "[ĐỎ]" in r.stdout, (r.returncode, r.stdout[-300:], r.stderr[-300:])


# ── AC-3 ────────────────────────────────────────────────────────────────────────
def test_AC3_anh_2026_03_dung_tung_byte():
    assert hashlib.sha256(ANH_03.read_bytes()).hexdigest() == SHA_ANH_03


def test_AC3_khuon_cot_bang_anh_2026_03():
    cot = _cot_khuon()
    assert len(cot) == 30 and cot[:2] == ["itl_id_sheet", "ngay"]            # 28 + ngày + itl_id
    for ky in MONG:
        assert _doc(_anh(ky))["cot"] == cot, ky
    assert list(_nap_khuon().COT) == cot


def test_AC3_doi_ten_mot_cot_khuon_la_do(tmp_path):
    """Chiều ĐỎ: bản thô đổi 1 tên cột ⇒ khuôn TỪ CHỐI *(exit 2)*, ⛔ ghi ảnh."""
    tho = _doc(_tho_mau(tmp_path))
    tho["tieu_de"][5] = tho["tieu_de"][5] + " (đổi)"
    p = tmp_path / "doi.json"
    p.write_text(json.dumps(tho, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(TOOL), "itl_ledge_ky", str(p), "--mong", "2",
                        "--ra", str(tmp_path / "x.json")], capture_output=True, text=True, cwd=GOC)
    assert r.returncode == 2 and not (tmp_path / "x.json").exists(), (r.returncode, r.stderr[-300:])


# ── AC-4 ────────────────────────────────────────────────────────────────────────
def test_AC4_anh_khong_mang_cot_cam():
    for ky in MONG:
        a = _doc(_anh(ky))
        ten = [a["khoa"], *a["cot"], *a.get("cot_khong_chon", [])]
        bad = [c for c in ten if any(x in c.casefold() for x in CAM)]
        assert not bad, (ky, bad)


def test_AC4_cay_mot_cot_cam_la_do(tmp_path):
    """Chiều ĐỎ: bản thô cấy cột `Diễn giải` vào tiêu đề ⇒ TỪ CHỐI, ⛔ ghi ảnh."""
    for cam in ("Diễn giải", "Số chứng từ", "Email Address"):
        tho = _doc(_tho_mau(tmp_path))
        tho["tieu_de"][7] = cam
        p = tmp_path / "cam.json"
        p.write_text(json.dumps(tho, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(TOOL), "itl_ledge_ky", str(p), "--mong", "2",
                            "--ra", str(tmp_path / "y.json")], capture_output=True, text=True, cwd=GOC)
        assert r.returncode == 2 and not (tmp_path / "y.json").exists(), (cam, r.returncode)


# ── AC-5 ────────────────────────────────────────────────────────────────────────
def test_AC5_do_voi_so_luong_nap_duoc_anh_moi():
    spec = importlib.util.spec_from_file_location("_do_voi_so_luong_dt12", GOC / "tools" / "do_voi_so_luong.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    a = m._nap("dap_an/itl_ledge_2026-04.json")
    assert a["so_dong"] == len(a["dong"]) == MONG["2026-04"]


def test_checksum_ghim_va_itl_id_loi_va_kich_thuoc():
    for k in MONG:
        a = _doc(_anh(k))
        assert a["checksum_noi_dung"] == CHECKSUM[k], k
        n = sum(1 for r in a["dong"] if r["itl_id_sheet"]["chu"] == "#N/A ()")
        assert n == ITL_ID_LOI.get(k, 0), (k, n)
        assert all(r["itl_id_sheet"]["chu"] in ("#N/A ()",) or r["itl_id_sheet"]["chu"].startswith("ITL#")
                   for r in a["dong"]), k
        assert _anh(k).stat().st_size <= TRAN_BYTE, k
    m = _doc(MANIFEST)
    assert m["anh_lon_hon_2MB"] == [] and m["tong_bytes"] == sum(_anh(k).stat().st_size for k in MONG)
    assert {k: x["itl_id_loi"] for k, x in m["anh"].items() if x["itl_id_loi"]} == ITL_ID_LOI


def test_o_loi_khac_n_a_o_bat_ky_cot_la_tu_choi(tmp_path):
    """Chiều ĐỎ: chỉ `#N/A ()` ở `itl_id` được qua; `#REF!` ở 28 cột ⇒ TỪ CHỐI *(exit 2)*."""
    tho = _doc(_tho_mau(tmp_path))
    tho["hang"][0][5] = "#REF!"
    p = tmp_path / "loi.json"
    p.write_text(json.dumps(tho, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(TOOL), "itl_ledge_ky", str(p), "--mong", "2",
                        "--ra", str(tmp_path / "z.json")], capture_output=True, text=True, cwd=GOC)
    assert r.returncode == 2 and not (tmp_path / "z.json").exists()
    tho = _doc(_tho_mau(tmp_path)); tho["hang"][0][2] = "#N/A ()"      # itl_id lỗi đúng tập ⇒ QUA
    p.write_text(json.dumps(tho, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(TOOL), "itl_ledge_ky", str(p), "--mong", "2",
                        "--ra", str(tmp_path / "z.json")], capture_output=True, text=True, cwd=GOC)
    assert r.returncode == 0, r.stdout[-300:]


# ── checksum ───────────────────────────────────────────────────────────────────
def test_checksum_noi_dung_tinh_lai_khop_anh():
    sai = [k for k in MONG if _doc(_anh(k))["checksum_noi_dung"] != _checksum_lai(_doc(_anh(k)))]
    assert not sai, sai


# ── bản thô mẫu cho bài chiều ĐỎ ───────────────────────────────────────────────────
def _tho_mau(tmp_path) -> pathlib.Path:
    """Bản thô NHỎ đúng hình khuôn: 2 hàng · 1 kỳ. Dùng cho bài chiều ĐỎ — ⛔ dữ liệu thật."""
    k = _nap_khuon()
    p = tmp_path / "mau.json"
    p.write_text(json.dumps(k.tho_mau(), ensure_ascii=False), encoding="utf-8")
    return p
