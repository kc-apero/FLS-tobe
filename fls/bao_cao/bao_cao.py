"""`RP.PL` · `RP.CF` — **Daily Report 3 · Daily Report 2 dựng theo KHUÔN**, FS là THAM SỐ *(ISP 3.1.2 · Step 46 ·
H14 · `WO-311` · AP v3.1.2 §3.3.2 PD 605–617 · §3.5.3 D5 A · cổng WP-C5c)*.

⭐ **Khái niệm mới duy nhất: dựng báo cáo theo khuôn.** Báo cáo ⛔ tính gì mới — mỗi ô là **một phép chiếu** của MỘT ô
(hoặc tổng vài ô cùng mã/cột) ở lưới ENGINE thượng nguồn, đúng phép SUMIFS/tham chiếu của sổ AS-IS. Đo 22/11 trên
các ảnh đáp án *(chỉ để HIỂU khuôn — ⛔ đầu vào; `BG-312` §1)*:

  · DR3 *(RP.PL — 607 `[FS2]` · 608 `[FS1]` · 609 `5. Daily Report 3`)* phần **ngày** = `PLA3 Daily PM + HR` *(H8 ·
    `pla.pla_pm_hr_daily`)* — **100 %** ô ≠ 0 *(304 · 269 · 306)* khớp; nhãn khối `HGO2` = khối `HGO6` của engine.
  · DR3 phần **luỹ kế `CM Cumulative`** ở FS2 = **ATL** *(H12 AL.KEY + H13 dòng PL)*; khối `SHQ` = `SHQ1 + SHQ2`.
    FS1 *(608, nửa `[FS1][PLA3]` của 609)* ⛔ khớp nguồn nào của FLS *(vd `GROUP·GI·2025` = 57,6738 ≠ ATL 57,2144)* ⇒
    `chua_co_dau_vao` CÓ TÊN *(⛔ ngầm 0, ⛔ đọc đáp án thay)*.
  · DR2 *(RP.CF — 610)* phần **ngày** = `CFA1 Daily` *(H5)*; **luỹ kế** = `CFA1 Y/H/Q/M` *(H6)* — 100 % ô ≠ 0
    *(788 · 4.687)*; phần **`hr`** *(`Report HR`, số người)* ⛔ có engine ⇒ `chua_co_dau_vao`.

⭐ **FS là THAM SỐ** *(D5 A — "cùng engine, khác tham số")*: `FS1` · `FS2` · `FS1_FS2_gop` · `FS3` chỉ đổi **tập phần
luỹ kế** của khuôn *(`KHUON_FS`)*; phần ngày + phép chiếu + JSON ra **dùng chung**.
⛔ **FS3 ⛔ phải hợp FS1 ∪ FS2** *(`H14-R1-08`, KQ-313)*: ảnh 609 VÀ 615 ghi nguyên văn *"Level báo cáo: FS1 -> FS3 trong
đó FS3 là mức độ tin cậy giao dịch đủ (PI&PM; Finance&Non-Finance) để phục vụ Audits/Due Diligence"* — FS = **cấp tin
cậy dữ liệu**, FS3 là cấp CAO NHẤT *(data đủ VÀ consistent với Non-Finance)*. Bản `5. Daily Report 3` *(609)* chỉ mang
hai khối `[FS1][PLA3]` + `[FS2][PLA3]` ⇒ tên đúng nghĩa hiện dựng là **`FS1_FS2_gop`**. `FS3` thật ⛔ dựng: phần luỹ kế
của nó DỪNG `chua_co_dau_vao` *(nguồn `fs3_tin_cay` ⛔ tồn tại — câu hỏi BA: định nghĩa FS3 + đầu vào Non-Finance)*;
⛔ trả nhãn FS3 cho dữ liệu FS1/FS2 *(chủ gọi FS3 để nộp Audit sẽ nhận nhầm)*.

⭐ **Đầu ra = JSON ô theo hợp đồng C13** *(`ban_ky.checksum`: object JSON THUẦN — ⛔ `Decimal`)* ⇒ giá trị là CHUỖI
`str(Decimal)`; khoá ô `"<phần>|<khối>|<mã>|<cột>"` *(cột = ngày ISO hoặc kỳ `2025` · `2025H1` · `2025Q1` · `2025M01`)*.
Cùng đầu vào ⇒ cùng byte ⇒ `dua_ban_ky` trả `khong_doi` *(bài AC-3)*.

⛔ Engine ⛔ đọc kho, ⛔ đọc tệp, ⛔ đọc đáp án: mọi lưới thượng nguồn đến qua tham số `nguon`. Lưới vắng mặt ⇒ phần ấy
vào `chua_co_dau_vao` *(có tên + cần gì)*, ⛔ 0. Ô vắng trong lưới có mặt ⇒ ⛔ in *(lưới engine thượng nguồn là lưới
ĐỦ — vắng = engine ⛔ tính ô ấy; nơi so đếm riêng)*.
"""
from __future__ import annotations

