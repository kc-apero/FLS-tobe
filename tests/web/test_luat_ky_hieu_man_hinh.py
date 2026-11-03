"""⛔ Cong: LUAT KY HIEU tren man hinh — do bang may, ⛔ khong bang mat.

⛔⛔ **Vi sao cong nay ton tai.** Ke toan noi *"vung panel qua nhieu note, ky
hieu -> kho nhin"* (04/09). Do that tren `man_f02.js`: **235 ky hieu / 260 cau**
hien ra man hinh — gan **mot ky hieu moi cau**. Rieng dau `⛔` la **111 lan**,
va **73 (66%)** trong so do dung ngay truoc chu *"khong"/"chua"*.

⇒ Dau `⛔` sinh ra de noi *"nguy hiem, dung lai"*. Hai phan ba so lan no chi
dang dung truoc mot chu **phu dinh** — no da tut xuong thanh mot **tat chinh
ta**, ⛔ khong con la tin hieu. Mot tin hieu dung 111 lan tren mot man ⛔ khong
con la tin hieu.

⭐⭐ **Va day la cho quan trong: cat mot lan thi no se BO lai.** Nguoi sau *(ke
ca toi)* se viet `⛔ khong ...` vi ca ban tai lieu quanh day deu viet the — chu
thich, quyet dinh, ban khai. Mot luat ⛔ khong co may canh la mot luat se troi.
⇒ Luat nam o day.

⚠⚠ **Chu thich thi ⛔ KHONG bi cam.** Ky hieu trong chu thich la cho lap trinh
vien doc, no ⛔ khong lam roi mat ke toan — va bo chung di se lam mat cac dau
neo `⛔⛔`/`⭐` ma ca bo tai lieu dung de chi cho quan trong. Cong nay chi soi
**chuoi ngoai chu thich**.

⛔⛔ **Ban dau tien cua cong nay SAI, va no bao 102 vi pham.** No chi bo qua chu
thich **mot dong** (`//`), nen no bat ca nhung cau tieng Viet nam trong khoi
`/* ... */` — thu ⛔ khong bao gio hien ra man hinh. Suyt di "sua" chu thich de
lam xanh mot phep do sai. ⇒ Phep che chu thich nay ra
`tests/web/van_ban_man.py`, **mot ban**, va da duoc chung minh tren 6 ca *(gom
ca `//` nam trong chuoi va `"` nam trong khoi)*.

Nguon luat: `Design-F02-Panel` handoff, muc *"Bo luat ky hieu & mau"* —
`⛔ ⚠ ⭐ 🔒` **cat han** (toi da 0), `✓` giu lai.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from fls.web import phuc_vu as pv
from tests.web.van_ban_man import van_ban_hien_ra, van_ban_hien_ra_moi

TEP = Path(pv.THU_MUC)

# ⛔ Ky hieu bi CAT HAN khoi van ban hien ra man hinh.
CAM: str = "⛔⚠⭐\U0001f512"          # ⛔ ⚠ ⭐ 🔒

# ⭐ `✓` la ky hieu DUY NHAT con duoc dung trong chu chay.
CHO_PHEP: str = "✓"

# ⛔ Tep man hinh phai theo luat. Ban TRANG — them ten vao day la mien luat cho
#    mot tep, nen no phai la mot quyet dinh co nguoi ky.
THEO_LUAT: tuple[str, ...] = ("man_f02.js",)


def _van_ban(ten: str) -> list[str]:
    """Moi manh van ban HIEN RA man hinh — ⛔ da tru chu thich."""
    return van_ban_hien_ra((TEP / ten).read_text(encoding="utf-8"))


def _moi_chuoi_co_ky_hieu(ten: str) -> list[str]:
    """⭐ Moi chuoi **co ky hieu bi cam**, ⛔ ke ca khi ⛔ khong co chu Viet.

    ⛔⛔ **Lo trong chinh cong nay, bat duoc 04/09 khi doc lai ma.** `_van_ban`
    loc theo *"co dau tieng Viet"* — phep loc ay dung de bo qua ten lop CSS
    (`'crit'`, `'so-nhom-2'`). Nhung mot manh nhu `'⛔ '` thi **⛔ khong co chu
    Viet nao**, nen cong **⛔ khong thay** — trong khi no duoc noi chuoi thanh
    `'⛔ ' + v.chua + ' ô chưa gán'` va **hien nguyen ra man hinh**.

    ⇒ Bat ky chuoi nao mang mot trong bon ky hieu deu la van ban: ⛔ khong mot
    ten lop hay `id` nao chua `⛔ ⚠ ⭐ 🔒`.
    """
    return [t for t in van_ban_hien_ra_moi(
        (TEP / ten).read_text(encoding="utf-8"))
        if any(ch in CAM for ch in t)]


@pytest.mark.parametrize("ten", THEO_LUAT)
def test_khong_ky_hieu_bi_cam_trong_van_ban_hien_ra(ten: str) -> None:
    """⛔ 4 ky hieu bi cat han. Toi da **0** lan trong van ban hien ra."""
    xau: list[str] = []
    for t in _moi_chuoi_co_ky_hieu(ten):
        thay = sorted({ch for ch in t if ch in CAM})
        if thay:
            xau.append(f"{''.join(thay)}  ->  {t[:88]}")
    assert not xau, (
        f"{ten}: {len(xau)} chuoi hien ra man hinh con mang ky hieu bi cat "
        f"({' '.join(CAM)}).\n"
        f"⛔ Chung ⛔ khong duoc dung trong VAN BAN — chu thich thi duoc.\n"
        f"⇒ Viet lai cau cho no noi VIEC PHAI LAM, dung can dau.\n\n"
        + "\n".join(xau[:20]))


@pytest.mark.parametrize("ten", THEO_LUAT)
def test_dau_tich_dung_dung_cho_viec_da_xong(ten: str) -> None:
    """⭐ `✓` la ky hieu duy nhat con lai ⇒ no phai giu MOT nghia.

    ⛔⛔ Loi cu that: `'✓ dòng này ⛔ không còn việc'` — mot dau bao TIN TOT
    dung chung cau voi mot dau bao NGUY. Hai dau trong mot cau thi ⛔ khong dau
    nao con noi duoc gi.
    """
    xau = [t for t in _van_ban(ten)
           if CHO_PHEP in t and any(ch in CAM for ch in t)]
    assert not xau, (
        f"{ten}: {len(xau)} cau dung `✓` LAN mot ky hieu bi cat trong cung "
        f"mot cau:\n" + "\n".join(t[:88] for t in xau[:10]))


@pytest.mark.parametrize("ten", THEO_LUAT)
def test_cau_hien_ra_khong_dai_qua(ten: str) -> None:
    """⚠ Cau dai la cau giang bai. Nguong **160** ky tu cho mot manh chuoi.

    ⛔ Day ⛔ KHONG phai phep do do dai cau tieng Viet *(mot cau bi chia thanh
    nhieu manh boi phep noi chuoi)*. No do **mot manh**, va no chan dung cai
    da xay ra: nhung doan van ban ba bon dong lien mot ve mot ma noi bo.
    """
    dai = [t for t in _van_ban(ten) if len(t) > 160]
    assert not dai, (
        f"{ten}: {len(dai)} manh van ban dai hon 160 ky tu:\n"
        + "\n".join(f"[{len(t)}] {t[:100]}" for t in dai[:10]))
