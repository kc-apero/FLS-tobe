"""`do_hd2.py --goi WP-C3c` — PARITY HD2 họ HR *(ISP 3.1.2 · Step 32 · H7 · WO-245)*: CA.GL dòng HR ↔ `gl_hr_408`
*(PD 408)* + SO.CFA3 ↔ `cfa3` *(MID I Report I CFA3 Daily)*.

⭐ **Đầu vào = THƯỢNG NGUỒN, ⛔ đáp án** *(lượt đầu H7 DỪNG vì thiếu — DT6c / BG-250 đóng băng)*:
`tests/fixture/dau_vao/hr_ledger_2025.json` = file H1000 Ledger *(`1.3 Ledger NIS/INT/COM 2025` + `PIT 2025`, 10.105
hàng)*. Config: IX.FX *(`ix_fx.json`)* · IX.HD *(cây ATL `atl_cay.json` + cột `Code HR Allocate` của Mapping Master)* ·
IX.ORG *(ĐỌC TỪ KHO, C8 — `chay_wp_c3c`; chưa khai ⇒ ĐỎ có lý do)*. ⛔ đọc cột nào của đáp án làm đầu vào.

Chuỗi *(dùng lại — ⛔ chép)*: dòng HR → `gl.hd_final_hr` *(cột V)* + `gl.cdt1_hr` *(`cdt_cua`)* → `tinh_gl` *(H1/H4:
BA = AX ÷ USD tháng × 10³ — công thức `BA10` đọc 19/11, BG-250 §3)* →
  ① **GL HR**: Σ `musd_no`/`musd_co` theo (kỳ, nhãn V) ↔ Σ `BA`/`BB` của 408 cùng khoá;
  ② **CFA3**: `cfa1_daily` *(H5)* với trục = KỲ THÁNG, khối GROUP ↔ Σ các ô NGÀY của `cfa3` trong tháng.
     ⚠ **Hạt THÁNG, ⛔ ngày** *(Đ4)*: ảnh đầu vào chỉ mang `ky` *(khuôn DT6c bỏ cột A sau khi suy kỳ)* ⇒ ô so CFA3
     = mã × tháng. Công thức CFA3 `G13 = SUMIFS(BA, A=ngày, V=nhãn) − SUMIFS(BB, …)` ⇒ Σ theo tháng của nó = đúng
     phép ① gom theo nhãn cây — so được, chỉ mất độ mịn ngày *(câu cho BA: giữ cột A ở ảnh đầu vào?)*.

**Đáp án chính GL = 408** *(⛔ 407 · 413)*: DT6c đối chiếu nguồn ↔ 408 *(lệch theo kỳ đã đo, orchestrator chốt)*; 408
mang 2.302 hàng `ky_suy` *(AC-3)*; 407 = 408 có ngày + 11 hàng LE `#N/A` *(CFA3 đọc 407 — các hàng ấy ⛔ làm lệch ô
CFA3 nào: đo 0 lệch ngoài lớp)*; 413 ⊃ 408 + 1.375 hàng 2024/2025-01·04 *(Y2024 — ⛔ trong đầu vào 2025)*.

── LỚP LỆCH CÓ TÊN *(Đ5: `mong` khai TRƯỚC — khác ⇒ ĐỎ CẢ HAI CHIỀU)* ────────────────────────────────────────────
  · `dap_an_khac_nguon` *(Ô — `lech_co_chu_dich` của hợp đồng CG2)*: ô lệch nằm ĐÚNG kỳ DT6c đo được "đáp án ≠ nguồn"
    *(BG-250 §2: 02 +3 hàng · 06/08/09 +1 · 10 +1.227 *(408 thiếu PIT kỳ 10)* · 12 −269)* + **04** *(cùng số hàng
    & Σ PS Có nhưng PS NỢ của hàng PIT khác — 408 chia lại, như BG-227 §2 ở 413)*. Orchestrator chốt 19/11: khai
    theo kỳ, ⛔ lấp. Số ô mỗi kỳ ở `MongC3c.lech_gl` / `lech_cfa3`.
  · `chua_co_dau_vao`: kỳ của đáp án ⛔ có trong đầu vào *(408: 2026-01 = 269 hàng; CFA3: 2024-10…12 + 2026-01…02)*
    ⇒ ⛔ so, ĐẾM *(hàng · ô tháng ≠ 0)*.
  · `ky_suy`: 2.302 hàng 408 thiếu ngày, gán kỳ "hàng trên" *(DT6b, quyết chủ)* — `BA`/`BB` RỖNG *(A rỗng ⇒ công
    thức ⛔ tra tỷ giá)* ⇒ ⛔ vào Σ, ⛔ hoá 0, ⛔ tính là FLS sai. ĐẾM hàng + Σ PS Có + số hàng `BA`/`BB` rỗng.
  · `thieu_tien_te_D` *(dòng ĐẦU VÀO thiếu D ⇒ AS-IS AX rỗng ⇒ BA 0)* · `hd_mac_dinh_oga` *(I ⛔ khớp `code_hr` ⇒
    `OGA | GAC - Other`)* · `cdt_la` *(theo giá trị nguồn — `COR_Terasofts` khác hoa thường `COR_TeraSofts`)*.
⛔ Mọi ô lệch NGOÀI lớp trên ⇒ ĐỎ. Mẫu số 0 ⇒ ĐỎ *(Đ3)*.

── VÒNG SỬA SAU R1 `KQ-247` ─────────────────────────────────────────────────────────────────────────────────────
  · `H7-R1-01`: `mong.o_lech` khai **từng ô lệch** — khoá `phan|ky|ô` → (engine, đáp án) ⇒ đổi GIÁ TRỊ một ô đã lệch
    ĐỎ *(`ATOL_LECH` 1e-9: engine Decimal tất định, đáp án đọc chuỗi ⇒ ⛔ nhiễu số thực; đột biến R1 B1/B4/B5 ≥ 0,5)*.
    Ô mong lệch mà nay KHỚP cũng ĐỎ *(chiều ngược)*.
  · `H7-R1-02` *(Đ4 — nhãn từng số)*: `tong_o` 888 = **`o_co_so` 269** *(ô mà engine ≠ 0 hoặc đáp án ≠ 0)* + **`o_0_0` 619**
    *(engine = 0 = đáp án)*; `khop` 835 = `khop_co_so` 216 + `o_0_0` 619 *(hợp đồng CG2: `khop` + `lech_co_chu_dich` =
    `tong_o`)*. Khớp THẬT = **216/269**. + cổng MỨC NHÓM `(kỳ, D, E, F, V)` — khối `nhom`: nhóm có CÙNG số dòng ở hai
    bên ⇒ Σ `BA`/`BB` engine ↔ Σ 408; `mong` khai nhóm·dòng ghép **và** dòng ⛔ ghép, lệch = 0 ⇒ khác ⇒ ĐỎ cả hai chiều.
"""
from __future__ import annotations

