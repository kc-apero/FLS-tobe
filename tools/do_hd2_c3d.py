"""`do_hd2.py --goi WP-C3d` — PARITY HD2 họ PLA *(ISP 3.1.2 · Step 39 · H8 · `WO-277`)*: SO.PLA1 · SO.PLA3 HR ·
SO.PLA3 PM + HR, Daily + Y/H/Q/M ↔ đáp án 414–419 *(DT7, `BG-262`)*.

⭐ **Đầu vào = THƯỢNG NGUỒN, ⛔ đáp án** *(lượt đầu H8 DỪNG đúng luật AC-2 ⇒ DT7b / `BG-282` đóng băng)*:
  · PLA1: `tests/fixture/dau_vao/gl_pl_dau_vao.json` — tab `Report I General Ledger` sổ P&L, 7.883 hàng ·
    `A·D·E·F` → `tinh_gl` *(H1/H4 — BR/BS tính LẠI, cột BR/BS của ảnh chỉ để đối chiếu)* · `P` *(khối LE)* ·
    `V` *(nhãn HD)* · `AH` → ngày ghi nhận **`ky.ngay_ghi_nhan` của C6** *(D4 A; `DE` chỉ để đối chiếu)*.
  · PLA3 HR: `tests/fixture/dau_vao/hr_pl_dau_vao.json` — tab `…Y2025 | For PL Report`, 13.356 hàng · `V` ·
    `BA`/`BB` *(mUSD của tab — tab ⛔ mang E/F nguyên tệ)* · `BK`/`BL` → ngày ghi nhận *(luật năm AS-IS
    của `BM` + C6; `BM` chỉ để đối chiếu)*.
  Config: IX.FX *(`ix_fx.json`)* · IX.HD *(`atl_cay.json`)* · **IX.PER ĐỌC TỪ KHO** *(C6 — ngày đầu trục + luật)*.

Chuỗi *(dùng lại — ⛔ chép)*: `tinh_gl` *(H4)* → `pla.pla_daily` *(= `cfa1_daily` H5 + công thức tab)* →
`pla.pla_pm_hr_daily` *(cộng THEO KHOÁ)* → `pla.pla_yhqm` *(= `cuon_ky` H6 + công thức tab)*.

── PHẠM VI KHỐI *(Đ4 — đếm cái gì)* ──────────────────────────────────────────────────────────────────────────────
  · ĐO ĐƯỢC: PLA1 `GROUP` + 4 khối LE *(`SGO2 SGO1 HGO6 BGO2` — khoá `GL!P`)*; HR `GROUP`; PM+HR `GROUP`.
  · `chua_co_dau_vao` *(CÓ TÊN, ⛔ coi là khớp, ⛔ đoán khoá — orchestrator chốt 22/11)*: PLA1 7 khối CDT
    *(`CVL…ASA` khoá `GL!AD` ⛔ có trong ảnh · `SHQ2` = dư của GROUP − 6 khối ấy)*; HR 4 khối LE *(cộng `HR!BR/BS`
    — ⛔ có trong ảnh)* + 7 khối CDT *(khoá `HR!J` — `DT7B-R1-02`)*; PM+HR 11 khối *(phần HR thiếu)*.
  · `khong_so_duoc`: 417 chỉ có khối `GROUP` ⇒ 11 khối × 74 mã × 57 kỳ = 46.398 ô.
  · `cot_ngoai_truc`: cột đáp án ⛔ nằm trên trục IX.PER *(2024-10-20 — IX.PER kho = 21/10, errata ㉑ ·
    `DT7-R1-07`)*.
── LỚP LỆCH *(Đ5: `mong` khai TRƯỚC — khác ⇒ ĐỎ CẢ HAI CHIỀU)* — xem `MongC3d`.
"""
from __future__ import annotations

import datetime
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

from fls.bao_cao import pla
from fls.bao_cao.cfa import KHOI_TONG, DongCFA, truc_ngay
from fls.bao_cao.gl import DongGL, ThieuTyGia, TienTeNgoaiGL, tinh_gl
from fls.cau_hinh.hd import CayHD
from fls.cau_hinh.ky import LichKy
from fls.oracle.cong_parity import PhanXu
from tools.do_hd2 import GOC, _chu, _so, nap_anh, nap_cay, nap_fx

