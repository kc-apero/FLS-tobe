"""Ba cua DOC **phia lenh chi** chay THAT qua HTTP (`GAP-SCR-14`).

⛔⛔⛔ **Bai dat nhat cua tep nay la `test_KHONG_them_mot_duong_GHI_nao`.**

`QĐ-ITL-122` doi **cau hoi** cua man ghep, ⛔ khong doi **duong ghi**. Cu ghep
van la `POST /queue/{itl_id}/match` — mot chuyen. Neu ai do them mot cua ghi
o phia lenh chi thi he se co **hai duong ghi** vao `fls_pm_link`, va tu do:

  · cong quet ma nguon *(chi-mot-cho-ghi-tay)* do — dung nhu no phai do;
  · nhung te hon: hai duong ghi se **lech nhau** ve bon cong cua `ghep_lenh`
    *(cung te · chua ghep · da duyet · Σ trong dung sai)*, va mot cua ghi de
    hon cua kia la mot **duong tat vong qua kiem tra** ⛔ khong ai thay.

⇒ Bai ay dem **so tuyen GHI** truoc va sau, va doi con so ⛔ **khong doi**.
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

KHOA = "khoa-thu-cua-LENH-CHO-dai-hon-ba-muoi-hai-ky-tu-that"
AI = "ke.toan@apero.vn"
V = cua.bang_tuyen.TIEN_TO


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def du_lieu():
    """Bon dong lenh: **khop · chua duyet · te khac · cung phieu**."""
    run = f"NAP-2000-03-01-LCH{_hex(6)}"
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        ref = "REF-LC-" + _hex(5)
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, doc_no, curr, ps_co,"
            " work_status) VALUES (%s,'RAW','L1',701,%s,'v1.0','v1.0','v1.0',"
            "false,'{}'::jsonb,%s,'VND',%s,'UNMAPPED') RETURNING itl_id",
            (uuid.uuid4().hex, run, ref, D(1_000_000)))
        itl = cur.fetchone()[0]

        def _pm(r, tien, *, status="Approve", te="VND", dong=1, slip=None):
            pid = "PL" + _hex(10)
            cur.execute(
                "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                " ref_tho, ref_canon, amount, curr, status, source_row)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (run, pid, slip or ("SL" + _hex(6)), r, canon_ref(r),
                 D(tien), te, status, dong))
            return pid

        pm = {
            "khop": _pm(ref, 1_000_000, dong=1),
            "chua_duyet": _pm("REF-P-" + _hex(4), 500_000,
                              status="Pending", dong=2),
            "te_khac": _pm("REF-U-" + _hex(4), 90, te="USD", dong=3),
        }
    return {"run": run, "itl": itl, "pm": pm, "ref": ref}


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


# ── ⭐⭐⭐ ⛔ KHONG duong GHI nao moi ────────────────────────────────────
def test_KHONG_them_mot_duong_GHI_nao(may):
    """⭐⭐⭐ **Bai dat nhat cua tep nay.**

    `QĐ-ITL-122` doi **cau hoi**, ⛔ khong doi **duong ghi**. Ba tuyen moi
    phai la **`GET` het**, va ⛔ khong tuyen nao trong so do khai `bang_ghi`.

    ⛔⛔ Hai duong ghi vao `fls_pm_link` se **lech nhau** ve bon cong cua
       `ghep_lenh` *(cung te · chua ghep · da duyet · Σ trong dung sai)*, va
       mot cua ghi **de hon** cua kia la mot **duong tat vong qua kiem tra**
       ⛔ khong ai thay.

    ⭐ **Con so `4` la mot DAY BAY, ⛔ khong phai luat.** Luat nam o vong `for`
      ben duoi *(GET het · ⛔ khong `bang_ghi`)*. Con so nay o day de mot tuyen
      moi **buoc nguoi them no phai mo bai nay ra doc** — va no da lam dung
      viec ay **hai lan trong mot ngay** `11/09`: `G2` them `/lenh-cho/ro`
      *(`3` → `4`)*, roi cua *"nhin du bang PM"* them `/queue/lenh/{id}`
      *(`4` → `5`)*.
      ⇒ Doi con so khi them mot tuyen **DOC** la dung. Doi no de cho qua mot
        tuyen **GHI** thi vong `for` se do — va no phai do.

    ⭐ **Lan thu ba, `21/09`** (`QĐ-ITL-148`): them `/queue/lenh/{id}/so`
      *(tra cuu TOAN SO — loi thoat ngo cut cua **768** dong)* ⇒ `5` → **`6`**.
      Van la `GET`, van ⛔ khong `bang_ghi`.
    """
    moi = [t for t in cua.bang_tuyen.BANG_TUYEN
           if "/lenh-cho" in t.duong or "/queue/lenh/" in t.duong]
    assert len(moi) == 6, [t.duong for t in moi]
    for t in moi:
        assert t.phuong_thuc == "GET", f"⛔ {t.duong} ⛔ khong phai GET"
        assert not getattr(t, "bang_ghi", ()) or t.bang_ghi == (), (
            f"⛔⛔ {t.duong} khai `bang_ghi` — day la duong GHI THU HAI")


# ── duong DOC ───────────────────────────────────────────────────────────
def test_LENH_CHO_xep_trong_TUNG_tien_te(may, du_lieu):
    s, d = _goi(may, f"{V}/queue/lenh-cho?run_id={du_lieu['run']}&limit=100")
    assert s == 200, d
    dong = d["data"]["rows"]
    assert dong, d
    theo = {}
    for r in dong:
        theo.setdefault(r["curr"], []).append(r["hang"])
    assert len(theo) >= 2
    for te, h in theo.items():
        assert h == list(range(1, len(h) + 1)), (te, h)


def test_MAC_DINH_hien_ca_dong_CHUA_DUYET(may, du_lieu):
    """⛔ An dong ⛔ chua duyet theo mac dinh la mot **mac dinh im lang**."""
    s, d = _goi(may, f"{V}/queue/lenh-cho?run_id={du_lieu['run']}&limit=100")
    assert s == 200
    ma = {r["pm_line_id"] for r in d["data"]["rows"]}
    assert du_lieu["pm"]["chua_duyet"] in ma


@pytest.mark.parametrize("v,mong", [("1", True), ("0", False)])
def test_loc_theo_DUYET(may, du_lieu, v, mong):
    s, d = _goi(may, f"{V}/queue/lenh-cho?run_id={du_lieu['run']}"
                     f"&duyet={v}&limit=100")
    assert s == 200
    dong = d["data"]["rows"]
    assert dong and all(bool(r["duyet"]) is mong for r in dong)


def test_duyet_LA_thi_400__khong_am_tham_bo_qua(may, du_lieu):
    """⛔ Bo qua im lang mot bo loc la de nguoi doc tin mot danh sach **⛔ khong
    phai cai ho vua yeu cau**."""
    s, d = _goi(may, f"{V}/queue/lenh-cho?run_id={du_lieu['run']}&duyet=2")
    assert s == 400, d


def test_TOM_theo_tien_te__KHONG_co_dong_TONG(may, du_lieu):
    s, d = _goi(may, f"{V}/queue/lenh-cho/summary?run_id={du_lieu['run']}")
    assert s == 200, d
    ds = d["data"]["theo_tien_te"]
    assert ds and all(str(r["curr"]).lower() not in ("tong", "total")
                      for r in ds)
    o = next(r for r in ds if r["curr"] == "VND")
    assert o["so_dong_duyet"] + o["so_dong_chua_duyet"] == o["so_dong"]


def test_TOM_muc_pct_la_thi_400(may, du_lieu):
    s, _ = _goi(may, f"{V}/queue/lenh-cho/summary?run_id={du_lieu['run']}"
                     f"&muc_pct=abc")
    assert s == 400


def test_UNG_VIEN_TIEN_bac_ma_dung_dau(may, du_lieu):
    s, d = _goi(may, f"{V}/queue/lenh/{du_lieu['pm']['khop']}"
                     f"/itl-candidates?run_id={du_lieu['run']}")
    assert s == 200, d
    r = d["data"]
    assert r["ung_vien"], r
    assert r["ung_vien"][0]["bac"] == "ma"
    assert r["ung_vien"][0]["itl_id"] == du_lieu["itl"]
    # ⭐ Phep CAT phai KHAI RA — cat ma im la mac dinh im lang (`INV-I16`)
    assert "bi_cat" in r and "tong_cung_tien_te" in r


#: ⭐ Khuon hop dong `BA-07 §4h ⓵` — **10** truong, dung ban da khai o
#: `test_b2_cua_man_ghep.MUOI_TRUONG`. ⛔ Nhap lai o day la tao ban thu hai.
from tests.api.test_b2_cua_man_ghep import MUOI_TRUONG  # noqa: E402


def test_UNG_VIEN_TIEN_tra_dung_KHUON_HOP_DONG_chu_KHONG_hang_tho(may, du_lieu):
    """⛔⛔⛔ Cua nay tra **hang THO** tu SQL, ⛔ **khong** qua `khuon_ung_vien`.

    ⛔ Man doc `uv.amount` · `uv.chieu` · `uv.nguon`; cua gui `tien` · `ps_no`
      · `ps_co` · `source_sheet` ⇒ **ba cot cua bang giao dich rong**, va
      `khop_dung_tien` so `Number(undefined)` ⇒ **MOI ung vien deu thanh
      "lech"** ⇒ nut `Gan` luon di duong canh bao. Mot phep khop DUNG bi
      trinh bay nhu mot phep khop SAI — te hon la ⛔ khong hien gi.

    ⛔⛔ **Vi sao no song sot:** bai thu cu chi hoi `bac` va `itl_id` — dung
       **hai khoa ma hang tho TINH CO cung co**. Mot bai thu hoi vai khoa
       giao nhau thi ⛔ khong bao gio thay hai khuon la HAI.

    ⭐ Va `/so` (Toan so) **da** nan khuon ⇒ hai cua nuoi **mot** ham ve ma
      noi **hai** thu tieng. Anh chup cua owner `23/09` ⛔ khong lo ra dieu
      nay vi man luc ay dang o che do Toan so — dung cua KIA.
    """
    s, d = _goi(may, f"{V}/queue/lenh/{du_lieu['pm']['khop']}"
                     f"/itl-candidates?run_id={du_lieu['run']}")
    assert s == 200, d
    uv = d["data"]["ung_vien"]
    assert uv, d
    thieu = [k for k in MUOI_TRUONG if k not in uv[0]]
    assert not thieu, (
        "⛔ Cửa thiếu %d/%d trường hợp đồng: %s — nó đang trả HÀNG THÔ "
        "(%s)" % (len(thieu), len(MUOI_TRUONG), ", ".join(thieu),
                  ", ".join(sorted(uv[0])[:6]) + "…"))
    assert uv[0]["amount"] is not None, "⛔ `amount` rỗng — màn in `— không có`"
    assert uv[0]["chieu"] in ("no", "co"), "⛔ `chieu` ⛔ không có"
    # ⭐ `nguon` là **object** *(một chuỗi đã ghép thì tầng dưới ⛔ không bỏ
    #   bớt cột được khi màn hẹp)* — HOẶC `None` kèm `loi_nguon` nói vì sao.
    #   ⛔ Khuôn thử này cố ý dùng `source_sheet='L1'`, tức **đúng cái ca
    #   hỏng**; nên ⛔ không đòi `dict` vô điều kiện, mà đòi **một trong hai
    #   câu trả lời có tên**.
    assert isinstance(uv[0]["nguon"], dict) or uv[0].get("loi_nguon"), (
        "⛔ `nguon` rỗng mà ⛔ **không nói vì sao** — một chỗ trống ⛔ không "
        "tên là chỗ người đọc tự điền nghĩa vào (`INV-I16`)")


def test_HAI_CUA_ung_vien_noi_CUNG_MOT_KHUON(may, du_lieu):
    """⛔⛔ `/itl-candidates` va `/so` nuoi **cung mot ham ve** (`ve_ung_vien`).

    Hai cua ma hai khuon thi ham ve phai **doan** minh dang duoc cho an gi —
    va no ⛔ khong doan duoc, nen no in `— khong co`. ⇒ Tap khoa phai **trung
    nhau o ca 10 truong hop dong**; ⛔ khong doi trung TUYET DOI (cua `/so`
    them `dien_giai_vi_sao`, ca hai them `khoa_to`), chi doi **⛔ khong cua
    nao THIEU** thu ham ve doc."""
    ra = {}
    for duong in ("itl-candidates", "so"):
        s, d = _goi(may, f"{V}/queue/lenh/{du_lieu['pm']['khop']}"
                         f"/{duong}?run_id={du_lieu['run']}")
        assert s == 200, (duong, d)
        uv = d["data"]["ung_vien"]
        ra[duong] = set(uv[0]) if uv else set()
    thieu = set(MUOI_TRUONG) - ra["itl-candidates"]
    thieu2 = set(MUOI_TRUONG) - ra["so"]
    assert not thieu and not thieu2, (
        "⛔ `/itl-candidates` thiếu %s ／ `/so` thiếu %s"
        % (sorted(thieu) or "—", sorted(thieu2) or "—"))


def test_UNG_VIEN_TIEN_khai_CANH_BAO_status(may, du_lieu):
    s, d = _goi(may, f"{V}/queue/lenh/{du_lieu['pm']['chua_duyet']}"
                     f"/itl-candidates?run_id={du_lieu['run']}")
    assert s == 200, d
    assert d["data"]["canh_bao"], "⛔ dong `Pending` phai co canh bao"


def test_UNG_VIEN_TIEN_dong_lenh_KHONG_CO_thi_404(may, du_lieu):
    s, _ = _goi(may, f"{V}/queue/lenh/PL-KHONG-CO-BAO-GIO"
                     f"/itl-candidates?run_id={du_lieu['run']}")
    assert s == 404


def test_ba_tuyen_deu_TRA_pham_vi(may, du_lieu):
    """⛔ Mot con so ⛔ khong kem pham vi la mot con so ⛔ khong doi chieu duoc."""
    for duong in (f"{V}/queue/lenh-cho?run_id={du_lieu['run']}",
                  f"{V}/queue/lenh/{du_lieu['pm']['khop']}/itl-candidates"
                  f"?run_id={du_lieu['run']}"):
        s, d = _goi(may, duong)
        assert s == 200
        assert du_lieu["run"] in json.dumps(d, default=str)
