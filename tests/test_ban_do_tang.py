# -*- coding: utf-8 -*-
"""Phep thu cho `tools/sinh_ban_do_tang.py` — ban do KIEN TRUC 7 tang.

⛔⛔ **Cai dang thu ⛔ khong phai "ban do dep" — la "ban do ⛔ KHONG GIA duoc".**

`ERD-CONTRACT.mmd` sinh tu `schema.py` va co `G-ERD-1` canh nen no ⛔ khong
gia. Ban do tang phai co **cung tinh chat ay**, neu khong thi no la mot to
giay dep treo canh mot bo ma dang chay — va no se gia **im lang**.
"""
from __future__ import annotations

from fls.db import schema
from tools import sinh_ban_do_tang as B


def test_MOI_bang_deu_khai_TANG():
    """⭐⭐ Them mot bang ma quen khai tang ⇒ no **VO HINH** tren ban do kien
    truc, va ⛔ khong ai thay no bien mat. Bai nay la cho dieu do no ra."""
    bang = B.doc_bang()
    assert bang, "⛔ ⛔ khong doc duoc bang nao — phep trich da hong"
    thieu = sorted(b.name for b in bang if not b.tang)
    assert not thieu, f"⛔ {len(thieu)} bang ⛔ khong khai `tang`: {thieu}"


def test_moi_TANG_khai_deu_co_THAT_trong_schema():
    """⛔ Mot tang khai trong `TANG` ma ⛔ khong bang nao thuoc ve no la mot
    o TRONG tren ban ve — no noi ve mot thu ⛔ khong ton tai."""
    co = {b.tang for b in B.doc_bang()}
    khai = {ma for ma, _, _ in B.TANG}
    assert not (co - khai), f"⛔ tang co that ma ⛔ khong khai: {sorted(co - khai)}"
    assert not (khai - co), f"⛔ tang khai ma RONG: {sorted(khai - co)}"


def test_BA_ban_ve_KHOP_ban_khai():
    """⭐ Day la cong that, dat trong bo test de mot cu `pytest` cung bat."""
    assert B.main.__module__  # giu import song
    ve = B.sinh()
    assert B.MMD.exists() and B.MMD.read_text(encoding="utf-8") == ve, \
        "⛔ `ERD-TANG.mmd` lech ban khai — chay `python tools/sinh_ban_do_tang.py`"
    trang = B.sinh_html(B.doc_bang())
    assert B.HTM.exists() and B.HTM.read_text(encoding="utf-8") == trang, \
        "⛔ trang HTML lech ban khai — chay lai cong cu"
    assert "```mermaid\nflowchart" in B.DOC.read_text(encoding="utf-8"), \
        "⛔ `BA-05` mat khoi `flowchart`"


def test_NO_khi_mot_bang_MOI_chua_khai_tang():
    """⛔ Cong ra that: bang moi ⛔ chua khai tang ⇒ `sinh()` phai **NO**,
    ⛔ khong duoc lang le bo qua no."""
    import pytest
    from fls.db.model import Column as C
    from fls.db.model import Table
    goc = B.doc_bang
    B.doc_bang = lambda: goc() + [                   # type: ignore[assignment]
        Table(name="fls_bang_moi", columns=(C("x", "int"),))]
    try:
        with pytest.raises(SystemExit) as e:
            B.sinh()
        assert "fls_bang_moi" in str(e.value)
    finally:
        B.doc_bang = goc                             # type: ignore[assignment]


def test_NO_khi_phep_trich_RONG__xanh_tren_tap_rong_la_CHUA_DO():
    """⛔⛔⛔ Neu `schema.py` doi cach khai thi `doc_bang()` tra **rong** — va
    mot ban ve rong ma bao "xanh" la mot ban ve **NOI DOI**."""
    import pytest
    goc = B.doc_bang
    B.doc_bang = lambda: []                          # type: ignore[assignment]
    try:
        with pytest.raises(SystemExit):
            B.sinh()
    finally:
        B.doc_bang = goc                             # type: ignore[assignment]


