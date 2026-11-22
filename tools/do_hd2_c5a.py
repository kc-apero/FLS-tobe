"""`do_hd2.py --goi WP-C5a` — PARITY HD2 `AL.KEY` cờ TẮT ↔ ATL 606 *(+ tham chiếu 604)* — ISP 3.1.2 · Step 42 ·
H12 · `WO-291`.

⭐ **Đầu vào = THƯỢNG NGUỒN, ⛔ đáp án**: lưới `SO.PLA3 PM + HR` Y/H/Q/M do H8 tính từ ảnh đầu vào DT7b
*(`do_hd2_c3d.tinh_luoi` → `pla.pla_yhqm`)* → `phan_bo_khoa` *(cờ từ `IX.ALR` ĐỌC TỪ KHO — C11, mọi cờ TẮT — D2)*.
Đáp án `tests/fixture/dap_an/atl.json` *(DT10)* chỉ ĐỌC ở bước so. Khoá hàng ATL → `(khối, mã)` dựng từ CHÍNH ảnh
ATL *(khối mở ở mỗi hàng `GI`, thứ tự `KHOI_12` của H8; mã = nhãn trước ` | `)*.

⚠ **ERRATA đo 22/11** *(SA đọc FORMULA `B5:BK1110`, chỉ-đọc)*: WO/BG-197 ghi "AS-IS CHƯA phân bổ ⇒ ATL = đáp án
cờ tắt" — SAI cho 2025. Ô tháng 2025 của 6 khối CDT: **576** ô By GI *(8 mã × 6 khối × 12: `iferror(sumifs(GROUP)×
(GI khối/GI GROUP))`)* · **348** ô By NOEM *(5 mã — CAH 4, ngoại lệ OFR — × 12: `INDEX('[H1.2026][2025]H1000 I HR
Report'…)`)* · **66** ô `GI` khối CDT lấy `CFA2 | MID 3 | GI Platform Data Ledger` *(⛔ PLA3)*; GROUP `OMC` 2025-02 =
`PLA3 − 0,5` *(gõ tay)*; SGO1 một hàng `+ 'Allocation Table | NB | By LE'×−1` *(12 ô 2025)*. ⇒ AS-IS ĐÃ BẬT phân bổ;
FLS giữ cờ TẮT *(D2)* ⇒ các ô ấy là **lệch AS-IS có tên** *(⛔ chép vào engine)*.

── LỚP LỆCH *(Đ5 — `mong` khai TRƯỚC ở `do_hd2_c5a_mong.py`, khác ⇒ ĐỎ CẢ HAI CHIỀU)* ────────────────────────
  · `o_lech` — khai TỪNG Ô theo giá trị *(GROUP: −0,5 tay + lan cây/KPI/NPC · SGO1: NB by LE + lan)*.
  · `as_is_bat_phan_bo_2025` — khối CDT ∪ {SHQ2} × kỳ 2025: đếm theo khối + sha256 *(ô, engine, đáp án)*.
  · `as_is_truoc_CA` — khối CDT ∪ {SHQ2} × kỳ 2024: lệch AS-IS 416 lan từ H8 *(`BG-278` — 72 cột 2024)*; như trên.
  Ô lệch ngoài ba lớp ⇒ `lech_ngoai_ten` ⇒ ĐỎ.
"""
from __future__ import annotations

import datetime
import hashlib
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from fls.bao_cao import pla
from fls.bao_cao import phan_bo_khoa as pbk
from fls.bao_cao.cfa import KHOI_TONG
from fls.cau_hinh import luat_pb
from fls.cau_hinh.hd import CayHD
from fls.oracle.cong_parity import PhanXu
from tools import do_hd2_c3d as c3d
from tools.do_hd2 import GOC, _chu, _so, nap_anh

