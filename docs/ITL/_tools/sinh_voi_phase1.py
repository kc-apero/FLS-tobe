# -*- coding: utf-8 -*-
"""Sinh `docs/ITL/02_BA/Artifacts/Voi-FLS-tobe-phase1.html` từ MỘT bản khai hộp + mũi tên.

    python docs/ITL/_tools/sinh_voi_phase1.py          # sinh + kiểm, in số đếm
    python docs/ITL/_tools/sinh_voi_phase1.py --kiem   # chỉ kiểm, ⛔ không ghi

⭐ Vì sao sơ đồ được SINH, ⛔ không vẽ tay (luật `apr-vevoi`, mục *diagram truth gate*):
  ⓐ mọi mũi tên phải THẲNG, chỉ nối hai dải KỀ NHAU (hoặc hai hộp cùng dải),
  ⓑ ⛔ không mũi tên nào cắt qua một hộp, ⛔ không hai mũi tên nào cắt nhau,
  ⓒ 2–5 hộp mỗi dải, ≤ 5 dải mỗi vùng,
  ⓓ bảng "mũi tên nói gì", bảng kiểm cạnh và khung chi tiết tương tác lấy từ CÙNG
     bản khai với hình ⇒ hình, bảng và khung ⛔ không thể lệch nhau.
  Vẽ tay thì cả bốn điều trên chỉ là lời hứa; ở đây máy NỔ nếu sai một điều.

⭐ Đầu ra là trang ARTIFACT (claude.ai): ⛔ không `<!doctype>`/`<html>`/`<body>` riêng
  — nền tảng bọc khung lúc đăng. Trang khai năng lực `comments` để người xem bình
  luận / gửi câu hỏi cho Claude gắn đúng vào hộp hay mũi tên đang chọn.

⛔ PD Now là bản THAM KHẢO: chỉ mượn THUẬT NGỮ (PE · PI · PM · PC · LE · CDT ·
   HD/KRF · Reference No · General Trustest), ⛔ không mượn tên sheet / file / bước.

v0.3 (2026-11-04, owner): nguồn FPS là **sổ cái PM / PC** — đã mang đủ chiều —
   ⛔ không đọc phiếu PE/PI và danh mục riêng.
"""
from __future__ import annotations

import html
import json
import sys
from dataclasses import dataclass
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
DICH = GOC / "docs/ITL/02_BA/Artifacts/Voi-FLS-tobe-phase1.html"

# ───────────────────────────── lưới ─────────────────────────────
# v0.4 (owner 06/11): MỘT hình có cả TO-BE (trái) và AS-IS (phải), chung dải — AS-IS xếp vào đúng các
#   lớp của TO-BE, ⛔ sinh lớp mới. Bỏ bớt chữ: hộp chỉ còn tên + một dòng (NGAN), chi tiết ở khung bấm.
#   Bảy cột, CÙNG nghĩa ở hai bên: 1 lệnh chi · 2 tham chiếu/bản khai · 3 bank · 4 quỹ · 5 CCR · 6 lương · 7 nền tảng.
W, H = 1780, 736
C0 = (102, 176)                         # cột 0: điểm khởi động của vùng FLS
SH = 10                                 # cạnh hộp lùi vào chỗ có mũi tên NGANG (khe 8 → 28)
XA0 = 994                               # cột 1 của AS-IS
COT_NGHIA = ("lệnh chi", "bản khai", "bank", "quỹ", "CCR", "lương", "nền tảng")


def cot(i: int) -> tuple[int, int]:
    x = 186 + (i - 1) * 112
    return x, x + 104


def cota(a: int, b: int | None = None) -> tuple[int, int]:
    b = b or a
    return XA0 + (a - 1) * 112, XA0 + (b - 1) * 112 + 104


def nhip(a: int, b: int, trai: int = 0, phai: int = 0) -> tuple[int, int]:
    return cot(a)[0] + trai, cot(b)[1] - phai


def tam(i: int) -> float:
    a, b = cot(i)
    return (a + b) / 2


# dải: (vùng, y, cao, nhãn rail)
DAI = {
    "A0": ("A", 46, 36, "ai sinh ra"),
    "A1": ("A", 104, 44, "sổ nguồn"),
    "B0": ("B", 46, 36, ""),
    "B1": ("B", 104, 44, ""),
    "G0": ("G", 46, 36, ""),
    "G1": ("G", 104, 44, ""),
    "H0": ("H", 46, 36, ""),
    "H1": ("H", 104, 44, ""),
    "c1": ("C", 192, 42, "① KHAI & CHỤP"),
    "c2": ("C", 262, 42, "② DỰNG"),
    "c3": ("C", 332, 42, "③ MAPPING"),
    "c4": ("C", 402, 42, "④ SOÁT"),
    "c5": ("C", 472, 42, "⑤ GHI"),
    "d1": ("D", 540, 42, "⑥ SỔ GỐC"),
    "d2": ("D", 610, 42, "⑦ HIỆU LỰC"),
    "e1": ("E", 678, 42, "⑧ NGƯỜI THẤY"),
}
TANG = {"A0": 0, "B0": 0, "G0": 0, "H0": 0, "A1": 1, "B1": 1, "G1": 1, "H1": 1, "c1": 2, "c2": 3, "c3": 4, "c4": 5, "c5": 6, "d1": 7, "d2": 8, "e1": 9}
VUNG = {   # mã: (nhãn, nhãn phụ, y0, y1)
    "C": ("NẠP", "chưa vào sổ", 184, 522),
    "D": ("SỔ", "PostgreSQL · chỉ-thêm", 532, 660),
    "E": ("RA", "màn FLS + hệ khác", 670, 728),
}
TEN_VUNG = {"A": "Nguồn ngoài · FPS", "B": "Phương pháp xử lý (1) · mapping với bank transaction — sao kê · sổ quỹ · CCR",
            "G": "Phương pháp xử lý (2) · HR", "H": "Phương pháp xử lý (3) · nền tảng", "C": "FLS · NẠP",
            "D": "FLS · SỔ", "E": "ĐẦU RA"}


@dataclass
class Hop:
    ma: str
    dai: str
    x: tuple[int, int]
    loai: str            # o khởi động · x ngoài FLS · d dữ liệu · p xử lý
    tt: str              # b có mã · q GĐ1 đã chốt, chưa dựng · n đề xuất trang này
    ten: str
    dong: tuple[str, ...] = ()
    mono: str = ""
    huy: tuple[str, ...] = ()        # huy hiệu khởi động S1..S5
    tang: str = ""                   # "tren" | "duoi" cho hộp xếp chồng ở cột 0
    doi_chieu: str = ""              # đối chiếu mã / tài liệu (bảng kiểm cạnh)
    luong: tuple[str, ...] = ()      # luồng xử lý tổng quan, ≤ 5 bước (gán từ LUONG bên dưới)
    nm: tuple[str, ...] = ()         # (chiều VÀO/RA, MÁY|NGƯỜI|NGƯỜI+MÁY, ai, rủi ro & cổng) — gán từ NGUON_NM
    khoi: str = ""                   # khung chứa (vd "pp1" = phương pháp xử lý 1) — tính MỘT mục khi đếm dải
    goc: tuple[str, ...] = ()        # AS-IS: mã các hộp gốc của artifact "Voi ITL AS-IS" gộp vào hộp này
    tay: bool = False                # AS-IS: có bước NGƯỜI bấm / gõ ở đây

    @property
    def y(self) -> tuple[float, float]:
        _v, y0, h, _n = DAI.get(self.dai) or DAI_M.get(self.dai) or DAI_N[self.dai]
        if self.tang == "tren":
            return y0, y0 + h / 2 - 4
        if self.tang == "duoi":
            return y0 + h / 2 + 4, y0 + h
        return y0, y0 + h


HOP: list[Hop] = [
    # ── ngoài FLS · FPS — v0.3: SỔ CÁI PM / PC ──
    Hop("oPM", "A0", cot(1), "o", "b", "LẬP & DUYỆT PM · PC", ("lệnh chi · quyết toán trong FPS",),
        doi_chieu="ngoài FLS — FLS chỉ đọc dòng đã vào sổ cái"),
    Hop("soPM", "A1", cot(1), "x", "b", "sổ cái PM · PC",
        ("1 dòng = 1 PM line / PC line", "PE·PI · HD · CDT1 · Ref No · PC: quyết toán, hoàn ứng"),
        "PM 28 cột · 3.772 dòng · PC chưa đọc",
        doi_chieu="AS-IS đọc PM qua tab PM_Unpivot: 28 cột có tên (pm_join.py, G-MOD-3) — 14 có kiểu · 1 cấm · 13 thô; "
                  "PC: 0 tham chiếu trong fls/ · tools/ · tests/"),
    # ── ngoài FLS · Google Sheets ──
    Hop("oKTnh", "B0", cot(3), "o", "b", "KẾ TOÁN NGÂN HÀNG", ("dán sao kê vào sheet R |",),
        doi_chieu="ngoài FLS — 60 dòng chảy ngân hàng có bản khai dòng 1"),
    Hop("oKTq", "B0", cot(4), "o", "b", "KẾ TOÁN QUỸ", ("ghi sổ quỹ hằng ngày",),
        doi_chieu="ngoài FLS — 8 dòng chảy quỹ có bản khai dòng 1"),
    Hop("oCCR", "B0", cot(5), "o", "b", "NGƯỜI NHẬP SỐ DƯ", ("số dư ngày từng TK",),
        doi_chieu="ngoài FLS — người nhập chưa xác định (FLS-Process-PM-den-ITL §8 #14)"),
    Hop("oHR", "G0", cot(6), "o", "b", "HR · C&B", ("lập sổ lương",), doi_chieu="ngoài FLS"),
    Hop("oNT", "H0", cot(7), "o", "b", "DATA · SHQ1 · SHQ2", ("GI · OMC: Data (AnhTQ) xuất Looker · SC: Luận · PS: kế toán",),
        doi_chieu="ngoài FLS — PD Now bước 103–106 (owner 06/11: Looker chỉ GI · OMC; SC · PS ở Google Sheets)"),
    Hop("saoke", "B1", cot(3), "x", "b", "sao kê ngân hàng", ("60 dòng chảy", "19 bố cục cột"), "sheet R |",
        doi_chieu="tools/nap_nguon_va_khai.py (60 ngân hàng + 8 quỹ = 68 nguồn)"),
    Hop("soquy", "B1", cot(4), "x", "b", "sổ quỹ", ("8 dòng chảy", "kế toán ghi tay"), "sheet R |",
        doi_chieu="như trên"),
    Hop("ccr", "B1", cot(5), "x", "b", "CCR · CCR Cash", ("số dư ngày từng TK / quỹ", "Treasury ↔ Accounting"), "A-CCR · 2 sheet",
        doi_chieu="A-CCR: sheet 2. CCR (229 × 655 cột ngày) và 2. CCR Cash — tools/do_trong_tai.py chỉ ĐO, ⛔ ghi"),
    Hop("soluong", "G1", cot(6), "x", "b", "sổ H1000 (lương · BH · PIT)",
        ("6 sổ năm NIS/INT/COM · PIT (có 2026)", "đã tách HD · CDT1 · pháp nhân từng nhân viên; số FT do kế toán dán"),
        "AS-IS [dH1000] · nạp thẳng (owner 06/11)",
        doi_chieu="AS-IS: file lương tháng → sheet No n → 1.3 Ledger → H1000 Ledger năm; 0 tham chiếu trong fls/"),
    Hop("sont", "H1", cot(7), "x", "b", "4 sổ Platform Data Ledger",
        ("GI · OMC: Source (Looker) · SC: Gsheet 'Chi phí Service Apero' · PS: Gsheet 'AperoGroup_Payment'",
         "có PE/PM trên FPS · nối dòng ITL qua Combine Code"), "H2.2025 · PD Now 210–213",
        doi_chieu="PD Now 103–106 (nguồn) · 210–213 (Platform Data Ledger); 0 tham chiếu trong fls/ (Platform chỉ là enum)"),
    # ── c1 · KHAI & CHỤP ──
    Hop("S1", "c1", C0, "o", "b", "S1 · NHỊP", ("mỗi giờ 8h–19h",), tang="tren", khoi="kd1",
        doi_chieu="fls/repo/nhip_chup.py (QĐ-ITL-114) · tools/nhip_chup.py chụp Bank + PM"),
    Hop("S2", "c1", C0, "o", "b", "S2 · KHAI", ("kế toán · F04",), tang="duoi", khoi="kd1",
        doi_chieu="POST khai-cot · thu-tu (fls/api)"),
    Hop("anhFPS", "c1", (cot(1)[0], cot(1)[1] - SH), "d", "q", "ảnh sổ cái FPS",
        ("PM + PC, đóng băng mỗi lần chụp", "hôm nay: chỉ PM, đọc qua Sheets"), "fls_pm_line 3.772 · PC chưa có",
        huy=("S1",), doi_chieu="fls_pm_line (migration 0011/0023) · fls/repo/anh_pm.py; PC: chưa có bảng"),
    Hop("khai", "c1", (cot(2)[0] + SH, cot(2)[1] - SH), "d", "b", "bản khai nguồn",
        ("cột · thứ tự ngày", "+ pháp nhân TK từ tên sheet · Mapping Master"), "fls_khai_cot 408", huy=("S2",),
        doi_chieu="fls/repo/khai_cot.py (chỉ-thêm, có version); AS-IS: tên sheet R | <TK>_<bank> <tiền tệ>_<LE> + Mapping Master sheet → LE", khoi="pp1"),
    Hop("anhTien", "c1", (cot(3)[0] + SH, cot(5)[1]), "d", "b", "ảnh sao kê · sổ quỹ · CCR",
        ("lằn Bank ✅ 60 nguồn · 182 ảnh · lằn Cash ⛔ · lằn CCR ⛔",
         "đọc vùng chuẩn THEO bản khai · + Reference number_adjust (người đè mã, 58/60 nguồn)"),
        "fls_chup · fls_chup_nguon (khai_version)", huy=("S1",),
        doi_chieu="tools/chup_sao_ke.py (LAN='Bank') · fls/repo/chup.py:16 khai_version", khoi="pp1"),
    Hop("anhHR", "c1", cot(6), "d", "q", "ảnh sổ lương HR",
        ("lằn HR ⛔", "6 sổ H1000 · từng dòng nhân viên"), "fls_chup lằn 'HR'", huy=("S1",),
        doi_chieu="chưa có: chup_sao_ke.py chỉ chụp lằn Bank", khoi="pp2"),
    Hop("anhNT", "c1", cot(7), "d", "q", "ảnh nguồn nền tảng",
        ("lằn Platform ⛔", "Looker (GI · OMC) + 2 Gsheet (SC · PS)"), "fls_chup 'Platform'", huy=("S1",),
        doi_chieu="chưa có: chup_sao_ke.py chỉ chụp lằn Bank", khoi="pp3"),
    # ── c2 · DỰNG ──
    Hop("S3", "c2", C0, "o", "b", "S3 · XEM LÔ", ("kế toán chọn lô", "màn F04"),
        doi_chieu="POST /nap/lo/xem-truoc"),
    Hop("dLenh", "c2", cot(1), "p", "q", "DỰNG dòng lệnh",
        ("mỗi PM / PC line → tiền · Ref · HD/KRF", "· CDT1 · đối tác · kỳ DV · pháp nhân trả"),
        "khoá: pm_line_id · pc_line_id", huy=("S3", "S4"),
        doi_chieu="có một phần: fls_pm_line đặt kiểu 14 cột (PM_COT); PC + cột còn thô: chưa"),
    Hop("dTien", "c2", nhip(2, 5), "p", "b", "DỰNG dòng tiền + số dư ngày",
        ("lằn Bank · Cash → canon 36 trường, đủ hai vế PS Nợ và PS Có · gắn pháp nhân TK từ bản khai",
         "lằn CCR → số dư ngày từng TK / quỹ (đầu kỳ + mỗi ngày) · content_key chống trùng"),
        "bank 8.338/8.338 · quỹ chưa chạy · pháp nhân: chưa", huy=("S3", "S4"),
        doi_chieu="fls/adapters/sao_ke.py + sao_ke_canon.py", khoi="pp1"),
    Hop("dHR", "c2", cot(6), "p", "q", "DỰNG dòng lương",
        ("nạp thẳng H1000: HD · CDT1 · pháp nhân", "dòng đảo mang Số CT bank"), "owner 06/11: ⛔ tự khớp Σ",
        huy=("S3", "S4"), khoi="pp2",
        doi_chieu="chưa có (adapter D) · AS-IS [pTACH] đã tách tới từng nhân viên · 5 pháp nhân × 5 loại"),
    Hop("dNT", "c2", cot(7), "p", "q", "DỰNG chi phí nền tảng",
        ("4 loại → vendor · CDT1 · tháng", "+ Combine Code Vendor-Date-NoTrans"), "chi tiết: §1c",
        huy=("S3", "S4"), doi_chieu="chưa có (adapter E)", khoi="pp3"),
    # ── c3 · MAPPING — tách theo nhóm (owner 04/11): phần chưa khớp chuyển NGANG sang nhóm kế ──
    Hop("ghep", "c3", (cot(1)[0], cot(5)[1] - SH), "p", "b", "MAPPING PP (1) · bank txns ↔ lệnh chi (Reference No) · cả PS Nợ và PS Có",
        ("PS Có (tiền ra): Reference No → PM line, chia tiền theo line · PS Nợ (tiền vào): luật vế Nợ (§1b)",
         "Σ line = tiền dòng, lệch ⇒ chặn · khác tiền tệ · N×M ⇒ để người · ra 3 lớp L1 · L2 · L3"),
        "hôm nay chỉ ghép vế PS Có (mẫu số 8.246) · nối 26,79% dòng", huy=("S4",), khoi="m1",
        doi_chieu="fls/adapters/pm_join.py · chay_nap.py:637 chen_moi_noi"),
    Hop("ghep2", "c3", (cot(6)[0] + SH, cot(6)[1] - SH), "p", "q", "MAPPING PP (2)",
        ("dòng lương ↔ bank", "theo Số CT (số FT)"), "AS-IS [dH1F] VLOOKUP Số CT", huy=("S4",), khoi="m2",
        doi_chieu="chưa có · owner 06/11: nạp thẳng H1000"),
    Hop("ghep3", "c3", (cot(7)[0] + SH, cot(7)[1]), "p", "q", "MAPPING PP (3)",
        ("Combine Code → PE/PM", "→ Ref → bank · chia CDT1"), "chi tiết §1c", huy=("S4",), khoi="m3",
        doi_chieu="chưa có · AS-IS [oALL] map PE qua PM theo Combine Code · owner 06/11: phải tới bank txns"),
    # ── c4 · SOÁT — mỗi nhóm một bộ luật soát ──
    Hop("soat", "c4", nhip(1, 5), "p", "b", "SOÁT PP (1)",
        ("9 luật sao kê · CHẶN ⇒ nguồn bị chừa · CỜ ⇒ vẫn ghi, vào hàng chờ · 4 vế cân · biên bản 9 dòng trên F04",
         "số dư đầu + Σ PS Nợ − Σ PS Có theo ngày = số dư CCR / CCR Cash (DIF = 0), lệch liệt kê từng TK · từng ngày"),
        "fls/kiem/soat_nap.py", huy=("S3", "S4"), khoi="m1",
        doi_chieu="fls/kiem/soat_nap.py · chay_nap.py:611 cổng bốn đường · QĐ-ITL-112"),
    Hop("soat2", "c4", cot(6), "p", "q", "SOÁT PP (2)",
        ("Σ Có = Σ Nợ mỗi đợt", "đủ tháng · ⛔ tháng trùng"), "chưa có", huy=("S3", "S4"), khoi="m2",
        doi_chieu="chưa có"),
    Hop("soat3", "c4", cot(7), "p", "q", "SOÁT PP (3)",
        ("Σ phần chia = tiền", "Σ % CDT1 = 100"), "chưa có", huy=("S3", "S4"), khoi="m3",
        doi_chieu="chưa có"),
    # ── c5 · GHI ──
    Hop("S4", "c5", C0, "o", "b", "S4 · NHẬN", ("kế toán · F04",), tang="tren", khoi="kd4",
        doi_chieu="POST /nap/lo"),
    Hop("S5", "c5", C0, "o", "b", "S5 · SỬA", ("kế toán · F01·F02",), tang="duoi", khoi="kd4",
        doi_chieu="POST match · adjust · reverse · …"),
    Hop("ghiNap", "c5", nhip(1, 7), "p", "b", "GHI lượt nạp — một giao dịch cho cả 3 nhóm",
        ("run · dòng sổ · dòng loại · mối nối máy (PP 1) · dòng lương nối Số CT (PP 2) · phần chia CDT1 (PP 3) · gợi ý hd/cdt1",
         "lỗi giữa chừng ⇒ ⛔ không còn dòng nào đã ghi"),
        "fls/repo/chay_nap.py — hôm nay chỉ phần PP (1)", huy=("S4",),
        doi_chieu="chay_nap.py:621 `with conn.transaction()`"),
    # ── d1 · SỔ GỐC ──
    Hop("loai", "d1", cot(1), "d", "b", "dòng bị loại", ("mỗi dòng một", "lý do có tên"), "fls_reject",
        doi_chieu="schema.py fls_reject"),
    Hop("soITL", "d1", nhip(2, 3), "d", "b", "SỔ ITL",
        ("một bảng · 4 họ nguồn · đủ PS Nợ và PS Có", "chỉ-thêm · ⛔ không PUT/DELETE"),
        "fls_itl 8.387 · hôm nay 1 họ nguồn",
        doi_chieu="schema.py fls_itl · INV-I08 · source_system khai 4 giá trị"),
    Hop("lopSua", "d1", (cot(4)[0], cot(6)[1] - SH), "d", "b", "lớp sửa chỉ-thêm (gộp vẽ)",
        ("mối nối · bỏ nối · bút toán (người / máy gợi ý) · sự kiện · nhật ký",
         "sửa = thêm dòng · dòng sổ ⛔ không đổi một ô"),
        "fls_pm_link 2.263 · fls_adjustment 4.428 · fls_journal",
        doi_chieu="fls_pm_link · fls_pm_unlink · fls_adjustment · fls_queue_event · fls_journal"),
    Hop("ghiTay", "d1", (cot(7)[0] + SH, cot(7)[1]), "p", "b", "GHI tay",
        ("ghép · sửa · đảo · lý do", "actor từ thẻ đăng nhập"),
        "chỗ ghi duy nhất", huy=("S5",),
        doi_chieu="fls/repo/ghi_tay.py"),
    # ── d2 · HIỆU LỰC ──
    Hop("kiem", "d2", (cot(1)[0], cot(1)[1] - SH), "p", "q", "KIỂM cổng GĐ1",
        ("mỗi cổng khai mong",), "đỏ khi khác",
        doi_chieu="/gates có 8 cổng · cổng GĐ1 (§3 nhóm 5): chưa"),
    Hop("hieuLuc", "d2", (cot(2)[0] + SH, cot(7)[1]), "d", "q", "SỔ ITL HIỆU LỰC — bảng ITL duy nhất của GĐ1",
        ("dòng sổ + giá trị đang hiệu lực (người › máy gợi ý › nguồn) + chiều lệnh chi + 3 vai pháp nhân",),
        "hôm nay: ghép tại cửa đọc (doc_bao_cao + 7 view) · GĐ1: một view có tên, đủ 4 họ",
        doi_chieu="fls/repo/doc_bao_cao.py · view fls_sua_tay / fls_may_goi_y / fls_moi_noi …"),
    # ── e1 · NGƯỜI THẤY · HỆ KHÁC ──
    Hop("f03", "e1", cot(1), "d", "b", "màn F03 · cổng", ("đạt · không đạt", "· chưa đo được"),
        doi_chieu="fls/web/tep/man_f03.js"),
    Hop("f01", "e1", nhip(2, 3), "d", "b", "màn F01 · hàng chờ", ("dòng chưa ghép / chưa đủ chiều", "luôn lọc một tiền tệ"),
        doi_chieu="fls/web/tep/man_f01*.js"),
    Hop("f02", "e1", nhip(4, 5), "d", "b", "màn F02 · sổ ITL", ("lưới sổ hiệu lực", "ô nào · ai nói · lúc nào"),
        doi_chieu="fls/web/tep/man_f02.js"),
    Hop("xuat", "e1", nhip(6, 7), "d", "q", "XUẤT báo cáo daily trong CCR",
        ("output GĐ1: ghi vào sheet báo cáo daily của CCR, theo TK · pháp nhân · ngày",
         "qua ghi_o.py: neo theo khoá (⛔ ô A1 cứng) · chạy khô · cờ duyệt"),
        "bộ xuất chưa có · cơ chế ghi an toàn có (27 bài)",
        doi_chieu="fls/xuat/ghi_o.py · tools/ghi_o_that.py (FLS_CHO_GHI_SHEET=1) · owner 04/11: output = báo cáo daily trong CCR"),
]
HOP_THEO = {h.ma: h for h in HOP}


@dataclass
class Ten:
    ma: str
    tu: str
    toi: str
    tt: str                   # b · q · n
    cai_gi: str
    khoa: str
    ban_so: str
    cong: str
    co_ma: str                # ✅ · ◐ · ⛔ + chữ
    x: float | None = None    # mũi tên dọc (hình 1: chỉ là CỜ "dọc" — x thật do dat_x tính)
    nhom: str = ""
    goc: tuple[str, ...] = ()  # AS-IS: mã mũi tên gốc của artifact "Voi ITL AS-IS"


TEN: list[Ten] = [
    # 1 · nguồn sinh ra
    Ten("o1", "oPM", "soPM", "b", "PM / PC duyệt xong thì thành dòng sổ cái PM / PC", "pm_line_id · pc_line_id", "1 phiếu – n dòng",
        "FLS ⛔ không can thiệp luồng duyệt; chỉ đọc trạng thái cuối", "ngoài FLS", tam(1), "1a"),
    Ten("o3", "oKTnh", "saoke", "b", "dán sao kê vào vùng chuẩn của sheet R |", "(dòng chảy, dòng)", "1 dòng chảy – n dòng",
        "bố cục cột theo bản khai dòng 1 (68/68 sheet khai đủ)", "ngoài FLS", tam(4), "1b"),
    Ten("o4", "oKTq", "soquy", "b", "ghi thu chi quỹ", "(dòng chảy quỹ, dòng)", "1 quỹ – n dòng",
        "như o3", "ngoài FLS", tam(5), "1b"),
    Ten("o7", "oCCR", "ccr", "b", "nhập số dư cuối ngày từng TK / quỹ (Treasury)", "(TK, ngày)", "1 TK – n ngày",
        "ô số dư rỗng ⇒ ngày ấy 'chưa đo được'", "ngoài FLS", tam(6), "1b"),
    Ten("o5", "oHR", "soluong", "b", "lập file lương, tách HD · CDT1 · pháp nhân; kế toán dán số FT bank vào từng khoản", "(sổ, năm, dòng)", "1 sổ – n dòng",
        "bề rộng cột đổi ⇒ bộ đọc nổ, ⛔ không đoán", "ngoài FLS", tam(7), "1c"),
    Ten("o6", "oNT", "sont", "b", "GI · OMC xuất bảng Transactions từ Looker; SC (Luận) · PS (kế toán) cập nhật ở Google Sheets", "(loại, tháng, dòng)", "1 sổ – n dòng",
        "như o5", "ngoài FLS", tam(8), "1c"),
    # 2 · vượt ranh giới
    Ten("x1", "soPM", "anhFPS", "q", "dòng sổ cái PM: tiền · tiền tệ · Ref · khoá PE/PI · HD · CDT1 · pháp nhân trả · trạng thái; "
        "dòng sổ cái PC: tiền · khoá PM/PE gốc · trạng thái",
        "pm_line_id · pc_line_id", "1 lần chụp – n dòng",
        "bộ tiêu đề lệch hợp đồng ⇒ nổ to (như kiem_tieu_de_pm) · chụp 2 lần ⇒ 2 chup_id, ảnh cũ ⛔ không đổi · Email ⛔ không vào kho",
        "◐ PM có, đọc qua Sheets (3.772 dòng) · PC ⛔ chưa đọc", tam(1), "2a"),
    Ten("x3", "saoke", "anhTien", "b", "vùng chuẩn, 5/6 trường (⛔ không Diễn giải)", "(nguồn, dòng) + khai_version",
        "1 nguồn – n dòng", "thiếu bản khai ⇒ nổ, nêu tên sheet · 429 ⇒ lùi rồi thử lại · nguồn 0 dòng vẫn có mặt",
        "✅ 60 nguồn · 182 ảnh", tam(4), "2b"),
    Ten("x4", "soquy", "anhTien", "q", "vùng chuẩn sổ quỹ", "(nguồn, dòng)", "1 quỹ – n dòng",
        "như x3 + số dư theo ngày nếu nguồn có", "⛔ lằn Cash chưa bật (GAP-CANON-02)", tam(5), "2b"),
    Ten("x7", "ccr", "anhTien", "q", "số dư ngày từng TK / quỹ + tỷ giá tháng (dòng 6–9)", "(TK, ngày)", "1 TK – n ngày",
        "TK có giao dịch mà không có số dư ngày ⇒ 'chưa đo được', ⛔ coi là khớp", "◐ chỉ đo (do_trong_tai.py)", tam(6), "2b"),
    Ten("x5", "soluong", "anhHR", "q", "6 sổ H1000 năm (NIS/INT/COM · PIT)", "(sổ, năm, dòng)", "1 sổ – n dòng",
        "Σ Nợ/Có từng sổ phải bằng sổ nguồn", "⛔", tam(7), "2c"),
    Ten("x6", "sont", "anhNT", "q", "file chi phí 4 loại", "(loại, tháng, dòng)", "1 file – n dòng",
        "như x5", "⛔", tam(8), "2c"),
    # 3 · khai & dựng
    Ten("k1", "anhFPS", "khai", "n", "đối chiếu pháp nhân TK (lấy từ tên sheet + Mapping Master) với pháp nhân thanh toán trên sổ cái PM",
        "số TK ↔ nguồn", "1 nguồn – 1 pháp nhân",
        "khác nhau ⇒ cờ cho kế toán (tên sheet đặt sai?) · nguồn có >1 pháp nhân ⇒ ⛔ đoán (14 TK · 211 dòng)",
        "⛔ đề xuất mới", None, "3a"),
    Ten("k2", "khai", "anhTien", "b", "bố cục cột + thứ tự ngày của từng nguồn", "source_id + khai_version",
        "1 nguồn – 1 bản khai hiệu lực", "thiếu khai ⇒ nổ · khai sửa = version mới, bản cũ ⛔ không đổi",
        "✅ 408 dòng = 68 × 6", None, "3a"),
    Ten("b2", "khai", "dTien", "n", "pháp nhân TK của nguồn", "source_id", "1 nguồn – n dòng tiền",
        "nguồn chưa khai pháp nhân ⇒ dòng vào hàng chờ 'thiếu pháp nhân', ⛔ không đoán",
        "⛔ đề xuất mới", tam(3), "3a"),
    Ten("b1", "anhFPS", "dLenh", "q", "dòng sổ cái PM + PC, đủ chiều", "pm_line_id · pc_line_id", "1 – 1",
        "cột hợp đồng rỗng ⇒ cờ có tên cột, dòng vẫn vào · 13 cột còn thô phải đặt kiểu", "◐ PM 14 cột có kiểu", 410.0, "3b"),
    Ten("b3", "anhTien", "dTien", "b", "dòng lằn Bank · Cash", "chup_id + dòng", "1 – 1",
        "đọc từ ẢNH, ⛔ không đọc Sheets sống", "✅ Bank · ⛔ Cash", 911.0, "3b"),
    Ten("b4", "anhHR", "dHR", "q", "dòng lương: nhân viên · HD · CDT1 · pháp nhân · loại (NIS L1 · NIS L3 · COM L2 · INT · PIT) · Số CT", "chup_id + dòng", "1 – 1",
        "tháng trùng / thiếu ⇒ chặn (AS-IS: PIT 2025 gọi tháng 6 hai lần · NIS 2025 thiếu tháng 12)", "⛔", tam(7), "3b"),
    Ten("b5", "anhNT", "dNT", "q", "dòng lằn Platform", "chup_id + dòng", "1 – 1",
        "dòng thiếu pháp nhân ⇒ hàng chờ có tên", "⛔", tam(8), "3b"),
    # 4 · mapping, soát, ghi — tách theo nhóm
    Ten("g1", "dLenh", "ghep", "q", "mỗi PM line: tiền · tiền tệ · Reference No · chiều chi phí", "pm_line_id", "1 – 1",
        "N line một phiếu nói N giá trị ⇒ 'không suy được', ⛔ không lấy dòng đầu (INV-I16)",
        "◐ có phần PM, chưa đủ chiều", 410.0, "4a"),
    Ten("g2", "dTien", "ghep", "b", "dòng tiền canon + Reference No", "content_key", "1 dòng tiền – n PM line",
        "Σ tiền các line = tiền dòng · khác tiền tệ ⇒ để người (chờ tỷ giá, GĐ2)", "✅", 827.0, "4a"),
    Ten("g3", "dHR", "ghep2", "q", "dòng lương + Số CT (số FT) của giao dịch đã chi", "Số CT", "n dòng lương – 1 giao dịch bank",
        "Số CT không thấy giao dịch ⇒ hàng chờ 'đợt chưa thấy tiền'", "⛔", 1310.0, "4a"),
    Ten("g4", "dNT", "ghep3", "q", "chi phí nền tảng 4 loại + Combine Code (Vendor-Date-NoTrans)", "(vendor, ngày, NoTrans)", "n – 1 PE/PM",
        "Combine Code trúng 0 hoặc ≥ 2 PE ⇒ hàng chờ · loại lạ ⇒ chặn", "⛔", tam(8), "4a"),
    Ten("q1", "ghep", "ghep2", "q", "giao dịch bank còn ở lớp L3 sau PP (1)", "content_key", "—",
        "chỉ chuyển dòng chưa khớp; dòng đã khớp ⛔ thử lại ở nhóm sau", "⛔", None, "4b"),
    Ten("q2", "ghep2", "ghep3", "q", "giao dịch bank còn lại sau PP (2)", "content_key", "—",
        "còn lại sau PP (3) ⇒ ở L3, vào vòng cộng dồn §1b", "⛔", None, "4b"),
    Ten("w1", "ghep", "soat", "b", "mối nối dự kiến + dòng tiền canon", "(content_key, pm_line_id)", "1 – n",
        "9 luật soát chạy theo TỪNG nguồn (⛔ nối phẳng 60 nguồn)", "✅", 410.0, "4c"),
    Ten("w2", "ghep2", "soat2", "q", "dòng lương đã nối Số CT", "(Số CT, dòng)", "1 – n",
        "Σ Có = Σ Nợ mỗi đợt (CHECK BALANCE như AS-IS)", "⛔", 1310.0, "4c"),
    Ten("w3", "ghep3", "soat3", "q", "chi phí ↔ PE/PM ↔ giao dịch bank + phần chia CDT1", "(content_key, CDT1)", "1 – n",
        "Σ phần chia = tiền giao dịch", "⛔", tam(8), "4c"),
    Ten("r1", "soat", "ghiNap", "b", "dòng đạt + dòng loại + cờ + mối nối", "content_key", "1 – 1",
        "CHẶN ⇒ 0 dòng của nguồn ấy · 4 vế không cân ⇒ ⛔ không ghi gì", "✅", 827.0, "4d"),
    Ten("r2", "soat2", "ghiNap", "q", "dòng lương đạt soát (HD · CDT1 · pháp nhân)", "(Số CT, dòng)", "—",
        "đợt lệch ⇒ ⛔ ghi, vào hàng chờ", "⛔", 1310.0, "4d"),
    Ten("r3", "soat3", "ghiNap", "q", "phần chia CDT1 đạt soát", "(content_key, CDT1)", "—",
        "lệch Σ ⇒ ⛔ ghi cả giao dịch ấy", "⛔", tam(8), "4d"),
    Ten("s1", "ghiNap", "loai", "b", "dòng bị loại + lý do", "run_id + dòng nguồn", "1 – 1",
        "mỗi dòng loại có lý do có tên", "✅", tam(1), "4e"),
    Ten("s2", "ghiNap", "soITL", "b", "dòng sổ: General Trustest + TK + pháp nhân + run_id", "content_key UNIQUE", "1 – 1",
        "trùng ⇒ ⛔ không ghi, đếm vế 'trùng' · nạp lại cùng ảnh ⇒ vào sổ = 0", "✅ (pháp nhân còn rỗng)", 577.0, "4e"),
    Ten("s3", "ghiNap", "lopSua", "b", "mối nối máy · dòng lương nối Số CT · phần chia CDT1 · gợi ý (nguồn = máy)", "itl_id", "1 – n",
        "máy gợi ý ⛔ không đè lên ô người đã chốt", "◐ phần PP (1)", 827.0, "4e"),
    Ten("s4", "ghiTay", "lopSua", "b", "ghép · bỏ ghép · sửa · đảo · lý do · xong/mở lại", "itl_id", "1 – n",
        "bút toán + nhật ký trong MỘT giao dịch · actor từ thẻ, gửi trong thân ⇒ 400", "✅", None, "4e"),
    # 5 · hiệu lực & ra ngoài
    Ten("h1", "loai", "kiem", "q", "số dòng loại theo lý do", "run_id", "—",
        "vế 'loại' của 4 vế", "◐ cổng 4 vế có ở lúc nạp", tam(1), "5a"),
    Ten("h2", "soITL", "hieuLuc", "b", "dòng sổ gốc", "itl_id", "1 – 1",
        "sổ gốc ⛔ không đổi; giá trị hiệu lực đọc qua view", "✅", 577.0, "5a"),
    Ten("h3", "lopSua", "hieuLuc", "b", "giá trị người / máy gợi ý · mối nối · trạng thái hàng chờ", "itl_id",
        "n – 1", "người › máy gợi ý › nguồn; bỏ nối ⇒ giá trị máy rút theo", "✅", 1078.0, "5a"),
    Ten("h4", "hieuLuc", "kiem", "q", "sổ hiệu lực cho 5 cổng GĐ1", "le · source_system · curr", "—",
        "pháp nhân rỗng = 0 · Σ theo pháp nhân = Σ theo nguồn · 0 khoá lệnh chi trỏ rỗng", "⛔", None, "5a"),
    Ten("v1", "kiem", "f03", "q", "kết quả cổng: đạt / không đạt / chưa đo được", "mã cổng", "—",
        "phép ⛔ đo được là ĐỎ, ⛔ không phải 'không thấy lệch'", "◐ 8 cổng cũ", 320.0, "5b"),
    Ten("v2", "hieuLuc", "f01", "b", "dòng chưa ghép / chưa đủ chiều + lý do", "itl_id", "—",
        "luôn lọc một tiền tệ, ⛔ không có dòng tổng", "✅", 577.0, "5b"),
    Ten("v3", "hieuLuc", "f02", "b", "lưới sổ hiệu lực + ngăn kéo 'nguồn nói · người nói'", "itl_id", "—",
        "ô máy gợi ý hiện là gợi ý, ⛔ không trông như số chốt", "✅", 911.0, "5b"),
    Ten("v4", "hieuLuc", "xuat", "q", "sổ hiệu lực gom theo TK · pháp nhân · ngày → báo cáo daily CCR", "(TK, ngày)", "n – 1 ô",
        "chênh liệt kê TỪNG dòng, mọi chênh có tên lý do, ⛔ không phần trăm", "⛔ bộ xuất chưa có", 1330.0, "5b"),
]


