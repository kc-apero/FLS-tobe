"""Cong GHEP LENH BANG TAY (`OP-02`, `QĐ-ITL-48`) — dong `GAP-API-04`.

★★ Bai quan trong nhat o day ⛔ khong phai *"ghep duoc"* ma la **bay cho TU CHOI**:
mot cua ghep chi biet dong y la mot cua se ghi ra so nhung con so khong ai kiem.

    ⓐ dong ngoai pham vi            -> `NgoaiPhamVi`
    ⓑ ky da chot                    -> `KyDaChot`  (⛔ ke ca `force`)
    ⓒ dong DA ghep                  -> `DaGhep`
    ⓓ ma dong lenh khong co         -> `DongLenhLa`
    ⓔ tien te khac nhau             -> `KhacTienTe`  (kiem TRUOC Σ)
    ⓕ Σ lech qua dung sai           -> `LechTong`
    ⓖ `status` khong phai Approve   -> `ChuaDuyet`  (tru khi `force`)

★ Va hai bat bien phai giu sau khi ghi:
    · `Σ moi noi = tien dong bank`   KHIT, ⛔ khong sai mot dong
    · `fls_itl` ⛔ KHONG doi mot o nao (`INV-I08`)
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo import ghi_tay as gt
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.pham_vi import chi_nap_that

pytestmark = pytest.mark.pg

DSN = dsn_test()
ACTOR = "ke-toan@apero.vn"
LY_DO = "ghep tay tu man F01"

# Cac cot cua `fls_itl` PHAI khong doi sau khi ghep (`INV-I08` + `QĐ-ITL-35`).
COT_PHAI_GIU = ("hd", "hd_thyt", "pay_type", "pay_type_thyt", "cdt1",
                "cdt1_thyt", "svc_start", "svc_end", "id_payee", "invoice",
                "work_status",
                "period_state", "raw_frozen", "pm_hinh")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    """Lan nap HINH DANG THAT nhung nam **2000** — xem `fls/repo/kho_sach.py`."""
    r = "NAP-2000-01-01-G" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong_bank(conn, run: str, tien: str, curr: str = "VND",
               doc_no: str = "FT-X", ky: str = "open") -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,%s,'UNMAPPED',%s) RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, doc_no, curr,
         D(tien), ky)).fetchone()[0]


def _lenh(conn, run: str, *ds: tuple) -> None:
    """`ds` = (line, tien, curr, status, hd, cdt1) — dat vao anh chup."""
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + i, x[0].split("-")[0], x[0], D(x[1]), x[2], x[3], None,
               x[4], x[5], ref_tho=None) for i, x in enumerate(ds)])


def _anh_so(conn, itl_id: int) -> tuple:
    return conn.execute(
        f"SELECT {', '.join(COT_PHAI_GIU)} FROM fls_itl WHERE itl_id=%s",
        (itl_id,)).fetchone()


# ─────────────────────────────────────────────── ghep duoc
def test_ghep_MOT_dong_lenh__so_khong_doi_mot_o(conn):
    """★ Ca ghep don gian nhat, va bat bien quan trong nhat: SO ⛔ KHONG DOI."""
    run = _run(conn)
    i = _dong_bank(conn, run, "20957000.00")
    _lenh(conn, run, ("PM30-2", "20957000.00", "VND", "Approve",
                      "FNS | Facilities", "SHQ2 | HQ2"))
    truoc = _anh_so(conn, i)

    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PM30-2"],
                      actor=ACTOR, reason=LY_DO)
    assert [x["pm_line_id"] for x in ra["moi_noi"]] == ["PM30-2"]
    assert ra["moi_noi"][0]["hinh"] == "T", "ghep tay phai mang hinh `T`"
    assert ra["khong_suy_duoc"] == []
    assert {x["field"] for x in ra["but_toan"]} == {"hd", "cdt1"}

    assert _anh_so(conn, i) == truoc, "⛔⛔ `fls_itl` BI DOI sau khi ghep"
    tong = conn.execute("select sum(amount) from fls_pm_link where itl_id=%s",
                        (i,)).fetchone()[0]
    assert tong == D("20957000.00")


def test_ghep_N_dong_lenh__chia_tien_KHIT_khong_sai_mot_dong(conn):
    """Hinh `B`: mot lan chuyen tra N dong lenh. Σ phai KHIT."""
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run,
          ("PM1-1", "60.00", "VND", "Approve", "HD-A", "CDT-A"),
          ("PM1-2", "40.00", "VND", "Approve", "HD-A", "CDT-A"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PM1-1", "PM1-2"],
                      actor=ACTOR, reason=LY_DO)
    assert sum(D(x["amount"]) for x in ra["moi_noi"]) == D("100.00")
    assert ra["phieu"] == ["PM1"]


def test_N_dong_lenh_noi_N_thu__may_KHONG_CHON_va_KHAI_RA(conn):
    """★★ `INV-I16`: hai dong lenh mang hai `hd` khac nhau ⇒ may ⛔ khong chon.

    Day la cho de nhat de mot he thong "thong minh" quyet thay nguoi. Ket qua
    dung la **noi ra la khong suy duoc**, ⛔ khong phai lay dong dau tien.
    """
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run,
          ("PM2-1", "60.00", "VND", "Approve", "HD-A", "CDT-A"),
          ("PM2-2", "40.00", "VND", "Approve", "HD-B", "CDT-A"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PM2-1", "PM2-2"],
                      actor=ACTOR, reason=LY_DO)
    assert ra["khong_suy_duoc"] == ["hd"], "hd lech nhau thi phai khai la khong suy duoc"
    assert [x["field"] for x in ra["but_toan"]] == ["cdt1"], \
        "cdt1 hai dong dong y nen VAN duoc ghi"


def test_dung_sai_VND_1000_cuu_duoc_phi_bank(conn):
    """`QĐ-ITL-57`: dung sai Σ = 1.000 **VND**. Lech 500 thi qua."""
    run = _run(conn)
    i = _dong_bank(conn, run, "1000500.00")
    _lenh(conn, run, ("PM3-1", "1000000.00", "VND", "Approve", "H", "C"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PM3-1"],
                      actor=ACTOR, reason=LY_DO)
    # ⛔ Moi noi mang tien cua DONG BANK, ⛔ khong phai tien cua dong lenh:
    # so ghi tien that da chuyen, chenh 500 la phi bank.
    assert ra["moi_noi"][0]["amount"] == "1000500.00"


def test_ngoai_te_dung_sai_0__lech_mot_xu_la_TU_CHOI(conn):
    """⚠ `GAP-CR1-03` chua chot: tien te ngoai VND co dung sai **0**.

    Bai nay la **cho ghi lai** con so dang cho ke toan tra loi — doi thi doi o
    `DUNG_SAI`, ⛔ khong doi bang cach noi long cong.
    """
    run = _run(conn)
    i = _dong_bank(conn, run, "100.01", curr="USD")
    _lenh(conn, run, ("PM4-1", "100.00", "USD", "Approve", "H", "C"))
    with pytest.raises(gt.LechTong) as e:
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PM4-1"],
                     actor=ACTOR, reason=LY_DO)
    assert "dung sai 0" in str(e.value)


# ─────────────────────────────────────────────── bay cho TU CHOI
def test_TU_CHOI_khi_tien_te_khac_nhau__kiem_TRUOC_Σ(conn):
    """★ Thu tu co chu y: neu kiem Σ truoc thi hai so khac don vi tinh co bang
    nhau se ghep SAI ma ⛔ khong cong nao do (199 dong that thuoc lop nay)."""
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00", curr="VND")
    _lenh(conn, run, ("PM5-1", "100.00", "USD", "Approve", "H", "C"))
    with pytest.raises(gt.KhacTienTe):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PM5-1"],
                     actor=ACTOR, reason=LY_DO)


def test_TU_CHOI_khi_Σ_lech__va_KHONG_ghi_gi(conn):
    """⛔ Lech thi GIU UNMAPPED va ⛔ khong de lai mot moi noi nao.

    ⚠ Lech phai VUOT dung sai (1.000 VND) moi bi tu choi — ban dau toi viet bai
    nay voi lech **30 VND** va no khong do, dung: 30 nam TRONG dung sai. Xem bai
    `test_DO_LO_cua_dung_sai_TUYET_DOI_tren_cua_ghep_TAY` ngay duoi.
    """
    run = _run(conn)
    i = _dong_bank(conn, run, "100000.00")
    _lenh(conn, run, ("PM6-1", "70000.00", "VND", "Approve", "H", "C"))
    with pytest.raises(gt.LechTong) as e:
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PM6-1"],
                     actor=ACTOR, reason=LY_DO)
    assert e.value.them["khac"]["lech"] == "-30000.00"
    assert conn.execute("select count(*) from fls_pm_link where itl_id=%s",
                        (i,)).fetchone()[0] == 0
    assert conn.execute("select count(*) from fls_queue_event where itl_id=%s",
                        (i,)).fetchone()[0] == 0, \
        "⛔ tu choi ma van de lai vet su kien = da ghi mot phan"


def test_DO_LO_dung_sai_TUYET_DOI_da_DONG_bang_TY_LE(conn):
    """⭐⭐ **Bai nay tung ghi mot DO LO. Nay no ghi do lo DA DONG.**

    ⛔ Truoc `QĐ-ITL-63`: `QĐ-ITL-57` chot dung sai Σ = **1.000 VND**, va con so
    ay duoc do/duyet tren phep ghep **TU DONG**, noi khoang lech LON NHAT that
    chi **2,00 dong**. Nhung o cua **TAY** nguoi go chon dong lenh nao cung
    duoc, nen cung con so ay cho ghep dong bank **100 dong** voi dong lenh
    **1.099 dong** — lech **999% cua chinh giao dich** ma cong VAN xanh. Chinh
    fixture duoi day, truoc 28/08, **ghep DUOC**.

    ⭐ Owner chot 2026-08-28 (`QĐ-ITL-63`, dong `GAP-CR1-04`): cua ghep TAY doi
    **CA HAI** dieu kien, lay cai NHO hon — lech <= **1.000 dong** VA lech <=
    **0,5%** cua tien bank. ⇒ 0,5% cua 100 dong = **0,5 dong** ⇒ **tu choi**.

    ★ Vi sao phai la CA HAI, ⛔ khong phai mot: mot minh **con so tuyet doi** ho
    dau khoan NHO (ca nay); mot minh **ty le** ho dau khoan LON (0,5% cua 3,7
    ty = **18,5 trieu**, rong hon han khoang lam tron). Moi dieu kien chan mot
    dau, va do la ly do giu ca hai.
    """
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run, ("PMF-1", "1099.00", "VND", "Approve", "H", "C"))
    with pytest.raises(gt.LechTong) as e:
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PMF-1"],
                     actor=ACTOR, reason=LY_DO)
    khac = e.value.them["khac"]
    assert khac["lech"] == "999.00"
    assert D(khac["dung_sai"]) == D("0.5"), "0,5% cua 100 = 0,5 dong"
    assert khac["ty_le"] == "0.005"
    # ⛔ Va tu choi thi ⛔ khong de lai mot vet nao — nua vet la da ghi mot phan.
    assert conn.execute("select count(*) from fls_pm_link where itl_id=%s",
                        (i,)).fetchone()[0] == 0
    assert conn.execute("select count(*) from fls_queue_event where itl_id=%s",
                        (i,)).fetchone()[0] == 0


def test_LAM_TRON_that_van_ghep_DUOC_sau_QĐ_63(conn):
    """⛔ Luat moi ⛔ KHONG duoc chan cai no khong nen chan.

    18 ca lech THAT do duoc tren so that nam trong **0,40 → 2,00 dong**, tren
    nhung khoan tu **560 nghin** den **3,7 ty**. Bai nay lay ca NHO NHAT trong
    so do (`560.002` vs `560.001,60` — lech **0,40 dong**): 0,5% cua 560.002 la
    **2.800 dong** ⇒ dung sai = min(1.000, 2.800) = **1.000** ⇒ **ghep duoc**.

    ⇒ Ty le chi bat dau chat hon con so tuyet doi khi tien bank **< 200.000
    dong** — dung khoang ma mot con so tuyet doi 1.000 la qua rong.
    """
    run = _run(conn)
    i = _dong_bank(conn, run, "560002.00")
    _lenh(conn, run, ("PMG-1", "560001.60", "VND", "Approve", "H", "C"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PMG-1"],
                      actor=ACTOR, reason=LY_DO)
    assert ra["moi_noi"][0]["amount"] == "560002.00", \
        "moi noi mang tien BANK, ⛔ khong phai tien dong lenh"


def test_TU_CHOI_dong_lenh_KHONG_co_trong_anh_chup(conn):
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run, ("PM7-1", "100.00", "VND", "Approve", "H", "C"))
    with pytest.raises(gt.DongLenhLa) as e:
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PM7-1", "KHONG-CO"],
                     actor=ACTOR, reason=LY_DO)
    assert e.value.them["khac"]["thieu"] == ["KHONG-CO"]


def test_TU_CHOI_dong_lenh_cua_LAN_NAP_KHAC(conn):
    """★ Anh chup gan voi LAN NAP. Dong lenh cua lan nap khac ⛔ khong dung duoc —
    khong thi lineage `INV-I05` dut, va tien co the da doi tu luc do."""
    r1, r2 = _run(conn), _run(conn)
    i = _dong_bank(conn, r1, "100.00")
    _lenh(conn, r2, ("PM8-1", "100.00", "VND", "Approve", "H", "C"))
    with pytest.raises(gt.DongLenhLa):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PM8-1"],
                     actor=ACTOR, reason=LY_DO)


def test_TU_CHOI_khi_dong_DA_ghep__kem_moi_noi_dang_co(conn):
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run,
          ("PM9-1", "100.00", "VND", "Approve", "H", "C"),
          ("PM9-2", "100.00", "VND", "Approve", "H", "C"))
    gt.ghep_lenh(conn, chi_nap_that(), i, ["PM9-1"], actor=ACTOR, reason=LY_DO)
    with pytest.raises(gt.DaGhep) as e:
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PM9-2"],
                     actor=ACTOR, reason=LY_DO)
    assert e.value.them["khac"]["moi_noi"][0]["pm_line_id"] == "PM9-1"


def test_TU_CHOI_status_khong_phai_Approve__tru_khi_force(conn):
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run, ("PMA-1", "100.00", "VND", "Reject", "H", "C"))
    with pytest.raises(gt.ChuaDuyet):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PMA-1"],
                     actor=ACTOR, reason=LY_DO)
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PMA-1"], actor=ACTOR,
                      reason=LY_DO, force=True)
    assert ra["chua_duyet"] == ["PMA-1"]
    # ⛔ `force` phai de lai vet la DA force, khong thi vet khong doc duoc.
    vet = conn.execute("select reason from fls_queue_event where itl_id=%s",
                       (i,)).fetchone()[0]
    assert "FORCE chua duyet" in vet


def test_status_RONG_cung_bi_TU_CHOI__RONG_la_KHONG_BIET(conn):
    """⛔ `INV-I16`: `status` rong la **khong biet**, ⛔ khong phai 'da duyet'."""
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run, ("PMB-1", "100.00", "VND", "", "H", "C"))
    with pytest.raises(gt.ChuaDuyet):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PMB-1"],
                     actor=ACTOR, reason=LY_DO)


def test_TU_CHOI_ky_DA_CHOT__ke_ca_force(conn):
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00", ky="locked")
    _lenh(conn, run, ("PMC-1", "100.00", "VND", "Approve", "H", "C"))
    for f in (False, True):
        with pytest.raises(gt.KyDaChot):
            gt.ghep_lenh(conn, chi_nap_that(), i, ["PMC-1"],
                         actor=ACTOR, reason=LY_DO, force=f)


def test_TU_CHOI_khi_THIEU_LY_DO(conn):
    """Ly do la bat buoc — mot phep ghep khong noi vi sao la khong truy duoc."""
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run, ("PMD-1", "100.00", "VND", "Approve", "H", "C"))
    with pytest.raises(gt.ThieuLyDo):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PMD-1"], actor=ACTOR, reason="  ")


def test_TU_CHOI_khi_danh_sach_RONG_hay_LAP(conn):
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    with pytest.raises(gt.DongLenhLa):
        gt.ghep_lenh(conn, chi_nap_that(), i, [], actor=ACTOR, reason=LY_DO)
    with pytest.raises(gt.DongLenhLa):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["X", "X"],
                     actor=ACTOR, reason=LY_DO)


def test_TU_CHOI_dong_NGOAI_pham_vi(conn):
    """⛔ Cung mot cau tra loi voi *"khong co dong nay"*."""
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES ('KHONG-PHAI-NAP','v1.0','v1.0','v1.0')"
                 " ON CONFLICT DO NOTHING")
    i = _dong_bank(conn, "KHONG-PHAI-NAP", "100.00")
    with pytest.raises(gt.NgoaiPhamVi):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["X"], actor=ACTOR, reason=LY_DO)


def test_THIEU_actor_thi_NO(conn):
    """`actor` den tu THE. Thieu la nhat ky vo nghia."""
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run, ("PME-1", "100.00", "VND", "Approve", "H", "C"))
    with pytest.raises(gt.LoiGhi):
        gt.ghep_lenh(conn, chi_nap_that(), i, ["PME-1"], actor="", reason=LY_DO)
