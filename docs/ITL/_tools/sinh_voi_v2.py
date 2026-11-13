# -*- coding: utf-8 -*-
"""Sinh BẢN NHÁP `docs/ITL/02_BA/Artifacts/Voi-FLS-v2-nhap.html` — voi FLS vẽ lại theo kiến trúc FPA.

    python docs/ITL/_tools/sinh_voi_v2.py          # kiểm + sinh, in số đếm
    python docs/ITL/_tools/sinh_voi_v2.py --kiem   # chỉ kiểm, ⛔ không ghi

⭐ Owner 11/11 (KhanhCQ): "FLS sẽ tương tự FPA: cùng collect data (RI) → Calculate → Allocate →
   Standard Output → Report. Một con voi chia theo layers, theo hàng và cột như hình FPA. Đồng bộ
   cách đặt tên: đọc tên ô là biết ô thuộc bước nào, phần nào — tiền tố = phần tính (Actual/Plan)
   + bước (CA = calculate …), như ACA / PCA của FPA."
   ⛔ CHƯA sửa vào artifact chính (`sinh_voi_phase1.py`) — owner duyệt bản này rồi mới gộp.

⭐ Ba nguồn đọc lúc dựng:
   ⓐ PD Now (FS2) — 116 bước, ma trận I/O → `pdnow_buoc.json` (175 mũi tên suy từ ma trận).
   ⓑ PD200 Runner Guide + ảnh "[A] Tobe #FP&A #ARCHITECTURE" — mượn LƯỚI (INPUT · CALCULATE ·
      ALLOCATE · WAREHOUSE · REPORT) và NGỮ PHÁP TÊN bước + phần (FPA: APR · ACA). Owner 12/11: FLS chỉ có số
      thực ⇒ bỏ chữ ACTUAL và chữ A đầu mã; trục ngang đầu tiên là AGENT.
   ⓒ Mã FLS hôm nay — mỗi hộp ghi module / bảng / số đo đã có.

⭐ Luật máy kiểm (nổ nếu sai — luật vẽ voi `apr-vevoi`):
   ① TÊN: mã hộp = <kịch bản><bước>.<phần>; <bước> PHẢI trùng bước của cột (hoặc hàng) chứa hộp
      ⇒ "đọc tên là biết ô ở đâu" là một phép kiểm, ⛔ một lời hứa.
   ② MŨI TÊN: mọi mũi tên NẰM NGANG, đi trái → phải trong một làn hàng; làn ấy phải nằm trong cả hai
      hộp; ⛔ cắt qua hộp nào ở giữa (được đi qua làn TRỐNG).
   ③ ĐẾM: ≤ 5 hộp mỗi cột con trong một nhóm hàng; ≤ 5 nhóm cột; ≤ 5 hàng dữ liệu.
   ④ PHỦ: mỗi bước PD Now (116) thuộc ĐÚNG MỘT hộp TO-BE hoặc một rổ "ngoài GĐ1" có lý do.
"""
from __future__ import annotations

import html
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
DICH = GOC / "docs/ITL/02_BA/Artifacts/Voi-FLS-v2-nhap.html"
PDNOW = json.loads(Path(__file__).with_name("pdnow_buoc.json").read_text(encoding="utf-8"))
E = html.escape

# ═════════════════ NGỮ PHÁP TÊN ═════════════════
BUOC = {  # mã bước: (tên, nghĩa, nhóm PD Now)
    "RI": ("RAW INPUT", "chụp nguồn thô, đóng băng", "PD 1xx"),
    "PR": ("PREPARE", "dựng dòng chuẩn từ ảnh", "PD 2xx"),
    "SI": ("STANDARD INPUT", "ghép + sổ ITL hiệu lực", "PD 3xx"),
    "CA": ("CALCULATE", "quy đổi, gắn chiều CFA/PLA", "PD 4xx"),
    "SO": ("STANDARD OUTPUT", "khối KRF × kỳ (trước / sau phân bổ)", "PD 409–419 · 600–606"),
    "AL": ("ALLOCATE", "phân bổ về LE / CDT1", "PD 5xx"),
    "DW": ("WAREHOUSE", "kho FLS, truy ngược ô → giao dịch", "—"),
    "RP": ("REPORT", "báo cáo + màn hình", "PD 6xx"),
    "KS": ("KIỂM SOÁT", "cổng của từng bước (Agent 4)", "PD 204 · 209"),
    "IX": ("INDEX · CONFIG", "bản khai, danh mục, tỷ giá, khuôn", "PD 5xx TMP"),
}
MA_RE = re.compile(r"^(RI|PR|SI|CA|SO|AL|DW|RP|KS|IX)(\.[A-Z0-9]+(-[A-Z0-9]+)?)?$")

# ═════════════════ LƯỚI ═════════════════
# 11 cột con, gom 5 nhóm như hình FPA. (nhóm, nhãn cột con, mã bước)
COT = {
    1: ("INPUT", "RAW", "RI"), 2: ("INPUT", "PREPARE", "PR"),
    3: ("CALCULATE", "STANDARD INPUT · ghép", "SI"), 4: ("CALCULATE", "STANDARD INPUT · sổ ITL", "SI"),
    5: ("CALCULATE", "CALCULATE", "CA"), 6: ("CALCULATE", "STANDARD OUTPUT", "SO"),
    7: ("ALLOCATE", "ALLOCATE", "AL"), 8: ("ALLOCATE", "STANDARD OUTPUT", "SO"),
    9: ("WAREHOUSE", "KHO FLS", "DW"),
    10: ("REPORT", "báo cáo thành phần", "RP"), 11: ("REPORT", "báo cáo đích · màn", "RP"),
}
NHOM_COT = ["INPUT", "CALCULATE", "ALLOCATE", "WAREHOUSE", "REPORT"]
# ⭐ Owner 12/11: "các phần theo chiều ngang phải thể hiện được chiều của các agents" ⇒ tầng ngang ĐẦU là agent
#   (khung màu như "1. APR-ACA TA+L" của FPA), tầng bước INPUT…REPORT ở dưới. Tên agent: owner 06/11.
#   Chia theo hai file AS-IS: ITL 1/2 (RAW) gồm cả Transaction Mapping L1 (PD 301–308) ⇒ Agent 2 · ITL raw;
#   ITL 2/2 (ADJUSTED) (313–318) ⇒ Agent 3 · ITL Adjust. CALCULATE → REPORT là mã tất định (F0b: ⛔ cần mô hình).
#   Agent 4 · Auditor là một LÀN NGANG chạy suốt các cột (hàng KIỂM SOÁT).
AGENT_TEN = {"ag1": "Agent 1 · Collect_raw_data", "ag2": "Agent 2 · Generate Group Ledger (ITL raw)",
             "ag3": "Agent 3 · Filter Fulfill & Adjust (ITL Adjust)", "ma": "mã tất định · không agent",
             "ag4": "Agent 4 · Auditor (Compounding Loop)", "ix": "cấu hình · người khai, owner ký"}
AGENT_NHAN = {"ag1": ("AGENT 1 · RAW", "Collect_raw_data"), "ag2": ("AGENT 2 · ITL RAW", "Generate Group Ledger"),
              "ag3": ("AGENT 3 · ITL ADJUST", "Filter Fulfill & Adjust"),
              "ma": ("MÃ TẤT ĐỊNH", "Calculate → Report: luật + phép cộng, không cần mô hình (F0b)")}
AGENT_DAI = [("ag1", 1, 1), ("ag2", 2, 3), ("ag3", 4, 4), ("ma", 5, 11)]   # (agent, cột đầu, cột cuối) — chạy liền, ⛔ chồng


def agent_cua(h) -> str:
    if h.buoc == "KS":
        return "ag4"
    if h.buoc == "IX":
        return "ix"
    return next(a for a, c0, c1 in AGENT_DAI if c0 <= h.cot[0] <= c1)
HANG = {  # mã hàng: (nhóm hàng, nhãn, nhãn phụ, mã bước của hàng nếu là hàng xuyên suốt)
    "BANK": ("DỮ LIỆU", "BANK", "tiền · sao kê · quỹ · CCR", None),
    "PAY": ("DỮ LIỆU", "PAY", "lệnh chi · PE·PI·PM·PC", None),
    "HR": ("DỮ LIỆU", "HR", "lương · H1000", None),
    "PLT": ("DỮ LIỆU", "PLT", "nền tảng GI·OMC·SC·PS", None),
    "KS": ("KIỂM SOÁT", "KIỂM SOÁT", "NOW: người · TO-BE: Agent 4", "KS"),
    "IX": ("CONFIG", "INDEX", "khai · danh mục · tỷ giá", "IX"),
}
LX, CW, GAP = 178, 158, 30
TOP = 120
HY = {"BANK": (TOP, 104), "PAY": (TOP + 118, 104), "HR": (TOP + 236, 104), "PLT": (TOP + 354, 104),
      "KS": (TOP + 500, 70), "IX": (TOP + 584, 70)}        # khe trên KS: dải nhãn Agent 4
W = LX + 11 * CW + 10 * GAP + 18
H = TOP + 584 + 70 + 12
THU_TU_HANG = list(HY)


def cx(c: int) -> tuple[int, int]:
    x = LX + (c - 1) * (CW + GAP)
    return x, x + CW


def lan(h: str) -> float:          # tâm làn của một hàng
    y, hh = HY[h]
    return y + hh / 2


@dataclass
class Hop:
    ma: str
    cot: tuple[int, int]          # cột con đầu, cuối
    hang: tuple[str, str]         # hàng đầu, cuối
    ten: str
    hien: tuple[str, ...]         # dòng hiện trên hình
    tt: str                       # ✅ · ◐ · ⛔ · — kèm chữ
    pd: tuple[str, ...] = ()      # bước PD Now hộp này thay (AS-IS ↔ TO-BE)
    vao: tuple[str, ...] = ()     # đầu vào ngoài mũi tên (nguồn ngoài, người, cấu hình)
    ra: tuple[str, ...] = ()      # đầu ra ngoài mũi tên
    fls: str = ""                 # mã / bảng FLS hôm nay — có số đo
    cu: str = ""                  # hộp của voi v0.9 mà hộp này thay
    nguoi: str = ""               # bước có tay người

    @property
    def x(self):
        return cx(self.cot[0])[0], cx(self.cot[1])[1]

    @property
    def y(self):
        a, b = THU_TU_HANG.index(self.hang[0]), THU_TU_HANG.index(self.hang[1])
        y0 = HY[THU_TU_HANG[a]][0]
        y1 = HY[THU_TU_HANG[b]][0] + HY[THU_TU_HANG[b]][1]
        return y0, y1

    @property
    def buoc(self):
        return MA_RE.match(self.ma).group(1)


def r(a: int, b: int | None = None):
    return tuple(str(i) for i in range(a, (b or a) + 1))