def test_MUI_TEN_la_khoa_ngoai_THAT_chu_khong_go_tay():
    """⛔ Mot mui ten ⛔ khong ung voi mot `FK` that la mot **loi bia** — no
    ve ra mot quan he kho ⛔ khong he cuong che."""
    bang = B.doc_bang()
    ten = {b.name for b in bang}
    cn = B.canh(bang)
    assert cn, "⛔ ⛔ khong doc duoc khoa ngoai nao"
    for tu, den, cot in cn:
        assert tu in ten and den in ten
        b = next(x for x in bang if x.name == tu)
        c = next(x for x in b.columns if x.name == cot)
        assert c.fk and c.fk.split(".")[0] == den, \
            f"⛔ mui ten {tu}->{den} ⛔ khong ung voi FK nao"


def test_TU_THAM_CHIEU_cua_but_toan_DAO_phai_duoc_VE():
    """⛔⛔⛔ **Ghim dung mot quan he toi da AM THAM nuot mat.**

    `canh()` ban dau loc `den != b.name` *"cho ban ve gon"* — va no xoa mat
    quan he **quan trong nhat** cua ca kho:

        fls_adjustment.reversal_of  →  fls_adjustment.adj_id

    Mot but toan **DAO** tro ve but toan no dao. Do la co che thay cho
    `DELETE`: `INV-I08` noi so **chi THEM**, nen *"xoa"* trong TO-BE la
    *"them mot dong tro nguoc lai"*. ⛔ Loc no di la ve ra mot cai kho trong
    do **⛔ khong the dao duoc gi** — mot ban ve **noi sai ve he thong**.

    ⇒ Mot phep loc viet cho *"gon mat"* co the la mot phep loc **xoa mat su
      that**, va no ⛔ khong bao gio tu bao.
    """
    cn = B.canh(B.doc_bang())
    assert ("fls_adjustment", "fls_adjustment", "reversal_of") in cn, \
        "⛔ quan he DAO but toan ⛔ khong con tren ban do"
    assert "fls_adjustment -->|reversal_of| fls_adjustment" in B.sinh()
    # ⛔ Va no phai doc duoc thanh CAU tren trang, ⛔ khong chi la mot mui ten
    assert "tự tham chiếu" in B.sinh_html(B.doc_bang())


def test_MOI_khoa_ngoai_khai_deu_len_ban_do__KHONG_cai_nao_bi_loc():
    """⭐ Canh **ca lop** loi tren: so mui ten phai **bang** so `fk` khai."""
    bang = B.doc_bang()
    ten = {b.name for b in bang}
    khai = [(b.name, c.name) for b in bang for c in b.columns
            if c.fk and c.fk.split(".")[0] in ten]
    # ⚠ Con so nay la mot GHIM co y: them mot `fk` thi phai sua o day, va do
    #   la cho de tuyen bo *"toi biet minh vua them mot khoa"*.
    #   23 -> 24 ngay 2026-09-18 (migration `0024`, `CR#12`):
    #   `fls_pm_link.run_pm -> fls_run.run_id`.
    assert len(B.canh(bang)) == len(khai) == 24, \
        f"⛔ {len(khai)} khoá khai mà chỉ vẽ {len(B.canh(bang))}"


def test_SVG_hop_le_va_moi_FK_co_MOT_mui_ten():
    """⛔ Mot `<svg>` hong thi trinh duyet ve ra **mot khoang trang** — ⛔ khong
    bao loi. ⇒ Phai phan tich duoc, va so mui ten phai bang so `fk`."""
    import xml.etree.ElementTree as ET
    ve = B.sinh_svg(B.doc_bang())
    ET.fromstring(ve)                      # NO neu SVG ⛔ khong hop le
    # ⚠ Ghim co y — xem chu thich o `test_MOI_khoa_ngoai...`. 23 -> 24 ngay
    #   2026-09-18 (migration `0024`): `fls_pm_link.run_pm`.
    assert ve.count("marker-end") == len(B.canh(B.doc_bang())) == 24