ANH_ATL = GOC / "tests" / "fixture" / "dap_an" / "atl.json"
ANH_DRV = GOC / "tests" / "fixture" / "cau_hinh" / "ix_drv.json"
ANH_MM = GOC / "tests" / "fixture" / "cau_hinh" / "mapping_master_cfg.json"
KHOI_CDT6 = tuple(c3d.KHOI_CDT)
KHOI_PB = frozenset(KHOI_CDT6) | {c3d.KHOI_DU}
ATOL = c3d.ATOL                                  # 1e-12, rtol 0 *(cùng WP-C3d — lưới vào là của H8)*
ATOL_604 = Decimal("1e-9")
#: tháng IX.ALR bắt đầu hiệu lực khi nạp vào kho test *(giá trị cấu hình người gọi khai)*. ⚠ CÙNG khoá `hd@202501`
#: với bài C11 *(`tests/cau_hinh/test_luat_pb_pg.py`)*: kho config TÍCH LUỸ *(`C11-R1-01`)* ⇒ nạp mốc KHÁC làm bài C11
#: chạy SAU thấy 34 luật *(đo 22/11: `--tu_ky 202410` ⇒ 2 bài C11 ĐỎ khi `tests/oracle` chạy trước `tests/cau_hinh`)*.
#: Cờ TẮT ⇒ mốc ⛔ đổi kết quả cổng *(đồng nhất)*.
TU_KY_ALR = 202501
_THANG = [f"m{m:02d}" for m in range(1, 13)]


# ── config ────────────────────────────────────────────────────────────────────────────────────────

def alr_tu_anh_mm(tu_ky: int = TU_KY_ALR) -> luat_pb.BangALR:
    """`BangALR` từ ảnh Mapping Master DT3 qua CHÍNH `luat_pb.dung_tu_mm` + `kiem` *(cùng đường `nap_ix_alr`;
    cho bài đơn vị ⛔ kho — cổng đọc kho bằng `doc_alr`)*."""
    anh = nap_anh(ANH_MM)
    mm = [{"hd_code": _chu(r.get("hd_code")), "need_cfa2": _chu(r.get("need_cfa2")),
           "method_cfa2": _chu(r.get("method_cfa2"))} for r in anh["dong"]]
    return luat_pb.kiem(luat_pb.dung_tu_mm(mm, tu_ky=tu_ky), nguon=ANH_MM.name)


def luoi_driver_tu_anh(anh: Mapping[str, Any] | None = None) -> pbk.LuoiDriver:
    """Ảnh IX.DRV DT10 → `LuoiDriver`: 238 ô số + 146 ô thiếu CÓ TÊN *(bảng `o_thieu`)*."""
    anh = anh or nap_anh(ANH_DRV)
    o: dict[tuple[str, str, int], Decimal] = {}
    for r in anh["dong"]:
        nam = int(_so(r["nam"]))
        for i, c in enumerate(_THANG, start=1):
            v = _so(r.get(c))
            if v is not None:
                o[(_chu(r["driver"]), _chu(r["cdt1"]), nam * 100 + i)] = v
    thieu = {(_chu(x["driver"]), _chu(x["cdt1"]), int(_chu(x["thang"]))): _chu(x["ly_do"])
             for x in anh["phu"]["o_thieu"]["dong"]}
    return pbk.LuoiDriver(o=o, thieu=thieu)


def tham_chieu_604(anh_drv: Mapping[str, Any], anh_atl: Mapping[str, Any]) -> dict[str, Any]:
    """PD 604 *(tham chiếu)*: số CDT1 có số theo (driver, tháng) ở ATL `pd604_ky` ↔ lưới IX.DRV; Σ7 CDT1 = 1."""
    drv = luoi_driver_tu_anh(anh_drv)
    o_so = khop = 0
    lech: list[str] = []
    for r in anh_atl["phu"]["pd604_ky"]["dong"]:
        d = _chu(r["driver"])
        for i, c in enumerate(_THANG, start=1):
            o_so += 1
            n = sum(1 for (dd, _, t) in drv.o if dd == d and t == 202500 + i)
            if n == int(_so(r[c])):
                khop += 1
            else:
                lech.append(f"{d}|2025{i:02d}: drv {n} ≠ ATL {_so(r[c])}")
    tong: dict[tuple[str, int], Decimal] = {}
    for (d, _, t), v in drv.o.items():
        tong[(d, t)] = tong.get((d, t), Decimal(0)) + v
    sigma_lech = sorted(f"{d}|{t}" for (d, t), v in tong.items() if abs(v - 1) > ATOL_604)
    return {"o_so": o_so, "khop": khop, "lech": lech, "o_drv": len(drv.o), "o_thieu": len(drv.thieu),
            "sigma_7": len(tong), "sigma_7_lech": sigma_lech}


# ── ATL ──────────────────────────────────────────────────────────────────────────────────────────

