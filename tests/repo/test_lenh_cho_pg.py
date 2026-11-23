"""`GAP-SCR-14` — HANG CHO PHIA LENH CHI. Chieu nguoc cua `doc_hang_cho`.

⛔⛔⛔ **Bo bai nay canh nam thu, va ⛔ khong thu nao la *"con so co dung
   khong"*:**

  ⓐ ⭐⭐ **Mot moi noi DA BO phai tra dong lenh VE hang cho.** Dem tren
    `fls_pm_link` *(bang goc, con giu ca moi noi da bo)* thay vi `fls_moi_noi`
    se **an vinh vien** mot dong lenh vua duoc go — ke toan bo ghep vi ghep
    sai, roi ⛔ khong bao gio thay lai no de ghep dung.
  ⓑ **⛔ Khong gop tien te.** `luy_ke_pct` phai tinh **trong tung** tien te.
    Gop lai thi 700 dong USD bi 590 dong VND dim xuong duoi.
  ⓒ ⭐⭐⭐ **Bac `ma` phai dung `canon_ref`, ⛔ khong mot cau `regexp` SQL.**
    Kho ⛔ **khong** co ban chuan hoa cua `doc_no`, nen mot cau tu dung la ban
    thu hai va no ⛔ khong tuong duong *(da do: `560` vs **`475`**)*.
  ⓓ **Phep CAT phai KHAI RA minh da cat** *(`INV-I16`)*. Bac `cung_tien_te`
    cua chieu nguoc co hang nghin dong; cat ma im thi nguoi go ket luan
    *"⛔ khong co dong tien nao khop"*.
  ⓔ **Do tren ANH HIEU LUC**, ⛔ khong cong ca hai anh.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import canon_ref
from fls.db.kho import dsn_test
from fls.repo import ghi_tay as gt
from fls.repo import lenh_cho as lc
from fls.repo.pham_vi import mot_lan_nap

pytestmark = pytest.mark.pg

ACTOR = "ke_toan@apero.vn"


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def c():
    with psycopg.connect(dsn_test(), autocommit=True) as conn:
        yield conn


@pytest.fixture()
def kho():
    """Mot lan nap RIENG cho moi bai — ⛔ khong dung `scope="module"`.

    ⚠ Bo bai `do_mau_so` dung `module` va no da cắn: mot bai KHAC trong cung
    tep them dong lenh vao kho chung, nen moi con so go tay thanh **phu thuoc
    thu tu chay**. O day moi bai co kho rieng ⇒ dem duoc.
    """
    tt = "L" + _hex(5)
    run = f"NAP-2000-02-01-LENHCHO{_hex()}"
    ma: dict[str, object] = {}
    with psycopg.connect(dsn_test(), autocommit=True) as conn, \
            conn.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))

        def _so(doc_no, tien, *, te=None, dong=None):
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system,"
                " source_sheet, source_row, run_id, contract_version,"
                " canon_version, mapping_version, raw_frozen, canon, curr,"
                " ps_co, work_status, doc_date, doc_no) VALUES (%s,'RAW','L1',"
                "%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,%s,%s,"
                "'UNMAPPED','2026-08-01',%s) RETURNING itl_id",
                (uuid.uuid4().hex, dong or abs(hash(doc_no or "")) % 90000,
                 run, te or tt, D(tien), doc_no))
            return cur.fetchone()[0]

        def _pm(ref, tien, *, status="Approve", te=None, dong=1, slip=None):
            pid = "PML" + _hex(10)
            cur.execute(
                "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                " ref_tho, ref_canon, amount, curr, status, source_row)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (run, pid, slip or ("SLIP" + _hex(6)), ref, canon_ref(ref),
                 D(tien), te or tt, status, dong))
            return pid

        # ⓐ mot cap KHOP HOAN TOAN — de bai "bo ghep tra ve hang cho" dung
        r1 = "REF-KHOP-" + _hex(4)
        ma["itl_khop"] = _so(r1, 1_000_000, dong=11)
        ma["pm_khop"] = _pm(r1, 1_000_000, dong=11)
        # ⓑ mot dong lenh ⛔ CHUA DUYET
        ma["pm_chua_duyet"] = _pm("REF-PEND-" + _hex(4), 500_000,
                                  status="Pending", dong=12)
        # ⓒ mot dong lenh o TIEN TE KHAC — de kiem "⛔ khong gop tien te"
        ma["te_khac"] = "X" + _hex(5)
        ma["pm_te_khac"] = _pm("REF-TE-" + _hex(4), 9_000_000,
                               te=ma["te_khac"], dong=13)
        # ⓓ HAI dong lenh cung MOT phieu ⇒ dem phieu phai DISTINCT
        slip = "SLIP" + _hex(6)
        ma["pm_cung_phieu"] = [
            _pm("REF-P1-" + _hex(4), 300_000, slip=slip, dong=14),
            _pm("REF-P2-" + _hex(4), 200_000, slip=slip, dong=15)]
        # ⓔ mot dong tien KHOA HOC — bac `ma` chi khop qua `canon_ref`
        ma["itl_kh"] = _so("4.36619E+15", 700, dong=16)
        ma["pm_kh"] = _pm("4366190000000000", 700, dong=17)
    return {"tt": tt, "run": run, "ma": ma}


def _pv(kho):
    return mot_lan_nap(kho["run"])


# ── ⓐ⭐⭐ MOI NOI DA BO phai tra dong lenh VE hang cho ──────────────────
def test_bo_ghep_tra_dong_lenh_VE_hang_cho(c, kho):
    """⭐⭐⭐ **Bai dat nhat cua tep nay.**

    Dem tren `fls_pm_link` *(bang GOC — no con giu ca moi noi DA BO,
    migration `0013`)* thay vi `fls_moi_noi` *(khung xem moi noi CON HIEU
    LUC)* se **an vinh vien** mot dong lenh vua duoc go: ke toan bo ghep vi
    ghep sai, roi ⛔ **khong bao gio thay lai no** de ghep dung.

    ⛔ Va no ⛔ khong bao loi gi ca — danh sach chi **thieu mot dong**.
    """
    pv = _pv(kho)
    pm, itl = kho["ma"]["pm_khop"], kho["ma"]["itl_khop"]

    co = [r["pm_line_id"] for r in lc.doc_lenh_cho(c, pv, limit=200).dong]
    assert pm in co, "dong lenh ⛔ chua ghep phai co trong hang cho"

    gt.ghep_lenh(c, pv, itl, [pm], actor=ACTOR,
                 reason="bai kiem ghep")
    sau = [r["pm_line_id"] for r in lc.doc_lenh_cho(c, pv, limit=200).dong]
    assert pm not in sau, "da ghep thi phai roi hang cho"

    gt.bo_moi_noi(c, pv, itl, actor=ACTOR,
                  reason="bai kiem bo ghep")
    lai = [r["pm_line_id"] for r in lc.doc_lenh_cho(c, pv, limit=200).dong]
    assert pm in lai, (
        "⛔⛔ BO GHEP roi ma dong lenh ⛔ KHONG quay lai hang cho — phep dem "
        "dang doc `fls_pm_link` (bang goc) thay vi `fls_moi_noi`")


# ── ⓑ ⛔ KHONG gop tien te ───────────────────────────────────────────────
def test_luy_ke_tinh_TRONG_TUNG_tien_te(c, kho):
    """⛔ Gop lai thi **700 dong USD** bi **590 dong VND** dim xuong duoi —
    mot khoan 300.000 USD xep sau mot khoan 400.000 dong."""
    pv = _pv(kho)
    dong = lc.doc_lenh_cho(c, pv, limit=200).dong
    theo_te: dict[str, list[dict]] = {}
    for r in dong:
        theo_te.setdefault(r["curr"], []).append(r)
    assert len(theo_te) >= 2, "kho bai phai co >= 2 tien te"
    for te, ds in theo_te.items():
        assert [r["hang"] for r in ds] == list(range(1, len(ds) + 1)), (
            f"⛔ `hang` cua tien te {te} ⛔ khong bat dau tu 1 — no dang duoc "
            f"xep TREN CA SO thay vi trong tung tien te")
        assert max(float(r["luy_ke_pct"]) for r in ds) == pytest.approx(100.0)


def test_dem_theo_tien_te__KHONG_co_dong_TONG(c, kho):
    pv = _pv(kho)
    ds = lc.dem_lenh_cho(c, pv)
    te = [r["curr"] for r in ds]
    assert te and all(str(t).lower() not in ("tong", "total", "all")
                      for t in te)
    # ⭐ Phieu dem DISTINCT: hai dong cung mot phieu van la MOT phieu
    o = next(r for r in ds if r["curr"] == kho["tt"])
    assert o["so_phieu"] < o["so_dong"], (
        "⛔ dem phieu ⛔ khong DISTINCT — kho bai co hai dong cung mot phieu")
    # ⭐ Hai loai viec tach doi, va Σ = tong
    assert o["so_dong_duyet"] + o["so_dong_chua_duyet"] == o["so_dong"]
    assert o["so_dong_chua_duyet"] >= 1


def test_muc_pct_ngoai_khoang_thi_NO(c, kho):
    for x in (0, -1, 101):
        with pytest.raises(ValueError):
            lc.dem_lenh_cho(c, _pv(kho), x)


# ── loc theo `status` ───────────────────────────────────────────────────
def test_MAC_DINH_hien_CA_HAI__khong_an_dong_chua_duyet(c, kho):
    """⛔⛔ An dong ⛔ chua duyet **theo mac dinh** la mot **mac dinh im lang**
    *(`INV-I16`)*: ke toan biet phieu ay ton tai, ⛔ khong thay no trong danh
    sach, va se ket luan **he mat du lieu**."""
    pv = _pv(kho)
    het = lc.doc_lenh_cho(c, pv, limit=200).dong
    assert any(not r["duyet"] for r in het), (
        "⛔ mac dinh dang AN dong ⛔ chua duyet")
    chi_duyet = lc.doc_lenh_cho(c, pv, chi_duyet=True, limit=200).dong
    assert chi_duyet and all(r["duyet"] for r in chi_duyet)
    chi_chua = lc.doc_lenh_cho(c, pv, chi_duyet=False, limit=200).dong
    assert chi_chua and all(not r["duyet"] for r in chi_chua)
    assert len(chi_duyet) + len(chi_chua) == len(het)


def test_status_RONG_KHONG_duoc_tinh_la_da_duyet(c, kho):
    """⛔ RONG la **KHONG BIET**, ⛔ khong phai *"da duyet"* — `INV-I16`."""
    pv = _pv(kho)
    with psycopg.connect(dsn_test(), autocommit=True) as cc:
        pid = "PML" + _hex(10)
        cc.execute(
            "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
            " ref_tho, ref_canon, amount, curr, status, source_row)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,'',99)",
            (kho["run"], pid, "SLIP" + _hex(6), "REF-RONG", "REFRONG",
             D(1), kho["tt"]))
    r = next(x for x in lc.doc_lenh_cho(c, pv, limit=200).dong
             if x["pm_line_id"] == pid)
    assert r["duyet"] is False


# ── ⓒ⭐⭐⭐ bac `ma` dung `canon_ref` ────────────────────────────────────
def test_bac_ma_dung_CANON_REF__khong_dung_regexp_SQL(c, kho):
    """⭐⭐⭐ Kho ⛔ **khong** co ban chuan hoa cua `doc_no`.

    `canon_ref('4.36619E+15')` -> `4366190000000000` ⇒ **KHOP**
    mot `regexp` tu dung        -> `436619E15`        ⇒ **TRUOT**
    """
    import re

    tho = "4.36619E+15"
    assert canon_ref(tho) == "4366190000000000"
    assert re.sub(r"[^A-Za-z0-9]", "", tho).upper() != canon_ref(tho)

    d = lc.ung_vien_itl(c, _pv(kho), str(kho["ma"]["pm_kh"]))
    bac = {r["itl_id"]: r["bac"] for r in d["ung_vien"]}
    assert bac.get(kho["ma"]["itl_kh"]) == "ma", (
        "⛔⛔ dong tien mang so chung tu dang KHOA HOC ⛔ khong vao bac `ma` — "
        "phep giao dang dung mot luat KHAC `canon_ref`")


def test_bac_ma_THANG_moi_bac_tien(c, kho):
    """⛔ Mot dong tien mang **dung** ma tham chieu thi no la ung vien manh
    nhat, **du so tien co lech**. Xep no sau mot dong chi *"gan tien"* la doi
    thu tu cua bang chung."""
    d = lc.ung_vien_itl(c, _pv(kho), str(kho["ma"]["pm_khop"]))
    assert d["ung_vien"], "phai co ung vien"
    assert d["ung_vien"][0]["bac"] == "ma"
    assert d["ung_vien"][0]["itl_id"] == kho["ma"]["itl_khop"]


def test_TEN_BAC_giu_y_nguyen_nhu_chieu_thuan(c):
    """⛔ Hai man hinh phai noi **cung mot tu** cho **cung mot y**."""
    from fls.repo.doc_bao_cao import BAC_UNG_VIEN
    assert lc.BAC_UNG_VIEN_ITL == BAC_UNG_VIEN


# ── ⓓ phep CAT phai KHAI RA ─────────────────────────────────────────────
def test_phep_CAT_phai_KHAI_RA__khong_cat_im_lang(c, kho):
    """⛔⛔ Cat ma im la mot **mac dinh im lang** *(`INV-I16`)*: nguoi go se
    tuong danh sach la **day du** va ket luan *"⛔ khong co dong tien nao
    khop"*."""
    pv = _pv(kho)
    d = lc.ung_vien_itl(c, pv, str(kho["ma"]["pm_khop"]), n=1)
    assert "bi_cat" in d and "tong_cung_tien_te" in d
    assert d["tong_cung_tien_te"] >= 1, (
        "⛔ `tong_cung_tien_te` phai la so THAT cua ca tap, ⛔ khong phai so "
        "dong da tra ve")
    assert len(d["ung_vien"]) <= 1


