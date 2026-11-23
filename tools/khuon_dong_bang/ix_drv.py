"""Khuôn đóng băng `ix_drv` — ẢNH IX.DRV *(driver tháng — tab `Allocation Table`, PD 604 + NB theo LE)*
*(ISP 3.1.2 · Step 27 · DT10 · `WO-196` AC-1 · AC-2 · AC-4)*.

    python tools/dong_bang_sheet.py ix_drv <bản_thô.json> --mong 21
        ⇒ tests/fixture/cau_hinh/ix_drv.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.2.2 IX.DRV · §3.4.2 PD 511–513 · 604. Engine AL.KEY *(H12)*
cần driver theo `(driver, CDT1, tháng)`; AP khai **4 loại × 8 CDT1 × 12 tháng**: NOEM *(headcount)* ·
GI theo PE · GI theo PM · NB theo LE, *"chỉ có 2025"*, NOEM *"tham chiếu ô cứng của H1000 I HR
Report"*. Khuôn đóng băng ĐÚNG những gì nguồn có, và **khai CÓ TÊN từng ô thiếu** *(⛔ lấp)*.

Nguồn *(`[COPY] Report I General Ledger | P&L Report`, MỘT ứng viên — đo 18/11)*:
  · `Allocation Table | By NOEM & By GI` *(1000×26; dữ liệu `A1:O35`)* — 3 bảng: **GI theo PE**
    *(hàng 3–12)* · **GI theo PM** *(hàng 14–23)* · **NOEM** *(hàng 25–35)*; mỗi bảng = tiêu đề tháng
    + hàng `Group` + **7** hàng CDT1 *(CVL · COR · CSM · CAH · ASA · SHQ1 · SHQ2)* + hàng CHECK.
  · `Allocation Table | NB | By LE` *(919×27)* — 3 khối 304 hàng `From × To` mUSD: BALANCE *(Ps Có −
    Ps Nợ, hàng 5–308)* · CREDIT *(310–613)* · DEBIT *(615–918)*; **ảnh giữ BALANCE** *(= CREDIT −
    DEBIT, AP §3.4.2 PD 511)* ở bảng phụ `nb_le`; CREDIT/DEBIT chỉ dùng ĐỐI SOÁT.

Hợp đồng bản thô *(phiên cloud DATA, khoá SA chỉ-đọc, ⛔ commit)* — hình `{nguon, doc_luc,
cach_doc, cot, at, nb, hr, cong_thuc_noem}`: `at` = lưới `A1:Z35` · `nb` = `A1:Q918` · `hr` = vùng
HR cứng `A4289:Q4300` · `cong_thuc_noem` = công thức `FORMULA` của `D27:O34`. ⛔ cột nào khác.

⭐ **Bốn quyết định** *(mỗi cái một con số đo 18/11 — Đ4/Đ5)*:

  ① **Ảnh chính = 21 dòng** *(3 driver × 7 CDT1)* × 12 cột tháng `m01…m12` *(số HOẶC rỗng)* + `nam`
    *(năm đọc ở TIÊU ĐỀ tháng — `2025`)* + `ngoai` *(số ô có dữ liệu ở `P:Z` của hàng sheet ấy — 0)*.
    **CMN KHÔNG có hàng**: AP khai 8 CDT1, nguồn 7 — CMN *(CMN_Management)* ⇒ SHQ1 theo CDT Correct
    và ở NOEM nó rơi vào phần DƯ của SHQ2 *(`=100% − Σ 6 CDT1`)*; ⛔ bịa.

  ② **Cổng = `thieu_lac` — lệch CÓ TÊN, HAI CHIỀU** *(Đ5)*. Lưới 4 × 8 × 12 = **384** ô; ô SỐ ở nguồn
    **238** = NOEM 7×12 + GI-PE 7×11 + GI-PM 7×11. **146** ô thiếu có tên *(`MONG_THIEU`)*:
      · **NB_LE 96** = 8 CDT1 × 12 — NB khoá theo LE *(From × To)*, ⛔ theo CDT1 ⇒ 0/96 ở lưới CDT1;
      · **CMN 36** = 3 driver × 12;
      · **GI 202501 14** = 2 driver × 7 CDT1 — công thức dùng `SUMIFS … "TOTAL "&202501` trên `CFA2 |
        MID 3 | GI Platform Data Ledger`, MID3 chỉ có 11 dòng TOTAL *(202502…202512)* ⇒ `iferror` ⇒ rỗng.
    Thiếu MỚI *(ô mong CÓ mà rỗng)* **và** đã-có *(ô mong thiếu mà nay CÓ)* đều ⇒ `thieu` ⇒ ĐỎ.
    Thêm: `nam ≠ 2025` · `ngoai ≠ 0` · `Σ 7 CDT1 ≠ 100 %` *(34 tổng: NOEM 12 + GI-PE 11 + GI-PM 11)* ⇒ ĐỎ.
    Tập rỗng ⇒ `ValueError` *(Đ3)*.

  ③ **driver CHỈ có 2025** *(AP đo)*: mọi tiêu đề tháng cùng năm `2025`; `P:Z` rỗng. ⇒ **2026 ⛔ có ở
    nguồn** ⇒ ATL 2026 chỉ đối chiếu được khi cờ luật TẮT (D2). Tiêu đề lẫn năm ⇒ `ValueError`.

  ④ **NOEM ghi NGUỒN từng ô** *(AC-2)*: bảng phụ `nguon_noem` **96** dòng = 8 hàng *(Group + 7 CDT1)*
    × 12 tháng: tab · địa chỉ ô · công thức GỐC · ô HR cứng của tử/mẫu *(`'[H1.2026][2025]H1000 I HR
    Report'!$A$4289:$Q$4300`)* và giá trị tử/mẫu. 84 ô trỏ HR *(Group 12 + 6 hàng × 12)*; SHQ2 *(12)* =
    `100% − Σ`. Tử/mẫu ĐỌC từ HR và tái dựng ra đúng số NOEM *(lệch lớn nhất ghi ở `ghi_chu`)*.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any

BANG = "IX.DRV"
KHOA = "ma"
KIEU_KHOA = "ma"
THANG = tuple(f"m{m:02d}" for m in range(1, 13))
#: Cột ảnh chính = `driver` `cdt1` `nam` `ngoai` + 12 tháng. ⛔ thêm cột.
COT = ("driver", "cdt1", "nam", "ngoai", *THANG)
KIEU_COT = {"driver": "chu", "cdt1": "chu", **{m: "so?" for m in THANG}}
RA = "tests/fixture/cau_hinh/ix_drv.json"
PHU_MONG = {"nb_le": 304, "nguon_noem": 96, "o_thieu": 146, "tong": 3}

#: Cột LƯỚI `at` — vùng `A:Z` hàng 1…35 *(chỉ `D:O` mang tháng; `P:Z` phải RỖNG — ③)*.
COT_THO = ["A", "B", "C", *[chr(68 + i) for i in range(12)]]
NAM = 2025
DRIVER = ("NOEM", "GI_PE", "GI_PM", "NB_LE")
DRIVER_CDT1 = DRIVER[:3]
CDT1_8 = ("SHQ2", "SHQ1", "COR", "CVL", "CSM", "CAH", "ASA", "CMN")
#: Thứ tự 7 hàng CDT1 của sheet *(hàng 5–11 · 16–22 · 28–34)*.
CDT1_SHEET = ("CVL", "COR", "CSM", "CAH", "ASA", "SHQ1", "SHQ2")
#: Mỗi bảng: (driver, hàng tiêu đề, hàng Group) — hàng CDT1 = Group + 1…+7, CHECK = Group + 8.
BANG_AT = (("GI_PE", 3, 4), ("GI_PM", 14, 15), ("NOEM", 26, 27))
TAB_HR = "[H1.2026][2025]H1000 I HR Report"
VUNG_HR = "$A$4289:$Q$4300"
TOL = Decimal("0.000000001")


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _tt(thang: int) -> str:
    return f"{NAM}{thang:02d}"


def mong_thieu() -> frozenset[str]:
    """146 ô thiếu CÓ TÊN *(②)* — `driver|cdt1|yyyymm`. Khai MỘT chỗ; công cụ đo lại từ nguồn."""
    ten: set[str] = set()
    for c in CDT1_8:                                         # NB_LE 96: khoá theo LE, ⛔ theo CDT1
        for m in range(1, 13):
            ten.add(f"NB_LE|{c}|{_tt(m)}")
    for d in DRIVER_CDT1:                                    # CMN 36
        for m in range(1, 13):
            ten.add(f"{d}|CMN|{_tt(m)}")
    for d in ("GI_PE", "GI_PM"):                            # GI 202501: 14
        for c in CDT1_SHEET:
            ten.add(f"{d}|{c}|{_tt(1)}")
    return frozenset(ten)


def _ly_do_thieu(driver: str, cdt1: str, thang: int) -> str:
    if driver == "NB_LE":
        return "NB khoá theo LE (From × To), ⛔ theo CDT1"
    if cdt1 == "CMN":
        return "CMN gộp vào SHQ1 theo CDT Correct; ở NOEM rơi vào phần dư của SHQ2"
    if driver in ("GI_PE", "GI_PM") and thang == 1:
        return "GI: MID3 ⛔ có dòng TOTAL 202501 (chỉ 202502…202512) ⇒ iferror ⇒ rỗng"
    return "⛔ có tên trong khai"


def _luoi_so(v: Any) -> Any:
    return None if _rong(v) else v


def _cot_chu(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, q = divmod(i - 1, 26)
        s = chr(65 + q) + s
    return s


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Bản thô `{at, nb, hr, cong_thuc_noem}` → bảng chính 21 dòng + 4 bảng phụ.
    ⛔ lời lỗi mang giá trị ô; `ValueError` ⇒ TỪ CHỐI."""
    if tho.get("cot") != COT_THO:
        raise ValueError(f"`cot` phải đúng {COT_THO} *(vùng at A:O)*")
    at, nb, hr, ct = (tho.get(k) for k in ("at", "nb", "hr", "cong_thuc_noem"))
    if not all(isinstance(x, dict) for x in (at, nb, hr, ct)):
        raise ValueError("bản thô thiếu một trong `at` · `nb` · `hr` · `cong_thuc_noem`")
    if at.get("dong_dau_sheet") != 1 or nb.get("dong_dau_sheet") != 1:
        raise ValueError("`at`/`nb` `dong_dau_sheet` phải 1 *(lưới từ hàng sheet 1)*")
    A, N = at.get("values"), nb.get("values")
    if not isinstance(A, list) or len(A) != 35 or any(not isinstance(h, list) or len(h) != 26 for h in A):
        raise ValueError("`at.values` phải 35 hàng × 26 cột *(A1:Z35)*")
    if not isinstance(N, list) or len(N) != 918 or any(not isinstance(h, list) or len(h) != 17 for h in N):
        raise ValueError("`nb.values` phải 918 hàng × 17 cột *(A1:Q918)*")

    dong: list[list[Any]] = []
    tong: list[dict[str, Any]] = []
    co: set[str] = set()
    for driver, h_tieu, h_grp in BANG_AT:
        tieu = A[h_tieu - 1][3:15]
        if driver == "NOEM":
            ok = [str(t) for t in tieu] == [f"{m}{NAM}" for m in range(1, 13)]
        else:
            ok = [str(t) for t in tieu] == [_tt(m) for m in range(1, 13)]
        if not ok:
            raise ValueError(f"{driver}: tiêu đề tháng hàng {h_tieu} ⛔ phải 12 tháng liền của {NAM} "
                             "(driver chỉ có 2025 — AP đo; năm khác ⇒ TỪ CHỐI)")
        if str(A[h_grp - 1][2]).strip() != "Group":
            raise ValueError(f"{driver}: hàng {h_grp} cột C phải `Group`")
        tong.append({"driver": driver, **{m: _luoi_so(A[h_grp - 1][3 + i]) for i, m in enumerate(THANG)}})
        for k, cdt1 in enumerate(CDT1_SHEET, 1):
            h = A[h_grp - 1 + k]
            if str(h[2]).split("|")[0].strip() != cdt1:
                raise ValueError(f"{driver}: hàng {h_grp + k} nhãn ⛔ phải CDT1 `{cdt1}`")
            ngoai = sum(1 for x in h[15:26] if not _rong(x))
            vals = [_luoi_so(x) for x in h[3:15]]
            for i, v in enumerate(vals):
                if v is not None:
                    co.add(f"{driver}|{cdt1}|{_tt(i + 1)}")
            dong.append([f"{driver}|{cdt1}", driver, cdt1, NAM, ngoai, *vals])
    # `P:Z` của MỌI hàng sheet 1…35 *(kể cả hàng ⛔ chọn)* — ③: ô nào cũng đếm.
    ngoai_tat = sum(1 for h in A for x in h[15:26] if not _rong(x))

    # ── ô thiếu CÓ TÊN (②): lưới 4 × 8 × 12 trừ ô CÓ ──
    thieu_tt = []
    for d in DRIVER:
        for c in CDT1_8:
            for m in range(1, 13):
                if f"{d}|{c}|{_tt(m)}" not in co:
                    thieu_tt.append({"driver": d, "cdt1": c, "thang": _tt(m),
                                     "ly_do": _ly_do_thieu(d, c, m)})

    # ── NB theo LE: BALANCE + đối soát CREDIT − DEBIT ──
    if _rong(N[3][0]) or not str(N[3][0]).startswith("BALANCE") or not str(N[308][0]).startswith("CREDIT") \
            or not str(N[613][0]).startswith("DEBIT"):
        raise ValueError("`nb`: hàng 4 · 309 · 614 phải mở khối BALANCE · CREDIT · DEBIT")
    if [str(x) for x in N[2][5:17]] != [_tt(m) for m in range(1, 13)] or any(str(x) != str(NAM) for x in N[0][4:17]):
        raise ValueError("`nb`: tiêu đề tháng ⛔ phải 202501…202512 và năm 2025")
    nb_dong: list[dict[str, Any]] = []
    du_max = Decimal(0)
    for k in range(304):
        b, c, d = N[4 + k], N[309 + k], N[614 + k]
        if not (b[1] == c[1] == d[1] and b[2] == c[2] == d[2]):
            raise ValueError(f"`nb`: ba khối lệch khoá From/To ở hàng {k + 1} của khối")
        nb_dong.append({"from": b[1], "to": b[2], "loai": b[3], **{m: b[5 + i] for i, m in enumerate(THANG)}})
        for i in range(12):
            if all(isinstance(x, (int, Decimal)) and not isinstance(x, bool) for x in (b[5 + i], c[5 + i], d[5 + i])):
                du_max = max(du_max, abs(Decimal(b[5 + i]) - (Decimal(c[5 + i]) - Decimal(d[5 + i]))))

    # ── NOEM nguồn từng ô (④) ──
    Hh = hr.get("values")
    if hr.get("tab") != TAB_HR or hr.get("dong_dau_sheet") != 4289 or not isinstance(Hh, list) or len(Hh) != 12:
        raise ValueError(f"`hr` phải vùng A4289:Q4300 của tab `{TAB_HR}`")
    tieu_hr = [str(x) for x in Hh[0]]
    cot_hr = {t: _cot_chu(j) for j, t in enumerate(tieu_hr) if t}
    nhan_hr = [str(h[0]) for h in Hh]

    def o_hr(ma: str, thang: int) -> tuple[str, Any]:
        r = nhan_hr.index(ma)                                  # MATCH(…, A4289:A4300, 0) = KHỚP ĐẦU
        c = f"{thang}{NAM}"
        if c not in cot_hr:
            raise ValueError(f"`hr`: tiêu đề `{c}` ⛔ có ở A4289:Q4289")
        return f"{cot_hr[c]}{4289 + r}", Hh[r][tieu_hr.index(c)]

    if ct.get("dong_dau_sheet") != 27 or not isinstance(ct.get("values"), list) or len(ct["values"]) != 8 \
            or any(not isinstance(h, list) or len(h) != 12 for h in ct["values"]):
        raise ValueError("`cong_thuc_noem` phải 8 hàng × 12 cột `D27:O34`")
    nguon: list[dict[str, Any]] = []
    noem = {c: d for c, d in ((r[2], r) for r in dong if r[1] == "NOEM")}
    lech_max = Decimal(0)
    for k in range(8):
        cdt1 = "Group" if k == 0 else CDT1_SHEET[k - 1]
        for i in range(12):
            f = ct["values"][k][i]
            o = f"{chr(68 + i)}{27 + k}"
            row = {"o": o, "cdt1": cdt1, "thang": _tt(i + 1), "tab_nguon": TAB_HR,
                   "cong_thuc": f, "o_tu": None, "o_mau": None, "tu": None, "mau": None}
            if isinstance(f, str) and VUNG_HR in f:
                ma = "GAG" if k == 0 else ("SHQ" if cdt1 == "SHQ1" else cdt1)
                ot, tu = o_hr(ma, i + 1)
                om, mau = o_hr("GAG", i + 1)
                row.update(o_tu=ot, o_mau=om, tu=tu, mau=mau)
                if k > 0 and isinstance(tu, (int, Decimal)) and isinstance(mau, (int, Decimal)) and mau != 0:
                    got = noem[cdt1][5 + i]
                    if got is not None:
                        lech_max = max(lech_max, abs(Decimal(tu) / Decimal(mau) - Decimal(got)))
            elif k == 7:
                if "sum(" not in str(f).lower():
                    raise ValueError(f"{o}: SHQ2 phải là `100% − Σ`")
            else:
                raise ValueError(f"{o}: công thức ⛔ trỏ vùng HR cứng {VUNG_HR}")
            nguon.append(row)

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"nb_le": nb_dong, "nguon_noem": nguon, "o_thieu": thieu_tt,
                "tong": [{"driver": r["driver"], **{m: r[m] for m in THANG}} for r in tong]},
        "ghi_chu": (
            f"IX.DRV = {len(dong)} dòng (3 driver × 7 CDT1) × 12 tháng {NAM}. Lưới AP 4 × 8 × 12 = 384; "
            f"nguồn có {len(co)} ô số, {len(thieu_tt)} ô thiếu CÓ TÊN ở bảng phụ `o_thieu` (NB_LE 96 · "
            "CMN 36 · GI 202501 14). driver CHỈ có 2025 (AP đo; ô ngoài 12 cột tháng, `P:Z` hàng 1–35: "
            f"{ngoai_tat}) ⇒ 2026 ⛔ có ở nguồn ⇒ ATL 2026 chỉ đối chiếu được khi cờ tắt (D2). Nguồn "
            "`[COPY] Report I General Ledger | P&L Report`: tab `Allocation Table | By NOEM & By GI` "
            "(GI-PE hàng 3–12 · GI-PM 14–23 · NOEM 25–35; GI = SUMIFS trên `CFA2 | MID 3 | GI Platform "
            "Data Ledger` dòng `TOTAL <yyyymm>` cột O/P ÷ S…AD; NOEM = INDEX/MATCH trên ô CỨNG "
            f"`{TAB_HR}`!A4289:Q4300 — bảng phụ `nguon_noem` 96 ô, tử/mẫu tái dựng NOEM lệch lớn nhất "
            f"{lech_max}). NB theo LE: tab `Allocation Table | NB | By LE` khối BALANCE 304 hàng From × To "
            f"(mUSD) ở `nb_le`; đối soát BALANCE = CREDIT − DEBIT lệch lớn nhất {du_max} (hai khối CREDIT · "
            "DEBIT ⛔ mang). `tong` = hàng Group của 3 bảng. ⛔ mang cột ngoài A:Z."),
    }


