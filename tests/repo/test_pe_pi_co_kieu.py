"""Bay khoa `PE`/`PI` len KIEU trong `fls_pm_line` — migration `0023`.

⭐⭐⭐ Owner chot 2026-09-17: *"PE/PI cot CO KIEU trong `fls_pm_line`, chua
can lam bang rieng"*. ⇒ **Duong VAO ≠ THUC THE**: ca ba di nho MOT duong nap
(`PM_Unpivot`), nhung `PE` · `PI` · `PM` la ba thuc the khac nhau.

⛔⛔ Bo bai nay canh **ba** thu, va thu thu ba la thu de bi "sua giup" nhat:

  ⓐ doc dung — 5 truong tu `PM_Unpivot` vao `DongPM`, `pe_loai` do MA sinh;
  ⓑ ghi dung — duong ghi that co cho cho 5 cot, ⛔ khong bo quen;
  ⓒ ⭐ **CO Y ⛔ KHONG dat `CHECK` tren khoa `PE`/`PI`** — va bai
    `test_CO_Y_khong_dat_CHECK_...` **ghim quyet dinh ay**, keo mot nguoi
    sau doc thay *"0 ngoai le tren 26.404 dong"* roi them `CHECK` cho chac.
    Them vao la **do ca luot nap** thay vi bao mot dong la.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import PM_COT, PM_TIEU_DE_MONG_DOI, DongPM
from fls.db import schema as db_schema
from fls.db.kho import dsn_test
from fls.repo.chay_nap import chen_dong_pm

KHOA_PE_PI = ("pe_slip", "pe_line", "pe_loai", "pi_slip", "pi_line")


def _bang():
    return [v for v in vars(db_schema).values()
            if getattr(v, "name", "") == "fls_pm_line"][0]


# ── ⓐ BAN KHAI ───────────────────────────────────────────────────────────
def test_nam_cot_PE_PI_deu_duoc_KHAI_trong_schema():
    co = {c.name for c in _bang().columns}
    thieu = [x for x in KHOA_PE_PI if x not in co]
    assert not thieu, f"⛔ `schema.py` thieu cot: {thieu}"


def test_hop_dong_cot_PM_doc_du_bay_vi_tri_cua_PE_PI():
    """⛔ Doc thieu mot vi tri = mot cot **im lang rong mai mai**."""
    for k in ("pe_adv", "pe_urg", "pe_slip", "pe_line", "pi_slip", "pi_line"):
        assert k in PM_COT, f"⛔ `PM_COT` thieu {k!r}"
        assert PM_COT[k] in PM_TIEU_DE_MONG_DOI, (
            f"⛔ vi tri {PM_COT[k]} ({k}) ⛔ khong co tieu de mong doi ⇒ nguon "
            f"doi cot thi ⛔ KHONG cong nao bao")


def test_tieu_de_mong_doi_cua_PE_PI_dung_NGUYEN_VAN_cua_nguon():
    """⛔ Do tu `A _ PAY100 _ PM11 Entry Data` tab `PM_Unpivot`, hang 2."""
    assert PM_TIEU_DE_MONG_DOI[17] == "ID PESlip"
    assert PM_TIEU_DE_MONG_DOI[18] == "ID PELine"
    assert PM_TIEU_DE_MONG_DOI[19] == "ID PISlip"
    assert PM_TIEU_DE_MONG_DOI[20] == "ID PILine"
    assert PM_TIEU_DE_MONG_DOI[3] == "ID PELine - Nội dung PE (Advance)"
    assert PM_TIEU_DE_MONG_DOI[4] == "ID PELine - Nội dung PE (Urgent)"


# ── ⓑ DUONG GHI ──────────────────────────────────────────────────────────
@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), connect_timeout=5) as c:
        yield c


def _mot_dong(**kw) -> DongPM:
    goc = dict(dong_sheet=3, slip="PMS1", line="PML" + uuid.uuid4().hex[:8],
               tien=D("1000"), cur="VND", status="Approve", ref=None)
    return DongPM(**{**goc, **kw})


def _nap(conn, dong):
    """Mot lan nap toi thieu. ⛔ Bon cot `*_version` la `NOT NULL` va ⛔ khong
    co mac dinh — co y: mot lan nap ⛔ khong duoc quen minh chay theo hop dong
    NAO (`INV-I16`)."""
    ma = "T-PEPI-" + uuid.uuid4().hex[:8]
    conn.execute(
        "INSERT INTO fls_run (run_id, contract_version, canon_version,"
        " mapping_version) VALUES (%s,'t','t','t')", (ma,))

    class _NC:
        run_id = ma
    chen_dong_pm(conn, _NC(), dong)
    return ma


def test_duong_GHI_co_cho_cho_ca_nam_cot(conn):
    """⛔⛔ Bai nay chan dung mot lo that: them cot vao `schema.py` ma quen
    them vao cau `INSERT` ⇒ moi lan nap SAU de trong cot vua khai, va
    ⛔ khong gi bao."""
    d = _mot_dong(pe_slip="PES9", pe_line="PEL9", pe_loai="Urgent")
    ma = _nap(conn, [d])
    r = conn.execute(
        "select pe_slip, pe_line, pe_loai, pi_slip, pi_line"
        " from fls_pm_line where run_id=%s", (ma,)).fetchone()
    assert r == ("PES9", "PEL9", "Urgent", None, None), (
        f"⛔ duong ghi lam MAT gia tri: {r}")
    conn.rollback()


# ── ⓒ RANG BUOC: mot cai CO, bon cai CO Y KHONG ─────────────────────────
def test_CHECK_pe_loai_CAN_that(conn):
    """⛔ Mot rang buoc chua tung thay do la mot rang buoc chua biet co song."""
    with pytest.raises(psycopg.errors.CheckViolation):
        _nap(conn, [_mot_dong(pe_line="PEL1", pe_loai="Linh tinh")])
    conn.rollback()
    with pytest.raises(psycopg.errors.CheckViolation):
        # `pe_loai` ma ⛔ KHONG co `pe_line` — mot loai khong gan vao dau
        _nap(conn, [_mot_dong(pe_loai="Advance")])
    conn.rollback()


def test_CO_Y_khong_dat_CHECK_tren_khoa_PE_PI():
    """⭐⭐⭐ GHIM MOT QUYET DINH, ⛔ khong ghim mot hanh vi.

    Do tren kho 17/09: **0** ngoai le / 26.404 dong *(mot dong co DUNG MOT
    cha)*. Con so ay moi mot nguoi sau them `CHECK` **cho chac**.

    ⛔⛔ ⛔ Dung them. `chay_nap.chen_dong_pm` chen **ca lan nap trong MOT
    giao dich**, va chinh ham do da ghi: *"nem loi la huy ca lan nap chi vi
    mot dong lenh thieu ma"*. ⇒ Mot `CHECK` o day bien **mot dong la** thanh
    **do ca luot nap**: tin tuc thanh su co, va ke toan mat ca anh chup.

    ⇒ Ba bat bien ay duoc **DEM va NEU TEN** luc nap (`INV-I16`), va co bai
      `test_kho_THAT_*` duoi day do chung tren kho.
    """
    co_check = {c.name for c in _bang().columns if c.check}
    assert co_check == {"pe_loai"}, (
        "⛔ Nhom `PE`/`PI` chi duoc co DUNG MOT `CHECK` (`pe_loai` — gia tri "
        "do MA CUA TA sinh, nguon ⛔ khong lam vo duoc). Dat them `CHECK` len "
        "`pe_line`/`pi_line` la doi **mot dong la** thanh **do ca luot nap**. "
        f"Dang co: {sorted(co_check)}")


def test_may_DEM_va_NEU_TEN_dong_la_thay_vi_chan(conn, capsys):
    """⛔ ⛔ Im lang cung ⛔ khong duoc (`INV-I16`) — phai DEM va goi TEN."""
    # ⛔ `dong_sheet` phai KHAC nhau — `(run_id, source_row)` la khoa DUY
    #   NHAT: mot so dong cua to giay ⛔ khong the ung voi hai dong.
    ma = _nap(conn, [
        _mot_dong(dong_sheet=3, pe_line="PEL2", pe_slip="PES2",
                  pe_loai="Advance", pi_line="PIL2", pi_slip="PIS2"),
        _mot_dong(dong_sheet=4),                         # ⛔ KHONG cha nao
        _mot_dong(dong_sheet=5, pe_slip="PES3"),         # lech CAP
    ])
    ra = capsys.readouterr().out
    assert "CA HAI cha" in ra and "KHONG co cha nao" in ra and "lech CAP" in ra, (
        f"⛔ may nap ⛔ khong neu ten dong la:\n{ra}")
    n = conn.execute("select count(*) from fls_pm_line where run_id=%s",
                     (ma,)).fetchone()[0]
    assert n == 3, "⛔ dong la phai VAO KHO — chung la tin tuc, ⛔ khong phai rac"
    conn.rollback()