def _ky(cot: str) -> str:
    nam, k = cot[1:].split("_")
    return nam if k == "y" else nam + k.upper()


def hang_atl(anh: Mapping[str, Any]) -> tuple[list[tuple[str, str, dict]], list[dict]]:
    """Hàng ATL → (khối, mã, hàng). Khối mở ở mỗi hàng nhãn `GI` theo thứ tự `KHOI_12`; hàng ⛔ nhãn tách riêng."""
    ra: list[tuple[str, str, dict]] = []
    khong_nhan: list[dict] = []
    i = -1
    for r in anh["dong"]:
        nhan = next((_chu(r[k]) for k in ("l1", "l2", "l3", "l4") if r.get(k)), None)
        if not nhan:
            khong_nhan.append(r)
            continue
        ma = nhan.split("|")[0].strip()
        if ma == "GI":
            i += 1
        if not 0 <= i < len(c3d.KHOI_12):
            raise ValueError(f"hàng sheet {r['dong_sheet']}: khối thứ {i + 1} ⛔ có trong KHOI_12 (Đ5)")
        ra.append((c3d.KHOI_12[i], ma, r))
    return ra, khong_nhan


@dataclass(frozen=True)
class MongC5a:
    so: Mapping[str, Any] | None = None


def mong_c5a_mac_dinh() -> MongC5a:
    from tools.do_hd2_c5a_mong import MONG
    return MongC5a(so=MONG)


@dataclass
class ThanhQuaC5a:
    so: dict[str, Any]
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    lech: list[dict[str, Any]] = field(default_factory=list)


def _lop(x: Mapping[str, str]) -> str | None:
    kh, _, t = x["o"].split("#")
    if kh not in KHOI_PB:
        return None
    return {"2025": "as_is_bat_phan_bo_2025", "2024": "as_is_truoc_CA"}.get(t[:4])


def _tom(ds: list[Mapping[str, str]]) -> dict[str, Any]:
    q = Decimal("1e-12")
    dem = Counter(x["o"].split("#")[0] for x in ds)
    chuoi = "\n".join(sorted(f"{x['o']}={Decimal(x['engine']).quantize(q)}|{Decimal(x['dap_an']).quantize(q)}"
                              for x in ds))
    return {"theo_khoi": dict(sorted(dem.items())), "so_o": len(ds),
            "sha256": hashlib.sha256(chuoi.encode()).hexdigest()}