def dat_x(tens: list, ht: dict) -> None:
    """v0.4: x của mũi tên dọc = GIỮA phần hai hộp chồng nhau — đổi nhịp hộp thì mũi tên tự theo,
    ⛔ còn tọa độ gõ tay nào để lệch. Không chồng nhau ⇒ x rơi ngoài hộp ⇒ kiem() nổ."""
    for t in tens:
        if t.x is not None:
            a, b = ht[t.tu], ht[t.toi]
            t.x = (max(a.x[0], b.x[0]) + min(a.x[1], b.x[1])) / 2


dat_x(TEN, HOP_THEO)

NHOM = {
    "1": "Nhóm 1 · Nguồn sinh ra (o1 · o3–o7)", "1a": "FPS (o1)", "1b": "Phương pháp (1) · mapping với bank transaction — sao kê · sổ quỹ · CCR (o3 · o4 · o7)",
    "1c": "Phương pháp (2) · HR và (3) · nền tảng (o5 · o6)",
    "2": "Nhóm 2 · Vượt ranh giới vào FLS (x1 · x3–x7)", "2a": "FPS → FLS · đọc sổ cái PM · PC chỉ-đọc (x1)",
    "2b": "Phương pháp (1) · Sheets API, tài khoản dịch vụ chỉ-đọc (x3 · x4 · x7)",
    "2c": "Phương pháp (2) và (3) · Sheets API, tài khoản dịch vụ chỉ-đọc (x5 · x6)",
    "3": "Nhóm 3 · Khai và dựng (k1–k2 · b1–b5)", "3a": "Bản khai nguồn và pháp nhân TK (k1 · k2 · b2)",
    "3b": "Đọc ảnh thành dòng (b1 · b3 · b4 · b5)",
    "4": "Nhóm 4 · Mapping, soát, ghi — theo nhóm (g · q · w · r · s)", "4a": "Vào mapping từng nhóm (g1–g4)",
    "4b": "Chuyển phần chưa khớp sang nhóm kế (q1 · q2)", "4c": "Mapping → soát, từng nhóm (w1–w3)",
    "4d": "Soát → ghi (r1–r3)", "4e": "Vào sổ (s1–s4)",
    "5": "Nhóm 5 · Hiệu lực và ra ngoài (h1–h4 · v1–v4)", "5a": "Sổ hiệu lực và cổng (h1–h4)",
    "5b": "Người thấy và hệ khác (v1–v4)",
}


# ═════════════════ HÌNH PHÓNG TO · MAPPING PP (1) — ba lớp giao dịch + vòng cộng dồn ═════════════════
# Owner 04/11 (bình luận trên hình): cần luật xác định ① giao dịch có trên FPS mà chưa có trên bank txns,
# ② có trên bank txns mà không có trên FPS, ③ cơ chế vòng cộng dồn tự suy diễn: TK + nội dung + loại bank
# → loại giao dịch. ⛔ Máy chỉ GỢI Ý; luật do người ký (INV-I16 · QĐ-ITL-56/58 — máy ⛔ tự đặt quy định).
WM, HM = 1220, 600
# khe 40 giữa cột 2|3 và 4|5 — chỗ các mũi tên ngang chạy qua, đủ chỗ cho nhãn mũi tên
_XM = (130, 302, 502, 674, 874, 1046)


def cotm(a: int, b: int | None = None) -> tuple[int, int]:
    b = b or a
    return _XM[a - 1], _XM[b - 1] + 160


def tamm(a: int, b: int | None = None) -> float:
    x0, x1 = cotm(a, b)
    return (x0 + x1) / 2


DAI_M = {
    "m1": ("M", 16, 84, "① VÀO"),
    "m2": ("M", 136, 84, "② MAPPING"),
    "m3": ("M", 256, 84, "③ BA LỚP"),
    "m4": ("M", 376, 84, "④ SUY DIỄN"),
    "m5": ("M", 496, 84, "⑤ XÁC NHẬN"),
}
TANG_M = {"m1": 0, "m2": 1, "m3": 2, "m4": 3, "m5": 4}

HOP_M: list[Hop] = [
    Hop("mPM", "m1", cotm(1), "d", "q", "dòng sổ cái PM",
        ("Ref · tiền · tiền tệ", "pháp nhân trả · vendor"),
        "đã DỰNG (b1)", doi_chieu="fls_pm_line 3.772 dòng (14 cột có kiểu) · hôm nay qua Sheets"),
    Hop("mHR", "m1", cotm(2), "d", "q", "đợt lương · BH",
        ("PP (2): dòng lương H1000", "Số CT · HD · CDT1 · pháp nhân"),
        "đã DỰNG (b4)", doi_chieu="owner 04/11: GĐ1 → LE, GĐ2 → KRF"),
    Hop("mBank", "m1", cotm(3, 4), "d", "b", "bank transactions",
        ("dòng tiền đã DỰNG (b3)", "TK · ngày · Nợ/Có · Ref · nội dung"),
        "nội dung: chưa đọc (QĐ-ITL-92)", doi_chieu="fls_itl 8.387 · memo rỗng 8.387/8.387"),
    Hop("mLuatGhep", "m1", cotm(5, 6), "d", "q", "luật ghép đã ký",
        ("VN: Ref + tiền + pháp nhân · ngoài: từ khoá + vendor + tiền",
         "lương / BH: Số CT (số FT kế toán dán) = Reference number"),
        "QĐ-ITL-144 · máy mới dùng Ref + tiền", doi_chieu="QĐ-ITL-144 (owner + kế toán 18/09)"),
    Hop("mMap", "m2", cotm(1, 5), "p", "b", "MAPPING bank txns ↔ lệnh chi",
        ("chạy luật ghép theo thứ tự; Σ tiền các PM line = tiền giao dịch, lệch ⇒ chặn",
         "khác tiền tệ · N×M ⇒ để người, ⛔ không đoán, ⛔ không chia bừa"),
        "fls/adapters/pm_join.py · fls/repo/may_ghep.py", doi_chieu="pm_join.py hình A–F · INV-I16"),
    Hop("mBB", "m2", cotm(6), "d", "q", "biên bản mapping",
        ("đếm 3 lớp", "+ lý do có tên"), "mỗi lượt nạp", doi_chieu="hôm nay: /queue/coverage · /queue/mau-so"),
    Hop("mL1", "m3", cotm(1, 2), "d", "b", "L1 · khớp",
        ("Ref chung + Σ khớp, hoặc Số CT của dòng lương", "→ mối nối (s3)"),
        "hôm nay 2.263 mối nối", doi_chieu="fls_pm_link"),
    Hop("mL2", "m3", cotm(3, 4), "d", "b", "L2 · có trên FPS, chưa có bank",
        ("PM đã duyệt, chưa thấy tiền ở TK chi", "tuổi > N ngày ⇒ cờ 'lệnh chưa thấy tiền'"),
        "hôm nay 1.345 dòng · 698 phiếu", doi_chieu="fls/repo/lenh_cho.py · màn F01 lằn lệnh"),
    Hop("mL3", "m3", cotm(5, 6), "d", "b", "L3 · có bank, không có FPS",
        ("không Ref, hoặc Ref không PM nào mang", "trạng thái vẫn UNMAPPED (QĐ-ITL-58)"),
        "89,7% dòng chưa ghép: có mã, không PM", doi_chieu="13_LO_TRINH §0 ⓶ (6.577 dòng)"),
    Hop("mKy", "m4", cotm(1, 2), "o", "n", "S6 · OWNER KÝ LUẬT", ("luật ứng viên → luật hiệu lực",),
        doi_chieu="đề xuất · người ký, máy ⛔ tự đặt quy định (QĐ-ITL-56)"),
    Hop("mLuat", "m4", cotm(3, 4), "d", "n", "bảng luật suy diễn",
        ("(TK + mẫu nội dung + loại bank)", "→ loại giao dịch · có version"),
        "seed: 5 loại hay sót", doi_chieu="đề xuất · seed từ 'Check list mapping' (lãi/phí NH, điều chuyển nội bộ…)"),
    Hop("mSuy", "m4", cotm(5, 6), "p", "n", "SUY DIỄN loại giao dịch",
        ("áp luật hiệu lực cho dòng L3", "ra gợi ý, ⛔ không tự chốt"),
        "INV-I16", doi_chieu="đề xuất"),
    Hop("mKT", "m5", cotm(1, 2), "o", "b", "S5 · KẾ TOÁN XÁC NHẬN", ("giữ hoặc sửa gợi ý · F01",),
        doi_chieu="POST adjust / match (ghi_tay.py)"),
    Hop("mXN", "m5", cotm(3, 4), "p", "n", "GOM bằng chứng luật",
        ("mỗi xác nhận +1 cho khoá luật", "≥k lần đồng ý, 0 lần khác ⇒ luật ứng viên"),
        "một lần sửa ngược ⇒ luật về 'xem lại'", doi_chieu="đề xuất"),
    Hop("mGoiY", "m5", cotm(5, 6), "d", "n", "gợi ý loại giao dịch",
        ("nguồn = máy gợi ý (lớp sửa)", "hiện ở F01 cạnh dòng L3"),
        "đo: độ phủ L3 · tỉ lệ giữ nguyên", doi_chieu="đề xuất · cùng cơ chế fls_may_goi_y"),
]
HOP_M_THEO = {h.ma: h for h in HOP_M}

TEN_M: list[Ten] = [
    Ten("m1", "mPM", "mMap", "q", "PM line: Ref · tiền · tiền tệ · pháp nhân trả · vendor", "pm_line_id", "1 – 1",
        "chỉ dòng trạng thái cuối đã duyệt", "◐ có, chưa có pháp nhân/vendor có kiểu", tamm(1)),
    Ten("m15", "mHR", "mMap", "q", "dòng lương H1000 + Số CT (số FT kế toán dán)", "Số CT", "n dòng lương – 1 giao dịch",
        "Σ dòng lương của một giao dịch = tiền giao dịch; lệch ⇒ hàng chờ", "⛔ chưa có", tamm(2)),
    Ten("m2", "mBank", "mMap", "b", "giao dịch: TK · ngày · tiền · tiền tệ · Ref", "content_key", "1 – 1",
        "đọc từ ảnh, ⛔ Sheets sống", "✅", tamm(3, 4)),
    Ten("m3", "mLuatGhep", "mMap", "q", "thứ tự nhánh: VN (Ref + tiền + pháp nhân) → nước ngoài (từ khoá + vendor + tiền)",
        "version luật", "1 bộ luật / lượt", "luật đổi ⇒ version mới, lượt cũ giữ version đã dùng",
        "◐ máy mới dùng Ref + tiền, chưa dùng pháp nhân", tamm(5)),
    Ten("m4", "mMap", "mBB", "q", "số dòng mỗi lớp + lý do", "run_id", "1 / lượt",
        "L1 + L1b + L2 + L3 = mẫu số, đếm trước (Đ3)", "◐ có /queue/mau-so", None),
    Ten("m5", "mMap", "mL1", "b", "cặp (giao dịch, PM line, tiền chia)", "itl_id + pm_line_id", "1 – n",
        "Σ tiền chia = tiền giao dịch · cùng tiền tệ", "✅", tamm(1, 2)),
    Ten("m6", "mMap", "mL2", "b", "PM line đã duyệt không giao dịch nào mang Ref của nó", "pm_line_id", "—",
        "chỉ so với ảnh sao kê của TK chi tới ảnh mới nhất · tuổi > N ngày ⇒ cờ", "✅ 1.345 dòng", tamm(3, 4)),
    Ten("m7", "mMap", "mL3", "b", "giao dịch không Ref, hoặc Ref không PM nào mang", "content_key", "—",
        "⛔ không gán nhãn 'không cần lệnh chi' (QĐ-ITL-56/58)", "✅ hàng chờ UNMAPPED", tamm(5)),
    Ten("m8", "mL3", "mSuy", "n", "dòng L3: TK · mẫu nội dung · loại bank · chiều Nợ/Có", "content_key", "1 – 1",
        "thiếu nội dung ⇒ ⛔ suy diễn, chỉ báo 'thiếu nội dung'", "⛔ chờ nới QĐ-ITL-92", 1120.0),
    Ten("m9", "mLuat", "mSuy", "n", "luật hiệu lực", "(TK, mẫu nội dung, loại bank)", "1 khoá – 1 loại GD",
        "khoá khớp ≥2 luật nói khác nhau ⇒ ⛔ gợi ý", "⛔ đề xuất", None),
    Ten("m10", "mKy", "mLuat", "n", "chữ ký trên luật ứng viên", "luật + version", "1 – 1",
        "luật chỉ hiệu lực khi có người ký (signed_by, signed_at)", "⛔ đề xuất", None),
    Ten("m11", "mSuy", "mGoiY", "n", "loại giao dịch gợi ý + luật đã dùng", "itl_id", "1 – 1",
        "gợi ý ⛔ đè ô người đã chốt", "⛔ đề xuất", 1120.0),
    Ten("m12", "mGoiY", "mXN", "n", "gợi ý đã được người giữ hoặc sửa", "itl_id", "1 – 1",
        "chỉ đếm xác nhận của NGƯỜI (actor từ thẻ), ⛔ máy tự xác nhận", "⛔ đề xuất", None),
    Ten("m13", "mKT", "mXN", "b", "cú bấm giữ / sửa loại giao dịch", "itl_id", "1 – 1",
        "ghi lớp sửa trong một giao dịch (ghi_tay.py)", "✅ cửa ghi có", None),
    Ten("m14", "mXN", "mLuat", "n", "luật ứng viên: khoá + loại GD + số bằng chứng", "(TK, mẫu nội dung, loại bank)", "1 – 1",
        "VÒNG CỘNG DỒN: càng nhiều xác nhận, càng nhiều dòng L3 có gợi ý ở lượt sau", "⛔ đề xuất", tamm(3, 4)),
]


def kiem_m() -> list[str]:
    return (kiem_phong(HOP_M, TEN_M, HOP_M_THEO, DAI_M, TANG_M)
            + kiem_phong(HOP_N, TEN_N, HOP_N_THEO, DAI_N, TANG_N))


def kiem_phong(hops, tens, ht, dai, tang) -> list[str]:
    loi: list[str] = []
    for d in dai:
        n = sum(1 for h in hops if h.dai == d)
        if not 2 <= n <= 5:
            loi.append(f"hình phóng to · dải {d}: {n} hộp")
    for t in tens:
        a, b = ht[t.tu], ht[t.toi]
        x1, y1, x2, y2 = doan(t, ht)
        if t.x is not None:
            if not (a.x[0] + 6 <= t.x <= a.x[1] - 6 and b.x[0] + 6 <= t.x <= b.x[1] - 6):
                loi.append(f"{t.ma}: x={t.x} ngoài hộp {a.ma}/{b.ma}")
            if abs(tang[b.dai] - tang[a.dai]) != 1:
                loi.append(f"{t.ma}: ⛔ không kề nhau")
        elif a.dai != b.dai:
            loi.append(f"{t.ma}: ngang mà khác dải")
        for h in hops:
            if h.ma in (t.tu, t.toi):
                continue
            if cat_hop(x1, min(y1, y2) + 0.5, x2, max(y1, y2) - 0.5, h) and cat_hop(min(x1, x2) + 0.5, y1, max(x1, x2) - 0.5, y2, h):
                loi.append(f"{t.ma} cắt qua hộp {h.ma}")
    return loi


# ═════════════════ HÌNH PHÓNG TO · PP (3) — 4 chi phí nền tảng ═════════════════
# Owner 04/11: OMC · GI · SC · PS ⛔ có trên FPS ⇒ xuất file từ data Looker → mapping với bank txns
# ⚠ SỬA 06/11 (KhanhCQ): chi phí nền tảng CÓ PE/PM (AS-IS [oALL]: Combine Code Vendor-Date-NoTrans) — kết quả
#   phải tới được bank txns; chia theo CDT1 (AS-IS). SC = server cost.
# (4 loại, 4 luật khác nhau) → allocate về các ventures. Luật cụ thể do owner điền — trang ⛔ tự bịa.
WN, HN = 1300, 600


def cotn(a: int, b: int | None = None) -> tuple[int, int]:
    b = b or a
    return 130 + (a - 1) * 200, 130 + (b - 1) * 200 + 160


def tamn(a: int, b: int | None = None) -> float:
    x0, x1 = cotn(a, b)
    return (x0 + x1) / 2


DAI_N = {
    "n1": ("N", 16, 84, "① VÀO"),
    "n2": ("N", 136, 84, "② MAPPING"),
    "n3": ("N", 256, 84, "③ KẾT QUẢ"),
    "n4": ("N", 376, 84, "④ ALLOCATE"),
    "n5": ("N", 496, 84, "⑤ RA"),
}
TANG_N = {"n1": 0, "n2": 1, "n3": 2, "n4": 3, "n5": 4}

HOP_N: list[Hop] = [
    Hop("nFile", "n1", cotn(1, 3), "x", "b", "4 sổ Platform Data Ledger (đã chụp, b5)",
        ("GI · OMC: Looker · SC · PS: Google Sheets — mỗi dòng: vendor · ngày · NoTrans · tiền",
         "có PE/PM trên FPS ⇒ nối qua Combine Code (Vendor-Date-NoTrans)"), "4 loại · 4 luật", doi_chieu="owner 04/11"),
    Hop("nBank", "n1", cotn(4, 5), "d", "b", "bank txns chưa ghép (L3)",
        ("giao dịch không có trên FPS (§1b)", "TK · ngày · tiền · tiền tệ · nội dung"),
        "nội dung: chờ nới QĐ-ITL-92", doi_chieu="hàng chờ UNMAPPED"),
    Hop("nLuat", "n1", cotn(6), "d", "n", "4 luật mapping",
        ("1 luật / loại", "người ký"), "owner điền", doi_chieu="chờ owner — xem bảng §1c"),
    Hop("nTach", "n2", cotn(1), "p", "n", "TÁCH tỉ lệ CDT1",
        ("Mapping Block 1", "Vendor ↔ Network-Acc ↔ CDT1"), "mỗi loại · tháng", doi_chieu="PD Now 503–507 (CFA1 → CFA2 MID 1–3)"),
    Hop("nMap", "n2", cotn(2, 6), "p", "n", "MAPPING chi phí ↔ PE/PM ↔ bank txns",
        ("Combine Code → PE/PM line → Reference No → giao dịch bank; khớp kỳ · khớp Σ tiền",
         "lệch ⇒ chặn, ⛔ chia bừa · giao dịch khớp ≥ 2 loại ⇒ để người"), "đi qua PE/PM (owner 06/11)", doi_chieu="đề xuất"),
    Hop("nTyLe", "n3", cotn(1), "d", "n", "tỉ lệ CDT1",
        ("loại · tháng ·", "CDT1 · %"), "Σ % = 100", doi_chieu="đề xuất"),
    Hop("nKhop", "n3", cotn(2, 3), "d", "n", "khớp",
        ("giao dịch ↔ chi phí kỳ của một loại", "→ mối nối"), "Σ chi phí kỳ = Σ giao dịch", doi_chieu="đề xuất"),
    Hop("nCho", "n3", cotn(4, 5), "d", "n", "có trên sổ nguồn, chưa có tiền",
        ("chi phí kỳ chưa thấy giao dịch", "tuổi > N ngày ⇒ cờ"), "giống L2 của §1b", doi_chieu="đề xuất"),
    Hop("nCon", "n3", cotn(6), "d", "n", "tiền chưa khớp",
        ("ở lại L3, vào", "vòng cộng dồn §1b"), "UNMAPPED", doi_chieu="đề xuất"),
    Hop("nAlloc", "n4", cotn(1, 3), "p", "n", "ALLOCATE về các CDT1s",
        ("chia tiền giao dịch đã khớp theo tỉ lệ CDT1 của đúng loại · tháng",
         "phần lẻ làm tròn dồn vào một CDT1 có tên, ⛔ mất xu"), "Σ phần chia = tiền giao dịch", doi_chieu="đề xuất"),
    Hop("nBB", "n4", cotn(4, 6), "d", "n", "biên bản PP (3)",
        ("đếm theo loại: khớp · chờ tiền · tiền chưa khớp", "+ lý do có tên"), "mỗi lượt", doi_chieu="đề xuất"),
    Hop("nRa", "n5", cotn(1, 3), "d", "n", "dòng phân bổ theo CDT1",
        ("CDT1 · LE · loại · tháng · tiền · giao dịch gốc", "→ lớp sửa (chỉ-thêm) → sổ hiệu lực"), "giao dịch gốc ⛔ đổi một ô",
        doi_chieu="đề xuất"),
    Hop("nKiem", "n5", cotn(4, 5), "p", "n", "KIỂM Σ phân bổ",
        ("Σ phần chia = tiền giao dịch,", "từng giao dịch · từng tiền tệ"), "lệch ⇒ chặn cả lượt", doi_chieu="đề xuất"),
]
HOP_N_THEO = {h.ma: h for h in HOP_N}

TEN_N: list[Ten] = [
    Ten("n1", "nFile", "nTach", "n", "dòng chi phí có cột CDT1", "(loại, tháng, CDT1)", "n – 1",
        "CDT1 rỗng ⇒ hàng chờ có tên", "⛔ đề xuất", tamn(1)),
    Ten("n2", "nFile", "nMap", "q", "chi phí theo loại · vendor · tháng", "(loại, vendor, tháng)", "n – 1 kỳ",
        "loại lạ ⇒ chặn, nêu tên loại", "⛔", tamn(2, 3)),
    Ten("n3", "nBank", "nMap", "b", "giao dịch chưa ghép: TK · ngày · tiền · nội dung", "content_key", "1 – 1",
        "đọc từ ảnh, ⛔ Sheets sống", "✅ hàng chờ có", tamn(4, 5)),
    Ten("n4", "nLuat", "nMap", "n", "luật của từng loại", "loại + version", "4 luật",
        "luật chưa ký ⇒ loại ấy ⛔ chạy", "⛔ chờ owner", tamn(6)),
    Ten("n5", "nTach", "nTyLe", "n", "tỉ lệ % theo CDT1", "(loại, tháng, CDT1)", "1 – n",
        "Σ % mỗi loại · tháng = 100, lệch ⇒ chặn", "⛔", tamn(1)),
    Ten("n6", "nMap", "nKhop", "n", "cặp (giao dịch, chi phí kỳ, loại)", "(content_key, loại, tháng)", "n – m",
        "Σ chi phí kỳ = Σ giao dịch của loại", "⛔", tamn(2, 3)),
    Ten("n7", "nMap", "nCho", "n", "chi phí kỳ không giao dịch nào khớp", "(loại, tháng)", "—",
        "chỉ so với ảnh sao kê của TK chi tới ảnh mới nhất", "⛔", tamn(4, 5)),
    Ten("n8", "nMap", "nCon", "n", "giao dịch không khớp loại nào", "content_key", "—",
        "vẫn UNMAPPED, ⛔ tự gán loại", "⛔", tamn(6)),
    Ten("n9", "nTyLe", "nAlloc", "n", "tỉ lệ CDT1 của đúng loại · tháng", "(loại, tháng)", "1 – n",
        "thiếu tỉ lệ ⇒ ⛔ chia, vào hàng chờ", "⛔", tamn(1)),
    Ten("n10", "nKhop", "nAlloc", "n", "giao dịch đã khớp + loại + tháng", "content_key", "1 – n phần",
        "chỉ chia giao dịch đã khớp", "⛔", tamn(2, 3)),
    Ten("n11", "nCho", "nBB", "n", "số chi phí chờ tiền theo loại", "(loại, tháng)", "—", "in mẫu số", "⛔", tamn(4, 5)),
    Ten("n12", "nCon", "nBB", "n", "số giao dịch chưa khớp", "content_key", "—", "in mẫu số", "⛔", tamn(6)),
    Ten("n13", "nAlloc", "nRa", "n", "phần chia theo CDT1", "(content_key, CDT1)", "1 – n",
        "ghi chỉ-thêm, giao dịch gốc giữ nguyên", "⛔", tamn(2)),
    Ten("n14", "nRa", "nKiem", "n", "các phần chia của từng giao dịch", "content_key", "n – 1",
        "Σ phần = tiền giao dịch", "⛔", None),
]


