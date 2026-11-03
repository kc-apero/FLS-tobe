"""Sinh DEMO ĐỘNG `F01`+`F02` từ **kho thật**, kèm ĐỐI SOÁT với file kế toán.

  python tools/demo_dong.py            # sinh demo + doi soat voi so song
  python tools/demo_dong.py --khong-mang   # chi doc kho, ⛔ khong doc Sheets

⛔ Chi DOC. ⛔ Khong ghi mot o nao vao file ke toan (`QĐ-ITL-34`), ⛔ khong ghi
   mot dong nao vao kho.

★★ **Ba viec trong mot lan chay:**
  ⓐ **lay du lieu THAT** tu kho — hang cho, mot trang so, ung vien ghep, danh
    muc phan bo *(⛔ khong bia mot dong nao)*
  ⓑ **doi soat** so lieu ay voi **so ke toan SONG** *(ban sao RAW —
    `QĐ-ITL-50`)*, roi **nhung ket qua doi soat vao chinh tep demo**
  ⓒ sinh mot trang `.html` **bam duoc**: go 7 o · ghep · bo ghep · xong · mo
    lai — moi thao tac in ra **MAY SE GHI GI VAO DAU**

⛔⛔ **Tep sinh ra nam o `hien_vat/` va do la CO Y:** no cho `memo` (Dien giai)
   cua **dong so that**, va cot do **co the mang ten nguoi**. `hien_vat/` da
   nam trong `.gitignore` — cung lop nguy voi `sao_luu/`. ⇒ ⛔ khong bao gio
   vao git, va khi gui cho ai thi phai biet minh dang gui **du lieu ke toan
   that**.

⚠ **Vi sao doi soat theo TIEN TE chu ⛔ khong theo KY.** Cot ngay chung tu cua
  so goc bi **hoan ngay↔thang o 93% dong** *(da do — `itl-date-daymonth-swap`)*
  ⇒ moi phep chia theo ky deu dung mot cai truc **da biet la sai**. Tong theo
  tien te ⛔ khong phu thuoc ngay, nen no do duoc that.
"""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from decimal import Decimal
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

import psycopg                                                    # noqa: E402

from fls.adapters.pm_join import dung_sai_ghep_tay, TY_LE_GHEP_TAY  # noqa: E402
from fls.canon.spec import pos_of                                 # noqa: E402
from fls.db.kho import dsn_that                                   # noqa: E402
from fls.ledger.allocate import suy_allocate                      # noqa: E402
from fls.oracle.nguon import BAN_SAO_RAW                          # noqa: E402
from fls.repo import doc_bao_cao as bc                            # noqa: E402
from fls.repo.ghi_tay import TRUONG_GHI, TRUONG_HOP_DONG          # noqa: E402
from fls.repo.nap_mapping import TRUONG as MM_TRUONG              # noqa: E402
from fls.repo.pham_vi import chi_nap_that                         # noqa: E402

SA = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
RA = GOC / "hien_vat" / "FLS-Demo-Dong.html"

# ⭐⭐ MOT ban su that ve mau (`B2`, 2026-09-03).
#
# ⛔⛔ Truoc do khoi `:root{…}` duoc **chep tay** vao day, thanh **ban sao thu
# ba** *(A-CCR handoff · `FLS-Design-P6.html` · tep nay)*. Ba ban sao thi cau
# *"mau nhan la mau gi"* co ba cau tra loi dung — va chung se lech, **trong im
# lang**, dung cai benh bo tai lieu nay chua o tang so lieu.
# ⇒ Doc thang tu `fls/web/tep/tokens.css`. Sua mau o **mot** cho.
#
# ⚠ Bai `tests/web/test_mot_ban_mau_duy_nhat.py` NO neu tep nay co lai mot
#   khoi `:root{` cua rieng no.
TOKENS = GOC / "fls" / "web" / "tep" / "tokens.css"


def _tokens() -> str:
    """Khoi `:root{…}` doc tu `tokens.css`. ⛔ NO neu ⛔ khong doc duoc."""
    chu = TOKENS.read_text(encoding="utf-8")
    i = chu.index(":root{")
    j = chu.index("\n}", i) + 2
    # ⚠ ⛔ KHONG nhan doi `{`/`}` o day. Khoi nay di vao f-string qua mot phep
    # **chen gia tri** (`{_tokens()}`), va Python ⛔ khong quet lai dau ngoac
    # ben trong gia tri da chen. Nhan doi se ra `{{` **that** tren man.
    return chu[i:j]


SO_HANG_CHO = 14
SO_DONG_SO = 12


# ─────────────────────────────────────────────────────── ⓐ doc KHO
def doc_kho(conn) -> dict:
    pv = chi_nap_that()
    d: dict = {}

    # hang cho VND — dung CHINH cua doc, ⛔ khong viet lai cau SQL
    tr = bc.doc_hang_cho(conn, pv, curr="VND", limit=SO_HANG_CHO)
    d["hang_cho"] = tr.dong
    d["tom"] = bc.dem_hang_cho(conn, pv)

    # mot trang so + moi noi hieu luc + vung phan bo suy that
    with conn.cursor() as cur:
        cur.execute(
            "SELECT i.itl_id, i.doc_date, i.doc_no, i.curr,"
            " COALESCE(i.ps_no,0)+COALESCE(i.ps_co,0) AS tien, i.memo,"
            " i.hd, i.pay_type, i.cdt1, i.svc_start, i.svc_end,"
            " i.id_payee, i.invoice, i.work_status,"
            " (SELECT count(*) FROM fls_moi_noi m WHERE m.itl_id=i.itl_id) AS moi_noi"
            " FROM fls_itl i"
            " WHERE i.curr='VND' ORDER BY COALESCE(i.ps_no,0)+COALESCE(i.ps_co,0)"
            " DESC LIMIT %s", (SO_DONG_SO,))
        ten = [x.name for x in cur.description]
        d["so"] = [dict(zip(ten, r)) for r in cur.fetchall()]

        cur.execute(f"SELECT {', '.join(MM_TRUONG)} FROM fls_mapping_master")
        mm = {str(r[0]).strip().lower(): dict(zip(MM_TRUONG, r))
              for r in cur.fetchall()}
    d["mm_so_ma"] = len(mm)

    # vung PHAN BO: suy that cho tung dong cua trang so
    for x in d["so"]:
        v = suy_allocate(x["cdt1"], x["hd"],
                         mm.get(str(x["hd"] or "").strip().lower()))
        x["alloc"] = {"cfa1": v.cfa1, "cfa2": v.cfa2, "method": v.method,
                      "khong_tra_duoc": v.khong_tra_duoc}

    # ung vien ghep cho dong hang cho DAU TIEN chua co moi noi
    d["ghep"] = None
    for x in d["hang_cho"]:
        u = bc.ung_vien_pm(conn, pv, x["itl_id"], n=8)
        if u and u.get("ung_vien"):
            d["ghep"] = {"dong": x, "ung_vien": u["ung_vien"],
                         "tien_bank": str(u.get("tien_bank") or x["tien"]),
                         "dung_sai": str(u.get("dung_sai") or "")}
            break

    # mot dong DA GHEP (de demo BO GHEP)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT i.itl_id, i.doc_no, i.memo,"
            " COALESCE(i.ps_no,0)+COALESCE(i.ps_co,0) AS tien,"
            " json_agg(json_build_object('pm_line_id', m.pm_line_id,"
            "   'amount', m.amount::text, 'lan', m.lan) ORDER BY m.pm_line_id)"
            "  AS moi_noi"
            " FROM fls_itl i JOIN fls_moi_noi m USING (itl_id)"
            " WHERE i.curr='VND' GROUP BY i.itl_id, i.doc_no, i.memo, i.ps_no,"
            " i.ps_co ORDER BY 4 DESC LIMIT 1")
        r = cur.fetchone()
    d["da_ghep"] = None if r is None else {
        "itl_id": r[0], "doc_no": r[1], "memo": r[2], "tien": r[3],
        "moi_noi": r[4]}

    # ── truc doi soat: tong theo TIEN TE + KHOA NOI DUNG tung dong
    with conn.cursor() as cur:
        cur.execute(
            "SELECT curr, count(*)::int, COALESCE(SUM(ps_no),0),"
            " COALESCE(SUM(ps_co),0) FROM fls_itl GROUP BY curr ORDER BY 2 DESC")
        d["tong_kho"] = [{"curr": (x[0] or "").strip(), "dong": x[1],
                          "no": str(x[2]), "co": str(x[3])}
                         for x in cur.fetchall()]
        d["dong_kho"] = sum(x["dong"] for x in d["tong_kho"])

        # ⭐⭐ KHOA NOI DUNG, ⛔ khong phai VI TRI. Xem `doi_soat` de biet vi sao.
        cur.execute("SELECT doc_no, curr, COALESCE(ps_no,0), COALESCE(ps_co,0)"
                    " FROM fls_itl")
        d["khoa_kho"] = [_khoa(r[0], r[1], r[2], r[3]) for r in cur.fetchall()]

        cur.execute("SELECT reason, count(*)::int FROM fls_reject"
                    " GROUP BY 1 ORDER BY 2 DESC")
        d["loai"] = [{"ly_do": r[0], "so": r[1]} for r in cur.fetchall()]
        d["so_loai"] = sum(x["so"] for x in d["loai"])
        cur.execute("SELECT max(source_row) FROM fls_itl")
        d["dong_cuoi_da_nap"] = cur.fetchone()[0]
    return d


