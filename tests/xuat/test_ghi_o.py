"""`D3` — CO CHE GHI AN TOAN. Bon cong cua no, va **⛔ khong cong nao la
*"chay duoc"***.

Lo trinh `13` §1 chang ① khai cong ra cua `D3` bang dung bon cau:

    · ⛔ khong range tuyet doi
    · ghi hai lan ⇒ ⛔ khong nhan doi
    · bien ban neu **o dich that**
    · mot bai chung minh cu ghi ⛔ **khong chay** khi co duyet tat

⇒ Nen bo bai nay do **hau qua**, ⛔ khong do loi goi. Ham `ghi` la mot bo van
  chuyen GIA co **so ghi rieng**: moi bai doc so ay de tra loi cau *"co bao
  nhieu o thuc su bi cham"* — va **`0`** la cau tra loi ma ba trong bay bai
  o day doi.
"""
from __future__ import annotations

import pytest

from fls.xuat import ghi_o as g


def _bo_van_chuyen():
    """Bo van chuyen GIA + so ghi. ⛔ Khong mang, ⛔ khong Google."""
    so: list[tuple[str, str, str]] = []

    def ghi(tab, o, v):
        so.append((tab, o, v))
    return ghi, so


# ⭐ Luoi mau: hang tieu de o **hang 2** (⛔ khong hang 1) va du lieu tu hang 3
#   — cung hinh voi `[Master] ITL Ledge` that. Mot luoi mau co tieu de o hang 1
#   se lam moi phep doi 1-based/0-based **trong nhu dung** ke ca khi lech.
_LUOI = {
    "ITL Ledge": [
        ["ban nay la dong GHI CHU cua chu so — ⛔ khong phai tieu de"],
        ["ITL ID", "Ngay", "HĐ · Final", "CĐT1 · Final"],
        ["ITL-001", "2026-08-01", "HD-CU", ""],
        ["ITL-002", "2026-08-02", "", "CAC"],
        ["ITL-003", "2026-08-03", "HD-X", "MAC"],
        ["ITL-003", "2026-08-04", "HD-Y", "MAC"],      # ⛔ khoa TRUNG
    ],
}
_KHUNG = {"ITL Ledge": g.KhungTab("ITL Ledge", dong_tieu_de=2, dong_dau=3)}


def _neo(khoa, cot="HĐ · Final"):
    return g.Neo("ITL Ledge", "ITL ID", khoa, cot)


# ── ⓐ ⛔ KHONG dia chi tuyet doi: o dich duoc GIAI RA tu ban song ────────
def test_o_dich_GIAI_RA_tu_ban_song_chu_KHONG_go_tay():
    """⭐⭐ `ITL-002` nam o **hang 4** — va ⛔ khong ai go so `4` vao dau ca.

    ⛔⛔ Day la cong quan trong nhat cua `D3`. Chu so **dang cung mo tep**; mot
    cu chen dong lam moi dia chi duoi no dich mot dong, va mot cu ghi theo
    `A1` cung se **ghi dung, vao o SAI** — ⛔ khong bao loi.
    """
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [g.MotO(_neo("ITL-002"), "HD-MOI")])
    assert len(bb.se_ghi) == 1
    assert bb.se_ghi[0].o_a1 == "C4"


def test_CHEN_mot_dong_thi_o_dich_TU_DOI_theo():
    """⭐⭐⭐ Bai **chung minh** cau ⓐ: chen mot dong ⇒ o dich dich theo.

    ⛔ Neu module nay giu bat ky mot dia chi go tay nao thi bai nay do — va do
    la cach duy nhat de biet no **thuc su** neo theo khoa.
    """
    hang = list(_LUOI["ITL Ledge"])
    hang.insert(2, ["ITL-000", "2026-07-31", "HD-CHEN", ""])   # chen TRUOC
    bb = g.lap_bien_ban({"ITL Ledge": hang}, _KHUNG,
                        [g.MotO(_neo("ITL-002"), "HD-MOI")])
    assert bb.se_ghi[0].o_a1 == "C5", g.van_bien_ban(bb)


def test_chu_cot_dung_ca_o_moc_hai_ky_tu():
    assert [g.chu_cot(i) for i in (0, 25, 26, 27, 63)] == \
        ["A", "Z", "AA", "AB", "BL"]
    with pytest.raises(ValueError):
        g.chu_cot(-1)


