"""ĐẦU VÀO PLA cho H8 — `gl_pl_dau_vao` (GL sổ P&L, cột `DE`) + `hr_pl_dau_vao` (HR For PL Report, cột `BM`)
*(ISP 3.1.2 · DT7b · `WO-281` AC-1…AC-5)*.

    PLV-B1  ảnh GL thật: 7.883 hàng liên tục 10…7892 · số hàng MỖI kỳ có MONG · `DE = DATE(AH)` khớp 7.574 + 309 `#NUM!`
    PLV-B2  ảnh HR thật: 13.356 hàng · `BM = f(BK, BL)` khớp 13.356 · số hàng MỖI kỳ BM có MONG
    PLV-B3  PII: 0 cột B/C/H/G…O · 0 `@` · tập đóng P/V/LE/HD · ca phá cổng ĐỎ hai chiều
    PLV-AC2 tái tạo lưới thô từ ảnh ⇒ đúng TỪNG BYTE · mở rộng `gl_406_dau_vao` *(0 lệch dong_sheet·D·E·F·R·kỳ)*
    PLV-AC4 đối chiếu (CHỈ ĐO) Σ(BR−BS) theo (mã HD, ngày DE) ↔ ô `la` khối GROUP của `pla1_daily` (414);
            Σ(BA−BB) theo (mã HD, BM) ↔ `pla3_hr_daily` (416) — mẫu số TRƯỚC, lệch CÓ TÊN
    PLV-OLD mọi ảnh cũ ⛔ đổi byte
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from collections import Counter
from decimal import Decimal

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
FX = GOC / "tests" / "fixture"
ANH_GL = FX / "dau_vao" / "gl_pl_dau_vao.json"
ANH_HR = FX / "dau_vao" / "hr_pl_dau_vao.json"
EPOCH = datetime.date(1899, 12, 30)
sys.path.insert(0, str(GOC / "tools" / "khuon_dong_bang"))
import gl_pl_dau_vao as G  # noqa: E402
import hr_pl_dau_vao as H  # noqa: E402

MONG_GL = 7883
MONG_HR = 13356
CHECKSUM_GL = "725fab7b8140c6af"
CHECKSUM_HR = "71b0434574bba96f"
#: AC-4 — đo 22/11, ghim *(Đ5)*.
MONG_AC4 = {
    "gl": {"mau_so_o_dap_an": 371, "mau_so_o_input": 446, "o_so": 372, "o_khong_zero": 371, "khop": 371,
           "lech": [], "ngoai_nhan": 360, "ngay_ngoai_luoi": 74},
    "hr": {"mau_so_o_dap_an": 119, "mau_so_o_input": 127, "o_so": 127, "o_khong_zero": 119, "khop": 119,
           "lech": [], "ngoai_nhan": 0, "ngay_ngoai_luoi": 0}}
#: Mọi ảnh cũ: sha256 TỪNG BYTE *(`git hash` lúc nền `2799bbe`)*.
SHA_CU = {
    "dap_an/gl_406_dau_vao.json":
        "bf4a40aafa405954031b7d0f9a25ce76ca0e4da4a7eda48faf10615913084f82",
    "dap_an/gl_cf_dau_vao.json":
        "e3f46e6c146db88e45414aa8b976b026b3b6e090874b2c7e42747bbebf57bad5",
    "dau_vao/hr_ledger_2024.json":
        "919ef27e3234ad1a16cf6c2972c25ff53e64ad2ee37f8328be37bb10d33762aa",
    "dau_vao/hr_ledger_2025.json":
        "2d65c4250c5e49ea61cbbe11e2a805933da465a8a77e557994c1c1179e2627a3",
    "dap_an/pla1_daily.json":
        "bf34c43bea6993b39958c95cd230613e876c755265d835281af89850f1fd9595",
    "dap_an/pla3_hr_daily.json":
        "2c6e6816f96e6c1f8aedcd5118638448cd3b1cf58b70f301acb7a0d1dac0b426",
}


def _doc(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _chay(*doi_so):
    return subprocess.run([sys.executable, str(TOOL), *map(str, doi_so)], cwd=GOC,
                          env=dict(os.environ, PYTHONUTF8="1"), capture_output=True, text=True, timeout=300)


def _checksum_lai(anh):
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {})) for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _so(v):
    if v is None:
        return ""
    d = Decimal(str(v))
    return int(d) if d == d.to_integral_value() else float(d)


def _o(v):
    """Ô ảnh → ô lưới thô *(chuỗi chữ số ⇒ số · `{chu}` ⇒ chuỗi · null ⇒ rỗng)*."""
    if v is None:
        return ""
    return v["chu"] if isinstance(v, dict) else _so(v)


def luoi(anh, cot_tho, dau=10):
    return {"spreadsheet_id": "x", "nguon": anh["nguon"], "doc_luc": anh["ngay_dong_bang"],
            "cach_doc": anh["cach_doc"], "dong_dau_sheet": dau, "cot": list(cot_tho),
            "values": [[_o(d[c]) for c in cot_tho] for d in anh["dong"]]}


def _ky(serial):
    d = EPOCH + datetime.timedelta(days=int(serial))
    return d.year * 100 + d.month


@pytest.fixture(scope="module")
def gl():
    return _doc(ANH_GL)


@pytest.fixture(scope="module")
def hr():
    return _doc(ANH_HR)


# ── PLV-B1 · GL ────────────────────────────────────────────────────────────

def test_B1_gl_anh_that(gl):
    assert ANH_GL.is_file()
    assert gl["so_dong"] == MONG_GL and len(gl["dong"]) == MONG_GL        # Đ3: mẫu số > 0
    assert gl["cong"]["dat"] if "dat" in gl.get("cong", {}) else True
    assert gl["thieu"] == [] and gl["trung"] == [] and gl["khoa_hong"] == [] and gl["o_rong"] == []
    assert [int(_chu(d["dong_sheet"])) for d in gl["dong"]] == list(range(10, 10 + MONG_GL))
    assert gl["checksum_noi_dung"] == CHECKSUM_GL == _checksum_lai(gl)
    assert gl["cot"] == list(G.COT) and gl["khoa"] == "dong_sheet"


def test_B1_gl_hang_moi_ky(gl):
    """Số hàng mỗi kỳ cột A = `phan_bo_ky` ± 4 kỳ lệch có tên *(GỌI 406 — ⛔ chép)*."""
    thuc = Counter(_ky(_chu(d["A"])) for d in gl["dong"])
    mong = {k: G._k406.LECH_CO_TEN.get(k, v) for k, v in G._k406._phan_bo_ledger().items()}
    assert {k: v for k, v in thuc.items()} == {k: v for k, v in mong.items() if v}
    assert sum(thuc.values()) == MONG_GL and len(thuc) == 20


def test_B1_gl_DE_tai_dung_tu_AH(gl):
    """Bằng chứng DƯƠNG: `DE = DATE(AH//100, AH%100, 1)` — 7.574 khớp + 309 `#NUM!` ⇔ 309 `AH` rỗng + 0 lệch."""
    khop = loi = lech = ah_rong = 0
    for d in gl["dong"]:
        ah, de = d["AH"], d["DE"]
        if ah is None:
            ah_rong += 1
            loi += isinstance(de, dict) and de["chu"].startswith("#NUM!")
            continue
        khop += (de == str(G.de_tu_ah(Decimal(ah)))) if not isinstance(de, dict) else 0
        lech += isinstance(de, dict) or de != str(G.de_tu_ah(Decimal(ah)))
    assert (khop, loi, lech, ah_rong) == (7574, 309, 0, 309)
    assert G.MONG_AH_LA == (5487, 5556, 5557, 5634, 5712, 7098)
    assert [d["dong_sheet"] for d in gl["dong"] if d["AH"] is not None
            and not 202000 < int(d["AH"]) < 203000] == [str(x) for x in G.MONG_AH_LA]


def test_B1_gl_DE_phan_bo(gl):
    de = Counter(_chu(d["DE"]).split(" ")[0] if isinstance(d["DE"], dict) else d["DE"] for d in gl["dong"])
    assert de["#NUM!"] == 309 and sum(de.values()) == MONG_GL
    ngay_1 = [(EPOCH + datetime.timedelta(days=int(k))).day for k in de if k != "#NUM!" and 45000 < int(k) < 50000]
    assert ngay_1 and set(ngay_1) == {1}                                   # mọi DE hợp lệ là NGÀY MÙNG 1
    assert gl["cong"]["loi_theo_cot"]["DE"] if "loi_theo_cot" in gl.get("cong", {}) else True


# ── PLV-B2 · HR ────────────────────────────────────────────────────────────

def test_B2_hr_anh_that(hr):
    assert ANH_HR.is_file()
    assert hr["so_dong"] == MONG_HR and len(hr["dong"]) == MONG_HR
    assert hr["thieu"] == [] and hr["trung"] == [] and hr["khoa_hong"] == []
    assert [int(_chu(d["dong_sheet"])) for d in hr["dong"]] == list(range(10, 10 + MONG_HR))
    assert hr["checksum_noi_dung"] == CHECKSUM_HR == _checksum_lai(hr)
    assert hr["cot"] == list(H.COT) and hr["khoa"] == "dong_sheet"


def test_B2_hr_BM_tai_dung_tu_BK_BL(hr):
    """`BM = if(BL=2024 ∧ BK∈{11,12}, DATE(BL,BK,1), DATE(2025,BK,1))` ở 13.356/13.356 hàng; BM ⛔ theo cột A."""
    khop = a_khac = co_a = 0
    for d in hr["dong"]:
        bk, bl, bm = int(d["BK"]), int(d["BL"]), int(d["BM"])
        nam = bl if (bl == 2024 and bk in (11, 12)) else 2025
        khop += bm == G.date_sheets(nam, bk, 1)
        if d["A"] is not None:
            co_a += 1
            a_khac += _ky(d["A"]) != _ky(bm)
    assert khop == MONG_HR
    assert (co_a, a_khac) == (10785, 7578)                                 # BM ≠ tháng của A ở 7.578/10.785
    assert sum(1 for d in hr["dong"] if d["A"] is None) == 2571


def test_B2_hr_hang_moi_ky_BM(hr):
    thuc = Counter(_ky(d["BM"]) for d in hr["dong"])
    assert dict(thuc) == H.MONG_KY_BM_THAT and sum(thuc.values()) == MONG_HR
    ph = {int(_chu(r["ky_bm"])): int(r["so_hang"]) for r in hr["phu"]["tong_ky"]["dong"]}
    assert ph == H.MONG_KY_BM_THAT


# ── PLV-B3 · PII + ca phá ──────────────────────────────────────────────────

@pytest.mark.parametrize("anh,cot", [("gl", G.COT), ("hr", H.COT)])
def test_B3_pii(anh, cot, gl, hr):
    a = gl if anh == "gl" else hr
    txt = (ANH_GL if anh == "gl" else ANH_HR).read_text(encoding="utf-8")
    cell = json.dumps(a["dong"] + [r for b in a["phu"].values() for r in b["dong"]], ensure_ascii=False)
    assert "@" not in txt and a["khong_mang_PII"].startswith("⛔ KHÔNG mang cột riêng tư")
    assert set(a["dong"][0]) == {"thu_tu", "dong_sheet", *cot}
    for cam in ("Số chứng từ", "Diễn giải", "Email", "Payee"):
        assert cam not in cell
    assert not any(len(s) >= 6 and s.isdigit() for d in a["dong"] for c in ("P", "V") for s in [_chu(d[c]) or ""])


def _thu_cong(tmp, tho, ten, mong, ra="ra.json"):
    p = pathlib.Path(tmp) / "tho.json"
    p.write_text(json.dumps(tho, ensure_ascii=False), encoding="utf-8")
    r = _chay(ten, p, "--mong", mong, "--ra", pathlib.Path(tmp) / ra)
    return r


@pytest.fixture(scope="module")
def tho_gl(gl):
    return luoi(gl, G.COT_THO[1:] and ("dong_sheet", *G.COT))


@pytest.fixture(scope="module")
def tho_hr(hr):
    return luoi(hr, ("dong_sheet", *H.COT))


def test_AC2_tai_tao_dung_tung_byte(tho_gl, tho_hr):
    with tempfile.TemporaryDirectory() as t:
        for ten, tho, mong, anh in (("gl_pl_dau_vao", tho_gl, MONG_GL, ANH_GL), ("hr_pl_dau_vao", tho_hr, MONG_HR, ANH_HR)):
            r = _thu_cong(t, tho, ten, mong, ra=f"{ten}.json")
            assert r.returncode == 0, r.stdout[-400:] + r.stderr[-400:]
            assert (pathlib.Path(t) / f"{ten}.json").read_bytes() == anh.read_bytes()


def _ca_pha(tho, mong, ten, sua):
    t2 = copy.deepcopy(tho)
    sua(t2)
    with tempfile.TemporaryDirectory() as t:
        r = _thu_cong(t, t2, ten, mong)
    return r.returncode


def _i(tho, c):
    return tho["cot"].index(c)


def test_B3_ca_pha_gl_do(tho_gl):
    """Mỗi đột biến 1 ô ⇒ cổng ĐỎ *(exit ≠ 0)*; trả nguyên ⇒ xanh *(đã ở AC2)*."""
    def DE(t):
        t["values"][0][_i(t, "DE")] += 1                                   # DE ≠ DATE(AH)
    def AH(t):
        t["values"][5][_i(t, "AH")] = 202411                               # AH đổi, DE giữ
    def P_la(t):
        t["values"][3][_i(t, "P")] = "NGUYEN VAN A"                        # chuỗi lạ ở LE
    def V_la(t):
        t["values"][3][_i(t, "V")] = "0912345678"
    def rong(t):
        i = next(i for i, r in enumerate(t["values"]) if r[_i(t, "DE")] == "" or isinstance(r[_i(t, "DE")], str))
        t["values"][i][_i(t, "DE")] = 46000                                # #NUM! thành số
    def cot_cam(t):
        t["cot"][_i(t, "P")] = "Diễn giải"
    for f in (DE, AH, P_la, V_la, rong):
        assert _ca_pha(tho_gl, MONG_GL, "gl_pl_dau_vao", f) != 0, f.__name__


def test_B3_ca_pha_hr_do(tho_hr):
    def BM(t):
        t["values"][0][_i(t, "BM")] += 31
    def BK(t):
        t["values"][7][_i(t, "BK")] = 12 if t["values"][7][_i(t, "BK")] != 12 else 1
    def BL(t):
        t["values"][20][_i(t, "BL")] = 2024 if t["values"][20][_i(t, "BL")] != 2024 else 2025
    def P_la(t):
        t["values"][3][_i(t, "P")] = "NGUYEN VAN A"
    def A_lech(t):
        i = next(i for i, r in enumerate(t["values"]) if r[_i(t, "A")] == "")
        t["values"][i][_i(t, "A")] = 45700                                 # A có mà BA/BB rỗng
    for f in (BM, BK, BL, P_la, A_lech):
        assert _ca_pha(tho_hr, MONG_HR, "hr_pl_dau_vao", f) != 0, f.__name__


# ── PLV-AC2 · mở rộng 406 ───────────────────────────────────────────────────

def test_AC2_mo_rong_406_khong_lech(gl):
    """`gl_pl_dau_vao` đọc CÙNG khoá hàng với `gl_406_dau_vao`: dong_sheet · D · E · F · R · kỳ(A) — 0 lệch."""
    c = _doc(FX / "dap_an" / "gl_406_dau_vao.json")
    assert len(c["dong"]) == len(gl["dong"]) > 0
    lech = 0
    for a, b in zip(c["dong"], gl["dong"]):
        lech += (a["dong_sheet"] != b["dong_sheet"] or a["D"] != b["D"] or a["E"] != b["E"] or a["F"] != b["F"]
                 or a["itl_id"] != b["R"] or int(a["ky"]) != _ky(b["A"]))
    assert lech == 0


@pytest.mark.parametrize("rel", sorted(SHA_CU))
def test_OLD_anh_cu_dung_tung_byte(rel):
    assert hashlib.sha256((FX / rel).read_bytes()).hexdigest() == SHA_CU[rel]


# ── PLV-AC4 · đối chiếu 414/416 (CHỈ ĐO) ─────────────────────────────────────

DUNG_SAI = Decimal("1e-6")


def _dap_an(ten):
    a = _doc(FX / "dap_an" / f"{ten}.json")
    hd = {_chu(r["ma"]): _chu(r["ten"]) for r in a["phu"]["hd"]["dong"] if _chu(r["le"]) == "GROUP"
          and _chu(r["loai"]) == "la"}
    o = {(_chu(d["ma_hd"]), int(d["ngay"])): Decimal(d["gt"]) for d in a["dong"]
         if _chu(d["le"]) == "GROUP" and _chu(d["ma_hd"]) in hd}
    ngay = {int(_chu(r["ngay"])) for r in a["phu"]["ngay_truc"]["dong"]}
    return hd, o, ngay


def doi_chieu(anh, cot_ngay, cot_no, cot_co, ten_pd):
    """Σ(nợ−có) theo (mã HD, ngày) trên ảnh đầu vào ↔ ô `la` GROUP của đáp án — ĐẾM mẫu số TRƯỚC (Đ3/Đ4)."""
    hd, o, ngay = _dap_an(ten_pd)
    nhan = {f"{m} | {t}".casefold(): m for m, t in hd.items()}
    s: dict = {}
    ngoai_nhan = 0
    for d in anh["dong"]:
        m = nhan.get((_chu(d["V"]) or "").casefold())
        n = d[cot_ngay]
        if m is None or isinstance(n, dict):
            ngoai_nhan += 1
            continue
        k = (m, int(n))
        s[k] = s.get(k, Decimal(0)) + (Decimal(d[cot_no] or 0) - Decimal(d[cot_co] or 0))
    khoa = {k for k in (set(s) | set(o)) if k[1] in ngay}
    kq = {"mau_so_o_dap_an": len(o), "mau_so_o_input": len(s), "o_so": len(khoa), "o_khong_zero": 0,
          "khop": 0, "lech": [], "ngoai_nhan": ngoai_nhan, "ngay_ngoai_luoi": sum(1 for k in s if k[1] not in ngay)}
    for k in sorted(khoa):
        a, b = s.get(k, Decimal(0)), o.get(k, Decimal(0))
        if a == 0 and b == 0:
            continue
        kq["o_khong_zero"] += 1
        if abs(a - b) <= DUNG_SAI:
            kq["khop"] += 1
        else:
            kq["lech"].append(f"{k[0]}#{k[1]}")
    return kq


def test_AC4_mau_so_khac_rong():
    hd, o, ngay = _dap_an("pla1_daily")
    assert len(hd) == 40 and len(o) > 0 and len(ngay) == 496               # Đ3 — tập khác rỗng


def test_AC4_gl_vs_414(gl):
    # GL: Σ(BR−BS) theo (mã HD ở V, ngày DE) — DE là số *(chuỗi chữ số)* hoặc `#NUM!` *(bỏ)*.
    kq = doi_chieu(gl, "DE", "BR", "BS", "pla1_daily")
    assert kq["o_khong_zero"] > 0
    assert kq == MONG_AC4["gl"], kq


def test_AC4_hr_vs_416(hr):
    kq = doi_chieu(hr, "BM", "BA", "BB", "pla3_hr_daily")
    assert kq["o_khong_zero"] > 0
    assert kq == MONG_AC4["hr"], kq
