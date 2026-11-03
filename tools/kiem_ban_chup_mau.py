"""⛔ CONG: ban chup mau trong bo asset thiet ke ⛔ khong duoc gia hon ban song.

⛔⛔ **Vi sao cong nay ton tai.** `Design-F02-Panel/tokens.SNAPSHOT.css` la mot
BAN SAO cua `fls/web/tep/tokens.css`. Ban sao ton tai co ly do that — bo asset
phai tu dung duoc khi dua cho mot phien thiet ke ⛔ khong co repo — nhung mot
ban sao ⛔ khong ai canh thi **gia di trong im lang**, va nguoi thiet ke se ve
tren mot bo mau ⛔ khong con dung.

⭐ Chinh tep SSOT da ghi dung bai hoc nay: truoc `B2` bo mau ton tai o **BA
cho**, va cau *"mau nhan la mau gi"* co ba cau tra loi dung.

⇒ Cong so **khoi `:root{...}` nguyen van**, ⛔ khong so ca tep *(banner cua ban
chup CO Y khac)*.

Chay:  python tools/kiem_ban_chup_mau.py
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SONG = GOC / "fls" / "web" / "tep" / "tokens.css"
CHUP = (GOC / "docs" / "ITL" / "02_BA" / "Artifacts" / "Design-F02-Panel"
        / "tokens.SNAPSHOT.css")

ROOT = re.compile(r":root\{.*?\n\}", re.S)


def _khoi(p: Path) -> str:
    if not p.exists():
        raise SystemExit(f"⛔ ⛔ khong thay tep: {p}")
    s = io.open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    m = ROOT.search(s)
    if not m:
        raise SystemExit(f"⛔ {p.name} ⛔ khong co khoi `:root{{...}}`")
    return m.group(0)


def main() -> int:
    a, b = _khoi(SONG), _khoi(CHUP)
    if a == b:
        n = len([l for l in a.split("\n") if "--" in l])
        print(f"⭐ CONG XANH — ban chup khop ban song ({n} bien)")
        return 0

    da = {l.strip() for l in a.split("\n") if l.strip().startswith("--")}
    db = {l.strip() for l in b.split("\n") if l.strip().startswith("--")}
    print("⛔ CONG DO — ban chup da GIA hon ban song")
    print(f"   song: {SONG}")
    print(f"   chup: {CHUP}")
    for x in sorted(da - db):
        print(f"   + chi co o BAN SONG : {x[:78]}")
    for x in sorted(db - da):
        print(f"   - chi co o BAN CHUP : {x[:78]}")
    if da == db:
        print("   ⚠ cung bo bien nhung khac cach trinh bay / chu thich")
    print("\n⇒ Sua o BAN SONG, roi CHUP LAI. ⛔ Dung sua ban chup.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