def test_canh_bao_status_di_KEM_dong_lenh(c, kho):
    d = lc.ung_vien_itl(c, _pv(kho), str(kho["ma"]["pm_chua_duyet"]))
    assert "Approve" in d["canh_bao"] or "Pending" in d["canh_bao"]


def test_dong_lenh_NGOAI_anh_thi_tra_NONE(c, kho):
    """⛔ Cung mot cau tra loi cho *"⛔ khong co"* va *"co ma ngoai pham vi"*."""
    assert lc.ung_vien_itl(c, _pv(kho), "PML-KHONG-CO-BAO-GIO") is None


# ── ⓔ do tren ANH HIEU LUC ──────────────────────────────────────────────
def test_do_tren_ANH_HIEU_LUC__khong_cong_ca_hai_anh(c, kho):
    """⛔ Mot anh thu hai lam hang cho **gap doi**, va no se noi rang con
    **nhieu viec hon** su thuc."""
    pv = _pv(kho)
    n1 = len(lc.doc_lenh_cho(c, pv, limit=500).dong)
    run2 = f"NAP-2000-02-02-LC2{_hex()}"
    try:
        with psycopg.connect(dsn_test(), autocommit=True) as cc, \
                cc.cursor() as cur:
            cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                        " canon_version, mapping_version)"
                        " VALUES (%s,'v1.0','v1.0','v1.0')", (run2,))
            cur.execute("SELECT ref_tho, amount, curr FROM fls_pm_line"
                        " WHERE run_id=%s", (kho["run"],))
            for i, (ref, tien, te) in enumerate(cur.fetchall()):
                cur.execute(
                    "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                    " ref_tho, ref_canon, amount, curr, status, source_row,"
                    " read_at) VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',%s,"
                    " '1999-01-01T00:00:00+00'::timestamptz)",
                    (run2, "PML" + _hex(10), "SLIP" + _hex(6), ref,
                     canon_ref(ref), tien, te, 900000 + i))
        n2 = len(lc.doc_lenh_cho(c, pv, limit=500).dong)
        assert n2 == n1, (
            f"⛔⛔ hang cho {n2} dong trong khi anh hieu luc chi cho {n1} — "
            f"dang CONG CA HAI ANH")
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as cc:
            cc.execute("DELETE FROM fls_pm_line WHERE run_id=%s", (run2,))
            cc.execute("DELETE FROM fls_run WHERE run_id=%s", (run2,))


