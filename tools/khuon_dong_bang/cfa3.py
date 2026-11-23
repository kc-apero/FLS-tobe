"""Khuôn đóng băng `cfa3` — ĐÁP ÁN `MID I Report I CFA3 Daily` *(HD × ngày, CF CFA3 — HR)*.

    python tools/dong_bang_sheet.py cfa3 <bản_thô.json> --mong 650
        ⇒ tests/fixture/dap_an/cfa3.json

⭐ **Vì sao có khuôn này** *(ISP 3.1.2 · Step 23 · DT6 · `WO-192` + chốt nguồn của orchestrator
18/11)*. Bước engine CFA3 *(HR ⛔ qua ALLOCATE — Q3)* cần ẢNH đứng yên của sheet CFA3 Daily — đọc
MỘT lần, đóng băng có checksum, cổng khẳng định **mọi mã HD ∈ cây ATL 74** và **trục ngày LIÊN TỤC**.

⚠ **Errata ISP** *(orchestrator 18/11)*: `CFA3 Daily` thuộc **PD 411** phần CFA3 *(DT5 LOẠI nó)* —
PD 412 · 413 trong tiêu đề Step 23 là GL, ⛔ CFA3.

Hợp đồng bản thô = **LƯỚI SA** `{spreadsheet_id, nguon, doc_luc, cach_doc, values}` — `values` =
sheet `'MID I Report I CFA3 Daily'` *(99 × 502, đọc `A1:SH99`)*. Bố cục = `Report I CFA1 Daily`
nhưng **MỘT khối LE** *(`GROUP`, hàng 7)* × 74 mã HD *(cùng cây ATL)* — nên ⛔ dùng được `dung_cay`
của `_cfa1` *(đòi 5 khối)*; khuôn này dựng cây một khối, còn lại MƯỢN `_cfa1` *(`_loai_hang` ·
`boc_o` · `soat_pii_luoi` …)*. Cột `A` = số mUSD *(⛔ vào ảnh — chỉ CẤU TRÚC, như `cfa1_daily`)*.

⭐ **Đo 18/11 *(khoá SA chỉ-đọc, mỗi số đếm MỘT vật, Đ4)*:**
  · **496 cột ngày** LIÊN TỤC `2024-10-20 … 2026-02-27` *(serial 45585…46080)* — sheet **DỪNG** ở
    2026-02-27 *(⛔ sinh sẵn cột tương lai như CFA1)* ⇒ `ngay_truc` mong 496, cắt 0 cột tương lai.
  · **74 hàng HD** = 1 khối `GROUP` × 74 mã *(== cây ATL)*.
  · **650** ô số ≠ 0 ⇒ dòng chính thưa; **5** ô `"-"` ⇒ bảng phụ `o_loi` *(giữ chuỗi, ĐẾM, ⛔ hoá
    0)*; ⛔ ô `#REF!`/`#N/A`.
"""
from __future__ import annotations

import datetime
import importlib.util
import pathlib
import sys
from collections import Counter
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "_cfa1.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__cfa1", _P)
_c = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _c
_spec.loader.exec_module(_c)

BANG = "PD.CFA3"
KHOA = "o_id"
KIEU_KHOA = "ma"
COT = ("le", "ma_hd", "ngay", "gt")
KIEU_COT = {"le": "chu", "ma_hd": "chu", "ngay": "so", "gt": "so"}
RA = "tests/fixture/dap_an/cfa3.json"
#: Đ5 — số dòng bảng phụ *(đo 18/11)*: `ngay_truc` = số cột ngày ≤ ngày đọc.
PHU_MONG = {"hd": 74, "ngay_truc": 496, "o_loi": 5}
#: Đ5 — phân bố giá trị ô lỗi *(đo 18/11: tập ⛔ số = `{"-"}` ×5)*. Đổi tập ⇒ ĐỎ *(`DT5-R1-04`)*.
O_LOI_GIA = {"-": 5}
#: Khối LE duy nhất của CFA3 *(hàng nhóm `HDO` có `GROUP` ở cột A)*.
LE_CFA3 = "GROUP"
SERIAL_MOC = 45585            # 2024-10-20 *(cột ngày đầu THẬT, như CFA1)*
I_DAY, I_DOW, COT_DAU = 4, 5, 6
_DOW_IDX = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}
NHOM = _c.NHOM

_NGU_CANH: dict[str, Any] | None = None


