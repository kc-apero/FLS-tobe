"""`do_hd2.py --goi WP-C5c` — **RP.PL · RP.CF · Daily Report 2 · 3** dựng theo khuôn *(`fls.bao_cao.bao_cao`)* ↔ đáp án
605 · 607 · 608 · 609 · 610 · 615 TỪNG Ô — ISP 3.1.2 · Step 46 · H14 · `WO-311`.

⭐ **Đầu vào = ĐẦU RA ENGINE thượng nguồn, ⛔ đáp án** *(AC-4)*:
   · `cfa1_daily` = lưới `so_sanh_c3a(...).luoi` *(H5 — GL CF `gl_cf_dau_vao.json` → `tinh_gl` → `cfa1_daily`)*;
   · `cfa1_yhqm`  = lưới `so_sanh_c3b(...).luoi` *(H6 — `cuon_ky`)*;
   · `pla3_daily` = lưới `so_sanh_c3d(...).luoi['pla3_pm_hr_daily'].o` *(H8 — GL P&L + HR → PLA3 PM + HR)*;
   · `atl`        = `so_sanh_c5a(...).o` *(H12 AL.KEY, cờ IX.ALR 2025 BẬT ký — đọc từ KHO)* đè dòng `PL*` bằng
                    `so_sanh_c5b(...).pl` *(H13 — IX.PL kho)*; ô `PL5` IX.PL ⛔ tính được ⇒ BỎ khỏi lưới *(⛔ ngầm 0)*.
   Đáp án 605–615 + đáp án thượng nguồn *(409 · 410 · 418 · 606)* chỉ ĐỌC ở bước SO.

── LỚP LỆCH *(Đ5 — `mong` khai TRƯỚC ở `do_hd2_c5c_mong.py`, khác ⇒ ĐỎ CẢ HAI CHIỀU)* ────────────────────────────────
⭐ Ô báo cáo lệch **THỪA KẾ** lớp bằng TRUY NGƯỢC THẬT *(luật `H12-R1-01`: ⛔ quy tắc khối × năm)*: mỗi ô báo cáo là phép
   chiếu của 1–2 ô nguồn *(SHQ = SHQ1 + SHQ2)*. So 3 số cùng khoá: `e` engine · `a` đáp án báo cáo · `s` đáp án NGUỒN.
   · `e ≈ a` ⇒ khớp;
   · `e ≈ s`, `a ≠ s` ⇒ `lech_dap_an_nguon` *(hai ảnh AS-IS của CÙNG ô khác nhau — đóng băng khác ngày)*;
   · `e ≠ s` ⇒ lớp của CHÍNH ô nguồn ở cổng thượng nguồn *(C3a/C3b `lech_ite` ⇒ `ite_alias` · C3d `as_is_truoc_CA` /
     `as_is_416_GAC_thieu_CXA` · C5a `lop_o` · C5b `lop`)*, nối `+`; thêm `+lech_dap_an_nguon` nếu cả `a ≠ s`.
     Ô nguồn lệch mà cổng thượng nguồn ⛔ gán lớp ⇒ `lech_FLS` *(mong 0)*.
⭐ **Ô chỉnh tay** *(ISP mục 3)*: ô lệch có lớp chứa `loi_as_is` và `|e − a| = 0,5` *(±1e-9)* ⇒ liệt kê tên
   "chỉnh tay ⛔ actor" *(gốc: ATL `AH12` `='…'!AH12-0.5` — `phu.o_chinh_tay` của ảnh 605)*; ⛔ chép vào config.
⭐ Phần ⛔ có đầu vào *(FS1 luỹ kế · `hr` · cả 605 · 615)* ⇒ DỪNG, đếm ô đáp án bỏ + câu "cần ảnh nào" *(tiền lệ
   DT7b)*, NGOÀI mẫu số. CHECK của báo cáo: chỉ ĐẾM + LIỆT KÊ *(câu chặn đóng sổ chờ chủ)*.
"""
from __future__ import annotations

import datetime
import hashlib
import re
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from fls.bao_cao import bao_cao as bc
from fls.cau_hinh import dong_pl
from fls.oracle.cong_parity import PhanXu
from tools import do_hd2 as h
from tools import do_hd2_c3d as c3d
from tools import do_hd2_c5a as c5a
from tools import do_hd2_c5b as c5b
from tools.do_hd2 import GOC, nap_anh

