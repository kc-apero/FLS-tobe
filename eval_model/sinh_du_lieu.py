"""Sinh du lieu GIA LAP + dap an tat dinh cho 4 bai, moi bai ung mot agent cua AP.

⛔ Toan bo du lieu la BIA (vendor, ma tham chieu, so tien, TK) — khong lay mot dong
nao tu so that. Dap an tinh bang luat AS-IS da doc nguyen van (AP §4.1–§4.4), viet
LAI DOC LAP o day, ⛔ khong import `fls.*`.

    A1  Collect_raw_data      ban khai cot (drift) · ref_adjust thang · dem dong
    A2  Generate Group Ledger SI.MAP: chuan hoa ma + 6 hinh A–F + dung sai
    A3  ITL Adjust            MID/Final 7 khoi theo cong thuc sheet + de xuat HD / day nguoi
    A4  Auditor               tim loi cai san: DIF · trung · ty gia · HD la · chia PM

Chay:  python sinh_du_lieu.py [seed]   ->  du_lieu/cases.jsonl
"""
from __future__ import annotations

import json
import random
import re
import sys
import unicodedata
from decimal import Decimal
from pathlib import Path

NA = "Need to manual input"
IH = "Input here"

# ============================ SKILL (van ban dua cho model) ====================
SKILL = {
"A1": """Bạn là Agent 1 · Collect_raw_data của hệ FLS (kế toán). Nhiệm vụ: kiểm một sheet sao kê vừa chụp.
LUẬT:
1. So TIÊU ĐỀ sheet (dòng 1) với BẢN KHAI cột (danh sách tên cột theo thứ tự). So theo TÊN cột.
   - Cột có trong sheet mà không có trong bản khai -> {"loai":"them","cot":<tên>}
   - Cột có trong bản khai mà không có trong sheet -> {"loai":"bo","cot":<tên>}
   - Nếu tập tên GIỐNG HỆT nhưng thứ tự khác -> MỘT mục {"loai":"doi_vi_tri","cot":"*"}
   - Không khác gì -> danh sách rỗng.
2. Mã tham chiếu hiệu lực mỗi dòng: nếu ô "Reference number_adjust" khác rỗng thì dùng nó, ngược lại dùng "Reference number". Giữ nguyên chuỗi, không chuẩn hoá.
3. so_dong = số dòng dữ liệu có (PS Nợ > 0 hoặc PS Có > 0). Dòng cả hai bằng 0 hoặc rỗng không đếm.
Trả JSON: {"thay_doi":[...], "ref_hieu_luc":[<theo thứ tự dòng>], "so_dong":<int>}""",

"A2": """Bạn là Agent 2 · Generate Group Ledger, bước SI.MAP: ghép dòng BANK với dòng lệnh chi PM.
LUẬT (áp đúng thứ tự):
1. Chuẩn hoá mã (canon_ref): ô lỗi (bắt đầu bằng '#', ví dụ #N/A) hoặc rỗng -> KHÔNG có mã.
   Nếu mã có dạng số khoa học (vd 4.36619E+15) -> đổi thành số nguyên đầy đủ ("%.0f").
   Chuẩn hoá Unicode NFKC, viết HOA, bỏ mọi khoảng trắng và các ký tự - _ . , / \\
2. Gom theo mã đã chuẩn hoá. Chỉ xét nhóm có ÍT NHẤT 1 dòng bank VÀ 1 dòng PM; nhóm thiếu một bên -> hình "KHONG_GHEP".
3. Tiền tệ: lấy tập tiền tệ KHÁC RỖNG của cả hai bên. Có từ 2 tiền tệ trở lên -> "E". (Rỗng là KHÔNG BIẾT, không phải khác.)
4. Dung sai: nếu MỌI dòng của nhóm (cả hai bên) đều ghi tiền tệ VND -> 1000; còn lại (ngoại tệ, hoặc có dòng tiền tệ rỗng) -> 0.
   |Σ tiền bank − Σ tiền PM| > dung sai -> "F".
5. Còn lại theo số dòng: 1 bank × 1 PM -> "A"; 1 bank × N PM -> "B"; N bank × 1 PM -> "C"; N bank × M PM (N,M ≥ 2) -> "D" (KHÔNG đoán cách chia).
Trả JSON: {"nhom":[{"ma":<mã đã chuẩn hoá>,"hinh":"A|B|C|D|E|F|KHONG_GHEP"}, ...]} — đủ mọi mã có ít nhất một dòng.""",

"A3": """Bạn là Agent 3 · ITL ADJUST. Sổ ITL Ledge có 7 khối, mỗi khối 4 cột: S=Classifying, T=Manual input, U=MID, V=Final.
CÔNG THỨC NGUYÊN VĂN (khối 1, các khối khác giống hệt, chỉ đổi mặc định):
  U = ArrayFormula(if(and(T10:T="",S10:S<>"Need to manual input"),S10:S,if(T10:T="Input here",<MẶC ĐỊNH>,T10:T)))
  V = if(or(S10="Need to manual input",len(S10)=0),U10,S10)
HÀNH VI ĐÃ ĐO TRÊN SỔ THẬT: and() bên trong ArrayFormula gộp CẢ CỘT thành một giá trị (luôn FALSE trên sổ này), nên thực tế
  U = (T = "Input here") ? <MẶC ĐỊNH> : T        (T rỗng -> U rỗng)
MẶC ĐỊNH theo khối: hd="OGA | GAC - Other" · pay_type="Thanh toán (Regular)" · cdt1="SHQ2 | Headquarters2" ·
  svc_start = svc_end = yyyymm của Ngày chứng từ (vd 2026-03-07 -> "202603") · id_payee="VD0" · invoice="Nợ hoá đơn".
Ô rỗng ghi là "" (chuỗi rỗng).
VIỆC 1: tính U và V cho mọi dòng × 7 khối.
VIỆC 2: với các dòng mà khối hd có S="Need to manual input" và T rỗng (người chưa gõ), ĐỀ XUẤT giá trị gõ vào T của khối hd,
  dựa trên BẢNG LỊCH SỬ (vendor -> hd) và BẢNG TỪ KHOÁ (từ khoá trong diễn giải -> hd). Ưu tiên vendor; không có vendor thì dùng từ khoá.
  Nếu không căn cứ nào khớp, hoặc hai căn cứ mâu thuẫn nhau -> trả "ESCALATE" (đẩy người). ⛔ Không đoán.
Trả JSON: {"khoi":[{"dong":<id>,"khoi":<tên khối>,"U":<str>,"V":<str>}...], "de_xuat":[{"dong":<id>,"hd":<mã hd hoặc "ESCALATE">}...]}""",

"A4": """Bạn là Agent 4 · AUDITOR. Soát một ngày sổ trước khi xuất CCR daily. Tìm MỌI lỗi thuộc 5 loại:
- "DIF": với mỗi TK: số dư đầu + Σ PS Nợ − Σ PS Có ≠ số dư cuối gõ ở CCR (so đúng tới đơn vị). khoa = mã TK.
- "TRUNG": hai dòng trùng hệt (cùng TK, ngày, ref, PS Nợ, PS Có). khoa = id của dòng xuất hiện SAU.
- "TY_GIA": bVND của dòng ≠ tỷ giá(tiền tệ dòng) × (PS Nợ + PS Có) ÷ 10^9, lệch tương đối > 0,5%. khoa = id dòng.
- "HD_LA": hd của dòng không có trong Mapping Master. khoa = id dòng.
- "CHIA_PM": dòng có chia PM mà |Σ phần chia − (PS Nợ + PS Có)| > 1000 (VND) hoặc > 0 (ngoại tệ). khoa = id dòng.
Lưu ý: một dòng TRUNG vẫn làm lệch số dư — nếu số dư cuối CCR không tính dòng trùng thì TK đó cũng là DIF.
Không có lỗi -> danh sách rỗng. ⛔ Không báo lỗi không có thật.
Trả JSON: {"loi":[{"loai":"DIF|TRUNG|TY_GIA|HD_LA|CHIA_PM","khoa":<str>}...]}""",
}