HOP: list[Hop] = [
    # ── ① INPUT · RAW — chụp, đóng băng (Agent 1) ──
    Hop("RI.BANK", (1, 1), ("BANK", "BANK"), "ẢNH SAO KÊ · QUỸ · CCR", ("60 sao kê · 8 quỹ · 2 sheet CCR", "đọc theo bản khai"),
        "◐ Bank ✅ · Cash ⛔ · CCR ⛔", r(115, 116) + ("200", "202", "204", "209"),
        vao=("sheet R | sao kê — KT ngân hàng dán (PD 115 · 200)", "sheet R | sổ quỹ — KT quỹ ghi (116 · 202)",
             "2. CCR · 2. CCR Cash — người nhập số dư (204 · 209)", "IX.KHAI — bố cục cột · thứ tự ngày"),
        fls="tools/chup_sao_ke.py (LAN='Bank') · fls_chup · fls_chup_nguon (khai_version) — 60 nguồn · 182 ảnh; Cash, CCR: 0 ảnh",
        cu="anhTien", nguoi="dán / ghi / nhập số dư ở Google Sheets"),
    Hop("RI.PAY", (1, 1), ("PAY", "PAY"), "ẢNH SỔ CÁI PM · PC", ("PE·PI·PM·PC đã duyệt", "Email ⛔ vào kho"),
        "◐ PM ✅ · PC ⛔", r(107, 114),
        vao=("FPS · A|PAY100 PE11/PI11/PM11/PC11 Entry Data — người đề nghị Gform, sếp duyệt (107–114)",),
        fls="fls_pm_line 3.772 dòng (migration 0011/0023) · fls/repo/anh_pm.py · PM_COT_RIENG_TU = {Email Address}",
        cu="anhFPS", nguoi="đề nghị · duyệt · CA gõ Reference No sau khi chi"),
    Hop("RI.HR", (1, 1), ("HR", "HR"), "ẢNH SỔ H1000", ("payroll tháng · đã tách HD·CDT1", "số FT do kế toán dán"),
        "⛔", ("101",),
        vao=("H1000 Ledger (APERO-HR Allocate HD) — HR · C&B lập, kế toán dán số FT (101)",),
        fls="0 mã: grep H1000 trong fls/ = 1 tệp, chỉ chú thích",
        cu="anhHR", nguoi="HR lập payroll · KT dán số FT"),
    Hop("RI.PLT", (1, 1), ("PLT", "PLT"), "ẢNH 4 NGUỒN NỀN TẢNG", ("GI·OMC: Looker", "SC·PS: Google Sheets"),
        "⛔", r(103, 106),
        vao=("GI · OMC — Looker, Data (AnhTQ) xuất (103 · 104)", "SC — 'Chi phí Service Apero', SHQ1 (105)",
             "PS — 'AperoGroup_Payment', SHQ2 (106)"),
        fls="0 mã: chup_sao_ke.py chỉ chụp lằn Bank",
        cu="anhNT", nguoi="Data xuất Looker · Luận / KT cập nhật Gsheet"),
    # ── ① INPUT · PREPARE — dựng dòng chuẩn (Agent 2) ──
    Hop("PR.BANK", (2, 2), ("BANK", "BANK"), "DÒNG TIỀN + SỐ DƯ NGÀY", ("canon 36 trường · 2 vế Nợ/Có", "LE TK · content_key"),
        "◐ bank 8.338/8.338 · quỹ ⛔", ("201", "203") + r(205, 208),
        fls="fls/adapters/sao_ke.py + sao_ke_canon.py — 8.338/8.338 dòng bank; số dư ngày: 0 mã",
        cu="dTien"),
    Hop("PR.PAY", (2, 2), ("PAY", "PAY"), "DÒNG LỆNH PM · PC", ("duỗi line · đặt kiểu", "Ref · tiền · HD · CDT1 · LE trả"),
        "◐ 14 cột có kiểu · 13 thô", r(214, 218),
        fls="fls/adapters/pm_join.py — 28 cột: 14 có kiểu · 1 cấm · 13 thô; PC: 0 tham chiếu",
        cu="dLenh"),
    Hop("PR.HR", (2, 2), ("HR", "HR"), "DÒNG LƯƠNG", ("NIS·INT·COM·PIT · HD·CDT1·LE", "Số CT (số FT) · đủ tháng"),
        "⛔", r(219, 222),
        fls="0 mã (adapter D chưa có)", cu="dHR"),
    Hop("PR.PLT", (2, 2), ("PLT", "PLT"), "CHI PHÍ 4 LOẠI", ("vendor · ngày · NoTrans · tiền", "+ Combine Code"),
        "⛔", r(210, 213),
        fls="0 mã: grep 'Combine Code' trong fls/ + tools/ = 0", cu="dNT"),
    # ── ② CALCULATE · STANDARD INPUT ──
    # ⭐ owner 13/11 (bình luận trên hình): "PLT cũng cần được đưa về standard input (tương đương ITL raw ở as-is).
    #   Vì giới hạn của nền tảng as-is nên H1000 và PLT không thể đưa vào, nhưng lên hệ thống mới SI cần đủ cả 4 phần"
    #   ⇒ SI.MAP · SI.ITL · CA.GL trải BANK → PLT; e8 vào SI.MAP (⛔ còn đi thẳng ALLOCATE); thêm output SI-4.
    Hop("SI.MAP", (3, 3), ("BANK", "PLT"), "GHÉP GIAO DỊCH ↔ LỆNH",
        ("PP1 Ref No → PM · PP2 Số CT → lương", "PP3 Combine Code → PE/PM (nền tảng)", "  Σ line = tiền · N×M để người",
         "→ L1 khớp · L1b lệch", "→ L2 FPS có, bank chưa", "→ L3 bank có, FPS không", "L3: vòng cộng dồn gợi ý loại GD"),
        "◐ PS Có: 26,79% dòng nối", r(302, 308),
        vao=("IX.MM — Mapping Master · luật ghép đã ký",),
        fls="fls/adapters/pm_join.py · fls/repo/may_ghep.py — fls_pm_link 2.263 · mẫu số PS Có 8.246; PP (2): 0 mã · PP (3) Combine Code: 0 mã",
        cu="ghep · ghep2 (+ hình 2)"),
    Hop("SI.ITL", (4, 4), ("BANK", "PLT"), "SỔ ITL HIỆU LỰC",
        ("gốc chỉ-thêm + lớp sửa (người › máy)", "một bảng · đủ 4 họ: BANK·PAY·HR·PLT", "dòng loại có lý do",
         "3 vai pháp nhân", "thay ITL Ledge + H1000 Ledge", "(Final · cột R–AT)"),
        "◐ 1 họ nguồn · parity 4.088/4.088", ("313", "314") + r(315, 319),
        vao=("người: ghép / sửa / đảo trên F01 · F02 (ghi_tay, actor từ thẻ)",),
        fls="fls_itl 8.387 · fls_adjustment 4.428 · fls_reject · fls_journal · final_rule 7 khối 4.088/4.088 ô · RAW 64.393/64.393 ô",
        cu="ghiNap · loai · soITL · lopSua · ghiTay · hieuLuc", nguoi="kế toán sửa tay (thay vùng R–AT)"),
    # ── ② CALCULATE · CA + SO ──
    Hop("CA.GL", (5, 5), ("BANK", "PLT"), "SỔ CÁI GL · QUY ĐỔI",
        ("ITL → khuôn GL (Templ 2)", "quy đổi theo tỷ giá tháng", "gắn chiều: CFA1 (LE)", "PLA1 · CFA3 · PLA3 (KRF)",
         "ngày → kỳ chuẩn"),
        "⛔", r(400, 406),
        vao=("IX.FX — tỷ giá tháng (9.2 Exchange Rate)",),
        fls="0 mã: grep ty_gia / exchange trong fls/ = 0 · 'Report I General Ledger' chỉ có trong 1 chú thích",
        cu="(mới — v0.9 không có tầng CALCULATE)"),
    Hop("SO.CFA1", (6, 6), ("BANK", "BANK"), "CF THEO LE", ("khối KRF × ngày", "+ Y · H · Q · M"),
        "⛔", ("409", "410"), fls="0 mã", cu="(mới)"),
    Hop("SO.PLA3", (6, 6), ("PAY", "HR"), "P&L THEO KRF · TRƯỚC PB",
        ("PLA1 PM-only · PLA3 HR", "CFA3 HR · PLA3 PM + HR", "ngày + Y·H·Q·M", "+ dòng GL chi tiết (412)", "HR đã phân bổ ở payroll (500)"),
        "⛔", ("407", "408") + r(411, 419), fls="0 mã: grep PLA1 / PLA3 trong fls/ = 0", cu="(mới)"),
    # ── ③ ALLOCATE ──
    Hop("AL.KEY", (7, 7), ("PAY", "PAY"), "PHÂN BỔ THEO KHOÁ", ("By LE · By NOEM · By GI", "bảng tỷ trọng"),
        "⛔", r(511, 513), vao=("IX.MB — tỷ trọng LE · NOEM · GI",),
        fls="fls/adapters/mapping_master.py biết từ vựng By GI (8) · By NOEM (5); phép chia: 0 mã", cu="(mới)"),
    Hop("AL.PLT", (7, 7), ("HR", "PLT"), "PHÂN BỔ NỀN TẢNG",
        ("Mapping Block 1: Vendor ↔ Network ↔ CDT1", "CFA2 MID 1–3 · ×7 CDT1", "Σ phần chia = tiền GD", "(Combine Code đã ghép ở SI.MAP)"),
        "⛔", ("500",) + r(501, 510), vao=("IX.MB — Mapping Block 1",),
        fls="0 mã (fls/ledger/allocate.py chỉ là cột AU = CFA1 của ITL Ledge, ⛔ phân bổ nền tảng)",
        cu="ghep3 · soat3 (+ hình 3)"),
    Hop("SO.PLA3-ATL", (8, 8), ("PAY", "PLT"), "P&L SAU PHÂN BỔ",
        ("theo CDT1 · LE", "ngày + Y·H·Q·M", "Allocation Table", "PM + HR + nền tảng", "(ATL = PD Now 606)"),
        "⛔", r(600, 604) + ("606",), fls="0 mã", cu="(mới)"),
    # ── ④ WAREHOUSE ──
    Hop("DW", (9, 9), ("BANK", "PLT"), "KHO FLS",
        ("PostgreSQL · chỉ-thêm", "ảnh · dòng · sổ · lớp sửa", "khối SO theo kỳ", "dây truy ngược:", "ô → dòng → giao dịch → ảnh",
         "thay IMPORTRANGE giữa", "~10 file Gsheet", "AS-IS: không có kho"),
        "◐ sổ có · khối SO ⛔", (),
        fls="fls_chup · fls_itl · fls_pm_link · fls_adjustment · fls_journal (fls/db/schema.py); bảng khối báo cáo: 0",
        cu="(mới — v0.9 vẽ sổ ở tầng ⑥ ⑦)"),
    # ── ⑤ REPORT ──
    Hop("RP.CF", (10, 10), ("BANK", "BANK"), "DAILY REPORT 2 · CF", ("Group · LE", "Templ 5"), "⛔", ("610",),
        fls="0 mã: grep 'Daily Report' trong fls/ = 0", cu="(mới)"),
    Hop("RP.PL", (10, 10), ("PAY", "PAY"), "DAILY REPORT 3 · P&L", ("Group · CDT1", "FS1 + FS2"), "⛔", ("605", "607", "608", "609"),
        vao=("[FS1] PLA5 Daily Report 3 đã sign-off (605)",), fls="0 mã", cu="(mới)"),
    Hop("RP.CCR", (11, 11), ("BANK", "PAY"), "BÁO CÁO DAILY TRONG CCR",
        ("5. Daily Report", "6. CCR ký tháng (pdf)", "ghi neo theo khoá", "chạy khô → cờ duyệt"),
        "◐ cơ chế ghi ✅ · bộ xuất ⛔", r(614, 616),
        vao=("khối Treasury (số dư nhập tay) ở chính file CCR", "IX.FX — tỷ giá in trên CCR (614)"),
        ra=("ThuongCT ký CCR mỗi tháng · email pdf + bản scan có chữ ký",),
        fls="fls/xuat/ghi_o.py — ghi ô an toàn, 27 bài · tools/ghi_o_that.py (FLS_CHO_GHI_SHEET=1)",
        cu="xuat", nguoi="owner duyệt cú ghi · ThuongCT ký tháng"),
    Hop("RP.FLS", (10, 11), ("HR", "PLT"), "MÀN FLS · TRUY NGƯỢC",
        ("F01 hàng chờ · F02 sổ · F03 cổng · F04 nạp lô", "bấm một ô báo cáo → dòng → giao dịch → ảnh",
         "thay [RAW ITL] Data Management", "+ nhật ký xử lý giao dịch"),
        "◐ 6 màn ✅ · truy ngược báo cáo ⛔", ("613", "617"),
        fls="fls/web/tep/man_f01*.js · man_f02.js · man_f03.js · man_f04.js — 37 tuyến API", cu="f01 · f02 · f03"),
    # ── KIỂM SOÁT — một cổng mỗi nhóm cột (Agent 4 · Auditor) ──
    Hop("KS.RI", (1, 2), ("KS", "KS"), "CỔNG INPUT", ("bản khai đủ · bề rộng cột", "Σ dòng ảnh = Σ dòng nguồn"), "◐",
        fls="fls/kiem/soat_nap.py (sao kê) · kiem_tieu_de_pm", cu="soat (một phần)"),
    Hop("KS.SI", (3, 4), ("KS", "KS"), "CỔNG GHÉP + SỔ", ("9 luật · Σ line = tiền · 4 vế", "số dư ngày = CCR (DIF = 0)"),
        "◐ 9 luật ✅ · DIF ⛔", (), fls="fls/kiem/soat_nap.py · chay_nap.py:611 cổng 4 vế",
        cu="soat · soat2 · kiem", nguoi="AS-IS: người soát DIF bằng mắt (phép so của 204 · 209)"),
    Hop("KS.CA", (5, 6), ("KS", "KS"), "CỔNG CALCULATE", ("Σ theo LE = Σ theo nguồn", "Σ ngày = Σ Y·H·Q·M"), "⛔",
        fls="0 mã", cu="kiem (h4)"),
    Hop("KS.AL", (7, 8), ("KS", "KS"), "CỔNG ALLOCATE", ("Σ phần chia = tiền GD", "Σ % CDT1 = 100"), "⛔",
        fls="0 mã", cu="soat3"),
    Hop("KS.RP", (9, 11), ("KS", "KS"), "CỔNG REPORT · PARITY", ("từng ô = ITL Ledge Final / Daily Report AS-IS", "chênh liệt kê từng ô, có tên"),
        "◐ parity ITL ✅ · báo cáo ⛔", fls="fls/oracle/cong_parity.py — RAW 64.393/64.393 · ADJUSTED 4.088/4.088 ô", cu="(mới)"),
    # ── INDEX · CONFIG ──
    Hop("IX.KHAI", (1, 2), ("IX", "IX"), "BẢN KHAI NGUỒN", ("cột · thứ tự ngày · LE TK", "có version, owner ký"), "✅ 408 dòng = 68 × 6",
        fls="fls/repo/khai_cot.py · fls_khai_cot", cu="khai", nguoi="kế toán khai · owner ký"),
    Hop("IX.MM", (3, 4), ("IX", "IX"), "MAPPING MASTER", ("sheet → LE · hd → cách phân bổ", "+ luật ghép đã ký"), "◐ bộ nạp có",
        ("301",), fls="fls/adapters/mapping_master.py — 73 mã hd, 0 trùng (đo 28/08)", cu="(trong ghep)"),
    Hop("IX.FX", (5, 6), ("IX", "IX"), "TỶ GIÁ · CHIỀU ASD", ("9.2 Exchange Rate theo tháng", "ASD · HD List · kỳ Day/Y/H/Q/M"), "⛔",
        fls="0 mã tỷ giá", cu="(mới)"),
    Hop("IX.MB", (7, 8), ("IX", "IX"), "MAPPING BLOCK · TỶ TRỌNG", ("Vendor ↔ Network-Acc ↔ CDT1", "By LE · NOEM · GI"), "⛔",
        fls="0 mã", cu="(mới)"),
    Hop("IX.TMP", (9, 11), ("IX", "IX"), "KHUÔN BÁO CÁO", ("Templ 1–5 (PD590) · Filters (PD510)", "kỳ (PD520) · KRF (PD530)"), "⛔",
        fls="0 mã", cu="(mới)"),
]
HOP_THEO = {h.ma: h for h in HOP}


@dataclass
class Ten:
    ma: str
    tu: str
    toi: str
    hang: str          # làn chạy
    cai_gi: str
    khoa: str
    pd: str = ""       # mũi tên / bước AS-IS tương ứng
    nhom: str = ""


