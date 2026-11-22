"""`do_hd2.py --goi WP-C5a` — PARITY HD2 `AL.KEY` cờ TẮT ↔ ATL 606 *(+ tham chiếu 604)* — ISP 3.1.2 · Step 42 ·
H12 · `WO-291`.

⭐ **Đầu vào = THƯỢNG NGUỒN, ⛔ đáp án**: lưới `SO.PLA3 PM + HR` Y/H/Q/M do H8 tính từ ảnh đầu vào DT7b
*(`do_hd2_c3d.tinh_luoi` → `pla.pla_yhqm`)* → `phan_bo_khoa` *(cờ từ `IX.ALR` ĐỌC TỪ KHO — C11, mọi cờ TẮT — D2)*.
Đáp án `tests/fixture/dap_an/atl.json` *(DT10)* chỉ ĐỌC ở bước so. Khoá hàng ATL → `(khối, mã)` dựng từ CHÍNH ảnh
ATL *(khối mở ở mỗi hàng `GI`, thứ tự `KHOI_12` của H8; mã = nhãn trước ` | `)*.

⚠ **ERRATA đo 22/11** *(SA đọc FORMULA `B5:BK1110`, chỉ-đọc)*: WO/BG-197 ghi "AS-IS CHƯA phân bổ ⇒ ATL = đáp án
cờ tắt" — SAI cho 2025. Ô tháng 2025 của 6 khối CDT: **576** ô By GI *(8 mã × 6 khối × 12: `iferror(sumifs(GROUP)×
(GI khối/GI GROUP))`)* · **348** ô By NOEM *(5 mã — CAH 4, ngoại lệ OFR — × 12: `INDEX('[H1.2026][2025]H1000 I HR
Report'…)`)* · **66** ô `GI` khối CDT lấy `CFA2 | MID 3 | GI Platform Data Ledger` *(⛔ PLA3)*; GROUP `OMC` 2025-02 =
`PLA3 − 0,5` *(gõ tay)*; SGO1 một hàng `+ 'Allocation Table | NB | By LE'×−1` *(12 ô 2025)*. ⇒ AS-IS ĐÃ BẬT phân bổ;
FLS giữ cờ TẮT *(D2)* ⇒ các ô ấy là **lệch AS-IS có tên** *(⛔ chép vào engine)*.

⭐ **VÒNG SỬA R1 *(`KQ-293` · `H12-R1-01`)* — cổng đo ở CỜ BẬT 2025** *(quyết của chủ 22/11 ~10:05 UTC: ký bật
IX.ALR 2025 giống AS-IS)*: cờ đọc từ KHO = phiên bản ký `tests/fixture/cau_hinh/ix_alr_2025_bat.json`
*(`cau_hinh_repo.ky_bat_ix_alr`, actor = người ký)*. Cờ TẮT còn là bài đồng nhất `H12-B1` *(⛔ cổng)*.

── LỚP LỆCH *(Đ5 — `mong` khai TRƯỚC ở `do_hd2_c5a_mong.py`, khác ⇒ ĐỎ CẢ HAI CHIỀU)* ────────────────────────
⭐ Nhãn do **PHÉP ĐO** gán *(luật phòng tái phạm `H12-R1-01`: ⛔ quy tắc khối × năm cho 2025)*:
  ① `loi_as_is` — lỗi AS-IS thật: `o_lech` TỪNG Ô theo giá trị *(224: GROUP `OMC` −0,5 gõ tay + lan · SGO1 NB by
     LE + lan)* + `as_is_truoc_CA` *(675: lệch 416 dán cũ 2024 lan từ H8 — `BG-278`; cờ 2025 ⛔ đổi đếm)* +
     `as_is_tay_lan_du` *(ô chỉ hồi phục ở phản thực ②b — dư SHQ2 lấy GROUP của ATL mang −0,5 gõ tay)*.
  ② `chua_co_dau_vao` — ô HỒI PHỤC khi thay lá khối CDT 2025 của 4 sổ nền tảng `GI · OMC · PS · SC` bằng giá trị
     nguồn AS-IS *(phản thực — CHẨN ĐOÁN, ⛔ đầu vào engine)*. SA FORMULA 22/11: lá ấy = hàng `TOTAL yyyymm` của tab
     `CFA2 | MID 3 | X Platform Data Ledger` cột PM theo CDT *(T·V·X·Z·AB·AD)* ÷ 10⁶ *(× −1 trừ GI)* — đo khớp
     GI 66/66 · OMC 60/60 · SC 54/54 · PS 51/54 ô; tháng ngoài MID3 *(GI M01 · OMC M01–02 · PS/SC M01–03)* =
     `sumifs(GROUP) × '[FS1]5. Daily Report 3'` *(PD 608 — đáp án bước sau)*. Hàng `TOTAL` ⛔ có trong ảnh MID3
     đóng băng *(44 hàng ⛔ vendor/tháng — ⛔ cột A)* và Σ PM CDT của engine AL.PLT ≠ `TOTAL` *(PM CDT = None ở
     vendor-tháng `P` chữ "Need to manual input")* ⇒ **cần ảnh**, ⛔ đoán.
  ③ `lech_D3` — ô hồi phục THÊM khi đổi driver By GI từ `PE` *(D3, AP DECIDED)* sang tỉ lệ AS-IS `GI khối / GI
     GROUP` *(và bật By GI từ 202501)* — phản thực; giữ D3, câu hỏi chủ ở BG.
  ④ còn lại = `lech_ngoai_ten` *(lệch FLS — mong 0)* ⇒ ĐỎ.
"""
from __future__ import annotations