SCHEMA = {
"A1": {"type": "object", "additionalProperties": False, "required": ["thay_doi", "ref_hieu_luc", "so_dong"],
       "properties": {"thay_doi": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                      "required": ["loai", "cot"], "properties": {"loai": {"type": "string"}, "cot": {"type": "string"}}}},
                      "ref_hieu_luc": {"type": "array", "items": {"type": "string"}}, "so_dong": {"type": "integer"}}},
"A2": {"type": "object", "additionalProperties": False, "required": ["nhom"],
       "properties": {"nhom": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                      "required": ["ma", "hinh"], "properties": {"ma": {"type": "string"}, "hinh": {"type": "string"}}}}}},
"A3": {"type": "object", "additionalProperties": False, "required": ["khoi", "de_xuat"],
       "properties": {"khoi": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                      "required": ["dong", "khoi", "U", "V"], "properties": {"dong": {"type": "string"}, "khoi": {"type": "string"},
                      "U": {"type": "string"}, "V": {"type": "string"}}}},
                      "de_xuat": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                      "required": ["dong", "hd"], "properties": {"dong": {"type": "string"}, "hd": {"type": "string"}}}}}},
"A4": {"type": "object", "additionalProperties": False, "required": ["loi"],
       "properties": {"loi": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                      "required": ["loai", "khoa"], "properties": {"loai": {"type": "string"}, "khoa": {"type": "string"}}}}}},
}

