# -*- coding: utf-8 -*-
"""Report MỘT TRANG — HTML tĩnh, mọi ô của 4 lớp, cột agent ↔ máy (`WO-329` AC-4).

⭐ Đ4: mỗi ô in kèm NHÃN nó đếm gì (`NHAN`); mỗi skill in mẫu số · khớp · lệch · ⛔ đo được · thiếu · thừa.
⭐ Đ5: KẾT khai `mong` trước — lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0 · chưa chạy 0 · 4/4 agent A4 ĐẠT.
   Khác MỘT trong các số ấy ⇒ KẾT ĐỎ (cả hai chiều: thêm ô lệch hay bớt ô mong đều ĐỎ).
⭐ Lệch AS-IS CÓ TÊN (HD2 `lech_co_chu_dich` · HD1 dòng thiếu chưa ký) ở khối RIÊNG — ⛔ cộng vào lệch agent ↔ máy.
⭐ G0 bóng (ghép theo nội dung) ở khối RIÊNG — so với đáp án giữ riêng, ⛔ vào KẾT agent ↔ máy.
⭐ Bia `AG-R1-01` (KQ-331 — chủ đòi "khớp 100 %"): trang cũ ghi `claude-opus-5-5 ✅` cạnh "627/627" trong khi bản
   phát lại do mô hình GIẢ sinh, **0** chữ "giả", **0** chữ "chứng minh". Nay trang PHẢI có: khối *"Báo cáo này
   chứng minh gì / ⛔ chứng minh gì"* · nhãn nguồn trả lời cạnh cột mô hình (giả ⇒ ⛔ dấu ✅) · KẾT tách ô ĐỘC LẬP
   khỏi ô VÒNG TRÒN (`doi_chieu.nhom_o`), hai mẫu số riêng.
⭐ Bia `AG-R1-05`: mẫu số = ô của các mẫu skill, ⛔ "mọi dữ liệu" — khối *Độ phủ* khai phần tệp đo ⛔ vào mẫu số.
"""
from __future__ import annotations

import html
import json
from typing import Any

from fls.agent import doi_chieu as dc
from fls.agent.chuoi import KqChuoi
from fls.agent.o import VANG

NHAN = {
    "co": "dòng sổ AS-IS", "chay": "dòng FLS ghép 1-1", "map_fls": "dòng bank ghép A·B·C",
    "pm_noi": "PM line đã nối", "map_now": "dòng VLOOKUP NOW trả mã", "day_nguoi": "dòng đẩy người",
    "thieu": "dòng sổ chưa dựng 1-1", "o_parity": "ô Final được so", "o_parity_khop": "ô Final khớp",
    "hd_parity": "ô khối HD được so", "hd_parity_khop": "ô khối HD khớp", "o_go_that": "ô người gõ",
    "o_mac_dinh": "ô nhận mặc định", "o_trong": "ô máy ⛔ trả lời & Final rỗng", "o_de": "ô Final ≠ Classifying",
    "loai_tu_soi": "dòng tự-soi loại", "so_dong": "dòng ảnh tự khai", "dem_dong": "dòng máy đếm",
    "van_tay": "vân tay nội dung", "co_ref": "PM line có Ref", "khop": "ô đáp án khớp", "tong_o": "ô đáp án so",
    "lech_co_chu_dich": "ô lệch CÓ TÊN (AS-IS)", "dat": "phán cổng", "so_ky_dat": "kỳ đạt HD1",
    "so_ky": "kỳ trong mẫu số", "dong_bank": "dòng bank", "pm_noi_tong": "PM line nối (tổng)",
    "pm_co_ref": "PM line có Ref", "o": "[khớp, mẫu] ô 7 khối", "hd": "[khớp, mẫu] ô HD", "mid": "[khớp, mẫu] ô MID",
    "o_loi": "ô mã lỗi", "chon": "PM line agent chọn",
}


def _nhan(ma: str) -> str:
    duoi = ma.rsplit(".", 1)[-1]
    if duoi.isdigit() or duoi in ("A", "B", "C", "D", "E", "F"):
        if ".khoi_theo_ky." in ma or "khoi_theo_ky" in ma:
            return "khối: " + ("ô máy trả lời" if duoi == "0" else "ô người phải điền")
        if "dong_theo_hinh" in ma:
            return f"dòng bank hình {duoi}"
    return NHAN.get(duoi, duoi)