import datetime
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

from fls.bao_cao.cfa import KHOI_TONG, DongCFA, cfa1_daily
from fls.bao_cao.gl import CdtLaHR, DongGL, ThieuTyGia, TienTeNgoaiGL, cdt1_hr, hd_final_hr, tinh_gl
from fls.cau_hinh import hd as hd_cfg
from fls.cau_hinh import to_chuc
from fls.cau_hinh.hd import CayHD
from fls.oracle.cong_parity import PhanXu
from tools.do_hd2 import GOC, MA_KPI, _chu, _so, nap_anh, nap_cay, nap_fx
from tools.do_hd2_c3c_lech import LECH_O_MONG

ANH_VAO = GOC / "tests" / "fixture" / "dau_vao" / "hr_ledger_2025.json"
ANH_GL = GOC / "tests" / "fixture" / "dap_an" / "gl_hr_408.json"
ANH_CFA3 = GOC / "tests" / "fixture" / "dap_an" / "cfa3.json"
MM = GOC / "tests" / "fixture" / "cau_hinh" / "mapping_master_cfg.json"
CDT_CORRECT = GOC / "tests" / "fixture" / "cau_hinh" / "cdt_correct.json"

COT_GL = ("BA", "BB")
#: Dung sai *(rtol 0)* — đo 19/11 trên ô KHỚP, ⛔ áp dung sai: GL max|lệch| 3,35e-17 · CFA3 9,34e-17 *(|exp| ≤ 0,4)*
#: ⇒ `atol 1e-15` *(≥ ×10)*. Chứng ĐỎ: +1e-12 một ô `BA` đáp án ⇒ đúng ô ấy ĐỎ *(bài `…mot_o_dap_an…`)*.
ATOL = Decimal("1e-15")
#: Dung sai ô LỆCH CÓ TÊN *(H7-R1-01)* — ⛔ nới ATOL: ghim giá trị đã đo, sai ≥ 1e-9 mUSD ⇒ ĐỎ.
ATOL_LECH = Decimal("1e-9")
#: Dung sai Σ nhóm `(kỳ,D,E,F,V)` *(H7-R1-02)* — đo: max|Σeng − Σ408| ở nhóm ghép 3,79e-17 ⇒ atol 1e-15 ≥ ×10.
ATOL_NHOM = Decimal("1e-15")
_EPOCH = datetime.date(1899, 12, 30)


