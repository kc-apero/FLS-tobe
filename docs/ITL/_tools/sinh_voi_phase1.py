# -*- coding: utf-8 -*-
"""Sinh `docs/ITL/02_BA/Artifacts/Voi-FLS-tobe-phase1.html` từ MỘT bản khai hộp + mũi tên.

    python docs/ITL/_tools/sinh_voi_phase1.py          # sinh + kiểm, in số đếm
    python docs/ITL/_tools/sinh_voi_phase1.py --kiem   # chỉ kiểm, ⛔ không ghi

⭐ Vì sao sơ đồ được SINH, ⛔ không vẽ tay (luật `apr-vevoi`, mục *diagram truth gate*):
  ⓐ mọi mũi tên phải THẲNG, chỉ nối hai dải KỀ NHAU (hoặc hai hộp cùng dải),
  ⓑ ⛔ không mũi tên nào cắt qua một hộp, ⛔ không hai mũi tên nào cắt nhau,
  ⓒ ≤ 5 hộp mỗi dải, ≤ 5 dải mỗi vùng,
  ⓓ bảng "mũi tên nói gì" và bảng kiểm cạnh lấy từ CÙNG bản khai với hình
     ⇒ hình và bảng ⛔ không thể lệch nhau.
  Vẽ tay thì cả bốn điều trên chỉ là lời hứa; ở đây máy NỔ nếu sai một điều.

⛔ PD Now là bản THAM KHẢO: chỉ mượn THUẬT NGỮ (PE · PI · PM · PC · LE · CDT ·
   HD/KRF · Reference No · General Trustest), ⛔ không mượn tên sheet / file / bước.
"""
from __future__ import annotations

import html
import sys
from dataclasses import dataclass, field
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
DICH = GOC / "docs/ITL/02_BA/Artifacts/Voi-FLS-tobe-phase1.html"

# ───────────────────────────── lưới ─────────────────────────────
W, H = 1420, 1092
C0 = (128, 236)                         # cột 0: điểm khởi động của vùng FLS


def cot(i: int) -> tuple[int, int]:
    x = 248 + (i - 1) * 167
    return x, x + 157


def nhip(a: int, b: int, trai: int = 0, phai: int = 0) -> tuple[int, int]:
    return cot(a)[0] + trai, cot(b)[1] - phai


def tam(i: int) -> float:
    a, b = cot(i)
    return (a + b) / 2


# dải: (mã, vùng, y, cao, nhãn rail)
DAI = {
    "A0": ("A", 40, 46, "ai sinh ra"),
    "A1": ("A", 118, 74, "phiếu · sổ nguồn"),
    "B0": ("B", 40, 46, ""),
    "B1": ("B", 118, 74, ""),
    "c1": ("C", 290, 84, "① KHAI & CHỤP"),
    "c2": ("C", 410, 78, "② DỰNG"),
    "c3": ("C", 524, 78, "③ GHÉP & SOÁT"),
    "c4": ("C", 638, 78, "④ GHI"),
    "d1": ("D", 764, 78, "⑤ SỔ GỐC"),
    "d2": ("D", 878, 72, "⑥ HIỆU LỰC"),
    "e1": ("E", 998, 70, "⑦ NGƯỜI THẤY"),
}
VUNG = {   # mã: (nhãn, y0, y1)
    "C": ("FLS · NẠP", "chưa vào sổ", 266, 728),
    "D": ("FLS · SỔ", "PostgreSQL · chỉ-thêm", 740, 962),
    "E": ("ĐẦU RA", "màn FLS + hệ khác", 974, 1080),
}


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

    @property
    def y(self) -> tuple[float, float]:
        _v, y0, h, _n = DAI[self.dai]
        if self.tang == "tren":
            return y0, y0 + h / 2 - 4
        if self.tang == "duoi":
            return y0 + h / 2 + 4, y0 + h
        return y0, y0 + h