# ── ⓑ ghi hai lan ⇒ ⛔ KHONG nhan doi ────────────────────────────────────
def test_ghi_HAI_LAN_thi_lan_hai_ghi_KHONG_O_NAO():
    """⭐⭐⭐ Va no do bang cach **doc lai ban song**, ⛔ khong bang mot cai the.

    ⛔⛔ Mot cai the trong kho *("toi da ghi o nay")* ⛔ **khong lam duoc viec
    nay**: the tra loi *"toi da ghi"*, con cau hoi that la *"o kia dang la
    gi"*. Neu chu so sua tay o do sau cu ghi thi cai the noi **da xong** trong
    khi o da khac han.
    """
    ghi, so = _bo_van_chuyen()
    ds = [g.MotO(_neo("ITL-002"), "HD-MOI")]

    bb1 = g.lap_bien_ban(_LUOI, _KHUNG, ds)
    kq1 = g.ap_dung(bb1, ghi, duyet=True)
    assert kq1["so_o_da_ghi"] == 1 and len(so) == 1

    # ⭐ Ban song sau cu ghi — dung cai bo van chuyen vua ghi vao
    hang = [list(r) for r in _LUOI["ITL Ledge"]]
    hang[3][2] = "HD-MOI"
    bb2 = g.lap_bien_ban({"ITL Ledge": hang}, _KHUNG, ds)
    assert bb2.tom() == {"tong": 1, "se_ghi": 0, "da_dung_roi": 1,
                         "tu_choi": 0}
    kq2 = g.ap_dung(bb2, ghi, duyet=True)
    assert kq2["so_o_da_ghi"] == 0
    assert len(so) == 1, "⛔ lan hai da cham vao ban song ⇒ NHAN DOI"


def test_O_TRONG_va_None_la_CUNG_mot_thu():
    """⚠ `''` va `None` deu la *"o trong"*. Neu ⛔ khong gop hai cai lai thi mot
    cu ghi `''` len mot o `None` se **luon** hien la `SE_GHI` ⇒ lan nao chay
    lai cung ghi lai, tuc **nhan doi mot cach khac**."""
    hang = [list(r) for r in _LUOI["ITL Ledge"]]
    hang[3][2] = None
    bb = g.lap_bien_ban({"ITL Ledge": hang}, _KHUNG,
                        [g.MotO(_neo("ITL-002"), "")])
    assert bb.tom()["da_dung_roi"] == 1


# ── ⓒ bien ban neu O DICH THAT, va moi TU CHOI co TEN ───────────────────
def test_bien_ban_neu_O_DICH_THAT_va_gia_tri_TRUOC_SAU():
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [g.MotO(_neo("ITL-001"), "HD-MOI")])
    v = g.van_bien_ban(bb)
    assert "ITL Ledge!C3" in v[0], v
    assert "'HD-CU'" in v[0] and "'HD-MOI'" in v[0], v
    assert "1 se ghi" in v[-1], v


@pytest.mark.parametrize("moto,ly_do", [
    (g.MotO(g.Neo("Tab La", "ITL ID", "ITL-001", "HĐ · Final"), "x"),
     "tab_khong_co"),
    (g.MotO(g.Neo("ITL Ledge", "Khoa La", "ITL-001", "HĐ · Final"), "x"),
     "cot_khoa_khong_co"),
    (g.MotO(g.Neo("ITL Ledge", "ITL ID", "ITL-001", "Cot La"), "x"),
     "cot_dich_khong_co"),
    (g.MotO(_neo("ITL-999"), "x"), "khoa_khong_co"),
    (g.MotO(_neo("ITL-003"), "x"), "khoa_TRUNG"),
])
def test_moi_hinh_TU_CHOI_co_TEN_va_co_CAU(moto, ly_do):
    """⛔ Nam hinh tu choi ⇒ **nam ten khac nhau**, moi ten mot cau tieng Viet.

    ⛔⛔ Gop chung thanh mot ly do *"⛔ khong giai ra o"* la bo di dung phan tin
    nguoi doc can: doi ten tab · doi ten cot · xoa dong · khoa trung la **bon
    duong sua khac nhau**.
    """
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [moto])
    assert bb.tom()["tu_choi"] == 1
    assert bb.tu_choi[0].ly_do == ly_do
    assert g.LY_DO_TU_CHOI[ly_do].strip()
    assert ly_do in g.van_bien_ban(bb)[0]


def test_khoa_TRUNG_thi_TU_CHOI_chu_KHONG_lay_dong_dau():
    """⭐⭐ `ITL-003` co **hai** dong. Lay dong dau la **may chon ho nguoi**.

    ⛔ Va do la loai sai ⛔ khong ai phat hien lai duoc: cu ghi thanh cong, o
    doi dung, chi la **dong sai** — va dong con lai giu gia tri cu, im lang.
    """
    ghi, so = _bo_van_chuyen()
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [g.MotO(_neo("ITL-003"), "HD-MOI")])
    assert bb.tu_choi[0].ly_do == "khoa_TRUNG"
    with pytest.raises(g.CoDongTuChoi):
        g.ap_dung(bb, ghi, duyet=True)
    assert so == []


def test_HAI_but_toan_mot_O_thi_CA_HAI_bi_tu_choi():
    """⛔⛔ **CA HAI**, ⛔ khong phai *"lay cai sau"*.

    Lay cai sau la mot phep chon ma ⛔ khong ai khai, va no dap len ket luan
    cua nguoi kia **trong im lang**.
    """
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [
        g.MotO(_neo("ITL-001"), "HD-A"),
        g.MotO(_neo("ITL-001"), "HD-B"),
    ])
    assert bb.tom() == {"tong": 2, "se_ghi": 0, "da_dung_roi": 0,
                        "tu_choi": 2}
    assert {d.ly_do for d in bb.tu_choi} == {"hai_but_toan_mot_O"}