def _dec(v: Any) -> Decimal | None:
    if v is None:
        return None
    return Decimal(v)


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng IX.DRV *(②③)*: ô thiếu so `mong_thieu()` HAI CHIỀU · `nam == 2025` · `ngoai == 0` ·
    `Σ 7 CDT1 = 100 %` mỗi (driver, tháng) có số. Tập rỗng ⇒ `ValueError` *(Đ3)*."""
    if not dong:
        raise ValueError("0 dòng driver — mẫu số 0, ⛔ nền xanh (Đ3)")
    thieu: list[str] = []
    co: set[str] = set()
    cong: dict[tuple[str, int], Decimal] = {}
    for d in dong:
        dr, c = d["driver"]["chu"], d["cdt1"]["chu"]
        if dr not in DRIVER_CDT1 or c not in CDT1_8:
            raise ValueError(f"dòng `{dr}|{c}` ⛔ thuộc lưới driver × CDT1 của AP")
        if str(d["nam"]) != str(NAM):
            thieu.append(f"nam@{dr}|{c}={d['nam']}")
        if str(d["ngoai"]) != "0":
            thieu.append(f"ngoai@{dr}|{c}={d['ngoai']}")
        for i, m in enumerate(THANG, 1):
            v = _dec(d[m])
            if v is not None:
                co.add(f"{dr}|{c}|{_tt(i)}")
                cong[(dr, i)] = cong.get((dr, i), Decimal(0)) + v
    mong = mong_thieu()
    luoi = {f"{d}|{c}|{_tt(m)}" for d in DRIVER for c in CDT1_8 for m in range(1, 13)}
    thieu_that = luoi - co
    thieu += [f"thiếu_mới:{x}" for x in sorted(thieu_that - mong)]
    thieu += [f"đã_có(mong thiếu):{x}" for x in sorted(mong - thieu_that)]
    for (dr, i), s in sorted(cong.items()):
        if abs(s - 1) > TOL:
            thieu.append(f"tong@{dr}|{_tt(i)}")
    return {
        "thieu": thieu,
        "lac": [],
        "dai": (f"{len(co)}/{len(luoi)} ô số ở lưới 4 loại × 8 CDT1 × 12 tháng · thiếu {len(thieu_that)} "
                f"(mong {len(mong)}: NB_LE 96 · CMN 36 · GI 202501 14) · {len(cong)} tổng Σ7 CDT1 = 100 % "
                "· driver chỉ 2025"),
    }