def _gt(v: Any) -> str:
    if v is VANG:
        return "—"
    return html.escape(json.dumps(v, ensure_ascii=False))


CSS = """
:root{--nen:#fff;--chu:#1b1b1b;--mo:#666;--vien:#ddd;--xanh:#0a7a3d;--do:#b3261e;--vang:#8a6d00;--xam:#eee}
@media (prefers-color-scheme: dark){:root{--nen:#141414;--chu:#eee;--mo:#aaa;--vien:#333;--xanh:#5ad08a;--do:#ff8a80;--vang:#f0c94a;--xam:#222}}
body{background:var(--nen);color:var(--chu);font:13px/1.45 system-ui,sans-serif;margin:0 16px 40px;max-width:1200px}
h1{font-size:20px;margin:16px 0 4px} h2{font-size:16px;margin:22px 0 6px} h3{font-size:14px;margin:12px 0 4px}
table{border-collapse:collapse;width:100%;margin:4px 0 8px} th,td{border:1px solid var(--vien);padding:2px 6px;text-align:left;vertical-align:top}
th{background:var(--xam)} td.s{text-align:right;font-variant-numeric:tabular-nums}
.ok{color:var(--xanh);font-weight:600} .do{color:var(--do);font-weight:600} .mo{color:var(--mo)}
.ket{font-size:18px;padding:8px 12px;border:2px solid;display:inline-block;margin:6px 0}
details{margin:2px 0} summary{cursor:pointer}
.bang-cuon{overflow-x:auto}
"""


#: Nguồn trả lời ⇒ có phải lượt API THẬT không. Khác danh sách này (giả · phát lại của giả · ⛔ rõ) ⇒ ⛔ thật.
NGUON_THAT = ("anthropic", "google")


def _la_that(pb: dict[str, Any] | None) -> bool:
    return bool(pb) and str(pb.get("nguon_tra_loi", "")) in NGUON_THAT


def _o_la(x: Any, duong: list[str], ra: list[tuple[str, bool]]) -> None:
    """Lá của tệp đo theo đúng luật `o.mo_rong` (vô hướng · danh sách vô hướng). `(đường, là số vô hướng)`."""
    if isinstance(x, dict):
        for k, v in x.items():
            _o_la(v, duong + [str(k)], ra)
        return
    if isinstance(x, list) and any(isinstance(y, (dict, list)) for y in x):
        for i, y in enumerate(x):
            _o_la(y, duong + [str(i)], ra)
        return
    ra.append((".".join(duong), isinstance(x, (int, float)) and not isinstance(x, bool)))


def do_phu(may: dict[str, Any], ma_o: set[str], nguon: tuple[str, ...] = ("voi", "hd2")) -> list[dict[str, Any]]:
    """Độ phủ mẫu số trên từng tệp đo, theo khối cấp 1: lá · lá vào mẫu số · lá SỐ · lá số vào mẫu số."""
    ra: list[dict[str, Any]] = []
    for n in nguon:
        goc = may.get(n)
        if not isinstance(goc, dict):
            ra.append({"nguon": n, "khoi": "(VẮNG)", "la": 0, "la_vao": 0, "so": 0, "so_vao": 0})
            continue
        for k, v in goc.items():
            la: list[tuple[str, bool]] = []
            _o_la(v, [str(k)], la)
            vao = [(d, s) for d, s in la if f"{n}:{d}" in ma_o]
            ra.append({"nguon": n, "khoi": str(k), "la": len(la), "la_vao": len(vao),
                       "so": sum(1 for _, s in la if s), "so_vao": sum(1 for _, s in vao if s)})
    return ra