def test_HINH_HOC_khong_TRAN_khung_va_khong_CHONG_nhau():
    """⭐⭐ **Bai nay thay cho doi mat toi.**

    Toi ⛔ khong nhin duoc ban ve minh sinh ra. Mot o de len o khac, hay tran
    ra ngoai khung, thi trinh duyet **van ve** — va ⛔ khong ai biet cho den
    luc co nguoi mo tep. ⇒ Do bang so.
    """
    o, dai, cao = B._bo_tri(B.doc_bang())
    assert o and dai and cao > 0
    for n, (x, y, w, h, _) in o.items():
        assert x >= B._LE_NHAN + 17, f"⛔ {n} đè lên nhãn tầng"
        assert x + w <= B._RONG - 10, f"⛔ {n} tràn khung phải"
        assert y + h <= cao, f"⛔ {n} tràn khung dưới"
    it = list(o.items())
    for i, (n1, (x1, y1, w1, h1, _)) in enumerate(it):
        for n2, (x2, y2, w2, h2, _) in it[i + 1:]:
            assert not (x1 < x2 + w2 and x2 < x1 + w1
                        and y1 < y2 + h2 and y2 < y1 + h1), \
                f"⛔ {n1} và {n2} CHỒNG nhau"
    for a, b in zip(dai, dai[1:]):
        assert a[3] + a[4] <= b[3], f"⛔ dải {a[0]} chồng dải {b[0]}"


def test_BO_TRI_tat_dinh__hai_lan_sinh_ra_HAI_TEP_GIONG_HET():
    """⛔ Bo tri phai **tinh duoc**, ⛔ khong duoc ngau nhien — neu khong thi
    cong `--kiem` se bao lech mot cach **vo nghia** va nguoi ta se tat no."""
    assert B.sinh_svg(B.doc_bang()) == B.sinh_svg(B.doc_bang())


def test_SVG_TU_CHUA__khong_CDN_khong_JS():
    """⛔ Owner mo trang nay bang cach **nhap doi mot tep**. Mot ban do kien
    truc ⛔ khong duoc phu thuoc vao duong truyen."""
    ve = B.sinh_svg(B.doc_bang())
    for xau in ("<script", "onload", "<foreignObject", "<image", "@import"):
        assert xau not in ve, f"⛔ SVG mang {xau!r} — ⛔ khong con tu chua"
    # ⚠ `xmlns="http://www.w3.org/2000/svg"` la **khai khong gian ten**, ⛔ KHONG
    #   phai mot lan tai mang — trinh duyet ⛔ khong he goi dia chi ay. Bai thu
    #   ban dau cua toi bat ca no, va do la mot phep do **qua tho**.
    #   ⇒ Chi cam dia chi nam trong thuoc *tai ve*: `href` / `src` / `url()`.
    import re
    goi = re.findall(r'(?:href|src)\s*=\s*"[^"]*"|url\(\s*[\'"]?https?:', ve)
    assert not goi, f"⛔ SVG tai tai nguyen ngoai: {goi[:3]}"


def test_VIEW_ve_KHAC_bang():
    """⛔ `fls_moi_noi` / `fls_sua_tay` / `fls_queue_state` la **khung xem** —
    chung ⛔ khong luu gi. Ve giong bang la noi rang kho co mot ban sao."""
    ve = B.sinh()
    for v in ("fls_moi_noi", "fls_sua_tay", "fls_queue_state"):
        assert f'{v}["{v}<br><i>khung xem</i>"]:::view' in ve, v
    assert "classDef view" in ve