ANH_GL = GOC / "tests" / "fixture" / "dau_vao" / "gl_pl_dau_vao.json"
ANH_HR = GOC / "tests" / "fixture" / "dau_vao" / "hr_pl_dau_vao.json"
_DA = GOC / "tests" / "fixture" / "dap_an"
TAB = {"pla1_daily": "PM", "pla3_hr_daily": "HR", "pla3_pm_hr_daily": "PMHR",
       "pla1_yhqm": "PM", "pla3_hr_yhqm": "HR", "pla3_pm_hr_yhqm": "PMHR"}
KHOI_LE = ("SGO2", "SGO1", "HGO6", "BGO2")
KHOI_DO = {"PM": (KHOI_TONG,) + KHOI_LE, "HR": (KHOI_TONG,), "PMHR": (KHOI_TONG,)}
#: Dung sai ô *(rtol 0)* — đo 22/11 trên ô khớp: xem `MONG` `max_lech` *(⇒ atol ≥ ×10)*.
ATOL = Decimal("1e-12")
#: Dung sai đối chiếu BR/BS `tinh_gl` ↔ cột BR/BS của ảnh *(chỉ để kiểm feed — ⛔ đầu vào)*.
ATOL_BR = Decimal("1e-15")
_EPOCH = datetime.date(1899, 12, 30)


@dataclass(frozen=True)
class MongC3d:
    """Mong khai TRƯỚC *(Đ4 nhãn · Đ5 hai chiều)*. `None` ⇒ chưa khai ⇒ ĐỎ."""
    so: Mapping[str, Any] | None = None


def mong_c3d_mac_dinh() -> MongC3d:
    from tools.do_hd2_c3d_mong import MONG
    return MongC3d(so=MONG)


@dataclass
class ThanhQuaC3d:
    so: dict[str, Any]
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    luoi: dict[str, pla.KetQuaPLA] = field(default_factory=dict)
    lech: list[dict[str, Any]] = field(default_factory=list)


def nap_nguon() -> tuple:
    return (nap_anh(ANH_GL), nap_anh(ANH_HR), {k: nap_anh(_DA / f"{k}.json") for k in TAB}, nap_fx(), nap_cay())


def _ngay(serial: int) -> datetime.date:
    return _EPOCH + datetime.timedelta(days=serial)


# ── feed ─────────────────────────────────────────────────────────────────────────────────────────

def feed_gl(anh: dict, fx, luat: str, ly: list[str]) -> tuple[list[DongCFA], dict[str, Any]]:
    """GL sổ P&L → `tinh_gl` *(BR/BS)* + ngày ghi nhận D4 *(AH)* → `DongCFA`. Lớp bỏ CÓ TÊN, đếm."""
    dem: dict[str, Any] = {"vao": 0, "thieu_D": [], "AH_RONG": [], "AH_LA": [], "de_lech": [], "br_lech": 0}
    feed: list[DongGL] = []
    meta: list[tuple[int, str | None, str | None, Decimal | None, Decimal | None]] = []
    for r in anh["dong"]:
        dem["vao"] += 1
        ds = int(_so(r["dong_sheet"]))
        tt = _chu(r.get("D"))
        if not tt:
            dem["thieu_D"].append(ds)
            continue
        try:
            t = pla.ngay_pl_tu_yyyymm(luat, r.get("AH"))
        except pla.LoiNgayPL as e:
            dem[e.ma].append(ds)
            continue
        de = _so(r.get("DE")) if not isinstance(r.get("DE"), dict) else None
        if de is None or int(de) != t:
            dem["de_lech"].append(ds)                          # đối chiếu: C6 ↔ cột DE của sổ
        a = _ngay(int(_so(r["A"])))
        feed.append(DongGL(thang=a.year * 100 + a.month, tien_te=tt,
                           no=_so(r.get("E")) or Decimal(0), co=_so(r.get("F")) or Decimal(0)))
        meta.append((t, _chu(r.get("P")), _chu(r.get("V")), _so(r.get("BR")), _so(r.get("BS"))))
    try:
        kq = tinh_gl(feed, fx)
    except (ThieuTyGia, TienTeNgoaiGL) as e:
        ly.append(f"tinh_gl ⛔ chạy được *(⛔ đo được ⇒ ĐỎ)*: {type(e).__name__}: {' '.join(str(e).split())}")
        kq = []
    dong = []
    for (t, le, v, br, bs), k in zip(meta, kq):
        if br is None or bs is None or abs(k.musd_no - br) > ATOL_BR or abs(k.musd_co - bs) > ATOL_BR:
            dem["br_lech"] += 1
        dong.append(DongCFA(ngay=t, le=le, hd=v, musd_no=k.musd_no, musd_co=k.musd_co))
    dem["vao_engine"] = len(dong)
    return dong, dem


