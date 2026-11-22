"""Bộ máy CHUNG cho sáu khuôn PLA — `pla1_daily`/`pla1_yhqm` *(PD 414·415)* · `pla3_hr_daily`/
`pla3_hr_yhqm` *(416·417)* · `pla3_pm_hr_daily`/`pla3_pm_hr_yhqm` *(418·419)*.

⭐ **Vì sao tệp RIÊNG, ⛔ sửa `_cfa1.py`** *(ISP 3.1.2 · Step 31 · DT7 · `WO-261` AC-7)*. Sáu tab PLA có
**cùng bố cục cây HD** với CFA1 *(6 nhóm HDO…HDCI × 74 mã, cột L1…L4 ở B…E, trục cột G trở đi)*
nhưng KHÁC ở ba chỗ đã ĐO 20/11 — nên mượn `_cfa1.dung_cay` *(cứng 5 khối LE · `LE`)* là sai:
  · **12 khối** *(⛔ 5)*: `GROUP · SGO2 · SGO1 · HGO6 · BGO2` rồi 7 khối mang nhãn dạng
    `CVL | Vision…` *(mã đứng trước `" | "`)*; tab `417` *(PLA3 HR Y/H/Q/M)* chỉ có **1 khối**
    `GROUP` *(92 hàng)* — ⛔ giả định đủ khối.
  · **Hàng KPI** *(công thức chéo hàng: EBITDA · NCF · PL2 …)* nằm NGAY trong cây HD — AC-5 buộc
    đóng băng nhưng KHAI RIÊNG. Khai ở hằng `LOAI_MA` *(đo từ công thức cột G của tab 418)*.
  · **Hàng không nhãn** *(đo: dòng sheet 35 của khối `GROUP` — cột A là số, `B…E` rỗng)*: ⛔ bỏ im
    lặng — nếu có ô ≠ 0 thì vào bảng phụ `hang_khong_nhan`, ĐẾM.

⭐ **Dùng lại** *(⛔ chép)* từ `_cfa1` qua `importlib`: `_o` · `_chuoi` · `_la_so` · `_loai_hang` ·
`_an_toan` · `soat_pii_luoi` · `boc_o` · `ngay_tu_serial` · `ma_cay_atl` · `NHOM`; và từ
`cfa1_yhqm`: `_khoa_ky` · `_KY_CHUAN` *(luật khoá kỳ)*. ⛔ sửa chúng ⇒ mọi ảnh cũ đúng từng byte.

⭐ **Hợp đồng bản thô = LƯỚI SA** `{spreadsheet_id, nguon, doc_luc, cach_doc, values}` — hệt CFA1.
Ô số ≠ 0 ở hàng HD ⇒ dòng chính thưa; ô ⛔ số *(`-` · `#REF!`)* ⇒ bảng phụ `o_loi` *(giữ NGUYÊN
chuỗi, ĐẾM theo cột, ⛔ hoá 0 — `DT5-R1-04`)*. Cột A *(mUSD)* ⛔ vào ảnh.
"""
from __future__ import annotations

import datetime
import importlib.util
import pathlib
import sys
from collections import Counter, OrderedDict
from typing import Any

_D = pathlib.Path(__file__).resolve().parent


def _nap(ten: str):
    p = _D / f"{ten}.py"
    spec = importlib.util.spec_from_file_location(f"khuon_dong_bang__{ten}", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


_c = _nap("_cfa1")
_y = _nap("cfa1_yhqm")

_o, _chuoi, _la_so, _loai_hang = _c._o, _c._chuoi, _c._la_so, _c._loai_hang
_an_toan, soat_pii_luoi, boc_o = _c._an_toan, _c.soat_pii_luoi, _c.boc_o
ngay_tu_serial, ma_cay_atl, NHOM, _TACH = _c.ngay_tu_serial, _c.ma_cay_atl, _c.NHOM, _c._TACH
_chu_cua = _c._chu_cua

#: 12 khối của bốn tab `414·415·416·418·419` *(thứ tự như sheet; ĐO 20/11)*. `417` chỉ 1 khối.
LE12 = ("GROUP", "SGO2", "SGO1", "HGO6", "BGO2", "CVL", "COR", "SHQ1", "CSM", "CAH", "ASA", "SHQ2")
LE1 = ("GROUP",)

I_DAY, I_DOW, I_YEAR, I_PERIOD, COT_DAU = 4, 5, 4, 5, 6
SERIAL_MOC = 45585                                   # 2024-10-20 (CN) — cột ngày đầu THẬT
_DOW_IDX = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}

