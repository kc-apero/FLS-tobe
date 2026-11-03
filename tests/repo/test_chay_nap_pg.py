"""Cong cua lan nap THAT: bon duong phai can, va chay lai khong nhan doi."""
from __future__ import annotations

import os
import uuid

import psycopg
import pytest

from fls.db.kho import dsn_test

from fls.canon.row import SO_VI_TRI
from fls.canon.spec import pos_of
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import KetQuaNap, chay, danh_seq_trung

pytestmark = pytest.mark.pg

# ⛔ Kho TEST, KHONG phai kho that. `dsn_test()` NO neu no tro vao kho
# that — xem `fls/db/kho.py`: bo test tung ghi 1.204 dong vao `fls_itl`.
DSN = dsn_test()


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _nc(run: str) -> NgucCanh:
    return NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "Transaction Mapping L1")


def _hang(**kw):
    o = [None] * SO_VI_TRI
    o[0], o[3], o[4], o[5], o[6] = 46000, "VND", 0, 1000, "R | test"
    o[1] = kw.pop("ct", "CT-" + uuid.uuid4().hex[:8])
    for lt, v in kw.items():
        o[pos_of(lt)] = v
    return o


def test_bon_duong_can_va_ket_qua_noi_ro_tung_duong(conn):
    lo = "T-" + uuid.uuid4().hex[:8]
    tho = [_hang(),                       # -> vao so
           _hang(C="#REF!"),              # -> fls_reject (cot goc la o loi)
           [None] * SO_VI_TRI,            # -> dong trong
           _hang(S="OGA | GAC - Other")]  # -> vao so, co hd
    kq = chay(conn, tho, _nc(lo))
    assert kq.can(), kq.bao()
    assert (kq.vao, kq.vao_so, kq.loai, kq.rong, kq.bo_qua_trung) == (4, 2, 1, 1, 0)
    assert kq.ok + kq.unmapped == kq.vao_so


def test_CHAY_LAI_KHONG_NHAN_DOI__va_noi_ro_da_bo_qua(conn):
    """★ Cong chung #4. `content_key` UNIQUE nen lan hai NO neu khong co duong
    bo qua; ma bo qua trong im lang thi khong ai biet so co tang hay khong.
    """
    lo = "T-" + uuid.uuid4().hex[:8]
    tho = [_hang(ct=lo + "-a"), _hang(ct=lo + "-b")]
    a = chay(conn, tho, _nc(lo))
    b = chay(conn, tho, _nc(lo))
    assert (a.vao_so, a.bo_qua_trung) == (2, 0)
    assert (b.vao_so, b.bo_qua_trung) == (0, 2)
    assert b.can() and b.unmapped == 0 and b.ok == 0

    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl WHERE run_id = %s", (lo,))
        assert cur.fetchone()[0] == 2, "chay lai da NHAN DOI so"


def test_dong_TRUNG_NOI_DUNG_deu_vao_so_nho_seq_trung(conn):
    """So that co 281 dong trung noi dung + 103 dong khong co so chung tu.
    Khong danh `seq_trung` thi ca nhom dung MOT khoa ⇒ mat du lieu trong im lang.

    ⚠ Ba dong phai giong het NHAU nhung khac moi lan CHAY. `content_key` co chu y
    KHONG chua `run_id` (do la co che de lan nap sau nhan ra dong da co trong so),
    nen neu de tien co dinh thi phep thu nay xanh khi chay rieng va DO khi chay
    ca bo — da xay ra that.
    """
    lo = "T-" + uuid.uuid4().hex[:8]
    tien = 1000 + int(uuid.uuid4().hex[:6], 16)          # khac moi lan chay
    tho = [_hang(ct="", F=tien) for _ in range(3)]        # y het nhau trong lo nay
    kq = chay(conn, tho, _nc(lo))
    assert (kq.vao_so, kq.bo_qua_trung) == (3, 0), kq.bao()


def test_content_key_KHONG_chua_run_id__nen_nap_lai_o_run_KHAC_van_nhan_ra(conn):
    """★ Tinh chat de hieu nham nhat cua `content_key`, nen khoa lai tuong minh.

    Cung noi dung, HAI run khac nhau ⇒ lan hai KHONG vao so. Do la dung: neu
    khoa chua `run_id` thi moi lan chay lai pipeline se nhan doi ca so ma khong
    cong nao do — va so tien se tang gap doi trong im lang.
    """
    tien = 1000 + int(uuid.uuid4().hex[:6], 16)
    tho = [_hang(ct="X-" + uuid.uuid4().hex[:6], F=tien)]
    a = chay(conn, tho, _nc("T-" + uuid.uuid4().hex[:8]))
    b = chay(conn, tho, _nc("T-" + uuid.uuid4().hex[:8]))   # RUN KHAC
    assert (a.vao_so, a.bo_qua_trung) == (1, 0)
    assert (b.vao_so, b.bo_qua_trung) == (0, 1), b.bao()


