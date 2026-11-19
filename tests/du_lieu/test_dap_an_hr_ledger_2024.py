"""ĐẦU VÀO Y2024 sổ HR `hr_ledger_2024` + ĐỐI CHIẾU với `gl_hr_413` *(ISP 3.1.2 · DT6b · `WO-225` AC-1·AC-2)*.

    Y24-B1  ảnh thật: 1.381 hàng · số hàng MỖI (tab, kỳ) và Σ PS Có MỖI kỳ có MONG · cổng ĐẠT · checksum ghim
    Y24-B2  PII: 0 cột Số CT/Diễn giải/ID Payee · 6 ô `H` mang số tài khoản đã CHE về `R` · máy quét có ca phá
    Y24-AC1 tái tạo lưới thô từ ảnh ⇒ đúng TỪNG BYTE; ca phá cổng ĐỎ hai chiều
    Y24-AC2 đối chiếu với `gl_hr_413` − `gl_hr_408` *(P&L dán giá trị)*: khớp/lệch theo kỳ, lệch CÓ TÊN
"""
from __future__ import annotations

import datetime
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
ANH = GOC / "tests" / "fixture" / "dau_vao" / "hr_ledger_2024.json"
DAP_AN = GOC / "tests" / "fixture" / "dap_an"
EPOCH = datetime.date(1899, 12, 30)
sys.path.insert(0, str(GOC / "tools" / "khuon_dong_bang"))
import hr_ledger_2024 as Y  # noqa: E402

MONG = 1381
CHECKSUM = "4905b28f88819142"
TAB_KY = {"NIS|202411": 165, "NIS|202412": 536, "NIS|202501": 268, "PIT|202501": 200, "PIT|202504": 212}
F_KY = {202411: 286400000, 202412: 5140567470, 202501: 5543361433, 202504: 551671054}
#: AC-2 — đo 19/11: so Y2024 với phần 413 hơn 408 *(DT6: 165 · 530 · 468 · 212 = 1.375)*.
KHOP = {202411: 165, 202412: 530, 202501: 468, 202504: 207}
CHI_Y2024 = {202412: 6, 202504: 5}
CHI_413 = {202504: 5}