import datetime
import hashlib
from collections import Counter
import dataclasses
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from fls.bao_cao import pla
from fls.bao_cao import phan_bo_khoa as pbk
from fls.bao_cao.cfa import KHOI_TONG
from fls.cau_hinh import luat_pb
from fls.cau_hinh.hd import CayHD
from fls.oracle.cong_parity import PhanXu
from tools import do_hd2_c3d as c3d
from tools.do_hd2 import GOC, _chu, _so, nap_anh

ANH_ATL = GOC / "tests" / "fixture" / "dap_an" / "atl.json"
ANH_DRV = GOC / "tests" / "fixture" / "cau_hinh" / "ix_drv.json"
ANH_MM = GOC / "tests" / "fixture" / "cau_hinh" / "mapping_master_cfg.json"
#: tệp KÝ bật cờ 2025 *(config có phiên bản — vòng sửa R1)*
TEP_KY = GOC / "tests" / "fixture" / "cau_hinh" / "ix_alr_2025_bat.json"
#: 4 sổ nền tảng *(MID3)* — mã = chữ đầu nhãn `luat_pb.NHAN_NEN_TANG` *(⛔ gõ lại)*
MA_NEN_TANG = tuple(n.split()[0] for n in luat_pb.NHAN_NEN_TANG)
THANG_2025 = tuple(f"2025M{m:02d}" for m in range(1, 13))
KHOI_CDT6 = tuple(c3d.KHOI_CDT)
KHOI_PB = frozenset(KHOI_CDT6) | {c3d.KHOI_DU}
ATOL = c3d.ATOL                                  # 1e-12, rtol 0 *(cùng WP-C3d — lưới vào là của H8)*
ATOL_604 = Decimal("1e-9")
#: tháng IX.ALR bắt đầu hiệu lực khi nạp vào kho test *(giá trị cấu hình người gọi khai)*. ⚠ CÙNG khoá `hd@202501`
#: với bài C11 *(`tests/cau_hinh/test_luat_pb_pg.py`)*: kho config TÍCH LUỸ *(`C11-R1-01`)* ⇒ nạp mốc KHÁC làm bài C11
#: chạy SAU thấy 34 luật *(đo 22/11: `--tu_ky 202410` ⇒ 2 bài C11 ĐỎ khi `tests/oracle` chạy trước `tests/cau_hinh`)*.
#: Cờ TẮT ⇒ mốc ⛔ đổi kết quả cổng *(đồng nhất)*.
TU_KY_ALR = 202501
_THANG = [f"m{m:02d}" for m in range(1, 13)]


# ── config ────────────────────────────────────────────────────────────────────────────────────────

def alr_tu_anh_mm(tu_ky: int = TU_KY_ALR) -> luat_pb.BangALR:
    """`BangALR` từ ảnh Mapping Master DT3 qua CHÍNH `luat_pb.dung_tu_mm` + `kiem` *(cùng đường `nap_ix_alr`;
    cho bài đơn vị ⛔ kho — cổng đọc kho bằng `doc_alr`)*."""
    anh = nap_anh(ANH_MM)
    mm = [{"hd_code": _chu(r.get("hd_code")), "need_cfa2": _chu(r.get("need_cfa2")),
           "method_cfa2": _chu(r.get("method_cfa2"))} for r in anh["dong"]]
    return luat_pb.kiem(luat_pb.dung_tu_mm(mm, tu_ky=tu_ky), nguon=ANH_MM.name)


