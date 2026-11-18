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
from decimal import Decimal
from typing import Iterable, Sequence

from fls.cau_hinh.hd import CayHD

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

    `ngay`: trục cột *(serial, tạm lấy từ tham số tới H6 đọc IX.PER)*; `khoi`: khối tính, phải có
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
