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
W, H = 1420, 1206
C0 = (128, 236)                         # cột 0: điểm khởi động của vùng FLS


def cot(i: int) -> tuple[int, int]:
    x = 248 + (i - 1) * 167
    return x, x + 157


def nhip(a: int, b: int, trai: int = 0, phai: int = 0) -> tuple[int, int]:
    return cot(a)[0] + trai, cot(b)[1] - phai


def tam(i: int) -> float:
    a, b = cot(i)
    return (a + b) / 2


# dải: (vùng, y, cao, nhãn rail)
DAI = {
    "A0": ("A", 40, 46, "ai sinh ra"),
    "A1": ("A", 118, 74, "sổ nguồn"),
    "B0": ("B", 40, 46, ""),
    "B1": ("B", 118, 74, ""),
    "G0": ("G", 40, 46, ""),
    "G1": ("G", 118, 74, ""),
    "H0": ("H", 40, 46, ""),
    "H1": ("H", 118, 74, ""),
    "c1": ("C", 290, 84, "① KHAI & CHỤP"),
    "c2": ("C", 410, 78, "② DỰNG"),
    "c3": ("C", 524, 78, "③ MAPPING"),
    "c4": ("C", 638, 78, "④ SOÁT"),
    "c5": ("C", 752, 78, "⑤ GHI"),
    "d1": ("D", 878, 78, "⑥ SỔ GỐC"),
    "d2": ("D", 992, 72, "⑦ HIỆU LỰC"),
    "e1": ("E", 1112, 70, "⑧ NGƯỜI THẤY"),
}
TANG = {"A0": 0, "B0": 0, "G0": 0, "H0": 0, "A1": 1, "B1": 1, "G1": 1, "H1": 1, "c1": 2, "c2": 3, "c3": 4, "c4": 5, "c5": 6, "d1": 7, "d2": 8, "e1": 9}
VUNG = {   # mã: (nhãn, nhãn phụ, y0, y1)
    "C": ("FLS · NẠP", "chưa vào sổ", 266, 842),
    "D": ("FLS · SỔ", "PostgreSQL · chỉ-thêm", 854, 1076),
    "E": ("ĐẦU RA", "màn FLS + hệ khác", 1088, 1194),
}
TEN_VUNG = {"A": "Nguồn ngoài · FPS", "B": "Phương pháp xử lý (1) · mapping với bank transaction — sao kê & sổ quỹ",
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
    khoi: str = ""                   # khung chứa (vd "pp1" = phương pháp xử lý 1) — tính MỘT mục khi đếm dải

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
    Hop("oPM", "A0", cot(1), "o", "b", "LẬP & DUYỆT PM", ("lệnh chi trong FPS",),
        doi_chieu="ngoài FLS — FLS chỉ đọc dòng đã vào sổ cái"),
    Hop("oPC", "A0", cot(2), "o", "b", "LẬP & DUYỆT PC", ("quyết toán trong FPS",),
        doi_chieu="ngoài FLS"),
    Hop("soPM", "A1", cot(1), "x", "b", "sổ cái PM",
        ("1 dòng = 1 PM line", "PE·PI · HD · CDT1 · Ref No"), "28 cột · 3.772 dòng",
        doi_chieu="AS-IS đọc qua tab PM_Unpivot: 28 cột có tên (pm_join.py, G-MOD-3) — 14 có kiểu · 1 cấm · 13 thô"),
    Hop("soPC", "A1", cot(2), "x", "b", "sổ cái PC",
        ("1 dòng = 1 PC line", "quyết toán · hoàn ứng"), "AS-IS: chưa đọc",
        doi_chieu="0 tham chiếu PC trong fls/ · tools/ · tests/"),
    # ── ngoài FLS · Google Sheets ──
    Hop("oKTnh", "B0", cot(4), "o", "b", "KẾ TOÁN NGÂN HÀNG", ("dán sao kê vào sheet R |",),
        doi_chieu="ngoài FLS — 60 dòng chảy ngân hàng có bản khai dòng 1"),
    Hop("oKTq", "B0", cot(5), "o", "b", "KẾ TOÁN QUỸ", ("ghi sổ quỹ hằng ngày",),
        doi_chieu="ngoài FLS — 8 dòng chảy quỹ có bản khai dòng 1"),
    Hop("oHR", "G0", cot(6), "o", "b", "HR · C&B", ("lập sổ lương",), doi_chieu="ngoài FLS"),
    Hop("oNT", "H0", cot(7), "o", "b", "DATA · LOOKER", ("xuất file chi phí",), doi_chieu="ngoài FLS — owner 04/11"),
    Hop("saoke", "B1", cot(4), "x", "b", "sao kê ngân hàng", ("60 dòng chảy", "19 bố cục cột"), "sheet R |",
        doi_chieu="tools/nap_nguon_va_khai.py (60 ngân hàng + 8 quỹ = 68 nguồn)"),
    Hop("soquy", "B1", cot(5), "x", "b", "sổ quỹ", ("8 dòng chảy", "kế toán ghi tay"), "sheet R |",
        doi_chieu="như trên"),
    Hop("soluong", "G1", cot(6), "x", "b", "sổ lương HR", ("4 sổ: 2 loại × 2 năm", "HD/KRF tách sẵn"), "sheet HR",
        doi_chieu="0 tham chiếu trong fls/ (chỉ chuỗi phương pháp ở mapping_master.py:31)"),
    Hop("sont", "H1", cot(7), "x", "b", "file xuất Looker", ("OMC · GI · Server · PS", "4 loại · 4 luật"), "không có trên FPS",
        doi_chieu="0 tham chiếu trong fls/ (Platform chỉ là enum)"),
    # ── c1 · KHAI & CHỤP ──
    Hop("S1", "c1", C0, "o", "b", "S1 · NHỊP", ("mỗi giờ 8h–19h",), tang="tren", khoi="kd1",
        doi_chieu="fls/repo/nhip_chup.py (QĐ-ITL-114) · tools/nhip_chup.py chụp Bank + PM"),
    Hop("S2", "c1", C0, "o", "b", "S2 · KHAI", ("kế toán · F04",), tang="duoi", khoi="kd1",
        doi_chieu="POST khai-cot · thu-tu (fls/api)"),
    Hop("anhFPS", "c1", (cot(1)[0], cot(2)[1] - 16), "d", "q", "ảnh sổ cái FPS",
        ("PM + PC, đóng băng mỗi lần chụp", "hôm nay: chỉ PM, đọc qua Sheets"), "fls_pm_line 3.772 · PC chưa có",
        huy=("S1",), doi_chieu="fls_pm_line (migration 0011/0023) · fls/repo/anh_pm.py; PC: chưa có bảng"),
    Hop("khai", "c1", (cot(3)[0] + 12, cot(3)[1] - 12), "d", "b", "bản khai nguồn",
        ("cột · thứ tự ngày", "+ pháp nhân: đề xuất"), "fls_khai_cot 408", huy=("S2",),
        doi_chieu="fls/repo/khai_cot.py (chỉ-thêm, có version); cột pháp nhân: chưa có", khoi="pp1"),
    Hop("anhTien", "c1", (cot(4)[0] + 16, cot(5)[1]), "d", "b", "ảnh sao kê & sổ quỹ",
        ("lằn Bank ✅ 60 nguồn · 182 ảnh · lằn Cash ⛔",
         "đọc vùng chuẩn THEO bản khai · không đọc Diễn giải"),
        "fls_chup · fls_chup_nguon (khai_version)", huy=("S1",),
        doi_chieu="tools/chup_sao_ke.py (LAN='Bank') · fls/repo/chup.py:16 khai_version", khoi="pp1"),
    Hop("anhHR", "c1", cot(6), "d", "q", "ảnh sổ lương HR",
        ("lằn HR ⛔", "đợt chi theo venture · kỳ"), "fls_chup lằn 'HR'", huy=("S1",),
        doi_chieu="chưa có: chup_sao_ke.py chỉ chụp lằn Bank", khoi="pp2"),
    Hop("anhNT", "c1", cot(7), "d", "q", "ảnh file Looker",
        ("lằn Platform ⛔", "bố cục cột: chưa chốt"), "fls_chup 'Platform'", huy=("S1",),
        doi_chieu="chưa có: chup_sao_ke.py chỉ chụp lằn Bank", khoi="pp3"),
    # ── c2 · DỰNG ──
    Hop("S3", "c2", C0, "o", "b", "S3 · XEM LÔ", ("kế toán chọn lô", "màn F04"),
        doi_chieu="POST /nap/lo/xem-truoc"),
    Hop("dLenh", "c2", nhip(1, 2), "p", "q", "DỰNG dòng lệnh",
        ("mỗi PM / PC line → tiền · Ref · HD/KRF", "· CDT1 · đối tác · kỳ DV · pháp nhân trả"),
        "khoá: pm_line_id · pc_line_id", huy=("S3", "S4"),
        doi_chieu="có một phần: fls_pm_line đặt kiểu 14 cột (PM_COT); PC + cột còn thô: chưa"),
    Hop("dTien", "c2", nhip(3, 5), "p", "b", "DỰNG dòng tiền",
        ("ảnh lằn Bank · Cash → canon 36 trường (General Trustest + TK)",
         "gắn pháp nhân TK từ bản khai của nguồn · content_key chống trùng"),
        "bank 8.338/8.338 · quỹ chưa chạy · pháp nhân: chưa", huy=("S3", "S4"),
        doi_chieu="fls/adapters/sao_ke.py + sao_ke_canon.py", khoi="pp1"),
    Hop("dHR", "c2", cot(6), "p", "q", "DỰNG đợt lương · BH",
        ("lương · BHXH · BHYT", "→ Σ mỗi đợt + LE venture"), "GĐ2: tách xuống KRF",
        huy=("S3", "S4"), khoi="pp2",
        doi_chieu="chưa có (adapter D) · owner 04/11: GĐ1 mapping đợt đi tiền → LE, GĐ2 → KRF"),
    Hop("dNT", "c2", cot(7), "p", "q", "DỰNG chi phí nền tảng",
        ("4 loại → canon", "→ mapping + allocate"), "chi tiết: §1c",
        huy=("S3", "S4"), doi_chieu="chưa có (adapter E)", khoi="pp3"),
    # ── c3 · MAPPING — tách theo nhóm (owner 04/11): phần chưa khớp chuyển NGANG sang nhóm kế ──
    Hop("ghep", "c3", (cot(1)[0], cot(5)[1] - 24), "p", "b", "MAPPING PP (1) · bank txns ↔ lệnh chi (Reference No)",
        ("Reference No → chia tiền theo PM line · Σ line = tiền dòng, lệch ⇒ chặn",
         "khác tiền tệ · N×M ⇒ để người · ra 3 lớp L1 · L2 · L3 (§1b)"),
        "hôm nay nối 26,79% dòng", huy=("S4",), khoi="m1",
        doi_chieu="fls/adapters/pm_join.py · chay_nap.py:637 chen_moi_noi"),
    Hop("ghep2", "c3", (cot(6)[0], cot(6)[1] - 18), "p", "q", "MAPPING PP (2)",
        ("đợt lương · BH", "↔ bank txns → LE"), "chi tiết §1b", huy=("S4",), khoi="m2",
        doi_chieu="chưa có · owner 04/11"),
    Hop("ghep3", "c3", cot(7), "p", "q", "MAPPING PP (3)",
        ("4 luật · khớp kỳ + Σ", "→ allocate venture"), "chi tiết §1c", huy=("S4",), khoi="m3",
        doi_chieu="chưa có · owner 04/11"),
    # ── c4 · SOÁT — mỗi nhóm một bộ luật soát ──
    Hop("soat", "c4", (cot(1)[0], cot(5)[1] - 24), "p", "b", "SOÁT PP (1)",
        ("9 luật sao kê · CHẶN ⇒ nguồn bị chừa · CỜ ⇒ vẫn ghi, vào hàng chờ có lý do",
         "Σ PM line = tiền dòng · 4 vế cân: vào = sổ + loại + rỗng + trùng · biên bản 9 dòng trên F04"),
        "fls/kiem/soat_nap.py", huy=("S3", "S4"), khoi="m1",
        doi_chieu="fls/kiem/soat_nap.py · chay_nap.py:611 cổng bốn đường · QĐ-ITL-112"),
    Hop("soat2", "c4", (cot(6)[0], cot(6)[1] - 18), "p", "q", "SOÁT PP (2)",
        ("Σ đợt = Σ giao dịch", "mọi đợt có LE"), "chưa có", huy=("S3", "S4"), khoi="m2",
        doi_chieu="chưa có"),
    Hop("soat3", "c4", cot(7), "p", "q", "SOÁT PP (3)",
        ("Σ phần chia = tiền", "Σ % venture = 100"), "chưa có", huy=("S3", "S4"), khoi="m3",
        doi_chieu="chưa có"),
    # ── c5 · GHI ──
    Hop("S4", "c5", C0, "o", "b", "S4 · NHẬN", ("kế toán · F04",), tang="tren", khoi="kd4",
        doi_chieu="POST /nap/lo"),
    Hop("S5", "c5", C0, "o", "b", "S5 · GHÉP·SỬA", ("kế toán · F01·F02",), tang="duoi", khoi="kd4",
        doi_chieu="POST match · adjust · reverse · …"),
    Hop("ghiNap", "c5", nhip(1, 7), "p", "b", "GHI lượt nạp — một giao dịch cho cả 3 nhóm",
        ("run · dòng sổ · dòng loại · mối nối máy (PP 1) · đợt gắn LE (PP 2) · phần chia venture (PP 3) · gợi ý hd/cdt1",
         "lỗi giữa chừng ⇒ ⛔ không còn dòng nào đã ghi"),
        "fls/repo/chay_nap.py — hôm nay chỉ phần PP (1)", huy=("S4",),
        doi_chieu="chay_nap.py:621 `with conn.transaction()`"),
    # ── d1 · SỔ GỐC ──
    Hop("loai", "d1", cot(1), "d", "b", "dòng bị loại", ("mỗi dòng một", "lý do có tên"), "fls_reject",
        doi_chieu="schema.py fls_reject"),
    Hop("soITL", "d1", nhip(2, 3), "d", "b", "SỔ ITL",
        ("một bảng · 4 họ nguồn (Bank·Cash·HR·Platform)", "chỉ-thêm · ⛔ không PUT/DELETE"),
        "fls_itl 8.387 · hôm nay 1 họ nguồn",
        doi_chieu="schema.py fls_itl · INV-I08 · source_system khai 4 giá trị"),
    Hop("lopSua", "d1", (cot(4)[0], cot(6)[1] - 24), "d", "b", "lớp sửa chỉ-thêm (gộp vẽ)",
        ("mối nối · bỏ nối · bút toán (người / máy gợi ý) · sự kiện · nhật ký",
         "sửa = thêm dòng · dòng sổ ⛔ không đổi một ô"),
        "fls_pm_link 2.263 · fls_adjustment 4.428 · fls_journal",
        doi_chieu="fls_pm_link · fls_pm_unlink · fls_adjustment · fls_queue_event · fls_journal"),
    Hop("ghiTay", "d1", cot(7), "p", "b", "GHI tay",
        ("ghép · sửa · đảo · lý do", "actor từ thẻ đăng nhập"),
        "chỗ ghi duy nhất", huy=("S5",),
        doi_chieu="fls/repo/ghi_tay.py"),
    # ── d2 · HIỆU LỰC ──
    Hop("kiem", "d2", (cot(1)[0], cot(1)[1] - 16), "p", "q", "KIỂM cổng GĐ1",
        ("mỗi cổng khai mong",), "đỏ khi khác",
        doi_chieu="/gates có 8 cổng · cổng GĐ1 (§3 nhóm 5): chưa"),
    Hop("hieuLuc", "d2", (cot(2)[0] + 16, cot(7)[1]), "d", "q", "SỔ ITL HIỆU LỰC — bảng ITL duy nhất của GĐ1",
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
    Hop("xuat", "e1", nhip(6, 7), "d", "q", "XUẤT cho hệ khác",
        ("GĐ1: khuôn sổ đang chạy, đối chiếu từng dòng", "GĐ4: hợp đồng xuất đủ chiều"),
        doi_chieu="fls/xuat/ chỉ có ghi_o.py; bộ xuất: chưa có"),
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
    x: float | None = None    # mũi tên dọc
    nhom: str = ""


TEN: list[Ten] = [
    # 1 · nguồn sinh ra
    Ten("o1", "oPM", "soPM", "b", "PM duyệt xong thì thành dòng sổ cái PM", "pm_line_id", "1 PM – n dòng",
        "FLS ⛔ không can thiệp luồng duyệt; chỉ đọc trạng thái cuối", "ngoài FLS", tam(1), "1a"),
    Ten("o2", "oPC", "soPC", "b", "PC duyệt xong thì thành dòng sổ cái PC", "pc_line_id", "1 PC – n dòng",
        "như o1", "ngoài FLS", tam(2), "1a"),
    Ten("o3", "oKTnh", "saoke", "b", "dán sao kê vào vùng chuẩn của sheet R |", "(dòng chảy, dòng)", "1 dòng chảy – n dòng",
        "bố cục cột theo bản khai dòng 1 (68/68 sheet khai đủ)", "ngoài FLS", tam(4), "1b"),
    Ten("o4", "oKTq", "soquy", "b", "ghi thu chi quỹ", "(dòng chảy quỹ, dòng)", "1 quỹ – n dòng",
        "như o3", "ngoài FLS", tam(5), "1b"),
    Ten("o5", "oHR", "soluong", "b", "lập sổ lương đã tách HD/KRF", "(sổ, năm, dòng)", "1 sổ – n dòng",
        "bề rộng cột đổi ⇒ bộ đọc nổ, ⛔ không đoán", "ngoài FLS", tam(6), "1c"),
    Ten("o6", "oNT", "sont", "b", "xuất file chi phí OMC · GI · Server · PS theo vendor · venture · tháng", "(loại, tháng, dòng)", "1 file – n dòng",
        "như o5", "ngoài FLS", tam(7), "1c"),
    # 2 · vượt ranh giới
    Ten("x1", "soPM", "anhFPS", "q", "dòng sổ cái PM: tiền · tiền tệ · Ref · khoá PE/PI · HD · CDT1 · pháp nhân trả · trạng thái",
        "pm_line_id", "1 lần chụp – n dòng",
        "bộ tiêu đề lệch hợp đồng ⇒ nổ to (như kiem_tieu_de_pm) · chụp 2 lần ⇒ 2 chup_id, ảnh cũ ⛔ không đổi · Email ⛔ không vào kho",
        "◐ có, đọc qua Sheets (3.772 dòng)", tam(1), "2a"),
    Ten("x2", "soPC", "anhFPS", "q", "dòng sổ cái PC: tiền · khoá PM/PE gốc · trạng thái", "pc_line_id", "1 lần chụp – n dòng",
        "như x1", "⛔ chưa đọc", tam(2), "2a"),
    Ten("x3", "saoke", "anhTien", "b", "vùng chuẩn, 5/6 trường (⛔ không Diễn giải)", "(nguồn, dòng) + khai_version",
        "1 nguồn – n dòng", "thiếu bản khai ⇒ nổ, nêu tên sheet · 429 ⇒ lùi rồi thử lại · nguồn 0 dòng vẫn có mặt",
        "✅ 60 nguồn · 182 ảnh", tam(4), "2b"),
    Ten("x4", "soquy", "anhTien", "q", "vùng chuẩn sổ quỹ", "(nguồn, dòng)", "1 quỹ – n dòng",
        "như x3 + số dư theo ngày nếu nguồn có", "⛔ lằn Cash chưa bật (GAP-CANON-02)", tam(5), "2b"),
    Ten("x5", "soluong", "anhHR", "q", "4 sổ lương theo năm", "(sổ, năm, dòng)", "1 sổ – n dòng",
        "Σ Nợ/Có từng sổ phải bằng sổ nguồn", "⛔", tam(6), "2c"),
    Ten("x6", "sont", "anhNT", "q", "file chi phí 4 loại", "(loại, tháng, dòng)", "1 file – n dòng",
        "như x5", "⛔", tam(7), "2c"),
    # 3 · khai & dựng
    Ten("k1", "anhFPS", "khai", "n", "đề xuất pháp nhân TK: TK chi + pháp nhân thanh toán trên sổ cái PM, đếm theo nguồn",
        "số TK ↔ nguồn", "1 nguồn – 1 pháp nhân",
        "máy đề xuất, kế toán khai, owner ký · nguồn có >1 pháp nhân ⇒ ⛔ không đề xuất · ⛔ không regex (14 TK · 211 dòng)",
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
    Ten("b4", "anhHR", "dHR", "q", "dòng sổ lương: venture · kỳ · loại (lương / BHXH / BHYT) · tiền", "chup_id + dòng", "n – 1 đợt",
        "dòng thiếu venture ⇒ hàng chờ có tên (mong 0)", "⛔", tam(6), "3b"),
    Ten("b5", "anhNT", "dNT", "q", "dòng lằn Platform", "chup_id + dòng", "1 – 1",
        "dòng thiếu pháp nhân ⇒ hàng chờ có tên", "⛔", tam(7), "3b"),
    # 4 · mapping, soát, ghi — tách theo nhóm
    Ten("g1", "dLenh", "ghep", "q", "mỗi PM line: tiền · tiền tệ · Reference No · chiều chi phí", "pm_line_id", "1 – 1",
        "N line một phiếu nói N giá trị ⇒ 'không suy được', ⛔ không lấy dòng đầu (INV-I16)",
        "◐ có phần PM, chưa đủ chiều", 410.0, "4a"),
    Ten("g2", "dTien", "ghep", "b", "dòng tiền canon + Reference No", "content_key", "1 dòng tiền – n PM line",
        "Σ tiền các line = tiền dòng · khác tiền tệ ⇒ để người (chờ tỷ giá, GĐ2)", "✅", 827.0, "4a"),
    Ten("g3", "dHR", "ghep2", "q", "đợt lương / BHXH / BHYT: venture · kỳ · Σ tiền · LE", "(venture, kỳ, loại)", "1 đợt – n giao dịch bank",
        "đợt không ra LE ⇒ hàng chờ", "⛔", 1140.0, "4a"),
    Ten("g4", "dNT", "ghep3", "q", "chi phí nền tảng 4 loại theo vendor · venture · tháng", "(loại, vendor, tháng)", "n – 1 kỳ",
        "loại lạ ⇒ chặn, nêu tên loại", "⛔", tam(7), "4a"),
    Ten("q1", "ghep", "ghep2", "q", "giao dịch bank còn ở lớp L3 sau PP (1)", "content_key", "—",
        "chỉ chuyển dòng chưa khớp; dòng đã khớp ⛔ thử lại ở nhóm sau", "⛔", None, "4b"),
    Ten("q2", "ghep2", "ghep3", "q", "giao dịch bank còn lại sau PP (2)", "content_key", "—",
        "còn lại sau PP (3) ⇒ ở L3, vào vòng cộng dồn §1b", "⛔", None, "4b"),
    Ten("w1", "ghep", "soat", "b", "mối nối dự kiến + dòng tiền canon", "(content_key, pm_line_id)", "1 – n",
        "9 luật soát chạy theo TỪNG nguồn (⛔ nối phẳng 60 nguồn)", "✅", 410.0, "4c"),
    Ten("w2", "ghep2", "soat2", "q", "đợt đã khớp + LE", "(venture, kỳ, loại)", "1 – n",
        "Σ đợt = Σ giao dịch", "⛔", 1140.0, "4c"),
    Ten("w3", "ghep3", "soat3", "q", "giao dịch khớp + phần chia venture", "(content_key, venture)", "1 – n",
        "Σ phần chia = tiền giao dịch", "⛔", tam(7), "4c"),
    Ten("r1", "soat", "ghiNap", "b", "dòng đạt + dòng loại + cờ + mối nối", "content_key", "1 – 1",
        "CHẶN ⇒ 0 dòng của nguồn ấy · 4 vế không cân ⇒ ⛔ không ghi gì", "✅", 827.0, "4d"),
    Ten("r2", "soat2", "ghiNap", "q", "đợt đạt soát, đã gắn LE", "(venture, kỳ, loại)", "—",
        "đợt lệch ⇒ ⛔ ghi, vào hàng chờ", "⛔", 1140.0, "4d"),
    Ten("r3", "soat3", "ghiNap", "q", "phần chia venture đạt soát", "(content_key, venture)", "—",
        "lệch Σ ⇒ ⛔ ghi cả giao dịch ấy", "⛔", tam(7), "4d"),
    Ten("s1", "ghiNap", "loai", "b", "dòng bị loại + lý do", "run_id + dòng nguồn", "1 – 1",
        "mỗi dòng loại có lý do có tên", "✅", tam(1), "4e"),
    Ten("s2", "ghiNap", "soITL", "b", "dòng sổ: General Trustest + TK + pháp nhân + run_id", "content_key UNIQUE", "1 – 1",
        "trùng ⇒ ⛔ không ghi, đếm vế 'trùng' · nạp lại cùng ảnh ⇒ vào sổ = 0", "✅ (pháp nhân còn rỗng)", 577.0, "4e"),
    Ten("s3", "ghiNap", "lopSua", "b", "mối nối máy · đợt gắn LE · phần chia venture · gợi ý (nguồn = máy)", "itl_id", "1 – n",
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
    Ten("v4", "hieuLuc", "xuat", "q", "sổ hiệu lực theo khuôn sổ đang chạy", "số chứng từ + ngày + TK", "1 – 1",
        "chênh liệt kê TỪNG dòng, mọi chênh có tên lý do, ⛔ không phần trăm", "⛔ bộ xuất chưa có", 1245.0, "5b"),
]

NHOM = {
    "1": "Nhóm 1 · Nguồn sinh ra (o1–o6)", "1a": "FPS (o1–o2)", "1b": "Phương pháp (1) · mapping với bank transaction — sao kê & sổ quỹ (o3–o4)",
    "1c": "Phương pháp (2) · HR và (3) · nền tảng (o5 · o6)",
    "2": "Nhóm 2 · Vượt ranh giới vào FLS (x1–x6)", "2a": "FPS → FLS · đọc sổ cái chỉ-đọc (x1–x2)",
    "2b": "Phương pháp (1) · Sheets API, tài khoản dịch vụ chỉ-đọc, đọc theo bản khai (x3–x4)",
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
        ("PP (2): lương · BHXH", "· BHYT, Σ venture · kỳ"),
        "đã DỰNG (b4)", doi_chieu="owner 04/11: GĐ1 → LE, GĐ2 → KRF"),
    Hop("mBank", "m1", cotm(3, 4), "d", "b", "bank transactions",
        ("dòng tiền đã DỰNG (b3)", "TK · ngày · Nợ/Có · Ref · nội dung"),
        "nội dung: chưa đọc (QĐ-ITL-92)", doi_chieu="fls_itl 8.387 · memo rỗng 8.387/8.387"),
    Hop("mLuatGhep", "m1", cotm(5, 6), "d", "q", "luật ghép đã ký",
        ("VN: Ref + tiền + pháp nhân · ngoài: từ khoá + vendor + tiền",
         "lương / BH: TK chi + nội dung + Σ đợt venture · kỳ → LE"),
        "QĐ-ITL-144 · máy mới dùng Ref + tiền", doi_chieu="QĐ-ITL-144 (owner + kế toán 18/09)"),
    Hop("mMap", "m2", cotm(1, 5), "p", "b", "MAPPING bank txns ↔ lệnh chi",
        ("chạy luật ghép theo thứ tự; Σ tiền các PM line = tiền giao dịch, lệch ⇒ chặn",
         "khác tiền tệ · N×M ⇒ để người, ⛔ không đoán, ⛔ không chia bừa"),
        "fls/adapters/pm_join.py · fls/repo/may_ghep.py", doi_chieu="pm_join.py hình A–F · INV-I16"),
    Hop("mBB", "m2", cotm(6), "d", "q", "biên bản mapping",
        ("đếm 3 lớp", "+ lý do có tên"), "mỗi lượt nạp", doi_chieu="hôm nay: /queue/coverage · /queue/mau-so"),
    Hop("mL1", "m3", cotm(1, 2), "d", "b", "L1 · khớp",
        ("Ref chung + Σ khớp, hoặc khớp đợt lương / BH", "→ mối nối · LE venture (s3)"),
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
    Ten("m15", "mHR", "mMap", "q", "đợt lương / BHXH / BHYT: venture · kỳ · Σ tiền · LE", "(venture, kỳ, loại)", "1 đợt – n giao dịch",
        "Σ giao dịch ghép vào một đợt = Σ đợt; lệch ⇒ chặn", "⛔ chưa có", tamm(2)),
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
# Owner 04/11: OMC · GI · Server · PS ⛔ có trên FPS ⇒ xuất file từ data Looker → mapping với bank txns
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
    Hop("nFile", "n1", cotn(1, 3), "x", "b", "file xuất Looker (đã chụp, b5)",
        ("OMC · GI · Server · PS — mỗi dòng: loại · vendor · app/venture · tháng · tiền",
         "không có trên FPS ⇒ không có Reference No"), "4 loại · 4 luật", doi_chieu="owner 04/11"),
    Hop("nBank", "n1", cotn(4, 5), "d", "b", "bank txns chưa ghép (L3)",
        ("giao dịch không có trên FPS (§1b)", "TK · ngày · tiền · tiền tệ · nội dung"),
        "nội dung: chờ nới QĐ-ITL-92", doi_chieu="hàng chờ UNMAPPED"),
    Hop("nLuat", "n1", cotn(6), "d", "n", "4 luật mapping",
        ("1 luật / loại", "người ký"), "owner điền", doi_chieu="chờ owner — xem bảng §1c"),
    Hop("nTach", "n2", cotn(1), "p", "n", "TÁCH tỉ lệ venture",
        ("từ chính file", "Looker"), "mỗi loại · tháng", doi_chieu="đề xuất"),
    Hop("nMap", "n2", cotn(2, 6), "p", "n", "MAPPING chi phí nền tảng ↔ bank txns",
        ("áp luật của từng loại: nhận diện giao dịch · khớp kỳ · khớp Σ tiền",
         "lệch ⇒ chặn, ⛔ chia bừa · giao dịch khớp ≥ 2 loại ⇒ để người"), "không đi qua FPS", doi_chieu="đề xuất"),
    Hop("nTyLe", "n3", cotn(1), "d", "n", "tỉ lệ venture",
        ("loại · tháng ·", "venture · %"), "Σ % = 100", doi_chieu="đề xuất"),
    Hop("nKhop", "n3", cotn(2, 3), "d", "n", "khớp",
        ("giao dịch ↔ chi phí kỳ của một loại", "→ mối nối"), "Σ chi phí kỳ = Σ giao dịch", doi_chieu="đề xuất"),
    Hop("nCho", "n3", cotn(4, 5), "d", "n", "có trên Looker, chưa có tiền",
        ("chi phí kỳ chưa thấy giao dịch", "tuổi > N ngày ⇒ cờ"), "giống L2 của §1b", doi_chieu="đề xuất"),
    Hop("nCon", "n3", cotn(6), "d", "n", "tiền chưa khớp",
        ("ở lại L3, vào", "vòng cộng dồn §1b"), "UNMAPPED", doi_chieu="đề xuất"),
    Hop("nAlloc", "n4", cotn(1, 3), "p", "n", "ALLOCATE về các ventures",
        ("chia tiền giao dịch đã khớp theo tỉ lệ venture của đúng loại · tháng",
         "phần lẻ làm tròn dồn vào một venture có tên, ⛔ mất xu"), "Σ phần chia = tiền giao dịch", doi_chieu="đề xuất"),
    Hop("nBB", "n4", cotn(4, 6), "d", "n", "biên bản PP (3)",
        ("đếm theo loại: khớp · chờ tiền · tiền chưa khớp", "+ lý do có tên"), "mỗi lượt", doi_chieu="đề xuất"),
    Hop("nRa", "n5", cotn(1, 3), "d", "n", "dòng phân bổ theo venture",
        ("venture · LE · loại · tháng · tiền · giao dịch gốc", "→ lớp sửa (chỉ-thêm) → sổ hiệu lực"), "giao dịch gốc ⛔ đổi một ô",
        doi_chieu="đề xuất"),
    Hop("nKiem", "n5", cotn(4, 5), "p", "n", "KIỂM Σ phân bổ",
        ("Σ phần chia = tiền giao dịch,", "từng giao dịch · từng tiền tệ"), "lệch ⇒ chặn cả lượt", doi_chieu="đề xuất"),
]
HOP_N_THEO = {h.ma: h for h in HOP_N}

TEN_N: list[Ten] = [
    Ten("n1", "nFile", "nTach", "n", "dòng chi phí có cột venture", "(loại, tháng, venture)", "n – 1",
        "venture rỗng ⇒ hàng chờ có tên", "⛔ đề xuất", tamn(1)),
    Ten("n2", "nFile", "nMap", "q", "chi phí theo loại · vendor · tháng", "(loại, vendor, tháng)", "n – 1 kỳ",
        "loại lạ ⇒ chặn, nêu tên loại", "⛔", tamn(2, 3)),
    Ten("n3", "nBank", "nMap", "b", "giao dịch chưa ghép: TK · ngày · tiền · nội dung", "content_key", "1 – 1",
        "đọc từ ảnh, ⛔ Sheets sống", "✅ hàng chờ có", tamn(4, 5)),
    Ten("n4", "nLuat", "nMap", "n", "luật của từng loại", "loại + version", "4 luật",
        "luật chưa ký ⇒ loại ấy ⛔ chạy", "⛔ chờ owner", tamn(6)),
    Ten("n5", "nTach", "nTyLe", "n", "tỉ lệ % theo venture", "(loại, tháng, venture)", "1 – n",
        "Σ % mỗi loại · tháng = 100, lệch ⇒ chặn", "⛔", tamn(1)),
    Ten("n6", "nMap", "nKhop", "n", "cặp (giao dịch, chi phí kỳ, loại)", "(content_key, loại, tháng)", "n – m",
        "Σ chi phí kỳ = Σ giao dịch của loại", "⛔", tamn(2, 3)),
    Ten("n7", "nMap", "nCho", "n", "chi phí kỳ không giao dịch nào khớp", "(loại, tháng)", "—",
        "chỉ so với ảnh sao kê của TK chi tới ảnh mới nhất", "⛔", tamn(4, 5)),
    Ten("n8", "nMap", "nCon", "n", "giao dịch không khớp loại nào", "content_key", "—",
        "vẫn UNMAPPED, ⛔ tự gán loại", "⛔", tamn(6)),
    Ten("n9", "nTyLe", "nAlloc", "n", "tỉ lệ venture của đúng loại · tháng", "(loại, tháng)", "1 – n",
        "thiếu tỉ lệ ⇒ ⛔ chia, vào hàng chờ", "⛔", tamn(1)),
    Ten("n10", "nKhop", "nAlloc", "n", "giao dịch đã khớp + loại + tháng", "content_key", "1 – n phần",
        "chỉ chia giao dịch đã khớp", "⛔", tamn(2, 3)),
    Ten("n11", "nCho", "nBB", "n", "số chi phí chờ tiền theo loại", "(loại, tháng)", "—", "in mẫu số", "⛔", tamn(4, 5)),
    Ten("n12", "nCon", "nBB", "n", "số giao dịch chưa khớp", "content_key", "—", "in mẫu số", "⛔", tamn(6)),
    Ten("n13", "nAlloc", "nRa", "n", "phần chia theo venture", "(content_key, venture)", "1 – n",
        "ghi chỉ-thêm, giao dịch gốc giữ nguyên", "⛔", tamn(2)),
    Ten("n14", "nRa", "nKiem", "n", "các phần chia của từng giao dịch", "content_key", "n – 1",
        "Σ phần = tiền giao dịch", "⛔", None),
]


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
MOT_HOP_OK = {"G0", "G1", "H0", "H1"}


def so_muc(d: str) -> int:
    """Số mục của một dải: hộp lẻ + mỗi khung chứa tính MỘT (luật vẽ voi: khung là một tầng)."""
    hs = [h for h in HOP if h.dai == d]
    return sum(1 for h in hs if not h.khoi) + len({h.khoi for h in hs if h.khoi})


def kiem() -> dict:
    loi: list[str] = []
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


# ───────────────────────────── vẽ SVG ─────────────────────────────
E = html.escape
LOAI_CHU = {"o": "khởi động", "x": "nguồn ngoài", "d": "dữ liệu", "p": "xử lý"}
TT_CHU = {"b": "có mã", "q": "GĐ1 phải dựng", "n": "đề xuất, chờ owner"}


def svg() -> str:
    o: list[str] = [f'<svg viewBox="0 0 {W} {H}" role="group" aria-label="Voi FLS-tobe-phase1: bấm một hộp hay mũi tên để xem chi tiết">',
                    '<defs>']
    for k in ("b", "q", "n"):
        o.append(f'<marker id="m{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                 f'orient="auto"><path d="M0 0L10 5L0 10z" class="mk-{k}"/></marker>')
    o.append('</defs>')
    o.append('<rect class="vz vz-ext" x="242" y="10" width="336" height="194" rx="6"/>')
    o.append('<text class="vt" x="250" y="28">FPS · sổ cái (ngoài FLS)</text>')
    o.append('<rect class="vz vz-pp1" x="743" y="10" width="334" height="194" rx="6"/>')
    o.append('<text class="vt vt-pp1" x="751" y="28">PHƯƠNG PHÁP (1) · MAPPING VỚI BANK TXN</text>')
    o.append('<rect class="vz vz-pp1" x="1080" y="10" width="164" height="194" rx="6"/>')
    o.append('<text class="vt vt-pp1" x="1086" y="28">PHƯƠNG PHÁP (2)</text>')
    o.append('<rect class="vz vz-pp1" x="1247" y="10" width="165" height="194" rx="6"/>')
    o.append('<text class="vt vt-pp1" x="1253" y="28">PHƯƠNG PHÁP (3)</text>')
    for v, (n1, n2, y0, y1) in VUNG.items():
        o.append(f'<rect class="vz vz-{v}" x="124" y="{y0}" width="1288" height="{y1 - y0}" rx="6"/>')
        o.append(f'<text class="vr" x="10" y="{y0 + 18}">{E(n1)}</text>')
        o.append(f'<text class="vr2" x="10" y="{y0 + 32}">{E(n2)}</text>')
    o.append('<text class="vr" x="10" y="28">NGUỒN</text><text class="vr2" x="10" y="42">ngoài FLS, chỉ-đọc</text>')
    for d, (_v, y0, h, nh) in DAI.items():
        if not nh or d in ("B0", "B1", "G0", "G1", "H0", "H1"):
            continue
        dy = 18 if d in ("A0", "A1") else 4
        o.append(f'<text class="br" x="10" y="{y0 + h / 2 + dy}">{E(nh)}</text>')
    o.append('<line class="ranh" x1="124" y1="261" x2="1412" y2="261"/>')
    o.append('<rect class="khung-pp1" x="576" y="281" width="501" height="216" rx="6"/>')
    o.append('<text class="vt vt-pp1" x="582" y="277">PP (1) · MAPPING VỚI BANK TXN</text>')
    o.append('<rect class="khung-pp1" x="1079" y="281" width="166" height="216" rx="6"/>')
    o.append('<text class="vt vt-pp1" x="1085" y="277">PP (2)</text>')
    o.append('<rect class="khung-pp1" x="1247" y="281" width="165" height="216" rx="6"/>')
    o.append('<text class="vt vt-pp1" x="1253" y="277">PP (3)</text>')
    for x0, x1, nh, lx in ((242, 1055, "PP (1)", 250), (1077, 1229, "PP (2)", 1083), (1244, 1412, "PP (3)", 1252)):
        o.append(f'<rect class="khung-pp1" x="{x0}" y="515" width="{x1 - x0}" height="210" rx="6"/>')
        o.append(f'<text class="vt vt-pp1" x="{lx}" y="511">{nh}</text>')
    for i, s in enumerate(("◀ FPS: đọc sổ cái", "chỉ-đọc · vai đọc riêng", "Sheets API · TK dịch vụ ▶",
                           "quyền chỉ-đọc")):
        o.append(f'<text class="rt" x="{tam(3)}" y="{213 + i * 12}" text-anchor="middle">{E(s)}</text>')
    o.append('<text class="rt" x="182" y="256" text-anchor="middle">ranh giới FLS</text>')
    ve_phan(o, HOP, TEN, HOP_THEO)
    o.append('</svg>')
    return "\n".join(o)


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
                 f'<rect class="khung" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
                 f'rx="{9 if h.loai == "o" else 3}"/>')
        nho = h.loai == "o"
        ty = y0 + (14 if nho else 16)
        o.append(f'<text class="{"to" if nho else "t1"}" x="{x0 + 8}" y="{ty}">{E(h.ten)}</text>')
        for i, d in enumerate(h.dong):
            cl = "t2n" if "đề xuất" in d else ("t2o" if nho else "t2")
            o.append(f'<text class="{cl}" x="{x0 + 8}" y="{ty + (13 if nho else 15) * (i + 1)}">{E(d)}</text>')
        if h.mono:
            o.append(f'<text class="t3" x="{x0 + 8}" y="{y1 - 8}">{E(h.mono)}</text>')
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
                  "dai": NHAN_DAI_BANG.get(h.dai) or DAI[h.dai][3], "vao": vao[h.ma], "ra": ra[h.ma]}
           for h in HOP}
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
                         "dai": dai[h.dai][3], "vao": vm[h.ma], "ra": rm[h.ma]}
    ten = {t.ma: {"tu": t.tu, "toi": t.toi, "tt": t.tt, "cai_gi": t.cai_gi, "khoa": t.khoa, "ban_so": t.ban_so,
                  "cong": t.cong, "co_ma": t.co_ma, "nhom": NHOM[t.nhom[0]] + " · " + NHOM[t.nhom]}
           for t in TEN}
    for tens, nv in ((TEN_M, "Mapping PP (1) · phóng to"), (TEN_N, "PP (3) nền tảng · phóng to")):
        for t in tens:
            ten[t.ma] = {"tu": t.tu, "toi": t.toi, "tt": t.tt, "cai_gi": t.cai_gi, "khoa": t.khoa, "ban_so": t.ban_so,
                         "cong": t.cong, "co_ma": t.co_ma, "nhom": nv}
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
  --sans:"IBM Plex Sans",system-ui,"Segoe UI",Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;
  --serif:"IBM Plex Serif",Georgia,serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#141815; --paper:#1c221f; --fg:#e5eae6; --muted:#a0aaa3; --line:#353d38;
  --accent:#8fb8e0; --accent-soft:#213041;
  --ok:#6fcf97; --ok-soft:#1d3729; --mid:#e2b45a; --mid-soft:#3a2f18; --no:#8d968f; --no-soft:#262b28;
  --prop:#86a8f0; --prop-soft:#1f2a44; --sel:#fb923c;
  --ext:#29251e; --zc:#1a222a; --zd:#1a271f; --ze:#251f29; --box:#222926; --orig:#2d281c; color-scheme:dark }}
:root[data-theme="dark"]{
  --bg:#141815; --paper:#1c221f; --fg:#e5eae6; --muted:#a0aaa3; --line:#353d38;
  --accent:#8fb8e0; --accent-soft:#213041;
  --ok:#6fcf97; --ok-soft:#1d3729; --mid:#e2b45a; --mid-soft:#3a2f18; --no:#8d968f; --no-soft:#262b28;
  --prop:#86a8f0; --prop-soft:#1f2a44; --sel:#fb923c;
  --ext:#29251e; --zc:#1a222a; --zd:#1a271f; --ze:#251f29; --box:#222926; --orig:#2d281c; color-scheme:dark }
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:15px/1.55 var(--sans);margin:0;
  padding-block:0 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:1440px;margin:0 auto}
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
.diagram svg{display:block;min-width:1200px;width:100%;height:auto;font-family:var(--sans)}
figcaption{font-size:13px;color:var(--muted);margin:8px 2px 0;max-width:none}
.vz{stroke:var(--line);stroke-width:1} .vz-ext{fill:var(--ext)} .vz-C{fill:var(--zc)} .vz-D{fill:var(--zd)} .vz-E{fill:var(--ze)}
.vt{font:600 11.5px var(--mono);fill:var(--muted);letter-spacing:.04em}
.vt-pp1{fill:var(--sel)} .vt2{font:10.5px var(--sans);fill:var(--muted)}
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
    quaMoiHinh(sv => sv.querySelectorAll('.hop,.ten-g').forEach(n => { if (n.dataset.tt === loc) ids.add(n.dataset.id); }));
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
    if (h.dong.length) s += '<p>' + h.dong.map(txt).join('<br>') + '</p>';
    s += '<dl>';
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
    n.classList.add('chon-dang');
    document.querySelectorAll('tr.chon[data-ref="' + id + '"]').forEach(r => r.classList.add('dang'));
    const [k, m] = id.split(':');
    const ids = new Set([id]);
    if (k === 'h') { const h = D.hop[m]; h.vao.concat(h.ra).forEach(t => { ids.add('t:' + t); ids.add('h:' + D.ten[t].tu); ids.add('h:' + D.ten[t].toi); }); }
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
    const g = e.target.closest('.hop,.ten-g');
    if (g) chon(g.dataset.id, false); else if (dang) dong();
  }));
  quaMoiHinh(svg => svg.addEventListener('keydown', e => {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('.hop,.ten-g')) { e.preventDefault(); chon(e.target.closest('.hop,.ten-g').dataset.id, false); }
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
  if (window.claude && window.claude.use) {
    window.claude.use('comments').then(c => { binh = c; if (dang) capNhatNut(); }).catch(() => { binh = null; });
  }
})();
"""

THAN_TREN = """
<header class="top">
  <h1>Voi FLS-tobe-phase1</h1>
  <p class="meta"><b>v0.3.2 · 2026-11-04</b> · Giai đoạn 1: đi hết INPUT, về <b>một</b> bảng ITL, mọi dòng có pháp nhân. Lệnh chi lấy từ <b>sổ cái PM / PC của FPS</b> qua hợp đồng dữ liệu (§5).
  Hình, bảng mũi tên, bảng kiểm cạnh và khung chi tiết <b>sinh từ cùng một bản khai</b> (<code>docs/ITL/_tools/sinh_voi_phase1.py</code>); máy kiểm hình trước khi ghi.<br>
  PD Now là bản gốc tham khảo: trang này chỉ mượn <b>thuật ngữ</b> (PE · PI · PM · PC · LE · CDT · HD/KRF · Reference No · General Trustest), không dùng tên sheet, tên file hay bước tính của nó. Mã FLS @ <code>2d1b710</code>.</p>
