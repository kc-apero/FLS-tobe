"""⛔ Cong: vung PHAN BO 🔒 di ra cua DOC — va **ba ca** deu dung.

⛔⛔ **Vi sao bai nay ton tai.** Ngay `03/09` toi viet trong `man_f02.js` rang
vung phan bo *"⛔ khong cua nao mang no"* va cho man hien mot khoi **xin loi**.
Cau ay **chua duoc do**: luat `suy_allocate` da co tu truoc, va
`fls_mapping_master` da co **73 ma** nam trong kho — thieu duy nhat **mot phep
gan** o tang doc. ⇒ Mot cau *"⛔ khong lam duoc"* ma ⛔ khong ai do la mot cau
**tu chan minh**.

★ Ba ca cua `fls/ledger/allocate.py`, va ca thu ba la mot **bay da do duoc**:
  ⓐ tra duoc + danh muc noi **CO** can phan bo ⇒ `cfa2` = chuoi co
  ⓑ tra duoc + danh muc noi **KHONG** ⇒ `cfa2` roi ve `cfa1` *(= `cdt1`)*
  ⓒ ⛔ **khong tra duoc** `hd` ⇒ **`#N/A`** o ca hai o — mot **cau tra loi**,
    ⛔ khong phai mot loi, va ⛔ khong phai rong *(`INV-I16`)*
  ⓓ o `Method` **rong THAT** ⇒ `VLOOKUP` cua Sheets cho **`0`** ⇒ so that hien
    dung chu `0`. ⛔ Chua cho dep o day la lam may noi khac so.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test, noi_chi_doc
from fls.ledger.allocate import CO_CAN_PHAN_BO, KHONG_TRA_DUOC
from fls.repo import doc_bao_cao as bc
from fls.repo.pham_vi import PhamVi

pytestmark = pytest.mark.pg


def _chen(cur, run, *, curr, hd, cdt1):
    cur.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version,"
        " mapping_version, raw_frozen, canon, doc_no, curr, ps_co,"
        " work_status, doc_date, hd, cdt1)"
        " VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0','v1.0',false,'[]'::jsonb,"
        "'FT-AL',%s,%s,'UNMAPPED','2026-08-01',%s,%s) RETURNING itl_id",
        (uuid.uuid4().hex, run, curr, D("1000.00"), hd, cdt1))
    return cur.fetchone()[0]


@pytest.fixture()
def du_lieu():
    """Bon dong, bon ca — tren **danh muc THAT** cua kho test."""
    ma = "ZZTHU" + uuid.uuid4().hex[:4].upper()
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        tt = "A" + uuid.uuid4().hex[:5].upper()
        run = f"NAP-2000-01-01-AL{uuid.uuid4().hex[:6].upper()}"
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        # ⭐ Ba dong danh muc RIENG cho bai nay — ⛔ khong dung ma that, de bai
        #   ⛔ khong vo khi ke toan sua danh muc.
        for hd_code, need, method in (
                (ma + "-CO", CO_CAN_PHAN_BO, "Theo doanh thu"),
                (ma + "-KHONG", "No need", ""),
                (ma + "-RONG", "No need", None)):
            cur.execute(
                "INSERT INTO fls_mapping_master (hd_code, need_cfa2,"
                " method_cfa2) VALUES (%s,%s,%s)", (hd_code, need, method))
        d = {
            "co": _chen(cur, run, curr=tt, hd=ma + "-CO", cdt1="SHQ2 | HQ2"),
            "khong": _chen(cur, run, curr=tt, hd=ma + "-KHONG",
                           cdt1="SHQ2 | HQ2"),
            "rong": _chen(cur, run, curr=tt, hd=ma + "-RONG",
                          cdt1="SHQ2 | HQ2"),
            "la": _chen(cur, run, curr=tt, hd=ma + "-KHONG-CO-TRONG-DANH-MUC",
                        cdt1="SHQ2 | HQ2"),
        }
    d["run"] = run
    d["ma"] = ma
    yield d
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("DELETE FROM fls_mapping_master WHERE hd_code LIKE %s",
                    (ma + "%",))


def _theo_id(du_lieu):
    with noi_chi_doc(dsn_test()) as conn:
        t = bc.doc_so(conn, PhamVi("mot_lan_nap", run_id=du_lieu["run"]),
                      limit=500)
    return {d["itl_id"]: d for d in t.dong}


def test_ca_a_danh_muc_noi_CO_can_phan_bo(du_lieu):
    d = _theo_id(du_lieu)[du_lieu["co"]]
    assert d["alloc_cfa2"] == CO_CAN_PHAN_BO
    assert d["alloc_can_phan_bo"] is True
    assert d["alloc_method"] == "Theo doanh thu"
    assert d["alloc_na"] is False
    assert d["alloc_cfa1"] == "SHQ2 | HQ2"


def test_ca_b_danh_muc_noi_KHONG_thi_cfa2_ROI_VE_cfa1(du_lieu):
    """⛔ ⛔ Khong de rong: cong thuc **roi ve `AU`** *(= `cdt1`)*, va mot o
    rong o day se lam nguoi doc tuong dong nay chua ai gan."""
    d = _theo_id(du_lieu)[du_lieu["khong"]]
    assert d["alloc_cfa2"] == d["alloc_cfa1"] == "SHQ2 | HQ2"
    assert d["alloc_can_phan_bo"] is False
    assert d["alloc_method"] == "No need"


def test_ca_c_KHONG_tra_duoc_thi_hien_dung_N_A_o_CA_HAI_o(du_lieu):
    """⭐⭐ `#N/A` la mot **CAU TRA LOI**, ⛔ khong phai mot loi.

    Va no ⛔ **khong phai rong**: *"tra duoc va no rong"* voi *"⛔ khong tra
    duoc"* la hai chuyen khac nhau (`INV-I16`). So that cung dang hien `#N/A`.
    """
    d = _theo_id(du_lieu)[du_lieu["la"]]
    assert d["alloc_na"] is True
    assert d["alloc_cfa2"] == KHONG_TRA_DUOC
    assert d["alloc_method"] == KHONG_TRA_DUOC
    # ⛔ `cfa1` VAN co gia tri — no ⛔ khong phu thuoc danh muc.
    assert d["alloc_cfa1"] == "SHQ2 | HQ2"


def test_ca_d_o_Method_RONG_THAT_thi_hien_dung_chu_0(du_lieu):
    """⚠⚠ **Bay `VLOOKUP`**: o `Mapping Master!L` rong that ⇒ Sheets tra `0`,
    va `0 <> ""` la **DUNG** ⇒ o `Method` hien **`0`**.

    ⛔ Day la cho de "chua cho dep" nhat trong ca vung phan bo, va chua thi may
    se noi khac so — dung luc ke toan doi chieu hai ben.
    """
    d = _theo_id(du_lieu)[du_lieu["rong"]]
    assert d["alloc_method"] == "0", (
        "o Method rong THAT phai ra chu `0` — xem `fls/ledger/allocate.py`")
    assert d["alloc_na"] is False


def test_doc_mot_dong_mang_CUNG_vung_phan_bo_voi_doc_so(du_lieu):
    """⛔ Luoi va ngan keo ⛔ khong duoc noi hai dieu ve cung mot dong."""
    luoi = _theo_id(du_lieu)
    with noi_chi_doc(dsn_test()) as conn:
        for ten in ("co", "khong", "rong", "la"):
            i = du_lieu[ten]
            d = bc.doc_mot_dong(
                conn, PhamVi("mot_lan_nap", run_id=du_lieu["run"]), i)
            for t in bc.TRUONG_ALLOC:
                assert d[t] == luoi[i][t], (
                    f"dong {i} truong {t}: ngan keo noi {d[t]!r}, luoi noi "
                    f"{luoi[i][t]!r}")


def test_bang_mapping_master_NO_khi_co_hai_dong_cung_ma(du_lieu):
    """⛔⛔ Phep tra cua Sheets ⛔ khong phan biet hoa thuong, con khoa chinh
    cua bang thi **CO**. ⇒ `NB` va `nb` cung ton tai duoc, va luc do may
    ⛔ khong biet dong nao la dong dung.

    ⚠ NO chu ⛔ khong lay dong dau: lay dong dau la **may tu chon** giua hai
    cau tra loi, va o cot phan bo thi hai cau ay ⛔ khong nhat thiet giong nhau.
    """
    ma = du_lieu["ma"]
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_mapping_master (hd_code, need_cfa2,"
                    " method_cfa2) VALUES (%s,'No need','')",
                    (ma.lower() + "-CO",))
    try:
        with noi_chi_doc(dsn_test()) as conn:
            with pytest.raises(ValueError, match="HAI dong cung ma"):
                bc.bang_mapping_master(conn)
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as k:
            k.execute("DELETE FROM fls_mapping_master WHERE hd_code = %s",
                      (ma.lower() + "-CO",))


def test_danh_muc_THAT_cua_kho_khong_co_hai_ma_trung(du_lieu):
    """⭐ Cong tren kho THAT: neu danh muc that co hai ma trung *(bo qua hoa/
    thuong)* thi ca cua `GET /ledger` se NO — nen phai biet TRUOC."""
    with noi_chi_doc(dsn_test()) as conn:
        bang = bc.bang_mapping_master(conn)
    assert bang, "⛔ danh muc RONG — chay `tools/nap_mapping_master.py --ghi`"