def feed_hr(anh: dict, luat: str) -> tuple[list[DongCFA], dict[str, Any]]:
    """HR For PL Report → ngày ghi nhận *(BK/BL, luật năm AS-IS của BM + C6)* → `DongCFA` *(BA/BB)*."""
    dem: dict[str, Any] = {"vao": 0, "BK_RONG": [], "AH_LA": [], "bm_lech": [], "ba_bb_rong": 0}
    dong = []
    for r in anh["dong"]:
        dem["vao"] += 1
        ds = int(_so(r["dong_sheet"]))
        if r.get("BK") in (None, ""):
            dem["BK_RONG"].append(ds)
            continue
        try:
            t = pla.ngay_pl_hr(luat, r.get("BK"), r.get("BL"))
        except pla.LoiNgayPL as e:
            dem[e.ma].append(ds)
            continue
        bm = _so(r.get("BM")) if not isinstance(r.get("BM"), dict) else None
        if bm is None or int(bm) != t:
            dem["bm_lech"].append(ds)
        ba, bb = _so(r.get("BA")), _so(r.get("BB"))
        if ba is None and bb is None:
            dem["ba_bb_rong"] += 1
        dong.append(DongCFA(ngay=t, le=_chu(r.get("P")), hd=_chu(r.get("V")),
                            musd_no=ba or Decimal(0), musd_co=bb or Decimal(0)))
    dem["vao_engine"] = len(dong)
    return dong, dem


# ── đáp án ───────────────────────────────────────────────────────────────────────────────────────

def _dap_an(anh: dict) -> tuple[dict[tuple[str, str, Any], Decimal], list, dict[str, str], set]:
    """(ô ≠ 0 · trục cột theo thứ tự ảnh · mã → loại của ảnh · khối có trong ảnh)."""
    daily = "ngay_truc" in anh["phu"]
    if daily:
        truc = [int(_so(x["ngay"])) for x in anh["phu"]["ngay_truc"]["dong"]]
        o = {(_chu(x["le"]), _chu(x["ma_hd"]), int(_so(x["ngay"]))): _so(x["gt"]) for x in anh["dong"]}
    else:
        truc = [_chu(x["ky"]) for x in anh["phu"]["ky_truc"]["dong"]]
        o = {(_chu(x["le"]), _chu(x["ma_hd"]), _chu(x["ky"])): _so(x["gt"]) for x in anh["dong"]}
    loai = {_chu(h["ma"]): _chu(h["loai"]) for h in anh["phu"]["hd"]["dong"]}
    khoi = {_chu(h["le"]) for h in anh["phu"]["le"]["dong"]}
    return o, truc, loai, khoi


# ── so ───────────────────────────────────────────────────────────────────────────────────────────

