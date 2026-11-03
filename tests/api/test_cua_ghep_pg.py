"""Hai duong GHEP LENH chay THAT qua HTTP (`OP-02`, `QĐ-ITL-48`).

⛔ Truoc 27/08 ca hai duong nay **BI CHAN, ⛔ khong phai chua lam**: danh sach dong
lenh chi nam o he khac va bo nap doc no **luc chay roi khong luu** (`GAP-API-04`).
Owner chot duong **(a)** — luu anh chup vao kho (`fls_pm_line`, migration `0011`).

★ Bo bai nay ⛔ khong goi ham Python truc tiep: no phai di qua the, qua phep chon
ket noi theo bang tuyen, va qua vo boc `{data, error, meta}`.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import threading
import time
import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM
from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm

pytestmark = pytest.mark.pg

KHOA = "khoa-thu-cua-ghep-dai-hon-ba-muoi-hai-ky-tu-that"
AI = "ke.toan@apero.vn"
V = cua.bang_tuyen.TIEN_TO


@pytest.fixture()
def du_lieu():
    """Mot dong bank **1.000.000 VND** + bon dong lenh phu bon BAC xep hang.

    ⚠ Vi sao 1.000.000 chu ⛔ khong 100: dung sai VND la **1.000 tuyet doi**
    (`QĐ-ITL-57`), nen tren mot dong bank 100 VND thi hai dong lenh 100 + 100
    (lech 100) VAN nam trong dung sai ⇒ bai *"Σ lech thi 422"* xanh SAI. Day la
    lan thu hai dung sai tuyet doi lam mot bai cua toi xanh sai trong cung mot
    buoi — xem `GAP-CR1-04`.
    """
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        run = f"NAP-2000-01-01-GH{uuid.uuid4().hex[:6].upper()}"
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, doc_no, curr, ps_co,"
            " work_status) VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0','v1.0',"
            " false,'{}'::jsonb,'FT-25 099/7','VND',%s,'UNMAPPED')"
            " RETURNING itl_id",
            (uuid.uuid4().hex, run, D("1000000.00")))
        itl = cur.fetchone()[0]
        chen_dong_pm(c, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
            # bac `ma`: reference khop sau khi chuan hoa (`FT-25 099/7`)
            DongPM(3, "PMS1", "PMS1-1", D("1000000.00"), "VND", "Approve",
                   "FT250997", "HD-1", "CDT-1", ref_tho="FT25099/7"),
            # bac `tien`: tien bang dung, ma khac
            DongPM(4, "PMS2", "PMS2-1", D("1000000.00"), "VND", "Approve",
                   "KHAC", "HD-2", "CDT-2", ref_tho="KHAC"),
            # bac `gan_tien`: lech 500 — nam TRONG dung sai 1.000 VND
            DongPM(5, "PMS3", "PMS3-1", D("1000500.00"), "VND", "Approve",
                   None, "HD-3", "CDT-3"),
            # tien te khac: ⛔ khong duoc xuat hien trong danh sach
            DongPM(6, "PMS4", "PMS4-1", D("1000000.00"), "USD", "Approve",
                   None, "HD-4", "CDT-4"),
        ])
    return {"run": run, "itl": itl}


def _mo_doc():
    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()
    return mo


def _mo_ghi():
    @contextlib.contextmanager
    def mo():
        conn = psycopg.connect(dsn_test(), autocommit=True)
        try:
            yield conn
        finally:
            conn.close()
    return mo


@contextlib.contextmanager
def _may(mo_ghi=None):
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = None
    try:
        m = cua.dung_may(_mo_doc(), cong=0, mo_ghi=mo_ghi)
        threading.Thread(target=m.serve_forever, daemon=True).start()
        yield m
    finally:
        if m is not None:
            m.shutdown()
            m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


@pytest.fixture()
def may():
    with _may(mo_ghi=_mo_ghi()) as m:
        yield m


@pytest.fixture()
def may_chi_doc():
    with _may(mo_ghi=None) as m:
        yield m


def _goi(may, duong: str, *, pt: str = "GET", than: dict | None = None,
         co_the: bool = True) -> tuple[int, dict]:
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de: dict[str, str] = {}
    if co_the:
        de["Authorization"] = "Bearer " + the.dong_the(
            {"sub": AI, "exp": int(time.time()) + 300}, KHOA.encode())
    body = json.dumps(than).encode() if than is not None else None
    if body is not None:
        de["Content-Type"] = "application/json"
    try:
        c.request(pt, duong, body=body, headers=de)
        r = c.getresponse()
        d = r.read()
        return r.status, (json.loads(d) if d else {})
    finally:
        c.close()


# ─────────────────────────────────────────── duong DOC ung vien
def test_ung_vien_xep_theo_BON_BAC_CO_TEN(may, du_lieu):
    """★ Bac doc len thanh cau, ⛔ khong phai mot diem so 0..1."""
    ma, r = _goi(may, f"{V}/queue/{du_lieu['itl']}/pm-candidates")
    assert ma == 200, r
    uv = r["data"]["ung_vien"]
    assert [x["bac"] for x in uv] == ["ma", "tien", "gan_tien"], \
        "thu tu phai la ma > tien > gan_tien"
    assert [x["pm_line_id"] for x in uv] == ["PMS1-1", "PMS2-1", "PMS3-1"]
    # ⛔ Dong USD ⛔ khong duoc lot vao: cong hai don vi khac nhau la vo nghia.
    assert "PMS4-1" not in [x["pm_line_id"] for x in uv]


def test_ung_vien_mang_TUOI_cua_anh_chup(may, du_lieu):
    """★★ Cau tra loi cho *"ban luu gia di thi sao"* ⛔ khong phai *"no khong
    gia"* — ma la **noi ra no gia bao nhieu**, de nguoi go tu quyet."""
    ma, r = _goi(may, f"{V}/queue/{du_lieu['itl']}/pm-candidates")
    assert ma == 200
    ac = r["data"]["anh_chup"]
    assert ac["run_id"] == du_lieu["run"]
    assert ac["so_dong"] == 4
    assert ac["doc_luc_muon_nhat"], "⛔ thieu TUOI cua anh chup"


