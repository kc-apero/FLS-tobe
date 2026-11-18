"""`SO.CFA1 Daily` — Σ theo (khối LE, HD, ngày) trên cây IX.HD *(ISP 3.1.2 · Step 16 · H5 · AP v3.1.2
§3.3.1 PD 409 · §3.2.4 "cây HD theo vị trí dòng, cha = SUM con" · WP-C3)*.

⭐ **Hành vi AS-IS mà engine tái lập** *(công thức SA của `Report I CFA1 Daily`, orchestrator đọc 18/11)*:
  · ô LÁ khối `GROUP` = `SUMIFS(BR, A, ngày, V, nhãn) − SUMIFS(BS, …)` ⇒ Σ mUSD Nợ − Σ mUSD Có của
    MỌI dòng sổ có ngày = cột và nhãn HD Final = nhãn hàng *(⛔ lọc LE)*;
  · khối LE = cùng phép + `P = mã LE`;
  · ô CHA = `=sum(con)` ⇒ engine cộng con THEO CÂY *(⛔ cộng dòng sổ gán thẳng vào mã cha — AS-IS
    ⛔ có SUMIFS ở hàng cha, dòng ấy RƠI; engine ĐẾM nó ở `dong_nhan_cha`, ⛔ rơi im lặng)*.

⛔ **Engine ⛔ quy đổi tiền.** `musd_no`/`musd_co` là BR/BS do `tinh_gl` *(H1/H4)* tính từ E/F + tỷ
giá — nơi gọi *(`tools/do_hd2.py --goi WP-C3a`)* nối hai bước. Một nghĩa của tiền ⇒ một chỗ.

⛔ **Nhãn so KHÔNG phân biệt hoa thường** *(SUMIFS của Sheets — đo 18/11: 4 dòng `oga | GAC - Other`
vào `OGA`, 1 dòng `ofR | …` vào `OFR`)*, so NGUYÊN NHÃN `"MÃ | Tên"` *(⛔ so mã: 153 dòng `ITE | …` nhãn khác ⛔ vào `ITE` ở
AS-IS)*. Nhãn ⛔ khớp nút nào ⇒ `dong_ngoai_cay`; ngày ngoài trục ⇒ `dong_ngoai_truc`.

⛔ **Hàng KPI** *(EBITDA · NCF · PL2… — công thức CHÉO hàng `=H8+H9+H23`, ⛔ "cha = Σ con")* ⛔ ở
bước này: engine tính mọi nút như cây ATL khai *(nút KPI là gốc ⛔ con ⇒ ô = Σ dòng gán nhãn ấy)*;
cổng WP-C3a loại chúng khỏi phép so bằng danh sách CÓ TÊN.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal
from typing import Iterable, Sequence

from fls.cau_hinh.hd import CayHD
from fls.cau_hinh.ky import Ky, LichKy, ky_cua

#: Khối tổng — Σ MỌI dòng *(⛔ lọc LE)*. Các khối khác là mã LE *(cột P)*.
KHOI_TONG = "GROUP"
_KHONG = Decimal(0)


@dataclass(frozen=True)
class DongCFA:
    """Một dòng sổ cho CFA1: ngày *(serial)* · LE *(None ⇒ chỉ vào GROUP)* · nhãn HD Final · BR/BS."""
    ngay: int
    le: str | None
    hd: str | None
    musd_no: Decimal
    musd_co: Decimal


@dataclass
class KetQuaCFA1:
    #: (khối, mã HD, ngày) → mUSD. Lưới ĐỦ: mọi khối × mọi nút × mọi ngày của trục.
    o: dict[tuple[str, str, int], Decimal]
    dong_ngoai_cay: list[int] = field(default_factory=list)    # chỉ số dòng vào
    dong_khac_hoa: list[int] = field(default_factory=list)     # khớp chỉ khi bỏ hoa thường
    dong_nhan_cha: list[int] = field(default_factory=list)     # nhãn là nút CÓ con ⇒ ⛔ cộng
    dong_ngoai_truc: list[int] = field(default_factory=list)


def _nhan(ma: str, ten: str) -> str:
    return f"{ma} | {ten}"


def cfa1_daily(dong: Iterable[DongCFA], cay: CayHD, ngay: Sequence[int],
               khoi: Sequence[str]) -> KetQuaCFA1:
    """Lá = Σ (musd_no − musd_co) theo (khối, nhãn HD, ngày); cha = Σ con theo `cay`.

    `ngay`: trục cột *(serial — H6: dựng bằng `truc_ngay(IX.PER, den)`, ⛔ ngày đầu tạm)*; `khoi`: khối tính, phải có
    `KHOI_TONG`. ⛔ đọc gì ngoài tham số *(⛔ đáp án, ⛔ kho)*.
    """
    if KHOI_TONG not in khoi:
        raise ValueError(f"`khoi` phải chứa {KHOI_TONG!r} *(khối Σ mọi dòng)*")
    truc = set(ngay)
    nut = cay.nut
    con: dict[str, list[str]] = {n.ma: [] for n in nut}
    for n in nut:
        if n.cha is not None:
            con[n.cha].append(n.ma)
    theo_nhan = {_nhan(n.ma, n.ten): n.ma for n in nut}
    theo_nhan_thuong = {k.casefold(): m for k, m in theo_nhan.items()}

    la: dict[tuple[str, str, int], Decimal] = {}
    kq = KetQuaCFA1(o={})
    for i, d in enumerate(dong):
        nhan = d.hd if isinstance(d.hd, str) else None
        ma = theo_nhan.get(nhan) if nhan is not None else None
        if ma is None and nhan is not None:
            ma = theo_nhan_thuong.get(nhan.casefold())
            if ma is not None:
                kq.dong_khac_hoa.append(i)
        if ma is None:
            kq.dong_ngoai_cay.append(i)
            continue
        if con[ma]:
            kq.dong_nhan_cha.append(i)
            continue
        if d.ngay not in truc:
            kq.dong_ngoai_truc.append(i)
            continue
        x = d.musd_no - d.musd_co
        for k in khoi:
            if k == KHOI_TONG or d.le == k:
                kh = (k, ma, d.ngay)
                la[kh] = la.get(kh, _KHONG) + x

    # cây: hậu thứ tự — con trước cha *(cây ATL ⛔ chu trình — C4 đã kiểm)*
    thu_tu: list[str] = []
    da: set[str] = set()

    def _di(m: str) -> None:
        if m in da:
            return
        da.add(m)
        for c in con[m]:
            _di(c)
        thu_tu.append(m)

    for n in nut:
        _di(n.ma)
    o = kq.o
    for k in khoi:
        for m in thu_tu:
            cs = con[m]
            for t in ngay:
                if cs:
                    s = _KHONG
                    for c in cs:
                        s += o[(k, c, t)]
                    o[(k, m, t)] = s
                else:
                    o[(k, m, t)] = la.get((k, m, t), _KHONG)
    return kq


# ══════════════════════════════════════════════════════════════════════════════════
# H6 — cuộn kỳ Y/H/Q/M theo IX.PER *(ISP 3.1.2 · Step 20 · WO-188 · AP §3.3.1 PD 410)*
# ══════════════════════════════════════════════════════════════════════════════════
# ⭐ Hành vi AS-IS *(công thức SA `Report I CFA1 Y H Q M`, đọc 18/11)*: ô LÁ =
#   `SUMIFS(Daily!hàng, Daily!$1:$1, năm[, Daily!$2|$3|$4, H|Q|M])`; tiêu đề Daily `Year=YEAR(ngày)`
#   · `Half=if(tháng<7,"H1","H2")` · `Quarter=if(tháng<4,"Q1",…)` · `Month=MONTH(ngày)` ⇒ đúng
#   `fls.cau_hinh.ky.ky_cua` *(năm của CHÍNH ngày — ⛔ ép 2025)*. Ô CHA = `=sum(con)`; Daily cha cũng
#   = Σ con ⇒ cuộn THẲNG mọi hàng của lưới Daily cho cùng số *(⛔ cây lần hai)*.
# ⛔ Trục ngày ⛔ còn là tham số tạm *(H5)*: `truc_ngay(IX.PER, den)` — ngày đầu là CONFIG trong kho
#   *(C6, `cau_hinh_repo.doc_per`)*; `den` = ngày đọc của ảnh đầu vào.
# ⛔ Kỳ ⛔ có ngày nào trên trục *(trước ngày đầu · chưa tới — errata ㉑)* ⇒ `ky_khong_ngay`: ô = 0
#   nhưng là "⛔ đo được", ⛔ "0 đã chốt".

#: Thứ tự 19 kỳ của một năm — khuôn cột 410 *(`2024` · `2024H1` · … · `2024Q4` · `2024M01` … `M12`)*.
def ky_truc_nam(nam: int) -> list[str]:
    return ([f"{nam}"] + [f"{nam}H{h}" for h in (1, 2)] + [f"{nam}Q{q}" for q in (1, 2, 3, 4)]
            + [f"{nam}M{m:02d}" for m in range(1, 13)])


def nhan_ky(k: Ky) -> tuple[str, str, str, str]:
    """(Y, H, Q, M) của một `Ky` — nhãn khuôn 410."""
    return (f"{k.nam}", f"{k.nam}H{k.nua}", f"{k.nam}Q{k.quy}", f"{k.nam}M{k.thang:02d}")


_GOC_SERIAL = date(1899, 12, 30)


def _ngay_serial(s: int) -> date:
    return _GOC_SERIAL + timedelta(days=s)


def truc_ngay(lich: LichKy, den: date) -> list[int]:
    """Trục cột Daily *(serial)* = `lich.ngay_dau` … `den` *(gồm hai đầu)*. `den` < ngày đầu ⇒ ném."""
    if den < lich.ngay_dau:
        raise ValueError(f"`den` {den} trước ngày đầu IX.PER {lich.ngay_dau} *(nguồn {lich.nguon})*")
    a = (lich.ngay_dau - _GOC_SERIAL).days
    return list(range(a, (den - _GOC_SERIAL).days + 1))


@dataclass
class KetQuaCuon:
    #: (khối, mã HD, nhãn kỳ) → mUSD. Lưới ĐỦ: mọi khối × mọi nút × 19 kỳ × mọi năm của trục.
    o: dict[tuple[str, str, str], Decimal]
    nam: tuple[int, ...]
    ky: list[str]                          # thứ tự cột
    so_ngay: dict[str, int]                # nhãn kỳ → số ngày trục rơi vào (chỉ kỳ > 0)
    ky_khong_ngay: tuple[str, ...]         # kỳ 0 ngày trên trục — ⛔ "0 đã chốt"


def cuon_ky(daily: dict[tuple[str, str, int], Decimal], cay: CayHD, ngay: Sequence[int],
            khoi: Sequence[str]) -> KetQuaCuon:
    """Σ lưới Daily *(`cfa1_daily(...).o`)* theo Y/H/Q/M của từng ngày trục *(`ky_cua`)*.

    Năm = các năm của CHÍNH trục *(min…max)*. Ô Daily thiếu ⇒ `KeyError` *(⛔ hoá 0)*.
    """
    if not ngay:
        raise ValueError("trục ngày rỗng ⇒ ⛔ cuộn được (Đ3)")
    nhan_theo_ngay = {t: nhan_ky(ky_cua(_ngay_serial(t))) for t in ngay}
    nams = tuple(range(_ngay_serial(min(ngay)).year, _ngay_serial(max(ngay)).year + 1))
    cot = [k for n in nams for k in ky_truc_nam(n)]
    so_ngay: dict[str, int] = {}
    for nh in nhan_theo_ngay.values():
        for k in nh:
            so_ngay[k] = so_ngay.get(k, 0) + 1
    o: dict[tuple[str, str, str], Decimal] = {}
    for kh in khoi:
        for n in cay.nut:
            for k in cot:
                o[(kh, n.ma, k)] = _KHONG
            for t in ngay:
                v = daily[(kh, n.ma, t)]
                for k in nhan_theo_ngay[t]:
                    o[(kh, n.ma, k)] += v
    return KetQuaCuon(o=o, nam=nams, ky=cot, so_ngay=so_ngay,
                      ky_khong_ngay=tuple(k for k in cot if k not in so_ngay))
