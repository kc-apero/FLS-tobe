"""Cham diem tat dinh — ⛔ khong LLM-judge. Moi bai tra (diem 0..1, chi_tiet)."""
from __future__ import annotations


def _s(x) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    return str(x).strip()


def cham_a1(dung, ra):
    td = {(_s(x.get("loai")), _s(x.get("cot"))) for x in ra.get("thay_doi", [])}
    tdd = {(x["loai"], x["cot"]) for x in dung["thay_doi"]}
    rd, rr = dung["ref_hieu_luc"], [_s(x) for x in ra.get("ref_hieu_luc", [])]
    ref = sum(1 for i, x in enumerate(rd) if i < len(rr) and rr[i] == x) / max(1, len(rd))
    if len(rr) != len(rd):
        ref *= min(len(rr), len(rd)) / max(len(rr), len(rd))
    ct = {"drift_dung": float(td == tdd), "ref_dung": ref, "dem_dung": float(ra.get("so_dong") == dung["so_dong"])}
    return sum(ct.values()) / 3, ct


def cham_a2(dung, ra):
    d = {x["ma"]: x["hinh"] for x in dung["nhom"]}
    r = {}
    for x in ra.get("nhom", []):
        r[_s(x.get("ma")).upper()] = _s(x.get("hinh")).upper()
    dung_n = sum(1 for k, h in d.items() if r.get(k) == h)
    thua = len(set(r) - set(d))
    sai_nguy = sum(1 for k, h in d.items() if h in ("D", "E", "F", "KHONG_GHEP") and r.get(k) in ("A", "B", "C"))
    ct = {"nhom_dung": dung_n, "tong": len(d), "ma_thua": thua, "ghep_bua (D/E/F->A/B/C)": sai_nguy}
    return dung_n / (len(d) + thua), ct


def cham_a3(dung, ra):
    d = {(x["dong"], x["khoi"]): x for x in dung["khoi"]}
    r = {(_s(x.get("dong")), _s(x.get("khoi"))): x for x in ra.get("khoi", [])}
    v = sum(1 for k, x in d.items() if k in r and _s(r[k].get("V")) == x["V"]) / len(d)
    u = sum(1 for k, x in d.items() if k in r and _s(r[k].get("U")) == x["U"]) / len(d)
    dd = {x["dong"]: x["hd"] for x in dung["de_xuat"]}
    rd = {_s(x.get("dong")): _s(x.get("hd")) for x in ra.get("de_xuat", [])}
    dx = sum(1 for k, h in dd.items() if rd.get(k) == h) / max(1, len(dd))
    doan = sum(1 for k, h in dd.items() if h == "ESCALATE" and rd.get(k) not in (None, "ESCALATE"))
    bo_sot = sum(1 for k, h in dd.items() if h != "ESCALATE" and rd.get(k) == "ESCALATE")
    ct = {"V_dung": round(v, 4), "U_dung": round(u, 4), "de_xuat_dung": round(dx, 4),
          "doan_thay_vi_day_nguoi": doan, "day_nguoi_thua": bo_sot}
    # Final (V) la so vao bao cao => trong so lon nhat
    return 0.5 * v + 0.2 * u + 0.3 * dx, ct


def cham_a4(dung, ra):
    d = {(x["loai"], x["khoa"]) for x in dung["loi"]}
    r = {(_s(x.get("loai")).upper(), _s(x.get("khoa"))) for x in ra.get("loi", [])}
    tp = len(d & r)
    p = tp / len(r) if r else 1.0
    rc = tp / len(d) if d else 1.0
    f1 = 0.0 if p + rc == 0 else 2 * p * rc / (p + rc)
    ct = {"dung": tp, "bao_sai": len(r - d), "bo_sot": len(d - r), "precision": round(p, 3), "recall": round(rc, 3)}
    return f1, ct


CHAM = {"A1": cham_a1, "A2": cham_a2, "A3": cham_a3, "A4": cham_a4}
