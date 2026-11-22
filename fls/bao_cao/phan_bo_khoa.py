"""`AL.KEY` — **phân bổ theo khoá driver có cờ** *(AP v3.1.2 §3.4.2 PD 500 · 511–513 · 604 · §3.5.3 D2 · D3 —
ISP 3.1.2 · Step 42 · `H12` · `WO-291`)*.

Đầu vào = lưới `SO.PLA3 PM + HR` Y/H/Q/M của H8 *(`pla.pla_yhqm` — `KetQuaPLA`)*; đầu ra = lưới cùng khoá
`(khối, mã HD, kỳ)` sau khi chia các mã có luật BẬT của `IX.ALR` *(C11)* từ khối nguồn *(`GROUP`)* xuống các
khối CDT theo tỉ lệ driver `(driver, CDT1, tháng)` *(IX.DRV — PD 604)*.

    lá[khối CDT, mã, tháng] = lá[GROUP, mã, tháng] × driver[(driver của luật, CDT1, tháng)]
    lá[khối dư, mã, tháng]  = lá[GROUP, …] − Σ lá[khối CDT, …]        (công thức `SHQ2` của sổ — ⛔ driver)
    kỳ Y/H/Q              = Σ tháng của nó          (ATL: `=sumifs(N8:Y8, N5:Y5, G5)`)
    tong / kpi            = `pla.danh_gia` *(công thức tab — dùng lại, ⛔ chép)*

⭐ **Cờ** = `BangALR.luat_cua(mã, tháng, cdt1=khối)` — ⛔ một mã HD nào gõ cứng ở đây *(bài `AC5` grep)*.
   Chia khi luật có hiệu lực, `bat` = True, có `driver` và ⛔ `khong_qua_allocate` *(Q3 — H1000)*; ngoại lệ AP
   §3.2.5 *(`luat_cua` trả `phuong_phap None`)* ⇒ giữ nguyên khối ấy.
⭐ **D2 — mặc định mọi cờ TẮT** ⇒ ⛔ một ô nào được chia ⇒ trả **đúng** lưới vào *(bản sao `o`, ⛔ tính lại —
   đồng nhất TỪNG Ô, ⛔ "khớp trong dung sai")*. Bật cờ chỉ trên dữ liệu TỔNG HỢP *(owner ký mới bật thật)*.
⭐ **Ngoại lệ CDT1 *(AP §3.2.5 — `OFR` × `CAH`)***: khối ngoại lệ giữ nguyên; khối khác nhận
   `d_khối / (1 − Σ d_ngoại lệ)` *(chuẩn hoá phần còn lại — công thức AS-IS đo SA FORMULA 22/11, vòng sửa R1)*.
⛔ **Driver thiếu ⇒ lỗi CÓ TÊN `DRIVER_THIEU`** kèm MỌI ô thiếu và lý do của bảng `o_thieu` *(ảnh DT10: 146 ô —
   `NB_LE` 96 · `CMN` 36 · `GI 202501` 14)* — ⛔ hoá 0. Ô có tiền nguồn = 0 ⛔ cần driver *(0 × mọi tỉ lệ = 0 —
   chính xác, ⛔ phải hoá 0)*. ⛔ bảng luật ⇒ `LUAT_THIEU`. Kỳ lạ ⇒ `KY_LA`.

Lõi THUẦN *(⛔ biết kho — khuôn `cfa.py`/`pla.py`)*: `BangALR` đọc từ kho ở tầng gọi
*(`fls.repo.cau_hinh_repo.doc_alr`)*; `LuoiDriver` do tầng gọi dựng.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Mapping, Sequence

from fls.bao_cao import pla
from fls.cau_hinh.hd import CayHD

LUAT_THIEU = "LUAT_THIEU"
DRIVER_THIEU = "DRIVER_THIEU"
KY_LA = "KY_LA"

#: driver của luật *(`luat_pb.DRIVER` — D3: By GI ⇒ PE)* → tên bảng trong lưới IX.DRV *(ảnh DT10)*
DRIVER_LUOI: dict[str, str] = {"PE": "GI_PE", "PM": "GI_PM", "NOEM": "NOEM"}

_KHONG = Decimal(0)
_KY = re.compile(r"^(\d{4})(?:([HQM])(\d{1,2}))?$")


class LoiPhanBoKhoa(ValueError):
    """Lỗi CÓ TÊN: `ma` ∈ {`LUAT_THIEU`, `DRIVER_THIEU`, `KY_LA`}; `o_thieu` = mọi ô driver thiếu."""

    def __init__(self, ma: str, thong_bao: str, o_thieu: Sequence[str] = ()) -> None:
        super().__init__(f"{ma}: {thong_bao}")
        self.ma = ma
        self.o_thieu = tuple(o_thieu)


@dataclass(frozen=True)
class LuoiDriver:
    """`o[(driver, cdt1, yyyymm)]` = tỉ lệ; `thieu[(…)]` = lý do CÓ TÊN của ô ⛔ có số *(bảng `o_thieu`)*."""
    o: Mapping[tuple[str, str, int], Decimal]
    thieu: Mapping[tuple[str, str, int], str] = field(default_factory=dict)


@dataclass
class KetQuaKhoa:
    o: dict[tuple[str, str, Any], Decimal]
    la: dict[tuple[str, str, Any], Decimal]
    cot: list
    khoi: tuple[str, ...]
    #: Đ4 — `o`: ô của lưới ra · `o_chia`: ô LÁ tháng được chia *(khối CDT)* · `luat_bat`: mã HD có ô chia
    dem: dict[str, int]
    #: (khối, mã, tháng) → (driver, tỉ lệ) của mỗi ô chia
    chia: dict[tuple[str, str, Any], tuple[str, Decimal]] = field(default_factory=dict)


def _tach(ky: Any) -> tuple[int, str | None, int | None]:
    m = _KY.match(ky) if isinstance(ky, str) else None
    if m is None:
        raise LoiPhanBoKhoa(KY_LA, f"kỳ {ky!r} ⛔ dạng YYYY · YYYYHn · YYYYQn · YYYYMmm")
    nam, loai, so = int(m.group(1)), m.group(2), (int(m.group(3)) if m.group(3) else None)
    gioi = {"H": 2, "Q": 4, "M": 12}.get(loai or "", 0)
    if loai and not 1 <= so <= gioi:
        raise LoiPhanBoKhoa(KY_LA, f"kỳ {ky!r} ⛔ hợp lệ")
    return nam, loai, so


def thang_cua(ky: Any) -> int | None:
    """`YYYYMmm` → yyyymm; kỳ gộp *(Y/H/Q)* → None."""
    nam, loai, so = _tach(ky)
    return nam * 100 + so if loai == "M" else None


def ky_gop(ky: Any) -> tuple[str, ...]:
    """Kỳ gộp CHỨA tháng `ky` *(Q · H · Y)*; kỳ gộp ⇒ ()."""
    nam, loai, so = _tach(ky)
    if loai != "M":
        return ()
    return (f"{nam}Q{(so - 1) // 3 + 1}", f"{nam}H{(so - 1) // 6 + 1}", str(nam))


def phan_bo_khoa(kq: pla.KetQuaPLA, alr: Any, cay: CayHD, ct: pla.CongThuc, *, khoi_nguon: str,
                 khoi_cdt: Sequence[str], khoi_du: str | None, driver: LuoiDriver | None = None) -> KetQuaKhoa:
    """Chia các mã có luật BẬT *(xem đầu tệp)*. `alr` = `luat_pb.BangALR` *(⛔ None — `LUAT_THIEU`)*."""
    if alr is None or not hasattr(alr, "luat_cua"):
        raise LoiPhanBoKhoa(LUAT_THIEU, "⛔ có bảng luật IX.ALR (C11) ⇒ ⛔ biết cờ — ⛔ đoán TẮT")
    loai = kq.loai
    thang = {t: thang_cua(t) for t in kq.cot}
    la = dict(kq.la)
    chia: dict[tuple[str, str, Any], tuple[str, Decimal]] = {}
    thieu: list[str] = []
    for n in cay.nut:
        if loai.get(n.ma) != "la":
            continue
        for t, yyyymm in thang.items():
            if yyyymm is None or not la.get((khoi_nguon, n.ma, t)):
                continue                            # tiền nguồn 0 ⇒ chia ra 0 ĐÚNG mọi tỉ lệ — ⛔ cần driver
            for kh in khoi_cdt:
                luat = alr.luat_cua(n.ma, yyyymm, cdt1=kh)
                if luat is None or not luat.bat or luat.khong_qua_allocate or luat.phuong_phap is None \
                        or luat.driver is None:
                    continue
                ten_drv = DRIVER_LUOI.get(luat.driver, luat.driver)
                # ⭐ vòng sửa R1 `H12`: luật có ngoại lệ CDT1 *(AP §3.2.5 — `luat.ngoai_le_cdt1`)* chia phần CÒN
                #    LẠI theo driver chuẩn hoá TRỪ khối ngoại lệ: `d_khối / (1 − Σ d_ngoại lệ)` *(AS-IS, SA FORMULA
                #    ATL 22/11: `NOEM_khối / (NOEM_GAG − NOEM_CAH)`; Σ7 NOEM = 1 — tham chiếu 604)*.
                can = [(ten_drv, kh, yyyymm)] + [(ten_drv, e, yyyymm) for e in luat.ngoai_le_cdt1]
                if driver is None:
                    thieu.append(f"{'|'.join(map(str, can[0]))} (⛔ có lưới driver IX.DRV)")
                    continue
                vang = [k for k in can if k not in driver.o]
                for k in vang:
                    thieu.append(f"{'|'.join(map(str, k))} "
                                 f"({driver.thieu.get(k, '⛔ có trong lưới driver — ngoài kỳ/khối có số')})")
                if not vang:
                    ty_le = driver.o[can[0]]
                    if len(can) > 1:
                        ty_le = ty_le / (1 - sum((driver.o[k] for k in can[1:]), _KHONG))
                    chia[(kh, n.ma, t)] = (ten_drv, ty_le)
    if thieu:
        raise LoiPhanBoKhoa(DRIVER_THIEU, f"{len(thieu)} ô driver thiếu ⇒ ⛔ chia (⛔ hoá 0): "
                            + " · ".join(thieu[:12]) + (" …" if len(thieu) > 12 else ""), thieu)
    dem = {"o": len(kq.o), "o_chia": len(chia), "luat_bat": len({m for _, m, _ in chia})}
    if not chia:                                    # D2: cờ tắt ⇒ đồng nhất TỪNG Ô
        return KetQuaKhoa(o=dict(kq.o), la=la, cot=list(kq.cot), khoi=tuple(kq.khoi), dem=dem)
    for (kh, m, t), (_, ty_le) in chia.items():
        la[(kh, m, t)] = la[(khoi_nguon, m, t)] * ty_le
    co_ky = set(kq.cot)
    # ⭐ vòng sửa R1 `H12`: cuộn kỳ + dư CHỈ ở kỳ CÓ ô chia *(tháng chia + kỳ gộp chứa nó)* — đo trước sửa: cờ ký 2025
    #    làm 6 ô `SHQ2` 2026 Y/H1/Q1 lệch 1e-29 vì dư tính lại CẢ kỳ ⛔ chia *(bài `…ky_ngoai_2025_dong_nhat…`)*.
    ky_cham: dict[str, set] = {}
    for _, m, t in chia:
        ky_cham.setdefault(m, set()).update({t, *ky_gop(t)})
    for kh, m in {(kh, m) for kh, m, _ in chia}:     # cuộn lại Y/H/Q của mã bị chia *(ATL: Σ tháng)*
        for g in {g for g in ky_cham[m] if thang.get(g) is None} & co_ky:
            la[(kh, m, g)] = sum((la[(kh, m, t)] for t in kq.cot if g in ky_gop(t)), _KHONG)
    if khoi_du is not None:
        for m, kys in ky_cham.items():
            for t in kys & co_ky:
                la[(khoi_du, m, t)] = la[(khoi_nguon, m, t)] - sum((la[(k, m, t)] for k in khoi_cdt), _KHONG)
    o = pla.danh_gia(la, cay, list(kq.cot), tuple(kq.khoi), ct)
    return KetQuaKhoa(o=o, la=la, cot=list(kq.cot), khoi=tuple(kq.khoi), dem=dem, chia=chia)