# ================================ tu dien bia ================================
HD = ["OGA | GAC - Other", "LC | License Cost", "SC | Server Cost", "OMC | Online Marketing Cost",
      "GI | Gross Inflow", "NB | Lưu chuyển nội bộ", "API | API", "PS | Platform Service", "MC | Marketing Cost",
      "CIT | Corporate Income Tax"]
VENDOR = [f"VDX{i:03d}" for i in range(1, 31)]
TU_KHOA = {"server": "SC | Server Cost", "license": "LC | License Cost", "quang cao": "OMC | Online Marketing Cost",
           "chuyen noi bo": "NB | Lưu chuyển nội bộ", "api call": "API | API", "thue tndn": "CIT | Corporate Income Tax"}
PAY = ["Thanh toán (Regular)", "Tạm ứng (Advance)", "Khẩn (Urgent)"]
CDT = ["SHQ2 | Headquarters2", "COR | Core", "CVL | Venture Lab", "CSM | Studio M", "CAH | Apps Hub"]
COT_KHAI = ["Ngày chứng từ", "Số chứng từ", "Diễn giải", "Đơn vị tiền tệ", "PS Nợ", "PS Có",
            "Reference number", "Reference number_adjust"]
KHOI = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")
MAC_DINH = {"hd": "OGA | GAC - Other", "pay_type": "Thanh toán (Regular)", "cdt1": "SHQ2 | Headquarters2",
            "id_payee": "VD0", "invoice": "Nợ hoá đơn"}


# ================================ A1 ==========================================
def a1_dap_an(khai, tieu_de, dong):
    tk, ts = list(khai), list(tieu_de)
    thay = [{"loai": "them", "cot": c} for c in ts if c not in tk] + \
           [{"loai": "bo", "cot": c} for c in tk if c not in ts]
    if not thay and tk != ts:
        thay = [{"loai": "doi_vi_tri", "cot": "*"}]
    ref = [d.get("Reference number_adjust") or d.get("Reference number") or "" for d in dong]
    n = sum(1 for d in dong if (d.get("PS Nợ") or 0) > 0 or (d.get("PS Có") or 0) > 0)
    return {"thay_doi": thay, "ref_hieu_luc": ref, "so_dong": n}


