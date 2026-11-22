"""Khuôn đóng băng `gl_pl_dau_vao` — ĐẦU VÀO PLA của sổ P&L · tab `Report I General Ledger`.

    python tools/dong_bang_sheet.py gl_pl_dau_vao <bản_thô.json> --mong 7883
        ⇒ tests/fixture/dau_vao/gl_pl_dau_vao.json

⭐ **Vì sao có khuôn này** *(ISP 3.1.2 · DT7b · `WO-281`)*. H8 *(`WO-277`)* DỪNG đúng luật AC-2: đáp án PLA1 *(414)*
= `SUMIFS(GL!$BR, GL!$DE, <ngày>, GL!$V, <mã HD>) − SUMIFS(GL!$BS, …)`, mà ảnh đầu vào `gl_406_dau_vao` chỉ giữ
`A·D·E·F·R` *(⛔ `V` · ⛔ `P` · ⛔ `BR`/`BS` · ⛔ `DE`)*. Khuôn này **MỞ RỘNG** ảnh ấy: GỌI hằng của
`gl_406_dau_vao` *(`TIEN_TE` · `ITL_*` · `LECH_CO_TEN` · `_phan_bo_ledger` — ⛔ chép)*, thêm các cột còn thiếu.
`gl_406_dau_vao` và mọi ảnh cũ giữ TỪNG BYTE *(bài `test_dap_an_pl_dau_vao`)*.

⭐ **CÔNG THỨC `DE`** *(đọc 22/11 bằng FORMULA, chỉ-đọc — ô `DE10`; mọi ô `DE11…` là phần TRÀN của nó)*:
    `=ArrayFormula(DATE(left(AH10:AH,4),RIGHT(AH10:AH,2),1))`
⇒ `DE` = ngày MÙNG 1 của tháng `yyyymm` ghi ở cột **`AH`** *(= "Thời điểm bắt đầu sử dụng dịch vụ" · nhóm `Final`,
**HẰNG DÁN** `yyyymm`, ⛔ công thức — đọc FORMULA `AH10/11/3000/5487/7000` đều là hằng)*. Cột NGUỒN = `AH`, cùng tab,
cùng sổ, ⛔ PII ⇒ đóng băng CẢ `AH` *(`WO-281` AC-1)*. ⭐ Cổng tái dựng `DE = DATE(AH//100, AH%100, 1)` cho **mọi** hàng:
`AH` rỗng ⇒ `DE = #NUM!` *(`DATE(-29…)`)*; `AH` ⛔ phải `yyyymm` hợp lệ *(**8** hàng sheet 5487·5556·5557·5634·5712·7098 mang
serial/`yymmdd` lạ ⇒ `DE` ra ngày vô lý, + 669·6230 mang tháng 27·14 ⇒ `DE` ngoài lưới; `DT7B-R1-01`)* ⇒ khai CÓ TÊN, ⛔ sửa.

⭐ **Hợp đồng bản thô** — LƯỚI `{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values}`:
  · `cot` = `("dong_sheet","A","D","E","F","P","R","V","AH","BR","BS","DE","AD")` *(SA, ánh xạ cột bằng hàng tiêu đề 7–8
    TRƯỚC: `P`=LE · `R`=ITL ID · `V`=Budget Code Final · `AH`=Thời điểm bắt đầu Final · `BR`/`BS`=PS Nợ/Có mUSD ·
    `AD`=Chủ dự toán CDT1 Final — khoá 6 khối CDT của 414, `DT7B-R1-02`)*.
    ⛔⛔ `B` Số chứng từ · `C` Diễn giải · `G`…`O` *(PII)* — vùng đọc ⛔ phủ.
  · `values` = hàng dữ liệu *(cột `A` có ngày)* theo thứ tự sheet; `dong_sheet` liên tục `10…7892`.

⭐ **Tập đóng** *(Đ5 — chuỗi ngoài tập ⇒ `thieu` ⇒ ĐỎ; ⛔ in giá trị)*: `D` tiền tệ · `P` LE *(18 giá trị đo 22/11, kể cả
`Cash Treasury` có/không dấu cách đuôi và `#N/A ()` ×4)* · `V` mã HD *(37 giá trị + 3 rỗng; 3 biến thể `ITE`)*.
"""
from __future__ import annotations

