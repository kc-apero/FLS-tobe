"""`AL.PLT` · **phân bổ nền tảng GI theo tỷ lệ** + `KS.AL` *(Σ chia = O / P)* — AP v3.1.2 §3.4.1
PD 505–507 · §3.5.4 WP-C4. ISP 3.1.2 · Step 24 · `H9` *(`WO-200`)*.

    RATE_cdt = PE_cdt ÷ Σ PE các CDT1        theo Vendor-tháng
    chia_pe_cdt = RATE_cdt × O · chia_pm_cdt = RATE_cdt × P
    O = 0 ∧ P > 0  ⇒  RATE theo TỔNG THÁNG   (Σ PE_cdt mọi vendor của tháng ÷ Σ PE tháng)

⭐ Lõi **THUẦN** *(⛔ biết kho — khuôn `cfa.py`)*: IX.VEN *(`BangVen` của C9, đọc từ kho ở tầng
gọi)* · PE theo CDT1 · O · P được TRUYỀN VÀO.

⛔ **Vendor đặc biệt bỏ qua có ĐẾM** *(`chia_nen_tang` — H9)*: vendor có BẤT KỲ dòng IX.VEN nào
mang nhãn `cach_tinh` ≠ `thường` ⇒ ⛔ chia, ghi vào `bo_qua[nhãn]`. `bo_qua` LUÔN có đủ **5** khoá
có tên `NHAN_RIENG` *(kể cả khi 0 vendor-tháng — ⛔ im)*. Đo ảnh DT8 *(Đ4)*: vendor mang nhãn đặc
biệt = **15** mã *(12 qua network nhãn riêng + 3 mã nhãn riêng; một mã mang hai nhãn riêng; một mã
mang nhãn riêng lẫn `thường` ⇒ đặc biệt)*; vendor THUẦN `thường` = **4** mã. ⭐ H10 *(dưới)*: mọi
vendor đi CHUNG một đường `chia_theo_cach_tinh`, `bo_qua` = 0.

⭐ **`H10` — tính theo MÃ 'cách tính'** *(ISP 3.1.2 · Step 28 · `WO-216`)*. Tên 5 mã chỉ sống ở config
`fls.cau_hinh.vendor.CACH_TINH` *(mã → KIỂU hàm)*; ở đây ⛔ một chuỗi tên vendor *(`H10-B2`: grep = 0)*.
Công thức AS-IS đọc NGUYÊN VĂN bằng `FORMULA` 19/11 *(sổ `[COPY] GI Platform Data Ledger`)* — tên mã
thay bằng `‹mã›`, sheet viết tắt *(L = `Source (Looker)` · VNM = `Vendor & Network Mapping` ·
M2 = `CFA2 | MID 2 …` · F3 = `[Formula] CFA2 | MID 3 …`)*:

  · **PE theo CDT1 — `CFA2 | MID 1` cột `E`** *(= CFA1 `E` thêm điều kiện `L!S:S,J`)* — `HAM_PE`:
      `=iferror(if(or(M10="‹mã theo No›",M10="‹mã theo No›"),SUMIFS(L!$K:$K,L!$I:$I,VLOOKUP($M10,
       {VNM!$N$4:$N$35,VNM!$O$4:$O$35},2,FALSE),L!$Q:$Q,$Q10,L!$O:$O,$K10,L!S:S,J10),
       if(and(VLOOKUP(M10,{VNM!$N$4:$N$35,VNM!$O$4:$O$35},2,FALSE)="‹mã tỷ lệ›",Q10=1),
       sumifs(L!$K:$K,L!$I:$I,VLOOKUP(M10,…,2,FALSE),L!O:O,K10,L!S:S,J10)*VLOOKUP(M10,
       {VNM!$N$4:$N$35,VNM!$Q$4:$Q$35},2,FALSE),
       if(and(M10="‹mã theo dòng›",Q10=1),SUMIFS(L!$K:$K,L!$I:$I,"Apple_store",L!$O:$O,K10,L!S:S,J10),
       if(and(M10="‹mã theo dòng›",Q10=2),SUMIFS(L!$K:$K,L!$I:$I,"IAP_tracking",L!$O:$O,K10,L!S:S,J10),
       0)))))`
    ⇒ bốn kiểu: `mang_theo_no` · `mang_ty_le_no1` · `mang_dong_no` · `khong` *(nhánh cuối `0`: vendor
    `thường` có PE = 0 vì CÔNG THỨC)*. `VLOOKUP(…,FALSE)` lấy dòng ĐẦU của vendor ⇒ hàm PE theo
    nhãn dòng đầu.
  · **RATE — `M2!AA`**: `=T11/sum(T11:T16)` *(T = PE MID2 = `SUMIFS(MID1!E; M; K; J)` — gộp mọi No;
    6 CDT1, ⛔ SHQ2)*.
  · **Chia — `F3!S:T`** *(một dòng = một dòng CFA1 = Vendor × tháng × No)*:
      PE `=iferror(sumifs(M2!$AA:$AA,M2!$M:$M,$AU11,M2!$K:$K,$F11,M2!$J:$J,S$7)*$O11)`
      PM `=iferror(if(and($O11=0,$P11>0),$P11*S10/O10, sumifs(M2!$AA:$AA,…,$AU11,…,T$7)*$P11))`
    với `S10 = sum(S11:S46)` · `O10 = sum(O11:O46)` *(tổng KHỐI THÁNG — mọi dòng CFA1 của tháng)*.
  · **Khoá RATE — `F3!AU`**: `=if(H11<>"‹mã mượn›",H11,VLOOKUP(AQ11,AR11:AT12,3,FALSE))`,
      `AS11 = SUMIFS(P11:P46,AQ11:AQ46,AR11)` *(ΣP của ‹mã mượn›-No)*,
      `AT11 = if(AS11>AS12,"‹vendor cho mượn›","‹mã mượn›")` · `AT12 = if(AT11="‹vendor cho mượn›",
      "‹mã mượn›","‹vendor cho mượn›")` ⇒ `khoa_rate`.
  · MID3 hiển thị = `sumifs(F3!…; F = tháng; H = vendor)` ⇒ khoá so `(vendor, tháng)`.

⛔ **Lỗi CÓ TÊN, ⛔ im** *(`LoiPhanBo`, gói MỌI lý do)*: Σ PE = 0 mà tiền ≠ 0 *(⛔ chia 0 im)*;
vendor ⛔ có trong IX.VEN; CDT1 lạ; khoá O/P/PE lệch nhau. `ks_al` đo lại Σ chia = O / P
ĐỘC LẬP *(TOL `1e-6` = TOL cổng DT8 `gi_mid3`)* và nêu `Vendor · tháng · lệch`.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Mapping

from fls.cau_hinh.vendor import CACH_TINH, NHAN_RIENG, NHAN_THUONG, BangVen

#: Dung sai `KS.AL` *(= `TOL` khuôn `gi_mid3`; đo DT8: dư lớn nhất của sheet `5,085e-9`)*.
TOL = Decimal("0.000001")
_0 = Decimal(0)

Khoa = tuple[str, str]                   # (vendor, thang yyyymm)


class LoiPhanBo(ValueError):
    """`AL.PLT`/`KS.AL` ⛔ chia được hoặc chia sai. `ly_do` = **mọi** lý do có tên."""

    def __init__(self, ly_do: Iterable[str]) -> None:
        self.ly_do = tuple(ly_do)
        super().__init__(f"⛔ AL.PLT — {len(self.ly_do)} lỗi: " + " · ".join(self.ly_do))


@dataclass(frozen=True)
class KetQuaPhanBo:
    cdt1: tuple[str, ...]
    #: (vendor, tháng) → cdt1 → (chia_pe, chia_pm) — CHỈ vendor thường.
    chia: dict[Khoa, dict[str, tuple[Decimal, Decimal]]]
    rate: dict[Khoa, dict[str, Decimal]]
    #: (vendor, tháng) chia theo TỔNG THÁNG *(O = 0 ∧ P > 0)*.
    theo_tong_thang: tuple[Khoa, ...]
    #: nhãn đặc biệt → các (vendor, tháng) bỏ qua. Luôn đủ 5 khoá `NHAN_RIENG`.
    bo_qua: dict[str, tuple[Khoa, ...]]


def nhan_vendor(ven: BangVen) -> dict[str, frozenset[str]]:
    """vendor → tập nhãn `cach_tinh` trên mọi dòng IX.VEN của nó."""
    d: dict[str, set[str]] = defaultdict(set)
    for r in ven.dong:
        d[r.vendor].add(r.cach_tinh)
    return {v: frozenset(s) for v, s in d.items()}


def chia_nen_tang(pe: Mapping[Khoa, Mapping[str, Decimal]], o: Mapping[Khoa, Decimal],
                  p: Mapping[Khoa, Decimal], ven: BangVen, *,
                  cdt1: Iterable[str]) -> KetQuaPhanBo:
    """Chia O / P của từng Vendor-tháng thường xuống `cdt1` theo RATE. Rồi `ks_al`."""
    cdt = tuple(cdt1)
    ly: list[str] = []
    if not cdt or len(set(cdt)) != len(cdt):
        raise LoiPhanBo([f"CDT1: {len(cdt)} mục, {len(set(cdt))} khác nhau — phải ≥ 1, ⛔ trùng"])
    la = sorted(set(cdt) - set(ven.cdt1))
    if la:
        ly.append(f"CDT1 ⛔ thuộc IX.VEN: {la}")
    if set(o) != set(p) or set(o) != set(pe):
        ly.append(f"khoá lệch: O {len(o)} · P {len(p)} · PE {len(pe)} Vendor-tháng "
                  f"*(thiếu ở PE: {sorted(set(o) - set(pe))[:5]} · thừa ở PE: "
                  f"{sorted(set(pe) - set(o))[:5]})*")
    if not o:
        ly.append("0 Vendor-tháng ⇒ ⛔ chia được (Đ3: tập rỗng là KẾT QUẢ, ⛔ nền xanh)")
    nhan = nhan_vendor(ven)
    for k, d in pe.items():
        lc = sorted(set(d) - set(cdt))
        if lc:
            ly.append(f"{k[0]} · {k[1]}: CDT1 lạ ở PE {lc}")
    if ly:
        raise LoiPhanBo(ly)

    def _pe(k: Khoa, c: str) -> Decimal:
        return pe[k].get(c, _0)

    # Σ PE_cdt theo TỔNG THÁNG — mọi vendor trong PE của tháng ấy *(kể cả đặc biệt: tổng tháng
    # là thuộc tính của đầu vào, ⛔ của nhóm vendor)*.
    tong_thang: dict[str, dict[str, Decimal]] = defaultdict(lambda: {c: _0 for c in cdt})
    for k in pe:
        for c in cdt:
            tong_thang[k[1]][c] += _pe(k, c)

    chia: dict[Khoa, dict[str, tuple[Decimal, Decimal]]] = {}
    rate: dict[Khoa, dict[str, Decimal]] = {}
    ttt: list[Khoa] = []
    bo_qua: dict[str, list[Khoa]] = {n: [] for n in NHAN_RIENG}
    for k in sorted(o):
        v, t = k
        if v not in nhan:
            ly.append(f"{v} · {t}: vendor ⛔ có trong IX.VEN ({ven.nguon})")
            continue
        rieng = sorted(nhan[v] - {NHAN_THUONG})
        if rieng:
            for n in rieng:
                bo_qua[n].append(k)
            continue
        ok, pk = o[k], p[k]
        if ok == 0 and pk > 0:
            nen, ttt_ = tong_thang[t], True
        else:
            nen, ttt_ = {c: _pe(k, c) for c in cdt}, False
        s = sum(nen.values(), _0)
        if s == 0:
            if ok == 0 and pk == 0:
                rate[k] = {}
                chia[k] = {c: (_0, _0) for c in cdt}
                continue
            ly.append(f"{v} · {t}: Σ PE {'tổng tháng' if ttt_ else 'Vendor-tháng'} = 0 mà "
                      f"O = {ok} · P = {pk} ⇒ ⛔ chia được (⛔ chia 0 im)")
            continue
        r = {c: nen[c] / s for c in cdt}
        rate[k] = r
        chia[k] = {c: (r[c] * ok, r[c] * pk) for c in cdt}
        if ttt_:
            ttt.append(k)
    if ly:
        raise LoiPhanBo(ly)
    kq = KetQuaPhanBo(cdt, chia, rate, tuple(ttt), {n: tuple(x) for n, x in bo_qua.items()})
    ks_al(kq, o, p)
    return kq


def ks_al(kq: "KetQuaPhanBo | KetQuaCachTinh", o: Mapping[Khoa, Decimal],
          p: Mapping[Khoa, Decimal | None], *,
          tol: Decimal = TOL) -> int:
    """`KS.AL`: Σ chia = O ∧ Σ chia = P từng Vendor-tháng đã chia. Trả SỐ Vendor-tháng đã đo
    *(mẫu số — 0 ⇒ `LoiPhanBo`, Đ3)*; lệch ⇒ `LoiPhanBo` nêu `Vendor · tháng · vế · lệch`."""
    if not kq.chia:
        raise LoiPhanBo(["KS.AL: 0 Vendor-tháng đã chia ⇒ ⛔ đo được (Đ3)"])
    ly: list[str] = []
    for k, d in sorted(kq.chia.items()):
        for ve, i, tien in (("PE", 0, o[k]), ("PM", 1, p[k])):
            if tien is None:               # H10: P = chữ ⇒ vế PM ⛔ xác định ⇒ ⛔ đo *(⛔ hoá 0)*
                continue
            lech = sum((x[i] for x in d.values()), _0) - tien
            if abs(lech) > tol:
                ly.append(f"KS.AL {k[0]} · {k[1]} · {ve}: Σ chia − tiền = {lech}")
    if ly:
        raise LoiPhanBo(ly)
    return len(kq.chia)


# ═════════════════════════════════════════════════════════════════════════════════════════════
# H10 — tính theo MÃ 'cách tính' *(công thức AS-IS nguyên văn ở docstring mô-đun)*
# ═════════════════════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class DongLooker:
    """Một dòng `Source (Looker)` đã gộp: I network · Q No *(None = ⛔ có)* · O tháng · S CDT1 · K tiền."""
    mang: str
    no: str | None
    thang: str
    cdt1: str
    tien: Decimal


@dataclass(frozen=True)
class DongCFA1:
    """Một dòng CFA1 GI *(PD 504)* = Vendor × tháng × No: O = `E` PE Amount · P = `S` PM Amount
    *(None = chữ `Need to manual input` ⇒ ⛔ hoá 0)*."""
    vendor: str
    thang: str
    no: str
    o: Decimal
    p: Decimal | None


@dataclass(frozen=True)
class KetQuaCachTinh:
    cdt1: tuple[str, ...]
    #: (vendor, tháng) → cdt1 → (chia_pe, chia_pm | None) — MỌI vendor *(thường + đặc biệt)*.
    chia: dict[Khoa, dict[str, tuple[Decimal, Decimal | None]]]
    o: dict[Khoa, Decimal]
    p: dict[Khoa, Decimal | None]
    #: vendor → KIỂU hàm PE *(theo nhãn dòng IX.VEN ĐẦU)*.
    ma: dict[str, str]
    #: (vendor, tháng, No, vendor cho mượn) — dòng lấy RATE của vendor khác *(`F3!AU`)*.
    muon: tuple[tuple[str, str, str, str], ...]
    #: (vendor, tháng, No) chia PM theo tổng khối tháng *(O = 0 ∧ P > 0)*.
    theo_tong_thang: tuple[tuple[str, str, str], ...]
    #: luôn đủ 5 khoá `NHAN_RIENG`, mỗi khoá RỖNG — H10 ⛔ bỏ qua vendor nào *(WP-C4b: bỏ qua = 0)*.
    bo_qua: dict[str, tuple[Khoa, ...]]


def _dau(ven: BangVen) -> dict[str, object]:
    d: dict[str, object] = {}
    for r in ven.dong:                       # thứ tự sheet ⇒ dòng ĐẦU = `VLOOKUP(…,FALSE)`
        d.setdefault(r.vendor, r)
    return d


def _pe_khong(ven, looker, v, t, no, c) -> Decimal:
    return _0


def _pe_mang_theo_no(ven, looker, v, t, no, c) -> Decimal:
    net = _dau(ven)[v].network
    return sum((x.tien for x in looker if x.mang == net and x.no == no and x.thang == t
                and x.cdt1 == c), _0)


def _pe_mang_ty_le_no1(ven, looker, v, t, no, c) -> Decimal:
    d = _dau(ven)[v]
    if no != "1" or d.pct is None:
        return _0
    return sum((x.tien for x in looker if x.mang == d.network and x.thang == t and x.cdt1 == c),
               _0) * d.pct


def _pe_mang_dong_no(ven, looker, v, t, no, c) -> Decimal:
    net = next((r.network for r in ven.dong if r.vendor == v and r.no == no), None)
    if net is None:
        return _0
    return sum((x.tien for x in looker if x.mang == net and x.thang == t and x.cdt1 == c), _0)


#: KIỂU hàm PE → hàm. Khoá là kiểu *(⛔ tên vendor)*; mã → kiểu ở `CACH_TINH` (config).
HAM_PE = {"khong": _pe_khong, "mang_theo_no": _pe_mang_theo_no,
          "mang_ty_le_no1": _pe_mang_ty_le_no1, "mang_dong_no": _pe_mang_dong_no}


def ma_cach_tinh(ven: BangVen, bang: Mapping[str, tuple[str, str | None]] = CACH_TINH
                 ) -> dict[str, tuple[str, str | None]]:
    """vendor → (kiểu hàm PE theo nhãn dòng ĐẦU, vendor cho mượn RATE | None). Mã ⛔ có trong
    `bang`, kiểu lạ, hai nguồn mượn ⇒ `LoiPhanBo` có tên *(⛔ rơi im về `thường`)*."""
    ly: list[str] = []
    for m, (k, _) in sorted(bang.items()):
        if k not in HAM_PE:
            ly.append(f"kiểu hàm PE lạ {k!r} (mã {m!r})")
    nhan: dict[str, list[str]] = defaultdict(list)
    for r in ven.dong:
        if r.cach_tinh not in bang:
            ly.append(f"mã 'cách tính' ⛔ có hàm: {r.cach_tinh!r} (vendor {r.vendor})")
        elif r.cach_tinh not in nhan[r.vendor]:
            nhan[r.vendor].append(r.cach_tinh)
    if ly:
        raise LoiPhanBo(ly)
    kq: dict[str, tuple[str, str | None]] = {}
    for v, ns in nhan.items():
        muon = sorted({bang[n][1] for n in ns} - {None})
        if len(muon) > 1:
            ly.append(f"{v}: hai nguồn mượn RATE {muon}")
        kq[v] = (bang[ns[0]][0], muon[0] if muon else None)
    if ly:
        raise LoiPhanBo(ly)
    return kq


def pe_tu_looker(ven: BangVen, looker: Iterable[DongLooker], vendor: str, thang: str, no: str,
                 cdt1: str, *, bang: Mapping[str, tuple[str, str | None]] = CACH_TINH) -> Decimal:
    """PE của (vendor, tháng, No, CDT1) từ Looker theo hàm của mã 'cách tính' *(= MID1 `E`)*."""
    ma = ma_cach_tinh(ven, bang)
    if vendor not in ma:
        raise LoiPhanBo([f"{vendor}: vendor ⛔ có trong IX.VEN ({ven.nguon})"])
    return HAM_PE[ma[vendor][0]](ven, list(looker), vendor, thang, no, cdt1)


def chia_theo_cach_tinh(dong: Iterable[DongCFA1], pe: Mapping[Khoa, Mapping[str, Decimal]],
                        ven: BangVen, *, cdt1: Iterable[str],
                        bang: Mapping[str, tuple[str, str | None]] = CACH_TINH) -> KetQuaCachTinh:
    """`[Formula] MID3`: chia TỪNG dòng CFA1 xuống `cdt1` theo RATE MID2 của khoá `khoa_rate`;
    gộp theo (vendor, tháng) *(= MID3 hiển thị)*; rồi `ks_al`. `pe` = PE MID2 theo (vendor, tháng)
    × CDT1 *(tầng gọi gộp MID1 `E` mọi No)*."""
    cdt = tuple(cdt1)
    ds = list(dong)
    ma = ma_cach_tinh(ven, bang)
    ly: list[str] = []
    if not cdt or len(set(cdt)) != len(cdt):
        raise LoiPhanBo([f"CDT1: {len(cdt)} mục, {len(set(cdt))} khác nhau — phải ≥ 1, ⛔ trùng"])
    if not ds:
        raise LoiPhanBo(["0 dòng CFA1 ⇒ ⛔ chia được (Đ3)"])
    for r in ds:
        if r.vendor not in ma:
            ly.append(f"{r.vendor} · {r.thang}: vendor ⛔ có trong IX.VEN ({ven.nguon})")
    if ly:
        raise LoiPhanBo(ly)

    def rate(k: Khoa) -> dict[str, Decimal] | None:
        d = pe.get(k, {})
        s = sum((d.get(c, _0) for c in cdt), _0)
        return None if s == 0 else {c: d.get(c, _0) / s for c in cdt}

    # khoá RATE từng dòng *(F3!AU)*
    nhom: dict[Khoa, list[DongCFA1]] = defaultdict(list)
    for r in ds:
        nhom[(r.vendor, r.thang)].append(r)
    khoa: dict[int, str] = {}
    muon: list[tuple[str, str, str, str]] = []
    for (v, t), rs in sorted(nhom.items()):
        b = ma[v][1]
        if b is None:
            continue
        nos = sorted({r.no for r in rs}, key=lambda x: (len(x), x))
        if len(nos) != 2:
            ly.append(f"{v} · {t}: mượn RATE cần đúng 2 No, đo {len(nos)}")
            continue
        sp = [sum((r.p or _0 for r in rs if r.no == n), _0) for n in nos]
        ai = nos[0] if sp[0] > sp[1] else nos[1]
        muon.append((v, t, ai, b))
        for r in rs:
            if r.no == ai:
                khoa[id(r)] = b
    if ly:
        raise LoiPhanBo(ly)

    pe_dong: list[tuple[DongCFA1, dict[str, Decimal]]] = []
    s_thang: dict[str, dict[str, Decimal]] = defaultdict(lambda: {c: _0 for c in cdt})
    o_thang: dict[str, Decimal] = defaultdict(lambda: _0)
    for r in ds:
        r_ = rate((khoa.get(id(r), r.vendor), r.thang))
        if r_ is None and (r.o != 0 or (r.p is not None and r.p != 0 and not (r.o == 0 and r.p > 0))):
            ly.append(f"{r.vendor} · {r.thang} · No {r.no}: Σ PE = 0 mà O = {r.o} · P = {r.p} "
                      f"⇒ ⛔ chia được (⛔ chia 0 im)")
            continue
        x = {c: (r_[c] * r.o if r_ else _0) for c in cdt}
        pe_dong.append((r, x))
        o_thang[r.thang] += r.o
        for c in cdt:
            s_thang[r.thang][c] += x[c]
    if ly:
        raise LoiPhanBo(ly)

    chia: dict[Khoa, dict[str, list]] = {}
    o: dict[Khoa, Decimal] = defaultdict(lambda: _0)
    p: dict[Khoa, Decimal | None] = {}
    ttt: list[tuple[str, str, str]] = []
    for r, x in pe_dong:
        k = (r.vendor, r.thang)
        d = chia.setdefault(k, {c: [_0, _0] for c in cdt})
        o[k] += r.o
        p[k] = None if r.p is None or (k in p and p[k] is None) else p.get(k, _0) + r.p
        if r.p is None:
            pm = {c: None for c in cdt}
        elif r.o == 0 and r.p > 0:
            if o_thang[r.thang] == 0:
                ly.append(f"{r.vendor} · {r.thang} · No {r.no}: tổng tháng Σ O = 0 ⇒ ⛔ chia P")
                continue
            pm = {c: r.p * s_thang[r.thang][c] / o_thang[r.thang] for c in cdt}
            ttt.append((r.vendor, r.thang, r.no))
        else:
            r_ = rate((khoa.get(id(r), r.vendor), r.thang))
            pm = {c: (r_[c] * r.p if r_ else _0) for c in cdt}
        for c in cdt:
            d[c][0] += x[c]
            d[c][1] = None if pm[c] is None or d[c][1] is None else d[c][1] + pm[c]
    if ly:
        raise LoiPhanBo(ly)
    kq = KetQuaCachTinh(cdt, {k: {c: (a, b) for c, (a, b) in d.items()} for k, d in chia.items()},
                        dict(o), p, {v: m[0] for v, m in ma.items()}, tuple(muon), tuple(ttt),
                        {n: () for n in NHAN_RIENG})
    ks_al(kq, kq.o, kq.p)
    return kq