def test_pham_vi_KHAC_lan_nap_tra_tap_RONG(c):
    t = lc.doc_lenh_cho(c, mot_lan_nap("NAP-1999-12-31-KHONGCO"))
    assert t.dong == []


def test_dung_sai_lay_tu_PHEP_CUA_CUA_GHI(c, kho):
    """⛔⛔ Mot ban dung sai rieng o day se **ve mot ung vien vao bac
    `gan_tien` roi cua GHI tu choi no** — mot cai bay."""
    from fls.adapters.pm_join import dung_sai_ghep_tay
    d = lc.ung_vien_itl(c, _pv(kho), str(kho["ma"]["pm_khop"]))
    assert d["dung_sai"] == dung_sai_ghep_tay({kho["tt"]}, D(1_000_000))


# ══ `G2` · CHIA BA RO (`BA-12 §2`) ═══════════════════════════════════════
def _ro_theo_pm(c, run: str, pv) -> dict[str, str]:
    t = lc.doc_lenh_cho(c, pv, limit=500)
    lc.xep_ro(t.dong, lc.chi_muc_ma(c, pv))
    return {d["pm_line_id"]: d["ro"] for d in t.dong}


def test_BAC_MA_tinh_bang_canon_ref_chu_KHONG_bang_so_sanh_THO(c, kho):
    """⛔⛔⛔ **Bai dat nhat cua `G2`, va no ghim mot loi TOI VUA MAC.**

    `fls_pm_line.ref_canon` **da chuan hoa** luc nap; `fls_itl.doc_no` thi
    **THO**. Ngay 11/09 toi do so ro bang mot cau SQL `i.doc_no = l.ref_canon`
    va duoc **121** dong ro `may`; goi `canon_ref` that cho **250** — **sai
    107%**, va sai cung chieu o ro `khong` *(514 → 768)*.

    ⚠ Do ⛔ khong phai lan dau: chu thich cua `_SQL_ITL_MA` da ghi mot con so
      khac cho **cung mot lop loi** *(560 vs 475, 09/09)*. Mot bai hoc nam
      trong chu thich ⛔ **khong** ngan duoc lan sau — **bai thu** thi co.

    ⇒ Bai nay dung mot cap ma **CHI khop sau khi chuan hoa**: dong tien mang
      `FT 2600-1234`, dong lenh mang `ft26001234`. So THO thi **khac nhau**;
      qua `canon_ref` thi **mot**.
    """
    run, pv = kho["run"], mot_lan_nap(kho["run"])
    with psycopg.connect(dsn_test(), autocommit=True) as cn, cn.cursor() as cur:
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, curr, ps_co, work_status,"
            " doc_date, doc_no) VALUES (%s,'RAW','L1',77771,%s,'v1.0','v1.0',"
            "'v1.0',false,'{}'::jsonb,%s,%s,'UNMAPPED','2026-08-01',%s)",
            (uuid.uuid4().hex, run, kho["tt"], D(777), "FT 2600-1234"))
        pid = "PMLCANON" + _hex(6)
        cur.execute(
            "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id, ref_tho,"
            " ref_canon, amount, curr, status, source_row)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',77771)",
            (run, pid, "SLIPC" + _hex(4), "ft26001234",
             canon_ref("ft26001234"), D(777), kho["tt"]))

    assert _ro_theo_pm(c, run, pv).get(pid) == lc.RO_MAY, (
        "⛔ cap nay CHI khop sau `canon_ref` — neu no roi vao ro `khong` thi "
        "phep chia dang so chuoi THO, dung cai loi da cho ra 121 thay vi 250")


