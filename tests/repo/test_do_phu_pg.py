"""DO PHU hang cho — `B3`. ⛔ Dem trong KHO, ⛔ khong dem o man hinh.

⛔⛔ **Vi sao ham nay ra doi.** Truoc no, cach duy nhat lay so *"N dong phu 90
phan tram tien"* la keo `/queue?den_pct=90&limit=500` roi **dem so dong tra ve**
— va chan tren mot trang la **500** (`TRANG_TOI_DA`). Ngay nao hang cho dai ra
den muc phu 90 phan tram can hon 500 dong thi con so ay **im lang dung o 500**:
⛔ khong bao loi, ⛔ khong bao thieu, no chi **nho di**. Bai
`test_dem_o_man_hinh_BI_CHAN_TREN_con_dem_trong_kho_thi_khong` ghim dung cho do.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import doc_bao_cao as bc
from fls.repo.pham_vi import chi_nap_that

pytestmark = pytest.mark.pg


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture(scope="module")
def kho():
    """Mot lan nap that, **mot tien te rieng** de ⛔ khong dinh du lieu bai khac.

    Hinh so tien co chu y: **1 dong to** + **9 dong nho bang nhau** ⇒ moc 90
    phan tram roi dung o mot cho **dem duoc bang tay**, ⛔ khong phai mot con so
    'may bao sao thi tin vay'.
    """
    tt = "P" + _hex(5)
    run = f"NAP-2000-01-01-PHU{_hex()}"
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        ids = []
        for tien in [820] + [20] * 9:            # Σ = 1.000
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
                " source_row, run_id, contract_version, canon_version,"
                " mapping_version, raw_frozen, canon, curr, ps_co, work_status,"
                " doc_date, doc_no) VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0',"
                "'v1.0',false,'{}'::jsonb,%s,%s,'UNMAPPED','2026-08-01',%s)"
                " RETURNING itl_id",
                (uuid.uuid4().hex, run, tt, D(tien), f"CT{_hex(6)}"))
            ids.append(cur.fetchone()[0])
    return {"tt": tt, "run": run, "ids": ids}


def _cua_toi(hang, tt):
    return next((r for r in hang if r["curr"] == tt), None)


def _mo():
    return psycopg.connect(dsn_test(), autocommit=True)


# ── phep do co ban ────────────────────────────────────────────────────────
def test_dem_dung_so_dong_va_tong_tien(kho):
    with _mo() as c:
        r = _cua_toi(bc.do_phu_hang_cho(c, chi_nap_that()), kho["tt"])
    assert r is not None
    assert r["so_dong_cho"] == 10
    assert D(r["tien_cho"]) == D(1000)


def test_moc_90_dem_duoc_bang_tay(kho):
    """820 (82,0) · +20 (84,0) · 86 · 88 · **90,0** ⇒ dong thu **5** dat muc."""
    with _mo() as c:
        r = _cua_toi(bc.do_phu_hang_cho(c, chi_nap_that(), 90), kho["tt"])
    assert r["so_dong_phu"] == 5
    assert D(r["pct_that"]) == D("90.00")


def test_hai_cau_hoi_khac_nhau_deu_duoc_tra_ra(kho):
    """⭐⭐ *"Luy ke <= 90"* va *"du cham 90"* la HAI cau hoi.

    O moc 90 chung **trung nhau** (dong thu 5 dung 90,00). O moc 89 thi lech
    dung mot dong — va do la ly do ham nay tra ca hai con so thay vi bat man
    hinh doan.
    """
    with _mo() as c:
        r = _cua_toi(bc.do_phu_hang_cho(c, chi_nap_that(), 89), kho["tt"])
    assert r["so_dong_trong_danh_sach"] == 4      # luy ke <= 89  ⇒ 4 dong (88,0)
    assert r["so_dong_phu"] == 5                  # du cham 89    ⇒ 5 dong (90,0)
    assert D(r["pct_that"]) == D("90.00")


@pytest.mark.parametrize("muc,cho_doi", [
    (82, 1),      # dong to mot minh da 82,0
    (84, 2),
    (90, 5),
    (100, 10),    # ⛔ ca hang cho
    (99, 10),     # ⚠ 98,0 chua du ⇒ phai den dong cuoi
])
def test_moc_khac_nhau_deu_dem_duoc_bang_tay(kho, muc, cho_doi):
    with _mo() as c:
        r = _cua_toi(bc.do_phu_hang_cho(c, chi_nap_that(), muc), kho["tt"])
    assert r["so_dong_phu"] == cho_doi


# ── ⛔⛔ cai ly do ham nay ton tai ─────────────────────────────────────────
def test_dem_o_man_hinh_BI_CHAN_TREN_con_dem_trong_kho_thi_khong(kho):
    """⭐⭐ Ghim **dung** lop loi ma `B3` sinh ra de chua.

    Keo mot trang roi dem la mot phep dem **bi chan tren boi kich thuoc trang**.
    O day gia lap bang `limit=3`: phep dem cu tra **3** *(sai, va im lang)*,
    phep dem moi tra **5** *(dung)*.
    """
    pv = chi_nap_that()
    with _mo() as c:
        trang = bc.doc_hang_cho(c, pv, curr=kho["tt"], den_pct=90, limit=3)
        that = _cua_toi(bc.do_phu_hang_cho(c, pv, 90), kho["tt"])
    assert len(trang.dong) == 3          # ⛔ dem theo trang: **3** — SAI
    assert that["so_dong_phu"] == 5      # ⭐ dem trong kho: **5** — DUNG
    assert len(trang.dong) != that["so_dong_phu"], (
        "⛔ neu hai con so nay bang nhau thi bai kiem ⛔ khong chung minh duoc "
        "gi — phai chon `limit` NHO HON so dong phu that")


def test_khong_co_dong_TONG(kho):
    """⛔ Cong hai don vi tien te ra mot con so la vo nghia (`dem_hang_cho`)."""
    with _mo() as c:
        hang = bc.do_phu_hang_cho(c, chi_nap_that())
    assert all(r["curr"] for r in hang), "⛔ co mot dong ⛔ khong mang tien te"
    assert len({r["curr"] for r in hang}) == len(hang), "⛔ tien te bi trung"


def test_dong_da_bam_XONG_bi_tru_khoi_do_phu(kho):
    """⭐ Cung luat voi `dem_hang_cho`/`doc_hang_cho` (`QĐ-ITL-71`).

    ⛔⛔ Va no phai tru **TRUOC** khi tinh phan tram luy ke: tru o dau ra se de
    dong da xong **day phan tram cua moi dong con lai** — cung lop loi `CR#4`.
    """
    pv = chi_nap_that()
    to = kho["ids"][0]                       # dong 820 — mot minh no 82 phan tram
    with _mo() as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_queue_event (itl_id, evt_type, actor)"
                    " VALUES (%s,'done','bo-test@apero.vn')", (to,))
        r = _cua_toi(bc.do_phu_hang_cho(c, pv, 90), kho["tt"])
        # ⛔ Tra lai hien trang cho cac bai khac trong module.
        cur.execute("INSERT INTO fls_queue_event (itl_id, evt_type, actor,"
                    " reason) VALUES (%s,'reopen','bo-test@apero.vn','tra lai')",
                    (to,))
    assert r["so_dong_cho"] == 9
    assert D(r["tien_cho"]) == D(180)
    # 9 dong bang nhau: dong 8 moi 88,89 ⇒ phai den dong **9** moi cham 90.
    assert r["so_dong_phu"] == 9
    assert r["so_dong_trong_danh_sach"] == 8


# ── ⛔ muc_pct la thi NO, ⛔ khong am tham quay ve 90 ──────────────────────
@pytest.mark.parametrize("muc", [0, -1, 100.01, 150])
def test_muc_pct_ngoai_khoang_thi_NO(muc):
    with _mo() as c, pytest.raises(ValueError, match="muc_pct"):
        bc.do_phu_hang_cho(c, chi_nap_that(), muc)


def test_pham_vi_van_la_LAN_NAP_THAT(kho):
    """⛔ Ham moi ⛔ khong duoc la duong vong ra ngoai pham vi."""
    with _mo() as c:
        hang = bc.do_phu_hang_cho(c, chi_nap_that())
    assert _cua_toi(hang, kho["tt"]) is not None


def test_khong_co_tien_thi_KHONG_DO_DUOC_chu_khong_phai_0():
    """⭐⭐ Luat so mot cua du an, dat vao mot o cua bang.

    Σ tien = 0 ⇒ *"phu bao nhieu phan tram tien"* ⛔ khong co nghia. Tra `0` la
    noi *"xem 0 dong la du"* — mot cau **sai va nghe nhu tin tot**. Tra `NULL`
    de man hinh ve *"⛔ khong do duoc"*.
    """
    tt = "Z" + _hex(5)
    run = f"NAP-2000-01-01-ZERO{_hex()}"
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        for _ in range(3):
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
                " source_row, run_id, contract_version, canon_version,"
                " mapping_version, raw_frozen, canon, curr, ps_co, work_status,"
                " doc_date, doc_no) VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0',"
                "'v1.0',false,'{}'::jsonb,%s,0,'UNMAPPED','2026-08-01',%s)",
                (uuid.uuid4().hex, run, tt, f"CT{_hex(6)}"))
    with _mo() as c:
        r = _cua_toi(bc.do_phu_hang_cho(c, chi_nap_that()), tt)
    assert r["so_dong_cho"] == 3
    assert r["so_dong_phu"] is None, "⛔ phai la NULL = khong do duoc"
    assert r["so_dong_phu"] != 0, "⛔ 0 nghe nhu 'xem 0 dong la du'"