DA = GOC / "tests" / "fixture" / "dap_an"
ATOL = Decimal("1e-12")            # rtol 0 — ô báo cáo là CHÍNH ô nguồn (≤ 2 hạng tử) ⇒ cùng ngưỡng C5a/C5b
ATOL_CHINH_TAY = Decimal("1e-9")
CHINH_TAY = Decimal("0.5")
LECH_FLS = "lech_FLS"
LECH_NGUON = "lech_dap_an_nguon"

#: đáp án → (tệp, loại, FS, kỳ) *(kỳ = tháng của trục ngày `From`/`To` — đo ở `BG-270`)*
DAP_AN: dict[str, dict[str, Any]] = {
    "607": {"anh": "daily_report_3_fs2", "loai": "PL", "fs": "FS2", "ky": 202511},
    "608": {"anh": "daily_report_3_fs1", "loai": "PL", "fs": "FS1", "ky": 202511},
    "609": {"anh": "daily_report_3_gop", "loai": "PL", "fs": "FS3", "ky": 202512},
    "610": {"anh": "daily_report_2", "loai": "CF", "fs": "-", "ky": 202611},
}
#: đáp án DỪNG cả bản *(⛔ engine FLS nào sinh được nguồn)* — câu "cần ảnh nào"
DUNG: dict[str, dict[str, str]] = {
    "605": {"anh": "daily_report_3",
            "can": "nguồn `[MID][FS1][PLA5]` (P&L VND theo 8 thực thể × 24 tháng 2024–2025, bản dán giá trị Sign off): "
                   "ảnh `[FS1][PLA3]`/`[PLA5]` Y/H/Q/M trước khi dán + đường VND; FLS ⛔ có engine FS1, và 2024 "
                   "(trước ITL 10/2024) ⛔ có sổ nguồn"},
    "615": {"anh": "ccr_daily_report",
            "can": "nguồn `Cash Balance by LE` (số dư tiền mặt/ngân hàng theo LE × ngày, sổ A-CCR): ảnh số dư quỹ + "
                   "ngân hàng theo ngày; FLS ⛔ có engine số dư (HD4 · CCR ngoài ISP)"},
}


def _so(v: Any) -> Decimal | None:
    if v is None or isinstance(v, (bool, dict)):
        return None
    try:
        return Decimal(str(v))
    except InvalidOperation:
        return None


def _chu(v: Any) -> str | None:
    return v.get("chu") if isinstance(v, dict) else None


# ── đọc khuôn của đáp án *(nhãn hàng + tiêu đề cột — ⛔ giá trị vào engine)* ─────────────────────────────────────────

_TIEN_TO = re.compile(r"^\[(FS\d)\]\[PLA3\] ")


def _tieu_de(anh: Mapping[str, Any]) -> dict[int, dict[str, Any]]:
    by: dict[int, dict[str, Any]] = {}
    for t in anh["phu"]["tieu_de"]["dong"]:
        g = t["gia_tri"]
        by.setdefault(int(t["dong_sheet"]), {})[t["cot"]["chu"].lower()] = _chu(g) if isinstance(g, dict) else g
    return by


def _cot_ky(hd: Mapping[str, Any]) -> dict[str, str]:
    """Hàng tiêu đề luỹ kế *(`2025` · `H1` … `Q4` · `1` … `12` · `2026` …)* ⇒ cột → kỳ `2025H1`/`2025M01`."""
    ra: dict[str, str] = {}
    nam = None
    for c in sorted(hd, key=lambda x: (len(x), x)):
        v = str(hd[c])
        if re.fullmatch(r"20\d\d", v):
            nam = v
            ra[c] = v
        elif nam and v in ("H1", "H2", "Q1", "Q2", "Q3", "Q4"):
            ra[c] = nam + v
        elif nam and v.isdigit() and 1 <= int(v) <= 12:
            ra[c] = f"{nam}M{int(v):02d}"
    return ra