def test_BA_RO_KHEP_ve_tong_khong_dong_nao_roi(c, kho):
    """⛔ Mot bang phan loai ⛔ khong cong ve tong la mot bang ⛔ khong kiem duoc."""
    pv = mot_lan_nap(kho["run"])
    d = lc.dem_theo_ro(c, pv)
    assert d[lc.RO_MAY] + d[lc.RO_NGUOI] + d[lc.RO_KHONG] == d["tong"]
    assert d["tong"] > 0, "⛔ do tren tap RONG la CHUA DO, ⛔ khong phai dat"


def test_RO_KHONG_luon_mang_cau_VI_SAO(c, kho):
    """⛔⛔ Mot ro *"⛔ khong bao gio"* ma ⛔ khong noi vi sao thi ke toan se
    **tim mai mai** — dung dieu man hinh truoc `G2` dang bat ho lam."""
    pv = mot_lan_nap(kho["run"])
    t = lc.doc_lenh_cho(c, pv, limit=500)
    lc.xep_ro(t.dong, lc.chi_muc_ma(c, pv))
    xau = [d for d in t.dong if d["ro"] != lc.RO_MAY and not d["vi_sao"]]
    assert not xau, f"⛔ {len(xau)} dong ⛔ khong co cau vi sao"


def test_TU_CHUNG_doi_KHOP_CA_TIEN_chu_khong_chi_khop_MA(c, kho):
    """⛔⛔ Nhom *"khop ma nhung LECH tien"* ⛔ KHONG duoc coi la tu chung.

    O do may **phai** hoi *"lenh nay an bao nhieu cua giao dich kia"*, va tra
    loi ho la de **may quyet thay nguoi** (`INV-I16`). Do 11/09: 250 dong ro
    `may` nhung chi **90** tu chung — gop lai la ghep sai **160** dong.
    """
    run, pv = kho["run"], mot_lan_nap(kho["run"])
    with psycopg.connect(dsn_test(), autocommit=True) as cn, cn.cursor() as cur:
        ma = "REFLECH" + _hex(5)
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, curr, ps_co, work_status,"
            " doc_date, doc_no) VALUES (%s,'RAW','L1',77772,%s,'v1.0','v1.0',"
            "'v1.0',false,'{}'::jsonb,%s,%s,'UNMAPPED','2026-08-01',%s)",
            (uuid.uuid4().hex, run, kho["tt"], D(1000), ma))
        pid = "PMLLECH" + _hex(6)
        cur.execute(
            "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id, ref_tho,"
            " ref_canon, amount, curr, status, source_row)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',77772)",
            (run, pid, "SLIPL" + _hex(4), ma, canon_ref(ma),
             D(400), kho["tt"]))          # ⛔ 400 != 1000

    t = lc.doc_lenh_cho(c, pv, limit=500)
    lc.xep_ro(t.dong, lc.chi_muc_ma(c, pv))
    d = next(x for x in t.dong if x["pm_line_id"] == pid)
    assert d["ro"] == lc.RO_MAY, "khop ma ⇒ van thuoc ro `may`"
    assert d["tu_chung"] is False, (
        "⛔ tien lech 400 vs 1000 ma van bao TU CHUNG — mot cu ghep lo se "
        "ghep sai so tien, im lang")


