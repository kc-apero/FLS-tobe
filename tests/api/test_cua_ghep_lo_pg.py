"""Cua **GHEP LO** chay THAT qua HTTP (`B2`, `QĐ-ITL-118`).

⛔⛔ **Vi sao cua nay ⛔ KHONG nhan `pm_line_ids`, va do la ca thiet ke.**

Cua ghep TAY (`POST /queue/{itl_id}/match`) nhan danh sach dong lenh **vi
nguoi da chon**. Cua LO ⛔ khong co nguoi chon — nen neu no cung nhan danh sach
thi mot cu bam se thanh **N phep ghep tay ⛔ khong ai xem**, va cai nhan "tu
chung" bien thanh "tin loi nguoi goi". ⇒ Than yeu cau **chi** co `itl_ids` +
`reason`; may **do lai phia may chu** (`ds_tu_chung`) roi ghep dung cai no do.

★ Va cung khuon `422 CA LO` voi cua khai thu tu LO: mot dong ⛔ khong tu chung
⇒ **⛔ 0 moi noi moi**. Bai `test_MOT_dong_xau_lam_CA_LO_khong_ghi_gi` do dieu
do bang cach **dem `fls_pm_link` truoc va sau**, ⛔ khong bang cach doc ma tra
ve — mot cua co the tra `422` roi vẫn da ghi mot nua.
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

from fls.adapters.pm_join import canon_ref
from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc

pytestmark = pytest.mark.pg

KHOA = "khoa-thu-cua-ghep-LO-dai-hon-ba-muoi-hai-ky-tu-that"
AI = "ke.toan@apero.vn"
V = cua.bang_tuyen.TIEN_TO


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def du_lieu():
    """Bon dong: **hai TU CHUNG** *(1 dong lenh · chum 2 dong)* + **hai XAU**.

    ⚠ So tien **1.000.000** chu ⛔ khong 100: dung sai VND la **1.000 tuyet
    doi** (`QĐ-ITL-57`) nen tren mot dong nho, mot dong lenh lech vai tram
    **van** nam trong dung sai va bai *"lech thi tu choi"* se xanh SAI.
    """
    run = f"NAP-2000-01-01-GLO{_hex(6)}"
    r = {k: f"REF-{k}-{_hex(4)}" for k in
         ("mot", "chum", "lech", "chuaduyet")}
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        so = {}
        for n, (k, tien) in enumerate((("mot", 1_000_000),
                                       ("chum", 3_000_000),
                                       ("lech", 5_000_000),
                                       ("chuaduyet", 800_000))):
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
                " source_row, run_id, contract_version, canon_version,"
                " mapping_version, raw_frozen, canon, doc_no, curr, ps_co,"
                " work_status) VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0',"
                "'v1.0',false,'{}'::jsonb,%s,'VND',%s,'UNMAPPED')"
                " RETURNING itl_id",
                (uuid.uuid4().hex, 500 + n, run, r[k], D(tien)))
            so[k] = cur.fetchone()[0]

        def _pm(ref, tien, *, status="Approve"):
            pid = "PL" + _hex(10)
            cur.execute(
                "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                " ref_tho, ref_canon, amount, curr, status, source_row)"
                " VALUES (%s,%s,%s,%s,%s,%s,'VND',%s,%s)",
                (run, pid, "SL" + _hex(6), ref, canon_ref(ref), D(tien),
                 status, abs(hash(pid)) % 900000))
            return pid

        pm = {
            "mot": [_pm(r["mot"], 1_000_000)],
            # ⭐ Chum HAI dong cong lai dung tien bank ⇒ `ghep_lenh` nhan CA HAI
            "chum": sorted([_pm(r["chum"], 1_000_000),
                            _pm(r["chum"], 2_000_000)]),
            "lech": [_pm(r["lech"], 77)],
            "chuaduyet": [_pm(r["chuaduyet"], 800_000, status="Pending")],
        }
    return {"run": run, "so": so, "pm": pm}


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


@pytest.fixture()
def may():
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = None
    try:
        m = cua.dung_may(_mo_doc(), cong=0, mo_ghi=_mo_ghi())
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


def _goi(may, duong: str, *, pt: str = "GET", than: dict | None = None
         ) -> tuple[int, dict]:
    c = http.client.HTTPConnection(*may.server_address, timeout=20)
    de = {"Authorization": "Bearer " + the.dong_the(
        {"sub": AI, "exp": int(time.time()) + 300}, KHOA.encode())}
    body = json.dumps(than).encode() if than is not None else None
    if body is not None:
        de["Content-Type"] = "application/json"
    try:
        c.request(pt, duong, body=body, headers=de)
        rp = c.getresponse()
        d = rp.read()
        return rp.status, (json.loads(d) if d else {})
    finally:
        c.close()


def _dem_link(run: str) -> int:
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_pm_link WHERE run_id = %s",
                    (run,))
        return int(cur.fetchone()[0])


# ── duong DOC ───────────────────────────────────────────────────────────
def test_MAU_SO_bon_nhom_VE_va_moi_O_co_TEN(may, du_lieu):
    s, d = _goi(may, f"{V}/queue/mau-so?run_id={du_lieu['run']}")
    assert s == 200, d
    r = d["data"]
    assert [x["ve"] for x in r["ve"]] == ["ps_co", "ps_no", "ca_hai",
                                          "khong_ve_nao"]
    assert sum(x["so_dong"] for x in r["ve"]) == r["tong_dong"] == 4
    for x in r["nhan"] + r["vi_sao"]:
        assert x["ly_do"].strip() and x["ma"] not in ("khac", "")
    assert r["tu_chung"] == 2


def test_TU_CHUNG_ds_khai_ca_ly_do_TU_CHOI(may, du_lieu):
    """⛔ Man hinh chi thay *"2 dong ghep duoc"* ma ⛔ khong thay *"2 dong bi
    tu choi VI SAO"* la mot man hinh **an di phan viec con lai**."""
    s, d = _goi(may, f"{V}/queue/tu-chung?run_id={du_lieu['run']}")
    assert s == 200, d
    r = d["data"]
    assert {x["itl_id"] for x in r["tu_chung"]} == {du_lieu["so"]["mot"],
                                                   du_lieu["so"]["chum"]}
    ly = {x["itl_id"]: x["ly_do"] for x in r["khong"]}
    assert ly[du_lieu["so"]["lech"]] == "mot_dong_lech_tien"
    assert ly[du_lieu["so"]["chuaduyet"]] == "co_dong_chua_duyet"
    # ⭐ moi dong TU CHOI mang mot CAU tieng Viet — ⛔ khong chi mot ma
    for x in r["khong"]:
        assert x["cau"].strip()


