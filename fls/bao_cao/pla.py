"""`SO.PLA1` *(PM only)* · `SO.PLA3` *(HR only · PM + HR)* — Daily + Y/H/Q/M *(ISP 3.1.2 · Step 39 · H8 ·
`WO-277` · AP v3.1.2 §3.3.1 PD 414–419 · cổng WP-C3d)*.

⭐ **Hành vi AS-IS mà engine tái lập** *(công thức SA đọc FORMULA 22/11 — `BG-262` §5 · `BG-282` §1 · `BG-278`)*:
  · ô LÁ PLA1 khối `GROUP` = `SUMIFS(GL!BR, GL!DE, ngày, GL!V, nhãn) − SUMIFS(GL!BS, …)`; khối LE thêm
    `GL!P = mã LE`; khối CDT thêm `GL!AD = nhãn khối` *(cột `AD` CHƯA có trong ảnh đầu vào ⇒ khối CDT
    ⛔ ở engine này — nơi gọi khai `chua_co_dau_vao`)*. ⇒ đúng phép `cfa1_daily` *(H5)* trên trục ngày
    GHI NHẬN thay ngày chứng từ — **dùng lại**, ⛔ chép.
  · Ngày ghi nhận `GL!DE = DATE(left(AH,4), right(AH,2), 1)` *(`AH` = yyyymm "Thời điểm bắt đầu sử dụng
    dịch vụ")* ⇒ D4 A *(dồn ngày 1 tháng PL start)* — engine gọi **`ky.ngay_ghi_nhan` của C6**, `DE` chỉ để
    đối chiếu. `AH` rỗng ⇒ `DE = #NUM!` ⇒ SUMIFS ⛔ khớp cột nào; `AH` tháng ∉ 1…12 / serial ⇒ `DATE` TRÀN
    ra ngày ngoài lưới ⇒ SUMIFS cũng bỏ. Engine ⛔ tràn tháng: ném `LoiNgayPL` CÓ TÊN *(`AH_RONG` · `AH_LA`)*
    ⇒ nơi gọi đếm, ⛔ hoá 0 im lặng.
  · HR: `BM = if(BL=2024 và BK∈{11,12}, DATE(BL,BK,1), DATE(2025,BK,1))` *(`BK` = tháng PL start, `BL` =
    năm gõ tay)* — luật năm AS-IS, giữ để parity *(`ngay_pl_hr`)*.
  · ô `tong` = `=sum(con)` theo cây IX.HD *(đo: 10 mã, khớp cây ATL)*.
  · ô `kpi` = công thức CHÉO hàng **của từng tab** *(`CONG_THUC_PM` cho 414/415/418/419 · `CONG_THUC_HR`
    cho 416/417 — dấu HR NGƯỢC)*; `NPC = sum(G67:67)` ⇒ **Σ HẬU TỐ** của `NP` dọc trục cột; ở tab HR
    11 mã KPI CHỈ có công thức ở cột đầu `G` *(cột khác rỗng ⇒ 0)*.
  · ô `trong` *(AR · CP1.1 (PL2) · CP1.2 · CP2 · CP3 · CFO · PL5)* ⛔ công thức ⇒ 0.
  · tab HR khối `GROUP`: `TAC` · `CIT` ⛔ công thức *(`DT7-R1-04`)* ⇒ 0 dù có dòng gán nhãn.
  · PM + HR *(418)*: ô lá = `PLA1!G + HR!G` ⇒ engine cộng **THEO KHOÁ** `(khối, mã HD, ngày)` *(⛔ theo vị
    trí)*; `tong`/`kpi` tính LẠI bằng công thức của CHÍNH tab 418 *(⇒ KPI PM+HR ≠ KPI PM + KPI HR)*.
  · Y/H/Q/M *(415/417/419)*: ô lá = `SUMIFS(Daily!hàng, Daily!$1:$1, kỳ)` ⇒ `cuon_ky` *(H6)* trên lưới lá
    Daily; `tong`/`kpi` tính LẠI trong không gian kỳ *(NPC hậu tố dọc cột kỳ; HR KPI chỉ cột kỳ đầu)*.

⛔ Engine ⛔ quy đổi tiền *(BR/BS do `tinh_gl` — H1/H4 — ở nơi gọi)* · ⛔ đọc gì ngoài tham số.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, Iterable, Mapping, Sequence

from fls.bao_cao.cfa import KHOI_TONG, DongCFA, cfa1_daily, cuon_ky
from fls.cau_hinh import ky
from fls.cau_hinh.hd import CayHD

_KHONG = Decimal(0)
_GOC_SERIAL = date(1899, 12, 30)

AH_RONG = "AH_RONG"     # `AH` rỗng ⇒ AS-IS `DE = #NUM!`
AH_LA = "AH_LA"         # `AH` ⛔ dạng yyyymm hợp lệ *(tháng ∉ 1…12, serial, chữ)* ⇒ AS-IS `DE` tràn ngoài lưới


class LoiNgayPL(ValueError):
    """Ngày PL ⛔ dựng được — lỗi CÓ TÊN `ma` ∈ {`AH_RONG`, `AH_LA`}."""

    def __init__(self, ma: str, thong_bao: str) -> None:
        super().__init__(f"{ma}: {thong_bao}")
        self.ma = ma


def _serial(d: date) -> int:
    return (d - _GOC_SERIAL).days


def ngay_pl(luat: Any, pl_start: date, pl_end: date) -> int:
    """Serial ngày ghi nhận của một dòng PL — **chỉ** qua `ky.ngay_ghi_nhan` *(C6, D4)*."""
    return _serial(ky.ngay_ghi_nhan(luat, pl_start, pl_end))


def ngay_pl_tu_yyyymm(luat: Any, ah: Any) -> int:
    """`AH` *(yyyymm của PL start)* → serial ngày ghi nhận. Rỗng ⇒ `AH_RONG`; ⛔ hợp lệ ⇒ `AH_LA`."""
    if ah is None or (isinstance(ah, str) and not ah.strip()):
        raise LoiNgayPL(AH_RONG, "AH rỗng (AS-IS DE = #NUM!)")
    try:
        v = int(Decimal(str(ah).strip()))
        if Decimal(str(ah).strip()) != v:
            raise ValueError
    except Exception:  # noqa: BLE001 — mọi dạng lạ cùng một tên
        raise LoiNgayPL(AH_LA, "AH ⛔ phải số nguyên yyyymm") from None
    nam, thang = divmod(v, 100)
    # ⚠ năm 2000…2099: đo 22/11 (`DT7B-R1-01`) 8 hàng AH lạ = serial (45962) · tháng 27/14 · `yymmdd`
    #   (262601 · 260601 · 252512 · 260603 ⇒ "năm" 2525…2626) — mọi dạng ấy ⇒ một tên, ⛔ tràn tháng.
    if not (2000 <= nam <= 2099 and 1 <= thang <= 12):
        raise LoiNgayPL(AH_LA, f"AH {v} ⛔ phải yyyymm (năm 2000…2099, tháng 1…12)")
    d = date(nam, thang, 1)
    return ngay_pl(luat, d, d)


def ngay_pl_hr(luat: Any, bk: Any, bl: Any) -> int:
    """HR *(tab `…For PL Report`)*: năm theo luật AS-IS của `BM` — 2024 chỉ khi `BL=2024` và tháng 11·12,
    còn lại 2025 *(gõ cứng ở công thức SỔ, ⛔ ở mã luật D4)*; rồi D4 qua C6."""
    try:
        thang, nam_bl = int(Decimal(str(bk))), int(Decimal(str(bl)))
    except Exception:  # noqa: BLE001
        raise LoiNgayPL(AH_LA, "BK/BL ⛔ phải số") from None
    if not 1 <= thang <= 12:
        raise LoiNgayPL(AH_LA, f"BK {thang} ⛔ phải tháng 1…12")
    nam = nam_bl if (nam_bl == 2024 and thang in (11, 12)) else 2025
    d = date(nam, thang, 1)
    return ngay_pl(luat, d, d)


# ── công thức từng tab *(đo FORMULA cột G khối GROUP, 22/11; đồng dạng mọi khối đo được)* ──────────
# Mỗi KPI = Σ dấu × mã; `NPC` riêng *(Σ hậu tố của `NP`)*. Hàng sheet → mã: 8 GI · 9 OPC · 12 OMC · 13 MC ·
# 14 OTMC · 17 PS · 18 API · 19 SC · 20 LC · 21 DC · 22 CSO · 23 GAC · 34 CDC · 43 ITE · 44 CFI · 45 LMN ·
# 46 OMN · 48 NIS · 49 INT · 50 PIT · 51 COM · 53 DEP · 55 NB · 57 TAC · 58 CIT · 64 EBITDA … 87 PL8.
_COO = ("OPC", "GAC", "ITE", "NIS", "INT", "PIT", "COM", "DEP", "NB", "TAC", "CIT")


def _kpi(d: int) -> dict[str, tuple[tuple[int, str], ...]]:
    """`d` = dấu của số hạng sau số hạng đầu ở 11 KPI "lợi nhuận" *(PM +1 · HR −1)*."""
    return {
        "EBITDA": ((1, "GI"), (d, "OPC"), (d, "GAC")),
        "EBIT": ((1, "EBITDA"), (d, "CDC")),
        "EBT": ((1, "EBIT"), (d, "ITE")),
        "NP": ((1, "EBT"), (d, "CIT")),
        "NCF": ((1, "NCFO"), (1, "NCFI"), (1, "NCFF")),
        "CRO": ((1, "GI"),),
        "COO": tuple((1, m) for m in _COO),
        "COI": ((1, "CDC"),),
        "CRF": ((1, "CFI"), (1, "LMN")),
        "COF": ((1, "OMN"),),
        "PL2": ((1, "GI"), (d, "OMC")),
        "PL3": ((1, "PL2"), (d, "API"), (d, "SC"), (d, "LC")),
        "PL4": ((1, "PL3"), (d, "PS")),
        "PL6": ((1, "PL4"), (d, "MC"), (d, "OTMC"), (d, "DC"), (d, "CSO")),
        "PL7": ((1, "PL6"), (d, "GAC"), (d, "CDC"), (d, "ITE")),
        "PL8": ((1, "PL7"), (d, "TAC")),        # ⚠ `=G86+G57`: hàng 57 = TAC *(⛔ CIT — chữ "Tax (CIT)")*
    }


_KPI_LOI_NHUAN = ("EBITDA", "EBIT", "EBT", "NP", "NPC", "PL2", "PL3", "PL4", "PL6", "PL7", "PL8")
TRONG = frozenset({"AR", "CP1.1 (PL2)", "CP1.2", "CP2", "CP3", "CFO", "PL5"})


@dataclass(frozen=True)
class CongThuc:
    """Bộ công thức của MỘT tab. `chi_cot_dau`: KPI chỉ có công thức ở cột đầu *(cột khác ⇒ 0)*;
    `khong_cong_thuc`: (khối → mã lá ⛔ công thức ⇒ 0)."""
    ten: str
    kpi: Mapping[str, tuple[tuple[int, str], ...]]
    npc: tuple[str, str] = ("NPC", "NP")
    chi_cot_dau: frozenset[str] = frozenset()
    trong: frozenset[str] = TRONG
    khong_cong_thuc: Mapping[str, frozenset[str]] = field(default_factory=dict)
    #: bộ này CHỈ áp cho các khối ấy; khối khác dùng `khoi_khac` *(416: chỉ GROUP dấu HR · khối LE/CDT/dư dấu PM)*
    chi_khoi: frozenset[str] | None = None
    khoi_khac: "CongThuc | None" = None

    def cua_khoi(self, kh: str) -> "CongThuc":
        return self if self.chi_khoi is None or kh in self.chi_khoi or self.khoi_khac is None else self.khoi_khac

    @property
    def ma_kpi(self) -> frozenset[str]:
        return frozenset(self.kpi) | {self.npc[0]}


CONG_THUC_PM = CongThuc("PM", _kpi(1))
#: 416/417: dấu HR NGƯỢC + 11 KPI chỉ cột đầu + TAC/CIT ⛔ công thức — CHỈ khối GROUP *(đo FORMULA 22/11: khối LE ·
#: CDT · dư của 416 dùng đúng khuôn KPI của 414, mọi cột)*.
CONG_THUC_HR = CongThuc("HR", _kpi(-1), chi_cot_dau=frozenset(_KPI_LOI_NHUAN),
                        khong_cong_thuc={KHOI_TONG: frozenset({"TAC", "CIT"})},
                        chi_khoi=frozenset({KHOI_TONG}), khoi_khac=CONG_THUC_PM)


def loai_ma(cay: CayHD, ct: CongThuc) -> dict[str, str]:
    """`la` · `tong` · `kpi` · `trong` cho mỗi nút cây — KPI/trong theo công thức tab, `tong` = nút có con."""
    co_con = {n.cha for n in cay.nut if n.cha is not None}
    out: dict[str, str] = {}
    for n in cay.nut:
        out[n.ma] = ("kpi" if n.ma in ct.ma_kpi else "trong" if n.ma in ct.trong
                     else "tong" if n.ma in co_con else "la")
    return out


@dataclass
class KetQuaPLA:
    #: (khối, mã HD, cột) → mUSD — lưới ĐỦ: mọi khối × mọi nút × mọi cột của `cot`.
    o: dict[tuple[str, str, Any], Decimal]
    cot: list
    khoi: tuple[str, ...]
    loai: dict[str, str]
    #: lá trước khi tính tong/kpi — để cộng PM+HR theo khoá và cuộn kỳ
    la: dict[tuple[str, str, Any], Decimal]
    dong: Any = None                       # `KetQuaCFA1` *(đếm dòng ngoài cây / nhãn cha / ngoài trục)*
    ky_khong_ngay: tuple[str, ...] = ()


def danh_gia(la: Mapping[tuple[str, str, Any], Decimal], cay: CayHD, cot: Sequence[Any],
             khoi: Sequence[str], ct: CongThuc) -> dict[tuple[str, str, Any], Decimal]:
    """Lưới lá → lưới đủ theo công thức tab: `tong` = Σ con · `kpi` = công thức · `NPC` hậu tố · `trong` 0."""
    loai = loai_ma(cay, ct)
    con: dict[str, list[str]] = {n.ma: [] for n in cay.nut}
    for n in cay.nut:
        if n.cha is not None:
            con[n.cha].append(n.ma)
    thieu = [m for f in ct.kpi.values() for _, m in f if m not in loai] + \
            [m for m in ct.npc if m not in loai]
    if thieu:
        raise KeyError(f"công thức {ct.ten} nhắc mã ⛔ có trong cây: {sorted(set(thieu))}")
    dau = cot[0] if cot else None
    o: dict[tuple[str, str, Any], Decimal] = {}
    ct0 = ct
    for kh in khoi:
        ct = ct0.cua_khoi(kh)
        kcc = ct.khong_cong_thuc.get(kh, frozenset())
        for t in cot:
            nho: dict[str, Decimal] = {}

            def tinh(m: str, dang: frozenset[str] = frozenset()) -> Decimal:
                if m in nho:
                    return nho[m]
                if m in dang:
                    raise ValueError(f"công thức {ct.ten} vòng ở {m}")
                lo = loai[m]
                if lo == "trong" or m == ct.npc[0]:
                    v = _KHONG                                  # NPC tính sau (hậu tố)
                elif lo == "kpi":
                    if m in ct.chi_cot_dau and t != dau:
                        v = _KHONG
                    else:
                        v = sum((s * tinh(x, dang | {m}) for s, x in ct.kpi[m]), _KHONG)
                elif lo == "tong":
                    v = sum((tinh(c, dang | {m}) for c in con[m]), _KHONG)
                else:
                    v = _KHONG if m in kcc else la.get((kh, m, t), _KHONG)
                nho[m] = v
                return v

            for n in cay.nut:
                o[(kh, n.ma, t)] = tinh(n.ma)
        # NPC = sum(G67:67): Σ hậu tố của NP dọc trục cột *(HR: chỉ cột đầu)*
        npc, np_ = ct.npc
        if npc in loai:
            chay = _KHONG
            for t in reversed(list(cot)):
                chay += o[(kh, np_, t)]
                o[(kh, npc, t)] = chay if (npc not in ct.chi_cot_dau or t == dau) else _KHONG
            # mã cha của NPC *(nếu cây đặt NPC dưới một tong)* phải tính lại — cây ATL: NPC là gốc
    return o


def _chi_la(o: Mapping[tuple[str, str, Any], Decimal], loai: Mapping[str, str]
            ) -> dict[tuple[str, str, Any], Decimal]:
    return {k: (v if loai[k[1]] == "la" else _KHONG) for k, v in o.items()}


def pla_daily(dong: Iterable[DongCFA], cay: CayHD, ngay: Sequence[int], khoi: Sequence[str],
              ct: CongThuc, alias: Mapping[str, str] | None = None,
              cdt: tuple[Iterable[DongCFA], Sequence[str], str] | None = None) -> KetQuaPLA:
    """Daily: lá = `cfa1_daily` *(H5 — Σ BR−BS theo (khối, nhãn V, ngày GHI NHẬN))*; tong/kpi theo `ct`.

    `dong[i].ngay` = serial ngày ghi nhận *(`ngay_pl_tu_yyyymm` / `ngay_pl_hr`)*, ⛔ ngày chứng từ; `dong[i].le` =
    khoá khối LE *(GL/HR cột `P`)*. `cdt` = (cùng các dòng nhưng `le` = mã khối CDT *(GL `AD` · HR `BP`, nơi gọi
    tra nhãn)*, các khối CDT, khối dư) ⇒ khối dư = GROUP − Σ khối CDT *(công thức `SHQ2`)*.
    """
    kq = cfa1_daily(dong, cay, ngay, khoi, alias)
    loai = loai_ma(cay, ct)
    la = _chi_la(kq.o, loai)
    tat = tuple(khoi)
    if cdt is not None:
        dong_cdt, khoi_cdt, khoi_du = cdt
        kq2 = cfa1_daily(dong_cdt, cay, ngay, (KHOI_TONG,) + tuple(khoi_cdt), alias)
        la2 = _chi_la(kq2.o, loai)
        for k, v in la2.items():
            if k[0] != KHOI_TONG:
                la[k] = v
        # khối DƯ *(SHQ2)*: `=G{GROUP} − SUMIFS(G{khối CDT}…)` — Σ lá GROUP trừ Σ lá 6 khối CDT
        for n in cay.nut:
            for t in ngay:
                la[(khoi_du, n.ma, t)] = la[(KHOI_TONG, n.ma, t)] - sum(
                    (la[(k, n.ma, t)] for k in khoi_cdt), _KHONG)
        tat = tat + tuple(khoi_cdt) + (khoi_du,)
    return KetQuaPLA(o=danh_gia(la, cay, list(ngay), tat, ct), cot=list(ngay), khoi=tat,
                     loai=loai, la=la, dong=kq)


def cong_theo_khoa(a: Mapping[tuple, Decimal], b: Mapping[tuple, Decimal],
                   khoa: Iterable[tuple]) -> dict[tuple, Decimal]:
    """PM + HR **theo KHOÁ** `(khối, mã HD, cột)`: mỗi khoá tra CẢ HAI lưới *(thiếu ⇒ `KeyError`, ⛔ hoá 0
    — lưới đủ nên thiếu là lệch trục)*. ⛔ zip theo vị trí."""
    return {k: a[k] + b[k] for k in khoa}


def pla_pm_hr_daily(pm: KetQuaPLA, hr: KetQuaPLA, cay: CayHD, khoi: Sequence[str],
                    ct: CongThuc = CONG_THUC_PM) -> KetQuaPLA:
    """418: lá = PLA1 + HR theo khoá trên `khoi` *(khối đo được ở CẢ HAI)*; tong/kpi theo công thức 418."""
    if list(pm.cot) != list(hr.cot):
        raise ValueError("trục PM ≠ trục HR ⇒ ⛔ cộng được (Đ5)")
    loai = loai_ma(cay, ct)
    khoa = [(kh, n.ma, t) for kh in khoi for n in cay.nut for t in pm.cot]
    la = {k: (v if loai[k[1]] == "la" else _KHONG) for k, v in cong_theo_khoa(pm.la, hr.la, khoa).items()}
    return KetQuaPLA(o=danh_gia(la, cay, pm.cot, khoi, ct), cot=list(pm.cot), khoi=tuple(khoi),
                     loai=loai, la=la)


def pla_yhqm(daily: KetQuaPLA, cay: CayHD, khoi: Sequence[str], ct: CongThuc) -> KetQuaPLA:
    """Y/H/Q/M: cuộn LÁ Daily theo kỳ *(`cuon_ky` — H6)*; tong/kpi tính lại trong không gian kỳ."""
    cu = cuon_ky(daily.la, cay, daily.cot, khoi)
    loai = loai_ma(cay, ct)
    la = _chi_la(cu.o, loai)
    return KetQuaPLA(o=danh_gia(la, cay, cu.ky, khoi, ct), cot=list(cu.ky), khoi=tuple(khoi),
                     loai=loai, la=la, ky_khong_ngay=cu.ky_khong_ngay)