import datetime
import importlib.util
import pathlib
import sys
from decimal import Decimal
from typing import Any

_D = pathlib.Path(__file__).resolve().parent


def _nap(ten: str):
    spec = importlib.util.spec_from_file_location(f"khuon_dong_bang_{ten}", _D / f"{ten}.py")
    m = sys.modules.get(spec.name) or importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    if not hasattr(m, "BANG"):
        spec.loader.exec_module(m)
    return m


_k406 = _nap("gl_406_dau_vao")
_gl = _nap("_gl_hr")

BANG = "PD.PL.GL.DauVao"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("A", "D", "E", "F", "P", "R", "V", "AH", "BR", "BS", "DE", "AD")
#: `A` *(ngày chứng từ, serial)* · `D` tiền tệ *(6 hàng rỗng)* · `E`/`F` nguyên tệ · `P` LE · `R` ITL ID ·
#: `V` mã HD *(3 rỗng)* · `AH` yyyymm *(309 rỗng)* · `BR`/`BS` mUSD · `DE` số HOẶC `#NUM!` *(309)*.
KIEU_COT = {"A": "so", "D": "chu?", "E": "so?", "F": "so?", "P": "chu", "R": "chu", "V": "chu?",
            "AH": "so?", "BR": "so", "BS": "so", "DE": "so!", "AD": "chu"}
RA = "tests/fixture/dau_vao/gl_pl_dau_vao.json"
#: Đ5 — số ô lỗi `DE` *(phân bố theo loại)*: 309 `#NUM!` = đúng 309 hàng `AH` rỗng.
LOI_MONG = {"DE": {"#NUM!": 309}}
#: Bảng phụ: `tong_ky` *(mỗi kỳ của cột A)* · `tong_de` *(mỗi giá trị `DE` + 1 nhóm lỗi)*.
PHU_MONG = {"tong_ky": 20, "tong_de": 34}

COT_THO = ("dong_sheet", "A", "D", "E", "F", "P", "R", "V", "AH", "BR", "BS", "DE", "AD")
DONG_DAU_SHEET = 10
EPOCH = datetime.date(1899, 12, 30)
TIEN_TE = _k406.TIEN_TE

#: Đ5 — đo 22/11 *(⛔ chép từ 406: số liệu của CHÍNH tab này)*.
MONG_AH_RONG = 309
MONG_DE_KHOP = 7574          # DE = DATE(AH//100, AH%100, 1) khớp — gồm 8 hàng AH lạ
#: ⭐ `AH` lạ = **8** hàng *(`DT7B-R1-01`; bản đầu khai 6 vì cổng chỉ nhìn dải `202000…203000` — Đ1 phủ định thiếu)*:
#: 6 hàng serial/`yymmdd` *(5487·5556·5557·5634·5712·7098 — `DE` ra ngày vô lý)* + 2 hàng `yyyymm` có THÁNG ∉ 1…12
#: *(669: tháng 27 ⇒ `DE` 2027-03-01 · 6230: tháng 14 ⇒ `DE` 2027-02-01; `DATE` tràn tháng nên `DE` ĐÚNG công thức nhưng
#: ngoài lưới 2024-10-20…2026-02-27 ⇒ `SUMIFS` bỏ)*. ⛔ sửa dữ liệu — khai CÓ TÊN.
MONG_AH_LA = (669, 5487, 5556, 5557, 5634, 5712, 6230, 7098)
#: ⭐ `AD` = "Chủ dự toán (CDT1)" nhóm `Final` *(hàng 7 `AA`=`=J7` · hàng 8 `Final`; HẰNG dán, 0 công thức — đọc FORMULA
#: `AD10:AD8100`)*: khoá khối CDT của 414 *(`SUMIFS(BR, DE, V, AD = A{mở khối})` ở 6 khối `CVL COR SHQ1 CSM CAH ASA`; `SHQ2` = dư)*.
#: **Tập đóng 14 giá trị** *(đo 22/11 trên 7.883 hàng, ⛔ rỗng)* — kể cả biến thể lệch dấu cách / hoa-thường *(`SHQ1| Headquarters1`
#: ×92 · `SHQ2| Headquarters2` ×28 · `COR | Terasofts` ×16 · `SHQ2 | Headquarters1` ×31 · `SHQ1 | Headquarters2` ×2)*: `SUMIFS` khớp
#: chuỗi nên biến thể ⛔ vào khối CDT nào ⇒ rơi vào `SHQ2` *(dư)*. Mã nhóm, ⛔ tên người/TK.
MONG_AD: dict[str, int] = {
    "SHQ2 | Headquarters2": 4769, "SHQ1 | Headquarters1": 2091, "COR | TeraSofts": 525, "CVL | VisionLab": 121,
    "CAH | Astronex": 97, "CSM | SuperMinds": 92, "SHQ1| Headquarters1": 92, "SHQ2 | Headquarters1": 31,
    "SHQ2| Headquarters2": 28, "COR | Terasofts": 16, "TOR | Project A": 12, "ASA | Super App": 5,
    "SHQ1 | Headquarters2": 2, "TOL | Project L": 2}