#: ⭐ Loại hàng theo CÔNG THỨC cột G của tab `418` *(ĐO 20/11 trên 12 khối, `BG-262`)*:
#:   `la`  = ô tra sổ / bằng *PLA1 + PLA3 HR cùng vị trí* ⇒ vào phép tự kiểm cộng (AC-2);
#:   `tong`= cha cộng con `=sum(G…)` ⇒ cộng tuyến tính nên cũng vào phép cộng;
#:   `kpi` = công thức CHÉO hàng *(EBITDA · NCF · PL2 …)* ⇒ AC-5: đóng băng, KHAI RIÊNG, ⛔ trộn
#:           vào số ô khớp *(dấu HR ở tab 416 ngược 414: `G8-G9-G23` vs `G8+G9+G23` ⇒ cộng vị trí ⛔ đúng)*;
#:   `trong` = hàng KHÔNG công thức ở cột G *(AR · CP1.x · PL5 · CFO — nguồn để trống/hằng)*.
#: Khai ở khuôn con — `LOAI_MA` rỗng ⇒ lỗi khuôn.
LOAI_MA: dict[str, str] = {}
for _l, _ds in {
    "la": "GI OMC MC OTMC COT PS API SC LC DC CSO OFR GAH BRC HCC REC BON BUT OPO CXA OGA CXP OSF FNS "
          "CIO CXB CXO ITE CFI LMN OMN NIS INT PIT COM DEP NB TAC CIT CRI",
    "tong": "OPC CAC MAC COS GAC CDC CXI NCFO NCFI NCFF",
    "kpi": "EBITDA EBIT EBT NP NPC NCF CRO COO COI CRF COF PL2 PL3 PL4 PL6 PL7 PL8",
    "trong": "AR CP1.1 CP1.2 CP2 CP3 CFO PL5",
}.items():
    for _m in _ds.split():
        LOAI_MA[_m] = _l
#: ⚠ mã trong cây ATL là `CP1.1 (PL2)` — khoá riêng vì có khoảng trắng.
LOAI_MA["CP1.1 (PL2)"] = LOAI_MA.pop("CP1.1")
assert len(LOAI_MA) == 74, len(LOAI_MA)


