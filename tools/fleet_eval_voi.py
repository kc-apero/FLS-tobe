# -*- coding: utf-8 -*-
"""Fleet eval NHIỀU VÒNG cho skill ghép theo NỘI DUNG (A2.04) — thẻ `a3-1-ref.eval.ghep-sai`.

    python tools/fleet_eval_voi.py                 # chạy các vòng khai ở VONG (giả), in bảng, ⛔ ghi
    python tools/fleet_eval_voi.py --ghi           # + ghi docs/ITL/05_FleetEval/vong/*.json + TONG_HOP.md

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
    ("v0-ma-tat-dinh", gnd.luat_v0, False),
    ("v1-gia-tat-noi-dung", gnd.luat_gia_v1, False),
    ("v1-gia-bat-noi-dung", gnd.luat_gia_v1, True),
)
#: Bar (thẻ a3-1-ref, đề xuất): 0 ca "phải để người" bị nối · tỉ lệ nối sai ≤ v0 (v0 0/0 ⇒ bar = 0).
BAR_PHAI_NGUOI_BI_NOI = 0


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def chay_vong(ma: str, luat, cho_noi_dung: bool, ca: dict, dap_an: dict, hat: int = 23) -> dict:
    s = [x for x in nap_bo("A2_PR_MAP") if x.loai == "bong"][0]
    dn = [a for a in ch.AGENT if a.ma == "A2_PR_MAP"][0]
    ks = ch.chay_skill(dn, he_thong(dn.ma), s, mh.GiaLap({"ung_vien_ghep": luat}),
                       {"ung_vien_ghep": lambda: cav.o_ca(ca)}, cho_noi_dung=cho_noi_dung)
    if ks.loi or ks.ra is None:
        return {"phien_ban": ma, "loi": ks.loi or "⛔ đầu ra"}
    # chấm MÙ: xáo mã ca (hạt cố định), bộ chấm chỉ thấy mã xáo
    ma_ca = sorted(dap_an["noi"])
    xao = ma_ca[:]
    random.Random(hat).shuffle(xao)
    doi = {c: f"x{i:03d}" for i, c in enumerate(xao)}
    chon_mu = {f"noi:{doi[c]}.{f}": ks.ra.get(f"noi:{c}.{f}") for c in ma_ca for f in ("chon", "ly_do")}
    dap_mu = {f"noi:{doi[c]}.{f}": v for c, b in dap_an["noi"].items() for f, v in b.items()}
    cham = gnd.cham(chon_mu, dap_mu)
    nguoc = {v: k for k, v in doi.items()}
    for x in cham:
        x["ca"] = nguoc[x["ca"]]
    th = gnd.tong_hop(cham)
    return {"phien_ban": ma, "mo_hinh": f"GIẢ ({luat.__name__}) thay {dn.mo_hinh.ma}",
            "checksum_prompt": checksum_prompt("A2_PR_MAP"), "cho_noi_dung": cho_noi_dung,
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


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="fleet_eval_voi.py")
    p.add_argument("--ghi", action="store_true")
    a = p.parse_args(argv)
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