def a1_ca(r, i):
    tieu = list(COT_KHAI)
    kieu = ["khong", "them", "bo", "doi_vi_tri", "them_bo"][i % 5]
    if kieu in ("them", "them_bo"):
        tieu.insert(r.randrange(len(tieu)), r.choice(["Ghi chú", "Mã chi nhánh", "PS Nợ (USD)"]))
    if kieu in ("bo", "them_bo"):
        tieu.remove(r.choice(["Diễn giải", "Số chứng từ", "Reference number_adjust"]))
    if kieu == "doi_vi_tri":
        a, b = r.sample(range(len(tieu)), 2)
        tieu[a], tieu[b] = tieu[b], tieu[a]
    dong = []
    for k in range(r.randint(6, 10)):
        no = r.choice([0, 0, r.randint(1, 900) * 10_000])
        co = 0 if no else r.choice([0, r.randint(1, 900) * 10_000])
        d = {"Ngày chứng từ": f"2026-10-{r.randint(1, 28):02d}", "Số chứng từ": f"CT{r.randint(1000, 9999)}",
             "Đơn vị tiền tệ": "VND", "PS Nợ": no, "PS Có": co,
             "Reference number": r.choice([f"FT26{r.randint(10**9, 10**10 - 1)}", ""]),
             "Reference number_adjust": r.choice(["", "", f"ADJ-{r.randint(100, 999)}"])}
        d = {c: d.get(c, "") for c in tieu}
        dong.append(d)
    inp = {"ban_khai": COT_KHAI, "tieu_de_sheet": tieu, "dong": dong}
    # dap an dung dong ⛔ co cot bi bo thi gia tri coi nhu rong
    return inp, a1_dap_an(COT_KHAI, tieu, dong)


# ================================ A2 ==========================================
_BO = re.compile(r"[\s\-_.,/\\]+")
_KH = re.compile(r"^\d(?:\.\d+)?E\+\d+$", re.I)


def canon_ref(x):
    if x is None:
        return None
    x = str(x).strip()
    if not x or x.startswith("#"):
        return None
    if _KH.match(x):
        x = "%.0f" % float(x)
    x = unicodedata.normalize("NFKC", x).upper()
    return _BO.sub("", x) or None


def a2_dap_an(bank, pm):
    g: dict[str, dict] = {}
    for side, rows in (("b", bank), ("p", pm)):
        for d in rows:
            k = canon_ref(d["ref"])
            if k:
                g.setdefault(k, {"b": [], "p": []})[side].append(d)
    out = []
    for k, v in sorted(g.items()):
        b, p = v["b"], v["p"]
        if not b or not p:
            h = "KHONG_GHEP"
        else:
            cur = {d["cur"] for d in b + p if d["cur"]}
            if len(cur) >= 2:
                h = "E"
            else:
                ds = Decimal(1000) if all(d["cur"] == "VND" for d in b + p) else Decimal(0)
                lech = abs(sum(Decimal(str(d["tien"])) for d in b) - sum(Decimal(str(d["tien"])) for d in p))
                if lech > ds:
                    h = "F"
                elif len(b) == 1 and len(p) == 1:
                    h = "A"
                elif len(b) == 1:
                    h = "B"
                elif len(p) == 1:
                    h = "C"
                else:
                    h = "D"
        out.append({"ma": k, "hinh": h})
    return {"nhom": out}


def _bien_dang(r, ma):
    """Viet cung mot ma theo dang khac — bay chuan hoa."""
    return r.choice([ma, ma.lower(), ma[:4] + " " + ma[4:], ma[:4] + "-" + ma[4:], " " + ma + " ", ma[:6] + "." + ma[6:]])