# ═════════════════ LUỒNG XỬ LÝ TỔNG QUAN — mỗi hộp ≤ 5 bước (owner 05/11) ═════════════════
# Hiện ở: khung chi tiết khi bấm hộp · chú thích khi rê chuột · bảng §1d. Luật vẽ voi: ≤ 5 bước.
LUONG: dict[str, tuple[str, ...]] = {
    # ── c1 · KHAI & CHỤP
    "anhFPS": ("Nhịp S1 mở kết nối chỉ-đọc vào sổ cái PM / PC (hôm nay: tab PM đọc qua Sheets)",
               "Kiểm bộ tiêu đề theo hợp đồng cột; lệch ⇒ nổ, nêu tên cột",
               "Bỏ cột riêng tư (email người lập) trước khi lưu",
               "Ghi một ảnh mới có chup_id; ảnh cũ không đổi một ô",
               "Báo số dòng và tuổi ảnh cho bước dựng"),
    "khai": ("Kế toán mở F04, chọn nguồn (S2)",
             "FLS đọc dòng 1 của sheet: vị trí 6 trường chuẩn, đo thứ tự ngày dmy / mdy",
             "Máy đề xuất pháp nhân TK từ TK chi + pháp nhân thanh toán trên sổ cái PM (k1)",
             "Kế toán khai, owner ký pháp nhân",
             "Ghi bản khai version mới; bản cũ giữ nguyên"),
    "anhTien": ("Nhịp S1 lấy bản khai hiệu lực của từng nguồn",
                "Đọc vùng chuẩn 60 sheet sao kê, 8 dòng chảy quỹ, 2 sheet CCR qua Sheets API chỉ-đọc",
                "Chỉ lấy cột đã khai, không đọc Diễn giải",
                "Ghi ảnh có chup_id + khai_version từng nguồn; nguồn 0 dòng vẫn có mặt",
                "Dọn ảnh không ai dùng sau 30 ngày; ảnh đã nạp giữ vĩnh viễn"),
    "anhHR": ("Nhịp chụp sổ lương HR",
              "Kiểm bề rộng cột theo hợp đồng; lệch ⇒ nổ",
              "Ghi ảnh theo sổ · năm, có chup_id"),
    "anhNT": ("Data xuất GI · OMC từ Looker; Luận / kế toán cập nhật SC / PS ở Google Sheets",
              "Nhịp chụp file vào kho",
              "Kiểm 4 loại OMC · GI · SC · PS; loại lạ ⇒ chặn",
              "Ghi ảnh có chup_id"),
    # ── c2 · DỰNG
    "dLenh": ("Đọc ảnh sổ cái PM / PC mới nhất",
              "Đặt kiểu từng cột theo hợp đồng (14 cột có kiểu, 13 cột còn thô phải đặt)",
              "Mỗi PM / PC line → bản ghi lệnh: Ref · tiền · tiền tệ · HD/KRF · CDT1 · đối tác · kỳ DV · pháp nhân trả",
              "Cột hợp đồng rỗng ⇒ cờ có tên cột, dòng vẫn đi tiếp",
              "Chuyển sang MAPPING PP (1)"),
    "dTien": ("Đọc ảnh lằn Bank · Cash · CCR",
              "Mỗi dòng sao kê / quỹ → canon 36 trường, giữ cả PS Nợ và PS Có",
              "Đọc ngày theo thứ tự đã khai; gắn pháp nhân TK từ bản khai nguồn",
              "Tính content_key chống trùng",
              "Lằn CCR → bảng số dư đầu kỳ và số dư từng ngày của từng TK / quỹ"),
    "dHR": ("Đọc ảnh 6 sổ H1000",
            "Mỗi dòng nhân viên → dòng lương: HD · CDT1 · pháp nhân · loại",
            "Lấy Số CT bank từ dòng đảo (số FT kế toán đã dán)",
            "Kiểm đủ tháng, không tháng trùng",
            "Chuyển sang MAPPING PP (2)"),
    "dNT": ("Đọc ảnh 4 sổ Platform Data Ledger (Looker · Gsheet)",
            "Tách 4 loại OMC · GI · SC · PS",
            "Mỗi loại → chi phí theo vendor · CDT1 · tháng",
            "Dựng Combine Code Vendor-Date-NoTrans",
            "Chuyển sang MAPPING PP (3)"),
    # ── c3 · MAPPING
    "ghep": ("Nhận dòng tiền (cả hai vế) và dòng lệnh",
             "Vế Có (tiền ra): so Reference No với PM line; Σ tiền các line = tiền dòng",
             "Vế Nợ (tiền vào): luật vế Nợ — nội bộ, doanh thu, hoàn tiền, vay và lãi",
             "Xếp lớp L1 khớp · L1b khớp mã lệch · L2 FPS có, bank chưa · L3 bank có, FPS không",
             "Chuyển L3 sang MAPPING PP (2) (q1)"),
    "ghep2": ("Nhận dòng lương (có Số CT) và giao dịch L3 từ PP (1)",
              "Nối theo Số CT = Reference number của giao dịch bank",
              "Một giao dịch – n dòng lương; Σ dòng = tiền giao dịch",
              "Không thấy giao dịch ⇒ hàng chờ 'đợt chưa thấy tiền'",
              "Còn lại chuyển sang MAPPING PP (3) (q2)"),
    "ghep3": ("Nhận chi phí 4 loại và giao dịch còn lại",
              "Combine Code → PE/PM line trên FPS",
              "Reference No của PM → giao dịch bank",
              "Chia tiền giao dịch theo CDT1 (% CDT1 × tháng)",
              "Trúng 0 hoặc ≥ 2 PE ⇒ hàng chờ; chuyển sang SOÁT PP (3)"),
    # ── c4 · SOÁT
    "soat": ("Chạy 9 luật trên TỪNG nguồn",
             "CHẶN ⇒ chừa nguồn ấy; CỜ ⇒ vẫn ghi, vào hàng chờ có lý do",
             "Kiểm Σ PM line = tiền dòng và 4 vế: vào = sổ + loại + rỗng + trùng",
             "Kiểm số dư đầu + Σ PS Nợ − Σ PS Có theo ngày = số dư CCR / CCR Cash (DIF = 0)",
             "In biên bản 9 dòng trên F04"),
    "soat2": ("Kiểm Σ Có = Σ Nợ mỗi đợt (CHECK BALANCE như AS-IS)",
              "Kiểm đủ tháng mỗi sổ, không tháng trùng",
              "Lệch ⇒ không ghi đợt ấy, vào hàng chờ"),
    "soat3": ("Kiểm Σ phần chia = tiền giao dịch",
              "Kiểm Σ % CDT1 = 100 mỗi loại · tháng",
              "Lệch ⇒ không ghi giao dịch ấy"),
    # ── c5 · GHI
    "ghiNap": ("Kế toán bấm Nhận lô trên F04 (S4)",
               "Mở MỘT giao dịch cơ sở dữ liệu",
               "Ghi run, dòng sổ (bỏ qua dòng trùng content_key), dòng loại",
               "Ghi mối nối (PP 1), dòng lương nối Số CT (PP 2), phần chia CDT1 (PP 3), gợi ý của máy",
               "Kiểm 4 vế cân; lỗi giữa chừng ⇒ huỷ cả lượt"),
    # ── d1 · SỔ GỐC
    "loai": ("Mỗi dòng không vào sổ được một lý do có tên",
             "Được đếm vào vế 'loại' của 4 vế"),
    "soITL": ("Nhận dòng từ GHI lượt nạp",
              "content_key UNIQUE chặn dòng trùng",
              "Chỉ-thêm (INV-I08): không cửa sửa, không cửa xoá",
              "Mỗi dòng mang run_id, nguồn và pháp nhân TK"),
    "lopSua": ("Nhận mối nối / bút toán của máy (s3) và của người (s4)",
               "Mỗi thay đổi là một dòng mới; bỏ nối là thêm dòng bỏ nối",
               "Giá trị hiệu lực: người › máy gợi ý › nguồn",
               "Nhật ký ghi ai · lúc nào · giá trị cũ → mới"),
    "ghiTay": ("Kế toán ghép / sửa / đảo trên F01 · F02 (S5)",
               "Actor lấy từ thẻ đăng nhập; gửi trong thân ⇒ 400",
               "Ghi bút toán + sự kiện + nhật ký trong một giao dịch",
               "Ô đang mang giá trị khác nguồn ⇒ 409, kèm giá trị đang có",
               "Sổ gốc không đổi một ô"),
    # ── d2 · HIỆU LỰC
    "kiem": ("Đọc sổ hiệu lực và dòng loại",
             "Chạy 5 cổng GĐ1: pháp nhân rỗng · Σ theo pháp nhân = Σ theo nguồn · khoá lệnh chi trỏ rỗng · DIF CCR · 4 vế",
             "Mỗi cổng so với kết quả mong đã khai",
             "Không đo được ⇒ ĐỎ",
             "Đẩy kết quả ra F03"),
    "hieuLuc": ("Ghép dòng sổ gốc với lớp sửa",
                "Lấy giá trị hiệu lực từng ô",
                "Gắn chiều lệnh chi và 3 vai pháp nhân (TK · trả · nhận)",
                "Một view có tên, đủ 4 họ nguồn, đủ hai vế",
                "Được F01, F02, XUẤT và KIỂM đọc"),
    # ── e1 · ĐẦU RA
    "f03": ("Đọc kết quả cổng", "Hiện đạt · không đạt · chưa đo được"),
    "f01": ("Lọc theo một tiền tệ", "Hiện dòng chưa ghép / chưa đủ chiều kèm lý do", "Kế toán ghép hoặc sửa (S5)"),
    "f02": ("Hiện lưới sổ hiệu lực", "Ngăn kéo: nguồn nói gì · người nói gì · lúc nào", "Sửa một ô → GHI tay"),
    "xuat": ("Gom sổ hiệu lực theo TK · pháp nhân · ngày",
             "Dựng bảng báo cáo daily",
             "ghi_o.py tìm ô đích theo khoá, không theo địa chỉ cứng",
             "Chạy khô → owner duyệt",
             "Ghi vào sheet báo cáo daily của CCR khi cờ duyệt bật"),
    # ── hình 2 · mapping PP (1)
    "mMap": ("Nhận PM line, đợt lương / BH, giao dịch bank và luật ghép đã ký",
             "Chạy luật theo thứ tự: VN (Ref + tiền + pháp nhân) → nước ngoài (từ khoá + vendor + tiền) → lương / BH",
             "Σ tiền phải khớp; lệch ⇒ chặn; khác tiền tệ / N×M ⇒ để người",
             "Xếp mỗi dòng vào đúng một lớp L1 · L1b · L2 · L3",
             "Đếm từng lớp vào biên bản mapping"),
    "mSuy": ("Nhận dòng L3 và luật hiệu lực",
             "Tìm luật theo khoá (TK, mẫu nội dung, loại bank)",
             "Hai luật nói khác nhau ⇒ không gợi ý",
             "Ghi gợi ý loại giao dịch, nguồn = máy gợi ý"),
    "mXN": ("Nhận các lần kế toán giữ / sửa gợi ý",
            "Cộng bằng chứng theo khoá luật",
            "Đủ k lần cùng kết quả, 0 lần khác ⇒ luật ứng viên",
            "Một lần người sửa ngược ⇒ luật về 'xem lại'",
            "Đưa luật ứng viên lên chờ owner ký (m14)"),
    "mLuat": ("Luật mồi: 5 loại giao dịch hay sót",
              "Thêm luật ứng viên từ vòng cộng dồn",
              "Chỉ hiệu lực khi owner ký; có version"),
    # ── hình 3 · PP (3)
    "nTach": ("Đọc Mapping Block 1: ID Vendor ↔ Network-Acc ↔ CDT1 (PD Now 503)",
              "Tính % từng CDT1 theo loại · tháng",
              "Σ % ≠ 100 ⇒ chặn"),
    "nMap": ("Nhận chi phí 4 loại, giao dịch L3 và 4 luật đã ký",
             "Nhận diện giao dịch theo luật của từng loại",
             "Khớp kỳ và Σ tiền; lệch ⇒ chặn",
             "Giao dịch khớp ≥ 2 loại ⇒ để người",
             "Xếp: khớp · chờ tiền · tiền chưa khớp"),
    "nAlloc": ("Nhận giao dịch đã khớp và tỉ lệ CDT1",
               "Chia tiền theo tỉ lệ đúng loại · tháng",
               "Phần lẻ dồn vào một CDT1 có tên",
               "Ghi phần chia chỉ-thêm; giao dịch gốc giữ nguyên"),
    "nKiem": ("Cộng các phần chia của từng giao dịch",
              "So với tiền giao dịch, từng tiền tệ",
              "Lệch ⇒ chặn cả lượt"),
}

# ── ba phương pháp: luồng trọn từ nguồn tới sổ (bấm nhãn khung PP trên hình 1)
# ── bốn agent của vùng FLS · NẠP (owner 05/11: "highlight 4 con agents") — bước sau: dựng AP, chạy Flip eval
AGENT = {   # mã: (dải, nhãn ngắn, tên, luồng ≤ 5 bước, hộp thuộc agent)
    "ag1": ("c1", "AGENT 1", "Agent 1 · Collect_raw_data", (
        "Khởi bởi nhịp mỗi giờ (S1) và cú khai nguồn của kế toán (S2)",
        "Đọc chỉ-đọc: sổ cái PM / PC (FPS), 60 sao kê + 8 quỹ + 2 sheet CCR, 6 sổ H1000, 4 sổ nền tảng (Looker · Gsheet)",
        "Giữ bản khai nguồn có version: cột · thứ tự ngày · pháp nhân TK",
        "Ghi ảnh chụp đóng băng có chup_id; ảnh cũ không đổi một ô",
        "Ra: ảnh cho Agent 2"), ("anhFPS", "khai", "anhTien", "anhHR", "anhNT")),
    "ag2": ("c2", "AGENT 2", "Agent 2 · Generate Group Ledger (ITL raw)", (
        "Khởi bởi kế toán chọn lô / xem trước (S3) hoặc Nhận (S4)",
        "Đọc ảnh của Agent 1",
        "Dựng 4 loại dòng: lệnh (PM/PC) · tiền + số dư ngày · dòng lương H1000 · chi phí nền tảng + Combine Code",
        "Gắn pháp nhân, tính content_key, giữ đủ hai vế Nợ / Có",
        "Ra: dòng chuẩn cho Agent 3"), ("dLenh", "dTien", "dHR", "dNT")),
    "ag3": ("c3", "AGENT 3", "Agent 3 · Filter Fulfill & Adjust (ITL Adjust)", (
        "Khởi bởi Nhận lô (S4)",
        "PP (1): bank txns ↔ lệnh chi qua Reference No + luật vế Nợ → L1 · L2 · L3",
        "PP (2): dòng lương H1000 ↔ giao dịch bank theo Số CT",
        "PP (3): dòng ITL (đã có PE, đã nối bank) ⨝ nguồn GI · OMC · SC · PS theo Combine Code → chia CDT1",
        "Ra: mối nối, phần chia và dòng chưa khớp cho Agent 4"), ("ghep", "ghep2", "ghep3")),
    "ag4": ("c4", "AGENT 4", "Agent 4 · Auditor (Compounding Loop)", (
        "Chạy gpt-oss-20b — khác mô hình với A1–A3 (Qwen); khởi bởi xem trước (S3) và Nhận (S4)",
        "PP (1): 9 luật sao kê · Σ PM line = tiền · 4 vế · số dư ngày = CCR (DIF = 0)",
        "PP (2): Σ Có = Σ Nợ mỗi đợt · đủ tháng, ⛔ tháng trùng",
        "PP (3): Σ phần chia = tiền · Σ % CDT1 = 100",
        "Ra: dòng đạt cho GHI; CHẶN / CỜ / lệch vào hàng chờ có lý do"), ("soat", "soat2", "soat3")),
}
AG_THEO_DAI = {v[0]: k for k, v in AGENT.items()}

# ⭐ Owner 06/11: "dùng 1 model khác để kiểm". Agent LÀM (A1 · A2 · A3.x) chạy Qwen; agent KIỂM trong luồng (A4 · Auditor)
#   chạy mô hình KHÁC họ (gpt-oss-20b) — một bộ kiểm cùng họ với thứ nó kiểm sẽ chấm dễ (how-to 5.1).
#   Bộ chấm FLEET EVAL thì phải khác mô hình của CHÍNH agent bị đo ⇒ A1–A3 chấm bằng gpt-oss, A4 chấm bằng Qwen.
AG_NGAN = {"ag1": "Collect_raw_data", "ag2": "Group Ledger", "ag3": "Filter·Adjust", "ag4": "Auditor"}
AG_MO_HINH = {"ag1": "Qwen 3.8-27B", "ag2": "Qwen 3.8-27B", "ag3": "Qwen 3.8-27B", "ag4": "gpt-oss-20b"}
AG_CHAM = {"ag1": "gpt-oss-20b", "ag2": "gpt-oss-20b", "ag3": "gpt-oss-20b", "ag4": "Qwen 3.8-27B"}

# ── owner 06/11: "phần TO-BE thể hiện rõ được các agents mapping" ⇒ Agent 3 tách ba agent con, mỗi PP một con,
#    nối nhau bằng phần CHƯA khớp (q1 · q2). Chip "A3.1 / A3.2 / A3.3" trên hộp MAPPING bấm được.
AGENT_CON = {   # mã: (agent cha, chip, tên, luồng ≤ 5 bước, hộp)
    "ag3a": ("ag3", "A3.1", "Agent 3.1 · Filter Fulfill & Adjust · PP (1) — bank txns ↔ lệnh chi", (
        "Nhận dòng tiền hai vế (Agent 2) và dòng lệnh PM / PC",
        "Vế Có: Reference No → PM line; Σ tiền các line = tiền giao dịch, lệch ⇒ chặn",
        "Vế Nợ: luật vế Nợ (nội bộ · doanh thu · hoàn tiền · vay và lãi)",
        "Xếp L1 · L1b · L2 · L3; L3 đi qua vòng cộng dồn (hình 2) để được gợi ý loại giao dịch",
        "Chuyển L3 còn lại cho Agent 3.2 (q1)"), ("ghep",)),
    "ag3b": ("ag3", "A3.2", "Agent 3.2 · Filter Fulfill & Adjust · PP (2) — dòng lương H1000 ↔ bank txns", (
        "Nhận L3 từ Agent 3.1 và dòng lương H1000 đã tách HD · CDT1 · pháp nhân (Agent 2)",
        "Nối theo Số CT (số FT kế toán đã dán) = Reference number của giao dịch",
        "Σ dòng lương của một giao dịch = tiền giao dịch, lệch ⇒ hàng chờ",
        "Tháng trùng / thiếu ⇒ chặn",
        "Chuyển phần còn lại cho Agent 3.3 (q2)"), ("ghep2",)),
    "ag3c": ("ag3", "A3.3", "Agent 3.3 · Filter Fulfill & Adjust · PP (3) — 4 chi phí nền tảng ↔ PE/PM ↔ bank txns", (
        "Nhận giao dịch còn lại và chi phí OMC · GI · SC · PS (Agent 2)",
        "Combine Code (Vendor-Date-NoTrans) → PE/PM line trên FPS",
        "Reference No của PM → giao dịch bank; chia tiền theo CDT1",
        "Trúng 0 hoặc ≥ 2 PE ⇒ ở lại L3, vào hàng chờ có lý do",
        "Ra: mối nối, phần chia và dòng chưa khớp cho Agent 4"), ("ghep3",)),
}

PP_LUONG = {
    "pp1": ("Phương pháp (1) · mapping với bank transaction", (
        "Kế toán dán sao kê, ghi sổ quỹ, nhập số dư CCR ở Google Sheets",
        "FLS chụp theo bản khai nguồn (Bank · Cash · CCR)",
        "Dựng dòng tiền đủ hai vế PS Nợ / PS Có + số dư ngày; gắn pháp nhân TK",
        "Mapping với sổ cái PM qua Reference No (vế Có) và luật vế Nợ → L1 · L2 · L3",
        "Soát 9 luật + DIF CCR = 0 → ghi sổ; L3 chuyển sang PP (2)"),
        ("oKTnh", "oKTq", "oCCR", "saoke", "soquy", "ccr", "khai", "anhTien", "dTien", "ghep", "soat", "ghiNap")),
    "pp2": ("Phương pháp (2) · lương · BHXH · BHYT · PIT", (
        "HR lập file lương đã tách HD · CDT1 · pháp nhân; kế toán dán số FT bank",
        "FLS chụp 6 sổ H1000 năm",
        "Nạp thẳng dòng lương (owner 06/11 — ⛔ tự khớp Σ)",
        "Nối dòng lương với giao dịch bank theo Số CT",
        "Soát Σ Có = Σ Nợ, đủ tháng → ghi sổ; phần còn lại sang PP (3)"),
        ("oHR", "soluong", "anhHR", "dHR", "ghep2", "soat2", "ghiNap")),
    "pp3": ("Phương pháp (3) · 4 chi phí nền tảng", (
        "Data xuất GI · OMC từ Looker; SC (Luận) · PS (kế toán) ở Google Sheets",
        "FLS chụp 4 sổ Platform Data Ledger",
        "Dựng 4 loại chi phí + Combine Code Vendor-Date-NoTrans",
        "Combine Code nối dòng ITL (đã có PE/PM, đã nối bank) với dòng nguồn; Mapping Block 1 → chia CDT1 × tháng",
        "Soát Σ phần chia = tiền giao dịch → ghi sổ"),
        ("oNT", "sont", "anhNT", "dNT", "ghep3", "soat3", "ghiNap")),
}


# ═════════════════ NGUỒN CỦA MÁY / CỦA NGƯỜI — cả input lẫn output (owner 05/11) ═════════════════
# (chiều, nhãn, ai làm ra / ai nhận, rủi ro và cổng canh). Nhãn: MÁY = hệ sinh, không ai gõ ·
# NGƯỜI = người gõ / dán / ký · NGƯỜI+MÁY = người nhập, máy sinh sổ (hoặc máy đề xuất, người chốt).
NGUON_NM: dict[str, tuple[str, str, str, str]] = {
    # ── VÀO · nguồn ngoài FLS
    "soPM": ("VÀO", "NGƯỜI+MÁY", "người lập & duyệt PM / PC trên FPS; sổ cái do FPS sinh; Reference No do người gõ khi chi",
             "gõ sai / thiếu Reference No ⇒ không ghép được (L2 · L3); khoá gốc PM / PE của PC do người chọn ⇒ cần xác nhận cột (§5); FLS chỉ đọc trạng thái cuối"),
    "saoke": ("VÀO", "NGƯỜI+MÁY", "số liệu do ngân hàng sinh; kế toán ngân hàng dán vào sheet R |",
              "dán thiếu / thừa / lệch cột ⇒ bắt bằng bản khai + 9 luật soát + DIF CCR"),
    "soquy": ("VÀO", "NGƯỜI", "kế toán quỹ ghi tay hằng ngày",
              "gõ sai ⇒ chỉ bắt được khi số dư ngày lệch CCR Cash"),
    "ccr": ("VÀO", "NGƯỜI", "số dư Treasury nhập tay từng TK từng ngày (người nhập chưa xác định); khối Accounting là công thức",
            "ô rỗng ⇒ ngày ấy 'chưa đo được', ⛔ coi là khớp"),
    "soluong": ("VÀO", "NGƯỜI", "HR · C&B lập file lương, tách HD · CDT1 · pháp nhân; kế toán dán số FT bank vào từng khoản",
                "tháng trùng / thiếu, Σ lệch khi chưa dán FT (2025-10: INT lệch 567.500 · PIT ≈ 510,8 tr) ⇒ soát chặn"),
    "sont": ("VÀO", "NGƯỜI+MÁY", "GI · OMC do Looker sinh, Data (AnhTQ) xuất; SC (server cost) do SHQ1 (Luận) nhập ở Gsheet 'Chi phí Service Apero'; PS do SHQ2 (kế toán) nhập ở Gsheet 'AperoGroup_Payment'",
             "xuất sai kỳ / thiếu loại ⇒ chặn khi loại lạ; Σ chi phí kỳ phải khớp giao dịch"),
    # ── VÀO · người nhập ngay trong FLS
    "khai": ("VÀO", "NGƯỜI+MÁY", "máy đề xuất cột, thứ tự ngày, pháp nhân TK; kế toán khai, owner ký",
             "khai sai pháp nhân ⇒ sai chiều pháp nhân cả nguồn ⇒ owner ký, có version"),
    "lopSua": ("VÀO", "NGƯỜI+MÁY", "máy ghi mối nối + gợi ý; kế toán ghép / sửa / đảo trên F01 · F02",
               "máy gợi ý ⛔ đè ô người đã chốt; mọi sửa có actor + nhật ký"),
    "mLuat": ("VÀO", "NGƯỜI+MÁY", "máy gom bằng chứng ra luật ứng viên; owner ký thành luật",
              "luật chưa ký ⛔ hiệu lực; một lần người sửa ngược ⇒ luật về 'xem lại'"),
    # ── RA
    "f01": ("RA", "NGƯỜI", "kế toán đọc hàng chờ, quyết ghép / sửa",
            "luôn lọc một tiền tệ; ô máy gợi ý hiện là gợi ý"),
    "f02": ("RA", "NGƯỜI", "kế toán, owner đọc lưới sổ hiệu lực",
            "mỗi ô nói được nguồn nói gì, người nói gì, lúc nào"),
    "f03": ("RA", "NGƯỜI", "owner, kế toán đọc kết quả cổng",
            "phép không đo được hiện ĐỎ, ⛔ hiện 'không thấy lệch'"),
    "xuat": ("RA", "NGƯỜI+MÁY", "máy ghi vào báo cáo daily của CCR; owner duyệt cú ghi; người đọc báo cáo",
             "ghi neo theo khoá, chạy khô trước, cờ duyệt tắt ⇒ ⛔ ghi"),
}


# ═════════════════ CHỮ GỌN TRÊN HÌNH 1 — tên + MỘT dòng (owner 06/11: "bỏ bớt chữ") ═════════════════
# Chữ đầy đủ (tên dài · dòng · số liệu · đối chiếu) vẫn ở khung chi tiết và chú thích rê chuột.
NGAN: dict[str, tuple[str, str]] = {
    "oPM": ("LẬP·DUYỆT PM·PC", "trong FPS"), "oKTnh": ("KT NGÂN HÀNG", "dán sao kê"),
    "oKTq": ("KẾ TOÁN QUỸ", "ghi sổ quỹ"), "oCCR": ("NHẬP SỐ DƯ", "từng TK · ngày"),
    "oHR": ("HR · C&B", "lập sổ lương"), "oNT": ("DATA·LUẬN·KT", "Looker · Gsheet"),
    "soPM": ("sổ cái PM · PC", "FPS · 3.772 dòng"), "saoke": ("sao kê", "60 dòng chảy"),
    "soquy": ("sổ quỹ", "8 dòng chảy"), "ccr": ("CCR · CCR Cash", "số dư ngày"),
    "soluong": ("sổ H1000", "6 sổ năm · đã tách"), "sont": ("sổ nền tảng", "Looker + 2 Gsheet"),
    "S1": ("S1 · NHỊP", ""), "S2": ("S2 · KHAI", ""), "S3": ("S3 · XEM", "F04"),
    "S4": ("S4 · NHẬN", ""), "S5": ("S5 · SỬA", ""),
    "anhFPS": ("ảnh sổ cái", "PM·PC đóng băng"), "khai": ("bản khai", "cột·ngày·LE"),
    "anhTien": ("ảnh sao kê · quỹ · CCR", "theo bản khai · Bank ✅ · Cash ⛔ · CCR ⛔"),
    "anhHR": ("ảnh sổ lương", "lằn HR ⛔"), "anhNT": ("ảnh nền tảng", "lằn Platform ⛔"),
    "dLenh": ("DỰNG lệnh chi", "PM / PC line"),
    "dTien": ("DỰNG dòng tiền + số dư ngày", "hai vế PS Nợ · PS Có · pháp nhân TK · content_key"),
    "dHR": ("DỰNG dòng lương", "nạp thẳng H1000"), "dNT": ("DỰNG nền tảng", "+ Combine Code"),
    "ghep": ("MAPPING PP (1) · bank txns ↔ lệnh chi", "Reference No · cả PS Nợ và PS Có → L1 · L2 · L3"),
    "ghep2": ("MAPPING (2)", "lương ↔ Số CT"), "ghep3": ("MAPPING (3)", "PE/PM → bank"),
    "soat": ("SOÁT PP (1)", "9 luật · 4 vế · số dư ngày = CCR (DIF = 0)"),
    "soat2": ("SOÁT (2)", "Σ Có = Σ Nợ"), "soat3": ("SOÁT (3)", "Σ % CDT1 = 100"),
    "ghiNap": ("GHI lượt nạp — một giao dịch cho cả 3 PP", "lỗi giữa chừng ⇒ không còn dòng nào đã ghi"),
    "loai": ("dòng bị loại", "fls_reject"), "soITL": ("SỔ ITL", "chỉ-thêm · fls_itl 8.387"),
    "lopSua": ("lớp sửa chỉ-thêm", "mối nối · bút toán · nhật ký"), "ghiTay": ("GHI tay", "chỗ ghi duy nhất"),
    "kiem": ("KIỂM cổng", "khai mong · đỏ"),
    "hieuLuc": ("SỔ ITL HIỆU LỰC — bảng ITL duy nhất", "sổ gốc + lớp sửa · 3 vai pháp nhân"),
    "f03": ("F03 · cổng", "đạt · không đạt"), "f01": ("F01 · hàng chờ", "chưa ghép · thiếu chiều"),
    "f02": ("F02 · sổ ITL", "ô nào · ai nói · lúc nào"), "xuat": ("XUẤT báo cáo daily CCR", "theo TK · pháp nhân · ngày"),
}


# ═════════════════ AS-IS — bên phải hình 1, xếp vào ĐÚNG các lớp của TO-BE ═════════════════
# Nguồn: artifact "Voi ITL AS-IS" (owner gửi 06/11), dữ liệu chép ở voi_asis_goc.json (đã bỏ URL Sheets).
# Mỗi hộp AS-IS trên hình gộp ≥ 1 hộp gốc (goc); máy kiểm: 52/52 hộp gốc có mặt đúng một lần, và mọi
# mũi tên gốc hoặc nằm TRONG một hộp gộp, hoặc được một mũi tên AS-IS chở (goc) — ⛔ mất một đường nào.
ASIS_GOC = json.loads((Path(__file__).with_name("voi_asis_goc.json")).read_text(encoding="utf-8"))

HOP_A: list[Hop] = [
    # ai sinh ra
    Hop("aoP", "A0", cota(1), "o", "a", "NGƯỜI ĐỀ NGHỊ · DUYỆT · CA NHẬP REF", goc=("oDN", "oCA"),
        doi_chieu="TO-BE cùng lớp: LẬP & DUYỆT PM · PC (FPS)"),
    Hop("aoNH", "A0", cota(3), "o", "a", "KẾ TOÁN NGÂN HÀNG", goc=("oNH",), doi_chieu="TO-BE: KẾ TOÁN NGÂN HÀNG"),
    Hop("aoKQ", "A0", cota(4), "o", "a", "KẾ TOÁN QUỸ", goc=("oKQ",), doi_chieu="TO-BE: KẾ TOÁN QUỸ"),
    Hop("aoSD", "A0", cota(5), "o", "a", "NGƯỜI NHẬP SỐ DƯ", goc=("oSD",), doi_chieu="TO-BE: NGƯỜI NHẬP SỐ DƯ"),
    Hop("aoHR", "A0", cota(6), "o", "a", "HR · C&B", goc=("oHR",), doi_chieu="TO-BE: HR · C&B"),
    Hop("aoDT", "A0", cota(7), "o", "a", "DATA (Looker) · LUẬN · KẾ TOÁN (Gsheet)", goc=("oDT",), doi_chieu="TO-BE: DATA · SHQ1 · SHQ2"),
    # sổ nguồn
    Hop("aEntry", "A1", cota(1), "x", "a", "Entry Data P100 (PE · PI · PM · PC)", goc=("dEntry",),
        doi_chieu="TO-BE: sổ cái PM · PC của FPS (đọc thẳng sổ cái, ⛔ đọc phiếu)"),
    Hop("aSK", "A1", cota(3), "x", "a", "sao kê · sheet R |", goc=("dSK",), doi_chieu="TO-BE: sao kê (cùng sheet)"),
    Hop("aSQ", "A1", cota(4), "x", "a", "sổ quỹ · sheet R |", goc=("dSQ",), doi_chieu="TO-BE: sổ quỹ (cùng sheet)"),
    Hop("aCCR", "A1", cota(5), "x", "a", "2. CCR · CCR Cash", goc=("dCCR",), doi_chieu="TO-BE: CCR · CCR Cash (cùng sheet)"),
    Hop("aPR", "A1", cota(6), "x", "a", "EDD + file lương tháng", goc=("dEDD", "dPR"), doi_chieu="TO-BE: sổ lương HR"),
    Hop("aLK", "A1", cota(7), "x", "a", "GI · OMC (Looker) + SC · PS (Google Sheets)", goc=("dLK",),
        doi_chieu="TO-BE: 4 sổ Platform Data Ledger (cùng nguồn) · PD Now 103–106"),
    # ① KHAI & CHỤP
    Hop("aDuoi", "c1", cota(1), "p", "a", "DUỖI DÒNG (GScript) → PE·PI·PM_Unpivot", goc=("oKTS", "pDUOI", "dUNP"), tay=True,
        doi_chieu="TO-BE: ảnh sổ cái (nhịp S1, ⛔ người bấm)"),
    Hop("aMM", "c1", cota(2), "d", "a", "Mapping Master", goc=("dMM",),
        doi_chieu="TO-BE: bản khai nguồn — cột pháp nhân TK (máy đề xuất, kế toán khai, owner ký, có version)"),
    Hop("aGom", "c1", cota(3, 4), "p", "a", "GOM GD BANK · QUỸ (nút GScript) → Bank Transactions · Cash Ledger Trans.",
        goc=("oKTG", "pGB", "dBT", "pGQ", "dCT"), tay=True, doi_chieu="TO-BE: ảnh sao kê · quỹ · CCR (nhịp S1 theo bản khai)"),
    Hop("aGN", "c1", cota(7), "p", "a", "GOM NGUỒN NỀN TẢNG → Platform Data Ledger", goc=("pGN", "dPL"),
        doi_chieu="TO-BE: ảnh Looker"),
    # ② DỰNG
    Hop("aGop", "c2", cota(3, 4), "p", "a", "CHUYỂN A-CCR · GỘP → Ledger 111/112 → Transaction Original",
        goc=("oKTC", "pCH", "dLED", "dIL", "pGOP", "dTO"), tay=True,
        doi_chieu="TO-BE: DỰNG dòng tiền + số dư ngày (từ ảnh, ⛔ đẩy tay)"),
    Hop("aTach", "c2", cota(6), "p", "a", "TÁCH LƯƠNG theo HD·CDT1 → 1.3 Ledger → H1000 (12 tháng)",
        goc=("oKTL", "pTACH", "dL13", "oKT12", "pG12", "dH1000", "pTH", "dHRR"), tay=True,
        doi_chieu="TO-BE: DỰNG đợt lương · BH (GĐ1 → LE; GĐ2 → KRF)"),
    # ③ MAPPING
    Hop("aGhep", "c3", cota(1, 3), "p", "a", "GHÉP LỆNH CHI (VLOOKUP Reference number) → Transaction Mapping L1",
        goc=("dIU", "pGHEP", "dML1"), doi_chieu="TO-BE: MAPPING PP (1)"),
    # ④ SOÁT
    Hop("aSoat", "c4", cota(4, 5), "p", "a", "SOÁT ĐỦ GIAO DỊCH · số dư CCR ↔ lũy kế Ledger (DIF)", goc=("pSOAT",),
        doi_chieu="TO-BE: SOÁT PP (1) — số dư ngày = CCR (DIF = 0)"),
    # ⑤ GHI
    Hop("aNhap", "c5", cota(1, 3), "d", "a", "ITL Ledge · cột A–Q (IMPORTRANGE)", goc=("dITLi",),
        doi_chieu="TO-BE: GHI lượt nạp"),
    Hop("aH1i", "c5", cota(6), "d", "a", "H1000 Ledge (HR Allocate HD)", goc=("dH1i",), doi_chieu="TO-BE: GHI lượt nạp (phần PP 2)"),
    # ⑥ SỔ GỐC
    Hop("aADJ", "d1", cota(1, 6), "p", "a", "CHỈNH TAY · ADJUSTMENT ZONE (cột R–AT)", goc=("oKTA", "pADJ"), tay=True,
        doi_chieu="TO-BE: lớp sửa chỉ-thêm + GHI tay (actor, nhật ký)"),
    # ⑦ HIỆU LỰC
    Hop("aFinal", "d2", cota(1, 3), "d", "a", "ITL Ledge (Final)", goc=("dITLF",), doi_chieu="TO-BE: SỔ ITL HIỆU LỰC"),
    Hop("aH1F", "d2", cota(6), "d", "a", "H1000 Ledge (Final)", goc=("dH1F",), doi_chieu="TO-BE: SỔ ITL HIỆU LỰC (một bảng, ⛔ hai sổ)"),
    # ⑧ NGƯỜI THẤY
    Hop("aRPT", "e1", cota(1, 3), "d", "a", "Report General Ledger · CF report", goc=("oRPT",),
        doi_chieu="TO-BE: XUẤT báo cáo daily CCR · F02"),
    Hop("aRH", "e1", cota(6), "d", "a", "Report H1000 Ledge · PLA3 Daily", goc=("oRH",), doi_chieu="TO-BE: XUẤT"),
    Hop("aALL", "e1", cota(7), "d", "a", "PHÂN BỔ NỀN TẢNG (% CDT1 × tháng)", goc=("oALL",),
        doi_chieu="TO-BE: MAPPING (3) → chia theo CDT1"),
]
HOP_A_THEO = {h.ma: h for h in HOP_A}

