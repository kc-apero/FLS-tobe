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

⭐ **Bật cờ CÓ KÝ** *(vòng sửa R1 `H12` — `KQ-293`; quyết của chủ 22/11 ~10:05 UTC "ký BẬT luật phân bổ
   IX.ALR năm 2025 giống AS-IS")*: đường NẠP vẫn ⛔ bao giờ ra `bat=True`. Bật/tắt là đường RIÊNG
   `dung_tu_tep_ky` ← một TỆP config có phiên bản *(`tests/fixture/cau_hinh/ix_alr_2025_bat.json`)* mang
   `ky = {nguoi_ky, ngay, can_cu}` — người ký có TÊN *(⛔ email)*, ngày ⛔ tương lai, căn cứ ⛔ rỗng. `kiem`
   nhận `bat=True` **chỉ** khi dòng mang chữ ký hợp lệ; ghi vào kho chỉ-thêm như một phiên bản MỚI
   *(`cau_hinh_repo.ky_bat_ix_alr` — ⛔ sửa bản cũ)*.

⛔ **Đếm `mong` hai chiều** *(Đ5)*: nạp từ Mapping Master mà số luật ≠ `8 · 5 · 4` — thiếu
   HAY thừa — ⇒ `LoiLuatPB`; nhãn phương pháp lạ ⇒ `LoiLuatPB`; tập rỗng ⇒ nổ *(Đ3)*.
"""
from __future__ import annotations

import datetime
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
#: cột TUỲ CHỌN — chữ ký của dòng bật/tắt *(đường `dung_tu_tep_ky`)*
COT_KY = "ky"
KHOA_KY = ("nguoi_ky", "ngay", "can_cu")
LOAI_TEP_KY = "ky_bat_co_IX.ALR"


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
    #: người ký bật/tắt *(tên — ⛔ email)*; `None` = dòng của đường nạp *(D2, chưa ai ký)*
    nguoi_ky: str | None = None


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
                          ngoai_le=cdt1, ngoai_le_cdt1=x.ngoai_le_cdt1, nguoi_ky=x.nguoi_ky)
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


def kiem_ky(ky: Any) -> list[str]:
    """Lý do chữ ký HỎNG *(rỗng = hợp lệ)*: đúng ba khoá `nguoi_ky` · `ngay` · `can_cu`; người ký là TÊN
    *(⛔ chứa `@` — ⛔ email: luật riêng tư `CLAUDE.md`)*; ngày `YYYY-MM-DD` có thật, ⛔ tương lai."""
    if not isinstance(ky, Mapping):
        return [f"ky={_mot(ky)} ⛔ phải một đối tượng {{{', '.join(KHOA_KY)}}}"]
    ly: list[str] = []
    la = sorted(set(ky) - set(KHOA_KY))
    thieu = sorted(set(KHOA_KY) - set(ky))
    if la:
        ly.append(f"ky: khoá lạ {la}")
    if thieu:
        ly.append(f"ky: thiếu khoá {thieu}")
    if la or thieu:
        return ly
    ng = ky["nguoi_ky"]
    if not isinstance(ng, str) or not ng.strip():
        ly.append(f"ky.nguoi_ky={_mot(ng)} ⛔ phải TÊN người ký ⛔ rỗng")
    elif "@" in ng:
        ly.append("ky.nguoi_ky ⛔ được là email — ghi TÊN người ký (luật riêng tư)")
    if not isinstance(ky["can_cu"], str) or not ky["can_cu"].strip():
        ly.append(f"ky.can_cu={_mot(ky['can_cu'])} ⛔ rỗng — chữ ký phải nói quyết định nào")
    try:
        ngay = datetime.date.fromisoformat(ky["ngay"]) if isinstance(ky["ngay"], str) else None
    except ValueError:
        ngay = None
    if ngay is None:
        ly.append(f"ky.ngay={_mot(ky['ngay'])} ⛔ YYYY-MM-DD có thật")
    elif ngay > datetime.date.today():
        ly.append(f"ky.ngay={ky['ngay']} ở tương lai ⛔ ký được")
    return ly


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
        la = sorted(k for k in r if k not in _COT and k not in ("khoa", COT_KY))
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
        ky = r.get(COT_KY)
        if not isinstance(bat, bool):
            ly.append(f"dòng {i}: bat={_mot(bat)} ⛔ bool — D2: parity trước, bật cờ là việc owner ký")
        elif bat is True and COT_KY not in r:
            ly.append(f"dòng {i}: bat={_mot(bat)} ⛔ đúng False — D2: parity trước, bật cờ "
                      f"là việc owner ký (⛔ qua nạp; đường ký: `dung_tu_tep_ky`)")
        if COT_KY in r:
            ly += [f"dòng {i}: {x}" for x in kiem_ky(ky)]
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
                             driver=DRIVER[pp], bat=bat, khong_qua_allocate=pp == H1000,
                             ngoai_le_cdt1=tuple(nl),
                             nguoi_ky=ky["nguoi_ky"] if COT_KY in r else None))
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


_KHOA_TEP = ("bang", "loai", "phien_ban_tep", "ky", "mong_dem", "luat")
_COT_TEP = ("hd", "tu_ky", "bat")


def dung_tu_tep_ky(tep: Mapping[str, Any], hien: BangALR) -> list[dict[str, Any]]:
    """Tệp KÝ bật/tắt *(config có phiên bản)* ⇒ dòng `IX.ALR` mang chữ ký, sẵn cho `kiem`/kho.

    Mỗi dòng tệp chỉ `{hd, tu_ky, bat}`: `nhan_mm` + `ngoai_le` lấy từ luật HIỆN HÀNH của `hd` trong `hien`
    *(bản `tu_ky` lớn nhất — ⛔ đổi phương pháp qua đường ký)*; HD ⛔ có luật · luật ⛔ driver *(H1000 —
    Q3)* ⇒ lỗi. `mong_dem = {bat: {pp: n}, tat: {pp: n}}` khai TRƯỚC — đếm khác *(thiếu HAY thừa)* ⇒ lỗi."""
    ly: list[str] = []
    if not isinstance(tep, Mapping):
        raise LoiLuatPB("tệp ký ⛔ phải một đối tượng")
    la = sorted(set(tep) - set(_KHOA_TEP) - {"_vi_sao"})      # `_vi_sao` = lời giải thích, ⛔ dữ liệu
    thieu = sorted(set(_KHOA_TEP) - set(tep))
    if la or thieu:
        raise LoiLuatPB(f"tệp ký: khoá lạ {la} · thiếu {thieu}")
    if tep["bang"] != BANG:
        ly.append(f"tệp ký: bang={_mot(tep['bang'])} ≠ {BANG!r}")
    if tep["loai"] != LOAI_TEP_KY:
        ly.append(f"tệp ký: loai={_mot(tep['loai'])} ≠ {LOAI_TEP_KY!r}")
    pbt = tep["phien_ban_tep"]
    if isinstance(pbt, bool) or not isinstance(pbt, int) or pbt < 1:
        ly.append(f"tệp ký: phien_ban_tep={_mot(pbt)} ⛔ số nguyên ≥ 1")
    ly += [f"tệp ký: {x}" for x in kiem_ky(tep["ky"])]
    luat = tep["luat"]
    if not isinstance(luat, list) or not luat:
        ly.append("tệp ký: 0 dòng luật ⇒ ⛔ có gì để ký")
        luat = []
    moi: list[dict[str, Any]] = []
    dem: dict[str, Counter] = {"bat": Counter(), "tat": Counter()}
    for i, r in enumerate(luat, start=1):
        if not isinstance(r, Mapping) or set(r) != set(_COT_TEP):
            ly.append(f"luật {i}: cột lạ/thiếu — đúng {list(_COT_TEP)} (đo {sorted(r) if isinstance(r, Mapping) else r!r})")
            continue
        if not isinstance(r["bat"], bool):
            ly.append(f"luật {i}: bat={_mot(r['bat'])} ⛔ bool")
            continue
        cu = [x for x in hien.luat if x.hd == r["hd"]]
        if not cu:
            ly.append(f"luật {i}: hd={_mot(r['hd'])} ⛔ có luật trong IX.ALR hiện hành ⇒ ⛔ ký bật được")
            continue
        x = max(cu, key=lambda y: y.tu_ky)
        if x.driver is None:
            ly.append(f"luật {i}: hd={r['hd']!r} ({x.phuong_phap}) ⛔ có driver ⇒ ⛔ chia (Q3)")
            continue
        dem["bat" if r["bat"] else "tat"][x.phuong_phap] += 1
        moi.append({"hd": r["hd"], "tu_ky": r["tu_ky"], "nhan_mm": x.nhan_mm, "bat": r["bat"],
                    "ngoai_le": list(x.ngoai_le_cdt1), COT_KY: dict(tep["ky"]) if isinstance(tep["ky"], Mapping)
                    else tep["ky"]})
    md = tep["mong_dem"] if isinstance(tep["mong_dem"], Mapping) else {}
    for k in ("bat", "tat"):
        if dict(dem[k]) != dict(md.get(k) or {}):
            ly.append(f"mong_dem.{k}: đo {dict(sorted(dem[k].items()))} ≠ mong {md.get(k)}")
    if ly:
        raise LoiLuatPB(ly)
    kiem(moi, nguon="(tệp ký)")                    # chữ ký · kỳ · trùng — CHÍNH `kiem`
    return moi