def test_seq_trung_on_dinh_theo_thu_tu_doc():
    nc = _nc("x")
    from fls.canon.row import CanonRow
    h = [(5, CanonRow.from_list(_hang(ct="A"))),
         (6, CanonRow.from_list(_hang(ct="A"))),
         (7, CanonRow.from_list(_hang(ct="B")))]
    assert danh_seq_trung(h, nc) == [0, 1, 0]
    assert danh_seq_trung(h, nc) == [0, 1, 0]        # chay lai y het


def test_dong_bi_loai_vao_fls_reject_voi_LY_DO_CO_TEN(conn):
    lo = "T-" + uuid.uuid4().hex[:8]
    chay(conn, [_hang(AG="#N/A")], _nc(lo))
    with conn.cursor() as cur:
        cur.execute("SELECT source_row, reason FROM fls_reject WHERE run_id = %s", (lo,))
        r = cur.fetchall()
    assert len(r) == 1
    assert r[0][0] == 5 and "AG" in r[0][1] and "#N/A" in r[0][1]


def test_khong_can_thi_KHONG_GHI_GI(conn):
    """⛔ Mot lan nap lech ma van commit thi tu do khong ai biet so thieu bao nhieu."""
    lo = "T-" + uuid.uuid4().hex[:8]
    kq = KetQuaNap(lo, vao=10, vao_so=5, loai=1, rong=1, bo_qua_trung=0,
                   unmapped=0, ok=5)
    assert not kq.can()
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_run WHERE run_id = %s", (lo,))
        assert cur.fetchone()[0] == 0


def test_chay_LAI_khong_nhan_doi_dong_bi_loai_trong_fls_reject(conn):
    """★ Lo do duoc 2026-08-26: bon lan chay `nap_that.py` de lai **76 dong**
    trong `fls_reject` cho **19 dong bi loai** that.

    Con so "bao nhieu dong bi loai" la con so nguoi ta doc de biet nguon co bao
    nhieu lo. Nhan bon lan thi no vo nghia — va vo nghia trong IM LANG.
    """
    lo = "T-" + uuid.uuid4().hex[:8]
    tien = 1000 + int(uuid.uuid4().hex[:6], 16)
    tho = [_hang(F=tien, AG="#N/A"), _hang(F=tien + 1, C="#REF!")]
    for _ in range(3):
        chay(conn, tho, _nc(lo))
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_reject WHERE run_id = %s", (lo,))
        assert cur.fetchone()[0] == 2, "fls_reject bi nhan ban moi lan chay lai"


def test_KHONG_co_duong_XOA_fls_reject(conn):
    """⛔ Mot ham don duoc `fls_reject` la mot ham co the xoa bang chung.
    Chan trung bang DIEU KIEN, khong bang xoa.
    """
    import pathlib

    import fls.repo.chay_nap as m
    t = pathlib.Path(m.__file__).read_text(encoding="utf-8").upper()
    assert "DELETE FROM FLS_REJECT" not in t
    assert "DELETE FROM FLS_ITL" not in t
    assert "UPDATE FLS_ITL" not in t


def test_chay_LAI_khong_XOA_MAT_row_count_cua_lan_chay_that(conn):
    """★ `fls_run.row_count` dem TU BANG. Ban dau no lay `len(da_vao)`, nen lan
    chay thu hai (bo qua het) ghi `row_count = 0` trong khi so co 9.973 dong.
    """
    lo = "T-" + uuid.uuid4().hex[:8]
    tien = 1000 + int(uuid.uuid4().hex[:6], 16)
    tho = [_hang(F=tien), _hang(F=tien + 1)]
    chay(conn, tho, _nc(lo))
    chay(conn, tho, _nc(lo))                     # lan hai: bo qua het
    with conn.cursor() as cur:
        cur.execute("SELECT row_count, state FROM fls_run WHERE run_id = %s", (lo,))
        assert cur.fetchone() == (2, "mapped")
