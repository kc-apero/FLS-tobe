"""`do_hd2.py --goi WP-C5b` — dòng `PL2…PL8` từ **IX.PL** *(C12)* trên **ATL của FLS** + hai phép CHECK mỗi kỳ ↔ ATL
606 — ISP 3.1.2 · Step 44 · H13 · `WO-307`.

⭐ **Đầu vào = THƯỢNG NGUỒN, ⛔ đáp án**: ATL của FLS = đầu ra AL.KEY của H12 *(`do_hd2_c5a.so_sanh_c5a` — lưới
`SO.PLA3 PM + HR` của H8 trên ảnh DT7b → `phan_bo_khoa`, cờ IX.ALR 2025 BẬT ký — đọc từ KHO)*; định nghĩa dòng PL =
**IX.PL ĐỌC TỪ KHO** *(`cau_hinh_repo.doc_pl`)*; `COM_GAG` *(đầu vào ngoài cây của PL5)* = ảnh
`tests/fixture/dau_vao/noem_com_gag.json` ÷ tỷ giá USD *(`ix_fx.json`)* ÷ 10⁶ — đúng phép của ô sheet `AG84:AR84`
*(bài C12 `test_C12_R2_01_PL5_khop_o_AG_AR_sheet…`)*, chỉ có ở **GROUP × 12 tháng 2025** ⇒ ô PL5 khác có số ở ATL
là `pl5_khong_tinh_duoc` CÓ TÊN *(ngoài mẫu số — ⛔ ngầm 0)*. Đáp án `atl.json` chỉ ĐỌC ở bước so.

── LỚP LỆCH *(Đ5 — `mong` khai TRƯỚC ở `do_hd2_c5b_mong.py`, khác ⇒ ĐỎ CẢ HAI CHIỀU)* ──────────────────────────────
⭐ Dòng PL lệch **THỪA KẾ** lớp từ ô LÁ *(luật phòng tái phạm `H12-R1-01`: ⛔ quy tắc khối × năm)*: lá của dòng =
   `pla.la_cua_dong` *(trải chuỗi PL)*; lá nào lệch ở WP-C5a mang lớp C5a của nó *(`loi_as_is` · `chua_co_dau_vao` ·
   `lech_D3`)*. **Lan nhãn bằng PHÉP ĐO**: tìm TẬP lớp NHỎ NHẤT mà thay lá lệch thuộc tập ấy bằng giá trị ATL ⇒ dòng
   PL hồi phục *(≤ `ATOL_HOI`)*; nhãn = các lớp nối `+` *(vd `chua_co_dau_vao+lech_D3`: cần CẢ hai mới hồi phục)*.
   ⛔ hồi phục / ⛔ lá lệch nào ⇒ `lech_FLS` *(mong 0)* ⇒ ĐỎ.
⭐ CHECK: mỗi kỳ-khối `dat_co_so` · `dat_0_0` · `do` · `khong_do_duoc` *(`pla.check_atl`)*; kỳ đỏ in TÊN *(kỳ · phép
   · khối · chênh)*. Đối chiếu CHECK của FLS ↔ CHECK của ATL *(cùng hàm trên giá trị ATL — chỉ ở bước so)*: ô khác
   cũng thừa kế lớp từ lá theo cùng phép đo.
"""
from __future__ import annotations

import datetime
import hashlib
import itertools
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Mapping

from fls.bao_cao import pla
from fls.bao_cao.cfa import KHOI_TONG
from fls.cau_hinh import dong_pl
from fls.oracle.cong_parity import PhanXu
from tools import do_hd2_c3d as c3d
from tools import do_hd2_c5a as c5a
from tools.do_hd2 import GOC, nap_anh, nap_fx

ANH_GAG = GOC / "tests" / "fixture" / "dau_vao" / "noem_com_gag.json"
ATOL = c5a.ATOL                     # 1e-12, rtol 0 — cùng WP-C5a *(dòng PL là tổng của ô đã khớp ở 1e-12)*
ATOL_HOI = Decimal("1e-9")          # phép đo HỒI PHỤC + đối chiếu CHECK *(cùng `atol_lech` của WP-C5a)*
#: lớp LÁ của WP-C5a *(`ThanhQuaC5a.lop_o`)* — nhãn thừa kế là tập con của nó
LOP_GOC = ("loi_as_is", "chua_co_dau_vao", "lech_D3")
LECH_FLS = "lech_FLS"