def test_THU_TU_tang_tren_ban_ve_dung_thu_tu_khai():
    """⭐ Thu tu bay tang la **mot ket luan** *(anh → nap → so → ghep → viec)*,
    ⛔ khong phai sap xep chu cai. Doi thu tu la doi cach doc ca he."""
    ve = B.sinh()
    vt = [ve.index(f'subgraph {ma.replace("-", "_")}[') for ma, _, _ in B.TANG
          if any(b.tang == ma for b in B.doc_bang())]
    assert vt == sorted(vt), "⛔ thu tu tang tren ban ve ⛔ khong theo `TANG`"


def test_DONG_DAU_schema_py_noi_dung_so_bang_no_dang_khai():
    """⛔⛔⛔ **Ghim mot CAU GIA nam ngay tren SSOT cua ca kho.**

    Dong dau `fls/db/schema.py` ghi *"Khai bao **10 bang + 2 view**"* trong
    khi no dang khai **18 bang + 5 view** — sai suot nhieu thang, va ⛔ khong
    mot cong nao doc no vi cong chi canh **SO DO DUOC**, ⛔ khong canh **CAU**.

    ⇒ Bai nay bat hai con so ay phai **do duoc**, y nhu moi con so khac.
    """
    bang = B.doc_bang()
    n_view = sum(1 for b in bang if getattr(b, "kind", "table") == "view")
    n_bang = len(bang) - n_view
    dong_dau = (schema.__doc__ or "").splitlines()[0]
    assert f"{n_bang} bang" in dong_dau, \
        f"⛔ dong dau noi khac so bang THAT ({n_bang}): {dong_dau!r}"
    assert f"{n_view} view" in dong_dau, \
        f"⛔ dong dau noi khac so view THAT ({n_view}): {dong_dau!r}"


def test_schema_van_khai_du_25_bang():
    """⛔ Chot con so de mot lan xoa nham bang lo ra ngay."""
    bang = B.doc_bang()
    # ⭐ `23` → `24`: them khung xem `fls_may_goi_y` (migration `0025`,
    #   `QĐ-ITL-143`) — **toi biet minh vua them mot thuc the**
    # ⭐ `24` → `25`: them khung xem `fls_dien_giai` (migration `0026`,
    #   `QĐ-ITL-145`) — **toi biet minh vua them mot thuc the**
    assert len(bang) == 25
    assert sum(1 for b in bang if getattr(b, "kind", "table") == "view") == 7
    assert schema.SEQUENCES  # bo khai van song


def test_TANG_5_chi_co_MOT_bang_that__ba_cai_kia_la_KHUNG_XEM():
    """⭐⭐⭐ **Bai nay ghim mot su that lam RE han mot quyet dinh dang cho.**

    Ngay 14/09 toi noi voi owner rang duong **Ⓐ** *(cho dong LENH mang duoc
    trang thai cong viec)* ton *"**2 migration**"*, vi toi tuong
    `fls_queue_event` va `fls_da_xong` la **hai bang**.

    ⛔ Sai. `fls_da_xong` · `fls_queue_state` · `fls_queue_reason_weekly` deu
    la **KHUNG XEM doc tu `fls_queue_event`**. ⇒ Ca tang ⑤ dung tren **MOT**
    bang that. Duong Ⓐ thuc ra la: **1 cot moi** + **sinh lai 3 khung xem**.

    ⇒ Bai nay giu cho ket luan ay dung. Neu mot ngay `fls_da_xong` thanh mot
      BANG THAT thi phep tinh gia ay **doi**, va bai nay do ngay.
    """
    bang = {b.name: b for b in B.doc_bang()}
    that = [n for n, b in bang.items()
            if b.tang == "5-viec" and getattr(b, "kind", "table") != "view"]
    assert that == ["fls_queue_event"], \
        f"⛔ tang ⑤ nay co nhieu hon MOT bang that: {that}"
    for v in ("fls_da_xong", "fls_queue_state", "fls_queue_reason_weekly"):
        assert "fls_queue_event" in bang[v].view_sql, \
            f"⛔ {v} ⛔ khong con doc tu `fls_queue_event`"