def alr_ky_tu_anh(tu_ky: int = TU_KY_ALR) -> luat_pb.BangALR:
    """`BangALR` cờ BẬT = ảnh MM *(`alr_tu_anh_mm`)* + tệp ký qua CHÍNH `luat_pb.dung_tu_tep_ky` + `kiem` — cùng
    phép gộp của `cau_hinh_repo.ky_bat_ix_alr` *(dòng ký thắng cùng khoá)*; cho bài ⛔ kho."""
    hien = alr_tu_anh_mm(tu_ky)
    d = {luat_pb.khoa_cua(x.hd, x.tu_ky): {"hd": x.hd, "tu_ky": x.tu_ky, "nhan_mm": x.nhan_mm, "bat": x.bat,
                                           "ngoai_le": list(x.ngoai_le_cdt1)} for x in hien.luat}
    import json
    d.update((luat_pb.khoa_cua(r["hd"], r["tu_ky"]), r)
             for r in luat_pb.dung_tu_tep_ky(json.loads(TEP_KY.read_text(encoding="utf-8")), hien))
    return luat_pb.kiem(list(d.values()), nguon=f"{ANH_MM.name} + {TEP_KY.name}")


def luoi_driver_tu_anh(anh: Mapping[str, Any] | None = None) -> pbk.LuoiDriver:
    """Ảnh IX.DRV DT10 → `LuoiDriver`: 238 ô số + 146 ô thiếu CÓ TÊN *(bảng `o_thieu`)*."""
    anh = anh or nap_anh(ANH_DRV)
    o: dict[tuple[str, str, int], Decimal] = {}
    for r in anh["dong"]:
        nam = int(_so(r["nam"]))
        for i, c in enumerate(_THANG, start=1):
            v = _so(r.get(c))
            if v is not None:
                o[(_chu(r["driver"]), _chu(r["cdt1"]), nam * 100 + i)] = v
    thieu = {(_chu(x["driver"]), _chu(x["cdt1"]), int(_chu(x["thang"]))): _chu(x["ly_do"])
             for x in anh["phu"]["o_thieu"]["dong"]}
    return pbk.LuoiDriver(o=o, thieu=thieu)


def tham_chieu_604(anh_drv: Mapping[str, Any], anh_atl: Mapping[str, Any]) -> dict[str, Any]:
    """PD 604 *(tham chiếu)*: số CDT1 có số theo (driver, tháng) ở ATL `pd604_ky` ↔ lưới IX.DRV; Σ7 CDT1 = 1."""
    drv = luoi_driver_tu_anh(anh_drv)
    o_so = khop = 0
    lech: list[str] = []
    for r in anh_atl["phu"]["pd604_ky"]["dong"]:
        d = _chu(r["driver"])
        for i, c in enumerate(_THANG, start=1):
            o_so += 1
            n = sum(1 for (dd, _, t) in drv.o if dd == d and t == 202500 + i)
            if n == int(_so(r[c])):
                khop += 1
            else:
                lech.append(f"{d}|2025{i:02d}: drv {n} ≠ ATL {_so(r[c])}")
    tong: dict[tuple[str, int], Decimal] = {}
    for (d, _, t), v in drv.o.items():
        tong[(d, t)] = tong.get((d, t), Decimal(0)) + v
    sigma_lech = sorted(f"{d}|{t}" for (d, t), v in tong.items() if abs(v - 1) > ATOL_604)
    return {"o_so": o_so, "khop": khop, "lech": lech, "o_drv": len(drv.o), "o_thieu": len(drv.thieu),
            "sigma_7": len(tong), "sigma_7_lech": sigma_lech}


# ── ATL ──────────────────────────────────────────────────────────────────────────────────────────

def _ky(cot: str) -> str:
    nam, k = cot[1:].split("_")
    return nam if k == "y" else nam + k.upper()


def hang_atl(anh: Mapping[str, Any]) -> tuple[list[tuple[str, str, dict]], list[dict]]:
    """Hàng ATL → (khối, mã, hàng). Khối mở ở mỗi hàng nhãn `GI` theo thứ tự `KHOI_12`; hàng ⛔ nhãn tách riêng."""
    ra: list[tuple[str, str, dict]] = []
    khong_nhan: list[dict] = []
    i = -1
    for r in anh["dong"]:
        nhan = next((_chu(r[k]) for k in ("l1", "l2", "l3", "l4") if r.get(k)), None)
        if not nhan:
            khong_nhan.append(r)
            continue
        ma = nhan.split("|")[0].strip()
        if ma == "GI":
            i += 1
        if not 0 <= i < len(c3d.KHOI_12):
            raise ValueError(f"hàng sheet {r['dong_sheet']}: khối thứ {i + 1} ⛔ có trong KHOI_12 (Đ5)")
        ra.append((c3d.KHOI_12[i], ma, r))
    return ra, khong_nhan


@dataclass(frozen=True)
class MongC5a:
    so: Mapping[str, Any] | None = None


def mong_c5a_mac_dinh() -> MongC5a:
    from tools.do_hd2_c5a_mong import MONG
    return MongC5a(so=MONG)