def com_gag_ngoai(anh: Mapping[str, Any] | None = None,
                  fx: Mapping[int, Mapping[str, Decimal]] | None = None) -> dict[tuple[str, str], dict[str, Decimal]]:
    """`COM_GAG` USD triệu = VND ÷ tỷ giá USD ÷ 10⁶ *(dấu ở IX.PL — ⛔ nhân −1)*, khoá `(GROUP, yyyyMmm)`."""
    anh = anh or nap_anh(ANH_GAG)
    fx = fx or nap_fx()
    (ten,) = tuple(dong_pl.DAU_VAO_NGOAI)
    ra: dict[tuple[str, str], dict[str, Decimal]] = {}
    for d in anh["dong"]:
        t = int(d["thang"])
        ra[(KHOI_TONG, f"{t // 100}M{t % 100:02d}")] = {
            ten: Decimal(str(d["com_gag_vnd"])) / Decimal(str(fx[t]["USD"])) / Decimal(10) ** 6}
    return ra


@dataclass(frozen=True)
class MongC5b:
    so: Mapping[str, Any] | None = None


def mong_c5b_mac_dinh() -> MongC5b:
    from tools.do_hd2_c5b_mong import MONG
    return MongC5b(so=MONG)


@dataclass
class ThanhQuaC5b:
    so: dict[str, Any]
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    lech: list[dict[str, Any]] = field(default_factory=list)
    pl: dict[tuple[str, str, str], Decimal] = field(default_factory=dict)


def _sha(dong: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(dong)).encode("utf-8")).hexdigest()


def _tom(ds: list[Mapping[str, str]]) -> dict[str, Any]:
    q = Decimal("1e-12")
    dem = Counter(x["o"].split("#")[0] for x in ds)
    return {"so_o": len(ds), "theo_khoi": dict(sorted(dem.items())),
            "sha256": _sha([f"{x['o']}={Decimal(x['engine']).quantize(q)}|{Decimal(x['dap_an']).quantize(q)}"
                            for x in ds])}


def _thua_ke(kh: str, t: str, la: frozenset[str], lop_o: Mapping[str, str], o: Mapping, atl_o: Mapping,
             ngoai: Mapping[str, Any], f: Callable[[dict], Decimal], dich: Decimal) -> tuple[str, list[str]]:
    """Lan nhãn THẬT: TẬP lớp nhỏ nhất mà thay lá lệch của nó bằng ATL ⇒ `f` hồi phục về `dich`."""
    lech_la = {m: lop_o[f"{kh}#{m}#{t}"] for m in sorted(la) if f"{kh}#{m}#{t}" in lop_o}
    nen = {m: o[(kh, m, t)] for m in la if (kh, m, t) in o}
    nen.update({m: v for m, v in ngoai.items() if m in la})
    lop = sorted(set(lech_la.values()))
    for r in range(1, len(lop) + 1):
        for tap in itertools.combinations(lop, r):
            gt = dict(nen)
            gt.update({m: atl_o[(kh, m, t)] for m, l in lech_la.items() if l in tap and (kh, m, t) in atl_o})
            try:
                if abs(f(gt) - dich) <= ATOL_HOI:
                    return "+".join(tap), [f"{m}:{l}" for m, l in lech_la.items()]
            except dong_pl.LoiPL:
                pass
    return LECH_FLS, [f"{m}:{l}" for m, l in lech_la.items()]


#: trạng thái CHECK → bậc cách nhau xa hơn mọi chênh *(phép đo hồi phục so được cả trạng thái — `H13-R1-01`)*
MA_HOA_TT = {tt: Decimal(10) ** 9 * i for i, tt in enumerate(pla.TRANG_THAI_CHECK)}


def _ma_hoa(x: pla.OCheck) -> Decimal:
    return MA_HOA_TT[x.trang_thai] + (x.chenh if x.chenh is not None else 0)


def _ma_hoa_check(gt: Mapping[str, Any], kh: str, t: str, phep: str, ma_la: frozenset[str] | None) -> Decimal:
    (x,) = [c for c in pla.check_atl({(kh, m, t): v for m, v in gt.items()}, (kh,), (t,), ma_la=ma_la)
            if c.phep == phep]
    return _ma_hoa(x)


def _co_chu_dich(nhan: str) -> bool:
    return nhan != LECH_FLS and set(nhan.split("+")) <= set(LOP_GOC)


