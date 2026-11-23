# -*- coding: utf-8 -*-
"""Fleet eval NHIỀU VÒNG cho skill ghép theo NỘI DUNG (A2.04) — thẻ `a3-1-ref.eval.ghep-sai`.

    python tools/fleet_eval_voi.py                 # chạy các vòng khai ở VONG (giả), in bảng, ⛔ ghi
    python tools/fleet_eval_voi.py --ghi           # + ghi docs/ITL/05_FleetEval/vong/*.json + TONG_HOP.md
    python tools/fleet_eval_voi.py --be-giu-rieng [--ghi]   # WO-338: bể A (dữ liệu CŨ) ↔ bể B (THẬT hiện tại), GIẢ/phát lại

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


def chay_vong(ma: str, luat, che_do: str, ca: dict, dap_an: dict, hat: int = 23) -> dict:
    """MỘT vòng QUA `chay_skill` (cổng skill + chốt + bộ che theo `che_do`). ⭐ `HELD-R1-06`: bản R0 có nhánh
    `khong_che` đọc thẳng `luat(cav.o_ca(ca))` ⇒ BỎ cổng skill — vòng ấy đo LUẬT, ⛔ đo đường ống. Chế độ
    chính theo chủ 23/11 ~06:00 ("agent đọc TOÀN BỘ nội dung + số TK") nay là `che_do="mo"` — đi ĐÚNG đường ống."""
    s = [x for x in nap_bo("A2_PR_MAP") if x.loai == "bong"][0]
    dn = [a for a in ch.AGENT if a.ma == "A2_PR_MAP"][0]
    ks = ch.chay_skill(dn, he_thong(dn.ma), s, mh.GiaLap({"ung_vien_ghep": luat}),
                       {"ung_vien_ghep": lambda: cav.o_ca(ca)}, che_do=che_do)
    if ks.loi and ks.loi.startswith("CamGui") and che_do != CHE_CHINH:
        # Lớp 2 của bộ che TỪ CHỐI gửi (số dài còn sót sau che) — chế độ che là TUỲ CHỌN, nên đây là KẾT QUẢ ĐO của che
        # (đo 23/11 trên bể thật: che_noi_dung để lọt dãy số DÍNH CHỮ ⇒ bị chặn), ⛔ lỗi hạ tầng làm dừng cả vòng.
        return {"phien_ban": ma, "che_do": che_do, "bi_cam_gui": ks.loi[:160]}
    if ks.loi or ks.ra is None:
        return {"phien_ban": ma, "loi": ks.loi or "⛔ đầu ra"}
    cham, th = _cham_mu(ks.ra, dap_an, hat)
    return {"phien_ban": ma, "mo_hinh": f"GIẢ ({luat.__name__}) thay {dn.mo_hinh.ma}",
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


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fleet_eval_voi.py")
    p.add_argument("--ghi", action="store_true")
    p.add_argument("--be-giu-rieng", action="store_true", help="WO-338: bể A ↔ bể B (GIẢ/phát lại, ⛔ API thật)")
    a = p.parse_args(argv)
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
