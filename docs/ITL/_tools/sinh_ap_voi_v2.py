# -*- coding: utf-8 -*-
"""Sinh AP hoàn chỉnh của Voi FLS v2 — `AP_FLS-Voi_v2.5.0_Doi-Chieu-NOW-TOBE_2026-11-13.html`.

⭐ Owner 13/11 (KhanhCQ): "Dựa vào voi trên, làm lại 1 bản AP hoàn chỉnh (skill apr-build-ap), cập nhật vào
   bản ver 2 này. Cột là tháng, dòng là các loại dữ liệu. Mỗi ô cần có dữ liệu đối chiếu → Voi số lượng dữ
   liệu: số có, số chạy, mapping và số đã sửa sai. Tôi sẽ giao agents đọc công thức gsheet, script của now →
   hệ thống tính toán của tobe → code."

⭐ MỘT nguồn sự thật cho mỗi thứ — AP ⛔ chép tay:
   · hộp · mũi tên · hình voi · bước PD Now  ← `sinh_voi_v2.py` (import, ⛔ sao chép)
   · ma trận tháng × loại dữ liệu             ← `voi_so_luong.json` (sinh bởi `tools/do_voi_so_luong.py`)
   · khung AP (CSS · rail · trạng thái)        ← skill apr-build-ap `references/` (inline nguyên văn, §A.31)

Chạy:  python docs/ITL/_tools/sinh_ap_voi_v2.py
Sau đó (bắt buộc, theo skill): ap-status-check --restamp + --rebuild-index · toc-tree-check · style-check ·
figure-section-check — lệnh nằm ở cuối tệp này (`CONG`).
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

DAY = Path(__file__).resolve().parent
GOC = DAY.parents[2]
sys.path.insert(0, str(DAY))
import sinh_voi_v2 as V  # noqa: E402

SKILL = Path("/root/.claude/skills/synced/1b8da73f-77c4-495f-89f5-e856b18560a0_5ecf2698-132a-4770-9b6d-414419313b06/apr-build-ap/references")
RA = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v2.5.0_Doi-Chieu-NOW-TOBE_2026-11-13.html"
SL = json.loads((DAY / "voi_so_luong.json").read_text(encoding="utf-8"))
NGAY = "2026-11-13"
E = html.escape
SEP = "<!-- " + "═" * 72 + " -->"


def so(n) -> str:
    return f"{n:,}".replace(",", ".")


def pt(a, b) -> str:
    return "—" if not b else f"{100 * a / b:.1f}".replace(".", ",") + "%"


# ═════════════════ KHUNG: heading mang trạng thái (§A.14) ═════════════════
_cha: dict[int, str] = {}


def h(lvl: int, uid: str, text: str, st: str | None = None, part: bool = False, badge: str = "") -> str:
    """Heading. st=None ⇒ thừa kế trạng thái của heading cha gần nhất (data-st-inherited)."""
    if st is None:
        cha = next(_cha[l] for l in range(lvl - 1, 1, -1) if l in _cha)
        st_eff, inh = _st[cha], f' data-st-inherited="{cha}"'
    else:
        st_eff, inh = st, ""
    _cha[lvl] = uid
    for l in list(_cha):
        if l > lvl:
            del _cha[l]
    _st[uid] = st_eff
    cls = ' class="part"' if part else ""
    b = f' <span class="badge {badge[0]}">{badge[1]}</span>' if badge else ""
    tag = f'<h{lvl}{cls} id="{uid}" data-st="{st_eff}" data-st-on="{NGAY}"{inh}>{text}{b}</h{lvl}>'
    return (SEP + "\n" + tag + "\n" + SEP) if part else tag


_st: dict[str, str] = {}


def part(k: int, ten: str) -> str:
    return f'<h2 class="part-divider">Part {k} — {ten}</h2>'


def bang(cot: list[tuple[str, int]], hang: list[list[str]], cls: str = "", nhom: dict[int, str] | None = None) -> str:
    assert sum(w for _, w in cot) == 100, cot
    o = [f'<div class="tw"><table{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} style="table-layout:fixed">',
         "<colgroup>" + "".join(f'<col style="width:{w}%">' for _, w in cot) + "</colgroup>",
         "<tr>" + "".join(f"<th>{t}</th>" for t, _ in cot) + "</tr>"]
    for i, r in enumerate(hang):
        if nhom and i in nhom:
            o.append(f'<tr><th colspan="{len(cot)}" style="text-align:left">{nhom[i]}</th></tr>')
        o.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    o.append("</table></div>")
    return "\n".join(o)


def ul(xs) -> str:
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def cap(num: str, comp: str, ten: str, ghi: list[str]) -> str:
    return (f'<p class="fig-cap"><strong>Figure {num}</strong> — <strong>{comp}:</strong> {ten}</p>'
            + (f'<ul class="fig-notes">{"".join(f"<li>{x}</li>" for x in ghi)}</ul>' if ghi else ""))


def gap(tom: str, noi: str) -> str:
    """Khối cho agent / máy kiểm đọc (§A.27) — gập mặc định, tóm tắt nói rõ bên trong là gì."""
    return f"<details><summary>{tom}</summary>{noi}</details>"


# ═════════════════ HỘP: lấy từ voi v2 (⛔ chép) ═════════════════
HOP = {x.ma: x for x in V.HOP}
TEN = {t.ma: t for t in V.TEN} if hasattr(V.TEN[0], "ma") else {}
PD = V.PDNOW["buoc"]


def trang_thai(ma: str) -> tuple[str, str]:
    tt = HOP[ma].tt
    if tt.startswith("✅"):
        return "built", "BUILT"
    if tt.startswith("◐"):
        return "partial", "PARTIAL"
    return "miss", "PROPOSED"


def pd_html(ma: str) -> str:
    ds = HOP[ma].pd
    if not ds:
        return '<span class="nw">— (AS-IS không có bước này)</span>'
    out = []
    for s in ds:
        b = PD.get(s, {})
        ten = " › ".join(x for x in (b.get("tep", ""), b.get("sheet", "") or b.get("nhom", "")) if x)
        out.append(f"<code>{s}</code> {E(ten)}" + (f" <i>({E(b.get('tt'))})</i>" if b.get("tt") and b.get("tt") != "Done" else ""))
    return "<br>".join(out)


# ═════════════════ TRUY VẾT: NOW (công thức · script) → TO-BE (phép tính) → CODE ═════════════════
# Công thức NGUYÊN VĂN chỉ lấy từ chỗ đã đọc và ghi trong mã (Đ1: grep fls/ + tools/ trước khi viết):
#   final_rule.py:1-30 (7 khối Final/MID) · allocate.py:1-20 (AU/AV/AW) · classifying.py:1-10 (iferror)
#   · tools/do_kha_nang_doc.py:17 (A10 = filter(IMPORTRANGE…)) · Kiem-TOBE-theo-ASIS.md #1–#14.
F_FINAL = 'V = if(or(S="Need to manual input", len(S)=0), U, S)   ← Final = f(Classifying, MID), ×7 khối'
F_MID = 'U = if(T="" và S<>"Need to manual input", S, if(T="Input here", &lt;MẶC ĐỊNH CỨNG của khối&gt;, T))'
F_CLS = 'Classifying = iferror(&lt;cột canon của Transaction Mapping L1&gt;, "Need to manual input")'
F_ALLOC = ('AU =ArrayFormula(AD7:AD)\nAV =ArrayFormula(if(VLOOKUP(V7:V,{MM!H:H,MM!K:K},2,FALSE)="Need to Allocate to CFA2",'
           '"Need to Allocate to CFA2",AU7:AU))\nAW =ArrayFormula(if(VLOOKUP(V7:V,{MM!H:H,MM!L:L},2,FALSE)&lt;&gt;"",'
           'VLOOKUP(V7:V,{MM!H:H,MM!L:L},2,FALSE),"No need"))')
F_A10 = 'A10 = filter(IMPORTRANGE($B$1,$B$2&amp;"!A4:F"), IMPORTRANGE($B$1,$B$2&amp;"!A4:A")&gt;$B$3)'

TRUY = {  # mã: (NOW · công thức / script, TO-BE · phép tính, CODE · tệp + test, SỐ ĐỐI CHIẾU, CÒN LẠI cho agent)
    "RI.BANK": ("Sheet <code>R | &lt;số TK&gt;_&lt;bank&gt; &lt;tiền tệ&gt;_&lt;LE&gt;</code> — pháp nhân nằm trong tên sheet; dòng 1 = bố cục cột. "
                "Script <code>Run</code> ở <code>BankAccountList</code> / <code>Cash Ledger List</code> đọc <code>Range_Condition/Debit/Credit</code>. "
                "Cột <code>Reference number_adjust</code> người gõ đè: có <code>_adjust</code> thì <code>_adjust</code> thắng.",
                "Chụp vùng chuẩn theo bản khai có version → ảnh chỉ-thêm (<code>chup_id</code>); "
                "so hai bản khai (dòng 1 ↔ Range_*) mỗi lần nạp (S10).",
                "<code>tools/chup_sao_ke.py</code> · <code>fls/repo/chup.py</code> · <code>fls/repo/khai_cot.py</code> · <code>fls/repo/nguon_dai.py</code>"
                "<br>test: <code>tests/repo/test_chup_pg.py</code> · <code>test_khai_cot_pg.py</code> · <code>tests/kiem/test_s10_hai_ban_khai.py</code>",
                "Bank: 60 nguồn · 8.338/8.338 dòng đọc được · 192 phép so hai bản khai, 0 lệch. Quỹ · CCR: 0 ảnh.",
                ["bật lằn Cash (<code>LAN</code> đã khai Bank · Cash · PM, công cụ chỉ chạy Bank)",
                 "thêm <code>ref_adjust</code> vào bản khai + ảnh, đánh dấu dòng bị đè (58/60 bank · 7/8 quỹ)",
                 "chụp 2 sheet CCR (số dư ngày) — hiện chỉ đo bằng <code>tools/do_trong_tai.py</code>"]),
    "RI.PAY": ("FPS · <code>A|PAY100</code> Entry Data PE11 / PI11 / PM11 / PC11 (Gform, sếp duyệt). "
               "<code>PM_Unpivot</code>: tiêu đề dòng 2, dữ liệu dòng 3.",
               "Chụp dòng sổ cái PM qua cùng lằn ảnh chụp → bản khai → soát → nạp lô; cột <code>Email Address</code> cấm vào kho.",
               "<code>fls/repo/anh_pm.py</code> · <code>fls/adapters/pm_join.py</code> (<code>kiem_tieu_de_pm</code>)"
               "<br>test: <code>tests/repo/test_anh_pm_pg.py</code> · <code>test_nap_anh_pm_pg.py</code> · <code>test_pm_line_snap_pg.py</code>",
               f"PM: {so(SL['pm_tong']['so_dong_pm'])} dòng trên ảnh 27/08 ({so(SL['pm_tong']['pm_co_ref'])} có Ref No) · kho: 3.772 dòng <code>fls_pm_line</code>. PC: 0 tham chiếu.",
               ["đọc lằn PC (PC11 Entry Data, PD 113–114)", "đọc PE · PI làm chiều phụ của PM line"]),
    "PR.BANK": ("GScript gom các sheet <code>R |</code> → <code>Bank Transactions</code> / <code>Cash Ledger Transactions</code> → "
                "<code>1.2 Ledger 112</code> · <code>1.1 Ledger 111</code>. <code>Bank Transactions_Filter</code> là cầu, ⛔ bộ lọc. "
                "<code>Num</code> chống trùng.",
                "Dựng dòng canon 36 trường, hai vế Nợ / Có, LE theo TK, <code>content_key</code>; nạp lô một giao dịch, cổng 4 vế.",
                "<code>fls/adapters/sao_ke.py</code> · <code>sao_ke_canon.py</code> · <code>fls/repo/chay_nap.py</code>"
                "<br>test: <code>tests/adapters/test_sao_ke.py</code> · <code>tests/repo/test_chay_nap_pg.py</code> · <code>test_nap_lo_pg.py</code>",
                f"Trên ảnh 26/08: {so(SL['tong']['chay'])}/{so(SL['tong']['co'])} dòng sổ dựng lại và ghép 1-1 ({pt(SL['tong']['chay'], SL['tong']['co'])}) — Figure 2.2 hàng BANK.",
                ["số dư ngày từng TK (0 mã)", "dòng quỹ (Ledger 111) khi lằn Cash bật",
                 f"122 dòng sổ chưa có bản dựng 1-1 — tìm vì sao (Figure 2.2: chạy &lt; có ở 20/23 tháng)"]),
    "PR.PAY": ("GScript duỗi → <code>PE_Unpivot</code> · <code>PI_Unpivot</code> · <code>PM_Unpivot</code> · <code>PC_Unpivot</code>: một dòng mỗi line.",
               "Duỗi line, đặt kiểu 28 cột (14 có kiểu · 1 cấm · 13 thô); khoá dòng là <code>line</code>, ⛔ <code>slip</code>.",
               "<code>fls/adapters/pm_join.py</code> (<code>DongPM</code>, <code>loc_tho</code>)"
               "<br>test: <code>tests/adapters/test_pm_join.py</code> · <code>tests/repo/test_pe_pi_co_kieu.py</code> · <code>test_g_mod_3_phan_hoach_truong_pm.py</code>",
               "28 cột PM: 14 có kiểu · 13 thô.",
               ["đặt kiểu 13 cột thô còn lại", "duỗi PC"]),
    "SI.MAP": ("<code>Transaction Original</code> → <code>Transaction Mapping L1</code>: VLOOKUP Số CT (Reference number) vào "
               "<code>PM_Unpivot</code> cột Z, lấy dòng đầu tiên tìm thấy. Classifying 7 khối:"
               f"<pre>{F_CLS}</pre>",
               "Ghép theo Ref No + Σ tiền trong dung sai (1.000 VND · tiền tệ khác 0); xếp 6 hình A–F; "
               "A · B · C ghép được, D · E · F để người (kèm lý do có tên); N×M ⛔ đoán.",
               "<code>fls/adapters/pm_join.py</code> (<code>xep_ca_lat</code>, <code>xep_hinh</code>, <code>moi_noi</code>) · <code>fls/repo/may_ghep.py</code> · "
               "<code>fls/ledger/classifying.py</code><br>test: <code>tests/adapters/test_pm_join.py</code> · <code>tests/ledger/test_classifying.py</code> · "
               "<code>tests/repo/test_pm_link_pg.py</code>",
               f"Bank {so(SL['bank_tong']['dong_bank'])} dòng: NOW VLOOKUP trả mã {so(SL['tong']['map_now'])} dòng sổ; FLS ghép hình A·B·C "
               f"{so(SL['tong']['map_fls'])} dòng có kỳ — Classifying suy từ canon 68.915 ô, 100%.",
               ["PP (2): nối dòng lương H1000 theo Số CT (0 mã)", "PP (3): Combine Code vendor-ngày-NoTrans (0 mã)",
                "hình D · E · F: agent A2 gợi ý (Phase 2)"]),
    "SI.ITL": (f"File <code>ITL 2/2 (ADJUSTED)</code> › <code>ITL Ledge</code>: <pre>{F_A10}</pre>"
               f"Vùng chỉnh tay R–AT, 7 khối, mỗi khối 4 cột S T U V:<pre>{F_MID}\n{F_FINAL}</pre>"
               f"Vùng ALLOCATE:<pre>{F_ALLOC}</pre>",
               "Sổ ITL gốc chỉ-thêm + lớp sửa có actor (người › máy); giá trị hiệu lực = lớp sửa mới nhất, nếu không thì gốc; "
               "Final tái hiện đúng hai bước MID → Final; 3 cột ALLOCATE suy lại từ <code>fls_mapping_master</code>, ⛔ lưu.",
               "<code>fls/ledger/final_rule.py</code> · <code>fls/ledger/allocate.py</code> · <code>fls/ledger/build.py</code> · <code>fls/repo/itl_repo.py</code> · "
               "<code>fls/repo/ghi_tay.py</code><br>test: <code>tests/ledger/test_parity_ca_so.py</code> · <code>test_final_rule.py</code> · "
               "<code>test_allocate.py</code> · <code>tests/repo/test_ghi_tay_pg.py</code>",
               f"Parity trên ảnh 26/08: {so(SL['tong']['o_parity_khop'])}/{so(SL['tong']['o_parity'])} ô Final, 23 kỳ (37 dòng 2026-07 bị tự soi loại, có lý do). "
               "Kho: <code>fls_itl</code> 8.387 · <code>fls_adjustment</code> 4.428.",
               ["MID chưa xác nhận công thức live (<code>GAP-ORA-05</code>) — đọc lại với <code>valueRenderOption=FORMULA</code>",
                "khối 4–5 kỳ DV: chưa suy được mặc định (<code>GAP-ORA-06</code>)",
                "đủ 4 họ: dòng H1000 + dòng nền tảng vào cùng sổ (Part 5)"]),
    "KS.RI": ("— (AS-IS ⛔ có cổng; người nhìn)", "Bản khai đủ · bề rộng cột · Σ dòng ảnh = Σ dòng nguồn.",
              "<code>fls/kiem/soat_nap.py</code> · <code>kiem_tieu_de_pm</code><br>test: <code>tests/kiem/test_soat_nap.py</code>",
              "9 luật S1–S8 + S10 có ca đỏ.", ["mở rộng cho PM · PC · H1000 · nền tảng"]),
    "KS.SI": ("<code>CHECK BALANCE</code>: số dư nhập tay ở <code>2. CCR</code> ↔ lũy kế Ledger 112/111 theo ngày (DIF) — người soát bằng mắt.",
              "Σ PM line = tiền giao dịch · 4 vế · số dư đầu + Σ Nợ − Σ Có = CCR (DIF = 0), liệt kê lệch từng TK · ngày.",
              "<code>fls/kiem/soat_nap.py</code> · <code>fls/repo/chay_nap.py</code> (cổng 4 vế)<br>test: <code>tests/kiem/test_soat_nap.py</code> · <code>tests/repo/test_chay_nap_pg.py</code>",
              "9 luật ✅ · DIF ⛔ (chưa có ảnh CCR).", ["cổng DIF khi RI.BANK chụp CCR"]),
    "KS.RP": ("— (AS-IS ⛔ có)", "So từng ô với ITL Ledge Final / Daily Report AS-IS; chênh liệt kê từng ô, có tên.",
              "<code>fls/oracle/cong_parity.py</code> · <code>fls/oracle/tu_soi.py</code><br>test: <code>tests/oracle/test_cong_parity.py</code> · <code>test_tu_soi.py</code>",
              f"ITL: {so(SL['tong']['o_parity_khop'])}/{so(SL['tong']['o_parity'])} ô ✅ · báo cáo ⛔.", ["parity Daily Report 2 · 3 khi RP.CF · RP.PL có"]),
    "IX.KHAI": ("Dòng 1 của mỗi sheet <code>R |</code> + <code>Range_*</code> của danh mục.", "Bản khai cột · thứ tự ngày · LE TK, có version, owner ký; chỉ-thêm.",
                "<code>fls/repo/khai_cot.py</code> · <code>fls/repo/nguon_dai.py</code><br>test: <code>tests/repo/test_khai_cot_pg.py</code> · <code>test_nguon_dai_pg.py</code>",
                "408 dòng = 68 × 6.", ["khai cho PC · H1000 · 4 nguồn nền tảng"]),
    "IX.MM": ("<code>Mapping Master</code> (PD 301): H = hd → K (cần phân bổ CFA2) · L (phương pháp).", "Bảng <code>fls_mapping_master(need_cfa2, method_cfa2)</code>; ALLOCATE tra theo hd.",
              "<code>fls/adapters/mapping_master.py</code> · <code>tools/nap_mapping_master.py</code><br>test: <code>tests/adapters/test_mapping_master.py</code> · <code>tests/repo/test_nap_mapping_pg.py</code>",
              "73 mã hd, 0 trùng (đo 28/08).", ["Mapping Block 1 (vendor ↔ network ↔ CDT1) — Part 5"]),
    "DW": ("— AS-IS không có kho: ~10 file Gsheet nối nhau bằng IMPORTRANGE.", "PostgreSQL chỉ-thêm: ảnh · dòng · sổ · lớp sửa; dây truy ngược ô → dòng → giao dịch → ảnh.",
           "<code>fls/db/schema.py</code> · <code>fls/db/migrations/</code><br>test: <code>tests/db/</code> · <code>tests/repo/test_kho_sach.py</code>",
           "Sổ có; bảng khối báo cáo SO: 0.", ["bảng khối SO (KRF × kỳ) khi CA · SO có"]),
    "RP.FLS": ("<code>[RAW ITL] Data Management</code> (613) · <code>[CA] Nhật ký xử lý giao dịch</code> (617).", "Màn F01 hàng chờ · F02 sổ · F03 cổng · F04 nạp lô; bấm một ô → dòng → giao dịch → ảnh.",
               "<code>fls/web/tep/man_f01*.js</code> · <code>man_f02.js</code> · <code>man_f03.js</code> · <code>man_f04.js</code> · <code>fls/api/</code>"
               "<br>test: <code>tests/web/</code> · <code>tests/api/</code>", "6 màn · 37 tuyến API.", ["truy ngược từ ô báo cáo (khi RP.CF · RP.PL có)"]),
    "RP.CCR": ("<code>5. Daily Report</code> (615) · <code>6. CCR I DEL I W I Pdf</code> (616); ThuongCT ký mỗi tháng.", "Ghi ô neo theo khoá vào CCR: chạy khô → cờ duyệt.",
               "<code>fls/xuat/ghi_o.py</code> · <code>tools/ghi_o_that.py</code><br>test: <code>tests/xuat/test_ghi_o.py</code>",
               "Cơ chế ghi ✅ (27 bài) · bộ xuất ⛔.", ["bộ xuất báo cáo daily theo TK · pháp nhân · ngày"]),
}
DE_XUAT = {  # mã: (NOW, TO-BE dự kiến, CODE đích, cách đối chiếu)
    "RI.HR": ("H1000 Ledger (APERO-HR Allocate HD), PD 101 — HR · C&amp;B lập, kế toán dán số FT vào dòng 4–8 sheet <i>No n</i>.",
              "Chụp ~34 tệp H1000 đã adjust qua lằn ảnh chụp thứ tư.", "lằn <code>HR</code> trong <code>fls/repo/chup.py</code> + bản khai",
              "Σ dòng ảnh = Σ dòng tệp, theo tháng (Figure 2.2 hàng HR)"),
    "RI.PLT": ("GI · OMC xuất từ Looker (Data · AnhTQ, PD 103–104); SC từ Gsheet <i>Chi phí Service Apero</i> (105); PS từ <i>AperoGroup_Payment</i> (106).",
               "Chụp 4 nguồn, đóng băng theo tháng.", "lằn <code>PLT</code> + bản khai 4 nguồn", "Σ dòng theo loại × tháng (hàng PLT)"),
    "PR.HR": ("Tách lương → <code>1.3 Ledger NIS/INT/COM</code> · <code>PIT</code> 2024–2025 (PD 219–222); đợt = 5 pháp nhân × 5 loại.",
              "Dòng lương + Số CT; Σ Có = Σ Nợ mỗi đợt; đủ tháng, ⛔ trùng.", "adapter D (mới) · <code>fls/adapters/</code>", "Σ đợt = Σ tệp; tháng trùng · thiếu = 0"),
    "PR.PLT": ("Gom → Platform Data Ledger ×4 (PD 210–213); Combine Code = Vendor-Date-NoTrans.",
               "Chi phí theo loại · vendor · ngày + Combine Code, vào STANDARD INPUT như 3 họ kia.", "adapter mới + khoá Combine Code", "Σ tiền theo loại × tháng = sổ H2.2025"),
    "CA.GL": ("<code>Report I General Ledger</code> (406), <code>9.2.Exchange Rate</code> (405); H1000 Ledge 401–404.",
              "ITL hiệu lực → khuôn GL (Templ 2); quy đổi theo tỷ giá tháng; gắn chiều CFA1 (LE) · PLA1 · CFA3 · PLA3 (KRF).",
              "<code>fls/ledger/</code> (mới) — grep <code>ty_gia</code> / <code>exchange</code> trong fls/ = 0", "từng ô = Report GL AS-IS"),
    "SO.CFA1": ("<code>Report I CFA1 Daily</code> · <code>Y H Q M</code> (409–410).", "Khối CF: KRF × LE × kỳ.", "bảng khối SO (mới)", "Σ ngày = Σ Y·H·Q·M · từng ô = 409–410"),
    "SO.PLA3": ("PLA1 PM-only · PLA3 HR-only · CFA3 · PLA3 PM + HR (407–408 · 411–419).", "Khối P&amp;L theo KRF trước phân bổ.", "bảng khối SO (mới)", "từng ô = 411–419"),
    "AL.KEY": ("NON-HR 511–513: By LE · By NOEM · By GI.", "Phân bổ theo bảng tỷ trọng.", "<code>fls/ledger/</code> (mới) — từ vựng By GI (8) · By NOEM (5) đã có ở mapping_master", "Σ phần chia = tiền GD"),
    "AL.PLT": ("500–510: [Import] Report GL + Source (Looker) + Vendor &amp; Network Mapping → CFA1 | GI Platform Data Ledger → CFA2 MID 1–3.",
               "Mapping Block 1: Vendor ↔ Network ↔ CDT1; chia ×7 CDT1.", "mới — <code>allocate.py</code> hiện chỉ là cột AU", "Σ % CDT1 = 100 · Σ phần chia = tiền"),
    "SO.PLA3-ATL": ("600–604 · 606: CFA2 MID 3 ×4 · Allocation Table · <code>Report I PLA3 Y H Q M | PM + HR | ATL</code>.",
                    "Khối P&amp;L sau phân bổ: KRF × CDT1 × kỳ.", "bảng khối SO (mới)", "từng ô = 606"),
    "RP.CF": ("<code>5. Daily Report 2</code> (610).", "Daily Report 2 · CF · Group · LE (Templ 5).", "<code>fls/xuat/</code> (mới)", "từng ô = 610"),
    "RP.PL": ("<code>[FS1]/[FS2] 5. Daily Report 3</code> (605 · 607–609).", "Daily Report 3 · P&amp;L · Group · CDT1.", "<code>fls/xuat/</code> (mới)", "từng ô = 609"),
    "KS.CA": ("—", "Σ theo LE = Σ theo nguồn · Σ ngày = Σ Y·H·Q·M.", "<code>fls/kiem/</code> (mới)", "cổng đỏ được chứng minh"),
    "KS.AL": ("—", "Σ phần chia = tiền GD · Σ % CDT1 = 100.", "<code>fls/kiem/</code> (mới)", "cổng đỏ được chứng minh"),
    "IX.FX": ("<code>9.2.Exchange Rate</code> (405 · 614).", "Tỷ giá tháng · chiều ASD · kỳ Day/Y/H/Q/M.", "bảng cấu hình (mới)", "tỷ giá = 9.2 theo tháng"),
    "IX.MB": ("<code>Vendor &amp; Network Mapping</code> (503).", "Mapping Block · tỷ trọng LE · NOEM · GI.", "bảng cấu hình (mới)", "0 vendor không có CDT1"),
    "IX.TMP": ("Templ 1–5 (PD590) · Filters (PD510) · kỳ (PD520) · KRF (PD530).", "Khuôn báo cáo có version.", "bảng cấu hình (mới)", "khuôn = file mẫu AS-IS"),
}
assert set(TRUY) | set(DE_XUAT) == set(HOP), sorted(set(HOP) ^ (set(TRUY) | set(DE_XUAT)))
assert all(trang_thai(m)[0] in ("built", "partial") for m in TRUY), [m for m in TRUY if trang_thai(m)[0] == "miss"]
assert all(trang_thai(m)[0] == "miss" for m in DE_XUAT), [m for m in DE_XUAT if trang_thai(m)[0] != "miss"]


def bang_truy(ds: list[str]) -> str:
    rows = []
    for m in ds:
        now, tobe, code, sod, con = TRUY[m]
        k, nhan = trang_thai(m)
        rows.append([f'<b class="nw">{m}</b><br>{E(HOP[m].ten)}<br><span class="badge {k}">{nhan}</span><br><span class="nw">{E(V.agent_cua(HOP[m]) if hasattr(V, "agent_cua") else "")}</span>',
                     f"{now}<br><span class='nw'>PD Now:</span><br>{pd_html(m)}", tobe, code, sod, ul(con)])
    return bang([("hộp", 11), ("NOW · công thức · script · bước PD", 27), ("TO-BE · phép tính", 17),
                 ("CODE · tệp · test", 19), ("số đối chiếu", 12), ("còn lại cho agent", 14)], rows)


def bang_de_xuat(ds: list[str]) -> str:
    rows = []
    for m in ds:
        now, tobe, code, dc = DE_XUAT[m]
        rows.append([f'<b class="nw">{m}</b><br>{E(HOP[m].ten)}<br><span class="badge miss">PROPOSED</span>',
                     f"{now}<br><span class='nw'>PD Now:</span><br>{pd_html(m)}", tobe, code, dc])
    return bang([("hộp", 13), ("NOW · công thức · script · bước PD", 33), ("TO-BE dự kiến", 20), ("CODE đích", 17), ("đối chiếu", 17)], rows)


# ═════════════════ FIGURE 2.2 · MA TRẬN THÁNG × LOẠI DỮ LIỆU ═════════════════
KY = SL["ky"]
TK = SL["theo_ky"]


def _m(ky: str) -> str:
    y, m = ky.split("-")
    return f"{m}/{y[2:]}"


def o_cell(lines: list[tuple[str, str]], lop: str = "") -> str:
    return f'<td class="vo {lop}">' + "".join(f'<div><span>{a}</span><b>{b}</b></div>' for a, b in lines) + "</td>"


def lop_ty(a: int, b: int) -> str:
    if not b:
        return "vo-na"
    r = a / b
    return "vo-ok" if r >= 0.999 else ("vo-mid" if r >= 0.95 else "vo-no")


def ma_tran() -> str:
    t = SL["tong"]
    hang = []
    # ① BANK · QUỸ — giao dịch trong sổ ITL (dòng)
    r = ['<th class="vo-h"><b>BANK · QUỸ</b><br>giao dịch trong sổ ITL<br><i>đơn vị: dòng</i></th>']
    for k in KY:
        x = TK[k]
        r.append(o_cell([("có", so(x["co"])), ("chạy", so(x["chay"])), ("map", f'{so(x.get("map_now", 0))} · {so(x.get("map_fls", 0))}'),
                         ("sửa", "–")], lop_ty(x["chay"], x["co"])))
    r.append(o_cell([("có", so(t["co"])), ("chạy", so(t["chay"])), ("map", f'{so(t["map_now"])} · {so(t["map_fls"])}'), ("sửa", "⛔")], "vo-sum"))
    hang.append("".join(r))
    # ② ITL ADJUST — 7 khối vùng R–AT (ô)
    r = ['<th class="vo-h"><b>ITL ADJUST</b><br>7 khối vùng R–AT<br><i>đơn vị: ô</i></th>']
    for k in KY:
        x = TK[k]
        r.append(o_cell([("có", so(7 * x["co"])), ("chạy", so(x["o_parity"])), ("map", so(x["o_parity_khop"])),
                         ("sửa", f'{so(x["o_go_that"])} · {so(x["o_mac_dinh"])}')], lop_ty(x["o_parity_khop"], x["o_parity"])))
    r.append(o_cell([("có", so(7 * t["co"])), ("chạy", so(t["o_parity"])), ("map", so(t["o_parity_khop"])),
                     ("sửa", f'{so(t["o_go_that"])} · {so(t["o_mac_dinh"])}')], "vo-sum"))
    hang.append("".join(r))
    # ③ PAY — PM line
    p = SL["pm_tong"]
    r = ['<th class="vo-h"><b>PAY</b><br>PM line (sổ cái FPS)<br><i>đơn vị: line</i></th>']
    for k in KY:
        r.append(o_cell([("có", "–"), ("chạy", "–"), ("map", so(TK[k]["pm_noi"])), ("sửa", "–")], "vo-part"))
    r.append(o_cell([("có", so(p["so_dong_pm"])), ("chạy", so(p["so_dong_pm"])), ("map", so(p["pm_noi_tong"])), ("sửa", "⛔")], "vo-sum"))
    hang.append("".join(r))
    # ④–⑥ chưa có nguồn trong FLS
    for ten, phu, tong in (("HR", "H1000 · lương<br><i>đơn vị: dòng lương</i>", "~34 tệp đã adjust · 0 mã"),
                           ("PLT", "GI · OMC · SC · PS<br><i>đơn vị: dòng chi phí</i>", "4 sổ H2.2025 · 0 mã"),
                           ("CCR", "số dư ngày TK · quỹ<br><i>đơn vị: TK × ngày</i>", "2 sheet · chỉ đo, ⛔ chụp")):
        r = [f'<th class="vo-h"><b>{ten}</b><br>{phu}</th>']
        r += ['<td class="vo vo-na">–</td>'] * len(KY)
        r.append(f'<td class="vo vo-sum vo-na">{tong}</td>')
        hang.append("".join(r))
    head = ('<tr><th class="vo-h">loại dữ liệu ↓ · tháng →</th>' + "".join(f"<th>{_m(k)}</th>" for k in KY) + "<th>Σ 23 kỳ</th></tr>")
    return ('<div class="tw vo-khung"><table class="grid vo-bang" data-figure="2.2">' + head
            + "".join(f"<tr>{x}</tr>" for x in hang) + "</table></div>")


def khoi_thang() -> str:
    ten = {"hd": "1 · HD (Budget Code)", "pay_type": "2 · Loại giao dịch", "cdt1": "3 · CDT1 (chủ dự toán)", "svc_start": "4 · Bắt đầu DV",
           "svc_end": "5 · Kết thúc DV", "id_payee": "6 · ID đối tác", "invoice": "7 · Hoá đơn"}
    kt = SL["khoi_theo_ky"]
    rows = []
    for kh, nhan in ten.items():
        r = [f'<th class="vo-h"><b>{nhan}</b></th>']
        sg = sm = 0
        for k in KY:
            g, mmd = kt[k][kh]
            sg, sm = sg + g, sm + mmd
            r.append(f'<td class="vo"><div><span>gõ</span><b>{so(g)}</b></div><div><span>mđ</span><b>{so(mmd)}</b></div></td>')
        r.append(f'<td class="vo vo-sum"><div><span>gõ</span><b>{so(sg)}</b></div><div><span>mđ</span><b>{so(sm)}</b></div></td>')
        rows.append("".join(r))
    head = '<tr><th class="vo-h">khối ↓ · tháng →</th>' + "".join(f"<th>{_m(k)}</th>" for k in KY) + "<th>Σ</th></tr>"
    return ('<div class="tw vo-khung"><table class="grid vo-bang" data-figure="2.4">' + head
            + "".join(f"<tr>{x}</tr>" for x in rows) + "</table></div>")


def pheu() -> str:
    """Figure 2.3 — voi số lượng Σ: hai làn (BANK dòng · ADJUST ô), bốn cột CÓ → CHẠY → MAP → SỬA; mũi tên ngang."""
    t = SL["tong"]
    co_o = 7 * t["co"]
    lan = [("BANK · QUỸ (dòng)", [("CÓ", t["co"], t["co"], "dòng sổ AS-IS"), ("CHẠY", t["chay"], t["co"], "FLS dựng 1-1"),
                                  ("MAP NOW", t["map_now"], t["co"], "VLOOKUP trả mã"), ("MAP FLS", t["map_fls"], t["co"], "ghép A·B·C")]),
           ("ITL ADJUST (ô)", [("CÓ", co_o, co_o, "ô 7 khối"), ("CHẠY", t["o_parity"], co_o, "ô FLS tính lại"),
                               ("KHỚP", t["o_parity_khop"], co_o, "ô = Final AS-IS"), ("SỬA", t["o_go_that"] + t["o_mac_dinh"], co_o,
                                                                                         f"gõ {so(t['o_go_that'])} · mđ {so(t['o_mac_dinh'])}")])]
    W, X0, CW, GAP, Y0, LH = 1180, 190, 210, 40, 40, 110
    o = [f'<svg viewBox="0 0 {W} {Y0 + 2 * LH + 10}" width="100%" role="img" aria-label="Figure 2.3 voi số lượng tổng">',
         '<defs><marker id="m23" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0 0L10 5L0 10z" fill="#374151"/></marker></defs>']
    for i, (nhan, cot) in enumerate(lan):
        y = Y0 + i * LH
        o.append(f'<rect x="8" y="{y}" width="{X0 - 24}" height="{LH - 20}" rx="6" fill="#f3f4f6" stroke="#d1d5db"/>'
                 f'<text x="18" y="{y + 48}" font-size="13" font-weight="700" fill="#1f2937">{E(nhan)}</text>')
        for j, (ten, n, mau, ghi) in enumerate(cot):
            x = X0 + j * (CW + GAP)
            w = max(6, (CW - 20) * n / mau)
            o.append(f'<rect class="box" x="{x}" y="{y}" width="{CW}" height="{LH - 20}" rx="6" fill="#fff" stroke="#9ca3af"/>'
                     f'<text x="{x + 10}" y="{y + 18}" font-size="11" font-weight="700" fill="#b14a23">{ten}</text>'
                     f'<text x="{x + 10}" y="{y + 40}" font-size="17" font-weight="700" fill="#111827">{so(n)}</text>'
                     f'<text x="{x + CW - 10}" y="{y + 40}" font-size="11" text-anchor="end" fill="#374151">{pt(n, mau)}</text>'
                     f'<rect x="{x + 10}" y="{y + 50}" width="{CW - 20}" height="8" rx="3" fill="#e5e7eb"/>'
                     f'<rect x="{x + 10}" y="{y + 50}" width="{w:.1f}" height="8" rx="3" fill="#E57347"/>'
                     f'<text x="{x + 10}" y="{y + 78}" font-size="10.5" fill="#4b5563">{E(ghi)}</text>')
            if j:
                xa = x - GAP
                o.append(f'<line x1="{xa + 2}" y1="{y + 45}" x2="{x - 4}" y2="{y + 45}" stroke="#374151" stroke-width="1.5" marker-end="url(#m23)"/>')
    o.append("</svg>")
    return "".join(o)


def vong_agent() -> str:
    """Figure 1.3.1 — vòng 4 bước của một gói việc; mũi tên ngang trong một làn, ⛔ mũi tên vòng ngược."""
    buoc = [("① ĐỌC NOW", "agent fls-ba", ["công thức Gsheet", "(valueRenderOption=FORMULA)", "+ script GScript / Apps Script"]),
            ("② TÍNH TO-BE", "agent fls-ba → WO", ["luật thành hàm thuần", "+ số mong theo tháng", "(Figure 2.2)"]),
            ("③ CODE", "agent fls-dev", ["TDD trên ảnh đóng băng", "fls/ · tools/ · test", "cổng chứng minh ĐỎ"]),
            ("④ ĐỐI CHIẾU", "agent fls-test → KQ", ["do_voi_so_luong · cong_parity", "ô ⛔ → số; lệch ⇒", "quay lại ① với lý do"])]
    W, CW, GAP, Y = 1180, 250, 60, 20
    o = [f'<svg viewBox="0 0 {W} 150" width="100%" role="img" aria-label="Figure 1.3.1 vòng một gói việc">',
         '<defs><marker id="m131" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         '<path d="M0 0L10 5L0 10z" fill="#374151"/></marker></defs>']
    for j, (ten, ai, dong) in enumerate(buoc):
        x = 20 + j * (CW + GAP)
        o.append(f'<rect class="box" x="{x}" y="{Y}" width="{CW}" height="112" rx="8" fill="#fef3e8" stroke="#E57347"/>'
                 f'<text x="{x + 12}" y="{Y + 22}" font-size="13" font-weight="700" fill="#b14a23">{ten}</text>'
                 f'<text x="{x + 12}" y="{Y + 40}" font-size="11" font-style="italic" fill="#4b5563">{E(ai)}</text>'
                 + "".join(f'<text x="{x + 12}" y="{Y + 62 + 16 * i}" font-size="11.5" fill="#1f2937">{E(d)}</text>' for i, d in enumerate(dong)))
        if j:
            o.append(f'<line x1="{x - GAP + 2}" y1="{Y + 56}" x2="{x - 4}" y2="{Y + 56}" stroke="#374151" stroke-width="1.6" marker-end="url(#m131)"/>')
    o.append("</svg>")
    return "".join(o)


# ═════════════════ FIGURE 1.1 · voi NOW ↔ TO-BE: SVG + CSS của voi v2, đổi var(--…) sang hex (§A.31) ═════════════════
def css_voi() -> str:
    css = V.CSS
    goc = re.search(r":root\{(.*?)\}", css, re.S).group(1)
    bien = dict(re.findall(r"--([\w-]+):\s*([^;]+);", goc))
    bien["sans"] = "-apple-system,Segoe UI,sans-serif"
    bien["mono"] = "ui-monospace,SFMono-Regular,Menlo,monospace"
    than = re.sub(r"@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    than = re.sub(r":root[^{]*\{[^{}]*\}", "", than)
    than = re.sub(r"/\*.*?\*/", "", than, flags=re.S)
    giu = ("svg", ".ag-", ".buoc-", ".hop", ".chip", ".hang", ".nhom", ".khung", ".cot-", ".plan", ".nguoi", ".ten", ".mui", ".hit",
           ".ben", ".tang2", ".ra-ngoai", ".tach", ".tt-")
    out = []
    for sel, decl in re.findall(r"([^{}]+)\{([^{}]*)\}", than):
        sels = [s.strip() for s in sel.split(",") if s.strip()]
        if not sels or not all(s.startswith(giu) or s.startswith("#hinh-khung svg") for s in sels):
            continue
        if ".khung-ct" in sel or ".zoom" in sel:
            continue
        d = re.sub(r"var\(--([\w-]+)\)", lambda m: bien[m.group(1)].strip(), decl)
        assert "var(" not in d, d
        out.append(",".join(".voi " + s.replace("#hinh-khung ", "") for s in sels) + "{" + d + "}")
    return "\n".join(out)


def svg_voi() -> str:
    s = V.svg()
    return s.replace(f'width="{V.W_ALL}" height="{V.H}"', 'width="100%"', 1)


# ═════════════════ CÁC PHẦN ═════════════════
def header() -> str:
    lich_su = [("v2.4", "2026-11-12", "STANDARD INPUT đủ 4 họ — PLT vào SI (bình luận owner)."),
               ("v2.3.1", "2026-11-12", "Agent 4 về đúng làn bên TO-BE."),
               ("v2.3", "2026-11-12", "Gộp NOW và TO-BE vào một sơ đồ, đặt cạnh nhau."),
               ("v2.2", "2026-11-12", "NOW ↔ TO-BE từ RAW tới ITL Adjust, ghép 1-1 theo output."),
               ("v2.1", "2026-11-12", "Trục ngang theo agent, bỏ chữ ACTUAL, thêm zoom."),
               ("v2", "2026-11-11", "Vẽ lại theo kiến trúc FPA, chưa gộp vào artifact chính.")]
    hist = "".join(f'<tr><th style="white-space:nowrap;vertical-align:top">{v}</th><td>{d} · {E(t)}</td></tr>' for v, d, t in lich_su)
    return f"""<table class="hdr">