TEN: list[Ten] = [
    Ten("e1", "RI.BANK", "PR.BANK", "BANK", "ảnh sao kê · quỹ · số dư CCR, đọc theo bản khai", "chup_id + khai_version", "115→200→201 · 116→202→203", "a"),
    Ten("e2", "RI.PAY", "PR.PAY", "PAY", "ảnh dòng sổ cái PM · PC (bỏ cột Email)", "pm_line_id · pc_line_id", "107→214 · 109→215 · 111→216 · 113→218", "a"),
    Ten("e3", "RI.HR", "PR.HR", "HR", "ảnh payroll tháng đã tách HD · CDT1 · LE + số FT", "(sổ, tháng, dòng)", "101→219…222", "a"),
    Ten("e4", "RI.PLT", "PR.PLT", "PLT", "ảnh 4 nguồn GI · OMC · SC · PS", "(loại, tháng, dòng)", "103→210 · 104→211 · 105→212 · 106→213", "a"),
    Ten("e5", "PR.BANK", "SI.MAP", "BANK", "dòng tiền canon hai vế + số dư ngày từng TK", "content_key", "207·208→302→307→308", "b"),
    Ten("e6", "PR.PAY", "SI.MAP", "PAY", "dòng lệnh: Ref No · tiền · tiền tệ · HD/KRF · CDT1 · LE trả · kỳ DV", "pm_line_id", "214…217→303…305→308", "b"),
    Ten("e7", "PR.HR", "SI.MAP", "HR", "dòng lương + Số CT (số FT kế toán dán)", "Số CT", "219…222→315…318 (VLOOKUP Số CT)", "b"),
    Ten("e8", "PR.PLT", "SI.MAP", "PLT", "chi phí theo loại · vendor · ngày + Combine Code — vào STANDARD INPUT như 3 họ kia", "(vendor, ngày, NoTrans)", "210…213→502→504 (AS-IS: ở ALLOCATE)", "b"),
    Ten("e9", "SI.MAP", "SI.ITL", "PAY", "mối nối (giao dịch ↔ PM line / dòng lương, tiền chia) + lớp L1 · L1b · L2 · L3", "(content_key, pm_line_id)", "308→314 · 315…318", "c"),
    Ten("e10", "SI.ITL", "CA.GL", "PAY", "sổ ITL hiệu lực: dòng + giá trị hiệu lực + 3 vai pháp nhân", "itl_id", "314→400 · 315…318→401…404", "c"),
    Ten("e11", "CA.GL", "SO.CFA1", "BANK", "dòng GL đã quy đổi, chiều CFA1 (theo LE)", "itl_id + kỳ", "400→409→410", "c"),
    Ten("e12", "CA.GL", "SO.PLA3", "PAY", "dòng GL đã quy đổi, chiều PLA1 · CFA3 · PLA3 (theo KRF)", "itl_id + kỳ", "406→412→414 · 407/408→413→416", "c"),
    Ten("e13", "SO.CFA1", "DW", "BANK", "khối CF: KRF × LE × kỳ — đi qua làn trống của ALLOCATE (CF không phân bổ)", "(KRF, LE, kỳ)", "409·410→610", "e"),
    Ten("e14", "SO.PLA3", "AL.KEY", "PAY", "P&L theo KRF trước phân bổ", "(KRF, CDT1, kỳ)", "412→511…513", "d"),
    Ten("e15", "SO.PLA3", "AL.PLT", "HR", "dòng GL mang PE nền tảng (đã nối bank qua Ref No)", "itl_id", "406→501→504", "d"),
    Ten("e16", "AL.KEY", "SO.PLA3-ATL", "PAY", "phần chia theo LE · NOEM · GI", "(KRF, khoá, kỳ)", "511…513→604", "d"),
    Ten("e17", "AL.PLT", "SO.PLA3-ATL", "PLT", "phần chia chi phí nền tảng theo CDT1 × tháng", "(content_key, CDT1)", "507→600 · 508…510→601…603", "d"),
    Ten("e18", "SO.PLA3-ATL", "DW", "PAY", "khối P&L sau phân bổ: KRF × CDT1 × kỳ", "(KRF, CDT1, kỳ)", "600…604→606", "e"),
    Ten("e19", "DW", "RP.CF", "BANK", "khối CF đã lưu", "(KRF, LE, kỳ)", "409·410→610", "f"),
    Ten("e20", "DW", "RP.PL", "PAY", "khối P&L sau phân bổ đã lưu", "(KRF, CDT1, kỳ)", "606→607→608→609", "f"),
    Ten("e21", "DW", "RP.FLS", "HR", "sổ hiệu lực + dây truy ngược", "itl_id · ô báo cáo", "308·314→613", "f"),
    Ten("e22", "RP.CF", "RP.CCR", "BANK", "Daily Report 2 (CF) vào báo cáo daily CCR", "(LE, ngày)", "610→615", "f"),
    Ten("e23", "RP.PL", "RP.CCR", "PAY", "Daily Report 3 (P&L) vào báo cáo daily CCR", "(CDT1, ngày)", "609→615", "f"),
]
NHOM_TEN = {  # 5 nhóm trên; INPUT chia 2 nhóm con
    "a": ("① INPUT", "RAW → PREPARE"), "b": ("① INPUT", "PREPARE → STANDARD INPUT"),
    "c": ("② CALCULATE", ""), "d": ("③ ALLOCATE", ""), "e": ("④ vào KHO", ""), "f": ("⑤ REPORT", ""),
}

# ── bước PD Now ⛔ vào hộp TO-BE nào — phải có LÝ DO (máy kiểm phủ đủ 112) ──
NGOAI = {
    "chưa làm ở AS-IS (Not yet) — owner chốt GĐ nào": ("100", "223", "224", "310", "311", "312"),
    "AS-IS đã huỷ (Cancel)": ("309",),
    "báo cáo HR từ EDD, ⛔ đi qua sổ tiền — ngoài GĐ1": ("102", "611", "612"),
    "OTHERS · báo cáo phụ (C12, BHXH, nghiệm thu dịch vụ)": ("700", "701", "702"),
}


# ═════════════════ MÁY KIỂM ═════════════════
def cat(x0, x1, y, h: Hop) -> bool:
    return h.x[0] < x1 and x0 < h.x[1] and h.y[0] < y < h.y[1]


def kiem() -> list[str]:
    loi: list[str] = []
    for h in HOP:
        m = MA_RE.match(h.ma)
        if not m:
            loi.append(f"{h.ma}: sai ngữ pháp tên")
            continue
        hang_buoc = HANG[h.hang[0]][3]
        mong = hang_buoc or COT[h.cot[0]][2]
        if hang_buoc is None and COT[h.cot[0]][2] != COT[h.cot[1]][2] and h.buoc != "RP":
            loi.append(f"{h.ma}: trải hai cột khác bước")
        if h.buoc != mong:
            loi.append(f"{h.ma}: tên nói bước {h.buoc} mà nằm ở cột/hàng bước {mong}")
    for i, a in enumerate(HOP):
        for b in HOP[i + 1:]:
            if a.x[0] < b.x[1] and b.x[0] < a.x[1] and a.y[0] < b.y[1] and b.y[0] < a.y[1]:
                loi.append(f"{a.ma} chồng {b.ma}")
    for c in COT:
        for nh in ("DỮ LIỆU",):
            n = sum(1 for h in HOP if h.cot[0] <= c <= h.cot[1] and HANG[h.hang[0]][0] == nh)
            if n > 5:
                loi.append(f"cột {c}: {n} hộp")
    if len({v[0] for v in COT.values()}) > 5 or sum(1 for v in HANG.values() if v[0] == "DỮ LIỆU") > 5:
        loi.append("quá 5 nhóm cột / hàng")
    for t in TEN:
        a, b = HOP_THEO[t.tu], HOP_THEO[t.toi]
        y = lan(t.hang)
        if not (a.y[0] < y < a.y[1] and b.y[0] < y < b.y[1]):
            loi.append(f"{t.ma}: làn {t.hang} ngoài hộp {a.ma}/{b.ma}")
        if not a.x[1] < b.x[0]:
            loi.append(f"{t.ma}: ⛔ đi trái → phải")
        for h in HOP:
            if h.ma not in (a.ma, b.ma) and cat(a.x[1], b.x[0], y, h):
                loi.append(f"{t.ma} cắt qua {h.ma}")
    tat = [s for h in HOP for s in h.pd] + [s for v in NGOAI.values() for s in v]
    pd = set(PDNOW["buoc"])
    if len(tat) != len(set(tat)):
        loi.append("PD Now: bước bị gán hai lần " + str(sorted({s for s in tat if tat.count(s) > 1})))
    if set(tat) - pd:
        loi.append(f"PD Now: bước lạ {sorted(set(tat) - pd)}")
    if pd - set(tat):
        loi.append(f"PD Now: thiếu {sorted(pd - set(tat))}")
    return loi


# ═════════════════ VẼ ═════════════════
MAU_NHOM = {"INPUT": "g-in", "CALCULATE": "g-ca", "ALLOCATE": "g-al", "WAREHOUSE": "g-dw", "REPORT": "g-rp"}


def lop_tt(tt: str) -> str:
    return "ok" if tt.startswith("✅") else ("mid" if tt.startswith("◐") else ("no" if tt.startswith("⛔") else "na"))


def svg() -> str:
    o = [f'<svg viewBox="0 0 {W_ALL} {H}" width="{W_ALL}" height="{H}" role="group" '
         f'aria-label="Voi FLS v2: NOW (AS-IS) bên trái tới ITL Adjust, TO-BE bên phải; hàng = họ dữ liệu, cột = bước; chip cùng mã là cùng một output">',
         '<defs><marker id="mui" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0 0L10 5L0 10z" class="mui"/></marker></defs>']
    o.append(ve_now())
    xg = cx(NCOT_NOW)[1] + KHE_NOW / 2
    o.append(f'<line class="tach" x1="{xg}" y1="4" x2="{xg}" y2="{H - 4}"/>')
    nhan: list[str] = []
    o.append(f'<g transform="translate({XN},0)">')
    # tầng 1 · AGENT (khung màu bao 4 hàng dữ liệu) — tầng 2 · bước — tầng 3 · cột con
    y0, y1 = HY["BANK"][0] - 8, HY["PLT"][0] + HY["PLT"][1] + 8
    for ag, c0, c1 in AGENT_DAI:
        x0, x1 = cx(c0)[0] - 8, cx(c1)[1] + 8
        d1, d2 = AGENT_NHAN[ag]
        o.append(f'<rect class="ag-dai ag-{ag}" x="{x0}" y="4" width="{x1 - x0}" height="36" rx="6"/>'
                 f'<text class="ag-t" x="{x0 + 10}" y="18">{E(d1)}</text><text class="ag-t2" x="{x0 + 10}" y="33">{E(d2)}</text>'
                 f'<rect class="ag-khung ag-{ag}" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="10"/>')
    # ⭐ owner 13/11: "đưa agent 4 về đúng chỗ bên phần to-be" — Agent 4 là một LÀN của TO-BE (dải + khung riêng
    #   quanh hàng KIỂM SOÁT), ⛔ nằm ở nhãn hàng chung (chỗ ấy đứng cạnh hộp NOW "soát bằng mắt").
    yk, hk = HY["KS"]
    x0, x1 = cx(1)[0] - 8, cx(11)[1] + 8
    o.append(f'<rect class="ag-dai ag-ag4" x="{x0}" y="{yk - 26}" width="{x1 - x0}" height="20" rx="5"/>'
             f'<text class="ag-t" x="{x0 + 10}" y="{yk - 12}">{E(AGENT_TEN["ag4"].upper())}</text>'
             f'<text class="ag-t2" x="{x1 - 10}" y="{yk - 12}" text-anchor="end">một cổng cho mỗi bước · mô hình khác họ với Agent 1–3</text>'
             f'<rect class="ag-khung ag-ag4" x="{x0}" y="{yk - 6}" width="{x1 - x0}" height="{hk + 12}" rx="10"/>')
    for g in NHOM_COT:
        cs = [c for c, v in COT.items() if v[0] == g]
        x0, x1 = cx(cs[0])[0] - 2, cx(cs[-1])[1] + 2
        o.append(f'<line class="buoc-l" x1="{x0}" y1="57" x2="{x1}" y2="57"/>'
                 f'<text class="buoc-t" x="{(x0 + x1) / 2}" y="53" text-anchor="middle">{E(g)}</text>')
    for c, (g, nh, b) in COT.items():
        x0, x1 = cx(c)
        o.append(f'<text class="cot-t" x="{(x0 + x1) / 2}" y="73" text-anchor="middle">{E(nh)}</text>'
                 f'<text class="cot-ma" x="{(x0 + x1) / 2}" y="88" text-anchor="middle">{b} · {E(BUOC[b][2])}</text>')
    # hàng
    for hm, (nh, t, phu, _b) in HANG.items():
        y, hh = HY[hm]
        nhan.append(f'<rect class="hang-n hang-{nh.split()[0].lower()}" x="16" y="{y}" width="{LX - 30}" height="{hh}" rx="6"/>'
                    f'<text class="hang-t" x="26" y="{y + hh / 2 - 3}">{E(t)}</text>'
                    f'<text class="hang-p" x="26" y="{y + hh / 2 + 12}">{E(phu)}</text>')
    # mũi tên trước, hộp sau
    for t in TEN:
        a, b = HOP_THEO[t.tu], HOP_THEO[t.toi]
        y = lan(t.hang)
        x1, x2 = a.x[1], b.x[0] - 1
        o.append(f'<g class="ten-g" data-id="t:{t.ma}" tabindex="0" role="button" aria-label="Mũi tên {t.ma}: {E(t.tu)} → {E(t.toi)}">'
                 f'<title>{E(t.ma + " · " + t.cai_gi)}</title>'
                 f'<line class="hit" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'
                 f'<line class="ten" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" marker-end="url(#mui)"/>'
                 f'<text class="ten-t" x="{(x1 + x2) / 2}" y="{y - 4}" text-anchor="middle">{t.ma}</text></g>')
    for h in HOP:
        x0, x1 = h.x
        y0, y1 = h.y
        lop = "ag-" + agent_cua(h)
        ra = RA_TOBE.get(h.ma, ())
        o.append(f'<g class="hop {lop}" data-id="h:{h.ma}" data-o="{" ".join(ra)}" tabindex="0" role="button" aria-label="{E(h.ma)} · {E(h.ten)}">'
                 f'<title>{E(h.ma + " · " + h.ten)}</title>'
                 f'<rect class="hop-k" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="6"/>'
                 f'<text class="hop-ma" x="{x0 + 8}" y="{y0 + 15}">{E(h.ma)}</text>')
        if h.ma == "AL.PLT":                       # A3.3 chỉ gợi ý phần dư: khoá Combine Code trúng 0 / ≥ 2 PE, vendor mới
            o.append(f'<rect class="chip3" x="{x1 - 92}" y="{y0 + 5}" width="40" height="13" rx="6.5"/>'
                     f'<text class="chip3-t" x="{x1 - 72}" y="{y0 + 15}" text-anchor="middle">A3.3</text>')
        if h.nguoi:
            o.append(f'<rect class="nguoi" x="{x1 - 46}" y="{y0 + 5}" width="40" height="13" rx="3"/>'
                     f'<text class="nguoi-t" x="{x1 - 26}" y="{y0 + 15}" text-anchor="middle">NGƯỜI</text>')
        rong = x1 - x0 - 14
        dong_ten = boc(h.ten, rong, 6.3)
        for i, d in enumerate(dong_ten):
            o.append(f'<text class="hop-ten" x="{x0 + 8}" y="{y0 + 30 + i * 13}">{E(d)}</text>')
        y_chip = y1 - (50 if h.pd else 37)                            # hàng chip output: trên dòng PD và dòng trạng thái
        y_cuoi = (y_chip - 4) if ra else (y1 - (21 if h.pd else 8) - 9)
        yy = y0 + 30 + len(dong_ten) * 13
        for d in h.hien[:2]:                         # owner 12/11: bỏ bớt chữ — đủ ở khung chi tiết
            for dd in boc(d, rong, 5.5):
                if yy > y_cuoi:
                    break
                o.append(f'<text class="hop-d" x="{x0 + 8}" y="{yy}">{E(dd)}</text>')
                yy += 12.5
        if h.pd:
            o.append(f'<text class="hop-pd" x="{x0 + 8}" y="{y1 - 20}">PD {E(cat_chu(pd_gon(h.pd), rong, 6))}</text>')
        o.append(f'<text class="hop-tt tt-{lop_tt(h.tt)}" x="{x0 + 8}" y="{y1 - 7}">{E(cat_chu(h.tt, rong, 6.1))}</text>')
        o.append(chip_ra(ra, x0 + 8, y_chip))
        o.append('</g>')
    o.append('</g>')
    o += nhan
    o.append('</svg>')
    return "\n".join(o)


