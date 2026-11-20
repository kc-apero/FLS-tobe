"""ĐÁP ÁN PLA · PD 414–419 — sáu khuôn `pla1_*` · `pla3_hr_*` · `pla3_pm_hr_*` *(ISP 3.1.2 · Step 31 · DT7 · `WO-261`)*.

⭐ **Vì sao có tệp này.** Bước **H8** *(SO.PLA1 + SO.PLA3 — AP v3.1.2 §3.3.1 PD 414–419 · §3.5.3 D4)* so
engine PLA với đáp án TỪNG Ô. Cần ẢNH đứng yên của sáu tab `[MID] Report I PLA…` *(sổ `[COPY] Report I
General Ledger | P&L Report`, đọc bằng khoá SA chỉ-đọc 20/11)*. Bài này canh **ảnh đã commit** *(⛔ bản
thô — nằm ngoài repo)* và chạy **phép tự kiểm cộng theo VỊ TRÍ ô** ngay trên đáp án.

Bài của ISP *(mục 6)* + AC của `WO-261`:

    DT7-B1  đóng băng + tự kiểm cộng: số ô lệch của chính AS-IS có MONG *(đo lần đầu rồi khai)*
    AC-1    sáu ảnh *(⛔ ba — công cụ đóng băng MỘT lưới ↔ MỘT ảnh; Daily và Y/H/Q/M khác trục)* ≠ rỗng
    AC-2    `PM+HR[i,j] = PLA1[i,j] + HR[i,j]` — đột biến 1 ô ⇒ ĐỎ *(hàm `tu_kiem` nhận ảnh làm đối số)*
    AC-3    mẫu số tách nhãn: ô so được · `0=0=0` · có số thật *(bia `H7-R1-02`: 835/888 giấu 619 ô `0=0`)*
    AC-4    dải ngày Daily + kỳ Y/H/Q/M thật; kỳ không có số ⇒ `chua_co_du_lieu` *(ghi tên, ⛔ hoá 0)*
    AC-5    hàng KPI ⇒ đóng băng, đếm RIÊNG, ⛔ trộn vào số ô khớp
    AC-6    ô ⛔ số *(`-`)* ghi NGUYÊN chuỗi, đếm THEO CỘT, ghim phân bố; lời lỗi ⛔ in giá trị ô

⭐ **Số đo 20/11 *(mỗi số đếm MỘT vật, Đ4)*** — xem hằng bên dưới *(nhãn cạnh mỗi số)*.
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import json
import pathlib
from collections import Counter
from decimal import Decimal

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
DIR_ANH = GOC / "tests" / "fixture" / "dap_an"
EPOCH = datetime.date(1899, 12, 30)

#: tên ảnh → (PD, trục, số khối). Ảnh `pla3_hr_yhqm` *(417)* chỉ có khối `GROUP` — sheet chỉ có 92 hàng.
ANH = {
    "pla1_daily": (414, "ngay", 12), "pla1_yhqm": (415, "ky", 12),
    "pla3_hr_daily": (416, "ngay", 12), "pla3_hr_yhqm": (417, "ky", 1),
    "pla3_pm_hr_daily": (418, "ngay", 12), "pla3_pm_hr_yhqm": (419, "ky", 12),
}
#: Đ5 — `mong` mỗi ảnh. `dong` = ô SỐ ≠ 0 ở hàng HD *(dòng chính thưa)*; `co_so` = số MÃ HD khác nhau có ≥ 1 ô ≠ 0; `o_loi` = ô CHỮ ở hàng HD;
#: `tl_chu` = ô CHỮ ở cột TƯƠNG LAI bị cắt; `truc` = số cột trục giữ; `hd` = hàng HD = khối × 74.
MONG = {
    "pla1_daily":       {"dong": 9694,  "o_loi": 60,  "tl_chu": 0,   "truc": 496, "hd": 888, "co_so": 62},
    "pla1_yhqm":        {"dong": 8844,  "o_loi": 60,  "tl_chu": 0,   "truc": 57,  "hd": 888, "co_so": 62},
    "pla3_hr_daily":    {"dong": 4730,  "o_loi": 60,  "tl_chu": 0,   "truc": 496, "hd": 888, "co_so": 29},
    "pla3_hr_yhqm":     {"dong": 486,   "o_loi": 5,   "tl_chu": 0,   "truc": 57,  "hd": 74,  "co_so": 29},
    "pla3_pm_hr_daily": {"dong": 10343, "o_loi": 60,  "tl_chu": 0,   "truc": 496, "hd": 888, "co_so": 64},
    "pla3_pm_hr_yhqm":  {"dong": 9714,  "o_loi": 240, "tl_chu": 420, "truc": 57,  "hd": 888, "co_so": 64},
}
LE12 = ["GROUP", "SGO2", "SGO1", "HGO6", "BGO2", "CVL", "COR", "SHQ1", "CSM", "CAH", "ASA", "SHQ2"]
#: Mã KPI *(công thức CHÉO hàng, đo từ cột G của tab 418)* — 17 mã × số khối hàng KPI.
MA_KPI = sorted("EBITDA EBIT EBT NP NPC NCF CRO COO COI CRF COF PL2 PL3 PL4 PL6 PL7 PL8".split())
#: Dung sai phép cộng *(mUSD)*: 1e-6 — nguồn là số thực dấu phẩy động *(Sheets)*; khai rõ, ⛔ ngầm.
DUNG_SAI = Decimal("1e-6")
#: ⭐ **MONG tự kiểm** — ĐO lần đầu 20/11 rồi khai *(Đ5)*; mỗi số kèm NHÃN nó đếm gì *(Đ4)*.
#:   `so_duoc`  = ô (hàng HD × cột trục) có ở CẢ BA ảnh *(Daily = 888 × 496)*;
#:   `o_00`     = ô `0 = 0 = 0` · `o_so_that` = ô có ≥ 1 giá trị ≠ 0 *(bia `H7-R1-02`)*;
#:   `lech`     = ô **không-KPI** `|PM+HR − (PLA1+HR)| > 1e-6` — lệch của AS-IS, ⛔ của FLS;
#:   `lech_kpi` = ô **KPI** lệch *(AC-5: tách riêng — KPI tính CHÉO hàng, dấu HR ngược ⇒ cộng vị trí ⛔ áp)*;
#:   `khop_so_that` = ô không-KPI CÓ SỐ THẬT mà khớp — bằng chứng DƯƠNG;
#:   `khong_so_duoc` = ô ở `pm_hr` mà HR ⛔ có khối *(417 chỉ có `GROUP`: 11 khối × 74 mã × 57 kỳ)*.
#:   `hash_lech*` = sha256[:16] của danh sách `(khoá, 3 giá trị, chênh)` đã sắp xếp.
MONG_TU_KIEM = {
    "daily": {"so_duoc": 440448, "o_00": 430084, "o_so_that": 10364, "lech": 4, "lech_kpi": 510,
              "khop_so_that": 2699, "khong_so_duoc": 0,
              "hash_lech": "dbfddf4aebb75ecb", "hash_lech_kpi": "2fe00184c165076e"},
    "yhqm": {"so_duoc": 4218, "o_00": 2639, "o_so_that": 1579, "lech": 0, "lech_kpi": 206,
             "khop_so_that": 1094, "khong_so_duoc": 46398,
             "hash_lech": "4f53cda18c2baa0c", "hash_lech_kpi": "2b1f1041530f34e0"},
}
#: Bốn ô lệch KHÔNG-KPI của Daily — **của AS-IS** *(khối `GROUP`; chênh `PM+HR − (PLA1+HR)` mUSD)*:
#: hai mã `GAC` *(cha của nhóm chi phí chung)* và hai mã `NCFO` *(dòng tiền hoạt động)* ở HAI ngày.
OLECH_DAILY_KHOA = {"GROUP#GAC#45597", "GROUP#GAC#45627", "GROUP#NCFO#45597", "GROUP#NCFO#45627"}
#: Ô chữ `-` ở hàng HD: ĐẾM theo cột. Daily/PLA1·HR·PM+HR: MỘT cột *(cột đầu)* × 60 = 5 mã × 12 khối.
OLOI_COT = {"pla1_daily": (1, 60), "pla1_yhqm": (1, 60), "pla3_hr_daily": (1, 60),
            "pla3_hr_yhqm": (1, 5), "pla3_pm_hr_daily": (1, 60), "pla3_pm_hr_yhqm": (37, 240)}
MA_OLOI = ["AR", "CP1.1 (PL2)", "CP1.2", "CP2", "CP3"]                   # 5 mã `trong` mang `-` gõ tay
#: AC-5 — ô ≠ 0 nằm ở hàng KPI *(đếm RIÊNG khỏi số ô khớp)*.
KPI_O_KHAC_0 = {"pla1_daily": 7493, "pla1_yhqm": 4317, "pla3_hr_daily": 3681, "pla3_hr_yhqm": 80,
                "pla3_pm_hr_daily": 7661, "pla3_pm_hr_yhqm": 4441}
#: AC-4 — cột trục KHÔNG có số nào ở hàng HD *(ghi `chua_co_du_lieu`, ⛔ hoá 0)*.
CHUA_CO = {"pla1_daily": 26, "pla1_yhqm": 10, "pla3_hr_daily": 88, "pla3_hr_yhqm": 33,
           "pla3_pm_hr_daily": 26, "pla3_pm_hr_yhqm": 10}
CHECKSUM = {"pla1_daily": "eb90a8e647a17fa5", "pla1_yhqm": "5dd3a7d44eebc0fc",
            "pla3_hr_daily": "69a427844fa082be", "pla3_hr_yhqm": "15e1cc9e7f76ad02",
            "pla3_pm_hr_daily": "bbb4551aa2051e94", "pla3_pm_hr_yhqm": "160ea879897965b7"}


# ── trợ thủ ───────────────────────────────────────────────────────────────

def _doc(ten: str, thu_muc: pathlib.Path | None = None) -> dict:
    return json.loads(((thu_muc or DIR_ANH) / f"{ten}.json").read_text(encoding="utf-8"),
                      parse_float=Decimal)


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _checksum_lai(anh: dict) -> str:
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def luoi(anh: dict, truc: str) -> tuple[dict, list[dict], list]:
    """Ảnh → (`{(le, ma, trục): Decimal}` thưa, hàng HD, trục theo thứ tự)."""
    o = {(_chu(d["le"]), _chu(d["ma_hd"]), _chu(d[truc])): Decimal(d["gt"]) for d in anh["dong"]}
    hd = [{k: _chu(v) for k, v in r.items()} for r in anh["phu"]["hd"]["dong"]]
    t = anh["phu"]["ngay_truc" if truc == "ngay" else "ky_truc"]["dong"]
    return o, hd, [_chu(r[truc]) for r in t]


def tu_kiem(pm_hr: dict, pla1: dict, hr: dict, truc: str, dung_sai: Decimal = DUNG_SAI) -> dict:
    """Phép cộng THEO VỊ TRÍ: `PM+HR[le, ma, trục] = PLA1[…] + HR[…]` trên mọi (hàng HD × cột trục)
    **có mặt ở CẢ BA** ảnh; hàng ở `pm_hr` mà `hr` ⛔ có khối ⇒ `khong_so_duoc` *(Đ3: ⛔ giả vờ khớp)*.

    Trả: `so_duoc` *(mẫu số)* · `o_00` *(0=0=0)* · `o_so_that` *(≥ 1 giá trị ≠ 0)* · `khong_so_duoc` ·
    `lech` / `lech_kpi` *(list `(khoá, pm_hr, pla1, hr, chênh)` — KPI tách RIÊNG, AC-5)* ·
    `khop_so_that` *(ô có số thật mà khớp — bằng chứng DƯƠNG, ⛔ bị `0=0` làm nhiễu)*."""
    o3, hd3, t3 = luoi(pm_hr, truc)
    o1, hd1, t1 = luoi(pla1, truc)
    oh, hdh, th = luoi(hr, truc)
    assert t3 == t1, "trục PM+HR ≠ trục PLA1"
    khoi_hr = {r["le"] for r in hdh}
    loai = {(r["le"], r["ma"]): r["loai"] for r in hd3}
    kq = {"so_duoc": 0, "o_00": 0, "o_so_that": 0, "khop_so_that": 0, "khong_so_duoc": 0,
          "lech": [], "lech_kpi": []}
    tap_th = set(th)
    for (le, ma), lo in loai.items():
        if le not in khoi_hr:
            kq["khong_so_duoc"] += len(t3)
            continue
        for t in t3:
            if t not in tap_th:
                kq["khong_so_duoc"] += 1
                continue
            a, b, c = o3.get((le, ma, t), Decimal(0)), o1.get((le, ma, t), Decimal(0)), \
                oh.get((le, ma, t), Decimal(0))
            kq["so_duoc"] += 1
            if a == 0 and b == 0 and c == 0:
                kq["o_00"] += 1
                continue
            kq["o_so_that"] += 1
            if abs(a - (b + c)) > dung_sai:
                kq["lech_kpi" if lo == "kpi" else "lech"].append(
                    (f"{le}#{ma}#{t}", str(a), str(b), str(c), str(a - (b + c))))
            elif lo != "kpi":
                kq["khop_so_that"] += 1
    return kq


def bang_tu_kiem(thu_muc: pathlib.Path | None = None) -> dict:
    d, y = {}, {}
    for kieu, truc, hau in (("daily", "ngay", d), ("yhqm", "ky", y)):
        hau.update(tu_kiem(_doc(f"pla3_pm_hr_{kieu}", thu_muc), _doc(f"pla1_{kieu}", thu_muc),
                           _doc(f"pla3_hr_{kieu}", thu_muc), truc))
    return {"daily": d, "yhqm": y}


# ── AC-1 · mong từng ảnh ──────────────────────────────────────────────────

@pytest.mark.parametrize("ten", sorted(ANH))
def test_AC1_anh_ton_tai_va_mong_khai_truoc(ten):
    """Ảnh CÓ MẶT; số dòng chính · hàng HD · cột trục · ô chữ = `MONG` — ⛔ rỗng (Đ3), ⛔ lệch (Đ5)."""
    p = DIR_ANH / f"{ten}.json"
    assert p.is_file(), f"⛔ thiếu ảnh {p.name} — chưa đóng băng PD {ANH[ten][0]}"
    a = _doc(ten)
    m, (pd, truc, n_khoi) = MONG[ten], ANH[ten]
    assert a["bang"] == f"PD.{pd}"
    assert a["so_dong"] == len(a["dong"]) == m["dong"] > 0, "dòng chính ĐẾM *ô số ≠ 0*"
    assert a["phu"]["hd"]["so_dong"] == m["hd"] == n_khoi * 74, "hàng HD = khối × 74 mã ATL"
    assert a["phu"]["le"]["so_dong"] == n_khoi
    assert a["phu"]["ngay_truc" if truc == "ngay" else "ky_truc"]["so_dong"] == m["truc"]
    assert a["phu"]["o_loi"]["so_dong"] == m["o_loi"]
    assert a["phu"]["tuong_lai_chu"]["so_dong"] == (1 if m["tl_chu"] else 0)
    assert sum(_chu(r["so_o"]) if not isinstance(_chu(r["so_o"]), str) else int(_chu(r["so_o"]))
               for r in a["phu"]["tuong_lai_chu"]["dong"]) == m["tl_chu"]
    assert not a["thieu"] and not a["trung"] and not a["o_rong"] and not a["khoa_hong"]
    assert str(a["khong_mang_PII"]).startswith("⛔ KHÔNG mang cột riêng tư"), "soát PII đã chạy"
    assert _checksum_lai(a) == a["checksum_noi_dung"], "checksum ghi ≠ tính lại"
    co_so = {_chu(d["ma_hd"]) for d in a["dong"]}
    assert len(co_so) == m["co_so"], "số MÃ HD (⛔ hàng) khác nhau có ≥ 1 ô ≠ 0"
    van = (DIR_ANH / f"{ten}.json").read_text(encoding="utf-8")
    assert "@" not in van, "ảnh ⛔ mang email"
    # tên cột cấm chỉ được NHẮC ở chính dòng khai soát PII của công cụ *(1 lần)*, ⛔ ở đâu khác
    assert van.lower().count("email address") == str(a["khong_mang_PII"]).lower().count("email address") == 1


def test_AC1_12_khoi_dung_thu_tu_va_417_chi_co_GROUP():
    for ten, (pd, truc, n) in ANH.items():
        le = [r["le"] for r in _doc(ten)["phu"]["le"]["dong"]]
        assert [_chu(x) for x in le] == (LE12 if n == 12 else ["GROUP"]), ten


# ── AC-4 · trục ──────────────────────────────────────────────────────────

def test_AC4_truc_ngay_lien_tuc_2024_10_20_den_2026_02_27():
    for ten in ("pla1_daily", "pla3_hr_daily", "pla3_pm_hr_daily"):
        t = [(int(_chu(r["ngay"])), _chu(r["ngay_iso"]), _chu(r["trang_thai"]))
             for r in _doc(ten)["phu"]["ngay_truc"]["dong"]]
        assert [x[0] for x in t] == list(range(45585, 45585 + 496)), ten
        assert t[0][1] == "2024-10-20" and t[-1][1] == "2026-02-27", (t[0], t[-1])
        assert (EPOCH + datetime.timedelta(days=t[-1][0])).isoformat() == "2026-02-27"


def test_AC4_truc_ky_57_cot_2024_2026_va_chua_co_du_lieu_ghi_ten():
    nam = [str(y) for y in (2024, 2025, 2026)]
    mong_ky = [k for y in nam for k in (
        [y] + [f"{y}H{h}" for h in (1, 2)] + [f"{y}Q{q}" for q in range(1, 5)]
        + [f"{y}M{m:02d}" for m in range(1, 13)])]
    for ten in ("pla1_yhqm", "pla3_hr_yhqm", "pla3_pm_hr_yhqm"):
        t = _doc(ten)["phu"]["ky_truc"]["dong"]
        assert [_chu(r["ky"]) for r in t] == mong_ky, ten
        assert {_chu(r["trang_thai"]) for r in t} <= {"co_so", "chua_co_du_lieu"}


# ── AC-2/AC-3 · tự kiểm cộng theo VỊ TRÍ ô ────────────────────────────────

def _h(xs: list) -> str:
    return hashlib.sha256(json.dumps(sorted(xs)).encode()).hexdigest()[:16]


@pytest.mark.parametrize("kieu", ["daily", "yhqm"])
def test_AC2_AC3_tu_kiem_cong_so_o_lech_AS_IS_dung_mong(kieu):
    """Số ô lệch của chính AS-IS = `MONG_TU_KIEM`; mẫu số tách nhãn; `so_duoc` = `o_00` + `o_so_that`."""
    kq = bang_tu_kiem()[kieu]
    m = MONG_TU_KIEM[kieu]
    assert kq["so_duoc"] == m["so_duoc"] > 0, "mẫu số ≠ 0 (Đ3)"
    assert kq["so_duoc"] == kq["o_00"] + kq["o_so_that"], "mẫu số phải tách đủ 2 nhãn"
    assert (kq["o_00"], kq["o_so_that"]) == (m["o_00"], m["o_so_that"])
    assert kq["khop_so_that"] == m["khop_so_that"] > 0, "bằng chứng DƯƠNG phải ≠ 0"
    assert (len(kq["lech"]), len(kq["lech_kpi"])) == (m["lech"], m["lech_kpi"])
    assert kq["khong_so_duoc"] == m["khong_so_duoc"]
    assert _h(kq["lech"]) == m["hash_lech"] and _h(kq["lech_kpi"]) == m["hash_lech_kpi"]


def test_AC2_so_o_so_duoc_daily_bang_hang_HD_nhan_cot_ngay():
    kq = bang_tu_kiem()
    assert kq["daily"]["so_duoc"] == 888 * 496                            # 888 hàng HD × 496 ngày
    assert kq["yhqm"]["so_duoc"] + kq["yhqm"]["khong_so_duoc"] == 888 * 57   # 888 hàng × 57 kỳ


def test_AC2_o_lech_AS_IS_khong_KPI_la_GAC_va_NCFO_khoi_GROUP():
    """4 ô lệch không-KPI ở Daily đúng khoá + chênh ≠ 0 *(liệt kê — BG-262 ghi 3 giá trị)*."""
    lech = bang_tu_kiem()["daily"]["lech"]
    assert {x[0] for x in lech} == OLECH_DAILY_KHOA
    assert all(abs(Decimal(x[4])) > DUNG_SAI for x in lech)


@pytest.mark.parametrize("kieu,truc", [("daily", "ngay"), ("yhqm", "ky")])
@pytest.mark.parametrize("chon", ["pm_hr_doi_1_o", "pla1_xoa_1_o", "hr_doi_1_o"])
def test_AC2_dot_bien_1_o_thi_DO(kieu, truc, chon):
    """**Chứng minh ĐỎ** *(Đ5)*: đổi/xoá MỘT ô *(không-KPI, có số thật)* ở một ảnh ⇒ `lech` tăng đúng 1."""
    pm, p1, hr = (_doc(f"pla3_pm_hr_{kieu}"), _doc(f"pla1_{kieu}"), _doc(f"pla3_hr_{kieu}"))
    goc = len(tu_kiem(pm, p1, hr, truc)["lech"])
    anh = {"pm_hr_doi_1_o": pm, "pla1_xoa_1_o": p1, "hr_doi_1_o": hr}[chon]
    loai = {(_chu(r["le"]), _chu(r["ma"])): _chu(r["loai"]) for r in pm["phu"]["hd"]["dong"]}
    o_gt = {(_chu(d["le"]), _chu(d["ma_hd"]), _chu(d[truc])): d for d in pm["dong"]}
    # ô không-KPI, ≠ 0 và KHỚP ở cả 3 ảnh *(để đột biến là nguyên nhân DUY NHẤT)*
    tk = tu_kiem(pm, p1, hr, truc)
    bad = {x[0] for x in tk["lech"]}
    tu_chon = next(d for d in anh["dong"]
                   if loai[(_chu(d["le"]), _chu(d["ma_hd"]))] in ("la", "tong")
                   and f"{_chu(d['le'])}#{_chu(d['ma_hd'])}#{_chu(d[truc])}" not in bad
                   and (_chu(d["le"]), _chu(d["ma_hd"]), _chu(d[truc])) in o_gt)
    if chon == "pla1_xoa_1_o":
        anh["dong"].remove(tu_chon)
    else:
        tu_chon["gt"] = str(Decimal(tu_chon["gt"]) + Decimal("0.5"))
    assert len(tu_kiem(pm, p1, hr, truc)["lech"]) == goc + 1, "đột biến 1 ô PHẢI làm cổng ĐỎ"


def test_AC2_dung_sai_khai_ro_va_dot_bien_duoi_dung_sai_khong_do():
    assert DUNG_SAI == Decimal("1e-6")
    pm, p1, hr = (_doc("pla3_pm_hr_daily"), _doc("pla1_daily"), _doc("pla3_hr_daily"))
    goc = len(tu_kiem(pm, p1, hr, "ngay")["lech"])
    d = next(r for r in pm["dong"] if _chu(r["ma_hd"]) == "GI" and _chu(r["le"]) == "SGO2")
    d["gt"] = str(Decimal(d["gt"]) + Decimal("1e-9"))          # dưới dung sai ⇒ ⛔ đỏ
    assert len(tu_kiem(pm, p1, hr, "ngay")["lech"]) == goc


# ── AC-5 · KPI đếm riêng ──────────────────────────────────────────────────

@pytest.mark.parametrize("ten", sorted(ANH))
def test_AC5_KPI_khai_rieng_ma_kpi_va_dem(ten):
    a = _doc(ten)
    n_khoi = ANH[ten][2]
    hd = [{k: _chu(v) for k, v in r.items()} for r in a["phu"]["hd"]["dong"]]
    assert sorted({r["ma"] for r in hd if r["loai"] == "kpi"}) == MA_KPI
    assert sum(1 for r in hd if r["loai"] == "kpi") == 17 * n_khoi, "17 mã KPI × khối"
    assert {r["loai"] for r in hd} == {"la", "tong", "kpi", "trong"}, "mã chưa khai loại ⇒ `?`"
    kp = {(r["le"], r["ma"]) for r in hd if r["loai"] == "kpi"}
    n = sum(1 for d in a["dong"] if (_chu(d["le"]), _chu(d["ma_hd"])) in kp)
    assert n == KPI_O_KHAC_0[ten] > 0, "ô ≠ 0 ở hàng KPI — đếm RIÊNG, ⛔ trộn vào số ô khớp"


def test_AC5_o_KPI_khong_lot_vao_danh_sach_lech_khong_KPI():
    kq = bang_tu_kiem()
    for k in ("daily", "yhqm"):
        assert not {x[0].split("#")[1] for x in kq[k]["lech"]} & set(MA_KPI)
        assert {x[0].split("#")[1] for x in kq[k]["lech_kpi"]} <= set(MA_KPI)


# ── AC-4 (tiếp) · AC-6 · checksum ─────────────────────────────────────────

@pytest.mark.parametrize("ten", sorted(ANH))
def test_AC4_cot_chua_co_du_lieu_dem_dung_va_khong_hoa_0(ten):
    a = _doc(ten)
    truc = ANH[ten][1]
    ts = a["phu"]["ngay_truc" if truc == "ngay" else "ky_truc"]["dong"]
    chua = {_chu(r[truc]) for r in ts if _chu(r["trang_thai"]) == "chua_co_du_lieu"}
    assert len(chua) == CHUA_CO[ten] > 0
    assert not {_chu(d[truc]) for d in a["dong"]} & chua, "cột `chua_co_du_lieu` ⛔ có ô ≠ 0"


@pytest.mark.parametrize("ten", sorted(ANH))
def test_AC6_o_loi_giu_NGUYEN_chuoi_dem_theo_cot_va_chi_o_5_ma(ten):
    a = _doc(ten)
    truc = ANH[ten][1]
    dong = a["phu"]["o_loi"]["dong"]
    assert {_chu(r["gia"]) for r in dong} == {"-"}, "tập ⛔ số = {`-`} — thêm `#REF!`/`#N/A` ⇒ ĐỎ"
    assert {_chu(r["ma_hd"]) for r in dong} == set(MA_OLOI)
    cot = Counter(_chu(r[truc]) for r in dong)
    assert (len(cot), sum(cot.values())) == OLOI_COT[ten]
    assert not {(_chu(d["le"]), _chu(d["ma_hd"]), _chu(d[truc])) for d in a["dong"]} & \
        {(_chu(r["le"]), _chu(r["ma_hd"]), _chu(r[truc])) for r in dong}, "ô chữ ⛔ hoá số"


def test_AC6_419_cat_420_o_chu_tuong_lai_ghi_phan_bo():
    a = _doc("pla3_pm_hr_yhqm")
    assert [(_chu(r["gia"]), int(_chu(r["so_o"]))) for r in a["phu"]["tuong_lai_chu"]["dong"]] \
        == [("-", 420)]


@pytest.mark.parametrize("ten", sorted(ANH))
def test_AC1_checksum_ghim(ten):
    assert _doc(ten)["checksum_noi_dung"] == CHECKSUM[ten]


def test_AC6_loi_tu_choi_khong_in_gia_tri_o():
    """Lời lỗi của khuôn ⛔ in giá trị ô *(`DT5-R1-02`)* — dùng chung `_an_toan` của `_cfa1`."""
    import importlib.util
    import sys
    p = GOC / "tools" / "khuon_dong_bang" / "_pla.py"
    sp = importlib.util.spec_from_file_location("kdb_pla_test", p)
    m = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = m
    sp.loader.exec_module(m)
    ngu = "Nguyen Van A nguoi.dung@vi-du.vn"
    luoi_x = [[""] * 8 for _ in range(7)]
    luoi_x[6] = ["GROUP", "HDO", "HD Original"] + [""] * 5
    luoi_x[6][0] = ngu
    with pytest.raises(ValueError) as e:
        m.dung_cay(luoi_x, m.LE12, m.LOAI_MA)
    assert "nguoi.dung" not in str(e.value) and "Nguyen" not in str(e.value)


def test_AC7_cong_cu_chung_va_anh_cu_giu_tung_byte():
    """⛔ sửa công cụ chung / ảnh cũ: sha ghim *(cùng bảng `SHA_GIU` của `test_dap_an_cfa1`)*."""
    from tests.du_lieu import test_dap_an_cfa1 as C
    for ten, sha in C.SHA_GIU.items():
        got = hashlib.sha256((GOC / "tests" / "fixture" / f"{ten}.json").read_bytes()).hexdigest()[:16]
        assert got == sha, (ten, got, sha)
    assert _doc("pla1_daily")["checksum_noi_dung"] != _doc("pla3_hr_daily")["checksum_noi_dung"]