def dung_cay(values: list[list], le_mong: tuple[str, ...], loai_ma: dict[str, str]
             ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Lưới → (`hd` hàng HD · `le` khối · `khong_nhan` hàng không nhãn có ô ≠ 0).

    `ValueError` ⇒ TỪ CHỐI: số hàng nhóm `HDO` ≠ khối mong · mã LE lạ/sai thứ tự · khối ≠ 74 mã ·
    nhóm lạ · dữ liệu SAU vùng canh *(rác lọt giữa bảng)*. `cha` = thụt cột trong khối."""
    hdo = [i for i, r in enumerate(values)
           if _loai_hang(r)[0] == "nhom" and _chuoi(r, 1) == "HDO"]
    if len(hdo) != len(le_mong):
        raise ValueError(f"thấy {len(hdo)} hàng nhóm HDO ≠ {len(le_mong)} khối mong "
                         f"*(mỗi khối mở bằng một hàng HDO có mã khối ở cột A)*")
    hd: list[dict[str, Any]] = []
    le_ra: list[dict[str, Any]] = []
    khong_nhan: list[dict[str, Any]] = []
    for bi, start in enumerate(hdo):
        end = hdo[bi + 1] if bi + 1 < len(hdo) else len(values)
        a = _chuoi(values[start], 0)
        ma_le, _, ten_le = (a or "").partition(_TACH)
        ma_le = ma_le.strip()
        if ma_le != le_mong[bi]:
            raise ValueError(f"khối {bi} *(hàng sheet {start + 1}, cột A)*: mã khối = "
                             f"{_an_toan(ma_le)} ≠ mong {le_mong[bi]!r} *(thứ tự {list(le_mong)})*")
        le_ra.append({"le": ma_le, "ten_le": ten_le.strip() or ma_le, "dong_dau": start + 1})
        ngan: list[tuple[int, str]] = []
        nhom_hien: str | None = None
        xong = False
        n_ma = 0
        for i in range(start, end):
            r = values[i]
            lo, col = _loai_hang(r)
            if lo == "trong":
                # hàng không nhãn B…E nhưng có ô SỐ ≠ 0 ở vùng dữ liệu ⇒ ⛔ bỏ im lặng
                if not xong and i > start:
                    n = sum(1 for v in r[COT_DAU:] if _la_so(v) and v != 0)
                    if n:
                        khong_nhan.append({"le": ma_le, "dong_sheet": i + 1, "so_o_khac_0": n})
                continue
            if lo == "khac":
                xong = True
                continue
            if xong:
                raise ValueError(f"dòng sheet {i + 1} *(khối {ma_le})*: dữ liệu `{lo}` nằm SAU "
                                 "vùng canh/CHECK ZONE — rác lọt giữa bảng")
            if lo == "nhom":
                nhom_hien = _chuoi(r, 1)
                if nhom_hien not in NHOM:
                    raise ValueError(f"dòng sheet {i + 1}: nhóm {_an_toan(nhom_hien)} ⛔ thuộc "
                                     f"{list(NHOM)}")
                ngan = []
                continue
            nhan = _chuoi(r, col)
            ma, ten = (x.strip() for x in nhan.split(_TACH, 1))
            if not ma or not ten:
                raise ValueError(f"dòng sheet {i + 1}: `MÃ | Tên` thiếu mã hoặc tên")
            if nhom_hien is None:
                raise ValueError(f"dòng sheet {i + 1}: dòng mã trước tiêu đề nhóm đầu")
            while ngan and ngan[-1][0] >= col:
                ngan.pop()
            hd.append({"le": ma_le, "ma": ma, "ten": ten, "cha": ngan[-1][1] if ngan else None,
                       "cap": col, "nhom": nhom_hien, "dong_sheet": i + 1,
                       "loai": loai_ma.get(ma, "?")})
            ngan.append((col, ma))
            n_ma += 1
        if n_ma != 74:
            raise ValueError(f"khối {ma_le}: {n_ma} mã HD ≠ 74 *(cây ATL)*")
    return hd, le_ra, khong_nhan


def truc_ngay(values: list[list], read_date: datetime.date) -> tuple[list, list, list[dict]]:
    """(`giu` = [(j, serial)], `tuong_lai` = [j], `ngay_truc`) — luật hệt `cfa1_daily`."""
    day = values[I_DAY]
    sers = []
    for j in range(COT_DAU, len(day)):
        v = day[j]
        if not _la_so(v):
            continue
        if int(v) != v:
            raise ValueError(f"serial ngày cột {j + 1} ⛔ nguyên")
        sers.append((j, int(v)))
    if not sers:
        raise ValueError("hàng Day *(hàng 5)* ⛔ có serial ngày nào từ cột G")
    if sers[0][1] != SERIAL_MOC:
        raise ValueError(f"cột ngày đầu serial {sers[0][1]} ≠ mốc {SERIAL_MOC} *(2024-10-20)*")
    giu = [(j, s) for j, s in sers if ngay_tu_serial(s) <= read_date]
    tl = [j for j, s in sers if ngay_tu_serial(s) > read_date]
    for k, (j, s) in enumerate(giu):
        if s != giu[0][1] + k:
            raise ValueError(f"trục ngày ⛔ liên tục ở cột {j} *(serial {s} ≠ {giu[0][1] + k})*")
    truc = []
    for j, s in giu:
        dw = values[I_DOW][j] if j < len(values[I_DOW]) else None
        if not isinstance(dw, str) or _DOW_IDX.get(dw) != (s + 6) % 7:
            raise ValueError(f"thứ ngày cột {j + 1} *(serial {s})* ⛔ khớp (serial+6)%7")
        truc.append({"ngay": s, "ngay_iso": ngay_tu_serial(s).isoformat(), "dow": dw})
    return giu, tl, truc


def truc_ky(values: list[list], read_year: int) -> tuple[list, list, list[dict]]:
    """(`giu` = [(j, nam, khoa, loai)], `tuong_lai` = [j], `ky_truc`) — luật hệt `cfa1_yhqm`."""
    yr, per = values[I_YEAR], values[I_PERIOD]
    cols = []
    for j in range(COT_DAU, len(per)):
        if per[j] is None or (isinstance(per[j], str) and not per[j].strip()):
            continue
        if not _la_so(yr[j] if j < len(yr) else None):
            raise ValueError(f"cột kỳ {j} có Period nhưng Year *(hàng 5)* ⛔ phải số")
        nam = int(yr[j])
        khoa, loai = _y._khoa_ky(nam, per[j])
        if loai == "?":
            raise ValueError(f"cột kỳ {j}: Period {_an_toan(per[j])} ⛔ thuộc năm·H·Q·tháng")
        cols.append((j, nam, khoa, loai))
    if not cols:
        raise ValueError("hàng Period *(hàng 6)* ⛔ có cột kỳ nào từ cột G")
    giu = [c for c in cols if c[1] <= read_year]
    tl = [c[0] for c in cols if c[1] > read_year]
    seq: OrderedDict[int, list[str]] = OrderedDict()
    for j, nam, khoa, loai in giu:
        seq.setdefault(nam, []).append("Y" if khoa == str(nam) else khoa[len(str(nam)):])
    for nam, toks in seq.items():
        if len(toks) != 19 or tuple(toks) != _y._KY_CHUAN:
            raise ValueError(f"năm {nam}: {len(toks)} cột kỳ ⛔ đúng thứ tự 19 Y/H/Q/M")
    return giu, tl, [{"ky": k, "nam": n, "loai": lo} for j, n, k, lo in giu]


def kiem_tuong_lai_rong(values: list[list], hd: list[dict], tl: list[int]) -> list[dict]:
    """③ Cột tương lai *(năm > năm đọc · ngày > ngày đọc)*: ô SỐ phải 0/rỗng — ô số ≠ 0 ⇒ `ValueError`
    *(⛔ dám cắt)*. ⚠ KHÁC `_cfa1`: ĐO 20/11 ở tab `419` các cột tương lai mang ô CHỮ `-` *(hằng gõ tay
    ở hàng `AR`)* — `_cfa1` coi chữ là ≠ 0 và TỪ CHỐI cả tab. Chữ không phải SỐ ⇒ ⛔ cắt mất số; nhưng
    ⛔ cắt im lặng ⇒ trả bảng `tuong_lai_chu` `{gia, so_o}` *(phân bố THEO GIÁ; pytest ghim THEO CỘT)*."""
    dem: Counter = Counter()
    for d in hd:
        r = values[d["dong_sheet"] - 1]
        for j in tl:
            v = _o(r, j)
            if v is None:
                continue
            if _la_so(v):
                if v != 0:
                    raise ValueError(f"cột tương lai {j} *(dòng sheet {d['dong_sheet']})* có ô số ≠ 0 "
                                     "⇒ ⛔ cắt được — trục cột phải dừng ở ngày/năm đọc")
            else:
                dem[_chu_cua(v) if isinstance(v, str) else str(v)] += 1
    return [{"gia": g, "so_o": n} for g, n in sorted(dem.items())]


def trang_thai_truc(values: list[list], hd: list[dict], cot_giu: list[int]) -> dict[int, str]:
    """Cột trục `co_so` ⇔ ≥ 1 ô SỐ ≠ 0 ở hàng HD; ⛔ ⇒ `chua_co_du_lieu` *(AC-4 — ghi tên, ⛔ hoá 0)*."""
    co = {j: False for j in cot_giu}
    for d in hd:
        r = values[d["dong_sheet"] - 1]
        for j in cot_giu:
            v = _o(r, j)
            if _la_so(v) and v != 0:
                co[j] = True
    return {j: ("co_so" if c else "chua_co_du_lieu") for j, c in co.items()}


# ── cổng DT7 *(Đ5 — hai chiều)* ─────────────────────────────────────────────
_NGU_CANH: dict[str, Any] | None = None


def ghi_ngu_canh(hd, o_loi, o_loi_gia_mong, le_mong, ten_truc, tl_chu, tl_chu_mong) -> None:
    global _NGU_CANH
    _NGU_CANH = {"hd": hd, "o_loi": o_loi, "gia_mong": dict(o_loi_gia_mong), "tl_chu": tl_chu,
                 "tl_chu_mong": dict(tl_chu_mong),
                 "le_mong": tuple(le_mong), "ten_truc": ten_truc}


def cong(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng DÙNG CHUNG sáu khuôn. ĐỎ *(`thieu` ⛔ rỗng)* khi: mã ở dòng chính ⛔ ∈ cây ATL · khối ⛔
    ∈ khối mong · cây đầy đủ mỗi khối ≠ ATL 74 CHÍNH XÁC *(lạ · vắng · trùng)* · mã chưa khai
    `loai` *(`?`)* · phân bố ô lỗi ≠ bản khai · ⛔ có ngữ cảnh *(Đ5: ⛔ đo được = ĐỎ)*."""
    cay = ma_cay_atl()
    thieu: list[str] = []
    nc = _NGU_CANH
    if nc is None:
        return {"thieu": ["NGU_CANH@thiếu"], "lac": [], "dai": "⛔ có ngữ cảnh"}
    le_mong = nc["le_mong"]
    co_so, ma_co, le_co = set(), [], []
    for d in dong:
        m, le = _chu_cua(d["ma_hd"]), _chu_cua(d["le"])
        co_so.add((le, m))
        if m not in ma_co:
            ma_co.append(m)
        if le not in le_co:
            le_co.append(le)
    thieu += sorted(m for m in ma_co if m not in cay)
    thieu += [f"LE_la@{le}" for le in sorted(x for x in le_co if x not in le_mong)]
    hd = nc["hd"]
    for le in le_mong:
        ma_khoi = [_chu_cua(r["ma"]) for r in hd if _chu_cua(r["le"]) == le]
        c = Counter(ma_khoi)
        thieu += [f"{le}:lạ@{m}" for m in sorted(m for m in c if m not in cay)]
        thieu += [f"{le}:trùng@{m}" for m in sorted(m for m, n in c.items() if n > 1)]
        thieu += [f"{le}:vắng@{m}" for m in sorted(cay - set(ma_khoi))]
    thieu += sorted({f"loai_chua_khai@{_chu_cua(r['ma'])}" for r in hd if _chu_cua(r["loai"]) == "?"})
    rows = {(_chu_cua(r["le"]), _chu_cua(r["ma"])) for r in hd}
    toan_0 = sum(1 for r in rows if r not in co_so)
    thuc = Counter(_chu_cua(x["gia"]) for x in nc["o_loi"])
    mong = nc["gia_mong"]                                 # phân bố THEO GIÁ; theo CỘT ghim ở pytest
    if dict(thuc) != dict(mong):
        def _d(m: dict) -> str:
            return "{" + ", ".join(f"{_an_toan(k)[:20]}:{v}" for k, v in sorted(m.items())) + "}"
        thieu.append(f"o_loi_gia@khác: khai {_d(mong)} ≠ thực {_d(dict(thuc))}")
    tl = {x["gia"]: x["so_o"] for x in nc["tl_chu"]}
    if tl != nc["tl_chu_mong"]:
        thieu.append(f"tuong_lai_chu@khác: khai {sum(nc['tl_chu_mong'].values())} ô ≠ thực {sum(tl.values())} ô")
    dai = (f"{len(ma_co)} mã HD *(dòng chính ≠ 0)* · cây đầy đủ {len(hd)} hàng = "
           f"{len(le_mong)} khối × ATL {len(cay)} · hàng toàn-0 {toan_0} *(Đ3 mẫu số)* · "
           f"o_loi khai {sum(mong.values())} ô · {len(le_co)} khối có số")
    return {"thieu": thieu, "lac": [], "dai": dai}


def phan_bo_o_loi(o_loi: list[dict], ten_truc: str) -> dict[str, int]:
    """Phân bố ô lỗi THEO (giá, cột trục) — dạng `{"giá@cột": n}`; giá chỉ hiện nguyên khi là token
    an toàn *(⛔ PII — `_an_toan`)*."""
    return dict(Counter(f"{_chu_cua(x['gia'])}@{x[ten_truc]}" for x in o_loi))


def chuan_bi_chung(tho: dict[str, Any], *, kieu: str, le_mong: tuple[str, ...], ten_pd: str,
                   o_loi_gia: dict[str, int], tl_chu_gia: dict[str, int]) -> dict[str, Any]:
    """LƯỚI SA → `{cot, dong, phu, ghi_chu}`. `kieu` = `ngay` | `ky`. `ValueError` ⇒ TỪ CHỐI."""
    values = tho.get("values")
    if not isinstance(values, list) or len(values) <= COT_DAU:
        raise ValueError("`values` phải lưới đủ 6 hàng tiêu đề + dữ liệu")
    soat_pii_luoi(values)                                          # ⛔ PII trước mọi thứ (AC-8)
    doc = datetime.date.fromisoformat(tho["doc_luc"])
    if kieu == "ngay":
        giu, tl, truc = truc_ngay(values, doc)
        cot_giu = [(j, str(s), s) for j, s in giu]
        ten_truc, ten_bang = "ngay", "ngay_truc"
        cot_idx = [j for j, _ in giu]
    else:
        giu, tl, truc = truc_ky(values, doc.year)
        cot_giu = [(j, k, k) for j, n, k, lo in giu]
        ten_truc, ten_bang = "ky", "ky_truc"
        cot_idx = [c[0] for c in giu]
    hd, le_ra, khong_nhan = dung_cay(values, le_mong, LOAI_MA)
    tl_chu = kiem_tuong_lai_rong(values, hd, tl)                   # ③ cột tương lai: số toàn 0
    dong, o_loi = boc_o(values, hd, cot_giu, ten_truc)
    tt = trang_thai_truc(values, hd, cot_idx)
    for t, j in zip(truc, cot_idx):
        t["trang_thai"] = tt[j]
    ghi_ngu_canh(hd, o_loi, o_loi_gia, le_mong, ten_truc, tl_chu, tl_chu_gia)
    n_chua = sum(1 for t in truc if t["trang_thai"] == "chua_co_du_lieu")
    kpi = sum(1 for d in hd if d["loai"] == "kpi")
    return {
        "cot": ["o_id", "le", "ma_hd", ten_truc, "gt"],
        "dong": dong,
        "phu": {"hd": hd, "le": le_ra, ten_bang: truc, "o_loi": o_loi,
                "hang_khong_nhan": khong_nhan, "tuong_lai_chu": tl_chu},
        "ghi_chu": (
            f"{ten_pd} *(lưới SA)*: {len(le_mong)} khối {list(le_mong)} × 74 mã HD = {len(hd)} hàng "
            f"*(trong đó {kpi} hàng `kpi`, khai RIÊNG — AC-5)*; trục {ten_truc.upper()} "
            f"{len(giu)} cột, cắt {len(tl)} cột tương lai (toàn 0), {n_chua} cột `chua_co_du_lieu` "
            f"*(⛔ hoá 0 — chỉ GHI)*. {len(dong)} ô số ≠ 0 ⇒ dòng chính thưa (ô 0/vắng ⇒ 0); "
            f"{len(o_loi)} ô ⛔ số ⇒ `o_loi` (giữ chuỗi, ĐẾM theo cột, ⛔ hoá 0 — AC-6); "
            f"{sum(x['so_o'] for x in tl_chu)} ô CHỮ ở cột tương lai bị cắt ⇒ `tuong_lai_chu` (ĐẾM, ⛔ hoá 0); "
            f"{len(khong_nhan)} hàng không nhãn có ô ≠ 0. Cột A (mUSD) ⛔ vào ảnh."),
    }