def so_sanh_c5b(tq5a: c5a.ThanhQuaC5a, atl: Mapping[str, Any], dinh_nghia: Mapping[str, str],
                ngoai: Mapping[tuple[str, str], Mapping[str, Any]], mong: MongC5b) -> ThanhQuaC5b:
    ly: list[str] = []
    if not tq5a.phan_xu.dat:
        ly.append("nền WP-C5a (ATL của FLS) ĐỎ ⇒ dòng PL ⛔ tin được: " + " | ".join(tq5a.phan_xu.ly_do[:3]))
    hang, _ = c5a.hang_atl(atl)
    cot = [c for c in atl["cot"] if c[:1] == "y"]
    ky_ds = [c5a._ky(c) for c in cot]
    khoi = tuple(c3d.KHOI_12)
    kq = pla.dong_pl_atl(tq5a.o, khoi, ky_ds, dinh_nghia, ngoai)
    atl_o = c5a.gia_tri_atl(atl)
    la: dict[str, frozenset[str]] = {}
    for d in dinh_nghia:
        try:
            la[d] = pla.la_cua_dong(dinh_nghia, d)
        except dong_pl.LoiPL:
            la[d] = frozenset()
    dem: Counter = Counter()
    theo_khoi: dict[str, Counter] = {}
    khong_tinh: Counter = Counter()
    khong_tinh_o: list[dict[str, str]] = []
    lech: list[dict[str, Any]] = []
    mx = Decimal(0)
    for kh, ma, r in hang:
        if ma not in dinh_nghia:
            continue
        dem["hang_pl"] += 1
        tk = theo_khoi.setdefault(kh, Counter())
        for c, t in zip(cot, ky_ds):
            v = r.get(c)
            if v is None or v == "":
                dem["o_trong_dap_an"] += 1
                continue
            try:
                a = Decimal(str(v))
            except InvalidOperation:
                dem["khong_so_duoc"] += 1
                continue
            k = (kh, ma, t)
            if k in kq.khong_tinh:
                ten = f"{ma}|{'+'.join(sorted(kq.khong_tinh[k]))}"
                khong_tinh[ten] += 1
                khong_tinh_o.append({"o": f"{kh}#{ma}#{t}", "engine": "0", "dap_an": str(a)})
                continue
            e = kq.o[k]
            dem["o_so"] += 1
            tk["o_so"] += 1
            if e == 0 and a == 0:
                dem["o_0_0"] += 1
            elif abs(e - a) <= ATOL:
                dem["khop_co_so"] += 1
                mx = max(mx, abs(e - a))
            else:
                tk["lech"] += 1
                bd = pla._bao_dong(dinh_nghia, ma)
                nhan, la_lech = _thua_ke(kh, t, la[ma], tq5a.lop_o, tq5a.o, atl_o, ngoai.get((kh, t), {}),
                                         lambda gt, bd=bd, ma=ma: dong_pl.tinh_pl(gt, bd)[ma], a)
                lech.append({"o": f"{kh}#{ma}#{t}", "engine": str(e), "dap_an": str(a), "lop": nhan,
                             "la_lech": la_lech})
    dem["khop"] = dem["khop_co_so"] + dem["o_0_0"]
    # ── nhãn ──
    theo_lop: dict[str, list[dict[str, Any]]] = {}
    for x in lech:
        theo_lop.setdefault(x["lop"], []).append(x)
    ngoai_ten = [x for x in lech if not _co_chu_dich(x["lop"])]
    co_chu_dich = len(lech) - len(ngoai_ten)
    lop_thua_ke = {k: _tom(v) for k, v in sorted(theo_lop.items()) if _co_chu_dich(k)}
    # bằng chứng ĐỘC LẬP: C5a gán lớp cho CHÍNH ô KPI `PL*` bằng phản thực cả lưới ⇒ nhãn thừa kế phải chứa nó
    nhan_c5a = Counter()
    for x in lech:
        c = tq5a.lop_o.get(x["o"])
        nhan_c5a["khong_co" if c is None else ("trung" if c in x["lop"].split("+") else "khac")] += 1
    # hai định nghĩa: IX.PL ↔ KPI `PL*` của `pla.CONG_THUC_PM` *(H8)* trên CÙNG lưới FLS
    hai = Counter()
    for (kh, d, t), v in kq.o.items():
        if d in pla.TRONG or (kh, d, t) not in tq5a.o:
            continue
        hai["o_so"] += 1
        hai["chenh"] += abs(v - tq5a.o[(kh, d, t)]) > ATOL
    # ── CHECK mỗi kỳ-khối ──
    # `H13-R1-01`: "kỳ-khối rỗng" của phép ① đo trên mã LÁ *(cùng tập cho FLS và ATL — ⛔ KPI cộng dồn `NPC`)*
    chk_f = pla.check_atl(tq5a.o, khoi, ky_ds, ma_la=tq5a.ma_la)
    chk_d = {(x.khoi, x.ky, x.phep): x for x in pla.check_atl(atl_o, khoi, ky_ds, ma_la=tq5a.ma_la)}
    phep_ds = [t for t, _, _ in dong_pl.CHECK]
    dem_f = {p: {tt: 0 for tt in pla.TRANG_THAI_CHECK} for p in phep_ds}
    dem_d = {p: {tt: 0 for tt in pla.TRANG_THAI_CHECK} for p in phep_ds}
    do_theo_ky: dict[str, list[str]] = {}
    ma_chk = {p: frozenset(tr + ph) for p, tr, ph in dong_pl.CHECK}
    dc: Counter = Counter()
    dc_lop: Counter = Counter()
    check_ngoai_ten: list[str] = []
    for x in chk_f:
        dem_f[x.phep][x.trang_thai] += 1
        y = chk_d[(x.khoi, x.ky, x.phep)]
        dem_d[y.phep][y.trang_thai] += 1
        if x.trang_thai == "do":
            do_theo_ky.setdefault(x.ky, []).append(f"{x.phep} @{x.khoi}: {x.chenh.quantize(Decimal('1e-9'))}")
        if y.trang_thai == "khong_do_duoc":
            dc["dap_an_khong_do_duoc"] += 1
            continue
        if x.trang_thai == y.trang_thai and x.chenh is not None and abs(x.chenh - y.chenh) <= ATOL_HOI:
            dc["khop"] += 1
            continue
        # `H13-R1-01`: phép đo hồi phục so CẢ chênh LẪN trạng thái *(⛔ chỉ chênh: ① khác `dat_co_so` ↔ `dat_0_0`
        # khi chênh đã bằng nhau ⇒ phép đo xanh trên tập rỗng — Đ3)*: lá = mã CHECK ∪ mã LÁ *(rỗng của ①)*,
        # `f` = CHÍNH `pla.check_atl` trên lưới một kỳ-khối, mã hoá `chênh + MA_HOA_TT[trạng thái]`.
        tat_ca = frozenset(m for s in ma_chk.values() for m in s) | (tq5a.ma_la or frozenset())
        nhan, _ = _thua_ke(x.khoi, x.ky, tat_ca, tq5a.lop_o, tq5a.o, atl_o, {},
                           lambda gt, x=x: _ma_hoa_check(gt, x.khoi, x.ky, x.phep, tq5a.ma_la), _ma_hoa(y))
        if _co_chu_dich(nhan):
            dc_lop[nhan] += 1
        else:
            check_ngoai_ten.append(f"{x.phep}@{x.khoi}#{x.ky}")
    thu_tu = {t: i for i, t in enumerate(ky_ds)}
    do_theo_ky = dict(sorted(do_theo_ky.items(), key=lambda kv: thu_tu[kv[0]]))
    check = {"fls": dem_f, "dap_an": dem_d, "so_ky_do": len(do_theo_ky),
             "do_sha256": _sha([f"{t}|{x}" for t, v in do_theo_ky.items() for x in v]),
             "doi_chieu_dap_an": {"khop": dc["khop"], "dap_an_khong_do_duoc": dc["dap_an_khong_do_duoc"],
                                  "lop_thua_ke": dict(sorted(dc_lop.items())), "lech_FLS": len(check_ngoai_ten)},
             "do_theo_ky": do_theo_ky}
    so: dict[str, Any] = {"dem": dict(dem), "theo_khoi": {k: dict(v) for k, v in theo_khoi.items()},
                          "khong_tinh": dict(sorted(khong_tinh.items())), "lop_thua_ke": lop_thua_ke,
                          "nhan_c5a": {k: nhan_c5a[k] for k in ("trung", "khac", "khong_co")},
                          "hai_dinh_nghia": {"o_so": hai["o_so"], "chenh": hai["chenh"]},
                          "ngoai_ten_o": sorted(x["o"] for x in ngoai_ten), "check_ngoai_ten": check_ngoai_ten,
                          "max_lech_khop": str(mx)}
    # ── phán quyết *(Đ5 hai chiều)* ──
    m = mong.so
    if dem["o_so"] == 0:
        ly.append("0 ô dòng PL được so ⇒ ⛔ đo được gì (Đ3)")
    if m is None:
        ly.append("`mong` chưa khai ⇒ ⛔ tin (Đ5)")
        m = {}
    lop_thuc = {"dem": dict(dem), "khong_tinh": so["khong_tinh"], "nhan_c5a": so["nhan_c5a"],
                "hai_dinh_nghia": so["hai_dinh_nghia"],
                "check": {k: v for k, v in check.items() if k != "do_theo_ky"}}
    c3d._khac(lop_thuc, m.get("lop"), "lop", ly)
    c3d._khac(lop_thua_ke, m.get("lop_thua_ke"), "lop_thua_ke", ly)
    if m.get("tong_o") is not None and m["tong_o"] != dem["o_so"]:
        ly.append(f"mẫu số tong_o {dem['o_so']} ≠ mong {m['tong_o']}")
    for x in ngoai_ten[:20]:
        ly.append(f"ô dòng PL lệch ngoài tên `{x['o']}`: engine {x['engine']} · ATL {x['dap_an']} · lá lệch "
                  f"{x['la_lech'] or '∅'}")
    if len(ngoai_ten) > 20:
        ly.append(f"… +{len(ngoai_ten) - 20} ô dòng PL lệch ngoài tên")
    for x in check_ngoai_ten[:20]:
        ly.append(f"CHECK lệch đáp án ngoài tên `{x}`")
    px = PhanXu(not ly, tuple(ly))
    pl5 = [x for x in khong_tinh_o]
    hd2 = {
        "bang": "HD2.WP-C5b", "goi": "WP-C5b",
        "mo_ta": "SO.PLA3-ATL: dòng PL2…PL8 từ IX.PL (kho, C12) trên ATL của FLS (đầu ra AL.KEY H12, cờ IX.ALR 2025 "
                 "BẬT ký) ↔ dòng PL của ATL 606; lệch THỪA KẾ lớp từ ô lá (phép đo hồi phục); 2 phép CHECK mỗi "
                 "kỳ-khối",
        "nguon_dau_vao": ["WP-C5a (ATL của FLS — tests/fixture/dau_vao/gl_pl_dau_vao.json + hr_pl_dau_vao.json + "
                          "tests/fixture/cau_hinh/ix_drv.json + IX.ALR kho)", "IX.PL (kho) ← fls/cau_hinh/dong_pl.py",
                          "tests/fixture/dau_vao/noem_com_gag.json + tests/fixture/cau_hinh/ix_fx.json (COM_GAG)"],
        "dap_an": ["tests/fixture/dap_an/atl.json"],
        "khoa": "khối (12) × dòng PL (7) × kỳ (57) của hàng ATL có nhãn PL*; ô là số và IX.PL tính được",
        "dung_sai": {"atol": str(ATOL), "rtol": "0", "atol_hoi_phuc": str(ATOL_HOI),
                     "atol_check": str(pla.ATOL_CHECK), "max_lech_khop": str(mx)},
        "tong_o": dem["o_so"], "mong_tong_o": m.get("tong_o"),
        "o_co_so": dem["o_so"] - dem["o_0_0"], "khop_co_so": dem["khop_co_so"], "o_0_0": dem["o_0_0"],
        "khop": dem["khop"], "lech_co_chu_dich": co_chu_dich,
        "mong_lech_co_chu_dich": sum((v or {}).get("so_o", 0) for v in (m.get("lop_thua_ke") or {}).values()),
        "lech_ngoai_ten": len(ngoai_ten),
        "khop_ghi_chu": "tong_o = ô so (hàng PL* có nhãn của ATL, ô là số, IX.PL tính được) = o_co_so + o_0_0; khop = "
                        "ô khớp THẬT (khop_co_so) + o_0_0; khop + lech_co_chu_dich = tong_o",
        "lech_co_ten": {"lop_thua_ke": lop_thua_ke,
                        "pl5_khong_tinh_duoc": {**_tom(pl5), "ly_do": "IX.PL PL5 = PL4 − COM_GAG; ảnh COM_GAG chỉ "
                                                "có GROUP × 12 tháng 2025 ⇒ ô khác ⛔ có đầu vào (⛔ ngầm 0)",
                                                "theo_loi": so["khong_tinh"]},
                        "o_trong_dap_an": dem["o_trong_dap_an"], "khong_so_duoc": dem["khong_so_duoc"]},
        "nhan_c5a": so["nhan_c5a"], "hai_dinh_nghia": so["hai_dinh_nghia"],
        "chenh_dinh_nghia_mm": [{"dong": pl, "ma": ma, "ly_do": l} for pl, ma, l in dong_pl.CHENH_VOI_MM],
        "check": check,
        "theo_khoi": so["theo_khoi"],
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    return ThanhQuaC5b(so=so, phan_xu=px, hd2_cong=hd2, lech=lech, pl=kq.o)


def _pl_tu_kho(dsn: str | None, conn=None):
    try:
        from fls.repo import cau_hinh_repo as chc
        if conn is not None:
            return chc.doc_pl(conn), None
        import psycopg
        from fls.db.kho import dsn_that
        with psycopg.connect(dsn or dsn_that()) as c:
            return chc.doc_pl(c), None
    except Exception as e:  # noqa: BLE001 — Đ5: ⛔ đo được ⇒ ĐỎ có lý do
        return None, f"IX.PL ⛔ đọc được từ kho: {type(e).__name__}: {' '.join(str(e).split())}"


def _do(ly: tuple[str, ...]) -> ThanhQuaC5b:
    px = PhanXu(False, ly)
    return ThanhQuaC5b(so={}, phan_xu=px, hd2_cong={"bang": "HD2.WP-C5b", "goi": "WP-C5b", "dat": False,
                                                    "ly_do": list(ly)})


def chay_wp_c5b(dsn: str | None = None, conn=None) -> ThanhQuaC5b:
    """IX.PER + IX.ALR + IX.PL ĐỌC TỪ KHO *(`conn` tuỳ chọn — bài chạy trong giao dịch rollback)*."""
    lich, l1 = c5a._lich_tu_conn(conn) if conn is not None else c3d._lich_tu_kho(dsn)
    alr, l2 = c5a._alr_tu_kho(dsn, conn)
    dn, l3 = _pl_tu_kho(dsn, conn)
    if lich is None or alr is None or dn is None:
        return _do(tuple(x for x in (l1, l2, l3) if x))
    gl, hr, _, fx, cay, atl, drv = c5a.nap_nguon()
    den = datetime.date.fromisoformat(c3d.mong_c3d_mac_dinh().so["den"])
    tq5a = c5a.so_sanh_c5a(c5a.tinh_pla3(gl, hr, fx, cay, lich, den), atl, drv, alr, cay, c5a.mong_c5a_mac_dinh())
    return so_sanh_c5b(tq5a, atl, dn, com_gag_ngoai(fx=fx), mong_c5b_mac_dinh())


def in_bao(tq: ThanhQuaC5b) -> None:
    h = tq.hd2_cong
    print("══ WP-C5b · dòng PL (IX.PL kho) trên ATL của FLS ↔ ATL 606 · 2 phép CHECK mỗi kỳ-khối")
    if "tong_o" in h:
        lt = h["lech_co_ten"]
        print(f"  ô so {h['tong_o']} = có số {h['o_co_so']} + 0=0 {h['o_0_0']} · khớp {h['khop']} "
              f"(thật {h['khop_co_so']}/{h['o_co_so']}) · lệch có chủ đích {h['lech_co_chu_dich']} · "
              f"lệch FLS {h['lech_ngoai_ten']}")
        print("  lệch THỪA KẾ từ lá: " + " · ".join(f"{k} {v['so_o']}" for k, v in lt["lop_thua_ke"].items()))
        print(f"  ngoài mẫu số: pl5_khong_tinh_duoc {lt['pl5_khong_tinh_duoc']['so_o']} · ô ATL rỗng "
              f"{lt['o_trong_dap_an']} · khong_so_duoc {lt['khong_so_duoc']}")
        print(f"  hai định nghĩa (IX.PL ↔ KPI pla H8): {h['hai_dinh_nghia']} · nhãn C5a của ô PL: {h['nhan_c5a']}")
        c = h["check"]
        for p, d in c["fls"].items():
            print(f"  CHECK `{p}` (kỳ-khối): " + " · ".join(f"{k} {v}" for k, v in d.items()))
        print(f"  CHECK đối chiếu đáp án: {c['doi_chieu_dap_an']} · kỳ có đỏ {c['so_ky_do']}")
        for t, v in c["do_theo_ky"].items():
            print(f"    đỏ {t}: " + " · ".join(v))
        for x in h["chenh_dinh_nghia_mm"]:
            print(f"  chênh định nghĩa ATL ↔ Mapping Master: {x['dong']} `{x['ma']}` — {x['ly_do']}")
    for x in h.get("ly_do", []):
        print(f"  ⛔ {x}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")
