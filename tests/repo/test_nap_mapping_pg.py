"""Cong GHI `Mapping Master` vao kho — danh muc SOI GUONG, ⛔ khong phai so.

★★ Bai quan trong nhat o day ⛔ khong phai *"nap duoc"* ma la **nap RONG thi
KHONG duoc nap**. Mot luot doc that bai *(mang chap, quyen bi thu, tab doi ten)*
cung tra ve mot danh sach rong — va neu bo nap cu the ma xoa thi **mot su co
mang bien thanh mot lan xoa sach danh muc**, sau do moi phep suy phan bo lang le
tra `#N/A`. ⛔ Khong co loi nao, ⛔ khong ai biet.

★ Va mot bai nua ma `UPSERT` ⛔ khong bao gio dat: mot ma **da bi xoa khoi
sheet** phai **mat khoi kho**. `UPSERT` se de no song mai va tiep tuc tra ve mot
quyet dinh phan bo ma ke toan ⛔ khong con thay o dau.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.adapters.mapping_master import DongMM
from fls.db.kho import dsn_test
from fls.repo.nap_mapping import KHOA_NGUON, nap_mapping_master, tra_mapping

pytestmark = pytest.mark.pg


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c
        # ⚠ Don sach: bang nay la danh muc dung chung, ⛔ khong theo `run_id`,
        # nen mot bai de lai rac se lam bai khac do vi mot ly do ⛔ khong lien
        # quan — dung loai "do gia" kho nhat de truy.
        c.execute("DELETE FROM fls_mapping_master")


def _ba_dong() -> list[DongMM]:
    return [
        DongMM(7, "GI | Gross Inflow", need_cfa2="Need to Allocate to CFA2",
               method_cfa2="GI Ledger"),
        DongMM(8, "OPC | Operating Cost"),
        DongMM(9, "MC | Maketer Cost", code_hr="MC"),
    ]


def test_nap_roi_TRA_duoc_theo_hd(conn):
    kq = nap_mapping_master(conn, _ba_dong())
    assert (kq.da_chen, kq.bi_loai) == (3, 0)
    d = tra_mapping(conn, "GI | Gross Inflow")
    assert d["need_cfa2"] == "Need to Allocate to CFA2"
    assert d["method_cfa2"] == "GI Ledger"
    # ⛔ O rong phai ve `None`, ⛔ khong phai chuoi rong (bay `VLOOKUP`).
    assert tra_mapping(conn, "OPC | Operating Cost")["method_cfa2"] is None


def test_tra_KHONG_phan_biet_hoa_thuong__dung_nhu_VLOOKUP(conn):
    """⛔ Sheets so chuoi khong phan biet hoa thuong. So phan biet o day thi may
    cho `#N/A` o nhung dong ma sheet that tra duoc gia tri."""
    nap_mapping_master(conn, _ba_dong())
    assert tra_mapping(conn, "gi | gross inflow") is not None
    assert tra_mapping(conn, "  GI | Gross Inflow  ") is not None


def test_hd_KHONG_co_thi_tra_None__va_allocate_cho_NA(conn):
    from fls.ledger.allocate import KHONG_TRA_DUOC, suy_allocate
    nap_mapping_master(conn, _ba_dong())
    assert tra_mapping(conn, "KHONG-CO-MA-NAY") is None
    v = suy_allocate("SHQ2 | HQ2", "KHONG-CO-MA-NAY",
                     tra_mapping(conn, "KHONG-CO-MA-NAY"))
    assert v.cfa2 == KHONG_TRA_DUOC and v.khong_tra_duoc is True


def test_hd_RONG_hay_None_thi_tra_None__khong_no(conn):
    nap_mapping_master(conn, _ba_dong())
    for x in (None, "", "   "):
        assert tra_mapping(conn, x) is None


# ─────────────────────────────────────── hai bay chinh
def test_nap_RONG_thi_NO__khong_xoa_sach_danh_muc(conn):
    """⛔⛔ Bai nang nhat cua file nay."""
    nap_mapping_master(conn, _ba_dong())
    with pytest.raises(ValueError, match="RONG"):
        nap_mapping_master(conn, [])
    assert conn.execute("select count(*) from fls_mapping_master"
                        ).fetchone()[0] == 3, (
        "⛔⛔ mot luot doc that bai vua xoa sach danh muc phan bo")


def test_ma_BI_XOA_khoi_sheet_thi_MAT_khoi_kho__khong_song_mai(conn):
    """⛔ `UPSERT` ⛔ khong bao gio dat bai nay."""
    nap_mapping_master(conn, _ba_dong())
    assert tra_mapping(conn, "MC | Maketer Cost") is not None

    kq = nap_mapping_master(conn, _ba_dong()[:2])    # sheet bo dong thu ba
    assert (kq.da_xoa, kq.da_chen) == (3, 2)
    assert tra_mapping(conn, "MC | Maketer Cost") is None, (
        "⛔ ma da bi xoa khoi sheet van song trong kho va van tra ve mot quyet "
        "dinh phan bo — dung loai lech im lang nhat")


def test_nap_lai_KHONG_nhan_ban__va_de_lai_VET_o_fls_source(conn):
    nap_mapping_master(conn, _ba_dong())
    nap_mapping_master(conn, _ba_dong())
    assert conn.execute("select count(*) from fls_mapping_master"
                        ).fetchone()[0] == 3
    r = conn.execute(
        "select src_type, txn_count, last_seen_at from fls_source"
        " where source_key=%s", (KHOA_NGUON,)).fetchone()
    assert r is not None, "nap mot danh muc ma ⛔ khong de lai vet nao"
    assert (r[0], r[1]) == ("Mapping", 3) and r[2] is not None


def test_KHONG_ghi_but_toan_hay_nhat_ky(conn):
    """⛔ Nap mot DANH MUC ⛔ khong phai thao tac cua nguoi tren mot dong so —
    no ⛔ khong duoc lam phong so nhat ky."""
    t = conn.execute("select (select count(*) from fls_adjustment),"
                     " (select count(*) from fls_journal)").fetchone()
    nap_mapping_master(conn, _ba_dong())
    assert conn.execute("select (select count(*) from fls_adjustment),"
                        " (select count(*) from fls_journal)").fetchone() == t
