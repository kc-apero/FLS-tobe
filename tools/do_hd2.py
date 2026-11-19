"""`do_hd2.py --goi WP-C2 | WP-C3a | WP-C3b | WP-C4a | WP-C4b` — PARITY HD2: CA.GL ↔ 406 *(H4)* · SO.CFA1 Daily ↔ 409 *(H5)* · Y/H/Q/M ↔ 410 *(H6)*.

    python tools/do_hd2.py --goi WP-C2            # chạy cổng, in báo, exit 0/1
    python tools/do_hd2.py --goi WP-C2 --ghi      # … + ghi docs/ITL/_tools/hd2_cong.json
    python tools/do_hd2.py --goi WP-C3a [--ghi]   # H5 · SO.CFA1 Daily ↔ 409 (khối WP-C3a — xem dưới)
    python tools/do_hd2.py --goi WP-C3b [--ghi]   # H6 · Y/H/Q/M ↔ 410; IX.PER đọc TỪ KHO (PG_DSN)

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
import dataclasses
import datetime
import json
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

GOC = Path(__file__).resolve().parents[1]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from fls.bao_cao.cfa import KHOI_TONG, DongCFA, cfa1_daily, cuon_ky, truc_ngay  # noqa: E402
from fls.bao_cao.gl import DongGL, SoDuDau, ThieuTyGia, TienTeNgoaiGL, tinh_gl  # noqa: E402
from fls.cau_hinh import fx as cfx  # noqa: E402
from fls.cau_hinh import hd as hd_cfg  # noqa: E402
from fls.cau_hinh.hd import CayHD  # noqa: E402
from fls.cau_hinh.ky import LichKy  # noqa: E402
from fls.canon.tien_te import ma_tien_te  # noqa: E402
from fls.oracle.cong_parity import PhanXu, danh_gia  # noqa: E402

GOI_BIET = ("WP-C2", "WP-C3a", "WP-C3b", "WP-C4a", "WP-C4b")
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
MONG_O_DAP_AN_BO = 36                #: ô đáp án khác rỗng của 6 hàng thiếu D (6×6) — KHOÁ (H4-R2-02)


@dataclass(frozen=True)
class DungSaiCot:
    """Dung sai số thực *(IEEE-754 ↔ `Decimal`)* cho MỘT cột. `khop` = `|got-exp| ≤ atol+rtol·|exp|`.

    ⭐ **`atol` THEO CỘT, có căn cứ ĐO** *(H4-R1-01; Đ5 — khai ngưỡng kèm số đo biên)*. R1 chỉ ra
    `atol 1e-6` chung là ngưỡng thật của 7/8 cột, rộng **~10⁶×** lệch thật *(đột biến `BO +9e-7` lọt)*
    — và câu *"BT theo độ lớn lũy kế (rtol)"* SAI: chỉ **BM** *(VND ~1e11)* mới do `rtol` canh;
    `BT≈2,3` ⇒ `rtol·|BT|≈2e-9 ≪ atol` nên BT do `atol` quyết định.
    """
    atol: Decimal
    rtol: Decimal = Decimal("1e-9")      # MẶC ĐỊNH = rtol CŨ (chung 1e-9); DUNG_SAI_COT khai THEO CỘT (H4-R2-01)

    def khop(self, got: Decimal, exp: Decimal) -> bool:
        return abs(got - exp) <= self.atol + self.rtol * abs(exp)


# ── Dung sai THEO CỘT — đo 18/11 trên 7.877 dòng (so engine ↔ đáp án, KHÔNG áp dung sai) ──────────
# Lệch engine↔đáp án là CỐ ĐỊNH (chạy 2 lần cùng kết — xác định; khác-triển-khai Excel↔Python, ⛔
# noise ngẫu nhiên BLAS). Hai knob, cả hai CÓ ĐO: `atol` = sàn tuyệt đối (ôm max|lệch| cộng dồn);
# `rtol` = sàn tương đối theo độ lớn (ôm max rel). ⭐ **H4-R2-01**: `rtol` CŨ chung `1e-9` rộng
# **≥ 10⁴×** noise đo (rel max 1,6e-13) ⇒ BM lọt `+50 VND`, đuôi BO lỏng tới `1,16e-7`; `atol` của
# BQ/BT thành mã chết vì `rtol·|exp| ≫ atol`. Hạ `rtol` THEO CỘT = ~10–40× max rel đo (biên in cạnh).
#   cột  đơn vị        max|lệch|      max rel     atol(sàn 0)  rtol MỚI   biên rtol/rel  knob CẮN
#   BM   VND  ~2,98e11  3,14e-04 ulp   1,60e-13    1e-3         2e-12      ×12,5          rtol (|exp|~1e11)
#   BN   mUSD ~11,5     1,22e-14       1,60e-13    1e-12        2e-12      ×12,5          rtol (≥|exp|~0,5)
#   BO   bVND ~115,6    1,00e-14       3,03e-16    1e-12        1e-14      ×33            rtol (≥|exp|~100)
#   BP   bVND ~128,9    1,27e-14       2,38e-16    1e-12        1e-14      ×42            rtol (≥|exp|~100)
#   BQ   bVND ~296,3    1,09e-12       3,19e-12    1e-11        4e-11      ×12,5          atol+rtol (cộng dồn)
#   BR   mUSD ~4,5      1,00e-15       3,38e-16    1e-12        1e-14      ×29,6          atol (|exp|≤4,5)
#   BS   mUSD ~5,1      1,00e-15       3,72e-16    1e-12        1e-14      ×26,9          atol (|exp|≤5,1)
#   BT   mUSD ~11,5     7,35e-14       2,04e-12    1e-12        4e-11      ×19,6          atol+rtol (cộng dồn)
# BR/BS: |exp| quá nhỏ ⇒ `rtol·|exp| < atol` ⇒ knob thật là `atol` (noise tuyệt đối < atol); rtol chỉ
# sàn tương đối phụ. Chứng ĐỎ (Đ5): `rtol 1e-9` cũ ⇒ `BM +50 VND` · `BQ +1e-9` XANH; dung sai này ⇒
# `BM +1 VND` ĐỎ (tol đuôi ~0,6 VND) · `BQ +1e-9` ĐỎ ở hàng |BQ| nhỏ (tol ~atol 1e-11); `BO +9e-7` ĐỎ.
DUNG_SAI_COT: dict[str, DungSaiCot] = {
    "BM": DungSaiCot(atol=Decimal("1e-3"), rtol=Decimal("2e-12")),
    "BN": DungSaiCot(atol=Decimal("1e-12"), rtol=Decimal("2e-12")),
    "BO": DungSaiCot(atol=Decimal("1e-12"), rtol=Decimal("1e-14")),
    "BP": DungSaiCot(atol=Decimal("1e-12"), rtol=Decimal("1e-14")),
    "BQ": DungSaiCot(atol=Decimal("1e-11"), rtol=Decimal("4e-11")),
    "BR": DungSaiCot(atol=Decimal("1e-12"), rtol=Decimal("1e-14")),
    "BS": DungSaiCot(atol=Decimal("1e-12"), rtol=Decimal("1e-14")),
    "BT": DungSaiCot(atol=Decimal("1e-12"), rtol=Decimal("4e-11")),
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
    mong_o_dap_an_bo: int | None = None        # ô đáp án bỏ (6 hàng thiếu D) — khoá (H4-R2-02)


def mong_mac_dinh() -> Mong:
    return Mong(thieu_D=MONG_THIEU_D, itl_na=MONG_ITL_NA, ky_vang=dict(MONG_KY_VANG),
               thang_thieu_ty_gia=MONG_THANG_THIEU_TY_GIA, dung_sai=dung_sai_mac_dinh(),
               mong_dong_so=MONG_DONG_SO, mong_tong_o=MONG_TONG_O,
               mong_so_dong_dap_an=MONG_SO_DONG_DAP_AN, mong_o_dap_an_bo=MONG_O_DAP_AN_BO)


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
                  so_dong_dap_an, no_op_lech, o_dap_an_bo)

    hd2_cong = _hop_dong(tong_o, khop, so_o_dap_an_so_duoc, lech, lech_co_ten, mau_so_thang,
                         len(feed_ds), ds, px, so_dong_dap_an, o_dap_an_bo, no_op_lech)
    return ThanhQua(tong_o=tong_o, khop=khop, so_o_dap_an_so_duoc=so_o_dap_an_so_duoc,
                    lech=lech, lech_co_ten=lech_co_ten, mau_so_thang=mau_so_thang,
                    phan_xu=px, hd2_cong=hd2_cong, so_dong_dap_an=so_dong_dap_an,
                    o_dap_an_bo=o_dap_an_bo, no_op_lech=no_op_lech)


def _phan_xu(tong_o: int, khop: int, dong_doc: int, lech: list, lech_co_ten: dict,
             mong: Mong, loi_engine: str | None, so_dong_dap_an: int,
             no_op_lech: list[int], o_dap_an_bo: int) -> PhanXu:
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
    # ── H4-R2-02: ô đáp án BỎ (6 hàng thiếu D × 6 ô khác rỗng = 36) khai TRƯỚC — con số in phải có mong ──
    if mong.mong_o_dap_an_bo is not None and o_dap_an_bo != mong.mong_o_dap_an_bo:
        ly.append(f"ô đáp án bỏ (6 hàng thiếu D) {o_dap_an_bo} ≠ mong {mong.mong_o_dap_an_bo}")
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
        "dung_sai_ghi_chu": "atol = sàn tuyệt đối (ôm max|lệch| cộng dồn); rtol THEO CỘT = ~10–40× "
                            "max rel đo 18/11 (H4-R2-01: hạ từ 1e-9 chung — BM·BN 2e-12 · "
                            "BO·BP·BR·BS 1e-14 · BQ·BT 4e-11). Chứng ĐỎ: rtol cũ 1e-9 ⇒ BM +50 VND · "
                            "BQ +1e-9 XANH; rtol này ⇒ BM +1 VND · BQ +1e-9 ĐỎ; BO +9e-7 ĐỎ, "
                            "atol 1e-6 cũ ⇒ XANH.",
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
        "mong_o_dap_an_bo": MONG_O_DAP_AN_BO,       # H4-R2-02: con số in ra phải khai mong (Đ5)
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
    print(f"  ô đáp án bỏ   : {tq.o_dap_an_bo} (mong {MONG_O_DAP_AN_BO}; 6 hàng thiếu D × 6 ô khác "
          f"rỗng — H4-R1-03/R2-02; no-op lệch: {tq.no_op_lech})")
    print(f"  ô lệch ngoài tên: {len(tq.lech)}")
    for x in tq.lech[:10]:
        print(f"      [ds {x['dong_sheet']} · {x['ky']} · {x['cot']}] exp {x['exp']} got {x['got']}")
    print("  lệch có tên:")
    for k, v in tq.lech_co_ten.items():
        print(f"      {k}: {len(v)} {v[:8]}")
    print(f"  tháng phủ fx  : {tq.mau_so_thang} (mẫu số — Đ3)")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")


# ══════════════════════════════════════════════════════════════════════════════════
# WP-C3a — SO.CFA1 Daily ↔ đáp án 409 từng ô *(ISP 3.1.2 · Step 16 · H5 · WO-164)*
# ══════════════════════════════════════════════════════════════════════════════════
# ⭐ Nguồn ĐẦU VÀO *(errata ㉓; orchestrator đọc công thức SA 18/11)*: SUMIFS của `Report I CFA1
# Daily` đọc `Report I General Ledger` CỦA BẢN SAO CF report *(⛔ bản sao 406 của H4)* — ô lá GROUP
# = Σ BR − Σ BS theo (ngày A, nhãn V); khối LE thêm `P = mã LE`; hàng cha `=sum(con)`. Ảnh đầu vào
# `gl_cf_dau_vao.json` *(A·D·E·F·P·R·V, ⛔ B:C·G)*. BR/BS do `tinh_gl` tính lại từ E/F + `ix_fx`
# *(⛔ đọc BR/BS của sheet — vòng tròn)*; cộng theo cây do `fls.bao_cao.cfa.cfa1_daily`. Đáp án 409
# CHỈ cấp giá trị mong. ⭐ Trục ngày lấy từ IX.PER ĐỌC TỪ KHO *(H6 · H6-R1-02)* như WP-C3b, ⛔ từ
# `phu.ngay_truc` của đáp án.
# ⛔ Số dư đầu kỳ *(5 ô hàng 24 của H4)* KHÔNG dùng: CFA1 Daily là PHÁT SINH theo ngày *(BR/BS
# từng dòng)*, ⛔ tồn luỹ kế — `tinh_gl` gọi KHÔNG `so_du_dau` ⇒ BR/BS ⛔ đổi.

ANH_GL_CF = GOC / "tests" / "fixture" / "dap_an" / "gl_cf_dau_vao.json"
ANH_CFA1 = GOC / "tests" / "fixture" / "dap_an" / "cfa1_daily.json"
ATL_CAY = GOC / "tests" / "fixture" / "cau_hinh" / "atl_cay.json"

#: 5 khối của đáp án 409, thứ tự sheet *(khối 1 = Σ mọi dòng)*.
KHOI_CFA1 = (KHOI_TONG, "SGO2", "SGO1", "HGO6", "BGO2")

#: Hàng KPI — công thức CHÉO hàng *(đọc FORMULA khối GROUP `F53:H93` 18/11)*, ⛔ "lá = SUMIFS" ⛔
#: "cha = Σ con theo cây": `EBITDA=H8+H9+H23` · `EBIT` · `EBT` · `NP` · `NPC=sum(H67:67)` *(luỹ kế)* ·
#: `NCF=H70+H73+H76` · `NCFO/NCFI/NCFF=sum(con)` nhưng con là KPI *(`CRO=H8` · `COO=H9+H23+…` ·
#: `COI=H34` · `CRF=H44+H45` · `COF=H46`)* · `PL2…PL8` *(trừ PL5 — hàng TRỐNG)*. 20 mã × 5 khối × 760
#: ngày = 76.000 ô LOẠI khỏi phép so, ĐẾM có tên *(việc của bước sau — ⛔ H5)*. Hàng TRỐNG *(AR ·
#: CP1.1 (PL2) · CP1.2 · CP2 · CP3 · CFO · PL5)* VẪN so: engine 0 ↔ đáp án 0/vắng.
MA_KPI = ("EBITDA", "EBIT", "EBT", "NP", "NPC", "NCF", "NCFO", "CRO", "COO", "NCFI", "COI",
          "NCFF", "CRF", "COF", "PL2", "PL3", "PL4", "PL6", "PL7", "PL8")

# ── MONG *(đo 18/11 — Đ5: khai TRƯỚC; khác ⇒ ĐỎ cả hai chiều)* ──────────────────────────
MONG_C3A_SO_DONG_ANH = 12385          #: dòng ảnh gl_cf_dau_vao (hàng 10…12394)
MONG_C3A_THIEU_D = (4957, 4958, 6068, 6502, 6944, 7626, 8026, 8593, 8649, 8999, 9071, 9380)
MONG_C3A_DONG_SO = MONG_C3A_SO_DONG_ANH - len(MONG_C3A_THIEU_D)   #: 12.373 dòng vào tinh_gl
#: nhãn V ⛔ khớp nút nào *(kể cả bỏ hoa thường)* ⇒ AS-IS SUMIFS cũng ⛔ cộng — dòng rơi, CÓ TÊN.
#: WO-226: 162 → **9** — 153 dòng `ITE | ITE Interest` (152) + `… ` cách cuối (1) nay vào nút `ITE` nhờ
#: bảng alias `hd_cfg.ALIAS_NHAN_HD` (khai ở `MONG_C3A_HD_ALIAS`); 9 còn lại GIỮ NGUYÊN.
MONG_C3A_HD_NGOAI_CAY = {"Server Cost": 7, "GAC - Other": 1, "<rỗng>": 1}
#: dòng sổ vào nút nhờ alias *(nhãn nguồn nguyên văn → số dòng)* — 153 = 152 + 1 *(Đ4: số DÒNG, ⛔ số ô)*.
MONG_C3A_HD_ALIAS = {"ITE | ITE Interest": 152, "ITE | ITE Interest ": 1}
MONG_C3A_HD_KHAC_HOA = 5               #: 4 `oga | GAC - Other` ⇒ OGA + 1 `ofR | Office Rental Cost` ⇒ OFR (SUMIFS ⛔ phân biệt hoa thường)
#: ⭐ WO-226 AC-3 · Ô LỆCH ĐÁP ÁN CÓ CHỦ ĐÍCH `lech_co_chu_dich_ite` *(Đ4: đếm Ô của lưới, ⛔ dòng sổ)*:
#: ô khác nhau giữa lưới CÓ alias và lưới KHÔNG alias *(= ô alias chạm tới)* VÀ ≠ đáp án. AS-IS bỏ sót
#: lãi ITE nên đáp án = 0 ở các ô này; FLS cố ý ≠. Σ mUSD = Σ (got − exp) ở khối GROUP ≈ 0,01197 *(WO-226
#: đo 19/11: ≈ 0,01197 mUSD ròng)*; `tong_musd_moi_khoi` gồm cả khối LE.
MONG_LECH_ITE_C3A = {
    "so_o": 35, "theo_khoi": {"BGO2": 1, "GROUP": 26, "SGO2": 8}, "ma": ["ITE"],
    "ngay_dau": "2025-02-24", "ngay_cuoi": "2026-10-31", "so_cot_ngay": 26,
    "tong_musd_group": "0.011973111599", "tong_musd_moi_khoi": "0.023567965790"}
#: C3b: 42 ô = 24 kỳ × khối. Σ mUSD GROUP 0,047892… = 4 × 0,011973 *(mỗi dòng sổ rơi vào 4 cấp kỳ chồng
#: nhau Y · H · Q · M — Đ4: Σ ô, ⛔ số tiền ròng; số tiền ròng = `tong_musd_group` của C3a)*.
MONG_LECH_ITE_C3B = {
    "so_o": 42, "theo_khoi": {"BGO2": 4, "GROUP": 24, "SGO2": 14}, "ma": ["ITE"],
    "ky_dau": "2025", "ky_cuoi": "2026Q4", "so_ky": 24,
    "tong_musd_group": "0.047892446397", "tong_musd_moi_khoi": "0.094271863160"}
MONG_C3A_SO_NGAY = 760                 #: cột ngày ≤ ngày đọc 2026-11-18
MONG_C3A_NGAY_DAU = 45585              #: 2024-10-20 — errata ㉑ (⛔ 21/10 của spec)
#: errata ㉑: đáp án 409 có THÊM 1 cột TRƯỚC ngày đầu IX.PER *(C6 lưu 21/10, 409 bắt đầu 20/10)*. Khai
#: ở đây như MONG *(⛔ đọc từ đáp án)*: cột đầu trục C3a = `IX.PER.ngay_dau` − 1; đổi IX.PER ⇒ cột đầu
#: đổi ⇒ lệch `MONG_C3A_NGAY_DAU` ⇒ ĐỎ.
C3A_NGAY_TRUOC_PER = 1
MONG_C3A_NGAY_SO_CUOI = 46337          #: 2026-11-11 — dòng sổ cuối ⇒ 7 cột cuối "chưa có số"
MONG_C3A_SO_DONG_DAP_AN = 33355        #: ô ≠ 0 của đáp án (dòng chính thưa)
MONG_C3A_O_LOI = 25                    #: ô "-" của đáp án (phu.o_loi) — LOẠI khỏi so, đếm
MONG_C3A_O_KPI = 5 * len(MA_KPI) * MONG_C3A_SO_NGAY                       #: 76.000
MONG_C3A_TONG_O = 5 * (74 - len(MA_KPI)) * MONG_C3A_SO_NGAY - MONG_C3A_O_LOI   #: 205.175

# ── Dung sai THEO KHỐI *(lá · cha)* — đo 18/11 trên 205.175 ô, KHÔNG áp dung sai ─────────────
#   khối  ô       max|lệch|   max|exp|   max rel (exp≠0)   atol      biên
#   la    178.575 1,0e-15     6,07       1,0 (exp ~1e-15)  1e-14     ×10
#   cha    26.600 7,51e-16    3,32       7,4e-15           1e-14     ×13
# `rtol = 0`: |exp| ≤ 6,1 ⇒ `atol` là knob duy nhất; rel max 1,0 ở ô exp ~1e-15 *(sai số cộng của
# Sheets)* ⇒ rtol vô nghĩa. Chứng ĐỎ: +1 VND một dòng *(≈4e-11 mUSD)* ⇒ ĐỎ lá + mọi cha
# *(bài AC-3)*; +1e-12 một ô đáp án ⇒ ĐỎ đúng ô ấy *(bài Đ5)*.
DO_C3A_MAX_LECH = {"la": Decimal("1.0e-15"), "cha": Decimal("7.6e-16")}
DUNG_SAI_C3A: dict[str, DungSaiCot] = {
    "la": DungSaiCot(atol=Decimal("1e-14"), rtol=Decimal(0)),
    "cha": DungSaiCot(atol=Decimal("1e-14"), rtol=Decimal(0)),
}


@dataclass(frozen=True)
class MongC3a:
    thieu_D: tuple[int, ...]
    hd_ngoai_cay: Mapping[str, int]
    hd_khac_hoa: int
    dong_nhan_cha: int = 0
    dong_ngoai_truc: int = 0
    dong_so: int | None = None
    so_dong_anh: int | None = None
    tong_o: int | None = None
    o_kpi: int | None = None
    o_loi: int | None = None
    so_dong_dap_an: int | None = None
    so_ngay: int | None = None
    ngay_dau: int | None = None
    ngay_so_cuoi: int | None = None
    hd_alias: Mapping[str, int] | None = None
    lech_ite: Mapping[str, Any] | None = None


def mong_c3a_mac_dinh() -> MongC3a:
    return MongC3a(thieu_D=MONG_C3A_THIEU_D, hd_ngoai_cay=dict(MONG_C3A_HD_NGOAI_CAY),
                   hd_khac_hoa=MONG_C3A_HD_KHAC_HOA, dong_so=MONG_C3A_DONG_SO,
                   so_dong_anh=MONG_C3A_SO_DONG_ANH, tong_o=MONG_C3A_TONG_O, o_kpi=MONG_C3A_O_KPI,
                   o_loi=MONG_C3A_O_LOI, so_dong_dap_an=MONG_C3A_SO_DONG_DAP_AN,
                   so_ngay=MONG_C3A_SO_NGAY, ngay_dau=MONG_C3A_NGAY_DAU,
                   ngay_so_cuoi=MONG_C3A_NGAY_SO_CUOI, hd_alias=dict(MONG_C3A_HD_ALIAS),
                   lech_ite=dict(MONG_LECH_ITE_C3A))


@dataclass
class ThanhQuaC3a:
    tong_o: int
    khop: int
    lech: list[dict[str, Any]]
    lech_co_ten: dict[str, Any]
    o_kpi: int
    o_loi: int
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    luoi: dict[tuple[str, str, int], Decimal]
    lech_ite: list[dict[str, Any]] = field(default_factory=list)   #: WO-226 — ô lệch CÓ CHỦ ĐÍCH
    khop_dap_an: int = 0                                          #: ô khớp đáp án THUẦN (⛔ cộng lệch ITE)


def nap_cay(path: Path = ATL_CAY) -> CayHD:
    """Cây IX.HD *(ảnh ATL của C4 — qua `fls.cau_hinh.hd.doc_van_ban`, kiểm cha–con)*."""
    return hd_cfg.doc_van_ban(path.read_text(encoding="utf-8"), nguon=path.name)


def _iso(serial: int) -> str:
    return (datetime.date(1899, 12, 30) + datetime.timedelta(days=serial)).isoformat()


_Q12 = Decimal("1e-12")


def _o_chiu_alias(co: Mapping[Any, Decimal], khong: Mapping[Any, Decimal]) -> set:
    """Ô mà bảng alias làm ĐỔI giá trị *(lưới CÓ alias ≠ lưới KHÔNG alias — cùng dòng, cùng trục)*."""
    return {k for k, v in co.items() if v != khong[k]}


def _tom_tat_lech_ite(lech_ite: list[dict[str, Any]], tr: str, dinh_dang) -> dict[str, Any]:
    """`lech_co_chu_dich_ite`: số ô · theo khối · mã · khoảng ngày/kỳ · Σ mUSD *(GROUP · mọi khối)*."""
    cot = sorted({x[tr] for x in lech_ite})
    q = lambda d: str(d.quantize(_Q12))  # noqa: E731
    return {
        "so_o": len(lech_ite),
        "theo_khoi": {k: sum(1 for x in lech_ite if x["le"] == k)
                      for k in sorted({x["le"] for x in lech_ite})},
        "ma": sorted({x["ma"] for x in lech_ite}),
        ("ngay_dau" if tr == "ngay" else "ky_dau"): dinh_dang(cot[0]) if cot else None,
        ("ngay_cuoi" if tr == "ngay" else "ky_cuoi"): dinh_dang(cot[-1]) if cot else None,
        ("so_cot_ngay" if tr == "ngay" else "so_ky"): len(cot),
        "tong_musd_group": q(sum((Decimal(x["lech"]) for x in lech_ite if x["le"] == KHOI_TONG),
                                 Decimal(0))),
        "tong_musd_moi_khoi": q(sum((Decimal(x["lech"]) for x in lech_ite), Decimal(0))),
    }


def _dem_alias(kq, meta) -> dict[str, int]:
    """Dòng sổ vào nút nhờ alias: nhãn nguồn NGUYÊN VĂN *(kể cả khoảng trắng cuối)* → số dòng."""
    r: dict[str, int] = {}
    for i in kq.dong_alias:
        r[meta[i][2]] = r.get(meta[i][2], 0) + 1
    return r


def _so_mong_ite(thuc: dict[str, Any], mong: Mapping[str, Any] | None) -> list[str]:
    """Đ5 hai chiều: `lech_co_chu_dich_ite` thực ↔ MONG *(từng khoá; mong `None` ⇒ ĐỎ, ⛔ bỏ qua)*."""
    if mong is None:
        return ["lech_co_chu_dich_ite ⛔ khai mong"]
    return [f"lech_co_chu_dich_ite.{k} {thuc.get(k)!r} ≠ mong {mong.get(k)!r}"
            for k in sorted(set(thuc) | set(mong)) if thuc.get(k) != mong.get(k)]


def so_sanh_c3a(anh_vao: dict, anh_dap_an: dict, fx: Mapping[int, Mapping[str, Decimal]],
                cay: CayHD, lich: LichKy, mong: MongC3a) -> ThanhQuaC3a:
    """Dòng sổ CF → `tinh_gl` *(BR/BS)* → `cfa1_daily` *(lá + cây)* → so TỪNG Ô với đáp án 409."""
    ly: list[str] = []
    # ── 1 · feed tinh_gl (bỏ dòng thiếu D — lệch có tên, ⛔ quy đổi được) ──
    thieu_D: list[int] = []
    feed: list[DongGL] = []
    meta: list[tuple[int, str | None, str | None]] = []
    for r in anh_vao["dong"]:
        ds, ngay = int(_so(r["dong_sheet"])), int(_so(r["ngay"]))
        tt = _chu(r.get("D"))
        if not tt:
            thieu_D.append(ds)
            continue
        d = datetime.date(1899, 12, 30) + datetime.timedelta(days=ngay)
        feed.append(DongGL(thang=d.year * 100 + d.month, tien_te=tt,
                           no=(_so(r.get("E")) or Decimal(0)), co=(_so(r.get("F")) or Decimal(0))))
        meta.append((ngay, _chu(r.get("le")), _chu(r.get("hd_final"))))
    kq_gl = []
    try:
        kq_gl = tinh_gl(feed, fx)                          # ⛔ so_du_dau: CFA1 là phát sinh
    except (ThieuTyGia, TienTeNgoaiGL) as e:
        ly.append(f"tinh_gl ⛔ chạy được *(⛔ đo được ⇒ ĐỎ)*: {type(e).__name__}: "
                  f"{' '.join(str(e).split())}")
    dong_cfa = [DongCFA(ngay=n, le=le, hd=h, musd_no=k.musd_no, musd_co=k.musd_co)
                for (n, le, h), k in zip(meta, kq_gl)]

    # ── 2 · trục ngày: IX.PER (kho) + 1 cột errata ㉑, đến ngày đọc của ẢNH ĐẦU VÀO *(⛔ đáp án 409)* ──
    den = datetime.date.fromisoformat(str(anh_vao["ngay_dong_bang"]))
    dau = lich.ngay_dau - datetime.timedelta(days=C3A_NGAY_TRUOC_PER)
    truc = truc_ngay(dataclasses.replace(lich, ngay_dau=dau), den) if den >= dau else []
    if not truc:
        ly.append(f"trục ngày IX.PER ⛔ rỗng: ngày đọc {den} < cột đầu {dau}")

    # ── 3 · engine ──
    kq = cfa1_daily(dong_cfa, cay, ngay=truc, khoi=KHOI_CFA1, alias=hd_cfg.ALIAS_NHAN_HD)
    luoi = kq.o
    chiu_alias = _o_chiu_alias(luoi, cfa1_daily(dong_cfa, cay, ngay=truc, khoi=KHOI_CFA1).o)

    # ── 4 · đáp án ──
    ch = lambda v: _chu(v)  # noqa: E731
    exp: dict[tuple[str, str, int], Decimal] = {}
    ngoai_luoi = 0
    for r in anh_dap_an["dong"]:
        k = (ch(r["le"]), ch(r["ma_hd"]), int(_so(r["ngay"])))
        if k not in luoi:
            ngoai_luoi += 1
            continue
        exp[k] = _so(r["gt"])
    o_loi_set = {(ch(r["le"]), ch(r["ma_hd"]), int(_so(r["ngay"])))
                 for r in anh_dap_an.get("phu", {}).get("o_loi", {}).get("dong", [])}
    if ngoai_luoi:
        ly.append(f"{ngoai_luoi} ô đáp án ⛔ thuộc lưới engine (khối × cây × trục)")

    # ── 5 · so từng ô ──
    kpi = set(MA_KPI)
    tong_o = khop = o_kpi = o_loi = 0
    lech: list[dict[str, Any]] = []
    lech_ite: list[dict[str, Any]] = []
    for k in KHOI_CFA1:
        for n in cay.nut:
            khoi_ds = "la" if cay.la(n.ma) else "cha"
            for t in truc:
                key = (k, n.ma, t)
                if n.ma in kpi:
                    o_kpi += 1
                    continue
                if key in o_loi_set:
                    o_loi += 1
                    continue
                tong_o += 1
                e = exp.get(key, Decimal(0))
                g = luoi[key]
                if DUNG_SAI_C3A[khoi_ds].khop(g, e):
                    khop += 1
                else:
                    x = {"le": k, "ma": n.ma, "ngay": t, "khoi": khoi_ds,
                         "exp": str(e), "got": str(g), "lech": str(g - e)}
                    (lech_ite if key in chiu_alias else lech).append(x)

    # ── 6 · lệch có tên ──
    hd_ngoai: dict[str, int] = {}
    for i in kq.dong_ngoai_cay:
        nh = meta[i][2] if meta[i][2] else "<rỗng>"
        hd_ngoai[nh] = hd_ngoai.get(nh, 0) + 1
    lech_co_ten = {"thieu_tien_te_D": sorted(thieu_D), "hd_ngoai_cay": hd_ngoai,
                   "hd_alias": _dem_alias(kq, meta),
                   "hd_khac_hoa_thuong": len(kq.dong_khac_hoa),
                   "dong_nhan_cha": len(kq.dong_nhan_cha),
                   "dong_ngoai_truc": len(kq.dong_ngoai_truc)}
    tom_ite = _tom_tat_lech_ite(lech_ite, "ngay", _iso)
    ngay_so_cuoi = max((m[0] for m in meta), default=0)

    # ── 7 · phân xử ──
    khop_dap_an = khop
    khop = khop + len(lech_ite)           # hợp đồng CG2: khớp đáp án + lệch CÓ CHỦ ĐÍCH đã khai mong
    px = danh_gia(tong_o=tong_o, khop=khop, lat_truot=0, dong_doc=len(dong_cfa),
                  dong_mong_doi=len(dong_cfa), toi_thieu_o=1)
    ly = list(px.ly_do) + ly
    ly += _so_mong_ite(tom_ite, mong.lech_ite)
    for ten, thuc, mg in (
            ("dòng ảnh đầu vào", len(anh_vao["dong"]), mong.so_dong_anh),
            ("dòng vào tinh_gl", len(feed), mong.dong_so),
            ("mẫu số ô so", tong_o, mong.tong_o),
            ("ô KPI loại", o_kpi, mong.o_kpi),
            ("ô '-' đáp án loại", o_loi, mong.o_loi),
            ("số hàng đáp án", len(anh_dap_an["dong"]), mong.so_dong_dap_an),
            ("số cột ngày", len(truc), mong.so_ngay),
            ("ngày đầu trục", truc[0] if truc else None, mong.ngay_dau),
            ("ngày có số cuối", ngay_so_cuoi, mong.ngay_so_cuoi)):
        if mg is not None and thuc != mg:
            ly.append(f"{ten} {thuc} ≠ mong {mg}")
    for ten, thuc, mg in (
            ("thieu_tien_te_D", lech_co_ten["thieu_tien_te_D"], sorted(mong.thieu_D)),
            ("hd_ngoai_cay", hd_ngoai, dict(mong.hd_ngoai_cay)),
            ("hd_alias", lech_co_ten["hd_alias"], dict(mong.hd_alias or {})),
            ("hd_khac_hoa_thuong", lech_co_ten["hd_khac_hoa_thuong"], mong.hd_khac_hoa),
            ("dong_nhan_cha", lech_co_ten["dong_nhan_cha"], mong.dong_nhan_cha),
            ("dong_ngoai_truc", lech_co_ten["dong_ngoai_truc"], mong.dong_ngoai_truc)):
        if thuc != mg:
            ly.append(f"lệch có tên `{ten}` ≠ mong: thực {thuc} · mong {mg}")
    px = PhanXu(not ly, tuple(ly))

    hd2 = {
        "bang": "HD2.WP-C3a", "goi": "WP-C3a",
        "mo_ta": "SO.CFA1 Daily: tinh_gl (BR/BS từ E/F + ix_fx) trên GL của bản sao CF report → "
                 "cfa1_daily (lá = Σ BR−BS theo (khối, nhãn HD V, ngày A); khối LE lọc cột P; "
                 "cha = Σ con theo cây IX.HD) ↔ đáp án 409 từng ô",
        "nguon_dau_vao": "tests/fixture/dap_an/gl_cf_dau_vao.json (A·D·E·F·P·R·V, ⛔ B:C·G; errata ㉓)",
        "khoa": "khoi(5) + ma_hd(cây ATL 74) + ngay(serial)",
        "khoi": list(KHOI_CFA1),
        "dung_sai_theo_khoi": {k: {"atol": str(v.atol), "rtol": str(v.rtol),
                                   "max_lech_do": str(DO_C3A_MAX_LECH[k])}
                               for k, v in DUNG_SAI_C3A.items()},
        "dung_sai_ghi_chu": "atol 1e-14 = ≥10× max|lệch| đo 18/11 (lá 1,0e-15 · cha 7,5e-16); rtol 0 "
                            "(|exp| ≤ 6,1). Chứng ĐỎ: +1 VND một dòng ⇒ lá + mọi cha ĐỎ; +1e-12 một "
                            "ô đáp án ⇒ đúng ô ấy ĐỎ.",
        "dong_so": len(feed), "mong_dong_so": MONG_C3A_DONG_SO,
        "tong_o": tong_o, "mong_tong_o": MONG_C3A_TONG_O, "khop": khop,
        "khop_dap_an": khop_dap_an,
        "khop_ghi_chu": "khop = ô khớp đáp án (khop_dap_an) + ô lệch CÓ CHỦ ĐÍCH ITE đã khai mong "
                        "(lech_co_chu_dich_ite.so_o) — WO-226 phương án A; ⛔ giấu: khop_dap_an + "
                        "so_o = khop, lech_ngoai_ten = 0, mong khác ⇒ ĐỎ cả hai chiều",
        "lech_co_chu_dich_ite": tom_ite,
        "mong_lech_co_chu_dich_ite": dict(mong.lech_ite or {}),
        "lech_ngoai_ten": len(lech),
        "o_kpi_loai": o_kpi, "mong_o_kpi": MONG_C3A_O_KPI, "ma_kpi": list(MA_KPI),
        "o_loi_dap_an_loai": o_loi, "mong_o_loi": MONG_C3A_O_LOI,
        "so_dong_dap_an": len(anh_dap_an["dong"]), "mong_so_dong_dap_an": MONG_C3A_SO_DONG_DAP_AN,
        "truc_ngay": {"dau": _iso(truc[0]) if truc else None, "so_cot": len(truc),
                      "ngay_so_cuoi": _iso(ngay_so_cuoi) if ngay_so_cuoi else None,
                      "cot_chua_co_so": sum(1 for t in truc if t > ngay_so_cuoi),
                      "ngay_dau_ix_per": lich.ngay_dau.isoformat(), "nguon_ngay_dau": lich.nguon,
                      "ghi_chu": "trục từ IX.PER KHO (H6; C6 lưu 21/10) lùi 1 cột = 2024-10-20 "
                                 "(errata ㉑, ⛔ 21/10 của spec); ⛔ đọc phu.ngay_truc của đáp án 409"},
        "lech_co_ten": lech_co_ten,
        "so_du_dau": "KHÔNG dùng — CFA1 Daily là phát sinh theo ngày (BR/BS từng dòng), ⛔ tồn luỹ kế",
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    return ThanhQuaC3a(tong_o=tong_o, khop=khop, lech=lech, lech_co_ten=lech_co_ten,
                       o_kpi=o_kpi, o_loi=o_loi, phan_xu=px, hd2_cong=hd2, luoi=luoi,
                       lech_ite=lech_ite, khop_dap_an=khop_dap_an)


def chay_wp_c3a(dsn: str | None = None) -> ThanhQuaC3a:
    """IX.PER TỪ KHO *(như `chay_wp_c3b`)*; kho tắt / chưa khai ⇒ ĐỎ có lý do, ⛔ rơi về ngày tạm."""
    lich, loi = _lich_tu_kho(dsn)
    if lich is None:
        px = PhanXu(False, (loi or "IX.PER rỗng",))
        return ThanhQuaC3a(tong_o=0, khop=0, lech=[], lech_co_ten={}, o_kpi=0, o_loi=0, phan_xu=px,
                           hd2_cong={"bang": "HD2.WP-C3a", "goi": "WP-C3a", "dat": False,
                                     "ly_do": list(px.ly_do)}, luoi={})
    return so_sanh_c3a(nap_anh(ANH_GL_CF), nap_anh(ANH_CFA1), nap_fx(), nap_cay(), lich,
                       mong_c3a_mac_dinh())


def _in_bao_c3a(tq: ThanhQuaC3a) -> None:
    h = tq.hd2_cong
    print("══ do_hd2 · WP-C3a — SO.CFA1 Daily ↔ đáp án 409 (5 khối × cây × ngày)")
    print(f"  dòng sổ vào   : {h['dong_so']} (mong {MONG_C3A_DONG_SO}; bỏ "
          f"{len(tq.lech_co_ten['thieu_tien_te_D'])} thiếu D)")
    print(f"  ô so / khớp   : {tq.khop}/{tq.tong_o}  (mẫu số mong {MONG_C3A_TONG_O} = 5 × 54 mã × "
          f"760 ngày − 25 ô '-')")
    print(f"  ô KPI loại    : {tq.o_kpi} (mong {MONG_C3A_O_KPI}; {len(MA_KPI)} mã công thức chéo)")
    print(f"  ô lệch ngoài tên: {len(tq.lech)}")
    for x in tq.lech[:10]:
        print(f"      [{x['le']} · {x['ma']} · {_iso(x['ngay'])}] exp {x['exp']} got {x['got']}")
    print(f"  lệch có tên   : {tq.lech_co_ten}")
    print(f"  trục ngày     : {h['truc_ngay']['dau']} · {h['truc_ngay']['so_cot']} cột · số cuối "
          f"{h['truc_ngay']['ngay_so_cuoi']} ({h['truc_ngay']['cot_chua_co_so']} cột chưa có số)")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")


# ══════════════════════════════════════════════════════════════════════════════════
# WP-C3b — SO.CFA1 Y/H/Q/M ↔ đáp án 410 từng ô *(ISP 3.1.2 · Step 20 · H6 · WO-188)*
# ══════════════════════════════════════════════════════════════════════════════════
# ⭐ Công thức 410 *(SA FORMULA 18/11, `Report I CFA1 Y H Q M` hàng 6…12 · 52…60)*: lá =
#   `SUMIFS('Report I CFA1 Daily'!hàng, Daily!$1:$1, năm[, Daily!$2|$3|$4, H|Q|M])`; tiêu đề Daily
#   `YEAR(ngày)` · `if(tháng<7,"H1","H2")` · `if(tháng<4,"Q1",…)` · `MONTH(ngày)`; cha `=sum(con)`;
#   AR/CP1.1/CP1.2/CP2/CP3 = "-" ⇒ `phu.o_loi` (25 ô, năm 2024).
# Chuỗi: GL CF *(cùng feed WP-C3a)* → `tinh_gl` → `cfa1_daily` trên trục `truc_ngay(IX.PER kho, ngày
#   đọc)` → `cuon_ky` → so TỪNG Ô. Đáp án 410 CHỈ cấp giá trị mong *(⛔ trục ngày, ⛔ đầu vào)*.
# ⛔ 411 *(CFA3 Daily)*: DT5 LOẠI khỏi đóng băng *(ISP Step 15)* ⇒ ⛔ có đáp án để so — khai `loai_tru`.
# ⭐ Ngày 20/10/2024 *(errata ㉑: trục 409/410 từ 20/10, IX.PER kho = 21/10)*: engine theo KHO. Đo
#   18/11: dòng sổ ngày 20/10 = 0 *(ngày sổ nhỏ nhất 2024-10-21 = 45586)*; ô ≠ 0 cột 20/10 của 409 = 5,
#   cả 5 là `NPC` *(KPI luỹ kế — đã loại)* ⇒ 21/10 ⛔ làm rơi số nào; `dong_ngoai_truc` MONG 0 canh.

ANH_YHQM = GOC / "tests" / "fixture" / "dap_an" / "cfa1_yhqm.json"
#: AC-3: CÙNG 20 mã KPI của H5 *(⛔ bản thứ hai)* — loại khỏi so, ĐẾM.
MA_KPI_C3B = MA_KPI

# ── MONG *(đo 18/11 — Đ5: khai TRƯỚC; khác ⇒ ĐỎ cả hai chiều)* ──────────────────────────
MONG_C3B_NGAY_DAU = "2024-10-21"       #: IX.PER kho (C6) — ⛔ 20/10 của trục đáp án (errata ㉑)
MONG_C3B_DEN = "2026-11-18"            #: ngày đọc ảnh gl_cf_dau_vao (`ngay_dong_bang`)
MONG_C3B_SO_KY = 57                    #: 3 năm (2024…2026, năm của trục) × 19
MONG_C3B_KY_KHONG_NGAY = 14            #: 2024 H1·Q1·Q2·Q3·M01…M09 (trước ngày đầu) + 2026M12 (chưa tới)
MONG_C3B_O_KPI = 5 * len(MA_KPI) * MONG_C3B_SO_KY                                     #: 5.700
MONG_C3B_O_LOI = 25                    #: ô "-" của 410 (phu.o_loi)
MONG_C3B_O_KY_KHONG_NGAY = 5 * (74 - len(MA_KPI)) * MONG_C3B_KY_KHONG_NGAY             #: 3.780
MONG_C3B_TONG_O = (5 * (74 - len(MA_KPI)) * (MONG_C3B_SO_KY - MONG_C3B_KY_KHONG_NGAY)
                   - MONG_C3B_O_LOI)                                                    #: 11.585
MONG_C3B_O_SO_KHAC_0 = 2636           #: ô SO được mà đáp án ≠ 0 (bằng chứng dương — Đ3/Đ4)
MONG_C3B_SO_DONG_DAP_AN = 5655         #: ô ≠ 0 của đáp án 410 (dòng chính thưa, cả KPI)

# ── Dung sai THEO KHỐI — đo 18/11 trên 11.585 ô, KHÔNG áp dung sai ───────────────────
#   khối  max|lệch| đo   max|exp| (cả 410)   atol     biên
#   la    1,10e-14       59,6               2e-13    ×18
#   cha   1,17e-14                           2e-13    ×17
# Lệch lớn hơn WP-C3a *(1e-15)* vì mỗi ô kỳ là Σ ≤ 366 ô Daily *(sai số cộng dồn của Sheets)*.
# `rtol = 0`: atol là knob duy nhất. Chứng ĐỎ: +1 VND một dòng *(≈4e-11 mUSD)* ⇒ lá + mọi cha × 4
# kỳ ĐỎ *(bài đột biến)*; +1e-12 một ô đáp án ⇒ ĐỎ đúng ô ấy *(bài Đ5)*.
DO_C3B_MAX_LECH = {"la": Decimal("1.10e-14"), "cha": Decimal("1.17e-14")}
DUNG_SAI_C3B_GHI_CHU = ("atol 2e-13 = ≥17× max|lệch| đo 18/11 trên 11.585 ô (lá 1,10e-14 · cha "
                        "1,17e-14 — Σ ≤ 366 ô Daily); rtol 0. Chứng ĐỎ: +1 VND một dòng ⇒ lá + "
                        "mọi cha × 4 kỳ ĐỎ; +1e-12 một ô đáp án ⇒ đúng ô ấy ĐỎ.")
DUNG_SAI_C3B: dict[str, DungSaiCot] = {
    "la": DungSaiCot(atol=Decimal("2e-13"), rtol=Decimal(0)),
    "cha": DungSaiCot(atol=Decimal("2e-13"), rtol=Decimal(0)),
}


@dataclass(frozen=True)
class MongC3b:
    thieu_D: tuple[int, ...]
    hd_ngoai_cay: Mapping[str, int]
    hd_khac_hoa: int
    tong_o: int
    o_so_khac_0: int
    dong_nhan_cha: int = 0
    dong_ngoai_truc: int = 0
    o_khac_0_ky_khong_ngay: int = 0
    o_kpi: int | None = None
    o_loi: int | None = None
    o_ky_khong_ngay: int | None = None
    so_dong_dap_an: int | None = None
    so_ky: int | None = None
    ngay_dau: str | None = None
    den: str | None = None
    hd_alias: Mapping[str, int] | None = None
    lech_ite: Mapping[str, Any] | None = None


def mong_c3b_mac_dinh() -> MongC3b:
    return MongC3b(thieu_D=MONG_C3A_THIEU_D, hd_ngoai_cay=dict(MONG_C3A_HD_NGOAI_CAY),
                   hd_khac_hoa=MONG_C3A_HD_KHAC_HOA, tong_o=MONG_C3B_TONG_O,
                   o_so_khac_0=MONG_C3B_O_SO_KHAC_0, o_kpi=MONG_C3B_O_KPI, o_loi=MONG_C3B_O_LOI,
                   o_ky_khong_ngay=MONG_C3B_O_KY_KHONG_NGAY,
                   so_dong_dap_an=MONG_C3B_SO_DONG_DAP_AN, so_ky=MONG_C3B_SO_KY,
                   ngay_dau=MONG_C3B_NGAY_DAU, den=MONG_C3B_DEN, hd_alias=dict(MONG_C3A_HD_ALIAS),
                   lech_ite=dict(MONG_LECH_ITE_C3B))


@dataclass
class ThanhQuaC3b:
    tong_o: int
    khop: int
    lech: list[dict[str, Any]]
    lech_co_ten: dict[str, Any]
    o_kpi: int
    o_loi: int
    o_ky_khong_ngay: int
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    luoi: dict[tuple[str, str, str], Decimal]
    max_lech: dict[str, Decimal] = field(default_factory=dict)
    lech_ite: list[dict[str, Any]] = field(default_factory=list)
    khop_dap_an: int = 0


def _feed_cfa(anh_vao: dict, fx: Mapping[int, Mapping[str, Decimal]], ly: list[str]):
    """Dòng sổ CF → `tinh_gl` → `DongCFA` *(cùng phép WP-C3a; bỏ dòng thiếu D — có tên)*."""
    thieu_D: list[int] = []
    feed: list[DongGL] = []
    meta: list[tuple[int, str | None, str | None]] = []
    for r in anh_vao["dong"]:
        ds, ngay = int(_so(r["dong_sheet"])), int(_so(r["ngay"]))
        tt = _chu(r.get("D"))
        if not tt:
            thieu_D.append(ds)
            continue
        d = datetime.date(1899, 12, 30) + datetime.timedelta(days=ngay)
        feed.append(DongGL(thang=d.year * 100 + d.month, tien_te=tt,
                           no=(_so(r.get("E")) or Decimal(0)), co=(_so(r.get("F")) or Decimal(0))))
        meta.append((ngay, _chu(r.get("le")), _chu(r.get("hd_final"))))
    kq_gl = []
    try:
        kq_gl = tinh_gl(feed, fx)
    except (ThieuTyGia, TienTeNgoaiGL) as e:
        ly.append(f"tinh_gl ⛔ chạy được *(⛔ đo được ⇒ ĐỎ)*: {type(e).__name__}: "
                  f"{' '.join(str(e).split())}")
    dong = [DongCFA(ngay=n, le=le, hd=h, musd_no=k.musd_no, musd_co=k.musd_co)
            for (n, le, h), k in zip(meta, kq_gl)]
    return dong, meta, thieu_D, len(feed)


def so_sanh_c3b(anh_vao: dict, anh_dap_an: dict, fx: Mapping[int, Mapping[str, Decimal]],
                cay: CayHD, lich: LichKy, mong: MongC3b) -> ThanhQuaC3b:
    """GL CF → `tinh_gl` → `cfa1_daily` *(trục IX.PER)* → `cuon_ky` → so TỪNG Ô với 410."""
    ly: list[str] = []
    dong_cfa, meta, thieu_D, n_feed = _feed_cfa(anh_vao, fx, ly)

    # ── trục: IX.PER (kho) → ngày đọc của ẢNH ĐẦU VÀO *(⛔ đáp án)* ──
    den = datetime.date.fromisoformat(str(anh_vao["ngay_dong_bang"]))
    truc = truc_ngay(lich, den)
    kq = cfa1_daily(dong_cfa, cay, ngay=truc, khoi=KHOI_CFA1, alias=hd_cfg.ALIAS_NHAN_HD)
    cu = cuon_ky(kq.o, cay, ngay=truc, khoi=KHOI_CFA1)
    luoi = cu.o
    chiu_alias = _o_chiu_alias(
        luoi, cuon_ky(cfa1_daily(dong_cfa, cay, ngay=truc, khoi=KHOI_CFA1).o, cay, ngay=truc,
                      khoi=KHOI_CFA1).o)
    khong_ngay = set(cu.ky_khong_ngay)

    # ── đáp án ──
    exp: dict[tuple[str, str, str], Decimal] = {}
    ngoai_luoi = 0
    for r in anh_dap_an["dong"]:
        k = (_chu(r["le"]), _chu(r["ma_hd"]), _chu(r["ky"]))
        if k not in luoi:
            ngoai_luoi += 1
            continue
        exp[k] = _so(r["gt"])
    o_loi_set = {(_chu(r["le"]), _chu(r["ma_hd"]), _chu(r["ky"]))
                 for r in anh_dap_an.get("phu", {}).get("o_loi", {}).get("dong", [])}
    if ngoai_luoi:
        ly.append(f"{ngoai_luoi} ô đáp án ⛔ thuộc lưới engine (khối × cây × kỳ)")
    ky_dap_an = [_chu(x["ky"]) for x in anh_dap_an.get("phu", {}).get("ky_truc", {}).get("dong", [])]
    if ky_dap_an != cu.ky:
        ly.append(f"trục kỳ engine ({len(cu.ky)}) ≠ trục kỳ đáp án ({len(ky_dap_an)})")

    # ── so từng ô ──
    kpi = set(MA_KPI_C3B)
    tong_o = khop = o_kpi = o_loi = o_kkn = o_kkn_khac_0 = o_so_khac_0 = 0
    lech: list[dict[str, Any]] = []
    lech_ite: list[dict[str, Any]] = []
    max_lech = {"la": Decimal(0), "cha": Decimal(0)}
    for kh in KHOI_CFA1:
        for n in cay.nut:
            khoi_ds = "la" if cay.la(n.ma) else "cha"
            for t in cu.ky:
                key = (kh, n.ma, t)
                if n.ma in kpi:
                    o_kpi += 1
                    continue
                if key in o_loi_set:
                    o_loi += 1
                    continue
                e = exp.get(key, Decimal(0))
                if t in khong_ngay:
                    o_kkn += 1
                    if e != 0:
                        o_kkn_khac_0 += 1
                    continue
                tong_o += 1
                if e != 0:
                    o_so_khac_0 += 1
                g = luoi[key]
                max_lech[khoi_ds] = max(max_lech[khoi_ds], abs(g - e))
                if DUNG_SAI_C3B[khoi_ds].khop(g, e):
                    khop += 1
                else:
                    x = {"le": kh, "ma": n.ma, "ky": t, "khoi": khoi_ds,
                         "exp": str(e), "got": str(g), "lech": str(g - e)}
                    (lech_ite if key in chiu_alias else lech).append(x)

    hd_ngoai: dict[str, int] = {}
    for i in kq.dong_ngoai_cay:
        nh = meta[i][2] if meta[i][2] else "<rỗng>"
        hd_ngoai[nh] = hd_ngoai.get(nh, 0) + 1
    lech_co_ten = {"thieu_tien_te_D": sorted(thieu_D), "hd_ngoai_cay": hd_ngoai,
                   "hd_alias": _dem_alias(kq, meta),
                   "hd_khac_hoa_thuong": len(kq.dong_khac_hoa),
                   "dong_nhan_cha": len(kq.dong_nhan_cha),
                   "dong_ngoai_truc": len(kq.dong_ngoai_truc),
                   "o_khac_0_ky_khong_ngay": o_kkn_khac_0}
    tom_ite = _tom_tat_lech_ite(lech_ite, "ky", str)

    khop_dap_an = khop
    khop = khop + len(lech_ite)           # hợp đồng CG2: khớp đáp án + lệch CÓ CHỦ ĐÍCH đã khai mong
    px = danh_gia(tong_o=tong_o, khop=khop, lat_truot=0, dong_doc=len(dong_cfa),
                  dong_mong_doi=len(dong_cfa), toi_thieu_o=1)
    ly = list(px.ly_do) + ly
    ly += _so_mong_ite(tom_ite, mong.lech_ite)
    for ten, thuc, mg in (
            ("mẫu số ô so", tong_o, mong.tong_o),
            ("ô so ≠ 0 (đáp án)", o_so_khac_0, mong.o_so_khac_0),
            ("ô KPI loại", o_kpi, mong.o_kpi),
            ("ô '-' đáp án loại", o_loi, mong.o_loi),
            ("ô kỳ không ngày", o_kkn, mong.o_ky_khong_ngay),
            ("số hàng đáp án", len(anh_dap_an["dong"]), mong.so_dong_dap_an),
            ("số cột kỳ", len(cu.ky), mong.so_ky),
            ("ngày đầu trục (IX.PER)", lich.ngay_dau.isoformat(), mong.ngay_dau),
            ("ngày cuối trục (ngày đọc)", den.isoformat(), mong.den)):
        if mg is not None and thuc != mg:
            ly.append(f"{ten} {thuc} ≠ mong {mg}")
    for ten, thuc, mg in (
            ("thieu_tien_te_D", lech_co_ten["thieu_tien_te_D"], sorted(mong.thieu_D)),
            ("hd_ngoai_cay", hd_ngoai, dict(mong.hd_ngoai_cay)),
            ("hd_alias", lech_co_ten["hd_alias"], dict(mong.hd_alias or {})),
            ("hd_khac_hoa_thuong", lech_co_ten["hd_khac_hoa_thuong"], mong.hd_khac_hoa),
            ("dong_nhan_cha", lech_co_ten["dong_nhan_cha"], mong.dong_nhan_cha),
            ("dong_ngoai_truc", lech_co_ten["dong_ngoai_truc"], mong.dong_ngoai_truc),
            ("o_khac_0_ky_khong_ngay", o_kkn_khac_0, mong.o_khac_0_ky_khong_ngay)):
        if thuc != mg:
            ly.append(f"lệch có tên `{ten}` ≠ mong: thực {thuc} · mong {mg}")
    px = PhanXu(not ly, tuple(ly))

    hd2 = {
        "bang": "HD2.WP-C3b", "goi": "WP-C3b",
        "mo_ta": "SO.CFA1 Y/H/Q/M: tinh_gl → cfa1_daily (trục truc_ngay(IX.PER kho, ngày đọc)) → "
                 "cuon_ky (Σ Daily theo ky_cua: năm của CHÍNH ngày) ↔ đáp án 410 từng ô",
        "nguon_dau_vao": "tests/fixture/dap_an/gl_cf_dau_vao.json (cùng feed WP-C3a)",
        "dap_an": "tests/fixture/dap_an/cfa1_yhqm.json (PD 410, 370 hàng × 57 kỳ)",
        "loai_tru": "411 (CFA3 Daily) — DT5 loại khỏi đóng băng (ISP Step 15) ⇒ ⛔ đáp án để so",
        "khoa": "khoi(5) + ma_hd(cây ATL 74) + ky(57: năm×19 Y/H/Q/M)",
        "khoi": list(KHOI_CFA1),
        "dung_sai_theo_khoi": {k: {"atol": str(v.atol), "rtol": str(v.rtol),
                                   "max_lech_do": str(DO_C3B_MAX_LECH[k])}
                               for k, v in DUNG_SAI_C3B.items()},
        "dung_sai_ghi_chu": DUNG_SAI_C3B_GHI_CHU,
        "dong_so": n_feed, "tong_o": tong_o, "mong_tong_o": mong.tong_o, "khop": khop,
        "khop_dap_an": khop_dap_an,
        "khop_ghi_chu": "khop = ô khớp đáp án (khop_dap_an) + ô lệch CÓ CHỦ ĐÍCH ITE đã khai mong "
                        "(lech_co_chu_dich_ite.so_o) — WO-226 phương án A; ⛔ giấu: khop_dap_an + "
                        "so_o = khop, lech_ngoai_ten = 0, mong khác ⇒ ĐỎ cả hai chiều",
        "lech_co_chu_dich_ite": tom_ite,
        "mong_lech_co_chu_dich_ite": dict(mong.lech_ite or {}),
        "o_so_khac_0": o_so_khac_0, "mong_o_so_khac_0": mong.o_so_khac_0,
        "lech_ngoai_ten": len(lech),
        "o_kpi_loai": o_kpi, "ma_kpi": list(MA_KPI_C3B),
        "o_loi_dap_an_loai": o_loi, "o_ky_khong_ngay_loai": o_kkn,
        "so_dong_dap_an": len(anh_dap_an["dong"]),
        "truc": {"ngay_dau": lich.ngay_dau.isoformat(), "nguon_ngay_dau": lich.nguon,
                 "den": den.isoformat(), "so_ngay": len(truc), "nam": list(cu.nam),
                 "so_ky": len(cu.ky), "ky_khong_ngay": list(cu.ky_khong_ngay),
                 "ghi_chu": "ngày đầu = IX.PER KHO (C6, 21/10); trục 409/410 từ 20/10 (errata ㉑) — "
                            "đo 18/11: 0 dòng sổ ngày 20/10, 5 ô ≠ 0 cột 20/10 của 409 đều NPC (KPI). "
                            "Kỳ 0 ngày trên trục ⛔ so (⛔ '0 đã chốt'), đáp án ≠ 0 ở đó ⇒ ĐỎ"},
        "lech_co_ten": lech_co_ten,
        "dat": px.dat, "ly_do": list(px.ly_do),
    }
    return ThanhQuaC3b(tong_o=tong_o, khop=khop, lech=lech, lech_co_ten=lech_co_ten,
                       o_kpi=o_kpi, o_loi=o_loi, o_ky_khong_ngay=o_kkn, phan_xu=px,
                       hd2_cong=hd2, luoi=luoi, max_lech=max_lech, lech_ite=lech_ite,
                       khop_dap_an=khop_dap_an)


def _lich_tu_kho(dsn: str | None) -> tuple[LichKy | None, str | None]:
    """IX.PER mới nhất TỪ KHO *(C6)*. Kho tắt / chưa khai / bản hỏng ⇒ (None, lý do) — ⛔ ngày tạm."""
    try:
        import psycopg
        from fls.db.kho import dsn_that
        from fls.repo import cau_hinh_repo as chc
        with psycopg.connect(dsn or dsn_that()) as c:
            return chc.doc_per(c), None
    except Exception as e:  # noqa: BLE001 — Đ5: ⛔ đo được ⇒ ĐỎ có lý do, ⛔ nổ
        return None, f"IX.PER ⛔ đọc được từ kho: {type(e).__name__}: {' '.join(str(e).split())}"


def chay_wp_c3b(dsn: str | None = None) -> ThanhQuaC3b:
    lich, loi = _lich_tu_kho(dsn)
    if lich is None:
        px = PhanXu(False, (loi or "IX.PER rỗng",))
        return ThanhQuaC3b(tong_o=0, khop=0, lech=[], lech_co_ten={}, o_kpi=0, o_loi=0,
                           o_ky_khong_ngay=0, phan_xu=px,
                           hd2_cong={"bang": "HD2.WP-C3b", "goi": "WP-C3b", "dat": False,
                                     "ly_do": list(px.ly_do)}, luoi={})
    return so_sanh_c3b(nap_anh(ANH_GL_CF), nap_anh(ANH_YHQM), nap_fx(), nap_cay(), lich,
                       mong_c3b_mac_dinh())


def _in_bao_c3b(tq: ThanhQuaC3b) -> None:
    h = tq.hd2_cong
    print("══ do_hd2 · WP-C3b — SO.CFA1 Y/H/Q/M ↔ đáp án 410 (5 khối × cây × kỳ)")
    if "truc" in h:
        t = h["truc"]
        print(f"  trục          : IX.PER {t['ngay_dau']} ({t['nguon_ngay_dau']}) → {t['den']} · "
              f"{t['so_ngay']} ngày · năm {t['nam']} · {t['so_ky']} kỳ · {len(t['ky_khong_ngay'])} kỳ 0 ngày")
        print(f"  ô so / khớp   : {tq.khop}/{tq.tong_o}  (mẫu số mong {h['mong_tong_o']} = 5 × 54 mã × "
              f"43 kỳ có ngày − 25 ô '-'); ô so ≠ 0: {h['o_so_khac_0']} (mong {h['mong_o_so_khac_0']})")
        print(f"  ô loại        : KPI {tq.o_kpi} · '-' {tq.o_loi} · kỳ 0 ngày {tq.o_ky_khong_ngay}")
        print(f"  max|lệch|     : { {k: str(v) for k, v in tq.max_lech.items()} }")
    print(f"  ô lệch ngoài tên: {len(tq.lech)}")
    for x in tq.lech[:10]:
        print(f"      [{x['le']} · {x['ma']} · {x['ky']}] exp {x['exp']} got {x['got']}")
    print(f"  lệch có tên   : {tq.lech_co_ten}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")


# ─────────────────────────────────────────────────────────────────────────────────────────────
# WP-C4a — AL.PLT GI vendor THƯỜNG ↔ đáp án MID3 (PD 507) từng ô *(ISP 3.1.2 · Step 24 · H9 ·
# WO-200 · sau DT8b BG-205)*. Đầu vào: IX.VEN ĐỌC TỪ KHO + ảnh CFA1 GI (PD 504) — ⛔ MID3 làm
# đầu vào. O = Σ `pe` CFA1, P = Σ `pm` số CFA1 theo (vendor, tháng). PE theo CDT1 (Looker PD 502)
# ⛔ có ảnh ⇒ engine nhận PE rỗng: Vendor-tháng thường có tiền ≠ 0 ⇒ `LoiPhanBo` ⇒ ĐỎ — đó
# chính là chiều thứ hai của Đ5 *(một Vendor-tháng thường bỗng ≠ 0 ⇒ ĐỎ, buộc khai lại)*.
# ⭐ Đo 18/11 *(Đ3)*: ô ≠ 0 của vendor thường = 0 ⇒ "tập toàn 0 — đo được nhưng ⛔ chứng minh
# RATE"; phép so ô ≠ 0 của RATE chuyển H10 *(orchestrator chốt, BG-201 "Sau DT8b")*.
# Vế PM của Vendor-tháng có `pm_ghi_chu` *(chữ 'Need to manual input')* = ô ⛔ so được *(⛔ hoá 0)*.
# ─────────────────────────────────────────────────────────────────────────────────────────────
ANH_CFA1_GI = GOC / "tests" / "fixture" / "dau_vao" / "gi_cfa1.json"
ANH_MID3 = GOC / "tests" / "fixture" / "dap_an" / "gi_mid3.json"
MID3_CDT = ("cvl", "cor", "shq1", "csm", "cah", "asa")
TOL_C4A = Decimal("0.000001")


@dataclass(frozen=True)
class MongC4a:
    """Khai TRƯỚC *(Đ4 nhãn · Đ5 khác ⇒ ĐỎ cả hai chiều)* — đo 18/11 trên ảnh DT8b."""
    vm_thuong: int = 44            # Vendor-tháng thường = 4 vendor × 11 tháng
    vendor_thuong: tuple = ("VD113", "VD336", "VD58", "VD61")
    o_so: int = 420                # ô so = 44 × 14 − ô PM ⛔ so được
    o_khong_so: int = 196          # 28 Vendor-tháng P = chữ × (P + 6 PM_cdt)
    o_khac_0: int = 0              # ⭐ tập toàn 0 — ⛔ chứng minh RATE
    o_khong_so_khac_0: int = 0     # H9-R1-01: PHÍA ĐÁP ÁN của 196 ô ⛔ so được — đo 0/196 (R1, 18/11)
    ks_al_vm: int = 44             # H9-R1-02: KS.AL đo = số Vendor-tháng thường (⛔ hằng ghim trong bài)
    lech: int = 0
    bo_qua: tuple = (("Max", 132), ("VD341", 11), ("VD428", 11), ("VD444", 11), ("VD62", 11))
    vendor_bo_qua: int = 15


@dataclass
class ThanhQuaC4a:
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    lech: list = field(default_factory=list)


def so_sanh_c4a(cfa1: dict, mid3: dict, ven, mong: MongC4a) -> ThanhQuaC4a:
    from fls.bao_cao import phan_bo as pb
    ly: list[str] = []
    o: dict = {}
    p: dict = {}
    p_chu: set = set()
    for r in cfa1["dong"]:
        k = (_chu(r["vendor"]), r["thang"])
        o[k] = o.get(k, Decimal(0)) + Decimal(r["pe"])
        p[k] = p.get(k, Decimal(0)) + (Decimal(r["pm"]) if r.get("pm") is not None else 0)
        if r.get("pm_ghi_chu") is not None:
            p_chu.add(k)
    cdt = tuple(c for c in ven.cdt1 if c.split(" |")[0].lower() in MID3_CDT)
    ma = {c.split(" |")[0].lower(): c for c in cdt}
    if len(cdt) != 6:
        ly.append(f"CDT1 khớp 6 cột MID3: đo {len(cdt)} trên {len(ven.cdt1)} CDT1 IX.VEN")
    try:
        kq = pb.chia_nen_tang({k: {} for k in o}, o, p, ven, cdt1=cdt)
    except pb.LoiPhanBo as e:
        px = PhanXu(False, (*ly, f"engine: {e}"))
        return ThanhQuaC4a(px, {"bang": "HD2.WP-C4a", "goi": "WP-C4a", "dat": False,
                                "ly_do": list(px.ly_do)})
    dap: dict = {}
    for r in mid3["dong"]:
        if r.get("vendor") is not None:
            k = (_chu(r["vendor"]), r["thang"])
            if k in dap:
                ly.append(f"MID3 trùng khoá {k}")
            dap[k] = r
    o_so = o_khong = o_khac0 = o_khong_khac0 = 0
    lech: list = []
    for k, d in sorted(kq.chia.items()):
        r = dap.get(k)
        if r is None:
            ly.append(f"MID3 thiếu Vendor-tháng {k}")
            continue
        cap = [("pe", o[k]), ("pm", p[k])]
        for c in MID3_CDT:
            cap += [(f"{c}_pe", d[ma[c]][0]), (f"{c}_pm", d[ma[c]][1])]
        for cot, got in cap:
            if cot.endswith("pm") and k in p_chu:
                o_khong += 1
                try:                       # H9-R1-01: ô ⛔ so được vẫn có `mong` cho PHÍA ĐÁP ÁN (Đ5)
                    o_khong_khac0 += Decimal(r[cot]) != 0
                except (ArithmeticError, TypeError, ValueError):
                    o_khong_khac0 += 1     # ⛔ đo được ⇒ ĐỎ, ⛔ coi là 0
                continue
            exp = Decimal(r[cot])
            o_so += 1
            o_khac0 += (exp != 0 or got != 0)
            if abs(exp - got) > TOL_C4A:
                lech.append({"vendor": k[0], "thang": k[1], "cot": cot, "exp": str(exp), "got": str(got)})
    try:
        ks = pb.ks_al(kq, o, p)
    except pb.LoiPhanBo as e:
        ks, ly = 0, [*ly, str(e)]
    bo = tuple((n, len(x)) for n, x in kq.bo_qua.items())
    vbo = len({k[0] for x in kq.bo_qua.values() for k in x})
    thuong = tuple(sorted({k[0] for k in kq.chia}))
    do = {"vm_thuong": (len(kq.chia), mong.vm_thuong), "vendor_thuong": (thuong, mong.vendor_thuong),
          "o_so": (o_so, mong.o_so), "o_khong_so": (o_khong, mong.o_khong_so),
          "o_khac_0": (o_khac0, mong.o_khac_0), "o_khong_so_khac_0": (o_khong_khac0, mong.o_khong_so_khac_0),
          "ks_al_vm": (ks, mong.ks_al_vm), "lech": (len(lech), mong.lech),
          "bo_qua": (bo, mong.bo_qua), "vendor_bo_qua": (vbo, mong.vendor_bo_qua)}
    for ten, (thuc, m) in do.items():
        if thuc != m:
            ly.append(f"{ten}: đo {thuc} ≠ mong {m}")
    if o_so == 0:
        ly.append("0 ô so ⇒ ⛔ đo được (Đ3)")
    px = PhanXu(not ly, tuple(ly))
    hd2 = {"bang": "HD2.WP-C4a", "goi": "WP-C4a",
           "mo_ta": "AL.PLT GI vendor thường: IX.VEN kho + CFA1 GI → chia_nen_tang → KS.AL ↔ MID3 (vendor, tháng) từng ô",
           "nguon_dau_vao": "tests/fixture/dau_vao/gi_cfa1.json (PD 504) + IX.VEN kho",
           "dap_an": "tests/fixture/dap_an/gi_mid3.json (PD 507, 209 hàng có khoá)",
           "khoa": "(vendor, thang) × 14 cột (O · P · 6 CDT1 × PE/PM)",
           "vm_thuong": len(kq.chia), "vendor_thuong": list(thuong), "o_so": o_so,
           "o_khong_so": o_khong, "o_khong_so_ly_do": "P = chữ 'Need to manual input' (⛔ hoá 0)",
           # CG2-R2-03 · hợp đồng khối gói H4 (`doc_bao_cao._goi_la`): `tong_o` = ô SO ĐƯỢC (= `o_so`,
           #   ⛔ tính ô P chữ), `khop` = ô so khớp = `o_so − lech`. Khoá cũ giữ nguyên nghĩa.
           "tong_o": o_so, "khop": o_so - len(lech),
           "vm_p_chu": len(p_chu & set(kq.chia)), "o_khac_0": o_khac0,
           "o_khong_so_khac_0": o_khong_khac0,
           "o_khac_0_nhan": "tập toàn 0 — đo được nhưng ⛔ chứng minh RATE (phép so ô ≠ 0 ⇒ H10)",
           "lech": len(lech), "ks_al_vm": ks,
           "bo_qua": dict(bo), "vendor_bo_qua": vbo,
           "mong": dataclasses.asdict(mong), "dat": px.dat, "ly_do": list(px.ly_do)}
    return ThanhQuaC4a(px, hd2, lech)


def chay_wp_c4a(dsn: str | None = None) -> ThanhQuaC4a:
    try:
        import psycopg
        from fls.db.kho import dsn_that
        from fls.repo import cau_hinh_repo as chc
        with psycopg.connect(dsn or dsn_that()) as c:
            ven = chc.doc_ven(c)
    except Exception as e:  # noqa: BLE001 — Đ5: ⛔ đo được ⇒ ĐỎ có lý do
        px = PhanXu(False, (f"IX.VEN ⛔ đọc được từ kho: {type(e).__name__}: {' '.join(str(e).split())}",))
        return ThanhQuaC4a(px, {"bang": "HD2.WP-C4a", "goi": "WP-C4a", "dat": False,
                                "ly_do": list(px.ly_do)})
    return so_sanh_c4a(nap_anh(ANH_CFA1_GI), nap_anh(ANH_MID3), ven, MongC4a())


def _in_bao_c4a(tq: ThanhQuaC4a) -> None:
    h = tq.hd2_cong
    print("══ do_hd2 · WP-C4a — AL.PLT GI vendor thường ↔ MID3 (vendor, tháng)")
    if "o_so" in h:
        print(f"  Vendor-tháng thường : {h['vm_thuong']} ({len(h['vendor_thuong'])} vendor {h['vendor_thuong']})")
        print(f"  ô so / ô ⛔ so được  : {h['o_so']} / {h['o_khong_so']} ({h['o_khong_so_ly_do']}; {h['vm_p_chu']} Vendor-tháng)")
        print(f"  ô ≠ 0               : {h['o_khac_0']} — {h['o_khac_0_nhan']}")
        print(f"  đáp án ≠ 0 ở ô ⛔ so : {h['o_khong_so_khac_0']}/{h['o_khong_so']} (mong 0)")
        print(f"  lệch                : {h['lech']} · KS.AL đo {h['ks_al_vm']} Vendor-tháng")
        print(f"  bỏ qua (5 nhãn)     : {h['bo_qua']} · {h['vendor_bo_qua']} vendor")
    for x in tq.lech[:10]:
        print(f"      [{x['vendor']} · {x['thang']} · {x['cot']}] exp {x['exp']} got {x['got']}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")


# ─────────────────────────────────────────────────────────────────────────────────────────────
# WP-C4b — AL.PLT GI MỌI vendor theo MÃ 'cách tính' ↔ đáp án MID3 (PD 507) từng ô *(ISP 3.1.2 ·
# Step 28 · H10 · WO-216)*. Đầu vào: IX.VEN ĐỌC TỪ KHO + ảnh CFA1 GI (PD 504: O · P TỪNG DÒNG
# Vendor × tháng × No) + ảnh **MID1 (PD 505) cột T = PE theo CDT1**. ⭐ MID1 là THƯỢNG NGUỒN của
# MID3, ⛔ vòng tròn: công thức `E` của MID1 *(đọc `FORMULA` 19/11)* = `iferror(…SUMIFS('Source
# (Looker)'!K; I; Q; O; S)…)` — chỉ Looker + VNM, ⛔ tham chiếu MID2/MID3; `T = iferror(E10:E,…)`.
# RATE tính LẠI từ MID1 *(⛔ đọc RATE `AA` của MID2)*. `pe` MID1 rỗng = `iferror` rỗng ⇒ 0 *(SUMIFS)*.
# ─────────────────────────────────────────────────────────────────────────────────────────────
ANH_MID1 = GOC / "tests" / "fixture" / "dap_an" / "gi_mid1.json"
MID1_BO_CDT = "shq2"               # MID2 RATE = T/sum(T11:T16): 6 CDT1, ⛔ SHQ2 (hàng đầu khối)


@dataclass(frozen=True)
class MongC4b:
    """Khai TRƯỚC *(Đ4 nhãn · Đ5 khác ⇒ ĐỎ cả hai chiều)* — đo 19/11 bằng nguyên mẫu ĐỘC LẬP
    *(scratchpad, ⛔ engine)* + phép đếm thẳng trên ảnh DT8/DT8b: 1.254/1.254 ô PE_cdt lệch ≤ 8,3e-10;
    135 Vendor-tháng P chữ; 988 ô O/PE ≠ 0 ở MID3; 66 `pe` MID1 rỗng ngoài SHQ2."""
    vm: int = 209                  # Vendor-tháng = 19 vendor × 11 tháng (khoá MID3)
    vm_dac_biet: int = 165         # 15 vendor mang nhãn ≠ thường × 11
    vm_thuong: int = 44            # 4 vendor thuần thường × 11
    dong_cfa1: int = 408           # dòng CFA1 = Vendor × tháng × No vào engine
    dong_mid1: int = 2856          # dòng MID1 (PE theo CDT1) đọc
    mid1_pe_rong: int = 66         # `pe` rỗng (iferror) ở 6 CDT1 ⇒ 0 — ĐẾM, ⛔ im (77 cả 7 CDT1, 11 ở SHQ2)
    o_so: int = 1981               # ô so = 209 × 14 − ô ⛔ so được = 2.926 − 945
    o_khong_so: int = 945          # 135 Vendor-tháng có dòng P = chữ × (P + 6 PM_cdt)
    o_khac_0: int = 988            # ô so mà đáp án HAY engine ≠ 0 = 823 PE_cdt + 165 O — KHÔNG rỗng (Đ3)
    o_khac_0_dac_biet: int = 988   # … trong đó thuộc vendor đặc biệt *(thường: 0 — BG-205)*
    o_khong_so_khac_0: int = 0     # PHÍA ĐÁP ÁN của ô ⛔ so được ≠ 0 *(H9-R1-01)*
    lech: int = 0
    ks_al_vm: int = 209            # KS.AL đo Σ chia = O (/ P khi P số) — mọi Vendor-tháng
    ks_al_dac_biet: int = 165
    bo_qua: int = 0                # ⭐ H10: vendor bỏ qua = 0
    muon: int = 11                 # dòng mượn RATE *(một mã · No ΣP lớn hơn — hoà ⇒ No sau)*
    muon_o_khac_0: int = 0         # ⭐ dòng mượn có O ≠ 0 — đo 0 ⇒ luật mượn ⛔ chứng minh trên số thật
    theo_tong_thang: int = 0       # dòng O = 0 ∧ P > 0 — đo 0 (P số = 0 trên mọi dòng)
    kieu_vm: tuple = (("khong", 44), ("mang_dong_no", 11), ("mang_theo_no", 22), ("mang_ty_le_no1", 132))


@dataclass
class ThanhQuaC4b:
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    lech: list = field(default_factory=list)


def _do_c4b(px: PhanXu) -> ThanhQuaC4b:
    return ThanhQuaC4b(px, {"bang": "HD2.WP-C4b", "goi": "WP-C4b", "dat": False, "ly_do": list(px.ly_do)})


def so_sanh_c4b(cfa1: dict, mid1: dict, mid3: dict, ven, mong: MongC4b) -> ThanhQuaC4b:
    from fls.bao_cao import phan_bo as pb
    ly: list[str] = []
    cdt = tuple(c for c in ven.cdt1 if c.split(" |")[0].lower() in MID3_CDT)
    ma = {c.split(" |")[0].lower(): c for c in cdt}
    if len(cdt) != 6:
        ly.append(f"CDT1 khớp 6 cột MID3: đo {len(cdt)} trên {len(ven.cdt1)} CDT1 IX.VEN")
    dong = []
    for r in cfa1["dong"]:
        dong.append(pb.DongCFA1(_chu(r["vendor"]), r["thang"], r["no"], Decimal(r["pe"]),
                                None if r.get("pm_ghi_chu") is not None or r.get("pm") is None
                                else Decimal(r["pm"])))
    pe: dict = {}
    rong = 0
    for r in mid1["dong"]:
        c = _chu(r["cdt1"])
        if c.split(" |")[0].lower() == MID1_BO_CDT:
            continue
        if c not in cdt:
            ly.append(f"MID1 CDT1 lạ {c!r} @ {r['dong_sheet']}")
            continue
        if r.get("pe") is None:
            rong += 1
            continue
        k = (_chu(r["vendor"]), r["thang"])
        pe.setdefault(k, {}).setdefault(c, Decimal(0))
        pe[k][c] += Decimal(r["pe"])
    try:
        kq = pb.chia_theo_cach_tinh(dong, pe, ven, cdt1=cdt)
        ks = pb.ks_al(kq, kq.o, kq.p)
    except pb.LoiPhanBo as e:
        return _do_c4b(PhanXu(False, (*ly, f"engine: {e}")))
    dac = {v for v, ns in pb.nhan_vendor(ven).items() if ns - {pb.NHAN_THUONG}}
    dap: dict = {}
    for r in mid3["dong"]:
        if r.get("vendor") is not None:
            k = (_chu(r["vendor"]), r["thang"])
            if k in dap:
                ly.append(f"MID3 trùng khoá {k}")
            dap[k] = r
    if set(dap) != set(kq.chia):
        ly.append(f"khoá MID3 ≠ khoá engine: thiếu ở engine {sorted(set(dap) - set(kq.chia))[:5]} · "
                  f"thừa {sorted(set(kq.chia) - set(dap))[:5]}")
    o_so = o_khong = o_khac0 = o_khac0_db = o_khong_khac0 = 0
    lech: list = []
    for k, d in sorted(kq.chia.items()):
        r = dap.get(k)
        if r is None:
            continue
        cap = [("pe", kq.o[k]), ("pm", kq.p[k])]
        for c in MID3_CDT:
            cap += [(f"{c}_pe", d[ma[c]][0]), (f"{c}_pm", d[ma[c]][1])]
        for cot, got in cap:
            if got is None:
                o_khong += 1
                try:
                    o_khong_khac0 += Decimal(r[cot]) != 0
                except (ArithmeticError, TypeError, ValueError):
                    o_khong_khac0 += 1     # ⛔ đo được ⇒ ĐỎ, ⛔ coi là 0
                continue
            try:
                exp = Decimal(r[cot])
            except (ArithmeticError, TypeError, ValueError):
                ly.append(f"MID3 {k} · {cot}: ⛔ số")
                continue
            o_so += 1
            nz = exp != 0 or got != 0
            o_khac0 += nz
            o_khac0_db += nz and k[0] in dac
            if abs(exp - got) > TOL_C4A:
                lech.append({"vendor": k[0], "thang": k[1], "cot": cot, "exp": str(exp), "got": str(got)})
    m_o = {(v, t, n): x.o for x in dong for (v, t, n) in [(x.vendor, x.thang, x.no)]}
    muon0 = sum(1 for v, t, n, _ in kq.muon if m_o[(v, t, n)] != 0)
    kieu: dict = {}
    for v, _t in kq.chia:
        kieu[kq.ma[v]] = kieu.get(kq.ma[v], 0) + 1
    bo = sum(len(x) for x in kq.bo_qua.values())
    vm_db = sum(1 for k in kq.chia if k[0] in dac)
    do = {"vm": (len(kq.chia), mong.vm), "vm_dac_biet": (vm_db, mong.vm_dac_biet),
          "vm_thuong": (len(kq.chia) - vm_db, mong.vm_thuong), "dong_cfa1": (len(dong), mong.dong_cfa1),
          "dong_mid1": (len(mid1["dong"]), mong.dong_mid1), "mid1_pe_rong": (rong, mong.mid1_pe_rong),
          "o_so": (o_so, mong.o_so), "o_khong_so": (o_khong, mong.o_khong_so),
          "o_khac_0": (o_khac0, mong.o_khac_0), "o_khac_0_dac_biet": (o_khac0_db, mong.o_khac_0_dac_biet),
          "o_khong_so_khac_0": (o_khong_khac0, mong.o_khong_so_khac_0), "lech": (len(lech), mong.lech),
          "ks_al_vm": (ks, mong.ks_al_vm), "ks_al_dac_biet": (vm_db, mong.ks_al_dac_biet),
          "bo_qua": (bo, mong.bo_qua), "muon": (len(kq.muon), mong.muon),
          "muon_o_khac_0": (muon0, mong.muon_o_khac_0),
          "theo_tong_thang": (len(kq.theo_tong_thang), mong.theo_tong_thang),
          "kieu_vm": (tuple(sorted(kieu.items())), mong.kieu_vm)}
    for ten, (thuc, m) in do.items():
        if thuc != m:
            ly.append(f"{ten}: đo {thuc} ≠ mong {m}")
    if o_so == 0 or o_khac0 == 0:
        ly.append(f"ô so {o_so} · ô ≠ 0 {o_khac0} ⇒ ⛔ đo được (Đ3)")
    px = PhanXu(not ly, tuple(ly))
    hd2 = {"bang": "HD2.WP-C4b", "goi": "WP-C4b",
           "mo_ta": "AL.PLT GI mọi vendor theo mã 'cách tính': IX.VEN kho + CFA1 (O/P từng dòng) + MID1 "
                    "(PE theo CDT1) → chia_theo_cach_tinh → KS.AL ↔ MID3 (vendor, tháng) từng ô",
           "nguon_dau_vao": "tests/fixture/dau_vao/gi_cfa1.json (PD 504) + tests/fixture/dap_an/gi_mid1.json "
                            "cột T (PD 505, thượng nguồn — ⛔ tính từ MID3) + IX.VEN kho",
           "dap_an": "tests/fixture/dap_an/gi_mid3.json (PD 507, 209 hàng có khoá)",
           "khoa": "(vendor, thang) × 14 cột (O · P · 6 CDT1 × PE/PM)",
           **{k: v[0] for k, v in do.items() if k not in ("kieu_vm",)},
           # CG2-R2-03 → H10-R2-01 · hợp đồng khối gói H4 (`doc_bao_cao._goi_la`): `tong_o` = ô SO ĐƯỢC
           #   (= `o_so` 1.981, ⛔ tính 945 ô P chữ), `khop` = ô so khớp = `o_so − lech`. Khoá cũ giữ nghĩa.
           "tong_o": o_so, "khop": o_so - len(lech),
           "kieu_vm": dict(kieu),
           "o_khong_so_ly_do": "Vendor-tháng có dòng P = chữ 'Need to manual input' (⛔ hoá 0)",
           "o_khac_0_nhan": "ô so mà đáp án hay engine ≠ 0 — tập KHÔNG rỗng: chứng minh RATE trên số thật",
           "muon_nhan": "dòng mượn RATE có O ≠ 0 = 0 ⇒ luật mượn chỉ chứng minh ở bài tổng hợp",
           "mong": dataclasses.asdict(mong), "dat": px.dat, "ly_do": list(px.ly_do)}
    return ThanhQuaC4b(px, hd2, lech)


def chay_wp_c4b(dsn: str | None = None) -> ThanhQuaC4b:
    try:
        import psycopg
        from fls.db.kho import dsn_that
        from fls.repo import cau_hinh_repo as chc
        with psycopg.connect(dsn or dsn_that()) as c:
            ven = chc.doc_ven(c)
    except Exception as e:  # noqa: BLE001 — Đ5: ⛔ đo được ⇒ ĐỎ có lý do
        return _do_c4b(PhanXu(False, (f"IX.VEN ⛔ đọc được từ kho: {type(e).__name__}: "
                                      f"{' '.join(str(e).split())}",)))
    return so_sanh_c4b(nap_anh(ANH_CFA1_GI), nap_anh(ANH_MID1), nap_anh(ANH_MID3), ven, MongC4b())


def _in_bao_c4b(tq: ThanhQuaC4b) -> None:
    h = tq.hd2_cong
    print("══ do_hd2 · WP-C4b — AL.PLT GI mọi vendor theo mã 'cách tính' ↔ MID3 (vendor, tháng)")
    if "o_so" in h:
        print(f"  Vendor-tháng        : {h['vm']} = đặc biệt {h['vm_dac_biet']} + thường {h['vm_thuong']}"
              f" · kiểu PE {h['kieu_vm']}")
        print(f"  đầu vào             : CFA1 {h['dong_cfa1']} dòng · MID1 {h['dong_mid1']} dòng "
              f"(pe rỗng ⇒ 0: {h['mid1_pe_rong']})")
        print(f"  ô so / ô ⛔ so được  : {h['o_so']} / {h['o_khong_so']} ({h['o_khong_so_ly_do']})")
        print(f"  ô ≠ 0               : {h['o_khac_0']} (đặc biệt {h['o_khac_0_dac_biet']}) — {h['o_khac_0_nhan']}")
        print(f"  đáp án ≠ 0 ở ô ⛔ so : {h['o_khong_so_khac_0']}/{h['o_khong_so']}")
        print(f"  lệch                : {h['lech']} · KS.AL {h['ks_al_vm']} Vendor-tháng "
              f"(đặc biệt {h['ks_al_dac_biet']}) · bỏ qua {h['bo_qua']}")
        print(f"  mượn RATE           : {h['muon']} dòng, O ≠ 0: {h['muon_o_khac_0']} — {h['muon_nhan']}"
              f" · tổng tháng {h['theo_tong_thang']}")
    for x in tq.lech[:10]:
        print(f"      [{x['vendor']} · {x['thang']} · {x['cot']}] exp {x['exp']} got {x['got']}")
    print(f"  KẾT: {tq.phan_xu.mot_dong}")


def _ghi_cong(goi: str, hop_dong: dict[str, Any]) -> None:
    """`hd2_cong.json` CHỈ THÊM: WP-C2 giữ ở gốc *(hợp đồng H4)*; gói khác vào khoá `<goi>`."""
    cu: dict[str, Any] = {}
    if RA_CONG.is_file():
        cu = json.loads(RA_CONG.read_text(encoding="utf-8"))
    if goi == "WP-C2":
        them = {k: v for k, v in cu.items() if k in GOI_BIET and k != "WP-C2"}
        moi = {**hop_dong, **them}
    else:
        moi = {**cu, goi: hop_dong}
    RA_CONG.parent.mkdir(parents=True, exist_ok=True)
    RA_CONG.write_text(json.dumps(moi, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  ghi: {RA_CONG.relative_to(GOC)} [{goi}]")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="do_hd2.py", description="Cổng parity HD2.")
    p.add_argument("--goi", required=True, choices=GOI_BIET, help="gói cổng HD2")
    p.add_argument("--ghi", action="store_true", help="ghi docs/ITL/_tools/hd2_cong.json")
    p.add_argument("--dsn", default=None,
                   help="WP-C4a/WP-C4b: kho đọc IX.VEN (mặc định PG_DSN; ISP dùng PG_DSN_TEST — ⛔ ghi kho thật)")
    a = p.parse_args(argv)
    if a.goi == "WP-C4b":
        tq4b = chay_wp_c4b(a.dsn)
        _in_bao_c4b(tq4b)
        if a.ghi:
            _ghi_cong("WP-C4b", tq4b.hd2_cong)
        return 0 if tq4b.phan_xu.dat else 1
    if a.goi == "WP-C4a":
        tq4 = chay_wp_c4a(a.dsn)
        _in_bao_c4a(tq4)
        if a.ghi:
            _ghi_cong("WP-C4a", tq4.hd2_cong)
        return 0 if tq4.phan_xu.dat else 1
    if a.goi == "WP-C3b":
        tq3b = chay_wp_c3b()
        _in_bao_c3b(tq3b)
        if a.ghi:
            _ghi_cong("WP-C3b", tq3b.hd2_cong)
        return 0 if tq3b.phan_xu.dat else 1
    if a.goi == "WP-C3a":
        tq3 = chay_wp_c3a()
        _in_bao_c3a(tq3)
        if a.ghi:
            _ghi_cong("WP-C3a", tq3.hd2_cong)
        return 0 if tq3.phan_xu.dat else 1
    tq = chay_wp_c2()
    _in_bao(tq)
    if a.ghi:
        _ghi_cong("WP-C2", tq.hd2_cong)
    return 0 if tq.phan_xu.dat else 1


if __name__ == "__main__":
    raise SystemExit(main())