def _doc(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _num(v):
    return None if v is None else Decimal(str(v))


def _chay(*doi_so):
    return subprocess.run([sys.executable, str(TOOL), *map(str, doi_so)], cwd=GOC,
                          env=dict(os.environ, PYTHONUTF8="1"), capture_output=True, text=True,
                          timeout=300)


def _checksum_lai(anh):
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _serial(ky):
    y, m = divmod(int(ky), 100)
    return (datetime.date(y, m, 1) - EPOCH).days


def _luoi(anh):
    """Lưới thô TÁI TẠO từ ảnh *(cột A = ngày mùng 1 của kỳ; H `R` ⇒ `R`)*."""
    tabs = []
    for ten, tab in zip(("NIS", "PIT"), Y.TABS):
        vals = []
        for d in anh["dong"]:
            if _chu(d["tab"]) != ten:
                continue
            g = lambda c: "" if _chu(d[c]) is None else _chu(d[c])      # noqa: E731
            e = "" if d["E"] is None else int(d["E"])
            f = "" if d["F"] is None else int(d["F"])
            vals.append([_serial(d["ky"]), g("D"), e, f, g("G"), g("H"), g("hd"), g("cdt1"), g("le")])
        tabs.append({"tab": tab, "dong_dau_sheet": 4, "cot_sheet": list(Y.COT_THO),
                     "tieu_de": list(Y.TIEU_DE), "values": vals})
    return {"nguon": anh["nguon"], "doc_luc": anh["ngay_dong_bang"], "cach_doc": anh["cach_doc"],
            "tabs": tabs}


def _ghi(p, tho):
    p.write_text(json.dumps(tho, ensure_ascii=False), encoding="utf-8")
    return p


# ══ Y24-B1 ═══════════════════════════════════════════════════════════════

def test_Y24_B1_anh_1381_hang_theo_tab_ky_va_tong_PS_Co_co_MONG():
    anh = _doc(ANH)
    assert anh["bang"] == "HR.Ledger.2024" and anh["khuon"] == "hr_ledger_2024"
    assert anh["so_dong"] == len(anh["dong"]) == MONG == 969 + 412 > 0
    assert anh["cong"] == {"mong": MONG, "so_dong": MONG, "dat": True, "ly_do": []}
    assert (anh["thieu"], anh["lac"], anh["khoa_hong"], anh["o_rong"]) == ([], [], [], [])
    dem = Counter(f"{_chu(d['tab'])}|{d['ky']}" for d in anh["dong"])
    assert dict(dem) == TAB_KY
    f = Counter()
    for d in anh["dong"]:
        f[int(d["ky"])] += int(d["F"] or 0)
    assert dict(f) == F_KY
    tong = {(_chu(r["tab"]), int(r["ky"])): (int(r["so_hang"]), int(r["tong_F"]))
            for r in anh["phu"]["tong_ky"]["dong"]}
    assert sum(v[0] for v in tong.values()) == MONG and sum(v[1] for v in tong.values()) == sum(F_KY.values())
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM
    assert len({int(d["dong_sheet"]) for d in anh["dong"]}) == MONG          # khoá ⛔ trùng
    assert sum(1 for d in anh["dong"] if int(d["dong_sheet"]) >= 100000) == 412   # PIT +100000


# ══ Y24-B2 · PII ═════════════════════════════════════════════════════════

def test_Y24_B2_anh_0_cot_rieng_tu_va_6_o_H_so_tai_khoan_bi_CHE_ve_R():
    van = ANH.read_text(encoding="utf-8")
    anh = json.loads(van)
    ten_cot = {anh["khoa"], *anh["cot"]}
    for p in anh["phu"].values():
        for r in p["dong"]:
            ten_cot |= set(r)
    cam = {"email address", "số chứng từ", "diễn giải", "mã đối tác (id payee)", "b", "c", "id payee"}
    assert not {c.casefold() for c in ten_cot} & cam
    assert "@" not in van
    h = Counter(_chu(d["H"]) for d in anh["dong"])
    assert set(h) <= {None, "R", "Thanh toán (Regular)"} and h["R"] == Y.MONG_H_R == 6   # Đ3: mẫu số > 0
    for d in anh["dong"]:                                        # ⛔ ô chữ nào ≥ 6 chữ số liền
        for c in Y.CHU:
            s = _chu(d[c])
            assert s is None or not any(len(x) >= 6 for x in "".join(ch if ch.isdigit() else " " for ch in s).split())


def test_Y24_B2_so_tk_tran_va_dang_R_pipe_deu_bi_che_va_khong_in_ra(tmp_path):
    anh = _doc(ANH)
    tho = _luoi(anh)
    v = tho["tabs"][0]["values"]
    v[0][5] = "987654321"                                        # số trần (dạng Y2024)
    v[1][5] = "R | 123456789_ABC VND_DONVI"                       # dạng DT6
    ra = tmp_path / "r.json"
    kq = _chay("hr_ledger_2024", _ghi(tmp_path / "t.json", tho), "--mong", MONG, "--ra", ra)
    txt = ra.read_text(encoding="utf-8")
    assert "987654321" not in txt and "123456789" not in txt and "987654321" not in kq.stdout + kq.stderr
    assert kq.returncode == 1 and "H_che@khác:8/6" in kq.stdout        # che ĐÚNG, nhưng số ô che ≠ mong ⇒ ĐỎ


@pytest.mark.parametrize("chen", ["ten_o_cdt1", "so_tk_la_o_H", "tieu_de_lech"])
def test_Y24_B2_may_quet_co_CA_PHA_va_loi_KHONG_in_gia_tri(chen, tmp_path):
    tho = _luoi(_doc(ANH))
    v = tho["tabs"][1]["values"]
    bi_mat = "Nguyen Van Thanh"
    if chen == "ten_o_cdt1":
        v[0][7] = bi_mat
    elif chen == "so_tk_la_o_H":
        v[0][5] = "X | 987654321012 BANK"
        bi_mat = "987654321012"
    else:
        tho["tabs"][0]["tieu_de"][3] = "PS Nợ"
    kq = _chay("hr_ledger_2024", _ghi(tmp_path / "t.json", tho), "--mong", MONG, "--ra", tmp_path / "r.json")
    if chen == "tieu_de_lech":
        assert kq.returncode == 2 and len([d for d in kq.stderr.splitlines() if d.startswith("⛔ TỪ CHỐI")]) == 1
    else:
        assert kq.returncode == 1 and ("cdt1_la@" in kq.stdout or "H_la@" in kq.stdout)
    assert bi_mat not in kq.stdout + kq.stderr


# ══ Y24-AC1 ══════════════════════════════════════════════════════════════

def test_Y24_AC1_tai_tao_luoi_tu_anh_ra_DUNG_TUNG_BYTE(tmp_path):
    anh = _doc(ANH)
    ra = tmp_path / "r.json"
    kq = _chay("hr_ledger_2024", _ghi(tmp_path / "t.json", _luoi(anh)), "--mong", MONG, "--ra", ra)
    assert kq.returncode == 0 and "[ĐẠT]" in kq.stdout, (kq.stdout[-600:], kq.stderr[-400:])
    assert ra.read_bytes() == ANH.read_bytes()


def test_Y24_AC1_cong_DO_khi_thieu_mot_hang_hay_doi_PS_Co_hay_so_hang_mong(tmp_path):
    tho = _luoi(_doc(ANH))
    tho["tabs"][1]["values"].pop(0)                              # PIT mất một hàng 2025-01
    kq = _chay("hr_ledger_2024", _ghi(tmp_path / "t.json", tho), "--mong", MONG - 1, "--ra", tmp_path / "r.json")
    assert kq.returncode == 1 and "tab_ky@PIT:202501:199/200" in kq.stdout
    tho = _luoi(_doc(ANH))
    tho["tabs"][0]["values"][0][3] = 1                           # PS Có đổi ⇒ Σ kỳ lệch
    kq = _chay("hr_ledger_2024", _ghi(tmp_path / "t2.json", tho), "--mong", MONG, "--ra", tmp_path / "r2.json")
    assert kq.returncode == 1 and "F_ky@" in kq.stdout


def test_Y24_AC1_tap_rong_la_TU_CHOI_va_ngay_khong_phai_so_la_TU_CHOI(tmp_path):
    tho = _luoi(_doc(ANH))
    tho["tabs"][1]["values"] = []
    assert _chay("hr_ledger_2024", _ghi(tmp_path / "a.json", tho), "--mong", 1, "--ra", tmp_path / "r.json").returncode == 2
    tho = _luoi(_doc(ANH))
    tho["tabs"][0]["values"][0][0] = ""
    assert _chay("hr_ledger_2024", _ghi(tmp_path / "b.json", tho), "--mong", MONG, "--ra", tmp_path / "r.json").returncode == 2


# ══ Y24-AC2 · đối chiếu với gl_hr_413 ═══════════════════════════════════

def _khoa_413(ten):
    """Hàng CÓ NGÀY của 413/408 ở bốn kỳ Y2024, khoá `(ky, E, F, G, HDCode, CDT1)`."""
    r = Counter()
    for d in _doc(DAP_AN / f"{ten}.json")["dong"]:
        if _chu(d.get("ky_suy")) is not None or int(d["ky"]) not in KHOP:
            continue
        r[(int(d["ky"]), _num(d["E"]), _num(d["F"]), _chu(d["G"]), _chu(d["I"]), _chu(d["J"]))] += 1
    return r


def test_Y24_AC2_doi_chieu_Y2024_voi_413_tru_408_khop_lech_theo_ky_lech_CO_TEN():
    anh = _doc(ANH)
    y = Counter((int(d["ky"]), _num(d["E"]), _num(d["F"]), _chu(d["G"]), _chu(d["hd"]), _chu(d["cdt1"]))
                for d in anh["dong"])
    c413, c408 = _khoa_413("gl_hr_413"), _khoa_413("gl_hr_408")
    them = c413 - c408                                           # phần CHỈ có ở 413 *(1.375 dòng — DT6)*
    assert sum(them.values()) == 1375 and not (c408 - c413)
    assert dict(Counter(k[0] for k in them.elements())) == {202411: 165, 202412: 530, 202501: 468, 202504: 212}
    assert dict(Counter(k[0] for k in (y & them).elements())) == KHOP          # khớp từng ô
    chi_y, chi_413 = y - them, them - y
    assert dict(Counter(k[0] for k in chi_y.elements())) == CHI_Y2024
    assert dict(Counter(k[0] for k in chi_413.elements())) == CHI_413
    # Σ PS Có mỗi kỳ Y2024 = Σ PS Có phần 413 hơn 408 *(lệch CHỈ ở PS Nợ)*
    for ky, f in F_KY.items():
        assert sum((k[2] or 0) * n for k, n in them.items() if k[0] == ky) == f
    # ── lệch 2024-12 *(536 vs 530)*: 6 hàng CHỈ có PS Nợ, ⛔ TK/HDCode/CDT1 — đúng 6 ô `H` mang số tài khoản
    assert all(k[3] is None and k[4] is None and k[5] is None and k[2] is None
               for k in chi_y.elements() if k[0] == 202412)
    r_202412 = [d for d in anh["dong"] if _chu(d["H"]) == "R"]
    assert len(r_202412) == 6 and {int(d["ky"]) for d in r_202412} == {202412}
    # ── lệch 2025-04 *(5 hàng PIT)*: cùng F·G·HDCode·CDT1, KHÁC PS Nợ *(413 chia lại, có phần lẻ)*
    ky04 = [k for k in chi_y.elements() if k[0] == 202504]
    assert sorted(k[3] for k in ky04) == sorted(k[3] for k in chi_413.elements() if k[0] == 202504)
    assert {k[2] for k in ky04} == {Decimal(0)}