def a2_ca(r, i):
    bank, pm = [], []
    hinh_muc_tieu = r.sample(["A", "A", "B", "C", "D", "E", "F", "F_le", "KG", "NUM", "ERR", "EMPTYCUR"], 8)
    for j, h in enumerate(hinh_muc_tieu):
        ma = f"FT26{r.randint(10**9, 10**10 - 1)}"
        cur = r.choice(["VND", "VND", "USD"])
        tien = r.randint(1, 5000) * 1000 if cur == "VND" else round(r.uniform(10, 5000), 2)
        if h == "A":
            bank.append(dict(ref=ma, tien=tien, cur=cur)); pm.append(dict(ref=_bien_dang(r, ma), tien=tien, cur=cur))
        elif h == "B":
            a = round(tien * 0.4, 2) if cur != "VND" else tien * 2 // 5
            bank.append(dict(ref=ma, tien=tien, cur=cur))
            pm += [dict(ref=_bien_dang(r, ma), tien=a, cur=cur), dict(ref=ma, tien=round(tien - a, 2), cur=cur)]
        elif h == "C":
            a = round(tien * 0.5, 2) if cur != "VND" else tien // 2
            bank += [dict(ref=ma, tien=a, cur=cur), dict(ref=_bien_dang(r, ma), tien=round(tien - a, 2), cur=cur)]
            pm.append(dict(ref=ma, tien=tien, cur=cur))
        elif h == "D":
            bank += [dict(ref=ma, tien=tien, cur=cur), dict(ref=ma, tien=tien, cur=cur)]
            pm += [dict(ref=ma, tien=tien, cur=cur), dict(ref=_bien_dang(r, ma), tien=tien, cur=cur)]
        elif h == "E":
            bank.append(dict(ref=ma, tien=tien, cur="USD")); pm.append(dict(ref=ma, tien=tien, cur="VND"))
        elif h == "F":   # lech lon
            bank.append(dict(ref=ma, tien=tien, cur=cur)); pm.append(dict(ref=ma, tien=round(tien * 1.3, 2), cur=cur))
        elif h == "F_le":  # USD lech 0,50 -> F (ngoai te dung sai 0); VND lech 800 -> A
            c2 = r.choice(["USD", "VND"])
            t = 1_000_000 if c2 == "VND" else 100.0
            bank.append(dict(ref=ma, tien=t, cur=c2)); pm.append(dict(ref=ma, tien=t + (800 if c2 == "VND" else 0.5), cur=c2))
        elif h == "KG":
            bank.append(dict(ref=ma, tien=tien, cur=cur))
        elif h == "NUM":   # ma dai bi Sheets doc thanh so khoa hoc o mot ben
            so = r.randint(10**15, 10**16 - 1)
            so = int(float("%.5E" % so))
            bank.append(dict(ref=str(so), tien=tien, cur=cur)); pm.append(dict(ref="%.5E" % so, tien=tien, cur=cur))
        elif h == "ERR":   # o loi khong bao gio la khoa
            bank.append(dict(ref="#N/A", tien=tien, cur=cur)); pm.append(dict(ref="#N/A", tien=tien, cur=cur))
        elif h == "EMPTYCUR":  # tien te rong = khong biet: ⛔ khong phai E, nhung dung sai 0 -> lech 500 la F
            bank.append(dict(ref=ma, tien=1_000_000, cur="")); pm.append(dict(ref=ma, tien=1_000_500, cur="VND"))
    r.shuffle(bank); r.shuffle(pm)
    for k, d in enumerate(bank):
        d["id"] = f"B{k + 1}"
    for k, d in enumerate(pm):
        d["id"] = f"P{k + 1}"
    return {"bank": bank, "pm": pm}, a2_dap_an(bank, pm)


# ================================ A3 ==========================================
def a3_u(khoi, s, t, ngay):
    if t == IH:
        return ngay[:4] + ngay[5:7] if khoi in ("svc_start", "svc_end") else MAC_DINH[khoi]
    return t


def a3_v(s, u):
    return u if (s == NA or len(s) == 0) else s


