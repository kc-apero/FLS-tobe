"""Uoc tinh chi phi model / ngay de ra CCR daily — 4 agent cua AP Voi FLS v3.1.0.

⛔ So token la GIA DINH co khai bao (bang HO_SO duoi), chua do. Phep chay that cua
harness (`chay_eval.py`) ghi `usage` tung ca -> thay gia dinh bang so do.

Khoi luong lay tu RAW live `Transaction Mapping L1` (doc 17/11/2026):
  12/2025-09/2026: 15-25 dong/ngay · 10/2026: 33,5 · 11/2026: 36,0 · ngay dinh 89.
  Co giao dich ca 7 ngay/tuan => CCR daily chay ~30 lan/thang.
  Ty le dong co ma PM (cot H): 3.549/12.550 = 28% => ~72% dong can A3 dien tay.
"""
from __future__ import annotations
import json, math, sys

# USD / 1M token. Nguon: Anthropic (gia API 1P) · Google AI Studio pricing page (17/11/2026).
GIA = {
    "Opus 5.5":            dict(inp=4.00, out=20.00, cache_read=0.20, cache_write=5.00,  kieu="claude"),
    "Opus 5":              dict(inp=5.00, out=25.00, cache_read=0.50, cache_write=6.25,  kieu="claude"),
    "Gemini 3.8 Flash":    dict(inp=0.75, out=3.75,  cache_read=0.075, cache_write=None, kieu="gemini"),
    "Gemini 3.8 Flash (tu 01/2027)": dict(inp=1.50, out=7.50, cache_read=0.15, cache_write=None, kieu="gemini"),
    "Gemini 3.1 Pro":      dict(inp=2.00, out=12.00, cache_read=0.20, cache_write=None, kieu="gemini"),
}

# Ho so token moi agent, theo n = so dong giao dich trong ngay.
#   S: system + skill + dinh nghia tool (token)   T(n): so luot goi model
#   r: token ket qua tool moi luot                o: token ra moi luot (gom thinking o effort medium)
HO_SO = {
    "A1 Collect_raw_data":       dict(S=10_000, T=lambda n: 8 + math.ceil(n / 40),          r=1_500, o=500),
    "A2 Group Ledger + SI.MAP":  dict(S=14_000, T=lambda n: 6 + math.ceil(n / 10),          r=2_000, o=700),
    "A3 ITL Adjust (7 khoi)":    dict(S=30_000, T=lambda n: 4 + math.ceil(0.72 * n / 8),    r=3_500, o=1_800),
    "A4 Auditor (cong moi buoc)": dict(S=15_000, T=lambda n: 6 + math.ceil(n / 15),         r=3_000, o=900),
}
HE_SO_CHAY_LAI = 1.2      # cong A4 danh truot => chay lai mot phan
TY_LE_TRUNG_CACHE_GEMINI = 0.8   # implicit caching cua Gemini khong bao dam trung 100%
NGAY_THANG = 30


def mot_phien(ho, n):
    S, T, r, o = ho["S"], ho["T"](n), ho["r"], ho["o"]
    doc_cache = ghi_cache = khong_cache = 0
    for t in range(1, T + 1):
        if t == 1:
            ghi_cache += S + r            # luot dau: ghi ca tien to
        else:
            doc_cache += S + (t - 1) * r + (t - 2) * o
            ghi_cache += o + r            # output luot truoc + tool result moi
    return dict(luot=T, vao_doc_cache=doc_cache, vao_moi=ghi_cache, ra=T * o)


def tien(model, tk, he_so_ra=1.0):
    g = GIA[model]
    ra = tk["ra"] * he_so_ra
    if g["kieu"] == "claude":
        usd = tk["vao_doc_cache"] * g["cache_read"] + tk["vao_moi"] * g["cache_write"] + ra * g["out"]
    else:
        h = TY_LE_TRUNG_CACHE_GEMINI
        usd = (tk["vao_doc_cache"] * (h * g["cache_read"] + (1 - h) * g["inp"])
               + tk["vao_moi"] * g["inp"] + ra * g["out"])
    return usd / 1e6 * HE_SO_CHAY_LAI


def bang(n, he_so_ra=1.0):
    kq = {}
    for m in GIA:
        kq[m] = {a: tien(m, mot_phien(h, n), he_so_ra) for a, h in HO_SO.items()}
    return kq


if __name__ == "__main__":
    out = {"gia": GIA, "kich_ban": {}}
    for ten, n in (("thap (20 dong/ngay)", 20), ("co so (35 dong/ngay)", 35), ("dinh (90 dong/ngay)", 90)):
        print(f"\n=== {ten} ===")
        tk = {a: mot_phien(h, n) for a, h in HO_SO.items()}
        for a, v in tk.items():
            print(f"  {a:28s} luot={v['luot']:3d} vao(cache)={v['vao_doc_cache']:>9,} vao(moi)={v['vao_moi']:>7,} ra={v['ra']:>7,}")
        b = bang(n)
        print(f"  {'model':32s} {'A1':>7} {'A2':>7} {'A3':>7} {'A4':>7} {'USD/ngay':>9} {'USD/thang':>10}")
        for m, d in b.items():
            s = sum(d.values())
            print(f"  {m:32s} " + " ".join(f"{x:7.3f}" for x in d.values()) + f" {s:9.2f} {s*NGAY_THANG:10.0f}")
        # cau hinh tron: A1-A3 mot ho, A4 ho khac (AP: Auditor 'mo hinh khac ho')
        for a13, a4 in (("Opus 5.5", "Gemini 3.1 Pro"), ("Opus 5.5", "Gemini 3.8 Flash"),
                        ("Gemini 3.8 Flash", "Opus 5.5"), ("Gemini 3.1 Pro", "Opus 5.5")):
            s = sum(v for k, v in b[a13].items() if not k.startswith("A4")) + b[a4]["A4 Auditor (cong moi buoc)"]
            print(f"  TRON A1-3={a13} + A4={a4}: {s:.2f} USD/ngay · {s*NGAY_THANG:.0f} USD/thang")
        nhay = bang(n, he_so_ra=2.0)
        print("  do nhay: neu model ra gap doi token (thinking dai hon): "
              + " · ".join(f"{m} {sum(d.values()):.2f}" for m, d in nhay.items()))
        out["kich_ban"][ten] = {"n": n, "token": tk, "usd_ngay": {m: sum(d.values()) for m, d in b.items()},
                                "usd_theo_agent": b}
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "uoc_chi_phi.json", "w"),
              ensure_ascii=False, indent=1, default=str)
