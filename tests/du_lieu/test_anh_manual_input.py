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


# ── AC-1 ────────────────────────────────────────────────────────────────────────
def test_mong_la_phep_do_doc_lap_khong_rong():
    """Đ3: mẫu số của mọi phép so dưới đây KHÔNG rỗng — 25 kỳ · 12.049 dòng, ⛔ 0."""
    assert len(MONG) == 25 and sum(MONG.values()) == MONG_TONG_DONG and "2026-03" not in MONG


def test_AC1_moi_ky_ngoai_2026_03_co_anh_dung_so_dong():
    thieu = [k for k in MONG if not _anh(k).is_file()]
    assert not thieu, f"{len(thieu)}/25 kỳ chưa có ảnh: {thieu}"
    sai = {}
    m = _doc(MANIFEST)
    for k, n in MONG.items():
        a = _doc(_anh(k))
        cong = m["anh"][k]["cong"]          # cổng `--mong` của lượt đóng băng — ở manifest *(ảnh = hình 2026-03, ⛔ mang cổng)*
        if not (a["so_dong"] == len(a["dong"]) == n and cong["dat"] and cong["mong"] == cong["so_dong"] == n):
            sai[k] = (a["so_dong"], len(a["dong"]), n)
    assert not sai, sai
    assert sum(_doc(_anh(k))["so_dong"] for k in MONG) == MONG_TONG_DONG


