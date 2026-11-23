# -*- coding: utf-8 -*-
"""ap-status-check.py — checker §A.14 cho Architecture Pack HTML của FPA-T4.

Dùng:
  python docs/ap-status-check.py <AP.html>                 # kiểm; exit 1 nếu có failure
  python docs/ap-status-check.py <AP.html> --stamp s7-4=approved [--round R3]
  python docs/ap-status-check.py <AP.html> --rebuild-index  # sinh lại §0.B từ marker
  python docs/ap-status-check.py <AP.html> --restamp        # ghi lại hash theo hàm hiện tại, GIỮ data-st-on/inherited

Luật kiểm (đỏ khi):
  unmarked        heading h2–h4 không có data-st và không data-st-inherited
  stale-approval  mục approved/locked có hash nội dung hiện tại ≠ data-st-hash lúc ký
  locked-no-round mục locked không ghi data-st-round
  stale-index     §0.B không liệt kê đủ mục review / số đếm draft lệch marker
  bad-state       data-st ngoài 5 trạng thái
  tag-balance / fan-out>5 / dangling § / href treo
Hash = sha256 của thân mục (từ heading tới heading kế tiếp), bỏ comment HTML, gộp khoảng trắng, lấy 8 hex.
"""
from __future__ import annotations
import re, sys, hashlib, datetime, io
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
STATES = {"draft", "review", "approved", "locked", "superseded"}
HEAD = re.compile(r'<(h[234])\b([^>]*)>(.*?)</\1>', re.S)

def body_hash(body: str) -> str:
    b = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return hashlib.sha256(re.sub(r"\s+", " ", b).strip().encode()).hexdigest()[:8]

def attr(attrs: str, name: str):
    m = re.search(rf'\b{name}="([^"]*)"', attrs)
    return m.group(1) if m else None

def units(html: str):
    main_start = html.find("<main>")
    main_end = html.rfind("</main>")
    main = html[main_start:main_end]
    heads = list(HEAD.finditer(main))
    out = []
    for i, m in enumerate(heads):
        attrs = m.group(2)
        if "part-divider" in attrs:
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(main)
        body = main[m.end():end]
        title = re.sub(r"<[^>]+>", "", m.group(3)).strip()
        uid = attr(attrs, "id") or ""
        num = re.fullmatch(r"s([\dB-]+)", uid)
        out.append({"id": uid, "tag": m.group(1), "attrs": attrs, "title": title,
                    "st": attr(attrs, "data-st"), "inh": "data-st-inherited" in attrs,
                    "hash": attr(attrs, "data-st-hash"), "on": attr(attrs, "data-st-on"),
                    "round": attr(attrs, "data-st-round"), "live": body_hash(body),
                    "span": (main_start + m.start(), main_start + m.end()),
                    "num": (num.group(1).replace("-", ".") if num else None)})
    return out