def tinh_luoi(gl: dict, hr: dict, fx, cay: CayHD, lich: LichKy, den: datetime.date, ly: list[str]):
    dong_gl, dem_gl = feed_gl(gl, fx, lich.luat, ly)
    dong_hr, dem_hr = feed_hr(hr, lich.luat)
    truc = truc_ngay(lich, den)
    pm = pla.pla_daily(dong_gl, cay, truc, KHOI_DO["PM"], pla.CONG_THUC_PM)
    hrd = pla.pla_daily(dong_hr, cay, truc, KHOI_DO["HR"], pla.CONG_THUC_HR)
    ph = pla.pla_pm_hr_daily(pm, hrd, cay, KHOI_DO["PMHR"])
    luoi = {"pla1_daily": pm, "pla3_hr_daily": hrd, "pla3_pm_hr_daily": ph,
            "pla1_yhqm": pla.pla_yhqm(pm, cay, KHOI_DO["PM"], pla.CONG_THUC_PM),
            "pla3_hr_yhqm": pla.pla_yhqm(hrd, cay, KHOI_DO["HR"], pla.CONG_THUC_HR),
            "pla3_pm_hr_yhqm": pla.pla_yhqm(ph, cay, KHOI_DO["PMHR"], pla.CONG_THUC_PM)}
    dem_dong = {}
    for ten, kq in (("gl", pm), ("hr", hrd)):
        d = kq.dong
        dem_dong[ten] = {"ngoai_cay": len(d.dong_ngoai_cay), "nhan_cha": len(d.dong_nhan_cha),
                         "ngoai_truc": len(d.dong_ngoai_truc), "khac_hoa": len(d.dong_khac_hoa)}
    return luoi, {"gl": dem_gl, "hr": dem_hr, "dong": dem_dong, "truc": (truc[0], truc[-1], len(truc))}


def so_tab(ten: str, kq: pla.KetQuaPLA, anh: dict) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """So TỪNG Ô một tab trên khối đo được. Nhãn Đ4: ô so tách `thuong` *(la+tong)* · `kpi`."""
    o_da, truc_da, loai_da, khoi_da = _dap_an(anh)
    tren_truc = set(kq.cot)
    cot = [t for t in truc_da if t in tren_truc]
    cot_ngoai = [t for t in truc_da if t not in tren_truc]
    khoi_do = [k for k in kq.khoi if k in khoi_da]
    s: dict[str, Any] = {"cot_so": len(cot), "khoi_do": khoi_do}
    lech: list[dict[str, Any]] = []
    for nhom in ("thuong", "kpi"):
        o_so = khop = o00 = 0
        mx = Decimal(0)
        for kh in khoi_do:
            for m, lo in loai_da.items():
                if lo == "trong" or (lo == "kpi") != (nhom == "kpi"):
                    continue
                for t in cot:
                    e, a = kq.o[(kh, m, t)], o_da.get((kh, m, t), Decimal(0))
                    o_so += 1
                    if e == 0 and a == 0:
                        o00 += 1
                        khop += 1
                    elif abs(e - a) <= ATOL:
                        khop += 1
                        mx = max(mx, abs(e - a))
                    else:
                        lech.append({"tab": ten, "o": f"{kh}#{m}#{t}", "engine": str(e), "dap_an": str(a)})
        s[nhom] = {"o_so": o_so, "khop": khop, "o_0_0": o00, "lech": o_so - khop, "max_lech_khop": str(mx)}
    # ô đáp án ≠ 0 NGOÀI phạm vi — mỗi lớp một tên
    s["chua_co_dau_vao"] = sum(1 for (kh, _, _), v in o_da.items() if kh not in khoi_do and v)
    s["cot_ngoai_truc"] = {"cot": [str(t) for t in cot_ngoai],
                           "o_khac_0": sum(1 for (kh, _, t), v in o_da.items() if t in set(cot_ngoai)
                                           and kh in khoi_do and v)}
    s["trong_khac_0"] = sum(1 for (kh, m, _), v in o_da.items() if loai_da.get(m) == "trong" and v)
    return s, lech


_CAP = (("pla1_daily", "pla3_hr_daily", "pla3_pm_hr_daily"), ("pla1_yhqm", "pla3_hr_yhqm", "pla3_pm_hr_yhqm"))