import calendar
import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Mapping, Sequence

from fls.bao_cao import pla

#: khối LE của phần ngày *(nhãn sổ → khối engine)*. ⚠ sổ ghi `HGO2`, engine/ảnh CFA1·PLA gọi `HGO6` — đo khớp 100 %.
KHOI_LE: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("GROUP", ("GROUP",)), ("SGO2", ("SGO2",)), ("SGO1", ("SGO1",)), ("HGO2", ("HGO6",)), ("BGO2", ("BGO2",)))
#: 6 khối CDT của nửa luỹ kế P&L; `SHQ` = `SHQ1 + SHQ2` *(đo: `SHQ·GI·2025` 0,7777 = 0,2393 + 0,5385)*
KHOI_CDT: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("CVL", ("CVL",)), ("COR", ("COR",)), ("CSM", ("CSM",)), ("CAH", ("CAH",)), ("ASA", ("ASA",)),
    ("SHQ", ("SHQ1", "SHQ2")))

#: nguồn → cần gì nếu vắng *(câu báo DỪNG — tiền lệ DT7b)*
CAN_ANH = {
    "pla3_daily": "lưới SO.PLA3 Daily PM + HR của engine H8 (`pla.pla_pm_hr_daily`)",
    "atl": "lưới ATL của FLS (AL.KEY H12 + dòng PL H13)",
    "atl_fs1": "ảnh nguồn của bản `[FS1][PLA3]` Y/H/Q/M (tab PLA3 FS1 ở sổ P&L Report) — FLS ⛔ có engine sinh nó; "
                "đo 22/11: ATL FLS ⛔ tái lập (vd GROUP·GI·2025 57,6738 ≠ 57,2144)",
    "cfa1_daily": "lưới SO.CFA1 Daily của engine H5 (`cfa.cfa1_daily`)",
    "cfa1_yhqm": "lưới SO.CFA1 Y/H/Q/M của engine H6 (`cfa.cuon_ky`)",
    "hr_report": "ảnh `Report HR` (số người theo Grade, sổ CF report hàng 843+) — FLS ⛔ có engine số người",
    "fs3_tin_cay": "cấp FS3 = data đủ (PI&PM) VÀ consistent với data Non-Finance (ảnh 609/615: 'mức độ tin cậy giao "
                   "dịch đủ (PI&PM; Finance&Non-Finance) để phục vụ Audits/Due Diligence') — FLS ⛔ có nguồn/engine; "
                   "định nghĩa FS3 chờ BA (H14-R1-08) ⇒ ⛔ dựng",
}


@dataclass(frozen=True)
class Phan:
    """Một phần của khuôn: `id` · chế độ trục *(`ngay` | `ky`)* · nguồn · khối *(nhãn → khối engine)* · năm luỹ kế."""
    id: str
    truc: str
    nguon: str
    khoi: tuple[tuple[str, tuple[str, ...]], ...]
    nam: tuple[int, ...] = (0,)          # năm luỹ kế, tương đối năm của `ky` *(CF: (-1, 0))*


#: luỹ kế P&L theo FS — chỗ DUY NHẤT FS làm khác *(D5 A)*
_LK_FS2 = Phan("luy_ke:FS2", "ky", "atl", KHOI_LE + KHOI_CDT)
_LK_FS1 = Phan("luy_ke:FS1", "ky", "atl_fs1", (KHOI_LE[0],) + KHOI_CDT)
_LK_FS3 = Phan("luy_ke:FS3", "ky", "fs3_tin_cay", KHOI_LE + KHOI_CDT)     # ⛔ nguồn nào sinh ⇒ luôn DỪNG có tên
KHUON_FS: dict[str, tuple[Phan, ...]] = {"FS1": (_LK_FS1,), "FS2": (_LK_FS2,), "FS1_FS2_gop": (_LK_FS1, _LK_FS2),
                                         "FS3": (_LK_FS3,)}