def boc(chu: str, rong: float, px: float) -> list[str]:
    """Xuống dòng theo bề rộng hộp (ước lượng px / ký tự) — chữ ⛔ được tràn khỏi hộp."""
    n = max(8, int(rong / px))
    out, cur = [], ""
    for w in chu.split(" "):
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + ([cur] if cur else [])


def cat_chu(chu: str, rong: float, px: float) -> str:
    """Cắt chữ một dòng cho vừa hộp; bản đủ ở khung chi tiết và bảng §2."""
    n = int(rong / px)
    return chu if len(chu) <= n else chu[: n - 1].rstrip(" ·") + "…"


def pd_gon(ds: tuple[str, ...]) -> str:
    """'115 116 200 202' → '115–116 · 200 · 202' (dải liên tiếp gộp)."""
    so = sorted(int(s) for s in ds)
    out, a = [], so[0]
    for p, q in zip(so, so[1:] + [None]):
        if q != p + 1:
            out.append(f"{a}–{p}" if p != a else f"{a}")
            a = q
    return " · ".join(out)


def ten_buoc(s: str) -> str:
    b = PDNOW["buoc"][s]
    return (b["sheet"] or b["tep"] or b["nhom"] or "—")


# ═════════════════ BẢNG ═════════════════
NHOM_BANG = [  # (nhóm, [(nhóm con, [mã])]) — gom theo AGENT (owner 12/11), ≤ 5 mỗi tầng
    ("Agent 1 · Collect_raw_data", [("RAW · chụp nguồn", ["RI.BANK", "RI.PAY", "RI.HR", "RI.PLT"])]),
    ("Agent 2 · Generate Group Ledger (ITL raw)", [("PREPARE · dựng dòng chuẩn", ["PR.BANK", "PR.PAY", "PR.HR", "PR.PLT"]),
                                                    ("STANDARD INPUT · ghép (= file ITL 1/2 RAW)", ["SI.MAP"])]),
    ("Agent 3 · Filter Fulfill & Adjust (ITL Adjust)", [("STANDARD INPUT · sổ ITL (= file ITL 2/2 ADJUSTED)", ["SI.ITL"])]),
    ("Mã tất định · không agent", [("CALCULATE", ["CA.GL", "SO.CFA1", "SO.PLA3"]),
                                   ("ALLOCATE (A3.3 gợi ý phần dư của AL.PLT)", ["AL.KEY", "AL.PLT", "SO.PLA3-ATL"]),
                                   ("WAREHOUSE · REPORT", ["DW", "RP.CF", "RP.PL", "RP.CCR", "RP.FLS"])]),
    ("Xuyên suốt", [("Agent 4 · Auditor (Compounding Loop) — một cổng mỗi bước", ["KS.RI", "KS.SI", "KS.CA", "KS.AL", "KS.RP"]),
                    ("INDEX · CONFIG — người khai, owner ký", ["IX.KHAI", "IX.MM", "IX.FX", "IX.MB", "IX.TMP"])]),
]


def vao_ra():
    v = {h.ma: [] for h in HOP}
    ra = {h.ma: [] for h in HOP}
    for t in TEN:
        ra[t.tu].append(t)
        v[t.toi].append(t)
    return v, ra