<tr><th>Component</th><td>FLS · Voi v2 — đối chiếu NOW (Google Sheets) ↔ TO-BE (FLS) theo agent × bước FPA, kèm Voi số lượng dữ liệu</td></tr>
<tr><th>Version</th><td>2.5.0 · {NGAY}</td></tr>
<tr><th>Status</th><td><span class="badge tbd">DRAFT</span> mọi mục là <code>draft</code> hoặc <code>review</code>; chỉ owner đặt <code>approved</code> (§1.4).</td></tr>
<tr><th>Owner · operator · duyệt</th><td>Owner <b>ThuongCT</b> · operator <b>KhanhCQ</b> · duyệt độc lập <b>Lanptn</b> · thi hành: agent <code>fls-ba</code> · <code>fls-dev</code> · <code>fls-test</code> (phiếu WO / BG / KQ)</td></tr>
<tr><th>Related</th><td>Voi FLS-tobe-phase1 v0.9.1 (<code>Voi-FLS-tobe-phase1.html</code>) · <code>AP_FLS_FleetEval_v1.3.0_2026-11-09.html</code> · <code>architecturepack_FLS_v1.0.0_current-state_2026-09-17.html</code></td></tr>
<tr><th>Changes in v2.5.0</th><td>Dựng lại bản nháp Voi FLS v2.4 thành AP đầy đủ theo skill apr-build-ap: thêm Voi số lượng dữ liệu (Part 2: ma trận 23 tháng × 6 loại dữ liệu, mỗi ô bốn số có · chạy · mapping · sửa, sinh bởi <code>tools/do_voi_so_luong.py</code>); truy vết NOW → TO-BE → code cho 31 hộp (Part 3 phần đã có · Part 5 phần đề xuất); vòng giao việc cho agent (§1.3); Userflows · Acceptance · lưới đối chiếu (Part 4); trạng thái đồng thuận từng mục. Nội dung §0–§7 của v2.4 giữ nguyên ý, đổi số theo bảng §1.5.2.</td></tr>
<tr><th style="vertical-align:top">Lịch sử sửa đổi</th><td><details><summary><b>6 sửa đổi trước đó</b> — v2 → v2.4 (bản nháp, ⛔ AP)</summary><table style="margin-top:8px">{hist}</table></details></td></tr>
</table>"""


def p1() -> str:
    comp = [("RI · PR", "Agent 1 · Agent 2 — chụp nguồn thô, dựng dòng chuẩn", "§3.1 · §3.2 · §5.1"),
            ("SI", "STANDARD INPUT — ghép (Agent 2) · sổ ITL hiệu lực (Agent 3)", "§3.3"),
            ("CA · SO · AL", "mã tất định — quy đổi, khối KRF × kỳ, phân bổ", "§5.2"),
            ("DW · RP", "kho FLS · báo cáo · màn hình", "§3.5 · §5.3"),
            ("KS · IX", "Agent 4 · Auditor (cổng mỗi bước) · cấu hình", "§2 · §3.4 · §5.3")]
    ngu = [[f"<b>{a}</b>", E(b), c, d] for a, b, c, d in (
        ("RI", "RAW INPUT — chụp nguồn thô, đóng băng", "PD 1xx", "RI.BANK · RI.PAY · RI.HR · RI.PLT"),
        ("PR", "PREPARE — dựng dòng chuẩn từ ảnh", "PD 2xx", "PR.BANK · PR.PAY · PR.HR · PR.PLT"),
        ("SI", "STANDARD INPUT — ghép + sổ ITL hiệu lực", "PD 3xx", "SI.MAP · SI.ITL"),
        ("CA · SO", "CALCULATE · STANDARD OUTPUT (trước / sau phân bổ, đuôi -ATL)", "PD 4xx · 409–419 · 600–606", "CA.GL · SO.CFA1 · SO.PLA3 · SO.PLA3-ATL"),
        ("AL · DW · RP · KS · IX", "ALLOCATE · kho · báo cáo · cổng Agent 4 · cấu hình", "PD 5xx · 6xx", "AL.KEY · DW · RP.CCR · KS.SI · IX.FX"))]
    return "\n".join([
        part(1, "SYSTEM · khung, voi và cách giao việc"),
        h(2, "s1-1", "§1.1 SYSTEM: Voi NOW ↔ TO-BE — hình chính", "draft", True),
        "<p>Một hình, chung hàng họ dữ liệu: nửa trái là luồng Google Sheets hôm nay (NOW) tới ITL Adjust; nửa phải là TO-BE theo agent × bước FPA. "
        "Mọi heading sau đây mở bằng tên một thành phần trên hình (RI · PR · SI · CA · SO · AL · DW · RP · KS · IX) hoặc <code>SYSTEM</code>.</p>",
        cap("1.1", "SYSTEM", "Voi FLS v2 — NOW bên trái tới ITL Adjust, TO-BE bên phải; hàng = họ dữ liệu, cột = bước.",
            ["Sinh từ <code>docs/ITL/_tools/sinh_voi_v2.py</code> (nguồn sự thật của hộp, mũi tên, bước PD Now); AP import, ⛔ chép.",
             f"Máy kiểm lúc sinh: {len(V.HOP)} hộp · {len(V.TEN)} mũi tên, mũi tên nằm ngang, ⛔ cắt qua hộp; mã mỗi hộp nói đúng bước của cột chứa nó.",
             "Nhãn NGƯỜI / TAY = có tay người · chip RI-1 … SI-4 = output, cùng mã ở hai bên là cùng một output.",
             "✅ có mã · ◐ một phần · ⛔ chưa có mã — trục <b>dựng</b>, khác trục <b>đồng thuận</b> của heading (§1.4.1)."]),
        f'<div class="tw voi">{svg_voi()}</div>',
        h(3, "s1-1-1", "§1.1.1 SYSTEM: chỉ mục thành phần"),
        bang([("thành phần", 16), ("là gì", 54), ("chi tiết ở", 30)], [[f"<b>{a}</b>", E(b), c] for a, b, c in comp]),
        h(3, "s1-1-2", "§1.1.2 SYSTEM: ngữ pháp tên — đọc tên là biết ô ở đâu"),
        "<p>Mỗi hộp có mã <b>bước + \".\" + phần</b> (như FPA ghép mã bước vào tên); máy kiểm: mã bước trong tên phải trùng bước của cột chứa hộp.</p>",
        bang([("mã bước", 16), ("bước · làm gì", 40), ("PD Now", 18), ("ví dụ", 26)], ngu),
        h(2, "s1-2", "§1.2 SYSTEM: mục tiêu, phạm vi và vai", "draft", True),
        h(3, "s1-2-1", "§1.2.1 SYSTEM: mục tiêu và ngoài phạm vi"),
        "<p>AP này là bản giao việc: mỗi hộp TO-BE có đủ <b>NOW</b> (công thức Gsheet, script, bước PD Now) → <b>TO-BE</b> (phép tính) → <b>code</b> (tệp, test) → <b>số đối chiếu</b>.</p>",
        ul(["<b>Trong phạm vi:</b> 31 hộp của Figure 1.1; 116 bước PD Now (103 vào hộp, 13 ngoài GĐ1 có lý do — §5.4); Voi số lượng dữ liệu theo tháng (Part 2).",
            "<b>Ngoài phạm vi:</b> báo cáo HR từ EDD (102 · 611 · 612) · AP / AR (223 · 224 · 310–312, AS-IS \"Not yet\") · OTHERS 700–702 — chờ owner (§5.5).",
            "<b>⛔ ghi gì vào sổ thật:</b> AP chỉ đọc ảnh đóng băng và mã; mọi cú ghi đi qua <code>FLS_CHO_GHI_THAT=1</code> + cờ duyệt như cũ."]),
        h(3, "s1-2-2", "§1.2.2 SYSTEM: vai"),
        bang([("vai", 20), ("ai", 26), ("làm gì với AP này", 54)], [
            ["owner", "<b>ThuongCT</b>", "chốt định nghĩa bốn số (§2.1) và các câu §5.5; đặt <code>approved</code>"],
            ["operator", "<b>KhanhCQ</b>", "chọn hộp, phát WO cho agent, chạy cổng, cập nhật AP theo phiên bản mới"],
            ["duyệt độc lập", "<b>Lanptn</b>", "soát vòng đối chiếu (UF-1 bước 5) và số trong Figure 2.2"],
            ["agent", "<code>fls-ba</code> · <code>fls-dev</code> · <code>fls-test</code>", "đọc NOW → viết luật → code → đối chiếu; nói với nhau chỉ qua phiếu WO / HOI·TL / BG / KQ"],
            ["kế toán", "AnhMC · NgaNLT", "xác nhận ô lệch có tên lý do; think-aloud cho persona fleet eval"]]),
        h(2, "s1-3", "§1.3 SYSTEM: giao việc cho agent — ĐỌC NOW → TÍNH TO-BE → CODE → ĐỐI CHIẾU", "review", True),
        "<p>Mỗi gói việc là <b>một hộp</b> của Figure 1.1, chạy đủ bốn bước; một ô của Figure 2.2 đổi từ ⛔ sang số là bằng chứng gói việc xong.</p>",
        h(3, "s1-3-1", "§1.3.1 SYSTEM: vòng bốn bước của một gói việc"),
        cap("1.3.1", "SYSTEM", "một gói việc chạy bốn bước, mỗi bước một agent, giao nhau bằng phiếu.",
            ["Mũi tên chỉ đi trái → phải trong một làn; \"lệch ⇒ quay lại ①\" là một phiếu KQ TRƯỢT, ⛔ một mũi tên.",
             "Bước ④ dùng đúng công cụ của Part 2: <code>tools/do_voi_so_luong.py</code> và <code>fls/oracle/cong_parity.py</code>."]),
        vong_agent(),
        h(3, "s1-3-2", "§1.3.2 SYSTEM: khuôn một gói việc (WO)"),
        bang([("trường", 22), ("nội dung bắt buộc", 50), ("lấy ở đâu", 28)], [
            ["hộp · bước PD Now", "mã hộp + mọi bước PD Now nó thay", "Part 3 / Part 5, cột NOW"],
            ["công thức NGUYÊN VĂN", "đọc bằng <code>valueRenderOption=FORMULA</code>, ⛔ diễn giải lại; script: tên dự án Apps Script + hàm", "Gsheet · Apps Script (agent đọc live)"],
            ["luật TO-BE", "hàm thuần + bảng ca mẫu 3 dòng (đầu · giữa · cuối kỳ)", "spec BA"],
            ["số mong theo tháng", "ô Figure 2.2 mà gói việc phải làm đổi màu, với số NOW của tháng ấy", "Figure 2.2 · <code>voi_so_luong.json</code>"],
            ["cổng", "khai <code>mong</code>, NO khi khác cả hai chiều; chứng minh ĐỎ trước khi tin", "CLAUDE.md Đ5"]]),
        h(3, "s1-3-3", "§1.3.3 SYSTEM: luật cho agent — lấy từ CLAUDE.md, ⛔ nới"),
        ul(["<b>Đ1</b> trước câu phủ định (\"chưa có X\"): grep <code>docs/</code> lẫn <code>fls/</code> + <code>tools/</code>, dán số đếm.",
            "<b>Đ3</b> phép so ra 0 hoặc 100% phải đếm mẫu số trước; mẫu số 0 là KẾT QUẢ.",
            "<b>Đ4</b> mỗi số nói nó đếm gì (dòng · ô · line · tháng) ngay tại chỗ in — Figure 2.2 ghi đơn vị ở đầu hàng.",
            "<b>Riêng tư:</b> <code>Email Address</code> cấm vào kho; <code>Diễn giải</code> · <code>Số chứng từ</code> ⛔ vào ảnh đóng băng; <code>sao_luu/</code> · <code>hien_vat/</code> giữ gitignore.",
            "<b>⛔</b> <code>docker compose down</code>; sổ <code>fls_itl</code> chỉ-thêm (<code>INV-I08</code>)."]),
        h(2, "s1-4", "§1.4 SYSTEM: trạng thái của tài liệu", "draft", True),
        h(3, "s1-4-1", "§1.4.1 SYSTEM: hai trục — đồng thuận và dựng"),
        "<p>Thanh màu bên trái heading là <b>đồng thuận</b> (văn bản đã được chốt chưa); nhãn BUILT · PARTIAL · PROPOSED là <b>dựng</b> (mã có chưa). Hai trục độc lập: một mục có thể đã chốt mà chưa dựng.</p>",
        '<div class="tw"><table class="stlegend"><tr><th>state</th><th>nghĩa</th><th>đếm</th></tr>'
        '<tr><td><span class="stkey" data-st="draft">draft</span></td><td>đã viết, chưa ai chốt</td><td>0 units</td></tr>'
        '<tr><td><span class="stkey" data-st="review">review</span></td><td>có câu hỏi / quyết định chờ người đọc</td><td>0 units</td></tr>'
        '<tr><td><span class="stkey" data-st="approved">approved</span></td><td>owner đã chốt văn bản này (chỉ owner đặt)</td><td>0 units</td></tr>'
        '<tr><td><span class="stkey" data-st="locked">locked</span></td><td>đã chốt và một vòng đã thấy đúng trên bản chạy</td><td>0 units</td></tr>'
        '<tr><td><span class="stkey" data-st="superseded">superseded</span></td><td>giữ làm biên bản, đã thay ở chỗ khác</td><td>0 units</td></tr></table></div>',
        h(3, "s1-4-2", "§1.4.2 SYSTEM: What is outstanding &#8212; 0 units"),
        "<p>Mục chưa <code>approved</code> — tức là mọi mục của bản này, vì phiên dựng ⛔ tự chốt.</p>",
        gap("Mở danh sách mọi mục còn chờ quyết định",
            '<div class="tw"><table><tr><th>Unit</th><th>Title</th><th>State</th><th>Marked</th></tr>\n</table></div>'),
        h(2, "s1-5", "§1.5 SYSTEM: nguồn và đổi số", "draft", True),
        h(3, "s1-5-1", "§1.5.1 SYSTEM: sổ nguồn"),
        gap("Cho máy kiểm: nguồn đã gộp và dấu vân tay (8 nguồn)", bang([("nguồn", 34), ("vai", 14), ("dùng cho", 52)], [
            ["<code>Voi-FLS-v2-nhap.html</code> v2.4 (artifact Voi FLS v2)", "BUILT · gộp", "toàn bộ §0–§7 cũ → Part 1 · 3 · 5"],
            ["<code>docs/ITL/_tools/sinh_voi_v2.py</code> + <code>pdnow_buoc.json</code>", "nguồn sự thật", "Figure 1.1, hộp, mũi tên, 116 bước PD Now"],
            ["<code>tools/do_voi_so_luong.py</code> → <code>voi_so_luong.json</code>", "nguồn sự thật", "Figure 2.2 · 2.3 · 2.4"],
            [f"<code>tests/fixture/itl_ledge_adjustment.json</code> ({SL['nguon']['checksum']['itl_ledge_adjustment.json']})", "ảnh đóng băng 26/08", "sổ AS-IS 9.967 dòng × 7 khối"],
            [f"<code>tests/fixture/classifying_vs_canon.json</code> ({SL['nguon']['checksum']['classifying_vs_canon.json']})", "ảnh 26/08", "ghép dòng sổ ↔ dòng FLS dựng lại"],
            [f"<code>tests/fixture/pm_join.json</code> ({SL['nguon']['checksum']['pm_join.json']})", "ảnh 27/08", "9.992 dòng bank · 3.703 dòng PM"],
            ["<code>fls/ledger/final_rule.py</code> · <code>allocate.py</code> · <code>classifying.py</code>", "mã", "công thức NOW nguyên văn trích ở §3.3"],
            ["<code>docs/ITL/02_BA/Artifacts/Kiem-TOBE-theo-ASIS.md</code>", "biên bản", "khớp / lệch TO-BE ↔ AS-IS, quyết định owner 06/11"]])),
        h(3, "s1-5-2", "§1.5.2 SYSTEM: đổi số từ voi v2.4 sang AP"),
        gap("Cho người cầm link cũ: §0–§7 của v2.4 nằm ở đâu bây giờ (8 dòng)", bang([("v2.4", 20), ("AP v2.5.0", 30), ("ghi chú", 50)], [
            ["§0 ngữ pháp tên", "§1.1.2", "giữ nguyên"], ["§1 con voi", "§1.1 · Figure 1.1", "cùng bộ sinh"],
            ["§2 audit ngược", "§3 cột \"số đối chiếu\"", "gộp theo hộp"], ["§3 vào / ra từng hộp", "Part 3 · Part 5", "thêm cột CODE · còn lại"],
            ["§4 mũi tên", "§3 · §5 (cột NOW)", "khoá đi kèm hộp"], ["§5 phủ PD Now", "§5.4", "giữ số 116/116"],
            ["§6 soát voi AS-IS", "§5.4", "giữ"], ["§7 câu chờ owner", "§5.5", "thêm phương án · được · mất"]])),
    ])


def p2() -> str:
    t = SL["tong"]
    return "\n".join([
        part(2, "KS · Voi số lượng dữ liệu"),
        h(2, "s2-1", "§2.1 KS: bốn số đối chiếu — mỗi số đếm gì", "review", True),
        "<p>Bốn số trong mỗi ô của Figure 2.2. Định nghĩa là một <b>quyết định</b> (đếm khác ⇒ màu khác), nên mỗi số có phương án, được · mất, và điều sẽ làm đổi ý.</p>",
        h(3, "s2-1-1", "§2.1.1 KS: số có · số chạy", "review"),
        bang([("phương án", 18), ("được", 28), ("mất", 30), ("phán", 24)], [
            ["<b>CÓ = dòng sổ AS-IS của kỳ</b>", "đúng thứ kế toán đang đọc; có cho 23 kỳ trên ảnh đóng băng", "là số của một ngày chụp (26/08); kỳ 2026-08 còn đang chạy", '<span class="badge new">RECOMMENDED</span>'],
            ["CÓ = dòng sao kê nguồn", "gần tiền thật nhất", "ảnh sao kê ⛔ mang kỳ trong repo; lẫn dòng ITL đã loại", '<span class="badge tbd">REJECTED</span> — chưa đo được theo tháng'],
            ["<b>CHẠY = dòng FLS dựng lại + ghép 1-1</b>", "đo bằng chính mã FLS trên ảnh, không cần kho", "chưa phải số của kho hôm nay (<code>fls_itl</code> 8.387)", '<span class="badge new">RECOMMENDED</span>'],
            ["CHẠY = dòng <code>fls_itl</code> theo tháng", "số thật của hệ đang chạy", "kho ⛔ chạy ở phiên dựng; cần agent ở máy có kho", '<span class="badge tbd">LATER</span> — gói việc §2.5.3']]),
        "<p><b>Điều sẽ làm đổi ý:</b> khi kho chạy lại và <code>fls_itl</code> theo tháng khác số CHẠY trên ảnh quá 1% ở một kỳ, CHẠY đổi sang số của kho.</p>",
        h(3, "s2-1-2", "§2.1.2 KS: mapping · số đã sửa sai", "review"),
        bang([("phương án", 18), ("được", 28), ("mất", 30), ("phán", 24)], [
            ["<b>MAPPING = hai số NOW · FLS, ⛔ gộp</b>", "thấy ngay NOW báo ghép nhiều hơn FLS vì VLOOKUP không kiểm tiền", "ô dài hơn; người đọc phải biết số nào là của ai", '<span class="badge new">RECOMMENDED</span>'],
            ["MAPPING = chỉ số FLS", "gọn", "mất bằng chứng 968 dòng AS-IS \"đã ghép\" mà tiền không khớp", '<span class="badge tbd">REJECTED</span>'],
            ["SỬA theo dòng (≥1 khối người điền)", "dễ hiểu", f"ra {so(9964)}/{so(t['co'])} — gần như mọi dòng, vô nghĩa", '<span class="badge tbd">REJECTED</span> — đo 13/11'],
            ["<b>SỬA theo ô: gõ thật · mặc định</b>", "tách việc người thật làm khỏi ô nhận mặc định im lặng (trái <code>NFR-I05</code>)", "chỉ đo phía AS-IS; lớp sửa FLS (<code>fls_adjustment</code> 4.428) chưa theo tháng", '<span class="badge new">RECOMMENDED</span>']]),
        "<p><b>Điều sẽ làm đổi ý:</b> owner chốt rằng \"sửa sai\" là lớp sửa của FLS (người sửa trên F01 · F02) — khi ấy SỬA lấy từ <code>fls_adjustment</code> theo tháng, số AS-IS lùi về cột phụ.</p>",
        h(2, "s2-2", "§2.2 KS: ma trận tháng × loại dữ liệu", "review", True),
        cap("2.2", "KS", "23 tháng × 6 loại dữ liệu; mỗi ô bốn số có · chạy · mapping · sửa, đo trên ảnh đóng băng 26–27/08.",
            ["<b>Hàng BANK · QUỸ</b> (dòng): có = dòng sổ ITL Ledge · chạy = FLS dựng lại và ghép 1-1 · map = NOW (VLOOKUP trả mã) · FLS (ghép hình A·B·C) · sửa ⛔ (<code>ref_adjust</code> chưa vào ảnh).",
             "<b>Hàng ITL ADJUST</b> (ô, 7 khối R–AT): có = 7 × dòng · chạy = ô FLS tính lại Final (bỏ ô lỗi, bỏ dòng tự soi loại) · map = ô khớp Final AS-IS · sửa = ô người gõ · ô nhận mặc định.",
             "<b>Hàng PAY</b> (line): ảnh PM ⛔ mang tháng, nên chỉ cột map theo tháng của giao dịch bank nó nối; có · chạy ở cột Σ.",
             "<b>HR · PLT · CCR</b>: ⛔ = chưa có nguồn trong FLS (0 mã) — gói việc ở Part 5.",
             "Màu: xanh = chạy (hoặc khớp) bằng có · vàng ≥ 95% · đỏ &lt; 95% · xám = chưa đo. Dấu – trong ô = chưa đo ở tháng ấy; lý do ở cột Σ và §2.5.3."]),
        ma_tran(),
        h(2, "s2-3", "§2.3 KS: voi số lượng — tổng 23 kỳ theo bước", "draft", True),
        cap("2.3", "KS", "tổng 23 kỳ: từ dòng có tới dòng chạy, ghép, sửa — hai làn BANK (dòng) và ADJUST (ô).",
            ["Thanh cam = tỷ lệ so với ô CÓ cùng làn.",
             f"MAP NOW {pt(t['map_now'], t['co'])} &gt; MAP FLS {pt(t['map_fls'], t['co'])}: VLOOKUP lấy dòng đầu tìm thấy và ⛔ kiểm tiền; FLS đòi Σ tiền trong dung sai.",
             f"SỬA = {so(t['o_go_that'])} ô gõ thật + {so(t['o_mac_dinh'])} ô mặc định; còn {so(t['o_trong'])} ô máy không trả lời mà Final rỗng; {so(t['o_de'])} ô Final ≠ Classifying dù máy có trả lời (đều ở 2026-07)."]),
        pheu(),
        h(2, "s2-4", "§2.4 KS: ô người điền theo khối × tháng", "draft", True),
        cap("2.4", "KS", "7 khối vùng R–AT × 23 tháng; mỗi ô: gõ = giá trị thật người gõ · mđ = nhận mặc định cứng của khối.",
            ["Đây là bảng xếp đơn vị cho agent A3 · Filter Fulfill &amp; Adjust: khối nhiều \"gõ\" là việc người tốn nhất; khối nhiều \"mđ\" là chỗ <code>NFR-I05</code> (⛔ mặc định im lặng) phải được owner chốt.",
             "Khối 4–5 (kỳ DV) không có mặc định cứng (<code>GAP-ORA-06</code>), nên mọi ô điền là \"gõ\"."]),
        khoi_thang(),
        h(2, "s2-5", "§2.5 KS: đọc kết quả và đo lại", "draft", True),
        h(3, "s2-5-1", "§2.5.1 KS: số liệu nói gì"),
        ul([f"<b>Đọc và dựng:</b> FLS dựng lại {so(t['chay'])}/{so(t['co'])} dòng sổ ({pt(t['chay'], t['co'])}); 122 dòng chưa có bản dựng 1-1, rải ở 20/23 tháng — gói việc PR.BANK.",
            f"<b>Tính lại vùng chỉnh tay:</b> {so(t['o_parity_khop'])}/{so(t['o_parity'])} ô Final khớp, 23/23 tháng — luật hai bước MID → Final đúng trên cả sổ.",
            f"<b>Ghép:</b> NOW báo {so(t['map_now'])} dòng có mã, FLS ghép chắc {so(t['map_fls'])} dòng; phần chênh là dòng VLOOKUP trả mã mà tiền không khớp, FLS đưa vào hàng chờ kèm lý do.",
            f"<b>Việc người:</b> {so(t['o_go_that'] + t['o_mac_dinh'])} ô vùng R–AT do người điền — {pt(t['o_mac_dinh'], t['o_go_that'] + t['o_mac_dinh'])} trong số đó là mặc định.",
            "<b>Chưa đo:</b> HR · PLT · CCR · sửa của BANK và PAY — ô xám của Figure 2.2."]),
        h(3, "s2-5-2", "§2.5.2 KS: cách đo lại"),
        gap("Cho máy kiểm: lệnh, cổng và bằng chứng cổng đỏ", ul([
            "<code>python tools/do_voi_so_luong.py</code> (in bảng) · <code>--ghi</code> (ghi <code>docs/ITL/_tools/voi_so_luong.json</code>) · rồi <code>python docs/ITL/_tools/sinh_ap_voi_v2.py</code>.",
            "Cổng khai <code>mong</code> cho 11 số, mỗi số lấy từ bài test đã ghim của chính ảnh ấy: 9.967 dòng · 23 kỳ · 9.845 ghép · 9.992 bank · 3.703 PM · 105 không mã · 6.532 không thấy mã PM · hình A–F · parity 69.510/69.510 · 37 dòng tự soi loại · 3 checksum.",
            "Đã chứng minh ĐỎ 13/11: đổi <code>so_dong_so</code> mong 9.967 → 9.968 trên bản sao ⇒ exit 1, \"số dòng sổ: đo 9967 · mong 9968\"; trả nguyên ⇒ exit 0.",
            "Công cụ ⛔ đọc kho; chạy mã FLS (<code>pm_join.xep_ca_lat</code>, <code>final_rule.tinh_final</code>, <code>tu_soi.soi_mot_dong</code>) lên ảnh."])),
        h(3, "s2-5-3", "§2.5.3 KS: ô chưa đo và ai đo"),
        bang([("ô xám", 22), ("vì sao chưa đo", 38), ("gói việc · ai", 40)], [
            ["CHẠY theo kho (mọi hàng)", "kho <code>fls-pg-1</code> ⛔ chạy ở phiên dựng (cổng 5433 từ chối)", "fls-test ở máy có kho: <code>fls_itl</code> · <code>fls_pm_link</code> · <code>fls_adjustment</code> theo tháng"],
            ["BANK · sửa", "<code>Reference number_adjust</code> chưa vào bản khai / ảnh (<code>GAP-KHAI-02</code>)", "RI.BANK (§3.1) — fls-dev"],
            ["PAY · có · chạy theo tháng", "ảnh PM ⛔ mang ngày", "RI.PAY — thêm ngày duyệt vào ảnh"],
            ["HR · PLT", "0 mã (grep <code>H1000</code> trong fls/ = 1 dòng chú thích; <code>Combine Code</code> = 0)", "RI.HR · PR.HR · RI.PLT · PR.PLT (§5.1)"],
            ["CCR", "chỉ đo bằng <code>tools/do_trong_tai.py</code>, ⛔ chụp", "RI.BANK + KS.SI (DIF)"]]),
    ])


def p3() -> str:
    return "\n".join([
        part(3, "Truy vết NOW → TO-BE → code · phần đã có"),
        h(2, "s3-1", "§3.1 RI: Agent 1 · Collect_raw_data — chụp nguồn", "draft", True),
        "<p>Chỉ hộp đã có mã (BUILT · PARTIAL); phần chưa có ở Part 5. Cột NOW là thứ agent phải đọc lại nguyên văn trước khi sửa mã.</p>",
        bang_truy(["RI.BANK", "RI.PAY"]),
        h(2, "s3-2", "§3.2 PR: Agent 2 · Generate Group Ledger — dựng dòng chuẩn", "draft", True),
        bang_truy(["PR.BANK", "PR.PAY"]),
        h(2, "s3-3", "§3.3 SI: STANDARD INPUT — ghép và sổ ITL hiệu lực", "review", True),
        "<p>Hai hộp này mang công thức NOW đã đọc nguyên văn; AP trích đúng chỗ mã đã ghi (final_rule · allocate · classifying).</p>",
        h(3, "s3-3-1", "§3.3.1 SI: SI.MAP — ghép giao dịch ↔ lệnh (Agent 2)"),
        bang_truy(["SI.MAP"]),
        h(3, "s3-3-2", "§3.3.2 SI: SI.ITL — sổ ITL hiệu lực, 7 khối R–AT (Agent 3)"),
        bang_truy(["SI.ITL"]),
        "<p><b>Câu chờ owner:</b> chuyển SI.MAP từ Agent 3 sang Agent 2 (theo hai file ITL của AS-IS) — xem §5.5.</p>",
        h(2, "s3-4", "§3.4 KS: cổng của Agent 4 và cấu hình đã có", "draft", True),
        bang_truy(["KS.RI", "KS.SI", "KS.RP", "IX.KHAI", "IX.MM"]),
        h(2, "s3-5", "§3.5 DW: kho, màn hình và ghi CCR", "draft", True),
        bang_truy(["DW", "RP.FLS", "RP.CCR"]),
    ])


def p4() -> str:
    uf1 = [["1 · Chọn hộp", "KhanhCQ", "AP <b>§2.2</b> → ô xám / đỏ → hộp ở <b>Part 3 / Part 5</b> → phát <b>WO</b>", "AP v2.5.0 mở được",
            ul(["WO ghi mã hộp + mọi bước PD Now", "WO ghi ô Figure 2.2 sẽ đổi màu"]), ul(["WO chỉ ghi \"làm H1000\", không bước PD", "chọn hộp không có ô nào trên Figure 2.2"]), "AC1"],
           ["2 · Đọc NOW", "fls-ba", "Gsheet → <b>valueRenderOption=FORMULA</b> → chép công thức; Apps Script → tên dự án + hàm", "quyền đọc sheet · dự án script",
            ul(["mỗi bước PD của hộp có công thức nguyên văn", "ca mẫu 3 dòng có giá trị thật"]), ul(["diễn giải lại công thức bằng lời", "đọc giá trị thay công thức (IMPORTRANGE timeout)"]), "AC2"],
           ["3 · Viết luật", "fls-ba", "spec → <b>TL / WO</b> với hàm thuần + số mong theo tháng", "bước 2 xong",
            ul(["số mong lấy từ Figure 2.2", "luật có ca đỏ"]), ul(["không khai mong", "mong chỉ có tổng, không theo tháng"]), "AC3"],
           ["4 · Code", "fls-dev", "<code>fls/</code> · <code>tools/</code> → test trên ảnh đóng băng → <b>BG</b>", "WO MO",
            ul(["bài test ghim số theo tháng", "cổng được chứng minh đỏ"]), ul(["test chỉ \"không lỗi\"", "sửa ảnh đóng băng cho xanh"]), "AC4"],
           ["5 · Đối chiếu", "fls-test", "<code>python tools/do_voi_so_luong.py</code> → <b>KQ</b>; AP sinh lại", "BG chờ kiểm",
            ul(["ô Figure 2.2 đổi từ ⛔ sang số", "lệch có tên lý do"]), ul(["cổng xanh trên tập rỗng", "ô đổi màu mà số Σ không đổi"]), "AC5 · AC6"]]
    uf2 = [["1 · Mở voi số lượng", "ThuongCT", "AP → <b>§2.2</b>", "AP đã đăng",
            ul(["thấy 23 tháng × 6 loại", "đầu hàng ghi đơn vị"]), ul(["ô có số mà không nói đơn vị", "tháng thiếu cột"]), "AC7"],
           ["2 · Soi một ô lệch", "ThuongCT", "ô vàng / đỏ → <b>§2.5.1</b> → hộp ở Part 3", "bước 1",
            ul(["biết ô lệch thuộc hộp nào", "biết agent nào đang làm"]), ul(["ô lệch không trỏ tới hộp", "giải thích chung chung"]), "AC7"],
           ["3 · Chốt định nghĩa", "ThuongCT", "<b>§2.1</b> → chọn phương án → báo KhanhCQ đặt <code>approved</code>", "§2.1 ở review",
            ul(["§2.1 đổi sang approved có ngày", "Figure 2.2 sinh lại theo định nghĩa chốt"]), ul(["tác giả tự đặt approved", "đổi định nghĩa mà số không sinh lại"]), "AC3"],
           ["4 · Chốt câu mở", "ThuongCT", "<b>§5.5</b> → chọn phương án từng câu", "§5.5 ở review",
            ul(["mỗi câu có phán + ngày", "phương án bị bác vẫn còn trong AP"]), ul(["xoá phương án bị bác", "chốt mà không ghi điều làm đổi ý"]), "AC8"]]
    cot = [("bước", 9), ("ai", 7), ("BẤM GÌ · ở đâu", 22), ("điều kiện trước", 12), ("KỲ VỌNG", 20), ("FAIL trông như thế nào", 22), ("probe", 8)]
    ac = [("AC1", "L1", "Mọi 31 hộp của Figure 1.1 có một dòng ở Part 3 hoặc Part 5 với NOW · TO-BE · CODE · đối chiếu.", "UF-1.1",
           f"{len(TRUY)} + {len(DE_XUAT)} = {len(TRUY) + len(DE_XUAT)}/31 · {NGAY} (máy đếm lúc sinh)"),
          ("AC2", "L3", "Mỗi hộp PARTIAL có công thức / script NOW ghi nguyên văn hoặc ghi rõ \"AS-IS không có bước\".", "UF-1.2",
           f"{sum(1 for m in TRUY if '<pre>' in TRUY[m][0] or '<code>' in TRUY[m][0] or '—' in TRUY[m][0])}/{len(TRUY)} · {NGAY}"),
          ("AC3", "L3", "Bốn số có định nghĩa một câu và đơn vị ghi ở đầu hàng Figure 2.2.", "UF-1.3 · UF-2.3", f"4/4 · {NGAY}"),
          ("AC4", "L2", "Mỗi hộp PARTIAL trỏ tới ít nhất một tệp test có thật trong repo.", "UF-1.4",
           f"{sum(1 for m in TRUY if 'test' in TRUY[m][2])}/{len(TRUY)} · {NGAY}"),
          ("AC5", "L5", "Hàng BANK · ADJUST của Figure 2.2 tái hiện được bằng một lệnh, và cổng của lệnh ấy đã được chứng minh đỏ.", "UF-1.5",
           f"exit 0 · đỏ đã thấy · {NGAY}"),
          ("AC6", "L5", "Một hộp chỉ được ghi \"xong\" khi ô của nó trên Figure 2.2 bằng số NOW ở mọi tháng có dữ liệu.", "UF-1.5",
           f"ADJUST 23/23 tháng khớp · BANK 3/23 tháng chạy = có · HR · PLT 0/23 · {NGAY}"),
          ("AC7", "L4", "Từ một ô vàng / đỏ của Figure 2.2, owner tới được hộp và gói việc trong một cú bấm mục lục.", "UF-2.1 · UF-2.2", "chưa đo — chờ ThuongCT đọc"),
          ("AC8", "L4", "Mỗi câu §5.5 có ≥ 2 phương án với được · mất và một dòng \"điều sẽ làm đổi ý\".", "UF-2.4", f"6/6 · {NGAY}")]
    luoi_hang = ["UF-1.1", "UF-1.2", "UF-1.3", "UF-1.4", "UF-1.5", "UF-2.1", "UF-2.2", "UF-2.3", "UF-2.4"]
    lv = ["L1", "L2", "L3", "L4", "L5"]
    o_luoi = []
    for b in luoi_hang:
        cells = []
        for L in lv:
            ids = [a for a, l, _, uf, _ in ac if l == L and b in uf]
            cells.append(f"<td>{' · '.join(ids)}</td>" if ids else '<td class="hole">▢</td>')
        o_luoi.append(f'<tr><td class="lbl">{b}</td>{"".join(cells)}</tr>')
    return "\n".join([
        part(4, "SYSTEM · Userflows và nghiệm thu"),
        h(2, "s4-1", "§4.1 SYSTEM: UF-1 — agent đưa một hộp từ NOW sang code", "review", True),
        "<p>Persona: ba agent dự án dưới operator KhanhCQ. Bước đánh số ổn định — UF-1.4 mang cùng nghĩa ở mọi phiên bản sau.</p>",
        bang(cot, uf1, "uf"),
        h(2, "s4-2", "§4.2 SYSTEM: UF-2 — owner đọc voi số lượng và chốt", "review", True),
        bang(cot, uf2, "uf"),
        h(2, "s4-3", "§4.3 SYSTEM: nghiệm thu", "review", True),
        "<p>Mỗi câu thấy được (trang đã render hoặc lệnh chạy), một người kiểm trong vài phút, mang một cấp L1–L5 và nối về bước Userflow.</p>",
        bang([("mã", 6), ("cấp", 6), ("câu", 44), ("bước", 14), ("trạng thái · số · ngày", 30)], [[f"<b>{a}</b>", l, c, uf, s] for a, l, c, uf, s in ac]),
        h(2, "s4-4", "§4.4 SYSTEM: lưới đối chiếu bước × cấp", "draft", True),
        cap("4.4", "SYSTEM", "mỗi bước Userflow × năm cấp L1–L5; ô là mã câu nghiệm thu, ▢ = lỗ.",
            ["Mọi hàng có ít nhất một câu; mọi câu phủ ít nhất một bước (AC1–AC8 đều xuất hiện).",
             "Ô ▢ là lỗ thật, để nguyên cho người đọc và agent cùng thấy — không có cấp nào trống hẳn."]),
        '<div class="tw"><table class="grid"><tr><th>bước</th>' + "".join(f"<th>{L}</th>" for L in lv) + "</tr>" + "".join(o_luoi) + "</table></div>",
    ])


def p5() -> str:
    phu = V.bang_phu() if hasattr(V, "bang_phu") else ""
    phu = re.sub(r'class="io"', 'class="io5"', phu)
    asis = re.sub(r'class="io"', 'class="io5"', V.bang_asis()) if hasattr(V, "bang_asis") else ""
    q = [("Ngữ pháp tên <code>RI·PR·SI·CA·SO·AL·DW·RP·KS·IX</code> + đuôi <code>-ATL</code>",
          "A · giữ — đọc tên là biết bước; máy kiểm được", "phải dạy người đọc 10 mã", "B · tên tiếng Việt theo hộp v0.9", "dễ đọc lúc đầu", "không kiểm bằng máy được; lệch với FPA",
          "A", "nếu FPA đổi ngữ pháp mã bước"),
         ("Chuyển ghép Ref No (SI.MAP, PD 302–308) từ Agent 3 sang Agent 2",
          "A · chuyển — khớp đúng hai file ITL của AS-IS (1/2 RAW · 2/2 ADJUSTED)", "Agent 2 nặng hơn; fleet eval A3.1 đổi tên đơn vị", "B · giữ ở Agent 3 như v0.9", "không đổi AP fleet eval", "một agent ôm cả ghép lẫn điền tay, khó đo riêng",
          "A", "nếu fleet eval cho thấy ghép và điền tay cần cùng ngữ cảnh"),
         ("HR ⛔ qua ALLOCATE; báo cáo HR 102 · 611 · 612 ngoài GĐ1",
          "A · giữ — PD 500: HR đã phân bổ ở payroll", "báo cáo HR vẫn ở EDD", "B · đưa HR qua ALLOCATE", "một đường cho mọi chi phí", "phân bổ hai lần",
          "A", "nếu payroll ngừng phân bổ HD · CDT1"),
         ("Kho: PostgreSQL chỉ-thêm, hay đẩy khối SO lên BigQuery như FDW của FPA",
          "A · PostgreSQL cho sổ, BigQuery chỉ cho khối SO", "hai kho phải đồng bộ", "B · chỉ PostgreSQL", "một kho, đã có", "REPORT không dùng chung với FPA",
          "B trước, A khi REPORT cần", "khi báo cáo FPA phải đọc khối SO của FLS"),
         ("AP / AR (223 · 224 · 310–312, AS-IS \"Not yet\")",
          "A · GĐ2", "không mở việc mới trong 10 ngày Phase 1", "B · GĐ1", "đủ luồng tiền", "AS-IS còn chưa làm, không có đáp án để đối chiếu",
          "A", "nếu AS-IS bắt đầu chạy AP / AR"),
         ("Định nghĩa bốn số của Voi số lượng (§2.1)",
          "A · như §2.1 (CÓ = sổ AS-IS · CHẠY = FLS dựng 1-1 · MAP hai số · SỬA theo ô)", "chưa là số của kho", "B · mọi số lấy từ kho", "số của hệ đang chạy", "chưa đo được hôm nay",
          "A, đổi sang B khi kho chạy", "khi kho lệch ảnh &gt; 1% ở một kỳ")]
    qrows = []
    for i, (a, b1, m1, b2, p2, m2, w, f) in enumerate(q):
        qrows.append([f"<b>Q{i + 1}</b> {a}", f"<b>{b1}</b><br><i>mất:</i> {m1}", f"<b>{b2}</b><br><i>được:</i> {p2}<br><i>mất:</i> {m2}",
                      f'<span class="badge new">RECOMMENDED</span> {w}', f])
    return "\n".join([
        part(5, "SYSTEM · Đề xuất chưa dựng, phủ PD Now, câu chờ owner"),
        h(2, "s5-1", "§5.1 RI: Proposed — not built · họ HR và PLT ở Agent 1 · 2", "draft", True, ("miss", "PROPOSED")),
        "<p>Phần này chỉ chứa hộp ⛔ có mã (§A.11): thiết kế, chưa dựng. Cùng khuôn với Part 3 để agent nhận gói việc ngay.</p>",
        bang_de_xuat(["RI.HR", "RI.PLT", "PR.HR", "PR.PLT"]),
        h(2, "s5-2", "§5.2 CA: Proposed — not built · CALCULATE, STANDARD OUTPUT, ALLOCATE", "draft", True, ("miss", "PROPOSED")),
        bang_de_xuat(["CA.GL", "SO.CFA1", "SO.PLA3", "AL.KEY", "AL.PLT", "SO.PLA3-ATL"]),
        h(2, "s5-3", "§5.3 RP: Proposed — not built · báo cáo, cổng và cấu hình còn thiếu", "draft", True, ("miss", "PROPOSED")),
        bang_de_xuat(["RP.CF", "RP.PL", "KS.CA", "KS.AL", "IX.FX", "IX.MB", "IX.TMP"]),
        h(2, "s5-4", "§5.4 SYSTEM: phủ 116 bước PD Now và soát voi AS-IS", "draft", True),
        h(3, "s5-4-1", "§5.4.1 SYSTEM: mọi bước PD Now đều có chỗ"),
        f'<div class="tw">{phu}</div>',
        h(3, "s5-4-2", "§5.4.2 SYSTEM: soát voi AS-IS v0.9 theo PD Now"),
        f'<div class="tw">{asis}</div>',
        h(2, "s5-5", "§5.5 SYSTEM: câu chờ owner — phương án, được và mất", "review", True),
        "<p>Mỗi câu: phương án đề xuất (A, có cả cái mất), phương án khác (B, giữ lại kể cả khi bị bác), và điều sẽ làm đổi ý. Owner chốt — tác giả ⛔ tự chốt.</p>",
        bang([("câu", 20), ("A · đề xuất", 25), ("B · phương án khác", 25), ("phán", 14), ("điều sẽ làm đổi ý", 16)], qrows),
    ])


AP_CSS = r"""
/* AP-specific rules (§A.31) */
.voi{overflow-x:auto}
.voi svg{min-width:1600px;height:auto;display:block}
.vo-khung{overflow-x:auto}
table.vo-bang{table-layout:auto;font-size:11px;border-collapse:collapse;min-width:1700px}
table.vo-bang th{position:sticky;top:0;background:#f9fafb;font-size:11px;white-space:nowrap;padding:4px 6px}
table.vo-bang th.vo-h{position:sticky;left:0;z-index:2;background:#fff;text-align:left;min-width:150px;font-weight:400;white-space:normal}
table.vo-bang td.vo{padding:3px 5px;vertical-align:top;white-space:nowrap;border:1px solid #e5e7eb}
table.vo-bang td.vo div{display:flex;justify-content:space-between;gap:6px;line-height:1.35}
table.vo-bang td.vo span{color:#6b7280}
table.vo-bang td.vo b{font-weight:600;color:#111827}
td.vo-ok{background:#ecfdf3} td.vo-mid{background:#fffbeb} td.vo-no{background:#fef2f2}
td.vo-na{background:#f3f4f6;color:#9ca3af;text-align:center} td.vo-part{background:#f8fafc}
td.vo-sum{background:#fef3e8;font-weight:600}
table.io5{width:100%;border-collapse:collapse;font-size:13px}
table.io5 th,table.io5 td{border-bottom:1px solid #e5e7eb;padding:6px 8px;text-align:left;vertical-align:top}
table.io5 .mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
table.io5 tr.b1 th{background:#fef3e8}
pre{white-space:pre-wrap}
.ghichu{color:#6b7280;font-size:13px}
.scroll{overflow-x:auto}
"""


def trang() -> str:
    _cha.clear()
    _st.clear()
    style = (SKILL / "ap-style.css").read_text(encoding="utf-8")
    toc = (SKILL / "ap-toc.js").read_text(encoding="utf-8")
    than = "\n".join([p1(), p2(), p3(), p4(), p5()])
    return f"""<!doctype html>
<!-- AP_FLS-Voi_v2.5.0_Doi-Chieu-NOW-TOBE_2026-11-13.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v2.py · mỗi thay đổi là một tệp mới -->
<html lang="vi"><head>
<meta charset="utf-8">
<meta name="ap:lineage" content="AP_FLS-Voi">
<meta name="ap:branch" content="">
<meta name="ap:version" content="2.5.0">
<meta name="ap:parent" content="">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AP Voi FLS v2.5.0</title>
<style>
{style}
{AP_CSS}
{css_voi()}
</style></head>
<body>
<nav class="toc"><p class="toc-title">Contents</p><div id="toc"></div></nav>
<main>
<h1>AP · Voi FLS v2.5.0 — đối chiếu NOW ↔ TO-BE và Voi số lượng dữ liệu</h1>
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
    print(f"✅ đã ghi {RA.relative_to(GOC)} · {len(s):,} byte · hộp Part 3 {len(TRUY)} · Part 5 {len(DE_XUAT)}")
    return 0


CONG = """
R=/root/.claude/skills/synced/1b8da73f-77c4-495f-89f5-e856b18560a0_5ecf2698-132a-4770-9b6d-414419313b06/apr-build-ap/references
python3 $R/ap-status-check.py <AP> --restamp <mọi id> && python3 $R/ap-status-check.py <AP>
python3 $R/toc-tree-check.py <AP> · python3 $R/figure-section-check.py <AP> · style-check (cần ap-style-pulled.css rỗng cạnh nó)
"""

if __name__ == "__main__":
    raise SystemExit(main())