def dong_ket(tom: dict[str, Any]) -> str:
    """Dòng KẾT dùng chung cho trang và CLI — hai nhóm ô, hai mẫu số (Đ4), nhãn nguồn trả lời."""
    dl, vt = tom["doc_lap"], tom["vong_tron"]
    gia = "" if tom.get("mo_hinh_that") else " · câu trả lời do mô hình GIẢ (0 lượt API thật)"
    return (f"{'ĐẠT' if tom['dat'] else 'ĐỎ'} — ô ĐỘC LẬP (voi: engine chạy lại ↔ tệp đo) {dl['khop']}/{dl['mau_so']} khớp"
            f" · ô VÒNG TRÒN (hd2·cong·nguon: chỉ bắt lỗi chép) {vt['khop']}/{vt['mau_so']} khớp"
            f" · lệch {tom[dc.LECH]} · ⛔ đo được {tom[dc.KHONG_DO_DUOC]} · thiếu {tom[dc.AGENT_THIEU]}"
            f" · thừa {tom[dc.AGENT_THUA]} · chưa chạy {tom[dc.CHUA_CHAY]} · A4 ĐẠT {tom['agent_dat']}/{tom['agent']} agent"
            + gia)


def _dem_html(dem: dict[str, int]) -> str:
    cot = ("mau_so", dc.KHOP, dc.LECH, dc.KHONG_DO_DUOC, dc.AGENT_THIEU, dc.AGENT_THUA, dc.CHUA_CHAY)
    return "".join(f'<td class="s{" do" if k in dc.TRANG_THAI_DO and dem.get(k) else ""}">{dem.get(k, 0)}</td>'
                   for k in cot)


