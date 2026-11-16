# -*- coding: utf-8 -*-
"""VOI SỐ LƯỢNG DỮ LIỆU — ma trận THÁNG × LOẠI DỮ LIỆU, mỗi ô bốn số: CÓ · CHẠY · MAPPING · SỬA.

⭐ Owner 13/11 (AP Voi FLS v2): *"Cột là tháng, dòng là các loại dữ liệu. Mỗi ô cần có dữ liệu
   đối chiếu → Voi số lượng dữ liệu. Số có, số chạy, mapping và số đã sửa sai."*

⛔⛔ Công cụ này CHỈ đọc ẢNH ĐÓNG BĂNG đã có trong repo (`tests/fixture/`), và chạy CHÍNH MÃ FLS lên
   ảnh ấy (`pm_join.xep_ca_lat`, `final_rule.tinh_final`, `tu_soi.soi_mot_dong`). Nó ⛔ đọc kho:
   kho `fls-pg-1` ⛔ chạy trong phiên dựng AP (cổng 5433 từ chối). Số của kho (fls_itl · fls_adjustment
   theo tháng) là việc của agent ở máy có kho — AP ghi rõ ô nào đo trên ảnh, ô nào ⛔ đo.

Bốn số — mỗi số nói NÓ ĐẾM GÌ (Đ4), đơn vị là DÒNG trừ khi ghi "ô":
  CÓ      = dòng sổ AS-IS `ITL Ledge` của kỳ (ảnh `[Master] ITL_Ledge_raw.xlsx`, đóng băng 26/08).
  CHẠY    = dòng FLS dựng lại được từ `Transaction Mapping L1` (đọc live 26/08) VÀ ghép 1-1 được với
            dòng sổ theo khoá (Số CT, PS Nợ, PS Có, TK, tiền tệ) — `classifying_vs_canon.json`.
  MAPPING = hai số, ⛔ gộp: NOW = dòng mà VLOOKUP của Gsheet trả được mã HD (Classifying khối 1 có giá
            trị, ⛔ `#N/A`, ⛔ "Need to manual input"); FLS = dòng bank thuộc nhóm ghép được hình A · B · C
            của `pm_join` (Ref No + Σ tiền trong dung sai).
  SỬA     = Ô (⛔ dòng) kế toán phải điền ở vùng chỉnh tay R–AT, 7 khối: máy KHÔNG trả lời (Classifying
            rỗng hoặc "Need to manual input") mà Final có giá trị. Tách: GÕ = giá trị thật người gõ ·
            MĐ = nhận mặc định cứng của khối (`MAC_DINH_THEO_KHOI`). Thêm hai số để soát: TRỐNG = máy không
            trả lời và Final vẫn rỗng · ĐÈ = Final ≠ Classifying dù máy CÓ trả lời (trái công thức
            `Final = f(S, U)` — lỗi bản xuất, test_parity_ca_so ghim 63 ô lệch kiểu này trên cả sổ).
  ⚠ Đã thử đếm SỬA theo DÒNG ("≥1 khối người điền"): ra 9.964/9.967 — vô nghĩa, vì khối 4–7 (kỳ DV ·
            đối tác · hoá đơn) gần như dòng nào máy cũng không trả lời. Nên đếm ô và tách theo khối.

Cổng (Đ5 — khai `mong`, NO khi khác, cả hai chiều): tổng dòng · số ghép · hình ghép · parity phải
   bằng đúng số đã ghim trong bài test của chính các ảnh; lệch ⇒ exit 1, ⛔ ghi JSON.

HD1 THEO KỲ — khối `dat_hd1` (ISP 3.1.2 · Step 4 · H2 · `WO-090` · AP v3.1.2 §5.3.1 HD1 ★: *"Lệch = 0,
   hoặc mỗi lệch có tên lý do và owner ký"*):
  Một kỳ ĐẠT ⇔ (dòng 1-1 100 % — `chạy = có` — HOẶC mọi dòng thiếu của kỳ có nhãn lý do ĐÃ KÝ)
              ∧ (ô Final 7 khối 100 % — `o_parity_khop = o_parity`, mẫu số > 0, Đ3).
  ⛔ gồm chế độ tự sinh: nó chỉ đo được 2026-03 (một ảnh Manual input) — theo kỳ là việc của `H15`
     (Step 43). Vì thế số ở đây (5/23 khi sổ rỗng) ≠ "tháng đạt HD1" của Figure 5.3.3 (0/23, đòi CẢ
     tự sinh) — hai phép, hai nhãn (Đ4).
  · NHÃN lý do: tệp `docs/ITL/_tools/phan_loai_ly_do.json` của DT1b (Step 5, làm song song) — H2 chỉ ĐỌC.
    Hợp đồng đọc = khuôn của chính `phan_loai_dong_thieu.json` (DT1a): `{"van_tay": {"thieu", "nguoc"},
    "dong_thieu": [{"dong_sheet": int, "nhan": str | null}, …]}` (khoá thừa bỏ qua). Hai vân tay phải
    BẰNG vân tay tập dòng H2 tính lại từ ảnh (cùng công thức DT1a) — ⛔ thì đó là nhãn của một tập dòng
    KHÁC ⇒ ĐỎ. Tệp VẮNG ⇒ mọi dòng thiếu = "chưa có nhãn" (đỏ) — ⛔ lỗi: DT1b chưa về.
  · CHỮ KÝ: sổ `docs/ITL/_tools/so_ly_do_hd1.json` — `{"chu_ky": [{"nhan", "so_dong", "nguoi_ky",
    "ngay"}]}`, khởi tạo RỖNG; O8 = ThuongCT ký thật (⛔ agent). Một chữ ký phủ MỌI dòng thiếu mang nhãn
    ấy, và `so_dong` phải BẰNG số dòng thiếu mang nhãn ấy trong tệp nhãn — lệch ⇒ ĐỎ (chữ ký cũ: owner
    ký N dòng, ⛔ được lặng lẽ phủ dòng thứ N+1 mà owner chưa thấy). Sổ VẮNG ⇒ ĐỎ (mất sổ ⛔ được
    trông như "chưa ai ký").
  · ⛔⛔ Đây là MIỄN TRỪ trong cổng — repo cấm "gõ tên vào danh sách miễn trừ để cổng xanh". Nên mọi
    đầu vào hỏng (JSON · cấu trúc · kiểu · trùng · ngoài tập · vân tay · số dòng) là ĐỎ với nguyên
    nhân MỘT dòng (`S0-R1-04`), ⛔ rơi về "chưa có nhãn" cho êm; và TẬP kỳ đạt có `MONG` khai trước —
    một chữ ký thật làm đổi tập ⇒ ĐỎ ⇒ người sửa phải khai lại `MONG["dat_hd1_theo_ky"]` (Đ5, cố ý).
  · ⚠ `_sha` và `MONG` (các khoá cũ) được `tools/phan_loai_dong_thieu.py` (DT1a) import — GIỮ NGUYÊN
    tên + nghĩa (`DT1a-R1-06`); H2 chỉ THÊM khoá `dat_hd1_theo_ky`.

Chạy:  python tools/do_voi_so_luong.py            # in bảng, ⛔ ghi
       python tools/do_voi_so_luong.py --ghi      # ghi docs/ITL/_tools/voi_so_luong.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal as D
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.adapters.pm_join import (DAY_NGUOI, GHEP_DUOC, DongBank, DongPM,  # noqa: E402
                                  canon_ref, moi_noi, xep_ca_lat)
from fls.ledger.final_rule import (MAC_DINH_THEO_KHOI, may_khong_tra_loi,  # noqa: E402
                                   tinh_final)
from fls.oracle.tu_soi import la_o_loi, soi_mot_dong  # noqa: E402

FX = GOC / "tests" / "fixture"
RA = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
NHAN = GOC / "docs" / "ITL" / "_tools" / "phan_loai_ly_do.json"     # DT1b ghi — H2 chỉ ĐỌC (vắng = chưa có nhãn)
SO_LY_DO = GOC / "docs" / "ITL" / "_tools" / "so_ly_do_hd1.json"    # O8 ký — H2 khởi tạo RỖNG (vắng = ĐỎ)
KHOA_CHU_KY = ("nhan", "so_dong", "nguoi_ky", "ngay")             # ISP Step 4 §3: nhãn · số dòng · người ký · ngày
KHOI = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")

# ── `mong` — mỗi số lấy từ bài test đã ghim của chính ảnh ấy (⛔ đặt tay ở đây cho đẹp) ──
MONG = {
    "so_dong_so": 9967,              # tests/ledger/test_parity_ca_so.py · DONG_MONG_DOI
    "so_ky": 23,                     # test_pham_vi_hien_vat_dung_nhu_khai
    "so_dong_ghep_canon": 9845,      # tests/ledger/test_classifying.py · DONG_MONG_DOI
    "so_dong_bank": 9992,            # tests/adapters/test_pm_join.py
    "so_dong_pm": 3703,
    "khong_co_ma": 105,
    "khong_thay_ma_PM": 6532,
    "dong_theo_hinh": {"A": 2272, "B": 29, "C": 400, "D": 27, "E": 199, "F": 428},
    "parity_o": (69510, 69510),      # test_parity_100_phan_tram_tung_o_tren_CA_SO
    "dong_loai_tu_soi": 37,
    # ⭐ 16/11 (owner: "How done quan trọng nhất là mapping được 100%, giống các dữ liệu quá khứ"):
    "hd_parity": (9930, 9930),       # khối 1 HD, chế độ oracle (đọc MID của sổ) — đo 16/11 rồi ghim
    "tu_sinh_o": (4088, 4088),       # chế độ TỰ SINH 2026-03: FLS tự tính MID từ Manual input (tinh_mid) → Final
    "tu_sinh_hd": (584, 584),
    "tu_sinh_mid": (4020, 4088),     # MID tự tính = MID của sổ ở 4.020 ô (Final vẫn khớp đủ vì Classifying có trả lời)
    "checksum": {"itl_ledge_adjustment.json": "575c53379074c759",
                 "classifying_vs_canon.json": "7226ef112dbd00f7",
                 "pm_join.json": "6ec10945e6c1636a"},
    # ⭐ H2 (ISP 3.1.2 · Step 4 · WO-090) — TẬP kỳ ĐẠT HD1 (mọi kỳ khác là ĐỎ), khai TRƯỚC lần đo đầu:
    #    AP v3.1.2 §5.3.1 "dòng ghép 1-1: 9.845/9.967 — 5/23 tháng đủ" + BG-081 §Bảng đếm (đúng 5 kỳ ⛔ có
    #    dòng thiếu) · ô Final 23/23 tháng. Sổ lý do RỖNG ⇒ chỉ kỳ đủ dòng mới đạt. Một chữ ký THẬT (O8)
    #    làm đổi tập này ⇒ ĐỎ ⇒ khai lại ở đây cùng commit chữ ký (Đ5 — cố ý, ⛔ lỗi).
    "dat_hd1_theo_ky": ("2024-10", "2024-11", "2024-12", "2025-03", "2025-04"),
}
_HONG = object()                     # dấu "tệp ⛔ đọc được" của _doc_json (⛔ nhầm với JSON `null`)


def _chuan(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def _nap(ten: str) -> dict:
    return json.loads((FX / ten).read_text(encoding="utf-8"))


def _sha(*phan) -> str:
    return hashlib.sha256(json.dumps(list(phan), ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()[:16]


# ══════════════════════════════════════════════════════════════════ HD1 theo kỳ (H2 · WO-090)
def _van_tay_dong(so_dong) -> str:
    """Vân tay một TẬP dòng = sha256 (16 ký tự) của danh sách số dòng ĐÃ SẮP — ĐÚNG công thức `_van_tay`
    của `tools/phan_loai_dong_thieu.py` (DT1a). ⛔ import ngược từ đó: DT1a đã import tệp này (vòng).
    Bài `test_H2_B1_van_tay_tap_dong_TRUNG_DT1a` canh hai bản bằng nhau (Đ2 — hai nguồn)."""
    return hashlib.sha256(json.dumps(sorted(so_dong), separators=(",", ":")).encode()).hexdigest()[:16]


def _duong(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(GOC))
    except ValueError:
        return str(p)


def _doc_json(p: Path, ten: str, loi: list[str]):
    """Đọc một tệp JSON; ⛔ đọc được ⇒ MỘT dòng lỗi (`S0-R1-04`, ⛔ traceback) và trả `_HONG`."""
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:        # vắng/quyền ⊂ OSError · JSON/UTF-8 hỏng ⊂ ValueError
        loi.append(f"{ten} {_duong(p)}: ⛔ đọc được — {type(e).__name__}: " + " ".join(str(e).split()))
        return _HONG


def _co_chu(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _so_nguyen(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)   # ⛔ True/False: bool là con của int


def _ngay_that(v) -> bool:
    if not (isinstance(v, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", v)):
        return False
    try:
        date.fromisoformat(v)
    except ValueError:                         # 2026-02-30 đúng khuôn mà ⛔ có thật
        return False
    return True


def _doc_nhan(tep: Path, van_tay: dict, tap_thieu: set[int], loi: list[str]) -> dict[int, str] | None:
    """Tệp nhãn DT1b → `{dong_sheet: nhãn}` (chỉ dòng CÓ nhãn). Vắng ⇒ `{}` (DT1b chưa về — mọi dòng thiếu
    là "chưa có nhãn", ⛔ lỗi). Có mà hỏng ⇒ `None` + lỗi (mỗi luật một dòng; bài thử có ca phá riêng)."""
    if not tep.exists():
        return {}
    d = _doc_json(tep, "tệp nhãn", loi)
    if d is _HONG:
        return None
    if not (isinstance(d, dict) and isinstance(d.get("van_tay"), dict) and isinstance(d.get("dong_thieu"), list)):
        loi.append(f"tệp nhãn {_duong(tep)}: cấu trúc sai — cần "
                   "{'van_tay': {'thieu', 'nguoc'}, 'dong_thieu': [{'dong_sheet', 'nhan'}]}")
        return None
    truoc = len(loi)
    for tap, ten in (("thieu", "thiếu"), ("nguoc", "ngược")):
        if d["van_tay"].get(tap) != van_tay[tap]:
            loi.append(f"tệp nhãn: vân tay tập {ten} — tệp ghi {d['van_tay'].get(tap)!r} · ảnh hôm nay "
                       f"{van_tay[tap]!r} — nhãn của một tập dòng KHÁC")
    nhan: dict[int, str] = {}
    da_thay: set[int] = set()
    for i, x in enumerate(d["dong_thieu"]):
        ds = x.get("dong_sheet") if isinstance(x, dict) else None
        if not _so_nguyen(ds):
            loi.append(f"tệp nhãn: dong_thieu[{i}] cần dong_sheet là số nguyên — có {ds!r}")
            continue
        if ds not in tap_thieu:
            loi.append(f"tệp nhãn: dong_sheet {ds} ngoài tập {len(tap_thieu)} dòng thiếu")
            continue
        if ds in da_thay:
            loi.append(f"tệp nhãn: dong_sheet {ds} trùng — một dòng chỉ một nhãn")
            continue
        da_thay.add(ds)
        n = x.get("nhan")
        if n is None:
            continue                           # null = chưa có nhãn (đỏ), ⛔ lỗi
        if not _co_chu(n):
            loi.append(f"tệp nhãn: dong_sheet {ds} — nhãn phải là chuỗi có chữ hoặc null, có {n!r}")
            continue
        nhan[ds] = n
    return None if len(loi) > truoc else nhan


def _doc_so(tep: Path, loi: list[str]) -> list[dict] | None:
    """Sổ lý do → danh sách chữ ký đã kiểm. Vắng/hỏng ⇒ `None` + lỗi (mỗi luật một dòng)."""
    d = _doc_json(tep, "sổ lý do", loi)
    if d is _HONG:
        return None
    if not (isinstance(d, dict) and isinstance(d.get("chu_ky"), list)):
        loi.append(f"sổ lý do {_duong(tep)}: cấu trúc sai — cần {{'chu_ky': [{{{', '.join(KHOA_CHU_KY)}}}]}}")
        return None
    truoc = len(loi)
    for i, c in enumerate(d["chu_ky"]):
        if not (isinstance(c, dict) and set(c) == set(KHOA_CHU_KY)):
            loi.append(f"sổ lý do: chu_ky[{i}] khoá phải đúng {KHOA_CHU_KY} — có "
                       f"{tuple(sorted(c)) if isinstance(c, dict) else type(c).__name__}")
            continue
        if not _co_chu(c["nhan"]):
            loi.append(f"sổ lý do: chu_ky[{i}] nhãn phải là chuỗi có chữ — có {c['nhan']!r}")
        if not (_so_nguyen(c["so_dong"]) and c["so_dong"] > 0):
            loi.append(f"sổ lý do: chu_ky[{i}] so_dong phải là số nguyên > 0 — có {c['so_dong']!r}")
        if not _co_chu(c["nguoi_ky"]):
            loi.append(f"sổ lý do: chu_ky[{i}] người ký phải là chuỗi có chữ — có {c['nguoi_ky']!r}")
        if not _ngay_that(c["ngay"]):
            loi.append(f"sổ lý do: chu_ky[{i}] ngày phải là YYYY-MM-DD có thật — có {c['ngay']!r}")
    dem = Counter(c["nhan"] for c in d["chu_ky"] if isinstance(c, dict) and isinstance(c.get("nhan"), str))
    for n, k in sorted(dem.items()):
        if k > 1:
            loi.append(f"sổ lý do: nhãn {n!r} ký trùng {k} lần — một nhãn một chữ ký")
    return None if len(loi) > truoc else d["chu_ky"]


def phan_hd1(theo_ky: dict, thieu: list[tuple[int, str]], van_tay: dict,
             tep_nhan: Path = NHAN, tep_so: Path = SO_LY_DO) -> tuple[dict | None, list[str]]:
    """Phán HD1 theo kỳ → (khối `dat_hd1`, lỗi). Đầu vào hỏng ⇒ (None, lỗi): ⛔ phán kỳ nào (Đ5).

    `theo_ky` — `{kỳ: {"co", "chay", "o_parity", "o_parity_khop", …}}` (bốn số của `do()`);
    `thieu`   — `[(dong_sheet, kỳ)]` dòng sổ ⛔ ghép 1-1; `van_tay` — `{"thieu", "nguoc"}` tính từ ảnh."""
    loi: list[str] = []
    cac_ky = sorted(theo_ky)
    thieu_ky: dict[str, list[int]] = defaultdict(list)
    for d, k in thieu:
        thieu_ky[k].append(d)
    # Phòng thủ chồng (Đ2 — hai nguồn cho cùng một số): `có − chạy` của kỳ ↔ dòng thiếu liệt kê.
    for k in cac_ky:
        a = theo_ky[k].get("co", 0) - theo_ky[k].get("chay", 0)
        if a != len(thieu_ky.get(k, ())):
            loi.append(f"phòng thủ: kỳ {k} có − chạy = {a} · dòng thiếu liệt kê {len(thieu_ky.get(k, ()))}")
    if set(thieu_ky) - set(cac_ky):
        loi.append(f"phòng thủ: dòng thiếu thuộc kỳ ngoài bảng {sorted(set(thieu_ky) - set(cac_ky))}")
    nhan = _doc_nhan(tep_nhan, van_tay, {d for d, _ in thieu}, loi)
    chu_ky = _doc_so(tep_so, loi)
    if nhan is not None and chu_ky is not None:
        dem_nhan = Counter(nhan.values())
        for c in chu_ky:
            if dem_nhan.get(c["nhan"], 0) != c["so_dong"]:
                loi.append(f"sổ lý do: chữ ký {c['nhan']!r} ({c['nguoi_ky']} · {c['ngay']}) ghi số dòng {c['so_dong']} "
                           f"· tệp nhãn có {dem_nhan.get(c['nhan'], 0)} dòng thiếu mang nhãn ấy — chữ ký cũ, ký lại")
    if loi:
        return None, loi

    da_ky = {c["nhan"] for c in chu_ky}
    ket: dict[str, dict] = {}
    for k in cac_ky:
        x, ds = theo_ky[k], thieu_ky.get(k, [])
        ky = sum(1 for d in ds if nhan.get(d) in da_ky)
        dong_100 = not ds
        o_100 = x.get("o_parity", 0) > 0 and x.get("o_parity_khop", 0) == x.get("o_parity", 0)   # Đ3: 0/0 ⛔ 100 %
        ket[k] = {"dat": (dong_100 or ky == len(ds)) and o_100, "thieu": len(ds),
                  "co_nhan": sum(1 for d in ds if d in nhan), "da_ky": ky,
                  "dong_100": dong_100, "o_100": o_100}
    ky_dat = [k for k in cac_ky if ket[k]["dat"]]
    return {
        "_luat": ("kỳ ĐẠT HD1 ⇔ (dòng 1-1 100 % hoặc mọi dòng thiếu của kỳ có nhãn ĐÃ KÝ trong sổ lý do) "
                  "∧ (ô Final 7 khối 100 %, mẫu số > 0). ⛔ gồm chế độ tự sinh (H15). AP v3.1.2 §5.3.1 HD1."),
        "mau_so": {"so_ky": len(cac_ky), "dong_so": sum(theo_ky[k].get("co", 0) for k in cac_ky),
                   "dong_thieu": len(thieu)},
        "tep_nhan": {"duong": _duong(tep_nhan), "co": tep_nhan.exists()},
        "so_ly_do": _duong(tep_so),
        "so_chu_ky": len(chu_ky),
        "van_tay": dict(van_tay),
        "dem": {"thieu": len(thieu), "co_nhan": len(nhan),
                "da_ky": sum(1 for v in nhan.values() if v in da_ky)},
        "so_ky_dat": len(ky_dat),
        "ky_dat": ky_dat,
        "theo_ky": ket,
    }, []


def do(nhan: Path = NHAN, so_ly_do: Path = SO_LY_DO) -> dict:
    loi: list[str] = []

    def kiem(ten, co, mong):
        if co != mong:
            loi.append(f"{ten}: đo {co!r} · mong {mong!r}")

    # ① sổ AS-IS · ITL Ledge (Classifying / MID / Final × 7 khối, kỳ đã dựng lại)
    g = _nap("itl_ledge_adjustment.json")
    kiem("checksum itl_ledge_adjustment", _sha(g["dong"], g["bang_gia_tri"]),
         MONG["checksum"]["itl_ledge_adjustment.json"])
    idx = {n: i for i, n in enumerate(g["cot"])}
    bang = g["bang_gia_tri"]

    def val(h, ten):
        i = h[idx[ten]]
        return None if i == -1 else bang[i]

    so = []                                   # (dong_sheet, ky, {khoi: (cls, None, mid, fin)})
    for h in g["dong"]:
        so.append((h[0], h[1], {k: (val(h, f"{k}_classifying"), None, val(h, f"{k}_mid"),
                                    val(h, f"{k}_final")) for k in KHOI}))
    kiem("số dòng sổ", len(so), MONG["so_dong_so"])
    ky_cua_dong = {d: k for d, k, _ in so}
    cac_ky = sorted({k for _, k, _ in so})
    kiem("số kỳ", len(cac_ky), MONG["so_ky"])

    # ② dòng FLS dựng lại ↔ dòng sổ (khoá Số CT · PS Nợ · PS Có · TK · tiền tệ)
    c = _nap("classifying_vs_canon.json")
    kiem("checksum classifying_vs_canon", c["checksum_noi_dung"], MONG["checksum"]["classifying_vs_canon.json"])
    ci = {n: i for i, n in enumerate(c["cot"])}
    canon_ve_so = {r[ci["dong_canon"]]: r[ci["dong_so"]] for r in c["dong"]}
    so_co_canon = set(canon_ve_so.values())
    kiem("số dòng ghép canon", len(so_co_canon), MONG["so_dong_ghep_canon"])

    # ③ ghép bank ↔ PM bằng CHÍNH mã FLS
    p = _nap("pm_join.json")
    kiem("checksum pm_join", p["checksum_noi_dung"], MONG["checksum"]["pm_join.json"])
    bank = [DongBank(x["dong"], canon_ref(x["ref_tho"]), D(x["tien"]), x["cur"]) for x in p["bank"]]
    pm = [DongPM(x["dong"], x["slip"], x["line"], D(x["tien"]) if x["tien"] else None, x["cur"],
                 x["status"], canon_ref(x["ref_tho"]), x["hd"] or None, x["cdt1"] or None) for x in p["pm"]]
    nhom, tk = xep_ca_lat(bank, pm)
    kiem("số dòng bank", tk.dong_bank, MONG["so_dong_bank"])
    kiem("số dòng PM", len(pm), MONG["so_dong_pm"])
    kiem("bank không có mã", tk.khong_co_ma, MONG["khong_co_ma"])
    kiem("bank không thấy mã PM", tk.khong_thay_ma_PM, MONG["khong_thay_ma_PM"])
    kiem("dòng theo hình", dict(tk.dong_theo_hinh), MONG["dong_theo_hinh"])
    hinh_cua_bank: dict[int, str] = {}
    line_cua_bank: dict[int, set] = defaultdict(set)
    for n in nhom:
        for b in n.bank:
            hinh_cua_bank[b.dong_sheet] = n.hinh
        if n.ghep_duoc:
            for dong_b, line, _t in moi_noi(n):
                line_cua_bank[dong_b].add(line)

    # ④ từng kỳ
    o = {k: Counter() for k in cac_ky}
    khoi_ky = {k: Counter() for k in cac_ky}           # ô người điền theo khối: '<khối>:go' · '<khối>:md'
    line_ky: dict[str, set] = {k: set() for k in cac_ky}
    tong_o = khop_o = 0
    loai = 0
    for dong, ky, bon in so:
        x = o[ky]
        x["co"] += 1
        if dong in so_co_canon:
            x["chay"] += 1
        cls_hd = _chuan(bon["hd"][0])
        if cls_hd and not la_o_loi(cls_hd) and not may_khong_tra_loi(cls_hd):
            x["map_now"] += 1
        for kh, (cls, _m, mid, fin) in bon.items():
            sc, sf = _chuan(cls), _chuan(fin)
            if la_o_loi(sc) or la_o_loi(sf):
                continue
            if may_khong_tra_loi(sc):
                if not sf:
                    x["o_trong"] += 1
                elif MAC_DINH_THEO_KHOI.get(kh) is not None and sf == MAC_DINH_THEO_KHOI[kh]:
                    x["o_mac_dinh"] += 1
                    khoi_ky[ky][f"{kh}:md"] += 1
                else:
                    x["o_go_that"] += 1
                    khoi_ky[ky][f"{kh}:go"] += 1
            elif sf and sf != sc:
                x["o_de"] += 1
        # parity: FLS tính lại Final (bỏ dòng tu_soi loại, ô lỗi là câu trả lời)
        if not soi_mot_dong(bon).giu:
            loai += 1
            x["loai_tu_soi"] += 1
            continue
        for kh, (cls, _m, mid, fin) in bon.items():
            if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):
                continue
            tinh = tinh_final(_chuan(cls) or None, _chuan(mid) or None)
            tong_o += 1
            x["o_parity"] += 1
            trung = _chuan(tinh) == _chuan(fin)
            if trung:
                khop_o += 1
                x["o_parity_khop"] += 1
            if kh == "hd":
                x["hd_parity"] += 1
                x["hd_parity_khop"] += trung
    kiem("parity ô", (khop_o, tong_o), MONG["parity_o"])
    kiem("dòng tu_soi loại", loai, MONG["dong_loai_tu_soi"])
    kiem("parity khối HD", (sum(o[k]["hd_parity_khop"] for k in cac_ky), sum(o[k]["hd_parity"] for k in cac_ky)), MONG["hd_parity"])
    tu_sinh = do_tu_sinh()
    kiem("tự sinh ô Final 2026-03", tu_sinh["o"], MONG["tu_sinh_o"])
    kiem("tự sinh khối HD 2026-03", tu_sinh["hd"], MONG["tu_sinh_hd"])
    kiem("tự sinh MID 2026-03", tu_sinh["mid"], MONG["tu_sinh_mid"])

    # mapping FLS + PM line theo kỳ (bank → dòng canon → dòng sổ → kỳ)
    bank_khong_ky = 0
    for b in bank:
        dso = canon_ve_so.get(b.dong_sheet)
        ky = ky_cua_dong.get(dso) if dso is not None else None
        if ky is None:
            bank_khong_ky += 1
            continue
        h = hinh_cua_bank.get(b.dong_sheet)
        if h in GHEP_DUOC:
            o[ky]["map_fls"] += 1
            line_ky[ky] |= line_cua_bank.get(b.dong_sheet, set())
        elif h in DAY_NGUOI:
            o[ky]["day_nguoi"] += 1
    for k in cac_ky:
        o[k]["pm_noi"] = len(line_ky[k])

    # ⑤ HD1 theo kỳ (H2): dòng thiếu = dòng sổ ⛔ ghép 1-1 — cùng phép trừ với DT1a, tập khoá bằng vân tay
    thieu = [(dong, ky) for dong, ky, _ in so if dong not in so_co_canon]
    van_tay = {"thieu": _van_tay_dong(d for d, _ in thieu),
               "nguoc": _van_tay_dong({b.dong_sheet for b in bank} - set(canon_ve_so))}
    hd1, loi_hd1 = phan_hd1({k: o[k] for k in cac_ky}, thieu, van_tay, nhan, so_ly_do)
    loi.extend(loi_hd1)
    if hd1 is not None:                        # đầu vào hỏng ⇒ loi_hd1 đã ĐỎ, ⛔ so MONG trên phán rỗng
        kiem("kỳ đạt HD1 (dat_hd1_theo_ky)", tuple(hd1["ky_dat"]), tuple(MONG.get("dat_hd1_theo_ky") or ()))

    if any(o[k]["co"] == 0 for k in cac_ky):   # Đ3 — mẫu số rỗng là KẾT QUẢ, ⛔ nền
        loi.append("có kỳ 0 dòng")
    if loi:
        raise SystemExit("⛔ VOI SỐ LƯỢNG ĐỎ — số đo khác số đã ghim, hoặc ⛔ đo được:\n  " + "\n  ".join(loi))

    tong = Counter()
    for k in cac_ky:
        tong.update(o[k])
    return {
        "_vi_sao": "Sinh bởi tools/do_voi_so_luong.py — chạy mã FLS lên ảnh đóng băng tests/fixture/. ⛔ sửa tay.",
        "nguon": {"so": g["nguon"], "so_dong_bang": g["ngay_dong_bang"], "canon": c["nguon"], "pm": p["nguon"],
                  "checksum": MONG["checksum"]},
        "ky": cac_ky,
        "theo_ky": {k: dict(o[k]) for k in cac_ky},
        "khoi_theo_ky": {k: {kh: [khoi_ky[k][f"{kh}:go"], khoi_ky[k][f"{kh}:md"]] for kh in KHOI} for k in cac_ky},
        "tong": dict(tong),
        "pm_tong": {"so_dong_pm": len(pm), "pm_noi_tong": len(set().union(*line_ky.values())),
                    "pm_co_ref": sum(1 for x in pm if x.ref)},
        "tu_sinh": tu_sinh,
        "bank_tong": {"dong_bank": tk.dong_bank, "khong_co_ma": tk.khong_co_ma,
                      "khong_thay_ma_PM": tk.khong_thay_ma_PM, "dong_theo_hinh": dict(tk.dong_theo_hinh),
                      "bank_khong_ky": bank_khong_ky},
        "dat_hd1": hd1,
    }


def do_tu_sinh() -> dict:
    """Chế độ TỰ SINH trên tháng duy nhất có cột Manual input (itl_ledge_2026_03.json, 584 dòng):
    MID_fls = tinh_mid(Classifying, Manual, mặc định khối) → Final_fls = tinh_final(Classifying, MID_fls), so Final sổ.
    ⛔ đọc MID của sổ — đây mới là phép đo "FLS tự mapping ra đúng quá khứ"."""
    from fls.ledger.final_rule import tinh_mid
    d = _nap("itl_ledge_2026_03.json")
    if len(d["dong"]) != d["so_dong"] or d["ky"] != "2026-03":
        raise SystemExit("⛔ ảnh 2026-03 khác khai")
    tong = khop = hd_t = hd_k = mid_k = 0
    for r in d["dong"]:
        for k in KHOI:
            cls, man, mid, fin = (r[f"{k}_{c}"] for c in ("classifying", "manual", "mid", "final"))
            if any(la_o_loi(_chuan(v)) for v in (cls, mid, fin) if v is not None):
                continue
            m2 = tinh_mid(_chuan(cls) or None, _chuan(man) or None, MAC_DINH_THEO_KHOI[k])
            f2 = tinh_final(_chuan(cls) or None, m2)
            tong += 1
            ok = _chuan(f2) == _chuan(fin)
            khop += ok
            mid_k += _chuan(m2) == _chuan(mid)
            if k == "hd":
                hd_t, hd_k = hd_t + 1, hd_k + ok
    return {"ky": "2026-03", "o": (khop, tong), "hd": (hd_k, hd_t), "mid": (mid_k, tong)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ghi", action="store_true")
    a = ap.parse_args()
    kq = do()
    print(f"{'kỳ':8s} {'có':>6s} {'chạy':>6s} {'mapNOW':>7s} {'mapFLS':>7s} {'ô gõ':>6s} {'ô mđ':>6s} {'trống':>6s} {'đè':>4s} {'parity':>13s}")
    for k in kq["ky"]:
        x = kq["theo_ky"][k]
        print(f"{k:8s} {x.get('co',0):6d} {x.get('chay',0):6d} {x.get('map_now',0):7d} {x.get('map_fls',0):7d} "
              f"{x.get('o_go_that',0):6d} {x.get('o_mac_dinh',0):6d} {x.get('o_trong',0):6d} {x.get('o_de',0):4d} "
              f"{x.get('o_parity_khop',0):6d}/{x.get('o_parity',0):<6d}")
    t = kq["tong"]
    print(f"{'Σ':8s} {t['co']:6d} {t['chay']:6d} {t['map_now']:7d} {t['map_fls']:7d} "
          f"{t['o_go_that']:6d} {t['o_mac_dinh']:6d} {t['o_trong']:6d} {t['o_de']:4d} {t['o_parity_khop']:6d}/{t['o_parity']}")
    print("PM:", kq["pm_tong"], "· bank:", kq["bank_tong"])
    # HD1 theo kỳ — Đ3: MẪU SỐ in TRƯỚC mọi tỷ lệ; Đ4: mỗi số mang nhãn NÓ ĐẾM GÌ
    h, ms, d = kq["dat_hd1"], kq["dat_hd1"]["mau_so"], kq["dat_hd1"]["dem"]
    print(f"HD1 · ① MẪU SỐ: {ms['so_ky']} kỳ · {ms['dong_so']} dòng sổ · {ms['dong_thieu']} dòng thiếu (sổ ⛔ ghép 1-1) "
          f"· tệp nhãn DT1b {h['tep_nhan']['duong']}: {'có' if h['tep_nhan']['co'] else 'VẮNG'} "
          f"· sổ lý do {h['so_ly_do']}: {h['so_chu_ky']} chữ ký")
    print(f"HD1 · ② dòng thiếu có nhãn {d['co_nhan']}/{d['thieu']} · có nhãn ĐÃ KÝ {d['da_ky']}/{d['thieu']}")
    print(f"HD1 · ③ kỳ đạt (dòng 1-1 100 % hoặc mọi dòng thiếu có nhãn ĐÃ KÝ — và ô Final 7 khối 100 %): "
          f"{h['so_ky_dat']}/{ms['so_ky']} · " + (" · ".join(h["ky_dat"]) or "—"))
    do_ = [k for k in kq["ky"] if not h["theo_ky"][k]["dat"]]
    print(f"HD1 · ④ kỳ đỏ {len(do_)}/{ms['so_ky']} (dòng thiếu · có nhãn · đã ký"
          + (" · ô khớp/ô" if any(not h["theo_ky"][k]["o_100"] for k in do_) else "") + "): "
          + (" · ".join(f"{k} {h['theo_ky'][k]['thieu']}·{h['theo_ky'][k]['co_nhan']}·{h['theo_ky'][k]['da_ky']}"
                        + ("" if h["theo_ky"][k]["o_100"] else
                           f" ô {kq['theo_ky'][k].get('o_parity_khop', 0)}/{kq['theo_ky'][k].get('o_parity', 0)}")
                        for k in do_) or "—"))
    if a.ghi:
        # tệp tạm + os.replace (`DT1a-R1-07`): đứt giữa chừng ⛔ để lại voi_so_luong.json cụt
        tam = RA.with_name(RA.name + ".tam")
        tam.write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tam, RA)
        print("✅ đã ghi", RA.relative_to(GOC))


if __name__ == "__main__":
    main()
