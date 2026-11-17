"""Sinh BO DU LIEU FULL LUONG (gia lap) + DAP AN, tu cung bo luat `luat.py`.

  input/   -> dua cho model:  PE · PI · PM (phieu chi) · 4 sheet bank/quy · so du dau · CCR go tay ·
                              H1000 (luong) · PLT (GI/OMC/SC/PS) · Mapping Master · lich su vendor · ty gia
  dap_an/  -> ⛔ KHONG dua cho model: ledger · ghep · ITL adjust · hang cho · R1/R2/R3 CCR · kiem nguon · audit

⛔ Moi ten, ma, so tien deu BIA. Ky: 01–07/10/2026. Chay: python sinh_full.py [seed]
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from luat import (BAN_KHAI, DONG_PL_HD, DONG_PL_TONG, IH, KHOI, NA, NGAY, allocate, canon_ref,
                  dien_tay, doc_ten_sheet, drift, final, lam_tron, mid, musd, ref_hieu_luc, xep_hinh)

GOC = Path(__file__).parent
D = Decimal

CDT = ["SHQ2 | Headquarters2", "COR | Core Apps", "CVL | Venture Lab", "CSM | Studio M",
       "CAH | Apps Hub", "ASA | Asia Studio", "CMN | Media Network"]
MM = [  # hd, nhom PL, K (can phan bo), L (phuong phap)
    ("GI | Gross Inflow", "GI", "", ""), ("OMC | Online Marketing Cost", "OMC", "", ""),
    ("API | API", "API", "", ""), ("SC | Server Cost", "SC", "", ""), ("LC | License Cost", "LC", "", ""),
    ("PS | Platform Service", "PS", "", ""),
    ("NIS | Net Income Salary", "HR", "Need to Allocate to CFA2", "By NOEM"),
    ("INT | Insurance", "HR", "Need to Allocate to CFA2", "By NOEM"),
    ("COM | Commission", "HR", "Need to Allocate to CFA2", "By NOEM"),
    ("PIT | Personal Income Tax", "HR", "Need to Allocate to CFA2", "By NOEM"),
    ("MC | Marketing Cost", "MC", "Need to Allocate to CFA2", "By GI"),
    ("OGA | GAC - Other", "GAC", "Need to Allocate to CFA2", "By NOEM"),
    ("FI | Financial Income", "FI", "", ""), ("BF | Bank Fee", "BF", "Need to Allocate to CFA2", "By LE"),
    ("CIT | Corporate Income Tax", "CIT", "", ""), ("NB | Lưu chuyển nội bộ", "NB", "", ""),
]
HD_PE = ["API | API", "SC | Server Cost", "LC | License Cost", "MC | Marketing Cost", "OGA | GAC - Other",
         "OMC | Online Marketing Cost"]
HD_LA = "XYZ | Hạng mục chưa khai"
PAY = ["Thanh toán (Regular)", "Tạm ứng (Advance)", "Khẩn (Urgent)"]
SHEET = {"S1": "R | 112001_ACB VND_HQ1", "S2": "R | 112002_VCB USD_HQ1",
         "S3": "R | 112003_TCB VND_SG2", "S4": "R | 111001_QUY VND_HQ1"}
SO_DU_DAU = {"S1": D("20000000000"), "S2": D("850000.00"), "S3": D("5000000000"), "S4": D("200000000")}


class Bo:
    def __init__(self, seed):
        self.r = random.Random(seed)
        self.pe, self.pi, self.pm, self.h1000, self.plt = [], [], [], [], []
        self.bank = {k: [] for k in SHEET}     # dong tho, chua STT
        self.n_pe = self.n_ft = 0
        self.vendor = {f"VDX{i:03d}": {"hd": self.r.choice(HD_PE), "cdt1": self.r.choice(CDT)} for i in range(1, 41)}
        ds = sorted(self.vendor)
        self.lich_su = {v: self.vendor[v] for v in ds[:24]}       # 24 vendor co lich su
        self.vendor_moi = ds[24:]                                   # 16 vendor chua co lich su

    # ------------------------------------------------------------ tien ich
    def ft(self, ngay):
        self.n_ft += 1
        return f"FT26{int(ngay[5:7]) * 31 + int(ngay[8:]):03d}{self.r.randint(10**6, 10**7 - 1)}{self.n_ft:02d}"

    def tien(self, cur, lo=1, hi=400):
        return D(self.r.randint(lo, hi) * 250_000) if cur == "VND" else D(self.r.randint(5_000, 900_000)) / 100

    def bien_dang(self, ma):
        return self.r.choice([ma, ma.lower(), ma[:4] + " " + ma[4:], ma[:4] + "-" + ma[4:], ma + " "])

    def them_bank(self, s, ngay, dien_giai, no=D(0), co=D(0), ref="", ref_adj="", so_ct=None):
        self.bank[s].append({"Ngày": ngay, "Số CT": so_ct or f"CT{self.r.randint(100000, 999999)}",
                             "Diễn giải": dien_giai, "PS Nợ": no, "PS Có": co,
                             "Reference number": ref, "Reference number_adjust": ref_adj})

    def phieu(self, ngay, cur, so_dong=1, vendor=None, hd=None, tien=None, le="HQ1", ref=None, co_pi=None):
        """Mot phieu PE (N dong) -> N dong PM cung MOT ma tham chieu. Tra (ref, tong tien, ds dong PM)."""
        self.n_pe += 1
        ref = ref or self.ft(ngay)
        v = vendor or self.r.choice(list(self.vendor))
        out = []
        for k in range(1, so_dong + 1):
            pel = f"PE-{self.n_pe:04d}-{k}"
            t = tien[k - 1] if isinstance(tien, list) else (tien or self.tien(cur))
            info = self.vendor[v]
            pil = ""
            if co_pi if co_pi is not None else self.r.random() < 0.6:
                pil = f"PI-{self.n_pe:04d}-{k}"
                m1 = self.r.choice([7, 8, 9, 10])
                self.pi.append({"ID PILine": pil, "ID PELine": pel, "Bắt đầu dịch vụ": f"2026{m1:02d}",
                                "Kết thúc dịch vụ": f"2026{min(12, m1 + self.r.choice([0, 1, 2])):02d}",
                                "Hoá đơn": self.r.choice(["Có hoá đơn", "Chưa có hoá đơn"])})
            self.pe.append({"ID PESlip": f"PE-{self.n_pe:04d}", "ID PELine": pel, "Ngày đề nghị": ngay,
                            "Mã đối tác": v, "Budget Code (HDCode)": hd or info["hd"],
                            "Chủ dự toán (CDT1)": self.r.choice(CDT) if so_dong > 1 else info["cdt1"],
                            "Loại giao dịch": self.r.choice(PAY), "Số tiền": t, "Tiền tệ": cur, "ID PILine": pil})
            out.append({"ID PMSlip": f"PM-{self.n_pe:04d}", "ID PMLine": f"PM-{self.n_pe:04d}-{k}",
                        "ID PELine": pel, "Pháp nhân trả": le, "Số tiền": t, "Tiền tệ": cur,
                        "Reference number": self.bien_dang(ref) if k == 1 else ref, "Status_Final": "Đã chi"})
        self.pm += out
        return ref, sum(x["Số tiền"] for x in out), v

    # ------------------------------------------------------------ kich ban 7 ngay
    def dung(self):
        r = self.r
        for i, ngay in enumerate(NGAY):
            dd = ngay.replace("-", "")
            for s, cur, le, n in (("S1", "VND", "HQ1", 5), ("S3", "VND", "SG2", 3), ("S2", "USD", "HQ1", 1)):
                for _ in range(n):                                  # A: 1 bank x 1 PM
                    ref, t, v = self.phieu(ngay, cur, le=le)
                    self.them_bank(s, ngay, f"TT {v} THEO DE NGHI", co=t, ref=ref)
            self.them_bank("S1", ngay, "PHI DICH VU SMS BANKING", co=D(11000))
            v = r.choice(list(self.lich_su))                        # chi quy co vendor lich su
            self.them_bank("S4", ngay, f"CHI TIEN MAT {v} VAN PHONG PHAM", co=D(r.randint(2, 40) * 50_000))
            if i in (1, 4):                                         # vendor co lich su, khong co PM
                v = r.choice(list(self.lich_su))
                self.them_bank("S1", ngay, f"CK {v} HOP DONG DICH VU", co=self.tien("VND"), ref=self.ft(ngay))
            if i in (2, 5):                                         # vendor moi, khong lich su -> hang cho
                v = r.choice(self.vendor_moi)
                self.them_bank("S3", ngay, f"CK {v} THANH TOAN", co=self.tien("VND"), ref=self.ft(ngay))
            if i == 0:                                              # ref_adjust thang
                for _ in range(2):
                    ref, t, v = self.phieu(ngay, "VND")
                    self.them_bank("S1", ngay, f"TT {v}", co=t, ref="FT26SAI" + str(r.randint(100, 999)), ref_adj=ref)
                ref, t, v = self.phieu(ngay, "VND", le="SG2")
                self.them_bank("S3", ngay, f"TT {v}", co=t, ref="", ref_adj=ref)
                self.them_bank("S3", ngay, "DONG TRONG", no=D(0), co=D(0))
            if i == 1:                                              # B: 1 bank x 3 PM, lech 600 VND (trong dung sai)
                ref, t, v = self.phieu(ngay, "VND", so_dong=3)
                self.them_bank("S1", ngay, f"TT GOP {v}", co=t + 600, ref=ref)
                # PLT GI: tien ve tu kho ung dung
                self.plt_nhom("GI", "PLT-STORE-A", ngay, "S2", 4, chieu="no")
            if i == 2:                                              # C: 2 bank x 1 PM (tra 2 lan)
                ref, t, v = self.phieu(ngay, "VND", tien=[D(480_000_000)], co_pi=True)
                self.them_bank("S1", ngay, f"TT DOT 1 {v}", co=D(200_000_000), ref=ref)
                self.c_ref = (ref, v)
                # NB: chuyen noi bo hai ve
                nb = f"NB-{dd}-1"
                self.them_bank("S1", ngay, "CHUYEN NOI BO HQ1 SANG SG2", co=D(500_000_000), ref=nb)
                self.them_bank("S3", ngay, "CHUYEN NOI BO NHAN TU HQ1", no=D(500_000_000), ref=nb)
                self.plt_nhom("PS", "PLT-SVC-B", ngay, "S1", 2, chieu="co")
                self.them_bank("S1", ngay, "PHI DICH VU SMS BANKING", co=D(11000))      # main() chep de thanh dong TRUNG
            if i == 3:
                ref, v = self.c_ref
                self.them_bank("S1", ngay, f"TT DOT 2 {v}", co=D(280_000_000), ref=ref)
                ref, t, v = self.phieu(ngay, "VND", le="SG2")              # F: lech qua dung sai
                self.them_bank("S3", ngay, f"TT {v}", co=t + D(2_000_000), ref=ref)
                self.plt_nhom("OMC", "PLT-ADS-C", ngay, "S2", 3, chieu="co")
                self.them_bank("S1", ngay, "RUT TIEN CHUYEN NOI BO NHAP QUY", co=D(50_000_000), ref=f"NB-{dd}-2")
                self.them_bank("S4", ngay, "NHAP QUY CHUYEN NOI BO TU ACB", no=D(50_000_000), ref=f"NB-{dd}-2")
                ref, t, v = self.phieu(ngay, "VND", hd=HD_LA, co_pi=False)   # HD khong co trong Mapping Master
                self.them_bank("S1", ngay, f"TT {v}", co=t, ref=ref)
            if i == 4:
                ref, t, v = self.phieu(ngay, "VND", so_dong=2, tien=[D(30_000_000), D(30_000_000)], le="SG2")  # D: 2x2
                self.them_bank("S3", ngay, f"TT {v} LAN 1", co=D(30_000_000), ref=ref)
                self.them_bank("S3", ngay, f"TT {v} LAN 2", co=D(30_000_000), ref=ref)
                self.luong(ngay)
                self.plt_nhom("SC", "PLT-CLOUD-D", ngay, "S2", 2, chieu="co")
                so = 4366190000000000                                         # ma so dai: Sheets doc thanh so khoa hoc
                ref, t, v = self.phieu(ngay, "VND", ref=str(so))
                self.pm[-1]["Reference number"] = "%.5E" % so
                self.them_bank("S1", ngay, f"TT {v} MA SO", co=t, ref=str(so))
                self.them_bank("S1", ngay, "DONG TRONG", no=D(0), co=D(0))
            if i == 5:
                ref, t, v = self.phieu(ngay, "USD")                           # E: PM USD, bank VND
                self.them_bank("S1", ngay, f"TT {v} QUY DOI", co=(t * 26300).quantize(D(1)), ref=ref)
                self.them_bank("S1", ngay, "NOP THUE TNDN QUY 3", co=D(300_000_000), ref=self.ft(ngay))
                self.plt_nhom("GI", "PLT-STORE-E", ngay, "S2", 3, chieu="no")
                self.them_bank("S4", ngay, "CHI TIEN MAT TIEP KHACH", co=D(1_500_000))
                self.them_bank("S2", ngay, "PHI DICH VU SWIFT", co=D("5.00"))
            if i == 6:
                self.them_bank("S1", ngay, "LAI TIEN GUI THANG 9", no=D(1_234_567))
                for _ in range(3):                                            # PM chua chi trong ky -> KHONG_GHEP
                    self.phieu(ngay, "VND")

    def plt_nhom(self, loai, vendor, ngay, s, n, chieu):
        cc = f"{vendor.split('-')[1][:3]}-{ngay.replace('-', '')}-1"
        cur = "USD" if s == "S2" else "VND"
        tong = D(0)
        for k in range(1, n + 1):
            t = self.tien(cur)
            tong += t
            su_dung = f"2026-09-{self.r.randint(1, 30):02d}"
            self.plt.append({"ID dòng": f"{loai}-{len(self.plt) + 1:03d}", "Loại": loai, "Vendor": vendor,
                             "Ngày sử dụng": su_dung, "Sản phẩm": f"APP-{self.r.randint(10, 99)}",
                             "Chủ dự toán (CDT1)": self.r.choice(CDT[1:]), "Số tiền": t, "Tiền tệ": cur,
                             "Combine Code": cc})
        if chieu == "no":
            self.them_bank(s, ngay, f"NHAN TIEN {vendor}", no=tong, ref=cc)
        else:
            self.them_bank(s, ngay, f"TT {vendor}", co=tong, ref=cc)

    def luong(self, ngay):
        for s, le in (("S1", "HQ1"), ("S3", "SG2")):
            so_ct = self.ft(ngay)
            tong = D(0)
            for hd, n in (("NIS | Net Income Salary", 3), ("INT | Insurance", 1), ("COM | Commission", 1)):
                for cdt in self.r.sample(CDT, n):
                    t = D(self.r.randint(40, 900) * 1_000_000)
                    tong += t
                    self.h1000.append({"ID dòng": f"H-{len(self.h1000) + 1:03d}", "Pháp nhân": le, "Kỳ lương": "202609",
                                       "Loại": hd.split(" |")[0], "Budget Code (HDCode)": hd, "Chủ dự toán (CDT1)": cdt,
                                       "Số tiền": t, "Số CT": so_ct})
            self.them_bank(s, ngay, f"CHI LUONG THANG 09 {le}", co=tong, ref=so_ct)
        so_ct = self.ft(ngay)                                         # PIT HQ1 nop rieng
        tong = D(0)
        for cdt in self.r.sample(CDT, 2):
            t = D(self.r.randint(10, 90) * 1_000_000)
            tong += t
            self.h1000.append({"ID dòng": f"H-{len(self.h1000) + 1:03d}", "Pháp nhân": "HQ1", "Kỳ lương": "202609",
                               "Loại": "PIT", "Budget Code (HDCode)": "PIT | Personal Income Tax",
                               "Chủ dự toán (CDT1)": cdt, "Số tiền": t, "Số CT": so_ct})
        self.them_bank("S1", ngay, "NOP THUE TNCN THANG 09", co=tong, ref=so_ct)


# ====================================================================== DAP AN
def tinh_dap_an(b: Bo, tieu_de: dict, ccr_go: dict):
    mm = {h: {"nhom": n, "K": k, "L": l} for h, n, k, l in MM}
    # ---------- A1
    a1 = {"sheet": [], "pe_lines": len(b.pe), "pi_lines": len(b.pi), "pm_lines": len(b.pm),
          "h1000_lines": len(b.h1000), "plt_lines": len(b.plt)}
    ledger, trung = [], []
    for s, ten in SHEET.items():
        meta = doc_ten_sheet(ten)
        dong = b.bank[s]
        a1["sheet"].append({"ma_sheet": s, "tk": meta["tk"], "ngan_hang": meta["bank"], "cur": meta["cur"],
                            "le": meta["le"], "thay_doi": drift(BAN_KHAI, tieu_de[s]),
                            "so_dong": sum(1 for d in dong if d["PS Nợ"] or d["PS Có"])})
        seen = set()
        for d in dong:
            if not (d["PS Nợ"] or d["PS Có"]):
                continue
            key = (d["Ngày"], d["Số CT"], d["Diễn giải"], d["PS Nợ"], d["PS Có"], d["Reference number"],
                   d["Reference number_adjust"])
            rid = f"{s}-{d['STT']}"
            if key in seen:
                trung.append(rid)
                continue
            seen.add(key)
            ledger.append({"id": rid, "ngay": d["Ngày"], "tk": meta["tk"], "le": meta["le"], "cur": meta["cur"],
                           "ps_no": d["PS Nợ"], "ps_co": d["PS Có"], "ref": ref_hieu_luc(d),
                           "dien_giai": d["Diễn giải"], "_s": s, "_stt": d["STT"]})
    # ---------- A2: ghep
    pe = {x["ID PELine"]: x for x in b.pe}
    pi = {x["ID PILine"]: x for x in b.pi}
    nguon = defaultdict(list)
    for x in b.pm:
        p = pe[x["ID PELine"]]
        p_i = pi.get(p["ID PILine"]) if p["ID PILine"] else None
        cls = {"hd": p["Budget Code (HDCode)"], "pay_type": p["Loại giao dịch"], "cdt1": p["Chủ dự toán (CDT1)"],
               "svc_start": p_i["Bắt đầu dịch vụ"] if p_i else "", "svc_end": p_i["Kết thúc dịch vụ"] if p_i else "",
               "id_payee": p["Mã đối tác"], "invoice": p_i["Hoá đơn"] if p_i else ""}
        k = canon_ref(x["Reference number"])
        if k:
            nguon[k].append({"nguon": "PM", "id": x["ID PMLine"], "tien": x["Số tiền"], "cur": x["Tiền tệ"], "cls": cls})
    for x in b.h1000:
        cls = {"hd": x["Budget Code (HDCode)"], "pay_type": "Lương (Payroll)", "cdt1": x["Chủ dự toán (CDT1)"],
               "svc_start": x["Kỳ lương"], "svc_end": x["Kỳ lương"], "id_payee": "", "invoice": "Bỏ qua"}
        nguon[canon_ref(x["Số CT"])].append({"nguon": "H1000", "id": x["ID dòng"], "tien": x["Số tiền"], "cur": "VND", "cls": cls})
    HD_PLT = {"GI": "GI | Gross Inflow", "OMC": "OMC | Online Marketing Cost", "SC": "SC | Server Cost",
              "PS": "PS | Platform Service"}
    for x in b.plt:
        ky = x["Ngày sử dụng"][:4] + x["Ngày sử dụng"][5:7]
        cls = {"hd": HD_PLT[x["Loại"]], "pay_type": "Thu từ nền tảng" if x["Loại"] == "GI" else "Thanh toán (Regular)",
               "cdt1": x["Chủ dự toán (CDT1)"], "svc_start": ky, "svc_end": ky, "id_payee": x["Vendor"], "invoice": ""}
        nguon[canon_ref(x["Combine Code"])].append({"nguon": "PLT", "id": x["ID dòng"], "tien": x["Số tiền"],
                                                    "cur": x["Tiền tệ"], "cls": cls})
    bank_theo_ma = defaultdict(list)
    for d in ledger:
        k = canon_ref(d["ref"])
        d["_ma"] = k
        if k:
            bank_theo_ma[k].append(d)
    ghep, hinh_ma = [], {}
    for k in sorted(set(bank_theo_ma) | set(nguon)):
        bb = [{"tien": x["ps_no"] + x["ps_co"], "cur": x["cur"]} for x in bank_theo_ma.get(k, [])]
        nn = nguon.get(k, [])
        h = xep_hinh(bb, nn)
        hinh_ma[k] = h
        ghep.append({"ma": k, "nguon": nn[0]["nguon"] if nn else "", "so_bank": len(bb), "so_nguon": len(nn), "hinh": h})
    # ---------- A3: ITL
    itl, cho = [], []
    lich = b.lich_su
    for d in sorted(ledger, key=lambda x: (x["ngay"], x["_s"], x["_stt"])):
        k, h = d["_ma"], hinh_ma.get(d["_ma"]) if d["_ma"] else None
        tong = d["ps_no"] + d["ps_co"]
        phia = "no" if d["ps_no"] else "co"
        if h in ("A", "B", "C"):
            nn = sorted(nguon[k], key=lambda x: x["id"])
            if h == "B":
                phan = [x["tien"] for x in nn]
                phan[-1] += tong - sum(phan)
                cac = [(f"{d['id']}.{j + 1}", nn[j], phan[j]) for j in range(len(nn))]
            else:
                cac = [(d["id"], nn[0], tong)]
            for iid, src, t in cac:
                row = {"S": dict(src["cls"]), "T": {kh: "" for kh in KHOI}, "nguon": src["nguon"], "tien": t}
                itl.append((iid, d, phia, row, None))
        else:
            t_, _v = dien_tay(d["dien_giai"], lich)
            ly_do = h if h in ("D", "E", "F") else ("khong_can_cu" if t_["hd"] == IH else None)
            row = {"S": {kh: NA for kh in KHOI}, "T": t_, "nguon": "", "tien": tong}
            itl.append((d["id"], d, phia, row, ly_do))
    out_itl = []
    for iid, d, phia, row, ly_do in itl:
        rec = {"itl_id": iid, "ngay": d["ngay"], "tk": d["tk"], "le": d["le"], "cur": d["cur"],
               "ps_no": row["tien"] if phia == "no" else D(0), "ps_co": row["tien"] if phia == "co" else D(0),
               "nguon": row["nguon"]}
        for kh in KHOI:
            s, t = row["S"][kh], row["T"][kh]
            rec[f"{kh}_T"] = t
            rec[f"{kh}_V"] = final(s, mid(kh, t, d["ngay"]))
        rec["AU"], rec["AV"], rec["AW"] = allocate(rec["cdt1_V"], rec["hd_V"], mm)
        rec["work_status"] = "UNMAPPED" if ly_do else "ok"
        if ly_do:
            cho.append({"itl_id": iid, "ly_do": ly_do})
        out_itl.append(rec)
    # ---------- CA + R1/R2/R3
    r1 = []
    for s, ten in SHEET.items():
        meta = doc_ten_sheet(ten)
        dau = SO_DU_DAU[s]
        for ngay in NGAY:
            no = sum((x["ps_no"] for x in ledger if x["_s"] == s and x["ngay"] == ngay), D(0))
            co = sum((x["ps_co"] for x in ledger if x["_s"] == s and x["ngay"] == ngay), D(0))
            cuoi = dau + no - co
            go = ccr_go[(s, ngay)]
            r1.append({"tk": meta["tk"], "ngay": ngay, "dau_ky": dau, "ps_no": no, "ps_co": co, "cuoi_ky": cuoi,
                       "ccr_go": go, "dif": cuoi - go})
            dau = cuoi
    r2 = defaultdict(lambda: defaultdict(D))
    r3 = defaultdict(lambda: defaultdict(D))
    for x in out_itl:
        v = musd(x["ps_no"], x["cur"]) - musd(x["ps_co"], x["cur"])
        r2[(x["le"], x["hd_V"])][x["ngay"]] += v
        r2[(x["le"], "TOTAL")][x["ngay"]] += v
        m = mm.get(x["hd_V"])
        if m and m["nhom"] != "NB":
            r3[m["nhom"]][x["ngay"]] += v
    for dong, thanh in DONG_PL_TONG.items():
        for ngay in NGAY:
            r3[dong][ngay] = sum((r3[t][ngay] for t in thanh), D(0))
    def bang(dd, khoa):
        out = []
        for kk in khoa:
            hang = dict(zip(("le", "hd"), kk)) if isinstance(kk, tuple) else {"dong": kk}
            for ngay in NGAY:
                hang[ngay] = lam_tron(dd[kk][ngay])
            hang["tong"] = lam_tron(sum((dd[kk][n] for n in NGAY), D(0)))
            out.append(hang)
        return out
    k2 = sorted(r2, key=lambda x: (x[0], x[1] == "TOTAL", x[1]))
    r2b = bang(r2, k2)
    r3b = bang(r3, DONG_PL_HD + list(DONG_PL_TONG))
    # ---------- A4
    loi = [{"loai": "DIF", "khoa": f"{x['tk']}|{x['ngay']}"} for x in r1 if x["dif"] != 0]
    loi += [{"loai": "TRUNG", "khoa": t} for t in trung]
    loi += [{"loai": "HD_LA", "khoa": x["itl_id"]} for x in out_itl if x["hd_V"] not in mm]
    loi += [{"loai": "GHEP_LECH", "khoa": g["ma"]} for g in ghep if g["hinh"] in ("D", "E", "F")]
    led = [{k: v for k, v in x.items() if not k.startswith("_") and k != "dien_giai"} for x in ledger]
    return {"a1": a1, "ledger": led, "ghep": ghep, "itl": out_itl, "hang_cho": cho, "r1": r1, "r2": r2b,
            "r3": r3b, "a4": {"loi": sorted(loi, key=lambda x: (x["loai"], x["khoa"]))}}


# ====================================================================== GHI
def ghi_csv(p: Path, rows: list[dict], cot=None):
    cot = cot or (list(rows[0]) if rows else [])
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cot, extrasaction="ignore")
        w.writeheader()
        for x in rows:
            w.writerow({k: ("" if x.get(k) is None else str(x.get(k))) for k in cot})


def main(seed=20261007):
    b = Bo(seed)
    b.dung()
    # tieu de tung sheet: S2 doi vi tri, S3 them cot
    tieu_de = {s: list(BAN_KHAI) for s in SHEET}
    tieu_de["S2"][2], tieu_de["S2"][3] = tieu_de["S2"][3], tieu_de["S2"][2]
    tieu_de["S3"].append("Ghi chú")
    # sap theo ngay, danh STT; nhan dong TRUNG: chep y het dong phi lien truoc cung ngay 03
    for s in SHEET:
        b.bank[s].sort(key=lambda x: x["Ngày"])
    s1 = b.bank["S1"]
    phi3 = [j for j, x in enumerate(s1) if x["Ngày"] == NGAY[2] and x["Diễn giải"].startswith("PHI DICH VU SMS")]
    s1[phi3[1]] = dict(s1[phi3[0]])                          # dong thu hai = ban sao y het dong thu nhat
    for s in SHEET:
        for j, x in enumerate(b.bank[s], 1):
            x["STT"] = j
            if s == "S3":
                x["Ghi chú"] = ""
    # CCR go tay: dung so sach, tru MOT o go nham
    ccr = {}
    for s in SHEET:
        dau = SO_DU_DAU[s]
        seen = set()
        for ngay in NGAY:
            for x in b.bank[s]:
                if x["Ngày"] != ngay or not (x["PS Nợ"] or x["PS Có"]):
                    continue
                key = tuple(x[c] for c in BAN_KHAI if c != "STT")
                if key in seen:
                    continue
                seen.add(key)
                dau += x["PS Nợ"] - x["PS Có"]
            ccr[(s, ngay)] = dau
    ccr[("S3", NGAY[3])] += D(100_000)                       # go nham 100.000 o TCB ngay 04/10
    da = tinh_dap_an(b, tieu_de, ccr)

    vao, ra = GOC / "input", GOC / "dap_an"
    vao.mkdir(exist_ok=True)
    ra.mkdir(exist_ok=True)
    ghi_csv(vao / "danh_muc_sheet.csv", [{"ma_sheet": s, "ten_sheet": t} for s, t in SHEET.items()])
    ghi_csv(vao / "ban_khai_cot.csv", [{"thu_tu": i + 1, "cot": c} for i, c in enumerate(BAN_KHAI)])
    for s in SHEET:
        ghi_csv(vao / f"bank_{s}.csv", b.bank[s], tieu_de[s])
    ghi_csv(vao / "so_du_dau.csv", [{"ma_sheet": s, "tk": doc_ten_sheet(SHEET[s])["tk"], "ngay": "2026-09-30",
                                      "so_du": v} for s, v in SO_DU_DAU.items()])
    ghi_csv(vao / "ccr_so_du_go_tay.csv", [{"tk": doc_ten_sheet(SHEET[s])["tk"], "ngay": n, "so_du_cuoi": v}
                                             for (s, n), v in ccr.items()])
    ghi_csv(vao / "pe_lines.csv", b.pe)
    ghi_csv(vao / "pi_lines.csv", b.pi)
    ghi_csv(vao / "pm_lines.csv", b.pm)
    ghi_csv(vao / "h1000.csv", b.h1000)
    ghi_csv(vao / "plt.csv", b.plt)
    ghi_csv(vao / "mapping_master.csv", [{"H_hd": h, "nhom_pl": n, "K_can_phan_bo": k, "L_phuong_phap": l}
                                          for h, n, k, l in MM])
    ghi_csv(vao / "lich_su_vendor.csv", [{"vendor": v, "hd": x["hd"], "cdt1": x["cdt1"]} for v, x in sorted(b.lich_su.items())])
    ghi_csv(vao / "ty_gia.csv", [{"thang": "2026-10", "tien_te": "VND", "ty_gia": 1},
                                  {"thang": "2026-10", "tien_te": "USD", "ty_gia": 26300}])

    (ra / "a1_kiem_nguon.json").write_text(json.dumps(da["a1"], ensure_ascii=False, indent=1), encoding="utf-8")
    ghi_csv(ra / "a2_ledger.csv", da["ledger"])
    ghi_csv(ra / "a2_ghep.csv", da["ghep"])
    ghi_csv(ra / "a3_itl_adjust.csv", da["itl"])
    ghi_csv(ra / "a3_hang_cho.csv", da["hang_cho"], ["itl_id", "ly_do"])
    ghi_csv(ra / "r1_so_du.csv", da["r1"])
    ghi_csv(ra / "r2_cf.csv", da["r2"])
    ghi_csv(ra / "r3_pl.csv", da["r3"])
    (ra / "a4_audit.json").write_text(json.dumps(da["a4"], ensure_ascii=False, indent=1), encoding="utf-8")

    hinh = defaultdict(int)
    for g in da["ghep"]:
        hinh[g["hinh"]] += 1
    print(f"seed={seed} · bank {sum(len(v) for v in b.bank.values())} dong ({len(da['ledger'])} vao ledger) · "
          f"PE {len(b.pe)} · PI {len(b.pi)} · PM {len(b.pm)} · H1000 {len(b.h1000)} · PLT {len(b.plt)}")
    print(f"ITL {len(da['itl'])} dong · hang cho {len(da['hang_cho'])} · hinh {dict(hinh)} · loi A4 {len(da['a4']['loi'])}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20261007)