NGAN.update({
    "aoP": ("ĐỀ NGHỊ · CA", "Gform · gõ Ref"), "aoNH": ("KT NGÂN HÀNG", "gõ sao kê"),
    "aoKQ": ("KẾ TOÁN QUỸ", "ghi thu chi"), "aoSD": ("NHẬP SỐ DƯ", "tay · ai: ?"),
    "aoHR": ("HR · C&B", "EDD · lương"), "aoDT": ("DATA·LUẬN·KT", "Looker · Gsheet"),
    "aEntry": ("Entry Data P100", "PE·PI·PM·PC"), "aSK": ("sao kê R |", "60 sheet"),
    "aSQ": ("sổ quỹ R |", "8 quỹ"), "aCCR": ("2. CCR · Cash", "số dư gõ tay"),
    "aPR": ("EDD · lương", "file tháng"), "aLK": ("sổ nền tảng", "Looker + Gsheet"),
    "aDuoi": ("DUỖI DÒNG", "→ PM_Unpivot"), "aMM": ("Mapping Master", "sheet → LE"),
    "aGom": ("GOM GD BANK · QUỸ", "nút GScript → Bank / Cash Trans."), "aGN": ("GOM NỀN TẢNG", "→ Platform Ledger"),
    "aGop": ("CHUYỂN A-CCR · GỘP", "Ledger 111/112 → Trans. Original"), "aTach": ("TÁCH LƯƠNG", "HD·CDT1 → H1000"),
    "aGhep": ("GHÉP LỆNH CHI", "VLOOKUP Ref → Mapping L1"), "aSoat": ("SOÁT SỐ DƯ", "CCR ↔ Ledger · DIF bằng mắt"),
    "aNhap": ("ITL Ledge · A–Q", "IMPORTRANGE"), "aH1i": ("H1000 Ledge", "HR Allocate HD"),
    "aADJ": ("CHỈNH TAY · ADJUSTMENT ZONE", "kế toán điền R–AT · ô trống nhận mặc định"),
    "aFinal": ("ITL Ledge (Final)", "đè ô · người + máy"), "aH1F": ("H1000 (Final)", "sổ thứ hai"),
    "aRPT": ("Report General Ledger", "CF report · in CCR ký tháng"), "aRH": ("Report H1000", "PLA3 Daily"),
    "aALL": ("PHÂN BỔ N.TẢNG", "% CDT1 × tháng"),
})

TEN_A: list[Ten] = [
    Ten("a1", "aoP", "aEntry", "t", "đề nghị · duyệt (Gform → Gsheet) · Reference number gõ tay sau khi chi", "", "", "", "", 0.0, "", ("n1", "n2")),
    Ten("a2", "aoNH", "aSK", "t", "gõ / dán sao kê thô, mỗi TK một sheet", "", "", "", "", 0.0, "", ("n4",)),
    Ten("a3", "aoKQ", "aSQ", "t", "ghi giao dịch quỹ", "", "", "", "", 0.0, "", ("n5",)),
    Ten("a4", "aoSD", "aCCR", "t", "nhập số dư cuối ngày từng TK / quỹ", "", "", "", "", 0.0, "", ("n3",)),
    Ten("a5", "aoHR", "aPR", "t", "quyết định nhân sự · chấm công · BH · COM · thưởng", "", "", "", "", 0.0, "", ("n6", "n7")),
    Ten("a6", "aoDT", "aLK", "t", "GI · OMC xuất bảng từ Looker; SC · PS cập nhật tay ở Google Sheets", "", "", "", "", 0.0, "", ("n8",)),
    Ten("a7", "aEntry", "aDuoi", "a", "dòng đã duyệt", "", "", "", "", 0.0, "", ("m1",)),
    Ten("a8", "aSK", "aGom", "a", "6 cột chuẩn của sheet R |", "", "", "", "", 0.0, "", ("m3",)),
    Ten("a9", "aSQ", "aGom", "a", "dòng sổ quỹ", "", "", "", "", 0.0, "", ("m6",)),
    Ten("a10", "aLK", "aGN", "a", "tab tháng", "", "", "", "", 0.0, "", ("m10",)),
    Ten("a11", "aGom", "aGop", "a", "Bank Transactions · Cash Ledger Transactions", "", "", "", "", 0.0, "", ("m17", "m19")),
    Ten("a12", "aPR", "aTach", "a", "EDD · dòng nhân viên + khoá PE", "", "", "", "", 0.0, "", ("m7", "m8")),
    Ten("a13", "aDuoi", "aGhep", "a", "PM · PE · PI line (khoá Ref) qua IMPORTRANGE", "", "", "", "", 0.0, "", ("r1",)),
    Ten("a14", "aMM", "aGhep", "a", "LE theo tên sheet bank", "", "", "", "", 0.0, "", ("r7",)),
    Ten("a15", "aGop", "aGhep", "a", "giao dịch theo ngày (Transaction Original)", "", "", "", "", 0.0, "", ("r5",)),
    Ten("a16", "aGop", "aSoat", "a", "lũy kế Ledger 111 / 112 theo ngày", "", "", "", "", 0.0, "", ("m24",)),
    Ten("a17", "aCCR", "aSoat", "a", "số dư nhập tay", "", "", "", "", 0.0, "", ("m22",)),
    Ten("a18", "aGhep", "aNhap", "a", "IMPORTRANGE cột A–Q", "", "", "", "", 0.0, "", ("j1",)),
    Ten("a19", "aTach", "aH1i", "a", "IMPORTRANGE + FILTER", "", "", "", "", 0.0, "", ("j2",)),
    Ten("a20", "aNhap", "aADJ", "a", "dòng ITL", "", "", "", "", 0.0, "", ("j3",)),
    Ten("a21", "aH1i", "aADJ", "a", "dòng HR", "", "", "", "", 0.0, "", ("j5",)),
    Ten("a22", "aADJ", "aFinal", "a", "Final", "", "", "", "", 0.0, "", ("j6",)),
    Ten("a23", "aADJ", "aH1F", "a", "Final", "", "", "", "", 0.0, "", ("j7",)),
    Ten("a24", "aFinal", "aH1F", "a", "ITL ID (VLOOKUP Số CT)", "", "", "", "", None, "", ("j8",)),
    Ten("a25", "aFinal", "aRPT", "a", "ITL Ledge", "", "", "", "", 0.0, "", ("o1",)),
    Ten("a26", "aH1F", "aRH", "a", "H1000 Ledge", "", "", "", "", 0.0, "", ("o2",)),
    Ten("a27", "aGN", "aALL", "a", "sổ nền tảng", "", "", "", "", 0.0, "", ("o3",)),
]
for _t in TEN_A:
    _t.khoa = "gốc " + " · ".join(_t.goc)
    _t.ban_so = "—"
    _t.cong = "người làm tay" if _t.tt == "t" else "công thức / GScript"
    _t.co_ma = "AS-IS hôm nay"
dat_x(TEN_A, HOP_A_THEO)


def _gan_asis() -> None:
    """Gắn nhãn máy/người cho hộp AS-IS từ hộp gốc dữ liệu đầu tiên có nhãn."""
    for h in HOP_A:
        if h.dai in ("A1", "d2") or h.ma == "aMM":
            g = next((ASIS_GOC["hop"][m] for m in h.goc if ASIS_GOC["hop"][m].get("nm")), None)
            if g:
                h.nm = ("VÀO", g["nm"], g.get("ai") or g.get("cach", "")[:120], g.get("issue", ""))


_gan_asis()


# ───────────────────────────── kiểm hình ─────────────────────────────
def doan(t: Ten, ht: dict | None = None) -> tuple[float, float, float, float]:
    ht = ht or HOP_THEO
    a, b = ht[t.tu], ht[t.toi]
    if t.x is not None:
        if a.y[0] > b.y[0]:                                # dọc đi LÊN (vòng cộng dồn)
            return t.x, a.y[0], t.x, b.y[1]
        return t.x, a.y[1], t.x, b.y[0]                    # dọc, a ở trên b
    ya = (max(a.y[0], b.y[0]) + min(a.y[1], b.y[1])) / 2   # ngang, cùng dải
    if a.x[1] <= b.x[0]:
        return a.x[1], ya, b.x[0], ya
    return a.x[0], ya, b.x[1], ya


def cat_hop(x1, y1, x2, y2, h: Hop) -> bool:
    lx, rx = sorted((x1, x2))
    ty, by = sorted((y1, y2))
    return not (rx <= h.x[0] or lx >= h.x[1] or by <= h.y[0] or ty >= h.y[1])


# ⚠ Ngoại lệ có chủ: vùng nguồn của phương pháp (2) HR và (3) nền tảng mỗi vùng chỉ có
#   MỘT người lập và MỘT sổ — owner tách thành phương pháp riêng (bình luận 04/11).
#   Gộp lại cho đủ 2 hộp là vẽ sai sự thật để chiều luật đếm.
MOT_HOP_OK = {"A0", "A1", "G0", "G1", "H0", "H1"}   # v0.4: PM · PC gộp ⇒ FPS cũng một người lập + một sổ


def so_muc(d: str) -> int:
    """Số mục của một dải: hộp lẻ + mỗi khung chứa tính MỘT (luật vẽ voi: khung là một tầng)."""
    hs = [h for h in HOP if h.dai == d]
    return sum(1 for h in hs if not h.khoi) + len({h.khoi for h in hs if h.khoi})


def gan_luong() -> list[str]:
    loi = []
    tat_ca = {h.ma: h for h in HOP + HOP_M + HOP_N}
    for ma, buoc in LUONG.items():
        if ma not in tat_ca:
            loi.append(f"LUONG có hộp lạ: {ma}")
            continue
        if not 1 <= len(buoc) <= 5:
            loi.append(f"luồng {ma}: {len(buoc)} bước (phải 1–5)")
        tat_ca[ma].luong = buoc
    for k, (cha, _c, _t, buoc, tv) in AGENT_CON.items():
        if not 1 <= len(buoc) <= 5:
            loi.append(f"{k}: {len(buoc)} bước")
        loi += [f"{k}: hộp {m} không thuộc agent cha {cha}" for m in tv if m not in AGENT[cha][4]]
    con_phu = sorted(m for v in AGENT_CON.values() for m in v[4])
    if con_phu != sorted(AGENT["ag3"][4]):
        loi.append(f"agent con phải phủ ĐÚNG hộp của Agent 3: {con_phu} ≠ {sorted(AGENT['ag3'][4])}")
    for k, (d, _n, _t, buoc, tv) in AGENT.items():
        if not 1 <= len(buoc) <= 5:
            loi.append(f"{k}: {len(buoc)} bước")
        loi += [f"{k}: hộp {m} không ở dải {d}" for m in tv if m not in HOP_THEO or HOP_THEO[m].dai != d]
    for k, (_t, buoc, tv) in PP_LUONG.items():
        if not 1 <= len(buoc) <= 5:
            loi.append(f"luồng {k}: {len(buoc)} bước")
        loi += [f"{k}: thành viên lạ {m}" for m in tv if m not in HOP_THEO]
    for ma, v in NGUON_NM.items():
        if ma not in tat_ca:
            loi.append(f"NGUON_NM có hộp lạ: {ma}")
        elif v[1] not in ("MÁY", "NGƯỜI", "NGƯỜI+MÁY") or v[0] not in ("VÀO", "RA"):
            loi.append(f"NGUON_NM {ma}: nhãn sai {v[:2]}")
        else:
            tat_ca[ma].nm = v
    # mọi nguồn ngoài FLS và mọi hộp ở dải ĐẦU RA phải có nhãn máy / người
    loi += [f"hộp {h.ma} thiếu nhãn máy/người" for h in HOP if (h.loai == "x" or h.dai == "e1") and not h.nm]
    # mọi hộp XỬ LÝ phải có luồng
    loi += [f"hộp xử lý {h.ma} thiếu luồng" for h in HOP + HOP_M + HOP_N if h.loai == "p" and not h.luong]
    return loi


def kiem() -> dict:
    loi: list[str] = gan_luong()
    for d in DAI:
        n = so_muc(d)
        if d in MOT_HOP_OK and n == 1:
            continue
        if not 2 <= n <= 5:
            loi.append(f"dải {d}: {n} mục (phải 2–5)")
    for kh in {h.khoi for h in HOP if h.khoi}:
        n = sum(1 for h in HOP if h.khoi == kh)
        if not 2 <= n <= 5:
            loi.append(f"khung {kh}: {n} hộp (phải 2–5)")
    for v in TEN_VUNG:
        n = sum(1 for d in DAI.values() if d[0] == v)
        if n > 5:
            loi.append(f"vùng {v}: {n} dải")
    for t in TEN:
        a, b = HOP_THEO[t.tu], HOP_THEO[t.toi]
        x1, y1, x2, y2 = doan(t)
        if t.x is not None:
            if not (a.x[0] + 6 <= t.x <= a.x[1] - 6 and b.x[0] + 6 <= t.x <= b.x[1] - 6):
                loi.append(f"{t.ma}: x={t.x} ngoài hộp {a.ma}/{b.ma}")
            if TANG[b.dai] - TANG[a.dai] != 1:
                loi.append(f"{t.ma}: {a.dai}→{b.dai} ⛔ không kề nhau")
            if y2 <= y1:
                loi.append(f"{t.ma}: đi ngược")
        elif a.dai != b.dai:
            loi.append(f"{t.ma}: ngang mà khác dải")
        for h in HOP:
            if h.ma in (t.tu, t.toi):
                continue
            if cat_hop(x1, y1 + 0.5, x2, y2 - 0.5, h) and cat_hop(x1 + 0.5, y1, x2 - 0.5, y2, h):
                loi.append(f"{t.ma} cắt qua hộp {h.ma}")
    cheo = 0
    for i, t in enumerate(TEN):
        for u in TEN[i + 1:]:
            if (t.x is None) == (u.x is None):
                continue
            dd, nn = (doan(t), doan(u)) if t.x is not None else (doan(u), doan(t))
            x, ya, _, yb = dd
            xa, y, xb, _ = nn
            if min(xa, xb) < x < max(xa, xb) and min(ya, yb) < y < max(ya, yb):
                cheo += 1
                loi.append(f"{t.ma} × {u.ma} cắt nhau")
    ma = [t.ma for t in TEN] + [h.ma for h in HOP]
    if len(set(ma)) != len(ma):
        loi.append("mã trùng")
    return {"hop": len(HOP), "ten": len(TEN), "doc": sum(t.x is not None for t in TEN),
            "ngang": sum(t.x is None for t in TEN), "cheo": cheo, "loi": loi}


NHOM_COT = {1: "lệnh chi", 2: "bản khai", 3: "PP1", 4: "PP1", 5: "PP1", 6: "PP2", 7: "PP3"}


def cot_cua(x0: float) -> int:
    return round((x0 - XA0) / 112) + 1


def kiem_a() -> list[str]:
    """Luật vẽ của nửa AS-IS. Khác TO-BE đúng MỘT điều có chủ ý: mũi tên dọc được đi qua dải giữa
    nếu làn ấy TRỐNG (AS-IS có những bước nhảy thật, ví dụ sổ CCR gõ tay đi thẳng xuống bước soát).
    Còn lại giữ nguyên: thẳng, đi xuống, ⛔ cắt qua hộp, ⛔ hai mũi tên chồng hay cắt nhau."""
    loi: list[str] = []
    goc_hop = [m for h in HOP_A for m in h.goc]
    tat_ca = set(ASIS_GOC["hop"])
    if len(goc_hop) != len(set(goc_hop)):
        loi.append("AS-IS: hộp gốc bị gộp hai lần")
    if set(goc_hop) != tat_ca:
        loi.append(f"AS-IS: thiếu hộp gốc {sorted(tat_ca - set(goc_hop))} · lạ {sorted(set(goc_hop) - tat_ca)}")
    o_dau = {m: h.ma for h in HOP_A for m in h.goc}
    cho = {m for t in TEN_A for m in t.goc}
    for m, t in ASIS_GOC["ten"].items():
        a, b = o_dau.get(t["tu"]), o_dau.get(t["toi"])
        if a == b:
            if m in cho:
                loi.append(f"AS-IS: {m} nằm trong {a} mà vẫn vẽ mũi tên")
            continue
        chu = [u for u in TEN_A if m in u.goc]
        if len(chu) != 1 or (chu[0].tu, chu[0].toi) != (a, b):
            loi.append(f"AS-IS: mũi tên gốc {m} ({a} → {b}) không có đúng một mũi tên chở")
    for d in DAI:
        hs = [h for h in HOP_A if h.dai == d]
        nhom = {NHOM_COT.get(cot_cua(h.x[0]), "ngoài lưới") for h in hs}
        if hs and not 1 <= len(nhom) <= 5:
            loi.append(f"AS-IS dải {d}: {len(nhom)} nhóm")
    for i, h in enumerate(HOP_A):
        if h.x[0] < XA0 or h.x[1] > W - 4:
            loi.append(f"AS-IS {h.ma}: ra ngoài nửa phải")
        for g in HOP_A[i + 1:]:
            if h.dai == g.dai and not (h.x[1] <= g.x[0] or g.x[1] <= h.x[0]):
                loi.append(f"AS-IS {h.ma} chồng {g.ma}")
    for t in TEN_A:
        a, b = HOP_A_THEO[t.tu], HOP_A_THEO[t.toi]
        x1, y1, x2, y2 = doan(t, HOP_A_THEO)
        if t.x is not None:
            if not (a.x[0] + 6 <= t.x <= a.x[1] - 6 and b.x[0] + 6 <= t.x <= b.x[1] - 6):
                loi.append(f"{t.ma}: x={t.x} ngoài hộp {a.ma}/{b.ma}")
            if y2 <= y1:
                loi.append(f"{t.ma}: đi ngược")
        elif a.dai != b.dai:
            loi.append(f"{t.ma}: ngang mà khác dải")
        for h in HOP_A:
            if h.ma in (t.tu, t.toi):
                continue
            if cat_hop(x1, y1 + 0.5, x2, y2 - 0.5, h) and cat_hop(x1 + 0.5, y1, x2 - 0.5, y2, h):
                loi.append(f"{t.ma} cắt qua hộp {h.ma}")
    for i, t in enumerate(TEN_A):
        for u in TEN_A[i + 1:]:
            p, q = doan(t, HOP_A_THEO), doan(u, HOP_A_THEO)
            if t.x is not None and u.x is not None:
                if abs(p[0] - q[0]) < 1 and min(p[3], q[3]) > max(p[1], q[1]):
                    loi.append(f"{t.ma} chồng lên {u.ma}")
            elif (t.x is None) != (u.x is None):
                dd, nn = (p, q) if t.x is not None else (q, p)
                if min(nn[0], nn[2]) < dd[0] < max(nn[0], nn[2]) and min(dd[1], dd[3]) < nn[1] < max(dd[1], dd[3]):
                    loi.append(f"{t.ma} × {u.ma} cắt nhau")
    ma = [t.ma for t in TEN_A] + [h.ma for h in HOP_A] + [t.ma for t in TEN] + [h.ma for h in HOP]
    if len(set(ma)) != len(ma):
        loi.append("AS-IS: mã trùng với TO-BE")
    loi += [f"thiếu chữ gọn cho {h.ma}" for h in HOP + HOP_A if h.ma not in NGAN]
    return loi


# ───────────────────────────── vẽ SVG ─────────────────────────────
E = html.escape
LOAI_CHU = {"o": "khởi động", "x": "nguồn ngoài", "d": "dữ liệu", "p": "xử lý"}
TT_CHU = {"b": "có mã", "q": "GĐ1 phải dựng", "n": "đề xuất, chờ owner", "a": "AS-IS hôm nay", "t": "AS-IS · người làm tay"}