def test_LOC_THEO_RO_tra_dung_tap_va_KHONG_bo_sot(c, kho):
    """⛔ Ba ro loc rieng phai **cong lai** bang tong — ⛔ khong dong nao roi
    giua hai bo loc, va ⛔ khong dong nao dem hai lan."""
    pv = mot_lan_nap(kho["run"])
    d = lc.dem_theo_ro(c, pv)
    tong = 0
    for ro in (lc.RO_MAY, lc.RO_NGUOI, lc.RO_KHONG):
        t = lc.doc_lenh_cho_theo_ro(c, pv, ro, limit=500)
        assert all(x["ro"] == ro for x in t.dong), f"⛔ ro {ro} lan sang ro khac"
        assert len(t.dong) == d[ro], (ro, len(t.dong), d[ro])
        tong += len(t.dong)
    assert tong == d["tong"]


def test_RO_LA_thi_NO_chu_KHONG_tra_danh_sach_RONG(c, kho):
    """⛔⛔ Tra rong cho mot ro ⛔ khong ton tai la noi *"⛔ khong co dong nao"*
    — mot cau **sai**. Nguoi doc se ket luan da xong viec."""
    with pytest.raises(ValueError):
        lc.doc_lenh_cho_theo_ro(c, mot_lan_nap(kho["run"]), "ro_bia_dat")


def test_TU_CHUNG_loc_HEP_HON_ro_may(c, kho):
    """`tu_chung=True` phai la **tap con** cua ro `may`, ⛔ khong phai mot tap
    khac."""
    pv = mot_lan_nap(kho["run"])
    may = {d["pm_line_id"] for d in
           lc.doc_lenh_cho_theo_ro(c, pv, lc.RO_MAY, limit=500).dong}
    tc = {d["pm_line_id"] for d in
          lc.doc_lenh_cho_theo_ro(c, pv, lc.RO_MAY, tu_chung=True,
                                  limit=500).dong}
    assert tc <= may and len(tc) == lc.dem_theo_ro(c, pv)["tu_chung"]
