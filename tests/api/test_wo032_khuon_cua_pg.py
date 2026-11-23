# -*- coding: utf-8 -*-
"""`WO-032` — **cửa** trả khuôn `⓵` đủ trường ở **mọi** cửa *(`BA-07` v3.7 §4h)*.

  `AC-2` · `lech` = `|amount − amount lệnh|` ở **mọi** bậc, `null` ⇔ khác tiền
          tệ / thiếu số — đo **quan hệ** trên **bốn** cửa *(`itl-candidates` ·
          `/so` · `lenh-cho` `the.gd` · `lenh-da-gan` `the.gd`/`gd_ds`)*.
  `AC-4` · `khoa_to` **luôn có mặt** trên **mọi** `the.gd` / `gd_ds` của hai cửa
          danh sách; ca có số CT trong diễn giải ⇒ `khoa_to` ∋ số ấy.
  `AC-5` · `/so` — dòng ⛔ khớp mã, **khác tiền tệ** lệnh ⇒ `bac = 'khac_tien_te'`;
          ⛔ dòng khác tiền tệ nào mang `cung_tien_te`.

⛔⛔ Đo bằng **HTTP** trên **kho TEST** *(`dsn_test()` nổ nếu trỏ kho thật; ca
assert `current_database() = 'fls_test'`)*. Lỗi gốc *(`KQ-031` `F-2`/`F-3`, sổ
thật 8088)*: bậc `ma` luôn `lech = null` — **338 / 448** ứng viên lệch thật in
`—`; `/so` + `the.gd`/`gd_ds` `null` ở **mọi** dòng; `the.gd` **0 / 768** mang
`khoa_to`; `/so` dán `cung_tien_te` lên **3.926 / 6.165** dòng khác tiền tệ với
một lệnh VND.

⭐ Phép đo là **quan hệ** *(một oracle độc lập bằng `Decimal`, ⛔ gọi lại hàm
của mã)*: một luật sai ở **một** trong bốn cửa *(vd. so tiền tệ ⛔ `trim`)* thì
cửa ấy ĐỎ, ⛔ chìm trong tổng.
"""
from __future__ import annotations

from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo032 import dung_ca, goi_het, hang
from tests.web.test_vong_f02_pg import _may

pytestmark = pytest.mark.pg