# ── ⓓ co duyet TAT ⇒ cu ghi ⛔ KHONG CHAY ────────────────────────────────
def test_CO_DUYET_TAT_thi_KHONG_O_NAO_bi_cham():
    """⭐⭐⭐ Cong ra cua `D3` doi dung bai nay.

    ⛔ Va no do **so ghi cua bo van chuyen**, ⛔ khong do gia tri tra ve: mot
    ham co the nem loi **sau khi** da gui cu ghi dau tien, va luc do "bi chan"
    la mot cau **noi doi**.
    """
    ghi, so = _bo_van_chuyen()
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [g.MotO(_neo("ITL-001"), "HD-MOI"),
                                        g.MotO(_neo("ITL-002"), "HD-MOI")])
    assert len(bb.se_ghi) == 2
    with pytest.raises(g.ChuaDuyet):
        g.ap_dung(bb, ghi)                       # ⛔ thieu `duyet`
    with pytest.raises(g.ChuaDuyet):
        g.ap_dung(bb, ghi, duyet=False)
    assert so == [], "⛔ co duyet TAT ma van co o bi cham"


def test_duyet_phai_la_TRUE_chu_KHONG_phai_mot_gia_tri_DUNG_LA():
    """⛔ `duyet='co'` hay `duyet=1` **⛔ KHONG** duoc tinh la da duyet.

    ⚠ Mot chuoi khong rong la `truthy` trong Python. Neu kiem `if not duyet`
    thi mot loi go *(`duyet="false"`)* se **mo cong** — dung loai sai ma cai co
    nay dat ra de chan.
    """
    ghi, so = _bo_van_chuyen()
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [g.MotO(_neo("ITL-001"), "HD-MOI")])
    for xau in ("co", 1, "false", [1]):
        with pytest.raises(g.ChuaDuyet):
            g.ap_dung(bb, ghi, duyet=xau)
    assert so == []


def test_bien_ban_VAN_DOC_DUOC_khi_co_duyet_tat():
    """⭐ Chan cu GHI, ⛔ khong chan phep DOC bien ban — do la ca cong dung cua
    mot ban chay kho: doc truoc, duyet sau."""
    bb = g.lap_bien_ban(_LUOI, _KHUNG, [g.MotO(_neo("ITL-001"), "HD-MOI")])
    with pytest.raises(g.ChuaDuyet) as e:
        g.ap_dung(bb, lambda *a: None)
    assert "se_ghi" in str(e.value)
    assert len(g.van_bien_ban(bb)) == 2


# ── khung: hai he dem ────────────────────────────────────────────────────
def test_KhungTab_chan_hinh_VO_NGHIA():
    with pytest.raises(ValueError):
        g.KhungTab("x", dong_tieu_de=0)
    with pytest.raises(ValueError):
        g.KhungTab("x", dong_tieu_de=5, dong_dau=5)     # doc tieu de thanh du lieu


def test_Neo_RONG_bi_chan_ngay_luc_dung():
    """⛔ Mot neo rong ⛔ khong giai ra o nao — nen no NO **luc dung**, ⛔ khong
    doi den luc lap bien ban roi tra ve mot dong `TU_CHOI` mo ho."""
    for xau in ({"tab": ""}, {"cot_khoa": " "}, {"khoa": ""}, {"cot": ""}):
        tham = {"tab": "T", "cot_khoa": "K", "khoa": "1", "cot": "C"}
        tham.update(xau)
        with pytest.raises(ValueError):
            g.Neo(**tham)


# ── luat HAI KHOA ────────────────────────────────────────────────────────
@pytest.mark.parametrize("duyet,bien,mo", [
    (True, "1", True),
    (True, None, False),          # thieu khoa 2
    (False, "1", False),          # thieu khoa 1
    (False, None, False),
    (True, "0", False),
    (True, "", False),
    (True, "true", False),        # ⛔ chi chuoi `"1"`
    (1, "1", False),              # ⛔ `1` truthy ma ⛔ khong phai `True`
    ("co", "1", False),
])
def test_HAI_KHOA_chi_mo_khi_CA_HAI_mo(duyet, bien, mo):
    """⭐⭐ Luat quan trong nhat cua `D3` — va no o day de **do duoc**.

    ⛔⛔ Neu luat nay song trong `tools/ghi_o_that.py` thi no la mot luat
    ⛔ **khong bai nao do duoc**: cong cu ay chi chay khi co mang va co the
    Google. Mot cai co an toan ⛔ chua tung duoc thu la mot cai co ⛔ chua biet
    co hoat dong.
    """
    assert g.hai_khoa_mo(duyet, bien) is mo