@dataclass(frozen=True)
class MongC3c:
    """Khai TRƯỚC *(Đ4 nhãn · Đ5 khác ⇒ ĐỎ cả hai chiều)* — đo 19/11 bằng nguyên mẫu ĐỘC LẬP *(scratchpad)*."""
    dong_vao: int = 10105               # hàng ảnh đầu vào (NIS 7.585 + PIT 2.520)
    thieu_D: int = 462                  # hàng đầu vào thiếu D ⇒ ⛔ vào tinh_gl
    hd_mac_dinh: int = 20               # hàng I ⛔ khớp code_hr ⇒ OGA
    cdt_la: Mapping[str, int] = field(default_factory=lambda: {
        "COR_Terasofts": 592, "(rỗng)": 59, "INT | Insurance Total": 4, "NIS | Net Income Staff": 3,
        "COM | COM Total": 1})
    ky_so: tuple[str, ...] = tuple(f"2025{m:02d}" for m in range(1, 13))   # kỳ có đầu vào = kỳ so
    gl_o_so: int = 240                  # 12 kỳ × 10 nhãn V (9 code_hr + OGA) × {BA, BB}
    gl_o_khac_0: int = 93               # … ô mà Σ đáp án ≠ 0 (Đ3)
    cfa3_o_so: int = 648                # 54 mã ⛔ KPI × 12 kỳ
    cfa3_o_khac_0: int = 170            # … ô tháng mà Σ đáp án ≠ 0 (nguyên mẫu: 182 ô ≠ 0 trên 17 tháng − 12 ở 2026-01)
    cfa3_o_kpi: int = 240               # 20 mã KPI × 12 kỳ — LOẠI, đếm
    lech_gl: Mapping[str, int] = field(default_factory=lambda: {
        "202502": 2, "202504": 2, "202506": 1, "202508": 1, "202509": 1, "202510": 7, "202512": 6})
    lech_cfa3: Mapping[str, int] = field(default_factory=lambda: {
        "202502": 4, "202504": 3, "202510": 13, "202512": 13})
    ky_suy_hang: int = 2302
    ky_suy_tong_F: Decimal = Decimal("6763528503")
    gl_chua_vao: Mapping[str, int] = field(default_factory=lambda: {"202601": 269})
    cfa3_chua_vao_khac_0: int = 17      # ô THÁNG ngoài kỳ so mà Σ đáp án ≠ 0 — kể cả mã KPI (12 mã thường + 5 KPI, đều 2026-01)
    cfa3_o_loi: int = 5                 # ô '-' của đáp án (2024-10-20) — ngoài kỳ so, ĐẾM
    # ── H7-R1-02 (Đ4): ô tổng tách ô CÓ SỐ khỏi ô 0 = 0 ──
    o_co_so: int = 269                  # ô mà engine ≠ 0 HOẶC đáp án ≠ 0 (GL 93+5 · CFA3 170+1 …đo R1)
    khop_co_so: int = 216               # … trong đó khớp ĐÁP ÁN THẬT (≠ 0)
    o_0_0: int = 619                    # ô engine = 0 = đáp án (GL 142 · CFA3 477) — khớp rỗng
    # ── H7-R1-02: cổng nhóm (kỳ, D, E, F, V) — R1 đo 19/11 bằng nguyên mẫu độc lập ──
    nhom_ghep: int = 4323               # nhóm có CÙNG số dòng ở engine & 408
    nhom_dong_ghep: int = 7952          # … = 7.952 dòng (mỗi bên)
    nhom_lech: int = 0                  # … Σ BA/BB lệch quá ATOL_NHOM
    dong_vao_khong_ghep: int = 1691     # dòng vào engine (9.643) ⛔ ghép được nhóm
    dong_408_khong_ghep: int = 1189     # dòng 408 trong kỳ so ⛔ ghép được nhóm (+ 269 dòng kỳ 2026-01 ở `chua_co_dau_vao` = 1.458 R1)
    # ── H7-R1-01: giá trị từng ô lệch có tên (khoá `phan|ky|ô` → (engine, đáp án)) ──
    o_lech: Mapping[str, tuple[str, str]] = field(default_factory=lambda: dict(LECH_O_MONG))


