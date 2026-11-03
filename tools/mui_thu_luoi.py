"""Dung MUI THU LUOI `F02` tu DU LIEU THAT — `GAP-SCR-03`.

    python tools/mui_thu_luoi.py                    # kho THAT, ky day nhat
    python tools/mui_thu_luoi.py --ky 2026-07        # mot ky cu the
    python tools/mui_thu_luoi.py --test --dong 100

Sinh ra MOT tep `.html` **tu chua** (⛔ khong mang, ⛔ khong thu vien ngoai) de
chu so va ke toan **mo ra go thu that** — do dung la cai `GAP-SCR-03` doi:
*"chay thu voi LAN/THUONG tren vai chuc dong that, do 'co thua Sheets o dau'"*.

⛔⛔ **VI SAO MUI THU NAY KHONG DUNG THU VIEN NAO.** `BA-06` §6b khao sat 7 thu
vien va chon `react-datasheet-glid` vi bai toan *"~64 cot x vai nghin dong, chi 5
cot sua duoc"* doi **ao hoa** (virtualization). Nhung `tools/do_luoi_f02.py` do
tren kho that ra ba con so KHAC:

    cot luoi     : **52** (38 canon + 14 hop dong), ⛔ khong phai ~64
    cot sua duoc : **10**, ⛔ khong phai 5 (`QĐ-owner-0824` da mo 5 -> 10)
    dong MOT LAT : **ky day nhat 748 dong**, ⛔ khong phai "vai nghin"
                   (F02 loc theo ky; ca so 10.030 nhung khong ai mo ca so)

⇒ Bai toan that la **~750 x 52 = ~39.000 o**, va o quy mo do thi **ao hoa CO THE
khong can**, ma neu khong can ao hoa thi ly do chinh de chon thu vien tan mat.
Nen mui thu nay tra loi cau **re nhat truoc**: *mot bang HTML tran, khong thu vien,
co du 8 hanh vi khong?* Neu DU thi ta tiet kiem ca mot phu thuoc; neu THIEU thi
biet **thieu dung cho nao**, va do la dau vao that cho phep chon thu vien.

★ Tam hanh vi `BA-06` §1, va tep sinh ra **tu khai** cai nao lam duoc bang MAY:
  1 dieu huong ban phim   · 2 dan mot vung  · 3 keo xuong  · 4 hoan tac
  5 filter view           · 6 dong cung tieu de + cot khoa
  7 so kieu ke toan       · 8 luu khong can bam (gom lo)
"""
from __future__ import annotations

import argparse
import html
import json
import os
import pathlib
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fls.canon.spec import CANON_COLS                      # noqa: E402
from fls.ledger.classifying import VI_TRI_CLASSIFYING      # noqa: E402
from fls.db.kho import dsn_test, dsn_that                  # noqa: E402
from fls.repo.ghi_tay import TRUONG_GHI                    # noqa: E402

# ⛔⛔ Tung co 3 cot vung ALLOCATE o day (`cdt1_cfa1` `cdt1_cfa2`
# `alloc_method`) — BO 2026-08-28 vi owner chot bo chung khoi khuon kho
# (`QĐ-ITL-65`, migration `0012`): ca ba SUY LAI DUOC tu `cdt1` + `hd` +
# `Mapping Master`, va ke toan ⛔ khong sua chung (`QĐ-ITL-64`).
# ⇒ Luoi ve **52 cot**. Vung phan bo se **hien lai** khi `fls_mapping_master`
#   co bo nap — luc do la mot **phep tinh** (`ledger/allocate.py`), ⛔ khong
#   phai mot cot cua so.
COT_NGOAI_THEM: tuple[str, ...] = ()

