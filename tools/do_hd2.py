"""`do_hd2.py --goi WP-C2` — PARITY CA.GL ↔ đáp án 406 mọi kỳ *(ISP 3.1.2 · Step 13 · H4)*.

    python tools/do_hd2.py --goi WP-C2            # chạy cổng, in báo, exit 0/1
    python tools/do_hd2.py --goi WP-C2 --ghi      # … + ghi docs/ITL/_tools/hd2_cong.json

⭐ **Vì sao có tệp này** *(AP v3.1.2 §3.5.4 WP-C2 · HD2; WO-132)*. H4 là cổng HD2 ĐẦU TIÊN: chạy
engine `fls.bao_cao.gl.tinh_gl` *(H1)* trên **dòng sổ THẬT** *(tiền nguyên tệ `E`/`F` đọc từ sheet
406, đóng băng ở `gl_406_dau_vao.json`)* + tỷ giá `ix_fx.json` *(qua `fls.cau_hinh.fx` — ⛔ đọc kho,
I2)*, rồi so TỪNG Ô 8 cột `BM…BT` với đáp án `gl_406.json` *(DT4)* ở mọi kỳ có dữ liệu.

── Vì sao NGUỒN đầu vào là ĐỘC LẬP, ⛔ tái dựng từ `BO`/`BP` *(orchestrator 18/11)* ──────────────
Tái dựng Nợ/Có từ `BO`/`BP` của đáp án là VÒNG TRÒN *(hai cột ấy tự khớp)*. Nguồn độc lập = cột
ĐẦU VÀO `D·E·F` của chính sheet 406 — tiền NGUYÊN TỆ mà công thức `AX…BT` dùng. Nhờ vậy `BO`/`BP`
ở đây là phép kiểm THẬT. Repo ⛔ có ảnh nào mang `E`/`F` *(O10: cột PS Nợ/Có bị bỏ)* ⇒ H4 thêm một
khuôn DATA `gl_406_dau_vao` *(đóng băng SA chỉ-đọc A·D·E·F·R; ⛔ phủ B:C)*.

── SỐ DƯ ĐẦU KỲ gõ tay *(5 ô hàng 24 — `SoDuDau`)* ──────────────────────────────────────────────
AS-IS gõ CỨNG số dư đầu kỳ ở hàng 24 *(R-chẩn orchestrator: quét công thức `AX10:BT7892` = 181.263
ô, ĐÚNG 5 ô lệch khuôn CALC_ZONE, cả 5 ở hàng 24)* ⇒ `BM·BN·BQ·BT` của đáp án chênh ~56.84e9 bVND ·
~2.2677 mUSD so với H1 thuần TỪ ds24 *(đo độc lập 18/11 TRƯỚC khi biết công thức — đúng từng đồng)*.
H4 GIEO 5 hằng ấy *(đọc từ `gl_406_dau_vao.json` → `phu.so_du_dau`)* vào engine qua tham số TƯỜNG
MINH `tinh_gl(..., so_du_dau=…)` ⇒ cả 8 cột về 0 trong dung sai. FLS CHƯA có khái niệm số dư đầu kỳ
— nguồn chính thức là câu hỏi cho BA/owner *(errata ⑳)*; `hd2_cong.json` + BG khai rõ.

── LỆCH CÓ TÊN *(Đ5: khai MONG trước; khác ⇒ ĐỎ CẢ HAI CHIỀU)* ─────────────────────────────────
  · `thieu_tien_te_D` — **6 hàng** thiếu `D` *(ds 4962·4963·6073·6507·6949·7631)* ⇒ AS-IS INDEX/
    MATCH ⛔ khớp tiền tệ ⇒ `BO`/`BP` RỖNG; FLS ⛔ dựng được dòng *(tiền tệ ngoài 5 cột)* ⇒ bỏ khỏi
    phép so, đếm có tên. Dòng ấy là **no-op** cho tồn luỹ kế AS-IS *(AX…BL = "" cả hàng)* ⇒ bỏ ⛔
    làm lệch dòng sau *(đo 18/11: ds10…23 khớp đúng, 6 dòng này ở sau)*.
  · `itl_id_na` — **4 hàng** `itl_id = "#N/A ()"` *(ds 6684·6836·7500·7832)* ⇒ nối 406 ↔ sổ bằng
    `dong_sheet` *(⛔ bằng itl_id)*; vẫn SO được *(có `D`/`E`/`F`)*, chỉ khai tên.
  · `ky_vang_406` — kỳ sổ *(`itl_ledge_adjustment.json` 9967 dòng)* vượt bản sao 406: `2026-05`
    239/537 · `2026-06`·`07`·`08` vắng ⇒ ⛔ có ô để so, đếm có tên *(⛔ lỗi)*.
  · `thang_thieu_ty_gia` — HAI ngữ nghĩa tra tỷ giá *(INDEX/MATCH ⇒ ô rỗng · SUMIFS ⇒ 0/`#DIV/0!`;
    `CALC_ZONE_406.md`)*: tháng của dòng ⛔ có trong `ix_fx` ⇒ `tinh_gl` ném `ThieuTyGia`. Đo 18/11:
    `ix_fx` phủ 202401…202612 ⇒ **0** tháng thiếu trong dải 406 *(Đ3: khai mẫu số `mau_so_thang`)*.

⛔ Mọi lệch NGOÀI bốn tên trên ⇒ cổng ĐỎ. Mẫu số 0 ô ⇒ ĐỎ *(Đ3)*. `hd2_cong.json` = hợp đồng cho
`CG2` *(Step 30)*: khai khoá rõ ràng, CHỈ THÊM về sau.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

GOC = Path(__file__).resolve().parents[1]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.bao_cao.gl import DongGL, SoDuDau, ThieuTyGia, TienTeNgoaiGL, tinh_gl  # noqa: E402
from fls.cau_hinh import fx as cfx  # noqa: E402
from fls.canon.tien_te import ma_tien_te  # noqa: E402
from fls.oracle.cong_parity import PhanXu, danh_gia  # noqa: E402

GOI_BIET = ("WP-C2",)
COT_BMBT = ("BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT")
#: ô kết quả → thuộc tính `KetQuaDongGL`.
ATTR = {"BM": "vnd_ton_all", "BN": "musd_ton_all", "BO": "bvnd_no", "BP": "bvnd_co",
        "BQ": "bvnd_ton", "BR": "musd_no", "BS": "musd_co", "BT": "musd_ton"}

ANH_DAU_VAO = GOC / "tests" / "fixture" / "dap_an" / "gl_406_dau_vao.json"
ANH_DAP_AN = GOC / "tests" / "fixture" / "dap_an" / "gl_406.json"
IX_FX = GOC / "tests" / "fixture" / "cau_hinh" / "ix_fx.json"
ADJ = GOC / "tests" / "fixture" / "itl_ledge_adjustment.json"
RA_CONG = GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json"

#: Tháng đầu dải IX.FX *(AP §3.2.1: sổ bắt đầu 2024; dòng lạc 202306 < đây)*.
THANG_DAU_FX = 202401

# ── MONG lệch có tên *(đo 18/11; Đ5 — khai TRƯỚC kết quả)* ────────────────────────
MONG_THIEU_D = (4962, 4963, 6073, 6507, 6949, 7631)
MONG_ITL_NA = (6684, 6836, 7500, 7832)
MONG_KY_VANG = {202605: 239, 202606: 0, 202607: 0, 202608: 0}
MONG_THANG_THIEU_TY_GIA: tuple[int, ...] = ()        # ix_fx phủ cả dải ⇒ 0 (Đ3: mẫu số khai riêng)

# ── MONG mẫu số *(H4-R1-02 · Đ2/Đ5: khai TRƯỚC cả TỬ lẫn MẪU — cổng ⛔ tự đếm rồi tự so)* ──
MONG_DONG_SO = 7877                  #: dòng sổ vào engine = 7883 − 6 hàng thiếu D (Đ4)
MONG_TONG_O = 8 * MONG_DONG_SO       #: 63.016 = 8 cột BM…BT × dòng feed
MONG_SO_DONG_DAP_AN = 7883           #: số hàng đáp án 406 (hàng 10…7892) — bắt xoá/nhân đôi hàng


@dataclass(frozen=True)
class DungSaiCot:
    """Dung sai số thực *(IEEE-754 ↔ `Decimal`)* cho MỘT cột. `khop` = `|got-exp| ≤ atol+rtol·|exp|`.

    ⭐ **`atol` THEO CỘT, có căn cứ ĐO** *(H4-R1-01; Đ5 — khai ngưỡng kèm số đo biên)*. R1 chỉ ra
    `atol 1e-6` chung là ngưỡng thật của 7/8 cột, rộng **~10⁶×** lệch thật *(đột biến `BO +9e-7` lọt)*
    — và câu *"BT theo độ lớn lũy kế (rtol)"* SAI: chỉ **BM** *(VND ~1e11)* mới do `rtol` canh;
    `BT≈2,3` ⇒ `rtol·|BT|≈2e-9 ≪ atol` nên BT do `atol` quyết định.
    """
    atol: Decimal
    rtol: Decimal = Decimal("1e-9")      # theo độ lớn — chỉ CẮN ở BM (~1e11); sàn vô hại cho cột nhỏ

    def khop(self, got: Decimal, exp: Decimal) -> bool:
        return abs(got - exp) <= self.atol + self.rtol * abs(exp)


# ── Dung sai THEO CỘT — đo 18/11 trên 7.877 dòng (so engine ↔ đáp án, KHÔNG áp dung sai) ──────────
#   cột  đơn vị          max|lệch| thật   max rel      ngưỡng atol   biên atol/noise
#   BM   VND  ~2,98e11    3,14e-04 (ulp)   1,60e-13    1e-3*         rtol 1e-9 canh (≈57 VND ở đuôi)
#   BN   mUSD ~11,5       1,22e-14         1,60e-13    1e-12         ×82
#   BO   bVND ~115,6      1,00e-14         3,03e-16    1e-12         ×100   ← đột biến +9e-7 (900 VND)
#   BP   bVND ~128,9      1,27e-14         2,38e-16    1e-12         ×79
#   BQ   bVND ~296,3      1,09e-12         3,19e-12    1e-11         ×9     (cộng dồn — noise sát 1e-12)
#   BR   mUSD ~4,5        1,00e-15         3,38e-16    1e-12         ×1000
#   BS   mUSD ~5,1        1,00e-15         3,72e-16    1e-12         ×1000
#   BT   mUSD ~11,5       7,35e-14         2,04e-12    1e-12         ×14    (cộng dồn)
#   * BM: |exp| ≥ 6e7 luôn ⇒ `rtol·|exp| ≥ 0,06 ≫ noise ulp 3,1e-4`; atol 1e-3 chỉ là sàn gần-0.
# Chứng ĐỎ (Đ5): `atol 1e-6` cũ ⇒ `BO +9e-7` XANH; dung sai này ⇒ `BO +9e-7` và `BO +1 VND` ĐỎ.
DUNG_SAI_COT: dict[str, DungSaiCot] = {
    "BM": DungSaiCot(atol=Decimal("1e-3")),
    "BN": DungSaiCot(atol=Decimal("1e-12")),
    "BO": DungSaiCot(atol=Decimal("1e-12")),
    "BP": DungSaiCot(atol=Decimal("1e-12")),
    "BQ": DungSaiCot(atol=Decimal("1e-11")),
    "BR": DungSaiCot(atol=Decimal("1e-12")),
    "BS": DungSaiCot(atol=Decimal("1e-12")),
    "BT": DungSaiCot(atol=Decimal("1e-12")),
}


def dung_sai_mac_dinh() -> dict[str, DungSaiCot]:
    return dict(DUNG_SAI_COT)


@dataclass(frozen=True)
class Mong:
    """Khai TRƯỚC *(Đ5)*: tập lệch-có-tên mong đợi + dung sai THEO CỘT + MẪU SỐ mong.

    Thực ≠ mong ⇒ ĐỎ cả hai chiều. `mong_tong_o`/`mong_dong_so`/`mong_so_dong_dap_an` = None ⇒ ⛔
    khoá mẫu số *(cho ảnh nhỏ B2/B3)*; `mong_mac_dinh()` khoá đủ ba cho ảnh thật *(H4-R1-02)*.
    """
    thieu_D: tuple[int, ...]
    itl_na: tuple[int, ...]
    ky_vang: Mapping[int, int]
    thang_thieu_ty_gia: tuple[int, ...]
    dung_sai: Mapping[str, DungSaiCot] = field(default_factory=dung_sai_mac_dinh)
    mong_dong_so: int | None = None            # dòng sổ vào engine (Đ4)
    mong_tong_o: int | None = None             # 8 × dòng feed — mẫu số parity
    mong_so_dong_dap_an: int | None = None     # số hàng đáp án 406


def mong_mac_dinh() -> Mong:
    return Mong(thieu_D=MONG_THIEU_D, itl_na=MONG_ITL_NA, ky_vang=dict(MONG_KY_VANG),
               thang_thieu_ty_gia=MONG_THANG_THIEU_TY_GIA, dung_sai=dung_sai_mac_dinh(),
               mong_dong_so=MONG_DONG_SO, mong_tong_o=MONG_TONG_O,
               mong_so_dong_dap_an=MONG_SO_DONG_DAP_AN)


@dataclass
class ThanhQua:
    tong_o: int
    khop: int
    so_o_dap_an_so_duoc: int
    lech: list[dict[str, Any]]
    lech_co_ten: dict[str, list]
    mau_so_thang: int
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    so_dong_dap_an: int = 0            #: số hàng đáp án (bắt xoá/nhân đôi — H4-R1-02)
    o_dap_an_bo: int = 0               #: ô đáp án khác rỗng của 6 hàng thiếu D, BỎ khỏi so (H4-R1-03)
    no_op_lech: list[int] = field(default_factory=list)  #: hàng thiếu D mà BM·BQ·BT ≠ hàng trên


# ── đọc ô ảnh ────────────────────────────────────────────────────────────────────

def _chu(v: Any) -> str | None:
    if v is None:
        return None
    if isinstance(v, dict):
        return v.get("chu")
    return str(v)


def _so(v: Any) -> Decimal | None:
    """Ô ảnh *(chuỗi số, `{chu}`, hay None)* → `Decimal` hữu hạn, hoặc None nếu rỗng."""
    if v is None:
        return None
    s = v["chu"] if isinstance(v, dict) else str(v)
    if s is None or s == "":
        return None
    return Decimal(s)


# ── nạp ──────────────────────────────────────────────────────────────────────────

def nap_anh(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def nap_fx(path: Path = IX_FX) -> dict[int, dict[str, Decimal]]:
    """`ix_fx.json` *(ảnh DT2)* → `{int yyyymm: {tiền tệ: Decimal}}` QUA `fls.cau_hinh.fx.kiem`
    *(C1 — validate tỷ giá; ⛔ đọc kho, I2)*. Khoá nguồn là `Month` *(chuỗi 6 chữ số)*."""
    j = json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal)
    dong = [{"yyyymm": int(r["Month"]), **{c: r[c] for c in cfx.TIEN_TE}} for r in j["dong"]]
    bang = cfx.kiem(dong, thang_dau=THANG_DAU_FX, nguon=str(path.name))
    return {d.yyyymm: dict(d.ty_gia) for d in bang.ky}


def nap_phan_bo(path: Path = ADJ) -> dict[int, int]:
    j = json.loads(path.read_text(encoding="utf-8"))
    ra: dict[int, int] = {}
    for k, v in j["phan_bo_ky"].items():
        nam, thang = k.split("-")
        ra[int(nam) * 100 + int(thang)] = int(v)
    return ra


def _doc_seed(anh_dau_vao: dict) -> dict[int, SoDuDau]:
    """`phu.so_du_dau` → `{dong_sheet: SoDuDau}` *(gộp các ô cùng hàng)*."""
    hang = anh_dau_vao.get("phu", {}).get("so_du_dau", {}).get("dong", [])
    gom: dict[int, dict[str, Any]] = {}
    for o in hang:
        ds = int(_so(o["ds"]))
        g = gom.setdefault(ds, {"ton": {}, "bvnd": Decimal(0), "musd": Decimal(0)})
        vao = _chu(o["vao"])
        hs = _so(o["hang_so"])
        if vao == "ton":
            tt = _chu(o["tien_te"])
            g["ton"][tt] = g["ton"].get(tt, Decimal(0)) + hs
        elif vao == "bvnd_ton":
            g["bvnd"] += hs
        elif vao == "musd_ton":
            g["musd"] += hs
    return {ds: SoDuDau(ton_them=g["ton"], bvnd_ton_them=g["bvnd"], musd_ton_them=g["musd"])
            for ds, g in gom.items()}


# ── so sánh ──────────────────────────────────────────────────────────────────────

def so_sanh(anh_dau_vao: dict, anh_dap_an: dict, fx: Mapping[int, Mapping[str, Decimal]],
            phan_bo_ky: Mapping[int, int], mong: Mong) -> ThanhQua:
    """So TỪNG Ô 8 cột `BM…BT`: chạy `tinh_gl` trên `E`/`F` *(ảnh đầu vào, gieo số dư đầu kỳ)*,
    nối với đáp án bằng `dong_sheet`. Trả `ThanhQua` *(⛔ ghi gì)*."""
    ds = mong.dung_sai
    seed_theo_ds = _doc_seed(anh_dau_vao)

    # ── dựng feed: bỏ hàng thiếu D (lệch có tên no-op), giữ THỨ TỰ dòng ──
    thieu_D: list[int] = []
    feed: list[DongGL] = []
    feed_ds: list[int] = []
    for r in anh_dau_vao["dong"]:
        dsn = int(_so(r["dong_sheet"]))
        tt = _chu(r.get("D"))
        if tt is None or tt == "":
            thieu_D.append(dsn)
            continue
        feed.append(DongGL(thang=int(_so(r["ky"])), tien_te=tt,
                           no=(_so(r.get("E")) or Decimal(0)),
                           co=(_so(r.get("F")) or Decimal(0))))
        feed_ds.append(dsn)

    # ── tháng thiếu tỷ giá *(HAI ngữ nghĩa — CALC_ZONE)*: tháng của feed ⛔ có trong fx ──
    thang_feed = {int(_so(r["ky"])) for r in anh_dau_vao["dong"]}
    thang_thieu = sorted(t for t in thang_feed if t not in fx)
    mau_so_thang = len(thang_feed & set(fx))        # Đ3: mẫu số = số tháng ĐÃ phủ

    # ── gieo số dư đầu kỳ theo VỊ TRÍ dòng trong feed ──
    vi_tri_theo_ds = {d: i + 1 for i, d in enumerate(feed_ds)}
    so_du_dau = {vi_tri_theo_ds[dsn]: sd for dsn, sd in seed_theo_ds.items()
                 if dsn in vi_tri_theo_ds}

    # ── chạy engine ──
    loi_engine: str | None = None
    kq = []
    try:
        kq = tinh_gl(feed, fx, so_du_dau=so_du_dau)
    except (ThieuTyGia, TienTeNgoaiGL) as e:        # Đ3/Đ5: ⛔ đo được ⇒ ĐỎ
        loi_engine = f"{type(e).__name__}: {' '.join(str(e).split())}"

    # ── so từng ô với đáp án (nối dong_sheet) ──
    da_theo_ds = {int(_so(r["dong_sheet"])): r for r in anh_dap_an["dong"]}
    so_dong_dap_an = len(anh_dap_an["dong"])              # H4-R1-02: bắt xoá/thừa/nhân đôi hàng
    tong_o = khop = so_o_dap_an_so_duoc = 0
    lech: list[dict[str, Any]] = []
    for dsn, k in zip(feed_ds, kq):
        a = da_theo_ds.get(dsn)
        if a is None:
            continue
        for c in COT_BMBT:
            exp = _so(a.get(c))
            if exp is None:
                continue
            so_o_dap_an_so_duoc += 1
            tong_o += 1
            got = getattr(k, ATTR[c])
            if ds[c].khop(got, exp):                      # dung sai THEO CỘT (H4-R1-01)
                khop += 1
            else:
                lech.append({"dong_sheet": dsn, "ky": _chu(a.get("ky")), "cot": c,
                             "exp": str(exp), "got": str(got),
                             "lech": str(got - exp)})

    # ── H4-R1-03: ô đáp án BỎ (6 hàng thiếu D) phải ĐẾM ĐƯỢC + no-op phải ĐO được ──
    #   mỗi hàng thiếu D vẫn có 6 ô đáp án khác rỗng (BM·BN·BQ·BR·BS·BT) ⇒ 36 ô bỏ khỏi so.
    o_dap_an_bo = sum(1 for dsn in thieu_D
                      for c in COT_BMBT
                      if (a := da_theo_ds.get(dsn)) is not None and _so(a.get(c)) is not None)
    #   no-op (AS-IS AX…BL rỗng cả hàng): tồn luỹ kế BM·BQ·BT PHẢI bằng y hàng trên (ds−1).
    no_op_lech: list[int] = []
    for dsn in sorted(thieu_D):
        a, truoc = da_theo_ds.get(dsn), da_theo_ds.get(dsn - 1)
        if a is None or truoc is None:
            no_op_lech.append(dsn)                        # ⛔ đo được ⇒ coi là lệch
            continue
        if any(_so(a.get(c)) != _so(truoc.get(c)) for c in ("BM", "BQ", "BT")):
            no_op_lech.append(dsn)

    # ── lệch có tên ──
    itl_na = sorted(int(_so(o["dong_sheet"]))
                    for o in anh_dau_vao.get("phu", {}).get("itl_id_lech", {}).get("dong", []))
    ky_vang = sorted(k for k, n in phan_bo_ky.items()
                     if sum(1 for r in anh_dap_an["dong"] if int(_so(r["ky"])) == k) < n)
    lech_co_ten = {
        "thieu_tien_te_D": sorted(thieu_D),
        "itl_id_na": itl_na,
        "ky_vang_406": [str(k) for k in ky_vang],
        "thang_thieu_ty_gia": [str(t) for t in thang_thieu],
    }

    # ── phân xử *(cong_parity + khớp MONG cả hai chiều)* ──
    px = _phan_xu(tong_o, khop, len(feed_ds), lech, lech_co_ten, mong, loi_engine,
                  so_dong_dap_an, no_op_lech)

    hd2_cong = _hop_dong(tong_o, khop, so_o_dap_an_so_duoc, lech, lech_co_ten, mau_so_thang,
                         len(feed_ds), ds, px, so_dong_dap_an, o_dap_an_bo, no_op_lech)
    return ThanhQua(tong_o=tong_o, khop=khop, so_o_dap_an_so_duoc=so_o_dap_an_so_duoc,
                    lech=lech, lech_co_ten=lech_co_ten, mau_so_thang=mau_so_thang,
                    phan_xu=px, hd2_cong=hd2_cong, so_dong_dap_an=so_dong_dap_an,
                    o_dap_an_bo=o_dap_an_bo, no_op_lech=no_op_lech)


def _phan_xu(tong_o: int, khop: int, dong_doc: int, lech: list, lech_co_ten: dict,
             mong: Mong, loi_engine: str | None, so_dong_dap_an: int,
             no_op_lech: list[int]) -> PhanXu:
    # lõi: ≥1 ô · ⛔ lát bỏ · 0 ô lệch *(cong_parity — toi_thieu_o=1 theo AC-1 "số ô > 0")*
    px = danh_gia(tong_o=tong_o, khop=khop, lat_truot=0, dong_doc=dong_doc,
                  dong_mong_doi=dong_doc, toi_thieu_o=1)
    ly = list(px.ly_do)
    if loi_engine is not None:
        ly.append(f"engine ⛔ chạy được *(⛔ đo được ⇒ ĐỎ)*: {loi_engine}")
    # ── H4-R1-02: MẪU SỐ khai TRƯỚC — tử (tong_o) lẫn mẫu (dòng feed · hàng đáp án) ⇒ ĐỎ nếu lệch ──
    if mong.mong_dong_so is not None and dong_doc != mong.mong_dong_so:
        ly.append(f"dòng sổ vào engine {dong_doc} ≠ mong {mong.mong_dong_so}")
    if mong.mong_tong_o is not None and tong_o != mong.mong_tong_o:
        ly.append(f"mẫu số ô so {tong_o} ≠ mong {mong.mong_tong_o} "
                  f"(= 8 × {mong.mong_dong_so} dòng feed)")
    if mong.mong_so_dong_dap_an is not None and so_dong_dap_an != mong.mong_so_dong_dap_an:
        ly.append(f"số hàng đáp án {so_dong_dap_an} ≠ mong {mong.mong_so_dong_dap_an} "
                  f"(xoá/thừa/nhân đôi hàng)")
    # ── H4-R1-03: no-op của 6 hàng thiếu D phải ĐO được (BM·BQ·BT = hàng trên), lệch ⇒ ĐỎ ──
    if no_op_lech:
        ly.append(f"hàng thiếu D ⛔ no-op (BM·BQ·BT ≠ hàng trên): {sorted(no_op_lech)}")
    # Đ5: tập lệch-có-tên THỰC ≠ MONG ⇒ ĐỎ cả hai chiều
    for ten, thuc, mg in (
            ("thieu_tien_te_D", lech_co_ten["thieu_tien_te_D"], sorted(mong.thieu_D)),
            ("itl_id_na", lech_co_ten["itl_id_na"], sorted(mong.itl_na)),
            ("ky_vang_406", sorted(int(x) for x in lech_co_ten["ky_vang_406"]),
             sorted(mong.ky_vang)),
            ("thang_thieu_ty_gia", sorted(int(x) for x in lech_co_ten["thang_thieu_ty_gia"]),
             sorted(mong.thang_thieu_ty_gia))):
        if list(thuc) != list(mg):
            thieu = sorted(set(mg) - set(thuc))
            thua = sorted(set(thuc) - set(mg))
            ly.append(f"lệch có tên `{ten}` ≠ mong: thiếu {thieu} · thừa {thua}")
    return PhanXu(not ly, tuple(ly))


def _hop_dong(tong_o, khop, so_o_dap_an, lech, lech_co_ten, mau_so_thang, dong_so,
              ds: Mapping[str, DungSaiCot], px: PhanXu, so_dong_dap_an: int,
              o_dap_an_bo: int, no_op_lech: list[int]) -> dict[str, Any]:
    """Hợp đồng `hd2_cong.json` cho `CG2` *(Step 30)* — khai khoá RÕ, chỉ THÊM về sau."""
    return {
        "bang": "HD2.WP-C2",
        "goi": "WP-C2",
        "mo_ta": "parity CA.GL (tinh_gl trên E/F + ix_fx, gieo số dư đầu kỳ hàng 24) ↔ đáp án 406 "
                 "BM…BT, nối dong_sheet",
        "khoa": "dong_sheet + cot(BM…BT)",
        "cot_so": list(COT_BMBT),
        # H4-R1-01: dung sai THEO CỘT (atol có căn cứ đo; rtol 1e-9 chỉ cắn ở BM ~1e11).
        "dung_sai_theo_cot": {c: {"atol": str(ds[c].atol), "rtol": str(ds[c].rtol)}
                              for c in COT_BMBT},
        "dung_sai_ghi_chu": "atol THEO CỘT = ~10× noise đo 18/11 (BM: VND 1e11 ⇒ rtol 1e-9 canh, "
                            "atol 1e-3 là sàn gần-0; BQ: 1e-11 vì cộng dồn; 6 cột khác 1e-12). "
                            "Chứng ĐỎ: BO +9e-7 (900 VND) ⇒ lệch; atol 1e-6 cũ ⇒ XANH.",
        "dong_so": dong_so,
        "mong_dong_so": MONG_DONG_SO,
        "tong_o": tong_o,
        "mong_tong_o": MONG_TONG_O,                 # H4-R1-02: mẫu số = hằng khai TRƯỚC, ⛔ tự đếm
        "so_dong_dap_an": so_dong_dap_an,
        "mong_so_dong_dap_an": MONG_SO_DONG_DAP_AN,
        "khop": khop,
        "so_o_dap_an_so_duoc": so_o_dap_an,
        "lech_ngoai_ten": len(lech),
        "lech_co_ten": {k: len(v) for k, v in lech_co_ten.items()},
        "lech_co_ten_chi_tiet": lech_co_ten,
        "mau_so_thang": mau_so_thang,
        # H4-R1-03: ô đáp án BỎ (6 hàng thiếu D × 6 ô khác rỗng = 36) đếm được + no-op đã đo.
        "o_dap_an_bo_hang_thieu_D": o_dap_an_bo,
        "no_op_hang_thieu_D": {"kiem": "BM·BQ·BT[ds] == [ds−1]", "lech": sorted(no_op_lech)},
        "so_du_dau": "5 ô gõ tay hàng 24 (errata ⑳: FLS chưa có khái niệm số dư đầu kỳ; nguồn "
                     "chính thức = câu hỏi BA/owner) — gieo qua tinh_gl(so_du_dau=…)",
        "dat": px.dat,
        "ly_do": list(px.ly_do),
    }


# ── chạy thật + CLI ───────────────────────────────────────────────────────────────

def chay_wp_c2() -> ThanhQua:
    """Chạy WP-C2 trên ẢNH THẬT trong repo."""
    return so_sanh(nap_anh(ANH_DAU_VAO), nap_anh(ANH_DAP_AN), nap_fx(), nap_phan_bo(),
                   mong_mac_dinh())


def _in_bao(tq: ThanhQua) -> None:
    print("══ do_hd2 · WP-C2 — parity CA.GL ↔ đáp án 406 (BM…BT)")
    print(f"  dòng sổ so    : {tq.hd2_cong['dong_so']} dòng (bỏ {len(tq.lech_co_ten['thieu_tien_te_D'])} "
          f"hàng thiếu D)")
    print(f"  ô so / khớp   : {tq.khop}/{tq.tong_o}  (mẫu số mong {MONG_TONG_O} = 8 × {MONG_DONG_SO}; "
          f"= số ô đáp án so được {tq.so_o_dap_an_so_duoc})")
    print(f"  hàng đáp án   : {tq.so_dong_dap_an} (mong {MONG_SO_DONG_DAP_AN})")
    print(f"  ô đáp án bỏ   : {tq.o_dap_an_bo} (6 hàng thiếu D × 6 ô khác rỗng — H4-R1-03; "
          f"no-op lệch: {tq.no_op_lech})")
    print(f"  ô lệch ngoài tên: {len(tq.lech)}")
    for x in tq.lech[:10]:
        print(f"      [ds {x['dong_sheet']} · {x['ky']} · {x['cot']}] exp {x['exp']} got {x['got']}")
    print("  lệch có tên:")
    for k, v in tq.lech_co_ten.items():
        print(f"      {k}: {len(v)} {v[:8]}")
    print(f"  tháng phủ fx  : {tq.mau_so_thang} (mẫu số — Đ3)")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="do_hd2.py", description="Cổng parity HD2.")
    p.add_argument("--goi", required=True, choices=GOI_BIET, help="gói cổng HD2")
    p.add_argument("--ghi", action="store_true", help="ghi docs/ITL/_tools/hd2_cong.json")
    a = p.parse_args(argv)
    tq = chay_wp_c2()
    _in_bao(tq)
    if a.ghi:
        RA_CONG.parent.mkdir(parents=True, exist_ok=True)
        RA_CONG.write_text(json.dumps(tq.hd2_cong, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
        print(f"  ghi: {RA_CONG.relative_to(GOC)}")
    return 0 if tq.phan_xu.dat else 1


if __name__ == "__main__":
    raise SystemExit(main())
