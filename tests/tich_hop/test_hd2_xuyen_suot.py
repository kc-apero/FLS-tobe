# -*- coding: utf-8 -*-
"""I2 (ISP 3.1.2 · Step 47 · `WO-315`) — HD2 xuyên suốt: config KÝ trong kho → GL → CFA/PLA → phân bổ →
báo cáo → ký bản. Mỗi tầng là CHÍNH mã thật, ⛔ tầng nào tự dựng số.

  ⓪ kho     một kho TEST RIÊNG `fls_test_i2` *(dựng lại từ 0 mỗi lượt — ký tháng là hành vi MỘT CHIỀU, ⛔ huỷ ký
            (C7 `WO-212`) ⇒ "bỏ ký 202510" = kho CHƯA có chữ ký 202510; kho chung `fls_test` có bài khác ký tháng ⇒
            ⛔ dùng chung)*. Nạp: IX.FX (`ix_fx.json`) · IX.PER (21/10, luật A) · IX.ALR (17 luật MM rồi KÝ BẬT 2025 —
            `ix_alr_2025_bat.json`, quyết chủ 22/11) · IX.PL · IX.ORG · IX.VEN.
  ① ký      `POST /config/fx/{yyyymm}/sign` qua máy chủ thử THẬT, `actor` = thẻ test *(C7 — ⛔ gọi hàm repo thẳng)*.
  ② chuỗi   11 gói `WP-C2 … WP-C5c` *(CA → SO → AL → RP)* chạy bằng CHÍNH đường sản phẩm `tools/do_hd2.chay_goi(gói,
            dsn, fx="kho")` *(vòng sửa R1 `I2-R1-02` — ⛔ còn mock `nap_fx` trong bài)*: tỷ giá của MỌI gói đến từ
            `fls.repo.cau_hinh_repo.fx_cua(conn, tháng)` THẬT; tháng chưa ký ⇒ `FxChan` ⇒ khối ĐỎ do MÃ ghép. C4a/b/c
            *(đầu vào đã quy đổi)* hỏi `fx_cua` mọi tháng đầu vào *(`kiem_fx_thang` — `I2-R1-01`)*. Ảnh `ix_fx.json` bị
            trỏ vào tệp vắng suốt chuỗi ⇒ gói nào lén đọc ảnh là NỔ.
  ③ cổng    `GET /gates` *(máy chủ thử, `tep_hd2` = tệp tạm ghi theo hợp đồng `_ghi_cong`)*.
  ④ màn     F03 — node-vm (`man_f03.js` thật) VÀ Chromium headless THẬT, 390 px.
  ⑤ ký bản  báo cáo kỳ 2025-12 *(đầu ra H14 `bao["609"]`)* → `dua_ban_ky` → `ky_ban` ⇒ checksum = checksum JSON ô.

⭐ `mong` = khối gói trong `docs/ITL/_tools/hd2_cong.json` ĐÃ COMMIT ở bước của gói *(H4…H14 — ⛔ khai lại)*. I2 chỉ
đòi: chạy với tỷ giá TỪ KHO ĐÃ KÝ ra ĐÚNG các số ấy. Khác ⇒ lệch giữa tầng ⇒ ĐỎ *(Đ5 — cả hai chiều)*.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import threading
import time
from collections.abc import Mapping
from decimal import Decimal
from pathlib import Path
from unittest import mock

import psycopg
import pytest

from fls.api import bang_tuyen as bt
from fls.api import cua, the
from fls.cau_hinh import ban_ky
from fls.cau_hinh import fx as cfx
from fls.db.kho import doi_ten_kho, dsn_test, dung_lai_kho_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from fls.web.phuc_vu import lam_nguoi_phuc_vu
from tests.web.test_isp_f03_hd import _do_tran, _lop, _the, _ve_f03, can_browser
from tests.web.than_sinh import than_sinh
from tools import do_hd2 as h
from tools import do_hd2_c3c, do_hd2_c3d, do_hd2_c5a, do_hd2_c5b, do_hd2_c5c

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
TEP_CONG_THAT = GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json"
KHOA = "khoa-thu-cua-bai-tich-hop-i2-hd2-xuyen-suot-dai-hon-32"
V = bt.TIEN_TO
ACTOR = "i2.tich.hop@vi-du.invalid"           # actor TEST (⛔ chữ ký thật — O6/O8 là chủ)
TEN_KHO = "fls_test_i2"

# ══ MONG — khai TRƯỚC (Đ5), mỗi số kèm NHÃN (Đ4) ════════════════════════════════════════════════════════════════
THANG_BO_KY = 202510                         # tháng "bỏ ký" (AC-2)
KY_BAN = 202512                              # kỳ ký bản (AC-3) — đầu ra H14 `609` (Daily Report 3 PL · FS1_FS2_gop)
MA_BAN = "609"
MONG_SO_THANG_FX = 37                        # tháng của IX.FX (`ix_fx.json`: 202306 + 202401…202612) — mọi tháng đều ký
GOI = ("WP-C2", "WP-C3a", "WP-C3b", "WP-C3c", "WP-C3d", "WP-C4a", "WP-C4b", "WP-C4c", "WP-C5a", "WP-C5b", "WP-C5c")
#: ⭐ `I2-R1-01` (KQ-317 CHẶN) — D1 DECIDED: bỏ ký 202510 ⇒ CẢ 11/11 gói CHẶN, **0 ô số** ở mọi gói *(trước vòng sửa
#: C4a/b/c còn ra 35 + 175 + 2.303 = 2.513 ô — bài cũ ghim vi phạm làm `mong`)*.
MONG_GOI_CHAN = GOI
#: Giới hạn CÓ TÊN (`I2-R1-03`): đầu vào C4a/b/c *(CFA1 GI · MID1 — PD 504/MID1)* mang **mUSD đã quy đổi ở AS-IS** ⇒
#: GIÁ TRỊ tỷ giá ⛔ vào phép tính; gói chỉ hỏi CHỮ KÝ tháng *(D1 vẫn CHẶN — xem trên)*.
MONG_GOI_DA_QUY_DOI = ("WP-C4a", "WP-C4b", "WP-C4c")
#: Đột biến tỷ giá *(`I2-R1-03`, đo 22/11)* — mong gói ĐỔI số theo hai kiểu phá:
#:  · CHỈ USD ×1,01 *(VND = 1 giữ)* ⇒ mọi gói đọc GIÁ TRỊ tỷ giá đổi = 8/11; C4a/b/c giữ *(đầu vào đã quy đổi)*.
#:  · MỌI tiền tệ ×1,01 *(kể cả VND)* ⇒ chỉ C2 · C5b · C5c đổi: mUSD = tỷ giá(tt) ÷ tỷ giá(USD) × số *(`gl.py` BR/BS)*
#:    ⇒ nhân ĐỀU triệt tiêu — C3a…d · C5a ⛔ bỏ qua tỷ giá, chỉ là đột biến đồng dạng ⛔ có răng với chúng. C2 đổi
#:    vì bVND *(BO/BP/BQ)* + tồn VND; C5b vì COM_GAG VND ÷ USD; C5c vì đọc lại C5b.
MONG_DOI_USD = tuple(g for g in GOI if g not in MONG_GOI_DA_QUY_DOI)
MONG_DOI_DEU = ("WP-C2", "WP-C5b", "WP-C5c")
#: khoá số so với khối đã commit — mọi khoá CÓ trong khối commit đều phải bằng (⛔ chọn lọc)
KHOA_SO = ("tong_o", "khop", "khop_co_so", "o_co_so", "o_0_0", "so_o_dap_an_so_duoc", "lech_co_chu_dich",
           "lech_ngoai_ten", "o_so", "o_khong_so", "o_khac_0", "dong_so", "mau_so_thang", "dat")
#: ⭐ `H14-R2-01` (KQ-314) — ngọn `isp/H14` `a6a2df2` CHƯA sinh lại `mong` CHECK `NB = 0` sau H13-R1 (`pla.check_atl`)
#: ⇒ `WP-C5c` ĐỎ với ĐÚNG 18 dòng lý do `check.<đáp án>.….NB = 0.…` *(đo 22/11: y hệt khi chạy bằng ảnh `ix_fx.json` ⇒
#: ⛔ do I2)*. Gộp lại ngọn H14 đã sửa ⇒ đặt `False` ⇒ C5c `dat = None` (605 chờ chủ) ⇒ bài ghim này ĐỎ cho tới khi khai lại.
MONG_H14_R2_01_CHUA_SUA = False         # gộp ngọn H14 `4b49d00` (R2-01 đã sửa) ⇒ khai lại 22/11
MONG_C5C_DAT = False if MONG_H14_R2_01_CHUA_SUA else None
MONG_C5C_SO_LY_DO_NB0 = 18 if MONG_H14_R2_01_CHUA_SUA else 0
#: cổng cha F03 — WP-C5 = None vì `WP-C5c` 605 DỪNG chờ chủ ký `DUNG_KY` (H14-R1-01) — lệch CÓ TÊN so với chữ ISP I2-F1
#: *(trong lúc `H14-R2-01` chưa gộp: False — xem trên)*
MONG_CHA = {"WP-C2": True, "WP-C3": True, "WP-C4": True, "WP-C5": MONG_C5C_DAT}


# ══ ② chuỗi = ĐƯỜNG SẢN PHẨM `h.chay_goi` ═════════════════════════════════════════════════════════════════════════
def chay_chuoi(dsn: str) -> dict:
    """11 gói qua `h.chay_goi(g, dsn, fx="kho")` — MÃ ghép khối ĐỎ khi `FxChan` *(⛔ bài ghép)*. Ảnh `ix_fx.json` trỏ
    vào tệp vắng ⇒ gói nào đọc ảnh là NỔ `FileNotFoundError` *(canh có răng — `I2-R1-04`; `nap_fx` đọc `IX_FX` lúc
    GỌI)*. Trả `{khoi, tq, fx_chan, fx_doc, fx_doc_goi}`."""
    khoi: dict[str, dict] = {}
    tq: dict = {}
    chan: dict[str, str] = {}
    doc_goi: dict[str, list[int]] = {}
    with mock.patch.object(h, "IX_FX", Path("/khong-co/ix_fx.json")):
        for g in GOI:
            k, _dat, t, doc = h.chay_goi(g, dsn, fx="kho")
            khoi[g], doc_goi[g] = k, doc
            if t is None:
                chan[g] = k["ly_do"][0]
            else:
                tq[g] = t
    return {"khoi": khoi, "tq": tq, "fx_chan": chan, "fx_doc_goi": doc_goi,
            "fx_doc": sorted({m for d in doc_goi.values() for m in d})}


def ghi_cong(khoi: Mapping[str, dict], p: Path) -> Path:
    """Đúng hợp đồng `do_hd2._ghi_cong`: `WP-C2` ở gốc, gói khác khoá theo tên."""
    d = {**khoi["WP-C2"], **{g: b for g, b in khoi.items() if g != "WP-C2"}}
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return p


# ══ ⓪ ① kho + máy chủ ══════════════════════════════════════════════════════════════════════════════════════════
def _tok(sub: str = ACTOR) -> str:
    return the.dong_the({"sub": sub, "exp": int(time.time()) + 900, "vai": ["ke_toan"]}, KHOA.encode())


@contextlib.contextmanager
def _may(dsn: str, *, ghi: bool = False, tep_hd2=None):
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA

    @contextlib.contextmanager
    def mo_doc():
        c = noi_chi_doc(dsn)
        try:
            yield c
        finally:
            c.close()

    @contextlib.contextmanager
    def mo_ghi():
        c = psycopg.connect(dsn, autocommit=True)
        try:
            yield c
        finally:
            c.close()

    m = cua.dung_may(mo_doc, cong=0, mo_ghi=mo_ghi if ghi else None, tep_hd2=tep_hd2,
                     phuc_vu_tep=None if ghi else lam_nguoi_phuc_vu(
                         {"the": _tok(), "actor": ACTOR, "cho_ghi": False}, than_sinh=than_sinh()))
    threading.Thread(target=m.serve_forever, daemon=True).start()
    try:
        yield m
    finally:
        m.shutdown()
        m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


def _goi(m, duong: str, pt: str = "GET") -> tuple[int, dict]:
    c = http.client.HTTPConnection(*m.server_address, timeout=30)
    try:
        c.request(pt, duong, body=b"{}" if pt == "POST" else None,
                  headers={"Authorization": f"Bearer {_tok()}", "Content-Type": "application/json"})
        r = c.getresponse()
        raw = r.read()
        return r.status, (json.loads(raw) if raw else {})
    finally:
        c.close()


def _nap_config(dsn: str) -> None:
    with psycopg.connect(dsn, autocommit=True) as c:
        chc.nap_ix_fx(c, str(h.IX_FX), actor="bai-i2", thang_dau=h.THANG_DAU_FX, nguon="I2 · ix_fx.json")
        do_hd2_c5c.nap_nen_kho(c, actor="bai-i2")        # IX.PER · IX.ALR (+ KÝ BẬT 2025) · IX.PL
        chc.nap_ix_org(c, str(do_hd2_c3c.CDT_CORRECT), str(do_hd2_c3c.MM), actor="bai-i2")
        chc.nap_ix_ven(c, str(GOC / "tests/fixture/cau_hinh/ix_ven.json"),
                       duong_cdt1=str(GOC / "tests/fixture/cau_hinh/cdt_correct.json"), actor="bai-i2")


@pytest.fixture(scope="module")
def chuoi(tmp_path_factory):
    dsn = doi_ten_kho(dsn_test(), TEN_KHO)
    dung_lai_kho_test(dsn)                                # kho RIÊNG, từ 0 (⛔ chữ ký sót của lượt trước)
    _nap_config(dsn)
    tmp = tmp_path_factory.mktemp("i2")
    with psycopg.connect(dsn, autocommit=True) as c:
        thang = [d.yyyymm for d in chc.doc_fx(c).ky]
        alr_ky = chc.doc_alr(c)
    ky: dict[int, int] = {}
    with _may(dsn, ghi=True) as m:
        for t in thang:
            if t != THANG_BO_KY:
                ky[t] = _goi(m, f"{V}/config/fx/{t}/sign", "POST")[0]
        a = chay_chuoi(dsn)                               # 202510 CHƯA ký
        st_bo, _ = _goi(m, f"{V}/config/fx/{THANG_BO_KY}/sign", "POST")
        b = chay_chuoi(dsn)                               # đủ 36 tháng đã ký
        ky[THANG_BO_KY] = st_bo
        that = chc.fx_cua
        dot = {}
        for ten, cot in (("usd", ("USD",)), ("deu", tuple(cfx.TIEN_TE))):     # `I2-R1-03` — đột biến tỷ giá kho
            with mock.patch.object(chc, "fx_cua", lambda c, m, cot=cot: {
                    t: (v * Decimal("1.01") if t in cot else v) for t, v in that(c, m).items()}):
                dot[ten] = chay_chuoi(dsn)["khoi"]
    with psycopg.connect(dsn, autocommit=True) as c:
        nguoi_ky = {k: v.actor for k, v in chc.doc_ky_fx(c).items()}
        noi_dung = b["tq"]["WP-C5c"].bao[MA_BAN]
        v_dua = chc.dua_ban_ky(c, KY_BAN, noi_dung, actor="engine-h14-i2")
        v_ky = chc.ky_ban(c, KY_BAN, actor=ACTOR)
        nd_kho = chc.doc_noi_dung_ban_ky(c, KY_BAN, v_ky.phien_ban)
    return {"dsn": dsn, "thang": thang, "ky": ky, "nguoi_ky": nguoi_ky, "alr": alr_ky, "a": a, "b": b, "dot": dot,
            "p_a": ghi_cong(a["khoi"], tmp / "hd2_cong_bo_ky.json"), "p_b": ghi_cong(b["khoi"], tmp / "hd2_cong.json"),
            "noi_dung": noi_dung, "v_dua": v_dua, "v_ky": v_ky, "nd_kho": nd_kho}


@pytest.fixture(scope="module")
def cong_that() -> dict:
    return json.loads(TEP_CONG_THAT.read_text(encoding="utf-8"))


def _khoi_that(d: dict, g: str) -> dict:
    return d if g == "WP-C2" else d[g]


def _gates(dsn: str, p: Path) -> dict:
    with _may(dsn, tep_hd2=str(p)) as m:
        st, env = _goi(m, f"{V}/gates")
    assert st == 200, env
    return env["data"]


# ══ ⓪ ① ════════════════════════════════════════════════════════════════════════════════════════════════════════
def test_ky_thang_qua_tuyen_C7_actor_tu_the_36_thang(chuoi):
    assert len(chuoi["thang"]) == MONG_SO_THANG_FX                                  # Đ3: mẫu số
    assert set(chuoi["ky"].values()) == {201}, chuoi["ky"]
    assert set(chuoi["nguoi_ky"]) == set(chuoi["thang"]) and set(chuoi["nguoi_ky"].values()) == {ACTOR}


def test_config_ALR_2025_bat_da_ky_trong_kho(chuoi):
    """IX.ALR đọc từ kho có luật 2025 BẬT *(quyết chủ 22/11 — `ix_alr_2025_bat.json`)*."""
    tep = json.loads(do_hd2_c5a.TEP_KY.read_text(encoding="utf-8"))
    kho = {(x.hd, x.tu_ky): x for x in chuoi["alr"].luat}
    assert len(tep["luat"]) == 26                                                 # Đ3: mẫu số (13 bật + 13 tắt 2026)
    for r in tep["luat"]:
        x = kho[(r["hd"], r["tu_ky"])]
        assert (x.bat, x.nguoi_ky) == (r["bat"], tep["ky"]["nguoi_ky"]), (r, x)
    assert sum(r["bat"] for r in tep["luat"]) == 13


# ══ AC-1 · I2-B1 ═══════════════════════════════════════════════════════════════════════════════════════════════
def test_B1_ty_gia_moi_goi_TU_KHO_qua_duong_san_pham(chuoi):
    """`I2-R1-02`: MỖI gói *(11/11)* hỏi `fx_cua` ≥ 1 tháng qua `h.chay_goi` — bằng chứng DƯƠNG, ⛔ đếm 0 lần mở ảnh."""
    b = chuoi["b"]
    assert b["fx_chan"] == {}
    assert {g: bool(d) for g, d in b["fx_doc_goi"].items()} == {g: True for g in GOI}, b["fx_doc_goi"]
    assert THANG_BO_KY in b["fx_doc"] and len(b["fx_doc"]) >= 20, b["fx_doc"]    # mẫu số tháng đọc qua fx_cua
    for g in MONG_GOI_DA_QUY_DOI:                                                 # C4: đủ mọi tháng đầu vào
        assert THANG_BO_KY in b["fx_doc_goi"][g], (g, b["fx_doc_goi"][g])


def test_B1_anh_ix_fx_canh_co_rang():
    """Canh của `chay_chuoi` có RĂNG (`I2-R1-04`): ngoài `ty_gia_kho`, `nap_fx()` với `IX_FX` vắng ⇒ NỔ."""
    with mock.patch.object(h, "IX_FX", Path("/khong-co/ix_fx.json")), pytest.raises(FileNotFoundError):
        h.nap_fx()


def test_chay_goi_kho_khong_doc_duoc_la_khoi_DO_co_ly_do():
    """Đ5: kho tắt / IX.FX chưa nạp ⇒ `chay_goi` trả khối ĐỎ có chữ `IX.FX ⛔ đọc được` — ⛔ nổ, ⛔ rơi về ảnh."""
    k, dat, tq, doc = h.chay_goi("WP-C2", "postgresql://fls:fls@127.0.0.1:1/khong_co", fx="kho")
    assert (dat, tq, doc, k["dat"]) == (False, None, [], False), k
    assert k["ly_do"][0].startswith("IX.FX ⛔ đọc được từ kho:"), k["ly_do"]


def _so(k: dict) -> dict:
    return {x: k[x] for x in KHOA_SO if x != "dat" and isinstance(k.get(x), int | float)}


def test_B1_dot_bien_ty_gia_goi_doi_so_dung_mong(chuoi):
    """`I2-R1-03`: đột biến USD ×1,01 ⇒ 8/11 gói đọc GIÁ TRỊ tỷ giá đổi số; nhân ĐỀU ⇒ chỉ 3/11 *(triệt tiêu ở mUSD)*.
    C4a/b/c giữ ở cả hai *(đầu vào đã quy đổi — giới hạn có tên)*."""
    goc = {g: _so(chuoi["b"]["khoi"][g]) for g in GOI}
    assert all(goc[g] for g in GOI), goc                                         # Đ3: mỗi gói có số để so
    for ten, mong in (("usd", MONG_DOI_USD), ("deu", MONG_DOI_DEU)):
        doi = tuple(g for g in GOI if _so(chuoi["dot"][ten][g]) != goc[g])
        assert doi == mong, (ten, doi)


@pytest.mark.parametrize("g", GOI)
def test_B1_goi_so_o_va_lech_bang_mong_da_khai(chuoi, cong_that, g):
    """Mỗi gói: số ô so = số ô đáp án đã khai, lệch theo lớp = `mong` của bước — đọc khối commit (⛔ khai lại)."""
    thuc, mong = chuoi["b"]["khoi"][g], _khoi_that(cong_that, g)
    khoa = [k for k in KHOA_SO if k in mong]
    assert "tong_o" in khoa and mong["tong_o"] > 0, (g, sorted(mong))             # Đ3: mẫu số ⛔ rỗng
    if g == "WP-C5c":
        mong = {**mong, "dat": MONG_C5C_DAT}
    assert {k: thuc.get(k) for k in khoa} == {k: mong[k] for k in khoa}, g
    for k in ("lech_co_ten", "mong_lech_co_chu_dich", "mong_tong_o"):
        if k in mong:
            assert thuc.get(k) == mong[k], (g, k)


def test_B1_C2_o_so_bang_o_dap_an_so_duoc(chuoi):
    k = chuoi["b"]["khoi"]["WP-C2"]
    assert k["tong_o"] == k["so_o_dap_an_so_duoc"] == k["khop"] > 0 and k["lech_ngoai_ten"] == 0


def test_B1_C5a_co_bat_khop_va_lop_lech_dung_WO(chuoi):
    """WO-315 "Đã đo": cờ bật — khớp 6.646/11.764 *(nhãn: ô CÓ SỐ — `khop_co_so`/`o_co_so`; toàn khối 40.556/45.674
    gồm 0 = 0)*; `loi_as_is` 928 · `lech_D3` 3.099 · `chua_co_dau_vao` 1.091."""
    k = chuoi["b"]["khoi"]["WP-C5a"]
    assert (k["khop_co_so"], k["o_co_so"], k["khop"], k["tong_o"]) == (6646, 11764, 40556, 45674)
    lop = k["lech_co_ten"]
    assert (k["loi_as_is"], lop["lech_D3"]["so_o"], lop["chua_co_dau_vao"]["so_o"]) == (928, 3099, 1091)


def test_B1_C3d_lech_FLS_0(chuoi):
    assert chuoi["b"]["khoi"]["WP-C3d"]["lech_ngoai_ten"] == 0


# ══ AC-2 · I2-B2 ═══════════════════════════════════════════════════════════════════════════════════════════════
def test_B2_bo_ky_202510_FX_CHAN_xuyen_chuoi(chuoi):
    """`I2-R1-01`: D1 xuyên MỌI tầng — 11/11 gói CHẶN, đếm ô số TỪNG gói = 0 *(⛔ chỉ đếm gói nổ)*."""
    a = chuoi["a"]
    assert sorted(a["fx_chan"]) == sorted(MONG_GOI_CHAN), sorted(a["fx_chan"])
    for g, ly in a["fx_chan"].items():
        assert ly.startswith(f"FX_CHAN {THANG_BO_KY}:") and "CHƯA ký" in ly, (g, ly)
    assert THANG_BO_KY not in a["fx_doc"]                 # ⛔ số tỷ giá nào ra cho tháng ấy
    assert a["tq"] == {}                                  # ⛔ gói nào chạy ra kết quả
    o_so = {g: sum(_so(a["khoi"][g]).values()) for g in GOI}
    assert len(o_so) == 11 and o_so == {g: 0 for g in GOI}, o_so
    for g in GOI:
        k = a["khoi"][g]
        assert (k["dat"], k["fx_chan"], k["nguon_ty_gia"]) == (False, THANG_BO_KY, "kho"), (g, k)


def test_B2_cong_HD2_WP_C2_dat_false_co_chu(chuoi):
    d = _gates(chuoi["dsn"], chuoi["p_a"])
    g = {x["ma"]: x for x in d["cong"]}
    c2 = g["HD2_WP_C2"]
    assert c2["dat"] is False and f"FX_CHAN {THANG_BO_KY}" in (c2.get("ly_do") or ""), c2
    for cha in ("HD2_WP_C3", "HD2_WP_C4", "HD2_WP_C5"):
        assert g[cha]["dat"] is False, g[cha]
    c4 = json.dumps(g["HD2_WP_C4"], ensure_ascii=False)                          # `I2-R1-01`: C4 ĐỎ có chữ
    assert f"FX_CHAN {THANG_BO_KY}" in c4, c4


# ══ AC-3 · I2-B3 ═══════════════════════════════════════════════════════════════════════════════════════════════
def test_B3_ky_ban_2025_12_checksum_bang_checksum_JSON_o(chuoi):
    nd, v1, v2 = chuoi["noi_dung"], chuoi["v_dua"], chuoi["v_ky"]
    assert nd["ky"] == KY_BAN and len(nd["o"]) > 0, (nd.get("ky"), len(nd.get("o") or {}))
    assert (v1.phien_ban, v1.trang_thai, v1.khong_doi) == (1, "chua_ky", False)
    assert (v2.phien_ban, v2.trang_thai, v2.actor) == (1, "da_ky", ACTOR)
    assert v1.checksum == v2.checksum == ban_ky.checksum(nd) == ban_ky.checksum(chuoi["nd_kho"])
    assert chuoi["nd_kho"] == json.loads(ban_ky.chuan_hoa(nd))


# ══ AC-4/5 · I2-F1/F2 ═════════════════════════════════════════════════════════════════════════════════════════
def _cha(ve: dict) -> dict[str, dict]:
    return {g: _the(ve, f"HD2 {g}:") for g in MONG_CHA}


def _muc(t: dict) -> bool | None:
    lop = _lop(t)
    return True if "pass" in lop else False if "fail" in lop else None if "unk" in lop else "?"


def test_F1_cong_bon_cha_sau_chuoi_du(chuoi):
    d = _gates(chuoi["dsn"], chuoi["p_b"])
    g = {x["ma"]: x for x in d["cong"]}
    assert {c: g[f"HD2_{c.replace('-', '_')}"]["dat"] for c in MONG_CHA} == MONG_CHA
    c5 = json.dumps(g["HD2_WP_C5"], ensure_ascii=False)
    assert ("NB = 0" if MONG_H14_R2_01_CHUA_SUA else "605") in c5, c5             # lý do có TÊN


def test_C5c_H14_R2_01_ly_do_dung_18_dong_check_NB0_ngoai_ra_khop(chuoi):
    k = chuoi["b"]["khoi"]["WP-C5c"]
    assert len(k["ly_do"]) == MONG_C5C_SO_LY_DO_NB0, k["ly_do"][:3]
    assert all(x.startswith("check.") and ".NB = 0." in x for x in k["ly_do"])
    assert k["dat_mong"] is (not MONG_H14_R2_01_CHUA_SUA)
    assert any(x.startswith("605:") for x in k["khong_do_duoc"])                 # 605 vẫn DỪNG có tên


def test_F1_vm_bon_the_HD2_co_so_C5_khong_do_duoc_co_ly_do(chuoi):
    ve = _ve_f03(_gates(chuoi["dsn"], chuoi["p_b"]))
    t = _cha(ve)
    assert {g: _muc(x) for g, x in t.items()} == MONG_CHA
    for g, x in t.items():
        assert any(ch.isdigit() for ch in x["txt"].split(":", 1)[1]), (g, x["txt"][:120])
    if not MONG_H14_R2_01_CHUA_SUA:
        assert "KHÔNG ĐO ĐƯỢC" in t["WP-C5"]["txt"] and "605" in t["WP-C5"]["txt"]
    else:
        assert "KHÔNG ĐẠT" in t["WP-C5"]["txt"] and "NB = 0" in t["WP-C5"]["txt"]


@can_browser
def test_F1_F2_chromium_that(chuoi):
    for p, mong in ((chuoi["p_b"], MONG_CHA), (chuoi["p_a"], None)):
        with _may(chuoi["dsn"], tep_hd2=str(p)) as m:
            res = _do_tran("http://%s:%d/" % m.server_address, 390)
        t = _cha(res)
        if mong is not None:
            assert {g: _muc(x) for g, x in t.items()} == mong
            assert ("KHÔNG ĐẠT" if MONG_H14_R2_01_CHUA_SUA else "KHÔNG ĐO ĐƯỢC") in t["WP-C5"]["txt"]
        else:
            assert _muc(t["WP-C2"]) is False and f"FX_CHAN {THANG_BO_KY}" in t["WP-C2"]["txt"]


def test_F2_vm_bo_ky_the_C2_do_co_chu(chuoi):
    t = _cha(_ve_f03(_gates(chuoi["dsn"], chuoi["p_a"])))
    assert _muc(t["WP-C2"]) is False
    assert "KHÔNG ĐẠT" in t["WP-C2"]["txt"] and f"FX_CHAN {THANG_BO_KY}" in t["WP-C2"]["txt"]