def mong_c3c_mac_dinh() -> MongC3c:
    return MongC3c()


@dataclass
class ThanhQuaC3c:
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    lech: list[dict[str, Any]] = field(default_factory=list)
    luoi: dict[tuple[str, str, str], Decimal] = field(default_factory=dict)


def nap_code_hr(path: Path = MM) -> Mapping[str, str]:
    return hd_cfg.doc_code_hr_van_ban(path.read_text(encoding="utf-8"), nguon=path.name)


def nap_org_anh() -> to_chuc.ToChuc:
    """IX.ORG từ ẢNH *(bài đơn vị/oracle)*; cổng thật đọc TỪ KHO *(`chay_wp_c3c`)*."""
    return to_chuc.doc_anh(CDT_CORRECT.read_text(encoding="utf-8"), MM.read_text(encoding="utf-8"),
                           nguon=f"{CDT_CORRECT.name} + {MM.name}")


def nap_nguon(org: to_chuc.ToChuc | None = None) -> tuple:
    return (nap_anh(ANH_VAO), nap_anh(ANH_GL), nap_anh(ANH_CFA3), nap_fx(), nap_cay(), nap_code_hr(),
            org or nap_org_anh())


def _ky_ngay(serial: int) -> str:
    d = _EPOCH + datetime.timedelta(days=serial)
    return f"{d.year}{d.month:02d}"