def _tu_kiem(o_pm, o_hr, o_ph, loai: Mapping[str, str], cot) -> dict[str, int]:
    """Đếm ô GROUP mà `PM+HR ≠ PM + HR` *(cộng THEO KHOÁ — Đ4: tách thường · KPI)*."""
    n = {"thuong": 0, "kpi": 0}
    for m, lo in loai.items():
        if lo == "trong":
            continue
        for t in cot:
            k = (KHOI_TONG, m, t)
            if abs(o_ph.get(k, Decimal(0)) - (o_pm.get(k, Decimal(0)) + o_hr.get(k, Decimal(0)))) > ATOL:
                n["kpi" if lo == "kpi" else "thuong"] += 1
    return n


def _khong_so_duoc(dap_an: Mapping[str, dict]) -> int:
    """417 thiếu khối: (số khối của 415 − số khối của 417) × mã × kỳ của 417 *(⛔ coi là khớp)*."""
    a, b = dap_an["pla1_yhqm"], dap_an["pla3_hr_yhqm"]
    nk = len(a["phu"]["le"]["dong"]) - len(b["phu"]["le"]["dong"])
    nm = len({_chu(h["ma"]) for h in b["phu"]["hd"]["dong"]})
    return nk * nm * len(b["phu"]["ky_truc"]["dong"])


def _so_lop(so: Mapping[str, Any]) -> dict[str, Any]:
    """Phần SO ĐƯỢC với `mong` *(mọi khoá ở đây phải có trong `MONG` — Đ5 hai chiều)*."""
    dg, dh, dd = so["dem"]["gl"], so["dem"]["hr"], so["dem"]["dong"]
    return {
        "gl": {"vao": dg["vao"], "thieu_D": len(dg["thieu_D"]), "AH_RONG": len(dg["AH_RONG"]),
               "AH_LA": sorted(dg["AH_LA"]), "de_lech": len(dg["de_lech"]), "br_lech": dg["br_lech"],
               "vao_engine": dg["vao_engine"], **{f"dong_{k}": v for k, v in dd["gl"].items()}},
        "hr": {"vao": dh["vao"], "BK_RONG": len(dh["BK_RONG"]), "AH_LA": len(dh["AH_LA"]),
               "bm_lech": len(dh["bm_lech"]), "ba_bb_rong": dh["ba_bb_rong"], "vao_engine": dh["vao_engine"],
               **{f"dong_{k}": v for k, v in dd["hr"].items()}},
        "truc": [_ngay(so["dem"]["truc"][0]).isoformat(), _ngay(so["dem"]["truc"][1]).isoformat(),
                 so["dem"]["truc"][2]],
        "tab": {t: {"o_so": s["thuong"]["o_so"], "o_so_kpi": s["kpi"]["o_so"],
                    "o_0_0": s["thuong"]["o_0_0"] + s["kpi"]["o_0_0"],
                    "chua_co_dau_vao": s["chua_co_dau_vao"], "cot_ngoai_truc": s["cot_ngoai_truc"]["o_khac_0"],
                    "trong_khac_0": s["trong_khac_0"]} for t, s in so["tab"].items()},
        "khong_so_duoc": so["khong_so_duoc"],
        "tu_kiem_dap_an": so["tu_kiem_dap_an"], "tu_kiem_engine": so["tu_kiem_engine"],
    }


def _khac(thuc: Any, mong: Any, duong: str, ly: list[str]) -> None:
    if isinstance(mong, Mapping) and isinstance(thuc, Mapping):
        for k in sorted(set(mong) | set(thuc), key=str):
            if k not in mong:
                ly.append(f"{duong}.{k} = {thuc[k]!r} ⛔ có trong mong (khai TRƯỚC)")
            elif k not in thuc:
                ly.append(f"{duong}.{k}: mong {mong[k]!r} ⛔ đo được")
            else:
                _khac(thuc[k], mong[k], f"{duong}.{k}", ly)
    elif thuc != mong:
        ly.append(f"{duong} thực {thuc!r} ≠ mong {mong!r}")