# Ten cho NGUOI doc. ⛔ Truoc 28/08 luoi in `k` — tuc ten cot ky thuat cho 14
# cot dau va **CHU CAI** (`Y`, `AD`, `AL`...) cho 38 cot canon. Ke toan ⛔ khong
# tim duoc mot cot ma ho ⛔ khong doc duoc ten.
TEN_CHO_NGUOI = {
    "itl_id": "Số ITL", "doc_date": "Ngày chứng từ", "doc_no": "Số chứng từ",
    "curr": "Tiền tệ", "ps_no": "PS Nợ", "ps_co": "PS Có",
    "le": "Pháp nhân", "acct": "Tài khoản", "memo": "Diễn giải",
    "hd": "Budget Code (HDCode)", "pay_type": "Loại giao dịch",
    "cdt1": "Chủ dự toán (CDT1)",
    "svc_start": "Dịch vụ · bắt đầu", "svc_end": "Dịch vụ · kết thúc",
    # ⛔ Ba cot nay do duoc la **0% trong kho** (bo nap chi doc `Transaction
    # Mapping L1`, con vung ALLOCATE nam o so ADJUSTED) ⇒ tieu de PHAI noi ra,
    # ⛔ khong de mot cot rong trong nhu mot cot "chua ai dien".
    # ⭐ 28/08: owner dua nguyen van 3 cong thuc ⇒ ca ba o nay tren sheet la
    # CONG THUC, suy lai duoc tu `cdt1` + `hd` + `Mapping Master` K/L
    # (`fls/ledger/allocate.py`). Kho chua nap `Mapping Master` (0 dong) nen
    # chung con rong — tieu de phai noi CA HAI dieu do.
    # (3 cot vung ALLOCATE da bo — xem `COT_NGOAI_THEM` o tren)
}

COT_HOP_DONG = ("itl_id", "doc_date", "doc_no", "curr", "ps_no", "ps_co",
                "le", "acct", "memo", "hd", "pay_type", "cdt1", "svc_start",
                "svc_end")
# ⛔ Cot KHOA ben trai phai dong cung: khong co chung thi cuon sang phai la mat
# phuong huong — dung hanh vi so 6.
COT_DONG_CUNG = ("itl_id", "doc_date", "doc_no")
COT_TIEN = ("ps_no", "ps_co")
# ⭐ Be rong KHAI cho ba cot dong cung — xem ghi chu o cho dung CSS ben duoi.
# ⛔ Doi con so o day thi `left` tu doi theo; ⛔ khong co cho thu hai de lech.
RONG_DONG_CUNG = {"itl_id": 76, "doc_date": 100, "doc_no": 170}

