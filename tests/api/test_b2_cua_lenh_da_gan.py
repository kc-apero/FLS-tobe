# -*- coding: utf-8 -*-
"""`B2` — ⭐⭐ Cua lenh chi **DA GAN** (tuyen 40) — `GAP-API-08`.

⛔⛔ `/queue/lenh-cho` loc cung `NOT EXISTS (fls_moi_noi)` ⇒ no **chi** tra
   dong **chua noi**. Suot chang `B3`, `khuon_the_lenh` doc `r["da_gan"]` ma
   ⛔ **khong cua nao sinh khoa ay** ⇒ `trang_thai` **vinh vien**
   `'chua_gan'`, va ca nua *"da gan"* cua man chet theo day chuyen:

     · nhan *"Doi sang giao dich da chon"*  ⛔ khong bao gio hien
     · nut *"Bo gan"*                       ⛔ khong bao gio bat
     · `.mrow.da_gan`                       CSS **chet**
     · `lenh_ke_tiep`                       ⛔ khong bo qua duoc dong nao

⭐⭐⭐ **Va `itl_id_da_gan` SO IT la SAI.** Do `22/09` tren kho THAT:

     lenh chi da gan                      2.219
     lenh chi chua gan                    1.553   (khep ve 3.772 ✔)
     ⭐ lenh gan NHIEU HON MOT dong tien     23  = **1,0%**

   Mot khoa so it se **im lang bo mat** moi noi thu hai o **23** lenh — dung
   o cho nguoi ta bam `Bo gan`. ⇒ Truong phai la mot **DANH SACH**.

⭐ `1,0%` gan dung `1,1%` ca co chum: **cung mot su that** *(tien va lenh la
  quan he nhieu ↔ nhieu)* nhin tu hai phia.

⚠ Bai nay **tu dung du lieu** trong kho `fls_test` — con so `2.219`/`23` o
  tren la phep do tren kho THAT, ⛔ khong phai thu bai nay khang dinh.
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
from fls.repo import lenh_cho as lc
from fls.repo import man_ghep as mg
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.pham_vi import chi_nap_that, mot_lan_nap

pytestmark = pytest.mark.pg

DSN = dsn_test()
ACTOR = "b2-da-gan@fls"
LY_DO = "bai thu B2 — cua lenh da gan"


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    r = "NAP-2000-01-01-D" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong_bank(conn, run: str, tien: str, curr: str = "VND") -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-D',%s,%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, curr,
         D(tien))).fetchone()[0]


def _lenh(conn, run: str, *ma: str) -> None:
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(10 + i, m.split("-")[0], m, D("1000000.00"), "VND", "Approve",
               None, "FNS | Facilities", "SHQ2 | HQ2", ref_tho=None)
        for i, m in enumerate(ma)])


@pytest.fixture()
def kho(conn):
    """⭐ BA dong lenh, ba trang thai khac nhau — de bai do duoc **ca ba**:

      `PM-CHUA`  ⛔ chua gan
      `PM-MOT`   da gan **mot** dong tien
      `PM-HAI`   da gan **HAI** dong tien  ← ly do truong phai la danh sach
    """
    run = _run(conn)
    _lenh(conn, run, "PM-CHUA", "PM-MOT", "PM-HAI")
    pv = mot_lan_nap(run)
    i1 = _dong_bank(conn, run, "1000000.00")
    i2 = _dong_bank(conn, run, "1000000.00")
    i3 = _dong_bank(conn, run, "1000000.00")
    gt.ghep_lenh(conn, pv, i1, ["PM-MOT"], actor=ACTOR, reason=LY_DO)
    gt.ghep_lenh(conn, pv, i2, ["PM-HAI"], actor=ACTOR, reason=LY_DO)
    gt.ghep_lenh(conn, pv, i3, ["PM-HAI"], actor=ACTOR, reason=LY_DO)
    return {"run": run, "pv": pv, "i": {"mot": i1, "hai": sorted([i2, i3])}}


# ── ⓐ ⭐⭐⭐ `itl_da_gan` la mot DANH SACH ──────────────────────────────

def test_khuon_the_sinh_DANH_SACH_chu_KHONG_mot_so():
    r = {"pm_line_id": "PM1-1", "amount": "40.00", "curr": "EUR",
         "cdt1": "COR | X", "ref_tho": None, "tho": {},
         "itl_da_gan": [42, 77]}
    t = mg.khuon_the_lenh(r)
    assert t["itl_da_gan"] == [42, 77], (
        "⛔⛔ Mot khoa SO IT bo mat moi noi thu hai o **23** lenh chi")
    assert t["trang_thai"] == "da_gan"
    assert "itl_id_da_gan" not in t, (
        "⛔ Ten SO IT phai bien mat han — giu ca hai la giu **hai ban su that**")


def test_chua_gan_thi_danh_sach_RONG_chu_KHONG_thieu_khoa():
    """⭐ `[]` la mot **CAU TRA LOI** *(⛔ chua gan gi)*; thieu khoa la
    *"FLS ⛔ khong biet"*. Hai cau khac nhau — `INV-I16`."""
    t = mg.khuon_the_lenh({"pm_line_id": "PM1-1", "tho": {}})
    assert t["itl_da_gan"] == [] and t["trang_thai"] == "chua_gan"


# ── ⓑ ⭐⭐ Cua tra DUNG ro ─────────────────────────────────────────────

def test_cua_tra_DUNG_hai_dong_da_gan(conn, kho):
    t = lc.doc_lenh_da_gan(conn, kho["pv"], limit=500)
    ma = sorted(d["pm_line_id"] for d in t.dong)
    assert ma == ["PM-HAI", "PM-MOT"], f"⛔ ro DA GAN sai: {ma}"


def test_lenh_gan_HAI_dong_tien_tra_DU_CA_HAI(conn, kho):
    """⭐⭐ Day la ly do truong phai la **danh sach**: mot con so se im lang
    bo mat moi noi thu hai, dung o cho nguoi ta bam `Bo gan`."""
    t = lc.doc_lenh_da_gan(conn, kho["pv"], limit=500)
    d = {x["pm_line_id"]: x for x in t.dong}
    assert sorted(d["PM-HAI"]["itl_da_gan"]) == kho["i"]["hai"]
    assert d["PM-MOT"]["itl_da_gan"] == [kho["i"]["mot"]]


def test_HAI_ro_KHONG_giao_nhau_va_KHEP_ve_TONG(conn, kho):
    """⛔⛔ Hai ro chong nhau thi mot dong hien **hai lan** o chip `Tat ca`,
    va **⛔ khong ai cong duoc**."""
    da = {d["pm_line_id"] for d in lc.doc_lenh_da_gan(conn, kho["pv"],
                                                      limit=500).dong}
    chua = {d["pm_line_id"] for d in lc.doc_lenh_cho(conn, kho["pv"],
                                                     limit=500).dong}
    assert not (da & chua), f"⛔⛔ **{len(da & chua)}** dong nam o CA HAI ro"
    assert da | chua == {"PM-CHUA", "PM-MOT", "PM-HAI"}, (da, chua)


def test_the_cua_dong_DA_GAN_doc_ra_dung_trang_thai(conn, kho):
    t = lc.doc_lenh_da_gan(conn, kho["pv"], limit=500)
    for d in t.dong:
        the = mg.khuon_the_lenh(d)
        assert the["trang_thai"] == "da_gan"
        assert the["trang_thai_nhan"] == "Đã gán"
        assert the["itl_da_gan"], f"⛔ {d['pm_line_id']} o ro DA GAN ma rong"


# ── ⓒ ⭐ LAT TRANG ────────────────────────────────────────────────────

def test_LAT_TRANG_di_het_chu_KHONG_bo_dong_nao(conn, kho):
    """⛔ Con tro la `pm_line_id` — khoa DON, vi thu tu o ro nay la
    `(pm_line_id)`. ⚠ ⛔ Khong dung `(curr, hang)` nhu `doc_lenh_cho`: ro nay
    ⛔ khong co thu hang theo tien *(no ⛔ khong phai mot hang doi viec)*."""
    ma, ct = [], None
    while True:
        t = lc.doc_lenh_da_gan(conn, kho["pv"], con_tro=ct, limit=1)
        ma += [d["pm_line_id"] for d in t.dong]
        ct = t.con_tro
        if not ct:
            break
    assert sorted(ma) == ["PM-HAI", "PM-MOT"], ma


# ── ⓓ ⭐ Cua HTTP co that ─────────────────────────────────────────────

def test_tuyen_40_co_trong_BANG_TUYEN():
    from fls.api import bang_tuyen as bt
    d = [t for t in bt.BANG_TUYEN if t.duong.endswith("/queue/lenh-da-gan")]
    assert len(d) == 1, "⛔ tuyen `lenh-da-gan` ⛔ chua khai o `BANG_TUYEN`"
    assert d[0].phuong_thuc == "GET"
    assert not getattr(d[0], "ghi", False), "⛔ cua DOC ⛔ khong duoc mo duong ghi"
    assert set(d[0].bang) >= {"fls_pm_line", "fls_moi_noi"}, d[0].bang
