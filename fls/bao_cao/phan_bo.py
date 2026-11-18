"""`AL.PLT` · **phân bổ nền tảng GI theo tỷ lệ** + `KS.AL` *(Σ chia = O / P)* — AP v3.1.2 §3.4.1
PD 505–507 · §3.5.4 WP-C4. ISP 3.1.2 · Step 24 · `H9` *(`WO-200`)*.

    RATE_cdt = PE_cdt ÷ Σ PE các CDT1        theo Vendor-tháng
    chia_pe_cdt = RATE_cdt × O · chia_pm_cdt = RATE_cdt × P
    O = 0 ∧ P > 0  ⇒  RATE theo TỔNG THÁNG   (Σ PE_cdt mọi vendor của tháng ÷ Σ PE tháng)

⭐ Lõi **THUẦN** *(⛔ biết kho — khuôn `cfa.py`)*: IX.VEN *(`BangVen` của C9, đọc từ kho ở tầng
gọi)* · PE theo CDT1 · O · P được TRUYỀN VÀO.

⛔ **Vendor đặc biệt bỏ qua có ĐẾM** *(H10)*: vendor có BẤT KỲ dòng IX.VEN nào mang nhãn
`cach_tinh` ≠ `thường` ⇒ ⛔ chia, ghi vào `bo_qua[nhãn]`. `bo_qua` LUÔN có đủ **5** khoá có tên
`NHAN_RIENG` *(kể cả khi 0 vendor-tháng — ⛔ im)*. Đo ảnh DT8 *(Đ4)*: vendor mang nhãn đặc
biệt = **15** mã *(12 qua network `Max` + VD341 · VD428 · VD444; VD62 mang cả `Max` lẫn `VD62`;
VD57 mang cả `Max` lẫn `thường` ⇒ đặc biệt)*; vendor THUẦN `thường` = **4** mã
*(VD58 · VD61 · VD113 · VD336)*.

⛔ **Lỗi CÓ TÊN, ⛔ im** *(`LoiPhanBo`, gói MỌI lý do)*: Σ PE = 0 mà tiền ≠ 0 *(⛔ chia 0 im)*;
vendor ⛔ có trong IX.VEN; CDT1 lạ; khoá O/P/PE lệch nhau. `ks_al` đo lại Σ chia = O / P
ĐỘC LẬP *(TOL `1e-6` = TOL cổng DT8 `gi_mid3`)* và nêu `Vendor · tháng · lệch`.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Mapping

from fls.cau_hinh.vendor import NHAN_RIENG, NHAN_THUONG, BangVen

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


def ks_al(kq: KetQuaPhanBo, o: Mapping[Khoa, Decimal], p: Mapping[Khoa, Decimal], *,
          tol: Decimal = TOL) -> int:
    """`KS.AL`: Σ chia = O ∧ Σ chia = P từng Vendor-tháng đã chia. Trả SỐ Vendor-tháng đã đo
    *(mẫu số — 0 ⇒ `LoiPhanBo`, Đ3)*; lệch ⇒ `LoiPhanBo` nêu `Vendor · tháng · vế · lệch`."""
    if not kq.chia:
        raise LoiPhanBo(["KS.AL: 0 Vendor-tháng đã chia ⇒ ⛔ đo được (Đ3)"])
    ly: list[str] = []
    for k, d in sorted(kq.chia.items()):
        for ve, i, tien in (("PE", 0, o[k]), ("PM", 1, p[k])):
            lech = sum((x[i] for x in d.values()), _0) - tien
            if abs(lech) > tol:
                ly.append(f"KS.AL {k[0]} · {k[1]} · {ve}: Σ chia − tiền = {lech}")
    if ly:
        raise LoiPhanBo(ly)
    return len(kq.chia)