def so_sanh_c3d(gl: dict, hr: dict, dap_an: Mapping[str, dict], fx, cay: CayHD, lich: LichKy,
                den: datetime.date, mong: MongC3d) -> ThanhQuaC3d:
    ly: list[str] = []
    luoi, dem = tinh_luoi(gl, hr, fx, cay, lich, den, ly)
    so: dict[str, Any] = {"dem": dem, "tab": {}}
    lech: list[dict[str, Any]] = []
    for ten in TAB:
        s, lc = so_tab(ten, luoi[ten], dap_an[ten])
        so["tab"][ten] = s
        lech += lc
    so["khong_so_duoc"] = _khong_so_duoc(dap_an)
    so["tu_kiem_engine"], so["tu_kiem_dap_an"] = {}, {}
    for (a, b, c), hat in zip(_CAP, ("daily", "yhqm")):
        so["tu_kiem_engine"][hat] = _tu_kiem(luoi[a].o, luoi[b].o, luoi[c].o, luoi[c].loai, luoi[c].cot)
        oa, ta, la_, _ = _dap_an(dap_an[a])
        ob, _, _, _ = _dap_an(dap_an[b])
        oc, _, _, _ = _dap_an(dap_an[c])
        so["tu_kiem_dap_an"][hat] = _tu_kiem(oa, ob, oc, la_, ta)
    # ── phán quyết ──
    m = mong.so
    tong = {k: sum(s[n][k] for s in so["tab"].values() for n in ("thuong", "kpi")) for k in ("o_so", "khop", "o_0_0")}
    if tong["o_so"] == 0:
        ly.append("0 ô được so ⇒ ⛔ đo được gì (Đ3)")
    if m is None:
        ly.append("`mong` chưa khai ⇒ ⛔ tin (Đ5)")
        m = {}
    _khac(_so_lop(so), m.get("lop"), "lop", ly)
    mong_o = m.get("o_lech") or {}
    atol_lech = Decimal(str(m.get("atol_lech", "1e-9")))
    co_chu_dich: list[dict[str, Any]] = []
    ngoai_ten: list[dict[str, Any]] = []
    for x in lech:
        k = f"{x['tab']}|{x['o']}"
        mg = mong_o.get(k)
        if mg is not None and abs(Decimal(x["engine"]) - Decimal(mg[0])) <= atol_lech \
                and abs(Decimal(x["dap_an"]) - Decimal(mg[1])) <= atol_lech:
            co_chu_dich.append(x)
        else:
            ngoai_ten.append(x)
    thay = {f"{x['tab']}|{x['o']}" for x in lech}
    for k in sorted(set(mong_o) - thay):
        ly.append(f"ô mong lệch `{k}` nay KHỚP ⇒ sửa bản khai (Đ5 chiều ngược)")
    for x in ngoai_ten[:20]:
        ly.append(f"ô lệch ngoài tên `{x['tab']}|{x['o']}`: engine {x['engine']} · đáp án {x['dap_an']}")
    if len(ngoai_ten) > 20:
        ly.append(f"… +{len(ngoai_ten) - 20} ô lệch ngoài tên")
    so["lech_co_chu_dich"], so["lech_ngoai_ten"] = len(co_chu_dich), len(ngoai_ten)
    px = PhanXu(not ly, tuple(ly))
    o_co_so = tong["o_so"] - tong["o_0_0"]
    khop_co_so = tong["khop"] - tong["o_0_0"]
    hd2 = {
        "bang": "HD2.WP-C3d", "goi": "WP-C3d",
        "mo_ta": "SO.PLA1 · PLA3 HR · PLA3 PM+HR (gl_pl_dau_vao → tinh_gl + C6 D4 A từ AH; hr_pl_dau_vao BA/BB + "
                 "BK/BL) → pla_daily (cfa1_daily H5 + công thức tab) · cộng THEO KHOÁ · pla_yhqm (cuon_ky H6) ↔ 414–419",
        "nguon_dau_vao": ["tests/fixture/dau_vao/gl_pl_dau_vao.json", "tests/fixture/dau_vao/hr_pl_dau_vao.json"],
        "dap_an": [f"tests/fixture/dap_an/{t}.json" for t in TAB],
        "khoa": "tab × khối đo được × mã (la+tong | kpi — ⛔ trong) × cột trục (ngày | kỳ)",
        "khoi_do": {t: list(KHOI_DO[v]) for t, v in TAB.items()},
        "dung_sai": {"atol": str(ATOL), "rtol": "0",
                     "ghi_chu": "đo 22/11: max|lệch| ô khớp " + " · ".join(
                         f"{t} {max(Decimal(s['thuong']['max_lech_khop']), Decimal(s['kpi']['max_lech_khop'])):.1E}"
                         for t, s in so["tab"].items()) + " ⇒ atol ≥ ×30"},
        "truc": _so_lop(so)["truc"],
        "tong_o": tong["o_so"], "mong_tong_o": m.get("tong_o"),
        "o_co_so": o_co_so, "khop_co_so": khop_co_so, "o_0_0": tong["o_0_0"],
        "khop": tong["khop"],
        "lech_co_chu_dich": len(co_chu_dich), "mong_lech_co_chu_dich": len(mong_o),
        "lech_ngoai_ten": len(ngoai_ten),
        "khop_ghi_chu": "tong_o = Σ ô so 6 tab (la+tong và kpi, khối đo được, cột trên trục) = o_co_so + o_0_0; "
                        "khop = ô khớp THẬT (khop_co_so + o_0_0); khop + lech_co_chu_dich = tong_o",
        "theo_tab": {t: {"thuong": s["thuong"], "kpi": s["kpi"]} for t, s in so["tab"].items()},
        "lech_co_ten": {
            "as_is_416_GAC_thieu_CXA": [f"{x['tab']}|{x['o']}" for x in co_chu_dich],
            "chua_co_dau_vao": {t: s["chua_co_dau_vao"] for t, s in so["tab"].items()},
            "khong_so_duoc": so["khong_so_duoc"],
            "cot_ngoai_truc": {t: s["cot_ngoai_truc"] for t, s in so["tab"].items()},
            "gl": _so_lop(so)["gl"], "hr": _so_lop(so)["hr"],
            "tu_kiem_dap_an": so["tu_kiem_dap_an"], "tu_kiem_engine": so["tu_kiem_engine"],
        },
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    if m.get("tong_o") is not None and m["tong_o"] != tong["o_so"]:
        ly.append(f"mẫu số tong_o {tong['o_so']} ≠ mong {m['tong_o']}")
        px = PhanXu(False, tuple(ly))
        hd2["dat"], hd2["ly_do"] = False, list(ly)
    return ThanhQuaC3d(so=so, phan_xu=px, hd2_cong=hd2, luoi=luoi, lech=lech)


def _lich_tu_kho(dsn: str | None):
    from tools.do_hd2 import _lich_tu_kho as f      # C6 — một đường đọc IX.PER (⛔ chép)
    return f(dsn)


def chay_wp_c3d(dsn: str | None = None) -> ThanhQuaC3d:
    lich, loi = _lich_tu_kho(dsn)
    if lich is None:
        px = PhanXu(False, (loi or "IX.PER rỗng",))
        return ThanhQuaC3d(so={}, phan_xu=px, hd2_cong={"bang": "HD2.WP-C3d", "goi": "WP-C3d", "dat": False,
                                                        "ly_do": list(px.ly_do)})
    m = mong_c3d_mac_dinh()
    return so_sanh_c3d(*nap_nguon(), lich, datetime.date.fromisoformat(m.so["den"]), m)


def in_bao(tq: ThanhQuaC3d) -> None:
    h = tq.hd2_cong
    print("══ WP-C3d · SO.PLA1 · PLA3 HR · PLA3 PM+HR ↔ 414–419")
    if "tong_o" in h:
        print(f"  ô so {h['tong_o']} = có số {h['o_co_so']} + 0=0 {h['o_0_0']} · khớp {h['khop']} "
              f"(thật {h['khop_co_so']}/{h['o_co_so']}) · lệch có chủ đích {h['lech_co_chu_dich']} · "
              f"ngoài tên {h['lech_ngoai_ten']}")
        for t, s in h["theo_tab"].items():
            print(f"  {t:<18} thường {s['thuong']['khop']}/{s['thuong']['o_so']} · KPI {s['kpi']['khop']}/{s['kpi']['o_so']}")
    for x in h.get("ly_do", []):
        print(f"  ⛔ {x}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")