def bang_io() -> str:
    v, ra = vao_ra()
    o = ['<div class="scroll"><table class="io"><thead><tr><th>mã · việc</th><th>vào</th><th>ra</th>'
         '<th>thay bước PD Now (AS-IS)</th><th>FLS hôm nay</th></tr></thead><tbody>']
    for nhom, con in NHOM_BANG:
        o.append(f'<tr class="b1"><th colspan="5">{E(nhom)}</th></tr>')
        for tc, mas in con:
            if tc:
                o.append(f'<tr class="b2"><th colspan="5">{E(tc)}</th></tr>')
            for m in mas:
                h = HOP_THEO[m]
                vao = [f'<li><b>{t.tu}</b> <span class="ma">{t.ma}</span> {E(t.cai_gi)}</li>' for t in v[m]]
                vao += [f'<li class="ngoai">{E(x)}</li>' for x in h.vao]
                ras = [f'<li>{E(t.cai_gi)} → <b>{t.toi}</b> <span class="ma">{t.ma}</span></li>' for t in ra[m]]
                ras += [f'<li class="ngoai">{E(x)}</li>' for x in h.ra]
                pd = "".join(f'<li><span class="ma">{s}</span> {E(ten_buoc(s))}</li>' for s in sorted(h.pd, key=int)) or '<li class="ngoai">— (AS-IS không có bước này)</li>'
                o.append(f'<tr class="chon" data-ref="h:{m}" tabindex="0"><td><b class="mono">{E(m)}</b><br>{E(h.ten)}'
                         f'<div class="cu">v0.9: {E(h.cu)}</div></td>'
                         f'<td><ul>{"".join(vao) or "<li>—</li>"}</ul></td><td><ul>{"".join(ras) or "<li>—</li>"}</ul></td>'
                         f'<td><ul class="pd">{pd}</ul></td>'
                         f'<td><span class="pill {lop_tt(h.tt)}">{E(h.tt)}</span><div class="fls">{E(h.fls)}</div></td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


def bang_ten() -> str:
    o = ['<div class="scroll"><table class="io"><thead><tr><th>#</th><th>từ → tới</th><th>làn</th><th>cái gì chảy</th>'
         '<th>khoá</th><th>AS-IS hôm nay (bước PD Now)</th></tr></thead><tbody>']
    cu = None
    for t in TEN:
        g, gc = NHOM_TEN[t.nhom]
        if g != cu:
            cu = g
            o.append(f'<tr class="b1"><th colspan="6">{E(g)}</th></tr>')
        if gc:
            if not o[-1].startswith('<tr class="b2"><th colspan="6">' + E(gc)):
                o.append(f'<tr class="b2"><th colspan="6">{E(gc)}</th></tr>')
        o.append(f'<tr class="chon" data-ref="t:{t.ma}" tabindex="0"><td class="mono">{t.ma}</td>'
                 f'<td class="mono">{E(t.tu)} → {E(t.toi)}</td><td>{t.hang}</td><td>{E(t.cai_gi)}</td>'
                 f'<td><code>{E(t.khoa)}</code></td><td class="mono">{E(t.pd)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


PHA = [("① INPUT · 1xx–2xx", lambda n: n < 300), ("② ITL · 3xx", lambda n: 300 <= n < 400),
       ("② CALCULATE · 4xx", lambda n: 400 <= n < 500), ("③ ALLOCATE · 5xx", lambda n: 500 <= n < 600),
       ("⑤ REPORT + OTHERS · 6xx–7xx", lambda n: n >= 600)]


def bang_phu() -> str:
    hop_cua = {s: h.ma for h in HOP for s in h.pd}
    ngoai_cua = {s: ly for ly, v in NGOAI.items() for s in v}
    o = ['<div class="scroll"><table class="io"><thead><tr><th>pha PD Now</th><th>số bước</th><th>vào hộp TO-BE</th>'
         '<th>ngoài GĐ1 · lý do</th></tr></thead><tbody>']
    tong = 0
    for ten, f in PHA:
        ss = sorted((s for s in PDNOW["buoc"] if f(int(s))), key=int)
        tong += len(ss)
        hops: dict[str, list[str]] = {}
        for s in ss:
            if s in hop_cua:
                hops.setdefault(hop_cua[s], []).append(s)
        ng: dict[str, list[str]] = {}
        for s in ss:
            if s in ngoai_cua:
                ng.setdefault(ngoai_cua[s], []).append(s)
        o.append(f'<tr><td><b>{E(ten)}</b></td><td class="mono">{len(ss)}</td>'
                 f'<td>{" · ".join(f"<b class=mono>{m}</b> {pd_gon(tuple(v))}" for m, v in hops.items())}</td>'
                 f'<td>{"<br>".join(f"{pd_gon(tuple(v))} — {E(ly)}" for ly, v in ng.items()) or "—"}</td></tr>')
    o.append(f'</tbody></table></div><p class="ghichu">Máy đếm lúc sinh: <b>{tong}/{len(PDNOW["buoc"])}</b> bước PD Now có chỗ — '
             f'<b>{len(hop_cua)}</b> vào một hộp TO-BE, <b>{len(ngoai_cua)}</b> ở rổ "ngoài GĐ1" có lý do; 0 bước gán hai lần.</p>')
    return "\n".join(o)


def bang_asis() -> str:
    # đo lại độ phủ của voi AS-IS (voi_asis_goc.json) trên PD Now — cùng phép đo đã chạy khi dựng trang
    a = json.loads(Path(__file__).with_name("voi_asis_goc.json").read_text(encoding="utf-8"))
    cov = set()
    for v in a["hop"].values():
        for m in re.finditer(r"(\d{3})(?:\s*[–-]\s*(\d{3}))?", v.get("buoc", "")):
            x, y = int(m.group(1)), int(m.group(2) or m.group(1))
            cov |= {str(s) for s in range(x, y + 1)}
    pd = PDNOW["buoc"]
    co = [s for s in pd if s in cov]
    thieu = sorted((s for s in pd if s not in cov), key=int)
    thieu_done = [s for s in thieu if pd[s]["tt"] == "Done"]
    thieu_khac = [s for s in thieu if pd[s]["tt"] != "Done"]
    rows = [
        ("Độ phủ", f"{len(co)}/{len(pd)} bước PD Now có trong một hộp AS-IS. Thiếu {len(thieu)}: {len(thieu_khac)} chưa làm / huỷ "
                   f"({pd_gon(tuple(thieu_khac))}) và <b>{len(thieu_done)} bước đang chạy</b> ({pd_gon(tuple(thieu_done))}) — toàn bộ chuỗi REPORT.",
         "vẽ đủ: RP.CF · RP.PL · RP.CCR · RP.FLS"),
        ("Đúng", "Tầng INPUT + ITL (101–319) khớp ma trận I/O: duỗi PE·PI·PM, gom bank / quỹ, chuyển A-CCR + sắp Ledger 111/112, "
                 "IMPORTRANGE, Transaction Original → Mapping L1, vùng chỉnh tay R–AT, H1000 Ledge.", "giữ, đổi tên theo ngữ pháp mới"),
        ("Nén", "CALCULATE 400–419 (20 bước) và ALLOCATE 500–513 (14 bước) gộp vào 3 hộp đầu ra (Report GL · Report H1000 · Phân bổ nền tảng): "
                "không thấy quy đổi tỷ giá (405 · 406), khối CFA1 / PLA1 / PLA3 theo ngày và Y/H/Q/M, chuỗi Mapping Block → CFA2 MID 1–3.",
         "tách: CA.GL · SO.CFA1 · SO.PLA3 · AL.KEY · AL.PLT · SO.PLA3-ATL"),
        ("Sai đầu vào", "Mũi tên o3 vẽ <i>sổ nền tảng → PHÂN BỔ</i>. PD Now 501 phân bổ đọc <b>[Import] Report General Ledger</b> (406) + Source (502) "
                        "+ Vendor &amp; Network Mapping (503) — thiếu đầu vào GL: chi phí nền tảng được chia từ dòng PE đã vào sổ, không chỉ từ file nguồn.",
         "e8 PR.PLT → SI.MAP (nền tảng vào SI) + e15 SO.PLA3 → AL.PLT"),
        ("Thiếu nút", "9.2 Exchange Rate (405 · 614); CCR là cả đầu vào (204 · 209) lẫn đầu ra (615 · 616) nhưng chỉ vẽ vào SOÁT. "
                      f"Ma trận PD Now tự nó có {len(PDNOW['treo'])} chỗ 'I' trỏ vào cột không bước nào sinh ra (vd 207 → [Importrange] 1.2 Ledger 112: 302 chỉ ghi 111).",
         "IX.FX · RP.CCR; câu hỏi ④ cuối trang"),
    ]
    o = ['<div class="scroll"><table class="io"><thead><tr><th>soát</th><th>voi AS-IS (artifact v0.9) so với PD Now</th><th>bản v2 xử lý ở</th></tr></thead><tbody>']
    for a1, b1, c1 in rows:
        o.append(f'<tr><td><b>{a1}</b></td><td>{b1}</td><td class="mono">{c1}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


def bang_ngu_phap() -> str:
    nhom = [("① INPUT", ["RI", "PR"]), ("② CALCULATE", ["SI", "CA", "SO"]), ("③ ALLOCATE", ["AL"]),
            ("④–⑤ KHO · BÁO CÁO", ["DW", "RP"]), ("Xuyên suốt", ["KS", "IX"])]
    o = ['<div class="scroll"><table class="io"><thead><tr><th>mã bước</th><th>bước</th><th>làm gì</th><th>PD Now</th><th>ví dụ</th></tr></thead><tbody>']
    for g, bs in nhom:
        o.append(f'<tr class="b1"><th colspan="5">{E(g)}</th></tr>')
        for b in bs:
            vd = " · ".join(h.ma for h in HOP if h.buoc == b)
            o.append(f'<tr><td class="mono"><b>{b}</b></td><td>{E(BUOC[b][0])}</td><td>{E(BUOC[b][1])}</td>'
                     f'<td class="mono">{E(BUOC[b][2])}</td><td class="mono">{E(vd)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


def du_lieu() -> str:
    v, ra = vao_ra()
    hop = {h.ma: {"ten": h.ten, "tt": h.tt, "hien": list(h.hien), "fls": h.fls, "cu": h.cu, "nguoi": h.nguoi,
                  "vao": [[t.ma, t.tu, t.cai_gi] for t in v[h.ma]] + [["", "", x] for x in h.vao],
                  "ra": [[t.ma, t.toi, t.cai_gi] for t in ra[h.ma]] + [["", "", x] for x in h.ra],
                  "pd": [[s, ten_buoc(s), PDNOW["buoc"][s]["tt"]] for s in sorted(h.pd, key=int)],
                  "buoc": f"{h.buoc} · {BUOC[h.buoc][0]}", "kb": AGENT_TEN[agent_cua(h)]} for h in HOP}
    ten = {t.ma: {"tu": t.tu, "toi": t.toi, "cai_gi": t.cai_gi, "khoa": t.khoa, "pd": t.pd} for t in TEN}
    return json.dumps({"hop": hop, "ten": ten}, ensure_ascii=False).replace("</", "<\\/")


# ═════════════════ NOW ↔ TO-BE · RAW → ITL ADJUST (owner 12/11) ═════════════════
# "Đặt 2 phần cạnh nhau, mapping 1-1 các OUTPUT giữa as-is và to-be, chỉ tới ITL adjust (sau đó là mã tất định).
#  Output của as-is và to-be phải giống nhau và phải thể hiện được trên voi. Audit ngược từ output cuối trở lại."
# ⇒ khoá ghép hai bên là OUTPUT (⛔ hộp): mỗi output có ĐÚNG MỘT hộp sinh ở NOW và ĐÚNG MỘT ở TO-BE.
#   Mã output = <bước>-<số> theo cùng ngữ pháp tên (RI-1 … SI-3) ⇒ đọc mã là biết output ra ở bước nào.
OUT = {  # mã: (tên ngắn, đọc từ — output phía trên, giống nhau ở hai bên vì output giống nhau)
    "RI-1": ("giao dịch sao kê thô", ()),
    "RI-2": ("giao dịch quỹ thô", ()),
    "RI-3": ("số dư ngày TK · quỹ", ()),
    "RI-4": ("PE·PI·PM·PC line đã duyệt", ()),
    "RI-5": ("payroll tháng + số FT", ()),
    "RI-6": ("GI·OMC·SC·PS theo vendor", ()),
    "PR-1": ("giao dịch bank theo ngày (Ledger 112)", ("RI-1",)),
    "PR-2": ("giao dịch quỹ theo ngày (Ledger 111)", ("RI-2",)),
    "PR-3": ("PM line đủ chiều (Unpivot)", ("RI-4",)),
    "PR-4": ("dòng lương theo HD·CDT1 (1.3 Ledger)", ("RI-5",)),
    "PR-5": ("Platform Data Ledger ×4", ("RI-6",)),
    "SI-1": ("giao dịch ↔ PM line (Mapping L1)", ("PR-1", "PR-2", "PR-3")),
    "SI-2": ("ITL Ledge Final", ("SI-1",)),
    "SI-3": ("H1000 Ledge Final", ("PR-4", "SI-2")),
    "SI-4": ("dòng nền tảng nối PE/PM (Combine Code)", ("PR-5", "SI-1")),
}
OUT_CUOI = ("SI-2", "SI-3", "SI-4")
# output mà nửa NOW ⛔ sinh được tới ITL Adjust — AS-IS làm ở chỗ khác; máy chấp nhận CHỈ khi có ghi chỗ ấy
OUT_NOW_NGOAI = {"SI-4": ("PD 504", "ALLOCATE · CFA1 | GI Platform Data Ledger — Combine Code ghép dòng ITL với nguồn; "
                                    "Gsheet không gộp được vào ITL (ITL AGGREGATE 319 đã huỷ)")}
OUT_RA_NGOAI = {"RI-3": "cổng soát số dư (KS.SI) — ⛔ vào ITL", }
BANG_CHUNG = {  # output: (trạng thái, bằng chứng hai bên giống nhau — số đo có nhãn)
    "SI-2": ("◐", "so từng ô với ITL Ledge Final đóng băng: vùng A–Q 64.393/64.393 ô · 22 kỳ; vùng chỉnh tay R–AT (7 khối) 4.088/4.088 ô · 584 dòng tháng 3/2026 — mới họ BANK"),
    "SI-3": ("⛔", "chưa so: 0 mã H1000 trong fls/"),
    "SI-4": ("⛔", "chưa so: 0 mã Combine Code trong fls/ + tools/; đáp án AS-IS ở cột A–Q của CFA1 | GI Platform Data Ledger (504)"),
    "SI-1": ("◐", "A–Q của ITL Ledge = IMPORTRANGE của Mapping L1 ⇒ cùng phép so 64.393 ô; máy ghép fls_pm_link 2.263 mối nối"),
    "PR-1": ("◐", "đọc 8.338/8.338 dòng bank; so từng dòng với Ledger 112: qua parity A–Q"),
    "PR-2": ("⛔", "lằn Cash chưa chạy"),
    "PR-3": ("◐", "28 cột PM: 14 có kiểu · 1 cấm · 13 thô; PC: 0 tham chiếu"),
    "PR-4": ("⛔", "0 mã"),
    "PR-5": ("⛔", "0 mã (đi ALLOCATE)"),
    "RI-1": ("✅", "60 nguồn · 182 ảnh, đọc theo bản khai (408 dòng = 68 × 6)"),
    "RI-2": ("⛔", "0 ảnh lằn Cash"),
    "RI-3": ("⛔", "chỉ đo (tools/do_trong_tai.py), ⛔ chụp"),
    "RI-4": ("◐", "PM 3.772 dòng (fls_pm_line) · PC chưa đọc"),
    "RI-5": ("⛔", "0 mã"),
    "RI-6": ("⛔", "0 mã"),
}


@dataclass
class HopN:                 # hộp NOW (AS-IS hôm nay) — gộp các hộp gốc của voi AS-IS
    ma: str
    cot: int                # 1–4 trong nửa NOW (cùng bề rộng cột hình 1)
    hang: tuple[str, str]
    ten: str
    ra: tuple[str, ...]     # output sinh ra
    goc: tuple[str, ...]    # mã hộp gốc trong voi_asis_goc.json
    pd: str
    tay: bool = False
    cot1: int = 0           # cột cuối nếu hộp trải nhiều cột


HOP_NOW: list[HopN] = [
    HopN("N1", 1, ("BANK", "BANK"), "sheet R | · 2. CCR", ("RI-1", "RI-2", "RI-3"), ("dSK", "dSQ", "dCCR", "oNH", "oKQ", "oSD"), "115–116 · 200 · 202 · 204 · 209", True),
    HopN("N2", 1, ("PAY", "PAY"), "Entry Data PE·PI·PM·PC", ("RI-4",), ("dEntry", "oDN", "oCA"), "107–114", True),
    HopN("N3", 1, ("HR", "HR"), "file lương tháng", ("RI-5",), ("dPR", "dEDD", "oHR", "oKTL"), "101", True),
    HopN("N4", 1, ("PLT", "PLT"), "Looker · 2 Gsheet", ("RI-6",), ("dLK", "oDT"), "103–106", True),
    HopN("N5", 2, ("BANK", "BANK"), "GScript gom → Ledger 112 · 111", ("PR-1", "PR-2"), ("pGB", "dBT", "pGQ", "dCT", "pCH", "dLED", "oKTG", "oKTC"), "201 · 203 · 205–208", True),
    HopN("N6", 2, ("PAY", "PAY"), "GScript duỗi → Unpivot", ("PR-3",), ("pDUOI", "dUNP", "oKTS"), "214–218", True),
    HopN("N7", 2, ("HR", "HR"), "tách lương → 1.3 Ledger", ("PR-4",), ("pTACH", "dL13", "pG12", "dH1000", "oKT12"), "219–222", True),
    HopN("N8", 2, ("PLT", "PLT"), "gom → Platform Ledger", ("PR-5",), ("pGN", "dPL"), "210–213"),
    HopN("N9", 3, ("BANK", "PAY"), "ITL 1/2 RAW · VLOOKUP Ref", ("SI-1",), ("dIU", "dIL", "pGOP", "dTO", "pGHEP", "dML1"), "302–308"),
    HopN("N10", 4, ("BANK", "PAY"), "ITL 2/2 ADJUSTED · chỉnh tay R–AT", ("SI-2",), ("dITLi", "pADJ", "dITLF", "oKTA"), "313–314 · 319 huỷ", True),
    HopN("N11", 4, ("HR", "HR"), "H1000 Ledge · VLOOKUP Số CT", ("SI-3",), ("dH1i", "dH1F"), "315–318"),
    # hàng xuyên suốt của NOW — cùng hàng với KS · IX của TO-BE, ⛔ mang output (ngoài phép so 1-1)
    HopN("N12", 1, ("KS", "KS"), "soát số dư bằng mắt: Ledger 111/112 ↔ 2. CCR (DIF)", (), ("pSOAT",), "204 · 209", True, 4),
    HopN("N13", 3, ("IX", "IX"), "Mapping Master (sheet → LE · hd)", (), ("dMM",), "301"),
]
HOP_NOW_THEO = {h.ma: h for h in HOP_NOW}
NGOAI_NOW = {  # hộp gốc AS-IS ⛔ vào nửa NOW — có lý do
    "pTH": "báo cáo HR từ EDD — ngoài GĐ1", "dHRR": "báo cáo HR từ EDD — ngoài GĐ1",
    "oRPT": "sau ITL — mã tất định", "oRH": "sau ITL — mã tất định", "oALL": "sau ITL — mã tất định",
}
RA_TOBE = {"RI.BANK": ("RI-1", "RI-2", "RI-3"), "RI.PAY": ("RI-4",), "RI.HR": ("RI-5",), "RI.PLT": ("RI-6",),
           "PR.BANK": ("PR-1", "PR-2"), "PR.PAY": ("PR-3",), "PR.HR": ("PR-4",), "PR.PLT": ("PR-5",),
           "SI.MAP": ("SI-1",), "SI.ITL": ("SI-2", "SI-3", "SI-4")}
TEN_NOW = [  # (mã, từ, tới, làn | "doc") — dọc chỉ trong một cột
    ("n1", "N1", "N5", "BANK"), ("n2", "N2", "N6", "PAY"), ("n3", "N3", "N7", "HR"), ("n4", "N4", "N8", "PLT"),
    ("n5", "N5", "N9", "BANK"), ("n6", "N6", "N9", "PAY"), ("n7", "N9", "N10", "PAY"), ("n8", "N7", "N11", "HR"),
    ("n9", "N10", "N11", "doc"),
]
TEN2_TOBE = {"RI.BANK": "Ảnh sao kê · quỹ · CCR", "RI.PAY": "Ảnh sổ cái PM · PC", "RI.HR": "Ảnh sổ H1000",
             "RI.PLT": "Ảnh 4 nguồn nền tảng", "PR.BANK": "Dòng tiền + số dư ngày", "PR.PAY": "Dòng lệnh PM · PC",
             "PR.HR": "Dòng lương + Số CT", "PR.PLT": "Chi phí 4 loại", "SI.MAP": "Ghép Ref No · Số CT · Combine Code",
             "SI.ITL": "Sổ ITL hiệu lực · đủ 4 họ"}
TEN_TOBE2 = [t for t in TEN if t.tu in RA_TOBE and t.toi in RA_TOBE]

# ⭐ Owner 13/11: "đưa sơ đồ 1 và sơ đồ 2 về cùng 1 sơ đồ và đặt cạnh nhau" ⇒ NOW là nửa TRÁI của hình 1,
#   cùng lưới hàng (HY) và cùng bề rộng cột (CW · GAP); TO-BE dịch phải XN. Chip output nằm thẳng trên hộp TO-BE.
NCOT_NOW, KHE_NOW = 4, 56
XN = NCOT_NOW * (CW + GAP) - GAP + KHE_NOW
W_ALL = W + XN
NOW_COT = {1: ("sheet nguồn", "RAW", "PD 1xx"), 2: ("P100 · A-CCR · H1000", "PREPARE", "PD 2xx"),
           3: ("file ITL 1/2 RAW", "ITL RAW · ghép", "PD 30x"), 4: ("file ITL 2/2 ADJUSTED", "ITL ADJUST", "PD 31x")}


def x_now(h):
    return cx(h.cot)[0], cx(h.cot1 or h.cot)[1]


def y_now(h):
    a, b = h.hang
    return HY[a][0], HY[b][0] + HY[b][1]


def chip_ra(ra, x, y) -> str:
    o = []
    for oo in ra:
        o.append(f'<g class="chip" data-o="{oo}"><rect class="chip-k chip-{oo[:2].lower()}{" chip-cuoi" if oo in OUT_CUOI else ""}" '
                 f'x="{x}" y="{y}" width="38" height="15" rx="7.5"/><text class="chip-t" x="{x + 19}" y="{y + 11}" text-anchor="middle">{oo}</text></g>')
        x += 42
    return "".join(o)


def kiem_now() -> list[str]:
    loi: list[str] = []
    # ① 1-1 theo output
    for ben, ds in (("NOW", [(h.ma, h.ra) for h in HOP_NOW] + [("ngoài", tuple(OUT_NOW_NGOAI))]), ("TO-BE", list(RA_TOBE.items()))):
        tat = [o for _m, ra in ds for o in ra]
        if sorted(tat) != sorted(OUT):
            loi.append(f"{ben}: output ≠ bộ chung — thiếu {sorted(set(OUT) - set(tat))} · thừa / trùng {sorted(o for o in set(tat) if tat.count(o) != 1 or o not in OUT)}")
    for o in OUT:
        if not o.split("-")[0] in ("RI", "PR", "SI"):
            loi.append(f"{o}: sai ngữ pháp")
    for ma, ra in RA_TOBE.items():                    # output TO-BE ra đúng bước của hộp sinh nó
        loi += [f"{o}: ra ở hộp {ma} khác bước" for o in ra if o.split("-")[0] != HOP_THEO[ma].buoc]
    # ② 52 hộp AS-IS gốc đều có chỗ
    goc = [g for h in HOP_NOW for g in h.goc] + list(NGOAI_NOW)
    tat = set(json.loads(Path(__file__).with_name("voi_asis_goc.json").read_text(encoding="utf-8"))["hop"])
    if sorted(goc) != sorted(tat):
        loi.append(f"AS-IS gốc: thiếu {sorted(tat - set(goc))} · lạ / trùng {sorted(g for g in set(goc) if goc.count(g) != 1 or g not in tat)}")
    # ③ mũi tên NOW thẳng, ⛔ cắt hộp NOW (mũi tên TO-BE do kiem() canh)
    hs = {h.ma: (x_now(h), y_now(h)) for h in HOP_NOW}
    for i, a in enumerate(HOP_NOW):
        for b in HOP_NOW[i + 1:]:
            (ax, ay), (bx, by) = hs[a.ma], hs[b.ma]
            if ax[0] < bx[1] and bx[0] < ax[1] and ay[0] < by[1] and by[0] < ay[1]:
                loi.append(f"NOW: {a.ma} chồng {b.ma}")
    for ma, tu, toi, lan_ in TEN_NOW:
        (ax, ay), (bx, by) = hs[tu], hs[toi]
        if lan_ == "doc":
            xm = (max(ax[0], bx[0]) + min(ax[1], bx[1])) / 2
            if not (ax[0] < xm < ax[1] and bx[0] < xm < bx[1] and ay[1] <= by[0]):
                loi.append(f"{ma}: dọc mà ⛔ cùng cột / ⛔ đi xuống")
            continue
        y = lan(lan_)
        if not (ay[0] < y < ay[1] and by[0] < y < by[1] and ax[1] < bx[0]):
            loi.append(f"{ma}: làn {lan_} sai")
        for m2, (x2, y2) in hs.items():
            if m2 not in (tu, toi) and x2[0] < bx[0] and ax[1] < x2[1] and y2[0] < y < y2[1]:
                loi.append(f"{ma} cắt qua {m2}")
    # ④ mỗi quan hệ "đọc từ" có đường mũi tên ở CẢ HAI voi ⇒ output giống nhau thì đường đi cũng hiện trên voi
    for ben, sinh, canh in (("NOW", {o: h.ma for h in HOP_NOW for o in h.ra}, [(t[1], t[2]) for t in TEN_NOW]),
                            ("TO-BE", {o: m for m, ra in RA_TOBE.items() for o in ra}, [(t.tu, t.toi) for t in TEN_TOBE2])):
        for o, (_t, tu_ds) in OUT.items():
            if ben == "NOW" and o in OUT_NOW_NGOAI:      # AS-IS sinh ở ngoài nửa NOW — đã ghi chỗ, ⛔ đòi đường
                continue
            for i in tu_ds:
                if i not in sinh or o not in sinh:          # thiếu hộp sinh ⇒ luật ① đã báo ĐỎ; ⛔ nổ ở đây
                    loi.append(f"{ben}: ⛔ đo được đường {i} → {o} (thiếu hộp sinh)")
                    continue
                a, b = sinh[i], sinh[o]
                if a != b and not co_duong(a, b, canh):
                    loi.append(f"{ben}: {o} đọc từ {i} mà ⛔ có đường {a} → {b}")
    return loi


def co_duong(a, b, canh) -> bool:
    di, thay = [a], {a}
    while di:
        x = di.pop()
        for u, v in canh:
            if u == x and v not in thay:
                if v == b:
                    return True
                thay.add(v)
                di.append(v)
    return False


def ve_now() -> str:
    """Nửa TRÁI của hình 1: NOW (AS-IS hôm nay) tới ITL Adjust, cùng hàng với TO-BE; chip = output."""
    o = []
    x0, x1 = cx(1)[0] - 8, cx(NCOT_NOW)[1] + 8
    y0, y1 = HY["BANK"][0] - 8, HY["PLT"][0] + HY["PLT"][1] + 8
    o.append(f'<rect class="ben ben-now" x="{x0}" y="4" width="{x1 - x0}" height="36" rx="6"/>'
             f'<text class="ag-t" x="{x0 + 10}" y="18">NOW · AS-IS GOOGLE SHEETS HÔM NAY</text>'
             f'<text class="ag-t2" x="{x0 + 10}" y="33">tới ITL Adjust — phần sau là mã tất định, giữ nguyên</text>'
             f'<rect class="ben-k ben-now" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="10"/>')
    for c, (tep, nh, pd) in NOW_COT.items():
        a, b = cx(c)
        o.append(f'<line class="buoc-l" x1="{a}" y1="57" x2="{b}" y2="57"/><text class="buoc-t" x="{(a + b) / 2}" y="53" text-anchor="middle">{E(tep)}</text>'
                 f'<text class="cot-t" x="{(a + b) / 2}" y="73" text-anchor="middle">{E(nh)}</text>'
                 f'<text class="cot-ma" x="{(a + b) / 2}" y="88" text-anchor="middle">{E(pd)}</text>')
    hs = {h.ma: (x_now(h), y_now(h)) for h in HOP_NOW}
    for ma, tu, toi, lan_ in TEN_NOW:
        (ax, ay), (bx, by) = hs[tu], hs[toi]
        if lan_ == "doc":
            xm = (max(ax[0], bx[0]) + min(ax[1], bx[1])) / 2
            o.append(f'<g class="ten-g"><title>{ma} · VLOOKUP Số CT → ITL ID</title><line class="ten" x1="{xm}" y1="{ay[1]}" x2="{xm}" y2="{by[0] - 1}" marker-end="url(#mui)"/>'
                     f'<text class="ten-t" x="{xm + 4}" y="{(ay[1] + by[0]) / 2 + 3}">{ma}</text></g>')
            continue
        y = lan(lan_)
        o.append(f'<g class="ten-g"><line class="ten" x1="{ax[1]}" y1="{y}" x2="{bx[0] - 1}" y2="{y}" marker-end="url(#mui)"/>'
                 f'<text class="ten-t" x="{(ax[1] + bx[0]) / 2}" y="{y - 4}" text-anchor="middle">{ma}</text></g>')
    a, b = cx(3)
    o.append(f'<text class="ra-ngoai" x="{a}" y="{lan("PLT") + 4}">→ ALLOCATE (mã tất định)</text>')
    for h in HOP_NOW:
        (a, b), (c, d) = hs[h.ma]
        o.append(f'<g class="hop2 now" data-o="{" ".join(h.ra)}" tabindex="0" role="button" aria-label="NOW {E(h.ten)}{" · ra " + " ".join(h.ra) if h.ra else ""}">'
                 f'<title>{E(h.ten)} · PD {E(h.pd)}{" — ra: " + E(" · ".join(x + " " + OUT[x][0] for x in h.ra)) if h.ra else ""}</title>'
                 f'<rect class="hop-k" x="{a}" y="{c}" width="{b - a}" height="{d - c}" rx="6"/>'
                 f'<text class="hop-ma" x="{a + 8}" y="{c + 15}">{E(cat_chu("PD " + h.pd, b - a - (62 if h.tay else 16), 6.2))}</text>')
        if h.tay:
            o.append(f'<rect class="nguoi" x="{b - 46}" y="{c + 5}" width="40" height="13" rx="3"/><text class="nguoi-t" x="{b - 26}" y="{c + 15}" text-anchor="middle">TAY</text>')
        for i, t in enumerate(boc(h.ten, b - a - 16, 6.3)[:2]):
            o.append(f'<text class="hop-ten" x="{a + 8}" y="{c + 31 + i * 13}">{E(t)}</text>')
        o.append(chip_ra(h.ra, a + 8, d - 22))
        o.append('</g>')
    return "\n".join(o)


def bang_audit() -> str:
    sinh_now = {o: h for h in HOP_NOW for o in h.ra}
    sinh_tb = {o: m for m, ra in RA_TOBE.items() for o in ra}
    dung = {o: [p for p, (_t, tu) in OUT.items() if o in tu] for o in OUT}
    nhom = [("① OUTPUT CUỐI · ITL ADJUST", [("", ["SI-2", "SI-3", "SI-4"])]),
            ("② ITL RAW · ghép", [("", ["SI-1"])]),
            ("③ PREPARE", [("", ["PR-1", "PR-2", "PR-3", "PR-4", "PR-5"])]),
            ("④ RAW", [("tiền", ["RI-1", "RI-2", "RI-3"]), ("lệnh chi · lương · nền tảng", ["RI-4", "RI-5", "RI-6"])])]
    o = ['<div class="scroll"><table class="io"><thead><tr><th>output</th><th>đọc từ ← · dùng bởi →</th><th>NOW sinh ở</th><th>TO-BE sinh ở</th>'
         '<th>bằng chứng hai bên giống nhau</th></tr></thead><tbody>']
    for g, con in nhom:
        o.append(f'<tr class="b1"><th colspan="5">{E(g)}</th></tr>')
        for tc, ds in con:
            if tc:
                o.append(f'<tr class="b2"><th colspan="5">{E(tc)}</th></tr>')
            for oo in ds:
                tt, bc = BANG_CHUNG[oo]
                n = sinh_now.get(oo)
                tu = " · ".join(OUT[oo][1]) or "nguồn ngoài"
                ra = " · ".join(dung[oo]) or OUT_RA_NGOAI.get(oo, "mã tất định (CALCULATE)")
                o.append(f'<tr class="chon2" data-o="{oo}" tabindex="0"><td><span class="chip-h chip-{oo[:2].lower()}">{oo}</span> {E(OUT[oo][0])}'
                         f'{" <b>· output cuối</b>" if oo in OUT_CUOI else ""}</td>'
                         f'<td class="mono">← {E(tu)}<br>→ {E(ra)}</td>'
                         + (f'<td><b class="mono">{n.ma}</b> {E(n.ten)}<div class="fls">PD {E(n.pd)}</div></td>' if n else
                            f'<td><b class="mono">{OUT_NOW_NGOAI[oo][0]}</b> {E(OUT_NOW_NGOAI[oo][1])}</td>')
                         + f'<td><b class="mono">{E(sinh_tb[oo])}</b> {E(TEN2_TOBE[sinh_tb[oo]])}</td>'
                         f'<td><span class="pill {lop_tt(tt)}">{tt}</span> {E(bc)}</td></tr>')
    o.append('</tbody></table></div>')
    return "\n".join(o)


def tom_tat_now() -> str:
    dem = {k: sum(1 for v in BANG_CHUNG.values() if v[0] == k) for k in ("✅", "◐", "⛔")}
    cuoi = " · ".join(f"{o} {OUT[o][0]} {BANG_CHUNG[o][0]}" for o in OUT_CUOI)
    return (f'<p class="note">Máy kiểm lúc sinh: <b>{len(OUT)} output</b>, mỗi output có đúng 1 hộp sinh ở NOW và đúng 1 ở TO-BE; '
            f'{len(HOP_NOW)} hộp NOW gộp đủ {sum(len(h.goc) for h in HOP_NOW)} hộp gốc của voi AS-IS ({len(NGOAI_NOW)} hộp còn lại có lý do: cấu hình, cổng, sau ITL); '
            f'mọi quan hệ "đọc từ" đều có đường mũi tên trên CẢ HAI voi. Output cuối: {E(cuoi)}. '
            f'Đã chứng minh giống nhau: ✅ {dem["✅"]} · ◐ {dem["◐"]} · ⛔ {dem["⛔"]} trên {len(OUT)}.</p>')


CSS = r"""
/* Lưới FPA: hàng = phần dữ liệu, cột = bước. Hình rộng cuộn trong khung; khung chi tiết neo phải (điện thoại: đáy). */
:root{
  --bg:#f5f6f4; --paper:#fff; --fg:#1b2420; --muted:#5a655f; --line:#d4dad5;
  --in:#2f5d8a; --in-s:#e6eef6; --ca:#b3362b; --ca-s:#fbeceb; --al:#7a4bb0; --al-s:#f1ebf8;
  --dw:#2f7a5b; --dw-s:#e5f2ec; --rp:#9a6a10; --rp-s:#f7f0e1; --ks:#6b2f2f; --ks-s:#f4e8e8; --ix:#3d4a55; --ix-s:#eceff2;
  --ok:#1f7a45; --ok-s:#e3f3e9; --mid:#9a6a10; --mid-s:#fbf1dc; --no:#b3362b; --no-s:#fbe7e5; --sel:#e0a100;
  --a1:#2f5d8a; --a1-s:#e6eef6; --a2:#1f7a6a; --a2-s:#e2f2ee; --a3:#7a4bb0; --a3-s:#f1ebf8; --a4:#a3332a; --a4-s:#fbecea;
  --sans:"IBM Plex Sans",system-ui,sans-serif; --mono:"IBM Plex Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#141a17; --paper:#1b2320; --fg:#e5ebe7; --muted:#9aa69f; --line:#34403a;
  --in:#8db8e3; --in-s:#1d2a37; --ca:#f08a80; --ca-s:#341f1d; --al:#c3a2ea; --al-s:#2a2236; --dw:#7fd0ab; --dw-s:#1a2e25;
  --rp:#e2bd6c; --rp-s:#30281a; --ks:#e6a3a3; --ks-s:#2f2020; --ix:#b5c2cc; --ix-s:#232a30;
  --a1:#8db8e3; --a1-s:#1d2a37; --a2:#7fd0c0; --a2-s:#17302b; --a3:#c3a2ea; --a3-s:#2a2236; --a4:#f08a80; --a4-s:#341f1d;
  --ok:#7fd0a0; --ok-s:#1a2e22; --mid:#e2bd6c; --mid-s:#30281a; --no:#f08a80; --no-s:#341f1d; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#141a17; --paper:#1b2320; --fg:#e5ebe7; --muted:#9aa69f; --line:#34403a;
  --in:#8db8e3; --in-s:#1d2a37; --ca:#f08a80; --ca-s:#341f1d; --al:#c3a2ea; --al-s:#2a2236; --dw:#7fd0ab; --dw-s:#1a2e25;
  --rp:#e2bd6c; --rp-s:#30281a; --ks:#e6a3a3; --ks-s:#2f2020; --ix:#b5c2cc; --ix-s:#232a30;
  --a1:#8db8e3; --a1-s:#1d2a37; --a2:#7fd0c0; --a2-s:#17302b; --a3:#c3a2ea; --a3-s:#2a2236; --a4:#f08a80; --a4-s:#341f1d;
  --ok:#7fd0a0; --ok-s:#1a2e22; --mid:#e2bd6c; --mid-s:#30281a; --no:#f08a80; --no-s:#341f1d; color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:14px/1.55 var(--sans)}
main{padding-block:20px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));max-width:1500px;margin:0 auto}
h1{font:600 26px/1.2 var(--sans);margin:0 0 6px;text-wrap:balance}
h2{font:600 19px/1.3 var(--sans);margin:34px 0 8px;text-wrap:balance}
p{max-width:80ch}
.meta,.ghichu{color:var(--muted);font-size:13px}
.nhap{display:inline-block;font:600 11px var(--mono);letter-spacing:.06em;background:var(--no-s);color:var(--no);border:1px solid var(--no);border-radius:4px;padding:1px 6px;margin-right:6px}
.mono,code{font-family:var(--mono);font-size:12px}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
figure{margin:12px 0}
figure .scroll{padding:6px}
figcaption{color:var(--muted);font-size:13px;margin-top:8px;max-width:110ch}
svg text{font-family:var(--sans);fill:var(--fg)}
.ag-dai{stroke:none}.ag-t{font:700 11.5px var(--mono);letter-spacing:.06em;fill:var(--paper)}.ag-t2{font:500 10.5px var(--sans);fill:var(--paper)}
.ag-dai.ag-ag1{fill:var(--a1)}.ag-dai.ag-ag2{fill:var(--a2)}.ag-dai.ag-ag3{fill:var(--a3)}.ag-dai.ag-ag4{fill:var(--a4)}.ag-khung.ag-ag4{stroke:var(--a4)}.ag-dai.ag-ma{fill:var(--muted)}
.ag-khung{fill:none;stroke-width:2}.ag-khung.ag-ag1{stroke:var(--a1)}.ag-khung.ag-ag2{stroke:var(--a2)}.ag-khung.ag-ag3{stroke:var(--a3)}
.ag-khung.ag-ma{stroke:var(--muted);stroke-dasharray:6 4}
.buoc-l{stroke:var(--line);stroke-width:1.5}.buoc-t{font:600 10.5px var(--mono);letter-spacing:.12em;fill:var(--muted)}
.hop.ag-ag1 .hop-k{stroke:var(--a1);fill:var(--a1-s)}.hop.ag-ag2 .hop-k{stroke:var(--a2);fill:var(--a2-s)}.hop.ag-ag3 .hop-k{stroke:var(--a3);fill:var(--a3-s)}
.hop.ag-ma .hop-k{stroke:var(--muted);fill:var(--paper)}.hop.ag-ag4 .hop-k{stroke:var(--a4);fill:var(--a4-s)}.hop.ag-ix .hop-k{stroke:var(--ix);fill:var(--ix-s);stroke-dasharray:4 3}
.hop.ag-ag1 .hop-ma{fill:var(--a1)}.hop.ag-ag2 .hop-ma{fill:var(--a2)}.hop.ag-ag3 .hop-ma{fill:var(--a3)}.hop.ag-ma .hop-ma{fill:var(--fg)}
.hop.ag-ag4 .hop-ma{fill:var(--a4)}.hop.ag-ix .hop-ma{fill:var(--ix)}
.chip3{fill:var(--a3-s);stroke:var(--a3)}.chip3-t{font:700 8.5px var(--mono);fill:var(--a3)}
.hang-kiểm{fill:var(--a4-s)!important}.hang-kiểm+text{fill:var(--a4)}
.nhom{stroke:none}.nhom-t{font:600 12px var(--mono);letter-spacing:.08em;fill:var(--paper)}
.nhom.g-in{fill:var(--in)}.nhom.g-ca{fill:var(--ca)}.nhom.g-al{fill:var(--al)}.nhom.g-dw{fill:var(--dw)}.nhom.g-rp{fill:var(--rp)}
.khung{fill:none;stroke-width:2}
.khung.g-in{stroke:var(--in)}.khung.g-ca{stroke:var(--ca)}.khung.g-al{stroke:var(--al)}.khung.g-dw{stroke:var(--dw)}.khung.g-rp{stroke:var(--rp)}
.cot-t{font:600 11px var(--sans);fill:var(--fg)}.cot-ma{font:500 10.5px var(--mono);fill:var(--muted)}.cot-ag{font:italic 10px var(--sans);fill:var(--muted)}
.hang-n{fill:var(--paper);stroke:var(--line)}.hang-kiểm{fill:var(--ks-s)}.hang-config{fill:var(--ix-s)}
.hang-t{font:700 12.5px var(--mono);letter-spacing:.04em}.hang-p{font:11px var(--sans);fill:var(--muted)}
.hang-nhom{font:700 11px var(--mono);letter-spacing:.12em;fill:var(--muted)}
.plan{fill:none;stroke:var(--muted);stroke-dasharray:5 4}.plan-t{font:italic 12px var(--sans);fill:var(--muted)}
.hop{cursor:pointer}
.hop-k{fill:var(--paper);stroke-width:1.6}
.hop.g-in .hop-k{stroke:var(--in);fill:var(--in-s)}.hop.g-ca .hop-k{stroke:var(--ca);fill:var(--ca-s)}
.hop.g-al .hop-k{stroke:var(--al);fill:var(--al-s)}.hop.g-dw .hop-k{stroke:var(--dw);fill:var(--dw-s)}
.hop.g-rp .hop-k{stroke:var(--rp);fill:var(--rp-s)}.hop.g-ks .hop-k{stroke:var(--ks);fill:var(--ks-s)}.hop.g-ix .hop-k{stroke:var(--ix);fill:var(--ix-s);stroke-dasharray:4 3}
.hop-ma{font:700 11.5px var(--mono)}
.hop.g-in .hop-ma{fill:var(--in)}.hop.g-ca .hop-ma{fill:var(--ca)}.hop.g-al .hop-ma{fill:var(--al)}.hop.g-dw .hop-ma{fill:var(--dw)}
.hop.g-rp .hop-ma{fill:var(--rp)}.hop.g-ks .hop-ma{fill:var(--ks)}.hop.g-ix .hop-ma{fill:var(--ix)}
.hop-ten{font:600 11px var(--sans)}.hop-d{font:10.5px var(--sans);fill:var(--muted)}
.hop-tt{font:600 10px var(--mono)}.tt-ok{fill:var(--ok)}.tt-mid{fill:var(--mid)}.tt-no{fill:var(--no)}.tt-na{fill:var(--muted)}
.hop-pd{font:10px var(--mono);fill:var(--muted)}
.nguoi{fill:var(--mid-s);stroke:var(--mid)}.nguoi-t{font:700 8.5px var(--mono);fill:var(--mid)}
.ten{stroke:var(--fg);stroke-width:1.5}.mui{fill:var(--fg)}.hit{stroke:transparent;stroke-width:12}
.ten-g{cursor:pointer}.ten-t{font:600 10px var(--mono);fill:var(--muted)}
.hop:focus-visible .hop-k,.hop.sang .hop-k{stroke:var(--sel);stroke-width:3}
.ten-g:focus-visible .ten,.ten-g.sang .ten{stroke:var(--sel);stroke-width:3}
.ten-g.sang .ten-t{fill:var(--sel)}
svg.loc .hop:not(.sang),svg.loc .ten-g:not(.sang){opacity:.28}
table.io{border-collapse:collapse;width:100%;font-size:13px}
.io th,.io td{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
.io thead th{font:600 11px var(--mono);letter-spacing:.05em;color:var(--muted);text-transform:uppercase;background:var(--bg)}
.io tr.b1 th{background:var(--in-s);color:var(--fg);font:700 12.5px var(--sans);letter-spacing:0;text-transform:none}
.io tr.b2 th{background:var(--bg);font:600 12px var(--sans);color:var(--muted)}
.io ul{margin:0;padding-left:16px}.io li{margin:1px 0}.io li.ngoai{color:var(--muted);list-style:circle}
.io .ma{font:600 11px var(--mono);color:var(--muted)}.io ul.pd{padding-left:0;list-style:none}
.io .cu{font-size:11.5px;color:var(--muted);margin-top:4px}.io .fls{font-size:12px;color:var(--muted);margin-top:4px}
tr.chon{cursor:pointer}tr.chon:hover,tr.chon.sang{background:var(--mid-s)}
.pill{display:inline-block;font:600 11px var(--mono);padding:1px 6px;border-radius:4px;white-space:nowrap}
.pill.ok{background:var(--ok-s);color:var(--ok)}.pill.mid{background:var(--mid-s);color:var(--mid)}.pill.no{background:var(--no-s);color:var(--no)}.pill.na{background:var(--bg);color:var(--muted)}
.zoom{display:flex;gap:6px;align-items:center;margin:6px 0;position:sticky;top:env(safe-area-inset-top,0px);z-index:3;background:var(--bg);padding-block:4px}
.zoom button{font:600 13px var(--mono);min-width:34px;height:30px;padding:0 10px;border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--fg);cursor:pointer}
.zoom button:hover{border-color:var(--fg)}.zoom button[aria-pressed="true"]{background:var(--fg);color:var(--paper)}
.zoom button:focus-visible{outline:2px solid var(--sel);outline-offset:1px}
#z-muc{font:600 12px var(--mono);min-width:48px;text-align:center;color:var(--muted);font-variant-numeric:tabular-nums}
#hinh-khung svg{display:block;height:auto}
.ben{stroke:none}.ben-now{fill:var(--muted)}.ben-tobe{fill:var(--fg)}.ben-t{font:700 11.5px var(--mono);letter-spacing:.06em;fill:var(--paper)}
.ben-k{fill:none;stroke-width:1.6}.ben-k.ben-now{stroke:var(--muted);stroke-dasharray:6 4}.ben-k.ben-tobe{stroke:var(--fg)}
.tang2{stroke:none}.tang2.ag-now{fill:var(--line)}.tang2.ag-ag1{fill:var(--a1-s)}.tang2.ag-ag2{fill:var(--a2-s)}.tang2.ag-ag3{fill:var(--a3-s)}
.tang2-t{font:600 10px var(--mono);letter-spacing:.05em}
.hop2{cursor:pointer}.hop2.now .hop-k{fill:var(--paper);stroke:var(--muted);stroke-dasharray:4 3;stroke-width:1.4}.hop2.now .hop-ma{fill:var(--muted);font-weight:500}
.hop2.ag-ag1 .hop-k{stroke:var(--a1);fill:var(--a1-s)}.hop2.ag-ag2 .hop-k{stroke:var(--a2);fill:var(--a2-s)}.hop2.ag-ag3 .hop-k{stroke:var(--a3);fill:var(--a3-s)}
.hop2.ag-ag1 .hop-ma{fill:var(--a1)}.hop2.ag-ag2 .hop-ma{fill:var(--a2)}.hop2.ag-ag3 .hop-ma{fill:var(--a3)}
.chip{cursor:pointer}.chip-k{stroke-width:1.2}.chip-t{font:700 9.5px var(--mono)}
.chip-ri{fill:var(--a1-s);stroke:var(--a1)}.chip-pr{fill:var(--a2-s);stroke:var(--a2)}.chip-si{fill:var(--a3-s);stroke:var(--a3)}.chip-cuoi{stroke-width:2.4}
.chip-h{display:inline-block;font:700 11px var(--mono);padding:0 6px;border-radius:8px;border:1.2px solid}
span.chip-ri{background:var(--a1-s);border-color:var(--a1);color:var(--a1)}span.chip-pr{background:var(--a2-s);border-color:var(--a2);color:var(--a2)}span.chip-si{background:var(--a3-s);border-color:var(--a3);color:var(--a3)}
.ra-ngoai{font:italic 10px var(--sans);fill:var(--muted)}
svg.loc2 .hop2:not(.sang2),svg.loc2 .hop:not(.sang2){opacity:.28}svg.loc2 .ten-g{opacity:.28}
.hop.sang2 .hop-k{stroke:var(--sel)!important;stroke-width:3}.tach{stroke:var(--line);stroke-width:2;stroke-dasharray:2 5}
.hop2.sang2 .hop-k{stroke:var(--sel)!important;stroke-width:3}.chip.sang2 .chip-k{stroke:var(--sel);stroke-width:3}
tr.chon2{cursor:pointer}tr.chon2.sang2{background:var(--mid-s)}
.note{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:10px 14px;font-size:13px;max-width:none}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--muted);margin:8px 0}
.legend i{display:inline-block;width:14px;height:10px;border-radius:2px;vertical-align:-1px;margin-right:5px;border:1.5px solid}
.ngu{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:10px 0}
.ngu>div{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:12px 14px;min-width:0}
.ngu .cong{font:700 20px var(--mono);letter-spacing:.02em}
.ngu .cong span{padding:0 2px;border-bottom:3px solid}
.khung-ct{position:fixed;right:max(12px,env(safe-area-inset-right,0px));top:calc(12px + env(safe-area-inset-top,0px));width:min(420px,calc(100vw - 24px));max-height:calc(100vh - 24px);overflow:auto;
  background:var(--paper);border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 28px rgba(0,0,0,.18);padding:14px 16px;z-index:5;font-size:13px}
.khung-ct h3{margin:2px 0 4px;font:700 15px var(--mono)}.khung-ct h4{margin:12px 0 4px;font:600 11px var(--mono);letter-spacing:.06em;color:var(--muted);text-transform:uppercase}
.khung-ct ul{margin:0;padding-left:16px}.khung-ct .x{float:right;border:0;background:none;font-size:20px;color:var(--muted);cursor:pointer}
@media (max-width:700px){.khung-ct{top:auto;bottom:calc(10px + env(safe-area-inset-bottom,0px));max-height:55vh}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = r"""
(function(){
  const D = JSON.parse(document.getElementById('du-lieu').textContent);
  const svg = document.querySelector('#hinh svg');
  const khung = document.getElementById('khung-ct'), nd = document.getElementById('ct');
  const e = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function sang(ids){
    document.querySelectorAll('.sang').forEach(x => x.classList.remove('sang'));
    if (!ids) { svg.classList.remove('loc'); return; }
    svg.classList.add('loc');
    ids.forEach(id => document.querySelectorAll('[data-id="'+id+'"],[data-ref="'+id+'"]').forEach(x => x.classList.add('sang')));
  }
  function li(a){ return a.length ? '<ul>' + a.join('') + '</ul>' : '<p>—</p>'; }
  function chon(id){
    const [k, m] = id.split(':');
    let html = '', ids = [id];
    if (k === 'h') {
      const h = D.hop[m];
      Object.entries(D.ten).forEach(([t, v]) => { if (v.tu === m || v.toi === m) ids.push('t:'+t, 'h:'+(v.tu === m ? v.toi : v.tu)); });
      html = '<h3>'+e(m)+'</h3><div>'+e(h.ten)+'</div><div class="ghichu">'+e(h.kb)+' · bước '+e(h.buoc)+'</div>'
        + '<h4>Vào</h4>' + li(h.vao.map(([t, tu, c]) => '<li>' + (t ? '<b class="mono">'+e(tu)+'</b> <span class="mono">'+t+'</span> ' : '') + e(c) + '</li>'))
        + '<h4>Ra</h4>' + li(h.ra.map(([t, toi, c]) => '<li>' + e(c) + (t ? ' → <b class="mono">'+e(toi)+'</b> <span class="mono">'+t+'</span>' : '') + '</li>'))
        + '<h4>Làm gì</h4>' + li(h.hien.map(x => '<li>'+e(x)+'</li>'))
        + (h.nguoi ? '<h4>Tay người</h4><p>'+e(h.nguoi)+'</p>' : '')
        + '<h4>Thay bước PD Now (AS-IS)</h4>' + li(h.pd.map(([s, t, tt]) => '<li><span class="mono">'+s+'</span> '+e(t)+(tt ? ' · '+e(tt) : '')+'</li>'))
        + '<h4>FLS hôm nay</h4><p><span class="pill">'+e(h.tt)+'</span><br>'+e(h.fls)+'</p>'
        + '<h4>Hộp voi v0.9</h4><p class="mono">'+e(h.cu)+'</p>';
    } else {
      const t = D.ten[m]; ids.push('h:'+t.tu, 'h:'+t.toi);
      html = '<h3>'+e(m)+'</h3><div class="mono">'+e(t.tu)+' → '+e(t.toi)+'</div><h4>Cái gì chảy</h4><p>'+e(t.cai_gi)+'</p>'
        + '<h4>Khoá</h4><p class="mono">'+e(t.khoa)+'</p><h4>AS-IS hôm nay (bước PD Now)</h4><p class="mono">'+e(t.pd)+'</p>';
    }
    nd.innerHTML = html; khung.hidden = false; sang(ids);
  }
  function dong(){ khung.hidden = true; sang(null); }
  svg.addEventListener('click', ev => {
    const c = ev.target.closest('.chip') || ev.target.closest('.hop2');
    if (c) { dong(); sang2(c.dataset.o ? c.dataset.o.split(' ') : null); return; }
    sang2(null);
    const g = ev.target.closest('[data-id]'); if (g) chon(g.dataset.id); else dong(); });
  svg.addEventListener('keydown', ev => { const g = ev.target.closest('[data-id]'); if (g && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); chon(g.dataset.id); } });
  document.querySelectorAll('tr.chon').forEach(r => { r.addEventListener('click', () => chon(r.dataset.ref)); r.addEventListener('keydown', ev => { if (ev.key === 'Enter') chon(r.dataset.ref); }); });
  document.getElementById('nut-dong').addEventListener('click', dong);
  // ── phóng to / thu nhỏ: "Vừa khung" = cả hình nằm gọn bề ngang khung, tự theo khi đổi cỡ cửa sổ
  const W0 = svg.viewBox.baseVal.width, khungH = document.getElementById('hinh-khung');
  const muc = document.getElementById('z-muc'), nutVua = document.getElementById('z-vua');
  let tl = 1, vua = true;
  function dat(t){ tl = Math.min(2.5, Math.max(0.3, t)); svg.style.width = (W0 * tl) + 'px'; muc.textContent = Math.round(tl * 100) + '%'; }
  function vuaKhung(){ vua = true; nutVua.setAttribute('aria-pressed', 'true'); dat((khungH.clientWidth - 14) / W0); }
  function tay(t){ vua = false; nutVua.setAttribute('aria-pressed', 'false'); dat(t); }
  document.getElementById('z-cong').addEventListener('click', () => tay(tl * 1.2));
  document.getElementById('z-tru').addEventListener('click', () => tay(tl / 1.2));
  document.getElementById('z-100').addEventListener('click', () => tay(1));
  nutVua.addEventListener('click', vuaKhung);
  window.addEventListener('resize', () => { if (vua) vuaKhung(); });
  vuaKhung();
  // ── hình 2: bấm chip / hộp / dòng bảng ⇒ sáng mọi chỗ mang cùng output, ở cả hai bên
  const svg2 = svg;
  function sang2(os){
    document.querySelectorAll('.sang2').forEach(x => x.classList.remove('sang2'));
    if (!os) { svg2.classList.remove('loc2'); return; }
    svg2.classList.add('loc2');
    os.forEach(o => document.querySelectorAll('[data-o~="'+o+'"]').forEach(x => x.classList.add('sang2')));
  }
  svg2.addEventListener('keydown', ev => { const c = ev.target.closest('[data-o]'); if (c && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); sang2(c.dataset.o.split(' ')); } });
  document.querySelectorAll('tr.chon2').forEach(r => r.addEventListener('click', () => { dong(); sang2([r.dataset.o]); document.getElementById('hinh').scrollIntoView({block:'nearest'}); }));
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape') dong(); });
})();
"""


def trang() -> str:
    loi = kiem() + kiem_now()
    if loi:
        raise SystemExit("⛔ voi SAI:\n  " + "\n  ".join(loi))
    n_dl = sum(1 for h in HOP if HANG[h.hang[0]][0] == "DỮ LIỆU")
    cap = (f'Hình 1 — Voi FLS v2. <b>Nửa trái NOW</b>: {len(HOP_NOW)} hộp gộp từ voi AS-IS của artifact cũ, tới ITL Adjust. <b>Nửa phải TO-BE</b> — trục ngang: tầng trên là <b>agent</b> (Agent 1 · Agent 2 · Agent 3 · mã tất định), tầng dưới là <b>bước</b> '
           f'theo kiến trúc FPA (INPUT · CALCULATE · ALLOCATE · WAREHOUSE · REPORT, 11 cột con); <b>Agent 4 · Auditor</b> là làn ngang chạy suốt các bước. '
           f'<b>Trục dọc</b>: bốn họ dữ liệu BANK · PAY · HR · PLT, rồi hàng INDEX. '
           f'Máy kiểm lúc sinh: <b>{len(HOP)} hộp</b> ({n_dl} hộp luồng · 5 cổng · 5 cấu hình) · <b>{len(TEN)} mũi tên</b>, cả {len(TEN)} nằm ngang, '
           f'đi trái → phải, 0 cắt qua hộp (e13 đi qua làn trống); mã mỗi hộp nói đúng bước của cột chứa nó. '
           f'Nhãn NGƯỜI = có tay người · chip A3.3 = agent gợi ý phần dư · "PD …" = bước PD Now hộp ấy thay.')
    o = ['<title>Voi FLS v2</title>', '<meta name="claude:viewport-fit-sides" content="cover">',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;display=swap">',
         f'<style>{CSS}</style><main>',
         '<header><h1>Voi FLS v2 — vẽ lại theo kiến trúc FPA</h1>'
         '<p class="meta"><span class="nhap">BẢN NHÁP v2.1</span>chờ owner duyệt · 2026-11-12 · ⛔ chưa gộp vào artifact "Voi FLS-tobe-phase1" (v0.9.1). '
         f'Dựng từ PD Now FS2 ({len(PDNOW["buoc"])} bước, {len(PDNOW["ten"])} mũi tên suy từ ma trận I/O), PD200 Runner Guide và ảnh kiến trúc FPA; '
         'sinh bởi <code>docs/ITL/_tools/sinh_voi_v2.py</code>.</p></header>',
         '<h2>§0 · Đọc tên là biết ô ở đâu</h2>'
         '<p>Mỗi hộp có mã <b>bước + "." + phần</b>, cùng cách FPA ghép mã bước vào tên (<code>APR</code> · <code>ACA</code>). '
         'FLS chỉ có số thực, nên bỏ chữ kịch bản (A / P) của FPA. Máy kiểm: mã bước trong tên phải trùng bước của cột chứa hộp — đặt sai cột là trang không sinh được.</p>'
         '<div class="ngu"><div><div class="cong"><span style="border-color:var(--ca)">CA</span>.<span style="border-color:var(--muted)">GL</span></div>'
         '<p class="ghichu"><b>CA</b> = bước Calculate<br><b>.GL</b> = phần: một họ nguồn (BANK · PAY · HR · PLT), một chiều (CFA1 · PLA3) hay một vật (MAP · ITL · GL · CCR)</p></div>'
         '<div><div class="cong">SO.PLA3<span style="border-color:var(--al)">-ATL</span></div><p class="ghichu">đuôi <b>-ATL</b> = sau phân bổ (đúng chữ PD Now dùng ở sheet 606). '
         'Cùng chiều PLA3 có hai đầu ra: <code>SO.PLA3</code> (trước, cột CALCULATE) và <code>SO.PLA3-ATL</code> (sau, cột ALLOCATE).</p></div>'
         '<div><div class="cong">KS.SI · IX.FX</div><p class="ghichu">hai hàng xuyên suốt theo cùng luật: <b>KS</b> = cổng của Agent 4 · Auditor, <b>IX</b> = index / config; '
         'phần sau dấu chấm là bước mà cổng / cấu hình phục vụ.</p></div></div>',
         bang_ngu_phap(),
         '<h2>§1 · Con voi — NOW bên trái, TO-BE bên phải</h2>''<p>Một hình, chung hàng họ dữ liệu. Bên trái: luồng Google Sheets hôm nay tới ITL Adjust. Bên phải: TO-BE theo agent × bước. Chip <span class="chip-h chip-ri">RI-1</span> … <span class="chip-h chip-si">SI-3</span> là <b>output</b> — cùng mã ở hai bên là cùng một output; bấm một chip để làm sáng cặp. Sau ITL Adjust là mã tất định nên bên NOW dừng ở đó.</p>'
         '<div class="legend">'
         '<span><i style="border-color:var(--muted);border-style:dashed"></i>NOW · Google Sheets hôm nay · TAY = người bấm / gõ</span>'
         '<span><i style="border-color:var(--a1);background:var(--a1-s)"></i>Agent 1 · Collect_raw_data</span>'
         '<span><i style="border-color:var(--a2);background:var(--a2-s)"></i>Agent 2 · Generate Group Ledger (ITL raw)</span>'
         '<span><i style="border-color:var(--a3);background:var(--a3-s)"></i>Agent 3 · Filter Fulfill &amp; Adjust (ITL Adjust)</span>'
         '<span><i style="border-color:var(--muted);border-style:dashed"></i>mã tất định</span>'
         '<span><i style="border-color:var(--a4);background:var(--a4-s)"></i>Agent 4 · Auditor (Compounding Loop)</span>'
         '<span><i style="border-color:var(--ix);background:var(--ix-s);border-style:dashed"></i>INDEX · CONFIG</span>'
         '<span><b style="color:var(--ok)">✅</b> có mã · <b style="color:var(--mid)">◐</b> một phần · <b style="color:var(--no)">⛔</b> chưa có mã</span></div>',
         '<div class="zoom" role="toolbar" aria-label="Phóng to thu nhỏ hình"><button type="button" id="z-tru" aria-label="Thu nhỏ">−</button>'
         '<span id="z-muc" aria-live="polite">100%</span><button type="button" id="z-cong" aria-label="Phóng to">+</button>'
         '<button type="button" id="z-100">100%</button><button type="button" id="z-vua" aria-pressed="true">Vừa khung</button></div>',
         f'<figure id="hinh"><div class="scroll" id="hinh-khung">{svg()}</div><figcaption>{cap}</figcaption></figure>',
         tom_tat_now(),
         '<h2>§2 · Audit ngược — từ output cuối về RAW</h2>'
         '<p>Đọc từ trên xuống: output cuối trước, rồi output nó đọc từ, tới nguồn thô. Mỗi dòng: NOW sinh ở đâu, TO-BE sinh ở đâu, và phép đo nào chứng minh hai bên ra cùng một thứ.</p>',
         bang_audit(),
         '<h2>§3 · Đầu vào và đầu ra của từng hộp TO-BE</h2>'
         '<p>Cột <i>vào</i> / <i>ra</i>: dòng đậm là mũi tên trên hình (mã <span class="mono">e…</span>), dòng nhạt là nguồn ngoài, người, hay cấu hình. '
         'Cột <i>thay bước PD Now</i> nối mỗi hộp về đúng các bước AS-IS nó thay — bấm một dòng để thấy hộp trên hình.</p>',
         bang_io(),
         '<h2>§4 · Mũi tên nói gì</h2>', bang_ten(),
         '<h2>§5 · Mọi bước PD Now đều có chỗ</h2>', bang_phu(),
         '<h2>§6 · Soát lại voi AS-IS trong artifact theo PD Now</h2>'
         f'<p>Đo bằng máy: lấy cột "bước" của 52 hộp AS-IS gốc (<code>voi_asis_goc.json</code>) so với {len(PDNOW["buoc"])} bước PD Now và {len(PDNOW["ten"])} mũi tên suy từ ma trận I/O.</p>',
         bang_asis(),
         '<h2>§7 · Câu chờ owner duyệt</h2><ol>'
         '<li><b>Ngữ pháp tên</b> <code>RI·PR·SI·CA·SO·AL·DW·RP·KS·IX + .phần</code> và đuôi <code>-ATL</code> — giữ? (vd <code>APR</code> của FPA gồm cả RAW, ở đây RAW tách thành <code>RI</code>.)</li>'
         '<li><b>Chia agent theo hai file ITL của AS-IS:</b> bước ghép Reference No / Số CT (<code>SI.MAP</code>, PD 302–308 nằm trong file ITL 1/2 RAW) chuyển từ Agent 3 sang <b>Agent 2 · ITL raw</b>; Agent 3 · ITL Adjust giữ sổ ITL + lớp sửa (file 2/2 ADJUSTED). Voi v0.9 đặt bước ghép ở Agent 3 — đổi như vậy được không?</li>'
         '<li><b>Hai cột STANDARD INPUT</b> (ghép · sổ ITL): sổ ITL hiệu lực là "standard input" của FLS (như A-SI-R20/R50 của FPA) — đúng ý chưa?</li>'
         '<li><b>HR ⛔ qua ALLOCATE</b> (PD 500: đã phân bổ ở payroll) — giữ? <b>Báo cáo HR</b> 102 · 611 · 612 để ngoài GĐ1?</li>'
         '<li><b>Kho:</b> FLS giữ PostgreSQL chỉ-thêm, hay đẩy khối SO lên BigQuery như FDW của FPA để REPORT dùng chung? Và bước <code>[Importrange] 1.2 Ledger 112</code> mà ma trận PD Now trỏ tới (cột 54) nhưng không ghi thành bước — có thật không?</li>'
         '<li><b>AP / AR</b> (223 · 224 · 310–312, AS-IS "Not yet") — đưa vào GĐ1 hay GĐ2?</li></ol>',
         '</main>',
         '<aside class="khung-ct" id="khung-ct" hidden aria-label="Chi tiết"><button class="x" id="nut-dong" type="button" aria-label="Đóng">×</button><div id="ct"></div></aside>',
         f'<script type="application/json" id="du-lieu">{du_lieu()}</script>', f'<script>{JS}</script>']
    return "\n".join(o)


def main() -> int:
    loi = kiem() + kiem_now()
    print(f"NOW ↔ TO-BE: output {len(OUT)} · hộp NOW {len(HOP_NOW)} (gộp {sum(len(h.goc) for h in HOP_NOW)} hộp gốc + {len(NGOAI_NOW)} ngoài)")
    print(f"hộp {len(HOP)} · mũi tên {len(TEN)} · cột {len(COT)} · hàng {len(HANG)}")
    print(f"PD Now: {len(PDNOW['buoc'])} bước · vào hộp {sum(len(h.pd) for h in HOP)} · ngoài {sum(len(v) for v in NGOAI.values())}")
    if loi:
        print("⛔ LỖI:\n  " + "\n  ".join(loi))
        return 1
    if "--kiem" in sys.argv:
        print("✅ voi đúng luật — ⛔ không ghi (--kiem)")
        return 0
    DICH.write_text(trang(), encoding="utf-8")
    print(f"✅ đã ghi {DICH.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