def o_dap_an(ma_da: str, anh: Mapping[str, Any]) -> tuple[dict[str, Decimal], Counter]:
    """Đáp án ⇒ {khoá ô báo cáo → số}; cột ⛔ thuộc trục *(`F` ngày trước · `AK` ⛔ ngày)* đếm riêng có tên."""
    cfg = DAP_AN[ma_da]
    td = _tieu_de(anh)
    nam, thang = divmod(cfg["ky"], 100)
    hd5 = td.get(5, {})
    cot_ngay: dict[str, str] = {}
    for c, v in hd5.items():
        s = _so(v)
        if s is not None and 40000 < s < 50000:
            d = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(s))
            if (d.year, d.month) == (nam, thang):
                cot_ngay[c] = d.isoformat()
    hd_ky = sorted((r, _cot_ky(m)) for r, m in td.items() if str(m.get("g")) in ("2024", "2025", "2026"))
    ra: dict[str, Decimal] = {}
    ngoai = Counter()
    for r in anh["dong"]:
        ds = int(r["dong_sheet"])
        ph = _chu(r.get("phan")) or _chu(r.get("che_do"))
        kh, ma = _chu(r.get("khoi")), _chu(r.get("ma"))
        if kh is None or ma is None:
            ngoai["hang_khong_nhan"] += 1
            continue
        if ph in (None, "ngay"):
            phan, cot = "ngay", cot_ngay
        else:
            m = _TIEN_TO.match(kh)
            if cfg["loai"] == "CF":
                phan = ph
            else:
                phan = "luy_ke:" + (m.group(1) if m else ("FS1" if cfg["fs"] == "FS1" else "FS2"))
            kh = _TIEN_TO.sub("", kh)
            tr = [x for x in hd_ky if x[0] < ds]
            cot = tr[-1][1] if tr else {}
        for c, v in r.items():
            if len(c) > 2 or not c.isalpha():
                continue
            s = _so(v)
            if s is None:
                continue
            if c not in cot:
                ngoai[f"{phan}:{c}"] += 1
                continue
            ra[bc.khoa_o(phan, kh, ma, cot[c])] = s
    return ra, ngoai


# ── nguồn engine + lớp của ô nguồn ở cổng thượng nguồn ─────────────────────────────────────────────────────────────

@dataclass
class NguonEngine:
    luoi: dict[str, dict[tuple, Decimal]]
    lop: dict[str, dict[tuple, str]]                     # nguồn → (khối, mã, cột) → lớp ở cổng thượng nguồn
    dap_an: dict[str, dict[tuple, Decimal]]              # nguồn → giá trị đáp án THƯỢNG NGUỒN *(chỉ bước so)*
    cong: dict[str, bool]                                # cổng thượng nguồn ĐẠT?
    pl5_bo: int = 0
    tom: dict[str, tuple[set[str], int]] = field(default_factory=dict)   # bộ nhớ đệm (mã có · cột ngày lớn nhất)


def _dap_an_thua(anh: Mapping[str, Any], cot: str) -> dict[tuple, Decimal]:
    """Ảnh thưa *(409 · 410 · 418: ô 0/vắng ⇒ 0)* ⇒ {(khối, mã, cột) → số}."""
    ra: dict[tuple, Decimal] = {}
    for r in anh["dong"]:
        k = r[cot]
        k = int(k) if cot == "ngay" else _chu(k)
        s = _so(r["gt"])
        if s is not None:
            ra[(_chu(r["le"]), _chu(r["ma_hd"]), k)] = s
    return ra


