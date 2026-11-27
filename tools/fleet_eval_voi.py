# -*- coding: utf-8 -*-
"""Fleet eval NHIỀU VÒNG cho skill ghép theo NỘI DUNG (A2.04) — thẻ `a3-1-ref.eval.ghep-sai`.

    python tools/fleet_eval_voi.py                 # chạy các vòng khai ở VONG (giả), in bảng, ⛔ ghi
    python tools/fleet_eval_voi.py --ghi           # + ghi docs/ITL/05_FleetEval/vong/*.json + TONG_HOP.md
    python tools/fleet_eval_voi.py --be-giu-rieng [--ghi]   # WO-338: bể A (dữ liệu CŨ) ↔ bể B (THẬT hiện tại), GIẢ/phát lại
    python tools/fleet_eval_voi.py --ma-tran [--ghi]        # WO-367: ma trận ứng viên OpenRouter × bể — GIẢ (127.0.0.1)
    python tools/fleet_eval_voi.py --ma-tran --that --tran-usd 2 [--tran-usd-mo-hinh 1] [--ung-vien a/x,b/y] [--ghi]

⭐ Một VÒNG = một PHIÊN BẢN đóng băng (mã mô hình ghim + checksum prompt A2 + checksum bể ca + cờ nội dung)
   chạy trên CÙNG bể ca, chấm MÙ (bộ chấm thấy mã ca xáo, ⛔ tên agent/phiên bản), so với vòng trước và `v0`.
   Quy tắc dừng (thẻ `_chung`): Ship = đạt bar + ⛔ tệ hơn v0/bản trước · Chặn = một ca "phải để người" bị nối.
⭐ Hôm nay mọi vòng chạy bằng mô hình GIẢ (`ghep_noi_dung.luat_gia_v1` đứng thay) trên bể ca DỰNG — đó là
   chạy thử bộ máy, ⛔ số đo mô hình. Vòng THẬT cần: bể giữ riêng (`FLS_HELDOUT_NOI_DUNG`), chủ chốt C1–C4
   (BG-330), rồi `--that` + `FLS_CHO_GOI_API=1` + khoá — ⛔ trong WO-329.
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

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "tools"))

from fls.agent import chuoi as ch  # noqa: E402
from fls.agent import ghep_noi_dung as gnd  # noqa: E402
from fls.agent import mo_hinh as mh  # noqa: E402
from fls.agent.skill import checksum_prompt, he_thong, nap_bo  # noqa: E402

import chay_agent_voi as cav  # noqa: E402

TM_VONG = GOC / "docs" / "ITL" / "05_FleetEval" / "vong"
#: (mã phiên bản, luật đứng thay mô hình, cờ gửi nội dung đã che). Thêm vòng = thêm MỘT dòng.
VONG = (
    ("v0-ma-tat-dinh", gnd.luat_v0, "che_het"),
    ("v1-gia-che-het", gnd.luat_gia_v1, "che_het"),
    ("v1-gia-che-noi-dung", gnd.luat_gia_v1, "che_noi_dung"),
    ("v1-gia-mo", gnd.luat_gia_v1, "mo"),           # chủ 23/11: mặc định — nội dung + số TK nguyên văn
)
#: Bar (thẻ a3-1-ref, đề xuất): 0 ca "phải để người" bị nối · tỉ lệ nối sai ≤ v0 (v0 0/0 ⇒ bar = 0).
BAR_PHAI_NGUOI_BI_NOI = 0


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _cham_mu(ra: dict, dap_an: dict, hat: int = 23) -> tuple[list[dict], dict]:
    """chấm MÙ: xáo mã ca (hạt cố định), bộ chấm chỉ thấy mã xáo."""
    ma_ca = sorted(dap_an["noi"])
    xao = ma_ca[:]
    random.Random(hat).shuffle(xao)
    doi = {c: f"x{i:03d}" for i, c in enumerate(xao)}
    chon_mu = {f"noi:{doi[c]}.{f}": ra.get(f"noi:{c}.{f}") for c in ma_ca for f in ("chon", "ly_do")}
    dap_mu = {f"noi:{doi[c]}.{f}": v for c, b in dap_an["noi"].items() for f, v in b.items()}
    cham = gnd.cham(chon_mu, dap_mu)
    nguoc = {v: k for k, v in doi.items()}
    for x in cham:
        x["ca"] = nguoc[x["ca"]]
    return cham, gnd.tong_hop(cham)


def chay_vong(ma: str, luat, che_do: str, ca: dict, dap_an: dict, hat: int = 23, ncc=None) -> dict:
    """MỘT vòng QUA `chay_skill` (cổng skill + chốt + bộ che theo `che_do`). ⭐ `HELD-R1-06`: bản R0 có nhánh
    `khong_che` đọc thẳng `luat(cav.o_ca(ca))` ⇒ BỎ cổng skill — vòng ấy đo LUẬT, ⛔ đo đường ống. Chế độ
    chính theo chủ 23/11 ~06:00 ("agent đọc TOÀN BỘ nội dung + số TK") nay là `che_do="mo"` — đi ĐÚNG đường ống.
    ⭐ `WO-355`: `ncc` tiêm được (adapter THẬT `claude-opus-5-5`) — CÙNG `chay_skill`, CÙNG bộ chấm mù; `None` ⇒ GIẢ(`luat`)."""
    s = [x for x in nap_bo("A2_PR_MAP") if x.loai == "bong"][0]
    dn = [a for a in ch.AGENT if a.ma == "A2_PR_MAP"][0]
    that = ncc is not None
    ks = ch.chay_skill(dn, he_thong(dn.ma), s, ncc if that else mh.GiaLap({"ung_vien_ghep": luat}),
                       {"ung_vien_ghep": lambda: cav.o_ca(ca)}, che_do=che_do)
    if ks.loi and ks.loi.startswith("CamGui") and che_do != CHE_CHINH:
        # Lớp 2 của bộ che TỪ CHỐI gửi (số dài còn sót sau che) — chế độ che là TUỲ CHỌN, nên đây là KẾT QUẢ ĐO của che
        # (đo 23/11 trên bể thật: che_noi_dung để lọt dãy số DÍNH CHỮ ⇒ bị chặn), ⛔ lỗi hạ tầng làm dừng cả vòng.
        return {"phien_ban": ma, "che_do": che_do, "bi_cam_gui": ks.loi[:160]}
    if ks.loi or ks.ra is None:
        return {"phien_ban": ma, "loi": ks.loi or "⛔ đầu ra"}
    cham, th = _cham_mu(ks.ra, dap_an, hat)
    return {"phien_ban": ma, "mo_hinh": (f"THẬT {dn.mo_hinh.ma}" if that else f"GIẢ ({luat.__name__}) thay {dn.mo_hinh.ma}"),
            "checksum_prompt": checksum_prompt("A2_PR_MAP"), "che_do": che_do,
            "cong_skill": {"dat": ks.dat_cong, "ly_do": ks.ly_do}, "the_noi_dung_che": ks.the_noi_dung,
            "tong_hop": th, "theo_nhom": {n: gnd.tong_hop([x for x in cham if x["nhom"] == n])
                                          for n in ("phai_noi", "phai_nguoi")},
            "cham": cham}


def phan_xu(ds: list[dict]) -> list[dict]:
    v0 = ds[0]["tong_hop"]
    ra = []
    for i, v in enumerate(ds):
        th = v["tong_hop"]
        truoc = ds[i - 1]["tong_hop"] if i else None
        chan = th["phai_nguoi_bi_noi"] > BAR_PHAI_NGUOI_BI_NOI
        te_hon_v0 = (th["ti_le_noi_sai"] or 0) > (v0["ti_le_noi_sai"] or 0)
        te_hon_truoc = truoc is not None and (th["diem_tb"] or 0) < (truoc["diem_tb"] or 0)
        ra.append({"phien_ban": v["phien_ban"], "chan": chan, "te_hon_v0": te_hon_v0, "te_hon_truoc": te_hon_truoc,
                   "ket": "CHẶN" if chan else ("⛔ SHIP (tệ hơn)" if te_hon_v0 or te_hon_truoc else "ĐẠT bar")})
    return ra


# ───────────────────────────── WO-338 · bể GIỮ RIÊNG (A ↔ B) ─────────────────────────────
BIEN_BE = cav.BIEN_HELDOUT
TEP_BE_MD = TM_VONG / "BE_GIU_RIENG.md"
TEP_BE_JSON = TM_VONG / "BE_GIU_RIENG.json"
TEP_DEM_BE = GOC / "docs" / "ITL" / "05_FleetEval" / "be" / "DEM_BE.json"
#: Chủ 23/11 ~06:00: chế độ CHÍNH = agent đọc TOÀN BỘ nội dung + số TK = `che_do="mo"` = vòng `v1-gia-mo` ở `VONG`
#: (⛔ còn vòng riêng "KHÔNG CHE" bỏ cổng skill — `HELD-R1-06`). Che là TUỲ CHỌN: hai vòng `che_noi_dung` · `che_het`.
CHE_CHINH = "mo"
CHE_CHUOI = ("mo", "che_noi_dung", "che_het")        # chuỗi 4 agent: chính trước, rồi hai mức che tuỳ chọn
NHOM_CHINH = ("phai_noi", "phai_nguoi", "l3")        # `chua_chot` ⛔ vào recall chính (WO-338 AC-7)


def tong_hop_be(cham: list[dict]) -> dict:
    """Chỉ số vòng trên bể giữ riêng. `chua_chot` TÁCH RA: đếm agent nối bao nhiêu, ⛔ tính recall."""
    chinh = [x for x in cham if x["nhom"] in NHOM_CHINH]
    ck = [x for x in cham if x["nhom"] == "chua_chot"]
    th = gnd.tong_hop(chinh)
    th["l3_bi_noi"] = sum(1 for x in chinh if x["nhom"] == "l3" and x["noi"])
    th["mau_so_chinh"] = len(chinh)
    th["so_phai_noi"] = sum(1 for x in chinh if x["nhom"] == "phai_noi")
    th["chua_chot"] = {"so_ca": len(ck), "agent_noi": sum(1 for x in ck if x["noi"])}
    return th


def chay_chuoi_be(thu_muc: Path, che_do: str) -> dict:
    """AC-6: chuỗi 4 agent ở chế độ GIẢ trên bể (⛔ API thật) ⇒ ô khớp/lệch agent ↔ máy + G0 của A2.04."""
    from fls.agent import report as rp
    cu = os.environ.get(BIEN_BE)
    os.environ[BIEN_BE] = str(thu_muc)
    try:
        ncc = cav.ncc_cho("gia")
        kc, may, dap_an, nhan = cav.chay("gia", che_do, ncc=ncc)
        _, tom = cav.sinh_report(kc, may, dap_an, nhan, ncc)
        return {"mau_so": tom["mau_so"], "khop": tom["khop"], "lech": tom["LECH"], "khong_do_duoc": tom["KHONG_DO_DUOC"],
                "doc_lap": tom["doc_lap"], "vong_tron": tom["vong_tron"],
                "agent_dat": f"{tom['agent_dat']}/{tom['agent']}", "dung_o": list(kc.dung_o or []),
                "g0": cav.g0_tong_hop(kc, dap_an, nhan)}
    except Exception as e:                            # noqa: BLE001 — lỗi = ĐỎ có tên, ⛔ nuốt
        return {"loi": f"{type(e).__name__}: {str(e)[:120]}"}
    finally:
        if cu is None:
            os.environ.pop(BIEN_BE, None)
        else:
            os.environ[BIEN_BE] = cu


def chay_be(thu_muc: Path) -> dict:
    ca = json.loads((thu_muc / "ca.json").read_text(encoding="utf-8"))
    dap_an = json.loads((thu_muc / "dap_an.json").read_text(encoding="utf-8"))
    vong = []
    for m, luat, che in VONG:
        v = chay_vong(m, luat, che, ca, dap_an)
        if "loi" in v:
            return {"loi": v["loi"]}
        if "bi_cam_gui" in v:                          # che tuỳ chọn bị lớp 2 chặn ⇒ có TÊN, ⛔ số giả
            v["be"], v["theo_nhom_be"] = None, None
            vong.append(v)
            continue
        v["be"] = tong_hop_be(v["cham"])
        v["theo_nhom_be"] = {n: gnd.tong_hop([x for x in v["cham"] if x["nhom"] == n]) for n in NHOM_CHINH}
        v.pop("cham")
        vong.append(v)
    return {"vong": vong, "chuoi": {c: chay_chuoi_be(thu_muc, c) for c in CHE_CHUOI}}


def _x(v) -> str:
    return "—" if v is None else str(v)


def md_be(kq: dict, dem: dict) -> str:
    hom = date.today().isoformat()
    cot = ("a", "b")
    L = [f"# Fleet eval — bể GIỮ RIÊNG · bể A (dữ liệu CŨ) ↔ bể B (dữ liệu THẬT hiện tại) · {hom}", "",
         "⚠ **Report đo ĐƯỜNG ỐNG + CỔNG, ⛔ chất lượng mô hình**: agent = mô hình GIẢ tất định (`luat_v0` · `luat_gia_v1`), "
         "⛔ gọi API thật. Chỉ số, ⛔ nội dung giao dịch. Sinh bởi `python tools/fleet_eval_voi.py --be-giu-rieng --ghi` (⛔ sửa tay).", "",
         "| | bể A · dữ liệu CŨ | bể B · dữ liệu THẬT hiện tại |", "|---|---|---|"]
    row = lambda ten, f: L.append(f"| {ten} | " + " | ".join(f(c) for c in cot) + " |")      # noqa: E731
    d = dem["be"]
    row("kỳ ĐÃ CHỐT (số kỳ) · kỳ ĐANG MỞ", lambda c: f"{len(d[c]['ky_chot'])} · {len(d[c]['ky_mo'])}")
    row("ca / mong *(số MÃ tham chiếu; L3·chuyển·chưa chốt = số DÒNG bank)*", lambda c: f"{d[c]['tong_ca']} / {d[c]['mong_tong']}")
    for t in list(d["a"]["mong_theo_tang"]) + ["chua_chot"]:
        row(f"· tầng `{t}` (thực / mong)", lambda c, t=t: (f"{d[c]['thuc_theo_tang'].get(t, 0)} / {d[c]['mong_theo_tang'][t]}"
                                                           if t in d[c]["mong_theo_tang"] else "—"))
    row("ca nhóm `phai_noi` · `phai_nguoi` · `l3` · `chua_chot`", lambda c: " · ".join(
        str(d[c]["theo_nhom"].get(n, 0)) for n in ("phai_noi", "phai_nguoi", "l3", "chua_chot")))
    row("độc lập: trùng ca dựng WO-329 · trùng prompt/ví dụ agent", lambda c: (
        f"{d[c]['doc_lap']['trung_ca_dung_wo329']} · {d[c]['doc_lap']['trung_prompt_agent']}"))
    L += ["", "## Vòng GIẢ trên bể (recall CHÍNH = nhóm `phai_noi`; `chua_chot` ⛔ vào)", "",
          "| phiên bản (nội dung) | chỉ số | bể A | bể B |", "|---|---|---|---|"]
    for i, (m, _, cho) in enumerate(VONG):
        nhan = f"`{m}` (`{cho}`{' · CHÍNH' if cho == CHE_CHINH else ''})"
        if any(kq[c]["vong"][i].get("be") is None for c in cot):
            L.append(f"| {nhan} | **bị lớp 2 chặn (`CamGui`)** — ⛔ có số | " + " | ".join(
                ("⛔ " + kq[c]["vong"][i]["bi_cam_gui"].split("—")[-1].strip()[:70]) if kq[c]["vong"][i].get("be") is None
                else "đã chạy" for c in cot) + " |")
            continue
        for ten, k in (("mẫu số chính (ca)", "mau_so_chinh"), ("nối", "so_noi"), ("nối sai", "noi_sai"), ("tỉ lệ nối sai", "ti_le_noi_sai"),
                       ("recall phải-nối", "recall_phai_noi"), ("ca phải-để-người bị nối", "phai_nguoi_bi_noi"),
                       ("L3 bị nối", "l3_bi_noi"), ("điểm TB (0–2)", "diem_tb")):
            L.append(f"| {nhan if k == 'mau_so_chinh' else ''} | {ten} | " + " | ".join(
                _x(kq[c]["vong"][i]["be"][k]) for c in cot) + " |")
        L.append("| | `chua_chot`: ca · agent nối *(⛔ recall)* | " + " | ".join(
            f"{kq[c]['vong'][i]['be']['chua_chot']['so_ca']} · {kq[c]['vong'][i]['be']['chua_chot']['agent_noi']}" for c in cot) + " |")
    L += ["", "## Chuỗi 4 agent (GIẢ) — ô khớp ↔ máy *(mẫu số cổ định: các ô máy không phụ thuộc bể; phần phụ thuộc bể = G0 A2.04)*", "",
          "| chế độ che | chỉ số | bể A | bể B |", "|---|---|---|---|"]
    for k, nh in ((c, f"`{c}`{' · CHÍNH' if c == CHE_CHINH else ''}") for c in CHE_CHUOI):
        L.append(f"| {nh} | khớp / mẫu số · lệch · ⛔ đo được | " + " | ".join(
            (f"{kq[c]['chuoi'][k]['khop']}/{kq[c]['chuoi'][k]['mau_so']} · {kq[c]['chuoi'][k]['lech']} · {kq[c]['chuoi'][k]['khong_do_duoc']}"
             if "loi" not in kq[c]["chuoi"][k] else "⛔ " + kq[c]["chuoi"][k]["loi"]) for c in cot) + " |")
        L.append(f"| {nh} | G0 A2.04: nối · sai · recall · người-bị-nối | " + " | ".join(
            (lambda g: f"{g.get('so_noi')} · {g.get('noi_sai')} · {g.get('recall_phai_noi')} · {g.get('phai_nguoi_bi_noi')}")(
                kq[c]["chuoi"][k].get("g0") or {}) for c in cot) + " |")
    dc = dem["doi_chieu_A_B"]
    L += ["", "## Đối chiếu kỳ ĐÃ CHỐT A ↔ B", "",
          f"- kết: **{dc['ket']}**",
          f"- tập kỳ chốt A = B: **{dc['ky_chot_A'] == dc['ky_chot_B']}** *(A {len(dc['ky_chot_A'])} kỳ · B {len(dc['ky_chot_B'])} kỳ)*",
          ]
    lg = dc["ledge_song_vs_dong_bang"]
    if lg["mau_so_o_ngay_song"] == 0:                  # Đ3: mẫu số 0 ⇒ phép đo ⛔ có nghĩa, ⛔ in "lệch 26 kỳ"
        L.append(f"- Ledge Final đọc hôm nay ↔ ảnh đóng băng DT12: **⛔ đo được** (mẫu số 0 ô ngày giải mã; lát hỏng "
                 f"{len(lg.get('lat_ledge_hong', []))} — đọc Ledge hết giờ liên tục) ⇒ ĐỎ, ⛔ coi là KHỚP")
        tt = lg.get("thay_the_bank_song_vs_ledge_dong_bang") or {}
        kl = tt.get("ky_lech", {})
        L.append(f"- phép THAY THẾ *(khác vật đo)*: dòng bank sống ở `Mapping L1` ↔ dòng Ledge đóng băng, trên {tt.get('mau_so_ky')} kỳ — "
                 f"lệch **{len(kl)}** kỳ: " + ", ".join(f"`{k}` bank {v['bank_song']} · Ledge {v['ledge_dong_bang']}" for k, v in kl.items()))
    else:
        L.append(f"- Ledge Final đọc hôm nay ↔ ảnh đóng băng DT12 — kỳ ĐÃ CHỐT lệch số dòng: **{len(lg['ky_lech_ky_chot'])}**/"
                 f"{lg['so_ky_chot_so_sanh']} {sorted(lg['ky_lech_ky_chot'])} *(mẫu số: {lg['mau_so_o_ngay_song']} ô ngày)*; "
                 f"kỳ ĐANG MỞ (nhận thêm dòng sau ảnh — lớn lên là đúng): {len(lg['ky_lech_ky_mo'])} "
                 + ", ".join(f"`{k}` ảnh {v['dong_bang']} · sống {v['song']}" for k, v in sorted(lg['ky_lech_ky_mo'].items())))
    return "\n".join(L) + "\n"


def main_be(ghi: bool) -> int:
    tm = os.environ.get(BIEN_BE)
    if not tm or not (Path(tm) / "a" / "ca.json").exists() or not (Path(tm) / "b" / "ca.json").exists():
        print(f"⛔ ĐỎ (⛔ đo được): thiếu bể giữ riêng — đặt ${BIEN_BE}=<thư mục chứa a/ và b/> (dựng bằng tools/dung_be_giu_rieng.py)")
        return 2
    if not TEP_DEM_BE.exists():
        print("⛔ ĐỎ: thiếu docs/ITL/05_FleetEval/be/DEM_BE.json")
        return 2
    dem = json.loads(TEP_DEM_BE.read_text(encoding="utf-8"))
    kq = {c: chay_be(Path(tm) / c) for c in ("a", "b")}
    if any("loi" in v for v in kq.values()):
        print("⛔ vòng lỗi:", {c: v.get("loi") for c, v in kq.items()})
        return 1
    chan = False
    for c in ("a", "b"):
        print(f"── bể {c.upper()} · {dem['be'][c]['tong_ca']}/{dem['be'][c]['mong_tong']} ca ──")
        for (m, _, cho), v in zip(VONG, kq[c]["vong"]):
            t = v["be"]
            if t is None:
                print(f"  {m:24s} {cho:12s} ⛔ bị lớp 2 chặn: {v['bi_cam_gui'][:110]}")
                continue
            chan |= t["phai_nguoi_bi_noi"] > BAR_PHAI_NGUOI_BI_NOI
            print(f"  {m:24s} {cho:12s} nối {t['so_noi']:3d} sai {t['noi_sai']:3d} recall {_x(t['recall_phai_noi']):>6s} "
                  f"người-bị-nối {t['phai_nguoi_bi_noi']} L3-bị-nối {t['l3_bi_noi']} chưa-chốt-nối {t['chua_chot']['agent_noi']}/{t['chua_chot']['so_ca']}")
    print("đối chiếu kỳ A↔B:", dem["doi_chieu_A_B"]["ket"])
    if ghi:
        TM_VONG.mkdir(parents=True, exist_ok=True)
        TEP_BE_MD.write_text(md_be(kq, dem), encoding="utf-8")
        TEP_BE_JSON.write_text(json.dumps({"ngay": date.today().isoformat(), "doi_chieu_A_B": dem["doi_chieu_A_B"]["ket"], "kq": kq},
                                          ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
        print(f"  đã ghi {TEP_BE_MD.relative_to(GOC)} · {TEP_BE_JSON.relative_to(GOC)}")
    đỏ = chan or dem["doi_chieu_A_B"]["ket"] != "KHỚP" or any(dem["be"][c]["thieu"] for c in ("a", "b"))
    return 1 if đỏ else 0


# ───────────────────────── WO-367 · MA TRẬN ứng viên OpenRouter × bể (A2.04) ─────────────────────────
#: ⭐ Mỗi Ô = CÙNG bộ ca, CÙNG skill A2.04 (`bong`), CÙNG bộ che `mo`, CÙNG chấm MÙ bằng MÃ (`_cham_mu` so với ĐÁP ÁN giữ riêng
#:    — số máy đã đo) — CHỈ đổi mô hình. ⛔ mô hình nào chấm câu trả lời của mình hay của mô hình khác.
#: ⭐ Trần: TỔNG cả lượt (`--tran-usd`) + RIÊNG mỗi mô hình (`--tran-usd-mo-hinh`) — kiểm TRƯỚC mỗi lời gọi (`VuotTran` chặn
#:    lời KẾ). Chạm trần TỔNG ⇒ mọi ô còn lại `bo_qua` có tên; chạm trần MÔ HÌNH ⇒ chỉ các ô còn lại của mô hình ấy.
#: ⭐ `AG3-R1-01`: chế độ THẬT ghi nhật ký trên MỌI lối thoát (trả về · `LoiApi`/`VuotTran` trong ô · ngoại lệ chưa lường).
TEP_MT_MD = TM_VONG / "MA_TRAN_OPENROUTER.md"
TEP_MT_JSON = TM_VONG / "MA_TRAN_OPENROUTER.json"
HAT_MA_TRAN = 367


class _GiuNhatKy:
    """Vỏ cho `cav.ghi_nhat_ky` (đọc `nhat_ky` từ nhà cung cấp) — ma trận dùng MỘT danh sách chung cho mọi ô."""
    def __init__(self, nk: list):
        self.nhat_ky = nk


def be_ma_tran(be: Path | None) -> tuple[dict[str, tuple[dict, dict]], str]:
    """Bể của ma trận: `a`/`b` giữ riêng nếu có; VẮNG ⇒ MỘT bể `dung` = 12 ca DỰNG, report KHAI rõ (⛔ im lặng)."""
    if be is not None and all((be / c / "ca.json").exists() for c in ("a", "b")):
        return ({c: (json.loads((be / c / "ca.json").read_text(encoding="utf-8")),
                     json.loads((be / c / "dap_an.json").read_text(encoding="utf-8"))) for c in ("a", "b")},
                "bể giữ riêng A (dữ liệu CŨ) · B (THẬT hiện tại) — ngoài repo")
    ca, dap, nhan = cav.bo_ca(cho_heldout=False)
    return {"dung": (ca, dap)}, f"⚠ bể giữ riêng A/B VẮNG (${BIEN_BE}/a · /b) ⇒ chỉ bể `dung` = {nhan} — ⛔ thay được bể A/B"


def _o_tu_nhat_ky(ds: list) -> dict:
    t = mh.tong_nhat_ky(ds)
    return {"so_goi": t["so_goi"], "token_vao": t["token_vao"], "token_ra": t["token_ra"], "cache_doc": t["cache_doc"],
            "usd": t["chi_phi_usd"], "nguon_usd": t.get("nguon_usd") or {}, "giay_api": t["giay"]}


def chay_ma_tran(ung_vien: list[str], be_ds: dict[str, tuple[dict, dict]], dung_ncc, nk: list) -> dict:
    """`dung_ncc(slug, nk)` ⇒ adapter (thật hoặc tới máy chủ GIẢ). Lỗi dựng (thiếu chốt) ⇒ ô `do` CÓ TÊN, ⛔ gọi."""
    import time
    o: dict[str, dict[str, dict]] = {}
    dung_tong = ""
    for slug in ung_vien:
        o[slug] = {}
        try:
            ncc = dung_ncc(slug, nk)
        except (mh.CamGoiThat, mh.ChuaDung) as e:
            for b in be_ds:
                o[slug][b] = {"do": f"{type(e).__name__}: {e}"}
            continue
        dung_mh = ""
        for b, (ca, dap) in be_ds.items():
            if dung_tong or dung_mh:
                o[slug][b] = {"bo_qua": dung_tong or dung_mh}
                continue
            n0, t0 = len(nk), time.monotonic()
            v = chay_vong(f"or:{slug}", gnd.luat_gia_v1, CHE_CHINH, ca, dap, ncc=ncc)
            o_b: dict = {"giay": round(time.monotonic() - t0, 3), **_o_tu_nhat_ky(nk[n0:])}
            loi = v.get("loi") or v.get("bi_cam_gui")
            if loi:
                o_b["loi"] = loi[:240]
                if loi.startswith("VuotTran"):
                    if "trần TỔNG" in loi:
                        dung_tong = "trần TỔNG đã chạm — " + loi[:160]
                    else:
                        dung_mh = "trần MÔ HÌNH đã chạm — " + loi[:160]
            else:
                th = tong_hop_be(v["cham"])
                o_b.update({k: th[k] for k in ("mau_so_chinh", "so_noi", "noi_sai", "recall_phai_noi", "phai_nguoi_bi_noi",
                                               "l3_bi_noi", "diem_tb", "ti_le_noi_sai")})
                o_b["noi_dung"] = th["so_noi"] - th["noi_sai"]
            o[slug][b] = o_b
    return o


def ket_ma_tran(o: dict) -> tuple[bool, list[str]]:
    """Đ5 — mong khai trước: MỌI ô CHẠY (⛔ thiếu chốt · lỗi · vượt trần · bỏ qua) và 0 ca phải-để-người bị nối ở mọi ô."""
    do = []
    for slug, cot in o.items():
        for b, x in cot.items():
            for k in ("do", "loi", "bo_qua"):
                if k in x:
                    do.append(f"`{slug}` × `{b}`: {k} — {x[k][:120]}")
            if (x.get("phai_nguoi_bi_noi") or 0) > BAR_PHAI_NGUOI_BI_NOI:
                do.append(f"`{slug}` × `{b}`: {x['phai_nguoi_bi_noi']} ca phải-để-người bị nối (bar 0)")
    if not o:
        do.append("0 ứng viên (Đ3: ma trận RỖNG ⛔ là ĐẠT)")
    return not do, do


def nhan_usd_ma_tran(x: dict, che_do: str = "that") -> str:
    n = x.get("nguon_usd") or {}
    if not x.get("so_goi"):
        return "—"
    if che_do != "that":                       # số do máy chủ GIẢ trả ⇒ ⛔ được mang nhãn THẬT
        return f"{x['usd']} · GIẢ (máy chủ 127.0.0.1 — ⛔ tiền)"
    nhan = "THẬT (usage.cost OpenRouter trả)" if not n.get(mh.NGUON_USD_UOC) else (
        "ƯỚC (bảng giá × token)" if not n.get(mh.NGUON_USD_THAT) else
        f"{n[mh.NGUON_USD_THAT]} lời THẬT + {n[mh.NGUON_USD_UOC]} lời ƯỚC")
    return f"{x['usd']} · {nhan}"


def md_ma_tran(kq: dict, truoc: dict | None) -> str:
    dat, ly = ket_ma_tran(kq["o"])
    be = list(next(iter(kq["o"].values()), {}).keys())
    L = [f"# Fleet eval ĐA MÔ HÌNH qua OpenRouter — A2.04 · {kq['ngay']}", "",
         f"> Sinh bởi `python tools/fleet_eval_voi.py --ma-tran {'--that ' if kq['che_do'] == 'that' else ''}--ghi` "
         "(`WO-367` AC-4) — ⛔ sửa tay. CHỈ số đếm; ⛔ nội dung giao dịch, ⛔ phản hồi mô hình.", "",
         f"**Chế độ: {'THẬT — API OpenRouter' if kq['che_do'] == 'that' else 'GIẢ — adapter THẬT ↔ máy chủ OpenRouter GIẢ 127.0.0.1 (luat_gia_v1 đứng thay MỌI mô hình) ⇒ số đo ĐƯỜNG ỐNG, ⛔ chất lượng mô hình'}**", "",
         f"**KẾT: {'ĐẠT' if dat else 'ĐỎ'}**" + ("" if dat else " — " + " · ".join(x.replace('|', '\\|') for x in ly)), "",
         "Mong (khai trước, Đ5): MỌI ô chạy (⛔ thiếu chốt · lỗi · vượt trần · bỏ qua) · 0 ca phải-để-người bị nối ở mọi ô.", "",
         "| | |", "|---|---|",
         f"| bể | {kq['be']} |", f"| ứng viên | {' · '.join(f'`{s}`' for s in kq['o'])} |",
         f"| chấm | MÃ `_cham_mu` ↔ đáp án giữ riêng (⛔ mô hình chấm) · che `{CHE_CHINH}` · skill A2.04 checksum `{kq['checksum_prompt']}` |",
         f"| trần USD | tổng {kq['tran_usd']} · mỗi mô hình {kq['tran_usd_mo_hinh']} — chặn lời KẾ (⛔ cắt lời đang chạy) |",
         f"| định tuyến mỗi lời | `provider = {json.dumps(mh.DINH_TUYEN_OPENROUTER)}` |", "",
         "## Ma trận mô hình × bể", "",
         "| mô hình | bể | ca (mẫu số chính) | nối ĐÚNG | nối SAI | phải-để-người bị nối | recall phải-nối | điểm TB 0–2 | lỗi / bỏ qua | lời gọi | token vào/ra | USD + nguồn | giây |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for slug, cot in kq["o"].items():
        for b, x in cot.items():
            loi = x.get("do") or x.get("loi") or x.get("bo_qua")
            L.append(f"| `{slug}` | `{b}` | " + " | ".join(_x(x.get(k)) for k in ("mau_so_chinh", "noi_dung", "noi_sai",
                                                                                     "phai_nguoi_bi_noi", "recall_phai_noi", "diem_tb"))
                     + f" | {('⛔ ' + loi[:90].replace('|', '/')) if loi else '—'} | {_x(x.get('so_goi'))} | "
                     f"{_x(x.get('token_vao'))}/{_x(x.get('token_ra'))} | {nhan_usd_ma_tran(x, kq['che_do'])} | {_x(x.get('giay'))} |")
    t = kq["nhat_ky"]
    L += ["", f"Tổng: **{t['so_goi']}** lời gọi · token vào {t['token_vao']} / ra {t['token_ra']} · "
          + (f"USD {t['chi_phi_usd']} (nguồn {t.get('nguon_usd') or '—'}; bảng giá dự phòng tra {mh.NGAY_TRA_GIA_OPENROUTER})."
           if kq["che_do"] == "that" else f"USD {t['chi_phi_usd']} GIẢ (máy chủ cục bộ — ⛔ tiền, ⛔ giá thật)."), "",
          "## So ngược bản trước", ""]
    if not truoc:
        L.append("⛔ có bản trước (`MA_TRAN_OPENROUTER.json` vắng) — lượt đầu.")
    else:
        L += [f"Bản trước: {truoc.get('ngay')} · chế độ {truoc.get('che_do')}.", "",
              "| mô hình | bể | điểm TB trước → nay | nối SAI trước → nay | USD trước → nay |", "|---|---|---|---|---|"]
        for slug, cot in kq["o"].items():
            for b, x in cot.items():
                y = ((truoc.get("o") or {}).get(slug) or {}).get(b)
                if y is None:
                    L.append(f"| `{slug}` | `{b}` | MỚI | MỚI | MỚI |")
                    continue
                L.append(f"| `{slug}` | `{b}` | {_x(y.get('diem_tb'))} → {_x(x.get('diem_tb'))} | "
                         f"{_x(y.get('noi_sai'))} → {_x(x.get('noi_sai'))} | {_x(y.get('usd'))} → {_x(x.get('usd'))} |")
        bo = [s for s in (truoc.get("o") or {}) if s not in kq["o"]]
        if bo:
            L.append(f"\nCó ở bản trước, VẮNG bản này: {', '.join(f'`{s}`' for s in bo)}.")
    return "\n".join(L) + "\n"


def main_ma_tran(a, goc_api: str | None = None) -> int:
    """`goc_api` (CHỈ bài thử, ⛔ CLI): lái chế độ THẬT tới máy chủ GIẢ để đo lối thoát + nhật ký mà ⛔ tiền."""
    from contextlib import ExitStack
    import openrouter_gia as og
    mt = mh.ma_tran_openrouter()
    ung_vien = [s.strip() for s in a.ung_vien.split(",")] if a.ung_vien else list(mt["ung_vien"])
    sai = {s: mh.loi_slug_openrouter(s) for s in ung_vien if mh.loi_slug_openrouter(s)}
    if sai:
        print("⛔ ĐỎ: ứng viên ⛔ hợp lệ —", sai)
        return 2
    be_ds, nhan_be = be_ma_tran(Path(os.environ[BIEN_BE]) if os.environ.get(BIEN_BE) else None)
    nk: list = []
    tran_mh = a.tran_usd_mo_hinh if a.tran_usd_mo_hinh is not None else a.tran_usd
    with ExitStack() as st:
        if a.that:
            moi, goc = None, (goc_api or mh.GOC_API_OPENROUTER)
            if mh.duong_goi() != mh.DUONG_OPENROUTER:
                print(f"⛔ ĐỎ (⛔ gọi): `--that` cần {mh.BIEN_NHA_CUNG_CAP}=openrouter (hiện `{mh.duong_goi()}`)")
                return 2
        else:   # GIẢ: adapter THẬT ↔ máy chủ GIẢ cục bộ; chốt thoả bằng môi trường RIÊNG (⛔ đụng os.environ, ⛔ khoá thật)
            goc, _tt = st.enter_context(og.may_chu_gia())
            moi = {mh.BIEN_CHO_GOI: "1", mh.BIEN_NHA_CUNG_CAP: mh.DUONG_OPENROUTER, mh.BIEN_OPENROUTER_KHOA: "gia-khong-phai-khoa",
                   mh.BIEN_OPENROUTER_DU_LIEU: "1"}

        def dung_ncc(slug: str, ds: list):
            return mh.OpenRouterChat(mh.mo_hinh_openrouter(slug), co_that=True, che_do=CHE_CHINH, tran_usd=a.tran_usd,
                                     tran_usd_mo_hinh=tran_mh, nhat_ky=ds, moi_truong=moi, goc_api=goc,
                                     thay_cho=[d for d in ch.AGENT if d.ma == "A2_PR_MAP"][0].mo_hinh.ma)
        loi_ngoai = None
        try:
            o = chay_ma_tran(ung_vien, be_ds, dung_ncc, nk)
        except BaseException as e:                  # `AG3-R1-01`: ngoại lệ CHƯA lường — tiền đã tiêu vẫn để lại nhật ký
            loi_ngoai = f"{type(e).__name__} (lượt dừng ngoài dự kiến)"
            raise
        finally:
            if a.that:
                loi_o = loi_ngoai or "; ".join(x for x in ket_ma_tran(locals().get("o") or {})[1] if "lỗi" in x or "loi" in x
                                               or "bo_qua" in x)[:400] or None
                pn = cav.ghi_nhat_ky({"_": _GiuNhatKy(nk)}, "fleet_ma_tran_openrouter", loi=loi_o)
                if pn:
                    print(f"  đã ghi nhật ký {_tuong_doi(pn)}")
    kq = {"ngay": date.today().isoformat(), "che_do": "that" if a.that else "gia", "be": nhan_be,
          "checksum_prompt": checksum_prompt("A2_PR_MAP"), "tran_usd": a.tran_usd, "tran_usd_mo_hinh": tran_mh,
          "o": o, "nhat_ky": mh.tong_nhat_ky(nk)}
    truoc = json.loads(TEP_MT_JSON.read_text(encoding="utf-8")) if TEP_MT_JSON.exists() else None
    trang = md_ma_tran(kq, truoc)
    print(trang)
    if a.ghi:
        TM_VONG.mkdir(parents=True, exist_ok=True)
        TEP_MT_MD.write_text(trang, encoding="utf-8")
        TEP_MT_JSON.write_text(json.dumps(kq, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"  đã ghi {_tuong_doi(TEP_MT_MD)} · {_tuong_doi(TEP_MT_JSON)}")
    return 0 if ket_ma_tran(o)[0] else 1


def _tuong_doi(p: Path) -> Path:
    return p.relative_to(GOC) if p.is_relative_to(GOC) else p


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fleet_eval_voi.py")
    p.add_argument("--ghi", action="store_true")
    p.add_argument("--be-giu-rieng", action="store_true", help="WO-338: bể A ↔ bể B (GIẢ/phát lại, ⛔ API thật)")
    p.add_argument("--ma-tran", action="store_true",
                   help="WO-367: ma trận ứng viên OpenRouter × bể A/B (vắng bể ⇒ 12 ca dựng, KHAI rõ). Mặc định GIẢ (máy chủ 127.0.0.1)")
    p.add_argument("--that", action="store_true", help="(--ma-tran) gọi OpenRouter THẬT — đủ chốt: FLS_NHA_CUNG_CAP=openrouter · "
                   "FLS_CHO_GOI_API=1 · OPENROUTER_API_KEY · FLS_OPENROUTER_DU_LIEU_XAC_NHAN=1")
    p.add_argument("--ung-vien", default="", help="(--ma-tran) slug cách nhau dấu phẩy — phải có trong fls/agent/openrouter_mo_hinh.json; "
                   "vắng ⇒ `ung_vien` của tệp ấy")
    p.add_argument("--tran-usd", type=float, default=cav.TRAN_USD_MAC_DINH, help="(--ma-tran) trần USD TỔNG cả lượt — chặn lời KẾ")
    p.add_argument("--tran-usd-mo-hinh", type=float, default=None, help="(--ma-tran) trần USD RIÊNG mỗi mô hình (vắng ⇒ = trần tổng)")
    a = p.parse_args(argv)
    if a.ma_tran:
        return main_ma_tran(a)
    if a.that:
        p.error("--that chỉ đi với --ma-tran")
    if a.be_giu_rieng:
        return main_be(a.ghi)
    ca, dap_an, nhan_be = cav.bo_ca()
    ds = [chay_vong(m, l, c, ca, dap_an) for m, l, c in VONG]
    loi = [v for v in ds if "loi" in v]
    if loi:
        print("⛔ vòng lỗi:", loi)
        return 1
    px = phan_xu(ds)
    print(f"Bể: {nhan_be} · {len(dap_an['noi'])} ca · checksum bể {_sha(cav.CA_DUNG)}")
    print(f"{'phiên bản':24s} {'nối':>4s} {'sai':>4s} {'tỉ lệ sai':>9s} {'recall':>7s} {'người bị nối':>12s} {'điểm TB':>8s}  phán")
    for v, x in zip(ds, px):
        t = v["tong_hop"]
        print(f"{v['phien_ban']:24s} {t['so_noi']:4d} {t['noi_sai']:4d} {str(t['ti_le_noi_sai']):>9s} "
              f"{str(t['recall_phai_noi']):>7s} {t['phai_nguoi_bi_noi']:12d} {str(t['diem_tb']):>8s}  {x['ket']}")
    if a.ghi:
        TM_VONG.mkdir(parents=True, exist_ok=True)
        hom = date.today().isoformat()
        for i, v in enumerate(ds, 1):
            (TM_VONG / f"{hom}_vong{i}_{v['phien_ban']}.json").write_text(
                json.dumps({"be": nhan_be, "checksum_be": _sha(cav.CA_DUNG), **v}, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8")
        md = [f"# Fleet eval nhiều vòng — A2.04 ghép theo nội dung · {hom}", "",
              f"Bể: **{nhan_be}** · `{len(dap_an['noi'])}` ca · checksum bể `{_sha(cav.CA_DUNG)}` · "
              "sinh bởi `python tools/fleet_eval_voi.py --ghi` (⛔ sửa tay).", "",
              "⚠ Mọi vòng dưới đây chạy mô hình **GIẢ** trên bể **DỰNG** — chạy thử bộ máy, ⛔ số đo mô hình thật.", "",
              "| vòng | phiên bản | nối | sai | tỉ lệ nối sai | recall phải-nối | ca phải-để-người bị nối | điểm TB (0–2) | phán |",
              "|---|---|---|---|---|---|---|---|---|"]
        for i, (v, x) in enumerate(zip(ds, px), 1):
            t = v["tong_hop"]
            md.append(f"| {i} | `{v['phien_ban']}` | {t['so_noi']} | {t['noi_sai']} | {t['ti_le_noi_sai']} | "
                      f"{t['recall_phai_noi']} | {t['phai_nguoi_bi_noi']} | {t['diem_tb']} | {x['ket']} |")
        md += ["", "Heatmap đơn vị × phiên bản (điểm TB 0–2):", "",
               "| đơn vị | " + " | ".join(f"`{v['phien_ban']}`" for v in ds) + " |",
               "|---|" + "---|" * len(ds)]
        for n in ("phai_noi", "phai_nguoi"):
            md.append(f"| {n} | " + " | ".join(str(v["theo_nhom"][n]["diem_tb"]) for v in ds) + " |")
        (TM_VONG / "TONG_HOP.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"  đã ghi {TM_VONG.relative_to(GOC)}/")
    return 0 if not any(x["chan"] for x in px) else 1


if __name__ == "__main__":
    raise SystemExit(main())