# ─────────────────────────────────────────── ⓑ doc SO SONG + doi soat
def _token() -> str:
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA, "--scopes",
         "https://www.googleapis.com/auth/spreadsheets.readonly"],
        capture_output=True, text=True, shell=True)
    t = r.stdout.strip()
    if not t:
        raise RuntimeError("khong lay duoc token: " + r.stderr.strip()[:200])
    return t


def _cot(tok: str, ch: str, het: int) -> list:
    u = (f"https://sheets.googleapis.com/v4/spreadsheets/"
         f"{BAN_SAO_RAW.spreadsheet_id}/values/"
         + urllib.parse.quote(f"{BAN_SAO_RAW.sheet}!{ch}1:{ch}{het}")
         + "?valueRenderOption=UNFORMATTED_VALUE&majorDimension=COLUMNS")
    q = urllib.request.Request(u, headers={"Authorization": f"Bearer {tok}"})
    v = json.load(urllib.request.urlopen(q, timeout=600)).get("values", [[]])
    return v[0] if v else []


def _khoa(ct, curr, no, co) -> tuple:
    """Khoa NOI DUNG cua mot dong: so chung tu + tien te + hai ve tien.

    ⚠ Lam tron 2 chu so: Google Sheets tra ve **so thuc dau phay dong**, nen
    cung mot gia tri co the ra `142591.08000000002`. Khong lam tron thi phep
    so se bao LECH o muc `1e-11` — mot cai do gia.
    """
    return (str(ct or "").strip(),
            str(curr or "").strip().upper(),
            _so(no).quantize(Decimal("0.01")),
            _so(co).quantize(Decimal("0.01")))


def _so(v) -> Decimal:
    if v is None or v == "":
        return Decimal(0)
    try:
        return Decimal(str(v))
    except Exception:                                          # noqa: BLE001
        return Decimal(0)


def doc_song(het: int = 10500) -> dict:
    """Tong theo tien te doc TRUC TIEP tu so ke toan song (ban sao RAW)."""
    tok = _token()
    ch = {"ct": "B", "curr": "D", "no": "E", "co": "F"}
    tho = {k: _cot(tok, c, het) for k, c in ch.items()}
    i0 = BAN_SAO_RAW.dong_dau - 1
    n = max(len(v) for v in tho.values())
    def o(k: int, key: str):
        v = tho[key]
        return v[k] if k < len(v) else ""

    gom: dict[str, dict] = {}
    khoa: list[tuple] = []
    for k in range(i0, n):
        c = str(o(k, "curr")).strip().upper()
        no, co = _so(o(k, "no")), _so(o(k, "co"))
        if not c and no == 0 and co == 0:
            continue                                   # dong trong
        # ⚠ Khoa la tien te THO ("" khi rong), ⛔ khong phai nhan de hien:
        #   kho dung "" nen neu o day dung "(rong)" thi hai ben ⛔ khong ghep
        #   duoc, va cot "chi o SO" cua dong ay se ra 0 — mot cai do GIA.
        g = gom.setdefault(c, {"dong": 0, "no": Decimal(0), "co": Decimal(0)})
        g["dong"] += 1
        g["no"] += no
        g["co"] += co
        khoa.append(_khoa(o(k, "ct"), c, no, co))
    return {"tong": [{"curr": k, "dong": v["dong"], "no": str(v["no"]),
                      "co": str(v["co"])}
                     for k, v in sorted(gom.items(),
                                        key=lambda x: -x[1]["dong"])],
            "dong": sum(v["dong"] for v in gom.values()),
            "khoa": khoa, "cot": ch, "dong_dau": BAN_SAO_RAW.dong_dau}


def doi_soat(kho: dict, song: dict | None) -> dict:
    """Doi soat kho ↔ so song **THEO NOI DUNG**, ⛔ khong theo VI TRI.

    ⛔⛔ **Vi sao ⛔ KHONG so theo vi tri — va day la mot phep do, ⛔ khong phai
    mot y kien.** Luot dau toi so `source_row` cua kho voi dong cung so tren
    sheet, va ra **6 dong "lech"**. Do lai theo NOI DUNG thi **ca 6 dong deu
    con nguyen tren so song**, chi **o dong khac**: 3 dong truot **+1**, 3 dong
    truot **+37**. ⇒ Ke toan da **CHEN 37 dong** vao vung duoi sau khi chup ban
    sao, va moi dong duoi cho chen **truot theo**.

    ★ Ket luan dat gia: **`source_row` la mot VI TRI, ⛔ khong phai mot DANH
      TINH.** Day dung la ly do `fls_itl` lay danh tinh tu `content_key`
      (`INV-I04a`), va o day ta co **bang chung do duoc** cho quyet dinh do.

    ⇒ Phep so o day dung **da tap** khoa noi dung: moi dong so song tim mot
      dong kho co cung `(so CT, tien te, PS No, PS Co)`. Con lai chia hai:
        · **chi o SO SONG** = dong bi LOAI (co ly do co ten) + dong THEM SAU
        · **chi o KHO** = ⛔ dong bi MAT — con so nay PHAI la 0
    """
    if song is None:
        return {"do_duoc": False}

    from collections import Counter
    ck, cs = Counter(kho["khoa_kho"]), Counter(song["khoa"])
    khop = ck & cs                       # giao cua hai da tap
    chi_kho, chi_song = ck - cs, cs - ck

    a = {x["curr"]: x for x in kho["tong_kho"]}
    b = {x["curr"]: x for x in song["tong"]}
    theo_te = []
    for c in sorted(set(a) | set(b)):
        x, y = a.get(c), b.get(c)
        n_khop = sum(v for k, v in khop.items() if k[1] == c)
        theo_te.append({
            "curr": c or "(rỗng — ⛔ dòng CÓ tiền mà KHÔNG có đơn vị tiền)",
            "kho_dong": x["dong"] if x else 0,
            "song_dong": y["dong"] if y else 0,
            "khop": n_khop,
            "chi_kho": sum(v for k, v in chi_kho.items() if k[1] == c),
            "chi_song": sum(v for k, v in chi_song.items() if k[1] == c),
        })
    return {
        "do_duoc": True,
        "khop": sum(khop.values()),
        "chi_kho": sum(chi_kho.values()),
        "chi_song": sum(chi_song.values()),
        "theo_te": theo_te,
        # phep cong PHAI dong: da nap + bi loai + them sau = so song
        "cong": {"da_nap": kho["dong_kho"], "bi_loai": kho["so_loai"],
                 "them_sau": song["dong"] - kho["dong_kho"] - kho["so_loai"],
                 "so_song": song["dong"]},
    }