# ── duong GHI ───────────────────────────────────────────────────────────
def test_ghep_LO_hai_hinh__mot_dong_va_CA_CHUM(may, du_lieu):
    ids = [du_lieu["so"]["mot"], du_lieu["so"]["chum"]]
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": ids, "reason": "bai kiem ghep LO"})
    assert s == 200, d
    r = d["data"]
    assert r["so_dong_yeu_cau"] == 2 and r["so_dong_da_ghep"] == 2
    # ⭐ **BA** moi noi tu **HAI** dong: chum mang hai dong lenh
    assert r["so_moi_noi"] == 3
    got = {x["itl_id"]: x["pm_line_ids"] for x in r["dong"]}
    assert got[du_lieu["so"]["chum"]] == du_lieu["pm"]["chum"]
    for x in r["dong"]:
        assert x["tien_bank"] == x["tong_lenh"], x
    assert _dem_link(du_lieu["run"]) == 3


def test_MOT_dong_xau_lam_CA_LO_khong_ghi_gi(may, du_lieu):
    """⛔⛔ Do bang cach **dem kho truoc/sau**, ⛔ khong bang cach doc ma tra ve.

    Mot cua co the tra `422` roi **van** da ghi mot nua — va do dung la trang
    thai ⛔ khong ai doc duoc ma cua LO ra doi de tranh.
    """
    truoc = _dem_link(du_lieu["run"])
    ids = [du_lieu["so"]["mot"], du_lieu["so"]["chum"],
           du_lieu["so"]["lech"]]
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": ids, "reason": "bai kiem tu choi ca lo"})
    assert s == 422, d
    assert d["error"]["code"] == "FLS-GHEP-KHONG-TU-CHUNG"
    ly = {x["itl_id"]: x["ly_do"] for x in d["error"]["khac"]["dong"]}
    assert ly == {du_lieu["so"]["lech"]: "mot_dong_lech_tien"}
    assert d["error"]["khac"]["so_dong_xau"] == 1
    assert _dem_link(du_lieu["run"]) == truoc


def test_than_KHONG_nhan_pm_line_ids(may, du_lieu):
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": [du_lieu["so"]["mot"]],
                      "pm_line_ids": du_lieu["pm"]["mot"], "reason": "x"})
    assert s == 400, d
    assert "pm_line_ids" in d["error"]["detail"]


def test_cua_LO_KHONG_BAO_GIO_nhan_force(may, du_lieu):
    """⭐⭐ `force` la cach nguoi ghi de ket luan cua may cho **MOT** dong co ly
    do cu the. Rai no len ca lo la **bo cong duyet cho N dong bang mot cu bam**.
    """
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": [du_lieu["so"]["chuaduyet"]],
                      "force": True, "reason": "x"})
    assert s == 400, d
    assert "force" in d["error"]["detail"]