@dataclass
class ThanhQuaC5a:
    so: dict[str, Any]
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    lech: list[dict[str, Any]] = field(default_factory=list)
    #: H13 *(WP-C5b)*: lưới ATL của FLS *(đầu ra AL.KEY)* + lớp của TỪNG ô lệch — để dòng PL THỪA KẾ nhãn từ lá
    o: Mapping[tuple[str, str, str], Decimal] = field(default_factory=dict)
    lop_o: dict[str, str] = field(default_factory=dict)


def _lop_2024(x: Mapping[str, str]) -> str | None:
    """Lớp H8 *(`BG-278`)*: lệch 416 dán cũ 2024 lan sang khối CDT ∪ {SHQ2}. Cờ ký chỉ hiệu lực 2025 ⇒ ô 2024 GIỮ
    NGUYÊN giữa cờ tắt/bật trừ `NPC` *(Σ hậu tố — bài `test_H12_R1_co_ky_2025__ky_ngoai_2025_dong_nhat…`)*: đếm 675
    y nguyên, sha đổi vì giá trị engine `NPC`."""
    kh, _, t = x["o"].split("#")
    return "as_is_truoc_CA" if kh in KHOI_PB and t[:4] == "2024" else None


def gia_tri_atl(atl: Mapping[str, Any]) -> dict[tuple[str, str, str], Decimal]:
    """Ô SỐ của ATL theo `(khối, mã, kỳ)` — chỉ cho bước SO và phép đo PHẢN THỰC *(⛔ đầu vào engine)*."""
    ra: dict[tuple[str, str, str], Decimal] = {}
    for kh, ma, r in hang_atl(atl)[0]:
        for c in atl["cot"]:
            if c[:1] == "y" and r.get(c) is not None:
                try:
                    ra[(kh, ma, _ky(c))] = Decimal(str(r[c]))
                except InvalidOperation:
                    pass
    return ra


def pla3_thay_la_nen_tang(pla3: pla.KetQuaPLA, atl_o: Mapping, cay: CayHD, *,
                          group_atl: bool = False) -> pla.KetQuaPLA:
    """PHẢN THỰC ② *(chẩn đoán — ⛔ đầu vào engine)*: lá tháng 2025 của `MA_NEN_TANG` ở 6 khối CDT := giá trị nguồn
    AS-IS *(đọc từ ATL — chính là ô cần đo)*, dư SHQ2 = GROUP − Σ CDT *(công thức ATL)*, cuộn lại Y/H/Q, tính lại
    cây/KPI. `group_atl` *(bước ②b)*: dư lấy GROUP của ATL *(mang lỗi gõ tay `o_lech` của GROUP — vd `OMC`
    2025-02 −0,5)* ⇒ ô chỉ hồi phục ở ②b là lỗi AS-IS LAN qua dư SHQ2, ⛔ thiếu đầu vào."""
    la = dict(pla3.la)
    co = set(pla3.cot)
    gop = {g for t in THANG_2025 for g in pbk.ky_gop(t)} & co
    for ma in MA_NEN_TANG:
        if pla3.loai.get(ma) != "la":
            continue
        for kh in KHOI_CDT6:
            for t in THANG_2025:
                if (kh, ma, t) in atl_o:
                    la[(kh, ma, t)] = atl_o[(kh, ma, t)]
        for t in THANG_2025:            # dư SHQ2 = GROUP − Σ CDT *(công thức SHQ2 2025 của ATL: `=R-SUMIFS(…)`)*
            g = atl_o.get((KHOI_TONG, ma, t), la[(KHOI_TONG, ma, t)]) if group_atl else la[(KHOI_TONG, ma, t)]
            la[(c3d.KHOI_DU, ma, t)] = g - sum((la[(k, ma, t)] for k in KHOI_CDT6), Decimal(0))
        for kh in (*KHOI_CDT6, c3d.KHOI_DU):
            for g in gop:
                la[(kh, ma, g)] = sum((la[(kh, ma, t)] for t in THANG_2025 if g in pbk.ky_gop(t)), Decimal(0))
    return dataclasses.replace(pla3, la=la, o=pla.danh_gia(la, cay, list(pla3.cot), tuple(pla3.khoi),
                                                           pla.CONG_THUC_PM))