</header>
<p class="tin"><b>Cách dùng:</b> bấm một hộp hay một mũi tên (hoặc một dòng trong bảng) để làm nổi các đường nối của nó và mở khung chi tiết. Trong khung có <b>Bình luận phần này</b> và ô <b>Hỏi Claude</b>: câu hỏi được gắn đúng vào phần đang chọn, Claude trả lời trong luồng bình luận ở đó.</p>
"""


def trang() -> str:
    k = kiem()
    if k["loi"] or kiem_m():
        raise SystemExit("⛔ hình SAI:\n  " + "\n  ".join(k["loi"] + kiem_m()))
    cap = (f'Hình 1 — Voi FLS-tobe-phase1. Máy kiểm lúc sinh: <b>{len(TEN_VUNG)} vùng · {len(DAI)} dải · {k["hop"]} hộp · '
           f'{k["ten"]} mũi tên</b> ({k["doc"]} dọc · {k["ngang"]} ngang) · <b>0</b> mũi tên chéo · <b>0</b> mũi tên nhảy dải · '
           f'<b>{k["cheo"]}</b> chỗ hai mũi tên cắt nhau · <b>0</b> mũi tên cắt qua hộp. Mỗi dải 2–5 mục (một khung PP hay cột khởi động tính một mục; vùng nguồn PP (2), (3) có chủ ý một hộp mỗi dải), mỗi vùng 1–5 dải. '
           'Hai thứ cố ý <b>không vẽ thành mũi tên</b>: ① điểm khởi động (S1–S5) vẽ bằng <b>huy hiệu</b> trên hộp nó khởi, '
           'vì một nhịp kích hai phép chụp sẽ phải cắt các mũi tên đi vào; ② <i>GHI tay</i> đọc dòng sổ và ứng viên lệnh chi '
           'từ dải dưới (chiều đọc ngược). Một hộp <b>gộp vẽ</b>: '
           'lớp sửa (5 bảng luôn ghi trong cùng một giao dịch).')
    o = ['<title>Voi FLS-tobe-phase1</title>',
         '<meta name="claude:viewport-fit-sides" content="cover">',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;family=IBM+Plex+Serif:wght@600&amp;display=swap">',
         f'<style>{CSS}</style>', '<main>', THAN_TREN,
         '<h2>§1 · Con voi — vùng theo nơi chạy và phương pháp xử lý, dải theo đời sống của dữ liệu</h2>',
         '<div class="thanh" role="toolbar" aria-label="Lọc theo trạng thái"><span class="nhan">Làm nổi:</span>'
         '<button class="chip" data-loc="tat" aria-pressed="true" type="button">Tất cả</button>'
         '<button class="chip" data-loc="b" aria-pressed="false" type="button">Có mã</button>'
         '<button class="chip" data-loc="q" aria-pressed="false" type="button">GĐ1 phải dựng</button>'
         '<button class="chip" data-loc="n" aria-pressed="false" type="button">Đề xuất, chờ owner</button></div>',
         '<div class="legend">'
         '<span><i class="sw" style="background:var(--orig);border-color:var(--mid);border-radius:6px"></i>khởi động (người · nhịp)</span>'
         '<span><i class="sw" style="background:var(--ext)"></i>nguồn ngoài FLS</span>'
         '<span><i class="sw" style="border-color:var(--muted)"></i>dữ liệu (tên của vật)</span>'
         '<span><i class="sw" style="border-color:var(--accent)"></i>xử lý (ĐỘNG TỪ + danh từ)</span>'
         '<span><i class="ln"></i>có mã</span><span><i class="ln ln-q"></i>GĐ1 phải dựng (đã chốt)</span>'
         '<span><i class="ln ln-n"></i>đề xuất của trang này (chờ owner)</span>'
         '<span><span class="pill mid" style="font-size:10px">S1</span> huy hiệu = hộp này do điểm khởi động S1 chạy</span><span><i class="sw" style="border:1.4px dashed var(--sel)"></i>PP (n) = phương pháp xử lý n</span>'
         '</div>',
         f'<figure class="diagram" id="hinh">{svg()}<figcaption>{cap}</figcaption></figure>',
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
<tr class="chon" data-ref="h:mL1" tabindex="0"><td><b>L1 · khớp</b></td><td>giao dịch có Reference No trùng ≥ 1 dòng sổ cái PM; Σ tiền các PM line = tiền giao dịch; cùng tiền tệ; nhánh VN thêm pháp nhân trả = pháp nhân TK (QĐ-ITL-144). <b>Hoặc</b> (PP 2) giao dịch từ TK chi lương khớp Σ một đợt lương / BHXH / BHYT của một venture trong kỳ ⇒ LE venture</td><td>Reference No + tiền (+ pháp nhân)</td><td>2.263 mối nối</td><td>mối nối vào lớp sửa; gợi ý hd/cdt1 từ PM line</td><td>Σ lệch ⇒ chặn, ⛔ chia bừa</td></tr>
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
<p class="note"><b>Luật GĐ1 cho PP (2):</b> các đợt đi tiền lương / BHXH / BHYT của các venture — giao dịch bank từ TK chi lương, nội dung mang loại đợt, tổng khớp Σ đợt của một venture trong kỳ ⇒ <b>LE</b> của venture ấy. <b>GĐ2:</b> từ đợt đã gắn LE, tách xuống <b>KRF</b> theo sổ lương.<br>
<b>Luật mồi cho bảng luật</b> — năm loại giao dịch kế toán ghi là hay bị sót trên PM: lãi và phí ngân hàng · điều chuyển nội bộ, mua bán ngoại tệ · chi phí năm trước trả năm nay · quẹt thẻ chưa nhập PM · doanh thu, OMC, server chưa nhập. <b>Danh mục loại giao dịch</b> dùng lại cột "Loại giao dịch (Payment Type)" của sổ cái PM để L1 và L3 nói cùng một bộ từ.<br>
<b>Hai câu chờ owner:</b> ① vòng này cần đọc <b>nội dung giao dịch</b> trên sao kê, nhưng hôm nay FLS chỉ được đọc ba cột (ngày · Reference number · nguồn — QĐ-ITL-92) và <code>fls_itl.memo</code> rỗng 8.387/8.387 ⇒ có nới QĐ-ITL-92 cho cột nội dung, chỉ để suy diễn? ② chọn <b>k</b> (số xác nhận để thành luật ứng viên) và <b>N</b> (số ngày để L2 bị cờ).</p>
""", """
<h2>§1c · Phương pháp (3) — 4 chi phí nền tảng: OMC · GI · Server · PS</h2>
<p>Bốn loại chi phí này <b>không có trên FPS</b>, nên không có Reference No để ghép như PP (1). Đường đi: xuất file từ data Looker → mapping với bank txns, <b>mỗi loại một luật</b> → allocate về các ventures. Giao dịch ngân hàng đưa vào là những dòng còn ở lớp L3 của §1b.</p>
<figure class="diagram" id="hinh-n">""", svg_n(), """<figcaption>Hình 3 — PP (3) phóng to. 5 dải · 13 hộp · 14 mũi tên, máy kiểm như hình 1. Mọi hộp nét đứt xanh: đề xuất, chờ owner ký luật.</figcaption></figure>
<h3>Mỗi luật mapping phải khai năm điều</h3>
<p>Luật cụ thể của OMC, GI, Server, PS do owner điền; trang này chỉ khai <b>hình dạng</b> một luật phải có, để bốn luật so được với nhau.</p>
<div class="scroll"><table>
<thead><tr><th>điều phải khai</th><th>hình dạng</th><th>vì sao</th></tr></thead>
<tbody>
<tr><td>① nhận diện giao dịch</td><td>TK chi + vendor / từ khoá nội dung + chiều tiền ra</td><td>không có Reference No; thiếu nội dung thì cần nới QĐ-ITL-92 (câu ① §1b)</td></tr>
<tr><td>② khớp kỳ</td><td>tháng chi phí trên Looker ↔ tháng của giao dịch (trả trước / trả sau bao nhiêu tháng)</td><td>một giao dịch có thể trả chi phí của tháng trước</td></tr>
<tr><td>③ khớp tiền</td><td>Σ chi phí kỳ của loại = Σ giao dịch khớp; dung sai; cùng tiền tệ hay quy đổi</td><td>lệch thì chặn, không chia bừa (INV-I16)</td></tr>
<tr><td>④ tỉ lệ venture</td><td>cột nào của file Looker cho phần của từng venture; venture = LE hay CDT1 (câu 5 §7)</td><td>allocate cần Σ % = 100 cho từng loại · tháng</td></tr>
<tr><td>⑤ ai ký, từ khi nào</td><td>người ký + ngày hiệu lực + version</td><td>luật đổi thì lượt cũ giữ version đã dùng</td></tr>
</tbody></table></div>
""", """
<h2>§2 · Đã sửa gì</h2>
<p class="note"><b>v0.3 (owner, 04/11):</b> nguồn FPS là <b>sổ cái PM / PC</b>, đã mang đủ chiều ⇒ bỏ hai hộp "phiếu PE·PI·PM·PC" và "danh mục FPS"; bước dựng đổi từ <i>DỰNG chuỗi phiếu</i> (đi PM → PI → PE) thành <i>DỰNG dòng lệnh</i> (đọc thẳng từng dòng sổ cái). Đề xuất pháp nhân TK (k1) nay đếm từ TK chi + pháp nhân thanh toán trên sổ cái PM.</p>
<p class="note"><b>v0.3.1–v0.3.2 (owner, 04/11, bình luận trên hình):</b> tách riêng ba phương pháp xử lý nguồn Sheets. <b>(1) mapping với bank transaction</b> — sao kê &amp; sổ quỹ: kế toán dán / ghi → bản khai nguồn → ảnh chụp đọc theo bản khai → DỰNG dòng tiền; dòng tiền chưa mang chiều chi phí nên phải <b>mapping với bank txns theo reference number</b> (hộp MAPPING: mã Reference number trên giao dịch ngân hàng ↔ cùng mã trên dòng sổ cái PM, chia tiền theo PM line). PP (2), (3) cũng mapping với bank txns nhưng bằng luật riêng (§1b, §1c), không qua Reference No của PM. Sửa tay (GHI tay → lớp sửa) là bước chung cho mọi dòng sổ, không riêng phương pháp nào. <b>(2) lương · BHXH · BHYT</b> — sổ lương HR: HR lập → ảnh sổ lương → DỰNG đợt lương · BH. <b>GĐ1:</b> luật mapping các đợt đi tiền lương / BHXH / BHYT của các venture với bank txns → gắn <b>LE</b> (§1b). <b>GĐ2:</b> mapping xuống <b>KRF</b>. <b>(3) 4 chi phí nền tảng OMC · GI · Server · PS</b> — không có trên FPS: xuất file từ data Looker → mapping với bank txns, mỗi loại một luật → allocate về các ventures (§1c). Vùng nguồn Sheets tách làm ba; hộp "ảnh sổ nhập tay" tách làm ba; mỗi phương pháp là một khung đi từ nguồn xuống tới bước dựng.</p>
<p>Năm chỗ bản v0.1 vẽ sai, sửa từ v0.2:</p>
<ol class="fix">
<li><b>Bản khai nguồn đứng trước phép chụp.</b> Ảnh sao kê đọc vùng chuẩn <i>theo</i> bản khai và ghi lại <code>khai_version</code> (<code>fls/repo/chup.py:16</code>, <code>tools/chup_sao_ke.py</code>).</li>
<li><b>Pháp nhân của dòng tiền phải có lúc DỰNG.</b> <code>fls_itl</code> chỉ-thêm và pháp nhân là cột của dòng sổ ⇒ luật gắn pháp nhân nằm trong bản khai của nguồn (người khai, owner ký), đọc ở bước dựng.</li>
<li><b>Hai đường ghi tách bạch.</b> Máy ghi cả lượt nạp trong <i>một</i> giao dịch (<code>chay_nap.py:621</code>); người ghi qua <code>ghi_tay.py</code>, chỗ ghi duy nhất.</li>
<li><b>Năm điểm khởi động vẽ riêng.</b> Nhịp mỗi giờ chỉ <i>chụp</i>; khai nguồn, xem lô, Nhận lô, ghép/sửa là bốn cú bấm khác nhau của kế toán.</li>
<li><b>"Một bảng ITL duy nhất" là sổ hiệu lực</b> (sổ gốc + lớp sửa), không chỉ <code>fls_itl</code>.</li>
</ol>

<h2>§3 · Mũi tên nói gì — 43 mũi tên, 5 nhóm</h2>
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
<tr><td>2</td><td>x4 · b3 cho lằn Cash</td><td>Cùng bộ đọc với sao kê, chỉ bật lằn và khuôn quỹ</td><td>số dòng = sổ quỹ từng quỹ · nạp lại = 0 trùng · số dư theo ngày khớp</td></tr>
<tr class="b1"><th colspan="4">Chặng II · Mở họ lệnh chi và chi phí (bước 3–5)</th></tr>
<tr><td>3</td><td>x1 · x2 · b1 · g1 (sổ cái PM + PC)</td><td>Hợp đồng §5 chốt trước; đặt kiểu 13 cột PM còn thô; ảnh sổ cái dùng lại lằn ảnh chụp, không dựng hệ thứ hai</td><td>0 khoá lệnh chi trỏ rỗng · chiều lệnh chi khớp sổ đang chạy 100% từng ô</td></tr>
<tr><td>4</td><td>x5 · b4 · g4 (PP 2 · lương / BHXH / BHYT)</td><td>GĐ1 chỉ cần đợt đi tiền của từng venture để gắn LE cho giao dịch bank; KRF để GĐ2; không mở hộp đen lương</td><td>mọi giao dịch bank loại lương / BH có LE (hoặc hàng chờ có tên) · Σ đợt mỗi venture mỗi kỳ = Σ giao dịch đã ghép</td></tr>
<tr><td>5</td><td>x6 · b5 · g5 (PP 3 · OMC · GI · Server · PS)</td><td>Không có trên FPS ⇒ 4 luật mapping riêng; Looker → mapping bank txns → allocate về ventures (§1c)</td><td>số dòng = file Looker · mọi giao dịch 4 loại khớp hoặc vào hàng chờ có tên · Σ phần chia = tiền giao dịch</td></tr>
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
<tr><td>3</td><td>FPS cấp sổ cái PM / PC qua <b>kết nối CSDL chỉ-đọc</b> hay <b>xuất bảng định kỳ</b>? Và ba cột ở cuối §5 có trong sổ cái không?</td><td>Quyết định tuyến của x1/x2 và việc chiều lệnh chi có đủ không; hôm nay sổ PM đi qua Sheets</td><td>bước 3</td></tr>
<tr><td>4</td><td>HR và nền tảng: FLS đọc sổ ở Sheets như hôm nay, hay chờ hệ nguồn có hợp đồng?</td><td>Quyết định tuyến của x5/x6</td><td>bước 4–5</td></tr>
<tr><td>5</td><td>PP (3): "venture" khi allocate là <b>LE</b> hay <b>CDT1</b>? Tỉ lệ chia lấy từ cột nào của file Looker? AP/AR lùi khỏi GĐ1?</td><td>Owner 04/11 chốt OMC · GI · Server · PS là chi phí, mapping với bank txns rồi allocate về ventures — thay câu cũ "GI/OMC không vào sổ"</td><td>bước 5</td></tr>
</tbody></table></div>

<footer>Voi FLS-tobe-phase1 v0.3.2 · 2026-11-04 · sinh bởi <code>docs/ITL/_tools/sinh_voi_phase1.py</code> · cùng bộ với <code>_PD_NOW_VOI_VA_GIAI_DOAN.md</code>.</footer>
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
    if k["loi"] or km:
        print("⛔ LỖI:\n  " + "\n  ".join(k["loi"] + km))
        return 1
    if "--kiem" in sys.argv:
        print("✅ hình đúng luật — ⛔ không ghi (--kiem)")
        return 0
    DICH.write_text(trang(), encoding="utf-8")
    print(f"✅ đã ghi {DICH.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
