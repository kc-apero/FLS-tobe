"""⛔ CONG RA cua `B4` — ca vong `F01` chay THAT qua HTTP.

`DEV-12` §4 khai cong ra cua buoc nay bang **hai cau**, va day la hai cau do:

  ⓐ *"ghep → bo ghep → ghep lai **cung mot dong lenh** (`lan 2`) chay tron"*
  ⓑ *"bam **Xong** thi dong **roi hang cho ngay**, bam **Mo lai** thi **quay
     ve**"*

⛔⛔ **Vi sao phai la MOT bai di tron vong, ⛔ khong phai bon bai le.** Tang kho
da co bai cho tung manh *(`test_bo_moi_noi_pg`, `test_da_xong_pg`,
`test_ghep_lenh_pg`)* va tat ca deu xanh. Nhung cau hoi cua man hinh la khac:
*"sau khi bo, dong ay co **quay lai hang cho** khong — va co **ghep lai duoc**
khong"*. Do la mot cau hoi **ve chuoi**, va mot chuoi ⛔ khong duoc chung minh
bang cach kiem tung mat xich.

★ ⛔ Khoa cu `(itl_id, pm_line_id)` **chan dung viec pho bien nhat sau khi go**:
  ghep lai chinh dong lenh vua go. `QĐ-ITL-69` doi khoa de dem **LAN**; bai ⓐ o
  day la cho no phai chung minh dieu do — tren duong HTTP that.
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

KHOA = "khoa-thu-vong-f01-dai-hon-ba-muoi-hai-ky-tu-that"
AI = "lan@apero.vn"
V = cua.bang_tuyen.TIEN_TO


@pytest.fixture()
def du_lieu():
    """Mot dong bank **1.000.000 VND** + mot dong lenh **dung bang** so do.

    ⚠ 1.000.000 chu ⛔ khong 100: dung sai VND la **1.000 tuyet doi**
    (`QĐ-ITL-57`), nen tren mot dong bank nho thi phep kiem Σ xanh SAI.
    """
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        tt = "V" + uuid.uuid4().hex[:5].upper()   # ⛔ tien te RIENG
        run = f"NAP-2000-01-01-VF{uuid.uuid4().hex[:6].upper()}"
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, doc_no, curr, ps_co,"
            " work_status, doc_date) VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0',"
            "'v1.0',false,'{}'::jsonb,'FT-VONG-F01',%s,%s,'UNMAPPED',"
            "'2026-08-01') RETURNING itl_id",
            (uuid.uuid4().hex, run, tt, D("1000000.00")))
        itl = cur.fetchone()[0]
        chen_dong_pm(c, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
            DongPM(11, "PMV1", "PMV1-1", D("1000000.00"), tt, "Approve",
                   "FTVONGF01", "HD-1", "CDT-1", ref_tho="FT-VONG-F01"),
        ])
    return {"run": run, "itl": itl, "tt": tt}


@contextlib.contextmanager
def _may():
    @contextlib.contextmanager
    def mo_doc():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    @contextlib.contextmanager
    def mo_ghi():
        conn = psycopg.connect(dsn_test(), autocommit=True)
        try:
            yield conn
        finally:
            conn.close()

    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = None
    try:
        m = cua.dung_may(mo_doc, cong=0, mo_ghi=mo_ghi)
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
    with _may() as m:
        yield m


def _goi(may, duong, *, pt="GET", than=None):
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de = {"Authorization": "Bearer " + the.dong_the(
        {"sub": AI, "exp": int(time.time()) + 300}, KHOA.encode())}
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


def _trong_hang_cho(may, itl, tt) -> bool:
    """⛔ Hoi CHINH cua ma man hinh doc, ⛔ khong hoi thang kho."""
    ma, r = _goi(may, f"{V}/queue?curr={tt}&limit=500")
    assert ma == 200
    return any(x["itl_id"] == itl for x in r["data"]["rows"])


def _so_moi_noi(may, itl) -> int:
    ma, r = _goi(may, f"{V}/ledger/{itl}")
    assert ma == 200
    return len(r["data"].get("moi_noi") or [])


# ══ ⓐ GHEP → BO GHEP → GHEP LAI DUNG DONG LENH CU (lan 2) ═══════════════
def test_vong_ghep_bo_ghep_lai_chay_TRON(may, du_lieu):
    itl = du_lieu["itl"]

    # ① ung vien phai co dong lenh kia
    ma, r = _goi(may, f"{V}/queue/{itl}/pm-candidates")
    assert ma == 200
    uv = r["data"]["ung_vien"]
    assert any(u["pm_line_id"] == "PMV1-1" for u in uv), \
        f"⛔ ⛔ khong thay dong lenh trong ung vien: {uv}"

    # ② ghep lan 1
    ma, r = _goi(may, f"{V}/queue/{itl}/match", pt="POST",
                 than={"pm_line_ids": ["PMV1-1"], "reason": "ghep tay"})
    assert ma == 200, r
    assert _so_moi_noi(may, itl) == 1

    # ③ bo CA CHUM
    ma, r = _goi(may, f"{V}/queue/{itl}/unmatch", pt="POST",
                 than={"reason": "ghep nham"})
    assert ma == 200, r
    assert (r["data"].get("da_bo") or []), "⛔ cua ⛔ khong khai da bo gi"
    assert _so_moi_noi(may, itl) == 0

    # ④ ⭐⭐ GHEP LAI **dung dong lenh vua go** — day la cho khoa CU se chan.
    ma, r = _goi(may, f"{V}/queue/{itl}/match", pt="POST",
                 than={"pm_line_ids": ["PMV1-1"], "reason": "ghep tay"})
    assert ma == 200, (
        f"⛔ ghep lai dung dong lenh vua go BI CHAN ({ma}) — do la viec pho "
        f"bien nhat sau khi go, va `QĐ-ITL-69` doi khoa chinh de cho phep no")
    assert _so_moi_noi(may, itl) == 1

    # ⑤ va no phai la **LAN 2**, ⛔ khong phai mot moi noi trong nhu lan dau
    ma, r = _goi(may, f"{V}/ledger/{itl}")
    lan = [n.get("lan") for n in r["data"]["moi_noi"]]
    assert 2 in lan, f"⛔ ⛔ khong dem duoc LAN ghep: {lan}"


def test_bo_ghep_LE_bi_chan_400(may, du_lieu):
    """⛔ Bo le lam `Σ moi noi != tien bank` — tao ra dung trang thai sai ma
    cong `SIGMA_MOI_NOI` dung ra de bat."""
    itl = du_lieu["itl"]
    _goi(may, f"{V}/queue/{itl}/match", pt="POST",
         than={"pm_line_ids": ["PMV1-1"], "reason": "ghep tay"})
    ma, r = _goi(may, f"{V}/queue/{itl}/unmatch", pt="POST",
                 than={"reason": "x", "pm_line_ids": ["PMV1-1"]})
    assert ma == 400
    assert "toan bo" in (r["error"].get("detail") or "").lower() \
        or "TOAN BO" in (r["error"].get("detail") or "")


# ══ ⓑ XONG ⇒ ROI HANG CHO · MO LAI ⇒ QUAY VE ════════════════════════════
def test_xong_thi_ROI_hang_cho_va_mo_lai_thi_QUAY_VE(may, du_lieu):
    itl = du_lieu["itl"]
    assert _trong_hang_cho(may, itl, du_lieu["tt"]), "⛔ dong moi nap phai nam trong hang cho"

    ma, r = _goi(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    assert ma == 200, r
    assert not _trong_hang_cho(may, itl, du_lieu["tt"]), \
        "⛔ bam xong ma dong VAN nam trong hang cho — `GAP-JOIN-06` quay lai"

    ma, r = _goi(may, f"{V}/queue/{itl}/reopen", pt="POST",
                 than={"reason": "bam nham"})
    assert ma == 200, r
    assert _trong_hang_cho(may, itl, du_lieu["tt"]), "⛔ mo lai ma dong ⛔ khong quay ve"


def test_bam_XONG_hai_lan_khong_thanh_hai_su_kien(may, du_lieu):
    """⭐ Tra ve **ai da bam va luc nao**, ⛔ khong bao loi — man hinh hien
    *"da xong boi X"* thay vi mot cau do."""
    itl = du_lieu["itl"]
    _goi(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    ma, r = _goi(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    assert ma == 200
    assert r["data"]["da_co"] is True
    assert r["data"].get("boi") == AI
    assert r["data"].get("luc")


def test_mo_lai_KHONG_co_ly_do_thi_bi_chan(may, du_lieu):
    """⚠ Khac nut `Xong` — keo lai la **lat ket luan cua nguoi khac**."""
    itl = du_lieu["itl"]
    _goi(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    ma, _ = _goi(may, f"{V}/queue/{itl}/reopen", pt="POST", than={})
    assert ma == 400


def test_mo_lai_mot_dong_CHUA_TUNG_xong_thi_409(may, du_lieu):
    ma, _ = _goi(may, f"{V}/queue/{du_lieu['itl']}/reopen", pt="POST",
                 than={"reason": "x"})
    assert ma in (409, 400)


# ══ ⓒ dong da XONG cung bien khoi phep DO PHU ═══════════════════════════
def test_dong_da_xong_bien_khoi_ca_do_phu_va_chan_man(may, du_lieu):
    """⛔ Ba cho khai cung mot luat *(danh sach · dem · do phu)* thi chung phai
    **cung doi** — ⛔ khong thi man hinh se noi *"con N dong"* tren mot danh
    sach do dai khac."""
    itl = du_lieu["itl"]

    def _dem():
        ma, r = _goi(may, f"{V}/queue/summary")
        assert ma == 200
        return sum(x["so_dong"] for x in r["data"]["theo_tien_te"]
                   if x["curr"] == du_lieu["tt"])

    def _phu():
        ma, r = _goi(may, f"{V}/queue/coverage")
        assert ma == 200
        return sum(x["so_dong_cho"] for x in r["data"]["theo_tien_te"]
                   if x["curr"] == du_lieu["tt"])

    truoc_dem, truoc_phu = _dem(), _phu()
    _goi(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    assert _dem() == truoc_dem - 1
    assert _phu() == truoc_phu - 1


# ══ ⓓ cua CHI DOC: moi nut ghi phai tra 405 ═════════════════════════════
def test_che_do_chi_doc_thi_moi_duong_ghi_tra_405(du_lieu):
    """⭐ Man hinh doc co nay tu `phien.js` va **lam mo nut TRUOC**, ⛔ khong de
    ke toan bam roi moi bao."""
    @contextlib.contextmanager
    def mo_doc():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = None
    try:
        m = cua.dung_may(mo_doc, cong=0, mo_ghi=None)   # ⛔ CHI DOC
        threading.Thread(target=m.serve_forever, daemon=True).start()
        itl = du_lieu["itl"]
        for duong, than in ((f"{V}/queue/{itl}/done", {}),
                            (f"{V}/queue/{itl}/reason", {"reason": "x"}),
                            (f"{V}/queue/{itl}/match",
                             {"pm_line_ids": ["PMV1-1"]}),
                            (f"{V}/queue/{itl}/unmatch", {"reason": "x"})):
            ma, r = _goi(m, duong, pt="POST", than=than)
            assert ma == 405, f"⛔ {duong} tra {ma}, phai 405"
            assert r["error"]["code"] == "FLS-METHOD"
    finally:
        if m is not None:
            m.shutdown()
            m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


# ══ ⓔ ⛔⛔ TEN TRUONG man hinh dua vao PHAI co that ══════════════════════
#
# ⛔⛔ **Ba lan trong mot buoi, cung mot lop loi.** Man `F01` doc `xong_boi` /
# `xong_luc` *(dung nhu `BA-06` §8 ghi)* nhung cua tra `boi`/`luc`; quen gui
# `reason` *(§8 ⛔ khong nhac, cua thi DOI)*; va doc `cursor` trong khi cua tra
# **`next_cursor`** — cai cuoi lam nut *"Xem them"* ⛔ **khong bao gio hien**,
# tuc man hinh trong nhu **het danh sach** trong khi con 2.937 dong.
#
# ★ Ca ba deu **im lang**: ⛔ khong loi, ⛔ khong canh bao, chi la mot o rong hay
#   mot nut vang mat. Va ⛔ khong cong nao cu bat duoc — `soi_bang_tuyen` canh
#   *bang nao bi cham*, ⛔ khong canh *ten truong trong phan hoi*.
# ⇒ Ghim tung ten, tren phan hoi THAT (`GAP-SPEC-02`).
def _khoa(may, duong, **kw):
    ma, r = _goi(may, duong, **kw)
    assert ma == 200, r
    return r["data"]


def test_ten_truong_man_hinh_dua_vao_deu_CO_THAT(may, du_lieu):
    itl, tt = du_lieu["itl"], du_lieu["tt"]

    d = _khoa(may, f"{V}/queue?curr={tt}&limit=50")
    assert {"rows", "next_cursor"} <= set(d), (
        "⛔ man hinh doc `rows` + `next_cursor` — doc nham `cursor` thi nut "
        "'Xem them' ⛔ khong bao gio hien")
    assert {"itl_id", "doc_no", "memo", "tien", "hang", "luy_ke_pct", "le",
            "reason", "defer_until", "defer_count"} <= set(d["rows"][0])

    d = _khoa(may, f"{V}/queue/summary")
    assert "theo_tien_te" in d and "tong" not in d
    assert {"curr", "so_dong", "tien"} <= set(d["theo_tien_te"][0])

    d = _khoa(may, f"{V}/queue/{itl}/pm-candidates")
    assert {"dong_so", "ung_vien", "dung_sai", "anh_chup",
            "khong_xep_duoc_theo", "vi_sao"} <= set(d)
    assert {"pm_line_id", "amount", "bac", "status", "da_ghep"} \
        <= set(d["ung_vien"][0])

    d = _khoa(may, f"{V}/queue/{itl}/match", pt="POST",
              than={"pm_line_ids": ["PMV1-1"], "reason": "x"})
    assert {"khong_suy_duoc", "tien_bank", "tong_lenh", "dung_sai"} <= set(d)

    d = _khoa(may, f"{V}/queue/{itl}/unmatch", pt="POST", than={"reason": "x"})
    assert {"da_bo", "but_toan_dao", "bo_qua", "ve_hang_cho"} <= set(d)

    _goi(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    d = _khoa(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    # ⚠ `boi`/`luc` — ⛔ KHONG `xong_boi`/`xong_luc` nhu `BA-06` §8 ghi.
    assert {"da_co", "boi", "luc", "thieu_truong", "ky_da_chot"} <= set(d)
    assert "xong_boi" not in d, (
        "⛔ neu cua doi sang `xong_boi` thi man hinh phai doi theo — va `BA-06` "
        "§8 luc do moi dung (`GAP-SPEC-02`)")


def test_moi_thao_tac_ghi_TRU_xong_deu_DOI_ly_do(may, du_lieu):
    """⚠ Cua doi `reason` o **5/6** thao tac; chi `Xong` la tuy y
    (`QĐ-ITL-72`). `BA-06` §8 ⛔ khong noi mot chu nao ve dieu nay."""
    itl = du_lieu["itl"]
    doi = [(f"{V}/queue/{itl}/reason", {}),
           (f"{V}/queue/{itl}/defer", {"until": "2026-12-31"}),
           (f"{V}/queue/{itl}/match", {"pm_line_ids": ["PMV1-1"]})]
    for duong, than in doi:
        ma, r = _goi(may, duong, pt="POST", than=than)
        assert ma == 400 and "reason" in (r["error"].get("detail") or ""), \
            f"⛔ {duong} phai DOI `reason`, nhung tra {ma}"
    # ⭐ `Xong` thi ⛔ KHONG doi — bat ly do cho thao tac pho bien nhat la mot
    #   ma sat ⛔ khong thu duoc gi (nguoi ta se go bua mot chu roi bam).
    ma, _ = _goi(may, f"{V}/queue/{itl}/done", pt="POST", than={})
    assert ma == 200