def test_than_RONG_hay_thieu_ly_do_bi_tu_choi(may, du_lieu):
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": [], "reason": "x"})
    assert s == 400, d
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": [du_lieu["so"]["mot"]]})
    assert s == 400, d
    assert "reason" in d["error"]["detail"]


@pytest.mark.parametrize("than_ly_do", [{}, {"reason": ""}, {"reason": "   "}])
def test_cua_LO_thieu_ly_do_VAN_400__du_cu_Ghep_tren_man_da_tuy_y(
        may, du_lieu, than_ly_do):
    """⭐⭐ `WO-003 AC-3` — `BA-07` v3.4 `§4h ⓼`: `match` + `unmatch` nhận thiếu
    lý do *(owner: "bỏ yêu cầu lý do cho cú Ghép")*, nhưng cửa **LÔ** **GIỮ**
    bắt buộc — ⛔ có người chọn dòng *(`§4g ⓓ`)*.

    ⚠ Vì sao bài này cần riêng: từ `WO-003` tầng repo `ghep_lenh` **tự điền**
      lý do mặc định khi rỗng ⇒ nới `_chu(..., "reason")` ở cửa lô là cú bấm
      LÔ **đi qua êm** *(lý do `" · ghep LO…"` ⛔ rỗng)*. Phép chặn chỉ còn
      sống ở tầng cửa ⇒ đếm `fls_pm_link` trước/sau: ⛔ một mối nối nào.
    """
    truoc = _dem_link(du_lieu["run"])
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": [du_lieu["so"]["mot"]], **than_ly_do})
    assert s == 400, d
    assert "reason" in d["error"]["detail"]
    assert _dem_link(du_lieu["run"]) == truoc, "⛔ cửa LÔ thiếu lý do mà vẫn GHI"


def test_dong_NGOAI_pham_vi_bi_TU_CHOI_khong_im_lang_bo_qua(may, du_lieu):
    """⛔ Mot `itl_id` ⛔ khong co that PHAI lam ca lo do — ⛔ khong bi loc bo
    trong im lang roi bao *"da ghep 1 dong"*."""
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": [du_lieu["so"]["mot"], 10**15],
                      "reason": "bai kiem dong ngoai"})
    assert s == 422, d
    ly = {x["itl_id"]: x["ly_do"] for x in d["error"]["khac"]["dong"]}
    assert ly == {10**15: "ngoai_pham_vi_hay_da_noi"}


def test_ghep_LO_hai_lan__lan_hai_TU_CHOI_vi_da_noi(may, du_lieu):
    """⭐ Sau khi ghep, dong ay ⛔ khong con trong tap chua noi ⇒ lan hai `422`.

    ⛔ ⛔ Khong phai `200` voi *"0 dong"*: mot cu bam lai ma tra `200` se lam
    nguoi ta tuong no vua ghep them.
    """
    ids = [du_lieu["so"]["mot"]]
    s, _ = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": ids, "reason": "lan mot"})
    assert s == 200
    s, d = _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": ids, "reason": "lan hai"})
    assert s == 422, d
    assert d["error"]["khac"]["dong"][0]["ly_do"] == "ngoai_pham_vi_hay_da_noi"


# ── `B4` · duong LUI cua mot LO ─────────────────────────────────────────
def _dem_hieu_luc(run: str) -> int:
    """Moi noi **DANG HIEU LUC** — ⛔ khong phai so dong `fls_pm_link`.

    ⛔⛔ Dem tren `fls_pm_link` la dem **ca cac moi noi DA BO**: so chi-them
      nen phep bo la mot dong THEM, ⛔ khong phai mot cu xoa. ⇒ Mot bai dem
      `fls_pm_link` roi ket luan *"da bo xong"* se **XANH SAI mai mai**.
    """
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_moi_noi m JOIN fls_itl i"
                    " USING (itl_id) WHERE i.run_id = %s", (run,))
        return int(cur.fetchone()[0])