def nguon_engine(lich, alr, dinh_nghia: Mapping[str, str]) -> NguonEngine:
    fx, cay = h.nap_fx(), h.nap_cay()
    gl_cf = nap_anh(h.ANH_CFA1.parent / "gl_cf_dau_vao.json")
    a = h.so_sanh_c3a(gl_cf, nap_anh(h.ANH_CFA1), fx, cay, lich, h.mong_c3a_mac_dinh())
    b = h.so_sanh_c3b(gl_cf, nap_anh(DA / "cfa1_yhqm.json"), fx, cay, lich, h.mong_c3b_mac_dinh())
    gl, hr, tabs, _fx, _cay = c3d.nap_nguon()
    den = datetime.date.fromisoformat(c3d.mong_c3d_mac_dinh().so["den"])
    d = c3d.so_sanh_c3d(gl, hr, tabs, fx, cay, lich, den, c3d.mong_c3d_mac_dinh())
    atl, drv = nap_anh(c5a.ANH_ATL), nap_anh(c5a.ANH_DRV)
    t5a = c5a.so_sanh_c5a(d.luoi["pla3_pm_hr_yhqm"], atl, drv, alr, cay, c5a.mong_c5a_mac_dinh())
    t5b = c5b.so_sanh_c5b(t5a, atl, dinh_nghia, c5b.com_gag_ngoai(fx=fx), c5b.mong_c5b_mac_dinh())
    # ── ATL của FLS = lưới C5a, dòng PL* đè bằng IX.PL (C5b); PL5 IX.PL ⛔ tính được ⇒ BỎ ──
    luoi_atl = dict(t5a.o)
    pl_ma = set(dinh_nghia)
    bo = [k for k in luoi_atl if k[1] in pl_ma and k not in t5b.pl]
    for k in bo:
        del luoi_atl[k]
    luoi_atl.update(t5b.pl)
    lop_atl = {tuple(k.split("#")): v for k, v in t5a.lop_o.items()}
    lop_atl.update({tuple(x["o"].split("#")): x["lop"] for x in t5b.lech})
    lop_cfa1 = {(x["le"], x["ma"], int(x["ngay"])): "ite_alias" for x in a.lech_ite}
    lop_yhqm = {(x["le"], x["ma"], x["ky"]): "ite_alias" for x in b.lech_ite}
    lop_pla3: dict[tuple, str] = {}
    for x in d.lech:
        if x["tab"] != "pla3_pm_hr_daily":
            continue
        kh, ma, t = x["o"].split("#")
        lop_pla3[(kh, ma, int(t))] = "as_is_truoc_CA" if c3d.la_truoc_ca(x) else "as_is_416_GAC_thieu_CXA"
    pla3 = d.luoi["pla3_pm_hr_daily"].o
    # ── KPI của CFA1 *(`MA_KPI`)*: engine H5/H6 ⛔ tính *(ô 0 giữ chỗ — C3a/C3b LOẠI có tên `o_kpi`)* ⇒ BỎ khỏi lưới,
    #    ⛔ để báo cáo in 0 ngầm *(đo 22/11: 2.948 ô luỹ kế 610 "lệch FLS" chính là ô KPI giữ chỗ này)* ──
    kpi = set(h.MA_KPI)
    cfa1 = {k: v for k, v in a.luoi.items() if k[1] not in kpi}
    yhqm = {k: v for k, v in b.luoi.items() if k[1] not in kpi}
    return NguonEngine(
        luoi={"cfa1_daily": cfa1, "cfa1_yhqm": yhqm, "pla3_daily": dict(pla3), "atl": luoi_atl},
        lop={"cfa1_daily": lop_cfa1, "cfa1_yhqm": lop_yhqm, "pla3_daily": lop_pla3, "atl": lop_atl},
        dap_an={"cfa1_daily": _dap_an_thua(nap_anh(h.ANH_CFA1), "ngay"),
                "cfa1_yhqm": _dap_an_thua(nap_anh(DA / "cfa1_yhqm.json"), "ky"),
                "pla3_daily": _dap_an_thua(nap_anh(DA / "pla3_pm_hr_daily.json"), "ngay"),
                "atl": c5a.gia_tri_atl(atl)},
        cong={"WP-C3a": a.phan_xu.dat, "WP-C3b": b.phan_xu.dat, "WP-C3d": d.phan_xu.dat,
              "WP-C5a": t5a.phan_xu.dat, "WP-C5b": t5b.phan_xu.dat},
        pl5_bo=len(bo))


# ── so ─────────────────────────────────────────────────────────────────────────────────────────────────────────────

