"""`IX.ALR` — **luật phân bổ có hiệu lực theo kỳ + cờ `bat` mặc định TẮT** *(AP v3.1.2 §3.2.2
IX.ALR · §3.2.5 · §3.5.3 D2 · D3 · Q3 — ISP 3.1.2 · Step 25 · `C11` · `WO-180`)*.

Làn **BE-CF**, khuôn `vendor.py`/`ky.py`: lõi kiểm THUẦN, bản config được TRUYỀN VÀO *(⛔ biết
kho — `.importlinter` hợp đồng 10)*; đọc/ghi kho là `fls/repo/cau_hinh_repo.py`.

⭐ **Lỗ mà tệp này lấp.** Luật phân bổ nằm ở `fls_mapping_master(need_cfa2, method_cfa2)` — bảng
   bị **XOÁ-NẠP LẠI toàn bộ** mỗi lần đồng bộ *(`fls/repo/nap_mapping.py`: ⛔ phiên bản)* ⇒ hỏi
   *"tháng trước HD này phân bổ thế nào"* ⛔ trả lời được. `IX.ALR` ghi luật vào kho config
   **chỉ-thêm có phiên bản**, kèm `tu_ky` *(hiệu lực từ kỳ `yyyymm`)* và cờ `bat`.

⭐ **Số đo** *(ảnh DT3 `mapping_master_cfg.json` — mỗi số một nhãn, Đ4)*: **21** mã có
   `method_cfa2` = `By GI` 8 · `By NOEM` 5 · `H1000 Ledger` 4 · `GI/OMC/PS/SC Ledger` mỗi loại 1;
   **17** là HD CÓ LUẬT *(4 + 8 + 5 — AP đo "PM 4 · by GI 8 · by NOEM 5 · by LE 0 HD")*. 4 mã
   `X Ledger` là SỔ NỀN TẢNG *(MID3)* ⇒ ⛔ luật của `IX.ALR`. Thêm **2** mã có `need_cfa2` mà
   RỖNG `method_cfa2` ⇒ ⛔ luật *(bẫy `VLOOKUP` ở `fls/ledger/allocate.py` giữ nguyên: ô `Method`
   rỗng hiện `0`, ⛔ `No need`)*.

⛔ **D2 — parity trước, cờ TẮT.** Mọi luật nạp vào có `bat` đúng `False` *(kiểm trước khi ghi:
   `True`/`0`/`"false"` ⇒ `LoiLuatPB`)*. Bật cờ là việc owner ký — ngoài ISP, ⛔ tuyến.
⭐ **D3** — `By GI` ⇒ driver `PE`. **Q3** — `H1000 Ledger` *(PM, HR)* ⇒ `khong_qua_allocate`
   *(⛔ qua ALLOCATE)*. **Ngoại lệ AP §3.2.5**: `OFR` của `CAH` ⛔ chia By NOEM *(HCM có văn
   phòng riêng)* ⇒ hỏi `OFR` mà ⛔ khai `cdt1` là lỗi CÓ TÊN `CAN_CDT1`, ⛔ đoán.

⛔ **Đếm `mong` hai chiều** *(Đ5)*: nạp từ Mapping Master mà số luật ≠ `8 · 5 · 4` — thiếu
   HAY thừa — ⇒ `LoiLuatPB`; nhãn phương pháp lạ ⇒ `LoiLuatPB`; tập rỗng ⇒ nổ *(Đ3)*.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from fls.cau_hinh import hd as hd_mod
from fls.cau_hinh import ky as ky_mod

BANG = "IX.ALR"

BY_GI = "BY_GI"
BY_NOEM = "BY_NOEM"
H1000 = "H1000_LEDGER"
# nhãn của `Mapping Master!L` → mã phương pháp. ⛔ phân biệt hoa thường (cell sheet là nguồn).
NHAN_MM: dict[str, str] = {"By GI": BY_GI, "By NOEM": BY_NOEM, "H1000 Ledger": H1000}
# 4 nhãn SỔ NỀN TẢNG (MID3) — có `method_cfa2` nhưng ⛔ phải luật IX.ALR.
NHAN_NEN_TANG: tuple[str, ...] = ("GI Ledger", "OMC Ledger", "PS Ledger", "SC Ledger")
# ⭐ mong — đếm HD có luật theo phương pháp *(AP đo "PM 4 · by GI 8 · by NOEM 5")*.
MONG_DEM: dict[str, int] = {BY_GI: 8, BY_NOEM: 5, H1000: 4}
DRIVER: dict[str, str | None] = {BY_GI: "PE", BY_NOEM: "NOEM", H1000: None}    # D3
DRIVER_BY_GI = DRIVER[BY_GI]
# AP §3.2.5: `OFR` của `CAH` ⛔ By NOEM. Khai Ở ĐÂY *(nguồn AP)*, ghi vào kho theo từng dòng.
NGOAI_LE_AP: dict[str, tuple[str, ...]] = {"OFR": ("CAH",)}
CO_PHAN_BO = "need to allocate to cfa2"

ALR_HONG = "ALR_HONG"
KY_HONG = "KY_HONG"
CAN_CDT1 = "CAN_CDT1"

_COT = ("hd", "tu_ky", "nhan_mm", "bat", "ngoai_le")


class LoiLuatPB(ValueError):
    """Lỗi `IX.ALR` **có tên**: `ma` ∈ {`ALR_HONG`, `KY_HONG`, `CAN_CDT1`}. `ly_do` = **mọi**
    lý do, ⛔ chỉ lý do đầu."""

    def __init__(self, ly_do: Iterable[str] | str, ma: str = ALR_HONG) -> None:
        self.ly_do = (ly_do,) if isinstance(ly_do, str) else tuple(ly_do)
        self.ma = ma
        super().__init__(f"{ma}: ⛔ {BANG} — {len(self.ly_do)} lỗi: " + " · ".join(self.ly_do))


@dataclass(frozen=True)
class LuatPB:
    """Một luật có hiệu lực từ kỳ `tu_ky`. `phuong_phap is None` ⇔ HD thuộc ngoại lệ `ngoai_le`
    *(⛔ chia theo luật gốc)* — khác `None` của *"HD ⛔ có luật"* ở `BangALR.luat_cua`."""

    hd: str
    tu_ky: int
    phuong_phap: str | None
    nhan_mm: str
    driver: str | None
    bat: bool
    khong_qua_allocate: bool
    ngoai_le: str | None = None
    ngoai_le_cdt1: tuple[str, ...] = ()


@dataclass(frozen=True)
class BangALR:
    nguon: str
    luat: tuple[LuatPB, ...]

    def luat_cua(self, hd: str, ky: Any, *, cdt1: str | None = None) -> LuatPB | None:
        """Luật của `hd` ở kỳ `ky` *(`yyyymm` hay `Ky`)*: bản có `tu_ky` lớn nhất ≤ `ky`.
        `None` = ⛔ có luật hiệu lực *(chưa hiệu lực / HD ⛔ có luật)*. HD có ngoại lệ mà
        ⛔ khai `cdt1` ⇒ `LoiLuatPB(CAN_CDT1)`."""
        k = _ky(ky)
        ung = [x for x in self.luat if x.hd == hd and x.tu_ky <= k]
        if not ung:
            return None
        x = max(ung, key=lambda y: y.tu_ky)
        if not x.ngoai_le_cdt1:
            return x
        if cdt1 is None or not str(cdt1).strip():        # `C11-R1-03`: "" / khoảng trắng = THIẾU
            raise LoiLuatPB(f"HD {hd!r} có ngoại lệ theo CDT1 {list(x.ngoai_le_cdt1)} — phải "
                            f"khai cdt1, ⛔ đoán", CAN_CDT1)
        if cdt1 in x.ngoai_le_cdt1:
            return LuatPB(hd=x.hd, tu_ky=x.tu_ky, phuong_phap=None, nhan_mm=x.nhan_mm,
                          driver=None, bat=x.bat, khong_qua_allocate=False,
                          ngoai_le=cdt1, ngoai_le_cdt1=x.ngoai_le_cdt1)
        return x


def _ky(ky: Any) -> int:
    if isinstance(ky, ky_mod.Ky):
        ky = ky.nam * 100 + ky.thang
    if isinstance(ky, bool) or not isinstance(ky, int) or not 190001 <= ky <= 299912 \
            or not 1 <= ky % 100 <= 12:
        raise LoiLuatPB(f"ky={ky!r} ⛔ yyyymm (190001…299912, tháng 1…12) hay Ky", KY_HONG)
    return ky


def _mot(s: Any) -> str:
    return " ".join(repr(s).split())


def khoa_cua(hd: str, tu_ky: int) -> str:
    """Khoá kho của một luật: `'<hd>@<tu_ky>'` — cùng `(hd, tu_ky)` hai lần ⇒ khoá trùng."""
    return f"{hd}@{tu_ky}"


def kiem(dong: Iterable[Mapping[str, Any]], *, nguon: str) -> BangALR:
    """Kiểm **thuần**. Mỗi dòng đúng `{hd, tu_ky, nhan_mm, bat, ngoai_le}` *(có thể thêm `khoa`
    — đọc từ kho — phải KHỚP `hd@tu_ky`)*. Hỏng ⇒ `LoiLuatPB` *(mọi lý do)*."""
    ly: list[str] = []
    ds: list[LuatPB] = []
    for i, r in enumerate(dong, start=1):
        if not isinstance(r, Mapping):
            ly.append(f"dòng {i}: ⛔ phải một đối tượng")
            continue
        la = sorted(k for k in r if k not in _COT and k != "khoa")
        thieu = sorted(k for k in _COT if k not in r)
        if la:
            ly.append(f"dòng {i}: cột lạ {la}")
        if thieu:
            ly.append(f"dòng {i}: thiếu cột {thieu}")
        if la or thieu:
            continue
        n0 = len(ly)
        hd, tu_ky, nhan, bat, nl = (r["hd"], r["tu_ky"], r["nhan_mm"], r["bat"], r["ngoai_le"])
        if not isinstance(hd, str) or not hd.strip():
            ly.append(f"dòng {i}: hd={_mot(hd)} ⛔ phải chuỗi ⛔ rỗng")
        if isinstance(tu_ky, bool) or not isinstance(tu_ky, int) \
                or not 190001 <= tu_ky <= 299912 or not 1 <= tu_ky % 100 <= 12:
            ly.append(f"dòng {i}: tu_ky={_mot(tu_ky)} ⛔ số nguyên yyyymm hợp lệ")
        if nhan not in NHAN_MM:
            ly.append(f"dòng {i}: nhan_mm={_mot(nhan)} ⛔ thuộc {sorted(NHAN_MM)}")
        if bat is not False:
            ly.append(f"dòng {i}: bat={_mot(bat)} ⛔ đúng False — D2: parity trước, bật cờ "
                      f"là việc owner ký (⛔ qua nạp)")
        if not isinstance(nl, list) or any(not isinstance(c, str) or not c.strip() for c in nl) \
                or len(set(nl)) != len(nl):
            ly.append(f"dòng {i}: ngoai_le={_mot(nl)} ⛔ danh sách CDT1 không rỗng, không trùng")
        if isinstance(nl, list) and nl and isinstance(hd, str) and hd not in NGOAI_LE_AP:
            ly.append(f"dòng {i}: ngoai_le={_mot(nl)} ⛔ ở hd={hd!r} — chỉ HD AP khai "
                      f"{sorted(NGOAI_LE_AP)} mới có ngoại lệ (AP §3.2.5)")   # `C11-R1-03`
        if "khoa" in r and len(ly) == n0 and r["khoa"] != khoa_cua(hd, tu_ky):
            ly.append(f"dòng {i}: khoá {_mot(r['khoa'])} ≠ {khoa_cua(hd, tu_ky)!r} (hd@tu_ky)")
        if len(ly) == n0:
            pp = NHAN_MM[nhan]
            ds.append(LuatPB(hd=hd, tu_ky=tu_ky, phuong_phap=pp, nhan_mm=nhan,
                             driver=DRIVER[pp], bat=False, khong_qua_allocate=pp == H1000,
                             ngoai_le_cdt1=tuple(nl)))
    if not ds and not ly:
        ly.append("0 dòng ⇒ ⛔ có bảng để kiểm")
    for (h, t), n in sorted(Counter((x.hd, x.tu_ky) for x in ds).items()):
        if n >= 2:
            ly.append(f"hd={h} tu_ky={t} trùng {n} dòng")
    if ly:
        raise LoiLuatPB(ly)
    return BangALR(nguon=nguon, luat=tuple(ds))


def dung_tu_mm(dong_mm: Iterable[Mapping[str, Any]], *, tu_ky: int) -> list[dict[str, Any]]:
    """Dòng Mapping Master `{hd_code, need_cfa2, method_cfa2}` *(chuỗi thuần)* ⇒ dòng `IX.ALR`.
    Mã HD = trước ` | `. ⛔ bật cờ. Số luật ≠ `MONG_DEM` *(thiếu HAY thừa)* ⇒ `LoiLuatPB`."""
    ly: list[str] = []
    ra: list[dict[str, Any]] = []
    for i, r in enumerate(dong_mm, start=1):
        method = r.get("method_cfa2")
        if not isinstance(method, str) or not method.strip() or method in NHAN_NEN_TANG:
            continue                                        # ⛔ luật: rỗng / sổ nền tảng (MID3)
        if method not in NHAN_MM:
            ly.append(f"dòng {i}: method_cfa2={_mot(method)} ⛔ thuộc {sorted(NHAN_MM)} "
                      f"hay {list(NHAN_NEN_TANG)}")
            continue
        need = r.get("need_cfa2")
        if not isinstance(need, str) or need.strip().lower() != CO_PHAN_BO:
            ly.append(f"dòng {i}: có method_cfa2={_mot(method)} mà need_cfa2={_mot(need)} "
                      f"⛔ 'Need to Allocate to CFA2'")
            continue
        ma = hd_mod._ma_mm(str(r.get("hd_code") or ""))
        ra.append({"hd": ma, "tu_ky": tu_ky, "nhan_mm": method, "bat": False,
                   "ngoai_le": list(NGOAI_LE_AP.get(ma, ()))})
    dem = Counter(NHAN_MM[x["nhan_mm"]] for x in ra)
    for pp, mong in MONG_DEM.items():
        if dem.get(pp, 0) != mong:
            ly.append(f"{pp}: đo {dem.get(pp, 0)} HD, mong {mong}")
    ma_ra = {x["hd"] for x in ra}
    for h, cdt in NGOAI_LE_AP.items():
        if ra and h not in ma_ra:
            ly.append(f"ngoại lệ AP {h!r}×{list(cdt)} trỏ tới HD ⛔ có luật")
    if not ra and not ly:
        ly.append("0 dòng Mapping Master có luật ⇒ ⛔ có gì để nạp")
    if ly:
        raise LoiLuatPB(ly)
    return ra