KHUON: dict[str, dict[str, Any]] = {
    "PL": {"ten": "RP.PL · Daily Report 3", "don_vi": "mUSD",
           "chung": (Phan("ngay", "ngay", "pla3_daily", KHOI_LE),)},
    "CF": {"ten": "RP.CF · Daily Report 2", "don_vi": "mUSD",
           "chung": (Phan("ngay", "ngay", "cfa1_daily", KHOI_LE),
                     Phan("luy_ke", "ky", "cfa1_yhqm", KHOI_LE, nam=(-1, 0)),
                     Phan("hr", "ky", "hr_report", (KHOI_LE[0],), nam=(-1, 0)))},
}
FS_HOP_LE = tuple(KHUON_FS)


class LoiBaoCao(ValueError):
    """Tham số báo cáo hỏng *(kỳ · FS · loại)* — CÓ TÊN, ⛔ rơi về mặc định."""


def kiem_ky(ky: Any) -> tuple[int, int]:
    """`yyyymm` *(int/str)* hoặc `yyyy-mm` ⇒ (năm, tháng)."""
    s = str(ky).strip().replace("-", "")
    if len(s) != 6 or not s.isdigit() or not 1 <= int(s[4:]) <= 12:
        raise LoiBaoCao(f"ky={ky!r} ⛔ đúng khuôn yyyymm / yyyy-mm")
    return int(s[:4]), int(s[4:])


def _serial(d: datetime.date) -> int:
    return (d - datetime.date(1899, 12, 30)).days


def cot_ngay(nam: int, thang: int) -> list[datetime.date]:
    """Mọi ngày của tháng `ky` *(đo: 607/608/610 = 30 ngày; 609 tháng 12 = 31 ngày, `AK` là ngày thật)*."""
    return [datetime.date(nam, thang, d) for d in range(1, calendar.monthrange(nam, thang)[1] + 1)]


def cot_ky(nam: int) -> list[str]:
    """19 kỳ một năm theo thứ tự sổ: Y · H1 · H2 · Q1…Q4 · M01…M12 *(khoá như `cfa.ky_truc_nam`)*."""
    return [f"{nam}", f"{nam}H1", f"{nam}H2"] + [f"{nam}Q{q}" for q in range(1, 5)] + \
        [f"{nam}M{m:02d}" for m in range(1, 13)]


def khuon(loai: str, fs: str) -> tuple[Phan, ...]:
    if loai not in KHUON:
        raise LoiBaoCao(f"loai={loai!r} ⛔ ∈ {tuple(KHUON)}")
    if loai == "CF":
        return KHUON["CF"]["chung"]
    if fs not in KHUON_FS:
        raise LoiBaoCao(f"fs={fs!r} ⛔ ∈ {FS_HOP_LE} (D5 A: FS là tham số của MỘT engine)")
    return KHUON["PL"]["chung"] + KHUON_FS[fs]


def _chieu(luoi: Mapping[tuple, Any], khoi: Sequence[str], ma: str, c: Any) -> Decimal | None:
    """Phép chiếu MỘT ô: Σ các khối engine của nhãn *(SHQ = SHQ1 + SHQ2)*; thiếu một phần ⇒ None *(⛔ tổng dở)*."""
    s = Decimal(0)
    for k in khoi:
        v = luoi.get((k, ma, c))
        if v is None:
            return None
        s += Decimal(str(v))
    return s


def khoa_o(phan: str, khoi: str, ma: str, cot: str) -> str:
    return f"{phan}|{khoi}|{ma}|{cot}"


