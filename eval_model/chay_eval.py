"""Chay bo ca gia lap qua nhieu model, cham, ghi ket qua + chi phi DO DUOC.

Nha cung cap:
  oracle             tra dung dap an  -> phai ra 100% (cong cham khong bo sot)
  ngay_tho           luat "nghe hop ly" nhung sai o cac bay da biet -> phai ra < 100% (cong cham biet do)
  claude:<model_id>  Anthropic managed tren Google Cloud (AnthropicGoogleCloud). Can:
                       ANTHROPIC_GOOGLE_CLOUD_PROJECT, ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID, ADC/GOOGLE_APPLICATION_CREDENTIALS
  gemini:<model_id>  google-genai tren Vertex AI. Can: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, ADC

Vi du:
  python chay_eval.py oracle ngay_tho
  python chay_eval.py claude:claude-opus-5-5 claude:claude-opus-5 gemini:gemini-3.8-flash gemini:gemini-3.1-pro --lap 3

⛔ Khong bat fallback model khi bi tu choi: ca bi tu choi tinh la TRUOT, de so sanh
   khong bi lan model khac vao. So ca bi tu choi in rieng.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import time
from collections import defaultdict
from pathlib import Path

from cham import CHAM
from uoc_chi_phi import GIA

GOC = Path(__file__).parent
DU_LIEU = GOC / "du_lieu"
KET_QUA = GOC / "ket_qua"
NA, IH = "Need to manual input", "Input here"

TEN_GIA = {"claude-opus-5-5": "Opus 5.5", "claude-opus-5": "Opus 5",
           "gemini-3.8-flash": "Gemini 3.8 Flash", "gemini-3.1-pro": "Gemini 3.1 Pro"}


def nap():
    sk = json.loads((DU_LIEU / "skill.json").read_text(encoding="utf-8"))
    ca = [json.loads(l) for l in (DU_LIEU / "cases.jsonl").read_text(encoding="utf-8").splitlines()]
    return sk, ca


def loi_nhac(c) -> str:
    return ("DỮ LIỆU (JSON):\n" + json.dumps(c["dau_vao"], ensure_ascii=False)
            + "\n\nChỉ trả về MỘT đối tượng JSON đúng schema, không giải thích.")


# ---------------------------------------------------------------- baseline ngay tho
def ngay_tho(c):
    b, x = c["bai"], c["dau_vao"]
    if b == "A1":     # bo qua _adjust, dem moi dong, so theo vi tri
        return {"thay_doi": [] if x["ban_khai"] == x["tieu_de_sheet"] else [{"loai": "doi_vi_tri", "cot": "*"}],
                "ref_hieu_luc": [d.get("Reference number", "") for d in x["dong"]], "so_dong": len(x["dong"])}
    if b == "A2":     # khong chuan hoa ma, dung sai 1.000 cho moi tien te
        g = defaultdict(lambda: {"b": [], "p": []})
        for d in x["bank"]:
            g[d["ref"].upper()]["b"].append(d)
        for d in x["pm"]:
            g[d["ref"].upper()]["p"].append(d)
        out = []
        for k, v in g.items():
            if k.startswith("#"):
                continue
            bb, pp = v["b"], v["p"]
            if not bb or not pp:
                h = "KHONG_GHEP"
            elif abs(sum(d["tien"] for d in bb) - sum(d["tien"] for d in pp)) > 1000:
                h = "F"
            else:
                h = "A" if len(bb) == len(pp) == 1 else "B" if len(bb) == 1 else "C" if len(pp) == 1 else "D"
            out.append({"ma": k, "hinh": h})
        return {"nhom": out}
    if b == "A3":     # MID = S khi T rong (doc cong thuc theo tung dong), svc khong co mac dinh, luon doan
        md = {"hd": "OGA | GAC - Other", "pay_type": "Thanh toán (Regular)", "cdt1": "SHQ2 | Headquarters2",
              "id_payee": "VD0", "invoice": "Nợ hoá đơn"}
        kh, dx = [], []
        for d in x["dong"]:
            for k, v in d["khoi"].items():
                s, t = v["S"], v["T"]
                u = s if (t == "" and s != NA) else (md.get(k, "") if t == IH else t)
                vv = u if s in (NA, "") else s
                kh.append({"dong": d["dong"], "khoi": k, "U": u, "V": vv})
            if d["khoi"]["hd"]["S"] == NA and d["khoi"]["hd"]["T"] == "":
                dx.append({"dong": d["dong"], "hd": x["lich_su_vendor_hd"].get(d["vendor"], "OGA | GAC - Other")})
        return {"khoi": kh, "de_xuat": dx}
    if b == "A4":     # chi soat so du
        loi = []
        for tk, dau in x["so_du_dau"].items():
            t = dau + sum(d["ps_no"] - d["ps_co"] for d in x["dong"] if d["tk"] == tk)
            if abs(t - x["so_du_cuoi_ccr"][tk]) > 1e-6:
                loi.append({"loai": "DIF", "khoa": tk})
        return {"loi": loi}
    raise ValueError(b)


# ---------------------------------------------------------------- model that
_CLIENTS: dict = {}


def goi_claude(model, he_thong, nguoi, schema):
    from anthropic import AnthropicGoogleCloud
    c = _CLIENTS.setdefault("claude", AnthropicGoogleCloud())
    t0 = time.time()
    with c.messages.stream(
        model=model, max_tokens=64000,
        system=[{"type": "text", "text": he_thong, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": nguoi}],
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": schema}},
    ) as s:
        m = s.get_final_message()
    if m.stop_reason == "refusal":
        return None, {"tu_choi": True}, time.time() - t0
    txt = next((b.text for b in m.content if b.type == "text"), "")
    u = m.usage
    use = {"vao": u.input_tokens, "doc_cache": u.cache_read_input_tokens or 0,
           "ghi_cache": u.cache_creation_input_tokens or 0, "ra": u.output_tokens}
    return txt, use, time.time() - t0


def goi_gemini(model, he_thong, nguoi, schema):
    # ⚠ Chua chay thu tren tai khoan that: ten truong cau hinh lay theo google-genai hien hanh;
    #   lan chay dau neu SDK bao loi ten truong thi sua o day, ⛔ khong doi cach cham.
    from google import genai
    from google.genai import types
    c = _CLIENTS.setdefault("gemini", genai.Client(vertexai=True))
    t0 = time.time()
    r = c.models.generate_content(
        model=model, contents=nguoi,
        config=types.GenerateContentConfig(
            system_instruction=he_thong, response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(thinking_level="medium")))
    um = r.usage_metadata
    use = {"vao": (um.prompt_token_count or 0) - (um.cached_content_token_count or 0),
           "doc_cache": um.cached_content_token_count or 0, "ghi_cache": 0,
           "ra": (um.candidates_token_count or 0) + (um.thoughts_token_count or 0)}
    return r.text, use, time.time() - t0


def tien_usd(model, use):
    g = GIA.get(TEN_GIA.get(model, ""), None)
    if not g or not use or use.get("tu_choi"):
        return 0.0
    ghi = g["cache_write"] if g["cache_write"] is not None else g["inp"]
    return (use["vao"] * g["inp"] + use["doc_cache"] * g["cache_read"] + use["ghi_cache"] * ghi
            + use["ra"] * g["out"]) / 1e6


def _json(txt):
    if txt is None:
        return None
    m = re.search(r"\{.*\}", txt, re.S)
    try:
        return json.loads(m.group(0) if m else txt)
    except Exception:
        return None


def chay_mot(ncc, c, sk):
    if ncc == "oracle":
        return c["dap_an"], {}, 0.0
    if ncc == "ngay_tho":
        return ngay_tho(c), {}, 0.0
    loai, model = ncc.split(":", 1)
    f = goi_claude if loai == "claude" else goi_gemini
    txt, use, dt = f(model, sk["skill"][c["bai"]], loi_nhac(c), sk["schema"][c["bai"]])
    return _json(txt), use, dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ncc", nargs="+")
    ap.add_argument("--lap", type=int, default=1, help="so lan lap moi ca (do dao dong)")
    ap.add_argument("--song_song", type=int, default=4)
    ap.add_argument("--bai", default="A1,A2,A3,A4")
    a = ap.parse_args()
    sk, ca = nap()
    ca = [c for c in ca if c["bai"] in a.bai.split(",")]
    KET_QUA.mkdir(exist_ok=True)
    tong = {}
    for ncc in a.ncc:
        dong = []
        viec = [(c, k) for c in ca for k in range(a.lap)]
        with cf.ThreadPoolExecutor(a.song_song) as ex:
            fut = {ex.submit(chay_mot, ncc, c, sk): (c, k) for c, k in viec}
            for f in cf.as_completed(fut):
                c, k = fut[f]
                try:
                    ra, use, dt = f.result()
                    loi = None
                except Exception as e:      # noqa: BLE001 — loi goi API tinh la truot, co ghi ly do
                    ra, use, dt, loi = None, {}, 0.0, f"{type(e).__name__}: {e}"[:300]
                if ra is None:
                    diem, ct = 0.0, {"khong_doc_duoc_json_hoac_loi": loi or ("tu_choi" if use.get("tu_choi") else "json hong")}
                else:
                    diem, ct = CHAM[c["bai"]](c["dap_an"], ra)
                model = ncc.split(":", 1)[-1]
                dong.append({"ncc": ncc, "ca": c["id"], "bai": c["bai"], "lan": k, "diem": round(diem, 4),
                             "chi_tiet": ct, "usage": use, "usd": round(tien_usd(model, use), 5), "giay": round(dt, 1)})
        ten = ncc.replace(":", "_").replace("/", "_")
        (KET_QUA / f"{ten}.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in dong), encoding="utf-8")
        theo_bai = defaultdict(list)
        for x in dong:
            theo_bai[x["bai"]].append(x["diem"])
        tong[ncc] = {b: sum(v) / len(v) for b, v in sorted(theo_bai.items())}
        tong[ncc]["TB"] = sum(tong[ncc].values()) / len(theo_bai)
        tong[ncc]["usd"] = sum(x["usd"] for x in dong)
        tong[ncc]["truot_100"] = sum(1 for x in dong if x["diem"] < 1)
    print(f"{'nha cung cap':34s} " + " ".join(f"{b:>6}" for b in a.bai.split(",")) + f" {'TB':>6} {'ca<100%':>8} {'USD':>8}")
    for n, t in tong.items():
        print(f"{n:34s} " + " ".join(f"{t.get(b, 0):6.1%}" for b in a.bai.split(","))
              + f" {t['TB']:6.1%} {t['truot_100']:8d} {t['usd']:8.3f}")
    (KET_QUA / "tong.json").write_text(json.dumps(tong, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
