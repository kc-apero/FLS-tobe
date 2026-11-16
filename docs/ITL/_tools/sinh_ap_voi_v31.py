# -*- coding: utf-8 -*-
"""Sinh AP Voi FLS v3.1.0 — thêm HOW DONE LOOKS + ACCEPTANCE (minor: ⛔ đổi số mục nào).

⭐ Owner 16/11 (KhanhCQ): "bổ sung thêm How done looks và Acceptance vào AP. HD quan trọng nhất là mapping được
   100%, giống các dữ liệu quá khứ" — HD hiểu là How Done; tiêu chí ấy phủ luôn khối HD (mã ngân sách).

⭐ Cách làm: lấy nguyên v3.0.0 từ `sinh_ap_voi_v3.py` (⛔ chép), rồi:
   · §5.3 (nghiệm thu) thành mục cha "How done looks và Acceptance" với 3 mục con MỚI ở biên: §5.3.1 How done looks ·
     §5.3.2 Acceptance (bảng AC cũ, gom theo cấp L1–L5 + AC10 · AC11) · §5.3.3 Figure 5.3.3 mapping giống quá khứ theo tháng.
   · §5.4 lưới thêm AC10 · AC11.
   · SỬA SỐ SAI tự tôi ghi tay ở v2.5.0/v3.0.0 ("20/23 tháng", "BANK 3/23 tháng") — giờ máy tính từ `voi_so_luong.json`.
   Số mục cũ giữ nguyên ⇒ minor 3.0.0 → 3.1.0; v3.0.0 đóng băng.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DAY = Path(__file__).resolve().parent
sys.path.insert(0, str(DAY))
import sinh_ap_voi_v3 as A3  # noqa: E402

A2 = A3.A2
GOC = A2.GOC
RA = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.0_How-Done-Acceptance_2026-11-16.html"
NGAY = "2026-11-16"
SL = A2.SL
KY, TK, T = SL["ky"], SL["theo_ky"], SL["tong"]
so, pt, E = A2.so, A2.pt, A2.E
TS = SL["tu_sinh"]

DU_DONG = [k for k in KY if TK[k]["chay"] == TK[k]["co"]]
DU_O = [k for k in KY if TK[k]["o_parity_khop"] == TK[k]["o_parity"]]
DU_HD = [k for k in KY if TK[k]["hd_parity_khop"] == TK[k]["hd_parity"]]
THIEU_DONG = len(KY) - len(DU_DONG)


def thay(s: str, a: str, b: str, n: int = 1) -> str:
    k = s.count(a)
    if k != n:
        raise SystemExit(f"⛔ khớp {k} lần (mong {n}): {a[:90]!r}")
    return s.replace(a, b)


def how_done() -> str:
    hd1_hom_nay = (f"dòng ghép 1-1: {so(T['chay'])}/{so(T['co'])} ({pt(T['chay'], T['co'])}) — {len(DU_DONG)}/{len(KY)} tháng đủ · "
                   f"ô Final 7 khối (đọc MID của sổ): {so(T['o_parity_khop'])}/{so(T['o_parity'])} — {len(DU_O)}/{len(KY)} tháng · "
                   f"khối HD: {so(T['hd_parity_khop'])}/{so(T['hd_parity'])} — {len(DU_HD)}/{len(KY)} tháng · "
                   f"tự sinh (FLS tự tính MID từ Manual input): {so(TS['o'][0])}/{so(TS['o'][1])} ô, HD {TS['hd'][0]}/{TS['hd'][1]} — chỉ đo được {TS['ky']}")
    rows = [
        ["<b>HD1 ★</b>", "<b>Mapping 100%, giống dữ liệu quá khứ</b> (owner 16/11): mỗi tháng có dữ liệu, mọi dòng giao dịch của sổ AS-IS có đúng một dòng FLS, "
         "và mọi ô mapping của FLS — khối 1 HD trước hết, rồi đủ 7 khối — bằng Final của sổ đã chốt. Lệch = 0, hoặc mỗi lệch có tên lý do và owner ký.",
         "<code>tools/do_voi_so_luong.py</code> (Figure 2.2 hàng BANK + ADJUST · Figure 5.3.3) · <code>fls/oracle/cong_parity.py</code>",
         hd1_hom_nay,
         f"{so(T['co'] - T['chay'])} dòng chưa dựng 1-1 ở {THIEU_DONG}/{len(KY)} tháng · ảnh Manual input cho {len(KY) - 1} tháng còn lại · họ HR · PLT"],
        ["<b>HD2</b>", "<b>Báo cáo và phân bổ giống quá khứ</b>: mọi ô CFA / PLA · MID3 · Daily Report 2 · 3 của FLS bằng sheet NOW cùng kỳ (cột đáp án của Figure 3.1).",
         "cổng KS.RP từng ô theo gói WP-C2…C5 (§3.5.4)", "0 ô — engine báo cáo, phân bổ chưa dựng", "5 gói việc WP-C1…C5"],
        ["<b>HD3</b>", "<b>Đủ bốn họ dữ liệu</b>: Figure 2.2 không còn ô xám ở BANK · PAY · HR · PLT · CCR.",
         "Figure 2.2", "2/6 hàng có số theo tháng (BANK · ADJUST); PAY có map theo tháng", "lằn Cash · H1000 · nền tảng · CCR (RI.* · PR.*)"],
        ["<b>HD4</b>", "<b>Kế toán làm trên FLS, ⛔ Gsheet</b>: mọi sửa đi qua lớp sửa có actor; GScript gom / duỗi ⛔ còn ai bấm; Gsheet chỉ còn để đối chiếu.",
         "kho: <code>fls_adjustment</code> có actor · log GScript", "6 màn + <code>ghi_tay</code> có; Gsheet vẫn chạy song song", "cắt Gsheet sau HD1 + HD2"],
        ["<b>HD5</b>", "<b>Lặp lại được</b>: một lệnh sinh lại mọi số đối chiếu; mọi cổng đã được chứng minh đỏ; tháng mới tự vào.",
         "<code>python tools/do_voi_so_luong.py --ghi</code> rồi sinh AP", "exit 0; cổng đỏ đã thấy 13/11 và 16/11", "đọc kho (số của <code>fls_itl</code> theo tháng)"]]
    return "\n".join([
        A3.dau(3, "n5-3-1", "§5.3.1 SYSTEM: How done looks — xong trông như thế nào", st="review"),
        "<p><b>Xong</b> = chạy FLS trên mọi tháng quá khứ cho ra đúng sổ kế toán đã chốt, từng dòng, từng ô — rồi mới bật agent. "
        "Năm điều nhìn thấy được; HD1 là điều owner đặt lên đầu.</p>",
        A2.bang([("#", 6), ("nhìn thấy gì khi xong", 34), ("đo bằng", 18), (f"hôm nay (đo {NGAY})", 26), ("còn thiếu", 16)], rows),
        "<p class=\"note\"><b>\"Xong\" ⛔ có nghĩa là có agent.</b> Agent chỉ vào sau khi HD1 và HD2 đạt — khi ấy mới có đáp án sạch để đo agent (cửa G0 → G3 ở Voi phase 1).</p>",
    ])


def acceptance(than_cu: str) -> str:
    hang = re.findall(r"<tr><td><b>(AC\d+)</b></td><td>(L\d)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>", than_cu, re.S)
    if len(hang) != 9:
        raise SystemExit(f"⛔ bảng AC cũ có {len(hang)} dòng (mong 9)")
    hang = [list(h) for h in hang]
    for h in hang:   # sửa số sai ghi tay ở v2.5.0 (AC6)
        if h[0] == "AC6":
            a = "BANK 3/23 tháng chạy = có"
            if a not in h[4]:
                raise SystemExit("⛔ AC6 không có chuỗi cũ")
            h[4] = h[4].replace(a, f"BANK {len(DU_DONG)}/{len(KY)} tháng chạy = có (sửa 16/11: bản trước ghi 3/23)")
    hang += [
        ["AC10", "L5", f"<b>Mapping 100% theo tháng</b> (HD1): với mỗi tháng có dữ liệu quá khứ, dòng FLS ghép 1-1 bằng dòng sổ AS-IS và ô mapping FLS bằng Final AS-IS ở cả 7 khối; "
         "một tháng chỉ ghi \"đạt\" khi cả hai cùng 100%, và chế độ tự sinh (FLS tự tính MID) cũng 100%.", "UF-1.5 · UF-2.2",
         f"dòng {len(DU_DONG)}/{len(KY)} tháng · ô {len(DU_O)}/{len(KY)} tháng · tự sinh 1/1 tháng đo được ({TS['ky']}) · {NGAY}"],
        ["AC11", "L5", "<b>Khối HD trước hết</b>: ô khối 1 HD của FLS bằng Final AS-IS ở mọi tháng, ở cả chế độ đọc MID của sổ lẫn chế độ tự sinh.", "UF-1.5",
         f"đọc MID sổ {so(T['hd_parity_khop'])}/{so(T['hd_parity'])} ô, {len(DU_HD)}/{len(KY)} tháng · tự sinh {TS['hd'][0]}/{TS['hd'][1]} ({TS['ky']}) · {NGAY}"]]
    cap_ten = [("L1 · Reachable · L2 · Executable", ("L1", "L2")), ("L3 · Understandable", ("L3",)), ("L4 · Goal-aligned", ("L4",)), ("L5 · Sufficient", ("L5",))]
    nhom_hang, rows, nhan = [], [], {}
    for ten, lv in cap_ten:
        ds = [h for h in hang if h[1] in lv]
        nhan[len(rows)] = ten
        rows += [[f"<b>{a}</b>", l, c, uf, st] for a, l, c, uf, st in ds]
    assert len(rows) == 11
    return "\n".join([
        A3.dau(3, "n5-3-2", "§5.3.2 SYSTEM: Acceptance — câu nghiệm thu L1–L5", st="review"),
        "<p>Mỗi câu thấy được (trang đã render hoặc lệnh chạy), một người kiểm trong vài phút, mang một cấp L1–L5 và nối về bước Userflow. "
        "Gom theo cấp để mỗi nhóm ≤ 5 câu; AC1–AC9 giữ nguyên từ v3.0.0, AC10 · AC11 mới cho HD1.</p>",
        A2.bang([("mã", 6), ("cấp", 6), ("câu", 44), ("bước", 14), ("trạng thái · số · ngày", 30)], rows, nhom=nhan),
    ])


def hinh_533() -> str:
    def o(a, b):
        if not b:
            return '<td class="vo vo-na">–</td>'
        lop = "vo-ok" if a == b else ("vo-mid" if a / b >= 0.95 else "vo-no")
        return f'<td class="vo {lop}"><div><b>{pt(a, b)}</b></div><div><span>{so(a)}/{so(b)}</span></div></td>'
    hang = [("dòng ghép 1-1", "dòng FLS dựng lại = dòng sổ", lambda k: o(TK[k]["chay"], TK[k]["co"])),
            ("ô Final · 7 khối", "đọc MID của sổ (oracle)", lambda k: o(TK[k]["o_parity_khop"], TK[k]["o_parity"])),
            ("ô khối HD", "đọc MID của sổ (oracle)", lambda k: o(TK[k]["hd_parity_khop"], TK[k]["hd_parity"])),
            ("ô Final · tự sinh", "FLS tự tính MID từ Manual input", lambda k: o(*TS["o"]) if k == TS["ky"] else '<td class="vo vo-na">–</td>')]
    head = '<tr><th class="vo-h">phép đo ↓ · tháng →</th>' + "".join(f"<th>{A2._m(k)}</th>" for k in KY) + "</tr>"
    body = "".join(f'<tr><th class="vo-h"><b>{a}</b><br><i>{b}</i></th>' + "".join(f(k) for k in KY) + "</tr>" for a, b, f in hang)
    dat = "".join(f'<td class="vo {"vo-ok" if (k in DU_DONG and k in DU_O and k == TS["ky"]) else "vo-na"}">'
                  f'{"✓" if (k in DU_DONG and k in DU_O and k == TS["ky"]) else "–"}</td>' for k in KY)
    body += f'<tr><th class="vo-h"><b>tháng đạt HD1</b><br><i>cả bốn dòng trên 100%</i></th>{dat}</tr>'
    n_dat = sum(1 for k in KY if k in DU_DONG and k in DU_O and k == TS["ky"])
    return "\n".join([
        A3.dau(3, "n5-3-3", "§5.3.3 SYSTEM: mapping giống quá khứ theo tháng", st="draft"),
        A2.cap("5.3.3", "SYSTEM", f"HD1 đo theo tháng: dòng 1-1, ô Final, ô khối HD, chế độ tự sinh — {len(KY)} kỳ trên ảnh đóng băng 26/08.",
               [f"Một tháng <b>đạt HD1</b> khi cả bốn dòng cùng 100%. Hôm nay: <b>{n_dat}/{len(KY)}</b> tháng — vì dòng 1-1 chỉ đủ ở {len(DU_DONG)} tháng, "
                f"còn chế độ tự sinh chỉ đo được {TS['ky']} (ảnh Manual input có đúng một tháng).",
                f"{TS['ky']} chưa đạt dù tự sinh 100%: dòng 1-1 của tháng ấy là {so(TK[TS['ky']]['chay'])}/{so(TK[TS['ky']]['co'])}.",
                "Màu: xanh = 100% · vàng ≥ 95% · đỏ &lt; 95% · xám = chưa đo được.",
                "Sinh từ <code>voi_so_luong.json</code> (cổng ghim 16/11: khối HD 9.930/9.930 · tự sinh 4.088/4.088 · HD 584/584; đã chứng minh đỏ)."]),
        '<div class="tw vo-khung"><table class="grid vo-bang" data-figure="5.3.3">' + head + body + "</table></div>",
    ])


def header(s: str) -> str:
    cu = re.search(r"<tr><th>Changes in v3\.0\.0</th><td>(.*?)</td></tr>", s, re.S)
    moi = (f"<tr><th>Changes in v3.1.0</th><td>Minor (⛔ đổi số mục nào). §5.3 thành <b>How done looks và Acceptance</b>: §5.3.1 How done looks (HD1 ★ mapping 100% giống "
           "dữ liệu quá khứ — owner 16/11 · HD2–HD5), §5.3.2 Acceptance (AC1–AC9 gom theo cấp + AC10 mapping 100% theo tháng · AC11 khối HD), §5.3.3 Figure 5.3.3 "
           "đo HD1 theo tháng. §5.4 lưới thêm AC10 · AC11. Công cụ đo thêm phép khớp khối HD theo tháng và chế độ tự sinh (cổng đã chứng minh đỏ). "
           f"<b>Sửa số sai</b> tôi ghi tay ở v2.5.0/v3.0.0: tháng có dòng ghép đủ là {len(DU_DONG)}/{len(KY)} (bản trước ghi 3/23), tháng còn thiếu là "
           f"{THIEU_DONG}/{len(KY)} (bản trước ghi 20/23) — ở §2.5.1 · §4.2 · AC6; giờ máy tính.</td></tr>")
    s = thay(s, cu.group(0), moi)
    lich = re.search(r'(<details><summary><b>)7 sửa đổi trước đó(</b> — )v2 → v2\.5\.0(</summary><table style="margin-top:8px">)', s)
    s = thay(s, lich.group(0), f"{lich.group(1)}8 sửa đổi trước đó{lich.group(2)}v2 → v3.0.0{lich.group(3)}"
             f'<tr><th style="white-space:nowrap;vertical-align:top">v3.0.0</th><td>2026-11-16 · {cu.group(1)}</td></tr>')
    s = thay(s, "<tr><th>Version</th><td>3.0.0 · 2026-11-16</td></tr>", f"<tr><th>Version</th><td>3.1.0 · {NGAY}</td></tr>")
    return s


def trang() -> str:
    s = A3.trang()
    s = thay(s, "<!-- AP_FLS-Voi_v3.0.0_Loi-Config-Chung_2026-11-16.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v3.py · v2.5.0 đóng băng -->",
             "<!-- AP_FLS-Voi_v3.1.0_How-Done-Acceptance_2026-11-16.html · sinh bởi docs/ITL/_tools/sinh_ap_voi_v31.py · v3.0.0 đóng băng -->")
    s = thay(s, '<meta name="ap:version" content="3.0.0">', '<meta name="ap:version" content="3.1.0">')
    s = thay(s, "<title>AP Voi FLS v3.0.0</title>", "<title>AP Voi FLS v3.1.0</title>")
    s = thay(s, "<h1>AP · Voi FLS v3.0.0 — lõi config chung", "<h1>AP · Voi FLS v3.1.0 — How done looks, lõi config chung")
    s = header(s)
    # §5.3: heading đổi tên + nội dung chuyển vào 3 mục con
    m = re.search(r'(<h2 class="part" id="s4-3"[^>]*>)(§5\.3 SYSTEM: nghiệm thu)(</h2>\n' + re.escape(A3.SEP) + r')(.*?)(' + re.escape(A3.SEP) + r'\n<h2 class="part" id="s4-4")', s, re.S)
    if not m:
        raise SystemExit("⛔ không thấy §5.3")
    dau53 = re.sub(r' data-st-on="[^"]*"', f' data-st-on="{NGAY}"', m.group(1))
    moi53 = (dau53 + "§5.3 SYSTEM: How done looks và Acceptance" + m.group(3)
             + "\n<p>Hai câu hỏi, theo thứ tự: <b>xong trông như thế nào</b> (§5.3.1), rồi <b>câu nào phải đúng và đo bằng gì</b> (§5.3.2); "
               "§5.3.3 đo điều số 1 — mapping 100% giống dữ liệu quá khứ — theo từng tháng.</p>\n"
             + how_done() + "\n" + acceptance(m.group(4)) + "\n" + hinh_533() + "\n")
    s = s[:m.start()] + moi53 + s[m.start(5):]
    # §5.4 lưới: thêm AC10 · AC11
    s = thay(s, "<td>AC5 · AC6 · AC9</td></tr>", "<td>AC5 · AC6 · AC9 · AC10 · AC11</td></tr>")
    r22 = re.search(r'<tr><td class="lbl">UF-2\.2</td>(?:<td[^>]*>[^<]*</td>){4}<td class="hole">▢</td></tr>', s)
    if not r22:
        raise SystemExit("⛔ dòng UF-2.2 của lưới")
    s = s.replace(r22.group(0), r22.group(0)[:-len('<td class="hole">▢</td></tr>')] + "<td>AC10</td></tr>", 1)
    s = thay(s, "(AC1–AC9 đều xuất hiện)", "(AC1–AC11 đều xuất hiện)")
    # sửa số sai ghi tay (máy tính lại)
    s = thay(s, "122 dòng sổ chưa có bản dựng 1-1 — tìm vì sao (Figure 2.2: chạy &lt; có ở 20/23 tháng)",
             f"{so(T['co'] - T['chay'])} dòng sổ chưa có bản dựng 1-1 — tìm vì sao (Figure 2.2: chạy &lt; có ở {THIEU_DONG}/{len(KY)} tháng)")
    s = thay(s, "122 dòng chưa có bản dựng 1-1, rải ở 20/23 tháng", f"{so(T['co'] - T['chay'])} dòng chưa có bản dựng 1-1, rải ở {THIEU_DONG}/{len(KY)} tháng")
    for tag in ("table", "tr", "div", "svg", "details", "ul"):
        a, b = len(re.findall(rf"<{tag}[\s>]", s)), s.count(f"</{tag}>")
        assert a == b, (tag, a, b)
    return s


def main() -> int:
    s = trang()
    RA.write_text(s, encoding="utf-8")
    print(f"✅ đã ghi {RA.relative_to(GOC)} · {len(s):,} byte · tháng đủ dòng {len(DU_DONG)}/{len(KY)} · đủ ô {len(DU_O)} · đủ HD {len(DU_HD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