def _nguon_cua(bao: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {p["id"]: p for p in bao["phan"]}


def _khoi_engine(phan: str, nhan: str) -> tuple[str, ...]:
    for n, k in bc.KHOI_LE + bc.KHOI_CDT:
        if n == nhan:
            return k
    return (nhan,)


def _cot_nguon(truc: str, c: str) -> Any:
    if truc == "ngay":
        return (datetime.date.fromisoformat(c) - datetime.date(1899, 12, 30)).days
    return c


def _lop_lech(ne: NguonEngine, nguon: str, truc: str, khoi: str, ma: str, c: str, e: Decimal, a: Decimal) -> str:
    """TRUY NGƯỢC THẬT về ô nguồn *(xem đầu tệp)*."""
    cn = _cot_nguon(truc, c)
    kh_e = _khoi_engine("", khoi)
    da = ne.dap_an[nguon]
    thua = nguon != "atl"
    s = Decimal(0)
    for k in kh_e:
        v = da.get((k, ma, cn))
        if v is None and not thua:
            return LECH_FLS                                  # ô nguồn ⛔ có ở đáp án nguồn ⇒ ⛔ truy được
        s += v or Decimal(0)
    a_khac_s = abs(a - s) > ATOL
    if abs(e - s) <= ATOL:
        return LECH_NGUON if a_khac_s else LECH_FLS
    lop: set[str] = set()
    for k in kh_e:
        ev = ne.luoi[nguon].get((k, ma, cn))
        sv = da.get((k, ma, cn), Decimal(0))
        if ev is not None and abs(ev - sv) <= ATOL:
            continue
        l = ne.lop[nguon].get((k, ma, cn))
        if l is None:
            return LECH_FLS
        lop.update(l.split("+"))
    if a_khac_s:
        lop.add(LECH_NGUON)
    return "+".join(sorted(lop)) if lop else LECH_FLS


def ly_do_vang(ne: NguonEngine, p: Mapping[str, Any], ma: str, c: str) -> str:
    """Ô đáp án mà báo cáo engine ⛔ có ⇒ lý do CÓ TÊN *(⛔ một rổ "vắng")*."""
    luoi = ne.luoi[p["nguon"]]
    if p["nguon"] not in ne.tom:
        ne.tom[p["nguon"]] = ({k[1] for k in luoi}, max((k[2] for k in luoi if isinstance(k[2], int)), default=0))
    ma_co, cot_max = ne.tom[p["nguon"]]
    if p["nguon"].startswith("cfa1") and ma in h.MA_KPI:
        return "kpi_cfa1_engine_chua_tinh"                 # C3a/C3b loại KPI (o_kpi)
    if p["nguon"] == "atl" and ma in dong_pl.DINH_NGHIA:
        return f"{ma}_ix_pl_khong_tinh_duoc"              # C5b `pl5_khong_tinh_duoc`
    if ma not in ma_co:
        return f"ma_ngoai_luoi:{ma}"                      # mã có ở sổ, ⛔ ở cây IX.HD của engine
    if p["truc"] == "ngay":
        cn = _cot_nguon("ngay", c)
        if cn > cot_max:
            return "ngay_sau_ngay_doc_dau_vao"
    return "khac"


def _sha(ds: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ds)).encode("utf-8")).hexdigest()


def so_mot(ma_da: str, anh: Mapping[str, Any], bao: Mapping[str, Any], ne: NguonEngine) -> dict[str, Any]:
    """So TỪNG Ô một đáp án với báo cáo engine. Trả số đếm *(Đ4 — mỗi khoá nói nó đếm gì)*."""
    da, ngoai = o_dap_an(ma_da, anh)
    phan = _nguon_cua(bao)
    dem = Counter()
    chua = Counter()
    vang = Counter()
    lech: list[dict[str, str]] = []
    mx = Decimal(0)
    for k, a in sorted(da.items()):
        ph, kh, ma, c = k.split("|")
        p = phan.get(ph)
        if p is None or p.get("dung"):
            chua[ph] += 1
            continue
        e = bao["o"].get(k)
        if e is None:
            vang[ly_do_vang(ne, p, ma, c)] += 1
            continue
        e = Decimal(e)
        dem["tong_o"] += 1
        if e == 0 and a == 0:
            dem["o_0_0"] += 1
        elif abs(e - a) <= ATOL:
            dem["khop_co_so"] += 1
            mx = max(mx, abs(e - a))
        else:
            lech.append({"o": k, "engine": str(e), "dap_an": str(a),
                         "lop": _lop_lech(ne, p["nguon"], p["truc"], kh, ma, c, e, a)})
    dem["khop"] = dem["khop_co_so"] + dem["o_0_0"]
    dem["o_co_so"] = dem["tong_o"] - dem["o_0_0"]
    q = Decimal("1e-12")
    theo_lop: dict[str, list[dict[str, str]]] = {}
    for x in lech:
        theo_lop.setdefault(x["lop"], []).append(x)
    lop = {l: {"so_o": len(v), "sha256": _sha([f"{x['o']}={Decimal(x['engine']).quantize(q)}|"
                                                f"{Decimal(x['dap_an']).quantize(q)}" for x in v])}
           for l, v in sorted(theo_lop.items())}
    chinh_tay = sorted(x["o"] for x in lech if "loi_as_is" in x["lop"].split("+")
                       and abs(abs(Decimal(x["engine"]) - Decimal(x["dap_an"])) - CHINH_TAY) <= ATOL_CHINH_TAY)
    vang_ma = Counter()
    for k, n in vang.items():
        vang_ma[k] += n
    return {"dem": dict(dem), "lop": lop, "chua_co_dau_vao": dict(sorted(chua.items())),
            "engine_vang": dict(sorted(vang_ma.items())), "ngoai_truc": dict(sorted(ngoai.items())),
            "chinh_tay": chinh_tay, "max_lech_khop": str(mx),
            "lech_FLS": sorted(x["o"] for x in lech if x["lop"] == LECH_FLS),
            "_lech": lech}


