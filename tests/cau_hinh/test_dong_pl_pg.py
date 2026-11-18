# -*- coding: utf-8 -*-
"""`C12` — kho config `IX.PL`: dòng PL nạp chỉ-thêm *(di trú `0027` có sẵn — ⛔ di trú mới)*."""
from __future__ import annotations

import psycopg
import pytest

from fls.cau_hinh import dong_pl
from fls.db.kho import dsn_test
from fls.repo import cau_hinh_repo as chr

pytestmark = pytest.mark.pg


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _max(conn) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT coalesce(max(phien_ban),0) FROM fls_cau_hinh_ban "
                    "WHERE bang='IX.PL'")
        return int(cur.fetchone()[0])


def test_C12_nap_ix_pl_roi_doc_lai_dung_7_dong_dinh_nghia(conn):
    truoc = _max(conn)
    ban = chr.nap_ix_pl(conn, actor="test-c12")
    assert ban.phien_ban == truoc + 1 and len(ban.dong) == 7
    assert chr.doc_pl(conn) == dong_pl.DINH_NGHIA


def test_C12_nap_bieu_thuc_hong_bi_tu_choi_TRUOC_khi_ghi_khong_them_phien_ban(conn):
    chr.nap_ix_pl(conn, actor="test-c12")
    truoc = _max(conn)
    with pytest.raises(chr.LoiCauHinh) as e:
        chr.nap_ix_pl(conn, actor="test-c12",
                      dinh_nghia={"PL2": "__import__('os')"})
    assert "PL_CU_PHAP" in str(e.value)
    assert _max(conn) == truoc


def test_C12_ban_ma_la_trong_kho_nap_duoc_nhung_doc_pl_kiem_voi_cay_HD(conn):
    # nap_ix_pl kiểm CÚ PHÁP; mã lạ đối chiếu cây ở doc_pl khi có cây — ở đây chỉ ghim:
    # bản mã lạ ⇒ `nap_ix_pl` nhận `cay=` để kiểm trước khi ghi.
    from fls.cau_hinh import hd
    from pathlib import Path
    cay = hd.doc_van_ban(Path("tests/fixture/cau_hinh/atl_cay.json")
                         .read_text(encoding="utf-8"), nguon="atl")
    truoc = _max(conn)
    with pytest.raises(chr.LoiCauHinh) as e:
        chr.nap_ix_pl(conn, actor="test-c12", cay=cay, dinh_nghia={"PL2": "GI - NOPE"})
    assert "PL_MA_LA" in str(e.value) and _max(conn) == truoc