@pytest.fixture(scope="module")
def ca_than():
    """`(ca, {khoá: thân cửa thật})` — ⭐ dựng **một lần** cho cả tệp."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca(c)
    with _may() as m:
        yield ca, goi_het(m, ca)


def _te(c) -> str:
    return str(c or "").strip().upper()


def _mong_lech(amount, curr, amount_lenh, curr_lenh):
    """Oracle **độc lập** của `BA-07` v3.7 §4h ⓵ dòng `lech`."""
    if not _te(curr) or not _te(curr_lenh) or _te(curr) != _te(curr_lenh):
        return None
    if amount is None or amount_lenh is None:
        return None
    return abs(D(str(amount)) - D(str(amount_lenh)))


def _phan_tu(ca, t) -> dict[str, list[tuple[dict, object, object]]]:
    """`{cửa: [(phần tử khuôn ⓵, amount lệnh, curr lệnh)]}` — so với dòng lệnh
    **của chính cửa/thẻ** *(`BA-07` v3.7)*. Phần tử *"lỗi nguồn"* ⛔ đủ khuôn
    *(chỉ `{loi_nguon, itl_id}` — `xu_ly._gan_gd` nhánh ngoại lệ)* ⇒ bỏ, đếm."""
    ra: dict[str, list] = {"itl-candidates": [], "/so": [], "lenh-cho": [],
                           "lenh-da-gan": []}
    for k in ("UV_A", "UV_X"):
        dl = t[k]["dong_lenh"]
        ra["itl-candidates"] += [(u, dl["amount"], dl["curr"])
                                 for u in t[k]["ung_vien"]]
    for k in ("SO_A", "SO_X"):
        dl = t[k]["dong_lenh"]
        ra["/so"] += [(u, dl["amount"], dl["curr"]) for u in t[k]["ung_vien"]]
    for k, cua in (("GHEP_MAY", "lenh-cho"), ("LUOI_VND", "lenh-cho"),
                   ("GHEP_DA_GAN", "lenh-da-gan")):
        for x in t[k].get("rows") or []:
            th = x.get("the") or {}
            for g in [th.get("gd")] + list(th.get("gd_ds") or []):
                if g and "amount" in g:
                    ra[cua].append((g, x.get("amount"), x.get("curr")))
    return ra


# ═══ AC-2 · `lech` đúng QUAN HỆ ở cả BỐN cửa ═══════════════════════════════
def test_AC2_lech_BON_cua_la_tri_tuyet_doi_moi_bac_null_CHI_khi_khac_tien_te(
        ca_than):
    """⭐ Mọi phần tử khuôn `⓵`: cùng tiền tệ ∧ hai số có mặt ⇒
    `Decimal(lech) == |amount − amount lệnh|`; khác tiền tệ ⇒ `lech is None`.
    Mỗi cửa có **≥1** ca lệch ≠ 0 cùng tiền tệ **và** ≥1 ca khác tiền tệ
    **và** ≥1 ca **bậc `ma`** lệch ≠ 0 — **cả bốn** cửa.

    ⭐ *(vòng 2, `TL-033 ⓐ`)*: vòng 1 miễn `lenh-da-gan` khỏi vế *"bậc `ma`"*
      vì `xu_ly._bac` ⛔ bao giờ ra `ma` ở cửa ấy *(`HOI-033`)*; `fls-ba` ⛔
      chấp nhận phép thay thế ⇒ vòng 2 sửa mã *(`lc.gan_ma_canon`)* và bài này
      đo **đúng chữ** `AC-2`. Lo gốc giữ nguyên — chỉ bỏ miễn trừ.

    ⭐⭐ *(`WO-037`, `BA-07` **v3.9** §4h ⓵')* — viết lại **một** vế, lo gốc giữ:
      cửa `lenh-cho` chỉ trả lệnh **chưa** gán, và `the.gd` của lệnh chưa gán
      nay ⛔ **bao giờ** là dòng khác tiền tệ *(đề xuất của máy phải ghi được —
      sổ thật **84 / 268** trước vá ⇒ **0**)*. Vế mẫu số *"≥1 ca khác tiền tệ"*
      của `lenh-cho` vì thế **đảo** thành luật mới: **= 0** *(⛔ bỏ, ⛔ nới)*.
      Nhánh `lech = null` khi khác tiền tệ vẫn đo ở **ba** cửa kia
      *(`itl-candidates` · `/so` · `lenh-da-gan` — mẫu số in ra, `Đ3`)*; phép so
      quan hệ `lech` vẫn chạy trên **mọi** phần tử của **cả bốn** cửa.

    ⛔ Chiều ĐỎ: trả `lenh_cho.py:420` về `lech_tuyet_doi=None` *(hôm nay)* ⇒ bậc
    `ma` `null` ⇒ ĐỎ; `/so` `None` ⇒ ĐỎ; tính lệch qua hai tiền tệ ⇒ ĐỎ;
    tập rỗng ⇒ ĐỎ; ⭐ `lenh-cho` đề xuất lại dòng khác tiền tệ *(mã `8d7bea2`)*
    ⇒ ĐỎ."""
    ca, t = ca_than
    sai, bang = [], []
    for cua, ds in _phan_tu(ca, t).items():
        assert ds, f"⛔ không đo được: cửa {cua} ⛔ trả phần tử khuôn ⓵ nào"
        n_lech = n_ma = n_khac = 0
        for u, al, cl in ds:
            mong = _mong_lech(u.get("amount"), u.get("curr"), al, cl)
            co = None if u.get("lech") is None else D(str(u["lech"]))
            if co != mong:
                sai.append(f"{cua} itl {u['itl_id']} bậc {u.get('bac')}: "
                           f"{u.get('amount')} {u.get('curr')} ↔ lệnh {al} {cl} "
                           f"⇒ lech {u.get('lech')!r}, mong {mong!r}")
            if mong is not None and mong != 0:
                n_lech += 1
                n_ma += u.get("bac") == "ma"
            if _te(u.get("curr")) and _te(cl) and _te(u.get("curr")) != _te(cl):
                n_khac += 1
        bang.append((cua, len(ds), n_lech, n_ma, n_khac))
    for cua, n, a, b, c in bang:
        print(f"WO-032 AC-2 · {cua}: {n} phần tử · lệch≠0 cùng tiền tệ {a} "
              f"(bậc ma {b}) · khác tiền tệ {c}")
    assert not sai, "⛔ `lech` sai quan hệ:\n  " + "\n  ".join(sai)
    for cua, n, a, b, c in bang:
        assert a >= 1, f"⛔ không đo được: {cua} ⛔ có ca lệch ≠ 0 cùng tiền tệ"
        if cua == "lenh-cho":
            # ⭐ `BA-07` v3.9 §4h ⓵' — `the.gd` chưa gán ⛔ khác tiền tệ.
            assert c == 0, f"⛔ lenh-cho đề xuất {c} dòng khác tiền tệ (v3.9: 0)"
            continue
        assert c >= 1, f"⛔ không đo được: {cua} ⛔ có ca khác tiền tệ"
        assert b >= 1, f"⛔ không đo được: {cua} ⛔ có ca bậc `ma` lệch ≠ 0"


def test_AC2_bac_MA_lech_DUNG_1_trieu_o_ung_vien_va_toan_so(ca_than):
    """Ca cụ thể của `KQ-031 F-2`: lệnh `A` ↔ dòng tiền `A+1.000.000` bậc `ma`
    ⇒ `lech = 1000000` ở **cả** `itl-candidates` lẫn `/so` lẫn `the.gd`."""
    ca, t = ca_than
    for k in ("UV_A", "SO_A"):
        u = {x["itl_id"]: x for x in t[k]["ung_vien"]}[ca["i_a"]]
        assert u["bac"] == "ma", (k, u)
        assert D(str(u["lech"])) == D("1000000"), (k, u)
    g = hang(t["GHEP_MAY"], ca["lenh"]["A"])["the"]["gd"]
    assert g["itl_id"] == ca["i_a"] and D(str(g["lech"])) == D("1000000"), g


# ═══ AC-4 · `khoa_to` trên MỌI gd / gd_ds ════════════════════════════════
def test_AC4_khoa_to_LUON_CO_tren_moi_gd_va_gd_ds_hai_cua_danh_sach(ca_than):
    """⛔ Chiều ĐỎ: bỏ gắn `khoa_to` cho `gd` *(hôm nay — sổ thật **0 / 768**)*
    ⇒ ĐỎ; tập rỗng ⇒ ĐỎ."""
    ca, t = ca_than
    dem, thieu = {}, []
    for k in ("GHEP_MAY", "LUOI_VND", "GHEP_DA_GAN"):
        n = 0
        for x in t[k].get("rows") or []:
            th = x.get("the") or {}
            for g in [th.get("gd")] + list(th.get("gd_ds") or []):
                if not g or "amount" not in g:
                    continue
                n += 1
                if not isinstance(g.get("khoa_to"), list):
                    thieu.append(f"{k} {x.get('pm_line_id')} itl {g.get('itl_id')}")
        dem[k] = n
    print(f"WO-032 AC-4 · phần tử gd/gd_ds đo: {dem}")
    assert all(n > 0 for n in dem.values()), f"⛔ không đo được: {dem}"
    assert not thieu, "⛔ `khoa_to` vắng:\n  " + "\n  ".join(thieu)


def test_AC4_gd_DA_GAN_dien_giai_chua_so_CT_thi_khoa_to_CHUA_so_ay(ca_than):
    """Lệnh `B` *(đã gán, diễn giải sao kê chứa số CT)* ⇒ `gd.khoa_to` ∋ số CT,
    **cùng** luật `khoa_bang_chung` của cửa ứng viên."""
    ca, t = ca_than
    th = hang(t["GHEP_DA_GAN"], ca["lenh"]["B"])["the"]
    g = th["gd"]
    assert g["itl_id"] == ca["i_b"] and g["dien_giai"] == ca["dg_b"], g
    assert ca["doc"]["B"] in g["khoa_to"], g
    assert all(ca["doc"]["B"] in x["khoa_to"] for x in th["gd_ds"]), th["gd_ds"]


# ═══ AC-5 · bậc `khac_tien_te` ở `/so` ════════════════════════════════════
def test_AC5_toan_so_dong_USD_canh_lenh_VND_la_KHAC_TIEN_TE(ca_than):
    """⛔ Chiều ĐỎ: trả nhánh `else` cũ ⇒ `cung_tien_te` ⇒ ĐỎ; thiếu
    `khac_tien_te` trong `BAC_XEP` ⇒ cửa `500` ⇒ ĐỎ *(`goi_ok` đòi `200`)*."""
    ca, t = ca_than
    u = {x["itl_id"]: x for x in t["SO_A"]["ung_vien"]}
    assert ca["i_x"] in u, f"⛔ không đo được: `/so` ⛔ trả {ca['i_x']}"
    assert u[ca["i_x"]]["bac"] == "khac_tien_te", u[ca["i_x"]]
    assert u[ca["i_x"]]["lech"] is None, u[ca["i_x"]]


def test_AC5_KHONG_dong_khac_tien_te_nao_mang_cung_tien_te_ca_trang_toan_so(
        ca_than):
    """Quét **cả trang** `/so` cửa trả cho hai lệnh của ca *(`A` VND · `X` VND,
    `?q=` mã ca)*: ⛔ dòng nào khác tiền tệ lệnh mang `cung_tien_te`; mỗi dòng
    khác tiền tệ ⛔ khớp mã mang `khac_tien_te`.

    ⚠ Trang **⛔ lọc `q`** của kho TEST ⛔ đo được: cửa `/so` trả `500` —
      **có từ trước** `WO-032`, ⛔ do phiếu này: `chieu_tien` ném khi một dòng
      chưa nối có `ps_no`/`ps_co` đều `0`/rỗng *(kho TEST **11** dòng · sổ thật
      **0**, đếm 02/10)*. Khai ở `BG-034` *"Dev tự thấy còn yếu"*."""
    ca, t = ca_than
    sai, khac = [], 0
    for than in (t["SO_A"], t["SO_X"]):
        cl = _te(than["dong_lenh"]["curr"])
        for u in than["ung_vien"]:
            if _te(u["curr"]) != cl and u["bac"] != "ma":
                khac += 1
                if u["bac"] != "khac_tien_te":
                    sai.append((u["itl_id"], u["curr"], u["bac"]))
    print(f"WO-032 AC-5 · dòng toàn sổ khác tiền tệ lệnh ⛔ khớp mã: {khac}")
    assert khac >= 1, "⛔ không đo được: 0 dòng khác tiền tệ"
    assert not sai, sai