def daily_report(ky: Any, fs: str, nguon: Mapping[str, Mapping[tuple, Any] | None], *,
                 loai: str = "PL") -> dict[str, Any]:
    """Dựng một Daily Report theo khuôn ⇒ JSON ô THUẦN *(hợp đồng C13)*.

    `nguon` = {tên nguồn → lưới engine `(khối, mã, cột) → số`}; cột = serial ngày *(phần ngày)* hoặc kỳ `2025M01`
    *(phần luỹ kế)*. Nguồn vắng/`None` ⇒ phần ấy DỪNG, ghi `chua_co_dau_vao` *(cần gì)*.
    """
    nam, thang = kiem_ky(ky)
    phan_ds = khuon(loai, fs)
    o: dict[str, str] = {}
    phan_ra: list[dict[str, Any]] = []
    chua: list[dict[str, Any]] = []
    for p in phan_ds:
        if p.truc == "ngay":
            ngay = cot_ngay(nam, thang)
            cot = [(d.isoformat(), _serial(d)) for d in ngay]
        else:
            cot = [(k, k) for n in p.nam for k in cot_ky(nam + n)]
        luoi = nguon.get(p.nguon)
        mo_ta = {"id": p.id, "nguon": p.nguon, "truc": p.truc, "khoi": [n for n, _ in p.khoi],
                 "cot": [c for c, _ in cot]}
        if not luoi:
            chua.append({"phan": p.id, "nguon": p.nguon, "khoi": mo_ta["khoi"], "can": CAN_ANH[p.nguon]})
            mo_ta["dung"] = "chua_co_dau_vao"
            phan_ra.append(mo_ta)
            continue
        ma_theo_khoi: dict[str, set[str]] = {}
        for (k, m, _c) in luoi:
            ma_theo_khoi.setdefault(k, set()).add(m)
        so = 0
        for nhan, khoi in p.khoi:
            ma_ds = set.intersection(*(ma_theo_khoi.get(k, set()) for k in khoi))
            for m in sorted(ma_ds):
                for c, ck in cot:
                    v = _chieu(luoi, khoi, m, ck)
                    if v is not None:
                        o[khoa_o(p.id, nhan, m, c)] = str(v)
                        so += 1
        mo_ta["so_o"] = so
        phan_ra.append(mo_ta)
    return {"bao_cao": KHUON[loai]["ten"], "loai": loai, "ky": nam * 100 + thang,
            "fs": fs if loai == "PL" else None, "don_vi": KHUON[loai]["don_vi"],
            "phan": phan_ra, "chua_co_dau_vao": chua, "check": check_bao_cao(o, phan_ra), "o": o}


def rp_pl(ky: Any, fs: str, nguon: Mapping[str, Any]) -> dict[str, Any]:
    """RP.PL = Daily Report 3 *(P&L)*; FS ∈ FS1 · FS2 · FS1_FS2_gop *(609)* · FS3 *(luỹ kế DỪNG — `H14-R1-08`)*."""
    return daily_report(ky, fs, nguon, loai="PL")


def rp_cf(ky: Any, nguon: Mapping[str, Any]) -> dict[str, Any]:
    """RP.CF = Daily Report 2 *(sổ CF)*; ⛔ FS."""
    return daily_report(ky, "-", nguon, loai="CF")


def check_bao_cao(o: Mapping[str, str], phan: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Hai phép CHECK IX.PL *(`pla.check_atl` — dùng lại, ⛔ chép biểu thức)* ở MỖI (phần, khối, cột) của báo cáo.

    ⛔ Phán: chỉ ĐẾM theo trạng thái + LIỆT KÊ ô đỏ *(câu "CHECK đỏ có chặn đóng sổ không" đang chờ chủ — `BG-308`)*.
    """
    ra: dict[str, Any] = {"theo_phan": {}, "do": []}
    for p in phan:
        if p.get("dung") or p["nguon"] == "hr_report":
            continue
        luoi = {}
        for k, v in o.items():
            ph, kh, m, c = k.split("|")
            if ph == p["id"]:
                luoi[(kh, m, c)] = Decimal(v)
        dem: dict[str, dict[str, int]] = {}
        for x in pla.check_atl(luoi, p["khoi"], p["cot"]):
            dem.setdefault(x.phep, {t: 0 for t in pla.TRANG_THAI_CHECK})[x.trang_thai] += 1
            if x.trang_thai == "do":
                ra["do"].append(f"{p['id']}|{x.khoi}|{x.ky}|{x.phep}: {x.chenh.quantize(Decimal('1e-9'))}")
        ra["theo_phan"][p["id"]] = dem
    ra["so_do"] = len(ra["do"])
    return ra