# ─────────────────────────────────────────────────────── ⓒ sinh HTML
def _tien(v) -> str:
    d = Decimal(str(v or 0))
    return f"{d:,.0f}".replace(",", ".")


def _e(v) -> str:
    return html.escape("" if v is None else str(v))


def sinh(kho: dict, song: dict | None, ds: dict, gio: str) -> str:
    du = {
        "hang_cho": [{"itl_id": x["itl_id"],
                      "ngay": str(x["doc_date"] or "")[:10],
                      "so_ct": x.get("doc_no") or "",
                      "memo": x.get("memo") or "",
                      "tien": str(x["tien"]), "curr": x["curr"],
                      "hang": x["hang"], "pct": str(x["luy_ke_pct"] or 0),
                      "ly_do": x.get("reason") or ""}
                     for x in kho["hang_cho"]],
        "so": [{"itl_id": x["itl_id"], "ngay": str(x["doc_date"] or "")[:10],
                "so_ct": x["doc_no"] or "", "memo": x["memo"] or "",
                "tien": str(x["tien"]), "curr": x["curr"],
                "moi_noi": x["moi_noi"],
                **{f: (x[f] or "") for f in TRUONG_GHI},
                "alloc": x["alloc"]} for x in kho["so"]],
        "ghep": None if kho["ghep"] is None else {
            "itl_id": kho["ghep"]["dong"]["itl_id"],
            "memo": kho["ghep"]["dong"].get("memo") or "",
            "tien_bank": kho["ghep"]["tien_bank"],
            "dung_sai": kho["ghep"]["dung_sai"],
            "ung_vien": [{"pm_line_id": u["pm_line_id"],
                          "amount": str(u.get("amount") or 0),
                          "bac": u.get("bac") or "", "status": u.get("status") or "",
                          "da_ghep": u.get("da_ghep") or 0,
                          "hd": u.get("hd") or "", "cdt1": u.get("cdt1") or ""}
                         for u in kho["ghep"]["ung_vien"]]},
        "da_ghep": None if kho["da_ghep"] is None else {
            "itl_id": kho["da_ghep"]["itl_id"],
            "memo": kho["da_ghep"]["memo"] or "",
            "tien": str(kho["da_ghep"]["tien"]),
            "moi_noi": kho["da_ghep"]["moi_noi"]},
        "truong_ghi": sorted(TRUONG_GHI),
        "truong_hop_dong": list(TRUONG_HOP_DONG),
        "ty_le": str(TY_LE_GHEP_TAY),
        "dung_sai_vnd": str(dung_sai_ghep_tay({"VND"}, Decimal("1000000000"))),
    }

    hc_tom = "".join(
        f"<span><b>{_e(t['curr'])}</b> · <span class='num'>{t['so_dong']:,}"
        f"</span> dòng · Σ <span class='num'>{_tien(t['tien'])}</span></span>"
        .replace(",", ".")
        for t in kho["tom"])

    do_duoc = bool(ds.get("do_duoc"))
    ds_rows = "".join(
        f"<tr><td>{_e(r['curr'])}</td>"
        f"<td class='r'>{r['kho_dong']:,}</td>"
        f"<td class='r'>{r['song_dong']:,}</td>"
        f"<td class='r'>{r['khop']:,}</td>"
        f"<td class='r'>{r['chi_kho']:,}</td>"
        f"<td class='r'>{r['chi_song']:,}</td>"
        f"<td>{'<span class=chip-ok>⛔ không mất dòng nào</span>' if r['chi_kho'] == 0 else '<span class=chip-no>⛔ MẤT DÒNG</span>'}</td>"
        "</tr>".replace(",", ".")
        for r in ds.get("theo_te", []))

    c = ds.get("cong", {})
    khop_het = do_duoc and ds.get("chi_kho", 1) == 0
    if not do_duoc:
        ds_ket = ("⛔ <b>KHÔNG ĐO ĐƯỢC</b> — lượt này chạy với "
                  "<code>--khong-mang</code>, hay đọc sổ sống thất bại. "
                  "⛔ Không đo được thì ⛔ không phải “khớp”.")
    elif khop_het:
        ds_ket = (
            f"✅ <b>⛔ KHÔNG MỘT DÒNG NÀO CỦA KHO BỊ MẤT hay BỊ SỬA</b> — cả "
            f"<b class='num'>{ds['khop']:,}</b> dòng đều tìm thấy trên sổ sống "
            f"với <b>đúng số chứng từ, đúng tiền tệ, đúng cả hai vế tiền</b>."
            .replace(",", ".") +
            f"<div style='margin-top:7px'>Và phép cộng <b>đóng khít</b>: "
            f"<b class='num'>{c.get('da_nap', 0):,}</b> đã nạp + "
            f"<b class='num'>{c.get('bi_loai', 0)}</b> bị loại "
            f"<i>(lý do có tên)</i> + "
            f"<b class='num'>{c.get('them_sau', 0)}</b> thêm sau khi chụp = "
            f"<b class='num'>{c.get('so_song', 0):,}</b> dòng sổ sống.</div>"
            .replace(",", "."))
    else:
        ds_ket = (f"⛔ <b>{ds.get('chi_kho')} dòng của kho ⛔ KHÔNG tìm thấy "
                  f"trên sổ sống</b> — đây ⛔ không phải lỗi hiển thị: một dòng "
                  f"đã vào sổ FLS mà nay ⛔ không còn ở nguồn.")

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FLS · Demo động F01 + F02 — dữ liệu THẬT</title>
<style>
{_tokens()}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--page);color:var(--ink);font:400 13.5px/1.5 var(--sans)}}
.wrap{{max-width:1500px;margin:0 auto;padding:0 18px 60px}}
h1,h2,h3{{margin:0;letter-spacing:-.01em}}
.num{{font-family:var(--mono);font-variant-numeric:tabular-nums}}
.mono{{font-family:var(--mono)}}
.muted{{color:var(--muted)}} .faint{{color:var(--faint)}}
.top{{background:var(--ink);color:#fff;padding:10px 18px;display:flex;gap:14px;
     align-items:center;flex-wrap:wrap}}
.top b{{font-size:15px}}
.warnbar{{background:var(--crit-bg);border-bottom:1px solid #f3cdcd;color:#7d2020;
  padding:9px 18px;font-size:12.5px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:8px;margin:14px 0}}
.card>header{{padding:11px 14px;border-bottom:1px solid var(--line);display:flex;
  gap:10px;align-items:center}}
.card>header h3{{font:600 13.5px/1 var(--sans)}}
.pad{{padding:13px 14px}}
.spacer{{flex:1}}
table{{border-collapse:separate;border-spacing:0;width:100%;font-size:12.5px}}
th,td{{text-align:left;padding:0 9px;height:var(--row);border-bottom:1px solid var(--line);
  white-space:nowrap}}
th{{background:var(--alt);font:600 11.5px/1 var(--sans);color:var(--muted);
  position:sticky;top:0;z-index:2}}
td.r,th.r{{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums}}
.scroll{{overflow:auto;max-height:430px}}
button.b{{font:600 12.5px/1 var(--sans);border-radius:6px;padding:6px 10px;
  cursor:pointer;border:1px solid var(--line);background:var(--surface);color:var(--ink)}}
