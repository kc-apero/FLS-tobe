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

Chạy:  python tools/do_voi_so_luong.py            # in bảng, ⛔ ghi
       python tools/do_voi_so_luong.py --ghi      # ghi docs/ITL/_tools/voi_so_luong.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
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
    "checksum": {"itl_ledge_adjustment.json": "575c53379074c759",
                 "classifying_vs_canon.json": "7226ef112dbd00f7",
                 "pm_join.json": "6ec10945e6c1636a"},
}


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


def do() -> dict:
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
            if _chuan(tinh) == _chuan(fin):
                khop_o += 1
                x["o_parity_khop"] += 1
    kiem("parity ô", (khop_o, tong_o), MONG["parity_o"])
    kiem("dòng tu_soi loại", loai, MONG["dong_loai_tu_soi"])

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

    if any(o[k]["co"] == 0 for k in cac_ky):   # Đ3 — mẫu số rỗng là KẾT QUẢ, ⛔ nền
        loi.append("có kỳ 0 dòng")
    if loi:
        raise SystemExit("⛔ VOI SỐ LƯỢNG ĐỎ — số đo khác số đã ghim:\n  " + "\n  ".join(loi))

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
        "bank_tong": {"dong_bank": tk.dong_bank, "khong_co_ma": tk.khong_co_ma,
                      "khong_thay_ma_PM": tk.khong_thay_ma_PM, "dong_theo_hinh": dict(tk.dong_theo_hinh),
                      "bank_khong_ky": bank_khong_ky},
    }


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
    if a.ghi:
        RA.write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
        print("✅ đã ghi", RA.relative_to(GOC))


if __name__ == "__main__":
    main()