def test_ung_vien_KHAI_RA_thu_KHONG_xep_duoc(may, du_lieu):
    """⛔ `BA-07` §2 mong xep theo ngay/payee. Anh chup ⛔ khong mang PII va ⛔
    khong mang ngay ⇒ **khai ra**, ⛔ khong de man hinh tu suy (`GAP-JOIN-04`)."""
    ma, r = _goi(may, f"{V}/queue/{du_lieu['itl']}/pm-candidates")
    assert r["data"]["khong_xep_duoc_theo"] == ["ngay", "payee"]
    assert "PII" in r["data"]["vi_sao"]


def test_ung_vien_mang_CANH_BAO_chu_khong_AN_dong_chua_duyet(may, du_lieu):
    """⛔ An dong `Reject` di la **mac dinh im lang** (`INV-I16`)."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        c.execute("UPDATE fls_pm_line SET status='Reject'"
                  " WHERE run_id=%s AND pm_line_id='PMS2-1'", (du_lieu["run"],))
    ma, r = _goi(may, f"{V}/queue/{du_lieu['itl']}/pm-candidates")
    x = [y for y in r["data"]["ung_vien"] if y["pm_line_id"] == "PMS2-1"]
    assert x, "dong Reject VAN phai hien"
    assert "Reject" in x[0]["canh_bao"]


def test_ung_vien_ngoai_pham_vi_thi_404(may):
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES ('KHONG-NAP-GH','v1.0','v1.0','v1.0')"
                    " ON CONFLICT DO NOTHING")
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, curr, ps_co, work_status)"
            " VALUES (%s,'RAW','L1',1,'KHONG-NAP-GH','v1.0','v1.0','v1.0',"
            " false,'{}'::jsonb,'VND',1,'UNMAPPED') RETURNING itl_id",
            (uuid.uuid4().hex,))
        la = cur.fetchone()[0]
    ma, _ = _goi(may, f"{V}/queue/{la}/pm-candidates")
    assert ma == 404


# ─────────────────────────────────────────── duong GHI /match
def test_ghep_qua_HTTP__va_SO_khong_doi_mot_o(may, du_lieu):
    i = du_lieu["itl"]
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        truoc = c.execute("SELECT hd, cdt1, work_status, pm_hinh FROM fls_itl"
                          " WHERE itl_id=%s", (i,)).fetchone()
    ma, r = _goi(may, f"{V}/queue/{i}/match", pt="POST",
                 than={"pm_line_ids": ["PMS1-1"], "reason": "ghep tay F01"})
    assert ma == 200, r
    d = r["data"]
    assert d["moi_noi"] == [{"pm_line_id": "PMS1-1", "amount": "1000000.00",
                             "hinh": "T"}]
    assert {x["field"] for x in d["but_toan"]} == {"hd", "cdt1"}
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT hd, cdt1, work_status, pm_hinh FROM fls_itl"
                         " WHERE itl_id=%s", (i,)).fetchone() == truoc, \
            "⛔⛔ `fls_itl` BI DOI — ghep phai la THEM, khong SUA"


def test_ghep_de_lai_VET_co_actor_TU_THE(may, du_lieu):
    ma, _ = _goi(may, f"{V}/queue/{du_lieu['itl']}/match", pt="POST",
                 than={"pm_line_ids": ["PMS1-1"], "reason": "ghep tay F01"})
    assert ma == 200
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        r = c.execute("SELECT evt_type, actor, reason FROM fls_queue_event"
                      " WHERE itl_id=%s", (du_lieu["itl"],)).fetchone()
    assert r[0] == "match"
    assert r[1] == AI, "actor phai den TU THE"
    assert "ghep tay 1 dong lenh" in r[2]


def test_gui_actor_trong_THAN_bi_chan_400(may, du_lieu):
    """`actor` den tu THE. Gui trong than ⇒ **400**, ⛔ khong am tham bo qua."""
    ma, _ = _goi(may, f"{V}/queue/{du_lieu['itl']}/match", pt="POST",
                 than={"pm_line_ids": ["PMS1-1"], "reason": "x",
                       "actor": "ai-khac@apero.vn"})
    assert ma == 400


def test_gui_ma_PHIEU_thay_vi_ma_DONG_thi_400_kem_ly_do(may, du_lieu):
    """⛔⛔ `BA-07` §2 viet `{pm_id}` — ghep vao mot PHIEU. So lieu lat cau do:
    526 phieu mang 2–36 reference KHAC NHAU ⇒ ghep vao phieu thi MAY phai tu
    chon dong nao, tuc may quyet thay nguoi (`INV-I16`). Sua dac ta: `CR#6`."""
    ma, r = _goi(may, f"{V}/queue/{du_lieu['itl']}/match", pt="POST",
                 than={"pm_id": "PMS1", "reason": "x"})
    assert ma == 400
    # ⚠ `error.message` la mo ta CANH cua ma loi (*"tham so sai"*); cau chi tiet
    # nam o `error.detail` — de man hinh hien duoc cau nao thi tuy no chon.
    assert "pm_line_ids" in r["error"]["detail"]


def test_Σ_lech_thi_422_va_KHONG_ghi_gi(may, du_lieu):
    i = du_lieu["itl"]
    ma, r = _goi(may, f"{V}/queue/{i}/match", pt="POST",
                 than={"pm_line_ids": ["PMS1-1", "PMS2-1"],
                       "reason": "ghep hai dong"})
    assert ma == 422, r
    assert r["error"]["khac"]["tong_lenh"] == "2000000.00"
    assert r["error"]["khac"]["tien_bank"] == "1000000.00"
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("select count(*) from fls_pm_link where itl_id=%s",
                         (i,)).fetchone()[0] == 0
        assert c.execute("select count(*) from fls_queue_event where itl_id=%s",
                         (i,)).fetchone()[0] == 0


def test_ghep_LAN_HAI_thi_409_kem_moi_noi_dang_co(may, du_lieu):
    i = du_lieu["itl"]
    assert _goi(may, f"{V}/queue/{i}/match", pt="POST",
                than={"pm_line_ids": ["PMS1-1"], "reason": "lan 1"})[0] == 200
    ma, r = _goi(may, f"{V}/queue/{i}/match", pt="POST",
                 than={"pm_line_ids": ["PMS2-1"], "reason": "lan 2"})
    assert ma == 409, r
    assert r["error"]["khac"]["moi_noi"][0]["pm_line_id"] == "PMS1-1"


def test_thieu_ly_do_thi_400(may, du_lieu):
    ma, _ = _goi(may, f"{V}/queue/{du_lieu['itl']}/match", pt="POST",
                 than={"pm_line_ids": ["PMS1-1"]})
    assert ma == 400


def test_khong_co_THE_thi_401(may, du_lieu):
    ma, _ = _goi(may, f"{V}/queue/{du_lieu['itl']}/match", pt="POST",
                 than={"pm_line_ids": ["PMS1-1"], "reason": "x"},
                 co_the=False)
    assert ma == 401


def test_cua_CHI_DOC_thi_duong_ghep_tra_405(may_chi_doc, du_lieu):
    """⭐ Mac dinh cua ⛔ khong mo nhom ghi — phai go `--cho-ghi` tuong minh."""
    ma, _ = _goi(may_chi_doc, f"{V}/queue/{du_lieu['itl']}/match", pt="POST",
                 than={"pm_line_ids": ["PMS1-1"], "reason": "x"})
    assert ma == 405
    # ...nhung duong DOC ung vien van chay.
    assert _goi(may_chi_doc,
                f"{V}/queue/{du_lieu['itl']}/pm-candidates")[0] == 200