def dung_cay_mot_khoi(values: list[list]) -> list[dict[str, Any]]:
    """Lưới → hàng HD `{le, ma, ten, cha, cap, nhom, dong_sheet}` của MỘT khối `GROUP`.
    `ValueError` ⇒ TỪ CHỐI *(⛔ lời lỗi mang ô cột A/B — qua `_an_toan`)*."""
    hdo = [i for i, r in enumerate(values)
           if _c._loai_hang(r)[0] == "nhom" and _c._chuoi(r, 1) == "HDO"]
    if len(hdo) != 1:
        raise ValueError(f"thấy {len(hdo)} hàng nhóm HDO ≠ 1 khối *(CFA3 chỉ có khối GROUP)*")
    start = hdo[0]
    le = _c._chuoi(values[start], 0)
    if le != LE_CFA3:
        raise ValueError(f"khối *(hàng sheet {start + 1}, cột A)*: mã LE = {_c._an_toan(le)} "
                         f"≠ mong {LE_CFA3!r}")
    ra: list[dict[str, Any]] = []
    ngan: list[tuple[int, str]] = []
    nhom_hien: str | None = None
    xong = False
    for i in range(start, len(values)):
        r = values[i]
        lo, col = _c._loai_hang(r)
        ds = i + 1
        if lo == "trong":
            continue
        if lo == "khac":
            xong = True                              # ô canh *(CHECK ZONE…)* chỉ SAU dữ liệu
            continue
        if xong:
            raise ValueError(f"dòng sheet {ds}: dữ liệu `{lo}` nằm SAU vùng canh/CHECK ZONE — "
                             "rác lọt giữa bảng")
        if lo == "nhom":
            nhom_hien = _c._chuoi(r, 1)
            if nhom_hien not in NHOM:
                raise ValueError(f"dòng sheet {ds}: nhóm {_c._an_toan(nhom_hien)} ⛔ thuộc "
                                 f"{list(NHOM)}")
            ngan = []
            continue
        ma, ten = (x.strip() for x in _c._chuoi(r, col).split(_c._TACH, 1))
        if not ma or not ten:
            raise ValueError(f"dòng sheet {ds}: `MÃ | Tên` thiếu mã hoặc tên")
        if nhom_hien is None:
            raise ValueError(f"dòng sheet {ds}: dòng mã trước tiêu đề nhóm đầu")
        while ngan and ngan[-1][0] >= col:
            ngan.pop()
        ra.append({"le": le, "ma": ma, "ten": ten, "cha": ngan[-1][1] if ngan else None,
                   "cap": col, "nhom": nhom_hien, "dong_sheet": ds})
        ngan.append((col, ma))
    if len(ra) != 74:
        raise ValueError(f"{len(ra)} mã HD ≠ 74 *(cây ATL)*")
    return ra


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI CFA3 → bảng `{o_id, le, ma_hd, ngay, gt}` *(thưa, ≠ 0)* + bảng phụ `hd`·`ngay_truc`·
    `o_loi`. `ValueError` ⇒ TỪ CHỐI *(⛔ lời lỗi mang giá trị ô)*."""
    global _NGU_CANH
    values = tho.get("values")
    if not isinstance(values, list) or len(values) <= COT_DAU:
        raise ValueError("`values` phải lưới đủ 6 hàng tiêu đề + dữ liệu")
    _c.soat_pii_luoi(values)                                   # ⛔ PII trước mọi thứ
    read_date = datetime.date.fromisoformat(tho["doc_luc"])
    day = values[I_DAY]
    sers: list[tuple[int, int]] = []
    for j in range(COT_DAU, len(day)):
        v = day[j]
        if not _c._la_so(v):
            continue
        if int(v) != v:
            raise ValueError(f"serial ngày cột {j + 1} ⛔ nguyên")
        sers.append((j, int(v)))
    if not sers:
        raise ValueError("hàng Day *(hàng 5)* ⛔ có serial ngày nào từ cột G")
    if sers[0][1] != SERIAL_MOC:
        raise ValueError(f"cột ngày đầu serial {sers[0][1]} ≠ mốc {SERIAL_MOC} *(2024-10-20)*")
    giu = [(j, s) for j, s in sers if _c.ngay_tu_serial(s) <= read_date]
    tuong_lai = [j for j, s in sers if _c.ngay_tu_serial(s) > read_date]
    for k, (j, s) in enumerate(giu):
        if s != giu[0][1] + k:
            raise ValueError(f"trục ngày ⛔ liên tục ở cột {j} *(serial {s} ≠ {giu[0][1] + k})*")
    hd = dung_cay_mot_khoi(values)
    _c.kiem_tuong_lai_rong(values, hd, tuong_lai)
    dong, o_loi = _c.boc_o(values, hd, [(j, str(s), s) for j, s in giu], "ngay")
    ngay_truc = []
    for j, s in giu:
        dw = values[I_DOW][j] if j < len(values[I_DOW]) else None
        if not isinstance(dw, str) or _DOW_IDX.get(dw) != (s + 6) % 7:
            raise ValueError(f"thứ ngày cột {j + 1} *(serial {s})* ⛔ khớp (serial+6)%7 — hàng "
                             "'Days of the week' sai hoặc trục ngày lệch")
        ngay_truc.append({"ngay": s, "ngay_iso": _c.ngay_tu_serial(s).isoformat(), "dow": dw})
    _NGU_CANH = {"hd": hd, "o_loi": o_loi}
    d_cuoi = _c.ngay_tu_serial(giu[-1][1])
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"hd": hd, "ngay_truc": ngay_truc, "o_loi": o_loi},
        "ghi_chu": (
            f"CFA3 Daily *(lưới SA)*: 1 khối LE {LE_CFA3} × 74 mã HD = {len(hd)} hàng; trục NGÀY "
            f"{len(giu)} cột LIÊN TỤC 2024-10-20 … {d_cuoi.isoformat()} *(ngày đọc "
            f"{read_date.isoformat()}; cắt {len(tuong_lai)} cột tương lai)*. {len(dong)} ô số ≠ 0 "
            f"⇒ dòng chính thưa (ô 0/vắng ⇒ 0); {len(o_loi)} ô ⛔ số ⇒ bảng phụ `o_loi` (giữ "
            "chuỗi, ĐẾM, ⛔ hoá 0). Cột A (mUSD) ⛔ vào ảnh. Sheet DỪNG ở "
            f"{d_cuoi.isoformat()} — ⛔ suy phần sau."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng CFA3 *(Đ5)*. ĐỎ khi: ⒜ mã HD ở dòng chính ⛔ ∈ cây ATL / LE ≠ GROUP; ⒝ cây ĐẦY ĐỦ
    `phu.hd` ≠ ATL 74 CHÍNH XÁC *(lạ · vắng · trùng)*; ⒞ phân bố `o_loi` ≠ `O_LOI_GIA`; thiếu
    ngữ cảnh ⇒ ĐỎ *(Đ3/Đ5)*. ⛔ `lac`."""
    cay = _c.ma_cay_atl()
    thieu: list[str] = []
    ma_co: list[str] = []
    for d in dong:
        m, l = _c._chu_cua(d["ma_hd"]), _c._chu_cua(d["le"])
        if m not in ma_co:
            ma_co.append(m)
        if l != LE_CFA3:
            thieu.append(f"LE_la@{l}")
    thieu += sorted(m for m in ma_co if m not in cay)
    nc = _NGU_CANH
    toan_0: int | None = None
    if nc is None:
        thieu.append("NGU_CANH@thiếu")
    else:
        ma_khoi = [_c._chu_cua(r["ma"]) for r in nc["hd"]]
        c = Counter(ma_khoi)
        thieu += [f"{m}:lạ" for m in sorted(m for m in c if m not in cay)]
        thieu += [f"{m}:trùng" for m in sorted(m for m, n in c.items() if n > 1)]
        thieu += [f"{m}:vắng" for m in sorted(cay - set(ma_khoi))]
        toan_0 = len(set(ma_khoi) - set(ma_co))
        thuc = Counter(_c._chu_cua(x["gia"]) for x in nc["o_loi"])
        if dict(thuc) != dict(O_LOI_GIA):
            thieu.append(f"o_loi_gia@khác: khai {sum(O_LOI_GIA.values())} ô ≠ thực "
                         f"{sum(thuc.values())} ô")
    dai = (f"{len(ma_co)} mã HD trên dòng chính *(≠ 0)* · cây đầy đủ "
           f"{'?' if nc is None else len(nc['hd'])} hàng == ATL {len(cay)} · hàng toàn-0 "
           f"{'?' if toan_0 is None else toan_0} *(Đ3 mẫu số)* · o_loi khai "
           f"{sum(O_LOI_GIA.values())} · 1 LE {LE_CFA3} · nguồn {_c.NGUON_CAY.name}")
    return {"thieu": thieu, "lac": [], "dai": dai}