_HTML = """<!doctype html>
<meta charset="utf-8">
<title>Mui thu luoi F02 — {n_dong} dong x {n_cot} cot</title>
<style>
  :root {{ --vien:#d0d7de; --dau:#f6f8fa; --sua:#fffbe6; --do:#cf222e;
           --chon:#0969da; --nhat:#8c959f; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:13px/1.45 -apple-system,Segoe UI,system-ui,sans-serif;
          color:#1f2328; }}
  header {{ padding:10px 14px; border-bottom:1px solid var(--vien);
            display:flex; gap:16px; align-items:center; flex-wrap:wrap; }}
  header b {{ font-size:14px; }}
  .canh {{ color:var(--nhat); font-size:12px; }}
  #loc {{ padding:4px 8px; border:1px solid var(--vien); border-radius:6px; }}
  #trangthai {{ margin-left:auto; font-size:12px; padding:3px 10px;
                border-radius:999px; background:var(--dau); }}
  #trangthai.dang {{ background:#fff8c5; }}
  #trangthai.xong {{ background:#dafbe1; }}
  .khung {{ overflow:auto; height:calc(100vh - 118px); }}
  table {{ border-collapse:separate; border-spacing:0; font-variant-numeric:tabular-nums; }}
  th, td {{ border-right:1px solid var(--vien); border-bottom:1px solid var(--vien);
            padding:3px 7px; white-space:nowrap; max-width:260px; overflow:hidden;
            text-overflow:ellipsis; background:#fff; }}
  thead th {{ position:sticky; top:0; z-index:3; background:var(--dau);
              font-weight:600; text-align:left; }}
  /* ⓺ dong cung CA tieu de LAN cac cot khoa ben trai */
  .k0 {{ position:sticky; z-index:2; background:#fff; }}
  thead .k0 {{ z-index:4; background:var(--dau); }}
  td.sua {{ background:var(--sua); cursor:text; }}
  td.tien {{ text-align:right; }}
  td.am {{ color:var(--do); }}
  td.chon {{ outline:2px solid var(--chon); outline-offset:-2px; }}
  td.ban {{ box-shadow:inset 3px 0 0 #bf8700; }}
  footer {{ padding:8px 14px; border-top:1px solid var(--vien); font-size:12px;
            color:var(--nhat); }}
  kbd {{ font:11px ui-monospace,monospace; border:1px solid var(--vien);
         border-bottom-width:2px; border-radius:4px; padding:0 4px; }}
</style>

<header>
  <b>Mui thu luoi F02</b>
  <span class="canh">{n_dong} dong x {n_cot} cot &middot; {n_sua} cot sua duoc
    &middot; du lieu THAT, ky {ky}</span>
  <input id="loc" placeholder="loc view (go de loc moi cot)&hellip;" size="26">
  <span id="trangthai">chua sua gi</span>
</header>

<div class="khung"><table id="luoi">
<thead><tr>{dau}</tr></thead>
<tbody>{than}</tbody>
</table></div>

<footer>
  <kbd>Tab</kbd>/<kbd>Enter</kbd>/<kbd>&larr;&uarr;&darr;&rarr;</kbd> di chuyen
  &middot; go de sua &middot; <kbd>Ctrl+V</kbd> dan mot vung
  &middot; <kbd>Ctrl+D</kbd> keo xuong tu o tren
  &middot; <kbd>Ctrl+Z</kbd> hoan tac
  &middot; tu luu sau 2,5s &mdash; <b>khong co nut Luu</b>
</footer>

<script>
const SUA = new Set({sua_json});
const state = {{ o:null, lich:[], hen:null, ban:new Set() }};
const luoi = document.getElementById('luoi');
const tt = document.getElementById('trangthai');

function o_tai(r, c) {{
  const tr = luoi.tBodies[0].rows[r];
  return tr ? tr.cells[c] : null;
}}
function chon(td) {{
  if (!td) return;
  if (state.o) state.o.classList.remove('chon');
  state.o = td; td.classList.add('chon');
  td.scrollIntoView({{block:'nearest', inline:'nearest'}});
}}
function toa_do(td) {{ return [td.parentNode.rowIndex - 1, td.cellIndex]; }}

/* ⓼ gom lo: moi lan sua chi hen lai dong ho, ⛔ khong ban di ngay mot o */
function danh_dau(td, cu) {{
  state.lich.push({{td, cu}});
  state.ban.add(td); td.classList.add('ban');
  tt.textContent = state.ban.size + ' o cho luu…';
  tt.className = 'dang';
  clearTimeout(state.hen);
  state.hen = setTimeout(() => {{
    const n = state.ban.size;
    state.ban.forEach(x => x.classList.remove('ban'));
    state.ban.clear();
    tt.textContent = 'da luu ' + n + ' o (mot lo)';
    tt.className = 'xong';
  }}, 2500);
}}
function dat(td, v) {{
  if (!SUA.has(td.dataset.cot)) return false;
  const cu = td.textContent;
  if (cu === v) return false;
  td.textContent = v; danh_dau(td, cu); return true;
}}

luoi.addEventListener('click', e => {{
  const td = e.target.closest('td'); if (td) chon(td);
}});

document.addEventListener('keydown', e => {{
  const td = state.o; if (!td) return;
  const [r, c] = toa_do(td);
  const di = {{ArrowUp:[-1,0], ArrowDown:[1,0], ArrowLeft:[0,-1],
              ArrowRight:[0,1], Enter:[1,0], Tab:[0,1]}}[e.key];

  /* ⓸ hoan tac */
  if ((e.ctrlKey||e.metaKey) && e.key.toLowerCase() === 'z') {{
    const b = state.lich.pop();
    if (b) {{ b.td.textContent = b.cu; chon(b.td);
              tt.textContent = 'da hoan tac'; tt.className = ''; }}
    e.preventDefault(); return;
  }}
  /* ⓷ keo xuong: lay gia tri o NGAY TREN */
  if ((e.ctrlKey||e.metaKey) && e.key.toLowerCase() === 'd') {{
    const tren = o_tai(r-1, c);
    if (tren) dat(td, tren.textContent);
    e.preventDefault(); return;
  }}
  if (e.ctrlKey || e.metaKey || e.altKey) return;

  /* ⓵ dieu huong ban phim */
  if (di) {{
    if (e.key === 'Tab' && e.shiftKey) di[1] = -1;
    chon(o_tai(r + di[0], c + di[1]) || td);
    e.preventDefault(); return;
  }}
  /* go de sua ngay, ⛔ khong can bam dup */
  if (e.key.length === 1 && SUA.has(td.dataset.cot)) {{
    dat(td, e.key); td.focus?.();
    e.preventDefault(); return;
  }}
  if (e.key === 'Backspace' && SUA.has(td.dataset.cot)) {{
    dat(td, ''); e.preventDefault();
  }}
}});

/* ⓶ dan MOT VUNG: tach theo tab/newline roi rai tu o dang chon */
document.addEventListener('paste', e => {{
  const td = state.o; if (!td) return;
  const txt = (e.clipboardData || window.clipboardData).getData('text');
  const bang = txt.replace(/\\r/g, '').split('\\n').filter(x => x !== '')
                  .map(x => x.split('\\t'));
  const [r0, c0] = toa_do(td);
  let n = 0;
  bang.forEach((hang, i) => hang.forEach((v, j) => {{
    const x = o_tai(r0 + i, c0 + j);
    if (x && dat(x, v)) n++;
  }}));
  tt.textContent = 'dan ' + n + ' o';
  e.preventDefault();
}});

/* ⓹ filter VIEW: an dong, ⛔ khong doi du lieu */
document.getElementById('loc').addEventListener('input', e => {{
  const q = e.target.value.trim().toLowerCase();
  let hien = 0;
  for (const tr of luoi.tBodies[0].rows) {{
    const co = !q || tr.textContent.toLowerCase().includes(q);
    tr.style.display = co ? '' : 'none';
    if (co) hien++;
  }}
  tt.textContent = q ? ('hien ' + hien + ' dong') : 'chua sua gi';
  tt.className = '';
}});

chon(o_tai(0, 0));
</script>
"""