def test_LO_ghep_roi_LUI_HET__va_fls_pm_link_KHONG_mat_dong_nao(may, du_lieu):
    """⭐⭐⭐ `B4` cho mot **LO** — va ⛔ CHUA AI DI QUA nhanh nay.

    ⛔⛔⛔ **Vi sao bai nay phai ton tai.** Bai vong `test_vong_ghep_bo_ghep_
      lai_chay_TRON` di duong `/match` **LE**. Cua `/match-lo` tao **nhieu**
      moi noi trong **MOT** giao dich, va ⛔ chua mot bai nao chung minh chung
      lui lai duoc **het**. Luat cua chinh du an nay: *"mot nhanh ⛔ chua ai
      di qua la mot nhanh CHUA BIET CO CHAY"* — va tien le la duong
      `422 FLS-SOAT-CHAN`, no **NO** ngay lan dau co mot lo that.

    ⚠ Bai do tren **HAI** be mat, vi mot be mat ⛔ khong du:
      · `fls_moi_noi` *(hieu luc)* phai ve **0**;
      · `fls_pm_link` *(so goc)* phai **⛔ KHONG mat dong nao** — `INV-I08`.
    """
    so, run = du_lieu["so"], du_lieu["run"]
    lo = [so["mot"], so["chum"]]

    truoc_link = _dem_link(run)
    assert _dem_hieu_luc(run) == 0

    # ① ghep CA LO — `mot` (1 dong lenh) + `chum` (2 dong lenh) = 3 moi noi
    ma, r = _goi(may, f"{V}/queue/match-lo", pt="POST",
                 than={"itl_ids": lo, "reason": "lo tu chung"})
    assert ma == 200, r
    assert _dem_hieu_luc(run) == 3, "⛔ lo phai tao dung 3 moi noi"
    sau_ghep_link = _dem_link(run)
    assert sau_ghep_link == truoc_link + 3

    # ② LUI — bo tung dong (⛔ khong co cua bo-lo, va `§8` ⛔ khong doi co)
    for itl in lo:
        ma, r = _goi(may, f"{V}/queue/{itl}/unmatch", pt="POST",
                     than={"reason": "lui ca lo"})
        assert ma == 200, (itl, r)

    # ③ hieu luc ve 0 …
    assert _dem_hieu_luc(run) == 0, "⛔ con moi noi hieu luc sau khi lui het"
    # … va so goc ⛔ KHONG mat mot dong nao (`INV-I08`)
    assert _dem_link(run) >= sau_ghep_link, (
        "⛔⛔ `fls_pm_link` MAT dong sau khi bo ghep — so chi-them bi vi pham, "
        "va luc ay ⛔ khong ai truy duoc *ai da noi gi, luc nao*")


def test_LO_lui_het_roi_GHEP_LAI_duoc__va_la_LAN_2(may, du_lieu):
    """⭐ Sau khi lui, dung cai lo ay phai ghep lai duoc — do la viec **pho
    bien nhat** sau mot cu bo ghep, va `QĐ-ITL-69` doi khoa chinh cho phep no.

    ⚠ Va no phai la **lan 2**: mot moi noi moi trong y het lan dau se lam
      *"dong nay da bi noi may lan"* ⛔ khong tra loi duoc.
    """
    so, run = du_lieu["so"], du_lieu["run"]
    lo = [so["mot"], so["chum"]]

    for than in ({"itl_ids": lo, "reason": "lo lan 1"},):
        assert _goi(may, f"{V}/queue/match-lo", pt="POST", than=than)[0] == 200
    for itl in lo:
        assert _goi(may, f"{V}/queue/{itl}/unmatch", pt="POST",
                    than={"reason": "lui"})[0] == 200
    ma, r = _goi(may, f"{V}/queue/match-lo", pt="POST",
                 than={"itl_ids": lo, "reason": "lo lan 2"})
    assert ma == 200, r
    assert _dem_hieu_luc(run) == 3

    ma, r = _goi(may, f"{V}/ledger/{so['mot']}")
    lan = [n.get("lan") for n in r["data"]["moi_noi"]]
    assert 2 in lan, f"⛔ ⛔ khong dem duoc LAN ghep sau khi lui: {lan}"


def test_LUI_MOT_NUA_lo_thi_nua_kia_CON_NGUYEN(may, du_lieu):
    """⛔⛔ Mot lo la **N phep ghep doc lap**, ⛔ khong phai mot khoi.

    Bo `mot` thi `chum` phai **con nguyen 2 moi noi**. Neu phep bo ghep di
    theo `run_id` hay theo *"lo vua ghep"* thi no se keo ca `chum` di theo —
    va do la mot cu **mat du lieu im lang** ma so dong tong van trong hop ly.
    """
    so, run = du_lieu["so"], du_lieu["run"]
    assert _goi(may, f"{V}/queue/match-lo", pt="POST",
                than={"itl_ids": [so["mot"], so["chum"]],
                      "reason": "lo"})[0] == 200
    assert _dem_hieu_luc(run) == 3

    assert _goi(may, f"{V}/queue/{so['mot']}/unmatch", pt="POST",
                than={"reason": "chi bo mot"})[0] == 200
    assert _dem_hieu_luc(run) == 2, (
        "⛔ bo mot dong cua lo lam doi so moi noi cua dong KHAC")
