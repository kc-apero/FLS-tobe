"""⭐ MOT cho tra loi cau: *"doan chu nay co HIEN RA man hinh khong?"*

⛔⛔ **Vi sao no phai la mot cho duy nhat.** Phep nay de trong nhu de: tim chuoi
trong nhay, xong. Nhung `man_f02.js` la mot tep **50% chu thich**, va chu thich
cua no chua **ca cau tieng Viet trong nhay kep**:

    ⓑ `#N/A` ⇒ hien **đúng `#N/A`**. No la mot CAU TRA LOI — *"dong nay
                    khong tra duoc `hd` trong danh mục"* — khong phai...

Doan tren nam trong mot khoi `/* ... */`. Neu phep tim chi bo qua chu thich
**mot dong** (`//`) thi no se bat cap `"` kia lam mot **chuoi**, va bao rang
man hinh dang hien mot cau ma man hinh ⛔ **chua bao gio hien**.

⚠⚠ Toi da vap dung cai nay khi viet cong luat ky hieu (04/09): cong dem **102**
chuoi vi pham, trong do co nhung doan **chi song trong chu thich**. Va mot kich
ban tu dong "don ky hieu" thi suyt **sua vao chu thich** — tuc la sua ho so de
lam xanh mot phep do sai.

⇒ Phep che chu thich nam o day, **mot ban**, cho ca cong lan moi cong cu khac.
"""
from __future__ import annotations

import re

# Chu Viet CO DAU. Day la phep loc *"day la van ban cho nguoi doc"*: mot chuoi
# nhu `'crit'` hay `'so-nhom-2'` thi ⛔ khong phai van ban.
DAU = re.compile(r"[À-ỹ]")

_CHUOI = re.compile(r"'(?:[^'\\\n]|\\.)*'" + r'|"(?:[^"\\\n]|\\.)*"'
                    + r"|`(?:[^`\\]|\\.)*`")
_DONG = re.compile(r"//[^\n]*")
_KHOI = re.compile(r"/\*.*?\*/", re.S)


def che_chu_thich(s: str) -> str:
    """Thay moi chu thich bang khoang trang **cung do dai**.

    ⭐ Giu do dai de moi vi tri trong ket qua van la vi tri **that** trong tep
    goc — nho vay mot cong cu sua chu co the ap thay doi theo VI TRI ma ⛔ khong
    lech mot ky tu nao.

    ⚠ Phai quet **mot luot** ba thu cung nhau *(chuoi · `//` · `/* */`)*: mot
    `//` nam **trong chuoi** thi ⛔ khong phai chu thich, va mot `"` nam **trong
    chu thich** thi ⛔ khong phai chuoi. Quet rieng tung loai la sai — do dung
    la loi vua vap.
    """
    ra: list[str] = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in "'\"`":
            m = _CHUOI.match(s, i)
            if m:
                ra.append(m.group(0))
                i = m.end()
                continue
            ra.append(c)
            i += 1
            continue
        if s.startswith("//", i):
            m = _DONG.match(s, i)
            assert m
            ra.append(" " * (m.end() - m.start()))
            i = m.end()
            continue
        if s.startswith("/*", i):
            m = _KHOI.match(s, i)
            if m:
                # ⭐ Giu dong moi: bo di thi so dong bao loi se lech.
                ra.append("".join(ch if ch == "\n" else " "
                                  for ch in m.group(0)))
                i = m.end()
                continue
        ra.append(c)
        i += 1
    return "".join(ra)


def van_ban_hien_ra(ma: str) -> list[str]:
    """Moi manh chuoi CO DAU tieng Viet **ngoai chu thich**."""
    return [t for t in van_ban_hien_ra_moi(ma) if DAU.search(t)]


def van_ban_hien_ra_moi(ma: str) -> list[str]:
    """MOI manh chuoi **ngoai chu thich** — ⛔ khong loc theo dau tieng Viet.

    ⭐ Dung cho phep do nao ⛔ khong duoc phu thuoc vao viec chuoi co chu Viet
    hay khong. Vi du: mot manh `'⛔ '` thi ⛔ khong co chu Viet nao, nhung no
    duoc noi chuoi thanh mot cau va **hien nguyen ra man hinh** — `van_ban_hien
    _ra` bo sot dung lop nay *(bat duoc 04/09)*.
    """
    return [m.group(0)[1:-1] for m in _CHUOI.finditer(che_chu_thich(ma))]