def phan_thuc_D3(alr: luat_pb.BangALR, drv: pbk.LuoiDriver, atl_o: Mapping) -> tuple:
    """PHẢN THỰC ③ *(chẩn đoán)*: driver By GI := tỉ lệ AS-IS `GI khối / GI GROUP` *(công thức ATL
    `iferror(sumifs(GROUP) × (GI khối / sumifs GI GROUP))`)* thay `GI_PE` *(D3)*; By GI bật từ 202501 như AS-IS."""
    ten = pbk.DRIVER_LUOI[luat_pb.DRIVER_BY_GI]
    o = dict(drv.o)
    for t in THANG_2025:
        g = atl_o.get((KHOI_TONG, "GI", t))
        for kh in KHOI_CDT6:
            if g and (kh, "GI", t) in atl_o:
                o[(ten, kh, pbk.thang_cua(t))] = atl_o[(kh, "GI", t)] / g
    bat_gi = {x.hd: x for x in alr.luat if x.phuong_phap == luat_pb.BY_GI and x.bat}
    som = min(pbk.thang_cua(t) for t in THANG_2025)
    luat = [x for x in alr.luat if not (x.hd in bat_gi and x.tu_ky <= som)]
    luat += [dataclasses.replace(x, tu_ky=som) for x in bat_gi.values()]
    return luat_pb.BangALR(nguon=alr.nguon + " +phản thực D3", luat=tuple(luat)), \
        pbk.LuoiDriver(o=o, thieu=drv.thieu)


def _tom(ds: list[Mapping[str, str]]) -> dict[str, Any]:
    q = Decimal("1e-12")
    dem = Counter(x["o"].split("#")[0] for x in ds)
    chuoi = "\n".join(sorted(f"{x['o']}={Decimal(x['engine']).quantize(q)}|{Decimal(x['dap_an']).quantize(q)}"
                              for x in ds))
    return {"theo_khoi": dict(sorted(dem.items())), "so_o": len(ds),
            "sha256": hashlib.sha256(chuoi.encode()).hexdigest()}


def _khop_co_so(o: Mapping, hang: list, cot: list, loai: Mapping) -> int:
    """Ô khớp THẬT *(⛔ `0 = 0`)* của lưới `o` ↔ ATL — CÙNG định nghĩa `khop_co_so` của cổng *(để báo cờ tắt → bật)*."""
    n = 0
    for kh, ma, r in hang:
        if loai.get(ma) in (None, "trong"):
            continue
        for c in cot:
            v = r.get(c)
            try:
                a = Decimal(0) if v is None else Decimal(str(v))
            except InvalidOperation:
                continue
            e = o[(kh, ma, _ky(c))]
            n += not (e == 0 and a == 0) and abs(e - a) <= ATOL
    return n


def _pbk(p, alr, drv: pbk.LuoiDriver, cay: CayHD) -> pbk.KetQuaKhoa:
    return pbk.phan_bo_khoa(p, alr, cay, pla.CONG_THUC_PM, khoi_nguon=KHOI_TONG, khoi_cdt=KHOI_CDT6,
                            khoi_du=c3d.KHOI_DU, driver=drv)