def ah_la(ah: int) -> bool:
    """`AH` ⛔ `yyyymm` hợp lệ *(năm 2020…2029, THÁNG 1…12)* ⇒ lạ. ⭐ Tháng ∉ 1…12 cũng là lạ *(`DT7B-R1-01`)*."""
    return not (202000 < ah < 203000 and 1 <= ah % 100 <= 12)
MONG_R_LOI = 4
TAP_P = frozenset({"VGOH", "VVOH", "VVOS", "VVOT", "VVOV", "SGO1", "SGO2", "BGO1", "BGO2", "VGO1", "HGO6",
                   "UGO2", "MGO1", "VOOA", "CN", "Cash Treasury", "Cash Treasury ", "#N/A ()"})
TAP_V = frozenset({
    "NB | Lưu chuyển nội bộ", "ITE | Interest", "OMC | Online Marketing Cost", "LMN | Loan/Borrowing",
    "HCC | HR Culture Activities Cost", "BRC | Branding Cost", "GI | Gross Inflow", "OSF | Office Setup Fee",
    "FNS | Facilities for New Staff", "BON | Bonus", "CIO | Infrastructure - Other", "API | API",
    "OPO | Operating - Other", "BUT | Travel Cost", "LC | License Cost", "OMN | Repayment of Loan",
    "OFR | Office Rental Cost", "TAC | Tax Cash", "SC | Server Cost", "COT | CAC - Other",
    "REC | Recruitment Cost", "PS | Profit Share", "DEP | Deposit", "CSO | Service Cost - Other",
    "ITE | ITE Interest ", "OTMC | Other Marketing Cost", "CFI | Issuance of Stock", "CXO | CPX - Other",
    "ITE | ITE Interest", *_gl.HD_FINAL})


def date_sheets(y: int, m: int, d: int = 1) -> int:
    """`DATE(y, m, d)` của Sheets → serial *(tháng ngoài 1…12 tràn sang năm — như Sheets)*."""
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    return (datetime.date(y, m, d) - EPOCH).days


def de_tu_ah(ah: Any) -> Any:
    """Tái dựng `DE` từ `AH` *(công thức nguyên văn ở docstring)*: rỗng ⇒ `None` *(ô sẽ là `#NUM!`)*."""
    if ah is None:
        return None
    s = str(int(ah))
    return date_sheets(int(s[:4]), int(s[-2:]), 1)


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v == "")


