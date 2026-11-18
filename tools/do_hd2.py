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


@dataclass(frozen=True)
class DungSai:
    """Dung sai số thực *(IEEE-754 ↔ `Decimal`; BT theo ĐỘ LỚN lũy kế — rtol)*. Đo 18/11: lệch tối
    đa quan sát được rel ≈ 3.2e-12 *(BQ/BT)* · abs ≈ 1.3e-14 *(ô theo dòng)* ⇒ ngưỡng dưới chừa
    ~300× biên, vẫn bắt mọi lệch THẬT *(thiếu gieo số dư ⇒ rel ~300)*."""
    atol: Decimal = Decimal("1e-6")      # sàn tuyệt đối cho ô gần 0
    rtol: Decimal = Decimal("1e-9")      # theo độ lớn (lũy kế)

    def khop(self, got: Decimal, exp: Decimal) -> bool:
        return abs(got - exp) <= self.atol + self.rtol * abs(exp)


@dataclass(frozen=True)
class Mong:
    """Khai TRƯỚC *(Đ5)*: tập lệch-có-tên mong đợi + dung sai. Thực ≠ mong ⇒ ĐỎ cả hai chiều."""
    thieu_D: tuple[int, ...]
    itl_na: tuple[int, ...]
    ky_vang: Mapping[int, int]
    thang_thieu_ty_gia: tuple[int, ...]
    dung_sai: DungSai = field(default_factory=DungSai)


def mong_mac_dinh() -> Mong:
    return Mong(thieu_D=MONG_THIEU_D, itl_na=MONG_ITL_NA, ky_vang=dict(MONG_KY_VANG),
               thang_thieu_ty_gia=MONG_THANG_THIEU_TY_GIA, dung_sai=DungSai())


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
            if ds.khop(got, exp):
                khop += 1
            else:
                lech.append({"dong_sheet": dsn, "ky": _chu(a.get("ky")), "cot": c,
                             "exp": str(exp), "got": str(got),
                             "lech": str(got - exp)})

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
    px = _phan_xu(tong_o, khop, len(feed_ds), lech, lech_co_ten, mong, loi_engine)

    hd2_cong = _hop_dong(tong_o, khop, so_o_dap_an_so_duoc, lech, lech_co_ten, mau_so_thang,
                         len(feed_ds), ds, px)
    return ThanhQua(tong_o=tong_o, khop=khop, so_o_dap_an_so_duoc=so_o_dap_an_so_duoc,
                    lech=lech, lech_co_ten=lech_co_ten, mau_so_thang=mau_so_thang,
                    phan_xu=px, hd2_cong=hd2_cong)


def _phan_xu(tong_o: int, khop: int, dong_doc: int, lech: list, lech_co_ten: dict,
             mong: Mong, loi_engine: str | None) -> PhanXu:
    # lõi: ≥1 ô · ⛔ lát bỏ · 0 ô lệch *(cong_parity — toi_thieu_o=1 theo AC-1 "số ô > 0")*
    px = danh_gia(tong_o=tong_o, khop=khop, lat_truot=0, dong_doc=dong_doc,
                  dong_mong_doi=dong_doc, toi_thieu_o=1)
    ly = list(px.ly_do)
    if loi_engine is not None:
        ly.append(f"engine ⛔ chạy được *(⛔ đo được ⇒ ĐỎ)*: {loi_engine}")
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
              ds: DungSai, px: PhanXu) -> dict[str, Any]:
    """Hợp đồng `hd2_cong.json` cho `CG2` *(Step 30)* — khai khoá RÕ, chỉ THÊM về sau."""
    return {
        "bang": "HD2.WP-C2",
        "goi": "WP-C2",
        "mo_ta": "parity CA.GL (tinh_gl trên E/F + ix_fx, gieo số dư đầu kỳ hàng 24) ↔ đáp án 406 "
                 "BM…BT, nối dong_sheet",
        "khoa": "dong_sheet + cot(BM…BT)",
        "cot_so": list(COT_BMBT),
        "dung_sai": {"atol": str(ds.atol), "rtol": str(ds.rtol),
                     "ghi_chu": "IEEE-754 ↔ Decimal; BT theo độ lớn lũy kế (rtol)"},
        "dong_so": dong_so,
        "tong_o": tong_o,
        "khop": khop,
        "so_o_dap_an_so_duoc": so_o_dap_an,
        "lech_ngoai_ten": len(lech),
        "lech_co_ten": {k: len(v) for k, v in lech_co_ten.items()},
        "lech_co_ten_chi_tiet": lech_co_ten,
        "mau_so_thang": mau_so_thang,
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
    print(f"  ô so / khớp   : {tq.khop}/{tq.tong_o}  (= số ô đáp án so được {tq.so_o_dap_an_so_duoc})")
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
