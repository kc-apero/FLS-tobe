# -*- coding: utf-8 -*-
"""Chạy chuỗi 4 agent vận hành Voi (`WO-329`) — MẶC ĐỊNH chế độ PHÁT LẠI, ⛔ gọi API thật.

    python tools/chay_agent_voi.py                     # phát lại · in KẾT · exit 0 khi ĐẠT
    python tools/chay_agent_voi.py --ghi-report        # + ghi docs/ITL/06_Agent/report.html
    python tools/chay_agent_voi.py --gia --ghi-phat-lai  # mô hình GIẢ tất định ⇒ ghi lại bản phát lại
    python tools/chay_agent_voi.py --che che_het       # che lại (mặc định `mo` — chủ 23/11: agent đọc toàn bộ)
    python tools/chay_agent_voi.py --that --tran-usd 2 # API THẬT (WO-355) — cần FLS_CHO_GOI_API=1 + ANTHROPIC_API_KEY
                                                       #   + FLS_ZDR_DA_BAT=1 (chế độ `mo`); in token + USD ước;
                                                       #   ghi nhật ký vòng (CHỈ số đếm + vân tay) docs/ITL/06_Agent/nhat_ky/
    FLS_NHA_CUNG_CAP=google-cloud FLS_GCP_PROJECT=fp-a-project FLS_CLAUDE_WORKSPACE_ID=wrkspc_… \
      FLS_GC_DU_LIEU_XAC_NHAN=1 FLS_CHO_GOI_API=1 python tools/chay_agent_voi.py --that
                                                       # ⭐ WO-359: đường CHÍNH claude.googleapis.com (ADC/SA, ⛔ khoá)
                                                       #   dự phòng: FLS_NHA_CUNG_CAP=vertex | anthropic (= khi vắng)

⭐ Công cụ agent gọi = CHỈ hàm FLS có sẵn, tiêm vào chuỗi từ đây (gói `fls.agent` ⛔ biết kho/tuyến):
   nguon_bank · nguon_fps · nguon_h1000 · nguon_plt   đếm ảnh đóng băng 4 nguồn raw (`tests/fixture/…`)
   dong_chuan · ghep_ref · hang_cho · final_7_khoi ·  engine HD1 `tools/do_voi_so_luong.do()` — chạy CHÍNH mã FLS
   vung_sua · tu_sinh                                  (`pm_join.xep_ca_lat` · `final_rule.tinh_final` · `tu_soi`)
   phan_bo_bao_cao                                     số 10 gói HD2 (`hd2_cong.json`, ghi bởi `tools/do_hd2.py`)
   cong_hd1 · cong_hd2                                 cổng FLS `fls.repo.doc_bao_cao.doc_cong_tep_do/_hd2`
   ung_vien_ghep                                       bể ca ghép theo nội dung (dựng · hoặc GIỮ RIÊNG ngoài repo)
⭐ MÁY ĐÃ ĐO (cột "máy" của report) — đọc ĐỘC LẬP với đường agent:
   voi = `docs/ITL/_tools/voi_so_luong.json` · hd2 = `docs/ITL/_tools/hd2_cong.json` (tách theo gói) ·
   nguon = đếm ảnh trực tiếp · cong = gọi thẳng `doc_cong_*` trên hai tệp trên.
⚠ Tự thấy yếu (khai ở BG-330): với `hd2` và `cong`, đường agent và đường máy cùng đọc một tệp đo — phép so
   bắt lỗi CHÉP của agent, ⛔ bắt engine HD2 cũ (engine HD2 cần kho có IX config: `tools/do_hd2.py --dsn`).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any, Callable

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "tools"))

from fls.agent import chuoi as ch  # noqa: E402
from fls.agent import ghep_noi_dung as gnd  # noqa: E402
from fls.agent import mo_hinh as mh  # noqa: E402
from fls.agent import report as rp  # noqa: E402
from fls.agent.o import gia_tri, mo_rong  # noqa: E402
from fls.agent.skill import nap_bo  # noqa: E402

FX = GOC / "tests" / "fixture"
TEP_VOI = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
TEP_HD2 = GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json"
TM_AGENT = GOC / "docs" / "ITL" / "06_Agent"
TM_PHAT_LAI = TM_AGENT / "phat_lai"
TEP_REPORT = TM_AGENT / "report.html"
TM_NHAT_KY = TM_AGENT / "nhat_ky"          # nhật ký vòng THẬT: số đếm + vân tay, ⛔ nội dung (WO-355 AC-2/AC-4)
TRAN_USD_MAC_DINH = 2.0                   # trần chi phí MỘT vòng thật — chạy tập nhỏ trước, xem chi phí
CA_DUNG = FX / "agent" / "ca_noi_dung_dung.json"
DAP_AN_DUNG = FX / "agent" / "dap_an_noi_dung_dung.json"
BIEN_HELDOUT = "FLS_HELDOUT_NOI_DUNG"     # thư mục GIỮ RIÊNG (ca.json + dap_an.json) — ngoài repo

#: Ảnh đóng băng 4 nguồn raw: tên ô → (tệp, khoá danh sách dòng, khoá số dòng tự khai).
ANH_NGUON: dict[str, tuple[str, str, str]] = {
    "bank": ("pm_join.json", "bank", "so_dong_bank"),
    "so_asis": ("itl_ledge_adjustment.json", "dong", "so_dong"),
    "fps": ("pm_join.json", "pm", "so_dong_pm"),
    "hr2024": ("dau_vao/hr_ledger_2024.json", "dong", "so_dong"),
    "hr2025": ("dau_vao/hr_ledger_2025.json", "dong", "so_dong"),
    "gi": ("dau_vao/gi_cfa1.json", "dong", "so_dong"),
    "omc": ("dap_an/omc_mid1.json", "dong", "so_dong"),
    "sc": ("dap_an/sc_mid1.json", "dong", "so_dong"),
    "ps": ("dap_an/ps_mid1.json", "dong", "so_dong"),
}
NHOM_NGUON = {"nguon_bank": ("bank", "so_asis"), "nguon_fps": ("fps",), "nguon_h1000": ("hr2024", "hr2025"),
              "nguon_plt": ("gi", "omc", "sc", "ps")}


def _nap(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def dem_nguon(ten: str, fx: Path = FX) -> dict[str, Any]:
    tep, khoa_dong, khoa_so = ANH_NGUON[ten]
    d = _nap(fx / tep)
    ra = {f"nguon:{ten}.so_dong": int(d[khoa_so]), f"nguon:{ten}.dem_dong": len(d[khoa_dong]),
          f"nguon:{ten}.van_tay": d.get("checksum_noi_dung")}
    if ten == "fps":
        ra["nguon:fps.co_ref"] = sum(1 for x in d["pm"] if str(x.get("ref_tho") or "").strip())
    return ra


def may_nguon(fx: Path = FX) -> dict[str, Any] | None:
    try:
        ra: dict[str, Any] = {}
        for ten in ANH_NGUON:
            for k, v in dem_nguon(ten, fx).items():
                ra.setdefault(ten, {})[k.split(".", 1)[1]] = v
        return ra
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return None


def tach_hd2(d: dict | None) -> dict | None:
    """`hd2_cong.json` → `{gói: khối}` — WP-C2 nằm ở GỐC tệp (bỏ các khoá gói con)."""
    if d is None:
        return None
    ra = {k: v for k, v in d.items() if k.startswith("WP-C") and isinstance(v, dict)}
    if d.get("goi") == "WP-C2":
        ra["WP-C2"] = {k: v for k, v in d.items() if not k.startswith("WP-C")}
    return ra


def cong_tu_tep(tep_voi: Path, tep_hd2: Path) -> dict[str, Any]:
    from fls.repo.doc_bao_cao import doc_cong_hd2, doc_cong_tep_do
    return {"HD1": {c.ma: {"dat": c.dat} for c in doc_cong_tep_do(tep_voi)},
            "HD2": {c.ma: {"dat": c.dat} for c in doc_cong_hd2(tep_hd2)}}


def doc_tep_hoac_none(p: Path) -> Any:
    try:
        return _nap(p)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def dung_may(tep_voi: Path = TEP_VOI, tep_hd2: Path = TEP_HD2, fx: Path = FX) -> dict[str, Any]:
    """Số MÁY ĐÃ ĐO — nguồn vắng ⇒ `None` (report ĐỎ "⛔ đo được" cho mọi ô của nguồn ấy)."""
    voi, hd2 = doc_tep_hoac_none(tep_voi), doc_tep_hoac_none(tep_hd2)
    return {"voi": voi, "hd2": tach_hd2(hd2), "nguon": may_nguon(fx),
            "cong": cong_tu_tep(tep_voi, tep_hd2) if voi is not None and hd2 is not None else None}


def bo_ca(cho_heldout: bool = True) -> tuple[dict, dict, str]:
    """(ca, đáp án, nhãn bể). Có `FLS_HELDOUT_NOI_DUNG` ⇒ bể GIỮ RIÊNG; ⛔ thì bể DỰNG trong repo.

    ⭐ `AG2-R1-02` (KQ-357): `dung_be_giu_rieng.py` ghi bố cục `$DIR/a/` · `$DIR/b/` (BG-356/360 đặt biến cho
    `vong_that_voi.py`) còn bản cũ đọc `$DIR/ca.json` ⇒ `FileNotFoundError`. Nay nhận CẢ HAI: phẳng (`$DIR/ca.json`) ·
    hai bể ⇒ bể **B** (dữ liệu THẬT hiện tại). Cả hai vắng ⇒ `FileNotFoundError` có tên (⛔ rơi về bể dựng im lặng)."""
    tm = os.environ.get(BIEN_HELDOUT)
    if cho_heldout and tm:
        if (Path(tm) / "ca.json").exists():
            return _nap(Path(tm) / "ca.json"), _nap(Path(tm) / "dap_an.json"), "giữ riêng (ngoài repo)"
        if (Path(tm) / "b" / "ca.json").exists():
            return (_nap(Path(tm) / "b" / "ca.json"), _nap(Path(tm) / "b" / "dap_an.json"),
                    "giữ riêng — bể B (ngoài repo)")
        raise FileNotFoundError(f"${BIEN_HELDOUT} ⛔ có `ca.json` lẫn `b/ca.json`")
    return _nap(CA_DUNG), _nap(DAP_AN_DUNG), "ca DỰNG trong repo (⛔ dữ liệu thật)"


def o_ca(ca: dict) -> dict[str, Any]:
    ra: dict[str, Any] = {}
    for k, c in ca["ca"].items():
        for f in ("tien", "cur", "ngay", "tk", "noi_dung"):
            ra[f"noi:{k}.{f}"] = c[f]
        for i, u in enumerate(c["ung_vien"]):
            for f in ("pm", "tien", "cur", "ngay"):
                ra[f"noi:{k}.uv.{i}.{f}"] = u[f]
    return ra


def dung_cong_cu(tep_voi: Path = TEP_VOI, tep_hd2: Path = TEP_HD2, fx: Path = FX,
                 ca: dict | None = None) -> dict[str, Callable[[], dict]]:
    """Sổ công cụ agent được gọi. Engine HD1 chạy MỘT lần (nhớ đệm)."""
    dem: dict[str, Any] = {}

    def eng() -> dict:
        if "voi" not in dem:
            import do_voi_so_luong
            dem["voi"] = do_voi_so_luong.do()
        return dem["voi"]

    def theo_mau(skill_ma: str, du: Callable[[], dict]) -> Callable[[], dict]:
        def f() -> dict:
            ag, _, sk = skill_ma.partition("/")
            s = [x for x in nap_bo(ag) if x.ma == sk][0]
            d = du()
            return {m: gia_tri(m, d) for mau in s.mau_o for m in mo_rong(mau, d)}
        return f

    def du_voi() -> dict:
        return {"voi": eng()}

    def du_hd2() -> dict:
        return {"hd2": tach_hd2(_nap(tep_hd2))}

    def du_cong() -> dict:
        return {"voi": eng(), "cong": cong_tu_tep(tep_voi, tep_hd2)}

    cc: dict[str, Callable[[], dict]] = {}
    for ten, nhom in NHOM_NGUON.items():
        cc[ten] = (lambda nhom=nhom: {k: v for n in nhom for k, v in dem_nguon(n, fx).items()})
    for ten, sk in (("dong_chuan", "A2_PR_MAP/01_dong_chuan"), ("ghep_ref", "A2_PR_MAP/02_ghep_ref"),
                    ("hang_cho", "A2_PR_MAP/03_hang_cho_nguoi"), ("final_7_khoi", "A3_SI_ITL/01_final_7_khoi"),
                    ("vung_sua", "A3_SI_ITL/02_vung_sua"), ("tu_sinh", "A3_SI_ITL/03_tu_sinh")):
        cc[ten] = theo_mau(sk, du_voi)
    cc["phan_bo_bao_cao"] = theo_mau("A3_SI_ITL/04_phan_bo_bao_cao", du_hd2)
    cc["cong_hd1"] = theo_mau("A4_AUDITOR/02_cong_hd1", du_cong)
    cc["cong_hd2"] = theo_mau("A4_AUDITOR/03_cong_hd2", du_cong)
    ca_ = ca if ca is not None else bo_ca()[0]
    cc["ung_vien_ghep"] = lambda: o_ca(ca_)
    return cc


def as_is_co_ten(may: dict) -> list[tuple[str, str, Any]]:
    ra: list[tuple[str, str, Any]] = []
    for g, b in sorted((may.get("hd2") or {}).items()):
        if b.get("lech_co_chu_dich"):
            ra.append((f"HD2 {g}", "ô lệch có chủ đích (AS-IS sai đã khai tên)", b["lech_co_chu_dich"]))
        lt = b.get("lech_co_ten")
        if isinstance(lt, dict):
            for k, v in lt.items():
                if isinstance(v, (int, float)) and v:
                    ra.append((f"HD2 {g}", f"`{k}`", v))
    voi = may.get("voi") or {}
    dh = voi.get("dat_hd1") or {}
    if dh:
        ra.append(("HD1", "dòng sổ chưa dựng 1-1 (nhãn lý do: chưa ký)", (dh.get("dem") or {}).get("thieu")))
        ra.append(("HD1", "chữ ký trong sổ lý do", dh.get("so_chu_ky")))
        ra.append(("HD1", "kỳ đạt HD1 / kỳ trong mẫu số", f"{dh.get('so_ky_dat')}/{(dh.get('mau_so') or {}).get('so_ky')}"))
    ts = voi.get("tu_sinh") or {}
    for k, v in (ts.get("lech_mid") or {}).items():
        ra.append(("HD1 tự sinh 2026-03", f"ô MID lệch khối `{k}`", v))
    return ra


def ncc_cho(che_do: str, co_that: bool = False, luat: dict | None = None, che: str | None = None,
            tran_usd: float | None = TRAN_USD_MAC_DINH, nhat_ky: list | None = None) -> dict[str, Any]:
    """Nhà cung cấp theo agent — CHỈ cho agent có skill gọi mô hình (`ch.can_mo_hinh`).

    ⚠ Bia `AG-R1-06`: bản đầu dựng cho cả 4 agent ⇒ `--that` dựng Google cho A4 ⇒ `GoogleChuaDung` chặn luôn A1–A3.
    ⭐ `WO-355`: chế độ `that` ⇒ MỌI adapter dùng CHUNG một `nhat_ky` (trần USD tính trên cả vòng).
    """
    ra: dict[str, Any] = {}
    nk: list = nhat_ky if nhat_ky is not None else []
    for dn in ch.AGENT:
        if not ch.can_mo_hinh(dn.ma):
            continue
        if che_do == "that":
            ra[dn.ma] = mh.tao_that(dn.mo_hinh, co_that, che or ch.che_mod.CHE_DO_MAC_DINH,
                                    tran_usd=tran_usd, nhat_ky=nk)
        elif che_do == "gia":
            ra[dn.ma] = mh.GiaLap(luat if luat is not None else {"ung_vien_ghep": gnd.luat_gia_v1})
        else:
            ra[dn.ma] = mh.PhatLai(TM_PHAT_LAI / f"{dn.ma}.json")
    return ra


def nhat_ky_cua(ncc: dict[str, Any]) -> list:
    """Nhật ký lời gọi THẬT của vòng (danh sách chung) — ⛔ adapter thật ⇒ `[]`."""
    for n in ncc.values():
        nk = getattr(n, "nhat_ky", None)
        if isinstance(nk, list):
            return nk
    return []


def nhan_usd(t: dict[str, Any]) -> str:
    """`~X USD ƯỚC (…)` — ⭐ `AG3-R1-03` (KQ-361): MỌI số USD in ra mang nhãn ƯỚC + nguồn giá theo ĐƯỜNG. Đường
    `google-cloud` nói rõ CHƯA có bảng giá (giá Claude API dùng để giữ trần); số thật ở hoá đơn GCP."""
    duong = t.get("duong") or []
    if duong == [mh.DUONG_GOOGLE_CLOUD]:
        nguon = "giá Claude API — nền claude.googleapis.com CHƯA có bảng giá; số thật ở hoá đơn GCP"
    elif duong == [mh.DUONG_VERTEX]:
        nguon = "Vertex: global = giá Claude API (giả định chưa kiểm), us/eu +10%; số thật ở Billing GCP"
    else:
        nguon = "giá Claude API"
    return f"~{t['chi_phi_usd']} USD ƯỚC ({nguon}; tra {t['ngay_tra_gia']})"


def ghi_nhat_ky(ncc: dict[str, Any], nhan: str, tm: Path | None = None, loi: str | None = None) -> Path | None:
    """Ghi nhật ký vòng: mỗi lời gọi = mô hình · token · giây · USD ước · stop_reason · VÂN TAY yêu cầu/đáp.
    ⛔ nội dung yêu cầu, ⛔ phản hồi thô, ⛔ khoá (luật cứng WO-355). 0 lời gọi ⇒ ⛔ ghi (Đ3: ⛔ tệp rỗng giả vờ có số).

    `tm` vắng ⇒ đọc `TM_NHAT_KY` LÚC GỌI (⛔ lúc định nghĩa) ⇒ bài thử đổi hướng được bằng `monkeypatch` (`AG3-R1-02`).
    `loi` (`AG3-R1-01`): lượt DỪNG giữa chừng ⇒ thêm MỘT dòng `loi` = TÊN lỗi (⛔ nội dung) cạnh các lời đã tính tiền."""
    nk = nhat_ky_cua(ncc)
    if not nk:
        return None
    tm = TM_NHAT_KY if tm is None else tm
    from datetime import datetime, timezone
    tm.mkdir(parents=True, exist_ok=True)
    p = tm / f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}_{nhan}.json"
    d = {"_vi_sao": "Nhật ký vòng API THẬT — CHỈ số đếm + vân tay (WO-355 AC-2/AC-4 · WO-359).",
         "tong": mh.tong_nhat_ky(nk), "goi": [x.dict() for x in nk]}
    if loi:
        d["loi"] = loi
    p.write_text(json.dumps(d,
                            ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return p


def ghi_phat_lai(ncc: dict[str, mh.GhiLai]) -> None:
    from fls.agent.skill import checksum_prompt
    TM_PHAT_LAI.mkdir(parents=True, exist_ok=True)
    for dn in ch.AGENT:
        if dn.ma not in ncc:
            continue
        g = ncc[dn.ma]
        d = {"_vi_sao": "Bản ghi PHÁT LẠI — sinh bằng mô hình GIẢ tất định (`--gia --ghi-phat-lai`), ⛔ lượt API thật. "
                        "Tra theo vân tay yêu cầu ĐÃ CHE; prompt/dữ liệu đổi ⇒ ⛔ có lượt ⇒ ĐỎ.",
             "agent": dn.ma, "mo_hinh": dn.mo_hinh.ma, "checksum_prompt": checksum_prompt(dn.ma),
             "nguon_tra_loi": g.goc.ten, "luot": g.luot}
        (TM_PHAT_LAI / f"{dn.ma}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                                  encoding="utf-8")


def g0_tong_hop(kc: ch.KqChuoi, dap_an: dict, nhan_be: str) -> dict[str, Any] | None:
    a2 = [a for a in kc.agents if a.dn.ma == "A2_PR_MAP"]
    if not a2:
        return None
    ks = [k for k in a2[0].skills if k.skill.loai == "bong"]
    if not ks or ks[0].ra is None:
        return {"be": nhan_be, "trang_thai": "chưa chạy"}
    phang = {f"noi:{c}.{f}": v for c, b in dap_an["noi"].items() for f, v in b.items()}
    return {"be": nhan_be, **gnd.tong_hop(gnd.cham(ks[0].ra, phang))}


def phien_ban_cua(ncc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Nguồn trả lời THẬT SỰ của từng agent — đọc từ nhà cung cấp, ⛔ từ mã mô hình (bia `AG-R1-01`).

    Phát lại ⇒ trường `nguon_tra_loi` ghi trong tệp phát lại (hôm nay `gia-lap`); bọc ghi ⇒ nhà cung cấp gốc.
    """
    ra: dict[str, dict[str, Any]] = {}
    for ma, n in ncc.items():
        if isinstance(n, mh.PhatLai):
            ra[ma] = {"nguon_tra_loi": str(n.dau.get("nguon_tra_loi", "⛔ rõ")), "che_do": "phat-lai"}
        elif isinstance(n, mh.GhiLai):
            ra[ma] = {"nguon_tra_loi": n.goc.ten, "che_do": "ghi"}
        else:
            ra[ma] = {"nguon_tra_loi": getattr(n, "ten", "⛔ rõ"), "che_do": "truc-tiep"}
    return ra