def a3_ca(r, i):
    lich_su = {v: r.choice(HD) for v in r.sample(VENDOR, 15)}
    tu_khoa = dict(TU_KHOA)
    dong = []
    for k in range(10):
        ngay = f"2026-{r.randint(1, 10):02d}-{r.randint(1, 28):02d}"
        blk = {}
        for kh in KHOI:
            s = r.choice([NA, NA, "", "VAL"])
            t = r.choice(["", "", IH, "VAL"])
            pool = {"hd": HD, "pay_type": PAY, "cdt1": CDT, "svc_start": ["202601", "202605", "202609"],
                    "svc_end": ["202603", "202608", "202612"], "id_payee": VENDOR, "invoice": ["Có hoá đơn", "Bỏ qua"]}[kh]
            s = r.choice(pool) if s == "VAL" else s
            t = r.choice(pool) if t == "VAL" else t
            blk[kh] = {"S": s, "T": t}
        # bay: dong hd can de xuat
        loai = r.choice(["vendor", "tu_khoa", "mau_thuan", "khong_co", None, None])
        vendor = r.choice(list(lich_su)) if loai in ("vendor", "mau_thuan") else r.choice([v for v in VENDOR if v not in lich_su])
        kw = r.choice(list(tu_khoa)) if loai in ("tu_khoa", "mau_thuan") else None
        if loai == "mau_thuan":
            while tu_khoa[kw] == lich_su[vendor]:
                kw = r.choice(list(tu_khoa))
        if loai:
            blk["hd"] = {"S": NA, "T": ""}
        dien_giai = f"TT {kw} thang {ngay[5:7]}" if kw else f"Thanh toan hop dong so {r.randint(100, 999)}"
        dong.append({"dong": f"R{k + 1}", "ngay": ngay, "vendor": vendor, "dien_giai": dien_giai, "khoi": blk})
    kq_k, kq_d = [], []
    for d in dong:
        for kh in KHOI:
            s, t = d["khoi"][kh]["S"], d["khoi"][kh]["T"]
            u = a3_u(kh, s, t, d["ngay"])
            kq_k.append({"dong": d["dong"], "khoi": kh, "U": u, "V": a3_v(s, u)})
        if d["khoi"]["hd"]["S"] == NA and d["khoi"]["hd"]["T"] == "":
            hv = lich_su.get(d["vendor"])
            kw = next((w for w in tu_khoa if w in d["dien_giai"]), None)
            hk = tu_khoa.get(kw) if kw else None
            if hv and hk and hv != hk:
                hd = "ESCALATE"
            else:
                hd = hv or hk or "ESCALATE"
            kq_d.append({"dong": d["dong"], "hd": hd})
    inp = {"lich_su_vendor_hd": lich_su, "tu_khoa_hd": tu_khoa, "dong": dong}
    return inp, {"khoi": kq_k, "de_xuat": kq_d}


# ================================ A4 ==========================================
TY_GIA = {"VND": 1, "USD": 26_300, "HKD": 3_380}


