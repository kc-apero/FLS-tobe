# -*- coding: utf-8 -*-
"""Sinh AP Voi FLS v3.0.0 — thêm voi LÕI CONFIG CHUNG (hệ báo cáo + hệ phân bổ) và đổi số cây (level-1).

⭐ Owner 16/11 (KhanhCQ): "xem toàn bộ file sheet trong này (Drive folder 1UTC-PZ_…), đây là toàn bộ logic vận
   hành hiện tại của bản as-is. Trước khi có agents cần có code config cho những phần giống nhau giữa 2 bản (hệ
   thống báo cáo, hệ thống phân bổ). Dựng phần này thành 1 con voi trước và đưa vào AP. Cập nhật phiên bản tiếp
   theo" — kèm skill apr-vevoi + apr-build-ap-reformat.

⭐ Cách làm (skill apr-build-ap-reformat):
   · v2.5.0 ĐÓNG BĂNG. Mọi mục cũ lấy NGUYÊN VĂN từ `sinh_ap_voi_v2.py` (import, ⛔ chép), rồi đổi số MỘT lượt theo
     `DOI_SO` (alternation dài-trước), heading id giữ nguyên ⇒ link cũ vẫn tới.
   · Thêm Part 3 mới (id `c3-…`). Thêm 6 Part sẽ vượt ≤5 ⇒ gộp lại: phủ PD Now về §1.5, Part 3 cũ → Part 4,
     Part 4 cũ → Part 5, đề xuất CA·SO·AL·RP vào Part 3 mới, HR·PLT → §4.5, câu chờ owner → §5.5.
   · Nguồn của Part 3: Drive folder owner gửi (24 tệp), chủ yếu tab `PD Now – Logic & Conflict` của tệp
     "[FS2] PD Now – Logic & Rules script (Claude 1311)" — cột DJ (logic chi tiết, đọc script + formula thật 13/11)
     và DK (conflict) cho bước 400–419 · 500–513 · 600–617; cộng đọc trực tiếp ATL (cây HD, luật phân bổ, dòng PL),
     Mapping Master (ITL 1/2 RAW, tiêu đề), 9.2 Exchange Rate (APERO | FS2). ⛔ ghi gì vào Drive.

Chạy:  python docs/ITL/_tools/sinh_ap_voi_v3.py   (rồi ap-status-check --restamp · các cổng — xem CONG ở cuối)
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

DAY = Path(__file__).resolve().parent
sys.path.insert(0, str(DAY))
import sinh_ap_voi_v2 as A2  # noqa: E402

GOC = A2.GOC
RA = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.0.0_Loi-Config-Chung_2026-11-16.html"
CU = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v2.5.0_Doi-Chieu-NOW-TOBE_2026-11-13.html"
NGAY = "2026-11-16"
E = html.escape
SEP = A2.SEP
so = A2.so

# ═════════════════ BẢN ĐỒ ĐỔI SỐ v2.5.0 → v3.0.0 (dữ liệu, ⛔ suy) ═════════════════
DOI_SO = {  # số cũ → số mới (heading và mọi tham chiếu §…)
    "3.1": "4.1", "3.2": "4.2", "3.3": "4.3", "3.3.1": "4.3.1", "3.3.2": "4.3.2", "3.4": "4.4.1", "3.5": "4.4.2",
    "4.1": "5.1", "4.2": "5.2", "4.3": "5.3", "4.4": "5.4",
    "5.1": "4.5", "5.2": "3.5.1", "5.3": "3.5.2", "5.4": "1.5", "5.4.1": "1.5.3", "5.4.2": "1.5.4", "5.5": "5.5",
}
DOI_HINH = {"4.4": "5.4"}           # Figure cũ → mới
DOI_PART = {"3": "Part 4", "4": "Part 5", "5": "Part 3 · §4.5"}   # "Part N" trong thân mục
GIU_NGUYEN = {"s1-5-2"}             # biên bản v2.4 → v2.5.0: giữ số của phiên bản nó tả (§A.21)
SUA_CHU = {"s1-5-1": [("Part 1 · 3 · 5", "Part 1 · 3 · 4 · 5")]}       # đổi số Part không đều — ghi ra, ⛔ ẩn
BO_DON_VI = {"s5-4"}                # §5.4 cũ (chỉ có heading) gộp vào §1.5 — nội dung của nó là 5.4.1 · 5.4.2


def doi(body: str, uid: str) -> str:
    if uid in GIU_NGUYEN:
        return body
    for a, b in SUA_CHU.get(uid, []):
        assert body.count(a) == 1, (uid, a)
        body = body.replace(a, b)
    khoa = sorted(DOI_SO, key=len, reverse=True)
    rx = re.compile(r"§(" + "|".join(re.escape(k) for k in khoa) + r")(?!\d|\.\d)")
    body = rx.sub(lambda m: "§" + DOI_SO[m.group(1)], body)
    body = re.sub(r"Figure (\d+(?:\.\d+)*)", lambda m: "Figure " + DOI_HINH.get(m.group(1), m.group(1)), body)
    body = re.sub(r"Part ([345])(?!\d)", lambda m: DOI_PART[m.group(1)], body)
    return body


# ═════════════════ TÁCH v2.5.0 THÀNH TỪNG MỤC (từ bộ sinh, ⛔ từ HTML đã đóng dấu) ═════════════════
TOKEN = re.compile(r'(<h2 class="part-divider">.*?</h2>)|' + re.escape(SEP) + r'\n(<h2 class="part"[^>]*>.*?</h2>)\n' + re.escape(SEP)
                   + r'|(<h3[^>]*>.*?</h3>)', re.S)


def muc_cu() -> dict:
    A2._cha.clear()
    A2._st.clear()
    than = "\n".join([A2.p1(), A2.p2(), A2.p3(), A2.p4(), A2.p5()])
    out, cuoi, hien = {}, 0, None
    for m in TOKEN.finditer(than):
        if hien:
            hien["than"] = than[cuoi:m.start()]
        cuoi = m.end()
        if m.group(1):
            hien = None
            continue
        tag = m.group(2) or m.group(3)
        uid = re.search(r'id="([^"]+)"', tag).group(1)
        hien = {"tag": tag, "lvl": 2 if m.group(2) else 3, "than": ""}
        out[uid] = hien
    if hien:
        hien["than"] = than[cuoi:]
    return out


def dau(lvl: int, uid: str, text: str, attrs_cu: str | None = None, st: str = "draft", inh: str | None = None) -> str:
    """Heading. attrs_cu = data-st… của mục cũ (giữ trạng thái + ngày, §A.14 're-stamp, never re-decide')."""
    if attrs_cu is not None:
        a = attrs_cu
    else:
        a = f' data-st="{st}" data-st-on="{NGAY}"' + (f' data-st-inherited="{inh}"' if inh else "")
    cls = ' class="part"' if lvl == 2 else ""
    tag = f'<h{lvl}{cls} id="{uid}"{a}>{text}</h{lvl}>'
    return (SEP + "\n" + tag + "\n" + SEP) if lvl == 2 else tag


def dung_lai(m: dict, uid: str, so_moi: str, lvl: int, ten_moi: str | None = None, inh_moi: str | None = None) -> str:
    m = m[uid]
    tag = m["tag"]
    inner = re.search(r">(.*)</h[23]>$", tag, re.S).group(1)
    inner = re.sub(r"^§[\d.]+", "§" + so_moi, inner)
    if ten_moi:
        inner = re.sub(r"^(§[\d.]+ [A-Z.]+: )[^<]*", lambda x: x.group(1) + ten_moi, inner)
    attrs = re.search(r'id="[^"]+"([^>]*)>', tag).group(1)
    if inh_moi is not None:
        attrs = re.sub(r' data-st-inherited="[^"]*"', "", attrs)
        if inh_moi:
            attrs += f' data-st-inherited="{inh_moi}"'
    return dau(lvl, uid, inner, attrs) + doi(m["than"], uid)


# ═════════════════ PART 3 MỚI · LÕI CONFIG CHUNG ═════════════════
# Mỗi số dưới đây đọc từ Drive 16/11 hoặc từ cột DJ/DK do phiên 13/11 ghi (đọc script + formula thật). Đ4: nhãn tại chỗ.
HD_CAY = [  # (nhóm, cấp, mã · tên) — đọc nguyên ATL 'Report I PLA3 Y H Q M | PM + HR | ATL'!B8:E88, 16/11
    ("HDO", 1, "GI | Gross Inflow"), ("HDO", 1, "OPC | Operating Cost"), ("HDO", 2, "CAC | Customer Acquisition Cost"),
    ("HDO", 3, "MAC | Marketing Cost"), ("HDO", 4, "OMC | Online Marketing Cost"), ("HDO", 4, "MC | Maketer Cost"),
    ("HDO", 4, "OTMC | Other Marketing Cost"), ("HDO", 3, "COT | CAC - Other"), ("HDO", 2, "COS | Cost of Servies"),
    ("HDO", 3, "PS | Profit Share"), ("HDO", 3, "API | API"), ("HDO", 3, "SC | Server Cost"), ("HDO", 3, "LC | License Cost"),
    ("HDO", 3, "DC | Dev Cost (Maintain App)"), ("HDO", 3, "CSO | Service Cost - Other"), ("HDO", 1, "GAC | General Admin Cost"),
    ("HDO", 2, "OFR | Office Rental Cost"), ("HDO", 2, "GAH | GA HR Cost"), ("HDO", 2, "BRC | Branding Cost"),
    ("HDO", 2, "HCC | HR Culture Activities Cost"), ("HDO", 2, "REC | Recruitment Cost"), ("HDO", 2, "BON | Bonus"),
    ("HDO", 2, "BUT | Travel Cost"), ("HDO", 2, "OPO | Operating - Other"), ("HDO", 2, "CXA | Product Cost In-House Development App"),
    ("HDO", 2, "OGA | GAC - Other"), ("HDO", 1, "CDC | Capex and Depreciation"), ("HDO", 2, "CXP | Partnership Development"),
    ("HDO", 2, "CXI | Infrastructure"), ("HDO", 3, "OSF | Office Setup Fee"), ("HDO", 3, "FNS | Facilities for New Staff"),
    ("HDO", 3, "CIO | Infrastructure - Other"), ("HDO", 2, "CXB | Biz Development"), ("HDO", 2, "CXO | CPX - Other"),
    ("HDO", 1, "ITE | Interest"), ("HDO", 1, "CFI | Issuance of Stock"), ("HDO", 1, "LMN | Loan/Borrowing"), ("HDO", 1, "OMN | Repayment of Loan"),
    ("HDH", 1, "NIS | Net Income Staff"), ("HDH", 1, "INT | Insurance Total"), ("HDH", 1, "PIT | PIT Total"), ("HDH", 1, "COM | COM Total"),
    ("HDAP", 1, "DEP | Deposit"), ("HDT", 1, "NB | Lưu chuyển nội bộ"),
    ("HDC", 1, "TAC | Tax Cash"), ("HDC", 1, "CIT | Corporate Incomes Tax"), ("HDC", 1, "AR | Adjustment Revenue"),
    ("HDC", 1, "CP1.1 (PL2) | Contribution Profit 11"), ("HDC", 1, "CP1.2 | Contribution Profit 12"), ("HDC", 1, "CP2 | Contribution Profit 2"),
    ("HDC", 1, "CP3 | Contribution Profit 3"), ("HDC", 1, "EBITDA | EBITDA"), ("HDC", 1, "EBIT | EBIT"), ("HDC", 1, "EBT | EBT"),
    ("HDC", 1, "NP | NP"), ("HDC", 1, "NPC | Net Profit Cumulative"), ("HDC", 1, "NCF | Net Cashflow (Burn Rate)"),
    ("HDC", 1, "NCFO | Net Cashflow from Operating"), ("HDC", 2, "CRO | Cash Received from Operating"), ("HDC", 2, "COO | Cash Outflow from Operating"),
    ("HDC", 1, "NCFI | Net Cashflow from Investing"), ("HDC", 2, "CRI | Cash Received from Investing"), ("HDC", 2, "COI | Cash Outflow from Investing"),
    ("HDC", 1, "NCFF | Net Cashflow from Financing"), ("HDC", 2, "CRF | Cash Received from Financing"), ("HDC", 2, "COF | Cash Outflow from Financing"),
    ("HDC", 2, "CFO | NCFF - Other"),
    ("HDCI", 1, "PL2 | = GI - OMC"), ("HDCI", 1, "PL3 | = PL2 - Tech Service Cost (none HR: server, API.. + Tools)"),
    ("HDCI", 1, "PL4 | = PL3 - Profit share (Partners)"), ("HDCI", 1, "PL5 | = PL4 - COM"),
    ("HDCI", 1, "PL6 | = PL5 - Other Venture cost (Marketer + product dev + Tech dev)"), ("HDCI", 1, "PL7 | = PL6 - HQ Cost"),
    ("HDCI", 1, "PL8 | = PL7 - Tax (CIT)"),
]
NHOM_HD = {"HDO": "HD Original", "HDH": "HD HR", "HDAP": "HD Account Payable", "HDT": "HD Tempo", "HDC": "HD Calculated", "HDCI": "HD Calculated Internal"}
assert len(HD_CAY) == 74, len(HD_CAY)
LUAT_PB = [  # ATL!B2:C4, đọc 16/11
    ("theo PM Amount của CFA2 | MID 3 (từng sổ nền tảng)", ["GI", "OMC", "SC", "PS"]),
    ("Allocate by GI", ["LC", "BRC", "CXP", "OSF", "FNS", "CIO", "CXB", "CXO"]),
    ("Allocate by NOEM, trừ OFR của CAH (HCM có văn phòng riêng)", ["OFR", "HCC", "REC", "BON", "OGA"]),
]


def voi_config() -> str:
    """Figure 3.1 — 5 dải × 5 cột chặng; mọi mũi tên thẳng, giữa hai dải kề nhau hoặc trong một dải (§A.32)."""
    BW, GX, CG = 160, 12, 46            # bề rộng hộp · khe trong cột · khe giữa cột
    so_hop = [2, 2, 3, 1, 1]            # số hộp config (dải 3 + 4) mỗi cột — quyết định bề rộng cột
    cw = [max(1, n) * BW + (max(1, n) - 1) * GX for n in so_hop]
    cw = [max(w, 210) for w in cw]
    LX = 172
    cx0 = [LX + sum(cw[:i]) + CG * i for i in range(5)]
    W = cx0[-1] + cw[-1] + 20
    D = {"now": (56, 84), "eng": (176, 136), "chieu": (348, 84), "luat": (468, 84), "nguon": (588, 92)}   # (y, cao)
    H = 700
    cot = [("① QUY ĐỔI · CA", "PD 400–406"), ("② KHỐI TRƯỚC PB · SO", "PD 407–419"), ("③ PHÂN BỔ · AL", "PD 500–513"),
           ("④ KHỐI SAU PB · SO-ATL", "PD 600–606"), ("⑤ BÁO CÁO · RP", "PD 607–617")]
    dai = [("now", "NOW · sheet AS-IS", "đáp án đối chiếu", "#f3f4f6"), ("eng", "TO-BE · ENGINE", "mã tất định, ⛔ agent", "#fef3e8"),
           ("chieu", "TO-BE · CONFIG", "chiều dùng chung", "#eef2ff"), ("luat", "TO-BE · CONFIG", "luật", "#eef2ff"),
           ("nguon", "NOW · config đang nằm", "nhập tay · gõ cứng", "#f3f4f6")]
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Figure 3.1 voi lõi config chung báo cáo và phân bổ">',
         '<defs><marker id="m31" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0 0L10 5L0 10z" fill="#374151"/></marker></defs>']
    for i, (t, p) in enumerate(cot):
        x = cx0[i]
        o.append(f'<line x1="{x}" y1="34" x2="{x + cw[i]}" y2="34" stroke="#d1d5db" stroke-width="1.5"/>'
                 f'<text x="{x + cw[i] / 2}" y="22" font-size="12" font-weight="700" fill="#b14a23" text-anchor="middle">{E(t)}</text>'
                 f'<text x="{x + cw[i] / 2}" y="48" font-size="10.5" fill="#6b7280" text-anchor="middle">{E(p)}</text>')
    for k, t1, t2, nen in dai:
        y, hh = D[k]
        o.append(f'<rect x="8" y="{y}" width="{LX - 20}" height="{hh}" rx="6" fill="{nen}" stroke="#d1d5db"/>'
                 f'<text x="16" y="{y + hh / 2 - 4}" font-size="11.5" font-weight="700" fill="#1f2937">{E(t1)}</text>'
                 f'<text x="16" y="{y + hh / 2 + 12}" font-size="10.5" fill="#4b5563">{E(t2)}</text>')

    def hop(x, y, w, h, ma, dong, vien="#9ca3af", nen="#fff", net=""):
        s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{nen}" stroke="{vien}" stroke-width="1.5"{net}/>',
             f'<text x="{x + 8}" y="{y + 16}" font-size="11" font-weight="700" fill="#111827">{E(ma)}</text>']
        s += [f'<text x="{x + 8}" y="{y + 31 + 13 * i}" font-size="10" fill="#374151">{E(d)}</text>' for i, d in enumerate(dong)]
        return "".join(s)

    def mui(x1, y1, x2, y2, net=False, mau="#374151"):
        d = ' stroke-dasharray="5 4"' if net else ""
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{mau}" stroke-width="1.5"{d} marker-end="url(#m31)"/>'

    now = [("406 · General Ledger", ["CALC ZONE: Nợ/Có × 5 tiền tệ", "tồn luỹ kế · bVND · mUSD"]),
           ("409–419 · CFA · PLA", ["CFA1 · CFA3 · PLA1 · PLA3", "Daily + Y/H/Q/M (mUSD)"]),
           ("501–513 · nền tảng · khoá", ["CFA1 → MID1 → MID2 → MID3 ×4", "Allocation Table NOEM · GI · LE"]),
           ("606 · ATL", ["PLA3 PM + HR | ATL", "chưa có công thức phân bổ"]),
           ("607–616 · Daily · CCR", ["Daily Report 2 · 3", "A-CCR PDF · CCR ký tháng"])]
    y, hh = D["now"]
    for i, (ma, dong) in enumerate(now):
        o.append(hop(cx0[i] + 6, y + 6, cw[i] - 12, hh - 12, ma, dong, "#9ca3af", "#fff", ' stroke-dasharray="4 3"'))
    # ENGINE — hai làn: a = CF (đi thẳng, ⛔ phân bổ), b = P&L
    y, hh = D["eng"]
    la, lb = y + 34, y + 100
    eng = {0: ("CA.GL", ["SỔ CÁI GL · QUY ĐỔI", "ITL hiệu lực → dòng GL", "5 tiền tệ → bVND · mUSD", "tồn theo (TK, ngày)"], "ab"),
           1: ("SO.CFA · SO.PLA", ["KHỐI TRƯỚC PHÂN BỔ", "CF: CFA1 · CFA3 (làn trên)", "P&L: PLA1 · PLA3 (làn dưới)", "Σ theo (HD, ngày) + Y/H/Q/M"], "ab"),
           2: ("AL.PLT · AL.KEY", ["PHÂN BỔ", "nền tảng: tỷ trọng CDT1", "HD: khoá GI · NOEM · LE"], "b"),
           3: ("SO.PLA3-ATL", ["KHỐI SAU PB", "P&L × CDT1 × kỳ", "dòng PL2–PL8 + CHECK"], "b"),
           4: ("RP.CF · RP.PL · RP.CCR", ["BÁO CÁO", "Daily Report 2 (CF) · 3 (P&L)", "CCR · PDF ký tháng"], "ab")}
    hop_eng = {}
    for i, (ma, dong, lan) in eng.items():
        x = cx0[i] + 6
        w = cw[i] - 12
        if lan == "ab":
            yy, h2 = y + 6, hh - 12
        else:
            yy, h2 = la + 26, hh - 12 - (la + 26 - (y + 6))
        o.append(hop(x, yy, w, h2, ma, dong, "#E57347", "#fff"))
        hop_eng[i] = (x, yy, w, h2)
    # mũi tên ENGINE (ngang): CF làn a — CA → SO → (làn trống cột ③ ④) → RP; P&L làn b — CA → SO → AL → ATL → RP
    def phai(i): return hop_eng[i][0] + hop_eng[i][2]
    def trai(i): return hop_eng[i][0]
    o.append(mui(phai(0), la, trai(1) - 2, la))
    o.append(mui(phai(1), la, trai(4) - 2, la))
    o.append(f'<text x="{(phai(1) + trai(4)) / 2}" y="{la - 6}" font-size="10" fill="#6b7280" text-anchor="middle">CF ⛔ phân bổ</text>')
    for a_, b_ in ((0, 1), (1, 2), (2, 3), (3, 4)):
        o.append(mui(phai(a_), lb, trai(b_) - 2, lb))
    # CONFIG — chiều (cột ① ②) và luật (cột ③ ④ ⑤); mũi tên dọc lên hộp ENGINE cùng cột
    chieu = {0: [("IX.FX", ["TỶ GIÁ THÁNG", "yyyymm × 5 tiền tệ"]), ("IX.ORG", ["TỔ CHỨC", "TK → LE · CDT1 · Cash"])],
             1: [("IX.HD", ["CÂY HD", "74 dòng · 6 nhóm · L1–L4"]), ("IX.PER", ["KỲ", "ngày · Y/H/Q/M · PL"])]}
    luat = {2: [("IX.VEN", ["VENDOR · NETWORK", "Block 1 × 7 CDT1"]), ("IX.DRV", ["DRIVER THÁNG", "NOEM · GI · LE"]),
                ("IX.ALR", ["LUẬT PHÂN BỔ", "HD → phương pháp"])],
            3: [("IX.PL", ["DÒNG PL", "PL2–PL8 + 2 CHECK"])], 4: [("IX.TMP", ["KHUÔN + BẢN KÝ", "Templ 1–5 · sign-off"])]}
    o_cfg = {}
    for k, nhom in (("chieu", chieu), ("luat", luat)):
        y, hh = D[k]
        for i, ds in nhom.items():
            n = len(ds)
            x0 = cx0[i] + (cw[i] - (n * BW + (n - 1) * GX)) / 2
            for j, (ma, dong) in enumerate(ds):
                x = x0 + j * (BW + GX)
                o.append(hop(x, y + 8, BW, hh - 16, ma, dong, "#6366f1", "#fff"))
                o_cfg[ma] = (x, y + 8, BW, hh - 16, i)
    yeng_day = {i: hop_eng[i][1] + hop_eng[i][3] for i in hop_eng}
    for ma, (x, yy, w, h2, i) in o_cfg.items():
        o.append(mui(x + w / 2, yy, x + w / 2, yeng_day[i] + 2, mau="#6366f1"))
    # NOW · nơi config đang nằm — một hộp mỗi cột, mũi tên dọc lên từng hộp config của cột (qua làn trống)
    nguon = [("9.2 Exchange Rate · Mapping Master", ["APERO | FS2 nhập tay", "R | → LE · AA:AD Cash/Bank"]),
             ("cây HD gõ cứng theo dòng", ["ngày đầu 21/10/2024", "năm ép 2025 (For PL)"]),
             ("Vendor & Network Mapping", ["ô cứng H1000 HR Report", "MID3 TOTAL · ghi chú ATL B2:C4"]),
             ("định nghĩa PL", ["Mapping Master (Nghiệm thu)", "+ công thức dòng ATL"]),
             ("Templ 1–5 · Filters", ["PD590 · PD510", "[PLA5] dán value"])]
    y, hh = D["nguon"]
    for i, (ma, dong) in enumerate(nguon):
        x, w = cx0[i] + 6, cw[i] - 12
        o.append(hop(x, y + 6, w, hh - 12, ma, dong, "#9ca3af", "#fff", ' stroke-dasharray="4 3"'))
        for cma, (cx, cy, cwid, ch, ci) in o_cfg.items():
            if ci == i:
                o.append(mui(cx + cwid / 2, y + 6, cx + cwid / 2, cy + ch + 2, net=True, mau="#6b7280"))
    o.append("</svg>")
    return "".join(o)


def bang_band(cot, nhom_hang) -> str:
    """Bảng có dải nhóm (vevoi): mỗi dải ≤ 5 dòng."""
    hang, nhan, i = [], {}, 0
    for ten, ds in nhom_hang:
        assert 2 <= len(ds) <= 5 or len(nhom_hang) == 1, (ten, len(ds))
        nhan[i] = ten
        hang += ds
        i += len(ds)
    return A2.bang(cot, hang, nhom=nhan)


def p3_moi() -> str:
    cot_logic = [("bước PD", 9), ("NOW · script · công thức (đọc 13/11)", 38), ("rủi ro · conflict đã ghi", 28), ("TO-BE · config · engine", 25)]
    tong_hd = len(HD_CAY)
    o = [A2.part(3, "IX · Lõi config chung — báo cáo và phân bổ, dựng trước agent"),
         dau(2, "c3-1", "§3.1 IX: voi lõi config chung", st="review"),
         "<p>Hệ <b>báo cáo</b> và hệ <b>phân bổ</b> là phần giống nhau giữa NOW và TO-BE: cùng luật, mã tất định, ⛔ cần agent (F0b). "
         "Nên dựng chúng <b>trước agent</b>, dưới dạng <b>engine đọc config</b>: mọi chỗ AS-IS đang gõ cứng trong công thức thành một dòng config có version, owner ký.</p>",
         A2.cap("3.1", "IX", "năm dải × năm chặng: sheet NOW (đáp án) · engine TO-BE · config chiều · config luật · nơi config NOW đang nằm.",
                ["Cùng cột = cùng chặng: engine của cột phải ra đúng từng ô của sheet NOW cùng cột (cổng KS); giữa hai dải ấy ⛔ có dữ liệu chảy, nên ⛔ vẽ mũi tên.",
                 "Engine hai làn: làn trên CF (CFA1 · CFA3) đi thẳng tới báo cáo qua làn trống của ③ ④ — CF ⛔ phân bổ; làn dưới P&L đi qua phân bổ.",
                 "Mũi tên tím = engine đọc config cùng cột; mũi tên xám đứt = chuyển config từ chỗ NOW đang nằm vào bảng config (một lần, rồi khai tiếp theo tháng).",
                 "IX.HD · IX.PER · IX.FX còn dùng lại ở các cột sau (cây HD là hàng của mọi báo cáo); mũi tên chỉ vẽ tới cột dùng đầu tiên.",
                 "Mọi hộp TO-BE là <b>PROPOSED</b> trừ phần đã nạp được: Mapping Master 73 mã hd · <code>need_cfa2</code> · <code>method_cfa2</code> (<code>fls/adapters/mapping_master.py</code>), bản khai LE theo TK."]),
         f'<div class="tw voi3">{voi_config()}</div>',
         dau(2, "c3-2", "§3.2 IX: các bảng config — chiều, luật, và chỗ AS-IS đang gõ cứng", st="review"),
         "<p>Mười bảng config, chia theo dải của Figure 3.1. Số dòng hôm nay đọc từ Drive 16/11 hoặc từ cột DJ/DK do phiên 13/11 ghi.</p>",
         dau(3, "c3-2-1", "§3.2.1 IX: chiều dùng chung", inh="c3-2"),
         A2.bang([("bảng", 13), ("khoá · cột", 27), ("hôm nay (đo)", 22), ("nguồn NOW", 22), ("FLS", 16)], [
             ["<b>IX.FX</b> tỷ giá", "tháng <code>yyyymm</code> × USD · SGD · COP · VND (=1) · HKD", "37 dòng 202401 → 202612 (kể cả dòng lạc 202306)", "<code>9.2.Exchange Rate</code> của <code>APERO | FS2</code>, nhập tay; CF report · P&amp;L report · A-CCR đều IMPORTRANGE", "0 mã"],
             ["<b>IX.ORG</b> tổ chức", "sheet <code>R |</code> → LE · TK → Cash/Bank · CDT1 · bảng <code>CDT Correct</code>", "≥ 13 pháp nhân (ma trận NB) · 8 CDT1 (SHQ2 · SHQ1 · COR · CVL · CSM · CAH · ASA · CMN) · CDT Correct 18 dòng, mặc định SHQ2", "Mapping Master A:B · AA:AD (ITL 1/2 RAW) · P&amp;L <code>BR11:BS28</code>", "◐ LE theo TK ở bản khai"],
             ["<b>IX.HD</b> cây HD", "mã · tên · cha · cấp L1–L4 · nhóm · COA1/COA2", f"{tong_hd} dòng ở cây ATL, 6 nhóm (§3.2.5) · Mapping Master 73 mã hd (đo 28/08)", "cây gõ cứng theo vị trí dòng ở từng sheet Daily; Mapping Master D:L", "◐ 73 mã hd nạp được"],
             ["<b>IX.PER</b> kỳ", "lịch ngày · Y/H/Q/M · ngày đầu · luật ghi nhận kỳ dịch vụ (PL start → PL end)", "ngày đầu 21/10/2024 gõ cứng · năm ép 2025 ở <code>For PL Report</code>", "ô G5 các sheet Daily · BM/BO sheet HR", "0 mã"]]),
         dau(3, "c3-2-2", "§3.2.2 AL: luật phân bổ", inh="c3-2"),
         A2.bang([("bảng", 13), ("khoá · cột", 27), ("hôm nay (đo)", 22), ("nguồn NOW", 22), ("FLS", 16)], [
             ["<b>IX.VEN</b> vendor · network", "No/Vendor · Vendor ID · Network · Account · % · cash-in (+tháng, ngày) · product_id → CDT1 · cách tính riêng", "Block 1 = 36 dòng (M:S hàng 4–39) × 7 CDT1 · 5 vendor tính riêng gõ cứng (VD341 · VD444 · VD428 · 'Max' · VD62)", "<code>Vendor &amp; Network Mapping</code> (sổ GI · OMC) + script <code>MappingBlock2.gs</code>", "0 mã"],
             ["<b>IX.DRV</b> driver tháng", "driver × CDT1 × tháng: NOEM (headcount) · GI theo PE · GI theo PM · NB theo LE", "chỉ có 2025; NOEM tham chiếu ô cứng của <code>H1000 I HR Report</code>", "<code>Allocation Table | By NOEM &amp; By GI</code> · <code>| NB | By LE</code>", "0 mã"],
             ["<b>IX.ALR</b> luật phân bổ", "HD → phương pháp × hiệu lực từ kỳ", "theo PM: 4 HD · by GI: 8 HD · by NOEM: 5 HD · by LE: chưa có luật (§3.2.5)", "ghi chú chữ ở ATL <code>B2:C4</code> · Mapping Master K · L", "◐ <code>need_cfa2</code> · <code>method_cfa2</code>; biết By GI (8) · By NOEM (5)"]]),
         dau(3, "c3-2-3", "§3.2.3 RP: báo cáo", inh="c3-2"),
         A2.bang([("bảng", 13), ("khoá · cột", 27), ("hôm nay (đo)", 22), ("nguồn NOW", 22), ("FLS", 16)], [
             ["<b>IX.PL</b> dòng PL", "PL2 … PL8 = công thức trên cây HD · 2 phép CHECK", "7 dòng HDCI · CHECK: NB = 0 · NIS + INT + PIT + COM = CXA + GAH + DC + MC", "công thức dòng ATL · định nghĩa ở Mapping Master (file Nghiệm thu) — hai bản lệch nhau", "0 mã"],
             ["<b>IX.TMP</b> khuôn + bản ký", "khuôn Templ 1–5 · Filters · kỳ · KRF · snapshot sign-off có version", "Templ 1–5 (PD590) · 3 filter (PD510) · bản <code>[PLA5]</code> dán value", "PD510 · PD520 · PD530 · PD590 · sheet <code>[MID][FS1][PLA5]5. Daily Report 3 (Sign off)</code>", "0 mã"]]),
         dau(3, "c3-2-4", "§3.2.4 IX: chỗ AS-IS gõ cứng → dòng config", inh="c3-2"),
         "<p>Mỗi dòng là một chỗ phiên 13/11 tìm thấy trong công thức thật (cột DK). Engine TO-BE ⛔ được gõ lại chỗ ấy: nó đọc config.</p>",
         bang_band([("chỗ gõ cứng ở NOW", 38), ("hậu quả đã thấy", 32), ("thành config / luật", 30)], [
             ("chiều dùng chung", [
                 ["cây HD theo vị trí dòng, cha = SUM con; Y/H/Q/M nối theo vị trí dòng", "chèn dòng HD ở Daily mà quên sheet kia ⇒ cộng sai im lặng", "IX.HD cha–con; engine tự cộng"],
                 ["ngày đầu cột 21/10/2024; năm ép 2025 (T11/T12 → 2024)", "dữ liệu 2026 bị gán sai năm", "IX.PER; năm lấy từ dữ liệu"],
                 ["bảng tỷ giá: 2024 một giá cả năm · 07–12/2025 cố định 25.500 · 2026 điền sẵn 26.200 · dòng lạc 202306", "tháng thiếu ⇒ SUMIFS = 0 ⇒ mất số không báo; tháng nhập hai dòng ⇒ cộng đôi", "IX.FX một dòng / tháng; thiếu = CHẶN"],
                 ["<code>CDT Correct</code> BR11:BS28, mặc định SHQ2", "CDT lạ rơi im lặng về SHQ2", "IX.ORG; CDT lạ = hàng chờ"]]),
             ("phân bổ", [
                 ["block 7 dòng CDT1 (T11:T16) · block 36 dòng MID3", "thêm CDT1 / vendor phải sửa tay mọi block", "IX.VEN × danh mục CDT1"],
                 ["VD341 · VD444 · VD428 · 'Max' · VD62 tính riêng trong công thức", "vendor mới ⇒ sửa công thức", "IX.VEN cột 'cách tính'"],
                 ["headcount NOEM lấy ô cứng của <code>H1000 I HR Report</code>", "HR report đổi dòng / cột ⇒ headcount sai im lặng", "IX.DRV theo khoá (CDT1, tháng)"],
                 ["luật by GI · by NOEM là ghi chú chữ ở ATL B2:C4; ATL N1 'Cần add Formula Allocate'", "ATL = PLA3 PM + HR — chưa phân bổ HQ · GI · NOEM · LE", "IX.ALR có hiệu lực theo kỳ; bật bằng cờ"]]),
             ("báo cáo", [
                 ["PLA3 PM + HR = cộng theo VỊ TRÍ ô của PLA1 và PLA3 HR", "lệch cấu trúc dòng ⇒ cộng sai, ⛔ báo lỗi", "engine cộng theo khoá (HD, ngày)"],
                 ["dòng PL viết trong ô ATL; định nghĩa ở Mapping Master khác (vd LC ở PL3)", "hai định nghĩa cho một dòng PL", "IX.PL một định nghĩa"],
                 ["ATL AH12 = … − 0.5 chỉnh tay", "số chỉnh ⛔ có người, ⛔ lý do", "lớp sửa có actor (⛔ config)"],
                 ["sign-off dán value ở sheet <code>[PLA5]</code>", "số ký ⛔ tự cập nhật, ⛔ biết bản nào", "IX.TMP snapshot có version"]])]),
         dau(3, "c3-2-5", "§3.2.5 IX: cây HD và luật phân bổ hôm nay", inh="c3-2"),
         A2.gap(f"Mở cây HD {tong_hd} dòng (6 nhóm) và 3 luật phân bổ ghi ở ATL B2:C4",
                A2.bang([("nhóm", 22), ("cấp L1 → L4", 78)],
                        [[f"<b>{n}</b> · {E(NHOM_HD[n])}", " · ".join(("&nbsp;" * 2 * (c - 1)) + E(t.split(' | ')[0]) for g, c, t in HD_CAY if g == n)]
                         for n in NHOM_HD])
                + A2.bang([("luật (ATL B2:C4)", 40), ("HD", 60)], [[E(a), " · ".join(b)] for a, b in LUAT_PB])),
         dau(2, "c3-3", "§3.3 CA: hệ báo cáo hôm nay — script và công thức NOW", st="draft"),
         "<p>Tóm từ cột DJ (logic chi tiết) và DK (conflict) của tab <code>PD Now – Logic &amp; Conflict</code>; agent đọc lại nguyên văn ở đó (cột DM có script) trước khi viết mã.</p>",
         dau(3, "c3-3-1", "§3.3.1 CA: quy đổi và khối trước phân bổ (PD 400–419)", inh="c3-3"),
         bang_band(cot_logic, [
             ("nguồn của GL", [
                 ["400", "<code>copyITLTransactions_to_Report_Optimized()</code>: ITL 2/2 › <code>ITL Ledge</code> hàng 10+, 49 cột A:AW, chép đè toàn bộ; AX = YEAR, AY = MONTH", "khớp FS2", "CA.GL đọc thẳng sổ ITL hiệu lực (SI.ITL), ⛔ chép"],
                 ["401–404", "H1000 Ledge NIS/INT/COM + PIT: Y2025 bằng script A:AT; Y2024 bằng IMPORTRANGE", "chỉ có Y2024 · Y2025", "CA.GL đọc dòng họ HR của SI.ITL"],
                 ["405", "<code>9.2.Exchange Rate</code> = IMPORTRANGE <code>APERO | FS2</code>; tra bằng SUMIFS(tháng) và INDEX(MATCH tháng; MATCH tiền tệ)", "bảng đứng yên từ 07/2025; tháng thiếu ⇒ mất số", "IX.FX"]]),
             ("quy đổi", [
                 ["406 · 412", "A10 = QUERY(<code>ITL Ledge</code>); tách Nợ/Có theo 5 tiền tệ; tồn = tồn trên + Nợ − Có; BO/BP = tỷ giá × E|F / 10^9 (bVND); BR/BS = BO|BP ÷ USD × 10^3 (mUSD); CA = VLOOKUP(TK, Mapping Master AB→AD)", "tồn luỹ kế theo thứ tự dòng của cả bảng, ⛔ theo TK ⇒ phụ thuộc sort; tỷ giá theo tháng", "CA.GL: tồn theo (TK, ngày); quy đổi qua IX.FX; Cash/Bank qua IX.ORG"],
                 ["407 · 408 · 413", "như 406 cho HR; AU = AD (CDT1 Final); AV/AW theo Mapping Master K/L; BP chuẩn hoá CDT theo <code>CDT Correct</code>", "BM/BO ép năm 2025; chỉ có sheet Y2025", "năm từ dữ liệu (IX.PER); CDT qua IX.ORG"]]),
             ("khối CF · P&amp;L", [
                 ["409 · 410 · 411", "CFA1 Daily (Templ 3): hàng = cây HD L1–L4, cột = ngày từ G5; lá = SUMIFS(GL!BR mUSD; ngày; HD Final) − SUMIFS(GL!BS …); Y/H/Q/M (Templ 4) = SUMIFS theo hàng header; CFA3 như vậy từ GL HR", "cây gõ cứng theo dòng", "SO.CFA1 · SO.CFA3 = Σ theo (HD, ngày) trên IX.HD"],
                 ["414 · 415", "PLA1 PM-only: như CFA1 nhưng ngày = DATE(PL start) — mọi số dồn vào ngày 1 tháng PL start; cột từ 21/10/2024", "⛔ chia PL start → PL end; dấu: chi phí âm", "SO.PLA1; cách ghi nhận kỳ là quyết định (§3.5.3)"],
                 ["416–419", "PLA3 HR-only; PLA3 PM + HR = ô cùng vị trí của PLA1 + PLA3 HR; Y/H/Q/M theo hàng header", "cộng theo vị trí ô", "SO.PLA3 cộng theo khoá"]])]),
         dau(3, "c3-3-2", "§3.3.2 RP: khối sau phân bổ và báo cáo (PD 605–617)", inh="c3-3"),
         A2.bang(cot_logic, [
             ["605", "<code>[PLA5] Daily Report 3 (Sign off)</code>: bảng giá trị tĩnh Y24/Y25 theo HD + cột 'Logic phân bổ'", "dán value, ⛔ tự cập nhật", "IX.TMP snapshot có version"],
             ["606", "ATL: 9 block, ≈ 2.630 ô link sang <code>PLA3 Y H Q M | PM + HR</code>; PL2 = GI − OMC · PL3 = PL2 − API − SC − LC · PL4 = PL3 − PS · PL6 = PL5 − MC − OTMC − DC − CSO · PL7 = PL6 − GAC − CDC − ITE · PL8 = PL7 − CIT; CHECK NB = 0", "N1 'Cần add Formula Allocate' ⇒ chưa phân bổ; AH12 chỉnh tay −0.5; định nghĩa PL lệch Mapping Master", "SO.PLA3-ATL + IX.PL + IX.ALR"],
             ["607 · 608 · 609", "Daily Report 3 (FS2 · FS1 · bản chính): SUMIFS PLA3 Daily theo ngày, C2 From · C3 To", "chưa rõ bản chính thức gửi BOD; file tự ghi FS2 còn bug", "RP.PL một bản, FS là tham số"],
             ["610", "Daily Report 2 (CF); A-CCR chép bằng <code>copyReport_to_A_CCR()</code> A:AN", "chú thích script ghi nguồn sai tên", "RP.CF"],
             ["614 · 615 · 616", "A-CCR: tỷ giá IMPORTRANGE FS2; <code>exportSheetToPDF()</code> A1:AK2526, A4 ngang, tên 'Daily Report dd/MM/yyyy'; 6. CCR in ký tháng", "<code>createAndSendDailyReport()</code> gọi hàm ⛔ tồn tại (đã đổi tên _off)", "RP.CCR: ghi ô an toàn (<code>xuat/ghi_o</code>) + PDF"]]),
         dau(2, "c3-4", "§3.4 AL: hệ phân bổ hôm nay — script và công thức NOW", st="draft"),
         dau(3, "c3-4-1", "§3.4.1 AL: chi phí nền tảng GI · OMC · SC · PS (PD 501–510 · 600–603)", inh="c3-4"),
         A2.bang(cot_logic, [
             ["501", "<code>syncData_Final_SafeMode()</code>: lọc GL theo V = B4 ('GI | Gross Inflow') → A:AT; AU..BC: Vendor-PL start, STT, mã <code>Vendor-yyyymm-No{n}</code>, PE Amount từ CFA1; BD:BF = FILTER(IMPORTRANGE GL)", "hai nguồn ghép theo vị trí dòng", "AL.PLT đọc GL của CA.GL theo khoá"],
             ["503", "<code>Vendor &amp; Network Mapping</code>: Block 1 M:S (36 dòng); product_id → CDT1; <code>MappingBlock2.gs</code> ghép × 7 CDT1", "script ⛔ xoá vùng cũ trước khi ghi", "IX.VEN"],
             ["504", "<code>CFA1 | GI Platform Data Ledger</code>: một dòng = Vendor × tháng × No; PE Amount = SUMIFS(Looker USD); VD444 · VD341 · VD428 · 'Max' tính riêng; ITL ID = VLOOKUP; PM Amount = VLOOKUP(ITL ID) × 10^6", "vendor đặc biệt gõ cứng", "IX.VEN cột 'cách tính'"],
             ["505 · 506 · 507", "MID1 → MID2 → MID3: RATE = PE của CDT1 ÷ Σ PE 6 CDT1 theo Vendor-tháng; PE_cdt = RATE × O, PM_cdt = RATE × P; O = 0 và P &gt; 0 ⇒ theo tổng tháng; kiểm Σ chia = O / P", "W PM Date chia 6; block 7 / 36 dòng gõ cứng; U3 #REF!", "AL.PLT; KS.AL kiểm Σ chia = tiền"],
             ["508–510 · 600–603", "OMC · SC · PS như GI; P&amp;L chép MID3 bằng <code>copy*Ledger_to_Report_Optimized()</code>", "lỗi <code>row[45]</code> ngoài 30 cột ⇒ ⛔ lọc gì; trạng thái PS đếm nhầm cột; PS thiếu 03–09/2026", "AL.PLT · KS.AL"]]),
         dau(3, "c3-4-2", "§3.4.2 AL: phân bổ theo khoá (PD 500 · 511–513 · 604)", inh="c3-4"),
         A2.bang(cot_logic, [
             ["500", "HR: đã phân bổ ở payroll theo HD / KRF", "—", "⛔ qua ALLOCATE (Q3 · §5.5)"],
             ["511", "By LE: ma trận From LE → To LE, số dư NB (Ps Có − Ps Nợ) mUSD theo tháng 2025-01 → 2026-06", "chỉ theo dõi; ATL ghi 'ALLOCATE by LE (DOING)'", "IX.DRV (NB theo LE); luật: chờ owner"],
             ["512", "By NOEM: tỷ lệ = headcount CDT1 ÷ tổng GAG theo tháng, từ <code>[H1.2026][2025]H1000 I HR Report</code>; áp cho OFR · HCC · REC · BON · OGA (trừ OFR của CAH)", "chỉ 2025; ô cứng; ⛔ sheet nào dùng; mô hình FS2 cũ khác (PBC = HC Venture ÷ (HC Group − HC HQ))", "IX.DRV + IX.ALR"],
             ["513", "By GI: tỷ lệ CDT1 = Σ PE (hoặc Σ PM) ở dòng TOTAL tháng của MID3 GI ÷ tổng; SHQ2 = 100% − Σ; áp cho LC · BRC · CXP · OSF · FNS · CIO · CXB · CXO", "PE hay PM chưa rõ; chỉ 2025; chưa áp vào ATL; FS2 cũ khấu hao 60 tháng", "IX.DRV + IX.ALR"],
             ["604", "<code>Allocation Table | By NOEM &amp; By GI</code>: bảng tỷ lệ tháng 2025", "⛔ sheet nào tham chiếu", "IX.DRV"]]),
         dau(2, "c3-5", "§3.5 AL: engine đề xuất, câu cần chốt và thứ tự dựng", st="review"),
         "<p>Hai bảng đầu là hộp engine và cấu hình chưa dựng (chuyển nguyên từ Part 5 của v2.5.0); hai mục sau là việc mới của bản này.</p>",
    ]
    return "\n".join(o)


def p3_duoi() -> str:
    d = [("D1 · Nguồn tỷ giá", "A · bảng IX.FX kế toán khai, owner ký mỗi tháng; thiếu tháng = CHẶN", "B · đọc tiếp <code>9.2</code> của <code>APERO | FS2</code> như hôm nay",
          "được: giữ đúng AS-IS · mất: bảng đứng yên từ 07/2025, tháng thiếu mất số im lặng", "A", "khi kế toán chọn tỷ giá ngày của ngân hàng thay tỷ giá tháng"),
         ("D2 · Bật luật phân bổ (by GI · NOEM · LE)", "A · engine tái hiện ATL đúng như AS-IS (chưa phân bổ), bật từng luật IX.ALR bằng cờ khi owner ký",
          "B · áp ngay luật ghi ở ATL B2:C4", "được: P&amp;L đúng ý thiết kế sớm · mất: ⛔ còn đáp án để đối chiếu, số khác AS-IS", "A", "khi owner chốt kỳ bắt đầu áp luật"),
         ("D3 · Driver by GI", "A · theo PE (doanh thu kỳ vọng) — cùng gốc với RATE của MID2", "B · theo PM (tiền thực nhận)",
          "được: theo tiền thật · mất: tháng chưa thu tiền thì tỷ lệ lệch", "owner chọn — đề xuất A", "khi ATL chính thức đã dùng một trong hai"),
         ("D4 · Ghi nhận kỳ P&amp;L", "A · như AS-IS: dồn vào ngày 1 tháng PL start", "B · chia đều PL start → PL end",
          "được: dịch vụ nhiều tháng ghi đúng kỳ · mất: khác AS-IS, cần đáp án mới", "A trước, B sau khi owner ký", "khi owner muốn P&amp;L theo kỳ dịch vụ thật"),
         ("D5 · Bản Daily Report 3 chính thức", "A · bản A-CCR chép (<code>5. Daily Report 3</code>), FS là tham số", "B · giữ ba bản FS1 · FS2 · FS3 song song",
          "được: so được từng bản · mất: ba bản một báo cáo, file tự ghi FS2 còn bug", "A", "khi BOD đọc bản khác")]
    rows = [[f"<b>{a}</b>", f"<b>{b}</b><br><i>mất:</i> {('mỗi tháng thêm một bước khai — mất tự động' if a.startswith('D1') else 'P&amp;L chưa phân bổ thêm một thời gian' if a.startswith('D2') else 'lệch với tiền thật khi PE khác PM' if a.startswith('D3') else 'dịch vụ nhiều tháng vẫn dồn một tháng' if a.startswith('D4') else 'phải xác nhận bản ấy là bản BOD đọc')}",
             f"<b>{c}</b><br>{p}", f'<span class="badge new">RECOMMENDED</span> {w}', f] for a, b, c, p, w, f in d]
    wp = [("WP-C1 · chiều", "IX.FX · IX.ORG · IX.HD · IX.PER", "bảng 9.2 FS2 · Mapping Master · cây ATL 74 dòng", "nạp được 37 tháng, 74 dòng HD, 0 dòng trùng; thiếu tháng = đỏ"),
          ("WP-C2 · quy đổi", "CA.GL", "<code>Report I General Ledger</code> CALC ZONE (406)", "từng ô BM–BT khớp, mọi tháng có dữ liệu"),
          ("WP-C3 · khối trước PB", "SO.CFA1 · SO.CFA3 · SO.PLA1 · SO.PLA3", "sheet 409–419", "từng ô Daily + Y/H/Q/M khớp"),
          ("WP-C4 · phân bổ nền tảng", "IX.VEN · AL.PLT · KS.AL", "CFA1 · MID1–MID3 của 4 sổ nền tảng", "Σ chia = O / P; từng ô MID3 khớp"),
          ("WP-C5 · khoá, ATL, báo cáo", "IX.DRV · IX.ALR · AL.KEY · IX.PL · SO.PLA3-ATL · IX.TMP · RP.*", "604 · 606 · 607–616", "ATL khớp AS-IS khi cờ luật tắt (D2); Daily Report 2 · 3 khớp từng ô")]
    return "\n".join([
        dau(3, "c3-5-3", "§3.5.3 AL: câu cần chốt cho config", inh="c3-5"),
        "<p>Năm câu, mỗi câu từ một conflict cột DK. A có cả cái mất; B giữ lại kể cả khi bị bác. Owner chốt — tác giả ⛔ tự chốt.</p>",
        A2.bang([("câu", 18), ("A · đề xuất", 28), ("B · phương án khác", 26), ("phán", 12), ("điều sẽ làm đổi ý", 16)], rows),
        dau(3, "c3-5-4", "§3.5.4 AL: thứ tự dựng — năm gói việc trước agent", inh="c3-5"),
        "<p>Mỗi gói đi đúng vòng §1.3; đáp án là sheet NOW cùng cột của Figure 3.1. Gói sau chỉ bắt đầu khi gói trước khớp.</p>",
        A2.bang([("gói", 16), ("dựng", 28), ("đáp án NOW", 28), ("cổng xong", 28)], [[f"<b>{a}</b>", b, c, e] for a, b, c, e in wp]),
    ])


def p4_moi_cha() -> str:
    return (dau(2, "n4-4", "§4.4 KS: cổng, cấu hình, kho và màn hình đã có", st="draft")
            + "\n<p>Gộp hai mục của v2.5.0 (§3.4 · §3.5) dưới một mục cha để Part 4 giữ ≤ 5 mục.</p>")


def chuyen_hang() -> str:
    nhom = [("Part 3 cũ → Part 4", [["§3.1 · §3.2 · §3.3", "§4.1 · §4.2 · §4.3", "đổi số"], ["§3.4 · §3.5", "§4.4.1 · §4.4.2", "hạ cấp dưới §4.4 mới"]]),
            ("Part 4 cũ → Part 5", [["§4.1 · §4.2", "§5.1 · §5.2", "đổi số"], ["§4.3 · §4.4 (Figure 4.4)", "§5.3 · §5.4 (Figure 5.4)", "thêm AC9"]]),
            ("Part 5 cũ → rải ra", [["§5.1", "§4.5", "HR · PLT"], ["§5.2 · §5.3", "§3.5.1 · §3.5.2", "vào lõi config"],
                                     ["§5.4 · §5.4.1 · §5.4.2", "§1.5 · §1.5.3 · §1.5.4", "phủ PD Now về nguồn"], ["§5.5", "§5.5", "giữ số"]])]
    hang, nhan, i = [], {}, 0
    for t, ds in nhom:
        nhan[i] = t
        hang += ds
        i += len(ds)
    return A2.gap("Cho người cầm link v2.5.0: mục cũ nằm ở đâu bây giờ (id giữ nguyên)",
                  A2.bang([("v2.5.0", 30), ("v3.0.0", 34), ("ghi chú", 36)], hang, nhom=nhan))


def header() -> str:
    h0 = A2.header()
    h0 = h0.replace("<tr><th>Version</th><td>2.5.0 · 2026-11-13</td></tr>", f"<tr><th>Version</th><td>3.0.0 · {NGAY}</td></tr>")
    cu = re.search(r"<tr><th>Changes in v2\.5\.0</th><td>(.*?)</td></tr>", h0, re.S)
    moi = (f"<tr><th>Changes in v3.0.0</th><td>Level-1 vì đổi số cây. Thêm <b>Part 3 · Lõi config chung</b> (hệ báo cáo + hệ phân bổ, dựng trước agent): "
           "voi Figure 3.1, mười bảng config, 14 chỗ AS-IS gõ cứng → config, script + công thức NOW của PD 400–419 · 500–513 · 605–617 "
           "(nguồn: Drive folder owner gửi 16/11, tab <code>PD Now – Logic &amp; Conflict</code>), 5 câu cần chốt, 5 gói việc. "
           "Đổi số: Part 3 cũ → Part 4 · Part 4 cũ → Part 5 · Part 5 cũ rải về §1.5 · §3.5 · §4.5 · §5.5 (bảng §1.5.5); id giữ nguyên. "
           "Sửa chữ: §1.5 (đổi tên) · §1.5.1 (Part 1 · 3 · 4 · 5) · §5.3 (+AC9) · §5.4 (lưới thêm AC9).</td></tr>")
    h0 = h0.replace(cu.group(0), moi)
    lich = re.search(r'(<details><summary><b>)6 sửa đổi trước đó(</b> — )v2 → v2\.4 \(bản nháp, ⛔ AP\)(</summary><table style="margin-top:8px">)', h0)
    h0 = h0.replace(lich.group(0), f"{lich.group(1)}7 sửa đổi trước đó{lich.group(2)}v2 → v2.5.0{lich.group(3)}"
                    f'<tr><th style="white-space:nowrap;vertical-align:top">v2.5.0</th><td>2026-11-13 · {cu.group(1)}</td></tr>')
    return h0


def trang() -> str:
    m = muc_cu()
    ac9 = ('<tr><td><b>AC9</b></td><td>L5</td><td>Một bảng config (Part 3) chỉ được ghi "xong" khi engine đọc nó ra đúng từng ô của sheet NOW cùng cột Figure 3.1, ở mọi tháng có dữ liệu.</td>'
           f'<td>UF-1.5</td><td>chưa đo — 0/10 bảng config có mã engine · {NGAY}</td></tr>')
    m["s4-3"]["than"] = m["s4-3"]["than"].replace("</table></div>", ac9 + "\n</table></div>", 1) if m["s4-3"]["than"].count("</table></div>") == 1 else (_ for _ in ()).throw(SystemExit("⛔ s4-3"))
    a = '<tr><td class="lbl">UF-1.5</td><td class="hole">▢</td><td class="hole">▢</td><td class="hole">▢</td><td class="hole">▢</td><td>AC5 · AC6</td></tr>'
    assert m["s4-4"]["than"].count(a) == 1
    m["s4-4"]["than"] = m["s4-4"]["than"].replace(a, a.replace("AC5 · AC6", "AC5 · AC6 · AC9"))
    m["s4-4"]["than"] = m["s4-4"]["than"].replace("(AC1–AC8 đều xuất hiện)", "(AC1–AC9 đều xuất hiện)")
    th = []
    # Part 1 — giữ, §1.5 thêm phủ PD Now + bảng chuyển hàng
    p1_ids = ["s1-1", "s1-1-1", "s1-1-2", "s1-2", "s1-2-1", "s1-2-2", "s1-3", "s1-3-1", "s1-3-2", "s1-3-3", "s1-4", "s1-4-1", "s1-4-2"]
    th.append(A2.part(1, "SYSTEM · khung, voi và cách giao việc"))
    for u in p1_ids:
        num = re.search(r">§([\d.]+)", m[u]["tag"]).group(1)
        th.append(dung_lai(m, u, num, m[u]["lvl"]))
    th.append(dung_lai(m, "s1-5", "1.5", 2, ten_moi="nguồn, đổi số và phủ PD Now"))
    th.append(dung_lai(m, "s1-5-1", "1.5.1", 3))
    th.append(dung_lai(m, "s1-5-2", "1.5.2", 3))
    th.append(dung_lai(m, "s5-4-1", "1.5.3", 3, inh_moi="s1-5"))
    th.append(dung_lai(m, "s5-4-2", "1.5.4", 3, inh_moi="s1-5"))
    th.append(dau(3, "n1-5-5", "§1.5.5 SYSTEM: đổi số từ v2.5.0 sang v3.0.0", inh="s1-5") + "\n" + chuyen_hang())
    # Part 2 — giữ nguyên
    th.append(A2.part(2, "KS · Voi số lượng dữ liệu"))
    for u in ["s2-1", "s2-1-1", "s2-1-2", "s2-2", "s2-3", "s2-4", "s2-5", "s2-5-1", "s2-5-2", "s2-5-3"]:
        num = re.search(r">§([\d.]+)", m[u]["tag"]).group(1)
        th.append(dung_lai(m, u, num, m[u]["lvl"]))
    # Part 3 — MỚI
    th.append(p3_moi())
    th.append(dung_lai(m, "s5-2", "3.5.1", 3, inh_moi=""))
    th.append(dung_lai(m, "s5-3", "3.5.2", 3, inh_moi=""))
    th.append(p3_duoi())
    # Part 4 — Part 3 cũ + HR · PLT
    th.append(A2.part(4, "Truy vết NOW → TO-BE → code · phần đã có, và họ HR · PLT"))
    for u, n in (("s3-1", "4.1"), ("s3-2", "4.2"), ("s3-3", "4.3"), ("s3-3-1", "4.3.1"), ("s3-3-2", "4.3.2")):
        th.append(dung_lai(m, u, n, m[u]["lvl"]))
    th.append(p4_moi_cha())
    th.append(dung_lai(m, "s3-4", "4.4.1", 3, inh_moi=""))
    th.append(dung_lai(m, "s3-5", "4.4.2", 3, inh_moi=""))
    th.append(dung_lai(m, "s5-1", "4.5", 2))
    # Part 5 — Part 4 cũ + câu chờ owner
    th.append(A2.part(5, "SYSTEM · Userflows, nghiệm thu và câu chờ owner"))
    for u, n in (("s4-1", "5.1"), ("s4-2", "5.2"), ("s4-3", "5.3"), ("s4-4", "5.4"), ("s5-5", "5.5")):
        th.append(dung_lai(m, u, n, 2))
    dung = {u for u in m} - BO_DON_VI
    da = set(re.findall(r'id="(s[\d-]+)"', "\n".join(th)))
    assert dung <= da, sorted(dung - da)
    than = "\n".join(th)
    style = (A2.SKILL / "ap-style.css").read_text(encoding="utf-8")
    toc = (A2.SKILL / "ap-toc.js").read_text(encoding="utf-8")
    return f"""<!doctype html>