HOP: list[Hop] = [
    # ── ngoài FLS · FPS ──
    Hop("oLap", "A0", cot(1), "o", "b", "NGƯỜI LẬP & DUYỆT", ("phiếu trong FPS",),
        doi_chieu="ngoài FLS — FLS chỉ đọc trạng thái cuối"),
    Hop("oDm", "A0", cot(2), "o", "b", "NGƯỜI GIỮ DANH MỤC", ("danh mục trong FPS",),
        doi_chieu="ngoài FLS"),
    Hop("fpsPhieu", "A1", cot(1), "x", "b", "phiếu đã duyệt",
        ("PE · PI · PM · PC", "mỗi loại: slip + line"), "fps_*_slip · _line",
        doi_chieu="10 bảng slip/line có trong code FPS (FLS-vs-FPS-Compare-Audit §4)"),
    Hop("fpsDm", "A1", cot(2), "x", "b", "danh mục FPS",
        ("LE · CDT · HD/KRF", "đối tác · TK · tỷ giá"), "fps_le · fps_ven …",
        doi_chieu="fps_le · fps_cdt · fps_kr · fps_bgc · fps_ven · fps_bank_account · fps_exchange_rate (Audit §4)"),
    # ── ngoài FLS · Google Sheets ──
    Hop("oKT", "B0", nhip(4, 5), "o", "b", "KẾ TOÁN", ("dán sao kê vào sheet R | · ghi sổ quỹ",),
        doi_chieu="ngoài FLS — 68 dòng chảy có bản khai dòng 1"),
    Hop("oHR", "B0", cot(6), "o", "b", "HR · C&B", ("lập sổ lương",), doi_chieu="ngoài FLS"),
    Hop("oNT", "B0", cot(7), "o", "b", "CHỦ SỔ NỀN TẢNG", ("dịch vụ · thanh toán",), doi_chieu="ngoài FLS"),
    Hop("saoke", "B1", cot(4), "x", "b", "sao kê ngân hàng", ("60 dòng chảy", "19 bố cục cột"), "sheet R |",
        doi_chieu="tools/nap_nguon_va_khai.py (60 ngân hàng + 8 quỹ = 68 nguồn)"),
    Hop("soquy", "B1", cot(5), "x", "b", "sổ quỹ", ("8 dòng chảy", "kế toán ghi tay"), "sheet R |",
        doi_chieu="như trên"),
    Hop("soluong", "B1", cot(6), "x", "b", "sổ lương HR", ("4 sổ: 2 loại × 2 năm", "HD/KRF tách sẵn"), "sheet HR",
        doi_chieu="0 tham chiếu trong fls/ (chỉ chuỗi phương pháp ở mapping_master.py:31)"),
    Hop("sont", "B1", cot(7), "x", "b", "sổ nền tảng", ("chi phí dịch vụ (SC)", "thanh toán (PS)"), "file RAW",
        doi_chieu="0 tham chiếu trong fls/ (Platform chỉ là enum)"),
    # ── c1 · KHAI & CHỤP ──
    Hop("S1", "c1", C0, "o", "b", "S1 · NHỊP", ("mỗi giờ 8h–19h",), tang="tren",
        doi_chieu="fls/repo/nhip_chup.py (QĐ-ITL-114) · tools/nhip_chup.py chụp Bank + PM"),
    Hop("S2", "c1", C0, "o", "b", "S2 · KHAI", ("kế toán · F04",), tang="duoi",
        doi_chieu="POST khai-cot · thu-tu (fls/api)"),
    Hop("anhFPS", "c1", (cot(1)[0], cot(2)[1] - 16), "d", "q", "ảnh FPS",
        ("phiếu 4 loại + danh mục, đóng băng", "hôm nay: chỉ PM, đọc qua Sheets"), "fls_pm_line 3.772 · thiếu PE/PI/PC",
        huy=("S1",), doi_chieu="fls_pm_line (migration 0011/0023); PE/PI/PC/danh mục: chưa có bảng"),
    Hop("khai", "c1", (cot(3)[0] + 12, cot(3)[1] - 12), "d", "b", "bản khai nguồn",
        ("cột · thứ tự ngày", "+ pháp nhân: đề xuất"), "fls_khai_cot 408", huy=("S2",),
        doi_chieu="fls/repo/khai_cot.py (chỉ-thêm, có version); cột pháp nhân: chưa có"),
    Hop("anhSo", "c1", (cot(4)[0] + 16, cot(7)[1]), "d", "b", "ảnh sổ nhập tay",
        ("lằn Bank ✅ 60 nguồn · 182 ảnh  ·  Cash ⛔  ·  HR ⛔  ·  Platform ⛔",
         "đọc vùng chuẩn THEO bản khai, ghi khai_version · không đọc Diễn giải"),
        "fls_chup · fls_chup_nguon · fls_chup_dong", huy=("S1",),
        doi_chieu="tools/chup_sao_ke.py (LAN='Bank') · fls/repo/chup.py:16 khai_version"),
    # ── c2 · DỰNG ──
    Hop("S3", "c2", C0, "o", "b", "S3 · XEM LÔ", ("kế toán chọn lô", "màn F04"),
        doi_chieu="POST /nap/lo/xem-truoc"),
    Hop("dChuoi", "c2", nhip(1, 2), "p", "q", "DỰNG chuỗi phiếu",
        ("PM line → PI line → PE line → PE slip", "ra: HD/KRF · CDT1 · đối tác · kỳ DV · LE trả"),
        "khoá: pm_line_id · pi_line_id · pe_line_id", huy=("S3", "S4"),
        doi_chieu="chưa có: fls_pm_line.pe_line/pi_line trỏ vào bảng không tồn tại (QĐ-ITL-140)"),
    Hop("dTien", "c2", nhip(3, 5), "p", "b", "DỰNG dòng tiền",
        ("ảnh lằn Bank · Cash → canon 36 trường (General Trustest + TK)",
         "gắn pháp nhân TK từ bản khai của nguồn · content_key chống trùng"),
        "bank 8.338/8.338 · quỹ chưa chạy · pháp nhân: chưa", huy=("S3", "S4"),
        doi_chieu="fls/adapters/sao_ke.py + sao_ke_canon.py"),
    Hop("dChiPhi", "c2", nhip(6, 7), "p", "q", "DỰNG dòng chi phí",
        ("ảnh lằn HR · Platform → canon", "giữ HD/KRF + pháp nhân của sổ"), "không phân bổ lại",
        huy=("S3", "S4"), doi_chieu="chưa có (adapter D/E)"),
    # ── c3 · GHÉP & SOÁT ──
    Hop("ghep", "c3", nhip(1, 3), "p", "b", "GHÉP lệnh chi với dòng tiền",
        ("Reference No (ở PM slip) → chia tiền theo PM line",
         "Σ line = tiền dòng, lệch ⇒ chặn · khác tiền tệ ⇒ để người"),
        "có: ghép theo dòng 26,79% · thiếu: chuỗi PI/PE", huy=("S4",),
        doi_chieu="fls/adapters/pm_join.py · chay_nap.py:637 chen_moi_noi"),
    Hop("soat", "c3", nhip(4, 7), "p", "b", "SOÁT lô",
        ("9 luật · CHẶN ⇒ nguồn bị chừa · CỜ ⇒ vẫn ghi, vào hàng chờ có lý do",
         "4 vế phải cân: vào = sổ + loại + rỗng + trùng"),
        "fls/kiem/soat_nap.py", huy=("S3", "S4"),
        doi_chieu="fls/kiem/soat_nap.py · chay_nap.py:611 cổng bốn đường"),
    # ── c4 · GHI ──
    Hop("S4", "c4", C0, "o", "b", "S4 · NHẬN", ("kế toán · F04",), tang="tren",
        doi_chieu="POST /nap/lo"),
    Hop("S5", "c4", C0, "o", "b", "S5 · GHÉP·SỬA", ("kế toán · F01·F02",), tang="duoi",
        doi_chieu="POST match · adjust · reverse · …"),
    Hop("ghiNap", "c4", nhip(1, 4), "p", "b", "GHI lượt nạp — một giao dịch",
        ("run · dòng sổ · dòng loại · mối nối máy · gợi ý hd/cdt1",
         "lỗi giữa chừng ⇒ ⛔ không còn dòng nào đã ghi"),
        "fls/repo/chay_nap.py", huy=("S4",),
        doi_chieu="chay_nap.py:621 `with conn.transaction()`"),
    Hop("bienban", "c4", cot(5), "d", "b", "biên bản lô", ("9 dòng tổng", "n vào · m bị chừa"), "hiện trên F04",
        huy=("S3",), doi_chieu="QĐ-ITL-112 · man_f04.js"),
    Hop("ghiTay", "c4", nhip(6, 7), "p", "b", "GHI tay — một giao dịch",
        ("ghép · bỏ ghép · sửa · đảo · lý do", "actor lấy từ thẻ đăng nhập"),
        "fls/repo/ghi_tay.py — chỗ ghi duy nhất", huy=("S5",),
        doi_chieu="fls/repo/ghi_tay.py"),
    # ── d1 · SỔ GỐC ──
    Hop("loai", "d1", cot(1), "d", "b", "dòng bị loại", ("mỗi dòng một", "lý do có tên"), "fls_reject",
        doi_chieu="schema.py fls_reject"),
    Hop("soITL", "d1", nhip(2, 3), "d", "b", "SỔ ITL",
        ("một bảng · 4 họ nguồn (Bank·Cash·HR·Platform)", "chỉ-thêm · ⛔ không PUT/DELETE"),
        "fls_itl 8.387 · hôm nay 1 họ nguồn",
        doi_chieu="schema.py fls_itl · INV-I08 · source_system khai 4 giá trị"),
    Hop("lopSua", "d1", nhip(4, 7), "d", "b", "lớp sửa chỉ-thêm (gộp vẽ)",
        ("mối nối · bỏ nối · bút toán (người / máy gợi ý) · sự kiện hàng chờ · nhật ký",
         "sửa = thêm dòng · dòng sổ ⛔ không đổi một ô"),
        "fls_pm_link 2.263 · fls_adjustment 4.428 · fls_journal",
        doi_chieu="fls_pm_link · fls_pm_unlink · fls_adjustment · fls_queue_event · fls_journal"),
    # ── d2 · HIỆU LỰC ──
    Hop("kiem", "d2", (cot(1)[0], cot(1)[1] - 16), "p", "q", "KIỂM cổng GĐ1",
        ("mỗi cổng khai mong",), "đỏ khi khác",
        doi_chieu="/gates có 8 cổng · cổng GĐ1 (§3 nhóm 5): chưa"),
    Hop("hieuLuc", "d2", (cot(2)[0] + 16, cot(7)[1]), "d", "q", "SỔ ITL HIỆU LỰC — bảng ITL duy nhất của GĐ1",
        ("dòng sổ + giá trị đang hiệu lực (người › máy gợi ý › nguồn) + chuỗi phiếu + 3 vai pháp nhân",),
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
    Ten("o1", "oLap", "fpsPhieu", "b", "phiếu đi luồng lập → duyệt của FPS", "pe/pi/pm/pc_id", "1 phiếu – n dòng",
        "FLS ⛔ không can thiệp; chỉ đọc trạng thái cuối", "ngoài FLS", tam(1), "1a"),
    Ten("o2", "oDm", "fpsDm", "b", "mã + tên + hiệu lực của danh mục", "mã", "1 mã – 1 bản ghi hiệu lực",
        "mã trùng là lỗi của FPS, FLS báo chứ ⛔ không sửa", "ngoài FLS", tam(2), "1a"),
    Ten("o3", "oKT", "saoke", "b", "dán sao kê vào vùng chuẩn của sheet R |", "(dòng chảy, dòng)", "1 dòng chảy – n dòng",
        "bố cục cột theo bản khai dòng 1 (68/68 sheet khai đủ)", "ngoài FLS", tam(4), "1b"),
    Ten("o4", "oKT", "soquy", "b", "ghi thu chi quỹ", "(dòng chảy quỹ, dòng)", "1 quỹ – n dòng",
        "như o3", "ngoài FLS", tam(5), "1b"),
    Ten("o5", "oHR", "soluong", "b", "lập sổ lương đã tách HD/KRF", "(sổ, năm, dòng)", "1 sổ – n dòng",
        "bề rộng cột đổi ⇒ bộ đọc nổ, ⛔ không đoán", "ngoài FLS", tam(6), "1b"),
    Ten("o6", "oNT", "sont", "b", "ghi chi phí dịch vụ · thanh toán", "(sổ, tháng, dòng)", "1 sổ – n dòng",
        "như o5", "ngoài FLS", tam(7), "1b"),
    # 2 · vượt ranh giới
    Ten("x1", "fpsPhieu", "anhFPS", "q", "slip + line 4 loại phiếu · trạng thái · Reference No · payer_id",
        "line_id", "1 lần chụp – n dòng",
        "chụp 2 lần ⇒ 2 chup_id, ảnh cũ ⛔ không đổi một ô · cột riêng tư ⛔ không vào kho",
        "◐ PM có, đọc qua Sheets; PE/PI/PC ⛔", tam(1), "2a"),
    Ten("x2", "fpsDm", "anhFPS", "q", "danh mục đang hiệu lực (LE · CDT · HD/KRF · ngân sách · đối tác · TK · tỷ giá)",
        "mã + ngày hiệu lực", "1 lần chụp – n mã",
        "mã trùng ⇒ chặn · tên rỗng ⇒ cờ (hôm nay 24/29 LE thiếu tên)", "⛔ chỉ fls_le suy từ giá trị", tam(2), "2a"),
    Ten("x3", "saoke", "anhSo", "b", "vùng chuẩn, 5/6 trường (⛔ không Diễn giải)", "(nguồn, dòng) + khai_version",
        "1 nguồn – n dòng", "thiếu bản khai ⇒ nổ, nêu tên sheet · 429 ⇒ lùi rồi thử lại · nguồn 0 dòng vẫn có mặt",
        "✅ 60 nguồn · 182 ảnh", tam(4), "2b"),
    Ten("x4", "soquy", "anhSo", "q", "vùng chuẩn sổ quỹ", "(nguồn, dòng)", "1 quỹ – n dòng",
        "như x3 + số dư theo ngày nếu nguồn có", "⛔ lằn Cash chưa bật (GAP-CANON-02)", tam(5), "2b"),
    Ten("x5", "soluong", "anhSo", "q", "4 sổ lương theo năm", "(sổ, năm, dòng)", "1 sổ – n dòng",
        "Σ Nợ/Có từng sổ phải bằng sổ nguồn", "⛔", tam(6), "2b"),
    Ten("x6", "sont", "anhSo", "q", "sổ chi phí dịch vụ · sổ thanh toán", "(sổ, tháng, dòng)", "1 sổ – n dòng",
        "như x5", "⛔", tam(7), "2b"),
    # 3 · khai & dựng
    Ten("k1", "anhFPS", "khai", "n", "đề xuất pháp nhân TK: TK ngân hàng → LE chủ TK (danh mục FPS)",
        "bank_account_id ↔ nguồn", "1 nguồn – 1 LE",
        "máy đề xuất, người khai, owner ký · ⛔ không regex (14 TK · 211 dòng tên TK không nói LE)", "⛔ đề xuất mới",
        None, "3a"),
    Ten("k2", "khai", "anhSo", "b", "bố cục cột + thứ tự ngày của từng nguồn", "source_id + khai_version",
        "1 nguồn – 1 bản khai hiệu lực", "thiếu khai ⇒ nổ · khai sửa = version mới, bản cũ ⛔ không đổi",
        "✅ 408 dòng = 68 × 6", None, "3a"),
    Ten("b2", "khai", "dTien", "n", "pháp nhân TK của nguồn", "source_id", "1 nguồn – n dòng tiền",
        "nguồn chưa khai pháp nhân ⇒ dòng vào hàng chờ 'thiếu pháp nhân', ⛔ không đoán",
        "⛔ đề xuất mới", tam(3) + 0, "3a"),
    Ten("b1", "anhFPS", "dChuoi", "q", "slip + line 4 loại phiếu + danh mục", "line_id", "n – 1 mỗi bậc chuỗi",
        "khoá trỏ rỗng ⇒ cờ 'chuỗi đứt', dòng vẫn vào kèm lý do", "⛔", 410.0, "3b"),
    Ten("b3", "anhSo", "dTien", "b", "dòng lằn Bank · Cash", "chup_id + dòng", "1 – 1",
        "đọc từ ẢNH, ⛔ không đọc Sheets sống", "✅ Bank · ⛔ Cash", 911.0, "3b"),
    Ten("b4", "anhSo", "dChiPhi", "q", "dòng lằn HR · Platform", "chup_id + dòng", "1 – 1",
        "dòng thiếu HD ⇒ hàng chờ (mong 0)", "⛔", 1245.0, "3b"),
    # 4 · ghép, soát, ghi
    Ten("g1", "dChuoi", "ghep", "q", "mỗi PM line: tiền · tiền tệ · Reference No · chiều phiếu", "pm_line_id", "1 – 1",
        "N line một phiếu nói N giá trị ⇒ 'không suy được', ⛔ không lấy dòng đầu (INV-I16)",
        "◐ chỉ phần PM", 410.0, "4a"),
    Ten("g2", "dTien", "ghep", "b", "dòng tiền canon + Reference No", "content_key", "1 dòng tiền – n PM line",
        "Σ tiền các line = tiền dòng · khác tiền tệ ⇒ để người (chờ tỷ giá, GĐ2)", "✅", tam(3), "4a"),
    Ten("g3", "dTien", "soat", "b", "dòng tiền canon", "content_key", "1 – 1",
        "9 luật soát chạy theo TỪNG nguồn (⛔ nối phẳng 60 nguồn)", "✅", 911.0, "4a"),
    Ten("g4", "dChiPhi", "soat", "q", "dòng chi phí canon", "content_key", "1 – 1",
        "cùng 9 luật + Σ từng sổ = nguồn", "⛔", 1245.0, "4a"),
    Ten("w1", "ghep", "ghiNap", "b", "mối nối dự kiến (dòng, PM line, tiền chia, hình nối)", "(content_key, pm_line_id)",
        "1 – n", "chèn SAU dòng sổ (cần itl_id) nhưng TRONG cùng giao dịch", "✅", 410.0, "4b"),
    Ten("w2", "soat", "ghiNap", "b", "dòng đạt + dòng loại + cờ", "content_key", "1 – 1",
        "CHẶN ⇒ 0 dòng của nguồn ấy · 4 vế không cân ⇒ ⛔ không ghi gì", "✅", 827.0, "4b"),
    Ten("w3", "soat", "bienban", "b", "9 dòng tổng · nguồn bị chừa có tên luật", "luật", "9 dòng / lô",
        "đã đo = 0 hiện 'chưa đo', ⛔ không hiện số 0", "✅", tam(5), "4b"),
    Ten("s1", "ghiNap", "loai", "b", "dòng bị loại + lý do", "run_id + dòng nguồn", "1 – 1",
        "mỗi dòng loại có lý do có tên", "✅", tam(1), "4c"),
    Ten("s2", "ghiNap", "soITL", "b", "dòng sổ: General Trustest + TK + pháp nhân + run_id", "content_key UNIQUE", "1 – 1",
        "trùng ⇒ ⛔ không ghi, đếm vế 'trùng' · nạp lại cùng ảnh ⇒ vào sổ = 0", "✅ (pháp nhân còn rỗng)", 577.0, "4c"),
    Ten("s3", "ghiNap", "lopSua", "b", "mối nối máy + gợi ý hd/cdt1 (nguồn = máy gợi ý)", "itl_id + pm_line_id", "1 – n",
        "máy gợi ý ⛔ không đè lên ô người đã chốt", "✅", 827.0, "4c"),
    Ten("s4", "ghiTay", "lopSua", "b", "ghép · bỏ ghép · sửa · đảo · lý do · xong/mở lại", "itl_id", "1 – n",
        "bút toán + nhật ký trong MỘT giao dịch · actor từ thẻ, gửi trong thân ⇒ 400", "✅", 1245.0, "4c"),
    # 5 · hiệu lực & ra ngoài
    Ten("h1", "loai", "kiem", "q", "số dòng loại theo lý do", "run_id", "—",
        "vế 'loại' của 4 vế", "◐ cổng 4 vế có ở lúc nạp", tam(1), "5a"),
    Ten("h2", "soITL", "hieuLuc", "b", "dòng sổ gốc", "itl_id", "1 – 1",
        "sổ gốc ⛔ không đổi; giá trị hiệu lực đọc qua view", "✅", 577.0, "5a"),
    Ten("h3", "lopSua", "hieuLuc", "b", "giá trị người / máy gợi ý · mối nối · trạng thái hàng chờ", "itl_id",
        "n – 1", "người › máy gợi ý › nguồn; bỏ nối ⇒ giá trị máy rút theo", "✅", 1078.0, "5a"),
    Ten("h4", "hieuLuc", "kiem", "q", "sổ hiệu lực cho 5 cổng GĐ1", "le · source_system · curr", "—",
        "le NULL = 0 · Σ theo LE = Σ theo nguồn · 0 khoá phiếu trỏ rỗng", "⛔", None, "5a"),
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
    "1": "Nhóm 1 · Nguồn sinh ra (o1–o6)", "1a": "FPS (o1–o2)", "1b": "Google Sheets (o3–o6)",
    "2": "Nhóm 2 · Vượt ranh giới vào FLS (x1–x6)", "2a": "FPS → FLS · kết nối CSDL chỉ-đọc · vai đọc riêng (x1–x2)",
    "2b": "Sheets → FLS · Sheets API · tài khoản dịch vụ, quyền chỉ-đọc (x3–x6)",
    "3": "Nhóm 3 · Khai và dựng (k1–k2 · b1–b4)", "3a": "Bản khai nguồn và pháp nhân TK (k1 · k2 · b2)",
    "3b": "Đọc ảnh thành dòng canon (b1 · b3 · b4)",
    "4": "Nhóm 4 · Ghép, soát, ghi (g1–g4 · w1–w3 · s1–s4)", "4a": "Vào ghép và soát (g1–g4)",
    "4b": "Ra ghi và biên bản (w1–w3)", "4c": "Vào sổ (s1–s4)",
    "5": "Nhóm 5 · Hiệu lực và ra ngoài (h1–h4 · v1–v4)", "5a": "Sổ hiệu lực và cổng (h1–h4)",
    "5b": "Người thấy và hệ khác (v1–v4)",
}


# ───────────────────────────── kiểm hình ─────────────────────────────
def doan(t: Ten) -> tuple[float, float, float, float]:
    a, b = HOP_THEO[t.tu], HOP_THEO[t.toi]
    if t.x is not None:                                    # dọc, a ở trên b
        return t.x, a.y[1], t.x, b.y[0]
    ya = (max(a.y[0], b.y[0]) + min(a.y[1], b.y[1])) / 2   # ngang, cùng dải
    if a.x[1] <= b.x[0]:
        return a.x[1], ya, b.x[0], ya
    return a.x[0], ya, b.x[1], ya


def cat_hop(x1, y1, x2, y2, h: Hop) -> bool:
    lx, rx = sorted((x1, x2))
    ty, by = sorted((y1, y2))
    return not (rx <= h.x[0] or lx >= h.x[1] or by <= h.y[0] or ty >= h.y[1])


def kiem() -> dict:
    loi: list[str] = []
    tang = {"A0": 0, "B0": 0, "A1": 1, "B1": 1, "c1": 2, "c2": 3, "c3": 4, "c4": 5, "d1": 6, "d2": 7, "e1": 8}
    for d in DAI:
        n = sum(1 for h in HOP if h.dai == d)
        if not 2 <= n <= 5:
            loi.append(f"dải {d}: {n} hộp (phải 2–5)")
    for v in VUNG:
        n = sum(1 for d in DAI.values() if d[0] == v)
        if n > 5:
            loi.append(f"vùng {v}: {n} dải")
    for t in TEN:
        a, b = HOP_THEO[t.tu], HOP_THEO[t.toi]
        x1, y1, x2, y2 = doan(t)
        if t.x is not None:
            if not (a.x[0] + 6 <= t.x <= a.x[1] - 6 and b.x[0] + 6 <= t.x <= b.x[1] - 6):
                loi.append(f"{t.ma}: x={t.x} ngoài hộp {a.ma}/{b.ma}")
            if tang[b.dai] - tang[a.dai] != 1:
                loi.append(f"{t.ma}: {a.dai}→{b.dai} ⛔ không kề nhau")
            if y2 <= y1:
                loi.append(f"{t.ma}: đi ngược")
        else:
            if a.dai != b.dai:
                loi.append(f"{t.ma}: ngang mà khác dải")
        for h in HOP:
            if h.ma in (t.tu, t.toi):
                continue
            if cat_hop(x1 + (0.5 if t.x is None else 0), y1, x2, y2, h) and \
                    cat_hop(x1, y1 + 0.5, x2, y2 - 0.5, h):
                loi.append(f"{t.ma} cắt qua hộp {h.ma}")
    cheo = 0
    for i, t in enumerate(TEN):
        for u in TEN[i + 1:]:
            p, q = doan(t), doan(u)
            if (t.x is None) == (u.x is None):
                continue
            dd, nn = (p, q) if t.x is not None else (q, p)
            x, ya, _, yb = dd
            xa, y, xb, _ = nn
            if min(xa, xb) < x < max(xa, xb) and min(ya, yb) < y < max(ya, yb):
                cheo += 1
                loi.append(f"{t.ma} × {u.ma} cắt nhau")
    ma = [t.ma for t in TEN]
    if len(set(ma)) != len(ma):
        loi.append("mã mũi tên trùng")
    return {"hop": len(HOP), "ten": len(TEN), "doc": sum(t.x is not None for t in TEN),
            "ngang": sum(t.x is None for t in TEN), "cheo": cheo, "loi": loi}


# ───────────────────────────── vẽ SVG ─────────────────────────────
E = html.escape


def svg() -> str:
    o: list[str] = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Voi FLS-tobe-phase1">',
                    '<defs>']
    for k in ("b", "q", "n"):
        o.append(f'<marker id="m{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                 f'orient="auto"><path d="M0 0L10 5L0 10z" class="mk-{k}"/></marker>')
    o.append('</defs>')
    # vùng ngoài
    o.append('<rect class="vz vz-ext" x="242" y="10" width="336" height="194" rx="6"/>')
    o.append('<text class="vt" x="250" y="28">FPS · hệ thanh toán (ngoài FLS)</text>')
    o.append('<rect class="vz vz-ext" x="743" y="10" width="669" height="194" rx="6"/>')
    o.append('<text class="vt" x="751" y="28">GOOGLE SHEETS · tầng nhập tay (ngoài FLS)</text>')
    for v, (n1, n2, y0, y1) in VUNG.items():
        o.append(f'<rect class="vz vz-{v}" x="124" y="{y0}" width="1288" height="{y1 - y0}" rx="6"/>')
        o.append(f'<text class="vr" x="10" y="{y0 + 18}">{E(n1)}</text>')
        o.append(f'<text class="vr2" x="10" y="{y0 + 32}">{E(n2)}</text>')
    o.append('<text class="vr" x="10" y="28">NGUỒN</text><text class="vr2" x="10" y="42">ngoài FLS, chỉ-đọc</text>')
    for d, (_v, y0, h, nh) in DAI.items():
        if not nh:
            continue
        if d in ("A0", "A1"):
            o.append(f'<text class="br" x="10" y="{y0 + h / 2 + 18}">{E(nh)}</text>')
        else:
            o.append(f'<text class="br" x="10" y="{y0 + h / 2 + 4}">{E(nh)}</text>')
    # ranh giới FLS
    o.append('<line class="ranh" x1="124" y1="261" x2="1412" y2="261"/>')
    for i, s in enumerate(("◀ FPS: kết nối CSDL", "chỉ-đọc · vai đọc riêng", "Sheets API · TK dịch vụ ▶",
                           "quyền chỉ-đọc")):
        o.append(f'<text class="rt" x="{tam(3)}" y="{213 + i * 12}" text-anchor="middle">{E(s)}</text>')
    o.append('<text class="rt" x="182" y="256" text-anchor="middle">ranh giới FLS</text>')
    # hộp
    for h in HOP:
        x0, x1 = h.x
        y0, y1 = h.y
        cls = f"hop hop-{h.loai} tt-{h.tt}"
        o.append(f'<g class="{cls}"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
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
    # mũi tên
    for t in TEN:
        x1, y1, x2, y2 = doan(t)
        if t.x is not None:
            y2 -= 1
        else:
            x2 += -1 if x2 > x1 else 1
        o.append(f'<line class="ten ten-{t.tt}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'marker-end="url(#m{t.tt})"/>')
        if t.x is not None:
            o.append(f'<text class="tl" x="{x1 + 4:.1f}" y="{(y1 + y2) / 2 + 4:.1f}">{t.ma}</text>')
        else:
            o.append(f'<text class="tl" x="{(x1 + x2) / 2:.1f}" y="{y1 - 4:.1f}" text-anchor="middle">{t.ma}</text>')
    o.append('</svg>')
    return "\n".join(o)


# ───────────────────────────── bảng ─────────────────────────────
TT_CHU = {"b": "có mã", "q": "GĐ1 dựng", "n": "đề xuất"}


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
        o.append(f'<tr><td class="id"><i class="ln ln-{t.tt}"></i>{t.ma}</td>'
                 f'<td>{E(a.ten)} → {E(b.ten)}</td><td>{E(t.cai_gi)}</td><td><code>{E(t.khoa)}</code></td>'
                 f'<td>{E(t.ban_so)}</td><td>{E(t.cong)}</td><td>{pill(t.co_ma)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


LOAI_CHU = {"o": "khởi động", "x": "nguồn ngoài", "d": "dữ liệu", "p": "xử lý"}
VUNG_BANG = [("Nguồn ngoài · FPS", ("A0", "A1")), ("Nguồn ngoài · Google Sheets", ("B0", "B1")), ("FLS · NẠP", ("c1", "c2", "c3", "c4")),
             ("FLS · SỔ", ("d1", "d2")), ("ĐẦU RA", ("e1",))]


def bang_canh() -> str:
    vao: dict[str, list[str]] = {h.ma: [] for h in HOP}
    ra: dict[str, list[str]] = {h.ma: [] for h in HOP}
    for t in TEN:
        ra[t.tu].append(t.ma)
        vao[t.toi].append(t.ma)
    o = ['<div class="scroll"><table class="audit">',
         '<thead><tr><th>hộp</th><th>loại · trạng thái</th><th>vào</th><th>ra</th><th>đối chiếu mã / tài liệu</th>'
         '</tr></thead><tbody>']
    for vn, dais in VUNG_BANG:
        o.append(f'<tr class="b1"><th colspan="5">{E(vn)}</th></tr>')
        for d in dais:
            if len(dais) > 1:
                o.append(f'<tr class="b2"><th colspan="5">{E(DAI[d][3] or DAI[d.replace("B", "A")][3])}</th></tr>')
            for h in [h for h in HOP if h.dai == d]:
                kd = " · khởi bởi " + ", ".join(h.huy) if h.huy else ""
                o.append(f'<tr><td><b>{E(h.ten)}</b></td><td>{LOAI_CHU[h.loai]} · {TT_CHU[h.tt]}{E(kd)}</td>'
                         f'<td class="mono">{" ".join(vao[h.ma]) or "—"}</td>'
                         f'<td class="mono">{" ".join(ra[h.ma]) or "—"}</td><td>{E(h.doi_chieu)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


# ───────────────────────────── trang ─────────────────────────────
CSS = r"""
/* Bố cục: hình rộng 1420 nằm trong khung cuộn riêng; chữ một cột; bảng gom 2 tầng theo luật vẽ voi. */
:root{
  --bg:#f6f7f5; --paper:#ffffff; --fg:#1c231f; --muted:#59645d; --line:#d3d9d4;
  --accent:#1f4e79; --accent-soft:#e2ebf4;
  --ok:#2e7d4f; --ok-soft:#dcefe3; --mid:#a86d12; --mid-soft:#fff0cf; --no:#7d8580; --no-soft:#eceeec;
  --prop:#2f62c9; --prop-soft:#e4ecfb;
  --ext:#f1ece2; --zc:#eaf0f6; --zd:#eaf3ed; --ze:#f3eef6; --box:#ffffff; --orig:#fdf6e6;
  --sans:"IBM Plex Sans",system-ui,"Segoe UI",Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;
  --serif:"IBM Plex Serif",Georgia,serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#141815; --paper:#1c221f; --fg:#e5eae6; --muted:#a0aaa3; --line:#353d38;
  --accent:#8fb8e0; --accent-soft:#213041;
  --ok:#6fcf97; --ok-soft:#1d3729; --mid:#e2b45a; --mid-soft:#3a2f18; --no:#8d968f; --no-soft:#262b28;
  --prop:#86a8f0; --prop-soft:#1f2a44;
  --ext:#29251e; --zc:#1a222a; --zd:#1a271f; --ze:#251f29; --box:#222926; --orig:#2d281c; color-scheme:dark }}
:root[data-theme="dark"]{
  --bg:#141815; --paper:#1c221f; --fg:#e5eae6; --muted:#a0aaa3; --line:#353d38;
  --accent:#8fb8e0; --accent-soft:#213041;
  --ok:#6fcf97; --ok-soft:#1d3729; --mid:#e2b45a; --mid-soft:#3a2f18; --no:#8d968f; --no-soft:#262b28;
  --prop:#86a8f0; --prop-soft:#1f2a44;
  --ext:#29251e; --zc:#1a222a; --zd:#1a271f; --ze:#251f29; --box:#222926; --orig:#2d281c; color-scheme:dark }
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--fg);font:15px/1.55 var(--sans);
  padding-block:0 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:1440px;margin:0 auto}
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
td.id{font-family:var(--mono);white-space:nowrap;font-weight:500}
.ln{display:inline-block;width:18px;height:0;border-top:2px solid var(--muted);vertical-align:middle;margin-right:6px}
.ln-q{border-top:2px dashed var(--mid)} .ln-n{border-top:2px dashed var(--prop)}
.pill{display:inline-block;font:500 12px/1.3 var(--mono);padding:3px 7px;border-radius:3px}
.ok{background:var(--ok-soft);color:var(--ok)} .mid{background:var(--mid-soft);color:var(--mid)}
.no{background:var(--no-soft);color:var(--no)} .ext{background:var(--ext);color:var(--muted)}
.legend{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:13px;color:var(--muted);margin:10px 0}
.legend span{display:inline-flex;align-items:center;gap:6px}
.sw{width:16px;height:12px;border-radius:2px;border:1.3px solid var(--line);display:inline-block}
.diagram{overflow-x:auto;background:var(--paper);border:1px solid var(--line);border-radius:4px;padding:8px;margin:0}
.diagram svg{display:block;min-width:1200px;width:100%;height:auto;font-family:var(--sans)}
figcaption{font-size:13px;color:var(--muted);margin:8px 2px 0;max-width:none}
.vz{stroke:var(--line);stroke-width:1} .vz-ext{fill:var(--ext)} .vz-C{fill:var(--zc)} .vz-D{fill:var(--zd)} .vz-E{fill:var(--ze)}
.vt{font:600 11.5px var(--mono);fill:var(--muted);letter-spacing:.04em}
.vr{font:700 12px var(--mono);fill:var(--accent);letter-spacing:.04em}
.vr2{font:10.5px var(--sans);fill:var(--muted)}
.br{font:600 11.5px var(--sans);fill:var(--fg)}
.ranh{stroke:var(--accent);stroke-width:1.4;stroke-dasharray:8 4}
.rt{font:500 10.5px var(--mono);fill:var(--accent)}
.hop rect{stroke-width:1.3;fill:var(--box);stroke:var(--muted)}
.hop-x rect{fill:var(--ext)} .hop-o rect{fill:var(--orig);stroke:var(--mid)} .hop-p rect{stroke:var(--accent)}
.tt-q rect{stroke:var(--mid);stroke-dasharray:6 3} .tt-n rect{stroke:var(--prop);stroke-dasharray:6 3}
.t1{font:600 12.5px var(--sans);fill:var(--fg)} .to{font:700 11px var(--mono);fill:var(--fg);letter-spacing:.02em}
.t2{font:11.5px var(--sans);fill:var(--fg)} .t2o{font:11px var(--sans);fill:var(--muted)}
.t2n{font:italic 11.5px var(--sans);fill:var(--prop)} .t3{font:10.5px var(--mono);fill:var(--muted)}
.huy{fill:var(--orig);stroke:var(--mid);stroke-width:1} .huyt{font:600 9.5px var(--mono);fill:var(--mid)}
.ten{stroke-width:1.6;fill:none} .ten-b{stroke:var(--muted)} .ten-q{stroke:var(--mid);stroke-dasharray:6 3}
.ten-n{stroke:var(--prop);stroke-dasharray:6 3}
.mk-b{fill:var(--muted)} .mk-q{fill:var(--mid)} .mk-n{fill:var(--prop)}
.tl{font:600 10.5px var(--mono);fill:var(--accent)}
.note{border-left:3px solid var(--mid);background:var(--mid-soft);padding:8px 12px;max-width:96ch;font-size:14px}
ol.fix li,ul.terms li{margin:6px 0} ul.terms ul{margin:4px 0;padding-left:1.1em}
footer{margin-top:48px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);padding-top:10px}
@media (max-width:640px){ h1{font-size:24px} body{font-size:14px} }
"""

THAN_TREN = """
<header class="top">
  <h1>Voi FLS-tobe-phase1</h1>
  <p class="meta"><b>v0.2 · 2026-11-03</b> · Giai đoạn 1: đi hết INPUT, về <b>một</b> bảng ITL, mọi dòng có pháp nhân. Phiếu chi lấy từ <b>FPS</b> qua <b>hợp đồng dữ liệu FPS → FLS</b> (§5).
  Vẽ lại theo luật <i>vẽ voi</i>: gọi đúng tên từng thứ trước, rồi mới gom ≤ 5. Hình, bảng mũi tên và bảng kiểm cạnh <b>sinh từ cùng một bản khai</b> (<code>docs/ITL/_tools/sinh_voi_phase1.py</code>), máy kiểm hình trước khi ghi.<br>
  PD Now là bản gốc tham khảo: trang này chỉ mượn <b>thuật ngữ</b> (PE · PI · PM · PC · LE · CDT · HD/KRF · Reference No · General Trustest), không dùng tên sheet, tên file hay bước tính của nó. Mã FLS @ <code>2d1b710</code>.</p>
</header>
"""


def trang() -> str:
    k = kiem()
    if k["loi"]:
        raise SystemExit("⛔ hình SAI:\n  " + "\n  ".join(k["loi"]))
    so_dai = len(DAI)
    cap = (f'Hình 1 — Voi FLS-tobe-phase1. Máy kiểm lúc sinh: <b>5 vùng · {so_dai} dải · {k["hop"]} hộp · '
           f'{k["ten"]} mũi tên</b> ({k["doc"]} dọc · {k["ngang"]} ngang) · <b>0</b> mũi tên chéo · <b>0</b> mũi tên nhảy dải · '
           f'<b>{k["cheo"]}</b> chỗ hai mũi tên cắt nhau · <b>0</b> mũi tên cắt qua hộp. Mỗi dải 2–5 hộp, mỗi vùng 1–4 dải. '
           'Hai thứ cố ý <b>không vẽ thành mũi tên</b>: ① điểm khởi động (S1–S5) vẽ bằng <b>huy hiệu</b> trên hộp nó khởi, '
           'vì một nhịp kích ba phép chụp sẽ phải cắt sáu mũi tên đi vào; ② <i>GHI tay</i> đọc dòng sổ và ứng viên lệnh chi '
           'từ dải dưới (chiều đọc ngược). Ba hộp <b>gộp vẽ</b>: ảnh FPS (phiếu + danh mục, một nguồn một hợp đồng), '
           'phiếu đã duyệt (4 loại), lớp sửa (5 bảng luôn ghi trong cùng một giao dịch).')
    o = ['<!doctype html><html lang="vi"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
         '<title>Voi FLS-tobe-phase1</title>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;family=IBM+Plex+Serif:wght@600&amp;display=swap">',
         f'<style>{CSS}</style></head><body><main>', THAN_TREN,
         '<h2>§1 · Con voi — 5 vùng theo nơi chạy, dải theo đời sống của dữ liệu</h2>',
         '<div class="legend">'
         '<span><i class="sw" style="background:var(--orig);border-color:var(--mid);border-radius:6px"></i>khởi động (người · nhịp)</span>'
         '<span><i class="sw" style="background:var(--ext)"></i>nguồn ngoài FLS</span>'
         '<span><i class="sw" style="border-color:var(--muted)"></i>dữ liệu (tên của vật)</span>'
         '<span><i class="sw" style="border-color:var(--accent)"></i>xử lý (ĐỘNG TỪ + danh từ)</span>'
         '<span><i class="ln"></i>có mã</span><span><i class="ln ln-q"></i>GĐ1 phải dựng (đã chốt)</span>'
         '<span><i class="ln ln-n"></i>đề xuất của trang này (chờ owner)</span>'
         '<span><span class="pill mid" style="font-size:10px">S1</span> huy hiệu = hộp này do điểm khởi động S1 chạy</span>'
         '</div>',
         f'<figure class="diagram">{svg()}<figcaption>{cap}</figcaption></figure>',
         """
<h3>Thuật ngữ trên hình</h3>
<ul class="terms">
<li><b>Phiếu FPS</b><ul><li>PE dự toán · PI hoá đơn · PM lệnh chi · PC quyết toán</li><li><i>slip</i> = phiếu · <i>line</i> = dòng tiền trong phiếu; line giữ tiền + khoá chuỗi, slip giữ mô tả · ngân hàng · kỳ dịch vụ · Reference No · pháp nhân trả · CDT</li></ul></li>
<li><b>Tiền</b><ul><li>General Trustest: bộ trường tối thiểu của một dòng tiền — ngày · tiền · tiền tệ · LE</li><li>Reference No: mã ngân hàng cấp, có trên sao kê và trên PM slip — khoá ghép tiền ↔ lệnh chi</li></ul></li>
<li><b>Ba vai pháp nhân</b> (xem câu 1, §7)<ul><li>pháp nhân TK: chủ tài khoản tiền đi ra / vào — khai theo nguồn</li><li><code>le_payer</code>: pháp nhân thanh toán ghi trên PM</li><li><code>le</code>: pháp nhân nhận, khi đối tác của PE là pháp nhân Apero; <code>le ≠ le_payer</code> ⇒ cờ nội bộ (<code>is_intercompany</code>)</li></ul></li>
<li><b>Chiều chi phí</b><ul><li>CDT1 chủ dự toán (gốc ở PE slip) · HD/KRF mã hạng mục · Budget Code mã ngân sách</li></ul></li>
<li><b>Máy FLS</b><ul><li>canon 36 trường: khuôn dòng chuẩn · <code>content_key</code>: khoá chống trùng nội dung</li><li><code>chup_id</code> / <code>run_id</code>: vết lần chụp / lần nạp · bản khai nguồn: bố cục cột + thứ tự ngày (+ pháp nhân TK)</li><li>lớp sửa: mọi thay đổi là dòng thêm · sổ hiệu lực: sổ gốc + lớp sửa, đọc ra một bảng</li></ul></li>
</ul>

<h2>§2 · Năm chỗ bản v0.1 vẽ sai — sửa trước khi gom</h2>
<ol class="fix">
<li><b>Bản khai nguồn đứng trước phép chụp.</b> Ảnh sao kê đọc vùng chuẩn <i>theo</i> bản khai và ghi lại <code>khai_version</code> (<code>fls/repo/chup.py:16</code>, <code>tools/chup_sao_ke.py</code>). v0.1 không có bản khai trên hình.</li>
<li><b>Pháp nhân của dòng tiền phải có lúc DỰNG, không phải một bước sau.</b> <code>fls_itl</code> chỉ-thêm và pháp nhân là cột của dòng sổ ⇒ luật gắn pháp nhân phải nằm trong bản khai của nguồn (người khai, owner ký), đọc ở bước dựng. v0.1 vẽ "GẮN pháp nhân" thành hộp riêng, không nói luật nằm ở đâu.</li>
<li><b>Hai đường ghi tách bạch.</b> Máy ghi cả lượt nạp trong <i>một</i> giao dịch (run · dòng sổ · dòng loại · mối nối · gợi ý — <code>chay_nap.py:621</code>); người ghi qua <code>ghi_tay.py</code>, chỗ ghi duy nhất. v0.1 gộp hai đường làm một hộp "NỐI".</li>
<li><b>Năm điểm khởi động vẽ riêng.</b> Nhịp mỗi giờ chỉ <i>chụp</i>; khai nguồn, xem trước lô, Nhận lô, ghép/sửa là bốn cú bấm khác nhau của kế toán. v0.1 không vẽ ai hay cái gì làm cho dữ liệu chạy.</li>
<li><b>"Một bảng ITL duy nhất" là sổ hiệu lực, không chỉ <code>fls_itl</code>.</b> Sửa là thêm bút toán, nên bảng người đọc và hệ khác nhận = sổ gốc + lớp sửa. v0.1 dừng ở <code>fls_itl</code>.</li>
</ol>

<h2>§3 · Mũi tên nói gì — 37 mũi tên, 5 nhóm</h2>
<p>Mỗi mũi tên là <b>một dòng dữ liệu</b>: nó chở gì, nối bằng khoá nào, một-nhiều ra sao, cổng nào đứng trên nó, và hôm nay đã chảy chưa. Mã mũi tên trùng với nhãn trên hình.</p>
""",
         bang_ten(),
         '<h2>§4 · Kiểm cạnh — mỗi hộp: vào gì, ra gì, khớp mã nào</h2>'
         '<p>Bảng này máy sinh từ cùng bản khai với hình: cột <i>vào</i>/<i>ra</i> là mã mũi tên, nên một mũi tên thiếu trên hình cũng thiếu ở đây.</p>',
         bang_canh(),
         """
<h2>§5 · Hợp đồng dữ liệu FPS → FLS — trường nào phải sang</h2>
<p>Trường cần có lấy từ các nhóm khoá của bản gốc. "Ở FPS" = đã thấy trong code FPS theo tài liệu đối chiếu (<code>FLS-vs-FPS-Compare-Audit.md</code> §3–§4, <code>FLS-ERD-Full-Detail.md</code> §0.4); "hỏi FPS" = chưa thấy, phải xác nhận hoặc mở CR.</p>
<div class="scroll"><table>
<thead><tr><th colspan="2" class="sup">FPS</th><th colspan="2" class="sup">Hợp đồng</th><th colspan="2" class="sup">FLS</th></tr>
<tr><th>thực thể</th><th>mức</th><th>trường cần sang</th><th>thoả nhóm khoá</th><th>đích trong FLS</th><th>ở FPS?</th></tr></thead>
<tbody>
<tr class="b1"><th colspan="6">PE — dự toán</th></tr>
<tr><td><code>fps_pe_slip</code></td><td>slip</td><td><code>pe_id</code> · <code>cdt_code</code> · <code>vendor_id</code> (đối tác nhận) · loại chi (đơn lẻ / tạm ứng) · ngày duyệt · <code>service_start/end_date</code> · trạng thái</td><td>khoá PE: CDT · Vendor · Singular/Advance · Action Date</td><td>ảnh FPS → chuỗi phiếu: CDT1 · đối tác · kỳ dịch vụ (nhánh PE)</td><td>cdt_code · service dates: <b>ở FPS</b> · loại chi, ngày duyệt: <b>hỏi FPS</b></td></tr>
<tr><td><code>fps_pe_line</code></td><td>line</td><td><code>line_id</code> · <code>pe_id</code> · <code>bgc_code</code> · <code>kr_code</code> · <code>amount</code> · <code>pe_date</code></td><td>khoá PE: Budget / KRF / HD</td><td>chuỗi phiếu: HD/KRF · Budget Code</td><td><b>ở FPS</b> · tiền tệ của line: <b>hỏi FPS</b></td></tr>
<tr class="b1"><th colspan="6">PI — hoá đơn</th></tr>
<tr><td><code>fps_pi_slip</code></td><td>slip</td><td><code>pi_id</code> · số hoá đơn · tệp hoá đơn (đường dẫn) · <code>service_start/end_date</code> · ghi chú</td><td>khoá PI: Invoice</td><td>chuỗi phiếu: hoá đơn · kỳ dịch vụ (nhánh PI) · ghi chú</td><td>service dates: <b>ở FPS</b> · số hoá đơn, tệp: <b>hỏi FPS</b></td></tr>
<tr><td><code>fps_pi_line</code></td><td>line</td><td><code>line_id</code> · <code>pi_id</code> · <code>pe_line_id</code> · <code>amount</code></td><td>khoá PI: PE ID</td><td>chuỗi PI → PE</td><td><code>pe_line_id</code> trên PI line: <b>hỏi FPS</b></td></tr>
<tr class="b1"><th colspan="6">PM — lệnh chi (mắt xích nối với tiền)</th></tr>
<tr><td><code>fps_pm_slip</code></td><td>slip</td><td><code>pm_id</code> · <b><code>reference_number</code></b> · <b><code>payer_id</code></b> · <code>bank_account_id</code> · loại giao dịch · <code>service_start/end_date</code> · trạng thái cuối</td><td>Reference No · General Trustest (LE trả)</td><td>ghép (c3) · <code>le_payer</code></td><td><b>ở FPS</b> (slip)</td></tr>
<tr><td><code>fps_pm_line</code></td><td>line</td><td><code>line_id</code> · <code>pm_id</code> · <b><code>pi_line_id</code></b> · <code>amount</code> · tiền tệ · <code>pm_date</code></td><td>khoá PM: PI ID · PE ID · Tiền · Tiền tệ</td><td><code>fls_pm_line</code> → mối nối</td><td>line_id · pm_id · pi_line_id · amount · pm_date: <b>ở FPS</b> · tiền tệ line, <code>pe_line_id</code> trực tiếp: <b>hỏi FPS</b></td></tr>
<tr class="b1"><th colspan="6">PC — quyết toán</th></tr>
<tr><td><code>fps_pc_slip</code> · <code>fps_pc_line</code></td><td>slip + line</td><td><code>pc_id</code> · <code>line_id</code> · phiếu gốc · <code>amount</code> · ngày</td><td>nhóm khoá PC: bản gốc để trống ⇒ GĐ1 chỉ chụp</td><td>ảnh FPS; chưa vào canon</td><td>bảng: <b>ở FPS</b> · cột: <b>hỏi FPS</b></td></tr>
<tr class="b1"><th colspan="6">Danh mục — nguồn của tên, hiệu lực và pháp nhân</th></tr>
<tr><td><code>fps_le</code></td><td>danh mục</td><td><code>le_code</code> · <code>le_name</code> · <code>country</code> · <code>is_active</code></td><td>General Trustest: LE</td><td><code>fls_le</code> (thay bản suy từ giá trị, hết 24/29 thiếu tên)</td><td><b>ở FPS</b>; <code>is_entity</code> là CR</td></tr>
<tr><td><code>fps_bank_account</code></td><td>danh mục</td><td><code>bank_account_id</code> · số TK · ngân hàng · tiền tệ · <b>pháp nhân chủ TK</b></td><td>General Trustest: LE qua TK</td><td>k1: đề xuất pháp nhân TK cho bản khai nguồn</td><td>bảng: <b>ở FPS</b> · cột chủ TK: <b>hỏi FPS</b> / CR</td></tr>
<tr><td><code>fps_ven</code> (+ khối đối tác)</td><td>danh mục</td><td><code>vendor_id</code> · tên · khối · <b>đối tác nào là pháp nhân Apero</b></td><td>khoá PE: Vendor</td><td>đối tác · <code>le</code> (pháp nhân nhận)</td><td>vendor: <b>ở FPS</b> · luật vendor ↔ pháp nhân: ở FPS, <b>hỏi FPS</b></td></tr>
<tr><td><code>fps_cdt</code> · <code>fps_kr</code> · <code>fps_bgc</code></td><td>danh mục</td><td>mã · tên · cha · hiệu lực</td><td>CDT · khoá PE</td><td>tên cho chuỗi phiếu</td><td><b>ở FPS</b></td></tr>
<tr><td><code>fps_exchange_rate</code></td><td>danh mục</td><td>tiền tệ từ / tới · tỷ giá · ngày hiệu lực</td><td>(GĐ2)</td><td>chụp sẵn; GĐ1 không quy đổi</td><td><b>ở FPS</b></td></tr>
</tbody></table></div>
<p class="note"><b>Ba điểm phải chốt với FPS trước khi viết bộ đọc:</b> ① Reference No nằm ở <b>PM slip</b>, không ở line ⇒ FLS chia tiền theo line và đòi Σ line = tiền dòng. ② Kỳ dịch vụ nằm ở <b>slip</b> của PE/PI/PM ⇒ hai nhánh kỳ dịch vụ đều đọc từ slip. ③ CDT gốc ở <b>PE slip</b> ⇒ CDT1 lấy qua chuỗi PM → PI → PE, không lấy ở PM.</p>

<h2>§6 · Thứ tự làm trong GĐ1 — theo mũi tên</h2>
<div class="scroll"><table>
<thead><tr><th>bước</th><th>mũi tên / hộp dựng</th><th>vì sao đứng đây</th><th>cổng đóng bước (mong)</th></tr></thead>
<tbody>
<tr class="b1"><th colspan="4">Chặng I · Đóng họ tiền trên sổ đang có (bước 1–2)</th></tr>
<tr><td>1</td><td>k1 · b2 · cột pháp nhân TK trong bản khai nguồn</td><td>Rẻ nhất: tách tài khoản ra pháp nhân đã đo 8.387/8.387 trên 49 nguồn; đổi ngay chiều pháp nhân của sổ đang có</td><td>pháp nhân TK rỗng = 0 hoặc danh sách có tên TK, owner ký (14 TK · 211 dòng)</td></tr>
<tr><td>2</td><td>x4 · b3 cho lằn Cash</td><td>Cùng bộ đọc với sao kê, chỉ bật lằn và khuôn quỹ</td><td>số dòng = sổ quỹ từng quỹ · nạp lại = 0 trùng · số dư theo ngày khớp</td></tr>
<tr class="b1"><th colspan="4">Chặng II · Mở họ phiếu và chi phí (bước 3–5)</th></tr>
<tr><td>3</td><td>x1 · x2 · b1 · g1 (FPS 4 phiếu + danh mục)</td><td>Hợp đồng §5 chốt trước; ảnh FPS dùng lại lằn ảnh chụp, không dựng hệ thứ hai</td><td>0 khoá phiếu trỏ rỗng · chiều phiếu khớp sổ đang chạy 100% từng ô</td></tr>
<tr><td>4</td><td>x5 · b4 · g4 (HR)</td><td>HR đã tách HD/KRF ở nguồn ⇒ không phân bổ; chỉ đọc đầu ra, không mở hộp đen lương</td><td>Σ từng sổ từng năm = nguồn · 0 dòng thiếu HD</td></tr>
<tr><td>5</td><td>x6 · b4 · g4 (nền tảng SC · PS)</td><td>Chờ owner chốt phạm vi (câu 5)</td><td>số dòng = sổ nguồn</td></tr>
<tr class="b1"><th colspan="4">Chặng III · Chứng minh một bảng (bước 6–7)</th></tr>
<tr><td>6</td><td>h2 · h3 · sổ hiệu lực thành một view có tên</td><td>Hôm nay màn tự ghép ở cửa đọc; hệ khác cần một bảng</td><td>một SELECT trả đủ 4 họ nguồn · đủ 3 vai pháp nhân</td></tr>
<tr><td>7</td><td>h1 · h4 · v1 · v4 (cổng GĐ1 + xuất đối chiếu)</td><td>Hợp nhất chỉ chứng minh được khi cả 4 họ đã vào</td><td>Σ theo pháp nhân = Σ theo nguồn, từng tiền tệ · chênh với sổ đang chạy liệt kê từng dòng, có tên</td></tr>
</tbody></table></div>

<h2>§7 · Câu chờ owner</h2>
<div class="scroll"><table>
<thead><tr><th>#</th><th>câu</th><th>vì sao phải hỏi</th><th>chặn</th></tr></thead>
<tbody>
<tr><td>1</td><td><b><code>le</code> nghĩa là gì?</b> Đề xuất: tách ba vai thành ba trường — pháp nhân TK (mới, từ bản khai) · <code>le_payer</code> (PM) · <code>le</code> = pháp nhân nhận (PE). "Chi phí về pháp nhân" ở GĐ1 = pháp nhân TK.</td><td>Hai tài liệu nói khác nhau: <code>00_MASTER_INDEX</code> (<code>QĐ-ITL-144</code>) ghi <code>le</code> "suy được 100% từ <code>source_sheet</code>" (tức chủ TK); <code>05_DATA_DICTIONARY_ERD</code> §ⓑ ghi <code>le</code> = "ai nhận" ← đối tác của PE</td><td>bước 1</td></tr>
<tr><td>2</td><td>Pháp nhân TK nằm trong <b>bản khai nguồn</b> (máy đề xuất, kế toán khai, owner ký) — đồng ý?</td><td>14 TK · 211 dòng có tên TK không nói pháp nhân; hai bên còn gọi một pháp nhân bằng hai mã (<code>VVOH - Astronex</code> ↔ <code>ASTRONEX</code>)</td><td>bước 1</td></tr>
<tr><td>3</td><td>FPS cấp <b>kết nối CSDL chỉ-đọc</b> (vai đọc riêng) hay <b>xuất bảng định kỳ</b>?</td><td>Quyết định tuyến của x1/x2; hôm nay PM đi qua Sheets</td><td>bước 3</td></tr>
<tr><td>4</td><td>HR và nền tảng: FLS đọc sổ ở Sheets như hôm nay, hay chờ hệ nguồn có hợp đồng?</td><td>Quyết định tuyến của x5/x6</td><td>bước 4–5</td></tr>
<tr><td>5</td><td>GI/OMC không vào sổ (là khoá phân bổ, dùng ở GĐ3)? AP/AR lùi khỏi GĐ1?</td><td>Phạm vi họ "Platform" của sổ</td><td>bước 5</td></tr>
</tbody></table></div>

<footer>Voi FLS-tobe-phase1 v0.2 · 2026-11-03 · sinh bởi <code>docs/ITL/_tools/sinh_voi_phase1.py</code> · cùng bộ với <code>_PD_NOW_VOI_VA_GIAI_DOAN.md</code>. Trang tự chứa, chỉ gọi mạng cho font.</footer>
</main></body></html>
"""]
    return "\n".join(o)


def main() -> int:
    k = kiem()
    print(f"hộp {k['hop']} · mũi tên {k['ten']} (dọc {k['doc']} · ngang {k['ngang']}) · cắt nhau {k['cheo']}")
    for d in DAI:
        print(f"  dải {d}: {sum(1 for h in HOP if h.dai == d)} hộp")
    if k["loi"]:
        print("⛔ LỖI:\n  " + "\n  ".join(k["loi"]))
        return 1
    if "--kiem" in sys.argv:
        print("✅ hình đúng luật — ⛔ không ghi (--kiem)")
        return 0
    DICH.write_text(trang(), encoding="utf-8")
    print(f"✅ đã ghi {DICH.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