def check(html: str):
    fails = []
    us = units(html)
    for u in us:
        if not u["st"] and not u["inh"]:
            fails.append(f"unmarked: {u['id']} {u['title'][:60]}")
        if u["st"] and u["st"] not in STATES:
            fails.append(f"bad-state: {u['id']} = {u['st']}")
        if u["st"] in ("approved", "locked") and not u["inh"] and u["hash"] != u["live"]:
            fails.append(f"stale-approval: {u['id']} stamped {u['hash']} live {u['live']} — chữ đổi dưới thanh xanh")
        if u["st"] == "locked" and not u["inh"] and not u["round"]:
            fails.append(f"locked-no-round: {u['id']}")
    # §0.B consistency
    ob = next((u for u in us if u["id"] == "s0-B"), None)
    if ob:
        i = [u["id"] for u in us].index("s0-B")
        end = us[i + 1]["span"][0] if i + 1 < len(us) else len(html)
        ob_body = html[ob["span"][1]:end]
        review_ids = [u["id"] for u in us if u["st"] == "review" and u["id"] != "s0-B"]
        for rid in review_ids:
            if f'href="#{rid}"' not in ob_body:
                fails.append(f"stale-index: §0.B thiếu mục review {rid}")
        cnt = Counter(u["st"] for u in us)
        for st, n in cnt.items():
            if not re.search(rf"<code>{st}</code>\s*{n}\b", ob_body):
                fails.append(f"stale-index: §0.B đếm {st} ≠ {n}")
    # structure
    nos = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    for tag in ["table", "tr", "td", "div", "details", "ul", "ol", "li", "h2", "h3", "h4"]:
        o = len(re.findall(rf"<{tag}\b[^>]*>", nos)); c = nos.count(f"</{tag}>")
        if o != c:
            fails.append(f"tag-balance {tag}: {o} vs {c}")
    parents = Counter(u["num"].rsplit(".", 1)[0] for u in us if u["num"] and "." in u["num"])
    for p, c in parents.items():
        if c > 5:
            fails.append(f"fan-out {p}: {c} > 5")
    valid = {u["num"] for u in us if u["num"]}
    pref = set()
    for v in valid:
        parts = v.split(".")
        for k in range(1, len(parts) + 1):
            pref.add(".".join(parts[:k]))
    body_only = re.sub(r"<pre.*?</pre>|<code>.*?</code>|<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    dangling = sorted(r for r in set(re.findall(r"(?<![A-Za-z])§(\d+(?:\.\d+)*)", body_only)) if r not in pref)
    if dangling:
        fails.append("dangling §: " + ", ".join(dangling[:20]))
    ids = set(re.findall(r'id="([^"]+)"', html)); hrefs = set(re.findall(r'href="#([^"]+)"', html))
    miss = sorted(hrefs - ids)
    if miss:
        fails.append("href treo: " + ", ".join(miss[:20]))
    return fails, us

def stamp(html: str, uid: str, state: str, rnd: str | None):
    if state not in STATES:
        raise SystemExit(f"state lạ: {state}")
    us = units(html)
    u = next((x for x in us if x["id"] == uid), None)
    if not u:
        raise SystemExit(f"không thấy id {uid}")
    s, e = u["span"]
    head = html[s:e]
    today = datetime.date.today().isoformat()
    head2 = re.sub(r'\bdata-st="[^"]*"', f'data-st="{state}"', head)
    head2 = re.sub(r'\s*data-st-inherited="1"', "", head2)
    head2 = re.sub(r'\bdata-st-hash="[^"]*"', f'data-st-hash="{u["live"]}"', head2)
    head2 = re.sub(r'\bdata-st-on="[^"]*"', f'data-st-on="{today}"', head2)
    head2 = re.sub(r'\s*data-st-round="[^"]*"', "", head2)
    if state == "locked":
        if not rnd:
            raise SystemExit("locked cần --round <tên vòng>")
        head2 = head2.replace(f'data-st-on="{today}"', f'data-st-on="{today}" data-st-round="{rnd}"')
    return html[:s] + head2 + html[e:]

def restamp(html: str):
    """Ghi lại hash theo hàm hiện tại; GIỮ data-st-on và inherited (re-hash không phải re-decision)."""
    us = units(html)
    out = html
    for u in reversed(us):
        s, e = u["span"]
        head = out[s:e]
        head2 = re.sub(r'\bdata-st-hash="[^"]*"', f'data-st-hash="{u["live"]}"', head)
        out = out[:s] + head2 + out[e:]
    return out

def rebuild_index(html: str):
    us = units(html)
    ob = next(u for u in us if u["id"] == "s0-B")
    i = [u["id"] for u in us].index("s0-B")
    end = us[i + 1]["span"][0] if i + 1 < len(us) else html.rfind("</main>")
    cnt = Counter(u["st"] for u in us)
    review = [u for u in us if u["st"] == "review" and u["id"] != "s0-B"]
    lines = [f'\n<p>Đếm trạng thái thoả thuận trên <b>{len(us)}</b> đơn vị (h2–h4): '
             + " · ".join(f'<code>{k}</code> {v}' for k, v in sorted(cnt.items())) + ".</p>",
             '<p>Bảng dưới liệt kê <b>chỉ</b> những mục đang <code>review</code>.</p>',
             '<table><thead><tr><th>Mục</th><th>Trạng thái</th></tr></thead><tbody>'
             + "".join(f'<tr><td><a href="#{u["id"]}">{u["title"]}</a></td><td><code>{u["st"]}</code></td></tr>' for u in review)
             + '</tbody></table>\n']
    return html[:ob["span"][1]] + "\n".join(lines) + html[end:]

def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    path = argv[1]
    html = open(path, encoding="utf-8").read()
    if "--stamp" in argv:
        spec = argv[argv.index("--stamp") + 1]
        uid, st = spec.split("=")
        rnd = argv[argv.index("--round") + 1] if "--round" in argv else None
        html = stamp(html, uid, st, rnd)
        html = rebuild_index(html)
        # §0.B thân đổi ⇒ hash của chính nó phải ghi lại (mục sinh tự động)
        html = restamp_one(html, "s0-B")
        open(path, "w", encoding="utf-8").write(html)
        print(f"stamped {uid} = {st}")
    elif "--rebuild-index" in argv:
        html = restamp_one(rebuild_index(html), "s0-B")
        open(path, "w", encoding="utf-8").write(html); print("index rebuilt")
    elif "--restamp" in argv:
        open(path, "w", encoding="utf-8").write(restamp(html)); print("restamped (dates preserved)")
    fails, us = check(open(path, encoding="utf-8").read())
    cnt = Counter(u["st"] for u in us)
    print(f"{len(us)} units · " + " · ".join(f"{k}={v}" for k, v in sorted(cnt.items())))
    for f in fails:
        print("FAIL", f)
    print(f"{len(fails)} failure(s)")
    return 1 if fails else 0

def restamp_one(html: str, uid: str):
    us = units(html)
    u = next(x for x in us if x["id"] == uid)
    s, e = u["span"]
    return html[:s] + re.sub(r'\bdata-st-hash="[^"]*"', f'data-st-hash="{u["live"]}"', html[s:e]) + html[e:]

if __name__ == "__main__":
    sys.exit(main(sys.argv))