def so_sanh_c3c(vao: dict, gl: dict, cfa3: dict, fx: Mapping[int, Mapping[str, Decimal]], cay: CayHD,
                code_hr: Mapping[str, str], org: to_chuc.ToChuc, mong: MongC3c) -> ThanhQuaC3c:
    ly: list[str] = []
    ky_so = list(mong.ky_so)
    nhan_v = sorted({*code_hr.values(), hd_final_hr(code_hr, None)[0]})

    # ── ① feed: dòng HR → nhãn V + CDT1 (`cdt_cua`) → tinh_gl ──
    feed: list[DongGL] = []
    meta: list[tuple[str, str]] = []
    khoa_nhom: list[tuple] = []         # (kỳ, D, E, F, V) từng dòng vào engine — cổng nhóm (H7-R1-02)
    thieu_D = mac_dinh = 0
    cdt_la: Counter = Counter()
    for r in vao.get("dong", []):
        v, md = hd_final_hr(code_hr, _chu(r.get("hd")))
        mac_dinh += md
        try:
            cdt1_hr(org, _chu(r.get("cdt1")))
        except CdtLaHR as e:
            cdt_la[e.cdt_nguon if isinstance(e.cdt_nguon, str) and e.cdt_nguon.strip() else "(rỗng)"] += 1
        tt = _chu(r.get("D"))
        if not tt:
            thieu_D += 1
            continue
        feed.append(DongGL(thang=int(r["ky"]), tien_te=tt, no=_so(r.get("E")) or Decimal(0),
                           co=_so(r.get("F")) or Decimal(0)))
        meta.append((str(r["ky"]), v))
        khoa_nhom.append((str(r["ky"]), tt, _so(r.get("E")) or Decimal(0), _so(r.get("F")) or Decimal(0), v))
    kq: list = []
    try:
        kq = tinh_gl(feed, fx)
    except (ThieuTyGia, TienTeNgoaiGL) as e:
        ly.append(f"tinh_gl ⛔ chạy được *(⛔ đo được ⇒ ĐỎ)*: {type(e).__name__}: {' '.join(str(e).split())}")
    ky_vao = sorted({k for k, _ in meta})
    if ky_vao != ky_so:
        ly.append(f"kỳ đầu vào {ky_vao} ≠ kỳ so khai {ky_so}")

    luoi: dict[tuple[str, str, str], Decimal] = {}
    eng_gl: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    for (k, v), x in zip(meta, kq):
        eng_gl[(k, v + "·BA")] += x.musd_no
        eng_gl[(k, v + "·BB")] += x.musd_co

    # ── đáp án GL 408: Σ BA/BB theo (kỳ, V); ky_suy ⇒ lớp riêng; kỳ ngoài đầu vào ⇒ chua_co_dau_vao ──
    dap_gl: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    suy_hang = suy_rong = 0
    suy_F = Decimal(0)
    gl_chua: Counter = Counter()
    nhom_408: dict[tuple, list] = defaultdict(lambda: [0, Decimal(0), Decimal(0)])
    for r in gl.get("dong", []):
        if r.get("ky_suy") is not None:
            suy_hang += 1
            suy_F += _so(r.get("F")) or Decimal(0)
            suy_rong += r.get("BA") is None and r.get("BB") is None
            continue
        k, v = str(r["ky"]), _chu(r.get("V"))
        if k not in ky_so:
            gl_chua[k] += 1
            continue
        if v not in nhan_v:
            ly.append(f"408 dòng {r.get('dong_sheet')}: nhãn V ⛔ thuộc {len(nhan_v)} nhãn HR")
            continue
        for c in COT_GL:
            dap_gl[(k, f"{v}·{c}")] += _so(r.get(c)) or Decimal(0)
        n408 = nhom_408[(k, _chu(r.get("D")), _so(r.get("E")) or Decimal(0), _so(r.get("F")) or Decimal(0), v)]
        n408[0] += 1
        n408[1] += _so(r.get("BA")) or Decimal(0)
        n408[2] += _so(r.get("BB")) or Decimal(0)

    lech: list[dict[str, Any]] = []
    lech_ky = {"gl": Counter(), "cfa3": Counter()}
    o_so = {"gl": 0, "cfa3": 0}
    o_khac_0 = {"gl": 0, "cfa3": 0}
    khop = o_0_0 = 0
    lech_o: dict[str, tuple[Decimal, Decimal]] = {}      # ô lệch THỰC (mọi lớp) — H7-R1-01

    def _so_o(phan: str, k: str, o: str, got: Decimal, exp: Decimal, mong_ky: Mapping[str, int]) -> None:
        nonlocal khop, o_0_0
        o_so[phan] += 1
        o_khac_0[phan] += exp != 0
        luoi[(phan, k, o)] = got
        if abs(got - exp) <= ATOL:
            khop += 1
            o_0_0 += abs(got) <= ATOL and abs(exp) <= ATOL      # Đ4: khớp RỖNG tách khỏi khớp có số
            return
        lech_ky[phan][k] += 1
        lech_o[f"{phan}|{k}|{o}"] = (got, exp)

    for k in ky_so:
        for v in nhan_v:
            for c in COT_GL:
                o = f"{v}·{c}"
                _so_o("gl", k, o, eng_gl.get((k, o), Decimal(0)), dap_gl.get((k, o), Decimal(0)), mong.lech_gl)

    # ── ② CFA3: cfa1_daily *(H5)* trên trục KỲ THÁNG, khối GROUP ──
    dong3 = [DongCFA(ngay=int(k), le=None, hd=v, musd_no=x.musd_no, musd_co=x.musd_co)
             for (k, v), x in zip(meta, kq)]
    r3 = cfa1_daily(dong3, cay, [int(k) for k in ky_so], [KHOI_TONG])
    if r3.dong_ngoai_cay or r3.dong_nhan_cha or r3.dong_ngoai_truc:
        ly.append(f"CFA3: dòng ngoài cây {len(r3.dong_ngoai_cay)} · gán nút cha {len(r3.dong_nhan_cha)} · "
                  f"ngoài trục {len(r3.dong_ngoai_truc)} ≠ 0")
    dap3: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    for r in cfa3.get("dong", []):
        if _chu(r.get("le")) != KHOI_TONG:
            ly.append("cfa3: khối ≠ GROUP")
            continue
        dap3[(_chu(r["ma_hd"]), _ky_ngay(int(r["ngay"])))] += Decimal(str(r["gt"]))
    o_loi = len(cfa3.get("phu", {}).get("o_loi", {}).get("dong", []))
    cfa3_chua_khac_0 = sum(1 for (ma, k), x in dap3.items() if k not in ky_so and x != 0)
    loi_trong_ky = [o for o in cfa3.get("phu", {}).get("o_loi", {}).get("dong", [])
                    if _ky_ngay(int(o["ngay"])) in ky_so]
    if loi_trong_ky:
        ly.append(f"cfa3: {len(loi_trong_ky)} ô '-' nằm trong kỳ so ⇒ ⛔ đo được")
    kpi = set(MA_KPI)
    o_kpi = 0
    for n in cay.nut:
        for k in ky_so:
            if n.ma in kpi:
                o_kpi += 1
                continue
            _so_o("cfa3", k, n.ma, r3.o[(KHOI_TONG, n.ma, int(k))], dap3.get((n.ma, k), Decimal(0)),
                  mong.lech_cfa3)

    # ── phân xử *(Đ3 · Đ4 · Đ5)* ──
    # ⭐ H7-R1-01: ô lệch CÓ TÊN = khoá ô nằm trong `mong.o_lech` VÀ giá trị (engine, đáp án) ≤ ATOL_LECH ⇒ ⛔ chỉ đếm ô.
    lech_cd = 0
    for kh, (got, exp) in sorted(lech_o.items()):
        mg = mong.o_lech.get(kh)
        phan, k, o = kh.split("|", 2)
        if mg is None:
            lech.append({"phan": phan, "ky": k, "o": o, "got": str(got), "exp": str(exp)})
        elif abs(got - Decimal(mg[0])) > ATOL_LECH or abs(exp - Decimal(mg[1])) > ATOL_LECH:
            ly.append(f"ô lệch {kh}: engine {got} · đáp án {exp} ≠ mong {mg[0]} · {mg[1]} (chênh engine "
                      f"{got - Decimal(mg[0])} · đáp án {exp - Decimal(mg[1])}; dung sai {ATOL_LECH})")
        else:
            lech_cd += 1
    for kh in sorted(set(mong.o_lech) - set(lech_o)):
        ly.append(f"ô mong lệch {kh} nay KHỚP ⇒ ⛔ đã khai trước")
    tong_o = o_so["gl"] + o_so["cfa3"]
    mong_lech = sum(mong.lech_gl.values()) + sum(mong.lech_cfa3.values())
    o_co_so = tong_o - o_0_0
    khop_co_so = khop - o_0_0

    # ── H7-R1-02 · cổng NHÓM (kỳ, D, E, F, V): nhóm cùng số dòng hai bên ⇒ Σ BA/BB engine ↔ Σ 408 ──
    nhom_vao: dict[tuple, list] = defaultdict(lambda: [0, Decimal(0), Decimal(0)])
    for kn, x in zip(khoa_nhom, kq):
        a = nhom_vao[kn]
        a[0] += 1
        a[1] += x.musd_no
        a[2] += x.musd_co
    nhom_ghep = nhom_dong = nhom_lech = 0
    nhom_max = Decimal(0)
    for kn, a in nhom_vao.items():
        b = nhom_408.get(kn)
        if b is None or b[0] != a[0]:
            continue
        nhom_ghep += 1
        nhom_dong += a[0]
        d = max(abs(a[1] - b[1]), abs(a[2] - b[2]))
        nhom_max = max(nhom_max, d)
        nhom_lech += d > ATOL_NHOM
    dong_vao_kg = len(khoa_nhom) - nhom_dong
    dong_408_kg = sum(b[0] for b in nhom_408.values()) - nhom_dong

    def _so_mong(ten: str, thuc: Any, mg: Any) -> None:
        if thuc != mg:
            ly.append(f"`{ten}` thực {thuc} ≠ mong {mg}")

    _so_mong("dong_vao", len(vao.get("dong", [])), mong.dong_vao)
    _so_mong("thieu_tien_te_D", thieu_D, mong.thieu_D)
    _so_mong("hd_mac_dinh_oga", mac_dinh, mong.hd_mac_dinh)
    _so_mong("cdt_la", dict(sorted(cdt_la.items())), dict(sorted(mong.cdt_la.items())))
    _so_mong("gl.o_so", o_so["gl"], mong.gl_o_so)
    _so_mong("cfa3.o_so", o_so["cfa3"], mong.cfa3_o_so)
    _so_mong("gl.o_so_dap_an_khac_0", o_khac_0["gl"], mong.gl_o_khac_0)
    _so_mong("cfa3.o_so_dap_an_khac_0", o_khac_0["cfa3"], mong.cfa3_o_khac_0)
    _so_mong("cfa3.o_kpi", o_kpi, mong.cfa3_o_kpi)
    _so_mong("gl.lech_theo_ky", dict(sorted(lech_ky["gl"].items())), dict(sorted(mong.lech_gl.items())))
    _so_mong("cfa3.lech_theo_ky", dict(sorted(lech_ky["cfa3"].items())), dict(sorted(mong.lech_cfa3.items())))
    _so_mong("ky_suy.so_hang", suy_hang, mong.ky_suy_hang)
    _so_mong("ky_suy.tong_F", suy_F, mong.ky_suy_tong_F)
    _so_mong("ky_suy.ba_bb_rong", suy_rong, mong.ky_suy_hang)
    _so_mong("chua_co_dau_vao.gl_hang", dict(sorted(gl_chua.items())), dict(sorted(mong.gl_chua_vao.items())))
    _so_mong("chua_co_dau_vao.cfa3_o_thang_khac_0", cfa3_chua_khac_0, mong.cfa3_chua_vao_khac_0)
    _so_mong("cfa3.o_loi", o_loi, mong.cfa3_o_loi)
    _so_mong("o_co_so", o_co_so, mong.o_co_so)
    _so_mong("khop_co_so", khop_co_so, mong.khop_co_so)
    _so_mong("o_0_0", o_0_0, mong.o_0_0)
    _so_mong("nhom.ghep", nhom_ghep, mong.nhom_ghep)
    _so_mong("nhom.dong_ghep", nhom_dong, mong.nhom_dong_ghep)
    _so_mong("nhom.lech", nhom_lech, mong.nhom_lech)
    _so_mong("nhom.dong_vao_khong_ghep", dong_vao_kg, mong.dong_vao_khong_ghep)
    _so_mong("nhom.dong_408_khong_ghep", dong_408_kg, mong.dong_408_khong_ghep)
    if nhom_ghep == 0:
        ly.append("Đ3: 0 nhóm ghép ⇒ ⛔ đo được gì ở mức nhóm")
    if tong_o == 0 or o_khac_0["gl"] == 0 or o_khac_0["cfa3"] == 0:
        ly.append(f"Đ3: mẫu số rỗng — ô so {tong_o} · ô đáp án ≠ 0 GL {o_khac_0['gl']} · CFA3 {o_khac_0['cfa3']}")
    if lech:
        ly.append(f"{len(lech)} ô lệch NGOÀI lớp có tên")
    px = PhanXu(not ly, tuple(ly))

    hop_dong = {
        "bang": "HD2.WP-C3c", "goi": "WP-C3c",
        "mo_ta": "CA.GL dòng HR (hr_ledger_2025 → hd_final_hr + cdt1_hr/cdt_cua → tinh_gl) ↔ 408 Σ BA/BB theo "
                 "(kỳ, nhãn V) + SO.CFA3 (cfa1_daily, trục KỲ tháng, GROUP) ↔ cfa3 Σ ô ngày theo tháng",
        "nguon_dau_vao": "tests/fixture/dau_vao/hr_ledger_2025.json (DT6c — file H1000 Ledger, thượng nguồn)",
        "dap_an": {"gl": "tests/fixture/dap_an/gl_hr_408.json (PD 408 — đáp án chính, ⛔ 407/413: xem docstring)",
                   "cfa3": "tests/fixture/dap_an/cfa3.json (MID I Report I CFA3 Daily — đọc sheet 407)"},
        "khoa": {"gl": "ky(12) × nhan_V(10) × {BA, BB}", "cfa3": "ky(12) × ma_hd(54 ⛔ KPI) — hạt THÁNG (Đ4)"},
        "dung_sai": {"atol": str(ATOL), "rtol": "0",
                     "ghi_chu": "đo 19/11 trên ô khớp: GL 3,35e-17 · CFA3 9,34e-17 ⇒ ≥ ×10"},
        "dong_vao": len(vao.get("dong", [])), "dong_so": len(feed),
        "tong_o": tong_o, "mong_tong_o": mong.gl_o_so + mong.cfa3_o_so,
        "o_co_so": o_co_so, "khop_co_so": khop_co_so, "o_0_0": o_0_0,
        "khop": khop, "lech_co_chu_dich": lech_cd, "mong_lech_co_chu_dich": mong_lech,
        "khop_ghi_chu": "tong_o = o_co_so (ô engine ≠ 0 hoặc đáp án ≠ 0) + o_0_0 (engine = 0 = đáp án); "
                        "khop = khop_co_so + o_0_0 (hợp đồng CG2: khop + lech_co_chu_dich = tong_o) — khớp THẬT "
                        "= khop_co_so/o_co_so; lech_co_chu_dich = ô lệch ĐÚNG khoá ô + giá trị đã khai ở mong "
                        "(dung_sai_lech) — dat khi lech_co_chu_dich = mong, lech_ngoai_ten = 0, nhom.lech = 0",
        "dung_sai_lech": {"atol": str(ATOL_LECH), "rtol": "0",
                          "ghi_chu": "ô lệch có tên khai (engine, đáp án) từng ô ở mong.o_lech; sai > atol ⇒ ĐỎ"},
        "nhom": {"khoa": "(ky, D, E, F, V) — nhóm CÙNG số dòng ở engine & 408; so Σ BA/BB",
                 "dung_sai": {"atol": str(ATOL_NHOM), "rtol": "0"}, "ghep": nhom_ghep, "dong_ghep": nhom_dong,
                 "lech": nhom_lech, "max_lech": f"{nhom_max:.3E}",
                 "dong_vao_khong_ghep": dong_vao_kg, "dong_408_khong_ghep": dong_408_kg},
        "lech_ngoai_ten": len(lech),
        "gl": {"o_so": o_so["gl"], "o_so_dap_an_khac_0": o_khac_0["gl"],
               "lech_theo_ky": dict(sorted(lech_ky["gl"].items()))},
        "cfa3": {"o_so": o_so["cfa3"], "o_so_dap_an_khac_0": o_khac_0["cfa3"], "o_kpi_loai": o_kpi,
                 "lech_theo_ky": dict(sorted(lech_ky["cfa3"].items()))},
        "lech_co_ten": {
            "thieu_tien_te_D": thieu_D, "hd_mac_dinh_oga": mac_dinh,
            "cdt_la": dict(sorted(cdt_la.items(), key=lambda x: -x[1])),
            "ky_suy": {"so_hang": suy_hang, "tong_F": str(suy_F), "ba_bb_rong": suy_rong},
            "chua_co_dau_vao": {"gl_hang": dict(sorted(gl_chua.items())),
                                "cfa3_o_thang_khac_0": cfa3_chua_khac_0, "cfa3_o_loi": o_loi},
        },
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    return ThanhQuaC3c(px, hop_dong, lech, luoi)


def _org_tu_kho(dsn: str | None) -> tuple[to_chuc.ToChuc | None, str | None]:
    """IX.ORG mới nhất TỪ KHO *(C8)*. Kho tắt / chưa khai ⇒ (None, lý do) — ⛔ rơi về ảnh, ⛔ SHQ2."""
    try:
        import psycopg
        from fls.db.kho import dsn_that
        from fls.repo import cau_hinh_repo as chc
        with psycopg.connect(dsn or dsn_that()) as c:
            return chc.doc_org(c), None
    except Exception as e:  # noqa: BLE001 — Đ5: ⛔ đo được ⇒ ĐỎ có lý do
        return None, f"IX.ORG ⛔ đọc được từ kho: {type(e).__name__}: {' '.join(str(e).split())}"


def chay_wp_c3c(dsn: str | None = None) -> ThanhQuaC3c:
    org, loi = _org_tu_kho(dsn)
    if org is None:
        px = PhanXu(False, (loi or "IX.ORG rỗng",))
        return ThanhQuaC3c(px, {"bang": "HD2.WP-C3c", "goi": "WP-C3c", "dat": False, "ly_do": list(px.ly_do)})
    return so_sanh_c3c(*nap_nguon(org), mong_c3c_mac_dinh())


def in_bao(tq: ThanhQuaC3c) -> None:
    h = tq.hd2_cong
    print("══ do_hd2 · WP-C3c — CA.GL dòng HR ↔ 408 (kỳ × V × BA/BB) + SO.CFA3 ↔ cfa3 (kỳ × mã)")
    if "tong_o" in h:
        print(f"  ô so {h['tong_o']} (GL {h['gl']['o_so']} · CFA3 {h['cfa3']['o_so']}) · khớp {h['khop']} · "
              f"lệch có chủ đích {h['lech_co_chu_dich']}/{h['mong_lech_co_chu_dich']} · ngoài tên {h['lech_ngoai_ten']}")
        print(f"  ô có số {h['o_co_so']} (khớp thật {h['khop_co_so']}) · ô 0 = 0 {h['o_0_0']} · "
              f"nhóm (kỳ,D,E,F,V): ghép {h['nhom']['ghep']} = {h['nhom']['dong_ghep']} dòng · lệch {h['nhom']['lech']}")
        print(f"  ô ≠ 0 đáp án: GL {h['gl']['o_so_dap_an_khac_0']} · CFA3 {h['cfa3']['o_so_dap_an_khac_0']}")
        print(f"  lệch theo kỳ: GL {h['gl']['lech_theo_ky']} · CFA3 {h['cfa3']['lech_theo_ky']}")
        print(f"  lớp: {h['lech_co_ten']}")
    for x in tq.lech[:10]:
        print(f"      [{x['phan']} · {x['ky']} · {x['o']}] exp {x['exp']} got {x['got']}")
    for l in tq.phan_xu.ly_do:
        print(f"  ✗ {l}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")
