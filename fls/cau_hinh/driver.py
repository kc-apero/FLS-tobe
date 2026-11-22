"""`IX.DRV` — **driver phân bổ theo (loại, CDT1, tháng)** *(AP v3.1.2 §3.2.4 · ISP 3.1.2 · Step 29
· `C10` · `WO-295`)*.

Làn **BE-CF**, khuôn `luat_pb.py`: lõi kiểm THUẦN, bản config được TRUYỀN VÀO *(⛔ biết kho —
`.importlinter` hợp đồng 10)*; đọc/ghi kho là `fls/repo/cau_hinh_repo.py`.

⭐ **Số đo** *(ảnh DT10 `ix_drv.json` — mỗi số một nhãn, Đ4)*: **21** dòng = 3 loại số
   *(`GI_PE` · `GI_PM` · `NOEM`)* × 7 CDT1 × 12 tháng 2025 = 252 ô; **238** ô CÓ SỐ *(252 − 14 ô
   `GI` tháng `202501` — MID3 ⛔ có `TOTAL 202501`)*; **146** ô THIẾU, mỗi ô có tên ở phụ
   `o_thieu`: `NB_LE` 96 *(NB khoá theo LE `From × To`, ⛔ theo CDT1 — phụ `nb_le`, 304 dòng)* ·
   `CMN` 36 *(rơi vào phần dư SHQ2)* · `GI 202501` 14. **Chỉ 2025** — ⛔ driver 2026 ở nguồn.
   Σ 7 CDT1 = 1 ± 1e-9 ở **34** tổng *(GI_PE 11 + GI_PM 11 + NOEM 12)*.

⛔ **Ô thiếu ⇒ `DRV_THIEU` CÓ TÊN** *(loại · CDT1 · tháng · lý do)* — ⛔ trả `0` *(một `0` là một
   *driver thật bằng 0*)*, ⛔ rơi về ô cứng H1000 `A4289:Q4300` *(AP §3.2.4: NOEM headcount ⛔ trỏ
   ô cứng trong mã)*. ⛔ Đếm `mong` hai chiều *(Đ5)*: mọi ô `null` PHẢI có dòng `o_thieu` và mọi dòng
   `o_thieu` PHẢI trỏ ô ⛔ có số — thiếu HAY thừa đều ⇒ `LoiDRV`.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

BANG = "IX.DRV"

LOAI_SO: tuple[str, ...] = ("GI_PE", "GI_PM", "NOEM")      # loại có lưới CDT1
LOAI_NB = "NB_LE"                                           # NB khoá theo LE ⇒ ⛔ lưới CDT1
LOAI: tuple[str, ...] = LOAI_SO + (LOAI_NB,)
CDT1_LUOI: tuple[str, ...] = ("CVL", "COR", "CSM", "CAH", "ASA", "SHQ1", "SHQ2")   # 7 CDT1
CDT1_BIET: frozenset[str] = frozenset(CDT1_LUOI) | {"CMN"}  # + CMN: gộp SHQ1, ⛔ có lưới riêng
THANG = tuple(f"m{i:02d}" for i in range(1, 13))
MONG_O_SO = 238          # ô CÓ SỐ (21 dòng × 12 tháng − 14 ô GI 202501)
MONG_O_THIEU = 146
MONG_TONG = 34           # tổng Σ7 CDT1 kiểm được
TOL = 1e-9

DRV_HONG = "DRV_HONG"
DRV_THIEU = "DRV_THIEU"
DRV_LA = "DRV_LA"
KY_HONG = "KY_HONG"

_P_THIEU = "@thieu:"
_P_NB = "@nb_le:"
_COT_SO = ("driver", "cdt1", "nam", "ngoai") + THANG
_COT_NB = ("from", "to", "loai") + THANG


class LoiDRV(ValueError):
    """Lỗi `IX.DRV` **có tên**: `ma` ∈ {`DRV_HONG`, `DRV_THIEU`, `DRV_LA`, `KY_HONG`}. `ly_do` =
    **mọi** lý do, ⛔ chỉ lý do đầu."""

    def __init__(self, ly_do: Iterable[str] | str, ma: str = DRV_HONG) -> None:
        self.ly_do = (ly_do,) if isinstance(ly_do, str) else tuple(ly_do)
        self.ma = ma
        super().__init__(f"{ma}: ⛔ {BANG} — {len(self.ly_do)} lỗi: " + " · ".join(self.ly_do))


class DrvThieu(LoiDRV):
    """Ô ⛔ có driver — mang `loai` · `cdt1` · `thang` · `ly` *(⛔ `0`, ⛔ ô cứng H1000)*."""

    def __init__(self, loai: str, cdt1: str, thang: int, ly: str) -> None:
        self.loai, self.cdt1, self.thang, self.ly = loai, cdt1, thang, ly
        super().__init__(f"loại={loai} · CDT1={cdt1} · tháng={thang} ⛔ có driver — {ly}",
                         DRV_THIEU)


@dataclass(frozen=True)
class BangDRV:
    nguon: str
    luoi: Mapping[tuple[str, str], Mapping[str, Any]]       # (loai, cdt1) → {nam, ngoai, m01..m12}
    thieu: Mapping[tuple[str, str, int], str]               # (loai, cdt1, yyyymm) → lý do
    nb_le: Mapping[tuple[str, str], Mapping[str, Any]]      # (from, to) → {loai, m01..m12}

    def so_o_so(self) -> int:
        return sum(1 for r in self.luoi.values() for m in THANG if r[m] is not None)

    def driver_cua(self, loai: str, cdt1: str, thang: Any) -> float:
        """Driver của `(loai, cdt1)` ở `thang` *(`yyyymm`)*. Ô ⛔ có số ⇒ `DrvThieu` CÓ TÊN."""
        t = _thang(thang)
        if loai not in LOAI:
            raise LoiDRV(f"loại={loai!r} ⛔ thuộc {list(LOAI)}", DRV_LA)
        if cdt1 not in CDT1_BIET:
            raise LoiDRV(f"CDT1={cdt1!r} ⛔ thuộc {sorted(CDT1_BIET)}", DRV_LA)
        ly = self.thieu.get((loai, cdt1, t))
        if ly is not None:
            raise DrvThieu(loai, cdt1, t, ly)
        r = self.luoi.get((loai, cdt1))
        if r is not None and t // 100 == int(r["nam"]):
            v = r[THANG[t % 100 - 1]]
            if v is not None:
                return v
        # ⛔ ô ngoài lưới 2025 *(driver 2026 ⛔ có ở nguồn)* — có tên, ⛔ 0
        raise DrvThieu(loai, cdt1, t, f"nguồn ⛔ có driver năm {t // 100} "
                       f"(ảnh DT10 chỉ có 2025)")

    def nb_le_cua(self, tu: str, den: str, thang: Any) -> float:
        """NB theo LE *(`From × To`)* — đường đọc RIÊNG, ⛔ giả làm lưới CDT1."""
        t = _thang(thang)
        r = self.nb_le.get((tu, den))
        if r is None:
            raise LoiDRV(f"NB_LE {tu!r}→{den!r} ⛔ có trong `nb_le`", DRV_LA)
        if t // 100 != 2025:
            raise DrvThieu(LOAI_NB, f"{tu}→{den}", t, f"nguồn ⛔ có NB năm {t // 100} (chỉ 2025)")
        return r[THANG[t % 100 - 1]]


def _thang(t: Any) -> int:
    if isinstance(t, bool) or not isinstance(t, int) or not 190001 <= t <= 299912 \
            or not 1 <= t % 100 <= 12:
        raise LoiDRV(f"thang={t!r} ⛔ yyyymm (190001…299912, tháng 1…12)", KY_HONG)
    return t


def _mot(s: Any) -> str:
    return " ".join(repr(s).split())


def khoa_so(loai: str, cdt1: str) -> str:
    return f"{loai}|{cdt1}"


def khoa_thieu(loai: str, cdt1: str, thang: int) -> str:
    return f"{_P_THIEU}{loai}|{cdt1}|{thang}"


def khoa_nb(tu: str, den: str) -> str:
    return f"{_P_NB}{tu}|{den}"


def _so(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) \
        and math.isfinite(v) and -TOL <= v <= 1 + TOL     # ảnh có nhiễu -1.1e-15 (phần dư SHQ2)


def _huu_han(v: Any) -> bool:
    """NB theo LE có số ÂM thật (min −0,2567 ở 15/3.648 ô) ⇒ chỉ đòi số hữu hạn."""
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def kiem(dong: Iterable[Mapping[str, Any]], *, nguon: str) -> BangDRV:
    """Kiểm **thuần**. Mỗi dòng mang `khoa` *(đọc từ kho)*: `loai|cdt1` = ô số · `@thieu:…` = lý do
    ô thiếu `{ly_do}` · `@nb_le:from|to` = NB theo LE. Hỏng ⇒ `LoiDRV` *(mọi lý do)*."""
    ly: list[str] = []
    luoi: dict[tuple[str, str], dict[str, Any]] = {}
    thieu: dict[tuple[str, str, int], str] = {}
    nb: dict[tuple[str, str], dict[str, Any]] = {}
    for i, r in enumerate(dong, start=1):
        if not isinstance(r, Mapping) or not isinstance(r.get("khoa"), str):
            ly.append(f"dòng {i}: ⛔ phải một đối tượng có `khoa`")
            continue
        k, n0 = r["khoa"], len(ly)
        if k.startswith(_P_THIEU):
            loai, cdt1, th = (k[len(_P_THIEU):].split("|") + ["", "", ""])[:3]
            bo = sorted(c for c in r if c not in ("khoa", "ly_do"))
            if bo or not isinstance(r.get("ly_do"), str) or not r["ly_do"].strip():
                ly.append(f"dòng {i} ({k}): cần đúng `ly_do` chuỗi ⛔ rỗng (lạ: {bo})")
            if not th.isdigit() or loai not in LOAI or cdt1 not in CDT1_BIET \
                    or not 1 <= int(th) % 100 <= 12:
                ly.append(f"dòng {i}: khoá thiếu {k!r} hỏng")
            if len(ly) == n0:
                thieu[(loai, cdt1, int(th))] = r["ly_do"]
        elif k.startswith(_P_NB):
            tu, den = (k[len(_P_NB):].split("|") + ["", ""])[:2]
            la = sorted(c for c in r if c not in _COT_NB and c != "khoa")
            tha = sorted(c for c in _COT_NB if c not in r)
            if la or tha:
                ly.append(f"dòng {i} ({k}): cột lạ {la} · thiếu {tha}")
                continue
            if (r["from"], r["to"]) != (tu, den) or not _so_het(r):
                ly.append(f"dòng {i} ({k}): khoá ≠ (from,to) hay ô ⛔ số hữu hạn")
                continue
            nb[(tu, den)] = {c: r[c] for c in ("loai",) + THANG}
        else:
            la = sorted(c for c in r if c not in _COT_SO and c != "khoa")
            tha = sorted(c for c in _COT_SO if c not in r)
            if la or tha:
                ly.append(f"dòng {i} ({k}): cột lạ {la} · thiếu {tha}")
                continue
            loai, cdt1 = r["driver"], r["cdt1"]
            if loai not in LOAI_SO or cdt1 not in CDT1_LUOI:
                ly.append(f"dòng {i}: driver={_mot(loai)} CDT1={_mot(cdt1)} ⛔ thuộc "
                          f"{list(LOAI_SO)} × {list(CDT1_LUOI)}")
            elif k != khoa_so(loai, cdt1):
                ly.append(f"dòng {i}: khoá {k!r} ≠ {khoa_so(loai, cdt1)!r}")
            if not _so(r["ngoai"]) or not isinstance(r["nam"], int) or isinstance(r["nam"], bool):
                ly.append(f"dòng {i} ({k}): nam/ngoai ⛔ hợp lệ")
            bad = [m for m in THANG if r[m] is not None and not _so(r[m])]
            if bad:
                ly.append(f"dòng {i} ({k}): ô {bad} ⛔ số trong [0,1]")
            if len(ly) == n0:
                luoi[(loai, cdt1)] = {c: r[c] for c in ("nam", "ngoai") + THANG}
    if not luoi and not ly:
        ly.append("0 dòng ⇒ ⛔ có bảng để kiểm")
    if not ly:
        # ⛔ Đ5 hai chiều: mỗi ô null ⇔ có `o_thieu`; ô có số ⛔ được có `o_thieu`.
        for (loai, cdt1), r in sorted(luoi.items()):
            for m in THANG:
                t = int(r["nam"]) * 100 + int(m[1:])
                if (r[m] is None) != ((loai, cdt1, t) in thieu):
                    ly.append(f"({loai},{cdt1},{t}): ô "
                              f"{'null mà ⛔ có' if r[m] is None else 'CÓ SỐ mà lại có'} dòng o_thieu")
        for (loai, cdt1, t) in sorted(thieu):
            if (loai, cdt1) in luoi and not any(
                    int(r["nam"]) == t // 100 for r in [luoi[(loai, cdt1)]]):
                ly.append(f"o_thieu ({loai},{cdt1},{t}) ngoài năm của lưới")
        # ⛔ Σ 7 CDT1 = 1 ở tháng mà cả 7 có số
        for loai in LOAI_SO:
            for m in THANG:
                v = [luoi[(loai, c)][m] for c in CDT1_LUOI if (loai, c) in luoi]
                if len(v) == 7 and all(x is not None for x in v) and abs(sum(v) - 1) > TOL:
                    ly.append(f"{loai} {m}: Σ7 CDT1 = {sum(v)!r} ≠ 1 (±{TOL:g})")
    if ly:
        raise LoiDRV(ly)
    return BangDRV(nguon=nguon, luoi=luoi, thieu=thieu, nb_le=nb)


def _so_het(r: Mapping[str, Any]) -> bool:
    return isinstance(r.get("loai"), str) and all(_huu_han(r[m]) for m in THANG)


def dung_tu_anh(anh: Mapping[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Ảnh DT10 `ix_drv.json` ⇒ cặp `(khoa, giá trị)` của kho. Ô là chuỗi `{chu}` hay số ⇒ số.
    Số ô ≠ `MONG_O_SO`/`MONG_O_THIEU` ⇒ `LoiDRV` *(thiếu HAY thừa — Đ5)*."""
    def chu(o: Any) -> Any:
        return o.get("chu") if isinstance(o, Mapping) else o

    def num(o: Any) -> Any:
        o = chu(o)
        return None if o is None else float(o)

    cap: list[tuple[str, dict[str, Any]]] = []
    for r in anh["dong"]:
        loai, cdt1 = chu(r["driver"]), chu(r["cdt1"])
        cap.append((khoa_so(loai, cdt1), {
            "driver": loai, "cdt1": cdt1, "nam": int(chu(r["nam"])), "ngoai": num(r["ngoai"]),
            **{m: num(r[m]) for m in THANG}}))
    for r in anh["phu"]["o_thieu"]["dong"]:
        loai, cdt1, th = chu(r["driver"]), chu(r["cdt1"]), int(chu(r["thang"]))
        cap.append((khoa_thieu(loai, cdt1, th), {"ly_do": chu(r["ly_do"])}))
    for r in anh["phu"]["nb_le"]["dong"]:
        tu, den = chu(r["from"]), chu(r["to"])
        cap.append((khoa_nb(tu, den), {"from": tu, "to": den, "loai": chu(r["loai"]),
                                       **{m: num(r[m]) for m in THANG}}))
    so = sum(1 for k, v in cap if "|" in k and not k.startswith("@") for m in THANG
             if v[m] is not None)
    th = sum(1 for k, _ in cap if k.startswith(_P_THIEU))
    if (so, th) != (MONG_O_SO, MONG_O_THIEU):
        raise LoiDRV(f"ảnh có {so} ô số / {th} ô thiếu, mong {MONG_O_SO} / {MONG_O_THIEU} "
                     f"(thiếu HAY thừa)")
    return cap


def driver_cua(bang: BangDRV, loai: str, cdt1: str, thang: Any) -> float:
    """Hàm tự do — `bang` TRUYỀN VÀO. Đọc từ KHO: `cau_hinh_repo.driver_cua(conn, …)`."""
    return bang.driver_cua(loai, cdt1, thang)