def sinh(kc: KqChuoi, phien_ban: dict[str, Any], as_is: list[tuple[str, str, Any]],
         g0: dict[str, Any] | None, nguon_may: dict[str, str], ngay: str,
         may: dict[str, Any] | None = None) -> tuple[str, dict[str, Any]]:
    """Trả (HTML, tóm tắt KẾT). `as_is` = [(nhóm, tên lệch, số)] · `g0` = tổng hợp chấm ghép nội dung.

    `phien_ban` = `{mã agent: {"nguon_tra_loi": …}}` — thiếu ⇒ coi là ⛔ gọi thật (⛔ được in ✅).
    `may` = số máy đã đo (cho khối Độ phủ); `None` ⇒ khối ấy ghi ⛔ đo được.
    """
    moi_o = [o for a in kc.agents for o in a.o]
    dem = dc.tom_tat(moi_o)
    nhom = dc.tom_tat_nhom(moi_o)
    dl, vt = nhom[dc.DOC_LAP], nhom[dc.VONG_TRON]
    agent_mh = [a for a in kc.agents if any(k.skill.loai in ("lam", "bong") for k in a.skills)]
    so_that = sum(1 for a in agent_mh if _la_that(phien_ban.get(a.dn.ma)))
    nguon_tl = sorted({str((phien_ban.get(a.dn.ma) or {}).get("nguon_tra_loi", "⛔ rõ")) for a in agent_mh})
    so_agent_dat = sum(1 for a in kc.agents if a.dat_a4)
    mong = {dc.LECH: 0, dc.KHONG_DO_DUOC: 0, dc.AGENT_THIEU: 0, dc.AGENT_THUA: 0, dc.CHUA_CHAY: 0}
    lech_mong = {k: dem[k] for k, v in mong.items() if dem[k] != v}
    dat = (not lech_mong) and dem["mau_so"] > 0 and so_agent_dat == len(kc.agents) and kc.dung_o is None
    tom = {"dat": dat, "mau_so": dem["mau_so"], "khop": dem[dc.KHOP],
           **{k: dem[k] for k in mong}, "agent_dat": so_agent_dat, "agent": len(kc.agents), "dung_o": kc.dung_o,
           "doc_lap": {"mau_so": dl["mau_so"], "khop": dl[dc.KHOP]},
           "vong_tron": {"mau_so": vt["mau_so"], "khop": vt[dc.KHOP]},
           "mo_hinh_that": so_that, "agent_mo_hinh": len(agent_mh), "nguon_tra_loi": nguon_tl}
    h: list[str] = []
    w = h.append
    w(f"<!doctype html><html lang='vi'><head><meta charset='utf-8'><meta name='viewport' "
      f"content='width=device-width,initial-scale=1'><title>Report 4 agent Voi</title><style>{CSS}</style></head><body>")
    w("<h1>Report 4 agent vận hành Voi — agent ↔ số máy đã đo</h1>")
    w(f"<div class='mo'>Sinh bằng <code>python tools/chay_agent_voi.py --ghi-report</code> · {html.escape(ngay)} · "
      "chế độ PHÁT LẠI (⛔ gọi API thật) · ⛔ sửa tay.</div>")
    lop = "ok" if dat else "do"
    w(f"<div class='ket {lop}'>KẾT: {dong_ket(tom)}</div>")
    gia = so_that == 0
    w("<h2>0 · Báo cáo này chứng minh gì / ⛔ chứng minh gì</h2><table>"
      "<tr><th>✅ chứng minh</th><th>⛔ KHÔNG chứng minh</th></tr><tr><td><ul>"
      "<li><b>Đường ống</b>: 4 agent chạy TUẦN TỰ, cổng ra từng skill, A4 (MÃ) so từng ô; phá một cổng hay một ô ⇒ "
      "chuỗi DỪNG có tên, agent sau ⛔ chạy (bài <code>tests/agent/test_chuoi.py</code>).</li>"
      f"<li><b>Ô ĐỘC LẬP</b> <code>voi</code> — {dl[dc.KHOP]}/{dl['mau_so']}: engine FLS chạy LẠI trên ảnh đóng băng "
      "bằng đúng tệp đo đã ghi (<code>voi_so_luong.json</code>); sửa 1 ô tệp ⇒ LECH 1.</li>"
      "<li><b>A4 bắt lỗi CHÉP</b>: agent trả sai/thiếu/thừa 1 ô ⇒ A4 TRƯỢT, chuỗi DỪNG.</li></ul></td><td><ul>"
      + (f"<li><b>Chất lượng mô hình</b>: bản phát lại sinh bằng <b>mô hình GIẢ</b> (nguồn trả lời "
         f"<code>{html.escape(', '.join(nguon_tl))}</code> — chép nguyên kết quả công cụ); <b>0</b> lượt API thật. "
         "Mã mô hình ở §1 là mô hình GHIM cho lần chạy thật — CHƯA chạy.</li>" if gia else
         f"<li>Lượt API thật: {so_that}/{len(agent_mh)} agent gọi mô hình — xem §1.</li>")
      + f"<li><b>Ô VÒNG TRÒN</b> <code>hd2</code> · <code>cong</code> · <code>nguon</code> — {vt[dc.KHOP]}/{vt['mau_so']}: "
      "công cụ của agent và cột máy cùng đọc MỘT tệp/ảnh ⇒ khớp hiển nhiên khi chép đúng; sửa tệp ⇒ VẪN khớp. "
      "Chỉ bắt lỗi chép, ⛔ bắt lỗi dữ liệu hay engine HD2.</li>"
      "<li><b>\"Mọi dữ liệu\"</b>: mẫu số = ô của các mẫu skill — phần tệp đo ⛔ vào mẫu số khai ở §6 Độ phủ.</li>"
      "<li><b>Đúng nghiệp vụ so với sổ AS-IS</b>: chỗ FLS ≠ AS-IS có tên ở §4, ⛔ tính vào khớp.</li>"
      "</ul></td></tr></table>")
    w("<div class='mo'>Mong (khai trước, Đ5): lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0 · chưa chạy 0 · A4 ĐẠT 4/4 — "
      "trên CẢ HAI nhóm ô. Khác một số ⇒ ĐỎ.</div>")
    if kc.dung_o:
        w(f"<p class='do'>⛔ {html.escape(kc.dung_o)}</p>")
    if lech_mong:
        w(f"<p class='do'>Lệch so với mong: {html.escape(json.dumps(lech_mong, ensure_ascii=False))}</p>")

    w("<h2>1 · Phiên bản agent (mô hình ghim + nguồn trả lời + checksum prompt)</h2><table>"
      "<tr><th>agent</th><th>mô hình ghim</th><th>câu trả lời trong report do ai sinh</th><th>họ</th><th>ghim</th>"
      "<th>checksum prompt</th><th>A4</th></tr>")
    for a in kc.agents:
        m = a.dn.mo_hinh
        pb = phien_ban.get(a.dn.ma) or {}
        if a not in agent_mh:
            ai = ("<b>MÃ thuần</b> — ⛔ gọi mô hình tới G1 (quyết chủ C2); mô hình bên trái là mô hình DỰ KIẾN cho G1")
            ghim = "—"
        elif _la_that(pb):
            ai = f"API THẬT <code>{html.escape(str(pb.get('nguon_tra_loi')))}</code>"
            ghim = "✅" if m.ghim else "<span class=do>CHƯA ghim</span>"
        else:
            ai = (f"<span class=do>bản phát lại sinh bằng mô hình GIẢ</span> (<code>"
                  f"{html.escape(str(pb.get('nguon_tra_loi', '⛔ rõ')))}</code>) — 0 lượt API thật")
            ghim = ("ghim · <span class=do>CHƯA gọi thật</span>" if m.ghim else "<span class=do>CHƯA ghim</span>")
        w(f"<tr><td>{html.escape(a.dn.ten)}</td><td><code>{m.ma}</code></td><td>{ai}</td><td>{m.ho}</td>"
          f"<td>{ghim}</td><td><code>{a.checksum}</code></td>"
          f"<td class='{'ok' if a.dat_a4 else 'do'}'>{'ĐẠT' if a.dat_a4 else 'TRƯỢT'}</td></tr>")
    w("</table><div class='mo'>Tham chiếu (số máy đã đo): " +
      " · ".join(f"<code>{html.escape(k)}</code> {html.escape(v)}" for k, v in nguon_may.items()) + "</div>")

    w("<h2>2 · Chuỗi skill tuần tự (cổng ra từng skill)</h2><table><tr><th>#</th><th>skill</th><th>loại</th>"
      "<th>cổng</th><th>kết quả cổng</th><th>lượt</th><th>ô bị che</th></tr>")
    for a in kc.agents:
        for ks in a.skills:
            s = ks.skill
            if ks.loi:
                kqc = f"<span class=do>⛔ {html.escape(ks.loi)}</span>"
            elif ks.dat_cong is None:
                kqc = "<span class=do>chưa chạy</span>"
            else:
                kqc = f"<span class={'ok' if ks.dat_cong else 'do'}>{'ĐẠT' if ks.dat_cong else 'ĐỎ'}</span> " + \
                      html.escape(ks.ly_do)
            w(f"<tr><td>{s.agent[:2]}.{s.so:02d}</td><td>{html.escape(s.ten)}</td><td>{s.loai}</td>"
              f"<td><code>{html.escape(s.cong)}</code></td><td>{kqc}</td><td class=s>{ks.so_luot}</td>"
              f"<td class=s>{ks.so_bo_che}</td></tr>")
    w("</table>")

    w("<h2>3 · Mọi ô — agent ↔ máy, theo lớp và skill (hai nhóm, hai mẫu số)</h2><table><tr><th>lớp · skill</th>"
      "<th>nhóm</th><th>mẫu số</th><th>khớp</th><th>lệch</th><th>⛔ đo được</th><th>thiếu</th><th>thừa</th><th>chưa chạy</th></tr>")
    ten_nhom = {dc.DOC_LAP: "ĐỘC LẬP (voi)", dc.VONG_TRON: "VÒNG TRÒN (hd2·cong·nguon)"}
    for a in kc.agents:
        for ks in a.skills:
            if not ks.skill.mau_o or ks.skill.loai == "bong":
                continue
            for n in (dc.DOC_LAP, dc.VONG_TRON):
                ds = [o for o in a.o if o.skill == ks.skill.nhan and dc.nhom_o(o.ma) == n]
                if ds:
                    w(f"<tr><td>{html.escape(ks.skill.nhan)}{' <span class=mo>(mã)</span>' if ks.skill.loai == 'ma' else ''}"
                      f"</td><td>{ten_nhom[n]}</td>{_dem_html(dc.tom_tat(ds))}</tr>")
    for n in (dc.DOC_LAP, dc.VONG_TRON):
        w(f"<tr><th>TỔNG {ten_nhom[n]}</th><th></th>{_dem_html(nhom[n])}</tr>")
    w("</table>")
    for a in kc.agents:
        for ks in a.skills:
            if not ks.skill.mau_o or ks.skill.loai == "bong":
                continue
            ds = [o for o in a.o if o.skill == ks.skill.nhan]
            t = dc.tom_tat(ds)
            co_do = any(o.do for o in ds)
            w(f"<details{' open' if co_do else ''}><summary><b>{html.escape(ks.skill.nhan)}</b> — "
              f"{t[dc.KHOP]}/{t['mau_so']} ô khớp{' · <span class=do>CÓ ĐỎ</span>' if co_do else ''}</summary>"
              "<div class='bang-cuon'><table><tr><th>mã ô</th><th>nhóm</th><th>đếm gì</th><th>agent</th><th>máy</th>"
              "<th>trạng thái</th></tr>")
            for o in ds:
                w(f"<tr><td><code>{html.escape(o.ma)}</code></td>"
                  f"<td>{'độc lập' if dc.nhom_o(o.ma) == dc.DOC_LAP else 'vòng tròn'}</td><td>{html.escape(_nhan(o.ma))}</td>"
                  f"<td class=s>{_gt(o.agent)}</td><td class=s>{_gt(o.may)}</td>"
                  f"<td class={'do' if o.do else 'ok'}>{o.trang_thai}{(' · ' + html.escape(o.ly_do)) if o.ly_do else ''}</td></tr>")
            w("</table></div></details>")

    w("<h2>4 · Lệch AS-IS CÓ TÊN — ⛔ tính vào lệch agent ↔ máy</h2>"
      "<div class='mo'>Đây là chỗ FLS ≠ sổ AS-IS mà máy đã khai tên lý do (hoặc chưa ký). Agent chép đúng số này thì vẫn khớp 100 %.</div>"
      "<table><tr><th>nhóm</th><th>lệch có tên</th><th>số</th></tr>")
    for nhom, ten, so in as_is:
        w(f"<tr><td>{html.escape(nhom)}</td><td>{html.escape(ten)}</td><td class=s>{_gt(so)}</td></tr>")
    w("</table>")

    w("<h2>5 · G0 bóng — ghép theo NỘI DUNG (A2.04) ↔ đáp án giữ riêng</h2>")
    if g0:
        w("<div class='mo'>⛔ ghi sổ · ⛔ vào KẾT agent ↔ máy. Bể ca: " + html.escape(str(g0.get("be", ""))) + "</div><table>")
        for k, v in g0.items():
            if k != "be":
                w(f"<tr><td>{html.escape(k)}</td><td class=s>{_gt(v)}</td></tr>")
        w("</table>")
    else:
        w("<p class=do>⛔ đo được — không có bể ca.</p>")

    w("<h2>6 · Độ phủ — phần tệp đo ⛔ vào mẫu số</h2><div class='mo'>Lá = giá trị vô hướng hoặc danh sách vô hướng "
      "(đúng luật mở mẫu ô). Mẫu số của KẾT chỉ gồm lá mà một mẫu skill đưa vào; phần còn lại chưa có agent nào chép.</div>")
    if may is None:
        w("<p class=do>⛔ đo được — thiếu số máy.</p>")
    else:
        dp = do_phu(may, {o.ma for o in moi_o})
        w("<table><tr><th>tệp</th><th>khối</th><th>lá</th><th>lá vào mẫu số</th><th>lá ⛔ vào</th>"
          "<th>lá SỐ</th><th>lá số vào</th></tr>")
        for r in dp:
            w(f"<tr><td>{r['nguon']}</td><td><code>{html.escape(r['khoi'])}</code></td><td class=s>{r['la']}</td>"
              f"<td class=s>{r['la_vao']}</td><td class=s>{r['la'] - r['la_vao']}</td><td class=s>{r['so']}</td>"
              f"<td class=s>{r['so_vao']}</td></tr>")
        for n in ("voi", "hd2"):
            rr = [r for r in dp if r["nguon"] == n]
            la, vao = sum(r["la"] for r in rr), sum(r["la_vao"] for r in rr)
            so, so_vao = sum(r["so"] for r in rr), sum(r["so_vao"] for r in rr)
            tom.setdefault("do_phu", {})[n] = {"la": la, "la_vao": vao, "so": so, "so_vao": so_vao}
            w(f"<tr><th>{n}</th><th>TỔNG</th><th class=s>{la}</th><th class=s>{vao}</th><th class=s>{la - vao}</th>"
              f"<th class=s>{so}</th><th class=s>{so_vao}</th></tr>")
        w("</table>")
    w("</body></html>")
    return "".join(h), tom