def svg() -> str:
    """Hình 1 gộp: TO-BE (trái) · AS-IS (phải), chung dải. Chữ gọn; chi tiết ở khung bấm."""
    o: list[str] = [f'<svg viewBox="0 0 {W} {H}" role="group" aria-label="Voi FLS phase 1: TO-BE bên trái, AS-IS bên phải; bấm một hộp hay mũi tên để xem chi tiết">',
                    '<defs>']
    for k in ("b", "q", "n", "a", "t"):
        o.append(f'<marker id="m{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                 f'orient="auto"><path d="M0 0L10 5L0 10z" class="mk-{k}"/></marker>')
    o.append('</defs>')
    xr = cot(7)[1] + 6                                   # mép phải nửa TO-BE
    xa = XA0 - 6                                         # mép trái nửa AS-IS
    # ── tiêu đề hai nửa ──
    o.append(f'<text class="hd" x="{C0[0]}" y="16">TO-BE · FLS giai đoạn 1</text>')
    o.append(f'<text class="hd hd-a" x="{XA0}" y="16">AS-IS · Google Sheets hôm nay</text>')
    o.append(f'<line class="tach" x1="{(xr + xa) / 2}" y1="4" x2="{(xr + xa) / 2}" y2="{H - 4}"/>')
    # ── vùng nguồn: khung theo phương pháp, hai nửa cùng cột ──
    yt0, yt1 = 24, DAI["A1"][1] + DAI["A1"][2] + 8
    khung_tren = [((1, 1), "FPS", "vz-ext", None), ((3, 5), "PHƯƠNG PHÁP (1) ▸", "vz-pp1", "pp1"),
                  ((6, 6), "PP (2) ▸", "vz-pp1", "pp2"), ((7, 7), "PP (3) ▸", "vz-pp1", "pp3")]
    for (a, b), nh, cl, pp in khung_tren:
        x0, x1 = cot(a)[0] - 3, cot(b)[1] + 3
        o.append(f'<rect class="vz {cl}" x="{x0}" y="{yt0}" width="{x1 - x0}" height="{yt1 - yt0}" rx="5"/>')
        if pp:
            o.append(f'<g class="pp-nhan" data-id="h:{pp}" tabindex="0" role="button" aria-label="Luồng {E(PP_LUONG[pp][0])}">'
                     f'<rect class="pp-hit" x="{x0 + 2}" y="{yt0 + 3}" width="{min(x1 - x0 - 4, 7 * len(nh) + 8)}" height="14" rx="3"/>'
                     f'<text class="vt vt-pp1" x="{x0 + 6}" y="{yt0 + 14}">{E(nh)}</text></g>')
        else:
            o.append(f'<text class="vt" x="{x0 + 6}" y="{yt0 + 14}">{E(nh)}</text>')
    for (a, b), nh in (((1, 1), "P100"), ((2, 2), ""), ((3, 5), "R | · CCR"), ((6, 6), "HR"), ((7, 7), "Looker·GS")):
        if not nh:
            continue
        x0, x1 = cota(a)[0] - 3, cota(b)[1] + 3
        o.append(f'<rect class="vz vz-asis" x="{x0}" y="{yt0}" width="{x1 - x0}" height="{yt1 - yt0}" rx="5"/>')
        o.append(f'<text class="vt vt-a" x="{x0 + 6}" y="{yt0 + 14}">{E(nh)}</text>')
    # ── vùng NẠP · SỔ · RA: hai nửa ──
    for v, (n1, _n2, y0, y1) in VUNG.items():
        o.append(f'<rect class="vz vz-{v}" x="{C0[0] - 4}" y="{y0}" width="{xr - C0[0] + 4}" height="{y1 - y0}" rx="5"/>')
        o.append(f'<rect class="vz vz-asis" x="{xa}" y="{y0}" width="{W - 2 - xa}" height="{y1 - y0}" rx="5"/>')
    # ── dải màu của 4 agent: trải ngang nửa TO-BE, cùng màu với nhãn ở lề ──
    for k, (d, *_r) in AGENT.items():
        _v, y0, h, _nh = DAI[d]
        o.append(f'<rect class="ag-dai ag-dai-{k}" x="16" y="{y0 - 5}" width="{xr - 16}" height="{h + 10}" rx="6"/>')
    # ── dải chữ dọc tên vùng (lề trái) ──
    for nh, y0, y1 in (("NGUỒN", yt0, yt1),) + tuple((n1, y0, y1) for n1, _n2, y0, y1 in VUNG.values()):
        ym = (y0 + y1) / 2
        o.append(f'<text class="vr" x="10" y="{ym}" text-anchor="middle" transform="rotate(-90 10 {ym})">{E(nh)}</text>')
    # ── rail: nhãn dải · agent ──
    for d, (_v, y0, h, nh) in DAI.items():
        if not nh:
            continue
        if d in AG_THEO_DAI:
            k = AG_THEO_DAI[d]
            o.append(f'<g class="pp-nhan ag-nhan" data-id="h:{k}" tabindex="0" role="button" aria-label="{E(AGENT[k][2])}">'
                     f'<rect class="ag-the ag-the-{k}" x="20" y="{y0 + 1}" width="76" height="{h - 2}" rx="5"/>'
                     f'<text class="ag-so ag-so-{k}" x="25" y="{y0 + 13}">{E(AGENT[k][1])} ▸</text>'
                     f'<text class="ag-ten" x="25" y="{y0 + 25}">{E(AG_NGAN[k])}</text>'
                     f'<text class="ag-mh ag-so-{k}" x="25" y="{y0 + 36}">{E(AG_MO_HINH[k])}</text></g>')
            continue
        o.append(f'<text class="br" x="22" y="{y0 + h / 2 + 4}">{E(nh)}</text>')
    # ── ranh giới FLS (chỉ nửa TO-BE: bên AS-IS mọi thứ đều ở Sheets) ──
    yr = yt1 + 10
    o.append(f'<line class="ranh" x1="{C0[0] - 4}" y1="{yr}" x2="{xr}" y2="{yr}"/>')
    o.append(f'<text class="rt" x="22" y="{yr + 4}">ranh FLS</text>')
    o.append(f'<text class="rt" x="22" y="{yr + 15}">chỉ-đọc</text>')
    # ── khung phương pháp trong vùng NẠP (không chữ: tên PP đã ở đầu cột) ──
    for (a, b), d0, d1 in (((2, 5), "c1", "c2"), ((6, 6), "c1", "c2"), ((7, 7), "c1", "c2"),
                           ((1, 5), "c3", "c4"), ((6, 6), "c3", "c4"), ((7, 7), "c3", "c4")):
        x0, x1 = cot(a)[0] - 3, cot(b)[1] + 3
        y0, y1 = DAI[d0][1] - 4, DAI[d1][1] + DAI[d1][2] + 4
        o.append(f'<rect class="khung-pp1" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="5"/>')
    ve_gon(o, HOP, TEN, HOP_THEO)
    for k, (_cha, chip, ten_c, _b, tv) in AGENT_CON.items():    # chip agent con, mép trên-phải hộp MAPPING
        h = HOP_THEO[tv[0]]
        bw = 9 + 5.6 * len(chip)
        bx = h.x[1] - 6 - bw
        o.append(f'<g class="pp-nhan ag-chip" data-id="h:{k}" tabindex="0" role="button" aria-label="{E(ten_c)}">'
                 f'<rect class="ag-the ag-the-ag3 ag-chip-n" x="{bx:.1f}" y="{h.y[0] - 7}" width="{bw:.1f}" height="13" rx="6.5"/>'
                 f'<text class="ag-so ag-so-ag3 ag-chip-t" x="{bx + bw / 2:.1f}" y="{h.y[0] + 2.5}" text-anchor="middle">{E(chip)}</text></g>')
    ve_gon(o, HOP_A, TEN_A, HOP_A_THEO)
    o.append('</svg>')
    return "\n".join(o)


def ve_gon(o: list[str], hops: list, tens: list, ht: dict) -> None:
    """Vẽ GỌN cho hình 1: tên + một dòng; nhãn máy/người thành vạch màu mép trái; huy hiệu nhỏ trên mép."""
    for t in tens:
        x1, y1, x2, y2 = doan(t, ht)
        if t.x is not None:
            y2 += 1 if y2 < y1 else -1
        else:
            x2 += -1 if x2 > x1 else 1
        a, b = ht[t.tu], ht[t.toi]
        nhan = f"Mũi tên {t.ma}: {a.ten} → {b.ten}"
        o.append(f'<g class="ten-g" data-id="t:{t.ma}" data-tt="{t.tt}" data-comment-target tabindex="0" '
                 f'role="button" aria-label="{E(nhan)}"><title>{E(t.ma + " · " + t.cai_gi)}</title>')
        o.append(f'<line class="hit" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
        o.append(f'<line class="ten ten-{t.tt}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'marker-end="url(#m{t.tt})"/>')
        if t.x is not None:
            o.append(f'<text class="tl" x="{x1 + 3:.1f}" y="{(y1 + y2) / 2 + 3.5:.1f}">{t.ma}</text>')
        else:
            o.append(f'<text class="tl" x="{(x1 + x2) / 2:.1f}" y="{y1 - 3:.1f}" text-anchor="middle">{t.ma}</text>')
        o.append('</g>')
    for h in hops:
        x0, x1 = h.x
        y0, y1 = h.y
        ten, dong = NGAN[h.ma]
        meo = [h.ten] + list(h.dong)
        if h.luong:
            meo.append("luồng: " + " → ".join(f"{i + 1}. {b}" for i, b in enumerate(h.luong)))
        if h.goc:
            meo.append("gộp từ AS-IS: " + " · ".join(ASIS_GOC["hop"][m]["ten"] for m in h.goc))
        o.append(f'<g class="hop hop-{h.loai} tt-{h.tt}" data-id="h:{h.ma}" data-tt="{h.tt}" data-comment-target tabindex="0" '
                 f'role="button" aria-label="{E(h.ten)} ({LOAI_CHU[h.loai]}, {TT_CHU[h.tt]})"><title>{E(chr(10).join(meo))}</title>'
                 f'<rect class="khung" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="{7 if h.loai == "o" else 3}"/>')
        if h.nm:
            lop = {"MÁY": "may", "NGƯỜI": "nguoi", "NGƯỜI+MÁY": "ca"}[h.nm[1]]
            o.append(f'<rect class="nms nms-{lop}" x="{x0 + 1.5}" y="{y0 + 1.5}" width="4" height="{y1 - y0 - 3}" rx="1"/>')
        if h.tang:
            o.append(f'<text class="g0" x="{x0 + 6}" y="{y0 + 12.5}">{E(ten)}</text>')
        else:
            nho = h.dai in ("A0", "B0", "G0", "H0")
            ty = y0 + (14 if nho else 16)
            o.append(f'<text class="{"g0" if h.loai == "o" else "g1"}" x="{x0 + 9}" y="{ty}">{E(ten)}</text>')
            if dong:
                o.append(f'<text class="{"g2n" if h.tt == "n" else "g2"}" x="{x0 + 9}" y="{ty + 14}">{E(dong)}</text>')
        hy = []
        if h.huy:
            hy.append(("huy", "huyg", "·".join(h.huy)))
        if h.tay:
            hy.append(("tay", "tayt", "TAY"))
        bx = x0 + 6
        for cl, clt, chu in hy:
            bw = 9 + 5.1 * len(chu)
            o.append(f'<rect class="{cl}" x="{bx:.1f}" y="{y0 - 6}" width="{bw:.1f}" height="11" rx="5.5"/>'
                     f'<text class="{clt}" x="{bx + bw / 2:.1f}" y="{y0 + 2.5}" text-anchor="middle">{E(chu)}</text>')
            bx += bw + 3
        if h.goc and any(ASIS_GOC["hop"][m].get("issue") for m in h.goc):
            o.append(f'<circle class="van" cx="{x1 - 9}" cy="{y0}" r="6"/><text class="vant" x="{x1 - 9}" y="{y0 + 3.5}" text-anchor="middle">!</text>')
        o.append('</g>')


def ve_phan(o: list[str], hops: list, tens: list, ht: dict) -> None:
    """Vẽ mũi tên (trước) rồi hộp (sau) — dùng chung cho hình chính và hình phóng to."""
    for t in tens:
        x1, y1, x2, y2 = doan(t, ht)
        if t.x is not None:
            y2 += 1 if y2 < y1 else -1
        else:
            x2 += -1 if x2 > x1 else 1
        a, b = ht[t.tu], ht[t.toi]
        nhan = f"Mũi tên {t.ma}: {a.ten} → {b.ten}"
        o.append(f'<g class="ten-g" data-id="t:{t.ma}" data-tt="{t.tt}" data-comment-target tabindex="0" '
                 f'role="button" aria-label="{E(nhan)}">')
        o.append(f'<line class="hit" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
        o.append(f'<line class="ten ten-{t.tt}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'marker-end="url(#m{t.tt})"/>')
        if t.x is not None:
            o.append(f'<text class="tl" x="{x1 + 4:.1f}" y="{(y1 + y2) / 2 + 4:.1f}">{t.ma}</text>')
        else:
            o.append(f'<text class="tl" x="{(x1 + x2) / 2:.1f}" y="{y1 - 4:.1f}" text-anchor="middle">{t.ma}</text>')
        o.append('</g>')
    for h in hops:
        x0, x1 = h.x
        y0, y1 = h.y
        cls = f"hop hop-{h.loai} tt-{h.tt}"
        o.append(f'<g class="{cls}" data-id="h:{h.ma}" data-tt="{h.tt}" data-comment-target tabindex="0" '
                 f'role="button" aria-label="{E(h.ten)} ({LOAI_CHU[h.loai]}, {TT_CHU[h.tt]})">'
                 + (f'<title>{E(h.ten)} — luồng: ' + E(" → ".join(f"{i + 1}. {b}" for i, b in enumerate(h.luong)))
                    + '</title>' if h.luong else '')
                 + f'<rect class="khung" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
                 f'rx="{9 if h.loai == "o" else 3}"/>')
        nho = h.loai == "o"
        ty = y0 + (14 if nho else 16)
        o.append(f'<text class="{"to" if nho else "t1"}" x="{x0 + 8}" y="{ty}">{E(h.ten)}</text>')
        for i, d in enumerate(h.dong):
            cl = "t2n" if "đề xuất" in d else ("t2o" if nho else "t2")
            o.append(f'<text class="{cl}" x="{x0 + 8}" y="{ty + (13 if nho else 15) * (i + 1)}">{E(d)}</text>')
        if h.mono:
            o.append(f'<text class="t3" x="{x0 + 8}" y="{y1 - 8}">{E(h.mono)}</text>')
        if h.nm:
            nh = h.nm[1]
            bw = 10 + 6.6 * len(nh)
            lop = {"MÁY": "may", "NGƯỜI": "nguoi", "NGƯỜI+MÁY": "ca"}[nh]
            o.append(f'<rect class="nm nm-{lop}" x="{x0 + 6}" y="{y0 - 12}" width="{bw:.1f}" height="12" rx="3"/>'
                     f'<text class="nmt nmt-{lop}" x="{x0 + 6 + bw / 2:.1f}" y="{y0 - 3}" text-anchor="middle">{E(nh)}</text>')
        if h.huy:
            s = "·".join(h.huy)
            bw = 10 + 7.2 * len(s)
            bx = x1 - 6 - bw
            o.append(f'<rect class="huy" x="{bx:.1f}" y="{y0 - 7}" width="{bw:.1f}" height="14" rx="7"/>'
                     f'<text class="huyt" x="{bx + bw / 2:.1f}" y="{y0 + 3.5}" text-anchor="middle">{E(s)}</text>')
        o.append('</g>')


def svg_m() -> str:
    o = [f'<svg viewBox="0 0 {WM} {HM}" role="group" aria-label="Mapping PP (1) phóng to: bấm một hộp hay mũi tên để xem chi tiết">']
    o.append('<rect class="vz vz-C" x="124" y="6" width="1092" height="588" rx="6"/>')
    for d, (_v, y0, h, nh) in DAI_M.items():
        o.append(f'<text class="br" x="10" y="{y0 + h / 2 + 4}">{E(nh)}</text>')
    o.append(f'<text class="vt vt-pp1" x="{cotm(1)[0]}" y="{DAI_M["m5"][1] - 10}">VÒNG CỘNG DỒN: m14 đưa luật ứng viên lên lại bảng luật</text>')
    ve_phan(o, HOP_M, TEN_M, HOP_M_THEO)
    o.append('</svg>')
    return "\n".join(o)


def svg_n() -> str:
    o = [f'<svg viewBox="0 0 {WN} {HN}" role="group" aria-label="PP (3) phóng to: bấm một hộp hay mũi tên để xem chi tiết">']
    o.append(f'<rect class="vz vz-C" x="124" y="6" width="{WN - 128}" height="588" rx="6"/>')
    for d, (_v, y0, h, nh) in DAI_N.items():
        o.append(f'<text class="br" x="10" y="{y0 + h / 2 + 4}">{E(nh)}</text>')
    ve_phan(o, HOP_N, TEN_N, HOP_N_THEO)
    o.append('</svg>')
    return "\n".join(o)


# ───────────────────────────── bảng ─────────────────────────────
def pill(co_ma: str) -> str:
    c = "ok" if co_ma.startswith("✅") else ("mid" if co_ma.startswith("◐") else
                                              ("ext" if co_ma.startswith("ngoài") else "no"))
    return f'<span class="pill {c}">{E(co_ma)}</span>'


def bang_ten() -> str:
    o = ['<div class="scroll"><table class="arrows">',
         '<thead><tr><th colspan="2" class="sup">Mũi tên</th><th colspan="3" class="sup">Dữ liệu chảy</th>'
         '<th colspan="2" class="sup">Kiểm soát</th></tr>',
         '<tr><th>#</th><th>từ → tới</th><th>cái gì chảy</th><th>khoá</th><th>bản số</th>'
         '<th>cổng trên mũi tên</th><th>hôm nay</th></tr></thead><tbody>']
    cu1 = cu2 = None
    for t in sorted(TEN, key=lambda t: (t.nhom, TEN.index(t))):
        if t.nhom[0] != cu1:
            cu1 = t.nhom[0]
            o.append(f'<tr class="b1"><th colspan="7">{E(NHOM[cu1])}</th></tr>')
        if t.nhom != cu2:
            cu2 = t.nhom
            o.append(f'<tr class="b2"><th colspan="7">{E(NHOM[cu2])}</th></tr>')
        a, b = HOP_THEO[t.tu], HOP_THEO[t.toi]
        o.append(f'<tr class="chon" data-ref="t:{t.ma}" data-comment-target tabindex="0">'
                 f'<td class="id"><i class="ln ln-{t.tt}"></i>{t.ma}</td>'
                 f'<td>{E(a.ten)} → {E(b.ten)}</td><td>{E(t.cai_gi)}</td><td><code>{E(t.khoa)}</code></td>'
                 f'<td>{E(t.ban_so)}</td><td>{E(t.cong)}</td><td>{pill(t.co_ma)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


VUNG_BANG = [("A", ("A0", "A1")), ("B", ("B0", "B1")), ("G", ("G0", "G1")), ("H", ("H0", "H1")), ("C", ("c1", "c2", "c3", "c4", "c5")),
             ("D", ("d1", "d2")), ("E", ("e1",))]
NHAN_DAI_BANG = {"A0": "ai sinh ra", "A1": "sổ nguồn", "B0": "ai sinh ra", "B1": "sổ nguồn",
                 "G0": "ai sinh ra", "G1": "sổ nguồn", "H0": "ai sinh ra", "H1": "sổ nguồn"}


def vao_ra() -> tuple[dict, dict]:
    vao: dict[str, list[str]] = {h.ma: [] for h in HOP}
    ra: dict[str, list[str]] = {h.ma: [] for h in HOP}
    for t in TEN:
        ra[t.tu].append(t.ma)
        vao[t.toi].append(t.ma)
    return vao, ra


NHOM_LUONG = [
    ("Bốn agent và ba phương pháp", [("Bốn agent · FLS · NẠP", ["ag1", "ag2", "ag3", "ag4"]),
                                     ("Agent 3 · Filter Fulfill & Adjust tách ba agent con — mỗi phương pháp một con", ["ag3a", "ag3b", "ag3c"]),
                                     ("Ba phương pháp · luồng trọn từ nguồn tới sổ", ["pp1", "pp2", "pp3"])]),
    ("FLS · NẠP", [("① KHAI & CHỤP", ["anhFPS", "khai", "anhTien", "anhHR", "anhNT"]),
                   ("② DỰNG", ["dLenh", "dTien", "dHR", "dNT"]),
                   ("③ MAPPING", ["ghep", "ghep2", "ghep3"]),
                   ("④–⑤ SOÁT & GHI", ["soat", "soat2", "soat3", "ghiNap"])]),
    ("FLS · SỔ", [("⑥ SỔ GỐC", ["loai", "soITL", "lopSua", "ghiTay"]),
                  ("⑦ HIỆU LỰC", ["kiem", "hieuLuc"])]),
    ("ĐẦU RA", [("", ["f03", "f01", "f02", "xuat"])]),
    ("Hình phóng to", [("Hình 2 · mapping PP (1)", ["mMap", "mSuy", "mXN", "mLuat"]),
                       ("Hình 3 · PP (3)", ["nTach", "nMap", "nAlloc", "nKiem"])]),
]


def bang_luong() -> str:
    gan_luong()
    tat_ca = {h.ma: h for h in HOP + HOP_M + HOP_N}
    o = ['<div class="scroll"><table class="luong-bang">',
         '<thead><tr><th>hộp</th><th>luồng xử lý tổng quan</th><th>hôm nay</th></tr></thead><tbody>']
    for nhom, con in NHOM_LUONG:
        o.append(f'<tr class="b1"><th colspan="3">{E(nhom)}</th></tr>')
        for ten_con, mas in con:
            if ten_con:
                o.append(f'<tr class="b2"><th colspan="3">{E(ten_con)}</th></tr>')
            for ma in mas:
                if ma in AGENT:
                    _d, _n, ten, buoc, _tv = AGENT[ma]
                    tt = "agent · bước sau: AP → Flip eval"
                elif ma in AGENT_CON:
                    _c, _n, ten, buoc, _tv = AGENT_CON[ma]
                    tt = "agent con · thuộc Agent 3 · Filter Fulfill & Adjust"
                elif ma in PP_LUONG:
                    ten, buoc, _tv = PP_LUONG[ma]
                    tt = "GĐ1 phải dựng"
                else:
                    h = tat_ca[ma]
                    ten, buoc, tt = h.ten, h.luong, TT_CHU[h.tt]
                li = "".join(f"<li>{E(b)}</li>" for b in buoc)
                o.append(f'<tr class="chon" data-ref="h:{ma}" data-comment-target tabindex="0"><td><b>{E(ten)}</b></td>'
                         f'<td><ol>{li}</ol></td><td>{E(tt)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


# ── §1 · đọc ngang từng lớp: TO-BE ↔ AS-IS ↔ khác ở đâu (danh sách gap đầu tiên của audit) ──
KHAC_LOP = {
    "A0": "Người vẫn gõ ở cả hai bên; FLS không thay chỗ gõ. Bên AS-IS, CA gõ Reference number SAU khi chi, giờ không cố định; người nhập số dư CCR chưa xác định.",
    "A1": "AS-IS đọc phiếu Entry Data P100; TO-BE đọc thẳng sổ cái PM · PC của FPS. Sao kê, sổ quỹ, CCR, nguồn nền tảng (Looker GI · OMC + Gsheet SC · PS): cùng nguồn ở hai bên.",
    "c1": "AS-IS: người bấm GScript duỗi / gom; Mapping Master là bảng tra sửa tại chỗ. TO-BE: nhịp S1 chụp theo bản khai, bản khai có version, owner ký.",
    "c2": "AS-IS: đẩy tay sang A-CCR (đang trễ 19 ngày, thiếu 377 dòng — mô tả luồng người N3). TO-BE: DỰNG từ ảnh, đủ hai vế, gắn pháp nhân TK.",
    "c3": "AS-IS: VLOOKUP Reference number chỉ lấy dòng đầu, mã trùng bị bỏ qua không báo; người nhận ra giao dịch nhờ đọc Diễn giải. TO-BE: Σ line = tiền, N×M để người; máy chưa đọc Diễn giải (QĐ-ITL-92).",
    "c4": "AS-IS: người soát DIF bằng mắt trên CCR. TO-BE: SOÁT số dư ngày = CCR (DIF = 0) từng TK từng ngày — hôm nay máy mới chỉ đọc CCR.",
    "c5": "AS-IS: IMPORTRANGE cột A–Q, hai sổ (ITL · H1000). TO-BE: một lượt nạp ghi trong một giao dịch cho cả 3 PP.",
    "d1": "AS-IS: kế toán điền tay cột R–AT, ô bỏ trống tự nhận giá trị mặc định. TO-BE: lớp sửa chỉ-thêm, mỗi sửa có actor và nhật ký.",
    "d2": "AS-IS: ITL Ledge Final đè ô, H1000 là sổ thứ hai. TO-BE: một sổ hiệu lực = sổ gốc + lớp sửa.",
    "e1": "AS-IS: Report General Ledger, in CCR ký tháng một lần. TO-BE: F01–F03 + XUẤT báo cáo daily vào CCR.",
}


def bang_lop() -> str:
    o = ['<h3>Đọc ngang từng lớp — TO-BE · AS-IS · khác ở đâu</h3>',
         '<div class="scroll"><table class="lop"><thead><tr><th>lớp</th><th>TO-BE (trái)</th><th>AS-IS (phải)</th><th>khác ở đâu</th></tr></thead><tbody>']
    for d, nh in (("A0", "ai sinh ra"), ("A1", "sổ nguồn")) + tuple((d, DAI[d][3]) for d in ("c1", "c2", "c3", "c4", "c5", "d1", "d2", "e1")):
        dais = {d} | ({"B0", "G0", "H0"} if d == "A0" else {"B1", "G1", "H1"} if d == "A1" else set())
        tb = " · ".join(NGAN[h.ma][0] for h in HOP if h.dai in dais)
        ai = " · ".join(NGAN[h.ma][0] for h in HOP_A if h.dai == d)
        o.append(f'<tr><td>{E(nh)}</td><td>{E(tb)}</td><td>{E(ai)}</td><td>{E(KHAC_LOP[d])}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


# ═════════════════ §8 · CHI PHÍ SERVER ↔ MÔ HÌNH MỞ (owner 06/11) ═════════════════
# ⚠ Mọi con số tiền dưới đây là GIÁ CÔNG BỐ tra ngày 06/11/2026 (nguồn ở cuối §8) nhân với GIẢ ĐỊNH khối lượng
#   — ⛔ chưa đo trên FLS. Tính bằng máy ở đây để bảng và lời văn ⛔ lệch nhau (Đ4: mỗi số nói nó đếm gì).
TOK_VAO, TOK_RA = 1000, 300           # token / dòng cần mô hình (giả định: luật + ngữ cảnh ~1.000 vào, ~300 ra gồm suy nghĩ)
KHOI_LUONG = (10_000, 50_000)         # dòng cần mô hình / tháng — 2 kịch bản, ⛔ chưa đo
GIA_API = {                           # $ / 1 triệu token (vào, ra) — bảng giá Anthropic, bộ nhớ đệm 06/10/2026
    "Claude Haiku 5.5": (0.10, 0.50), "Claude Sonnet 5.5": (2.00, 10.00), "Claude Opus 5.5": (4.00, 20.00)}
GIAM_LO = 0.5                         # Message Batches API: −50 %
GPU_L40S = (0.79, 0.99)               # $ / giờ thuê theo nhu cầu (RunPod · Lambda, 2026)
GPU_H100 = (2.01, 3.99)               # $ / giờ, nhà cung cấp chuyên GPU; hyperscaler $10–12
GIO_THANG = 730
LORA_LUOT = (2, 60)                   # $ tính toán cho MỘT lượt LoRA mô hình 8B (vài–10 giờ GPU)
LORA_SO_LUOT = (1, 10)                # số lượt thử tới khi đạt


def usd(x: float) -> str:
    if x >= 100:
        return f"${x:,.0f}".replace(",", ".")
    return f"${x:.3f}".replace(".", ",") if x < 1 else f"${x:.2f}".replace(".", ",")


def tp(x: float) -> str:
    """số thập phân kiểu Việt: 0,79 — ⛔ trộn 0.79 với 0,79 trên cùng trang."""
    return f"{x:g}".replace(".", ",")


def so(n: float) -> str:
    return f"{n:,.0f}".replace(",", ".")


def gia_1000(model: str, lo: bool = True) -> float:
    vao, ra = GIA_API[model]
    g = (TOK_VAO * vao + TOK_RA * ra) / 1000   # $ / 1.000 dòng
    return g * (GIAM_LO if lo else 1)


def bang_chi_phi() -> str:
    n1, n2 = KHOI_LUONG
    gpu_ngay = tuple(30 * g for g in GPU_L40S)                 # lô 1 giờ/ngày
    gpu_247 = tuple(GIO_THANG * g for g in GPU_L40S)
    h100_247 = tuple(GIO_THANG * g for g in GPU_H100)
    lora = (LORA_LUOT[0] * LORA_SO_LUOT[0], LORA_LUOT[1] * LORA_SO_LUOT[1])
    hoa_von_sonnet = gpu_247[0] / gia_1000("Claude Sonnet 5.5") * 1000
    hoa_von_haiku = gpu_247[0] / gia_1000("Claude Haiku 5.5") * 1000
    k = lambda t: f"{so(t[0])}–{so(t[1])}"   # noqa: E731
    o = ['''
<h2>§8 · Chi phí: máy chủ ↔ mô hình mã nguồn mở tự huấn luyện</h2>
<p class="note"><b>06/11:</b> đã chọn <b>Qwen 3.8-27B chạy local</b> cho các agent. Các dòng "mô hình mở 8B" dưới đây chỉ còn là mốc so sánh; giờ GPU cho mô hình 27B <b>chưa tính lại</b>.</p>
<p><b>Câu hỏi trước tiên là agent nào cần mô hình.</b> Ba trong bốn agent chạy bằng luật, không cần mô hình — chi phí của chúng chỉ là <b>máy chủ</b>. Mô hình chỉ có việc ở <b>phần dư</b> của các agent con của Agent 3 · Filter Fulfill &amp; Adjust: dòng còn ở L3 sau khi luật đã chạy hết.</p>
<div class="scroll"><table>
<thead><tr><th>agent</th><th>việc</th><th>cần mô hình?</th></tr></thead><tbody>
<tr class="chon" data-ref="h:ag1" tabindex="0"><td><b>Agent 1 · Collect_raw_data</b></td><td>đọc chỉ-đọc theo bản khai, ghi ảnh</td><td>không — luật</td></tr>
<tr class="chon" data-ref="h:ag2" tabindex="0"><td><b>Agent 2 · Generate Group Ledger (ITL raw)</b></td><td>đặt kiểu, canon 36 trường, content_key</td><td>không — luật</td></tr>
<tr class="chon" data-ref="h:ag3a" tabindex="0"><td><b>Agent 3.1 · Filter Fulfill &amp; Adjust · PP (1)</b></td><td>Reference No + Σ tiền → L1 · L2 · L3</td><td>L1 · L2: không. <b>L3: có thể</b> — suy diễn loại giao dịch từ diễn giải sao kê (vòng cộng dồn, hình 2)</td></tr>
<tr class="chon" data-ref="h:ag3b" tabindex="0"><td><b>Agent 3.2 · Filter Fulfill &amp; Adjust · PP (2)</b></td><td>nối dòng lương H1000 với bank theo Số CT</td><td>không — tra khoá + phép cộng</td></tr>
<tr class="chon" data-ref="h:ag3c" tabindex="0"><td><b>Agent 3.3 · Filter Fulfill &amp; Adjust · PP (3)</b></td><td>nhận diện giao dịch OMC · GI · SC · PS</td><td><b>có thể</b> — khi từ khoá / vendor không đủ nhận diện</td></tr>
<tr class="chon" data-ref="h:ag4" tabindex="0"><td><b>Agent 4 · Auditor (Compounding Loop)</b></td><td>9 luật · Σ · DIF CCR = 0</td><td>không — kiểm phải tất định</td></tr>
</tbody></table></div>
<h3>Giá đơn vị (công bố, tra 06/11/2026)</h3>
<div class="scroll"><table>
<thead><tr><th>khoản</th><th>giá</th><th>ghi chú</th></tr></thead><tbody>''']
    for m, (vao, ra) in GIA_API.items():
        o.append(f'<tr><td>API {E(m)}</td><td>${tp(vao)} vào · ${tp(ra)} ra / 1 triệu token</td>'
                 f'<td>gửi theo lô (Batches API) giảm 50% ⇒ <b>{usd(gia_1000(m))}</b> / 1.000 dòng</td></tr>')
    o.append(f'<tr><td>thuê GPU L40S (48 GB, đủ chạy mô hình mở 7–8B)</td><td>${tp(GPU_L40S[0])}–{tp(GPU_L40S[1])} / giờ</td><td>RunPod · Lambda, theo nhu cầu</td></tr>')
    o.append(f'<tr><td>thuê GPU H100</td><td>${tp(GPU_H100[0])}–{tp(GPU_H100[1])} / giờ</td><td>nhà cung cấp chuyên GPU; hyperscaler $10–12; giá đang <b>tăng</b> trong 2026</td></tr>')
    o.append(f'<tr><td>một lượt LoRA mô hình mở 8B</td><td>${LORA_LUOT[0]}–{LORA_LUOT[1]} tiền GPU</td><td>vài tới ~10 giờ GPU tuỳ số mẫu; tốn chủ yếu ở chạy lại và giờ máy rảnh</td></tr>')
    o.append('</tbody></table></div>')
    o.append(f'''<h3>Chi phí tháng theo phương án — phần mô hình, cộng thêm máy chủ FLS</h3>
<p class="ghichu">Giả định (⛔ chưa đo): mỗi dòng cần mô hình ≈ {so(TOK_VAO)} token vào + {TOK_RA} token ra; {so(n1)} hoặc {so(n2)} dòng / tháng. Máy chủ FLS (PostgreSQL + Python) phương án nào cũng phải có, nên không cộng vào cột dưới.</p>''')
    o.append(f'<div class="scroll"><table><thead><tr><th>phương án</th><th>một lần</th><th>/ tháng @ {so(n1)} dòng</th>'
             f'<th>/ tháng @ {so(n2)} dòng</th><th>dữ liệu rời công ty?</th><th>đánh đổi</th></tr></thead><tbody>')
    o.append('<tr><td><b>⓪ Chỉ luật + vòng cộng dồn</b> (không mô hình)</td><td>—</td><td>$0</td><td>$0</td><td>không</td><td>dòng L3 chưa có luật ở lại hàng chờ cho người</td></tr>')
    for m in GIA_API:
        g = gia_1000(m)
        o.append(f'<tr><td>API {E(m)}, gửi theo lô</td><td>—</td><td>{usd(g * n1 / 1000)}</td><td>{usd(g * n2 / 1000)}</td>'
                 f'<td><b>có</b> — diễn giải sao kê ra API ngoài</td><td>không giữ máy; chất lượng tiếng Việt phải đo</td></tr>')
    o.append(f'<tr><td>Mô hình mở 8B tự chạy, <b>không</b> huấn luyện — GPU L40S theo lô 1 giờ/ngày</td><td>công dựng</td>'
             f'<td colspan="2">${k(gpu_ngay)} cho 1 giờ GPU/ngày — đủ bao nhiêu dòng / giờ thì ⛔ chưa đo</td><td>không</td><td>người vận hành GPU; mô hình chưa quen chữ kế toán Việt</td></tr>')
    o.append(f'<tr><td>Như trên, GPU L40S chạy 24/7 (trả lời ngay mỗi nhịp)</td><td>công dựng</td><td colspan="2">${k(gpu_247)}</td><td>không</td><td>trả tiền cả giờ rảnh</td></tr>')
    o.append(f'<tr><td><b>Huấn luyện mô hình mở 8B (LoRA)</b> + tự chạy như trên</td><td>${k(lora)} tiền GPU ({LORA_SO_LUOT[0]}–{LORA_SO_LUOT[1]} lượt) + <b>công gắn nhãn</b></td>'
             f'<td colspan="2">như dòng tự chạy: ${k(gpu_ngay)} theo lô · ${k(gpu_247)} 24/7</td><td>không</td><td>cần tập dòng L3 đã được kế toán xác nhận; huấn luyện lại khi luật / nguồn đổi</td></tr>')
    o.append(f'<tr><td>Tự chạy trên H100 24/7 (mô hình lớn hơn)</td><td>công dựng</td><td colspan="2">${k(h100_247)}</td><td>không</td><td>chỉ đáng khi 8B không đủ đúng</td></tr>')
    o.append('</tbody></table></div>')
    o.append(f'''<p class="note"><b>Điểm hoà vốn.</b> GPU L40S chạy 24/7 (từ ~{usd(gpu_247[0])}/tháng) chỉ rẻ hơn API Sonnet 5.5 gửi theo lô khi vượt <b>~{so(hoa_von_sonnet)} dòng/tháng</b>, và rẻ hơn API Haiku 5.5 gửi theo lô khi vượt <b>~{so(hoa_von_haiku)} dòng/tháng</b>. Sổ FLS hôm nay có 8.387 dòng tiền tất cả — phần cần mô hình chỉ là phần dư L3 của số ấy. ⇒ Ở khối lượng này, <b>tiền GPU không phải lý do chọn mô hình mở</b>; lý do thật (nếu có) là <b>dữ liệu không được rời công ty</b>.</p>''')
    o.append('''<p class="note"><b>Ba thứ không nằm trong bảng tiền:</b> ① <b>dữ liệu rời công ty</b> — diễn giải sao kê có tên người ~4,3–4,8% số ô (đo khi mở QĐ-ITL-128, <code>NFR-I13</code>); gửi ra API ngoài là quyết định của owner. ② <b>chất lượng chưa đo</b> — mô hình nào cũng phải chấm trên chính các dòng L3 kế toán đã xác nhận; vòng cộng dồn sinh ra tập này miễn phí, nó cũng là dữ liệu huấn luyện duy nhất cho phương án LoRA. ③ <b>người vận hành</b> — tự chạy GPU cần người giữ máy, cập nhật mô hình, canh hỏng; API thì không.</p>
<p><b>Đề xuất thứ tự:</b> GĐ1 chạy phương án ⓪ và <b>đo</b> số dòng L3 còn lại mỗi tháng. Khi có ≥ vài trăm dòng đã xác nhận: chấm thử API Haiku 5.5 và Sonnet 5.5 gửi theo lô trên tập ấy (vài đô). Chỉ tính huấn luyện mô hình mở khi owner chốt <b>dữ liệu không ra ngoài</b>, hoặc khối lượng vượt điểm hoà vốn ở trên.</p>
<p class="ghichu">Nguồn giá (tra 06/11/2026; giá đổi thường xuyên, xem lại trước khi chi): bảng giá API Anthropic (bộ nhớ đệm 06/10/2026, Batches −50%) ·
<a href="https://www.spheron.network/blog/h100-price-per-hour-2026/">Spheron · H100 2026</a> ·
<a href="https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison">IntuitionLabs · H100 15 nhà cung cấp</a> ·
<a href="https://gpu-cost.pages.dev/gpu/l40s/">gpu-cost · L40S</a> ·
<a href="https://deploybase.ai/articles/l40s-on-runpod-pricing-specs-how-to-rent">DeployBase · L40S RunPod</a> ·
<a href="https://www.techloy.com/fine-tuning-an-open-model-on-a-rented-gpu-what-an-hour-costs-in-2026/">Techloy · fine-tune trên GPU thuê 2026</a> ·
<a href="https://io.net/p/faq-how-much-does-it-cost-to-fine-tune-an-llm">io.net · chi phí fine-tune</a>. Nhiều nguồn là blog của nhà cho thuê GPU, có thể lạc quan.</p>''')
    return "\n".join(o)


# ═════════════════ markdown → HTML tối thiểu (bảng · tiêu đề · danh sách · trích) ═════════════════
# Repo ⛔ có thư viện `markdown`; hai tài liệu nhúng vào trang (kiểm TO-BE theo AS-IS · thẻ eval) chỉ dùng chừng này cú pháp.
import re as _re


def _md_dong(t: str) -> str:
    t = E(t, quote=False)
    t = _re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = _re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = _re.sub(r"(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])", r"<i>\1</i>", t)
    return t


def md_html(van: str, cap: int = 3) -> str:
    o: list[str] = []
    dong = van.splitlines()
    i = 0
    while i < len(dong):
        d = dong[i]
        if not d.strip():
            i += 1
            continue
        m = _re.match(r"^(#{1,4}) (.*)", d)
        if m:
            n = min(6, len(m.group(1)) + cap - 1)
            o.append(f"<h{n}>{_md_dong(m.group(2))}</h{n}>")
            i += 1
            continue
        if d.strip() == "---":
            o.append("<hr>")
            i += 1
            continue
        if d.startswith("|"):
            bang = []
            while i < len(dong) and dong[i].startswith("|"):
                bang.append(dong[i])
                i += 1
            hang = [[c.strip().replace("\x00", "|") for c in r.replace("\\|", "\x00").strip().strip("|").split("|")] for r in bang]
            hang = [r for r in hang if not all(_re.fullmatch(r":?-{2,}:?", c) for c in r)]
            o.append('<div class="scroll"><table><thead><tr>' + "".join(f"<th>{_md_dong(c)}</th>" for c in hang[0]) + "</tr></thead><tbody>")
            for r in hang[1:]:
                o.append("<tr>" + "".join(f"<td>{_md_dong(c)}</td>" for c in r) + "</tr>")
            o.append("</tbody></table></div>")
            continue
        if d.startswith("> "):
            k = []
            while i < len(dong) and dong[i].startswith(">"):
                k.append(dong[i][1:].strip())
                i += 1
            o.append('<p class="tin">' + " ".join(_md_dong(x) for x in k) + "</p>")
            continue
        if d.startswith("- "):
            o.append("<ul>")
            while i < len(dong) and dong[i].startswith("- "):
                o.append(f"<li>{_md_dong(dong[i][2:])}</li>")
                i += 1
            o.append("</ul>")
            continue
        k = []
        while i < len(dong) and dong[i].strip() and not _re.match(r"^(#{1,4} |\||> |- |---$)", dong[i]):
            k.append(dong[i])
            i += 1
        o.append("<p>" + " ".join(_md_dong(x) for x in k) + "</p>")
    return "\n".join(o)


def bang_kiem_asis() -> str:
    van = (GOC / "docs/ITL/02_BA/Artifacts/Kiem-TOBE-theo-ASIS.md").read_text(encoding="utf-8")
    van = van.split("\n", 1)[1]                      # bỏ tiêu đề cấp 1 — trang đặt tiêu đề riêng
    return ('<h2 id="kiem-asis">§1a · Kiểm TO-BE theo luồng AS-IS thực tế</h2>'
            '<p class="ghichu">Nhúng nguyên từ <code>docs/ITL/02_BA/Artifacts/Kiem-TOBE-theo-ASIS.md</code> lúc sinh trang — sửa tài liệu ấy rồi sinh lại, ⛔ sửa ở đây.</p>'
            + md_html(van, cap=3))


# ═════════════════ §9 · FLEET EVAL — sơ đồ quy trình + bốn thẻ (owner 06/11: "đưa sơ đồ vào artifact này") ═════════════════
# Nguồn sự thật: docs/ITL/05_FleetEval/grid-spec.json (render bằng skill plan-fleet-eval) và eval-cards/*.md.
# Trang chỉ NHÚNG grid.svg đã render — ⛔ vẽ lại tay, để sơ đồ ở đây và ở AP không lệch nhau.
FE_THU_MUC = GOC / "docs/ITL/05_FleetEval"
FE_THE = [   # (agent, phép kiểm, lỗi đáng sợ, đơn vị heatmap, đáp án, bar đề xuất)
    ("A3.1 · Filter Fulfill & Adjust · PP (1)", "a3-1-ref.eval.ghep-sai", "nối chắc chắn nhưng sai một PM line ⇒ HD/CDT1 sai mà kế toán tin",
     "phải nối A · B · C — phải để người D · E · F — L3 · ca chuyển", "ITL Ledge Final (AS-IS) + oracle",
     "0 nối sai trên nhóm phải-để-người; tổng ≤ v0"),
    ("A3.2 · Filter Fulfill & Adjust · PP (2)", "a3-2-luong.eval.noi-sai-dot", "ghi đợt sai không báo: tháng trùng / thiếu, Σ Có ≠ Σ Nợ",
     "NIS L1 · NIS L3 · COM L2 · INT · PIT — tháng trùng · thiếu · Σ lệch · sổ 2026", "~34 file H1000 đã adjust ↔ ITL (AS-IS)",
     "0 đợt lỗi bị ghi"),
    ("A3.3 · Filter Fulfill & Adjust · PP (3)", "a3-3-nen-tang.eval.chia-sai", "nối nhầm PE hoặc chia sai CDT1 ⇒ chi phí về sai chủ dự toán",
     "OMC · GI · SC · PS — trúng nhiều · trúng 0 · lệch kỳ · vendor mới", "PHÂN BỔ NỀN TẢNG (AS-IS) sau khi người gán nhãn",
     "0 sai trên ca cài sẵn; không bar tổng"),
    ("A4 · Auditor (Compounding Loop)", "a4-soat.eval.lot-chan", "bỏ lọt: lô đáng CHẶN được báo đạt ⇒ dòng sai vào sổ chỉ-thêm",
     "mất/thừa dòng · thiếu trường · định dạng/nguồn · số dư · ca chuyển", "lô đột biến dựng + lỗi thật (646 dòng mất, 31 mã float)",
     "0 bỏ lọt; báo động oan ≤ v0"),
]


AP_FE = "AP_FLS_FleetEval_v1.1.3_2026-11-06.html"     # bản AP nhúng nguyên vào trang 2 (F4)
FE_THE_TEP = ("a3-1-ref", "a3-2-luong", "a3-3-nen-tang", "a4-soat")


def bang_fleet_eval() -> str:
    svg_fe = (FE_THU_MUC / "grid.svg").read_text(encoding="utf-8")
    if "<svg" not in svg_fe:
        raise SystemExit("⛔ grid.svg hỏng — render lại bằng render_grid.py")
    if not (FE_THU_MUC / AP_FE).exists():
        raise SystemExit(f"⛔ thiếu {AP_FE}")
    vai = {"ag1": "WRITE · đọc nguồn", "ag2": "WRITE · chuẩn hoá dòng", "ag3": "WRITE · nối lệnh chi", "ag4": "JUDGE · kiểm kết quả của A2 · A3"}
    the = {"ag1": "phiên bản sau", "ag2": "phiên bản sau", "ag3a": "a3-1-ref.eval.ghep-sai", "ag3b": "a3-2-luong.eval.noi-sai-dot",
           "ag3c": "a3-3-nen-tang.eval.chia-sai", "ag4": "a4-soat.eval.lot-chan"}
    nguoi = {"ag1": "kế toán khai, owner ký · mỗi nguồn", "ag2": "kế toán xem trước lô F04 · mỗi lô",
             "ag3a": "kế toán ghép / sửa F01 · mỗi dòng hàng chờ", "ag3b": "⛔ chưa có (Q4)", "ag3c": "⛔ chưa có (Q4)",
             "ag4": "kế toán đọc biên bản F04 · mỗi lô"}
    o = ['''
<h2>F1 · Mỗi agent khác nhau ở đâu</h2>
<p>Năm agent <b>làm</b> (A1 · A2 · A3.1–A3.3) chạy <b>Qwen 3.8-27B</b>. Agent <b>kiểm</b> trong luồng (A4 · Auditor) chạy <b>gpt-oss-20b</b> — một mô hình khác họ, vì bộ kiểm cùng họ với thứ nó kiểm sẽ chấm dễ. Bộ chấm của fleet eval cũng phải khác mô hình của <b>chính</b> agent bị đo: A1–A3 chấm bằng gpt-oss-20b, còn A4 (đã là gpt-oss) chấm bằng Qwen. Không agent nào được chấm bằng mô hình của chính nó.</p>
<div class="scroll"><table>
<thead><tr><th>agent</th><th>vai</th><th>mô hình chạy</th><th>ai kiểm khi chạy thật</th><th>fleet eval chấm bằng</th><th>phép kiểm</th></tr></thead><tbody>''']
    for k in ("ag1", "ag2", "ag3a", "ag3b", "ag3c", "ag4"):
        cha = AGENT_CON[k][0] if k in AGENT_CON else k
        ten = AGENT_CON[k][2] if k in AGENT_CON else AGENT[k][2]
        mh, ch = AG_MO_HINH[cha], AG_CHAM[cha]
        lop = "mh-kiem" if mh != "Qwen 3.8-27B" else "mh-lam"
        o.append(f'<tr class="chon" data-ref="h:{k}" data-comment-target tabindex="0"><td><b>{E(ten)}</b></td><td>{E(vai[cha])}</td>'
                 f'<td><span class="pill {lop}">{E(mh)}</span></td><td>{E(nguoi[k])}</td>'
                 f'<td><span class="pill {"mh-lam" if ch.startswith("Qwen") else "mh-kiem"}">{E(ch)}</span></td><td><code>{E(the[k])}</code></td></tr>')
    o.append('''</tbody></table></div>
<p class="ghichu">Persona của fleet eval dùng cùng mô hình với bộ chấm của agent ấy, nhưng prompt riêng. Bản mã tất định hôm nay là <code>v0</code> — mốc "không tệ hơn" cho vòng LLM đầu của A3.1 và A4.</p>
<h2>F2 · Sơ đồ quy trình fleet eval</h2>
<figure class="diagram fe-hinh" id="hinh-fe">''')
    o.append(svg_fe)
    o.append('''<figcaption>Hình F2 — 4 dải · 6 agent, sinh từ <code>docs/ITL/05_FleetEval/grid-spec.json</code> bằng <code>render_grid.py</code> (kiểm: 0 lỗ). Viền liền = đang chạy · đứt = một phần · chấm = chưa chạy; màu nền ô người = độ nặng; cờ góc = hỏi mỗi mục (EACH) / mỗi phiên bản (VER). A3.2 và A3.3 ghi vào sổ <b>không qua người kiểm</b> — chỉ fleet eval chặn trước.</figcaption></figure>
<h2>F3 · Bốn thẻ eval</h2>
<p>Thẻ là hợp đồng: operator chạy đúng điều thẻ ghi, người duyệt soát vòng theo thẻ. Nguồn: <code>docs/ITL/05_FleetEval/eval-cards/</code> (nhúng nguyên lúc sinh trang).</p>''')
    chung = (FE_THU_MUC / "eval-cards/_chung.md").read_text(encoding="utf-8")
    o.append('<details class="the" open><summary>Phần chung của bốn thẻ</summary>' + md_html(chung.split("\n", 1)[1], cap=4) + '</details>')
    for t in FE_THE_TEP:
        van = (FE_THU_MUC / f"eval-cards/{t}.md").read_text(encoding="utf-8")
        tieu, than = van.split("\n", 1)
        o.append(f'<details class="the"><summary>{_md_dong(tieu.lstrip("# "))}</summary>' + md_html(than, cap=4) + '</details>')
    ap = (FE_THU_MUC / AP_FE).read_text(encoding="utf-8")
    than = ap[ap.index("<main>") + 6:ap.index("</main>")]
    than = than.replace("<h1>", '<h3 class="ap-h1">', 1).replace("</h1>", "</h3>", 1)
    o.append(f'''<h2 id="ap">F4 · Bản kế hoạch (AP) — nhúng nguyên trong trang này</h2>
<p class="ghichu">Nguồn: <code>docs/ITL/05_FleetEval/{AP_FE}</code> (khuôn skill <code>plan-fleet-eval</code>); trang chép phần thân lúc sinh — sửa file AP (bản mới) rồi sinh lại, ⛔ sửa ở đây. Mọi mục ở trạng thái <b>review</b>, chỉ owner ThuongCT đặt <i>agreed</i>.</p>
<div class="ap-nhung">''' + than + "</div>")
    return "\n".join(o)


NHOM_NM = [
    ("VÀO — nguồn đầu vào", [("Do hệ sinh (+ người): FPS · Looker / Gsheet nền tảng", ["soPM", "sont"]),
                             ("Do người nhập ở Google Sheets", ["saoke", "soquy", "ccr", "soluong"]),
                             ("Do người nhập ngay trong FLS", ["khai", "lopSua", "mLuat"])]),
    ("RA — đầu ra", [("", ["f01", "f02", "f03", "xuat"])]),
]


def bang_nm() -> str:
    gan_luong()
    tat_ca = {h.ma: h for h in HOP + HOP_M + HOP_N}
    lop = {"MÁY": "nm-may", "NGƯỜI": "nm-nguoi", "NGƯỜI+MÁY": "nm-ca"}
    o = ['<div class="scroll"><table>',
         '<thead><tr><th>hộp</th><th>máy / người</th><th>ai làm ra · ai nhận</th><th>rủi ro · cổng canh</th></tr></thead><tbody>']
    for nhom, con in NHOM_NM:
        o.append(f'<tr class="b1"><th colspan="4">{E(nhom)}</th></tr>')
        for ten_con, mas in con:
            if ten_con:
                o.append(f'<tr class="b2"><th colspan="4">{E(ten_con)}</th></tr>')
            for ma in mas:
                h = tat_ca[ma]
                _c, nh, ai, rr = h.nm
                o.append(f'<tr class="chon" data-ref="h:{ma}" data-comment-target tabindex="0"><td><b>{E(h.ten)}</b></td>'
                         f'<td><span class="pill {lop[nh]}">{E(nh)}</span></td><td>{E(ai)}</td><td>{E(rr)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


def bang_canh() -> str:
    vao, ra = vao_ra()
    o = ['<div class="scroll"><table class="audit">',
         '<thead><tr><th>hộp</th><th>loại · trạng thái</th><th>vào</th><th>ra</th><th>đối chiếu mã / tài liệu</th>'
         '</tr></thead><tbody>']
    for v, dais in VUNG_BANG:
        o.append(f'<tr class="b1"><th colspan="5">{E(TEN_VUNG[v])}</th></tr>')
        for d in dais:
            if len(dais) > 1:
                o.append(f'<tr class="b2"><th colspan="5">{E(NHAN_DAI_BANG.get(d) or DAI[d][3])}</th></tr>')
            for h in [h for h in HOP if h.dai == d]:
                kd = " · khởi bởi " + ", ".join(h.huy) if h.huy else ""
                o.append(f'<tr class="chon" data-ref="h:{h.ma}" data-comment-target tabindex="0">'
                         f'<td><b>{E(h.ten)}</b></td><td>{LOAI_CHU[h.loai]} · {TT_CHU[h.tt]}{E(kd)}</td>'
                         f'<td class="mono">{" ".join(vao[h.ma]) or "—"}</td>'
                         f'<td class="mono">{" ".join(ra[h.ma]) or "—"}</td><td>{E(h.doi_chieu)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


def du_lieu_js() -> str:
    vao, ra = vao_ra()
    hop = {h.ma: {"ten": h.ten, "loai": LOAI_CHU[h.loai], "tt": h.tt, "dong": list(h.dong), "mono": h.mono,
                  "huy": list(h.huy), "dc": h.doi_chieu, "vung": TEN_VUNG[DAI[h.dai][0]],
                  "dai": NHAN_DAI_BANG.get(h.dai) or DAI[h.dai][3], "vao": vao[h.ma], "ra": ra[h.ma],
                  "luong": list(h.luong), "nm": list(h.nm)}
           for h in HOP}
    for k, (_d, _n, ten_ag, buoc, tv) in AGENT.items():
        hop[k] = {"ten": ten_ag, "loai": f"agent · chạy {AG_MO_HINH[k]}", "tt": "b", "dong": [], "mono": "", "huy": [],
                  "dc": f"mô hình chạy: {AG_MO_HINH[k]} · fleet eval chấm bằng: {AG_CHAM[k]} · AP fleet eval v1.1.0 (trang 2)",
                  "vung": "FLS · NẠP · bốn agent",
                  "dai": f"{DAI[_d][3]} · {AG_NGAN[k]}", "vao": [], "ra": [], "luong": list(buoc), "thanh_vien": list(tv)}
    for k, (cha, _c, ten_c, buoc, tv) in AGENT_CON.items():
        hop[k] = {"ten": ten_c, "loai": f"agent con · chạy {AG_MO_HINH[cha]}", "tt": "b", "dong": [], "mono": "", "huy": [],
                  "dc": f"thuộc {AGENT[cha][2]} · mô hình chạy: {AG_MO_HINH[cha]} · fleet eval chấm bằng: {AG_CHAM[cha]}",
                  "vung": "FLS · NẠP · Agent 3 · Filter Fulfill & Adjust",
                  "dai": DAI[AGENT[cha][0]][3], "vao": [], "ra": [], "luong": list(buoc), "thanh_vien": list(tv)}
    for k, (ten_pp, buoc, tv) in PP_LUONG.items():
        hop[k] = {"ten": ten_pp, "loai": "phương pháp", "tt": "q", "dong": [], "mono": "", "huy": [],
                  "dc": "bình luận owner 04/11 trên hình", "vung": "Ba phương pháp xử lý", "dai": "luồng trọn",
                  "vao": [], "ra": [], "luong": list(buoc), "thanh_vien": list(tv)}
    for hops, tens, nv, dai in ((HOP_M, TEN_M, "Mapping PP (1) · phóng to", DAI_M),
                                (HOP_N, TEN_N, "PP (3) nền tảng · phóng to", DAI_N)):
        vm = {h.ma: [] for h in hops}
        rm = {h.ma: [] for h in hops}
        for t in tens:
            rm[t.tu].append(t.ma)
            vm[t.toi].append(t.ma)
        for h in hops:
            hop[h.ma] = {"ten": h.ten, "loai": LOAI_CHU[h.loai], "tt": h.tt, "dong": list(h.dong), "mono": h.mono,
                         "huy": list(h.huy), "dc": h.doi_chieu, "vung": nv,
                         "dai": dai[h.dai][3], "vao": vm[h.ma], "ra": rm[h.ma], "luong": list(h.luong),
                         "nm": list(h.nm)}
    ten = {t.ma: {"tu": t.tu, "toi": t.toi, "tt": t.tt, "cai_gi": t.cai_gi, "khoa": t.khoa, "ban_so": t.ban_so,
                  "cong": t.cong, "co_ma": t.co_ma, "nhom": NHOM[t.nhom[0]] + " · " + NHOM[t.nhom]}
           for t in TEN}
    for tens, nv in ((TEN_M, "Mapping PP (1) · phóng to"), (TEN_N, "PP (3) nền tảng · phóng to")):
        for t in tens:
            ten[t.ma] = {"tu": t.tu, "toi": t.toi, "tt": t.tt, "cai_gi": t.cai_gi, "khoa": t.khoa, "ban_so": t.ban_so,
                         "cong": t.cong, "co_ma": t.co_ma, "nhom": nv}
    va = {h.ma: [] for h in HOP_A}
    ra_a = {h.ma: [] for h in HOP_A}
    for t in TEN_A:
        ra_a[t.tu].append(t.ma)
        va[t.toi].append(t.ma)
    for h in HOP_A:
        g = ASIS_GOC["hop"]
        hop[h.ma] = {"ten": h.ten, "loai": "AS-IS · " + LOAI_CHU[h.loai], "tt": "a", "dong": [], "mono": "", "huy": [],
                     "dc": h.doi_chieu, "vung": "AS-IS", "dai": NHAN_DAI_BANG.get(h.dai) or DAI[h.dai][3],
                     "vao": va[h.ma], "ra": ra_a[h.ma], "luong": [], "nm": list(h.nm), "tay": h.tay,
                     "goc": [{"ten": g[m]["ten"], "loai": g[m]["loai"], "ai": g[m].get("ai", ""), "cach": g[m].get("cach", ""),
                              "buoc": g[m].get("buoc", ""), "file": g[m].get("file", ""), "issue": g[m].get("issue", ""),
                              "dong": g[m].get("dong", []), "luong": g[m].get("luong", "")} for m in h.goc]}
    for t in TEN_A:
        ten[t.ma] = {"tu": t.tu, "toi": t.toi, "tt": t.tt, "cai_gi": t.cai_gi, "khoa": t.khoa, "ban_so": t.ban_so,
                     "cong": t.cong, "co_ma": t.co_ma, "nhom": "AS-IS · mũi tên gốc " + " · ".join(t.goc)}
    s = json.dumps({"hop": hop, "ten": ten, "tt": TT_CHU}, ensure_ascii=False)
    return s.replace("</", "<\\/")


# ───────────────────────────── trang ─────────────────────────────
CSS = r"""
/* Bố cục: hình rộng 1420 trong khung cuộn riêng; khung chi tiết neo phải (điện thoại: neo đáy); chữ một cột; bảng gom 2 tầng theo luật vẽ voi. */
:root{
  --bg:#f6f7f5; --paper:#ffffff; --fg:#1c231f; --muted:#59645d; --line:#d3d9d4;
  --accent:#1f4e79; --accent-soft:#e2ebf4;
  --ok:#2e7d4f; --ok-soft:#dcefe3; --mid:#a86d12; --mid-soft:#fff0cf; --no:#7d8580; --no-soft:#eceeec;
  --prop:#2f62c9; --prop-soft:#e4ecfb; --sel:#c2410c;
  --ext:#f1ece2; --zc:#eaf0f6; --zd:#eaf3ed; --ze:#f3eef6; --box:#ffffff; --orig:#fdf6e6;
  --za:#f0eee8; --asis:#8a6a44;
  --ag1:#0f766e; --ag2:#6d28d9; --ag3:#c2410c; --ag4:#15803d;
  --sans:"IBM Plex Sans",system-ui,"Segoe UI",Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;
  --serif:"IBM Plex Serif",Georgia,serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#141815; --paper:#1c221f; --fg:#e5eae6; --muted:#a0aaa3; --line:#353d38;
  --accent:#8fb8e0; --accent-soft:#213041;
  --ok:#6fcf97; --ok-soft:#1d3729; --mid:#e2b45a; --mid-soft:#3a2f18; --no:#8d968f; --no-soft:#262b28;
  --prop:#86a8f0; --prop-soft:#1f2a44; --sel:#fb923c;
  --ext:#29251e; --zc:#1a222a; --zd:#1a271f; --ze:#251f29; --box:#222926; --orig:#2d281c; --za:#22211e; --asis:#cfa977; --ag1:#2dd4bf; --ag2:#a78bfa; --ag3:#fb923c; --ag4:#4ade80; color-scheme:dark }}
:root[data-theme="dark"]{
  --bg:#141815; --paper:#1c221f; --fg:#e5eae6; --muted:#a0aaa3; --line:#353d38;
  --accent:#8fb8e0; --accent-soft:#213041;
  --ok:#6fcf97; --ok-soft:#1d3729; --mid:#e2b45a; --mid-soft:#3a2f18; --no:#8d968f; --no-soft:#262b28;
  --prop:#86a8f0; --prop-soft:#1f2a44; --sel:#fb923c;
  --ext:#29251e; --zc:#1a222a; --zd:#1a271f; --ze:#251f29; --box:#222926; --orig:#2d281c; --za:#22211e; --asis:#cfa977; --ag1:#2dd4bf; --ag2:#a78bfa; --ag3:#fb923c; --ag4:#4ade80; color-scheme:dark }
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:15px/1.55 var(--sans);margin:0;
  padding-block:0 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:1800px;margin:0 auto} main > p,main > ul,main > ol,main > h2,main > h3{max-width:1100px}
body.co-khung main{margin-right:400px}
header.top{padding:28px 0 12px;border-bottom:2px solid var(--accent)}
h1{font:600 30px/1.2 var(--serif);margin:0 0 8px;text-wrap:balance}
h2{font:600 21px/1.25 var(--serif);margin:40px 0 10px;text-wrap:balance}
h3{font:600 16px/1.3 var(--sans);margin:22px 0 8px}
p,ul,ol{max-width:92ch}
.meta{color:var(--muted);font-size:13.5px}
.meta b{color:var(--fg)}
code{font-family:var(--mono);font-size:.9em;background:var(--accent-soft);padding:0 .3em;border-radius:3px}
.mono{font-family:var(--mono);font-size:12.5px}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:4px;background:var(--paper)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{border-bottom:1px solid var(--line);padding:7px 9px;vertical-align:top;text-align:left}
thead th{background:var(--accent-soft);font-weight:600;font-size:12.5px;letter-spacing:.02em}
thead th.sup{text-transform:uppercase;font-size:11.5px;letter-spacing:.06em;color:var(--accent);border-bottom:1px solid var(--line)}
tr.b1 th{background:var(--accent-soft);font-size:14px;font-weight:700}
tr.b2 th{background:var(--paper);font-weight:600;color:var(--accent);padding-left:22px;font-size:13px}
tr.chon{cursor:pointer}
tr.chon:hover td{background:var(--accent-soft)}
tr.chon.dang td{background:var(--mid-soft)}
tr.chon:focus-visible{outline:2px solid var(--sel);outline-offset:-2px}
td.id{font-family:var(--mono);white-space:nowrap;font-weight:500}
.ln{display:inline-block;width:18px;height:0;border-top:2px solid var(--muted);vertical-align:middle;margin-right:6px}
.ln-q{border-top:2px dashed var(--mid)} .ln-n{border-top:2px dashed var(--prop)}
.pill{display:inline-block;font:500 12px/1.3 var(--mono);padding:3px 7px;border-radius:3px}
.ok{background:var(--ok-soft);color:var(--ok)} .mid{background:var(--mid-soft);color:var(--mid)}
.no{background:var(--no-soft);color:var(--no)} .ext{background:var(--ext);color:var(--muted)}
.thanh{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;padding:10px 0;border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.thanh .nhan{font-size:12.5px;color:var(--muted)}
.chip{font:500 13px/1 var(--sans);padding:7px 11px;border-radius:999px;border:1px solid var(--line);background:var(--paper);color:var(--fg);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--paper)}
.chip:focus-visible,.nut:focus-visible{outline:2px solid var(--sel);outline-offset:2px}
.legend{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:13px;color:var(--muted);margin:10px 0}
.legend span{display:inline-flex;align-items:center;gap:6px}
.sw{width:16px;height:12px;border-radius:2px;border:1.3px solid var(--line);display:inline-block}
.diagram{overflow-x:auto;background:var(--paper);border:1px solid var(--line);border-radius:4px;padding:8px;margin:0}
.diagram svg{display:block;min-width:1280px;width:100%;height:auto;font-family:var(--sans)}
figcaption{font-size:13px;color:var(--muted);margin:8px 2px 0;max-width:none}
.vz{stroke:var(--line);stroke-width:1} .vz-ext{fill:var(--ext)} .vz-C{fill:var(--zc)} .vz-D{fill:var(--zd)} .vz-E{fill:var(--ze)}
.vt{font:600 11.5px var(--mono);fill:var(--muted);letter-spacing:.04em}
.vt-pp1{fill:var(--sel)} .vt2{font:10.5px var(--sans);fill:var(--muted)}
.nm{stroke-width:1} .nm-may{fill:var(--prop-soft);stroke:var(--prop)} .nm-nguoi{fill:var(--mid-soft);stroke:var(--mid)} .nm-ca{fill:var(--accent-soft);stroke:var(--accent)}
.nmt{font:700 9px var(--mono)} .nmt-may{fill:var(--prop)} .nmt-nguoi{fill:var(--mid)} .nmt-ca{fill:var(--accent)}
span.pill.nm-may{background:var(--prop-soft);color:var(--prop)} span.pill.nm-nguoi{background:var(--mid-soft);color:var(--mid)} span.pill.nm-ca{background:var(--accent-soft);color:var(--accent)}
.ag-the{fill:var(--sel);fill-opacity:.12;stroke:var(--sel);stroke-width:1.4}
.ag-the-ag1{fill:var(--ag1);stroke:var(--ag1)} .ag-the-ag2{fill:var(--ag2);stroke:var(--ag2)} .ag-the-ag3{fill:var(--ag3);stroke:var(--ag3)} .ag-the-ag4{fill:var(--ag4);stroke:var(--ag4)}
.ag-so-ag1{fill:var(--ag1)} .ag-so-ag2{fill:var(--ag2)} .ag-so-ag3{fill:var(--ag3)} .ag-so-ag4{fill:var(--ag4)}
.ag-dai{fill-opacity:.07;stroke-opacity:.45;stroke-width:1}
.ag-dai-ag1{fill:var(--ag1);stroke:var(--ag1)} .ag-dai-ag2{fill:var(--ag2);stroke:var(--ag2)} .ag-dai-ag3{fill:var(--ag3);stroke:var(--ag3)} .ag-dai-ag4{fill:var(--ag4);stroke:var(--ag4)}
.ag-mh{font:600 8.5px var(--mono);letter-spacing:.01em}
.ag-chip-n{fill:var(--paper);fill-opacity:1} .ag-chip-t{font:700 8.5px var(--mono)}
.ag-chip:hover .ag-chip-n,.ag-chip:focus-visible .ag-chip-n{fill:var(--mid-soft)}
.ag-nhan:hover .ag-the,.ag-nhan:focus-visible .ag-the{fill-opacity:.26}
.ag-so{font:700 11px var(--mono);fill:var(--sel);letter-spacing:.03em} .ag-ten{font:600 9px var(--sans);fill:var(--fg)}
.pp-nhan{cursor:pointer} .pp-hit{fill:transparent} .pp-nhan:hover .pp-hit,.pp-nhan:focus-visible .pp-hit{fill:var(--mid-soft)}
.pp-nhan:focus{outline:none} .pp-nhan:focus-visible .vt{text-decoration:underline}
ol.luong{margin:4px 0 12px;padding-left:1.3em;font-size:13.5px} ol.luong li{margin:3px 0}
table.luong-bang ol{margin:0;padding-left:1.2em} table.luong-bang li{margin:2px 0}
.vz-pp1{fill:var(--ext);stroke:var(--sel);stroke-width:1.4}
.khung-pp1{fill:none;stroke:var(--sel);stroke-width:1.4;stroke-dasharray:3 3}
.vr{font:700 12px var(--mono);fill:var(--accent);letter-spacing:.04em}
.vr2{font:10.5px var(--sans);fill:var(--muted)}
.br{font:600 11.5px var(--sans);fill:var(--fg)}
.ranh{stroke:var(--accent);stroke-width:1.4;stroke-dasharray:8 4}
.rt{font:500 10.5px var(--mono);fill:var(--accent)}
.hop{cursor:pointer}
.hop .khung{stroke-width:1.3;fill:var(--box);stroke:var(--muted)}
.hop-x .khung{fill:var(--ext)} .hop-o .khung{fill:var(--orig);stroke:var(--mid)} .hop-p .khung{stroke:var(--accent)}
.tt-q .khung{stroke:var(--mid);stroke-dasharray:6 3} .tt-n .khung{stroke:var(--prop);stroke-dasharray:6 3}
.hop:hover .khung{stroke-width:2.2}
.hop:focus{outline:none} .hop:focus-visible .khung{stroke:var(--sel);stroke-width:2.6}
.t1{font:600 12.5px var(--sans);fill:var(--fg)} .to{font:700 11px var(--mono);fill:var(--fg);letter-spacing:.02em}
.t2{font:11.5px var(--sans);fill:var(--fg)} .t2o{font:11px var(--sans);fill:var(--muted)}
.t2n{font:italic 11.5px var(--sans);fill:var(--prop)} .t3{font:10.5px var(--mono);fill:var(--muted)}
.huy{fill:var(--orig);stroke:var(--mid);stroke-width:1} .huyt{font:600 9.5px var(--mono);fill:var(--mid)}
.ten-g{cursor:pointer} .ten-g:focus{outline:none}
.hit{stroke:transparent;stroke-width:14;fill:none;pointer-events:stroke}
.ten{stroke-width:1.6;fill:none;pointer-events:none} .ten-b{stroke:var(--muted)} .ten-q{stroke:var(--mid);stroke-dasharray:6 3}
.ten-n{stroke:var(--prop);stroke-dasharray:6 3}
.ten-g:hover .ten,.ten-g:focus-visible .ten{stroke-width:3}
.ten-g:focus-visible .tl{fill:var(--sel)}
.mk-b{fill:var(--muted)} .mk-q{fill:var(--mid)} .mk-n{fill:var(--prop)}
.tl{font:600 10.5px var(--mono);fill:var(--accent)}
svg.loc .hop,svg.loc .ten-g{opacity:.18;transition:opacity .15s}
svg.loc .hop.sang,svg.loc .ten-g.sang{opacity:1}
svg .hop.chon-dang .khung{stroke:var(--sel);stroke-width:2.8}
svg .ten-g.chon-dang .ten{stroke:var(--sel);stroke-width:3.2}
svg .ten-g.chon-dang .tl{fill:var(--sel)}
@media (prefers-reduced-motion: reduce){ svg.loc .hop,svg.loc .ten-g{transition:none} }
.khung-ct{position:fixed;top:env(safe-area-inset-top,0px);right:0;bottom:0;width:384px;background:var(--paper);border-left:1px solid var(--line);
  padding:16px max(16px,env(safe-area-inset-right,0px)) calc(16px + env(safe-area-inset-bottom,0px)) 16px;overflow-y:auto;z-index:20;box-shadow:-6px 0 18px rgba(0,0,0,.08)}
.khung-ct .eb{font:600 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.khung-ct h3{font:600 18px/1.3 var(--serif);margin:6px 0 10px;text-wrap:balance}
.khung-ct dl{display:grid;grid-template-columns:96px 1fr;gap:6px 10px;font-size:13.5px;margin:0 0 12px}
.khung-ct dt{color:var(--muted)} .khung-ct dd{margin:0;min-width:0}
.khung-ct .dsach{display:flex;flex-direction:column;gap:6px;margin:4px 0 12px}
.lien{all:unset;cursor:pointer;display:block;font-size:13px;padding:6px 8px;border:1px solid var(--line);border-radius:4px;background:var(--bg)}
.lien:hover{border-color:var(--accent)} .lien:focus-visible{outline:2px solid var(--sel)}
.lien b{font-family:var(--mono);color:var(--accent);margin-right:6px}
.dong{display:flex;gap:8px;align-items:center;justify-content:space-between}
.nut{font:600 13px/1 var(--sans);padding:9px 12px;border-radius:4px;border:1px solid var(--accent);background:var(--accent);color:var(--paper);cursor:pointer}
.nut.phu{background:var(--paper);color:var(--accent)}
.nut[disabled]{opacity:.5;cursor:not-allowed}
.dong-nut{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.hoi{border-top:1px solid var(--line);margin-top:14px;padding-top:12px}
.hoi label{font-size:13px;font-weight:600;display:block;margin-bottom:6px}
.hoi textarea{width:100%;min-height:96px;font:14px/1.45 var(--sans);padding:8px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--fg);resize:vertical}
.hoi textarea:focus-visible{outline:2px solid var(--sel)}
.bao{font-size:13px;margin:6px 0 0;min-height:1.2em}
.bao.tot{color:var(--ok)} .bao.loi{color:var(--sel)}
.ghichu{font-size:12.5px;color:var(--muted)}
.dong-x{all:unset;cursor:pointer;font:600 20px/1 var(--sans);color:var(--muted);padding:4px 8px}
.dong-x:focus-visible{outline:2px solid var(--sel)}
.note{border-left:3px solid var(--mid);background:var(--mid-soft);padding:8px 12px;max-width:96ch;font-size:14px}
.tin{border-left:3px solid var(--accent);background:var(--accent-soft);padding:8px 12px;max-width:96ch;font-size:14px}
ol.fix li,ul.terms li{margin:6px 0} ul.terms ul{margin:4px 0;padding-left:1.1em}
footer{margin-top:48px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);padding-top:10px}
@media (max-width:1100px){ body.co-khung main{margin-right:0}
  .khung-ct{top:auto;left:0;width:auto;max-height:62vh;border-left:0;border-top:1px solid var(--line);box-shadow:0 -6px 18px rgba(0,0,0,.12);
    padding-left:max(16px,env(safe-area-inset-left,0px))} }
@media (max-width:640px){ h1{font-size:24px} body{font-size:14px} }
/* v0.4 · hình gộp TO-BE | AS-IS, chữ gọn */
.hd{font:700 12.5px var(--mono);fill:var(--accent);letter-spacing:.05em} .hd-a{fill:var(--asis)}
.tach{stroke:var(--line);stroke-width:2}
.vz-asis{fill:var(--za)} .vt-a{fill:var(--asis)}
.g0{font:700 9.5px var(--mono);fill:var(--fg);letter-spacing:.01em}
.g1{font:600 10.5px var(--sans);fill:var(--fg)} .g2{font:10px var(--sans);fill:var(--muted)} .g2n{font:italic 10px var(--sans);fill:var(--prop)}
.nms-may{fill:var(--prop)} .nms-nguoi{fill:var(--mid)} .nms-ca{fill:var(--accent)}
.huyg{font:700 8px var(--mono);fill:var(--mid)}
.tay{fill:var(--mid-soft);stroke:var(--mid);stroke-width:1} .tayt{font:700 8px var(--mono);fill:var(--mid)}
.van{fill:var(--paper);stroke:var(--sel);stroke-width:1.4} .vant{font:700 9px var(--sans);fill:var(--sel)}
.tt-a .khung{stroke:var(--asis)} .hop-p.tt-a .khung{stroke:var(--asis);stroke-width:1.6}
.ten-a{stroke:var(--asis)} .ten-t{stroke:var(--asis);stroke-dasharray:2 3}
.mk-a,.mk-t{fill:var(--asis)}
.fe-hinh svg{min-width:1000px;background:#fff;border-radius:4px}
.tab-trang{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 4px;border-bottom:2px solid var(--line)}
.tab-trang a{font:600 14px/1 var(--sans);padding:10px 14px;color:var(--muted);text-decoration:none;border:1px solid transparent;border-bottom:none;border-radius:6px 6px 0 0;margin-bottom:-2px}
.tab-trang a[aria-current="page"]{color:var(--accent);background:var(--paper);border-color:var(--line);border-bottom:2px solid var(--paper)}
.tab-trang a:hover{color:var(--fg)} .tab-trang a:focus-visible{outline:2px solid var(--sel);outline-offset:2px}
section.trang[hidden]{display:none}
.pill.mh-lam{background:var(--ag3);color:var(--paper)} .pill.mh-kiem{background:var(--ag4);color:var(--paper)}
details.the{border:1px solid var(--line);border-radius:4px;background:var(--paper);margin:8px 0;padding:6px 12px}
details.the>summary{cursor:pointer;font-weight:600;color:var(--accent);padding:4px 0}
details.the h4,details.the h5{margin:12px 0 6px}
a.nut{display:inline-block;text-decoration:none}
.ap-nhung{border:1px solid var(--line);border-radius:6px;background:var(--paper);padding:4px 18px 18px;margin-top:10px}
.ap-nhung .ap-h1{font:600 20px/1.3 var(--serif);margin:16px 0 4px} .ap-nhung .sub{color:var(--muted)}
.ap-nhung .tw{overflow-x:auto;margin:8px 0} .ap-nhung table{font-size:13px}
.ap-nhung th,.ap-nhung td{border:1px solid var(--line);padding:5px 8px} .ap-nhung th{background:var(--accent-soft)}
.ap-nhung tr.band td{background:var(--accent-soft);font-weight:600;color:var(--muted)}
.ap-nhung .state{display:inline-block;font:600 11px/1.4 var(--sans);padding:1px 7px;border-radius:10px;border:1px solid currentColor;margin-left:6px}
.ap-nhung .state.review{color:var(--mid)} .ap-nhung .state.agreed{color:var(--ok)} .ap-nhung .state.draft{color:var(--muted)}
.ap-nhung nav{background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px 14px;margin:10px 0}
.ap-nhung nav a{color:var(--accent)} .ap-nhung h2{border-top:2px solid var(--fg);padding-top:10px}
.ap-nhung .grid-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px}
.ap-nhung .grid-wrap svg{min-width:1000px;display:block;background:#fff}
.ap-nhung figcaption{font-size:13px;color:var(--muted)}
.goc{font-size:13px;border-left:3px solid var(--asis);padding:5px 9px;margin:6px 0;background:var(--bg)}
.goc .van-chu,span.van-chu{color:var(--sel)}
.sw-a{background:var(--za);border-color:var(--asis)}
.ln-a{border-top:2px solid var(--asis)} .ln-t{border-top:2px dotted var(--asis)}
table.lop td:first-child{white-space:nowrap;font-weight:600}
"""

JS = r"""
(function(){
  const D = JSON.parse(document.getElementById('du-lieu').textContent);
  const svgs = Array.from(document.querySelectorAll('figure.diagram svg'));
  const svg = svgs[0];
  const quaMoiHinh = (f) => svgs.forEach(f);
  const khung = document.getElementById('khung-ct');
  const noiDung = document.getElementById('ct-noi-dung');
  let dang = null, loc = 'tat', binh = null, luuNhap = {};

  const el = (id) => document.querySelector('[data-id="' + id + '"]');
  const txt = (s) => { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; };
  const tenHop = (m) => D.hop[m].ten;

  function sangLen(ids){
    quaMoiHinh(sv => { sv.classList.toggle('loc', !!ids);
      sv.querySelectorAll('.hop,.ten-g').forEach(n => n.classList.toggle('sang', !!ids && ids.has(n.dataset.id))); });
  }
  function apLoc(){
    if (dang) return;
    if (loc === 'tat') { sangLen(null); return; }
    const ids = new Set();
    quaMoiHinh(sv => sv.querySelectorAll('.hop,.ten-g').forEach(n => { if (n.dataset.tt === loc || (loc === 'a' && n.dataset.tt === 't')) ids.add(n.dataset.id); }));
    sangLen(ids);
  }
  document.querySelectorAll('.chip[data-loc]').forEach(c => c.addEventListener('click', () => {
    loc = c.dataset.loc;
    document.querySelectorAll('.chip[data-loc]').forEach(x => x.setAttribute('aria-pressed', String(x === c)));
    apLoc();
  }));

  function lienTen(m){
    const t = D.ten[m];
    return '<button class="lien" data-di="t:' + m + '"><b>' + m + '</b>' + txt(tenHop(t.tu) + ' → ' + tenHop(t.toi)) +
      '<br><span class="ghichu">' + txt(t.cai_gi) + '</span></button>';
  }
  function veHop(m){
    const h = D.hop[m];
    let s = '<div class="eb">' + txt(h.vung + ' · ' + h.dai + ' · ' + h.loai + ' · ' + D.tt[h.tt]) + '</div>';
    s += '<h3>' + txt(h.ten) + '</h3>';
    if (h.luong && h.luong.length) s += '<div class="eb">luồng xử lý</div><ol class="luong">' + h.luong.map(b => '<li>' + txt(b) + '</li>').join('') + '</ol>';
    if (h.thanh_vien) s += '<div class="eb">hộp thuộc luồng (' + h.thanh_vien.length + ')</div><div class="dsach">' + h.thanh_vien.map(x => '<button class="lien" data-di="h:' + x + '">' + txt(D.hop[x].ten) + '</button>').join('') + '</div>';
    if (h.dong.length) s += '<p>' + h.dong.map(txt).join('<br>') + '</p>';
    if (h.goc) s += '<div class="eb">gộp từ ' + h.goc.length + ' hộp của sơ đồ AS-IS' + (h.tay ? ' · có bước người làm tay' : '') + '</div>' +
      h.goc.map(g => '<div class="goc"><b>' + txt(g.ten) + '</b> <span class="ghichu">' + txt(g.loai) + (g.buoc ? ' · bước ' + txt(g.buoc) : '') + (g.luong ? ' · ' + txt(g.luong) : '') + '</span>' +
        (g.dong && g.dong.length ? '<br>' + g.dong.map(txt).join(' · ') : '') + (g.ai ? '<br>ai: ' + txt(g.ai) : '') + (g.cach ? '<br>' + txt(g.cach) : '') +
        (g.file ? '<br><span class="mono">' + txt(g.file) + '</span>' : '') + (g.issue ? '<br><span class="van-chu">⚠ ' + txt(g.issue) + '</span>' : '') + '</div>').join('');
    s += '<dl>';
    if (h.nm && h.nm.length) s += '<dt>' + txt(h.nm[0] === 'VÀO' ? 'nguồn vào' : 'đầu ra') + '</dt><dd><span class="pill ' + ({'MÁY':'nm-may','NGƯỜI':'nm-nguoi','NGƯỜI+MÁY':'nm-ca'})[h.nm[1]] + '">' + txt(h.nm[1]) + '</span> ' + txt(h.nm[2]) + '</dd><dt>rủi ro · cổng</dt><dd>' + txt(h.nm[3]) + '</dd>';
    if (h.mono) s += '<dt>số liệu</dt><dd class="mono">' + txt(h.mono) + '</dd>';
    if (h.huy.length) s += '<dt>khởi bởi</dt><dd>' + h.huy.map(x => '<button class="lien" data-di="h:' + x + '" style="display:inline-block"><b>' + x + '</b>' + txt(D.hop[x].ten.replace(/^S\d · /, '')) + '</button>').join(' ') + '</dd>';
    s += '<dt>đối chiếu</dt><dd>' + txt(h.dc) + '</dd></dl>';
    s += '<div class="eb">vào (' + h.vao.length + ')</div><div class="dsach">' + (h.vao.map(lienTen).join('') || '<span class="ghichu">không có mũi tên vào</span>') + '</div>';
    s += '<div class="eb">ra (' + h.ra.length + ')</div><div class="dsach">' + (h.ra.map(lienTen).join('') || '<span class="ghichu">không có mũi tên ra</span>') + '</div>';
    return s;
  }
  function veTen(m){
    const t = D.ten[m];
    let s = '<div class="eb">mũi tên ' + m + ' · ' + txt(D.tt[t.tt]) + '</div>';
    s += '<h3>' + txt(tenHop(t.tu) + ' → ' + tenHop(t.toi)) + '</h3>';
    s += '<p class="ghichu">' + txt(t.nhom) + '</p><dl>';
    s += '<dt>chở gì</dt><dd>' + txt(t.cai_gi) + '</dd>';
    s += '<dt>khoá</dt><dd><code>' + txt(t.khoa) + '</code></dd>';
    s += '<dt>bản số</dt><dd>' + txt(t.ban_so) + '</dd>';
    s += '<dt>cổng</dt><dd>' + txt(t.cong) + '</dd>';
    s += '<dt>hôm nay</dt><dd>' + txt(t.co_ma) + '</dd></dl>';
    s += '<div class="dsach"><button class="lien" data-di="h:' + t.tu + '"><b>từ</b>' + txt(tenHop(t.tu)) + '</button>';
    s += '<button class="lien" data-di="h:' + t.toi + '"><b>tới</b>' + txt(tenHop(t.toi)) + '</button></div>';
    return s;
  }
  function nhanPhan(id){
    const [k, m] = id.split(':');
    if (k === 'h') return 'Hộp "' + tenHop(m) + '"';
    const t = D.ten[m];
    return 'Mũi tên ' + m + ' (' + tenHop(t.tu) + ' → ' + tenHop(t.toi) + ')';
  }
  function veHoi(id){
    let s = '<div class="hoi"><div class="dong-nut">';
    s += '<button class="nut phu" id="nut-bl" type="button">Bình luận phần này</button>';
    s += '<button class="nut phu" id="nut-xem" type="button">Xem trên hình</button></div>';
    s += '<label for="o-hoi">Hỏi Claude về ' + txt(nhanPhan(id)) + '</label>';
    s += '<textarea id="o-hoi" maxlength="3000" placeholder="Ví dụ: cột pháp nhân này lấy từ đâu khi nguồn có hai pháp nhân?"></textarea>';
    s += '<div class="dong-nut"><button class="nut" id="nut-gui" type="button">Gửi cho Claude</button></div>';
    s += '<p class="bao" id="bao" role="status"></p>';
    s += '<p class="ghichu">Câu hỏi được đăng thành một luồng bình luận gắn vào đúng phần này; Claude trả lời ngay trong luồng đó.</p></div>';
    return s;
  }

  function chon(id, cuon){
    if (dang) { const cu = el(dang); if (cu) cu.classList.remove('chon-dang'); }
    document.querySelectorAll('tr.chon.dang').forEach(r => r.classList.remove('dang'));
    const o = document.getElementById('o-hoi'); if (o && dang) luuNhap[dang] = o.value;
    dang = id;
    const n = el(id); if (!n) return;
    // chỉ chuyển trang khi phần ấy KHÔNG có mặt ở trang đang mở (bấm dòng bảng ở trang 2 ⛔ bị kéo sang trang 1)
    const thay = [...document.querySelectorAll('[data-id="' + id + '"],[data-ref="' + id + '"]')].some(x => !x.closest('section.trang[hidden]'));
    const sc = n.closest('section.trang'); if (!thay && sc && sc.hidden) document.querySelector('.tab-trang a[data-trang="' + sc.id + '"]').click();
    n.classList.add('chon-dang');
    document.querySelectorAll('tr.chon[data-ref="' + id + '"]').forEach(r => r.classList.add('dang'));
    const [k, m] = id.split(':');
    const ids = new Set([id]);
    if (k === 'h' && D.hop[m].thanh_vien) {
      const tv = new Set(D.hop[m].thanh_vien); tv.forEach(x => ids.add('h:' + x));
      Object.keys(D.ten).forEach(t => { if (tv.has(D.ten[t].tu) && tv.has(D.ten[t].toi)) ids.add('t:' + t); });
    }
    else if (k === 'h') { const h = D.hop[m]; h.vao.concat(h.ra).forEach(t => { ids.add('t:' + t); ids.add('h:' + D.ten[t].tu); ids.add('h:' + D.ten[t].toi); }); }
    else { const t = D.ten[m]; ids.add('h:' + t.tu); ids.add('h:' + t.toi); }
    sangLen(ids);
    noiDung.innerHTML = (k === 'h' ? veHop(m) : veTen(m)) + veHoi(id);
    khung.hidden = false; document.body.classList.add('co-khung');
    const oh = document.getElementById('o-hoi'); oh.value = luuNhap[id] || '';
    capNhatNut();
    if (cuon) n.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center', inline: 'center'});
  }
  function dong(){
    const o = document.getElementById('o-hoi'); if (o && dang) luuNhap[dang] = o.value;
    if (dang) { const cu = el(dang); if (cu) cu.classList.remove('chon-dang'); }
    document.querySelectorAll('tr.chon.dang').forEach(r => r.classList.remove('dang'));
    dang = null; khung.hidden = true; document.body.classList.remove('co-khung'); apLoc();
  }
  document.getElementById('nut-dong').addEventListener('click', dong);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !khung.hidden) dong(); });

  quaMoiHinh(svg => svg.addEventListener('click', e => {
    const g = e.target.closest('.hop,.ten-g,.pp-nhan');
    if (g) chon(g.dataset.id, false); else if (dang) dong();
  }));
  quaMoiHinh(svg => svg.addEventListener('keydown', e => {
    const g = e.target.closest('.hop,.ten-g,.pp-nhan');
    if ((e.key === 'Enter' || e.key === ' ') && g) { e.preventDefault(); chon(g.dataset.id, false); }
  }));
  document.querySelectorAll('tr.chon').forEach(r => {
    r.addEventListener('click', () => chon(r.dataset.ref, false));
    r.addEventListener('keydown', e => { if (e.key === 'Enter') chon(r.dataset.ref, false); });
  });
  noiDung.addEventListener('click', async e => {
    const l = e.target.closest('.lien'); if (l) { chon(l.dataset.di, false); return; }
    if (e.target.id === 'nut-xem') { const n = el(dang); if (n) n.scrollIntoView({behavior:'auto', block:'center', inline:'center'}); return; }
    if (e.target.id === 'nut-bl') return moBinhLuan();
    if (e.target.id === 'nut-gui') return guiClaude();
  });

  // ── bình luận / gửi Claude ──
  function bao(s, kieu){ const b = document.getElementById('bao'); if (b) { b.textContent = s; b.className = 'bao ' + (kieu || ''); } }
  async function capNhatNut(){
    const bl = document.getElementById('nut-bl'), gui = document.getElementById('nut-gui');
    if (!bl) return;
    if (!binh) { bl.disabled = true; gui.disabled = true; bao('Bình luận và hỏi Claude chỉ có khi mở trang này trên claude.ai.', ''); return; }
    bl.disabled = false;
    let tt = 'off';
    try { tt = await binh.canSendToClaude(); } catch (_) { tt = 'off'; }
    if (tt === 'available') { gui.disabled = false; return; }
    gui.disabled = true;
    bao(tt === 'writers_only' ? 'Chỉ người có quyền chỉnh sửa trang mới gửi được cho Claude; bạn vẫn bình luận thường được.'
      : tt === 'no_session' ? 'Chưa có phiên Claude nào đang theo dõi trang này. Câu hỏi vẫn đăng được bằng nút "Bình luận phần này".'
      : 'Gửi cho Claude không bật ở đây. Dùng nút "Bình luận phần này".', '');
  }
  async function moBinhLuan(){
    const n = el(dang); if (!binh || !n) return;
    try { const r = await binh.openComposer({element: n}); if (!r.opened) bao('Khung bình luận đang mở với nội dung chưa gửi.', ''); }
    catch (err) { bao(err && err.code === 'rate_limited' ? 'Mở hơi nhanh, đợi một chút rồi bấm lại.' : 'Không mở được khung bình luận ở đây.', 'loi'); }
  }
  const LOI = {
    consent_required: 'Chưa gửi: bạn chưa cho phép trang này bình luận thay bạn. Bản nháp vẫn còn.',
    forbidden: 'Bình luận từ trang đang tắt ở đây. Dùng chế độ bình luận của claude.ai.',
    claude_unavailable: 'Không gửi được cho Claude lúc này, chưa có gì được đăng. Bản nháp vẫn còn; bạn có thể bình luận thường.',
    rate_limited: 'Gửi hơi nhanh, đợi một chút rồi bấm lại.',
    invalid: 'Nội dung không hợp lệ (rỗng hoặc quá dài).'
  };
  async function guiClaude(){
    const o = document.getElementById('o-hoi'), gui = document.getElementById('nut-gui');
    const chu = (o.value || '').trim();
    if (!chu) { bao('Gõ câu hỏi trước đã.', 'loi'); o.focus(); return; }
    const n = el(dang); if (!binh || !n) return;
    gui.disabled = true; bao('Đang gửi…', '');
    try {
      const anchor = await binh.anchorFor(n);
      await binh.sendToClaude({anchor, text: '[' + dang.slice(2) + ' · ' + nhanPhan(dang) + '] ' + chu});
      o.value = ''; luuNhap[dang] = '';
      bao('Đã gửi cho Claude. Câu trả lời sẽ hiện trong luồng bình luận gắn ở phần này.', 'tot');
    } catch (err) {
      bao(LOI[err && err.code] || ('Không gửi được (' + ((err && err.code) || 'lỗi') + '). Bản nháp vẫn còn.'), 'loi');
    } finally { gui.disabled = false; capNhatNut(); }
  }
  // ── hai trang: #trang-1 · #trang-2 ──
  function moTrang(id){
    if (!document.getElementById(id)) id = 'trang-1';
    document.querySelectorAll('section.trang').forEach(sc => { sc.hidden = sc.id !== id; });
    document.querySelectorAll('.tab-trang a[data-trang]').forEach(a => {
      if (a.dataset.trang === id) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
  }
  document.querySelectorAll('.tab-trang a[data-trang]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault(); moTrang(a.dataset.trang);
    try { history.replaceState(null, '', '#' + a.dataset.trang); } catch (_) {}
    window.scrollTo({top: 0}); }));
  moTrang((location.hash || '#trang-1').slice(1));
  window.addEventListener('hashchange', () => moTrang(location.hash.slice(1)));
  if (window.claude && window.claude.use) {
    window.claude.use('comments').then(c => { binh = c; if (dang) capNhatNut(); }).catch(() => { binh = null; });
  }
})();
"""

THAN_TREN = """
<header class="top">
  <h1>Voi FLS-tobe-phase1</h1>
  <p class="meta"><b>v0.6.1 · 2026-11-06</b> · Giai đoạn 1: đi hết INPUT, về <b>một</b> bảng ITL, mọi dòng có pháp nhân. Lệnh chi lấy từ <b>sổ cái PM / PC của FPS</b> qua hợp đồng dữ liệu (§5).
  Hình, bảng mũi tên, bảng kiểm cạnh và khung chi tiết <b>sinh từ cùng một bản khai</b> (<code>docs/ITL/_tools/sinh_voi_phase1.py</code>); máy kiểm hình trước khi ghi.<br>
  Nửa phải của hình 1 là luồng <b>AS-IS</b> lấy từ sơ đồ "Voi ITL AS-IS" (<code>docs/ITL/_tools/voi_asis_goc.json</code>).<br>
  PD Now là bản gốc tham khảo: trang này chỉ mượn <b>thuật ngữ</b> (PE · PI · PM · PC · LE · CDT · HD/KRF · Reference No · General Trustest), không dùng tên sheet, tên file hay bước tính của nó. Mã FLS @ <code>2d1b710</code>.</p>
</header>
<p class="tin"><b>Hai trang:</b> <b>Trang 1</b> — con voi TO-BE cạnh AS-IS và bản kiểm từng bước (§1a). <b>Trang 2</b> — fleet eval: agent nào chạy mô hình nào, sơ đồ quy trình, bốn thẻ, và <b>bản AP nhúng nguyên</b> (F4). <b>Cách dùng:</b> bấm một hộp hay một mũi tên (hoặc một dòng trong bảng) để làm nổi các đường nối của nó và mở khung chi tiết. Trong khung có <b>Bình luận phần này</b> và ô <b>Hỏi Claude</b>: câu hỏi được gắn đúng vào phần đang chọn, Claude trả lời trong luồng bình luận ở đó.</p>
"""


def trang() -> str:
    k = kiem()
    if k["loi"] or kiem_m() or kiem_a():
        raise SystemExit("⛔ hình SAI:\n  " + "\n  ".join(k["loi"] + kiem_m() + kiem_a()))
    n_lop = len({d for d in DAI if DAI[d][3]})
    cap = (f'Hình 1 — Voi FLS phase 1: <b>TO-BE bên trái, AS-IS bên phải, chung {n_lop} lớp</b> (AS-IS xếp vào lớp của TO-BE, không thêm lớp nào). '
           f'Hai nửa cùng bảy cột: {" · ".join(f"{i + 1} {c}" for i, c in enumerate(COT_NGHIA))}. '
           f'Máy kiểm lúc sinh — TO-BE: <b>{k["hop"]} hộp · {k["ten"]} mũi tên</b> ({k["doc"]} dọc · {k["ngang"]} ngang), '
           f'0 mũi tên nhảy dải, <b>{k["cheo"]}</b> chỗ cắt nhau, 0 mũi tên cắt qua hộp, mỗi dải 2–5 mục (nguồn FPS, PP (2), PP (3) có chủ ý một hộp). '
           f'AS-IS: <b>{len(HOP_A)} hộp · {len(TEN_A)} mũi tên</b> gộp từ <b>{len(ASIS_GOC["hop"])}/{len(ASIS_GOC["hop"])}</b> hộp và '
           f'{len(ASIS_GOC["ten"])} mũi tên của sơ đồ AS-IS gốc — mỗi mũi tên gốc hoặc nằm trong một hộp gộp, hoặc được đúng một mũi tên AS-IS chở; '
           'mũi tên AS-IS được đi xuyên dải khi làn trống (bước nhảy thật của Sheets), vẫn 0 cắt qua hộp, 0 chồng nhau. '
           'Chữ trên hộp đã rút còn tên + một dòng; rê chuột hay bấm hộp để xem đủ. Điểm khởi động S1–S5 là <b>huy hiệu</b> trên hộp; '
           '<i>GHI tay</i> đọc dải dưới (chiều đọc ngược) nên không vẽ mũi tên.')
    o = ['<title>Voi FLS-tobe-phase1</title>',
         '<meta name="claude:viewport-fit-sides" content="cover">',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;family=IBM+Plex+Serif:wght@600&amp;display=swap">',
         f'<style>{CSS}</style>', '<main>', THAN_TREN,
         '<nav class="tab-trang" aria-label="Trang"><a href="#trang-1" data-trang="trang-1" aria-current="page">Trang 1 · Mapping TO-BE ↔ AS-IS</a>'
         '<a href="#trang-2" data-trang="trang-2">Trang 2 · Fleet eval + AP</a></nav>',
         '<section class="trang" id="trang-1">',
         '<h2>§1 · Con voi — TO-BE và AS-IS cạnh nhau, chung lớp theo đời sống của dữ liệu</h2>',
         '<div class="thanh" role="toolbar" aria-label="Lọc theo trạng thái"><span class="nhan">Làm nổi:</span>'
         '<button class="chip" data-loc="tat" aria-pressed="true" type="button">Tất cả</button>'
         '<button class="chip" data-loc="b" aria-pressed="false" type="button">Có mã</button>'
         '<button class="chip" data-loc="q" aria-pressed="false" type="button">GĐ1 phải dựng</button>'
         '<button class="chip" data-loc="n" aria-pressed="false" type="button">Đề xuất, chờ owner</button>'
         '<button class="chip" data-loc="a" aria-pressed="false" type="button">AS-IS</button></div>',
         '<div class="legend">'
         '<span><i class="sw" style="background:var(--orig);border-color:var(--mid);border-radius:6px"></i>khởi động (người · nhịp)</span>'
         '<span><i class="sw" style="background:var(--ext)"></i>nguồn ngoài FLS</span>'
         '<span><i class="sw" style="border-color:var(--muted)"></i>dữ liệu (tên của vật)</span>'
         '<span><i class="sw" style="border-color:var(--accent)"></i>xử lý (ĐỘNG TỪ + danh từ)</span>'
         '<span><i class="ln"></i>có mã</span><span><i class="ln ln-q"></i>GĐ1 phải dựng (đã chốt)</span>'
         '<span><i class="ln ln-n"></i>đề xuất của trang này (chờ owner)</span>'
         '<span><i class="sw" style="border-left:4px solid var(--mid)"></i>NGƯỜI <i class="sw" style="border-left:4px solid var(--prop)"></i>MÁY <i class="sw" style="border-left:4px solid var(--accent)"></i>NGƯỜI+MÁY · vạch mép trái = nguồn do ai làm ra (§1e)</span>'
         '<span><span class="pill mid" style="font-size:10px">S1</span> huy hiệu = hộp do điểm khởi động S1 chạy</span><span><i class="sw" style="border:1.4px dashed var(--sel)"></i>PP (n) = phương pháp xử lý n</span>'
         '<span><i class="sw" style="background:var(--ag1);opacity:.5"></i><i class="sw" style="background:var(--ag2);opacity:.5"></i><i class="sw" style="background:var(--ag3);opacity:.5"></i><i class="sw" style="background:var(--ag4);opacity:.5"></i>dải màu = việc của Agent 1–4 · chip A3.1–A3.3 = ba agent con của Filter Fulfill &amp; Adjust</span>'
         '<span><i class="sw sw-a"></i>AS-IS (Sheets hôm nay)</span><span><i class="ln ln-a"></i>công thức / GScript</span><span><i class="ln ln-t"></i>người làm tay</span>'
         '<span><span class="pill mid" style="font-size:10px">TAY</span> có bước người bấm / gõ</span><span><b style="color:var(--sel)">!</b> AS-IS có lỗi đã ghi nhận</span>'
         '</div>',
         f'<figure class="diagram" id="hinh">{svg()}<figcaption>{cap}</figcaption></figure>',
         bang_lop(), bang_kiem_asis(),
         """
<h3>Thuật ngữ trên hình</h3>
<ul class="terms">
<li><b>Sổ cái FPS</b><ul><li>sổ cái PM: mỗi dòng một PM line (lệnh chi), mang sẵn khoá PE/PI, HD/KRF, CDT1, pháp nhân thanh toán, Reference No</li><li>sổ cái PC: mỗi dòng một PC line (quyết toán, hoàn ứng), trỏ về PM/PE gốc</li></ul></li>
<li><b>Tiền</b><ul><li>General Trustest: bộ trường tối thiểu của một dòng tiền — ngày · tiền · tiền tệ · LE</li><li>Reference No: mã ngân hàng cấp, có trên sao kê và trên dòng sổ cái PM — khoá ghép tiền ↔ lệnh chi</li></ul></li>
<li><b>Ba vai pháp nhân</b> (xem câu 1, §7)<ul><li>pháp nhân TK: chủ tài khoản tiền đi ra / vào — khai theo nguồn</li><li><code>le_payer</code>: pháp nhân thanh toán ghi trên sổ cái PM</li><li><code>le</code>: pháp nhân nhận, khi đối tác là pháp nhân Apero; <code>le ≠ le_payer</code> ⇒ cờ nội bộ (<code>is_intercompany</code>)</li></ul></li>
<li><b>Chiều chi phí</b><ul><li>CDT1 chủ dự toán · HD/KRF mã hạng mục · Budget Code mã ngân sách</li></ul></li>
<li><b>Máy FLS</b><ul><li>canon 36 trường: khuôn dòng chuẩn · <code>content_key</code>: khoá chống trùng nội dung</li><li><code>chup_id</code> / <code>run_id</code>: vết lần chụp / lần nạp · bản khai nguồn: bố cục cột + thứ tự ngày (+ pháp nhân TK)</li><li>lớp sửa: mọi thay đổi là dòng thêm · sổ hiệu lực: sổ gốc + lớp sửa, đọc ra một bảng</li></ul></li>
</ul>
""", """
<h2>§1b · Mapping của phương pháp (1) — ba lớp giao dịch và vòng cộng dồn</h2>
<p>Phóng to hộp MAPPING trên hình chính. Mỗi giao dịch ngân hàng và mỗi dòng sổ cái PM sau một lượt mapping rơi vào <b>đúng một</b> lớp; dòng ở lớp L3 đi qua <b>vòng cộng dồn</b>: luật đã ký gợi ý loại giao dịch, kế toán xác nhận, xác nhận tích lại thành luật mới cho lượt sau. Máy chỉ gợi ý; luật chỉ hiệu lực khi có người ký.</p>
<figure class="diagram" id="hinh-m">""", svg_m(), """<figcaption>Hình 2 — Mapping PP (1) phóng to, nhận cả đợt lương / BH của PP (2). 5 dải · 15 hộp · 15 mũi tên; mũi tên m14 đi <b>lên</b> có chủ ý: đó là vòng cộng dồn. Máy kiểm như hình 1: không mũi tên nhảy dải, lệch hộp hay cắt qua hộp.</figcaption></figure>
<h3>Luật xếp lớp sau mapping</h3>
<div class="scroll"><table>
<thead><tr><th colspan="2" class="sup">Lớp</th><th class="sup">So khớp</th><th class="sup">Hiện trạng</th><th colspan="2" class="sup">Xử lý</th></tr>
<tr><th>lớp</th><th>điều kiện</th><th>khoá</th><th>hôm nay</th><th>đi đâu</th><th>cổng</th></tr></thead>
<tbody>
<tr class="chon" data-ref="h:mL1" tabindex="0"><td><b>L1 · khớp</b></td><td>giao dịch có Reference No trùng ≥ 1 dòng sổ cái PM; Σ tiền các PM line = tiền giao dịch; cùng tiền tệ; nhánh VN thêm pháp nhân trả = pháp nhân TK (QĐ-ITL-144). <b>Hoặc</b> (PP 2) Reference number của giao dịch = Số CT kế toán đã dán vào dòng lương H1000 (Σ dòng = tiền giao dịch)</td><td>Reference No + tiền (+ pháp nhân)</td><td>2.263 mối nối</td><td>mối nối vào lớp sửa; gợi ý hd/cdt1 từ PM line</td><td>Σ lệch ⇒ chặn, ⛔ chia bừa</td></tr>
<tr class="chon" data-ref="h:mMap" tabindex="0"><td><b>L1b · khớp mã, lệch</b></td><td>có Reference No chung nhưng Σ tiền lệch, khác tiền tệ, hoặc N giao dịch × M PM line</td><td>Reference No</td><td>84 lệnh khác tiền tệ (Q-FX-1)</td><td>hàng chờ cho người, kèm lý do có tên</td><td>⛔ tự chọn cặp</td></tr>
<tr class="chon" data-ref="h:mL2" tabindex="0"><td><b>L2 · có trên FPS, chưa có trên bank txns</b></td><td>dòng sổ cái PM trạng thái cuối đã duyệt, không giao dịch nào mang Reference No của nó trong các ảnh sao kê của TK chi, tính tới ảnh mới nhất</td><td>pm_line_id · Reference No · TK chi</td><td>1.345 dòng · 698 phiếu</td><td>F01 lằn lệnh: "lệnh chưa thấy tiền"; tuổi = ngày ảnh mới nhất − ngày thực chi</td><td>tuổi &gt; N ngày ⇒ cờ; TK chi chưa có ảnh ⇒ "chưa đo được", ⛔ coi là chưa chi</td></tr>
<tr class="chon" data-ref="h:mL3" tabindex="0"><td><b>L3 · có trên bank txns, không có trên FPS</b></td><td>giao dịch không có Reference No, hoặc có mà không dòng sổ cái PM nào mang</td><td>content_key · TK · nội dung · loại bank</td><td>89,7% dòng chưa ghép có mã mà không PM nào mang</td><td>SUY DIỄN loại giao dịch (vòng cộng dồn) → gợi ý ở F01</td><td>trạng thái vẫn UNMAPPED tới khi người chốt; ⛔ nhãn "không cần lệnh chi" (QĐ-ITL-58)</td></tr>
</tbody></table></div>
<h3>Vòng cộng dồn — tự suy diễn loại giao dịch</h3>
<div class="scroll"><table>
<thead><tr><th>bước</th><th>ai</th><th>đọc</th><th>ghi</th><th>cổng</th></tr></thead>
<tbody>
<tr class="chon" data-ref="h:mSuy" tabindex="0"><td>① gợi ý</td><td>máy</td><td>dòng L3 + bảng luật hiệu lực, khoá <code>(TK, mẫu nội dung, loại bank)</code></td><td>gợi ý loại giao dịch, nguồn = máy gợi ý</td><td>khoá khớp hai luật nói khác nhau ⇒ không gợi ý</td></tr>
<tr class="chon" data-ref="h:mKT" tabindex="0"><td>② xác nhận</td><td>kế toán (F01)</td><td>gợi ý cạnh dòng L3</td><td>giữ hoặc sửa → lớp sửa (chỉ-thêm)</td><td>actor từ thẻ đăng nhập; máy ⛔ tự xác nhận</td></tr>
<tr class="chon" data-ref="h:mXN" tabindex="0"><td>③ gom bằng chứng</td><td>máy</td><td>các xác nhận theo khoá luật</td><td>luật ứng viên khi ≥ k lần cùng loại giao dịch và 0 lần khác</td><td>một lần người sửa ngược ⇒ luật về "xem lại"</td></tr>
<tr class="chon" data-ref="h:mKy" tabindex="0"><td>④ ký</td><td>owner / kế toán trưởng</td><td>luật ứng viên + bằng chứng</td><td>luật hiệu lực, có version, <code>signed_by</code>, <code>signed_at</code></td><td>luật ⛔ hiệu lực khi chưa ký (INV-I16 · QĐ-ITL-56)</td></tr>
<tr class="chon" data-ref="h:mGoiY" tabindex="0"><td>⑤ đo mỗi vòng</td><td>máy</td><td>gợi ý và xác nhận của lượt</td><td>độ phủ (dòng L3 có gợi ý) · độ đúng (gợi ý được giữ nguyên)</td><td>in cả mẫu số; độ đúng tụt ⇒ dừng áp luật mới</td></tr>
</tbody></table></div>
<p class="note"><b>Vế PS Nợ (tiền vào)</b> — hôm nay máy chỉ ghép vế PS Có (mẫu số 8.246 dòng, <code>13_LO_TRINH</code> B0). Tiền vào không có PM nên mặc định rơi vào L3; luật mồi cho vế Nợ: chuyển nội bộ giữa hai TK Apero (cặp với một PS Có cùng tiền ở TK kia, lệch ngày nhỏ ⇒ bật <code>is_intercompany</code>) · doanh thu nền tảng · hoàn tiền · vay và lãi. Mọi dòng, cả hai vế, cuối ngày phải cộng ra đúng số dư trong CCR / CCR Cash.<br>
<b>Luật PP (2) (sửa 06/11):</b> nạp thẳng sổ H1000 — dòng lương đã tách HD · CDT1 · pháp nhân tới từng nhân viên; nối giao dịch bank theo <b>Số CT</b> (số FT kế toán dán), soát Σ Có = Σ Nợ mỗi đợt và đủ tháng. Bỏ luật cũ "khớp Σ đợt theo venture → LE".<br>
<b>Luật mồi cho bảng luật</b> — năm loại giao dịch kế toán ghi là hay bị sót trên PM: lãi và phí ngân hàng · điều chuyển nội bộ, mua bán ngoại tệ · chi phí năm trước trả năm nay · quẹt thẻ chưa nhập PM · doanh thu, OMC, server chưa nhập. <b>Danh mục loại giao dịch</b> dùng lại cột "Loại giao dịch (Payment Type)" của sổ cái PM để L1 và L3 nói cùng một bộ từ.<br>
<b>Hai câu chờ owner:</b> ① vòng này cần đọc <b>nội dung giao dịch</b> trên sao kê, nhưng hôm nay FLS chỉ được đọc ba cột (ngày · Reference number · nguồn — QĐ-ITL-92) và <code>fls_itl.memo</code> rỗng 8.387/8.387 ⇒ có nới QĐ-ITL-92 cho cột nội dung, chỉ để suy diễn? ② chọn <b>k</b> (số xác nhận để thành luật ứng viên) và <b>N</b> (số ngày để L2 bị cờ).</p>
""", """
<h2>§1c · Phương pháp (3) — 4 chi phí nền tảng: OMC · GI · SC · PS</h2>
<p><b>Sửa 06/11:</b> bốn loại chi phí này <b>có PE/PM trên FPS</b> (AS-IS nối bằng Combine Code Vendor-Date-NoTrans), và kết quả phải <b>mapping được với bank txns</b>. <b>Nguồn (PD Now 103–106, sửa theo bình luận owner):</b> GI · OMC xuất từ <b>Looker</b> (Data · AnhTQ); <b>SC</b> (server cost) ở Gsheet <i>Chi phí Service Apero</i> (SHQ1 · Luận); <b>PS</b> ở Gsheet <i>AperoGroup_Payment</i> (SHQ2 · kế toán). <b>Cách nối (PD Now 501–507):</b> dòng ITL đã adjust (đã có PE/PM, đã nối bank qua Reference No) ⨝ dòng nguồn theo Combine Code <i>Vendor-Date-NoTrans</i> → Mapping Block 1 (ID Vendor ↔ Network-Acc ↔ CDT1) → chia theo <b>CDT1 × tháng</b> (CFA2 MID 1–3) → báo cáo P&amp;L theo CDT1 (600–603). Giao dịch ngân hàng đưa vào là những dòng còn ở lớp L3 của §1b.</p>
<figure class="diagram" id="hinh-n">""", svg_n(), """<figcaption>Hình 3 — PP (3) phóng to. 5 dải · 13 hộp · 14 mũi tên, máy kiểm như hình 1. Mọi hộp nét đứt xanh: đề xuất, chờ owner ký luật.</figcaption></figure>
<h3>Mỗi luật mapping phải khai năm điều</h3>
<p>Luật cụ thể của OMC, GI, SC (server cost), PS do owner điền; trang này chỉ khai <b>hình dạng</b> một luật phải có, để bốn luật so được với nhau.</p>
<div class="scroll"><table>
<thead><tr><th>điều phải khai</th><th>hình dạng</th><th>vì sao</th></tr></thead>
<tbody>
<tr><td>① nhận diện giao dịch</td><td>TK chi + vendor / từ khoá nội dung + chiều tiền ra</td><td>không có Reference No; thiếu nội dung thì cần nới QĐ-ITL-92 (câu ① §1b)</td></tr>
<tr><td>② khớp kỳ</td><td>tháng chi phí trên sổ nguồn ↔ tháng của giao dịch (trả trước / trả sau bao nhiêu tháng)</td><td>một giao dịch có thể trả chi phí của tháng trước</td></tr>
<tr><td>③ khớp tiền</td><td>Σ chi phí kỳ của loại = Σ giao dịch khớp; dung sai; cùng tiền tệ hay quy đổi</td><td>lệch thì chặn, không chia bừa (INV-I16)</td></tr>
<tr><td>④ tỉ lệ CDT1</td><td>chia theo <b>CDT1</b> (đã chốt 06/11, như AS-IS) qua Mapping Block 1 (ID Vendor ↔ Network-Acc ↔ CDT1 × số tháng, PD Now 503–504)</td><td>allocate cần Σ % = 100 cho từng loại · tháng</td></tr>
<tr><td>⑤ ai ký, từ khi nào</td><td>người ký + ngày hiệu lực + version</td><td>luật đổi thì lượt cũ giữ version đã dùng</td></tr>
</tbody></table></div>
""", """
<h2>§1d · Luồng xử lý dữ liệu theo từng hộp</h2>
<p>Vùng FLS · NẠP chạy bởi <b>bốn agent</b> (nhãn màu ở lề trái hình 1: AGENT 1 Collect_raw_data · AGENT 2 Generate Group Ledger (ITL raw) · AGENT 3 Filter Fulfill &amp; Adjust (ITL Adjust) · AGENT 4 Auditor (Compounding Loop)); bấm nhãn để xem agent nhận gì, làm gì, ra gì. Bước sau khi xong voi: dựng AP rồi chạy Flip eval cho bốn agent này. Mỗi hộp xử lý và hộp dữ liệu trong FLS có một luồng tổng quan, tối đa 5 bước. Cùng luồng này hiện ở đầu khung chi tiết khi bấm hộp, và trong chú thích khi rê chuột lên hộp. Bấm nhãn <b>PHƯƠNG PHÁP (1) / (2) / (3) ▸</b> trên hình 1 để xem luồng trọn của từng phương pháp và làm nổi các hộp thuộc nó.</p>
""", bang_luong(), """
<h2>§1e · Nguồn của máy, nguồn của người — đầu vào và đầu ra</h2>
<p>Mỗi nguồn vào và mỗi đầu ra mang một nhãn ở góc trên-trái của hộp: <b>MÁY</b> (hệ sinh, không ai gõ) · <b>NGƯỜI</b> (người gõ, dán hoặc ký) · <b>NGƯỜI+MÁY</b> (người nhập, máy sinh sổ; hoặc máy đề xuất, người chốt). Chỗ nào có tay người là chỗ cần một cổng canh, ghi ở cột cuối.</p>
""", bang_nm(), """
<h2>§2 · Đã sửa gì</h2>
<p class="note"><b>v0.6.1 (owner, 06/11, bình luận trên hình):</b> đổi tên bốn agent — Agent 1 <b>Collect_raw_data</b> · Agent 2 <b>Generate Group Ledger (ITL raw)</b> · Agent 3 <b>Filter Fulfill &amp; Adjust (ITL Adjust)</b> · Agent 4 <b>Auditor (Compounding Loop)</b>. Phạm vi hộp của từng agent giữ nguyên. Nguồn PP (3) theo PD Now: GI · OMC từ Looker, SC · PS từ Google Sheets.</p>
<p class="note"><b>v0.6 (KhanhCQ, 06/11):</b> tách hai trang; nhúng bản kiểm TO-BE theo AS-IS (§1a) và bản AP fleet eval. <b>Agent kiểm dùng mô hình khác agent làm:</b> A4 SOÁT chạy gpt-oss-20b, A1–A3 chạy Qwen 3.8-27B; nhãn mô hình hiện trên từng nhãn agent ở lề trái hình 1.</p>
<p class="note"><b>v0.5 (KhanhCQ, 06/11):</b> <b>TO-BE thay thế, cải tiến và bao gồm AS-IS</b> — không chạy song song (kiểm từng bước: <code>docs/ITL/02_BA/Artifacts/Kiem-TOBE-theo-ASIS.md</code>). Agent dự kiến: <b>Qwen 3.8-27B chạy local</b>. PP (2) <b>nạp thẳng sổ H1000</b> (đã tách HD · CDT1 · pháp nhân tới từng nhân viên) và nối giao dịch bank theo Số CT, bỏ phép tự khớp Σ đợt theo venture. PP (3) đi qua <b>PE/PM</b> bằng Combine Code rồi tới bank txns, chia theo <b>CDT1</b>. SC = server cost. Pháp nhân TK lấy từ <b>tên sheet R + Mapping Master</b>; ảnh đọc thêm <code>Reference number_adjust</code> (người đè mã). Ô bỏ trống ở vùng chỉnh tay <b>giữ giá trị mặc định như AS-IS</b> (parity: CDT1 = SHQ2, ID đối tác = VD0, …).</p>
<p class="note"><b>v0.4.1 (owner, 06/11):</b> nửa TO-BE hiện rõ các agent — mỗi agent một <b>dải màu</b> trải ngang (cùng màu nhãn ở lề); Agent 3 tách thành <b>ba agent mapping</b> A3.1 (PP 1 · Reference No) · A3.2 (PP 2 · lương / BH) · A3.3 (PP 3 · nền tảng), chip trên hộp bấm được. Thêm <b>§8</b>: chi phí máy chủ ↔ mô hình mã nguồn mở tự huấn luyện.</p>
<p class="note"><b>v0.4 (owner, 06/11):</b> đặt luồng <b>AS-IS</b> (sơ đồ "Voi ITL AS-IS") <b>cạnh</b> TO-BE trong <b>một</b> hình — AS-IS bên phải; AS-IS xếp vào đúng các lớp của TO-BE, <b>không sinh lớp mới</b>; 52 hộp gốc gộp thành 28 hộp, mỗi hộp gộp giữ đủ chi tiết gốc trong khung bấm. Bỏ bớt chữ để thu nhỏ: hộp chỉ còn tên + một dòng, nhãn máy/người thành vạch màu mép trái. Hai hộp FPS gộp thành <i>sổ cái PM · PC</i> (bỏ o2, x2). Mũi tên dọc nay tự đặt giữa phần hai hộp chồng nhau. Hình cao 736 thay vì 1.206.</p>
<p class="note"><b>v0.3 (owner, 04/11):</b> nguồn FPS là <b>sổ cái PM / PC</b>, đã mang đủ chiều ⇒ bỏ hai hộp "phiếu PE·PI·PM·PC" và "danh mục FPS"; bước dựng đổi từ <i>DỰNG chuỗi phiếu</i> (đi PM → PI → PE) thành <i>DỰNG dòng lệnh</i> (đọc thẳng từng dòng sổ cái). Đề xuất pháp nhân TK (k1) nay đếm từ TK chi + pháp nhân thanh toán trên sổ cái PM.</p>
<p class="note"><b>v0.3.1–v0.3.2 (owner, 04/11, bình luận trên hình):</b> tách riêng ba phương pháp xử lý nguồn Sheets. <b>(1) mapping với bank transaction</b> — đủ hai vế PS Nợ (tiền vào) và PS Có (tiền ra), soát số dư ngày theo CCR / CCR Cash — sao kê &amp; sổ quỹ: kế toán dán / ghi → bản khai nguồn → ảnh chụp đọc theo bản khai → DỰNG dòng tiền; dòng tiền chưa mang chiều chi phí nên phải <b>mapping với bank txns theo reference number</b> (hộp MAPPING: mã Reference number trên giao dịch ngân hàng ↔ cùng mã trên dòng sổ cái PM, chia tiền theo PM line). PP (2), (3) cũng mapping với bank txns nhưng bằng luật riêng (§1b, §1c), không qua Reference No của PM. Sửa tay (GHI tay → lớp sửa) là bước chung cho mọi dòng sổ, không riêng phương pháp nào. <b>(2) lương · BHXH · BHYT</b> — sổ lương HR: HR lập → ảnh sổ lương → DỰNG đợt lương · BH. <b>GĐ1:</b> luật mapping các đợt đi tiền lương / BHXH / BHYT của các venture với bank txns → gắn <b>LE</b> (§1b). <b>GĐ2:</b> mapping xuống <b>KRF</b>. <b>(3) 4 chi phí nền tảng OMC · GI · SC · PS</b> — không có trên FPS: xuất file từ data Looker → mapping với bank txns, mỗi loại một luật → allocate về các ventures (§1c). Vùng nguồn Sheets tách làm ba; hộp "ảnh sổ nhập tay" tách làm ba; mỗi phương pháp là một khung đi từ nguồn xuống tới bước dựng.</p>
<p>Năm chỗ bản v0.1 vẽ sai, sửa từ v0.2:</p>
<ol class="fix">
<li><b>Bản khai nguồn đứng trước phép chụp.</b> Ảnh sao kê đọc vùng chuẩn <i>theo</i> bản khai và ghi lại <code>khai_version</code> (<code>fls/repo/chup.py:16</code>, <code>tools/chup_sao_ke.py</code>).</li>
<li><b>Pháp nhân của dòng tiền phải có lúc DỰNG.</b> <code>fls_itl</code> chỉ-thêm và pháp nhân là cột của dòng sổ ⇒ luật gắn pháp nhân nằm trong bản khai của nguồn (người khai, owner ký), đọc ở bước dựng.</li>
<li><b>Hai đường ghi tách bạch.</b> Máy ghi cả lượt nạp trong <i>một</i> giao dịch (<code>chay_nap.py:621</code>); người ghi qua <code>ghi_tay.py</code>, chỗ ghi duy nhất.</li>
<li><b>Năm điểm khởi động vẽ riêng.</b> Nhịp mỗi giờ chỉ <i>chụp</i>; khai nguồn, xem lô, Nhận lô, ghép/sửa là bốn cú bấm khác nhau của kế toán.</li>
<li><b>"Một bảng ITL duy nhất" là sổ hiệu lực</b> (sổ gốc + lớp sửa), không chỉ <code>fls_itl</code>.</li>
</ol>

<h2>§3 · Mũi tên nói gì — mũi tên TO-BE, 5 nhóm</h2>
<p>Mỗi mũi tên là <b>một dòng dữ liệu</b>: nó chở gì, nối bằng khoá nào, một-nhiều ra sao, cổng nào đứng trên nó, và hôm nay đã chảy chưa. Bấm một dòng để thấy nó trên hình.</p>
""",
         bang_ten(),
         '<h2>§4 · Kiểm cạnh — mỗi hộp: vào gì, ra gì, khớp mã nào</h2>'
         '<p>Máy sinh từ cùng bản khai với hình: cột <i>vào</i>/<i>ra</i> là mã mũi tên, nên một mũi tên thiếu trên hình cũng thiếu ở đây.</p>',
         bang_canh(),
         """
<h2>§5 · Hợp đồng dữ liệu sổ cái PM / PC → FLS</h2>
<p>Trường cần có lấy từ các nhóm khoá của bản gốc. Cột <i>sổ PM hôm nay</i> đối chiếu với <b>28 cột</b> FLS đang đọc từ sổ PM qua Sheets (<code>fls/adapters/pm_join.py</code>: 14 cột đã đặt kiểu · 1 cột cấm · 13 cột còn thô). "Cần xác nhận" = sổ PM hôm nay chưa có cột ấy; theo owner sổ cái FPS có đủ, cần FPS cho tên cột.</p>
<div class="scroll"><table>
<thead><tr><th colspan="2" class="sup">Hợp đồng</th><th class="sup">FLS</th><th colspan="2" class="sup">Đối chiếu</th></tr>
<tr><th>trường</th><th>nhóm khoá</th><th>đích trong FLS</th><th>sổ PM hôm nay</th><th>sổ PC</th></tr></thead>
<tbody>
<tr class="b1"><th colspan="5">Tiền và tham chiếu</th></tr>
<tr><td>số tiền · tiền tệ của line</td><td>General Trustest</td><td>ghép: Σ line = tiền dòng (g1)</td><td><span class="pill ok">có kiểu · cột 9, 8</span></td><td><span class="pill no">cần xác nhận</span></td></tr>
<tr><td>Reference No</td><td>Statement Ref No</td><td>khoá ghép tiền ↔ lệnh chi (c3)</td><td><span class="pill ok">có kiểu · cột 25</span></td><td><span class="pill ext">không cần</span></td></tr>
<tr><td>ngân hàng · số TK chi</td><td>General Trustest (LE qua TK)</td><td>k1: đề xuất pháp nhân TK</td><td><span class="pill mid">thô</span></td><td><span class="pill ext">không cần</span></td></tr>
<tr><td>ngày thực chi</td><td>General Trustest</td><td>đối chiếu ngày với sao kê</td><td><span class="pill no">cần xác nhận</span> (chỉ có dấu thời điểm lập)</td><td><span class="pill no">cần xác nhận</span></td></tr>
<tr class="b1"><th colspan="5">Khoá chuỗi</th></tr>
<tr><td>ID PM slip · ID PM line</td><td>khoá PM</td><td><code>pm_line_id</code> của mối nối</td><td><span class="pill ok">có kiểu · cột 15, 16</span></td><td>PM gốc: <span class="pill no">cần xác nhận</span></td></tr>
<tr><td>ID PE slip · ID PE line (+ tạm ứng / gấp)</td><td>khoá PE</td><td>chiều lệnh chi</td><td><span class="pill ok">có kiểu · cột 17, 18, 3, 4</span></td><td>PE gốc: <span class="pill no">cần xác nhận</span></td></tr>
<tr><td>ID PI slip · ID PI line</td><td>khoá PI</td><td>chiều lệnh chi</td><td><span class="pill ok">có kiểu · cột 19, 20</span></td><td><span class="pill ext">không cần</span></td></tr>
<tr><td>ID PC slip · ID PC line</td><td>khoá PC</td><td><code>pc_line_id</code></td><td><span class="pill ext">không có</span></td><td><span class="pill no">cần xác nhận</span></td></tr>
<tr class="b1"><th colspan="5">Chiều chi phí</th></tr>
<tr><td>Budget Code (HD/KRF)</td><td>khoá PE: Budget/KRF/HD</td><td><code>hd</code> (máy gợi ý → người chốt)</td><td><span class="pill ok">có kiểu · cột 21</span></td><td><span class="pill no">cần xác nhận</span></td></tr>
<tr><td>Chủ dự toán CDT1</td><td>CDT</td><td><code>cdt1</code></td><td><span class="pill ok">có kiểu · cột 22</span> (+ biến thể "Chủ dự toán *" còn thô)</td><td><span class="pill no">cần xác nhận</span></td></tr>
<tr><td>loại giao dịch (Payment Type)</td><td>khoá PE: Singular/Advance</td><td><code>pay_type</code></td><td><span class="pill mid">thô</span></td><td><span class="pill ext">không cần</span></td></tr>
<tr class="b1"><th colspan="5">Pháp nhân và đối tác</th></tr>
<tr><td>pháp nhân thanh toán</td><td>General Trustest: LE</td><td><code>le_payer</code></td><td><span class="pill mid">thô · đầy 100%</span></td><td><span class="pill no">cần xác nhận</span></td></tr>
<tr><td>đối tác nhận (ID Payee) + đối tác có phải pháp nhân Apero</td><td>khoá PE: Vendor ID</td><td><code>id_payee</code> · <code>le</code> (pháp nhân nhận)</td><td><span class="pill no">cần xác nhận</span> (hôm nay ở PE, 95%)</td><td><span class="pill ext">không cần</span></td></tr>
<tr><td>tên TK nhận</td><td>—</td><td>giữ trong kho, không đưa lên bề mặt (owner 11/09)</td><td><span class="pill mid">thô</span></td><td><span class="pill ext">không cần</span></td></tr>
<tr><td>email người lập</td><td>—</td><td><b>cấm vào kho</b> (<code>PM_COT_RIENG_TU</code>)</td><td><span class="pill ext">có, bị chặn</span></td><td>—</td></tr>
<tr class="b1"><th colspan="5">Kỳ và trạng thái</th></tr>
<tr><td>trạng thái cuối</td><td>—</td><td>chỉ đọc dòng đã duyệt</td><td><span class="pill ok">có kiểu · cột 24</span></td><td><span class="pill no">cần xác nhận</span></td></tr>
<tr><td>kỳ dịch vụ: bắt đầu · kết thúc</td><td>khoá PI / PE</td><td><code>svc_start</code> · <code>svc_end</code></td><td><span class="pill no">cần xác nhận</span> (hôm nay ở PI)</td><td><span class="pill ext">không cần</span></td></tr>
</tbody></table></div>
<p class="note"><b>Ba cột phải hỏi FPS trước khi viết bộ đọc:</b> ① <b>đối tác nhận</b> và cờ "đối tác là pháp nhân Apero": thiếu thì <code>le</code> rỗng và cờ nội bộ không bao giờ bật. ② <b>kỳ dịch vụ</b>: thiếu thì sai kỳ ghi nhận P&amp;L. ③ <b>khoá gốc của dòng PC</b> (PM hay PE): thiếu thì quyết toán không nối được về lệnh chi.</p>

<h2>§6 · Thứ tự làm trong GĐ1 — theo mũi tên</h2>
<div class="scroll"><table>
<thead><tr><th>bước</th><th>mũi tên / hộp dựng</th><th>vì sao đứng đây</th><th>cổng đóng bước (mong)</th></tr></thead>
<tbody>
<tr class="b1"><th colspan="4">Chặng I · Đóng họ tiền trên sổ đang có (bước 1–2)</th></tr>
<tr><td>1</td><td>k1 · b2 · cột pháp nhân TK trong bản khai nguồn</td><td>Rẻ nhất: tách tài khoản ra pháp nhân đã đo 8.387/8.387 trên 49 nguồn; đổi ngay chiều pháp nhân của sổ đang có</td><td>pháp nhân TK rỗng = 0 hoặc danh sách có tên TK, owner ký (14 TK · 211 dòng)</td></tr>
<tr><td>2</td><td>x4 · x7 · b3 (lằn Cash + lằn CCR)</td><td>Cùng bộ đọc với sao kê, chỉ bật lằn; CCR cho số dư ngày để soát đủ hai vế PS Nợ · PS Có</td><td>số dòng = sổ quỹ từng quỹ · nạp lại = 0 trùng · số dư đầu + Σ Nợ − Σ Có = số dư CCR / CCR Cash từng TK từng ngày (DIF = 0)</td></tr>
<tr class="b1"><th colspan="4">Chặng II · Mở họ lệnh chi và chi phí (bước 3–5)</th></tr>
<tr><td>3</td><td>x1 · b1 · g1 (sổ cái PM + PC)</td><td>Hợp đồng §5 chốt trước; đặt kiểu 13 cột PM còn thô; ảnh sổ cái dùng lại lằn ảnh chụp, không dựng hệ thứ hai</td><td>0 khoá lệnh chi trỏ rỗng · chiều lệnh chi khớp sổ đang chạy 100% từng ô</td></tr>
<tr><td>4</td><td>x5 · b4 · g4 (PP 2 · lương / BHXH / BHYT)</td><td>Nạp thẳng H1000 đã tách (06/11) — không tự khớp Σ; khoá là Số CT kế toán đã dán</td><td>mọi dòng lương nối được Số CT (hoặc hàng chờ có tên) · Σ Có = Σ Nợ mỗi đợt · đủ tháng, 0 tháng trùng</td></tr>
<tr><td>5</td><td>x6 · b5 · g5 (PP 3 · OMC · GI · SC · PS)</td><td>Có PE/PM (sửa 06/11): dòng ITL ⨝ nguồn GI · OMC (Looker) · SC · PS (Gsheet) theo Combine Code → chia CDT1 (§1c)</td><td>số dòng = 4 sổ nguồn · mọi giao dịch 4 loại khớp hoặc vào hàng chờ có tên · Σ phần chia = tiền giao dịch</td></tr>
<tr class="b1"><th colspan="4">Chặng III · Chứng minh một bảng (bước 6–7)</th></tr>
<tr><td>6</td><td>h2 · h3 · sổ hiệu lực thành một view có tên</td><td>Hôm nay màn tự ghép ở cửa đọc; hệ khác cần một bảng</td><td>một SELECT trả đủ 4 họ nguồn · đủ 3 vai pháp nhân</td></tr>
<tr><td>7</td><td>h1 · h4 · v1 · v4 (cổng GĐ1 + xuất đối chiếu)</td><td>Hợp nhất chỉ chứng minh được khi cả 4 họ đã vào</td><td>Σ theo pháp nhân = Σ theo nguồn, từng tiền tệ · chênh với sổ đang chạy liệt kê từng dòng, có tên</td></tr>
</tbody></table></div>

<h2>§7 · Câu chờ owner</h2>
<div class="scroll"><table>
<thead><tr><th>#</th><th>câu</th><th>vì sao phải hỏi</th><th>chặn</th></tr></thead>
<tbody>
<tr><td>1</td><td><b><code>le</code> nghĩa là gì?</b> Đề xuất: tách ba vai thành ba trường — pháp nhân TK (mới, từ bản khai) · <code>le_payer</code> (sổ cái PM) · <code>le</code> = pháp nhân nhận. "Chi phí về pháp nhân" ở GĐ1 = pháp nhân TK.</td><td>Hai tài liệu nói khác nhau: <code>00_MASTER_INDEX</code> (<code>QĐ-ITL-144</code>) ghi <code>le</code> "suy được 100% từ <code>source_sheet</code>" (tức chủ TK); <code>05_DATA_DICTIONARY_ERD</code> §ⓑ ghi <code>le</code> = "ai nhận" ← đối tác</td><td>bước 1</td></tr>
<tr><td>2</td><td>Pháp nhân TK nằm trong <b>bản khai nguồn</b> (máy đề xuất, kế toán khai, owner ký) — đồng ý? Tên pháp nhân chuẩn lấy từ đâu?</td><td>14 TK · 211 dòng có tên TK không nói pháp nhân; hai bên còn gọi một pháp nhân bằng hai mã (<code>VVOH - Astronex</code> ↔ <code>ASTRONEX</code>); 24/29 mã thiếu tên</td><td>bước 1</td></tr>
<tr><td>3</td><td>FPS cấp sổ cái PM / PC qua <b>kết nối CSDL chỉ-đọc</b> hay <b>xuất bảng định kỳ</b>? Và ba cột ở cuối §5 có trong sổ cái không?</td><td>Quyết định tuyến của x1 và việc chiều lệnh chi có đủ không; hôm nay sổ PM đi qua Sheets</td><td>bước 3</td></tr>
<tr><td>4</td><td>HR và nền tảng: FLS đọc sổ ở Sheets như hôm nay, hay chờ hệ nguồn có hợp đồng?</td><td>Quyết định tuyến của x5/x6</td><td>bước 4–5</td></tr>
<tr><td>5</td><td>⭐ <b>Đã trả lời 06/11:</b> chia theo <b>CDT1</b> (như AS-IS), qua PE/PM. Câu cũ: PP (3): "venture" khi allocate là <b>LE</b> hay <b>CDT1</b>? Tỉ lệ chia lấy từ cột nào của file Looker? AP/AR lùi khỏi GĐ1?</td><td>Owner 04/11 chốt OMC · GI · SC · PS là chi phí, mapping với bank txns rồi allocate về ventures — thay câu cũ "GI/OMC không vào sổ"</td><td>bước 5</td></tr>
</tbody></table></div>
""", bang_chi_phi(), '</section><section class="trang" id="trang-2" hidden>', bang_fleet_eval(), '</section>', """
<footer>Voi FLS-tobe-phase1 v0.6.1 · 2026-11-06 · Trang 1 mapping TO-BE ↔ AS-IS · Trang 2 fleet eval · sinh bởi <code>docs/ITL/_tools/sinh_voi_phase1.py</code> · cùng bộ với <code>_PD_NOW_VOI_VA_GIAI_DOAN.md</code>.</footer>
</main>
<aside class="khung-ct" id="khung-ct" hidden aria-label="Chi tiết phần đang chọn">
  <div class="dong"><span class="eb" style="font:600 11px var(--mono);letter-spacing:.06em;color:var(--muted)">CHI TIẾT</span><button class="dong-x" id="nut-dong" type="button" aria-label="Đóng khung chi tiết">×</button></div>
  <div id="ct-noi-dung"></div>
</aside>
"""]
    o.append(f'<script type="application/json" id="du-lieu">{du_lieu_js()}</script>')
    o.append(f'<script>{JS}</script>')
    return "\n".join(o)


def main() -> int:
    k = kiem()
    print(f"hộp {k['hop']} · mũi tên {k['ten']} (dọc {k['doc']} · ngang {k['ngang']}) · cắt nhau {k['cheo']}")
    for d in DAI:
        print(f"  dải {d}: {so_muc(d)} mục")
    km = kiem_m()
    print(f"hình phóng to: hộp {len(HOP_M)} · mũi tên {len(TEN_M)} · lỗi {len(km)}")
    ka = kiem_a()
    print(f"AS-IS: hộp {len(HOP_A)} (gộp {sum(len(h.goc) for h in HOP_A)}/{len(ASIS_GOC['hop'])} hộp gốc) · "
          f"mũi tên {len(TEN_A)} (chở {sum(len(t.goc) for t in TEN_A)}/{len(ASIS_GOC['ten'])} mũi tên gốc, còn lại nằm trong hộp) · lỗi {len(ka)}")
    if k["loi"] or km or ka:
        print("⛔ LỖI:\n  " + "\n  ".join(k["loi"] + km + ka))
        return 1
    if "--kiem" in sys.argv:
        print("✅ hình đúng luật — ⛔ không ghi (--kiem)")
        return 0
    DICH.write_text(trang(), encoding="utf-8")
    print(f"✅ đã ghi {DICH.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
