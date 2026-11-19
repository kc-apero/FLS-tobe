"""ĐẦU VÀO Y2025 sổ HR `hr_ledger_2025` + ĐỐI CHIẾU với `gl_hr_408` *(ISP 3.1.2 · DT6c · `WO-249` AC-1…AC-4)*.

    Y25-B1  ảnh thật: 10.105 hàng · số hàng MỖI (tab, kỳ) và Σ PS Có MỖI kỳ có MONG · cổng ĐẠT · checksum ghim
    Y25-B2  PII: 0 cột Số CT/Diễn giải/ID Payee · 9 ô `H` mang số tài khoản đã CHE về `R` · ca phá
    Y25-AC1 tái tạo lưới thô từ ảnh ⇒ đúng TỪNG BYTE; ca phá cổng ĐỎ hai chiều (kể cả `#N/A` ở LE)
    Y25-AC2 đối chiếu với `gl_hr_408` *(đáp án — chỉ để ĐO)*: số hàng · Σ PS Có theo kỳ, lệch CÓ TÊN
    Y25-AC3 KHOÁ ĐÚNG: ảnh 2024 ⛔ đổi byte khi mở rộng khuôn
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
ANH = GOC / "tests" / "fixture" / "dau_vao" / "hr_ledger_2025.json"
ANH24 = GOC / "tests" / "fixture" / "dau_vao" / "hr_ledger_2024.json"
DAP_AN = GOC / "tests" / "fixture" / "dap_an"
EPOCH = datetime.date(1899, 12, 30)
sys.path.insert(0, str(GOC / "tools" / "khuon_dong_bang"))
import hr_ledger_2025 as Y  # noqa: E402

MONG = 10105
CHECKSUM = "c27a12e49b7aa875"
TAB_KY = {"NIS|202501": 225, "NIS|202502": 668, "NIS|202503": 629, "NIS|202504": 579, "NIS|202505": 365,
          "NIS|202506": 916, "NIS|202507": 850, "NIS|202508": 767, "NIS|202509": 912, "NIS|202510": 868,
          "NIS|202511": 478, "NIS|202512": 328, "PIT|202504": 462, "PIT|202507": 835, "PIT|202510": 1223}
F_KY = {202501: "321317500", 202502: "5745812541", 202503: "5971078533", 202504: "7967090891",
        202505: "6623088442", 202506: "7642967845.363", 202507: "9712306163.707232147", 202508: "7862221681",
        202509: "8241418295", 202510: "11751792973", 202511: "7356669375", 202512: "7332731464"}


def _doc(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _chay(*doi_so):
    return subprocess.run([sys.executable, str(TOOL), *map(str, doi_so)], cwd=GOC,
                          env=dict(os.environ, PYTHONUTF8="1"), capture_output=True, text=True,
                          timeout=300)


def _checksum_lai(anh):
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _so(v):
    """Ô số của ảnh *(chuỗi `Decimal`)* → số của lưới thô: `int` khi nguyên, `float` khi lẻ."""
    if v is None:
        return ""
    d = Decimal(str(v))
    return int(d) if d == d.to_integral_value() else float(d)


def _serial(ky):
    y, m = divmod(int(ky), 100)
    return (datetime.date(y, m, 1) - EPOCH).days


def _luoi(anh):
    """Lưới thô TÁI TẠO từ ảnh *(cột A = ngày mùng 1 của kỳ; H `R` ⇒ `R`; số lẻ giữ nguyên)*."""
    tabs = []
    for ten, tab in zip(("NIS", "PIT"), Y.TABS):
        vals = []
        for d in anh["dong"]:
            if _chu(d["tab"]) != ten:
                continue
            g = lambda c: "" if _chu(d[c]) is None else _chu(d[c])      # noqa: E731
            vals.append([_serial(d["ky"]), g("D"), _so(d["E"]), _so(d["F"]), g("G"), g("H"), g("hd"), g("cdt1"), g("le")])
        tabs.append({"tab": tab, "dong_dau_sheet": 4, "cot_sheet": list(Y.COT_THO),
                     "tieu_de": list(Y.TIEU_DE), "values": vals})
    return {"nguon": anh["nguon"], "doc_luc": anh["ngay_dong_bang"], "cach_doc": anh["cach_doc"],
            "tabs": tabs}


def _ghi(p, tho):
    p.write_text(json.dumps(tho, ensure_ascii=False), encoding="utf-8")
    return p


# ══ Y25-B1 ═══════════════════════════════════════════════════════════════

def test_Y25_B1_anh_10105_hang_theo_tab_ky_va_tong_PS_Co_co_MONG():
    anh = _doc(ANH)
    assert anh["bang"] == "HR.Ledger.2025" and anh["khuon"] == "hr_ledger_2025"
    assert anh["so_dong"] == len(anh["dong"]) == MONG == 7585 + 2520 > 0
    assert anh["cong"] == {"mong": MONG, "so_dong": MONG, "dat": True, "ly_do": []}
    assert (anh["thieu"], anh["lac"], anh["khoa_hong"], anh["o_rong"]) == ([], [], [], [])
    dem = Counter(f"{_chu(d['tab'])}|{d['ky']}" for d in anh["dong"])
    assert dict(dem) == TAB_KY
    f = {}
    for d in anh["dong"]:
        f[int(d["ky"])] = f.get(int(d["ky"]), Decimal(0)) + Decimal(str(d["F"] or 0))
    assert f == {k: Decimal(v) for k, v in F_KY.items()}
    tong = {(_chu(r["tab"]), int(r["ky"])): (int(r["so_hang"]), Decimal(str(r["tong_F"])))
            for r in anh["phu"]["tong_ky"]["dong"]}
    assert sum(v[0] for v in tong.values()) == MONG
    assert sum(v[1] for v in tong.values()) == sum(Decimal(v) for v in F_KY.values())
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM
    assert len({int(d["dong_sheet"]) for d in anh["dong"]}) == MONG          # khoá ⛔ trùng
    assert sum(1 for d in anh["dong"] if int(d["dong_sheet"]) >= 100000) == 2520   # PIT +100000
    assert sum(1 for d in anh["dong"] if _chu(d["le"]) == "#N/A") == Y.MONG_LE_NA == 1   # Đ3 mẫu số > 0
    assert sum(1 for d in anh["dong"] if d["F"] is not None and Decimal(str(d["F"])) % 1 != 0) == 9   # số lẻ có thật


# ══ Y25-B2 · PII ═════════════════════════════════════════════════════════

def test_Y25_B2_anh_0_cot_rieng_tu_va_9_o_H_so_tai_khoan_bi_CHE_ve_R():
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
    assert h["R"] == Y.MONG_H_R == 9 and set(h) <= {None, "R", "Thanh toán (Regular)"}   # Đ3: mẫu số > 0
    for d in anh["dong"]:                                        # ⛔ ô chữ nào ≥ 6 chữ số liền
        for c in Y.CHU:
            s = _chu(d[c])
            assert s is None or not any(len(x) >= 6 for x in "".join(ch if ch.isdigit() else " " for ch in s).split())


def test_Y25_B2_so_tk_tran_va_dang_R_pipe_deu_bi_che_va_khong_in_ra(tmp_path):
    tho = _luoi(_doc(ANH))
    v = tho["tabs"][0]["values"]
    v[0][5] = "987654321"                                        # số trần
    v[1][5] = "R | 123456789_ABC VND_DONVI"                       # dạng DT6
    ra = tmp_path / "r.json"
    kq = _chay("hr_ledger_2025", _ghi(tmp_path / "t.json", tho), "--mong", MONG, "--ra", ra)
    txt = ra.read_text(encoding="utf-8")
    assert "987654321" not in txt and "123456789" not in txt and "987654321" not in kq.stdout + kq.stderr
    assert kq.returncode == 1 and "H_che@khác:11/9" in kq.stdout        # che ĐÚNG, nhưng số ô che ≠ mong ⇒ ĐỎ


@pytest.mark.parametrize("chen", ["ten_o_cdt1", "so_tk_la_o_H", "tieu_de_lech"])
def test_Y25_B2_may_quet_co_CA_PHA_va_loi_KHONG_in_gia_tri(chen, tmp_path):
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
    kq = _chay("hr_ledger_2025", _ghi(tmp_path / "t.json", tho), "--mong", MONG, "--ra", tmp_path / "r.json")
    if chen == "tieu_de_lech":
        assert kq.returncode == 2 and len([d for d in kq.stderr.splitlines() if d.startswith("⛔ TỪ CHỐI")]) == 1
    else:
        assert kq.returncode == 1 and ("cdt1_la@" in kq.stdout or "H_la@" in kq.stdout)
    assert bi_mat not in kq.stdout + kq.stderr


# ══ Y25-AC1 ══════════════════════════════════════════════════════════════

def test_Y25_AC1_tai_tao_luoi_tu_anh_ra_DUNG_TUNG_BYTE(tmp_path):
    anh = _doc(ANH)
    ra = tmp_path / "r.json"
    kq = _chay("hr_ledger_2025", _ghi(tmp_path / "t.json", _luoi(anh)), "--mong", MONG, "--ra", ra)
    assert kq.returncode == 0 and "[ĐẠT]" in kq.stdout, (kq.stdout[-600:], kq.stderr[-400:])
    assert ra.read_bytes() == ANH.read_bytes()


def test_Y25_AC1_cong_DO_khi_thieu_hang_doi_PS_Co_hay_so_hang_mong(tmp_path):
    tho = _luoi(_doc(ANH))
    tho["tabs"][1]["values"].pop(0)                              # PIT mất một hàng 2025-10 (hàng đầu của tab là kỳ 10)
    kq = _chay("hr_ledger_2025", _ghi(tmp_path / "t.json", tho), "--mong", MONG - 1, "--ra", tmp_path / "r.json")
    assert kq.returncode == 1 and "tab_ky@PIT:202510:1222/1223" in kq.stdout
    tho = _luoi(_doc(ANH))
    tho["tabs"][0]["values"][0][3] = 1                           # PS Có đổi ⇒ Σ kỳ lệch
    kq = _chay("hr_ledger_2025", _ghi(tmp_path / "t2.json", tho), "--mong", MONG, "--ra", tmp_path / "r2.json")
    assert kq.returncode == 1 and "F_ky@" in kq.stdout


def test_Y25_AC1_NA_o_LE_dem_hai_chieu_va_so_le_bi_cat_la_DO(tmp_path):
    tho = _luoi(_doc(ANH))
    for h in tho["tabs"][0]["values"]:                           # bỏ `#N/A` ⇒ 0 ≠ mong 1
        if h[8] == "#N/A":
            h[8] = "VVOH"
    kq = _chay("hr_ledger_2025", _ghi(tmp_path / "a.json", tho), "--mong", MONG, "--ra", tmp_path / "r.json")
    assert kq.returncode == 1 and "le_NA@khác:0/1" in kq.stdout
    tho = _luoi(_doc(ANH))
    n = 0
    for h in tho["tabs"][0]["values"]:                           # cắt phần lẻ ⇒ Σ kỳ lệch
        if h[3] != "" and h[3] != int(h[3]) and n < 1:
            h[3] = int(h[3]); n += 1
    kq = _chay("hr_ledger_2025", _ghi(tmp_path / "b.json", tho), "--mong", MONG, "--ra", tmp_path / "r2.json")
    assert n == 1 and kq.returncode == 1 and "F_ky@" in kq.stdout


def test_Y25_AC1_tap_rong_la_TU_CHOI_va_ngay_khong_phai_so_la_TU_CHOI(tmp_path):
    tho = _luoi(_doc(ANH))
    tho["tabs"][1]["values"] = []
    assert _chay("hr_ledger_2025", _ghi(tmp_path / "a.json", tho), "--mong", 1, "--ra", tmp_path / "r.json").returncode == 2
    tho = _luoi(_doc(ANH))
    tho["tabs"][0]["values"][0][0] = ""
    assert _chay("hr_ledger_2025", _ghi(tmp_path / "b.json", tho), "--mong", MONG, "--ra", tmp_path / "r.json").returncode == 2


# ══ Y25-AC3 · khoá ảnh 2024 ═════════════════════════════════════════════

def test_Y25_AC3_anh_2024_DUNG_TUNG_BYTE_sau_khi_mo_rong_khuon(tmp_path):
    import hr_ledger_2024 as Y24
    assert (Y24.MONG_TAB_KY, Y24.MONG_H_R) != (Y.MONG_TAB_KY, Y.MONG_H_R)
    anh = _doc(ANH24)
    assert anh["checksum_noi_dung"] == "4905b28f88819142" and anh["so_dong"] == 1381
    assert len(ANH24.read_bytes()) == 481877                      # BG-227: 481.877 B


# ══ Y25-AC2 · đối chiếu với gl_hr_408 *(đáp án, chỉ để ĐO)* ═══════════════

def _theo_ky_408():
    """408: hàng CÓ NGÀY *(⛔ `ky_suy`)* — số hàng + Σ PS Có theo kỳ."""
    n, f = Counter(), {}
    for d in _doc(DAP_AN / "gl_hr_408.json")["dong"]:
        if _chu(d.get("ky_suy")) is not None:
            continue
        k = int(d["ky"])
        n[k] += 1
        f[k] = f.get(k, Decimal(0)) + Decimal(str(d["F"] or 0))
    return n, f


#: Đo 19/11 — KHỚP hoàn toàn *(số hàng VÀ Σ PS Có)* ở các kỳ này; ⛔ ghi lệch khác ngoài danh sách LỆCH.
KHOP_HOAN_TOAN = (202501, 202503, 202504, 202505, 202507, 202511)
#: LỆCH CÓ TÊN *(kỳ → (hàng nguồn − hàng 408, ΣF nguồn − ΣF 408))* — mỗi dòng một NGUYÊN NHÂN đã đo.
LECH = {202502: (3, Decimal(1760000)),            # nguồn hơn 408 3 hàng *(đo: chỉ kỳ này lệch ΣF ở nhóm 'hàng hơn nhỏ')*
        202506: (1, Decimal(0)), 202508: (1, Decimal(0)), 202509: (1, Decimal(0)),  # nguồn hơn 1 hàng, ΣF bằng nhau ⇒ hàng PS Có rỗng/0
        202510: (1227, Decimal(3369480447)),      # PIT 2025-10 *(1.223 hàng, ΣF 3.369.480.447)* ⛔ ở 408 + 4 hàng NIS
        202512: (-269, Decimal(-413535000))}      # 408 hơn nguồn 269 hàng *(trùng đúng số hàng 2026-01 ở 408)*


def test_Y25_AC2_doi_chieu_voi_408_so_hang_va_tong_PS_Co_theo_ky_lech_CO_TEN():
    anh = _doc(ANH)
    n408, f408 = _theo_ky_408()
    assert sum(n408.values()) == 9410 > 0                        # Đ3: mẫu số (408 có ngày) > 0
    ns, fs = Counter(), {}
    for d in anh["dong"]:
        k = int(d["ky"])
        ns[k] += 1
        fs[k] = fs.get(k, Decimal(0)) + Decimal(str(d["F"] or 0))
    for k in KHOP_HOAN_TOAN:
        assert (ns[k], fs[k]) == (n408[k], f408[k]), k
    for k, (dn, df) in LECH.items():
        assert (ns[k] - n408[k], fs[k] - f408[k]) == (dn, df), k
    assert set(KHOP_HOAN_TOAN) | set(LECH) == set(ns) | {202512}
    assert n408[202601] == 269 and 202601 not in ns             # 2026-01 ở 408: ⛔ có đầu vào ở file nguồn