button.b:hover{{border-color:var(--accent);color:var(--accent)}}
button.b.pri{{background:var(--accent);border-color:var(--accent);color:#fff}}
button.b.pri:hover{{background:var(--accent-hi)}}
button.b[disabled]{{opacity:.42;cursor:not-allowed;border-color:var(--line);color:var(--faint)}}
button.b[disabled]:hover{{border-color:var(--line);color:var(--faint)}}
.tiny{{font:600 11px/1 var(--sans);padding:4px 7px}}
.chip{{display:inline-flex;align-items:center;border-radius:999px;padding:2px 8px;
  font:600 11px/1.5 var(--sans);border:1px solid transparent;white-space:nowrap}}
.chip-ok,.chip.ok{{background:var(--good-bg);color:var(--good);border:1px solid var(--good-line);
  border-radius:999px;padding:2px 8px;font:600 11px/1.5 var(--sans)}}
.chip-no,.chip.no{{background:var(--crit-bg);color:var(--crit);border:1px solid #f3cdcd;
  border-radius:999px;padding:2px 8px;font:600 11px/1.5 var(--sans)}}
.chip.info{{background:var(--info-bg);color:var(--info);border-color:var(--info-line)}}
.chip.warn{{background:var(--warn-bg);color:var(--warn);border-color:#f0dcbe}}
.chip.lock{{background:var(--alt);color:var(--faint);border-color:var(--line)}}
.note{{background:var(--alt);border:1px solid var(--line);border-radius:6px;
  padding:9px 12px;font-size:12.5px;margin:9px 0}}
.note.warn{{background:var(--warn-bg);border-color:#f0dcbe}}
.note.crit{{background:var(--crit-bg);border-color:#f3cdcd}}
.note.ok{{background:var(--good-bg);border-color:var(--good-line)}}
input.cell{{width:100%;border:1px solid var(--info-line);border-radius:4px;
  padding:3px 6px;font:inherit;font-family:var(--mono);font-size:12px}}
input.cell:focus{{outline:0;border-color:var(--accent);box-shadow:0 0 0 2px #0e757022}}
input.cell.dirty{{border-color:var(--warn);background:var(--warn-bg)}}
input.cell.saved{{border-color:var(--good-line);background:var(--good-bg)}}
td.unmapped input.cell{{background:var(--warn-bg);color:var(--warn);font-style:italic}}
td.ro{{color:var(--muted);background:var(--alt)}}
.tabs{{display:flex;gap:6px;flex-wrap:wrap;padding:14px 0 0}}
.tabs button{{border:1px solid var(--line);background:var(--surface);border-radius:7px;
  padding:8px 13px;font:600 12.5px/1 var(--sans);color:var(--muted);cursor:pointer}}
.tabs button[aria-pressed=true]{{background:var(--ink);color:#fff;border-color:var(--ink)}}
section.sc{{display:none}} section.sc.on{{display:block}}
/* ── bảng OUTPUT: máy sẽ ghi gì ─────────────────────────────────────── */
#out{{font-family:var(--mono);font-size:11.5px;background:#0f1a19;color:#cfe3e0;
  border-radius:8px;padding:12px 14px;max-height:340px;overflow:auto;
  white-space:pre-wrap;line-height:1.55}}
#out .t{{color:#7fd3cc}} #out .w{{color:#f0c27a}} #out .n{{color:#9aa8a5}}
#out .g{{color:#8fd6a8}} #out .r{{color:#f2a0a0}}
.dlg{{position:fixed;inset:0;background:rgba(20,32,30,.45);display:none;
  align-items:center;justify-content:center;z-index:50;padding:18px}}
.dlg.on{{display:flex}}
.dlg>div{{background:var(--surface);border-radius:9px;max-width:560px;width:100%;
  box-shadow:0 16px 44px rgba(20,32,30,.3)}}
.dlg header{{padding:13px 16px;border-bottom:1px solid var(--line);font:700 14px/1 var(--sans)}}
.dlg .bd{{padding:14px 16px;font-size:13px;max-height:60vh;overflow:auto}}
.dlg .ft{{padding:12px 16px;border-top:1px solid var(--line);display:flex;gap:9px;
  justify-content:flex-end}}
.kv{{display:grid;grid-template-columns:180px 1fr;gap:0}}
.kv>div{{padding:6px 10px;border-top:1px solid var(--line);font-size:12.5px}}
.kv>div:nth-child(odd){{color:var(--muted);background:#fcfdfd}}
</style>
</head>
<body>
<div class="top">
  <b>FLS · Demo động</b>
  <span class="mono" style="font-size:11.5px;color:#9aa8a5">F01 Hàng chờ · F02 Sổ ITL</span>
  <span class="chip lock" style="background:#24322f;color:#cfe3e0;border-color:#3a4a47">dữ liệu THẬT · kho <span class="mono">fls</span></span>
  <span class="spacer"></span>
  <span class="mono" style="font-size:11.5px;color:#9aa8a5">sinh {gio}</span>
</div>
<div class="warnbar">
  ⛔⛔ <b>Tệp này chở DỮ LIỆU KẾ TOÁN THẬT</b>, gồm cột <b>Diễn giải</b> của dòng sổ thật
  — cột đó <b>có thể mang tên người</b>. Nó nằm trong <code>hien_vat/</code> đã bị
  <code>.gitignore</code> loại khỏi git. ⛔ <b>Đừng gửi qua Zalo/email.</b>
  Muốn cho ai xem thì đưa vào một thư mục Drive người đó đã có quyền, rồi xoá sau.
</div>

<div class="wrap">
<div class="tabs">
  <button data-s="ds" aria-pressed="true">① Đối soát với sổ kế toán</button>
  <button data-s="f01">② Hàng chờ — bấm được</button>
  <button data-s="f02">③ Sổ ITL — gõ được</button>
  <button data-s="mt">④ Mô tả OUTPUT</button>
</div>

<!-- ══════════════════ ① ĐỐI SOÁT ══════════════════ -->
<section class="sc on" id="ds">
  <div class="card">
    <header><h3>Kho FLS ↔ sổ kế toán SỐNG</h3>
      <span class="spacer"></span>
      <span class="muted" style="font-size:12px">bản sao RAW · tab <span class="mono">{_e(BAN_SAO_RAW.sheet)}</span> · từ dòng {BAN_SAO_RAW.dong_dau}</span>
    </header>
    <div class="pad">
      <div class="note {'ok' if khop_het else ('crit' if ds else 'warn')}">{ds_ket}</div>
      <div class="note">
        ⚠ <b>Vì sao đối theo NỘI DUNG chứ ⛔ không theo VỊ TRÍ — và đây là một
        PHÉP ĐO, ⛔ không phải một ý kiến.</b> Lượt đầu tôi so dòng thứ <i>n</i>
        của kho với dòng thứ <i>n</i> của sheet, và ra <b>6 dòng “lệch”</b>. Đo lại
        theo nội dung thì <b>cả 6 dòng đều còn nguyên</b> trên sổ sống, chỉ
        <b>ở dòng khác</b>: 3 dòng trượt <b>+1</b>, 3 dòng trượt <b>+37</b>.
        ⇒ Kế toán đã <b>CHÈN 37 dòng</b> vào vùng đuôi sau khi chụp bản sao.
        <div style="margin-top:7px">★ <b>Bài học đáng giá:</b> số dòng trên sheet là
        một <b>VỊ TRÍ</b>, ⛔ không phải một <b>DANH TÍNH</b>. Đây đúng là lý do sổ
        FLS lấy danh tính từ nội dung dòng (<span class="mono">content_key</span>,
        <span class="mono">INV-I04a</span>) — và hôm nay ta có <b>bằng chứng đo
        được</b> cho quyết định đó.</div>
      </div>
      <div class="note">
        ⚠ <b>Và ⛔ không chia theo KỲ.</b> Cột ngày chứng từ của sổ gốc bị
        <b>hoán ngày↔tháng ở 93% dòng</b> (đã đo) ⇒ mọi phép chia theo kỳ đều dựng
        trên một cái trục <b>đã biết là sai</b>.
      </div>
    </div>
    <div class="scroll">
      <table>
        <thead><tr><th>Tiền tệ</th>
          <th class="r">Dòng · kho</th><th class="r">Dòng · sổ sống</th>
          <th class="r">Khớp nội dung</th>
          <th class="r">Chỉ có ở KHO</th><th class="r">Chỉ có ở SỔ</th>
          <th>Kết luận</th></tr></thead>
        <tbody>{ds_rows or '<tr><td colspan="8" class="faint">⛔ không đo được</td></tr>'}</tbody>
      </table>
    </div>
    <div class="pad" style="border-top:1px solid var(--line)">
      <b>Kho:</b> <span class="num">{kho['dong_kho']:,}</span> dòng ·
      <b>Sổ sống:</b> <span class="num">{(song or {}).get('dong', 0):,}</span> dòng ·
      <b>Bị loại:</b> <span class="num">{kho['so_loai']}</span> dòng
      <span class="muted">({" · ".join(f"{x['so']} · {_e(str(x['ly_do'])[:58])}" for x in kho['loai'])})</span> ·
      <b>Danh mục phân bổ:</b> <span class="num">{kho['mm_so_ma']}</span> mã <span class="mono">hd</span>
    </div>
  </div>
</section>

<!-- ══════════════════ ② F01 ══════════════════ -->
<section class="sc" id="f01">
  <div class="card">
    <header><h3>Hàng chờ · VND</h3>
      <span class="chip info">xếp theo tiền giảm, trong TỪNG tiền tệ</span>
      <span class="spacer"></span><span class="muted" id="hc-con"></span></header>
    <div class="scroll"><table id="t-hc">
      <thead><tr><th class="r">Hạng</th><th>itl_id</th><th>Ngày CT</th>
        <th>Diễn giải</th><th class="r">Tiền</th><th class="r">% luỹ kế</th>
        <th>Trạng thái</th><th style="width:290px">Việc</th></tr></thead>
      <tbody></tbody></table></div>
    <div class="pad" style="border-top:1px solid var(--line);display:flex;gap:16px;flex-wrap:wrap">
      {hc_tom}<span class="spacer"></span>
      <span class="muted" style="font-size:12px">⛔ Không có dòng “tổng”.</span>
    </div>
  </div>
  <div class="card" id="card-daghep">
    <header><h3>Dòng ĐÃ ghép — để thử <b>Bỏ ghép</b></h3></header>
    <div class="pad" id="daghep-body"></div>
  </div>
</section>

<!-- ══════════════════ ③ F02 ══════════════════ -->
<section class="sc" id="f02">
  <div class="card">
    <header><h3>Sổ ITL · 7 ô gõ được</h3>
      <span class="chip lock">🔒 vùng phân bổ = máy suy</span>
      <span class="spacer"></span>
      <span class="chip ok" id="luu-tt">tự lưu · chưa có gì để lưu</span></header>
    <div class="scroll"><table id="t-so">
      <thead><tr><th>itl_id</th><th>Diễn giải</th><th class="r">Tiền</th>
        <th>Mã hợp đồng ✎</th><th>Chủ dự toán ✎</th><th>Loại GD ✎</th>
        <th>Bắt đầu DV ✎</th><th>Kết thúc DV ✎</th>
        <th>CFA2 🔒</th><th>Cách phân bổ 🔒</th></tr></thead>
      <tbody></tbody></table></div>
    <div class="pad" style="border-top:1px solid var(--line)">
      <span class="muted" style="font-size:12px">Gõ vào ô viền xanh → ô đổi
      <b style="color:var(--warn)">vàng (chưa lưu)</b> → sau ~2 giây thành
      <b style="color:var(--good)">xanh (đã lưu)</b>, và tab ④ in ra <b>máy sẽ ghi gì</b>.</span>
    </div>
  </div>
</section>

<!-- ══════════════════ ④ OUTPUT ══════════════════ -->
<section class="sc" id="mt">
  <div class="card">
    <header><h3>Máy sẽ ghi gì — nhật ký thao tác</h3>
      <span class="spacer"></span>
      <button class="b tiny" onclick="document.getElementById('out').textContent='';">Xoá</button></header>
    <div class="pad">
      <div class="note">⭐ Mỗi dòng dưới đây là <b>một lệnh ghi thật</b> mà cửa API sẽ
      thực hiện: <b>bảng nào</b>, <b>trường nào</b>, và <b>vì sao</b>. Demo ⛔ không
      ghi vào kho — nó chỉ <b>in ra ý định</b>.</div>
      <div id="out"><span class="n">— chưa có thao tác nào. Sang tab ② hoặc ③ và bấm/gõ thử. —</span></div>
    </div>
  </div>
  <div class="card">
    <header><h3>Bảy trường gõ được · và ranh giới</h3></header>
    <div class="pad">
      <div class="kv" id="kv-truong"></div>
    </div>
  </div>
</section>
</div>

<div class="dlg" id="dlg"><div>
  <header id="dlg-t"></header>
  <div class="bd" id="dlg-b"></div>
  <div class="ft" id="dlg-f"></div>
</div></div>

<script>
const DU = {json.dumps(du, ensure_ascii=False)};
const $ = s => document.querySelector(s);
const el = (t, c, h) => {{ const e = document.createElement(t);
  if (c) e.className = c; if (h !== undefined) e.innerHTML = h; return e; }};
const tien = v => Number(v || 0).toLocaleString('vi-VN',
  {{ maximumFractionDigits: 0 }});

/* ── nhật ký OUTPUT ─────────────────────────────────────────────────── */
function log(kind, dong) {{
  const o = $('#out');
  if (o.querySelector('.n')) o.textContent = '';
  const gio = new Date().toLocaleTimeString('vi-VN');
  const cls = {{ ghi: 'g', chan: 'r', canh: 'w', doc: 't' }}[kind] || 'n';
  o.insertAdjacentHTML('beforeend',
    `<span class="n">${{gio}}</span>  <span class="${{cls}}">${{dong}}</span>\\n`);
  o.scrollTop = o.scrollHeight;
}}

/* trạng thái phiên — demo giữ trong bộ nhớ, ⛔ không ghi kho */
const ST = {{ xong: new Set(), moi_noi: {{}}, sua: {{}} }};
if (DU.da_ghep) ST.moi_noi[DU.da_ghep.itl_id] = DU.da_ghep.moi_noi.slice();

/* ── ② HÀNG CHỜ ────────────────────────────────────────────────────── */
function veHangCho() {{
  const tb = $('#t-hc tbody'); tb.textContent = '';
  let con = 0;
  DU.hang_cho.forEach(function (r) {{
    const daXong = ST.xong.has(r.itl_id);
    if (!daXong) con++;
    const tr = el('tr');
    if (daXong) tr.style.opacity = '.55';
    const noi = ST.moi_noi[r.itl_id];
    tr.innerHTML =
      `<td class="r">${{daXong ? '—' : r.hang}}</td>` +
      `<td class="mono">${{r.itl_id}}</td>` +
      `<td class="mono">${{r.ngay}}</td>` +
      `<td>${{r.memo.replace(/</g, '&lt;')}}` +
        (noi && noi.length ? ` <span class="chip info">đã ghép ${{noi.length}} dòng lệnh</span>` : '') +
        (daXong ? ` <span class="chip ok">xong</span>` : '') + `</td>` +
      `<td class="r">${{tien(r.tien)}}</td>` +
      `<td class="r">${{r.pct}}%</td>` +
      `<td>${{daXong ? '<span class="chip ok">đã rời hàng chờ</span>'
                     : '<span class="chip warn">chưa gán</span>'}}</td>`;
    const td = el('td');
    if (daXong) {{
      const b = el('button', 'b tiny', 'Mở lại');
      b.onclick = () => moLai(r); td.appendChild(b);
    }} else {{
      if (DU.ghep && DU.ghep.itl_id === r.itl_id && !(noi && noi.length)) {{
        const g = el('button', 'b tiny pri', 'Ghép'); g.onclick = mophep;
        td.appendChild(g);
      }}
      if (noi && noi.length) {{
        const u = el('button', 'b tiny', 'Bỏ ghép');
        u.onclick = () => moBoGhep(r.itl_id); td.appendChild(u);
      }}
      const x = el('button', 'b tiny', 'Xong'); x.onclick = () => bamXong(r);
      td.appendChild(x);
    }}
    tr.appendChild(td); tb.appendChild(tr);
  }});
  $('#hc-con').innerHTML = `<span class="num">${{con}}</span> / ${{DU.hang_cho.length}} dòng còn trong hàng chờ`;
  veDaGhep();
}}

function bamXong(r) {{
  ST.xong.add(r.itl_id);
  const thieu = DU.truong_hop_dong.filter(function (f) {{
    const s = DU.so.find(x => x.itl_id === r.itl_id);
    return s ? !String((ST.sua[r.itl_id] || {{}})[f] || s[f] || '').trim() : true;
  }});
  log('ghi', `POST /queue/${{r.itl_id}}/done`);
  log('ghi', `  → fls_queue_event: evt_type='done' · actor='ke-toan@apero.vn' · reason=NULL`);
  log('canh', `  ⚠ reason RỖNG là ĐÚNG — QĐ-ITL-72: bấm xong ⛔ không cần lý do`);
  log('doc', `  → fls_itl: ⛔ KHÔNG một ô nào đổi (INV-I08)`);
  log('doc', `  → hàng chờ trừ dòng này qua khung xem fls_da_xong (phép TÍNH, ⛔ không phải cột)`);
  if (thieu.length) log('canh',
    `  ⚠ dòng này xong MÀ CÒN THIẾU: ${{thieu.join(', ')}} → máy trả thieu_truong[] để màn hình HIỆN, và phép đếm dem_xong_du_thieu() +1`);
  veHangCho();
}}

function moLai(r) {{
  moDlg('Mở lại · itl_id ' + r.itl_id,
    `<p style="margin:0 0 9px">Kéo dòng này về hàng chờ?</p>
     <div class="note warn" style="margin:0">⚠ <b>Lý do BẮT BUỘC</b> ở đây — khác nút
     <i>Xong</i>. Dòng này đã có NGƯỜI kết luận là xong, kéo lại là
     <b>lật kết luận của người khác</b>.</div>
     <input class="cell" id="ml-r" placeholder="Vì sao mở lại…" style="margin-top:9px;font-family:var(--sans)">`,
    [['Thôi', null], ['Mở lại', function () {{
      const v = ($('#ml-r').value || '').trim();
      if (!v) {{ log('chan', `⛔ 400 — POST /queue/${{r.itl_id}}/reopen thiếu reason ⇒ BỊ CHẶN`); return false; }}
      ST.xong.delete(r.itl_id);
      log('ghi', `POST /queue/${{r.itl_id}}/reopen`);
      log('ghi', `  → fls_queue_event: evt_type='reopen' · reason='${{v.replace(/</g, '&lt;')}}'`);
      log('doc', `  → sự kiện 'done' cũ VẪN nằm trong sổ — mở lại là THÊM một dòng, ⛔ không xoá`);
      veHangCho(); return true;
    }}]]);
}}

/* ── drawer GHÉP ───────────────────────────────────────────────────── */
function mophep() {{
  const g = DU.ghep;
  const bank = Number(g.tien_bank);
  const rows = g.ung_vien.map(function (u, i) {{
    const bac = {{ ma: '<span class="chip ok">mã khớp</span>',
      tien: '<span class="chip info">tiền khớp</span>',
      gan_tien: '<span class="chip warn">gần tiền</span>',
      cung_tien_te: '<span class="chip lock">cùng tiền tệ</span>' }}[u.bac] || u.bac;
    return `<tr><td><input type="checkbox" data-i="${{i}}" data-a="${{u.amount}}"></td>
      <td class="mono">${{u.pm_line_id}}</td><td>${{bac}}</td>
      <td class="r">${{tien(u.amount)}}</td>
      <td>${{u.status || '<span class="faint">—</span>'}}</td>
      <td>${{u.da_ghep > 0 ? '<span class="chip warn">đã ghép nơi khác</span>' : ''}}</td></tr>`;
  }}).join('');
  moDlg('Ghép lệnh · itl_id ' + g.itl_id,
    `<div class="note" style="margin-top:0"><b>Dòng tiền (ghim):</b>
       <span class="num">${{tien(bank)}}</span> VND — ${{g.memo.replace(/</g, '&lt;').slice(0, 70)}}</div>
     <table><thead><tr><th></th><th>Dòng lệnh</th><th>Độ khớp</th>
       <th class="r">Tiền lệnh</th><th>Trạng thái</th><th></th></tr></thead>
       <tbody>${{rows}}</tbody></table>
     <div class="note" id="sig" style="margin-bottom:0"></div>`,
    [['Thôi', null], ['Ghép', function () {{
      const ck = [...document.querySelectorAll('#dlg-b input[type=checkbox]:checked')];
      const tong = ck.reduce((s, c) => s + Number(c.dataset.a), 0);
      const ds = Math.min(1000, Math.abs(bank) * Number(DU.ty_le));
      if (!ck.length || Math.abs(tong - bank) > ds) {{
        log('chan', `⛔ 422 — POST /queue/${{g.itl_id}}/match BỊ CHẶN: Σ ${{tien(tong)}} vs bank ${{tien(bank)}} · lệch ${{tien(tong - bank)}} > dung sai ${{tien(ds)}}`);
        log('canh', `  ⚠ dung sai TAY = min(1.000 đồng, ${{Number(DU.ty_le) * 100}}% của tiền bank) — QĐ-ITL-63, ⛔ KHÁC dung sai của máy`);
        log('doc', `  → GIỮ UNMAPPED, ⛔ không chia bừa (INV-I16)`);
        return false;
      }}
      const ma = ck.map(c => DU.ghep.ung_vien[Number(c.dataset.i)]);
      ST.moi_noi[g.itl_id] = ma.map(u => ({{ pm_line_id: u.pm_line_id, amount: u.amount, lan: 1 }}));
      log('ghi', `POST /queue/${{g.itl_id}}/match  {{pm_line_ids: [${{ma.map(u => "'" + u.pm_line_id + "'").join(', ')}}]}}`);
      log('doc', `  ⚠ thân yêu cầu là danh sách mã DÒNG, ⛔ KHÔNG mã phiếu — 526 phiếu mang 2–36 reference khác nhau (CR#6)`);
      log('ghi', `  → fls_queue_event: evt_type='match' (chèn TRƯỚC, để bút toán trỏ về nó)`);
      ma.forEach(u => log('ghi', `  → fls_pm_link: ${{u.pm_line_id}} · ${{tien(u.amount)}} · hinh='T' · lan=1`));
      const hd = [...new Set(ma.map(u => u.hd).filter(Boolean))];
      const cd = [...new Set(ma.map(u => u.cdt1).filter(Boolean))];
      if (hd.length === 1) log('ghi', `  → fls_adjustment + fls_journal: hd='${{hd[0]}}' (SUY từ dòng lệnh, evt_id trỏ về thao tác ghép)`);
      else if (hd.length > 1) log('canh', `  ⚠ ${{hd.length}} dòng lệnh nói ${{hd.length}} mã hd khác nhau ⇒ máy KHAI 'khong_suy_duoc', ⛔ không tự chọn (INV-I16)`);
      if (cd.length === 1) log('ghi', `  → fls_adjustment + fls_journal: cdt1='${{cd[0]}}' (SUY từ dòng lệnh)`);
      log('doc', `  → fls_itl: ⛔ KHÔNG một ô nào đổi`);
      veHangCho(); return true;
    }}]]);
  function tinhSig() {{
    const ck = [...document.querySelectorAll('#dlg-b input[type=checkbox]:checked')];
    const tong = ck.reduce((s, c) => s + Number(c.dataset.a), 0);
    const ds = Math.min(1000, Math.abs(bank) * Number(DU.ty_le));
    const lech = tong - bank, ok = ck.length && Math.abs(lech) <= ds;
    $('#sig').className = 'note ' + (ok ? 'ok' : 'crit');
    $('#sig').innerHTML = `Σ dòng lệnh <b class="num">${{tien(tong)}}</b> / tiền bank
      <b class="num">${{tien(bank)}}</b> · lệch <b class="num">${{tien(lech)}}</b>
      · dung sai <b class="num">${{tien(ds)}}</b> ` +
      (ok ? '<span class="chip ok">khớp — cho ghép</span>'
          : '<span class="chip no">⛔ lệch — nút Ghép sẽ CHẶN, giữ UNMAPPED</span>');
    const b = [...document.querySelectorAll('#dlg-f button')].pop();
    if (b) b.disabled = !ok;
  }}
  document.querySelectorAll('#dlg-b input[type=checkbox]').forEach(
    c => c.addEventListener('change', tinhSig));
  tinhSig();
}}

function moBoGhep(id) {{
  const noi = ST.moi_noi[id] || [];
  moDlg('Bỏ ghép · itl_id ' + id,
    `<p style="margin:0 0 9px">Bỏ <b>cả chùm</b> ${{noi.length}} mối nối?</p>
     <table><tbody>${{noi.map(n => `<tr><td class="mono">${{n.pm_line_id}}</td>
       <td class="r">${{tien(n.amount)}}</td></tr>`).join('')}}</tbody></table>
     <div class="note" style="margin-top:9px">⭐ <b>Sổ ⛔ không mất gì.</b> Bỏ mối nối là
       <b>thêm một dòng</b>; lịch sử mọi lần ghép vẫn đọc lại được, và ghép lại được
       kể cả đúng dòng lệnh cũ (sẽ là <i>lần 2</i>).</div>
     <div class="note warn" style="margin:0">⚠ <b>Bỏ CẢ CHÙM, ⛔ không bỏ lẻ</b> — bỏ lẻ
       làm Σ ≠ tiền bank, tức tạo ra đúng cái trạng thái sai mà cổng dựng ra để bắt.</div>`,
    [['Thôi', null], ['Bỏ ghép', function () {{
      delete ST.moi_noi[id];
      log('ghi', `POST /queue/${{id}}/unmatch  {{reason: '…'}}`);
      log('doc', `  ⚠ POST chứ ⛔ không DELETE: bỏ một mối nối là THÊM một dòng (INV-I08)`);
      log('ghi', `  → fls_queue_event: evt_type='unmatch'`);
      noi.forEach(n => log('ghi', `  → fls_pm_unlink: link_id của ${{n.pm_line_id}} (bảng gốc fls_pm_link GIỮ NGUYÊN)`));
      log('ghi', `  → fls_adjustment: ĐẢO bút toán hd/cdt1 do CHÍNH phép ghép suy ra (state='reversed')`);
      log('canh', `  ⚠ ô nào NGƯỜI đã gõ tay sau phép ghép thì ⛔ KHÔNG đảo — máy trả bo_qua[] và màn hình PHẢI hiện`);
      veHangCho(); return true;
    }}]]);
}}

function veDaGhep() {{
  const b = $('#daghep-body');
  if (!DU.da_ghep) {{ b.innerHTML = '<span class="faint">⛔ kho ⛔ không có dòng VND nào đang có mối nối.</span>'; return; }}
  const id = DU.da_ghep.itl_id, noi = ST.moi_noi[id];
  b.innerHTML =
    `<div><b class="mono">itl_id ${{id}}</b> · <span class="num">${{tien(DU.da_ghep.tien)}}</span> VND ·
      ${{DU.da_ghep.memo.replace(/</g, '&lt;').slice(0, 80)}}</div>
     <div style="margin-top:8px">` +
    (noi && noi.length
      ? noi.map(n => `<span class="chip info">${{n.pm_line_id}} · ${{tien(n.amount)}} · lần ${{n.lan}}</span> `).join('')
      : '<span class="chip warn">⛔ không còn mối nối nào — đã bỏ</span>') +
    `</div><div style="margin-top:10px" id="dg-btn"></div>`;
  const w = $('#dg-btn');
  if (noi && noi.length) {{
    const u = el('button', 'b', 'Bỏ ghép cả chùm'); u.onclick = () => moBoGhep(id); w.appendChild(u);
  }} else {{
    const g = el('button', 'b pri', 'Ghép lại đúng dòng lệnh cũ (lần 2)');
    g.onclick = function () {{
      ST.moi_noi[id] = DU.da_ghep.moi_noi.map(n => ({{ ...n, lan: (n.lan || 1) + 1 }}));
      log('ghi', `POST /queue/${{id}}/match — GHÉP LẠI đúng dòng lệnh vừa gỡ`);
      log('doc', `  ⭐ Đây là việc mà KHOÁ CŨ (itl_id, pm_line_id) sẽ CHẶN bằng lỗi trùng khoá.`);
      log('doc', `  ⭐ Khoá mới đếm LẦN ghép ⇒ chèn được với lan=2 (QĐ-ITL-69, migration 0013)`);
      veDaGhep();
    }};
    w.appendChild(g);
  }}
}}

/* ── ③ SỔ ITL ─────────────────────────────────────────────────────── */
function veSo() {{
  const tb = $('#t-so tbody'); tb.textContent = '';
  DU.so.forEach(function (r) {{
    const tr = el('tr');
    tr.innerHTML = `<td class="mono">${{r.itl_id}}</td>
      <td>${{r.memo.replace(/</g, '&lt;').slice(0, 46)}}</td>
      <td class="r">${{tien(r.tien)}}</td>`;
    ['hd', 'cdt1', 'pay_type', 'svc_start', 'svc_end'].forEach(function (f) {{
      const td = el('td'); if (!r[f]) td.className = 'unmapped';
      const i = el('input', 'cell'); i.value = r[f] || '';
      i.placeholder = 'chưa gán'; i.dataset.f = f; i.dataset.id = r.itl_id;
      i.addEventListener('input', () => goO(i, r));
      td.appendChild(i); tr.appendChild(td);
    }});
    const a = r.alloc;
    tr.insertAdjacentHTML('beforeend',
      `<td class="ro">${{a.khong_tra_duoc ? '<span class="faint mono">#N/A</span>'
        : (a.cfa2 || '<span class="faint">—</span>')}}</td>
       <td class="ro">${{a.khong_tra_duoc ? '<span class="faint mono">#N/A</span>'
        : (a.method === '0' ? '<span class="mono" title="bẫy VLOOKUP: ô Method của danh mục RỖNG nên Sheets cho 0">0</span>'
                            : a.method)}}</td>`);
    tb.appendChild(tr);
  }});
}}

let hen = null;
function goO(i, r) {{
  i.classList.add('dirty'); i.classList.remove('saved');
  ST.sua[r.itl_id] = ST.sua[r.itl_id] || {{}};
  ST.sua[r.itl_id][i.dataset.f] = i.value;
  $('#luu-tt').className = 'chip warn'; $('#luu-tt').textContent = 'tự lưu · đang chờ…';
  clearTimeout(hen);
  hen = setTimeout(function () {{
    document.querySelectorAll('input.cell.dirty').forEach(function (c) {{
      c.classList.remove('dirty'); c.classList.add('saved');
      const cu = (DU.so.find(x => x.itl_id === Number(c.dataset.id)) || {{}})[c.dataset.f] || '';
      const moi = c.value;
      if (cu && cu !== moi) {{
        log('chan', `⛔ 409 — POST /ledger/${{c.dataset.id}}/adjust {{field:'${{c.dataset.f}}'}} : giá trị KHÁC NGUỒN`);
        log('canh', `  ⚠ nguồn đang có '${{cu}}' — US-025: hệ phải KÊU. Cần force=true + lý do mới ghi được`);
      }} else {{
        log('ghi', `POST /ledger/${{c.dataset.id}}/adjust {{field:'${{c.dataset.f}}', value:'${{moi}}'}}`);
        log('ghi', `  → fls_adjustment: THÊM một dòng (⛔ không UPDATE dòng cũ)`);
        log('ghi', `  → fls_journal: 7 trường AUD-1 · value_source='${{cu ? 'nguon' : 'UNMAPPED'}}'`);
        log('doc', `  → fls_itl: ⛔ KHÔNG đổi. "Giá trị hiện tại" là khung xem fls_sua_tay`);
      }}
    }});
    $('#luu-tt').className = 'chip ok';
    $('#luu-tt').textContent = 'tự lưu · đã lưu ' + new Date().toLocaleTimeString('vi-VN');
  }}, 2000);
}}

/* ── ④ bảng trường ────────────────────────────────────────────────── */
function veTruong() {{
  const w = $('#kv-truong');
  const noi = {{
    hd: 'Mã hợp đồng — vào P&L, có cột đo parity',
    cdt1: 'Chủ dự toán — vào P&L, có cột đo parity',
    pay_type: 'Loại giao dịch — vào P&L',
    svc_start: 'Bắt đầu dịch vụ — vào P&L',
    svc_end: 'Kết thúc dịch vụ — vào P&L',
    id_payee: 'Mã đối tác — ⛔ NGOÀI P&L',
    invoice: 'Hoá đơn — ⛔ NGOÀI P&L, chở ĐƯỜNG DẪN Drive'
  }};
  DU.truong_ghi.forEach(function (f) {{
    w.appendChild(el('div', null, '<span class="mono">' + f + '</span>'));
    w.appendChild(el('div', null, noi[f] || ''));
  }});
  w.appendChild(el('div', null, '<b>⛔ 31 cột còn lại</b>'));
  w.appendChild(el('div', null, 'CHỈ ĐỌC — gõ tên khác thì cửa trả <span class="mono">400</span> kèm danh sách 7 trường'));
  w.appendChild(el('div', null, '<b>⛔ Vùng phân bổ</b>'));
  w.appendChild(el('div', null, '🔒 máy suy từ <span class="mono">cdt1</span> + <span class="mono">hd</span> + danh mục — ⛔ KHÔNG có ô gõ (QĐ-ITL-64/65)'));
  w.appendChild(el('div', null, '<b>⛔ Kỳ đã CHỐT</b>'));
  w.appendChild(el('div', null, 'chặn mọi phép ghi, ⛔ kể cả khi xác nhận (INV-I13) — nhưng <b>vẫn bấm Xong được</b> (QĐ-ITL-71)'));
}}

/* ── hộp thoại ────────────────────────────────────────────────────── */
function moDlg(tieu_de, than, nut) {{
  $('#dlg-t').textContent = tieu_de; $('#dlg-b').innerHTML = than;
  const f = $('#dlg-f'); f.textContent = '';
  nut.forEach(function (n, i) {{
    const b = el('button', 'b' + (i === nut.length - 1 ? ' pri' : ''), n[0]);
    b.onclick = function () {{
      if (!n[1]) {{ $('#dlg').classList.remove('on'); return; }}
      if (n[1]() !== false) $('#dlg').classList.remove('on');
    }};
    f.appendChild(b);
  }});
  $('#dlg').classList.add('on');
}}
$('#dlg').addEventListener('click', function (e) {{
  if (e.target.id === 'dlg') $('#dlg').classList.remove('on');
}});

document.querySelectorAll('.tabs button').forEach(function (b) {{
  b.onclick = function () {{
    document.querySelectorAll('.tabs button').forEach(
      x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    document.querySelectorAll('section.sc').forEach(
      s => s.classList.toggle('on', s.id === b.dataset.s));
    window.scrollTo({{ top: 0 }});
  }};
}});

veHangCho(); veSo(); veTruong();
</script>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--khong-mang", action="store_true",
                   help="⛔ khong doc so song (chi doc kho)")
    a = p.parse_args(argv)

    from datetime import datetime, timezone, timedelta
    gio = datetime.now(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M")

    with psycopg.connect(dsn_that(), autocommit=True) as c:
        kho = doc_kho(c)
    print(f"kho: {kho['dong_kho']:,} dong · hang cho VND {len(kho['hang_cho'])} dong"
          f" · trang so {len(kho['so'])} dong"
          f" · danh muc {kho['mm_so_ma']} ma")

    song = None
    if not a.khong_mang:
        try:
            song = doc_song()
            print(f"so song: {song['dong']:,} dong (tab {BAN_SAO_RAW.sheet!r},"
                  f" tu dong {song['dong_dau']})")
        except Exception as e:                                 # noqa: BLE001
            print(f"⛔ khong doc duoc so song: {type(e).__name__}: {e}")
            print("   ⇒ phan DOI SOAT se ghi '⛔ khong do duoc', "
                  "⛔ khong ghi 'khop'")

    ds = doi_soat(kho, song)
    if ds.get("do_duoc"):
        c = ds["cong"]
        print("\ndoi soat kho <-> so song, theo NOI DUNG (⛔ khong theo vi tri):")
        for r in ds["theo_te"]:
            print(f"  {r['curr']:>8}  kho {r['kho_dong']:>5} · so {r['song_dong']:>5}"
                  f" · khop {r['khop']:>5} · chi-kho {r['chi_kho']:>3}"
                  f" · chi-so {r['chi_song']:>3}")
        print(f"\n  khop noi dung : {ds['khop']:,}")
        print(f"  chi o KHO     : {ds['chi_kho']}   "
              + ("⇒ ⛔ KHONG mat dong nao" if ds["chi_kho"] == 0
                 else "⇒ ⛔⛔ CO DONG BI MAT"))
        print(f"  chi o SO SONG : {ds['chi_song']}")
        print(f"\n  phep cong: {c['da_nap']:,} da nap + {c['bi_loai']} bi loai"
              f" + {c['them_sau']} them sau = {c['so_song']:,} dong so song "
              + ("✅" if c['da_nap'] + c['bi_loai'] + c['them_sau'] == c['so_song']
                 else "⛔ KHONG DONG"))

    RA.parent.mkdir(parents=True, exist_ok=True)
    RA.write_text(sinh(kho, song, ds, gio), encoding="utf-8")
    print(f"\nda ghi {RA}  ({RA.stat().st_size:,} byte)")
    print("⛔ Tep nay cho DU LIEU KE TOAN THAT (cot `memo`) — `hien_vat/` da "
          "gitignore. ⛔ Dung gui qua Zalo/email.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