def test_AC1_moi_dong_co_ngay_dung_ky_va_khoa_dong_sheet_khong_trung():
    for k in MONG:
        a = _doc(_anh(k))
        ngay = {r["ngay"][:7] for r in a["dong"]}
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
        assert [c for c in _doc(_anh(ky))["dong"][0] if c != "dong_sheet"] == cot, ky      # khoá dòng = ảnh 2026-03
        assert _doc(MANIFEST)["anh"][ky]["cot"] == cot, ky
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
        ten = [*a, *a["dong"][0]]          # khoá cấp trên + khoá dòng
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
def _h15():
    """Module `tools/do_voi_so_luong.py` — ĐÚNG đường đọc mà H15 *(Step 43)* sẽ dùng: `_nap` rồi `_chuan` từng ô."""
    spec = importlib.util.spec_from_file_location("_do_voi_so_luong_dt12", GOC / "tools" / "do_voi_so_luong.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


def _loi_gia_tri_h15(m, d: dict, ky: str) -> list[str]:
    """Đo GIÁ TRỊ qua đường đọc H15 *(⛔ chỉ `json.loads` — AC-5 cũ xanh trên ảnh mà `d["ky"]` KeyError)*."""
    loi = []
    if "ky" not in d or d["ky"] != ky:
        loi.append("khoá cấp trên `ky` thiếu/sai")
    if not isinstance(d.get("dong_du_lieu_bat_dau"), int):
        loi.append("`dong_du_lieu_bat_dau` thiếu/không phải số")
    n = len(d.get("dong", []))
    if not n or d.get("so_dong") != n:
        loi.append(f"`so_dong` {d.get('so_dong')} ≠ {n} dòng *(hoặc rỗng — Đ3)*")
    sai_chuoi = sai_kieu = 0
    for r in d.get("dong", []):
        if m._chuan(r["hd_manual"]).startswith("{"):          # `_chuan` của dict = "{'chu': …}" — chuỗi dict, ⛔ giá trị
            sai_chuoi += 1
        if not isinstance(r["dong_sheet"], int) or isinstance(r["dong_sheet"], bool):
            sai_kieu += 1
    if sai_chuoi:
        loi.append(f"{sai_chuoi} ô `hd_manual` qua `_chuan` ra chuỗi dict")
    if sai_kieu:
        loi.append(f"{sai_kieu} `dong_sheet` ⛔ phải số")
    return loi


KY_H15 = ("2024-10", "2025-06", "2026-04", "2026-11")


def test_AC5_do_gia_tri_qua_duong_doc_H15():
    """AC-5 *(sửa theo `KQ-267` `DT12-R1-01`)*: ≥ 3 ảnh mới — gồm `2024-10` · `2026-11` — đọc bằng `_nap` + `_chuan` ra GIÁ TRỊ."""
    m = _h15()
    ref03 = m._nap("itl_ledge_2026_03.json")
    for ky in KY_H15:
        d = m._nap(f"dap_an/itl_ledge_{ky}.json")
        assert not _loi_gia_tri_h15(m, d, ky), (ky, _loi_gia_tri_h15(m, d, ky))
        assert type(d["dong"][0]["dong_sheet"]) is type(ref03["dong"][0]["dong_sheet"]) is int, ky
        assert d["so_dong"] == len(d["dong"]) == MONG[ky]
        # ô chữ → chuỗi thật, ô trống → ""; ô SỐ giữ số rồi `_chuan` → chuỗi thập phân
        r = d["dong"][0]
        assert m._chuan(r["hd_manual"]) and not m._chuan(r["hd_manual"]).startswith("{"), ky
        assert isinstance(r["hd_manual"], str) and isinstance(r["itl_id_sheet"], str), ky


def test_AC5_do_hinh_moi_anh_bang_anh_2026_03():
    """Tập khoá cấp trên + khoá dòng + KIỂU ô của MỌI ảnh mới ⊆ ảnh 2026-03 *(25/25; mẫu số = 25 kỳ, Đ3)*."""
    k = _nap_khuon()
    mau = _doc(ANH_03)
    assert len(MONG) == 25
    sai = {ky: k.loi_hinh(_doc(_anh(ky)), mau) for ky in MONG}
    sai = {ky: v for ky, v in sai.items() if v}
    assert not sai, sai
    assert list(_doc(_anh("2026-04"))) == list(mau)                  # đúng THỨ TỰ khoá cấp trên


def _anh_mau_tu_tho(tmp_path) -> dict:
    """Dựng một ảnh nhỏ qua đường THẬT: bản thô mẫu → cổng `dong_bang_sheet` → `chuan_hoa_anh`."""
    ra = tmp_path / "cong.json"
    r = subprocess.run([sys.executable, str(TOOL), "itl_ledge_ky", str(_tho_mau(tmp_path)), "--mong", "2", "--ra", str(ra)],
                       capture_output=True, text=True, cwd=GOC)
    assert r.returncode == 0, r.stdout[-300:]
    return _nap_khuon().chuan_hoa_anh(_doc(ra))


def test_AC5_chuan_hoa_ra_dung_hinh_va_giu_so(tmp_path):
    a = _anh_mau_tu_tho(tmp_path)
    mau = _doc(ANH_03)
    assert _nap_khuon().loi_hinh(a, mau) == [] and list(a) == list(mau)
    r = a["dong"][0]
    assert r["dong_sheet"] == 10 and r["svc_start_manual"] == 202604 and type(r["svc_start_manual"]) is int
    assert r["hd_manual"] == "Need to manual input" or isinstance(r["hd_manual"], str)


def test_AC5_dot_bien_hinh_va_gia_tri_deu_do(tmp_path):
    """Đột biến *(bản sao trong bộ nhớ)*: bọc lại 1 ô `{"chu"}` · xoá khoá `ky` · `dong_sheet` thành chuỗi ⇒ MỖI cái ĐỎ ở
    cả hai bài đo *(hình + giá trị qua H15)*; ảnh nguyên ⇒ xanh *(chiều dương — bằng chứng ⛔ bị biên bản làm nhiễu)*."""
    k, m, mau = _nap_khuon(), _h15(), _doc(ANH_03)
    goc = _doc(_anh("2024-10"))
    assert k.loi_hinh(goc, mau) == [] and _loi_gia_tri_h15(m, goc, "2024-10") == []

    boc = copy.deepcopy(goc); boc["dong"][0]["hd_manual"] = {"chu": boc["dong"][0]["hd_manual"]}
    bo_ky = copy.deepcopy(goc); del bo_ky["ky"]
    ds_chu = copy.deepcopy(goc); ds_chu["dong"][0]["dong_sheet"] = str(ds_chu["dong"][0]["dong_sheet"])
    so_boc = copy.deepcopy(goc); so_boc["dong"][0]["svc_start_manual"] = {"chu": "202410"}
    for ten, d in (("bọc {chu}", boc), ("xoá ky", bo_ky), ("dong_sheet chuỗi", ds_chu), ("ô số bọc {chu}", so_boc)):
        assert k.loi_hinh(d, mau), f"hình: {ten} ⛔ bị bắt"
    for ten, d in (("bọc {chu}", boc), ("xoá ky", bo_ky), ("dong_sheet chuỗi", ds_chu)):
        assert _loi_gia_tri_h15(m, d, "2024-10"), f"giá trị H15: {ten} ⛔ bị bắt"


def test_checksum_ghim_va_itl_id_loi_va_kich_thuoc():
    for k in MONG:
        a = _doc(_anh(k))
        assert _doc(MANIFEST)["anh"][k]["checksum_noi_dung"] == CHECKSUM[k], k      # checksum sống ở manifest *(ảnh = hình 2026-03)*
        n = sum(1 for r in a["dong"] if r["itl_id_sheet"] == "#N/A ()")
        assert n == ITL_ID_LOI.get(k, 0), (k, n)
        assert all(r["itl_id_sheet"] in ("#N/A ()",) or r["itl_id_sheet"].startswith("ITL#")
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
    """⭐ KHỨ HỒI *(`DT12-R1-01`)*: ảnh ĐÃ chuẩn hoá về hình 2026-03 → `ve_dang_cong` (ô → `{"chu"}` · `thu_tu`) → checksum của
    `AnhChup` = checksum ghim của lượt đóng băng gốc ⇒ chuẩn hoá ⛔ mất/đổi một ô nào *(100 % — 25/25 kỳ, mẫu số ở `MONG`)*."""
    k = _nap_khuon()
    ngay = _doc(MANIFEST)["doc_luc"]
    sai = [ky for ky in MONG
           if CHECKSUM[ky] != AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(ngay), nguon=_doc(_anh(ky))["nguon"],
                                      dong=tuple(k.ve_dang_cong(_doc(_anh(ky))))).checksum()[:16]]
    assert len(MONG) == 25 and not sai, sai
    assert {ky: x["checksum_noi_dung"] for ky, x in _doc(MANIFEST)["anh"].items()} == CHECKSUM


# ── bản thô mẫu cho bài chiều ĐỎ ───────────────────────────────────────────────────
def _tho_mau(tmp_path) -> pathlib.Path:
    """Bản thô NHỎ đúng hình khuôn: 2 hàng · 1 kỳ. Dùng cho bài chiều ĐỎ — ⛔ dữ liệu thật."""
    k = _nap_khuon()
    p = tmp_path / "mau.json"
    p.write_text(json.dumps(k.tho_mau(), ensure_ascii=False), encoding="utf-8")
    return p