def _so_ke_toan(v) -> tuple[str, bool]:
    """⓻ So kieu ke toan: phan nhom nghin, am thi **do**. `None` -> rong."""
    if v is None or v == "":
        return "", False
    d = Decimal(str(v))
    am = d < 0
    return f"{d:,.2f}", am


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--ky", default=None, help="yyyy-mm; mac dinh ky DAY nhat")
    ap.add_argument("--dong", type=int, default=0, help="cat bot dong (0 = het ky)")
    ap.add_argument("--ra", default="hien_vat/mui_thu_luoi_F02.html")
    a = ap.parse_args()
    dsn = dsn_test() if a.test else dsn_that()

    import psycopg

    cot_canon = [c.letter for c in CANON_COLS]
    ten_canon = {c.letter: (c.name or "").strip() for c in CANON_COLS}
    # ⭐ MOT nguon duy nhat cho phep "chu cai canon nao la truong nao":
    # `ledger.classifying.VI_TRI_CLASSIFYING` — ⛔ khong khai lai o day.
    field_canon = {CANON_COLS[i].letter: f
                   for f, i in VI_TRI_CLASSIFYING.items()}
    cot = list(COT_HOP_DONG) + list(COT_NGOAI_THEM)
    # ⭐ Tap o go duoc = truong ghi co mat o 17 cot so + truong ghi lay tai
    # canon. ⛔ Truoc 28/08 chi tinh khoi dau ⇒ luoi chi cho go **5/10**.
    sua_keys = ([k for k in cot if k in TRUONG_GHI]
                + [f for k, f in ((c.letter, field_canon.get(c.letter))
                                  for c in CANON_COLS)
                   if f in TRUONG_GHI and f not in cot])
    with psycopg.connect(dsn, autocommit=True) as c:
        ky = a.ky
        if not ky:
            r = c.execute(
                "SELECT to_char(doc_date,'YYYY-MM'), count(*) FROM fls_itl"
                " WHERE doc_date IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 1"
            ).fetchone()
            if r is None:
                print("⛔ KHONG DAT — kho khong co dong nao co ngay ⇒ ⛔ khong "
                      "dung duoc mui thu tren du lieu that")
                return 1
            ky = r[0]
        sql = (f"SELECT {', '.join(cot)}, canon FROM fls_itl"
               " WHERE to_char(doc_date,'YYYY-MM') = %s ORDER BY itl_id")
        ts: list = [ky]
        if a.dong:
            sql += " LIMIT %s"
            ts.append(a.dong)
        hang = c.execute(sql, ts).fetchall()

    if not hang:
        print(f"⛔ KHONG DAT — ky {ky!r} khong co dong nao")
        return 1

    # ── dung bang
    dau = []
    for i, k in enumerate(cot):
        lop = "k0" if k in COT_DONG_CUNG else ""
        ten = TEN_CHO_NGUOI.get(k, k)
        dau.append(f'<th class="{lop}" data-cot="{k}" title="{html.escape(k)}">'
                   f'{html.escape(ten)}</th>')
    for k in cot_canon:
        f = field_canon.get(k)
        # ⭐ Cot canon nao LA mot truong ghi va ⛔ chua co mat o 17 cot so thi
        # o day chinh la cho go — dat `data-cot` bang TEN TRUONG de no vao
        # dung tap `SUA`, ⛔ khong de chu cai.
        khoa = f if (f in TRUONG_GHI and f not in cot) else f"canon.{k}"
        ten = ten_canon.get(k) or ""
        nhan = f"{ten} · {k}" if ten else f"(khuôn không đặt tên) · {k}"
        dau.append(f'<th data-cot="{khoa}" title="canon {k}">'
                   f'{html.escape(nhan)}</th>')

    than = []
    n_o = 0
    for r in hang:
        d = dict(zip(cot + ["canon"], r))
        cn = d.get("canon") or {}
        o = []
        for k in cot:
            v = d[k]
            lop = ["k0"] if k in COT_DONG_CUNG else []
            if k in TRUONG_GHI:
                lop.append("sua")
            if k in COT_TIEN:
                txt, am = _so_ke_toan(v)
                lop.append("tien")
                if am:
                    lop.append("am")
            else:
                txt = "" if v is None else str(v)
            o.append(f'<td class="{" ".join(lop)}" data-cot="{k}">'
                     f'{html.escape(txt)}</td>')
            n_o += 1
        for k in cot_canon:
            f = field_canon.get(k)
            if f in TRUONG_GHI and f not in cot:
                v = cn.get(k) if isinstance(cn, dict) else None
                o.append(f'<td class="sua" data-cot="{f}">'
                         f'{html.escape("" if v is None else str(v))}</td>')
                n_o += 1
                continue
            v = cn.get(k) if isinstance(cn, dict) else None
            o.append(f'<td data-cot="canon.{k}">'
                     f'{html.escape("" if v is None else str(v))}</td>')
            n_o += 1
        than.append("<tr>" + "".join(o) + "</tr>")

    # ⓺ ⭐ `BA-06` §6b goi **dong cung N cot trai** la cho YEU NHAT can thu
    # truoc. Ban dau toi de `left` la mot **uoc luong** be rong — va uoc luong
    # sai thi hai cot dong cung **de len nhau**, dung cai lo can thu.
    #
    # ★ Cach chua ⛔ khong phai doan ky hon, ma la **bo cho de sai**: KHAI
    # `width` cu the cho dung ba cot do, thi `left` la **tong dung** cua chung
    # **theo dinh nghia** — ⛔ khong con con so nao ai doan. 49 cot con lai giu
    # `table-layout: auto`, nen chi ba cot bi khai cung.
    css = []
    x = 0
    for k in COT_DONG_CUNG:
        w = RONG_DONG_CUNG[k]
        css.append(f'  th[data-cot="{k}"], td[data-cot="{k}"] '
                   f'{{ left:{x}px; width:{w}px; min-width:{w}px; '
                   f'max-width:{w}px; }}')
        x += w
    css.append(f'  th[data-cot="{COT_DONG_CUNG[-1]}"], '
               f'td[data-cot="{COT_DONG_CUNG[-1]}"] '
               f'{{ border-right:2px solid #8c959f; }}')
    css.append(f'  /* tong be rong khoi dong cung = {x}px (khai, ⛔ khong doan) */')

    trang = _HTML.format(
        n_dong=len(hang), n_cot=len(cot) + len(cot_canon),
        n_sua=len(sua_keys), ky=ky,
        dau="".join(dau), than="".join(than),
        sua_json=json.dumps(sua_keys))
    trang = trang.replace("</style>", "\n".join(css) + "\n</style>", 1)

    p = pathlib.Path(a.ra)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(trang, encoding="utf-8")
    kb = len(trang.encode()) / 1024

    print(f"kho: {dsn.rsplit('/', 1)[-1]}  ·  ky {ky}")
    print(f"da ghi {p}")
    print(f"  {len(hang):,} dong x {len(cot) + len(cot_canon)} cot = {n_o:,} o")
    print(f"  {kb:,.0f} KB mot tep, tu chua (⛔ khong mang, ⛔ khong thu vien)")
    print()
    print("★ TAM HANH VI — cai nao MAY tu khai duoc, cai nao PHAI nguoi ngoi go:")
    for s, t_ in (
        ("1 dieu huong ban phim", "MAY: Tab/Enter/mui ten co trong tep"),
        ("2 dan mot vung", "MAY: tach tab/newline roi rai tu o dang chon"),
        ("3 keo xuong", "MAY: Ctrl+D lay gia tri o ngay tren"),
        ("4 hoan tac", "MAY: Ctrl+Z, lich su tung buoc"),
        ("5 filter view", "MAY: an dong, ⛔ khong doi du lieu"),
        ("6 dong cung tieu de + cot khoa", "MAY: `left` la TONG DUNG be rong "
                                           "3 cot da KHAI (346px) — ⛔ khong doan"),
        ("7 so kieu ke toan", "MAY: tabular-nums + phan nhom nghin + am do"),
        ("8 luu khong can bam", "MAY: gom lo 2,5s, ⛔ khong co nut Luu"),
    ):
        print(f"   {s:34} {t_}")
    print()
    print("⛔ BA THU TEP NAY KHONG TU CHUNG MINH DUOC (khai ra, ⛔ khong de tu suy):")
    print("   · **cam giac** — 'co thua Sheets o dau' can LAN/THUONG go that")
    print("   · **thoi gian ve** — can mo tren may that, ⛔ khong do duoc tu day")
    print("   · **346px co du khong** — `left` la tong DUNG, nhung 3 cot khoa co")
    print("     du de khong mat phuong huong hay khong thi phai NGOI CUON moi biet")
    print()
    print("⛔⛔ TEP NAY MANG DU LIEU KE TOAN THAT — ke ca cot `memo` (Dien giai),")
    print("    cot CO THE mang ten nguoi. `hien_vat/` da bi chan khoi git; khi gui")
    print("    cho ai thi phai biet minh dang gui gi. ⛔ Dung dua len cho cong khai.")
    print(f"⇒ Mo tep: {p.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
