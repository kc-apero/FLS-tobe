"""ĐÁP ÁN GL HR *(PD 407 · 408 · 413)* + CFA3 *(PD 411 phần CFA3)* — khuôn `gl_hr_407` · `gl_hr_408` ·
`gl_hr_413` · `cfa3` *(ISP 3.1.2 · Step 23 · DT6 · `WO-192`)*.

⭐ Bài ở đây TÁI TẠO lưới thô **từ chính ảnh** *(bản đọc thật ⛔ nằm trong repo — scratchpad, ⛔
commit)* rồi chạy lại công cụ ⇒ phải ra **đúng từng byte** tệp đã commit. Ca phá dựng lưới TỔNG HỢP.

    DT6-B1  ảnh đóng băng: số dòng theo kỳ có MONG · kỳ ⊂ 2025 *(KHÔNG — cổng IN rõ)* · cổng ĐẠT
    DT6-B2  PII: 0 cột tên/email; số tài khoản ngân hàng ở H·Z bị CHE; máy quét có ca phá
    AC-3    Y2024 đi bằng IMPORTRANGE ⇒ `#REF!` ⇒ `thiếu Y2024` CÓ TÊN trong ảnh
    AC-4    ô lỗi ghi NGUYÊN chuỗi, ĐẾM theo cột, ghim phân bố
    PD 412  ≡ `gl_406` *(⛔ ảnh mới)* — đo 18/11: tab GL sổ P&L == ảnh `gl_406` 7883/7883 dòng
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

from fls.canon.o_loi import la_o_loi
from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
DAP_AN = GOC / "tests" / "fixture" / "dap_an"
EPOCH = datetime.date(1899, 12, 30)
sys.path.insert(0, str(GOC / "tools" / "khuon_dong_bang"))
import _gl_hr as GL  # noqa: E402

#: Đo 18/11 *(khoá SA chỉ-đọc)* — mỗi số đếm MỘT vật *(Đ4)*.
PD = {
    "407": {"ten": "gl_hr_407", "mong": 9421, "checksum": "62c6b780950f167a",
            "ngoai_2025": {202601: 269}, "n_ky": 13, "doan": 1,
            "loi": {("P", "#N/A"): 11}},
    "408": {"ten": "gl_hr_408", "mong": 9410, "checksum": "59e1157d077c51e8",
            "ngoai_2025": {202601: 269}, "n_ky": 13, "doan": 7, "loi": {}},
    "413": {"ten": "gl_hr_413", "mong": 10785, "checksum": "b3b4e8485378ff57",
            "ngoai_2025": {202411: 165, 202412: 530, 202601: 269}, "n_ky": 15, "doan": 7,
            "loi": {("R", "#N/A ()"): 18}},
}
CHECKSUM_GL_406 = "53a243b42101c314"
CFA3_CHECKSUM = "4e61473a6b526057"


def _chay(*doi_so, tin_hieu=None):
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([sys.executable, str(TOOL), *map(str, doi_so)], cwd=GOC, env=env,
                          capture_output=True, text=True, timeout=300)


def _doc(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _checksum_lai(anh):
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _lit(v):
    if v is None:
        return "null"
    if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?([eE][+-]?\d+)?", v):
        return v
    return json.dumps(v, ensure_ascii=False)


def _ghi(p, hdr: dict, values):
    """Lưới thô: phần `values` viết TAY để ô số ra literal SỐ."""
    dong = ",\n  ".join("[" + ", ".join(_lit(x) for x in h) + "]" for h in values)
    khac = "".join(f' {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},\n' for k, v in hdr.items())
    p.write_text("{\n" + khac + f' "values": [\n  {dong}\n ]\n}}\n', encoding="utf-8")
    return p


def _serial(ky):
    y, m = divmod(int(ky), 100)
    return (datetime.date(y, m, 1) - EPOCH).days


Y2024 = [{"tab": t, "loai_o_loi": "#REF!", "so_hang_doc": n, "so_o_loi": 1,
          "so_hang_rong": n - 1, "so_hang_co_gia_tri": 0}
         for t, n in zip(GL.TAB_Y2024, (970, 413))]


def _luoi_gl(anh):
    """Lưới thô GL HR TÁI TẠO từ ảnh: tiêu đề từ `TIEU_DE`; hàng dữ liệu theo `dong_sheet`; đoạn
    A-rỗng theo bảng phụ `doan_trong` *(`so_hang_co_o_khac` hàng đầu mang một ô số ở AZ)*."""
    ix = {c: i for i, c in enumerate(GL.COT_THO)}
    hang = {}
    hdr = [[""] * len(GL.COT_THO) for _ in range(3)]
    for c, (a, b, d) in GL.TIEU_DE.items():
        for r, t in enumerate((a, b, d)):
            hdr[r][ix[c]] = t
    for d in anh["dong"]:
        r = [""] * len(GL.COT_THO)
        r[ix["A"]] = _serial(d["ky"])
        for c in GL.COT[1:]:
            if c != "ky":
                v = _chu(d[c])
                r[ix[c]] = "" if v is None else v
        hang[int(d["dong_sheet"])] = r
    for x in anh["phu"]["doan_trong"]["dong"]:
        tu, n, co = int(x["tu"]), int(x["so_hang"]), int(x["so_hang_co_o_khac"])
        for k in range(n):
            r = [""] * len(GL.COT_THO)
            if k < co:
                r[ix["AZ"]] = 0
            hang[tu + k] = r
    cuoi = max(hang)
    assert sorted(hang) == list(range(10, cuoi + 1))
    return hdr + [hang[i] for i in range(10, cuoi + 1)]


def _hdr_gl(anh):
    return {"nguon": anh["nguon"], "doc_luc": anh["ngay_dong_bang"], "cach_doc": anh["cach_doc"],
            "cot_sheet": list(GL.COT_THO), "dong_dau_sheet": 7, "y2024": Y2024}


def _da_tu_choi(kq):
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-600:], kq.stderr[-600:])
    assert len([d for d in kq.stderr.splitlines() if d.startswith("⛔ TỪ CHỐI")]) == 1


# ══ DT6-B1 · ảnh đã commit ═══════════════════════════════════════════════

@pytest.mark.parametrize("k", sorted(PD))
def test_DT6_B1_anh_GL_HR_so_dong_theo_ky_ky_NGOAI_2025_co_ten(k):
    """Ảnh thật: số dòng · kỳ · cổng ĐẠT · kỳ ⊄ 2025 CÓ TÊN ở `lac` *(AS-IS Y2025 nhưng dải
    thật có kỳ ngoài 2025 — cổng IN rõ, ⛔ im lặng)*. Mẫu số > 0 *(Đ3)*."""
    m = PD[k]
    anh = _doc(DAP_AN / f"{m['ten']}.json")
    assert anh["bang"] == f"PD.{k}" and anh["khuon"] == m["ten"]
    assert anh["khoa"] == "dong_sheet" and anh["cot"] == list(GL.COT)
    assert anh["so_dong"] == len(anh["dong"]) == m["mong"] > 0
    assert anh["cong"] == {"mong": m["mong"], "so_dong": m["mong"], "dat": True, "ly_do": []}
    assert (anh["thieu"], anh["khoa_hong"], anh["o_rong"]) == ([], [], [])
    ky = {}
    for d in anh["dong"]:
        ky[int(d["ky"])] = ky.get(int(d["ky"]), 0) + 1
    assert len(ky) == m["n_ky"] and sum(ky.values()) == m["mong"]
    ngoai = {a: b for a, b in ky.items() if a // 100 != 2025}
    assert ngoai == m["ngoai_2025"]                      # kỳ ⊄ 2025 — CÓ TÊN, ĐÚNG số dòng
    assert anh["lac"] == [str(a) for a in sorted(ngoai)]
    assert len({a for a in ky if a // 100 == 2025}) == 12  # đủ 12 tháng 2025
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == m["checksum"]
    assert len(anh["phu"]["doan_trong"]["dong"]) == m["doan"]


def test_DT6_B1_413_chua_408_va_them_1375_dong_nhu_da_do():
    """413 ⊃ 408 *(đo: 408 ≡ 413 ⇒ ⛔ — hai ảnh)*: 413 hơn 408 đúng 1375 dòng ở 2024-11/12 ·
    2025-01 · 2025-04; 407 hơn 408 đúng 11 dòng *(LE = `#N/A`)*."""
    def ky(t):
        r = {}
        for d in _doc(DAP_AN / f"gl_hr_{t}.json")["dong"]:
            r[int(d["ky"])] = r.get(int(d["ky"]), 0) + 1
        return r
    k407, k408, k413 = ky("407"), ky("408"), ky("413")
    hon = {a: k413.get(a, 0) - k408.get(a, 0) for a in set(k413) | set(k408)
           if k413.get(a, 0) != k408.get(a, 0)}
    assert hon == {202411: 165, 202412: 530, 202501: 468, 202504: 212} and sum(hon.values()) == 1375
    assert sum(k407.values()) - sum(k408.values()) == 11


@pytest.mark.parametrize("k", sorted(PD))
def test_DT6_AC1_tai_tao_luoi_tu_anh_ra_DUNG_TUNG_BYTE_va_cong_IN_ky_ngoai_2025(k, tmp_path):
    m = PD[k]
    anh = _doc(DAP_AN / f"{m['ten']}.json")
    tho = _ghi(tmp_path / "tho.json", _hdr_gl(anh), _luoi_gl(anh))
    ra = tmp_path / "ra.json"
    kq = _chay(m["ten"], tho, "--mong", m["mong"], "--ra", ra)
    assert kq.returncode == 0, (kq.stdout[-800:], kq.stderr[-800:])
    assert "kỳ ⊂ 2025: KHÔNG" in kq.stdout and "[ĐẠT]" in kq.stdout
    assert ra.read_bytes() == (DAP_AN / f"{m['ten']}.json").read_bytes()


# ══ DT6-B2 · PII ═════════════════════════════════════════════════════════

@pytest.mark.parametrize("ten", ["gl_hr_407", "gl_hr_408", "gl_hr_413", "cfa3"])
def test_DT6_B2_anh_0_cot_ten_email_va_khong_ro_so_tai_khoan(ten):
    """Ảnh thật: ⛔ cột nào của PM_COT_RIENG_TU · ⛔ Số chứng từ/Diễn giải/ID Payee · ⛔ dãy ≥ 6
    chữ số liền *(số tài khoản)* ngoài mã `ITL#…`/`PI…`/serial; H·Z chỉ còn `R`/`Thanh toán`."""
    van = (DAP_AN / f"{ten}.json").read_text(encoding="utf-8")
    anh = json.loads(van)
    ten_cot = {anh["khoa"], *anh["cot"]}
    for p in anh.get("phu", {}).values():
        for r in p["dong"]:
            ten_cot |= set(r)
    cam = {"email address", "số chứng từ", "diễn giải", "mã đối tác (id payee)", "b", "c", "m", "ap"}
    assert not {c.casefold() for c in ten_cot} & cam
    assert "@" not in van
    if ten != "cfa3":
        assert not re.search(r"\d+_(VPB|MSB)|VPB VND|MSB VND", van)
        for d in anh["dong"]:
            assert _chu(d["H"]) in (None, *GL.PAYMENT_TYPE) and _chu(d["Z"]) in (None, *GL.PAYMENT_TYPE)


def test_DT6_B2_so_tai_khoan_o_H_Z_bi_CHE_ve_tien_to_R(tmp_path):
    """Ca DƯƠNG: lưới có `R | 123456789_BANK VND_X` ở H/Z ⇒ ảnh giữ `R`, ⛔ giữ số."""
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    ix = {c: i for i, c in enumerate(GL.COT_THO)}
    v[3][ix["H"]] = "R | 123456789_ABC VND_DONVI"
    v[3][ix["Z"]] = "R | 123456789_ABC VND_DONVI"
    tho = _ghi(tmp_path / "t.json", _hdr_gl(anh), v)
    kq = _chay("gl_hr_407", tho, "--mong", 9421, "--ra", tmp_path / "r.json")
    assert "123456789" not in (tmp_path / "r.json").read_text(encoding="utf-8")
    assert kq.returncode in (0, 1)


@pytest.mark.parametrize("chen", ["ten_nguoi_o_cot_J", "so_tk_lo_H", "tieu_de_Email"])
def test_DT6_B2_may_quet_PII_co_CA_PHA_va_loi_KHONG_in_gia_tri(chen, tmp_path):
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    ix = {c: i for i, c in enumerate(GL.COT_THO)}
    bi_mat = "Nguyen Van Thanh"
    if chen == "ten_nguoi_o_cot_J":
        v[3][ix["J"]] = bi_mat
    elif chen == "so_tk_lo_H":
        v[3][ix["H"]] = "X | 987654321012 BANK"
        bi_mat = "987654321012"
    else:
        v[0][ix["Q"]] = "Email Address"
    tho = _ghi(tmp_path / "t.json", _hdr_gl(anh), v)
    kq = _chay("gl_hr_407", tho, "--mong", 9421, "--ra", tmp_path / "r.json")
    if chen == "tieu_de_Email":
        _da_tu_choi(kq)
    else:
        assert kq.returncode == 1, (kq.returncode, kq.stdout[-500:], kq.stderr[-500:])
        assert "[ĐỎ]" in kq.stdout and ("J_la@" in kq.stdout or "H_la@" in kq.stdout)
    assert bi_mat not in kq.stdout + kq.stderr             # ⛔ in giá trị ô


@pytest.mark.parametrize("chen", ["ten_nguoi", "itl_so_dai"])
def test_DT6_R1_01_cot_R_ITL_ID_co_CA_PHA_rieng_va_loi_KHONG_in_gia_tri(chen, tmp_path):
    """`DT6-R1-01`: `R` canh bằng regex *(⛔ tập đóng)* ⇒ phải có ca phá riêng. Đột biến nới
    `ITL_ID_RE` ra `.*` ⇒ bài này ĐỎ. `itl_so_dai` = `ITL#` + 12 chữ số *(giống số TK)*."""
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    ix = {c: i for i, c in enumerate(GL.COT_THO)}
    bi_mat = "Nguyen Van Thanh" if chen == "ten_nguoi" else "987654321012"
    v[3][ix["R"]] = bi_mat if chen == "ten_nguoi" else "ITL#" + bi_mat
    tho = _ghi(tmp_path / "t.json", _hdr_gl(anh), v)
    kq = _chay("gl_hr_407", tho, "--mong", 9421, "--ra", tmp_path / "r.json")
    assert kq.returncode == 1 and "R_la@10" in kq.stdout, (kq.returncode, kq.stdout[-400:])
    assert bi_mat not in kq.stdout + kq.stderr
    assert GL.ITL_ID_RE.fullmatch("ITL#1234") and not GL.ITL_ID_RE.fullmatch("ITL#1234567")


def test_DT6_R1_02_hai_nhanh_DO_chua_co_bai_NGU_CANH_thieu_va_luoi_khong_co_ngay():
    """`DT6-R1-02` *(đột biến `M9`·`M10`)*: gọi thẳng hàm, ⛔ qua CLI."""
    kq = GL.thieu_lac([], pd="khong_ton_tai", ky_mong={}, loi_mong={}, doan_mong=[])
    assert "NGU_CANH@thiếu" in kq["thieu"]                            # Đ5: ⛔ đo được = ĐỎ
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    v = [r if i < 3 else [""] + r[1:] for i, r in enumerate(v)]
    with pytest.raises(ValueError, match="⛔ có hàng nào cột A có ngày"):
        GL.chuan_bi(dict(_hdr_gl(anh), values=v), "gl_hr_407")


# ══ ca phá cổng (Đ5 hai chiều · Đ3) ══════════════════════════════════════

def test_DT6_cong_DO_khi_mot_ky_thieu_mot_dong_va_khi_doi_so_dong_mong(tmp_path):
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    v.pop(3)                                              # bỏ một hàng dữ liệu đầu *(kỳ 2025-01)*
    tho = _ghi(tmp_path / "t.json", _hdr_gl(anh), v)
    kq = _chay("gl_hr_407", tho, "--mong", 9420, "--ra", tmp_path / "r.json")
    assert kq.returncode == 1 and "ky@202501:224/225" in kq.stdout


def test_DT6_cong_DO_khi_them_loai_o_loi_moi_hay_doi_phan_bo(tmp_path):
    """AC-4 *(`DT5-R1-04`)*: thêm `#REF!` ở cột P ⇒ ĐỎ *(bản khai buộc ghi lại)*."""
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    v[3][GL.COT_THO.index("P")] = "#REF!"
    tho = _ghi(tmp_path / "t.json", _hdr_gl(anh), v)
    kq = _chay("gl_hr_407", tho, "--mong", 9421, "--ra", tmp_path / "r.json")
    assert kq.returncode == 1 and "o_loi@khác" in kq.stdout


def test_DT6_cong_DO_khi_doan_A_rong_doi(tmp_path):
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    del v[-1]                                             # đuôi A-rỗng ngắn đi một hàng
    tho = _ghi(tmp_path / "t.json", _hdr_gl(anh), v)
    kq = _chay("gl_hr_407", tho, "--mong", 9421, "--ra", tmp_path / "r.json")
    assert kq.returncode == 1 and "doan_trong@khác" in kq.stdout


def test_DT6_tap_rong_la_TU_CHOI_Đ3(tmp_path):
    anh = _doc(DAP_AN / "gl_hr_407.json")
    v = _luoi_gl(anh)
    ix = GL.COT_THO.index("A")
    v = [r if i < 3 else [""] + r[1:] for i, r in enumerate(v)]
    assert v[3][ix] == ""
    tho = _ghi(tmp_path / "t.json", _hdr_gl(anh), v)
    _da_tu_choi(_chay("gl_hr_407", tho, "--mong", 1, "--ra", tmp_path / "r.json"))


def test_DT6_AC3_Y2024_doc_DUOC_thi_TU_CHOI_con_doc_KHONG_duoc_thi_co_ten_trong_anh(tmp_path):
    """Y2024 đi bằng IMPORTRANGE ⇒ `#REF!`: ảnh ghi `thiếu Y2024` CÓ TÊN hai tab *(⛔ suy, ⛔ 0)*.
    Nếu một tab Y2024 có hàng giá trị ⇒ bằng chứng ⛔ khớp ⇒ TỪ CHỐI."""
    for k in PD:
        tn = _doc(DAP_AN / f"{PD[k]['ten']}.json")["phu"]["thieu_nguon"]["dong"]
        assert [_chu(r["tab"]) for r in tn] == list(GL.TAB_Y2024)
        assert all(_chu(r["nguyen_nhan"]) == "IMPORTRANGE ⇒ #REF!" and "thiếu Y2024" in _chu(r["ghi_chu"])
                   for r in tn)
    anh = _doc(DAP_AN / "gl_hr_407.json")
    hdr = _hdr_gl(anh)
    hdr["y2024"] = [dict(Y2024[0], so_hang_co_gia_tri=3, so_hang_rong=Y2024[0]["so_hang_rong"] - 3),
                    Y2024[1]]
    tho = _ghi(tmp_path / "t.json", hdr, _luoi_gl(anh))
    _da_tu_choi(_chay("gl_hr_407", tho, "--mong", 9421, "--ra", tmp_path / "r.json"))


def test_DT6_AC4_o_loi_nguon_ghi_NGUYEN_chuoi_dem_theo_cot():
    for k, m in PD.items():
        dem = {}
        for d in _doc(DAP_AN / f"{m['ten']}.json")["dong"]:
            for c in GL.CHU:
                s = _chu(d[c])
                if s and la_o_loi(s):
                    dem[(c, s)] = dem.get((c, s), 0) + 1
        assert dem == m["loi"], (k, dem)


# ══ PD 412 ≡ gl_406 ══════════════════════════════════════════════════════

def test_DT6_PD412_la_gl_406_KHONG_co_anh_moi():
    """Đo 18/11 *(khoá SA chỉ-đọc)*: tab `Report I General Ledger` của sổ P&L, cột A·D·R·BM:BT,
    hàng 10…: **7883/7883** dòng GIỐNG TỪNG Ô ảnh `gl_406` *(chỉ-ở-nguồn 0 · chỉ-ở-ảnh 0)* ⇒
    PD 412 ⛔ ảnh mới; ghim tham chiếu `gl_406`. ⚠ Tab cùng tên ở sổ CF KHÁC *(12.385 hàng có ngày,
    kỳ tới 2026-11; chỉ 2243/7883 hàng giống ảnh; 4502 hàng chỉ ở nguồn)* — khai ở BG-193."""
    anh = _doc(DAP_AN / "gl_406.json")
    assert anh["bang"] == "PD.406" and anh["so_dong"] == 7883
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM_GL_406
    assert not list(DAP_AN.glob("gl_412*")) and not list(DAP_AN.glob("gl_hr_412*"))


# ══ CFA3 ═════════════════════════════════════════════════════════════════

def _luoi_cfa3(anh):
    """Lưới CFA3 TÁI TẠO từ ảnh *(cột A mUSD ⛔ vào ảnh ⇒ 0)*: hàng 5 = serial, hàng 6 = thứ."""
    hd = anh["phu"]["hd"]["dong"]
    ngay = anh["phu"]["ngay_truc"]["dong"]
    rong = int(ngay[-1]["ngay"]) - int(ngay[0]["ngay"]) + 1
    assert rong == len(ngay)
    rows = [[""] * (6 + len(ngay)) for _ in range(93)]
    rows[4] = ["", "", "", "", "", "Day"] + [int(n["ngay"]) for n in ngay]
    rows[5] = ["", "L1", "L2", "L3", "L4", "Days of the week"] + [_chu(n["dow"]) for n in ngay]
    rows[6][0:3] = ["GROUP", "HDO", "HD Original"]
    cot_ngay = {int(n["ngay"]): 6 + i for i, n in enumerate(ngay)}
    dau_nhom = {}
    for h in hd:
        ds = int(h["dong_sheet"])
        r = rows[ds - 1]
        nhan = f"{_chu(h['ma'])} | {_chu(h['ten'])}"
        r[int(h["cap"])] = nhan
        r[5] = nhan
        r[0] = 0
        for j in range(6, len(r)):
            r[j] = 0
        dau_nhom.setdefault(_chu(h["nhom"]), ds)
    ten_nhom = {"HDO": "HD Original", "HDH": "HD HR", "HDAP": "HD Account Payable",
                "HDT": "HD Tempo", "HDC": "HD Calculated", "HDCI": "HD Calculated Internal"}
    for n, ds in dau_nhom.items():
        if n != "HDO":
            rows[ds - 2][1:3] = [n, ten_nhom[n]]
    pos = {(_chu(h["ma"])): int(h["dong_sheet"]) for h in hd}
    for d in anh["dong"]:
        rows[pos[_chu(d["ma_hd"])] - 1][cot_ngay[int(d["ngay"])]] = d["gt"]
    for o in anh["phu"]["o_loi"]["dong"]:
        rows[pos[_chu(o["ma_hd"])] - 1][cot_ngay[int(o["ngay"])]] = _chu(o["gia"])
    rows[88][1] = "CHECK ZONE"
    return rows


def _hdr_cfa3(anh):
    return {"spreadsheet_id": "x", "nguon": anh["nguon"], "doc_luc": anh["ngay_dong_bang"],
            "cach_doc": anh["cach_doc"]}


def test_DT6_CFA3_anh_74_HD_496_ngay_650_o_650_o_loi_5():
    anh = _doc(DAP_AN / "cfa3.json")
    assert anh["bang"] == "PD.CFA3" and anh["so_dong"] == len(anh["dong"]) == 650
    assert (anh["thieu"], anh["lac"]) == ([], [])
    assert anh["cong"]["dat"] is True and anh["checksum_noi_dung"] == _checksum_lai(anh) == CFA3_CHECKSUM
    assert len(anh["phu"]["hd"]["dong"]) == 74
    ng = anh["phu"]["ngay_truc"]["dong"]
    assert len(ng) == 496 and _chu(ng[0]["ngay_iso"]) == "2024-10-20" and _chu(ng[-1]["ngay_iso"]) == "2026-02-27"
    assert {_chu(r["gia"]) for r in anh["phu"]["o_loi"]["dong"]} == {"-"} and len(anh["phu"]["o_loi"]["dong"]) == 5
    assert {_chu(d["le"]) for d in anh["dong"]} == {"GROUP"}


def test_DT6_CFA3_tai_tao_luoi_ra_DUNG_TUNG_BYTE(tmp_path):
    anh = _doc(DAP_AN / "cfa3.json")
    tho = _ghi(tmp_path / "t.json", _hdr_cfa3(anh), _luoi_cfa3(anh))
    ra = tmp_path / "r.json"
    kq = _chay("cfa3", tho, "--mong", 650, "--ra", ra)
    assert kq.returncode == 0, (kq.stdout[-600:], kq.stderr[-600:])
    assert ra.read_bytes() == (DAP_AN / "cfa3.json").read_bytes()


@pytest.mark.parametrize("pha", ["ma_la", "thieu_ma", "o_loi_moi"])
def test_DT6_CFA3_cong_DO_ma_la_thieu_ma_hay_doi_o_loi(pha, tmp_path):
    anh = _doc(DAP_AN / "cfa3.json")
    v = _luoi_cfa3(anh)
    mong = 650
    if pha == "ma_la":
        v[7][1] = "ZZZ | Ma La"                          # hàng GI → mã ⛔ ∈ ATL
    elif pha == "thieu_ma":
        v[7][1] = ""                                     # hàng GI mất nhãn ⇒ 73 mã
        v[7][5] = ""
    else:
        v[8][10] = "#REF!"
        mong = 650
    tho = _ghi(tmp_path / "t.json", _hdr_cfa3(anh), v)
    kq = _chay("cfa3", tho, "--mong", mong, "--ra", tmp_path / "r.json")
    if pha == "thieu_ma":
        _da_tu_choi(kq)                                  # 73 ≠ 74 ⇒ TỪ CHỐI *(khuôn)*
    else:
        assert kq.returncode == 1, (kq.returncode, kq.stdout[-400:], kq.stderr[-300:])