def dem_dap_an_dung(anh: Mapping[str, Any]) -> int:
    """Số ô SỐ của đáp án DỪNG *(mẫu số bị bỏ — Đ3: phải > 0 để câu "dừng" có nghĩa)*."""
    n = 0
    for r in anh["dong"]:
        for c, v in r.items():
            if c not in ("thu_tu", "dong_sheet", "cap") and _so(v) is not None and not isinstance(v, dict):
                n += 1
    return n


@dataclass(frozen=True)
class MongC5c:
    so: Mapping[str, Any] | None = None


def mong_c5c_mac_dinh() -> MongC5c:
    from tools.do_hd2_c5c_mong import MONG
    return MongC5c(so=MONG)


@dataclass
class ThanhQuaC5c:
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    theo_dap_an: dict[str, Any] = field(default_factory=dict)
    bao: dict[str, dict[str, Any]] = field(default_factory=dict)


def _khac(thuc: Any, mong: Any, duong: str, ly: list[str]) -> None:
    c3d._khac(thuc, mong, duong, ly)


def dung_bao(ne: NguonEngine) -> dict[str, dict[str, Any]]:
    """Dựng 4 báo cáo bằng CÙNG engine *(FS là tham số)* — đầu vào = lưới engine."""
    return {m: bc.daily_report(cfg["ky"], cfg["fs"], ne.luoi, loai=cfg["loai"]) for m, cfg in DAP_AN.items()}