def so_sanh_c5a(pla3: pla.KetQuaPLA, atl: Mapping[str, Any], drv: Mapping[str, Any], alr: Any, cay: CayHD,
                mong: MongC5a) -> ThanhQuaC5a:
    ly: list[str] = []
    luoi = luoi_driver_tu_anh(drv)
    try:
        kq = _pbk(pla3, alr, luoi, cay)
    except pbk.LoiPhanBoKhoa as e:
        px = PhanXu(False, (str(e),))
        return ThanhQuaC5a(so={}, phan_xu=px, hd2_cong={"bang": "HD2.WP-C5a", "goi": "WP-C5a", "dat": False,
                                                        "ly_do": list(px.ly_do)})
    hang, khong_nhan = hang_atl(atl)
    cot = [c for c in atl["cot"] if c[:1] == "y"]
    dem = Counter()
    theo_khoi: dict[str, Counter] = {}
    lech: list[dict[str, Any]] = []
    mx = Decimal(0)
    for kh, ma, r in hang:
        lo = pla3.loai.get(ma)
        if lo is None:
            dem["ma_ngoai_cay"] += 1
            continue
        if lo == "trong":
            dem["o_trong"] += len(cot)
            continue
        tk = theo_khoi.setdefault(kh, Counter())
        for c in cot:
            v = r.get(c)
            try:
                a = Decimal(0) if v is None else Decimal(str(v))
            except InvalidOperation:
                dem["khong_so_duoc"] += 1
                continue
            e = kq.o[(kh, ma, _ky(c))]
            dem["o_so"] += 1
            tk["o_so"] += 1
            if e == 0 and a == 0:
                dem["o_0_0"] += 1
                dem["khop"] += 1
            elif abs(e - a) <= ATOL:
                dem["khop"] += 1
                mx = max(mx, abs(e - a))
            else:
                tk["lech"] += 1
                lech.append({"o": f"{kh}#{ma}#{_ky(c)}", "engine": str(e), "dap_an": str(a)})
    dem["hang_so"] = len(hang)
    dem["hang_khong_nhan"] = len(khong_nhan)
    dem["hang_khong_nhan_khac_0"] = sum(1 for r in khong_nhan for c in cot if r.get(c) not in (None, "0"))
    t604 = tham_chieu_604(drv, atl)
    so: dict[str, Any] = {"dem": dict(dem), "theo_khoi": {k: dict(v) for k, v in theo_khoi.items()},
                          "tham_chieu_604": t604, "dem_phan_bo": kq.dem,
                          "max_lech_khop": str(mx)}
    # ── phán quyết ──
    m = mong.so
    if dem["o_so"] == 0:
        ly.append("0 ô được so ⇒ ⛔ đo được gì (Đ3)")
    if m is None:
        ly.append("`mong` chưa khai ⇒ ⛔ tin (Đ5)")
        m = {}
    lop_thuc = {"dem": dict(dem), "dem_phan_bo": kq.dem,
                "tham_chieu_604": {k: t604[k] for k in ("o_so", "khop", "o_drv", "o_thieu", "sigma_7")}}
    c3d._khac(lop_thuc, m.get("lop"), "lop", ly)
    if t604["lech"] or t604["sigma_7_lech"]:
        ly.append(f"tham chiếu 604 lệch: {t604['lech'][:5]} · Σ7≠1: {t604['sigma_7_lech'][:5]}")
    if not any(getattr(x, "bat", False) for x in getattr(alr, "luat", ())):
        ly.append("IX.ALR ⛔ có luật nào BẬT ⇒ ⛔ phải phiên bản KÝ 2025 (cổng đo ở cờ BẬT — vòng sửa R1)")
    mong_o = m.get("o_lech") or {}
    atol_lech = Decimal(str(m.get("atol_lech", "1e-9")))
    # ── PHẢN THỰC *(chẩn đoán gán nhãn — ⛔ đầu ra cổng)* ──
    atl_o = gia_tri_atl(atl)
    try:
        p2 = pla3_thay_la_nen_tang(pla3, atl_o, cay)
        e2 = _pbk(p2, alr, luoi, cay).o
        p2b = pla3_thay_la_nen_tang(pla3, atl_o, cay, group_atl=True)
        e2b = _pbk(p2b, alr, luoi, cay).o
        alr3, luoi3 = phan_thuc_D3(alr, luoi, atl_o)
        e3 = _pbk(p2b, alr3, luoi3, cay).o
    except (pbk.LoiPhanBoKhoa, luat_pb.LoiLuatPB) as e:
        ly.append(f"phản thực ⛔ chạy được ⇒ ⛔ gán nhãn được (Đ5): {e}")
        e2 = e2b = e3 = {}
    tung_o: list[dict[str, Any]] = []
    theo_lop: dict[str, list[dict[str, Any]]] = {"as_is_truoc_CA": [], "as_is_tay_lan_du": [],
                                                 "chua_co_dau_vao": [], "lech_D3": []}
    ngoai_ten: list[dict[str, Any]] = []

    def _hoi(e: Mapping, x: Mapping) -> bool:
        kh, ma, t = x["o"].split("#")
        v = e.get((kh, ma, t))
        return v is not None and abs(v - Decimal(x["dap_an"])) <= ATOL

    for x in lech:
        mg = mong_o.get(x["o"])
        if mg is not None and abs(Decimal(x["engine"]) - Decimal(mg[0])) <= atol_lech \
                and abs(Decimal(x["dap_an"]) - Decimal(mg[1])) <= atol_lech:
            tung_o.append(x)
        elif _lop_2024(x):
            theo_lop["as_is_truoc_CA"].append(x)
        elif _hoi(e2, x):
            theo_lop["chua_co_dau_vao"].append(x)
        elif _hoi(e2b, x):
            theo_lop["as_is_tay_lan_du"].append(x)
        elif _hoi(e3, x):
            theo_lop["lech_D3"].append(x)
        else:
            ngoai_ten.append(x)
    so["lop_do"] = {k: _tom(v) for k, v in theo_lop.items()}
    c3d._khac(so["lop_do"], m.get("lop_do"), "lop_do", ly)
    # lá khối CDT 2025 của 4 sổ nền tảng + mã có ngoại lệ (OFR) — khớp / chua_co_dau_vao THEO MÃ *(Đ4)*
    cdv = {x["o"] for x in theo_lop["chua_co_dau_vao"]}
    lech_o = {x["o"] for x in lech}
    ma_la = (*MA_NEN_TANG, *sorted({x.hd for x in getattr(alr, "luat", ()) if x.ngoai_le_cdt1}))
    so["la_cdt_2025"] = {ma: {"o": sum(1 for kh in KHOI_CDT6 for t in THANG_2025 if (kh, ma, t) in atl_o),
                              "khop": sum(1 for kh in KHOI_CDT6 for t in THANG_2025
                                          if (kh, ma, t) in atl_o and f"{kh}#{ma}#{t}" not in lech_o),
                              "chua_co_dau_vao": sum(1 for kh in KHOI_CDT6 for t in THANG_2025
                                                     if f"{kh}#{ma}#{t}" in cdv)} for ma in ma_la}
    c3d._khac(so["la_cdt_2025"], m.get("la_cdt_2025"), "la_cdt_2025", ly)
    # khớp THẬT ở cờ TẮT *(lưới vào — đồng nhất H12-B1)* để báo trước/sau
    so["khop_co_so_co_tat"] = _khop_co_so(pla3.o, hang, cot, pla3.loai)
    thay = {x["o"] for x in lech}
    for k in sorted(set(mong_o) - thay):
        ly.append(f"ô mong lệch `{k}` nay KHỚP ⇒ sửa bản khai (Đ5 chiều ngược)")
    for x in ngoai_ten[:20]:
        ly.append(f"ô lệch ngoài tên `{x['o']}`: engine {x['engine']} · ATL {x['dap_an']}")
    if len(ngoai_ten) > 20:
        ly.append(f"… +{len(ngoai_ten) - 20} ô lệch ngoài tên")
    co_chu_dich = len(tung_o) + sum(len(v) for v in theo_lop.values())
    so["loi_as_is"] = len(tung_o) + len(theo_lop["as_is_truoc_CA"]) + len(theo_lop["as_is_tay_lan_du"])
    so["lech_co_chu_dich"], so["lech_ngoai_ten"] = co_chu_dich, len(ngoai_ten)
    so["ngoai_ten_o"] = sorted(x["o"] for x in ngoai_ten)
    if m.get("tong_o") is not None and m["tong_o"] != dem["o_so"]:
        ly.append(f"mẫu số tong_o {dem['o_so']} ≠ mong {m['tong_o']}")
    px = PhanXu(not ly, tuple(ly))
    hd2 = {
        "bang": "HD2.WP-C5a", "goi": "WP-C5a",
        "mo_ta": "AL.KEY cờ IX.ALR BẬT 2025 (kho — phiên bản KÝ ix_alr_2025_bat.json, quyết của chủ 22/11) trên "
                 "lưới SO.PLA3 PM+HR Y/H/Q/M của H8 (đầu vào DT7b) ↔ ATL 606 (+ tham chiếu 604: lưới IX.DRV ↔ "
                 "pd604_ky); lớp lệch gán bằng PHÉP ĐO phản thực",
        "nguon_dau_vao": ["tests/fixture/dau_vao/gl_pl_dau_vao.json", "tests/fixture/dau_vao/hr_pl_dau_vao.json",
                          "tests/fixture/cau_hinh/ix_drv.json", "IX.ALR (kho) ← tests/fixture/cau_hinh/ix_alr_2025_bat.json"],
        "dap_an": ["tests/fixture/dap_an/atl.json"],
        "khoa": "khối (12) × mã (la+tong+kpi — ⛔ trong) × kỳ (57) của hàng ATL có nhãn",
        "dung_sai": {"atol": str(ATOL), "rtol": "0", "max_lech_khop": str(mx)},
        "tong_o": dem["o_so"], "mong_tong_o": m.get("tong_o"),
        "o_co_so": dem["o_so"] - dem["o_0_0"], "khop_co_so": dem["khop"] - dem["o_0_0"], "o_0_0": dem["o_0_0"],
        "khop": dem["khop"],
        "lech_co_chu_dich": co_chu_dich,
        "mong_lech_co_chu_dich": len(mong_o) + sum((v or {}).get("so_o", 0)
                                                   for v in (m.get("lop_do") or {}).values()),
        "khop_co_so_co_tat": so["khop_co_so_co_tat"], "loi_as_is": so["loi_as_is"],
        "la_cdt_2025": so["la_cdt_2025"],
        "lech_ngoai_ten": len(ngoai_ten),
        "khop_ghi_chu": "tong_o = ô so (hàng ATL có nhãn, mã ⛔ trong, ô là số) = o_co_so + o_0_0; khop = ô khớp "
                        "THẬT; khop + lech_co_chu_dich = tong_o",
        "lech_co_ten": {"o_lech": sorted(x["o"] for x in tung_o), **so["lop_do"],
                        "khong_so_duoc": dem["khong_so_duoc"], "o_trong": dem["o_trong"],
                        "hang_khong_nhan_khac_0": dem["hang_khong_nhan_khac_0"]},
        "theo_khoi": so["theo_khoi"],
        "tham_chieu_604": {k: t604[k] for k in ("o_so", "khop", "o_drv", "o_thieu", "sigma_7")},
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    lop_o = {x["o"]: "loi_as_is" for x in tung_o}
    for k, v in theo_lop.items():
        lop_o.update({x["o"]: ("loi_as_is" if k in ("as_is_truoc_CA", "as_is_tay_lan_du") else k) for x in v})
    lop_o.update({x["o"]: "lech_FLS" for x in ngoai_ten})
    return ThanhQuaC5a(so=so, phan_xu=px, hd2_cong=hd2, lech=lech, o=kq.o, lop_o=lop_o)


def nap_nguon() -> tuple:
    return (*c3d.nap_nguon(), nap_anh(ANH_ATL), nap_anh(ANH_DRV))


def tinh_pla3(gl, hr, fx, cay, lich, den) -> pla.KetQuaPLA:
    luoi, _ = c3d.tinh_luoi(gl, hr, fx, cay, lich, den, [])
    return luoi["pla3_pm_hr_yhqm"]


def _alr_tu_kho(dsn: str | None, conn=None):
    try:
        from fls.repo import cau_hinh_repo as chc
        if conn is not None:
            return chc.doc_alr(conn), None
        import psycopg
        from fls.db.kho import dsn_that
        with psycopg.connect(dsn or dsn_that()) as c:
            return chc.doc_alr(c), None
    except Exception as e:  # noqa: BLE001 — Đ5: ⛔ đo được ⇒ ĐỎ có lý do
        return None, f"IX.ALR ⛔ đọc được từ kho: {type(e).__name__}: {' '.join(str(e).split())}"


def _lich_tu_conn(conn):
    try:
        from fls.repo import cau_hinh_repo as chc
        return chc.doc_per(conn), None
    except Exception as e:  # noqa: BLE001
        return None, f"IX.PER ⛔ đọc được từ kho: {type(e).__name__}: {' '.join(str(e).split())}"


def chay_wp_c5a(dsn: str | None = None, conn=None) -> ThanhQuaC5a:
    """`conn` *(tuỳ chọn)*: đọc IX.PER + IX.ALR qua kết nối người gọi *(bài chạy trong giao dịch rollback —
    kho config TÍCH LUỸ, ⛔ để lại bản ký cho bài C11)*."""
    lich, loi = _lich_tu_conn(conn) if conn is not None else c3d._lich_tu_kho(dsn)
    alr, loi2 = _alr_tu_kho(dsn, conn)
    if lich is None or alr is None:
        px = PhanXu(False, tuple(x for x in (loi, loi2) if x))
        return ThanhQuaC5a(so={}, phan_xu=px, hd2_cong={"bang": "HD2.WP-C5a", "goi": "WP-C5a", "dat": False,
                                                        "ly_do": list(px.ly_do)})
    gl, hr, _, fx, cay, atl, drv = nap_nguon()
    den = datetime.date.fromisoformat(c3d.mong_c3d_mac_dinh().so["den"])
    return so_sanh_c5a(tinh_pla3(gl, hr, fx, cay, lich, den), atl, drv, alr, cay, mong_c5a_mac_dinh())


def in_bao(tq: ThanhQuaC5a) -> None:
    h = tq.hd2_cong
    print("══ WP-C5a · AL.KEY cờ BẬT 2025 (kho, phiên bản ký) ↔ ATL 606 (+ 604)")
    if "tong_o" in h:
        print(f"  ô so {h['tong_o']} = có số {h['o_co_so']} + 0=0 {h['o_0_0']} · khớp {h['khop']} "
              f"(thật {h['khop_co_so']}/{h['o_co_so']}) · lệch có chủ đích {h['lech_co_chu_dich']} · "
              f"ngoài tên {h['lech_ngoai_ten']} · khong_so_duoc {h['lech_co_ten']['khong_so_duoc']}")
        print(f"  khớp thật cờ TẮT {h['khop_co_so_co_tat']} → cờ BẬT {h['khop_co_so']} / {h['o_co_so']}")
        lt = h["lech_co_ten"]
        print(f"  lớp: loi_as_is {h['loi_as_is']} (o_lech {len(lt['o_lech'])} + as_is_truoc_CA "
              f"{lt['as_is_truoc_CA']['so_o']} + as_is_tay_lan_du {lt['as_is_tay_lan_du']['so_o']}) · chua_co_dau_vao {lt['chua_co_dau_vao']['so_o']} · "
              f"lech_D3 {lt['lech_D3']['so_o']} · lệch FLS {h['lech_ngoai_ten']}")
        print(f"  lá CDT 2025: {h['la_cdt_2025']}")
        print(f"  604: {h['tham_chieu_604']}")
    for x in h.get("ly_do", []):
        print(f"  ⛔ {x}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")