<!-- AP_FLS-Voi_v3.0.0_Loi-Config-Chung_2026-11-16.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v3.py · v2.5.0 đóng băng -->
<html lang="vi"><head>
<meta charset="utf-8">
<meta name="ap:lineage" content="AP_FLS-Voi">
<meta name="ap:branch" content="">
<meta name="ap:version" content="3.0.0">
<meta name="ap:parent" content="">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AP Voi FLS v3.0.0</title>
<style>
{style}
{A2.AP_CSS}
.voi3{{overflow-x:auto}} .voi3 svg{{display:block;max-width:none}}
{A2.css_voi()}
</style></head>
<body>
<nav class="toc"><p class="toc-title">Contents</p><div id="toc"></div></nav>
<main>
<h1>AP · Voi FLS v3.0.0 — lõi config chung, đối chiếu NOW ↔ TO-BE và Voi số lượng dữ liệu</h1>
{header()}
{than}
</main>
<script>
{toc}
</script>
</body></html>
"""


def main() -> int:
    s = trang()
    for tag in ("table", "tr", "div", "svg", "details", "ul"):
        a, b = len(re.findall(rf"<{tag}[\s>]", s)), s.count(f"</{tag}>")
        assert a == b, (tag, a, b)
    assert s.count('ap:lineage" content=') == 1
    RA.write_text(s, encoding="utf-8")
    print(f"✅ đã ghi {RA.relative_to(GOC)} · {len(s):,} byte")
    return 0


CONG = A2.CONG

if __name__ == "__main__":
    raise SystemExit(main())