def so_sanh_c5c(ne: NguonEngine, dap_an: Mapping[str, Mapping[str, Any]], mong: MongC5c,
                bao: Mapping[str, Mapping[str, Any]] | None = None) -> ThanhQuaC5c:
    ly: list[str] = []
    for g, ok in ne.cong.items():
        if not ok:
            ly.append(f"nền {g} ĐỎ ⇒ lưới engine ⛔ tin được")
    bao = dict(bao) if bao is not None else dung_bao(ne)
    m = mong.so
    if m is None:
        ly.append("`mong` chưa khai ⇒ ⛔ tin (Đ5)")
        m = {}
    theo: dict[str, Any] = {}
    tong = Counter()
    lop_tong = Counter()
    for ma_da in DAP_AN:
        r = so_mot(ma_da, dap_an[ma_da], bao[ma_da], ne)
        lech = r.pop("_lech")
        theo[ma_da] = r
        for k in ("tong_o", "khop", "khop_co_so", "o_0_0", "o_co_so"):
            tong[k] += r["dem"].get(k, 0)
        for l, v in r["lop"].items():
            lop_tong[l] += v["so_o"]
        if r["dem"].get("tong_o", 0) == 0:
            ly.append(f"{ma_da}: 0 ô được so ⇒ ⛔ đo được gì (Đ3)")
        for x in [x for x in lech if x["lop"] == LECH_FLS][:10]:
            ly.append(f"{ma_da}: ô lệch FLS `{x['o']}`: engine {x['engine']} · đáp án {x['dap_an']}")
        mg = (m.get("dap_an") or {}).get(ma_da)
        thuc = {k: v for k, v in r.items() if k not in ("max_lech_khop",)}
        _khac(thuc, mg, f"dap_an.{ma_da}", ly)
    dung: dict[str, Any] = {}
    for ma_da, cfg in DUNG.items():
        n = dem_dap_an_dung(dap_an[ma_da])
        dung[ma_da] = {"o_dap_an_so": n, "can": cfg["can"], "trang_thai": "chua_co_dau_vao"}
        if n == 0:
            ly.append(f"{ma_da}: đáp án DỪNG mà 0 ô số ⇒ câu 'dừng' ⛔ nghĩa (Đ3)")
    _khac({k: v["o_dap_an_so"] for k, v in dung.items()}, m.get("dung"), "dung", ly)
    check = {ma_da: {"theo_phan": b["check"]["theo_phan"], "so_do": b["check"]["so_do"],
                     "do_sha256": _sha(b["check"]["do"])} for ma_da, b in bao.items()}
    _khac(check, m.get("check"), "check", ly)
    fs = {ma_da: {"fs": b["fs"], "phan": [p["id"] for p in b["phan"]]} for ma_da, b in bao.items()}
    lech_co_chu_dich = sum(v for l, v in lop_tong.items() if l != LECH_FLS)
    px = PhanXu(not ly, tuple(ly))
    hd2 = {
        "bang": "HD2.WP-C5c", "goi": "WP-C5c",
        "mo_ta": "RP.PL · RP.CF: Daily Report 2 · 3 dựng theo khuôn (fls.bao_cao.bao_cao.daily_report, FS tham số) từ "
                 "lưới engine (CFA1 H5/H6 · PLA3 PM+HR H8 · ATL H12+H13) ↔ đáp án 607 · 608 · 609 · 610 từng ô; "
                 "605 · 615 DỪNG (chua_co_dau_vao); lệch THỪA KẾ lớp bằng truy ngược ô nguồn",
        "nguon_dau_vao": ["WP-C3a lưới cfa1_daily (tests/fixture/dap_an/gl_cf_dau_vao.json)", "WP-C3b lưới cfa1_yhqm",
                          "WP-C3d lưới pla3_pm_hr_daily (gl_pl_dau_vao.json + hr_pl_dau_vao.json)",
                          "WP-C5a + WP-C5b lưới ATL của FLS (IX.ALR kho cờ 2025 BẬT ký · IX.PL kho)"],
        "dap_an": [f"tests/fixture/dap_an/{c['anh']}.json" for c in DAP_AN.values()],
        "dap_an_dung": dung,
        "khoa": "đáp án × phần (ngay · luy_ke[:FS]) × khối × mã × cột (ngày ISO | kỳ); ô đáp án là số, cột thuộc trục, "
                "phần có đầu vào, engine có ô",
        "dung_sai": {"atol": str(ATOL), "rtol": "0", "chinh_tay": f"|e−a| = {CHINH_TAY} ± {ATOL_CHINH_TAY}"},
        "tong_o": tong["tong_o"], "mong_tong_o": sum(((m.get("dap_an") or {}).get(x) or {}).get("dem", {})
                                                     .get("tong_o", 0) for x in DAP_AN) or None,
        "o_co_so": tong["o_co_so"], "khop_co_so": tong["khop_co_so"], "o_0_0": tong["o_0_0"],
        "khop": tong["khop"], "lech_co_chu_dich": lech_co_chu_dich,
        "mong_lech_co_chu_dich": sum(v.get("so_o", 0) for x in DAP_AN
                                     for l, v in (((m.get("dap_an") or {}).get(x) or {}).get("lop") or {}).items()
                                     if l != LECH_FLS),
        "lech_ngoai_ten": lop_tong.get(LECH_FLS, 0),
        "khop_ghi_chu": "tong_o = Σ 4 đáp án ô so = o_co_so + o_0_0; khop = ô khớp THẬT (khop_co_so) + o_0_0; "
                        "khop + lech_co_chu_dich = tong_o; ô chua_co_dau_vao / engine_vang / ngoai_truc NGOÀI mẫu số",
        "lech_co_ten": {"lop_thua_ke": dict(sorted(lop_tong.items())),
                        "chinh_tay_actor": {x: theo[x]["chinh_tay"] for x in DAP_AN if theo[x]["chinh_tay"]},
                        "chinh_tay_goc": "ATL AH12 `='Report I PLA3 Y H Q M | PM + HR'!AH12-0.5` (GROUP·OMC·2025M02, "
                                         "lan SHQ2 dư) — chỉnh tay ⛔ actor; ⛔ chép vào config"},
        "fs_tham_so": fs,
        "check": check,
        "theo_dap_an": theo,
        "pl5_bo_khoi_luoi": ne.pl5_bo,
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    return ThanhQuaC5c(phan_xu=px, hd2_cong=hd2, theo_dap_an=theo, bao=bao)


def nap_nen_kho(conn, *, actor: str = "bai-h14") -> None:
    """Nạp nền cấu hình cổng vào kho *(bài: giao dịch ROLLBACK; `--ghi`: kho TEST — `PG_DSN_TEST`)*: IX.PER *(21/10,
    luật A)* · IX.ALR *(17 luật MM `@202501` rồi KÝ BẬT 2025 = `ix_alr_2025_bat.json` — quyết chủ 22/11)* · IX.PL.
    ⛔ kho THẬT *(nơi gọi chọn `conn`)*; ⛔ IX.TMP *(bản ký là ĐẦU RA, đưa riêng bằng `dua_ban_ky`)*."""
    from fls.cau_hinh import luat_pb
    from fls.repo import cau_hinh_repo as chc
    chc.nap_ix_per(conn, actor=actor, ngay_dau="2024-10-21", luat="A",
                   nguon=f"{actor}:ISP-3.1.2-Step46 (IX.PER = 21/10, C6)")
    nen = c5a.alr_tu_anh_mm()
    chc.nap(conn, luat_pb.BANG, [(luat_pb.khoa_cua(x.hd, x.tu_ky),
                                  {"hd": x.hd, "tu_ky": x.tu_ky, "nhan_mm": x.nhan_mm, "bat": x.bat,
                                   "ngoai_le": list(x.ngoai_le_cdt1)}) for x in nen.luat],
            nguon=f"{actor}:{c5a.ANH_MM.name}", actor=actor)
    import json
    nguoi_ky = json.loads(c5a.TEP_KY.read_text(encoding="utf-8"))["ky"]["nguoi_ky"]   # chữ ký CỦA người trong tệp
    chc.ky_bat_ix_alr(conn, str(c5a.TEP_KY), actor=nguoi_ky)
    chc.nap_ix_pl(conn, actor=actor)


def nap_dap_an() -> dict[str, dict[str, Any]]:
    ra = {m: nap_anh(DA / f"{c['anh']}.json") for m, c in DAP_AN.items()}
    ra.update({m: nap_anh(DA / f"{c['anh']}.json") for m, c in DUNG.items()})
    return ra


def _do(ly: tuple[str, ...]) -> ThanhQuaC5c:
    return ThanhQuaC5c(phan_xu=PhanXu(False, ly), hd2_cong={"bang": "HD2.WP-C5c", "goi": "WP-C5c", "dat": False,
                                                             "ly_do": list(ly)})


def chay_wp_c5c(dsn: str | None = None, conn=None) -> ThanhQuaC5c:
    """IX.PER + IX.ALR + IX.PL ĐỌC TỪ KHO *(`conn` tuỳ chọn — bài chạy trong giao dịch rollback)*."""
    lich, l1 = c5a._lich_tu_conn(conn) if conn is not None else c3d._lich_tu_kho(dsn)
    alr, l2 = c5a._alr_tu_kho(dsn, conn)
    dn, l3 = c5b._pl_tu_kho(dsn, conn)
    if lich is None or alr is None or dn is None:
        return _do(tuple(x for x in (l1, l2, l3) if x))
    return so_sanh_c5c(nguon_engine(lich, alr, dn), nap_dap_an(), mong_c5c_mac_dinh())


def in_bao(tq: ThanhQuaC5c) -> None:
    hh = tq.hd2_cong
    print("══ WP-C5c · RP.PL · RP.CF Daily Report 2 · 3 (khuôn, FS tham số) ↔ 605 · 607–610 · 615 từng ô")
    for ma_da, r in hh.get("theo_dap_an", {}).items():
        d = r["dem"]
        print(f"  {ma_da} ({DAP_AN[ma_da]['fs']}): ô so {d.get('tong_o', 0)} = có số {d.get('o_co_so', 0)} + 0=0 "
              f"{d.get('o_0_0', 0)} · khớp {d.get('khop', 0)} (thật {d.get('khop_co_so', 0)}) · lệch theo lớp "
              + (" · ".join(f"{k} {v['so_o']}" for k, v in r["lop"].items()) or "0")
              + f" · chua_co_dau_vao {sum(r['chua_co_dau_vao'].values())} · engine vắng "
              f"{sum(r['engine_vang'].values())} · ngoài trục {sum(r['ngoai_truc'].values())} · chỉnh tay "
              f"{len(r['chinh_tay'])}")
    for ma_da, v in hh.get("dap_an_dung", {}).items():
        print(f"  {ma_da}: DỪNG — {v['o_dap_an_so']} ô số ⛔ so · cần: {v['can']}")
    if "tong_o" in hh:
        print(f"  Σ ô so {hh['tong_o']} · khớp {hh['khop']} (thật {hh['khop_co_so']}/{hh['o_co_so']}) · lệch có chủ "
              f"đích {hh['lech_co_chu_dich']} · lệch FLS {hh['lech_ngoai_ten']}")
        for ma_da, c in hh["check"].items():
            print(f"  CHECK {ma_da}: đỏ {c['so_do']} · " + " · ".join(
                f"{p}: " + ", ".join(f"{ph} {dict((k, v) for k, v in d.items() if v)}" for ph, d in x.items())
                for p, x in c["theo_phan"].items()))
    for x in hh.get("ly_do", []):
        print(f"  ⛔ {x}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")
