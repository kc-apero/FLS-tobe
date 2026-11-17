"""Cham ket qua FULL LUONG cua model voi dap_an/ — tat dinh, ⛔ khong LLM-judge.

  python cham_full.py ket_qua_tho/opus55.md ket_qua_tho/gemini_pro.md ...
      -> moi tep: diem 9 khoi + diem tong, ghi ket_qua_cham/<ten>.json (kem vi du o lech)
      -> nhieu tep: in bang so sanh

Tep ket qua = nguyen van cau tra loi cua model (markdown co 9 khoi `### <TEN>` + code block).
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

GOC = Path(__file__).parent
DA = GOC / "dap_an"
KHOI_RA = ["A1_KIEM_NGUON", "A2_LEDGER", "A2_GHEP", "A3_ITL", "A3_HANG_CHO", "R1_SO_DU", "R2_CF", "R3_PL", "A4_AUDIT"]
TRONG_SO = {"A1_KIEM_NGUON": 0.05, "A2_LEDGER": 0.10, "A2_GHEP": 0.15, "A3_ITL": 0.30, "A3_HANG_CHO": 0.10,
            "R1_SO_DU": 0.10, "R2_CF": 0.05, "R3_PL": 0.05, "A4_AUDIT": 0.10}
KHOI7 = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")
NGAY = [f"2026-10-{d:02d}" for d in range(1, 8)]
SAI_TIEN, SAI_MUSD = Decimal("0.005"), Decimal("0.000000015")
VI_DU = 15


# ------------------------------------------------------------------ doc
def tach_khoi(txt: str) -> dict[str, str]:
    out = {}
    for ten in KHOI_RA:
        m = re.search(r"^#+\s*" + ten + r"\b.*?\n```[a-zA-Z]*\s*\n(.*?)```", txt, re.S | re.M)
        if m:
            out[ten] = m.group(1)
    return out


def doc_csv_txt(s: str) -> list[dict]:
    return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(io.StringIO(s.strip()))]


def doc_csv(p: Path) -> list[dict]:
    return doc_csv_txt(p.read_text(encoding="utf-8"))


def so(x):
    try:
        return Decimal(str(x).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None


def bang_so(a, b, tol):
    x, y = so(a), so(b)
    return x is not None and y is not None and abs(x - y) <= tol


def chu(x) -> str:
    return (x or "").strip()


def f1(dung: set, ra: set):
    tp = len(dung & ra)
    p = tp / len(ra) if ra else (1.0 if not dung else 0.0)
    r = tp / len(dung) if dung else 1.0
    return (0.0 if p + r == 0 else 2 * p * r / (p + r)), tp, len(ra - dung), len(dung - ra)


# ------------------------------------------------------------------ cham tung khoi
def cham_bang(dung: list[dict], ra: list[dict], khoa, cot_so: dict, cot_chu: list, ten: str):
    """So tung o theo khoa. Diem = 0,2·F1(khoa) + 0,8·(o dung / o mong doi)."""
    d = {khoa(x): x for x in dung}
    r = {}
    for x in ra:
        try:
            r.setdefault(khoa(x), x)
        except KeyError:
            continue
    fk, tp, thua, thieu = f1(set(d), set(r))
    o = dung_o = 0
    lech, theo_cot = [], {}
    for k, x in d.items():
        y = r.get(k)
        for c in list(cot_so) + cot_chu:
            o += 1
            ok = y is not None and (bang_so(x.get(c), y.get(c), cot_so[c]) if c in cot_so
                                    else chu(x.get(c)) == chu(y.get(c)))
            dung_o += ok
            tc = theo_cot.setdefault(c, [0, 0])
            tc[0] += ok
            tc[1] += 1
            if not ok and len(lech) < VI_DU:
                lech.append({"khoa": str(k), "cot": c, "dap_an": x.get(c), "model": None if y is None else y.get(c)})
    ct = {"khoa_dung": tp, "khoa_thua": thua, "khoa_thieu": thieu, "o_dung": dung_o, "o_tong": o,
          "dung_theo_cot": {c: f"{a}/{b}" for c, (a, b) in theo_cot.items()}, "vi_du_lech": lech}
    return 0.2 * fk + 0.8 * (dung_o / o if o else 1.0), ct


def cham_a1(dung, txt):
    ra = json.loads(txt)
    kiem, lech = [], []
    rs = {x.get("ma_sheet"): x for x in ra.get("sheet", [])}
    for s in dung["sheet"]:
        y = rs.get(s["ma_sheet"], {})
        for c in ("tk", "ngan_hang", "cur", "le", "so_dong"):
            ok = str(y.get(c)) == str(s[c])
            kiem.append(ok)
            if not ok:
                lech.append({"sheet": s["ma_sheet"], "cot": c, "dap_an": s[c], "model": y.get(c)})
        td = {(x["loai"], x["cot"]) for x in s["thay_doi"]}
        tr = {(str(x.get("loai")), str(x.get("cot"))) for x in y.get("thay_doi", [])}
        kiem.append(td == tr)
        if td != tr:
            lech.append({"sheet": s["ma_sheet"], "cot": "thay_doi", "dap_an": sorted(td), "model": sorted(tr)})
    for c in ("pe_lines", "pi_lines", "pm_lines", "h1000_lines", "plt_lines"):
        ok = str(ra.get(c)) == str(dung[c])
        kiem.append(ok)
        if not ok:
            lech.append({"cot": c, "dap_an": dung[c], "model": ra.get(c)})
    return sum(kiem) / len(kiem), {"dung": sum(kiem), "tong": len(kiem), "vi_du_lech": lech}


def cham_tap(dung_set, ra_set, ten):
    f, tp, thua, thieu = f1(dung_set, ra_set)
    return f, {"dung": tp, "bao_thua": sorted(map(str, ra_set - dung_set))[:VI_DU],
               "bo_sot": sorted(map(str, dung_set - ra_set))[:VI_DU], "so_thua": thua, "so_sot": thieu}


def cham(txt: str) -> dict:
    kh = tach_khoi(txt)
    kq = {}
    for ten in KHOI_RA:
        if ten not in kh:
            kq[ten] = {"diem": 0.0, "chi_tiet": {"loi": "khong tim thay khoi"}}
            continue
        try:
            s = kh[ten]
            if ten == "A1_KIEM_NGUON":
                d, ct = cham_a1(json.loads((DA / "a1_kiem_nguon.json").read_text(encoding="utf-8")), s)
            elif ten == "A2_LEDGER":
                d, ct = cham_bang(doc_csv(DA / "a2_ledger.csv"), doc_csv_txt(s), lambda x: x["id"],
                                  {"ps_no": SAI_TIEN, "ps_co": SAI_TIEN}, ["ngay", "tk", "le", "cur", "ref"], ten)
            elif ten == "A2_GHEP":
                d, ct = cham_bang(doc_csv(DA / "a2_ghep.csv"), doc_csv_txt(s), lambda x: x["ma"].upper(),
                                  {"so_bank": Decimal(0), "so_nguon": Decimal(0)}, ["nguon", "hinh"], ten)
            elif ten == "A3_ITL":
                cot_chu = ["ngay", "tk", "le", "cur", "nguon"] + [f"{k}_{x}" for k in KHOI7 for x in ("T", "V")] + \
                          ["AU", "AV", "AW", "work_status"]
                d, ct = cham_bang(doc_csv(DA / "a3_itl_adjust.csv"), doc_csv_txt(s), lambda x: x["itl_id"],
                                  {"ps_no": SAI_TIEN, "ps_co": SAI_TIEN}, cot_chu, ten)
                tc = ct["dung_theo_cot"]
                ct["Final_7_khoi"] = {k: tc[f"{k}_V"] for k in KHOI7}
            elif ten == "A3_HANG_CHO":
                dd = {(x["itl_id"], x["ly_do"]) for x in doc_csv(DA / "a3_hang_cho.csv")}
                rr = {(x.get("itl_id", ""), x.get("ly_do", "")) for x in doc_csv_txt(s)}
                d, ct = cham_tap(dd, rr, ten)
            elif ten == "R1_SO_DU":
                d, ct = cham_bang(doc_csv(DA / "r1_so_du.csv"), doc_csv_txt(s), lambda x: (x["tk"], x["ngay"]),
                                  {c: SAI_TIEN for c in ("dau_ky", "ps_no", "ps_co", "cuoi_ky", "ccr_go", "dif")}, [], ten)
            elif ten == "R2_CF":
                d, ct = cham_bang(doc_csv(DA / "r2_cf.csv"), doc_csv_txt(s), lambda x: (x["le"], x["hd"]),
                                  {c: SAI_MUSD for c in NGAY + ["tong"]}, [], ten)
            elif ten == "R3_PL":
                d, ct = cham_bang(doc_csv(DA / "r3_pl.csv"), doc_csv_txt(s), lambda x: x["dong"],
                                  {c: SAI_MUSD for c in NGAY + ["tong"]}, [], ten)
            elif ten == "A4_AUDIT":
                dd = {(x["loai"], x["khoa"]) for x in json.loads((DA / "a4_audit.json").read_text(encoding="utf-8"))["loi"]}
                rr = {(str(x.get("loai")), str(x.get("khoa"))) for x in json.loads(s).get("loi", [])}
                d, ct = cham_tap(dd, rr, ten)
            kq[ten] = {"diem": round(d, 4), "chi_tiet": ct}
        except Exception as e:      # noqa: BLE001 — khoi hong dinh dang = 0 diem, co ly do
            kq[ten] = {"diem": 0.0, "chi_tiet": {"loi": f"{type(e).__name__}: {e}"[:300]}}
    kq["TONG"] = round(sum(kq[k]["diem"] * w for k, w in TRONG_SO.items()), 4)
    return kq


def main(tep: list[str]):
    ra = GOC / "ket_qua_cham"
    ra.mkdir(exist_ok=True)
    tong = {}
    for t in tep:
        p = Path(t)
        kq = cham(p.read_text(encoding="utf-8"))
        (ra / f"{p.stem}.json").write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
        tong[p.stem] = kq
    w = max(12, max(len(k) for k in tong))
    print(f"{'khoi':16s} {'trong so':>8} " + " ".join(f"{k:>{w}}" for k in tong))
    def so_lech(ct):
        if "o_tong" in ct:
            return ct["o_tong"] - ct["o_dung"] + ct["khoa_thua"]
        if "so_sot" in ct:
            return ct["so_sot"] + ct["so_thua"]
        if "tong" in ct:
            return ct["tong"] - ct["dung"]
        return "hong"

    print("(diem % · [so o/muc lech tuyet doi] — 0 lech moi la DAT)")
    for ten in KHOI_RA + ["TONG"]:
        ts = f"{TRONG_SO.get(ten, 1):.2f}"
        if ten == "TONG":
            print(f"{ten:16s} {ts:>8} " + " ".join(f"{v[ten]:>{w}.1%}" for v in tong.values()))
        else:
            print(f"{ten:16s} {ts:>8} " + " ".join(
                f"{format(v[ten]['diem'], '.1%') + ' [' + str(so_lech(v[ten]['chi_tiet'])) + ']':>{w}}"
                for v in tong.values()))
    for k, v in tong.items():
        itl = v["A3_ITL"]["chi_tiet"]
        if "Final_7_khoi" in itl:
            print(f"\n[{k}] ITL Final dung theo khoi: " + " · ".join(f"{a} {b}" for a, b in itl["Final_7_khoi"].items()))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("dung: python cham_full.py <tep_ket_qua.md> [...]")
    main(sys.argv[1:])