def a4_ca(r, i):
    mm = r.sample(HD, 8)
    tks = [("112-ACB-VND", "VND"), ("112-VCB-USD", "USD"), ("111-QUY-VND", "VND")]
    dong, loi = [], []
    for tk, cur in tks:
        for _ in range(r.randint(3, 5)):
            amt = r.randint(1, 900) * 100_000 if cur == "VND" else round(r.uniform(50, 9000), 2)
            no, co = (amt, 0) if r.random() < 0.5 else (0, amt)
            d = {"id": "", "tk": tk, "ngay": "2026-11-16", "ref": f"FT26{r.randint(10**9, 10**10 - 1)}", "cur": cur,
                 "ps_no": no, "ps_co": co, "hd": r.choice(mm),
                 "bvnd": round(TY_GIA[cur] * (no + co) / 1e9, 6)}
            if r.random() < 0.3:
                a = round((no + co) * 0.6, 2) if cur != "VND" else (no + co) * 3 // 5
                d["chia_pm"] = [a, round(no + co - a, 2)]
            dong.append(d)
    loai_cai = r.sample(["TRUNG", "TY_GIA", "HD_LA", "CHIA_PM", "DIF"], r.choice([0, 1, 2, 3]))
    if "TRUNG" in loai_cai:
        goc = r.choice(dong)
        dong.insert(dong.index(goc) + r.randint(1, 3), dict(goc))
    for k, d in enumerate(dong):
        d["id"] = f"L{k + 1}"
    seen = {}
    for d in dong:
        key = (d["tk"], d["ngay"], d["ref"], d["ps_no"], d["ps_co"])
        if key in seen:
            loi.append({"loai": "TRUNG", "khoa": d["id"]})
        seen.setdefault(key, d["id"])
    sach = [d for d in dong if not any(x["khoa"] == d["id"] and x["loai"] == "TRUNG" for x in loi)]
    if "TY_GIA" in loai_cai:
        d = r.choice(sach); d["bvnd"] = round(d["bvnd"] * r.choice([1.02, 0.97, 1.1]), 6)
        loi.append({"loai": "TY_GIA", "khoa": d["id"]})
    if "HD_LA" in loai_cai:
        d = r.choice(sach); d["hd"] = r.choice([h for h in HD if h not in mm])
        loi.append({"loai": "HD_LA", "khoa": d["id"]})
    if "CHIA_PM" in loai_cai:
        d = r.choice(sach)
        tot = d["ps_no"] + d["ps_co"]
        d["chia_pm"] = [round(tot * 0.5, 2), round(tot * 0.5, 2) + (5_000 if d["cur"] == "VND" else 1.0)]
        loi.append({"loai": "CHIA_PM", "khoa": d["id"]})
    dau, cuoi = {}, {}
    for tk, cur in tks:
        dau[tk] = r.randint(100, 9000) * 1_000_000 if cur == "VND" else round(r.uniform(10_000, 90_000), 2)
        # CCR cuoi ngay: ke toan go theo SO SACH (khong tinh dong trung)
        cuoi[tk] = round(dau[tk] + sum(d["ps_no"] - d["ps_co"] for d in sach if d["tk"] == tk), 2)
    if "DIF" in loai_cai:
        tk = r.choice(tks)[0]
        cuoi[tk] = round(cuoi[tk] + r.choice([1, -50_000, 1_000_000]), 2)
    # DIF that = moi TK ma cong thuc tren TOAN BO dong (ke ca trung) != CCR
    for tk, _ in tks:
        tinh = round(dau[tk] + sum(d["ps_no"] - d["ps_co"] for d in dong if d["tk"] == tk), 2)
        if abs(tinh - cuoi[tk]) > 1e-9 and not any(x["loai"] == "DIF" and x["khoa"] == tk for x in loi):
            loi.append({"loai": "DIF", "khoa": tk})
    for d in dong:
        if "chia_pm" not in d:
            continue
        tot = d["ps_no"] + d["ps_co"]
        ds = 1000 if d["cur"] == "VND" else 0
        if abs(round(sum(d["chia_pm"]), 2) - tot) > ds and not any(x["khoa"] == d["id"] and x["loai"] == "CHIA_PM" for x in loi):
            loi.append({"loai": "CHIA_PM", "khoa": d["id"]})
    inp = {"mapping_master_hd": mm, "ty_gia": TY_GIA, "so_du_dau": dau, "so_du_cuoi_ccr": cuoi, "dong": dong}
    return inp, {"loi": sorted(loi, key=lambda x: (x["loai"], x["khoa"]))}


SINH = {"A1": a1_ca, "A2": a2_ca, "A3": a3_ca, "A4": a4_ca}
SO_CA = {"A1": 15, "A2": 15, "A3": 12, "A4": 15}


def main(seed: int = 20261117) -> None:
    r = random.Random(seed)
    out = Path(__file__).with_name("du_lieu")
    out.mkdir(exist_ok=True)
    with open(out / "cases.jsonl", "w", encoding="utf-8") as f:
        for bai, sinh in SINH.items():
            for i in range(SO_CA[bai]):
                inp, ans = sinh(r, i)
                f.write(json.dumps({"id": f"{bai}-{i + 1:02d}", "bai": bai, "dau_vao": inp, "dap_an": ans},
                                   ensure_ascii=False) + "\n")
    with open(out / "skill.json", "w", encoding="utf-8") as f:
        json.dump({"skill": SKILL, "schema": SCHEMA, "seed": seed}, f, ensure_ascii=False, indent=1)
    print(f"seed={seed} -> {out/'cases.jsonl'}: " + " · ".join(f"{b} {n} ca" for b, n in SO_CA.items()))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20261117)
