# -*- coding: utf-8 -*-
"""Vòng 1 test THẬT — report MỘT trang cột GIẢ ↔ THẬT (`WO-355` AC-3).

    python tools/vong_that_voi.py                          # GIẢ + thử THẬT; thiếu chốt ⇒ cột THẬT ĐỎ CÓ TÊN · ⛔ ghi
    python tools/vong_that_voi.py --ghi                    # + ghi docs/ITL/06_Agent/vong_that/REPORT_GIA_THAT.{md,json}
    python tools/vong_that_voi.py --that --tran-usd 2      # API THẬT: (a) tập nhỏ trước, in chi phí, DỪNG
    python tools/vong_that_voi.py --that --be --tran-usd 6 # + (b) fleet eval A2.04 trên bể A/B (sau khi xem chi phí (a))

⭐ `WO-359` (chủ 24/11 ~03:50): đường CHÍNH = **`claude.googleapis.com`** (Anthropic managed) của `fp-a-project`
   — đặt `FLS_NHA_CUNG_CAP=google-cloud` · `FLS_GCP_PROJECT=fp-a-project` · `FLS_CLAUDE_WORKSPACE_ID=wrkspc_…` · `FLS_GC_DU_LIEU_XAC_NHAN=1` (+
   `FLS_CHO_GOI_API=1`, `--that`); xác thực = ADC của GCP. Dự phòng: `FLS_NHA_CUNG_CAP=vertex` (Vertex AI) ·
   `FLS_NHA_CUNG_CAP=anthropic` (khoá, WO-355 — cũng là đường khi biến VẮNG). Khối lệnh cho chủ: BG-360 §B.

⭐ (a) CHUỖI 4 agent trên TẬP NHỎ có đáp án = 12 ca DỰNG (`tests/fixture/agent/`) + mẫu ≤ `--mau` ca (mặc định 20) của
   bể B giữ riêng (`$FLS_HELDOUT_NOI_DUNG/b`, hạt 355). Bể vắng ⇒ chỉ 12 ca dựng, report KHAI rõ (⛔ im lặng).
⭐ (b) FLEET EVAL A2.04 trên bể A (dữ liệu CŨ) và bể B (THẬT hiện tại): GIẢ = `luat_gia_v1` · THẬT = `claude-opus-5-5`;
   cùng `fleet_eval_voi.chay_vong` (cổng skill + bộ che `mo` + chấm MÙ) ⇒ hai cột so được.
⭐ Một `nhat_ky` + một trần USD cho CẢ lượt chạy (`mo_hinh.VuotTran`). Report chỉ có SỐ ĐẾM + VÂN TAY — ⛔ nội dung giao
   dịch, ⛔ phản hồi mô hình (luật cứng WO-355). G0 BÓNG: ⛔ ghi kho/sổ — mọi công cụ chỉ đọc ảnh/tệp đo.
⭐ Đ5 — KẾT khai `mong` trước: THẬT phải CHẠY (⛔ thiếu chốt) · A4 ĐẠT 4/4 · 0 ca phải-để-người bị nối (bar `a3-1-ref`)
   ở mọi tập. Thiếu một ⇒ ĐỎ (exit ≠ 0). THẬT ⛔ chạy được ⇒ exit 2 + tên chốt thiếu — ⛔ thay bằng số GIẢ.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from datetime import date
from pathlib import Path
from typing import Any

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "tools"))

from fls.agent import chuoi as ch  # noqa: E402
from fls.agent import ghep_noi_dung as gnd  # noqa: E402
from fls.agent import mo_hinh as mh  # noqa: E402
from fls.agent import report as rp  # noqa: E402

import chay_agent_voi as cav  # noqa: E402
import fleet_eval_voi as fe  # noqa: E402

TM_RA = GOC / "docs" / "ITL" / "06_Agent" / "vong_that"
TEP_MD = TM_RA / "REPORT_GIA_THAT.md"
TEP_JSON = TM_RA / "REPORT_GIA_THAT.json"
HAT_MAU = 355
MAU_MAC_DINH = 20
CHE = "mo"                                   # quyết chủ 23/11: agent đọc TOÀN BỘ nội dung + số TK


def _sha(x: Any) -> str:
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _nap(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def thu_muc_be() -> Path | None:
    tm = os.environ.get(cav.BIEN_HELDOUT)
    return Path(tm) if tm and (Path(tm) / "b" / "ca.json").exists() else None


def tap_nho(mau: int = MAU_MAC_DINH, be: Path | None = None) -> tuple[dict, dict, dict[str, Any]]:
    """12 ca dựng + ≤ `mau` ca bể B (khoá tiền tố `b_`, ⛔ đụng khoá ca dựng). Trả (ca, đáp án, khai)."""
    ca, dap = _nap(cav.CA_DUNG), _nap(cav.DAP_AN_DUNG)
    ca, dap = {"ca": dict(ca["ca"])}, {"noi": dict(dap["noi"])}
    khai: dict[str, Any] = {"ca_dung": len(ca["ca"]), "ca_be_b": 0, "be_b": "VẮNG (⛔ $" + cav.BIEN_HELDOUT + "/b)"}
    if be is not None and mau > 0:
        cb, db = _nap(be / "b" / "ca.json"), _nap(be / "b" / "dap_an.json")
        chon = sorted(random.Random(HAT_MAU).sample(sorted(cb["ca"]), min(mau, len(cb["ca"]))))
        for k in chon:
            ca["ca"][f"b_{k}"] = cb["ca"][k]
            dap["noi"][f"b_{k}"] = db["noi"][k]
        khai.update(ca_be_b=len(chon), be_b=f"mẫu {len(chon)}/{len(cb['ca'])} ca bể B (hạt {HAT_MAU})")
    khai["van_tay_tap"] = _sha(ca)
    khai["theo_nhom"] = {n: sum(1 for b in dap["noi"].values() if b.get("nhom") == n)
                         for n in sorted({b.get("nhom") for b in dap["noi"].values()})}
    return ca, dap, khai


def chay_chuoi_tap(ncc: dict[str, Any], ca: dict, dap: dict) -> dict[str, Any]:
    """Chuỗi 4 agent trên tập (ca, đáp án) — ⛔ đổi biến môi trường; trả số đếm (⛔ nội dung)."""
    cc = cav.dung_cong_cu(ca=ca)
    may = cav.dung_may()
    kc = ch.chay_chuoi(ncc, cc, may, dap_an=dap, che_do=CHE)
    _, tom = rp.sinh(kc, cav.phien_ban_cua(ncc), cav.as_is_co_ten(may), cav.g0_tong_hop(kc, dap, "tập nhỏ"),
                     {}, date.today().isoformat(), may=may)
    return {"doc_lap": tom["doc_lap"], "vong_tron": tom["vong_tron"], "lech": tom[rp.dc.LECH],
            "khong_do_duoc": tom[rp.dc.KHONG_DO_DUOC], "agent_dat": tom["agent_dat"], "agent": tom["agent"],
            "dung_o": kc.dung_o, "g0": cav.g0_tong_hop(kc, dap, "tập nhỏ"), "mo_hinh_that": tom["mo_hinh_that"]}


def chay_be(be: Path, ncc_a2: Any | None) -> dict[str, Any]:
    """A2.04 trên bể A và B. `ncc_a2` None ⇒ GIẢ (`luat_gia_v1`)."""
    ra: dict[str, Any] = {}
    for c in ("a", "b"):
        ca, dap = _nap(be / c / "ca.json"), _nap(be / c / "dap_an.json")
        ten = "v2-that-opus-5-5-mo" if ncc_a2 is not None else "v1-gia-mo"
        v = fe.chay_vong(ten, gnd.luat_gia_v1, CHE, ca, dap, ncc=ncc_a2)
        if "loi" in v or "bi_cam_gui" in v:
            ra[c] = {"loi": (v.get("loi") or v.get("bi_cam_gui"))[:200]}
            continue
        ra[c] = {"so_ca": len(dap["noi"]), "van_tay_be": _sha(ca), **fe.tong_hop_be(v["cham"])}
    return ra


def dung_that(co_that: bool, tran_usd: float, nk: list) -> tuple[dict[str, Any] | None, str | None]:
    """Nhà cung cấp THẬT cho chuỗi (A1–A3). Thiếu chốt ⇒ (None, lý do CÓ TÊN — ⛔ giá trị khoá)."""
    try:
        return cav.ncc_cho("that", co_that, che=CHE, tran_usd=tran_usd, nhat_ky=nk), None
    except (mh.CamGoiThat, mh.ChuaDung, ImportError) as e:
        return None, f"{type(e).__name__}: {e}"


def nhan_do(ly: str) -> str:
    """Tên ĐỎ khi ⛔ chạy được thật — chốt THIẾU QUAN TRỌNG NHẤT của đường đứng ĐẦU (WO-355: khoá; WO-359: project)."""
    if "ANTHROPIC_API_KEY" in ly and "vắng" in ly:
        return "thiếu ANTHROPIC_API_KEY · " + ly
    for b in (mh.BIEN_GCP_PROJECT, mh.BIEN_CLAUDE_WORKSPACE):
        if f"`{b}` vắng" in ly:
            return f"thiếu {b} (đường {mh.duong_goi()}) · " + ly
    return ly


def chay(co_that: bool = False, tran_usd: float = cav.TRAN_USD_MAC_DINH, mau: int = MAU_MAC_DINH,
         co_be: bool = False, be: Path | None = None, hop: dict[str, Any] | None = None) -> dict[str, Any]:
    """`hop` (`AG3-R1-01`): nhận nhà cung cấp THẬT NGAY khi dựng xong ⇒ `main` ghi nhật ký trên MỌI lối thoát (kể cả
    ngoại lệ chưa lường), ⛔ chỉ khi `chay` trả về bình thường."""
    be = be if be is not None else thu_muc_be()
    ca, dap, khai = tap_nho(mau, be)
    kq: dict[str, Any] = {"ngay": date.today().isoformat(), "tap_nho": khai, "che": CHE, "duong": mh.duong_goi(),
                          "mo_hinh": {a.ma: (ch.mo_hinh_skill(a, ch.nap_bo(a.ma)[0]) or a.mo_hinh).ma for a in ch.AGENT},
                          "gia": {"chuoi": chay_chuoi_tap(cav.ncc_cho("gia"), ca, dap)},
                          "that": {}, "be": "VẮNG" if be is None else "có (ngoài repo)"}
    if be is not None:
        kq["gia"]["be"] = chay_be(be, None)
    nk: list = []
    ncc, ly = dung_that(co_that, tran_usd, nk)
    if hop is not None and ncc is not None:
        hop["ncc"] = ncc
    if ncc is None:
        kq["that"] = {"do": nhan_do(ly or "")}
        kq["nhat_ky"] = mh.tong_nhat_ky([])
        return kq
    try:
        kq["that"]["chuoi"] = chay_chuoi_tap(ncc, ca, dap)
        kq["that"]["sau_tap_nho"] = mh.tong_nhat_ky(nk)
        dung = kq["that"]["chuoi"].get("dung_o") or ""
        if "LoiApi" in dung:                  # chuỗi tự bắt `LoiApi` (⇒ `dung_o`) — vẫn là lượt dừng GIỮA CHỪNG
            kq["that"]["loi_api"] = dung
        if co_be and be is not None:
            kq["that"]["be"] = chay_be(be, ncc["A2_PR_MAP"])
        elif co_be:
            kq["that"]["be"] = {"do": "ĐỎ — bể giữ riêng VẮNG"}
    except mh.VuotTran as e:
        kq["that"]["vuot_tran"] = str(e)
    except mh.LoiApi as e:
        # ⭐ `AG3-R1-01` (KQ-361): lỗi API/xác thực GIỮA CHỪNG (mạng · token ADC hết hạn · 403) ⇒ ĐỎ CÓ TÊN trong report,
        #   các lời đã tính tiền VẪN vào nhật ký (bản cũ: traceback, 0 tệp nhật ký). `str(LoiApi)` chỉ mang TÊN lỗi.
        kq["that"]["loi_api"] = str(e)
    kq["nhat_ky"] = mh.tong_nhat_ky(nk)
    kq["_ncc"] = ncc
    return kq


def ket(kq: dict[str, Any]) -> tuple[bool, list[str]]:
    """KẾT theo `mong` khai trước (Đ5). Trả (ĐẠT?, danh sách lý do ĐỎ)."""
    do: list[str] = []
    t = kq["that"]
    if "do" in t:
        return False, [t["do"]]
    if "vuot_tran" in t:
        do.append("vượt trần USD: " + t["vuot_tran"])
    if "loi_api" in t:
        do.append("LoiApi giữa chừng: " + t["loi_api"])
    c = t.get("chuoi") or {}
    if c.get("agent_dat") != c.get("agent"):
        do.append(f"A4 ĐẠT {c.get('agent_dat')}/{c.get('agent')} — dừng ở: {c.get('dung_o')}")
    g0 = c.get("g0") or {}
    if (g0.get("phai_nguoi_bi_noi") or 0) > fe.BAR_PHAI_NGUOI_BI_NOI:
        do.append(f"tập nhỏ: {g0['phai_nguoi_bi_noi']} ca phải-để-người bị nối (bar 0)")
    for b, v in (t.get("be") or {}).items():
        if isinstance(v, dict) and (v.get("phai_nguoi_bi_noi") or 0) > fe.BAR_PHAI_NGUOI_BI_NOI:
            do.append(f"bể {b.upper()}: {v['phai_nguoi_bi_noi']} ca phải-để-người bị nối (bar 0)")
    return not do, do


def _x(v: Any) -> str:
    return "—" if v is None else str(v).replace("|", "\\|")


def md(kq: dict[str, Any]) -> str:
    dat, ly = ket(kq)
    g, t = kq["gia"], kq["that"]
    # ô bảng ghi nhãn NGẮN; lý do đầy đủ (tên mọi chốt thiếu) chỉ ở dòng KẾT
    tc = None if "do" not in t else next((n for n in ("thiếu ANTHROPIC_API_KEY", f"thiếu {mh.BIEN_GCP_PROJECT}",
                                                      f"thiếu {mh.BIEN_CLAUDE_WORKSPACE}")
                                          if t["do"].startswith(n)), "ĐỎ — xem KẾT")
    L = [f"# Vòng 1 test THẬT — GIẢ ↔ THẬT · {kq['ngay']}", "",
         "> Sinh bởi `python tools/vong_that_voi.py --ghi` (`WO-355` AC-3) — ⛔ sửa tay. CHỈ số đếm + vân tay; ⛔ nội dung "
         "giao dịch, ⛔ phản hồi mô hình. G0 BÓNG: ⛔ ghi kho/sổ.", "",
         f"**KẾT: {'ĐẠT' if dat else 'ĐỎ'}**" + ("" if dat else " — " + " · ".join(_x(x) for x in ly)), "",
         "Mong (khai trước, Đ5): THẬT CHẠY được · A4 ĐẠT 4/4 · 0 ca phải-để-người bị nối ở mọi tập. Khác ⇒ ĐỎ.", "",
         "| | |", "|---|---|",
         "| mô hình | " + " · ".join(f"{a} `{m}`" for a, m in kq["mo_hinh"].items()) + " *(A4 = mô hình DỰ KIẾN G1; hôm nay MÃ)* |",
         f"| tập nhỏ | {kq['tap_nho']['ca_dung']} ca dựng + {kq['tap_nho']['ca_be_b']} ca bể B · {_x(kq['tap_nho']['be_b'])} · "
         f"theo nhóm {_x(kq['tap_nho']['theo_nhom'])} · vân tay `{kq['tap_nho']['van_tay_tap']}` |",
         f"| bể A/B | {kq['be']} |", f"| che | `{kq['che']}` (chủ 23/11: đọc toàn bộ) |",
         f"| đường gọi thật | `{_x(kq.get('duong'))}` " + {
             mh.DUONG_GOOGLE_CLOUD: "(claude.googleapis.com, Anthropic managed — CHÍNH, WO-359)",
             mh.DUONG_VERTEX: "(Claude trên Vertex AI — dự phòng, WO-359)"}.get(
             kq.get("duong"), "(Claude API, khoá — dự phòng WO-355)") + " |", "",
         "## (a) Chuỗi 4 agent trên tập nhỏ", "", "| chỉ số | GIẢ | THẬT |", "|---|---|---|"]
    gc, tcz = g["chuoi"], (t.get("chuoi") or {})
    hang = (("ô ĐỘC LẬP khớp / mẫu số", lambda d: f"{d['doc_lap']['khop']}/{d['doc_lap']['mau_so']}"),
            ("ô VÒNG TRÒN khớp / mẫu số", lambda d: f"{d['vong_tron']['khop']}/{d['vong_tron']['mau_so']}"),
            ("ô lệch · ⛔ đo được", lambda d: f"{d['lech']} · {d['khong_do_duoc']}"),
            ("A4 ĐẠT (agent)", lambda d: f"{d['agent_dat']}/{d['agent']}"),
            ("dừng ở", lambda d: d["dung_o"] or "—"),
            ("G0 A2.04: nối · nối sai · recall phải-nối · phải-người bị nối",
             lambda d: " · ".join(_x((d.get("g0") or {}).get(k)) for k in ("so_noi", "noi_sai", "recall_phai_noi", "phai_nguoi_bi_noi"))))
    for ten, f in hang:
        L.append(f"| {ten} | {_x(f(gc))} | " + (f"⛔ {_x(tc)}" if tc else (_x(f(tcz)) if tcz else "⛔ chưa chạy")) + " |")
    L += ["", "## (b) Fleet eval A2.04 — bể A (CŨ) · bể B (THẬT hiện tại)", ""]
    if kq["be"] == "VẮNG":
        L.append(f"⛔ bể giữ riêng VẮNG (`${cav.BIEN_HELDOUT}`) — dựng bằng `tools/dung_be_giu_rieng.py --doc-song` (ngoài repo).")
    else:
        L += ["| chỉ số | GIẢ bể A | THẬT bể A | GIẢ bể B | THẬT bể B |", "|---|---|---|---|---|"]
        tb = t.get("be") or {}
        for ten, k in (("ca (mẫu số chính)", "mau_so_chinh"), ("nối", "so_noi"), ("nối sai", "noi_sai"),
                       ("tỉ lệ nối sai", "ti_le_noi_sai"), ("recall phải-nối", "recall_phai_noi"),
                       ("ca phải-để-người bị nối", "phai_nguoi_bi_noi"), ("L3 bị nối", "l3_bi_noi"), ("điểm TB 0–2", "diem_tb")):
            o = []
            for b in ("a", "b"):
                gv = (g.get("be") or {}).get(b) or {}
                o.append(_x(gv.get(k)) if "loi" not in gv else "⛔ " + _x(gv["loi"]))
                if tc:
                    o.append("⛔ " + _x(tc))
                elif "do" in tb:
                    o.append("⛔ " + _x(tb["do"]))
                else:
                    tv = tb.get(b)
                    o.append("⛔ chưa chạy (`--be`)" if tv is None else ("⛔ " + _x(tv["loi"]) if "loi" in tv else _x(tv.get(k))))
            L.append(f"| {ten} | " + " | ".join(o) + " |")
    n = kq["nhat_ky"]
    L += ["", "## Token + chi phí (THẬT)", "",
          f"Giá tra ngày **{n['ngay_tra_gia']}** (Opus 5.5 $4/$20 · Sonnet 5.5 $2/$10 / 1M token vào/ra"
          + (" · Vertex: global = giá Claude API, `us`/`eu` +10% — giả định chưa kiểm, số thật ở Billing GCP"
             if n.get("duong") == [mh.DUONG_VERTEX] else "")
          + (" · google-cloud: CHƯA có bảng giá chính thức — ƯỚC theo giá Claude API để giữ trần; số thật ở hoá đơn "
             "Marketplace GCP" if n.get("duong") == [mh.DUONG_GOOGLE_CLOUD] else "") + f") · đường {_x('/'.join(n.get('duong') or []) or '—')}"
          + (f" · vùng {_x('/'.join(n['vung']))}" if n.get("vung") else "") + " — USD là ƯỚC.", "",
          "| lời gọi | token vào | token ra | cache đọc | cache ghi | giây | USD ước |", "|---|---|---|---|---|---|---|",
          f"| {n['so_goi']} | {n['token_vao']} | {n['token_ra']} | {n['cache_doc']} | {n['cache_ghi']} | {n['giay']} | {n['chi_phi_usd']} |"]
    if t.get("sau_tap_nho"):
        s = t["sau_tap_nho"]
        L.append(f"\nSau tập nhỏ (a): {s['so_goi']} lời gọi · {cav.nhan_usd(s)}.")
    if n["so_goi"] == 0:
        L.append("\n**0 lời gọi thật** (Đ3: mẫu số 0 ⇒ ⛔ có số token/chi phí để báo — đây là KẾT QUẢ, ⛔ là \"rẻ\").")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="vong_that_voi.py")
    p.add_argument("--that", action="store_true",
                   help="gọi THẬT — FLS_CHO_GOI_API=1 + đường FLS_NHA_CUNG_CAP=google-cloud (FLS_GCP_PROJECT · "
                        "FLS_CLAUDE_WORKSPACE_ID · FLS_GC_DU_LIEU_XAC_NHAN=1) | vertex | anthropic (vắng ⇒ anthropic)")
    p.add_argument("--be", action="store_true", help="(b) fleet eval A2.04 trên bể A/B — chạy SAU khi xem chi phí (a)")
    p.add_argument("--tran-usd", type=float, default=cav.TRAN_USD_MAC_DINH,
                   help="trần USD ƯỚC của cả vòng — chặn lời gọi KẾ khi tổng đã tiêu ≥ trần; ⛔ cắt lời gọi ĐANG chạy (một lời có thể vượt trần — AG2-R1-03)")
    p.add_argument("--mau", type=int, default=MAU_MAC_DINH, help="số ca bể B thêm vào tập nhỏ (≤ 20 theo WO-355)")
    p.add_argument("--ghi", action="store_true")
    a = p.parse_args(argv)
    if a.mau > MAU_MAC_DINH:
        print(f"⛔ --mau {a.mau} > {MAU_MAC_DINH} (WO-355: mẫu ≤ 20 ca)")
        return 2
    hop: dict[str, Any] = {}
    try:
        kq = chay(a.that, a.tran_usd, a.mau, a.be, hop=hop)
    except BaseException as e:
        # ⭐ `AG3-R1-01`: ngoại lệ CHƯA lường (⛔ `LoiApi`/`VuotTran`) — tiền đã tiêu vẫn để lại nhật ký + TÊN lỗi, rồi ném lại
        if hop.get("ncc"):
            pn = cav.ghi_nhat_ky(hop["ncc"], "vong_that", loi=f"{type(e).__name__} (lượt dừng ngoài dự kiến)")
            if pn:
                print(f"  ⛔ lượt dừng ({type(e).__name__}) — đã ghi nhật ký {pn.relative_to(GOC) if pn.is_relative_to(GOC) else pn}")
        raise
    ncc = kq.pop("_ncc", None)
    dat, ly = ket(kq)
    trang = md(kq)
    print(trang)
    if a.ghi:
        TM_RA.mkdir(parents=True, exist_ok=True)
        TEP_MD.write_text(trang, encoding="utf-8")
        TEP_JSON.write_text(json.dumps(kq, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
        print(f"  đã ghi {TEP_MD.relative_to(GOC)} · {TEP_JSON.relative_to(GOC)}")
    # ⭐ `AG2-R1-04` (KQ-357): nhật ký lời gọi THẬT ghi LUÔN (⛔ phụ thuộc `--ghi`) — tiền đã tiêu phải để lại dấu vết.
    #   `ghi_nhat_ky` trả None khi 0 lời gọi (Đ3) ⇒ lượt thiếu chốt ⛔ sinh tệp.
    if ncc:
        loi = kq["that"].get("loi_api") or kq["that"].get("vuot_tran")
        pn = cav.ghi_nhat_ky(ncc, "vong_that", loi=loi) if loi else cav.ghi_nhat_ky(ncc, "vong_that")
        if pn:
            print(f"  đã ghi nhật ký {pn.relative_to(GOC) if pn.is_relative_to(GOC) else pn}")
    if "do" in kq["that"]:
        return 2
    return 0 if dat else 1


if __name__ == "__main__":
    raise SystemExit(main())