def _so(v: Any) -> Any:
    return int(v) if isinstance(v, Decimal) and v == v.to_integral_value() else v


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI đầu vào PLA → bảng `{dong_sheet, A…DE}` + bảng phụ. `ValueError` ⇒ TỪ CHỐI; ⛔ lời lỗi mang giá trị ô."""
    if tho.get("cot") != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(⛔ phủ B·C·G…O)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng dữ liệu ⛔ rỗng")
    dong: list[list[Any]] = []
    tky: dict[int, list[Any]] = {}
    tde: dict[Any, list[Any]] = {}
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô")
        ds = h[0]
        if ds != DONG_DAU_SHEET + i:
            raise ValueError(f"hàng {i + 1}: dong_sheet {ds} ⛔ liên tục *(mong {DONG_DAU_SHEET + i})*")
        a = h[1]
        if not isinstance(a, int) or isinstance(a, bool) or a < 1:
            raise ValueError(f"hàng {i + 1}: cột A *(ngày)* phải serial số nguyên ≥ 1")
        row = [ds] + [None if _rong(x) else x for x in h[1:]]
        dong.append(row)
        ky = _k406._ky_tu_serial(a)
        br, bs, de = row[9], row[10], row[11]
        for v in (br, bs):
            if isinstance(v, bool) or not isinstance(v, (int, Decimal)):
                raise ValueError(f"hàng {i + 1}: BR/BS phải số")
        t = tky.setdefault(ky, [0, Decimal(0), Decimal(0)])
        t[0] += 1
        t[1] += Decimal(str(br))
        t[2] += Decimal(str(bs))
        kd = de if isinstance(de, (int, Decimal)) and not isinstance(de, bool) else "#NUM!"
        td = tde.setdefault(kd, [0, Decimal(0)])
        td[0] += 1
        td[1] += Decimal(str(br)) - Decimal(str(bs))
    tong_ky = [{"ky": k, "so_hang": v[0], "tong_BR": _gl._tong([v[1]]), "tong_BS": _gl._tong([v[2]])}
               for k, v in sorted(tky.items())]
    tong_de = [{"de": str(k), "so_hang": v[0], "tong_BR_tru_BS": _gl._tong([v[1]])}
               for k, v in sorted(tde.items(), key=lambda kv: (isinstance(kv[0], str), str(kv[0]).zfill(8)))]
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"tong_ky": tong_ky, "tong_de": tong_de},
        "ghi_chu": (
            f"ĐẦU VÀO PLA = {len(dong)} hàng dữ liệu *(cột A có ngày)* tab `Report I General Ledger` sổ P&L, khoá "
            f"dong_sheet {DONG_DAU_SHEET}…{DONG_DAU_SHEET + len(dong) - 1} liên tục; 12 cột A·D·E·F·P·R·V·AH·BR·BS·DE·AD "
            f"*(⛔ B Số chứng từ · C Diễn giải · G…O)*. `DE` = `=ArrayFormula(DATE(left(AH10:AH,4),RIGHT(AH10:AH,2),1))` "
            f"⇒ cột NGUỒN `AH` *(hằng dán yyyymm)*; cổng tái dựng DE từ AH ở `thieu_lac`. `P` LE · `V` mã HD "
            f"giữ NGUYÊN chuỗi *(tập đóng — kể cả biến thể dấu cách đuôi)*; `AD` tập đóng 14 giá trị. Bảng phụ `tong_ky` = số hàng + ΣBR/ΣBS "
            f"theo kỳ cột A; `tong_de` = số hàng + Σ(BR−BS) theo giá trị DE."),
    }


def _chu(v: Any) -> Any:
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _n(v: Any) -> Any:
    return None if v is None else Decimal(str(_chu(v)))


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5 — mong khai trước, NO cả hai chiều; ⛔ in giá trị ô)*: ⒜ số hàng mỗi kỳ cột A ↔ `phan_bo_ky`
    *(GỌI `gl_406_dau_vao`; 4 kỳ lệch có tên)*; ⒝ `D`/`P`/`V` ngoài tập đóng; ⒞ `R` ngoài `ITL#n` ∪ lỗi hợp lệ, số
    lỗi ≠ 4; ⒟ **`DE` ≠ `DATE(AH)`** ở hàng nào; số `AH` rỗng ≠ 309; số `DE` khớp ≠ 7574; `AH` lạ ≠ 8 hàng cố định *(⒠ tháng ∉ 1…12 cũng lạ)*;
    ⒡ **`AD` ngoài tập đóng 14 giá trị / phân bố ≠ mong**."""
    ledger = _k406._phan_bo_ledger()
    mong = {k: _k406.LECH_CO_TEN.get(k, v) for k, v in ledger.items()}
    thuc: dict[int, int] = {}
    for d in dong:
        k = _k406._ky_tu_serial(int(_chu(d["A"])))
        thuc[k] = thuc.get(k, 0) + 1
    thieu = [f"ky@{k}:{thuc.get(k, 0)}/{mong.get(k)}" for k in sorted(set(thuc) | set(mong))
             if thuc.get(k, 0) != mong.get(k)
             and k not in _k406.LECH_CO_TEN]
    thieu += [f"ky_lech@{k}:{thuc.get(k, 0)}/{v}" for k, v in sorted(_k406.LECH_CO_TEN.items())
              if thuc.get(k, 0) != v]
    n_ah_rong = n_khop = n_loi_r = 0
    ah_la_ds: list[int] = []
    ad_dem: dict[str, int] = {}
    for d in dong:
        ds = int(_chu(d["dong_sheet"]))
        for c, tap in (("D", set(TIEN_TE)), ("P", TAP_P), ("V", TAP_V), ("AD", set(MONG_AD))):
            s = _chu(d[c])
            if s is not None and s not in tap:
                thieu.append(f"{c}_la@{ds}")
        ad = _chu(d["AD"])
        if ad is not None:
            ad_dem[ad] = ad_dem.get(ad, 0) + 1
        r = _chu(d["R"])
        if not _k406.ITL_ID_RE.fullmatch(r):
            n_loi_r += 1
            if r not in _k406.ITL_LOI_HOP_LE:
                thieu.append(f"R_la@{ds}")
        ah, de = _n(d["AH"]), d["DE"]
        if ah is None:
            n_ah_rong += 1
            if not (isinstance(de, dict) and _chu(de).startswith("#NUM!")):
                thieu.append(f"DE_khac_AH@{ds}")
            continue
        exp = de_tu_ah(ah)
        if isinstance(de, dict) or _n(de) != exp:
            thieu.append(f"DE_khac_AH@{ds}")
        else:
            n_khop += 1
        if ah_la(int(ah)):
            ah_la_ds.append(ds)
    if n_ah_rong != MONG_AH_RONG:
        thieu.append(f"AH_rong@khác:{n_ah_rong}/{MONG_AH_RONG}")
    if n_khop != MONG_DE_KHOP:
        thieu.append(f"DE_khop@khác:{n_khop}/{MONG_DE_KHOP}")
    if tuple(ah_la_ds) != MONG_AH_LA:
        thieu.append(f"AH_la@khác:{len(ah_la_ds)}/{len(MONG_AH_LA)}")
    if ad_dem != MONG_AD:
        thieu.append("AD@phân_bố_khác")
    if n_loi_r != MONG_R_LOI:
        thieu.append(f"R_loi@khác:{n_loi_r}/{MONG_R_LOI}")
    lac = [str(k) for k in sorted(_k406.LECH_CO_TEN)]
    dai = (f"{len(dong)} hàng · {sum(1 for k in mong if thuc.get(k) == mong[k] and k not in _k406.LECH_CO_TEN)} kỳ "
           f"khớp phan_bo_ky · {len(lac)} kỳ lệch có tên · DE=DATE(AH) khớp {n_khop} + {n_ah_rong} `#NUM!` "
           f"(AH rỗng) · AH lạ {len(ah_la_ds)} · R lỗi {n_loi_r}")
    return {"thieu": thieu, "lac": lac, "dai": dai}