def sinh_report(kc: ch.KqChuoi, may: dict, dap_an: dict, nhan_be: str, ncc: dict[str, Any],
                ngay: str | None = None) -> tuple[str, dict[str, Any]]:
    return rp.sinh(kc, phien_ban_cua(ncc), as_is_co_ten(may), g0_tong_hop(kc, dap_an, nhan_be),
                   {"voi_so_luong.json": (may.get("voi") or {}).get("nguon", {}).get("so_dong_bang", "VẮNG")
                    if may.get("voi") else "VẮNG", "hd2_cong.json": "có" if may.get("hd2") else "VẮNG"},
                   ngay or date.today().isoformat(), may=may)


def chay(che_do: str = "phat_lai", che: str | None = None, co_that: bool = False,
         tep_voi: Path = TEP_VOI, tep_hd2: Path = TEP_HD2, fx: Path = FX, ncc: dict | None = None,
         cho_heldout: bool = True) -> tuple[ch.KqChuoi, dict, dict, str]:
    ca, dap_an, nhan_be = bo_ca(cho_heldout)
    cc = dung_cong_cu(tep_voi, tep_hd2, fx, ca)
    may = dung_may(tep_voi, tep_hd2, fx)
    ncc = ncc if ncc is not None else ncc_cho(che_do, co_that)
    kc = ch.chay_chuoi(ncc, cc, may, dap_an=dap_an, che_do=che)
    return kc, may, dap_an, nhan_be


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="chay_agent_voi.py")
    p.add_argument("--gia", action="store_true", help="mô hình GIẢ tất định (thay phát lại)")
    p.add_argument("--that", action="store_true",
                   help="gọi API THẬT — FLS_CHO_GOI_API=1 + đường (FLS_NHA_CUNG_CAP=google-cloud: "
                        "FLS_GCP_PROJECT · FLS_CLAUDE_WORKSPACE_ID · FLS_GC_DU_LIEU_XAC_NHAN=1 ở `mo`) | vertex | anthropic (vắng ⇒ anthropic)")
    p.add_argument("--tran-usd", type=float, default=TRAN_USD_MAC_DINH, help="trần USD ƯỚC của cả vòng — chặn lời gọi KẾ khi tổng đã tiêu ≥ trần; ⛔ cắt lời gọi ĐANG chạy (một lời có thể vượt trần — AG2-R1-03)")
    p.add_argument("--ghi-phat-lai", action="store_true", help="(với --gia) ghi docs/ITL/06_Agent/phat_lai/*.json")
    p.add_argument("--ghi-report", action="store_true", help="ghi docs/ITL/06_Agent/report.html")
    p.add_argument("--che", choices=("mo", "che_noi_dung", "che_het"), default=None,
                   help="chế độ che (mặc định `mo` — chủ 23/11: agent đọc toàn bộ nội dung + số TK)")
    a = p.parse_args(argv)
    che_do = "that" if a.that else ("gia" if a.gia else "phat_lai")
    try:
        ncc = ncc_cho(che_do, a.that, che=a.che, tran_usd=a.tran_usd)
    except (mh.CamGoiThat, mh.ChuaDung, mh.KhongCoBanGhi) as e:
        print(f"⛔ {type(e).__name__}: {e}")
        return 2
    if a.ghi_phat_lai:
        if che_do != "gia":
            print("⛔ --ghi-phat-lai chỉ đi với --gia")
            return 2
        ncc = {k: mh.GhiLai(v) for k, v in ncc.items()}
    kc, may, dap_an, nhan_be = chay(che_do, a.che, a.that, ncc=ncc)
    html_, tom = sinh_report(kc, may, dap_an, nhan_be, ncc)
    print("KẾT: " + rp.dong_ket(tom))
    if kc.dung_o:
        print("  ⛔", kc.dung_o)
    for ag in kc.agents:
        for ks in ag.skills:
            tt = "⛔ " + ks.loi if ks.loi else ("chưa chạy" if ks.dat_cong is None else
                                                ("ĐẠT" if ks.dat_cong else "ĐỎ") + " · " + ks.ly_do)
            print(f"  {ks.skill.nhan:32s} {tt}")
    if che_do == "that":
        t = mh.tong_nhat_ky(nhat_ky_cua(ncc))
        print(f"  API THẬT: {t['so_goi']} lời gọi · token vào {t['token_vao']} · ra {t['token_ra']} · cache đọc "
              f"{t['cache_doc']} · ghi {t['cache_ghi']} · {t['giay']} s · {nhan_usd(t)}"
              f" · đường {'/'.join(t['duong']) or '—'}{' · vùng ' + '/'.join(t['vung']) if t['vung'] else ''}")
        p_ = ghi_nhat_ky(ncc, f"chuoi_{a.che or ch.che_mod.CHE_DO_MAC_DINH}")
        if p_:
            print(f"  đã ghi nhật ký {p_.relative_to(GOC) if p_.is_relative_to(GOC) else p_}")
    if a.ghi_phat_lai:
        ghi_phat_lai(ncc)
        print(f"  đã ghi bản phát lại: {TM_PHAT_LAI.relative_to(GOC)}/")
    if a.ghi_report:
        TEP_REPORT.write_text(html_, encoding="utf-8")
        print(f"  đã ghi {TEP_REPORT.relative_to(GOC)}")
    return 0 if tom["dat"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