def so_sanh_c5a(pla3: pla.KetQuaPLA, atl: Mapping[str, Any], drv: Mapping[str, Any], alr: Any, cay: CayHD,
                mong: MongC5a) -> ThanhQuaC5a:
    ly: list[str] = []
    try:
        kq = pbk.phan_bo_khoa(pla3, alr, cay, pla.CONG_THUC_PM, khoi_nguon=KHOI_TONG, khoi_cdt=KHOI_CDT6,
                              khoi_du=c3d.KHOI_DU, driver=luoi_driver_tu_anh(drv))
    except pbk.LoiPhanBoKhoa as e:
        px = PhanXu(False, (str(e),))
        return ThanhQuaC5a(so={}, phan_xu=px, hd2_cong={"bang": "HD2.WP-C5a", "goi": "WP-C5a", "dat": False,
                                                        "ly_do": list(px.ly_do)})
    hang, khong_nhan = hang_atl(atl)
    cot = [c for c in atl["cot"] if c[:1] == "y"]
    dem = Counter()
    theo_khoi: dict[str, Counter] = {}
    lech: list[dict[str, Any]] = []
    mx = Decimal(0)
    for kh, ma, r in hang:
        lo = pla3.loai.get(ma)
        if lo is None:
            dem["ma_ngoai_cay"] += 1
            continue
        if lo == "trong":
            dem["o_trong"] += len(cot)
            continue
        tk = theo_khoi.setdefault(kh, Counter())
        for c in cot:
            v = r.get(c)
            try:
                a = Decimal(0) if v is None else Decimal(str(v))
            except InvalidOperation:
                dem["khong_so_duoc"] += 1
                continue
            e = kq.o[(kh, ma, _ky(c))]
            dem["o_so"] += 1
            tk["o_so"] += 1
            if e == 0 and a == 0:
                dem["o_0_0"] += 1
                dem["khop"] += 1
            elif abs(e - a) <= ATOL:
                dem["khop"] += 1
                mx = max(mx, abs(e - a))
            else:
                tk["lech"] += 1
                lech.append({"o": f"{kh}#{ma}#{_ky(c)}", "engine": str(e), "dap_an": str(a)})
    dem["hang_so"] = len(hang)
    dem["hang_khong_nhan"] = len(khong_nhan)
    dem["hang_khong_nhan_khac_0"] = sum(1 for r in khong_nhan for c in cot if r.get(c) not in (None, "0"))
    t604 = tham_chieu_604(drv, atl)
    so: dict[str, Any] = {"dem": dict(dem), "theo_khoi": {k: dict(v) for k, v in theo_khoi.items()},
                          "tham_chieu_604": t604, "dem_phan_bo": kq.dem,
                          "max_lech_khop": str(mx)}
    # ── phán quyết ──
    m = mong.so
    if dem["o_so"] == 0:
        ly.append("0 ô được so ⇒ ⛔ đo được gì (Đ3)")
    if m is None:
        ly.append("`mong` chưa khai ⇒ ⛔ tin (Đ5)")
        m = {}
    lop_thuc = {"dem": dict(dem), "dem_phan_bo": kq.dem,
                "tham_chieu_604": {k: t604[k] for k in ("o_so", "khop", "o_drv", "o_thieu", "sigma_7")}}
    c3d._khac(lop_thuc, m.get("lop"), "lop", ly)
    if t604["lech"] or t604["sigma_7_lech"]:
        ly.append(f"tham chiếu 604 lệch: {t604['lech'][:5]} · Σ7≠1: {t604['sigma_7_lech'][:5]}")
    mong_o = m.get("o_lech") or {}
    atol_lech = Decimal(str(m.get("atol_lech", "1e-9")))
    tung_o: list[dict[str, Any]] = []
    theo_lop: dict[str, list[dict[str, Any]]] = {"as_is_bat_phan_bo_2025": [], "as_is_truoc_CA": []}
    ngoai_ten: list[dict[str, Any]] = []
    for x in lech:
        mg = mong_o.get(x["o"])
        if mg is not None and abs(Decimal(x["engine"]) - Decimal(mg[0])) <= atol_lech \
                and abs(Decimal(x["dap_an"]) - Decimal(mg[1])) <= atol_lech:
            tung_o.append(x)
        elif _lop(x):
            theo_lop[_lop(x)].append(x)
        else:
            ngoai_ten.append(x)
    so["lop_quy_tac"] = {k: _tom(v) for k, v in theo_lop.items()}
    c3d._khac(so["lop_quy_tac"], m.get("lop_quy_tac"), "lop_quy_tac", ly)
    thay = {x["o"] for x in lech}
    for k in sorted(set(mong_o) - thay):
        ly.append(f"ô mong lệch `{k}` nay KHỚP ⇒ sửa bản khai (Đ5 chiều ngược)")
    for x in ngoai_ten[:20]:
        ly.append(f"ô lệch ngoài tên `{x['o']}`: engine {x['engine']} · ATL {x['dap_an']}")
    if len(ngoai_ten) > 20:
        ly.append(f"… +{len(ngoai_ten) - 20} ô lệch ngoài tên")
    co_chu_dich = len(tung_o) + sum(len(v) for v in theo_lop.values())
    so["lech_co_chu_dich"], so["lech_ngoai_ten"] = co_chu_dich, len(ngoai_ten)
    if m.get("tong_o") is not None and m["tong_o"] != dem["o_so"]:
        ly.append(f"mẫu số tong_o {dem['o_so']} ≠ mong {m['tong_o']}")
    px = PhanXu(not ly, tuple(ly))
    hd2 = {
        "bang": "HD2.WP-C5a", "goi": "WP-C5a",
        "mo_ta": "AL.KEY cờ IX.ALR TẮT (kho, C11 — D2) trên lưới SO.PLA3 PM+HR Y/H/Q/M của H8 (đầu vào DT7b) "
                 "↔ ATL 606 (+ tham chiếu 604: lưới IX.DRV ↔ pd604_ky)",
        "nguon_dau_vao": ["tests/fixture/dau_vao/gl_pl_dau_vao.json", "tests/fixture/dau_vao/hr_pl_dau_vao.json",
                          "tests/fixture/cau_hinh/ix_drv.json", "IX.ALR (kho)"],
        "dap_an": ["tests/fixture/dap_an/atl.json"],
        "khoa": "khối (12) × mã (la+tong+kpi — ⛔ trong) × kỳ (57) của hàng ATL có nhãn",
        "dung_sai": {"atol": str(ATOL), "rtol": "0", "max_lech_khop": str(mx)},
        "tong_o": dem["o_so"], "mong_tong_o": m.get("tong_o"),
        "o_co_so": dem["o_so"] - dem["o_0_0"], "khop_co_so": dem["khop"] - dem["o_0_0"], "o_0_0": dem["o_0_0"],
        "khop": dem["khop"],
        "lech_co_chu_dich": co_chu_dich,
        "mong_lech_co_chu_dich": len(mong_o) + sum((v or {}).get("so_o", 0)
                                                   for v in (m.get("lop_quy_tac") or {}).values()),
        "lech_ngoai_ten": len(ngoai_ten),
        "khop_ghi_chu": "tong_o = ô so (hàng ATL có nhãn, mã ⛔ trong, ô là số) = o_co_so + o_0_0; khop = ô khớp "
                        "THẬT; khop + lech_co_chu_dich = tong_o",
        "lech_co_ten": {"o_lech": sorted(x["o"] for x in tung_o), **so["lop_quy_tac"],
                        "khong_so_duoc": dem["khong_so_duoc"], "o_trong": dem["o_trong"],
                        "hang_khong_nhan_khac_0": dem["hang_khong_nhan_khac_0"]},
        "theo_khoi": so["theo_khoi"],
        "tham_chieu_604": {k: t604[k] for k in ("o_so", "khop", "o_drv", "o_thieu", "sigma_7")},
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    return ThanhQuaC5a(so=so, phan_xu=px, hd2_cong=hd2, lech=lech)


def nap_nguon() -> tuple:
    return (*c3d.nap_nguon(), nap_anh(ANH_ATL), nap_anh(ANH_DRV))


def tinh_pla3(gl, hr, fx, cay, lich, den) -> pla.KetQuaPLA:
    luoi, _ = c3d.tinh_luoi(gl, hr, fx, cay, lich, den, [])
    return luoi["pla3_pm_hr_yhqm"]


def _alr_tu_kho(dsn: str | None):
    try:
        import psycopg
        from fls.db.kho import dsn_that
        from fls.repo import cau_hinh_repo as chc
        with psycopg.connect(dsn or dsn_that()) as c:
            return chc.doc_alr(c), None
    except Exception as e:  # noqa: BLE001 — Đ5: ⛔ đo được ⇒ ĐỎ có lý do
        return None, f"IX.ALR ⛔ đọc được từ kho: {type(e).__name__}: {' '.join(str(e).split())}"


def chay_wp_c5a(dsn: str | None = None) -> ThanhQuaC5a:
    lich, loi = c3d._lich_tu_kho(dsn)
    alr, loi2 = _alr_tu_kho(dsn)
    if lich is None or alr is None:
        px = PhanXu(False, tuple(x for x in (loi, loi2) if x))
        return ThanhQuaC5a(so={}, phan_xu=px, hd2_cong={"bang": "HD2.WP-C5a", "goi": "WP-C5a", "dat": False,
                                                        "ly_do": list(px.ly_do)})
    gl, hr, _, fx, cay, atl, drv = nap_nguon()
    den = datetime.date.fromisoformat(c3d.mong_c3d_mac_dinh().so["den"])
    return so_sanh_c5a(tinh_pla3(gl, hr, fx, cay, lich, den), atl, drv, alr, cay, mong_c5a_mac_dinh())


def in_bao(tq: ThanhQuaC5a) -> None:
    h = tq.hd2_cong
    print("══ WP-C5a · AL.KEY cờ TẮT ↔ ATL 606 (+ 604)")
    if "tong_o" in h:
        print(f"  ô so {h['tong_o']} = có số {h['o_co_so']} + 0=0 {h['o_0_0']} · khớp {h['khop']} "
              f"(thật {h['khop_co_so']}/{h['o_co_so']}) · lệch có chủ đích {h['lech_co_chu_dich']} · "
              f"ngoài tên {h['lech_ngoai_ten']} · khong_so_duoc {h['lech_co_ten']['khong_so_duoc']}")
        print(f"  604: {h['tham_chieu_604']}")
    for x in h.get("ly_do", []):
        print(f"  ⛔ {x}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")
