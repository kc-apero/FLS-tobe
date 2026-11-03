"""Cong DUONG BO MOI NOI (`GAP-JOIN-05`, `QĐ-ITL-69`).

★★ **Vi sao cua nay ton tai, ghi lai cho nguoi doc sau.** Tu 27/08 ke toan ghep
duoc tien voi dong lenh, nhung mot moi noi ghep SAI thi ⛔ khong go duoc — chinh
`ghep_lenh` phai NO ra cau *"chua co duong nao lam viec do"*. Mot dong ghep sai
la mot dong **chet cung**. Mo man hang cho ma thieu cua nay la giao cho ke toan
mot cai nut ⛔ khong co duong lui.

★ Bai quan trong nhat o day ⛔ khong phai *"bo duoc"* ma la **bo dung cai gi**:

    ⓐ bo la **THEM dong** — `fls_pm_link` ⛔ khong mat mot dong nao (`INV-I08`)
    ⓑ bo roi thi **ghep lai duoc**, ke ca dung DUNG dong lenh cu (`lan` = 2)
    ⓒ dao dung but toan cua CHINH phep ghep — va ⛔ KHONG dao cai NGUOI da go
    ⓓ ⛔ khong co moi noi thi ⛔ khong bo (`KhongCoMoiNoi`, ⛔ khac `DaGhep`)
    ⓔ ky da CHOT thi ⛔ khong bo
    ⓕ ⛔ khong co ly do thi ⛔ khong bo (`ThieuLyDo`)
    ⓖ `fls_itl` ⛔ KHONG doi mot o nao — ca luc ghep lan luc bo
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
LY_DO_BO = "ghep sai dong lenh — go de ghep lai"

COT_PHAI_GIU = ("hd", "hd_thyt", "pay_type", "cdt1", "cdt1_thyt", "svc_start",
                "svc_end", "id_payee", "invoice", "work_status",
                "period_state", "raw_frozen", "pm_hinh")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    r = "NAP-2000-01-01-U" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong_bank(conn, run: str, tien: str, curr: str = "VND",
               ky: str = "open") -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-U',%s,%s,'UNMAPPED',%s) RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, curr, D(tien),
         ky)).fetchone()[0]


def _lenh(conn, run: str, *ds: tuple) -> None:
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + i, x[0].split("-")[0], x[0], D(x[1]), x[2], x[3], None,
               x[4], x[5], ref_tho=None) for i, x in enumerate(ds)])


def _anh_so(conn, itl_id: int) -> tuple:
    return conn.execute(
        f"SELECT {', '.join(COT_PHAI_GIU)} FROM fls_itl WHERE itl_id=%s",
        (itl_id,)).fetchone()


def _dem(conn, bang: str, itl_id: int) -> int:
    return conn.execute(f"select count(*) from {bang} where itl_id=%s",
                        (itl_id,)).fetchone()[0]


def _mot_ca_ghep(conn, tien: str = "20957000.00") -> tuple[str, int]:
    """Mot dong bank da ghep voi MOT dong lenh — trang thai xuat phat."""
    run = _run(conn)
    i = _dong_bank(conn, run, tien)
    _lenh(conn, run, ("PM30-2", tien, "VND", "Approve",
                      "FNS | Facilities", "SHQ2 | HQ2"))
    gt.ghep_lenh(conn, chi_nap_that(), i, ["PM30-2"], actor=ACTOR, reason=LY_DO)
    return run, i


# ─────────────────────────────────────────── ⓐ bo la THEM, khong XOA
def test_bo_moi_noi_la_THEM_dong__fls_pm_link_KHONG_mat_dong_nao(conn):
    """⛔⛔ Bat bien nang nhat: so giu CA LICH SU, ⛔ khong mot dong bi xoa.

    Neu bai nay do vi `fls_pm_link` mat dong thi co ai da thay `INSERT` bang
    `DELETE` — va tu do khong ai doc lai duoc *"dong nay tung ghep voi gi"*.
    """
    _run_id, i = _mot_ca_ghep(conn)
    assert _dem(conn, "fls_pm_link", i) == 1
    assert _dem(conn, "fls_moi_noi", i) == 1
    truoc = _anh_so(conn, i)

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)

    assert [x["pm_line_id"] for x in ra["da_bo"]] == ["PM30-2"]
    assert ra["ve_hang_cho"] is True
    # ⭐ Bang goc GIU nguyen; khung xem thay doi.
    assert _dem(conn, "fls_pm_link", i) == 1, "⛔ mot dong bi XOA khoi so"
    assert _dem(conn, "fls_moi_noi", i) == 0, "⛔ moi noi da bo van con hieu luc"
    assert _dem(conn, "fls_pm_unlink", i) == 1
    # ⭐ Va so ⛔ khong doi mot o nao.
    assert _anh_so(conn, i) == truoc, "⛔⛔ `fls_itl` BI DOI khi bo moi noi"


def test_bo_moi_noi_de_lai_VET_du_ba_thu__ai_luc_nao_vi_sao(conn):
    """`AUD-1`: mot thao tac khong doc lai duoc *ai lam · luc nao · vi sao* la
    mot thao tac ⛔ khong kiem soat duoc — sau `QĐ-ITL-27` thi vet la lop kiem
    soat DUY NHAT con lai."""
    _run_id, i = _mot_ca_ghep(conn)
    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)

    r = conn.execute(
        "SELECT evt_type, actor, reason, at FROM fls_queue_event"
        " WHERE evt_id=%s", (ra["evt_id"],)).fetchone()
    assert r[0] == "unmatch"
    assert r[1] == ACTOR
    assert LY_DO_BO in r[2] and "PM30-2" in r[2], (
        "ly do phai mang CA cau nguoi go LAN ma dong lenh da bo")
    assert r[3] is not None
    # ⭐ Moi dong bo tro ve DUNG thao tac do — ⛔ khong phai mot cho khac.
    assert conn.execute("select evt_id from fls_pm_unlink where itl_id=%s",
                        (i,)).fetchone()[0] == ra["evt_id"]


# ─────────────────────────────────────────── ⓑ bo roi GHEP LAI duoc
def test_bo_roi_GHEP_LAI_dung_dong_lenh_cu__lan_thanh_2(conn):
    """⭐⭐ **Day la bai da lat khoa cua `fls_pm_link`.**

    Ly do pho bien nhat de bo la **chia tien sai**, ⛔ khong phai chon sai dong
    lenh ⇒ viec ngay sau khi bo la ghep lai **dung dong lenh ay**. Voi khoa cu
    `(itl_id, pm_line_id)` thi viec do bi kho chan bang mot loi trung khoa ma ke
    toan ⛔ khong hieu. Bai nay chan huong quay lai cua khoa cu.
    """
    _run_id, i = _mot_ca_ghep(conn)
    gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)

    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PM30-2"],
                      actor=ACTOR, reason="ghep lai sau khi go")
    assert ra["moi_noi"][0]["pm_line_id"] == "PM30-2"
    assert _dem(conn, "fls_pm_link", i) == 2, "lich su phai co CA HAI lan ghep"
    assert _dem(conn, "fls_moi_noi", i) == 1, "chi MOT moi noi con hieu luc"
    assert conn.execute("select lan from fls_moi_noi where itl_id=%s",
                        (i,)).fetchone()[0] == 2


def test_dong_lenh_vua_go_hien_lai_la_CHUA_ghep_o_danh_sach_ung_vien(conn):
    """⛔ Neu cho DOC con dem tren `fls_pm_link` thi dong lenh vua go van hien
    la *da ghep* — ke toan ⛔ khong ghep lai duoc, va ⛔ khong co loi nao bao."""
    from fls.repo import doc_bao_cao as bc

    # ⚠ Ma dong lenh RIENG cho bai nay: `da_ghep` dem theo `pm_line_id` tren
    # CA kho ("dong lenh nay da ghep o dau chua"), nen dung ma dung chung voi
    # cac bai khac thi con so bi cac lan chay truoc cong vao.
    ma = "PM" + uuid.uuid4().hex[:6].upper() + "-1"
    run = _run(conn)
    i = _dong_bank(conn, run, "777000.00")
    _lenh(conn, run, (ma, "777000.00", "VND", "Approve",
                      "FNS | Facilities", "SHQ2 | HQ2"))
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)

    d = bc.ung_vien_pm(conn, chi_nap_that(), i, n=20)
    ung = {x["pm_line_id"]: x for x in d["ung_vien"]}
    assert ung[ma]["da_ghep"] == 1

    gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)
    d = bc.ung_vien_pm(conn, chi_nap_that(), i, n=20)
    ung = {x["pm_line_id"]: x for x in d["ung_vien"]}
    assert ung[ma]["da_ghep"] == 0, (
        "⛔ dong lenh da go van hien la DA GHEP — cho doc con tro vao bang goc")


# ─────────────────────────────── ⓒ dao dung but toan, va CHI cai cua may
def test_dao_but_toan_do_CHINH_phep_ghep_suy_ra(conn):
    """Phep ghep tu suy `hd`/`cdt1` tu dong lenh. Bo moi noi thi **can cu cua
    phep suy mat** ⇒ de nguyen la de lai mot gia tri ⛔ khong con nguon."""
    _run_id, i = _mot_ca_ghep(conn)
    hieu_luc = dict(conn.execute(
        "select field, value_after from fls_sua_tay where itl_id=%s",
        (i,)).fetchall())
    assert hieu_luc == {"hd": "FNS | Facilities", "cdt1": "SHQ2 | HQ2"}

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)
    assert {x["field"] for x in ra["but_toan_dao"]} == {"hd", "cdt1"}
    assert ra["bo_qua"] == []
    # ⭐ Sau khi dao, ⛔ khong con gia tri nguoi-go nao co hieu luc.
    assert conn.execute("select count(*) from fls_sua_tay where itl_id=%s",
                        (i,)).fetchone()[0] == 0
    # ⛔ Va dao cung la THEM dong: but toan cu VAN nam trong so.
    assert _dem(conn, "fls_adjustment", i) == 4   # 2 suy + 2 dao


def test_KHONG_dao_o_ma_NGUOI_da_go_tay__va_KHAI_RA(conn):
    """⛔⛔ Cai bay that cua cua nay.

    Neu sau phep ghep **nguoi** da go tay len dung o `hd`, thi cai dang co hieu
    luc la gia tri cua NGUOI. May ⛔ khong duoc dap len no khi bo moi noi — va
    cung ⛔ khong duoc im lang: no phai **khai ra** minh da ⛔ khong dao cai gi.
    """
    _run_id, i = _mot_ca_ghep(conn)
    gt.ghi_but_toan(conn, chi_nap_that(), i, "hd", "GAC | Nguoi go tay",
                    actor="ke-toan-2@apero.vn", reason="nguon sai, go lai",
                    force=True)

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)

    assert {x["field"] for x in ra["but_toan_dao"]} == {"cdt1"}, (
        "⛔ chi `cdt1` con la cua phep ghep — `hd` da la cua NGUOI")
    assert [x["field"] for x in ra["bo_qua"]] == ["hd"]
    assert "NGUOI da go tay" in ra["bo_qua"][0]["vi_sao"]
    # ⭐ Gia tri cua NGUOI PHAI con nguyen.
    hieu_luc = dict(conn.execute(
        "select field, value_after from fls_sua_tay where itl_id=%s",
        (i,)).fetchall())
    assert hieu_luc == {"hd": "GAC | Nguoi go tay"}, (
        "⛔⛔ may da dap len gia tri NGUOI go — dung thu `QĐ-ITL-35` cam")


# ─────────────────────────────────────────── ⓓⓔⓕ bay cho TU CHOI
def test_KHONG_co_moi_noi_thi_KHONG_bo(conn):
    """⛔ Cau tra loi phai KHAC `DaGhep`: chua ghep va da ghep la hai trang
    thai, va man hinh ve hai nut khac nhau."""
    run = _run(conn)
    i = _dong_bank(conn, run, "1000.00")
    with pytest.raises(gt.KhongCoMoiNoi):
        gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)


def test_bo_HAI_lan_thi_lan_thu_hai_bi_TU_CHOI(conn):
    """Nut bam hai lan ⛔ khong duoc thanh hai lan bo."""
    _run_id, i = _mot_ca_ghep(conn)
    gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)
    with pytest.raises(gt.KhongCoMoiNoi):
        gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)
    assert _dem(conn, "fls_pm_unlink", i) == 1


def test_ky_DA_CHOT_thi_KHONG_bo(conn):
    """`INV-I13`: ghep sai trong ky da chot xu bang but toan dieu chinh ky sau,
    ⛔ khong sua lai qua khu."""
    run = _run(conn)
    i = _dong_bank(conn, run, "5000.00")
    _lenh(conn, run, ("PM31-1", "5000.00", "VND", "Approve", "FNS | X", "SHQ2 | HQ2"))
    gt.ghep_lenh(conn, chi_nap_that(), i, ["PM31-1"], actor=ACTOR, reason=LY_DO)
    conn.execute("update fls_itl set period_state='locked' where itl_id=%s", (i,))
    with pytest.raises(gt.KyDaChot):
        gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)
    assert _dem(conn, "fls_moi_noi", i) == 1, "⛔ da bo du ky chot"


def test_KHONG_ly_do_thi_KHONG_bo(conn):
    """`INV-I16`: go mot moi noi ma khong noi vi sao thi ⛔ khong ai biet lan
    ghep nao dung."""
    _run_id, i = _mot_ca_ghep(conn)
    for xau in ("", "   ", None):
        with pytest.raises(gt.ThieuLyDo):
            gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=xau)
    assert _dem(conn, "fls_pm_unlink", i) == 0


def test_ngoai_pham_vi_thi_KHONG_bo(conn):
    """⛔ Cua ⛔ khong duoc tiet lo rang mot dong ngoai pham vi TON TAI."""
    with pytest.raises(gt.NgoaiPhamVi):
        gt.bo_moi_noi(conn, chi_nap_that(), 999_999_999, actor=ACTOR,
                      reason=LY_DO_BO)


# ─────────────────────────────────────────── bo CA CHUM, khong bo le
def test_bo_CA_CHUM_ba_moi_noi__Σ_khong_bao_gio_lech(conn):
    """⛔⛔ Cua nay CO Y ⛔ khong bo le mot moi noi.

    Bat bien la `Σ moi noi = tien dong bank`. Bo le mot trong ba thi Σ con 2/3
    ⇒ **tao ra dung cai trang thai sai** ma cong `SIGMA_MOI_NOI` bat. Muon doi
    mot dong lenh: bo ca chum roi ghep lai.
    """
    run = _run(conn)
    i = _dong_bank(conn, run, "600.00")
    _lenh(conn, run,
          ("PM40-1", "100.00", "VND", "Approve", "FNS | X", "SHQ2 | HQ2"),
          ("PM40-2", "200.00", "VND", "Approve", "FNS | X", "SHQ2 | HQ2"),
          ("PM40-3", "300.00", "VND", "Approve", "FNS | X", "SHQ2 | HQ2"))
    gt.ghep_lenh(conn, chi_nap_that(), i, ["PM40-1", "PM40-2", "PM40-3"],
                 actor=ACTOR, reason=LY_DO)
    assert _dem(conn, "fls_moi_noi", i) == 3

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason=LY_DO_BO)
    assert len(ra["da_bo"]) == 3
    assert _dem(conn, "fls_moi_noi", i) == 0, (
        "bo le se de lai Σ lech — cua nay phai bo HET hay ⛔ khong bo gi")
    assert _dem(conn, "fls_pm_link", i) == 3, "lich su giu nguyen ba dong"
